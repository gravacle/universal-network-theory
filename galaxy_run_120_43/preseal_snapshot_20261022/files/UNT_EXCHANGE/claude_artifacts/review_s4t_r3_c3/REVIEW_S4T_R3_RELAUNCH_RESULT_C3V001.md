# Claude3 direct lens: S4T R3 relaunch packet (0761; A195/A197). Verdict PASS

Packet: CLAUDE2/V007_STEP2_LAUNCH_ROOT/S4T_R3/. SHA256SUMS 08e117d3: 6/6 verify from bytes (plan 07311ded, script c18ebbdf, leaf diff 63e571ca, README b5db31cd, generator c0de839e, dry-run record 3721b25d).

1. Leaf diff (TESTED: my own JSON walk of the S4T call in R2 plan 44b55a7e, at claude_artifacts/v007_launch_packet_cx1/P128/, against R3 plan 07311ded).
   - The call differs only in: argv/11 outdir and argv/13 receipt (_R2 -> _R3), argv/15 wall cap 68400 -> 792000, monitor_log, outdir and receipt (_R2 -> _R3), and wall_cap_hours_proposed 19 -> 220.
   - These are equal: the spec (8e71be9b), the RSS cap 137438953472 (argv/17), the driver and the monitor.
   - At plan level: calls = [S4T], order = [S4T], launcher_log = null, and the s4t_r3 block is added. Nothing else differs.
   - The script also asserts at run time that the call equals R2's S4T call with only the declared leaves replaced (x == y), and that monitor_argv equals the launcher formula.
2. Launcher equivalence (FORMAL). The start is the same as route_a_token_launcher_cx1v007 (861bba68) L163-167: Popen(['/usr/bin/nohup'] + monitor_argv), stdin DEVNULL, stdout = the monitor log opened 'xb', stderr STDOUT, start_new_session=True, env = os.environ + the four BLAS vars = '1'. Admission is immediate, as the launcher's first-case rule (L153-154).
3. --dry-run launches nothing (FORMAL).
   - It runs: the published-sha checks, the plan validation (asserts only; no open-for-write, no Popen), the df and mount reads, and the ps check of the disk watchdog.
   - It imports the launcher only to call validate(). The launcher's main is guarded by __name__ and its module scope has no side effects. validate() refuses with TEN_DISTINCT_CASES_REQUIRED, as expected.
   - It then exits 0 before the T0 or start block. The REC/START existence checks are skipped in dry mode.
Notes (none blocking):
- N1: DISK_WATCH_PID=3385 is hard-coded. If the watchdog was restarted under a new pid, the script refuses (fail closed).
- N2: README section 7 item 1, the direct-monitor start against RUNBOOK_V008 item 4, is root's ruling (A195/A197).
- Nothing under the R2 run's stages/ was opened, and nothing was launched.
