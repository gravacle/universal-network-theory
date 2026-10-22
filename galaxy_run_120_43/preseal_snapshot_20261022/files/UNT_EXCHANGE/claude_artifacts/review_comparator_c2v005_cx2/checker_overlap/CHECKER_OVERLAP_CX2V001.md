# c2v005 supplied-checker overlap addendum

`date -u`: Sun Oct 18 15:36:13 UTC 2026

**The ≥20 independently authored canary-template requirement is supported.** The existing primary suites contain 23 structural plus 24 invocation templates (47), independently constructed before this supplied checker was available to this lane. Each ran under r4 and r5: 94 executions. The nine source-audit whole-gate executions and two duplicate-NPZ follow-ups bring the prior total to 105. These are not 105 unique templates.

**No claim of 20 semantically non-overlapping templates is made.** Independent origin and novel coverage are different claims. Both suites exercise the same contract; the older c2v004 checker was read to identify overlaps. The supplied checker explicitly ports that predecessor and adds its own cases. Its source contains 83 literal comparator-case declarations; this is a static inventory, not an execution result.

Provenance is supported by immutable own source, preparation and result records: invocation preparation at Sun Oct 18 15:05:20 UTC 2026, structural report at Sun Oct 18 15:19:23 UTC 2026, invocation r4/r5 records at 2026-10-18T15:18:59.828348+00:00 / 2026-10-18T15:19:23.472998+00:00, and source-audit follow-up at 2026-10-18T15:20:57.202024+00:00. The contemporaneous own reports state the successor checker was unavailable when they were sealed. This addendum does not claim a filesystem timestamp alone proves historical absence. Source inspection confirms independently generated fixtures, with no imported supplied checker builder or copied prior run tree in the primary suites.

STATIC REVIEW ONLY: the supplied checker was read and AST-parsed, never imported or executed. Part F calls real-run stand-in regressions; no such path was followed. No new comparator/scientific execution or real-run/receipt read occurred.

| Own cases | Nearest supplied cases | Relationship and distinction |
|---|---|---|
| Structural P01; invocation P00/P01 | P00_baseline_B0P, P00_baseline_Z2, P06_Z2_reference_swap_v008_to_driver_uvt_declared | DIRECT FAMILY: Positive synthetic baseline and declared successor custody. Independently built trees, not novel failure categories. |
| Structural P02/P03 | P01_stage_json_reformatted_key_order, P04_masked_keys_differ | RELATED: Own whole-result order/ended clock versus supplied stage JSON order/time mask. |
| Structural P04/F12/F15 | F03_extra_inputs_file, Q01_inputs_json_content_changed, N21_call_spec_leaf_differs | RELATED: Input presence/content family; own equal extra nested input and different contract shape. |
| Structural F01/F02/F03/F04/F05 | F04_duplicate_stage_number_tampered, F05_duplicate_stage_number_extra_copy, N05_duplicate_stage_number_distinct_names | RELATED: Own partial earlier/later aliases, equal collisions on both sides, tampered middle and empty extra stage add boundary shapes; duplicate-stage family overlaps. |
| Structural F06/F07 | N08_Z2_manifest_stage_missing, N37_stage_dir_renamed | RELATED: Own missing body and renamed suffix versus supplied missing manifest/renamed reference. |
| Structural F08/F09/F10/F11 | F07_stage_npy_1ulp, F16_result_unlisted_key_signed_zero, F20_result_unlisted_key_float_to_int, F21_result_unlisted_verdict_keys_flipped | RELATED: Scientific value and whole-result content coverage overlaps. Own nested one-ULP/key addition/removal differs from supplied scalar substitutions. |
| Structural F13/F14 | F03_extra_inputs_file, Q01_inputs_json_content_changed, N36_inputs_file_renamed | RELATED: Own raw binary last-byte and missing-binary controls; supplied input probes are JSON/filename. No exact binary-input mutation found. |
| Structural F16/F17 | Q03_toplevel_finish_changed | DIRECT/RELATED: Failed finish status directly overlaps; nested residual with intact status is a different concrete leaf. |
| Structural F18/F19 | Q04_route_a_attempt_result_changed, N17_attempt_finish_differs | RELATED: Attempt output content family; own nested entropy ULP and removed subrecord differ. |
| Invocation F02/F03 | F09_stage_argv_value, F10_route_a_argv_column_workers | RELATED: Ordinary argv comparison; own swapped value positions and repeated non-tail option. |
| Invocation F04/F05/F06 | F11_route_a_declared_flag_twice_first_outside_run, N12_Z2_config_sha_of_another_file | RELATED: Duplicate/malformed tail argv. Own joined assignment, missing final value and identical valid in-run duplicate are distinct concrete inputs; no exact joined/missing-value case found. |
| Invocation F07/F22/F23 | F12_Z2_rotation_dir_flag_on_reference_stage, F13_Z2_tail_flag_on_non_UVT_kind_stage, N11_Z2_truncation_flag_on_reference | RELATED: Stage/side/path restriction family. Own route-A-only flag on reference, flag on REF side and outside-run manifest differ. |
| Invocation F08/F09 | F24_script_swap_hidden_by_declared_token, F26_Z2_reference_swap_to_plain_base_not_uvt, N02_A59_F1_hole_base_ran_under_append_tokens | DIRECT/RELATED: Base-on-NEW refusal overlaps directly with F26. Own F08 additionally requires replace-mode TOKENS_POLICY to pass; N02 uses invalid append mode. F09 changes only hash. |
| Invocation F10/F11/F12/P13/P14 | F14_stage_json_signed_zero, F15_result_rows_signed_zero, F17_checkpoint_record_signed_zero, F18_stage_json_float_to_int, F19_result_rows_float_to_int, F22_result_pass_unlisted_key_bool_to_int | RELATED: Same strict numeric type families, moved to nested request matrices; own matching signed-zero/mixed-type positives. No request numeric_contract matrix case found. |
| Invocation F15/F16/P17 | F07_stage_npy_1ulp, P02_npz_recompressed_same_arrays | RELATED: Array equality family overlaps. Own imaginary signed zero, integer/float NPZ dtype and C/F logical-content positive have no exact literal counterpart in cases(). |
| Invocation F18/F19/F20 | N07_symlink_in_new | RELATED: Symlink rejection family directly overlaps; own dangling, external payload and directory links broaden target shapes. |
| Invocation P21 | P06_Z2_reference_swap_v008_to_driver_uvt_declared | RELATED: Own valid contiguous route-B tail-block prefix insertion has no exact supplied mutation; same valid tail-block family. |
| Source-audit normalized-key collision, structured NPY/NPZ dtype, duplicate JSON keys and duplicate NPZ members | No corresponding add(...) mutation found | NOT FOUND IN CASE LIST: Source inspection found no explicit canary for these reproduced false-PASS mechanisms; this is not a claim that all helper paths lack incidental coverage. |

