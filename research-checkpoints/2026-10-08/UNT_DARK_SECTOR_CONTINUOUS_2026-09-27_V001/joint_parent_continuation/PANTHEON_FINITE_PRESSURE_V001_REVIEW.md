# Pantheon+ finite-pressure saved-result review V001

2026-09-29. Complete saved-array/custody review accepted. No distances, cosmological quadrature, state inversion or producer were rerun. Independent covariance linear algebra was used solely to check the published residuals.

Result SHA256 `b06646ac8562257f88e423bbfa8d5842c9b93f63ed2b0bc080c39eeed5c6c815`; freeze `32c6f69d143e3c451e2b57e030a5bdf279080525617f720c38226d8e9b7b0612`; canonical payload `3a8cdc5b6c74372d9dacf393b23bbe15b9de7fb0f3d7b0cd72349b17fbfe1e0b`.

## Complete preservation and checks

The published zHD>0.01 mask selects 1,590 of 1,701 original rows. All 111 excluded rows are accounted for by that single mask; original indices, CID/survey labels and duplicates remain unchanged. Raw vector, full STAT+SYS covariance, README, SN-only likelihood and all 13 covariance transport parts authenticate. The selected covariance is the exact two-axis submatrix, not a diagonal or regularized approximation. All 335 histories and 1,340 source labels survive, with 295 finite histories and 40 dust limits.

All four packed little-endian float64 arrays authenticate and decode exactly: residual/whitened matrices of shape 1590x335 and dust matrices of shape 1590x5. The complete selected covariance was independently factored. Multiplication of its factor by every saved whitened residual reproduces every residual; all quadratic scores, common-offset stationarity/curvature, dust differences and absolute-magnitude convention pass. Reconstructed magnitude shapes are algebraic recoveries from residuals/offsets, not independent distance calculations. Numerical distance qualification remains the frozen producer's GL/Simpson/endpoint controls.

Audit: 128 unique files, 16 manifests, 658 member occurrences; 5,674,742 passing scalar/array arithmetic checks, maximum scaled discrepancy 2.183e-13. Producer: `COMPLETE_ALL_335_SN_PROFILES`, 7,811,405 numerical entries checked, no failures, 18.9171 seconds and 303,513,600 bytes self RSS. Millions of entries are not millions of scientific tests or independent observations.

Reproducer `pantheon_finite_pressure_saved_audit_v001.py` SHA256 `413487253cb3daba26114d6f335f427a4d4948fd147e35c2eedca343929a833b`; receipt `PANTHEON_FINITE_PRESSURE_V001_SAVED_AUDIT.json` SHA256 `ec7f34e5b3b00bb3097771695f2ba82b81dc07925ea666e57c2c2540006ed3d6`.

## Scientific result

The fitted-offset scores for backgrounds 0–4 are approximately 1402.939932, 1404.159218, 1403.658956, 1404.158387 and 1403.659482. There is no resolved finite-pressure improvement or worsening relative to each background's pressureless comparator:

- Across all 335 histories, the largest absolute saved score difference is 1.795e-9 and the largest residual change is 8.748e-11 magnitude.
- Across the 90 finite joint-band histories, the corresponding maxima are 8.186e-12 and 7.639e-14 magnitude.
- Both are far below the predeclared 2e-6 score-refinement tolerance. Tiny signed differences are retained, not scientifically ranked.

The one fitted magnitude offset spans 23.80232–23.81384. Its inferred absolute-M translation, about -19.28009 to -19.20367, uses each already-supplied Hcal; it is not a new determination of H0 or an absolute SN calibration.

The same role distinction as the BAO packet remains: 120 joint-role histories including 30 dust limits versus 215 single-observable central-contour histories. All joint-role rows have the inherited local BBN interpolation qualification, but many central-contour rows do not. Marginal-band endpoints do not form a joint confidence region, and numerical spectrum copies do not multiply the evidence.

## What this does and does not establish

The conditional finite-gap backgrounds preserve the low-redshift supernova distance performance of their matching dust backgrounds under one transparently counted magnitude nuisance. This is useful consistency, not discriminating superiority. The inherited Omega_m/background alternatives are Pantheon-exposed; this cannot be sold as unused validation or combined again with the Pantheon-derived parameter prior as independent evidence. No joint BBN+BAO+SN likelihood, exclusion significance or model-selection ratio is calculated.

The published survey product's calibration, bias and velocity assumptions remain imported. The correct luminosity convention is (1+zHEL)dM(zHD); a nuisance offset absorbs the global dimensional distance scale, not changes in shape. Recombination, growth, network thermal production and galaxy state selection remain distinct questions. A standard conditional ordinary-radiation comparison is not a requirement that UNT itself assumes inflation or an initial singular hot origin.
