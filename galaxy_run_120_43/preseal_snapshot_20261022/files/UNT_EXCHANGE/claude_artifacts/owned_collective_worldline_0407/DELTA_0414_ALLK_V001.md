# DELTA 0414 ALLK V001: all-momentum feature branch of the 0413 evaluator v004

**Role.** Author of the UNT 0414 all-momentum feature branch. I am not the W2 author and wrote no sequential v00N file. A distinct correctness review is still pending; this document is not that review.

**Scope of this record.** It records 0414 author activity only. It says nothing about 0413 delivery or its review, and nothing about W2 activity or its queue.

**Method (static only).**
- The module was written as text. Nothing was imported or executed: not the module, the TRANSFORM, any operator or the root adapter.
- No run, sampling, benchmark, network access or install.
- The only code run was `shasum -a 256`, `diff -u`, and `python3 -I -B` (3.9.6) doing `ast.parse`, `compile` (no exec) and `symtable` on TEXT copies in my scratch directory.
- Both files were written by exclusive create (`open(..., 'xb')`). Nothing was overwritten, moved, deleted or chmod-ed.
- There is no `__pycache__` in the 0407 directory.
- Nothing was written under `Universal Network Theory`, and no file with a forbidden name was opened.

## Integration order

0413 base v004 → {W2 sequential version, this all-k branch}, built in parallel → a later explicit merge revision combining both.

- This branch is an immutable feature file. It is not a v00N version, and it does not replace the pinned v004.
- The diff at the end of this document is the complete, self-contained `diff -u` from BASE v004. It can be re-applied onto the W2 version.
- **Expected conflict points for the merge revision:**
  - the module header docstring (first hunk) and the public signature;
  - the end of the `LIMITATIONS` string. This branch labels its items LK1–LK7 so they cannot collide with any W2 L27+; the merge renumbers them.
  - the `_progress` `"module"` string;
  - `_new_result` and the `run` dict;
  - the per-chain allocation and commit block of the sampling loop;
  - the pre-analysis region.
- All allk code paths are gated on `run["allk"] is not None`.

## Hashes (full sha256, computed from bytes)

| File | sha256 | Status |
|---|---|---|
| 0414 task `FROM_CODEX/0414_2026-10-16_all_momentum_response_from_one_ensemble.md` (read fully) | 64742c18a6d51468bc20b3c2a32e06c91bfe50c807a56269418822231bd28ef1 | binding, matched |
| BASE `owned_collective_worldline_static_response_v004.py` (187151 B, 3860 lines; text) | 6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea | binding, matched, unchanged |
| `CODEX1/OWNED_HOMOGENEOUS_COMPONENT_TRANSLATION_AND_MODE_BLOCKS_V001.txt` | d51e57761f7f55feab30671cf22898a337caf6e2af835c9d0c437db87bc305bb | binding, matched |
| `helpers/response_packet_audit/OWNED_HOMOGENEOUS_TRANSLATION_MODE_BLOCKS_DISTINCT_REVIEW_V001.json` | 5b7ffb0fbd94c38dd98231dcbd867014144133759ca6dd300094a71ffc38adf9 | binding, matched |
| TRANSFORM `helpers/coefficient_method/owned_all_momentum_path_algebra_v002.py` (text only) | 2de6e987ed8265caf91b934a9a777b84d42a908800cb735b0773d97ed339a0f5 | binding, matched |
| downstream `helpers/coefficient_method/owned_positive_cardinal_source_hessian_v001.py` | 4d123c1f01bdb20f2bd8a0dcc42e12475f09850eff8f6bbca9d5953d01326848 | binding, matched; hashed only, not read, not implemented |
| operator `owned_retained_response_0405/owned_parent_operator_v003.py` (text: API and record formats) | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 | binding, matched |
| root adapter `helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py` (text: cells are `product(range(L), repeat=3)`) | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 | matches the v004 binding |
| context read: `DELTA_0410_BUDGET_V004.md`, `REVIEW_0410_BUDGET_V001.md`, `CONVENTIONS_0407_V003.md`, `DELTA_0410_MODES_V003.md` (header and section list) | (unchanged files in this directory) | read |
| **NEW** `owned_collective_worldline_static_response_allk_v001.py` (234718 B, 4691 lines) | c37bca61b35579492d5a306519288762a596d787ed7c62d2fe0df2599a4ecbdd | written by exclusive create |

## Public interface

There is still one public entry point. It keeps all 25 v004 keyword arguments, in the same order and with the same meanings. It appends ONE required keyword-only argument with no default:

```
owned_collective_worldline_static_response(*, ..., implicit_closure, budget_hook, progress_sink, all_momentum)
```

**New input: `all_momentum`** (LK1; `_admit_all_momentum` L835).

- `None` disables the branch, and the run is then v004's run (see "Bit-identity" below).
- Otherwise it is `{"L": int >= 2, "cell_coordinates": {cell: three integers}}`.
  - The cells must be exactly `context.energy_cells`: L³ cells, unique modulo L.
  - For the root adapter, whose cells are the integer triples, `{c: c for c in cells}` is the identity map.
- It requires `diagonal_read_source_callback`, whose cells must equal the energy cells (L4111, L4397-4410).
- If the callback binding carries `"L"`, that value must equal `all_momentum["L"]` (L4412).
- Checkable proof scope (`_allk_scope_problems` L880; applied at L4422). The run returns `unsupported` unless all of these hold:
  - uniform `lapse_factors`;
  - uniform whitened `j_R'`/`J_S'`;
  - empty `source_coefficients`;
  - no λA term;
  - equal values in every Mapping model profile.
- The rest of the proof scope is the caller's declaration: covariant graph, registration, ports, frames and allocation, and the seed component.
- With `all_momentum` given, empty `derivative_coordinates` and `tracked_read_labels` are admitted (L4117).

**New outputs.** All are additive. With `all_momentum=None`, `result["all_momentum"]` is None.

- `result["all_momentum"]`:
  - `status` (`not_analysed` | `analysed` | `unsupported`);
  - `metadata`, set at binding (L4442):
    - L, cell order and reduced coordinates;
    - per-cell read order and score/contact layouts;
    - background labels and block fields;
    - the Mandel note and sign convention;
    - per-block k, partner, self_conjugate, profiles, `profile_values`, dimension, coordinate_order, `mode_square_sum`, `actual_mode_gram`, NN positions and contact offset/entries;
    - block counts and n_contact;
    - doubles and bytes per measurement;
    - the largest normalized cross-profile Gram offdiagonal;
    - contact, structure, scope and normalization notes.
  - `partition` and `identity_check`;
  - `series`: per chain, `chain_ids`, `measurement_ids`, `score_cells`, `contacts`, `background` and `events`, the full time series;
  - `blocks`: per block, extensive `dlogZ_deta`, `d2logZ_deta2`, `score_covariance`, `contact_mean`, `F_total_gradient` and `F_total_hessian`, plus `per_chain`, `mixing`, `errors`, `errors_layout_note` and F standard errors;
  - `background`;
  - `mixing` (joint).
- `partial` (incomplete stops):
  - per chain, `all_momentum` views of the committed rows;
  - `all_momentum_layout` and `all_momentum_zero_rate_cells_seen`.
- `inputs.all_momentum`, `conventions.all_momentum`, and the progress stage `all_momentum_analysis`.
- `ok` additionally requires the joint all-momentum mixing to be "passed" (L4690).

**Record change.** `_progress` `"module"` now reads `owned_collective_worldline_static_response_allk_v001` (L1819). This identifies the producing file.

## Change map (allk_v001 line numbers)

AST def-level comparison against BASE (text):
- **9 added:** `_admit_all_momentum`, `_allk_scope_problems`, `_allk_read_fields`, `_allk_block_fields`, `_allk_background_labels`, `_measure_allk`, `_allk_setup`, `_allk_hessian_se`, `_allk_analyze`.
- **0 removed.**
- **10 changed:** `LIMITATIONS`, `_channels_from_records`, `_diagonal_at`, `_event_from_channel`, `_new_result`, `_partial_prefixes`, `_progress`, `_reads_at`, `_segment_core` and the public function.
- **89 AST-identical**, including `_analyze`, `_sums`, `_sums_combine`, `_estimate`, `_layout`, `_sokal_tau`, `_rhat`, `_measure`, every move and CTMC function, `_op`, `_budget_check`, `_initial_path` and `_channels_at`.

| Where | Lines | Change |
|---|---|---|
| Module docstring | 3-25, 108-110, 234-254, 320-323 | branch header, 0414 binding sources and integration order; signature note; WHERE 0414 IS IMPLEMENTED; COST addendum |
| `LIMITATIONS` LK1-LK7 | 605-698 | scope; retained row; blocks; analysis; outputs; cost; not implemented |
| `_admit_all_momentum`, `_allk_scope_problems` | 835-913 | input validation; checkable proof scope |
| `_allk_read_fields` / `_allk_block_fields` / `_allk_background_labels` | 978-994 | TRANSFORM read order; block field names; background labels |
| `_channels_from_records` | 1996-1997 | zero-rate (multiplier 0) cells are recorded for all-k (L6) |
| `_diagonal_at` | 2138-2179 | 4th return: D_N[c] = fsum(d_X w_cX) for every cell, from the same records and terms as `("lapse", cell)` |
| `_reads_at` | 2299, 2377-2385 | 4th return: [cells, 9] whitened reads (R0..R2, S00, S11, S22, S12, S02, S01) from the SAME adapter evaluation |
| `_segment_core` | 2388-2424 | `seg["allk"]` = [−D_N, O_1..O_9] per cell; never enters D, r or W |
| `_event_from_channel` | 2463-2472 | sparse (`allk_idx`, `allk_rho` = w/multiplier) of the sampled primitive |
| `_measure_allk` | 2982-3024 | per-path row: score_cells, block NN contacts, background |
| `_allk_setup` | 3404-3563 | TRANSFORM profiles, Gram, mode_square_sum; cross-profile Gram; layout and metadata |
| `_allk_hessian_se`, `_allk_analyze` | 3566-3735 | identity-checked ONE partition; Mandel once; per-block unchanged `_analyze`; background; joint gate |
| `_partial_prefixes` | 3759-3778 | all-k prefix views plus layout |
| `_new_result` | 3817, 3881-3889 | `all_momentum` key; conventions |
| Public signature / docstring | 3931, 4016-4027, 4041-4046 | `all_momentum`; returns |
| Input admission / echo | 4110-4118, 4156-4159 | admission, callback requirement, relaxed nothing-to-compute check, echo |
| `run` dict | 4225-4226 | `allk`, `allk_layout` (None until binding) |
| Binding | 4395-4451 | cells, callback cells, binding L, scope, budget check, `_allk_setup`, metadata |
| Sampling loop | 4498-4509, 4520, 4548-4559 | rows allocated with the v004 arrays (ids initialised to −1); `_measure_allk` before the writes; ids and row written BEFORE `measurements_committed += 1` |
| Pre-analysis | 4587-4597 | all-k analysis after the full-commit guard and BEFORE v004's column slicing, so a budget stop still returns unmodified prefixes |
| Result assembly | 4663-4690 | `all_momentum` filled; series; flags; `ok` |

