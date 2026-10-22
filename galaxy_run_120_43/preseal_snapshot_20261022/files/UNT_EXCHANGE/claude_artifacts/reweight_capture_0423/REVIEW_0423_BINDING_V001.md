# REVIEW 0423 BINDING V001: recipe/worker capture C2V001 deltas, API binding, pins and invariance

- Role: distinct reviewer, not the author of 0423 or of the reviewed files.
- Method: static inspection only. Nothing was imported or executed: no recipe, worker, sampler, statistics, operator, adapter or occupancy module. There was no scientific worker, fixture sampling, target velocities, refit, cloud, network, install or retry. Read-only on the program tree.
- AST checks: `python3 -I -B` (3.9.6) ran `ast.parse`/`compile(text)` on text copies in the reviewer's own scratch directory. No `__pycache__` or `.pyc` exists in reweight_capture_0423.
- Date: 2026-10-16.

## Verdict

**PASS_WITH_NOTES.** No blocking issues. The binding matches the V002 contract and the revalidation's minimal recipe delta. All six loaded modules are pinned and checked from bytes at load, and the RNG, proposals, physical inputs and budgets are unchanged. The notes are scope and risk items for the root. None requires a file change.

## 1. Hashes recomputed from bytes (all match)

| item | sha256 |
|---|---|
| task 0423 | cf561cec76f8015ac15589eaa95250743ff3e52bf93955dd3592c7005672180f |
| base recipe V009 | 44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697 |
| sampler pairallk V002 | bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba |
| statistics V001 | 85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a |
| base worker V007 | d691efbb9f62ded53ccde5076af45fe027c5f7456cf21126071f5ce827a7f17e |
| capture distinct review JSON | aabea1dcd5fee2c5ed7c7c41438dbf58af1e6388919ed82f6b04969874d368fb |
| current-pin revalidation JSON | b10b91f16efc7e3b4eccbd7f12773f66057a3ad4843a7fbecb4ab617a158eef1 |
| operator V003 (recipe `DRAFT_SOURCE_PINS['operator_v003']`) | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 |
| adapter V001 | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 |
| occupancy V002 | 7f76641c2e1b442557b614e3d8cd6607c21defd7da64de0b1756a732588d9ff5 |
| prior sampler pairallk V001 (diff base only) | 1907a397d69cdd0a508a00fb0a858aab9c914e4bcf126b079c1f491cbb10e2b9 |
| NEW recipe `owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py` | a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95 |
| NEW worker `owned_L4_collective_response_root_worker_v007_capture_c2v001.py` | 6c62b8ad1520a1ccafaeac8cb64cbb52c8a6f13763afe974175827c72cc6cc19 |
| `DELTA_0423_CAPTURE_V001.md` | b97137e3e504563c64d09ed86cd7597ab39852d89421cb02b8ec57b15ec97d9c |

The author's reported hashes all agree with the bytes.

## 2. Reviewer's own diff -u

- **Recipe V009 to C2V001:** +64/−3. **Worker V007 to C2V001:** +11/−3.
- After the two `---`/`+++` header lines, each body is byte-identical to the diff embedded in DELTA §11.

AST comparison against the bases:

- **Recipe, unchanged parts.** All base top-level constants are AST-identical: `TRIAL`, `DRAFT_SOURCE_PINS`, `OCCUPANCY_SHA256` and `FINAL_MERGED_SAMPLER_SHA256=None`. So are the six helpers: `_verified_module`, `documentary_payload`, `normalize_complete_derivatives`, `convert_uniform_background`, `background_from_completed_outputs` and `background_from_allk_outputs`.
- **Recipe, new constants:** BASE_RECIPE_V009_SHA256, CAPTURE_SAMPLER_SHA256, STATISTICS_SHA256, OPERATOR_SHA256/ADAPTER_SHA256 (taken from `DRAFT_SOURCE_PINS`), CAPTURE_AMPLITUDE_ORDER, CAPTURE_RATE_TOLERANCE and CAPTURE_PROFILE_ATTESTATION.
- **`prepare`.** 27 of 29 base statements are unchanged and keep their order. The two changed statements are:
  - the `args=dict(...)`: the 27 base keyword values are AST-identical, and only `reweighting_capture=capture_args` is added;
  - the return dict: every base key/value is identical, and only `statistics_module` and `reweighting_capture_record` are added.

  Four statements are added: the h/t/theta accessor check, the `AMPS` order check, `capture_args` and `capture_record`.
