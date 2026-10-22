# s0_launch_kit_c2 C2V003A: launch-record parse wait (N1) and the twin's RSS cap (N4) (V006 A172)

**Stamp.** Mon Oct 19 20:36:11 UTC 2026 (`date -u`, taken right before this file was written).

**Who and what.** A Claude2 root-workflow lane built this for root (Claude2, UNT Galaxy Run 120/43). The spec of record is V006 A172, "S0 kit C2V003" ("Build S0 kit C2V003a with the N1 and N4 fixes"), read with A166, A170 and A171. It is a minimal-delta successor of C2V003 (HASHES `61a03d00`, kit `e58c8605`). Every C2V003 file the commission names was re-verified from bytes before the build.

- Nothing was launched. No real root_monitor, NGC driver, filler, dry harness or gate was run.
- No running process was signalled or inspected beyond a `ps` command-line listing (test row Z02, as in C2V003). That covers CP-1 pid 6974, the step-2 runs and every root_monitor.
- Nothing under /Volumes/External1 was opened.
- Every C2V001, C2V002 and C2V003 file is unchanged. TESTED: `HASHES.txt` (18 OK), `HASHES_V002.txt` (17 OK) and `HASHES_S0_KIT_C2V003.txt` (17 OK) re-verify after the build. Their FREEZE_EXPECTED_INPUTS_* lines (3 and 5) were skipped, not opened.
- None of this is adopted until root rules on it and Claude3 reviews C2V002 to C2V003A as one delta (A172).

**Labels.** TESTED: run here, result shown. FORMAL: read from the cited bytes. CHOICE: a decision this build made, which root may overrule.

## 1. Bottom line

- **N1 (TESTED).** `launch-check` now polls `<receipt>.launch.json` every 0.2 s until it parses as JSON, for at most 300 s, and only then decides.
  - A record that parses and differs from the plan is a MISLAUNCH at once (P05).
  - A record still unparseable at the bound is a MISLAUNCH (P04, and P07 end to end at the real 300 s bound).
  - A complete honest record is CONFIRMED as before (P03, P08, L11).
  - An empty or partial record completed within the bound reads LAUNCH, for the serial (P01) and the twin (P02).
  - Both scripts get the wait through the kit's `launch-check`, which both call.
- **N4 (FORMAL and TESTED).** The twin's process tree holds at most **11** processes, so its RSS cap is **RAM x 11 = 1,511,828,488,192 B** (`sysctl hw.memsize` = 137,438,953,472, TESTED). Serial caps stay RAM. `validate`, the plan, `monitor-argv` and `launch-check` enforce this (C01-C08).
- **Tests (TESTED): 28/28 MUST_PASS and 84/84 MUST_FAIL, plus 3 OBSERVED, in each of two record runs.** That is 115 rows: the 98 C2V003 rows that do not open a FREEZE file, plus 17 new rows. F01-F04 are not ported (section 7, R3).
- **Root must rule on three items (section 7):** the serial tree is up to 3 processes, not one; a MISLAUNCH for an unparseable record cannot be stopped by the kit; F01-F04 are not ported. One build error is disclosed in section 8 (E1, an empty DIFF file).

## 2. N4: the twin's process tree, from bytes (FORMAL)

