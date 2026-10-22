# REVIEW 0423 PRESERVATION V001: raw/partial preservation, returned row layout, storage and resources

Role: distinct reviewer, not author. This was a static inspection only. The reviewer did not import or execute the recipe, worker, sampler, statistics, operator, adapter or occupancy modules. There was no sampling, fixture, target velocity, refit, cloud, network or retry. `ast.parse` and `compile` ran only on text copies in the reviewer's own scratch directory (`python3 -I -B`, 3.9.6). Nothing was written to the 0423 directory except this file. The root alone chooses and launches.

**Verdict: PASS_WITH_NOTES. There are no blocking issues.**

## 1. Hashes recomputed from bytes (all match the brief and the author report)

| item | sha256 |
|---|---|
| task 0423 | cf561cec76f8015ac15589eaa95250743ff3e52bf93955dd3592c7005672180f |
| base recipe V009 | 44f1018682ef860f1ad5a4f4377210bec44947835249138bfbb33ac157a16697 |
| sampler pairallk V002 | bd63ad6a32de07a7cfbf6983a306b74dff2e51e33b9d63c4f8fc9eb1b3e638ba |
| statistics V001 | 85f4c638eb28361f806421048d9adbebff3ea0f1e02237029d7e0b947342638a |
| base worker V007 | d691efbb9f62ded53ccde5076af45fe027c5f7456cf21126071f5ce827a7f17e |
| capture distinct review | aabea1dcd5fee2c5ed7c7c41438dbf58af1e6388919ed82f6b04969874d368fb |
| current-pin revalidation | b10b91f16efc7e3b4eccbd7f12773f66057a3ad4843a7fbecb4ab617a158eef1 |
| operator V003 (recipe `DRAFT_SOURCE_PINS['operator_v003']`) | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 |
| adapter V001 | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 |
| occupancy V002 | 7f76641c2e1b442557b614e3d8cd6607c21defd7da64de0b1756a732588d9ff5 |
| sampler pairallk V001 (diff base only) | 1907a397d69cdd0a508a00fb0a858aab9c914e4bcf126b079c1f491cbb10e2b9 |
| NEW recipe `owned_L4_uniform_trial_launch_recipe_v009_capture_c2v001.py` | a0a24bb0ae946dfadb5e99d9bfeae1f188bf8cdd31809458d14b5cf6e8b2bf95 |
| NEW worker `owned_L4_collective_response_root_worker_v007_capture_c2v001.py` | 6c62b8ad1520a1ccafaeac8cb64cbb52c8a6f13763afe974175827c72cc6cc19 |
| NEW `DELTA_0423_CAPTURE_V001.md` | b97137e3e504563c64d09ed86cd7597ab39852d89421cb02b8ec57b15ec97d9c |

## 2. Delta and binding checks (static)

- **Diffs.** A recomputed `diff -u` gives recipe +64/−3 and worker +11/−3. Both match line for line the diffs embedded in DELTA §11.
- **AST of the recipe.**
  - Identical to base: `TRIAL`, `DRAFT_SOURCE_PINS`, `OCCUPANCY_SHA256`, `FINAL_MERGED_SAMPLER_SHA256`, all imports, and the six helpers (`_verified_module`, `documentary_payload`, `normalize_complete_derivatives`, `convert_uniform_background`, `background_from_completed_outputs`, `background_from_allk_outputs`).
  - Identical nested functions: `progress_sink`, `budget_state`, `guarded`, `tick` and `mixed_move`.
  - The sampler `dict(...)` has 27 keywords that are AST-identical to base, plus `reweighting_capture`. The resulting 28 equal V002's 28 keyword-only parameters.
  - The `prepare` return dict keeps every base key unchanged and in the same order, including `hard_monitor_required`. It adds only `statistics_module` and `reweighting_capture_record`.
  - In `run_prepared`, the try body is the base body plus one provenance assignment before `return`. `finally` is identical.
- **AST of the worker.** `load`, `clean`, `B` and `X` are identical. `SOURCES` swaps the sampler to V002 and the recipe to the new file, and adds `statistics`. `main` adds the `statistics_module=` argument and the `reweighting_capture_request` record.
- **Sampler V001 to V002.** The full diff confirms that V002 only:
  - changes the module tag (so the progress journal records now say `pairallk_v002`);
  - adds the keyword, configure, per-measurement capture before the shared commit, partial `reweighting` slices with `reweighting_metadata`, and the complete-path `reweighting_statistics.series`.

  `_move`, `_budget_check`, `_event_from_channel`, the RNG and caps are untouched.
