# REFUTE P6: seal tool 4's three B7 inputs (dispatch 0650, V006 A113 P6)

From: Claude4 refute helper. Folder: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4_refute/`. Written 2026-10-19T04:31:57Z (`date -u`). Object under refutation: the builder's folder `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/` (HASHES 731ff01a), read-only.

**Labels.** TESTED = run on bytes here. FORMAL = read from source. UNTESTED = neither.

**Hygiene.**
- I did not open, list or stat any NGC3198 target or velocity data, the C5H run, `runs_ext` or any `UVT_*` run output. I did not open the Z2 report of record `out/IDENTITY_C2V007_R5_V001/Z2.json`.
- No driver was invoked or imported; no `--validity-only`; nothing was launched. P6 has no RI-31 stage, so no dry run was run.
- Every Python step ran under byte copies of the fence (`tools/fence_c4v002.py` c993d34c) and runner (`tools/run_fenced_c4st2.py` fe904509). Every run passed 8/8 selftests and 15/15 probes, with `blocked_after_selftest: []` (TESTED, each run's summary).
- Writes went only to this folder, by exclusive create. Nothing was deleted or moved.

**Context that changed after the build (TESTED).** V006 is now `8ac68396…` (17,598 bytes). The builder read `63e7802f`. The new entries:
- **A116/A117**: r14 (f3f9ba7e, SELECTED_R14_CX1V002 6b650ece, IMPL_R14_CX1V002 2ba6d12e) is the compare of record.
- **A118**: NEW-30 and NEW-44 are ADOPTED; Claude4 completes `NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json` on IMPL_R14_CX1V002. Custody is **Option A**, using converter **1b097cba**.

V005 in CLAUDE2 still equals the read copy c01b3c51 (TESTED).

## Verdict

**REFUTED IN PART: 1 BLOCKING.** The custody converter refuses the genuine R5_V001 Z2 report, so the Option A step that A118 adopted will stop the seal script. The key map stands, and so do the 17 written NEW-item dispositions. A118 closes NEW-30 and NEW-44. The completion path gives 19 of 19 (TESTED in memory).

## Findings

| Id | Severity | Claim | Fix |
|---|---|---|---|
| R6-B1 | **BLOCKING** (A115 (a): reachable from honest producers on the real records) | The converter `make_custody_record_c4v001.py` (1b097cba) refuses `STAGE_KIND_HAS_NO_SUCCESSOR` on the honest Z2 run. Its `classify()` (L165-187) admits only the 8 UVT kinds, route_a and the manifest. Driver r5 always plans route-B stages of 3 other kinds, and runs them on their base `SCRIPTS[kind]` with tail ON. The comparator plans exactly those base scripts for Z2 (`planned_script` L1594), so `SCRIPT_CUSTODY` passes and gives each one a row. Evidence below. | Root rules how such stages count. Then a converter successor (c4v002) implements the ruling, is re-tested on the driver-planned stage set and is reviewed before root runs Option A. The spec is revised to match. Recommended reading (A59 as verified): a closed no-successor list derived from the driver, each stage on exactly its planned `SCRIPTS[kind]`, listed in the note, with the count over the successor kinds. |
| R6-S1 | SHOULD_FIX (A115: NOTE) | `new_items_codes` never checks the item list against C-08. TESTED: an invented `NEW-999`, an **empty** list and the 17-item file all pass with no failure. This confirms and extends P6-S1. | The A118 COMPLETE file is generated with `--require-complete` (TESTED: it refuses `INCOMPLETE` without rulings). Claude3's check compares the ids with the C-08 table explicitly. |
| R6-N1 | NOTE | In the R14 variant (and so in the A118 completion), the NEW-52 entry still describes the A75.7 allow-list and cites "A79 and A88". It does not name V006 A114, which is r14's only change: `'I4'` added to `GATE_RECORD_AFTER_SEAL_ALLOWED` (r13 L341 vs r14 L341, FORMAL). It also omits r14's 12 A114 MUST checks. | In the COMPLETE file, cite A114 in NEW-52's reason, and optionally its I4 MUST tests. |
| R6-N2 | NOTE | P6-B1 is superseded by A118. TESTED in memory with the generator's own `build()`: variant r14 with NEW-30 and NEW-44 ADOPTED, citing A118 (V006 8ac68396), gives 19 items in C-08 order, and tool 4 `new_items_codes` vs f3f9ba7e reports no failure (r13 likewise). Without the rulings, `--require-complete` refuses. | Write the COMPLETE file as A118 says: `--variant r14`, dry run, then exclusive write. |
| R6-N3 | NOTE | P6-S3 is resolved: A118 chose Option A. A118's wording "the guard [would] stat the C5H directory" is loose. FORMAL (c2v007r2 L312-323): the guard stats `runs_ext` and lists it, reading the C5H entry's inode from readdir; it does not stat C5H itself. The rejection still stands. | None. |
| R6-N4 | NOTE | P6-N4 is stale: V006 moved again, to 8ac68396 (A116-A118). | None. |
| R6-N5 | NOTE | P6-N1 (the six derived dispositions) is not refuted, and further root text supports two of them. NEW-4: A53 "R3-4 ruled" (V005 L269) refines the same worker-kind check. NEW-34: its boundary is A54 B4 (L291, "A pass recorded without rows is a record gap") together with S9 (L317). | None. |
| R6-N6 | NOTE | P6-N2 is confirmed and refined (TESTED, `MUST_FAIL_CLASSIFICATION_R6V001.json`). Every named test resolves to PASS tests in both runs of record. Some families include ADOPT_TAIL controls (NEW-4, 13, 16, 60). NEW-16's `A53_ROUTE_A_BRANCH_UNCHANGED` resolves **only** to an ADOPT_TAIL control. Every ADOPTED item still names at least one non-adopting test. | Optional: drop or label the control-only entry. |
| R6-N7 | NOTE | The fence hooks `open` only; stat, listdir and scandir are not audited. The builder's "not listed or stat-ed" claim about `runs_ext` is therefore FORMAL, from its script sources (no such call, TESTED by grep of its named tools). Its 5 saved fence summaries read `blocked_after_selftest: []`. Its other runs left no log (UNTESTED). | None for P6. |
| R6-N8 | NOTE | The generator pins `SEAL_MANUAL_DISCLOSURES_V003_DRAFT.json` at 21968a07 and indexes ids by the V002 table. The ids are equal (TESTED). If root edits the draft in place before Claude4 runs the completion, the generator refuses PIN_MISMATCH (fail closed). | Re-pin to the final V003 if it changes. |
| R6-N9 | NOTE | The RI-31 checks in the refute brief do not apply to P6: child BLOCKED lists, the c7023846 spec set and the map T. No dry run belongs to P6, and none was run. | None. |

## 1. Pins and hashes (TESTED)

- Tool 4 `build_seal_record_c4v004.py` 9787cf58; seal_common 101a3aeb; tool 3 316973a1; tool 2 c2c5dfc5; case block 76309ae3; disclosures V002 a0284ece; prereg r6 d28c95f5; compare r13 f5adfd11 and IMPL 274f7049; r14 f3f9ba7e and IMPL CX1V002 2ba6d12e; c2v007r2 052da0fe; driver r5 b5cc62af; B1 record 83e7b067. Every value was computed from bytes.
- The builder's HASHES (731ff01a): all 106 rows verify. The folder has 107 files, the table plus itself, with no symlink. All 18 shas in the build result equal the bytes (`BUILDER_HASHES_CHECK_R6V001.json`).
- The builder's generators reproduce their outputs byte for byte (dry runs with the original `--utc`):
  - key map 72a21888;
  - r13 list 9a9ee6cf;
  - R14 variant 6bd8fa95.

  So every quote, line, sha and test resolution they embed re-verifies on today's bytes.

## 2. Key map, RI-30 (TESTED; stands)

- The case block, parsed by tool 4's own `C.strict_json_bytes`, has top-level keys {cases, key_equivalence_map, note, route_a_mode, schema}. `key_equivalence_map` = `[]` appears only at `$.key_equivalence_map`.
- It is read there in three places:
  - r13 and r14 L1557 `km = cb.get('key_equivalence_map', [])` (in `validate_case_block`, L1471);
  - tool 3 L482;
  - tool 3 L485, which passes it through.
- Prereg r6 `binding_inputs.case_block` is exactly that path and sha.
- `key_map_codes(file 1, [])` reports no failure. The must-fails return:
  - an extra entry: KEY_MAP_NOT_THE_CASE_BLOCK_MAP;
  - an unmappable pointer: KEY_MAP_ENTRY and NOT_THE_CASE_BLOCK_MAP;
  - not a list: KEY_MAP_SCHEMA;
  - an extra key: KEY_MAP_SCHEMA.

## 3. NEW-item dispositions (A81 RI-20)

- **Completeness (TESTED).** C-08 (V002) has 19 ids: NEW-4, 7, 13, 16, 17, 19, 21, 30, 31, 34, 39, 44, 52, 53, 54, 60, 64, 71 and 73.
  - Both files hold 17, in C-08 order, with none invented; NEW-30 and NEW-44 are left out.
  - Cross-check of root's C-08 against the source: the 19 ids are exactly the bare `NEW-n` ids in the r13 and r14 sources, at each table line (0 mismatches; V003_DRAFT on r14 likewise).
- **compare_impl (TESTED).**
  - The r13 IMPL names f5adfd11 and no r14 sha. IMPL_R14_CX1V002 names f3f9ba7e and declares no NEW id.
  - Under A116/A117 the slot is r14, so only the R14 variant, or its completion, passes. The r13 file refuses NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE.
- **Dispositions (FORMAL, against the sources).** Each of the 17 agrees with its source:
  - NEW-7, 13, 16, 17 and 19: A53 (V005 L242-251).
  - NEW-21: the r6 RI-10 table, "Adopted" (L68), and RI-10 itself (V005 L461).
  - NEW-31: A67 "Accepted" (L654).
  - NEW-52: r10, as A75.7 rules it (L1483).
  - NEW-64: A79 "accepted" (L1410).
  - NEW-71 and NEW-73: A86.5 "adopted as declared" (L1264).
  - NEW-39 and NEW-60: root rulings, implemented in r7 and r10.
  - NEW-4, 34, 53 and 54: stricter declarations under RI-10/RI-20, as root's c08_confirmation directs. R6-N5 adds the supporting root text.
  - No V005 line rules NEW-30 or NEW-44 (TESTED by id search; the only ranges are NEW-21..29 and NEW-71..81). A118 now rules both.
- **MUST_FAIL tests (TESTED).**
  - Every name resolves to tests that PASS in the r13 run (cad67c41, 706/706, f5adfd11) and in the r14 run (42c4961f, 718/718, f3f9ba7e; tests 998e0c2e = SELECTED_R14_CX1V002's author harness).
  - The IMPLs before r11 carry no MUST_FAIL label (counts 0; r11 has 3, r12 1, r13 and r14 0).

## 4. Raw successor custody (A59, A67 N1): R6-B1 in detail

**What is right.** The pins and the path from report to record are correct:
- comparator slot c2v007r2 052da0fe;
- Z2 record B1_R5_C2V007 83e7b067 (gate B1, tail ON, run `runs_ext/UVT_Z2_A2F10_R5_RUN_V001`, call spec 2d5e79d0, driver b5cc62af);
- report of record ac793faf, the hash from the record.

FORMAL, from the records writer 67bb3d09 L133-180: it copies the tokens path and the run and reference paths from the report. The R5 commands script 283cfde4 ran the comparator and tokens by paths whose realpath is themselves (TESTED). So every report/record equality the converter checks holds for the genuine files, except the one below.

**What fails.**
1. The driver r5 (b5cc62af) stage plan, FORMAL:
   - tail ON sets `ctx.scripts = dict(SCRIPTS, **SCRIPTS_UVT, route_a_tail_manifest=…)` (L2609);
   - `fs_feedback` (kind `feedback_v002`) always runs (L3139-3147);
   - every LE pass but the last runs `le<p>_feedback` (`feedback_v004`, L3266-3277);
   - an observed pass runs `le<p>_column_mean` (`column_mean_v004`, L3223-3241); the last pass is always observed when it has one column run;
   - each stage gets `request.json` with `kind` and `script` (L1821, L1843).
2. The B1 record shows LE passes 1-3 (le1-le3 rotations in the tail-block list). So the run has at least `fs_feedback`, `le1_feedback`, `le2_feedback` and `le3_column_mean`: at least 22 stages. With observe-every-pass it has 24.
3. Supporting record evidence, for the same call spec 2d5e79d0 on r4 (A52 launch table):
   - the A59 verification `v007_identity_gates_c2/z2_v002/verify/VERIFY.md` (5ce4d5d8) L23: "The kinds with no successor are column_mean_v004, feedback_v002, feedback_v004 and route_a";
   - L42 names le1 and le2 feedback stages, and L57 names le1_column_mean;
   - A59's raw check covered "every stage of the 8 kinds" (L33).
4. The comparator (FORMAL, L2336-2347) gives these stages rows with `planned_sha256 = SCRIPTS[kind]` and `ok: true`. The converter (L187) refuses them, and its count rule (L280) also requires every stage to be a successor stage.
5. **TESTED (synthetic only; `TEST_CONVERTER_REAL_STAGE_SET_R6V001.json` 300f26d6, `fixtures/real_stage_set_v001/`)**:

   | Fixture | Stages | Result |
   |---|---|---|
   | the builder's 18-stage set | 18 | DRY_RUN_PASS |
   | the driver plan with 22 stages | 22 | refuses `STAGE_KIND_HAS_NO_SUCCESSOR` at `fs_feedback` (rc 2, nothing written) |
   | the driver plan with 24 stages | 24 | the same refusal |

   The builder's own harness turned this real shape into must-fail case F14 (test_custody_converter_c4v002 L208). Its PASS fixture (L23) omits all three kinds.
6. The real report was not opened, so the exact stage list is UNTESTED here. The refusal follows from the driver plan, the record and the converter source.

## 5. Tool 4's own functions (TESTED; `VALIDATION_TOOL4_REFUTE_R6V001.json` b8e0e81b, 21/21 as expected)

- **Call sites.** `key_map_codes(…pt['key_equivalence_map'])`, `new_items_codes(…slots['compare_reviewed_source']['sha256'])`, `custody_codes(…slots['driver']['sha256'])` and `C.strict_json(path)` each occur once.
- **The driver slot is r5 b5cc62af** (prereg r6 `seal_slots.driver`: branch r5, A96; the only candidate).
- **Custody.** The converter's dry-run record on the synthetic 18-stage control passes `custody_codes` against b5cc62af. Its six evidence pins verify. The must-fails return:
  - an r4 slot: CUSTODY_DRIVER_NOT_THE_SLOT;
  - n-1 successors: CUSTODY_STAGES;
  - boolean counts: CUSTODY_STAGES;
  - Z2_OFF_RO1: CUSTODY_RUN;
  - a bad evidence sha: PIN_BYTES_MISMATCH.

## 6. The builder's findings, re-graded

| Builder id | Refute reading |
|---|---|
| P6-B1 | Superseded by A118 (R6-N2); the completion path is TESTED. |
| P6-S1 | Confirmed and extended (R6-S1). |
| P6-S2 | Confirmed (TESTED), and now required: A116/A117 put r14 in the slot. R6-N1 is a note on NEW-52. |
| P6-S3 | Resolved by A118 (R6-N3). |
| P6-N1 | Not refuted; further support (R6-N5). |
| P6-N2 | Confirmed and refined (R6-N6). |
| P6-N3 | **Refuted as graded.** The refusal is certain, not a possible NOTE, and the expected n is 22-24, not 18. This is R6-B1. |
| P6-N4 | Stale (R6-N4). |
| P6-N5 | Confirmed: the builder's `--check-only` run here gives AST = regex on all 6 tables. |
| P6-N6 | Confirmed as to this helper: the Z2 report was not opened here either. |

## Files here

See `HASHES_REFUTE_P6.txt` (written last). The tools: `verify_builder_hashes_r6v001.py`, `test_converter_real_stage_set_r6v001.py`, `validate_b7_refute_r6v001.py` and `classify_must_fail_r6v001.py`, plus the fence and runner copies. The outputs: `BUILDER_HASHES_CHECK_R6V001.json`, `TEST_CONVERTER_REAL_STAGE_SET_R6V001.json`, `VALIDATION_TOOL4_REFUTE_R6V001.json` and `MUST_FAIL_CLASSIFICATION_R6V001.json`, with the synthetic fixtures and `PARTIAL.md`.
