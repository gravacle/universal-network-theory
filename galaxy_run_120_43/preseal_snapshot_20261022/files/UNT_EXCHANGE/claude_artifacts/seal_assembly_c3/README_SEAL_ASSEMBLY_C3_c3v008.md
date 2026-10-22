# README c3v008: the seal pre-stage tuple with root's manual disclosures inside the SEAL_RECORD (A110, A111) (Claude3)

Written 2026-10-19T01:50:15Z (`date -u`). This supersedes `README_SEAL_ASSEMBLY_C3_c3v007.md` (`dec02585`) for everything A110 and A111 change; c3v007 stays the reference for the v003 wiring and R-01 to R-07. The selection of record is `SELECTED_SEAL_PRESTAGE_C3SA_c3v008.json`.

**Step 0 refuses until tool 4 v004 is wired (P13, PENDING) and root gives P2 and P5–P10.**

## The tuple

| role | file | sha256 |
|---|---|---|
| script | `ROOT_SEAL_STEPS_c3v019.sh` | f4843a47dadf4fc98aca287d0f9b982e10a5f90e6f73de1f158123440b686e67 |
| helper | `tools/seal_steps_c3sa_c3v017.py` | 3c642d1a8be8bdac12d3472add602065c6d86cc47c7f3d96c297f534056a047b |
| runner / fence (unchanged) | `tools/run_pinned_c3sa_c3v003.py` / `tools/fence_c3sa_c3v003.py` | 2b040e94… / 9c62ad49… |
| slot draft (NEW: P3 and P4 ruled) | `SLOT_VALUES_DRAFT_c3v003.json` | e12292a27e58aacdebfde5dfc4d1a3f7ccb0c5b3ca4b756ef2a6d8468a5311c5 |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9… |
| root's disclosures file (a pinned input; root wrote it) | `root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json` | b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6 |

The watchdog `step2_disk_watch.sh` (`bd0d9bab…`) is unchanged and stays outside the hash chain.

## A110: the disclosures go inside the SEAL_RECORD; the separate-packet substitute is gone
**Step 0 runs the new helper subcommand `check-disclosures` on the pinned file.** The script fixes the file as the constant `DISCLOSURES`; it is not a root input. The check:
- **Reads the file once and parses it strictly,** with the c3v013 SELECTED-strictness rules. Each failure has a typed `DISCLOSURES_*` code: invalid UTF-8, BOM, depth over 64, duplicate key, NaN/Infinity/overflow, an integer over 4300 digits, trailing text, a non-object top level.
- **Requires exactly these keys:** `{schema, e_r6_1_text, c08_table, c08_confirmation, root_disclosures}`, with `schema` = `SEAL_MANUAL_DISCLOSURES_V001`.
- **Requires `e_r6_1_text` to be non-empty and equal to `SELECTED_R6_C4V001`'s `basis.erratum_E_R6_1`, byte for byte.** The comparison is on the decoded text: a JSON `\u` escape of the same character passes (control H-4f).
- **Checks the `c08_table` rows:** each is exactly `{new_item_id: NEW-<n>, file, line: int > 0, declared_in_r13: bool}`, and the ids are unique.
  - Root's rows carry `declared_in_r13`, which 0646's `{new_item_id, file, line}` does not list.
  - The check follows root's file, as 0647 tells Claude4 to.
- **Requires `c08_confirmation` to be non-empty.**
- **Checks `root_disclosures`:** each entry is exactly `{id, source, text}`, all non-empty, and the ids are unique.

**Not checked here:**
- the content against r6, A100, A101 and A105 (the coordinator is doing that);
- the `c08_table` line numbers against r13 (0647 assigns that to Codex1).

**Step 10** passes `--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"` to tool 4 v004, and pins the file again.

