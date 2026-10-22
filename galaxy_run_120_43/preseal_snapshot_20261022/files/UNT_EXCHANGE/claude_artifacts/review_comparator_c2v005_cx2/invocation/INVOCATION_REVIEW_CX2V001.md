# Invocation and value review of c2v005

`date -u`: Sun Oct 18 15:20:32 UTC 2026.

Verdict for this focused lane: PASS. TESTED 48/48 full-main comparator invocations: 24 with --driver r4 and the same 24 with --driver r5. Six must-pass and eighteen must-fail cases per driver. Both driver selections preserved the tested comparator SHA256 before and after execution. No source edits to the comparator. This is not an overall comparator review or a scientific run-pair verdict.

Every tree is a newly constructed local synthetic fixture. Source v003 executes no imported checker builder and copies no run fixture. Changes occur in memory before exclusive creation. The audit hook recorded zero subprocess/network attempts. No scientific launches or real-run reads; all runs_ext/UVT paths remained forbidden.

The two old c2v004 false-PASS controls are closed here. Repeating an otherwise valid in-run --uv-tail-config now fails REQUEST. With the Z2 declared token set still valid replace mode, NEW running the same base reference script as REF fails SCRIPT_CUSTODY and REQUEST; TOKENS_POLICY remains PASS, so that negative does not depend on malformed tokens.

The fixture successor adapts the API (--driver required), result driver pins, complete required tail blocks, manifest request/record, immediate-after-route-A manifest ordering, exact extra route-A dependency pins, and source-derived replace tokens for all UVT kinds. The intermediate v002 positive failed RA_PINSET because the fixture omitted four required dependency pins; v003 adds those actual pinned dependencies. That intermediate failure is a corrected test-fixture deficiency, not a comparator finding. Old source and outputs remain immutable.

Coverage: ordinary argv value swap/duplication; joined and missing-value tail options; duplicate valid tail options; wrong-stage flags; raw script/hash custody; nested request signed-zero/int-float/bool-int; matching signed-zero and mixed-type positive controls; complex NPZ imaginary signed zero; NPZ integer/float dtype; NPZ C/F logical-content positive; dangling/file/directory symlinks; exact contiguous route-B tail-block insertion; reference-side tail flags; and outside-run manifest arguments.

Differences from previous checker sets: request numeric_contract matrices replace their stage-finish/result/checkpoint numeric locations; complex imaginary signed zero and explicit int32/float32 NPZ dtypes replace real-ULP and JSON scalar changes; C/F logical content is a new positive; the duplicate-option canary repeats an identical valid path instead of the old first-outside/last-inside pattern; and the raw base-on-NEW test preserves valid replace-mode tokens and demands SCRIPT_CUSTODY failure. Symlink cases are built locally from scratch. These test some of the same required failure families with different concrete inputs. No c2v005 checker source had landed by the source-list check at 15:19:29 UTC (only comparator and token builder); comparison against that future checker set is UNTESTED/pending. The token builder was read, not executed, and the test tokens were constructed independently from driver constants.

UNTESTED: actual r4/r5 scientific identity pairs, Z2_OFF_RO1 scientific outputs, production-size cost, and any global acceptance claim outside these invocation/value canaries. The root lane and other helpers own broader source/structure review.

Per selection:

- r4: 24/24; elapsed 4.008 s; maximum RSS 86622208 bytes.
- r5: 24/24; elapsed 4.449 s; maximum RSS 86032384 bytes.

Cases (same expected/actual outcome under r4 and r5):

| Case | Expected | Actual |
|---|---|---|
| P00_distinct_invocation_baseline | PASS | PASS_BITWISE_EQUAL |
| P01_Z2_correct_explicit_replacement | PASS | PASS_BITWISE_EQUAL |
| F02_swap_nontail_option_values | FAIL | FAIL |
| F03_duplicate_nontail_option | FAIL | FAIL |
| F04_joined_tail_assignment | FAIL | FAIL |
| F05_tail_missing_value_at_end | FAIL | FAIL |
| F06_duplicate_valid_tail_config | FAIL | FAIL |
| F07_route_A_only_flag_on_reference | FAIL | FAIL |
| F08_Z2_NEW_base_equals_REF_with_tokens | FAIL | FAIL |
| F09_NEW_base_hash_wrong | FAIL | FAIL |
| F10_request_nested_signed_zero | FAIL | FAIL |
| F11_request_nested_int_float | FAIL | FAIL |
| F12_request_nested_bool_int | FAIL | FAIL |
| P13_equal_nested_signed_zero | PASS | PASS_BITWISE_EQUAL |
| P14_equal_distinct_scalar_types | PASS | PASS_BITWISE_EQUAL |
| F15_npz_imaginary_signed_zero | FAIL | FAIL |
| F16_npz_integer_float_dtype | FAIL | FAIL |
| P17_npz_C_F_logical_identity | PASS | PASS_BITWISE_EQUAL |
| F18_extra_dangling_symlink | FAIL | FAIL |
| F19_external_symlink_different_payload | FAIL | FAIL |
| F20_extra_stage_directory_symlink | FAIL | FAIL |
| P21_exact_tail_block_prefix_insertion | PASS | PASS_BITWISE_EQUAL |
| F22_tail_flag_on_reference_side | FAIL | FAIL |
| F23_manifest_outside_run | FAIL | FAIL |

Cited files, SHA256 from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py` — `711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/c2v005_r4_canaries_v001/RESULT.json` — `21809faec02fc08f2b0972a2c98e2c3e0c01b9f9a8b3a03d7546f2709508fc79`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/c2v005_r5_canaries_v001/RESULT.json` — `742994b147b03e0c3139ab2537e8fdb30f63ab9c88143576cb102044ac06be3b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/run_identity_compare_c2v005.py` — `6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/tools/make_tokens_c2v005.py` — `5891360c391dff5899ed15a89a07bba7813bc31cb2033e71eac4464be4900c94`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/PREPARATION_CX2V001.json` — `93fbffaf693745ad686a31edf81dd8c354207950f9a279bb99f205da035a620b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/c2v004_canary_preflight_v001/RESULT.json` — `662cee97e1b0856f62798118cd223c39bf437734d35378dbddea604c4391fcb3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/c2v005_r4_baseline_v001/RESULT.json` — `2e5136c8fc3274525648a556b3462739492b21f2d908dd3fdc6b9b7396e66e5b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v004/check/scripts/canaries_c2v004_cl001.py` — `9ff721e0b6b422fbcad8a5d906c67705959397d4571b755eecb210ffc8690610`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v004/tools/selftest_identity_compare_c2v004.py` — `e24925c5327eaebef673e014d3efe6b0c1bf5b5b9c9b0f0246c6de7dfcaa1b67`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v003/tools/selftest_identity_compare_c2v003.py` — `a99e3e4d119d1cfd142a0f2d2db1a202ea53088d4d9c5e32d96094949adc2b26`
