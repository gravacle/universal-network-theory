# INTERFACE 0427 V002: noncircular displacement action (Claude2, c2v002)

Module: `ddo_noncircular_displacement_action_c2v002.py` (same folder). It is inert: no I/O, nothing runs at import, it uses numpy and the stdlib only, public arguments are keyword-only with no defaults, and every failure returns a fail-closed dict.

This note supersedes `INTERFACE_0427_V001.md` (`1c34edf3fce32f7705382d9f1b802ec2d53ad6b097c57b4fad4bff64af4b60eb`), and c2v002 supersedes `ddo_noncircular_displacement_action_c2v001.py` (`6b4f2cc6ee0e0c1a4408e555004b510d2d11058bc6f3e9cc82f6ce697ef9e482`). Both earlier files are preserved unchanged. V002 changes only what resolves the following, mapped in `FIX_DELTA_0427_V002.md`:
- **B1** (interface review): lower-rank arrays were silently broadcast along the wrong axis. Fixed in code; §2 and §6.
- **B2** (interface review): a missing fact about where the free surface lies and the surface-mass source. INTERFACE only, no code change; §7 facts 7 and 10.
- **0428-F** (Codex 0428): non-finite identity diagnostics were returned with ok=True. Fixed in code; §3 and §6.
- **0428-B** (Codex 0428): base wording. The base is not a force-balance gate, r0 may be nonzero, and Omega is used as given. Code wording plus §2, §4 and §7 fact 4.

Binding inputs (sha256 checked from bytes before the fix):
- Task 0427: `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164`
- Codex 0428 `0428_2026-10-16_0427_finite_diagnostics_and_base_clarification.md`: `e94cc68d2ebde91ae839f7a960e964ef909474358993028d860088164266da60`
- Equation spec `DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt`: `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4` (sections 2-7)
- Equation review `NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json`: `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e`
- Context, read as text only: `galaxy_coupled_fourier_hi_prediction_v006.py` `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` and `owned_physical_fourier_metric_quadrature_v004.py` `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` (source Fourier convention only)
- Distinct reviews of c2v001: `REVIEW_0427_INTERFACE_V001.md` `1df58f47d90c457f0ad952489aa3b6118e8c6588e9abf4e5f3358edfc6496f42` and `REVIEW_0427_EQUATIONS_V001.md` `95eda7c805b6068d7dee442bddfe7586a4f8bcf625c40976d324617db832d21a`

## 1. Scope

The module evaluates the matrix-free bulk action of spec section 3, with the source feedback of section 4, for one caller-supplied stationary displacement `xi`. It also evaluates caller boundary rows in a separate function.

It does not do any of the following:
- solve or invert anything
- realize boundaries
- treat resonances (no ridge, no pseudoinverse, no mode deletion)
- fix neutral modes, circulation or annular mass
- construct the base or r0, or test the base's radial/vertical force balance
- apply metric/source-measure corrections
- run a Fourier transform or a kernel solve
- supply the surface-displacement source at the rho0→0 surface (§7 fact 10)
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

The signatures are unchanged from c2v001.

### Arguments of `evaluate_bulk_action`

All arrays must be real (int, uint or float up to float64; bool, complex and object are rejected) and finite. The module copies them to read-only float64 arrays of exactly `grid_shape`.

**Rank rule (V002, B1).** Every array argument must be one of these two:
- **0-d:** a scalar, constant on the grid.
- **Full rank:** exactly `len(grid_shape)` axes, each of length 1 or equal to that grid axis.

This covers `R`, `phi`, `z`, `rho0`, `K0`, `P0`, `Omega`, each `xi` and `base_residual_r0` component, `angular_forcing_dPhi`, and each supplied base derivative.

Singleton axes must be explicit. On an (N_R, N_phi, N_z) grid:
- a radial profile is passed as `f[:, None, None]`
- a vertical profile is passed as `f[None, None, :]`
- a 1-D array is never accepted

Any other rank is rejected at `input_validation`. The reason states the rank, the shape and this rule, and no callback is called first. The rule exists because numpy aligns shapes from the right. Without it, a 1-D radial profile on a grid with N_R == N_z, or with length equal to N_z, would be applied along z, and the axisymmetry and polytrope gates cannot see that.

The original shape of every accepted array is recorded in the result under `input_shapes`.

