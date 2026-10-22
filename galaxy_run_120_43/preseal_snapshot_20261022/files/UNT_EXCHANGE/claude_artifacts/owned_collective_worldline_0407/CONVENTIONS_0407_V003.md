# 0407 conventions: owned collective worldline static response, v003

Module: `owned_collective_worldline_static_response_v003.py`, in this directory (164654 bytes, 3486 lines, sha256 `e367f240e3cfc38300dee75a85a56bc13fb1eaa2ee8f3a26fe8a270216e97721`).

- It is static author text. Its author never imported or ran it.
- It uses numpy and the Python standard library only (`bisect`, `math`, `collections.abc.Mapping`).
- It is v002 (sha256 `0d041119bd11227746238663ed93d99863d3a94c8295e539dbed15255b42a941`, unchanged) plus three things:
  - the 0410 section 1 direct real-mode derivative columns;
  - the FINAL_CHECK R1 call to the actual operator v002 palette enumeration;
  - the FINAL_CHECK R3 wording for the coarse-row refusal.

This note replaces `CONVENTIONS_0407_V001.md` for v003. That note stays as the record for v001. v002 is covered by `FIX_DELTA_0407_V002.md` plus this note, because v003 changes no v002 logic for runs without mode directions. Line numbers below refer to v003.

## 1. Signature

There is one public function. Every argument is keyword-only and required. None has a default. The signature is unchanged from v002, and v003 adds no public argument.

```
owned_collective_worldline_static_response(*, operator_api, graph0, model, registration,
    initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients,
    volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels,
    diagonal_read_source_callback, chain_generators, move_parameters, palette_parameters,
    caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances,
    implicit_closure)
```

The module chooses no value. The full shapes are in the public docstring (L2940ff).

| Argument | Shape and meaning |
|---|---|
| `operator_api` | A mapping or object exposing the actual operator callables (section 2). `palette_channels` is required only when `palette_parameters` is not None. |
| `graph0`, `model`, `registration` | Passed unchanged to `validate_owned_model`. The callback binding must hold the SAME `graph0` and `registration` objects. |
| `initial_paths` | One entry per chain: `{"x0": state, "events": [{tau, kind, owner_id, target_key}, ...]}`. An empty list is the constant path. Each path must close and must net zero gauge increments. |
| `beta` | A finite real > 0. It is one global inverse energy. |
| `lapse_factors` | `{cell: N_alpha > 0}` for exactly `context.energy_cells`. This is the positive base lapse. |
| `source_coefficients` | `{operator read label: j_a}`. H_c gains −Σ j_a O_a. |
| `volume_gradient_coefficients`, `volume_multiplier` | A = Σ a_a O_a; H_c gains −λA. Whitened callback labels are allowed in A. |
| `gauge_phases` | `{"admission_phase": arg kappa, "birth_phase": arg epsilon}`. |
| `derivative_coordinates` | Tuple coordinates, as in v002: `("lapse", cell)`, `("source", label)`, `("volume_multiplier",)`, `("pair_source_R", cell, i)`, `("pair_source_S", cell, i, j)` with i <= j. **v003 mode-column inputs:** mode-direction mappings (section 6). Both kinds may be mixed in one list. |
| `tracked_read_labels` | Operator read labels, or callback labels `("whitened_R", cell, i)` / `("whitened_S", cell, i, j)` with i <= j. In mode runs with the callback, the kinds `uniform_whitened_R` and `uniform_whitened_S` are reserved. |
| `diagonal_read_source_callback` | None, or `{"adapter", "operator_module", "binding", "source_frame": "whitened" or "raw", "j_R": {cell: 3 reals}, "j_S": {cell: exactly symmetric 3x3 reals}, "source_consistency_tolerance": real >= 0}`. |
| `chain_generators` | Distinct `numpy.random.Generator` objects, one per chain. |
| `move_parameters` | `{"moves_per_sweep" >= 1, "rotation_probability" in (0,1), "whole_circle_probability" in (0,1), "length_components": [(weight > 0, upper_fraction in (0,1]), ...]}`. At least one upper_fraction must be 1. |
| `palette_parameters` | None, or `{"selection_probability" in (0,1), "palettes": [(weight > 0, nonempty collection of original owner labels), ...], "verify_against_full_enumeration": bool}`. Admission requires p_rot + p_palette < 1. |
| `caps` | `{"max_events_per_path", "max_total_events", "max_sweeps", "max_channel_enumerations"}`, each a positive int. Reaching any cap ends the run as `incomplete`. |
| `burn_in_sweeps`, `measurement_sweeps` | int >= 0 and int >= 1. There is one measurement per sweep. |
| `error_parameters` | `{"batches_per_chain" >= 2 dividing measurement_sweeps, "sokal_window_constant" > 0, "rhat_max" >= 1, "min_batch_length_over_tau" > 0, "max_explicit_covariance_dimension" >= 0}`. |
| `numerical_tolerances` | `{"gauge_phase", "weight_partition", "reverse_rate"}`, each a real >= 0. |
| `implicit_closure` | Must be None. Anything else returns `unsupported`. |

