# Independent two-current source/scope preflight V001

Read completely, without import, material evaluation, integration or other
numerical execution:

- `spherical_two_current_v001.py`, 429 lines,
  `0349740de7d0b4173f634eaf8fd52c7e5eb4ea9ea196f95a5b882024f6dd95df`;
- `SPHERICAL_TWO_CURRENT_FINITE_R_DESIGN_V001.md`,
  `4733e51a4bf5646861ec3123ab5799b3b3e5662faf8a449b8eb54f7cd4f661c1`;
- `SPHERICAL_TWO_CURRENT_PROTOCOL_V001.md`,
  `c124a0e0a361a33860ec4e0470b0380758405740bdb8b7d9f45783b0bf9a5ba2`.

No load-bearing mathematical or source-scope correction identified.

The material uses the conserved rest current, not total energy reinterpreted
as independently adjustable mass: rho0=S beta R I/c^2, internal energy
u=S beta(e-RI), p=S beta(I omega-e), and
cN^2=(omega/R)cI^2 c^2. The stable period excess and action derivative in the
source reproduce these definitions. The fixed-label positive cell masses and
separate ordered species meshes implement a declared variational spatial
approximation, not collisionless multistreaming.

The union-grid potential integrals and face derivatives agree with the
displayed W0. In particular, code `0.5*sum(m*(av+bg))` is correct because av
already contains self+background: self energy has its half, while the fixed
background potential enters with full weight. The finite-volume pressure
force is minus the derivative of U. Canonical momentum p=A*w*v and
xdot=p/(A^2*w) produce the correct Hubble drag and normalized gravity/pressure
accelerations. The total, mechanical, hard-specific, and baryon work ledgers
have mutually consistent signs, including explicit outer pressure work and
the separate -H*W term. Removing pressure in the dust control does not qualify
its retained internal-energy ledger; the source/protocol correctly exclude it.

All 12 inherited-state/interface/width cases, three time methods, four epochs,
both species, signed gradients and energy diagnostics are retained. Input
ancestry is hash-bound and no producer is imported. The controls test actual
operator derivatives, material anchors and time integration rather than an
observational success criterion. Failures and nonfinite states are retained.

Acceptance is only for the proposed calculation. Exact conservation of the
discrete action is not spatial continuum convergence. The prior characteristic
inequality is conditional on its domain guards; discrete-stage checks are not
an interval proof. Exterior traction is an owned finite-domain condition, not
a derived cosmic reservoir. Rest-gravity/internal-energy and radiation
omissions, weak initial geometry, and the lack of full Einstein/Weyl evolution
remain explicit. No halo, lensing, merger, shock continuation or observed
agreement is certified by this source preflight.