The supplied checker also covers token derivation, fill-tool guard/type/refill paths, progress/attempt ledgers, static pins, driver-selection mismatches and manifest ordering. This addendum does not claim the two own primary suites are a superset. Existing comparator FAIL and scientific comparisons UNTESTED/BLOCKED remain unchanged.

All cited source/evidence files and SHA256 from bytes:

| File | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/tools/selftest_c2v005.py` | `12dc576a5581adc254d99fd75d54517caaaa8f999a641a593c20f1393985adae` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/run_structural_canaries_cx2v002.py` | `7d924e33374183dd1935cf31c93cb154ca444cce9965feced2956b943046ad7e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/common_structural_cx2v003.py` | `db5d7dabecb5306d834eaf07ccf6881f4152a9c147fa107ad53ede5b2aff576e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/STRUCTURAL_SUMMARY_CX2V001.json` | `9c34726fa2e0cc1fc8e828c3d08e406b1f87706a7dfc372e36dafd71302b1eb3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/STRUCTURAL_REVIEW_CX2V001.md` | `a0245b9bce6f95ec195e04523f9146b3949e1fba8b7d25e1b9c5e2c8609fbc71` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py` | `711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/c2v005_r4_canaries_v001/RESULT.json` | `21809faec02fc08f2b0972a2c98e2c3e0c01b9f9a8b3a03d7546f2709508fc79` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/c2v005_r5_canaries_v001/RESULT.json` | `742994b147b03e0c3139ab2537e8fdb30f63ab9c88143576cb102044ac06be3b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/PREPARATION_CX2V001.json` | `93fbffaf693745ad686a31edf81dd8c354207950f9a279bb99f205da035a620b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/INVOCATION_REVIEW_CX2V002.md` | `c9a22571260754f36e6c53e47a683c7e8cdde2efe8aa8d9b18c9b48ee1245597` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_whole_gate_v001/RESULTS.json` | `11eeb55904bc8daa714c5e1fd4776833bb6a560a15280eb01805055b4b68c546` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/v005_duplicate_npz_v001/RESULTS.json` | `1ac023bb4a3e80c0741a99abf7216cdbc6347992f1baf0e28f2c689f302bf2eb` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/test_whole_gate_edge_cases_cx2v001.py` | `4b2635f65472bdca319f3d4aafbac4b0e908e033fa3dca5d69d43d8cf33267fa` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/test_duplicate_npz_members_cx2v001.py` | `3f94c347ec5714873c0e61326aba5df50f5f88dd1d07b7cc2bce567596c4c8db` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/source_audit/ADDENDUM_NPZ_MEMBERS_V005_CX2V001.md` | `d374e2b4443e5e4857b398c2307e70e808e66bde7a378a176b08d881b685d832` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/REVIEW.md` | `9317cd0dbaafc967ec80d6f2a4f13c470b6d6d8630e8d3b5c5ed2d4a4edf25e2` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/checker_overlap/build_overlap_addendum_cx2v001.py` | `422f86d34be16ee4d9fe144dcea193836841c375f63cf91d17e2fece4fd6dc8d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/run_20261018T151802_90972/STRUCTURAL_RESULTS.json` | `fb7e0baa367ab8a6f68afae408bb59f21aebc128b7a8e5c903773535382948bc` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/run_20261018T151802_90973/STRUCTURAL_RESULTS.json` | `6cec3c76ccab462f0197e9a2fd5531e33eb512b2b2250c1ff9b03c77b4f4ccac` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/checker_overlap/CHECKER_OVERLAP_CX2V001.json` | `acd9f806b29fb7b85ab01c551f77148996dcb9c2af3654dc476d9e13addc70b0` |
