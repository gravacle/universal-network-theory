# Galaxy-calibrated response and published lensing accelerations

2026-10-04. No-refit, conditional cross-probe comparison. The existing
stationary weak-metric prescription gives a concrete light-bending prediction
from the force response. This does not qualify the separate dynamical K(X)
branch or supply an alternative cosmological distance model.

The acceleration scale fitted only to51 SPARC calibration galaxies was kept
fixed at1.005983328e-10 m/s^2. No lensing or mass normalization was fitted.
The comparison uses the15 published reduced-acceleration bins of
[Mistele et al., Table1](https://arxiv.org/html/2310.15248v2), including its
distance, stellar/gas, isolation, spherical-deprojection and exterior assumptions.

| Predictor | RMS log residual in7 less isolation-sensitive bins | RMS across all15 bins |
| --- | ---: | ---: |
| Baryons only | 1.19168dex | 1.64279dex |
| Inherited response, SPARC-calibrated | .07949dex | .13388dex |
| Empirical RAR, SPARC-calibrated | .07739dex | .13308dex |

The7-bin subset uses gbar>=1e-13 m/s^2, based on the publication's isolation
warning. All8 lower-acceleration bins remain; the inherited response's RMS
there is.16757dex, with a largest residual.42187dex at the extreme low end.
The primary-subset mean residual is-.06698dex and largest magnitude.14799dex.
The table's reported errors and additional mass-scale sensitivity must be
retained when interpreting these numbers; no fit probability is assigned.

This is an encouraging transfer of the calibrated response to another probe,
but it is not a fresh distinctive prediction relative to RAR: both responses
remain similar. Stellar-population assumptions are shared with SPARC. The
published bin centers and deprojected accelerations are not a raw-shear forward
likelihood; bin covariance and source-lens weights are not supplied in Table1.
The table and qualitative published result were read before this comparison.
Calling it blindly acquired, fully independent or a Stage3 lensing pass would
overstate the evidence.

At the two fixed, nonfitted horizontal mass-scale shifts of+/-.2dex, the7-bin
inherited RMS is.05904/.17547dex. These are sensitivities, not alternative
best fits. The authors' approximately.1dex vertical mass band represents the
same mass uncertainty in another coordinate, not an additional independent
error to combine with those shifts. All shifts, finite-bin diagnostics and
point residuals are saved.

Independent source review verified the15 transcribed values, SI conventions,
metric-to-lensing factors and lack of a lensing refit. A syntax-only failure
before any calculation is recorded in the protocol. The corrected single
worker completed in under.1second. No old numerical result was rerun.
An independent saved-arithmetic audit then authenticated the receipt and both
SPARC-fitted scales, recovered all225 saved residuals exactly, and all45
summary groups within2.23e-16. No fit or force prediction was rerun. The
nearly zero all15-bin mean hides opposing primary/tail biases and is not
used as evidence of a precision match.

Next: use an ESD/shear data product with its covariance, consistent mass
distribution and cosmological geometry, keeping the galaxy constants fixed.
The older KiDS ESD release is documented at
https://kids.strw.leidenuniv.nl/sciencedata.php . Its bias corrections,
stacking and exterior assumptions must be incorporated before a joint score.
This small result motivates that test; it does not remove the independent
expansion/early-universe obligations or claim absence of dark particles.

Receipt: EFFECTIVE_NO_REFIT_LENSING_V001_RESULT.json
SHA256 05969f36703ddc8af54a88b1a2890264c03a9e90e98e9d23821a65f9d9e626a0.
Protocol: EFFECTIVE_NO_REFIT_LENSING_V001.md.
