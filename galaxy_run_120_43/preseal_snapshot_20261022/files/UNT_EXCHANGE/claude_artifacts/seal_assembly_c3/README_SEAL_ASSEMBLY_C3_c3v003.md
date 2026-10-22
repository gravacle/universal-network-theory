# README c3v003: the SELECTED seal pre-stage tuple after FROM_CODEX/0642 (A105) (Claude3)

Written 2026-10-18T23:00:47Z (`date -u`). This supersedes `README_SEAL_ASSEMBLY_C3_c3v002.md` (`904b5360`) for everything 0642 and the 0109 heads-up change; that file stays for history. The selection of record is `SELECTED_SEAL_PRESTAGE_C3SA_c3v003.json`. Codex1 delta-checks the tuple against the one it reviewed (script007 / helper009 / runner002; see "Differences").

## The selected tuple

| role | file | sha256 |
|---|---|---|
| script (root runs it) | `ROOT_SEAL_STEPS_c3v010.sh` | 2b9d02fa34b06c4c672c58617a9e93e5bacca26924405106e462d2af397cecef |
| per-step helper | `tools/seal_steps_c3sa_c3v011.py` | 7caad125be19160c6e431dcf6be8f038cb9bba172c95f1f8059ebcdd938a0aff |
| pinned-source runner (N1 closed) | `tools/run_pinned_c3sa_c3v003.py` | 2b040e94a2b74eae981485288471376b86be0784a0a50b59093312c4fd87bf73 |
| in-process fence (unchanged) | `tools/fence_c3sa_c3v003.py` | 9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863 |
| slot draft (unchanged) | `SLOT_VALUES_DRAFT.json` | c93691f5d1931beef8abb656ced3446c99d0adf286d4b5de0c709ecb570284ba |
| step-8 manifest draft (unchanged) | `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` | e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da |

**Listed separately: a convenience, NOT in the seal tuple or its hash chain.** `step2_disk_watch.sh` (`bd0d9bab0854627957781e1666c7f5eacd1e10cd03bfde0dd2efe2e27a5a2c28`) is the A105.3 disk watchdog. No seal file pins it, and it pins nothing.

Root runs `/bin/bash ROOT_SEAL_STEPS_c3v010.sh` after exporting the root inputs in its header. **Step 0 still refuses until seal tools v003 is pinned (P1).** That is kept on purpose.

## What 0642 (A105) adds

