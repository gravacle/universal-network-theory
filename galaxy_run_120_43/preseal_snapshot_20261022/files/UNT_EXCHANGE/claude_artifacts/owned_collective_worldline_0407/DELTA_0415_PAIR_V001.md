# DELTA 0415 PAIR V001: exact adjacent marked-event pair update, feature branch on v004

**Role.** Author of the 0415 adjacent pair insertion/deletion feature branch. I am not the W2 (sequential v005) author or the 0414 all-k author. A distinct correctness review is still pending; 0415 item 6 asks for one covering proposal algebra, primitive identity, graph-changing reverses, local-palette selection, diagnostics and budget-stop behavior.

**What pair_v001 is.** It is a byte copy of the accepted `owned_collective_worldline_static_response_v004.py` (0413 revision) plus ONLY:
- the 0415 pair move;
- its root-declared absolute schedule, carried by one new required argument;
- the 0415 item 4 diagnostic corrections.

It changes no physics, estimator, source, event contact, 10-field coupling, cosine/sine block, interval density, valid-prefix handling, same-sample covariance custody, warmup/measurement target or numerical threshold.

**Integration order.** 0413 v004 → {W2 sequential v005, 0414 all-k branch `allk_v001`, this pair branch} → one explicit later merge. This file is immutable. The `diff -u` at the end is self-contained, and I checked that it re-applies to v004 byte-identically (`patch` → `cmp`).

**Method (static only).**
- I wrote the module as text in my scratch directory. I did not import or execute it, any operator or the root adapter.
- I ran no numbers, did no sampling or benchmarks, used no network and installed nothing.
- The only code I ran was:
  - `shasum -a 256`, `diff -u`, `patch -o` (scratch), `cmp`;
  - `python3 -I -B` doing `ast.parse`, `compile` (no exec) and `symtable` on TEXT copies in scratch;
  - one `math.fsum` of the root's declared schedule constants (0.50 + 0.10 + 0.35 + 0.05 = 1.0, and 0.50 + 0.50 = 1.0).
- Both deliverables were written by exclusive create (noclobber). Nothing was overwritten, moved, deleted or chmod-ed.
- There is no `__pycache__` in the 0407 directory.
- I wrote nothing under `Universal Network Theory` and opened no file with a forbidden name.
- I did not touch the historical sampler or result files, or the W2 or all-k files.

## Hashes (full sha256, computed from bytes)

| File | sha256 | Status |
|---|---|---|
| `FROM_CODEX/0415_2026-10-16_exact_event_pair_update_after_zero_event_samples.md` (read fully) | 1283bb48baa48abfd45c80ebf2289f9bdc356f1cc7002d3ed2753ee070bd8a27 | binding, matched |
| BASE `owned_collective_worldline_static_response_v004.py` (187151 B, 3860 lines) | 6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea | binding, matched, unchanged |
| `helpers/coefficient_method/OWNED_WORLDLINE_ADJACENT_PAIR_INSERT_DELETE_PROPOSED_V001.txt` ("PAIR SPEC", read fully) | 252fbeaa74eb3bf448ca088e3c460bd531f07f597d7dc839f57cbbee36fc5f8a | binding, matched |
| `helpers/response_packet_audit/OWNED_ADJACENT_PAIR_INSERT_DELETE_DISTINCT_REVIEW_V001.json` ("PAIR REVIEW", read fully) | 9e444820713f9b10ccaf9cf2eb1fedb8eab2178d7ea85c2ee7382cbc5f35d18d | binding, matched |
| operator `owned_retained_response_0405/owned_parent_operator_v003.py` (text only) | a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07 | binding, matched |
| `DELTA_0410_BUDGET_V004.md`, `REVIEW_0410_BUDGET_V001.md`, `CONVENTIONS_0407_V003.md` | (base documentation) | read |
| **NEW** `owned_collective_worldline_static_response_pair_v001.py` (227823 B, 4545 lines) | 080153ee3ef69c470b9302570852c8ae612462ae32df62e99393ae0ec608f523 | exclusive create |

## Exact API additions

There is one public entry point. It keeps every v004 argument, in order and with its meaning. It appends ONE required keyword-only argument without default (L3845):

```
owned_collective_worldline_static_response(*, operator_api, graph0, model, registration,
    initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients,
    volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
    diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
    caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
    implicit_closure, budget_hook, progress_sink, pair_move_parameters)
```

`pair_move_parameters` is either `None` (no pair move: the v004 move law and draw sequence) or:

```
{"schedule": {"pair": p_pair, "rotation": p_rot, "palette_regrowth": p_pal, "full_regrowth": p_full},
 "insertion_probability": pI, "deletion_probability": pD, "local_palette": bool}
```

Validation is in `_admit_pair_move_parameters` (L1076-1177). It is fail-closed, and no value is chosen in the module:
- Every key is required.
- Every probability is a finite real.
- p_pair, p_rot and p_full lie in (0,1). p_pal lies in (0,1) when `palette_parameters` is given, and must be exactly 0 otherwise.
- `math.fsum` of the four ABSOLUTE probabilities must equal 1 exactly. No renormalization is applied.
- p_rot must equal `move_parameters['rotation_probability']`, and p_pal must equal `palette_parameters['selection_probability']` (one source of truth).
- pI and pD lie in (0,1), and their `math.fsum` must equal 1 exactly.
- `local_palette` is a bool. True requires `palette_parameters`, and S is then drawn from that argument's fixed weighted permanent-label palette list.

Root's declared trial, passed by the caller: `{"schedule": {"pair": 0.50, "rotation": 0.10, "palette_regrowth": 0.35, "full_regrowth": 0.05}, "insertion_probability": 0.50, "deletion_probability": 0.50, "local_palette": True}`. It needs `move_parameters['rotation_probability'] = 0.10` and `palette_parameters['selection_probability'] = 0.35`. Both fsums are exactly 1.0.

**Additive result keys:**
- `inputs.pair_move_parameters`.
- `diagnostics.pair_no_reverse_by_kind`.
- Per-chain diagnostics, changed versus identity acceptance: `changed_path_accepts`, `identity_accepts`, their `_in_measurement` versions, and `interval_/palette_{changed,identity}_accepts`.
- Per-chain diagnostics, measured event counts: `measured_events_total`, `measured_events_max`, `measured_zero_event_samples`.
- Per-chain diagnostics, pair counts: `pair_attempts`, `pair_accepted`, `pair_rejected`, `pair_insert_{attempts,no_forward,no_reverse,metropolis_rejections,accepted}` and `pair_delete_{attempts,too_few_events,ineligible,palette_nonmember,metropolis_rejections,accepted}`.
- `mixing` gains `stuck_chains_zero_changed_path_accepts_in_measurement`, `changed_path_accepts_in_measurement`, `identity_accepts_in_measurement`, `measured_event_counts` and `exact_invariant_columns`.
- `partial.chains[*]` gains `changed_path_accepts_in_measurement`, `identity_accepts_in_measurement` and `measured_zero_event_samples`.
- `conventions` gains `pair_move`.
- The progress-record `module` string is now `owned_collective_worldline_static_response_pair_v001`.

**Changed keys and semantics:**
- `mixing.column_status` can now be `"exact_invariant"`. A constant non-invariant column now has status `"unassessable"` (it was `"constant"`) and is still listed in `mixing.constant_columns`.
- Every move returns `(path, outcome)` with outcome `"rotation" | "rejected" | "changed" | "identity"`. This is internal.

## Change map (pair_v001 line numbers)

| Where | Lines | Change |
|---|---|---|
| Module docstring | 3-15, 89-101, 111-114, 238-255, 321-327 | header and integration order; bindings; signature; WHERE 0415 IS IMPLEMENTED; COST |
| `LIMITATIONS` | addenda to L10 (428-429), L13 (445-447), L16 (459) and L24 (587-589); NEW L27-L30 at 617-703 | pair move, diagnostics, schedule/RNG, primitive identity |
| `_admit_pair_move_parameters` | 1076-1177 | NEW: schedule and split validation |
| `_progress` | 1830 | module string |
| `_move` | 2639-2657 | outcome strings; pair dispatch when `u >= p_rot + p_pal + p_full` (2655) |
| `_interval_move` | 2660-2711 | outcome strings; changed/identity accept counters (2707-2711) |
| `_palette_move` | 2744-2888 | outcome strings; changed/identity accept counters (2883-2888) |
| `_pair_channels`, `_unique_mark`, `_pair_reverse_set`, `_pair_log_ratio`, `_pair_move`, `_pair_insert`, `_pair_delete` | 2891-3163 | NEW: the pair kernel |
| `_analyze` | 3321-3449 | exact-invariant / unassessable constant columns (3364-3383); stuck by changed-path acceptance (3398-3402); measured event counts (3413-3423); report keys |
| `_partial_prefixes` | 3673-3676 | changed/identity and zero-event counters |
| `_new_result` | 3746-3760 | `conventions.moves`, `conventions.pair_move` |
| Public function | 3845, 3930-3939, 3951-3955, 4015-4017, 4064-4069, 4114-4116, 4147, 4345-4372, 4391-4392, 4411-4421, 4431-4435, 4441-4442, 4479, 4520-4536 | argument and docstring; admission; inputs echo; run keys; diagnostics; diag counters; series entry; outcome split; measured events; entry counters; `supported_coords`; flags |

AST def-level comparison (text):
- 8 defs added: `_admit_pair_move_parameters`, `_pair_channels`, `_unique_mark`, `_pair_reverse_set`, `_pair_log_ratio`, `_pair_move`, `_pair_insert`, `_pair_delete`.
- 0 removed.
- 10 changed: the docstring, `LIMITATIONS`, `_progress`, `_move`, `_interval_move`, `_palette_move`, `_analyze`, `_partial_prefixes`, `_new_result` and the public function.
- 90 AST-identical, among them `_measure`, `_estimate`, `_sums`, `_sokal_tau`, `_rhat`, `_segment_core`, `_reads_at`, `_diagonal_at`, `_channels_from_records`, `_event_from_channel`, `_reverse_check`, `_ctmc_segment`, `_select_interval`, `_rotate`, `_choose_channel`, `_choose_palette`, `_count_new_event`, `_palette_channels`, `_initial_path` and `_mode_outputs`.

## Requirement trace (0415 and this assignment; pair_v001 line numbers)

