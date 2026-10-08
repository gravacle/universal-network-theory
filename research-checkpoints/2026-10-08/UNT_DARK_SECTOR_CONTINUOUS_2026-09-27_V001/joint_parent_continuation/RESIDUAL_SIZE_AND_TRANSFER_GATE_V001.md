# Residual size and prospective external-transfer assessment

2026-09-28. Independent saved-data audit; no new field solution, fit or retuning.
The NGC 3198 numbers below are descriptive. The DDO 154 criteria are specified
before this reviewer has viewed any DDO 154 velocity samples or predictions.

## 1. What remains in NGC 3198

The fixed network-response candidate greatly reduces the baryons-only Newtonian
mismatch, but its remaining mismatch is not negligible or numerical roundoff.
Both modern retained-HI representations and every observed row are preserved.

| Fixed HI representation | All 43 rows RMS, km/s | Same-source Newtonian | R >= 2 kpc, 37 rows RMS | Same-source Newtonian |
|---|---:|---:|---:|---:|
| 40 arcsec | 14.4142 | 53.2138 | 10.5644 | 56.8045 |
| 120 arcsec | 14.3604 | 53.1808 | 10.4642 | 56.7672 |

Dividing those network RMS values by the **median observed speed in the same
row set** gives 9.873%/9.836% for all rows (median 146 km/s), and 7.187%/7.119%
outside 2 kpc (median 147 km/s). This is a descriptive speed normalization,
not a fractional uncertainty, likelihood, or statement of statistical significance.
The all-row comparison remains primary; the historical R >= 2 summary does
not remove the six inner rows or authorize that cut for another galaxy.

At the last observed radius, 44.08 kpc, the observed speed is 149 km/s:

| HI representation | Predicted speed | Signed speed residual | Squared-speed residual | Acceleration residual | Fraction of observed acceleration |
|---|---:|---:|---:|---:|---:|
| 40 arcsec | 166.4294 km/s | +17.4294 km/s | +5497.754 (km/s)^2 | +4.0420e-12 m/s^2 | +24.764% |
| 120 arcsec | 165.6959 km/s | +16.6959 km/s | +5254.127 (km/s)^2 | +3.8629e-12 m/s^2 | +23.666% |

Here Delta g = (v_pred^2-v_obs^2)/R; the last column is
(v_pred^2-v_obs^2)/v_obs^2. These are +0.033683/+0.032190 of the fixed
a0 = 1.2e-10 m/s^2. The five rows at R >= 35 kpc all have positive residuals;
their mean residuals are +19.695/+19.622 km/s. Thus the outer discrepancy has
a coherent sign, rather than merely scatter around the observed curve.

The measured maximum speed changes from the saved mesh comparison are
0.606/0.433 km/s (40/120 arcsec); the enlarged-domain comparisons change speeds
by at most 0.00694/0.00709 km/s. These are measured refinement differences,
not rigorous continuum error bars. Changing the retained source representation
from 40 to 120 arcsec changes a speed by at most 5.189 km/s, with 1.655 km/s
RMS difference. Neither numerical convergence nor that one source contrast
quantifies distance, inclination/warp, missing flux, vertical structure,
stellar calibration, tracer corrections or correlated observational error.
No complete covariance or statistical significance is asserted.

## 2. Source-led target and exposure audit

The selected target is **DDO 154**, retained whether it later agrees or
disagrees. Independent inspection of the resident Leroy table4 source columns
and table7 confirms D = 4.3 Mpc, i = 66 deg, PA = 230 deg, stellar scale
0.8 kpc, rounded log masses 7.1/8.7, and atomic-to-stellar mass ratio about
39.8. This makes stellar normalization less dominant. The source tables are
not themselves a complete outer-disk model: the seven density rings end at
1.4 kpc; table7 HI includes helium, and missing H2 entries are not measured zero.
The reported H2 upper limit is an aperture constraint, not a radial allocation.

The selection author disclosed accidental exposure to published kinematic
narrative and a smooth-fit velocity parameter, but no sampled rotation table,
UNT prediction or residual. This is an **out-of-program prospective transfer**,
not a blind test. This reviewer checked source columns without reading those
fit columns. The original natural and robust HI moment-zero maps are the
next source qualification; the seven inner rings alone do not qualify an
outer-galaxy force test. Detailed header/pixel/geometry audits are additive
and do not change the selected target.

