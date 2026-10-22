# REVIEW 0427: equations, units and signs (V001)

**Role:** distinct reviewer, not the author. I did not write or edit the module, the interface note or the author's fixtures.
**Date:** 2026-10-16
**Verdict: PASS_WITH_NOTES.** There are no blocking issues. Every formula in spec sections 3-4 is implemented with the exact terms and signs. The units are consistent, and the forcing partition enters each contribution exactly once.

## 1. Bytes verified (sha256 recomputed from bytes; all match)

| item | sha256 |
|---|---|
| Task 0427 `FROM_CODEX/0427_2026-10-16_reviewed_noncircular_fluid_operator_implementation.md` | `1e9e7cfb4be32cae313543374edb76c647a14530720cb276c83f6e464e95c164` |
| Spec `DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt` | `d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4` |
| Equation review `NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json` | `99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e` |
| Context `galaxy_coupled_fourier_hi_prediction_v006.py`, read as text only (lines 59-82, 171-190) | `e0d0888de2487c9de1346b4268c0ef9c12401965134333741b389bb3a5cdca79` |
| Context `owned_physical_fourier_metric_quadrature_v004.py`, read as text only (docstring source convention) | `61dc1369726413cda55e87b6175adccce095c65495cb3d94afbff1b50a255582` |
| **Reviewed** `ddo_noncircular_displacement_action_c2v001.py` | `6b4f2cc6ee0e0c1a4408e555004b510d2d11058bc6f3e9cc82f6ce697ef9e482` |
| **Reviewed** `INTERFACE_0427_V001.md` | `1c34edf3fce32f7705382d9f1b802ec2d53ad6b097c57b4fad4bff64af4b60eb` |
| Author fixtures (scratch, not re-run) `r0427/test_0427_algebraic_fixtures.py` | `89e20cb76a529a920d69ea69b736f9b4fff72e12024dd32fb15eb01d8d67d8b6` |

The author's scratch copies of the module and the interface are byte-identical to the published files. I did not open the DDO154 run packet or any observation or calibration data, and I wrote nothing under `Universal Network Theory`.

## 2. Hand check against spec s3-s4 and the distinct equation review

Components are physical orthonormal cylindrical, with v0 = R Omega(R,z) e_phi and d_phi taken per radian.

| quantity | spec | code (line) | hand result |
|---|---|---|---|
| divergence | -div(rho0 xi), with 1/R | `dR(R rho0 xi_R)/R + dphi(rho0 xi_phi)/R + dz(rho0 xi_z)`, drho = -div (347-351) | correct. The conservative form carries the R factor inside d_R, and the product rule is applied to the caller callbacks through the product arrays. |
| dK | -xi.grad K0 | `-(xi_R K0_R + xi_phi K0_phi/R + xi_z K0_z)` (352) | correct, including the physical azimuthal gradient 1/R |
| dP | cs2 drho + rho0^gamma dK, cs2 = gamma P0/rho0 | 346, 353 | correct. From P = K rho^gamma, dP = rho^gamma dK + gamma K rho^(gamma-1) drho. |
| dv_R, dv_z | Omega d_phi xi_R, Omega d_phi xi_z | 357-358 | correct |
| dv_phi | Omega d_phi xi_phi - R(Omega_R xi_R + Omega_z xi_z) | 359 | correct (see derivation below) |
| radial Euler | Omega d_phi dv_R - 2Omega dv_phi + d_R dPhi + d_R dP/rho0 - drho P0_R/rho0^2 + r0_R | 424-427 | every term and sign matches the spec (residual = LHS - RHS) |
| angular Euler | Omega d_phi dv_phi + (2Omega + R Omega_R) dv_R + R Omega_z dv_z + d_phi dPhi/R + d_phi dP/(rho0 R) + r0_phi | 428-432 | matches |
| vertical Euler | Omega d_phi dv_z + d_z dPhi + d_z dP/rho0 - drho P0_z/rho0^2 + r0_z | 433-435 | matches |
| source | df_n = -c^2 drho, one call | 367, 373 | sign matches spec s4; the response is called exactly once, after all static and base checks |
| induced potential | c^2 x lapse component | 404 (c^2 delta_n), 414 (c^2 delta_N/N0) | matches both review qualifications. Neither form is chosen silently: the declared and returned forms must agree. |
| total potential | angular forcing + induced, each once | 416 | correct |

**Lie bracket (dv).** I used the cylindrical convective derivative with connection terms:
- (v0.grad)xi = (Omega d_phi xi_R - Omega xi_phi, Omega d_phi xi_phi + Omega xi_R, Omega d_phi xi_z)
- (xi.grad)v0 = (-Omega xi_phi, xi_R(Omega + R Omega_R) + R Omega_z xi_z + xi_phi Omega_phi, 0)