## 2. Actual operator and adapter API

The module never imports any of these. It calls them at run time through the objects the caller passes.

**Operator.** These are `owned_parent_operator_v001.py` (sha256 `27ad1762...`) and `owned_parent_operator_v002.py` (sha256 `b5fded4d...`). Both were read as text.

- `validate_owned_model(*, graph0, model, registration)` returns `{"ok", "stage_reached", "failures", "context"}`.
  - `context.energy_cells` is the ordered cell tuple. In both operator versions it equals `registration["cells"]`.
- `canonical_state_key(*, context, state)` returns a tuple of ints. `==` must give one bool.
- `primitive_channels(*, context, state)` returns records before aggregation.
  - Fields: `owner_id`, `kind`, `target_state`, `amplitude`, `queried_support`, `changed_support`, `energy_weights`.
  - `kind` is one of diag, flip, hop, bind, admit, admit_rev, birth, birth_rev.
  - `energy_weights` is a dense tuple aligned with `context.energy_cells`, equal to (w(target) + w(source))/2.
  - "diag" records are skipped. A record with amplitude exactly 0 is skipped.
- `diagonal_terms(*, context, state)` returns the "diag" records.
  - The value is `amplitude`, which must be real.
  - `energy_weights[alpha]` = w_alphaX(state).
- `read_rows(*, context, state)` returns `{"labels", "values", "presence"}`.
  - `labels` is a state-independent tuple. `values` and `presence` are float64 arrays.
  - Referenced labels are indexed once. An unknown referenced label is `failed`.
- `palette_channels(*, context, state, palette_owners)` exists in operator v002 only (op v002 L1837).
  - The module passes `palette_owners` as a frozenset of original owner labels.
  - It returns the palette-owned "diag" records, which are skipped, plus the member transition records.
  - With operator v001, a non-None `palette_parameters` ends as `failed` at input admission (L1, FINAL_CHECK R1).
- `owner_id` formats parsed for palette groups:
  - `("birth", owner, cut)`;
  - `(family, ("edge", (A, B)))`;
  - `(family, ("vertex", v))`, with family "admission" for admit and admit_rev.

**Root adapter.** This is `owned_diamond_registration_input_adapter_v001.py` (sha256 `0705be7c...`), read as text only. The module calls exactly these three functions:

- `adapted_moment_reads(*, operator_module, context, state, binding)` returns `{"cells", "R", "S", ...}`.
  - It uses `operator_module.state_labels`, `binding["L"]`, `binding["graph0"]` and `binding["registration"]`.
  - Only `cells`, `R` (whitened, 3 per cell) and `S` (whitened, an exactly symmetric 3x3 per cell) are read.
  - Its raw, presence, Z and ZZ outputs are never read.
- `pair_source_hamiltonian(*, reads, j_R, j_S)` returns −j_R'·R' − J_S':S'.
- `raw_to_whitened_sources(*, j_R_raw, j_S_raw)` returns `(j_R', J_S')`. It is called once, and only for `source_frame` "raw".

The adapter's `label_metadata`, `make_port_order`, `build_inputs`, `bind_context` and `central_covariance` are the root runner's, and the module does not call them. The member check recognizes `UniformEdgeProfile` through its declared `value`.

