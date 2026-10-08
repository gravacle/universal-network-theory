# Same-source fitted-halo comparator: prospective V001

2026-09-29. Design fixed before executing this comparator. No halo fit, new field solve or observation download was performed for this note. The existing galaxy curves and their residuals are already exposed; this is not a blind or held-out test. A targeted search of current continuation reports/scripts found no completed fitted-halo comparator. The existing distance-only diagnostic is not one.

## Scientific question and complete census

Using exactly the baryonic source, distance, geometry and observed velocity rows of each saved calculation, how closely can a two-parameter spherical dark halo plus Newtonian baryons reproduce the curve, compared with the unchanged conditional network prediction?

Retain **all nine source variants**, not only the most favorable one:

| Galaxy | Saved source/model stem | Role |
|---|---|---|
| NGC3198 | `galaxy_HI1_H21` | Original stellar convention, HI and H2 exponential continuations |
| NGC3198 | `galaxy_HI0_H21` | HI truncation contrast |
| NGC3198 | `galaxy_HI1_H20` | H2 truncation contrast |
| NGC3198 | `galaxy_HI0_H20` | Both gas truncation contrasts |
| NGC3198 | `ML36_CAL_HI1_H21_V001` | Fixed stellar-conversion substitution, old HI |
| NGC3198 | `HALOGAS40_ML36_RETAINED_V001` | Retained modern HI, 40-arcsec extraction |
| NGC3198 | `HALOGAS120_ML36_RETAINED_V001` | Retained modern HI, 120-arcsec extraction |
| DDO154 | `DDO154_THINGS_NA40_ML36_H2OMIT_V001` | Natural-weighted THINGS HI |
| DDO154 | `DDO154_THINGS_RO40_ML36_H2OMIT_V001` | Robust-weighted THINGS HI |

These are source sensitivities in **two galaxies**, not nine independent observational tests. They are not confidence bounds on all possible baryonic sources. The DDO154 molecular-gas omission and catalogue/profile discrepancies, and both galaxies' fixed-plane/photometric/geometry assumptions remain attached to both comparators.

## Exact extraction and custody

All paths below are relative to this directory except the explicit `../` source. Authenticate canonical payloads, freeze links, existing complete receipts and their actual input/case hashes before using arrays. The original four NGC3198 pairs have individually sealed case products rather than an assumed nonexistent `GALAXY_FIELD_RESULTS.json`; use their real freeze and prior review/qualification evidence.

For each NGC3198 stem read its `_N512_L255_Newton0.json` and `_N512_L255_Newton1.json`. Require identical ordered `(R,velocity,error)` rows and component masses. Use the latter's saved `comparison[].prediction²` as baryonic `b_i²`, and the former's prediction unchanged as the network curve. Do not use SPARC component-force columns, algebraic MOND substitutions or fitted distances. Each pair has all 43 rows, radii 0.32–44.08 kpc, 37 rows at R≥2 kpc and 21 at R≥8 kpc.

NGC3198 observed source: `../ngc3198_sparc_excerpt_v001.txt`, SHA-256 `58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900`. Its fixed distance remains 13.8 Mpc. The 43-row/all-source census and exact row matching were checked in preparing this design.

For DDO154 use `external_ddo154_v001/ROTATION_COMPARISON.json`, `payload.models.{NA,RO}.comparison`. Read `R_kpc`, unchanged `observed_velocity_kms`, `quoted_error_kms`, the saved `newtonian.velocity_squared_kms2`, and the unchanged `candidate.prediction_kms`. Require both complete 12-row censuses, all numerical checks, and matching raw observation rows. All 12 radii, 0.5215346534653466–6.300990099009901 kpc, were numerically qualified; nine satisfy R≥2 kpc. The fixed radius mapping remains `R_published*4.3/4.04`; published velocities/errors are not inclination-rescaled. Primary source `external_ddo154_v001/SPARC_MassModels_Lelli2016c.mrt` has SHA-256 `9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c`.

Authoritative receipt/freeze identities:

