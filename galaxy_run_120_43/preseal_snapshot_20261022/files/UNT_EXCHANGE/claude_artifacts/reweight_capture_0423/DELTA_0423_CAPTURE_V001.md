# DELTA 0423 CAPTURE V001: recipe V009 and worker V007 bound to the existing pairallk V002 reweighting_capture

Author: Claude (0423 author, not the 0422 author). Static inspection only. The author did not import, execute or sample with the recipe, worker, sampler, statistics, operator, adapter or occupancy modules. No fixture sampling, target velocities, refit, cloud, network or retries. This file contains no acceptance, review verdict or launch decision. A distinct helper reviews the deltas, and the root alone chooses and launches.

## 1. Binding inputs (sha256 computed from bytes, all matched)

| role | path | sha256 |
|---|---|---|
| task 0423 | /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0423_2026-10-16_actual_reweight_capture_binding.md | cf561cec76f8015ac15589eaa95250743ff3e52bf93955dd3592c7005672180f |
| base recipe V009 | B/helpers/coefficient_method/owned_L4_uniform_trial_launch_recipe_v009.py | 44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697 |
| sampler pairallk V002 | B/helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v002.py | bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba |
| statistics V001 | B/helpers/coefficient_method/owned_uniform_reweighting_statistics_v001.py | 85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a |
| base worker V007 | B/CODEX1/owned_L4_collective_response_root_worker_v007.py | d691efbb9f62ded53ccde5076af45fe027c5f7456cf21126071f5ce827a7f17e |
| capture review | B/helpers/recovered_packet_audit/OWNED_UNIFORM_REWEIGHTING_CAPTURE_DISTINCT_REVIEW_V001.json | aabea1dcd5fee2c5ed7c7c41438dbf58af1e6388919ed82f6b04969874d368fb |
| current-pin revalidation | B/helpers/recovered_packet_audit/OWNED_UNIFORM_REWEIGHTING_CURRENT_PIN_REVALIDATION_V001.json | b10b91f16efc7e3b4eccbd7f12773f66057a3ad4843a7fbecb4ab617a158eef1 |
| operator V003 (recipe pin operator_v003) | /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_retained_response_0405/owned_parent_operator_v003.py | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 |
| adapter V001 (recipe pin diamond_adapter_v001) | B/helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 |
| occupancy V002 (recipe OCCUPANCY_SHA256) | B/helpers/recovered_packet_audit/owned_worldline_occupancy_involution_v002.py | 7f76641c2e1b442557b614e3d8cd6607c21defd7da64de0b1756a732588d9ff5 |
| prior sampler pairallk V001 (diff base only) | B/helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v001.py | 1907a397d69cdd0a508a00fb0a858aab9c914e4bcf126b079c1f491cbb10e2b9 |

B = /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13

The V001-to-V002 sampler diff was read in full. V002 changes only the module tag, adds the optional `reweighting_capture=None` keyword, configures capture after all-k setup, captures one row before each shared measurement commit, and retains `reweighting` prefixes and `reweighting_metadata` in `partial`. It changes no `_move`, `_budget_check`, `_event_from_channel` or other internal used by occupancy V002.

## 2. New files (exclusive create)

| file | sha256 |
|---|---|
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/reweight_capture_0423/owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py | a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95 |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/reweight_capture_0423/owned_L4_collective_response_root_worker_v007_capture_c2v001.py | 6c62b8ad1520a1ccafaeac8cb64cbb52c8a6f13763afe974175827c72cc6cc19 |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/reweight_capture_0423/DELTA_0423_CAPTURE_V001.md | this file (cannot contain its own hash) |

The worker pins the recipe at a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95.

## 3. API binding as written

Recipe `prepare` (new required keyword `statistics_module`, with no default):

