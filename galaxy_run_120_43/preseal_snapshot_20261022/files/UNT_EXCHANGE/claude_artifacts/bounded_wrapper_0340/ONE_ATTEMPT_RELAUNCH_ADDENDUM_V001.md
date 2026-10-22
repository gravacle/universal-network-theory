# One-attempt relaunch addendum: fixed-probe C_ij L4/L6 census (task 0340)

**Status:** proposal only. Codex must review it separately before any run. No automatic retry.

## What failed (infrastructure, not science)
- The reviewed V002 wrapper (sha d5b1c774…) was launched once by root.
- It failed immediately with a sandbox `PermissionError: [Errno 1] Operation not permitted: /bin/ps`, raised from the RSS monitor.
- The scientific child was killed before any stdout or scientific output. No numerical result exists.
- Records: root reading `READINESS_FIXED_PROBE_CIJ_L4_L6_FAILED_LAUNCH_ROOT_READING_V001.json` (sha 8af1289c…), primary receipt (sha 3a4f6d87…), terminal receipt (sha 75304942…). All V001-suffixed files are preserved unchanged.

## What is unchanged (frozen science)
- Producer `owned_loop_merger_fixed_probe_cij_census_v002.py`, sha ff22b231…, with its prospect and addendum pins.
- Cases L4/L6 with four arms.
- All scientific completion predicates.
- Caps: 10 s wall, 256 MiB combined conservative RSS, 32 MiB output (1 MiB receipt reserve inside it).
- One scientific child. Group kill. Exclusive writes.

## What changes (custody/environment only)
1. **Wrapper V003.**
   - Results move to unused `_V002` suffixes.
   - A documentary `/bin/ps` self-PID preflight runs **before** any output file or child exists. If the monitor is inaccessible, the wrapper prints `FAILED_MONITOR_PREFLIGHT` and exits 2 with no files created (verified with a dummy).
   - A SIGTERM handler kills the scientific child group, so an outer terminate leaves no detached work.
   - The measurement-scope wording follows the V002 final review.
2. **Outer driver V001 (new).**
   - Measures the whole wrapper process with `time.monotonic`, start to exit, against a 10 s timeout.
   - Writes one exclusive outer receipt.
   - Acceptance requires all of: wrapper exit 0; no timeout; outer elapsed ≤ 10 s; terminal receipt COMPLETED with all predicates true; primary pin matching; driver peak + inner conservative peak ≤ 256 MiB; inner total-created bound + driver capture files + 64 KiB ≤ 32 MiB.
   - On timeout it snapshots descendant process groups, sends SIGTERM to the wrapper, waits up to 1 s, then SIGKILLs every group.
   - Tail scope: only the outer receipt's construction and write (≤ 64 KiB, bounded in bytes) follow the final measurement.
   - The exec tool's `wall_time_seconds` (wait latency) is **not** used as process evidence.

## Root launch procedure (one attempt)
1. Place the reviewed V003 at `CODEX1/readiness_fixed_probe_cij_root_launch_wrapper_v003.py` and the driver beside it. Their pinned bytes must match: the driver pins V003's sha256.
2. Request sandbox permission for `/bin/ps` through the app's normal mechanism. Without it, V003 now fails cleanly before creating anything.
3. Run `python3 fixed_probe_cij_outer_driver_v001.py <V002 final prelaunch review path> <its sha256>` exactly once.
4. Acceptance needs **both** an outer receipt with COMPLETED_WITHIN_ENVELOPE **and** the separate saved-result review. Any FAILED outcome is preserved as adverse evidence; no rerun without a new reviewed proposal.

## Validation (dummy-only, scratch)
| Scenario | Outer result | Notes |
|---|---|---|
| ok | COMPLETED (0.09 s) | |
| ps denied | FAILED | no wrapper files created |
| slow producer | FAILED at 10.04 s (timeout) | no leftover processes |
| hung child with wrapper wall 60 s | FAILED at 10.04 s | child group killed; no leftovers |

The real producer was never imported, compiled or executed.
