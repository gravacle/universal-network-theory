# Claude3 direct lens (A175): S0 launch kit C2V002 -> C2V003A delta review. Verdict PASS, 0 blocking (A115)

Object: claude_artifacts/s0_launch_kit_c2/, HASHES_S0_KIT_C2V003 61a03d00 (17/17 entries verify) and HASHES_S0_KIT_C2V003A 5e4e9eeb (18/18 verify). s0_kit_c2v003a.py fdc0ee6c, launch_s0_serial_root_c2v003a.sh 621263a2, launch_twin_root_c2v003a.sh f199544d, twin_kill_watch_c2v003a.sh a3d70bec, record writer a10965b7 (unchanged), tests f5d79dcb.

TESTED
- patch: DIFF_S0_KIT_C2V002_TO_C2V003 (5 files) and DIFF_S0_KIT_C2V003_TO_C2V003A_R1 99e838f7 (6 files) each rebuild the target bytes exactly.
- bash -n passes on all 3 scripts; each sets -euo pipefail and noclobber.
- N1 parse wait, on a byte copy in a sandbox with the bound patched to 3 s: empty then written -> PARSED; partial then complete -> PARSED; never written, absent, or written after the bound -> NOT_PARSED_AT_BOUND; complete at the first poll -> PARSED, 1 poll. 6/6.
- launch_checks: an honest serial and an honest twin record pass. RSS of the other call or the C2V002 RSS -> [caps, rss_cap_is_call_cap]; retries 1 -> retries_0; another outdir -> command_is_planned; launch before M-15 -> m15_record_precedes_this_launch; wall + 1 -> caps. 14/14.
- Root's two record runs (RESULTS fe30d047, fcb9d15c): identical 115 rows, 28/28 MUST_PASS, 84/84 MUST_FAIL and 3 OBSERVED, including N01-N06, C01-C08 and P01-P08. Not re-run here: the suite needs /bin/ps (setuid; it cannot run under sandbox-exec) and stats External1.

FORMAL
- Caps: serial 610324 s / RSS RAM 137438953472 / output 146028888064 B; twin 22752 s / RAM x 11 / 34359738368 B. TWIN_TREE sums to 11 and is checked at validate.
- Serial order is unchanged apart from A166/N1: validate -> M-15 first -> order-check -> fill + fill-check -> fresh dry plan -> register -> driver and monitor sha + D3 argv -> External1, disk guard, step-2 receipt, watch -> V006 freeze -> launch -> launch-check -> LAUNCH or MISLAUNCH.
- Removed: admission, gate-cli, confirm-kind, wave-state, twin-start-check and the A133 rule. The spec-sha and leaf checks survive in fill-check, launch_checks and kill-target.
- root_monitor ba031c23 writes rss_cap_bytes as an int (argparse type=int, L233) and the wall cap as a float, so the honest path passes.

NOTES (none blocking)
- R2 (ruled by root): a record still unparseable at the bound reads MISLAUNCH, but the kit cannot stop that run. The operator must watch for exit 5 with launch_record_parsed_within_bound false and stop it by hand.
- LAUNCH_CHECK_ERROR: any exception inside launch-check reads MISLAUNCH, and the script stops the run. This fails closed, and attempt k+1 recovers.
- Carried over from C2V002 (0233), unchanged: N2 (the M-15 freeze starts at attempt 1; 0736 covers it), N5 (a silent kill-watch exit), N6 (the synthetic --launch rows stat External1), N7 (the 120 s existence wait -> exit 5), --watch-poll-s 0 still allowed, N10 (the V007 pin is checked for form only), N11 (the A157 fields are bound only through the V006 sha).
- Closed since C2V002: N1 (A166 freed the twin after the seed), N3 (successor on demand, 0736), N4 (no V006 write rule, 0736), N8's empty-timeout case (the option is gone), N9 (C5: one kit version per launch root, fail closed).
