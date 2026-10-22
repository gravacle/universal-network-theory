date -u: Mon Oct 19 17:18:28 UTC 2026

# runbook_v002_c2, build c2v002: RUNBOOK_V002 and the roster builder, with the verifiers' blocking findings fixed (root workflow build; not adopted)

**What this is.** The second build of the A142 build-table item "RUNBOOK_V002 and roster builder (A133), root workflow, Claude4 review". It fixes every blocking finding the verifiers raised against the first build (c2v001). Nothing here is adopted until root pins it and Claude4 reviews it. Nothing authorizes a launch or target access. No production run was made. The c2v001 files in this folder are unchanged and are superseded by these; root pins only the c2v002 files.

## Files

| file | sha256 | what it is |
|---|---|---|
| `roster_builder_c2v002.py` | `301765881dc61ffbdc17ec65c468cc1e6d4fdf18c34dde8b244605981b55f8f9` | Commands: `build`, `pass` (new: the in-memory pass driver), `step7` (now with the build record and the STEP7_LEDGER), `sens-budget`, `check-gate-list`, `seal-check` (now with the role-line format and the freeze manifest) and `tsr-check` (now with the flag-record pin). c2v001's `pass-record` is removed. |
| `RUNBOOK_V002_C2V002.md` | `1e907dbdb3d67e5af0465a39d22fdb87d88e206a29a1107cf40dff83ed517b3d` | The per-phase runbook. It keeps V001 step numbers, so no step map is needed. |
| `test_runbook_v002_c2v002.py` | `8e0f57c77d77356bf016961b8a0ecafd7dbaf84e4fd5e51ae73068937d9edf3c` | The synthetic MUST_PASS / MUST_FAIL suite. |
| `test_records_v002/RUN1/TEST_RECORD.json`, `test_records_v002/RUN2/TEST_RECORD.json` | `13d3fb5d371492220ef3a0864437227ceebe9e44059adb4c1fa5b73fbd3c876b` (both; byte-identical) | Two record runs: 96/96 each (26 MUST_PASS, 70 MUST_FAIL); `results_sha256` `75df36e56e6d7f31c1e40a3ea3d93cb3b7645be381e640867db9672546b2920a`. |
| `test_records_v002/RUN*/work/` | not hashed | The synthetic fixtures each run wrote (including each test's STEP7_LEDGER and forged ledger entries). |
| `ROOT_TSR_FLAG_RECORD_V001.json` | `61bd8a83492e96ffb22d576a93b65d14c047f92e3be4bbfc2c0120f439cf7edc` | Unchanged from c2v001 (no finding against it); c2v002 pins it as a builder constant. |
| `HASHES_V002.txt` | — | sha256 of every file above, from bytes. |

## Running it (`python3 -I -B`; every input is a JSON document pinned by sha256)

```
python3 -I -B roster_builder_c2v002.py build       --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v002.py pass        --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v002.py step7       --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v002.py tsr-check   --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B roster_builder_c2v002.py seal-check  --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B test_runbook_v002_c2v002.py --record-dir NEW_DIR
```

- **Exit codes:** 0 means built or passed; 2 means refused (an input defect); 3 means a pre-target stop or a STOP_NOT_MECHANIZED step 7; 1 means an internal error.
- **Input schemas:** `STAGE_KEYS` (build), `PASS_INPUT_KEYS` (pass), and `_keys` in each command.
- **Production builds and passes** execute the pinned freeze module from verified bytes, so they read the real slots, nodes and query manifest. Only root runs them.
- **The suite never runs a production build or pass.** It patches the module's slots and node constants to synthetic fixtures, and a read guard refuses any path outside its work directory except the TSR record and the three files that record pins. Commands that load the freeze module run in-process under that guard.

## The verifiers' findings and what fixed each

| finding | fix | tests |
|---|---|---|
| **Rule (c) restated incompletely** (RUNBOOK L45, §4 row (c); RULE_TEXT['c']); `_terminal` accepted two equal raw statuses with no solo or cap evidence | Full A133 §3 (c) text (and A141 L1) in RUNBOOK §1 and §4 and in `RULE_TEXT['c']`. `_terminal` now needs a rule-(c) pair proven by receipt evidence: identical raw status, identical spec, `other_ngc_processes_max` 0 on both counted attempts, rerun RSS cap = host RAM, rerun wall cap = 2 × the first attempt's, OUTPUT_CAP cap raised. The evidence keys and the four readings are named as root gap **G25** | C01 (the verifier's probe: two FAILED_SOLVER 1 s apart, no evidence, now refused), C02–C08, B15, B20, B21 |
| **Validity-only rule had no compliant delivered path**; `pass-record` read full v003g outputs from pinned files | `pass-record` removed. New `pass`: the in-memory driver (envelopes, reference, sensitivity in memory under the replay adapter) writes only the validity-only `PASS_RECORD.json` and, for Phase-2 pass one, a whitelisted value-free sensitivity plan. The saved-plan check is now a whitelist. The driver is in RUNBOOK §8 UNTESTED until it runs on real inputs | V01, V02 (byte scans of every written file), V03 (`pass-record` gone), V04–V07, B03, B20, B21, P01, P02, P05 |
| **B1: step 7 not tied to the plan's budgets or the registered plan** (A3a–A3e) | (1) Each pass's per-alternative budget, the evaluated-member prefix and the sensitivity budget (the plan's, or re-derived for a Phase-2 successor) must match. (2) `step7` takes the BUILD_RECORD pin; the plan must be its REPLAY_PLAN.json or a successor verified through the append-only `STEP7_LEDGER`, every entry of which is re-derived from stored pass copies and must change only what step 7 changes. (3) The ledger records every result; a plan with a NEW_UNEVALUATED successor is refused by `step7` and by `pass`. Each pass record names its replay plan and build record; pass one is bound to the pass-one plan of record (Phase 2: through the new FULL input `members_stage_build_record`) | K01 (A3a), K02 (A3e), K03 (A3b), K04 (A3c), K05 (A3d), K06, K07, K08, K09, P02 |
| **B2: rule (c) met by one failure** (O1a, O1b, O5, O6) | Refuse a repeated run directory (by realpath), nested run directories, a repeated receipt (realpath or sha), receipt times that do not strictly increase, and any attempt after a FINISHED/PLANNED_STOP attempt or a rule-(c) pair | O1a, O1b, O1c, O2, O5, O6, O7, O8 |
| **B3: M-6 and M-7 did not bind sealed shas to roles or the freeze** (A4c, A4d, A4e, A5g) | `seal-check`: distinct objects per role; the seal entry (format proposed under G17) has one `- ROLE: \`sha\`` line per role and the sealed sha is the one on that line; entry roles = supplied roles; it takes the freeze manifest and requires the sealed TSR flag record in `input_files`, and requires it to be `61bd8a83`. `tsr-check`: `61bd8a83` added to `PRODUCTION_TSR` | S05 (A4c), S06 (A4d), S07 (A4e), S08 and T09 (A5g), S09–S12, S01–S04 |

**Mutation check (development, scratchpad).** 13 mutants, each removing one of these fixes from a copy of the builder; all 13 were killed by the suite. Not a record run.

## CHOICES this build made that the text did not force (root confirms or replaces each)

C1–C11, C13–C15, C17, C19 and C20 are carried from c2v001 unchanged (see `README_RUNBOOK_V002_C2V001.md`). C12, C16 and C18 are replaced by C21, C24 and C27.

- **C21. Rule (c) mechanization** (replaces C12).
  - Receipt evidence lives in the receipts, under eight key roles root names per producer (G25). It is needed only to make a call FAILED, CAP or OUTPUT_CAP terminal; a FINISHED terminal needs none.
  - Readings: "with no other NGC process running" applies to both counted failures; "RSS cap at RAM" is equality with the receipt's host RAM; "wall cap doubled" is exactly twice the call's first attempt; "identical deterministic failures" is the identical raw status in consecutive attempts.
  - OUTPUT_CAP is a sixth class (A141 L1): it disposes as UNEVALUATED_CAP and its rerun must raise the output cap above the first attempt's. A twin cap stop maps to PLANNED_STOP (A141 L4).
- **C22. Attempt distinctness.** Run directories distinct by realpath and disjoint (not nested); receipts distinct by realpath and by sha256; receipt times strictly increasing; nothing after a terminal attempt or a rule-(c) pair.
- **C23. The pass driver.** Inputs: the BUILD_RECORD, the replay plan, `ROSTER_PINS.json`, the build record's freeze-module pin, the saved `select_representative_points` output (with its `points`), the spec and the `null_direction_rule` inline. Query ids come from the PRIMARY roster's query manifest through v003g. Budgets come only from the plan. A registered result that no longer verifies refuses the whole pass (`PASS_RESULT_CUSTODY_BREACH`), not a member mark. Internal errors of `pass` print the exception type only.
- **C24. Value-free plan whitelist** (replaces C16). Exactly the v003g budget-0 keys; `per_query` and `per_target` empty; every value array null.
- **C25. The step-7 ledger.** It sits at `<build dir>/STEP7_LEDGER/` (derived from the BUILD_RECORD's path, never an input). It holds `STEP7_<seq>.json` hash-chained results, `PASS_<sha>.json` copies and `PLAN_<sha>.json` successors, all by exclusive create. Every read re-derives every result. A repeated comparison of a plan that has not been superseded is allowed and recorded (a later NEW_UNEVALUATED is never hidden); only NEW_UNEVALUATED supersedes. Deleting the ledger's last entry is not detectable by the tool, so root logs the head sha in the freeze entry.
- **C26. Pass-one binding.** Phase 1: the build's own (chain-root) plan. Phase 2: the MEMBERS plan, bound through the FULL input `members_stage_build_record` (same builder, rosters equal to `members_stage_rosters`).
- **C27. Seal check** (replaces C18). The seal-entry format proposed under G17 (RUNBOOK §6): a `## ` heading carrying `SEAL_ENTRY` and the text sha, then `- ROLE: \`sha\`` lines. Distinct objects; entry roles equal supplied roles; the PREREG_TEXT line equals the heading sha; the freeze manifest is a required input.
- **C28. TSR pin.** `61bd8a83` is a builder constant in both `tsr-check` and `seal-check`. A successor flag record (for instance after G7) needs a successor builder.
- **C29. Freeze in process (G26).** The step-8 freeze consumes the in-memory outputs of a final pass whose record must equal the ledger head's pass k byte for byte. The script is not built here.

## Gaps

Root rulings needed (detail in RUNBOOK §7): G1, G2 residual, G3, G7, G8, G9, G10, G13, G14, G15, G16, G17, G18, G19, G20, G21, G24, and new **G25** (rule-(c) receipt evidence keys and the four readings) and **G26** (the freeze script). Until G25 is ruled and the receipts carry the keys, a failed step-5 call cannot be made terminal; it stays non-terminal and is rerun.

## UNTESTED (deciding tests in RUNBOOK §8)

The `pass` driver on real inputs (the Phase-1 pass one on the S0 results); production builds; real receipts with the G25 keys; real cut records; the ledger in production; the freeze script and `write_freeze_manifest`; the M-14 successor; scoring.

## Deviations (disclosed)

- **Drafts in the scratchpad.** The builder, tests, runbook and README were drafted and iterated in the session scratchpad (`/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/rbv002c2/`), outside this folder; the mutation runs also ran there (`rbv002c2_mut*`). Each final file here was then written once, by exclusive create, from those bytes. No existing file in this folder was edited.
- **The test records' work directories** contain files the tests write by design: each FULL build's `STEP7_LEDGER`, two forged ledger entries (K07, K09) and one symlink (O1b), all inside `test_records_v002/RUN*/work/`.
- **V006 moved during this build.** Hashed at `08d67ad8` (A149, start), then at `9bcb3150` (A151, before the runbook was written). A147–A151 were read; none pins a gate document or holds a seal entry. A150 adds a precondition the runbook now cites at step 8 (the S1 reading gates Phase-1 reads; S1-B gates Phase-2 step-5 reads when u_A is AT_ANCHOR).
- **Freeze module execution.** The tests execute the pinned freeze module in-process, from verified bytes, with no bytecode written, its slots and node constants patched to synthetic fixtures. P02 and the K cases use a second module instance with `_member_contract_valid` patched to make M001 invalid in one pass (a stand-in for a validity outcome differing between passes; no fixture file is edited).
- **Read-only access to target-free records.** The tests read the real TSR flag record and the compare, N1 and node records it pins.
- **Opened in this build** (named or explicitly cited files only): the c2v001 README, RUNBOOK_V002.md, HASHES.txt, builder and tests; ROOT_TSR_FLAG_RECORD_V001.json; A133 (`cd92ef91`, L150-234 and a grep); V006 (greps, A141 L663-692, A147–A151 L899-1045); v003g (`48a1e48a`; L317-336, L532-545, L600-618, L1245-1262, L1656-1675, L2040-2479 and a list of its definitions).
- **Not opened.** The slots, the program query manifest, r3a, ROOT_ITEMS_R3A, the R3A rulings (their shas are carried from c2v001's record), the route-B config, the GL source files, anything under `v003g/slots`, `runs` or `independent235`, UNT_INTERNAL_RUNS, External1, ~/.codex, `c5h_hull_c2/` and `UVT_*`.
