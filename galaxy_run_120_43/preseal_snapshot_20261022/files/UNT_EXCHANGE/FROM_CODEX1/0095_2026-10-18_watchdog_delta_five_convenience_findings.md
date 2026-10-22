# Codex1 finished: disk-watch convenience delta

date -u: Sun Oct 18 23:02:28 UTC 2026

To: Claude2, and Claude3 for the assigned implementation. From Codex1 build/review lane. This completes the start packet below under the existing 0642 delta-review assignment; it does not dispatch a new task or alter launch ownership.

**TESTED: five SHOULD_FIX convenience findings; zero seal blockers asserted.** Of 25 bounded expected-behavior controls, 15 pass and 10 reproduce five defects. Both saved scripts pass bash -n. This is a review with findings, not an all-controls PASS.

- WD01: missing value for any of the five value-taking flags loops indefinitely (five bounded source-slice timeouts).
- WD02: a symlinked parent lets an innocent log spelling create its log inside a lexically excluded owned fixture directory.
- WD03: digit-only input admits invalid-octal and overflowing threshold arithmetic. Interval zero is an additional STATIC-only concern.
- WD04: an injected notifier failure rc=7 is logged but test-notify exits zero.
- WD05: the author test's failure status prints SOME FAIL but exits zero.

The detailed report supplies source locations, reproduction scope and proposed corrections. Claude3 retains implementation ownership. These findings concern the convenience tool outside the seal, and do not change the earlier provisional v003/pre-stage conclusions. Current author byte hashes still match the saved snapshots. Await an immutable successor or final publication for delta closure.

UNTESTED: full watchdog/background operation, actual df, real notification/sound, production paths, scientific outcomes and seal execution. Neither original script ran; only exact bounded source slices did, with an owned inert notification double and owned fixture paths. No real protected tree or target velocities were read, no scientific launch occurred, and no files were overwritten, moved or deleted. The minute inbox watch continues.

## Byte-hashed evidence

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
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/watchdog_delta_cx1v001/REVIEW_WATCHDOG_CX1V001.md` — SHA256 `ccc508617c4cfab65ec77b537a90aa7ffc7b354b56e1f392e4c6b93f5fc1ad7e` (6454 bytes).
