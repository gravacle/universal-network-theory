# Direct lensing prediction: progress and unresolved tension

2026-10-04. Same older conditional stationary force law as the galaxy screen;
no new halo, force scale, slip or lensing normalization was fitted. This is
not a formed K(X)/compression galaxy, a full cosmological likelihood or a
completed Stage 3 lane.

## Scientific result

The galaxy-calibrated response substantially improves on Newtonian baryons
alone in direct ESD space, but the nominal isolated KiDS-bright comparison
does not agree within its published statistical covariance. It is nearly
indistinguishable from the galaxy-calibrated empirical RAR. The smaller,
spectroscopically selected GAMA control is less discrepant, with larger
errors. Both outcomes must be retained; neither establishes superiority.

All entries below are Q=(prediction-data)^T C^-1(prediction-data), evaluated
at the published acceleration-bin centres with zero lensing refits. Q is
a measurement-covariance diagnostic, not a complete rejection significance.

| Profile and fixed range | Baryons only | Inherited effective response | Empirical RAR |
| --- | ---: | ---: | ---: |
| KiDS, seven primary bins, gbar>=1e-13 SI | 739.567 | 64.107 | 62.217 |
| KiDS, all 15 bins including isolation-flagged tail | 1625.784 | 169.790 | 167.671 |
| GAMA, same seven primary bins | 58.011 | 15.943 | 15.818 |
| GAMA, all 15 spectroscopic-selection bins | 95.942 | 20.253 | 20.107 |

GAMA's lower Q does not automatically mean smaller physical residuals or
better evidence: the smaller sample has larger statistical errors. Its
eight low-acceleration bins give Q=4.333 for the inherited response, while
the seven higher bins still give Q=15.943. Source shapes and footprints
overlap; there is no supplied cross-sample covariance. Do not add these
scores or attach a significance to their difference. The paper's qualitative
sample comparison was already exposed; these are not blind discoveries.

## What changed scientifically

Instead of treating the published SIS conversion g=4G DeltaSigma as a
general identity, we projected the actual candidate force into photon
deflection and ESD. The conditional compact spherical prediction is

    DeltaSigma(gbar) = sqrt(a0 gbar)/(pi G)
                       integral_0^(pi/2) sqrt(x)/f'(f^-1(x)) dtheta,
    x=(gbar/a0) cos^2(theta).

It is independent of lens mass at fixed gbar in this ideal family. Thus
the public acceleration-binned stack can be tested without replacing a
distribution of masses by one mean mass. Unknown within-bin pair weights,
extended gas, angular structure, external fields and exterior matching
still limit that simplification. Phi=Psi is the older adopted stationary
metric bridge, not a consequence of a rotation fit or proof of current
network formation. The Newtonian point-source and deep 1/r limits were
checked independently, as was a second derivative-free projection formula.

The same a0=1.0059833281731022e-10 SI from the 51-galaxy calibration was
held fixed. The shape r=25.51664211557329 remains inherited from earlier
cosmological matching, not newly determined by these low-acceleration data.
The empirical-RAR comparator retains its own galaxy-calibrated a0. The
model is still an effective response, not an independent UNT-specific
observational signature. Newtonian baryons alone is not the full DM model.

## What can and cannot explain the KiDS tension

In the primary bins, the inherited centre prediction undershoots the first
six measurements by approximately 13–39%, then overshoots the seventh by
about 15%. The mean log residual is -.09872 dex and RMS .12788 dex. The
earlier Mistele reduced-acceleration RMS .07949 used a different reduction,
mass convention and selection; it was never the likelihood calculated here.
These overlapping KiDS results are not independent confirmations.

Centre, uniform-log and uniform-annular-area bin averaging give primary
Q=64.107, 68.886 and 72.975. The latter two are explicit approximations to
missing source-pair weights, not reconstructed true averages.

A post-screen robustness calculation gives an optimistic lower bound on Q
for any positive normalized within-bin weights, CONDITIONAL on the endpoint
predictions bracketing the continuous profile in each bin. Monotonicity was
numerically checked, not certified by an interval proof. For the selected
covariance, D=diag(sqrt(Cii)) and R=D^-1 C D^-1,

    Q >= sum_i distance(data_i,[prediction_low_i,prediction_high_i])^2/Cii
         / lambda_max(R).

This follows from the Rayleigh bound and interval distances; it is not a
seven-parameter fit. lambda_max(R)=1.0160343. The nominal inherited bound
is Q>=30.064 (baryons>=703.190, RAR>=28.625). Bin weights alone therefore
cannot bring the nominal model to a Q near seven within the stated envelope.
The tabulated all-lower/all-upper edge scores are NOT bounds on Q.

Unfitted fixed-catalogue total-baryon shifts of -.2/+ .2 dex change the
inherited centre score to 147.392/31.413. At +.2 dex the optimistic bin-envelope
bound is only 6.631. Thus mass normalization together with bin uncertainty
can matter strongly; this does not prove an acceptable full recalibration.
It does not reconstruct the stellar-only shift, cold gas, selection or
correlated systematics. We have not replaced the central mass scale with
the more favorable value. The tiny inherited/RAR ranking also reverses
under this sensitivity, so no ranking claim is justified.

The primary cross-ESD statistic is 4.317 under a provisional equal tangential
covariance assumption; no independent cross covariance was supplied.

## Inputs, qualification and preservation