| argument | meaning / units (SI shown; any caller-consistent system allowed) |
|---|---|
| `grid_shape` | nonempty tuple of positive ints. The grid layout and axis order belong to the caller. |
| `R`, `phi`, `z` | physical cylindrical node coordinates [m, rad, m]. R > 0 everywhere. The module uses only R algebraically; phi and z go to boundary callbacks. |
| `rho0` | base density [kg m^-3], > 0 everywhere. Never clamped. This excludes the rho0→0 surface from the grid; see §7 fact 10. |
| `K0` | base polytropic K [Pa (kg m^-3)^-gamma], > 0 |
| `P0` | base pressure [Pa], > 0. Must satisfy P0 = K0 rho0**gamma within `polytrope_consistency_rtol` (max relative). |
| `Omega` | the caller's real base angular velocity Omega(R,z) [rad s^-1], **used exactly as given**. Any sign is allowed and vertical shear is retained. See the note after this table. |
| `gamma` | real scalar > 0 (bool rejected) |
| `xi` | tuple `(xi_R, xi_phi, xi_z)` of physical orthonormal components [m]. xi_phi is a length, not an angle. |
| `partial_R`, `partial_phi`, `partial_z` | caller's consistent linear derivative operators; see section 3 |
| `derivative_rule_description` | nonempty provenance string for the derivative rule |
| `base_derivative_mode` | `'caller_derivative_callbacks'`: the module computes base derivatives only through the three callbacks. `'supplied'`: the caller gives them all. |
| `base_derivatives` | `None` in callbacks mode. In supplied mode, a mapping with exactly the keys `rho0_phi, K0_R, K0_phi, K0_z, P0_R, P0_phi, P0_z, Omega_R, Omega_phi, Omega_z` (d_phi per radian). Mixing the two modes is rejected. |
| `base_axisymmetry_rtol` | >= 0. For each f in {rho0, K0, P0, Omega}, max\|d_phi f\| / max\|f\| must not exceed it. This checks the base as the stationary leading continuity/entropy reference: an axisymmetric rho0 and K0 carried by v0 = R Omega e_phi conserve mass and entropy at leading order. **It is not an equilibrium or force-balance gate.** With the polytrope relation, it is the only base gate. |
| `polytrope_consistency_rtol` | >= 0 (see `P0`) |
| `c_light` | > 0 [m s^-1], in the same unit system |
| `unit_system` | nonempty declaration, e.g. `'SI'` |
| `induced_response` | the caller's complete native response; see section 3 |
| `lapse_variation_form` | `'weak_field_delta_n'` (dPhi = c^2 delta_n) or `'exact_ln_N_first_variation'` (dPhi = c^2 delta_N/N0). There is no default and no silent choice. |
| `angular_forcing_dPhi` | the caller's angular forcing potential [m^2 s^-2]: the saved-field potential on this grid minus its m=0 projection |
| `base_residual_r0` | tuple `(r0_R, r0_phi, r0_z)`: the projected-base Euler residual [m s^-2] in physical components, sign in section 4. **It may be nonzero**, as the reviewed spec s3 explicitly allows. It is never tested and never required to vanish. It enters each residual component exactly once. |
| `forcing_partition` | declaration mapping; see section 5 |

**What the module does with Omega (V002, 0428-B).** It takes the caller's real Omega as given. It never derives Omega from a force balance, never forms or clips Omega**2, never drops radii, never enforces an inward force and never changes the source. Some reference nodes have no real circular balance, because the radial pressure gradient exceeds an inward lapse force. At those nodes the caller's chosen real Omega is still used, and the full radial/vertical Euler imbalance stays in r0. The success result carries this statement in `not_done`.

## 3. Callback signatures

- **Derivatives:** `partial_R(f)`, `partial_phi(f)`, `partial_z(f)`.
  - The argument is one positional read-only float64 array of exactly `grid_shape`.
  - Each must return a real finite array of exactly `grid_shape`: d/dR, d/dphi (per radian) and d/dz on the caller's grid.
  - They must be linear and mutually consistent. The module never picks a stencil, spectral rule or grid library.
  - They run under the caller's own numpy errstate.
