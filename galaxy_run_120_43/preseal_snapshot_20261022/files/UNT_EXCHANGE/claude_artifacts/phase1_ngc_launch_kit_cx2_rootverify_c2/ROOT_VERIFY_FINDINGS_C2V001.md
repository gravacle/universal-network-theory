# P-112 cx2v001 root verify findings (root workflow wf_a86fff74; two lenses). Root-written by exclusive create.

## Lens 1: conformance

**FAIL: 2 blocking items. Both have small, mechanical fixes. Nothing else in the build failed.**

The test suite passed both times I ran it, and my test records are byte-identical to Codex2's. All 35 mutants were killed with their controls passing. The two blocking items are things the suite does not test.

## Re-runs and checks
- **Suite runs:** I ran the suite twice with the pinned interpreter (`-I -B`, `nice -n 10`, the six thread variables set to 1) and Codex2's stamp `4565818…`. Each run: 580/580 passed, no refusal code left unexercised, 35/35 mutants killed. Both TEST_RECORD.json files are `50e0951bfe19216e143a8e90785e9569a9fd795334acc1a605144df08d1a5e15`, identical to Codex2's RUN1 and RUN2.
- **Manifest:** all 59 entries in HASHES_CX2V001 match their bytes. Tool `a72d96c1`, tests `fd50301b`, README `8a6f6604`, HASHES `7ec3cb33`, brief `cddbaa8d` and ROUND5 `4e3977ab` all match.
- **G13 status map:** I rebuilt it from the V006 A223 text (read by heading). It has 54 keys, 2,052 B, sha `c36c37886aa6…`, class counts 2/4/20/10/17/1, and equals the tool's literal (L58-113, asserted at L136-137).
- **Declared process list:** the tool's 13 entries match brief §9 in content and order. Every sha matches its file, only the driver is `driver_only`, and the list sha is `c08b9858…`.
- **Source pins:** all 42 match their bytes and every A/ row of brief §2, with no mismatches.
- **Kit ATTEMPT_RE:** the tool's copy (L38-40) equals the kit's pattern exactly.

## BLOCKING

**B1. The A226 item 1 single-read rule is not met.** In three places the hash that gets recorded comes from a different read than the bytes that were checked:
- (a) `history()`: L1469 reads and parses the monitor receipt; L1474 opens it again to make the non-attempt's pin. TESTED: the receipt is opened twice in one call, and the pin comes from the second read.
- (b) `finish_launch` → `write_launch_record`: the launch checks use the buffer from `wait_launch_json` (L1980-1981). L1956-1960 reads `.launch.json` again, and sometimes a third time, for the record's `sha256`, `utc` and `child_pid`. TESTED: two opens.
- (c) `assemble_registry --verify`: L1771 compares one read; L1773 returns a pin from a second read.

There are also literal double reads, where `pin_of` is followed by `read_pin`. The second read is checked against the first hash, so no unchecked byte is ever used, but each file is still read twice. Sites: L803-804, 815-816, 829-830, 921-922, 1186, 1201, 1317-1318, 1370-1371, 1481-1484, 1581-1582, 1610-1611, 1628-1629, 1641-1642, 1726-1727, 1829-1830, 1872-1873, 2018-2019. The EPS and GQ certificates are read at L919 and again at L928 (and L894). `write_cutoff` reads the copy at L1698 and again at L1701.