- **`run_prepared`.** 16 of 17 base statements are unchanged and keep their order. The `try` body gains only `result['recipe_reweighting_capture']=dict(...)`, and its `finally` is identical. Seven guard statements are added before the patch: the V002-only pin, the capture/callback identity and value comparison, and three `_verified_module` calls.
- **Worker.** `B`, `X`, `load` and `clean` are AST-identical. `SOURCES` changes the sampler to V002, changes the recipe to C2V001 and adds statistics. `main` only adds `statistics_module=` and `result['reweighting_capture_request']`.

## 3. API binding against the actual sampler and statistics code

**Sampler `owned_collective_worldline_static_response` (V002):**
- It has 28 keyword-only parameters. Only `reweighting_capture` has a default.
- The recipe passes exactly those 28 keywords, with no missing or extra keyword.

**V002 validation** (L5101–5116):
- The `set(reweighting_capture)` must equal {module, operator_module, uniform_amplitudes, uniform_profile_attestation, rate_tolerance}. `capture_args` has exactly these five keys.
- `module.configure(run, operator_module, uniform_amplitudes, uniform_profile_attestation, rate_tolerance)` matches the statistics V001 keyword-only signature exactly. So does `module.capture(run, path, allk_row, operator_module, budget_check=_budget_check, metadata)` (L5258).

**Values:**
- **module:** the pinned statistics V001 object (85f4…).
- **operator_module:** the same object as the guarded `operator_api` and `diagonal_read_source_callback['operator_module']`. `run_prepared` asserts the identity with the callback. Therefore `run['context']` and the private `_admit_state`/`_require_coverage`/`_diagonal_items`/`_full_scope`/`_native_weights` calls share one module, and all five exist in operator V003.
- **uniform_amplitudes:** `[float(abs(TRIAL[n])) for n in ('h','t','g','kappa','epsilon')]`. This is the same TRIAL dict, whose bytes are unchanged, with no new values. The order equals `statistics.AMPS`, which is checked in `prepare` and verified from the source text.
- **uniform_profile_attestation:** a non-empty explicit string.
- **rate_tolerance:** `1e-12`.

This matches the revalidation JSON `minimal_recipe_delta` literally.

**Static consistency of the premise** (not a run):
- **Edge profiles.** Adapter `build_inputs` makes h/t/theta `UniformEdgeProfile(L, value)`. Operator `_edge_table` admits them as `('accessor', obj)`, so `configure` skips them by design. The recipe's type/L/value check covers this gap structurally.
- **Vertex and owner maps.** g/kappa/epsilon are admitted as uniform maps, and `abs(complex(v))==amp` holds exactly.
- **Marked rate.** `W = |amplitude| * fsum([1.0] + [0.0*w])`, which is exactly |amp| at uniform unit lapse. The 1e-12 rate check therefore holds for every marked kind.
- **Names and kinds.** Operator `_diagonal_items` yields exactly the eleven RAW names (E_I is absent). Its transition kinds equal the statistics `KINDS` keys.
- **Occupancy events.** These come from `sampler._event_from_channel`, so they carry `allk_idx`/`allk_rho`.

## 4. Pins

- **Worker `load()`:** checks sha256 from bytes before `exec_module` for all six loaded modules (operator, sampler V002, adapter, occupancy, recipe C2V001, statistics). The paths and pins were verified above.
- **Imports:** no module imports any other project file. The imports are stdlib and numpy only.
- **Recipe `run_prepared`:** before patching `_move`, it re-hashes `__file__` for the sampler (bd63… required), occupancy, statistics, operator and adapter. The recipe itself is pinned at load.

## 5. Invariance (unchanged)

- **RNG and chains:** `SeedSequence(2026101601).spawn(2)` and two `default_rng` chains. The two initial paths are empty at the seed state.
- **Sweeps:** 64 burn-in and 256 measured.
- **Moves:**
  - 5 moves/sweep, with rotation .10, whole-circle .05 and the length components;
  - palette .35 over singleton owner palettes;
  - pair schedule .50/.10/.35/.05, insertion/deletion .50/.50 and local palette;
  - occupancy/base .50/.50 on the frozen graph0 roster, with the patch, restore and concurrency guard.