## Requirement trace (0414)

| Item | Implementation (allk_v001 lines) | Status |
|---|---|---|
| **1.** Per-cell S_N = −∫D_N dτ + Σρ, nine integrated corrected whitened R/S reads per cell, sparse per-event ρ_α = endpoint-mean allocation / multiplier; reuse current-state normalized callback reads and source definitions; no coincident channel counted twice | D_N per cell: `_diagonal_at` L2139, 2171-2176 (same `value * w` terms and fsum as `("lapse", cell)`). Reads: `_reads_at` L2377-2384, from the SAME `adapted_moment_reads` evaluation that feeds P(x) in D, configuration-normalized by the adapter, never re-whitened. Density: `_segment_core` L2416-2423. ρ: `_event_from_channel` L2463-2470, the chosen primitive's own `energy_weights` / `mult` (identical to the v004 lapse ρ). Integration: `_measure_allk` L3001-3010. Only the sampled record marks an event; diagonal owners enter only via `diagonal_terms` ("diag" records of `primitive_channels` stay skipped, unchanged). | MET (static) |
| **2.** Every independent k,−k complete block (20 reals; 10 self-conjugate); +sin; no phase average; Mandel √2 once on raw S off-diagonals; only NN bare event contacts; nonlinear contacts not declared zero | Profiles transcribed in `_allk_setup` L3417-3449 (TRANSFORM L62, L80-97). Mandel: `_allk_analyze` L3630-3634 (TRANSFORM L69): applied to per-cell S12/S02/S01 columns before projection L3644; `score_cells` stores raw S. NN contacts per block: `_measure_allk` L3011-3018 (TRANSFORM L88-92), placed at N-N positions L3646-3651. The non-NN zero is labelled API-only (LK3; `metadata.contact_note`). | MET (static) |
| **3.** Per-measurement chain and measurement IDs, complete 10L³ score vector, per-mode NN contacts, nine background reads; 741 doubles at L4; time series kept | Allocation L4498-4509; commit L4548-4559; `_measure_allk` returns (score [10L³], contacts [n_contact], background [9]); complete-run `series` L4668-4674; partial L3759-3778. Count at L4: 640 + (28·3 + 8) + 9 = 741 doubles plus 2 int64 = 5,944 B; ×256 = 1,521,664 B ≈ 1.52 MB (arithmetic only). | MET |
| **4.** Full 20/10 block covariance/contacts and existing mixing checks, processed sequentially; ONE identical partition; common leave-one-batch-out across ALL modes and backgrounds; mean subtraction, thresholds and failures kept; every block's diagnostics; no accepted-subset presented as complete | Identity-verified partition L3593-3607 (chain-major × `batches_per_chain`, i.e. v004 `_analyze`'s own `block_sums` order, so omission index i is the same batch for every block, the background and the v004 coordinates). Per block, the UNCHANGED `_analyze` at L3655, with mean subtraction, Cov + ⟨T⟩, (J−1)/J jackknife, Sokal τ, R-hat and caller thresholds. Background at L3687. Joint gate L3689-3704: errors only when every block and the background passed. Every block's mixing report is returned (L3672). The flag at L4682-4687 says no subset is a complete spatial response. | MET (static) |
| **5.** Extensive gradients/Hessians plus ordering/Gram/normalization metadata; no N/2 or N factor, Legendre, units, clipping, ridge, pseudoinverse, force law, target scale or state-band acceptance | Block outputs L3657-3681 (`F_total_*` = −y/β); metadata L3493-3562. The AST holds no division by `mode_square_sum`, no `linalg`/pinv and no clip. | MET |
| **6.** 0413 valid-prefix semantics, budget hook, progress sink and unchanged proposal/RNG law; costs disclosed; every contraction `einsum(..., optimize=False)`; no sample/move/physics change and no new framework | No RNG use, rate, D, W, move or operator/adapter call is added. Prefix commit unchanged (rows written before the increment). Budget checks are added only at binding (L4432) and in the all-k analysis (L3638, L3682), never during sampling. 17 `einsum` calls, all `optimize=False`; no `@`, `dot`, `matmul`, `vdot`, `inner`, `tensordot` or `linalg`. Costs: LK6 and below. | MET (static) |

**Bit-identity.**
- **`all_momentum=None`.** Every added statement is guarded by `run["allk"] is not None` or `allk_terms is not None`, or is inside `if allk_in is not None`. The added tuple elements and dict keys are None or unused. The hook-call sequence, RNG draws, rates, `_analyze` and thresholds are v004's. The visible changes are additive result keys, the `"module"` string and the required keyword.
- **`all_momentum` given.** The draw sequence and transition law are still v004's: the allk values never enter D, r, W or a move decision. Added stops are fail-closed only: non-finite rows and identity-check failure.
- Both statements rest on AST comparison plus hand trace, not on a run.

## TRANSFORM transcription map (no import, no run-time call)

| TRANSFORM (2de6e987…) | allk_v001 |
|---|---|
| L62 `coords.astype(int)%L` | L3415 |
| L68-69 fields, Mandel `[:,7:10]*=np.sqrt(2.)` | L3630-3634 (per-cell columns: 0 = S_N, 1-9 = reads; 7, 8, 9 = S12, S02, S01) |
| L80-86 `np.ndindex`, partner skip, phase, phi, score `'pc,cf->pf'` reshape | L3419-3425, L3644 (`'pc,mcf->mpf'`, row-batched; same sum over c) |
| L87-92 NN contact `-= outer(v,v)` with v = `phi[:,ii]·rr` | L3011-3018 (v by bincount per event; the same per-event sum) |
| L93-97 gram, `mode_square_sum` | L3426, L3441 |
| L127-139 `estimate` | v004 `_estimate` (unchanged; identical algebra: plug-in, no Bessel, cov + contact, −/β) |
| L142-166 `joint_batch_estimates` (LOO across all modes) | v004 `_analyze` jackknife (unchanged) per block and the background, with ONE identity-checked partition |

Floating summation order can differ in the last bits from the TRANSFORM's sequential `add_sample`. The algebra is identical.

## Cost disclosure (arithmetic; no measured timing)

| Item | L4 (n_c = 64) | L6 (216) | L8 (512) |
|---|---|---|---|
| blocks (self-conjugate + pairs) | 36 (8 + 28) | 112 (8 + 104) | 260 (8 + 252) |
| doubles per measurement (10n_c + n_contact + 9) | 741 | 2,489 | 5,893 |
| bytes per measurement (+16 B ids) | 5,944 | 19,928 | 47,160 |
| per 256-row chain | 1.52 MB | 5.10 MB | 12.07 MB |
| per dwell segment (score density, every stored or proposed path) | 5,120 B | 17,280 B | 40,960 B |
| analysis: Mandel copy per chain (256 rows) | 1.31 MB | 4.42 MB | 10.5 MB |
| explicit per-block joint covariance, only if `max_explicit_covariance_dimension` ≥ 230 (65 self-conj.) | 12.1 MB | 44.3 MB | 106.9 MB |

- **Per measurement.** This is one indivisible step with no budget check inside.
  - The time integral is O((K+1)·10·n_c), by sequential accumulation with no BLAS contraction.
  - All block contacts are O((nnz_K + K)·n_c) arithmetic, in about 4·n_blocks numpy calls.
- **Per new state.** O(diagonal records × nonzero weights + 9·n_c).
- **Analysis.**
  - Projection is O(chains × measurements × 10·n_c²).
  - One v004 `_analyze` runs per block at n_u = 20 or 10. That is 231 or 66 primary columns including the structurally zero contact columns, and R-hat plus Sokal FFT per column per chain.
  - One `_analyze` runs for the background.
- **Binding.** The cross-profile Gram is O(n_c³) (einsum, optimize=False).
- **Budget hook.** It is polled before setup, before each block and before the background, so root's hook can stop between blocks.
- Paths at L6/L8 grow by the per-segment figure above, on top of the state objects (L3). This should enter root's 900 MiB planning.

## LIMITATIONS of this branch (recorded literally)

1. **Scope.** Complete blocks are an exact model constraint only under the root proof's scope. Uniform base lapse and pair sources, no operator-read source or λA term, and uniform model mappings are checked. Graph, registration, port, frame and allocation covariance and the seed component are the caller's declaration and are unverified here. Isotropy, finite-volume convergence, continuum interpolation, mixing and correlation tails are neither proved nor assumed.
2. **Strict scope refusal.** The scope check refuses any nonempty `source_coefficients` and any λ ≠ 0 with A present, even when they might be translation invariant. A caller needing those must show invariance separately (fail-closed choice).
3. **Joint error gate.** If any block or the background fails or is unassessable, no block gets errors, even blocks that passed individually. This is the v004 L13 rule applied to the complete all-k column set. Point estimates and every diagnostic are still returned, and the per-row series allows any root re-analysis.
4. **Structurally zero contact columns.** These are the non-NN entries. They appear in each block's `constant_columns` through the unchanged `_analyze`, and they are API zeros, not sampled evidence. Every block also repeats the shared `events_per_path` column.
5. **Background order.** The background uses the TRANSFORM read order (S00, S11, S22, S12, S02, S01). This differs from the v003 L23 `uniform_*` order. Labels are explicit.
6. **Cross-block quantities.** No cross-block covariance or contact is estimated. The per-cell series is returned for any such check.
7. **Zero-rate cells.** A zero-rate primitive with a nonzero cell weight makes the whole all-k output `unsupported`; there is no per-block salvage.
8. **Overrun.** The per-measurement all-k computation and each block's `_analyze` are indivisible and can overrun the cooperative reserve (L26).
9. **Memory scaling.** Per-segment densities scale as 80·L³ bytes. At L8, long paths (about 10⁴ events, 410 MB) can approach root's threshold. No compression or delta storage is implemented.
10. **Operator v003** was read as text for API and record formats only; its compatibility is otherwise as v004's (unexecuted).
11. **Untested.** Everything is static. There is no run, timing or numerical check. Root supplies measured timing.

## AST results (`python3 -I -B` on a TEXT copy of the destination file)

