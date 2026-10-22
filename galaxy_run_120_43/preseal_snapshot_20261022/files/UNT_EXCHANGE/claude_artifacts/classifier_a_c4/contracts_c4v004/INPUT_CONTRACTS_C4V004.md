# INPUT_CONTRACTS_C4V004: the root-written input records of classifier A, with the `schema` key shown

Lane Claude4, 2026-10-19T20:08:49Z (`date -u`). Ruling: V006 A173, OI-A1 (a) (root dispatch 0746).

**Scope.** This is wording only. It adds no rule and changes no classifier. Every key set below is quoted from the line of `classifier_a_c4v004.py` (sha256 `e92aa30e22b98fea6c6e517702c02f77c43bfe429f69f8e0392963c94edc4cb0`) that checks it.

**What it replaces.** The record list of README_CLASSIFIER_A_C4V001 L74-L82, as amended by c4v002 C1-C5 and c4v003 C6-C9 (re-adopted in A168). That list gave each contract name only in parentheses and never showed the `schema` key, which the code has always required.

**General rule.**
- Each record is one JSON object. Its `schema` value is its contract name, and it has exactly the keys shown, no others, unless its row says otherwise.
- Strings are non-empty.
- Times are `date -u` ISO strings: `YYYY-MM-DDTHH:MM:SS[.ffffff]Z`.
- A **pin** is exactly `{path, sha256}`: a non-empty string path and 64 lower-case hex (`_pin_ok`, L380-382).
- The bundle role is the key under the bundle's `inputs` (`INPUT_ROLES`, L200-202).
- Failure readings are as in README_CLASSIFIER_A_C4V004 (the bundle table).

| # | Bundle role | `schema` value | Exact keys (code line) |
|---|---|---|---|
| 1 | `phase_inputs` | `PHASE_INPUTS_C4V001` | `{schema, phase_named, phase1_registry_root, phase2_registry_root, run_status, run_status_code, phase1_header, phase1_classification_absent_reason}` (L589-591) |
| 2 | `gate_status_list` | `GATE_STATUS_LIST_C4V001` | `{schema, gates}` (L734) |
| 3 | `tsr_flag_record` | `TSR_FLAG_RECORD_C4V001` | `{schema, target_free, rule, failing_ring_ordinal, ntest_compare_pin, n1_record_pin, gl_node_record_pin, flags}` (L679-681) |
| 4 | `stage0_status` | `STAGE0_STATUS_RECORD_C4V003` | `{schema, phase, sealed_successor, step4_start_utc, members, rule_a_receipts_finished, rule_b_successor_sealed, receipts_before_step4, receipt_refusals, evaluation_refusals, reading, reasons, post_score_exploratory}` (L82-85, L1391-1392) |
| 5 | `commitment_status` | `PHASE2_COMMITMENT_STATUS_C4V001` | `{schema, status, stops_or_changes}` (L2000-2001) |
| 6 | `fallback` | `FALLBACK_RECORD_C4V001` | A checks `schema` and a boolean `applies` only (L2495). Every other key is echoed as written (item 10). Root writes exactly `{schema, applies, classification_label, seal_candidate, pre_prediction_shas, post_prediction_changes}`. |
| 7 | `field_map` | `KEY_FIELD_MAP_C4V001` | `{schema, renames}` (L434) |
| 8 | `root_disclosures` | none | Any JSON object, echoed in the header (L2520-2521). A does not read a `schema` key here. A missing record prints NOT_AVAILABLE [ROOT_DISCLOSURES_NOT_SUPPLIED]. |

**Nested forms and value rules (as checked):**

1. **Phase inputs.**
   - `phase_named` is `PHASE_1` or `PHASE_2`. Both registry roots are absolute paths.
   - `run_status` is one of `SCORED`, `NO_NGC_CALL`, `AT0A_FAILED` or `HALTED`, and must be of the named phase (L581-582, L610-611). `run_status_code` is null or a string.
   - `phase1_header` is null or exactly `{b_p1, u_a_log_index, phase1_record_sha256, l1_sha256}`: two integers and two 64-hex values (L603-606). A scored Phase 1 requires it (L612-613).
   - `phase1_classification_absent_reason` is null, `AT0A_FAILURE` or `NO_PHASE_1_SCORE` (L608).
2. **Gate-status list.** `gates` is a list. Each entry is exactly `{gate_sha256, status, pinned_by_entry}`:
   - `gate_sha256` is 64 hex in either case, compared lower-cased, with no repeats;
   - `status` is `ON-TIME` or `LATE`;
   - `pinned_by_entry` is a non-empty string, such as the V006 heading text (L739-741).
3. **TSR flag record** (rulings M-7).
   - `target_free` is true, `rule` is a string, and `failing_ring_ordinal` is 15 (`FAILING_RING_ORDINAL`, L63).
   - The three pins carry fixed shas:
     - `ntest_compare_pin`: `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9`;
     - `n1_record_pin`: `8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70`;
     - `gl_node_record_pin`: `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` (L58-60, L684-690).
   - `flags` holds 43 objects, each exactly `{query_id, TRUNCATION_SHAPE_RESIDUAL}`. They are in manifest order with a boolean flag, and exactly `NGC3198-Q25` is flagged (L54, L698-704).
   - The record's own sha and the three pinned shas must be among the freeze manifest's `pins.input_files` (L689-693).
4. **STAGE0 status record** (Phase 2; A154, A168 F1).
   - Each `members` entry is exactly `{log_index, terminal_status, written_utc, finished, before_step4}` (L86).
   - **With the STAGE0 successor pinned,** the record is optional. If supplied, it must equal the exact projection of the frozen `stage0_status` block (L1457-1461).
   - **Without the successor,** it is read vacuously: the reason is NO_SEALED_SUCCESSOR only (A168 F1).
5. **Commitment status.**
   - `stops_or_changes` is a list of objects, each exactly `{what, entry}` with two non-empty strings.
   - `COMMITTED` takes an empty list, and `EXPLORATORY` a non-empty one (L2000-2007).
6. **Fallback record** (C-8 item 10). `classification_label` is null, `EXPLORATORY (post-prediction)` or `POST-PREDICTION (CLASSIFIER)`, as in the earlier contract text.
7. **Field map** (C-1.1).
   - `renames` maps each input role, other than `field_map`, to a list of objects, each exactly `{at, from, to}`.
   - `at` is a string. `from` and `to` are non-empty and differ. Keys only (L437-444).

**Not root-written, listed for completeness.** These are records of pinned producers, carrying those producers' own `schema` values:
- the freeze manifest (v003g, or the STAGE0 successor `FREEZE_MANIFEST_C2V003G_STAGE0_C2V002`), the score, the slots, `ntest_compare`, the `agree` record (phase1 v002 `d64351ec` or v003b `7d891ff7`), the Phase-1 classification, the L1 record and the M-13 C3 record;
- the TSR support record, role `tsr_support_record` and `schema` `UNT_ROOT_TSR_SUPPORT_CX3V001`, with exactly `{schema, mode, target_free, before_target_access, point_key, slots_pin, ntest_compare_pin, rule_id, rings}` (L705-707).

**Against the earlier text, wording only:**
- `schema` is shown in every root-written record;
- the fallback row says what A checks;
- root disclosures are stated as an open object.