**Integration notes.** These are carried from FINAL_CHECK R4. They fail closed, never wrong.

- With operator v002, the `build_inputs` registration needs `whitening` and `port_vectors` `{'A': T, 'B': -T}`.
- That same object must be `binding["registration"]`, and `binding` must carry `L`.
- Operator v001 rejects the adapter's callable edge profiles, so `validate_owned_model` gives `failed`.

## 3. Hamiltonian, signs and coordinates

With n = N − 1 and per-primitive weights w̄ from the operator:

- W_X(x→y) = |h_X[y,x]| · (1 + Σ_α n_α w̄_αX), with the multiplier applied before aggregation.
- D(x) = Σ_diag d_X(x)(1 + Σ_α n_α w_αX(x)) − Σ_a j_a O_a(x) + P(x) − λA(x).
- P(x) = `pair_source_hamiltonian` = −j_R'·R'(x) − J_S':S'(x). It is the root adapter's whitened pair source, and 0 without the callback.
- H_c = H[N] − Σ j_a O_a − j_R'·R' − J_S':S' − λA, and Z = Tr e^{−βH_c}.

Each new state gets one full evaluation: `diagonal_terms`, `read_rows` and the callback. This holds after every transition, Birth and held replays included. That single evaluation feeds D, every D_a, the tracked row and the uniform moments.

The adapter value must match the module's linear reconstruction within `source_consistency_tolerance`. Otherwise the run is `failed`.

**Coordinates.** All are affine, so D_ab = W_ab = 0 exactly.

| Coordinate | Differentiates | D_a | ρ_a = W_a/W per event |
|---|---|---|---|
| `("lapse", cell)` | n_α (= N_α) | Σ_diag d_X w_αX | w̄_αX / multiplier |
| `("source", label)` | j_label | −O_label | 0 |
| `("volume_multiplier",)` | λ | −A | 0 |
| `("pair_source_R", cell, i)` | j_R'[cell][i] | −R'_i | 0 |
| `("pair_source_S", cell, i, j)`, i <= j | the symmetric pair J_S'[i][j] = J_S'[j][i] | −mult · S'_ij, with mult 1 (i = j) or 2 (i < j) | 0 |
| `("lapse_direction", id)` (v003) | η in N_α = N_α(base) + η φ_α | Σ_diag d_X v_X, with v_X = Σ_α φ_α w_αX | v_X / multiplier, from the transition's own endpoint-averaged weights |
| `("source_direction", id)` (v003) | η in H_c − η Σ_α φ_α Σ_f c_f O_α,f | −Σ_α φ_α Σ_f c_f O_α,f (unnormalized whitened R'_i, S'_ij) | 0 |

**Estimators.**
- Per path: S_a = −∫D_a + Σ_events ρ_a and T_ab = −Σ_events ρ_a ρ_b.
- ∂_a log Z = ⟨S_a⟩ and ∂_ab log Z = Cov(S_a, S_b) + ⟨T_ab⟩.
- F_a = −⟨S_a⟩/β and F_ab = −(Cov + ⟨T⟩)/β. Absolute F is not estimated (None).
- For a lapse coordinate, F_{n_α} = ⟨E_α⟩. For a read source, F_j = −⟨O⟩.
- Tracked reads: ⟨(1/β)∫O⟩, and their responses Cov(S_a, Ō_r) on the same ensemble.

**Thermal Legendre.**
- F + j·Q has QQ Hessian +χ⁻¹.
- F_jj = −χ_OO^iso, F_nn = −χ_EE^iso and F_nj = +χ_EO^iso, with χ^iso_AB = ∫₀^β ⟨δA(τ)δB(0)⟩.
- Real-time action signs are not imported.

The result is the static isothermal native functional at fixed β. It is not fixed-preparation retarded response, and it is not the complete metric propagator. τ is imaginary time, and the Monte Carlo sweeps are Markov iterations; neither is physical time.

## 4. Positive gauge and the model-level member check

The positive gauge is G = (−1)^{Σq} (−e^{i·admission_phase})^{N_S} (−e^{i·birth_phase})^{N}. Every gauged off-diagonal element must equal −|h| within the relative `gauge_phase` tolerance. Otherwise the result is `unsupported`. The rate is W = |h| · multiplier ≥ 0.