| Artifact | SHA-256 |
|---|---|
| `GALAXY_FIELD_FROZEN.json` | `dcb22692af4397c08c8dfb15dc17cddebc1a3e377a02f8b48695197e075c2ef9` |
| `STELLAR_CALIBRATION_FROZEN.json` | `622f381e523b43ea4910fda55ff1130ef17e8ad143cffa29b0a72165498ac656` |
| `STELLAR_CALIBRATION_RESULTS.json` | `21db2263f7a49a11312d4e2c8abfb5412946784fbcebfa8e5db2b1447668f14a` |
| `HALOGAS_FIELD_FROZEN.json` | `81d01ef269d70f2699424b6576553c69944d92f51c169831c6d7a249584d694a` |
| `HALOGAS_FIELD_RESULTS.json` | `24729fb613fb3da2a07c41155cabd17898954f15cca3ae21d83f5fa00f54466d` |
| `external_ddo154_v001/FIELD_V002_FROZEN.json` | `c8dad033005354446b5b25744fcc774331a5ed9e3c3eec00127939cc6c20f605` |
| `external_ddo154_v001/FIELD_V002_RESULTS.json` | `ee79f97a02f46be9aa4c421b2af263f8cd40e1657ec738116cbc5fd81df2151e` |
| `external_ddo154_v001/SCORING_FROZEN.json` | `a4ec7082f6aa495a9f5699926642c78c4a881d7d22b116606891d96f0e8bd9e3` |
| `external_ddo154_v001/ROTATION_COMPARISON.json` | `36d11667ee7ca1cd534db91bef3a18cb735a07a74d69bbc0d29ca53f2299ed65` |

Exact fine-field pair hashes (candidate first, Newtonian second):

| Stem from the census above | Candidate SHA-256 | Newtonian SHA-256 |
|---|---|---|
| `galaxy_HI1_H21` | `2b5d79a1d957624be4fc1df56eb5343c3b4a48e363c704061e1f779274f88ea8` | `1a8c572c3ab27156d324f7592cf4120844700255c12cb08625425d2d62080328` |
| `galaxy_HI0_H21` | `256ebc4dff82d902c99e94d8d24968241ef923a4bace9a679709791fd9c51a11` | `b92b34dd386ee9f05acdb31ce3f95d7f87455cafba627ad14e40e99c1dd56353` |
| `galaxy_HI1_H20` | `96afcab4aaf9b9ccb10f27867f76e33ccca1b4a303fba16d43c56ade754b6d10` | `ed0804c5c624c7423d66bf80ca4b98735f8637ae21987a3aa114c032fa85b59b` |
| `galaxy_HI0_H20` | `d8e835ea6c415e661d81b4da7d08ce552b0eacaab28fbc4cd9dbf9ed9601563e` | `af78887ff83c08de8fcef4719bbfb8cf5b3292b0b541dff04e6c67acacd19864` |
| `ML36_CAL_HI1_H21_V001` | `2d246b3890fe91a2dc9df267fe2bb53bf0b286e19bbb730c07ff552819ed377e` | `d0fb392b28f89057948066391823e67267946f75d1d9a0559a051c7fb68135d8` |
| `HALOGAS40_ML36_RETAINED_V001` | `53d619cbcdf8a304bde5ccf13a1e8ae1bdf77cebb7a8816cfab597b29a9cfce7` | `c520bb9148195541a3acfc6ef110974fb145886ad88cd27453a0a2a6338c6f8d` |
| `HALOGAS120_ML36_RETAINED_V001` | `85d5cd76a4b6a1bb1a44b0aa1c7cee0955da578dc5246cc09ec8cf550ae9e943` | `1c52b2027bd1769acbe6415e3cea5e0bd8e590830bfcca58346c61fb1c629351` |
| `DDO154_THINGS_NA40_ML36_H2OMIT_V001` | `557eb3831903848582a332c39d57f7a6ff39caa282346c6e65a04d0f5922e6dc` | `6933fd4295c6d7cbaa8c7c336ce61c84785094c84d064a5c8afe5f3426ff646e` |
| `DDO154_THINGS_RO40_ML36_H2OMIT_V001` | `40afe36a4cab46441b6a4fc89e6ac9cbb23aa1b30f9c9c1d086ee14bc9379b61` | `9ea2e67adc25b0db154a229192fd8946357cb5cb8a46c5bfbb5530e57c911f31` |

Qualification references are `GALAXY_FIELD_RESULTS_REVIEW.md`, `STELLAR_CALIBRATION_RESULTS_REVIEW.md`, `HALOGAS_FIELD_RESULTS_REVIEW.md`, and `external_ddo154_v001/FIELD_V002_RESULTS_REVIEW.md` plus `ROTATION_COMPARISON_RESULTS_REVIEW.md`. The future wrapper must authenticate their underlying numerical products, not promote prose alone to a numerical pass. NGC3198's inner R<2 kpc rows are a retained descriptive sensitivity; the inherited practical mesh/domain gate does not qualify them to the same standard as R≥2. DDO154's full 12-row force comparison passed its every-row gates.

## Fixed halo models, objectives and search

Use the spherical NFW density `rho_s/[x(1+x)²]` and cored pseudoisothermal density `rho_0/(1+x²)`, with positive scale `s` and nonnegative normalization. Their circular-speed shapes are

`f_NFW(x)=[log(1+x)-x/(1+x)]/x`,

`f_ISO(x)=1-atan(x)/x`.

