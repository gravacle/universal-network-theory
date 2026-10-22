# FIX_DELTA 0407 V002: owned collective worldline static response

Author: fix author for UNT 0407 (Claude, static only). Nothing was imported, executed or sampled. v001 is preserved byte-identical.

| File | Bytes | Lines | sha256 |
|---|---:|---:|---|
| owned_collective_worldline_static_response_v001.py (unchanged) | 83799 | 1921 | 0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f |
| owned_collective_worldline_static_response_v002.py (new, exclusive create) | 135141 | 2946 | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 |

All binding inputs matched their stated sha256, computed from bytes before reading: 0407, SPEC, operator addendum, operator contract, 0406, register spec, proper-time V002, partial Legendre, Kubo/zero-mode, the PALETTE note and its distinct review, the root adapter, 0408, 0409, the registration and its whitening companion. Only lines 300-327 of the assembly note were read.

The operator file `owned_parent_operator_v001.py` matched 27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6 and was read as text. No operator v002 existed on disk. The root adapter was read as text only.

Line numbers below refer to v002 unless marked v001.

## Issue 1: model-level member check (blocking): FIXED

- **Defect confirmed.** The operator text at v001 L548-584 (`_admit_model`) admits:
  - any real theta on every edge key,
  - complex kappa per vertex and complex epsilon per owner,
  - real h, t and g of either sign.

  v001 delegated the member check to `validate_owned_model`, which does not perform it.
- **Approach.** Option (b): the module checks the caller's model mapping directly against the contract s3/s10 coefficient schema, independent of which states the chains visit.
  - `_model_schema` (L468) defines the schema: the 13 diagonal scalars plus the profiles h, t, theta, g, kappa and epsilon.
  - `_profile_entries` (L1058) yields every supplied entry. A Mapping is read entry by entry. A bare scalar is treated as a declared uniform value. A callable is admitted only through its declared uniform attribute `value`, which is the root adapter's `UniformEdgeProfile`.
  - `_model_member_check` (L1082) checks:
    - h > 0, t > 0 and theta == 0 exactly, for every edge key including newborn/child edges;
    - g > 0;
    - kappa nonzero, with |kappa - |kappa| e^{i admission_phase}| <= gauge_phase*|kappa|, for every vertex;
    - the same test for epsilon against birth_phase, for every owner;
    - every diagonal scalar is a finite real.
- **Placement.** The new stage "member_check" (L2734-2753) runs after `validate_owned_model` returns a context and before any initial path or sampling. Any violation, missing or unknown schema key, or profile it cannot evaluate gives status `unsupported`. `result["member_check"]` (L2412) reports the status, the profile forms and up to 20 listed problems.
- **Second line kept.** `_channels_from_records` (L1243) still checks every primitive at every visited state. It now also covers the restricted palette enumerations.
- **Documentation.** L2 is rewritten (L204-226). Also updated: the module SEMANTICS (L132ff), WHERE (L109ff) and the public docstring (L2506-2513).
- **Literal choices** (recorded in L2):
  - A zero kappa or epsilon is unsupported because its phase is undefined; the member requires nonzero common kappa and Birth amplitude.
  - theta must be exactly 0.0.
  - A callable profile is trusted through its declared `value`. Checking it otherwise would mean enumerating all 9L^6 potential endpoint pairs, which 0408/0409 forbid.

## Issue 2: 0408 blocked-palette move: IMPLEMENTED (additive)

- **Move selection.** The dispatcher `_move` (L1879) chooses between three moves with state-independent probabilities:
  - rotation, with probability p_rot;
  - the palette move, with probability p_palette;
  - the V001 global regrowth `_interval_move` (L1892), with probability 1 - p_rot - p_palette.

  Admission requires p_rot + p_palette < 1 (L2605ff), so the global moves always keep nonzero selection probability.
- **New public argument `palette_parameters`.** It is None or {selection_probability, palettes [(weight, original owner labels)], verify_against_full_enumeration}, admitted by `_admit_palette_parameters` (L605). The binding stage (L2755ff) reads the owner groups from graph0["A"], ["B"] and ["slots"], and rejects palette labels that are not original owners.
- **Membership from permanent labels.** `_record_groups` (L1318) maps each primitive to owner groups from the operator owner_id:
  - Birth and its reverse map to owner j.
  - Site events map to the fixed group of their vertex; a newborn belongs to the group of its original owner.
  - Edge events map to both endpoint groups.

  Forward and reverse primitives carry the same owner_id, so membership is reversal invariant. No state-dependent support weight or guard enters it.
- **The move (`_palette_move`, L1969).**
  - The palette is chosen by `_choose_palette` (L1939). The interval uses the same source-independent density as the global move (`_select_interval`, L1856).
  - Outside-palette events in the interval are held, keeping their times and their (kind, owner_id) descriptors.
  - Between held marks only member channels run, with their actual rates and r_S, via `_palette_channels` (L1385) on the run-time `owner_restricted_channels`.
  - Each held mark is replayed on the proposed state through the restricted enumeration on its own groups. The proposal is rejected when the record is absent (a guard, newborn/donor image or eligibility failure) or has zero rate. The replay gets the same self-loop and reverse-pairing checks as a sampled event.
  - An endpoint mismatch rejects.
  - The log ratio is int_I new(r_S - D) - int_I old(r_S - D) + sum_held log(W_new/W_old).
  - The proposal is never renormalized as a conditioned bridge. The gauge net-increment check is kept.
- **Restricted enumeration.**
  - Non-member records returned by the operator are dropped and counted (`restricted_nonmember_records_dropped`).
  - With verify_against_full_enumeration=True, every restricted enumeration is compared as a multiset against the members of `primitive_channels` (`_record_identity`, L1346).
  - Caps apply as before (`_count_new_event`, L1949; L14); a cap ends the run, it never rejects a proposal.
- **Lazy exit rates.** Segments created by palette moves get their full exit rate only when a global move needs it (`_seg_rate` L1658, `_clipped_integral` L1782, `_ctmc_segment` L1807-1811). In `_interval_move` the old-path integral is now computed after the endpoint check (L1919), which only avoids wasted enumeration.
- **What is not done.** No dependency cache is implemented. No fast-mixing or irreducibility claim is made for blocked moves alone. Both points are in L19 (L305) and COST.
- **Assumed API.** The 0405 module A v002 was not on disk, so the restricted enumeration is assumed as `owner_restricted_channels(*, context, state, owners)`, where owners is a frozenset of original owner labels and the records use the primitive_channels schema. It is required only when the palette move is enabled (`_admit_operator_api`, L446). The final checker must reconcile the name and signature (L1).
- **Descriptor uniqueness.** The held descriptor (kind, owner_id) identifies at most one record per state in the operator v001 structure:
  - one flip per edge;
  - at most one hop per edge;
  - one Bind or admission per vertex, with the kind fixing the direction;
  - one Birth per (cut, owner);
  - one reverse per restored cut.

  More than one match at run time returns `failed`.

## Issue 3: 0409 operator API compatibility and the root adapter path: FIXED

- **Actual operator API** (L66ff, L1):
  - `primitive_channels` records of kind "diag" are skipped (L1255, L1374).
  - `energy_weights` tuples aligned with `context.energy_cells` are read by `_energy_weights` (L1181).
  - The diagonal value is the "diag" record `amplitude` (`_diagonal_at`, L1417).
  - `read_rows` returns {labels, values, presence} arrays with state-independent labels. They are indexed once by `_index_read_labels` (L1457) and validated by `_read_array` (L1488). A referenced label that is not an operator label now fails at the first read, where v001 silently treated it as 0.
  - lapse_factors must cover exactly `context.energy_cells` (binding stage, L2755ff).
- **Root adapter, called with its ACTUAL signatures** (L92ff) through the new required argument `diagonal_read_source_callback`. This replaces v001 `extra_diagonal_reads`. Admission is by `_admit_pair_callback` (L548) and `_admit_pair_sources` (L507).
  - `adapted_moment_reads(operator_module=..., context=..., state=..., binding=...)` and `pair_source_hamiltonian(reads=..., j_R=..., j_S=...)` are called in `_reads_at` (L1541).
  - `raw_to_whitened_sources(j_R_raw=..., j_S_raw=...)` is called once at the binding stage (L2788-2803) when source_frame is "raw".
  - The binding's graph0 and registration must be the SAME objects passed to the operator, so ports, cells and presence have one source of truth.
- **Adapter functions the sampler does not call.** These belong to the root runner: `label_metadata`, `make_port_order`, `build_inputs`, `bind_context`, `central_covariance`. The sampler validates the model itself through the operator, with the same objects. `UniformEdgeProfile` is recognised only by the member check, through `.value`.
- **No unsupported or duplicate raw moment sources** (`_admit_label_roles` L659, `_unsupported_raw_kinds` L476, `_whitened_kinds` L481, L8):
  - Operator `coarse_first_R` / `coarse_second_S` rows give status unsupported in every role. Their single global port frame cannot represent B = -A.
  - The adapter's raw R/S, and its duplicate presence/Z/pair values, are never read.
  - Whitened R'/S' are exposed once, as ("whitened_R", cell, i) and ("whitened_S", cell, i, j) with i <= j. They enter H_c only through `pair_source_hamiltonian`. A generic ("source", label) coefficient or coordinate on them is an unsupported duplicate.

## Issue 4: 0408 corrected moments in H_c and every source derivative: FIXED

- **One evaluation per state.** `_segment_core` (L1626) runs at every new state: initial, global, palette and held replay, Birth included. It makes full `diagonal_terms`, `read_rows` and callback calls, with no copied-bit shortcut. That single evaluation forms:
  - D = H[N]diag - j.O + P - lambda A, with P the adapter's pair_source_hamiltonian;
  - every D_a;
  - the stored tracked-read row, which `_measure` (L2184) uses for the time-averaged moments.

  So H_c, D, D_a, D_ab and all moments share one evaluation.
- **New coordinates** (`_admit_coordinates`, L737):
  - ("pair_source_R", cell, i) gives D_a = -R'_i.
  - ("pair_source_S", cell, i, j), i <= j, gives D_a = -mult*S'_ij, with the declared multiplicity 1 or 2 from the Frobenius contraction.
  - D_ab = W_ab = 0 exactly, since the coordinates are affine.
- **Consistency check.** The adapter value must equal the module's linear reconstruction -j_R'.R' - J_S':S' within `source_consistency_tolerance` at every state, otherwise the run fails.
- **Whitening.** Fixed whitening is caller and registration input. Reads are whitened by the adapter. Dual sources are taken as given, or converted once from raw. Derivatives are always in the whitened dual frame.
- **Normalization.** R/S use the adapter's current per-configuration present count. The module never renormalizes and never forms C = M - mu mu^T.
- **Documentation:** L8 (L249), L20 (L325), SEMANTICS (L143-148), conventions "pair_sources" (L2424).

## Items judged not a defect (with reasons)

1. **"Obtain the FULL outgoing diagonal reads after every transition; no copied-bit shortcut for Birth."** v001 already re-evaluated the full target state at every new state. Its `_segment_at` (v001 L939-959), reached from `_ctmc_segment` (v001 L1135) and `_initial_path` (v001 L1244), called `canonical_state_key`, `primitive_channels`, `diagonal_terms` and `read_rows` on the target state, and no bits were ever copied. The real defects were:
   - the record-format mismatch (Issue 3);
   - the missing adapter path (Issue 3/4);
   - recomputing reads separately at measurement time.

   v002 keeps full per-state evaluation and shares it between D, D_a and the moments.
2. **"D_ab" in "used consistently in H_c, D, D_a, D_ab".** No computational change was needed. Every coordinate, including the new pair sources, is affine, so D_ab = W_ab = 0 exactly. This is now documented (L5, L20).

## Residual assumptions recorded in LIMITATIONS (not choices of physics or values)

- `owner_restricted_channels` name and signature are assumed (L1, L19). Its completeness is the operator's contract, cross-checked only in verify mode.
- A callable edge profile is trusted through its declared uniform `value` (L2).
- Per-event costs stay GLOBAL in every move: `diagonal_terms`, `read_rows` and `adapted_moment_reads` are O(current vertices / registered labels). Only channel enumeration and the exit rate are restricted in palette moves (L3, COST).
- With operator v001, the adapter's `build_inputs` model, whose h/t/theta are callables, is rejected by `validate_owned_model`. That gives status `failed`, by the adapter's own text, until operator v002 lands.

## Static checks of v002

These were run with `python3 -I -B` from the scratch directory on the file TEXT, on both the scratch copy and the destination file, with identical results. The module was never imported, and no `__pycache__` exists in the destination directory.

- **Parse and compile.** `ast.parse` plus `compile(..., "exec")` passed.
- **Imports.** Only `bisect`, `collections.abc`, `math` and `numpy`.
- **Forbidden constructs.**
  - There is no `@` or `@=`, and no call named `dot`, `matmul`, `vdot` or `inner`.
  - Every `einsum` call has `optimize=False`.
  - There is no `print`, `open`, `eval`, `exec`, `compile`, `__import__` or `input`, and no `os`, `sys`, `subprocess` or `threading` name.
- **Module level.** Only the docstring, the imports, the `LIMITATIONS` string, `class _Stop` and 84 function definitions; nothing runs at import.
- **Public signature.** One public function, `owned_collective_worldline_static_response`, with 0 positional parameters and 23 keyword-only parameters, none with a default. Relative to v001, `extra_diagonal_reads` became `diagonal_read_source_callback` and `palette_parameters` was added.
- **Undefined names.** A `symtable` scan for undefined implicit globals found none.

## diff -u v001 v002

