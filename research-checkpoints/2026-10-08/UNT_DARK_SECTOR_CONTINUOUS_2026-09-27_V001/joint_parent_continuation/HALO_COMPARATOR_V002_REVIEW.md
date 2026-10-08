# Independent same-source halo-comparator result review

2026-09-29. **Numerical/custody review accepted. Scientific result: both fitted halo families outperform the current fixed network candidate in every predeclared fitted-domain objective.** This unfavorable comparison for the present network law is retained, not relabelled a success or dismissed because halos have fitted parameters.

The complete source/protocol preflight is in `HALO_COMPARATOR_V002_PREFLIGHT.md`. This result review authenticated saved products and independently evaluated their saved parameters; it did not rerun a fit, propagate a field or alter a source, law or tolerance.

## Complete census and independent arithmetic

All 147 frozen inputs match. All nine source outputs are COMPLETE, each containing the eight prescribed family/domain/weighting combinations: **72 fits, 369 saved checks, zero failures**, following 42 passed synthetic controls. Each fit keeps every original row and its full predicted curve: 43 NGC3198 rows or 12 DDO154 rows, including rows outside an R≥2 fit. All-radius pivots are unchanged across fitting domains. The original paired Newtonian fields and observations match exactly, including the fixed DDO154 radius conversion and unchanged velocities/errors.

The independent audit script imports no fitting or physical-worker module. It reconstructs NFW/ISO shapes using separately summed small-x series and direct elementary kernels, evaluates every retained coarse/fine candidate at its stored parameters, checks amplitude derivatives, reconstructs every selected full curve and signed residual, and recomputes every stored domain summary and A=0 control. All 17,728 arithmetic comparisons pass. The maximum scaled candidate-objective discrepancy is `2.915163221806089e-14`; selected full-speed discrepancy is `8.457738541441168e-15`. Maximum absolute recomputed amplitude-gradient magnitude is `6.027702208893926e-13`.

All 72 selected solutions are finite sampled-local-minimum refinements with positive amplitude. None selects a finite search boundary, zero-amplitude solution or exact zero/infinite-size limiting profile. Those candidates remain in the output. The largest scaled 257/513-grid minimum disagreement is `4.093530727211654e-15`. This supports the frozen practical search criterion, not a mathematical guarantee against every unsampled minimum. The independent audit evaluates stored candidates; it does not regenerate optimization-grid digests or claim a second optimizer.

The nine accepted fit runs report 100.739033248 seconds in total and a maximum per-process **self** RSS of 121,995,264 bytes. These figures exclude the first truncated-output attempt, synthetic tests and review, and are not aggregate job memory or a guaranteed future runtime.

## Results in the predeclared domains

RMS velocity residuals in km/s below are from the **equal-weight fit in the displayed domain**. The network law is unchanged and not refitted. R≥2 uses 37 NGC3198 rows or nine DDO154 rows. The all-row and R≥2 columns correspond to different halo fits, not a post-fit cut chosen for each source.

| Fixed source | Network all | NFW all | ISO all | Network R≥2 | NFW R≥2 | ISO R≥2 |
|---|---:|---:|---:|---:|---:|---:|
| NGC3198 original HI1/H21 | 13.1737 | 10.6976 | 7.7308 | 11.1438 | 4.1695 | 3.1482 |
| NGC3198 original HI0/H21 | 13.2288 | 10.6992 | 7.7344 | 11.2195 | 4.1699 | 3.1552 |
| NGC3198 original HI1/H20 | 13.0988 | 10.7020 | 7.7346 | 11.0378 | 4.1987 | 3.1907 |
| NGC3198 original HI0/H20 | 13.1534 | 10.7037 | 7.7383 | 11.1130 | 4.1993 | 3.1978 |
| NGC3198 ML36 / old HI | 13.7895 | 11.6600 | 9.0566 | 9.5770 | 4.0141 | 2.5791 |
| NGC3198 HALOGAS40 | 14.4142 | 11.7582 | 9.1602 | 10.5644 | 4.2365 | 2.8624 |
| NGC3198 HALOGAS120 | 14.3604 | 11.7703 | 9.1610 | 10.4642 | 4.3415 | 2.9286 |
| DDO154 natural map | 4.7793 | 2.2141 | 1.2729 | 5.4668 | 1.4395 | 1.2906 |
| DDO154 robust map | 4.6921 | 2.2074 | 1.2614 | 5.3675 | 1.4287 | 1.2783 |

The weighted result is not omitted. For **each** source, **each** fitting domain and **each** halo family, the quoted-error-weighted fit also has lower quoted-error SSE than the fixed network curve. Representative descriptive R≥2 squared-residual sums in quoted-error units are:

| Source | Fixed network | Fitted NFW | Fitted ISO |
|---|---:|---:|---:|
| Original HI1/H21 | 994.4116 | 47.9852 | 50.0916 |
| ML36 / old HI | 647.4870 | 46.5828 | 34.7115 |
| HALOGAS40 | 881.4244 | 59.9125 | 47.5316 |
| HALOGAS120 | 883.6995 | 65.8796 | 51.9729 |
| DDO154 natural | 802.3725 | 67.7599 | 43.4573 |
| DDO154 robust | 784.3214 | 67.2723 | 43.1004 |