Their difference gives the three dv components as coded. The difference also contains a term -xi_phi Omega_phi, which vanishes for the axisymmetric base the spec assumes.

**Linear Euler.** (v0.grad)dv + (dv.grad)v0 gives:
- R component: Omega d_phi dv_R - 2Omega dv_phi
- phi component: Omega d_phi dv_phi + (2Omega + R Omega_R) dv_R + R Omega_z dv_z
- z component: Omega d_phi dv_z

Linearizing -grad P/rho gives -grad dP/rho0 + drho grad P0/rho0^2. All of this agrees with the code and with the five findings in the distinct equation review.

**r0 sign.** The residual is LHS - RHS. Because the spec puts -r0 on the RHS, r0 = (v0.grad)v0 + grad Phi0 + grad P0/rho0. INTERFACE s4 states this, and it is consistent with the spec s2 equilibrium: r0_R = P0_R/rho0 + Phi0_R - R Omega^2. The residual sign also agrees with the v006 diagnostic convention, `euler = grad lnN + grad P/(eps+P) - centripetal`, which is the same LHS - RHS orientation divided by c^2.

**Units (SI shown).**
- c^2 drho is in J m^-3. This matches v004, where source columns are ∫dV e^{-ik.x} of energy-density sources, which gives J.
- c^2 delta_n is in m^2 s^-2.
- Every Euler term is in m s^-2:
  - Omega d_phi dv: s^-1 · m s^-1
  - d_R dP/rho0: Pa m^-1 / (kg m^-3)
  - drho P0_R/rho0^2
  - d_phi dPhi/R
- rho0^gamma dK and cs2 drho are both in Pa.

The docstring and INTERFACE unit lists are correct.

**Forcing partition (exactly once).** The module accepts only `r0=projected_base_residual;dPhi_total=angular_forcing+induced_feedback`. It rejects, with the response never called:
- a full saved-field r0, including the spec's alternative partition
- induced feedback declared in r0 or in the forcing
- forcing that includes the m=0 projection
- missing or extra keys, and non-bool flags

Structurally, forcing, induced feedback and r0 are each added once (lines 416 and 424-435).

## 3. What I executed (distinct methods; NONPHYSICAL algebraic fixtures only)

I ran these under the isolated runtime `codex-primary-runtime python3.12 -I -B` (Python 3.12.14, numpy 2.3.5). The grid was 28×16×20, R in [1,2] and z in [-0.5,0.5], with my own Chebyshev-Lobatto R/z and FFT-phi callbacks. The base was synthetic, polytropic with gamma = 5/3, and had vertical shear: Omega = 1.3 - 0.4R + 0.25z + 0.1Rz^2. No project data, run, target velocity, network or install was involved. Files are in `scratchpad/r0427-eq/`.

| file | sha256 |
|---|---|
| `review_0427_eq_fixtures.py` | `a56c511ed9b08088b872194adf8de1ad5fee898b6fb927c1a467690823a8b4cd` |
| `run1.txt` (71/71 PASS) | `8fe6024928ed8538ca398b3c3e7c5e1efcb98cfc0d6c32fb9d45230529c0bec0` |
| `run_mutants.py` / `mutants_run.txt` (21/21 detected) | `cc6fe7f6be8c51d6f29f68bcc050a59f58dfb71b762db5b211053ee21482e471` / `4ed2f2e91d0330a17606ef9c2abbbec15373b65e6cb85d4f6e99f889eb7b8093` |
| `run_mutants2.py` / `mutants2_run.txt` (6/6 detected) | `8bb49785bccc506963374376f7281c4210ee720e9de40cf0b0ef39a1b74b6abb` / `e34324d58415fc6d40b0d92d80eb466a7752f7e68b53d2250b9e0a993ef64448` |

- **T1, rigid-motion covariance** (19 checks). The displacement is xi = a + w × x, with all six generators nonzero. Rotation and translation covariance requires the Euler acceleration E = (v.grad)v + grad P/rho to change by exactly -(xi.grad)E0 + w × E0. This reference uses only the closed-form E0 and a directional complex step. It uses neither the Lie bracket nor the linear Euler formulas.
  - Fluid-only residuals agree to ≤3.0e-10.
  - The full residual, with a nonlocal stub feedback, analytic angular forcing and r0, agrees to ≤2.3e-10.
  - drho, dK, dP and dv agree to ≤1e-12, and lagrangian_dP = 0 (4e-13).
  - The response was called once, and the native response was retained by identity.
