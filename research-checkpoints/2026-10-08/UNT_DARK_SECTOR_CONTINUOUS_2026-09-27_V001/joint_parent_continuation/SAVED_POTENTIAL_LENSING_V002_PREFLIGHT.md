# Independent V002 lensing preflight

Accepted with no changes requested. Read the complete 310-line implementation
and method note, in addition to the already reviewed immutable V001 helper,
field sources and failed outputs. AST parsing passes; no module import,
synthetic computation or physical postprocessing was executed by this reviewer.

The local normalized four-node Lagrange basis and its analytic s derivative
are correct. Fixed clipped stencils retain nodal values and C0 continuity;
the derivative may jump at stencil changes, with no potential-jump delta
term. Axis regularity follows from dependence on R². The expanded node
census includes all four radial nodes at both heights, all extrapolation
dependencies, and the extra (0,0)-dependency refusal. Outer residual faces
remain zero. No previously undefined central potential is invented.

For `P3(s)+|z|Q3(s)`, the sky-gradient integrand has degree at most six
within each fixed ray segment. Four-node Gauss is exact in real arithmetic;
eight-node comparison is appropriate. Absolute basis/derivative corner
contributions correctly control cancellation-sensitive comparisons. The
independent face-on trapezoid remains exact in height for this interpolant.

The prospective synthetic plan contains 246 checks: 24 normalized
monomial value/derivative tests, 192 monomial-ray comparisons, 26 nodal and
stencil-continuity tests, two outer-face and two origin-refusal tests.
Direct analytic monomial gradients do not reuse the Lagrange derivative
implementation. Failure is preserved before real-field projections begin.

All twenty fields and 300 rays retain their original physical sources,
constitutive law, parameters, photon geometry and exterior. Authenticated
V001 spherical pieces and passing analytic controls are reused explicitly,
not counted as new independent integrations. Both reference-potential
orders are recomputed on the expanded dependencies. All 25 projected-mass
controls keep the original 1% target; no V001 failure is overwritten.

This is a justified interpolation repair following the independently isolated
monopole-subtraction defect. Passing the new computation is still required;
preflight acceptance is not a numerical or observational success claim.

Reviewed source SHA-256:
`b918971c05188ca984f765e070e1fb188ede2e4a98b1e61c24d97e50b23c720f`.
Reviewed method SHA-256:
`124b6cc9e199a6c19f78106ef16b458313f624172034008e5e33c9a9ac0b86bd`.
