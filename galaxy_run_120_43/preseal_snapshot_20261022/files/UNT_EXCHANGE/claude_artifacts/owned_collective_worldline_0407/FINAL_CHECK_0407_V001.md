# FINAL CHECK 0407 V001: owned collective worldline static response, v002

**Role.** Distinct checker. I am not the author, not a reviewer and not the fix author of 0407.

**Method.** Static reading and hand trace only. I imported and executed nothing: not this module, not the operator (v001 or v002), not the root adapter, and no UNT, Codex or legacy code. I ran no numbers, did no sampling and extracted no data. The only code run was `python3 -I -B` doing `ast.parse` and `compile` (plus `symtable`) on a TEXT copy of v002 in my own scratch directory. No `__pycache__` exists in the 0407 directory. I did not write to `Universal Network Theory`. This file is the only file I wrote in the 0407 directory, and I wrote it by exclusive create. Date: 2026-10-16.

## Verdict: PASS_WITH_NOTES

- All four blocking items are closed in the v002 text:
  - the model-level member check (sampler review B1);
  - the 0408 blocked-palette move;
  - the 0409 actual operator API and root adapter;
  - the 0408 corrected moments in H_c and every source derivative.
- v001 is byte-identical. My own `diff -u v001 v002` is byte-identical to the diff embedded in FIX_DELTA. I found no logic change outside the four items.
- The AST inertness checks pass.
- I found no path that returns wrong numbers.
- Two items are **required** before root uses the palette move or the conventions note. Neither can produce wrong numbers.
  - **R1, API name.** Operator v002 now exists. v002 calls the palette enumeration `owner_restricted_channels(..., owners=...)`, but the operator provides `palette_channels(..., palette_owners=...)`. Passing the operator module directly with the palette move enabled ends as `failed` at input admission.
  - **R2, conventions note.** `CONVENTIONS_0407_V001.md` describes v001 and does not match v002.

## Hashes (full sha256, recomputed from bytes)

| File | sha256 | Match |
|---|---|---|
| owned_collective_worldline_static_response_v002.py (135141 B, 2946 lines) | 0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941 | as reported |
| owned_collective_worldline_static_response_v001.py (83799 B, 1921 lines) | 0552b71c88547bf0d0795976d2d3c333d8c38388831c8dc5499cb8ddd909eb8f | unchanged |
| FIX_DELTA_0407_V002.md (115332 B) | 94c1518231d42b58418111f790611d3c5d635195e6fbc4d88c5c66e2757a7b41 | as reported |
| CONVENTIONS_0407_V001.md | 7787d6a54ac1dbdf9e5374b215a4df2c399dde5a7e5f932815816614cd76f182 | unchanged since v001 |
| REVIEW_0407_SAMPLER_V001.md | 244a0cc986910e2a560c6c0453bd5b62d74339b07d9eae47f5ae44ddb6816c68 | as given |
| REVIEW_0407_ESTIMATOR_V001.md | f8627adb321ba378e209bdfe79c69286225e3f3d06d428bd50bb07dfa06debd7 | as given |
| owned_retained_response_0405/owned_parent_operator_v001.py | 27ad1762dbdc559eb92edcb6f7fe83790b73a4e23d71b12500b8586c811de3b6 | as given |
| owned_retained_response_0405/owned_parent_operator_v002.py (NEW, 128154 B, 04:15) | b5fded4d1272322036748d4d1b4e634a804c1da1ad6717e70e32b4f2a364a94e | read as text |
| root adapter owned_diamond_registration_input_adapter_v001.py | 0705be7ca500a3b8329566ba014b80645231be2178ad5b8ef089dbca163b3f77 | as given |
| 0407 brief | f3f60cebd42db1120b2193968404644a1890cf2f5e48563c2d94544a4bd33fc3 | as cited by the sampler review |
| 0408 | c0f0eaa940ce95c495fa2d7c21d59cae2a49e8028cc084df878d203e3c42e341 | as given |
| 0409 | 53465ac03cfb88bc7e641c15d8659591a315eafabb77dd966890e6dfb4ebb73c | as given |
| registration JSON | f65dbc234ae082df342235b1a6c13a0282cf94665ba3e1c3989d12b12e7d7174 | as given (not opened) |
| whitening companion JSON | 9eb4861cce5e4c435a259811dbca289e7e95a2b4ac34732c9f6c3ee56c34d7d7 | as given (not opened) |
| SPEC (positive worldline) | 915e8a43607bb93885b00c888a144d9f18fdbea0fccee046f9dab41523a80ec3 | as given |
| PALETTE note | 3b06ee3392894de2e96716c86f7b3184c792a407a81435f95aa448440418ca16 | as given |
| operator read/label addendum | 7cb15b4a5ac2ea33dfd43801c011142bc2b2388c3be0087152c049e78deccd39 | as given |