| Requirement | Where | Status |
|---|---|---|
| Insertion inside one dwell of length ell | segment uniform on 0..K, `rng.integers(0, k + 1)` (3003); lo, hi, ell (3004-3006) | MET |
| Two sorted uniform times, density 2/ell² | 3041-3044; strict lo < t1 < t2 < hi, otherwise L15 failed, never jitter (3045-3051) | MET |
| Actual x→y primitive mark | `_pair_channels` (2896-2909) gives the actual records at x (palette or full); `_choose_channel` gives p_a = W_a/r_S(x) (3013) | MET |
| Actual compatible y→x mark | `_pair_reverse_set` (2932-2944): reverse kind, SAME full owner_id, canonical target key(x) verified (3021) | MET |
| Both proposal probabilities and actual weights | `_pair_log_ratio` (2947-2971) keeps log W_a, log W_b, log p_a, log p_b unsimplified | MET |
| Full diagonal-action difference | −(D_y − D_x)(t2 − t1) (2966), from the actual D of the stored x dwell and the newly built y dwell | MET |
| Full canonical return | key(target of b) = key(x) verified before b is admitted (2942); gauge net increments (0,0,0) (3034-3040) | MET |
| All source/read changes | y built by `_segment_core` (3016): full canonical key, `diagonal_terms`, `read_rows`, callback reads, pair source; D, D_a and the read row from ONE evaluation; rho of both events from their own actual records (3032-3033) | MET |
| Deletion: uniform over ALL nonwrapping adjacent positions, reject ineligible, entire merged dwell | K < 2 rejects (3082); `rng.integers(0, k - 1)` with no eligibility conditioning (3086); ineligible and nonmember pairs reject (3093-3104); ell = t_{i+2} (or β) − t_{i−1} (or 0) (3147-3149) | MET |
| Marked reverse multiplicities and detailed balance | individual marks only; R holds same-owner records only; deletion recomputes p_a and p_b from actual enumerations at x and y (3113-3133); reciprocal ratio (3150) | MET (static algebra below) |
| Fixed state-independent local palettes, drawn BEFORE eligibility, never resampled | `_pair_move` (2984) draws S once per attempt, before insert/delete and before any enumeration; no loop anywhere | MET |
| Schedule as validated caller inputs, no defaults or numbers | `_admit_pair_move_parameters` (1076-1177); `_move` (2655) | MET |
| Same palette distribution for the local pair kernel | `_choose_palette(run["palette"], rng)` (2984), the palette regrowth's own cumulative list | MET |
| Full global and rotation support kept | p_rot and p_full required in (0,1) (1113); global regrowth and rotation code unchanged | MET |
| Primitive identity, duplicate-key assertion, p_b = 1 only after the unique compatible reverse check | `_unique_mark` (2912-2929) at the source (3014, 3114) and at y (via 2941); target verification (2942, 3115); r_back = Σ_R W (3029, 3133) | MET |
| Locality: reuse only with matching canonical identity; one intermediate build; splice only the affected dwell | insertion reuses the x dwell only after the key(x) check (3059); deletion requires key(z) = key(x) (3094) and equal D, D_a and row (3105-3112); O(K) slicing (3058-3062, 3156-3160); no replay or re-enumeration of the unchanged path | MET |
| Budget checkpoints and incomplete-prefix semantics | every operator and adapter call goes through `_op` / `_reads_at` (bracketed); no `except _Stop` in pair code, so a stop abandons the proposal (`move_open`); caps through `_count_new_event` (3015, 3031) give INCOMPLETE_CAP, never a rejection | MET |
| Changed-path versus identity acceptance across ALL moves | outcomes in `_move`, `_interval_move` (2709), `_palette_move` (2886), pair (3065, 3163); split in the loop (4411-4421) | MET |
| Measured event counts; pair attempt/accept/insert/delete/no-reverse/rejection counts | loop (4431-4435); `_analyze` (3413-3423); diag init (4345-4372); per-kind no-reverse (3024) | MET |
| Constant columns UNASSESSABLE unless exact invariants; no mixing from zero variance or identity acceptance | `_analyze` 3364-3383 and 3398-3402 | MET |
| Existing numerical criteria kept | `rhat_max`, `min_batch_length_over_tau`, Sokal window, jackknife and `max_explicit_covariance_dimension` unchanged | MET |
| Sources, event contacts, 10-field coupling, cos/sin blocks, valid prefixes, same-sample covariance intact | `_measure`, `_estimate`, `_sums`, `_segment_core`, `_reads_at`, `_diagonal_at`, `_event_from_channel` and `_mode_outputs` are AST-identical; the prefix logic is unchanged | MET |
| RNG law unchanged when the pair move is never selected; exact statement when it is | below and L29 | MET (static) |

## MH ratio as implemented (`_pair_log_ratio`, L2947-2971)

**Target.** The target is the PAIR SPEC target, the same one every other move samples. It is the rooted closed-path density with respect to ordered event times and individual primitive marks:

  π(path) ∝ exp(−∫ D dτ) · Π_events W_mark

There is no 1/K!.

**Proposals.** The rooted path has K events. Let x be dwell i, with bounds lo = (0 or t_{i−1}) and hi = (β or t_i), and ell = hi − lo.

- Insertion density: q_I(new | old) = p_pair · ω_S · pI · 1/(K+1) · p_a · p_b · 2/ell².
  - p_a = W_a / r_S(x), where r_S(x) is the full exit rate r(x) when `local_palette` is False.
  - p_b = W_b / r_back, with r_back = Σ_{R(a;x,y)} W.
- Reverse density: q_D(old | new) = p_pair · ω_S · pD · 1/(K+1). The new path has K+2 events, so K+1 nonwrapping adjacent positions.
- p_pair, ω_S and 1/(K+1) cancel.

**Insertion** of a at t1 and b at t2 in dwell x of length ell, with intermediate state y. It is accepted with min(1, exp(log R_I)):

```
log R_I = [log pD - log pI] + 2 log ell - log 2
          + log W_a + log W_b
          - [log W_a - log r_S(x)]          # - log p_a
          - [log W_b - log r_back]          # - log p_b
          - (D_y - D_x) * (t2 - t1)
```

**Deletion** of events i, i+1 (marks a, b) between dwells x = seg[i], y = seg[i+1] and z = seg[i+2], with key(z) = key(x). It is accepted with min(1, exp(log R_D)):

```
log R_D = - log R_I(ell_merged, W_a, r_S(x), W_b, r_back, D_x, D_y, t2 - t1)
ell_merged = (t_{i+2} or beta) - (t_{i-1} or 0)      # all three old dwells
```

**Inputs to the ratio.**
- p_a and p_b are recomputed from actual enumerations at x and at y, under the same selection rule and the same S.
- W_a and W_b are the re-enumerated actual rates. They must equal the stored event rates exactly.
- D_x and D_y are the stored full-evaluation dwell energies.
- The terms are summed with `math.fsum` and the result must be finite. No β², K!, degeneracy, holding-survival or bridge factor appears.

**Check.** π(new)/π(old) = W_a W_b e^{−(D_y−D_x)(t2−t1)}. Only the intermediate dwell changes D; the outside marks and the x dwell are unchanged, and canonical return is verified. So R_I = π(new) q_D / (π(old) q_I) is exactly the expression above, and R_D = 1/R_I for the same (path, pair) couple.

Because of the duplicate-key assertion, |R| = 1, so r_back = W_b and log p_b = 0 exactly. The unsimplified form is kept as PAIR SPEC asks.

**Accept/reject pattern.** It is v004's: a uniform is drawn only when log R < 0, and accepted iff u < exp(log R).

## Identity-check implementation (L30; operator v003 read as text)

**What operator v003 provides** (`_owner_id` L1781, `_root_cuts` L1097, `_reverse_channels` L1168, `_reverse_descriptor` L1217, `_transitions` L1566):

| kind | owner_id | Uniqueness at a fixed state | Reverse at y |
|---|---|---|---|
| flip | `("flip", ("edge", (A, B)))` | one per current edge | flip, same owner |
| hop | `("hop", ("edge", (A, B)))` | at most one, because the direction is fixed by p_A ≠ p_B | hop, same owner, opposite direction |
| bind | `("bind", ("vertex", v))` | one per carrier vertex | bind, same owner |
| admit | `("admission", ("vertex", v))` | one per vertex | admit_rev, same owner |
| admit_rev | `("admission", ("vertex", v))` | one per vertex; kind separates it from admit | admit, same owner |
| birth | `("birth", owner, sorted cut edge labels)` | one per (owner, cut); `_root_cuts` deduplicates cuts | birth_rev, same owner, restored set = the cut |
| birth_rev | `("birth", owner, sorted restored-cut labels)` | one per pairing σ; distinct matchings give distinct restored sets | birth, same owner |

**Module code.**
- `_unique_mark(run, channels, kind, owner, where)` (L2912-2929) returns the single positive-rate record with that kind and full owner_id. If more than one record matches, the run ends `failed` (the duplicate-key assertion).
  - It runs at the source after the forward mark is drawn (3014).
  - It runs at the source again on deletion (3114).
  - It runs at y through `_pair_reverse_set` (2941).
- `_pair_reverse_set(run, y_channels, mark, x_key, where)` (L2932-2944) builds R:
  - reverse kind from the v004 kind table;
  - the SAME full owner_id;
  - at most one record, by the assertion;
  - membership only after `_keys_equal(_target_key(rec), key(x))`, which is the canonical target verification.
  - It returns `[]` when no compatible reverse exists. Nothing is invented and no grouped or summed rate is substituted.
- Insertion with an empty R is a rejection. It is counted in `pair_insert_no_reverse` and `run["pair_no_reverse"][kind]`, and flagged in the result.
- Deletion with a missing record at x or y, or with a stored rate that differs from the re-enumerated one, ends the run `failed`. Such a path/operator inconsistency is never treated as a rejection.
- p_b = W_b / Σ_R W = 1 only after this unique compatible check. It is never inferred from `_reverse_check`'s grouped equality.
- The v004 grouped `_reverse_check` (L12) and `_no_self_loop` still run on the inserted forward mark, exactly as for every sampled event.
- Palette membership (`_record_groups`) depends only on (kind, owner_id). So a palette enumeration contains either every record of a key or none of them, and uniqueness inside it equals uniqueness in the full enumeration.

## Diagnostics added (L28)

- **Move outcomes.** Every move returns `"rotation" | "rejected" | "changed" | "identity"`.
  - An accepted global regrowth is `"identity"` iff the interval had no old event and generated none (2709).
  - An accepted palette regrowth is `"identity"` iff every old interval event was held and replayed and no member event was generated (2886).
  - An accepted pair move is always `"changed"`.
  - Rotation is never an acceptance, as in v004.
- **Per-chain counters.**
  - `changed_path_accepts`, `identity_accepts` and their `_in_measurement` versions;
  - `interval_{changed,identity}_accepts` and `palette_{changed,identity}_accepts`;
  - `measured_events_total`, `measured_events_max` and `measured_zero_event_samples`, updated after each committed sample;
  - `pair_attempts`, `pair_accepted`, `pair_rejected`;
  - `pair_insert_{attempts,no_forward,no_reverse,metropolis_rejections,accepted}`;
  - `pair_delete_{attempts,too_few_events,ineligible,palette_nonmember,metropolis_rejections,accepted}`.
- **Run-level.** `diagnostics.pair_no_reverse_by_kind`.
- **`_analyze`.**
  - A chain with zero changed-path acceptances in measurement is stuck, and mixing fails.
  - A primary column constant in every sample of every chain is `"unassessable"`, so mixing cannot pass and no error band is returned. The exception is an analytically exact invariant: a contact T_ab with a or b of a kind whose per-event rho is identically 0 (`source`, `volume_multiplier`, `pair_source_R`, `pair_source_S`, `source_direction`). Those are reported as `exact_invariant_columns`.
  - `measured_event_counts` per chain (min, max, mean, zero-event samples) is reported.
  - Thresholds are untouched.
