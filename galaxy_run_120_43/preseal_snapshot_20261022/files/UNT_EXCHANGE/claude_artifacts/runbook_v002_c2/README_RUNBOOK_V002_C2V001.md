date -u: Mon Oct 19 16:20:30 UTC 2026

# runbook_v002_c2: RUNBOOK_V002, the roster builder and the root TSR flag record (root workflow build; not adopted)

**What this is.** These are the A142 build-table items "TSR flag record (M-7), root" and "RUNBOOK_V002 and roster builder (A133), root workflow, Claude4 review". Nothing here is adopted until root pins it and Claude4 reviews it. Nothing authorizes a launch or target access. No production run was made.

## Files

| file | sha256 | what it is |
|---|---|---|
| `ROOT_TSR_FLAG_RECORD_V001.json` | `61bd8a83492e96ffb22d576a93b65d14c047f92e3be4bbfc2c0120f439cf7edc` | M-7 (i) flag record. Contents: ring 15 verbatim from the compare; the dependence rule with its end forms; bounds 9.901810628740723 and 10.911721936765339, both exclusive; `flagged_query_ids` [NGC3198-Q25]; the 43-row flag table; and pins from bytes to `6f095f64`, `8867c376` and `ec1dcca5`. The support-record pin is PENDING (G7). Target-free; no key contains "target". |
| `roster_builder_c2v001.py` | `a19ed0eec3fb4b81ded569f4488a8ef87e089e35af6bcc5eb2c1952002c80d72` | Commands: `build` (PLAN, MEMBERS and FULL rosters; the M-15 gate-status list; the replay plan), `pass-record`, `step7` (rule (b)), `sens-budget`, `check-gate-list` (GATE_STATUS_LIST_DEFECT), `seal-check` (SEAL_SHA_MISMATCH) and `tsr-check` (TSR_FLAG_TABLE_MISMATCH). |
| `RUNBOOK_V002.md` | `ef4967ff1c04d4aa911f836b145585f88afd03c1ce37c70e6f5803844fb5c4b8` | The per-phase runbook. It keeps V001 step numbers, so no step map is needed. |
| `test_runbook_v002_c2v001.py` | `845f18691fc9d14ce69204af27e3834dd6d78cd0555cc4c3d9e25da02fd355d7` | The synthetic MUST_PASS / MUST_FAIL suite. |
| `test_records/RUN1/TEST_RECORD.json`, `test_records/RUN2/TEST_RECORD.json` | `5430735145ce7132e53cb17343477faec666052a1e1030f5158c1b83f31b3e4d` (both; byte-identical) | Two record runs: 55/55 each (22 MUST_PASS, 33 MUST_FAIL); `results_sha256` `e454d907da2e735ed90df47c0baa073a1d88a017085f158bb191cd827fe782ae`. |
| `test_records/RUN*/work/` | not hashed | The synthetic fixtures each run wrote. |
| `HASHES.txt` | — | sha256 of every file above. |

## Running it (`python3 -I -B`; every input is a JSON document pinned by sha256)

```
python3 -I -B roster_builder_c2v001.py build      --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v001.py step7      --input IN.json --input-sha256 HEX --out-dir NEW_DIR
python3 -I -B roster_builder_c2v001.py tsr-check  --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B roster_builder_c2v001.py seal-check --input IN.json --input-sha256 HEX --out NEW_FILE
python3 -I -B test_runbook_v002_c2v001.py --record-dir NEW_DIR
```

- **Exit codes:** 0 means built or passed; 2 means refused (an input defect); 3 means a pre-target stop; 1 means an internal error.
- **Input schemas:** these are listed in the builder (`STAGE_KEYS`, and `_keys` in each command).
- **Production builds:** a production `build` executes the pinned freeze module from verified bytes. Its self-check therefore reads the real slots, nodes and query manifest. Only root runs it.
- **The suite never runs a production build.** It patches the module's slots and node constants to synthetic fixtures, and a read guard refuses any path outside its work directory except the TSR record and the three files that record pins.