## Diff verification

- My own `diff -u` of v001 against v002 has 1941 body lines. They are byte-identical to the fenced diff in FIX_DELTA, lines 151-2091.
- Every hunk maps to one of the four items or to the documentation of those items. The estimator reviewer's N2 fix-at-reconciliation item is included: unknown read labels now fail closed.
- `_interval_move` was refactored into `_select_interval`, `_move` and `_interval_move`. When the palette move is off, it consumes the per-chain RNG in exactly the v001 order.
- Two orderings changed, both pure:
  - The old-path integral is now computed after the endpoint check.
  - At measurement, the stored per-segment read row replaces a re-read keyed by state. The values are the same and come from the same deterministic evaluation.
- No other logic changed.

## Closure table

| Item (source) | Required fix | v002 evidence (line) | Status |
|---|---|---|---|
| **B1** model-level member (sampler review) | State-independent check of every supplied coefficient before sampling; `unsupported` if absent, failing or not evaluable; keep the visited-state check; correct L2 and the docstrings | See the B1 detail below | **CLOSED** (residual R5) |
| **0408 palette move** (fix-author issue 2; brief 0408) | Additive move: permanent-label palettes, held outside marks, restricted CTMC, held-rate ratios, endpoint rejection with no bridge, global moves kept | See the palette detail below | **CLOSED in text**; operator name/keyword open as **R1** |
| **0409 forced: operator API and root adapter** | Use the actual operator records and the actual adapter signatures; no conflicting adapter; no duplicated or unsupported raw sources | See the API detail below | **CLOSED for operator v001 and the adapter.** For operator v002, only the palette name/keyword is open (**R1**, fails closed) |
| **0408 forced: corrected moments** | Full outgoing reads after every transition, Birth included; the callback used consistently in H_c, D, D_a, D_ab and the moments; fixed whitening on reads and duals; current present count | See the moments detail below | **CLOSED** |

**B1 detail.**
- `_model_schema` (L468) defines the 13 scalars plus h, t, theta, g, kappa and epsilon. This is identical to `_SCALAR_KEYS`/`_PROFILE_KEYS` in operators v001 and v002.
- `_profile_entries` (L1058) yields the supplied entries. `_model_member_check` (L1082) applies these tests to every entry:
  - h, t, g finite real > 0;
  - theta exactly 0;
  - kappa and epsilon nonzero, with phase equal to `admission_phase` / `birth_phase` within the gauge_phase tolerance;
  - scalars finite real.
- A missing or unknown key, a non-evaluable profile, or a violation returns `unsupported`.
- The member-check stage (L2734-2753) runs after `validate_owned_model` and before the binding stage, any initial path or any operator state call.
- The second line remains: every enumerated primitive at every visited state is gauge-checked, restricted enumerations included (`_channels_from_records` L1243-1281).
- L2 (L204-226), the module docstring (L110, L137-139) and the public docstring (L2508-2513) are corrected.
- Hand check of the gauge factors (`_gauge_table` L1033):
  - flip -h, hop -t at theta=0 and bind -g each give -|.|;
  - admit: conj(s_a)·kappa = -|kappa|;
  - birth: conj(s_b)·eps = -|eps|;
  - the reverses are the conjugates and also give -|.|.
- The adapter's `build_inputs` model passes:
  - g and kappa are dicts over all 6L^3 vertex labels;
  - epsilon is a dict over the owners;
  - h, t and theta are `UniformEdgeProfile`. By its text (adapter L55-69), its `__call__` returns `self.value` for every ordered A-B pair and raises otherwise, so checking `.value` covers every coefficient it can supply.