- **Response:** `induced_response(*, delta_f_n)`. It is called exactly once, and only after every other validation has passed. It runs under the caller's own numpy errstate.
  - Input: a read-only array `delta_f_n = -c_light**2 * drho` [J m^-3] on the grid. It is the signed leading mass-source perturbation of the bulk only (see §7 fact 10). The module checks that the callback did not mutate it.
  - Output: a mapping with at least two keys:
    - `'native_response'`: the complete native 10-field response, not None. The module retains the whole callback output mapping unmodified, by identity, as `'induced_response_full'`.
    - `'lapse_component'`: exactly one of:
      - `{'form': 'weak_field_delta_n', 'delta_n': array}`
      - `{'form': 'exact_ln_N_first_variation', 'delta_N': array, 'N0': array}`, with N0 > 0.
  - Lapse arrays must be real, finite and exactly `grid_shape`. Extra keys, mixed keys, or a form that differs from `lapse_variation_form` are rejected.
  - The callback owns the Fourier transform. The existing convention (read from v004) is source F(k) = ∫ dV exp(-i k·x) f(x), with inverse x(x) = Σ_q w_q exp(+i k_q·x) x̃_q / (2π)^3. The callback also owns the kernel solve, k=0 handling, the reality tolerance and the extraction of n.
- **Boundary rows:** `boundary_row_callbacks[name](*, fields)`. `fields` is a read-only `MappingProxyType` with these entries:
  - read-only arrays: grid, base fields, base derivatives, `xi_R/xi_phi/xi_z`, `drho, dK, dP, cs2, dv_R, dv_phi, dv_z, lagrangian_dP, dPhi_total`
  - the three derivative callbacks
  - `grid_shape`, `unit_system`, `derivative_rule_description`

  Each callback must return a real finite array with ndim >= 1 and size >= 1.

**Floating point (V002, 0428-F).** The module's own arithmetic runs under `numpy.errstate(divide='raise', over='raise', invalid='raise', under='ignore')`. Underflow is ignored because it can only give finite values.
- Any division by zero, overflow or invalid operation in module arithmetic fails closed with stage `floating_point`. The reason names the phase: `input_validation`, `base_checks`, `perturbation`, `source_feedback`, `euler_residual`, `identity_diagnostics` or `output_validation`.
- This also catches an intermediate overflow that a later operation would turn into a finite but wrong value. One example is `rho0**2` overflowing, so that `drho P0_R / rho0**2` silently becomes 0.
- The caller's errstate is restored on return. The callbacks run under it.

## 4. Equations to code (line numbers in the c2v002 file)

The equations and their code are unchanged from c2v001; they are shifted by +58 lines.

| spec s3/s4 | code |
|---|---|
| cs2 = gamma P0/rho0 | L404 |
| drho = -div(rho0 xi), cylindrical: (1/R) d_R(R rho0 xi_R) + (1/R) d_phi(rho0 xi_phi) + d_z(rho0 xi_z) | L405-409 (conservative form, 1/R applied after d_R) |
| dK = -xi·grad K0 = -(xi_R K0_R + xi_phi K0_phi/R + xi_z K0_z) | L410 |
| dP = cs2 drho + rho0^gamma dK | L411 |
| dv_R = Omega d_phi xi_R; dv_z = Omega d_phi xi_z; dv_phi = Omega d_phi xi_phi - R(Omega_R xi_R + Omega_z xi_z) | L415-417 |
| Lagrangian dP + xi·grad P0 (s5 free-surface quantity; a field only, never imposed) | L418 |
| df_n = -c^2 drho, one response call | L426, L432 |
| dPhi_induced = c^2 delta_n (weak) or c^2 delta_N/N0 (exact) | L463 / L473 |
| dPhi_total = angular forcing + induced, each once | L475 |
| radial residual: Omega d_phi dv_R - 2 Omega dv_phi + d_R dPhi + d_R dP/rho0 - drho P0_R/rho0^2 + r0_R | L484-487; order L496-501; summed L502-510 |
| angular residual: Omega d_phi dv_phi + (2 Omega + R Omega_R) dv_R + R Omega_z dv_z + d_phi dPhi/R + d_phi dP/(rho0 R) + r0_phi | L488-492 |
| vertical residual: Omega d_phi dv_z + d_z dPhi + d_z dP/rho0 - drho P0_z/rho0^2 + r0_z | L493-495 |
| base continuity/entropy residuals (d_phi(rho0 Omega), Omega K0_phi) | L399-400 |
| diagnostics: div(rho0 dv + drho v0) and v0·grad dK + dv·grad K0 | L515-517 |

These lines are new in V002:

| new in V002 | code |
|---|---|
| module errstate constant (raise divide/over/invalid; ignore under) | L87 |
| rank rule; recording of input shapes | L137-143; L152 |
| finite sweep of module-owned outputs | helper L222-236; applied L576-583 |
| errstate applied; FloatingPointError fails closed | L256, L273-276; boundary rows L596, L631-632 |
| `not_done` line: no force-balance gate, Omega used as given | L94-95 |

**Residual sign.** Each residual is the spec's LHS minus its RHS, so a solution gives zero. With this sign, r0 is the projected-base acceleration residual (v0·∇)v0 + ∇Φ0 + ∇P0/ρ0. For an axisymmetric base:
- r0_R = P0_R/rho0 + Phi0_R - R Omega^2
- r0_z = P0_z/rho0 + Phi0_z
- r0_phi = 0 unless supplied

**r0 is in general nonzero.** The projected base need not be in radial/vertical force balance. Its full radial/vertical Euler residual stays in r0, and the module neither tests it nor removes it.

All derivatives of dP, dPhi_total and dv go through the caller callbacks. The analytic gradient that the response may carry is retained in `induced_response_full` but is not used.

## 5. Forcing partition (fixed for 0427; unchanged)

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

**On failure** the result is exactly `{'ok': False, 'module', 'stage', 'reason'}`. No partial fields are returned. The stage is one of:
- `input_validation`
- `forcing_partition`
- `base_checks`
- `derivative_callback`
- `perturbation`
- `source_feedback`
- `euler_residual`
- `floating_point` (new in V002)
- `output_validation` (new in V002)
- `internal`

**On success** the result has `'ok': True, 'module', 'stage', 'grid_shape'` plus:
- `input_shapes` (new in V002): a mapping from argument name to the original shape tuple of each accepted array. `()` means 0-d. Keys are the argument names, with components as `xi[R]` and `base_residual_r0[z]`, and supplied derivatives as `base_derivatives[K0_R]`.
- `perturbations`: `drho, dK, dP, cs2, dv_R, dv_phi, dv_z, lagrangian_dP`
- `source_feedback`: `delta_f_n`, `response_call_count` (=1), `lapse_variation_form`, `lapse_used`, `dPhi_forcing`, `dPhi_induced`, `dPhi_total`
- `induced_response_full`: the callback output object, unmodified
- `euler_residual`: `{'R','phi','z'}`, all three components
- `euler_terms`: per-component term arrays, summed in a fixed order
- `base_checks`: `polytrope_max_relative_mismatch`, `axisymmetry_max_ratio`, `base_continuity_residual`, `base_entropy_residual`, `base_derivative_mode`, `base_derivatives`
- `identity_diagnostics`: `linearized_continuity`, `linearized_entropy`, `scope`. Their values are not gated. They are zero analytically; a nonzero value measures base residual or non-commuting derivative rules.
- `forcing_partition`, `conventions`, `not_done`
- `boundary_rows`: the string `NOT_EVALUATED...`
- `boundary_state`: a read-only mapping for `evaluate_boundary_rows`

All arrays are read-only float64.

**Finite guarantee (V002, 0428-F).** `ok` is True only if every module-owned returned array and float is finite. That covers every key above except `induced_response_full`, and it includes both identity diagnostics, the base residuals, all Euler terms, `lapse_used` and every array in `boundary_state`.
- A non-finite value fails the whole call closed with stage `output_validation` or `floating_point`.
- No "unavailable diagnostic" status exists. Whenever ok=True, every returned residual and diagnostic is a finite array, and no non-finite value is ever returned as one.
- `induced_response_full` is the caller's object, retained by identity. It is not a module residual or diagnostic and is not traversed. The lapse arrays the module actually uses are validated as finite, and their read-only copies are returned under `source_feedback['lapse_used']`.

**Boundary rows.** `evaluate_boundary_rows` returns `{'ok': True, 'boundary_rows': {name: array}, 'call_counts', 'scope'}`. Rows are unweighted and are never added to `euler_residual`. They run under the same module errstate (stage `floating_point` on a floating-point error) and must be finite.

**The action is affine.** L[xi] = action(xi) - action(0) when the callbacks and the response are linear. action(0) is grad(angular forcing) + r0.

## 7. Missing interface facts Root must supply

