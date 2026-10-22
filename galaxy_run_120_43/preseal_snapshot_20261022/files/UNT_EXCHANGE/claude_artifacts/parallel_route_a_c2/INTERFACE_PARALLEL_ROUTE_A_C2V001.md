# INTERFACE: parallel route-A solver (Claude2 lane, c2v001)

## Files

| File | Role | Reviewed base it succeeds |
|---|---|---|
| `coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_c2v001.py` | solver | `44d9c23c` (resumable_coupled_gas_0422) |
| `ddo_composite_stable_cached_root_worker_v002_parallel_c2v001.py` | DDO154 worker | `c4cb6826` |
| `ngc43_composite_coupled_root_worker_v002_parallel_c2v001.py` | NGC3198 worker | `42bdd23e` |

- The checkpoint module is unchanged. Keep using `coupled_gas_checkpoint_c2v003.py` (`069b3935`).
- Diffs against the reviewed bases are in `diffs/`. Byte copies of the bases are in `base_copies/`.
- Pins computed from bytes are in `HASHES_C2V001.json`.

## API

```
solve(..., checkpoint=None, fixed_source_fourier_J=None, column_workers=1)
bind_column_workers(N)  -> module-shaped view: __file__ = solver file, solve = partial(solve, column_workers=N)
ColumnPoolError(RuntimeError)
last_pool_report()      -> diagnostics only (pids, peak RSS, task counts, split rule); never part of a result
```

- `column_workers` must be an `int` from 1 to 64. Anything else raises `ValueError` before any work starts.
- **N=1** calls `_solve(pool=None)`. That is the reviewed body with no pool and no processes. Every insertion in it is guarded by `pool is not None`.
- **N>1** starts min(N, number of gas columns) worker processes.
- Workers use the `multiprocessing` spawn context. Each worker is started with `VECLIB/OPENBLAS/OMP/MKL/NUMEXPR_NUM_THREADS=1`. The parent environment is restored after the workers start.
- Workers are started, and the column environment is proven shippable, **before** `checkpoint.open_run`. If this step fails, nothing is written.

## Worker CLI (DDO and NGC successors)

- New required flag: `--column-workers N` (1 to 64). The worker exits with argparse code 2 if the flag is missing. It raises `ValueError` before reading any input if N is out of range.
- `start.json` gains `column_workers`.
- The worker passes `mods['solver'].bind_column_workers(N)` to the reviewed binding. The binding and the composite adapter pin `solver_module.__file__`, so that check is unchanged.
- `LOCAL` paths are now absolute because these files live outside the reviewed tree. The `LOCAL` keys and pins are unchanged, so stage `stage_dict_items` overrides still apply.
- `--solver` must be the parallel solver, because the view comes from it.

## Semantics preserved (N>1)

1. **Column order.**
   - Each iteration's fresh columns (`len(restored)..n-1`) are queued in roster order.
   - Results are consumed **strictly in column order** through the reviewed `try` block, which uses `pool.take(column_index)`.
   - The reviewed statements are unchanged: append, `write_column`, `column_completed` progress, and J accumulation.
   - Look-ahead is at most 16·N columns, with at most 2 queued tasks per worker.
2. **HI failures.**
   - A worker catches `ValueError` around exactly the same `solve_hi_column` call.
   - The parent re-raises it inside the reviewed `try` with the same `type(exc).__name__` and `str(exc)`. The reviewed failure dict, `FAILURE` record and outcome are therefore produced by the reviewed code.
   - The first failing column in column order is reported. Later columns are never used, written or announced. The pool is terminated on return.
3. **Other worker exceptions** (for example `TypeError`) propagate out of `solve`, as in the serial path. The original type and message are kept, and the worker traceback is attached as a note.
4. **Pool failures** raise `ColumnPoolError`, a `RuntimeError` that is never recorded as a physical failure. Examples: a worker killed or crashed, transport failure, an unshippable environment.
   - All columns before the undelivered one are already committed. The run resumes from there.
5. **Checkpoint.**
   - The record set, every record field except attempt and payload tokens, and the content-addressed blob set are identical to the reviewed solver's (tested).
   - `IDENTITY` differs only in `code.solver.{path,sha256}`.
   - **N is not identity.** A killed run resumes with any N and gives bitwise-identical final outputs (tested with N = 8, 1 and 3).
   - A checkpoint written by `44d9c23c` cannot be resumed by this solver, and the reverse also fails, because the solver pin is identity.