**Palette detail.**
- `_move` (L1879) chooses with state-independent probabilities. Admission requires p_rot + p_palette < 1 (L2606).
- Groups come from graph0 A/B/slots (binding stage, L2756ff). `_record_groups` (L1318) parses the actual owner_id formats of operators v001 and v002 (op v002 `_owner_id` L1672):
  - `("birth", owner, cut)`;
  - `(family, ("edge", (A, B)))`;
  - `(family, ("vertex", v))`, with family "admission" for admit/admit_rev.
- These groups equal the operator v002 `_palette_scope` rule (op v002 L1415-1432).
- `_palette_move` (L1969):
  - holds the out-of-palette marks with their times and (kind, owner_id);
  - runs member channels with r_S, restarting the exponential at each held time (memoryless);
  - replays each held mark through the restricted enumeration on its own groups; an absent or zero-rate record rejects, and more than one match fails;
  - applies the self-loop and reverse checks to replays;
  - rejects on endpoint mismatch;
  - uses log ratio = ∫(r_S−D) new − ∫(r_S−D) old + Σ_held log(W_new/W_old), with r_S recomputed on the old segments over the same palette (L2077-2088);
  - is never a conditioned bridge.
- Caps end the run as `incomplete` (L1949) and replayed marks count as events.
- My hand trace of the detailed balance matches the PALETTE density cancellation: the selection is symmetric, the reverse holds the same skeleton, and the inside factors cancel.
- Held-descriptor uniqueness holds in the actual operator:
  - Forward cuts are deduplicated, and each reverse permutation gives a distinct restored cut (op v002 L1043-1157).
  - Hop owner_id carries no direction. The replay is the swap involution, so the descriptor is a well-defined partial map, as PALETTE requires.

**API detail.**
- `diag` records are skipped (L1255, L1374).
- `energy_weights` is aligned with `context.energy_cells` (L1181), and the binding stage checks that lapse covers exactly those cells.
- The diagonal value is taken from `amplitude` (L1430).
- `read_rows` is read as `{labels, values, presence}` arrays (L1547-1563, `_index_read_labels` L1457).
- The adapter is called with its exact keywords:
  - `adapted_moment_reads` (L1571);
  - `pair_source_hamiltonian` (L1588);
  - `raw_to_whitened_sources` (L2790).
- The adapter's `state_labels` dependency is checked (L572).
- Operator `coarse_first_R` and `coarse_second_S` are unsupported in every role (L659-689). Whitened R'/S' are exposed once (i <= j) and sourced only through the pair source.
- The adapter's raw, presence, Z and ZZ outputs are never read.

**Moments detail.**
- `_segment_core` (L1626-1647) runs at every new state: initial, global, palette and held replay, Birth included. It calls `diagonal_terms`, `read_rows` and the callback.
- The single evaluation feeds:
  - D = H[N]diag − j·O + P − λA;
  - every D_a, with pair coordinates −R'_i and −mult·S'_ij for mult 1 or 2 (L1616-1622);
  - the stored row used by `_measure` (L2184).
- D_ab = W_ab = 0 because every coordinate is affine.
- The adapter value must match the linear reconstruction within `source_consistency_tolerance` (L1598-1614).
- Whitening is the adapter's fixed W. Dual sources are caller input, or converted once.

**Carried review notes.**
- Estimator N1 (member check) is closed by B1.
- Estimator N2 (unseen label gave a silent zero) is closed: referenced labels must be operator labels at the first read (L1474-1482), and whitened labels must be callback cells.
- Estimator N5 (L8 stale) is closed for operator v001. L8 is stale again for operator v002 (see R3).
- Sampler N1 (record formats) is closed.
- Sampler N2 (reverse fallback only when the filtered sum is 0, L1716), N5 (generators checked by `id` only, L807-825), N6 (cap sizing for proposal length is undocumented) and N7 (per-chain SEs shown when mixing failed) are unchanged. They are non-blocking and remain open notes.

## AST inertness (v002 text copy, `python3 -I -B`)