1. **Response adapter.** This is the actual `induced_response`. It must:
   - transform grid-sampled `delta_f_n` with the existing v004 convention. That needs the physical volume quadrature on this grid (R dR dphi dz weights), the k-node set and weights, the finite-domain/tail scope, and k=0 handling, which v004 refuses and assigns to the boundary/normal solution. See also fact 10.
   - solve through the same complete kernel at the declared fixed coefficient/state point
   - evaluate on the grid nodes (Cartesian↔cylindrical mapping)
   - check reality with its own tolerance
   - extract the lapse field, which is n at index 0 of (n, C_Mandel6, mu3) in v004 ordering. Root must confirm this, and confirm which source column.
2. **Other nine source components.** The spec keeps them "as admitted in that branch". Root must state whether they are unperturbed under displacement in the leading mass-source approximation, or supply them inside the adapter.
3. **Lapse relation.** Root must declare whether N = 1 + n, which makes the weak form exact to first order only when N0 ≈ 1, or provide delta_N and N0 for the exact c^2 deltaN/N0 option.
4. **Axisymmetric reference base (V002 wording, 0428-B).**
   - **What Root supplies:**
     - rho0, K0, P0 (polytropic, gamma) and the caller's real Omega(R,z), with provenance and Phi0
     - r0 = the projected-base Euler residual in the §4 sign. **It may be nonzero.** The reviewed spec s3 allows a nonzero base acceleration residual "not already included in dPhi forcing".
   - **What the module requires:** only axisymmetry within `base_axisymmetry_rtol` and the polytrope relation within `polytrope_consistency_rtol`. Axisymmetric density and entropy with a real Omega provide the stationary leading continuity/entropy reference.
   - **What the module does not require:**
     - radial/vertical force balance
     - r0 = 0
     - a positive Omega**2
     - a particular source

     The full radial/vertical Euler residual remains in r0.
   - The saved circular trial and N-only columns are not, by themselves, this reference: spec s2/s7 say the base must be independently constructed and its residual evaluated before use. Supplying an arbitrary reference with its residual in r0 yields an evaluable action, not a stationary state. No final stationary-state claim follows.
5. **Angular forcing array.** The saved-field Phi on this grid minus its m=0 projection, from prepared-field evaluation, with no resampling or rerun.
6. **Grid and derivative rules.** Consistent operators, including near the radial and free-surface boundaries, plus periodic azimuth, all declared by Root. The gradient of dPhi uses these callbacks, not response-supplied analytic gradients. Using the latter would be a versioned interface change. Every array argument is passed 0-d or at full rank with explicit singleton axes (§2).
7. **Boundary rows.** Root must supply:
   - xi·n = 0 on the actual radial source domain
   - the free surface Lagrangian dP + xi·grad P0 = 0 (the `lagrangian_dP` field is provided), with the surface-location representation. This row is the spec s5 free-surface condition **only at the actual rho0→0 surface**. At a grid face where rho0 > 0 it is not the spec condition (see fact 10).
   - reflection only if the source and metric support it
   - circulation and neutral-mode data, plus the optional annular-mass constraint
8. **Metric-dependent source-measure corrections** and the retained-order assessment (spec s4/s6), plus full residual re-evaluation at any resulting state.
9. **Tolerances** for `base_axisymmetry_rtol` and `polytrope_consistency_rtol`, chosen by Root. No default is supplied.
10. **Free-surface position and the surface-mass source (V002, B2).**
    - **Why the bulk source is not mass-conserving at the faces.** The module requires rho0 > 0 and P0 > 0 at every node, so the grid can never contain the zero-density polytropic surface that spec s5 relies on ("no spurious surface-mass delta"). At any grid face where rho0 > 0 and xi·n ≠ 0 (typically the top and bottom faces), the bulk `drho = -div(rho0 xi)` omits the mass carried across that face. Its volume integral is ∫ drho dV = −∮ rho0 xi·n dA, not zero. So `delta_f_n` carries a spurious net mass: k→0 content, which v004 refuses.
    - **What Root must state:** where the physical rho0→0 surface lies relative to the grid faces.
    - **Then Root must do one of the following:**
      - (a) supply the boundary-layer surface-displacement source contribution inside the response adapter, consistent with v004's k=0/boundary-normal assignment
      - (b) give the retained-order assessment showing it is negligible
    - **What the module does:** it is unchanged and supplies neither. It has no quadrature and does not choose one.
    - **Illustration:** fixture B2 in §8 confirms the identity algebraically.

## 8. Fixtures run (NONPHYSICAL, algebraic only)

