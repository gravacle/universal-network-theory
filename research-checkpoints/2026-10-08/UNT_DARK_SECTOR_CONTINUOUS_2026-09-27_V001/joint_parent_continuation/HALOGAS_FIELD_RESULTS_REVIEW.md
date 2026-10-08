# Independent review of the complete two-source galaxy queue

Both retained-H I representations completed all four prescribed jobs. All
eight cases, 62 numerical case checks and 344 observed-radius rows are
retained and authenticated. The network candidate still gives substantially
smaller rotation-speed discrepancies than its same-source baryons-only
Newtonian controls. Substituting the modern retained gas source does **not**
remove the remaining shape mismatch or improve the aggregate residuals
relative to the fixed calibrated old-gas control.

## Complete fine-grid results

Descriptive unweighted RMS residuals, in km/s; all predictions have a real
circular speed and no observed-radius row is dropped:

| Fixed source | Equation | All 43 radii | R≥2 kpc (37) | R≥8 kpc (21) |
|---|---|---:|---:|---:|
| Modern retained H I, 40 arcsec | Network candidate | 14.41418 | 10.56440 | 13.51527 |
| Modern retained H I, 40 arcsec | Baryons-only Newtonian | 53.21379 | 56.80448 | 69.80808 |
| Modern retained H I, 120 arcsec | Network candidate | 14.36041 | 10.46421 | 13.46711 |
| Modern retained H I, 120 arcsec | Baryons-only Newtonian | 53.18081 | 56.76723 | 69.94828 |
| Calibrated old gas control | Network candidate | 13.78953 | 9.57703 | 12.16396 |
| Calibrated old gas control | Baryons-only Newtonian | 53.40666 | 57.01660 | 70.13068 |

At the last observed radius, 44.08 kpc, the observation is 149 km/s. Modern
40/120-arcsec predictions are 166.42943/165.69589 km/s, compared with
172.79223 for the old calibrated gas source. The source substitution therefore
reduces this particular outer excess by 6.36–7.10 km/s but retains a
16.70–17.43 km/s excess. Its same-source Newtonian controls predict
62.92703/62.54745 km/s there.

These are mixed, scientifically useful results rather than a source-choice
success. For example, an explicitly post-exposure regional check gives
RMS 15.14446/15.04509 km/s at 20≤R<35 kpc, worse than the old calibrated
11.59001. The two modern curves differ by at most 5.18867 km/s over the 43
radii; that representation sensitivity is not a measurement-error band.
Neither representation is selected by its residuals.

## Numerical resolution and independent control

| Source | Remote-domain maximum force change | Fine/coarse maximum force change | Newtonian/ring maximum relative discrepancy |
|---|---:|---:|---:|
| 40 arcsec | 0.00833631% | 0.70897211% | 0.14525160% |
| 120 arcsec | 0.00855761% | 0.43791863% | 0.05119676% |

Domain/refinement comparisons use all inherited R≥2-kpc rows. The ring
comparison uses all five frozen source-own reference radii and its unchanged
combined allowance. Both widths remain well inside the frozen 2% field
criteria. Reported final nonlinear residuals are at most 9.57898e−10, global
flux errors at most 7.13958e−7, with zero clipped faces. The six nonlinear
cases took 14–15 outer updates each; the two Newtonian controls took one.
Case runtimes sum to 613.9118 seconds. Maximum reported process RSS was
203,276,288 bytes; this is self-RSS, not an independently enforced job cap.

Source and ring qualifications were separately reviewed in
`HALOGAS_SOURCE_ORACLE_REVIEW.md`: 438 source checks and 170 ring checks,
68 included mass-conserving bins and ten independent ring cases. Both modern
representations have the same included mass and fixed calibrated stellar/H2
components. This experiment changes gas distribution as well as total gas
mass relative to the old source; it is not a one-parameter mass rescaling.

## Independent saved-data audit

`halogas_saved_results_audit_v002.py` imports no physical worker modules and
does not rerun a PDE, propagation or ring quadrature. It independently:

- verifies all 86 freeze members, all eight result identities, canonical
  payload hashes and the final index;
- recomputes Bernstein controls, exact bin/partial integrals and signed
  source ledgers from the extraction;
- recomputes all 170 oracle gate values, component sums, height extrapolation
  and omitted-tail bounds from saved quadrature output;
- obtains the saved midplane radial force by independent three-point
  Lagrange differentiation of the saved potential, then checks all 344
  sample rows, physical speed normalization, signed control contrasts and
  descriptive summaries;
- recomputes domain/refinement differences and all ten Newtonian/ring
  discrepancies and allowances.

The independently differentiated force differs by at most 2.28e−12 scaled
units. Row reconstructions differ by at most 4.31e−10 scaled units (including
subtractions of close quantities); summary arithmetic by 3.39e−16. Source
integrals and oracle arithmetic agree at the previously documented precision.
This audit checks the stored nonlinear-residual and flux gates against their
criteria; it does not claim an independent second PDE solve or a new direct
evaluation of the full residual operator.

V001 of this audit script is preserved. Its final ring-discrepancy arithmetic
comparison stopped on a 4.55e−13 subtraction difference from independently
reordered interpolation, while the physical forces are of order 10^3 in
those units. V002 changes only that audit agreement allowance to 2e−12.
No worker source, output, scientific tolerance or frozen protocol changed.
The complete reproducible snapshot is `HALOGAS_FIELD_RESULTS_REVIEW_DATA.json`.

## Scientific interpretation

No dark halo is present in any of these calculations. The common candidate
law plus specified baryonic source explains much more of the observed speed
amplitude than baryons-only Newtonian gravity. That is a concrete forward
result within the candidate model, not a comparison against a fitted halo,
an independent test of the law's microscopic origin, or complete agreement
with the observations. The law and some scales were previously calibrated;
this gas-source test is explicitly post-exposure and does not fit velocities.

The retained map, fixed planar geometry, interpolating source convention,
inherited 43-point tracer table and quoted errors are not a full compatible
warped/thick-gas reconstruction. The source/tracer distinction and incomplete
mask/source-association information remain part of the model identity. Nominal
quoted-error sums are descriptive, not a likelihood or a significance claim.
The remaining discrepancy has survived the numerical and fixed-source tests;
it should be addressed through an identified physical or observational input,
not by treating numerical convergence as an observational pass.

Final eight-case index SHA-256:
`24729fb613fb3da2a07c41155cabd17898954f15cca3ae21d83f5fa00f54466d`.
All individual input/output hashes and the audit script identity are retained
in the review-data JSON. No frozen evidence was edited.
