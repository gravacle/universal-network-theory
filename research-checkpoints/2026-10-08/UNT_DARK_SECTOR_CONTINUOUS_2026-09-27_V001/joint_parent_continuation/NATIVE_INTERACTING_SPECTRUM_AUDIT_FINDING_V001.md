# Independent audit finding: weak near-degenerate source curvature

2026-09-29. The first independent saved-projector recombination stopped at an
absolute `1.2789883970144047e-10` mismatch in an excited energy-source
curvature. No producer source, freeze, result or scientific tolerance was
changed. Follow-up matrix arithmetic identified the conditioning issue:
`Tr(P_a M P_b M)` has cancellation for forbidden/nearly forbidden lines;
roundoff-sized strengths are then divided by near-degenerate energy gaps.

For example, at q=0, h=0.00625, full-spectrum cluster 5 has saved energy-source
curvature `-4.658865165324921e-6`. Reconstructing the mathematically equivalent
positive strength `||P_a M P_b||_F^2` from the same saved projectors gives a
curvature approximately `1.46e-19`. Cluster 6 changes from
`4.658981885742138e-6` to approximately `1.36705e-10`. Their energy separation
is only `1.0172129805141594e-10`. The error is in a secondary derivative of
the weak-flip controls, not a change in the native h=1/2 spacing result.

The manifestly nonnegative norm-square representation should be used in an
additive saved-projector correction, with its own identities, checks and
remaining projector conditioning qualifications. It requires no new
eigenproblem. The main h=1/2 curvatures, ground susceptibilities and the
bright transition-spacing readout do not show this discrepancy at the
prospective absolute 1e-10 level.

The independent audit records the raw-versus-positive derivative differences
explicitly instead of changing its tolerance or calling every V001 derivative
independently qualified. The original V001 producer reported all its own
controls passing; this secondary cancellation was not caught by those
controls.
