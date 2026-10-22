# REVIEW 0410 BUDGET V001: 0413 cooperative budget / partial-return delta (v004)

**Role.** Distinct reviewer, not author. I did not write v004, its DELTA document or any earlier version of the 0407 module.

**Method.** Static only. I imported and executed nothing: not the module, not any operator and not the root adapter. I ran no numbers, did no sampling, used no network and installed nothing. The only commands I ran were:
- `shasum -a 256`;
- `diff -u`;
- `cmp`;
- `python3 -I -B` doing `ast.parse`, `compile` (no exec) and `symtable` on TEXT copies in my own scratch directory.

I wrote nothing under `Universal Network Theory` and opened no file with a forbidden name. There is no `__pycache__` in the 0407 directory. This file was written by exclusive create.

## Verdict: PASS_WITH_NOTES

**Blocking issues: none.** I found:
- no wrong math, normalization or target distribution;
- no interface mismatch that gives wrong numbers;
- no crash on valid input;
- no hard-rule violation.

All five 0413 items are met in the text. With the hook never firing, the RNG draw sequence and the transition law are those of v003. This rests on AST identity, checked by hand and by a strip comparison. It is not measured.

Notes N1 and N2 below matter for the next root launch. They concern stage identification and evidence loss at memory exhaustion, which is how RunV001 ended.

## Hashes (full sha256, recomputed from bytes)

All binding inputs match.

| File | sha256 | Result |
|---|---|---|
| `FROM_CODEX/0410_2026-10-16_direct_mode_columns_and_equal_time_pair_completion.md` | ac1db8fa81c06672d495448b82835072978dee8bce0d3a017044de29cc440e34 | matches binding |
| `FROM_CODEX/0413_2026-10-16_preserve_collective_measurements_on_bounded_exit.md` (read fully) | adfc9185663bb79880a85bc3bbd0194fa208df8aaf2404ca192499b3cddbf383 | matches binding |
| `owned_collective_worldline_static_response_v004.py` (187151 B, 3860 lines) | 6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea | matches author report |
| `DELTA_0410_BUDGET_V004.md` (854 lines) | f6f3676689cff30f3429094517aa3ae4624b08aae9dc19d7527f09ed2f742c24 | matches author report |
| `owned_collective_worldline_static_response_v003.py` (base of the delta) | e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721 | unchanged; same hash as reviewed in REVIEW_0410_MODES_V001 |
| `owned_collective_worldline_static_response_v002.py` (evaluator base) | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 | unchanged |
| `FIX_DELTA_0407_V002.md` | 94c1518231d42b58418111f790611d3c5d635195e6fbc4d88c5c66e2757a7b41 | read |
| `FINAL_CHECK_0407_V001.md` | 1e352a9eac3d672bf93da60ba4c00270eb1279269208e5052628b060e1d19042 | read |
| `REVIEW_0407_PALETTE_V001.md` | 251a6077291e44bc1f3a658abc138cfeacf16084684b7720c8561e1646d20c29 | read |
| `REVIEW_0410_MODES_V001.md` (v003 review) | 19eb6c88d95142e5b2bf4b62777f90ae49aa3c2f7e1b663685e2d1e67713b269 | read |
| operator `owned_parent_operator_v002.py` (present, so used) | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e | read as text (signatures) |
| root adapter `owned_diamond_registration_input_adapter_v001.py` | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 | matches binding; read as text (signatures) |
| registration `OWNED_DIAMOND_CURRENT_GRAPH_COLLECTIVE_REGISTRATION_PROPOSED_V001.json` | f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 | matches binding (semantics; this delta does not touch them) |
| companion `OWNED_DIAMOND_WHITENING_DUAL_SOURCE_MANDATORY_COMPANION_V001.json` | 9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7 | matches binding (semantics; this delta does not touch them) |

## Diff verification

- My own `diff -u v003 v004` on scratch text copies is 689 lines in 28 hunks.
- Its body, without the two header lines, is byte-identical (`cmp`) to the diff embedded in the DELTA document at lines 167-853.
- The v002→v003 part was reviewed in REVIEW_0410_MODES_V001, against the same v003 hash. So v004 is v002, plus the reviewed v003 changes, plus the diff checked here.

I compared top-level defs by AST:
- 5 added: `_BudgetStop`, `_admit_optional_callable`, `_budget_check`, `_progress`, `_partial_prefixes`.
- 0 removed.
- 7 changed: `LIMITATIONS`, `_ctmc_segment`, `_new_result`, `_op`, `_palette_move`, `_reads_at` and the public function.
- 87 AST-identical.

This matches the author report.

## Requirement trace (0413; v004 line numbers)