```python
capture_args={'module':statistics_module,'operator_module':operator_module,
    'uniform_amplitudes':[float(abs(TRIAL[name])) for name in CAPTURE_AMPLITUDE_ORDER],
    'uniform_profile_attestation':CAPTURE_PROFILE_ATTESTATION,
    'rate_tolerance':CAPTURE_RATE_TOLERANCE}
...
    implicit_closure=None,budget_hook=lambda: bool(budget_state()['stop_requested']),
    progress_sink=progress_sink,reweighting_capture=capture_args)
```

Here `CAPTURE_AMPLITUDE_ORDER=('h','t','g','kappa','epsilon')` and `CAPTURE_RATE_TOLERANCE=1e-12`. `operator_module` is the same object that `prepare` uses for the guarded `operator_api` and for `diagonal_read_source_callback['operator_module']`. The amplitudes are `abs()` of the unchanged `TRIAL` entries, so no new values are introduced.

`run_prepared` calls `prepared['sampler'](**args)` exactly as before. The sampler V002 then calls (sampler lines 5101-5110 and 5255-5263, unchanged):

```python
reweighting_capture["module"].configure(run=run, operator_module=reweighting_capture["operator_module"],
    uniform_amplitudes=reweighting_capture["uniform_amplitudes"],
    uniform_profile_attestation=reweighting_capture["uniform_profile_attestation"],
    rate_tolerance=reweighting_capture["rate_tolerance"])
# once per measured sweep, after _measure and _measure_allk, before the shared commit:
reweighting_capture["module"].capture(run=run, path=path, allk_row=allk_row,
    operator_module=reweighting_capture["operator_module"],
    budget_check=_budget_check, metadata=run["reweighting_metadata"])
```

The capture key set equals the V002 contract exactly: {module, operator_module, uniform_amplitudes, uniform_profile_attestation, rate_tolerance}. An AST check found that the recipe's 28 sampler keywords equal V002's 28 keyword-only parameters. The 27 pre-existing keyword values are AST-identical to V009, and the only added keyword is `reweighting_capture`. The statistics keyword-only signatures are configure(run, operator_module, uniform_amplitudes, uniform_profile_attestation, rate_tolerance) and capture(run, path, allk_row, operator_module, budget_check, metadata).

Fail-closed guards (added, structural, no RNG):
- In `prepare`, model h, t and theta must each be `diamond_adapter.UniformEdgeProfile` with `L==4` and `value==TRIAL[name]`, and `statistics_module.AMPS` must equal the order h,t,g,kappa,epsilon.
- In `run_prepared`, the effective sampler pin must equal `CAPTURE_SAMPLER_SHA256` (pairallk V002 only). The capture module must be `prepared['statistics_module']`, and its operator must be the callback operator object. The amplitudes, attestation and tolerance are re-derived and compared. The statistics (85f4…), operator (a04f…) and adapter (0705…) bytes are re-hashed from `__file__`, in addition to the existing sampler and occupancy checks. All of this happens before `_move` is patched.
- Provenance is added only: `result['recipe_reweighting_capture']` from the recipe after return and `result['reweighting_capture_request']` from the worker after `prepare`. Status, ok, mixing, estimates, all-k and raw series are never touched.

The explicit uniform-profile attestation (`CAPTURE_PROFILE_ATTESTATION`) declares a premise. It is not evidence. It states that the model comes from adapter V001 `build_inputs(L=4, coefficients=TRIAL)`. h, t and theta are UniformEdgeProfile accessors that return the single TRIAL scalar for every ordered A-B edge, checked structurally in prepare. g and kappa are uniform vertex maps and epsilon is a uniform owner map, checked by statistics configure on the validated model. Lapse is uniform, pair sources are zero and uniform, and dstar, registration and phases are fixed. Each marked-event weight is compared with lapse times amplitude at rate_tolerance. Statically, the operator's admitted values for g, kappa and epsilon are `float`/`complex` of the TRIAL scalars, so the configure equality `abs(complex(v))==amp` holds exactly. Event W is `|amplitude| * (1 + sum n wbar)` with n=0, so it equals N·amp.

## 4. Pins loaded

The worker's `load()` checks the sha256 of the file bytes before `exec_module` for each source:

| key | path | sha256 |
|---|---|---|
| operator | X/owned_retained_response_0405/owned_parent_operator_v003.py | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 |
| sampler | B/helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v002.py | bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba |
| adapter | B/helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 |
| occupancy | B/helpers/recovered_packet_audit/owned_worldline_occupancy_involution_v002.py | 7f76641c2e1b442557b614e3d8cd6607c21defd7da64de0b1756a732588d9ff5 |
| recipe | X/reweight_capture_0423/owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py | a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95 |
| statistics | B/helpers/coefficient_method/owned_uniform_reweighting_statistics_v001.py | 85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a |

X = /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts. Before sampling, the recipe re-hashes `__file__` for the sampler (must be bd63…), occupancy (7f76…), statistics (85f4…), operator (a04f…) and adapter (0705…). Every pin was recomputed from current bytes by the author on 2026-10-16.

## 5. Preserved invariants (unchanged bytes or AST-identical)

- `TRIAL` (all 19 entries), `DRAFT_SOURCE_PINS`, `OCCUPANCY_SHA256` and `FINAL_MERGED_SAMPLER_SHA256=None` (root still supplies the pin through `accepted_sampler_sha256`, and the worker passes V002) are unchanged. These are AST-identical constants.
- Physical registration is unchanged: L=4, port_cache_entries 4096, port_vectors A/B frame, whitening, max_cached_graphs 4, uniform phi=1 lapse and nine source directions, zero whitened j_R/j_S, and source_consistency_tolerance.
- `SeedSequence(2026101601).spawn(2)`, two `default_rng` chains and two empty initial paths at the seed state are unchanged.
- burn_in_sweeps 64 and measurement_sweeps 256. moves_per_sweep 5, rotation .10, whole_circle .05, length components. Palette .35 over the singleton owner palettes. Pair schedule pair .50, rotation .10, palette_regrowth .35, full_regrowth .05, insertion/deletion .50/.50 and local_palette.
- Occupancy/base mixture .50/.50 on the frozen graph0 edge roster, the `_move` patch and restore, and the concurrency guard are unchanged.
- caps (10000 events per path, 300000 total, 640 sweeps, 300000 enumerations), error_parameters and numerical_tolerances are unchanged.
- All-momentum is L=4 over the same cells. `implicit_closure=None`, with no W2 or two-hop.
- Progress journal: the durable fsync'd `progress_sink` via `documentary_payload`, with the worker opening `progress.jsonl` exclusively next to the output.
- Resource checks: soft stop at elapsed ≥1740 s, peak RSS ≥900 MiB or ≥300000 primitive calls. `hard_monitor_required={'wall_seconds':1800,'rss_bytes':1073741824}`.
- `_verified_module`, `documentary_payload`, `normalize_complete_derivatives`, `convert_uniform_background`, `background_from_completed_outputs` and `background_from_allk_outputs` are AST-identical.
- Worker: exclusive output reservation, the whole sampler dict saved as `result['sampler_result']`, `status` copied verbatim, `coefficients_accepted_for_galaxy: False`, the exception/traceback record, `runtime_counters`, `budget_at_return`, `clean()` and no retry. There is no checkpoint framework and no acceptance promotion.

## 5a. Unchanged transition law

Capture draws no RNG. Its operator calls (`_admit_state`, `_require_coverage`, `_diagonal_items`, `_full_scope`, `_native_weights`) only fill pure per-graph caches, and the V003 LRU rebuilds exactly. Proposals, acceptance, the RNG stream and measurement targets are therefore those of V009 with V001. Only wall time changes, and with it the sweep at which a cooperative budget stop can occur.

## 6. Returned row layout and where it lands

The row width is `21*n_cells + n_contact + 5`. With L=4 there are n_cells=64 cells. n_contact=92: 8 self-conjugate k contribute 1 entry each and 28 (k,-k) pair blocks contribute 3 each, which matches `_allk_setup`. That gives **1441 float64 per row**:

