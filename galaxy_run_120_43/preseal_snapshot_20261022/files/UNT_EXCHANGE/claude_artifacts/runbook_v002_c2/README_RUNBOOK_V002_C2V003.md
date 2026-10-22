date -u: Mon Oct 19 18:07:27 UTC 2026

# runbook_v002_c2, build c2v003: RUNBOOK_V002 and the roster builder, with the re-verify findings R1-R3 fixed and classifier A's input contracts met (root workflow build; not adopted)

**What this is.** The third build of the A142 build-table item "RUNBOOK_V002 and roster builder (A133), root workflow, Claude4 review". It fixes the three findings the re-verify raised against c2v002 (R1-R3, restated in the workflow journal) and conforms the records the builder writes to classifier A's input contracts (`README_CLASSIFIER_A_C4V001.md`, `4e1e7493`). Nothing here is adopted until root pins it and Claude4 reviews it. Nothing authorizes a launch or target access. No production build, pass or step 7 was run. The c2v001 and c2v002 files in this folder are unchanged and are superseded by these; root pins only the c2v003 files and `ROOT_TSR_FLAG_RECORD_V002.json`.

## Files

| file | sha256 | what it is |
|---|---|---|
| `roster_builder_c2v003.py` | `29870e5b8a24b83a9fb2fbdbea2a4ec4dcb172c40e62c1d52de9ba001deaadfa` | Commands: `build` (now with `launch_registry`, `step7_ledger_root`, A's gate-status list and the report), `pass`, `step7` (ledger at the root-fixed path), `sens-budget`, `check-gate-list` (A's schema, bound to the build), `seal-check`, `tsr-record` (new: derives V002), `tsr-check` (V002, A's schema). |
| `ROOT_TSR_FLAG_RECORD_V002.json` | `c9d8ab4573278f2d325bc5fe50e396e35e9981f0561cfa20e61e8a215bb5cea0` | The M-7 flag record in classifier A's `TSR_FLAG_RECORD_C4V001` schema, written by `tsr-record` from V001 (`61bd8a83`) by projection. A builder constant. |
| `RUNBOOK_V002_C2V003.md` | see `HASHES_C2V003.txt` | The per-phase runbook (V001 step numbers kept; no step map). New: §1 launch registry and receipt binding, §7a ledger location, §6b classifier A's inputs, G27, G28, OI-A1 to OI-A3. |
| `test_runbook_v002_c2v003.py` | `daf5555e6e49bd5abc8c21dad7e815ea68129b3000ec97fe8d842c82d547e2f5` | The synthetic MUST_PASS / MUST_FAIL suite: the 96 c2v002 cases ported, 28 new. |
| `test_records_c2v003/RUN1/TEST_RECORD.json`, `test_records_c2v003/RUN2/TEST_RECORD.json` | `ea18d7e8314c1fb60179ff75ce8cdbe62dd3b857e111f32ac402d0bbafe16e1b` (both; byte-identical) | Two record runs: 124/124 each (32 MUST_PASS, 92 MUST_FAIL); `results_sha256` `2898d533e769b10684f16e1e75e056ad0d3b84e3c23a49f2c79e11428416cd68`. |
| `test_records_c2v003/RUN*/work/` | not hashed | The synthetic fixtures each run wrote: launch registries, receipts, builds, ledger roots and ledgers (two ledger directories renamed by K12/K16), one symlink (O1b), forged ledger entries (K07, K09). |
| `HASHES_C2V003.txt` | — | sha256 of every file above, from bytes. |

## Running it (`python3 -I -B`; every input is a JSON document pinned by sha256)

```
python3 -I -B roster_builder_c2v003.py build           --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v003.py pass            --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v003.py step7           --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v003.py check-gate-list --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B roster_builder_c2v003.py tsr-record      --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B roster_builder_c2v003.py tsr-check       --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B roster_builder_c2v003.py seal-check      --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B test_runbook_v002_c2v003.py --record-dir NEW_DIR
```

- **Exit codes:** 0 built or passed; 2 refused (an input defect); 3 a pre-target stop or a STOP_NOT_MECHANIZED step 7; 1 an internal error.
- **Input schemas:** `ROSTER_BUILDER_INPUT_C2V003` (`STAGE_KEYS`), `PASS_INPUT_C2V003`, `STEP7_INPUT_C2V003`, `CHECK_GATE_LIST_INPUT_C2V003` (adds `build_record`), `TSR_RECORD_INPUT_C2V003` (`flag_record_v001`), `TSR_CHECK_INPUT_C2V003`, `SEAL_CHECK_INPUT_C2V003`, `SENS_BUDGET_INPUT_C2V003`; the launch registry `STEP5_LAUNCH_REGISTRY_C2V003`.
- **Where a FULL build's ledger is:** `<step7_ledger_root>/STEP7_LEDGER_<sha256 of its BUILD_RECORD.json>/`.
- **The suite never runs a production build or pass.** It patches the freeze module's slots and node constants to synthetic fixtures, and a read guard refuses any path outside its work directory except the two TSR flag records and the three files they pin.

## The re-verify findings and what fixed each

| finding | fix | tests |
|---|---|---|
| **R1.** An attempt after a terminal rule-(c) pair with a different `spec_sha256` re-rolled the call: `_rule_c_problem` read the spec set of every attempt, so the later spec un-terminated the pair | The pair is judged on `seen[:i+1]` only (`_rule_c_problem(prefix)`); nothing may follow the first terminal prefix (`ATTEMPT_AFTER_TERMINAL`). A call whose evidenced attempts carry more than one `spec_sha256` refuses (`RULE_C_SPEC_NOT_IDENTICAL`) | R1a (the verifier's probe: pair, then a FINISHED receipt of another spec), R1b (failure, then FINISHED of another spec), R1c (failure, then FINISHED of the same spec: EVALUATED), C05, O5–O7 |
| **R2.** One failure pair served two calls (byte copies of M001's receipts in M002's own run directories made both EVALUATED_FAILED) | Every receipt is bound to its call: its `theta_sha256` (new ninth receipt role) must equal the call's exact-theta key and its `spec_sha256` the spec sha of the call's entry in the pinned **launch registry** (new input, G27); the registry's theta key must equal the call's PLAN theta; registry entries and call records must match one to one; one call (alternative, theta) has one spec. One receipt, by realpath or sha256, serves one call across all roster and OTHER calls (`RECEIPT_REUSED_ACROSS_CALLS`) | R2a (the verifier's probe), R2b, R2c (twin registered at the serial's theta and spec, receipt byte-copied), R2d (same file), R2e–R2j |
| **R3.** The step-7 ledger beside the build record was reset by copying the build directory (same BUILD_RECORD sha, no ledger) | The ledger lives at `<step7_ledger_root>/STEP7_LEDGER_<BUILD_RECORD sha256>/`: root fixes the absolute root (G28), the FULL input names it, the BUILD_RECORD records it (so its sha binds it), and it must lie outside the build directory. The FULL build creates it with a genesis entry binding the record and replay-plan shas. A missing ledger refuses (`STEP7_LEDGER_MISSING`), never reads as empty; a `STEP7_LEDGER` beside the record refuses (`STEP7_LEDGER_SECOND_LEDGER`); a FULL build whose replay plan already has a ledger under the root refuses (`STEP7_LEDGER_PLAN_ALREADY_LEDGERED`, which also closes a rebuild into a new directory) | K10 (the verifier's probe: copy, then the superseded plan with an agreeing pass), K11 (the pass driver on the copy), K12–K17 |
| **Classifier A's input contracts** | The builder writes `GATE_STATUS_LIST.json` in A's `GATE_STATUS_LIST_C4V001` schema exactly (the c2v002 form is kept as `GATE_STATUS_REPORT.json`), and `ROOT_TSR_FLAG_RECORD_V002.json` in A's `TSR_FLAG_RECORD_C4V001` schema (V001's schema differs). `check-gate-list` and `tsr-check` read only A's schemas; `check-gate-list` also requires the list to be the build's own bytes. The 15 other inputs A expects are listed with their writers (RUNBOOK §6b; builder constant `A_INPUTS_NOT_PRODUCED`) | X01–X07, M07, M08, T01–T09 |

**Mutation check (development, scratchpad; not a record run).** 18 mutants, each removing one c2v003 fix from a copy of the builder; all 18 killed by the suite (list in RUNBOOK §8). The mutant that restores c2v002's ledger location fails K10 and K11, so the tests reproduce the copy attack against c2v002's semantics.

## Classifier A's records

- **Written here, in A's schema exactly:** `gate_status_list` (`GATE_STATUS_LIST.json` of the FULL build: `{gates: [{gate_sha256, status ON-TIME|LATE, pinned_by_entry}]}`) and `tsr_flag_record` (`ROOT_TSR_FLAG_RECORD_V002.json`: `target_free`, `rule`, `failing_ring_ordinal`, `ntest_compare_pin`, `n1_record_pin`, `gl_node_record_pin`, `flags`).
- **Expected by A and not written by this builder (root or another producer writes each):**
  - root-written: `phase_inputs` (PHASE_INPUTS_C4V001), `stage0_status` (STAGE0_STATUS_RECORD_C4V001, Phase 2; an exact projection of the frozen manifest `stage0_status` block of the STAGE0 successor, A154), `commitment_status` (PHASE2_COMMITMENT_STATUS_C4V001, Phase 2), `fallback` (FALLBACK_RECORD_C4V001), `field_map` (KEY_FIELD_MAP_C4V001, only if needed), `root_disclosures`;
  - other producers: `freeze_manifest` (v003g via the freeze script, G26), `score` (v003g), `slots` (pinned), `tsr_support_record` (does not exist; G7), `ntest_compare` (`6f095f64`, pinned), `agree_record` and `l1_record` (the phase1 tool), `phase1_classification` (A itself), `c3_record` (M-13).

## CHOICES this build made that the text did not force (root confirms or replaces each)

C1–C11, C13–C15, C17, C19 and C20 are carried from c2v001, and C21–C24 and C26–C29 from c2v002, unchanged. C25 (ledger location) is amended by C34; C28's pinned record moves from V001 to V002.

- **C30. One terminal prefix, one spec per call (R1).** A pair is judged on its own prefix. The one-spec check reuses the code `RULE_C_SPEC_NOT_IDENTICAL`; a present spec value of any type counts as evidenced. Check order inside a call: attempt structure, after-terminal, one spec, binding, last-attempt terminal rules.
- **C31. The launch registry (G27).** Schema `STEP5_LAUNCH_REGISTRY_C2V003` `{schema, phase, calls: [{alternative, kind MEMBER|SENSITIVITY|OTHER, key, theta_sha256, spec_sha256}]}`; it lists exactly the build input's calls, OTHER calls (F points, twin) included; one call (alternative, exact theta) has one spec; distinct calls may share a spec (A133 re-binding: the spec sha without column_workers).
- **C32. Receipt binding.** Every receipt of every class (FINISHED, INFRA and PLANNED_STOP included) carries `theta_sha256` (sha256 of the v003g canonical bytes of the exact `theta_ngc`; for OTHER calls the registry's key) and `spec_sha256`; theta is checked before spec.
- **C33. One receipt, one call.** Call identity is (alternative, exact theta) for roster calls (a MEMBER and a SENSITIVITY record at one theta are one call) and the label for OTHER calls; reuse by realpath or sha256 refuses. The M-15 identity-pair launch receipts are read for their time only and are not bound.
- **C34. The ledger location (R3; amends C25).** FULL input `step7_ledger_root` (existing, absolute, outside the build directory; recorded as its realpath); directory `STEP7_LEDGER_<BUILD_RECORD sha256>`; genesis `LEDGER_GENESIS.json` written by the build before `BUILD_RECORD.json` (so a build that fails after creating it leaves a ledger without a record, which root disregards); one ledger per replay plan under the root.
- **C35. Classifier A's record form.** Exactly the keys A's README shows, with no `schema` key (OI-A1); `pinned_by_entry` = the V006 heading text (OI-A2); statuses `ON-TIME`/`LATE` (OI-A3). The list is an exact projection of the report and is written by the build, never by hand.
- **C36. TSR V002.** A projection of V001: the rule text, ordinal, three pins and 43 flags verbatim; V001's support bounds, verbatim failing ring and cross-check fields are not in A's schema and are dropped from the record. `tsr-check` checks the compare's single failing ring, its N1 radius and the N1 neighbour radii (the bounds) against the pinned compare, N1 and node and the builder's bound constants. `tsr-record` accepts only V001 `61bd8a83`. V001 is no longer a classifier or `input_files` object.

## Gaps

Root rulings needed (detail in RUNBOOK §7): G1, G2 residual, G3, G7, G8, G9, G10, G13, G14, G15, G16, G17, G18, G19, G20, G21, G24, G25, G26, and new **G27** (the launch registry: producer, schema, OTHER entries, the θ-key function, binding keys on every receipt) and **G28** (the step-7 ledger root path). Until G27 is ruled and the registry exists, no MEMBERS or FULL build can be made.

**Open items for Claude4 (classifier A's owner):** OI-A1 (no `schema` key in the two records; confirm against `classifier_a_c4v001.py`, which this build did not open), OI-A2 (`pinned_by_entry` content), OI-A3 (status spelling).

## UNTESTED (deciding tests in RUNBOOK §8)

The `pass` driver on real inputs; production builds; real receipts with the G25 and G27 keys; a real launch registry; real cut records; the ledger in production under the G28 root; classifier A loading the two records (OI-A1); the freeze script and `write_freeze_manifest`; the M-14 successor; scoring.

## NOTEs (not blocking, recorded)

- A rebuild of the same input under a **different** ledger root gets its own ledger. That needs a change of the root-fixed root (G28), which is a V006 event, and produces a BUILD_RECORD sha other than the one root pinned at step 4.
- Deleting the last ledger entry is still not detectable by the tool (as in c2v002); root logs the ledger directory and head sha in the freeze entry.

## Deviations (disclosed)

- **Drafts in the scratchpad.** The builder, tests, runbook and README were drafted and iterated in the session scratchpad (`/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/rbv003c2/`); the mutation runs and five development runs ran there. Each final file here was then written once, by exclusive create, from those bytes. No existing file in this folder was edited.
- **V002 was written by the published builder.** `tsr-record` ran from this folder's `roster_builder_c2v003.py`; its input document (pinning V001 by path and sha) is in the scratchpad (`dev_tsr_in.json`, `3e795abe…`). The record holds no builder sha, so the builder's own V002 constant is not circular. `ROOT_TSR_FLAG_RECORD_V002.json` is not named c2v003; the name follows the commission.
- **Ported fixtures.** The 96 c2v002 cases keep their ids, expectations and observed codes (checked against the c2v002 record). Their fixtures moved to the c2v003 inputs: every receipt carries the binding keys; `receipt_keys` has nine roles; the launch registry is generated per input from the call list (content-addressed, so B04's two builds stay byte-equal); each FULL input gets its own ledger root; `ev()` no longer sets a fixed spec. Cases whose c2v002 object no longer exists test the same property on its successor: M01–M09 read `GATE_STATUS_REPORT.json`, M08 edits A's list, T01/T05/T08/T09 use V002, T04 makes the bound inclusive in the rule text (V002 has no support block), and the unsealed TSR variant is V002 in other bytes.
- **The record runs' work directories** hold, by design, the forged ledger entries (K07, K09), one symlink (O1b), and two ledger directories renamed in place (K12, K16; nothing was deleted).
- **V006 moved during this build:** `f1c5f657` (start, through A153), `3af07346` (A154), `73663c84` (A155). Read: A135–A141 (L530-689), A148 L934-956, A149 L975-987, A154 L1120-1146, the heading list, and greps for "launch registry", "registry", C4V001, "θ key" and "spec sha"; A155 by a keyword grep only (it concerns the NGC LO tolerance). None pins a gate document, holds a seal entry or defines a launch registry.
- **Classifier A.** Only `README_CLASSIFIER_A_C4V001.md` (`4e1e7493`) was opened. The implementation, its suite and its case files were not; OI-A1 is open for that reason.
- **Opened** (named or explicitly cited files only): the c2v002 README, RUNBOOK, builder, tests, HASHES_V002 and its test record; `ROOT_TSR_FLAG_RECORD_V001.json`; classifier A's README; V006 (as above). The tests (and `tsr-check` in development) read the compare, N1 and node records V001 pins, from bytes.
- **Not opened.** The slots, the program query manifest, r3a, ROOT_ITEMS_R3A, the R3A rulings, A133 (shas carried from c2v002's record), `step5_path_c2` and its STEP5_REGISTRY (`38a75614`; the launch-registry schema here is a proposal, not that object's), `classifier_a_c4v001.py` and A's suite, anything under `v003g/slots`, `runs` or `independent235`, run trees, External1, ~/.codex, `c5h_hull_c2/` and `UVT_*`.