| 0413 item | Where | Hand-trace result |
|---|---|---|
| **1. Per-chain arrays registered immediately; count only after a full commit; prefixes only; no zero padding; no burn-in.** | `series = []` is created before any stop can happen (3511). Each chain's `entry` is appended before sweep 0 (3725-3734). The commit is at 3757-3765. Burn-in is handled at 3766-3767. `_partial_prefixes` is at 3070-3120. The analysis guard is at 3782-3791. | **MET.** `score[i]`, `contact[i]`, `reads[i]` and `n_events[i]` are written before `measurements_committed += 1`. No hook, sink or operator call lies between them, and `_measure` has none either, so a budget stop cannot interrupt a row. Burn-in sweeps only advance `burn_in_sweeps_completed`; no row is written. Prefixes are `[:n]` slices of the committed count, so a chain stopped in burn-in returns shape-(0, ...) arrays. The v003 evidence-loss path is gone: v003 appended `series` only after all sweeps and dropped it in the `except _Stop` handler. The new guard means no row that is short of `n_meas` can reach `_analyze`. |
| **2. Required caller hook (callable or explicit None); checked before/after costly calls and between jumps and sweeps; INCOMPLETE_BUDGET distinct from validation failure; no RNG; unfinished proposal not turned into a rejection or measurement; no resumability.** | The signature is at 3241. Admission is at 3403. `_budget_check` is at 1545-1568 and `_BudgetStop` at 568-581. Check sites: `_op` before/after (1604/1613); `validate_owned_model` (3553/3574); adapter reads (2046/2058/2065/2074); CTMC jumps (2326); palette jumps (2520); held replay (2542); chain arrays (3718); sweep start (3744); between moves (3749); pre-analysis (3779). | **MET.** Every check site sits outside a `try` that catches `Exception`. `_op` re-raises `_Stop` before its generic handler. I found no `except _Stop` inside the move code, so a `_BudgetStop` always reaches `_stopped` (3771/3554/3576/3604/3780). It cannot become a rejection: every rejection counter is incremented immediately before its `return`, with no check between, and the accept/reject outcome is only assigned after `_move` returns. A budget stop gives status `incomplete` with `incomplete_reason` `INCOMPLETE_BUDGET` (3535). Validation failures stay `failed`/`unsupported` with reason None, and a hook that raises or returns a non-bool is `failed`. The check receives no Generator, state or path, and touches only `counters["budget_checks"]`. `resumable: False` is set; no RNG state or path is returned. |
| **3. Root's 150 s / 900 MiB cooperative policy documented, not hard-coded; indivisible-enumeration overrun reported.** | BUDGET paragraph 99-114; L26 at 543-554; public docstring 3316-3322. | **MET.** The AST has no numeric constants other than 0, 0.5, 1, 2, 3, 4 and 20, all from v003. It contains no clock, memory, OS or I/O name. The reserve arithmetic (180-150 = 30 s; 1024-900 = 124 MiB) is correct. |
| **4. Small stage/chain/warmup/measurement/move-counter records through a caller sink; no file I/O; no per-sample journal.** | `_progress` 1571-1594. Emitted at the model (3552), member_check (3575), binding (3603), initial_paths[c] (3686) and analysis (3778) stages, at chain_start (3735), after every completed sweep (3769) and at the stop (3544). | **MET.** Each record holds counters only: `dict(diag)` and `dict(run["counters"])`. It carries no sample values. The sweep record follows the commit, so `measurements_committed` is exact. Flushing is the sink's. See N1 for one stage-identification gap. |
| **5. Partial prefixes, metadata and explicit status with ok False; no mixing analysis after a stop; prefixes labelled diagnostics; completed runs unchanged.** | `_stopped` 3520-3547; partial label 3093 / 3111-3119; flag 3538-3542. | **MET.** `_stopped` returns before `_analyze`. `ok` stays False from `_new_result`, and estimates, errors, mixing and direction_status stay None. `_analyze`, `_sums`, `_estimate`, `_layout`, `_sokal_tau`, `_rhat`, `_mode_metadata` and `_mode_outputs` are AST-identical to v003. The post-analysis assembly (3792-3860) is unchanged apart from the guard placed before it. |
| **Bit-identity with the hook never firing.** | | **MET (static).** `_move`, `_interval_move`, `_select_interval`, `_rotate`, `_choose_channel`, `_initial_path`, `_segment_core`, `_channels_at`, `_palette_channels`, `_diagonal_at`, `_channels_from_records`, `_enumeration_tick`, `_count_new_event` and `_measure` are AST-identical. With the `_budget_check`/`_progress` statements stripped, `_ctmc_segment`, `_palette_move` and `_reads_at` are AST-identical to v003, and every check sits before the corresponding `rng.exponential`. `_op` returns the same object (`out = fn(**kwargs)` followed by `return out`). Main loop: `for mv in range(...)` replaces `for _ in range(...)`; the `if mv > 0` check and the `move_open` assignments draw nothing; the `run["stage"]` string is assigned before the sweep counter instead of after, and `run["stage"]` is used only in messages (grep). `budget_checks` is read only by diagnostics. |

