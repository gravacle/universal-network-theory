# INTERFACE_0462_V001 — calibration-region engine and prediction freeze (Claude3, dispatch 0462)

Frozen API for `calibration_region_engine_c3v001.py` (Module 1) and `prediction_freeze_c3v001.py` (Module 2). Authors implement exactly this; the fixture author tests exactly this without reading the modules first. No physics is chosen here.

## Common conventions (both modules)

- Python 3.12, `numpy` only (no scipy). `import json, math, hashlib, os` allowed. **Inert at import**: no file I/O, no computation, no environment changes at import time. No `__main__` block.
- Every public function takes **keyword-only arguments with no defaults** and returns a dict with at least `ok: bool` and `reasons: list[str]`. Anticipated bad input returns `ok=False` (fail closed); it does not raise. Exceptions raised by the root-supplied callables are caught, logged, and treated as invalid evaluations.
- Single-thread numerics: modules never spawn processes or threads. Callers set BLAS threads = 1 before importing numpy.
- Canonical JSON: `json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)`. File hashes are SHA256 over raw bytes. All returned arrays are plain lists (JSON-serialisable); no numpy objects escape.
- Forbidden target field names (from the P46 harness, lowercase compare): `vobs, vobs_km_s, observed_velocity, observed_km_s, error_v_km_s, velocity_error, chi2, residual_km_s, vgas, vdisk, vbul, vgas_km_s, vdisk_km_s, vbulge_km_s`, plus `target_rows, targets, target_velocity, target_velocities`. Module 2 refuses to write a manifest containing any such key at any depth.
- Neither module reads any NGC3198 velocity. Module 1 never reads anything about NGC3198 at all. Module 2 reads only the target-free query manifest; target rows reach it only through `score_after_freeze` and are never written to disk by it.

## Root-supplied callables

```
forward(theta_natural: dict[str, float]) -> {'speeds_km_s': dict[row_id, float], 'valid': bool, 'reasons': list[str]}
forward_ngc(theta_natural: dict[str, float]) -> {'speeds_km_s': dict[query_id, float], 'valid': bool, 'reasons': list[str]}
```
`theta_natural` carries every coordinate (free, nuisance and fixed) in natural units. An evaluation is **valid** only if the callable returned a dict with `valid is True`, every expected id is present, and every value is a finite float. Anything else (missing id, NaN, exception, wrong type) is invalid, with the reason recorded.

## Coordinates

```
coordinates = [
  {'name': str, 'transform': 'log' | 'linear', 'lower': float, 'upper': float,
   'role': 'free' | 'fixed' | 'nuisance', 'trial_value': float}, ...]
```
- Internal coordinate: `x = ln(v)` for `log` (requires `0 < lower < upper`), `x = v` for `linear` (`lower < upper`). Unit coordinate `u = (x - x_lo) / (x_hi - x_lo)` in `[0, 1]`.
- `free` and `nuisance` coordinates vary together (nuisances such as distance with `r_model = r_cat·(D/4.04 Mpc)` and inclination/estimator transfer are common parameters, never per-row biases). `fixed` coordinates stay at `trial_value`. Varying coordinates are ordered as given.
- Every output that mentions bounds carries `bounds_semantics: 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'`.

## Module 1 — `calibration_region_engine_c3v001.py`

```
load_observation_region(*, path, expected_sha256) -> {ok, sha256, row_ids (list of 12, file order),
    rectangles: {row_id: [low, high]}, sigmas: {row_id: float}, observed: {row_id: float},
    reference_radius_kpc: {row_id: float}, statistical_choice, distance_summary, forward_coordinates, reasons}
```
Verifies the byte hash before parsing, binds exactly `rows[].id, reference_radius_kpc, observed_speed_km_s, quoted_random_sigma_km_s, conditional_random_acceptance_low_km_s, conditional_random_acceptance_high_km_s, statistical_choice, distance_summary, forward_coordinates`. Does not alter the rule; `low < observed < high` and `sigma > 0` must hold for every row or `ok=False`.

```
make_coordinate_spec(*, coordinates) -> {ok, names, varying_names, fixed_names, nuisance_names, roles,
    transforms, lower, upper, trial_values, bounds_semantics, reasons}
to_natural(*, spec, u) -> {ok, theta_natural, theta_internal, reasons}   # u: list over varying coords; fixed coords inserted
to_unit(*, spec, theta_natural) -> {ok, u, reasons}
classify_prediction(*, prediction, rectangles, row_ids) -> {ok, valid, admitted, row_inside: {row_id: bool|None}, reasons}
```
Admitted means valid and every row's speed inside its closed rectangle `[low, high]`.