- A: 11×64 = 704, name-major in the order Delta, Ud, epsilon_c, epsilon_r, lambda_J, lambda_R, E_R, E_S, e_R, e_I, C_identity (normalized dwell integrals).
- R: 64×9 = 576, cell-major raw whitened time averages (the all-k score_cells read columns divided by beta).
- B: 64 (N·rho event weights).
- C: 92 (−N²·all-k NN contacts).
- counts: 5 (flip, hop, bind, admit+admit_rev, birth+birth_rev).

- On complete: `sampler_result.reweighting_statistics = {metadata, series:[{chain, chain_ids[256], measurement_ids[256], features[256,1441]} ×2], scope}`. This sits beside the unchanged `all_momentum.series` and the v004 outputs.
- On incomplete (budget or cap): `reweighting_statistics.series` is None. The committed prefixes are in `sampler_result.partial.chains[c].reweighting` (chain_ids, measurement_ids, features[:n]) with `partial.reweighting_metadata`, beside `partial.chains[c].all_momentum` and the v004 prefixes.
- On failed: `failures` holds the message, and metadata is present only if configure succeeded. V002 returns no prefixes for failed stops (see risk R2).

## 7. Storage estimate for 512 rows (2 chains × 256), from the layout

- In memory: features 512×1441×8 = 5,902,336 B (5.63 MiB; 2,951,168 B per chain), plus ids 2×512×8 = 8,192 B. For comparison, the existing all-k rows take 512×(741×8+16) = 3,043,328 B, so capture is about 1.9× that.
- Worker JSON (`json.dump(indent=2)`, one value per line, 14-space indent on the complete path and 16 on the partial path): 737,792 values at roughly 19–40 B each. Complete: about 14.0–29.5 MB. Partial with 512 rows: about 15.5–31.0 MB. This range runs from short reprs such as `0.0` to 24-character full-precision floats. The ids add about 20 KB and the metadata/attestation copies a few KB. Expect a realistic total near the upper part, since most A/R entries are full-precision.
- Worker `clean()` transient: about 24–30 MB of Python float and list objects for the capture rows, in addition to the existing all-k and v004 copies.

## 8. Added runtime and memory cost (qualitative, no measurement)

Per measured sweep, capture makes one more pass over every path segment. Each pass parses and admits the state (`_admit_state`, which can rebuild graph info when the 4-graph LRU misses), builds the full-scope diagonal item list (edges, vertices, donors and identity), looks up native weights, and does scalar numpy accumulation, plus one budget-hook call (getrusage) per segment. The cost is comparable to or larger than the existing `_measure` diagonal pass and grows with events per path. Warmup sweeps are unaffected. Memory adds about 5.6 MiB of committed row storage and small per-call temporaries. The operator caches remain bounded by the existing LRU. The capture's direct private operator calls are not counted in the recipe's 300000 primitive-call counter, so they are bounded only by the wall and RSS checks. The extra time means that under the same 1740 s budget a cooperative stop can occur at an earlier sweep than base V009. Nothing guarantees completion, mixing or performance.

## 9. Risks (including indivisible calls)