**What root does now:**
- **C-08:** root's manual check is done; it is recorded in the file's `c08_table` and `c08_confirmation`.
- **E_R6_1:** it is the file's `e_r6_1_text`.
- **Nothing about either is published separately.** The summary's `root_next` says so. It pins `manual_disclosures` instead of quoting E_R6_1, and the old E_R6_1 and C-08 manual-statement items are gone.
- **The C-08 instructions in README c3v006 are historical.**

## P13 (NEW, PENDING): tool 4 v004
- **Pins:** `V004_SELECTED`, `V004_SELECTED_SHA`, `V004_SELECTED_SCHEMA`, `T4` and `T4_SHA` are `PENDING`, so step 0 refuses. MUST_FAIL S-5 runs the real form.
- **Tools 1, 2, 3, 5 and seal_common** stay v003, checked role-qualified against `SELECTED_SEAL_TOOLS_V003_C4V001` (7 roles). Tool 4's role is no longer read from that file. Step 0 checks it against the v004 SELECTED file, role `tool_4_build_seal_record`.
- **Status at 01:49Z:** `v007_final_prereg_c4/seal_tools_v004/` exists, holding copies of the v003 tools, `dev/`, `tests/` and `tools/`. It has **no SELECTED file**, so nothing is wired.
- **To wire v004 when Claude4's SELECTED file lands:**
  - set the five pins (and any other tool the file names), and check `T4_RUN`'s module names against v004's imports;
  - re-run the dry runs without S24 and S25;
  - add a check that the SEAL_RECORD carries the file verbatim, in the record format v004 defines.

## A111: P3 and P4 are ruled
- **P3:** the driver check record is the constant `DRIVER_CHECK_RECORD`, CHECK.md `89a6de88`. It feeds tool 5 and `check-driver-build-record` in step 2a; the RI-36 candidate list is gone.
- **P4:** `certificates.EPS_NGC` `1d5eef1b` and `certificates.I1T_NGC` `3ae7981a` are plain pins in `SLOT_VALUES_DRAFT_c3v003.json`. That draft has **no `PENDING_ROOT_RULING` marker**, and it differs from c3v002 in exactly these three sha values.
- **Step 3a** passes no `--ruling` and no `DRIVER_CHECK_RECORD` runtime pin; `fill-slots` pins the three records from bytes.
- **Inputs removed:** `UNT_SEAL_DRIVER_CHECK_RECORD_PATH` / `_SHA256` and `UNT_SEAL_RULING_EPS_NGC` / `_I1T_NGC`. Step 0 **refuses if any of them is still set** (S-6, S-7).
- **Step 0 checks that the draft pins exactly the ruled records** (S-8: the old draft c3v002; S-9: another EPS_NGC sha).
- **`REQUIRED_ACK` is unchanged** (RI-28..RI-37, GAP-12), although RI-36 and GAP-12 are now ruled.

## SA-C3-E1 (found and fixed this round): a check that did not stop the script
**The defect.** Under `set -e`, bash does **not** stop when a **non-final** operand of an `&&` list fails; only the last operand is enforced. I tested this on /bin/bash 3.2.57.

**Where it applied.** Nine checks in steps 0 and 3 of c3v016 (the c3v007 tuple) had the form `[ A ] && [ B ]` with no fallback, so their first operands were never enforced:
- the HELPER sha, the root of trust;
- the draft's driver, registry and BUILD paths;
- the launcher sha and path, and the guard path;
- the Z2 and Z2-OFF shas;
- the draft's documented output paths;
- the binder's plan and driver paths.

**The fix.** Each check now ends in `|| { echo "REFUSE: ..."; false; }`.

**Tested.** MUST_FAIL E1-1 to E1-4 refuse on c3v019. The same four inputs PASS step 0 on the c3v016 form (E1-1old to E1-4old), which reproduces the defect.

**Exposure.** No real input was affected: the dry runs fed the correct values. The risk was a wrong helper or draft passing silently.

