# Lane B freeze/score readiness — Codex3, dispatch 0516

date -u: `Sun Oct 18 12:24:42 UTC 2026`

**Result: TESTED synthetic pipeline, 85/85 checks; production freeze remains BLOCKED.** No scientific forward, route-A or route-B launch occurred. No real NGC3198 target or observed-velocity file was opened. No network, forbidden run directory, session log, deletion, move, rename, overwrite or git write was used.

The current engine v003b and freeze v003d completed an end-to-end synthetic 3D/fixed-DDO-distance pipeline with 10 admitted representative members and 43 rows each. The new boundary candidate v002 completed the same flow for continuum_v001 and a separate nodes_v001 branch with RO1 fired. The nodes branch tests interface handling only: R1 adopts continuum_v001 for NGC, and the current driver does not implement NGC tail route B. The synthetic ro1/uv_tail records are source-derived field layouts with invented digests, certificate labels and values; they are not complete authentic driver runs or scientific certificates.

## What was tested

- Every member has the ordered 43-row manifest. An independent arithmetic oracle checks pointwise min/max bands and every LADDER field: observed/predicted synthetic speeds, quoted sigma, signed residual, sigma ratio, fractional error, validity and within-error count. The denominator is always 43. The headline is the member-count distribution and the frozen reference, not a pointwise envelope.
- The ORIGINAL_K alternative is evaluated at the same selected points with a synthetic offset and scored separately. M/L alternatives and GL10 remain NOT_EVALUATED_BEFORE_FREEZE. The candidate preserves both alternative status and headline separation.
- Both NGC geometry slots are attempted and refused at both box ends with GEOMETRY_NOT_EXPOSED: 4 refusals, all 43 sensitivity-band rows invalid by design, and no false zero-sensitivity claim. Headline bands retain A13/A23 conditions.
- Before synthetic target creation/access, a new external-log analogue records manifest, registration, calibration-record and observation-region hashes. SF-3 checks bind the calibration registry and region before scoring. Hashes are computed from file bytes. Edited manifest copies, wrong external manifest hashes, missing synthetic target rows and target-bearing freeze notes refuse.
- Fourteen adversarial raw-result probes cover missing map/row entries, honest null INVALID truncation, contradictory finite INVALID rows, Q01/Q02 honest null GL4 rows, duplicate rows, map/row mismatch, raw target fields and aliases, unarmed/malformed RO1, pending certificates, missing stage digest and missing nodes context. The candidate refuses every probe before a valid freeze reference can be selected.

## v003d compatibility findings and candidate fix

**TESTED:** v003d accepts the v010-shaped valid/speeds_km_s projection and ignores rows, invalid_rows, ro1 and uv_tail. Honest null INVALID rows already make its entire member invalid. However, it accepts contradictory finite rows marked INVALID, a missing rows entry while the speed map stays complete, and raw target fields, because those fields are not consumed or scanned. Its writer refuses exact target_rows but accepts the adversarial notes key targetVelocityKms. The suite preserves that accepted adversarial manifest as evidence; it is not an approved freeze.

Candidate `prediction_freeze_v010_boundary_cx3v002.py` is a separately named copy of v003d with exactly two existing function changes: `_call_forward` preflights raw results, and `_scan_forbidden` normalizes target-field aliases. One helper `_v010_preflight` is added; MODULE_NAME changes. All other functions, including scorer arithmetic, record binding, selection, headline rules and exclusive creation, are AST-identical. The candidate requires 43 consistent valid rows, an armed coherent RO1 record and syntactically complete tail metadata, including separate continuum/nodes handling. It does not relax INVALID handling. Review and real custody integration are pending; metadata shape is not certificate authentication.

## Production blockers

