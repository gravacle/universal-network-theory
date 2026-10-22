# STAGE0 successor c2v001 (r3a M-14): build record

`date -u` at write: 2026-10-19T16:10:45Z.

This is a root-workflow build (Claude2 lane) for the V006 A142 build row "STAGE0 successor (M-14, with both TESTs) | root workflow | Claude3". **Nothing here is adopted.** Under the M-14 pin rule, the seal entry pins this successor only if Claude3's independent review returns 0 blocking before the seal entry is written. The seal never waits for it.

Synthetic tests only; there was no production run. The only program file that code opened is the v003g module: its bytes were hashed and it was imported read-only with `-B`. The real slots V003 file was never opened. Instead, the tests use a synthetic slots copy with a synthetic pin (and a synthetic GL-node roster), patched in memory into both modules.

## Files

| File | sha256 | What |
|---|---|---|
| `prediction_freeze_c2v003g_stage0_c2v001.py` | `e015e617c7437afc1863ef8e30e82f040555bdf32ed0f6518f27ac7ccfb330fe` | the successor module, built by the script below and not edited by hand |
| `build_stage0_successor_c2v001.py` | `2f8e36689b3a684a7a1144f42a071cbed7fafbdc8c8616fe23322173b3c9c145` | builds it from v003g `48a1e48a…` through 18 named replacements, each of which must match exactly once |
| `test_stage0_successor_c2v001.py` | `1a8a06ed39b675ff775efcbc6fb9411ee5347a016c2335da90abfc5005f7b64a` | the 42 synthetic tests |
| `make_reports_stage0_successor_c2v001.py` | `d856163b791e96b5aa36f9ccaf7d07d318b11fd3b3c2702ed80c703ec24d6e7e` | writes the diff and the AST report |
| `DIFF_v003g_to_stage0_successor_c2v001.diff` | `a4c3acf0167306c3bdde07317820e245e186168b172786f333b795b4e2ca5fdf` | unified diff: 455 lines added, 10 removed |
| `AST_IDENTITY_STAGE0_SUCCESSOR_C2V001.md` | `aa67618ec09ad7f24bbbe113ef4879ce693e215686e26e57ed708e0ead84b88a` | AST identity of every top-level function, constant and statement |
| `test_runs/run_1_20261019T160509Z/`, `test_runs/run_2_20261019T160531Z/` | see `HASHES.txt` | the two record runs |
| `dev/` | see `HASHES.txt` | drafts, dev runs and the mutation check; not deliverables |

`HASHES.txt` gives the sha256, computed from the bytes, of every file in this directory except itself.

## What the successor changes

It changes only the status of STAGE0_GRID_OUTER. In a Phase-2 freeze, STAGE0 may read EVALUATED_BEFORE_FREEZE, and only by the M-14 receipt rule. The successor never requires EVALUATED, and STAGE0 never makes a freeze refuse.

- **Functions.** 102 of v003g's 109 functions are AST-identical. Seven changed, each only on lines marked `STAGE0 successor`: `_load_row_roster`, `_root_rosters_for_alternatives`, `_bind_alternatives`, `_validate_manifest_structure`, `write_freeze_manifest`, `_alternative_score_scope` and `score_after_freeze`. The AST report gives each change in one line.
- **New code.** There are 20 new functions, all named `_stage0_*`, and 19 new constants, all named `STAGE0_*`. They form one section placed after `_member_order`.
- **Everything else.** The module docstring gains a header. The imports and v003g's top-level order are unchanged.

### Constants and pins (M-5 addition (2))

| Constant | v003g | successor |
|---|---|---|
| `SCHEMA` | `FREEZE_MANIFEST_C2V003G` | `FREEZE_MANIFEST_C2V003G_STAGE0_C2V001` |
| `MODULE_NAME` | `prediction_freeze_c2v003g_cx3v001` | `prediction_freeze_c2v003g_stage0_c2v001` |
| `MANIFEST_KEYS` | 29 keys | the same 29 plus `stage0_status` |

These stay AST-identical: `ROOT_SLOTS_PATH` and `ROOT_SLOTS_SHA256` (slots V003 `d3859b42…`), `REGISTRATION_SCHEMA`, `PROGRAM_QUERY_MANIFEST_SHA256`, `REGISTERED_GL_NODES_PATH` and `REGISTERED_GL_NODES_SHA256`, and every other v003g constant. No slots successor is needed, because STAGE0's status now comes from root-written bytes and not from the slots file.

The seal entry would name these per phase:
- **Phase 1:** v003g `48a1e48a…` with slots `d3859b42…` (M-5, unchanged).
- **Phase 2, if the successor is pinned:** this module `e015e617…` with slots `d3859b42…`.
- **Phase 2, if it is not pinned:** v003g, where STAGE0 stays NOT_EVALUATED_BEFORE_FREEZE.

