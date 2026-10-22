# Classifier A (lane Claude4), build c4v001: the M-12 Implementation A for the miss-reading prereg r3a

**What it is.** `classifier_a_c4v001.py` is the mechanical, target-blind classifier of ROOT_ITEMS M-12, Implementation A. It implements the r3a text of record (`basis/PREREG_MISS_READING_R3A.md`, `1e17eb45…`) §1 to §9, with ROOT_ITEMS_R3A (`9c40b567…`) as ruled in A142 (rulings draft `0f45f3c4…`: M-1 (a′), M-3 (A)+(alpha), M-4 (i), M-5 with both additions, M-7 (i), M-8, M-9 tightened, M-10 with precedence, M-12 (i)–(v), M-13 fields, M-14, M-15 (a)+(1), M-16 (1)) and the A144 phase1 v003 encodings. Root runs it on the real score; its output tables are the report's tables (§8). Classifier B (Codex1) is built separately; nothing of B or of its predecessor was opened.

**Status of this build.** Built and suite-tested on synthetic, target-free inputs only. It has not been run on any real manifest or score. The open choices below are raised for root; none is silently decided, but each needs a value for the code to run, so each is listed with the value classifier A uses and the case that pins it.

**Files** (sha256 in `HASHES_C4V001.txt`):

| file | role |
|---|---|
| `classifier_a_c4v001.py` | the classifier (stdlib only, Python 3.12) |
| `run_suite_c4v001.py` | runs every suite case; checks the hand spec, then the output bytes |
| `suite/case_defs_c4v001.py` | the 206 case definitions, each with hand-written expectations, clauses and derivation |
| `suite/build_suite_c4v001.py` | writes the case folders from the definitions (exclusive create) |
| `suite/SUITE_INDEX_C4V001.json` | every case with its M-12 class and clauses |
| `suite/cases/<id>/` | per case: `BUNDLE.json`, its inputs, `EXPECT_SPEC.json` (plus `EXPECT_SPEC_R1.json` for 3 revised cases) and `EXPECTED_OUTPUT.json` |
| `suite/common/` | the synthetic slots query block (target-free ids and radii), a byte copy of the target-free N-test compare `6f095f64…`, stand-ins for the sealed classifier, STAGE0 successor and a phase1_c2v003 pin |
| `SUITE_RESULTS_C4V001.json` | the record run: 206 cases, 206 spec passes, 206 byte-equal |
| `tools/run_fenced_c4ep1.py`, `tools/fence_c4v003.py` | the fenced runner (EXPECTED_BUILD set to this folder; nothing else changed) and its fence |
| `tools/view_c4v001.py` | a review aid that pretty-prints one output |
| `work/` | development runs (`run01`–`run05`), outputs viewed by eye, `view_*.txt` |
| `PARTIAL.md` | the append-only progress log |

