# INTERFACE 0433 V001: supplied physical perturbations, native feedback and strong residuals

Module: `supplied_perturbation_action_c2v001.py` (Claude2, author). It is pure and inert: numpy plus stdlib only, nothing runs at import, and it does no I/O. Line numbers below refer to that file.

The module reads its contract from four texts: task 0433 (`a9f411b1…ac5c`), the root binding v002 (`87866875…5462`, read as text for its derivative and callback contract only), 0427 c2v002 (`056db7b1…f179925`, for the weak_field_delta_n contract and validation style) and 0431 (`1cf7d3f8…d1910790`, for the angular-slot norm convention). It imports none of them.

## 1. API

```
evaluate_supplied_perturbations(*, mesh, base_fields, delta_rho, deltaP, deltaK, delta_v,
                                c_light, gamma, induced_response, provenance)
```

All arguments are keyword-only and have no defaults.

| argument | requirement |
|---|---|
| `mesh` | Root `make_mesh` mapping. Needs `grid_shape` as a tuple of 3 positive ints (nr, nphi, neta) with nphi even. Needs `R`, `phi` and `volume_weights_m3` as real finite arrays of exactly that shape. Needs the callables `partial_R`, `partial_phi` and `partial_z`, and `derivative_rule_description` as a nonempty string. `R` must be > 0 and depend on the R axis only. The `phi` line must equal `2*pi*arange(nphi)/nphi` bitwise. Weights must be > 0. |
| `base_fields` | Mapping holding `rho0`, `K0`, `P0`, `Omega`, `Phi0` and `angular_forcing_dPhi` as real finite arrays of exactly grid_shape, plus `axisymmetry_phi_variation_rtol` as a finite real ≥ 0 (see §4, fact 1). `rho0`, `K0` and `P0` must be > 0 at every node. Other keys are ignored and listed in `ignored_base_field_keys`. |
| `delta_rho`, `deltaP`, `deltaK` | Plain numpy real arrays (not masked, not complex) of exactly grid_shape, finite. They are never broadcast. |
| `delta_v` | A `tuple` (w_R, w_phi, w_z) of three such arrays, as physical orthonormal components. w_phi is a speed, not an angular rate. |
| `c_light`, `gamma` | Finite real scalars > 0. Bool is rejected. |
| `induced_response` | Callable. Called exactly once (L457) as `induced_response(delta_f_n=...)` with a read-only array. |
| `provenance` | Nonempty `str`, recorded verbatim. |

**On success** the call returns `ok=True` and `status='not_assessed'`, together with:
- `response_call_count` (=1);
- the input perturbations, as read-only copies;
- `base_fields_used`;
- `source.delta_f_n`;
- `induced_response_output`, `native_response` and `lapse_component`, all by identity and complete, with all 10 fields and their imaginary parts;
- `response_checks`;
- `potential` (`angular_forcing_dPhi`, `induced_potential` and `dPhi`);
- `r0` (R, phi, z);
- `residuals` (`euler_R`, `euler_phi`, `euler_z`, `continuity`, `entropy` and `eos_discrepancy`), labelled *supplied-state STRONG residual diagnostics*;
- `angular_slot_norms`;
- `positivity_diagnostics`;
- `mass_perturbation`;
- `base_checks`;
- `derivative_call_counts`;
- `conventions` and `not_done`.

**On failure** the call returns `{ok: False, module, stage, reason, status: 'not_assessed', response_call_count}`. If the callback has already returned, the dict also carries `induced_response_output` (by identity, unmodified) and `induced_response_validated`. No other partial arrays are returned.

## 2. Formula to line map (0433 verbatim, w = delta_v)