Exact fix:
- Add one helper, `read_and_pin(path, decode=True)`: `guard_read`, a single `read_bytes`, then return `({"path", "sha256": sha(raw)}, strict_json(raw) or raw)`. Replace every pair listed above with it.
- `read_fill` passes the parsed EPS and GQ objects to `finish_call` instead of reading them again.
- `history`: read the receipt once, then `monitor = monitor_receipt(raw)` and pin with `sha(raw)`.
- Make `try_launch_json` and `wait_launch_json` return the last bytes they read even when those bytes do not parse. `finish_launch` passes `(raw, lj)` to `write_launch_record`, which pins and quotes only that buffer.
- `--verify`: `disk = p.read_bytes()`, compare `disk == raw`, pin `sha(disk)`.
- `write_cutoff`: read the copy once.
- Tests: add an audit-hook MUST_PASS that no pinned path is opened twice in any one subcommand (the tool's self-hash at L754 excepted), plus mutants that restore (a) and (b).
- Separately, the README should state, in A226 item 2's wording, that pinned executables are hashed and then run by path. This is unavoidable for the monitor, dry harness, kit, kill watch and driver, and the root integrity envelope covers it.

**B2. One unrelated process can null the whole attempt's sample, against G25 item 4.** `command_argv` (L981-985) runs `shlex.split` on every `ps` row. The `ps` output is not shell-quoted, so any process anywhere on the host whose arguments contain an unpaired `'` or `"` raises PS_COMMAND_PARSE. In the sampler (L1241-1245) that sets `complete=false`, so `other_ngc_processes_max` comes out null even though every `ps` call exited 0 and parsed. That is a false null, which costs about 14 days of rerun. If it happens at the first sample the launch refuses with SAMPLER_FIRST_SAMPLE_FAILED, and inside `enforce_solo` it refuses the launch outright. TESTED:
- a live process `python3 -I -c … don't` makes the count raise;
- a synthetic sampler with that row in one middle poll writes `complete:false`, giving null at close;
- the same run without the row gives `complete:true`, giving 0.

This host runs agent shell lanes all the time, so over a 7-day attempt this is a realistic risk.

Exact fix:
- L983: tokenise with `row["command"].split()`, matching how `has_arg` already treats `ps` output. Drop PS_COMMAND_PARSE or make it unreachable.
- Add a MUST_PASS test: a non-listed row with an unbalanced quote leaves `complete` true and the count unchanged. Add a mutant that restores `shlex` and must be killed.

## Conformance map (requirement → code → tests)
- §0 / G-rules, writing records: `write_x` L186-209 (exclusive, fsync, 0444, `date_u` from `/bin/date -u` with LC_ALL=C at L163).
- §1 not-do list:
  - the filler is never run or imported; its path appears only in SOURCE_PINS (L480);
  - no NGC ρ point registration anywhere (A211 N3);
  - no writes into the kit's `launches/` (L771-772; N03).
- §1a/§6.13, first attempts: S0 θ skipped through the kit-entry hit in `finish_call` (L933-950); serial leaf 1 only (L616-617); entry reuse `entry_reuse` (L468-476, ROUND5 1a). Tests T01, T11, N04*, N09.
- §1b, D6 numbering and the kit carve-out: `next_attempt` (L429-455; KIT_RELAUNCH_OWNS at L435-437) and `planned_origin` (L1326-1336). Tests N01, N11, N16, N17.
- D7, monitor refusals:
  - `record_monitor_refused` L1513-1536;
  - acceptance of root-written records in `refusal_records` L1355-1404, with the `absent` check only before the same-k relaunch at L1388-1391;
  - 0782 ruling 1 at L1392-1400.
  - Tests N04, N05, N10 including N10_0782_*, N18.
- §6.10, D9 disk and "run volume first": `disk_check` L698-709, `mount_first` L691-695, `attempt_volume` L458-459 (ROUND5 3). Tests K02, N19 and the related mutants.
- §6.1, D8 TOOL_PIN gate: `tool_gate` L291-311, regex at L45, whole-line match, name P112_LAUNCHER_CX2V001. Every writing path calls it: launch L2045, `--resume` L2008, close L1593, assemble L1766, stop-outside-set L2131, record-monitor-refused L1514, cutoff L1688, sampler L1213. Tests L01-L07 and the `unanchored_tool_pin` and `gate_on_launch_only` mutants.
- §7 θ checks:
  - code: L509-595, `float.hex` with -0.0 distinguished;
  - tests: T01-T13, including one-ulp T02-T07, T11 and T12, and T13 checked against the pinned orchestrator;
  - checked against bytes: orchestrator L523-529, filler L291-298, c2v006 `theta_sha256` L276-277.
- §8 caps: L30-33 and L438-451; check of the monitor command at L1091-1098. Tests K01-K05 (K03 and K04 are combined in one test).
- §9 / G25 sampler: L1210-1302; the five null cases in `sample_value` L365-386 with floor comparison; 1 s lead at L2078-2087; normal end at L1262-1275; 60 s wait counted only while mounted at L1276-1285. Tests P01-P09 and C14.
  - The nine role keys: RECEIPT_KEYS L52-55; test R02 uses the real builder's `_receipt`.
- §10, the next legal attempt (terminal checks first): `terminal_prefix` L397-426. The rule-(c) pair matches c2v006 L660-694 (read). The INFRA_REPEAT pair does not need rule-(c) caps. Tests N06-N08, N13, N15 and the mutants.
- RESIDUAL_RETRY: anchored parse L314-323 and `honor_residual` L1407-1443. Tests N14, N16, N19.
- D3 twin mode: L1984-1999, with the kill watch called with the brief's exact arguments and `watch_pid` recorded; twin key equals the seed key. Tests K03, K05, C05.
- D4 outside-set stop: L2130-2154, with the kit's `kill-target` exit codes checked against kit L927-967. Tests O01-O03.
- §11 launch, D7 at the launch bound, ROUND5 1b and 4: L2040-2104 and L1917-2037 (invocation.json, monitor_pid.json, `--resume`, LAUNCH_RECORD_MISSING). Tests N18, N20, LIVE.
- §12 bindings: L335-362. Tests S01-S04.
- §13 close and G24 cutoff: L1592-1717; T is the maximum over the set. Tests C01-C14, G01-G02.
- §14 assembly: L1736-1779. Tests R01-R04 and T12, as 0782 ruling 2 directs.
- ROUND5 items:
  - 2: qualified sampler check at L1001-1002 and L1615-1617; test C06_reused.
  - 5: "## A108 continued" is treated as an entry, the same as the kit.
  - 7: the README wording is correct.
  - 9c: a malformed RESIDUAL_RETRY line is caught in status (L1541), launch (L2046) and assembly (L1737).

## Not implemented or not tested
- **A226 item 1:** B1.
- **G25 `complete` definition:** B2. Nothing tests unrelated-process quoting.
- **Kit fill-check port is partial:** the handoff's `root_admission`, `policy_pin`, `driver_acceptance_pin` and `v007_adoption_pin` form (kit L506-509) are not checked. The filler enforces them and the fill receipt pins the handoff, and the brief's §6.6 list is fully covered, so this is non-blocking. I recommend adding them.
- **Entry-heading regex differs from the kit's** (non-blocking, TESTED):
  - P-112's ENTRY_RE (L46) refuses a TOOL_PIN line under `## A231. x` or `## A231(x)` with TOOL_PIN_MISMATCH; the kit's regex accepts both;
  - P-112 also clears the entry state on any `## ` heading that is not an A-entry, where the kit keeps it;
  - it does not bite today because every V006 heading has the `## A###:` form;
  - fix: use the kit's ENTRY_RE (record writer L45) with the kit's carry-forward behaviour, or have root write the adoption heading in the `## A2NN:` form.

## Notes (non-blocking)
1. `sample_value` adds a sixth null case, `n_samples < 2`, plus form checks. It cannot fire on an honest sample. Either disclose it or drop it so c2v007 stays identical.
2. `identify()` checks only absolute `.py`/`.sh` arguments, so relative paths and copies without those suffixes are missed. That is within the disclosed lower bound, but the README should say so.
3. `calls()` needs a full config row (handoff, fill dir, EPS, GQ) for members and F points already carried by S0 serials. Root must fill specs for those too, or status, close-attempt, assembly and launch all refuse.
4. There is a sub-millisecond window between Popen and `monitor_pid.json` with no `--resume` path.
5. The fix should land as a new file; it is root's call whether that means P112_LAUNCHER_CX2V002 with the writer and launcher strings updated. A226 (18:08:58Z) postdates the 0781 start and is not cited in the build report or README.
6. Disclosures:
   - My exclusive `mkdir` of `phase1_ngc_launch_kit_cx2_rootverify_c2` failed. The folder already existed, empty, created at 18:48:50Z by something else after my first check. I wrote only into a new subfolder created by exclusive `mkdir`.
   - The RUN1 log redirects were plain `>` to new files; RUN2's used noclobber.
   - My first probe run (PROBES) had a parser bug in my own probe and is superseded by PROBES2.
   - Looking for 0782, I ran a recursive `ls -R` over UNT_EXCHANGE that listed file names only, filtered to "0782". I stopped it and opened no contents.
   - V006 grew during the review (`57a2c005` → `1f7409b5`). I read A223 and A226 by heading only, and grepped it for TOOL_PIN or RESIDUAL_RETRY line starts (none).
   - No NGC3198 data, run outputs, V007 records, ~/.codex or network. No launch. No fixture processes left running.

## Result files (under `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2_rootverify_c2/VERIFY_C2_20261020T185533Z/`)
- RUN1/TEST_RECORD.json `50e0951bfe19216e143a8e90785e9569a9fd795334acc1a605144df08d1a5e15`
- RUN2/TEST_RECORD.json `50e0951bfe19216e143a8e90785e9569a9fd795334acc1a605144df08d1a5e15`
- RUN1/EXECUTION_METADATA.json `f2c2c77aa5628a0a40e41cc6ea9ba2b0d03747ad8ae7ca597495cb6a58765ca3`
- RUN2/EXECUTION_METADATA.json `61a2590967cdd76a99a0b3790bd2ee2bb54ca65c7a1e26fd87eaa0f48151947e`
- RUN1.stdout.txt `c45101bac0674a7e7db228f6f12c72f68f1bd13ecf88ac3c375289f36c248608`
- RUN2.stdout.txt `66e5ff2a62ca031ec5a8b5f76243f4beb50f49c659fce6f62675a0fabae1779b`
- PROBES2/PROBES_C2.json `a55bbdeed5e730f7561d560381c4d1499d4dbd88327ae9963c04385d604d0d16` (the probe results of record)
- PROBES/PROBES_C2.json `bdbcfbdafeaafacdfb92cd1facb70f9b24674fed68b1eac50aaf54498a27cf69` (superseded)
- probe_c2.py `4d158dd99498a0f55e5c471e0113db1eb86e9258cd0ff79a52049b0399470560`

## Lens 2: adversarial and integrity

**FAIL.** CX2V001 cannot be adopted as built. There are 4 blocking items, each a small local fix, so the next step is a successor build (CX2V002). The rest of the build holds up well under adversarial testing.

**Evidence base**
- **Vendor suite re-run:** I re-ran Codex2's suite in-process twice. Both runs passed 580/580, the case list is identical to their RUN1, and all 229 named refusal codes are exercised.
- **Audit hook:** checking both the path and its realpath, it saw 3,555 opens by P-112 code and 0 forbidden opens. The 6 signals P-112 sent all went to processes the suite started. The CLI and sampler subprocesses were not hooked; they use the same read functions, which I reviewed statically.
- **My adversarial tests:** 25 cases. 11 pass and 14 fail, with identical results in RUN1 and RUN2. No processes were left running.
- **Concurrent writer:** after I created the folder, another process wrote `VERIFY_C2_20261020T185533Z/` into it. Those files are not mine and I did not touch them. Its probes also hit the apostrophe case below.

**BLOCKING**

1. **B1 (A226): the launch record pins launch.json bytes that were never checked.** The checks run on one read (`finish_launch` L1980, or `stop_launch_failure` L1925). `write_launch_record` then reads the file again (L1956, plus L1960 when it did not parse) and records sha256, utc and child_pid from that second read.
   - RV01: with a different second read, the record says CONFIRMED but pins sha `91ab0d11…` instead of the checked `e542bfd1…`.
   - Fix: pass the `(raw, lj)` from `wait_launch_json` into `write_launch_record`. Have `stop_launch_failure` return the buffer it read; in its "exists but unparseable" branch, read once and return that. Delete L1956 and L1960 and pin `sha(raw)`, utc and child_pid from the passed buffer. Add a read-count fixture, an AST check and a re-read mutant, as A222 required.
2. **B2 (A226): a non-attempt is classified on one read of the monitor receipt and pinned from another.** `history` classifies OFF_SPEC or NO_RUN_DIRECTORY from L1469 but pins `pin_of(receipt_path)` at L1474. That pin goes into `status` output and the assembly record.
   - RV02 confirms it.
   - Fix: `guard_read(p); raw = Path(p).read_bytes(); monitor = monitor_receipt(raw); pin = {"path": p, "sha256": sha(raw)}`.
3. **B3 (A226): `--verify` compares one read and reports the pin of another** (compare at L1771, `pin_of` at L1773).
   - RV03: it reports VERIFIED with the sha of different bytes.
   - Fix: `got = read once (guarded); need(got == raw, "REGISTRY_BYTE_VERIFY"); return {"path": str(p), "sha256": sha(got)}`.
4. **B4: one unrelated process with an apostrophe in its command line breaks the sampler.** `ps` prints argv without quoting, so `shlex.split` raises inside `ProcessCounter.count` and P-112 treats that as a ps failure. Effects:
   - Any such process during an attempt sets `complete=false`, so `other_ngc_processes_max` is null and a counted rerun is lost, at about 14 days each (RV12).
   - While such a process persists, the sampler never ends: no `.solo.json`, no 60 s no-receipt rule, and close-attempt refuses SAMPLER_STILL_ALIVE (RV13: 400 polls with no decision).
   - If one is present at the first sample, the launch refuses SAMPLER_FIRST_SAMPLE_FAILED after the registry entry is written, and a solo launch refuses PS_COMMAND_PARSE (RV14).
   - RV11 confirms the real `ps` row form. Shell commands with apostrophes from the Codex and Claude lanes on this machine are a realistic trigger.
   - Fix: make `command_argv` fall back to `row["command"].split()` on ValueError and never raise from `count` for a single row. Keep `complete` tied to the `ps` exit code and `parse_ps` only. Add MUST_PASS tests for each effect above, plus a mutant that restores the raising tokenizer.

**Fixes recommended for the same successor (not blocking)**
- **F1, blinding through symlinks:** several reads skip `guard_read`, so a symlink at a monitor-record path leads P-112 into an outdir.
  - The sites are `history` L1469, `try_launch_json` L1123 (used by the sampler, `finish_launch`, `stop_launch_failure` and `write_launch_record`), sampler L1266/L1290/L1295, `launch_resume` L2023 and `launch` L2083.
  - RV05 (status opened `outdir/finish.json`) and RV06 (`result.json`) show it on synthetic sentinel files.
  - Fix: call `guard_read(path)` and require `realpath == path` before each of these reads.
- **F2, line splitting:** `tool_gate` and `residual_lines` use `str.splitlines()`, so a TOOL_PIN or RESIDUAL_RETRY placed mid-line after U+2028, FF, VT, NEL or a lone CR counts as a whole line. RV08 shows 9 of 9 separators accepted, while the kit parser does not see a pin in the same layout. Fix: use `text.split("\n")` with `rstrip("\r")`, the kit's form.
- **F3, a narrow resume gap (ROUND5 1(b)):** if the invocation dies between starting the monitor and writing `monitor_pid.json`, the call is left with a `.launch.json` and no legal next step. RV21 (live fork) shows resume refuses RESUME_INVOCATION_MISSING; launch, status and close refuse LAUNCH_RECORD_MISSING; a RESIDUAL_RETRY line gives RESIDUAL_RETRY_NOT_RESIDUAL.
  - Fix: let resume accept a work directory without `monitor_pid.json` and find the monitor by command line (`matching_monitors`: one live process, or none), recording where the pid came from. When `monitor_pid` is null, the liveness checks should search by command line.
- **F4, kill-target exit 1:** `kit_kill_target` reads exit code 1 as ALREADY_ENDED. An uncaught exception in the kit, such as a `ps_field` TimeoutExpired, also exits 1, so a live target is reported as ended (RV19). Fix: require the kit's stderr JSON to say `"alive": false`; otherwise record NOT_KILLED_TARGET_REFUSED.
- **F5, the TOOL_PIN gate reads whatever file the config names (lens 4):** the tool has no V006 path constant, so in production the gate passes on any file that contains the pin line (RV24). Fix: carry the V006 path as a constant and require `config["v006"] == V006` when not in synthetic mode. Brief §4 made `v006` a config key, so this is root's call.
- **F6:** add a `V007_POSTSEAL_RECORDS` component check to `path_rules`. Without it, the sampler would hash any `.py` or `.sh` under that folder named in some process's argv.

**Notes**
- **Read inventory:** the dynamic read-site audit over Codex2's own suite independently finds exactly B1, B2 and B3 outside the `pin_of`→`read_pin` pattern. That pattern (about 17 sites) is double-read but fails closed (RV04); one read-and-pin helper would make it cleaner.
- **Cross-process re-reads:** P-112 hash-checks files and then executes them by path in a child process. The driver and monitor are re-attested by the pins in `.launch.json`. The kit kill-target, twin watch, dry harness and memory watch are not. A226 limits the class to two reads in one process, so I treat this as a disclosure.
- **Own sha:** the tool's own sha is a second read of the script that is executing. This cannot be avoided.
- **Sampler procedure:** the literal argv rule counts `grep`, `cat` or `shasum` naming a listed tool as an NGC process. Root and the lanes must not touch listed tools during a solo attempt. A byte copy under a path with spaces, or a relative-path invocation, is not counted; the count stays a lower bound.
- **Stricter than spec, fail-closed:** `RESIDUAL_RETRY_X…` lines refuse MALFORMED, and a `## A230.` heading is not treated as an entry, unlike the kit.
- **Codex2's V03 hook:** it covers only the close-case outdirs and checks path strings, not realpaths.
- **Passed:**
  - TOOL_PIN near-miss matrix (20 cases) and RESIDUAL_RETRY grammar.
  - Reused-PID sampler qualification and wrong-volume checks, including a symlinked volume and a residual on an unmounted kit volume.
  - θ one-ulp and signed-zero checks (15 variants plus F-point cases).
  - MISLAUNCH `--mon-pid` rules.
  - Live recovery after death before the monitor starts.
  - Resume binding to the right invocation.
  - Gate coverage: all 9 writing paths refuse without the pin, and all 4 Popen sites run only after the gate.

**Result files (sha256)**, all in `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2_rootverify_c2/`:
- `adversarial_RUN1/ROOTVERIFY_ADVERSARIAL_RESULT.json`: 678d2c7369df59f7f6f0201528a0ec70ff3be483faf47d99e4d5fd9ac499847a
- `adversarial_RUN2/ROOTVERIFY_ADVERSARIAL_RESULT.json`: 95c21bd88eef68241099f94dbc29da87eb459209169153d2f41d4ab5d8f6e19c
- `vendor_suite_rerun_RUN1/ROOTVERIFY_SUITE_AUDIT.json`: 11ef6858ddaad5337ec03b517bb22d2efebd069c2c4783f8e84eba8e5c66aff0
- `vendor_suite_rerun_RUN2/ROOTVERIFY_SUITE_AUDIT.json`: d85a007849176a57cb4ac0caf015050907af7d2396d8e45b7936b71a1e4a127a
- `STATIC_A226_READ_SITES.json`: f560fa7d16bbaab860fb1e11734a48b47e3c6f33f5a30b925280bbe2f92ffdb9

Harness scripts:
- `rv_adversarial_c2v001.py`: 4e923239fa9df47522abfb1e68995daa9358e4af4036e7d0aae2796119798566
- `rv_suite_audit_c2v001.py`: 91cb40ddc3e7311deb1be1a3d066f865b0f5a934ca3e30fc7e1c2b7035ecbd99
- `rv_suite_audit_c2v002.py`: 450a762d3796de2a68bec5cc9fd9fae3cca62f5fdf81c44dabb72ec0e8d8adec
- `rv_static_a226_c2v001.py`: cb0928c6b9a86b65059f7a4218d83148b3cb5d65af73b74bef1b411440c88c1e

Inputs verified from bytes: tool a72d96c1, tests fd50301b, README 8a6f6604, HASHES 7ec3cb33, brief cddbaa8d, ROUND5 4e3977ab. V006 was read by heading only (A222, A223, A226) at sha 57a2c005…. I did not open NGC3198 data, run trees or outputs, V007_POSTSEAL_RECORDS or `~/.codex`, used no network, and launched nothing scientific.
