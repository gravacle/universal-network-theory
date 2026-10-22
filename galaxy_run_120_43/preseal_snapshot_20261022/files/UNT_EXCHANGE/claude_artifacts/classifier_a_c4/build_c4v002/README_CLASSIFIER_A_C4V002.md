# Classifier A (lane Claude4), build c4v002: the M-12 Implementation A for the miss-reading prereg r3a, successor of c4v001

**What it is.** `classifier_a_c4v002.py` is the mechanical, target-blind classifier of ROOT_ITEMS M-12, Implementation A, for the r3a text of record in `basis/` (`PREREG_MISS_READING_R3A.md` `a8c8686c…`, `ROOT_ITEMS_R3A.md` `ed9f5c5b…`, `CLAUSE_SOURCE_MAP_R3A.md` `e1dc19fc…`; shas in `BASIS_SHAS_C4V002.txt`), with root's rulings of M-1 to M-16 as adopted in A142. It succeeds `classifier_a_c4v001.py` (`06f169e2…`, verified 0 BLOCKING, `build_c4v001/verify_c4v001/VERIFY_C4V001.md`). It binds the phase1 `band` and `agree` encodings from the bytes of the two tools the seal may pin: `phase1_c2v002.py` `d64351ec…` and `phase1_c2v003a.py` `385b287c…` (A144, A149; root dispatch 0716). Classifier B (Codex1) is built separately; nothing of B or of its predecessor was opened.

**Status.** Built and suite-tested on synthetic, target-free inputs only; never run on a real manifest or score. Record run `SUITE_RESULTS_C4V002.json`: **362 cases, 362 pass** (206 c4v001 regression cases, 92 c4v001 verifier cases, 64 new cases). The open choices are listed below with the value classifier A uses; each is raised, not silently decided.

**Files** (sha256 in `HASHES_C4V002.txt`):

