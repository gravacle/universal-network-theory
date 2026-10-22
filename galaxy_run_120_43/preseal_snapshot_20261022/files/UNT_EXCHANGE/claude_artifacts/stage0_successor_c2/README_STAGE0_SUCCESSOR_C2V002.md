# STAGE0 successor c2v002 (r3a M-14): build record

`date -u` at write: 2026-10-19T17:21:35Z.

This is a root-workflow build (Claude2 lane) for the V006 A142 build row "STAGE0 successor (M-14, with both TESTs) | root workflow | Claude3". **Nothing here is adopted.** c2v002 supersedes c2v001 (`e015e617…`, never adopted). It fixes the two BLOCKING verifier items, D05 and D07. Under the M-14 pin rule, the seal entry pins this successor only if Claude3's independent review returns 0 blocking before the seal entry is written. The seal never waits for it.

The build used synthetic tests only; there was no production run. Code opened three program files, and imported each read-only with `-B`:
- the v003g module (`48a1e48a…`, sha256 checked from its bytes);
- the c2v001 module, built in this directory, which supplies the two controls;
- the c2v002 module.

The real slots V003 file was never opened. The tests use a synthetic slots copy with a synthetic pin and a synthetic GL-node roster, patched in memory into all three modules. No c2v001 file was edited. `HASHES.txt` (c2v001) is unchanged and is itself pinned in `HASHES_V002.txt`.

## The two review items

### D05: a STAGE0 defect made the writer refuse the whole Phase-2 freeze (fixed; TESTED)

**Cause (c2v001).** `_stage0_apply_record` set `status_record_custody_ok` and the row's `custody_ok` *before* the schema check. Suppose a custody-correct pin named a JSON whose schema is `CALIBRATION_RUN_RECORD_C2V003`, such as a copy of the calibration record. That file was added to `input_files`. v003g's calibration-record census then counted two records and refused with `REFUSED (P34-16): more than one calibration record pinned`. Control **C04** reproduces this on c2v001.

**Fix (c2v002).**
- **Schema check first.** `custody_ok` is set only after the file passes its STAGE0 schema check: the exact key set and the STAGE0 schema string. Only `custody_ok` files are pinned. A pinned STAGE0 file therefore carries a STAGE0 schema string and can never satisfy the census condition `schema == CALIBRATION_RUN_RECORD_C2V003`. A file that fails its schema check is neither pinned nor read again (see D07).
- **No duplicate pin paths.** The writer adds a `custody_ok` file to `input_files` by realpath, and skips it if `input_files` or `code_files` already list that realpath. This closes a refusal of the same class, `REFUSED: duplicate pin paths`. It is not in the D05 text; see deviation 1.

**Tests.**

| Test | What it shows |
|---|---|
| G1 | The record pin names a copy of the calibration record. |
| G2 | A receipt's schema is the calibration schema. |
| G3 | A receipt pin names a calibration copy. |
| G4 | The record pin names the bound record itself. |
| G5 | Schema-valid STAGE0 files carry the calibration schema string as a *value*. They are pinned, and the census is unaffected. |
| G6 | The status record is reached through a symlink alias and is also listed in `code_files`. A receipt is reached through an alias, and another receipt is also listed in `input_files`. The result is EVALUATED with no duplicate pin path. |

Every one of these freezes completes, verifies and scores.

### D07: an unpinned STAGE0 file could void a registered freeze (fixed; TESTED)

**Cause (c2v001).** `_stage0_manifest_check` recomputed the verdict at verify and score time by re-reading every STAGE0 path the frozen block lists, including files that were never pinned. Suppose a receipt was absent at freeze time and its root-pinned bytes appeared later. The recomputed block then differed from the frozen block, and verify and score refused with `STAGE0_STATUS_BLOCK_MISMATCH`. Control **C05** reproduces this on c2v001.