The fixtures were run against the published c2v002 bytes (`056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925`).
- **Runtime:** `python3 -I -B` (codex runtime, Python 3.12.14, numpy 2.3.5)
- **Location:** scratchpad `r0427-fix/`
- **Data:** synthetic fields only. No project data, run, or target velocities were used.

| run | result |
|---|---|
| V001 author suite, unchanged file (`89e20cb76a529a920d69ea69b736f9b4fff72e12024dd32fb15eb01d8d67d8b6`), on c2v002 | 93/93 |
| V002 suite `test_0427_algebraic_fixtures_v002.py` (`3cec22e4ed834d2910b3067c36641d4a8aafcba287268ffbc2c2813887ec0ab1`), on c2v002 | 127/127 (93 unchanged + 34 delta checks) |
| same V002 suite on c2v001 (contrast) | 107/127. The 20 failing checks are exactly the delta defects. |
| interface reviewer suite, unmodified (`144b3638a53e9f659436f1ee855dadef85fd828af762fac1f83c6c5adba00279`), on c2v002 | 136/138. The B1 PROBE now passes. See the note below the table for the two expected FAILs. |
| equation reviewer suite, unmodified (`a56c511ed9b08088b872194adf8de1ad5fee898b6fb927c1a467690823a8b4cd`), on c2v002 | 71/71 |
| interface reviewer probe `probe_broadcast_square_grid.py` (`336a8c77e8b844b2aa342650bb33b72096137c9712aef1575521783e79606a6c`), on c2v002 | "1-D Omega(R) accepted: False \| explicit (N,1,1) accepted: True". The script then stops with a KeyError because it assumes the 1-D input is accepted. |
| `probe_nonfinite_diagnostics.py` (`f0f629fe7410879923cd91c2ee57235d21643fd013a9020a39fd50278fa35c19`) | c2v001: ok=True with a non-finite `linearized_entropy`. c2v002: ok=False, stage `floating_point` in `identity_diagnostics`. |

The two expected FAILs in the interface reviewer suite:
- **Success key set:** it now includes the added `input_shapes` key, by design (B1).
- **Masked-array PROBE:** this is review note N2, which is outside this fix.

The 34 delta checks are:
- **B1:**
  - Rank-1, rank-2 and rank-4 inputs are rejected for every array argument, with zero callbacks first. This includes a 1-D length-N_z Omega that numpy would right-align to z, and 1-D `z`, xi, r0, forcing and supplied-derivative inputs.
  - On an 8×8×8 square grid:
    - 1-D Omega(R) is rejected.
    - (N,1,1) is accepted, with Omega_R = 0.5 and Omega_z = 0 to within 1.5e-14.
    - The residuals are bitwise equal to the full-array input.
    - 0-d and an explicit (1,1,N) are accepted and recorded in `input_shapes`.
- **0428-F:**
  - On success, every module-owned returned value is finite.
  - The diagnostic overflow fails closed (`floating_point`, `identity_diagnostics`). The response is called once and errstate is restored. The same happens under the caller's `seterr(all='raise')`.
  - A hidden `rho0**2` overflow in an Euler term fails closed (`floating_point`, `euler_residual`).
  - **Layer independence.** A scratch copy with the module errstate set to ignore was run on the same inputs:
    - The output sweep alone fails closed on `identity_diagnostics['linearized_entropy']`.
    - The same copy returns the overflowed Euler term as a finite, wrong 0. That is why errors are not suppressed.
  - Success results are identical under the caller's errstate set to ignore or to raise.
- **0428-B:**
  - A sign-changing real Omega with a large nonzero r0 is accepted.
  - Omega is used bitwise as given.
  - r0 enters each residual once (1.5e-16).
  - All three components are returned, with one response call and the full native output retained.
  - `not_done` states that there is no force-balance gate and no stationary state.
  - The module text contains no "equilibrated base" gate wording.
- **B2 (illustration, module unchanged).** On the 21×16×17 Chebyshev/FFT grid, rho0 > 0 on the top and bottom faces and an m=0 xi_z = 0.02 z R is applied. Integrating with Clenshaw–Curtis weights gives ∫drho dV = −1.514248 = −∮ rho0 xi·n dA. That is a nonzero net mass in `delta_f_n` (fact 10).

Engine errors on c2v002 are unchanged from c2v001:
- **Engine A:** at most 2.3e-11 relative.
- **Engine B:** at most 9.7e-11.
