# DELTA 0410 MODES V003: owned collective worldline static response, v002 → v003

Author: the author of the UNT 0410 modes delta (Claude, static only). Nothing was imported, executed or sampled.

- No numerical run was made.
- The only Python run was `python3 -I -B` doing `ast.parse`, `compile` and `symtable` on TEXT copies in my own scratch directory.
- No `__pycache__` exists in the 0407 directory.
- I made no write in `Universal Network Theory`.
- No file with a forbidden name was opened.

v001 and v002 are unchanged. Both new files in this directory were written by exclusive create.

| File | Bytes | Lines | sha256 (from bytes) |
|---|---:|---:|---|
| owned_collective_worldline_static_response_v002.py (base, unchanged) | 135141 | 2946 | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 |
| owned_collective_worldline_static_response_v003.py (new) | 164654 | 3486 | e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721 |
| CONVENTIONS_0407_V003.md (new, R2) | 23727 | 333 | 09f26701cab08e3c00eea5d27c2d038411a16d17499563b0de6c745043f71fe8 |

## Binding inputs (sha256 recomputed from bytes before reading; all matched)

| Input | sha256 |
|---|---|
| 0410 `FROM_CODEX/0410_2026-10-16_direct_mode_columns_and_equal_time_pair_completion.md` (section 1 used) | ac1db8fa81c06672d495448b82835072978dee8bce0d3a017044de29cc440e34 |
| MODE SPEC `helpers/coefficient_method/OWNED_WORLDLINE_REAL_MODE_SCORE_AND_METRIC_PAIRING_SPEC_V001.txt` (read fully) | 2b294c7a59758aa994bf043c0c01e2e3cf0a3ec9327d5ec35757826851d46f9b |
| Evaluator base v002 (text) | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 |
| FIX_DELTA_0407_V002.md | 94c1518231d42b58418111f790611d3c5d635195e6fbc4d88c5c66e2757a7b41 |
| FINAL_CHECK_0407_V001.md | 1e352a9eac3d672bf93da60ba4c00270eb1279269208e5052628b060e1d19042 |
| REVIEW_0407_PALETTE_V001.md | 251a6077291e44bc1f3a658abc138cfeacf16084684b7720c8561e1646d20c29 |
| Operator v002 `owned_retained_response_0405/owned_parent_operator_v002.py` (present, so used; text) | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e |
| Root adapter `owned_diamond_registration_input_adapter_v001.py` (text) | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 |
| Registration JSON (semantics only) | f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 |
| Whitening companion JSON (semantics only) | 9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7 |
| 0409 (to word R3 exactly) | 53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c |

## Public signatures

**No public function or argument is added.** The only public callable is still `owned_collective_worldline_static_response(*, operator_api, graph0, model, registration, initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients, volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels, diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters, caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances, implicit_closure)`. It has 23 keyword-only parameters, none with a default, and is identical to v002.

The mode columns follow the MODE SPEC section 1 "minimal API delta". They enter as new element forms of `derivative_coordinates`. Every key is required, and none has a default:

```
{"id": ID, "kind": "lapse_direction",  "profile_id": PID, "cell_weights": {cell: phi_alpha}}
{"id": ID, "kind": "source_direction", "profile_id": PID, "cell_weights": {cell: phi_alpha},
 "label_weights": {("whitened_R", i) | ("whitened_S", i, j), i <= j : c_f}}
```

- The coordinate key is `(kind, id)`.
- The tuple coordinate interface is unchanged and can be mixed with these forms.
- A run without mode directions computes exactly what v002 computes. The only additions are three keys: `result["modes"] = None`, `result["inputs"]["mode_directions"] = []` and `conventions["mode_directions"]`.

## Change map (v003 line numbers; v002 lines in parentheses)

### Requirement 0410 §1 / MODE SPEC s1–s2: direct real-mode columns

| # | Requirement | Where (v003) |
|---|---|---|
| M1 | Project scores and log contacts onto fixed profiles BEFORE storage; never form the 640-coordinate cell Hessian | Lapse directions: `_diagonal_at` L1673–1719 (D_a = Σ_diag d_X v_X, v_X = Σ_α φ_α w_αX via `_projected_weight` L1465); `_event_from_channel` L1963–1978 (ρ = v_X/multiplier). Source directions: `_reads_at` L1893–1904. Stored per dwell only as `Da[n_u]` in `_segment_core` L1914–1937. `_measure` (L2459, unchanged) forms S and T from these n_u columns, so the contact is n_u×n_u (20×20 for one joint cos/sin block). |
| M2 | Signed affine lapse-cell and read-label weights; no nonnegative-partition admission on mode weights | `_admit_mode_direction` L872–955: finite reals, signed, not all zero; no sign or sum test. The operator `energy_weights` partition check `_lapse_multiplier` is unchanged. Base lapse > 0 via `lapse_factors` (unchanged). |
| M3 | Same incoming/outgoing endpoint-averaged allocations as H[N] | v_X uses the operator's own `energy_weights` (transition records: (w(y)+w(x))/2; diag records: w(x)), exactly the weights entering W and D (L1465, L1715, L1974). |
| M4 | Corrected current-graph read/source callback enters H, not only the estimator | The source direction D_a comes from the SAME `adapted_moment_reads` evaluation that gives P(x) in D (`_reads_at` L1893–1904, inside the callback block). Base sources stay the callback's j_R'/J_S'. A source direction is a fixed combination of `pair_source_R/S` coordinates, so no source is duplicated. |
| M5 | Full joint cos/sin block, no phase averaging, no isotropy | All declared directions sit in one joint coordinate set. `_analyze`/`_estimate` return the full joint Hessian and joint jackknife. Nothing is averaged or symmetrized (L22; `_mode_metadata` note L2696ff). |
| M6 | EXTENSIVE F_total gradient/Hessian, joint errors | `_mode_outputs` L2789–2854: `F_total_gradient` = −⟨S⟩/β, `F_total_hessian` = −(Cov+⟨T⟩)/β, extensive score/contact moments, `error_layout_positions` into the joint jackknife layout, and F standard errors (se/β) when mixing passed. Called at L3461–3472. |
| M7 | Actual profile/Gram metadata | `_mode_metadata` L2696–2786 at the binding stage (L3308–3331): S = Σφ², Σφ, c1 = Σφ/S (metadata), unit-pairing Gram G_mn, max normalized off-diagonal (flag at L3466ff), directions, base sources (lapse, source coefficients, whitened j_R'/J_S' actually used). |
| M8 | Separately tracked uniform first/pair moments | `_uniform_kinds`/`_mode_fields`/`_uniform_labels` L590–605. Cell sums Σ_α R'_α,i and Σ_α S'_α,ij (i ≤ j) per state in `_reads_at` L1905–1910 (same evaluation). They are appended as tracked columns (`run["tracked_all"]` L3174–3175, `_segment_core` L1936, `_analyze` names L2583, output L3437–3438) and reported in `modes.uniform_moments`. Reserved labels: input L3082–3090, operator-label collision L1735–1740. |
| M9 | No division by the mode norm inside the sampler | No score, covariance, contact or estimate is divided by S anywhere. S and c1 are metadata only. |
| M10 | Keep the original coordinate interface | The tuple branch of `_admit_coordinates` L958–1034 is unchanged (only the failure message names the new form, L1016–1017). Mapping entries are a new branch (L966–980). |
| M11 | Zero-rate directions for lapse modes | `_channels_from_records` L1548–1550 (L6). |
| M12 | Input/binding checks | `_admit_coordinates`: unique ids (L970–975) and one φ per profile_id (L1024–1032). Binding: profile keys == `context.energy_cells`, and source-direction callback cells == energy cells (L3308–3325). |
| M13 | Documentation | Module docstring: header L1–11, v003 sources L55–64, signature note L75–77, WHERE MODE SPEC L147–159, SEMANTICS L182–185, COST L215–220. LIMITATIONS: L5 (L274), L6 (L280–285), new L21 (L383), L22 (L409), L23 (L425). Public docstring L2993–3003 and L3039–3049. `conventions["mode_directions"]` L2917. |

### R1: palette call reconciled with ACTUAL operator v002

| Item | v003 (v002) |
|---|---|
| `_admit_operator_api` requires `palette_channels` | L554 (v002 L455 `owner_restricted_channels`) |
| `_palette_channels` calls `_op(run, "palette_channels", context=..., state=..., palette_owners=owners)` | L1641–1670 (v002 L1385–1414) |
| The stale "operator v002 not on disk" / ASSUMED text is removed | L44–47 (v002 L42–44), L82–84 and L102–107 (v002 L66–68, L86–91), COST L208, L1 L233–240 (v002 L197–203), L19 L358 and L364 (v002 L311 and L317), public docstring L2971 (v002 L2504) |

The argument is still a frozenset of original owner labels. Operator v002 `_admit_palette` admits list, tuple, set or frozenset. The palette-owned "diag" records it returns are skipped by `_palette_members` (unchanged). No other palette logic changed.

