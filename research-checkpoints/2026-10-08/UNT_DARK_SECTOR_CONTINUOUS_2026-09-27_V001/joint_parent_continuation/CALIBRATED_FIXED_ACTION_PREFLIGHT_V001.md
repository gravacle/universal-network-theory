# Independent calibrated-field preflight

2026-09-29. Complete new source, protocol and analytical prediction note read,
along with the reused centered-orbit functions. No execution by this reviewer.
Accepted for the declared local, fixed-action constitutive census.

- `calibrated_fixed_action_v001.py`:
  `8bbbb95b8df1123c09ff4ec888bed7a2a068d7d3094c1a2ba8a4b3408cd50d91`
- `CALIBRATED_FIXED_ACTION_PROTOCOL_V001.md`:
  `217d63346b031a449aa3f6ad92b27c8baa8e01ea5b760950b1f2eab263f2dab3`

Each branch uses its new `G=g/g*`, `h=G/sqrt(1+(g/gs)^2)` and `hprime`;
the reused orbit function contains no inherited `gs` substitution. Its same-I
radius solve and cancellation-safe energy controls retain the previously
qualified kernel and tolerances. Both calibrated and kernel source/results
are authenticated transitively before execution.

The physical force `g*(G-hprime B/I0)`, actual finite-spectrum relaxed force,
stable universal lower bound, zero-source slope, and work difference
`I0 G^2/2 + minimum + excitation - E(0)` have the correct normalization.
The high-field coefficient `C3=gs^4 B(S)/(I0 S)` has acceleration-to-the-fourth
units and follows directly from the retained bounded source, not a finite-field
fit. The scalar force-order theorem justifies the inequalities but not a
derivative, stability or galaxy-PDE substitution.

All 648 branches, three fixed physical fields each, 648 saturation limits and
36 origins remain labeled. Caching identical source values does not discard
reference alternatives. No fit, new preparation, continuum approximation or
physical clock is introduced. This linked local response is not yet a
spatial galaxy solution or a demonstration that homogeneous isotropic and
radial scalar states have the same physical realization.
