# One-attempt relaunch addendum V002: fixed-probe C_ij L4/L6 census (tasks 0342/0343)

**Status:** proposal only. Custody repair, not authorization for a scientific attempt. A new distinct Codex final review of these exact bytes is required before any run. No automatic retry.

## Why V002 of this addendum
The V003 + outer V001 package received HOLD_PROCESS_CLEANUP (`OWNED_FIXED_PROBE_CIJ_RELAUNCH_V003_OUTER_PRELAUNCH_REVIEW_V001.md`, sha 49b4c8b2…), clarified by `OWNED_FIXED_PROBE_CIJ_MINIMAL_PROCESS_GROUP_REPAIR_CLARIFICATION_V001.md` (sha 8844e6f5…). V003, outer V001 and addendum V001 are preserved unchanged. No V003/outer V001 launch occurred.

## Unchanged
Producer `owned_loop_merger_fixed_probe_cij_census_v002.py` (ff22b231…) and its prospect/addendum pins; L4/L6 cases with four arms; all scientific completion predicates; caps (10 s, 256 MiB conservative combined, 32 MiB output with 1 MiB receipt reserve); one scientific child; exclusive writes; the unused `_V002` wrapper result paths and the unused `_V001` outer-driver capture/receipt paths; the prior failed V001 launch records.

## Changed (process custody only)
1. **Wrapper V004** (`readiness_fixed_probe_cij_root_launch_wrapper_v004.py`, sha 0008c65a765771e70fa6acd6c30ccce880bcb722ecf3b18a02284d293591c370).
   - Producer Popen has no `start_new_session`: producer and `/bin/ps` monitor calls share the wrapper's process group.
   - `stop_child` kills and reaps the direct child (`child.kill()`/`wait`) and records every attempt, error and reap outcome in `child_cleanup`.
2. **Outer driver V002** (`fixed_probe_cij_outer_driver_v002.py`, pins wrapper V004's exact sha above).
   - Wrapper launched with `start_new_session=True`; its PID is the known group.
   - One cleanup routine on every post-Popen path (wrapper exit, timeout, exception, SIGINT/SIGTERM/SIGHUP). It SIGKILLs the known group even when the wrapper leader has already exited, reaps the wrapper, and verifies the group is gone (`killpg(pgid,0)` → ProcessLookupError within 1 s).
   - Cleanup is `confirmed` only when the wrapper is reaped and the group is verified gone. Kill, wait, permission and verification errors are recorded, never counted as success. Unconfirmed cleanup fails the receipt (`process_group_cleanup_confirmed`) and sets `root_attention_required`.
   - Signal handlers never raise; the main path polls (50 ms) and takes the same cleanup. A signal before Popen prevents the launch.
   - No descendant scan, no PID handoff.
   - `outer_elapsed_seconds` is renamed `wrapper_lifetime_seconds`: from just before Popen until the wrapper is observed exited. Group verification, terminal-receipt reading/hashing and the outer receipt write follow it. It is not the total driver lifetime.
   - Residual, stated: SIGKILL of the driver itself cannot be handled. The wrapper's own 10 s wall cap still stops the producer, and the missing outer receipt is itself a failed launch.

## Root launch procedure (one attempt)
1. Place the reviewed V004 at `CODEX1/readiness_fixed_probe_cij_root_launch_wrapper_v004.py` and outer V002 beside it. Bytes must match the pins.
2. Ensure `/bin/ps` is permitted (otherwise V004 fails cleanly before creating files, as V003 did).
3. Run exactly once:
   `python3 fixed_probe_cij_outer_driver_v002.py <NEW final Codex prelaunch review of V004/outer V002> <its sha256>`
   The review argument must be that NEW distinct final review, which the wrapper pins into its inputs. It must NOT be the V002 wrapper review (`OWNED_FIXED_PROBE_CIJ_WRAPPER_V002_FINAL_PRELAUNCH_REVIEW_V001.md`), nor the V003 HOLD review (49b4c8b2…), nor the clarification (8844e6f5…).
4. Acceptance requires both an outer receipt COMPLETED_WITHIN_ENVELOPE and the separate saved-result review. Any FAILED or `root_attention_required: true` outcome is preserved as adverse evidence; no rerun without a new reviewed proposal.

## Dummy-only validation (scratch copies; real producer never imported, compiled or executed)
| # | Scenario | Outer result | Cleanup | Leftover processes |
|---|---|---|---|---|
| 1 | ok | COMPLETED (lifetime 0.06 s) | confirmed (group already absent) | 0 |
| 2 | `/bin/ps` denied | FAILED; wrapper rc 2, no wrapper files | confirmed | 0 |
| 3 | slow producer, wrapper wall 2 s | FAILED; wrapper stopped child (`child_cleanup` kill_sent, reaped, rc −9) | confirmed | 0 |
| 4 | hung producer, wrapper wall 60 s, driver wall 3 s | FAILED (timeout); group SIGKILL | confirmed | 0 |
| 5 | wrapper leader exits right after launch, producer hangs in group (0343 case) | FAILED; group killed although leader had exited | confirmed (kill_sent true) | 0 |
| 6 | SIGINT to driver at 1.5 s | FAILED (driver_error Signal 2) | confirmed | 0 |
| 7 | SIGTERM to driver at 1.5 s | FAILED (driver_error Signal 15) | confirmed | 0 |
| 8 | injected PermissionError on every `killpg` | FAILED; `process_group_cleanup_confirmed` false, `root_attention_required` true; errors recorded for kill, wait and verify | NOT confirmed | 2 at receipt time (test work then stopped by its own wrapper wall cap) |

Test copies differ from the deliverables only in root path, wall values, dummy pins and the named TEST-ONLY injections (5: `os._exit(3)` after producer launch; 8: `os.killpg` replaced). These are control-flow checks, not proof of every failure branch.
