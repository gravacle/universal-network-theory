date -u: Mon Oct 19 20:24:44 UTC 2026

# runbook_v002_c2, build c2v006: root ruling A173 on OI-A1, ruling (a): every root-written record carries `schema` (root workflow build; not adopted)

**What this is.** The sixth build of the A142 build-table item "RUNBOOK_V002 and roster builder (A133), root workflow, Claude4 review". It implements one root ruling, A173's ruling (a) on Claude4's OI-A1 (0228): every root-written record carries `schema` set to its contract name, with classifier A's exact key sets. c2v005 wrote its two classifier-A records without the key, and classifier A read both honest records as defective (GATE_STATUS_LIST_DEFECT, TSR_FLAG_TABLE_MISMATCH). There is no other behaviour change.

Nothing here is adopted until root pins it and Claude4 reviews the delta (A173: inside its RUNBOOK review of A169). Nothing authorizes a launch or target access, and no production build, pass or step 7 was run. The c2v001 to c2v005 files in this folder, and `ROOT_TSR_FLAG_RECORD_V002.json`, are unchanged and superseded. Root pins only the c2v006 files and `ROOT_TSR_FLAG_RECORD_V003.json`.

## Files

| file | sha256 | what it is |
|---|---|---|
| `roster_builder_c2v006.py` | `0cc731065d1f00e1549cb7b9442c901da0a35f48c8a03d67f14701f652ad0aa2` | The builder. Commands and input schemas are as in c2v005. Changed: the two classifier-A records and their checkers (below). |
| `ROOT_TSR_FLAG_RECORD_V003.json` | `7d3c1eb915cd9a85b1a9dab388e6a3fb6c218ef3d4e8e6f2dc726bea15c54070` | V002's exact content plus `"schema": "TSR_FLAG_RECORD_C4V001"`. Written by c2v006 `tsr-record` from V001 (`61bd8a83`); the builder's pinned production record. |
| `RUNBOOK_V002_C2V006.md` | `e162db3e7bcaf348db2455aac9032ac8b0c57bb536ec97d043b6d9aad084349b` | The minimal successor of RUNBOOK c2v005: its text names the record forms (§0, §4a, §6, §6b, §7 OI-A1, §8), so it changes there and in its header. Step numbers are unchanged. |
| `test_runbook_v002_c2v006.py` | `88d79035bab8f78131a44d4f03cd209b85ca9245799d3e489441deee5d31268e` | The synthetic suite: the 149 c2v005 cases ported, and 11 new cases (Y01–Y11). |
| `test_records_c2v006/RUN1/TEST_RECORD.json`, `test_records_c2v006/RUN2/TEST_RECORD.json` | `1896a0d885bd7c182f86446709430e2ab0d2245915994f018dc66ac9c69c71d1` (both; byte-identical) | Two record runs: 160/160 each (42 MUST_PASS, 118 MUST_FAIL); `results_sha256` `588844df27ab16cf62fd96f3d4fe1905915eef37a886a1702039505b5e88bb96`. The records carry no timing field. |
| `test_records_c2v006/RUN*/work/` | not hashed | The synthetic fixtures and build outputs each run wrote (hard links of H01, H03, H04, H05, H07, H13, J02, J03, J08 inside the work directory, as in c2v005). |
| `interface_proof_c2v006.py` | `9b3772cfc6cfcb3a9f5d89497c9b855e17f3508e3474c1ca1c961f9520e6402d` | The interface proof: classifier A c4v004's own record checks on the records the builders write (below). |
| `INTERFACE_PROOF_C2V006.json` | `b3dd4964f7fd556a8ac8513b5ec876bddf8b15cdf56b289663a408e5c730d939` | Its record: verdict PASS. A second run gave the same bytes. |
| `DIFF_roster_builder_c2v005_to_c2v006.diff` | `e2a50acf35abc46b3da89157b8acf4cf9ce76aed12329b8b482f16e8584daa04` | `diff -u` of the builders (31 lines out, 46 in). |
| `DIFF_ROOT_TSR_FLAG_RECORD_V002_to_V003.diff` | `368f190fd0f001377f295ebd20b939bfc265a76c14cbe4ed80143fe2e68d5374` | `diff -u` of the records: one added line. |
| `DIFF_test_runbook_v002_c2v005_to_c2v006.diff` | `85348c9f2ec220546d983313d92b026e7fd2b32bd6544c00819da84951036d46` | `diff -u` of the suites. |
| `DIFF_RUNBOOK_V002_C2V005_to_C2V006.diff` | `c3b77d259457fb6a9055688d106f49770f714da4b4d3ba80fadc1c34f7a9dabb` | `diff -u` of the runbooks. |
| `HASHES_C2V006.txt` | — | sha256 of every file above, from bytes. |

