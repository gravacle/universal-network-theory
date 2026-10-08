# Independent review: DESI DR2 saved expansion-shape results

2026-09-29. **Numerical/custody review accepted.** All 18 predeclared reference
alternatives and the complete 13-entry observation/covariance vector are
retained. The references give three distinct expansion shapes. Their scores
are not identical, and the extra fitted-shape comparator improves on each:

| Fixed reference Omega_m | Reference rows | Profiled acoustic A | Covariance chi-square | Difference from free-shape comparator |
|---|---|---:|---:|---:|
| 0.334 | 0, 1 | 30.33657580 | 26.02953706 | 15.75849606 |
| 0.352 | 2, 3, 6, 7, 10, 11, 14, 15 | 30.71887334 | 43.30217676 | 33.03113575 |
| 0.316 | 4, 5, 8, 9, 12, 13, 16, 17 | 29.94295951 | 14.59405159 | 4.32301059 |

The comparator's selected interior minimum is
`Omega_m = 0.2974618208407951`, `A = 29.524633443747238`,
`chi-square = 10.271041002564886`, with
`H0 rd = 10153.977307497797 km/s`. The two predeclared profile grids find
the same minimum to `1.60e-14` in score and `1.71e-8` in A. Both finite
endpoints, the best grid points and each sampled local-minimum bracket remain
in the original output. No observational success threshold was imposed.

## Independent audit and identities

The reviewer ran only `desi_bao_saved_audit_v001.py`: a standard-library,
read-only reconstruction using saved shapes/predictions and the original
covariance. It imports no scientific producer, integrates no distances,
performs no optimizer search and solves no eigenproblem. The audit verifies
all 20 frozen members, the complete original observation ordering, and the
canonical result payload.

| Artifact | SHA-256 |
|---|---|
| Original freeze | `8847e8267450d694cb59b25790767a88a187888d13e0dcc7076ccab7e399b461` |
| Original result file | `1b7f1b02b2988e0109c1afd01f4ca621e36f1cd5729261ebff676853596f3fe7` |
| Original result payload | `4921a95442fbe24c74e6bf0c7b4fa28ae99df3ab1b07b1635508e519411ae6b3` |
| Independent audit script | `44632666e23c91732a6668673c47c520b51e5a07d2e574ef9a6fe5ac6389b035` |
| Independent audit payload | `ec8814d8a89bae2f9bcdb95c356da24c95a48182f5eef88cdd3538249b0e9f39` |

The reproducible additive receipt is `DESI_BAO_SAVED_AUDIT_V001.json`.
The original source/protocol hashes are bound in
`DESI_BAO_SHAPE_PREFLIGHT_V001.md` and the unchanged original freeze.

The audit contains 6,747 arithmetic comparisons, in addition to the original
producer's 1,160 passing numerical controls. These are implementation checks,
not thousands of observational confirmations. Independent partial-pivot
Gaussian elimination reconstructs the fitted A, full-covariance score and
residual contributions; a separate scalar Cholesky construction checks the
stored whitened residuals. All 54 retained fit records, including Simpson
comparison fits and synthetic controls, pass. Largest score recombination
difference is `3.64e-12`, including the large endpoint scores.

All six AP pairs are checked for every reference and the selected comparator:
observed/model ratios, covariance submatrices, correlation and delta-method
error. The Ly-alpha primary vector retains DH before DM; the display alone
uses DM/DH. All 108 radiation sensitivity identities and interval bounds pass.
Their largest named distance change is `0.0003962458474` (0.0396246%); largest
H change is `0.0003964029204`. The altered present H ratio is
`1.0000221395` to `1.0000398288`, consistent with preserving the original
physical dust and vacuum coefficients rather than silently renormalizing them.

For scope: comparator-candidate shapes are recovered from saved prediction/A
before recombining their fits; this does not independently calculate their
distance integrals. Full-grid scores, Gauss/Simpson convergence and radiation
DM/DV integrals remain the frozen producer's evidence. No fresh quadrature or
search is disguised as a saved-data audit. The original run took 0.171185 s
and reported 37,208,064 bytes peak **self** RSS, not whole-job memory.

## Scientific interpretation

This is a useful outside-calibration expansion-shape test of the conditional
balanced hard-mode limit. It shows directly how the inherited reference
choices compare with all the specified BAO distances; the lower-matter
reference is closer to the freely fitted shape than the central/higher-matter
references. Every alternative remains visible; choosing the best after seeing
these scores would be additional calibration, not an unused prediction.

The candidate fits **one** common acoustic-scale nuisance. The comparator
fits that amplitude **and** Omega_m. Its lower in-sample score therefore does
not by itself rank explanatory or predictive superiority. At equal Omega_m
and A the adopted candidate and ordinary flat dust-plus-vacuum expansion
shapes are mathematically identical: these distances test the common shape,
not the microscopic identity of its pressureless or vacuum-like contributions.
Legitimate future shared calibration is possible, but its fitted freedom and
new-data status must be counted transparently.

The 18 alternatives are not a joint propagation of their original H0/BBN/
vacuum-reference uncertainties, nor 18 independent tests. Data exposure and
survey/template assumptions remain as disclosed in the prospective protocol.
No p-value, model-selection evidence ratio, derived acoustic length, complete
CMB fit, or proof of the finite-gap/clock/native-gravity connection follows.
The radiation rows are a separately unscored omission diagnostic, not a
network-origin photon result. No frozen file or numerical criterion changed
during this review.
