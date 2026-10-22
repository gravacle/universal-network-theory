# INTERFACE 0449 V001: nonzero-mode density increment through the cached full-ten response (Claude2 binding author)

## Pins (sha256 from bytes)

| File | sha256 | Use |
|---|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_cached_feedback_0449/nonzero_cached_feedback_c2v001.py` | `1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95` | **this deliverable** |
| Task `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0449_2026-10-16_claude2_nonzero_cached_feedback_binding.md` | `b7e1cdc3cd4a45d6c4dd36136ff9f720c7a5362adc683560f4f0775dda675cc4` | binding (the 14:31:40 rewrite) |
| `.../nonzero_density_fourier_0445/nonzero_density_fourier_c2v001.py` | `255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4` | injected as `density_fourier`; not rewritten |
| `.../nonzero_density_fourier_0445/posix_libm_bessel_jn_provider_c2v001.py` | `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67` | injected as `jn_provider` (its READY dict) |
| `.../nonzero_density_fourier_0445/REVIEW_0445_V001.md` | `0d89334a892b1c535aacf6114248caef0c6709d9f381d54b7f1f0fd1d7250b43` | read; note 1 (require READY) and note 6 (placement) adopted |
| `.../recovered_packet_audit/owned_fixed_xy_fourier_line_v002.py` | `3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18` | injected as `prepare_line` / `evaluate_line`. It equals `PINS['line']` in `ddo_homotopy_reference_root_worker_v001.py` (sha `acda989d…bbe36`, read as text). |
| `.../coefficient_method/ddo_free_surface_native_feedback_root_v004.py` | `6da11133734e65fe31b6408d4f64d0e50df9f453c8872308b960678d80ec02ed` | text only |
| `.../coefficient_method/ddo_free_surface_rotation_root_v005.py` | `1b42990556ee34d30a7a12eb5b5605aa1e43aa8322e03d73bbab86e5c38497b7` | text only |

`unit_response.npz` (`f3d29c62…`) and `refreshed_prepared.npz` (`e1135cd2…`) were not opened. The module does no I/O.

## Layout and lapse index (taken from the root text)

- **Unit response as root stores it:** `weighted_responses` has shape **(nk, 10, 1)**, aligned with `wavevectors` (nk, 3).
  - v004 line 2: "cached weighted full10 -K^-1 e_n".
  - v004 line 84 loads `wavevectors`, `weighted_responses` and `dk_weights`.
  - v004 line 90 requires `unit.shape == (len(waves), 10, 1)`.
- **Source column = source coordinate 0** (the lapse source e_n). It is the only stored column.
  - v004 line 74 requires `J[:,1:,:] == 0`.
  - v004 line 90 requires `oldgas[:,1:,:] == 0`.
  - v004 line 100 computes `unit * delta[:, 0:1, :]`.
- **Field lapse index = 0 on axis 1.**
  - v005 line 102: `N = 1 + f[0].real`.
  - v005 lines 104–107: Phi and its gradient come from `f[0]` and `g[0, :]`.
  - The line module's `lapse_difference` (line 76) reads `fields[:, 0, :]`.
- **Base:** the same (nk, 10, 1) layout, with wavevectors bitwise equal to the unit's (v004 lines 87–90; v005 line 88).
- **Evaluation roster (v005):**
  - Points are `R[i]`, `phi = 2*pi*j/16`, `x = R cos phi`, `y = R sin phi`, and `z = arrays['z'][i, j, l]` (v005 lines 95–96).
  - Boundaries are zero, with shapes (1,10,1), (1,10,1,3) and (1,10,1,3,3) (v005 line 97).
  - The reality test is `|Im| > atol + rtol |Re|` on f, g and h (v005 line 100).
- A (nk, 10, 10) layout is **rejected**. Root does not store one, and choosing a column from it would be a root decision.
- `dk_weights` is ignored if present, because the unit response already carries dk/(2pi)^3.

## Signature

```python
nonzero_cached_feedback(*, density_fourier, jn_provider, radius_m, z_m, weights_RdRdz_m3,
    rho_mode_kg_m3, mode, k_physical_inverse_m, unit_response, base_prepared,
    prepare_line, evaluate_line, eval_radius_m, eval_phi_rad, eval_z_m, c_m_s,
    base_reality_atol, base_reality_rtol, increment_reality_atol, increment_reality_rtol,
    wave_chunk, position_chunk, include_log_difference, provenance) -> dict
