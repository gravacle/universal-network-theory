# Unused expansion distances constrain the existing shared calibration

2026-09-29. The declared13-point DESI DR2 expansion-shape calculation is
complete. All1160 prospective numerical checks passed. The independent saved-
result audit also passed6747 arithmetic checks; see DESI_BAO_SHAPE_V001_RESULTS_REVIEW.md.
The source preflight was accepted before scoring.

The result is useful calibration information, not a contest won by relabeling
the same expansion function. The adopted ideal balanced hard-mode parent
has the same flat dust-plus-vacuum background shape as its reference model.
At identical parameters their predictions agree to3.44e-16 relative precision.
These data can test our existing parameter choices, but cannot distinguish
those two physical interpretations in this exact limiting background.

## Results, with fitting freedom counted

All18 inherited reference alternatives were retained. They reduce to THREE
distinct expansion shapes, not18 independent experiments. Each shape fits
one common acoustic-distance amplitude A=c/(H0*r_d); it does not predict r_d.

| Expansion choice | Omega_m | Fitted A | Full-covariance chi-square |
|---|---:|---:|---:|
| Existing lower matter-fraction alternative | .316 |29.9429595|14.5940516|
| Existing central calibration | .334 |30.3365758|26.0295371|
| Existing upper matter-fraction alternative | .352 |30.7188733|43.3021768|
| Same shape family with Omega_m additionally fitted | .297461821 |29.5246334|10.2710410|

The last row has TWO parameters adjusted to these distances, not one. It is
also an available expansion fit for the ideal network family, but it is NOT
one of our frozen outside-calibration predictions. Adopting it would be a new
global calibration to carry into other observables, not permission to reset
each galaxy independently or claim this dataset was predicted afterward.
The chi-square reductions relative to that fitted family are4.32301,
15.75850 and33.03114 respectively. No significance, posterior, information
criterion or success threshold was selected in this protocol.

The concrete implication is that these observations favor less total
pressureless gravitational weight than the central inherited reference,
within this shared background family. They do not determine whether that
weight belongs to particles or the adopted network excitation/polarization.
The latter retains real positive excitation energy; this calculation does
not remove the gravitational energy budget by changing its name.

## What was actually tested

All13 published survey-inferred distances, their supplied full covariance,
and all six transverse/radial pairs were used. The final Ly-alpha pair's
DH-then-DM ordering was retained. One amplitude is common to every redshift.
The original Gaussian vector was scored; derived AP ratios were only displayed.
No galaxy source, force curve, state population or time scale was retuned.

The independent257/513-point profiles retain both endpoints and every sampled
local minimum, refined without a target score. Their selected Omega_m differs
by7.48e-10 and chi-square by1.60e-14. The separately constructed Simpson
distances agree with Gauss distances within1.36e-13 over all checked reference
and comparator candidates. This is numerical profile convergence, not an
analytic global-optimality theorem or a joint cosmological likelihood.

Ordinary-radiation sensitivity was separately calculated without rescoring or
refitting. Across all108 stated photon/illustrative massless-neutrino alternatives,
the conservative distance-change bound over0<=z<=2.33 is at most0.039625%.
The original physical dust and vacuum coefficients were held fixed, so the
radiation-added H(0) shifts explicitly. This bound applies only to the named
radiation assumptions, not finite-gap pressure, nonstandard photons or the
network clock. The acoustic ruler and survey-template assumptions are not
derived by this test.

## Custody and interpretation

Primary observations and release conventions:
[DESI DR2 BAO paper](https://arxiv.org/html/2503.14738v3).
Exact input provenance is in desi_dr2_bao_external_v001/README.md, with pinned
repository commitbb0c1c9009dc76d1391300e169e8df38fd1096db and both byte hashes.
This was outside our calibration, but explicitly NOT blinded: prior exposure
to a Ly-alpha summary and the paper's fitted score is recorded. No observational
outcome was used to change the source, tolerances or selected vector.

Raw output: DESI_BAO_SHAPE_V001_RESULTS.json.
Payload SHA-2564921a95442fbe24c74e6bf0c7b4fa28ae99df3ab1b07b1635508e519411ae6b3.
Source/protocol and complete ancestry: DESI_BAO_SHAPE_V001_FROZEN.json.
The one sequential worker used .171185 seconds and37,208,064 bytes peak self
RSS and exited. Numerical COMPLETE does not certify the physical candidate.

The next discriminating work remains the SAME finite-state galaxy/lensing
response and its linked early history and clock: those carry consequences
not captured by this identical ideal expansion shape. A joint calibration
must use the actual calibration likelihoods and retain the unused-data ledger;
the18 discrete inherited alternatives are not an uncertainty posterior.
