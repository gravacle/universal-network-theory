# INTERFACE_0463_V001 — galaxy forward adapters and parallel campaign runner (Claude3, dispatch 0463)

Frozen API. Authors implement exactly this; the fixture author tests exactly this without reading the modules first. No physics is chosen. The 0462 modules are not modified; batching is a versioned adapter.

Root base: `R = /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/`.

## Common conventions

Same as INTERFACE_0462_V001: Python 3.12, numpy only (no scipy), inert at import, keyword-only args with no defaults, every public function returns `{ok, reasons, ...}` and fails closed, no numpy objects escape, canonical JSON = `json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)`, file pins are SHA256 over bytes and are verified before use. Nothing here reads an NGC3198 velocity, runs a real worker, uses the network or deletes anything. "theta" is a dict `{coordinate_name: float}` in natural units; its canonical key is the canonical JSON of the dict.

Forward-style result (what `forward`/`forward_ngc` return, as in 0462):
`{'speeds_km_s': {id: float}, 'valid': bool, 'reasons': list[str]}` plus optional `'provenance': dict`.

## Real worker command line (both workers, verified from their argparse)

```
<python> -I -B <worker.py> --seed <seed.json> --seed-sha256 <hex> --solver <solver.py> --solver-sha256 <hex>
   --checkpoint-module <ckpt.py> --checkpoint-module-sha256 <hex> --outdir <dir> --checkpoint-directory <dir>
   --start-iteration <int> [--resume]
```
The worker verifies every pin itself; it writes `start.json`, `progress.jsonl`, `result.json`, `finish.json` under `--outdir`. The runner builds exactly this command; the mock worker accepts exactly this command.

## Module A — `ddo154_forward_adapter_c3v001.py`