Data: [Brouwer et al. 2021](https://arxiv.org/html/2106.11677v1), official
[KiDS release](https://kids.strw.leidenuniv.nl/sciencedata.php) and
[README](https://kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar_README.txt).
The physical ESD reduction uses H0=70 and Omega_m=.2793 distances. It is not
a demonstration that cosmological dark energy has been eliminated. Stellar
mass, cold-gas and distance assumptions remain explicit external inputs.
Using them is legitimate; reinterpreting them requires a quantitative forward
map, not discarding an inconvenient observation.

The numerical producer passed all 22 predeclared controls in .47 seconds
with about 55 MB peak RSS and exited. Independent source review checked the
flux derivative, projection, units and covariance treatment. A separate
.072-second saved-arithmetic audit verified all six frozen inputs, three
archive members and all 135 scores to scaled discrepancy 4.30e-16, without
rerunning predictions. GAMA controls and the post-screen spectral checks
also passed. The separate GAMA saved-arithmetic audit reproduced all 135
scores to 4.32e-16 in .013 seconds. All workers ran serially. No previous
result was overwritten.

Evidence hashes:

- `EFFECTIVE_ESD_FORWARD_V001_RESULT.json`:
  ec9a99b80bebf2a634ae4068407e4ee6767614c43d5376eb6e564076f5b5a433
- `EFFECTIVE_ESD_BIN_BOUND_V001_RESULT.json`:
  db518cd7d312369250ad02dde0ddecd1280c226ae4be3f4978da715ac1049cfb
- `EFFECTIVE_ESD_GAMA_CONTROL_V001_RESULT.json`:
  0fdbd4f82b1734bf06c6bb0dac6feee5eec57d8863b4f7a768eb0c8af101959b
- intact public archive: 73adc2d4e848fa0a6a43187f7b5447e749b92eaec4a795b9902b0beaf8a78733.

## A sharper type-independence prediction was also tested

After the main screen, the same public release was used to test the response's
type-independence. At exact common gbar this universal spherical law predicts
the SAME ESD for different colours and structural types, independently of
a0 and r. This is a restriction, not a new force fit. The paper's qualitative
type-dependence was already known; applying the restriction is not discovery
of that observational correlation.

Both published splits were retained: red minus blue (u-r above/below 2.5),
and higher minus lower Sersic index (above/below 2). The 30-by-30 supplied
covariance gives the difference covariance C11+C00-C10-C01. Do not drop the
cross terms or add the two overlapping split results into a joint statistic.
The release uses catalogues selected to match stellar-mass distributions,
which need not match true total baryon profiles or source-pair weights.

| Direct ESD null comparison | Colour | Sersic |
| --- | ---: | ---: |
| Q, seven primary bins | 28.0847 | 20.9390 |
| Q, all 15 bins including flagged tail | 119.9264 | 69.0701 |
| log10 of arithmetic mean high/low ESD ratio, primary | .20618 | .16165 |
| Conditional optimistic bin-weight Q lower bound, primary | 7.5613 | 4.5250 |

The full central type-blind prediction is in nominal tension, but the primary
bin-weight bounds alone do not force a strong exclusion. Differential mass
calibration, hot gas and environment also remain. The stronger all-bin
contrasts include the isolation-sensitive tail. These ESD scores are our
specified calculation from the public release; they are not asserted to
reproduce the paper's SIS/RAR statistics exactly. No sigma was manufactured.

This is a meaningful target for an environment-dependent proposal: it must
predict which independently measurable state variable produces a difference,
its sign and its magnitude, while retaining the successful average relation.
Colour is NOT a direct measure of network state, and the observed difference
is not by itself evidence for UNT. An added term fitted to these same data
would be a development calibration, not a predicted success.

Receipt `EFFECTIVE_ESD_TYPE_CONTRAST_V001_RESULT.json`, SHA256
179e4e129e8f47dfbea3c439c34a39b41bc7af862bddffcc24e25d1c91359659.
The bounded worker used .033 seconds and exited. No observations were dropped.
An independent .015-second saved-arithmetic audit verified the six archive
members, both full covariances, difference cross terms and every score/bound
to scaled discrepancy 4.44e-16. It reran no force calculation or fit.

## Next scientific decision

Do not adjust a0, r, a photon-slip coefficient or independent per-bin masses
to hide these residuals. Before an observational promotion, separate the
SPARC/GAMA stellar-calibration conventions and extended baryon/isolation
effects using independently constrained inputs and the same forward map.
If exact pair weights or catalogue-level inputs are unavailable, retain the
conditional ceiling instead of manufacturing a likelihood.

The exact next observational step is an inverse-ESD calibration diagnostic
on these seven primary bins: quantify the differential total-baryon scale
each type would require under the SAME frozen response, retaining the joint
covariance. Compare that requirement to independently constrained stellar
and gas calibrations; distinguish required offsets inferred from the target
from external evidence supporting them. Do not turn independent per-bin
offsets into an accepted predictive model or claim residuals disappeared.
Use existing direct predictions and the complete source geometry where it
matters, not another population fit or microscopic onset calculation.

In parallel the shared expansion interpretation remains the essential join.
The operational metric/clock dictionary already exists in
`OPERATIONAL_GEOMETRY_SHARED_MODEL_V001.md`; do not rederive it as progress.
`DESI_BAO_SHAPE_RESULT_V001.md` already profiles the ruler amplitude and
displays AP ratios; do not rerun that calculation. Preserve BOTH the eta=1
no-acceleration result and the stronger trace-only scalar-kinetic failure in
`SHARED_GEOMETRY_KINETIC_SCREEN_V001.md`. The K(X) independent-vacuum/charge
audit also remains. A genuinely new source/evolution or physical measurement
coupling is required to change those decisions. Borrowing one branch's
cosmology for another's galaxy law or merely relabelling time is insufficient.
Full growth, merger, early-universe, both CMB tracks and reviewed synthesis
remain outstanding. Explanatory economy remains a criterion alongside fit.
