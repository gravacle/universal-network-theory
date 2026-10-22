# A97 B2 saved-component decomposition — CX2 v001

date -u: `Sun Oct 18 20:06:40 UTC 2026`

**TESTED:** the saved-component/readout decomposition passed 37/37 checks. This is a computational component report, not a B2 admission verdict. The 0.05 km/s allowance is unchanged. The fresh independent C3R3 le3 ADV reference is being computed in a separate lane; the old C3 ADV remains explicitly off-state here.

The excess in the same-state C2/C4 comparison is dominated by the unnamed gas-rule difference. The table shows maximum absolute values across 12 rows; these maxima must never be added.

| Quantity (km/s) | C2R3 | C3R3 | C4R3 |
| --- | ---: | ---: | ---: |
| Original production minus archived ADV P16 | 0.08213990321575437 | 0.09792780979164206 (le4/off-state) | 0.10832626088468089 |
| IND discrete minus archived ADV P16 | 1.1262102361797588e-11 | 0.0028638312519575493 (off-state) | 1.3713474800169934e-12 |
| Gas discrete → continuum, stars held discrete | 0.07899770395344774 | 0.0953735724132514 | 0.11137130880039336 |
| Stars discrete → continuum, gas held continuum | 0.030115450568374058 | 0.0356225797997638 | 0.03835728930356197 |
| Exact denominator force minus linear force | 2.6874328895587496e-7 | 1.9808299356327552e-7 | 1.2984194697196472e-7 |
| Named star contrast with gas held discrete (alternate order) | 0.030160704319449394 | 0.03568531612788206 | 0.038434533343675525 |
| Actual P16-to-P16 alias change | 0 | 0 | 0 |

**Named-only, same-le3 result:** the gas-matched stellar-roster contrasts 0.03011545 / 0.03562258 / 0.03835729 are each below 0.05. Both sides explicitly use the same linear lapse-force prescription `c² d_R t`, P16 azimuth average, continuum gas, and saved le3 state. The row readout itself remains nonlinear: it updates Omega², takes the square root, computes emissivity-weighted column means, then interpolates to rows and applies inclination. This is a directly computed common-force intervention, not a subtraction of scalar error maxima.

The independent saved-component calculation reconstructs five variants from the pinned `tR` arrays: both discrete; continuum gas/discrete stars; discrete gas/continuum stars; both continuum with linear force; both continuum with the exact kept-plus-tail denominator. It independently recomputes the exact force from the allowed saved OFF full fields and `t_total`, and computes the rows using saved readout weights. The zero-force baseline, all five saved row variants, exact force, source-force addition, and telescoping closure pass. No project module or producer is imported or executed.

The explicit gas-first chain is:

`archived ADV P16 → IND discrete → continuum gas/discrete stars → continuum gas/continuum stars (linear force) → exact denominator force → production`.

Every signed 12-row contribution and each intermediate row vector is saved. The first step is a combined reference-representation residual: Cartesian quadrature/implementation/roundoff and any remaining custody mismatch are not uniquely separated by this contrast. It is at most 1.13e-11 km/s for same-state C2/C4. For C3 it additionally contains the le4-to-le3 state change and cannot be treated as a same-state integration error.

At the raw worst row (row 08), C2's gas contribution is +0.07899770395344774 and star contribution +0.0031421700682443543 km/s; C4's are +0.11137130880039336 and −0.003045050246086589. Their signs explain why scalar-max summation is wrong. All other contributions and all rows appear in the result JSON.

The gas-first and star-first stellar contrasts differ by at most 9.0621e-5 / 1.30352e-4 / 1.69615e-4 km/s, respectively, from the nonlinear square-root row mapping. Both orders remain reported; no unique order-free additive attribution is claimed.

**Distinct mixed-force comparison:** production exact versus the gas-matched discrete-star *linear-force* reference has maxima 0.030115525466314352 / 0.03562262986638132 / 0.038357306548249426 km/s. These include the tiny nonlinear-denominator and implementation terms and are **not pure stellar-only residuals**. Full crossed exact-denominator references would require discrete-source tail-potential arrays, which these archives do not contain (`t_total` is continuum-only). That uncomputed variant is not needed for the explicit common-linear-force contrast and is not fabricated.

The original ADV `P16 − m0` vectors are saved only as diagnostics. Both actual compared channels use P16, so there is no m16-alias intervention in this chain. In particular the old C3 alias diagnostic is le4 and is not relabeled le3.

No production/shared-input error was detected in the tested force/readout relationships and byte joins. This does not prove all shared physical definitions correct, independently regenerate source quadrature, or replace the parallel method/provenance review. Same-state full-box discrete C2/C4 agreement and production-versus-independent continuum agreement are separately visible; neither is used to waive the fixed allowance.