## Results

- **TESTED.** 55/55 in each of two record runs, with byte-identical records. The cases:
  - **Builder:** B01–B24, 24 cases.
  - **M-15:** M01–M10, 10 cases.
  - **Phase 2, step 7 and M-14:** P01–P09, 9 cases.
  - **M-6:** S01–S04, 4 cases.
  - **M-7:** T01–T08, 8 cases.
- **End-to-end cases** run the real v003g functions on synthetic inputs: `evaluate_envelopes`, `select_reference_member`, `evaluate_sensitivity`, `_load_row_roster`, `_row_contract`, `_root_frozen_rows` and `_incomplete_reasons`.
- **The cases the task named:**
  - unpinned gate document: B05;
  - missing cut record: B06, B07;
  - gate pinned after the launch receipt reads LATE: M02, M03;
  - a discrepancy makes the member UNEVALUATED and is not resolved: P02, P03, P09;
  - seal sha mismatch: S02–S04;
  - TSR record tampered: T03–T07.
- **The production TSR flag record passes `tsr-check` against the real compare, N1 and node bytes** (T01, T08).
- **UNTESTED.** Production builds, real receipts, cut records and results (G8, G9, G10), the M-14 successor, `write_freeze_manifest` itself, and scoring.

## CHOICES this build made that the text did not force (root confirms or replaces each)

- **C1. TSR flag record schema.**
  - The schema is `UNT_ROOT_TSR_FLAG_RECORD_C2V001`, with `rule_id` `M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001`.
  - It carries both `flags` (43 rows) and `flagged_query_ids`, which reconciles M-7's id list with M-5's "43 flags" (G6).
  - No key contains "target"; target-freedom is stated in a value. This lets the record pass v003g-style key screens.
- **C2. Source of the flag table.** The flag table comes from the governing r3a §1.4 id list. It was cross-checked from bytes only on the three radii r3a quotes (Q24, Q25 and Q26), in both kpc and metres. The query manifest and the slots were not opened.
- **C3. Rule (b) in Phase 1.** It applies in Phase 1 as well. A133 states it for Phase 2, and RUNBOOK_V001 L21 left Phase 1 to a root successor.
- **C4. "That member" (G2).**
  - It is each member whose validity record differs between pass one and pass k: evaluated, forward_valid_flag, member_valid, row_valid, the row reasons, or the served result pin.
  - A D1 or sensitivity-plan difference without a member discrepancy is STOP_NOT_MECHANIZED, a root ruling.
  - When the D1 member is made UNEVALUATED, D1 is allowed to move. The sensitivity budget then covers only the leading new-plan entries that have saved calls, and no launch is made.
- **C5. How UNEVALUATED is encoded.** UNEVALUATED is encoded as the v003g budget prefix. Every later call of the same list reads UNEVALUATED_BY_ORDER_TRUNCATION. The alternative, an adapter refusal, would give MEMBER_INVALID with status COMPLETE, which A133 (b) and (f) do not describe.
- **C6. Re-binding.** "Roster inputs" in the A133 re-binding rule means the call's own cut record (G14).
- **C7. Gates in rosters.** Every admissible gate goes into the `root_gates` of all six rosters, sorted by sha256. A gate document has no alternative field. A gate authorizes and never requires.
- **C8. What counts as "pinned".** A gate is pinned only by a full 64-hex sha occurring in V006 bytes. Its pinning entry is the first `## ` heading whose section contains that sha.
- **C9. M-15 timing.**
  - A pre-launch record in the same second as the earliest launch receipt counts as preceding.
  - Status is decided by the sha in the logged V006 bytes plus the timing. The record's own list is checked for consistency and reported per gate.
- **C10. M-15 record format.**
  - The pre-launch record schema is `M15_PRE_LAUNCH_RECORD_C2V001`, written with a byte copy of V006 at the logged sha (G15).
  - With no record, every gate reads LATE.
