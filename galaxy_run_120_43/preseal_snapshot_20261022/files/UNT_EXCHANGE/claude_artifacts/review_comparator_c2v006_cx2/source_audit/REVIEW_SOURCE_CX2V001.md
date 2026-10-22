# c2v006 independent A71 and Store audit — FAIL

`date -u`: Sun Oct 18 16:20:00 UTC 2026

**FAIL: three TESTED blocking classes remain, plus one A71 should-fix.** All 13 whole-gate executions used fresh synthetic B0P/r5 trees and the unchanged target bytes. Seven negative executions unexpectedly returned PASS_BITWISE_EQUAL with every check passing. Three positive baselines passed; ordinary array, result and ledger changes failed solely on STAGES, RESULT and ATTEMPT_LEDGER respectively. The 18 unit observations confirm mechanisms and cache/hash behavior; finding observations are not correctness passes.

1. **Duplicate NPY header keys (B1).** `_npy_header` calls ast.literal_eval before checking the header. Duplicate descr, shape or fortran_order keys collapse to the final entry. Standalone NPY and NPY-inside-NPZ whole-gate controls pass, including unequal and equal duplicates; STRICT_PARSE and NO_LAST_WINS remain true. Guard the header AST before any mapping is built.

2. **Joined token-label alias (B2).** Distinct pairs receive the same final token: one literal label `<X>|<Y>` versus two labels `<X>` and `<Y>` joined with `|`. The original label-to-pair check misses the collision after joining. REF scientific_probe=cx2_left0 and NEW scientific_probe=cx2_right1 compare equal under these distinct pairs; all checks pass. Without tokens, the same value change fails RESULT. Validate injectivity after construction or use structured/opaque identifiers. This is separate from the A73 requirement to admit only driver-derived triples.

3. **Attempt-ledger alias (B3).** ATTEMPT_RE ends in `$`, which matches before a terminal newline. `cx2token.start.json` and `cx2token.start.json\n` map to the same captured directory/token/kind. The latter silently overwrites the former, and both raw paths have already been popped from inventory. A tampered value 900 in the ordinary NEW file is hidden by value 1 in the newline file; REF contains only ordinary value 1. ATTEMPT_LEDGER, INVENTORY, NO_LAST_WINS and COVERAGE all pass. Use fullmatch/absolute end and an explicit grouping-key duplicate guard before removing any raw file.

4. **Repeated equal token triples (S1).** Identical declared triples silently collapse in set accumulators. The whole gate passes with NO_LAST_WINS true. A71 requires duplicate rejection even when values agree. This unused-duplicate control is a strictness violation, not by itself a changed scientific-value demonstration.

Independent conversion inventory: **139 candidate sites**, plus all **199 dict literals** checked for duplicate constant keys (none found). The inventory was generated from the complete AST, not the BUILD list. It includes dict comprehensions/constructors, dynamic/unpack literals, set comprehensions, setdefault/update/literal_eval and all subscript assignments; fixed report/state/list-index operations are deliberately overincluded. Every site has its source location, enclosing scope and assessment.

Guarded paths reviewed: strict JSON object pairs; NPZ central-directory/member names and logical keys; driver AST dict keys; stage directory names/numbers and canonical inventory keys; normalized object and pin keys; stage_records; argv multimaps. Injective fixed-prefix inventory projections and dictionary copies preserve keys. Pinned checkpoint decode rejects repeated list-of-pairs keys. The missing header guard, token aggregation/final join and attempt-ledger grouping are identified separately. This is a finite source audit, not a formal completeness proof.

Store checks: JSON duplicates are rejected, NPY/NPZ array objects are cached, their recorded SHA is from the parsed bytes, stable rehashes pass, synthetic changed end hashes fail verification, and intermediate hash changes are retained in unstable. End-hash fault injection changed an in-memory function temporarily and restored it; no file was overwritten. Source review confirms module/driver exec uses the verified byte buffer. JSONL/raw/scan paths can read again: their digests are recorded against the first digest; the literal blanket claim “every file read once” should be understood with that implementation qualification. No new consistency bypass was found in this bounded Store slice.

Hygiene: audit guards installed before target/helper imports; isolated prescribed Python -I -B, NumPy/stdlib, one-thread environment, default priority under 0514 waiver. Source and synthetic fixtures only. No production runs, UVT/C5H reports/receipts, NGC targets, network, solver, scientific launch, logs, deletion, move, rename or overwrite. The existing own fixture writer was imported from pinned bytes; no supplied c2v006 checker was imported or run. Scientific identity and production incidence are UNTESTED. A73 SF1/SF2/SF3/N3/N6 are owned by the parallel review lane.

Whole-gate owner checks:

| Case | Expected owner | Actual verdict | Actual failing checks |
|---|---|---|---|
| P00_plain_synthetic_baseline | positive control | PASS_BITWISE_EQUAL | none |
| F01_npy_duplicate_descr | STRICT_PARSE | PASS_BITWISE_EQUAL | none |
| F02_npz_member_duplicate_shape | STRICT_PARSE | PASS_BITWISE_EQUAL | none |
| F03_npy_duplicate_equal_fortran | STRICT_PARSE | PASS_BITWISE_EQUAL | none |
| C04_ordinary_array_change | STAGES | FAIL | STAGES |
| F05_duplicate_exact_declared_token | NO_LAST_WINS | PASS_BITWISE_EQUAL | none |
| F06_joined_label_alias_changes_result | NORM_INJECTIVE | PASS_BITWISE_EQUAL | none |
| C07_same_result_change_without_tokens | RESULT | FAIL | RESULT |
| P08_one_honest_declared_pair | positive control | PASS_BITWISE_EQUAL | none |
| P00_ledger_equal | positive control | PASS_BITWISE_EQUAL | none |
| C01_ledger_ordinary_change | ATTEMPT_LEDGER | FAIL | ATTEMPT_LEDGER |
| F02_ledger_newline_alias_hides_change | NO_LAST_WINS / ATTEMPT_LEDGER / INVENTORY | PASS_BITWISE_EQUAL | none |
| F03_equal_duplicate_ledger_alias | NO_LAST_WINS / ATTEMPT_LEDGER / INVENTORY | PASS_BITWISE_EQUAL | none |

Every cited source and evidence file, SHA256 from bytes:

| File | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py` | `097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/BUILD.md` | `fedbc6157037e2e1c847e7211b9ed9519193c99185bc4ce2362783384bb647d1` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/DIFF_c2v005_c2v006.diff` | `ded144d333a50eaa0f0d45a36850f104227ed348a5db1abcff46c6658bd6621b` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md` | `c4d4ded6ee239836099162facd68b8a2944423ef76c320f24a4b474363aa5923` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0564_2026-10-18_codex2_crosslineage_review_comparator_c2v006.md` | `332ed9d11fc069b772673b50d07b5db678d11fb68cad13a152ea470c5173103d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py` | `069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py` | `711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probe_a71_store_cx2v001.py` | `4aa88cc4c4e3866e777c8ab5afc69d599daf5e1934df0f766df798b6f7fbd610` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probe_ledger_alias_cx2v001.py` | `e085d5cb4cd78312d7f872edcec044787994f9d2f6accac748d8069ef8815e14` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/RESULTS_CX2V001.json` | `39b218bb9296be1a6181688151f302a98bd499eff842947c79aa073c9e2f232a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/ledger_v001/RESULTS_LEDGER_CX2V001.json` | `203f85346f9a86c5ea39df03392a3d38eaa1ea009c5f510d6f3245cf12f11c18` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/seal_source_audit_cx2v001.py` | `0d14573023c07278b39c9731d54bd11b84ec07a5c53efed4f562a89578fbd192` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/P00_plain_synthetic_baseline/REPORT.json` | `37dce11c4791283cf9883a20db2c7a61324aab884ec291635713b5bc2679f802` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/F01_npy_duplicate_descr/REPORT.json` | `8a9d06f1728cae344f550c7591be33f8983680213deae3430d5a6ed72fc3eca6` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/F02_npz_member_duplicate_shape/REPORT.json` | `059d507e97314e383d85a4b17cabd37cc2ab66b96ff71b4305176cc203dd15ef` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/F03_npy_duplicate_equal_fortran/REPORT.json` | `f9c8ff3e9fc07184bb24269a3746793089429a0f1d74242397210d3e6da24012` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/C04_ordinary_array_change/REPORT.json` | `7b59cb1c09d3f675150eba4a5dca2db2e22633f19ce72ba1f3e14442d58b2a64` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/F05_duplicate_exact_declared_token/REPORT.json` | `f61dfae86281265dee21de57b018345cba2353fc7084df518f39d58726329c8c` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/F06_joined_label_alias_changes_result/REPORT.json` | `fdcb9aef7d44f7ee22c13f5203c729be3ffa3e4d60e0f8d46c9968a6a677612d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/C07_same_result_change_without_tokens/REPORT.json` | `ae9dff0f48c2194eea543c3bdc3594e7fe939010792173ba173b01689512ac8d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/probes_v001/P08_one_honest_declared_pair/REPORT.json` | `ef67ab06de02535c79c6fd9c1f1cc06723122fe6c8d4dcfee044b902b98fe0ca` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/ledger_v001/P00_ledger_equal/REPORT.json` | `8fa40daae3e626e97dbd49ea282b7411526808eb5ac5fbef7870069c05d10899` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/ledger_v001/C01_ledger_ordinary_change/REPORT.json` | `28f2a21f0a8997cc3881c6b01040158fce7e1829365f3c583b5447e7cf967930` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/ledger_v001/F02_ledger_newline_alias_hides_change/REPORT.json` | `8f4bc15ccb94ac303ae219e7b58db12348580655945ea1c803abd57830c79bbb` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/ledger_v001/F03_equal_duplicate_ledger_alias/REPORT.json` | `41cb169f67d2b7a0553d368dbacea02db39e00508506170881e1c4bdb277a40c` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/CONVERSION_INVENTORY_CX2V001.json` | `678980881cc452d2d67a618edbdb033495dd6e7f07950acb106a08e6c8ec7239` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_comparator_c2v006_cx2/source_audit/FINDINGS_SOURCE_CX2V001.json` | `d7e6ef0b787de58597bc19a50d7036408c28ca0fd4b8dbda7ef344433117cc22` |

The manifest additionally hashes all small synthetic fixture files. Open V005 addendum hashes are observations of mutable bytes, not seal pins.