```diff
--- owned_collective_worldline_static_response_v001.py	2026-10-16 03:39:03.091674441 -0500
+++ owned_collective_worldline_static_response_v002.py	2026-10-16 04:21:29.846046360 -0500
@@ -1,7 +1,10 @@
 """Owned collective static response by positive imaginary-time worldlines.
 
-UNT task 0407, version v001. Static author implementation: written as text and never
-imported or executed by its author. numpy plus the Python standard library only.
+UNT task 0407, version v002: the fix of v001 (sha256
+0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f, preserved unchanged) for the
+review/0408/0409 blocking items: model-level member check, additive blocked-palette move,
+actual operator API, root adapter read/source callback. Static author implementation: written
+as text and never imported or executed by its author. numpy plus the Python standard library.
 
 Binding sources (sha256 computed from bytes before writing; all read-only):
   * UNT_EXCHANGE/FROM_CODEX/0407_2026-10-16_main_collective_worldline_evaluator.md
@@ -27,6 +30,25 @@
     d81d48e8407f5576305dbbb50a275f163401bbb91f67b5938dc9736ec8b21663
   * helpers/coefficient_method/UNIFORM_ENERGY_KUBO_IDENTITIES_AND_LEGENDRE_ZERO_MODE_V001.md
     a7d048c11a826d6d2627afd3f5324458a0350bc6abbd58bd8ab8d6c39d7eedf7
+v002 additions (sha256 from bytes before writing; read-only; values never taken from them):
+  * UNT_EXCHANGE/FROM_CODEX/0408_2026-10-16_collective_palette_and_physical_registration_binding.md
+    c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341
+  * UNT_EXCHANGE/FROM_CODEX/0409_2026-10-16_actual_adapter_and_remaining_all_pair_allocation.md
+    53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c
+  * helpers/coefficient_method/OWNED_WORLDLINE_BLOCKED_PALETTE_MOVE_IMPLEMENTATION_V001.txt
+    3b06ee3392894de2e96716c86f7b3184c792a407a81435f95aa448440418ca16   ("PALETTE"), with its
+    distinct review helpers/response_packet_audit/OWNED_WORLDLINE_BLOCKED_PALETTE_DISTINCT_REVIEW_V001.json
+    42e4041006a07e3d9f5a44afbd079077be1e60ef91919d34251915f0e2f8de35
+  * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v001.py
+    27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6   (ACTUAL operator API,
+    read as text; no operator v002 existed on disk when this file was written)
+  * helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py
+    0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77   (root adapter, read as
+    TEXT only; its public callables are reached at run time through a caller-supplied object)
+  * helpers/recovered_packet_audit/OWNED_DIAMOND_CURRENT_GRAPH_COLLECTIVE_REGISTRATION_PROPOSED_V001.json
+    f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 and its companion
+    OWNED_DIAMOND_WHITENING_DUAL_SOURCE_MANDATORY_COMPANION_V001.json
+    9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7   (semantics only)
 Style reference (read as text): claude_artifacts/scalar_metric_solve_0397/
 scalar_metric_particular_solve_v002.py (fail-closed result dict).
 
@@ -34,49 +56,71 @@
   owned_collective_worldline_static_response(*, operator_api, graph0, model, registration,
       initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients,
       volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
-      extra_diagonal_reads, chain_generators, move_parameters, caps, burn_in_sweeps,
-      measurement_sweeps, error_parameters, numerical_tolerances, implicit_closure)
+      diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
+      caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
+      implicit_closure)
 It returns a plain fail-closed dict with "ok", "status" (complete | incomplete |
 unsupported | failed), "stage_reached" and "failures". When ok is False every populated
 field is evidence only, never a result.
 
-ASSUMED OPERATOR API (state level, basis free; the operator module is NOT imported here).
-The caller passes `operator_api`, a mapping or object exposing these module-level,
-keyword-only callables (names to be reconciled by the final checker if they differ):
+OPERATOR API: the ACTUAL owned_parent_operator_v001.py API (state level, basis free; the
+operator module is NOT imported here). The caller passes `operator_api`, a mapping or object
+exposing these module-level, keyword-only callables:
   validate_owned_model(*, graph0, model, registration)
-      -> dict with "ok" True and a validated "context"; otherwise its "status"
-         ("unsupported" is passed through, anything else is "failed") and "failures".
-  canonical_state_key(*, context, state) -> key; equal keys <=> equal current labelled
-      configurations (0406 item 2). Keys must compare with == to a single bool.
-  primitive_channels(*, context, state) -> list of records BEFORE aggregation, one per
-      primitive, each a mapping (or object) with fields
-        owner_id, kind in {flip, hop, bind, admit, admit_rev, birth, birth_rev},
-        target_state, amplitude (complex <target|h_X|state>), queried_support,
-        changed_support (iterable of hashables), weights {cell: (w(target)+w(source))/2}.
-      Every reverse reconnection alternative is a record; coincident destinations stay
-      separate records. A record with amplitude exactly 0 is skipped (no jump mark).
-  diagonal_terms(*, context, state) -> list of records with value (real), support and
-      weights {cell: w(state)}.
-  read_rows(*, context, state) -> list of records with label (hashable, unique per
-      state), value (real) and optionally kind (e.g. presence / first-moment Z / pair).
-      A label absent at a state has value 0 there (presence-masked reads; contract 5).
+      -> {"ok", "stage_reached", "failures", "context"}; context.energy_cells is the ordered
+         tuple of coarse cells (a "status" "unsupported", if ever returned, is passed through).
+  canonical_state_key(*, context, state) -> canonical key (tuple of ints); equal keys <=>
+      equal current labelled configurations (0406 item 2); == must give a single bool.
+  primitive_channels(*, context, state) -> list of records BEFORE aggregation with fields
+      owner_id, kind in {diag, flip, hop, bind, admit, admit_rev, birth, birth_rev},
+      target_state (canonical key; None for diag), amplitude (complex <target|h_X|state>),
+      queried_support, changed_support (tuple of hashable anchors), energy_weights (tuple
+      aligned with context.energy_cells, (w(target)+w(source))/2). Records of kind "diag"
+      are the diagonal owners; they are skipped here and read through diagonal_terms. Every
+      reverse reconnection is a record; coincident destinations stay separate records. A
+      record with amplitude exactly 0 is skipped (no jump mark).
+  diagonal_terms(*, context, state) -> the kind "diag" records; the real diagonal value is
+      the record amplitude and energy_weights[alpha] = w_alphaX(state).
+  read_rows(*, context, state) -> {"labels": state-independent tuple of typed labels,
+      "values": float64 [n], "presence": float64 [n]}; absent rows have value 0.
+  owner_restricted_channels(*, context, state, owners) -> ASSUMED (0405 module A v002 was
+      not on disk; name and signature to be reconciled by the final checker): the
+      primitive_channels records (same fields) of every primitive whose permanent palette
+      groups (classification below) meet `owners`, a frozenset of original owner labels,
+      with all Birth reverse alternatives and full current eligibility. Required only when
+      palette_parameters is not None.
+ROOT ADAPTER (owned_diamond_registration_input_adapter_v001.py; diagonal_read_source_callback
+supplies the adapter object at run time; these ACTUAL signatures are called unchanged):
+  adapted_moment_reads(*, operator_module, context, state, binding) -> {"cells", "R", "S",
+      ...}: whitened, configuration-normalized (current present count) coarse moments.
+  pair_source_hamiltonian(*, reads, j_R, j_S) -> -j_R.R' - J_S:S' (whitened duals).
+  raw_to_whitened_sources(*, j_R_raw, j_S_raw) -> (j_R', J_S') (only for source_frame "raw").
 Kind -> gauge increments (contract section 3 + assembly lines 300-327): flip and hop
 change no record bit, cell or slot; bind flips one record bit q_v; admit R->S raises the
 Spent number N_S by one (admit_rev lowers it); birth adds one active slot N with
 newborns loaded R,p=q=0 (birth_rev removes it). Reverse pairs: flip<->flip, hop<->hop,
 bind<->bind, admit<->admit_rev, birth<->birth_rev.
+Palette classification (PALETTE; permanent labels inside the operator owner_id): birth and
+birth_rev ("birth", owner, cut) -> {owner}; flip and hop (family, ("edge", (A, B))) ->
+{group(A), group(B)}; bind, admit and admit_rev (family, ("vertex", v)) -> {group(v)}; with
+group(original o) = o and group(a_j) = group(b_j) = o from graph0["slots"]. Forward and
+reverse primitives carry the same owner_id, so membership is reversal invariant.
 
 WHERE THE SPEC IS IMPLEMENTED
-  Section 1 (member, gauge, H_c, beta, component): _admit_gauge_phases, _gauge_table,
-    _channels_at (gauge check, W >= 0), _diagonal_at (real diagonals), _segment_at
-    (H_c = H[N] - sum_a j_a O_a - lambda A); validate_owned_model is called first.
+  Section 1 (member, gauge, H_c, beta, component): _model_member_check (model-level, every
+    supplied coefficient, before any state is visited), _admit_gauge_phases, _gauge_table,
+    _channels_from_records (per-primitive gauge check at visited states, W >= 0),
+    _diagonal_at (real diagonals), _segment_core (H_c = H[N] - sum_a j_a O_a - pair
+    sources - lambda A); validate_owned_model is called first.
   Section 2 (closed paths, no basis, primitive jump marks): path dict {segments,
-    events, times}; _segment_at/_channels_at enumerate only the current state's
+    events, times}; _segment_core/_channels_at enumerate only the current state's
     channels; per-primitive W with lapse weights BEFORE aggregation; r(x) = sum W.
-  Section 3 (detailed-balance moves): _interval_move (unconditioned CTMC regrowth from
-    the fixed initial endpoint, endpoint rejection, min(1, exp{int_new(r-D) -
-    int_old(r-D)}) in log arithmetic, all lengths < beta plus the whole circle with
-    anchor fixed), _rotate (uniform origin rotation, probability one), _ctmc_segment.
+  Section 3 (detailed-balance moves): _move dispatcher; _interval_move (global
+    unconditioned CTMC regrowth from the fixed initial endpoint, endpoint rejection,
+    min(1, exp{int_new(r-D) - int_old(r-D)}) in log arithmetic, all lengths < beta plus
+    the whole circle with anchor fixed), _rotate (uniform origin rotation, probability
+    one), _ctmc_segment; ADDITIVE _palette_move (PALETTE; held outside marks, restricted
+    inside CTMC, held-rate ratios) with the global moves kept at nonzero probability.
   Section 4 (estimators): _measure (S_a, T_ab, time-averaged reads), _estimate
     (<S>, Cov(S,S) + <T>, read means, Cov(S, read)), result "estimates".
   Section 7 (cost and errors): caps -> status incomplete (never rejection); _analyze
@@ -90,15 +134,23 @@
 as -e^{i phi_birth} = e^{i theta}), every primitive matrix element h_X[y,x] becomes
 conj(G(y)) h_X[y,x] G(x); it must equal -|h_X[y,x]| (real, nonpositive) within the
 caller's relative gauge_phase tolerance, otherwise status "unsupported" (outside the
-proven common-phase zero-holonomy member). With n_alpha = N_alpha - 1 and the V002 support
-mean weights wbar_alphaX,
+proven common-phase zero-holonomy member). Before that, _model_member_check verifies the
+member on the caller's model mapping itself, for every supplied coefficient (L2). With
+n_alpha = N_alpha - 1 and the V002 support mean weights wbar_alphaX,
     W_X(x->y) = |h_X[y,x]| * (1 + sum_alpha n_alpha wbar_alphaX)        (per primitive),
     D(x) = sum_diag d_X(x) (1 + sum_alpha n_alpha w_alphaX(x))
-           - sum_a j_a O_a(x) - lambda A(x),     A(x) = sum_a a_a O_a(x),
+           - sum_a j_a O_a(x) + P(x) - lambda A(x),     A(x) = sum_a a_a O_a(x),
+    P(x) = pair_source_hamiltonian(reads(x), j_R', J_S') = -j_R'.R'(x) - J_S':S'(x)
+           (root adapter callback, whitened duals; 0 when the callback is None),
     r(x) = sum_X W_X(x->.),   H_c = D - W,   Z = Tr exp(-beta H_c).
+Every new state (after every transition, Birth included) gets FULL diagonal_terms,
+read_rows and callback reads; the SAME evaluation enters D, every D_a and the tracked
+time averages (no copied-bit shortcut, no output-only correction).
 A closed path on the imaginary-time circle [0, beta) has weight
 exp(-int D) prod_events W. Source coordinates u are ("lapse", cell) [d/dn = d/dN],
-("source", label) [j_label] and ("volume_multiplier",) [lambda]; all are affine, so
+("source", label) [j_label], ("volume_multiplier",) [lambda], ("pair_source_R", cell, i)
+[j_R'[cell][i]] and ("pair_source_S", cell, i, j), i <= j [the symmetric pair J_S'[i][j] =
+J_S'[j][i], declared multiplicity 1 if i == j else 2]; all are affine, so
 D_ab = W_ab = 0 exactly and
     S_a  = -int D_a + sum_events W_a/W,       T_ab = -sum_events W_a W_b / W^2,
     d_a log Z = <S_a>,   d_ab log Z = Cov(S_a, S_b) + <T_ab>,
@@ -116,14 +168,20 @@
 not the complete metric propagator; no EH matching, c_star, scale or normalization is
 supplied or used. Absolute F is not estimated (needs a normalization not implemented).
 
-COST. One stored path holds one state object, canonical key and O(n_u) numbers per dwell
-segment plus O(n_u) numbers per event: O(events * (state size + n_u)) through this
-state-level API (see LIMITATIONS L3). Each generated event costs one primitive_channels,
-one diagonal_terms, one read_rows and one canonical_state_key call at the new state (all
-O(current vertices) in the worst case) plus the reverse-pairing check; each measurement
-costs one read_rows call per distinct dwell state and O(events * (n_u + n_r)) arithmetic.
-Error analysis stores O(chains * measurements * (n_u^2 + n_r)) numbers and O(J * n_y)
-jackknife replicates. No Hilbert-space list, basis index or dense operator is built.
+COST. One stored path holds one state object, canonical key and O(n_u + n_r) numbers per
+dwell segment plus O(n_u) numbers per event: O(events * (state size + n_u + n_r)) through
+this state-level API (see LIMITATIONS L3). Each generated event of a global move costs one
+primitive_channels, one diagonal_terms, one read_rows, one canonical_state_key and (with
+the callback) one adapted_moment_reads call at the new state, all O(current vertices) or
+O(registered labels) in the worst case, plus the reverse-pairing check. A palette event
+replaces the full channel enumeration by owner_restricted_channels (restricted exit rate
+r_S) but KEEPS the global diagonal_terms / read_rows / callback reads per new state, and
+one restricted enumeration per old dwell segment inside the interval: the remaining
+global per-event cost is reported, not hidden (L3, L19). Exit rates of segments created by
+palette moves are enumerated lazily when a global move needs them. A measurement uses the
+stored per-segment read rows and costs O(events * (n_u + n_r)) arithmetic. Error analysis
+stores O(chains * measurements * (n_u^2 + n_r)) numbers and O(J * n_y) jackknife
+replicates. No Hilbert-space list, basis index or dense operator is built.
 
 LIMITATIONS: see the module-level string LIMITATIONS.
 """
@@ -136,29 +194,49 @@
 
 
 LIMITATIONS = """
-L1. Operator API is ASSUMED (docstring): function names, record field names (owner_id,
-    kind, target_state, amplitude, queried_support, changed_support, weights, value,
-    label) and kind tokens. Mismatches fail closed ("failed"); the final checker
-    reconciles names with owned_parent_operator_v001.py.
-L2. Positive gauge. The gauge is applied through per-kind increments of record parity,
-    Spent number and slot number (contract section 3), with caller-declared common
-    phases gauge_phases {admission_phase = arg kappa, birth_phase = arg epsilon}. Every
-    primitive enumerated at every VISITED state (all alternatives, not only those taken)
-    is checked; primitives at never-visited states are not. Model-level membership (real
-    h, t, g > 0, zero hopping phases, uniform kappa phase, common epsilon phase) is
-    otherwise delegated to validate_owned_model. Net increments of every regrown segment
-    are compared with the replaced segment (and the initial path must close them), which
-    detects kind labels inconsistent with a state-function gauge on sampled paths only.
+L1. Operator API is the ACTUAL owned_parent_operator_v001.py API (sha256 27ad1762...):
+    energy_weights tuples aligned with context.energy_cells, the diagonal value is the
+    "diag" record amplitude, primitive_channels also returns the "diag" records (skipped
+    here), read_rows returns {labels, values, presence} arrays with state-independent
+    labels. The owner-restricted enumeration of the palette move is ASSUMED as
+    owner_restricted_channels(*, context, state, owners) because 0405 module A v002 was
+    not on disk; the final checker reconciles its name/signature. Mismatches fail closed.
+L2. Positive gauge, verified on TWO lines. (a) Model level, before any state is visited:
+    _model_member_check reads the caller's model mapping against the contract s3/s10
+    coefficient schema (exactly the 13 diagonal scalars Delta, Ud, dstar, epsilon_c,
+    epsilon_r, lambda_R, lambda_J, E_R, E_S, E_I, e_R, e_I, C_identity plus the profiles
+    h, t, theta, g, kappa, epsilon) and checks EVERY supplied entry, whether or not any
+    chain ever enumerates it: h_e > 0, t_e > 0 and theta_e == 0 exactly for every edge key
+    (newborn/child edges included), g_v > 0, kappa_v != 0 with |kappa_v - |kappa_v|
+    exp(i admission_phase)| <= gauge_phase*|kappa_v| for every vertex, the same for every
+    owner's epsilon_j with birth_phase, and every diagonal scalar a finite real. A Mapping
+    profile is checked entry by entry; a bare scalar is a declared uniform value; a
+    callable profile is admitted only through its declared uniform attribute `value` (the
+    root adapter's UniformEdgeProfile returns exactly that value for every ordered A-B
+    pair by its text, so the check trusts that declaration rather than enumerating all
+    potential endpoint pairs, which 0408/0409 forbid). Any other form, a missing or
+    unknown key, a violation or a non-evaluable entry returns status "unsupported" before
+    sampling. A zero kappa or epsilon has no phase and is unsupported (the member has
+    nonzero common kappa and Birth amplitude). (b) Second line, unchanged from v001: every
+    primitive enumerated at every VISITED state (all alternatives, restricted palette
+    enumerations included) must gauge to -|h|. The gauge itself is applied through
+    per-kind increments of record parity, Spent number and slot number (contract section
+    3) with caller-declared gauge_phases {admission_phase = arg kappa, birth_phase = arg
+    epsilon}. Net increments of every regrown segment are compared with the replaced
+    segment (and the initial path must close them).
 L3. Storage. The SPEC's O(V0 + events) path storage presumes event-delta storage. Through
     target_state objects this module stores one state object and key per dwell segment,
     i.e. O(events * state size) unless the operator's states share structure. An
-    operator "apply event delta" API would be needed to reach the SPEC bound.
+    operator "apply event delta" API would be needed to reach the SPEC bound. Per-event
+    work keeps GLOBAL terms: diagonal_terms, read_rows and the callback reads are full
+    O(current vertices / registered labels) evaluations at every new state, in global and
+    palette moves alike; no incremental diagonal or dependency cache is implemented.
 L4. Absolute free energy F = -log Z/beta is NOT estimated (None): the positive path
     measure gives derivatives only. A normalization (e.g. thermodynamic integration in
     beta) is not implemented. No global energy scalar is subtracted from D.
 L5. Coordinates are affine: lapse n_alpha (identical derivative to N_alpha), read source
-    j_label, lambda. W_ab = D_ab = 0 exactly. Nonlinear coordinates (e.g. g00 with
-    N = sqrt(1 + 2 n_g)) follow by the caller's chain rule d_vv log Z = J^T H J +
+    j_label, lambda, whitened pair sources (L20). W_ab = D_ab = 0 exactly. Nonlinear
+    coordinates (e.g. g00 with N = sqrt(1 + 2 n_g)) follow by the caller's chain rule d_vv log Z = J^T H J +
     sum_a d_a log Z d_vv u_a using the returned first AND second derivatives. Read-frame,
     registration, preparation and map derivative contacts are NOT included (reads fixed).
 L6. Zero-rate source-opening directions (an available primitive with W = 0 but W_a != 0)
@@ -168,20 +246,31 @@
 L7. Conserved-resource component. All chains must start in ONE declared component; the
     module cannot verify membership without enumeration. Explicitly weighted unions of
     superselection components are not combined here (caller weights separate runs).
-L8. Coarse R_alpha, S_alpha with the current-state 1/m_alpha normalization are available
-    only through the caller's extra_diagonal_reads callable (registration-owned); the
-    module never forms C = M - mu mu^T and never inverts covariance-only response. The
-    physical read-read susceptibility is obtained by making those reads source
-    coordinates (d2logZ); a separate read-read path covariance is not returned.
+L8. Coarse moments (0408/0409). Operator rows of kind coarse_first_R / coarse_second_S
+    (operator v001: one global port frame, which cannot represent the registered B = -A
+    frames) are unsupported in EVERY role (source coefficient, volume term, derivative
+    coordinate, tracked read): status "unsupported". Whitened, configuration-normalized
+    (current present count) coarse R', S' come only from the root adapter callback
+    (adapted_moment_reads), as labels ("whitened_R", cell, i) and ("whitened_S", cell, i,
+    j) with i <= j (S' is symmetric; the lower triangle is not duplicated). The adapter's
+    raw (unwhitened) moments and its duplicate presence/Z/pair values are never allocated
+    as reads or sources. Whitened labels enter H_c ONLY through pair_source_hamiltonian
+    with the callback's j_R, j_S (generic ("source", label) coefficients or coordinates on
+    them are unsupported duplicates); they may be tracked and used in A. The module never
+    forms C = M - mu mu^T (caller: adapter central_covariance on ensemble means) and never
+    inverts covariance-only response. Read-read susceptibilities come from making the
+    reads source coordinates (d2logZ); no separate read-read path covariance is returned.
 L9. A ("fixed diagonal volume gradient") is interpreted literally as an explicit linear
-    combination of diagonal reads (operator rows and/or extra reads) with caller
+    combination of diagonal reads (operator rows and/or whitened callback reads) with caller
     coefficients and multiplier lambda. A(m) self-consistency (SPEC section 5) is not
     solved; implicit_closure must be None (status unsupported otherwise).
 L10. Interval selection density (SPEC ambiguity): start time uniform on [0, beta); with
     probability whole_circle_probability the whole circle anchored at that time; else a
     length beta*U*f with U uniform on [0,1) and f drawn from caller-weighted components
     (at least one f = 1 so every length below beta has positive density). Rotation is a
-    separate move with caller probability. All are source independent and symmetric.
+    separate move with caller probability. All are source independent and symmetric. The
+    same interval density is used by the global and the palette moves; the move type is
+    chosen with state-independent probabilities p_rot, p_palette, 1 - p_rot - p_palette.
 L11. H[N] weighting is the literal source functional H + sum n_alpha E_alpha, i.e.
     multiplier 1 + sum n_alpha wbar_alpha; it equals sum N_alpha wbar_alpha when the
     weights partition, which is checked to the caller's weight_partition tolerance at
@@ -200,7 +289,8 @@
     not separately on products.
 L14. Caps (events per path, total events, sweeps, channel enumerations) end the whole
     computation with status incomplete and partial diagnostics; no estimate is returned
-    and no path is ever rejected because of a cap.
+    and no path is ever rejected because of a cap. Restricted, lazy and verification
+    enumerations count as channel enumerations; replayed held marks count as events.
 L15. An exact floating-point coincidence of event times (zero holding time, rotation
     origin or interval end equal to an event time, or rounding to beta) ends the
     computation as failed rather than perturbing times.
@@ -212,6 +302,37 @@
     errors are not caught.
 L18. Measurement is taken once after every measurement sweep; consecutive measurements
     are correlated and handled only by the error analysis above.
+L19. Blocked palette move (PALETTE, additive). A palette S (frozenset of original owner
+    labels) is drawn from the caller's weighted list and the interval by L10, both state
+    independent. Old events in the interval are held when their permanent groups (module
+    docstring classification) miss S; times and descriptors are kept. The held descriptor
+    is (kind, owner_id); it must identify at most one positive-rate record at any state
+    (more than one -> failed). Between held marks only member channels run, with their
+    actual rates and total r_S; a held mark is replayed through owner_restricted_channels
+    on its own groups and the proposal is rejected when the record is absent (guard,
+    newborn/donor image or eligibility failure) or has zero rate; the replayed event gets
+    the same reverse-pairing and self-loop checks as a sampled one. Endpoint mismatch
+    rejects. Acceptance is min(1, exp{int_I new(r_S - D) - int_I old(r_S - D) + sum_held
+    log(W(new pre-event)/W(old pre-event))}); endpoint rejection is never renormalized as a
+    conditioned bridge. Records returned by owner_restricted_channels that are not members
+    by this classification are dropped (counted in diagnostics); COMPLETENESS (no omitted
+    member primitive) is the operator's contract, cross-checked against
+    primitive_channels at every restricted enumeration only when
+    verify_against_full_enumeration is True (costly). No dependency cache is implemented
+    (none may omit affected events or globally normalized reads). No fast-mixing claim:
+    blocked moves alone are not claimed irreducible, so global regrowth keeps probability
+    1 - p_rot - p_palette > 0.
+L20. Pair sources (root adapter, companion equations). ("pair_source_R", cell, i)
+    differentiates j_R'[cell][i] (D_a = -R'_i); ("pair_source_S", cell, i, j), i <= j,
+    differentiates the symmetric pair J_S'[i][j] = J_S'[j][i] jointly with declared
+    multiplicity 1 (i == j) or 2 (i < j) (D_a = -mult * S'_ij), preserving the Frobenius
+    contraction. Fixed whitening is the caller's/registration's: reads are whitened by the
+    adapter; dual sources are taken as given (source_frame "whitened") or converted ONCE by
+    the adapter's raw_to_whitened_sources (source_frame "raw"); derivatives are always in
+    the whitened dual frame (raw-frame derivatives by the caller's chain rule, never a
+    second whitening). The adapter value and the module's linear reconstruction must agree
+    within source_consistency_tolerance at every state, else failed. The callback binding
+    must hold the SAME graph0 and registration objects as the operator call.
 """
 
 
@@ -322,26 +443,251 @@
     return not missing and not extra
 
 
-def _admit_operator_api(operator_api, failures):
-    names = (
+def _admit_operator_api(operator_api, need_restricted, failures):
+    names = [
         "validate_owned_model",
         "canonical_state_key",
         "primitive_channels",
         "diagonal_terms",
         "read_rows",
-    )
+    ]
+    if need_restricted:
+        names.append("owner_restricted_channels")
     api = {}
     for nm in names:
         present, fn = _field(operator_api, nm)
         if not present or not callable(fn):
             failures.append(
-                f"input operator_api: callable {nm!r} is missing (assumed API in docstring)"
+                f"input operator_api: callable {nm!r} is missing (operator API in docstring)"
             )
         else:
             api[nm] = fn
     return api if len(api) == len(names) else None
 
 
+def _model_schema():
+    """Contract s3/s10 coefficient schema (diagonal scalars, transition profiles)."""
+    scalars = ("Delta", "Ud", "dstar", "epsilon_c", "epsilon_r", "lambda_R", "lambda_J",
+               "E_R", "E_S", "E_I", "e_R", "e_I", "C_identity")
+    profiles = ("h", "t", "theta", "g", "kappa", "epsilon")
+    return scalars, profiles
+
+
+def _unsupported_raw_kinds():
+    """Operator v001 coarse moment rows built with ONE global port frame (0408/0409)."""
+    return ("coarse_first_R", "coarse_second_S")
+
+
+def _whitened_kinds():
+    """Read-label kinds supplied by the root adapter callback (whitened R', S')."""
+    return ("whitened_R", "whitened_S")
+
+
+def _label_kind(label):
+    if isinstance(label, tuple) and label and isinstance(label[0], str):
+        return label[0]
+    return None
+
+
+def _component(value):
+    return (not isinstance(value, (bool, np.bool_)) and isinstance(value, (int, np.integer))
+            and 0 <= int(value) <= 2)
+
+
+def _whitened_label_ok(label, cells):
+    kind = _label_kind(label)
+    if kind == "whitened_R":
+        return len(label) == 3 and label[1] in cells and _component(label[2])
+    if kind == "whitened_S":
+        return (len(label) == 4 and label[1] in cells and _component(label[2])
+                and _component(label[3]) and int(label[2]) <= int(label[3]))
+    return False
+
+
+def _admit_pair_sources(j_r, j_s, where, failures):
+    """({cell: [3 reals]}, {cell: symmetric [[3 reals] x 3]}) or None (whitened or raw)."""
+    if not isinstance(j_r, Mapping) or not isinstance(j_s, Mapping):
+        failures.append(f"{where}: j_R and j_S must be mappings cell -> 3-vector / 3x3 matrix")
+        return None
+    if not j_r or set(j_r) != set(j_s):
+        failures.append(f"{where}: j_R and j_S must be nonempty with the same cells")
+        return None
+    out_r = {}
+    out_s = {}
+    seq = (list, tuple, np.ndarray)
+    for cell in j_r:
+        vec = j_r[cell]
+        mat = j_s[cell]
+        vals = None
+        if isinstance(vec, seq) and len(vec) == 3:
+            vals = [_real_value(x) for x in vec]
+        rows = None
+        if isinstance(mat, seq) and len(mat) == 3 and all(
+            isinstance(row, seq) and len(row) == 3 for row in mat
+        ):
+            rows = [[_real_value(x) for x in row] for row in mat]
+        if vals is None or None in vals:
+            failures.append(f"{where}: j_R[{cell!r}] is not a 3-vector of finite reals")
+            continue
+        if rows is None or any(None in row for row in rows):
+            failures.append(f"{where}: j_S[{cell!r}] is not a 3x3 matrix of finite reals")
+            continue
+        if any(rows[i][j] != rows[j][i] for i in range(3) for j in range(3)):
+            failures.append(
+                f"{where}: j_S[{cell!r}] is not exactly symmetric (Frobenius contraction of a "
+                "symmetric source; multiplicities are never hidden)"
+            )
+            continue
+        out_r[cell] = vals
+        out_s[cell] = rows
+    if len(out_r) != len(j_r):
+        return None
+    return out_r, out_s
+
+
+def _admit_pair_callback(value, graph0, registration, failures):
+    """Root adapter read/source callback (0408/0409) or None."""
+    if value is None:
+        return None
+    keys = ("adapter", "operator_module", "binding", "source_frame", "j_R", "j_S",
+            "source_consistency_tolerance")
+    name = "diagonal_read_source_callback"
+    mp = _admit_mapping(name, value, failures)
+    if mp is None or not _admit_required_keys(name, mp, keys, failures):
+        return None
+    frame = mp["source_frame"]
+    if not (isinstance(frame, str) and frame in ("whitened", "raw")):
+        failures.append(f"input {name}['source_frame']: must be 'whitened' or 'raw'")
+        return None
+    fn_names = ["adapted_moment_reads", "pair_source_hamiltonian"]
+    if frame == "raw":
+        fn_names.append("raw_to_whitened_sources")
+    fns = {}
+    for nm in fn_names:
+        present, fn = _field(mp["adapter"], nm)
+        if not present or not callable(fn):
+            failures.append(f"input {name}['adapter']: callable {nm!r} is missing")
+        else:
+            fns[nm] = fn
+    if not callable(getattr(mp["operator_module"], "state_labels", None)):
+        failures.append(
+            f"input {name}['operator_module']: the adapter calls operator_module.state_labels; "
+            "an object with that callable attribute is required"
+        )
+    binding = mp["binding"]
+    if not isinstance(binding, Mapping) or "graph0" not in binding or "registration" not in binding:
+        failures.append(f"input {name}['binding']: a mapping with 'graph0' and 'registration'")
+    elif binding["graph0"] is not graph0 or binding["registration"] is not registration:
+        failures.append(
+            f"input {name}['binding']: binding['graph0'] and binding['registration'] must be the "
+            "SAME objects passed as graph0 and registration (one source of truth for ports, "
+            "cells and presence)"
+        )
+    tol = _admit_real(f"{name}['source_consistency_tolerance']",
+                      mp["source_consistency_tolerance"], failures)
+    if tol is not None and not tol >= 0.0:
+        failures.append(f"input {name}['source_consistency_tolerance']: must be >= 0")
+        tol = None
+    pair = _admit_pair_sources(mp["j_R"], mp["j_S"], f"input {name}", failures)
+    if len(fns) != len(fn_names) or tol is None or pair is None:
+        return None
+    return {
+        "fns": fns,
+        "operator_module": mp["operator_module"],
+        "binding": binding,
+        "source_frame": frame,
+        "j_R": pair[0],
+        "j_S": pair[1],
+        "tol": tol,
+    }
+
+
+def _admit_palette_parameters(value, failures):
+    """Additive blocked-palette move parameters (PALETTE) or None (move disabled)."""
+    if value is None:
+        return None
+    name = "palette_parameters"
+    keys = ("selection_probability", "palettes", "verify_against_full_enumeration")
+    mp = _admit_mapping(name, value, failures)
+    if mp is None or not _admit_required_keys(name, mp, keys, failures):
+        return None
+    p_sel = _admit_real(f"{name}['selection_probability']", mp["selection_probability"], failures)
+    if p_sel is not None and not 0.0 < p_sel < 1.0:
+        failures.append(f"input {name}['selection_probability']: must lie in (0, 1)")
+        p_sel = None
+    verify = mp["verify_against_full_enumeration"]
+    if not isinstance(verify, (bool, np.bool_)):
+        failures.append(f"input {name}['verify_against_full_enumeration']: must be a bool")
+        verify = None
+    raw = mp["palettes"]
+    pals = []
+    if not isinstance(raw, (list, tuple)) or not raw:
+        failures.append(f"input {name}['palettes']: nonempty list of (weight, owner labels)")
+    else:
+        for i, item in enumerate(raw):
+            if not isinstance(item, (list, tuple)) or len(item) != 2:
+                failures.append(f"input {name}['palettes'][{i}]: not a (weight, owners) pair")
+                continue
+            w = _real_value(item[0])
+            owners = item[1]
+            ok = isinstance(owners, (list, tuple, set, frozenset)) and len(owners) > 0 and all(
+                _hashable(o) for o in owners
+            )
+            if w is None or not w > 0.0 or not ok:
+                failures.append(
+                    f"input {name}['palettes'][{i}]: need weight > 0 and a nonempty collection "
+                    "of hashable original owner labels"
+                )
+                continue
+            pals.append((w, frozenset(owners)))
+    if p_sel is None or verify is None or not pals or len(pals) != len(raw):
+        return None
+    total = math.fsum(w for w, _ in pals)
+    cumulative = []
+    acc = []
+    for w, s in pals:
+        acc.append(w)
+        cumulative.append((math.fsum(acc) / total, s))
+    return {
+        "selection_probability": p_sel,
+        "palettes": pals,
+        "cumulative": cumulative,
+        "verify": bool(verify),
+    }
+
+
+def _admit_label_roles(sources, vgrad, tracked, coords, pair_cells, failures, unsupported):
+    """0408/0409: no unsupported raw coarse rows, no duplicated whitened source allocation."""
+    roles = [("source_coefficients", lbl) for lbl in sources]
+    roles += [("volume_gradient_coefficients", lbl) for lbl in vgrad]
+    roles += [("tracked_read_labels", lbl) for lbl in tracked]
+    roles += [("derivative_coordinates", c[1]) for c in coords if c[0] == "source"]
+    for role, lbl in roles:
+        kind = _label_kind(lbl)
+        if kind in _unsupported_raw_kinds():
+            unsupported.append(
+                f"input {role}: {lbl!r} is an operator v001 coarse moment row built with one "
+                "global port frame, which cannot represent the registered B = -A frames; "
+                "corrected moments enter only through diagonal_read_source_callback (L8)"
+            )
+        elif kind in _whitened_kinds():
+            if role in ("source_coefficients", "derivative_coordinates"):
+                unsupported.append(
+                    f"input {role}: {lbl!r} would duplicate the pair-source allocation; "
+                    "whitened moments are sourced only through the callback j_R/j_S and "
+                    "('pair_source_R'|'pair_source_S', ...) coordinates (L8, L20)"
+                )
+            elif pair_cells is None:
+                failures.append(
+                    f"input {role}: {lbl!r} needs diagonal_read_source_callback (whitened reads)"
+                )
+            elif not _whitened_label_ok(lbl, pair_cells):
+                failures.append(
+                    f"input {role}: {lbl!r} is not ('whitened_R', cell, i) or "
+                    "('whitened_S', cell, i, j) with i <= j in 0..2 and a callback cell"
+                )
+
+
 def _admit_lapse_factors(value, failures):
     mp = _admit_mapping("lapse_factors", value, failures)
     if mp is None:
@@ -388,7 +734,7 @@
     return {"admission_phase": phi_a, "birth_phase": phi_b}
 
 
-def _admit_coordinates(value, lapse, failures):
+def _admit_coordinates(value, lapse, pair_cells, failures):
     if not isinstance(value, (list, tuple)):
         failures.append("input derivative_coordinates: must be a list or tuple of tuples")
         return None
@@ -410,10 +756,27 @@
             pass
         elif tag == "volume_multiplier" and len(coord) == 1:
             pass
+        elif tag in ("pair_source_R", "pair_source_S"):
+            n_idx = 1 if tag == "pair_source_R" else 2
+            ok = (
+                pair_cells is not None
+                and len(coord) == 2 + n_idx
+                and coord[1] in pair_cells
+                and all(_component(x) for x in coord[2:])
+                and (n_idx == 1 or int(coord[2]) <= int(coord[3]))
+            )
+            if not ok:
+                failures.append(
+                    f"input derivative_coordinates[{i}]: {coord!r} is not ('pair_source_R', "
+                    "cell, i) or ('pair_source_S', cell, i, j), i <= j in 0..2, with cell a "
+                    "diagonal_read_source_callback cell (callback required)"
+                )
+                continue
         else:
             failures.append(
                 f"input derivative_coordinates[{i}]: {coord!r} is not ('lapse', cell), "
-                "('source', label) or ('volume_multiplier',)"
+                "('source', label), ('volume_multiplier',), ('pair_source_R', cell, i) or "
+                "('pair_source_S', cell, i, j)"
             )
             continue
         if coord in out:
@@ -692,6 +1055,93 @@
     return table
 
 
+def _profile_entries(name, prof):
+    """(form, [(where, value), ...]) for every supplied entry of a model profile.
+
+    A Mapping is read entry by entry; a bare scalar is a declared uniform value; a callable
+    is admitted only through its declared uniform attribute `value` (root adapter
+    UniformEdgeProfile). Anything else cannot be evaluated: (None, reason).
+    """
+    if isinstance(prof, Mapping):
+        return "mapping", [(f"model['{name}'][{k!r}]", v) for k, v in prof.items()]
+    if _complex_value(prof) is not None:
+        return "uniform_scalar", [(f"model['{name}']", prof)]
+    if callable(prof):
+        present, val = _field(prof, "value")
+        if present:
+            return "uniform_accessor_value", [(f"model['{name}'].value", val)]
+        return None, (
+            f"model['{name}'] is a callable without a declared uniform 'value'; its entries "
+            "cannot be checked without enumerating every potential endpoint pair"
+        )
+    return None, (
+        f"model['{name}'] has type {type(prof).__name__}, not a mapping or a declared uniform"
+    )
+
+
+def _model_member_check(model, phases, tol_g):
+    """Model-level common-phase zero-holonomy member check (SPEC s1; L2a), state independent.
+
+    Returns (ok, problems, forms). Every supplied coefficient of the caller's model mapping
+    is checked against the contract s3/s10 schema; nothing depends on visited states.
+    """
+    problems = []
+    forms = {}
+    count = [0]
+
+    def bad(msg):
+        count[0] += 1
+        if len(problems) < 20:
+            problems.append(msg)
+
+    scalars, profiles = _model_schema()
+    if not isinstance(model, Mapping):
+        return False, ["model is not a mapping; membership cannot be evaluated"], forms
+    expected = set(scalars) | set(profiles)
+    missing = [k for k in scalars + profiles if k not in model]
+    unknown = [k for k in model if k not in expected]
+    if missing or unknown:
+        return False, [
+            f"model keys differ from the contract s3/s10 coefficient schema (missing "
+            f"{missing!r}, unknown {unknown!r}); membership cannot be evaluated"
+        ], forms
+    for k in scalars:
+        if _real_value(model[k]) is None:
+            bad(f"model['{k}'] = {model[k]!r} is not a finite real scalar (real diagonal profile)")
+    unit = {
+        "kappa": complex(math.cos(phases["admission_phase"]), math.sin(phases["admission_phase"])),
+        "epsilon": complex(math.cos(phases["birth_phase"]), math.sin(phases["birth_phase"])),
+    }
+    for name in profiles:
+        form, entries = _profile_entries(name, model[name])
+        if form is None:
+            bad(entries + "; membership cannot be evaluated")
+            continue
+        forms[name] = form
+        for where, raw in entries:
+            if name in ("h", "t", "g"):
+                v = _real_value(raw)
+                if v is None or not v > 0.0:
+                    bad(f"{where} = {raw!r}: must be a finite real > 0 (member: real h, t, g > 0)")
+            elif name == "theta":
+                v = _real_value(raw)
+                if v is None or v != 0.0:
+                    bad(f"{where} = {raw!r}: hopping phase must be exactly 0 (zero holonomy)")
+            else:
+                z = _complex_value(raw)
+                if z is None or z == 0:
+                    bad(f"{where} = {raw!r}: a nonzero finite scalar is required (phase defined)")
+                elif not abs(z - abs(z) * unit[name]) <= tol_g * abs(z):
+                    which = "admission_phase" if name == "kappa" else "birth_phase"
+                    bad(
+                        f"{where} = {raw!r}: its phase differs from gauge_phases['{which}'] "
+                        "beyond the gauge_phase tolerance (no common phase)"
+                    )
+    if count[0] > len(problems):
+        problems.append(f"... {count[0] - len(problems)} further member violations not listed")
+    return count[0] == 0, problems, forms
+
+
 # ----------------------------------------------------------------------------------
 # Operator access (state level; no basis)
 # ----------------------------------------------------------------------------------
@@ -728,22 +1178,23 @@
     )
 
 
-def _weights(run, raw, where):
-    if not isinstance(raw, Mapping):
-        raise _Stop("failed", run["stage"], f"{where}: weights is not a mapping cell -> real")
-    out = {}
-    for cell, w in raw.items():
-        if cell not in run["n_of_cell"]:
-            raise _Stop(
-                "failed",
-                run["stage"],
-                f"{where}: weight cell {cell!r} has no caller lapse factor",
-            )
-        wf = _real_value(w)
-        if wf is None:
-            raise _Stop("failed", run["stage"], f"{where}: weight {cell!r} = {w!r} not finite real")
-        out[cell] = wf
-    return out
+def _energy_weights(run, raw, where):
+    """{cell: w} (nonzero entries) from an energy_weights tuple aligned with context.energy_cells."""
+    cells = run["energy_cells"]
+    try:
+        arr = np.asarray(raw)
+    except Exception as exc:
+        raise _Stop("failed", run["stage"], f"{where}: energy_weights not an array ({exc})")
+    if arr.ndim != 1 or arr.shape[0] != len(cells) or arr.dtype.kind not in "iuf":
+        raise _Stop(
+            "failed",
+            run["stage"],
+            f"{where}: energy_weights is not a real sequence aligned with context.energy_cells",
+        )
+    arr = arr.astype(np.float64)
+    if not bool(np.all(np.isfinite(arr))):
+        raise _Stop("failed", run["stage"], f"{where}: energy_weights not finite")
+    return {cells[int(i)]: float(arr[i]) for i in np.flatnonzero(arr)}
 
 
 def _lapse_multiplier(run, weights, where):
@@ -771,8 +1222,7 @@
     return sig
 
 
-def _channels_at(run, state):
-    """Nonnegative per-primitive rates at `state` (SPEC sections 1-2), before aggregation."""
+def _enumeration_tick(run):
     counters = run["counters"]
     if counters["channel_enumerations"] >= run["caps"]["max_channel_enumerations"]:
         raise _Stop(
@@ -781,21 +1231,35 @@
             "cap max_channel_enumerations reached; computation ended (no path was rejected)",
         )
     counters["channel_enumerations"] += 1
+
+
+def _channels_at(run, state):
+    """Nonnegative per-primitive rates at `state` (SPEC sections 1-2), before aggregation."""
+    _enumeration_tick(run)
     records = _op(run, "primitive_channels", context=run["context"], state=state)
+    return _channels_from_records(run, records, "primitive_channels")
+
+
+def _channels_from_records(run, records, source):
+    """Gauge check (L2b), lapse weighting and rates of operator records; 'diag' skipped."""
     if not isinstance(records, (list, tuple)):
-        raise _Stop("failed", run["stage"], "primitive_channels did not return a list")
+        raise _Stop("failed", run["stage"], f"{source} did not return a list")
     kinds = run["kinds"]
     tol_g = run["tol"]["gauge_phase"]
     channels = []
     for i, rec in enumerate(records):
-        where = f"primitive_channels record {i}"
+        where = f"{source} record {i}"
+        present_k, kind = _field(rec, "kind")
+        if not present_k:
+            raise _Stop("failed", run["stage"], f"{where}: field 'kind' missing")
+        if isinstance(kind, str) and kind == "diag":
+            continue  # diagonal owner: read through diagonal_terms (actual operator API)
         fields = {}
-        for nm in ("owner_id", "kind", "target_state", "amplitude", "changed_support", "weights"):
+        for nm in ("owner_id", "target_state", "amplitude", "changed_support", "energy_weights"):
             present, val = _field(rec, nm)
             if not present:
                 raise _Stop("failed", run["stage"], f"{where}: field {nm!r} missing")
             fields[nm] = val
-        kind = fields["kind"]
         if not _hashable(kind) or kind not in kinds:
             raise _Stop("failed", run["stage"], f"{where}: unknown kind {kind!r}")
         amp = _complex_value(fields["amplitude"])
@@ -815,7 +1279,7 @@
                 "(nonzero holonomy, non-common phase, complex flip/Bind) or gauge_phases do not "
                 "equal the model's common arg kappa / arg epsilon",
             )
-        weights = _weights(run, fields["weights"], where)
+        weights = _energy_weights(run, fields["energy_weights"], where)
         mult = _lapse_multiplier(run, weights, where)
         if mult < 0.0:
             raise _Stop(
@@ -851,6 +1315,105 @@
     return channels, exit_rate
 
 
+def _record_groups(run, kind, owner_id):
+    """Permanent original-owner groups of a primitive (PALETTE; module docstring), from labels."""
+    group = run["group"]
+    labels = None
+    try:
+        if kind in ("birth", "birth_rev"):
+            if owner_id[0] == "birth":
+                labels = (owner_id[1],)
+        elif kind in ("flip", "hop"):
+            tag, pair = owner_id[1]
+            if tag == "edge" and len(pair) == 2:
+                labels = (pair[0], pair[1])
+        elif kind in ("bind", "admit", "admit_rev"):
+            tag, vertex = owner_id[1]
+            if tag == "vertex":
+                labels = (vertex,)
+        if labels is not None:
+            return frozenset(group[lab] for lab in labels)
+    except (TypeError, KeyError, IndexError, ValueError):
+        pass
+    raise _Stop(
+        "failed",
+        run["stage"],
+        f"primitive kind {kind!r} owner_id {owner_id!r} cannot be classified into permanent "
+        "original-owner groups (palette membership must come from permanent labels)",
+    )
+
+
+def _record_identity(run, rec, where):
+    """Hashable (kind, owner_id, target_state, amplitude, energy_weights) of one record."""
+    vals = []
+    for nm in ("kind", "owner_id", "target_state", "amplitude", "energy_weights"):
+        present, val = _field(rec, nm)
+        if not present:
+            raise _Stop("failed", run["stage"], f"{where}: field {nm!r} missing")
+        vals.append(val)
+    try:
+        ident = (vals[0], vals[1], vals[2], complex(vals[3]),
+                 tuple(float(x) for x in vals[4]))
+        hash(ident)
+    except Exception as exc:
+        raise _Stop("failed", run["stage"], f"{where}: record identity not hashable ({exc})")
+    return ident
+
+
+def _palette_members(run, records, owners, source):
+    """Non-diag records whose permanent groups meet `owners` (others dropped and counted)."""
+    if not isinstance(records, (list, tuple)):
+        raise _Stop("failed", run["stage"], f"{source} did not return a list")
+    out = []
+    dropped = 0
+    for i, rec in enumerate(records):
+        present_k, kind = _field(rec, "kind")
+        present_o, owner_id = _field(rec, "owner_id")
+        if not present_k or not present_o:
+            raise _Stop("failed", run["stage"], f"{source} record {i}: kind/owner_id missing")
+        if isinstance(kind, str) and kind == "diag":
+            continue
+        if not _hashable(kind) or kind not in run["kinds"]:
+            raise _Stop("failed", run["stage"], f"{source} record {i}: unknown kind {kind!r}")
+        if _record_groups(run, kind, owner_id).isdisjoint(owners):
+            dropped += 1
+            continue
+        out.append(rec)
+    return out, dropped
+
+
+def _palette_channels(run, state, owners):
+    """Member channels and restricted exit rate r_S at `state` (owner_restricted_channels)."""
+    _enumeration_tick(run)
+    run["counters"]["restricted_enumerations"] += 1
+    records = _op(run, "owner_restricted_channels", context=run["context"], state=state,
+                  owners=owners)
+    members, dropped = _palette_members(run, records, owners, "owner_restricted_channels")
+    run["counters"]["restricted_nonmember_records_dropped"] += dropped
+    if run["palette"]["verify"]:
+        _enumeration_tick(run)
+        run["counters"]["palette_verifications"] += 1
+        full = _op(run, "primitive_channels", context=run["context"], state=state)
+        expected, _ = _palette_members(run, full, owners, "primitive_channels")
+        want = {}
+        for i, rec in enumerate(expected):
+            ident = _record_identity(run, rec, f"primitive_channels record {i}")
+            want[ident] = want.get(ident, 0) + 1
+        got = {}
+        for i, rec in enumerate(members):
+            ident = _record_identity(run, rec, f"owner_restricted_channels record {i}")
+            got[ident] = got.get(ident, 0) + 1
+        if want != got:
+            raise _Stop(
+                "failed",
+                run["stage"],
+                "owner_restricted_channels differs from the palette members of "
+                "primitive_channels at a visited state (omitted, extra or altered member "
+                "records; verify_against_full_enumeration)",
+            )
+    return _channels_from_records(run, members, "owner_restricted_channels")
+
+
 def _diagonal_at(run, state):
     """Diagonal H[N] energy and its lapse derivatives (real diagonals verified)."""
     records = _op(run, "diagonal_terms", context=run["context"], state=state)
@@ -861,10 +1424,15 @@
     lapse_terms = {cell: [] for cell in run["lapse_index"]}
     for i, rec in enumerate(records):
         where = f"diagonal_terms record {i}"
-        present_v, raw = _field(rec, "value")
-        present_w, wraw = _field(rec, "weights")
+        present_k, kind = _field(rec, "kind")
+        if present_k and not (isinstance(kind, str) and kind == "diag"):
+            raise _Stop("failed", run["stage"], f"{where}: kind {kind!r} is not 'diag'")
+        present_v, raw = _field(rec, "amplitude")
+        present_w, wraw = _field(rec, "energy_weights")
         if not present_v or not present_w:
-            raise _Stop("failed", run["stage"], f"{where}: fields 'value' and 'weights' required")
+            raise _Stop(
+                "failed", run["stage"], f"{where}: fields 'amplitude' and 'energy_weights' required"
+            )
         z = _complex_value(raw)
         if z is None:
             raise _Stop("failed", run["stage"], f"{where}: value not a finite scalar")
@@ -877,7 +1445,7 @@
         value = z.real
         if value == 0.0:
             continue
-        weights = _weights(run, wraw, where)
+        weights = _energy_weights(run, wraw, where)
         mult = _lapse_multiplier(run, weights, where)
         h_terms.append(value * mult)
         for cell, w in weights.items():
@@ -886,65 +1454,183 @@
     return math.fsum(h_terms), {c: math.fsum(v) for c, v in lapse_terms.items()}
 
 
+def _index_read_labels(run, labels):
+    """Once per run: index the operator's state-independent read labels."""
+    try:
+        lab_t = tuple(labels)
+    except TypeError:
+        raise _Stop("failed", run["stage"], "read_rows['labels'] is not a sequence")
+    index = {}
+    for i, lbl in enumerate(lab_t):
+        if not _hashable(lbl):
+            raise _Stop("failed", run["stage"], f"read_rows label {i} is not hashable")
+        if _label_kind(lbl) in _whitened_kinds():
+            raise _Stop(
+                "failed", run["stage"], f"operator read label {lbl!r} collides with callback labels"
+            )
+        if lbl in index:
+            raise _Stop("failed", run["stage"], f"read_rows: duplicate label {lbl!r}")
+        index[lbl] = i
+    missing = [lbl for lbl in run["needed_operator_labels"] if lbl not in index]
+    if missing:
+        raise _Stop(
+            "failed",
+            run["stage"],
+            f"referenced read labels {missing[:20]!r} are not operator read_rows labels (labels "
+            "are state independent; an absent object has value 0 and presence 0, not a "
+            "missing label)",
+        )
+    run["read_index"] = {lbl: index[lbl] for lbl in run["needed_operator_labels"]}
+    run["read_labels_ref"] = labels
+    run["read_labels_tuple"] = lab_t
+
+
+def _read_array(run, rows, name):
+    arr = rows[name]
+    n = len(run["read_labels_tuple"])
+    if type(arr) is not np.ndarray or arr.ndim != 1 or arr.shape[0] != n or arr.dtype.kind != "f":
+        raise _Stop("failed", run["stage"], f"read_rows['{name}'] is not a float array [{n}]")
+    if not bool(np.all(np.isfinite(arr))):
+        raise _Stop("failed", run["stage"], f"read_rows['{name}'] not finite")
+    return arr
+
+
+def _whitened_moments(run, reads):
+    """Validated whitened R'[cell] (3) and S'[cell] (3x3, exactly symmetric) of the callback."""
+    if not isinstance(reads, Mapping) or any(k not in reads for k in ("cells", "R", "S")):
+        raise _Stop("failed", run["stage"], "adapted_moment_reads did not return cells, R and S")
+    try:
+        cells = tuple(reads["cells"])
+    except TypeError:
+        raise _Stop("failed", run["stage"], "adapted_moment_reads['cells'] is not a sequence")
+    pair = run["pair"]
+    if pair["cells"] is None:
+        if len(set(cells)) != len(cells) or set(cells) != set(pair["j_R"]):
+            raise _Stop(
+                "failed",
+                run["stage"],
+                "adapter cells differ from the cells of the callback j_R/j_S sources",
+            )
+        pair["cells"] = cells
+    elif cells != pair["cells"]:
+        raise _Stop("failed", run["stage"], "adapter cells changed between states")
+    out_r = {}
+    out_s = {}
+    seq = (list, tuple, np.ndarray)
+    try:
+        for cell in cells:
+            vec = reads["R"][cell]
+            mat = reads["S"][cell]
+            r = [_real_value(x) for x in vec] if isinstance(vec, seq) and len(vec) == 3 else None
+            s = None
+            if isinstance(mat, seq) and len(mat) == 3 and all(
+                isinstance(row, seq) and len(row) == 3 for row in mat
+            ):
+                s = [[_real_value(x) for x in row] for row in mat]
+            if r is None or None in r or s is None or any(None in row for row in s):
+                raise _Stop("failed", run["stage"], f"adapter R/S of cell {cell!r} not finite real")
+            if any(s[i][j] != s[j][i] for i in range(3) for j in range(3)):
+                raise _Stop("failed", run["stage"], f"adapter S of cell {cell!r} not symmetric")
+            out_r[cell] = r
+            out_s[cell] = s
+    except (KeyError, TypeError) as exc:
+        raise _Stop("failed", run["stage"], f"adapter R/S not indexable by cell ({exc})")
+    return cells, out_r, out_s
+
+
 def _reads_at(run, state):
-    """Diagonal reads at `state`: operator rows plus caller extra reads (labels disjoint)."""
+    """Full diagonal reads at `state` (operator rows, callback whitened moments, pair source).
+
+    Returns (values for every referenced label, pair source value P(x), {coordinate index:
+    D_a of P}). The SAME evaluation feeds D, every D_a and the tracked time averages.
+    """
     rows = _op(run, "read_rows", context=run["context"], state=state)
-    if not isinstance(rows, (list, tuple)):
-        raise _Stop("failed", run["stage"], "read_rows did not return a list")
-    values = {}
-    kinds = {}
-    for i, rec in enumerate(rows):
-        present_l, label = _field(rec, "label")
-        present_v, raw = _field(rec, "value")
-        if not present_l or not present_v:
-            raise _Stop("failed", run["stage"], f"read_rows record {i}: label and value required")
-        if not _hashable(label):
-            raise _Stop("failed", run["stage"], f"read_rows record {i}: label not hashable")
-        v = _real_value(raw)
-        if v is None:
-            raise _Stop("failed", run["stage"], f"read_rows record {i}: value not finite real")
-        if label in values:
-            raise _Stop("failed", run["stage"], f"read_rows: duplicate label {label!r}")
-        values[label] = v
-        present_k, kind = _field(rec, "kind")
-        if present_k:
-            kinds[label] = kind
-    if run["extra"] is not None:
+    if not isinstance(rows, Mapping) or any(k not in rows for k in ("labels", "values", "presence")):
+        raise _Stop("failed", run["stage"], "read_rows did not return {labels, values, presence}")
+    labels = rows["labels"]
+    if run["read_labels_ref"] is None:
+        _index_read_labels(run, labels)
+    elif labels is not run["read_labels_ref"]:
         try:
-            extra = run["extra"](context=run["context"], state=state, rows=rows)
+            same = tuple(labels) == run["read_labels_tuple"]
+        except Exception:
+            same = False
+        if not same:
+            raise _Stop(
+                "failed", run["stage"], "read_rows labels changed between states (must be fixed)"
+            )
+    vals = _read_array(run, rows, "values")
+    _read_array(run, rows, "presence")
+    values = {lbl: float(vals[i]) for lbl, i in run["read_index"].items()}
+    pair = run["pair"]
+    pair_value = 0.0
+    pair_da = {}
+    if pair is not None:
+        fns = pair["fns"]
+        try:
+            reads = fns["adapted_moment_reads"](
+                operator_module=pair["operator_module"],
+                context=run["context"],
+                state=state,
+                binding=pair["binding"],
+            )
         except Exception as exc:
             raise _Stop(
-                "failed", run["stage"], f"extra_diagonal_reads raised {type(exc).__name__}: {exc}"
+                "failed", run["stage"], f"adapted_moment_reads raised {type(exc).__name__}: {exc}"
             )
-        if not isinstance(extra, Mapping):
-            raise _Stop("failed", run["stage"], "extra_diagonal_reads did not return a mapping")
-        for label, raw in extra.items():
-            if label in values:
-                raise _Stop(
-                    "failed", run["stage"], f"extra read label {label!r} collides with a read row"
-                )
-            v = _real_value(raw)
-            if v is None:
-                raise _Stop("failed", run["stage"], f"extra read {label!r} not finite real")
-            values[label] = v
-            kinds[label] = "extra_diagonal_read"
-    pending = run["labels_unseen"]
-    if pending:
-        seen = [lbl for lbl in pending if lbl in values]
-        for lbl in seen:
-            pending.discard(lbl)
-    return values, kinds
+        cells, r_w, s_w = _whitened_moments(run, reads)
+        for lbl in run["needed_whitened"]:
+            if lbl[0] == "whitened_R":
+                values[lbl] = r_w[lbl[1]][int(lbl[2])]
+            else:
+                values[lbl] = s_w[lbl[1]][int(lbl[2])][int(lbl[3])]
+        try:
+            raw_p = fns["pair_source_hamiltonian"](reads=reads, j_R=pair["j_R"], j_S=pair["j_S"])
+        except Exception as exc:
+            raise _Stop(
+                "failed",
+                run["stage"],
+                f"pair_source_hamiltonian raised {type(exc).__name__}: {exc}",
+            )
+        pv = _real_value(raw_p)
+        if pv is None:
+            raise _Stop("failed", run["stage"], "pair_source_hamiltonian value not finite real")
+        terms = []
+        for cell in cells:
+            jr = pair["j_R"][cell]
+            js = pair["j_S"][cell]
+            for i in range(3):
+                terms.append(-jr[i] * r_w[cell][i])
+                for j in range(3):
+                    terms.append(-js[i][j] * s_w[cell][i][j])
+        recon = math.fsum(terms)
+        scale = math.fsum(abs(x) for x in terms)
+        if not abs(pv - recon) <= pair["tol"] * scale:
+            raise _Stop(
+                "failed",
+                run["stage"],
+                f"pair_source_hamiltonian {pv!r} differs from -j_R.R' - J_S:S' = {recon!r} beyond "
+                "source_consistency_tolerance (H_c and its source derivatives would disagree)",
+            )
+        pair_value = pv
+        for idx, coord in run["pair_coords"]:
+            i = int(coord[2])
+            if coord[0] == "pair_source_R":
+                pair_da[idx] = -r_w[coord[1]][i]
+            else:
+                j = int(coord[3])
+                pair_da[idx] = -(1.0 if i == j else 2.0) * s_w[coord[1]][i][j]
+    return values, pair_value, pair_da
 
 
-def _segment_at(run, state):
-    """Dwell-segment record {state, key, D, r, Da} at `state` and its channels."""
+def _segment_core(run, state):
+    """Dwell-segment record {state, key, D, r (lazy), Da, row} from FULL diagonal reads."""
     key = _state_key(run, state)
-    channels, exit_rate = _channels_at(run, state)
     d_h, d_lapse = _diagonal_at(run, state)
-    values, _ = _reads_at(run, state)
-    src = math.fsum([-j * values.get(lbl, 0.0) for lbl, j in run["sources"].items()])
-    vol = math.fsum([a * values.get(lbl, 0.0) for lbl, a in run["volume_gradient"].items()])
-    diag = math.fsum([d_h, src, -run["lam"] * vol])
+    values, pair_value, pair_da = _reads_at(run, state)
+    src = math.fsum([-j * values[lbl] for lbl, j in run["sources"].items()])
+    vol = math.fsum([a * values[lbl] for lbl, a in run["volume_gradient"].items()])
+    diag = math.fsum([d_h, src, pair_value, -run["lam"] * vol])
     if not math.isfinite(diag):
         raise _Stop("failed", run["stage"], "diagonal energy D(x) not finite")
     da = np.zeros(run["n_u"], dtype=np.float64)
@@ -952,13 +1638,31 @@
         if coord[0] == "lapse":
             da[idx] = d_lapse[coord[1]]
         elif coord[0] == "source":
-            da[idx] = -values.get(coord[1], 0.0)
-        else:
+            da[idx] = -values[coord[1]]
+        elif coord[0] == "volume_multiplier":
             da[idx] = -vol
-    seg = {"state": state, "key": key, "D": diag, "r": exit_rate, "Da": da}
+        else:
+            da[idx] = pair_da[idx]
+    row = np.array([values[lbl] for lbl in run["tracked"]], dtype=np.float64)
+    return {"state": state, "key": key, "D": diag, "r": None, "Da": da, "row": row}
+
+
+def _segment_at(run, state):
+    """Dwell-segment record with its full exit rate, and the state's full channels."""
+    seg = _segment_core(run, state)
+    channels, exit_rate = _channels_at(run, state)
+    seg["r"] = exit_rate
     return seg, channels
 
 
+def _seg_rate(run, seg):
+    """Full exit rate r(x) of a segment, enumerated lazily (palette-created segments)."""
+    if seg["r"] is None:
+        _, exit_rate = _channels_at(run, seg["state"])
+        seg["r"] = exit_rate
+    return seg["r"]
+
+
 def _target_key(run, ch):
     if not ch["has_key"]:
         ch["key"] = _state_key(run, ch["target"])
@@ -1075,7 +1779,7 @@
     }
 
 
-def _clipped_integral(segments, times, horizon, length):
+def _clipped_integral(run, segments, times, horizon, length):
     """int_0^length (r - D) d tau; segment j spans [t_j, t_{j+1}), t_0 = 0, t_{K+1} = horizon."""
     terms = []
     k = len(times)
@@ -1086,7 +1790,7 @@
         hi = times[j] if j < k else horizon
         if hi > length:
             hi = length
-        terms.append((segments[j]["r"] - segments[j]["D"]) * (hi - lo))
+        terms.append((_seg_rate(run, segments[j]) - segments[j]["D"]) * (hi - lo))
     return math.fsum(terms)
 
 
@@ -1103,6 +1807,8 @@
 def _ctmc_segment(run, start_seg, length, rng, outside_events):
     """Unconditioned reference CTMC (rates W, holding rate r) from start_seg for `length`."""
     channels, exit_rate = _channels_at(run, start_seg["state"])
+    if start_seg["r"] is None:
+        start_seg["r"] = exit_rate
     segments = [start_seg]
     events = []
     times = []
@@ -1147,30 +1853,49 @@
     return segments, events, times
 
 
-def _interval_move(run, path, rng, diag):
-    """One move: rotation (prob p_rot) or interval regrowth with endpoint rejection."""
+def _select_interval(run, rng, diag, prefix):
+    """Source-independent symmetric interval density (L10): (origin, whole, length) or None."""
     beta = run["beta"]
     mp = run["moves"]
-    if float(rng.random()) < mp["rotation_probability"]:
-        diag["rotations"] += 1
-        return _rotate(run, path, float(rng.random()) * beta), False
     origin = float(rng.random()) * beta
     whole = float(rng.random()) < mp["whole_circle_probability"]
     if whole:
-        length = beta
-        diag["whole_circle_proposals"] += 1
-    else:
-        u = float(rng.random())
-        frac = mp["cumulative_components"][-1][1]
-        for cum, f in mp["cumulative_components"]:
-            if u < cum:
-                frac = f
-                break
-        length = float(rng.random()) * frac * beta
-        diag["interval_proposals"] += 1
-        if not length > 0.0:
-            diag["zero_length_intervals"] += 1
-            return path, False
+        diag[prefix + "whole_circle_proposals"] += 1
+        return origin, True, beta
+    u = float(rng.random())
+    frac = mp["cumulative_components"][-1][1]
+    for cum, f in mp["cumulative_components"]:
+        if u < cum:
+            frac = f
+            break
+    length = float(rng.random()) * frac * beta
+    diag[prefix + "interval_proposals"] += 1
+    if not length > 0.0:
+        diag[prefix + "zero_length_intervals"] += 1
+        return None
+    return origin, False, length
+
+
+def _move(run, path, rng, diag):
+    """Move type by state-independent probabilities: rotation, palette (if enabled), global."""
+    u = float(rng.random())
+    p_rot = run["moves"]["rotation_probability"]
+    if u < p_rot:
+        diag["rotations"] += 1
+        return _rotate(run, path, float(rng.random()) * run["beta"]), False
+    pal = run["palette"]
+    if pal is not None and u < p_rot + pal["selection_probability"]:
+        return _palette_move(run, path, rng, diag)
+    return _interval_move(run, path, rng, diag)
+
+
+def _interval_move(run, path, rng, diag):
+    """Global interval regrowth with endpoint rejection (SPEC section 3; the v001 move)."""
+    beta = run["beta"]
+    sel = _select_interval(run, rng, diag, "")
+    if sel is None:
+        return path, False
+    origin, whole, length = sel
     rot = _rotate(run, path, origin)
     k = len(rot["times"])
     if whole:
@@ -1180,7 +1905,6 @@
         if m < k and rot["times"][m] == length:
             raise _Stop("failed", run["stage"], "interval end coincides with an event time (L15)")
     terminal = rot["segments"][m]
-    old_int = _clipped_integral(rot["segments"], rot["times"], beta, length)
     segs, evs, times = _ctmc_segment(run, rot["segments"][0], length, rng, k - m)
     if not _keys_equal(run, segs[-1]["key"], terminal["key"]):
         diag["endpoint_rejections"] += 1
@@ -1192,7 +1916,8 @@
             "gauge increments of two segments between the same endpoints differ: primitive "
             "kind labels are inconsistent with a state-function gauge (L2)",
         )
-    new_int = _clipped_integral(segs, times, length, length)
+    old_int = _clipped_integral(run, rot["segments"], rot["times"], beta, length)
+    new_int = _clipped_integral(run, segs, times, length, length)
     log_acc = new_int - old_int
     if not math.isfinite(log_acc):
         raise _Stop("failed", run["stage"], "log acceptance ratio not finite")
@@ -1211,6 +1936,175 @@
     return _rotate(run, new_path, back), True
 
 
+def _choose_palette(pal, rng):
+    u = float(rng.random())
+    owners = pal["cumulative"][-1][1]
+    for cum, s in pal["cumulative"]:
+        if u < cum:
+            owners = s
+            break
+    return owners
+
+
+def _count_new_event(run, path_events):
+    """Event caps for palette proposals (incomplete, never a rejection; L14)."""
+    caps = run["caps"]
+    counters = run["counters"]
+    if counters["events"] >= caps["max_total_events"]:
+        raise _Stop(
+            "incomplete",
+            run["stage"],
+            "cap max_total_events reached; computation ended (no path was rejected)",
+        )
+    if path_events > caps["max_events_per_path"]:
+        raise _Stop(
+            "incomplete",
+            run["stage"],
+            "cap max_events_per_path reached by a palette proposal; computation ended "
+            "(the proposal was not rejected, so no high-event path is excluded)",
+        )
+    counters["events"] += 1
+
+
+def _palette_move(run, path, rng, diag):
+    """Additive blocked-palette move (PALETTE; L19).
+
+    Outside-palette marks inside the interval are held (times and (kind, owner_id)
+    descriptors); between them only member channels run with their actual rates and total
+    r_S; held marks are replayed on the proposed state (absent or zero rate -> reject);
+    endpoint mismatch rejects; log ratio int_I new(r_S - D) - int_I old(r_S - D) +
+    sum_held log(W_new / W_old). Unconditioned generation plus rejection, never a bridge.
+    """
+    beta = run["beta"]
+    owners = _choose_palette(run["palette"], rng)
+    sel = _select_interval(run, rng, diag, "palette_")
+    if sel is None:
+        return path, False
+    origin, whole, length = sel
+    diag["palette_proposals"] += 1
+    rot = _rotate(run, path, origin)
+    k = len(rot["times"])
+    if whole:
+        m = k
+    else:
+        m = bisect.bisect_left(rot["times"], length)
+        if m < k and rot["times"][m] == length:
+            raise _Stop(
+                "failed", run["stage"], "palette interval end coincides with an event time (L15)"
+            )
+    terminal = rot["segments"][m]
+    held = []
+    for i in range(m):
+        ev = rot["events"][i]
+        if _record_groups(run, ev["kind"], ev["owner"]).isdisjoint(owners):
+            held.append((rot["times"][i], ev))
+    outside = k - m
+    pending = len(held)
+    current = rot["segments"][0]
+    channels, r_s = _palette_channels(run, current["state"], owners)
+    segs = [current]
+    rates = [r_s]
+    evs = []
+    times = []
+    t = 0.0
+    log_held = 0.0
+    for bound, hev in held + [(length, None)]:
+        while r_s > 0.0:
+            dt = float(rng.exponential(1.0 / r_s))
+            t_next = t + dt
+            if t_next >= bound:
+                break
+            if not t_next > t:
+                raise _Stop("failed", run["stage"], "zero holding time in floating point (L15)")
+            chosen = _choose_channel(channels, r_s, rng)
+            _count_new_event(run, len(evs) + 1 + pending + outside)
+            y_seg = _segment_core(run, chosen["target"])
+            chosen["key"] = y_seg["key"]
+            chosen["has_key"] = True
+            _no_self_loop(run, current, y_seg, chosen)
+            y_channels, y_rs = _palette_channels(run, y_seg["state"], owners)
+            _reverse_check(run, current, channels, chosen, y_seg, y_channels)
+            evs.append(_event_from_channel(run, chosen))
+            times.append(t_next)
+            segs.append(y_seg)
+            rates.append(y_rs)
+            current, channels, r_s, t = y_seg, y_channels, y_rs, t_next
+        if hev is None:
+            break
+        groups = _record_groups(run, hev["kind"], hev["owner"])
+        x_channels, _ = _palette_channels(run, current["state"], groups)
+        matches = [
+            c for c in x_channels
+            if c["kind"] == hev["kind"] and _keys_equal(run, c["owner"], hev["owner"])
+        ]
+        if len(matches) > 1:
+            raise _Stop(
+                "failed",
+                run["stage"],
+                f"held descriptor (kind {hev['kind']!r}, owner {hev['owner']!r}) matches "
+                f"{len(matches)} positive-rate records at one state; a held replay must be "
+                "deterministic (L19)",
+            )
+        if not matches:
+            diag["palette_held_rejections"] += 1  # illegal held event or zero held rate
+            return path, False
+        held_ch = matches[0]
+        pending -= 1
+        _count_new_event(run, len(evs) + 1 + pending + outside)
+        y_seg = _segment_core(run, held_ch["target"])
+        held_ch["key"] = y_seg["key"]
+        held_ch["has_key"] = True
+        _no_self_loop(run, current, y_seg, held_ch)
+        y_held, _ = _palette_channels(run, y_seg["state"], groups)
+        _reverse_check(run, current, x_channels, held_ch, y_seg, y_held)
+        log_held += math.log(held_ch["W"]) - math.log(hev["W"])
+        evs.append(_event_from_channel(run, held_ch))
+        times.append(bound)
+        channels, r_s = _palette_channels(run, y_seg["state"], owners)
+        segs.append(y_seg)
+        rates.append(r_s)
+        current, t = y_seg, bound
+    if not _keys_equal(run, current["key"], terminal["key"]):
+        diag["palette_endpoint_rejections"] += 1
+        return path, False
+    if _net_increments(evs) != _net_increments(rot["events"][:m]):
+        raise _Stop(
+            "failed",
+            run["stage"],
+            "gauge increments of two segments between the same endpoints differ: primitive "
+            "kind labels are inconsistent with a state-function gauge (L2)",
+        )
+    old_terms = []
+    for j in range(m + 1):
+        lo = 0.0 if j == 0 else rot["times"][j - 1]
+        hi = rot["times"][j] if j < m else length
+        seg = rot["segments"][j]
+        _, r_old = _palette_channels(run, seg["state"], owners)
+        old_terms.append((r_old - seg["D"]) * (hi - lo))
+    new_terms = []
+    for j, seg in enumerate(segs):
+        lo = 0.0 if j == 0 else times[j - 1]
+        hi = times[j] if j < len(times) else length
+        new_terms.append((rates[j] - seg["D"]) * (hi - lo))
+    log_acc = math.fsum(new_terms) - math.fsum(old_terms) + log_held
+    if not math.isfinite(log_acc):
+        raise _Stop("failed", run["stage"], "palette log acceptance ratio not finite")
+    if log_acc < 0.0 and not float(rng.random()) < math.exp(log_acc):
+        diag["palette_metropolis_rejections"] += 1
+        return path, False
+    new_path = {
+        "segments": segs + rot["segments"][m + 1:],
+        "events": evs + rot["events"][m:],
+        "times": times + rot["times"][m:],
+    }
+    _check_times(run, new_path["times"], beta)
+    diag["palette_accepted"] += 1
+    back = beta - origin
+    if not back < beta:
+        back = 0.0
+    return _rotate(run, new_path, back), True
+
+
 def _initial_path(run, spec):
     """Admit a caller closed path (x0 plus events) or a constant path (no events)."""
     beta = run["beta"]
@@ -1286,22 +2180,8 @@
     score = -np.einsum("l,la->a", dur, da, optimize=False) + rho.sum(axis=0)
     contact = -np.einsum("ka,kb->ab", rho, rho, optimize=False)
     reads = np.zeros((k + 1, n_r), dtype=np.float64)
-    cache = {}
-    tracked = run["tracked"]
     for j, seg in enumerate(segments):
-        key = seg["key"]
-        cacheable = _hashable(key)
-        if cacheable and key in cache:
-            reads[j] = cache[key]
-            continue
-        values, kinds = _reads_at(run, seg["state"])
-        row = np.array([values.get(lbl, 0.0) for lbl in tracked], dtype=np.float64)
-        for lbl in tracked:
-            if lbl in kinds and lbl not in run["tracked_kinds"]:
-                run["tracked_kinds"][lbl] = kinds[lbl]
-        reads[j] = row
-        if cacheable:
-            cache[key] = row
+        reads[j] = seg["row"]  # the same full read evaluation that entered D and D_a
     read_avg = np.einsum("l,lr->r", dur, reads, optimize=False) / beta
     return score, contact, read_avg, k
 
@@ -1529,15 +2409,27 @@
         "direction_status": None,
         "tracked_read_labels": None,
         "read_kinds": None,
+        "member_check": None,
         "estimates": None,
         "errors": None,
         "mixing": None,
         "diagnostics": None,
         "conventions": {
             "hamiltonian": (
-                "H_c = H[N] - sum_a j_a O_a - lambda A, H[N] = H + sum_alpha n_alpha E_alpha, "
-                "n = N - 1; per primitive multiplier 1 + sum_alpha n_alpha wbar_alphaX applied "
-                "BEFORE aggregation; beta is one global inverse energy"
+                "H_c = H[N] - sum_a j_a O_a - j_R'.R' - J_S':S' - lambda A, H[N] = H + "
+                "sum_alpha n_alpha E_alpha, n = N - 1; per primitive multiplier 1 + sum_alpha "
+                "n_alpha wbar_alphaX applied BEFORE aggregation; beta is one global inverse "
+                "energy; the pair term is the root adapter's pair_source_hamiltonian"
+            ),
+            "pair_sources": (
+                "R', S' whitened, configuration-normalized (current present count) coarse "
+                "moments from adapted_moment_reads; j_R', J_S' whitened duals (caller input, or "
+                "converted once by raw_to_whitened_sources); ('pair_source_S', cell, i, j), "
+                "i <= j, moves J_S'[i][j] = J_S'[j][i] together: multiplicity 1 (i == j) or 2"
+            ),
+            "moves": (
+                "rotation (p_rot), additive blocked palette (p_palette, PALETTE note) and global "
+                "interval regrowth (1 - p_rot - p_palette > 0), all state independent"
             ),
             "positive_gauge": (
                 "G = (-1)^{sum q} (-e^{i admission_phase})^{N_S} (-e^{i birth_phase})^{N}; "
@@ -1559,8 +2451,10 @@
             ),
             "affine_coordinates": (
                 "('lapse', cell) differentiates n_alpha (= N_alpha), ('source', label) j_label, "
-                "('volume_multiplier',) lambda; second-source contacts are exactly zero in these "
-                "coordinates; other coordinates by the caller's chain rule"
+                "('volume_multiplier',) lambda, ('pair_source_R', cell, i) j_R'[cell][i], "
+                "('pair_source_S', cell, i, j) the symmetric pair J_S'[i][j]; second-source "
+                "contacts are exactly zero in these coordinates; other coordinates (raw-frame "
+                "sources included) by the caller's chain rule"
             ),
         },
         "scope": (
@@ -1591,9 +2485,10 @@
     gauge_phases,
     derivative_coordinates,
     tracked_read_labels,
-    extra_diagonal_reads,
+    diagonal_read_source_callback,
     chain_generators,
     move_parameters,
+    palette_parameters,
     caps,
     burn_in_sweeps,
     measurement_sweeps,
@@ -1604,36 +2499,54 @@
     """Static joint source Hessians of the owned collective by positive worldline sampling.
 
     Arguments (keyword-only, all required, no defaults; no value is chosen here):
-      operator_api: mapping/object with the state-level callables listed in the module
+      operator_api: mapping/object with the ACTUAL state-level callables listed in the module
         docstring (validate_owned_model, canonical_state_key, primitive_channels,
-        diagonal_terms, read_rows), supplied at run time; nothing is imported.
+        diagonal_terms, read_rows; plus owner_restricted_channels when palette_parameters is
+        not None), supplied at run time; nothing is imported.
       graph0, model, registration: passed unchanged to validate_owned_model. The model must
         be the common-phase zero-holonomy member (real h, t, g > 0, zero hopping phases,
-        uniform admission phase, common Birth phase, real diagonals); violations found at
-        visited states return status "unsupported".
+        uniform admission phase, common Birth phase, real diagonals). Before sampling,
+        _model_member_check verifies this on EVERY supplied coefficient of the model
+        mapping (every edge key including newborn/child edges, every vertex, every owner),
+        independent of which states the chains visit; a violation, an unknown schema key or
+        a profile it cannot evaluate returns status "unsupported". Every primitive at every
+        visited state is checked again (second line).
       initial_paths: one entry per chain, {"x0": state, "events": [ {tau, kind, owner_id,
         target_key}, ... ]}; an empty event list is the constant path at x0. Events must
         have 0 < tau strictly increasing < beta, match exactly one positive-rate primitive
         and close at x0. All chains must lie in one declared conserved-resource component.
       beta: finite real > 0 (one global inverse energy).
-      lapse_factors: {cell: N_alpha > 0} for every coarse cell appearing in any weight.
-      source_coefficients: {read label: j_a} (may be empty); H_c gains -sum j_a O_a.
-      volume_gradient_coefficients: {read label: a_a} with A = sum a_a O_a (may be empty).
+      lapse_factors: {cell: N_alpha > 0} for exactly the cells of context.energy_cells.
+      source_coefficients: {operator read label: j_a} (may be empty); H_c gains -sum j_a O_a.
+      volume_gradient_coefficients: {read label: a_a} with A = sum a_a O_a (may be empty;
+        whitened callback labels allowed).
       volume_multiplier: lambda (finite real); H_c gains -lambda A.
       gauge_phases: {"admission_phase": arg kappa, "birth_phase": arg epsilon} of the
         member's common phases (radians).
       derivative_coordinates: list of ("lapse", cell) | ("source", label) |
-        ("volume_multiplier",).
+        ("volume_multiplier",) | ("pair_source_R", cell, i) | ("pair_source_S", cell, i, j)
+        with i <= j (pair coordinates need the callback; L20).
       tracked_read_labels: list of read labels whose time averages, means and responses
-        are returned (presence, first-moment Z, pair, or extra reads).
-      extra_diagonal_reads: None or callable(*, context, state, rows) -> {label: real} for
-        caller/registration diagonal reads (e.g. coarse R, S with current 1/m_alpha);
-        labels must not collide with operator read rows.
+        are returned (operator presence, first-moment Z, pair, population rows, or
+        ("whitened_R", cell, i) / ("whitened_S", cell, i, j), i <= j, from the callback).
+        Operator coarse_first_R / coarse_second_S rows are unsupported in every role (L8).
+      diagonal_read_source_callback: None, or the root adapter path {"adapter": object
+        exposing adapted_moment_reads and pair_source_hamiltonian (and
+        raw_to_whitened_sources for source_frame "raw"), "operator_module": object passed
+        unchanged as operator_module (must expose state_labels), "binding": the adapter
+        binding whose "graph0" and "registration" are the SAME objects as graph0 and
+        registration, "source_frame": "whitened" | "raw", "j_R": {cell: 3 reals}, "j_S":
+        {cell: symmetric 3x3 reals}, "source_consistency_tolerance": real >= 0}. Its reads
+        are evaluated at every new state and used in D, every D_a and every time average.
       chain_generators: list of distinct numpy.random.Generator, one per chain (same
         length as initial_paths); all randomness of chain c uses chain_generators[c].
       move_parameters: {"moves_per_sweep": int >= 1, "rotation_probability": (0,1),
         "whole_circle_probability": (0,1), "length_components": [(weight > 0,
         upper_fraction in (0,1]), ...] with at least one upper_fraction == 1}.
+      palette_parameters: None (no palette move) or {"selection_probability": (0,1) with
+        rotation_probability + selection_probability < 1, "palettes": [(weight > 0,
+        nonempty collection of original owner labels), ...],
+        "verify_against_full_enumeration": bool}; the additive blocked-palette move (L19).
       caps: {"max_events_per_path", "max_total_events", "max_sweeps",
         "max_channel_enumerations"} positive ints; reaching any ends the run "incomplete".
       burn_in_sweeps: int >= 0. measurement_sweeps: int >= 1 (one measurement per sweep).
@@ -1646,7 +2559,7 @@
         anything else returns status "unsupported".
 
     Returns a dict: ok, status, stage_reached, failures, flags, inputs, coordinate_order,
-    direction_status, tracked_read_labels, read_kinds, estimates {dlogZ_du, d2logZ_du2,
+    direction_status, tracked_read_labels, read_kinds, member_check, estimates {dlogZ_du, d2logZ_du2,
     score_covariance, contact_mean, F (None), F_u, F_uu, read_means, read_mean_responses,
     per_chain, mean/max events per path, samples}, errors (only when mixing passed),
     mixing, diagnostics, conventions, scope, limitations. "ok" is True only when status is
@@ -1658,14 +2571,15 @@
     if implicit_closure is not None:
         result["status"] = "unsupported"
         failures.append(
-            "implicit_closure: v001 implements ordinary fixed-source equilibrium sampling only; "
+            "implicit_closure: v002 implements ordinary fixed-source equilibrium sampling only; "
             "the SPEC section 5 implicit HP volume closure is a retained later contract, so "
             "implicit_closure must be None"
         )
         return result
 
     kinds = _kind_table()
-    api = _admit_operator_api(operator_api, failures)
+    unsupported = []
+    api = _admit_operator_api(operator_api, palette_parameters is not None, failures)
     beta_in = _admit_real("beta", beta, failures)
     if beta_in is not None and not beta_in > 0.0:
         failures.append(f"input beta: must be > 0, got {beta_in!r}")
@@ -1675,10 +2589,12 @@
     vgrad = _admit_label_reals("volume_gradient_coefficients", volume_gradient_coefficients, failures)
     lam = _admit_real("volume_multiplier", volume_multiplier, failures)
     phases = _admit_gauge_phases(gauge_phases, failures)
-    coords = _admit_coordinates(derivative_coordinates, lapse, failures)
+    pair = _admit_pair_callback(diagonal_read_source_callback, graph0, registration, failures)
+    pair_cells = None if pair is None else set(pair["j_R"])
+    coords = _admit_coordinates(derivative_coordinates, lapse, pair_cells, failures)
     tracked = _admit_labels("tracked_read_labels", tracked_read_labels, failures)
-    if extra_diagonal_reads is not None and not callable(extra_diagonal_reads):
-        failures.append("input extra_diagonal_reads: must be None or a callable")
+    if None not in (sources, vgrad, tracked, coords):
+        _admit_label_roles(sources, vgrad, tracked, coords, pair_cells, failures, unsupported)
     gens = _admit_generators(chain_generators, failures)
     paths_in = _admit_initial_paths(initial_paths, kinds, failures)
     if gens is not None and paths_in is not None and len(gens) != len(paths_in):
@@ -1686,6 +2602,16 @@
             f"input chain_generators ({len(gens)}) and initial_paths ({len(paths_in)}) differ in length"
         )
     moves = _admit_move_parameters(move_parameters, failures)
+    palette = _admit_palette_parameters(palette_parameters, failures)
+    if moves is not None and palette is not None and not (
+        moves["rotation_probability"] + palette["selection_probability"] < 1.0
+    ):
+        failures.append(
+            "input palette_parameters['selection_probability']: rotation_probability + "
+            "selection_probability must be < 1 so the global regrowth keeps nonzero "
+            "selection probability (blocked moves alone are not claimed irreducible)"
+        )
+        palette = None
     caps_in = _admit_caps(caps, failures)
     burn = _admit_int("burn_in_sweeps", burn_in_sweeps, 0, failures)
     n_meas = _admit_int("measurement_sweeps", measurement_sweeps, 1, failures)
@@ -1702,12 +2628,21 @@
         "gauge_phases": phases,
         "derivative_coordinates": coords,
         "tracked_read_labels": tracked,
-        "extra_diagonal_reads": None if extra_diagonal_reads is None else "callable",
+        "diagonal_read_source_callback": None if pair is None else {
+            "source_frame": pair["source_frame"],
+            "cells": len(pair["j_R"]),
+            "source_consistency_tolerance": pair["tol"],
+        },
         "chains": None if gens is None else len(gens),
         "move_parameters": None if moves is None else {
             k: moves[k] for k in ("moves_per_sweep", "rotation_probability",
                                   "whole_circle_probability", "length_components")
         },
+        "palette_parameters": None if palette is None else {
+            "selection_probability": palette["selection_probability"],
+            "palettes": [(w, sorted(map(repr, s))) for w, s in palette["palettes"]],
+            "verify_against_full_enumeration": palette["verify"],
+        },
         "caps": caps_in,
         "burn_in_sweeps": burn,
         "measurement_sweeps": n_meas,
@@ -1716,6 +2651,11 @@
     }
     if failures:
         result["status"] = "failed"
+        failures.extend(unsupported)
+        return result
+    if unsupported:
+        result["status"] = "unsupported"
+        failures.extend(unsupported)
         return result
 
     referenced = set(sources) | set(vgrad) | set(tracked)
@@ -1734,8 +2674,18 @@
         "lam": lam,
         "tracked": tracked,
         "n_r": len(tracked),
-        "tracked_kinds": {},
-        "extra": extra_diagonal_reads,
+        "pair": None if pair is None else dict(pair, cells=None),
+        "pair_coords": [(i, c) for i, c in enumerate(coords)
+                        if c[0] in ("pair_source_R", "pair_source_S")],
+        "needed_operator_labels": [lbl for lbl in referenced
+                                   if _label_kind(lbl) not in _whitened_kinds()],
+        "needed_whitened": [lbl for lbl in referenced if _label_kind(lbl) in _whitened_kinds()],
+        "read_index": None,
+        "read_labels_ref": None,
+        "read_labels_tuple": None,
+        "energy_cells": None,
+        "group": None,
+        "palette": palette,
         "kinds": kinds,
         "gauge": _gauge_table(kinds, phases),
         "tol": tol,
@@ -1746,9 +2696,11 @@
             "channel_enumerations": 0,
             "sweeps": 0,
             "reverse_signature_fallbacks": 0,
+            "restricted_enumerations": 0,
+            "restricted_nonmember_records_dropped": 0,
+            "palette_verifications": 0,
         },
         "zero_rate_directions": set(),
-        "labels_unseen": set(referenced),
     }
     chain_diag = []
 
@@ -1756,11 +2708,10 @@
         return {
             "counters": dict(run["counters"]),
             "chains": [dict(d) for d in chain_diag],
-            "labels_never_observed": sorted(map(repr, run["labels_unseen"])),
             "zero_rate_directions": sorted(map(repr, run["zero_rate_directions"])),
         }
 
-    # ---- Stage: model validation (operator owns the model-level checks) ----------
+    # ---- Stage: operator schema validation (the member check follows; L2) --------
     result["stage_reached"] = "model"
     try:
         validated = api["validate_owned_model"](
@@ -1780,6 +2731,77 @@
         return result
     run["context"] = validated["context"]
 
+    # ---- Stage: model-level member check (state independent; L2a) ----------------
+    result["stage_reached"] = "member_check"
+    m_ok, m_problems, m_forms = _model_member_check(model, phases, tol["gauge_phase"])
+    result["member_check"] = {
+        "status": "verified" if m_ok else "unsupported",
+        "profile_forms": m_forms,
+        "problems": m_problems,
+        "note": (
+            "every supplied coefficient of the model mapping checked before sampling; the "
+            "per-primitive gauge check at visited states remains a second line (L2)"
+        ),
+    }
+    if not m_ok:
+        result["status"] = "unsupported"
+        failures.append(
+            "model is not verified to lie in the common-phase zero-holonomy member (checked on "
+            "every supplied coefficient, independent of visited states)"
+        )
+        failures.extend(f"member_check: {p}" for p in m_problems)
+        return result
+
+    # ---- Stage: binding of energy cells, palette groups and dual sources --------------
+    result["stage_reached"] = "binding"
+    present_c, cells = _field(run["context"], "energy_cells")
+    if not present_c or not isinstance(cells, (list, tuple)) or not all(_hashable(c) for c in cells):
+        result["status"] = "failed"
+        failures.append("context.energy_cells is missing or not a sequence of hashable cells")
+        return result
+    if len(set(cells)) != len(cells) or set(cells) != set(lapse):
+        result["status"] = "failed"
+        failures.append(
+            "lapse_factors must cover exactly the cells of context.energy_cells (one N_alpha > 0 "
+            "per coarse cell; energy_weights are aligned with that order)"
+        )
+        return result
+    run["energy_cells"] = tuple(cells)
+    if palette is not None:
+        try:
+            originals = list(graph0["A"]) + list(graph0["B"])
+            group = {o: o for o in originals}
+            for o in originals:
+                for lab in graph0["slots"][o]:
+                    group[lab] = o
+        except (TypeError, KeyError) as exc:
+            result["status"] = "failed"
+            failures.append(f"graph0 permanent owner groups cannot be read for the palette: {exc}")
+            return result
+        bad = [sorted(map(repr, s - set(originals))) for _, s in palette["palettes"]
+               if not s <= set(originals)]
+        if bad:
+            result["status"] = "failed"
+            failures.append(f"palette_parameters: labels {bad!r} are not original owner labels")
+            return result
+        run["group"] = group
+    if pair is not None and pair["source_frame"] == "raw":
+        try:
+            converted = pair["fns"]["raw_to_whitened_sources"](
+                j_R_raw=pair["j_R"], j_S_raw=pair["j_S"]
+            )
+            conv_r, conv_s = converted
+        except Exception as exc:
+            result["status"] = "failed"
+            failures.append(f"raw_to_whitened_sources failed: {type(exc).__name__}: {exc}")
+            return result
+        whitened = _admit_pair_sources(conv_r, conv_s, "raw_to_whitened_sources output", failures)
+        if whitened is None or set(whitened[0]) != set(pair["j_R"]):
+            result["status"] = "failed"
+            failures.append("raw_to_whitened_sources did not return sources on the same cells")
+            return result
+        run["pair"]["j_R"], run["pair"]["j_S"] = whitened
+
     n_u = run["n_u"]
     n_r = run["n_r"]
     series = []
@@ -1804,6 +2826,14 @@
                 "zero_length_intervals": 0,
                 "endpoint_rejections": 0,
                 "metropolis_rejections": 0,
+                "palette_proposals": 0,
+                "palette_interval_proposals": 0,
+                "palette_whole_circle_proposals": 0,
+                "palette_zero_length_intervals": 0,
+                "palette_held_rejections": 0,
+                "palette_endpoint_rejections": 0,
+                "palette_metropolis_rejections": 0,
+                "palette_accepted": 0,
                 "accepted_regrowths": 0,
                 "accepted_in_measurement": 0,
                 "sweeps_completed": 0,
@@ -1825,7 +2855,7 @@
                 run["stage"] = f"chain {c} sweep {sweep}"
                 measuring = sweep >= burn
                 for _ in range(moves["moves_per_sweep"]):
-                    path, accepted = _interval_move(run, path, rng, diag)
+                    path, accepted = _move(run, path, rng, diag)
                     if accepted:
                         diag["accepted_regrowths"] += 1
                         if measuring:
@@ -1877,7 +2907,7 @@
     all_events = np.concatenate([ser["events"] for ser in series])
     result["coordinate_order"] = [coords[i] for i in supported]
     result["tracked_read_labels"] = list(tracked)
-    result["read_kinds"] = [run["tracked_kinds"].get(lbl) for lbl in tracked]
+    result["read_kinds"] = [_label_kind(lbl) for lbl in tracked]
     result["estimates"] = {
         "beta": beta_f,
         "dlogZ_du": point["g"],
@@ -1900,11 +2930,6 @@
     result["mixing"] = mixing
     result["errors"] = errors
     result["diagnostics"] = _diagnostics()
-    if run["labels_unseen"]:
-        result["flags"].append(
-            "some referenced labels were never present in any visited state's reads (value 0 "
-            "throughout); see diagnostics.labels_never_observed"
-        )
     if mixing["constant_columns"]:
         result["flags"].append(
             "constant columns (no sample variation in any chain) are listed in "
```