These follow the original [Navarro, Frenk and White density profile](https://arxiv.org/pdf/astro-ph/9611107) and the NFW/ISO equations in [de Blok et al., sections 5.3.1–5.3.2](https://arxiv.org/pdf/0810.2100). The spherical halo is superposed with the **saved Newtonian disk force**, not with a spherical reinterpretation of the disk.

For conditioning choose a fixed pivot equal to the median of **all valid radii** in that galaxy, also for the R≥2 subset. Write `s=pivot*exp(ell)`, `F_i=f(r_i/s)/f(pivot/s)` and

`v_i(A,ell)=sqrt(b_i²+A F_i)`, `A>=0`.

Thus A is the halo speed squared at the pivot, not an independently floating baryonic normalization. Derive `rho_scale=A/[4*pi*G*s²*f(pivot/s)]` if reporting the physical density parameter. Fit velocities, not squared velocities.

For each of nine sources and each of two halo families, fit each of these four configurations: all radii/equal weights, all radii/quoted-error inverse variance, R≥2/equal weights, R≥2/quoted-error inverse variance. This gives **72 fits**, with identical fixed observations and baryonic forces supplied to the two families. Weights are respectively 1 or `1/sigma_i²` with no error floor or fitted scatter. The fixed network curve receives the same four descriptive scores and no extra local parameter.

For fixed shape, minimize `J(A)=sum w_i(v_i-y_i)²`. All resident velocities are positive and baryonic squared speeds are positive. Consequently

`J'(A)=sum w_i F_i(1-y_i/v_i)`,

`J''(A)=sum w_i F_i² y_i/(2v_i³)>0`.

Use A=0 if the right derivative there is nonnegative; otherwise bracket the unique positive root by `A_hi=max_i(y_i²/F_i)` and perform 96 bisections. Since `b_i²>=0`, every predicted speed at this upper endpoint is at least its observed speed, so the derivative is nonnegative. This is an analytical root bracket, not a finite astrophysical amplitude prior.

The parent-approved deterministic scale search uses `ell in [-20,20]`, both 257- and 513-point grids, and 80 golden-section refinements of every sampled local-minimum bracket. Retain both finite endpoints, all resolved local minima and the exact scale-limit shapes: NFW `(pivot/r)` and `(r/pivot)`, ISO `1` and `(r/pivot)²`. These limits are normalized speed-squared shapes and may correspond only to a parameter infimum, not a finite identifiable halo. Record that distinction and boundary/flat-profile flags. Check fine/coarse best objectives within `1e-6*max(1,abs(J_fine))`; preserve any failure. This is a deterministic convergence screen, not a theorem excluding arbitrarily narrow missed minima. Do not fit the search bounds after seeing a preferred radius.

Implementation controls should independently verify stable small-x shapes, the density-to-enclosed-mass formula, positivity, exact size asymptotes, amplitude boundary/root conditions, synthetic recovery and unchanged raw row census. The wrapper/helper and this design must be hashed before actual fitting; their newly written source is not authenticated by the older field manifests.

## Deliverable and interpretation fixed in advance

For every fit save all original rows, halo and total speeds, signed residuals, the full fitted index mask, halo parameters or boundary limits, profile minima, optimization diagnostics, velocity SSE/RMS and quoted-error squared residual sum. Report both scores for both weightings, plus all-row and R≥2 summaries regardless of fitting subset. NGC3198 R≥8 is a descriptive outer summary, not an additional optimized cut. Never omit an unfavorable source, family, central row or boundary minimum. Each fit's objective must be no worse than its A=0 Newtonian control within numerical tolerance.

Every fit's prediction/residual curves must cover the full original 43- or 12-row census, including rows outside its fitting subset. The deterministic optimization grids may be retained as SHA-256 digests together with minima, endpoints and convergence diagnostics rather than every temporary evaluation vector. Splitting the complete output into nine source-variant result files plus one authenticated census is allowed; this is publication sizing, not a change of scientific criteria or selection.

The quoted-error objective is descriptive: no full radial covariance, source/geometry covariance or nuisance marginalization is supplied. Do not publish a likelihood ratio, Bayes factor, AIC/BIC preference or discovery significance from these numbers. Report the two local halo parameters and the network model's previously calibrated common inputs separately; neither label the network globally parameter-free nor ignore its already exposed development choices. The distance-only fitted network curves are not substituted in this primary comparison.

If fitted halos do substantially better, the saved fixed network law has a concrete residual-shape deficit to explain. If its errors are comparable without per-galaxy halo parameters, that is useful conditional parsimony/transfer evidence, not elimination of dark matter. A free NFW fit without a cosmological concentration–mass prior is a rotation-profile comparator, not a test of the entire cosmological dark-matter framework. Neither outcome derives the native source/metric dictionary, closes the expansion/state ledger, or completes joint Stage 2 by itself.

This is a small saved-array calculation. No new PDE, source reconstruction, long-running trajectory or observational download is necessary.