Each freeze also gains new input pins: the root STAGE0 status record and every receipt whose custody verifies. The writer adds them to `input_files` itself.

## The rule as implemented

`write_freeze_manifest(..., stage0_status_record=None)` works as follows.

1. **The caller passes the slots alternatives unchanged.** If the caller sets STAGE0's status, it is put back to the slots value, so the status is never the producer's to set (TESTED, P1).
2. **A STAGE0 evaluation in `alternative_evaluations` is set aside before D9.** D9 then binds every other alternative exactly as v003g does. C03 shows v003g refusing the whole freeze in this situation; A1–A3 show the successor completing it.
3. **The receipt rule reads the status record.** The record's sha256 is checked from its bytes, and it passes the module's target screen.
   - **Phase 1:** STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE with NOT_IN_PHASE_1, and no receipt is read.
   - **Phase 2:** three conditions are checked.
     - **(a)** Every PRIMARY member (one STAGE0 call per PRIMARY member) has exactly one receipt. Its sha256 must match its bytes, and it must name STAGE0_GRID_OUTER, the member's `log_index`, the member's exact `theta_ngc` and the sha256 of the slots STAGE0 coefficient grid. It must read FINISHED.
     - **(b)** The record's `sealed_successor.module_sha256` equals the sha256 of this module's own bytes.
     - **Timing:** every FINISHED receipt has `written_utc` <= `step4_start_utc`. A tie counts as before step 4.
   - **When (a), (b) and the timing all hold,** the STAGE0 evaluation must pass every check v003g applies to a frozen alternative, and its status must be COMPLETE. STAGE0 is then frozen EVALUATED_BEFORE_FREEZE. If the evaluation fails a check, or if a receipt entry is refused (for example one for a non-member), the reading is EVALUATED_REFUSED and the status stays NOT_EVALUATED_BEFORE_FREEZE.
   - **Otherwise** the reading is NOT_EVALUATED_BEFORE_FREEZE with every code that applies: STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR, RECEIPTS_AFTER_STEP4. With the last code, `post_score_exploratory` is true. An absent, unreadable or malformed record establishes neither (a) nor (b).
4. **The writer, verifier and scorer all recompute the block** from the pinned bytes and the frozen PRIMARY members. They refuse a manifest whose block, STAGE0 status or custody pins disagree (TESTED: F4, F8, F10, F11).

The rule never reads an output value, and validity booleans never change the status (TESTED: E3).

## Field map (M-5: to be reviewed before the seal)

The manifest and the score output both carry `stage0_status`. In the score output it is `None` on refusal paths.

| Key | Meaning |
|---|---|
| `reading` | `EVALUATED_BEFORE_FREEZE`, `NOT_EVALUATED_BEFORE_FREEZE` or `EVALUATED_REFUSED` |
| `reasons` | the M-14 codes: `NOT_IN_PHASE_1`, `STAGE0_RECEIPT_NOT_FINISHED`, `NO_SEALED_SUCCESSOR`, `RECEIPTS_AFTER_STEP4`; empty for `EVALUATED_BEFORE_FREEZE` and `EVALUATED_REFUSED` |
| `post_score_exploratory` | true if and only if `RECEIPTS_AFTER_STEP4` applies |
| `phase` | `PHASE_1`, `PHASE_2`, or null when no record is readable |
| `step4_start_utc` | the root-recorded Phase-2 step-4 start |
| `members[]` | one row per PRIMARY member: `member_id`, `log_index`, `receipt` (pin), `custody_ok`, `terminal_status`, `written_utc` (the receipt time), `finished`, `before_step4`, `defects` |
| `sealed_successor`, `successor_module_sha256` | the record's `{module_sha256, source}`, and this module's own sha256 |
| `rule_a_receipts_finished`, `rule_b_successor_sealed`, `receipts_before_step4` | the three conditions |
| `receipt_refusals`, `evaluation_refusals` | why the reading is `EVALUATED_REFUSED` |
| `diagnostics` | codes at the level of the record |
| `status_record`, `status_record_custody_ok` | the record pin |
| `rule`, `alternative`, `module` | fixed text and names |

How the rest of the output follows the reading:
- `alternatives.declared[STAGE0_GRID_OUTER].status` is `EVALUATED_BEFORE_FREEZE` if and only if the reading is `EVALUATED_BEFORE_FREEZE`. Every other field under `alternatives` equals v003g.
- `alternative_results.STAGE0_GRID_OUTER` is present if and only if the reading is `EVALUATED_BEFORE_FREEZE`.
- The STAGE0 entry of the score output's `alternatives[]` keeps the v003g encoding. When the reading is `EVALUATED_BEFORE_FREEZE`, that entry is scored on `scoring_scope.query_ids` only (8 OUTER rows, denominator 8) with `headline: false`.