| quantity | line |
|---|---|
| r0 = (dR(Phi0) + dR(P0)/rho0 − R·Omega², 0, dz(Phi0) + dz(P0)/rho0) | L435-438 |
| continuity: dR(R·rho0·w_R)/R + dphi(rho0·w_phi)/R + dz(rho0·w_z) + Omega·dphi(delta_rho) | L439-440 |
| entropy: Omega·dphi(deltaK) + w_R·dR(K0) + w_z·dz(K0) | L441 |
| EOS: deltaP − gamma·P0·delta_rho/rho0 − rho0**gamma·deltaK (rho0**gamma at L401) | L442 |
| Euler pieces that do not depend on dPhi | L444-446 |
| delta_f_n = −c_light²·delta_rho (the supplied delta_rho) | L450 |
| the single callback | L454-457 |
| induced potential = c_light²·lapse_component['delta_n'] | L470 |
| dPhi = angular_forcing_dPhi + induced (Phi0 never added) | L471 |
| Euler R: r0_R + Omega·dphi(w_R) − 2·Omega·w_phi + dR(deltaP)/rho0 − delta_rho·dR(P0)/rho0² + dR(dPhi) | L473-474 |
| Euler phi: Omega·dphi(w_phi) + (2·Omega + R·dR(Omega))·w_R + R·dz(Omega)·w_z + dphi(deltaP)/(rho0·R) + dphi(dPhi)/R | L475-476 |
| Euler z: r0_z + Omega·dphi(w_z) + dz(deltaP)/rho0 − delta_rho·dz(P0)/rho0² + dz(dPhi) | L477 |
| min(rho0+delta_rho), min(P0+deltaP), max\|delta_rho/rho0\| | L487-489 |
| total quadrature mass perturbation | L490 |
| all-slot angular norms | L346-369 (FFT at L352) |

dR, dphi and dz are only the mesh's `partial_R`, `partial_phi` and `partial_z`. They are captured once (L205) and wrapped at L406-425. Each wrapped call passes a read-only copy, runs under the caller's errstate, and requires a real finite output of exactly grid_shape. Every derivative that does not depend on the response is evaluated **before** the callback, so a malformed input never triggers the callback. Module arithmetic raises on divide, overflow and invalid; underflow is ignored.

## 3. Checks and conventions

- **Axisymmetry gate (L231-241).** For f in (rho0, K0, P0, Omega, Phi0), `dev = max|f[i,j,k] − f[i,0,k]|` and `ratio = 0 if dev == 0 else dev/max|f|`. The gate requires `ratio <= base_fields['axisymmetry_phi_variation_rtol']`. `angular_forcing_dPhi` is excluded because it is the angular forcing. A derivative test of the form max|partial_phi f|/max|f| would miss Nyquist content, because root zeroes the Nyquist slot in `partial_phi`; the fixtures confirm this blind spot. That ratio is still reported, but it is not gated.
- **Response schema (L246-329), matching root L147-168.**
  - Top-level keys must be exactly {native_response, lapse_component}.
  - native_response keys must be exactly {fields_complex, imaginary_norms, reality_bounds, unit_response_custody, scope}.
  - `fields_complex` must be a plain complex128 array with shape exactly grid_shape+(10,).
  - All 10 fields must be finite, with real and imaginary parts checked separately per field.
  - `imaginary_norms` and `reality_bounds` must each be finite float arrays of shape (10,), with values ≥ 0.
  - `unit_response_custody.source_convention` must be `'unit_positive_lapse_e_n_full_signed'`, and `scope` must be a nonempty string.
  - lapse_component keys must be exactly {form, delta_n}, with form `'weak_field_delta_n'`. `delta_n` must be finite float64 of grid_shape and must equal `fields_complex[...,0].real` bitwise.
  - **Reality:** `np.linalg.norm(fields.reshape(-1,10).imag, axis=0)` must equal the declared `imaginary_norms` bitwise, which is the root L163 computation on the same array. Root's own rule, imag ≤ bound per field, is then applied. The bounds are taken as declared, because root's atol and rtol are not returned.
  - Imaginary parts are never discarded. The potential uses root's own `delta_n = Re(field 0)`, and `field0_imaginary_norm` is reported.
- **Angular norms.** These follow the 0431 convention: `F = np.fft.fft(a, axis=1)/nphi` over **all** nphi slots, signed m = s for s ≤ nphi/2 and s − nphi otherwise, with an unweighted l2 over the (R, eta) nodes. The report gives the per-slot l2, per-slot max, `all_slots_l2` and `nodal_l2_over_sqrt_nphi` (the Parseval match is reported, not gated). It covers the three Euler components and also continuity, entropy and EOS. Values are evaluated with max-abs scaling, so finite large residuals do not overflow (0431 check N1).
- **Quadrature weights.** The mass uses `mesh['volume_weights_m3']` exactly as root builds it (L70-71): `wr[:,None,None]*(2*pi/n_phi)*H[:,None,None]*we[None,None,:]`. The factors are the supplied R dR radial weights, the uniform angle weight, the half-thickness H = (upper root − lower root)/2, and the eta Gauss weights. The mass is `float(np.sum(volume_weights_m3*delta_rho))`, the same form as root's `constraint_rows` (L121). No metric or source-measure correction is applied.
- **No thresholds and no acceptance.** No result is clipped, corrected, iterated or calibrated. `status` is always `'not_assessed'`. A negative min(rho0+delta_rho) is reported as it is.

