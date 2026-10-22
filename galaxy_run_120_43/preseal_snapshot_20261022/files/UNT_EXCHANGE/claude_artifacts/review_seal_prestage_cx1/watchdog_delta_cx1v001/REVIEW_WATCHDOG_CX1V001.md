# Provisional disk-watch review — five convenience findings

date -u: Sun Oct 18 23:02:28 UTC 2026

**REVIEW COMPLETE WITH FINDINGS. Five SHOULD_FIX findings in the convenience watchdog/test. Zero seal blockers are asserted: this tool is outside the seal.**

TESTED: 25 bounded expected-behavior controls: 15 pass and 10 demonstrate the five defects below. Both saved scripts pass bash syntax checking. Neither original script was executed. Runtime checks used only exact source slices; the notification command was replaced by an explicitly owned shell-function double, and timeout controls killed only their own synthetic children.

## WD01 — A value-taking option at the end of argv hangs in the argument loop.

SHOULD_FIX; watchdog lines 28-34. TESTED: each of --log, --threshold-gib, --interval-s, --max-polls and --df-stub timed out in the exact leading source slice; subprocess.run killed each owned test child after 0.4 seconds. Failed shift 2 leaves argv unchanged.

Suggested correction: Check argument count before shift and refuse missing values with exit 2.

## WD02 — Lexical log restrictions can be bypassed through a symlinked parent directory.

SHOULD_FIX; watchdog lines 41-47. TESTED: a direct owned inert runs_ext fixture path refused, but an innocent-named symlink to that same owned fixture allowed log creation. No real excluded tree was accessed. Existing file and final-component symlink controls preserved prior bytes.

Suggested correction: Use a verified no-follow parent traversal and exclusive descriptor-based log creation; retain the verified descriptor for writes, or use the existing reviewed path helper contract.

## WD03 — Digit-only validation permits invalid octal and overflowing threshold arithmetic.

SHOULD_FIX; watchdog lines 40,66,75. TESTED: exact arithmetic accepts ordinary 80-GiB boundary controls, but 080 causes an arithmetic error; 8796093022208 wraps when multiplied by 1048576 and suppresses the expected low-space decision. STATIC ONLY: interval zero is accepted and would remove the intended poll delay.

Suggested correction: Normalize bounded decimal values, require positive interval and threshold, and bound the multiplication before use. Retain max-polls zero only as the documented unlimited sentinel.

## WD04 — The notification self-test exits successfully after the notification command fails.

SHOULD_FIX; watchdog lines 49-56. TESTED with exact function and test-notify branch: an owned shell-function osascript double returned 7; the log recorded rc=7, but the branch exited 0. The matching rc=0 control passed. No real AppleScript or notification ran.

Suggested correction: Return the notifier status after logging and propagate it from test-notify; continuous operation may log and continue with explicit degraded status.

## WD05 — The author test exits successfully when its accumulated status is failure.

SHOULD_FIX; author test lines 59-60. TESTED using only the exact final status slice: ok_all=0 printed SOME FAIL but exited 0 after the final echo. The ok_all=1 positive passed. The author test itself was never run.

Suggested correction: Exit nonzero after printing the output path whenever ok_all is not 1.

## Scope and pending work

UNTESTED: full continuous watchdog, actual df and notification/sound, production paths, scientific outcomes and seal execution. The default 80 GiB is documented and alerts earlier than 80 decimal GB; no defect is inferred from that stricter threshold. Final current selection and author successors still need their own delta review. Earlier provisional v003 and pre-stage conclusions are unchanged. No original script or author test ran, no background watcher started, and no real restricted path was accessed. All fixtures are immutable new review artifacts; there was no deletion, move, rename or overwrite. Isolated Python, nice >=10 and single-thread BLAS applied.

## Byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0642_2026-10-18_claude3_script_add_RP_S1_W7_S1.md` — SHA256 `b96f14fb3116cb277ff4b14ebf7e51f0c73ad8de1333464aa783cd799ad9ea74` (815 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0094_2026-10-18_start_watchdog_convenience_delta.md` — SHA256 `6a59e2894a2868eba597f8833603ca6f3c6d0cc585108d9259f0568d103cf950` (1474 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/step2_disk_watch.sh` — SHA256 `bd0d9bab0854627957781e1666c7f5eacd1e10cd03bfde0dd2efe2e27a5a2c28` (5301 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/tools/test_step2_disk_watch_c3sa_c3v001.sh` — SHA256 `696bfc9b3bb4e514dad0aac0c304d390f5044b39b1b59c3c1cbf0cf8375ecfe4` (6438 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/SNAPSHOT.json` — SHA256 `3d4fc0db31fb4e323a929e995cde3d6b8978e32f1a0b5ed9a4a4a4ea3f2e55b1` (876 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/watchdog_source.sh` — SHA256 `bd0d9bab0854627957781e1666c7f5eacd1e10cd03bfde0dd2efe2e27a5a2c28` (5301 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/author_test_source.sh` — SHA256 `696bfc9b3bb4e514dad0aac0c304d390f5044b39b1b59c3c1cbf0cf8375ecfe4` (6438 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/review_watchdog_slices_cx1v001.py` — SHA256 `a1f41b0207a7aeadc7e931acddf10b539b1025bba5987a4600bb1807facdbb90` (5019 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/SLICE_RESULTS_CX1V001.json` — SHA256 `ecebe51d52223ae85ea2461601224ba43c1a3f550d6cd14f5dd578fe4eea6768` (3946 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/review_watchdog_status_slices_cx1v001.py` — SHA256 `57f22e6d39a091cbb3ea41b4b7970793a3e979b5ec5fba400e1fbcc183048bbe` (2644 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/STATUS_SLICE_RESULTS_CX1V001.json` — SHA256 `98fe70dafbf51effd75a1f6f07c00dc0fb569b2cca8572326f59a667c33909ad` (1381 bytes).
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/REVIEW_WATCHDOG_CX1V001.json` — SHA256 `a028bedb5d90e483a335bdd84b4943bfdd295b4e864aa766c965b0fc96cd86d2` (7226 bytes).
