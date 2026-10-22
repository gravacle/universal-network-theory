# Seal tool 4 B7 inputs (V006 A113 P6): key map, NEW-item dispositions, raw successor-custody spec

From: Claude4 helper (dispatch 0650, root entry A113 in V006). Folder: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/`. Written 2026-10-19T04:02:58Z (`date -u`).

**Labels.** TESTED = run on bytes here. FORMAL = read from source. UNTESTED = neither.

**Hygiene.**
- No NGC3198 target or velocity data, no C5H run, no `runs_ext` path and no `UVT_*` run output was opened, listed or stat-ed.
- No driver was invoked or imported. The driver source was read as bytes and AST only.
- No `--validity-only` was run, and nothing was launched.
- Every Python step ran under the fence `tools/fence_c4v002.py` (c993d34c) with the runner `tools/run_fenced_c4st2.py` (fe904509). Both are byte copies of `seal_tools_v004/tools/`. Each run passed the 8/8 selftest and the 15/15 exception probes.
- Writes went only to this folder. Outputs of record were written by exclusive create. Nothing was deleted or moved.

## Tool 4 flags root passes

Tool 4 is `build_seal_record_c4v004.py` 9787cf58 (TESTED sha).

| Flag | File | What tool 4 checks it against (FORMAL; call sites TESTED to occur once in tool 4) |
|---|---|---|
| `--key-equivalence-map` | `KEY_EQUIVALENCE_MAP_V007.json` | `key_map_codes(chk, obj, pt['key_equivalence_map'])`: the validated case block's map, passed through by tool 3 |
| `--new-item-list` | `NEW_ITEM_DISPOSITIONS_V007.json` if root's `slots.compare_reviewed_source` is **r13** (f5adfd11); `NEW_ITEM_DISPOSITIONS_V007_R14_VARIANT.json` if it is **r14** (f3f9ba7e, A114) | `new_items_codes(chk, obj, slots['compare_reviewed_source']['sha256'])` |
| `--successor-custody` | root's `RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json`, produced as `CUSTODY_SPEC_FOR_ROOT_V001.md` says | `custody_codes(chk, obj, slots['driver']['sha256'])`; the driver slot is r5 b5cc62af (prereg r6 candidate, TESTED) |

**Do not pass the NEW-item file yet.** It holds 17 of the 19 C-08 ids. NEW-30 and NEW-44 wait for root's ruling (section 2). Tool 4 does not compare the list with the C-08 table (TESTED: the 17-item file passes `new_items_codes` with no failure). Only the file's own note, and this README, say that it is incomplete.

## 1. `KEY_EQUIVALENCE_MAP_V007.json`: RI-30 (A113)

- The content is `{"schema": "UNT_V007_SEAL_KEY_EQUIVALENCE_MAP_C4V002", "key_equivalence_map": [], "note": ...}`. The schema was read from tool 4's source by AST.
- TESTED from bytes: the case block of record `CASE_BLOCK_V007_C4V001.json` (76309ae3), parsed strictly, carries the top-level key `key_equivalence_map` = `[]`.
- That top-level key is where it is read:
  - r13 `validate_case_block` L1557 reads `cb.get('key_equivalence_map', [])`; r14 has the same line at L1557 (TESTED);
  - tool 3 v003 L482 reads it and passes it to tool 4 as `pt['key_equivalence_map']`.
- Prereg r6 (d28c95f5) `binding_inputs.case_block` pins exactly that path and sha (TESTED).
- Generator: `tools/make_key_map_c4v001.py`, run as a dry run and then an exclusive write.

## 2. `NEW_ITEM_DISPOSITIONS_V007.json` (and `_R14_VARIANT`): A81 RI-20, A113 P6

- **Id index.** The C-08 table of `SEAL_MANUAL_DISCLOSURES_V002.json` (a0284ece): 19 ids. Root's V003_DRAFT (21968a07) has the same ids in the same order, on r14 (TESTED).
- **compare_impl.**
  - r13 file: `v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md` (274f7049). It names f5adfd11 in full (TESTED).
  - R14 variant: `v007_compare_c2/r14/COMPARE_V007_IMPL_R14_CX1V002.md` (2ba6d12e). It names f3f9ba7e in full (TESTED) and declares no NEW item. r14 is `SELECTED_BUILD_FOR_CLAUDE3_CLAUDE4_REVIEW`; its reviews are pending.
- **Sources.** Every IMPL was opened by name: V001, r1-r8 and r10-r14 (r9 has none). The closed V005 addendum was read from the prereg r6 byte copy (c01b3c51). Each reason quotes the round, the IMPL file, its section, its sha256 from bytes and the line. Every quote is re-located in the bytes at generation time.
- **MUST_FAIL tests.** Every test name resolves to tests that PASS in the run of record of the variant's compare:
  - r13: `r13/out/author_cx3v001/TEST_SUMMARY.json` cad67c41, 706/706, `script_sha256` f5adfd11;
  - r14: `r14/out/author_v002/TEST_SUMMARY.json` 42c4961f, 718/718.
- **Generator.** `tools/make_new_items_c4v001.py`. All evidence is in its table. It refuses on any quote, sha or test that does not verify.

| Id | Introduced (IMPL, line) | Disposition | Basis | Disposition evidence | MUST_FAIL tests (IMPL names verbatim; a run-tag name where the IMPL prints none) |
|---|---|---|---|---|---|
| NEW-4 | r2 L84 | ADOPTED | RI-10 on the IMPL "stricter" declaration | r2 L79, r3 L88, r10 L62 | `R3_ORDER_N8_*`, `R4_VALIDITY_F1_D5_NODES_SERIAL_WORKER_ON_PARALLEL8_INVALID` |
| NEW-7 | r3 L109 | ADOPTED | stated in an IMPL | r5 L38, V005 L251 | `C3_B1_H2_NEW7`, `C3_H1_N7`, `A51_F2_NON_CONTRACTING_RATIO_2_E_UNAVAILABLE_A53_NEW7`, `…_INFINITE_E_UNAVAILABLE_A53_NEW7` |
| NEW-13 | r4 L81 | ADOPTED | stated in an IMPL | r5 L39, r7 L156, V005 L249 | `R4_VALIDITY_F1_*`, `A53_NEW13`, `A53_NEW13_NODES_RO1_WORKERS_ON_THE_CUSTODY_LIST_FROM_BYTES` |
| NEW-16 | r4 L97 | ADOPTED | stated in an IMPL | r4 L73, r5 L36, V005 L242 | `R4_ORDER_Nc_*`, `C3_R3_P11`, `A53_ROUTE_A_BRANCH_UNCHANGED` |
| NEW-17 | r4 L98 | ADOPTED | stated in an IMPL | r5 L37, r6 L72, V005 L248 | `A53_NEW17_DECIDABILITY_UNKNOWN…`, `A53_NEW17_CLI_REFUSAL_RC2_NO_OUTDIR` |
| NEW-19 | r4 L92 | ADOPTED | stated in an IMPL | r4 L45, r5 L39, V005 L250 | `R4_A52_5_*`, `A53_NEW19` |
| NEW-21 | r5 L105 | ADOPTED | stated in an IMPL | r5 L98, r6 L68, V005 L461 | `C3_S5_H1_F2`, `D1_I1T_FAIL_VERDICT_WITH_A_FAILING_BUILD_CASES_INCOMPLETE_A54_S5`, `…_RECORD_DEFECT_NO_RUN_A54_S5`, `…_EPS_DATA_AND_VERDICT_AGREE_A54_S5` |
| NEW-31 | r6 L105 | ADOPTED | stated in an IMPL | r6 L50, r8 L72, V005 L654 | `R6_ORDER_N2_…`, `R8_A67_NEW31_…` |
| NEW-34 | r6 L111 | ADOPTED | RI-10 on the IMPL "stricter" declaration | r6 L113, r6 L114, r7 L86 | `S9_UNIT…`, `R10_C3_R7_A_N1_*`, `R7_ORDER_B1_UNIT_PRESENT_NON_LIST_ROW_SET_IS_S9_ABSENT_NULL_EMPTY_ARE_THE_B4_GAP` |
| NEW-39 | r6 L123 | ADOPTED | root-ruled item, implemented | r7 L75, V005 L378 | `A62_3_V010_R5_CHECK_PIN_PENDING_AND_R5_CUSTODY_PINS_VERIFIED_FROM_BYTES`, `A54_A62_3_SEALED_MODE_WITH_A55_SET_STILL_REFUSES_WITHOUT_THE_V010_R5_CHECK`, `R7_A62_3_PINS_ARE_THE_R5_CASCADE_IMAGES_OF_THE_R4_SHAS_BINDING_UNCHANGED` |
| NEW-52 | r8 L117 | ADOPTED | stated in an IMPL | r8 L118, r10 L57, r10 L154, V005 L1483 | `R10_NEW52_*` |
| NEW-53 | r8 L122 | ADOPTED | RI-10 on the IMPL "stricter" declaration | r8 L124, r8 L106, V005 L653 | `R8_A67_N4_EPS_TOP_LEVEL_ENVELOPE_MAX_DISAGREES_RECORD_DEFECT_NO_RUN`, `R8_A67_N4_EPS_TOP_LEVEL_FLAG_WITHOUT_ENVELOPE_BOUND_RECORD_DEFECT_NO_RUN` |
| NEW-54 | r8 L125 | ADOPTED | RI-10 on the IMPL "stricter" declaration | V005 L651 | `R8_A67_N2_SR_K_TWO_OF_THREE_DELTAS_IDENTICAL_RECORD_DEFECT_NO_RUN` |
| NEW-60 | r8 L144 | ADOPTED | root-ruled item, implemented | r10 L48, r10 L49, r10 L51, V005 L751 | `R10_A68_CHK1_*`, `R10_A68_RECORDS_*`, `R10_A69_1_*`, `R10_A69_3_*` |
| NEW-64 | r10 L178 | ADOPTED | stated in an IMPL | r10 L179, r11 L117, V005 L1410 | `R10_H07_*` |
| NEW-71 | r11 L105 | ADOPTED | stated in an IMPL | V005 L1264 | `…_EXTRA_ROSTER_OFF_THE_MAP_…`, `…_WRONG_FIXED_GEOMETRY_ONLY_*` |
| NEW-73 | r11 L107 | ADOPTED | stated in an IMPL | r12 L25, r13 L5, V005 L1264 | `R11_R10_RECHECK_VALIDITY_N2_…` |
| NEW-30 | r6 L54 | **not written: root must rule** | none: RI-10 does not decide it (reporting only: neither stricter nor looser) | r6 L54, r10 L213 | (if ADOPTED) `R6_VALIDITY_F2_NO_RUN_STILL_REPORTS_THE_FAILING_EPS_AND_T2I_GATES_WITH_NEXT_STEPS` |
| NEW-44 | r7 L116 | **not written: root must rule** | none: it is a question for root (RB_FP is or is not an envelope consumer); a yes would change RB_FP's epsilon (1.277x larger on V006) and so could change a physics reading; no IMPL or addendum entry records a ruling | r7 L93 | (if ADOPTED) `R7_SF3_NEW44_RB_FP_ON_THE_ENVELOPE_EPS_CROSSREF_MISMATCH_PINNED` |

**Basis kinds.**
- **stated in an IMPL**: an IMPL records the item as adopted, accepted, confirmed or implemented as root ruled. The rulings are A53, A58 RI-10, A67, A79, A75.7 and A86.5.
- **RI-10 on the IMPL "stricter" declaration**: no IMPL writes "adopted". The originating IMPL declares the item stricter. A58 RI-10, made general by A81 RI-20, adopts as text an item that is stricter and fills a gap. Root's `c08_confirmation` says the dispositions "follow A58 RI-10 / A81 RI-20 as declared in their originating rounds' IMPLs".
- **root-ruled item, implemented**: not a proposal. The originating IMPL says it carries out root rulings (A56 follow-up 3; A68/A69), and a later IMPL records the implementation.

**NEW-30 and NEW-44 are not written: root must rule.**
- **NEW-30** (r6 L54): "Reporting only; the reading is unchanged. ... Root to confirm (NEW-30)." It is still open at r10 L213. RI-10 does not decide a reporting-only item. Under A115 it cannot change a reading.
- **NEW-44** (r7 L116, L93): "Is RB_FP an envelope consumer? R7 keeps EPS `eps_max` ... Root to rule (NEW-44)." Today r13 and r14 read eps_max, and the pin `R7_SF3_NEW44_..._CROSSREF_MISMATCH_PINNED` is in place. A "yes" would change RB_FP's epsilon (1.277x on V006) and would need a compare change.
- No V005 or V006 entry names either id (TESTED by id search of both addenda).

After root rules, complete the list (it is checked against all 19 ids):

```sh
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3; C4=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4
T=$(date -u +%Y-%m-%dT%H:%M:%SZ); V=r13   # or r14, matching slots.compare_reviewed_source
$PY -I -B $C4/tools/make_new_items_c4v001.py --variant $V --utc "$T" --root-ruling NEW-30=ADOPTED --root-ruling NEW-44=ADOPTED \
  --root-ruling-ref "V006 A1xx (sha256 ...): <root's words>" --require-complete --dry-run && \