- **T2, nonlinear Lagrangian pushforward** (13 checks). The xi is a non-rigid cubic polynomial, and xi_z depends on phi, so the -R Omega_z xi_z and R Omega_z dv_z terms are active (≈4e-2). The pushed-forward state is rho0/detJ, K0 and J v0 at y = x + eps xi. I evaluated the full nonlinear E in Lagrangian coordinates, took a central eps-derivative (eps = 1e-5), and subtracted the advection (xi.grad)E0.
  - The module's three residuals match to ≤3.8e-10.
  - drho, dP and dv match the pushforward to ≤3e-13.
  - The continuity and entropy identities are 1e-13 and 5e-17.
  - Flipping the vertical-shear sign as a negative control was detected (0.79).
- **T3, rigid rotation about z (neutral mode).** All perturbations are exactly 0. At xi = 0 the residual equals grad forcing + r0 (≤2.3e-13).
- **T4, exact ln N form.**
  - dPhi_induced = c^2 delta_N/N0, exact to the bit.
  - The response received -c^2 drho bitwise.
  - The feedback enters only as d_R dPhi_induced.
  - A declared exact form with a weak callback is rejected.
- **T5, unit-rescaling covariance.** I reran the identical configuration in kpc/Myr/Msun-like units. Every output (drho, dK, dP, dv, delta_f_n, dPhi, the three residuals) converted by its own dimension factor to ≤8.1e-11. There are no hidden constants.
- **T6, contract spot checks.** 21 forcing-partition and validation rejections were all fail-closed with exactly 4 keys and zero response calls. 4 bad-response rejections were caught. Supplied-mode analytic base derivatives equal callback mode (5.8e-11).
- **Mutants.** I planted 27 single sign/factor errors in scratch copies, and all 27 were detected. They covered:
  - each Euler term and Coriolis factor
  - (2Omega ± R Omega_R), R Omega_z dv_z, -R Omega_R xi_R and -R Omega_z xi_z
  - the divergence R and 1/R factors, cs2's gamma and the rho0^gamma power
  - the dK sign and the source sign
  - c versus c^2, and N0
  - the r0 sign, the forcing dropped, and the induced feedback double counted

I did not re-run the author's 93-check suite. I did read the module source in full: it performs no I/O, and its top level holds only imports, constants and definitions.

## 4. Blocking issues

None.

## 5. Notes (non-blocking)

1. **Axisymmetric-base terms.** dK and lagrangian_dP keep the K0_phi and P0_phi terms. dv_phi drops -xi_phi Omega_phi, and the phi-Euler equation drops +drho P0_phi/(rho0^2 R) and dv_phi Omega_phi, as spec s3 does. All of these vanish for an exactly axisymmetric base. With base_axisymmetry_rtol > 0, the action departs from the true linearization at O(rtol). Root's choice of rtol bounds this, and admitting any non-axisymmetric base would need a new version.
2. **Lapse and native consistency.** The module cannot verify that `lapse_component` is the n component (index 0 of (n, C_Mandel6, mu3)) of the retained `native_response`. Root's adapter should derive it deterministically from the native output. This is INTERFACE missing fact 1.
3. **`induced_response_full`** is held by reference, so it is unmodified by the module but not snapshotted. A caller that mutates the object after return changes the record.
4. **`unit_system` is a declaration only.** If it is not SI, the adapter must convert delta_f_n to v004's SI energy-density source units before the transform. T5 confirms the module itself is unit-agnostic.
5. **Weak versus exact lapse.** If N = 1 + n, the two forms differ by the factor N0, which is weak-field order and consistent with the review qualification. Both forms are explicit, and the choice is Root's (missing fact 3).
6. **Derivatives of dPhi_total** (forcing and induced) go through the caller callbacks, not through the analytic gradients that the prepared fields or response may carry. This is consistent with the task. Accuracy near the radial and free-surface boundaries is Root's (missing fact 6).
7. **Units of the residual.** It is in acceleration units. The v006 Euler diagnostic is the same orientation divided by c^2, in inverse length. Rescale before any cross-comparison.
8. **Author's line map.** The author's equation-to-line map (346, 347-351, 352, 353, 357-359, 360, 367/373, 404/414, 416, 424-435, 436-450, 342-343, 453-455) matches the published file.

## 6. Scope

This review covers only equations, units, signs, the forcing partition and the source-feedback contract. It is not a solve, base construction, boundary realization, resonance analysis or physical adoption. It also does not establish that a stationary state exists.