**First line, model level** (`_model_member_check` L1330; stage "member_check" L3239). This check runs after `validate_owned_model` and before any state is visited.

- The model keys must be exactly the contract schema: 13 diagonal scalars plus the profiles h, t, theta, g, kappa and epsilon.
- Every supplied entry is checked:
  - h, t and g are finite reals > 0;
  - theta is exactly 0;
  - kappa and epsilon are nonzero, with phase equal to `admission_phase` / `birth_phase` within tolerance;
  - each scalar is a finite real.
- A Mapping profile is checked entry by entry. A bare scalar is a declared uniform value. A callable profile is admitted only through its declared `value` (the root `UniformEdgeProfile`).
- A violation, an unknown or missing key, or a profile that cannot be evaluated gives `unsupported`.
- `result["member_check"]` = `{status, profile_forms, problems, note}`.

**Second line, visited states.** Every primitive enumerated at every visited state, restricted palette enumerations included, must gauge to −|h|. Net gauge increments of regrown segments must match.

## 5. Moves

`_move` (L2175) picks one of three moves with state-independent probabilities:

- **Rotation**, with probability p_rot.
- **Additive blocked palette**, with probability p_palette (`_palette_move` L2265, L19).
- **Global interval regrowth**, with probability 1 − p_rot − p_palette > 0 (`_interval_move` L2188). This is an unconditioned reference CTMC with endpoint rejection.

**The palette move in detail.**
- Old events in the interval whose permanent groups miss the palette are held, with their times and (kind, owner_id).
- Member channels run with their actual rates and r_S. The enumeration is `palette_channels` (L1641; operator v002).
- Each held mark is replayed on its own groups. An absent or zero-rate record rejects. More than one match is `failed`.
- An endpoint mismatch rejects. The proposal is never renormalized as a conditioned bridge.
- The log ratio is ∫_I new(r_S − D) − ∫_I old(r_S − D) + Σ_held log(W_new/W_old).
- `verify_against_full_enumeration` cross-checks every restricted call against `primitive_channels`.

## 6. Mode-column inputs and outputs (v003; 0410 section 1, MODE SPEC; L21–L23)

**Input.** These are elements of `derivative_coordinates`:

```
{"id": ID, "kind": "lapse_direction",  "profile_id": PID, "cell_weights": {cell: phi_alpha}}
{"id": ID, "kind": "source_direction", "profile_id": PID, "cell_weights": {cell: phi_alpha},
 "label_weights": {field: c_f}}
```

- Every key is required, and none has a default. `id` values are unique.
- The coordinate key is `(kind, id)`.
- `cell_weights` lists exactly `context.energy_cells`, with explicit zeros. The values are signed finite reals and must not all be zero.
- **No sign, sum or partition admission** is applied to φ. These are derivative directions around the positive base `lapse_factors` and the base sources, not an energy partition. The operator's own `energy_weights` keep their V002 partition check.
- Directions that share a `profile_id` must have identical `cell_weights`.
- `field` is one of the nine whitened callback fields: `("whitened_R", i)` and `("whitened_S", i, j)` with i <= j.
  - The module adds no multiplicity. c_f on an off-diagonal S field is the caller's chart factor, for example √2 for a Mandel component.
  - Equivalently, c_f = mult × the coefficient of `("pair_source_S", cell, i, j)`.
- A source direction needs the callback, and the callback cells must equal `context.energy_cells`.
- A source direction is a fixed combination of the pair coordinates. It allocates no new source: the base sources stay the callback's j_R'/J_S'.

**Projection before storage.**
- ρ_a is projected per primitive (`_event_from_channel` L1963). D_a is projected per state (`_diagonal_at` L1673; `_reads_at` L1893ff).
- Only n_u projected columns are stored per dwell and per event. For one joint cosine/sine block of 1 lapse plus 9 sources, n_u = 20.
- No per-cell column, full cell Hessian or 640-coordinate block is ever formed.
- The same incoming/outgoing endpoint-averaged allocations as H[N] are used. Source directions read the same corrected callback evaluation that enters H_c.