- **Caps, error parameters and tolerances:** unchanged.
- **Physical registration:** L=4, port cache, A/B port frame, whitening, max_cached_graphs and source directions. The j_R/j_S sources are zero and the source tolerance is unchanged.
- **Native model/operator:** unchanged. All-k L=4, `implicit_closure=None`, no W2.
- **Progress journal:** the fsync'd `progress_sink`, with `progress.jsonl` opened with `'x'`.
- **Soft budget:** `budget_state` stops at ≥1740 s, ≥900 MiB peak RSS or ≥300000 primitive calls.
- **Hard monitor:** `hard_monitor_required={'wall_seconds':1800,'rss_bytes':1073741824}`.
- **Sampler V001 to V002:** the full diff was read. Only the module tag, the optional keyword, configure, the pre-commit capture, and the raw rows/metadata in the complete and partial outputs change. `_move`, `_budget_check` and the other transition internals are unchanged.
- **Statistics:** has no RNG or random tokens. `capture` mutates neither `path` nor `allk_row`.
- **Transition law:** proposals, acceptance and the RNG stream are unchanged. Only wall time, and with it the budget-stop point, differs.

## 6. Raw/partial preservation and returned row layout

- **Complete run:** `sampler_result.reweighting_statistics = {metadata, series:[{chain, chain_ids, measurement_ids, features[256,1441]}×2], scope}`.
- **Incomplete run (budget/cap):** `partial.chains[c].reweighting` (ids plus `features[:n]`) and `partial.reweighting_metadata`. A budget `_Stop` raised inside capture is not converted to failed, because `_Stop` subclasses `Exception` and not ValueError/TypeError/KeyError.
- **Worker output:** saves the whole sampler dict, copies status verbatim and keeps `coefficients_accepted_for_galaxy: False`. There is no retry, checkpoint framework or acceptance promotion.
- **Row width:** 21·64 + 92 + 5 = 1441 float64. n_contact=92 was verified in `_allk_setup`: 8 self-conjugate blocks ×1 plus 28 pair blocks ×3. The author's storage figures are confirmed:
  - 5,902,336 B of rows plus 8,192 B of ids;
  - about 1.94× the existing all-k rows (3,043,328 B);
  - worker JSON about 14–30 MB at 14/16-space indent;
  - `clean()` transient about 24–30 MB.

## Blocking issues

None.

## Notes (non-blocking; for the root)

- **N1 (inherited, R2).** A capture ValueError, TypeError or KeyError makes V002 status `failed`, and V002 returns no committed prefixes for `failed`. Any other exception class escapes to the worker's FAILED record. Either way, committed rows are lost. Statically, the rate and feature checks hold at this trial (§3), so the expected trigger is a premise or registration surprise. Fixing this needs a sampler revision, which is outside 0423.
- **N2 (indivisible).** The worker's post-return `clean()` and `json.dump(indent=2)` are not budget-polled. With indent set, `json.dump` uses the pure-Python encoder over roughly 0.74 M added values (about 1.2 M or more in total). The 60 s / about 124 MiB margin to the hard monitor has not been measured. A kill mid-dump leaves invalid JSON, and `progress.jsonl` (counters only) is then the only durable record.
- **N3 (cost accounting).** Capture's direct private operator calls count toward neither the 300000 primitive-call counter nor the channel-enumeration cap. Only wall time and RSS bound them. They also touch the 4-graph LRU. This affects performance only, since rebuilds are exact. The `budget_checks` diagnostic counter will exceed base-V009 values by one per captured segment.
- **N4 (premise).** Uniform h/t is an attestation plus a structural accessor check. `configure` does not check accessor profiles, so the premise is recorded and not shown empirically.
- **N5 (documentary).** The new worker docstring retains the base line saying recipe V009 is frozen to "separately reviewed bytes". The C2V001 recipe bytes are reviewed only by this review. This has no functional effect.
- **N6 (pre-existing).** Load TOCTOU: the bytes are hashed, then the file is re-read on exec. The hard monitor is a launch requirement carried in `prepared` and is not enforced by the worker, the same as in the base.

The root alone chooses and launches.
