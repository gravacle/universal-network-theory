# Clamped common-phase Kuzmin patch: numerical protocol V001

2026-09-29. Prospective inert implementation of
`CLAMPED_COMMON_PHASE_KUZMIN_PATCH_V001.md`. Root alone executes the worker;
authors/reviewers do not import or run it. No physics parameter, boundary,
seed, numerical ceiling or acceptance threshold is selected after outcomes.
Each case is a small rerunnable job, with no checkpoint or wall-clock deadline.

## Fixed family and question

Use the exact same finite-gap calibrated scalar macroscopic action and soft
ground spectrum, source index1/reference0, hard gaps R=128 and8192. The source
is an externally supported synthetic Kuzmin sheet with a=3.2kpc and GM=gstar*a².
Use both clamped boxes L=1,2 and grids N=16,32. Case order is the Cartesian
order `(R,L,N)` with N varying fastest, indices0..7. Every case runs BOTH
fixed initial guesses from the design, with multipliers1 and2. No favored seed
is selected and no prolongation replaces either guess. The first case measures
resources before the root continues the complete sequential queue.

The equation is precisely the displayed weak-lapse diagnostic with
epsilon_scale=gstar*a/c², u=Phi/epsilon_scale, G=|grad_hat u|,

    div_hat[grad_hat u-(F/Kb) grad_hat u/G]
             =epsilon_scale*delta(E+3Pi)/Kb.

Axis flux is zero, the lower sheet supplies its exact annular incoming flux,
and u=0 at both outer faces. Boundary action is solved from the fixed common
phase and actual boundary field, not separately pinned to cosmic I_b.
The unchanged DeltaU is saved; it cancels here only by the declared background
subtraction. These clamps are a conditional open reservoir, not physical
cosmological matching or a fitted halo boundary.

## Mesh, discrete residual and Jacobian

The exponential-edge mesh is expm1(linspace(0,log1p(L),N+1)), scale1.
Cells are at edge midpoints. The volume divided by2pi is
[(x_right²-x_left²)/2]*Delta z. Radial face area divided by2pi is x_face*Delta z;
vertical face area is the annular area. The sheet integral for each radial bin
is exactly 1/sqrt(1+x_left²)-1/sqrt(1+x_right²). No center-sampled approximation
replaces this flux. Its sum and the total box volume are separately tested.

Cell gradients use the nonuniform three-point Lagrange derivative, including
one-sided end stencils, equivalent to the inherited edge_order=2 operator.
Interior normal face gradients are center differences. Tangential gradients
and face potentials use the same opposite-width linear interpolation between
adjacent cells. At an outer face the normal difference uses the half-cell
distance, while potential and tangential derivative equal the declared
Dirichlet boundary values. There is no evaluated flux at the axis or sheet:
those are exactly prescribed. The residual is signed integrated outgoing
minus incoming flux divided by the proper cell volume, minus the retained
stable material reaction.

The dense Jacobian differentiates these exact linear maps and both material
terms, including the longitudinal square B_I²/e_II, F_Phi face coupling,
the cell -epsilon_scale*J phase derivative and (2F-F_Phi) gradient derivative.
No repeated material solve per Jacobian entry, PCG positivity assumption,
stiffness floor, diagonal shift or clipped principal coefficient is used.
The matrix can be indefinite or singular; such outcomes remain explicit.

## Material API and controls

The inert `clamped_phase_material_v001.py` receives authenticated saved source
and spectrum dictionaries; it reads/writes no files and imports no producer.
`Material.evaluate(Phi,G,order)` broadcasts arrays and returns E,Pi,deltaE,
deltaPi, stable deltaT with hard/soft splits, KT,KL,F,F_Phi,J,I,I_over_Ib,
branch and complete minimum/excitation diagnostics. Branch0 means empty,
branch1 occupied. Nonfinite/uncertified material requests raise a named domain
error, not an invented continuation. Origin-safe positive deficits handle
G=0; the empty-origin KT=KL=0 is not floored.

Hard deltaT is beta*R^4 times the difference of the unit-gap moment combination
<z²>+1.5<z⁴> from the same cosmic baseline. This is compared with the alternative
deltaE+3deltaPi. Absolute minimum, excitation and pressure remain intact.
Exact Phi=G=0 has zero background-subtracted reaction.

Primary quadrature is GL128, independent residual control GL64. Every final
retained state is reevaluated under both rules. The nine previously saved local
probes for the selected source bind E,Pi,KT,KL,F,F_Phi,J to the frozen result.
Final cells/faces retain common-frequency errors and check energy, pressure
and reaction identities. No new native formation or state-selection claim
follows from this numerical qualification.

## Solver and prospective numerical controls

