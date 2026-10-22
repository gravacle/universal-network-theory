date -u: Mon Oct 19 16:19:38 UTC 2026

# RUNBOOK_V002 (draft for root): two-phase freeze, registration and score procedure, UNT Galaxy Run 120/43

**Status.** A root workflow build (`runbook_v002_c2`). It is not adopted. Root adopts it by pinning this file and `roster_builder_c2v001.py` (A133 §2 row 4), after Claude4's review (A142 build table). It authorizes no launch and no target access. Once pinned it replaces RUNBOOK_V001 (`9557b5aa`) in both phases; V001 stays as history.

**Step numbers.** V002 keeps steps 1 to 10 exactly as V001 numbers them and adds only sub-steps (0, 1a, 1b, 2b, 2c, 4a, 7a, 8a, 9-pre). So the r3a citations of steps 1–8, 4, 7, 9 and 10 bind unchanged and **no step map is needed** (r3a Status L39). The §8 header records "step map: none (V001 numbering kept)".

**Labels.** TESTED = executed in this build's synthetic record runs (55/55 cases, twice, byte-identical records). FORMAL = read from code or text bytes, not executed. UNTESTED = not executed; the deciding test is named.

## 0. Pinned inputs

| object | path | sha256 |
|---|---|---|
| freeze module v003g | `claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| slots V003 (Phase 1; Phase 2 unless the M-14 successor is pinned) | `claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` (cited; not opened by this build) |
| program query manifest | `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` | `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494` (cited; not opened) |
| roster builder | `claude_artifacts/runbook_v002_c2/roster_builder_c2v001.py` | `a19ed0eec3fb4b81ded569f4488a8ef87e089e35af6bcc5eb2c1952002c80d72` |
| root TSR flag record (M-7) | `claude_artifacts/runbook_v002_c2/ROOT_TSR_FLAG_RECORD_V001.json` | `61bd8a83492e96ffb22d576a93b65d14c047f92e3be4bbfc2c0120f439cf7edc` |
| N-test compare of record | `claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` | `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9` |
| N1 record (ring radii) | `claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json` | `8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70` |
| registered GL-node record | `claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` | `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` |
| TSR support record (UNT_ROOT_TSR_SUPPORT_CX3V001) | none yet | PENDING (gap G7) |
| A133 text of record | `UNT_PROGRAM_CONTROL/.../CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` | `cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17` |
| R3A rulings (A142) | `UNT_PROGRAM_CONTROL/.../CLAUDE2/R3A_ROOT_ITEMS_RULINGS_DRAFT_WF_B556A161.md` | `0f45f3c49644314ec3c8ca09c88b71d259c4da8a18d88282cc9c1aea7e6f79f1` |
| ROOT_ITEMS_R3A (sc3) | `claude_artifacts/miss_reading_prereg_c4/r3a_sc3/ROOT_ITEMS_R3A.md` | `0b2912754d1197a0d18e57a91b94b4ac0272125643688084115928698afce03f` |
| PREREG r3a (sc3 render; the final render is pending) | `claude_artifacts/miss_reading_prereg_c4/r3a_sc3/PREREG_MISS_READING_R3A.md` | `c64f65a357a0d3b44b362795fe7793576ba0ff6a71f1bafd2357573e2eb376c8` |
| RUNBOOK_V001 | `claude_artifacts/freeze_score_readiness_cx3/v003g/RUNBOOK_V001.md` | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` |
| 0545 (F5 two-pass) / 0548 (STAGE0 registration) | `UNT_EXCHANGE/FROM_CODEX/0545_…small_fixes.md` / `0548_…stage0_grid_outer_alternative.md` | `4049a3f81b524f5622e0eda6510eeee60c7a6b10fea97ea6c648d0b9698b84a5` / `7bf03716c95fc9d9ae06ebb038c69b6e9ed8452f2414919b35cae20365decace` |
| V006, as last read by this build (through A146; no gate pin, no seal entry) | `UNT_PROGRAM_CONTROL/.../CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` | `185486dc6c28a5f9fd45adb331667bb71a6f7f1afb9491a7e2905809ff62b9f5` |