| file | role |
|---|---|
| `classifier_a_c4v002.py` | the classifier (stdlib only, Python 3.12) |
| `run_suite_c4v002.py` | runs the three case sets (R1, R2, N), writes the results file |
| `SUITE_RESULTS_C4V002.json` | the record run |
| `suite/case_defs_c4v002.py`, `suite/build_suite_c4v002.py` | the 64 new case definitions (hand expectations, clauses, derivations) and their generator (a copy of c4v001's with the changes its docstring lists) |
| `suite/SUITE_INDEX_C4V002.json`, `suite/cases/<id>/`, `suite/common/` | the new cases: `BUNDLE.json`, inputs, `EXPECT_SPEC.json` (+ `EXPECT_SPEC_R1.json` for VF4A, VF5A), `EXPECTED_OUTPUT.json`; common = byte copies of c4v001's common files |
| `regression_c4v001/` | byte copies of c4v001's `basis/` (old text `1e17eb45…`, which the copied cases seal by relative path) and `suite/` (cases, common, index, case defs, generator) |
| `regression_verify/` | byte copies of the verifier's `cases_r3/` and `cases_r3_extra/`; each case adds `BUNDLE_C4V002.json` (its bundle with the absolute build_c4v001 paths re-pointed to these copies; nothing else changed) |
| `tools/run_fenced_c4ep1.py`, `tools/fence_c4v003.py` | the fenced runner (EXPECTED_BUILD set to this folder, nothing else changed) and its fence (`175b995b…`, byte copy) |
| `tools/prep_verify_bundles_c4v002.py`, `tools/write_spec_revisions_c4v002.py`, `tools/dump_outputs_c4v002.py` | the R2 bundle re-pathing, the two N spec revisions, a review aid that dumps outputs for reading with jq |
| `work/` | the two classifier drafts (`cls_c4v002_d01.py`, `cls_c4v002_d02.py` = the final bytes), dev runs `run01`–`run04`, `outs_d02/`, the copy check lists |
| `PARTIAL.md` | the append-only progress log |

## How to run

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  taskpolicy -b <codex python3> -I -B B/tools/run_fenced_c4ep1.py B/classifier_a_c4v002.py BUNDLE.json OUT.json
```
`OUT.json` is created exclusively. The importable entry point is `classify_bundle(bundle_path) -> bytes`. The suite: `run_suite_c4v002.py RESULTS.json [--classifier PATH] [--freeze] [--sets R1,R2,N]`.

## CHANGES against c4v001

Behaviour:
1. **Phase1 pin switch (brief item 1; A142 item 4; A149).** `phase1_tool.sha256` must be `d64351ec…` with module `phase1_c2v002`, or `385b287c…` with module `phase1_c2v003a` (the MODULE string those bytes write into L1, AT0A, AT0B and AT1). Any other sha, or a module name not the sha's, is `PHASE1_TOOL_PIN_DEFECT` (band column and item 11 only, never NOT_READ). c4v001's binding of "any sha naming module phase1_c2v003" is removed: v003 (`149ed4cb…`) is refused.
2. **The v003a `agree` encodings, bound from 385b287c's bytes** (`cmd_at0b`, `at1_rows`, `cmd_at1`, `member_eps`, `band_region_extent`, `band_region_box_only_extent`). c4v001's OC-18 assumptions were checked against the bytes and corrected (see "Discrepancies" below):
   - an **AT0B** record carries `members_sha256` (64 lower-case hex; `cmd_at0b` writes `a.members_sha256.lower()`), which item 11 prints as `at0b_members_sha256` when the AT-0b record is the record (A149 item 2);
   - an **AT1 failing entry** has exactly eleven keys: `log_index, id, excess, norm_n, category, flag, flag_reason, region_rows_violated, region_max_violation, geometric_part, residual_part` (`flag` is always present; c4v001 treated it as optional). `flag` and `flag_reason` come in pairs: (null, null) bounded; (`FD_NOISE_NOT_BOUNDED`, `NO_ROW_EPS_Q`) a row without eps_q; (`MEMBER_POINT_NOISE_NOT_BOUNDED`, one of `MEMBER_EPS_LIST_MISSING`, `MEMBER_EPS_NONE`, `MEMBER_EPS_BOOL`, `MEMBER_EPS_NOT_A_NUMBER`, `MEMBER_EPS_NON_FINITE`, `MEMBER_EPS_NEGATIVE`) an unbounded member-point entry (A149 item 1: an int beyond float range reads `MEMBER_EPS_NON_FINITE`). The category is the first violated family of `[TRUST_RADIUS, BOX, LINEAR_DDO]` (`OUTSIDE_TRUST_RADIUS`, `OUTSIDE_BOX_SLICE`, `OUTSIDE_LINEAR_DDO_REGION`), `NGC_NONLINEAR` iff the list is empty. Item 11 now prints `flag` for v003a entries too;
   - **`reported`** has exactly at1_rows' twelve keys: v002's seven plus `pairs_member_point_noise_not_bounded`, `band_region_extent`, `band_region_single_point`, `band_region_single_point_reason` (always present; c4v001 treated it as optional) and `band_region_box_only_extent` (A149 item 3). Checked: `e_q_per_member_row` entries `{log_index, id, e_q, eps_m, flag, flag_reason}` (bounded: `e_q`, `eps_m` numbers, `eps_m` ≥ 0; member-point flag: `e_q` a number, `eps_m` null; row flag: `e_q` = `FD_NOISE_NOT_BOUNDED`, `eps_m` null); per-pair list entries `{log_index, id, flag_reason}` with a `MEMBER_EPS_…` reason; both extent lists `[{direction, extent: [lo, hi], lp_status: [s_min, s_max]}]` (a bound is a number iff its status is `OPTIMAL`, else `NOT_AVAILABLE`), over the same directions in order; `band_region_single_point` is `NOT_AVAILABLE` iff some band-region program is not OPTIMAL, else true iff every extent is exactly [0.0, 0.0]; the reason is null unless that is true, then `BOX_CORNER` or `OTHER_ROWS`. All of `reported` is echoed in item 11 (`target_free_always_reported`), print only;
   - the v003a L1 is v002's except `module` (`lp_pair`, `band_rows`, `check_values`, `cmd_band`, and `cmd_at0a` are textually identical in d64351ec and 385b287c), so the band-column binding is unchanged; `module` must be the pin's.
3. **V-F1 (hex case as v003g).** Roster `root_gates` pins, the gate-status list's `gate_sha256` values and the frozen manifest's gate registration sha are read with v003g's own `_is_hex64` (64 characters, hex after lower-casing; `48a1e48a` L289) and compared lower-cased, as `_root_pinned_document` compares `pin['sha256'].lower()` (L1603–1607). A repeat in the gate list is judged after lower-casing.
4. **V-F2 (E3 scope words).** The E3 value prints `TESTED-NEGATIVE (A15 E3 scope)` (C-5.3; C-8 words rule), in `e3_line.value`, in R-MF part 2 and as the Phase-2 value in item 11's cross-phase E3 lines. The other values are unchanged (`NOT_NEGATIVE_AT_OUTER`, `NOT_TESTABLE`).
5. **V-F3 (integers beyond float range).** `is_num` reads an integer that is not finite as a float as not finite: it is a field defect of its class (a score row: `FIELD_DEFECT_ROW`; an L1 row: `L1_ROW_DEFECT`; an agree field: `AGREE_RECORD_DEFECT`; the C3 record: that P8 half NOT_AVAILABLE; a frozen manifest speed in prescore: `FIELD_DEFECT_OUTSIDE_ROWS`), never `INTERNAL_ERROR`. Floats are unchanged: an overflowing float literal (1e400) still refuses the whole input at the loader.
6. **V-F4 (Phase-1 header).** In a scored Phase 1 (`phase_named` PHASE_1, `run_status` SCORED) the phase-inputs record must carry `phase1_header` (its `l1_sha256` is the L1 sha logged at the Phase-1 freeze, C-1.1 L1 map row). Without it the record is refused: `PHASE_MISMATCH` (its "every other" class, as any malformed phase inputs), detail `phase inputs record: PHASE1_HEADER_MISSING (…)`. A Phase 1 with no NGC call or an AT-0a failure needs no header.
7. **V-F5 (run status of the other phase).** `AT0A_FAILED` is a Phase-1 run status only, `HALTED` a Phase-2 one (I-7); `SCORED` and `NO_NGC_CALL` serve both. A record naming a phase with the other phase's status is refused: `PHASE_MISMATCH`, detail `phase inputs record: RUN_STATUS_NOT_OF_PHASE (…)`. The text's AT-0a case is kept: Phase 2 `SCORED` with `phase1_classification_absent_reason` `AT0A_FAILURE` classifies in full (VF5B). For these two refusals (V-F4, V-F5) the record's named phase is kept, so no input of the other phase is demanded (OC-27).
8. **V-F6 (NEAR gloss).** Every per-row entry that prints `near` also prints `near_label: "envelope overlaps the error bar"` (C-1.1); so does `a15.E1.a`.

Contracts (root adopted the input contracts as its record forms, 0720): the schema strings are unchanged (`CLASSIFIER_A_BUNDLE_C4V001`, `CLASSIFIER_A_OUTPUT_C4V001`, `PHASE_INPUTS_C4V001`, …), as the phase1 tool keeps `PHASE1_AT1_C2V001` across versions. The contract changes are exactly:
- **C1** `phase1_tool` (bundle): the two bound pins only (change 1).
- **C2** the A133 `agree` record under 385b287c (change 2).
- **C3** `PHASE_INPUTS_C4V001`: `phase1_header` is required when Phase 1 is scored (change 6); `run_status` must be one of the named phase (change 7). Clarification, no behaviour change: in Phase 2 `phase1_header` should be null; a header given there is not read (c4v001 behaved the same).
- **C4** `GATE_STATUS_LIST_C4V001`: `gate_sha256` may be upper- or lower-case hex; identity is the lower-cased value, with no repeats after lower-casing (change 3).
- **C5** the output: `near_label` (change 8), the E3 value text (change 4), `flag` in v003a failing entries and `at0b_members_sha256` in item 11 (change 2).

Everything else is c4v001's, byte for byte in behaviour: R1 shows every c4v001 output unchanged except by the declared transforms and four listed overrides.

**Basis check (brief, "Read first").** The basis differs from c4v001's by the r3a classifier-build table and its text edits. Each was checked against c4v001's code: F1 (NEAR on tier-MISS rows only; `score_output`), F2 (the record is AT-1, else the AT-0a/AT-0b AGREEMENT_DEFECT record; `parse_agree`), F3 (onset counts LATE and null-ratio rows; `engine`), F4 (support record required; `check_tsr`), F5 (the named stop codes; `check_score`, `check_envelope`, `check_zone_table`), F7 (joint enumeration; `engine` over ROW and GATE), F8 (STAGE0 record field read as the alternative's; `prepare_alternatives`), F9 (missing-gate twin reads TWIN_INPUT_DEFECT; `twin_rows`), F10 (both roots in the phase inputs; `check_phase`), F12 (RECEIPTS_AFTER_STEP4 as a reason; `stage0_status`), F13 (row scope: MISS rows with a frozen prediction; `readings`), F14 (the frozen registration; `_kinds_of_registration`); ROOT_ITEMS M-5 (Phase-2 root) and M-12 (F12). c4v001 already matched each; no code change was needed. One case per change is in set N (BF01–BF14; BF06 shows the disclosed-open F6). F6, F11 and F15 stay open, disclosed (OC-10, OC-15, OC-21).

## The input bundle (`CLASSIFIER_A_BUNDLE_C4V001`)

One strict JSON object with exactly these keys. Every path may be absolute or relative to the bundle's folder. Every pin is `{"path": str, "sha256": 64 lowercase hex}`; the classifier hashes the bytes and refuses to parse an input whose bytes differ (the input then counts as missing, in its role's map class below). A malformed bundle refuses the run (`{"refused": true, "reason": "BUNDLE_…"}`).

| key | content |
|---|---|
| `schema` | `CLASSIFIER_A_BUNDLE_C4V001` |
| `mode` | `score` (the full classification with the re-run stops) or `prescore` (every stop checked on a synthetic score built from the frozen member arrays; C-1.1 "Pre-score checks") |
| `inputs` | an object with exactly the 17 roles below, each a pin or `null` |
| `rosters` | `{alternative name: pin}`: the v003g row-registration rosters (schema `ROOT_ROW_REGISTRATION_ROSTER_CX3V001`); the classifier reads `schema` and `root_gates` (each `{path, sha256}`, sha in either case, as v003g accepts it) |
| `sealed` | `{"text": pin, "classifier": pin, "tsr_flag_record_sha256": hex, "stage0_successor": pin or null}`: the shas of the seal entry (SEAL_SHA_MISMATCH checks them against bytes) |
| `phase1_tool` | `{"sha256": hex, "module": str}` or null: the `band`/`agree` pin of the seal entry. **Exactly** `d64351ec…` with `phase1_c2v002`, or `385b287c…` with `phase1_c2v003a`; anything else reads PHASE1_TOOL_PIN_DEFECT (band column, item 11) [C1] |
| `module_sha256` | the v003g module sha the seal entry pins (header only) |

**Roles** (`inputs`), and what a defect in each does (the C-1.1 map class):

| role | content | needed | defect class |
|---|---|---|---|
| `phase_inputs` | root-written, schema below | always | PHASE_MISMATCH ("every other") |
| `freeze_manifest` | the v003g freeze manifest | always | FIELD_DEFECT_OUTSIDE_ROWS ("every other") |
| `score` | the v003g `score_after_freeze` output | score mode | FIELD_DEFECT_OUTSIDE_ROWS |
| `slots` | an object with `query_block.rows[]` of `{query_id, Rad_text, Rad_unit}` (slots V003, or a target-free extract of its query block) | always | ZONE_TABLE_MISMATCH |
| `gate_status_list` | root-written, schema below | always | GATE_STATUS_LIST_DEFECT (its row rule) |
| `tsr_flag_record` | root-written, schema below | always | TSR_FLAG_TABLE_MISMATCH (and SEAL_SHA_MISMATCH if its bytes miss the sealed sha) |
| `tsr_support_record` | schema `UNT_ROOT_TSR_SUPPORT_CX3V001` (extractor `50c7db5f…`) | always | TSR_FLAG_TABLE_MISMATCH (F4) |
| `ntest_compare` | the N-test record of record (`6f095f64…`) | always | TSR_FLAG_TABLE_MISMATCH |
| `stage0_status` | root-written, schema below | Phase 2 | the STAGE0 alternative reads TWIN_INPUT_DEFECT (F8) |
| `commitment_status` | root-written, schema below | Phase 2 | EXPLORATORY with COMMITMENT_STATUS_DEFECT; blanks nothing; never NOT_READ |
| `agree_record` | the A133 `agree` record (F2; encodings below) | Phase 2 | §8 item 11 NOT_AVAILABLE (AGREE_RECORD_DEFECT); never NOT_READ |
| `phase1_classification` | classifier A's own Phase-1 output | Phase 2 | the cross-phase items NOT_AVAILABLE (PHASE1_CLASSIFICATION_INPUT_DEFECT); never NOT_READ |
| `l1_record` | the pinned `band` command's `L1_C2V001.json` (schema `PHASE1_L1_C2V001`) | Phase 1 | the Phase-1 band column only (L1_SHA_MISMATCH, L1_RECORD_DEFECT, L1_ROW_DEFECT, PHASE1_TOOL_PIN_DEFECT); never NOT_READ |
| `c3_record` | the M-13 record: `per_grid.T120L.C3_max_e` (finite) and `per_grid.T120L.C3_PASS` (bool) are read | P8 report | that half of the P8 report NOT_AVAILABLE |
| `root_disclosures` | any JSON object (D-4 values, attestation, V005/V006 shas, RUNBOOK_V002/roster-builder/step-map shas, window changes, `outer_gas_cut_report`) | header | echoed; absence noted |
| `fallback` | root-written, schema below | under the fallback | item 10 NOT_AVAILABLE |
| `field_map` | the key-only field map, schema below | only if pinned | not applied (header `FIELD_MAP_DEFECT_NOT_APPLIED`); the stops stand |

**What is read from the v003g files** (M-5, bound to `48a1e48a…`): unchanged from c4v001 (score `headline.reference_member_id`, `reference_member_log_index`; `members[].member_id`, `log_index`; the reference member's `member_valid` and `rows[].{id, score_status, within_error, sigma_ratio, registered_reason, status}`, in Phase 1 also `observed_speed_km_s`, `quoted_sigma_km_s`; `pointwise_envelope.label` and `rows[].{id, valid, band_overlaps_error_bar}`; `sensitivity.rows[]` (Phase 2); `alternatives[]`; `freeze_status`, `incomplete_reasons`; manifest `reference_member`, `members[].{member_id, row_registration}`, `alternative_results`, `input_bindings.calibration_record.path`, `pins.input_files[].sha256`, and in prescore the frozen arrays).

### Root-written input contracts (minimal strict schemas; root has adopted them, 0720)

Every one is a JSON object with exactly the keys shown; strings are non-empty; times are `date -u` ISO strings `YYYY-MM-DDTHH:MM:SS[.ffffff]Z`.

- **Phase inputs** (`PHASE_INPUTS_C4V001`): `phase_named` (`PHASE_1`/`PHASE_2`, the phase the score entry names); `phase1_registry_root` (the absolute path the seal entry names); `phase2_registry_root` (absolute); `run_status` (`SCORED` or `NO_NGC_CALL` in either phase; `AT0A_FAILED` in Phase 1 only; `HALTED` in Phase 2 only [C3]); `run_status_code` (string or null, e.g. the engine terminal status); `phase1_header` (`{b_p1: int, u_a_log_index: int, phase1_record_sha256, l1_sha256}`, the L1 sha logged at the Phase-1 freeze; **required when `phase_named` is PHASE_1 and `run_status` is SCORED** [C3]; null otherwise, and not read in Phase 2); `phase1_classification_absent_reason` (null, `AT0A_FAILURE` or `NO_PHASE_1_SCORE`). A refused record reads PHASE_MISMATCH; the refusal reasons PHASE1_HEADER_MISSING and RUN_STATUS_NOT_OF_PHASE are printed in the stop's detail.
- **Gate-status list** (`GATE_STATUS_LIST_C4V001`): `gates`: a list of `{gate_sha256, status: ON-TIME|LATE, pinned_by_entry}`, one per gate document sha, no repeats (C-4, M-15). Identity is the gate document's sha256, read case-insensitively and compared lower-cased, as in v003g [C4].
- **TSR flag record** (`TSR_FLAG_RECORD_C4V001`): `target_free: true`, `rule` (text), `failing_ring_ordinal: 15`, `ntest_compare_pin`, `n1_record_pin`, `gl_node_record_pin` (pins with shas `6f095f64…`, `8867c376…`, `ec1dcca5…`), `flags`: 43 `{query_id, TRUNCATION_SHAPE_RESIDUAL: bool}` in manifest order. Its own sha and the three pinned shas must be among the freeze manifest's `pins.input_files` (C-1.4; rulings M-7).
- **STAGE0 status record** (`STAGE0_STATUS_RECORD_C4V001`, Phase 2): `registered_members`: a list of `{log_index, terminal_receipt (FINISHED or another A133 rule-(c) status), receipt_written_utc}`; `phase2_step4_start_utc`; `successor_refused_a_record: bool`; `result_first_available_utc` (time or null). Condition (b) is the bundle's `sealed.stage0_successor` being non-null.
- **Commitment status** (`PHASE2_COMMITMENT_STATUS_C4V001`, Phase 2): `status` (`COMMITTED` with an empty `stops_or_changes`, or `EXPLORATORY` with a non-empty one); `stops_or_changes`: `[{what, entry}]`.
- **Fallback record** (`FALLBACK_RECORD_C4V001`): `applies: bool`, `classification_label` (null, `EXPLORATORY (post-prediction)` or `POST-PREDICTION (CLASSIFIER)`), `seal_candidate`, `pre_prediction_shas`, `post_prediction_changes` (echoed as item 10).
- **Field map** (`KEY_FIELD_MAP_C4V001`): `renames: {role: [{at, from, to}]}`; `at` is a container path such as `members[].rows[]` or `pointwise_envelope.rows[]` (`""` is the root). Keys only; a rename onto an existing key is refused.
- **The M-13 C3 fields** are read from the pinned record as named above.
- **The A133 `agree` record** (F2): the `PHASE1_AT1_C2V001` record of the pinned `agree at1`; when AT-1 did not run, the `PHASE1_AT0A_C2V001` or `PHASE1_AT0B_C2V001` record, accepted only with outcome `AGREEMENT_DEFECT`. Its `module` must equal the pinned tool's. Under AGREEMENT_DEFECT, `failing`, `non_discriminating_rows` and `reported` may be absent.
  - d64351ec (v002), unchanged: failing entries have exactly `{log_index, id, excess, norm_n, category, flag}`, categories OUTSIDE_TRUST_RADIUS, OUTSIDE_LINEAR_DDO_REGION, NGC_NONLINEAR, flag null or FD_NOISE_NOT_BOUNDED; `reported` carries at least the seven v002 keys.
  - 385b287c (v003a) [C2]: as in CHANGES item 2 (AT0B `members_sha256`; eleven-key failing entries with the flag pairs; twelve-key `reported`).

## The output (`CLASSIFIER_A_OUTPUT_C4V001`)

Canonical JSON: `json.dumps(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)` and a newline. Floats appear only where the text prints a value; R_q is printed as the registered `Rad_text`. An output that the stop-to-output map blanks is `{"NOT_AVAILABLE": [codes]}`. UNDEFINED quantities print `"UNDEFINED"`. `classifier` is `classifier_a_c4v002`.

Top level: `schema`, `classifier`, `mode`, `phase`, `status` (`CLASSIFIED`, `NOT_READ` or `NO_CLASSIFICATION`), `status_code`, `stops` (each `{code, class, alternative, detail, rows}`), `labels`, and the §8 items:

| §8 item | keys |
|---|---|
| 1 header | `header`, `headline` (echoed; I-5) |
| 2 per-row table | `rows`: `id, zone, R_q, tier, reading_kind, r_q, sign, frozen_prediction, near, near_label` [C5]`, tsr_flag, invalid_reason, gate_status, gate_after_predictions, sensitivity_band_overlap, sensitivity_band_label, phase1_band` (Phase 1)`, notes, tier_key` |
| 3 zone summaries, OUTER_FAILURE, E3 | `zones`, `outer_trend`, `outer_failure`, `e3_line` (`value` one of `TESTED-NEGATIVE (A15 E3 scope)` [C5], `NOT_NEGATIVE_AT_OUTER`, `NOT_TESTABLE`) |
| 4 patterns and flags | `patterns`, `patterns_holding`, `minority_miss`, `flagged_rows` |
| 5 readings | `readings` (R-MF part 2 `{status: <the E3 value>, test: E3_VERDICT_LINE}`), `descriptive` |
| 6 INVALID list | `invalid_list` |
| 7 A15 comparisons | `a15` (`E1.a` carries `near_label` [C5]), `p8_report` |
| 8 alternatives | `alternatives`, `stage0` |
| 9 | `exploratory_readings` (always empty) |
| 10 | `fallback` |
| 11 (Phase 2) | `agreement`: `outcome`, `phase1_consequence`, `non_discriminating_rows`, `failing_member_rows` (each `{member_log_index, row, excess, norm_n, category, flag}` plus, under v003a, `region_rows_violated, region_max_violation, geometric_part, residual_part, flag_reason`), `target_free_always_reported` (the record's `reported`, echoed), `agree_schema`, `at0b_members_sha256` (v003a AT0B record only) [C5], `withdrawn` (SUPERSEDED), `cross_phase`, or under a defective record `agree_record_defect` with the reason word |

`prescore` mode prints `{schema, classifier, mode, phase, manifest_phase_derived, result: PASS | CLASSIFICATION_INPUT_DEFECT, stops, not_stop_inputs, field_map}`.

## Rule-to-function map

| text rule (section, tag) | function(s) |
|---|---|
| strict parsing (M-12, A71): duplicate keys, NaN, ±Infinity, float overflow refused; nothing last-wins | `strict_loads`, `_pairs`, `_const`, `_float` |
| finite where finite is required; integers beyond float range (C-1.1; V-F3) | `is_num` |
| inputs verified by sha before parsing | `read_pinned`, `load_inputs`, `load_bundle` |
| rule M-T tiers, null ratio (C-1.1); LATE rows (C-4) | `build_rows` |
| sign (C-1.2) | `sign_of` |
| zone rule; ZONE_TABLE_MISMATCH (C-1.3, F5) | `check_zone_table` |
| TSR flag, carrier, support record, TSR_FLAG_TABLE_MISMATCH (C-1.4, C-1.1, F4) | `check_tsr` |
| NEAR flag on tier-MISS rows, its gloss (C-1.1, C-I7, F1; V-F6) | `score_output` (NEAR block, row table), `check_envelope`, `a15` |
| sensitivity column (C-1.1) | `check_sensitivity`, `score_output` |
| Phase-1 band column (C-1.1, M-16); the pin switch (A142 item 4, A149) | `band_column`, `_tool_module` |
| pre-score checks and stops: reference member, field checks, ids, envelope label (C-1.1, M-5, F5) | `check_score`, `check_envelope`, `check_alternatives` |
| GATE_STATUS_LIST_DEFECT, ON-TIME/LATE, gate identity (C-1.1, C-4, M-15; V-F1) | `check_gate_list`, `_frozen_registration`, `_kinds_of_registration`, `is_hex64_ci`, `_pin_ok_ci` |
| SEAL_SHA_MISMATCH (C-1.1, M-6) | `check_seal` |
| PHASE_MISMATCH, both roots (C-1.1, F10); the phase-inputs contract (V-F4, V-F5) | `check_phase`, `_phase_inputs_check`, `RUN_STATUS_PHASES` |
| pre-score run on a synthetic score (C-1.1) | `synthesize_score`, `prescore_output` |
| field map (C-1.1 "Rename a field") | `_field_map_renames`, `_apply_rename` |
| NOT_READ and the closed stop-to-output map, several stops, joint enumeration (C-1.1, F7, F14) | `stop`, `stops_out`, `zone_vectors`, `engine`, `readings`, `score_output` |
| zone summaries, patterns P0–P15, P1g, P11g (C-2) | `vec_counts`, `engine`, `zone_out`, `median` |
| readings, part-1 order, A10 rule, MINORITY_MISS, A15 E3 rule, scope (C-3, C-3.1, C-3.2, F13) | `readings`, `drift_part2` |
| onset radius (C-3, F3); DT-T1a | `engine`, `score_output` |
| INVALID list (C-4, C-8 item 6) | `invalid_list` |
| A15 E1, E2 (C-5.1, C-5.2); E3 line and its value (C-5.3; V-F2) | `a15`, `engine` (E3 value), `score_output` (E3 block) |
| P8 report (C-3.2, M-13) | `p8_report` |
| twin rule, TWIN_INVALID, TWIN_INPUT_DEFECT (C-6.1, M-10, F9) | `twin_rows`, `classify_twin`, `twin_row_out`, `prepare_alternatives`, `alternatives_out` |
| alternatives not evaluated; Phase-1 precedence (C-6.2, C-I4, M-10) | `alternatives_out`, `check_alternatives` |
| STAGE0 receipt rule and statuses (C-6.3, M-14, F8, F12) | `stage0_status`, `stage0_block` |
| DT-S0G comparison, M-9 as ruled, R-DRIFT mapping (C-6.3) | `s0g_compare`, `drift_part2`, `readings` |
| labels (C-I6, C-I7, M-8) | `labels` |
| commitment status (C-I7) | `commitment` |
| no classification (C-I7) | `run` |
| header (C-8 item 1); headline (C-I5) | `header`, `headline_out` |
| item 10 (C-8) | `fallback_out` |
| item 11 (C-8), the A133 `agree` record (C-1.1 map, F2; A144, A149) | `agreement`, `parse_agree`, `_flag_pair_ok`, `_extent_list_defect`, `_reported_v003a_defect`, `_p1_ok` |

## The NOT_READ map as implemented (C-1.1)

Unchanged from c4v001: each defective reference row (class ROW) takes HIT, signed MISS, null-ratio MISS, plus INVALID_AS_MISS (or LATE-gate MISS for a LATE gate) when its frozen registration is INVALID (F14); each row of a gate missing from the list (class GATE) takes INVALID_AS_MISS and LATE-gate MISS; the two are enumerated jointly (F7). Count-level outputs print when they take one value over every assignment; every other output computed from a defective row reads NOT_AVAILABLE unless a listed deduction fixes it (the list applied as closed; F6, OC-10). Each reading's part prints when the printed outputs fix it. Other classes: ENVELOPE, SENSITIVITY, ALT, TSR, ALL ("every other": every output except the header and the echoed headline). The band-column inputs, the item-11 inputs and the commitment status never stop.

## Open choices (raised, not decided; the value used and the pinning case)

Carried from c4v001, with their status under the new basis:

| id | question | classifier A uses | status | case |
|---|---|---|---|---|
| OC-01 | NEAR and invalid envelope rows | tier-MISS rows only | resolved by F1 | BF01, T231 |
| OC-02 | which `agree` record | AT1, else the AT-0a/AT-0b AGREEMENT_DEFECT record | resolved by F2 | BF02, V3A06, V3A24 |
| OC-03 | onset radius and LATE rows | counted | resolved by F3 | BF03, T224 |
| OC-04 | map class of a defective STAGE0 record | the alternative class | resolved by F8 | BF08, T052 |
| OC-05 | twin rows of a missing gate | TWIN_INPUT_DEFECT, and classifier A also prints the alternative-class stop FIELD_DEFECT_ALTERNATIVE beside GATE_STATUS_LIST_DEFECT; F9 fixes the reading but not that code | F9 resolves the reading; the code stays open | BF09, T229 |
| OC-06 | TSR support record | required | resolved by F4 | BF04, T079 |
| OC-07 | Phase-2 registry root; non-disjoint roots | from the phase inputs; PHASE_MISMATCH | resolved by F10 | BF10, T090 |
| OC-08 | unnamed stop codes | the F5 names; band codes L1_SHA_MISMATCH, L1_RECORD_DEFECT, L1_ROW_DEFECT, L1_ROW_NOT_AVAILABLE, TARGET_PAIR_DEFECT, Q01_Q02_ALWAYS_NOT_AVAILABLE, PHASE1_TOOL_PIN_DEFECT; AGREE_RECORD_DEFECT, PHASE1_CLASSIFICATION_INPUT_DEFECT, ENVELOPE_ROW_INVALID | stop codes resolved by F5; the column codes remain A's (A and B must share) | many |
| OC-10 | the closed deduction list | applied literally | F6 open, disclosed | BF06, T064, T065, T082 |
| OC-11 | several row-level stops | joint | resolved by F7 | BF07 |
| OC-12 | "the roster registers INVALID" | the frozen registration | resolved by F14 | BF14, T182 |
| OC-13 | which members' fields are checked | ids of all; rows of the reference member | open | — |
| OC-14 | "wrong type" | includes the enumerations, etc. | open | T181 |
| OC-15 | N-gate state at launch | the N-test record's `n_route_ab_gate` | F11 open, disclosed | T078 |
| OC-16 | RECEIPTS_AFTER_STEP4 | the reason of NOT_EVALUATED_BEFORE_FREEZE | resolved by F12 | BF12, T050 |
| OC-17 | row scope and HIT rows | MISS rows with a frozen prediction | resolved by F13 | BF13 |
| OC-18 | phase1_c2v003 encodings without bytes | **closed**: rebound from 385b287c's bytes (CHANGES item 2); its three assumptions are corrected: keys under `reported` (confirmed), `flag` optional (wrong: always present), the reason key's name (confirmed, but always present) | closed | V3A01–V3A30 |
| OC-19 | header and headline under an "every other" stop | both print | open | T069 |
| OC-20 | L1 `lo > hi`; non-positive sigma | not checked; sigma > 0 required | open | — |
| OC-21 | M-12 witness sets not pinned | class analogues | F15 open, disclosed | — |
| OC-22 | ML/GL10 marked evaluated and scored | the twin rule | open | T061 |
| OC-23 | root-written input formats | as defined here | adopted by root (0720); this build's changes C1–C5 listed | all |

New in c4v002:

| id | question | classifier A uses | case |
|---|---|---|---|
| OC-24 | how far to cross-check the print-only v003a fields | domain encodings, the flag/flag_reason pairs, single_point against the printed band-region extents, the reason null unless single_point is true, equal direction lists; **not** the reason against the box-only extents (equal by construction in the bytes, but a second LP run) | V3A22–V3A27 |
| OC-25 | "at0b `members_sha256` with at1's required match" | the AT1 record carries no members or AT-0b sha, so the match is not checkable from item 11's one input; it is enforced by at1 refusing (no record). Classifier A requires and prints `members_sha256` on a v003a AT0B record and reads the existence of an AT1 record as the match | V3A06–V3A08 |
| OC-26 | `HALTED` named with PHASE_1 (not in the text; V-F5's mirror) | refused, RUN_STATUS_NOT_OF_PHASE | VF5C |
| OC-27 | the printed phase, and which phase's inputs are demanded, when the phase inputs are refused | for a refusal of a well-formed record for its header or run status: the named phase (no other-phase input demanded); for any other malformed record: null (as c4v001) | VF4A, VF5A, T091 |
| OC-28 | V-F4's scope | the header is required only when Phase 1 is SCORED | VF4A–VF4C |
| OC-29 | the V-F4/V-F5 refusal codes | PHASE_MISMATCH with the detail words PHASE1_HEADER_MISSING and RUN_STATUS_NOT_OF_PHASE (no new stop code; F5's list is closed); A and B must share the words | VF4A, VF5A |
| OC-30 | V-F1's reach | roster root_gates, the gate-status list and the frozen registration are read case-insensitively; every other pin stays lower-case (v003g itself requires lower case for manifest `pins.input_files`, L3221) | VF1A–VF1D |
| OC-31 | an integer literal of more than 4300 digits | Python's int-string limit refuses the whole input (JSON_SYNTAX), not a field defect | — |
| OC-32 | where the NEAR gloss is printed | `near_label` on every row entry that prints `near`, and on `a15.E1.a` | VF6A, VF6B |
| OC-33 | the E3 value string | `TESTED-NEGATIVE (A15 E3 scope)` verbatim from C-5.3 (A and B must share it) | VF2 |
| OC-34 | `MEMBER_EPS_LIST_MISSING` | accepted as a member_eps reason although `check_member_eps` makes it unreachable in an honest at1 | — |
| OC-35 | an envelope-row field defect on a HIT or INVALID row (F1 restricts NEAR to tier-MISS rows; the map says "NEAR and N(Z) … on the rows concerned") | as c4v001: NEAR and N(Z) NOT_AVAILABLE on that row | T094 |

## Discrepancies between phase1_c2v003a's bytes and the A144/A149 descriptions

- **flag_reason values (A144 R3, M-12 binding list).** A144 calls FD_NOISE_NOT_BOUNDED and MEMBER_POINT_NOISE_NOT_BOUNDED "flag_reason values". In the bytes they are values of `flag`; `flag_reason` is NO_ROW_EPS_Q or a member_eps reason (MEMBER_EPS_…). A classifier bound to A144's wording (as c4v001's v003 binding was) refuses every honest v003a record with a flagged failing pair, so item 11 would read NOT_AVAILABLE on an honest record. Classifier A binds the bytes (V3A02, V3A03, V3A10).
- **`flag` in failing entries.** A144 R1's list of what a failing pair prints omits `flag`; the bytes write it in every entry (as v002 did). c4v001 had assumed it optional (V3A09).
- **`band_region_single_point_reason`.** A144 R2 describes the reason; the bytes always write the key, null unless the region is a single point (A149 choice 1) (V3A11, V3A25).
- **A149 item 1 wording.** "that pair is flagged MEMBER_EPS_NON_FINITE": in the bytes the pair's `flag` is MEMBER_POINT_NOISE_NOT_BOUNDED and MEMBER_EPS_NON_FINITE is its `flag_reason` (README_PHASE1_C2V003A states it correctly).
- **Members custody (A149 item 2, 0716).** The required match lives in at1 (a refusal with no out-dir); the AT1 record carries neither the members sha nor the AT-0b sha (OC-25).
- **No discrepancy:** A144 R2's "band, band_rows, cmd_band and the L1 schema are unchanged" holds in the bytes (textual identity with d64351ec except MODULE); so does cmd_at0a. The A149 box-only extent has band_region_extent's form, as A149 item 3 says. c4v001's own v003 suite fixture wrote band_region_extent entries as `{direction, min, max, status}`, which is not the bytes' form (c4v001 did not check that field).

## The suite

Three sets, all synthetic and target-free; `SUITE_RESULTS_C4V002.json` (classifier `a11ae7b9…`): 362 cases, 362 pass.

| set | cases | pass | failing | what is compared |
|---|---|---|---|---|
| R1 c4v001 regression (`regression_c4v001/suite/cases`) | 206 | 206 | none | the c4v001 hand spec and the c4v001 EXPECTED_OUTPUT bytes, carried by the declared transforms and overrides; the c4v002 output must equal those bytes exactly |
| R2 c4v001 verifier cases (`regression_verify/cases_r3`) | 92 | 92 | none (V71 and V85, the two c4v001 failures, now pass) | the verifier's own checks (VERIFIER_EXPECT.json), carried by the declared check transform; informational: outputs equal the verifier's recorded c4v001 outputs under the same transforms except V71 and V85 |
| N new (`suite/cases`) | 64 | 64 | none | hand spec written before any run, then the frozen bytes |

**Every changed expected output, with the clause that requires it** (declared in `run_suite_c4v002.py` before the first run):
- **X1, all 206 R1 cases and every R2 output:** the `classifier` value reads `classifier_a_c4v002` (a new build; brief item 4).
- **X2, V-F2 (C-5.3; C-8 words rule):** `TESTED-NEGATIVE` reads `TESTED-NEGATIVE (A15 E3 scope)` at the E3 value, R-MF part 2 and item 11's Phase-2 E3 value. R1 outputs: T002–T010, T012, T013, T020–T025, T028, T029, T033–T036, T039–T046, T049, T050, T053, T064, T082, T092, T094, T100, T102, T104–T111, T131, T150, T172, T185, T202–T207, T214–T219, T221–T223 (67 cases); R1 hand specs: T002, T008, T009, T013, T034, T036, T045, T064, T082, T092, T094, T102, T131, T221; R2 checks: V01, V02, V05, V09, V11, V16, V19–V23, V25, V32, V86, V91.
- **X3, V-F6 (C-1.1 NEAR gloss):** `near_label` beside every row's `near`, and on `a15.E1.a`: the 171 R1 outputs that print a row table (all but the 35 with none: T066, T067, T068b, T069–T076, T085–T091, T093, T127, T128, T156–T166, T168, T173, T228).
- **Overrides, brief item 1 (the pin switch; A142 item 4, A149):** T130 (band column PHASE1_TOOL_PIN_DEFECT on all 43 rows; spec Q03 NA), T141 and T143 (item 11 AGREE_RECORD_DEFECT with reason PHASE1_TOOL_PIN_DEFECT; spec outcome NA, failing-row expectations absent), T142 (already AGREE_RECORD_DEFECT; its reason word becomes PHASE1_TOOL_PIN_DEFECT). Each of these pins a stand-in sha with module `phase1_c2v003`, no longer bound. Their v003a counterparts are V3A18 (T130), V3A02 (T141, T143) and V3A30 (T142).
- **R2 outputs changed by a fix (informational):** V71 (V-F1: classifies), V85 (V-F3: FIELD_DEFECT_ROW, not INTERNAL_ERROR). Both now meet the verifier's own expectations.
- **N spec revisions:** VF4A and VF5A (`EXPECT_SPEC_R1.json`, the original kept): only `phase` changes from null to the named phase, after the first run exposed a classifier defect fixed in draft d02 (OC-27).

**New cases (N):** V3A01–V3A30 (the phase1_c2v003a encodings: COVERED; SUPERSEDED with OUTSIDE_BOX_SLICE and MEMBER_POINT_NOISE_NOT_BOUNDED / MEMBER_EPS_NON_FINITE, FD_NOISE_NOT_BOUNDED / NO_ROW_EPS_Q, NGC_NONLINEAR / MEMBER_EPS_NEGATIVE; AGREEMENT_DEFECT at AT-0b with members_sha256 (AT-1 refused for the members mismatch), at AT-0a, and in an AT-1 record; band_region_extent, _single_point and its reason, _box_only_extent prints (corner, NOT_AVAILABLE); the corrected OC-18 assumptions; encoding and module custody defects; the pin switch in both columns; the v003a L1); VF1A–VF6B (V-F1: upper-case roster pins, list values, registration, a case-only repeat; V-F2; V-F3 in the row, L1, agree, C3 and prescore classes, with an integer control; V-F4 with its two no-classification controls; V-F5 with the kept AT-0a case, HALTED in each phase and NO_NGC_CALL; V-F6 on a NEAR row and a defective row); BF01–BF14 (one per basis change F1–F14 except F11, which changed nothing; BF06 is the disclosed-open F6).

**Method.** As c4v001: N expectations were written by hand in `suite/case_defs_c4v002.py`, with clauses and derivations, before the classifier ran on any N case; `run_suite --freeze` wrote EXPECTED_OUTPUT.json only for cases whose spec passed; the record run then compared bytes. For R1, the c4v001 expected bytes are the oracle, carried mechanically by X1–X3 and four overrides, so any other change would fail.

## Rule notes (self-reported; also in PARTIAL.md)

- One unfenced Python run: early in the build, the codex python3 `-I -B` ran B1's read-only review aid `tools/view_c4v001.py` on one c4v001 EXPECTED_OUTPUT.json (nothing written). Every other Python run used the fenced runner; outputs were then read with jq.
- One recursive listing: `find -type f` over the copied regression trees (B1 source and B2 copies) to check the copies byte-equal. The HASHES file list was built by non-recursive `ls` of each named folder.
- `run_suite_c4v002.py` was edited in place once after its two dev runs (to read the latest N spec revision); classifier drafts were edited only before their first run, and a fix after a run went into a new draft (d01 → d02); the deliverable is a byte copy of d02.
- The V006 addendum was read by a section filter that printed only the A142, A144 and A149 sections (no other heading). Reads of the phase1 files, v003g, the dispatch, the V006 sections and the basis diffs used `taskpolicy -b`; some reads of build_c4v001 files did not (the two briefs, the c4v001 classifier through the Read tool, case files and the verifier's expectations through jq, a grep of its case defs, the head of its HASHES file).
- R2 case V84 makes the classifier `realpath` a non-existent path outside the build (`/Users/bgm/Research/elsewhere/CAL.json`), as the verifier disclosed; it reads no file.
