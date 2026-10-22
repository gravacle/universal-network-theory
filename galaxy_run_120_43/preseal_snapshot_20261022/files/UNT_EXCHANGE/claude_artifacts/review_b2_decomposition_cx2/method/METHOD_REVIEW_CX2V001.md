# A97 B2 method census and independent stellar arithmetic

`date -u`: Sun Oct 18 20:05:20 UTC 2026

**Source/method slice complete. The A97 row-level disposition is UNTESTED in this slice.** No allowance is changed and no outcome is advocated. Numerical per-row switching/decomposition is a separate independent lane. No reviewed producer/library was imported or executed; no original saved-run tree or target was accessed. Only explicit permitted source/artifact files were read, never paths followed from their contents. `nice unavailable (sandbox); 0514 waiver`.

## Differences established from source

| Aspect | ADV KB12 basis | B2 basis and interpretation |
|---|---|---|
| Domain / transfer | `box_discrete`: box12 minus cubeK, 1/(4γk²) | Same domain and asymptotic transfer. ADV's q(k) diagnostic does not enter `cart_tail`; disk_discrete is a different optional domain, not this reference. |
| Gas | Radial discrete rings at source rotation nodes; all-azimuth masses | Registered cubic Lagrange in s=R² at GL4 columns. Production integrates in s with M_s128; independent integrates the same polynomial in R. This is an unnamed source representation difference. |
| Stars | `stars_from_prep(continuum=False)`: GL4 radial/core/segment/u-tail and GL4 vertical nodes | Continuum registered profile plus analytic sech² vertical transform. The named star-roster difference includes radial and vertical quadrature. ADV's48/200 continuum option is only the separate stars-only diagnostic. |
| Angular statistic | `rows_P16` uses16 discrete azimuths; `rows_m0` uses J1 | Original gated comparison already uses P16 on both sides. P16−m0 is a separate named diagnostic, not a difference to subtract automatically from P16-vs-P16. |
| Integral quadrature | kx/ky positive quadrant×4 (D4), both kz signs, width0.25/order6 | Independent full signed box: BASE0.25/order12; REFINED0.2/order14; COARSE0.5/order8. Production uses its ring/corner harmonic cube machinery, order8, widths0.05/0.02. Different symmetry implementations do not alone prove an incorrect integral. |
| Bessel evaluation | libm J0/J1 through ctypes | Independent periodic-trapezoid J0; libm used only for a crosscheck. Production has its pinned libm provider. |
| Stellar tail quadrature | GL4 u-map for box_discrete | Production t∈[0,40] exponential panels; independent t∈[0,44]. Both approximate the same infinite profile, not different physical sharp cutoffs. Independent bounds below. |
| State / source | `Case` selects `result.passes[-1]`, then that pass's field/source rotation, rotation and column manifest | B2 explicitly selects le3 feedback17, columns18, rotation19, column mean20, and gas from rotation15 (le2). C2/C4 saved baselines are reported equal. C3 ADV selects le4, so evaluation geometry, gas source and baseline differ together. Exact source custody is not verified by a baseline-row equality. |
| Rotation law | Linear tail force c²〈t_R〉, then Ω² increment and square root | Production adds tail into nonlinear denominator at each phi. Independent averages t,t_R first and broadcasts their means into that denominator (RI-8). P1b component rows are linear diagnostics. |
| Observation | Same described observation pipeline, adapter, R√Ω², density weights and binding inclinations | No intended observation-rule change. Provenance strings differ; source-state readout weights can differ with C3's le4/le3 choice. |

Source sites: ADV `stars_from_prep`, `Case`, `validate`, `cart_tail`, `rows_with`, `main`; independent `star_nodes_continuum`, `star_rings_discrete`, `gas_nodes_continuum`, `SavedState`, `cmd_state`; roster `StarsProfile._nodes`, `GasColumns.radial_factors`, `vertical_factors`; PATH1/PATH1b docstrings and `main`. Exact source hashes are below.

## Quantitative independent source-only calculation

Own code integrates each linear-profile segment analytically, the exponential tail analytically, and separately evaluates the4-point Gauss rule. DDO profile bytes are pinned. **TESTED arithmetic:**

