# REVIEW 0414 ALLK V001: all-momentum feature branch of the 0413 evaluator v004

**Role.** Distinct reviewer, not author. I wrote no part of `owned_collective_worldline_static_response_allk_v001.py`, its DELTA, v004 or any earlier version of the 0407 module.

**Method (static only).** Nothing was imported or executed: not the branch, not v004, not the TRANSFORM, not any operator or the root adapter. No run, sampling, timing, benchmark, network or install. The only commands were `shasum -a 256`, `diff -u`, `cmp`, `patch` (on a scratch copy of v004), and `python3 -I` doing `ast.parse`, `compile` (no exec) and `symtable` on TEXT copies in my scratch directory, plus one arithmetic one-liner for the cost table (no module import). Read-only on `Universal Network Theory`; no file with a forbidden name opened. No `__pycache__` in the 0407 directory. This file was written by exclusive create; nothing was overwritten, moved, deleted or chmod-ed.

## Verdict: PASS_WITH_NOTES

**Blocking issues: none.** I found no wrong algebra, sign, normalization, index convention or target-law change, no crash on valid input reachable from the admitted inputs, and no hard-rule violation. The notes below are for the merge revision and root's launch planning.

## Hashes (full sha256, recomputed from bytes; all match)

| File | sha256 |
|---|---|
| 0414 task `FROM_CODEX/0414_2026-10-16_all_momentum_response_from_one_ensemble.md` (read fully) | 64742c18a6d51468bc20b3c2a32e06c91bfe50c807a56269418822231bd28ef1 |
| BASE `owned_collective_worldline_static_response_v004.py` (unchanged) | 6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea |
| BRANCH `owned_collective_worldline_static_response_allk_v001.py` (234718 B, 4691 lines) | c37bca61b35579492d5a306519288762a596d787ed7c62d2fe0df2599a4ecbdd |
| `DELTA_0414_ALLK_V001.md` (1341 lines) | 5fa4771736d9bbe10e9fe7e0afe8ee71b4ef9168bed7c5718e8d27af6997a5c8 |
| `CODEX1/OWNED_HOMOGENEOUS_COMPONENT_TRANSLATION_AND_MODE_BLOCKS_V001.txt` (read) | d51e57761f7f55feab30671cf22898a337caf6e2af835c9d0c437db87bc305bb |
| `helpers/response_packet_audit/OWNED_HOMOGENEOUS_TRANSLATION_MODE_BLOCKS_DISTINCT_REVIEW_V001.json` (read) | 5b7ffb0fbd94c38dd98231dcbd867014144133759ca6dd300094a71ffc38adf9 |
| TRANSFORM `helpers/coefficient_method/owned_all_momentum_path_algebra_v002.py` (read as text) | 2de6e987ed8265caf91b934a9a777b84d42a908800cb735b0773d97ed339a0f5 |
| downstream `helpers/coefficient_method/owned_positive_cardinal_source_hessian_v001.py` (hashed only) | 4d123c1f01bdb20f2bd8a0dcc42e12475f09850eff8f6bbca9d5953d01326848 |
| operator `owned_retained_response_0405/owned_parent_operator_v003.py` (text: record kinds, energy_weights) | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 |

Context read: `DELTA_0410_BUDGET_V004.md`, `REVIEW_0410_BUDGET_V001.md`, `CONVENTIONS_0407_V003.md` and `DELTA_0410_MODES_V003.md` (relevant sections).

## Diff and AST

