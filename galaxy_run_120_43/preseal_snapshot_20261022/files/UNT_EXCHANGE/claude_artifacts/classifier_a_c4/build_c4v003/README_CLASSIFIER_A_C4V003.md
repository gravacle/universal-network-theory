# Classifier A (lane Claude4), build c4v003: the M-12 Implementation A for the miss-reading prereg r3a, successor of c4v002

**What it is.** `classifier_a_c4v003.py` is the mechanical, target-blind classifier of ROOT_ITEMS M-12, Implementation A, for the r3a text of record in `basis/` (`PREREG_MISS_READING_R3A.md` `4242ee15…`, `ROOT_ITEMS_R3A.md` `ed9f5c5b…`, `CLAUSE_SOURCE_MAP_R3A.md` `eb578454…`; shas in `BASIS_SHAS_C4V003.txt`), with root's rulings of M-1 to M-16 as adopted in A142. It succeeds `classifier_a_c4v002.py` (`a11ae7b9…`, verified 0 BLOCKING with S1 open). It binds:
- the phase1 `band` and `agree` encodings from the bytes of the two tools the seal may pin: `phase1_c2v002.py` `d64351ec…` and `phase1_c2v003b.py` `7d891ff7…` (A144, A149, v003b's values custody; root dispatches 0724/0725, 0732, 0733);
- the STAGE0 successor `prediction_freeze_c2v003g_stage0_c2v002.py` `d260ee30…` through the frozen manifest's `stage0_status` block, when the seal pins it (A154 with erratum E_A154_1; dispatch 0726).

Classifier B (Codex1) is built separately; nothing of B or of its predecessor was opened.

**Status.** Built and suite-tested on synthetic, target-free inputs only; never run on a real manifest or score. Record run `SUITE_RESULTS_C4V003.json` (classifier `394a8b61…`): **409 cases, 409 pass** (206 c4v001 regression cases, 92 c4v001 verifier cases, 64 c4v002 cases, 47 new cases). The open choices are listed below with the value classifier A uses; each is raised, not silently decided.

**Files** (sha256 in `HASHES_C4V003.txt`):

| file | role |
|---|---|
| `classifier_a_c4v003.py` | the classifier (stdlib only, Python 3.12) |
| `run_suite_c4v003.py` | runs the four case sets (R1, R2, N2, N3), writes the results file |
| `SUITE_RESULTS_C4V003.json` | the record run |
| `suite/case_defs_c4v003.py`, `suite/build_suite_c4v003.py` | the 47 new case definitions (hand expectations, clauses, derivations) and their generator (a copy of c4v002's with the changes its docstring lists) |
| `suite/SUITE_INDEX_C4V003.json`, `suite/cases/<id>/`, `suite/common/` | the new cases (`BUNDLE.json`, inputs, `EXPECT_SPEC.json`, `EXPECTED_OUTPUT.json`); common = byte copies of c4v002's common files plus `STAGE0_SUCCESSOR_C2V002_d260ee30.py.txt`, a byte copy of the successor module (a pin target only, never imported) |
| `regression_c4v001/`, `regression_verify/`, `regression_c4v002/` | byte copies (cp -R -n) of c4v002's three case sets: R1 with its old basis, R2, and c4v002's `suite/` with c4v002's basis `a8c8686c` beside it (the N2 cases seal it by relative path) |
| `regression_conv_r2/` | the carried regression inputs (`tools/convert_regression_c4v003_r2.py`): per case `BUNDLE_C4V003.json` (absolute paths) and, where the STAGE0 contract changed, the converted record or successor manifest, plus `CONVERSION_C4V003.json` |
| `regression_conv/` | the superseded first conversion (r1; missed R1 T091), kept, not used |
| `tools/run_fenced_c4ep1.py`, `tools/fence_c4v003.py` | the fenced runner (EXPECTED_BUILD and its refusal message set to this folder; c4v002 N3 fixed) and its fence (`175b995b…`, byte copy) |
| `tools/convert_regression_c4v003.py`, `tools/convert_regression_c4v003_r2.py`, `tools/dump_outputs_c4v003.py` | the regression conversion (r1 superseded, r2 used) and a review aid |
| `work/` | the classifier drafts (`cls_c4v003_d01.py`, `cls_c4v003_d02.py` = the final bytes), dev runs `run01`–`run03`, `outs_d02/`, the copy checks |
| `PARTIAL.md` | the append-only progress log |

## How to run

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  taskpolicy -b <codex python3> -I -B B/tools/run_fenced_c4ep1.py B/classifier_a_c4v003.py BUNDLE.json OUT.json
```
`OUT.json` is created exclusively. The importable entry point is `classify_bundle(bundle_path) -> bytes`. The suite: `run_suite_c4v003.py RESULTS.json [--classifier PATH] [--freeze] [--sets R1,R2,N2,N3]`.

## CHANGES against c4v002

Behaviour:
1. **Phase1 pin switch (brief item 1).** `phase1_tool` must be `d64351ec…` with module `phase1_c2v002`, or `7d891ff7…` with module `phase1_c2v003b` (the MODULE literal, L99). Any other sha (385b287c, c4v002's v003a pin, included), or a module name not the sha's, is `PHASE1_TOOL_PIN_DEFECT` (band column and item 11 only, never NOT_READ).
2. **The v003b `agree` encodings (brief item 1).** From the bytes and the DIFF (`fd095be9`, confirmed by my own diff of the two files): v003b changes v003a at four sites only (docstring, MODULE, `cmd_at0b` +1 statement, `cmd_at1` +4 lines that only refuse). So every v003a binding of c4v002 is kept unchanged (AT1 eleven-key failing entries, flag pairs, twelve-key `reported`, extents, single point, AT0B `members_sha256`; `cmd_band`, `band_rows`, `cmd_at0a` untouched, so the L1 and AT0A records differ from v002 only in `module`). New: an AT0B record under `7d891ff7` must carry `values_sha256`, 64 lower-case hex (`res['values_sha256'] = a.values_sha256.lower()`, written on every AT0B record, PASS or AGREEMENT_DEFECT; the value is the sha `read_pinned` verified against the values bytes). When the AT-0b record is the record (F2), item 11 prints it as `at0b_values_sha256` beside `at0b_members_sha256`. A record without it, or with any other form, is `AGREE_RECORD_DEFECT` with the word `AT0B_VALUES_SHA256`. The at1 values check (AT-0b's `values_sha256` equals the L1's) is enforced by at1 refusing (no record), as the members check is (OC-25, OC-47).
3. **STAGE0 through the successor (brief item 2; A154, E_A154_1).** In a Phase 2 whose seal pins a STAGE0 successor (the bundle's `sealed.stage0_successor` non-null), Phase 2 runs under it (M-5 addition 2), and the STAGE0 status is read from the frozen manifest's `stage0_status` block, in the module's own schema (`STAGE0_BLOCK_KEYS`, `STAGE0_MEMBER_KEYS`, d260ee30 L3541–3550). Binding conditions (each failure: the block is a defective field of the STAGE0 alternative, `TWIN_INPUT_DEFECT`, stop `FIELD_DEFECT_ALTERNATIVE`; C-1.1 map, F8):
   - the sealed successor sha is `d260ee30…` (`STAGE0_SUCCESSOR_PIN_NOT_BOUND`);
   - the manifest schema is `FREEZE_MANIFEST_C2V003G_STAGE0_C2V002` (`MANIFEST_SCHEMA_NOT_SUCCESSOR`);
   - the block has exactly the module's keys and member-row keys; `alternative` STAGE0_GRID_OUTER, `module` `prediction_freeze_c2v003g_stage0_c2v002`; `successor_module_sha256` equals the sealed sha (the module writes the sha of its own bytes); the status-record pin and member receipt pins are well formed; a FINISHED member is custody_ok;
   - its members are the frozen PRIMARY members, `(member_id, log_index)` in order (M-14 ruling: one STAGE0 call per PRIMARY member; `_stage0_members_of`);
   - its facts satisfy the receipt rule as the module applies it: `finished` only with terminal status FINISHED and a receipt time; `before_step4` set exactly when finished and equal to (receipt time ≤ step-4 start); `rule_a_receipts_finished` = members non-empty and all finished; `rule_b_successor_sealed` = the record named the module's own sha; `receipts_before_step4`; reasons `STAGE0_RECEIPT_NOT_FINISHED`, `NO_SEALED_SUCCESSOR`, `RECEIPTS_AFTER_STEP4` in that order; reading NOT_EVALUATED with reasons, else EVALUATED_REFUSED on a receipt or evaluation refusal, else EVALUATED; evaluation refusals only where the rule holds; `post_score_exploratory` iff RECEIPTS_AFTER_STEP4; phase null (no root record at the freeze) or PHASE_2;
   - root's separate STAGE0 record, if the bundle supplies one, equals the block's exact projection (`STAGE0_STATUS_RECORD_NOT_THE_BLOCK_PROJECTION`).

   The printed status is then the block's reading and reasons. Without the successor pin, Phase 2 keeps v003g and reads root's separate record, whose contract is now the exact projection of the block (change 4).
4. **The STAGE0 status-record contract is rewritten as an exact projection of the block (brief item 2; contract change C7).** See the contract below. Without the successor, (b) fails by C-6.3, so the record must say `rule_b_successor_sealed: false` and the reading is always NOT_EVALUATED_BEFORE_FREEZE with NO_SEALED_SUCCESSOR (plus STAGE0_RECEIPT_NOT_FINISHED or RECEIPTS_AFTER_STEP4 where the record's facts give them). `result_first_available_utc` is gone (the block has no such field; the module carries RECEIPTS_AFTER_STEP4 as a FINISHED receipt written after the start).
5. **Manifest schema per phase (brief item 2; M-5 addition 2).** The frozen manifest's `schema` must be the one of the module the seal names for the phase: `FREEZE_MANIFEST_C2V003G` (v003g L49) for Phase 1 and for a Phase 2 without the successor; `FREEZE_MANIFEST_C2V003G_STAGE0_C2V002` (d260ee30 L64) for a Phase 2 with it. Any other schema (the superseded `…_STAGE0_C2V001` string included, E_A154_1) is `FIELD_DEFECT_OUTSIDE_ROWS` (every other; OC-36). Not checked when the phase is unknown. c4v002 did not read the schema; every regression manifest carries v003g's.
6. **Basis row T3.** An envelope-row field defect blanks NEAR and N(Z) only where the row is tier-MISS: a HIT, INVALID_AS_MISS or LATE-gate row prints `near: false` whatever its envelope row reads, and N(Z) prints unless a tier-MISS row of the zone is blanked. c4v002 blanked NEAR on the row whatever its tier (its OC-35). No regression output had an envelope defect on a non-MISS row (only T092, T094, V32, all MISS rows), so no regression output changed.
7. **Basis row D6.** A missing agree record (no AT-1 record because at1 refused after AT-0a and AT-0b passed) is a defective record. c4v002 already read it so (load error `NOT_SUPPLIED`: item 11 NOT_AVAILABLE, AGREE_RECORD_DEFECT, Phase 1 keeps its PROVISIONAL label, Phase 2 the score of record); no code change. Cases B09, B10.
8. **R-DRIFT's code list for a STAGE0 defect** is the status's own reason: `STAGE0_STATUS_RECORD_DEFECT` (record path, as before) or `STAGE0_STATUS_BLOCK_DEFECT` (block path).
9. **c4v002 notes.** N1: kept (a scored Phase 1 without `phase1_header` reads PHASE_MISMATCH, class ALL); it is now listed as a choice classifier B must share (OC-46). N3: the runner's refusal message names build_c4v003.

Contracts. Root adopted c4v001's contracts (0720); c4v002 changed them by C1–C5 (not yet re-adopted, per c4v002 verifier N1). The schema strings of the bundle and output are unchanged. This build's contract changes are exactly:
- **C6** `phase1_tool` (bundle): `d64351ec…`/`phase1_c2v002` or `7d891ff7…`/`phase1_c2v003b` only (change 1).
- **C7** the STAGE0 status record: `STAGE0_STATUS_RECORD_C4V001` is replaced by `STAGE0_STATUS_RECORD_C4V003`, the exact projection of the successor's block (change 4); in a successor-mode Phase 2 the record is optional and, if supplied, must equal the projection of the frozen block (change 3).
- **C8** the freeze manifest (role `freeze_manifest`): its `schema` is checked per phase (change 5); in successor mode its `stage0_status` block is read (change 3).
- **C9** the output: `at0b_values_sha256` in item 11 (change 2); the STAGE0 status dict (`header.stage0_status`, `stage0`) gains `source` and `post_score_exploratory` and loses `result_first_available_utc`; a block defect prints `{status: NOT_AVAILABLE, reasons: [STAGE0_STATUS_BLOCK_DEFECT], source, defect: <word>}` (a record defect prints as in c4v002); R-DRIFT's code list for a STAGE0 defect (change 8); `near: false` on non-MISS rows under an envelope defect (change 6).

## The input bundle (`CLASSIFIER_A_BUNDLE_C4V001`)

Unchanged from c4v002 except where marked. One strict JSON object with exactly these keys. Every path may be absolute or relative to the bundle's folder. Every pin is `{"path": str, "sha256": 64 lowercase hex}`; the classifier hashes the bytes and refuses to parse an input whose bytes differ (the input then counts as missing, in its role's map class). A malformed bundle refuses the run.

| key | content |
|---|---|
| `schema` | `CLASSIFIER_A_BUNDLE_C4V001` |
| `mode` | `score` or `prescore` |
| `inputs` | an object with exactly the 17 roles below, each a pin or `null` |
| `rosters` | `{alternative name: pin}`: the v003g row-registration rosters (`ROOT_ROW_REGISTRATION_ROSTER_CX3V001`) |
| `sealed` | `{"text": pin, "classifier": pin, "tsr_flag_record_sha256": hex, "stage0_successor": pin or null}`. A non-null `stage0_successor` is the seal entry's successor pin: it puts Phase 2 under the successor and is bound only at `d260ee30…` [C7, C8] |
| `phase1_tool` | `{"sha256": hex, "module": str}` or null: exactly `d64351ec…`/`phase1_c2v002` or `7d891ff7…`/`phase1_c2v003b` [C6] |
| `module_sha256` | the freeze module sha the seal entry pins for the phase (header only; not checked, OC-45) |

**Roles** (`inputs`), and what a defect in each does:

| role | content | needed | defect class |
|---|---|---|---|
| `phase_inputs` | root-written, schema below | always | PHASE_MISMATCH ("every other") |
| `freeze_manifest` | the v003g freeze manifest, or in successor mode the successor's (schema checked per phase [C8]) | always | FIELD_DEFECT_OUTSIDE_ROWS ("every other"); its `stage0_status` block: the STAGE0 alternative (TWIN_INPUT_DEFECT) |
| `score` | the `score_after_freeze` output | score mode | FIELD_DEFECT_OUTSIDE_ROWS |
| `slots` | `query_block.rows[]` of `{query_id, Rad_text, Rad_unit}` | always | ZONE_TABLE_MISMATCH |
| `gate_status_list` | root-written | always | GATE_STATUS_LIST_DEFECT |
| `tsr_flag_record` | root-written | always | TSR_FLAG_TABLE_MISMATCH (SEAL_SHA_MISMATCH if its bytes miss the sealed sha) |
| `tsr_support_record` | `UNT_ROOT_TSR_SUPPORT_CX3V001` | always | TSR_FLAG_TABLE_MISMATCH |
| `ntest_compare` | `6f095f64…` | always | TSR_FLAG_TABLE_MISMATCH |
| `stage0_status` | root-written, `STAGE0_STATUS_RECORD_C4V003` [C7] | Phase 2 without the successor; optional with it (then it must be the block's projection) | the STAGE0 alternative reads TWIN_INPUT_DEFECT (F8) |
| `commitment_status` | root-written | Phase 2 | EXPLORATORY with COMMITMENT_STATUS_DEFECT; never NOT_READ |
| `agree_record` | the A133 `agree` record (F2; encodings below) | Phase 2 | item 11 NOT_AVAILABLE (AGREE_RECORD_DEFECT); a missing one included (D6); never NOT_READ |
| `phase1_classification` | classifier A's own Phase-1 output | Phase 2 | cross-phase items NOT_AVAILABLE; never NOT_READ |
| `l1_record` | the pinned `band` command's L1 (`PHASE1_L1_C2V001`) | Phase 1 | the Phase-1 band column only |
| `c3_record` | the M-13 record | P8 report | that half NOT_AVAILABLE |
| `root_disclosures` | any JSON object | header | echoed |
| `fallback` | root-written | under the fallback | item 10 NOT_AVAILABLE |
| `field_map` | key-only field map | only if pinned | not applied |

### Root-written input contracts

Unchanged from c4v002 (`PHASE_INPUTS_C4V001` with C3, `GATE_STATUS_LIST_C4V001` with C4, `TSR_FLAG_RECORD_C4V001`, `PHASE2_COMMITMENT_STATUS_C4V001`, `FALLBACK_RECORD_C4V001`, `KEY_FIELD_MAP_C4V001`, the M-13 C3 fields), except:

- **STAGE0 status record (`STAGE0_STATUS_RECORD_C4V003`, Phase 2) [C7].** Exactly `schema` plus the projected keys of the successor's frozen `stage0_status` block, with the block's names and encodings: `phase` (null or `PHASE_2`), `sealed_successor` (null or `{module_sha256: 64 lower-case hex, source: str}`), `step4_start_utc` (`date -u` time or null), `members` (a list of `{log_index, terminal_status, written_utc, finished, before_step4}`, each the block's member row restricted to those keys), `rule_a_receipts_finished`, `rule_b_successor_sealed`, `receipts_before_step4`, `receipt_refusals`, `evaluation_refusals`, `reading`, `reasons`, `post_score_exploratory`. The facts must satisfy the receipt rule (change 3). With the successor pinned, the record is the block's projection verbatim. Without it, root writes the same form for a Phase 2 under v003g: `sealed_successor` null or not the seal's, `rule_b_successor_sealed: false`, and rule (a) over the registered STAGE0 members, which hold vacuously over an empty list (STAGE0 is not registered for Phase 2; OC-41). The default no-successor record is `{phase: PHASE_2, sealed_successor: null, step4_start_utc: <time>, members: [], rule_a_receipts_finished: true, rule_b_successor_sealed: false, receipts_before_step4: true, receipt_refusals: [], evaluation_refusals: [], reading: NOT_EVALUATED_BEFORE_FREEZE, reasons: [NO_SEALED_SUCCESSOR], post_score_exploratory: false}`. Not to be confused with the module's own input record `STAGE0_STATUS_RECORD_C2V001`, which root writes before the freeze for the successor to read.
- **The A133 `agree` record** (F2): as in c4v002, with the pinned sha now `d64351ec` (v002 encodings, unchanged) or `7d891ff7` (the v003a encodings c4v002 bound from 385b287c, unchanged, plus AT0B `values_sha256`, 64 lower-case hex, required) [C6].

**What is read from the freeze files** (M-5): as in c4v002, plus the manifest's `schema` [C8] and, in successor mode, its `stage0_status` block and the `(member_id, log_index)` of its `members[]` [C8]. The score output's own `stage0_status` echo is not read (OC-44).

## The output (`CLASSIFIER_A_OUTPUT_C4V001`)

As in c4v002 (`classifier` is `classifier_a_c4v003`), with C9: item 11 adds `at0b_values_sha256` (v003b AT0B record only); the STAGE0 status in `header.stage0_status` and `stage0` is, in Phase 2, `{status, reasons, source (STAGE0_STATUS_RECORD_C4V003 or FREEZE_MANIFEST_STAGE0_STATUS_BLOCK), phase2_step4_start_utc, receipt_times_utc (one per member, null where no receipt), post_score_exploratory}`; a block defect prints `{status: NOT_AVAILABLE, reasons: [STAGE0_STATUS_BLOCK_DEFECT], source, defect: <word>}` and its stop detail names the word; a record defect prints as in c4v002 (`{status: NOT_AVAILABLE, reasons: [STAGE0_STATUS_RECORD_DEFECT]}`).

## Rule-to-function map

As in c4v002 (its README table), with these rows changed or added:

| text rule (section, tag) | function(s) |
|---|---|
| Phase-1 band column (C-1.1, M-16); the pin switch (A142 item 4; brief item 1) | `band_column`, `_tool_module`, `PHASE1_TOOLS` |
| item 11, the `agree` record (C-1.1 map, F2, D6; A144, A149, v003b V1) | `agreement`, `parse_agree` (AT0B `values_sha256`), `_flag_pair_ok`, `_extent_list_defect`, `_reported_v003a_defect`, `_p1_ok` |
| STAGE0 receipt rule and statuses (C-6.3, M-14, F8, F12); the successor binding (M-5 addition 2, A154) | `stage0_status`, `_stage0_block_facts`, `_stage0_facts`, `successor_mode`, `stage0_block`, `prepare_alternatives` |
| freeze module per phase (M-5 addition 2; A154, E_A154_1) | `check_manifest_schema` |
| NEAR on tier-MISS rows under an envelope-row defect (C-1.1 map, T3) | `score_output` (NEAR block), `check_envelope` |

## Open choices (raised, not decided; the value used and the pinning case)

Carried from c4v002 with their status: OC-01–OC-34 as in the c4v002 README (OC-18 and OC-25 now read for v003b: the AT1 record still carries neither the members nor the values sha, so both custody matches are enforced by at1 refusing). **OC-35 is resolved by T3** (change 6; T3A–T3C).

New in c4v003:

| id | question | classifier A uses | case |
|---|---|---|---|
| OC-36 | the map class of a frozen manifest whose `schema` is not the sealed module's for the phase (the text and A154 say the successor schema "must be accepted", not what another reads) | FIELD_DEFECT_OUTSIDE_ROWS (every other); in successor mode the block also reads TWIN_INPUT_DEFECT | S10, S11, S12, R1 T087 |
| OC-37 | a sealed successor pin other than d260ee30 | the block is not bound: STAGE0 TWIN_INPUT_DEFECT (`STAGE0_SUCCESSOR_PIN_NOT_BOUND`); SEAL_SHA_MISMATCH still checks its bytes | S13, R1 T087 |
| OC-38 | is root's separate STAGE0 record required in successor mode? | optional; if supplied it must equal the block's exact projection | S14, S15 |
| OC-39 | rule (b): the text's "pinned in the seal entry" vs the module's "root's record names this module's sha" | the block's own reading is printed (with the successor pinned, a block can read NO_SEALED_SUCCESSOR when root's record named another sha) | S05 |
| OC-40 | the block's `phase` | null (no root record at the freeze: an honest block) and PHASE_2 accepted; PHASE_1 in a Phase-2 run is a defect | S07, S22 |
| OC-41 | the no-successor record: who are the registered members; the projected member keys | rule (a) holds vacuously over an empty list (reasons NO_SEALED_SUCCESSOR only, as c4v002); member keys `log_index, terminal_status, written_utc, finished, before_step4` | S19, S20, S21, every N3 Phase-2 default |
| OC-42 | the registered STAGE0 members in successor mode | the frozen PRIMARY members, `(member_id, log_index)` in order | S16 |
| OC-43 | how far the block is checked | key sets, module, self-sha, pins' form, members, and the receipt rule recomputed from the block's own facts; the `rule` text and `diagnostics` contents are not checked | S08, S09, S17 |
| OC-44 | the score output's `stage0_status` echo | not read (M-5 lists no such score field) | — |
| OC-45 | `module_sha256` in successor mode | header only, as before (not checked against d260ee30) | — |
| OC-46 | c4v002 N1: a scored Phase 1 without `phase1_header` | PHASE_MISMATCH, class ALL (NOT_READ); **classifier B must share it** | c4v002 VF4A (N2) |
| OC-47 | v003b's values custody in item 11 | `values_sha256` required on every v003b AT0B record (lower-case, 64 hex) and printed; its match with the L1's is enforced by at1 refusing, not checkable from the record | B04–B08 |
| OC-48 | the word for a missing agree record (D6) | `NOT_SUPPLIED` (load error) in `agree_record_defect`; a passing AT-0b record supplied instead reads `AT0_RECORD` | B09, B10 |
| OC-49 | RECEIPTS_AFTER_STEP4 | the block's encoding: a FINISHED receipt written after the recorded start; the text's "a result first available after step 4" has no field | S03, R1 T051 (converted) |

## Discrepancies between the bytes and root's descriptions

phase1_c2v003b (`7d891ff7`):
- **No discrepancy** with the brief: v003b = v003a + AT0B `values_sha256` + at1 VALUES refusal; MODULE `phase1_c2v003b`. The DIFF file `fd095be9` equals my own diff of the two files.
- The README adds one rule the brief does not name: **at1 accepts only an L1 whose module is phase1_c2v003b** (custody). The classifier's band column already requires the L1 module to be the pin's (B17).
- The L1's own `values_sha256` is written as given (band does not lower-case it), while AT0B lower-cases its value; at1 lower-cases both. The classifier reads neither the L1's nor the match (OC-47).
- The AT1 record carries neither `values_sha256` nor `members_sha256`: the custody chain is visible in item 11 only when the AT-0b record is the record.

STAGE0 successor (`d260ee30`):
- **Schema strings.** A154's body names `FREEZE_MANIFEST_C2V003G_STAGE0_C2V001`; the bytes (L64) and erratum E_A154_1 say `…_C2V002`, MODULE_NAME `prediction_freeze_c2v003g_stage0_c2v002` (L66). Classifier A binds the bytes (S11 refuses the C2V001 string).
- **"Its README field map".** README_STAGE0_SUCCESSOR_C2V002 gives the field map only as changes against c2v001's map; the full block key sets come from the bytes (`STAGE0_BLOCK_KEYS`, `STAGE0_MEMBER_KEYS`), which classifier A binds.
- **Rule (b).** The text: the successor is pinned in the seal entry. The module: root's status record names the module's own sha (it cannot see the seal). OC-39.
- **RECEIPTS_AFTER_STEP4.** The text: a result that first becomes available after step 4 begins. The module: a FINISHED receipt written after the recorded start. No block field carries a later result time. OC-49.
- **Registered members.** The text: every registered STAGE0 member. The module: every PRIMARY member, with `bool(members)` required for (a). OC-41, OC-42.
- **"Root writes [the separate record] as an exact projection of the frozen block."** Without the successor there is no frozen block (v003g writes none), so in that case the record is the projection's form, not a projection of anything. And the name `STAGE0_STATUS_RECORD` is also the module's input record (`STAGE0_STATUS_RECORD_C2V001`, written before the freeze). Classifier A's record schema is `STAGE0_STATUS_RECORD_C4V003` to keep the two apart.

## The suite

Four sets, all synthetic and target-free. `SUITE_RESULTS_C4V003.json` (classifier `394a8b61…`): 409 cases, 409 pass.

| set | cases | pass | failing | what is compared |
|---|---|---|---|---|
| R1 c4v001 regression (`regression_c4v001/suite/cases`) | 206 | 206 | none | the c4v001 hand spec and EXPECTED_OUTPUT bytes, carried to c4v002 by c4v002's X1–X3 and its four overrides, then by Z1–Z4; the output must equal those bytes (T087 by its declared spec and every unchanged top-level key) |
| R2 c4v001 verifier cases (`regression_verify/cases_r3`) | 92 | 92 | none | the verifier's checks (X2-carried); informational: its recorded c4v001 outputs carried by X1–X3, Z1–Z3 equal the c4v003 outputs except V71 and V85 (the c4v002 V-F1/V-F3 fixes) |
| N2 c4v002 suite (`regression_c4v002/suite/cases`) | 64 | 64 | none | the c4v002 hand spec (latest revision) and the c4v002 frozen bytes, carried by Z1–Z4 |
| N3 new (`suite/cases`) | 47 | 47 | none | hand spec written before any run, then the frozen bytes |

Every R1, R2 and N2 case ran on its carried bundle (`regression_conv_r2/<set>/<id>/BUNDLE_C4V003.json`): kinds NONE 45 (paths only), RECORD 287 (the C4V001 record rewritten as the C4V003 projection from the same facts, with no anomaly: c4v002's RECEIPTS_AFTER_STEP4 equals the block rule on every case), SUCC 28 (a stand-in successor pin with a v003g manifest, carried to a successor manifest with a block and the d260ee30 pin; anomalies, all declared: the second PRIMARY member M1, which the c4v001 records did not register, gets a synthetic FINISHED receipt at the step-4 start; R1 T051's result time after the start becomes the first receipt's write time; R2 V75's registered log_index 8, not a PRIMARY member, is replaced by M1), KEPT 2 (R1 T087, N2 BF08: the original inputs are the defect under test).

**Every changed expected output, with the clause that requires it** (declared in `run_suite_c4v003.py` before the first c4v003 run on any regression case):
- **Z1, every output:** `classifier` reads `classifier_a_c4v003` (new build).
- **Z2, brief item 2 (A154; C7, C9), every RECORD and SUCC case (315):** the STAGE0 status dict loses `result_first_available_utc`, gains `source` and `post_score_exploratory`; for SUCC, `receipt_times_utc` lists one time per PRIMARY member. Status and reasons are unchanged in every case.
- **Z3, brief item 2 (C8), every SUCC case (28):** `header.freeze_manifest_sha256` is the carried manifest's.
- **Z4, brief item 1 (C6), the 27 N2 cases pinning 385b287c** (V3A01–V3A13, V3A15, V3A17–V3A19, V3A21–V3A30): item 11 reads AGREE_RECORD_DEFECT with PHASE1_TOOL_PIN_DEFECT (Phase 2), or every band entry reads PHASE1_TOOL_PIN_DEFECT (Phase 1: V3A18, V3A19, V3A28); their spec expectations on item 11 or the band column are replaced by those. Their v003b counterparts are B01–B13, B16, B17.
- **Declared case change R1 T087 (brief item 2; M-5 addition 2):** the case pins a stand-in successor whose bytes miss the sealed sha (its SEAL_SHA_MISMATCH, kept). In c4v003 the pin puts Phase 2 under the successor: the v003g manifest also reads FIELD_DEFECT_OUTSIDE_ROWS and the stand-in is not the bound successor (FIELD_DEFECT_ALTERNATIVE). Checked by its declared spec and by equality of every top-level key outside the stop and blank keys.
- **T3 (basis):** none (no regression case had an envelope defect on a non-MISS row).

**New cases (N3):** B01–B19 (v003b AT1 COVERED/SUPERSEDED; AT0B AGREEMENT_DEFECT printing both shas; values_sha256 missing, upper-case, null, short; D6 with no record and with a passing AT-0b record; AT-0a and AT-1 AGREEMENT_DEFECT; module custody; 385b287c refused in item 11 and in the band column; the v003b L1; a v003a L1 under v003b; the module-name mismatch; the d64351ec control); S01–S25 (STAGE0 via the block: EVALUATED with DT-S0G CONSISTENT, NOT_FINISHED, RECEIPTS_AFTER_STEP4, the step-4 tie with AGAINST, the block's NO_SEALED_SUCCESSOR, EVALUATED_REFUSED by an evaluation and by a receipt refusal, no root record at the freeze; block defects: keys, rule consistency, members, self-sha, phase; the wrong schema strings with and without the pin; the stand-in pin; the projection record matching and not; Phase 1 with the pin; the no-successor projection record, a legacy C4V001 record, a record claiming (b); evaluated but not scored; prescore under the successor); T3A–T3C (an envelope defect on a HIT row, on an INVALID row, and on all rows).

**Method.** N3 expectations were written by hand in `suite/case_defs_c4v003.py`, with clauses and derivations, before the classifier ran on any N3 case. All 47 passed on their first run; `run_suite --freeze` then wrote EXPECTED_OUTPUT.json, and the record run compared bytes. For R1, R2 and N2, the prior builds' expected bytes are the oracle, carried mechanically by Z1–Z4 and one declared case change, so any other change fails.

## Rule notes (self-reported; also in PARTIAL.md)

- All Python ran through the fenced runner; the fence summary shows nothing opened or listed outside this build in any run. No `python -c`, heredoc Python or unfenced run. No `find`.
- Copy check: a first attempt used a recursive shell function over the copied trees (B2 sources and B3 copies) that mis-scoped its variables and failed; its partial list `work/copy_check_c4v003.txt` is left in place. The record check `work/copy_check_c4v003_r2.txt` (6857 files, 0 differing) used fixed-depth loops over named folders. Both were nested non-recursive `ls` walks of the copied trees only.
- The runner copy was edited in place (EXPECTED_BUILD and the refusal message), as the brief requires. The two conversion tools are separate files (r1 superseded by r2, its output kept). The classifier drafts were edited only before their first run; the deliverable is a byte copy of d02. The generator and the runner were written before their first runs and not edited after.
- Files opened outside this build and the named basis: the c4v001/c4v002 briefs, B2's README, classifier, runner, suite generator and case defs, PARTIAL, verify report; phase1_c2v003b.py, its README and DIFF (and, for the diff and the hash, phase1_c2v003a.py and phase1_c2v002.py, named in the c4v002 brief); the successor module and its README; the V006 addendum section A154 only (awk section filter); the rulings draft (grep for M-5/M-14 lines); v003g's SCHEMA lines. A non-recursive `ls` of `phase1_c2/` and `stage0_successor_c2/` showed other files (e.g. HASHES_V003B, test files); none of them was opened.
