# L12 process-parallel execution successor

## Scope

This packet prepares a new execution path after the 30-hour Stage 3
obstruction.  It does not modify, delete, resume, or publish from either
preserved V012/V004R4 L12 workspace.  It does not change the Hamiltonian,
graph, edge order, admission map, lineage definition, accuracy schedule,
quadrature, convergence test, or any Stage 4-6 definition.

The existing 12-event causal chain remains serial.  Full authority and cache
authentication remain in the branch parent.  Only independent numerical
charge/window work is submitted to spawned child processes.

## Observed bottleneck and parallel boundaries

The timed-out target and hostile workers each consumed one logical core.  Both
had already materialized every sharp `prefix_11` q-shard; their remaining work
was the terminal graph evolution.  The prior outer coordinator ran target and
hostile concurrently, but every q sector and row window inside each branch was
serial.

The successor parallelizes these exact units:

1. Nonterminal admission: one task per output q shard.  Each task is the sole
   writer of its shard.
2. Nonterminal transport: one task per `(actual/null, q, row interval)`.
   Tasks write disjoint row intervals of a q-sharded memmap.
3. Target terminal transport: one task per `(child0/child1, q, row interval)`.
   A child0 task performs its actual and null evolutions together, matching the
   predecessor's per-window order and counting as two solver workloads.
4. Hostile terminal transport: one task per
   `(child0/child1/null, q, row interval)`.

The 36 edge updates inside one carrier multiplication are intentionally not
parallelized or scatter-vectorized.  Those edge slices write overlapping
output locations; parallel scatter would require atomics or large private
arrays and would alter reduction behavior.  Parallelism one level above them
is race-free and retains the frozen graph operator.

Gate validation, dependency-hash checks, cache semantic validation, event
ordering, rough-before-sharp ordering, result adjudication, sealing, and JSON
publication remain serial in the parent.  They are not the measured 30-hour
bottleneck.

## Process and memory model

`concurrent.futures.ProcessPoolExecutor` uses the `spawn` context.  `fork` is
not used because it could inherit coordinator sockets and retained authority
descriptors.  Before spawning, the parent forces OpenMP, OpenBLAS, MKL,
Accelerate, and NumExpr thread counts to one, preventing nested oversubscription.

No amplitude, carrier, graph, or index array crosses a process pipe.  Task
messages contain only paths, q, row bounds, phase, and resolution label.  Each
worker:

- authenticates the already parent-pinned manifest;
- stable-opens only the immutable cache members needed by its task;
- reopens the relevant state memmap;
- allocates one predecessor-sized numerical window; and
- returns only small statistics, currents, and solver counters.

The target workset certificate remains 1,000,000,000 bytes per active worker;
the hostile certificate remains 1,400,000,000 bytes.  On this 14-core,
51,539,607,552-byte host, the default is seven workers per branch.  With both
branches live, this is 14 numerical processes and a certified maximum active
numerical workset of 16.8 GB, excluding shared read-only page-cache mappings.

The production successor count is explicit, not inferred at launch: seven
target workers and seven hostile workers, for fourteen concurrent numerical
worker processes when both branches run. Capacity calculation remains a
fail-closed preflight and may reject this count, but it cannot silently reduce
or increase it.

The successor hard wall ceiling is 345,600 seconds (96 hours), measured from
the fresh worker ACK/release boundary. The historical 30-hour policy remains
part of the preserved failed-run evidence but is not the successor policy.

Every mutable task owns either a distinct q file or a distinct row interval.
Workers never update shared Python aggregation objects.  The parent restores
all results to the predecessor's canonical order before floating-point
reduction, even though heavier tasks are submitted first for load balance.

## Parent-only telemetry

Before the first future is submitted, each adapter prints a whole-run record:

```
L12_PROGRESS_START branch=<branch> stage=full_rough_plus_sharp_run \
  total_tasks=<N> charge_sectors=<Nq> row_windows=<Nw> \
  estimated_solver_cell_steps=<W>
```

Each stage prints its own exact denominator.  As futures complete, the parent
prints `completed/total`, literal task percentage, weighted work percentage,
elapsed time, ETA, rolling tasks/second, and rolling solver-cell-steps/second.
The first ten completions are immediate; later routine updates are capped at
one line per five seconds.  Workers perform no logging and acquire no telemetry
lock; they do not sample or return telemetry. Process topology and all progress
counters are observed by the parent. The final resource record includes the
declared, completed, and remaining task/work counts, and the parent refuses to
continue if the full declared denominator was not consumed.

On a signal, deadline, child exception, or denominator mismatch, the parent
flushes `L12_PROGRESS_STOP` before pool teardown.  That record gives the exact
completed and remaining task counts and weighted solver-cell-step counts, so a
ceiling exit cannot again leave progress unknowable.

The weighted denominator is `rows * carrier_columns * checkpoint_depth`; target
child0 windows carry a factor of two because they execute both actual and null
transport.  This prevents tiny edge-q windows from dominating the early ETA.
The first submitted futures are the largest work units, but the reduction order
is unchanged.

The static L12 plan on this source packet is:

| branch | workers | charge-sector passes | solver row windows | total tasks | estimated solver cell-steps |
|---|---:|---:|---:|---:|---:|
| target | 7 | 488 | 4,560 | 4,714 | 274,768,288,592 |
| hostile | 7 | 512 | 1,516 | 1,670 | 431,778,739,216 |
| combined | 14 | 1,000 | 6,076 | 6,384 | 706,547,027,808 |

`print_l12_plan.py` recomputes this denominator without constructing a pool or
touching a workspace.

## Termination and custody

The integration context catches `SIGINT` and `SIGTERM`, refuses further work,
cancels pending futures, forwards termination to running pool children, and
waits for pool shutdown.  Completed row windows are flushed.  No result is
aggregated or published after an incomplete future, and the partial successor
workspace is left in place so the failure is visible and cannot be silently
overwritten.

Full cache SHA-256 verification remains the responsibility of the retained
parent context before and after the pool.  Children enforce the same manifest
hash, exact member census, immutable mode, stable inode identity, dtype, shape,
and byte count while avoiding repeated whole-cache hashing in every process.

## Integration and authorization boundary

`execution_integration.py` contains the two narrow replacements for the former
serial rough/sharp calls.  A new target and hostile consumer must:

1. authenticate the existing frozen proof inputs and cache in the parent;
2. bind every source hash in this packet with a new preflight/audit and new
   execution authorization;
3. use new canonical output and workspace paths (the obstructed workspaces are
   preserved and must not be overwritten);
4. call `run_target_rough_and_sharp` or `run_hostile_rough_and_sharp`;
5. reauthenticate the parent cache/authority context; and
6. use the existing adjudication, sealing, and publication machinery, extended
   to record `pool.resource_record()`.

This packet is implementation and control preparation only.  It is not itself
authorization to start L12.

`launch_config.py` reserves new canonical workspace/output names ending in
`L12_PROCESS_PARALLEL_V001` / `HISTORY_L12_PROCESS_PARALLEL_V001.json`. It
requires those paths to remain absent before launch and separately verifies
that both timed-out `L12` workspaces remain present.

## Verification

`test_parallel_successor.py` uses two spawned processes at L4 and compares:

- full target rough history (admission, mutable nonterminal routing, terminal
  routing, and ordered reduction) against V012 serial output;
- direct target fine terminal output against V012 serial output;
- full hostile rough history against V004R4 serial output; and
- direct hostile sharp terminal output against V004R4 serial output.

All numerical fields match at an absolute/relative tolerance of `2e-12`, and
each direct terminal test observes at least two distinct worker PIDs.