- My own `diff -u` v004 → branch has 36 hunks (+848/−17 lines). The diff embedded in the DELTA (lines 213-1340) is hunk-for-hunk identical to mine, and `patch` applied to a copy of v004 reproduces the branch byte for byte (`cmp` identical; sha256 c37bca61...).
- All 17 removed lines are accounted for: signature/docstring text, the `_progress` module string, the 3→4-tuple returns of `_diagonal_at`/`_reads_at` and their one caller `_segment_core`, the two dict literals that gained `allk` keys, the relaxed nothing-to-compute guard and the `ok` expression.
- Top level: 9 defs added, 0 removed, 9 functions changed (`_channels_from_records`, `_diagonal_at`, `_event_from_channel`, `_new_result`, `_partial_prefixes`, `_progress`, `_reads_at`, `_segment_core`, public function) plus the `LIMITATIONS` assignment (the DELTA's "10 changed"), 89 AST-identical. Identical includes `_analyze`, `_estimate`, `_sums`, `_sokal_tau`, `_rhat`, `_measure`, `_move`, `_interval_move`, `_palette_move`, `_ctmc_segment`, `_rotate`, `_initial_path`, `_budget_check`, `_mode_metadata`, `_mode_outputs`, `_admit_error_parameters`.
- `ast.parse` and `compile` succeed; `symtable` finds no undefined globals. Module level holds only the docstring, four imports (`bisect`, `math`, `collections.abc.Mapping`, `numpy`), the `LIMITATIONS` string, two classes and defs: inert at import. No `@`, `dot`, `matmul`, `vdot`, `inner`, `tensordot`, `linalg`, `open`, `print`, `exec`/`eval`, `global`/`nonlocal` or decorators. 17 `einsum` calls (10 in v004 + 7 new), every one with literal `optimize=False`.
- One public callable: 0 positional, 26 keyword-only parameters, no defaults: v004's 25 in order, then `all_momentum`.

## Verification by requirement

**Item 1: per-cell S_N, nine reads, sparse event ρ, no double count. VERIFIED.**
- D_N(c) (`_diagonal_at` 2138-2139, 2171-2176) appends `value * w` over the same `diagonal_terms` records, in the same order, as v004's `("lapse", cell)` term list, and sums with `math.fsum`; it is therefore bit-equal to v004's D_a for that cell. H = Σ d_X(1 + Σ_c n_c w_cX) gives ∂H/∂N_c = Σ d_X w_cX, the correct lapse derivative.
- Reads (`_reads_at` 2377-2384) are taken from the SAME `adapted_moment_reads` evaluation that has just passed the pair-source consistency check, in `context.energy_cells` order and TRANSFORM order (R0,R1,R2,S00,S11,S22,S12,S02,S01), raw S, never re-whitened.
- Density (`_segment_core` 2415-2423) is `[-D_N, O_1..O_9]` per cell; it never enters D, r, W or any move decision.
- ρ_c (`_event_from_channel` 2463-2470) is `w_c / mult` of the sampled channel's own nonzero endpoint-mean `energy_weights`, identical to v004's `("lapse", cell)` ρ. Each operator record is a separate channel and only the chosen one marks the event; `"diag"` records of `primitive_channels` remain skipped (1956-1957), so diagonal owners enter only through `diagonal_terms`. No channel is counted twice.
- `_measure_allk` (2999-3010) integrates over the same `bounds` as `_measure` (segment j spans [t_j, t_{j+1}), K+1 segments), then adds Σ_events ρ_c to column 0 only: S_N(c) = −∫D_N dτ + Σρ_c; columns 1-9 are +∫O dτ (sign of H − j·O, as v004's pair-source D_a = −O). No β division.
- All segments and events of every path are built after `run["allk"]` is set (initial paths are built after binding, 4459-4462), so no segment lacks its density.
- Recoverability (checked by hand): v004 lapse-direction scores are Σ_c φ_c S_N(c) and ρ_a = Σ_c φ_c ρ_c; v003 source-direction scores are Σ_c φ_c Σ_f c_f ∫O_c,f; pair_source_S off-diagonal scores are 2∫S_ij; v003 uniform moments are the background reordered. All are exact linear projections of the stored per-cell data (algebraically; summation order differs in the last bits). Contacts: see N3.

**Item 2: every k,−k block, +sin, no phase average, Mandel once, NN contacts only. VERIFIED.**
- `_allk_setup` 3419-3426, 3441 matches TRANSFORM lines 62, 80-97 statement for statement: coordinates reduced mod L, `np.ndindex((L,L,L))`, skip `k > partner` in tuple order, phase = (2π/L) k·x, φ = cos for k = −k mod L else (cos, +sin), Gram φφᵀ, `mode_square_sum` L³ or L³/2.
- Count: at L4, 8 self-conjugate + 28 pair blocks = 36 blocks, 8 + 56 = 64 real profiles = L³ (complete real basis; checked again at 3449). L6: 8 + 104; L8: 8 + 252.
- Block score (3644): `einsum("pc,mcf->mpf")` reshaped profile-major, identical to TRANSFORM `'pc,cf->pf'` per row; `coordinate_order` and `nn_positions` (0, 10) match TRANSFORM `nn = 10*arange(p)`.
- Mandel: `score_cells` stores raw S; √2 is applied once, to the per-cell S12/S02/S01 columns of a copy (3629-3634), before projection. The stored series is untouched (`.copy()`), the background carries no factor, and nothing else scales S.
- Contacts: `_measure_allk` 3011-3018 forms v[p, event] = Σ φ[p, cells]·ρ by a per-event `bincount` and −Σ_events v vᵀ (`einsum`, optimize=False), equal to TRANSFORM lines 88-92; stored as 1 or 3 independent entries and re-expanded symmetrically at the N-N positions (3646-3651). All other entries are zero and labelled zero "IN THIS API ONLY"; Legendre, metric, preparation, read-frame and mean-map contacts are explicitly not declared zero. Correct for the affine fixed-read API (W depends only on lapse; D affine in N and j).

**Item 3: ids, 10L³ scores, contacts, background, time series. VERIFIED.**
- Rows allocated with the v004 arrays (4498-4509; ids initialised to −1), computed before any write, written with chain id c and measurement id i at index i BEFORE `measurements_committed += 1` (4547-4559). Complete runs return every chain's full series (4668-4674); incomplete stops return views of committed rows (3759-3763) plus layout (3775).
- Row size: 640 + 92 + 9 = 741 float64 + 16 B ids = 5,944 B at L4; 1,521,664 B per 256 rows (≈1.52 MB). No batch-sum replacement.

**Item 4: one partition, common omission, sequential blocks, unchanged checks. VERIFIED.**
- `_allk_analyze` 3590-3607 builds the chain-major × `batches_per_chain` partition, which is exactly the `block_sums` order of the unchanged `_analyze`, and checks every row's stored (chain, measurement) id against it (fails closed; counts alone are not used).
- Each block then runs the unchanged v004 `_analyze` (3655) on its d score columns and d×d contact rows, and the background runs once (3687), all with the same `series` order, the same `errp`, the same thresholds, plug-in mean subtraction, Cov + ⟨T⟩, (J−1)/J jackknife, R-hat, Sokal τ and stuck-chain failure. Replicate i omits the same partition batch for every block, the background and the v004 coordinates.
- Joint gate (3690-3697): passed only if every block and the background passed; otherwise all block and background errors are withheld (v004 L13 applied to the complete column set). Every block's diagnostics are returned regardless, and a flag (4682-4687) states that no subset is a complete spatial response.

**Item 5: extensive outputs, metadata, nothing applied. VERIFIED.**
- Per block: dlogZ, d2logZ = Cov + ⟨T⟩, F_total gradient −g/β and Hessian −H/β, per-chain values, mixing, errors, and standard errors (gradient `se[:d]/β`; Hessian from the row-major upper triangle `se[d:d+d(d+1)/2]`, mirrored, /β; checked against the v004 y layout). Same algebra as TRANSFORM `estimate`.
- Metadata: ordering, profile values, per-block Gram, `mode_square_sum`, cross-profile Gram maximum, layouts, Mandel and sign notes. No division by a mode norm, N/2 or N factor, Legendre, units, clipping, ridge, pseudoinverse, force law, target scale or state-band acceptance anywhere in the added code.

**Item 6: 0413 semantics, RNG law, costs, optimize=False. VERIFIED.**
- With `all_momentum=None` every added statement is inert (guards on `run["allk"]`/`allk_in`). Hook calls, sink records (apart from the module string value), draws, rates, analysis and thresholds are v004's.
- With `all_momentum` set, all move/CTMC/RNG functions are AST-identical and the added code draws no random number and makes no operator or adapter call. The draw sequence is therefore v004's for the same hook answers. Added hook polls: one at binding (4432), one before each block (3638) and one before the background (3682), never during sampling.
- Valid-prefix: a row is visible only after its whole v004 + all-k tuple is written. The all-k analysis runs before v004's column slicing, so a budget stop inside it still returns unmodified prefixes (INCOMPLETE_BUDGET). Non-finite rows and identity failures are fail-closed `failed`.
- Cost table reproduced arithmetically: L4/L6/L8 = 741/2,489/5,893 doubles; 5,944/19,928/47,160 B; 1.52/5.10/12.07 MB per 256-row chain; 5,120/17,280/40,960 B per dwell segment; Mandel copy 1.31/4.42/10.49 MB per chain; per-block explicit covariances 12.12/44.28/106.92 MB; 409.6 MB of densities for a 10⁴-event L8 path. Disclosed costs are accurate.

**Scope gate.** `_admit_all_momentum` (835-877) and binding (4395-4451) check L ≥ 2, integer coordinates, exactly L³ cells unique mod L, cells = `context.energy_cells` = callback cells, binding L if present. `_allk_scope_problems` refuses nonuniform lapse, nonuniform whitened (post-conversion) pair sources, nonempty `source_coefficients`, a λA term and nonuniform Mapping profiles. These match the checkable part of the root proof's scope. The rest is recorded as the caller's declaration.

## Notes (non-blocking)

- **N1. Integration.** The order 0413 v004 → {W2 sequential, this branch} → explicit merge revision is stated, and the embedded diff re-applies cleanly to v004. The conflict list is plausible. LK labels avoid W2 L-numbers.
- **N2. Required keyword.** v004-style callers must now pass `all_momentum=None` (required, no default, per the hard rules). The progress record keeps its keys, but `"module"` now reads `..._allk_v001` even when disabled. Root's sink must not key on the v004 value.
- **N3. Contact recoverability is per block only.** Scores, read averages and the background are exactly recoverable for any profile. Contacts are recoverable for any single-k profile (the uniform k = 0 direction and the 0410 joint cos/sin block, any phase or scale) from the 1 or 3 stored NN entries. They are NOT recoverable for a profile mixing several momenta: per-sample cross-block contacts and per-event sparse ρ are not stored, and they vanish only in exact expectation under the proof. This is the 0414/TRANSFORM row design, and v004 coordinates are still computed directly in the same run, so no requested output is lost.
- **N4. Memory at L6/L8.** Dense per-segment densities (80·L³ B) on every stored and proposed path roughly add one state-sized array per dwell. At L8 a 10⁴-event path holds about 410 MB of densities. REVIEW_0410_BUDGET N2 still applies: an in-process `MemoryError` escapes and loses all prefixes, and this branch makes that route more likely. Root's 900 MiB planning should include densities, per-chain all-k rows and the analysis Mandel copies, which are held for all chains at once. The per-chain all-k allocation also sits before the `chain_start` record (REVIEW_0410_BUDGET N1 carries over, with a larger allocation).
- **N5. Stops inside the all-k analysis.** A hook stop between blocks returns status `incomplete`/INCOMPLETE_BUDGET after sampling finished. Blocks analysed before the stop are discarded, so the partial note "no mixing, error or mode analysis was run" is literally inexact; the checkpoint text identifies the block. No sink record is emitted per block, so a hard kill there is located only to stage `all_momentum_analysis`.
- **N6. Gates are separate.** v004 coordinate errors can be returned while the all-k joint gate withholds block errors. `ok` is then False. Partition and omission are common to both; root should key on `ok` and `all_momentum.mixing.status`.
- **N7. Identity check is structural.** It proves every row was written with its own (chain, index) id and that partition batch i holds exactly those rows. v004 coordinate rows carry no ids; they share the commit step and index. The `identity_check` text ("committed with the same ids") is slightly loose on that point.
- **N8. bincount for v.** Per-event projections use `np.bincount(weights=...)` (a non-BLAS segmented sum) instead of the TRANSFORM's `einsum('pc,c->p')`. The algebra is identical and consistent with the optimize=False intent; repeated cells are summed as in the TRANSFORM.
- **N9. Covariance threshold is per block.** `max_explicit_covariance_dimension` applies per block (n_y = 230 or 65), not to a joint all-k vector. A threshold sized for v004 coordinates can yield about 107 MB of block covariances at L8. Cross-block jackknife covariances can be formed by root from the returned replicates (same omission index) when the joint gate passes.
- **N10. Block mixing columns.** Each pair (self-conjugate) block's 231 (66) primary columns include 207 (52) structurally zero contact columns, reported as `constant`, plus the shared `events_per_path` column. These are documented API zeros, not evidence.
- **N11. Background convention.** (1/β)∫Σ_c O dτ: extensive cell sums, raw S, TRANSFORM order, which differs from the v003 L23 order. The k = 0 block's read scores carry the same information (×β, Mandel on off-diagonals). Labels are explicit.
- **N12. Strict scope.** Nonempty `source_coefficients` or any λA term makes the whole run `unsupported`, even if it might be invariant. Graph/registration/port/frame/allocation covariance and the seed-component membership of `initial_paths` are unverified caller declarations.
- **N13. Unsupported zero-rate cells.** These cannot occur under the checked uniform positive lapse (multiplier = N > 0); the branch is fail-closed if they do.

## LIMITATIONS of this review

- Everything is static. Bit-identity of the draw sequence and the transition law rests on AST identity plus a hand trace; no run confirmed it. It assumes the caller's hook and sink never draw from `chain_generators` or mutate inputs.
- Numerical behaviour (rounding of the sequential time integral against v004's einsum, FFT diagnostics on 260 blocks, actual memory and timing) is unmeasured; root supplies timing.
- The root adapter `owned_diamond_registration_input_adapter_v001.py` was not read in this review; translation covariance of registration, ports, frames, allocation and the seed component rests on the root proof and its review, as declared by the branch.
- The downstream positive-cardinal source Hessian was hashed only, not read; compatibility of the branch's output layout with it is not checked here.