- R1, indivisible calls. Inside capture, the budget checkpoint precedes each segment. Each segment's operator private calls, and the final R/B/C assembly after the last segment, cannot be interrupted, though they are small and bounded. The sampler's final `_analyze` and `_allk_analyze` cannot be interrupted either (pre-existing), and capture adds no analysis. The largest indivisible step is the worker's post-return `clean()` plus streaming `json.dump`, which the soft budget no longer polls. Capture adds about 14–31 MB of JSON and about 24–30 MB of transient objects to it. After a late soft stop (≥1740 s or ≥900 MiB), this must finish within the 60 s and about 124 MiB margin to the 1800 s and 1 GiB hard monitor. A hard kill mid-dump leaves a truncated, invalid output JSON. Then `progress.jsonl` (per-sweep counters only, no rows) is the only durable record.
- R2, failure modes that lose rows (inherited from V002 and the statistics module, not changed here). A capture ValueError, TypeError or KeyError becomes sampler status `failed`. Examples are a marked weight outside lapse×amplitude at 1e-12 relative, an unregistered kind, or a malformed path. V002 attaches `partial` prefixes only for `incomplete` stops, so the committed all-k and raw rows of such a run are not returned. Any other exception class from capture or the operator private calls escapes the sampler entirely, for example IndexError, AttributeError or MemoryError. The worker then records FAILED with a traceback, and the in-memory series is lost. Changing this needs a new sampler revision, which is a root decision.
- R3, premise. Uniform h/t is an attestation plus a structural accessor check. It is not established empirically, and configure skips accessor profiles. A wrong premise for hop or flip magnitude fails closed at the first measured hop or flip event, after chain-0 warmup.
- R4, budget interplay. The same soft budget is shared with the added capture work, so a stop becomes INCOMPLETE_BUDGET with shorter prefixes more readily. Those prefixes are diagnostics only, not unbiased estimates.
- R5, load TOCTOU (pre-existing pattern). `load()` hashes the bytes and then `exec_module` re-reads the file, and the recipe re-hashes `__file__` later. A file replaced between the reads is not excluded by construction.
- R6, scope. The previous finite response stays frozen with failed mixing. Capture does not repair mixing. The rows support later independent calibration or background evaluation only after separate review. ESS, overlap and acceptance are not established, and nothing is promoted.

## 10. AST results

The author copied both destination files into a separate scratch directory. There `python3 -I -B` (3.9.6) ran `ast.parse` and `compile(text, name, 'exec')` on the text. Nothing was imported or executed, and no `__pycache__` or `.pyc` exists in reweight_capture_0423.

- recipe a0a24bb0…: ast.parse OK, compile OK. Top-level functions: prepare, _verified_module, run_prepared, documentary_payload, normalize_complete_derivatives, convert_uniform_background, background_from_completed_outputs, background_from_allk_outputs. The keyword-only parameters of prepare are operator_module, sampler_module, diamond_adapter, progress_stream, occupancy_module, statistics_module (all required) and accepted_sampler_sha256 (default None).
- worker 6c62b8ad…: ast.parse OK, compile OK. Top-level functions: load, clean, main. SOURCES has 6 entries.
- AST comparisons against the bases: V009 constants identical. Six helper functions identical. The 27 pre-existing sampler keywords identical. Only `reweighting_capture` added. The keyword set equals the V002 signature.

Changed lines: the recipe has +64/−3 lines (diff below) and the worker +11/−3.

## 11. diff -u from the bases

### Recipe (base V009 to capture C2V001)