- **Partial prefixes** carry the changed/identity and zero-event counters.
- **Progress records** carry all new counters automatically (`dict(diag)`).

## RNG-sequence statement (L29)

**`pair_move_parameters` is None.**
- `_move` draws u, then takes the v004 branches with the v004 draws.
- `_interval_move` and `_palette_move` changed only their return values and added counter increments after acceptance. Neither touches `rng`.
- The draw sequence and the transition law are v004's (static argument: AST plus hand trace; not measured).

**`pair_move_parameters` is given.** The move-type uniform u is drawn as before.
- Rotation iff u < p_rot, and palette iff u < p_rot + p_pal. Both are the identical v004 float expressions.
- Global regrowth iff u < (p_rot + p_pal) + p_full; otherwise the pair move. In v004, global regrowth took every u ≥ p_rot + p_pal.
- Rotation, palette and global moves then draw exactly as in v004. So as long as no u reaches the pair interval, the run is draw-for-draw v004's.

**A pair move draws, in order:**

| Step | Draw | When |
|---|---|---|
| 1 | S: one `rng.random()` via `_choose_palette` | `local_palette` only |
| 2 | insert/delete: one `rng.random()` | always |
| 3 (insertion) | dwell: one `rng.integers(0, K+1)` | always |
| | forward mark: one `rng.random()` via `_choose_channel` | only if r_S(x) > 0 |
| | t1, t2: two `rng.random()` | only after the unique compatible reverse is found |
| | MH: one `rng.random()` | only if log R_I < 0 |
| 3 (deletion) | position: one `rng.integers(0, K−1)` | only if K ≥ 2 |
| | MH: one `rng.random()` | only if the pair is eligible and log R_D < 0 |

Notes:
- The conditional draw structure does not change the proposal density.
- Floating partial sums of the schedule (for example (0.10 + 0.35) + 0.05 = 0.49999999999999994) shift mixture weights by an ulp. They never change the target, because each kernel is separately reversible.

## AST results (final bytes, text copy, `python3 -I -B` 3.9)

- `ast.parse` and `compile` (no exec): OK. `symtable`: no undefined globals.
- Imports: `bisect`, `math`, `collections.abc.Mapping` and `numpy`, as in v004.
- No `MatMult` (binary or augmented). No `dot`, `matmul`, `vdot`, `inner`, `tensordot`, `outer`, `kron` or `linalg` attribute.
- 10 `einsum` calls, all with `optimize=False`. All are unchanged from v004.
- No `open`, `print`, `eval`, `exec`, `compile`, `__import__`, `os`, `sys`, `time`, `subprocess`, `pickle`, `pathlib`, `scipy` or similar name.
- No decorator, global/nonlocal or async/yield.
- Module level holds only the docstring, 4 imports, the `LIMITATIONS` string, 2 classes and 104 defs (v004 had 96). Nothing runs at import.
- Numeric constants are {0, 0.5, 1, 2, 3, 4, 20}, the same set as v004. No schedule or budget number is hard-coded.
- `rng` methods used: `random`, `exponential` (v004) and `integers` (new, for the uniform dwell or position choice).
- Exactly one public callable, `owned_collective_worldline_static_response` (L3818). It has 0 positional parameters, no `*args` or `**kwargs`, and 26 keyword-only parameters (the 25 of v004 plus `pair_move_parameters`) with no defaults.
- `diff -u v004 → pair_v001` is 1071 lines in 41 hunks. `patch` of a scratch copy of v004 with it reproduces pair_v001 byte for byte (sha256 080153ee…f523).

## LIMITATIONS (recorded, not resolved by inventing physics or numbers)

1. **Static only.** Detailed balance, the cancellations and the RNG statements are argued algebraically and by AST/hand trace. Nothing was run, and no acceptance rate, mixing or event-count behaviour is claimed. The 0415 zero-event result motivates this move; it does not certify the move's future samples.
2. **Not irreducible alone.** Pair moves are rooted and nonwrapping. Wrapping arcs are reached through rotation. Changes of the dwell-0 state, Birth-count and resource changes not made of adjacent same-owner pairs, and long-range paths need the global and palette regrowths. Both keep nonzero probability (p_full and p_pal admitted in (0,1)).
3. **Exact-sum admission.** The four absolute probabilities and the insertion/deletion split must sum to 1 exactly under `math.fsum`. Root's 0.50/0.10/0.35/0.05 and 0.50/0.50 do. Another declaration whose binary values do not sum exactly fails at admission rather than being renormalized.
4. **Duplicate primitive keys end the run.** If an operator ever returned two positive-rate records with the same (kind, owner_id) at one state, the run fails closed. Operator v003 does not expose a stable ordinal; for v003 the text shows none occurs. The same holds for a missing same-owner record at deletion and for a stored rate that differs from its re-enumerated record (exact float equality, justified by deterministic state functions).
5. **Missing same-owner reverse is a rejection, not a failure, in the pair move.** The global moves would end such a run `failed` through `_reverse_check` if no reverse existed at all. The pair move rejects first and reports by kind, as PAIR SPEC requires. The v004 grouped check still runs whenever the same-owner reverse exists.
6. **Analysis is stricter for every run, pair move or not.**
   - A chain whose measurement phase accepted only identity proposals is now stuck (mixing failed). In v004 it was not.
   - A caller read that is constant on the whole component, for example an always-present presence row, now makes mixing `unassessable`. The module cannot certify a read as an exact invariant; such a column should not be tracked. Only rho-zero contact columns are certified.
7. **Identity classification.** An identity-accepted regrowth still applies v004's rotate-there-and-back to the times, so they can move by float rounding. It is classified "identity" because no mark, state or event count changed.
8. **Cost.**
   - Every insertion attempt with a forward mark builds one full intermediate `_segment_core` before the reverse is known. A no-reverse rejection therefore costs a full read and callback evaluation.
   - The forward duplicate-key scan and the deletion's two enumerations are O(channels).
   - With `local_palette` False the enumerations are global `primitive_channels`.
   - The O(K) list splice remains, as PAIR SPEC allows. No incremental storage is implemented (L3).
9. **Float selection.** `_choose_channel` (v004) realizes p_a = W_a/r_S(x) up to the floating cumulative-sum rounding of the existing CTMC selection, and `rng.integers` is exactly uniform. Time coincidences end the run `failed` (L15).
10. **Budget/caps.** Pair-move operator and adapter calls are bracketed through `_op` / `_reads_at`; the move adds no checkpoint of its own. A stop abandons the proposal (`proposal_in_progress`). Pair counters already advanced (attempts, `events`) stay, as in L24. Event caps (k+1, then k+2) give INCOMPLETE_CAP, never a rejection.
11. **Merge.** This branch changes `_move`, `_interval_move`, `_palette_move`, `_analyze`, `_partial_prefixes`, `_new_result`, `_progress`, the docstring, `LIMITATIONS` and the public function. W2 v005 or allk_v001 may touch the same defs, so the explicit merge must reconcile them hunk by hunk.
    - The new argument is appended last.
    - L-numbers L27-L30 may collide with numbers added on other branches.
    - The progress `module` string must be set once at the merge.
12. **Not done here.**
    - No distinct review; one is required by 0415 item 6.
    - No root interface binding or limits.
    - No physical parameter, target velocity, fit, ridge or threshold relaxation.
    - The historical sampler/result files, operator files, W2/all-k files and anything under `Universal Network Theory` are untouched.
    - Author/queue state for 0414 and W² is not mine to report: this file covers only 0415.

## diff -u v004 -> pair_v001