**Output: `result["modes"]`.** It is None without mode directions. The metadata is set at the binding stage (`_mode_metadata` L2696), and the estimates are added after analysis (`_mode_outputs` L2789).

- `pairing`: the unit cell pairing over `context.energy_cells`. `cell_order` gives the cells.
- `profiles`: for each profile, `{profile_id, values, S = Σφ², sum_phi, c1 = Σφ/S}`.
- `profile_gram_order` and `profile_gram`: G_mn = Σ_α φ_m φ_n.
- `gram_max_normalized_offdiagonal`: the largest |G_mn|/√(G_mm G_nn), or None. A nonzero value adds a flag.
- `directions`: for each direction, the coordinate, id, kind, profile_id and label_weights.
- `base`: the lapse factors, the source coefficients and the whitened pair sources actually used.
- `extensive` (filled only when status is complete):
  - `coordinates`, `dropped_unsupported` and `positions_in_coordinate_order`;
  - `dlogZ_deta`, `d2logZ_deta2`, `score_covariance` and `contact_mean`;
  - `F_total_gradient` = −⟨S⟩/β and `F_total_hessian` = −(Cov + ⟨T⟩)/β;
  - `projected_read_means_extensive`, with Q_ext = ⟨S_a⟩/β on the source rows;
  - `error_layout_positions`, the y indices of the gradient and Hessian entries;
  - `F_total_gradient_standard_errors` and `F_total_hessian_standard_errors`, given only when mixing passed. These are the jackknife standard errors divided by β.
- `uniform_moments` (only with the callback):
  - `labels`: `("uniform_whitened_R", i)` and `("uniform_whitened_S", i, j)`, i <= j;
  - `n_cells`, `read_positions` and `error_layout_positions`;
  - `cell_sum_means`, the time-averaged Σ_α R'_α,i and Σ_α S'_α,ij;
  - `mode_responses`, Cov(S_a, those columns).
  - They are tracked separately from the mode block. They are not divided by n_cells, and neither a Mandel factor nor central covariance is applied.
- `note`.

**What stays with the root metric adapter:**
- dividing by S (F_mode = F_total/S) and the Gram/dual pairing;
- the Legendre transform, the J Jacobian, the full-background contact and the c1·j̄ slot;
- the metric and EH pairing;
- testing that the declared directions form an invariant block of the complete static source Hessian;
- uniform-block tadpoles and constraints.

The joint block is returned whole. No phase averaging, isotropy, cosine/sine decoupling or symmetrization is applied. A general fixed matrix P is applied post hoc by the caller: P^T g, P^T H P, and the same linear map of the jackknife replicates. This is exact because every coordinate is affine.

## 7. Outputs (all keys)

Every run returns these keys:

- `ok`, `status` (complete, incomplete, unsupported or failed), `stage_reached`, `failures`, `flags`.
- `inputs`: the admitted inputs, plus `mode_directions` (a summary of each direction) and a summary of the callback.
- `coordinate_order`: the supported coordinate keys.
- `direction_status`: each coordinate is "supported" or "unsupported: zero-rate source-opening".
- `tracked_read_labels` (output): the caller's labels, followed by the nine uniform moment labels in mode runs with the callback. `read_kinds` gives the label kind token of each.
- `member_check`: see section 4.
- `modes`: see section 6.
- `estimates`:
  - `beta`, `dlogZ_du`, `d2logZ_du2`, `score_covariance`, `contact_mean`;
  - `F` (None) and `F_note`, `F_u`, `F_uu`;
  - `read_means` and `read_mean_responses`;
  - `per_chain`, `mean_events_per_path`, `max_events_per_path_measured`, `samples_total`.
- `errors`, returned only when mixing "passed":
  - `layout` = [dlogZ (n_u), d2logZ upper triangle row-major, read_means (n_r), read_mean_responses (a-major)];
  - `jackknife_blocks`, `jackknife_standard_errors`, `jackknife_replicates`;
  - `joint_covariance`, formed only when n_y <= the cap;
  - `between_chain_standard_errors`.
