# 0407 conventions: owned collective worldline static response, v001

Module: `owned_collective_worldline_static_response_v001.py`, in this directory. Static author text. It has never been imported or run. It uses numpy and the standard library only.

## API
One public function. Every argument is keyword-only and required, with no defaults:

`owned_collective_worldline_static_response(*, operator_api, graph0, model, registration, initial_paths, beta, lapse_factors, source_coefficients, volume_gradient_coefficients, volume_multiplier, gauge_phases, derivative_coordinates, tracked_read_labels, extra_diagonal_reads, chain_generators, move_parameters, caps, burn_in_sweeps, measurement_sweeps, error_parameters, numerical_tolerances, implicit_closure)`

The function's docstring gives the shape and range of each input. The module chooses no value.
- The caller declares beta, lapse factors, sources, A and lambda, and the common phases of the member.
- The caller also sets the move-selection probabilities and length components, the caps, the sweep counts, the batch, R-hat and autocorrelation thresholds, and the tolerances.
- Each chain has its own `numpy.random.Generator`.
- `implicit_closure` must be `None`. Anything else returns `unsupported`. The SPEC section 5 contract is kept for later.

## Assumed operator API (to be reconciled with owned_parent_operator_v001.py)
`operator_api` is passed at run time. The module never imports it. It must expose:
- `validate_owned_model(*, graph0, model, registration)`
- `canonical_state_key(*, context, state)`
- `primitive_channels(*, context, state)`. Each record has: `owner_id`, `kind` ∈ {flip, hop, bind, admit, admit_rev, birth, birth_rev}, `target_state`, `amplitude`, `queried_support`, `changed_support`, `weights`.
- `diagonal_terms(*, context, state)`. Each record has `value` and `weights`.
- `read_rows(*, context, state)`. Each record has `label`, `value` and an optional `kind`.

Records may be mappings or objects. If a name or field is missing, the result is `failed`.

## Outputs
The result dict has:
- **Status fields:** `ok`, `status` ∈ {complete, incomplete, unsupported, failed}, `stage_reached`, `failures`, `flags`.
- **Labels and directions:** `coordinate_order`, `direction_status`, `tracked_read_labels`, `read_kinds`.
- **`estimates`:**
  - `dlogZ_du` = ⟨S⟩ and `d2logZ_du2` = Cov(S,S) + ⟨T⟩. `score_covariance` and `contact_mean` are also returned separately.
  - `F_u` = −⟨S⟩/β and `F_uu` = −(Cov + ⟨T⟩)/β. `F` itself is `None`.
  - `read_means` = ⟨(1/β)∫O⟩ and `read_mean_responses` = Cov(S_a, Ō_r).
  - Per-chain values and counts of events per path.
- **`errors`:** returned only when mixing passed. It holds jackknife standard errors over batches, the leave-one-batch-out replicates (the joint covariance), an explicit joint covariance when its dimension is at or below the caller's limit, and between-chain standard errors.
- **`mixing`:** R-hat, Sokal integrated autocorrelation time per chain, the status of each column, constant columns, and stuck chains.
- **`diagnostics`:** counters, acceptance and rejection counts for each chain, labels never observed, and zero-rate directions.
- **Also:** `conventions`, `scope`, `limitations`.

`ok` is True only when all three hold: the status is complete, every requested direction is supported, and mixing passed.

## Signs and Legendre
- H_c = H[N] − Σ_a j_a O_a − λA.
- H[N] = H + Σ_α n_α E_α, with n = N − 1. Each primitive's multiplier is 1 + Σ_α n_α w̄_αX. It is applied before aggregation.
- Z = Tr e^{−βH_c} and F = −log Z/β.
- For a lapse coordinate, F_{n_α} = ⟨E_α⟩. This is the full coarse energy, diagonal plus off-diagonal. For a read source, F_j = −⟨O⟩.
- The thermal Legendre functional F + j·Q has QQ Hessian **+χ⁻¹**, with:
  - F_jj = −χ_OO^iso, F_nn = −χ_EE^iso, F_nj = +χ_EO^iso
  - χ^iso_AB = ∫₀^β ⟨δA(τ)δB(0)⟩
- Real-time action signs are not imported.
- Derivative coordinates are affine: n_α (equivalently N_α), j_label and λ. Their second-source contacts are exactly zero. For g00 or other nonlinear coordinates, the caller applies the chain rule using both returned derivatives.
- Positive gauge: G = (−1)^{Σq} (−e^{i arg κ})^{N_S} (−e^{i arg ε})^{N}, from the assembly at lines 300–327.
  - Every gauged off-diagonal element must equal −|h|. Otherwise the result is `unsupported`.
  - The rate is W = |h| × multiplier ≥ 0.

## Meaning
- The result is the static isothermal native functional at fixed β, for the quasi-static maximum-entropy closure.
- It is not fixed-preparation retarded response. For example, χ_HH^iso = β Var H, while the retarded value is 0.
- It is not the complete metric propagator.
- It does not include EH/vacuum matching, c_star, scales, normalization, physical inputs or fits.
- Imaginary time τ is in inverse energy. Neither τ nor the Monte Carlo sweeps are physical or native time.

## Errors
- The errors are statistical estimates, assessed against the caller's thresholds. They are not a mixing-time bound.
- If mixing failed or could not be assessed, no band, replicates or covariance are returned. This includes runs with fewer than 2 chains.
- Caps end the run as `incomplete` and return only diagnostics. No path is ever rejected because of a cap.
- A zero-rate source-opening direction is marked `unsupported` and dropped. No division by zero is done.
- Finite-volume, wavelength, matching and normalization errors are separate. They are not estimated here.

## Cost
- **Storage per path:** one state object, key and O(n_u) numbers per dwell, plus O(n_u) per event. That is O(events × state size) through this API. LIMITATIONS L3 explains why this differs from the SPEC's O(V0 + events).
- **Work per generated event:** one call each to primitive_channels, diagonal_terms, read_rows and canonical_state_key, plus the reverse-pairing check.
- **Work per measurement:** one read_rows call for each distinct dwell state.
- No basis, Hilbert-space list or dense operator is built.

## Not implemented
- The HP implicit volume closure and cosmic preparation (SPEC section 5).
- Directed-worm or other efficiency moves.
- Translation averaging.
- Absolute F.
- Read-frame and registration derivative contacts.
- Combining weighted superselection components.
- EH matching, c_star and physical normalization.

The full list is in the module string `LIMITATIONS`, items L1–L18.
