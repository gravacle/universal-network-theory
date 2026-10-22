date -u: Mon Oct 19 19:12:40 UTC 2026

# RUNBOOK_V002 (build c2v005, draft for root): two-phase freeze, registration and score procedure, UNT Galaxy Run 120/43

**Status.** A root workflow build (`runbook_v002_c2`, fifth build). It is not adopted. Root adopts it by pinning this file and `roster_builder_c2v005.py` (A133 §2 row 4), after Claude4's review (A142 build table). It authorizes no launch and no target access. Once pinned it replaces RUNBOOK_V001 (`9557b5aa`) in both phases; V001 stays as history. It supersedes the c2v004 build (`RUNBOOK_V002_C2V004.md` `06ca537f`, `roster_builder_c2v004.py` `8e8022e2`), the c2v003, c2v002 and c2v001 builds; all stay unchanged in this folder and must not be pinned.

**What changed from c2v004 (root rulings on the c2v004 re-verify and on G29; implemented as ruled).**
- **Ruling (1): the cross-call file check covers every file of every call.** c2v004's §1 claimed that a receipt, result or cut record of one call that is a file of another call refuses, but its builder compared results and cut records only among roster calls: the receipts of OTHER calls (F points, the identity twin) were compared with other receipts only. The re-verify probes built BUILT: Q4b (M001's result pin was F1's receipt, same path), Q4 (M001's result a hard link of F1's receipt) and Q5 (M001's cut record a hard link of an OTHER call's receipt that also parses as a cut record; pass one read M001 evaluated and valid). c2v005 identifies every file of every call of the build input (each roster call's receipts, result and cut record; each OTHER call's receipts) by realpath and by file identity (`st_dev`, `st_ino`, from the fstat of the descriptor whose bytes the builder hashed), so the §1 claim is now what the builder checks. Q4b, Q4 and Q5 are MUST_FAIL cases J01–J03.
- **Ruling (2), G29: a cut record is bound to its call by residence.** Its realpath must lie inside its call's terminal run directory (`CUT_RECORD_NOT_OF_ITS_CALL`, as before) and inside no run directory, of any attempt, of any other call of the build input, roster or OTHER (`CUT_RECORD_IN_OTHER_CALL_RUN_DIR`, new), and it must be a file of no other call (by realpath or file identity). **The c2v004 byte-equality refusal for cut records is removed**: two honest calls may emit byte-identical cut records. **C38 is kept**: the result of a FINISHED call whose sha256 is another call's cut record or result refuses; it is now checked over all pairs of calls, so the outcome does not depend on the order of the calls. Failure records of FAILED calls may be byte-identical and must lie in their own call's terminal run directory (`RESULT_NOT_OF_ITS_CALL`, as before).
- Two ported cases change expectation (H02 and H06, from MUST_FAIL to MUST_PASS); 12 cases are new (J01–J12). No input or output schema changed (C39).

**Carried from c2v004 (the blocking finding against c2v003: one cut-record file could serve two calls).** c2v004 identified receipts, results and cut records also by file identity, which caught the c2v001 probe A2e (M000's cut record hard-linked into M001's run directory), and refused byte copies of cut records and of FINISHED results (C37, C38). The cut-record half of the content rule is withdrawn by G29 (above); the file identity and C38 stay.

