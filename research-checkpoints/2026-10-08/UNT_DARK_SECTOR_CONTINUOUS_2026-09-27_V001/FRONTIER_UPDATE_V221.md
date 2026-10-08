# Frontier update V221: critical grid stiffness measured

2026-10-06 UTC, after13:01 diagnostic closure. Ordinary continuation remains
ACTIVE on this Mac. The measured NGC3198 recovery42904/session45327 and
original coefficient18459/session88165 retain root ownership. The former
is now on the final epsilon1e-3 group; none of its first12 cases converged.
No live source/state was changed or duplicated. Old Goal/heartbeat remain
paused; no scheduler or automatic resumption.

Independent small diagnostic47083/session29283 naturally CLOSED exit0,
13:01:31.641468→13:01:33.362089UTC. It evaluated manufactured zero-field
gradient projections, not galaxy trajectories. Frozen source63363c94d8a96a0444ab932f360f6bf9501fc1020064b509f5faf7e37f0e42bf
and protocolc3ab70d3274feb39499c2b0eca482686085071362657a4766a93ecba071f00f9.
RESULTeb99696cfc5ff635cc56dbe3dd128f7ce7032529ff62f0c4037f0b3cfc346300 /
RECEIPTfe87ff6b30ae9d3086319e70a6cf5798e6aa3b0c9aabe1a781bb2e821820b474.
Root and independent FULL saved closure accepted11 unique inputs+self,
12 receipt outputs/13 files including receipt, all0444, eight direction/mesh
cases, two known controls and four symmetry predicates. True residuals
<=9.71460e-11; Schur/direct-energy identity error<=2.82551e-16. Exact
algebraic residual energy bounds and a separately declared numerical
allowance resolve every reported ratio; no rigorous binary64 interval claim.

Continuous Q1 native vectors cannot reproduce the generally discontinuous
gradient of a Q1 lapse. At zero field the discrete critical scalar response
contains Qlock=K-B^T M^-1 B>=0, in addition to the physical ell contribution
and negative phase-pressure contact. The illustrative uniform1D defect is
h^2*q^4/12. The actual cylindrical diagnostic measures:

| Fixed trial | Coarse Qlock/Qell | Refined Qlock/Qell | Refined/coarse Qlock |
|---|---:|---:|---:|
| global p2 |558.759849|134.658964|.243152863|
| global p3 |328.525080|78.044438|.239008801|
| global p4 |237.056276|56.399833|.238966641|
| interior support |47.274610|10.610639|.228958314|

Halving the inner spacings/doubling outer nodes reduces projection stiffness
to roughly one quarter, while the physical contribution changes only
.441–2.010%. This is a substantial manufactured zero-field spatial defect,
including after one refinement. It does not measure the actual nonzero
quartic branch's force bias or prove that it caused a specific solver stall.
The current and refined coarse grids therefore cannot qualify the critical
response solely through symmetric-Jacobian or nonlinear residual checks.
Neither pressure curvature nor failed physical tests are reinterpreted.

Three narrow1e-6 recovered cases are cap-adjacent with remaining gap fractions
6.79e-7–4.39e-6; fourth is an interior linear failure with13.84% room. All
original18 necessary stationary-width failures remain. Wider completed
cases are still unresolved iteration/linear attempts, not curve predictions.
All accepted states, failed partial directions and complete histories remain.

Next useful numerical recovery is fixed-whitening MINRES on the unchanged
symmetric indefinite Hessian, authenticating the saved accepted state and
partial coordinates, checking the true residual against the inherited
inexact target on every accepted exit. Its code/protocol are not yet frozen
or launched. It must await42904 natural closure/receipt and ownership check;
no physical law or pressure sign changes. A successful coarse solve still
needs a compatible-space/refinement comparison. Broken Q1 native vectors
with consistent symmetric interior-penalty ell energy are a concrete
faithful correction; jump-only springs or unrelated staggered stencils are
not. Axis/sheet/exterior layers and nonlinear quartic quadrature also remain.

The shared background result and constructive current/momentum equations
remain V220 evidence. Static/background effective assumptions include A,
Q0*I0, epsilon,a0,ell,KB; A is an adopted vacuumlike endpoint and I0 an
adopted abundance, not derived microscopic initial budgets. Dynamic clocks
and preparation add obligations. No fitted galaxy halo is introduced, but
native attribution and fair comparative cost must count these assumptions.
All11 Stage3 lanes remain OPEN. No observed same-law force, superiority,
absolute nonexistence, physical primordial/thermal origin or completion.
Canonical seven dirty URM files and all earlier sealed/failed/partial work
are preserved. Exact next: finish42904, recover its actual unfinished work
with a reviewed solver, then qualify spatial response and physical matching.