## 4. Missing interface facts (0433 is silent; the explicit choices made here)

1. **Axisymmetry tolerance and test.** 0433 gives neither. The tolerance is required as `base_fields['axisymmetry_phi_variation_rtol']`; there is no module constant. The test is defined in §3. Root must add this key, and the name is deliberately different from 0427's `base_axisymmetry_rtol`, which is a derivative ratio.
2. **Which base fields must be axisymmetric.** This module uses rho0, K0, P0, Omega and Phi0. angular_forcing_dPhi is excluded.
3. **`provenance` type.** It must be a nonempty `str`.
4. **Response key sets.** They must equal root v002's exactly, so any extension by root fails closed.
5. **Declared reality results.** Bitwise agreement between the declared and recomputed imaginary norms is required. Root's atol and rtol are not returned, so the bounds cannot be recomputed.
6. **Imaginary part of field 0.** 0433 and 0427 assign it no physical role. It is retained and bounded by root's rule, but it is not used.
7. **Units.** The module uses a caller-consistent unit system (SI per root) and does not declare one. `c_light` must be in the same system as delta_rho→delta_f_n.
8. **Polytrope relation.** 0433 does not require P0 = K0·rho0**gamma. The mismatch is reported (`polytrope_max_relative_mismatch_reported_not_gated`) and not gated. The EOS discrepancy is a linearization only about such a base.
9. **phi residual.** It has no r0_phi term, as 0433 writes it, and r0_phi = 0 by the 0433 formula.
10. **Input dtypes.** Float (≤ 8 bytes) and integer dtypes are accepted and copied to float64. Bool, complex, object, masked and list inputs are rejected.
11. **Mesh layout facts used.** These are root guarantees that are re-checked here: R depends on the R axis only, the phi nodes match the bitwise expression, nphi is even, and the weights are > 0.

## 5. Limitations

- These are strong pointwise residuals of the supplied state, computed through root's finite derivative rules. They do not show that a weak or conservative discretization makes them zero, and they are not a nonlinear acceptance test. They give no continuum-derivative, boundary or angular-tail certificate.
- Root's `partial_phi` zeroes the Nyquist slot. Nyquist content in the perturbations is therefore invisible to the dphi terms, although it does appear in the slot norms.
- The module computes no boundary rows and no weak-form residual. It does not check mass or annular mass against any target.
- The ungated polytrope and dphi-ratio reports are computed before the callback. An arithmetic overflow there fails the call closed, with zero callbacks made.
- The response is retained by identity, not copied. The caller must not mutate it afterwards.

## 6. Fixtures (stub only)

The fixtures are in `scratchpad/r0433/fixtures_0433.py`. They were run with `python3 -I -B` (Python 3.12.14, numpy 2.3.5) under a 90 s alarm, and the result was **105/105 PASS**.

- **Grid and inputs.** The grid is 7×16×5. The fields are polynomial in R and z times trigonometric functions of phi. Derivatives use Lagrange differentiation in R and z, which is exact for those polynomials, and root's formula for the FFT phi derivative.
- **Stub response.** It mimics root's output schema.
- **What the cases cover:**
  - closed forms for r0, all six residuals and dPhi;
  - a supplied m=0 w_phi, giving a radial Coriolis term −2Ω·w_phi;
  - zero fields;
  - the source sign, exactly one callback and no density recompute;
  - rejection of non-finite values in all 10 fields, including an imaginary-only NaN in a non-lapse field;
  - schema and reality rejections;
  - preservation of the response after a late derivative failure, a late NaN or a late overflow;
  - 28 input rejections with zero callbacks, including Nyquist non-axisymmetry;
  - norms checked against a direct DFT;
  - mass computed bitwise;
  - unclipped negative densities;
  - errstate left untouched;
  - inertness, checked through the AST.

The root binding and 0427 were never imported, and no project data was used.