The root-written inputs use schemas defined here:
- **Status record `STAGE0_STATUS_RECORD_C2V001`** has exactly these keys:
  - `schema`, `phase`, `alternative`;
  - `sealed_successor`: `{module_sha256, source}` or null;
  - `step4_start_utc`: `YYYY-MM-DDTHH:MM:SSZ`, or the same with a 6-digit fraction;
  - `receipts`: a list of `{member_log_index, receipt: {path, sha256}}`.
- **Terminal receipt `STAGE0_TERMINAL_RECEIPT_C2V001`** has exactly these keys: `schema`, `alternative`, `member_log_index`, `theta_ngc`, `coefficient_grid_sha256`, `terminal_status` (`FINISHED` or any other string) and `written_utc`.

## Tests

Command: `python3 -I -B test_stage0_successor_c2v001.py --run-dir test_runs/<new dir>`.

There were two record runs, and each passed 42 of 42: 26 MUST_PASS, 13 MUST_FAIL and 3 CONTROL. Their results are identical once the run-directory path is normalised. Each run directory holds the synthetic fixture, the files of every scenario (manifests, registrations, records, receipts) and `RESULTS_test_stage0_successor_c2v001.json`.

A MUST_FAIL test passes when the attack fails: it is refused, or STAGE0 reads something other than EVALUATED.

| Id | Expectation | What it shows |
|---|---|---|
| T01 | MUST_PASS | AST identity: every non-STAGE0 v003g function and constant is unchanged; 7 functions and 3 constants changed, as listed |
| C01–C03 | CONTROL | v003g baseline; v003g refuses a STAGE0 replay evaluation; **v003g D9 refuses the whole freeze** when a STAGE0 evaluation is supplied |
| **A1** | MUST_PASS | **TEST (a):** a Phase-2 freeze with a non-FINISHED STAGE0 receipt and a STAGE0 evaluation supplied completes. STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (STAGE0_RECEIPT_NOT_FINISHED); the manifest verifies and scores |
| A2, A3 | MUST_PASS | TEST (a) variants: no STAGE0 evaluation, or a BUDGET_EXHAUSTED one with `allow_incomplete=False`. The freeze is FREEZE_COMPLETE and STAGE0 adds no incomplete reason |
| **B1** | MUST_PASS | **TEST (b), NOT_EVALUATED:** the manifest `alternatives` and query block (`query_ids`, `input_bindings`) are byte-identical to v003g's output. The score output's `alternatives` is byte-identical too. Besides the identity hashes, only `stage0_status` is added |
| **B2** | MUST_PASS | **TEST (b), EVALUATED:** the manifest `alternatives` differs from v003g at exactly one path, `declared[5].status`. The query block and headline are identical. The score output differs only in STAGE0's status-dependent fields (`status`, `scored`, `note`, `members`, `member_within_error_counts`, `member_evaluation_status`) |
| E1–E3 | MUST_PASS | EVALUATED when the rule holds, scored on 8 OUTER rows; a receipt at the step-4 instant counts as before; a FINISHED member that is `valid:false` keeps STAGE0 EVALUATED |
| N1–N10 | MUST_PASS | every NOT_EVALUATED code, alone and combined; a Phase-1 record gives NOT_IN_PHASE_1; no record, a malformed record and a record custody mismatch; a v003g-style call; evaluation refusals are judged only when the rule holds |
| R1–R4 | MUST_PASS | EVALUATED_REFUSED, with the freeze completing, for: no evaluation, a partial evaluation, the wrong roster, a malformed member |
| P1 | MUST_PASS | a caller's flip of STAGE0 to EVALUATED is ignored |
| **F1** | MUST_FAIL | **forged FINISHED receipt (sha256 and custody mismatch)** is not accepted |
| F2, F3, F12, F13 | MUST_FAIL | FINISHED receipts with the wrong theta, the wrong grid, another member's receipt, or a PRIMARY (headline) call receipt are not accepted |
| **F5, F6** | MUST_FAIL | **a receipt for a non-member**, whether substituted for a member's (NOT_EVALUATED) or added alongside (EVALUATED_REFUSED), never reads EVALUATED |
| **F7, F8** | MUST_FAIL | **a partial receipt set is never read as EVALUATED**; a manifest re-hashed to claim it is refused |
| F4, F10, F11 | MUST_FAIL | forged manifests (a flipped status, an unpinned receipt, refusals recorded without the rule holding) are refused by the verifier. In F4 the scorer also refuses, even with a matching forged registration |
| F9 | MUST_FAIL | two receipts for one member are not accepted |
| X1 | MUST_PASS | no cross-use: each module refuses the other's manifest |
| S1 | MUST_PASS | STAGE0 never enters the headline: the headline and PRIMARY member scores are identical whether STAGE0 is evaluated or not |

