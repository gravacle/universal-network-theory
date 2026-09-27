# SSH remote-compute and restart contract V001

Date: 2026-09-27. Status: `NO_REMOTE_EXECUTION_AUTHORIZED`.

This is a preparation packet, not evidence of an SSH connection or a remote
calculation. The user selected SSH as the transport for memory-heavy work but
has not yet supplied a destination, remote scratch path, host-key fingerprint,
or measured machine capacity. No host was contacted and no L6/L8 calculation
was run.

## Scope and custody

Codex may remain on the current machine while an SSH-accessible machine runs a
bounded, approved numerical job. Inputs move **one way** from a frozen local
snapshot to a fresh remote stage. Results return to a **separate** local
receipt directory. Neither direction is a bidirectional repository sync. In
particular, the source checkout's approximately 73 GiB of mixed-custody
untracked/ignored material must not be copied wholesale, cleaned, or treated
as disposable. Only reviewed exact relative paths on a run-specific allowlist
may be staged. No `rsync --delete` or in-place reverse sync is permitted.

The direct V001 target runner requires exact Git HEAD
`f5973628fa25c8cc0e2812142e6d8516d0b5d28d`. The V002 wrapper instead
accepts a descendant checkout only when that frozen parent is an ancestor,
its tree is `be83f661a6e806c61a6291be315bf78b08bbc006`, and every frozen
dependency hash matches. Both routes also authenticate repo-relative engine,
history, baseline, and retained shard files. A bare tarball of the packet is
therefore not a runnable remote environment. The remote execution root must
be a **fresh, detached, verified checkout** of the exact base commit for V001
or an authenticated descendant for V002, with an explicitly hash-verified
overlay for prospective/untracked code and the exact sealed retained shards.
Historical absolute paths in history files are provenance and are never
rewritten. Neither runner's portability on another machine has been tested.

`POLICY.json` is the machine-readable lock state. `transfer_manifest.py` builds
or checks an exact SHA-256/byte-count census; it does not transfer or execute
anything. `test_transfer_manifest.py` exercises negative cases.

## Admission before any remote numerical run

1. Record `user@host` or an SSH config alias, a user-owned 0700 scratch path,
   and a host-key fingerprint verified through an independent trusted channel.
   Use batch SSH with strict host-key checking. No password or private key is
   placed in the repository or transfer manifest.
2. Freeze a run-specific source/input allowlist and the complete task plan.
   Include the runner, runtime, durable-evidence module, engine imports,
   historical source/history/baseline, all input shards actually read,
   protocol/policy, and manifest verifier. Authenticate each input against its
   existing scientific seal **before** constructing the transfer census.
3. Verify the remote checkout commit and overlay bytes; record Python, NumPy,
   SciPy, BLAS/LAPACK, OS/architecture, byte order, CPU count, cgroup/job limit,
   available RAM, scratch quota, and a pinned dependency lock. A numerically
   compatible environment must be demonstrated, not assumed from successful
   imports. The present dependency lock is absent.
4. Run synthetic and deliberately interrupted/resumed tests on that host.
   A last-in-flight-unit signal must leave no `COMPLETE` or final output, even
   if the worker returned a sector. A reboot or hard kill may leave orphan
   temporary files, but cannot promote partial output. Explicit resume must
   verify every committed result, receipt, and journal entry before scheduling
   only missing units. V002 may recover an unjournaled result-only task solely
   by re-executing that task and matching its scientific payload exactly before
   creating the missing receipt and recovery journal entry. Changed code,
   input, configuration, task plan, or environment identity must refuse resume.
5. Benchmark a representative *non-production* unit on the candidate host and
   record measured peak process-tree RSS, wall time, checkpoint/output growth,
   and power window. Set a real enforced memory cap at least 1.5 times the
   measured peak, below usable RAM after OS/other-work reserve. Set disk and
   wall caps with measured headroom and an initial worker count of one. Revise
   the estimate before increasing concurrency or moving from L6 to L8.
6. Obtain the frozen independent scientific agreement and restart gate for the
   exact production runner. L6 and L8 remain locked in this policy. L8 cannot
   start before an accepted L6 result and a revised L8 resource estimate.

The local L4 target's physics reproduction is not a remote benchmark or a
remote restart proof. The V001 inherited resume path has known custody gaps;
the prospective V002 hardening must be independently tested and frozen before
it can satisfy step 4. No dark-sector/cosmology work is authorized by this
contract; its separate prerequisite audit remains `NO_GO`.

## Durable execution and return

Partition by deterministic `(L,event,resolution,q_out,branch)` tasks. The
worker keeps only the current sector and bounded reduction state in memory;
after each sector it writes an immutable result atomically, fsyncs it and its
parent directory, then writes a receipt binding raw result SHA-256, scientific
payload SHA-256, task identity, and run identity. An append-only journal records
bound/start/commit/stop/resume/complete transitions. A signal always produces
`STOPPED`, including if the final unit finishes before the signal is handled.
Only a later explicit resume may publish `COMPLETE` and a final result. V002's
limited crash-window replay is not permission to accept a mismatched,
already-journaled, or otherwise unauthenticated result.

At completion, independently reconstruct the final scientific payload from
the authenticated per-unit files. The `COMPLETE` record, journal, receipts,
result census, and final output must agree exactly. Pull a separately
allowlisted result bundle into a new local directory, verify its exact transfer
manifest and every internal binding, then perform independent target/audit
scientific reconciliation. A transfer hash verifies bytes in transit; it is
not by itself proof that the computation or scientific model is correct.

See `RUNBOOK.md` for the staged procedure. This packet does not unlock L6/L8,
publish a result, or change any historical seal.