- **RP-S1 (A105.2): the step-2 output root.**
  - **Step 0** (check mode, writes nothing) refuses if `/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007` exists in any form: a directory, a file, or a symlink, dangling or not.
  - **Step 3**, before the binder, creates it with the helper's `output-root --mode create`:
    - every parent component passes the B1 no-follow walk;
    - a path component that is empty, `.` or `..` is refused lexically, before any walk or mkdir;
    - the one missing parent level is created. **`UNT_INTERNAL_RUNS` does not exist on disk today** (lstat, 22:4xZ), so it will be;
    - the root itself is created with `os.mkdir`, exclusively;
    - it is then opened `O_NOFOLLOW_ANY|O_DIRECTORY`, and its (st_dev, st_ino) must equal the walk's;
    - its realpath (fcntl `F_GETPATH` of that fd, the kernel's own path, so no link can be followed) must equal the literal;
    - its `st_dev` must equal /System/Volumes/Data's, and it must be empty.
  - **The record.** The device, realpath and free space go to `logs/STEP_03_OUTPUT_ROOT.json`, to a `RECORD` line on the terminal, and into the summary. The summary step re-verifies that the root is still the same empty directory.
  - **The dry run** points the root at a scratch path (S17/S18). **The real root was never created.**
- **W7-S1 (A105.1, A78 N2): the admission allowlist is BUILD_V007's table, exactly.**
  - Step 12's `make-config` parses the `## Supported runtime entry allowlist` section of BUILD_V007 (`94bc05a5`) strictly:
    - the heading occurs once;
    - there is one ```text fence, with only blank lines outside it;
    - every line in the fence is a full `<sha>  <path>` row;
    - there are exactly 15 rows, with no duplicate path or sha.
  - It builds `producer_allowlist` from those rows, in table order.
  - It checks the serialized bytes **before** the exclusive write, and the written file again after it. Then the new `check-config-allowlist` re-reads the written config from its bytes.
  - It refuses any count other than 15, any row not byte-equal in path and sha, a reordered row and a duplicated row (a duplicate JSON key refuses in the strict parser).
- **P11 (Claude4 0109 heads-up): one text-of-record pin.**
  - `PREREG_TOR` (path + sha) is the only prereg text pin, used by steps 0, 2, 4, 4a and 10.
  - The bytes its entry table was read from (`TABLE_BYTES`) are now **derived** in step 0 from the text of record's own `entries_after_A81.addendum_read`. For r5 these are the same values as before: `70a48f51`.
  - **So r5 → r6 is a one-line change**, provided r6 keeps r5's `seal_slots` keys and that `addendum_read` form; otherwise a step refuses (fail closed).
- **The disk watchdog (A105.3), outside the seal.**
  - Every ~60 s it runs `df -Pk /System/Volumes/Data` and writes one line to its own exclusive log at a path root chooses.
  - It refuses log paths in a run tree and the firmlink spelling.
  - It raises a macOS notification with the "Glass" sound while free space is **below 80 GiB (= 85.90 GB)**. That is the stricter reading of "80 GB", so the alert can only come earlier.
  - Start it with `nohup /bin/bash step2_disk_watch.sh --log /ABS/PATH/STEP2_DISK_WATCH_V007.log > /dev/null 2>&1 &`.
- **RP-S2's refusal is not implemented** (0642: print only). P10 is unchanged from the reviewed tuple: root's own `UNT_SEAL_MIN_FREE_GIB` floor still refuses below it. **Root may pass 0 for record-only.** Free space is always logged.

## PENDING (the script refuses in step 0 while P1-P10 are open)

| # | item | now |
|---|---|---|
| P1 | seal tools v003 (Claude4; v002 + D-05 + B8, widened by C-01) | NOT LANDED. T1-T4 are v001 placeholders; v001 tool 3 refuses r5 (`TEXT_OF_RECORD_NOT_R4`, pass A). A successor pins the v003 paths, shas and CLI. |
| P2 | compare reviewed source | A104: r13 `f5adfd11`, SELECTED_R13 `10acd098`. Root supplies it at invocation; r12, r11 and r10 are refused. |
| P3 | driver check record (RI-36) | CHECK.md `89a6de88` or R5_REVIEW_FINAL_V001.md `6758bd24` (PENDING_ROOT_RULING) |
| P4 | EPS_NGC, I1T_NGC (GAP-12) | single candidates `1d5eef1b` / `3ae7981a`; no sha-level ruling (PENDING_ROOT_RULING) |
| P5 | dispositions JSON (v003 object) | rows for **A102-A105** at the open V005 `18fd9a83`, plus any entry added before the freeze. Under 0640, A102 and A104 are `revised` with a prereg-revision pointer (Claude4 0109 F-01). |
| P6 | B7 inputs (GAP-17) | key-equivalence map, NEW-item list, successor-custody record |
| P7 | CASCADE_MAP_R5_ADDENDUM | required before the seal on r5 |
| P8 | C5H run dir spelling | string only until step 9 |
| P9 | ack string | RI-28..RI-37, GAP-12 |
| P10 | free-space floor (RUNBOOK_V008 L37) | root's integer; 0 = record only (A105.3 rules a watchdog, not a refusal) |
| **P11** | **text of record** | **text of record: r5 now; r6 expected (Claude4 0109).** One line (`PREREG_TOR`) changes. r6 may also change the slot draft if its `seal_slots` change. |

**Possible script-encoded checks pending root's ruling on 0109 §2 (NOT implemented).** Claude4 0109 option (b): root checks these by hand at assembly, or this script encodes them.

| gap | what Claude4 found | how the script could encode it |
|---|---|---|
| C-02 | while the text-of-record pin is PENDING, tool 3 accepts any file named as the text of record | partly covered already: the script passes only `PREREG_TOR`, pinned by sha. It could also refuse a `--text-of-record` equal to the sealed prereg. |
| C-03 | B6 provenance: the GATES_ONLY body is checked for form, not for having evaluated the slotted records | compare GATES_ONLY.json's evaluated records with the slot's identity_gate_records, by path and sha |
| C-04 | tool 3 never loads the registry through the compare's own `load_producer_registry` | run the sealed compare's loader in-process (fenced, from pinned bytes) and check every slot record against it |
| C-05 | any allowlisted source passes as the launcher or the guard (no exact-name check) | partly covered already: step 12 requires the exact LAUNCHER and GUARD paths and shas (A78 N2). The same check could be applied to the bound plan's launcher and guard. |
| C-06 | only the last line of the bound command is compared with the binder's output | compare the whole bound command file with the binder's two-line form, byte for byte |

## Evidence
- **Dry run of record:** `dry_run_20261018T225638Z/INDEX_DRY_RUN_C3SA.md`. Pass A: steps 0-4 PASS, then step 4a REFUSEs `TEXT_OF_RECORD_NOT_R4` (expected). Pass B: every step PASSes, step 9 STUBBED, fence 0, prefix empty.
- **MUST_FAIL, W7-S1 and RP-S1:** `mustfail_w7rps1_20261018T225606Z/MUSTFAIL_W7_RPS1_RESULTS_C3SA.json`, `a7aa9440…`. 41 cases, ALL_OK, target-metadata attempts 0 in every case.
  - **W7-S1 refused:** 17 rows (with the V006 writers 9fbdb0ca / 500f8b6a); V006's old 15 rows; a substring-matched (truncated) path; the binder row f3e4e2be (cited in BUILD outside the table); a reordered row; a duplicated row (duplicate key); a duplicated sha; 14 rows; the list form; an upper-case sha; a trailing space; a config pinning BUILD_V006; and four malformed BUILD sections.
  - **W7-S1 passed:** the exact table.
  - **RP-S1 refused:** the root existing as a directory, a file, a dangling symlink, a symlink to a real directory, or a protected-text link; a symlinked parent (nothing was created through it); a file as parent; a missing grandparent; the firmlink spelling; `..` and `.`; free space below a synthetic floor; a non-empty root at verify; a wrong inode; a protected name; an unknown mode; a bad floor.
  - **RP-S1 passed:** create with the parent absent, create with the parent present, check (writes nothing), verify, and **check mode on the real literal path (writes nothing; the real parent is still absent)**.
  - **Reproduction:** helper c3v010 created the parent before refusing a path ending in `..`. c3v011 refuses it lexically.
- **Regression, B1/B3 on helper c3v011:** `mustfail_regress_20261018T225625Z/MUSTFAIL_RESULTS_C3SA.json`, `d3c52ab5…`, ALL_OK. B1 is 8/8 with 0 target-metadata attempts. B3 is 17/17, now with A102-A105. B2 and N1 concern the runner and fence, which are unchanged; see `mustfail_20261018T221642Z/`.
- **Watchdog tests:** `watchdog_test_20261018T225843Z/WATCHDOG_TEST_RESULTS_C3SA.txt`, `4843b9fa…`, ALL PASS. They used only a simulated threshold or df stubs, with the notification stubbed and the AppleScript compiled but not run.
  - **UNTESTED:** a real notification with sound. Root can run `step2_disk_watch.sh --log ABS --test-notify` once.

## Retry note
If a run stops after step 3, the empty output root stays. **The script never deletes.** Before the next attempt, root removes it by hand with `rmdir`, which refuses a non-empty directory. Step 0 refuses while it exists.

## Superseded in this round (never selected; nothing was posted)
- `SELECTED_SEAL_PRESTAGE_C3SA_c3v002.json` (`32502ffc`) and `dry_run_20261018T222835Z/INDEX_DRY_RUN_C3SA.md` (`77b8a0ce`): both were written before 0642 arrived.
- `ROOT_SEAL_STEPS_c3v009.sh` (`ebef7377`) and helper `seal_steps_c3sa_c3v010.py` (`823c8aca`): used only by dry run `dry_run_20261018T225153Z`; superseded by the `..` fix.
- `tools/setup_dry_run_c3sa_c3v001.sh` (`5b0ae416`): its script name was fixed.

## Findings for other owners (unchanged)
- **F1:** compare r13's `load_pinned_module` (L694-L700) has the B2 pattern. It is mitigated here by `-X pycache_prefix=<empty>`.
- **F2:** Claude4's seal tools import their siblings through the import system. The pinned-source runner closes this here.

The full file list is in `HASHES_C3SA_c3v002.txt`.