root_monitor (`root_monitor_c2v001.py` `ba031c23`, path from the kit's pins) starts the driver in its own session (L147) and samples `tree_rss_bytes(proc.pid)` (L154). That function takes one `ps -A -o pid=,ppid=,rss=` snapshot and sums RSS over the driver pid and every descendant (L47-74). Each process's RSS counts once, so shared pages count once per process.

| Process | Count | Bytes (sha256 prefix, lines) |
|---|---|---|
| driver | 1 | Driver `577f8c94` is the tree root. Its only process start is `run_stages` (L1825-1865): one child `PY -I -B <driver> _stage request.json` per stage request (Popen L1847). The child runs the stage script in-process (`stage_main` L791-814; the scoped clone L6578-6600). |
| route-A stage process | 1 | Route A runs alone: `ctx.run_stages([req], [d])` (L8643; unscoped L5588). See the note below the table for which script it runs. |
| column workers | 8 | The parallel solver `7667025b` starts `n = max(1, min(requested, column_count))` workers (L872), so at most 8. It uses `multiprocessing.get_context('spawn')` (L888) and one `ctx.Process` per worker (L892-897). There is one pool per `solve()`, closed before `solve()` returns (L94-98). The worker side (`_worker_main`) starts nothing. |
| multiprocessing resource tracker | 1 | In the runtime Python 3.12.14, `popen_spawn_posix.py` `97b5d25a` `_launch` calls `resource_tracker.getfd()` (L38-40). `resource_tracker.py` `f9d73a81` `ensure_running` (L113-115, L117-185) then starts one tracker with `spawnv_passfds` (L173), as a child of the stage process. The spawned workers reuse it (`spawn.py` `ebf9fa40` L118-119). |
| **Total** | **11** | |

**Which script the route-A stage runs (FORMAL).**
- The twin template `1aa66269` sets `numerics.route_a.column_workers` 8 (L21-23) and has no `coefficient_alternative`, so the stage-0 alternative is off (driver L6147-6148).
- The stage script is therefore `V011_PINS['worker_parallel']` `293a417f` (driver L4992; swapped in by `_ngc_v011_context` L5117-5131; chosen at L8635-8637).
- It runs with `--column-workers 8` (L8625-8626) and the parallel solver `AUX_UVT['solver_parallel']` `7667025b` (L330; chosen at L8622-8623).
- The worker loads its modules in-process (worker L131-135) and passes `bind_column_workers(8)` (L150). The prediction calls `solve()` once (prediction `7ae28901` L55, through the binding `9b5ce82a` L175-188).

**Route B**, which runs only if the twin outlives its A141 L4 stop: `numerics.column_workers` is 2 (template L15), so two column stages run at once (driver L8420, L8814-8815). That is driver + 2 = 3 processes, fewer than 11.

**No other process start (FORMAL, by grep of each named file).**
- The driver's only process start is L1847.
- None of the following contains a `multiprocessing`, `subprocess`, `Popen`, `fork`, `spawn`, `ProcessPool`, `concurrent.futures`, `os.system`, `os.popen`, `posix_spawn` or `os.exec` call:
  - the parallel worker `293a417f`;
  - its in-process modules: prep `8681da84`, binding `9b5ce82a`, composite `75092cf6`, stream `cbbc4b96`, base `7167a264`, prediction `7ae28901`, checkpoint `069b3935`, UV-tail controller `c5bdd055`, lib `2026f2b6`, roster `4366e3d6` and provider `d6c55b55`;
  - the 15 helper modules the prep loads, its grid-cut helper `5d037291`, and the bernstein kernel `2544d22f` (its one hit is the docstring "no subprocesses");
  - the serial worker `ee27227c` and the serial solver `8ef3079b`;
  - the 11 route-B stage scripts, the route-B binding `aee7af12` and the manifest writer `b9247b1a`;
  - the 14 further modules those stage scripts load (11 helper modules and 3 stages2 modules).

**The count is a constant tied to the bytes.**
- `TWIN_TREE = {driver 1, route_a_stage_process 1, column_workers EXPECTED_LEAF['twin'] (8), resource_tracker 1}`, and `TWIN_TREE_MAX_PROCESSES = 11`.
- `validate` refuses unless the sum is 11 and the twin cap is RAM x 11 (`TWIN_RSS_CAP_NOT_RAM_X_11`).
- `fill-check` already fixes the twin's leaf at 8 (`twin_leaf`).

## 3. Files (sha256 from bytes; full values in `HASHES_S0_KIT_C2V003A.txt`)

| File | sha256 | What |
|---|---|---|
| `s0_kit_c2v003a.py` | `fdc0ee6c` | Checks and custody records. It pins the record writer `a10965b7` and `GATE_DOCUMENT_PINS_V002.json` `5e688882` by sha (both reused unchanged). |
| `launch_s0_serial_root_c2v003a.sh` | `621263a2` | `<seed\|j0\|j1\|j2> [--attempt K]`; DRY by default; `--launch` is for root only |
| `launch_twin_root_c2v003a.sh` | `f199544d` | The cw8 twin; DRY by default |
| `twin_kill_watch_c2v003a.sh` | `a3d70bec` | The A141 L4 kill trigger; only the kit name and sha change |
| `build/assemble_s0_launch_kit_c2v003a.py` | `40e83f30` | Fills the sha constants from bytes; writes the four code files by exclusive create |
| `build/src/*c2v003a*` | `d93b1f23` (kit), `714b3ed4` (serial), `459ebde4` (twin), `032b9ecb` (watch) | Code templates |
| `tests/test_s0_launch_kit_c2v003a.py` | `f5d79dcb` | 115 rows. Record runs: `tests/runs_v003a/RUN_20261019T202411Z_29980` and `RUN_20261019T202917Z_59339` |
| `DIFF_S0_KIT_C2V003_TO_C2V003A_R1.diff` | `99e838f7` | Unified diff, C2V003 to C2V003A, of the four code files, the assembler and the test (see E1 for the `_R1` name) |
| `DIFF_S0_KIT_C2V003_TO_C2V003A.diff` | `e3b0c442` (empty) | Error E1 (section 8): empty, left in place under the no-edit rule |

**Delta size** (lines removed / added): kit 37 / 136 (1,253 lines now); serial script 8 / 11; twin script 13 / 17; kill watch 4 / 5; assembler 15 / 16; test 127 / 415.

## 4. Every change

**Kit (`s0_kit_c2v003.py` to `s0_kit_c2v003a.py`):**
1. **N1: a new function, `wait_launch_record_parses(path)`.**
   - It polls every `LAUNCH_RECORD_PARSE_POLL_S` (0.2 s) until the bytes parse as JSON (`json.loads`), bounded at `LAUNCH_RECORD_PARSE_WAIT_S` (300 s) from its first poll.
   - An absent or unreadable file counts as not parsed yet.
   - It decides nothing. It returns a `parse_wait` record: outcome, waited_s, polls, the bound and exists_at_first_poll.
   - `cmd_launch_check` calls it after reading the M-15 record and before `launch_checks`. It adds the check `launch_record_parsed_within_bound` and writes `parse_wait` into the verdict.
2. **N4: the twin's cap.**
   - New constants: `TWIN_TREE`, `TWIN_TREE_MAX_PROCESSES = 11`, `CAPS['twin']['rss_cap_bytes'] = RAM x 11` and `RSS_CAP_OF_CALL = {serial: RAM, twin: RAM x 11}`.
   - `validate` refuses a serial cap other than RAM (`RSS_CAP_NOT_RAM`) and a twin cap other than RAM x 11 (`TWIN_RSS_CAP_NOT_RAM_X_11`).
   - The plan's `caps_basis.rss_cap_bytes` names the basis for each call.
   - `monitor-argv` also requires `--rss-cap-bytes` to equal the kit's cap for the call (`RSS_CAP_NOT_THE_CALL_CAP`), whatever the plan file says.
   - `launch_checks` adds `rss_cap_is_call_cap`: the record's RSS cap is an int equal to the kit's cap for the call.
   - The `LAUNCH_RULE` text names both caps.
3. **Version tags.**
   - `VTAG` is `C2V003A`.
   - Every record, plan and verdict schema ends `_C2V003A`.
   - Run names are `..._RUN_C2V003A_A<k>`.
   - The synthetic-pins schema is `S0_LAUNCH_KIT_SYNTHETIC_PINS_C2V003A`.
   - `CAPS_S45_C2V003` (the caps file) is unchanged.

**Serial and twin scripts:** only the kit name and sha, the comments, and the DRY text (the parse wait; the twin's RSS cap RAM x 11) change. There is no logic change: both already call the kit's `launch-check`, which now waits.

**Kill watch:** the kit name and sha only. **Assembler:** the file names only.

**Unchanged in logic:**
- the wall and output caps (`CAPS_S45_C2V003` `35f66b6a` is still compared);
- the disk guard;
- M-15 first and seed first;
- every pin;
- the step-2 receipt and the watch-check;
- the kill watch and the relaunch path;
- exclusive creates.

## 5. CHOICES (root may overrule each)

- **C1. The 300 s bound starts at launch-check's first poll,** not at the file's birth time. The script calls launch-check as soon as its own 0.2 s existence poll sees the file, so an honest record always gets at least 300 s from its creation, never less.
- **C2. "Parses" means any JSON text** (`json.loads`).
  - A prefix of root_monitor's one-object record never parses, so a parse means the write is complete.
  - Strict-reader faults (duplicate keys, NaN, not an object) are then judged by `launch_checks` and read MISLAUNCH at once.
- **C3. A wait that ended unparsed is a MISLAUNCH even if the record parses a moment later** (P06). The decision never depends on a race at the bound.
- **C4. The independent call-cap checks** (`RSS_CAP_NOT_THE_CALL_CAP`, `rss_cap_is_call_cap`) catch an edited plan file (C08). They add `rss_cap_is_call_cap` to the failed list of a cap mis-launch: K01, T10, C04 and C07 read `[caps, rss_cap_is_call_cap]`.
- **C5. One kit version per launch root (as C2V003 N5).** C2V003A counts only C2V003A-named records, so a C2V003 seed launch does not satisfy C2V003A's seed-first check (fail closed).

## 6. Tests (TESTED; two record runs; 28/28 + 84/84 + 3 OBSERVED each)

**Row accounting (TESTED, by comparing the RESULTS files).**
- Both runs have the same 115 rows with the same kinds and results.
- 98 of C2V003's 102 ids are ported. 92 change only in names (the C2V003A tags). 6 change their expectation:
  - N01: the twin cap is RAM x 11;
  - N04: the twin refusal is `TWIN_RSS_CAP_NOT_RAM_X_11`, and the twin is planned at RAM x 11;
  - T01: the DRY twin shows `--rss-cap-bytes 1511828488192`;
  - T08: the twin record is at RAM x 11 and `rss_cap_is_call_cap` is true;
  - K01 and T10: failed is `[caps, rss_cap_is_call_cap]`.
- 4 ids are not ported (F01-F04; R3). 17 ids are new.
- P07 waited 300.168 s and 300.195 s in the two runs. In both, its stop read `NOT_KILLED_TARGET_REFUSED`.

**New rows.**
- **N1, MUST_PASS:**
  - P01: an empty serial record, written 3 s later: LAUNCH;
  - P02: a half-written twin record, completed 3 s later: LAUNCH;
  - P03: launch-check alone, an empty record completed 2 s later: CONFIRMED;
  - P08: a record complete at the first poll: CONFIRMED, polls 1.
- **N1, MUST_FAIL:**
  - P04: still unparseable at the bound (the bound set to 3 s in the loaded module; the file is untouched): MISLAUNCH;
  - P05: parses and mismatches (retries 1): MISLAUNCH at once;
  - P06: a wait that timed out on bytes that are now honest: MISLAUNCH;
  - P07: end to end at the real 300 s bound: MISLAUNCH, exit 5.
- **N4, MUST_PASS:**
  - C01: validate plans the twin at RAM x 11 and the serial at RAM; `TWIN_TREE` sums to 11;
  - C01b: monitor-argv accepts the twin at RAM x 11.
- **N4, MUST_FAIL:**
  - twin cap = RAM alone is refused: C02 (validate; also RAM x 10 and RAM x 12), C03 (monitor-argv) and C04 (launch record);
  - serial cap != RAM is refused: C05 (validate; RAM x 11, RAM - 1 and RAM x 2), C06 (monitor-argv) and C07 (launch record);
  - C08: an edited twin plan file at RAM is refused.

**Test-side changes.**
- The honest stub monitor writes its record with `indent=1` and a final newline, as root_monitor's `_write_x` does.
- New stub variants: `ram1`, `x11`, `late`, `partial` and `never`.
- P07 runs in the background at the real bound, so each run takes about 306 s.
- The P03-P06/P08 launch records live under `RUN/PEXT`, outside the cleanup glob, with a fake child pid `0x7FFFFFFF` that is never signalled.
- RESULTS adds `ported_from` (`8001c2a7`) and `not_ported`. `kit_files` no longer lists `FREEZE_EXPECTED_INPUTS_C2V002.json`.

## 7. For root to rule

- **R1. The serial tree is up to 3 processes, not one.** A172 keeps serials at RAM because a serial is "one process". From bytes:
  - In route A, a serial runs the driver + 1 stage process. With `column_workers` 1, the serial worker `ee27227c` and the serial solver `8ef3079b` start nothing.
  - In route B, the column stages run two at a time, so the tree has 3 processes. `numerics.column_workers` is 2 (twin template L15, and `fill-check` requires the pair to differ only in the route-A leaf; driver L8420, L8814-8815).
  - By N4's own reasoning, the cap that can never stop an honest serial is RAM x 3.
  - This build keeps RAM, as commissioned. Root rules whether to commission a successor with the serial at RAM x 3.
- **R2. A MISLAUNCH for a record still unparseable at the bound cannot be stopped by the kit.**
  - `kill-target` needs the record's `child_pid`, so the stop reads `NOT_KILLED_TARGET_REFUSED` and the driver keeps running. The MISLAUNCH record is written and the script exits 5 (P07; this is C2V003's unchanged stop path).
  - Root stops such a run by hand, or commissions a successor that finds the child through the monitor pid (its ppid) and applies the other kill-target checks.
  - root_monitor writes the record in one write right after it starts the driver, so this case needs a write failure (for example, a full disk).
- **R3. F01-F04 are not ported.** They open `FREEZE_EXPECTED_INPUTS_C2V002`, `C2V001` and `CX3V002`, which this commission excludes. They test C2V002 freeze data that C2V003A does not change.

## 8. Conduct and disclosures

**Opened (named paths only):**
- V006: only sections A166, A170, A171 and A172 (an awk filter on the `## A1xx` headings), plus a count of pin lines;
- the C2V003 kit files, templates, assembler, test, README, HASHES and the runs_v003 RESULTS;
- root_monitor `ba031c23`;
- the driver `577f8c94` (targeted line reads and greps);
- the twin template `1aa66269`;
- `POLICY_C2V001.json` and the filler `ec417e76` (greps for the template pin only);
- the parallel worker `293a417f`, and parts of the parallel solver `7667025b`;
- the runtime's multiprocessing `popen_spawn_posix.py`, `resource_tracker.py` and `spawn.py` (targeted lines);
- greps of the module files listed in section 2;
- the path list of `GATE_DOCUMENT_PINS_V002.json`;
- the C2V002 builder's top-level lines (for F05).

**Hashed without reading:** the gate documents (G01, R14) and the real pins (validate, in Z01).

**Not opened:** any FREEZE_EXPECTED_INPUTS_* file, the slots file, run trees, External1, `~/.codex`, and any NGC3198 target, observed-velocity or sigma file. No ΛCDM import.

**V006 moved during the record runs:** `c5121811` became `8536ab73`, then `9fa290f2`. All three versions have 0 HANDOFF_PIN, SPEC_PIN and WATCH_PIN lines, so Z01 and Z01b refused at "no HANDOFF_PIN S0_SEED", as before.

**Writes.**
- Development and one full test run (28/28 + 84/84) were done in the session scratchpad first.
- In this folder, every C2V003A file was written once, by exclusive create: the 4 templates, the assembler, the 4 assembled code files (their bytes equal the scratch build's), the test, two runs under `tests/runs_v003a/`, the diff, this README and `HASHES_S0_KIT_C2V003A.txt`.
- No C2V001, C2V002 or C2V003 file was touched.

**Error E1.**
- A zsh loop that did not word-split its file pairs ran the exclusive create of `DIFF_S0_KIT_C2V003_TO_C2V003A.diff` with no diff output. The file is 0 bytes (sha `e3b0c442...b855`, the empty string).
- Under the no-edit rule it is left as is. The diff is `DIFF_S0_KIT_C2V003_TO_C2V003A_R1.diff` (`99e838f7`).
- Nothing else was written by that command. Root may delete the empty file.