## Intermediate versions (kept, never published)
- **`ROOT_SEAL_STEPS_c3v017.sh`** (`b6037eee`, never run) made the A110/A111 changes; c3v018 adds the E1 fix to it.
- **`ROOT_SEAL_STEPS_c3v018.sh`** (`32a023f0`) was used only by dry run `dry_run_20261019T013817Z`. That run passed steps 0–13 and stopped at the summary: an apostrophe in the new `root_next` text closed the summary's single-quoted python.
- **`ROOT_SEAL_STEPS_c3v019.sh`** rewords that text, and its generator compiles all six embedded python programs.
- **Generators:** `tools/make_root_script_c3v017.py`, `…c3v018.py` and `…c3v019.py`.

## Dry run of record: `dry_run_20261019T013957Z/INDEX_DRY_RUN_C3SA.md`
- **Both passes: ALL STEPS PASS.** Step 9 was STUBBED.
- **New substitutions:** S24 (v003 tool 4 and its SELECTED file stand in for P13) and S25 (step 10 drops `--manual-disclosures`).
  - So **this SEAL_RECORD does not yet carry the disclosures.**
  - Step 0's `check-disclosures` ran on root's real file and passed.
- **Slot values:** equal to dry run 10's apart from the scratch-path bound shas.

## Controls (helper c3v017 / script c3v019 / dry run 013957Z)

| suite | folder | result |
|---|---|---|
| **NEW: disclosures + script step 0 + SA-C3-E1** (H-0 to H-21; S-0 to S-9; E1-1 to E1-4 with c3v016 contrasts) | `mustfail_disclosures_20261019T014524Z/` (`252b6b23…`) | **60/60** |
| A + C-02 to C-06 + SELECTED roles + C03-S1 + C-04 | `mustfail_c0x_20261019T014708Z/` (`23afd966…`) | 85/85 |
| v003 (frozen copy, roles, tool-5 record, tool 4 admission) | `mustfail_v003_20261019T014708Z/` (`841aba60…`) | 16/16 |
| W7-S1 + RP-S1 | `mustfail_w7rps1_20261019T014708Z/` (`a399400d…`) | 41/41 |
| B1 + B3 | `mustfail_regress_20261019T014708Z/` (`309326d1…`) | ALL_OK |
| B2 + N1 | `mustfail_b2n1_20261019T014740Z/` (`798041d5…`) | ALL_OK |
| `tor_table_bytes` (script c3v019) | `tor_table_bytes_test_20261019T014741Z/` (`b03530d9…`) | ALL_OK |
| watchdog | `watchdog_test_20261019T014741Z/` (`24dd5f5a…`) | ALL PASS |

**The four cases the coordinator named,** all checked through the step-0 pre-check (both helper-level and the script's own step 0, since v004 is PENDING):
- a wrong sha: H-1 and S-1;
- a duplicate key: H-2, H-2b and S-2;
- an empty `e_r6_1_text`: H-3 and S-3;
- an `e_r6_1_text` one byte off: H-4a to H-4e and S-4.

## Left behind by this round (kept; nothing is deleted)
- **`dry_run_20261019T013817Z`** (script c3v018): stopped at the summary.
- **`tools/setup_dry_run_c3sa_c3v010.sh`** (`4dd7105a`): never run; it kept a no-op copy of the old sed. c3v011 replaces it.
- **`tools/mustfail_disclosures_c3sa_c3v001.py`** (`f24eb1ee`): never run; its H-4f construction replaced the character it meant to escape. c3v002 replaces it.

## PENDING
- **P13:** tool 4 v004 and Claude4's seal-tools SELECTED file (above).
- **Root inputs**, as listed in the script header:
  - P2: the compare, r13 `f5adfd11` plus its SELECTED;
  - P5: the dispositions object, `entries: []` for r6;
  - P6: the B7 inputs, in the C4V002 forms;
  - P7: CASCADE_MAP_R5_ADDENDUM, naming `a7281e10`;
  - P8: the C5H spelling;
  - P9: the ack;
  - P10: the floor.
- **P3 and P4 are done (A111).**