- Continuum stellar zero-mode mass: **11,925,050.049454598 M_sun**.
- ADV GL4 stellar zero-mode mass: **11,917,945.795564117 M_sun**, relative difference **−0.0005957420607057326**. This measures a roster difference; it is not a newly asserted production defect.
- Largest GL4 u-tail radial node: **2.4571672033246883 kpc**; largest absolute vertical node: **0.12743395314223308 kpc**.
- Continuum t40 endpoint: **15.83801166441615 kpc**; independent t44 endpoint: **17.271702103956017 kpc**. Registered phase extent R_last+12a is **5.802178587637087 kpc**, a distinct quantity.
- Exact profile mass fractions beyond t40/t44: **3.634868997108413e−18 / 7.246808868264954e−20**. Between40 and44: **3.5624009084257635e−18**. With |J0|≤1 these bound the omitted radial transform magnitude relative to the continuum zero mode. They do **not** bound integral quadrature, derivative/readout errors or row differences.
- At kz=2,3,4,12 per kpc, GL4 minus analytic sech² normalized vertical transforms are respectively **0.002874474488359424, 0.006160578903363523, 0.010219936565444732, 0.01443887328970761**. Both equal1 at zero. These are source-transform samples, not row-error attribution.

## Saved variant semantics and C3

`IND_*_BASE.rows.discrete_total` is full discrete gas+stars through the linear correction channel. `mixed_gas_disc_stars_cont` changes stars only from that baseline; `mixed_gas_cont_stars_disc` changes gas only. `B2_continuum_v001_linear` has both continuum sources. `B2_continuum_v001` adds the independent mean-tail nonlinear-denominator reading. All become rows after Ω²→sqrt and observation, so source-component row effects are not additive; use per-row telescoping along an explicit switch order, never sums of independently maximized norms.

C3 already has same-le3 `discrete_total` P16 and mixed variants in its declared IND_BASE artifact. The missing currently declared artifact is a **same-le3 ADV-like m0/J1 reference**, and an exact ADV order6 P16 replay if that implementation is required. The old C3 ADV P16 and m0 both refer to final le4 and cannot supply a same-le3 alias. No saved le3 raw input has been shown missing. Its named inputs are source rotation15/le2, feedback17, columns18, rotation19 and column mean20 of the C3R3 run; these were not opened here.

An IND_discrete_total−ADV_discrete residual on C2/C4 combines quadrature, Bessel/symmetry implementation and floating-point/source-custody differences. Calling it uniquely quadrature would require another controlled isolation. For C3, the old ADV residual also includes the state change. The nonlinear/linear channel differences saved previously are not a dedicated bound on averaging before nonlinear insertion. No exact equivalence is inferred from matching final rows.

## Scope and exact byte pins

**TESTED:** own profile arithmetic, strict safe JSON metadata, all listed expected source pins and unchanged end pins. **SOURCE OBSERVATION:** method census. **UNTESTED:** original-array custody, replayed integrals/rows, common-input errors, the final A97 named-only row residual and acceptance. No active process remains.

- authority: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md` — SHA256 `78ba2e9a645cbdf3d31e2dc4dcc35b552e2af323500383bd81b3a0b8d9ab9d01`.
- adv_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uv_tail_study_c2/check/adv_tail_check_v001.py` — SHA256 `67a6eeb66b1f94fe356272a31294be012fa448f6c8c03b75cdab66fb540e896a`.
- adv_c2: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uv_tail_study_c2/check/ADV_TAIL_CHECK_C2_KB12_W025_O6_V001.json` — SHA256 `82a84edd0f952077c39a6b652618b951f1d300d97db17b692671d725083658c5`.
- adv_c3c4: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uv_tail_study_c2/check/ADV_TAIL_CHECK_C3C4_KB12_W025_O6_V001.json` — SHA256 `63dc4c7dd313f21c6e3638027b3511bfa134169e19189db86abf471a76710954`.
- ind_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/scripts/b2_independent_c3v001.py` — SHA256 `6c013801d8b86255c9ca042deb9de2a95adaa37a11fad06ea23abe104c6089d5`.
- record: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/B2_GATE_RECORD_C3V002.json` — SHA256 `d4b41ffcab00a05bf0bead8c943b8f3555fdeb91beda2cba430efa65431315d7`.
- input_map: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/B2_RECORD_INPUT_MAP_C3V002.json` — SHA256 `63bb11908a1884ea38dd9e738d00d5e2cabd6144b9f935f1ca487a39aae1ffe4`.
- path1_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/scripts/b2_path1_replay_c3v001.py` — SHA256 `8344c99852e28cad3206e2d24d474be6b42a0d77a6a8674245d2083fda49fb1f`.
- path1b_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/scripts/b2_path1b_module_components_c3v001.py` — SHA256 `086346feb343c7c4b454a51cb2bd049d33430936af533121240d55862f8df877`.
- roster_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py` — SHA256 `4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2`.
- library_source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py` — SHA256 `2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54`.
- profile: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` — SHA256 `f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b`.