The seal entry (not yet written, G17) supplies, per phase: the module and slots shas (M-5 addition 2), the r3a text and classifier A shas, the flag-record sha, the STAGE0 successor if pinned, the `band`/`agree` sha (`phase1_c2v003` if its review returned 0 blocking first, else `d64351ec`; A142 item 4) and the Phase-1 registry root path. Every step below reads those from the seal entry; none is hard-coded here.

## 1. Definitions used in both phases

**Builder stages** (`roster_builder_c2v001.py build`; each input is one JSON document pinned by path and sha256):
- **PLAN**: six `outer_cut NONE` rosters with no gates. They exist only so that v003g can run at budget 0 and print each alternative's exact member thetas. They are never registered.
- **MEMBERS** (Phase 2 only): rosters with the member cut contexts. They are the step-2 candidate rosters.
- **FULL**: the step-4 rosters, the M-15 gate-status list, the replay plan (budgets, dispositions, the step-4 start and the STAGE0 status). In Phase 2 the builder refuses a FULL build whose member contexts are not byte-identical to the MEMBERS stage (`MEMBER_CONTEXTS_CHANGED`), so the step-7 D1 check holds by construction. TESTED (P01, P04).

Root adopts a build only if its `BUILD_RECORD.json` reads `BUILT`. That status means: two in-memory builds were byte-equal, and the pinned freeze module itself accepted every roster (`_load_row_roster`) and every evaluated exact theta (`_row_contract`). TESTED (B01, B04, B19).

**Call record** (one per registered call; written by root from the run tree, no field chosen): `alternative`, `kind` (MEMBER or SENSITIVITY), `key` (the v003g member_id or entry_id), `attempts` (each `{run_dir, receipt pin}`, in launch order), `result` (pin or null), `cut_record` (pin or an explicit `null`). The result and the cut record must lie inside the terminal attempt's run directory. A cut record or result file serving two calls refuses (`CUT_RECORD_BORROWED`, RI45-11). A call record without a `cut_record` key refuses (`CUT_CONTEXT_MISSING`). TESTED (B06–B09, B24).

**Terminal classes (rule (c)).** One fixed map, written once per receipt producer before the first launch, takes a receipt's raw status to FINISHED, FAILED, CAP, INFRA or PLANNED_STOP. A call is terminal when its last attempt is FINISHED, or is FAILED or CAP on two consecutive attempts with the identical raw status. An INFRA last attempt is not terminal (rule (c) retries it). PLANNED_STOP is admitted only for non-roster calls (the identity twin). TESTED (B14, B15, B20, B21).

**Dispositions and v003g budgets.**
- FINISHED: EVALUATED.
- FAILED: EVALUATED_FAILED. The replay returns the saved failure record, or raises when no result was saved; v003g records MEMBER_INVALID (excluded from D1 and the envelope, scores 0, status COMPLETE). TESTED (B21).
- CAP: UNEVALUATED_CAP (rule (f)). TESTED (B20).
- A step-7 discrepancy: UNEVALUATED_STEP7_DISCREPANCY (rule (b)). TESTED (P02).
- Unchanged v003g evaluates members and sensitivity entries in order up to a budget (FORMAL, v003g L2172-2176, L2440). So the budget is the index of the first UNEVALUATED call, and every later call of that list reads UNEVALUATED_BY_ORDER_TRUNCATION. This is forced by v003g, not chosen (gap G2). The freeze then reads FREEZE_INCOMPLETE. TESTED (B20, P02).

**Validity-only rule.** Until a phase's step 4 begins, and in any case until the seal, no output value is printed or written (r3a Status; A133 §2 row 2). The builder hashes result files and never parses them. Pass one runs in memory and writes only its validity-only PASS record (`pass_record`). PLAN outputs carry no value (budget 0; the builder refuses any evaluated member, `PLAN_OUTPUT_NOT_VALUE_FREE`). The budget-0 sensitivity plan is saved with `per_query` and `per_target` emptied, because v003g fills them from the reference member's own values (`SENSITIVITY_PLAN_NOT_VALUE_FREE` otherwise). TESTED (B17, P08).

