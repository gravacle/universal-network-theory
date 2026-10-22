# INTERFACE 0431 V001: modal candidate to full-grid action join (Claude2, c2v001)

Module: `modal_full_grid_join_c2v001.py` (same folder), sha256 `1cf7d3f884ff27938d94dc4a5d3efa75e15b7f82b3d27b16d25c75d8f1910790`.

The module is inert. It does no I/O and runs nothing at import. It uses numpy and the stdlib only (`inspect`, `math`, `types`, `collections.abc`). Public arguments are keyword-only with no defaults, and every failure returns a fail-closed dict. It never imports a UNT file: the binding module and the action module are module objects that the caller supplies.

Binding inputs (each sha256 was checked from its bytes before authoring):
- Task 0431: `4bbd7caad822c88abd10d415e190d0d5364d404a0a252543b2b9414f60bd8c5b`
- Action `ddo_noncircular_displacement_action_c2v002.py`: `056db7b19443d4a88dcb6396531dfe1ff61acd8ba8387e6bfd0a8b64cf179925`, with its `INTERFACE_0427_V002.md`: `82d7c6cdf37eb40b03d429e77ae11e1a3c80cd80f630f67ea8dbba972d834a7c`
- Root binding `owned_body_fitted_displacement_binding_v002.py`: `87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462`. It was read as text only (`make_mesh`, `constraint_rows`, `evaluate_action`).

The following were not read: the modal solver code, saved physical data, calibration values and target velocities.

## 1. Public signatures

```
assemble_real_displacement(*, mesh, mode_results, nphi, imag_atol, imag_rtol)

evaluate_modal_candidate(*, binding_module, action_module, mesh, base_fields, c_light,
    gamma, tolerances, provenance, mode_results, nphi, imag_atol, imag_rtol,
    induced_response)
```

## 2. Layout and conventions

**Mesh.** The mesh is the dict that root `make_mesh` returns.
- `grid_shape = (nr, nphi, neta)`, where `nr = len(radial_nodes_m)` and `neta = len(eta_nodes)`. The array axes are (R, phi, eta).
- The module reads only `grid_shape` and `phi`. The whole mesh object goes unchanged to `evaluate_action`.

**Phi nodes.** The phi nodes are phi_j = 2*pi*j/nphi for j = 0..nphi-1.
- They are taken from `mesh['phi']`. That array must be float64 with exactly `grid_shape`, must be constant along the R and eta axes, and its line must equal `2*np.pi*np.arange(nphi)/nphi` **bitwise**, which is root's own expression.
- `nphi` must be an int equal to `grid_shape[1]` and must satisfy `nphi > 12`, so that m = 0..6 has no aliasing. Root uses 16.

**Candidate layout.** `xi_cylindrical_m` has shape exactly `(3, nr*neta)`.
- Rows are (R, phi, z) physical orthonormal components in metres. xi_phi is a length, and z is physical z, not eta.
- Column k = iR*neta + ieta. That is R-major / eta-minor, the numpy C-order `reshape(nr, neta)`.

**Fourier convention (FFT/nphi).** xi_m = (1/nphi) Σ_j f(phi_j) exp(−i m phi_j), which is the `np.fft.fft(f, axis=phi)/nphi` slot m.

**Reconstruction.** f(iR, j, ieta) = Re xi_0 + 2·Re Σ_{m=1..6} xi_m exp(+i m phi_j).
- The factor 2 accounts for the conjugate slots nphi−m.
- The sum is evaluated directly, not by inverse FFT, in L223-232.
- Im xi_0 is tested (§3) and then discarded.

**Output xi.** The output is a tuple `(xi_R, xi_phi, xi_z)` of read-only float64 arrays of exactly `grid_shape`.
- This is the layout root `evaluate_action` requires: it forwards `xi` unchanged to c2v002 `evaluate_bulk_action(xi=...)`, whose `_triple` accepts only a tuple of three full-rank or 0-d arrays.
- All complex inputs, after conversion to complex128, are checked finite, and so are all outputs.

## 3. `assemble_real_displacement`

**`mode_results`** must be a list or tuple of mappings. Each mapping carries:

| key | requirement |
|---|---|
| `'m'` | int, not bool |
| `'solve_failed'` | explicit bool. True is rejected as a failed solve, and no candidate is invented. |
| `'accepted_inner'` | explicit bool |
| `'xi_cylindrical_m'` | a plain ndarray that is not None and not masked. Its dtype is float≤64 or complex≤128, its shape is exactly `(3, nr*neta)` and its values are finite. |

