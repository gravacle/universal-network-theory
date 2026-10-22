# Codex1 0588 preparation: NPZ fixtures and partial-check ledger

Sun Oct 18 18:17:17 UTC 2026

TESTED: seven direct-parser NPZ fixtures pass expected outcomes: clean control, extensionless alias in both archive orders, extensionless-only, duplicate raw names with equal/changed payloads, nested alias. Existing c2v007 already refuses these; each becomes a must-fail regression in the successor selftest.

TESTED re-judgment:58/58 available partial selftest rows match the frozen c2v007 expectation table. The two legacy harness baseline expectation_met=false rows are expected NORM_INJECTIVE failures in that table, not a new comparator defect. Token-policy output reports266 rows,0 breaches. Site inventory/root-scan/SF3 outputs retained as leads, not review verdicts. No overall partial-check PASS is claimed.

Codex2 full c2v007 review has not landed; immutable r2 implementation waits for its blocking/should-fix list. Prep files are under the authorized gates_v007/r2/prep. Full successor selftest remains UNTESTED. No real UVT/C5H run, observed velocity, network, scientific launch or overwrite. NGC LO91 and r6 BUILD remain pending; polling continues.

## Byte SHA256 citations

```text
83f978baecb06c8a434b26aa5b3c8048f66354c1ee2b77e222173854314d0bee  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/paths_regress/out/SELFTEST_RERUN_V001/A_whole_gate_r4/RESULTS.json
c6a327239d8576db4085158efca68690fa96809036e24effd17acef5dda8b1db  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/paths_regress/out/SELFTEST_RERUN_V001/A_duplicate_npz_r4/RESULTS.json
154d8abe5ad494a5621ce68db024fdc7369abe669e6d65c43e068676bb289a05  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/paths_regress/out/SELFTEST_RERUN_V001/B_invocation_r4/RESULT.json
8505bb9909958a53ccd8fefcf8480bc1c17eaaee2589466d95258cbb77a3eb3f  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/paths_regress/out/SELFTEST_RERUN_V001/B_structural_r4/run_20261018T181300_31535/STRUCTURAL_RESULTS.json
6c1acea7eae397698d633cae9e850cf3b2b77dcbae0f7d9b037c9f4092f9ebf8  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/tokens/out/TOKEN_POLICY_CANARIES_CKTOK.json
04dd60540a39ac0c47ceeac1cb12966477e4786acd9c8ad166bad7274f7866e3  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/tokens/out/DERIVE_INDEPENDENT_CKTOK.json
33e5b939ef0a5a235c81454582b1a862c43dd9cb28826a6267bc87fdf86f2de3  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/parse/out/A71_WALK/A71_WALK_CK.json
38175a0cd383c924ca36f0a4e7bf967e4f412f22160e4b6e34b5a1158cd19e91  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/parse/out/ROOT_SCAN/B0P_NEW.json
1eacd478e68807c01f111d54b484d355db979a501fcf67463c2305ee29cbd209  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/parse/out/ROOT_SCAN/Z2_NEW.json
017093f3837e9ddb450d9aa539675a3275568c4422514c1781ba05244a88f17d  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v007_c2/paths_regress/out/SF3_ENTRIES_V001.json
06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/run_identity_compare_c2v007.py
5f611606b6e5ee9ff01a1c7ea5a415f600f889488a845965d3aa80f315941996  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/selftest/expect_c2v007.json
4d8a503828b2be6a5a0161b3fdc5bd3b772d9129d2e46e19ec3fd22e984c4357  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/selftest/selftest_c2v007.py
b6f1360ab9515fa04fbcd88c65e631425aa90904f3c9c996bdef470068599d26  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/prep/prepare_npz_logical_cx1v001.py
02ba193a7e35aab352be4f7787cbd5a21c40d34d8c89c3289516195edc1313c8  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/prep/NPZ_LOGICAL_PREP_V001/NPZ_LOGICAL_PREP_RESULTS_V001.json
3139701dfe7cf6db835f293a00e81b2eceac6e68c839b92ebcd710c779534b5c  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/prep/PARTIAL_CHECK_LEDGER_CX1V001.json
```
