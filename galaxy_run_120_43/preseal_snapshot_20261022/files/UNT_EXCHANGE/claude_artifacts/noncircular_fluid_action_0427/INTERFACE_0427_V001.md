# INTERFACE 0427 V001: noncircular displacement action (Claude2, c2v001)

Module: `ddo_noncircular_displacement_action_c2v001.py` (same folder). It is inert: no I/O, nothing runs at import, it uses numpy and the stdlib only, public arguments are keyword-only with no defaults, and every failure returns a fail-closed dict.

Binding inputs (sha256 checked from bytes before implementation):
- Task 0427: `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164`
- Equation spec `DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt`: `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4` (sections 2-7)
- Equation review `NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json`: `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e`
- Context, read as text only: `galaxy_coupled_fourier_hi_prediction_v006.py` `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` and `owned_physical_fourier_metric_quadrature_v004.py` `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` (source Fourier convention only).

## 1. Scope

The module evaluates the matrix-free bulk action of spec section 3, with the source feedback of section 4, for one caller-supplied stationary displacement `xi`. It also evaluates caller boundary rows in a separate function.

It does not do any of the following:
- solve or invert anything
- realize boundaries
- treat resonances (no ridge, no pseudoinverse, no mode deletion)
- fix neutral modes, circulation or annular mass
- construct the base or r0
- apply metric/source-measure corrections
- run a Fourier transform or a kernel solve
- produce a stationary state, corrected velocities or observation rows

## 2. Public functions

```
evaluate_bulk_action(*, grid_shape, R, phi, z, rho0, K0, P0, Omega, gamma, xi,
    partial_R, partial_phi, partial_z, derivative_rule_description,
    base_derivative_mode, base_derivatives, base_axisymmetry_rtol,
    polytrope_consistency_rtol, c_light, unit_system, induced_response,
    lapse_variation_form, angular_forcing_dPhi, base_residual_r0, forcing_partition)

evaluate_boundary_rows(*, bulk_result, boundary_row_callbacks)
```

### Arguments of `evaluate_bulk_action`

All arrays must be real (int, uint or float up to float64; bool, complex and object are rejected), finite, and broadcast-compatible to `grid_shape`. The module copies them to read-only float64 arrays of exactly `grid_shape`.

| argument | meaning / units (SI shown; any caller-consistent system allowed) |
|---|---|
| `grid_shape` | nonempty tuple of positive ints. The grid layout and axis order belong to the caller. |
| `R`, `phi`, `z` | physical cylindrical node coordinates [m, rad, m]. R > 0 everywhere. The module uses only R algebraically; phi and z go to boundary callbacks. |
| `rho0` | base density [kg m^-3], > 0 everywhere. Never clamped. |
| `K0` | base polytropic K [Pa (kg m^-3)^-gamma], > 0 |
| `P0` | base pressure [Pa], > 0. Must satisfy P0 = K0 rho0**gamma within `polytrope_consistency_rtol` (max relative). |
| `Omega` | base angular velocity Omega(R,z) [rad s^-1], any sign. Vertical shear is retained. |
| `gamma` | real scalar > 0 (bool rejected) |
| `xi` | tuple `(xi_R, xi_phi, xi_z)` of physical orthonormal components [m]. xi_phi is a length, not an angle. |
| `partial_R`, `partial_phi`, `partial_z` | caller's consistent linear derivative operators; see section 3 |
| `derivative_rule_description` | nonempty provenance string for the derivative rule |
| `base_derivative_mode` | `'caller_derivative_callbacks'`: the module computes base derivatives only through the three callbacks. `'supplied'`: the caller gives them all. |
| `base_derivatives` | `None` in callbacks mode. In supplied mode, a mapping with exactly the keys `rho0_phi, K0_R, K0_phi, K0_z, P0_R, P0_phi, P0_z, Omega_R, Omega_phi, Omega_z` (d_phi per radian). Mixing the two modes is rejected. |
| `base_axisymmetry_rtol` | >= 0. For each f in {rho0, K0, P0, Omega}, max\|d_phi f\| / max\|f\| must not exceed it. This is the base stationary continuity/entropy precondition, because the spec s3 equations assume an axisymmetric base. |
| `polytrope_consistency_rtol` | >= 0 (see `P0`) |
| `c_light` | > 0 [m s^-1], in the same unit system |
| `unit_system` | nonempty declaration, e.g. `'SI'` |
| `induced_response` | the caller's complete native response; see section 3 |
| `lapse_variation_form` | `'weak_field_delta_n'` (dPhi = c^2 delta_n) or `'exact_ln_N_first_variation'` (dPhi = c^2 delta_N/N0). There is no default and no silent choice. |
| `angular_forcing_dPhi` | the caller's angular forcing potential [m^2 s^-2]: the saved-field potential on this grid minus its m=0 projection |
| `base_residual_r0` | tuple `(r0_R, r0_phi, r0_z)`, the projected-base acceleration residual [m s^-2] in physical components (sign in section 4) |
| `forcing_partition` | declaration mapping; see section 5 |