**Fix (c2v002).** At verify and score time (`_stage0_receipt_verdict(..., frozen=block, pinned=map)`), these rules apply:
- **Files that were not custody_ok are never read again.** This covers the status record and any receipt that was not `custody_ok` at freeze time. The verifier carries the file's single frozen code, and only if that code is one a read can produce:
  - for a record with a pin: `…_CUSTODY_MISMATCH`, `…_TARGET_FIELDS_REFUSED` or `…_MALFORMED`;
  - for a record without one: `STAGE0_STATUS_RECORD_NOT_SUPPLIED` or `…_PIN_MALFORMED`.

  Any other frozen code yields the sentinel `STAGE0_FROZEN_DEFECT_INCONSISTENT`. The recomputed block then differs from the frozen one, and the manifest is refused. A carried defect can never yield FINISHED, so it can only keep STAGE0 NOT_EVALUATED.
- **Custody_ok files are read from their pinned copy.** The copy is matched by sha256 across `code_files` and `input_files`, never taken from the path root named. No path a root record names is read or realpath'd after the freeze.
- **STAGE0 pins are normalised lexically.** This uses `os.path.normpath` of an *absolute* path, where c2v001 used realpath. A file or symlink that later appears at an unread path therefore cannot change the recomputation.
- **The custody pin check runs first.** It now runs before the recomputation and matches by sha256.

**Tests.**

| Test | What it shows |
|---|---|
| H1 | A receipt is absent at freeze time and its pinned bytes appear later. Verify and score succeed before and after, and the frozen block stands, although re-reading now would satisfy the rule. |
| H2 | The status record is absent at freeze time and appears later. A fresh freeze now reads EVALUATED, but the registered freeze still verifies and scores NOT_EVALUATED. |
| H3 | An empty path later becomes a symlink to the pinned bytes. |
| H4 | Verify and score are instrumented by wrapping `_read_regular` and `os.path.realpath`. On the G6 and H1 manifests they make no call on any root-named STAGE0 path. |
| F14–F17, F19 (MUST_FAIL) | Forged carried defects are refused. |
| F18 | Covers the D8 boundary; see the labels below. |

## Files (c2v002)

| File | sha256 | What |
|---|---|---|
| `prediction_freeze_c2v003g_stage0_c2v002.py` | `d260ee308a7f215176cab1fff51e94cb52c7fc6cdd64aa4da48c66f8091820f0` | the successor (278044 bytes), built by the script below and not edited by hand |
| `build_stage0_successor_c2v002.py` | `27cf64aafeaef298d8c171a0e58394c6fbed0c4c79c8a44be69a6709f2c49523` | builds it from v003g `48a1e48a…` through 18 named replacements, each of which must match exactly once |
| `test_stage0_successor_c2v002.py` | `acdebc011d5b03a35580a06911061d3015b89dcbcbc58d2abb6e8dc97b42b70e` | the 62 synthetic tests |
| `make_reports_stage0_successor_c2v002.py` | `dc58eb8a663c4b1f6bc030b2b58acfa03836b0b62b3fb6c3774cc7b85ff130b4` | writes the two diffs and the AST report |
| `DIFF_v003g_to_stage0_successor_c2v002.diff` | `7b2fae04c6dd69ff01723352e2c19190e4385a55de212e5b16ac12a856186b58` | unified diff against v003g: 566 lines added, 10 removed |
| `DIFF_stage0_successor_c2v001_to_c2v002.diff` | `fbc84003ceb7f38ff48f9fbde692f3596e690aa8517b14ea0d0bc69f5c0dde7b` | review aid, the fix only: 160 lines added, 49 removed |
| `AST_IDENTITY_STAGE0_SUCCESSOR_C2V002.md` | `252486f34214fe4c36c29ea81cbce1b0ac4824ce13b23a2057ac7aa89dc96241` | AST identity against v003g, plus a by-AST change list against c2v001 |
| `test_runs_c2v002/run_1_20261019T171802Z/`, `run_2_20261019T171842Z/` | see `HASHES_V002.txt` | the two record runs; each holds RESULTS and FILES_WRITTEN |
| `dev_v002/` | see `HASHES_V002.txt` | drafts, dev runs and the mutation check; not deliverables |
| `HASHES_V002.txt`, `hashes_stage0_successor_c2v002.py` | the script's sha256 is in `HASHES_V002.txt` | sha256 from bytes of every c2v002 file, the c2v001 top-level files and `HASHES.txt` |

## What the successor changes against v003g