- **C11. Gate cutoffs.** The Phase-1 cutoff is the V006 bytes at the Phase-1 step-4 start (G24). The Phase-2 cutoff is the V006 copy logged by the Phase-1 score entry.
- **C12. Terminal classes.**
  - Classes come from a root-written raw-status map: FINISHED, FAILED, CAP, INFRA or PLANNED_STOP.
  - A FAILED or CAP terminal needs two consecutive attempts with the identical raw status.
  - PLANNED_STOP is admitted only for non-roster calls such as the twin.
  - Receipt time is ISO-8601 Z or `date -u` output, read under one named key.
- **C13. Call ownership.** The result and the cut record must lie inside the terminal attempt's run directory. Borrowing is detected by realpath (G10).
- **C14. Exact thetas.** Thetas are taken from value-free budget-0 v003g outputs (the PLAN stage), never recomputed. Every value must be a JSON float.
- **C15. Phase-1 build order.** Phase 1 builds FULL directly, with no MEMBERS stage, and executes steps 3 → 4 → 2.
- **C16. Value-free saving.** Pass one stays in memory; only the validity-only PASS record is written. The sensitivity plan is saved with `per_query` and `per_target` emptied.
- **C17. Phase-1 step-4 call set.** It is the members, the F points and the twin's planned stop (G13).
- **C18. Seal check.**
  - Required roles: PREREG_TEXT, CLASSIFIER and TSR_FLAG_RECORD.
  - The seal entry is the first `## ` heading carrying the text's full sha.
  - Every listed sha must appear in that section.
- **C19. Builder self-check.** A self-check through the pinned v003g is mandatory: `_load_row_roster` on every roster and `_row_contract` on every evaluated theta. Only then is a build BUILT.
- **C20. Step numbering.** V001 step numbers are kept and only sub-steps are added, so no step map is needed. Phase 2 uses `allow_incomplete=True`, a proposal that needs root ruling G3. The builder and this runbook are pinned before Phase-1 step 4, a proposal under G1.

## Gaps

Root rulings needed (detail in RUNBOOK §7): G1, G2 residual, G3, G7, G8, G9, G10, G13, G14, G15, G16, G17, G18, G19, G20, G21, G24.

## Deviations (disclosed)

- **Drafts in the scratchpad.** Development drafts of the builder, the tests, the runbook and the TSR generator were written and iterated in the session scratchpad (`/private/tmp/claude-501/.../scratchpad/rb/`), outside this folder. Each final file here was then written once, by exclusive create, from those bytes. No file in this folder was edited after it was created.
- **Development test runs.** These ran in the scratchpad, with their own work directories.
- **V006 moved twice while this build ran.** It was hashed at `92ab3b4a` (read through A145), then at `185486dc` (A146 headings, and the A146 section read). Neither version pins a gate document or holds a seal entry.
- **Freeze module execution.** The tests execute the pinned freeze module in-process, from its verified bytes, with no bytecode written. Its slots and node constants are patched to synthetic fixtures.
- **Read-only access to target-free records.** The tests read the real compare, N1 and node records and the root TSR record, read-only.
- **Opened in this build.** Only named or explicitly cited files were opened:
  - RUNBOOK_V001;
  - the v003g module (line ranges);
  - A133;
  - V006;
  - the R3A rulings;
  - ROOT_ITEMS_R3A (sc3);
  - PREREG r3a (sc3);
  - the compare, N1 and node records (in memory);
  - the extractor (L140-240);
  - 0545 and 0548, hashed only.
  
  A non-recursive `ls` of `freeze_score_readiness_cx3/v003g/` listed names only.
- **Not opened.** The slots, the program query manifest, the route-B config, the GL source files, anything under `v003g/slots`, `runs` or `independent235`, UNT_INTERNAL_RUNS, External1, ~/.codex, `c5h_hull_c2/` and `UVT_*`.
