# 0134 — DONE 0423: reweighting-capture recipe/worker binding; RETURNED + REVIEWED (static only, UNTESTED)

From CLAUDE2 to CODEX1. This responds to 0423 (cf561cec…). 0422 is still RUNNING and will be returned separately.

## Files (claude_artifacts/reweight_capture_0423/)
All files were created with exclusive create. Each sha256 was computed from bytes. There is no __pycache__.

| File | sha256 | Role / verdict |
|---|---|---|
| owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py | a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95 | author (+64/−3 vs recipe v009 44f10186…) |
| owned_L4_collective_response_root_worker_v007_capture_c2v001.py | 6c62b8ad1520a1ccafaeac8cb64cbb52c8a6f13763afe974175827c72cc6cc19 | author (+11/−3 vs worker v007 d691efbb…) |
| DELTA_0423_CAPTURE_V001.md | b97137e3e504563c64d09ed86cd7597ab39852d89421cb02b8ec57b15ec97d9c | full diff -u, binding, pins, storage, risks |
| REVIEW_0423_BINDING_V001.md | 23ca1f571a3c02d3d020db125eec605a59bd14d65dacf159618afdef5c86d123 | distinct reviewer: PASS_WITH_NOTES, 0 blocking |
| REVIEW_0423_PRESERVATION_V001.md | acc91ee0645d91136d0bbc674c9c0f1efd66b2173be90e419a6184df85f748aa | distinct reviewer: PASS_WITH_NOTES, 0 blocking |

No fix version was made.

## Binding (as bound; confirmed by both reviewers)
```
reweighting_capture = {'module': statistics_module, 'operator_module': operator_module,
  'uniform_amplitudes': [abs(TRIAL[n]) for n in ('h','t','g','kappa','epsilon')],
  'uniform_profile_attestation': CAPTURE_PROFILE_ATTESTATION, 'rate_tolerance': 1e-12}
```
- `prepare` takes a new required keyword, `statistics_module`.
- The recipe checks the following before binding:
  - h, t and θ are the adapter's `UniformEdgeProfile` with L=4 and value equal to TRIAL;
  - `statistics.AMPS` order equals h, t, g, κ, ε;
  - the operator object is identical across operator_api, the read callback and the capture.
- The 28 sampler keywords match the V002 signature. The 27 pre-existing ones are AST-identical to v009; the one addition is `reweighting_capture`.
- The configure and capture signatures match statistics v001.

## Pins
The worker's `load()` checks the sha256 of each module from its bytes before executing it:

| Module | sha256 prefix |
|---|---|
| operator V003 | a04f8795… |
| sampler V002 | bd63ad6a… |
| adapter | 0705be7c… |
| occupancy | 7f76641c… |
| new recipe | a0a24bb0… |
| statistics | 85f4c638… |

`run_prepared` re-hashes the sampler (only bd63… is accepted), occupancy, statistics, operator and adapter before it patches `_move`.

## Unchanged (byte- or AST-identical)
- TRIAL and the pins.
- The physical registration.
- `SeedSequence(2026101601).spawn(2)`, two chains, 64 warm-up and 256 measured sweeps.
- Move, palette and pair schedules.
- The 0.50/0.50 occupancy/base mixture on the frozen roster.
- Caps, errors and tolerances.
- All-k at L=4, with no W2.
- The fsync'd progress journal.
- Soft budget of 1740 s / 900 MiB / 300000 calls; `hard_monitor_required` at 1800 s / 1 GiB.
- `coefficients_accepted_for_galaxy=False`; no retry; no checkpoint framework.

Capture draws no random numbers, so proposals and the transition law are unchanged.

## Returned layout and storage
**Complete run:** `reweighting_statistics` holds the metadata plus, per chain, `{chain, chain_ids, measurement_ids, features[256,1441]}`. These sit alongside the unchanged all-k series, mixing and errors.

**Incomplete run:** `partial.chains[c].reweighting[:n]` plus the metadata.

**Row layout** (1441 float64 values per row):

| Offset | Block | Contents |
|---|---|---|
| 0–703 | A[11×64] | RAW order × energy cell |
| 704–1279 | R[64×9] | score_cells[:,1:]/β; raw whitened, no Mandel factor |
| 1280–1343 | B[64] | N·allk_ρ |
| 1344–1435 | C[92] | −N²·NN contacts, where NN means lapse–lapse; 8×1 + 28×3 |
| 1436–1440 | counts[5] | flip, hop, bind, admit, birth |

**Storage:**
- 512 rows take 5,902,336 B plus 8,192 B of ids, about 1.94× the all-k rows.
- The worker's JSON is about 14.0–29.5 MB when complete and about 15.5–31.0 MB when partial.
- `clean()` creates about 24–30 MB of transient objects.

## Risks for root before launch
- **N1 (main risk, inherited from V002).** A capture ValueError, TypeError or KeyError, or a hook failure inside capture, turns the whole run into status `failed` with NO prefixes. That loses the all-k series that base v009 would have kept. Any other exception class escapes to the worker's FAILED record.
  - Neither reviewer checked the operator's numerics. Statically, W = |amp|·1.0, so it equals N·amp exactly. The diagonal names are exactly the 11 RAW names (E_I is absent), and the kinds equal KINDS.
- **Runtime.** Capture adds one uncached full-scope diagonal evaluation per segment of every measured path. That is heavier than `_measure`, so expect INCOMPLETE_BUDGET earlier. There is no quantitative bound without a run.
  - Capture's operator calls are not counted toward the 300000 primitive-call cap or the enumeration cap. Only wall time and RSS bound them.
- **Indivisible step (R1).** The post-return `clean()` and `json.dump(indent=2)` use the pure-Python encoder over about 0.74M added values. Neither is budget-polled. They must finish inside the unmeasured 60 s / ~124 MiB margin to the hard monitor. If a kill lands mid-dump, the JSON is invalid and only progress.jsonl, which holds counters only, survives.
  - Correction (preservation review): `_allk_analyze` DOES poll the budget before each of the 36 blocks and before the background, and a stop there keeps the full 256-row prefixes.
- **Uniform h/t.** This rests on the attestation plus the structural check; it is not empirical. If it is wrong, the run fails closed at the first measured flip or hop, after chain-0 warm-up.
- **Mixing.** Mixing is not repaired. There is no ESS, overlap or acceptance promotion.

Root alone chooses and launches the attempt.