The only behavioural change concerns STAGE0_GRID_OUTER's status. In a Phase-2 freeze it may read EVALUATED_BEFORE_FREEZE, and only by the M-14 receipt rule. The successor never requires EVALUATED, and STAGE0 never makes a freeze refuse.

- **Changed functions.** 102 of v003g's 109 functions are AST-identical. The same seven changed as in c2v001, each only on lines marked `STAGE0 successor`: `_load_row_roster`, `_root_rosters_for_alternatives`, `_bind_alternatives`, `_validate_manifest_structure`, `write_freeze_manifest`, `_alternative_score_scope` and `score_after_freeze`. Against c2v001, `write_freeze_manifest` changes in two places: its STAGE0 docstring paragraph, and one line, `_stage0_input_files(input_files, stage0, code_files)`.
- **New code.** There are 25 new functions, all named `_stage0_*`, and 25 new constants, all named `STAGE0_*`. They sit in one section after `_member_order`.
- **Everything else.** The imports and v003g's top-level order are unchanged.

### Constants and pins (M-5 addition (2))

| Constant | v003g | c2v002 |
|---|---|---|
| `SCHEMA` | `FREEZE_MANIFEST_C2V003G` | `FREEZE_MANIFEST_C2V003G_STAGE0_C2V002` |
| `MODULE_NAME` | `prediction_freeze_c2v003g_cx3v001` | `prediction_freeze_c2v003g_stage0_c2v002` |
| `MANIFEST_KEYS` | 29 keys | the same 29 plus `stage0_status` |

The following stay AST-identical:
- `ROOT_SLOTS_PATH` and `ROOT_SLOTS_SHA256` (slots V003 `d3859b42…`);
- `REGISTRATION_SCHEMA` and `PROGRAM_QUERY_MANIFEST_SHA256`;
- `REGISTERED_GL_NODES_PATH` and `REGISTERED_GL_NODES_SHA256`;
- every other v003g constant.

No slots successor is needed.

The seal entry would name these per phase:
- **Phase 1:** v003g `48a1e48a…` with slots `d3859b42…`.
- **Phase 2, if c2v002 is pinned:** module `d260ee30…` with slots `d3859b42…`.
- **Phase 2, if it is not pinned:** v003g, where STAGE0 stays NOT_EVALUATED_BEFORE_FREEZE.

Each freeze also gains new input pins, which the writer adds itself: the root STAGE0 status record and every receipt that is `custody_ok`.

## The rule as implemented

The receipt rule is unchanged from c2v001.
- **Phase 1:** STAGE0 reads NOT_IN_PHASE_1.
- **Phase 2:** STAGE0 is EVALUATED iff all of the following hold:
  - **(a)** Every PRIMARY member has exactly one `custody_ok` receipt. That receipt names STAGE0_GRID_OUTER, the member's `log_index`, its exact `theta_ngc` and the slots grid sha256, and it reads FINISHED.
  - **(b)** The record names this module's sha256 as the sealed successor.
  - **Timing:** each FINISHED receipt has `written_utc` <= `step4_start_utc`.
  - **Evaluation:** the STAGE0 evaluation passes every check v003g applies to a frozen alternative and is COMPLETE.
- **Otherwise:** STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE with STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR or RECEIPTS_AFTER_STEP4, or reads EVALUATED_REFUSED.

The writer, verifier and scorer all check the frozen block against a recomputation made under the D07 rules above.

## Field map (M-5: to be reviewed before the seal)

The field map is the c2v001 map with these changes.

| Field | c2v002 meaning |
|---|---|
| `status_record`, `members[].receipt` | `{path, sha256}`: `os.path.normpath` of an **absolute** path, with a lowercase sha256 (c2v001 used realpath). These are the pins root named. |
| `status_record_custody_ok`, `members[].custody_ok` | True iff the sha256 verifies from the bytes, the target screen passes, the file is a JSON object **and the STAGE0 schema check passes**. These are exactly the files whose bytes are pinned (by sha256, in `code_files` or `input_files`), and the only STAGE0 files that verify and score read, from their pinned copy. |
| `diagnostics` | New code `STAGE0_STATUS_RECORD_PIN_MALFORMED`: a supplied pin is not `{path, sha256}` with an absolute path and a 64-hex sha256. c2v001 read this as NOT_SUPPLIED. |
| `receipt_refusals` | A receipt entry whose path is not absolute is `STAGE0_RECEIPT_ENTRY_MALFORMED`. |
| `STAGE0_FROZEN_DEFECT_INCONSISTENT` | Never written to a manifest; it appears only in a recomputed block, to force a refusal. |
| verify reason `STAGE0_CUSTODY_FILE_NOT_PINNED` | Checked before the recomputation, by sha256 across `code_files` and `input_files`. |