## Estimator algebra and normalization (hand trace; unchanged from v003)

`_measure`, `_sums`, `_estimate` and `_analyze` are AST-identical to v003. I re-traced them anyway, since a delta must not change them:
- **Path weight and score.** The path weight is exp(-∫₀^β D dτ) · Π W_e. Then ∂_a log weight = -∫ D_a dτ + Σ_e W_{e,a}/W_e. `score = -einsum("l,la->a", dur, da) + Σ rho` with `rho = w/mult` for lapse and the projected `v_X/mult` for lapse directions; it is extensive over [0, β].
- **Contact term.** Because D and W are affine in u (lapse multiplier 1 + Σ n w; sources linear), ∂_b(W_a/W) = -ρ_a ρ_b and ∂_ab D = 0. That gives `contact = -einsum("ka,kb->ab", rho, rho)`.
- **Hessian and free-energy derivatives.** d²logZ = Cov(S) + ⟨T⟩ is `cov + tmean`. F_u = -g/β and F_uu = -H/β.
- **Reads.** `read_avg = Σ dur·row / β` is the time average. The response ⟨S R⟩ - ⟨S⟩⟨R⟩ = d⟨R⟩/du holds because reads are state functions independent of u.
- **Errors.** The jackknife is leave-one-batch-out on the total sums with factor (J-1)/J.

No normalization changed.

## Actual operator / adapter API (text only; unchanged by the delta)

v004 adds no operator or adapter call. It only brackets existing calls. The calls match the actual definitions:

| Call | Definition |
|---|---|
| `validate_owned_model(*, graph0, model, registration)` | operator v002 L979 |
| `canonical_state_key(*, context, state)` | operator v002 L1772 |
| `state_labels(*, context, state)` (used by the adapter) | operator v002 L1783 |
| `diagonal_terms(*, context, state)` | operator v002 L1789 |
| `primitive_channels(*, context, state)` | operator v002 L1801 |
| `palette_channels(*, context, state, palette_owners)` | operator v002 L1837 |
| `read_rows(*, context, state)` | operator v002 L1861 |
| `adapted_moment_reads(*, operator_module, context, state, binding)` | adapter L177 |
| `pair_source_hamiltonian(*, reads, j_R, j_S)` | adapter L235 |
| `raw_to_whitened_sources(*, j_R_raw, j_S_raw)` | adapter L254 |

`_admit_operator_api` is AST-identical to v003.

## Interface, semantics and inertness (AST on the text copy)

- `ast.parse` and `compile` (no exec) succeed. `symtable` finds no undefined globals.
- Imports are only `bisect`, `math`, `collections.abc.Mapping` and `numpy as np`.
- There is no `MatMult` and no `dot`, `matmul`, `vdot`, `inner`, `tensordot` or `linalg`. There are 10 `einsum` calls, all with `optimize=False`.
- No `open`, `print`, `exec`, `eval`, `__import__`, `os`, `sys`, `time`, `threading` or `subprocess`. No decorators and no global/nonlocal.
- Module level holds only the docstring, imports, the `LIMITATIONS` string, two classes and defs. Nothing runs at import.
- There is exactly one public callable, `owned_collective_worldline_static_response`. It has 0 positional parameters and 25 keyword-only parameters with no defaults: the 23 of v003 in the same order, plus `budget_hook` and `progress_sink`.
- The tuple and mode-direction coordinate interfaces are unchanged (`_admit_coordinates` is AST-identical).
- Every new result key is additive: `incomplete_reason`, `partial`, `inputs.budget_hook`/`progress_sink`, `diagnostics.counters.budget_checks`, per-chain `burn_in_sweeps_completed`, and `conventions.budget`.

Stop handling also passes a crash trace:
- `_stopped` references `paths_in` (bound at 3382), `series` and `chain_diag` (bound at 3510-3511), and `run["coords"]`, `run["tracked_all"]`, `run["beta"]` and `run["zero_rate_directions"]`. All are bound before the first checkpoint at the model stage, so a hook returning True at its very first call returns cleanly with `partial.chains == []`.
- `chain_diag[entry["chain"]]` is valid because both lists are appended in chain order.
- Every `_Stop("incomplete", ...)` raise in the module is a cap (1688, 2336, 2342, 2462, 2468, 2627, 3739), so the `INCOMPLETE_CAP` label is accurate.

## Blocking issues

None.

## Notes (non-blocking)