**Carried from c2v003 (the re-verify findings R1-R3 against c2v002, and classifier A's input contracts).**
- **R1, one terminal prefix and one spec per call.** A rule-(c) pair is judged on the attempts up to and including the pair, so a later attempt can never un-terminate it; any attempt after the first terminal prefix refuses (`ATTEMPT_AFTER_TERMINAL`). The attempts of one call carry one `spec_sha256` at most (`RULE_C_SPEC_NOT_IDENTICAL`). (CHOICE C30.)
- **R2, every receipt bound to its call.** A pinned step-5 **launch registry** (new input, gap G27) gives each call its exact-theta key and the spec sha registered at launch. Every receipt carries both (a ninth receipt role, `theta_sha256`), and both must equal the call's. One receipt (by realpath or sha256) never serves two calls (`RECEIPT_REUSED_ACROSS_CALLS`). (C31-C33.)
- **R3, the step-7 ledger outside the build directory.** It lives at `<step7_ledger_root>/STEP7_LEDGER_<BUILD_RECORD sha256>/`. Root fixes the absolute root (gap G28), the FULL build records it in `BUILD_RECORD.json` and creates the ledger with a genesis entry. Copying the build directory therefore never resets it; a missing ledger, a second ledger beside the build record, or a second ledger for the same replay plan under the root refuses. (C34.)
- **Classifier A's records.** The gate-status list is written in classifier A's `GATE_STATUS_LIST_C4V001` schema, and the TSR flag record has a successor in A's `TSR_FLAG_RECORD_C4V001` schema (`ROOT_TSR_FLAG_RECORD_V002.json`, `c9d8ab45`). §6b lists the 15 other inputs A expects and who writes each. (C35, C36.)

**Step numbers.** V002 keeps steps 1 to 10 exactly as V001 numbers them and adds only sub-steps (0, 1a, 1b, 2b, 2c, 4a, 7a, 8a, 9-pre). So the r3a citations of steps 1–8, 4, 7, 9 and 10 bind unchanged and **no step map is needed** (r3a Status L39). The §8 header records "step map: none (V001 numbering kept)".

**Labels.** TESTED = executed in this build's synthetic record runs (149/149 cases, twice, byte-identical records). FORMAL = read from code or text bytes, not executed. UNTESTED = not executed; the deciding test is named.

## 0. Pinned inputs

| object | path | sha256 |
|---|---|---|
| freeze module v003g | `claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| slots V003 (Phase 1; Phase 2 unless the M-14 successor is pinned) | `claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` (cited; not opened by this build) |
| program query manifest | `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` | `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494` (cited; not opened) |
| roster builder c2v005 | `claude_artifacts/runbook_v002_c2/roster_builder_c2v005.py` | `653ced76513d3415d8d4904a73bf1c2dc6d316a053be4f89029611c80ffc9075` |
| root TSR flag record V002 (M-7; classifier A's `TSR_FLAG_RECORD_C4V001` schema; c2v003) | `claude_artifacts/runbook_v002_c2/ROOT_TSR_FLAG_RECORD_V002.json` | `c9d8ab4573278f2d325bc5fe50e396e35e9981f0561cfa20e61e8a215bb5cea0` (a builder constant) |
| root TSR flag record V001 (c2v001; the only input `tsr-record` accepts; not a classifier input) | `claude_artifacts/runbook_v002_c2/ROOT_TSR_FLAG_RECORD_V001.json` | `61bd8a83492e96ffb22d576a93b65d14c047f92e3be4bbfc2c0120f439cf7edc` |
| N-test compare of record | `claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` | `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9` |
| N1 record (ring radii) | `claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json` | `8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70` |
| registered GL-node record | `claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` | `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` |
| TSR support record (UNT_ROOT_TSR_SUPPORT_CX3V001) | none yet | PENDING (gap G7) |
| classifier A README (input contracts) | `claude_artifacts/classifier_a_c4/build_c4v001/README_CLASSIFIER_A_C4V001.md` | `4e1e7493eec60247506a3012bada9f65f958a7f54d2f66ed2b1063df45c61d10` |
| A133 text of record | `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` | `cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17` (as c2v002 recorded; not reopened) |
| R3A rulings (A142) | `UNT_PROGRAM_CONTROL/.../CLAUDE2/R3A_ROOT_ITEMS_RULINGS_DRAFT_WF_B556A161.md` | `0f45f3c49644314ec3c8ca09c88b71d259c4da8a18d88282cc9c1aea7e6f79f1` (as recorded; not reopened) |
| ROOT_ITEMS_R3A (sc3) | `claude_artifacts/miss_reading_prereg_c4/r3a_sc3/ROOT_ITEMS_R3A.md` | `0b2912754d1197a0d18e57a91b94b4ac0272125643688084115928698afce03f` (as recorded; not reopened) |
| PREREG r3a (sc3 render; the final render is pending) | `claude_artifacts/miss_reading_prereg_c4/r3a_sc3/PREREG_MISS_READING_R3A.md` | `c64f65a357a0d3b44b362795fe7793576ba0ff6a71f1bafd2357573e2eb376c8` (as recorded; not reopened) |
| RUNBOOK_V001 | `claude_artifacts/freeze_score_readiness_cx3/v003g/RUNBOOK_V001.md` | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` |
| V006, as last read by this build (through A160; read by c2v005 only as its heading list, lines 1-516 and a keyword grep (G29, c2v004, c2v005, runbook_v002, Q4b, BORROWED, residence, RI45-11): no seal entry, no launch registry, no G29 entry; the rulings c2v005 implements are root's, as dispatched to this build; see the A157 NOTE in the README) | `UNT_PROGRAM_CONTROL/.../CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` | `96489e9f0770f01d8d1b56c777c0b4b0b512ef06af23e78e8a1de4152eb750cf` |

The seal entry (not yet written, G17; format proposed in §6) supplies, per phase: the module and slots shas (M-5 addition 2), the r3a text and classifier A shas, the flag-record sha (`c9d8ab45`, V002), the STAGE0 successor if pinned, the `band`/`agree` sha (A142 item 4) and the Phase-1 registry root path. Every step below reads those from the seal entry; none is hard-coded here, except the flag record `c9d8ab45`, which the builder pins as a constant beside the compare, N1 and node pins (C28, carried; the pinned record is V002 since c2v003).

## 1. Definitions used in both phases

**Builder stages** (`roster_builder_c2v005.py build`; each input is one JSON document pinned by path and sha256):
- **PLAN**: six `outer_cut NONE` rosters with no gates. They exist only so that v003g can run at budget 0 and print each alternative's exact member thetas. They are never registered.
- **MEMBERS** (Phase 2 only): rosters with the member cut contexts. They are the step-2 candidate rosters. Input adds `launch_registry`.
- **FULL**: the step-4 rosters, the M-15 gate-status list (classifier A's schema) and its report, the replay plan (budgets, dispositions, the step-4 start, the STAGE0 status, the pass-one binding and the launch-registry pin), and the step-7 ledger under `step7_ledger_root`. In Phase 2 the builder refuses a FULL build whose member contexts are not byte-identical to the MEMBERS stage (`MEMBER_CONTEXTS_CHANGED`), so the step-7 D1 check holds by construction. A Phase-2 FULL build also takes the MEMBERS stage's `BUILD_RECORD.json` (`members_stage_build_record`); it must be BUILT by the same builder, its roster outputs must equal the `members_stage_rosters` pins, and its replay plan's sha and budgets become the FULL plan's `pass_one` binding (C26). TESTED (P01, P04); the MEMBERS build-record refusals are FORMAL.

Root adopts a build only if its `BUILD_RECORD.json` reads `BUILT`. That status means: two in-memory builds were byte-equal, and the pinned freeze module itself accepted every roster (`_load_row_roster`) and every evaluated exact theta (`_row_contract`). TESTED (B01, B04, B19).

**Call record** (one per registered call; written by root from the run tree, no field chosen): `alternative`, `kind` (MEMBER or SENSITIVITY), `key` (the v003g member_id or entry_id), `attempts` (each `{run_dir, receipt pin}`, in launch order), `result` (pin or null), `cut_record` (pin or an explicit `null`). The result and the cut record must lie inside the terminal attempt's run directory (by realpath, so a symlink to a file elsewhere refuses: `RESULT_NOT_OF_ITS_CALL`, `CUT_RECORD_NOT_OF_ITS_CALL`; the cut record's residence rule continues in the next paragraph). A call record without a `cut_record` key refuses (`CUT_CONTEXT_MISSING`). TESTED (B06–B08, B24, J05, J11). The phase's non-roster NGC calls (F points, the identity twin) enter as `other_phase_calls` `{label, attempts}` (FULL only); their run files are their receipts (the input carries no result or cut record for them).

**One run file serves one call (RI45-11, "never reuse another point's file"; c2v004, extended by c2v005 under root's rulings).** Calls are identified as under R2 below: a roster call by (alternative, exact theta), so a MEMBER and a SENSITIVITY record at one theta are one call; an OTHER call by its label. The run files of a call are, for a roster call, its receipts, its result and its cut record, and, for an OTHER call, its receipts. Across all the calls of one build input, roster and OTHER, the builder refuses:
- **the same file.** A run file of one call that is a run file of another call, whatever the two roles, by realpath or by **file identity** (`st_dev`, `st_ino`, taken from the fstat of the descriptor whose bytes the builder hashed; a hard link is the same file under another path). Codes: between two receipts, `RECEIPT_REUSED_ACROSS_CALLS` (checked first); otherwise `CUT_RECORD_BORROWED` when either file is a cut record, else `FILE_BORROWED`. TESTED (B09 same path; H01 the c2v001 probe A2e: M000's cut record hard-linked into M001's run directory; H03 a hard-linked result; H04 a hard-linked receipt; H05 across alternatives at one theta; H07 one call's cut record as another's result; H13 a hard-linked failure record; J01 the re-verify probe Q4b: a roster call's result that is an OTHER call's receipt, same path; J02 Q4: a hard link of an OTHER call's receipt as a result; J03 Q5: a hard link of an OTHER call's receipt as a cut record; J08 two byte-identical cut records that are one hard-linked file).
- **a cut record outside its own call's residence (G29).** A cut record is bound to its call by residence: its realpath lies inside its call's terminal run directory (`CUT_RECORD_NOT_OF_ITS_CALL`) and inside no run directory, of any attempt, of any other call of the build input, roster or OTHER (`CUT_RECORD_IN_OTHER_CALL_RUN_DIR`). This check runs after the same-file and content checks, so a cut record that is another call's file reads `CUT_RECORD_BORROWED` even when it also lies in that call's run directory (B09). TESTED (B08, J05 outside its run directory; J06 inside another roster call's terminal run directory; J12 inside another call's non-terminal attempt run directory; J07 inside an OTHER call's run directory).
- **the same content, where root kept it (C38).** The result of a FINISHED call whose sha256 is that of another call's cut record or result (a byte copy, including an APFS clone), checked over all pairs of calls, so the call order never matters; and a receipt whose sha256 is another call's receipt (R2). TESTED (H09 a byte copy of M000's result; H10 across alternatives at one theta; H11 a FAILED call saving a FINISHED call's result; J10 a FINISHED result with another call's cut-record bytes, in both call orders).
- **Not refused** (G29 as ruled):
  - byte-identical cut records of distinct calls, each a file inside its own call's terminal run directory (TESTED H06 Phase 1, J04 Phase 2: PRIMARY and ORIGINAL_K at one theta, MEMBERS build and pass one; H02 a byte copy of M000's cut record inside M001's own run directory, below);
  - byte-identical failure records of FAILED calls (TESTED H12; J09: a failure record with the bytes of another call's cut record, in both call orders). Each must still lie in its own call's terminal run directory: a byte-identical failure record written in another call's run directory refuses `RESULT_NOT_OF_ITS_CALL` (TESTED J11).
- **Consequence (disclosed).** A byte copy, or any re-serialization, of another call's cut record written into a call's own terminal run directory is indistinguishable from an honest identical cut record and builds (TESTED H02; the re-verify probes Q2, Q3, Q3b build under c2v005). So does a hard link of a file that belongs to no call of the build input (probe Q7). The binding is residence: the builder checks where the file is and that it is no other call's file, not who wrote it (G29 item 4 stays open: a binding key in the cut record is the only content-level closure).
- Results keep c2v004's residence rule only: inside the terminal run directory. The "no other call's run directory" rule is applied to cut records, as ruled (NOTE in the README).
- c2v004's text claimed the same-file rule for every call while its builder left OTHER calls' receipts out of it: run against the c2v004 builder's bytes, J01–J03 build without a refusal (development run, README).

**Launch registry (since c2v003; G27, schema proposed here: `STEP5_LAUNCH_REGISTRY_C2V003`).** `{schema, phase, calls: [{alternative, kind, key, theta_sha256, spec_sha256}]}`, one entry per launched call, written by the launch workflow by machine as each call is launched (A135 item 9: "the spec sha registered"):
- `kind` MEMBER or SENSITIVITY (with the alternative), or OTHER (alternative `null`, `key` = the `other_phase_calls` label);
- `theta_sha256` = sha256 of the v003g canonical bytes of the call's exact `theta_ngc` (for OTHER calls, the launched point's key); `spec_sha256` = the spec sha registered at launch;
- the registry's entries are exactly the build input's calls: an entry without a call record (`LAUNCH_REGISTRY_ENTRY_WITHOUT_CALL`) and a call without an entry (`LAUNCH_REGISTRY_ENTRY_MISSING`) both refuse;
- a roster entry's `theta_sha256` must equal the call's exact theta from the PLAN output or the saved sensitivity plan (`LAUNCH_REGISTRY_THETA_MISMATCH`);
- one call (alternative, exact theta) has one spec sha: MEMBER and SENSITIVITY entries at one theta are one call (A133) and must agree (`LAUNCH_REGISTRY_CONFLICT`). Distinct calls may share a spec sha (A133 re-binding: the spec sha without column_workers once the identity is TESTED can make the twin's equal the serial member's); the receipt rule below keeps their receipts apart.
TESTED (R2e, R2f, R2h, R2i, R2j).

**Receipts, their evidence and their binding (G13, G25, G27).** Root names once per receipt producer, before the first launch, the receipt key that carries each of nine roles (`receipt_keys`): `status`, `time_utc`, `spec_sha256`, `theta_sha256` (new), `rss_cap_bytes`, `wall_cap_s`, `host_ram_bytes`, `other_ngc_processes_max` and `output_cap_bytes`. The launch workflow writes them into each attempt's receipt by machine; root enters none of them by hand. `other_ngc_processes_max` is the largest number of other NGC processes seen running at any time during the attempt.
- **Binding (every receipt, every class, FINISHED included).** `theta_sha256` must equal the call's registry entry (`RECEIPT_THETA_NOT_OF_CALL`), then `spec_sha256` must equal it (`RECEIPT_SPEC_NOT_REGISTERED`); a receipt without either reads `RECEIPT_CALL_BINDING_MISSING`. TESTED (R2a, R2b, R2g).
- **Evidence (failure terminals only).** A receipt without the cap and solo evidence still serves a FINISHED terminal, but can never make a call invalid or unevaluated (below).

**Rule (c), text of record (A133 §3 (c), step-5 NGC call):** "rerun the identical spec with the RSS cap at RAM and the wall cap doubled. It is marked invalid only after two identical deterministic failures that are not INFRA, with no other NGC process running." "There is never a deadline-based abandonment." A141 L1 adds: an OUTPUT_CAP stop "is rerun with the output cap raised". Rule (f): caps follow rule (c). (The campaign-halt branch of (c) belongs to the DDO campaign, not to a roster call.)

**Terminal classes (rule (c), as the builder enforces it; CHOICES C21, C22, C30).** One fixed map per receipt producer, written before the first launch, takes a receipt's raw status to FINISHED, FAILED, CAP, OUTPUT_CAP, INFRA or PLANNED_STOP. A141 L4: a twin cap stop maps to PLANNED_STOP.
- A call is **terminal** when its last attempt is FINISHED (or PLANNED_STOP, admitted only for a non-roster call such as the identity twin), or when its last two attempts form a **rule-(c) pair**. A rule-(c) pair is:
  - two consecutive FAILED, CAP or OUTPUT_CAP attempts with the identical raw status (the "identical deterministic failures"; non-INFRA by class);
  - the identical `spec_sha256` on every attempt up to the pair that carries one, and on the call's first attempt and both counted attempts at least ("the identical spec");
  - `other_ngc_processes_max` = 0 on **both** counted attempts ("with no other NGC process running");
  - on the counted rerun: `rss_cap_bytes` = `host_ram_bytes` ("the RSS cap at RAM") and `wall_cap_s` = 2 × the call's first attempt's `wall_cap_s` ("the wall cap doubled");
  - for OUTPUT_CAP, also `output_cap_bytes` above the first attempt's (A141 L1).
- **R1.** A pair is judged on its own prefix (the attempts up to and including it). Any attempt after the first terminal prefix (a FINISHED or PLANNED_STOP attempt, or a pair) refuses, whatever its spec (`ATTEMPT_AFTER_TERMINAL`; TESTED R1a, O5–O7). The attempts of one call carry one `spec_sha256` at most (`RULE_C_SPEC_NOT_IDENTICAL`; TESTED R1b, C05); a failure followed by a FINISHED rerun of the identical spec is EVALUATED (TESTED R1c).
- An INFRA last attempt is not terminal; rule (c) retries it. Fewer than two identical failures reads `RULE_C_INCOMPLETE`; a counted receipt without the evidence reads `RULE_C_EVIDENCE_MISSING`; the other failures read `RULE_C_NOT_SOLO`, `RULE_C_RERUN_CAPS` or `RULE_C_SPEC_NOT_IDENTICAL`. Every one of these refuses the build: the call is not terminal, so rule (c) reruns it. TESTED (B14, B15, C01–C08).
- **Attempts are distinct.** The builder refuses a run directory used twice (by realpath, so a symlink counts), nested run directories, a receipt used twice within a call (by realpath or by sha256), receipt times that do not strictly increase, and any attempt after the first terminal prefix. TESTED (O1a, O1b, O1c, O2, O5–O8).
- **Calls are distinct (R2).** One receipt, by realpath, by file identity (c2v004) or by sha256, serves one call across the whole build input: roster calls are identified by (alternative, exact theta), OTHER calls by label (`RECEIPT_REUSED_ACROSS_CALLS`). Since c2v005 an OTHER call's receipt is also never a roster call's result or cut record (by realpath or file identity; `FILE_BORROWED`, `CUT_RECORD_BORROWED`). TESTED (R2c: the twin registered at the serial member's theta and spec, its receipt a byte copy of the member's; R2d: the same file; H04: a hard link; J01–J03).
- The replay plan records, per member, the counted pair and its evidence (`rule_c`). TESTED (B20, C06, C08).

**Dispositions and v003g budgets.**
- FINISHED: EVALUATED.
- FAILED: EVALUATED_FAILED. The replay returns the saved failure record, or raises when no result was saved; v003g records MEMBER_INVALID (excluded from D1 and the envelope, scores 0, status COMPLETE). TESTED (B21).
- CAP and OUTPUT_CAP: UNEVALUATED_CAP (rule (f)). TESTED (B20, C08).
- A step-7 discrepancy: UNEVALUATED_STEP7_DISCREPANCY (rule (b)). TESTED (P02).
- Unchanged v003g evaluates members and sensitivity entries in order up to a budget (FORMAL, v003g L2172-2176, L2440). So the budget is the index of the first UNEVALUATED call, and every later call of that list reads UNEVALUATED_BY_ORDER_TRUNCATION. This is forced by v003g, not chosen (gap G2). The freeze then reads FREEZE_INCOMPLETE. TESTED (B20, P02).

**Validity-only rule.** Until a phase's step 4 begins, and in any case until the seal, no output value is printed or written (r3a Status; A133 §2 row 2: "Until then, reads are validity-only"). The delivered path:
- The builder hashes result files and never parses them.
- **`pass` (the in-memory pass driver; steps 2 and 7).** It loads the pinned v003g, runs `evaluate_envelopes`, `select_reference_member` and `evaluate_sensitivity` in memory under the replay adapter, and writes only `PASS_RECORD.json`. That record holds validity only: per member `evaluated`, `forward_valid_flag`, `member_valid`, `row_valid`, row reasons and the served result pin; D1's member id; and the sensitivity plan's ids and theta shas. For Phase-2 pass one it also writes `SENSITIVITY_PLAN_VALUE_FREE.json`, a whitelist extract of the budget-0 plan with `per_query` and `per_target` empty. It prints only a status and the file names (TESTED); its internal errors print the exception type only (FORMAL). TESTED (V01, V02: every written byte and the printed line scanned; no value key, no non-null value array, no float in the synthetic value range).
- c2v001's `pass-record` command does not exist in c2v002, c2v003, c2v004 or c2v005 (TESTED, V03). No delivered command writes an envelope, a reference member or a sensitivity output to disk.
- PLAN outputs carry no value (budget 0; the builder refuses any evaluated member, `PLAN_OUTPUT_NOT_VALUE_FREE`). A saved sensitivity plan with any key outside the whitelist, or with `per_query`/`per_target` not empty, refuses (`SENSITIVITY_PLAN_NOT_VALUE_FREE`). TESTED (B17, P08, V06).
- The driver's in-memory outputs exist for one in-process caller only: the step-8 freeze script, which runs after the seal (G26).

**`input_files` of `write_freeze_manifest`, both phases (M-7).** List exactly:
1. the phase's calibration record;
2. the DDO154 observation-region file;
3. the program query manifest (`a2936517`);
4. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/ROOT_TSR_FLAG_RECORD_V002.json` (`c9d8ab45`); `tsr-check` and `seal-check` both refuse a manifest without this exact pin (C28). V001 (`61bd8a83`) is **not** listed: it is not in classifier A's schema and `tsr-check` refuses it (TESTED, X04);
5. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` (`6f095f64`);
6. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json` (`8867c376`);
7. `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (`ec1dcca5`), spelled exactly so. v003g also adds this file as a roster dependency under its realpath, which is this spelling, so the two entries merge. Any other spelling of it refuses with "duplicate pin paths" (FORMAL, v003g L3629, L3694-3696; G12);
8. the TSR support record, once root rules G7 and it exists.

v003g adds the six rosters, the slots, the route-B config, the GL sources, every gate and cut document and the STAGE0 grid itself (FORMAL, L1698-1706, L3629).

## 2. Phase 1 (A133 §1.6: v003g unchanged, two-pass, FREEZE_INCOMPLETE)

**Recorded departures (A133 L172-178).** ROOT_CALL_ORDER_V003D steps 1 (COMPLETE), 3 (ORIGINAL_K), 4 (sensitivity) and 5 (allow_incomplete False); RI45-01's COMPLETE requirement (replaced by the Phase-1 tool, other obligations kept, 10-field RI45-10 handoff); RI45-10's FULL_FINAL_DECISION timing (RI45-03(b), restricted to the prefix). ROOT_CALL_ORDER_V003D has no cited path, so these are recorded by name and not mapped to V001 numbers (G20).

**0. Preconditions** (A133 §2).
- Before the first Phase-1 NGC launch: every target-free gate document is pinned **by its full sha256** in V006 (row 1). The builder recognizes a pin only as a full 64-hex sha in V006 bytes; an 8-hex prefix pins nothing.
- The identity-pair launch script writes the M-15 pre-launch record by exclusive create as its first action and refuses to launch if that fails (A142 item 6). Builder schema `M15_PRE_LAUNCH_RECORD_C2V001`: `{schema, date_u, v006_sha256, gate_document_sha256s}`. Beside it, the script keeps a byte copy of V006 at that sha (`cp -n`), because V006 keeps growing (G15).
- Every receipt producer's status map and its nine receipt keys are named before the first launch (G13, G25, G27), and the launch workflow writes the launch registry entry of every call it launches (G27).
- Root fixes the step-7 ledger root (an absolute directory outside every build directory) before the first FULL build (G28).
- No Phase-1 NGC value is read before r3a and the M-12 classifier are sealed (row 2), and before the S1 reading releases Phase-1 reads (A150: only PASS or PASS_AT_ADOPTION_POINT releases them).
- The freeze needs AT-0a PASS and L1 written (row 3).
- The roster builder and this RUNBOOK are pinned **before Phase-1 step 4 begins** (G1; A133 row 4 places the pin at the scoring gate, after the freeze that needs the step-4 rosters).

**1a. Selection.** `select_representative_points` on the B_P1 BUDGET_EXHAUSTED calibration record, which `snapshot` wrote into the Phase-1 registry by exclusive create (A133 §1.2), with `interior_count` from the RI45-14 list (G18). Save its output by exclusive create (the pass driver's `selection` input; it carries `points`), and the coordinate spec (`spec`).

**1b. Exact thetas.**
- Run `build` at stage PLAN (phase PHASE_1). This gives six NONE rosters. Its success also decides G8: the PLAN self-check runs v003g's own target screen on the program query manifest.
- Run `evaluate_envelopes(budget=0)` for PRIMARY and ORIGINAL_K with the PLAN pins, and save each output by exclusive create. They carry each member's exact `theta_ngc` and no value. The builder never recomputes a theta: one ulp is a different context (TESTED, B22).
- Each launched call's launch-registry `theta_sha256` must equal its PLAN theta key; the builder checks this (TESTED, R2e). That the launched spec's theta equals the PLAN theta bit for bit is the launch workflow's (UNTESTED; the call-spec format is not in a named file).

**1. First pass: runs and saves.**
- Every PRIMARY member runs (driver cx3r008) under the root launch workflow and the memory gate (A133 §1.4, A143).
- Every attempt's run directory, receipt (with its evidence and binding keys), result and cut record is kept, and every launch is registered.
- Rule (c) governs relaunches from T0, and no call is abandoned on a deadline. A failed call is rerun as §1 states (identical spec, RSS cap at RAM, wall cap doubled, no other NGC process running; for OUTPUT_CAP the output cap raised, A141 L1); each rerun is a new attempt with its own run directory and receipt, under the same registry entry.
- The three F points and the identity twin are not v003g members. They enter only `other_phase_calls` (for the step-4 start), the launch registry (kind OTHER) and the `band` values file.

**3 → 4 → 2 (execution order in Phase 1).** Phase 1 has no sensitivity calls, so the step-4 rosters are also the step-2 rosters. The builder refuses a separate MEMBERS stage in Phase 1. Steps 3 and 4 therefore execute before step 2.

**3. Gather.** One call record per PRIMARY member, failures included, each with its own cut-record pin or an explicit null. Never guess a cut and never borrow another call's file or receipt, roster or OTHER: not by path, not by hard link, not by copy (§1). Pin each call's own cut record where its run wrote it, inside that call's terminal run directory; the builder binds a cut record by that residence and refuses one inside another call's run directory (G29), and it cannot see a copy placed by hand (§1, "Consequence").

**4. Registration.** Step 4 begins when every Phase-1 NGC call has a terminal receipt under rule (c): members, F points and the twin's planned stop (A133 §3; G13).
- Run `build` at stage FULL (phase PHASE_1) with:
  - `gate_cutoff = {PHASE1_STEP4_START, a byte copy of V006 taken at the step-4 start}`;
  - `gate_documents`: every gate whose full sha that copy pins;
  - `m15`: the pre-launch record, its logged V006 copy and the identity-pair launch receipts (or `null` if none exists, in which case every gate reads LATE);
  - `receipt_keys` (nine roles) and `receipt_status_classes`;
  - `launch_registry`: the Phase-1 registry pin (members and OTHER calls);
  - `step7_ledger_root`: the root-fixed ledger root (G28);
  - `sensitivity_plan_output null`, `members_stage_rosters null`, `members_stage_build_record null`, and `other_phase_calls`.
- Outputs:
  - PRIMARY PER_THETA over the member contexts;
  - ORIGINAL_K NONE (budget 0, G22);
  - ML_3p6_0.4, ML_3p6_0.6, GL10 and STAGE0 NONE;
  - `GATE_STATUS_LIST.json` (classifier A's schema), `GATE_STATUS_REPORT.json`, the replay plan (PRIMARY budget = the member count unless a cap fired; ORIGINAL_K 0; sensitivity 0; `pass_one` = this plan; the launch-registry pin) and `stage0_status = NOT_EVALUATED_BEFORE_FREEZE [NOT_IN_PHASE_1]`;
  - the step-7 ledger `<step7_ledger_root>/STEP7_LEDGER_<sha256 of BUILD_RECORD.json>/` holding only `LEDGER_GENESIS.json` (TESTED, K15).
- Root pins the six roster pins of `ROSTER_PINS.json` unedited, and the `BUILD_RECORD.json`. TESTED (B02, B03).

**4a. Gate-status list (M-15).** The builder writes the list twice over one computation:
- `GATE_STATUS_LIST.json`, exactly classifier A's `GATE_STATUS_LIST_C4V001`: `{gates: [{gate_sha256, status, pinned_by_entry}]}`, status `ON-TIME` or `LATE`, one entry per gate document sha, no repeats, `pinned_by_entry` = the V006 heading of the entry whose bytes first carry the gate's full sha in the cutoff copy. Root pins this file, unedited, as the classifier bundle's `gate_status_list`. TESTED (X01).
- `GATE_STATUS_REPORT.json` (`GATE_STATUS_REPORT_C2V003`, the c2v002 list form): per gate the reason, the pre-launch record list membership and the rosters; the record and receipt times. The list is its exact projection (TESTED, X01).
- A gate is **ON-TIME** if and only if its full sha occurs in the logged pre-launch V006 bytes and the record's `date -u` is not after the earliest identity-pair launch receipt. The same second counts as preceding, because the script writes the record first. Every other gate is LATE. Every gate first adopted at step 4 is LATE (r3a L455). TESTED (M01–M05, M09, M10).

**2. Pass one (D1).** `pass` with `pass_label PASS_ONE`, the FULL `BUILD_RECORD.json`, its `REPLAY_PLAN.json` and `ROSTER_PINS.json`, the freeze-module pin the build record names, the saved selection and spec, and the registered `null_direction_rule`. In memory it runs `evaluate_envelopes` for PRIMARY (the plan's budget) and ORIGINAL_K (budget 0), `select_reference_member` and `evaluate_sensitivity` (budget 0). It writes only `PASS_RECORD.json`. The driver refuses: a plan that is not the build record's (`PLAN_NOT_OF_BUILD_RECORD`, shared with step 7: K04, K05), roster pins of another build (V04), a freeze-module pin other than the build record's (V07), a superseded plan (K08, and on a copy of the build directory K11), pass k under a MEMBERS plan (V05), and pass one under a successor plan (FORMAL). TESTED (B03, V01).

**5. Pin and retain** (byte-identical through scoring):
- the slots, the query manifest, the six rosters, every cut and gate record, and the GL-node record with its sources and the route-B config;
- the TSR flag record V002, compare, N1 and node;
- the PLAN outputs, the selection and spec, the BUILD_RECORD, the replay plan, the gate-status list and report, and the launch registry;
- every attempt's receipt;
- the pre-launch record and its V006 copy;
- the step-7 ledger directory (append-only);
- the builder.
Registration is custody, not cut certification (V001 L16). A registered result whose bytes no longer verify makes the pass refuse (`PASS_RESULT_CUSTODY_BREACH`; root rules, G16): the adapter's log entry TESTED (B23), the driver's refusal FORMAL.

**6. Replay adapter.** `make_replay_adapter(replay_plan, alternative, log, context)`. It returns only the saved, byte-verified raw result for (alternative, exact theta). It raises on an unknown theta or on a failed call with no saved result, and logs a result whose bytes no longer verify. It never launches, substitutes or invents. TESTED (B23).

**7. Pass two and the D1 check.**
- `pass` with `pass_label PASS_K` under the same build record and plan (later, under the step-7 successor; below).
- `step7` with `{build_record, replay_plan, pass_one, pass_k}` (input schema `STEP7_INPUT_C2V003`). It refuses unless:
  - the build record's ledger exists with its own genesis entry (`STEP7_LEDGER_MISSING`, TESTED K12; `STEP7_LEDGER_BROKEN`, TESTED K16) and no second ledger sits beside the build record (`STEP7_LEDGER_SECOND_LEDGER`, TESTED K13);
  - the replay plan is the build record's `REPLAY_PLAN.json` or a successor verified through the build record's ledger (`PLAN_NOT_OF_BUILD_RECORD`; TESTED K04, K05);
  - the plan has no NEW_UNEVALUATED successor already (`STEP7_PLAN_SUPERSEDED`; TESTED K03, and on a byte copy of the build directory K10);
  - pass k ran under this plan and this build record, and pass one under the pass-one plan of record (`STEP7_PASS_NOT_OF_THIS_PLAN`; TESTED K02 for pass k, FORMAL for pass one);
  - each pass ran under the recorded rosters (`STEP7_ROSTER_NOT_REGISTERED`, TESTED P03; `STEP7_PASS_ONE_ROSTER`, FORMAL);
  - each pass's per-alternative budget equals its plan's `member_budget` (TESTED K01), exactly the members below the budget are evaluated (FORMAL), and the sensitivity budget equals the plan's (TESTED K06) or, in a Phase-2 successor, the value the sensitivity-budget rule gives on pass k's own plan (TESTED P02), with exactly the leading entries evaluated (FORMAL) (`STEP7_PASS_BUDGET_MISMATCH`).
- It returns one of three results:
  - **NO_NEW_DISCREPANCY**: go to step 8.
  - **NEW_UNEVALUATED**: rule (b) is applied in Phase 1 as well (CHOICE C3). The successor replay plan marks the member UNEVALUATED; it is written into the ledger and into the out-dir. Run `pass` PASS_K under the successor and `step7` again, comparing with pass one. Budgets only fall, so this terminates.
  - **STOP_NOT_MECHANIZED**: the selection, member list or sensitivity plan itself differs. No freeze; root rules (G2 residual).
- **7a. The step-7 ledger** (append-only, exclusive create; C25 as amended by C34).
  - **Where.** `<step7_ledger_root>/STEP7_LEDGER_<sha256 of BUILD_RECORD.json>/`. Root fixes `step7_ledger_root` (G28); the FULL build input names it and `BUILD_RECORD.json` records it, so the record's sha256 binds it. It must be an existing absolute directory outside the build directory (`STEP7_LEDGER_ROOT_INVALID`, TESTED K14; `STEP7_LEDGER_ROOT_INSIDE_BUILD_DIR`, FORMAL). The ledger depends only on the record's bytes, never on where a copy of the build directory sits: a byte copy of the build directory finds the same ledger (TESTED K10, K11).
  - **Genesis.** The FULL build creates the directory and `LEDGER_GENESIS.json` (`STEP7_LEDGER_GENESIS_C2V003`: the build record sha and the replay plan sha), by exclusive create, before it writes `BUILD_RECORD.json` (TESTED K15). A ledger that is absent reads `STEP7_LEDGER_MISSING`, never an empty ledger (TESTED K12); a genesis of another record reads `STEP7_LEDGER_BROKEN` (TESTED K16).
  - **One ledger per plan under the root.** A FULL build whose replay plan already has a ledger under the same root refuses (`STEP7_LEDGER_PLAN_ALREADY_LEDGERED`, TESTED K17). A rebuild into a new directory is a new BUILD_RECORD sha; it cannot obtain a second, empty ledger for the same plan unless root changes the root (G28 makes that a V006 event).
  - **Second ledger.** A `STEP7_LEDGER` directory beside the build record (the c2v002 location) refuses (`STEP7_LEDGER_SECOND_LEDGER`, TESTED K13).
  - **Content.** Each step-7 run appends `STEP7_<seq>.json` (hash-chained to the previous result, carrying the build record sha), copies of both pass records and any successor plan. Every read re-derives every result from its stored passes and requires each successor to equal, byte for byte, what step 7 makes from its predecessor. A forged or non-re-deriving entry reads `STEP7_LEDGER_BROKEN` (TESTED K07, K09). A plan compared once with NEW_UNEVALUATED can never be compared or passed again (`STEP7_PLAN_SUPERSEDED`, `PASS_PLAN_SUPERSEDED`). Deleting the last entry is not detectable by the tool: root logs the ledger head's sha in the freeze entry.
- `step7` never writes a roster. TESTED (B03, P02, P03, P09, K01–K17).

**8. Freeze.**
- Preconditions: the seal entry exists (A133 §2 row 2); the S1 reading released the phase's reads (A150); the ledger head is NO_NEW_DISCREPANCY on the plan the freeze uses.
- The freeze script runs a final `pass` PASS_K **in process** under that plan, requires its record to equal, byte for byte, the pass-k record of the ledger head, and calls `write_freeze_manifest(allow_incomplete=True, row_registration_rosters=<the six registered pins>, input_files=<§1 list>)` on the driver's in-memory outputs. The result is FREEZE_INCOMPLETE, with `EXPLORATION_STATUS_BUDGET_EXHAUSTED`, `ALTERNATIVE_ORIGINAL_K_MEMBER_EVALUATION_BUDGET_EXHAUSTED` and `SENSITIVITY_BUDGET_EXHAUSTED` (FORMAL, v003g L2527-2539; the latter two TESTED in B03). The script is not delivered here (G26, UNTESTED).
- Verify it. Log the manifest file sha, the registration sha, the Phase-1 record sha, the L1 sha, the build record sha and the step-7 ledger directory and head sha before any target is opened (A133 §1.6).
- The predictions are the reference member's `speeds_km_s`.

**8a. Pre-target checks** (§6 below).

**9-pre. Seal check (M-6)** (§6 below).

**9. Score (A133 §2 row 5).**
- Only when root authorizes it: `score_after_freeze(manifest, registration, logged sha, the same six-roster mapping)`.
- Classifier A on the real score, labelled PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) (M-8), with the bundle inputs of §6b.
- No roster, cut or reference is chosen after targets are seen (v003g L4192-4194 refuses changed external pins, FORMAL).

**10. Denominators.** 43 for PRIMARY; every registered null INVALID is a miss; STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (NOT_IN_PHASE_1) and is unscored; ORIGINAL_K reads NOT_AVAILABLE (I-4, M-10 precedence).

## 3. Phase 2 (registered step 4 and the full step-5 set, unchanged; score of record)

**0. Fixed before the Phase-1 score** (A133 §3; r3a I-7):
- rules (a)–(f), the re-binding rule and the commitment;
- the gate set: gates pinned in V006 before the Phase-1 score; the cutoff is the V006 byte copy whose sha the Phase-1 score entry logs, kind PHASE1_SCORE;
- the module and slots of the seal entry (the M-14 successor's, if pinned; G21).
Any stop or change after the Phase-1 score makes Phase 2 EXPLORATORY, recorded as the commitment status in the score entry. Phase-2 step-5 reads also wait for S1-B PASS when u_A is AT_ANCHOR (A150 R-S1-1).

**1a/1b.** Selection on the campaign's own calibration record, outside the Phase-1 registry root (PHASE_MISMATCH needs the two roots disjoint, r3a L196); save the selection and spec. PLAN stage (phase PHASE_2), then `evaluate_envelopes(budget=0)` for every EVALUATED alternative: PRIMARY, ORIGINAL_K, and STAGE0 if the successor is pinned. Save the value-free outputs.

**1. Step-5 runs.**
- The members, the ORIGINAL_K twins and, if the successor is pinned, one STAGE0 call per PRIMARY member (M-14), each registered in the Phase-2 launch registry.
- Headline calls launch first. STAGE0 is admitted under the memory gate and never pre-empts a headline call.
- Rule (c) relaunch as §1 states; rule (d) R-D9 hull miss on the campaign side, with no widening; rule (e) D_lo/D_hi as the comparator decides; rule (f) caps.
- **Re-binding (A133 L203):** a Phase-1 result file is reused when the theta bits, the NGC spec sha (without column_workers once the identity is TESTED), the driver sha and the roster inputs match. "Roster inputs" means the call's own cut record (CHOICE C6; G14). A re-bound call keeps its receipts in exactly one call record (R2).
- Phase-2-only outputs stay validity-only until Phase-2 step 4.

**2. Pass one (D1).** When every member, twin and STAGE0 call has a terminal receipt:
- run `build` at stage MEMBERS (phase PHASE_2), with the Phase-2 launch registry of those calls;
- run `pass` PASS_ONE with the MEMBERS `BUILD_RECORD.json`, plan and roster pins. In memory: `evaluate_envelopes` for each evaluated alternative, `select_reference_member` and `evaluate_sensitivity(budget=0)`. It writes `PASS_RECORD.json` and **2b** `SENSITIVITY_PLAN_VALUE_FREE.json` (the whitelist extract). TESTED (V02).

**2c.** Launch the sensitivity calls at the plan thetas, under rule (c), each registered (kind SENSITIVITY, the plan's entry id and theta key). They are registered Phase-2 step-5 calls from the moment the plan is saved, so step 4 cannot begin before their receipts (G13). TESTED (P07).

**3. Gather.** Call records for every member, twin, STAGE0 and sensitivity call, failures included.

**4. Registration.**
- **When:** step 4 begins automatically when every registered Phase-2 call has a terminal receipt under rule (c). Its start is the write time of the last registered receipt, and a tie counts as before (`replay_plan.step4.start_utc`; TESTED, P01, P05).
- **Build:** stage FULL (phase PHASE_2), with:
  - `gate_cutoff = {PHASE1_SCORE, …}`;
  - `members_stage_rosters` = the MEMBERS pins, and `members_stage_build_record` = the MEMBERS `BUILD_RECORD.json`;
  - `sensitivity_plan_output` = the saved `SENSITIVITY_PLAN_VALUE_FREE.json`;
  - `launch_registry` = the Phase-2 registry (members, twins, STAGE0 and sensitivity calls);
  - `step7_ledger_root` = the root-fixed root (G28);
  - the same `m15` as Phase 1, so a gate's status is the same in both phases (TESTED, P01);
  - `other_phase_calls []`.
- **Outputs:**
  - PRIMARY: PER_THETA over the member and sensitivity contexts;
  - ORIGINAL_K: PER_THETA;
  - STAGE0: PER_THETA only under the successor;
  - the other alternatives: NONE;
  - the Phase-2 FULL build's own ledger.
- **Pinning:** root pins the six unedited and the `BUILD_RECORD.json`. These are "not roster changes" (r3a L480).

**4a.** Gate-status list and report, as in Phase 1.

**5, 6.** As in Phase 1, plus the sensitivity plan, the MEMBERS rosters and the MEMBERS build record.

**7. Pass two; rule (b).**
- `pass` PASS_K under the FULL build record and plan, at the plan's budgets (sensitivity budget from the plan), then `step7` as in Phase 1. A discrepancy makes that member UNEVALUATED (FREEZE_INCOMPLETE). It is **never** resolved by a successor made by root, and a later agreeing pass never resolves it: the superseded plan is refused, also on a copy of the build directory and on a rebuild under the same ledger root (K03, K08, K10, K11, K17). This replaces V001 L21 (A133 3 (b)).
- If the D1 member is among those made UNEVALUATED, D1 moves. Then, under the successor, `pass` itself:
  - runs `evaluate_sensitivity(budget=0)` in memory for the new D1's plan;
  - sets the sensitivity budget to the leading plan entries that have a saved evaluated call (the `sens-budget` rule; `sensitivity_budget_source SENS_BUDGET_RULE`), which `step7` re-derives from pass k's own plan;
  - launches no call for the new plan.
- Iterate until NO_NEW_DISCREPANCY. TESTED (P02).

**8. Freeze.**
- As in Phase 1 (in-process final pass, byte-equal to the ledger head's pass k; G26), with `write_freeze_manifest(allow_incomplete=True, …)` and the same `input_files` list. **Root ruling required (G3):** ROOT_CALL_ORDER_V003D step 5 (allow_incomplete False) is departed from only in Phase 1. Without this ruling, any rule (b) or (f) outcome makes the Phase-2 freeze refuse (v003g L3675-3678, FORMAL).
- Log the shas (including the build record and the ledger head) before the Phase-2 `score_after_freeze`.
- AT-0b and AT-1 are computed target-free and published (A133 §2 row 6). They are never stop inputs (r3a M-5).

**8a, 9-pre.** As in Phase 1 (§6), plus the commitment status in the score entry.

**9.** `score_after_freeze` on the Phase-2 manifest: the score of record (I-7).

**10.** Denominators:
- 43 for PRIMARY and ORIGINAL_K.
- STAGE0 only if EVALUATED_BEFORE_FREEZE under M-14: Q36–Q43, denominator 8, `headline=false`.

## 4. A133 §3 rules: where each is executed

| rule | executed by | test |
|---|---|---|
| (a) rosters from the pinned builder, run-produced cuts, gates pinned in advance | `build` (FULL), the gate cutoff and the full-sha pin check; each call's own cut record and result (inside its terminal run directory; a cut record inside no run directory of another call, G29); one run file per call across every roster and OTHER call (realpath or file identity); one FINISHED-result content per call (C38); root pins unedited | B02, B05, B08, B09, B10, B11, P01, H01–H13, J01–J12 |
| (b) step-7 discrepancy → that member UNEVALUATED, never a root successor | `step7`: the build record's plan or a ledger-verified successor only; each pass bound to its plan and budgets; the append-only ledger at the root-fixed path keyed by the build record sha (copy-proof; one ledger per plan under the root); no roster output | P02, P03, P09, K01–K17 |
| (c) step-5 NGC call: "rerun the identical spec with the RSS cap at RAM and the wall cap doubled"; "marked invalid only after two identical deterministic failures that are not INFRA, with no other NGC process running"; never a deadline. A141 L1: OUTPUT_CAP rerun with the output cap raised | `build` terminal classes from receipt evidence: a rule-(c) pair (identical raw status, identical spec, `other_ngc_processes_max` 0 on both counted attempts, rerun RSS cap = host RAM, rerun wall cap = 2 × the first attempt's, OUTPUT_CAP cap raised), judged on its own prefix; one spec per call; every receipt bound to its call through the launch registry; distinct, ordered attempts; one receipt per call; nothing after a terminal. The relaunch itself is the launch workflow; the evidence keys are G25, the registry and binding keys G27 | B14, B15, B20, B21, C01–C08, O1a–O8, R1a–R1c, R2a–R2j |
| (d) R-D9 hull miss: registered response, then (c) | campaign side; this runbook consumes the calibration record only | none |
| (e) D_lo/D_hi: the comparator decides | consumed as produced; no step-4 or step-7 judgment | none |
| (f) caps are value-relevant: a fired cap leaves the member unevaluated | CAP or OUTPUT_CAP rule-(c) pair → UNEVALUATED_CAP, budget prefix | B20, C08 |

## 5. STAGE0 receipt rule (M-14), Phase 2

- `replay_plan.stage0_status` is computed mechanically. It is the builder's own record, **not** classifier A's STAGE0 status record: root writes that one as an exact projection of the frozen manifest `stage0_status` block of the STAGE0 successor (A154; §6b).
- **NO_SEALED_SUCCESSOR:** when the phase's slots do not declare STAGE0 EVALUATED, which is the case under V003.
- **STAGE0_RECEIPT_NOT_FINISHED:** when a registered STAGE0 call's terminal class is not FINISHED.
- **EVALUATED_BEFORE_FREEZE:** otherwise, subject to EVALUATED_REFUSED by the successor at the freeze.
- Every STAGE0 receipt time and the step-4 start are recorded. RECEIPTS_AFTER_STEP4 cannot arise, because the start is the last registered receipt.
- The successor's TEST (a) must show that v003g completes a Phase-2 freeze with STAGE0 NOT_EVALUATED (A154 reports it TESTED in the successor's own build; not re-run here). TESTED on synthetic successor slots (P05).
- Root publishes the STAGE0 delay at the Phase-2 selection (A142 item 3).

## 6. Pre-target checks before step 9 (both phases)

**8a.**
- `tsr-check` on the flag record pin (V002), with the frozen manifest (input schema `TSR_CHECK_INPUT_C2V003`). TSR_FLAG_TABLE_MISMATCH fires if any of these fails:
  - the flag record is `c9d8ab45` (a builder constant; an unsealed variant with any changed byte stops, `FLAG_RECORD_NOT_THE_PINNED_RECORD`);
  - the record has exactly classifier A's keys (`target_free`, `rule`, `failing_ring_ordinal`, `ntest_compare_pin`, `n1_record_pin`, `gl_node_record_pin`, `flags`), `target_free` true and `failing_ring_ordinal` 15 (V001's form now stops: TESTED X04);
  - the compare is `6f095f64` with failing TRUNCATION_SHAPE rings exactly {15} and no other failing ring;
  - N1 is `8867c376`, with ring 15 at the compare's `R_kpc`;
  - the node record is `ec1dcca5`, with GL4 radii equal to N1's;
  - the 43 flags, in manifest order, are exactly {NGC3198-Q25};
  - the N1 rings 14 and 16 equal the builder's bound constants bitwise (the open interval is stated in the record's rule text, V001's verbatim);
  - all four files are in `input_files`.
  TESTED (T01–T09; production record PASS from bytes).
- `check-gate-list` with `{roster_pins, gate_status_list, build_record}` (input schema `CHECK_GATE_LIST_INPUT_C2V003`): GATE_STATUS_LIST_DEFECT fires if the list is not exactly `GATE_STATUS_LIST_C4V001` (TESTED X03, X06), a root-listed gate of the rosters is missing (TESTED M08), or the list is not, byte for byte, the FULL build's `GATE_STATUS_LIST.json` (TESTED X05: a well-formed list with an edited status). Roster pins that are not the build's refuse (`ROSTER_PINS_NOT_OF_BUILD`, FORMAL). TESTED (M07, M08, X03, X05, X06).
- The sealed classifier's synthetic pre-score run on the frozen member arrays, covering REFERENCE_MEMBER_MISMATCH, PHASE_MISMATCH (the calibration-record path against the Phase-1 registry root the seal entry names) and the rest of r3a §1.1. It goes in the seal or score entry (r3a L184-185).

**9-pre.** `seal-check` with `{v006_copy, objects, freeze_manifest}` (input schema `SEAL_CHECK_INPUT_C2V003`): a V006 byte copy taken after the seal entry, the sealed objects, and the frozen manifest.
- **Seal-entry format (proposed under G17; C27).** The seal entry is the first `## ` heading that carries the token `SEAL_ENTRY` and the sealed text's full sha256. Its section has one line per sealed object, of exactly this form (free text may follow the closing backtick):
  ```
  ## A<n>: SEAL_ENTRY <phase> <text sha256>
  - PREREG_TEXT: `<sha256>`
  - CLASSIFIER: `<sha256>`
  - TSR_FLAG_RECORD: `<sha256>`        (c9d8ab45…, V002)
  - STAGE0_SUCCESSOR: `<sha256>`   (only if pinned)
  - BAND_AGREE: `<sha256>`         (and any other sealed object)
  ```
- SEAL_SHA_MISMATCH fires, and `score_after_freeze` is not called, if any of these fails:
  - roles PREREG_TEXT, CLASSIFIER and TSR_FLAG_RECORD are supplied;
  - every supplied role is a distinct object (no two roles share a sha256 or a file);
  - the entry names each role exactly once, the roles it names equal the supplied roles, and its PREREG_TEXT line equals the heading's sha;
  - each object's bytes hash to the sha on **its own role line** (a sha that occurs elsewhere in the entry, such as "replaces the withdrawn …", does not count);
  - the sealed TSR flag record is `c9d8ab45` and its exact pin is in the frozen manifest's `input_files`.
  TESTED (S01–S12), except the PREREG_TEXT-line check (FORMAL). What follows a stop is not yet ruled (G16).

## 6b. Classifier A's input records (README_CLASSIFIER_A_C4V001 `4e1e7493`, "Root-written input contracts")

**Written by this builder, in A's schema exactly** (an object with exactly the keys A's README shows; no `schema` key, open item OI-A1):

| A bundle role | file | schema | how |
|---|---|---|---|
| `gate_status_list` | `<FULL build>/GATE_STATUS_LIST.json` | `GATE_STATUS_LIST_C4V001` | `build` (FULL); `check-gate-list` binds it to the build. TESTED (X01, X03, X05, X06, M07, M08) |
| `tsr_flag_record` | `ROOT_TSR_FLAG_RECORD_V002.json` (`c9d8ab45`) | `TSR_FLAG_RECORD_C4V001` | `tsr-record` from V001 by projection (V001's rule text, ordinal 15, its three pins and its 43 flags, verbatim); `tsr-check` verifies it. TESTED (X02, T01, T08) |

**Expected by classifier A and not written by this builder** (the builder's constant `A_INPUTS_NOT_PRODUCED`; TESTED X07 that the two lists cover A's 17 roles exactly):

| A bundle role | who writes it |
|---|---|
| `phase_inputs` (`PHASE_INPUTS_C4V001`) | **root**: phase named by the score entry, both registry roots, run status and code, the Phase-1 header (B_P1, u_A log index, Phase-1 record and L1 shas), the absent-reason. None of these is a builder input |
| `stage0_status` (`STAGE0_STATUS_RECORD_C4V001`, Phase 2) | **root**, as an exact projection of the frozen manifest `stage0_status` block of the STAGE0 successor (A154). The replay plan's `stage0_status` is not this record |
| `commitment_status` (`PHASE2_COMMITMENT_STATUS_C4V001`, Phase 2) | **root**, with the Phase-2 score entry |
| `fallback` (`FALLBACK_RECORD_C4V001`) | **root** |
| `field_map` (`KEY_FIELD_MAP_C4V001`) | **root**, only if a key rename is needed |
| `root_disclosures` | **root** (D-4 values, attestation, V005/V006 shas, RUNBOOK_V002 and builder shas, window changes, `outer_gas_cut_report`) |
| `freeze_manifest` | v003g `write_freeze_manifest`, run by the step-8 freeze script (G26) |
| `score` | v003g `score_after_freeze` (step 9) |
| `slots` | the sealed slots (V003, or the M-14 successor), pinned as is |
| `tsr_support_record` | UNT_ROOT_TSR_SUPPORT_CX3V001: does not exist; root ruling G7 |
| `ntest_compare` | the compare of record `6f095f64`, pinned as is |
| `agree_record` | the pinned phase1 tool's `agree` command (OC-02) |
| `phase1_classification` | classifier A itself (its Phase-1 output) |
| `l1_record` | the pinned phase1 tool's `band` command (`L1_C2V001.json`) |
| `c3_record` | the M-13 record |

The bundle's `rosters` are this builder's six FULL rosters (schema `ROOT_ROW_REGISTRATION_ROSTER_CX3V001`; A reads `schema` and `root_gates`); `sealed.tsr_flag_record_sha256` is `c9d8ab45`.

## 7. Root rulings this runbook needs

- **G1:** pin the builder and this runbook before Phase-1 step 4 (A133 row 4 places them after the freeze that needs them).
- **G2 residual:** a STOP_NOT_MECHANIZED step-7 result (a selection, member-list or plan difference that is not a member discrepancy).
- **G3:** Phase-2 `allow_incomplete=True`, ruled before the Phase-1 score.
- **G7:** whether the TSR support record exists, its writer and its point_key. V001 carries it as PENDING; V002 (A's schema) has no field for it.
- **G8 (UNTESTED):** the program query manifest under v003g's target screen. A PLAN build is the deciding test.
- **G9 (UNTESTED):** real results through `_v010_preflight`. The deciding test is pass one on the S0 results.
- **G10 (UNTESTED):** that real cx3r008/v011 runs write NGC_CANDIDATE_ROSTER_CUT_CX3V001 records inside the call's terminal run directory, which is the builder's ownership test (G29 residence), and that no call's run directory lies inside another call's.
- **G13:**
  - the Phase-1 call set (taken here as members, F points and the twin's planned stop);
  - the Phase-2 sensitivity registration (from the saved plan);
  - the receipt status map (named once per producer).
- **G14:** "roster inputs" in the re-binding rule; taken here as the call's own cut record.
- **G15:** the pre-launch record path and format (proposed: `M15_PRE_LAUNCH_RECORD_C2V001`).
- **G16:** the remedy after a pre-target stop, or after `PASS_RESULT_CUSTODY_BREACH`.
- **G17:** the seal entry; its format is proposed in §6.
- **G18:** the RI45-14 list.
- **G19:** the unruled RI45 items.
- **G20:** ROOT_CALL_ORDER_V003D's path.
- **G21:** the STAGE0 slots pin under a successor.
- **G24:** the Phase-1 gate cutoff; proposed here as the V006 at the step-4 start.
- **G25:** the rule-(c) receipt evidence. Root names, per receipt producer, the keys for `spec_sha256`, `rss_cap_bytes`, `wall_cap_s`, `host_ram_bytes`, `other_ngc_processes_max` and `output_cap_bytes`, and confirms that the launch workflow writes them by machine (the solo value from its process monitor over the whole attempt). Root also confirms or replaces four readings of the A133 text: "with no other NGC process running" applies to both counted failures (the campaign-halt branch says "both"); "at RAM" means equal to the host RAM the receipt records; "doubled" means exactly twice the call's first attempt; "identical deterministic failures" means the identical raw status, with no further determinism test. Until G25 is ruled and the receipts carry the keys, no step-5 call can be marked invalid or unevaluated: a failed call stays non-terminal and is rerun. A154 lists "the rule-(c) receipt format, to be bound to RUNBOOK_V002's receipts" as open: G25 with G27 is that format's proposal.
- **G26:** the step-8 freeze script: an in-process final pass under the step-7-final plan, byte-equal to the ledger head's pass k, then `write_freeze_manifest` on the driver's in-memory outputs, after the seal. Not delivered by this build.
- **G27:** the launch registry and the receipt binding. Root confirms or replaces: (1) the registry's producer (the launch workflow, by machine, at each launch) and its schema (`STEP5_LAUNCH_REGISTRY_C2V003`, §1), including OTHER entries for the F points and the twin; (2) the receipt key that carries `theta_sha256` and its value: sha256 of the v003g canonical bytes (`json.dumps(sort_keys=True, separators=(',', ':'))`) of the call's exact `theta_ngc`. If the program's own θ key (A136 G3, A148) is a different function, the receipts must carry this value as well, or a successor builder takes the other function; (3) that every receipt, of every class, carries both binding keys. Until G27 is ruled and the registry exists, no FULL or MEMBERS build can be made.
- **G28:** the step-7 ledger root: an absolute directory outside every build directory, fixed by root in V006 before the first FULL build and kept for both phases. Changing it is the only way a plan could get a second ledger, so a change is a V006 event.
- **G29 (ruled by root; implemented in c2v005):** file reuse across calls (RI45-11). As ruled: (1) a cut record is bound to its call by residence: inside its call's own run directory and inside no other call's, plus distinct file identity; (2) the byte-equality refusal for cut records is removed (two honest calls may emit byte-identical cut records); (3) C38 is kept: a FINISHED call's result byte-identical to another call's cut record or result refuses; (4) FAILED calls' failure records may be byte-identical and must reside in their own run directory. c2v005 reads "its own run directory" as the terminal attempt's run directory, the directory c2v001–c2v004 already required (CHOICE C41), and "any other call's" as every attempt's run directory of every other roster or OTHER call (C42). Still open from c2v004's item (4): a file from a run that is not one of the build input's calls, or a copy written by hand into a call's own run directory, cannot be recognised by path, identity or content; only a binding key carried in the cut record and result (`theta_sha256`, `spec_sha256`, as receipts carry under G27), a change to the CX3V001 cut-record producer, would close it. Root decides whether that successor is wanted; it is not needed by any honest producer (A115).

**Open items for Claude4's review (classifier A's owner; this build did not open `classifier_a_c4v001.py`):**
- **OI-A1.** A's README says each root-written record is "a JSON object with exactly the keys shown" and shows no `schema` key for these records (the bundle and the output list `schema` explicitly). This build therefore writes `GATE_STATUS_LIST.json` and V002 **without** a `schema` key, and `check-gate-list`/`tsr-check` refuse one (X06). If A requires `schema` (for instance `GATE_STATUS_LIST_C4V001`), a successor adds it; it is one constant per record.
- **OI-A2.** `pinned_by_entry`: A says only "a non-empty string". This build writes the full V006 heading text of the entry whose bytes first carry the gate's full sha in the cutoff copy (for example `A900: gate G1 pinned (synthetic)`), not an entry id alone.
- **OI-A3.** Statuses are written `ON-TIME`/`LATE` as A's README spells them; the builder's report keeps `ON_TIME`.

## 8. TESTED / FORMAL / UNTESTED

Step map: none (V001 numbering kept).

- **TESTED.** Synthetic suite `test_runbook_v002_c2v005.py`, run twice as record runs (`test_records_c2v005/RUN1`, `RUN2`): 149/149 each (38 MUST_PASS, 111 MUST_FAIL), with byte-identical TEST_RECORD files (`dbabe47228bf45ae43313b46e3cfa16f7e4686365a077f6464319faa0cb1847e`; `results_sha256` `dc360aa67eb1175bdcf65c1c3855c3890914cb76acaa467913e978ce43ee2e8d`). All 137 c2v004 cases are ported in c2v004's order. 135 keep their ids, expectations and observed codes (checked against the c2v004 record). Two change expectation under G29, from MUST_FAIL `CUT_RECORD_BORROWED` (by sha256) to MUST_PASS, with id suffixes changed to say so: `H02_..._refused` became `H02_byte_copy_of_M000_cut_record_in_M001_run_dir_builds_G29`, and `H06_..._refused_G29` became `H06_distinct_calls_with_byte_identical_cut_records_naming_no_call_build_G29`. H08's docstring lost its reference to a cut-record sha256 check; its body is unchanged. 12 cases are new (J01–J12). The c2v004 fixture form (a synthetic cut record names its call) is kept; H06, J04 and J08 use the plain form.
  - The end-to-end cases run the real v003g functions (`evaluate_envelopes`, `select_reference_member`, `evaluate_sensitivity`, `_load_row_roster`, `_row_contract`, `_root_frozen_rows`, `_incomplete_reasons`) through the delivered `pass` driver on synthetic slots, nodes, query manifest, selection and spec. The module's constants are patched, so no program slots are read.
  - The production TSR flag record V002 passes `tsr-check` against the real compare, N1 and node bytes, and `tsr-record` reproduces it byte for byte from V001.
  - Development checks (scratchpad, not record runs):
    1. The c2v005 suite run against the c2v004 builder's bytes gives 139/149. It fails H02, H06, J04 and J09 (c2v004's cut-record content rule), J01–J03 (OTHER calls outside the run-file check: the re-verify probes Q4b, Q4, Q5) and J06, J07, J12 (no residence rule). So the suite reproduces the re-verify finding and the G29 changes against c2v004.
    2. The re-verify probe script (Q1–Q9), run unchanged on the c2v005 builder:
       - refused: Q1 (A2e), Q4, Q4b and Q5 (by file identity or realpath), and Q9 (C38);
       - built, as G29 rules: Q2 (a byte copy), Q3 and Q3b (re-serialized copies), Q6A and Q6B (both call orders), Q7 (a hard link of a file outside every call), and the Q8 control.
    3. Ten mutants of the c2v005 changes, 9 killed:
       - OTHER calls left out of the run-file check (J01–J03);
       - no residence check (J06, J07, J12);
       - residence against roster calls only (J07);
       - residence against terminal run directories only (J12);
       - cut records content-unique again, the c2v004 form (H02, H06, J04, J09);
       - realpath only, no file identity (H01, H03, H05, H07, H13, J02, J03, J08);
       - no C38 (H09–H11, J10);
       - content rule for every result (18 Phase-2 cases, H12, J09);
       - CUT_RECORD_BORROWED by the later file's role only (H07, J03, J10).
       The survivor, the c2v004 first-owner form of the content loop, is equivalent under c2v005. A call's result is listed before its cut record, and only FINISHED results carry the content rule, so the first owner of a sha256 can never hide a pair. All pairs are checked anyway.
- **FORMAL.** The v003g line citations above, read from `48a1e48a` bytes (by c2v002; not reopened); the A133 §3 (c) text (L216-219) and A141 L1/L4 quoted from bytes.
- **UNTESTED.**
  - The `pass` driver on real inputs: the real selection output and spec, the program query manifest, real saved results (G8, G9). The deciding test is the Phase-1 pass one on the S0 results.
  - Production PLAN, MEMBERS and FULL builds; real receipts with the G25 evidence keys and the G27 binding keys; a real launch registry; real cut records (G10).
  - Whether real FINISHED results of distinct calls always differ in bytes from every other call's cut record and result, so that C38 never refuses a legitimate build (two distinct calls that are the same computation, one theta and one spec in two alternatives, would refuse). The deciding test is the first MEMBERS or FULL build on real call records; a refusal `FILE_BORROWED` or `CUT_RECORD_BORROWED` "by sha256" there goes to root.
  - The production run layout under G29 residence: that every attempt has its own run directory and no call's run directory lies inside another call's (otherwise a cut record in the inner directory refuses `CUT_RECORD_IN_OTHER_CALL_RUN_DIR`). The deciding test is the same first real build.
  - The file identity on the production run root's file system (A157 names `/Volumes/External1/NGC_S0_PHASE1_V001`; not opened): that `st_dev` and `st_ino` are stable and distinct per file there. If the file system gave two files one number, the check would refuse a legitimate build; if it gave one file two numbers, a hard link would not be seen (C38 still catches a FINISHED result; a hard-linked cut record would then be caught only if it lay outside its call's run directory or inside another call's). The deciding test is the same first real build, or a two-file `stat` probe on that volume.
  - The step-7 ledger in production under the G28 root.
  - Classifier A reading `GATE_STATUS_LIST.json` and V002 (OI-A1). The deciding test is classifier A's `load_bundle` on a bundle pinning both (a Claude4 one-line check, or A's prescore mode).
  - The step-8 freeze script (G26) and `write_freeze_manifest` itself (it needs a real calibration record; not run here).
  - The M-14 successor; real-target scoring.