- **Configure feasibility.** The structural premise holds statically:
  - The adapter builds h/t/theta as `UniformEdgeProfile(L=4, value=TRIAL[x])`. The operator admits them as `('accessor', …)`, and configure skips non-`map` h/t.
  - g, kappa and epsilon are uniform maps of float/complex TRIAL scalars, so the exact `abs(complex(v))==amp` test holds.
  - The lapse is uniform at 1 (`n_of_cell` is 0).
- **Rate check.** The marked weight is `W = |amp|·fsum([1.0]+[0·w])`, which equals `1·amp` exactly for all five families (theta = 0). The 1e-12 rate check should not trip on this trial. This is an expectation from reading the code, not a measurement.

## 3. Preservation (verified in V002 and statistics source)

| outcome | what the worker JSON keeps |
|---|---|
| complete | `sampler_result.reweighting_statistics = {metadata, series:[{chain, chain_ids[256], measurement_ids[256], features[256,1441]} ×2], scope}`, plus the unchanged `all_momentum.series` (chain_ids, measurement_ids, score_cells, contacts, background, events), blocks, `mixing` and `errors`. `errors` is `None` when mixing failed: the "unavailable" errors are kept as returned. |
| incomplete: budget or cap | `partial.chains[c].reweighting = {chain_ids, measurement_ids, features}[:n]`, `partial.reweighting_metadata`, the all-k and v004 prefixes, and the `stop` record. Rows count only after the whole tuple is written (v004, all-k, raw, then `measurements_committed += 1`, with no budget poll inside the commit). A `_BudgetStop` raised inside `capture` is a `_Stop(Exception)`, not a ValueError, so it bypasses the capture `except` and becomes INCOMPLETE_BUDGET with a valid prefix: measurement i is abandoned and `proposal_in_progress` is False. A budget stop during `_allk_analyze` returns all 256 rows per chain as prefixes. |
| failed or unsupported after configure | `failures` message, `diagnostics`, `reweighting_statistics.metadata` (series None) and the all-k metadata. No row prefixes (V002 `_stopped` attaches `partial` only for `incomplete`). |
| configure failure | status `failed` with "raw reweighting configuration: …". The sampler stops before initial paths. |
| exception escaping sampler | worker `FAILED` with type, message and traceback, plus `runtime_counters`. The `_move` patch is restored by `finally`. |

- **No acceptance promotion.**
  - Status is copied verbatim and `coefficients_accepted_for_galaxy` stays False.
  - Provenance is added only after return, and its scope text denies acceptance.
  - Neither new file calls `candidate_arrays`, `normalized_weights` or any ESS computation.