```
finite_difference_jacobian(*, forward, spec, region, u0, rel_step, min_step, max_halvings, budget, log)
  -> {ok, f0: {row_id: float}, seed_valid, seed_admitted, jacobian_u: 12×n list (rows in region.row_ids order,
      columns in varying order), steps_used: list, failed_columns: list, evaluations_used: int, reasons}
```
Central differences in `u`. Column step starts at `rel_step` (in u units), clipped to the box; if either side is invalid the step is halved, at most `max_halvings` times; a column that never succeeds is reported in `failed_columns` and its Jacobian column is `None`. Every call is appended to `log` (see below).

```
identifiability_report(*, jacobian_u, sigmas, row_ids, varying_names, null_tolerance)
  -> {ok, scaled_jacobian, singular_values, right_vectors (rows = directions in u-space), identified: list[int],
      near_null: list[int], condition_numbers, null_tolerance, reasons}
```
`scaled_jacobian = diag(1/sigma) · J_u`. Direction `i` is identified iff `s_i >= null_tolerance · s_max`; otherwise near-null. `condition_numbers[i] = s_max / s_i` (`inf` as the string `"inf"` if `s_i == 0`). Columns reported as `None` by the Jacobian make the report `ok=False`.

```
explore_region(*, forward, spec, region, u_anchor, identifiability, repair_iterations, max_repair_step,
               march_step, bisection_steps, design_count, rng_seed, budget, log)
  -> {ok, status: 'COMPLETE' | 'BUDGET_EXHAUSTED' | 'NO_ADMITTED_POINT', stage_reached,
      anchor: {u, theta_natural, admitted}, admitted_points: [{u, theta_internal, theta_natural, prediction, log_index}],
      rejected_points: [...same shape...], boundary: {direction_index: {'minus': t, 'plus': t}},
      hull_box: {direction_index: {'min': t, 'max': t}}, unidentified_directions: [{index, vector_u, singular_value,
      trial_projection, sensitivity}], evaluations_used, empty_region: bool, reasons}
```
Deterministic procedure, in this order, each step checking the remaining budget before every forward call:
1. Classify the anchor. If admitted, it is the first admitted point.
2. If not admitted: linearised repair. With the fixed seed Jacobian, take at most `repair_iterations` damped Gauss-Newton steps restricted to the identified directions, toward the rectangle centres in sigma-scaled units, each step clipped to `max_repair_step` in u-norm and projected into `[0, 1]^n`; evaluate each. Stop at the first admitted point. If none, return `status='NO_ADMITTED_POINT'`, `empty_region=True`, with every evaluation preserved. (This searches DDO154 calibration rows only; it is not target tuning.)
3. From the first admitted point `a`: for each identified direction `v_k` and sign `±`, march `a ± t v_k` with `t = march_step, 2·march_step, 4·march_step, …` until the point is not admitted or leaves the box; then bisect between the last admitted and first rejected `t` for `bisection_steps` steps. Record the boundary `t` per side (the box edge if never rejected).
4. Halton design (bases 2, 3, 5, 7, 11, 13, … per identified direction; `rng_seed` selects the integer offset of the first index) of `design_count` points inside the boundary box of step 3, mapped through the identified directions around `a`; classify each; points outside `[0, 1]^n` are skipped and counted.
5. `hull_box` = per identified direction the min and max projection `(p - a)·v_k` over all admitted points. `unidentified_directions` carries each near-null direction's vector, singular value, trial projection and `sensitivity = ||scaled_jacobian · v||`.
Budget exhaustion at any step returns `status='BUDGET_EXHAUSTED'` with `stage_reached` and everything evaluated so far.

```
run_calibration_region(*, forward, coordinates, observation_region_path, observation_region_sha256, u_seed,
                       budget, rel_step, min_step, max_halvings, null_tolerance, repair_iterations,
                       max_repair_step, march_step, bisection_steps, design_count, rng_seed)
  -> {ok, status, region: {...load_observation_region...}, spec, jacobian: {...}, identifiability: {...},
      exploration: {...}, evaluation_log: [...], evaluations_used, budget, ngc3198_access: 'NONE',
      bounds_semantics, reasons}
```
Orchestrates the above. `u_seed` is a list over varying coordinates (`None` means use `trial_value`). `budget` is the maximum number of forward evaluations in total.

**Evaluation log** entries (appended by every forward call, in order):
`{'index': int, 'purpose': str, 'u': list, 'theta_internal': list, 'theta_natural': dict, 'prediction': dict|None, 'valid': bool, 'admitted': bool|None, 'reasons': list, 'exception': str|None}`.