## 3. Fixed next-test criteria

1. **Freeze source conventions before kinematic scoring.** Retain both
   natural/robust maps as declared source contrasts, with original beam,
   flux-to-column units, blank/zero/signed-pixel meaning, center/WCS, footprint,
   flux loss, outer support, helium once, thickness and stellar/H2 conventions.
   Use D = 4.3 Mpc, i = 66 deg, PA = 230 deg and the existing photometric rule;
   document any mismatch with the future velocity-table conventions explicitly.
   Do not choose a source, bin width, tail, distance or inclination from its
   agreement with the rotation curve.
2. **Transfer the complete existing law without a galaxy fit.** Keep
   a0 = 1.2e-10 m/s^2 and r = 25.51664211557329 and its field equation fixed.
   No DDO 154 law scale, shape, M/L, geometry or halo parameter is optimized.
   Solve the identical baryonic density under Newtonian gravity as the control.
3. **Retain every valid published velocity row.** Freeze the original source's
   validity/quality rules and conversion conventions before scoring. Record
   all exclusions with source reasons, not residual size. Do not import the
   NGC 3198 2-kpc cut. Any interior/outer descriptive split is supplemental.
4. **Keep numerical and empirical decisions separate.** Inherited flux,
   source-mass, mesh/domain and independent Newtonian-oracle checks qualify the
   solver; source-specific numerical details are fixed before execution.
   Report all-row RMS, median-speed-normalized RMS, signed residual curve,
   outer residual and squared-speed/acceleration mismatch for each fixed
   source contrast and its same-source Newtonian control.
5. **Use uncertainties coherently, not as adjustable room.** Propagate
   independently owned source/geometry uncertainties as full curves; do not
   choose a different nuisance realization at each radius. Use an actual
   covariance/distribution if supplied and justified. Otherwise publish
   sensitivity contrasts and quoted errors as such, without inventing a
   likelihood or treating radial points as independent. A missing covariance
   does not prevent the calculation or descriptive comparison.

The outcome labels are deliberately distinct:

- **Numerically qualified:** the fixed solver/source checks pass.
- **Improvement over baryons-only Newtonian:** all-valid-row RMS is smaller
  under the fixed candidate than under the same-source Newtonian control.
  Report this separately for both source maps; success on one map does not
  erase the other. This is not a comparison with a fitted dark-matter halo.
- **Quantitative transfer:** the unfitted curve, including its radial shape,
  is compatible with an independently justified joint observational/source
  uncertainty account. State the actual statistical decision rule before
  scoring if such a probability model is available. In its absence the result
  can be strong descriptive agreement, but not a formal statistical acceptance.
- **Unresolved transfer:** a coherent discrepancy survives the declared source
  contrasts or the uncertainties cannot determine compatibility. Preserve it;
  do not relabel mere improvement as complete explanation or silently tune
  this target. Any subsequent explanatory change is a new, exposed test.

Passing this test would demonstrate portability of the adopted response law
to a different, gas-dominated system without a local dark halo or acceleration
fit. It would not by itself derive that law from native UNT records, establish
its cosmological completion, or show that no competing halo model works.

## 4. Reproduction and custody

`residual_size_audit.py` rechecks all eight immutable case digests, canonical
payload hashes, freeze references and saved numerical checks, then recomputes
the residuals above directly from their rows. It performs no fit or field solve.

- Audit source SHA-256:
  `582b908ca4f43947c492f7fef4a4a96ef6307994efceb614a72359c354e6fe8c`.
- Saved arithmetic `RESIDUAL_SIZE_AUDIT.json` SHA-256:
  `115e65ba43c9b5022fdc1b5171dac95829ac8200d39be28194e478b8522a521d`.
- Existing eight-case receipt `HALOGAS_FIELD_RESULTS.json` SHA-256:
  `24729fb613fb3da2a07c41155cabd17898954f15cca3ae21d83f5fa00f54466d`.
- Reviewed selection `EXTERNAL_GALAXY_SELECTION_V001.md` SHA-256:
  `db1c2053b64d52dff8418364637d52ac395c6757658e629872aa98816e4291b8`.

The three resident Leroy source hashes match that selection record exactly.
Detailed prior numerical/source qualification is preserved in
`HALOGAS_FIELD_RESULTS_REVIEW.md` and `HALOGAS_SOURCE_ORACLE_REVIEW.md`.