## 3. Callback signatures

- `partial_R(f)`, `partial_phi(f)`, `partial_z(f)`. The argument is one positional read-only float64 array of exactly `grid_shape`. Each must return a real finite array of exactly `grid_shape`: d/dR, d/dphi (per radian) and d/dz on the caller's grid. They must be linear and mutually consistent. The module never picks a stencil, spectral rule or grid library. They run under the caller's own numpy errstate.
- `induced_response(*, delta_f_n)`. This is called exactly once, and only after every other validation has passed.
  - Input: a read-only array `delta_f_n = -c_light**2 * drho` [J m^-3] on the grid. It is the signed leading mass-source perturbation, and the module checks that the callback did not mutate it.
  - Output: a mapping with at least two keys:
    - `'native_response'`: the complete native 10-field response, not None. The module retains it unmodified, without copying or mutating it, as `'induced_response_full'`.
    - `'lapse_component'`: exactly one of:
      - `{'form': 'weak_field_delta_n', 'delta_n': array}`
      - `{'form': 'exact_ln_N_first_variation', 'delta_N': array, 'N0': array}`, with N0 > 0.
  - Lapse arrays must be real, finite and exactly `grid_shape`. Extra keys, mixed keys, or a form that differs from `lapse_variation_form` are rejected.
  - The callback owns the Fourier transform. The existing convention (read from v004) is source F(k) = ∫ dV exp(-i k·x) f(x), with inverse x(x) = Σ_q w_q exp(+i k_q·x) x̃_q / (2π)^3. The callback also owns the kernel solve, k=0 handling, the reality tolerance and the extraction of n.
- `boundary_row_callbacks[name](*, fields)`. `fields` is a read-only `MappingProxyType` with these entries:
  - read-only arrays: grid, base fields, base derivatives, `xi_R/xi_phi/xi_z`, `drho, dK, dP, cs2, dv_R, dv_phi, dv_z, lagrangian_dP, dPhi_total`
  - the three derivative callbacks
  - `grid_shape`, `unit_system`, `derivative_rule_description`

  Each callback must return a real finite array with ndim >= 1 and size >= 1.

## 4. Equations to code (line numbers in the c2v001 file)

