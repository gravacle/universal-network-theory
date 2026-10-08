# First spatial common-phase diagnostic: clamped Kuzmin patch V001

2026-09-29. Prospective design approved in scope before implementation.
No new scientific producer, galaxy fit or change to frozen evidence.

## Decision and what the preceding result actually supplies

The saved finite-field census is COMPLETE: 1,296 occupied rows, 109,232
checks and no failed control. It demonstrates that a large change in the
phase-solved hard action can accompany a very small change in the direct
normalized flux. Consequently the next useful test is spatial: retain the
hard volume reaction, not merely insert the new flux in the old disk solver.

Implement one small axisymmetric clamped-source problem with both declared
gaps. Its question is whether this same local constitutive branch extends
to a resolved nonlinear spatial solution under fully explicit clamps.
It is not a prediction for NGC 3198, an isolated galaxy, cosmological
formation or the selection of the accelerated clock branch.

## 1. Fixed synthetic geometry and complete census

Use the already qualified Kuzmin sheet geometry, with a synthetic physical
scale a=3.2 kpc (the previously used stellar scale, not a fitted halo radius)
and GM=gstar*a^2. Thus

    Sigma(R)=M*a/[2*pi*(R^2+a^2)^(3/2)].                 (1)

The source is an externally supported, specified sheet. Its shape and mass
are not inferred from a rotation curve. Retain finite-R calibration source
spectrum index 1 (epsilon=.001, order128), reference index 0, and BOTH
R_hard=128 and8192. This is a declared numerical diagnostic subset, not
an observational selection or a claim covering the other references.

For each gap use boxes 0<=R/a,z/a<=L with L=1 and2 and grids16^2 then32^2.
Use the same exponential-edge mesh family already qualified for the disk
operator, with mesh scale1. The eight physical/grid cases retain two fixed
initial guesses each; publish every convergence/failure outcome. Domain
effects are differences between externally clamped patches, not estimates
of an isolated halo radius and not a quantity to optimize against data.

The initially considered old benchmark boxes L=8,16 are not used here:
their coarse outer cells could fail to resolve the cold finite-field
reaction length. This decision precedes the spatial outcomes. The smaller
patch is a genuinely limited geometry test, not a completed full-galaxy
domain disguised as a small mesh.

## 2. Dimensionless equations and boundary data

Let x=R/a, zhat=z/a and

    epsilon_scale=gstar*a/c_light^2,
    u=Phi/epsilon_scale, N=exp(epsilon_scale*u),
    g=|grad_hat u|, h=g/sqrt(1+g^2/S^2),
    mu=omega_R(I_b,0),
    omega_R(I,h)=mu*exp(-epsilon_scale*u).               (2)

Use the exact finite-gap source kernel, ground soft modes and unchanged
finite DeltaU. Define E,Pi,F,K_T,K_L,F_Phi,J exactly as in the reviewed
common-phase derivation. With d=grad_hat u-(F/Kb)grad_hat u/g, solve

    (1/x)partial_x(x*d_x)+partial_zhat d_z
       =epsilon_scale/Kb * [(E+3Pi)-(E_b+3Pi_b)].        (3)

There is no volume baryonic density above the razor-thin sheet. Its exact
upper-face flux is

    d_z(x,0+)=(1+x^2)^(-3/2).                            (4)

Axis flux vanishes. Impose u=0 at x=L and zhat=L. These are physical
mathematical clamps in this experiment, not an assertion of actual cosmic
matching at a finite galaxy boundary. The common mu is fixed; boundary I
is whatever (2) gives at the actual boundary field, not an independently
imposed cosmic I_b. No chemical potential is retuned between boxes.

For each radial bin [x_l,x_r], the incoming sheet flux divided by2pi is
exactly 1/sqrt(1+x_l^2)-1/sqrt(1+x_r^2). The geometric cell volume divided
by2pi is (x_r^2-x_l^2)*Delta z/2. An independently integrated flux ledger
must satisfy

    outer_flux = sheet_flux
       + epsilon_scale/Kb * sum_cells volume*delta(E+3Pi). (5)

The second term is an output of the same phase state, never a fitted halo.
Save its soft/hard pieces separately. DeltaU cancels only by the stated
FLRW-background subtraction; its original value, calibration and energy
identity remain in every case record.

## 3. Stable reaction and the analytic Newton operator

A useful hard-source identity is

    epsilon+3*pi_H/R_hard^4
                      =<z_mode^2>+(3/2)<z_mode^4>.       (6)

Explicit source terms cancel from (6), but its moments still depend on the
solved state. Subtract the cosmic unit-gap moment combination before
multiplying by beta*R_hard^4; retain the alternative energy/pressure
difference as an independent control. At exact Phi=g=0, use the exact
same calibrated baseline and zero reaction. Do not subtract two unrelated
rounded frequencies or reset the field-dependent minimum.

Let e=grad_hat u/g and

    K_ij=K_T delta_ij+(K_L-K_T)e_i e_j,
    T=E+3Pi, T_g=2F-F_Phi.

For a perturbation v of u, the continuum Newton map is

    delta d_i=(K_ij/Kb)partial_j v
                         -epsilon_scale*(F_Phi/Kb)e_i v,
    delta rhs=(epsilon_scale/Kb)
              [-epsilon_scale*J*v+(2F-F_Phi)e.grad_hat v]. (7)

