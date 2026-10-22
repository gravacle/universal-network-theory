# P-112 cx2v002 root re-verify findings (root workflow wf_ea5573b3; two lenses). Root-written by exclusive create.

## Lens 1: fixes closed

**PASS_WITH_FIXES. 0 BLOCKING.** All of B1–B4, F1–F6, the cleanup, the 0785 rules and the 0786 answers are closed in cx2v002 (tool `65ac5349…`, tests `920cf3ef…`). The 25 original root RV cases, retargeted to cx2v002, now all pass; on cx2v001, 14 of them failed. The fixes listed below are all non-blocking.

**Re-runs**
- **Vendor suite, run twice** (pinned interpreter `-I -B`, `nice -n 10`, the six thread variables set to 1, Codex2's run stamp `b075b21f…`): 639/639 passed both times, no named refusal code left unexercised (236 codes), and 56/56 mutants killed (35 carried over from cx2v001, 21 new). Both TEST_RECORD.json files are `b323fd78…`, byte-identical to Codex2's RUN1 and RUN2.
- **Manifest:** all 100 entries in HASHES_CX2V002 match their bytes.
- **Adversarial harness, run twice** (`rv_fixes_closed_c2v002c.py`, `8eee3bcf…`): 35/35 cases pass both times, with 0 forbidden opens out of about 5,945 P-112 opens. Cases RV01–RV25 are the original ones; RV26–RV35 are new regressions for items that had no original case.
- **My own mutation check:** 22/22 mutants behaved as expected.
  - 19 were killed. Each restored a fix site to its cx2v001 form or a cache-bypassing equivalent, and the matching RV case caught it.
  - 3 survived, and that was the expected result: putting back the literal cx2v001 `pin_of` line in `history` or in `--verify` is harmless, because the per-command byte snapshot returns the same bytes. The cx2v001 tokenizer that raises on a quote is caught by RV11, while `count` drops just that row, so RV12 still passes.

**Each required item: changed code (cx2v002 lines), then the regression that now passes**
- **B1:** `write_launch_record` L2098-2121 pins `sha(raw)` from the buffer passed in, with no re-read. `finish_launch` L2151/2159 passes that buffer. `stop_launch_failure` L2060-2095 takes one new observation only when nothing parsed within the bound. `try_launch_json` L1212-1224 returns the bytes even when they don't parse. Passing: RV01 (one read; record sha equals the checked sha), RV20 and RV28.
- **B2:** `history` L1597-1603 reads the receipt once and pins that read. Passing: RV02.
- **B3:** `--verify` L1907-1911 compares and pins the same read. Passing: RV03.
- **B4:** `command_argv` L1058-1063 falls back to `split()` on a parse error. `count` L1141-1164 skips a bad row instead of failing. In the sampler, L1326-1332 keeps only `processes()` inside the try. Passing: RV11-RV15, including a listed tool whose arguments contain an apostrophe, which is still counted.
- **F1:** `guard_record`, `read_record` and `observe_file` (L292-319), used at L1216, 1369, 1395, 1401, 2175, 2179-2180 and 2250. Passing: RV05-RV07, and RV32, where aliases of plan, invocation and monitor_pid refuse with RECORD_SYMLINK without opening the target.
- **F2:** L365-366 and L389-390. Passing: RV08 (all 9 separators), RV09 (the 21-case matrix updated for CX2V002) and RV10.
- **F3:** `live_monitor` L1097-1102; `launch_resume` L2178-2203; the twin watch `--mon-pid` is optional at L2139 (the kit's watch script accepts that). Passing: RV21 (a real fork that dies between starting the monitor and writing monitor_pid.json, then resume gives LAUNCH with source `no_live_match`, then close gives FINISHED), RV33 (one command-line match gives `command_line`; two give MULTIPLE_MONITORS) and RV20 (null pid).
- **F4:** L2043-2051. Passing: RV19. An uncaught exception, `alive: true`, `alive: null` or non-JSON stderr all give REFUSED; `alive: false` and a real ended child (real kit) give ALREADY_ENDED; pid reuse is refused and the target is untouched.
- **F5:** L27, L818, L737. Passing: RV24. A production Context refuses with V006_CONFIG_PATH before opening the configured file, and the synthetic fence refuses the real V006.
- **F6:** L222. Passing: RV26 (path_rules, guard_read and the process counter all refuse, with no open).
- **Cleanup:** `read_and_pin` L274-288 and `read_pin`/`pin_of` L326-334; `read_fill`/`finish_call` L992-1006 pass the certificate objects on. Passing: RV04 (retargeted; one read, pin equals that read), RV27 and RV31 (raw reads exist only in `read_and_pin`, `observe_file` and `identify`; no `pin_of`→`read_pin` pairs remain).
- **0785:** `read_scope` L260-271; observations in records via `Context.write` L857-859; cutoff L1820-1844.
  - RV27: no file is read twice within one operation, across 10 operations (live launch and close in RV22, resume and close in RV21).
  - RV28: launch.json does not parse for the whole bound, then a fresh read after the bound parses. The MISLAUNCH record pins, quotes and checks that one buffer.
  - RV29: the cutoff copy equals the hashed buffer from the cutoff read, not the gate read.
- **0786:** name P112_LAUNCHER_CX2V002 (L28); sibling check L1460-1477; record write order L1667-1670; the README table of retained names. Passing: RV30. The sibling is written first, both files are 0444, the record keeps its exact key set and the rule binds the sibling's sha. For both KIT and P112 records, a missing sibling, wrong sha, no binding, two tokens, a glued token or a symlinked sibling each refuse with the right code.
- The README states the A226 item 2 disclosure.

**Changes not traceable to a required fix, with my judgement**
1. **surrogateescape** (L755). Accept, and record it in V006 as an addition to B4. RV34 shows the problem it fixes is real: while one process with non-UTF-8 bytes in its arguments is alive, cx2v001's `System().processes()` raises UnicodeDecodeError, which cx2v001's sampler does not catch, so the sampler dies and the value is null. JSON round-trips the decoded text exactly. Restoring strict decoding is detected.
2. **MULTIPLE_MONITORS now stops the sampler** (L1334-1335, now outside the try). cx2v001 marked the poll incomplete and still wrote `.solo.json`; cx2v002 exits the sampler with no `.solo.json`, and at the first sample a launch now refuses with SAMPLER_FIRST_SAMPLE_MISSING after 60 s. The value is null either way. The vendor test REFUSE_MULTIPLE_MONITORS was rewritten to match, but the README does not mention it. RV35 shows that an operator running `pgrep -f <monitor path> --receipt <outdir>.receipt.json` is matched as a monitor. Accept, but fix: disclose it in the README, and add to root's procedure that nobody runs such a command during an attempt.
3. **The solo sample gains a `monitor_receipt` pin.** This goes beyond brief §9's key list, but the extra key is harmless; I recommend having close check that it matches the receipt pin close uses.
4. **New record fields:** `launch_wait` (benign), `monitor_pid_source` (required by F3), and in the failure path the checks are recomputed from the buffer read after the bound plus a new `launch_json_within_bound` key. Accept; this is what makes 0785 item 2 consistent.
5. **`SYNTHETIC_REAL_V006` in the synthetic fence.** Accept; it completes F5.
6. **The realpath check now covers every record and metadata read**, beyond the sites F1 named: kit records and receipts, the root-written refusal plan, the outside-stop launch.json and the dry outputs. It fails closed. But config validation checks realpath only for P-112's own roots (L819-821), not for `s0.launch_root` or `s0.run_root` (L822-823), so a non-canonical s0 path would make every command refuse with RECORD_SYMLINK. Fix: add the realpath check for the s0 roots at config time, or have root confirm the s0 paths are canonical.
7. **`read_and_pin` caches bytes before parsing them, and shares the cache across alias spellings.** No current caller retries within the same operation, so this is a hazard for later edits only.
8. **Dead code:** `IMPLEMENTATION_REVISION` (L29) and `Context.v006_gate_observation` (L832). Remove them in the next revision.
9. **`observations` is added to every record, including shared schemas** (attempt receipt, cutoff record, outside-stop record). 0786 authorizes this, and c2v006's `_receipt` reads by role keys so it tolerates the extra key. The G26 freeze dispatch must accept `observations`, and `advisory`, which cx2v001 already added to the cutoff record.

**Notes**
- **For root's D7 records:** write `<record>.observations.json` first, by exclusive create, as `{counts: {}, last_observation: {}, date_u}`. All paths must be canonical. The rule text needs exactly one whitespace-delimited `observations_sha256=<64 lowercase hex>`.
- **A race that also exists in cx2v001:** records are written by create-then-write, not atomically. If the sampler reads monitor_pid.json or invocation.json, or launch reads sampler_first_sample.json, in the microseconds between create and write, the parse fails and the sampler or launch stops. Writing to a temp file and renaming would remove this.

**Disclosures**
- The folder `phase1_ngc_launch_kit_cx2v002_rootverify_c2` did not exist, so I created it, then created `fixes_closed/` inside it by exclusive mkdir.
- The first run of my harness (revision a, RUN1) had two harness bugs, so RUN1 is superseded:
  - RV10's comparison of tuples against lists came from the original `rv_adversarial_c2v001.py`, so the original RV10 could never pass.
  - RV21 read the result wrapper instead of the result.
- RUN1's result file also quotes about 600 characters of this host's `ps` output in one mutant's detail. Revision b fixed the two bugs but was never run; revision c added bounded error text and produced RUN2 and RUN3.
- In the F1 mutant run, the mutant (by design) opened a synthetic result.json in a test fixture; this is logged separately from the unmutated runs.
- I read V006 by heading only (A223 was not opened; A226 and A229 were). Its sha was `0436cd81…` when I read it.
- I did not open NGC3198 data, run trees, V007_POSTSEAL_RECORDS or ~/.codex, used no network and launched nothing scientific. Every fixture process I started has been stopped.

**Result files** (in `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v002_rootverify_c2/fixes_closed/`, sha256)

| File | sha256 |
|---|---|
| `vendor_suite_RUN1/TEST_RECORD.json` | `b323fd780c77201560f1d975b2e410e4ebb35b09bb630b4efeb6c763f89fd954` |
| `vendor_suite_RUN2/TEST_RECORD.json` | `b323fd780c77201560f1d975b2e410e4ebb35b09bb630b4efeb6c763f89fd954` |
| `vendor_suite_RUN1/EXECUTION_METADATA.json` | `074394febf1c72dc8f6ebf47e244e4a0a8be4cf03373a812b53d6589a1f62db6` |
| `vendor_suite_RUN2/EXECUTION_METADATA.json` | `7780265d344dfe37d6819ca42a86637580a01a41e2c526795ab34eaa73c7c860` |
| `vendor_suite_RUN1.stdout.txt` | `d02a1027389a501b135c8a2afa5a9b5fd92677e40066ff133c6b1547f5a2fe0e` |
| `vendor_suite_RUN2.stdout.txt` | `9b2ee0a8a317ba8b35daca161075ce73d9bb2dd10d1ae0317fa43710a78b1e83` |
| `fixes_closed_RUN2/ROOTVERIFY_FIXES_CLOSED_RESULT.json` (of record) | `07e3c3d24f0eba004b9f6031e3e1fb2be99940e608ece8e71c4377d953bdf32d` |
| `fixes_closed_RUN3/ROOTVERIFY_FIXES_CLOSED_RESULT.json` (of record) | `646381295f442bc7e653855eea2473b314c32684a7712213d68dad985e8b4663` |
| `fixes_closed_RUN1/ROOTVERIFY_FIXES_CLOSED_RESULT.json` (superseded) | `06085179d393ae9a647174f88337d979376fb0c769c2db355b5e6c92cffadf04` |
| `rv_fixes_closed_c2v002c.py` (harness of record) | `8eee3bcf0530f2e0b0ca833c673b2df0bfcb06a2b10b97e54dda2d6a37763efa` |
| `rv_fixes_closed_c2v002.py` (revision a) | `a99ff2632b2901bd197b8cc565def51eb9d90a9856578b8c203d534c54d3295d` |
| `rv_fixes_closed_c2v002b.py` (revision b, never run) | `589f9467f32b4eb9d1638f1302b89fac724d43f3cc8ab94d8a181c9f93e46e71` |

## Lens 2: fresh adversarial

**Verdict: FAIL, with 1 blocking item.** The fix is about five lines. Everything else on the fresh-attack list held up or is a non-blocking fix.

Lens: fresh adversarial (Claude2 lineage). Object: P-112 cx2v002, tool `65ac5349…77aa`, tests `920cf3ef…`. Both were checked against their bytes before and after the runs and are unchanged.

Runs of record are RUN3 and RUN4. Both used the same harness and gave the same per-case results: 25 cases, 14 PASS and 11 FAIL. No processes were left running. In each run the audit hook flagged exactly 2 forbidden opens, both in my deliberate hard-link attack (A10) on a synthetic sentinel file.

**BLOCKING**

**V1. One process that names the monitor command kills the sampler, so the attempt's sample is null** (A13; the same consequence class as cx2v001 B4).
- The sampler's poll loop (L1334-1335) runs `mons = matching_monitors(...)` and then `need(len(mons) <= 1, "MULTIPLE_MONITORS")`. The refusal propagates and the `_sampler` process exits 2, so no `.solo.json` is written.
- close-attempt then proceeds and writes `other_ngc_processes_max: null`. A null sample can never be counted, so a counted rerun is lost (about 14 days).
- TESTED: with the real monitor row plus one transient pgrep-form row in poll 2, the sampler stopped with MULTIPLE_MONITORS, wrote no `.solo.json`, and close-attempt wrote null.
- The trigger is any process whose argv has the monitor path and `--receipt <receipt>` as separate whitespace-delimited tokens. `pgrep -f "<monitor> .* --receipt <receipt>"` qualifies, and so does `ps | grep -F "<planned command>"`. That is exactly the "gone" check A223 describes. A live inert decoy matched on the real `ps` (A12).
- With a periodic liveness loop running during a 7-day solo rerun, at least one hit is close to certain.
- Exact fix in `sampler`:
  - Once `work/monitor_pid.json` exists, read it once and set `mons = [r for r in matching_monitors(rows, monitor, outdir) if r["pid"] == mp_pid]`. Before it exists, use the matches as they are.
  - Delete `need(len(mons) <= 1, "MULTIPLE_MONITORS")` from the poll loop. A single row must never raise.
  - Optionally, also require `r["command"] == " ".join(plan["monitor_argv"])` and `r["pgid"] == r["pid"]`. The monitor is started with start_new_session.
- Tests: two MUST_PASS cases, one with a transient and one with a persistent pgrep-form decoy, each giving `complete` true and a value of 0. Add a restoring mutant that puts the raise back; it must be killed.

**Fixes recommended in the same cx2v003 (non-blocking)**
- **F-a (A12), decoy adopted on resume.** Resume without `monitor_pid.json` takes a decoy's pid as the monitor (L2196; recorded `monitor_pid` 900777, source `command_line`). With a null monitor pid, `status` reads ATTEMPT_ACTIVE instead of MONITOR_ENDED_NO_RECEIPT while the decoy lives. A real monitor plus a decoy gives MULTIPLE_MONITORS, which fails closed. Fix: match on the plan's exact `monitor_argv` plus `pgid == pid`, and use the same rule for null-pid liveness, rebuilt from the record.
- **F-b (A11c/A11d), blank-argv process.** An unrelated process with a whitespace-only argv produces the `ps` row `b'81289 80937 81289  '`. `parse_ps` (L1050) refuses it with PS_PARSE. Every poll is then incomplete and the sample is null (TESTED mid-run); enforce_solo and launch refuse. The trigger is rare. Fix: accept a 3-field row as command `""`, left uncounted.
- **F-c (A11e), FIFO argument hangs the counter.** When an unrelated process's argv names a FIFO ending in `.py`, `identify` (L1131-1136) blocks on read. TESTED: it was still blocked after 3 s, and the stalled poll means a null sample. Fix: return None unless `stat.S_ISREG(os.stat(path).st_mode)`, and cap the size.
- **F-d (A11b), shlex hides a listed tool.** Shlex-first tokenising merges `it's /listed/tool.py lane's` into one token, so the count is 0 when it should be 1. That is a false zero, not a null. Fix: `command_argv` returns `row["command"].split()` only; `ps` output is never shell-quoted.
- **F-e (A14), kit-target exit 1.**
  - ALREADY_ENDED is accepted on the kit's word while the planned driver command is visibly alive in P-112's own `ps`. Fix: confirm that no row equals the planned driver command (and `child_pid`) before returning ALREADY_ENDED; otherwise return NOT_KILLED_TARGET_REFUSED.
  - Non-UTF-8 kit stderr raises UnicodeDecodeError from `subprocess.run(text=True)` (L2042). Fix: capture bytes and treat a decode failure as NOT_KILLED. Also add a timeout.

**Notes and info (non-blocking)**
- **A15.** A parseable `.launch.json` whose fields have the wrong types (for example `"pins": [1]`) crashes `launch_checks` with AttributeError, and `cli` does not catch AttributeError. Only a malformed monitor could cause this. Harden the field type checks.
- **A06.** If the process crashes between writing the sibling and writing the record, the retry fails with FileExistsError. P-112 can then never record that refusal, and `status` shows READY with no sign of the orphan. Fix: verify and reuse the orphan sibling, or refuse with a named code.
- **A10/A04c, hard links.** A hard-linked `<outdir>.receipt.json` or `.launch.json` passes `guard_record` and its bytes are read (forbidden inode, synthetic only). A pre-existing hard-linked cutoff copy is accepted (nlink 2) and later changes as V006 grows. Fix: refuse any record or copy with `st_nlink != 1`.
- **A09 (info).** The refusal-record monitor logs, the `maybe_cutoff` record, M15 and the kit registry go through `guard_read` only, so a benign symlink is followed. Aliases into an outdir are still refused. The README's claim that "monitor/work records additionally require realpath" does not hold for the work logs.
- **A08 (info).** A malformed line starting `TOOL_PIN P112_LAUNCHER_CX2V002X …` is ignored as another tool's line.
- **Carried from cx2v001.** ENTRY_RE still differs from the kit's, and the fill-check port (`root_admission` and the other handoff pins) was still not added.
- **In-process only.** `new_work` collides when one pid launches twice in the same second. This cannot happen through separate CLI processes.

**PASS (TESTED)**
- **A01-A03, volatile `.launch.json`.** Polls went absent, then partial, then valid. The record sha, `utc` and checks all come from the checked buffer: 3 reads, 2 counted observations. After the bound, the fresh observation (parseable or not) is what gets pinned and checked: 5 observations, last pin equal to the record.
- **A04a/b, cutoff copy.** The copy is written from the hashed buffer: 1 read of V006, and the copy, the record and the observation hashes are equal even with V006 changing after the read. A planted copy with different bytes is refused; a symlinked one is refused with RECORD_SYMLINK.
- **A05/A05b/A07, siblings.** 22 tamper variants across P112 and root-written KIT records all refuse with the correct code: symlink, directory, duplicate key, NaN, relative pin, boolean count, list, token twice, glued token, uppercase hex and trailing period. Root siblings that carry root's own observation kinds are accepted.
- **A08/A08b, gate and V006.** An 18-case TOOL_PIN CX2V002 matrix under the F2 rules (line separators, NBSP, VT, BOM, heading forms, CX2V001 coexistence, case-variant path) all behave as expected. The F5 boundary holds: a case-variant V006 in production refuses V006_CONFIG_PATH. In synthetic mode the fence lets a case-variant spelling through, but `read_v006` still refuses PATH_NGC3198, and P-112 opened the real V006 0 times.
- **A09, symlink sweep.** All 11 further read sites refuse.
- **A11a, ps encoding.** A real row with surrogateescape bytes, an apostrophe, a backslash, `\012` and `\011` still counts the listed tool, with no crash.
- **A16a, static inventory.** P-112 has exactly six read/open call sites: `read_and_pin`, `observe_file` and `identify`, plus the write and directory-fsync opens.
- **A16b, audit-hook inventory.** 16 operations, including in-process `cli` runs of status, `launch --dry`, a live synthetic launch, close-attempt and assemble, plus resume, record-monitor-refused, the sampler, the cutoff and verify. There were 0 duplicate immutable reads by path, realpath or inode, and exactly one volatile V006 read per CLI operation.

**Disclosures**
- The parent folder already existed (another lens, `fixes_closed`); I created `fresh_adversarial/` with an exclusive mkdir.
- RUN1 and RUN2 are superseded by harness changes: an A09 target inside the run root, the A16b same-second work-dir name, and A11e not yet added. Their statuses are otherwise consistent with RUN3/4.
- V006 was read by heading only (A223, A226, A229), at sha `0436cd81`.
- No NGC3198 data, run trees, V007_POSTSEAL_RECORDS or `~/.codex` were opened. No network was used. Only synthetic and inert processes were started, and only they were signalled.

**Result files** (in `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v002_rootverify_c2/fresh_adversarial/`)

| File | sha256 |
|---|---|
| `rv_fresh_adversarial_c2v002.py` | `bab69dd7b9b69757d8c3fdedd797999d9ea017f98df45bf3ade1d0abeacc1f48` |
| `RUN3/ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json` | `b9203429dd4bdb2bfe6b5f5ce5f6d076d1b5f697d4dce2ae5f3f1ec04a920bc1` |
| `RUN4/ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json` | `961c299a4fdac6101a48553ee93ab2088dc434b656d46c8c65cd171979a21e9f` |
| `RUN3.stdout.txt` | `1fe8be1d2f14e8f62e50b32ddce5230537e0345634924a31074e88ba5e45e534` |
| `RUN4.stdout.txt` | `6d4fdc07befebefc52f92fa62fed1c8af67637964abe6392292425537f768c24` |
| `RUN1/ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json` (superseded) | `1d55607327377ebe275b5ac90d00a6e71e55c79f33737b8b7022a6f3ddba266b` |
| `RUN2/ROOTVERIFY_FRESH_ADVERSARIAL_RESULT.json` (superseded) | `670358d3eb231d71e64edb568a0985f4abc60b744de7a88bc7f379dd7cab2630` |

All stderr files are 0 bytes.