| spec s3/s4 | code |
|---|---|
| cs2 = gamma P0/rho0 | L346 |
| drho = -div(rho0 xi), cylindrical: (1/R) d_R(R rho0 xi_R) + (1/R) d_phi(rho0 xi_phi) + d_z(rho0 xi_z) | L347-351 (conservative form, 1/R applied after d_R) |
| dK = -xi·grad K0 = -(xi_R K0_R + xi_phi K0_phi/R + xi_z K0_z) | L352 |
| dP = cs2 drho + rho0^gamma dK | L353 |
| dv_R = Omega d_phi xi_R; dv_z = Omega d_phi xi_z; dv_phi = Omega d_phi xi_phi - R(Omega_R xi_R + Omega_z xi_z) | L357-359 |
| Lagrangian dP + xi·grad P0 (s5 free-surface quantity; a field only, never imposed) | L360 |
| df_n = -c^2 drho, one response call | L367, L373 |
| dPhi_induced = c^2 delta_n (weak) or c^2 delta_N/N0 (exact) | L404 / L414 |
| dPhi_total = angular forcing + induced, each once | L416 |
| radial residual: Omega d_phi dv_R - 2 Omega dv_phi + d_R dPhi + d_R dP/rho0 - drho P0_R/rho0^2 + r0_R | L424-427; order L436-441; summed L442-450 |
| angular residual: Omega d_phi dv_phi + (2 Omega + R Omega_R) dv_R + R Omega_z dv_z + d_phi dPhi/R + d_phi dP/(rho0 R) + r0_phi | L428-432 |
| vertical residual: Omega d_phi dv_z + d_z dPhi + d_z dP/rho0 - drho P0_z/rho0^2 + r0_z | L433-435 |
| base continuity/entropy residuals (d_phi(rho0 Omega), Omega K0_phi) | L342-343 |
| diagnostics: div(rho0 dv + drho v0) and v0·grad dK + dv·grad K0 | L453-455 |

Each residual is the spec's LHS minus its RHS, so a solution gives zero. With this sign, r0 must be the projected-base acceleration residual (v0·∇)v0 + ∇Φ0 + ∇P0/ρ0. For an axisymmetric base that means r0_R = P0_R/rho0 + Phi0_R - R Omega^2, r0_z = P0_z/rho0 + Phi0_z, and r0_phi = 0 unless supplied.

All derivatives of dP, dPhi_total and dv go through the caller callbacks. The analytic gradient that the response may carry is retained in `induced_response_full` but is not used.

## 5. Forcing partition (fixed for 0427)

`forcing_partition` must have exactly these keys:
- `convention == 'r0=projected_base_residual;dPhi_total=angular_forcing+induced_feedback'`
- `r0_content == 'projected_base_residual'`
- `r0_includes_induced_feedback is False`
- `angular_forcing_excludes_m0_projection is True`
- `angular_forcing_includes_induced_feedback is False`
- `r0_provenance`: nonempty string
- `angular_forcing_provenance`: nonempty string

The flags must be real bools. The following are rejected:
- missing or extra keys
- the spec's alternative partition (r0 = full saved-field force with induced-only dPhi), as "not the fixed convention"
- `r0_content == 'full_saved_field_angular_force'`, as DOUBLE COUNT, because angular forcing is always added
- any declaration that puts induced feedback in r0 or in the angular forcing (DOUBLE COUNT)
- angular forcing that includes the m=0 projection (DOUBLE COUNT)

The module cannot detect a double count inside the data, so these rules enforce the caller's declaration.

## 6. Return keys

On failure the result is exactly `{'ok': False, 'module', 'stage', 'reason'}`. The stage is one of `input_validation | forcing_partition | base_checks | derivative_callback | perturbation | source_feedback | euler_residual | internal`. No partial fields are returned.

On success the result has `'ok': True, 'module', 'stage', 'grid_shape'` plus:
- `perturbations`: `drho, dK, dP, cs2, dv_R, dv_phi, dv_z, lagrangian_dP`
- `source_feedback`: `delta_f_n`, `response_call_count` (=1), `lapse_variation_form`, `lapse_used`, `dPhi_forcing`, `dPhi_induced`, `dPhi_total`
- `induced_response_full`: the callback output object, unmodified
- `euler_residual`: `{'R','phi','z'}`
- `euler_terms`: per-component term arrays, summed in a fixed order
- `base_checks`: `polytrope_max_relative_mismatch`, `axisymmetry_max_ratio`, `base_continuity_residual`, `base_entropy_residual`, `base_derivative_mode`, `base_derivatives`
- `identity_diagnostics`: `linearized_continuity`, `linearized_entropy`, `scope`. These are not gated. They are zero analytically; a nonzero value measures base residual or non-commuting derivative rules.
- `forcing_partition`, `conventions`, `not_done`
- `boundary_rows`: the string `NOT_EVALUATED...`
- `boundary_state`: a read-only mapping for `evaluate_boundary_rows`

All arrays are read-only float64.