**Mutation check** (`dev/mutation_final/`; dev evidence). The final suite was run against 10 deliberately broken copies of the final module. Every copy was caught: each made at least one test fail.

| Broken copy | Tests that failed |
|---|---|
| rule (a) uses `any` instead of `all` | 16 tests |
| eligibility reduced to phase only | N10, F11 |
| no pre-screen of the STAGE0 evaluation | R1–R4 |
| no manifest check | F4, F8, F10, F11 |
| no theta check | F2 |
| no duplicate check | F9 |
| strict `<` for the step-4 tie | E2 |
| no sealed-sha check | N2 |
| no grid check | F3 |
| no custody-pin check | F10 |

## Labels

**TESTED** (synthetic, both record runs):
- TEST (a) and TEST (b);
- the MUST_FAIL attacks listed above;
- every M-14 code and the EVALUATED_REFUSED path;
- AST identity;
- no cross-use between the two modules;
- STAGE0 kept out of the headline;
- the mutation check.

**FORMAL** (follows from reading the code; not exercised):
- **Score-time byte changes.** A change to a STAGE0 record or receipt after the freeze is refused at score time: those files are pinned in `input_files`, and the scorer re-reads them and recomputes the block. This was not tested because the tests never edit a file.
- **Sensitivity roster.** `evaluate_sensitivity` shares `_load_row_roster`, so it also no longer refuses a STAGE0 roster. The writer's unchanged v003g check still refuses any sensitivity that is not on the PRIMARY roster.
- **Pre-screen coverage.** The pre-screen of the STAGE0 evaluation mirrors every check v003g applies to a frozen alternative, so an admitted STAGE0 cannot make the assembled manifest fail. R1–R4 exercise four kinds of failure.
- **Evaluation refusals.** `evaluation_refusals` is the writer's own record. The verifier accepts it only where the receipt rule holds (F11), but cannot recompute it, because a refused evaluation is not frozen. This rests on the honest-producer model (A115).

**UNTESTED:**
- **The real slots V003 bytes.** The module relies on their STAGE0 record reading NOT_EVALUATED_BEFORE_FREEZE and carrying `headline`, `scoring_scope` and `coefficient_grid_pin`. v003g's code reads these fields, and prereg §6.3 and M-14 state the status. This build did not open the file.
- **The real A133 §3 rule (c) receipts.** The receipt schema is defined here. If the launch path writes receipts in another format, every STAGE0 receipt reads MALFORMED and STAGE0 reads NOT_EVALUATED. That outcome is fail-safe: it never yields EVALUATED. Mapping the real receipts belongs to the reviewed field map before the pin.
- **Rule (b) against the seal entry itself.** The module checks that the root record names the module's own sha256; it does not read V006. Root's record attests the pin.
- **Headline-first, no preemption.** M-14 records knowingly that headline calls launch first and that STAGE0 calls never preempt a headline call. That is a launch-path (scheduling) rule this module cannot see. The module enforces only one receipt per PRIMARY member and never reads a PRIMARY receipt as STAGE0 (F13).
- **Real NGC runs, real rosters and real scoring.**

## Deviations and disclosures

1. **No slots successor.** M-14 (b) allows a "slots/module successor"; this is a module successor, and slots V003 stays pinned. TEST (b) is read as applying to the v003g **output** (manifest and score). The slots query block is unchanged by construction, because the file is the same.
2. **New input schemas.** The status-record and receipt schemas are defined here. The A133 text of record was not named in the dispatch, so it was not opened, and the real receipt format is unknown to this build.
3. **`SCHEMA` changed** because the manifest gains a key. Classifiers A and B must take `FREEZE_MANIFEST_C2V003G_STAGE0_C2V001` through the field map above.
4. **Synthetic fixtures carry program strings.** The module requires certain program strings, so the synthetic fixtures contain them: the GL-node schema name, `galaxy: NGC3198` in the synthetic forward results, and DDO154-region key names in the synthetic region file. Every value is synthetic, and the fixture files are marked `synthetic_fixture` where the layout allows.
5. **`dev/`** holds 3 drafts, 3 builder versions, 2 test-suite versions, 2 report-generator versions, dev runs, and two mutation sets (from drafts 01 and 02, plus `mutation_final`). Everything was written by exclusive create inside this directory, and nothing outside reads it.
6. **Recursion inside this build directory only.** `find` was run once on this build directory to confirm no bytecode was written, and `HASHES.txt` walks this directory. No other tree was searched recursively.
7. **Harness output outside this directory.** Background commands had their stdout captured by the harness in its own session temp directory. No other file was written outside this directory, and no existing file was edited.