### R3: coarse-row refusal wording (no logic change)

| Item | v003 (v002) |
|---|---|
| LIMITATIONS L8: refused per 0409 "avoid allocating or duplicating unsupported raw moment sources"; operator v001 (one global frame) and operator v002 (per-part B = −A frames plus registration whitening, refused as duplicates) | L289–299 (v002 L249–252) |
| `_unsupported_raw_kinds` docstring | L575–583 (v002 L476–478) |
| `_admit_label_roles` message | L790–794 (v002 L669–671) |
| Public docstring | L3008–3011 (v002 L2532) |

### R2: conventions

`CONVENTIONS_0407_V003.md` is a new file, written by exclusive create. It covers:
- the signature, including `diagonal_read_source_callback`, `palette_parameters` and the mode-column inputs;
- the actual operator record fields and adapter names;
- every output, including `member_check` and `modes`;
- H_c with the pair-source term, and the pair and mode coordinates;
- the model-level member check and the palette move;
- cost, storage and measurement;
- LIMITATIONS numbering L1–L23.

### Other textual changes (no logic)

- The `implicit_closure` message now says "v003" (L3057).
- `_diagonal_at` returns a third element. Its only caller, `_segment_core` (L1917), unpacks it.

## Operator and adapter API this version calls (exact names)

**Operator** (v001 `27ad1762…` and v002 `b5fded4d…`, read as text only, never imported):
- `validate_owned_model(*, graph0, model, registration)`
- `canonical_state_key(*, context, state)`
- `primitive_channels(*, context, state)`, with records `owner_id, kind, target_state, amplitude, queried_support, changed_support, energy_weights`
- `diagonal_terms(*, context, state)`, with value = `amplitude` and `energy_weights`
- `read_rows(*, context, state)` returning `{labels, values, presence}`
- `palette_channels(*, context, state, palette_owners)`, operator v002 only, needed only with `palette_parameters`
- `context.energy_cells`

**Root adapter** (`0705be7c…`, text only):
- `adapted_moment_reads(*, operator_module, context, state, binding)`, which needs `operator_module.state_labels` and `binding["L"]`, `["graph0"]` and `["registration"]`
- `pair_source_hamiltonian(*, reads, j_R, j_S)`
- `raw_to_whitened_sources(*, j_R_raw, j_S_raw)`

Nothing is assumed beyond these on-disk signatures. The mode addition needs no new operator or adapter function.

## LIMITATIONS of this delta (ambiguities recorded literally; no physics invented)

1. **API placement.** The mode columns go inside `derivative_coordinates`, following the MODE SPEC "minimal API delta". No new public argument was added, so v002 callers are unaffected.
2. **"label_weights: {label: coefficient}".** This is implemented in factorized form:
   - the profile is φ_α (`cell_weights`), and the coefficients c_f are cell-free over the nine whitened fields;
   - weight(α, f) = φ_α·c_f.
   - This keeps S, c1 and the Gram well defined per profile.
   - A non-factorized per-cell source weighting can still be expressed with several directions, or with the tuple `pair_source_R/S` coordinates.
   - Operator read rows are not available as mode source fields, which are restricted to the nine whitened callback fields.
3. **Mandel factor.** The module adds no multiplicity. c_f on an off-diagonal S field is the caller's chart coefficient (√2 for the Mandel components named in MODE SPEC s1). The relation to `pair_source_S` is c_f = mult × coefficient.
4. **"Orthonormal" profiles.** The module reports the actual Gram under the unit cell pairing and never thresholds it, since no tolerance is chosen. It does not require S = 1. Unequal cell weights (a weighted pairing) are not implemented.
5. **"General columns may combine these by a fixed matrix P."** P is not a separate input. All coordinates are affine, so P^T g, P^T H P and the same linear map of the returned jackknife replicates are exact post hoc.
6. **MODE SPEC s2 "report both … normalized F derivatives" versus 0410 "no division by the mode norm inside the sampler".** 0410 is followed. Only extensive F_total derivatives are returned, with S and c1 as metadata. F_mode = F_total/S and the Gram duals are the root adapter's.
7. **Uniform moments.** They are reported as cell SUMS, extensive and unnormalized, with n_cells. They exist only when the callback is present. No Mandel factor and no central covariance are applied.
8. **Profiles must list every cell of `context.energy_cells`** (explicit zeros). Source directions need callback cells equal to those cells. Both conditions hold for the actual adapter and operator v002 pairing (`energy_cells` = `registration["cells"]`).
9. **Invariant-block admissibility** (MODE SPEC s3, s5) is not tested. The caller must declare every coupled column. Uniform-block tadpoles and constraints need uniform-profile directions or separate runs.
10. **No guard against large tuple blocks.** A caller can still request a per-cell 640-coordinate block through the original tuple interface, because that interface is kept unchanged.
11. **Operator v002 is unreviewed** (FINAL_CHECK R7). Every compatibility statement rests on static text reading. FINAL_CHECK R4 integration notes (registration `whitening`, `{'A': T, 'B': -T}`, the same registration object, `binding["L"]`) remain the root runner's.
12. **Scope.** 0410 section 2 (the equal-time two-hop pair sector) is NOT part of this delta.

## AST results (text copy of the destination file, `python3 -I -B`)

- `ast.parse` and `compile(..., "exec")`: OK.
- Imports are only `bisect`, `math`, `collections.abc.Mapping` and `numpy`.
- No `MatMult` (`@` or `@=`). No `dot`, `matmul`, `vdot`, `inner`, `tensordot` or `linalg` name or attribute.
- There are 10 `einsum` calls, all with `optimize=False`.
- There is no `print`, `open`, `eval`, `exec`, `compile`, `__import__`, `input`, `globals`, `locals`, `vars`, `breakpoint`, `exit` or `quit` call. No `os`, `sys`, `subprocess`, `threading`, `socket`, `pickle`, `ctypes`, `io`, `pathlib`, `shutil`, `multiprocessing` or `asyncio` name appears.
- Module level holds the docstring, 4 imports, `LIMITATIONS` (a string constant), `class _Stop` and 92 `def`s (84 in v002). There are no decorators and no global/nonlocal statements, so nothing runs at import.
- A `symtable` scan found no undefined globals.
- There is one public callable, `owned_collective_worldline_static_response`, with 0 positional and 23 keyword-only parameters and no defaults.

## diff -u v002 v003