## Module 2 — `prediction_freeze_c3v001.py`

```
load_query_manifest(*, path, expected_sha256) -> {ok, sha256, query_ids (43, ascending data_row_index),
    radii_text: {query_id: str}, rad_unit, reasons}
```
Requires 43 unique ids and `rows[].data_row_index` 1..43. Binds only `query_id, data_row_index, Rad_text, Rad_unit`.

```
select_representative_points(*, exploration, interior_count) -> {ok, points: [{u, theta_natural, role: 'anchor' |
    'hull_vertex' | 'interior', log_index}], hull_vertex_count, interior_count_used, reasons}
```
All hull vertices (for each identified direction the admitted points attaining the min and the max projection), the anchor, then a deterministic interior subset: the remaining admitted points sorted by `log_index`, taking `interior_count` evenly spaced indices (all of them if fewer). Duplicates by `log_index` are removed.

```
evaluate_envelopes(*, forward_ngc, points, query_ids, budget) -> {ok, status, per_point: [{point_index, valid,
    speeds_km_s: dict|None, reasons, exception}], envelopes: {query_id: {min, max, central, n_points, n_valid, valid}},
    evaluations_used, evaluation_log, reasons}
```
`central` is the median over valid points. A query is `valid` only if **every** evaluated point returned a valid finite value for it. Budget exhaustion preserves partial results with `status='BUDGET_EXHAUSTED'`.

```
write_freeze_manifest(*, out_path, parameter_region, alternatives, observation_rule, envelopes, query_ids,
                      code_files: list[path], input_files: list[path], notes)
  -> {ok, path, manifest_sha256, bytes_written, reasons}
```
Refuses if `out_path` exists, if any forbidden key appears at any depth in the supplied dicts, if `envelopes` does not cover exactly `query_ids`, or if any listed file is unreadable. Manifest content:
```
{'schema': 'FREEZE_MANIFEST_C3V001', 'created_utc', 'parameter_region', 'alternatives', 'observation_rule',
 'query_ids', 'units': 'km/s', 'semantics': 'TOTAL_OBSERVABLE',
 'predictions': [{'id', 'velocity' (central), 'band_low', 'band_high', 'n_points', 'n_valid', 'valid'}, ... 43 in query_ids order],
 'pins': {'code_files': [{path, sha256}], 'input_files': [{path, sha256}]}, 'notes', 'target_velocities_included': False,
 'within_error_rule': 'valid and |velocity - observed| <= quoted sigma (central value); band overlap is reported separately and is not the headline',
 'manifest_sha256': <sha256 of the canonical JSON of everything above with this key absent>}
```
Written as canonical JSON bytes.

```
verify_freeze_manifest(*, freeze_manifest_path) -> {ok, manifest_sha256_recomputed, manifest_sha256_recorded,
    pins_verified: [{path, recorded, actual, ok}], reasons}
score_after_freeze(*, freeze_manifest_path, target_rows) -> {ok, refused: bool, rows: [...], within_error_count,
    band_overlap_count, invalid_count, n_rows: 43, manifest_sha256, error_model:
    'CONDITIONAL_QUOTED_SIGMA_DIAGONAL_ONLY', reasons}
```
`target_rows` is a list of 43 dicts `{'id', 'velocity', 'sigma'}` in manifest order (the P46 observation schema); any id/order mismatch, non-finite value or `sigma <= 0` refuses. The scorer refuses (`refused=True`, no rows) unless `verify_freeze_manifest` passes. Each row reports `id, observed_speed_km_s, predicted_speed_km_s, band_low_km_s, band_high_km_s, quoted_sigma_km_s, signed_residual_km_s (= predicted - observed), sigma_ratio, fractional_error (residual / observed, None if observed == 0), valid, within_error, band_overlaps_error_bar`. `within_error` is `valid and |sigma_ratio| <= 1`; an invalid entry is never within error. The scorer writes nothing to disk.

## File ownership under `claude_artifacts/calibration_freeze_0462/`

- Engine author: `calibration_region_engine_c3v001.py`, `ENGINE_NOTES_0462_V001.md`.
- Freeze/scorer author: `prediction_freeze_c3v001.py`, `FREEZE_NOTES_0462_V001.md`.
- Independent fixture author: `fixtures_0462_c3v001.py`, `FIXTURE_RESULTS_0462_V001.json`, `FIXTURE_NOTES_0462_V001.md`.
- Lead: this file, `REVIEW_0462_LEAD_CHECK_V001.md`, `HASHES_0462_V001.txt`.