Extra keys are allowed. They are ignored, and the original mappings are kept by identity under `mode_results_by_m`.

**Mode set.** Each m in 0..6 must appear exactly once. A single reason lists any `duplicate`, `extra` (outside 0..6) and `missing` modes. No mode is ever zero-filled.

**m=0 imaginary test (exact).** Both of these must hold:

`max|Im xi_0| <= imag_atol` AND `max|Im xi_0| <= imag_rtol * max|Re xi_0|`

- Each max runs over all three components and all nr·neta columns. The components share units of metres.
- `<=` is used, so atol = 0 admits an exactly real xi_0.
- Per-component maxima are reported but not gated.
- `imag_atol` and `imag_rtol` must be finite and ≥ 0.

**`accepted_inner`.** A False value does not stop assembly when finite arrays exist. The flag is returned in the read-only `inner_accepted_by_m` (a MappingProxyType) and in `modes_with_accepted_inner_false`. It is never aggregated or promoted.

**Return values.**
- Success: `{'ok': True, 'module', 'stage': 'assembled', 'acceptance', 'xi', 'grid_shape', 'nphi', 'phi_nodes', 'inner_accepted_by_m', 'modes_with_accepted_inner_false', 'm0_imaginary_check', 'mode_results_by_m', 'conventions'}`.
- Failure: exactly `{'ok': False, 'module', 'stage', 'reason', 'acceptance'}`, where the stage is one of `input_validation`, `mesh`, `mode_results`, `m0_imaginary`, `reconstruction`, `floating_point` or `internal`.
- The function receives no callback, so it cannot call native feedback.

## 4. `evaluate_modal_candidate`

**Order of operations.**
1. **Join validation (no call yet).**
   - `binding_module` and `action_module` must be `types.ModuleType`.
   - `binding_module.evaluate_action` must have exactly the keyword-only, default-free parameters of root v002: `{action_module, mesh, base_fields, xi, induced_response, gamma, c_light, base_axisymmetry_rtol, polytrope_consistency_rtol, base_provenance}`. This is checked with `inspect.signature`.
   - `action_module.MODULE_TAG` must be `'ddo_noncircular_displacement_action_c2v002'` and `evaluate_bulk_action` must be callable.
   - `induced_response` must be callable.
   - `tolerances` must be a mapping with exactly the keys `base_axisymmetry_rtol` and `polytrope_consistency_rtol`.
2. **Assembly.** It runs once (§3). If it fails, `evaluate_action` is never called.
3. **The single call** (L469):
   ```
   evaluate_action(action_module=action_module, mesh=mesh, base_fields=base_fields, xi=<assembled tuple>,
       induced_response=induced_response, gamma=gamma, c_light=c_light,
       base_axisymmetry_rtol=tolerances[...], polytrope_consistency_rtol=tolerances[...],
       base_provenance=provenance)
   ```
   - Every supplied object is passed by identity. The wrapper validates none of the values; root and c2v002 do.
   - `base_fields` is not touched, so the base-source offset already in Phi0, the angular forcing and r0 is not added again.
   - The call runs under the caller's numpy errstate.
4. **Report.** The returned mapping is kept **by identity, unmodified** as `action_result`. That includes the full Euler residual, `euler_terms`, perturbations, `source_feedback`, `induced_response_full`, `base_checks`, `identity_diagnostics`, `mesh_constraints` and `mesh_scope`.

