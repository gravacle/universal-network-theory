# Saved-array audit: radial transfer V001

Independent saved-data audit only; no producer, force law, halo fit, or calibration was rerun. The supplementary robustness summaries below are **posthoc descriptions**, not new acceptance gates or a replacement primary score.

## Custody and numerical accounting

All **13,685 audit checks pass**. The result hash is `77883bc7e0da4ceaf1d623ba835be6dc3c0666dd0b56d0b00aa36e551247f7c0`; the freeze hash is `1c6a13d71acd9b12ae6549a04a29520e57a4e2a93eb5e98a9825f9d2b8ed5219`. Every frozen source/protocol/helper/input hash, all 100 case hashes, saved source rows, radius sorting, inner-input digest, masks, pivots, outcome records, and aggregate copies match. All 92 synthetic and 4,606 eligible-galaxy control flags agree with their stored numerical errors and gates.

The census contains 100 evaluation galaxies: **94 eligible, 981 outer rows**, no tied split radii. The six retained exclusions are D512-2 (4 rows), NGC6789 (4), UGC00634 (4), UGC00891 (5), UGC07232 (4), and UGC09992 (5). All eligible outcomes are qualified. Independent reconstruction from saved velocities verifies residuals, quoted-error residuals, both inner/outer MSEs, selected inner objectives, paired differences, and all aggregates. This audits saved arithmetic and controls, not a proof of global optimization or independent observational validation.

## Frozen primary result and paired distribution

The primary score remains galaxy-balanced **outer velocity MSE**, in `(km/s)^2`. Halo figures below use the 513-point refinement; both resolutions and full per-galaxy paired arrays are retained in the audit JSON.

| Comparator | Outer velocity MSE | Network wins / ties / losses | Median network-minus-comparator MSE |
|---|---:|---:|---:|
| Network effective law | 285.872069 | — | — |
| RAR | 285.221205 | 50 / 0 / 44 | −1.696951 |
| Baryons only | 3873.052006 | 89 / 0 / 5 | −2078.917199 |
| Inner-fitted NFW | 988.661224 | 48 / 0 / 46 | −7.062987 |
| Inner-fitted ISO | 1702.299750 | 41 / 0 / 53 | +14.994153 |

Diagnostic ties use `abs(difference) <= 1e-10 max(1, MSE_network, MSE_comparator)`. Individual median MSEs are network 85.8170, RAR 89.0642, NFW 94.2291, and ISO 57.9838. Thus the large mean halo advantage is **not** a broad per-galaxy dominance; ISO wins on more galaxies and has the lower median individual MSE. Secondary log-acceleration MSEs are network 0.018976935, RAR 0.019186003, NFW 0.029596299, ISO 0.023431203, baryons 0.357137153; the secondary metric does not replace the primary ranking.

## Concentration in extrapolation failures

Largest five contributions to the total network-minus-halo MSE sum:

| Rank | NFW galaxy / difference | ISO galaxy / difference |
|---|---|---|
| 1 | UGC09133 / −31870.0980 | UGC06787 / −79963.4995 |
| 2 | UGC02953 / −11506.8185 | NGC5055 / −30106.1608 |
| 3 | UGC05253 / −4572.2317 | UGC09133 / −9312.1839 |
| 4 | F571-8 / −4483.4854 | UGC02953 / −4592.2611 |
| 5 | ESO563-G021 / −4035.6243 | UGC03546 / −3942.2760 |

These five account for **85.48% of the net NFW gain and 96.07% of the net ISO gain**. Removing the largest gain leaves paired mean differences −367.6568 (NFW) and −571.8355 (ISO); removing the largest five leaves −107.7969 and −58.7396. The corresponding five-removed paired medians are +0.5807 and +21.4360. These exclusions are descriptive sensitivity checks only; none changes the complete-census primary result. In these two comparisons the five largest absolute contributions are the same five gains; the JSON also retains largest losses and both deletion definitions.

Boundary counts reproduce exactly. NFW selects the infinite-scale limit in 50 cases, zero amplitude/undefined scale in 4, and strict sampled local minima in 40. ISO selects infinite-scale limits in 4, finite upper boundaries in 5, zero-scale limits in 4, zero amplitude in 3, lowest sampled grid points in 5, and strict minima in 73. All five ISO lowest-grid cases have logscale 16.5625–17.265625, vastly outside observed radii: they are numerically large-core-limit-like, not physically identified finite cores. In particular, the largest ISO outlier UGC06787 has scale about 44 million kpc. The literal-label boundary/interior strata in the JSON retain the producer labels; this caveat is essential when reading its nominal “interior” bucket.

Large gains therefore reflect severe extrapolation failures, often in asymptotic/poorly scale-constrained inner fits, but are not exclusively boundary effects: NFW's strict-minimum subset still has paired mean −401.7743, and ISO's strict-minimum subset −64.8816, with medians +1.6017 and +28.2317 respectively. A physically motivated external halo population prior is a different legitimate predictive baseline, not tested here.

## Network versus RAR leverage

The network primary mean is **0.650864 higher** than RAR, despite its slight median paired advantage. Among 981 outer rows, `v_network/v_RAR − 1` has median absolute magnitude **0.73663%**, maximum absolute magnitude **3.68666%**, signed median −0.67488%, signed row-weighted mean −0.15588%, and signed galaxy-balanced mean −0.39000%. These compare the separately frozen calibrated acceleration scales, not exactly equal `a0`. This experiment provides limited leverage to distinguish the two effective laws and does not establish network superiority over RAR.

The result supports a descriptive radial-transfer advantage over these unconstrained two-parameter inner-fitted halo families, with important tail sensitivity. It is exposed development evidence, not blind testing, a global ΛCDM comparison, a native network derivation, or a demonstration of a shared galaxy/cosmology mechanism.

## Artifacts

Audit JSON: `GALAXY_RADIAL_TRANSFER_V001_AUDIT.json`, SHA256 `ef931519dc1fee9b94714cb0da936543e96d854a1e8f977e0d69f67087c591d0`.

Audit source: `GALAXY_RADIAL_TRANSFER_V001_AUDIT.py`, SHA256 `48c0583f160c99434564739d44839cda0bfdc7405ebd709f598b63d6a3e3e073`.

Runtime: 0.239 seconds. The sole numerical slot was explicitly released after the saved-array audit; no producer files or receipts were modified.
