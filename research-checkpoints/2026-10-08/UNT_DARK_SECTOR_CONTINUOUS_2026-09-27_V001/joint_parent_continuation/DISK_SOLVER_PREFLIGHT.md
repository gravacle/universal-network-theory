# Disk solver preflight

2026-09-28. Independent analytical/source review before the first numerical
run. Read the complete `DISK_SOLVER_PROTOCOL.md` and `disk_solver.py`; no
solver was executed by this reviewer. The implementation belongs to the
parent agent. Source hashes and completed-case outcomes must be checked
after its final prospective amendments and freeze.

## Mathematical findings

No field-equation or normalization blocker was found.

1. The adopted law uses the earlier internal normalization `Kb=1/2`,
   `a0_int=8/(3*pi)` and `gs_int=r*a0_int`. Its returned flux is
   `f(g)=F_b(a0_int*g)/(Kb*a0_int)`. Thus both argument and flux have
   acceleration units `a0=1`, and the shape ratio is unchanged. The stable
   expression combines `2*F_el(h)*h'` with the positive compensated term,
   avoiding subtraction of nearly equal high-field terms.
2. The inverse bracket is guaranteed for these nonnegative inputs. With
   `r=gs/a0`, `f(g)>=g[1-(1+(g/r)^2)^(-2)]`. The selected upper endpoint is
   at least both `2r` and `2d`, so its flux is at least `(48/25)d`.
   Strict monotonicity of the already derived law gives the unique inverse.
3. Integrating the cylindrical equation with the common `2*pi` omitted
   gives radial conductance `R_face*h/h=R_face` and vertical conductance
   `(integral R dR)/h=R_center`. Dirichlet half-cell distances supply the
   factor two. The axis has exactly zero face radius and zero flux.
4. For the upper half-space the sheet condition is
   `mu*partial_z Phi=2*pi*G*Sigma`, not `4*pi*G*Sigma`. For the benchmark this
   is `eta/(R^2+1)^(3/2)`. Its annular integral is exactly the implemented
   difference of inverse square roots. Because the outward normal on the
   bottom points downward, its contribution to the positive matrix equation
   is negative on the RHS, as implemented. The retained mass is
   `eta[1-1/sqrt(65)]`.
5. Shared internal-face coefficients make the Picard matrix symmetric in
   the undivided finite-volume variables. Its quadratic form is a sum of
   positive conductances times squared neighbor differences plus positive
   Dirichlet terms. Thus it is SPD when face coefficients are positive;
   ordinary Euclidean PCG and the diagonal preconditioner are appropriate.
6. The nonlinear coefficient uses both gradient components. Boundary
   tangential derivatives agree with the differentiated exact boundary
   potential. The prescribed bottom flux needs no separate unknown bottom
   `mu` coefficient. One-sided extrapolation to the continuous disk
   potential is consistent despite its nonzero one-sided vertical slope.
7. Exact finite-domain boundaries are an oracle for this numerical
   benchmark, not a claim that arbitrary galaxies have this boundary or a
   potential vanishing at infinity. The score tests the true projected disk
   field rather than applying a scalar response to its radial component.

## Narrow prospective implementation corrections

Before any output, the parent proposed requiring the already declared
global flux tolerance along with the nonlinear residual before exiting
Picard, and tightening the inner PCG tolerance to `1e-12`. This is sound:
normalizing the residual by a boundary-potential RHS alone need not enforce
the relative sheet-mass balance.

The initial source wrote directly to final case filenames. An interruption
during that write could prevent the promised fresh restart of a small case.
Requested correction: publish only a completely serialized temporary file,
preserving incomplete files separately. Also verify resumed payload `N`
and `eta` against the case being requested, and recompute its refinement
comparison against the preceding verified case. These are case-integrity
corrections, not additional scientific acceptance criteria.

With these narrow amendments, the protocol is ready for the parent's frozen
single-worker benchmark. Passing it would qualify this discretization on
the exact disk family; it would not independently establish the physical
field equation, a galaxy fit, or a cosmological completion.