**`input_files` of `write_freeze_manifest`, both phases (M-7).** List exactly:
1. the phase's calibration record;
2. the DDO154 observation-region file;
3. the program query manifest (`a2936517`);
4. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/ROOT_TSR_FLAG_RECORD_V001.json` (`61bd8a83`);
5. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` (`6f095f64`);
6. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json` (`8867c376`);
7. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (`ec1dcca5`), spelled exactly so. v003g also adds this file as a roster dependency under its realpath, which is this spelling, so the two entries merge. Any other spelling of it refuses with "duplicate pin paths" (FORMAL, v003g L3629, L3694-3696; G12);
8. the TSR support record, once root rules G7 and it exists.

v003g adds the six rosters, the slots, the route-B config, the GL sources, every gate and cut document and the STAGE0 grid itself (FORMAL, L1698-1706, L3629). RUNBOOK_V001 listed none of items 4–7, so an honest V001 freeze would trip TSR_FLAG_TABLE_MISMATCH (R3A rulings L70).

## 2. Phase 1 (A133 §1.6: v003g unchanged, two-pass, FREEZE_INCOMPLETE)

**Recorded departures (A133 L172-178).** ROOT_CALL_ORDER_V003D steps 1 (COMPLETE), 3 (ORIGINAL_K), 4 (sensitivity) and 5 (allow_incomplete False); RI45-01's COMPLETE requirement (replaced by the Phase-1 tool, other obligations kept, 10-field RI45-10 handoff); RI45-10's FULL_FINAL_DECISION timing (RI45-03(b), restricted to the prefix). ROOT_CALL_ORDER_V003D has no cited path, so these are recorded by name and not mapped to V001 numbers (G20).

**0. Preconditions** (A133 §2).
- Before the first Phase-1 NGC launch: every target-free gate document is pinned **by its full sha256** in V006 (row 1). The builder recognizes a pin only as a full 64-hex sha in V006 bytes; an 8-hex prefix pins nothing.
- The identity-pair launch script writes the M-15 pre-launch record by exclusive create as its first action and refuses to launch if that fails (A142 item 6). Builder schema `M15_PRE_LAUNCH_RECORD_C2V001`: `{schema, date_u, v006_sha256, gate_document_sha256s}`. Beside it, the script keeps a byte copy of V006 at that sha (`cp -n`), because V006 keeps growing (G15).
- No Phase-1 NGC value is read before r3a and the M-12 classifier are sealed (row 2).
- The freeze needs AT-0a PASS and L1 written (row 3).
- The roster builder and this RUNBOOK are pinned **before Phase-1 step 4 begins** (G1; A133 row 4 places the pin at the scoring gate, after the freeze that needs the step-4 rosters).

**1a. Selection.** `select_representative_points` on the B_P1 BUDGET_EXHAUSTED calibration record, which `snapshot` wrote into the Phase-1 registry by exclusive create (A133 §1.2), with `interior_count` from the RI45-14 list (G18).

**1b. Exact thetas.**
- Run `build` at stage PLAN (phase PHASE_1). This gives six NONE rosters. Its success also decides G8: the PLAN self-check runs v003g's own target screen on the program query manifest.
- Run `evaluate_envelopes(budget=0)` for PRIMARY and ORIGINAL_K with the PLAN pins, and save each output by exclusive create. They carry each member's exact `theta_ngc` and no value. The builder never recomputes a theta: one ulp is a different context (TESTED, B22).
- Root checks that each launched call's spec theta equals its PLAN theta bit for bit (UNTESTED; the call-spec format is not in a named file).

**1. First pass: runs and saves.**
- Every PRIMARY member runs (driver cx3r008) under the root launch workflow and the memory gate (A133 §1.4, A143).
- Every attempt's run directory, receipt, result and cut record is kept.
- Rule (c) governs relaunches from T0, and no call is abandoned on a deadline. Rule (f): an OUTPUT_CAP stop is rerun with the cap raised (A141 L1).
- The three F points and the identity twin are not v003g members. They enter only `other_phase_calls` (for the step-4 start) and the `band` values file.

**3 → 4 → 2 (execution order in Phase 1).** Phase 1 has no sensitivity calls, so the step-4 rosters are also the step-2 rosters. The builder refuses a separate MEMBERS stage in Phase 1. Steps 3 and 4 therefore execute before step 2.

**3. Gather.** One call record per PRIMARY member, failures included, each with its own cut-record pin or an explicit null. Never guess a cut and never borrow another call's.

**4. Registration.** Step 4 begins when every Phase-1 NGC call has a terminal receipt: members, F points and the twin's planned stop (A133 §3; G13).
- Run `build` at stage FULL (phase PHASE_1) with:
  - `gate_cutoff = {PHASE1_STEP4_START, a byte copy of V006 taken at the step-4 start}`;
  - `gate_documents`: every gate whose full sha that copy pins;
  - `m15`: the pre-launch record, its logged V006 copy and the identity-pair launch receipts (or `null` if none exists, in which case every gate reads LATE);
  - `sensitivity_plan_output null`, `members_stage_rosters null`, and `other_phase_calls`.
- Outputs:
  - PRIMARY PER_THETA over the member contexts;
  - ORIGINAL_K NONE (budget 0, G22);
  - ML_3p6_0.4, ML_3p6_0.6, GL10 and STAGE0 NONE;
  - the gate-status list, the replay plan (PRIMARY budget = the member count unless a cap fired; ORIGINAL_K 0; sensitivity 0) and `stage0_status = NOT_EVALUATED_BEFORE_FREEZE [NOT_IN_PHASE_1]`.
- Root pins the six roster pins of `ROSTER_PINS.json` unedited. TESTED (B02, B03).

**4a. Gate-status list (M-15).** The builder's `GATE_STATUS_LIST.json` gives every root-listed gate with its status, reason and pinning entry.
- A gate is **ON-TIME** if and only if its full sha occurs in the logged pre-launch V006 bytes and the record's `date -u` is not after the earliest identity-pair launch receipt. The same second counts as preceding, because the script writes the record first.
- Every other gate is LATE. Every gate first adopted at step 4 is LATE (r3a L455).
- Root copies the list into the seal or score entry. TESTED (M01–M05, M09, M10).

**2. Pass one (D1).** In memory, under the registered rosters and the replay adapter (step 6):
- `evaluate_envelopes` PRIMARY (budget per the replay plan), ORIGINAL_K (budget 0), `select_reference_member`, `evaluate_sensitivity` (budget 0);
- write only `pass_record(PASS_ONE, …)`.

**5. Pin and retain** (byte-identical through scoring):
- the slots, the query manifest, the six rosters, every cut and gate record, and the GL-node record with its sources and the route-B config;
- the TSR flag record, compare, N1 and node;
- the PLAN outputs, the BUILD_RECORD, the replay plan and the gate-status list;
- the pre-launch record and its V006 copy;
- the builder.
Registration is custody, not cut certification (V001 L16).

**6. Replay adapter.** `make_replay_adapter(replay_plan, alternative, log, context)`. It returns only the saved, byte-verified raw result for (alternative, exact theta). It raises on an unknown theta or on a failed call with no saved result. It never launches, substitutes or invents. TESTED (B23).

**7. Pass two and the D1 check.**
- Repeat step 2's calls and write `pass_record(PASS_K, …)`.
- Run `step7(replay_plan, PASS_ONE, PASS_K)`. It returns one of three results:
  - **NO_NEW_DISCREPANCY**: go to step 8.
  - **NEW_UNEVALUATED**: rule (b) is applied in Phase 1 as well (CHOICE C3). The successor replay plan marks the member UNEVALUATED. Re-run step 7 with it, comparing again with pass one. Budgets only fall, so this terminates.
  - **STOP_NOT_MECHANIZED**: the selection, member list or sensitivity plan itself differs. No freeze; root rules (G2 residual).
- `step7` never writes a roster, and it refuses a pass run under any unregistered roster (`STEP7_ROSTER_NOT_REGISTERED`). TESTED (B03, P02, P03, P09).

**8. Freeze.**
- `write_freeze_manifest(allow_incomplete=True, row_registration_rosters=<the six registered pins>, input_files=<§1 list>)`. The result is FREEZE_INCOMPLETE, with `EXPLORATION_STATUS_BUDGET_EXHAUSTED`, `ALTERNATIVE_ORIGINAL_K_MEMBER_EVALUATION_BUDGET_EXHAUSTED` and `SENSITIVITY_BUDGET_EXHAUSTED` (FORMAL, v003g L2527-2539; the latter two TESTED in B03).
- Verify it. Log the manifest file sha, the registration sha, the Phase-1 record sha and the L1 sha before any target is opened (A133 §1.6).
- The predictions are the reference member's `speeds_km_s`.

**8a. Pre-target checks** (§6 below).

**9-pre. Seal check (M-6)** (§6 below).

**9. Score (A133 §2 row 5).**
- Only when root authorizes it: `score_after_freeze(manifest, registration, logged sha, the same six-roster mapping)`.
- Classifier A on the real score, labelled PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) (M-8).
- No roster, cut or reference is chosen after targets are seen (v003g L4192-4194 refuses changed external pins, FORMAL).

**10. Denominators.** 43 for PRIMARY; every registered null INVALID is a miss; STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (NOT_IN_PHASE_1) and is unscored; ORIGINAL_K reads NOT_AVAILABLE (I-4, M-10 precedence).

## 3. Phase 2 (registered step 4 and the full step-5 set, unchanged; score of record)

**0. Fixed before the Phase-1 score** (A133 §3; r3a I-7):
- rules (a)–(f), the re-binding rule and the commitment;
- the gate set: gates pinned in V006 before the Phase-1 score; the cutoff is the V006 byte copy whose sha the Phase-1 score entry logs, kind PHASE1_SCORE;
- the module and slots of the seal entry (the M-14 successor's, if pinned; G21).
Any stop or change after the Phase-1 score makes Phase 2 EXPLORATORY, recorded as the commitment status in the score entry.

**1a/1b.** Selection on the campaign's own calibration record, outside the Phase-1 registry root (PHASE_MISMATCH needs the two roots disjoint, r3a L196). PLAN stage (phase PHASE_2), then `evaluate_envelopes(budget=0)` for every EVALUATED alternative: PRIMARY, ORIGINAL_K, and STAGE0 if the successor is pinned. Save the value-free outputs.

**1. Step-5 runs.**
- The members, the ORIGINAL_K twins and, if the successor is pinned, one STAGE0 call per PRIMARY member (M-14).
- Headline calls launch first. STAGE0 is admitted under the memory gate and never pre-empts a headline call.
- Rule (c) relaunch; rule (d) R-D9 hull miss on the campaign side, with no widening; rule (e) D_lo/D_hi as the comparator decides; rule (f) caps.
- **Re-binding (A133 L203):** a Phase-1 result file is reused when the theta bits, the NGC spec sha (without column_workers once the identity is TESTED), the driver sha and the roster inputs match. "Roster inputs" means the call's own cut record (CHOICE C6; G14).
- Phase-2-only outputs stay validity-only until Phase-2 step 4.

**2. Pass one (D1).** When every member, twin and STAGE0 call has a terminal receipt:
- run `build` at stage MEMBERS (phase PHASE_2);
- in memory, run evaluate_envelopes for each evaluated alternative, `select_reference_member` and `evaluate_sensitivity(budget=0)`;
- write `pass_record(PASS_ONE, …)`.

**2b.** Save the budget-0 sensitivity plan with `per_query` and `per_target` emptied.

**2c.** Launch the sensitivity calls at the plan thetas, under rule (c). They are registered Phase-2 step-5 calls from the moment the plan is saved, so step 4 cannot begin before their receipts (G13). TESTED (P07).

**3. Gather.** Call records for every member, twin, STAGE0 and sensitivity call, failures included.

**4. Registration.**
- **When:** step 4 begins automatically when every registered Phase-2 call has a terminal receipt under rule (c). Its start is the write time of the last registered receipt, and a tie counts as before (`replay_plan.step4.start_utc`; TESTED, P01, P05).
- **Build:** stage FULL (phase PHASE_2), with:
  - `gate_cutoff = {PHASE1_SCORE, …}`;
  - `members_stage_rosters` = the MEMBERS pins;
  - `sensitivity_plan_output`;
  - the same `m15` as Phase 1, so a gate's status is the same in both phases (TESTED, P01);
  - `other_phase_calls []`.
- **Outputs:**
  - PRIMARY: PER_THETA over the member and sensitivity contexts;
  - ORIGINAL_K: PER_THETA;
  - STAGE0: PER_THETA only under the successor;
  - the other alternatives: NONE.
- **Pinning:** root pins the six unedited. These are "not roster changes" (r3a L480).

**4a.** Gate-status list, as in Phase 1.

**5, 6.** As in Phase 1, plus the sensitivity plan and the MEMBERS rosters.

**7. Pass two; rule (b).**
- Pass two runs under the FULL rosters, with the sensitivity budget from the replay plan, and writes `pass_record(PASS_K, …)`.
- `step7` compares it with pass one. A discrepancy makes that member UNEVALUATED (FREEZE_INCOMPLETE). It is **never** resolved by a successor made by root; this replaces V001 L21 (A133 3 (b)).
- If the D1 member is among those made UNEVALUATED, D1 moves. Then:
  - run `evaluate_sensitivity(budget=0)` for the new plan;
  - `sens-budget` sets the sensitivity budget to the leading plan entries that have a saved evaluated call;
  - no call is launched for the new plan.
- Iterate `step7` until NO_NEW_DISCREPANCY. TESTED (P02).

**8. Freeze.**
- `write_freeze_manifest(allow_incomplete=True, …)`, with the same `input_files` list as Phase 1. **Root ruling required (G3):** ROOT_CALL_ORDER_V003D step 5 (allow_incomplete False) is departed from only in Phase 1. Without this ruling, any rule (b) or (f) outcome makes the Phase-2 freeze refuse (v003g L3675-3678, FORMAL).
- Log the shas before the Phase-2 `score_after_freeze`.
- AT-0b and AT-1 are computed target-free and published (A133 §2 row 6). They are never stop inputs (r3a M-5).

**8a, 9-pre.** As in Phase 1 (§6), plus the commitment status in the score entry.

**9.** `score_after_freeze` on the Phase-2 manifest: the score of record (I-7).

**10.** Denominators:
- 43 for PRIMARY and ORIGINAL_K.
- STAGE0 only if EVALUATED_BEFORE_FREEZE under M-14: Q36–Q43, denominator 8, `headline=false`.

## 4. A133 §3 rules: where each is executed

| rule | executed by | test |
|---|---|---|
| (a) rosters from the pinned builder, run-produced cuts, gates pinned in advance | `build` (FULL), the gate cutoff and the full-sha pin check; root pins unedited | B02, B05, B10, B11, P01 |
| (b) step-7 discrepancy → that member UNEVALUATED, never a root successor | `step7` (no roster output; `STEP7_ROSTER_NOT_REGISTERED`) | P02, P03, P09 |
| (c) relaunch from T0; invalid only after two identical non-INFRA failures; never a deadline | terminal classes in `build`; the relaunch itself is the launch workflow | B14, B15 |
| (d) R-D9 hull miss: registered response, then (c) | campaign side; this runbook consumes the calibration record only | none |
| (e) D_lo/D_hi: the comparator decides | consumed as produced; no step-4 or step-7 judgment | none |
| (f) caps are value-relevant: a fired cap leaves the member unevaluated | CAP terminal → UNEVALUATED_CAP, budget prefix | B20 |

## 5. STAGE0 receipt rule (M-14), Phase 2

- `replay_plan.stage0_status` is computed mechanically.
- **NO_SEALED_SUCCESSOR:** when the phase's slots do not declare STAGE0 EVALUATED, which is the case under V003.
- **STAGE0_RECEIPT_NOT_FINISHED:** when a registered STAGE0 call's terminal class is not FINISHED.
- **EVALUATED_BEFORE_FREEZE:** otherwise, subject to EVALUATED_REFUSED by the successor at the freeze.
- Every STAGE0 receipt time and the step-4 start are recorded. RECEIPTS_AFTER_STEP4 cannot arise, because the start is the last registered receipt.
- The successor's TEST (a) must show that v003g completes a Phase-2 freeze with STAGE0 NOT_EVALUATED (UNTESTED; no successor exists). TESTED on synthetic successor slots (P05).
- Root publishes the STAGE0 delay at the Phase-2 selection (A142 item 3).

## 6. Pre-target checks before step 9 (both phases)

**8a.**
- `tsr-check` on the flag record pin, with the frozen manifest. TSR_FLAG_TABLE_MISMATCH fires if any of these fails:
  - the compare is `6f095f64` with failing TRUNCATION_SHAPE rings exactly {15} and no other failing ring;
  - N1 is `8867c376`;
  - the node record is `ec1dcca5`;
  - the 43 flags are exactly {NGC3198-Q25};
  - the bounds are bitwise N1 rings 14 and 16, exclusive;
  - all four files are in `input_files`.
  TESTED (T01–T08; production record PASS from bytes).
- `check-gate-list` over the six roster pins and the list root entered: GATE_STATUS_LIST_DEFECT (TESTED, M07, M08).
- The sealed classifier's synthetic pre-score run on the frozen member arrays, covering REFERENCE_MEMBER_MISMATCH, PHASE_MISMATCH (the calibration-record path against the Phase-1 registry root the seal entry names) and the rest of r3a §1.1. It goes in the seal or score entry (r3a L184-185).

**9-pre.** `seal-check` with a V006 byte copy taken after the seal entry and the sealed objects:
- roles PREREG_TEXT, CLASSIFIER and TSR_FLAG_RECORD, plus STAGE0_SUCCESSOR if pinned and any other sealed sha such as BAND_AGREE;
- the seal entry is the first `## ` heading carrying the text's full sha;
- each object's bytes must hash to a sha named in that entry.
On a mismatch the stop is SEAL_SHA_MISMATCH and `score_after_freeze` is not called. TESTED (S01–S04). What follows a stop is not yet ruled (G16).