`evaluate_boundary_rows` returns `{'ok': True, 'boundary_rows': {name: array}, 'call_counts', 'scope'}`. Rows are unweighted and are never added to `euler_residual`.

The action is affine: L[xi] = action(xi) - action(0) when the callbacks and the response are linear. action(0) is grad(angular forcing) + r0.

## 7. Missing interface facts Root must supply

1. **Response adapter.** This is the actual `induced_response`. It must:
   - transform grid-sampled `delta_f_n` with the existing v004 convention. That needs the physical volume quadrature on this grid (R dR dphi dz weights), the k-node set and weights, the finite-domain/tail scope, and k=0 handling, which v004 refuses and assigns to the boundary/normal solution.
   - solve through the same complete kernel at the declared fixed coefficient/state point
   - evaluate on the grid nodes (Cartesian↔cylindrical mapping)
   - check reality with its own tolerance
   - extract the lapse field, which is n at index 0 of (n, C_Mandel6, mu3) in v004 ordering. Root must confirm this, and confirm which source column.
2. **Other nine source components.** The spec keeps them "as admitted in that branch". Root must state whether they are unperturbed under displacement in the leading mass-source approximation, or supply them inside the adapter.
3. **Lapse relation.** Root must declare whether N = 1 + n, which makes the weak form exact to first order only when N0 ≈ 1, or provide delta_N and N0 for the exact c^2 deltaN/N0 option.
4. **Equilibrated axisymmetric base.** This means rho0, K0, P0 and Omega(R,z) with gamma, their provenance, Phi0, and r0 in the section 4 sign. The saved circular trial and N-only columns do not supply it (spec s2/s7).
5. **Angular forcing array.** The saved-field Phi on this grid minus its m=0 projection, from prepared-field evaluation, with no resampling or rerun.
6. **Grid and derivative rules.** Consistent operators, including near the radial and free-surface boundaries, plus periodic azimuth, all declared by Root. The gradient of dPhi uses these callbacks, not response-supplied analytic gradients. Using the latter would be a versioned interface change.
7. **Boundary rows.** Root must supply:
   - xi·n = 0 on the actual radial source domain
   - the free surface Lagrangian dP + xi·grad P0 = 0 (the `lagrangian_dP` field is provided), with the surface-location representation
   - reflection only if the source and metric support it
   - circulation and neutral-mode data, plus the optional annular-mass constraint
8. **Metric-dependent source-measure corrections** and the retained-order assessment (spec s4/s6), plus full residual re-evaluation at any resulting state.
9. **Tolerances** for `base_axisymmetry_rtol` and `polytrope_consistency_rtol`, chosen by Root. No default is supplied.

## 8. Fixtures run (NONPHYSICAL, algebraic only)

The fixtures live in the scratchpad (`test_0427_algebraic_fixtures.py`). They were run with `python3 -I -B` (codex runtime, numpy 2.3.5, Python 3.12.14). They use synthetic polynomial/trig fields on a 21×16×17 grid, with Chebyshev R and z and FFT phi callbacks that are exact for the fixture. The response is a stub. No project data, run, or target velocities were used.

Result: 93/93 checks passed. The two independent references:
- **Engine A**, an exact polynomial/trig symbolic engine (gamma = 2, nonlocal stub, weak form). Every output agrees within 2.3e-11 relative, and the continuity and entropy identities are at 3e-13 and 9e-16.
- **Engine B**, a Cartesian coordinate-free reference: complex-step plus central differences, Lie bracket, and (v0·∇)dv + (dv·∇)v0 + ∇dΦ + ∇dP/ρ0 − δρ∇P0/ρ0² (gamma = 5/3, exact lnN form). All fields and the three residuals agree within 9.7e-11.

The suite also covers:
- linearity
- the xi=0 affine part, which is exact
- the response contract: one call, a bitwise source, a read-only input, mutation detection, and form/key/shape/dtype/N0 rejections
- forcing-partition rejections
- 32 validation rejections, none of which calls a callback before static validation
- boundary-row separation
- errstate preservation
- an import audit with no open/os/socket events
- keyword-only signatures

Twelve planted sign/factor mutants were all detected, each of them by engine B.