- `ast.parse` and `compile` (no exec) succeed. `symtable` finds no undefined globals.
- Module level holds only the docstring, imports, the `LIMITATIONS` assignment, classes and function defs. Nothing runs at import.
- Imports: `bisect`, `math`, `collections.abc` and `numpy` only.
- Absent: `MatMult`, `dot`, `matmul`, `vdot`, `inner`, `tensordot`, `linalg`, `open`, `print`, `exec`, `eval`, `__import__`, `os`, `sys`, `time`, `subprocess`, global/nonlocal and decorators.
- `einsum` calls: 17, all with `optimize=False`.
- One public callable. It has 0 positional parameters and 26 keyword-only parameters with no defaults: v004's 25 in order, then `all_momentum`.
- Numeric constants: 0, 0.0, 0.5, 1, 1.0, 2, 2.0, 3, 4, 7, 8, 9, 10, 16, 20. The new ones are field/layout indices (7, 8, 9, 10) and the 16 id bytes. There are no budget or physics numbers.
- Defs: 9 added, 0 removed, 10 changed, 89 AST-identical.

## diff -u BASE v004 → allk_v001 (complete; re-applicable onto the W2 version)

Produced by `diff -u v004.py allk_v001.py` on byte copies of the two files in this directory. It has 36 hunks.