```
exposed_coordinates() -> {ok, coordinates: [{name, seed_pointer (JSON pointer into the seed), units, role_hint:
    'shared_scale' | 'nuisance' | 'numerical', exposed: bool, note}], not_variable_without_new_sampler_run: [names],
    shared_15_mapping: {shared_name: exposed_name | None}, reasons}
write_seed(*, base_seed_path, base_seed_sha256, theta, out_path) -> {ok, seed_sha256, changed_fields: [{pointer, old, new}],
    frozen_field_count, reasons}
read_result(*, outdir, region_path, region_sha256) -> forward-style result with provenance {result_sha256, transform}
reproduce_comparison(*, result_json_path, comparison_json_path, region_path, region_sha256) -> {ok, bitwise_equal: bool,
    max_abs_diff_km_s, rows: [{id, reproduced, recorded}], reasons}
make_theta_to_seed(*, base_seed_path, base_seed_sha256) -> {ok, theta_to_seed: callable(theta, out_path) -> write_seed result, reasons}
make_result_reader(*, region_path, region_sha256) -> {ok, result_reader: callable(outdir) -> forward-style result, reasons}
```
- `write_seed` verifies the base pin from bytes, changes **only** the fields that `exposed_coordinates` declares for the names present in `theta`, refuses an unknown name, refuses an existing `out_path`, and never edits the base seed. Every other seed field is copied unchanged.
- Distance and inclination nuisances are handled where the pinned evaluator handles them (the comparison's `forward_mapping_provenance`); if they are applied in the result transform rather than the seed, `exposed_coordinates` says so and `read_result` accepts them through `theta`-independent arguments documented in the notes. Do not invent a seed field for a nuisance the worker does not read.
- Acceptance: `reproduce_comparison` on `R/CODEX1/DDO154_STABLE_CACHED_COUPLED_RUN_V002/attempt_000/result.json` (SHA256 `79855e78bc1702b286828f6e7cf123d3e654509a08b395ced40cdbef06b453e0`) against `R/CODEX1/DDO154_FIRST_CONDITIONAL_CALIBRATION_EVALUATION_RUN_V001/comparison/comparison.json` (`0424798d…81bd1`) must give `bitwise_equal: True` for all 12 `predicted_catalogue_speed_km_s`. The transform is found by reading the evaluator that produced `comparison.json` (its path is in that run directory or the receipt), not guessed.

## Module B — `ngc3198_forward_adapter_c3v001.py`

Same six functions with the NGC43 worker (`R/helpers/recovered_packet_audit/ngc43_composite_coupled_root_worker_v001.py`, `1b95a4ff…0ca4`) and its seed. `read_result` returns 43 speeds keyed `NGC3198-Q01..Q43` in the order of `R/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` (`a2936517…5494`), binding ids by radius text/index as the worker exposes them; `reproduce_comparison` is replaced by `check_query_binding(*, manifest_path, manifest_sha256)` -> `{ok, query_ids, binding: [{query_id, worker_index, Rad_text}], reasons}`. If no launched NGC result exists, say so; synthetic result files are used only in fixtures. The adapter never reads a velocity for NGC3198.

## Module C — `campaign_runner_c3v001.py`

```
run_campaign(*, campaign_dir, python_executable, worker: {worker_path, worker_sha256, solver_path, solver_sha256,
             checkpoint_module_path, checkpoint_module_sha256, start_iteration}, thetas: list[dict],
             theta_to_seed: callable, result_reader: callable, max_workers, per_call_wall_s, per_call_rss_bytes,
             per_call_output_bytes, campaign_wall_s, resume: bool, poll_interval_s)
  -> {ok, status: 'COMPLETE' | 'CAMPAIGN_CAP' | 'REFUSED', calls: [per-call record in theta order], n_ok, n_failed,
      n_resumed, n_not_started, evaluations_run, campaign_wall_used_s, max_concurrent_observed, reasons}
forward_many(*, thetas, **same kwargs as run_campaign) -> {ok, results: [forward-style result per theta, in order],
      campaign: run_campaign output, reasons}
verify_receipt(*, receipt_path) -> {ok, receipt, reasons}
```
Per-call record: `{index, theta, theta_key, call_dir, status: 'OK' | 'FAILED' | 'RESUMED_OK' | 'RESUMED_FAILED' |
'DIR_EXISTS_UNVERIFIED' | 'NOT_STARTED', reason, receipt_path, result: forward-style | None, wall_s, exit_code,
max_rss_bytes_observed, output_bytes}`.

Rules the runner enforces:
1. `max_workers` is an int in `1..12`; more refuses. Each worker is a separate subprocess started with `start_new_session=True`, env `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`, `python_executable -I -B`, the exact command line above. The runner itself uses no threads.
2. `call_dir = campaign_dir / f'call_{index:04d}'` with `seed.json`, `out/`, `ckpt/`, `stdout.txt`, `stderr.txt`, `RECEIPT.json`. A call starts only if `call_dir` is absent (fresh directory, never overwritten). With `resume=True`, an existing `call_dir` whose `RECEIPT.json` verifies (self-hash, same `theta_key`, same worker pins, and `result_sha256` re-verified from bytes when present) is reused as `RESUMED_OK` or `RESUMED_FAILED` without rerunning. An existing `call_dir` that does not verify is `DIR_EXISTS_UNVERIFIED` and is never run or touched.
3. **No automatic retry.** A failure (non-zero exit, wall cap, RSS cap, output cap, missing/invalid result, reader failure) is recorded once with its reason; the campaign continues with the other calls.
4. Caps: wall per call (`per_call_wall_s`, kill the process group, status FAILED reason `WALL_CAP`); RSS per call (poll `ps -o rss=` on the child every `poll_interval_s`, kill when above `per_call_rss_bytes`, reason `RSS_CAP`); output bytes per call (total size under `call_dir`, reason `OUTPUT_CAP`); campaign wall (`campaign_wall_s`): no new call starts after it elapses, running calls finish under their own caps, status `CAMPAIGN_CAP`, unstarted calls are `NOT_STARTED`.
5. Receipt `RECEIPT.json` (canonical JSON, written once at call end): `{index, theta, theta_key, seed: {path, sha256}, worker pins (all four paths with sha256), command: list, started_utc, finished_utc, wall_s, exit_code, reason, max_rss_bytes_observed, output_bytes, result_json: {path, sha256} | None, result: forward-style | None, status, receipt_sha256 (self-hash with the key absent)}`.
6. Results are returned in theta order regardless of completion order. Every refusal returns `status='REFUSED'` with nothing started.

## Module D — `batched_engine_adapter_c3v001.py` (thin adapter on the 0462 API side; the 0462 modules are untouched)

```
make_cache() -> {ok, cache: dict, reasons}
make_cached_forward(*, forward_many, cache, stats) -> {ok, forward: callable(theta) -> forward-style, reasons}
prefetch(*, forward_many, cache, thetas, stats) -> {ok, requested, fetched, already_cached, reasons}
jacobian_stencil(*, engine, spec, u0, rel_step) -> {ok, u_points, thetas, reasons}
design_points(*, engine, spec, exploration, identifiability, design_count, rng_seed) -> {ok, u_points, thetas,
    skipped_outside_box, reasons}
run_calibration_region_batched(*, engine, forward_many, cache, stats, **every run_calibration_region kwarg except forward)
  -> {ok, engine_result (the 0462 run_calibration_region output), batching: {batches: [{purpose, n_requested, n_fetched}],
      cache_hits, cache_misses, sequential_fallbacks, replay_new_calls: int (must be 0)}, reasons}
```
- `forward(theta)` looks up `theta_key` in `cache`; on a miss it calls `forward_many(thetas=[theta])` (sequential fallback, counted) and stores the result. `stats` is a dict the adapter updates in place.
- `jacobian_stencil` reproduces the first-attempt central-difference points of the 0462 engine (`u0 ± rel_step·e_j`, clipped to the box, for every varying coordinate); halved steps after an invalid side are sequential cache misses, which is acceptable.
- `run_calibration_region_batched` runs: (1) prefetch the seed point and the Jacobian stencil in one batch; (2) `engine.run_calibration_region(..., design_count=0)` through the cached forward; (3) compute the Halton design points exactly as the engine does (same bases, same first index, same boundary box and directions, using the engine module's own helpers, pinned by the engine file hash); (4) prefetch them in one batch; (5) rerun `engine.run_calibration_region(..., design_count=requested)`; the replay of stages 1–3 must produce zero new forward calls (`replay_new_calls == 0`, else `ok=False`). The returned `engine_result` is the output of step 5, byte-identical to what a sequential run would produce.

## Fixtures — `mock_worker_0463.py` and `fixtures_0463_c3v001.py` (independent author)

The mock worker accepts the exact real command line, verifies its own pins the same way (sha256 of the given paths), reads the seed, and acts on `seed['mock']`: `{'sleep_s': float, 'mode': 'ok' | 'exit_nonzero' | 'hang' | 'rss' | 'output' | 'nan' | 'missing_result', 'speeds': {id: float}}`, writing `start.json`, `result.json` (deterministic from the seed) and `finish.json` under `--outdir`. Fixtures must demonstrate with numbers: the concurrency limit (max simultaneous ≤ max_workers, measured from the mock's start/finish timestamps), each cap, no retry, resumption by verified receipt, tampered receipt → `DIR_EXISTS_UNVERIFIED`, fresh-directory refusal, theta-order of results, `forward_many` shapes, and batched-adapter equivalence on a toy forward (identical canonical JSON of the engine result versus a sequential run, `replay_new_calls == 0`).

## File ownership under `claude_artifacts/galaxy_forward_0463/`

- DDO adapter author: `ddo154_forward_adapter_c3v001.py`, `DDO_ADAPTER_NOTES_0463_V001.md`, `DDO_REPRODUCTION_0463_V001.json`.
- NGC adapter author: `ngc3198_forward_adapter_c3v001.py`, `NGC_ADAPTER_NOTES_0463_V001.md`.
- Runner author: `campaign_runner_c3v001.py`, `RUNNER_NOTES_0463_V001.md`.
- Batched adapter author: `batched_engine_adapter_c3v001.py`, `BATCHED_ADAPTER_NOTES_0463_V001.md`.
- Fixture author: `mock_worker_0463.py`, `fixtures_0463_c3v001.py`, `FIXTURE_RESULTS_0463_V001.json`, `FIXTURE_NOTES_0463_V001.md`.
- Lead: this file, `EXPOSED_COORDINATES_0463_V001.md`, `REVIEW_0463_LEAD_CHECK_V001.md`, `HASHES_0463_V001.txt`.
