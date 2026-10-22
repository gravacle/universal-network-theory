# P-112 cx2v003 root re-verify findings (root workflow wf_97d200ad; two lenses; both PASS_WITH_FIXES, 0 blocking). Root-written by exclusive create.

## Lens 1: fixes closed

**PASS_WITH_FIXES. 0 BLOCKING.** cx2v003 closes every V006 A233 item. The suggested fixes are optional and none gates a launch.

Object checked: tool `af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7`, tests `a3cdbdc661b69bd8830ea0b0f68e02674b5319064c7fb8c7060928d971c73f49`, README `8620699a…`. All three were rechecked after the runs and had not changed. All 109 entries in HASHES_CX2V003 match their bytes.

**Re-runs (runs of record)**
- **Vendor suite, run twice** (pinned interpreter `-I -B`, `nice -n 10`, six thread variables set to 1, Codex2's run stamp `d8fc4395…`):
  - 681/681 passed both times, no refusal code left unexercised, 78/78 mutants killed (20 new code mutants, 2 documentation mutants).
  - Both TEST_RECORD.json files are `4ff500c0…`, byte-identical to Codex2's RUN1 and RUN2.
- **Part 1, the cx2v002 fixes-closed harness retargeted** (RV01–RV35):
  - 35/35 passed in RUN2 and RUN3.
  - 27/27 restoring mutants behaved as expected: the 22 earlier ones plus 5 new A233 ones.
  - 0 forbidden opens.
- **Part 2, the fresh-adversarial A-series retargeted, plus new A233 regressions:**
  - 31/31 passed in RUN2 and RUN3, and 21/21 restoring mutants were killed.
  - 0 forbidden opens and no processes left running.
  - All 11 A-cases that failed on cx2v002 now pass.

**Each A233 item: changed code (cx2v003 lines), then the regression that now passes**
- **V1:** `sampler` L1377-1399 and L1457-1458.
  - Before monitor_pid.json exists, monitors are matched by exact argv with pgid == pid. Once it exists, it is read once and matches are filtered to that pid. The raise is gone.
  - A13 covers six variants, including the cx2v002 reproduction: transient and persistent probes, the pid file published early or not at all, an exact-command row that is not a group leader, and two probes in one poll. Each gives `complete` true and a close value of 0, with the pid file read at most once.
  - A13_live uses the real `ps`, with and without monitor_pid.json. The decoy is still alive when the sampler writes `.solo.json`, and the value is 0.
  - RV35, an INFO case on cx2v002, now passes.
- **F-a:** L1094-1112; callers at L1328-1329, 1612, 1659, 1807, 2148-2149 and 2285-2289.
  - Resume with only a decoy gives `no_live_match`. Real monitor plus decoy gives `command_line` with the real pid. Two exact matches give MULTIPLE_MONITORS.
  - With a null pid and a decoy: status and close give MONITOR_ENDED_NO_RECEIPT, and enforce_solo does not refuse. An exact live match gives ATTEMPT_ACTIVE and SOLO_RERUN_ACTIVE.
  - Regressions: A12, RV20, RV33.
- **F-b:** L1050-1053. A blank-argv row on the real `ps` parses as command `""` and is not counted (A11c). Mid-attempt it leaves the sample complete with value 0 (A11d).
- **F-c:** L1125 and L1146-1168. The counter does not block on a FIFO argument (A11e). Restoring the cx2v002 `identify` makes it block, and that mutant is killed.
- **F-d:** L1058-1060. A listed tool between apostrophe arguments is counted on the real `ps` (A11b).
- **F-e:** L2103-2143.
  - Seven malformed stderr forms give NOT_KILLED_TARGET_REFUSED. An honest `alive:false` with nothing visible gives ALREADY_ENDED.
  - If the child pid is visible, or the planned driver is visible on the real `ps`, the result is NOT_KILLED_TARGET_REFUSED and the target is left alive.
  - A hanging kit is refused at the timeout with no process left behind; the production timeout is 30 s.
  - Regressions: A14, the RV19 sub-case, and A02 (still ALREADY_ENDED).
- **A15:** `validate_launch_json` L1223-1242, used at L1246, 1277, 1829, 2130 and 2193.
  - Malformed shapes give named refusals.
  - The pinned root_monitor's launch.json passes validation. I checked its fields in `root_monitor_c2v001.py` L140-149, and every fixture uses its `run_monitored` output.
- **A06:** L1551-1554 and L1725. After a simulated crash, both `status` and the retry give ORPHAN_OBSERVATIONS_SIBLING, and the sibling's bytes are unchanged.
- **A10:** L295 (`st_nlink == 1`).
  - Hard-linked receipt, launch.json and solo.json files are refused with RECORD_NLINK and their targets are never opened (A10).
  - Both hard-linked cutoff-copy variants are refused and no cutoff record is written (A04c).
- **A09:** the README now says work logs are guard-read only. The A09 sweep accepts a benign symlinked refusal log, which matches the new text.
- **Lens-1 items:**
  - The s0 realpath check is at L824; aliases are refused with CONFIG_SYMLINK (L1a).
  - The `monitor_receipt` check is at L1845; a missing or different pin is refused (L1b).
  - Both dead fields are gone (L1c).
  - The README discloses the MULTIPLE_MONITORS change, A09, A06 and A226 item 2 (L1d).
- **TOOL_PIN `P112_LAUNCHER_CX2V003`** (L28): the 21-case matrix in A08 and RV09 behaves as expected. A line named CX2V002, even with this tool's sha and path, gives TOOL_PIN_MISSING.
- **Single read (A226 item 1):**
  - A16a: reads happen only in `read_and_pin`, `observe_file` and `identify` (now a bounded descriptor read).
  - A16b: no duplicate reads across the CLI operations, and exactly one V006 read per CLI operation.
  - A18: the new `kit_kill_target` read in stop-outside-set reads launch.json once, and the record pins that read.

**Changes not traceable to A233, with my judgement.** The diff is 386 lines: 3 new definitions, 21 changed, 0 removed, which matches SOURCE_DELTA.
1. **A15 validation now runs inside `try_launch_json`** (L1277).
   - A parseable but misshapen launch.json now raises out of the sampler (L1402), out of `wait_launch_json` and out of `stop_launch_failure` (L2158). The sample is then null, and no LAUNCH or MISLAUNCH record can be written; resume repeats the refusal.
   - cx2v002 recorded a MISLAUNCH for, say, a string child_pid.
   - The pinned monitor cannot produce such a file, so this is a NOTE.
   - Suggested fix: in `try_launch_json`, catch the shape refusal and return `(raw, None)`. Keep the refusals in close and kill-target.
2. **The monitor_pid.json read moved to the top of the sampler loop** (L1390-1393).
   - A partially written file (the create-then-write race already noted on cx2v002) now ends the sampler.
   - The window is microseconds per attempt, so this is a NOTE.
   - Suggested fix: write by temp file and rename, or retry on JSON_PARSE through `observe_file`.
3. **Accepted as they are:**
   - the `identify` cache key now includes device, inode and ctime (stricter);
   - a redundant validation in `write_launch_record`;
   - the `launch_snapshot` keyword, which keeps the stop path to one read;
   - the equivalent rewrite of `seen_monitor`;
   - the test changes: REFUSE_LAUNCH_JSON_FORM now expects a raise, and the MULTIPLE_MONITORS test moved to `live_monitor`.
4. **Four sites still match monitors by name only:** L1342, 1606, 1717 and 2174. A live pgrep-form probe makes them refuse (fail-closed, transient, no record written). This is a NOTE for root's procedure: run no `pgrep -f` or grep naming the receipt while launching or recording a refusal.
5. **A06 consequence.** An orphan sibling blocks that call until root resolves it by an explicit successor procedure, as the README says.
6. **Carried from earlier versions, unchanged:** a probe whose argv contains the driver path followed by `run` is counted as an NGC process (RV15). Root's hold-rule "gone" checks must not grep for the driver command.

**Disclosures**
- I created `phase1_ngc_launch_kit_cx2v003_rootverify_c2/` and then `fixes_closed/` inside it by exclusive mkdir.
- Both RUN1s are superseded by harness bugs; neither came from the tool.
  - Part 1 RUN1 (harness revision a, sha `109fba43…`): RV28's stub lacked the new `launch_snapshot` keyword.
  - Part 2 RUN1 (harness revision a, sha `d1a2927f…`): the sample clocks in A11d and A13_live did not bracket the fixture receipt.
- As designed, the mutant runs opened synthetic sentinels only: 1 in part 1 (the F1 mutant) and 3 in part 2 (the A10 mutant).
- RV19 runs the real S0 kit's kill-target against a synthetic sleeping process only.
- V006 was read by heading only (A223, A226, A233), at sha `7649ef5b…`.
- I did not open NGC3198 data, run trees, V007_POSTSEAL_RECORDS or `~/.codex`, used no network, and launched nothing scientific. Only processes this lens started were signalled, and none is left running.

**Result files**

Folder: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v003_rootverify_c2/fixes_closed/`

| File | sha256 |
|---|---|
| `vendor_suite_RUN1/TEST_RECORD.json` | `4ff500c07c5679c2a130e78508609e24d39b81b1c3dad06a7409fd0306dc8852` |
| `vendor_suite_RUN2/TEST_RECORD.json` | `4ff500c07c5679c2a130e78508609e24d39b81b1c3dad06a7409fd0306dc8852` |
| `vendor_suite_RUN1/EXECUTION_METADATA.json` | `e70a52b553b8e49b9e59392b4d202be7320cff0bbeb040b9337a44e85a573a31` |
| `vendor_suite_RUN2/EXECUTION_METADATA.json` | `8c4f379948490f5c10444294fda8e1a85cb491acf26f49db9a3000ece069b7b7` |
| `vendor_suite_RUN1.stdout.txt` | `8ca0c798decffade63d428d3794fd8b148632663ba054939ab7c9d1574df238a` |
| `vendor_suite_RUN2.stdout.txt` | `35852c751c538a0332a427dff7eba0e58cbb2e358f421913c799412aa0a7dd2e` |
| `rv_fixes_closed_c2v003.py` (part 1 harness of record) | `144ba04b808b3b565f6e6d69ec10a7ebb6c07ffc3135eb67f9217286302f9175` |
| `part1_RUN2/ROOTVERIFY_FIXES_CLOSED_RESULT.json` | `aba9e7d3f48f226e22c707e9048f498026c12c03f8f98e3a10c0c701c66f6e6c` |
| `part1_RUN3/ROOTVERIFY_FIXES_CLOSED_RESULT.json` | `f85936bffe1ae29e0b561d2ada922e8b580fce9739ff404293e66f07fef9b1a8` |
| `rv_a233_c2v003.py` (part 2 harness of record) | `39cede451f4d260068febc1c36b6ff09b16ecd5cc5ad82b430be07bb3cf7154e` |
| `part2_RUN2/ROOTVERIFY_A233_RESULT.json` | `aef4e0eaea3286069a34ab8b2dbf3764b1e147e1404105bff8aa3703d1e25214` |
| `part2_RUN3/ROOTVERIFY_A233_RESULT.json` | `002b051da11559ce88b582f1fa3470ae7b59c06e27c747bd524cac2a7aa2c2a7` |
| `part1_RUN1/ROOTVERIFY_FIXES_CLOSED_RESULT.json` (superseded) | `09cd52729e95d40ae651f30b83703bc70cd9f2034c06c7c77feed178a388de63` |
| `part2_RUN1/ROOTVERIFY_A233_RESULT.json` (superseded) | `04601a029eed3dc29f1e966d3dae911856e4dbb79fe28b73f3a1e7d51bf97c3b` |
| `part1_RUN2.stdout.txt` | `ca366789336234f452f7b843cc52cbe4dd360a8f3b8b825e6ff3b386398324c5` |
| `part1_RUN3.stdout.txt` | `0903a4e5c0cf39a4b4d1cc61f8a063a8d9c3a13c04d82c4513fa6ec90463eef2` |
| `part2_RUN2.stdout.txt` | `c7d2fcdc7da0e0702fc86f7f3c337d274c33645b817425b2ff48930b7e099c89` |
| `part2_RUN3.stdout.txt` | `8e041da9374b4effec5c0abfea4b90bb1efaa9d1965a3f5d40ea96c0c3ff9574` |

All stderr files are 0 bytes.

## Lens 2: fresh adversarial on changed code

VERDICT: PASS_WITH_FIXES. There are 0 BLOCKING items.

Lens: fresh adversarial (Claude2 lineage), on changed code only. Object: P-112 cx2v003, tool `af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7`, tests `a3cdbdc661b69bd8830ea0b0f68e02674b5319064c7fb8c7060928d971c73f49`. Both were checked against their bytes before and after each run and are unchanged.

**Runs of record:** RUN1 and RUN2, run with the pinned interpreter `-I -B`, `nice -n 10` and the six thread variables set to 1.
- 27 cases each: 25 new attacks (B01–B25) plus a static (S1) and an audit-hook (S2) single-read inventory.
- Both runs gave the same result: 19 PASS, 8 FAIL.
- Every case labelled BLOCKING or FIX passed. All 8 FAILs are NOTE severity.
- 0 forbidden opens out of 1,900 P-112 opens per run, and no processes were left running.

**What holds (TESTED)**
- **V1 is closed.**
  - B01: on the real `ps`, a stand-in started exactly the way `launch()` starts the monitor (`/usr/bin/nohup` in a new session, paths with spaces) matches by exact argv with pgid == pid. In no poll did `ps` still show the nohup form.
  - B02: a 137 KB argv row comes back complete, and an 8.7 KB monitor argv still matches exactly. A counter poll over 1,001 files takes 0.08 s, or 0.04 s once cached, against the 10 s gap limit.
  - B06: a monitor restarted under a new pid after `monitor_pid.json` exists ends sampling at t=65 s, which is what A223 G25 item 4 requires.
- **F-a.**
  - B07 (real `ps`): resume without `monitor_pid.json` takes the live monitor (source `command_line`) and never the live pgrep-form decoy. Once the monitor is stopped it gives `no_live_match`.
  - B08 (real `ps`): for a solo record with a null monitor pid, a live monitor gives ATTEMPT_ACTIVE, MONITOR_RECEIPT_MISSING and SOLO_RERUN_ACTIVE. With only the decoy alive it gives MONITOR_ENDED_NO_RECEIPT.
  - B09: two exact group leaders give MULTIPLE_MONITORS. Non-leaders, whitespace variants, pid 1 and a malformed argv are never taken as the monitor.
  - B24: a launch failure with a null monitor pid never signals a live pgrep decoy; cx2v002's broad matcher would have sent it SIGTERM.
- **F-c.**
  - B11: a file that is regular at stat and a FIFO at open causes no hang (non-blocking open, then fstat). A file that grows after the stat is read with exactly `cap+1` bytes and refused. A device reached through a symlink, a socket and a directory are never opened.
  - B12: a copy exactly at the cap is identified; one byte over and a zero-length file give None. The largest declared tool is 669,113 bytes, under the 8 MiB cap.
- **F-b and F-d.**
  - B13: the real `ps` escapes a newline in an argument as `\012`, so no row can be forged.
  - B15: blank and whitespace-only rows are accepted and not counted; malformed rows still refuse.
- **A06.** B19: a KIT orphan, a dangling-symlink parent and the retry, history and assemble paths all refuse with the named code and write no files; a leading-zero k and a name that merely shares a prefix are ignored.
- **Lens 1.**
  - B23: the sample's receipt pin must be exactly equal; `//`, `/./`, an extra key, uppercase hex and a KIT sample without the pin all refuse.
  - B22 (INFO): a case-variant spelling of an s0 path passes the realpath check.
- **Single read (A226 item 1).**
  - S1 (static): there are 7 byte-read or open sites, all inside `read_and_pin`, `observe_file`, `identify` (`os.open` plus a bounded `fdopen`), `write_x_bytes` and `new_log`. Calls to the read helpers from the changed functions are listed in the result file.
  - S2 (audit hook): 15 operations (CLI status, dry launch, live synthetic launch, close, status; the sampler; resume; post-bound kill-target; stop-outside-set; close with a sample; refusal record; status; null-pid enforce_solo and status; cutoff). There were 0 duplicate reads of fixed inputs by path, realpath or inode.
    - V006 was read once, as a changing file, in each CLI operation.
    - Over 31 polls the sampler read `monitor_pid.json` once and the receipt once.
    - Kill-target used the launch-json snapshot it was given. Without one, it read `.launch.json` once and the second read was served from the cache.
    - The live synthetic launch gave LAUNCH, a complete sample with value 0 and a bound receipt pin.

**Notes (non-blocking), each with an exact fix**
1. **B04: `monitor_pid.json` caught mid-write kills the sampler.** If the sampler reads the file between its create and its write, it raises JSON_PARSE and dies, and close writes `other_ngc_processes_max: null`.
   - This is the race already noted for cx2v002. cx2v003 now makes this read on every attempt.
   - The window measured on this host was p50 about 40 µs and p99 54–158 µs, so about 1e-5 to 3e-5 per attempt.
   - A plain retry with `read_record` would be served the cached empty bytes, because `read_and_pin` caches before it parses.
   - Fix: read it as a changing file until it parses.
     ```
     raw, _ = observe_file(mp, "monitor_pid")
     try: doc = strict_json(raw)
     except Refusal: doc = None
     if doc is not None:
         need(type(doc) is dict and type(doc.get("monitor_pid")) is int and doc["monitor_pid"] > 1, "MONITOR_PID_FORM")
         monitor_identity = doc
     ```
2. **B14: a probe naming the full driver command is counted as an NGC process.** This rule predates cx2v003 and the F-d change keeps it.
   - Any process whose argv contains `<absolute driver path> run` as whitespace tokens is counted, for example `pgrep -f "<planned driver command>"` or `ps aux | grep "<abs driver path> run"`.
   - During a counted solo rerun that gives `other_ngc_processes_max` ≥ 1, so the rerun does not count (about 14 days).
   - A223 prescribes no such probe (the "gone" check uses the monitor pid and receipt), so this is a NOTE.
   - Fix (procedure): during an attempt, check the driver only by pid (`ps -o command= -p <child_pid>`).
   - Optional code fix: for `driver_only` tools, require the driver path at argv[3] after `PY -I -B`.
   - If root's procedure does include such a probe, this becomes a V1-class blocking item.
3. **B18 (A15 residual): a launch.json with wrong field types.** Only a malformed root_monitor can produce one.
   - `try_launch_json` lets the field-type refusal escape. The sampler then dies with a null sample, where cx2v002 kept sampling. Launch and resume refuse before any stop or record, which leaves LAUNCH_RECORD_MISSING.
   - An integer of 400 digits in `caps` raises OverflowError, which `cli` does not catch.
   - Fix: in `try_launch_json`, `try: return raw, validate_launch_json(doc) except Refusal: return raw, None`. In `validate_launch_json`, refuse ints with abs ≥ 2**63 before calling `math.isfinite`, or catch OverflowError as LAUNCH_JSON_FIELD_FORM.
4. **B20: a hard link that appears mid-attempt kills the sampler.** A same-volume hard link to `<outdir>.receipt.json` or to `monitor_pid.json` makes the sampler raise RECORD_NLINK and die, giving a null sample. Close refuses until the link is removed.
   - External1 is APFS and root_monitor writes with `open('x')`, so nlink is 1; only an outside tool that makes same-volume hard links (`cp -al`, `rsync --link-dest`) can trigger this.
   - Fix (procedure): no hard-linking under the run roots or launch roots during Phase-1.
5. **B16: the kill-target timeout is shorter than the kit's own worst case.** The 30 s timeout is below the real kit's internal worst case of 60 s (3 `ps -p` calls at 20 s each).
   - A slow kit gives NOT_KILLED_TARGET_REFUSED: the MISLAUNCH record is truthful but the target is not stopped, and stop-outside-set refuses (it can be retried).
   - The timeout path does kill the kit child; none was left running.
   - Fix: set `KIT_KILL_TARGET_TIMEOUT_S` to 75 or more, or document the gap.
6. **B17: a `ps` failure inside the cross-check aborts the stop path.** When `ctx.system.processes()` fails inside the ALREADY_ENDED cross-check, PS_FAILED propagates out of `stop_launch_failure` and no MISLAUNCH record is written. It is recoverable through LAUNCH_RECORD_MISSING and `--resume`.
   - Fix: wrap that call in `try … except (Refusal, OSError, subprocess.SubprocessError): return refused`.
   - Child-pid reuse, the planned command alive in a non-leader, the snapshot's child pid, and the stdout forms (Arabic-Indic digits, `+42`, two lines, `0`, `1`) all correctly give NOT_KILLED_TARGET_REFUSED.
7. **B03: the sampler does not bind `monitor_pid.json` to the plan.** A forged or stale file pointing at a decoy pid makes the sampler follow the decoy and stop with MONITOR_ENDED_NO_RECEIPT_NO_SOLO_FILE while the real monitor is alive.
   - Only P-112 writes this file, in a per-invocation work directory, so this is not realistic.
   - Fix: pass the plan pin into `sampler` from `cli _sampler`, and require `schema == "P112_MONITOR_PID_CX2V001"` and `plan == plan_pin`.
8. **B05: a duplicate exact monitor can take the root of the sampler's own process tree.** Before publication, the tree root is `mons[0]`. A second process with the exact planned argv that leads its own group (for example two concurrent launches of one attempt) can take that root, and the real driver is then counted (value 1 against 0 for the control).
   - Fix: exclude the descendants of every matched monitor, not only `mons[0]`.

**Information only**
- **B25: broad matching remains in four places.** Path-plus-`--receipt` matching is still used in `record_monitor_refused`, the in-flight-plan check in `enforce_solo`, `honor_residual` and the tail of `stop_launch_failure`. With a probe running, each refuses fail-closed and can be retried; none signals anything or nulls a sample. The README's "cannot terminate sampling or extend monitor liveness" holds for the sampler, resume and null-pid liveness, not for these four refusals.
- **B22:** `os.path.realpath` does not fold case on APFS. Root should write the s0 paths in their canonical case.
- **B21:** the nlink check is a stat by path before the read. A link added in between leads to reading the same inode, never a different file.
- **B10:** exact null-pid liveness cannot see a kit monitor that is not a group leader. This cannot happen, because the kit's `launch-record` requires `--mon-pid` (kit L1219).

**Disclosures**
- `phase1_ngc_launch_kit_cx2v003_rootverify_c2/` already existed with `fixes_closed/` from the other lens. I created `fresh_adversarial/` by exclusive mkdir and installed the harness by exclusive create (0444).
- One development run was made in my scratchpad and is not of record. It produced a false B13 failure because the fake pid 99991 belonged to a real process; that pid was changed to 999991, above PID_MAX.
- I read V006 by heading: A223 (the G25 items and the "gone" definition), A226 and A233, at sha `7649ef5b…`. I read tool sources only: the real kit's kill-target and launch-record code, root_monitor's write path and the twin watch.
- A real root_monitor and c2v010 run was live on this host. I saw it only through `ps` and never signalled it.
- Every live process I started had synthetic paths only in its argv, and only my own processes were signalled.
- The live synthetic CLI launch (S2) starts a sampler subprocess. As the vendor's own test does, it hashes `.py` files named in other host processes' argv, through `guard_read`.
- No NGC3198 data, run trees, V007_POSTSEAL_RECORDS or `~/.codex` were opened. No network was used and nothing scientific was launched.

**Result files** (in `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v003_rootverify_c2/fresh_adversarial/`, sha256)

| File | sha256 |
|---|---|
| `rv_fresh_adversarial_c2v003.py` (harness of record) | `cbf3b5a004b6e222ad597e884ea1fb01baf21d59f213a424c19456282765c5df` |
| `RUN1/ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json` | `3ddd2629b9a674fbfd9f69eeb57f9aab8172332f1a9753d690dfab57f285d66b` |
| `RUN2/ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json` | `647f666a64029049f45de8d289e0871c6faf28aa5c3a5bae531a2173b8c8e81a` |
| `RUN1.stdout.txt` | `b57aca3c04639bb55ceb4d6b1ef533d10d692447854b9f7640d15ce42af9da8e` |
| `RUN2.stdout.txt` | `e8479216086b2b01b5afaaf28f9d027943c61aa010a48ddada5f97a4c0a9f867` |
| `RUN1.stderr.txt`, `RUN2.stderr.txt` (0 bytes) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Run start times (`date -u`) are in `RUN1.date_u_start.txt` (20:52:26Z) and `RUN2.date_u_start.txt` (20:53:00Z).