```diff
--- v004.py	2026-10-16 05:48:16.022443100 -0500
+++ allk_v001.py	2026-10-16 05:48:16.019469636 -0500
@@ -1,5 +1,29 @@
 """Owned collective static response by positive imaginary-time worldlines.
 
+UNT task 0414 ALL-MOMENTUM FEATURE BRANCH allk_v001. Immutable feature file, NOT a sequential
+v00N version: it is the accepted 0413 evaluator v004 (sha256
+6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea, preserved unchanged) plus ONLY
+the 0414 all-momentum retention and complete k,-k block analysis (LK1-LK7), behind ONE new
+required keyword-only argument all_momentum (None disables it; then every draw, rate,
+estimator, threshold and returned v004 key is v004's). Integration order: 0413 base v004 ->
+{W2 sequential version, this all-k branch} in parallel -> a later explicit merge revision
+combining both; DELTA_0414_ALLK_V001.md holds the self-contained diff -u from v004.
+0414 binding sources (sha256 from bytes before writing; read-only; values never taken from them):
+  * UNT_EXCHANGE/FROM_CODEX/0414_2026-10-16_all_momentum_response_from_one_ensemble.md
+    64742c18a6d51468bc20b3c2a32e06c91bfe50c807a56269418822231bd28ef1   (items 1-6)
+  * CODEX1/OWNED_HOMOGENEOUS_COMPONENT_TRANSLATION_AND_MODE_BLOCKS_V001.txt
+    d51e57761f7f55feab30671cf22898a337caf6e2af835c9d0c437db87bc305bb   (block proof, its scope)
+    with its distinct review helpers/response_packet_audit/
+    OWNED_HOMOGENEOUS_TRANSLATION_MODE_BLOCKS_DISTINCT_REVIEW_V001.json
+    5b7ffb0fbd94c38dd98231dcbd867014144133759ca6dd300094a71ffc38adf9
+  * helpers/coefficient_method/owned_all_momentum_path_algebra_v002.py
+    2de6e987ed8265caf91b934a9a777b84d42a908800cb735b0773d97ed339a0f5   ("TRANSFORM"; read as
+    TEXT only, never imported or called; its profile/score/contact algebra is transcribed with
+    attribution in _allk_setup and _measure_allk, its estimator is v004's _estimate)
+  * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v003.py
+    a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07   (ACTUAL operator API,
+    read as text: public names, signatures and record formats unchanged from v002)
+
 UNT task 0407, version v004: v003 (sha256
 e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721, preserved unchanged) plus ONLY
 the 0413 cooperative budget / partial-return delta (budget_hook, progress_sink, committed
@@ -81,7 +105,9 @@
       volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
       diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
       caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
-      implicit_closure, budget_hook, progress_sink)
+      implicit_closure, budget_hook, progress_sink, all_momentum)
+allk_v001 appends exactly one REQUIRED keyword-only argument without default, all_momentum
+(None, or {"L", "cell_coordinates"}; LK1); every v004 argument keeps its v004 meaning.
 The v002 signature is unchanged in v003 (no public argument is added in v003): the 0410 mode
 columns enter as fixed affine direction mappings inside derivative_coordinates (MODE SPEC
 s1 "minimal API delta"; L21), next to the unchanged tuple coordinate interface. v004 adds
@@ -205,6 +231,27 @@
   Item 4 (progress sink): _progress (stage, chain_start, sweep and stop records).
   Item 5 (partial return, ok False, no mixing analysis after a stop): _stopped,
     _partial_prefixes; the completed path through _analyze is unchanged.
+WHERE 0414 IS IMPLEMENTED (allk_v001, LK1-LK7; active only when all_momentum is not None)
+  Input/scope: _admit_all_momentum (L, integer cell coordinates on Z_L^3), the binding stage
+    (cells, callback cells, binding L) and _allk_scope_problems (checkable proof scope).
+  Item 1 (per-cell S_N, nine integrated corrected whitened reads, sparse event rho): _diagonal_at
+    (D_N per cell from the SAME diagonal_terms records), _reads_at (nine reads per cell from the
+    SAME adapter evaluation that enters H_c), _segment_core (per-dwell score density),
+    _event_from_channel (rho_c = wbar_cX / multiplier of the sampled primitive only),
+    _measure_allk (S_N = -int D_N + sum rho; int O; no channel counted twice).
+  Item 2 (every independent k,-k block, 20 / 10 reals, +sin, no phase average, Mandel once, NN
+    bare contacts only): _allk_setup (TRANSFORM profiles transcribed), _measure_allk (NN event
+    contacts per block), _allk_analyze (Mandel on per-cell S12/S02/S01 once, then projection).
+  Item 3 (chain/measurement ids, 10 L^3 scores, per-block NN contacts, nine background reads,
+    per-row time series): sampling loop (allocation and commit), _measure_allk,
+    _partial_prefixes, result all_momentum["series"].
+  Item 4 (sequential full-block analysis, ONE partition, common omission, v004 checks, every
+    block reported, no accepted subset): _allk_analyze (identity check, unchanged _analyze per
+    block and for the background, joint gate).
+  Item 5 (extensive gradients/Hessians, ordering/Gram/normalization metadata, nothing applied):
+    _allk_setup (metadata), _allk_analyze (block outputs).
+  Item 6 (0413 semantics kept, costs disclosed, einsum optimize=False, no sample/move/physics
+    change): LK4, LK6; no random draw, rate or operator/adapter call is added.
 
 SEMANTICS. In the positive gauge G = (-1)^{sum_v q_v} (-e^{i phi_adm})^{N_S}
 (-e^{i phi_birth})^{N} (assembly lines 300-327, e^{-i theta} epsilon = -|epsilon| written
@@ -270,7 +317,10 @@
 proposal jump, held replay, move and sweep; progress records are O(1) in size (two small
 counter dicts), one per stage, chain start, completed sweep and stop. Per-chain arrays
 (measurement_sweeps * (n_u^2 + n_u + n_r + 1) numbers) are allocated once at chain start,
-as in v003; a stop returns views of their committed rows (no copy).
+as in v003; a stop returns views of their committed rows (no copy). allk_v001 (only with
+all_momentum): +80 L^3 bytes per dwell segment, a per-measurement row of 10 L^3 + n_contact + 9
+float64 plus two int64 ids (L4: 741 + 2 numbers, 5,944 bytes), O((K+1) 10 L^3 + (nnz_K + K)
+L^3) arithmetic per measurement and a sequential block analysis; see LK6.
 
 LIMITATIONS: see the module-level string LIMITATIONS.
 """
@@ -552,6 +602,99 @@
     with no returned result; only the sink records then identify the reached stage.
     Memory growth inside one call is not observable here. Earlier root failure evidence
     (runs V001 and V002) is neither touched nor reinterpreted.
+LK1. All-momentum input and scope (0414; branch allk_v001; labels LK* avoid collisions with the
+    parallel W2 sequential version and are renumbered only by the explicit merge revision).
+    all_momentum is None (disabled: the run is v004's) or {"L": int >= 2, "cell_coordinates":
+    {cell: three integers}} over EXACTLY context.energy_cells, L**3 cells, unique modulo L (for
+    the root adapter, whose cells are the integer triples product(range(L), repeat=3), the
+    identity map). It needs diagonal_read_source_callback with callback cells equal to the
+    energy cells; when the callback binding carries "L" it must equal all_momentum["L"]. The
+    complete k,-k block structure is the root-reviewed EXACT MODEL CONSTRAINT of
+    OWNED_HOMOGENEOUS_COMPONENT_TRANSLATION_AND_MODE_BLOCKS_V001 (d51e5776...) under ITS scope
+    only. Checked here (status "unsupported" otherwise, _allk_scope_problems): uniform base
+    lapse_factors, uniform whitened pair sources j_R'/J_S', empty source_coefficients, no
+    lambda A term (lambda == 0 or A empty), equal values in every Mapping model profile. NOT
+    checkable here, declared by the caller: translation covariance of graph0, registration,
+    port rule, frames and energy allocation, and the translation-fixed seed component of the
+    initial paths (L7). Rotation/isotropy, finite-volume convergence, continuum interpolation,
+    mixing and correlation tails are neither proved nor assumed.
+LK2. Retained per-measurement row. At every new state the SAME diagonal_terms and callback
+    evaluation that enters D gives the per-cell score density [-D_N, R'_0, R'_1, R'_2, S'_00,
+    S'_11, S'_22, S'_12, S'_02, S'_01](c) with D_N(c) = sum_diag d_X w_cX (exactly the D_a of
+    ("lapse", cell)) and the adapter's configuration-normalized whitened reads (no
+    re-normalization, no second whitening, raw S without Mandel factor). Every event keeps the
+    sparse rho_c = wbar_cX / multiplier of the SAMPLED primitive's own endpoint-averaged
+    energy_weights (exactly the rho of ("lapse", cell)); coincident primitives are separate
+    records and only the sampled one marks the event; diagonal owners enter only through
+    diagonal_terms (the primitive_channels "diag" records stay skipped), so no channel is
+    counted twice. Per measurement (one per measurement sweep, committed with the v004 tuple
+    before measurements_committed advances) the module stores chain id, measurement id,
+    score_cells [10 L^3] (index c*10 + f, context.energy_cells order: f = 0 S_N(c) = -int
+    D_N(c) dtau + sum_events rho_c, f = 1..9 int O_c,f dtau with the positive sign of
+    H_c - j.O), the bare NN event contacts of every block (1 entry per self-conjugate block, 3 =
+    (cos,cos), (cos,sin), (sin,sin) per k,-k pair: -sum_events v v^T, v = phi[:, cells] . rho)
+    and nine background reads (1/beta) int sum_c O_c,f dtau in the same read order (cell SUMS,
+    no Mandel; NOT the v003 L23 order). L4: 640 + 92 + 9 = 741 float64 plus two int64 ids =
+    5,944 bytes per measurement, 1.52 MB per 256-row chain (arithmetic estimate only). The time
+    series is kept per row (no batch-sum replacement) in result all_momentum["series"] and, on
+    an incomplete stop, in the committed prefixes (L24).
+LK3. Blocks. Profiles are TRANSFORM iter_path_blocks transcribed: k over np.ndindex((L, L, L)),
+    skipped when k > its partner -k mod L (tuple order), phase = (2 pi / L) k.x on the reduced
+    integer coordinates, phi = cos for a self-conjugate k (k = -k mod L; ten fields) else
+    (cos, +sin) (twenty fields); no phase average, no symmetrization between profiles. Block
+    score = phi . fields with the Mandel sqrt(2) applied ONCE, to the per-cell S12, S02, S01
+    columns before projection; order profile-major then [N, R0, R1, R2, S00, S11, S22,
+    sqrt2 S12, sqrt2 S02, sqrt2 S01]. Block contacts: only the N-N entries are nonzero, because
+    in the affine fixed-read API W depends only on lapse and D is affine; every other entry is
+    zero IN THIS API ONLY: nonlinear Legendre, metric, preparation, read-frame and mean-map
+    contacts are downstream and are NOT declared zero by this fact. No 10 L^3 x 10 L^3 matrix is
+    formed. Cross-block covariances are not estimated: they vanish in the exact homogeneous
+    expectation by the root proof, an exact model constraint, not evidence of mixing; the
+    per-cell series is returned so any cross-block check stays available to root.
+LK4. Analysis (only after every chain committed every row). ONE partition is built, chain-major
+    with batches_per_chain contiguous batches per chain, i.e. v004 _analyze's own, and every
+    batch's stored (chain id, measurement id) rows are verified against it (failed otherwise;
+    equal counts alone are not identity). Blocks are processed sequentially: for each block the
+    UNCHANGED v004 _analyze (plug-in mean subtraction, Cov + <T>, leave-one-batch-out jackknife
+    with (J-1)/J, between-chain spread, Sokal tau, R-hat, the caller's thresholds) runs on its d
+    score columns and d x d contact rows; then once on the nine background columns. Omission
+    index i is the same partition batch for every block and the background. Joint
+    all-momentum mixing is "passed" only if every block and the background passed; otherwise
+    ("failed" / "unassessable") NO block or background error, replicate or covariance is
+    returned (v004 L13 applied to the complete all-momentum column set) and a flag states that
+    no subset is a complete spatial response. Every block's diagnostics are returned whatever
+    its status. Each block's constant_columns include its structurally zero contact entries
+    (exact zeros of the affine API, not sampled evidence). A budget check runs before each
+    block and before the background; a True return abandons the analysis (INCOMPLETE_BUDGET,
+    committed prefixes, L24). A lapse cell met with a zero-rate primitive (L6) makes the
+    all-momentum output "unsupported" (no block estimate).
+LK5. Outputs are EXTENSIVE derivatives of F_total = -log Z / beta per block: dlogZ_deta,
+    d2logZ_deta2 (= score covariance + contact mean), F_total_gradient = -<S>/beta and
+    F_total_hessian = -(Cov + <T>)/beta, with the ordering, per-block actual Gram phi phi^T,
+    declared mode_square_sum (L^3 self-conjugate, L^3/2 pairs) and the largest normalized
+    cross-profile Gram offdiagonal as metadata only. No N/2 or N factor, division by a mode
+    norm, Legendre map, units, clipping, ridge, pseudoinverse, force law, target-informed scale
+    or state-band acceptance is applied; root applies the normalization, complete
+    source-Hessian extension, Legendre map, mean contacts, physical units and full metric
+    solve. "ok" additionally requires joint all-momentum mixing "passed"; acceptance is root's.
+LK6. Cost (disclosed, not measured; L3, L26). Per dwell segment +80 L^3 bytes (5,120 B at L4,
+    17,280 B at L6, 40,960 B at L8) for its score density, held by every stored and proposed
+    path next to its state object (L3); per new state O(diagonal records x nonzero weights +
+    9 L^3); per event two small arrays over its nonzero cell weights. Per measurement (one
+    indivisible step, no budget check inside): O((K+1) 10 L^3) for the time integral
+    (sequential accumulation, no BLAS contraction) and O(nnz_K L^3 + K L^3) for all block
+    contacts (K events, nnz_K their nonzero weights), plus about 4 numpy calls per block. Per
+    chain arrays measurement_sweeps x (10 L^3 + n_contact + 9 + 2) numbers next to v004's.
+    Analysis: one Mandel-scaled copy of every chain's score rows (chains x measurements x
+    10 L^3), per block a projection O(chains x measurements x 10 p L^3) (all blocks: O(chains x
+    measurements x 10 L^6)) and the v004 _analyze cost at n_u = 20 (230 primary score/contact
+    columns plus events) or 10 (65 plus events); an explicit joint covariance per block when
+    n_y = 230 (65) <= max_explicit_covariance_dimension (then about 12 MB at L4 and 107 MB at
+    L8 in total). Binding: the cross-profile Gram, O(L^9) (einsum, optimize=False).
+LK7. Not implemented: cross-block (k != k') estimates, symmetry repair or projection of samples,
+    translation averaging, Fourier interpolation, continuum limit, Legendre / metric / EH solve,
+    the equal-time two-hop sector and the downstream positive-cardinal source Hessian. The
+    TRANSFORM module is read as text and transcribed; it is never imported or called.
 """
 
 
@@ -689,6 +832,87 @@
     return True
 
 
+def _admit_all_momentum(value, failures):
+    """allk_v001 input (0414; LK1): None (disabled) or {"L", "cell_coordinates"}, validated."""
+    if value is None:
+        return None
+    name = "all_momentum"
+    mp = _admit_mapping(name, value, failures)
+    if mp is None or not _admit_required_keys(name, mp, ("L", "cell_coordinates"), failures):
+        return None
+    size = _admit_int(f"{name}['L']", mp["L"], 2, failures)
+    raw = mp["cell_coordinates"]
+    if not isinstance(raw, Mapping) or not raw:
+        failures.append(
+            f"input {name}['cell_coordinates']: a nonempty mapping cell -> three integers is "
+            "required (primitive cell coordinates on Z_L^3; LK1)"
+        )
+        return None
+    coords = {}
+    for cell, xyz in raw.items():
+        seq = isinstance(xyz, (list, tuple)) or (isinstance(xyz, np.ndarray) and xyz.ndim == 1)
+        if not (seq and len(xyz) == 3 and all(
+            not isinstance(x, (bool, np.bool_)) and isinstance(x, (int, np.integer)) for x in xyz
+        )):
+            failures.append(
+                f"input {name}['cell_coordinates'][{cell!r}]: three integers are required "
+                "(primitive integer cell coordinates; LK1)"
+            )
+            continue
+        coords[cell] = tuple(int(x) for x in xyz)
+    if size is None or len(coords) != len(raw):
+        return None
+    if len(coords) != size ** 3:
+        failures.append(
+            f"input {name}: {len(coords)} cell coordinates for L = {size}; exactly L**3 = "
+            f"{size ** 3} cells, one per point of Z_L^3, are required (LK1)"
+        )
+        return None
+    reduced = {cell: tuple(x % size for x in xyz) for cell, xyz in coords.items()}
+    if len(set(reduced.values())) != len(reduced):
+        failures.append(
+            f"input {name}['cell_coordinates']: coordinates are not unique modulo L (LK1)"
+        )
+        return None
+    return {"L": size, "cell_coordinates": reduced}
+
+
+def _allk_scope_problems(model, lapse, pair, sources, vgrad, lam):
+    """allk_v001: checkable items of the translation-proof scope (LK1); [] when all hold.
+
+    Registration / port / frame / allocation covariance and the seed component are NOT
+    checkable here and remain the caller's declaration (LK1).
+    """
+    problems = []
+    vals = list(lapse.values())
+    if any(v != vals[0] for v in vals):
+        problems.append("lapse_factors are not uniform over the cells (nonuniform base lapse)")
+    cells = list(pair["j_R"])
+    r0 = list(pair["j_R"][cells[0]])
+    s0 = [list(row) for row in pair["j_S"][cells[0]]]
+    if any(list(pair["j_R"][c]) != r0 or [list(row) for row in pair["j_S"][c]] != s0
+           for c in cells):
+        problems.append("whitened pair sources j_R'/J_S' are not uniform over the cells")
+    if sources:
+        problems.append(
+            "source_coefficients is nonempty: operator-read sources are not shown translation "
+            "invariant"
+        )
+    if vgrad and lam != 0.0:
+        problems.append(
+            "a volume term -lambda A with lambda != 0 is present: A is not shown translation "
+            "invariant"
+        )
+    _, profiles = _model_schema()
+    for name in profiles:
+        prof = model[name]
+        if isinstance(prof, Mapping):
+            pv = [_complex_value(v) for v in prof.values()]
+            if any(v is None or v != pv[0] for v in pv):
+                problems.append(f"model['{name}'] mapping values are not uniform")
+    return problems
+
+
 def _admit_operator_api(operator_api, need_restricted, failures):
     names = [
         "validate_owned_model",
@@ -751,6 +975,24 @@
     return tuple(("uniform_" + f[0],) + f[1:] for f in _mode_fields())
 
 
+def _allk_read_fields():
+    """allk_v001 per-cell read order of the TRANSFORM (LK2): R0, R1, R2, S00, S11, S22, S12, S02,
+    S01 of the whitened callback moments (raw S; the Mandel sqrt(2) is applied once, LK3)."""
+    return (("whitened_R", 0), ("whitened_R", 1), ("whitened_R", 2),
+            ("whitened_S", 0, 0), ("whitened_S", 1, 1), ("whitened_S", 2, 2),
+            ("whitened_S", 1, 2), ("whitened_S", 0, 2), ("whitened_S", 0, 1))
+
+
+def _allk_block_fields():
+    """allk_v001 ten block fields per profile (TRANSFORM order, Mandel components marked)."""
+    return ("N", "R0", "R1", "R2", "S00", "S11", "S22", "sqrt2_S12", "sqrt2_S02", "sqrt2_S01")
+
+
+def _allk_background_labels():
+    """allk_v001 nine background read labels (time-averaged cell sums; LK2), read order."""
+    return tuple(("background_cell_sum_" + f[0],) + f[1:] for f in _allk_read_fields())
+
+
 def _label_kind(label):
     if isinstance(label, tuple) and label and isinstance(label[0], str):
         return label[0]
@@ -1574,7 +1816,7 @@
     if sink is None:
         return
     record = {
-        "module": "owned_collective_worldline_static_response_v004",
+        "module": "owned_collective_worldline_static_response_allk_v001",  # 0414 branch id
         "event": event,
         "stage": stage,
         "chain": None if diag is None else diag["chain"],
@@ -1751,6 +1993,8 @@
             for cell, w in weights.items():
                 if w != 0.0 and cell in run["lapse_index"]:
                     run["zero_rate_directions"].add(("lapse", cell))
+                if w != 0.0 and run["allk"] is not None:
+                    run["allk"]["zero_rate_cells"].add(cell)  # allk_v001 (LK4, L6)
             for idx, phi in run["lapse_dirs"]:
                 if _projected_weight(phi, weights) != 0.0:
                     run["zero_rate_directions"].add(run["coords"][idx])  # L6, L21
@@ -1880,7 +2124,9 @@
     """Diagonal H[N] energy, its lapse derivatives and (v003) lapse-direction projections.
 
     Lapse directions (L21): sum_diag d_X v_X with v_X = sum_alpha phi_alpha w_alphaX, formed
-    per record from its own weights (no per-cell column is stored).
+    per record from its own weights (no per-cell column is stored). allk_v001 (LK2): with
+    all_momentum, a fourth element D_N[c] = sum_diag d_X w_cX for EVERY cell (the same terms
+    as ("lapse", cell)); otherwise None.
     """
     records = _op(run, "diagonal_terms", context=run["context"], state=state)
     if not isinstance(records, (list, tuple)):
@@ -1889,6 +2135,8 @@
     h_terms = []
     lapse_terms = {cell: [] for cell in run["lapse_index"]}
     dir_terms = {idx: [] for idx, _ in run["lapse_dirs"]}
+    allk = run["allk"]
+    allk_terms = None if allk is None else [[] for _ in range(allk["n_cells"])]
     for i, rec in enumerate(records):
         where = f"diagonal_terms record {i}"
         present_k, kind = _field(rec, "kind")
@@ -1920,8 +2168,14 @@
                 lapse_terms[cell].append(value * w)
         for idx, phi in run["lapse_dirs"]:
             dir_terms[idx].append(value * _projected_weight(phi, weights))
+        if allk_terms is not None:
+            for cell, w in weights.items():
+                allk_terms[allk["cell_pos"][cell]].append(value * w)  # allk_v001 (LK2)
+    d_allk = None
+    if allk_terms is not None:
+        d_allk = np.array([math.fsum(t) for t in allk_terms], dtype=np.float64)
     return (math.fsum(h_terms), {c: math.fsum(v) for c, v in lapse_terms.items()},
-            {idx: math.fsum(v) for idx, v in dir_terms.items()})
+            {idx: math.fsum(v) for idx, v in dir_terms.items()}, d_allk)
 
 
 def _index_read_labels(run, labels):
@@ -2018,7 +2272,8 @@
     """Full diagonal reads at `state` (operator rows, callback whitened moments, pair source).
 
     Returns (values for every referenced label, pair source value P(x), {coordinate index:
-    D_a of P}). The SAME evaluation feeds D, every D_a and the tracked time averages.
+    D_a of P}, allk_v001 per-cell reads or None). The SAME evaluation feeds D, every D_a, the
+    tracked time averages and (allk_v001, LK2) the [cells, 9] whitened reads in TRANSFORM order.
     """
     rows = _op(run, "read_rows", context=run["context"], state=state)
     if not isinstance(rows, Mapping) or any(k not in rows for k in ("labels", "values", "presence")):
@@ -2041,6 +2296,7 @@
     pair = run["pair"]
     pair_value = 0.0
     pair_da = {}
+    allk_reads = None
     if pair is not None:
         fns = pair["fns"]
         _budget_check(run, "before", "adapted_moment_reads")  # v004 (L24), outside the try
@@ -2118,14 +2374,26 @@
                 values[lbl] = math.fsum([r_w[cell][lbl[1]] for cell in cells])
             else:
                 values[lbl] = math.fsum([s_w[cell][lbl[1]][lbl[2]] for cell in cells])
-    return values, pair_value, pair_da
+        # allk_v001 (LK2): the nine current-state normalized whitened reads of EVERY cell,
+        # context.energy_cells order, TRANSFORM read order, raw S (no Mandel factor here).
+        if run["allk"] is not None:
+            allk_reads = np.array(
+                [[r_w[c][0], r_w[c][1], r_w[c][2], s_w[c][0][0], s_w[c][1][1], s_w[c][2][2],
+                  s_w[c][1][2], s_w[c][0][2], s_w[c][0][1]] for c in run["energy_cells"]],
+                dtype=np.float64,
+            )
+    return values, pair_value, pair_da, allk_reads
 
 
 def _segment_core(run, state):
-    """Dwell-segment record {state, key, D, r (lazy), Da, row} from FULL diagonal reads."""
+    """Dwell-segment record {state, key, D, r (lazy), Da, row, allk} from FULL diagonal reads.
+
+    allk_v001 (LK2): "allk" is the per-cell score density [-D_N, O_1..O_9] [cells, 10] of this
+    SAME evaluation when all_momentum is given, else None; it never enters D, r or W.
+    """
     key = _state_key(run, state)
-    d_h, d_lapse, d_dirs = _diagonal_at(run, state)
-    values, pair_value, pair_da = _reads_at(run, state)
+    d_h, d_lapse, d_dirs, d_allk = _diagonal_at(run, state)
+    values, pair_value, pair_da, r_allk = _reads_at(run, state)
     src = math.fsum([-j * values[lbl] for lbl, j in run["sources"].items()])
     vol = math.fsum([a * values[lbl] for lbl, a in run["volume_gradient"].items()])
     diag = math.fsum([d_h, src, pair_value, -run["lam"] * vol])
@@ -2144,7 +2412,15 @@
         else:  # pair_source_R / pair_source_S / v003 source_direction (callback reads)
             da[idx] = pair_da[idx]
     row = np.array([values[lbl] for lbl in run["tracked_all"]], dtype=np.float64)
-    return {"state": state, "key": key, "D": diag, "r": None, "Da": da, "row": row}
+    dens = None
+    if run["allk"] is not None:
+        if d_allk is None or r_allk is None:
+            raise _Stop("failed", run["stage"], "all_momentum per-cell evaluation missing (LK2)")
+        dens = np.column_stack((-d_allk, r_allk))  # allk_v001: score density, no D/W change
+        if not bool(np.all(np.isfinite(dens))):
+            raise _Stop("failed", run["stage"], "all_momentum per-cell density not finite")
+    return {"state": state, "key": key, "D": diag, "r": None, "Da": da, "row": row,
+            "allk": dens}
 
 
 def _segment_at(run, state):
@@ -2184,8 +2460,16 @@
     for idx, phi in run["lapse_dirs"]:
         rho[idx] = _projected_weight(phi, ch["weights"]) / ch["mult"]
     dq, dns, dn, _ = run["kinds"][ch["kind"]]
+    # allk_v001 (LK2): sparse per-cell rho_c = wbar_cX / multiplier of THIS sampled primitive
+    # (its own endpoint-averaged energy_weights; exactly the ("lapse", cell) rho).
+    allk_idx = None
+    allk_rho = None
+    if run["allk"] is not None:
+        cells = list(ch["weights"])
+        allk_idx = np.array([run["allk"]["cell_pos"][c] for c in cells], dtype=np.int64)
+        allk_rho = np.array([ch["weights"][c] / ch["mult"] for c in cells], dtype=np.float64)
     return {"kind": ch["kind"], "owner": ch["owner"], "W": ch["W"], "rho": rho,
-            "dq": dq, "dns": dns, "dn": dn}
+            "dq": dq, "dns": dns, "dn": dn, "allk_idx": allk_idx, "allk_rho": allk_rho}
 
 
 def _summed_rate(run, channels, kind, sig, target_key, use_sig):
@@ -2695,6 +2979,51 @@
     return score, contact, read_avg, k
 
 
+def _measure_allk(run, path):
+    """allk_v001 per-path row (0414 items 1-3; LK2): per-cell scores, block NN contacts, background.
+
+    score_cells[c*10 + f]: f = 0 is S_N(c) = -int D_N(c) dtau + sum_events rho_c, f = 1..9 is
+    int O_c,f dtau (TRANSFORM read order, raw whitened S, no Mandel factor). Per block, the bare
+    event contact -sum_events v v^T with v = phi[:, cells] . rho, transcribed from TRANSFORM
+    iter_path_blocks (owned_all_momentum_path_algebra_v002.py lines 88-92), kept as its 1
+    (self-conjugate) or 3 ((cos,cos), (cos,sin), (sin,sin)) independent entries. Background:
+    the nine time-averaged cell sums (1/beta) int sum_c O_c,f dtau. No operator, adapter or
+    hook call and no random draw: the row is one indivisible step (LK6).
+    """
+    ak = run["allk"]
+    beta = run["beta"]
+    n_c = ak["n_cells"]
+    segments = path["segments"]
+    events = path["events"]
+    times = path["times"]
+    k = len(times)
+    bounds = [0.0] + list(times) + [beta]
+    integ = np.zeros((n_c, 10), dtype=np.float64)
+    for j, seg in enumerate(segments):
+        integ += (bounds[j + 1] - bounds[j]) * seg["allk"]  # sequential, no BLAS contraction
+    contacts = np.zeros(ak["n_contact"], dtype=np.float64)
+    if k > 0:
+        lengths = [ev["allk_idx"].shape[0] for ev in events]
+        idx = np.concatenate([ev["allk_idx"] for ev in events])
+        rho = np.concatenate([ev["allk_rho"] for ev in events])
+        ev_ids = np.repeat(np.arange(k, dtype=np.int64), lengths)
+        integ[:, 0] += np.bincount(idx, weights=rho, minlength=n_c)  # + sum_events rho_c
+        for blk in ak["blocks"]:
+            phi = blk["phi"]
+            proj = phi[:, idx] * rho[None, :]
+            v = np.stack([np.bincount(ev_ids, weights=proj[q], minlength=k)
+                          for q in range(phi.shape[0])])  # v[p, event] = phi[p, cells] . rho
+            c_blk = -np.einsum("pk,qk->pq", v, v, optimize=False)
+            for col, (a, b) in enumerate(blk["contact_entries"]):
+                contacts[blk["contact_offset"] + col] = c_blk[a, b]
+    background = np.einsum("cf->f", integ[:, 1:], optimize=False) / beta
+    score = integ.reshape(-1)
+    if not (bool(np.all(np.isfinite(score))) and bool(np.all(np.isfinite(contacts)))
+            and bool(np.all(np.isfinite(background)))):
+        raise _Stop("failed", run["stage"], "all_momentum measurement row not finite (LK2)")
+    return score, contacts, background
+
+
 def _sums(S, T, R):
     return {
         "n": S.shape[0],
@@ -3067,6 +3396,345 @@
     return out, uni
 
 
+# ----------------------------------------------------------------------------------
+# All-momentum complete k,-k blocks (allk_v001; 0414; LK1-LK7)
+# ----------------------------------------------------------------------------------
+
+
+def _allk_setup(run, ak_in):
+    """Per-run all-momentum tables and metadata (LK2-LK5); (allk, layout, meta, problem).
+
+    Profiles, Gram and mode_square_sum are transcribed exactly from TRANSFORM
+    owned_all_momentum_path_algebra_v002.py (sha256 2de6e987...) iter_path_blocks, lines 62
+    and 80-97 (coords % L; np.ndindex k; skip k > partner; phase; cos / (cos, +sin); gram).
+    Called at the binding stage, after the cells were checked; nothing is divided by a norm.
+    """
+    cells = run["energy_cells"]
+    size = ak_in["L"]
+    n_c = len(cells)
+    coords = np.array([ak_in["cell_coordinates"][cell] for cell in cells], dtype=int) % size
+    fields = _allk_block_fields()
+    blocks = []
+    offset = 0
+    for k in np.ndindex((size, size, size)):
+        partner = tuple((-a) % size for a in k)
+        if k > partner:
+            continue
+        self_conjugate = k == partner
+        phase = (2. * np.pi / size) * np.einsum("ci,i->c", coords, np.asarray(k), optimize=False)
+        phi = np.cos(phase)[None, :] if self_conjugate else np.stack((np.cos(phase), np.sin(phase)))
+        gram = np.einsum("pc,qc->pq", phi, phi, optimize=False)
+        if not (bool(np.all(np.isfinite(phase))) and bool(np.all(np.isfinite(phi)))
+                and bool(np.all(np.isfinite(gram)))):
+            return None, None, None, f"all_momentum block k = {k!r}: profile or Gram not finite"
+        profiles = ("cos",) if self_conjugate else ("cos", "sin")
+        entries = [(0, 0)] if self_conjugate else [(0, 0), (0, 1), (1, 1)]
+        blocks.append({
+            "index": len(blocks),
+            "k": tuple(int(a) for a in k),
+            "partner": partner,
+            "self_conjugate": self_conjugate,
+            "phi": phi,
+            "profiles": profiles,
+            "dimension": 10 * len(profiles),
+            "coordinate_order": [(p, f) for p in profiles for f in fields],
+            "mode_square_sum": float(n_c if self_conjugate else n_c / 2),
+            "actual_mode_gram": gram,
+            "nn_positions": [10 * q for q in range(len(profiles))],
+            "contact_offset": offset,
+            "contact_entries": entries,
+        })
+        offset += len(entries)
+    n_prof = sum(len(b["profiles"]) for b in blocks)
+    if n_prof != n_c:
+        return None, None, None, (
+            f"all_momentum: {n_prof} real profiles for {n_c} cells (internal; LK3)"
+        )
+    stacked = np.concatenate([b["phi"] for b in blocks], axis=0)
+    cross = np.einsum("mc,nc->mn", stacked, stacked, optimize=False)
+    diag = np.sqrt(np.diagonal(cross).copy())
+    normed = np.abs(cross) / np.einsum("m,n->mn", diag, diag, optimize=False)
+    np.fill_diagonal(normed, 0.0)
+    worst = float(normed.max()) if n_prof > 1 else None
+    if worst is not None and not math.isfinite(worst):
+        return None, None, None, "all_momentum: cross-profile Gram not finite"
+    n_contact = offset
+    n_self = sum(1 for b in blocks if b["self_conjugate"])
+    allk = {
+        "L": size,
+        "n_cells": n_c,
+        "cell_pos": {cell: i for i, cell in enumerate(cells)},
+        "blocks": blocks,
+        "n_contact": n_contact,
+        "zero_rate_cells": set(),
+    }
+    score_layout = (
+        "score_cells[m, c*10 + f], c in context.energy_cells order, f = 0: S_N(c) = -int D_N(c) "
+        "dtau + sum_events rho_c; f = 1..9: int O_c,f dtau over ('whitened_R', 0..2), "
+        "('whitened_S', 0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1) (raw whitened S, no Mandel "
+        "factor; positive sign of H_c - j.O)"
+    )
+    contact_layout = (
+        "contacts[m, block contact_offset + col] = bare NN event contact entry contact_entries"
+        "[col] = (a, b) of profiles (a, b): -sum_events v_a v_b, v = phi[:, cells] . rho"
+    )
+    layout = {
+        "L": size,
+        "n_cells": n_c,
+        "n_contact": n_contact,
+        "score_layout": score_layout,
+        "contact_layout": contact_layout,
+        "per_cell_read_fields": list(_allk_read_fields()),
+        "background_labels": list(_allk_background_labels()),
+        "blocks": [{"k": b["k"], "contact_offset": b["contact_offset"],
+                    "contact_entries": list(b["contact_entries"])} for b in blocks],
+        "metadata": "see result['all_momentum']['metadata'] (set at the binding stage)",
+    }
+    meta = {
+        "L": size,
+        "n_cells": n_c,
+        "cell_order": list(cells),
+        "cell_coordinates_mod_L": [tuple(int(x) for x in row) for row in coords],
+        "per_cell_read_fields": list(_allk_read_fields()),
+        "score_layout": score_layout,
+        "contact_layout": contact_layout,
+        "background_labels": list(_allk_background_labels()),
+        "background_note": (
+            "(1/beta) int sum_c O_c,f dtau: time-averaged cell SUMS of the nine whitened reads, "
+            "same read order as score_cells, no Mandel factor, no division by n_cells, no "
+            "central covariance (root: mu = sum / n_cells)"
+        ),
+        "block_fields": list(fields),
+        "mandel": (
+            "block score fields 7, 8, 9 of each profile are sqrt(2) times the raw whitened S12, "
+            "S02, S01 integrals; the factor is applied ONCE, to the per-cell columns before "
+            "projection (TRANSFORM line 69); raw S is what score_cells stores"
+        ),
+        "sign_convention": (
+            "phase = (2 pi / L) k . x on integer coordinates reduced mod L; profiles cos, +sin; "
+            "block score order profile-major then block_fields; no phase average"
+        ),
+        "blocks": [dict({k2: b[k2] for k2 in ("index", "k", "partner", "self_conjugate",
+                                             "profiles", "dimension", "coordinate_order",
+                                             "mode_square_sum", "actual_mode_gram",
+                                             "nn_positions", "contact_offset",
+                                             "contact_entries")},
+                        profile_values=b["phi"]) for b in blocks],
+        "n_blocks": len(blocks),
+        "n_self_conjugate_blocks": n_self,
+        "n_pair_blocks": len(blocks) - n_self,
+        "n_contact": n_contact,
+        "doubles_per_measurement": 10 * n_c + n_contact + 9,
+        "bytes_per_measurement": 8 * (10 * n_c + n_contact + 9) + 16,
+        "cross_profile_gram_max_normalized_offdiagonal": worst,
+        "gram_note": (
+            "per-block actual_mode_gram = phi phi^T and the cross-profile maximum are reported, "
+            "never thresholded; mode_square_sum is the TRANSFORM's declared L^3 (self-conjugate) "
+            "or L^3/2; no score, covariance, contact or estimate is divided by either"
+        ),
+        "contact_note": (
+            "bare NN event contacts only: in the affine fixed-read API W depends only on lapse "
+            "and D is affine; the other block contact entries are zero IN THIS API ONLY; "
+            "nonlinear Legendre / metric / preparation / read-frame / mean-map contacts are "
+            "downstream and NOT declared zero (LK3)"
+        ),
+        "block_structure": (
+            "complete k,-k blocks are the root-reviewed exact model constraint "
+            "(OWNED_HOMOGENEOUS_COMPONENT_TRANSLATION_AND_MODE_BLOCKS_V001) under its scope; "
+            "cross-block covariances are not estimated and not evidence of mixing (LK1, LK3)"
+        ),
+        "translation_scope": {
+            "checked": [
+                "uniform lapse_factors", "uniform whitened pair sources",
+                "empty source_coefficients", "no lambda A term",
+                "equal values in every Mapping model profile",
+            ],
+            "declared_by_caller_unverified": [
+                "translation covariance of graph0, registration, port rule, frames and "
+                "energy allocation", "translation-fixed seed component of the initial paths",
+            ],
+        },
+        "normalization": (
+            "EXTENSIVE F_total = -log Z / beta derivatives; no N/2 or N factor, mode-norm "
+            "division, Legendre map, units, clipping, ridge, pseudoinverse, force law, target "
+            "scale or state-band acceptance (LK5)"
+        ),
+    }
+    return allk, layout, meta, None
+
+
+def _allk_hessian_se(se, d, beta):
+    """Symmetric F_total Hessian standard errors from the v004 y layout (upper triangle)."""
+    iu = np.triu_indices(d)
+    out = np.zeros((d, d), dtype=np.float64)
+    vals = se[d:d + iu[0].shape[0]]
+    out[iu] = vals
+    out[(iu[1], iu[0])] = vals
+    return out / beta
+
+
+def _allk_analyze(run, series, errp):
+    """allk_v001 sequential complete-block analysis (0414 items 4-5; LK4, LK5).
+
+    ONE partition (v004 _analyze's own: chain-major, batches_per_chain contiguous batches)
+    verified row by row against the stored (chain, measurement) ids; then, block by block, the
+    UNCHANGED v004 _analyze on the block's score / contact rows, and once on the background.
+    Errors are returned only when every block and the background passed (joint gate).
+    """
+    ak = run["allk"]
+    beta = run["beta"]
+    n_c = ak["n_cells"]
+    n_meas = series[0]["allk"]["score_cells"].shape[0]
+    n_batch = errp["batches_per_chain"]
+    blen = n_meas // n_batch
+    partition = []
+    for ser in series:
+        arr = ser["allk"]
+        for b in range(n_batch):
+            lo, hi = b * blen, (b + 1) * blen
+            same = bool(np.all(arr["chain_ids"][lo:hi] == ser["chain"])) and bool(
+                np.array_equal(arr["measurement_ids"][lo:hi], np.arange(lo, hi, dtype=np.int64))
+            )
+            if not same:
+                raise _Stop(
+                    "failed",
+                    run["stage"],
+                    f"all_momentum identity check: batch {b} of chain {ser['chain']} does not hold "
+                    "exactly its stored (chain, measurement) ids; one common partition cannot be "
+                    "established (equal counts are not identity; LK4)",
+                )
+            partition.append({"omission_index": len(partition), "chain": ser["chain"],
+                              "batch": b, "measurement_id_range_half_open": [lo, hi]})
+    base = {
+        "status": None,
+        "partition": partition,
+        "identity_check": (
+            "passed: every batch of the ONE partition holds exactly its stored (chain id, "
+            "measurement id) rows; the same partition and omission index serve every block, "
+            "the background and the v004 coordinate analysis (whose rows are committed with "
+            "the same ids)"
+        ),
+        "blocks": None,
+        "background": None,
+        "mixing": None,
+    }
+    if ak["zero_rate_cells"]:
+        base["status"] = "unsupported"
+        base["zero_rate_cells"] = sorted(map(repr, ak["zero_rate_cells"]))
+        base["note"] = (
+            "a zero-rate primitive with a nonzero cell weight was met (L6): the per-cell lapse "
+            "directions of these cells are unsupported, so no block estimate is returned (LK4)"
+        )
+        return base
+    root2 = np.sqrt(2.)
+    fields = []
+    for ser in series:
+        f = ser["allk"]["score_cells"].reshape(n_meas, n_c, 10).copy()
+        f[:, :, 7:10] *= root2  # TRANSFORM line 69: Mandel sqrt(2) once, before projection
+        fields.append(f)
+    sub_run = {"n_r": 0, "tracked_all": []}
+    blocks_out = []
+    for blk in ak["blocks"]:
+        _budget_check(run, "before", f"all-momentum block {blk['index']}")
+        phi = blk["phi"]
+        d = blk["dimension"]
+        off = blk["contact_offset"]
+        pseudo = []
+        for ser, f in zip(series, fields):
+            s = np.einsum("pc,mcf->mpf", phi, f, optimize=False).reshape(n_meas, d)
+            t = np.zeros((n_meas, d, d), dtype=np.float64)
+            raw = ser["allk"]["contacts"]
+            for col, (a, b) in enumerate(blk["contact_entries"]):
+                ia = blk["nn_positions"][a]
+                ib = blk["nn_positions"][b]
+                t[:, ia, ib] = raw[:, off + col]
+                t[:, ib, ia] = raw[:, off + col]
+            pseudo.append({"score": s, "contact": t, "reads": np.zeros((n_meas, 0)),
+                           "events": ser["events"],
+                           "accepted_in_measurement": ser["accepted_in_measurement"]})
+        point, per_chain, mixing, errors = _analyze(sub_run, pseudo, errp, d)
+        blocks_out.append({
+            "index": blk["index"],
+            "k": blk["k"],
+            "partner": blk["partner"],
+            "self_conjugate": blk["self_conjugate"],
+            "dimension": d,
+            "coordinate_order": blk["coordinate_order"],
+            "mode_square_sum": blk["mode_square_sum"],
+            "actual_mode_gram": blk["actual_mode_gram"],
+            "dlogZ_deta": point["g"],
+            "d2logZ_deta2": point["H"],
+            "score_covariance": point["cov"],
+            "contact_mean": point["T"],
+            "F_total_gradient": -point["g"] / beta,
+            "F_total_hessian": -point["H"] / beta,
+            "per_chain": [{"dlogZ_deta": e["g"], "d2logZ_deta2": e["H"]} for e in per_chain],
+            "mixing": mixing,
+            "errors": errors,
+            "errors_layout_note": (
+                "v004 y layout with n_u = dimension: [dlogZ_deta (d), d2logZ_deta2 upper "
+                "triangle row-major (d(d+1)/2)]; replicate i omits partition batch i, the same "
+                "batch for every block and the background; F_total = -y / beta"
+            ),
+            "F_total_gradient_standard_errors": None,
+            "F_total_hessian_standard_errors": None,
+        })
+    _budget_check(run, "before", "all-momentum background")
+    bg_labels = list(_allk_background_labels())
+    pseudo = [{"score": np.zeros((n_meas, 0)), "contact": np.zeros((n_meas, 0, 0)),
+               "reads": ser["allk"]["background"], "events": ser["events"],
+               "accepted_in_measurement": ser["accepted_in_measurement"]} for ser in series]
+    point_bg, per_chain_bg, mixing_bg, errors_bg = _analyze(
+        {"n_r": len(bg_labels), "tracked_all": bg_labels}, pseudo, errp, 0
+    )
+    statuses = [b["mixing"]["status"] for b in blocks_out] + [mixing_bg["status"]]
+    if all(st == "passed" for st in statuses):
+        joint = "passed"
+    elif "failed" in statuses:
+        joint = "failed"
+    else:
+        joint = "unassessable"
+    withheld = joint != "passed"
+    for b in blocks_out:
+        if withheld:
+            b["errors"] = None
+        elif b["errors"] is not None:
+            se = b["errors"]["jackknife_standard_errors"]
+            b["F_total_gradient_standard_errors"] = se[:b["dimension"]] / beta
+            b["F_total_hessian_standard_errors"] = _allk_hessian_se(se, b["dimension"], beta)
+    base["status"] = "analysed"
+    base["blocks"] = blocks_out
+    base["background"] = {
+        "labels": bg_labels,
+        "cell_sum_time_average_means": point_bg["m"],
+        "per_chain_means": [e["m"] for e in per_chain_bg],
+        "mixing": mixing_bg,
+        "errors": None if withheld else errors_bg,
+        "note": (
+            "time-averaged cell sums of the nine whitened reads (LK2); same partition and "
+            "omission index as every block; errors layout = read_means (9)"
+        ),
+    }
+    base["mixing"] = {
+        "status": joint,
+        "block_status": [(b["k"], b["mixing"]["status"]) for b in blocks_out],
+        "background_status": mixing_bg["status"],
+        "failed_blocks": [b["k"] for b in blocks_out if b["mixing"]["status"] == "failed"],
+        "unassessable_blocks": [b["k"] for b in blocks_out
+                                if b["mixing"]["status"] == "unassessable"],
+        "errors_withheld": withheld,
+        "note": (
+            "joint over EVERY block and the background with the caller's unchanged thresholds; "
+            "errors, replicates and covariances are returned only when all passed (v004 L13 "
+            "applied to the complete all-momentum column set); every block's diagnostics are "
+            "returned; no subset is a complete spatial response; each block's constant_columns "
+            "include its structurally zero contact entries (affine API zeros, not evidence); "
+            "acceptance is root's (LK4, LK5)"
+        ),
+    }
+    return base
+
+
 def _partial_prefixes(run, series, chain_diag, n_chains, stop):
     """v004 committed measurement prefixes on an incomplete stop (0413 items 1, 5; L24).
 
@@ -3088,6 +3756,11 @@
             "contact": entry["contact"][:n],
             "reads": entry["reads"][:n],
             "events": entry["events"][:n],
+            "all_momentum": None if entry["allk"] is None else {  # allk_v001 (LK2)
+                name: entry["allk"][name][:n]
+                for name in ("chain_ids", "measurement_ids", "score_cells", "contacts",
+                             "background")
+            },
         })
     return {
         "status": "diagnostic_prefixes",
@@ -3099,6 +3772,10 @@
         "coordinate_order_all": list(run["coords"]),
         "tracked_read_labels": list(run["tracked_all"]),
         "zero_rate_directions_seen": sorted(map(repr, run["zero_rate_directions"])),
+        "all_momentum_layout": run["allk_layout"],  # allk_v001 (LK2); None when disabled
+        "all_momentum_zero_rate_cells_seen": None if run["allk"] is None else sorted(
+            map(repr, run["allk"]["zero_rate_cells"])
+        ),
         "beta": run["beta"],
         "stop": {
             "reason": "INCOMPLETE_BUDGET" if budget else "INCOMPLETE_CAP",
@@ -3114,8 +3791,9 @@
             "padding). Wall-time/memory stopping can depend on the states reached, so these "
             "are not unbiased estimates and carry no accepted uncertainty; no mixing, error or "
             "mode analysis was run; columns follow coordinate_order_all (zero-rate directions "
-            "must be discarded) and tracked_read_labels; arrays are views of the per-chain "
-            "allocations; no resumability (L24)"
+            "must be discarded) and tracked_read_labels; all_momentum rows follow "
+            "all_momentum_layout (allk_v001, LK2; no block analysis was run); arrays are views "
+            "of the per-chain allocations; no resumability (L24)"
         ),
     }
 
@@ -3136,6 +3814,7 @@
         "read_kinds": None,
         "member_check": None,
         "modes": None,
+        "all_momentum": None,  # allk_v001 (LK1-LK5); None when all_momentum is None
         "estimates": None,
         "errors": None,
         "mixing": None,
@@ -3199,6 +3878,15 @@
                 "progress_sink(record=...) gets small synchronous records; no clock, memory "
                 "or threshold is read or hard-coded here"
             ),
+            "all_momentum": (
+                "allk_v001 (LK1-LK7): with all_momentum, every measurement also keeps chain and "
+                "measurement ids, the 10 L^3 per-cell scores (S_N = -int D_N + sum rho; int of "
+                "the nine whitened reads, raw S), the bare NN event contacts of every k,-k block "
+                "and nine background cell-sum reads; blocks use cos / +sin profiles, ten or "
+                "twenty fields, Mandel sqrt(2) once; ONE partition and common omission for every "
+                "block and the background; unchanged v004 analysis per block; errors only when "
+                "all passed; EXTENSIVE outputs, nothing normalized, inverted or clipped"
+            ),
         },
         "scope": (
             "Static isothermal native functional of the quasi-static maximum-entropy closure at "
@@ -3240,6 +3928,7 @@
     implicit_closure,
     budget_hook,
     progress_sink,
+    all_momentum,
 ):
     """Static joint source Hessians of the owned collective by positive worldline sampling.
 
@@ -3324,6 +4013,18 @@
         progress_sink(record=dict) with small stage / chain / completed-warmup /
         completed-measurement / move-counter records; return value ignored; flushing is
         the sink's; a raise is "failed".
+      all_momentum (allk_v001, 0414; LK1-LK7): None (the run is v004's), or {"L": int >= 2,
+        "cell_coordinates": {cell: three integers}} over exactly context.energy_cells, L**3
+        cells unique modulo L (the root adapter's cells are their own coordinates). Requires
+        diagonal_read_source_callback (cells equal to the energy cells). The checkable
+        translation-proof scope (uniform base lapse and pair sources, no operator-read source,
+        no lambda A term, uniform Mapping model profiles) must hold, else "unsupported"; the
+        rest of the scope is the caller's declaration. Each measurement then also keeps chain /
+        measurement ids, 10 L^3 per-cell scores, every block's bare NN event contacts and nine
+        background reads; after sampling every k,-k block (20 reals, 10 if self-conjugate) is
+        analysed sequentially with ONE partition and common omission. With all_momentum, the
+        "nothing to compute" input check accepts empty derivative_coordinates and
+        tracked_read_labels.
 
     Returns a dict: ok, status, incomplete_reason (v004), partial (v004; committed prefixes
     as diagnostics on an incomplete stop, else None; L24), stage_reached, failures, flags,
@@ -3337,7 +4038,11 @@
     mixing, diagnostics, conventions, scope, limitations. "ok" is True only when status is
     "complete", every requested direction is supported and mixing "passed". With mode
     directions and the callback, tracked_read_labels (output) ends with the nine reserved
-    uniform moment labels (L23).
+    uniform moment labels (L23). allk_v001: all_momentum (None when disabled) holds metadata
+    from the binding stage and, after a complete run, status, partition, identity_check, the
+    per-chain series, every block's extensive estimates / diagnostics / errors (errors only
+    when the joint all-momentum mixing passed), the background and the joint mixing; with
+    all_momentum, "ok" also requires that joint mixing "passed" (LK4, LK5).
     """
     result = _new_result()
     failures = result["failures"]
@@ -3402,7 +4107,14 @@
     tol = _admit_tolerances(numerical_tolerances, failures)
     hook_ok = _admit_optional_callable("budget_hook", budget_hook, failures)  # v004 (L24)
     sink_ok = _admit_optional_callable("progress_sink", progress_sink, failures)  # v004 (L25)
-    if coords is not None and tracked is not None and not coords and not tracked:
+    allk_in = _admit_all_momentum(all_momentum, failures)  # allk_v001 (LK1)
+    if all_momentum is not None and diagonal_read_source_callback is None:
+        failures.append(
+            "input all_momentum: diagonal_read_source_callback is required (the nine whitened "
+            "per-cell reads come only from the root adapter callback; LK1)"
+        )
+    if (coords is not None and tracked is not None and not coords and not tracked
+            and all_momentum is None):
         failures.append("input: no derivative coordinate and no tracked read; nothing to compute")
     result["inputs"] = {
         "beta": beta_in,
@@ -3441,6 +4153,10 @@
         "numerical_tolerances": tol,
         "budget_hook": None if budget_hook is None else ("callable" if hook_ok else "rejected"),
         "progress_sink": None if progress_sink is None else ("callable" if sink_ok else "rejected"),
+        "all_momentum": None if allk_in is None else {  # allk_v001 (LK1)
+            "L": allk_in["L"],
+            "cells": len(allk_in["cell_coordinates"]),
+        },
     }
     if failures:
         result["status"] = "failed"
@@ -3506,6 +4222,8 @@
         "burn_in_sweeps": burn,
         "measurement_sweeps": n_meas,
         "move_open": False,  # v004: True only while a proposal is unfinished
+        "allk": None,  # allk_v001: per-run all-momentum tables, set at the binding stage
+        "allk_layout": None,  # allk_v001: small row layout for partial prefixes
     }
     chain_diag = []
     series = []  # v004: per-chain arrays registered at chain start (0413 item 1)
@@ -3674,6 +4392,63 @@
             failures.append(problem)
             return result
         result["modes"] = meta
+    if allk_in is not None:
+        # allk_v001 (0414; LK1): cells, callback cells, binding L, checkable proof scope, tables.
+        if set(allk_in["cell_coordinates"]) != set(cells):
+            result["status"] = "failed"
+            failures.append(
+                "all_momentum['cell_coordinates'] must list exactly the cells of "
+                "context.energy_cells (LK1)"
+            )
+            return result
+        if set(run["pair"]["j_R"]) != set(cells):
+            result["status"] = "failed"
+            failures.append(
+                "all_momentum: diagonal_read_source_callback cells (j_R/j_S) must equal "
+                "context.energy_cells (LK1)"
+            )
+            return result
+        binding = run["pair"]["binding"]
+        if "L" in binding:
+            b_l = binding["L"]
+            if (isinstance(b_l, (bool, np.bool_)) or not isinstance(b_l, (int, np.integer))
+                    or int(b_l) != allk_in["L"]):
+                result["status"] = "failed"
+                failures.append(
+                    f"all_momentum['L'] = {allk_in['L']} differs from the callback binding "
+                    f"L = {b_l!r} (LK1)"
+                )
+                return result
+        scope = _allk_scope_problems(model, lapse, run["pair"], sources, vgrad, lam)
+        if scope:
+            result["status"] = "unsupported"
+            failures.append(
+                "all_momentum: the checkable scope of the translation block proof does not hold, "
+                "so complete k,-k blocks would not be a complete spatial response (LK1)"
+            )
+            failures.extend(f"all_momentum scope: {p}" for p in scope)
+            return result
+        try:
+            _budget_check(run, "before", "all-momentum setup")  # allk_v001 (LK6)
+        except _Stop as stop:
+            return _stopped(stop)
+        ak, layout, ak_meta, problem = _allk_setup(run, allk_in)
+        if ak is None:
+            result["status"] = "failed"
+            failures.append(problem)
+            return result
+        run["allk"] = ak
+        run["allk_layout"] = layout
+        result["all_momentum"] = {
+            "status": "not_analysed",
+            "metadata": ak_meta,
+            "partition": None,
+            "identity_check": None,
+            "series": None,
+            "blocks": None,
+            "background": None,
+            "mixing": None,
+        }
 
     n_u = run["n_u"]
     n_r = run["n_r"]
@@ -3720,6 +4495,18 @@
             contact = np.zeros((n_meas, n_u, n_u), dtype=np.float64)
             reads = np.zeros((n_meas, n_r), dtype=np.float64)
             n_events = np.zeros(n_meas, dtype=np.int64)
+            allk_rows = None
+            if run["allk"] is not None:
+                # allk_v001 (0414 item 3; LK2): ids start at -1 so an unwritten row can never
+                # pass the analysis identity check.
+                allk_rows = {
+                    "chain_ids": np.full(n_meas, -1, dtype=np.int64),
+                    "measurement_ids": np.full(n_meas, -1, dtype=np.int64),
+                    "score_cells": np.zeros((n_meas, 10 * run["allk"]["n_cells"]),
+                                            dtype=np.float64),
+                    "contacts": np.zeros((n_meas, run["allk"]["n_contact"]), dtype=np.float64),
+                    "background": np.zeros((n_meas, 9), dtype=np.float64),
+                }
             # v004 (0413 item 1): the chain is registered BEFORE its first sweep; its
             # committed count advances only after a whole measurement tuple is written.
             entry = {
@@ -3730,6 +4517,7 @@
                 "events": n_events,
                 "measurements_committed": 0,
                 "accepted_in_measurement": 0,
+                "allk": allk_rows,  # allk_v001 (LK2)
             }
             series.append(entry)
             _progress(run, "chain_start", run["stage"], diag, None)  # v004 (L25)
@@ -3757,10 +4545,17 @@
                 if measuring:
                     i = sweep - burn
                     s_vec, t_mat, r_vec, k = _measure(run, path)
+                    allk_row = None if allk_rows is None else _measure_allk(run, path)
                     score[i] = s_vec
                     contact[i] = t_mat
                     reads[i] = r_vec
                     n_events[i] = k
+                    if allk_row is not None:  # allk_v001 (LK2): same commit as the v004 tuple
+                        allk_rows["score_cells"][i] = allk_row[0]
+                        allk_rows["contacts"][i] = allk_row[1]
+                        allk_rows["background"][i] = allk_row[2]
+                        allk_rows["chain_ids"][i] = c
+                        allk_rows["measurement_ids"][i] = i
                     entry["measurements_committed"] += 1  # v004: whole tuple committed
                     diag["measurements"] += 1
                 else:
@@ -3789,6 +4584,17 @@
         )
         result["diagnostics"] = _diagnostics()
         return result
+    allk_res = None
+    if run["allk"] is not None:
+        # allk_v001 (0414 items 4-5; LK4): BEFORE the v004 column slicing below, so a budget
+        # stop here still returns the unmodified committed prefixes (L24).
+        run["stage"] = "all_momentum_analysis"
+        try:
+            _progress(run, "stage", "all_momentum_analysis", None, None)
+            allk_res = _allk_analyze(run, series, errp)
+        except _Stop as stop:
+            return _stopped(stop)
+        run["stage"] = "analysis"
     supported = [i for i, c in enumerate(coords) if c not in run["zero_rate_directions"]]
     result["direction_status"] = {
         repr(c): ("supported" if i in supported else "unsupported: zero-rate source-opening")
@@ -3854,7 +4660,32 @@
             f"mixing {mixing['status']}: no error band, replicate set or covariance is returned; "
             "estimates are evidence only"
         )
+    allk_ok = True
+    if allk_res is not None:
+        # allk_v001 (LK2-LK5): series, every block, background, joint mixing.
+        out = result["all_momentum"]
+        out.update(allk_res)
+        out["series"] = [
+            {"chain": ser["chain"], "chain_ids": ser["allk"]["chain_ids"],
+             "measurement_ids": ser["allk"]["measurement_ids"],
+             "score_cells": ser["allk"]["score_cells"], "contacts": ser["allk"]["contacts"],
+             "background": ser["allk"]["background"], "events": ser["events"]}
+            for ser in series
+        ]
+        allk_ok = (out["status"] == "analysed" and out["mixing"] is not None
+                   and out["mixing"]["status"] == "passed")
+        if out["status"] != "analysed":
+            result["flags"].append(
+                "all_momentum unsupported (zero-rate lapse cells, L6): no block estimate; the "
+                "per-cell series is returned as evidence only (LK4)"
+            )
+        elif not allk_ok:
+            result["flags"].append(
+                f"all_momentum joint mixing {out['mixing']['status']}: no block or background "
+                "error, replicate or covariance is returned; block estimates are evidence only "
+                "and no subset of blocks is a complete spatial response (LK4)"
+            )
     result["status"] = "complete"
     result["stage_reached"] = "complete"
-    result["ok"] = mixing["status"] == "passed" and len(supported) == len(coords)
+    result["ok"] = mixing["status"] == "passed" and len(supported) == len(coords) and allk_ok
     return result
```
