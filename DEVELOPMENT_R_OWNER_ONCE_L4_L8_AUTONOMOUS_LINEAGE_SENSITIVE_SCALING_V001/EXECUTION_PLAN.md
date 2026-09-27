# Exact target execution and resource plan V001

## Current disposition

| Stage | Status | Next authority |
|---|---|---|
| Input/source authentication | PASS | none |
| Explicit-density synthetic tests | PASS, 6 tests | none |
| Dense L4 target reproduction | PASS | independent audit required |
| Deliberate interruption/resume equivalence | PASS | independent audit still required |
| L6 execution | PROHIBITED | L4 independent agreement + resume gate + reviewed estimate |
| L8 execution | PROHIBITED | completed L6 target/audit + revised estimate |
| Curvature response adapter | NOT PRODUCED | completed all-event L8 target/audit agreement |

No L6/L8 execution command exists in V001.  Authorization requires a new
source freeze rather than a flag change or manual call into an internal
function.

## Exact later schedule

1. Freeze the separate audit packet before it reads this target result.
2. Reproduce L4 through the hostile engine and its independent compact-SVD
   signed-factor eigensystem.
3. Compare every L4 sector and registered aggregate; require the target's
   `5e-12` dense gate and the prospectively frozen target/audit tolerance.
4. The deliberate L4 SIGTERM/resume gate is complete: two commits before the
   signal, three after graceful stop, explicit resume, five matching canonical
   sector hashes, and an identical canonical final hash.  Six changed or
   corrupt-state cases were refused and an orphan temp was ignored unchanged.
5. Freeze a successor that authorizes L6 only.  Benchmark L6 event zero first,
   then compute each event `e=0,...,5` independently from the same terminal
   checkpoint, with output sectors `q=0,...,6` as tasks.  Seal target and audit
   results and revise the L8 estimate.
6. Only after L6 agreement and resource review, freeze L8.  Compute each event
   `e=0,...,7` independently with output sectors `q=0,...,8`.
7. Compare target/audit sectorwise and in aggregate.  Only then emit the
   compact eight-entry L8 configuration-TV adapter required by the curvature
   workstream.

Event zero is the primary L4--L6--L8 longitudinal sequence.  The remaining
events are a fixed all-event panel and the prerequisite for the separately
frozen curvature consumer; they are not sequential continuations.

## Measured inputs to the estimator

Prior prefix-history measurements on this machine were:

| Route | L4 wall / RSS | L6 wall / RSS | L8 wall / RSS |
|---|---:|---:|---:|
| target V012 | 0.635 s / 33.3 MB | 1.909 s / 48.0 MB | 17.958 s / 837.4 MB |
| hostile V002 | 0.605 s / 39.1 MB | 2.272 s / 44.6 MB | 26.523 s / 330.4 MB |

The actual target response L4 gate measured:

| Quantity | Value |
|---|---:|
| end-to-end wall | 0.903229917 s |
| slowest q task | 0.205485083 s |
| peak parent RSS | 33,685,504 bytes |
| peak child/sector RSS | 35,176,448 bytes |
| retained preterminal input | 3,152 bytes |
| immutable checkpoints | 19,443 bytes |
| final compact result | 15,210 bytes |

The real restart gate additionally measured:

| Quantity | Value |
|---|---:|
| complete harness wall | 1.853693625 s |
| uninterrupted control wall | 0.680212584 s |
| interrupted phase wall | 0.504730041 s |
| explicit resume wall | 0.460315334 s |
| peak child RSS | 35,094,528 bytes |
| uninterrupted checkpoint | 19,441 bytes |
| resumed checkpoint including orphan temp | 20,048 bytes |
| evidence before result | 92,310 bytes |
| resume result | 4,441 bytes |
| total owner-once evidence after result | 96,751 bytes |

The canonical final control/resume hash is
`0d5de10f17498fc12e05b26a56cdfe316c0c1f7db87fd21a45cb3b019406ac39`.
Raw result hashes differ, as expected, because measured resource values and
checkpoint locations are execution evidence excluded by the frozen canonical
scientific projection.

The first attempt is excluded from physical timing because it failed in
process setup before q0 completed.

## Static cost variables

For size `L` and output number sector `q`, record before execution:

```text
n_q = binomial(2L,q)                     carrier dimension
s_q = binomial(L,q)                      lineage dimension
k_A <= 3 s_q                             conservative actual-factor columns
k_P <= 4(s_(q-1)+s_q+s_(q+1))           conservative product-factor columns
Z bytes = 16 n_q (k_A+k_P)               raw complex factor storage
reduced bytes = 16 min(n_q,k_A+k_P)^2    reduced Hermitian storage
```

At L8, `max n_q=12,870`, `max s_q=70`, the conservative combined column
bound peaks at 938, and raw factor storage peaks near 56 MiB before solver and
QR workspace.  These are bounds, not a runtime forecast.

Each benchmark must record per task: terminal input sectors, factor column
counts, carrier dimension, QR reduced dimension, transport batches, solver
steps/residual, wall, peak RSS, and checkpoint bytes.  Estimate the next size
by summing measured task costs over the exact event/q census, using the larger
of measured scaling and the QR/transport operation model.  Do not extrapolate
from total Hilbert dimension alone.

## Resource acceptance before later launch

- freeze an RSS ceiling no larger than 8 GiB on the 16 GiB Mac;
- include temporary peak plus immutable checkpoint/result storage and retain
  at least 20 GiB free disk;
- require zero numerical warnings and finite solver/resource diagnostics;
- establish AC power immediately before launch;
- tie `caffeinate -i` to the computation and never use `-d`;
- report any estimate above ten hours before launch; and
- never promote an estimate to a pass when energy telemetry is unavailable.

The L6 benchmark must replace, not merely supplement, the preliminary L8
forecast.  A resource obstruction is an unresolved result and publishes no
partial physical aggregate.

## File-level successor boundaries

- Keep target changes versioned under this packet or a successor; never alter
  the V012 histories, retained shards, dense L4 packet, or migration audit.
- Create the independent route only under the separate `AUDIT_...SCALING...`
  packet; it must not import this target kernel.
- Put a later L8 adapter in the target successor only after the audit gate and
  bind its canonical JSON convention explicitly.
- The existing untracked curvature packet remains a consumer, not an input to
  this target calculation.