Dense Newton uses at most40 updates per seed. Each update tries the full step
then up to18 halvings, accepting an integrated-L1 residual decrease satisfying
1-1e-4*damping. The residual norm is sum(volume*abs(residual))/total_sheet_flux.
Stop as converged at norm<=1e-9. Retain iteration history, damping, rejected
material-domain trials and final state for iteration limit, singular matrix,
nonfinite step, line-search failure or material-domain failure. A iteration
allowance is a numerical solver condition, not a program/milestone stop.

Before nonlinear seeds, solve the pure Newtonian Kuzmin problem with exact
analytic outer potential and tangential derivatives. Prespecified tolerances:
maximum potential error normalized by maximum analytic potential .02; RMS
vector-gradient error normalized by analytic gradient norm .05; residual1e-9;
global flux2e-8. This tests the actual FV geometry, not just pointwise formulas.
If these geometry/Newtonian/material-anchor prerequisites fail, publish
FAILED_PREREQUISITES and the failed evidence with both fixed seeds explicitly
unstarted. Do not spend further physical Newton work on a known unqualified
operator. This is a numerical repair condition, not a physical branch result.

At each final material-valid seed state, check the dense analytic Jacobian in
two fixed directions: sin(pi*x/L)sin(pi*z/L) and
cos(pi*x/(2L))sin(pi*z/L), each normalized in maximum norm. Central steps are
1e-5 and5e-6 times max(1,max|u|). The volume-weighted directional relative
error must be<=2e-5 away from switching. An empty/occupied active-set change or
domain failure is explicitly recorded rather than evaluated as a smooth
derivative. No directional check at a switch certifies a global branch.
The output records the number of actually checked comparisons and an explicit
Jacobian qualification flag. It is qualified only if all four prescribed
comparisons are checked and pass; all ACTIVE_SET_SWITCH outcomes can never
be mistaken for successful Jacobian qualification. A converged residual alone
does not override that flag.

Arithmetic/identity tolerance is2e-11; material/quadrature tolerance2e-8.
The GL64 residual difference is integrated and scaled by the larger of sheet
flux and absolute integrated volume source. The exact independent flux ledger
outer=sheet+volume is compared to the integrated residual, and converged seeds
must satisfy the2e-8 flux gate. These are numerical gates, never gates on the
sign of the physical state response or on which seed looks preferable.

Postprocess the sheet normal derivative by bin-average prescribed flux at the
linearly extrapolated sheet potential/tangent field. Use at most40 positive
bracket doublings and64 bisections; retain all failures and final KT/KL.
This is a local recovered-flux diagnostic, not a theorem of unique normal
inversion for all possible roots, and does not alter the prescribed FV flux.

## Retained output and resolution meaning

Each case saves both full u fields, gradients, source reaction and hard/soft
volume contributions, material action and absolute energy ledgers, outer flux,
seed difference, all solver outcomes and numerical controls. It records local
length/a=sqrt(K/J)/epsilon_scale and cell_width/length with explicit validity
masks/nulls, not a selected halo radius. The inventory sum(volume*I) is per-copy
dimensionless action. Its leading physical hard phase charge multiplies by
C*beta*2pi*a³; exact spatial metric factors would additionally be needed. The
fixed-mu clamped patch is not asserted to have a closed conserved inventory.

After all eight cases, a separate saved-data comparison must pair N16/N32 by
the same gap,box and fixed seed, using interpolation to shared points for u,
radial/vertical fields, I and full hard reaction; and pair L1/L2 only in their
common inner region, naming the changed clamps. This collector is not yet
implemented in this producer. No coarse converged root is labeled spatially
resolved merely because Newton and flux gates pass. All cases are retained
before interpreting grid/clamp/seed dependence; no observed rotation samples
are consulted.

Save max|Phi|, H*a*L/c, gF, Kb*G², 3deltaPi and anisotropic components -gF e_i e_j
as omitted-term diagnostics. The parent design's optional scalar slip equation
is not solved by this first driver; no full tensor residual or lensing result
is claimed. Their comparable sizes can invalidate a full-metric interpretation
without invalidating the limited scalar diagnostic.

## Custody and execution

`freeze` authenticates the complete finite-gap and finite-field input streams,
recursive freezes, source/calibration maps and new source/material/protocol.
Root publishes its exact JSON before `run-case 0..7`. Each command verifies
that snapshot first. Stdout is a compressed complete wrapper with freeze and
canonical payload hashes. Root may use its already tested acknowledged paged
capture holder; publication is through apply_patch, not producer file writes.
Numerical-library thread counts are1 and bytecode writes disabled. No network,
subprocess, checkpoint, scientific execution at authoring time, or implicit
next job occurs. Status COMPLETE_RETAINED_OUTCOMES means the controls ran and
all outcomes are present; inspect each seed status separately for convergence.
