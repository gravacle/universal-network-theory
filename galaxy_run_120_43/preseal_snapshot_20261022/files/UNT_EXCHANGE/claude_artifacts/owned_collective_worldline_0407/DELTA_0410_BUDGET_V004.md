# DELTA 0410 BUDGET V004: owned collective worldline static response, v004

**Role.** Author of the 0413 cooperative budget / partial-return delta on the 0407 evaluator. Distinct review is still pending: 0413 asks a distinct reviewer to check commitment/counting, the unchanged random/transition law and the stop handling.

**What v004 is.** v004 is a byte copy of `owned_collective_worldline_static_response_v003.py` plus ONLY the 0413 addition. It changes no physics, estimator, move probability, warmup or measurement target, or chain schedule. It adds no checkpoint framework. The longer optional sink proposal `OWNED_WORLDLINE_COOPERATIVE_PARTIAL_RETURN_DELTA_V001.txt` was neither read nor implemented.

**Method (static only).**
- I wrote the module as text and did not import or execute it, any operator or the root adapter.
- I ran no numbers, did no sampling, used no network and installed nothing.
- The only code I ran was `shasum -a 256`, `diff -u`, and `python3 -I -B` (3.9.6) doing `ast.parse`, `compile` (no exec) and `symtable` on TEXT copies in my own scratch directory.
- There is no `__pycache__` in the 0407 directory.
- Both files were written by exclusive create (noclobber). Nothing was overwritten, moved, deleted or chmod-ed.
- I made no write under `Universal Network Theory` and opened no file with a forbidden name.

## Hashes (full sha256, computed from bytes)

| File | sha256 | Status |
|---|---|---|
| 0410 brief `FROM_CODEX/0410_2026-10-16_direct_mode_columns_and_equal_time_pair_completion.md` | ac1db8fa81c06672d495448b82835072978dee8bce0d3a017044de29cc440e34 | binding, matched |
| 0413 brief `FROM_CODEX/0413_2026-10-16_preserve_collective_measurements_on_bounded_exit.md` (read fully) | adfc9185663bb79880a85bc3bbd0194fa208df8aaf2404ca192499b3cddbf383 | binding, matched |
| base `owned_collective_worldline_static_response_v003.py` (copied) | e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721 | unchanged |
| evaluator `owned_collective_worldline_static_response_v002.py` | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 | unchanged |
| `FIX_DELTA_0407_V002.md` | 94c1518231d42b58418111f790611d3c5d635195e6fbc4d88c5c66e2757a7b41 | read (no stop-handling item) |
| `FINAL_CHECK_0407_V001.md` | 1e352a9eac3d672bf93da60ba4c00270eb1279269208e5052628b060e1d19042 | read |
| `REVIEW_0407_PALETTE_V001.md` | 251a6077291e44bc1f3a658abc138cfeacf16084684b7720c8561e1646d20c29 | read |
| `REVIEW_0410_MODES_V001.md` (review of v003: PASS_WITH_NOTES, no blocking item) | 19eb6c88d95142e5b2bf4b62777f90ae49aa3c2f7e1b663685e2d1e67713b269 | read |
| operator `owned_parent_operator_v002.py` (present, so used) | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e | matched, read as text (signatures) |
| root adapter `owned_diamond_registration_input_adapter_v001.py` | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 | binding, matched, read as text (signatures) |
| registration `OWNED_DIAMOND_CURRENT_GRAPH_COLLECTIVE_REGISTRATION_PROPOSED_V001.json` | f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 | binding, matched (semantics only) |
| companion `OWNED_DIAMOND_WHITENING_DUAL_SOURCE_MANDATORY_COMPANION_V001.json` | 9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7 | binding, matched (semantics only) |
| **NEW** `owned_collective_worldline_static_response_v004.py` (187151 B, 3860 lines) | 6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea | written by exclusive create |

`owned_parent_operator_v003.py` (a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07) is also on disk. Per the brief ("v002 if present") I hashed it but did not read it; see LIMITATIONS 13.

## Public signatures added

There is one public entry point, as before, and it keeps every v003 argument and meaning. v004 appends two REQUIRED keyword-only arguments with no defaults (v004 L3216-3243):

```
owned_collective_worldline_static_response(*, operator_api, graph0, model, registration,
    initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients,
    volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
    diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
    caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
    implicit_closure, budget_hook, progress_sink)
```

- `budget_hook`: `None`, or a caller callable with the exact contract `budget_hook() -> bool`. It takes no arguments. `True` requests a cooperative stop. `np.bool_` is accepted.
- `progress_sink`: `None`, or a caller callable with the exact contract `progress_sink(record=<dict>)`. Its return value is ignored.
- Both must be passed explicitly. With `budget_hook=None` and `progress_sink=None`, a v004 run is v003's run.

Additive result keys:
- top level: `incomplete_reason` and `partial`;
- `inputs`: `budget_hook` and `progress_sink`;
- `diagnostics.counters`: `budget_checks`;
- per-chain diagnostics: `burn_in_sweeps_completed`;
- `conventions`: `budget`.

No existing key changed meaning. The tuple coordinate interface and the v003 mode-direction interface are untouched.

## Change map (v004 line numbers)