```diff
--- owned_collective_worldline_static_response_v002.py	2026-10-16 04:21:29.846046360 -0500
+++ owned_collective_worldline_static_response_v003.py	2026-10-16 04:51:07.320826526 -0500
@@ -1,6 +1,9 @@
 """Owned collective static response by positive imaginary-time worldlines.
 
-UNT task 0407, version v002: the fix of v001 (sha256
+UNT task 0407, version v003: v002 (sha256
+0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941, preserved unchanged) plus the
+0410 section 1 direct real-mode derivative columns, the FINAL_CHECK R1 operator v002 palette
+call and the R3 coarse-row wording. v002 was the fix of v001 (sha256
 0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f, preserved unchanged) for the
 review/0408/0409 blocking items: model-level member check, additive blocked-palette move,
 actual operator API, root adapter read/source callback. Static author implementation: written
@@ -41,7 +44,7 @@
     42e4041006a07e3d9f5a44afbd079077be1e60ef91919d34251915f0e2f8de35
   * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v001.py
     27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6   (ACTUAL operator API,
-    read as text; no operator v002 existed on disk when this file was written)
+    read as text)
   * helpers/coefficient_method/owned_diamond_registration_input_adapter_v001.py
     0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77   (root adapter, read as
     TEXT only; its public callables are reached at run time through a caller-supplied object)
@@ -49,6 +52,16 @@
     f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 and its companion
     OWNED_DIAMOND_WHITENING_DUAL_SOURCE_MANDATORY_COMPANION_V001.json
     9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7   (semantics only)
+v003 additions (sha256 from bytes before writing; read-only; values never taken from them):
+  * UNT_EXCHANGE/FROM_CODEX/0410_2026-10-16_direct_mode_columns_and_equal_time_pair_completion.md
+    ac1db8fa81c06672d495448b82835072978dee8bce0d3a017044de29cc440e34   (section 1 only)
+  * helpers/coefficient_method/OWNED_WORLDLINE_REAL_MODE_SCORE_AND_METRIC_PAIRING_SPEC_V001.txt
+    2b294c7a59758aa994bf043c0c01e2e3cf0a3ec9327d5ec35757826851d46f9b   ("MODE SPEC")
+  * claude_artifacts/owned_collective_worldline_0407/FINAL_CHECK_0407_V001.md
+    1e352a9eac3d672bf93da60ba4c00270eb1279269208e5052628b060e1d19042   (items R1, R2, R3)
+  * claude_artifacts/owned_retained_response_0405/owned_parent_operator_v002.py
+    b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e   (ACTUAL operator v002
+    API, read as text; its palette_channels is the palette enumeration called here)
 Style reference (read as text): claude_artifacts/scalar_metric_solve_0397/
 scalar_metric_particular_solve_v002.py (fail-closed result dict).
 
@@ -59,13 +72,16 @@
       diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
       caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
       implicit_closure)
+The v002 signature is unchanged (no public argument is added in v003): the 0410 mode
+columns enter as fixed affine direction mappings inside derivative_coordinates (MODE SPEC
+s1 "minimal API delta"; L21), next to the unchanged tuple coordinate interface.
 It returns a plain fail-closed dict with "ok", "status" (complete | incomplete |
 unsupported | failed), "stage_reached" and "failures". When ok is False every populated
 field is evidence only, never a result.
 
-OPERATOR API: the ACTUAL owned_parent_operator_v001.py API (state level, basis free; the
-operator module is NOT imported here). The caller passes `operator_api`, a mapping or object
-exposing these module-level, keyword-only callables:
+OPERATOR API: the ACTUAL owned_parent_operator_v001.py / owned_parent_operator_v002.py API
+(state level, basis free; the operator module is NOT imported here). The caller passes
+`operator_api`, a mapping or object exposing these module-level, keyword-only callables:
   validate_owned_model(*, graph0, model, registration)
       -> {"ok", "stage_reached", "failures", "context"}; context.energy_cells is the ordered
          tuple of coarse cells (a "status" "unsupported", if ever returned, is passed through).
@@ -83,12 +99,12 @@
       the record amplitude and energy_weights[alpha] = w_alphaX(state).
   read_rows(*, context, state) -> {"labels": state-independent tuple of typed labels,
       "values": float64 [n], "presence": float64 [n]}; absent rows have value 0.
-  owner_restricted_channels(*, context, state, owners) -> ASSUMED (0405 module A v002 was
-      not on disk; name and signature to be reconciled by the final checker): the
-      primitive_channels records (same fields) of every primitive whose permanent palette
-      groups (classification below) meet `owners`, a frozenset of original owner labels,
-      with all Birth reverse alternatives and full current eligibility. Required only when
-      palette_parameters is not None.
+  palette_channels(*, context, state, palette_owners) -> the ACTUAL operator v002 palette
+      enumeration (op v002 L1837; absent in operator v001): the primitive_channels records
+      (same fields) of every primitive whose permanent palette groups (classification below)
+      meet `palette_owners`, passed here as a frozenset of original owner labels, with all
+      Birth reverse alternatives and full current eligibility; its palette-owned "diag"
+      records are skipped. Required only when palette_parameters is not None.
 ROOT ADAPTER (owned_diamond_registration_input_adapter_v001.py; diagonal_read_source_callback
 supplies the adapter object at run time; these ACTUAL signatures are called unchanged):
   adapted_moment_reads(*, operator_module, context, state, binding) -> {"cells", "R", "S",
@@ -127,7 +143,20 @@
     (batch means, jackknife joint covariance, integrated autocorrelation, R-hat across
     independent chains, mixing status); storage/work described under COST.
   Section 5 is NOT implemented: implicit_closure must be None (contract retained).
-  Section 6 is scope: see "scope" in the result and CONVENTIONS_0407_V001.md.
+  Section 6 is scope: see "scope" in the result and CONVENTIONS_0407_V003.md.
+WHERE THE MODE SPEC (0410 section 1) IS IMPLEMENTED (v003, L21-L23)
+  MODE SPEC s1 (fixed real columns before storage): _admit_mode_direction (signed weights,
+    no partition admission), _diagonal_at (lapse direction D_a = sum_diag d_X v_X with
+    v_X = sum_alpha phi_alpha w_alphaX), _event_from_channel (rho = v_X / multiplier from
+    the endpoint-averaged transition weights), _reads_at (source direction D_a = -sum_alpha
+    phi_alpha sum_f c_f O_alpha,f from the SAME callback evaluation that enters H_c);
+    _measure stores only the projected n_u columns; no full cell Hessian is formed.
+  MODE SPEC s2/0410 (extensive outputs): _mode_metadata (binding stage) and _mode_outputs
+    fill result "modes" (F_total gradient/Hessian, extensive score/contact moments, profile
+    S, sum, c1 and Gram, base sources, error positions, uniform first/pair moments from the
+    _reads_at cell sums); no division by any mode norm.
+  MODE SPEC s3-s5 (Legendre, J, contact, metric/EH pairing, block admissibility) are the
+    root metric adapter's and are NOT implemented here.
 
 SEMANTICS. In the positive gauge G = (-1)^{sum_v q_v} (-e^{i phi_adm})^{N_S}
 (-e^{i phi_birth})^{N} (assembly lines 300-327, e^{-i theta} epsilon = -|epsilon| written
@@ -150,8 +179,10 @@
 exp(-int D) prod_events W. Source coordinates u are ("lapse", cell) [d/dn = d/dN],
 ("source", label) [j_label], ("volume_multiplier",) [lambda], ("pair_source_R", cell, i)
 [j_R'[cell][i]] and ("pair_source_S", cell, i, j), i <= j [the symmetric pair J_S'[i][j] =
-J_S'[j][i], declared multiplicity 1 if i == j else 2]; all are affine, so
-D_ab = W_ab = 0 exactly and
+J_S'[j][i], declared multiplicity 1 if i == j else 2] and (v003) the fixed affine mode
+directions {"kind": "lapse_direction"} [N_alpha = N_alpha(base) + eta phi_alpha] and
+{"kind": "source_direction"} [H_c gains -eta sum_alpha phi_alpha sum_f c_f O_alpha,f]
+(L21); all are affine, so D_ab = W_ab = 0 exactly and
     S_a  = -int D_a + sum_events W_a/W,       T_ab = -sum_events W_a W_b / W^2,
     d_a log Z = <S_a>,   d_ab log Z = Cov(S_a, S_b) + <T_ab>,
     F_a = -<S_a>/beta,   F_ab = -(Cov + <T>)/beta.
@@ -174,14 +205,19 @@
 primitive_channels, one diagonal_terms, one read_rows, one canonical_state_key and (with
 the callback) one adapted_moment_reads call at the new state, all O(current vertices) or
 O(registered labels) in the worst case, plus the reverse-pairing check. A palette event
-replaces the full channel enumeration by owner_restricted_channels (restricted exit rate
+replaces the full channel enumeration by palette_channels (restricted exit rate
 r_S) but KEEPS the global diagonal_terms / read_rows / callback reads per new state, and
 one restricted enumeration per old dwell segment inside the interval: the remaining
 global per-event cost is reported, not hidden (L3, L19). Exit rates of segments created by
 palette moves are enumerated lazily when a global move needs them. A measurement uses the
 stored per-segment read rows and costs O(events * (n_u + n_r)) arithmetic. Error analysis
 stores O(chains * measurements * (n_u^2 + n_r)) numbers and O(J * n_y) jackknife
-replicates. No Hilbert-space list, basis index or dense operator is built.
+replicates. No Hilbert-space list, basis index or dense operator is built. Mode directions
+(v003) add, per new state, O(diagonal records * nonzero weights * lapse directions) for the
+lapse projections and O(cells * fields) per source direction plus O(9 * cells) for the
+uniform moments; per event O(nonzero weights * lapse directions). n_u counts directions
+(e.g. 20 for one joint cosine/sine block), never cells times fields, so per-sample storage
+is O(n_u^2 + n_r) whatever the cell count.
 
 LIMITATIONS: see the module-level string LIMITATIONS.
 """
@@ -194,13 +230,14 @@
 
 
 LIMITATIONS = """
-L1. Operator API is the ACTUAL owned_parent_operator_v001.py API (sha256 27ad1762...):
-    energy_weights tuples aligned with context.energy_cells, the diagonal value is the
-    "diag" record amplitude, primitive_channels also returns the "diag" records (skipped
-    here), read_rows returns {labels, values, presence} arrays with state-independent
-    labels. The owner-restricted enumeration of the palette move is ASSUMED as
-    owner_restricted_channels(*, context, state, owners) because 0405 module A v002 was
-    not on disk; the final checker reconciles its name/signature. Mismatches fail closed.
+L1. Operator API is the ACTUAL owned_parent_operator_v001.py API (sha256 27ad1762...),
+    unchanged in owned_parent_operator_v002.py (sha256 b5fded4d...): energy_weights tuples
+    aligned with context.energy_cells, the diagonal value is the "diag" record amplitude,
+    primitive_channels also returns the "diag" records (skipped here), read_rows returns
+    {labels, values, presence} arrays with state-independent labels. The palette move calls
+    the ACTUAL operator v002 enumeration palette_channels(*, context, state, palette_owners)
+    (FINAL_CHECK R1; operator v001 has none, so with v001 a non-None palette_parameters
+    fails closed at input admission). Mismatches fail closed.
 L2. Positive gauge, verified on TWO lines. (a) Model level, before any state is visited:
     _model_member_check reads the caller's model mapping against the contract s3/s10
     coefficient schema (exactly the 13 diagonal scalars Delta, Ud, dstar, epsilon_c,
@@ -235,21 +272,31 @@
     measure gives derivatives only. A normalization (e.g. thermodynamic integration in
     beta) is not implemented. No global energy scalar is subtracted from D.
 L5. Coordinates are affine: lapse n_alpha (identical derivative to N_alpha), read source
-    j_label, lambda, whitened pair sources (L20). W_ab = D_ab = 0 exactly. Nonlinear
-    coordinates (e.g. g00 with N = sqrt(1 + 2 n_g)) follow by the caller's chain rule d_vv log Z = J^T H J +
+    j_label, lambda, whitened pair sources (L20), fixed mode directions (L21). W_ab = D_ab =
+    0 exactly. Nonlinear coordinates (e.g. g00 with N = sqrt(1 + 2 n_g)) follow by the
+    caller's chain rule d_vv log Z = J^T H J +
     sum_a d_a log Z d_vv u_a using the returned first AND second derivatives. Read-frame,
     registration, preparation and map derivative contacts are NOT included (reads fixed).
 L6. Zero-rate source-opening directions (an available primitive with W = 0 but W_a != 0)
     are detected only at visited states; such a direction is dropped from all outputs and
     listed as unsupported. With N_alpha > 0 and nonnegative partition weights it cannot
-    occur; it is reachable only with weights that make 1 + sum n wbar = 0.
+    occur; it is reachable only with weights that make 1 + sum n wbar = 0. A lapse mode
+    direction (L21) is such a direction when sum_alpha phi_alpha wbar_alphaX != 0 at a
+    primitive with multiplier 0; source directions have W_a = 0 and never are.
 L7. Conserved-resource component. All chains must start in ONE declared component; the
     module cannot verify membership without enumeration. Explicitly weighted unions of
     superselection components are not combined here (caller weights separate runs).
 L8. Coarse moments (0408/0409). Operator rows of kind coarse_first_R / coarse_second_S
-    (operator v001: one global port frame, which cannot represent the registered B = -A
-    frames) are unsupported in EVERY role (source coefficient, volume term, derivative
-    coordinate, tracked read): status "unsupported". Whitened, configuration-normalized
+    are unsupported in EVERY role (source coefficient, volume term, derivative coordinate,
+    tracked read): status "unsupported". The reason is the 0409 rule "avoid
+    allocating or duplicating unsupported raw moment sources": the corrected moments have
+    ONE source of truth here, the root adapter callback, so no second moment row is
+    allocated beside it. For operator v001 (sha256 27ad1762...) those rows are moreover
+    built with one global port frame, which cannot represent the registered B = -A frames.
+    Operator v002 (sha256 b5fded4d...) builds them with the registered per-part frames
+    (B = -A under the 0408 registration) and registration['whitening'] folded in; they
+    would still duplicate the callback's moments and pair-source allocation and stay
+    refused. Whitened, configuration-normalized
     (current present count) coarse R', S' come only from the root adapter callback
     (adapted_moment_reads), as labels ("whitened_R", cell, i) and ("whitened_S", cell, i,
     j) with i <= j (S' is symmetric; the lower triangle is not duplicated). The adapter's
@@ -308,13 +355,13 @@
     docstring classification) miss S; times and descriptors are kept. The held descriptor
     is (kind, owner_id); it must identify at most one positive-rate record at any state
     (more than one -> failed). Between held marks only member channels run, with their
-    actual rates and total r_S; a held mark is replayed through owner_restricted_channels
+    actual rates and total r_S; a held mark is replayed through palette_channels
     on its own groups and the proposal is rejected when the record is absent (guard,
     newborn/donor image or eligibility failure) or has zero rate; the replayed event gets
     the same reverse-pairing and self-loop checks as a sampled one. Endpoint mismatch
     rejects. Acceptance is min(1, exp{int_I new(r_S - D) - int_I old(r_S - D) + sum_held
     log(W(new pre-event)/W(old pre-event))}); endpoint rejection is never renormalized as a
-    conditioned bridge. Records returned by owner_restricted_channels that are not members
+    conditioned bridge. Records returned by palette_channels that are not members
     by this classification are dropped (counted in diagnostics); COMPLETENESS (no omitted
     member primitive) is the operator's contract, cross-checked against
     primitive_channels at every restricted enumeration only when
@@ -333,6 +380,58 @@
     second whitening). The adapter value and the module's linear reconstruction must agree
     within source_consistency_tolerance at every state, else failed. The callback binding
     must hold the SAME graph0 and registration objects as the operator call.
+L21. Mode directions (0410 section 1; MODE SPEC s1-s2). derivative_coordinates may also
+    hold mappings {"id", "kind": "lapse_direction", "profile_id", "cell_weights"} or {"id",
+    "kind": "source_direction", "profile_id", "cell_weights", "label_weights"}; their
+    coordinate key is (kind, id) and ids are unique. cell_weights phi: finite reals over
+    EVERY cell of context.energy_cells (explicit zeros), signed, not all zero. They are
+    derivative directions around the caller's positive base lapse and sources, NOT an energy
+    partition: no sign, sum or partition admission is applied to them (the operator's own
+    energy_weights keep the V002 partition check, L11). Lapse direction: N_alpha =
+    N_alpha(base) + eta phi_alpha; per primitive v_X = sum_alpha phi_alpha w_alphaX with the
+    operator's energy_weights, i.e. exactly the allocations of H[N] (endpoint-averaged
+    (w(y) + w(x))/2 on transitions, w(x) on diagonal owners); D_a = sum_diag d_X v_X and
+    rho_a = v_X / multiplier. Source direction: label_weights {field: c_f} over the nine
+    whitened callback fields ("whitened_R", i) and ("whitened_S", i, j), i <= j in 0..2,
+    not all zero; D_a = -sum_alpha phi_alpha sum_f c_f O_alpha,f with O_alpha,f the
+    UNNORMALIZED whitened element R'_i or S'_ij of the SAME adapter evaluation that enters
+    H_c, and W_a = 0. No multiplicity is added: c_f on an off-diagonal S field is the
+    caller's chart factor (e.g. sqrt(2) for a Mandel component); c_f equals mult times the
+    coefficient of ("pair_source_S", cell, i, j) (L20). A source direction is a fixed
+    combination of the L20 pair coordinates, so it allocates and duplicates no source: base
+    sources remain the callback j_R'/J_S'. Source directions need the callback, whose cells
+    must equal context.energy_cells. Projection is applied per primitive and per state
+    BEFORE any sample is stored; no per-cell column, full cell Hessian or cells-times-fields
+    block is ever formed. Directions sharing a profile_id must carry identical cell_weights.
+    A general fixed matrix P combining declared directions into further columns is NOT a
+    separate input: all coordinates are affine, so P^T g, P^T H P and the same linear map of
+    the returned jackknife replicates are exact post hoc (caller).
+L22. Mode metadata and pairing. The pairing is the unit discrete cell pairing over
+    context.energy_cells (weight 1 per cell); an unequal-weight cell pairing is NOT
+    implemented (it would need the weighted dual pairing throughout). Per profile the
+    result gives S = sum phi^2, sum phi and c1 = sum phi / S (metadata only), and the Gram
+    G_mn = sum_alpha phi_m phi_n over all declared profiles with its largest normalized
+    offdiagonal |G_mn| / sqrt(G_mm G_nn). Orthonormality is the caller's declaration (0410):
+    it is reported, never thresholded (no tolerance is chosen here). Outputs are EXTENSIVE
+    (derivatives of F_total = -log Z / beta in eta); no score, covariance, contact or
+    estimate is divided by S or by any mode norm. Normalized F_mode, Gram duals, the
+    Legendre transform, the J Jacobian, background contacts and the metric/EH pairing (MODE
+    SPEC s2-s5) belong to the root metric adapter and are not computed here. The joint block
+    is returned whole: no phase averaging, isotropy, cosine/sine decoupling or
+    symmetrization between profiles is applied. Whether the declared directions form an
+    invariant block of the complete static source Hessian (MODE SPEC s3, s5) is NOT tested
+    here; the caller must declare every coupled column. Uniform-block lapse/metric tadpoles
+    and constraints need separate uniform-profile directions or runs.
+L23. Uniform first/pair moments. When mode directions are present and the callback is
+    given, nine extra tracked columns ("uniform_whitened_R", i) and ("uniform_whitened_S",
+    i, j), i <= j, hold the per-state cell SUMS sum_alpha R'_alpha,i and sum_alpha
+    S'_alpha,ij over the callback cells, from the same evaluation that enters H_c. They are
+    tracked separately from the mode columns; their means, responses and errors follow the
+    tracked-read rules. No division by the cell count, no Mandel factor and no central
+    covariance C = M - mu mu^T is applied (root: mu = sum / n_cells, M likewise). Without
+    the callback they are absent (result modes "uniform_moments" is None). These two label
+    kinds are reserved: a caller tracked label or an operator read label of either kind
+    fails.
 """
 
 
@@ -452,7 +551,7 @@
         "read_rows",
     ]
     if need_restricted:
-        names.append("owner_restricted_channels")
+        names.append("palette_channels")  # actual operator v002 name (FINAL_CHECK R1)
     api = {}
     for nm in names:
         present, fn = _field(operator_api, nm)
@@ -474,7 +573,12 @@
 
 
 def _unsupported_raw_kinds():
-    """Operator v001 coarse moment rows built with ONE global port frame (0408/0409)."""
+    """Operator coarse moment rows refused in every role (0409: no duplicated moment source).
+
+    Operator v001 builds them with one global port frame (cannot represent B = -A); operator
+    v002 builds them with per-part B = -A frames plus the registration whitening, but they
+    would duplicate the root adapter callback's moments and pair-source allocation (L8).
+    """
     return ("coarse_first_R", "coarse_second_S")
 
 
@@ -483,6 +587,23 @@
     return ("whitened_R", "whitened_S")
 
 
+def _uniform_kinds():
+    """Reserved kinds of the v003 uniform (cell-summed) whitened moment columns (L23)."""
+    return ("uniform_whitened_R", "uniform_whitened_S")
+
+
+def _mode_fields():
+    """The nine whitened callback fields a source direction may weight (L21), fixed order."""
+    fields = [("whitened_R", i) for i in range(3)]
+    fields += [("whitened_S", i, j) for i in range(3) for j in range(i, 3)]
+    return tuple(fields)
+
+
+def _uniform_labels():
+    """Uniform first/pair moment column labels (L23), in _mode_fields order."""
+    return tuple(("uniform_" + f[0],) + f[1:] for f in _mode_fields())
+
+
 def _label_kind(label):
     if isinstance(label, tuple) and label and isinstance(label[0], str):
         return label[0]
@@ -666,9 +787,11 @@
         kind = _label_kind(lbl)
         if kind in _unsupported_raw_kinds():
             unsupported.append(
-                f"input {role}: {lbl!r} is an operator v001 coarse moment row built with one "
-                "global port frame, which cannot represent the registered B = -A frames; "
-                "corrected moments enter only through diagonal_read_source_callback (L8)"
+                f"input {role}: {lbl!r} is an operator coarse moment row; per 0409 no unsupported "
+                "raw moment source is allocated or duplicated: corrected moments enter only "
+                "through diagonal_read_source_callback (operator v001 rows use one global port "
+                "frame; operator v002 rows use per-part B = -A frames plus whitening and would "
+                "duplicate the callback moments) (L8)"
             )
         elif kind in _whitened_kinds():
             if role in ("source_coefficients", "derivative_coordinates"):
@@ -734,12 +857,127 @@
     return {"admission_phase": phi_a, "birth_phase": phi_b}
 
 
-def _admit_coordinates(value, lapse, pair_cells, failures):
+def _mode_field(field):
+    """Normalized whitened callback field ("whitened_R", i) / ("whitened_S", i, j), i <= j."""
+    if not isinstance(field, tuple) or not field or field[0] not in _whitened_kinds():
+        return None
+    n_idx = 1 if field[0] == "whitened_R" else 2
+    if len(field) != 1 + n_idx or not all(_component(x) for x in field[1:]):
+        return None
+    if n_idx == 2 and int(field[1]) > int(field[2]):
+        return None
+    return (field[0],) + tuple(int(x) for x in field[1:])
+
+
+def _admit_mode_direction(i, spec, pair_cells, failures):
+    """(key, direction) of one v003 fixed affine mode direction (L21), or None.
+
+    Signed cell weights are derivative directions around the positive base lapse and
+    sources, NOT an energy partition: only finiteness and a nonzero profile are required.
+    """
+    name = f"derivative_coordinates[{i}]"
+    where = f"input {name}"
+    kind = spec["kind"] if "kind" in spec else None
+    if isinstance(kind, str) and kind == "lapse_direction":
+        keys = ("id", "kind", "profile_id", "cell_weights")
+    elif isinstance(kind, str) and kind == "source_direction":
+        keys = ("id", "kind", "profile_id", "cell_weights", "label_weights")
+    else:
+        failures.append(
+            f"{where}: a mode direction mapping needs kind 'lapse_direction' or "
+            "'source_direction' (L21)"
+        )
+        return None
+    if not _admit_required_keys(name, spec, keys, failures):
+        return None
+    good = True
+    if not _hashable(spec["id"]) or not _hashable(spec["profile_id"]):
+        failures.append(f"{where}: 'id' and 'profile_id' must be hashable")
+        good = False
+    raw = spec["cell_weights"]
+    phi = {}
+    if not isinstance(raw, Mapping) or not raw:
+        failures.append(f"{where}: 'cell_weights' must be a nonempty mapping cell -> finite real")
+        good = False
+    else:
+        for cell, val in raw.items():
+            v = _real_value(val)
+            if v is None:
+                failures.append(
+                    f"{where}: cell_weights[{cell!r}] = {val!r} is not a finite real (signed "
+                    "derivative weights are admitted; no partition admission)"
+                )
+                good = False
+                continue
+            phi[cell] = v
+        if good and all(v == 0.0 for v in phi.values()):
+            failures.append(f"{where}: cell_weights are identically zero (S = 0)")
+            good = False
+    fields = None
+    if kind == "source_direction":
+        if pair_cells is None:
+            failures.append(
+                f"{where}: a source_direction weights the whitened callback moments; "
+                "diagonal_read_source_callback is required (L21)"
+            )
+            good = False
+        lw = spec["label_weights"]
+        if not isinstance(lw, Mapping) or not lw:
+            failures.append(f"{where}: 'label_weights' must be a nonempty mapping field -> real")
+            good = False
+        else:
+            order = _mode_fields()
+            fields = []
+            for field, coef in lw.items():
+                norm = _mode_field(field)
+                c = _real_value(coef)
+                if norm is None or c is None:
+                    failures.append(
+                        f"{where}: label_weights[{field!r}] needs a field ('whitened_R', i) or "
+                        "('whitened_S', i, j), i <= j in 0..2, with a finite real coefficient"
+                    )
+                    good = False
+                    continue
+                fields.append((norm, c))
+            fields.sort(key=lambda fc: order.index(fc[0]))
+            if good and all(c == 0.0 for _, c in fields):
+                failures.append(f"{where}: label_weights are identically zero")
+                good = False
+    if not good:
+        return None
+    direction = {
+        "id": spec["id"],
+        "kind": kind,
+        "profile_id": spec["profile_id"],
+        "phi": phi,
+        "fields": None if fields is None else tuple(fields),
+    }
+    return (kind, spec["id"]), direction
+
+
+def _admit_coordinates(value, lapse, pair_cells, failures, modes):
+    """Coordinate keys in caller order; v003 mode directions are also recorded in `modes`."""
     if not isinstance(value, (list, tuple)):
         failures.append("input derivative_coordinates: must be a list or tuple of tuples")
         return None
     out = []
+    ids = set()
     for i, coord in enumerate(value):
+        if isinstance(coord, Mapping):
+            got = _admit_mode_direction(i, coord, pair_cells, failures)
+            if got is None:
+                continue
+            key, direction = got
+            if direction["id"] in ids:
+                failures.append(
+                    f"input derivative_coordinates[{i}]: duplicate mode direction id "
+                    f"{direction['id']!r}"
+                )
+                continue
+            ids.add(direction["id"])
+            modes[key] = direction
+            out.append(key)
+            continue
         if not isinstance(coord, tuple) or not coord or not _hashable(coord):
             failures.append(
                 f"input derivative_coordinates[{i}]: {coord!r} is not a nonempty hashable tuple"
@@ -775,14 +1013,24 @@
         else:
             failures.append(
                 f"input derivative_coordinates[{i}]: {coord!r} is not ('lapse', cell), "
-                "('source', label), ('volume_multiplier',), ('pair_source_R', cell, i) or "
-                "('pair_source_S', cell, i, j)"
+                "('source', label), ('volume_multiplier',), ('pair_source_R', cell, i), "
+                "('pair_source_S', cell, i, j) or a mode direction mapping (L21)"
             )
             continue
         if coord in out:
             failures.append(f"input derivative_coordinates[{i}]: duplicate {coord!r}")
             continue
         out.append(coord)
+    profiles = {}
+    for key, direction in modes.items():
+        pid = direction["profile_id"]
+        if pid not in profiles:
+            profiles[pid] = direction["phi"]
+        elif profiles[pid] != direction["phi"]:
+            failures.append(
+                f"input derivative_coordinates: mode direction {key!r} reuses profile_id "
+                f"{pid!r} with different cell_weights (one fixed profile per id; L21)"
+            )
     return out
 
 
@@ -1214,6 +1462,11 @@
     return mult
 
 
+def _projected_weight(phi, weights):
+    """v_X = sum_alpha phi_alpha w_alphaX of one primitive (L21), from its nonzero weights."""
+    return math.fsum([phi[cell] * w for cell, w in weights.items()])
+
+
 def _signature(changed):
     try:
         sig = frozenset(changed)
@@ -1292,6 +1545,9 @@
             for cell, w in weights.items():
                 if w != 0.0 and cell in run["lapse_index"]:
                     run["zero_rate_directions"].add(("lapse", cell))
+            for idx, phi in run["lapse_dirs"]:
+                if _projected_weight(phi, weights) != 0.0:
+                    run["zero_rate_directions"].add(run["coords"][idx])  # L6, L21
             continue
         rate = mag * mult
         if not (math.isfinite(rate) and rate > 0.0):
@@ -1383,12 +1639,12 @@
 
 
 def _palette_channels(run, state, owners):
-    """Member channels and restricted exit rate r_S at `state` (owner_restricted_channels)."""
+    """Member channels and restricted exit rate r_S at `state` (operator v002 palette_channels)."""
     _enumeration_tick(run)
     run["counters"]["restricted_enumerations"] += 1
-    records = _op(run, "owner_restricted_channels", context=run["context"], state=state,
-                  owners=owners)
-    members, dropped = _palette_members(run, records, owners, "owner_restricted_channels")
+    records = _op(run, "palette_channels", context=run["context"], state=state,
+                  palette_owners=owners)
+    members, dropped = _palette_members(run, records, owners, "palette_channels")
     run["counters"]["restricted_nonmember_records_dropped"] += dropped
     if run["palette"]["verify"]:
         _enumeration_tick(run)
@@ -1401,27 +1657,32 @@
             want[ident] = want.get(ident, 0) + 1
         got = {}
         for i, rec in enumerate(members):
-            ident = _record_identity(run, rec, f"owner_restricted_channels record {i}")
+            ident = _record_identity(run, rec, f"palette_channels record {i}")
             got[ident] = got.get(ident, 0) + 1
         if want != got:
             raise _Stop(
                 "failed",
                 run["stage"],
-                "owner_restricted_channels differs from the palette members of "
+                "palette_channels differs from the palette members of "
                 "primitive_channels at a visited state (omitted, extra or altered member "
                 "records; verify_against_full_enumeration)",
             )
-    return _channels_from_records(run, members, "owner_restricted_channels")
+    return _channels_from_records(run, members, "palette_channels")
 
 
 def _diagonal_at(run, state):
-    """Diagonal H[N] energy and its lapse derivatives (real diagonals verified)."""
+    """Diagonal H[N] energy, its lapse derivatives and (v003) lapse-direction projections.
+
+    Lapse directions (L21): sum_diag d_X v_X with v_X = sum_alpha phi_alpha w_alphaX, formed
+    per record from its own weights (no per-cell column is stored).
+    """
     records = _op(run, "diagonal_terms", context=run["context"], state=state)
     if not isinstance(records, (list, tuple)):
         raise _Stop("failed", run["stage"], "diagonal_terms did not return a list")
     tol_g = run["tol"]["gauge_phase"]
     h_terms = []
     lapse_terms = {cell: [] for cell in run["lapse_index"]}
+    dir_terms = {idx: [] for idx, _ in run["lapse_dirs"]}
     for i, rec in enumerate(records):
         where = f"diagonal_terms record {i}"
         present_k, kind = _field(rec, "kind")
@@ -1451,7 +1712,10 @@
         for cell, w in weights.items():
             if cell in lapse_terms:
                 lapse_terms[cell].append(value * w)
-    return math.fsum(h_terms), {c: math.fsum(v) for c, v in lapse_terms.items()}
+        for idx, phi in run["lapse_dirs"]:
+            dir_terms[idx].append(value * _projected_weight(phi, weights))
+    return (math.fsum(h_terms), {c: math.fsum(v) for c, v in lapse_terms.items()},
+            {idx: math.fsum(v) for idx, v in dir_terms.items()})
 
 
 def _index_read_labels(run, labels):
@@ -1468,6 +1732,12 @@
             raise _Stop(
                 "failed", run["stage"], f"operator read label {lbl!r} collides with callback labels"
             )
+        if run["uniform_labels"] and _label_kind(lbl) in _uniform_kinds():
+            raise _Stop(
+                "failed", run["stage"],
+                f"operator read label {lbl!r} collides with the reserved uniform moment "
+                "labels (L23)",
+            )
         if lbl in index:
             raise _Stop("failed", run["stage"], f"read_rows: duplicate label {lbl!r}")
         index[lbl] = i
@@ -1620,13 +1890,31 @@
             else:
                 j = int(coord[3])
                 pair_da[idx] = -(1.0 if i == j else 2.0) * s_w[coord[1]][i][j]
+        # v003 source directions (L21): D_a = -sum_alpha phi_alpha sum_f c_f O_alpha,f, the
+        # UNNORMALIZED projection of this same evaluation (no division by any mode norm).
+        for idx, phi, fields in run["source_dirs"]:
+            terms = []
+            for cell in cells:
+                w = phi[cell]
+                if w == 0.0:
+                    continue
+                for f, c in fields:
+                    o = r_w[cell][f[1]] if f[0] == "whitened_R" else s_w[cell][f[1]][f[2]]
+                    terms.append(-w * c * o)
+            pair_da[idx] = math.fsum(terms)
+        # v003 uniform first/pair moments (L23): cell sums, tracked separately.
+        for lbl in run["uniform_labels"]:
+            if lbl[0] == "uniform_whitened_R":
+                values[lbl] = math.fsum([r_w[cell][lbl[1]] for cell in cells])
+            else:
+                values[lbl] = math.fsum([s_w[cell][lbl[1]][lbl[2]] for cell in cells])
     return values, pair_value, pair_da
 
 
 def _segment_core(run, state):
     """Dwell-segment record {state, key, D, r (lazy), Da, row} from FULL diagonal reads."""
     key = _state_key(run, state)
-    d_h, d_lapse = _diagonal_at(run, state)
+    d_h, d_lapse, d_dirs = _diagonal_at(run, state)
     values, pair_value, pair_da = _reads_at(run, state)
     src = math.fsum([-j * values[lbl] for lbl, j in run["sources"].items()])
     vol = math.fsum([a * values[lbl] for lbl, a in run["volume_gradient"].items()])
@@ -1641,9 +1929,11 @@
             da[idx] = -values[coord[1]]
         elif coord[0] == "volume_multiplier":
             da[idx] = -vol
-        else:
+        elif coord[0] == "lapse_direction":
+            da[idx] = d_dirs[idx]  # v003 projected lapse direction (L21)
+        else:  # pair_source_R / pair_source_S / v003 source_direction (callback reads)
             da[idx] = pair_da[idx]
-    row = np.array([values[lbl] for lbl in run["tracked"]], dtype=np.float64)
+    row = np.array([values[lbl] for lbl in run["tracked_all"]], dtype=np.float64)
     return {"state": state, "key": key, "D": diag, "r": None, "Da": da, "row": row}
 
 
@@ -1671,12 +1961,18 @@
 
 
 def _event_from_channel(run, ch):
-    """Event record with rho_a = W_a / W (lapse: wbar_alpha / multiplier; others 0)."""
+    """Event record with rho_a = W_a / W (lapse: wbar_alpha / multiplier; others 0).
+
+    v003 lapse directions (L21): rho_a = v_X / multiplier, v_X = sum_alpha phi_alpha
+    wbar_alphaX from the transition's own endpoint-averaged weights (projected per event).
+    """
     rho = np.zeros(run["n_u"], dtype=np.float64)
     for cell, w in ch["weights"].items():
         idx = run["lapse_index"].get(cell)
         if idx is not None:
             rho[idx] = w / ch["mult"]
+    for idx, phi in run["lapse_dirs"]:
+        rho[idx] = _projected_weight(phi, ch["weights"]) / ch["mult"]
     dq, dns, dn, _ = run["kinds"][ch["kind"]]
     return {"kind": ch["kind"], "owner": ch["owner"], "W": ch["W"], "rho": rho,
             "dq": dq, "dns": dns, "dn": dn}
@@ -2284,7 +2580,7 @@
     names = (
         [("score", a) for a in range(n_u)]
         + [("contact", (int(i), int(j))) for i, j in zip(iu[0], iu[1])]
-        + [("read", lbl) for lbl in run["tracked"]]
+        + [("read", lbl) for lbl in run["tracked_all"]]
         + [("events_per_path", None)]
     )
     prim = []
@@ -2393,10 +2689,171 @@
 
 
 # ----------------------------------------------------------------------------------
-# Result
+# Mode metadata and extensive outputs (v003; 0410 section 1, MODE SPEC; L21-L23)
 # ----------------------------------------------------------------------------------
 
 
+def _mode_metadata(run, modes, lapse):
+    """Profiles (S, sum, c1), unit-pairing Gram, directions and base sources; (meta, problem).
+
+    Called at the binding stage, after every profile is checked to list exactly
+    context.energy_cells. Nothing here divides a score or estimate by any mode norm.
+    """
+    cells = run["energy_cells"]
+    pids = []
+    phis = {}
+    directions = []
+    for key in run["coords"]:
+        if key not in modes:
+            continue
+        d = modes[key]
+        if d["profile_id"] not in phis:
+            pids.append(d["profile_id"])
+            phis[d["profile_id"]] = d["phi"]
+        directions.append({
+            "coordinate": key,
+            "id": d["id"],
+            "kind": d["kind"],
+            "profile_id": d["profile_id"],
+            "label_weights": None if d["fields"] is None else [list(fc) for fc in d["fields"]],
+        })
+    profiles = []
+    for pid in pids:
+        vals = [phis[pid][c] for c in cells]
+        s_norm = math.fsum([v * v for v in vals])
+        total = math.fsum(vals)
+        if not (math.isfinite(s_norm) and s_norm > 0.0 and math.isfinite(total)):
+            return None, f"mode profile {pid!r}: S = sum phi^2 = {s_norm!r} is not finite positive"
+        profiles.append({"profile_id": pid, "values": vals, "S": s_norm, "sum_phi": total,
+                         "c1": total / s_norm})
+    n_p = len(pids)
+    gram = np.zeros((n_p, n_p), dtype=np.float64)
+    for m in range(n_p):
+        for n in range(m, n_p):
+            g = math.fsum([phis[pids[m]][c] * phis[pids[n]][c] for c in cells])
+            if not math.isfinite(g):
+                return None, f"mode profiles {pids[m]!r}, {pids[n]!r}: Gram entry not finite"
+            gram[m, n] = g
+            gram[n, m] = g
+    worst = None
+    for m in range(n_p):
+        for n in range(m + 1, n_p):
+            r = abs(float(gram[m, n])) / math.sqrt(float(gram[m, m]))
+            r = r / math.sqrt(float(gram[n, n]))
+            worst = r if worst is None or r > worst else worst
+    pair = run["pair"]
+    base_pair = None
+    if pair is not None:
+        base_pair = {
+            "source_frame_input": pair["source_frame"],
+            "j_R_whitened": {c: list(pair["j_R"][c]) for c in pair["j_R"]},
+            "j_S_whitened": {c: [list(row) for row in pair["j_S"][c]] for c in pair["j_S"]},
+        }
+    meta = {
+        "pairing": (
+            "unit discrete cell pairing over context.energy_cells (weight 1 per cell); "
+            "unequal cell weights are not implemented (L22)"
+        ),
+        "cell_order": list(cells),
+        "profiles": profiles,
+        "profile_gram_order": list(pids),
+        "profile_gram": gram,
+        "gram_max_normalized_offdiagonal": worst,
+        "orthonormality_note": (
+            "orthonormality is the caller's declaration (0410); the actual Gram is reported "
+            "and never thresholded; nonorthogonal profiles need the root's Gram/dual pairing"
+        ),
+        "directions": directions,
+        "base": {
+            "lapse_factors": {c: lapse[c] for c in cells},
+            "source_coefficients": dict(run["sources"]),
+            "pair_sources": base_pair,
+            "note": "derivatives are taken around these base inputs (eta = 0)",
+        },
+        "uniform_moments": None if not run["uniform_labels"] else {
+            "labels": list(run["uniform_labels"]),
+            "n_cells": len(cells),
+        },
+        "extensive": None,
+        "note": (
+            "EXTENSIVE derivatives of F_total = -log Z / beta in the eta coordinates of the "
+            "declared directions; no division by S or any mode norm inside the sampler; the "
+            "full joint block is returned (no phase averaging, isotropy or cosine/sine "
+            "decoupling); normalization F_mode = F_total / S, Gram duals, Legendre transform, "
+            "J, background contacts and metric/EH pairing belong to the root metric adapter"
+        ),
+    }
+    return meta, None
+
+
+def _mode_outputs(meta, coord_order, point, tracked_all, beta, errors):
+    """Extensive mode block from the joint estimates (selection only; nothing divided by S)."""
+    pos = {key: i for i, key in enumerate(coord_order)}
+    keys = [d["coordinate"] for d in meta["directions"]]
+    kept = [k for k in keys if k in pos]
+    sel = np.array([pos[k] for k in kept], dtype=np.int64)
+    n_us = len(coord_order)
+    g = point["g"][sel]
+    hess = point["H"][np.ix_(sel, sel)]
+
+    def tri(p, q):
+        a, b = (p, q) if p <= q else (q, p)
+        return n_us + a * n_us - (a * (a - 1)) // 2 + (b - a)
+
+    grad_pos = [int(p) for p in sel]
+    hess_pos = [[tri(int(p), int(q)) for q in sel] for p in sel]
+    source_rows = [i for i, k in enumerate(kept) if k[0] == "source_direction"]
+    out = {
+        "coordinates": kept,
+        "dropped_unsupported": [k for k in keys if k not in pos],
+        "positions_in_coordinate_order": grad_pos,
+        "dlogZ_deta": g,
+        "d2logZ_deta2": hess,
+        "score_covariance": point["cov"][np.ix_(sel, sel)],
+        "contact_mean": point["T"][np.ix_(sel, sel)],
+        "F_total_gradient": -g / beta,
+        "F_total_hessian": -hess / beta,
+        "projected_read_means_extensive": {
+            "coordinates": [kept[i] for i in source_rows],
+            "values": np.array([g[i] / beta for i in source_rows], dtype=np.float64),
+            "note": (
+                "Q_ext = sum_alpha phi_alpha sum_f c_f <O_alpha,f> = <S_a>/beta "
+                "(unnormalized; equals -F_total_gradient on these rows)"
+            ),
+        },
+        "error_layout_positions": {"gradient": grad_pos, "hessian": hess_pos},
+        "F_total_gradient_standard_errors": None,
+        "F_total_hessian_standard_errors": None,
+        "errors_note": (
+            "joint errors are errors['jackknife_replicates'] / ['joint_covariance'] at the "
+            "listed y positions; F_total = -y/beta, so its standard errors are the jackknife "
+            "standard errors divided by beta (only when mixing passed)"
+        ),
+    }
+    if errors is not None:
+        se = errors["jackknife_standard_errors"]
+        out["F_total_gradient_standard_errors"] = se[np.array(grad_pos, dtype=np.int64)] / beta
+        out["F_total_hessian_standard_errors"] = (
+            np.array([[se[y] for y in row] for row in hess_pos], dtype=np.float64) / beta
+        )
+    uni = None
+    if meta["uniform_moments"] is not None:
+        r_idx = np.array([tracked_all.index(lbl) for lbl in meta["uniform_moments"]["labels"]],
+                         dtype=np.int64)
+        uni = dict(meta["uniform_moments"])
+        uni["read_positions"] = [int(r) for r in r_idx]
+        uni["error_layout_positions"] = [
+            n_us + (n_us * (n_us + 1)) // 2 + int(r) for r in r_idx
+        ]
+        uni["cell_sum_means"] = point["m"][r_idx]
+        uni["mode_responses"] = point["resp"][np.ix_(sel, r_idx)]
+        uni["note"] = (
+            "cell sums of whitened R'_i and S'_ij (i <= j) per state, time-averaged; no division "
+            "by n_cells, no Mandel factor, no central covariance (L23)"
+        )
+    return out, uni
+
+
 def _new_result():
     return {
         "ok": False,
@@ -2410,6 +2867,7 @@
         "tracked_read_labels": None,
         "read_kinds": None,
         "member_check": None,
+        "modes": None,
         "estimates": None,
         "errors": None,
         "mixing": None,
@@ -2456,6 +2914,15 @@
                 "contacts are exactly zero in these coordinates; other coordinates (raw-frame "
                 "sources included) by the caller's chain rule"
             ),
+            "mode_directions": (
+                "v003 (L21-L23): ('lapse_direction', id) differentiates eta in N_alpha = "
+                "N_alpha(base) + eta phi_alpha; ('source_direction', id) adds -eta sum_alpha "
+                "phi_alpha sum_f c_f O_alpha,f to H_c (whitened callback fields, unnormalized); "
+                "projected per primitive before storage; outputs are EXTENSIVE F_total "
+                "derivatives with no division by S or any mode norm; unit cell pairing; full "
+                "joint block, no phase averaging; normalization, Gram duals, Legendre and "
+                "metric pairing are the root metric adapter's"
+            ),
         },
         "scope": (
             "Static isothermal native functional of the quasi-static maximum-entropy closure at "
@@ -2501,7 +2968,7 @@
     Arguments (keyword-only, all required, no defaults; no value is chosen here):
       operator_api: mapping/object with the ACTUAL state-level callables listed in the module
         docstring (validate_owned_model, canonical_state_key, primitive_channels,
-        diagonal_terms, read_rows; plus owner_restricted_channels when palette_parameters is
+        diagonal_terms, read_rows; plus palette_channels when palette_parameters is
         not None), supplied at run time; nothing is imported.
       graph0, model, registration: passed unchanged to validate_owned_model. The model must
         be the common-phase zero-holonomy member (real h, t, g > 0, zero hopping phases,
@@ -2525,11 +2992,22 @@
         member's common phases (radians).
       derivative_coordinates: list of ("lapse", cell) | ("source", label) |
         ("volume_multiplier",) | ("pair_source_R", cell, i) | ("pair_source_S", cell, i, j)
-        with i <= j (pair coordinates need the callback; L20).
+        with i <= j (pair coordinates need the callback; L20) | (v003, L21) a fixed affine
+        mode direction mapping {"id": hashable (unique), "kind": "lapse_direction",
+        "profile_id": hashable, "cell_weights": {cell: finite real phi_alpha} over EVERY
+        cell of context.energy_cells, signed, not all zero} or {"id", "kind":
+        "source_direction", "profile_id", "cell_weights", "label_weights": {field: finite
+        real c_f} over ("whitened_R", i) / ("whitened_S", i, j), i <= j, not all zero}
+        (source directions need the callback). A mode direction's coordinate key is (kind,
+        id); its derivatives are around the base lapse_factors / sources (no partition
+        admission on phi). The tuple interface is unchanged and may be mixed with these.
       tracked_read_labels: list of read labels whose time averages, means and responses
         are returned (operator presence, first-moment Z, pair, population rows, or
         ("whitened_R", cell, i) / ("whitened_S", cell, i, j), i <= j, from the callback).
-        Operator coarse_first_R / coarse_second_S rows are unsupported in every role (L8).
+        Operator coarse_first_R / coarse_second_S rows are unsupported in every role: per
+        0409 the corrected moments come only from the callback and are never duplicated
+        (operator v001 rows: one global port frame; operator v002 rows: per-part B = -A
+        frames plus whitening, refused as duplicates) (L8).
       diagonal_read_source_callback: None, or the root adapter path {"adapter": object
         exposing adapted_moment_reads and pair_source_hamiltonian (and
         raw_to_whitened_sources for source_frame "raw"), "operator_module": object passed
@@ -2559,11 +3037,16 @@
         anything else returns status "unsupported".
 
     Returns a dict: ok, status, stage_reached, failures, flags, inputs, coordinate_order,
-    direction_status, tracked_read_labels, read_kinds, member_check, estimates {dlogZ_du, d2logZ_du2,
+    direction_status, tracked_read_labels, read_kinds, member_check, modes (None without mode
+    directions; else profile/Gram metadata, base sources, direction positions, extensive
+    F_total gradient/Hessian and score/contact moments, error-layout positions and uniform
+    first/pair moments; L21-L23), estimates {dlogZ_du, d2logZ_du2,
     score_covariance, contact_mean, F (None), F_u, F_uu, read_means, read_mean_responses,
     per_chain, mean/max events per path, samples}, errors (only when mixing passed),
     mixing, diagnostics, conventions, scope, limitations. "ok" is True only when status is
-    "complete", every requested direction is supported and mixing "passed".
+    "complete", every requested direction is supported and mixing "passed". With mode
+    directions and the callback, tracked_read_labels (output) ends with the nine reserved
+    uniform moment labels (L23).
     """
     result = _new_result()
     failures = result["failures"]
@@ -2571,7 +3054,7 @@
     if implicit_closure is not None:
         result["status"] = "unsupported"
         failures.append(
-            "implicit_closure: v002 implements ordinary fixed-source equilibrium sampling only; "
+            "implicit_closure: v003 implements ordinary fixed-source equilibrium sampling only; "
             "the SPEC section 5 implicit HP volume closure is a retained later contract, so "
             "implicit_closure must be None"
         )
@@ -2591,10 +3074,19 @@
     phases = _admit_gauge_phases(gauge_phases, failures)
     pair = _admit_pair_callback(diagonal_read_source_callback, graph0, registration, failures)
     pair_cells = None if pair is None else set(pair["j_R"])
-    coords = _admit_coordinates(derivative_coordinates, lapse, pair_cells, failures)
+    modes_in = {}
+    coords = _admit_coordinates(derivative_coordinates, lapse, pair_cells, failures, modes_in)
     tracked = _admit_labels("tracked_read_labels", tracked_read_labels, failures)
     if None not in (sources, vgrad, tracked, coords):
         _admit_label_roles(sources, vgrad, tracked, coords, pair_cells, failures, unsupported)
+    uniform_active = bool(modes_in) and pair is not None  # L23
+    if uniform_active and tracked is not None:
+        for lbl in tracked:
+            if _label_kind(lbl) in _uniform_kinds():
+                failures.append(
+                    f"input tracked_read_labels: {lbl!r} uses a reserved uniform moment kind; "
+                    "these columns are added automatically with mode directions (L23)"
+                )
     gens = _admit_generators(chain_generators, failures)
     paths_in = _admit_initial_paths(initial_paths, kinds, failures)
     if gens is not None and paths_in is not None and len(gens) != len(paths_in):
@@ -2627,6 +3119,12 @@
         "volume_multiplier": lam,
         "gauge_phases": phases,
         "derivative_coordinates": coords,
+        "mode_directions": [
+            {"coordinate": k, "profile_id": d["profile_id"],
+             "cells_weighted": len(d["phi"]),
+             "label_weights": None if d["fields"] is None else [list(fc) for fc in d["fields"]]}
+            for k, d in modes_in.items()
+        ],
         "tracked_read_labels": tracked,
         "diagonal_read_source_callback": None if pair is None else {
             "source_frame": pair["source_frame"],
@@ -2673,7 +3171,13 @@
         "volume_gradient": vgrad,
         "lam": lam,
         "tracked": tracked,
-        "n_r": len(tracked),
+        "tracked_all": list(tracked) + (list(_uniform_labels()) if uniform_active else []),
+        "n_r": len(tracked) + (len(_uniform_labels()) if uniform_active else 0),
+        "lapse_dirs": [(i, modes_in[c]["phi"]) for i, c in enumerate(coords)
+                       if c[0] == "lapse_direction"],
+        "source_dirs": [(i, modes_in[c]["phi"], modes_in[c]["fields"])
+                        for i, c in enumerate(coords) if c[0] == "source_direction"],
+        "uniform_labels": _uniform_labels() if uniform_active else (),
         "pair": None if pair is None else dict(pair, cells=None),
         "pair_coords": [(i, c) for i, c in enumerate(coords)
                         if c[0] in ("pair_source_R", "pair_source_S")],
@@ -2801,6 +3305,30 @@
             failures.append("raw_to_whitened_sources did not return sources on the same cells")
             return result
         run["pair"]["j_R"], run["pair"]["j_S"] = whitened
+    if modes_in:
+        # v003 mode directions (L21, L22): every profile lists exactly context.energy_cells;
+        # source directions need callback cells equal to those cells.
+        bad = [repr(k) for k, d in modes_in.items() if set(d["phi"]) != set(cells)]
+        if bad:
+            result["status"] = "failed"
+            failures.append(
+                f"mode directions {bad[:20]!r}: cell_weights must list exactly the cells of "
+                "context.energy_cells (explicit zeros; unit cell pairing, L22)"
+            )
+            return result
+        if run["source_dirs"] and set(run["pair"]["j_R"]) != set(cells):
+            result["status"] = "failed"
+            failures.append(
+                "source directions: diagonal_read_source_callback cells (j_R/j_S) must equal "
+                "context.energy_cells (L21)"
+            )
+            return result
+        meta, problem = _mode_metadata(run, modes_in, lapse)
+        if meta is None:
+            result["status"] = "failed"
+            failures.append(problem)
+            return result
+        result["modes"] = meta
 
     n_u = run["n_u"]
     n_r = run["n_r"]
@@ -2906,8 +3434,8 @@
     beta_f = run["beta"]
     all_events = np.concatenate([ser["events"] for ser in series])
     result["coordinate_order"] = [coords[i] for i in supported]
-    result["tracked_read_labels"] = list(tracked)
-    result["read_kinds"] = [_label_kind(lbl) for lbl in tracked]
+    result["tracked_read_labels"] = list(run["tracked_all"])
+    result["read_kinds"] = [_label_kind(lbl) for lbl in run["tracked_all"]]
     result["estimates"] = {
         "beta": beta_f,
         "dlogZ_du": point["g"],
@@ -2930,6 +3458,18 @@
     result["mixing"] = mixing
     result["errors"] = errors
     result["diagnostics"] = _diagnostics()
+    if result["modes"] is not None:
+        ext, uni = _mode_outputs(result["modes"], result["coordinate_order"], point,
+                                 run["tracked_all"], beta_f, errors)
+        result["modes"]["extensive"] = ext
+        result["modes"]["uniform_moments"] = uni
+        worst = result["modes"]["gram_max_normalized_offdiagonal"]
+        if worst is not None and worst != 0.0:
+            result["flags"].append(
+                f"mode profiles are not exactly orthogonal under the unit cell pairing (largest "
+                f"normalized Gram offdiagonal {worst!r}); the root pairing must use the returned "
+                "Gram (L22)"
+            )
     if mixing["constant_columns"]:
         result["flags"].append(
             "constant columns (no sample variation in any chain) are listed in "
```