## Running it (`python3 -I -B`)

- Run the builder as c2v005, with `roster_builder_c2v006.py`. Input schemas keep their c2v003 names. c2v006 refuses a c2v005 BUILD_RECORD (`BUILD_RECORD_OTHER_BUILDER`), so any c2v005 build is rebuilt; none exists in production.
- Suite: `python3 -I -B test_runbook_v002_c2v006.py --record-dir NEW_DIR`.
- Proof: `python3 -I -B interface_proof_c2v006.py --out NEW_FILE`. It reads the two record runs `test_records_c2v006/RUN1` and `test_records_c2v005/RUN1` and pins every input by sha256.

## The ruling and what the builder now does

The contracts are read from the bytes of `classifier_a_c4v004.py` (`e92aa30e`, A173's seal candidate): `check_gate_list` L734 (`gl.get('schema') == 'GATE_STATUS_LIST_C4V001' and set(gl) == {'schema', 'gates'}`), entries L739; `check_tsr` L679-681 (`fr.get('schema') != 'TSR_FLAG_RECORD_C4V001' or set(fr) != {'schema', 'target_free', 'rule', 'failing_ring_ordinal', 'ntest_compare_pin', 'n1_record_pin', 'gl_node_record_pin', 'flags'}`), flags L699. The builder's constants use these names and key sets verbatim.

| record | c2v005 | c2v006 | tests |
|---|---|---|---|
| gate-status list `GATE_STATUS_LIST.json` (FULL build) | `{gates}`; `check-gate-list` refused a `schema` key (c2v005 X06) | `{schema: "GATE_STATUS_LIST_C4V001", gates}`. `check-gate-list` (`_a_gate_list_problem`) accepts exactly `{schema, gates}` with that schema string, and refuses a missing schema, any other schema value, or an extra key: `GATE_STATUS_LIST_DEFECT` | X01, X06 (flipped), M07, Y02; MUST_FAIL Y04 (no schema: the c2v005 form), Y05 (six wrong values), Y06 (extra key) |
| TSR flag record | V002 `c9d8ab45`: the seven keys, no `schema` | V003 `7d3c1eb9`: `schema` plus the seven keys. `tsr-record` (`tsr_record_v003`, renamed from `tsr_record_v002`) writes it from V001; `PRODUCTION_TSR['flag_record_sha256']` is V003; `tsr-check` accepts exactly the eight keys with that schema string and refuses a missing schema, any other schema value, or an extra key: `TSR_FLAG_TABLE_MISMATCH`. `seal-check` refuses V002 as the sealed record. | X02, T01, T08, Y03; MUST_FAIL Y07 (no schema), Y08 (V002 through the `tsr-check` command), Y09 (four wrong values), Y10 (extra key), Y11 (seal names V002) |
| rosters | `schema` `ROOT_ROW_REGISTRATION_ROSTER_CX3V001` | unchanged (A already checks it) | — |

No other file the builder writes is a classifier A input. The builder writes two of A's 17 bundle roles; X07 checks the split.

**Builder diff, in code (everything else is docstrings and comments):** `BUILDER_NAME`; `A_GATE_LIST_KEYS = ('schema', 'gates')`; `A_TSR_KEYS` gains `'schema'`; `PRODUCTION_TSR['flag_record_sha256']` is V003; `a_gate_status_list` writes `schema`; `_a_gate_list_problem` also compares the schema value; `tsr_record_v003` writes `schema`; `tsr_check` also compares the schema value; the CLI calls `tsr_record_v003`; and one text string, below.

## Interface proof (`INTERFACE_PROOF_C2V006.json`, verdict PASS)

Classifier A c4v004 is loaded read-only from its verified bytes (exec, no bytecode), and its own `Run.check_gate_list` and `Run.check_tsr` are called directly. Everything runs on synthetic fixtures; `classify_bundle` is not run.
- **Gate lists, c2v006.** All 67 lists that the c2v006 record run RUN1 wrote (every FULL build of the suite) are accepted with no stop of any kind. The check runs over each build's own six rosters, read through A's sha-verified `read_pinned`. A echoes each list as its `gate_status_list` output.
- **Gate lists, c2v005.** All 62 lists that the c2v005 record run RUN1 wrote are refused, `GATE_STATUS_LIST_DEFECT` ("gate-status list missing or malformed"). Each of them, with only `"schema": "GATE_STATUS_LIST_C4V001"` added in memory, is accepted with no stop. So the missing key was the whole mismatch.
- **Agreement on eight variants of one list** (as written; no schema; `GATE_STATUS_LIST_C4V002`; lower case; `TSR_FLAG_RECORD_C4V001`; null; an extra key; schema without gates). c2v006's checker agrees with A on all eight. c2v005's disagreed on exactly two: the honest list and its own form.
- **TSR flag record.** A's `check_tsr` accepts V003 with no stop. It fires `TSR_FLAG_TABLE_MISMATCH` ("flag record missing or malformed") on V002 and on four V003 variants (`UNT_ROOT_TSR_FLAG_RECORD_C2V001`, lower case, null, an extra key). The other carriers `check_tsr` reads are in-memory stand-ins built from A's own constants, so only the flag record can fire: the compare (6f095f64, failing TRUNCATION_SHAPE ring 15 only), the support record (ring 15 bounds) and the manifest's `input_files` (the four shas). The pinned compare, N1 and node files are not opened.
- c2v006's `tsr_record_v003` on V001 gives V003's bytes, and V003 is V002 plus the key.

## Ported tests

All 149 c2v005 cases are ported in order. 147 keep their ids, expectations and observed codes, checked against the c2v005 record. The two that change:
- `X02_tsr_flag_record_V002_...` is now `X02_tsr_flag_record_V003_is_classifier_A_TSR_FLAG_RECORD_C4V001_and_projects_V001`. It is still MUST_PASS, and it asserts the eight keys.
- `X06_gate_list_carrying_a_key_outside_A_schema_refused` (MUST_FAIL `GATE_STATUS_LIST_DEFECT`) is now `X06_gate_list_carrying_the_schema_key_accepted_A173` (MUST_PASS). Its list, A's list plus `schema`, is now byte for byte the builder's own list. A key outside A's schema is Y06.

Ported bodies updated for the new form: X01 asserts `{schema, gates}`, and SynTsr's synthetic flag records carry `schema` (used by T02–T04, T06, T07). The production record the suite reads is V003, used by T01, T05, T08, T09, X02 and the S cases. V002 is read only by Y03, Y08 and Y11, and pinned in the record.

## Development checks (scratchpad `rbv006c2/`, not record runs)

- **The c2v006 suite on the c2v005 builder's bytes: 141/160.** It fails S01, S02, S07, T01, T02, T04, T08, T09, X01, X02, X06, Y01–Y04, Y06–Y08 and Y11. Y05, Y09 and Y10 pass there too, because c2v005 refuses every record that has a `schema` key.
- **8 mutants of the c2v006 change, 8 killed.**
  - schema value unchecked: on the list (Y05), on the flag record (Y09);
  - schema optional: on the list (Y04), on the flag record (Y07, Y08);
  - extra keys allowed: on the list (Y06), on the flag record (Y10);
  - the list written without schema (M07, X01, X05, X06, Y02, Y04–Y06);
  - the production pin left at V002 (S01, S02, S07, T01, T08, X02, Y01, Y03, Y11).

## CHOICES this build made that the ruling did not force (root confirms or replaces each)

C1–C45 are carried from c2v005.
- **C46. V003 replaces V002 as the builder's production constant**, so `tsr-check` and `seal-check` stop on V002. This follows from "supersedes V002 for the seal" (A173); the `input_files` item and the seal role line name V003.
- **C47. `tsr_record_v002` is renamed `tsr_record_v003`.** The function now writes V003. The command name `tsr-record` and its input schema `TSR_RECORD_INPUT_C2V003` are unchanged.
- **C48. Check order.** The schema value is compared after the exact key set, in the same check, with the same code. Both checkers say "not the <contract> schema (exactly …, schema <contract>)". In `check-gate-list` this runs before the binding to the build; in `tsr-check`, after the pinned-sha comparison, as in c2v005.
- **C49. A text correction.** In `A_INPUTS_NOT_PRODUCED` and RUNBOOK §6b, root's STAGE0 status record is now named by A c4v004's contract name, `STAGE0_STATUS_RECORD_C4V003` (A L82 `STAGE0_RECORD_SCHEMA`). c2v005 wrote C4V001. This is a string only; the builder writes no such record. Under A173 (a), root writes it with `schema` set to that name.

## NOTEs (not blocking under A115, recorded)

- **A169's premise.** A169 recorded the c2v005 records as "in classifier A's schemas". They were not, as Claude4 0228 showed, and A173 rules the fix. The c2v005 build did not open classifier A's code (its README says so); the interface proof is the cross-check that was missing.
- **Hex case.** `_a_gate_list_problem` requires lower-case `gate_sha256`, while A accepts either case (`is_hex64_ci`, L739). The builder only ever writes lower case, so no honest record is affected. The builder is stricter than A here, which is unchanged since c2v003.
- **The other root-written records** (`PHASE_INPUTS_C4V001`, `STAGE0_STATUS_RECORD_C4V003`, `PHASE2_COMMITMENT_STATUS_C4V001`, `FALLBACK_RECORD_C4V001`, `KEY_FIELD_MAP_C4V001`) are root's, not this builder's. Each must carry `schema` under A173 (a). No tool here writes or checks them.
- Carried from c2v005: C43 (results inside another call's run directory), A157 and the gate-status list (a production FULL build lists only `gate_documents`), and the G28 ledger root.

## Gaps and UNTESTED

- **Root rulings this build raises:** none new. Root confirms C46–C49. G1, G2 residual, G3, G7, G8–G10, G13–G21 and G24–G28, and G29 item (4), are carried open from c2v005.
- **UNTESTED:** classifier A's full run (`classify_bundle`) on a complete bundle that pins `GATE_STATUS_LIST.json` and V003. The record checks themselves are TESTED by the interface proof; the other 15 bundle roles need real records. The deciding test is A's prescore mode on the first real bundle. Everything else UNTESTED in c2v005 stays so (RUNBOOK §8).

## Deviations (disclosed)

- **Drafts in the scratchpad.** The builder, suite, record, proof, runbook and this README were generated in `/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/rbv006c2/`, by counted exact replacements on the c2v005 bytes (`gen_builder2.py`, `gen_tests.py`, `gen_runbook2.py`). The development run, the mutation check and the c2v005-bytes run happened there. Each published file was written once, by exclusive create. The record runs and the proof ran from this folder.
- No existing file in this folder was edited.
- **Opened:**
  - V006 sections A169 and A173 only, by their headings (V006 sha at reading `8536ab73`);
  - Claude4 0228 (`d6679553`);
  - the c2v005 builder, suite, RUNBOOK, README, HASHES, record and V002;
  - in `classifier_a_c4v004.py`: L1-120 (docstring and constants), L196-530 (input roles, strict loader, helpers, `Run`, the bundle loader, `stop`, `check_seal`), L640-770 (`check_tsr`, `check_gate_list`), L1386-1395, L2430-2500 and L2600-2637, and a grep for its `schema` comparisons (L434, L591, L1391, L2000, L2495).
  - The suite and `tsr-check` read the compare, N1 and node files the TSR records pin, as in c2v005.
- **Not opened:** any NGC3198 target, velocity, sigma or observed file, the slots, the program query manifest, run trees, ~/.codex, and the rest of classifier A.