**Success keys.**
- `ok`, `module`, `stage='modal_candidate_evaluated'`, `acceptance='NOT_ASSESSED_BY_THIS_WRAPPER'`, `acceptance_scope`
- `evaluate_action_call_count` (=1)
- `action_result`, `action_result_module`, `response_call_count_reported` (the action's own count)
- `assembly`, `inner_accepted_by_m`, `modes_with_accepted_inner_false`
- `euler_residual_angular_fourier`
- `density_pressure_diagnostics`
- `diagnostic_availability`
- `xi_bitwise_equal_in_returned_boundary_state`
- `not_done`

**`euler_residual_angular_fourier`.**
- For each of R, phi and z it computes F = `np.fft.fft(res, axis=1)/nphi` and reports **all nphi slots** as two arrays of length nphi: `slot_l2_over_R_eta`, the unweighted Frobenius norm over the (R, eta) nodes, and `slot_max_abs`.
- It also reports `all_slots_l2`, `retained_slots_l2` (|m| ≤ 6), `omitted_slots_l2`, `omitted_slots_max_abs` and `nodal_l2_over_sqrt_nphi`. The last is the Parseval cross-check, which is not gated.
- The slot labels are `slot_index`, `signed_m` (s for s ≤ nphi/2, s−nphi otherwise), `retained_slot` and `omitted_slot_indices`.
- At nphi = 16 the omitted slots are 7, 8 and 9: signed m = +7, ±8 (Nyquist) and −7. The 0431 phrase "modes 7/8/9 and their conjugate slots" is read as exactly these slots. A literal m = 9 is not separately representable on 16 nodes.
- If the returned residual is not exactly {R, phi, z} real finite `grid_shape` arrays, the call fails closed at stage `euler_residual_report` and `action_result` is preserved.

**`density_pressure_diagnostics`.**
- When the returned fields permit it, this reports `min(rho0+drho)`, `min(P0+dP)` and `max|drho/rho0|`, each with its (R, phi, eta) index. The values are unclipped and may be negative.
- The sources are `boundary_state['rho0']`, `boundary_state['P0']`, `perturbations['drho']` and `perturbations['dP']`.
- Otherwise it returns `{'status': 'UNAVAILABLE', 'reason'}`.

**`diagnostic_availability`.**
- Status values for the top-level sections: `ABSENT` or `PRESENT`.
- Status values for the identity and base residual arrays: `AVAILABLE_FINITE`, `PRESENT_NONFINITE`, `PRESENT_NOT_ARRAY` or `ABSENT`.
- `induced_response_full` is reported as `PRESENT_NOT_TRAVERSED`.
- Each entry of `mesh_constraints` gets its own status. A text entry is reported as `TEXT`.

**Failure.**
- The base is `{'ok': False, 'module', 'stage', 'reason', 'acceptance', 'evaluate_action_call_count'}`.
- `assembly` is added once assembly has run.
- `action_result` is added, by identity, whenever `evaluate_action` returned.
- The stages are: `join_validation` (0 calls), `assembly` (0 calls), `evaluate_action_raised` (1), `evaluate_action_output` (1), `evaluate_action_not_ok` (1), `euler_residual_report` (1) and `internal`.
- No Fourier report or density/pressure diagnostic is ever returned on failure.

**Not done.** The wrapper does none of the following:
- clipping, forced positivity, a boundary lid or thresholds
- a convergence decision
- retained-mode-only assessment
- physical or calibration acceptance
- promotion of inner flags

`ok=True` means only this: assembly passed, the one call returned `ok=True`, and the all-slot report was computed.

## 5. Fixtures (NONPHYSICAL, stub modules only)

- **Script:** `scratchpad/r0431/fixtures_0431.py`, sha256 `9134dc91aa274cc556f8e623b3b2efd572baa26fbcd924ab3bddbb20ef9ebd1a`
- **Output:** `fixtures_0431.out`, sha256 `fb9f76dcc484ed0a09aca5e6ac2d9cfa0f54a03aefe8e3119e8d724e7c542d19`
- **Runtime:** `python3 -I -B` (codex runtime, Python 3.12.14, numpy 2.3.5), under a 120 s alarm
- **Grid:** 3×16×4
- **Result:** **62/62 PASS**
- The root binding and c2v002 were not imported. No project data was used.

| group | checks |
|---|---|
| Static contract | Top level holds only imports, constants and defs. Imports are numpy and stdlib only. There is no open/print/exec. Both public signatures are keyword-only with no defaults. |
| Conjugate / factor 2 | <ul><li>A hand-built real field a0 + Σ (A_m cos mφ + B_m sin mφ) gives coefficients (A−iB)/2. These equal the FFT/nphi slots to <1e-13.</li><li>Reconstruction from shuffled mode order matches the field to 1.78e-15.</li><li>Conjugated coefficients reproduce f(−φ), not f.</li><li>xi_3 = 0.5 gives cos 3φ, and xi_3 = −0.5i gives sin 3φ, both with amplitude 1.</li><li>eta-major (Fortran) flattening does not reproduce f, so the layout is load-bearing.</li><li>m0 imaginary: 1e-14 passes, 1e-9 > atol is rejected, and below-atol-but-above-rtol is rejected (the AND test).</li></ul> |
| Rejection | <ul><li>Mode set: missing m=3, duplicate m=2, extra m=7, m=5→7 (reports both extra and missing), and bool m.</li><li>Solve flag: `solve_failed=True`, and `solve_failed` absent.</li><li>Candidate: None or absent.</li><li>`accepted_inner` absent.</li><li>Arrays: non-finite imaginary part, and shapes (nr·neta, 3) and (3, nr, neta).</li><li>Containers and grid: mode_results given as a dict, nphi ≠ mesh, shifted phi nodes, and negative atol.</li></ul>Every rejection is the exact 5-key fail dict. |
| Join counters | <ul><li>The stub `evaluate_action` was called exactly once.</li><li>The `induced_response` count was 0 on entry to it, so assembly makes no calls. The total is 1, made by the stub itself.</li><li>mesh, base_fields, induced_response, action_module, gamma and c_light were passed by identity. The tolerances and provenance mapped to the root names.</li><li>The returned dict is preserved by identity.</li><li>The xi round trip is bitwise.</li></ul> |
| Omitted-mode retention | The stub returns these residuals: R = g·cos 7φ, phi = h·cos 8φ (Nyquist), z = p·sin 7φ + q·cos 2φ. <ul><li>All 16 slots are reported.</li><li>omitted = (7, 8, 9).</li><li>Slot norms are exact: 0.5‖g‖ in slots 7 and 9, and ‖h‖ in slot 8.</li><li>The retained norm is ~1e-15 for R and phi.</li><li>z splits into √0.5‖p‖ omitted and √0.5‖q‖ retained.</li><li>Parseval holds.</li></ul> |
| Diagnostics | <ul><li>min(rho0+drho) = −0.5 is reported unclipped at (1, 5, 2), along with min(P0+dP) and max ratio 1.25.</li><li>Availability distinguishes ABSENT, PRESENT_NONFINITE (a mesh constraint) and AVAILABLE_FINITE.</li></ul> |
| Fail paths | <ul><li>An assembly failure gives 0 evaluate and 0 response calls.</li><li>Rejected before any call: a signature with an extra defaulted parameter, a c2v001 MODULE_TAG, and a tolerance mapping with a missing key.</li><li>A raising `evaluate_action` gives `evaluate_action_raised` with count 1.</li><li>An `ok=False` return is preserved by identity, with no report.</li></ul> |

## 6. Missing interface facts

The task text does not name the items below. Each is required explicitly here and is never defaulted.

1. **Mode-index field.**
   - 0431 names no key for m. This module requires int `'m'` in each mapping, given as a list or tuple. That form is what makes duplicates detectable.
2. **Failed-solve representation.**
   - 0431 says "failed solves with no candidate" but names no field. This module requires an explicit bool `'solve_failed'` on every mode, and True is rejected.
   - A candidate that is absent or None is also rejected.
3. **Component order and type.**
   - 0431 says only "cylindrical". This module assumes rows (R, phi, z), physical orthonormal components in metres, with xi_phi a length and z physical z (the c2v002 convention).
4. **Nodal meaning.**
   - The columns are assumed to be values at the mesh nodes (R_i, eta_l), not coefficients of a radial or vertical basis.
5. **Coefficient sign and normalization.**
   - FFT/nphi with the forward kernel exp(−i m phi), phi_j = 2πj/nphi, is assumed as stated.
   - A conjugate-sign or eta-major producer cannot be detected from the data. The fixtures show that either one silently gives a different field.
6. **Wrapper-to-root argument names.**
   - `tolerances` → `base_axisymmetry_rtol` and `polytrope_consistency_rtol`.
   - `provenance` → `base_provenance`.
7. **Granularity of the m0 test.**
   - This module chose a max over all three components (§3) and reports the per-component values.

## 7. Limitations

- **Binding and action identity.**
  - The binding is matched by signature only. The action is matched by `MODULE_TAG` only.
  - Module bytes are not hashed. Root must supply the actual binding v002 and the actual c2v002 module.
- **Lost bulk result.**
  - Root `evaluate_action` raises `ValueError` from its own pre-checks and from `constraint_rows`. If `constraint_rows` raises after c2v002 succeeded, the bulk result is lost inside root.
  - The wrapper can report only `evaluate_action_raised` with count 1 and no `action_result`.
- **Fourier norms.**
  - They are unweighted and nodal. There is no volume weighting, normalization or gate.
- **Density and pressure diagnostics.**
  - These are first-order linear sums only.
- **Untested against the real modules.**
  - By policy, nothing was tested against the real root binding, real c2v002 or project data. The stubs mirror the root signature and the c2v002 return keys, which were read from text.
- **Not written here.**
  - A distinct review was not done here; that belongs to the checker.
  - No FROM_CLAUDE2 ACK was written. This run was restricted to this folder and the scratchpad.
