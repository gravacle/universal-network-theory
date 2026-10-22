# CLAUSE_SOURCE_MAP_R2 — where each clause of PREREG_MISS_READING_R2 comes from

Claude4, dispatch 0585. One row per clause tag in the r2 text.

**Change classes**, relative to V001 (`6aecf0cb…`):
- **UNCHANGED:** the same rule, possibly reworded.
- **CLARIFIED:** the same intent, with a tie or vacuous case closed. Not from a ruling; it needs root's adoption under M-3.
- **CHANGED:** the rule changed because of the ruling named.
- **NEW:** not in V001.

Ruling ids are root addendum entries. "Code" means the v003g freeze module (`48a1e48a…`), with the named function or constant. Every source's sha is in §11 of the text.

| tag | clause | V001 origin | change | sources |
|---|---|---|---|---|
| C-P | binding principles | head, principles | CHANGED: adds the conditionality on the I-6 numerics, and quotes the A15 E3 scope | A10, A12.3, A15 E3, A20, A23, A41, A48; A64, A66, A81 (via I-6) |
| C-I1 | the rows; denominators 43 and 8 | I-1 | CHANGED: adds the STAGE0 denominator 8 | 0518 item 1; A65; RUNBOOK_V001 step 10; code `_alternative_score_scope`, `_score_members_on_rows` |
| C-I2 | quoted values only | I-2 | UNCHANGED | V001 I-2; 0518 |
| C-I3 | frozen quantities only | I-3 | CHANGED: the fields are named for v003g; radii are bound by id with the kpc unit check; adds the M-7 flag record | 0531 (roster binding, v003f B1); 0545 (v003g F2/F3); code REFERENCE_RULE, `_score_members`, `_band_rows`; A66.2 |
| C-I4 | the six declared alternatives | I-4 | CHANGED: the slots V003 list, with the STAGE0 row | slots V003 `alternatives.declared`; A16.2; 0518 item 5; A65; 0548 |
| C-I5 | headline | I-5 | UNCHANGED (now cites v003g HEADLINE_RULE) | code HEADLINE_RULE; D5 |
| C-I6 | numerics conditions | — | NEW | A64.1–A64.3 (K_big 32, N3′, coverage 91, C1′ scope); A66.1–A66.3 (N-test reading and blocking); the 0512 ruling logged in V005, in the trailing block after the A65 heading (N_PASS is the only input to route A/B); A81 RI-22 (θ/20), RI-23 (M_s 96/128, the slotting rule, LO_NGC); 0546 |
| C-I7 | freeze status | — | NEW | code FREEZE_COMPLETE / FREEZE_INCOMPLETE, `incomplete_reasons`, `allow_incomplete`; A50 PROVISIONAL rule (by analogy); root item M-8 |
| C-1.1 | tier rule M-T | §1.1 | CHANGED: exact v003g fields; the INVALID test now reads the roster-bound `score_status`; NEAR uses the PRIMARY pointwise envelope only; the sensitivity band is excluded; fail-closed stops added | code `_score_members` (score_status, tier, registered_reason, within_error, sigma_ratio), `_band_rows` (band_overlaps_error_bar), `score_after_freeze` (headline.reference_member_id, members, pointwise_envelope, sensitivity); WITHIN_ERROR_RULE; REFERENCE_RULE; 0518; 0531; root item M-1 |
| C-1.2 | sign | §1.2 | CLARIFIED: sign 0 is allowed | V001 §1.2 |
| C-1.3 | zone rule and membership by id | §1.3 | CHANGED: membership is fixed by query id from the target-free query block, with the edge radii; mismatch stops; equal to the STAGE0 scope | A15 E1, E2; slots V003 `query_block.rows` (Rad_text, Rad_unit), source manifest `a2936517…`; code `_alternative_score_scope`; 0545 F2; root item M-2 |
| C-1.4 | row flags: NEAR, TRUNCATION_SHAPE_RESIDUAL | §1.1 NEAR remark | NEW: the TSR flag | A66.2 (flag, disclosure, not INVALID); A66 fact table (ordinal 15, 10.54 kpc, 1.0148); A64.3; root item M-7 |
| C-2 | zone summaries, trend, patterns P0–P10 | §2 | CHANGED: P0 per reason; P10 new. CLARIFIED: the even-count median; UNDEFINED makes a condition false; P5 needs N_v(TRANSITION) ≥ 1 | V001 §2; A60 and code REGISTERED_INVALID_REASONS (P0 reasons); A66.2 (P10); root item M-3 |
| C-3 | rules for every reading | §3 rules | CHANGED: adds the scope rule (R-TSR only flagged rows; R-DRIFT only OUTER rows) | V001 §3; A66.2; A63 ("outer-row misses") |
| C-3.1 | deciding tests | §3 table | CHANGED: DT-U12 is now NOT SCHEDULED in full; DT-ALT names the slots alternatives; new DT-S0G and DT-TSR | 0524; A63 (S0-FAIL-RHAT, WIRING_CHAIN_SPECIFIC, P-96 deferred per the principal); A65.2 (STAGE0 definition, timing, NOT_EVALUATED fallback); Claude4 0071 N2; A66.2 |
| C-3.2 | readings by pattern | §3 readings | CHANGED: R-DRIFT added to P1/P1g, P2 and P5; P9 notes that R-DRIFT stays OPEN; P10 with R-TSR is new | A63 (the further registered reading for outer-row misses); A65 (check R-3, the gloss UNTESTED); A66.2 (R-TSR; the route-B azimuthal mean; A42 TESTED); V001 §3 for every other row |
| C-3.3 | BH-T1a, diagnostic only | §3 BH-T1a | UNCHANGED | A10; A16.3 |
| C-4 | INVALID-as-miss rows | §4 | CHANGED: the three built-in reasons plus root-listed gate reasons (a gate may not use a built-in reason); gap rows; cut binding; roster integrity; the two-pass registration; INVALID OUTER rows count toward P9 | 0518 items 1–4; 0531 (ruled in A56); A60 (gap rows, cut binding); A62 (two-pass); code REGISTERED_INVALID_REASONS, INVALID_GATE_SCHEMA, the `root_gates` loop in `_load_row_roster` (ROOT_ROSTER_BUILTIN_REASON_MUST_DERIVE_FROM_RULE), `_authorized_row_registration`, `_invalid_registration_ok`; slots `invalid_primary_GL4`, `query_block.rule`; RUNBOOK_V001 steps 1–8; 0545 F5 |
| C-5.1 | A15 E1 comparison | §5 E1 | CHANGED: split into (a) the named deciding observable, with the Q03–Q15 sub-table, and (b) the model-internal expectation, NOT_AVAILABLE without a carrier; the data-table baryon wording made neutral | A15 E1 (deciding observable "Q03–Q15 or so"); code (no baryonic field); root item M-11 |
| C-5.2 | A15 E2 comparison | §5 E2 | CHANGED: the OUTER INVALID counts per reason | A15 E2 (outer rows may become INVALID); A60 |
| C-5.3 | A15 E3 applied | §5 E3 | UNCHANGED | A15 E3 |
| C-5.4 | never an adjustment | §5 last item | UNCHANGED | V001 §5 |
| C-6.1 | evaluated alternatives: the twin rule | I-4 ("classified the same way") | CHANGED: the twin at the same log_index; no NEAR; NO_TWIN | code `score_after_freeze` (alternatives scored by member, no reference member, no envelope scoring); A65.2 ("at the headline admitted DDO154 calibration point(s)"); root item M-10 |
| C-6.2 | NOT_EVALUATED alternatives | I-4 | UNCHANGED in effect; the wording follows v003g's note | code (the NOT_EVALUATED note text); A16.2; 0518 item 5 |
| C-6.3 | STAGE0_GRID_OUTER handling and the comparison rule | — | NEW | A65.1–A65.3; 0548; slots V003 STAGE0 record (scope, grid pin, headline false); code `_alternative_score_scope`, `_score_members_on_rows`; RUNBOOK_V001 step 10; A63; root item M-9 |
| C-7 | disclosures D-1 to D-4 | — | NEW | A63 (outcome, R-hat figures, wiring, the drift reading and its figures); A65 (grid distances, entry share, h_NN(0) figures, check R-3, the A65.4 disclosure); A66 (N1 facts, cause, the after-diagnostic disclosure); A64; A81 RI-22, RI-23 |
| C-8 | report format | §6 | CHANGED: header contents; the TSR flag column; the INVALID reason column; the alternatives section; the "SUPPORTED" wording rule | V001 §6; A63 (the SUPPORTED wording); A65.4; A66.2 |
| C-9 | self-check | §7 | CHANGED: five new closed risks and two new residual risks | V001 §7; A65.1–A65.2; A66.2; A64; A81 RI-23; root items M-7, M-9 |
| C-10 | root items list | §8 | CHANGED: M-1 to M-5 kept (M-4 and M-5 updated); M-6 to M-12 new | V001 §8; this document; `ROOT_ITEMS_R2.md` |
| C-11 | sources | §9 | CHANGED: v003g replaces v003d/v003f; slots V003, the runbook, the query manifest, both grids, the 0071 review and the new dispatches added | sha256 from bytes at writing (see `HASHES_R2.txt` for the r2 files) |