The input schemas keep their names: `STAGE0_STATUS_RECORD_C2V001` and `STAGE0_TERMINAL_RECEIPT_C2V001`. The one new input requirement is that paths must be absolute.

## Tests

Command: `python3 -I -B test_stage0_successor_c2v002.py --run-dir test_runs_c2v002/<new dir>`.

There were two record runs. Each passed 62 of 62: 38 MUST_PASS, 19 MUST_FAIL and 5 CONTROL. Their results are identical once the run-directory names and the 64-hex hashes are normalised; the hashes differ because of `created_utc` and paths. Each run created the same 400 files and symlinks.

All 42 c2v001 tests are kept unchanged: T01, C01–C03, A1–A3, E1–E3, B1, B2, N1–N10, R1–R4, P1, F1–F13, X1 and S1. That includes TEST (a) (A1–A3), TEST (b) (B1, B2) and the dispatch's MUST_FAIL attacks: forged FINISHED receipt (F1), non-member receipt (F5, F6) and partial receipt set (F7, F8). F10 now locates its pin by realpath. The 20 new tests are:

| Id | Expectation | What it shows |
|---|---|---|
| G1–G5 | MUST_PASS | D05 regressions (see above) |
| G6 | MUST_PASS | symlink aliases, plus files also listed in `code_files` or `input_files`: no duplicate pin; EVALUATED |
| N11, N12 | MUST_PASS | a relative record pin reads PIN_MALFORMED; a relative receipt entry reads ENTRY_MALFORMED; both NOT_EVALUATED |
| H1–H3 | MUST_PASS | D07 regressions: files absent at freeze time appear later, directly or as a symlink |
| H4 | MUST_PASS | verify and score make no read or realpath call on a root-named STAGE0 path |
| F14 | MUST_FAIL | a carried row flipped to `custody_ok` *with* the late bytes pinned is refused (BLOCK_MISMATCH) |
| F19 | MUST_FAIL | the same flip without pinning is refused (CUSTODY_FILE_NOT_PINNED) |
| F15, F16 | MUST_FAIL | a carried row given a code a read cannot produce, or another pin, is refused |
| F17 | MUST_FAIL | a carried record given NOT_SUPPLIED while a pin exists is refused |
| F18 | MUST_FAIL | a full re-hashed flip to EVALUATED after the late receipt appears is refused by the scorer under the genuine registration (D8) |
| C04, C05 | CONTROL | c2v001 reproduces D05 (the whole freeze is refused) and D07 (verify and score refuse after the bytes appear) |

**Mutation check** (`dev_v002/mutation/`, summary `MUTATION_SUMMARY_C2V002.json`; dev evidence). The final suite ran against 18 deliberately broken copies of `d260ee30…`, and every copy was caught.

| Broken copy | Tests that failed |
|---|---|
| M01–M10: the c2v001 set (rule (a) uses `any`, eligibility by phase only, no pre-screen, no manifest check, no theta check, no duplicate check, `<` for the step-4 tie, no sealed-sha check, no grid check, no custody-pin check) | each caught, as in c2v001 |
| M11: record `custody_ok` set before the schema check (D05 reverted) | G1, G4 |
| M12: receipt `custody_ok` set before the schema check | G2, G3 |
| M13: no carry-forward | N7, G2, N11 |
| M14: realpath pin normalisation | G6, H3, H4 |
| M15: no `code_files` dedup | G6, H4 |
| M16: any frozen code carried | F15, F17 |
| M17: verify reads the root-named path | H4 |
| M18: c2v001-style verify (M13 and M17 together) | N11, H1, H2, H3, H4 |

## Labels

