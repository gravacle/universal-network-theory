# Operator runbook: prospective SSH stage and recovery

This is a controlled procedure, not a command to execute now. Every italicized
value below is missing until a destination and a specific authorized run are
selected. `POLICY.json` currently says `NO_REMOTE_EXECUTION_AUTHORIZED`.

## 1. Freeze a narrow transfer

Prepare a fresh disposable local staging snapshot or frozen source checkout.
The transfer allowlist is a UTF-8 file containing only sorted, unique,
repo-relative regular-file paths, one per LF-terminated line; no globs,
comments, blank lines, symlinks, `.git`, `.` or `..` path components. Include
the verifier itself.
The list is reviewed against the scientific dependency census and retained
shard seals. The direct V001 L4 runner requires exact Git HEAD
`f5973628fa25c8cc0e2812142e6d8516d0b5d28d`. The V002 wrapper permits a
descendant only if that frozen parent is an ancestor, its tree matches
`be83f661a6e806c61a6291be315bf78b08bbc006`, and frozen dependency hashes
match. Any later runner must declare and authenticate its own source identity.

From the packet directory, after review:

```text
python3 transfer_manifest.py build \
  --root <frozen-local-source-root> \
  --allowlist <reviewed-sorted-allowlist> \
  --output <new-path-outside-source-root>/INPUT_MANIFEST.json
```

The command prints `MANIFEST_CREATED_NO_TRANSFER` and the manifest SHA-256.
Record that digest in the local signed/frozen run authorization separately
from the manifest file. The builder refuses to overwrite an existing
manifest. Re-run source authentication and compare hashes immediately before
transfer; any change requires a new manifest and attempt identity.

## 2. Stage to an SSH machine

Only after the host key has been verified out of band, create a **new** 0700
remote stage and a separate fresh detached Git checkout. Check exact HEAD for
V001, or the frozen-parent ancestor/tree/dependency checks for V002; do not
ship `.git` from the local mixed-custody tree. Use SSH with
`BatchMode=yes` and `StrictHostKeyChecking=yes`. A reviewed `rsync --archive
--files-from=<reviewed-sorted-allowlist>` from the frozen root may copy just
those files into the empty remote stage. Do not use `--delete`, a broad `.`
sync, or a two-way sync. Transfer `INPUT_MANIFEST.json` separately. Paths
containing shell metacharacters require explicit safe quoting; never paste an
unvalidated destination/path into a shell command.

On the remote stage, run the staged verifier with the independently recorded
digest (not a digest read from the remote manifest):

```text
python3 transfer_manifest.py verify \
  --root <remote-empty-stage-root> \
  --manifest <remote-manifest-path-outside-stage> \
  --expected-sha256 <locally-recorded-64-digit-sha256>
```

This strict mode rejects missing/extra files, changed bytes, symlinks, path
traversal, duplicate JSON keys, and malformed manifests. Overlay only these
verified bytes into the *disposable* remote checkout. Then check the same
manifest against that checkout with `--allow-extras`; this mode only allows
other checkout files and still verifies every listed byte and rejects symlinks
on each listed route. The detached commit, authenticated history/shard
contents, and complete dependency census must be checked by the scientific
runner before execution.

## 3. Preflight, bounded execution, and interruption

Write a run authorization recording the input manifest digest, source commit,
code/lock hashes, task plan, destination identity, environment, usable memory,
measured representative peak RSS, enforced job/cgroup memory limit, scratch
limit, worker count, wall estimate, and power/cooling window. If any value is
unknown, the gate fails. Begin with one worker and a synthetic benchmark.
Memory-cap violations must terminate only the remote job, not Codex or the
source machine. Do not rely on `ulimit` alone as a demonstrated process-tree
memory cap for NumPy/BLAS workers.

Each task commits one bounded sector result and receipt, then releases sector
arrays. If SSH drops, first determine whether the remote job is still alive;
do not launch a second controller against the same checkpoint root. On an
orderly SIGINT/SIGTERM the controller journals `RUN_STOPPED` and exits without
`COMPLETE` or final. On hard kill/reboot, resume only after checking there is
no active controller and authenticating the run identity, existing journal,
results, and receipts. Orphan `.tmp` files are not results. V002 has one
narrow crash-window recovery: for a result-only task with no commit journal
entry, it replays that task in a fresh worker and requires an exact match of
the scientific payload (excluding resource measurements) before creating the
missing receipt and appending a recovery journal entry. A replay mismatch,
an unreceipted already-committed result, or any other authentication failure
is fail-closed; preserve the attempt and use a new root after forensic review
rather than editing evidence in place. This recovery has not been tested over
SSH.

Use an explicit `--resume`; never infer completion from the presence of some
sector files. If all sectors were committed just before a signal, a separate
resume is still required to publish `COMPLETE` and final output. Preserve all
failed/stopped attempt logs and resource samples.

## 4. Return and reconcile

On the remote host, form a sorted output allowlist from the exact run identity,
journal, sector results, receipts, `COMPLETE`, final scientific output,
environment record, and resource log. Build a second manifest for that result
directory. Record its digest over the authenticated SSH channel and in the
local run ledger. Pull these files into a **new** local return directory,
never over the source checkout. Verify the exact output manifest there, then
independently verify internal checkpoint/journal/receipt/final bindings and
recompute the final scientific payload from sector results. Only after the
independent hostile/audit lane agrees may any finite result be classified.

The remote host is not a source of authority for changing protocol, thresholds,
historical paths, source seals, or the L6/L8 lock. A successful SSH transfer
is only a custody check. It does not prove a scaling law, geometry, gravity,
or dark-sector physics.