## Dispatch 0585 coverage

0585 asks r2 to integrate, at minimum, the items below.

| 0585 item | where it is in r2 |
|---|---|
| A60, gap rows | C-4 (reason QUERY_OUTSIDE_RETAINED_SUPPORT; cut binding); C-2 (P0 per reason); C-I3 (roster) |
| A63/A65, the stage-0 outcome | C-3.1 (DT-U12 status); C-7 D-1 |
| A63/A65, the STAGE0_GRID_OUTER alternative, with its disclosure | C-I1, C-I4, C-3.1 DT-S0G, C-3.2 R-DRIFT, C-6.3, C-7 D-1/D-2, C-9 |
| A64/A66, NGC K_big 32, N3′, and the N1 consequence | C-I6; C-1.4; C-2 P10; C-3.2 R-TSR; C-7 D-3/D-4 |
| the freeze v003g INVALID-as-miss rule | C-1.1; C-4; C-I3 |
| A81 RI-23, the conditional NGC M_s 128 | C-I6; C-7 D-4 |

**Entries read since V001 that touch the NGC reading,** beyond 0585's minimum:
- A81 RI-22: the DOUBLING NGC half, θ/20 (C-I6);
- A82: V005 closes at the freeze (root item M-6);
- A64.1: the C1′ scope (C-I6);
- A64.3: N1 is read only on production records (root item M-7).

**Entries read with no change to this text:**
- A61, A62, A67–A80 (driver, compare, launch packet and certificate work that does not alter how rows are read);
- A83–A88 (lane rebalancing; hardware; compare r11; seal records; LO_NGC_CERT_V002 as the V007 LO_NGC record, which is reported only in V007 under A81 RI-23; SR_K after the seal).