```diff
--- /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_L4_uniform_trial_launch_recipe_v009.py
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/reweight_capture_0423/owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py
@@ -1,4 +1,6 @@
-"""INERT V009: root occupancy plus pair/all-k attempt; final sampler pin required.
+"""INERT V009 CAPTURE C2V001 (UNT 0423): V009 plus ONLY the pairallk V002 reweighting_capture.
+Base V009 sha256 44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697.
+INERT V009: root occupancy plus pair/all-k attempt; final sampler pin required.
 Run fails closed until root supplies the accepted final sampler SHA256.
 Fixed state-independent outer mixture: occupancy .50, existing base _move .50.
 Base pair/rotation/palette/full probabilities remain unchanged. No W2/open sector.
@@ -7,6 +9,13 @@
 local pair palette and insertion/deletion .50/.50. Soft1740s/900MiB,
 hard1800s/1GiB. This is NOT the abandoned unchanged longer V007 trial.
 No import, compile, execution or sampling by author.
+0423: sampler must be pairallk V002 (the only reviewed capture bytes); its existing
+reweighting_capture binds statistics V001 and the SAME operator V003 module; sampler,
+occupancy, statistics, operator and adapter are re-hashed from __file__ bytes before
+sampling. Amplitudes are abs(TRIAL[x]), x in h,t,g,kappa,epsilon (same trial, no new
+values); explicit uniform-profile attestation; rate_tolerance 1e-12. Trial, registration,
+seeds, chains, sweeps, mixture, moves, caps, budgets, journal and helpers are unchanged.
+Raw rows are evidence only: no reweighting, overlap, mixing or calibration acceptance.
 """
 import time
 import resource
@@ -25,13 +34,30 @@
  'sampler_v004':'6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea',
  'diamond_adapter_v001':'0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77',
  'prior_recipe_v004':'23d9ea3f1c622c2d16b98704510ea366ed647628f07c26ad8caf68bf72448500'}
+# UNT 0423 capture pins (author verified from bytes; run_prepared re-hashes __file__ bytes).
+BASE_RECIPE_V009_SHA256='44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697'
+CAPTURE_SAMPLER_SHA256='bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba'  # pairallk V002
+STATISTICS_SHA256='85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a'  # reweighting statistics V001
+OPERATOR_SHA256=DRAFT_SOURCE_PINS['operator_v003']
+ADAPTER_SHA256=DRAFT_SOURCE_PINS['diamond_adapter_v001']
+CAPTURE_AMPLITUDE_ORDER=('h','t','g','kappa','epsilon')
+CAPTURE_RATE_TOLERANCE=1e-12
+CAPTURE_PROFILE_ATTESTATION=(
+ 'UNT 0423 declared uniform-amplitude family (a premise, not empirical evidence): model from '
+ 'diamond adapter V001 build_inputs(L=4, coefficients=TRIAL); h, t and theta are adapter '
+ 'UniformEdgeProfile accessors returning the single TRIAL scalar for every ordered A-B edge '
+ '(class, L and value checked in prepare); g and kappa are uniform maps over every vertex and '
+ 'epsilon a uniform map over every original owner, of the same TRIAL scalars (checked by '
+ 'statistics configure on the validated model); uniform lapse factors, zero uniform pair '
+ 'sources, fixed dstar, registration and gauge phases. Marked-event weights are compared '
+ 'with lapse times amplitude at rate_tolerance.')
 TRIAL=dict(Ud=1.,dstar=2.,Delta=1.,lambda_J=.1,lambda_R=.1,
  epsilon_c=.3,epsilon_r=.3,E_R=.1,E_S=.1,E_I=.1,e_R=.1,e_I=.1,
  C_identity=0.,h=.1,t=.1,g=.1,kappa=.1,epsilon=.1,theta=0.)
 
 
 def prepare(*,operator_module,sampler_module,diamond_adapter,progress_stream,
-            occupancy_module,accepted_sampler_sha256=None):
+            occupancy_module,statistics_module,accepted_sampler_sha256=None):
     if progress_stream is None:
         raise ValueError('Caller must supply an open durable progress journal')
     def progress_sink(*,record):
@@ -50,6 +76,12 @@
     A=set(binding['graph0']['A']); B=set(binding['graph0']['B'])
     if any(len(e)!=2 or e[0] not in A or e[1] not in B for e in edge_roster):
         raise ValueError('Frozen graph0 edges must be ordered A-to-B')
+    for name in ('h','t','theta'):  # 0423: declared uniform accessor family, structural only
+        prof=binding['model'][name]
+        if type(prof) is not diamond_adapter.UniformEdgeProfile or prof.L!=4 or prof.value!=TRIAL[name]:
+            raise ValueError('0423 capture: model '+name+' is not the declared uniform TRIAL accessor')
+    if tuple(statistics_module.AMPS)!=CAPTURE_AMPLITUDE_ORDER:
+        raise ValueError('0423 capture: statistics amplitude order is not h,t,g,kappa,epsilon')
     cells=reg['cells']; clock={'start':time.monotonic(),'primitive_calls':0}
     def budget_state():
         rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
@@ -80,6 +112,19 @@
           'j_S':{c:[[0.,0.,0.] for _ in range(3)] for c in cells},
           'source_consistency_tolerance':1e-12}
     owners=tuple(binding['graph0']['A'])+tuple(binding['graph0']['B'])
+    capture_args={'module':statistics_module,'operator_module':operator_module,
+        'uniform_amplitudes':[float(abs(TRIAL[name])) for name in CAPTURE_AMPLITUDE_ORDER],
+        'uniform_profile_attestation':CAPTURE_PROFILE_ATTESTATION,
+        'rate_tolerance':CAPTURE_RATE_TOLERANCE}
+    capture_record={'sampler_sha256':CAPTURE_SAMPLER_SHA256,'statistics_sha256':STATISTICS_SHA256,
+        'operator_sha256':OPERATOR_SHA256,'adapter_sha256':ADAPTER_SHA256,
+        'base_recipe_sha256':BASE_RECIPE_V009_SHA256,
+        'amplitude_order':list(CAPTURE_AMPLITUDE_ORDER),
+        'amplitude_source':'abs(TRIAL[name]) of the same trial; no new values',
+        'uniform_amplitudes':list(capture_args['uniform_amplitudes']),
+        'uniform_profile_attestation':CAPTURE_PROFILE_ATTESTATION,
+        'rate_tolerance':CAPTURE_RATE_TOLERANCE,
+        'scope':'raw per-path capture binding only; no reweighting, overlap, mixing or calibration acceptance'}
     seeds=np.random.SeedSequence(2026101601).spawn(2)
     args=dict(operator_api=api,graph0=binding['graph0'],model=binding['model'],registration=reg,
         initial_paths=[{'x0':binding['seed_state'],'events':[]} for _ in range(2)],
@@ -104,10 +149,11 @@
             'palette_regrowth':.35,'full_regrowth':.05},
             'insertion_probability':.50,'deletion_probability':.50,'local_palette':True},
         implicit_closure=None,budget_hook=lambda: bool(budget_state()['stop_requested']),
-        progress_sink=progress_sink)
+        progress_sink=progress_sink,reweighting_capture=capture_args)
     return {'arguments':args,'sampler':sampler_module.owned_collective_worldline_static_response,
         'binding':binding,'budget_state':budget_state,'counters':clock,'cell_count':64,
         'sampler_module':sampler_module,'occupancy_module':occupancy_module,
+        'statistics_module':statistics_module,'reweighting_capture_record':capture_record,
         'accepted_sampler_sha256':accepted_sampler_sha256,'edge_roster':edge_roster,
         'mixture_counters':{},
         'cooperative_binding_status':'FINAL_ACCEPTED_SAMPLER_PIN_REQUIRED_BEFORE_RUN',
@@ -133,12 +179,26 @@
     Preserve the entire returned sampler dictionary, including partial arrays;
     the worker serializes documentary_payload(result) without requiring estimates.
     Source-byte checks assume modules were loaded from those unchanged files.
+    0423: only the pairallk V002 pin is admitted; statistics, operator and adapter bytes
+    are checked too. Capture rows stay inside the returned sampler dictionary verbatim.
     """
     sampler=prepared['sampler_module']; occupancy=prepared['occupancy_module']
     expected=prepared['accepted_sampler_sha256'] or FINAL_MERGED_SAMPLER_SHA256
+    if expected!=CAPTURE_SAMPLER_SHA256:
+        raise RuntimeError('0423 capture binds only the reviewed pairallk V002 sampler bytes')
     _verified_module(sampler,expected,'final merged sampler')
     _verified_module(occupancy,OCCUPANCY_SHA256,'occupancy V002')
     args=prepared['arguments']
+    capture=args.get('reweighting_capture'); callback=args['diagonal_read_source_callback']
+    if (not isinstance(capture,dict) or capture.get('module') is not prepared['statistics_module']
+            or capture.get('operator_module') is not callback['operator_module']
+            or capture.get('uniform_amplitudes')!=[float(abs(TRIAL[n])) for n in CAPTURE_AMPLITUDE_ORDER]
+            or capture.get('uniform_profile_attestation')!=CAPTURE_PROFILE_ATTESTATION
+            or capture.get('rate_tolerance')!=CAPTURE_RATE_TOLERANCE):
+        raise RuntimeError('0423 capture must bind prepared modules, TRIAL amplitudes, attestation, tolerance')
+    _verified_module(capture['module'],STATISTICS_SHA256,'uniform reweighting statistics V001')
+    _verified_module(capture['operator_module'],OPERATOR_SHA256,'operator V003')
+    _verified_module(callback['adapter'],ADAPTER_SHA256,'diamond adapter V001')
     if args.get('implicit_closure') is not None or any(k in args for k in ('two_hop_parameters','w2_parameters')):
         raise RuntimeError('Occupancy recipe admits only ordinary closed-path sampling')
     if prepared['sampler'] is not sampler.owned_collective_worldline_static_response:
@@ -175,6 +235,7 @@
             'occupancy_sha256':OCCUPANCY_SHA256,'sampler_sha256':expected,
             'frozen_graph0_edge_roster':roster,'outcomes':dict(counts),
             'scope':'ordinary closed paths; full raw sampler result retained'}
+        result['recipe_reweighting_capture']=dict(prepared['reweighting_capture_record'])
         return result
     finally:
         sampler._move=base_move
```