```

All arguments are keyword-only, with no defaults. Import is inert. The module imports only `math`, `numbers`, `collections.abc` and `numpy`.

**Route chosen:** the core calls the supplied 0445 **callable** itself, using the supplied roster and the READY provider's `bessel_jn`. It never accepts a precomputed deltaJ0.

| Argument | Contract (a violation returns `INVALID_INPUT` at `validation`, and nothing is called) |
|---|---|
| `density_fourier` | callable; the pinned `nonzero_mode_density_fourier` |
| `jn_provider` | mapping with `status == 'READY'` and a callable `bessel_jn`; this is the return value of `create_jn_provider` |
| `radius_m`, `z_m`, `weights_RdRdz_m3`, `rho_mode_kg_m3`, `mode` | Root's roster (R dR dz **without 2pi**), passed unchanged to 0445, which validates them. 0445 `INVALID_INPUT` maps to `INVALID_INPUT` at `density_fourier_validation`. |
| `k_physical_inverse_m` | (nk, 3) real, finite, signed, in root order. The core passes its validated copy to 0445. |
| `unit_response`, `base_prepared` | mappings with `wavevectors` (bitwise equal to k, in the same order) and `weighted_responses` (nk, 10, 1), dtype complex128 or float64-representable, finite |
| `prepare_line`, `evaluate_line` | callables; the pinned v002 line functions |
| `eval_radius_m` | (nR,) finite, > 0 |
| `eval_phi_rad` | (nphi,) finite; pass all 16 roster angles |
| `eval_z_m` | (nR, nphi, nz) finite, nz >= 1; this is v005's `arrays['z']` |
| `c_m_s` | real, not bool, finite, > 0, with c*c finite and > 0 |
| four `*_reality_atol/rtol` | real, finite, >= 0. Base and increment are checked separately. |
| `wave_chunk`, `position_chunk` | int >= 1, not bool; passed to 0445 |
| `include_log_difference` | bool |
| `provenance` | mapping, returned as a shallow copy |

## Return dict

- **Top level:** `status` (`COMPLETE` / `INVALID_INPUT` / `FAILED_CLOSED`; `INTERRUPTED` only on an attached exception), `complete`, `reason`, `failure_stage`, `exception_type`, `failure_point` (i, j, l), `failure_check` (role, kind, max_abs_imag, max_excess), `provenance`, `inputs` (dtypes, grid, eval arrays, `angles_equal_2pi_j_over_n`, tolerances, chunks), `jn_provider_metadata`, `completeness`, `reality`, `convention`, `retained`.
- **Payload, set only on `COMPLETE`:**
  - `density_fourier_result`: the full 0445 dict.
  - `deltaJ0_J`: (nk,) J.
  - `delta_prepared`: `{wavevectors, weighted_responses (nk,10,1)}`.
  - `base_line` and `increment_line`: each `{fields (nR,nphi,nz,10), gradient (...,10,3), hessian (...,10,3,3)}`, complex, Cartesian.
  - `point_mask`.
  - `lapse`: `nb`, `grad_nb_cartesian`, `dn`, `grad_dn_cartesian`, `Nb`.
  - `linear`: `label`, `deltaPhi_m2_s2`, `grad_deltaPhi_cartesian_m_s2`, `grad_deltaPhi_cylindrical_R_phi_z_m_s2`.
  - `log_difference`: the same keys under its own label, or `None` when not requested.
- **On failure:** every payload key is `None`, and `retained` holds the same keys as computed so far. Unevaluated points are NaN and `point_mask` is False there.
- **Interruption:** a `KeyboardInterrupt` or other non-Exception is re-raised, with the retained dict attached as `exc.unt0449_retained_result`.
- **`completeness`:**
  - `density_fourier_status`, `points_expected` / `points_evaluated` / `all_points_evaluated`.
  - Line call counts, actual and expected.
  - `checks`: `density_fourier_complete`, `deltaJ0_finite`, `delta_prepared_finite`, `all_points_finite_and_real`, `lapse_inputs_finite_Nb_positive`, `linear_finite`, `log_difference_finite` (None if not requested).
- **`reality`:** for each of base/increment × fields/gradient/hessian, `max_abs_imag`, `max_excess` (<= 0 when passing) and `points_checked`.

## Step → line map (installed bytes)

| 0449 step | Lines |
|---|---|
| Validation: callables, READY provider, bool/int/c/tolerances, waves (nk, 3), layout (nk, 10, 1), bitwise wave order, eval shapes | 81–170 (READY 135–138; wave equality 100; layout 109) |
| 1. Call 0445 with the READY provider; map INVALID_INPUT | 299–308 |
| 1. Require COMPLETE, `complete is True`, counts.waves == nk, mode, full wave mask, complex128 (nk,), finite; read-only copy | 309–329 |
| 2. `delta_prepared = unit * delta_j[:, None, None]`, once; finite | 333–338 |
| 3. Base and increment prepared packets (same k), zero read-only boundaries | 342–356 |
| 3. Per (R_i, phi_j): `x = R cos phi`, `y = R sin phi`; `prepare_line` for base and increment | 357–365 |
| 3. Per z: `evaluate_line`; packet shape/dtype check; finite + reality check for f, g, h, base then increment; fail at first violation | 366–389 (helpers 173–197) |
| 3. Store complex full-ten fields and jets only after both roles pass; set mask | 390–394 |
| 4. Real lapse inputs (index 0), `Nb = 1 + nb`, finite, `Nb > 0` | 397–410 |
| 4. LINEAR `c^2*(dn/Nb)`, `c^2*(grad_dn/Nb - dn*grad_nb/(Nb*Nb))`, cylindrical, finite | 415–425 (cylindrical helper 200–204) |
| 4. Optional FINITE LOG DIFFERENCE, separate dict; `Nb+dn > 0` and `dn/Nb > -1` | 427–446 |
| 5. All supplied angles kept; full (nR, nphi, nz) arrays; no DFT | 357–393, 411–412 |
| 6. Completeness, checks, provenance, fail-closed / interrupt handling | 266–295, 448–456 |

**Where the finite and reality checks sit:**

1. Validation checks that every input array is finite (81–113, 153–167).
2. deltaJ0 is checked at 325, and delta_prepared at 334.
3. Every line read is checked at 373–389, which runs before line 392 stores it and before any `.real` is taken. Real parts are first taken at 398–401, after line 394 has confirmed that every point passed.
4. A failed imaginary remainder stops the call. Nothing is averaged, discarded or projected.

## Fixtures (synthetic analytic only)

**Setup:**

- Interpreter: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (Python 3.12.14, NumPy 2.3.5), with `VECLIB_MAXIMUM_THREADS=OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`.
- The 0445 contraction, the provider and the line module were loaded from hash-verified bytes. The verified bytes are the ones executed.
- No `.npz` file, root worker, target data or galaxy run was used.

**Scratch files:**

| File | sha256 |
|---|---|
| `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0449/binding_author/test_binding_c2v001.py` | `03d3b91bf411978268aa586f5db28e912765a6999b655f71be1e2fe10a5982ba` |
| `run1.json` (records target sha `1b4f129f…`) | `8a3af91d15968565ef21a0d9348abc30cad1b402a499c2e3cffa5ce67a9ee48c` |

**Result: 59 of 59 PASS.**

| Fixture | Result |
|---|---|
| **A. Paired ±k waves.** 8 waves including a k_perp=0 pair, in scrambled signed order; m=1; q=3; 2 radii × 16 roster angles × 3 z; errstate `raise` | COMPLETE. deltaJ0 vs a direct 2048-node azimuthal trapezoid (no Bessel, no (-i)^m): 1.3e-16. `delta_prepared` is bitwise equal to `unit*deltaJ0[:,None,None]` and to v004's `unit*delta[:,0:1,:]`. Increment fields, gradient and Hessian vs a brute Σ_k U_k ΔJ_k e^{ik·x}: ≤ 5.9e-16. Base vs brute: 4.6e-16. Base read is bitwise equal to a direct v005-pattern line call. Linear and gradient formulas match; log difference vs c²[log(Nb+dn) − log Nb]: 1.0e-15. max \|Im\| of increment is 1.2e-17. Call counts are 64/192. |
| **A2. Finite differences through the module.** R, phi and z steps of 1e-5 | linear and log cylindrical gradients agree to 9e-11; Cartesian FD of brute c²dn/Nb agrees to 1.5e-11. Non-roster angles are flagged. |
| **B. One wave in closed form.** Single ring point, real rho, m=1, unit u on component 0 | dn = −4π u c² J₁(k⊥) cos α sin(k·x) holds to 3.4e-16 (c=3) and 2.8e-16 (physical c). Component 3 is carried. Nb is exactly 1. A single k_perp=0 wave gives deltaJ0, increment and ΔPhi all exactly 0. |
| **C. Reality** | An unpaired single wave gives FAILED_CLOSED at `point_checks` (increment, fields, point (0,0,0)), with no lapse derived and deltaJ0 retained. It passes only when the caller's atol admits it. A corrupted base fails on the base role first. |
| **D. Positivity** | Nb ≤ 0 gives FAILED_CLOSED at `lapse_inputs`, with every complex point retained. Nb+dn ≤ 0 (33 points) with log requested gives FAILED_CLOSED at `log_difference`, with linear retained. The same input without log is COMPLETE. |
| **E. Gating** | A J0-substituting provider makes 0445 FAILED_CLOSED; the result is FAILED_CLOSED, and the partial deltaJ0 is not consumed (0 line calls). mode 7 gives INVALID_INPUT. A non-READY provider means 0445 is never called. A forged COMPLETE (complete flag False, or an incomplete wave mask) gives FAILED_CLOSED. |
| **F. Validation** | 25 malformed inputs, including (nk,10,10), permuted or perturbed waves, int dtype, inf/NaN, bad eval shapes and bool tolerances, all give INVALID_INPUT with nothing called. A missing keyword raises TypeError. Keyword-only with no defaults is confirmed. |
| **G. Errstate and interruption** | Under `raise`, overflow in delta_prepared gives `FloatingPointError` → FAILED_CLOSED with deltaJ0 retained. Under `warn`, the RuntimeWarning is emitted and the call fails closed. A KeyboardInterrupt on the 41st read is re-raised with INTERRUPTED attached and 20 points retained. A malformed line packet fails closed. |
| **H. Mode mixing** | A ring of 48 waves with an anisotropic unit response (1+0.6 cos 2α) and an m=1 source puts m=3/m=1 = 1.8e-2 in the 16-angle output, against 7.5e-13 for the isotropic response. The output is not projected to the input m. |
| **I. Chunks** | 5 (wave_chunk, position_chunk) pairs, recorded in the 0445 result, agree to rounding. |
| **J. kpc scale** | Physical c, rho ~1e-21, kpc radii and k under `raise`: COMPLETE and finite. |
| **K. Lane** | AST check: no `@`, dot, einsum, linalg, errstate, warnings, open, print, eval or exec. Imports and top level are as stated above. |
| **L. Mutants** | 8 author-side mutants are all detected: extra minus, extra c², extra 2π, Nb not squared, lapse from component 1, Im discarded before the check, log substituted into linear, cylindrical sin/cos swapped. |

## Root use (outside the core)

Root does all loading. Verify each pin from bytes, load the 0445 contraction, provider and line module, and call `create_jn_provider(library_policy='posix_find_library_m', ...)`, requiring READY. Pass these:

| Argument | Value |
|---|---|
| `unit_response` | `{wavevectors, weighted_responses}` from the unit packet |
| `base_prepared` | `{wavevectors, weighted_responses}` from the F2 `refreshed_prepared` packet |
| `k_physical_inverse_m` | the same waves |
| roster | R, z, R dR dz and rho_m |
| `eval_radius_m`, `eval_phi_rad`, `eval_z_m` | the v005 roster |

Persisting the result is also root's job.

## Limitations and missing interface facts

1. **Stored dtypes are UNTESTED.** I did not open the packets, so the dtypes of the stored `weighted_responses` are not known. The module accepts complex128 or float64-representable values and records both dtypes in `inputs`.
2. **rho_m convention.** rho_m must follow the 0445 convention: the real perturbation is rho_m e^{imφ} + conj(rho_m) e^{-imφ}. That makes rho_m equal to the complex azimuthal Fourier coefficient c_m of the real density, not 2c_m and not a real amplitude. Root must confirm its density-only m1 product uses this convention.
3. **Reality tolerances.** As in v005, one (atol, rtol) pair is applied to fields, gradients (1/m) and Hessians (1/m²) alike. The increment has its own pair because its scale differs from the base. Choosing values that suit both the scale and the units is root's job.
4. **Base boundary.** The base boundary is fixed at zero, following the v004 line 107 contract and v005 line 97. A nonzero base boundary would need a new version.
5. **No DFT.** No DFT or modal output is returned. Sixteen angles resolve |m| ≤ 7 without aliasing (m = 8 is the Nyquist slot), and content at higher m aliases. Interpretation belongs to root.
6. **Scale and memory are UNTESTED.**
   - The cost is 2 × nR × nphi `prepare_line` calls over all nk waves and 2 × points `evaluate_line` calls, plus one 0445 contraction.
   - The retained complex fields and jets take about 2 × points × 130 × 16 B, about 153 MB for 72 × 16 × 32 points.
   - There is no chunk control in the line stage; only the 0445 chunk controls exist.
   - Deciding test: root times one radius at production nk.
7. **Provenance only.** The module cannot verify that the injected callables are the pinned ones, or that the base is F2. These rest on the `provenance` that root supplies.
8. **Two outputs, no selection.** Linear and log-difference results are both reported where requested. Neither is selected or accepted physically. No solve, regularization, clipping, renormalization or acceptance is done.
