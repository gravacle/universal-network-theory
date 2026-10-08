# Complete finite-pressure BAO/ruler saved-result review V001

2026-09-29. All five background files pass independent custody and saved-array arithmetic. No producer, distance/action/acoustic quadrature, endpoint inversion or optimizer was rerun.

## Custody and census

Freeze SHA256: `f5302c8a70befba825b6c1252c75aac17efafc9280770bcc53b46fc0ae38c388`.
The exact result files `FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_0..4.json` have hashes, in order:

```
31cd0c151a6f6f906fa62ef84f3c3517b5ecbcd79f39beda29ecea2fddc9fdf2
38e4ff97e7158e31b6ae1482f5f4ce7971d256d9b67f4c96beb7b4fc59eb3479
8ac1241d4c378ab7ec6ced9447262cfb5df1772d23ab7a36349ed257437df772
b6c5d0e95efae74f19a09c93c0b2637324fd7535b636cccb5df0a35203802503
3bf9a0d352a64d0570177fdaf628d3c336ed6bb365415abffb69115ae6cd305f
```

Each is `COMPLETE_BACKGROUND_SUBSET`, 67 rows and no failed controls. Together they retain exactly 335 distinct histories: 295 finite states and 40 positive-energy dust limits. All 1,340 inherited source labels, five backgrounds, 18 reference labels, 67 point roles, four scale-canceling copies and all 13 covariance-ordered observations are retained. The copies are not independent physical histories. LyA order remains DH then DM.

The audit authenticates 110 unique files, 15 recursive manifests and 532 member occurrences, all wrapper payloads and frozen links. Independent arithmetic has 60,300 passing checks, maximum scaled discrepancy 2.899e-13. Producer totals are 40,455 numerical checks, 87.9755 seconds summed across five sequential runs, and maximum 67,272,704 bytes self RSS, not whole-machine memory. Counts include repeated array/control entries, not that many physical tests.

Reproducer `finite_pressure_bao_saved_audit_v001.py` SHA256 `b7115a51c588697628c2a85e5bafd9ed0a4b371e0ed2d08c48b55d12bd35c2a7`; full receipt `FINITE_PRESSURE_BAO_RULER_V001_SAVED_AUDIT.json` SHA256 `5184b86adc0581921bea650f2eb45b3c6f2433e82f57e2d3c406eb40f6a9bd31`.

## Independently checked arithmetic

Raw data/covariance equality, covariance factorization, all predictions/residuals/whitened residuals and signed covariance contributions, analytic nonnegative ruler amplitude, its curvature/derivative and every score were reconstructed. All state/copy associations, normalized action cancellation, present material anchors, energy and H identities, ordinary-radiation normalization, horizon-tail bounds, required-ruler units, dust controls and complete role groups were checked. The audit does not independently reproduce the saved distance/horizon integrals or transition/endpoint roots; those remain supported by the frozen producer's independent quadrature/refinement controls.

## What the complete results say

At these late BAO redshifts, the finite-pressure shapes are effectively the same as each background's pressureless control. Across all histories the largest relative shape difference is 2.012e-10 and the largest score difference is 1.230e-7. Across the 90 finite joint-band histories these shrink to 1.252e-13 and 7.743e-11. Such small differences are not a resolved preference: they lie below the frozen score qualification tolerance, and near-roundoff dust signs must not be interpreted as improvement or worsening.

The profiled covariance scores are approximately 26.2413, 43.5943, 14.7216, 43.5773 and 14.7142 for backgrounds 0–4. The one fitted ruler spans 130.628–138.077 Mpc. These values benchmark fixed backgrounds after fitting one amplitude; they do not determine an actual acoustic drag epoch or supply a new explanatory advantage over the same dust background.

The genuine state-dependent diagnostic is earlier pressure/propagation, not a measurable change to this low-redshift shape. The 18 finite joint-band points across five backgrounds give:

| Quantity at A=1101 or required endpoint | All 90 finite joint-band histories |
|---|---:|
| w | 4.9613e-8 to 1.14878e-5 |
| cI2 | 9.9226e-8 to 2.29749e-5 |
| Energy / corresponding dust energy | 1.0000000496 to 1.0000114882 |
| Truncated hard propagation horizon | 3.8692 to 19.8259 Mpc |
| Truncated photon acoustic horizon | 131.0926 to 138.5663 Mpc |
| Required A lower endpoints | 1083.4743 to 1131.6491 |
| Required A upper endpoints | 1084.6530 to 1134.3491 |
| Conservatively uncomputed tail width | 0.09237 to 0.20643 Mpc |

The hard propagation horizon is not the photon ruler. Nor does small background pressure prove small structure-growth effects; the relevant perturbation/wavenumber domain still needs its own calculation. The intervals above are tail bounds, not observational uncertainty or likelihood intervals.

There are 120 joint-role histories including 30 dust limits; all carry the inherited local BBN interpolation qualification. The remaining 215 histories are one-observable central-contour points, not joint-band solutions; 170 of those lack that local qualification. Across the full exploratory set, w at A=1101 reaches 0.01808 and the hard horizon reaches 99.85 Mpc. Those extrema must not be attributed to joint-band states. The receipt preserves separate 1-, 2-, 3-band role summaries, including their limit cases; these marginal-band constructions are not a joint-confidence analysis.

## Interpretation boundary

The same-state scalar background and one exposed DESI ruler nuisance are used transparently. BBN-derived state parameters, inherited expansion backgrounds and the reused DESI data are not held-out predictions or independent calibration evidence. There is no new free ruler per redshift, no distance rescaling hidden in the four numerical copies, and no new fit of their scalar equation of state.

The imported ordinary photon/neutrino thermal history through A=10^7 is a conditional comparison interface, not a premise that UNT began at a=0 or underwent inflation. The positive early tail is bounded rather than silently extrapolated. `actual_recombination_status=NOT_COMPUTED` remains essential: a required endpoint near 1100 is not a prediction of recombination/drag, a CMB fit or an observational acceptance result. This packet does establish a reproducible next target for an actual same-state recombination/perturbation calculation, without resolving network photon production or the galaxy-state boundary problem.