## How to run

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  taskpolicy -b <codex python3> -I -B B/tools/run_fenced_c4ep1.py B/classifier_a_c4v001.py BUNDLE.json OUT.json
```
`OUT.json` is created exclusively. The importable entry point is `classify_bundle(bundle_path) -> bytes`. The suite: `run_suite_c4v001.py RESULTS.json [--classifier PATH] [--freeze]`.

## The input bundle (`CLASSIFIER_A_BUNDLE_C4V001`)

One strict JSON object with exactly these keys. Every path may be absolute or relative to the bundle's folder. Every pin is `{"path": str, "sha256": 64 lowercase hex}`; the classifier hashes the bytes and refuses to parse an input whose bytes differ (the input then counts as missing, in its role's map class below). A malformed bundle refuses the run (`{"refused": true, "reason": "BUNDLE_…"}`).

| key | content |
|---|---|
| `schema` | `CLASSIFIER_A_BUNDLE_C4V001` |
| `mode` | `score` (the full classification with the re-run stops) or `prescore` (every stop checked on a synthetic score built from the frozen member arrays; C-1.1 "Pre-score checks") |
| `inputs` | an object with exactly the 17 roles below, each a pin or `null` |
| `rosters` | `{alternative name: pin}`: the v003g row-registration rosters (schema `ROOT_ROW_REGISTRATION_ROSTER_CX3V001`); the classifier reads `schema` and `root_gates` |
| `sealed` | `{"text": pin, "classifier": pin, "tsr_flag_record_sha256": hex, "stage0_successor": pin or null}`: the shas of the seal entry (SEAL_SHA_MISMATCH checks them against bytes) |
| `phase1_tool` | `{"sha256": hex, "module": "phase1_c2v002" or "phase1_c2v003"}`: the `band`/`agree` pin of the seal entry (A142 item 4). `d64351ec…` must name `phase1_c2v002`; any other sha must name `phase1_c2v003` (see OC-18) |
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
| `tsr_support_record` | schema `UNT_ROOT_TSR_SUPPORT_CX3V001` (extractor `50c7db5f…`) | always | TSR_FLAG_TABLE_MISMATCH (OC-06) |
| `ntest_compare` | the N-test record of record (`6f095f64…`) | always | TSR_FLAG_TABLE_MISMATCH |
| `stage0_status` | root-written, schema below | Phase 2 | the STAGE0 alternative reads TWIN_INPUT_DEFECT (OC-04) |
| `commitment_status` | root-written, schema below | Phase 2 | EXPLORATORY with COMMITMENT_STATUS_DEFECT; blanks nothing; never NOT_READ |
| `agree_record` | the A133 `agree` record (OC-02) | Phase 2 | §8 item 11 NOT_AVAILABLE (AGREE_RECORD_DEFECT); never NOT_READ |
| `phase1_classification` | classifier A's own Phase-1 output | Phase 2 | the cross-phase items NOT_AVAILABLE (PHASE1_CLASSIFICATION_INPUT_DEFECT); never NOT_READ |
| `l1_record` | the pinned `band` command's `L1_C2V001.json` (schema `PHASE1_L1_C2V001`) | Phase 1 | the Phase-1 band column only (L1_SHA_MISMATCH, L1_RECORD_DEFECT, L1_ROW_DEFECT); never NOT_READ |
| `c3_record` | the M-13 record: `per_grid.T120L.C3_max_e` (finite) and `per_grid.T120L.C3_PASS` (bool) are read | P8 report | that half of the P8 report NOT_AVAILABLE |
| `root_disclosures` | any JSON object (D-4 values, attestation, V005/V006 shas, RUNBOOK_V002/roster-builder/step-map shas, window changes, `outer_gas_cut_report`) | header | echoed; absence noted |
| `fallback` | root-written, schema below | under the fallback | item 10 NOT_AVAILABLE |
| `field_map` | the key-only field map, schema below | only if pinned | not applied (header `FIELD_MAP_DEFECT_NOT_APPLIED`); the stops stand |

**What is read from the v003g files** (M-5, bound to `48a1e48a…` by reading its `score_after_freeze`, `_score_members`, `_ladder_row`, `_band_rows`, `_pointwise_envelope`, `_alternative_score_scope`, `_authorized_row_registration`, `_root_frozen_rows`):
- score: `headline.reference_member_id`, `reference_member_log_index`; `members[].member_id`, `log_index` (all members), the reference member's `member_valid` and `rows[].{id, score_status, within_error, sigma_ratio, registered_reason, status}`; in Phase 1 also its `rows[].observed_speed_km_s` and `quoted_sigma_km_s` (the target pair, band column only); `pointwise_envelope.label` (prefix) and `rows[].{id, valid, band_overlaps_error_bar}`; `sensitivity.rows[].{id, valid, band_overlaps_error_bar}` (Phase 2); `alternatives[].{name, kind, status, role, scored, members, scoring_scope}`; `freeze_status`, `incomplete_reasons`; the headline counts are echoed.
- manifest: `reference_member.{member_id, log_index}`; `members[].{member_id, row_registration}` (the gate sha of a gate row); `alternative_results[name].members[].{log_index, row_registration}`; `input_bindings.calibration_record.path`; `pins.input_files[].sha256`. In prescore mode also `query_ids`, `members[].{speeds_km_s, row_valid, …}`, `pointwise_envelope[]`, `sensitivity.per_query[]`, `alternatives`, `freeze_status`, `incomplete_reasons` (to build the synthetic score; `synthesize_score`).

### Root-written input contracts (minimal strict schemas; root and classifier B adopt them)

Every one is a JSON object with exactly the keys shown; strings are non-empty; times are `date -u` ISO strings `YYYY-MM-DDTHH:MM:SS[.ffffff]Z`.

- **Phase inputs** (`PHASE_INPUTS_C4V001`): `phase_named` (`PHASE_1`/`PHASE_2`, the phase the score entry names); `phase1_registry_root` (the absolute path the seal entry names); `phase2_registry_root` (absolute; OC-07); `run_status` (`SCORED`, `NO_NGC_CALL`, `AT0A_FAILED`, `HALTED`); `run_status_code` (string or null, e.g. the engine terminal status); `phase1_header` (Phase 1: `{b_p1: int, u_a_log_index: int, phase1_record_sha256, l1_sha256}` — the L1 sha logged at the Phase-1 freeze; Phase 2: null); `phase1_classification_absent_reason` (null, `AT0A_FAILURE` or `NO_PHASE_1_SCORE`).
- **Gate-status list** (`GATE_STATUS_LIST_C4V001`): `gates`: a list of `{gate_sha256, status: ON-TIME|LATE, pinned_by_entry}`, one per gate document sha, no repeats (C-4, M-15). Identity is the gate document's sha256, as in the v003g roster `root_gates` pins.
- **TSR flag record** (`TSR_FLAG_RECORD_C4V001`): `target_free: true`, `rule` (text), `failing_ring_ordinal: 15`, `ntest_compare_pin`, `n1_record_pin`, `gl_node_record_pin` (pins with shas `6f095f64…`, `8867c376…`, `ec1dcca5…`), `flags`: 43 `{query_id, TRUNCATION_SHAPE_RESIDUAL: bool}` in manifest order. Its own sha and the three pinned shas must be among the freeze manifest's `pins.input_files` (C-1.4; rulings M-7).
- **STAGE0 status record** (`STAGE0_STATUS_RECORD_C4V001`, Phase 2): `registered_members`: a list of `{log_index, terminal_receipt (FINISHED or another A133 rule-(c) status), receipt_written_utc}`; `phase2_step4_start_utc`; `successor_refused_a_record: bool`; `result_first_available_utc` (time or null). Condition (b) is the bundle's `sealed.stage0_successor` being non-null.
- **Commitment status** (`PHASE2_COMMITMENT_STATUS_C4V001`, Phase 2): `status` (`COMMITTED` with an empty `stops_or_changes`, or `EXPLORATORY` with a non-empty one); `stops_or_changes`: `[{what, entry}]`.
- **Fallback record** (`FALLBACK_RECORD_C4V001`): `applies: bool`, `classification_label` (null, `EXPLORATORY (post-prediction)` or `POST-PREDICTION (CLASSIFIER)`), `seal_candidate`, `pre_prediction_shas`, `post_prediction_changes` (echoed as item 10).
- **Field map** (`KEY_FIELD_MAP_C4V001`): `renames: {role: [{at, from, to}]}`; `at` is a container path such as `members[].rows[]` or `pointwise_envelope.rows[]` (`""` is the root). Keys only; a rename onto an existing key is refused.
- **The M-13 C3 fields** are read from the pinned record as named above.
- **The A133 `agree` record** (OC-02): the `PHASE1_AT1_C2V001` record of the pinned `agree at1`; when AT-1 was not run, the `PHASE1_AT0A_C2V001` or `PHASE1_AT0B_C2V001` record, accepted only with outcome `AGREEMENT_DEFECT`. Its `module` must equal the pinned tool's. v002 encodings (`d64351ec…`): failing entries have exactly `{log_index, id, excess, norm_n, category, flag}`, categories OUTSIDE_TRUST_RADIUS, OUTSIDE_LINEAR_DDO_REGION, NGC_NONLINEAR, flag null or FD_NOISE_NOT_BOUNDED; `reported` carries the seven v002 keys. v003 encodings (A144): failing entries add `region_rows_violated` (in the order TRUST_RADIUS, BOX, LINEAR_DDO), `region_max_violation` (one number per family), `geometric_part`, `residual_part`, `flag_reason` (null, FD_NOISE_NOT_BOUNDED, MEMBER_POINT_NOISE_NOT_BOUNDED), category OUTSIDE_BOX_SLICE added, and the category must be the first violated family's (NGC_NONLINEAR iff the list is empty); `reported` adds `pairs_member_point_noise_not_bounded`, `band_region_extent`, `band_region_single_point` (true, false or NOT_AVAILABLE) and optionally `band_region_single_point_reason` (BOX_CORNER, OTHER_ROWS). Under AGREEMENT_DEFECT, `failing`, `non_discriminating_rows` and `reported` may be absent.

## The output (`CLASSIFIER_A_OUTPUT_C4V001`)

Canonical JSON: `json.dumps(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)` and a newline. Floats appear only where the text prints a value (r_q, m(Z), Δ_out, the far-half median, A_P/A_S and the twin r_q of DT-S0G, echoed record values); R_q is printed as the registered `Rad_text`. An output that the stop-to-output map blanks is `{"NOT_AVAILABLE": [codes]}`. UNDEFINED quantities print `"UNDEFINED"`.

Top level: `schema`, `classifier`, `mode`, `phase`, `status` (`CLASSIFIED`, `NOT_READ` or `NO_CLASSIFICATION`), `status_code` (the stop codes, or the run status), `stops` (each `{code, class, alternative, detail, rows}`), `labels` (the PROVISIONAL / EXPLORATORY labels; also repeated inside every pattern, reading, zone summary, the E3 line and DT-S0G), and the §8 items:

| §8 item | keys |
|---|---|
| 1 header | `header` (phase; Phase-1 label, B_P1, u_A log index, Phase-1 record and L1 shas; sealed text and classifier shas; manifest, slots, module and roster shas; the score's manifest/registration echo; TSR record shas; the gate-status list; the STAGE0 status with step-4 start and receipt times; the freeze status; the commitment status and `agree` / Phase-1 input shas in Phase 2; the Phase-2 attestation scope; D-1 to D-3; `root_disclosures`) and `headline` (the freeze module's, echoed; I-5) |
| 2 per-row table | `rows`: `id, zone, R_q, tier, reading_kind, r_q, sign, frozen_prediction, near, tsr_flag, invalid_reason, gate_status, gate_after_predictions, sensitivity_band_overlap, sensitivity_band_label, phase1_band` (Phase 1: `overlaps`, `fd_noise_not_bounded`, label, A13 condition)`, notes, tier_key` |
| 3 zone summaries, OUTER_FAILURE, E3 | `zones` (N_v, H, M, U, I, I per reason, miss-/hit-dominated, "S is UNDEFINED", m, S, N), `outer_trend`, `outer_failure`, `e3_line` |
| 4 patterns and flags | `patterns` (P0–P15, P1g, P11g; P13 sign class; P0 per zone and reason; the P8 companions), `patterns_holding`, `minority_miss`, `flagged_rows` |
| 5 readings | `readings`: in C-3.2 order, each `{reading, triggers_holding, part1 {relation, code}, part2, part3_prior_evidence, sign_scope, scope_zones, cited_miss_rows, cited_miss_rows_not_available}` (R-HIST also `qualifier_missing_long_range_component`); `descriptive` (onset radius, DT-T1a) |
| 6 INVALID list | `invalid_list` (per reason, with zone and gate status; LATE rows marked GATE_AFTER_PREDICTIONS; the outer-gas cut report) |
| 7 A15 comparisons | `a15` (E1 (a) with the Q03–Q15 sub-table, E1 (b) NOT_AVAILABLE per M-11; E2) and `p8_report` |
| 8 alternatives | `alternatives` (declared order, STAGE0 last) and `stage0` (status, reasons, times, SENSITIVITY label only when evaluated, the twin classification and the DT-S0G comparison) |
| 9 | `exploratory_readings` (always empty: none is registered) |
| 10 | `fallback` |
| 11 (Phase 2) | `agreement` (outcome, NON_DISCRIMINATING rows, failing (member, row) list, the target-free always-reported items, the Phase-1 consequence, the withdrawn items under SUPERSEDED, the cross-phase items) |

`prescore` mode prints `{schema, classifier, mode, phase, manifest_phase_derived, result: PASS | CLASSIFICATION_INPUT_DEFECT, stops, not_stop_inputs, field_map}`.

## Rule-to-function map

| text rule (section, tag) | function(s) |
|---|---|
| strict parsing (M-12, A71): duplicate keys, NaN, ±Infinity, overflow refused; nothing last-wins | `strict_loads`, `_pairs`, `_const`, `_float` |
| inputs verified by sha before parsing (brief item 1) | `read_pinned`, `load_inputs`, `load_bundle` |
| rule M-T tiers, null ratio (C-1.1); LATE rows (C-4) | `build_rows` |
| sign (C-1.2) | `sign_of` |
| zone rule and membership by id; ZONE_TABLE_MISMATCH (C-1.3) | `check_zone_table` |
| TSR flag, overlap rule, carrier, TSR_FLAG_TABLE_MISMATCH (C-1.4, C-1.1) | `check_tsr` |
| NEAR flag (C-1.1, C-I7) | `score_output` (NEAR block), `check_envelope` |
| sensitivity column (C-1.1) | `check_sensitivity`, `score_output` |
| Phase-1 band column (C-1.1, M-16) | `band_column`, `_tool_module` |
| pre-score checks and stops: reference member status and identity, field checks, ids, envelope label (C-1.1, M-5) | `check_score`, `check_envelope`, `check_alternatives` |
| GATE_STATUS_LIST_DEFECT, ON-TIME/LATE (C-1.1, C-4, M-15) | `check_gate_list`, `_frozen_registration`, `_kinds_of_registration` |
| SEAL_SHA_MISMATCH (C-1.1, M-6) | `check_seal` |
| PHASE_MISMATCH (C-1.1) | `check_phase`, `_phase_inputs_ok` |
| pre-score run on a synthetic score built from the frozen arrays (C-1.1) | `synthesize_score`, `prescore_output` |
| field map (C-1.1 "Rename a field") | `_field_map_renames`, `_apply_rename` |
| NOT_READ and the closed stop-to-output map, several stops (C-1.1) | `stop`, `stops_out`, `zone_vectors`, `engine` (count-level enumeration and the listed deductions), `readings` (three-valued tuple parts), `score_output` |
| zone summaries, sign class, dominance, outer trend, OUTER_FAILURE, patterns P0–P15, P1g, P11g (C-2) | `vec_counts`, `engine`, `zone_out`, `median` |
| readings: tuple, part-1 order, A10 rule, MINORITY_MISS, A15 E3 rule, scope, deficit-type sign rule, prior evidence (C-3, C-3.1, C-3.2) | `readings`, `drift_part2` |
| descriptive lines: onset radius, DT-T1a (C-3) | `engine` (onset), `score_output` |
| INVALID list (C-4, C-8 item 6) | `invalid_list` |
| A15 E1, E2 (C-5.1, C-5.2); E3 line (C-5.3) | `a15`, `score_output` (E3 block) |
| P8 report (C-3.2, M-13) | `p8_report` |
| twin rule, TWIN_INVALID, TWIN_INPUT_DEFECT (C-6.1, M-10) | `twin_rows`, `classify_twin`, `twin_row_out`, `prepare_alternatives`, `alternatives_out` |
| alternatives not evaluated (C-6.2); Phase-1 precedence (C-I4, M-10) | `alternatives_out`, `check_alternatives` |
| STAGE0 receipt rule and statuses (C-6.3, M-14) | `stage0_status`, `stage0_block` |
| DT-S0G comparison, M-9 as ruled, R-DRIFT mapping (C-6.3) | `s0g_compare`, `drift_part2`, `readings` |
| labels: PROVISIONAL (PHASE-1 …), PROVISIONAL (FREEZE_INCOMPLETE), PROVISIONAL (N_GATE_NOT_OPEN), EXPLORATORY (C-I6, C-I7, M-8) | `labels` |
| commitment status (C-I7) | `commitment` |
| no classification (C-I7) | `run` |
| header (C-8 item 1); headline (C-I5) | `header`, `headline_out` |
| item 10 (C-8) | `fallback_out` |
| item 11 (C-8), the A133 `agree` record binding (C-1.1 map, A144) | `agreement`, `parse_agree`, `_p1_ok` |

## The NOT_READ map as implemented (C-1.1)

- Each defective reference row (class ROW) takes every allowed kind: HIT, signed MISS, null-ratio MISS, plus INVALID_AS_MISS (or LATE-gate MISS for a LATE gate) when its frozen registration is INVALID (OC-12). Each row of a gate missing from the list (class GATE) takes INVALID_AS_MISS and LATE-gate MISS. The reachable count vectors are enumerated per zone, and cross-zone outputs over the product of per-zone feature sets.
- Count-level outputs (N_v, H, M, U, I per zone; dominance; "S is UNDEFINED"; OUTER_FAILURE; E3; P0, P5, P7, P8, P9, P10, P13, P14, P15; MINORITY_MISS; the onset radius) print when they take one value over every assignment.
- Every other output computed from a defective row reads NOT_AVAILABLE unless one of the listed deductions fixes it; the list is applied as closed (OC-10).
- Each reading's part prints when the printed outputs fix it (three-valued evaluation of triggers, the against-condition and the sign rule).
- Other classes: ENVELOPE (NEAR and N(Z) on the rows), SENSITIVITY (that column), ALT (that alternative: TWIN_INPUT_DEFECT; R-DRIFT by C-6.3), TSR (P10, R-TSR, the flag column and the flagged-row list), ALL ("every other": every output except the header and the echoed headline). The band-column inputs, the item-11 inputs and the commitment status never stop.
- Several stops: every code is printed; the row and gate classes are enumerated jointly (OC-11); each other class blanks its own outputs.

## Open choices (raised, not decided; the value used and the pinning case are given)

| id | the question the text leaves open | classifier A uses | case | class |
|---|---|---|---|---|
| OC-01 | I-7 / C-1.1: "When E_q.valid = false, NEAR reads NOT_AVAILABLE; N(Z) then reads NOT_AVAILABLE" against "a row of tier INVALID_AS_MISS never carries NEAR". v003g marks Q01/Q02 envelope rows invalid in every honest score (no member is valid there), so the literal I-7 sentence makes N(INNER) NOT_AVAILABLE always | NEAR is a flag of tier-MISS rows only; an invalid envelope row blanks NEAR and N(Z) only on a tier-MISS row | T231, T001 | text SHOULD_FIX |
| OC-02 | What "the A133 `agree` record" is: the pinned `agree` command writes three records (AT0A, AT0B, AT1) | the AT1 record; when AT-1 did not run, the AT0A/AT0B record with AGREEMENT_DEFECT | T137, T138, T148 | text SHOULD_FIX |
| OC-03 | Whether the onset radius ("the smallest R_q of a MISS row") counts LATE-gate rows (MISS for counts and patterns, INVALID_AS_MISS in LADDER) | counted as MISS rows | T224 | text SHOULD_FIX |
| OC-04 | The map class of a defective Phase-2 STAGE0 status record (M-5 input; "a field outside the rows" vs "a field of an alternative") | the alternative class: STAGE0 reads TWIN_INPUT_DEFECT, R-DRIFT OPEN | T052 | NOTE |
| OC-05 | Twin rows registered by a gate missing from the gate-status list (the row rule speaks of the reference rows) | that alternative reads TWIN_INPUT_DEFECT | T229 | NOTE |
| OC-06 | The TSR support record: required (M-5) and a stop input (C-11), but the C-1.1 stop list does not name it, and the M-7 ruling has one producer (root's flag record) with the extractor output "a cross-check only" | required; any difference from the C-1.4 record fires TSR_FLAG_TABLE_MISMATCH | T079 | text SHOULD_FIX |
| OC-07 | The Phase-2 registry root (needed for "neither contains the other") is not in M-5's input list, and the text names no stop for non-disjoint registries | read from the phase-inputs record; non-disjoint reads PHASE_MISMATCH | T090 | NOTE |
| OC-08 | Codes for the stops the text does not name | REFERENCE_ROW_UNEVALUATED_OR_REFUSED, QUERY_ID_DEFECT, ENVELOPE_LABEL_MISMATCH, ZONE_TABLE_MISMATCH, FIELD_DEFECT_ROW / _ENVELOPE / _SENSITIVITY / _OUTSIDE_ROWS / _ALTERNATIVE; band codes L1_SHA_MISMATCH, L1_RECORD_DEFECT, L1_ROW_DEFECT, L1_ROW_NOT_AVAILABLE, TARGET_PAIR_DEFECT, Q01_Q02_ALWAYS_NOT_AVAILABLE; AGREE_RECORD_DEFECT, PHASE1_CLASSIFICATION_INPUT_DEFECT, ENVELOPE_ROW_INVALID | many | NOTE (A and B must share them) |
| OC-10 | The closed deduction list is narrower than three-valued logic: P1g/P11g stay NOT_AVAILABLE when P1/P11 print false but a TRANSITION/OUTER row is defective; Δ_out reads NOT_AVAILABLE for a TRANSITION-only defective row; S(Z) reads NOT_AVAILABLE even when "S(Z) is UNDEFINED" prints true; the E3 line's defined/LATE/null-ratio counts are not on the count-level list | applied literally (as listed) | T064, T065, T082 | NOTE |
| OC-11 | Several row-level stops (a row field and the gate list) at once: joint or separate enumeration | joint (one defective set, kinds by class) | — | NOTE |
| OC-12 | "INVALID_AS_MISS for a row the roster registers INVALID" | the reference member's frozen registration in the manifest | T182 | NOTE |
| OC-13 | Which members' fields are checked (M-5 lists `members[]` fields) | member_id and log_index of every member; member_valid and the row fields of the reference member only | — | NOTE |
| OC-14 | "Wrong type" | includes the enumerations (score_status, status), a string registered_reason on an INVALID_AS_MISS row, and a finite sigma_ratio on a within-error row | T181 | NOTE |
| OC-15 | PROVISIONAL (N_GATE_NOT_OPEN): "the gate was not OPEN when that run launched" has no input carrying the gate at launch | the N-test record of record's `n_route_ab_gate`; unreadable reads not OPEN | T078 | NOTE |
| OC-16 | RECEIPTS_AFTER_STEP4 is listed among the "STAGE0 statuses" (M-12) but C-6.3 makes it a result first available after step 4 | NOT_EVALUATED_BEFORE_FREEZE with reason RECEIPTS_AFTER_STEP4 | T050, T051 | NOTE |
| OC-17 | Row scope ("rows of the zones its triggering patterns name"): whether HIT rows are listed | the MISS rows with a frozen prediction, plus the scope zones | many | NOTE |
| OC-18 | The phase1_c2v003 encodings: v003 is not yet posted, so its sha is unknown and the A144 key names are bound without the bytes | a pin naming module `phase1_c2v003` binds them; `band_region_*` read from `reported`, `flag` optional in v003 failing entries, the reason key `band_region_single_point_reason`; to be re-checked against the v003 bytes, with a classifier successor if they differ | T130, T141–T143 | open item before the seal |
| OC-19 | Whether the echoed freeze-module headline and the header print under an "every other" stop | both print | T069 | NOTE |
| OC-20 | L1 `lo > hi` (not a type defect) and a non-positive quoted sigma | not checked; the target pair requires sigma > 0 | — | NOTE |
| OC-21 | M-12 names witness sets (Codex2 0490 witnesses verbatim; newdefects C14, C15, C16b, C17d, C40, C16d; closure U1, U2, L1–L4; refuters' G1, G4, G5, G6, U1Lt) whose definitions are in files outside this build's read list | the suite carries class analogues (null-ratio, LATE, P14/P15, thresholds, E_tie, E_one, E_hit_majority, all-hit, P10G/P10L), not those witnesses verbatim | — | suite gap for root / B to fill |
| OC-22 | An alternative the text says is "never scored" (ML, GL10) that the score marks evaluated and scored | classified by the twin rule (C-6.1) | T061 | NOTE |
| OC-23 | Root-written input formats (the section above) | as defined here | all | for root and B to adopt |

## The suite

- **206 cases** (`suite/SUITE_INDEX_C4V001.json`), all synthetic and target-free. Coverage against M-12: every tier, flag and pattern (P0–P15, P1g, P11g) and zone counts with U (T001–T037); the E3 line and its counts; every reading tuple and NOT_ADDRESSED code (SIGN_SCOPE_EXCESS T004, _UNSIGNED T008, _NO_DEFICIT_MISS T007); the twin rule (T054–T061); PROVISIONAL FREEZE_INCOMPLETE (T105, T227) and N_GATE_NOT_OPEN (T078); every stop and NOT_READ (T064–T099, T181, T182), one case per map class (row T064, envelope T094, sensitivity T095, L1 T119/T121, target pair T124, `agree` T139, Phase-1 input T144, commitment T152, alternative T096, TSR T077, gate list T082, every other T069–T076, T085–T091), several stops (T092, T093); the STAGE0 statuses with the tie case (T038–T053, T222, T223); the checklist classes; the round-2 classes (null ratio, LATE, P14, P15); the refute witnesses W1, W1b, W1c, W2, W3, W7, W8, W9, W10, W11, W12; the LATE-against-on-time pairs for every pattern change C-4 lists (T031/T032, T034–T037, T200–T221); the Phase-1 cases (T113–T133, T226, T228); the Phase-2 cases (T135–T153); the A142 additions (honest NOT_AVAILABLE L1 rows T118; fd_noise string and object T117; Q01/Q02 always NOT_AVAILABLE T113, T123; a target-pair key defect T124, T125; both M-9 mixed cases T041, T042; Phase-1 ORIGINAL_K T058); the delta-check fixes (both item-11 inputs defective T146; AGREEMENT_DEFECT with a defective Phase-1 input T147; several stops T092); prescore (T156–T166); strict parsing of each input kind (T066–T068b, T132, T167–T170).
- **Method.** Each case's expectations (`EXPECT_SPEC.json`) were written by hand in `case_defs_c4v001.py`, with the clauses and the derivation, before the classifier was run on that case. `run_suite` checks them; `--freeze` then writes `EXPECTED_OUTPUT.json` (exclusive create) only for cases whose spec passes, and later runs compare the output bytes. So the byte files are the classifier's own outputs, admitted only after the pre-written expectations held; the expectations, not the byte files, are the independent oracle.
- **Spec revisions.** First run: 171 of 174 specs passed. The 3 failures were re-derived from the text and all three were errors in my specs (T026: R_q of Q30 is 18.13; T065: P6 is NOT_AVAILABLE, so R-S1 and R-GEO part 1 are too; T111: P5 also holds). They are corrected as `EXPECT_SPEC_R1.json` beside the original, with the reason; no classifier change was made for them. Every later case passed at its first run.
- **Record run** (`SUITE_RESULTS_C4V001.json`): classifier `06f169e2…`, 206 cases, 206 spec passes, 206 byte-equal. The empty folder `suite/cases/T068` is a generator abort (a raw-substitution target was absent) that the no-delete rule leaves in place; it holds no file, is skipped, and is replaced by T068b.

## Rule notes (self-reported; also in PARTIAL.md)

- Several early read commands on named program files (sed/grep/cat of the v003g module, the slots file, the phase1 tool and its README, the carrier extractor, the compare, the refute tools, the clause map) were run without the `taskpolicy -b` prefix. Every hash and the root files were read with it.
- To find the A142 and A144 sections, a `grep -n '^## '` listed every heading line of the V006 addendum (titles only); only the A142 and A144 sections were read.
- Shell heredocs (`cat >> … <<'EOF'`) were used twice to append Python source to `suite/case_defs_c4v001.py` (writing a file inside this folder; no Python was run that way). All Python ran through the fenced runner; no `python -c`, no system python.
- The harness saved one long `sed` output of the basis clause map to its own tool-results file, which was then read; it is a copy of this folder's basis bytes.