### Worker (base V007 to capture C2V001)

```diff
--- /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/owned_L4_collective_response_root_worker_v007.py
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/reweight_capture_0423/owned_L4_collective_response_root_worker_v007_capture_c2v001.py
@@ -1,5 +1,10 @@
 """Inert preparation for one root-owned, bounded collective-response attempt.
 
+UNT 0423 CAPTURE C2V001: worker V007 (sha256
+d691efbb9f62ded53ccde5076af45fe027c5f7456cf21126071f5ce827a7f17e) plus ONLY the raw
+reweighting capture binding: sampler pairallk V002, statistics V001 and recipe V009
+capture C2V001 are pinned and checked from bytes at load; the full sampler dictionary,
+including reweighting_statistics and partial prefixes, is saved unchanged. No acceptance.
 Merged sampler and recipe V009 are frozen to separately reviewed bytes. Entire raw sampler output is
 saved before any downstream scientific conversion; no automatic retry or fit.
 """
@@ -17,10 +22,11 @@
 X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
 SOURCES = {
     'operator': (X/'owned_retained_response_0405/owned_parent_operator_v003.py', 'a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07'),
-    'sampler': (B/'helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v001.py', '1907a397d69cdd0a508a00fb0a858aab9c914e4bcf126b079c1f491cbb10e2b9'),
+    'sampler': (B/'helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v002.py', 'bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba'),
     'adapter': (B/'helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py', '0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77'),
     'occupancy': (B/'helpers/recovered_packet_audit/owned_worldline_occupancy_involution_v002.py', '7f76641c2e1b442557b614e3d8cd6607c21defd7da64de0b1756a732588d9ff5'),
-    'recipe': (B/'helpers/coefficient_method/owned_L4_uniform_trial_launch_recipe_v009.py', '44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697'),
+    'recipe': (X/'reweight_capture_0423/owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py', 'a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95'),
+    'statistics': (B/'helpers/coefficient_method/owned_uniform_reweighting_statistics_v001.py', '85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a'),
 }
 
 
@@ -67,8 +73,10 @@
                 print('Preparing full-owned L4 collective response', flush=True)
                 prepared = recipe.prepare(operator_module=modules['operator'],
                     sampler_module=modules['sampler'], diamond_adapter=modules['adapter'],
-                    occupancy_module=modules['occupancy'], progress_stream=progress,
+                    occupancy_module=modules['occupancy'], statistics_module=modules['statistics'],
+                    progress_stream=progress,
                     accepted_sampler_sha256=SOURCES['sampler'][1])
+                result['reweighting_capture_request'] = prepared['reweighting_capture_record']
                 print('Sampling two chains with occupancy, event-pair and regrowth moves', flush=True)
                 sampled = recipe.run_prepared(prepared=prepared)
             # Preserve every actual returned row, status and uncertainty result.
```