- **N1. A hard kill during chain array allocation is ambiguous for chain 0. Recommended small fix before root launch.**
  - The `chain_start` record is emitted after `np.zeros` (3719-3735).
  - For chain 0, the last record before allocation is the `initial_paths[C-1]` stage record (3686), which is emitted before the last initial path is built. A hard kill while the last initial path is built and a hard kill during chain 0's arrays therefore leave the same last record.
  - For chain c > 0, the last record is chain c-1's final sweep, which does locate the kill between chains.
  - RunV001 ended at memory after 2.69 s, so this is the case most worth disambiguating.
  - Fix: emit a record before the allocation, for example a `chain_alloc` event carrying the planned size `n_meas*(n_u*n_u + n_u + n_r)*8 + n_meas*8` bytes, or move `chain_start` before `np.zeros`. It draws no RNG and changes no transition.
- **N2. Non-`_Stop` exceptions still lose every prefix.**
  - The sampling `try` catches only `_Stop`. A Python `MemoryError` escapes the public function with no result, losing the completed chains' committed rows. One way this happens is an address-space limit making `np.zeros` or an operator enumeration fail in-process instead of the process being killed.
  - The hook takes no arguments, so it cannot foresee an allocation.
  - All chains' arrays stay live in `series`. The retained total is about `C * n_meas * (n_u^2 + n_u + n_r + 1) * 8` bytes, plus per-sample transients. The caller can compute this before launch and should keep it well under 900 MiB.
  - L26 records the overrun but says only that it "ends at root's hard cap with no returned result". The in-process `MemoryError` route is worth one sentence there or in root's runner notes. I did not assume which limit mechanism root uses.
- **N3. Status vocabulary.** The literal `INCOMPLETE_BUDGET` lives in `incomplete_reason`, `partial.stop.reason` and the message; `status` is `incomplete`. This is consistent with the four-status coding rule. Root should key on `incomplete_reason`.
- **N4. Cap stops now also return prefixes (`INCOMPLETE_CAP`).**
  - This is additive and labelled as diagnostics. Event caps are state-dependent: high-event paths reach them first. The "DIAGNOSTICS ONLY" label and the no-analysis rule apply equally.
  - The note text names only wall-time and memory stopping; adding "and caps" would be exact.
- **N5. `accepted_in_measurement` in a partial entry can include accepted moves of an unfinished measuring sweep** that has no row. It is a counter only and never affects a prefix.
- **N6. Per-sweep sink records.** There is one record per completed sweep. If root's sink flushes durably on every record, its cost scales with the sweep count and counts against the 150 s margin. The sink can throttle; nothing in the module needs to change.
- **N7. Hook and sink failures end the run `failed` with no prefixes.** This includes a `MemoryError` raised inside the hook. Root's hook should catch its own errors and return True. This is documented (L24, L25, DELTA limitations 3-4).
- **N8. Some failed exits send no `stop` record.** The `validate_owned_model` exception and not-ok paths (3560-3571), the member-check failure and the binding-stage failures return without a final sink record. The returned result carries the status, so this matters only for a hard kill, which these paths do not involve.
- **N9. Signature compatibility.** Callers written for v003 (23 kwargs) raise `TypeError` on v004 until they pass `budget_hook=` and `progress_sink=` explicitly. 0413 and the coding rules mandate this (required, no default), and v003 remains on disk unchanged.
- **N10. The prefixes are views.** `.base` is the zero-filled allocation, documented as must-not-read. Copying, `np.save` and pickling a view serialize only the view's rows.
- **N11. Carried items.**
  - REVIEW_0410_MODES_V001 N1-N11 and FINAL_CHECK R4-R7 are unchanged; this delta is budget-only.
  - `raw_to_whitened_sources`, `_measure`, `_analyze`, `_mode_outputs` and result assembly are unbracketed, as documented.
  - 0410 section 2 (the equal-time two-hop sector) is out of scope.

## LIMITATIONS of this review (recorded, not resolved)

- Everything above is static. Bit-identity of the RNG sequence and the transition law rests on AST identity plus a hand trace. No run confirmed it. It also assumes the caller's hook and sink never draw from `chain_generators` and never mutate inputs, which the module cannot verify.
- `owned_parent_operator_v003.py` (a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07) is on disk. I hashed it but did not read it, following the binding "v002 if present". Its compatibility is unverified.
- I did not read the optional `OWNED_WORLDLINE_COOPERATIVE_PARTIAL_RETURN_DELTA_V001.txt`. 0413 says it is not a requirement.
- I read the registration and companion JSON for hash only. The delta changes no registration semantics, so this review makes no claim about them beyond what REVIEW_0410_MODES_V001 recorded.
- The memory-mechanism remarks in N1 and N2 describe possible failure routes. They make no claim about how root enforces its 1 GiB limit.
