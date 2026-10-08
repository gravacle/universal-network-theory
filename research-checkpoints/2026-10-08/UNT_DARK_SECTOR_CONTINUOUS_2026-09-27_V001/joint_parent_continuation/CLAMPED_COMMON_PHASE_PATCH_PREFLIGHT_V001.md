# Clamped common-phase patch: independent driver preflight

2026-09-29. Read-only mathematical/code review by the material author; no
producer import, numerical integration, solve, or outcome inspection. This
is an independent review of the driver, not an independent authorship claim
for the material module, which was separately read by the driver author.

Reviewed complete driver and protocol, then their final prerequisite and
directional-check qualification additions:

- `clamped_common_phase_patch_v001.py`: `c4279bb3690174f2158eb46c46b23adfed008c9585e5f2bf381e0eb04744a3b3`.
- `CLAMPED_COMMON_PHASE_PATCH_PROTOCOL_V001.md`: `b867a6db67d8bfcc1746bbf14830acd8a10c36bfbaa31dc049bb045f21bb7daa`.
- Material interface reviewed against `clamped_phase_material_v001.py`:
  `d8472d6d585167bab8756a9451254693aab675294c86aa4321ff56d50c5cc7a8`.

No load-bearing defect found. Opposite-width interpolation gives the stated
face potential and tangent derivative; center differences give the normal
derivative. Radial areas, annular vertical areas, positive outgoing flux,
negative incoming sheet flux, and the telescoping global flux ledger have
the declared axisymmetric normalization. The Newtonian control uses its
own analytic boundary data, not the clamped model's zero potential.

The dense Jacobian differentiates the actual discrete residual. In particular
it retains the material tensor with both transverse and longitudinal
coefficients, the face term `-epsilon*F_Phi*n*delta_u/Kb`, and the cell terms
`+epsilon^2*J*delta_u/Kb` and
`-epsilon*(2F-F_Phi)*n.grad(delta_u)/Kb`. This is not an SPD assumption.
At zero gradient the exact isotropic limiting coefficient is used; no
positive stiffness floor or alteration of the empty phase was introduced.

Energy, pressure, minimum, excitation, and the complete hard and soft
reaction remain separate. The stable forced-orbit identity is
`e+3p=<z^2>+3<z^4>/2`, with
`p=<z^4>/4+eta<z>/2`; the quartic pressure sign is positive.
The alternative energy/pressure reaction identity and the saved local
material anchors qualify the interface rather than choose a physical sign.

Failed prerequisites retain both seeds as explicitly unstarted. All later
seed outcomes remain present. An active-set or domain event cannot be called
a passing smooth Jacobian test: qualification requires all four prescribed
comparisons to be checked and pass. A converged coarse residual is not a
claim of spatial resolution, stable evolution, an isolated galaxy boundary,
or a complete tensor metric/lensing solution. The prescribed post-run mesh,
clamp and seed comparisons remain necessary for interpreting this diagnostic.

The code is ready for the parent's separately authorized frozen first-unit
test. This preflight makes no claim that those numerical gates have passed.
