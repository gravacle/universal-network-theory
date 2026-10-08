# Shared calibration gives a linked physical scale

2026-09-29. All 36 unchanged original-spectrum action templates were calibrated
against all 18 inherited late-time reference alternatives: 648 labeled rows.
All 7,327 arithmetic controls and 13,338 independent saved-arithmetic checks
pass. Runtime was 0.751219 seconds, peak self RSS 39,976,960 bytes.

Two shared scales, g* and S, were solved from the same state's positive
excitation energy and the existing absolute vacuum-matching rule. No separate
vacuum offset, dust abundance, per-galaxy parameter or radial population was
added. The historical reference acceleration was not used as a target.

Across the full census, g* spans 2.24246e-8 to 6.63737e-7 m/s², but the product
gs=g*S lies between 9.82690e-10 and 1.05819e-9 m/s². This restriction follows
from the exact relation

    gs = c H0 sqrt[3 Omega_Lambda / (1-d)],
    d = 2 W_el(S)/(I0 S²),  0 <= d < 1.

It is an internal consequence of the adopted common matching, not independent
observational confirmation. H0 and Omega_Lambda are model-calibrated references;
the baryon input inherits standard BBN. Their errors were not propagated.

For the previously designated template 6 and central reference 0:

- g* = 3.583833306e-7 m/s²; S = 0.002823442148.
- gs = 1.011874601e-9 m/s².
- Unchanged pressure/energy = 0.000609964535.
- The present acceleration-parameter shift relative to the reference dust
  state is Delta q0 = 0.000269007602, not zeroed by calibration.

The old relaxed acceleration coefficient is not the newly predicted galaxy
scale. Changing S changes the actual bounded source law. The finite-cutoff
quadratic-window diagnostic ranges from 0.342687 to 1235.75 across the census;
some branches have no such window at all, and a ratio only slightly above one
does not establish a broad one. New physical-field response and same-action
expansion-history tests are therefore the next linked outputs.

These 648 labels include old reference alternatives and numerical-resolution
controls; they are not 648 independent observations. Calibration is legitimate,
but success on its calibration targets is not predictive evidence. The same
standard applies to the previously fitted two-parameter halo comparators.

Evidence: `ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json`, its frozen
source/protocol, and `ORIGINAL_SPECTRUM_CALIBRATION_V001_REVIEW.md`.
Result SHA-256:
`1b155c6caf7ceb721db2f8766fa282b456b8c5f40d49555052ab4b0dc9a06abd`.