Execution: 0.230138 s, peak RSS 172802048 bytes, zero protected-path attempts in the successful run. Three exact C2/C3/C4 le3 OFF NPZ files were admitted only for this new A97 task; their canonical paths were checked component by component before reads. No C5H, UVT, target velocities, broad run listing, network, or scientific launch occurred. The earlier stricter B2 record review is unchanged.

Harness history: v001 stopped before component computation because the strict guard blocked lazy loading of the standard-library ZIP filename codec. Immutable v002 preloads `encodings.cp437` before installing the input guard; it passed. This was a harness issue, not a scientific finding. No previous artifact was edited.

Evidence:

- Harness: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/decompose_saved_components_cx2v002.py` — SHA256 `451a4ac93a44c9802637d32af9e54ad59aac05aa034d7658338cf8e7fe3d6efd`.
- Result (37/37): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/run_20261018T200537Z_93548/RESULTS_CX2V001.json` — SHA256 `0d672be05df87becc9ed5486946d20f23203921796b22b2e7e19b963e5a0cbe3`.
- Exact-versus-linear supplemental vectors: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json` — SHA256 `14243ae1e05e52172b58934dd7bae76f4549cb0f531e331e882da5c2ab30427d`.

Input pins below were rechecked unchanged at report sealing. They are explicit admitted files; embedded production pointers were not traversed automatically.

| Input | SHA256 |
| --- | --- |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md` | `78ba2e9a645cbdf3d31e2dc4dcc35b552e2af323500383bd81b3a0b8d9ab9d01` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/B2_GATE_RECORD_C3V002.json` | `d4b41ffcab00a05bf0bead8c943b8f3555fdeb91beda2cba430efa65431315d7` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path1/C2R3_CM_ON/observation/result.json` | `d2e835a95f8ce25bb4e07f454367138635c631073b5e63867d223a1c2b806c9b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path1/C3R3_CM_ON/observation/result.json` | `9735dc5adc90a75175348959210f9f5a75429c5ebb72263216f3a2581d134224` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path1/C4R3_CM_ON/observation/result.json` | `163284e2c349e6d8410e28b40fa25a68d4debbfd4b8be6e3141ce401a233f1ca` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path2/IND_C2R3_BASE.json` | `65861f0b7eed2a3ae329fe3f5caf8cbf08fe03b95e7b04740670b01156f5b5a9` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path2/IND_C2R3_BASE.npz` | `f495f1bbaa91e15f8e0dd73ad0efad195877d3aa630ba0ef26aaebb798b6d84a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path2/IND_C3R3_BASE.json` | `fdbacd7de467c10924d5201b0b168f974a8206d59ee2100473b9340623cfcbce` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path2/IND_C3R3_BASE.npz` | `ea16f2e0297e804beef897571689f8ba7fdd37ee39ccb70309471f4dc5ce60ca` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path2/IND_C4R3_BASE.json` | `94827aaeb57541c9abb4ad09856150c916369cf0642cd157c90bbadc76cc3f68` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/out/path2/IND_C4R3_BASE.npz` | `ce3e6b02dd38f960f5dcc12c2ea0186719848d71dc53ef8ddc6bd8c82f60d51e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/gate_b2_c3/scripts/b2_independent_c3v001.py` | `6c013801d8b86255c9ca042deb9de2a95adaa37a11fad06ea23abe104c6089d5` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uv_tail_study_c2/check/ADV_TAIL_CHECK_C2_KB12_W025_O6_V001.json` | `82a84edd0f952077c39a6b652618b951f1d300d97db17b692671d725083658c5` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uv_tail_study_c2/check/ADV_TAIL_CHECK_C3C4_KB12_W025_O6_V001.json` | `63dc4c7dd313f21c6e3638027b3511bfa134169e19189db86abf471a76710954` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/uv_tail_study_c2/check/adv_tail_check_v001.py` | `67a6eeb66b1f94fe356272a31294be012fa448f6c8c03b75cdab66fb540e896a` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/stages/19_le3_rotation/rotation/rotation_base_arrays.npz` | `5e66907c56497c30d616e50c82e2e271609d5adbf1f2a7c38687b0676986ddc0` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001/stages/19_le3_rotation/rotation/rotation_base_arrays.npz` | `f5709f8423fcf7de1373cab4043efad261ad2d5aece22e5342d5254e4b449d04` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/stages/19_le3_rotation/rotation/rotation_base_arrays.npz` | `b9a19e391e94f3e9bf8ab5e8c45f6521e00d717c7a4f561a4710262d4b900e60` |