**TESTED and material:** adopted slots V002 marks Q01/Q02 INVALID under primary GL4. A synthetic reconstruction using precisely that validity pattern makes v003d unable to choose any reference member. This differs from the all-valid fixture used to test the mechanics. Current GL4 therefore cannot produce a completed freeze under the existing D1 rule, even before any outer truncation. Claude2 must resolve this openly while retaining all 43 rows and invalid-as-miss semantics; GL10 is currently an unevaluated alternative, not an implicit repair.

The typed blocker file assigns owner and deciding step for the missing NGC tail producer, GL4 row-policy conflict, candidate review/real custody, real geometry wrapper and real scientific admission/alternatives. No claim here closes those dependencies, grants launch authority or permits real target access. A15 expectations were read as required context but are never read by the synthetic pipeline; runtime external reads are restricted to the two base modules, toy harness, target-free slots and driver source bytes.

## Resources and preserved attempts

Final run used one Python process, single-thread BLAS environment, no subprocess or network creation, and a read allowlist with exclusive-create output guard. Recorded peak RSS: 58,114,048 bytes (about 55.4 MiB). The macOS runtime rejected RLIMIT_AS; the exception is recorded, and observed usage remained far below 8 GiB. The final successful run is v004 with 85/85 checks. Earlier v001 failed before outputs when setting RLIMIT_AS; v002 preserved its new calibration record then refused registry creation under an overstrict audit guard; v003 passed 78/78. All prior source and partial outputs remain, and no reviewed file changed.

## Byte custody

All cited paths below include SHA256 computed from their actual bytes. The accompanying output manifest inventories every lane file except itself; its own hash belongs in the immutable exchange packet. Open V005 decision bytes are a point-in-time snapshot, not a declaration that the file is frozen.

