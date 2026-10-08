# One shared effective response transfers across the SPARC sample

2026-10-04. New population calculation under the user's calibrated-observational
route. This is useful effective-model evidence, not established UNT superiority.

Calibrate one acceleration scale on51 galaxies and predict100 other galaxies,
with fixed stellar conventions and no galaxy-specific adjustments. The
inherited effective response substantially improves on ordinary baryonic
Newtonian gravity, and essentially ties the established empirical RAR curve.

| Predictor | Evaluation log-acceleration RMS, dex | Galaxy-balanced velocity RMS, km/s |
| --- | ---: | ---: |
| Baryons only | .569091 | 51.8206 |
| Inherited response, previous a0=1.2e-10 | .208563 | 18.6494 |
| Inherited response, calibration-only a0 | .201573 | 18.8128 |
| Empirical RAR, calibration-only a0 | .201590 | 18.7621 |

The fitted scales are1.005983328e-10 and1.002273917e-10 m/s^2, respectively.
Calibration minimizes galaxy-balanced mean squared log-acceleration residuals,
not velocity RMS: improvement in the former need not improve the latter.
The inherited response improves the chosen loss in93/100 evaluation galaxies
relative to baryons-only. It improves over RAR in49/100, with paired mean-loss
difference -7.0250e-6 dex^2 and descriptive bootstrap interval
[-4.6634e-4,4.8304e-4]. There is no resolved advantage over RAR.

## What the result adds

Previous detailed field work covered NGC3198 and DDO154. Both are excluded
here. The present test covers151 different galaxies, with1172 calibration
rows and1939 evaluation rows, split by a fixed SHA256 identifier rule.
All280 other source rows and exclusion reasons remain in the receipt.
Public archive exposure and RAR's prior development on SPARC are disclosed:
this is an in-program predictive split, not blind data or a novel RAR discovery.

The low-acceleration response is not confined to two selected examples. A
single normalization plus the existing shape captures much of the missing
rotational support across this sample. That supports pursuing a mechanism
that changes the response to ordinary matter. It does not identify which
mechanism is correct, compare against a full dark-matter population model,
or demonstrate that the network forms this response.

This test deliberately adopts an algebraic radial closure applied to the
published baryonic component curves. It is not a new full nonlinear disk
field calculation, nor a result for the unresolved K(X)/compression galaxy
state. The inherited saturation ratio remains a second physical calibration
input, not a derived parameter. M/L=.5 for disks and.7 for bulges are imported
source conventions; gas signs and the existing helium factor are preserved.

## Residuals point to specific work

Inner radii R/Rdisk<2 have RMS.25243dex; outer R/Rdisk>=4 have.12664dex.
The lowest central-brightness group has RMS.26258dex and positive bias.10539dex;
the highest-brightness group has RMS.14591dex and nearly zero bias. These
overlapping partitions do not establish a density effect. They identify
geometry, source calibration, circular-motion assumptions and the empirical
radial closure as concrete issues to distinguish. No troublesome row is removed.

Six nonfitted distance, inclination and stellar-mass sensitivities leave the
calibrated response well ahead of baryons-only; its RMS ranges.20067-.22385dex.
The small ordering difference relative to RAR changes sign. Inclination-plus
has95 evaluation galaxies/1843rows because some transformed inclinations
exceed90deg; any direct baseline comparison must use matching coverage.
These are coherent stress tests, not uncertainty marginalization. Full
radial covariance, calibration uncertainty and shared distance systematics
are absent. No chi-square probability or discovery claim follows.

## Verification and next prediction

All18 frozen numerical controls pass. Runtime5.41seconds, peak self RSS58MB;
the single worker exited. A separate4.9second saved-arithmetic audit verified
all source hashes, split/exclusions, raw-to-acceleration conversions, scores,
bootstrap summaries and sensitivity coverage, with maximum relative arithmetic
difference1.05e-13. The audit did not rerun fits/fields or the nonlinear stellar
sensitivity predictions. A pre-freeze fixed-width-parser failure is retained
separately; correcting the whitespace-expanded MRT parser changed no science.

The next useful observable is lensing with the galaxy-calibrated constants
held fixed, using the existing conditional metric coupling. A published
reduced-data check comes first; full shear/ESD inference requires covariance,
source distributions and distance conventions. In parallel the shared
expansion model must still explain its independent cosmological freedoms.
Inflation is prospective scope, not an achieved result.

Result: SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json
SHA256 f8502c04a3f17655172b2f589b48d1eebaa7c46bb64ad9950fd10d34ceb23aa9.
Freeze: SPARC_EFFECTIVE_TRANSFER_V001_FROZEN.json
SHA256 a3cf6c736a647877eb6a2daba06b5f481e00b5c63f8b23b3d831b8d31bada549.
Definitions and limitations: SPARC_EFFECTIVE_TRANSFER_V001.md.
The underlying observational conventions are from [SPARC](https://arxiv.org/abs/1606.09251)
and the [RAR analysis](https://arxiv.org/abs/1609.05917); this is our new fixed-split
calculation, not those papers' quoted scatter or likelihood analysis.