- `ast.parse` and `compile(..., "exec")`: OK.
- Imports are only `bisect`, `math`, `collections.abc.Mapping` and `numpy`.
- There is no `@` or `@=`, and no `dot`/`matmul`/`vdot`/`inner`/linalg attribute.
- There are 10 `einsum` calls, all with `optimize=False`.
- There is no `print`/`open`/`eval`/`exec`/`compile`/`__import__`/`input`/`globals`/`locals`/`vars`/`breakpoint`/`exit`. No `os`/`sys`/`subprocess`/`threading`/`socket`/`pickle`/`ctypes` name or I/O attribute appears.
- Module level holds the docstring, 4 imports, `LIMITATIONS` (a string constant), `class _Stop` and 84 `def`s. There are no decorators and no global/nonlocal statements, so nothing runs at import.
- The `symtable` scan found no undefined globals.
- There is one public function with 0 positional and 23 keyword-only parameters, none with a default. They match the reported list.

## API reconciliation (v002 expectation vs actual operator v001 / v002 / root adapter)

| v002 expects | Operator v001 (27ad1762…) | Operator v002 (b5fded4d…) | Result |
|---|---|---|---|
| `validate_owned_model(*, graph0, model, registration)` returns ok/stage_reached/failures/context; `context.energy_cells` | same (L774); energy_cells = reg cells | same (L979). Registration keys are now 8 and include a required `whitening`; `port_vectors` may be global, {A,B}, per-vertex or callable | compatible. **M5**: the adapter's `build_inputs` registration has 7 keys, so op v002 validation fails closed until the runner adds `whitening` and `{'A': T, 'B': -T}`. The augmented object must also be `binding['registration']`, because v002 checks identity (L578-584) |
| model h, t, theta (member check `.value` for callables) | Mapping only; a callable is rejected (`_edge_table` L501) | Mapping or accessor called as `accessor(edge=(A, B))` (L625) | op v001 plus adapter model gives `failed` (recorded in v002). op v002 is compatible |
| `canonical_state_key(*, context, state)` gives a tuple of ints | L1456 | L1772 | match |
| `primitive_channels(*, context, state)` with records owner_id, kind (diag + 7 kinds), target_state, amplitude, queried_support, changed_support, energy_weights | L1485, `_Channel` L231 | L1801, `_Channel` L353 | match |
| `diagonal_terms(*, context, state)`: diag records, value = amplitude, energy_weights | L1473 | L1789 | match |
| `read_rows(*, context, state)` returns {labels (state-independent tuple), values f64[n], presence f64[n]} | L1503 | L1861 (the same `ctx.read_labels` object every call) | match |
| owner_id formats parsed by `_record_groups` | `_owner_id` L1358 | `_owner_id` L1672 | match |
| **`owner_restricted_channels(*, context, state, owners)`** (ASSUMED; required only when `palette_parameters` is not None) | **absent** | **`palette_channels(*, context, state, palette_owners)`** (L1837). It takes a list/tuple/set/frozenset of original owner labels. It returns the palette-owned `diag` records plus member transition records, with the same fields and the same membership rule (L13) | **M1 name mismatch, M2 keyword mismatch (`owners` vs `palette_owners`).** The argument type, record fields and membership rule are compatible, and the extra `diag` records are skipped (L1374). Fails closed (`failed`) when the module is passed directly |
| operator coarse rows `coarse_first_R` / `coarse_second_S` refused in every role (L8, L476-479, L670, L2532) | one global frame, no whitening: refusal justified | per-vertex/per-part frames and fixed whitening inside the rows (op v002 L140-153, L8, `_reads_from_z` L1726) | **M4**: compatible and fail-closed (`unsupported` only if referenced), but the stated reason is false for op v002 (see R3) |
| adapter `adapted_moment_reads(*, operator_module, context, state, binding)` returning `cells`, `R[cell]` (3), `S[cell]` (3x3, exactly symmetric) | adapter L177-232 | same | match. The binding also needs `L` (adapter L184); if `L` is absent, the run ends as `failed` |
| adapter `pair_source_hamiltonian(*, reads, j_R, j_S)` with j as cell maps | L235 | same | match |
| adapter `raw_to_whitened_sources(*, j_R_raw, j_S_raw)` returning (dict, dict) | L254 | same | match (exact symmetry is preserved elementwise) |
| `operator_module.state_labels` (used by the adapter) | L1467 | L1783 | match |