Discretize these derivatives through the SAME face interpolation, boundary
values and cell-gradient operators used in the residual. Cached local
material derivatives suffice; do not perturb every unknown and repeat
all orbit inversions to build the Jacobian. Recheck the assembled Jacobian
with prospectively chosen directional finite differences away from an
empty/occupied switching point. Report active-set changes at that point.

The reaction makes this operator potentially indefinite or singular even
when both principal coefficients are positive. Existing positive-PCG
assumptions are therefore not inherited. Use dense linear solves of the
analytic Jacobian, with a residual line search, explicit singular/failed
step outcomes and bounded numerical iteration allowances declared in the
worker protocol. Neither a convergence failure nor one converged seed is
a theorem about all nonlinear branches. Never clip K to a favorable floor.

The two fixed seeds are u_seed and2u_seed, where

    u_seed=-(1-x^2/L^2)(1-zhat^2/L^2)
                              /sqrt(x^2+(zhat+1)^2).    (8)

They satisfy the outer clamps and axis parity. They are numerical seeds,
not claimed histories or solutions of the sheet jump. Both final branches
and their difference are retained; no preferred result is selected because
it produces a better force. A fine-grid case may also use the authenticated
prolongated coarse solution as a separately identified continuation, never
as a replacement for the two fixed-seed outcomes.

## 4. What qualifies the small spatial computation

The separate implementation protocol will freeze the numerical tolerances
before outcomes. Its essential controls are:

- Pure Newtonian Kuzmin verification with its analytic outer potential,
  source flux and force, plus the exact axis/volume geometry identities.
- Reproduction of the already saved local kernel at the corresponding
  selected reference states; fixed-cosmic-I is a labeled comparator only.
- Common-frequency/branch certificate, no clipped principal coefficient,
  exact reaction identity(6), and both independently refined quadratures.
- The nonlinear residual, analytic-Jacobian directional check, global
  flux balance(5), resolved sheet-normal inversion and both seeds.
- Grid comparisons of u, radial/vertical field, solved action and complete
  hard source; report cell width/local reaction length, not just Newton
  convergence. A coarse converged root is not automatically a resolved
  spatial solution.
- Retain absolute minimum/excitation, pressure, DeltaU, hard action
  inventory and outer flux. A fixed-mu static patch is an open-reservoir
  prescription; it does not prove a closed initial inventory assembled it.

## 5. Metric scope and omitted-term estimates

This first solve is the displayed weak-field lapse diagnostic, not a silent
Phi=Psi ansatz or a complete static tensor Einstein solution. The exact
stress and metric equations of MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001 remain
the reference. Save gF, Kb*g^2, 3delta Pi, the anisotropic stress components,
max|Phi| and the cosmological size ratio H*a*L/c_light.

An auxiliary scalar metric constraint can be reconstructed using the same
flux divergence and delta E, with explicitly chosen corresponding metric
clamps. Its pressure-only leading slip equation is

    Laplacian_hat[(Phi-Psi)/epsilon_scale]
                            =3epsilon_scale*delta Pi/Kb. (9)

Equation(9) is a partial leading-order diagnostic, NOT an exact lensing
prediction: the full trace has the -gF term and metric nonlinear terms
at the relevant next order, while the traceless spatial equation contains
the full anisotropic stress. Keep those computable contributions separately
and compare their absolute sizes/residuals with the retained source; do not
select one g^2 contribution while claiming all others vanish. Ordinary
disk support and boundary stress are externally owned clamps here.

A large omitted-stress or metric residual means that the clamped scalar
result is not yet a qualified full metric solution, not permission to
set Psi=Phi. Conversely a small estimated correction is not a proof of
cosmological formation, stable equilibration or a physically supplied
outer phase. Full production metric reconstruction is a subsequent step,
not a precondition for measuring this clearly labeled spatial response.

## 6. Resources and implementation division

At32^2 there are1,024 potential unknowns and one dense Jacobian occupies
8MiB. Vectorize orbit quadrature over cells/faces; arrays scale as
O(number_of_faces*quadrature_order), not a Hilbert-space dimension.
Caching derivative arrays and constructing local Jacobian stencils avoids
one source solve per matrix entry. Dense workspace plus batched128-point
quadrature is expected to remain below a few hundred MiB; measure one
16^2 unit before committing to the complete queue. Runtime is to be
measured, not promised or imposed as a research deadline.

The root is the sole producer. New inert code/protocol must be reviewed
and frozen before that first timed unit. All old sources, calculations and
failed cases remain unchanged. This is the next executable test of the
same density/polarization coupling, not another local response grid.

## Read-source identities

- FINITE_FIELD_PHASE_RESPONSE_V001_TRANSPORT.json:
  18788e16f5575da64a7e6ed527179bd7142b9cd42ce3d814f98642c81e76a3a2.
- SPATIAL_GALAXY_TEST_DECISION_V001.md:
  ba90f7d309768bfb72594bde7ea97cca511f3c8cb18328890b2aba9de148ec11.
- MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md:
  64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3.
- FINITE_FIELD_COMMON_PHASE_DENSITY_V001.md:
  cb8ec369a4e70f78b0bd54e2142f746bdf414c8982b141ba9027bd4958d7bb59.

The saved result was inspected without rerunning its producer or quadrature.
