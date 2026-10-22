# c2v005 structural cross-lineage review — PASS within scope

UTC (`date -u`): Sun Oct 18 15:19:23 UTC 2026

TESTED: **46/46 executions pass**, comprising **23 independently authored case templates** run separately with `--driver r4` and `--driver r5`: four must-pass and 19 must-fail templates. There are no structural findings in this suite. The target source hash matched at load, at the end of both suites, and again when this report was written. This is a structural subset of dispatch 0553; the parent combines it with the other review lanes.

The eight positive executions pass with no failing check. Each of the 38 negative executions fails at the intended structural or content check; no exception or unrelated baseline defect is counted as a successful rejection. The paired-collision case is particularly useful: both sides contain the same duplicate body directory, so INVENTORY alone passes; STAGE_SET correctly refuses the ambiguous names. An empty extra stage likewise fails STAGE_SET despite contributing no extra file.

## Cases and attribution

The following table applies identically to r4 and r5.

| Case | Expected | Failing check(s), both drivers | Specific distinction / scope |
|---|---|---|---|
| P01_tiny_full_saved_tree | PASS | none | Independent scratch fixture; no old checker tree copied. |
| P02_result_object_key_order | PASS | none | Whole result object order varies; old order case was a stage JSON. |
| P03_result_ended_clock | PASS | none | Full result comparator must retain the declared ended-time mask. |
| P04_equal_nested_input_extension | PASS | none | Equal additional input filename and nested contents on both sides. |
| F01_collision_earlier_partial_body | FAIL | STAGE_SET, INVENTORY | Partial extra body before legitimate body; not a copied whole-stage test. |
| F02_collision_later_partial_body | FAIL | STAGE_SET, INVENTORY | Partial extra body after legitimate body, testing the opposite winner order. |
| F03_collision_both_sides_equal | FAIL | STAGE_SET | Both sides contain identical collisions: ambiguous inventory must still refuse. |
| F04_collision_middle_of_three | FAIL | STAGE_SET, INVENTORY | Tampered middle alias between equal outer aliases; four total body directories. |
| F05_empty_extra_stage | FAIL | STAGE_SET | An extra empty stage has no files for a file-only inventory to detect. |
| F06_missing_body_stage | FAIL | STAGE_SET, INVENTORY | A complete required compared stage disappears. |
| F07_renamed_stage_suffix | FAIL | STAGE_SET, INVENTORY | Unknown stage suffix preserves files but changes semantic directory name. |
| F08_body_nested_payload | FAIL | STAGES | Nested scientific body payload differs. |
| F09_result_unknown_nested_ulp | FAIL | RESULT | Previously unlisted result subtree numeric leaf differs by one ULP. |
| F10_result_unknown_nested_key_removed | FAIL | RESULT | Unknown nested result-key presence, distinct from old scalar substitutions. |
| F11_result_unknown_nested_key_added | FAIL | RESULT | Additional nested scientific result constraint. |
| F12_input_nested_contract | FAIL | FILES_INPUTS | Nested contract string in independently named input. |
| F13_input_binary_last_byte | FAIL | FILES_INPUTS | Non-JSON input binary bytes; old input probes were JSON. |
| F14_input_binary_missing | FAIL | INVENTORY | Missing non-JSON source input. |
| F15_input_extra_admission | FAIL | INVENTORY | One-side extra admission input; category control, not claimed novel category. |
| F16_finish_nested_residual | FAIL | FILES_TOP | Nested completion measure while status/hash/path remain well formed. |
| F17_finish_failed_status | FAIL | FILES_TOP | Contradictory final status with the same completed result. |
| F18_attempt_nested_entropy_ulp | FAIL | FILES_ROUTE_A | One-ULP attempt scientific scalar; independent field and tree. |
| F19_attempt_subrecord_missing | FAIL | FILES_ROUTE_A | Route-A attempt result subrecord removed rather than value changed. |

## Independence and limitations

The fixture factory was written before c2v005 landed. It creates fresh small saved-output trees from scratch: encoded route-A identity, checkpoint record/blob, NPZ array, attempt result, reference/body stages, top-level start/result/finish, and JSON/binary inputs. No prior checker fixture, mutation helper, or real run was copied. The old c2v004 checker source was read only to identify overlaps. The table explicitly distinguishes new boundary shapes and broad category controls; baseline, masked-clock, and extra-input categories are not claimed as novel categories. The target's selftest directory contained no checker source when this review ran, so comparison with an unpublished c2v005 checker set is UNTESTED.

These tests exercise plain tail-OFF `Z2_OFF` to isolate structural/content behavior. Tail flags, Z2 replace-mode custody, strict numeric types and symlinks belong to the other assigned review lanes. No claim is made here about their coverage. No actual r4 or r5 scientific identity pair was read or compared. All `runs_ext/UVT_*` files and receipts remained forbidden to this helper. Scientific identity comparisons and production launch/seal admission remain UNTESTED here.

The earlier single c2v004 baseline under the preparation directory was only a fixture-writer sanity check and is not counted among these 46 c2v005 executions. Preparatory artifacts are retained. No reviewed source was edited.

## Execution hygiene

Required isolated Python, bytecode disabled, single-thread BLAS, standard library and numpy. Candidate main was called in-process over synthetic saved files; no subprocess or scientific launch was attempted. Audit hooks recorded zero blocked process/network/mutation attempts. All outputs were exclusive-created in this directory. No deletion, move, rename, overwrite, network access, C5H read, NGC3198 observed/target velocity read, or Codex session-log read occurred.

## Byte pins

| File | SHA256 from bytes |
|---|---|
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/run_identity_compare_c2v005.py | `6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/run_20261018T151802_90972/STRUCTURAL_RESULTS.json | `fb7e0baa367ab8a6f68afae408bb59f21aebc128b7a8e5c903773535382948bc` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/run_20261018T151802_90973/STRUCTURAL_RESULTS.json | `6cec3c76ccab462f0197e9a2fd5531e33eb512b2b2250c1ff9b03c77b4f4ccac` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/run_structural_canaries_cx2v002.py | `7d924e33374183dd1935cf31c93cb154ca444cce9965feced2956b943046ad7e` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/structural/common_structural_cx2v003.py | `db5d7dabecb5306d834eaf07ccf6881f4152a9c147fa107ad53ede5b2aff576e` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v004/check/scripts/canaries_c2v004_cl001.py | `9ff721e0b6b422fbcad8a5d906c67705959397d4571b755eecb210ffc8690610` |