## CONVENTIONS_0407_V001.md vs final module: does NOT match (R2)

1. **API line.** The note still lists `extra_diagonal_reads`. It lacks `diagonal_read_source_callback` and `palette_parameters`.
2. **"Assumed operator API".** It lists record field `weights` (actual: `energy_weights`), diagonal `value`/`weights` (actual: `amplitude`/`energy_weights`), and read rows as records with label/value/kind (actual: `{labels, values, presence}` arrays). It has no `diag` kind and no palette enumeration.
3. **Outputs.** The note lacks `member_check`. It still lists "labels never observed" in diagnostics, which was removed; such a label is now a `failed` input. It does not say that `read_kinds` is now the label kind token.
4. **Signs/coordinates.** H_c lacks −j_R'·R' − J_S':S'. The coordinates lack `pair_source_R` and `pair_source_S`, including the multiplicity 1 or 2.
5. **Positive gauge.** Only the visited-state check is described. The model-level member check is missing.
6. **Cost.**
   - Per-event work now includes `adapted_moment_reads` and the restricted enumerations.
   - "One read_rows call per distinct dwell state" at measurement is stale; stored rows are used now.
   - Storage is now O(n_u + n_r) per dwell.
7. **Moves / not implemented.** The note says efficiency moves are not implemented. The additive blocked-palette move now exists, with p_rot + p_palette < 1.
8. **Limitations range.** The note says "items L1–L18"; the module now has L1–L20.

## Remaining real issues

- **R1 (REQUIRED for the palette move; fails closed, never wrong numbers).**
  - v002 names the restricted enumeration `owner_restricted_channels(..., owners=...)` (L86, L202, L455, L1389). Operator v002 exposes `palette_channels(..., palette_owners=...)`.
  - Reconcile either way:
    - in a v003: change the name in `_admit_operator_api` and the `_op` call in `_palette_channels`, and the keyword to `palette_owners`, then update L1, L19 and the docstrings;
    - or have the root runner pass `operator_api` as a mapping that aliases `owner_restricted_channels` to `palette_channels` with keyword translation. v002 already admits a mapping as `operator_api`.
- **R2 (REQUIRED, documentation).** CONVENTIONS_0407_V001.md does not describe v002 (8 points above). A CONVENTIONS V002 is needed before the return, or the FIX_DELTA must be explicitly designated as superseding it.
- **R3 (non-blocking, documentation; reconciliation with operator v002).**
  - L8, `_unsupported_raw_kinds`, the admission message (L670) and the public docstring (L2532) justify refusing the operator coarse rows by "one global port frame". Operator v002 rows are corrected: per-part B = −A frames plus registration whitening.
  - The refusal itself stays valid as the no-duplication rule (0409): corrected R'/S' enter only through the adapter callback.
  - The stated reason should say that, and name both operator versions.
- **R4 (non-blocking, integration; root runner).**
  - With operator v002, the adapter's `build_inputs` registration needs `whitening` and per-part `port_vectors`. op v002 L14 says its validation fails closed otherwise.
  - The same registration object must appear as `binding['registration']`, and `binding` must carry `L`. Otherwise v002 fails closed.
  - With operator v001, the adapter's callable model is rejected (`failed`).
- **R5 (non-blocking residual, documented in L2).**
  - Any callable profile that exposes `.value` is admitted on that declaration.
  - For the root `UniformEdgeProfile` this is exact (adapter L55-69).
  - A different callable whose returned values differ from `.value` would be caught only on visited edges (second line).
  - 0408 permits declared-uniform caller input. Admitting only the adapter class's declared form would remove the residual.
- **R6 (non-blocking; carried from the sampler review).** N2, N5, N6 and N7 are unchanged; see the carried review notes.
- **R7 (scope).** Operator v002 itself has no review file on disk in the 0405 directory at the time of this check. Every compatibility statement above rests on a static text reading only.

No physics, value, scale or target was chosen or read. Run status: nothing executed.