| File | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/RESULTS_CX3V004.json` | `41064ebd44339ee2c4a1ef46a1d10e42b420bdb2d13aa475c0e12746c02d38f3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/prediction_freeze_v010_boundary_cx3v002.py` | `edb86bfd60108db625fcc893ea646262f3edfdcf361c3a0d1b62dbb08b393d36` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/test_freeze_score_v010_cx3v004.py` | `8c5a562fdfe504fa2d701435551b941655950487c5a7f8145742add4c22fe6d0` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/DIFF_V003D_TO_BOUNDARY_CX3V002.diff` | `7a6d6420c342bdb89c0215b7d0d037cc1241f65c86d86cf2b76a3cf606d0d6e3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/TYPED_BLOCKERS_V001.json` | `faa2b34105f06b2e2b6c8e68b925bf5f613c3242676bea5f9d7411ac640d91d0` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/SOURCE_DELTA_V001.json` | `225eee59aa555cc6443d1c429ff92392bd2e4a1d9365d53f8c3a27e710f0d2cd` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/INPUT_HASHES_V001.json` | `b66bf6ada821a714459bcb0e080d979b9313c4022ccc3d81113a8adb8819e613` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/v003d_continuum/FREEZE_MANIFEST.json` | `cd1114046b754b3d618aa31c80e9961a3b0bb3f26db39061c8bfa82fa3032c1a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/v003d_continuum/FREEZE_REGISTRATION.json` | `9604ea7d5b293b9abbcce0efc4e3b3d7d3bf432ae5b85dc595fac0b3fd1de77a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/v003d_continuum/PRE_TARGET_REGISTRATION.json` | `372c83f84727d365ed6ec403780bd17cad9c7f4e6548befbe78710c2a7588fee` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/v003d_continuum/LADDER_SCORE_SYNTHETIC.json` | `0d6c582514727294caead0ae7cb97ae9b0c1543fc02dc697364182356438a2db` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/v003d_continuum/SYNTHETIC_TARGET_ROWS.json` | `6e16ea5d4452ae386f1dd75c79c957073375ddd58579fa8123e0ab4191b2ce07` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_continuum/FREEZE_MANIFEST.json` | `cc8cbe066ab6bcf3f2d66de4a6cee4da7d7bf79ee365be65139658981ad5e7c1` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_continuum/FREEZE_REGISTRATION.json` | `dec50c0488f91551b30d5e21ce25b4fa7b04bedfb33638908d0d06bb11b5ca52` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_continuum/PRE_TARGET_REGISTRATION.json` | `61477c498981cf36a7aa1c6cf541cb5ce2f782ea8e1650cc236f02a99ec6fc5f` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_continuum/LADDER_SCORE_SYNTHETIC.json` | `4d69c497bea9e789528aeb8ed20ee5ec3e7eb730a279a54f5e16f61546d7812a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_continuum/SYNTHETIC_TARGET_ROWS.json` | `6e16ea5d4452ae386f1dd75c79c957073375ddd58579fa8123e0ab4191b2ce07` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_nodes_ro1_fired/FREEZE_MANIFEST.json` | `78094b8ca69ef17ce9c34fad4b05ff59513d85bdbd7e2a9067bcecabc15c1790` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_nodes_ro1_fired/FREEZE_REGISTRATION.json` | `f9893e3e099220710ae72a80e6ae2969d67d4b3271f737626c241a8757b19a8d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_nodes_ro1_fired/PRE_TARGET_REGISTRATION.json` | `bddd33d8cb2d229bb2ca8a3990669ffa30f34c285c82e5777950a1839267d7c7` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_nodes_ro1_fired/LADDER_SCORE_SYNTHETIC.json` | `72c7fec23c9731efd40149370d4e6ad44b1e238ce4c13aede49810810ed13a37` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/synthetic_checks_v004_20261018T122433Z/successor_nodes_ro1_fired/SYNTHETIC_TARGET_ROWS.json` | `6e16ea5d4452ae386f1dd75c79c957073375ddd58579fa8123e0ab4191b2ce07` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0516_2026-10-18_codex3_ngc_route_readiness_and_freeze_score_readiness.md` | `bd4ff40fe0f42254b6da59ada5d6f702016cf70cfa8e3d92018ae21cf28c51c9` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md` | `59ada35ce59146c758374c88abeb3ed183f09217501d1f3c7a43463adacc6917` |
| `/Users/bgm/Research/Universal Network Theory/LADDER.md` | `b18e19aee7568d9ffb0a54710d2a99f890580b51e4b9a56a398fc53da199eae2` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/prediction_freeze_c2v003d.py` | `74e0d4060e443755486fba3aa0775060d2909c2bb78df9d948f346159112b67d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py` | `6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/ROOT_CALL_ORDER_V003D.md` | `c434542af7e1988ba57cb9062723745c2cc6d89633f13076569ca8f288e7958f` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/root_call_order/root_call_order_toy_v003d.py` | `92e0b20d6b7a7d448fa94e2501aa85afbcbd973af6ebca044718b06eea1cc779` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_freeze_c2_v003b/guard_check/v003c/prediction_freeze_c2v003c.py` | `3d58b5fbb5699b8a099a46164c0128cb04f17d7417a168ceda2a81dbfb03c5f5` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_freeze_inputs_c3/NGC3198_FREEZE_SLOTS_C3V002.json` | `4c5951cbef9aa2c1cf7e7e4c859b59a7aafb5476bd7e59c20caef769376f6c7e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_freeze_inputs_c3/NOTES_NGC_FREEZE_INPUTS_C3V002.md` | `57234507e4f321cda55c8a09872e77197df6638f34d502f5f1a24e01e6b1b8ca` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py` | `b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json` | `c691cab6dd9752a7bd98025cf7357a5c729b3fef90a78a6277195c5520671e33` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V002_ADDENDUM.md` | `17c2661603488478bafe2988e34e5c7b311bc7d8f6100fe75612b0c43f32648e` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V003_ADDENDUM.md` | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md` | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md` | `b3f2f38283767a0ff3aaca4a1c330a310f18ff0e89159c983ca241effa6a4028` |
