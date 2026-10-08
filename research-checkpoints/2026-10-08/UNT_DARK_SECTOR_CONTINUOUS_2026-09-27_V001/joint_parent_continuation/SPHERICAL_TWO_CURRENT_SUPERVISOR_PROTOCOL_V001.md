# Two-current custody/resource supervisor V001

This is an additive root-only execution and generated-output wrapper. It does
not alter or import the held scientific producer, its design, numerical gates,
12-case census, finite-R physics, or output scope. No producer or wrapper was
executed by its author. Only AST/source inspection is permitted before root
review and freeze. The root remains the sole scientific runner.

## Inputs and commands

The source pins the exact solver, design, numerical protocol, independent
scope preflight and existing `run_scientific_case_v001.py` no-overwrite
publisher. It loads only that publisher's definitions under a non-main name;
the publisher's scientific entry point is not called. The controller freeze
also binds its own source/protocol and the resolved Python executable bytes
and version. No compiler, installer, shell, network or new directory is used.

Run from the owned project root with the chosen existing Python runtime:

```
python -B .../spherical_two_current_supervisor_v001.py freeze
python -B .../spherical_two_current_supervisor_v001.py run-case 0
```

Only after inspecting the successful case-0 benchmark may root invoke cases
1..11 individually. The wrapper enforces a complete, authenticated successful
case-0 science/resource receipt for all later cases. It never queues the rest.
The root may stop after any case. All invocations remain serial root actions.

`freeze` invokes only the unchanged producer's custody-only `freeze` entry,
not `run_case`. It authenticates every returned project-relative member and
the exact 12-case census, and pins the reviewed source/design/protocol bytes.
It first publishes `SPHERICAL_TWO_CURRENT_V001_FREEZE_RUN.json` containing
the complete invocation. On success it publishes the producer's exact raw
stdout as `SPHERICAL_TWO_CURRENT_V001_FROZEN.json`, then the separate
`SPHERICAL_TWO_CURRENT_SUPERVISOR_V001_FROZEN.json`. All must be absent first.
JSON is parsed for checks but the producer's freeze bytes are not reserialized.

## Prospective resource limits

Case 0 is a technical sizing benchmark limited to 180 seconds wall time and
1 GiB (1,073,741,824 bytes) sampled summed RSS of its own process group. The
same limits apply to each later case in this wrapper; a larger limit would
require a separately reviewed additive version, not a runtime override.
The custody-only freeze is subject to these same ceilings.

The child uses `start_new_session=True`, no input, captured stdout/stderr,
the exact frozen Python path, and explicit one-thread environment settings.
Python path/home/startup/inspect overrides are removed. A 0.2-second watcher
reads `/bin/ps -axo pgid=,rss=` and sums only the just-created child's private
process group. RSS is sampled, not a hard address-space allocation ceiling;
an overshoot between samples is possible. Monitor failure is a retained
technical failure, not successful qualification. The supervisor's capture
memory is separate from this sampled child-group measure. Scientific self
RSS, where emitted by the unchanged producer, is retained independently.

At the wall/RSS limit or interruption, signal only that owned process group:
TERM, at most 3 seconds grace, then KILL if necessary. Pipe draining continues
to EOF; an exit-before-signal race is harmless. The wall limit is a technical
stop trigger, not a claim that process teardown and durable publication finish
within 180 seconds. There are no retries, shortened scientific trajectories,
changed timesteps, numerical clipping, or resource-based favorable selection.

## Durable evidence and failure semantics

Each `run-case i` first authenticates the controller freeze, exact producer
freeze and all ancestry. Existing output/receipt/intent (including a dangling
link) is refused before launch. A durable `..._CASE_iii_INTENT.json` is
published before the child starts; freeze has a separate
`SPHERICAL_TWO_CURRENT_V001_FREEZE_INTENT.json`. An orphaned intent after a
host crash prevents an unknowingly repeated invocation and requires explicit
review/recovery, not deletion or automatic retry. The invocation receipt is
`SPHERICAL_TWO_CURRENT_V001_CASE_iii_RUN.json`; it preserves complete raw
stdout and stderr as base64, their sizes/hashes, literal argv/root, process
return code, exception, wall time, sampled group peak RSS, monitor errors
and stop reason. No truncation or output-tail-only capture is allowed.

The unchanged science JSON must bind the exact requested case dictionary,
producer freeze SHA and canonical finite payload SHA. A valid scientific
failure is retained, never converted to success. The wrapper status is
`CASE_COMPLETE` only for a clean invocation and the producer's complete
finite-R numerical-case status with an empty failure list. Otherwise it is
`CASE_FAILED_RETAINED`, returning nonzero. It preserves the original scientific
status and flags; even a completed case is not spatial/GR/lensing qualification.

The receipt is published first, before the exact unmodified producer stdout
at `SPHERICAL_TWO_CURRENT_V001_CASE_iii.json`. The latter is published whenever
its custody/schema/input checks pass, including valid failed-science JSON.
Malformed/partial stdout after a watchdog stop remains fully in the receipt,
not mislabeled a scientific result. Input mutations detected after invocation
also retain the receipt but prevent raw scientific publication/qualification.

The pinned publisher writes an exact temporary in the intended directory,
fsyncs it, atomically hard-links to the new destination without overwrite,
fsyncs the directory, then removes only its exact redundant temporary. It
rejects symlink ancestry and project escapes. A publication failure preserves
the exact pending artifact; no broad cleanup occurs. A host crash or an
unrecoverable filesystem error cannot be guaranteed a complete receipt. A
crash between receipt and raw publication is recoverable from the receipt's
exact base64; root must inspect and explicitly restore that output, not rerun
the producer. Existing failed receipts require a reviewed separate attempt,
not deletion, overwrite, hidden resume, or automatic retry.

Successful publication prints only a compact receipt/path/hash/resource
summary, preventing the earlier host-output truncation without changing the
stdout-only scientific producer. Frozen source files are never written.