6. **Progress events** are identical in content and order. Only their wall-clock timing differs.
7. **Determinism.**
   - Each column is a pure function of the shipped inputs and pinned code. Worker assignment never reaches a result.
   - The fresh line cache per column is equivalent to the serial cache: `prepare_line` is pure in (prepared, x, y).

## Source transform split (an addition beyond the column loop)

- The measured cost profile is in "Measured cost profile" below. Without the split, N=8 gives only about 1.65x per DDO iteration.
- With the split, the gas update `physical_source_fourier` is computed by the pool over **chunk-aligned wave-row blocks**: multiples of `wave_chunk=64`, 3 blocks per worker. The blocks are stacked in wave order.
- The split is used only when **all** of these hold:
  - the source module file has sha256 `81af8715…` (`baryonic_metric_source_columns_v003`);
  - its `physical_source_fourier` code equals the compiled file function;
  - its kwdefaults are `{wave_chunk:64, source_chunk:256}`.

  Otherwise the reviewed serial call runs.
- In that function each output row depends only on its own wave, and a chunk-aligned sub-call performs the same per-chunk operations. Evidence:
  - random tests, including a partial last chunk;
  - the real-data comparison against the saved COMPLETED rows (below).
- Errors: the first failing block in wave order is raised.
  - Known difference: an input that is invalid in **both** a wave row and a column/position could report a different message first. This cannot happen for the solver's `k_physical`, which `prepare` already validates as finite.

## Environment shipping (spawn: nothing is inherited)

- Closures, such as the reviewed `make_modules` facades and the prep `boundary` closure, are rebuilt in the worker:
  - each `.py` file is loaded from bytes and its sha256 is verified;
  - shipped code bytes are used only to **find an equal code object in that file**, so no foreign code runs;
  - shared closure cells stay shared.
- Each file module's plain-data globals and function globals are replicated from the parent, so stage-runner `module_patches` hold in workers (tested).
- Not replicated: class instances or other objects held in module globals. These keep their file-defined values.
- Functions must be defined in `.py` files or importable modules.
- Spawn re-imports the parent `__main__` as `__mp_main__`. This is inert for both workers and for `galaxy_m0_forward_c2v005.py`. Any other main script needs a `__main__` guard.
- Not identical to serial:
  - worker traceback text;
  - exception object identity;
  - result object aliasing with inputs, which the reviewed HI does not use.

## Measured cost profile (saved DDO route-A runs, iterations ≥1)

| Run | prepare | 576 columns | source update |
|---|---|---|---|
| A2_ANCHOR_F10 | 7 s | 96 s | 103 s |
| KMAX_A2F10_C4 | 17 s | 231 s | 265 s |
| REPRO_PINNED_FULL | 7 s | 100–110 s | 106–110 s |

- The update is consistently 1.05–1.15x the column loop.
- Iteration 0 also does the base unit solve, 147–416 s, which **stays serial** in this version.

## Resources

- Peak RSS per worker, DDO measured: 0.36–0.39 GB. It holds the prepared response (70 MB) plus transient pickles of it, the waves (9 MB), the source inputs and numpy.
- NGC (80³ waves, about 85k source positions), estimated: about 0.6–0.8 GB per worker.
- Parent overhead: one extra pickled copy of prepared per iteration.
- With concurrent stages, keep the total number of workers plus parents across all stages at or below about 17 on 6 Super + 12 Performance cores.

## Expected per-iteration time (model in `results/projection_c2v001.json`)

- Model:
  - per-process speed: Super = 1, Performance = r, with r between 0.52 (measured with a background QoS clamp) and 0.70;
  - parallel efficiency 0.90 for columns and 0.95 for the update;
  - the machine is otherwise idle;
  - the serial parts (prepare, residual, COMPLETED write) are included.

| N | 1 | 6 | 8 | 10 | 12 | 14 | 16 |
|---|---|---|---|---|---|---|---|
| DDO F10 (s) | 206 | 44 | 38–39 | 33–35 | 30–32 | 27–30 | 25–28 |
| NGC est. (s), serial ≈2375 | 2375 | 442 | 361–379 | 307–332 | 267–296 | 236–268 | 213–244 |
| NGC if serial = 3500 s | 3500 | 652 | 533–558 | 452–490 | 393–436 | 348–394 | 313–360 |

- Replay measurement, 96 columns, under machine load of 13–100: the column phase was 5.6–5.7x faster at N=8, and the update phase 5.2–6.8x.
- Above about N=12 the gain comes from 0.5–0.7-speed cores. Under the current load, N=12 did not beat N=8.