- `mixing`: status, stuck chains, primary columns, column status, constant columns, R-hat, integrated autocorrelation times, batch length, thresholds and per-chain batch standard errors.
- `diagnostics`:
  - counters: events, channel_enumerations, sweeps, reverse_signature_fallbacks, restricted_enumerations, restricted_nonmember_records_dropped and palette_verifications;
  - per-chain move counts: rotations, interval, palette and rejection counters, accepted counts, sweeps and measurements;
  - `zero_rate_directions`.
- `conventions`: hamiltonian, pair_sources, moves, positive_gauge, free_energy, legendre, time, affine_coordinates and mode_directions.
- `scope` and `limitations`.

`ok` is True only when three things hold: the status is "complete", every requested direction is supported, and mixing "passed".

A referenced read label that the operator does not have is `failed` at the first read. The v001 diagnostic "labels never observed" no longer exists.

## 8. Errors

- The errors are statistical and assessed against the caller's thresholds: batch jackknife, between-chain spread, Sokal τ and R-hat. They are not a mixing-time bound.
- With mixing failed or unassessable, including runs with fewer than 2 chains, no band, replicates or covariance is returned.
- Caps end the run as `incomplete`. No path is rejected because of a cap.
- A zero-rate source-opening direction is dropped and listed. This includes a lapse direction with v_X ≠ 0 at a primitive whose multiplier is 0.
- Finite-volume, wavelength, matching and normalization errors are separate. They are not estimated here.

## 9. Cost, storage and measurement

**Storage per path.** One state object and key per dwell, plus O(n_u + n_r) numbers per dwell and O(n_u) per event. That is O(events × (state size + n_u + n_r)) (L3).

**Work per generated event of a global move:**
- one call each to `primitive_channels`, `diagonal_terms`, `read_rows` and `canonical_state_key`;
- one `adapted_moment_reads` and one `pair_source_hamiltonian` call when the callback is used;
- the reverse-pairing check.

**Work per palette event.** `palette_channels` replaces the full enumeration, but every new state still gets the global diagonal, read and callback evaluations. Each old interval segment costs one more restricted enumeration.

**Extra work for mode directions.**
- Per new state: O(diagonal records × nonzero weights × lapse directions), plus O(cells × fields) per source direction, plus O(9 × cells) for the uniform sums.
- Per event: O(nonzero weights × lapse directions).

**Measurement.** It uses the stored per-segment rows and costs O(events × (n_u + n_r)) arithmetic. No `read_rows` call is repeated.

**Error analysis.** It stores O(chains × measurements × (n_u² + n_r)) numbers and O(J × n_y) replicates.

No basis, Hilbert-space list or dense operator is built.

## 10. Not implemented

- SPEC section 5 (the HP implicit closure). `implicit_closure` must be None.
- Directed-worm moves, and dependency caches or frontiers for the palette move.
- Translation averaging and absolute F.
- Read-frame and registration derivative contacts.
- Weighted superselection unions.
- An unequal-weight cell pairing.
- Normalized F_mode and every MODE SPEC section 3–5 step.
- EH and vacuum matching, c_star and physical normalization.
- 0410 section 2, the equal-time two-hop pair sector. It is not part of this version.

## 11. LIMITATIONS numbering

The module string `LIMITATIONS` holds items **L1–L23**.

| Item | Topic |
|---|---|
| L1 | actual operator API; `palette_channels` (R1) |
| L2 | two-line positive gauge |
| L3 | storage and global per-event cost |
| L4 | no absolute F |
| L5 | affine coordinates |
| L6 | zero-rate directions, including lapse directions |
| L7 | single conserved-resource component |
| L8 | coarse rows refused in every role: the 0409 no-duplication reason, operator v001 and v002 (R3) |
| L9 | A is linear |
| L10 | interval density |
| L11 | H[N] weighting and partition check |
| L12 | reverse pairing |
| L13 | errors |
| L14 | caps |
| L15 | time coincidences |
| L16 | not implemented |
| L17 | operator exceptions |
| L18 | measurement cadence |
| L19 | palette move |
| L20 | pair sources |
| L21 | mode directions (new) |
| L22 | mode metadata and pairing (new) |
| L23 | uniform first/pair moments (new) |

No physics, value, scale or target was chosen or read.