All 72 outcomes, parameters, full-curve residuals and the remaining weighted scores are retained in the nine source files and `HALO_COMPARATOR_V002_REVIEW_DATA.json`. ISO beats NFW in every equal-weight family comparison, but NFW beats ISO for quoted-error R≥2 fits in the four original stellar-convention source variants. Neither a universally preferred halo family nor improved residuals at every individual radius is claimed. In particular, R≥2 optimization does not certify the omitted central rows; their full-curve errors remain present.

## What this does and does not settle

This closes the previously missing **same-baryon fitted-halo comparison** for the saved two-galaxy calculations. The result is not merely an unmatched comparison against baryons alone: halos were superposed on each source's own Newtonian baryonic force at exactly the same observed radii, without changing M/L, gas density, distance, inclination or errors. The network's substantial improvement over baryon-only Newtonian gravity remains true, but that improvement is not sufficient to match these fitted-halo alternatives.

The halo amplitudes and scales are fitted separately in each galaxy/source scenario; the network uses its previously calibrated common law without local fitting. Those differing freedoms are stated explicitly. They do not erase the observed fit-quality deficit, nor do these descriptive data supply a justified Bayesian evidence ratio or information-criterion preference. There is no full observational/source covariance, nuisance marginalization or unused prediction in this comparator. Nine source scenarios represent two galaxies, not nine independent tests. A free NFW rotation profile without a concentration–mass prior is not the whole cosmological dark-matter model.

The constructive implication is precise: the current fixed network response needs a physically owned correction or source/clock/state explanation of its residual shape before claiming explanatory parity here. Any subsequent adjustment based on these exposed residuals is development/calibration and must later face unused tests. This result does not refute every possible network universe, establish a native gravitational dictionary, or complete the joint galaxy/expansion program.

## Preserved technical failures

V001 stopped during input-freeze preparation because it expected COMPLETE where the DDO154 receipt legitimately says COMPLETE_DESCRIPTIVE_COMPARISON. Its source and error survive in the V002 ancestry. The exact-schema repair changes no science.

The first V002 source-00 execution completed but the caller truncated its stdout; that capture cannot authenticate a result. The original received text survives as `HALO_COMPARATOR_V002_SOURCE_00_CAPTURE_TRUNCATED.txt`, SHA-256 `ee32e5e90d078edf23e7916a4bd9c40853895aa189b214987bae53d090dbcae5`. The unchanged frozen worker was rerun with a larger capture allowance, as recorded in `HALO_COMPARATOR_V002_CAPTURE_RETRY.md`. The full accepted source-00 product is independently authenticated below. No tolerance or fitted model changed to turn either technical failure into success.

## Result identities

The common freeze is `12e1f8e99f8d64e67fcdc639c475402c8f4fcf28cadc0bf088621deb333e1727`; synthetic-controls result is `bd9bfedbb6a84387a6f1be9f2a8b77c17b41446cbb5e9b754576dce50b9da438`. Every output's canonical payload and both links were verified.

| `HALO_COMPARATOR_V002_SOURCE_XX.json` | SHA-256 |
|---|---|
| 00 | `e1aef536c0d96e078e10cd5a02b0368ef69fdd18722f164e0e67442acb2c4412` |
| 01 | `ef6a732589c532c814a83d64641f8ec12a45d2a0d0fb5cce5b95a64218ea4ed3` |
| 02 | `f309a43427f9e775ee9fcf4d8405058fc598edcbfbc7a4258a15b3a5fad66bf6` |
| 03 | `19fb3548c583289ae5f36841010dcd02ba9195a205cbc3e5ec7473b55965aa3e` |
| 04 | `887a8892d4e8db59080751c063d393eb344cb2e9c1729062632afca15bbf4fba` |
| 05 | `52981d8159b984484c56174b236cae9d25ee8ae7a2fa93781f941d3c4aa36ec6` |
| 06 | `cb053dfd66ef47d7413b663a4a89a22f93be1cf94e2d4f247a0bbd902d61bc49` |
| 07 | `6280a0a493db2fc6629c097556e6a3420940aa103c107f805a02c63ffa273f10` |
| 08 | `51e9ed99b6cd31cc230a1a245b16269ce865c76a1f5443ce30d182cfe78c8f97` |

Independent audit source `halo_comparator_saved_audit_v002.py`: `653c200c8d34b3f63cb64c995a9c5ba88606dd1d507c8836b1edc15728b5dbee`.

Audit output `HALO_COMPARATOR_V002_REVIEW_DATA.json`: `bc3a6c55fb8e4c306217d493bdc0a211c50cc7162ccc62d9d92b2ea062a584aa`.

This reviewer drafted the prospective source-census proposal but did not implement or run the fitter. The independent arithmetic and custody checks above should not be mistaken for an independently repeated optimization.