| Where | v004 lines | Change |
|---|---|---|
| Module docstring | 3-8, 72-74, 84-114, 194-207, 268-273 | version header; 0413 binding source; signature; BUDGET paragraph (hook contract, checkpoints, root's 150 s / 900 MiB policy lives in the hook, overrun); WHERE 0413 IS IMPLEMENTED; COST addendum |
| `LIMITATIONS` | 394-395 (L14 addendum), 490-554 (L24, L25, L26) | cap stops return prefixes; budget stop / partial return; progress sink; numbers and overrun |
| `class _BudgetStop(_Stop)` | 568-581 | NEW. Status `"incomplete"`; carries `checkpoint`. It is a `_Stop` subclass, so every existing `except _Stop` path handles it. |
| `_admit_optional_callable` | 681-689 | NEW. A callable or explicit `None`; anything else fails at input admission. |
| `_budget_check` | 1545-1568 | NEW. Calls the hook. A raise or non-bool return gives `failed`; `True` raises `_BudgetStop`; it counts `budget_checks`. It draws no random number and receives no state. |
| `_progress` | 1571-1594 | NEW. Builds a fresh small record and calls the sink synchronously; a sink raise gives `failed`. |
| `_op` | 1597-1614 | Checks the hook before and after every operator call (canonical_state_key, primitive_channels, palette_channels, diagonal_terms, read_rows). The checks sit OUTSIDE the try, so a budget stop is never converted into an operator failure. |
| `_reads_at` | 2046, 2058, 2065, 2074 | Checks before and after `adapted_moment_reads` and `pair_source_hamiltonian`, outside their try blocks. |
| `_ctmc_segment` | 2326 | Check at the top of every jump iteration, before `rng.exponential`. |
| `_palette_move` | 2520, 2542 | Check at the top of every member-CTMC jump iteration (before `rng.exponential`) and before every held-mark replay. |
| `_partial_prefixes` | 3070-3120 | NEW. Per registered chain it returns rows `[:measurements_committed]` of score/contact/reads/events (views), with targets, `coordinate_order_all`, `tracked_read_labels`, the zero-rate directions seen so far, `beta`, and the stop record (reason, stage, checkpoint, message, `proposal_in_progress`, `resumable` False), labelled DIAGNOSTICS ONLY. |
| `_new_result` | 3127-3128, 3194-3201 | `incomplete_reason: None`, `partial: None`; `conventions["budget"]`. |
| Public signature / docstring | 3241-3242, 3316-3330 | the two new arguments and their contract; new return keys |
| Input admission / echo | 3403-3404, 3442-3443 | the hook and sink are admitted and echoed |
| `run` dict | 3501, 3504-3508 | `budget_checks` counter; hook, sink, targets; `move_open` |
| `series`, `_stopped` | 3511, 3520-3547 | `series` is created before any stop can occur. `_stopped` handles every internal stop: it sets status/stage/failures/diagnostics as in v003; when status is `incomplete` it also sets `incomplete_reason` (BUDGET vs CAP), `partial` and a flag; it then emits a guarded final `stop` record. |
| Model / member / binding stages | 3551-3555, 3573-3577, 3602-3605 | progress records; hook before and after `validate_owned_model`. The after-check comes after the validation verdict, so a validation failure takes precedence. |
| Initial paths | 3686 | one progress record per chain's initial path |
| Sampling loop | 3714, 3717-3735, 3743-3752, 3764-3770 | `burn_in_sweeps_completed`; hook before the chain's array allocation; chain arrays registered in `series` BEFORE the first sweep; `chain_start` record. Sweep start: the unchanged `max_sweeps` cap check, then the stage, the hook, then the sweep counter. Hook between moves; `move_open` around `_move`. Committed count incremented only after all four writes; `sweep` record after every completed sweep. |
| Stop handler | 3771-3772 | `except _Stop: return _stopped(stop)` replaces the inline v003 handler, which DISCARDED the populated arrays. |
| Pre-analysis | 3775-3791 | `analysis` record; hook before the analysis; internal guard that every chain committed exactly `measurement_sweeps` rows before `_analyze` (zero padding is never analysed). |

AST def-level comparison (text): 5 defs added, 0 removed, 7 changed (`LIMITATIONS`, `_ctmc_segment`, `_new_result`, `_op`, `_palette_move`, `_reads_at`, the public function), 87 byte-identical in AST.

## Requirement trace (0413)

| 0413 item | Implementation (v004 lines) | Status |
|---|---|---|
| 1. Register per-chain arrays immediately; valid counts; count only after the whole tuple is committed; on a stop return only valid prefixes, never zero padding or burn-in | Registration 3725-3734 (before sweep 0; v003 appended after all sweeps and discarded the arrays on `_Stop`). Commit 3760-3765: score, contact, reads and events are written, and only then is `measurements_committed` incremented (no hook, sink or operator call lies in between). Burn-in is never stored (3766-3767 counts only). Prefixes are `[:n]` slices (3079-3091). The analysis guard is at 3782-3791. | MET |
| 2. Caller cooperative hook as a required kwarg (callable or explicit None), checked before and after costly calls and between jumps and sweeps; INCOMPLETE_BUDGET distinct from validation failure; no RNG; unfinished proposal not turned into a rejection or measured state; no implicit resumability | Argument at 3241, admission at 3403. Check sites: `_op` 1604/1613; validate 3553/3574; adapter 2046/2058/2065/2074; jumps 2326/2520; held replay 2542; chain arrays 3718; sweeps 3744; moves 3749; analysis 3779. `_BudgetStop` (568-581) gives status `incomplete` with `incomplete_reason` `INCOMPLETE_BUDGET` (3535); validation failures stay `failed`/`unsupported` with `incomplete_reason` None. A hook contract failure is `failed` (1553-1566). No check touches `rng`. A stop inside `_move` propagates as an exception, so `path, accepted` is never assigned, no accept/reject counter moves and no measurement is taken; `proposal_in_progress` records the case (3532, 3108). `resumable: False`, and no RNG state or path is returned. | MET |
| 3. Root uses a 150 s cooperative wall margin under the 180 s cap and 900 MiB under 1 GiB; the hook is the caller's, so no numbers are hard-coded; an indivisible enumeration can overrun (limitation) | Docstring BUDGET 99-114 and L26 543-554. AST: no `time`, `resource`, `tracemalloc`, `os` or `sys` names, and no numeric budget constant. | MET (documented) |
| 4. Small flushed stage/chain/completed-warmup/completed-measurement/move-counter diagnostics through a caller sink; no file I/O; no per-sample journal | `_progress` 1571-1594. Records at the model 3552, member_check 3575, binding 3603 and initial_paths 3686 stages; chain_start 3735; every completed sweep 3769; analysis 3778; stop 3544. Record keys: L25. The module does no I/O; flushing is the sink's. | MET (flush delegated) |
| 5. On budget exhaustion return partial prefixes, metadata and explicit status with ok False; skip expensive mixing analysis; label prefixes as diagnostics; completed runs keep the original analysis and thresholds | `_stopped` 3520-3547 returns before `_analyze`; `ok` stays False (`_new_result`); `estimates`/`errors`/`mixing` stay None. `partial["status"] = "diagnostic_prefixes"` plus the note (3112-3118), and a flag (3538-3542). `_analyze`, `_estimate`, `_sokal_tau`, `_rhat`, `_mode_outputs` and the post-analysis assembly are AST-identical to v003. | MET |
| With the hook never firing, the RNG sequence and transition law are bit-identical to the base | `_move`, `_select_interval`, `_interval_move`, `_rotate`, `_initial_path`, `_choose_channel`, `_choose_palette`, `_channels_from_records`, `_segment_core`, `_event_from_channel` and `_measure` are AST-identical. With every `_budget_check(...)` statement stripped, `_ctmc_segment`, `_palette_move` and `_reads_at` are AST-identical to v003. `_op` returns the same value. In the main loop, the only reordering is the `run["stage"]` string assignment before the sweep counter increment; neither affects a draw or a rate. | MET (static argument; not executed) |

## Assumed operator / adapter API (exact names; unchanged from v003)

v004 adds no operator or adapter call. It only brackets the existing calls with hook checks.

| Called as | Actual definition (read as text) |
|---|---|
| `validate_owned_model(*, graph0, model, registration)` | operator v002 L979 |
| `canonical_state_key(*, context, state)` | operator v002 L1772 |
| `diagonal_terms(*, context, state)` | operator v002 L1789 |
| `primitive_channels(*, context, state)` | operator v002 L1801 |
| `palette_channels(*, context, state, palette_owners)` (only when `palette_parameters` is not None) | operator v002 L1837 |
| `read_rows(*, context, state)` | operator v002 L1861 |
| `operator_module.state_labels` (called by the adapter, not here) | operator v002 L1783 |
| `adapted_moment_reads(*, operator_module, context, state, binding)` | adapter v001 L177 |
| `pair_source_hamiltonian(*, reads, j_R, j_S)` | adapter v001 L235 |
| `raw_to_whitened_sources(*, j_R_raw, j_S_raw)` (source_frame "raw", once, not bracketed) | adapter v001 L254 |

New caller-supplied contracts (v004):
- `budget_hook() -> bool`;
- `progress_sink(record=dict)`. Record keys: `module`, `event` (`stage` | `chain_start` | `sweep` | `stop`), `stage`, `chain`, `burn_in_sweeps_completed`, `burn_in_sweeps_target`, `measurements_committed`, `measurement_sweeps_target`, `move_counters`, `counters`, `stop`.

## AST results (text copy of the final v004 bytes, `python3 -I -B`, 3.9.6)

- `ast.parse` and `compile` (no exec): OK.
- Imports: `bisect`, `math`, `collections.abc.Mapping`, `numpy`. Nothing else.
- No `MatMult` (binary or augmented). No `dot`, `matmul`, `vdot`, `inner`, `tensordot`, `outer`, `kron` or `linalg` name or attribute.
- 10 `einsum` calls, all with `optimize=False`. All 10 are unchanged from v003.
- No call to `print`, `open`, `eval`, `exec`, `compile`, `__import__`, `input`, `globals`, `locals`, `vars`, `breakpoint`, `exit` or `quit`.
- No `os`, `sys`, `subprocess`, `threading`, `socket`, `pickle`, `ctypes`, `io`, `pathlib`, `shutil`, `multiprocessing`, `asyncio`, `time`, `random`, `resource`, `tracemalloc`, `signal` or `scipy` name.
- No numpy save/load/tofile attribute.
- No decorator, no global/nonlocal, no async/yield.
- Module level holds only the docstring, 4 imports, the `LIMITATIONS` string constant, `class _Stop(Exception)`, `class _BudgetStop(_Stop)` and 96 defs. Nothing runs at import.
- `symtable`: no undefined globals.
- Public callables: exactly one, `owned_collective_worldline_static_response` (L3216), with 0 positional parameters, no `*args` or `**kwargs`, 25 keyword-only parameters (the 23 of v003 plus `budget_hook` and `progress_sink`) and no defaults.

## LIMITATIONS (recorded, not resolved by inventing physics)

1. **Status vocabulary.** 0413 names `INCOMPLETE_BUDGET`; the coding rules restrict `status` to complete/incomplete/unsupported/failed. v004 therefore returns `status "incomplete"` with `incomplete_reason "INCOMPLETE_BUDGET"`. Cap stops use `"INCOMPLETE_CAP"`, and validation failures keep `failed`/`unsupported` with `incomplete_reason` None. If root wants the literal status string instead, that is a separate decision.
2. **Cap stops also return prefixes.** I read 0413 item 1 ("bounded exit") as covering every `incomplete` stop, so caps return prefixes as well. `failed` and `unsupported` stops return no prefixes, because a later validation failure can invalidate earlier samples; their counts remain in `diagnostics`.
3. **Hook contract.** The hook takes zero arguments and returns a bool. A hook that raises (including a MemoryError raised inside the hook) or returns a non-bool ends the run `failed`, not `INCOMPLETE_BUDGET`, and returns no prefixes. Root's hook should catch its own errors and return True.
4. **Sink failure is fail-closed.** A sink exception during the run gives `failed` and no prefixes. At the final stop record the stop status is kept and a failure line is appended. Root's sink should handle its own I/O errors. The module cannot flush: durability is the sink's job.
5. **Overrun (0413 item 3).** The hook is polled only between calls. The following are indivisible and can exceed root's reserve (about 30 s / 124 MiB):
   - one operator enumeration or other operator call;
   - `validate_owned_model`;
   - one adapter read;
   - one `_measure`;
   - a chain's array allocation (`measurement_sweeps * (n_u^2 + n_u + n_r + 1)` numbers, allocated at chain start as in v003);
   - the whole `_analyze` after the last pre-analysis check;
   - result assembly or serialization by the caller.

   Such an overrun ends at the hard cap with no result; only the sink records locate the stage. Memory growth inside a call is not observable here.
6. **Prefix statistics.** Wall-time and memory stopping can depend on the states reached, and chains run sequentially (scheduling unchanged). A stop therefore leaves early chains complete, one chain partial and later chains absent. The prefixes are diagnostics only: not unbiased estimates, not an accepted uncertainty, and not a balanced multi-chain sample. No R-hat, autocorrelation or jackknife is computed on them.
7. **No resumability.** The RNG states and the last paths are not returned. Draws consumed by an abandoned proposal are lost. Started-proposal counters (e.g. `interval_proposals`, `events`, `channel_enumerations`) can include the abandoned proposal; `partial.stop.proposal_in_progress` flags this.
8. **Views, not copies.** The prefix arrays are views, chosen to avoid allocation at a memory-bound stop. Their `.base` is the unfilled allocation, which callers must not read. A caller who needs independent arrays copies them.
9. **Hook cost.** There are about two hook calls per operator or adapter call, plus one per jump, held replay, move and sweep. The total cost scales with the caller hook's own cost; the hook's implementation is root's.
10. **Unbracketed calls.** `raw_to_whitened_sources` (once per run at binding) is not bracketed. `_measure`, `_mode_outputs` and `_analyze` have no internal checks: `_analyze` is unchanged by design.
11. **Bit-identity is argued statically, not measured.** The evidence is the AST identity of the move, estimator and analysis defs, plus the strip comparison of `_ctmc_segment`, `_palette_move` and `_reads_at`. It assumes the caller's hook and sink do not draw from `chain_generators` and do not mutate inputs; the module cannot verify that.
12. **v003 notes carried, not addressed.** REVIEW_0410_MODES_V001 notes N1-N11 (N1 input form, N2 Mandel factor, N3 Gram flag, and so on) and FINAL_CHECK R4-R7 remain as they were; this delta is budget-only. The v003 `implicit_closure` message text ("v003 implements ...") was left unchanged as non-budget text.
13. **Operator version.** API statements are for operator v002 (as directed) and v001 (unchanged). `owned_parent_operator_v003.py` exists on disk but was not read, and its compatibility is unverified.
14. **No completion record.** The sink receives no "complete" record: a completed run returns its result directly. The last record of a completed run is the `analysis` stage record.
15. **Out of scope.** 0410 section 2 (the equal-time two-hop sector) is not part of this delta.

## diff -u v003 -> v004

```diff
--- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_collective_worldline_0407/owned_collective_worldline_static_response_v003.py	2026-10-16 04:51:07.320826526 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_collective_worldline_0407/owned_collective_worldline_static_response_v004.py	2026-10-16 05:16:43.233434939 -0500
@@ -1,6 +1,13 @@
 """Owned collective static response by positive imaginary-time worldlines.
 
-UNT task 0407, version v003: v002 (sha256
+UNT task 0407, version v004: v003 (sha256
+e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721, preserved unchanged) plus ONLY
+the 0413 cooperative budget / partial-return delta (budget_hook, progress_sink, committed
+measurement prefixes; L24-L26). No physics, estimator, move probability, warmup/measurement
+target or chain schedule is changed; with budget_hook None or never returning True the RNG
+draw sequence and the transition law are those of v003.
+
+v003 header (unchanged): version v003: v002 (sha256
 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941, preserved unchanged) plus the
 0410 section 1 direct real-mode derivative columns, the FINAL_CHECK R1 operator v002 palette
 call and the R3 coarse-row wording. v002 was the fix of v001 (sha256
@@ -62,6 +69,9 @@
   * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v002.py
     b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e   (ACTUAL operator v002
     API, read as text; its palette_channels is the palette enumeration called here)
+v004 addition (sha256 from bytes before writing; read-only; values never taken from it):
+  * UNT_EXCHANGE/FROM_CODEX/0413_2026-10-16_preserve_collective_measurements_on_bounded_exit.md
+    adfc9185663bb79880a85bc3bbd0194fa208df8aaf2404ca192499b3cddbf383   (items 1-5)
 Style reference (read as text): claude_artifacts/scalar_metric_solve_0397/
 scalar_metric_particular_solve_v002.py (fail-closed result dict).
 
@@ -71,13 +81,37 @@
       volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
       diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
       caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
-      implicit_closure)
-The v002 signature is unchanged (no public argument is added in v003): the 0410 mode
+      implicit_closure, budget_hook, progress_sink)
+The v002 signature is unchanged in v003 (no public argument is added in v003): the 0410 mode
 columns enter as fixed affine direction mappings inside derivative_coordinates (MODE SPEC
-s1 "minimal API delta"; L21), next to the unchanged tuple coordinate interface.
+s1 "minimal API delta"; L21), next to the unchanged tuple coordinate interface. v004 adds
+exactly two REQUIRED keyword-only arguments without defaults, budget_hook and progress_sink
+(each a callable or an explicitly passed None; 0413 items 2 and 4; L24, L25); every other
+argument keeps its v003 meaning.
 It returns a plain fail-closed dict with "ok", "status" (complete | incomplete |
 unsupported | failed), "stage_reached" and "failures". When ok is False every populated
-field is evidence only, never a result.
+field is evidence only, never a result. v004: "incomplete_reason" is None unless status is
+"incomplete"; then it is "INCOMPLETE_BUDGET" (budget_hook requested a cooperative stop) or
+"INCOMPLETE_CAP" (a caps entry was reached), never a validation failure (status "failed" /
+"unsupported", incomplete_reason None). On an incomplete stop "partial" holds the committed
+measurement prefixes as diagnostics (L24).
+
+BUDGET (0413; L24-L26). budget_hook() is a caller callable taking no arguments and returning
+a bool, True meaning "stop now". It is called before and after every operator call (through
+_op, plus validate_owned_model) and every adapter read (adapted_moment_reads,
+pair_source_hamiltonian), between proposal jumps of the global and palette regrowths, before
+every held-mark replay, between moves, at every sweep start, before each chain's arrays are
+allocated and before the analysis. A True return raises the internal budget stop: the
+unfinished proposal is abandoned (never counted as an acceptance, a rejection or a
+measurement), no random draw is made, and the run returns status "incomplete" with
+incomplete_reason "INCOMPLETE_BUDGET", ok False, the committed prefixes and NO mixing or
+error analysis. progress_sink(record=dict) receives small synchronous stage / chain /
+completed-warmup / completed-measurement / move-counter records (L25); the module does no
+file I/O, flushing is the sink's. Root's planned policy (0413 item 3) is a 150 s cooperative
+wall margin under its 180 s external hard cap and a 900 MiB cooperative memory threshold
+under 1 GiB, implemented INSIDE the caller's hook; no time, memory or threshold value is
+read or hard-coded here. One indivisible operator enumeration (or adapter read, measurement,
+array allocation or analysis step) can still overrun that reserve (L26).
 
 OPERATOR API: the ACTUAL owned_parent_operator_v001.py / owned_parent_operator_v002.py API
 (state level, basis free; the operator module is NOT imported here). The caller passes
@@ -157,6 +191,20 @@
     _reads_at cell sums); no division by any mode norm.
   MODE SPEC s3-s5 (Legendre, J, contact, metric/EH pairing, block admissibility) are the
     root metric adapter's and are NOT implemented here.
+WHERE 0413 IS IMPLEMENTED (v004, L24-L26)
+  Item 1 (per-chain arrays registered at chain start, committed counts, valid prefixes):
+    sampling loop of the public function (series entry appended before the first sweep;
+    "measurements_committed" incremented only after score, contact, reads and events of
+    the sample are all written), _partial_prefixes (rows [:committed] only).
+  Item 2 (cooperative hook, INCOMPLETE_BUDGET, no RNG, unfinished proposal discarded):
+    _BudgetStop, _budget_check, _op, _reads_at, _ctmc_segment, _palette_move, the
+    sampling loop and the pre-sampling / pre-analysis checkpoints; _stopped (local to the
+    public function) sets incomplete_reason.
+  Item 3 (root's 150 s / 900 MiB policy lives in the caller's hook; overrun limitation):
+    BUDGET paragraph above, L26.
+  Item 4 (progress sink): _progress (stage, chain_start, sweep and stop records).
+  Item 5 (partial return, ok False, no mixing analysis after a stop): _stopped,
+    _partial_prefixes; the completed path through _analyze is unchanged.
 
 SEMANTICS. In the positive gauge G = (-1)^{sum_v q_v} (-e^{i phi_adm})^{N_S}
 (-e^{i phi_birth})^{N} (assembly lines 300-327, e^{-i theta} epsilon = -|epsilon| written
@@ -217,7 +265,12 @@
 lapse projections and O(cells * fields) per source direction plus O(9 * cells) for the
 uniform moments; per event O(nonzero weights * lapse directions). n_u counts directions
 (e.g. 20 for one joint cosine/sine block), never cells times fields, so per-sample storage
-is O(n_u^2 + n_r) whatever the cell count.
+is O(n_u^2 + n_r) whatever the cell count. v004: each budget check is O(1) module work plus
+the caller hook's own cost, about two checks per operator or adapter call plus one per
+proposal jump, held replay, move and sweep; progress records are O(1) in size (two small
+counter dicts), one per stage, chain start, completed sweep and stop. Per-chain arrays
+(measurement_sweeps * (n_u^2 + n_u + n_r + 1) numbers) are allocated once at chain start,
+as in v003; a stop returns views of their committed rows (no copy).
 
 LIMITATIONS: see the module-level string LIMITATIONS.
 """
@@ -338,6 +391,8 @@
     computation with status incomplete and partial diagnostics; no estimate is returned
     and no path is ever rejected because of a cap. Restricted, lazy and verification
     enumerations count as channel enumerations; replayed held marks count as events.
+    v004: a cap stop has incomplete_reason "INCOMPLETE_CAP" and returns the committed
+    measurement prefixes in "partial" exactly as a budget stop does (L24).
 L15. An exact floating-point coincidence of event times (zero holding time, rotation
     origin or interval end equal to an event time, or rounding to beta) ends the
     computation as failed rather than perturbing times.
@@ -432,6 +487,71 @@
     the callback they are absent (result modes "uniform_moments" is None). These two label
     kinds are reserved: a caller tracked label or an operator read label of either kind
     fails.
+L24. Cooperative budget stop and partial return (v004; 0413 items 1, 2, 5). budget_hook is
+    None (never called) or a caller callable called with NO arguments; it must return a
+    bool (Python or numpy), True requesting a stop. A hook that raises or returns anything
+    else ends the run "failed" (hook contract failure, not a budget stop). Checkpoints:
+    before and after every _op operator call and validate_owned_model, before and after
+    adapted_moment_reads and pair_source_hamiltonian, at the top of every jump iteration of
+    _ctmc_segment and of the palette member CTMC, before every held-mark replay, at every
+    sweep start (after the unchanged max_sweeps cap check, before the sweep counter), between
+    moves of a sweep, before each chain's array allocation and before the analysis. The
+    once-per-run raw_to_whitened_sources conversion is not bracketed. The check draws no
+    random number, receives no Generator, state or path, and changes no counter except
+    counters["budget_checks"]. A True return raises the internal _BudgetStop (status
+    "incomplete", incomplete_reason "INCOMPLETE_BUDGET", ok False): the unfinished proposal,
+    initial path or analysis is abandoned; it is NOT counted as an acceptance or a
+    rejection, the chain's path is not replaced and no measurement is taken. Counters the
+    started proposal had already advanced (e.g. interval_proposals, events,
+    channel_enumerations) stay as they are; partial["stop"]["proposal_in_progress"] marks
+    that case. The random draws already consumed by the abandoned proposal are lost: the
+    RNG states and paths are not returned and NO resumability is claimed or implied.
+    "partial" (status "incomplete" only, budget or cap): one entry per chain whose arrays
+    were registered (chains not yet started are absent) with the first
+    measurements_committed rows of score [n, n_u], contact [n, n_u, n_u], reads [n, n_r]
+    and events [n]; a row counts only after all four parts of its sample are written.
+    Burn-in sweeps are never stored (a chain stopped in burn-in has 0 rows) and rows beyond
+    the committed count are never exposed by the returned shapes (no zero padding). The
+    arrays are views of the per-chain allocations (no copy at a possibly memory-bound
+    stop); their .base is the unfilled allocation and must not be read. Columns follow
+    partial["coordinate_order_all"] (EVERY declared coordinate, before the zero-rate
+    filter; directions listed in partial["zero_rate_directions_seen"] are unsupported and
+    must be discarded) and partial["tracked_read_labels"]. Wall-time and memory stopping
+    can depend on the states reached (slow, high-event stretches are more likely to be
+    cut), so the prefixes are DIAGNOSTICS: not unbiased estimates, not an accepted
+    uncertainty, and a full-length prefix of a stopped run is not a completed run. After
+    any stop no _analyze, mixing, error or mode-output step runs; estimates, errors, mixing,
+    direction_status and coordinate_order stay None. A "failed" or "unsupported" stop
+    returns no prefixes (a later validation failure can invalidate earlier samples); the
+    per-chain counts stay in diagnostics. When the hook never returns True the run, its
+    RNG draws, its transition law, _analyze and every threshold are exactly v003's.
+L25. Progress sink (v004; 0413 item 4). progress_sink is None or a caller callable called
+    synchronously as progress_sink(record=<dict>); its return value is ignored. Records are
+    fresh dicts with keys "module", "event" ("stage" | "chain_start" | "sweep" | "stop"),
+    "stage", "chain" (None outside a chain), "burn_in_sweeps_completed",
+    "burn_in_sweeps_target", "measurements_committed", "measurement_sweeps_target",
+    "move_counters" (copy of the chain's diagnostic counters, or None), "counters" (copy of
+    the run counters) and "stop" (None, or reason / checkpoint / message on the stop record).
+    Emitted at the model, member_check, binding, initial_paths[c] and analysis stages, at
+    each chain start, after every completed sweep (its measurement already committed) and
+    once at a stop. A hard kill during a sweep therefore leaves the last completed sweep as
+    the last record. The module does no file I/O and cannot flush: writing and flushing
+    each record durably is the sink's job. No per-sample journal is kept. A sink exception
+    ends the run "failed"; an exception at the final stop record is appended to failures
+    and the stop status is kept. Neither hook nor sink may draw from chain_generators or
+    mutate any input (caller responsibility; not verifiable here).
+L26. Budget numbers and overrun (v004; 0413 item 3). Root's documented policy is a 150 s
+    cooperative wall margin under its 180 s external hard cap and a 900 MiB cooperative
+    memory threshold under 1 GiB, both evaluated INSIDE the caller's budget_hook; this
+    module reads no clock or memory and hard-codes no number. The hook is polled only
+    between calls, so one indivisible step can overrun the remaining reserve (about 30 s
+    and 124 MiB): an operator enumeration (primitive_channels / palette_channels on a large
+    state), read_rows, diagonal_terms, canonical_state_key, validate_owned_model, one
+    adapter read, one _measure, a chain's array allocation, the whole _analyze after the
+    last pre-analysis check, or result assembly. Such an overrun ends at root's hard cap
+    with no returned result; only the sink records then identify the reached stage.
+    Memory growth inside one call is not observable here. Earlier root failure evidence
+    (runs V001 and V002) is neither touched nor reinterpreted.
 """
 
 
@@ -445,6 +565,22 @@
         self.message = message
 
 
+class _BudgetStop(_Stop):
+    """v004 cooperative caller budget stop (0413 item 2): incomplete, INCOMPLETE_BUDGET."""
+
+    def __init__(self, stage, checkpoint):
+        _Stop.__init__(
+            self,
+            "incomplete",
+            stage,
+            f"INCOMPLETE_BUDGET: budget_hook requested a cooperative stop at checkpoint "
+            f"'{checkpoint}'; any unfinished proposal was abandoned (neither accepted, rejected "
+            "nor measured); only committed measurement prefixes are returned, as diagnostics; "
+            "no resumability (L24)",
+        )
+        self.checkpoint = checkpoint
+
+
 # ----------------------------------------------------------------------------------
 # Scalar and record admission helpers
 # ----------------------------------------------------------------------------------
@@ -542,6 +678,17 @@
     return not missing and not extra
 
 
+def _admit_optional_callable(name, value, failures):
+    """v004 budget_hook / progress_sink: a callable or an explicitly passed None (L24, L25)."""
+    if value is not None and not callable(value):
+        failures.append(
+            f"input {name}: {type(value).__name__} is neither a callable nor None (pass None "
+            "explicitly to disable it)"
+        )
+        return False
+    return True
+
+
 def _admit_operator_api(operator_api, need_restricted, failures):
     names = [
         "validate_owned_model",
@@ -1395,17 +1542,76 @@
 # ----------------------------------------------------------------------------------
 
 
+def _budget_check(run, phase, what):
+    """v004 cooperative budget checkpoint (0413 item 2; L24): no RNG, no state, no path."""
+    hook = run["budget_hook"]
+    if hook is None:
+        return
+    run["counters"]["budget_checks"] += 1
+    try:
+        stop = hook()
+    except Exception as exc:
+        raise _Stop(
+            "failed",
+            run["stage"],
+            f"budget_hook raised {type(exc).__name__}: {exc} at checkpoint '{phase} {what}' "
+            "(hook contract failure, not a budget stop; L24)",
+        )
+    if not isinstance(stop, (bool, np.bool_)):
+        raise _Stop(
+            "failed",
+            run["stage"],
+            f"budget_hook returned {type(stop).__name__}, not a bool, at checkpoint "
+            f"'{phase} {what}' (hook contract failure, not a budget stop; L24)",
+        )
+    if bool(stop):
+        raise _BudgetStop(run["stage"], f"{phase} {what}")
+
+
+def _progress(run, event, stage, diag, stop):
+    """v004 small synchronous progress record to the caller sink (0413 item 4; L25)."""
+    sink = run["progress_sink"]
+    if sink is None:
+        return
+    record = {
+        "module": "owned_collective_worldline_static_response_v004",
+        "event": event,
+        "stage": stage,
+        "chain": None if diag is None else diag["chain"],
+        "burn_in_sweeps_completed": None if diag is None else diag["burn_in_sweeps_completed"],
+        "burn_in_sweeps_target": run["burn_in_sweeps"],
+        "measurements_committed": None if diag is None else diag["measurements"],
+        "measurement_sweeps_target": run["measurement_sweeps"],
+        "move_counters": None if diag is None else dict(diag),
+        "counters": dict(run["counters"]),
+        "stop": stop,
+    }
+    try:
+        sink(record=record)
+    except Exception as exc:
+        raise _Stop(
+            "failed", stage, f"progress_sink raised {type(exc).__name__}: {exc} (L25)"
+        )
+
+
 def _op(run, name, **kwargs):
-    """Call an operator API function; any exception is a failed computation."""
+    """Call an operator API function; any exception is a failed computation.
+
+    v004: the caller budget hook is checked before and after the call (L24); the call
+    itself is indivisible (L26).
+    """
     fn = run["api"][name]
+    _budget_check(run, "before", name)
     try:
-        return fn(**kwargs)
+        out = fn(**kwargs)
     except _Stop:
         raise
     except Exception as exc:  # fail closed on operator errors (L17)
         raise _Stop(
             "failed", run["stage"], f"operator {name} raised {type(exc).__name__}: {exc}"
         )
+    _budget_check(run, "after", name)
+    return out
 
 
 def _state_key(run, state):
@@ -1837,6 +2043,7 @@
     pair_da = {}
     if pair is not None:
         fns = pair["fns"]
+        _budget_check(run, "before", "adapted_moment_reads")  # v004 (L24), outside the try
         try:
             reads = fns["adapted_moment_reads"](
                 operator_module=pair["operator_module"],
@@ -1848,12 +2055,14 @@
             raise _Stop(
                 "failed", run["stage"], f"adapted_moment_reads raised {type(exc).__name__}: {exc}"
             )
+        _budget_check(run, "after", "adapted_moment_reads")
         cells, r_w, s_w = _whitened_moments(run, reads)
         for lbl in run["needed_whitened"]:
             if lbl[0] == "whitened_R":
                 values[lbl] = r_w[lbl[1]][int(lbl[2])]
             else:
                 values[lbl] = s_w[lbl[1]][int(lbl[2])][int(lbl[3])]
+        _budget_check(run, "before", "pair_source_hamiltonian")  # v004 (L24), outside the try
         try:
             raw_p = fns["pair_source_hamiltonian"](reads=reads, j_R=pair["j_R"], j_S=pair["j_S"])
         except Exception as exc:
@@ -1862,6 +2071,7 @@
                 run["stage"],
                 f"pair_source_hamiltonian raised {type(exc).__name__}: {exc}",
             )
+        _budget_check(run, "after", "pair_source_hamiltonian")
         pv = _real_value(raw_p)
         if pv is None:
             raise _Stop("failed", run["stage"], "pair_source_hamiltonian value not finite real")
@@ -2113,6 +2323,7 @@
     caps = run["caps"]
     counters = run["counters"]
     while exit_rate > 0.0:
+        _budget_check(run, "between", "proposal jumps")  # v004 (L24): no RNG draw
         dt = float(rng.exponential(1.0 / exit_rate))
         t_next = t + dt
         if t_next >= length:
@@ -2306,6 +2517,7 @@
     log_held = 0.0
     for bound, hev in held + [(length, None)]:
         while r_s > 0.0:
+            _budget_check(run, "between", "palette proposal jumps")  # v004 (L24): no RNG draw
             dt = float(rng.exponential(1.0 / r_s))
             t_next = t + dt
             if t_next >= bound:
@@ -2327,6 +2539,7 @@
             current, channels, r_s, t = y_seg, y_channels, y_rs, t_next
         if hev is None:
             break
+        _budget_check(run, "before", "held-mark replay")  # v004 (L24): no RNG draw
         groups = _record_groups(run, hev["kind"], hev["owner"])
         x_channels, _ = _palette_channels(run, current["state"], groups)
         matches = [
@@ -2854,10 +3067,65 @@
     return out, uni
 
 
+def _partial_prefixes(run, series, chain_diag, n_chains, stop):
+    """v004 committed measurement prefixes on an incomplete stop (0413 items 1, 5; L24).
+
+    Only rows [:measurements_committed] are exposed (views, no copy); burn-in is never
+    stored; nothing here is analysed, averaged or treated as an estimate.
+    """
+    budget = isinstance(stop, _BudgetStop)
+    chains = []
+    for entry in series:
+        n = entry["measurements_committed"]
+        diag = chain_diag[entry["chain"]]
+        chains.append({
+            "chain": entry["chain"],
+            "measurements_committed": n,
+            "burn_in_sweeps_completed": diag["burn_in_sweeps_completed"],
+            "sweeps_completed": diag["sweeps_completed"],
+            "accepted_in_measurement": diag["accepted_in_measurement"],
+            "score": entry["score"][:n],
+            "contact": entry["contact"][:n],
+            "reads": entry["reads"][:n],
+            "events": entry["events"][:n],
+        })
+    return {
+        "status": "diagnostic_prefixes",
+        "chains": chains,
+        "chains_registered": len(series),
+        "chains_total": n_chains,
+        "burn_in_sweeps_target": run["burn_in_sweeps"],
+        "measurement_sweeps_target": run["measurement_sweeps"],
+        "coordinate_order_all": list(run["coords"]),
+        "tracked_read_labels": list(run["tracked_all"]),
+        "zero_rate_directions_seen": sorted(map(repr, run["zero_rate_directions"])),
+        "beta": run["beta"],
+        "stop": {
+            "reason": "INCOMPLETE_BUDGET" if budget else "INCOMPLETE_CAP",
+            "stage": stop.stage,
+            "checkpoint": stop.checkpoint if budget else None,
+            "message": stop.message,
+            "proposal_in_progress": bool(run["move_open"]),
+            "resumable": False,
+        },
+        "note": (
+            "DIAGNOSTICS ONLY: committed measurement prefixes of a stopped run (rows counted "
+            "only after the whole sample tuple was written; burn-in never stored; no zero "
+            "padding). Wall-time/memory stopping can depend on the states reached, so these "
+            "are not unbiased estimates and carry no accepted uncertainty; no mixing, error or "
+            "mode analysis was run; columns follow coordinate_order_all (zero-rate directions "
+            "must be discarded) and tracked_read_labels; arrays are views of the per-chain "
+            "allocations; no resumability (L24)"
+        ),
+    }
+
+
 def _new_result():
     return {
         "ok": False,
         "status": None,
+        "incomplete_reason": None,
+        "partial": None,
         "stage_reached": None,
         "failures": [],
         "flags": [],
@@ -2923,6 +3191,14 @@
                 "joint block, no phase averaging; normalization, Gram duals, Legendre and "
                 "metric pairing are the root metric adapter's"
             ),
+            "budget": (
+                "v004 (L24-L26): caller budget_hook() -> bool polled between calls, jumps, "
+                "moves and sweeps; True ends the run status incomplete, incomplete_reason "
+                "INCOMPLETE_BUDGET, ok False, committed prefixes in partial as diagnostics, "
+                "no analysis, no resumability; caps give INCOMPLETE_CAP with the same partial; "
+                "progress_sink(record=...) gets small synchronous records; no clock, memory "
+                "or threshold is read or hard-coded here"
+            ),
         },
         "scope": (
             "Static isothermal native functional of the quasi-static maximum-entropy closure at "
@@ -2962,6 +3238,8 @@
     error_parameters,
     numerical_tolerances,
     implicit_closure,
+    budget_hook,
+    progress_sink,
 ):
     """Static joint source Hessians of the owned collective by positive worldline sampling.
 
@@ -3035,8 +3313,21 @@
         (relative gauge/Hermiticity tolerances and absolute partition tolerance).
       implicit_closure: must be None (SPEC section 5 contract retained for later);
         anything else returns status "unsupported".
-
-    Returns a dict: ok, status, stage_reached, failures, flags, inputs, coordinate_order,
+      budget_hook (v004, 0413 item 2; L24, L26): None, or a callable taking NO arguments
+        and returning a bool, True requesting a cooperative stop. Polled before/after every
+        operator and adapter call, between proposal jumps, before held replays, between
+        moves, at sweep and chain starts and before analysis; never given a Generator. True
+        ends the run "incomplete" with incomplete_reason "INCOMPLETE_BUDGET", ok False and
+        the committed prefixes in "partial"; a raise or a non-bool return is "failed".
+        Root's 150 s / 900 MiB cooperative policy belongs inside this hook.
+      progress_sink (v004, 0413 item 4; L25): None, or a callable called synchronously as
+        progress_sink(record=dict) with small stage / chain / completed-warmup /
+        completed-measurement / move-counter records; return value ignored; flushing is
+        the sink's; a raise is "failed".
+
+    Returns a dict: ok, status, incomplete_reason (v004), partial (v004; committed prefixes
+    as diagnostics on an incomplete stop, else None; L24), stage_reached, failures, flags,
+    inputs, coordinate_order,
     direction_status, tracked_read_labels, read_kinds, member_check, modes (None without mode
     directions; else profile/Gram metadata, base sources, direction positions, extensive
     F_total gradient/Hessian and score/contact moments, error-layout positions and uniform
@@ -3109,6 +3400,8 @@
     n_meas = _admit_int("measurement_sweeps", measurement_sweeps, 1, failures)
     errp = _admit_error_parameters(error_parameters, n_meas, failures)
     tol = _admit_tolerances(numerical_tolerances, failures)
+    hook_ok = _admit_optional_callable("budget_hook", budget_hook, failures)  # v004 (L24)
+    sink_ok = _admit_optional_callable("progress_sink", progress_sink, failures)  # v004 (L25)
     if coords is not None and tracked is not None and not coords and not tracked:
         failures.append("input: no derivative coordinate and no tracked read; nothing to compute")
     result["inputs"] = {
@@ -3146,6 +3439,8 @@
         "measurement_sweeps": n_meas,
         "error_parameters": errp,
         "numerical_tolerances": tol,
+        "budget_hook": None if budget_hook is None else ("callable" if hook_ok else "rejected"),
+        "progress_sink": None if progress_sink is None else ("callable" if sink_ok else "rejected"),
     }
     if failures:
         result["status"] = "failed"
@@ -3203,10 +3498,17 @@
             "restricted_enumerations": 0,
             "restricted_nonmember_records_dropped": 0,
             "palette_verifications": 0,
+            "budget_checks": 0,  # v004 (L24)
         },
         "zero_rate_directions": set(),
+        "budget_hook": budget_hook,  # v004 (L24)
+        "progress_sink": progress_sink,  # v004 (L25)
+        "burn_in_sweeps": burn,
+        "measurement_sweeps": n_meas,
+        "move_open": False,  # v004: True only while a proposal is unfinished
     }
     chain_diag = []
+    series = []  # v004: per-chain arrays registered at chain start (0413 item 1)
 
     def _diagnostics():
         return {
@@ -3215,9 +3517,43 @@
             "zero_rate_directions": sorted(map(repr, run["zero_rate_directions"])),
         }
 
+    def _stopped(stop):
+        """v004: fail-closed result for any internal stop; prefixes only if incomplete (L24)."""
+        result["status"] = stop.status
+        result["stage_reached"] = stop.stage
+        failures.append(stop.message)
+        result["diagnostics"] = _diagnostics()
+        budget = isinstance(stop, _BudgetStop)
+        info = {
+            "status": stop.status,
+            "reason": None,
+            "checkpoint": stop.checkpoint if budget else None,
+            "message": stop.message,
+            "proposal_in_progress": bool(run["move_open"]),
+        }
+        if stop.status == "incomplete":
+            result["incomplete_reason"] = "INCOMPLETE_BUDGET" if budget else "INCOMPLETE_CAP"
+            info["reason"] = result["incomplete_reason"]
+            result["partial"] = _partial_prefixes(run, series, chain_diag, len(paths_in), stop)
+            result["flags"].append(
+                f"{result['incomplete_reason']}: committed measurement prefixes returned in "
+                "'partial' as diagnostics only (not unbiased estimates, no accepted "
+                "uncertainty); no mixing or error analysis was run; no resumability (L24)"
+            )
+        try:
+            _progress(run, "stop", stop.stage, None, info)
+        except _Stop as late:
+            failures.append(late.message + " (at the final stop record; stop status kept)")
+        return result
+
     # ---- Stage: operator schema validation (the member check follows; L2) --------
     result["stage_reached"] = "model"
     try:
+        _progress(run, "stage", "model", None, None)  # v004 (L25)
+        _budget_check(run, "before", "validate_owned_model")  # v004 (L24)
+    except _Stop as stop:
+        return _stopped(stop)
+    try:
         validated = api["validate_owned_model"](
             graph0=graph0, model=model, registration=registration
         )
@@ -3234,6 +3570,11 @@
             failures.extend(f"validate_owned_model: {f}" for f in validated["failures"])
         return result
     run["context"] = validated["context"]
+    try:
+        _budget_check(run, "after", "validate_owned_model")  # v004 (L24)
+        _progress(run, "stage", "member_check", None, None)  # v004 (L25)
+    except _Stop as stop:
+        return _stopped(stop)
 
     # ---- Stage: model-level member check (state independent; L2a) ----------------
     result["stage_reached"] = "member_check"
@@ -3258,6 +3599,10 @@
 
     # ---- Stage: binding of energy cells, palette groups and dual sources --------------
     result["stage_reached"] = "binding"
+    try:
+        _progress(run, "stage", "binding", None, None)  # v004 (L25)
+    except _Stop as stop:
+        return _stopped(stop)
     present_c, cells = _field(run["context"], "energy_cells")
     if not present_c or not isinstance(cells, (list, tuple)) or not all(_hashable(c) for c in cells):
         result["status"] = "failed"
@@ -3332,13 +3677,13 @@
 
     n_u = run["n_u"]
     n_r = run["n_r"]
-    series = []
     try:
         # ---- Stage: initial closed paths ------------------------------------------
         result["stage_reached"] = "initial_paths"
         paths = []
         for c, spec in enumerate(paths_in):
             run["stage"] = f"initial_paths[{c}]"
+            _progress(run, "stage", run["stage"], None, None)  # v004 (L25)
             paths.append(_initial_path(run, spec))
         # ---- Stage: sampling ------------------------------------------------------
         result["stage_reached"] = "sampling"
@@ -3366,12 +3711,28 @@
                 "accepted_in_measurement": 0,
                 "sweeps_completed": 0,
                 "measurements": 0,
+                "burn_in_sweeps_completed": 0,  # v004 (L25)
             }
             chain_diag.append(diag)
+            run["stage"] = f"chain {c} start"
+            _budget_check(run, "before", "chain arrays")  # v004 (L24)
             score = np.zeros((n_meas, n_u), dtype=np.float64)
             contact = np.zeros((n_meas, n_u, n_u), dtype=np.float64)
             reads = np.zeros((n_meas, n_r), dtype=np.float64)
             n_events = np.zeros(n_meas, dtype=np.int64)
+            # v004 (0413 item 1): the chain is registered BEFORE its first sweep; its
+            # committed count advances only after a whole measurement tuple is written.
+            entry = {
+                "chain": c,
+                "score": score,
+                "contact": contact,
+                "reads": reads,
+                "events": n_events,
+                "measurements_committed": 0,
+                "accepted_in_measurement": 0,
+            }
+            series.append(entry)
+            _progress(run, "chain_start", run["stage"], diag, None)  # v004 (L25)
             for sweep in range(burn + n_meas):
                 if run["counters"]["sweeps"] >= caps_in["max_sweeps"]:
                     raise _Stop(
@@ -3379,11 +3740,16 @@
                         f"chain {c} sweep {sweep}",
                         "cap max_sweeps reached; computation ended",
                     )
-                run["counters"]["sweeps"] += 1
                 run["stage"] = f"chain {c} sweep {sweep}"
+                _budget_check(run, "between", "sweeps")  # v004 (L24), before the sweep counts
+                run["counters"]["sweeps"] += 1
                 measuring = sweep >= burn
-                for _ in range(moves["moves_per_sweep"]):
+                for mv in range(moves["moves_per_sweep"]):
+                    if mv > 0:
+                        _budget_check(run, "between", "moves")  # v004 (L24)
+                    run["move_open"] = True  # v004: a stop now abandons this proposal
                     path, accepted = _move(run, path, rng, diag)
+                    run["move_open"] = False
                     if accepted:
                         diag["accepted_regrowths"] += 1
                         if measuring:
@@ -3395,26 +3761,34 @@
                     contact[i] = t_mat
                     reads[i] = r_vec
                     n_events[i] = k
+                    entry["measurements_committed"] += 1  # v004: whole tuple committed
                     diag["measurements"] += 1
+                else:
+                    diag["burn_in_sweeps_completed"] += 1  # v004 (never a measured sample)
                 diag["sweeps_completed"] += 1
-            series.append(
-                {
-                    "score": score,
-                    "contact": contact,
-                    "reads": reads,
-                    "events": n_events,
-                    "accepted_in_measurement": diag["accepted_in_measurement"],
-                }
-            )
+                _progress(run, "sweep", run["stage"], diag, None)  # v004 (L25)
+            entry["accepted_in_measurement"] = diag["accepted_in_measurement"]
     except _Stop as stop:
-        result["status"] = stop.status
-        result["stage_reached"] = stop.stage
-        failures.append(stop.message)
-        result["diagnostics"] = _diagnostics()
-        return result
+        return _stopped(stop)  # v004: prefixes kept on incomplete stops (L24)
 
     # ---- Stage: directions and analysis -------------------------------------------
     result["stage_reached"] = "analysis"
+    run["stage"] = "analysis"
+    try:
+        _progress(run, "stage", "analysis", None, None)  # v004 (L25)
+        _budget_check(run, "before", "analysis")  # v004 (L24): no analysis after a stop
+    except _Stop as stop:
+        return _stopped(stop)
+    if len(series) != len(paths_in) or any(
+        e["measurements_committed"] != n_meas for e in series
+    ):
+        result["status"] = "failed"
+        failures.append(
+            "internal: a chain reached the analysis without all measurement_sweeps committed "
+            "(zero padding is never analysed; L24)"
+        )
+        result["diagnostics"] = _diagnostics()
+        return result
     supported = [i for i, c in enumerate(coords) if c not in run["zero_rate_directions"]]
     result["direction_status"] = {
         repr(c): ("supported" if i in supported else "unsupported: zero-rate source-opening")
```