- **No checkpoint framework.** Only the exclusive output file and the exclusive `progress.jsonl` are written, and there is no resume.
- **Progress journal intact.** The `progress_sink` AST is identical (fsync'd, `documentary_payload`). Capture adds no progress records, only extra `budget_checks` counter increments.
- **JSON safety of the new content.** I checked every type:
  - Metadata: tuples of str; int; `float` beta, lapse and dstar (operator `_real`); lists of float; and `j_mandel`, which mixes floats and `np.float64`.
  - The capture record: str, float and lists.
  - Rows and ids: ndarrays.

  All of these survive `clean()` and `json.dump(allow_nan=False)`. Capture rows are checked finite before commit.

## 4. Returned row layout, field by field (statistics `capture` + V002 `_allk_setup` for L=4)

Here n_cells = 64. n_contact is 92: `np.ndindex(4,4,4)` gives k ≤ −k with 8 self-conjugate blocks of 1 entry (0,0) and 28 pair blocks of 3 entries (0,0),(0,1),(1,1). That gives 8 + 84 = 92, and the profiles total 64 = n_cells. The row width is `21·64+92+5 = 1441` float64, which `capture` checks against `metadata['row_width']`.

| offsets | n | field | definition |
|---|---|---|---|
| 0–703 | 704 | A[r,c] at r·64+c | Σ_segments (dwell/β)·feature·native weight, from operator `_diagonal_items(full scope)` and `_native_weights`. r runs in RAW order: Delta, Ud, epsilon_c, epsilon_r, lambda_J, lambda_R, E_R, E_S, e_R, e_I, C_identity. c is the integer energy-cell index: operator `cell_vid`/`cell_index` uses the same order as the sampler's `energy_cells` and `cell_pos`. |
| 704–1279 | 576 | R[c,f] at 704+9c+f | `allk_row[0].reshape(64,10)[:,1:]/β`: per-cell time-averaged whitened reads R0..2, S00, S11, S22, S12, S02, S01 (raw S, no Mandel factor). |
| 1280–1343 | 64 | B[c] | Σ_events N·`allk_rho` added at `allk_idx`. |
| 1344–1435 | 92 | C[j] | −N²·`allk_row[1]`: the all-k bare NN contacts, by block `contact_offset`. |
| 1436–1440 | 5 | counts | flip, hop, bind, admit+admit_rev, birth+birth_rev |

Each chain container is `{chain_ids:int64[256], measurement_ids:int64[256]}`, both initialized to −1, plus `features:float64[256,1441]`. Statistics `unpack` slices exactly this order. The author's DELTA §6 layout is correct.

## 5. Storage for 512 rows (recomputed; matches the author)

- **In memory.**
  - Features take 512·1441·8 = 5,902,336 B. They are allocated up front at chain start, 2,951,168 B per chain.
  - Ids take 2·512·8 = 8,192 B.
  - For comparison, the existing all-k rows take 512·(741·8+16) = 3,043,328 B, so capture is about 1.94× that.
- **Worker JSON (`indent=2`).** I confirmed the element indent: 14 spaces on the complete path (`sampler_result › reweighting_statistics › series › [i] › features › [row] › value`) and 16 on the partial path. Each value costs 19–40 B (`0.0` up to a 24-character repr, plus `,\n`) for 737,792 values:
  - complete: 14,018,048–29,511,680 B;
  - partial: 15,493,632–30,987,264 B.

  The ids add about 20 KB.
- **`clean()` transient.** At 32–40 B per value (tolist list, float objects and the cleaned list), the transient is about 23.6–29.5 MB.

## 6. Runtime, memory and indivisible-call statements: plausible, with corrections in the notes below

- Capture draws no RNG. Its operator calls touch only pure per-graph caches (LRU 4) and no sampler counter or cap, so the transition law is unchanged. Only timing changes, and therefore the sweep at which a cooperative stop occurs.
- The recipe's 300000 counter does not count capture's private operator calls. Only wall time and RSS bound them, as the author says.
- R1 is right about the main indivisible-call risk: the post-return `clean()` and `json.dump` run without budget polling. The streaming dump uses Python's pure iterencode because `indent` is set, and it can leave truncated JSON if the hard monitor fires. `progress.jsonl` holds counters only.

## Blocking issues

None.

## Notes (non-blocking)

1. **New failure surface for existing all-k output.** This is the root's main risk to weigh. With capture bound, any capture ValueError, TypeError or KeyError (premise/rate violation, malformed path, unregistered kind) or a hook failure inside capture turns the whole run `failed`. V002 then returns no prefixes, so the all-k series that base V009 would have returned are lost as well. Exceptions of other classes, such as the operator's own `_Stop` or IndexError, escape the sampler; the worker records FAILED and every row is lost. The author discloses this as R2. It cannot be fixed without a new sampler revision, and the brief mandates the V002 bytes. Section 2 found no static reason for this trial to trip.
2. **R1 understates the polling in all-k analysis.** R1 says `_allk_analyze` "cannot be interrupted". In fact it polls the budget before each of the 36 blocks and before the background, and a stop there returns full 256-row prefixes, capture rows included. Only each block's `_analyze`, the background `_analyze`, the final v004 `_analyze` and result assembly are unpolled. The correction is favourable to preservation.
3. **Runtime cost is understated.** "Comparable to or larger than `_measure`" understates the cost. `_measure` is a cheap numpy pass over stored segment data with no operator calls. Capture has no feature cache: for every segment of every measured path, it re-admits the state (parsing the labelled state), enumerates the full-scope diagonal items (all edges, vertices, donors and identity) and looks up native weights. That is about one uncached `diagonal_terms`-scale evaluation per segment, 512 times, growing with events per path. It is strictly larger than `_measure` and can be a material fraction of the 1740 s budget. No quantitative bound exists without running, so an earlier INCOMPLETE_BUDGET is the expected direction.
4. **Hard monitor margin.** The 60 s / about 124 MiB margin assumes the soft stop fires near its threshold. The hard monitor is a launch requirement that the root must provide externally. It is unchanged from V009 and is not implemented in these files.
5. **Duplicate provenance.** `reweighting_capture_request` (worker) and `sampler_result.recipe_reweighting_capture` (recipe) duplicate the same record. `reweighting_metadata` appears in both `reweighting_statistics` and `partial`. This is harmless and adds a few KB.
6. **TOCTOU (author R5).** The load-time hash-then-exec pattern is pre-existing and unchanged.
7. **Clean working directory.** The 0423 directory has no `__pycache__` or `.pyc`. The reviewer wrote only this file there.