## 7. Root rulings this runbook needs

- **G1:** pin the builder and this runbook before Phase-1 step 4 (A133 row 4 places them after the freeze that needs them).
- **G2 residual:** a STOP_NOT_MECHANIZED step-7 result (a selection, member-list or plan difference that is not a member discrepancy).
- **G3:** Phase-2 `allow_incomplete=True`, ruled before the Phase-1 score.
- **G7:** whether the TSR support record exists, its writer and its point_key. The flag record carries it as PENDING.
- **G8 (UNTESTED):** the program query manifest under v003g's target screen. A PLAN build is the deciding test.
- **G9 (UNTESTED):** real results through `_v010_preflight`. The deciding test is pass one on the S0 results.
- **G10 (UNTESTED):** that real cx3r008/v011 runs write NGC_CANDIDATE_ROSTER_CUT_CX3V001 records inside the call's run directory, which is the builder's ownership test.
- **G13:**
  - the Phase-1 call set (taken here as members, F points and the twin's planned stop);
  - the Phase-2 sensitivity registration (from the saved plan);
  - the receipt time key and status map (named once per producer).
- **G14:** "roster inputs" in the re-binding rule; taken here as the call's own cut record.
- **G15:** the pre-launch record path and format (proposed: `M15_PRE_LAUNCH_RECORD_C2V001`).
- **G16:** the remedy after a pre-target stop.
- **G17:** the seal entry.
- **G18:** the RI45-14 list.
- **G19:** the unruled RI45 items.
- **G20:** ROOT_CALL_ORDER_V003D's path.
- **G21:** the STAGE0 slots pin under a successor.
- **G24:** the Phase-1 gate cutoff; proposed here as the V006 at the step-4 start.

## 8. TESTED / FORMAL / UNTESTED

- **TESTED.** Synthetic suite `test_runbook_v002_c2v001.py`, run twice as record runs (`test_records/RUN1`, `RUN2`): 55/55 each (22 MUST_PASS, 33 MUST_FAIL), with byte-identical TEST_RECORD files.
  - The end-to-end cases run the real v003g functions (`evaluate_envelopes`, `select_reference_member`, `evaluate_sensitivity`, `_load_row_roster`, `_row_contract`, `_root_frozen_rows`, `_incomplete_reasons`) on synthetic slots, nodes and query manifest. The module's constants are patched, so no program slots are read.
  - The production TSR flag record passes `tsr-check` against the real compare, N1 and node bytes.
- **FORMAL.** The v003g line citations above, read from `48a1e48a` bytes.
- **UNTESTED.** Production PLAN, MEMBERS and FULL builds; real receipts, cut records and results (G8, G9, G10); the M-14 successor; `write_freeze_manifest` itself (it needs a real calibration record; not run here); real-target scoring.