**TESTED** (synthetic, both record runs):
- both review fixes (D05: G1–G6, C04, M11, M12, M15; D07: H1–H4, C05, M13, M14, M17, M18);
- carried defects cannot be forged (F14–F17, F19, M16);
- the F18 D8 boundary;
- everything c2v001 had TESTED, re-run: TEST (a), TEST (b), every M-14 code, EVALUATED_REFUSED, the MUST_FAIL attacks, AST identity, no cross-use with v003g, STAGE0 kept out of the headline;
- the mutation check.

**FORMAL** (follows from reading the code; not exercised):
- **D05 completeness.** A pinned STAGE0 file carries a STAGE0 schema string, so v003g's census (`schema == CALIBRATION_RUN_RECORD_C2V003`) cannot count it. The other v003g checks over `input_files` are additive (query manifest, region by sha256, roster dependencies) or are deduplicated (duplicate paths).
- **Carry-forward completeness.** Every state the writer can freeze for a file that will not be read again is in the carried set, so the writer's own final check always reproduces its block. The tests exercise CUSTODY_MISMATCH (H1–H3, N8), MALFORMED (N7, G1–G4), PIN_MALFORMED (N11) and NOT_SUPPLIED (N6, N9). They do not exercise TARGET_FIELDS_REFUSED.
- **Mid-freeze race.** Suppose a `custody_ok` STAGE0 file changes or vanishes between the writer's STAGE0 decision and `_pin_files`, within one `write_freeze_manifest` call. The freeze then refuses. Every v003g input file has the same exposure. The refusal happens before target access and can be recovered by re-running the freeze.
- **D8 boundary (F18).** The verifier on its own accepts a fully re-hashed forgery made after a late receipt appears. The scorer refuses it under the genuine registration. c2v001 and v003g behave the same way (v003g's D8 note).
- **Cross-use.** c2v001 and c2v002 refuse each other's manifests through the v003g `module` check.
- **The c2v001 FORMAL items stand:**
  - a byte change to a pinned STAGE0 file after the freeze is refused at score time;
  - the sensitivity roster;
  - pre-screen coverage;
  - evaluation refusals rest on the honest-producer model (A115).

**UNTESTED:**
- The real slots V003 bytes.
- The real A133 §3 rule (c) receipts. The receipt format and the absolute-path requirement are defined here. Real receipts in another format read MALFORMED, which is fail-safe.
- Rule (b) against the V006 seal entry itself.
- M-14's headline-first, no-preemption scheduling, which this module cannot see.
- Real NGC runs, rosters and scoring.
- Lexical path normalisation on any filesystem other than macOS APFS.

## Deviations and disclosures

1. **Scope beyond the two items' minimum.** Each change below was found while fixing D05/D07, is in the c2v001→c2v002 diff, and is tested and covered by a mutation:
   - verify and score read `custody_ok` files from their pinned copy by sha256, and the custody pin check runs first;
   - pins are normalised lexically, and absolute paths are required, with the new code PIN_MALFORMED;
   - the writer skips STAGE0 files that `code_files` already list.
2. **Input schemas.** The input schema names are unchanged; only the absolute-path requirement is new. `SCHEMA` and `MODULE_NAME` move to C2V002.
3. **The tests import c2v001** (unadopted, in this directory) read-only for controls C04 and C05.
4. **Synthetic fixtures carry program strings**, as in c2v001: the GL-node schema name, `galaxy: NGC3198` and the DDO154 key names. Every value is synthetic.
5. **Files created after a freeze.** The D07 tests and G6 create root files, or symlinks to them, after the freeze, at paths that were empty. Each is created exclusively; nothing is edited or deleted.
6. **No directory walk.** Each test run lists what it wrote (`FILES_WRITTEN_*.json`). The mutation driver records its own outputs. `hashes_stage0_successor_c2v002.py` hashes only explicitly named files and those lists. c2v001's `dev/` and `test_runs/` are covered transitively through `HASHES.txt`.
7. **One no-op command.** The builder was run once with OUT_PATH `/dev/stdout`. Exclusive create refused, because the path exists, and nothing was written. All commands ran in the foreground, and nothing was written outside this directory.
8. **The dev evidence** is in `dev_v002/`. It holds two module drafts (draft_02 is byte-identical to the final), the draft-01 builder and test snapshots, three dev runs, a report check and the mutation set.