$PY -I -B $C4/tools/make_new_items_c4v001.py --variant $V --utc "$T" --root-ruling NEW-30=ADOPTED --root-ruling NEW-44=ADOPTED \
  --root-ruling-ref "V006 A1xx (sha256 ...): <root's words>" --require-complete --write <ROOT_OUT>/NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json
```

REJECTED is also accepted. A REJECTED item names no test. The completion path was TESTED as a dry run with a synthetic reference string, and wrote nothing. `--require-complete` without the rulings refuses `INCOMPLETE` with exit code 2 (TESTED).

## 3. Raw successor custody: `CUSTODY_SPEC_FOR_ROOT_V001.md` and `tools/make_custody_record_c4v001.py`

- **The spec.**
  - The identity comparator of record is c2v007r2 (052da0fe, prereg r6 slot). It computes `SCRIPT_CUSTODY` (A59 raw) and `NEW_DRIVER_PIN` (FORMAL).
  - The Z2 record of record is R5_V001 `B1_R5_C2V007.json` (83e7b067). It names the Z2 run `runs_ext/UVT_Z2_A2F10_R5_RUN_V001` (path only) and its report of record `out/IDENTITY_C2V007_R5_V001/Z2.json` (ac793faf, from the record; not opened here).
  - It gives the exact commands for Option A (recommended: convert the report of record; no run is touched) and Option B (re-run c2v007r2). A re-run lists `runs_ext` to read the C5H directory's inode, which conflicts with root's A105_E_OPS5 disclosure.
  - It states what the output must show, and how the record maps one-to-one to tool 4's form.
- **The converter** writes the record by exclusive create. It refuses (exit 2, nothing written) when:
  - a stage lacks its custody row or its successor;
  - the run is not Z2;
  - the driver is not the slot;
  - the comparator is not c2v007r2;
  - the comparison is not PASS;
  - a re-run differs from the report of record;
  - any input is malformed.

  It reads the driver tables as AST, never executing driver code. Its AST reading equals an independent regex extraction on the real r5 bytes (TESTED).
- **Synthetic tests only.** `TEST_CUSTODY_CONVERTER_SYNTHETIC_C4V002.json`: 31 of 31 cases, 2 PASS and 29 must-fail. The CLI was also run through the fence runner (`fixtures/custody_cli_v002/`): a dry run and a write with the same sha, and an r4 refusal. v001 (`..._C4V001.json`) is superseded: a harness regex missed one commented driver line, so its cross-check read false. It is kept.

## 4. Validation with tool 4's own functions (TESTED)

`VALIDATION_TOOL4_B7_C4V001.json`: 12 of 12 calls as expected.

| Function | Input | Codes |
|---|---|---|
| `key_map_codes` | file 1, against the case block map `[]` | none |
| `key_map_codes` | must-fail: an extra entry | `KEY_MAP_NOT_THE_CASE_BLOCK_MAP` |
| `key_map_codes` | must-fail: wrong schema | `KEY_MAP_SCHEMA` |
| `new_items_codes` | r13 file, against f5adfd11 | none |
| `new_items_codes` | R14 variant, against f3f9ba7e | none |
| `new_items_codes` | must-fail: r13 file against the r14 sha | `NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE` |
| `new_items_codes` | must-fail: an ADOPTED item with no test | `NEW_ITEMS_ADOPTED_WITHOUT_MUST_FAIL` |
| `new_items_codes` | must-fail: a duplicate id | `NEW_ITEMS_DUPLICATE_ID` |
| `custody_codes` | the converter's synthetic output, against b5cc62af | none |
| `custody_codes` | must-fail: r4 sha | `CUSTODY_DRIVER_NOT_THE_SLOT` |
| `custody_codes` | must-fail: stages_successor = total - 1 | `CUSTODY_STAGES` |
| `custody_codes` | must-fail: identity_run Z2_OFF_RO1 | `CUSTODY_RUN` |

## Files

| File | What it is |
|---|---|
| `KEY_EQUIVALENCE_MAP_V007.json` | B7 input 1 (of record) |
| `NEW_ITEM_DISPOSITIONS_V007.json` | B7 input 2 for an r13 compare slot (17 of 19; incomplete until root rules) |
| `NEW_ITEM_DISPOSITIONS_V007_R14_VARIANT.json` | B7 input 2 for an r14 compare slot (the same 17 items; compare_impl is the r14 IMPL CX1V002) |
| `CUSTODY_SPEC_FOR_ROOT_V001.md` | B7 input 3: what root runs |
| `tools/make_custody_record_c4v001.py` | the converter root runs |
| `tools/make_key_map_c4v001.py`, `tools/make_new_items_c4v001.py` | generators of inputs 1 and 2 |
| `tools/validate_b7_with_tool4_c4v001.py`, `VALIDATION_TOOL4_B7_C4V001.json` | the tool-4 validation and its results |
| `tools/test_custody_converter_c4v002.py`, `TEST_CUSTODY_CONVERTER_SYNTHETIC_C4V002.json`, `fixtures/` | synthetic converter tests (v001 kept, superseded) |
| `tools/map_impl_tests_to_r13_run_c4v001.py`, `tools/impl_tests_in_r13_run_c4v001.out.json` | IMPL test names against the r13 run of record |
| `tools/extract_suite_tags_c4v001.py`, `tools/suite_tags_r13_c4v001.out.json` | first AST pass over the r13 suite (`check()` calls only; superseded by the run-of-record map) |
| `tools/inspect_prereg_r6_c4v001.py`, `tools/print_addendum_entries_c4v001.py`, `tools/grep_ids_in_file_c4v001.py` | read-only inspection helpers |
| `tools/fence_c4v002.py`, `tools/run_fenced_c4st2.py` | the fence and runner (byte copies) |
| `PARTIAL.md` | progress log |
| `HASHES_SEAL_B7_INPUTS_C4V001.txt` | sha256 of every file here, written last |
