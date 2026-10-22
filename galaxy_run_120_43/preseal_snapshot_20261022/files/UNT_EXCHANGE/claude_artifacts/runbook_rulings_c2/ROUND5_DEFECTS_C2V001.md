# RUNBOOK rulings + P-112 brief: round-5 checker defects (root workflow wf_0bb1531a, checker-r5). Adopted at insertion as binding build items (V006 A223).

DEFECTS

1. **[LOW-MED] A P-112 launch invocation that stops partway can leave a call with no legal next attempt, and the call is not one of the residuals.**
   - **Case (a): the registry entry is written but the monitor never starts.**
     - Brief §11 writes the registry entry at step 2, then starts the sampler (step 3) and the monitor (step 4).
     - The invocation can end between those steps: the sampler's first `ps` fails (§9 expects that it can), or P-112 refuses or is killed.
     - NAME then has a registry entry and no record of any kind. §6.13 admits an existing entry only "after a monitor refusal", so every launch at k = 1 refuses ALREADY_LAUNCHED or REGISTRY_ENTRY_EXISTS_FOR_ANOTHER_SPEC, permanently.
     - No receipt stdout or stderr exists, so a RESIDUAL_RETRY line refuses RESIDUAL_RETRY_NOT_RESIDUAL.
     - The kit has no such gap: its register admits a same-spec entry whenever no LAUNCH record exists (kit L635-644).
   - **Case (b): `.launch.json` exists but no LAUNCH or MISLAUNCH record does.**
     - The invocation ends after the monitor writes `.launch.json` (root_monitor L148) and before §11.6. That window includes the parse wait of up to 300 s.
     - close-attempt needs exactly one record, so it refuses forever, even after a valid receipt. Launch refuses at §6.10 and §6.13.
     - Neither residual form fits: MONITOR_STARTED_NO_LAUNCH_JSON requires no `.launch.json`, and MONITOR_ENDED_NO_RECEIPT requires a record. So a RESIDUAL_RETRY line is refused.
     - Only a P-112 successor can clear it, on the step-4 path. For a kit call, root still has the kit's `launch-check` and `launch-record` (L1096-1165), but the rulings do not say so.
   - **Fix (a):**
     - Brief §6.13 bullet 3: replace "After a monitor refusal at this k (D7), the existing entry is admitted if … and the only records for NAME are MONITOR_REFUSED records at this k" with "The existing entry is admitted if its spec sha, θ key and V006 pins equal this attempt's, no LAUNCH or MISLAUNCH record of NAME exists, and any MONITOR_REFUSED records of NAME are at this k. The kit's register works the same way (L635-644). §6.10 still requires all five `absent` paths of k to be absent."
     - RULINGS D7 relaunch bullet (L409): add "The same admission holds when a P-112 invocation ended after writing its registry entry and before its monitor started."
     - Add an N04 MUST_PASS: an invocation that writes its entry and exits on a failed first sample; the next launch at k = 1 reports ALREADY_REGISTERED_SAME_SPEC and writes no new entry.
   - **Fix (b), brief §11 and a new RULINGS process bullet ("An interrupted launch, LAUNCH_RECORD_MISSING"):**
     - Before the monitor starts, the invocation writes `<work>/invocation.json` by exclusive create, holding its own pid, sampler_pid and the planned monitor argv. Right after Popen it writes `<work>/monitor_pid.json`. The sampler finds the monitor by its command line (root_monitor with this attempt's `--receipt`), not only by a pid handed to it.
     - Add `launch --resume --name NAME --attempt k`, under the TOOL_PIN gate and the run-volume-first rule. It is admitted only when all three hold:
       - the `.launch.json` of k exists;
       - no LAUNCH or MISLAUNCH record of (NAME, k) exists;
       - the invocation pid is gone (pid and command-line test).
     - It runs §11.5-11.6 against the existing file with the recorded pids. If every launch-side check passes, it writes a LAUNCH record, whether the monitor still runs or its receipt exists (no receipt content is read). Otherwise it applies the §11.5 stop and writes a MISLAUNCH record.
     - `status` reports LAUNCH_RECORD_MISSING. Launch and close-attempt refuse LAUNCH_RECORD_MISSING until the record exists.
     - For a kit call, root runs the kit's `launch-check` and `launch-record`: LAUNCH on a CONFIRMED verdict; otherwise the D7 kit-bullet stop and `--outcome MISLAUNCH`.
     - Add this to the P-112 and root owner rows. Add N20 (MUST_PASS for both cases) and a mutant ("a call left with a registry entry or a `.launch.json` and no legal next attempt").

2. **[LOW] close-attempt's "`sampler_pid` has exited" check can be blocked by a reused pid.**
   - Brief §13 (L370) and C06 use a bare pid. The monitor gets a command-line "gone" test and the twin's watch is qualified ("live kill-watch process"), but the sampler does not.
   - Each sampler starts a `ps` on every poll (≥ 60,480 processes in a 7-day attempt). With several samplers, the macOS pid space (under 100,000) wraps within days, and a host restart resets it. Any live unrelated process holding that pid then blocks the close for as long as it lives.
   - **Fix:** §13: "for P-112 attempts, the sampler has exited: no live process has `sampler_pid` with a command line naming P-112's sampler and this attempt's outdir (the §10 'gone' form)". Add to C06 a MUST_PASS: a synthetic `sleep` holding the reused pid does not block the close.

3. **[LOW] "Run volume first" checks the wrong volume for kit attempts whenever `run_volume` is not External1.**
   - The kit hard-wires its run root one level under `/Volumes/External1` (kit L170, L348). Brief §4 lets root name another `run_volume`.
   - In that case, the mount check before MONITOR_ENDED_NO_RECEIPT, the D7 `absent` checks, the residual checks and close-attempt runs on P-112's volume while the kit's receipts sit on External1.
   - **Fix:**
     - RULINGS "Run volume first" and G16 3; brief §6.10, §10 and §13: "The mount check for an existing attempt is made on the volume that holds its outdir: `run_volume` for a P-112 attempt, and dirname(`s0.run_root`), the kit's External1 (kit L348), for a kit attempt. Each must be mounted and not symlinked."
     - In §13, `run_volume_at_close` records that volume.
     - Add an N19 case: P-112's volume mounted and the kit volume absent gives RUN_VOLUME_NOT_MOUNTED for a kit attempt.

4. **[LOW] Brief §11.5 bullet 1 applies kill-target to a `.launch.json` that does not parse.**
   - kill-target cannot read such a file: `strict_json` raises at kit L932, so the driver is not stopped. Nothing says what happens next. The kit itself records `--stop-result NOT_KILLED_TARGET_REFUSED` (L1222) in this case.
   - The case arises if root_monitor dies or hangs in `_write_x` after Popen (L147-148). The child runs in its own session with no caps.
   - **Fix, brief §11.5:**
     - Split bullet 1. "On a mismatch: kill-target (with `--mon-pid`), TERM, KILL after 15 s, wait up to 60 s for the receipt, then the MISLAUNCH record (A179 R2)."
     - "On a `.launch.json` that exists but does not parse by the bound:
       - if the monitor pid is alive, stop it as in the third bullet;
       - then, if the file parses, run kill-target without `--mon-pid` on its child_pid;
       - otherwise TERM, then KILL after 15 s, the process group of any live group leader whose command line is exactly the planned driver command (`<python> -I -B <driver> run --spec <spec> --outdir <outdir>`), recording the stop result in the kit's form (NOT_KILLED_TARGET_REFUSED when there is none);
       - write the MISLAUNCH record. An attempt with no monitor receipt is MONITOR_ENDED_NO_RECEIPT."
   - **Fix, RULINGS D7 kit bullet:** add the same rule for root ("If `.launch.json` then exists but does not parse …"), using the kit's `--stop-result`.
   - **Test:** add N18 (d): a truncated `.launch.json` plus a synthetic orphan driver.

5. **[LOW] The heading `## A108 continued` is unresolved in both files.**
   - V006 now keeps this unnumbered, unstamped heading last: A222 was inserted above it, at L3182, with the heading at L3204.
   - The kit's ENTRY_RE (record writer L45) parses it as entry A108.
   - Brief §2 tells Codex2 to read "A108" by heading, so it is unclear whether the continuation is in the read list.
   - RULINGS L11 has root confirm "by heading" that it changes no ruling, but the heading names no subject, so a heading read confirms nothing.
   - **Fix:**
     - Brief §2 V006 row: "A108 means the entry under the `## A108:` heading (V006 L20) only. The unnumbered `## A108 continued` heading, kept last in V006, is not in the read list unless root's send note adds it."
     - RULINGS L11: replace "V006 ends with … after A221; it was read by heading only, and its content is not checked here" with "V006 keeps an unnumbered, unstamped `## A108 continued` heading last; new entries, A222 included, are inserted above it. The kit's ENTRY_RE (L45) parses it as A108. At insertion root reads its body, which is root's own text, and confirms it changes no ruling here."

6. **[TRIVIAL] The V006 citation is stale.**
   - V006 is now `511ded6c7b40fba74485b289aa73a531787ac55a540132afebdbcca271b85577`, 287,653 B, written at 17:13:17Z and read at 17:21:09Z.
   - New entry, read by heading: A222. apply_h3_fields c2v005 fails its verifier on the seal-record path, and c2v006 is commissioned. Per the c2v005 docstring, that tool applies the H3 fields to a DDO154 calibration RUN_CONFIG. It is not an NGC launch-path tool and changes no ruling here.
   - **Fix, RULINGS L11:**
     - update the sha, bytes and span to A222;
     - write "A213-A222 change no ruling here";
     - extend the tools sentence to apply_h3_fields c2v005 and c2v006 (h3_campaign_path_c2, DDO154 calibration);
     - start the insertion re-check "after A222".
   - **Fix, brief §2:** update the V006 row to match.

7. **[TRIVIAL] Hold-rule wording drifts from G25 item 5.**
   - RULINGS root-procedures row (L463) says "NGC tools not on the list (adopted after A212)", and brief §9 says the same at L248 and L279.
   - Read as a restriction, that wording narrows G25 item 5 and reading 7: "whenever it was adopted (the list reflects adoptions through A212)".
   - **Fix:** in all three places, write "an NGC tool not on the list, whenever adopted (the list reflects adoptions through A212)".

8. **[TRIVIAL] The brief's stamp is older than its own contents.**
   - Line 1 says `Tue Oct 20 17:05:55 UTC 2026`. The §2 V006 row cites a reading at 17:08:48Z, and the file was written at 17:08:54Z.
   - **Fix:** run `date -u` immediately before writing the successor and use that value (E_STAMP_1).

9. **[TRIVIAL] Small text fixes.**
   - (a) Brief §10 (L291), "admits a further launch at k as it admitted the first relaunch (§6.13)": at k > 1 the relaunch is admitted under §6.12 and numbering. Write "(§6.13 at a first attempt; §6.12 otherwise)".
   - (b) The "Run volume first" lists (RULINGS L391, brief L285) omit the no-run-directory non-attempt test (G27 item 5 bullet 1) that `status` uses for its next legal attempt (§10 item 4). Add "and the no-run-directory non-attempt test".
   - (c) RESIDUAL_RETRY_MALFORMED is specified only for launch (RULINGS L416, brief L301). assemble-registry reads the lines (§14). Write "refuses every launch and assemble-registry, and `status` reports it".

**Checked and found correct**
- **File shas:**
  - RULINGS_FINAL_V005 is `f698defeba2c5128381c1af2c83b4628a6c90d82deb8f2100479c8cd66fc308b` (66,883 B).
  - P112_LAUNCHER_BRIEF_V005 is `29d3c89a1bd715b6c0f96c3c3ea73273df99a8939dfb6049614eef039e267d0a` (71,869 B).
  - All earlier versions (round 0, V001-V004) are unchanged.
- **Pin shas:**
  - All 43 full shas in brief §2 and §9 match their bytes.
  - The RULINGS short shas match: `e92aa30e`, `311ceedd` (the carriers_0606_v001 copy; the parent-folder POLICY_CX3V001 is `4f0d7d03`), `aa50c752`, `0c781a17`, `61bd8a83`, `cd92ef91`, `c64f65a3`.
  - `6f095f64` equals the TSR flag record's `ntest_compare` pin, and `d3859b42` equals the slots pin in all three policies. Neither the compare nor the slots file was opened.
- **Status map and constants:**
  - The map has 54 keys, 2,052 B, sha `c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54`, and class counts 2/4/20/10/17/1.
  - The seed key `968c915b…` equals kit `KEYS['seed']`.
  - The caps match CAPS_S45_C2V003, and the disk and cap arithmetic checks.
- **Checker-r4 defects 1-7:** all applied as written. R1-R6 hold. Root's acceptance of checker-r3 defects 1-5 is reflected in both files.
- **Code citations checked against bytes:**
  - driver L4971-4987, L4981 (`dry-run`), L8994, L9208-9215;
  - kit L318, L348, L635-644, L737-791 (L785-788), L932-959, L1032, L1132, L1222, L1231, L1237;
  - serial script L202-208, L236; twin script L150-155;
  - root_monitor L133, L143-148, L192, L199;
  - c2v006 L1380-1391;
  - record writer L41-45.
- **Pin-parser safety:** no line in either file matches KEYWORD_RE or ENTRY_RE, or begins with TOOL_PIN or RESIDUAL_RETRY.
- **Blinding:** I opened no NGC3198 data, slots, compare, run outputs, V007_POSTSEAL_RECORDS or ~/.codex. I read V006 by heading only and used no network. I wrote nothing under runbook_rulings; a scratch hash script elsewhere in the scratchpad was deleted.

Files reviewed:
- /private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/runbook_rulings/RULINGS_FINAL_V005.md
- /private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/runbook_rulings/P112_LAUNCHER_BRIEF_V005.md