```diff
--- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_collective_worldline_0407/owned_collective_worldline_static_response_v004.py	2026-10-16 05:16:43.233434939 -0500
+++ /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/owned_collective_worldline_0407/owned_collective_worldline_static_response_pair_v001.py	2026-10-16 05:56:02.552564629 -0500
@@ -1,6 +1,19 @@
 """Owned collective static response by positive imaginary-time worldlines.
 
-UNT task 0407, version v004: v003 (sha256
+UNT task 0415, PAIR FEATURE BRANCH pair_v001: v004 (sha256
+6836577f0a887317077d379c35822dbe827b5cb27b6f864d0b445513a6c55cea, the accepted 0413 revision,
+preserved unchanged) plus ONLY the 0415 exact adjacent marked-event pair insertion/deletion
+move, its root-declared absolute move schedule (new required keyword-only argument
+pair_move_parameters; None disables the pair move) and the 0415 item 4 diagnostic corrections
+(changed-path versus identity acceptance across all moves, measured event counts, constant
+columns unassessable unless analytically exact invariants; L27-L30). Immutable feature file:
+integration order 0413 v004 -> {W2 sequential v005, 0414 all-k branch allk_v001, this pair
+branch} -> one explicit later merge (DELTA_0415_PAIR_V001.md carries the self-contained diff -u
+from v004). No physics, estimator, source, contact, read, interval density, warmup/measurement
+target or numerical threshold of v004 is changed. With pair_move_parameters None the RNG draw
+sequence and transition law are v004's (L29); _analyze is stricter (L28).
+
+v004 header (unchanged): UNT task 0407, version v004: v003 (sha256
 e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721, preserved unchanged) plus ONLY
 the 0413 cooperative budget / partial-return delta (budget_hook, progress_sink, committed
 measurement prefixes; L24-L26). No physics, estimator, move probability, warmup/measurement
@@ -72,6 +85,20 @@
 v004 addition (sha256 from bytes before writing; read-only; values never taken from it):
   * UNT_EXCHANGE/FROM_CODEX/0413_2026-10-16_preserve_collective_measurements_on_bounded_exit.md
     adfc9185663bb79880a85bc3bbd0194fa208df8aaf2404ca192499b3cddbf383   (items 1-5)
+pair_v001 additions (sha256 from bytes before writing; read-only; values never taken from them):
+  * UNT_EXCHANGE/FROM_CODEX/0415_2026-10-16_exact_event_pair_update_after_zero_event_samples.md
+    1283bb48baa48abfd45c80ebf2289f9bdc356f1cc7002d3ed2753ee070bd8a27   (read fully)
+  * helpers/coefficient_method/OWNED_WORLDLINE_ADJACENT_PAIR_INSERT_DELETE_PROPOSED_V001.txt
+    252fbeaa74eb3bf448ca088e3c460bd531f07f597d7dc839f57cbbee36fc5f8a   ("PAIR SPEC"; target
+    measure and exact MH ratio), with its distinct review
+    helpers/response_packet_audit/OWNED_ADJACENT_PAIR_INSERT_DELETE_DISTINCT_REVIEW_V001.json
+    9e444820713f9b10ccaf9cf2eb1fedb8eab2178d7ea85c2ee7382cbc5f35d18d   ("PAIR REVIEW")
+  * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v003.py
+    a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07   (ACTUAL operator v003,
+    read as text: _owner_id, _root_cuts, _reverse_channels, _reverse_descriptor; same public
+    names, signatures and record formats as v002)
+  * claude_artifacts/owned_collective_worldline_0407/ DELTA_0410_BUDGET_V004.md,
+    REVIEW_0410_BUDGET_V001.md, CONVENTIONS_0407_V003.md (base documentation)
 Style reference (read as text): claude_artifacts/scalar_metric_solve_0397/
 scalar_metric_particular_solve_v002.py (fail-closed result dict).
 
@@ -81,7 +108,10 @@
       volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
       diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
       caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
-      implicit_closure, budget_hook, progress_sink)
+      implicit_closure, budget_hook, progress_sink, pair_move_parameters)
+pair_v001 appends exactly one REQUIRED keyword-only argument without default,
+pair_move_parameters (None, or the root-declared absolute schedule and pair-kernel inputs; L27,
+L29); every other argument keeps its v004 meaning.
 The v002 signature is unchanged in v003 (no public argument is added in v003): the 0410 mode
 columns enter as fixed affine direction mappings inside derivative_coordinates (MODE SPEC
 s1 "minimal API delta"; L21), next to the unchanged tuple coordinate interface. v004 adds
@@ -205,6 +235,24 @@
   Item 4 (progress sink): _progress (stage, chain_start, sweep and stop records).
   Item 5 (partial return, ok False, no mixing analysis after a stop): _stopped,
     _partial_prefixes; the completed path through _analyze is unchanged.
+WHERE 0415 IS IMPLEMENTED (pair_v001, L27-L30)
+  Schedule (absolute pair / rotation / palette regrowth / full regrowth probabilities and the
+    insertion / deletion split, validated caller inputs): _admit_pair_move_parameters, _move.
+  Insertion (one dwell of length ell, sorted uniform pair density 2/ell^2, actual x->y mark,
+    actual unique compatible y->x mark, both proposal probabilities and actual weights, full
+    diagonal-action difference, full canonical return, full intermediate reads): _pair_insert.
+  Deletion (uniform over ALL K-1 nonwrapping adjacent positions, ineligible pairs rejected,
+    entire merged dwell length): _pair_delete. MH ratio: _pair_log_ratio.
+  Fixed state-independent local palette drawn BEFORE eligibility, never resampled: _pair_move.
+  Primitive identity (unique (kind, owner_id) at the source, reverse_kind plus the same full
+    owner_id selecting at most one record whose canonical target is verified; duplicate-key
+    assertion; p_b = 1 only after that check): _unique_mark, _pair_reverse_set.
+  Locality (reuse of the x dwell only after canonical-key equality; one intermediate
+    _segment_core; O(K) list splice, no replay): _pair_insert, _pair_delete.
+  Diagnostics (changed-path versus identity acceptance across ALL moves; measured event
+    counts; pair attempt / accept / insert / delete / no-reverse / rejection counts; constant
+    columns unassessable unless exact invariants; stuck chains by changed-path acceptance):
+    _move, _interval_move, _palette_move, the sampling loop, _analyze, _partial_prefixes.
 
 SEMANTICS. In the positive gauge G = (-1)^{sum_v q_v} (-e^{i phi_adm})^{N_S}
 (-e^{i phi_birth})^{N} (assembly lines 300-327, e^{-i theta} epsilon = -|epsilon| written
@@ -270,7 +318,13 @@
 proposal jump, held replay, move and sweep; progress records are O(1) in size (two small
 counter dicts), one per stage, chain start, completed sweep and stop. Per-chain arrays
 (measurement_sweeps * (n_u^2 + n_u + n_r + 1) numbers) are allocated once at chain start,
-as in v003; a stop returns views of their committed rows (no copy).
+as in v003; a stop returns views of their committed rows (no copy). pair_v001: an insertion
+costs one channel enumeration at the chosen dwell (palette_channels with local palettes, else
+primitive_channels), one _segment_core (canonical_state_key, diagonal_terms, read_rows and the
+callback reads) and one enumeration at the intermediate state, plus the reverse-pairing check
+(canonical keys of the sig-matching records) and an O(K) list splice; a deletion costs two
+enumerations (no _segment_core) and an O(K) splice. Neither replays or re-enumerates the
+unchanged path. The changed/identity and event counters are O(1) per move and measurement.
 
 LIMITATIONS: see the module-level string LIMITATIONS.
 """
@@ -370,7 +424,9 @@
     (at least one f = 1 so every length below beta has positive density). Rotation is a
     separate move with caller probability. All are source independent and symmetric. The
     same interval density is used by the global and the palette moves; the move type is
-    chosen with state-independent probabilities p_rot, p_palette, 1 - p_rot - p_palette.
+    chosen with state-independent probabilities p_rot, p_palette, 1 - p_rot - p_palette
+    (pair_v001: with pair_move_parameters not None the root-declared absolute probabilities
+    p_rot, p_palette, p_full and p_pair; L29).
 L11. H[N] weighting is the literal source functional H + sum n_alpha E_alpha, i.e.
     multiplier 1 + sum n_alpha wbar_alpha; it equals sum N_alpha wbar_alpha when the
     weights partition, which is checked to the caller's weight_partition tolerance at
@@ -386,7 +442,9 @@
     chains) no error band, replicate set or covariance is returned. Columns constant in
     every sample of every chain are listed; their zero spread is a sample statistic only.
     Mixing is judged on the primary linear columns (S, T, read averages, event count),
-    not separately on products.
+    not separately on products. pair_v001 (L28): such a constant column is UNASSESSABLE
+    (mixing cannot pass) unless it is an analytically exact invariant, and a chain without
+    a changed-path acceptance in measurement is stuck (mixing failed).
 L14. Caps (events per path, total events, sweeps, channel enumerations) end the whole
     computation with status incomplete and partial diagnostics; no estimate is returned
     and no path is ever rejected because of a cap. Restricted, lazy and verification
@@ -397,7 +455,8 @@
     origin or interval end equal to an event time, or rounding to beta) ends the
     computation as failed rather than perturbing times.
 L16. Not implemented: SPEC section 5 (HP implicit closure, cosmic preparation, initial
-    phase-kick observables), directed-worm or other efficiency moves, translation
+    phase-kick observables), directed-worm or other efficiency moves (pair_v001 adds ONLY
+    the 0415 adjacent pair insertion/deletion, L27), translation
     averaging, EH/vacuum matching, c_star, physical normalization and any numerical or
     physical input choice.
 L17. Operator exceptions are converted to status failed; the module's own programming
@@ -525,6 +584,9 @@
     returns no prefixes (a later validation failure can invalidate earlier samples); the
     per-chain counts stay in diagnostics. When the hook never returns True the run, its
     RNG draws, its transition law, _analyze and every threshold are exactly v003's.
+    (pair_v001: the transition law and draws are v004's only with pair_move_parameters None
+    or a pair move never selected, L29; _analyze carries the L28 corrections; a budget or
+    cap stop inside a pair proposal abandons it exactly like any other proposal.)
 L25. Progress sink (v004; 0413 item 4). progress_sink is None or a caller callable called
     synchronously as progress_sink(record=<dict>); its return value is ignored. Records are
     fresh dicts with keys "module", "event" ("stage" | "chain_start" | "sweep" | "stop"),
@@ -552,6 +614,93 @@
     with no returned result; only the sink records then identify the reached stage.
     Memory growth inside one call is not observable here. Earlier root failure evidence
     (runs V001 and V002) is neither touched nor reinterpreted.
+L27. Adjacent marked-event pair move (pair_v001; 0415, PAIR SPEC, PAIR REVIEW). Target: the
+    rooted closed-path density exp(-int D) prod_events W_mark w.r.t. ordered event times and
+    individual primitive marks (no 1/K!), the SAME target as every other move. Insertion on a
+    rooted path with K events: segment i uniform on 0..K (rng.integers), bounds lo = 0 or
+    t_{i-1}, hi = beta or t_i, ell = hi - lo, state x; forward mark a: x->y with p_a = W_a /
+    r_S(x) (_choose_channel, rate-proportional); intermediate y by _segment_core (full
+    canonical key, diagonal, reads and callback; nothing copied); reverse set R(a;x,y) =
+    records at y of kind reverse(a) with the SAME full owner_id and canonical target key equal
+    to key(x), p_b = W_b / r_back, r_back = sum_R W; then two independent uniforms on (lo,
+    hi), sorted (density 2/ell^2); x,y,x replaces the dwell x. Deletion on K events: K < 2
+    rejects; else i uniform on 0..K-2 (all K-1 nonwrapping adjacent positions, never
+    conditioned on eligibility); requires key(seg[i+2]) = key(seg[i]) and the stored marks
+    (kind, owner) of events i, i+1 to be a and a member b of R(a;x,y), else rejected (self
+    loop); ell = t_{i+2} (or beta) - t_{i-1} (or 0) spans all THREE old dwells; p_a and p_b
+    are recomputed from actual enumerations at x and y. MH (_pair_log_ratio):
+      log R_I = log(pD/pI) + 2 log ell - log 2 + log W_a + log W_b
+                - [log W_a - log r_S(x)] - [log W_b - log r_back] - (D_y - D_x)(t2 - t1),
+    insertion accepted with min(1, exp(log R_I)), deletion with min(1, exp(-log R_I)) for the
+    removed pair and the merged dwell. The K+1 segment choices and the K+1 adjacent positions
+    of the K+2-event path cancel; the palette weight omega_S and the absolute pair schedule
+    probability cancel. No beta^2, K!, degeneracy, survival or bridge factor enters. The
+    unsimplified terms are kept (rate-proportional choices would reduce W_aW_b/(p_ap_b) to
+    r_S(x) r_back). A forward mark without a same-owner compatible reverse is a rejection
+    (counted per kind; never an invented or summed reverse; existing moves keep that
+    primitive's dynamics). Every created event gets the v004 self-loop and grouped reverse
+    (L12) checks; the pair's gauge increments must net (0 mod 2, 0, 0). Equal or rounded
+    times end the run failed (L15), never jitter. Event caps are checked as for palette
+    events (incomplete, never a rejection; L14). Pair moves alone are NOT claimed irreducible
+    (rooted, nonwrapping; wrapping pairs reach through rotation; Birth-count, resource and
+    long-range changes through the global and palette regrowths, both kept at nonzero
+    probability). No claim that this move reaches the campaign mixing criterion.
+L28. Diagnostics (pair_v001; 0415 item 4, PAIR REVIEW qualification). Every move returns an
+    outcome "rotation" | "rejected" | "changed" | "identity". An accepted global or palette
+    regrowth is "identity" when it regenerated no event and replaced no non-held event (the
+    closed path is unchanged up to the v004 rotate-and-back time rounding), else "changed"; an
+    accepted pair insertion or deletion is always "changed"; a rotation changes only the
+    rooting (the measured S, T and time-averaged reads are rotation invariant) and is never
+    an acceptance, as in v004. accepted_regrowths / accepted_in_measurement keep their v004
+    meaning (every accepted proposal); changed_path_accepts(_in_measurement) and
+    identity_accepts(_in_measurement) split them. Measured event counts per chain (total,
+    max, zero-event samples) are counted at each committed measurement. _analyze: a chain
+    with zero changed-path acceptances in measurement is stuck (mixing failed); a primary
+    column constant in every sample of every chain is "unassessable" for sampling error and
+    autocorrelation (so mixing cannot pass and no error band is returned) UNLESS it is an
+    analytically exact invariant, which here means only contact columns T_ab with a or b a
+    coordinate whose per-event rho is identically zero by construction ("source",
+    "volume_multiplier", "pair_source_R", "pair_source_S", "source_direction"). A caller read
+    that is constant on the whole component is not certified as invariant here and makes
+    mixing unassessable (untrack it). rhat_max, min_batch_length_over_tau, the Sokal window,
+    the batch jackknife and every other numerical criterion are unchanged.
+L29. Schedule and RNG (pair_v001). pair_move_parameters is None (no pair move; the v004 move
+    law and draw sequence) or {"schedule": {"pair", "rotation", "palette_regrowth",
+    "full_regrowth"}, "insertion_probability", "deletion_probability", "local_palette"}, all
+    keys required, no defaults, no value chosen here. The four schedule entries are ABSOLUTE
+    probabilities: finite reals with pair, rotation and full_regrowth in (0, 1),
+    palette_regrowth in (0, 1) when palette_parameters is given and exactly 0 otherwise,
+    math.fsum of the four exactly 1; rotation must equal move_parameters
+    ['rotation_probability'] and palette_regrowth palette_parameters['selection_probability']
+    (one source of truth). insertion/deletion are in (0, 1) with math.fsum exactly 1.
+    local_palette True requires palette_parameters and draws S from its fixed weighted
+    permanent-label palette list (the regrowth's distribution) BEFORE eligibility, once per
+    attempt; local_palette False runs the base kernel on primitive_channels. Draw sequence:
+    the move-type uniform u is drawn as in v004; rotation iff u < p_rot, palette iff u < p_rot
+    + p_palette (both as in v004), global iff u < p_rot + p_palette + p_full, else pair (v004:
+    global for every u >= p_rot + p_palette). Rotation, palette and global moves then draw
+    exactly as in v004. A pair move draws, in order: S (one rng.random, local_palette only),
+    insert/delete (one rng.random); insertion: segment (one rng.integers(0, K+1)), forward
+    mark (one rng.random, only if r_S(x) > 0), two time uniforms (two rng.random, only after
+    the unique compatible reverse is found), MH (one rng.random, only if log R < 0);
+    deletion: position (one rng.integers(0, K-1), only if K >= 2), MH (one rng.random, only
+    if eligible and log R < 0). Floating partial sums of the schedule may differ from the
+    declared values by an ulp; each kernel is separately reversible, so this changes mixture
+    weights only, never the target.
+L30. Primitive identity (pair_v001; 0415 item 2; operator v003 _owner_id, _root_cuts,
+    _reverse_channels, _reverse_descriptor read as text). (kind, owner_id) must identify at
+    most one positive-rate record at a state: _unique_mark fails closed on a duplicate both
+    at the source (forward mark) and at the intermediate state (reverse kind plus the SAME
+    full owner_id), then verifies the canonical target key of the selected reverse record
+    against key(x). Birth/birth_rev owner_id carries the owner and the sorted cut / restored
+    cut labels, so distinct reconstructed matchings are distinct marks; edge and vertex
+    channels have unique source-state keys. Palette membership depends on (kind, owner_id)
+    only, so uniqueness within a palette enumeration equals uniqueness in the full one. p_b =
+    1 follows only from |R| = 1 after this check (computed as W_b / sum_R W, never inferred
+    from grouped adjoint equality). On deletion a stored mark's rate must equal the
+    re-enumerated record's rate exactly (same canonical state), else failed. Exact duplicate
+    native terms would need a stable operator ordinal, which operator v003 does not expose;
+    their appearance ends the run failed rather than being merged.
 """
 
 
@@ -924,6 +1073,110 @@
     }
 
 
+def _admit_pair_move_parameters(value, moves, palette, palette_given, failures):
+    """pair_v001 root-declared absolute schedule and pair-kernel inputs (0415; L27, L29) or None.
+
+    Every key is required and no value is chosen here. The four schedule probabilities are
+    absolute (not conditional on non-rotation) and must sum to exactly one under math.fsum;
+    rotation and palette regrowth must equal the existing move_parameters / palette_parameters
+    entries (one source of truth). palette_given tells whether palette_parameters was passed
+    (its admission may have failed, in which case the failure is already recorded).
+    """
+    if value is None:
+        return None
+    name = "pair_move_parameters"
+    keys = ("schedule", "insertion_probability", "deletion_probability", "local_palette")
+    mp = _admit_mapping(name, value, failures)
+    if mp is None or not _admit_required_keys(name, mp, keys, failures):
+        return None
+    good = True
+    sched_keys = ("pair", "rotation", "palette_regrowth", "full_regrowth")
+    sched_in = _admit_mapping(f"{name}['schedule']", mp["schedule"], failures)
+    sched = {}
+    if sched_in is None or not _admit_required_keys(f"{name}['schedule']", sched_in, sched_keys,
+                                                    failures):
+        good = False
+    else:
+        for k in sched_keys:
+            v = _admit_real(f"{name}['schedule']['{k}']", sched_in[k], failures)
+            if v is None:
+                good = False
+                continue
+            if k == "palette_regrowth" and not palette_given:
+                if v != 0.0:
+                    failures.append(
+                        f"input {name}['schedule']['palette_regrowth']: must be exactly 0 when "
+                        "palette_parameters is None (no palette regrowth move exists)"
+                    )
+                    good = False
+                    continue
+            elif not 0.0 < v < 1.0:
+                failures.append(f"input {name}['schedule']['{k}']: must lie in (0, 1)")
+                good = False
+                continue
+            sched[k] = v
+        if good and math.fsum([sched[k] for k in sched_keys]) != 1.0:
+            failures.append(
+                f"input {name}['schedule']: the four ABSOLUTE probabilities must sum to exactly 1 "
+                "under math.fsum (no renormalization is applied; L29)"
+            )
+            good = False
+    split = {}
+    for k in ("insertion_probability", "deletion_probability"):
+        v = _admit_real(f"{name}['{k}']", mp[k], failures)
+        if v is None:
+            good = False
+            continue
+        if not 0.0 < v < 1.0:
+            failures.append(f"input {name}['{k}']: must lie in (0, 1)")
+            good = False
+            continue
+        split[k] = v
+    if len(split) == 2 and math.fsum(list(split.values())) != 1.0:
+        failures.append(
+            f"input {name}: insertion_probability + deletion_probability must equal exactly 1 "
+            "under math.fsum (the split within pair updates; L29)"
+        )
+        good = False
+    local = mp["local_palette"]
+    if not isinstance(local, (bool, np.bool_)):
+        failures.append(f"input {name}['local_palette']: must be a bool")
+        good = False
+    elif bool(local) and not palette_given:
+        failures.append(
+            f"input {name}['local_palette']: True needs palette_parameters (the pair kernel "
+            "draws S from the same fixed permanent-label palette distribution; L29)"
+        )
+        good = False
+    if not good:
+        return None
+    if moves is not None and sched["rotation"] != moves["rotation_probability"]:
+        failures.append(
+            f"input {name}['schedule']['rotation'] = {sched['rotation']!r} differs from "
+            f"move_parameters['rotation_probability'] = {moves['rotation_probability']!r} (one "
+            "source of truth for the absolute rotation probability)"
+        )
+        good = False
+    if palette is not None and sched["palette_regrowth"] != palette["selection_probability"]:
+        failures.append(
+            f"input {name}['schedule']['palette_regrowth'] = {sched['palette_regrowth']!r} differs "
+            f"from palette_parameters['selection_probability'] = "
+            f"{palette['selection_probability']!r} (one source of truth)"
+        )
+        good = False
+    if not good or moves is None or (palette_given and palette is None):
+        return None
+    p_sel = 0.0 if palette is None else palette["selection_probability"]
+    return {
+        "schedule": dict(sched),
+        "insertion_probability": split["insertion_probability"],
+        "deletion_probability": split["deletion_probability"],
+        "local_palette": bool(local),
+        # Same left-to-right float expression as the v004 palette bound, extended once (L29).
+        "global_upper": moves["rotation_probability"] + p_sel + sched["full_regrowth"],
+    }
+
+
 def _admit_label_roles(sources, vgrad, tracked, coords, pair_cells, failures, unsupported):
     """0408/0409: no unsupported raw coarse rows, no duplicated whitened source allocation."""
     roles = [("source_coefficients", lbl) for lbl in sources]
@@ -1574,7 +1827,7 @@
     if sink is None:
         return
     record = {
-        "module": "owned_collective_worldline_static_response_v004",
+        "module": "owned_collective_worldline_static_response_pair_v001",
         "event": event,
         "stage": stage,
         "chain": None if diag is None else diag["chain"],
@@ -2384,24 +2637,35 @@
 
 
 def _move(run, path, rng, diag):
-    """Move type by state-independent probabilities: rotation, palette (if enabled), global."""
+    """Move type by state-independent probabilities: rotation, palette (if enabled), global.
+
+    pair_v001 (L28, L29): returns (path, outcome), outcome "rotation" | "rejected" | "changed"
+    | "identity". With pair_move_parameters the same uniform u selects the pair move when u >=
+    p_rot + p_palette + p_full (absolute schedule); otherwise the v004 branches draw unchanged.
+    """
     u = float(rng.random())
     p_rot = run["moves"]["rotation_probability"]
     if u < p_rot:
         diag["rotations"] += 1
-        return _rotate(run, path, float(rng.random()) * run["beta"]), False
+        return _rotate(run, path, float(rng.random()) * run["beta"]), "rotation"
     pal = run["palette"]
     if pal is not None and u < p_rot + pal["selection_probability"]:
         return _palette_move(run, path, rng, diag)
+    pm = run["pair_move"]
+    if pm is not None and not u < pm["global_upper"]:
+        return _pair_move(run, path, rng, diag)  # pair_v001 (L27, L29)
     return _interval_move(run, path, rng, diag)
 
 
 def _interval_move(run, path, rng, diag):
-    """Global interval regrowth with endpoint rejection (SPEC section 3; the v001 move)."""
+    """Global interval regrowth with endpoint rejection (SPEC section 3; the v001 move).
+
+    pair_v001: returns an outcome string (L28); draws and acceptance are v004's.
+    """
     beta = run["beta"]
     sel = _select_interval(run, rng, diag, "")
     if sel is None:
-        return path, False
+        return path, "rejected"
     origin, whole, length = sel
     rot = _rotate(run, path, origin)
     k = len(rot["times"])
@@ -2415,7 +2679,7 @@
     segs, evs, times = _ctmc_segment(run, rot["segments"][0], length, rng, k - m)
     if not _keys_equal(run, segs[-1]["key"], terminal["key"]):
         diag["endpoint_rejections"] += 1
-        return path, False
+        return path, "rejected"
     if _net_increments(evs) != _net_increments(rot["events"][:m]):
         raise _Stop(
             "failed",
@@ -2430,7 +2694,7 @@
         raise _Stop("failed", run["stage"], "log acceptance ratio not finite")
     if log_acc < 0.0 and not float(rng.random()) < math.exp(log_acc):
         diag["metropolis_rejections"] += 1
-        return path, False
+        return path, "rejected"
     new_path = {
         "segments": segs + rot["segments"][m + 1:],
         "events": evs + rot["events"][m:],
@@ -2440,7 +2704,11 @@
     back = beta - origin
     if not back < beta:
         back = 0.0
-    return _rotate(run, new_path, back), True
+    rotated = _rotate(run, new_path, back)
+    # pair_v001 (L28): no old and no new event in the interval leaves the closed path unchanged.
+    outcome = "identity" if m == 0 and not evs else "changed"
+    diag["interval_" + outcome + "_accepts"] += 1
+    return rotated, outcome
 
 
 def _choose_palette(pal, rng):
@@ -2481,12 +2749,13 @@
     r_S; held marks are replayed on the proposed state (absent or zero rate -> reject);
     endpoint mismatch rejects; log ratio int_I new(r_S - D) - int_I old(r_S - D) +
     sum_held log(W_new / W_old). Unconditioned generation plus rejection, never a bridge.
+    pair_v001: returns an outcome string (L28); draws and acceptance are v004's.
     """
     beta = run["beta"]
     owners = _choose_palette(run["palette"], rng)
     sel = _select_interval(run, rng, diag, "palette_")
     if sel is None:
-        return path, False
+        return path, "rejected"
     origin, whole, length = sel
     diag["palette_proposals"] += 1
     rot = _rotate(run, path, origin)
@@ -2556,7 +2825,7 @@
             )
         if not matches:
             diag["palette_held_rejections"] += 1  # illegal held event or zero held rate
-            return path, False
+            return path, "rejected"
         held_ch = matches[0]
         pending -= 1
         _count_new_event(run, len(evs) + 1 + pending + outside)
@@ -2575,7 +2844,7 @@
         current, t = y_seg, bound
     if not _keys_equal(run, current["key"], terminal["key"]):
         diag["palette_endpoint_rejections"] += 1
-        return path, False
+        return path, "rejected"
     if _net_increments(evs) != _net_increments(rot["events"][:m]):
         raise _Stop(
             "failed",
@@ -2600,7 +2869,7 @@
         raise _Stop("failed", run["stage"], "palette log acceptance ratio not finite")
     if log_acc < 0.0 and not float(rng.random()) < math.exp(log_acc):
         diag["palette_metropolis_rejections"] += 1
-        return path, False
+        return path, "rejected"
     new_path = {
         "segments": segs + rot["segments"][m + 1:],
         "events": evs + rot["events"][m:],
@@ -2611,7 +2880,287 @@
     back = beta - origin
     if not back < beta:
         back = 0.0
-    return _rotate(run, new_path, back), True
+    rotated = _rotate(run, new_path, back)
+    # pair_v001 (L28): identity when every old interval event was held and replayed and no
+    # member event was generated (the same marks, times and states as before).
+    outcome = "identity" if m == len(held) and len(evs) == len(held) else "changed"
+    diag["palette_" + outcome + "_accepts"] += 1
+    return rotated, outcome
+
+
+# ----------------------------------------------------------------------------------
+# pair_v001: exact adjacent marked-event pair insertion/deletion (0415; L27-L30)
+# ----------------------------------------------------------------------------------
+
+
+def _pair_channels(run, seg, owners):
+    """(channels, exit rate) of the pair kernel at a dwell: palette r_S(x) or full r(x).
+
+    owners None (local_palette False): the full primitive_channels enumeration; its exit rate
+    is also stored lazily on the segment (a state function, exactly as _seg_rate stores it).
+    owners a frozenset: operator palette_channels restricted to the fixed palette S (L19
+    membership; the same restricted enumeration as the palette regrowth).
+    """
+    if owners is None:
+        channels, exit_rate = _channels_at(run, seg["state"])
+        if seg["r"] is None:
+            seg["r"] = exit_rate
+        return channels, exit_rate
+    return _palette_channels(run, seg["state"], owners)
+
+
+def _unique_mark(run, channels, kind, owner, where):
+    """The ONE positive-rate record (kind, owner_id) among `channels`, or None (L30).
+
+    Duplicate-key assertion: more than one record with the same kind and the same full
+    owner_id at one state ends the run failed (the primitive would not be identified).
+    Palette membership depends on (kind, owner_id) only, so a palette enumeration holds
+    either every record of that key or none of them.
+    """
+    hits = [c for c in channels if c["kind"] == kind and _keys_equal(run, c["owner"], owner)]
+    if len(hits) > 1:
+        raise _Stop(
+            "failed",
+            run["stage"],
+            f"{where}: (kind {kind!r}, owner {owner!r}) matches {len(hits)} positive-rate "
+            "records at one state; the pair move needs a unique primitive identity "
+            "(duplicate-key assertion; a stable operator ordinal would be required; L30)",
+        )
+    return hits[0] if hits else None
+
+
+def _pair_reverse_set(run, y_channels, mark, x_key, where):
+    """R(a;x,y): records at y of kind reverse(a), a's FULL owner_id and target key(x) (L30).
+
+    reverse_kind plus the same owner_id selects at most one record at y (duplicate-key
+    assertion in _unique_mark); that record belongs to R only after its canonical target key
+    is verified equal to key(x). An empty list means no compatible same-owner reverse: no
+    reverse is invented and no grouped or summed rate is substituted.
+    """
+    rev_kind = run["kinds"][mark["kind"]][3]
+    rec = _unique_mark(run, y_channels, rev_kind, mark["owner"], where)
+    if rec is None or not _keys_equal(run, _target_key(run, rec), x_key):
+        return []
+    return [rec]
+
+
+def _pair_log_ratio(run, ell, w_a, r_x, w_b, r_back, d_x, d_y, dwell):
+    """log R_I of PAIR SPEC for marks a (t1) and b (t2) inside one dwell x of length ell (L27).
+
+    log R_I = log(pD/pI) + 2 log ell - log 2 + log W_a + log W_b - log p_a - log p_b
+              - (D_y - D_x)(t2 - t1),   p_a = W_a / r_S(x),  p_b = W_b / r_back.
+    Insertion accepts with min(1, exp(log R_I)); deletion of the same pair from the same
+    merged dwell with min(1, exp(-log R_I)). Kept unsimplified on purpose (PAIR SPEC).
+    """
+    pm = run["pair_move"]
+    log_p_a = math.log(w_a) - math.log(r_x)
+    log_p_b = math.log(w_b) - math.log(r_back)
+    terms = [
+        math.log(pm["deletion_probability"]) - math.log(pm["insertion_probability"]),
+        2.0 * math.log(ell),
+        -math.log(2.0),
+        math.log(w_a),
+        math.log(w_b),
+        -log_p_a,
+        -log_p_b,
+        -(d_y - d_x) * dwell,
+    ]
+    out = math.fsum(terms)
+    if not math.isfinite(out):
+        raise _Stop("failed", run["stage"], "pair log acceptance ratio not finite")
+    return out
+
+
+def _pair_move(run, path, rng, diag):
+    """Exact adjacent marked-event pair insertion/deletion (0415; PAIR SPEC; L27-L30).
+
+    With local_palette the palette S is drawn from the fixed palette_parameters distribution
+    BEFORE any eligibility is evaluated and is never resampled in this attempt; then
+    insertion or deletion by the fixed split. Each fixed-S kernel is reversible for the
+    unchanged target, so the state-independent mixture over S is (PAIR REVIEW).
+    """
+    pm = run["pair_move"]
+    diag["pair_attempts"] += 1
+    owners = _choose_palette(run["palette"], rng) if pm["local_palette"] else None
+    if float(rng.random()) < pm["insertion_probability"]:
+        return _pair_insert(run, path, rng, diag, owners)
+    return _pair_delete(run, path, rng, diag, owners)
+
+
+def _pair_insert(run, path, rng, diag, owners):
+    """Insert an actual x->y mark a at t1 and its unique compatible y->x mark b at t2 (L27).
+
+    The chosen dwell x (one of the K+1 rooted dwells) becomes x, y, x. The x segment record is
+    reused on both sides only because key(target of b) equals key(x) (verified); y gets ONE
+    full _segment_core. The rest of the path is spliced by O(K) list slicing, not replayed.
+    """
+    beta = run["beta"]
+    segments = path["segments"]
+    events = path["events"]
+    times = path["times"]
+    k = len(times)
+    diag["pair_insert_attempts"] += 1
+    i = int(rng.integers(0, k + 1))  # uniform over the K+1 rooted dwells
+    lo = 0.0 if i == 0 else times[i - 1]
+    hi = beta if i == k else times[i]
+    ell = hi - lo
+    x_seg = segments[i]
+    x_channels, r_x = _pair_channels(run, x_seg, owners)
+    if not r_x > 0.0:
+        diag["pair_insert_no_forward"] += 1  # no (member) primitive at x; never resampled
+        diag["pair_rejected"] += 1
+        return path, "rejected"
+    mark_a = _choose_channel(x_channels, r_x, rng)  # p_a = W_a / r_S(x)
+    _unique_mark(run, x_channels, mark_a["kind"], mark_a["owner"], "pair insertion source")
+    _count_new_event(run, k + 1)
+    y_seg = _segment_core(run, mark_a["target"])  # full key, diagonal, reads and callback
+    mark_a["key"] = y_seg["key"]
+    mark_a["has_key"] = True
+    _no_self_loop(run, x_seg, y_seg, mark_a)
+    y_channels, _ = _pair_channels(run, y_seg, owners)
+    rev = _pair_reverse_set(run, y_channels, mark_a, x_seg["key"], "pair insertion reverse")
+    if not rev:
+        kind = mark_a["kind"]
+        run["pair_no_reverse"][kind] = run["pair_no_reverse"].get(kind, 0) + 1
+        diag["pair_insert_no_reverse"] += 1  # rejected selection (self loop), not invented
+        diag["pair_rejected"] += 1
+        return path, "rejected"
+    mark_b = rev[0]
+    r_back = math.fsum([c["W"] for c in rev])  # |R| = 1 after the check, so p_b = 1 exactly
+    _reverse_check(run, x_seg, x_channels, mark_a, y_seg, y_channels)  # v004 L12 check
+    _count_new_event(run, k + 2)
+    ev_a = _event_from_channel(run, mark_a)
+    ev_b = _event_from_channel(run, mark_b)
+    if _net_increments([ev_a, ev_b]) != (0, 0, 0):
+        raise _Stop(
+            "failed",
+            run["stage"],
+            "an inserted forward/reverse pair has nonzero net gauge increments: primitive kind "
+            "labels are inconsistent with a state-function gauge (L2)",
+        )
+    t1 = lo + float(rng.random()) * ell
+    t2 = lo + float(rng.random()) * ell
+    if t2 < t1:
+        t1, t2 = t2, t1  # sorted pair: density 2 / ell^2 on the ordered triangle
+    if not (lo < t1 and t1 < t2 and t2 < hi):
+        raise _Stop(
+            "failed",
+            run["stage"],
+            "pair insertion times coincide with each other or with a dwell boundary in "
+            "floating point; computation ended rather than perturbing times (L15)",
+        )
+    log_r = _pair_log_ratio(run, ell, mark_a["W"], r_x, mark_b["W"], r_back,
+                            x_seg["D"], y_seg["D"], t2 - t1)
+    if log_r < 0.0 and not float(rng.random()) < math.exp(log_r):
+        diag["pair_insert_metropolis_rejections"] += 1
+        diag["pair_rejected"] += 1
+        return path, "rejected"
+    new_path = {
+        "segments": segments[:i + 1] + [y_seg, x_seg] + segments[i + 1:],
+        "events": events[:i] + [ev_a, ev_b] + events[i:],
+        "times": times[:i] + [t1, t2] + times[i:],
+    }
+    diag["pair_insert_accepted"] += 1
+    diag["pair_accepted"] += 1
+    return new_path, "changed"
+
+
+def _pair_delete(run, path, rng, diag, owners):
+    """Delete adjacent events i, i+1 that form a same-owner forward/reverse pair (L27).
+
+    i is uniform over ALL K-1 nonwrapping adjacent positions (never conditioned on
+    eligibility); an ineligible pair is a rejection (self loop). The merged dwell spans the
+    three old dwells x, y, z (ell from t_{i-1} or 0 to t_{i+2} or beta). p_a and p_b are
+    recomputed from actual enumerations at x and y under the same selection rule.
+    """
+    beta = run["beta"]
+    segments = path["segments"]
+    events = path["events"]
+    times = path["times"]
+    k = len(times)
+    diag["pair_delete_attempts"] += 1
+    if k < 2:
+        diag["pair_delete_too_few_events"] += 1
+        diag["pair_rejected"] += 1
+        return path, "rejected"
+    i = int(rng.integers(0, k - 1))  # uniform over the K-1 nonwrapping adjacent positions
+    x_seg = segments[i]
+    y_seg = segments[i + 1]
+    z_seg = segments[i + 2]
+    ev_a = events[i]
+    ev_b = events[i + 1]
+    rev_kind = run["kinds"][ev_a["kind"]][3]
+    if not (ev_b["kind"] == rev_kind and _keys_equal(run, ev_b["owner"], ev_a["owner"])
+            and _keys_equal(run, z_seg["key"], x_seg["key"])):
+        diag["pair_delete_ineligible"] += 1  # not b in R(a;x,y) with z = x: self loop
+        diag["pair_rejected"] += 1
+        return path, "rejected"
+    if owners is not None and (
+        _record_groups(run, ev_a["kind"], ev_a["owner"]).isdisjoint(owners)
+        or _record_groups(run, ev_b["kind"], ev_b["owner"]).isdisjoint(owners)
+    ):
+        diag["pair_delete_palette_nonmember"] += 1  # a mark outside S: self loop
+        diag["pair_rejected"] += 1
+        return path, "rejected"
+    if not (z_seg["D"] == x_seg["D"] and bool(np.array_equal(z_seg["Da"], x_seg["Da"]))
+            and bool(np.array_equal(z_seg["row"], x_seg["row"]))):
+        raise _Stop(
+            "failed",
+            run["stage"],
+            "two dwells with equal canonical keys carry different diagonal energy, source "
+            "derivatives or reads; the x dwell cannot represent the merged interval (L30)",
+        )
+    x_channels, r_x = _pair_channels(run, x_seg, owners)
+    mark_a = _unique_mark(run, x_channels, ev_a["kind"], ev_a["owner"], "pair deletion source")
+    if mark_a is None or not _keys_equal(run, _target_key(run, mark_a), y_seg["key"]):
+        raise _Stop(
+            "failed",
+            run["stage"],
+            f"stored event (kind {ev_a['kind']!r}, owner {ev_a['owner']!r}) is not an actual "
+            "positive-rate record from its source dwell to the next dwell (path/operator "
+            "inconsistency; L30)",
+        )
+    y_channels, _ = _pair_channels(run, y_seg, owners)
+    rev = _pair_reverse_set(run, y_channels, mark_a, x_seg["key"], "pair deletion reverse")
+    if not rev:
+        raise _Stop(
+            "failed",
+            run["stage"],
+            f"stored event (kind {ev_b['kind']!r}, owner {ev_b['owner']!r}) is not an actual "
+            "positive-rate record back to the source state (path/operator inconsistency; L30)",
+        )
+    mark_b = rev[0]
+    r_back = math.fsum([c["W"] for c in rev])
+    if mark_a["W"] != ev_a["W"] or mark_b["W"] != ev_b["W"]:
+        raise _Stop(
+            "failed",
+            run["stage"],
+            "a stored mark rate differs from the re-enumerated record at the same canonical "
+            "state (rates must be state functions; L30)",
+        )
+    if _net_increments([ev_a, ev_b]) != (0, 0, 0):
+        raise _Stop(
+            "failed",
+            run["stage"],
+            "a deletable forward/reverse pair has nonzero net gauge increments (L2)",
+        )
+    lo = 0.0 if i == 0 else times[i - 1]
+    hi = beta if i + 2 == k else times[i + 2]
+    ell = hi - lo  # the ENTIRE merged dwell: all three old dwells x, y, z
+    log_r = -_pair_log_ratio(run, ell, mark_a["W"], r_x, mark_b["W"], r_back,
+                             x_seg["D"], y_seg["D"], times[i + 1] - times[i])
+    if log_r < 0.0 and not float(rng.random()) < math.exp(log_r):
+        diag["pair_delete_metropolis_rejections"] += 1
+        diag["pair_rejected"] += 1
+        return path, "rejected"
+    new_path = {
+        "segments": segments[:i + 1] + segments[i + 3:],
+        "events": events[:i] + events[i + 2:],
+        "times": times[:i] + times[i + 2:],
+    }
+    diag["pair_delete_accepted"] += 1
+    diag["pair_accepted"] += 1
+    return new_path, "changed"
 
 
 def _initial_path(run, spec):
@@ -2770,7 +3319,11 @@
 
 
 def _analyze(run, series, errp, n_u):
-    """Batch jackknife, between-chain spread, autocorrelation and R-hat (SPEC section 7)."""
+    """Batch jackknife, between-chain spread, autocorrelation and R-hat (SPEC section 7).
+
+    pair_v001 (L28): constant non-invariant columns are unassessable, stuck chains are judged
+    by changed-path acceptances, measured event counts are reported; thresholds unchanged.
+    """
     n_r = run["n_r"]
     n_chains = len(series)
     n_meas = series[0]["score"].shape[0]
@@ -2808,13 +3361,25 @@
     tau_table = np.full((n_chains, len(names)), np.nan)
     rhat_values = np.full(len(names), np.nan)
     constant_columns = []
+    # pair_v001 (L28): a contact column T_ab whose a or b coordinate has per-event rho
+    # identically zero by construction (_event_from_channel sets rho only for lapse and
+    # lapse-direction coordinates) is an exact invariant, T_ab = 0 in every sample. Any other
+    # column constant in every sample of every chain is UNASSESSABLE (zero spread is not
+    # evidence of mixing or of a zero sampling error).
+    rho_zero = [c[0] not in ("lapse", "lapse_direction") for c in run["supported_coords"]]
+    exact_invariant_columns = []
     for col in range(len(names)):
         r_status, r_val = _rhat(prim[:, :, col])
         if r_val is not None:
             rhat_values[col] = r_val
         if r_status == "constant":
-            column_status.append("constant")
-            constant_columns.append(names[col])
+            name = names[col]
+            if name[0] == "contact" and (rho_zero[name[1][0]] or rho_zero[name[1][1]]):
+                column_status.append("exact_invariant")
+                exact_invariant_columns.append(name)
+            else:
+                column_status.append("unassessable")
+                constant_columns.append(name)
             continue
         status = "passed"
         if r_status == "unassessable":
@@ -2831,7 +3396,9 @@
                 status = "unassessable"
         column_status.append(status)
     stuck = [i for i, ser in enumerate(series) if ser["accepted_in_measurement"] == 0]
-    if stuck or "failed" in column_status:
+    # pair_v001 (L28): identity acceptances never establish movement.
+    stuck_changed = [i for i, ser in enumerate(series) if ser["changed_in_measurement"] == 0]
+    if stuck or stuck_changed or "failed" in column_status:
         mixing = "failed"
     elif n_chains < 2 or "unassessable" in column_status:
         mixing = "unassessable"
@@ -2843,13 +3410,29 @@
         lin = np.concatenate([ser["score"], ser["reads"]], axis=1)
         bm = lin.reshape(n_batch, blen, lin.shape[1]).mean(axis=1)
         per_chain_batch_se.append(np.sqrt(bm.var(axis=0, ddof=1) / n_batch))
+    measured_events = []  # pair_v001 (L28): measured event counts per chain
+    for ser in series:
+        ev = ser["events"]
+        measured_events.append({
+            "chain": ser["chain"],
+            "samples": int(ev.shape[0]),
+            "min": int(ev.min()),
+            "max": int(ev.max()),
+            "mean": float(ev.mean()),
+            "zero_event_samples": int(np.count_nonzero(ev == 0)),
+        })
 
     mixing_report = {
         "status": mixing,
         "stuck_chains_zero_accepted_regrowths_in_measurement": stuck,
+        "stuck_chains_zero_changed_path_accepts_in_measurement": stuck_changed,
+        "changed_path_accepts_in_measurement": [ser["changed_in_measurement"] for ser in series],
+        "identity_accepts_in_measurement": [ser["identity_in_measurement"] for ser in series],
+        "measured_event_counts": measured_events,
         "primary_columns": names,
         "column_status": column_status,
         "constant_columns": constant_columns,
+        "exact_invariant_columns": exact_invariant_columns,
         "rhat": rhat_values,
         "integrated_autocorrelation_time": tau_table,
         "batch_length": blen,
@@ -2862,7 +3445,10 @@
         "note": (
             "statistical/assessed diagnostics, not a mixing-time bound; per-chain batch "
             "errors are within-chain statistics and are not an error band unless status "
-            "is 'passed'"
+            "is 'passed'; pair_v001 (L28): constant_columns are unassessable (zero spread is "
+            "not mixing evidence), exact_invariant_columns are contact columns identically "
+            "zero by construction, and a chain without a changed-path acceptance in "
+            "measurement is stuck (identity acceptances never establish movement)"
         ),
     }
 
@@ -3084,6 +3670,10 @@
             "burn_in_sweeps_completed": diag["burn_in_sweeps_completed"],
             "sweeps_completed": diag["sweeps_completed"],
             "accepted_in_measurement": diag["accepted_in_measurement"],
+            # pair_v001 (L28): changed-path versus identity acceptances and measured events
+            "changed_path_accepts_in_measurement": diag["changed_path_accepts_in_measurement"],
+            "identity_accepts_in_measurement": diag["identity_accepts_in_measurement"],
+            "measured_zero_event_samples": diag["measured_zero_event_samples"],
             "score": entry["score"][:n],
             "contact": entry["contact"][:n],
             "reads": entry["reads"][:n],
@@ -3155,7 +3745,19 @@
             ),
             "moves": (
                 "rotation (p_rot), additive blocked palette (p_palette, PALETTE note) and global "
-                "interval regrowth (1 - p_rot - p_palette > 0), all state independent"
+                "interval regrowth (1 - p_rot - p_palette > 0), all state independent; "
+                "pair_v001: with pair_move_parameters the ABSOLUTE schedule p_rot, p_palette, "
+                "p_full > 0 and p_pair adds the exact adjacent pair insertion/deletion (L27, "
+                "L29); every move returns rotation | rejected | changed | identity (L28)"
+            ),
+            "pair_move": (
+                "pair_v001 (L27): target exp(-int D) prod W_mark on rooted ordered times and "
+                "primitive marks; insertion in a uniform dwell (K+1), p_a = W_a/r_S(x), unique "
+                "same-owner reverse b with verified target x, p_b = W_b/r_back, sorted uniform "
+                "pair density 2/ell^2; deletion uniform over all K-1 nonwrapping positions, "
+                "ineligible pairs rejected, merged ell over three dwells; log R_I = log(pD/pI) + "
+                "2 log ell - log 2 + log W_a + log W_b - log p_a - log p_b - (D_y - D_x)(t2 - "
+                "t1), deletion uses -log R_I; local palettes drawn before eligibility"
             ),
             "positive_gauge": (
                 "G = (-1)^{sum q} (-e^{i admission_phase})^{N_S} (-e^{i birth_phase})^{N}; "
@@ -3240,6 +3842,7 @@
     implicit_closure,
     budget_hook,
     progress_sink,
+    pair_move_parameters,
 ):
     """Static joint source Hessians of the owned collective by positive worldline sampling.
 
@@ -3324,6 +3927,16 @@
         progress_sink(record=dict) with small stage / chain / completed-warmup /
         completed-measurement / move-counter records; return value ignored; flushing is
         the sink's; a raise is "failed".
+      pair_move_parameters (pair_v001, 0415; L27-L30): None (no pair move; v004 move law and
+        draw sequence), or {"schedule": {"pair": (0,1), "rotation": (0,1) equal to
+        move_parameters['rotation_probability'], "palette_regrowth": (0,1) equal to
+        palette_parameters['selection_probability'] (exactly 0 when palette_parameters is
+        None), "full_regrowth": (0,1)} with math.fsum of the four ABSOLUTE probabilities
+        exactly 1; "insertion_probability": (0,1), "deletion_probability": (0,1) with
+        math.fsum exactly 1; "local_palette": bool (True draws the pair kernel's palette S
+        from palette_parameters' fixed weighted list before eligibility; requires
+        palette_parameters)}. Root's declared trial: 0.50 / 0.10 / 0.35 / 0.05 and 0.50 /
+        0.50 with local palettes, passed by the caller; nothing is chosen here.
 
     Returns a dict: ok, status, incomplete_reason (v004), partial (v004; committed prefixes
     as diagnostics on an incomplete stop, else None; L24), stage_reached, failures, flags,
@@ -3335,7 +3948,11 @@
     score_covariance, contact_mean, F (None), F_u, F_uu, read_means, read_mean_responses,
     per_chain, mean/max events per path, samples}, errors (only when mixing passed),
     mixing, diagnostics, conventions, scope, limitations. "ok" is True only when status is
-    "complete", every requested direction is supported and mixing "passed". With mode
+    "complete", every requested direction is supported and mixing "passed". pair_v001: mixing
+    adds stuck_chains_zero_changed_path_accepts_in_measurement, changed/identity acceptances
+    in measurement, measured_event_counts and exact_invariant_columns (L28); per-chain
+    diagnostics add the changed/identity, measured-event and pair counters; diagnostics add
+    pair_no_reverse_by_kind; inputs echo pair_move_parameters. With mode
     directions and the callback, tracked_read_labels (output) ends with the nine reserved
     uniform moment labels (L23).
     """
@@ -3395,6 +4012,9 @@
             "selection probability (blocked moves alone are not claimed irreducible)"
         )
         palette = None
+    pair_mv = _admit_pair_move_parameters(  # pair_v001 (L27, L29)
+        pair_move_parameters, moves, palette, palette_parameters is not None, failures
+    )
     caps_in = _admit_caps(caps, failures)
     burn = _admit_int("burn_in_sweeps", burn_in_sweeps, 0, failures)
     n_meas = _admit_int("measurement_sweeps", measurement_sweeps, 1, failures)
@@ -3441,6 +4061,12 @@
         "numerical_tolerances": tol,
         "budget_hook": None if budget_hook is None else ("callable" if hook_ok else "rejected"),
         "progress_sink": None if progress_sink is None else ("callable" if sink_ok else "rejected"),
+        "pair_move_parameters": None if pair_mv is None else {  # pair_v001 (L29)
+            "schedule": dict(pair_mv["schedule"]),
+            "insertion_probability": pair_mv["insertion_probability"],
+            "deletion_probability": pair_mv["deletion_probability"],
+            "local_palette": pair_mv["local_palette"],
+        },
     }
     if failures:
         result["status"] = "failed"
@@ -3485,6 +4111,9 @@
         "energy_cells": None,
         "group": None,
         "palette": palette,
+        "pair_move": pair_mv,  # pair_v001 (L27, L29); None disables the pair move
+        "pair_no_reverse": {},  # pair_v001: forward marks without a same-owner reverse, by kind
+        "supported_coords": None,  # pair_v001: set before _analyze (L28)
         "kinds": kinds,
         "gauge": _gauge_table(kinds, phases),
         "tol": tol,
@@ -3515,6 +4144,7 @@
             "counters": dict(run["counters"]),
             "chains": [dict(d) for d in chain_diag],
             "zero_rate_directions": sorted(map(repr, run["zero_rate_directions"])),
+            "pair_no_reverse_by_kind": dict(run["pair_no_reverse"]),  # pair_v001 (L27)
         }
 
     def _stopped(stop):
@@ -3712,6 +4342,34 @@
                 "sweeps_completed": 0,
                 "measurements": 0,
                 "burn_in_sweeps_completed": 0,  # v004 (L25)
+                # pair_v001 (L28): changed-path versus identity acceptance, all moves
+                "changed_path_accepts": 0,
+                "identity_accepts": 0,
+                "changed_path_accepts_in_measurement": 0,
+                "identity_accepts_in_measurement": 0,
+                "interval_changed_accepts": 0,
+                "interval_identity_accepts": 0,
+                "palette_changed_accepts": 0,
+                "palette_identity_accepts": 0,
+                # pair_v001 (L28): measured event counts (committed samples only)
+                "measured_events_total": 0,
+                "measured_events_max": 0,
+                "measured_zero_event_samples": 0,
+                # pair_v001 (L27): pair attempt / insert / delete / no-reverse / reject counts
+                "pair_attempts": 0,
+                "pair_accepted": 0,
+                "pair_rejected": 0,
+                "pair_insert_attempts": 0,
+                "pair_insert_no_forward": 0,
+                "pair_insert_no_reverse": 0,
+                "pair_insert_metropolis_rejections": 0,
+                "pair_insert_accepted": 0,
+                "pair_delete_attempts": 0,
+                "pair_delete_too_few_events": 0,
+                "pair_delete_ineligible": 0,
+                "pair_delete_palette_nonmember": 0,
+                "pair_delete_metropolis_rejections": 0,
+                "pair_delete_accepted": 0,
             }
             chain_diag.append(diag)
             run["stage"] = f"chain {c} start"
@@ -3730,6 +4388,8 @@
                 "events": n_events,
                 "measurements_committed": 0,
                 "accepted_in_measurement": 0,
+                "changed_in_measurement": 0,  # pair_v001 (L28)
+                "identity_in_measurement": 0,  # pair_v001 (L28)
             }
             series.append(entry)
             _progress(run, "chain_start", run["stage"], diag, None)  # v004 (L25)
@@ -3748,12 +4408,17 @@
                     if mv > 0:
                         _budget_check(run, "between", "moves")  # v004 (L24)
                     run["move_open"] = True  # v004: a stop now abandons this proposal
-                    path, accepted = _move(run, path, rng, diag)
+                    path, outcome = _move(run, path, rng, diag)
                     run["move_open"] = False
-                    if accepted:
+                    if outcome in ("changed", "identity"):
                         diag["accepted_regrowths"] += 1
                         if measuring:
                             diag["accepted_in_measurement"] += 1
+                        # pair_v001 (L28): split every acceptance into changed / identity
+                        kept = "changed_path" if outcome == "changed" else "identity"
+                        diag[kept + "_accepts"] += 1
+                        if measuring:
+                            diag[kept + "_accepts_in_measurement"] += 1
                 if measuring:
                     i = sweep - burn
                     s_vec, t_mat, r_vec, k = _measure(run, path)
@@ -3763,11 +4428,18 @@
                     n_events[i] = k
                     entry["measurements_committed"] += 1  # v004: whole tuple committed
                     diag["measurements"] += 1
+                    diag["measured_events_total"] += k  # pair_v001 (L28)
+                    if k > diag["measured_events_max"]:
+                        diag["measured_events_max"] = k
+                    if k == 0:
+                        diag["measured_zero_event_samples"] += 1
                 else:
                     diag["burn_in_sweeps_completed"] += 1  # v004 (never a measured sample)
                 diag["sweeps_completed"] += 1
                 _progress(run, "sweep", run["stage"], diag, None)  # v004 (L25)
             entry["accepted_in_measurement"] = diag["accepted_in_measurement"]
+            entry["changed_in_measurement"] = diag["changed_path_accepts_in_measurement"]
+            entry["identity_in_measurement"] = diag["identity_accepts_in_measurement"]
     except _Stop as stop:
         return _stopped(stop)  # v004: prefixes kept on incomplete stops (L24)
 
@@ -3804,6 +4476,7 @@
         ser["score"] = ser["score"][:, sup]
         ser["contact"] = ser["contact"][:, sup][:, :, sup]
     n_us = len(supported)
+    run["supported_coords"] = [coords[i] for i in supported]  # pair_v001 (L28)
     point, per_chain, mixing, errors = _analyze(run, series, errp, n_us)
     beta_f = run["beta"]
     all_events = np.concatenate([ser["events"] for ser in series])
@@ -3847,7 +4520,19 @@
     if mixing["constant_columns"]:
         result["flags"].append(
             "constant columns (no sample variation in any chain) are listed in "
-            "mixing.constant_columns; their zero spread is not evidence of mixing"
+            "mixing.constant_columns; their zero spread is not evidence of mixing and they "
+            "are unassessable for sampling error and autocorrelation (pair_v001, L28)"
+        )
+    if mixing["stuck_chains_zero_changed_path_accepts_in_measurement"]:
+        result["flags"].append(
+            "chains without any changed-path acceptance in measurement (identity acceptances "
+            "do not count as movement) are listed in mixing; mixing failed (pair_v001, L28)"
+        )
+    if run["pair_no_reverse"]:
+        result["flags"].append(
+            "pair insertion found forward marks without a same-owner compatible reverse "
+            f"(by kind: {dict(run['pair_no_reverse'])!r}); those selections were rejected, "
+            "never paired with an invented or summed reverse (pair_v001, L27)"
         )
     if mixing["status"] != "passed":
         result["flags"].append(
```
