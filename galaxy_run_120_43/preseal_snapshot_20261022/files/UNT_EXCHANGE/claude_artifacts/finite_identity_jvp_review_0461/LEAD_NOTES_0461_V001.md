# LEAD_NOTES_0461_V001 — Claude4 lead facts gathered during the 0461 review (working notes, not the verdict)

UTC 2026-10-17, about 12:55Z. Reviewed bytes, all cmp-equal to the live files:

| File | SHA-256 |
|---|---|
| core | cfb988f4707d2296026174295802296b2d83b0bda873d67d4fe950f88d13d554 |
| driver | 2b89fa0cab9a8f4213e2d7eab60d6fa18c11b02455378cbad6c9f17029bda4e7 |
| INPUTS | d0c194f07f55c7b89444fbbd651c81712796628149cdda2f93cda9b8f7e40ecb |

## Verified directly by the lead

1. **B1: unfrozen input pin.** Driver L13 reads `INPUTS_SHA = 'TO_BE_FROZEN'`, and L59 checks the manifest against it. Every launch fails at stage `admission` with a pin mismatch.
2. **B2: scipy import.** Core L9 has `from scipy.special import jv` at module level. No interpreter here has scipy:
   - the root runtime has numpy 2.3.5 only;
   - `/usr/bin/python3` has none either.

   Driver L63 loads the core, so the run fails at `admission` with ModuleNotFoundError. `jv` is used only at L82, in `material_source_identity_jvp`, which the driver never calls.
3. **Fourier sign convention.** The 0455 scalar module `exact_scalar_force_c2v001.py` (0dab62be…) declares in CONVENTION, L59-60: `dn = SUM_j a_j exp(i k_j.x)` and `grad dn = SUM_j (i k_j) a_j exp(i k_j.x)`. The driver's amplitude `1j*k_c*total` (L135) therefore yields d/dx_c of the lapse, and its gradient gives the Hessian column. The sign is correct.
4. **JSON safety.** Scalar-module counts are Python ints:
   - `_positive_int` requires `type(value) is int` (L119-122);
   - the tallies accumulate `phase.size` and ints (L458-494).

   The driver's `write()` and `progress()` have no `serial()` conversion, but they are safe on this path.
5. **Mode order.** FINITE_MATERIAL_INPUTS_V001.json lists modes as [1,2,3,4,5,6] in order. The finite worker's positional `mi+1` (v002 L309-L317) and the driver's declared `mode['mode']` (L184-L193) therefore agree. Secant keys `m1..m6` match.
6. **Test identity.** Driver m0 tests (L149-L163) are line-for-line identical in meaning to the finite worker's (v002 L286-L299):
   - radial uses the core's `axisymmetric_radial_tests`;
   - azimuthal `W_phi = R h V`, with `D_phiR = (h+R h')V + R h V_R`, `D_phiz = R h V_z` and `D_Rphi = -h V`;
   - vertical `W_z = h V`.
7. **Core algebra spot-check by the lead.**
   - `k = (F t).(conj(DW) t)` holds exactly for every F, because `F^-1 F t = t`. Hence `dk = (G t).(conj(DW) t)`. The algebra review's three-term kdot collapses to this.
   - Pressure: `(2/3) P0dV0 tr G tr conj(DW) + P0dV0 tr(conj(DW) G)`.
   - Force: `c^2[grad dN/N - gradN dN/N^2] + c^2[H xi/N - gradN (gradN.xi)/N^2]`.
   - Speed solve: `H ds_dot = Rdot|S*`, consistent with the original `H ds = d` sign.
   - Sigma: `2 a_xy.xi_xy/L^2 * b'(s)`, using `_spline_matrices(...)[1]`, which is d/ds.
   - Conjugation: once each, on DW (L171) and W (L184).
8. **Interpretation notes for root.**
   - The `m0_radial` tangent-versus-secant comparison is noise-dominated by construction. Both sides reduce to the algebraic residuals of the speed solves.
   - For a pure m=1..6 candidate direction, `Hdot`, the Sigma JVP and the m0 kinetic and pressure parts vanish by symmetry. The real call exercises them little; see the J5 note.
   - The finite secant uses the 256-angle finite source, while the tangent uses the 128-angle identity derivative. The two differ at about 1e-15 relative, which is negligible.
9. **Missing packaging.** There is no monitor or launch recipe for this driver. The wall check runs only inside `progress()`, and there are no RSS or output caps (J3 to confirm).

## J5 supplement (finite_identity_jvp_review_0461/J5_supplement/): PASS 152/152

- **T1: manufactured closed-form case.** 35/35 pass. Worst relative error 9.3e-15.
- **T2/T2B: 4th-order finite differences of the actual finite residual.** 41+41 pass. Order 4.00, then a roundoff floor of about 1e-13 to 1e-12. Nine seeded errors were caught at relative error ≥0.38 against a 1e-9 threshold.
- **T3: failure behaviour.** 9/9 checks over 442 bad inputs. Each raises ValueError with no partial return and no input mutation.
- **T4: Bessel source against the tensor source.** 1.3e-15 at 64 angles and 1.7e-15 at 128. All six 2π/sign mutants were detected. The angular bound holds strictly at the driver's strip widths.
- **D2 (minor, latent).** The memory envelope of `material_source_identity_jvp` (L62-L64) omits the L85 temporaries and the L68 buffer. It underestimates by 1.09-3.76x when kz greatly exceeds the ring count. That function is not on the driver path.
- **Notes.**
  - A non-symmetric Hessian is accepted; symmetry is only reported at driver L205.
  - Empty point or ring sets return zeros.
  - The J7(10) reference in Claude4's prompt was wrong in the tenth digit; the exact value is 0.21671091768505152. This was a lead error, harmless.

## L1 Eulerian cross-check (finite_identity_jvp_review_0461/L1_eulerian_crosscheck/) and its verifier (L1_verify/): PASS (scoped), every claim CONFIRMED
- The identity-residual transport (xi.grad)rhat0 is counted exactly once. The fitted multiplicity is λ = 1 − 2.8e-15. The transport makes up 53% of DR, so dropping it or doubling it misses by 0.5323.
- Material route vs independent Eulerian strong form, relative L2 error by resolution: 2.31e-3 → 6.0e-6 → 3.1e-9 → 3e-15 (converged). The whole gap comes from the pressure integration by parts, as derived.
- Toy source coupling: agreement 3e-15. The material source matches −div(rho0 xi) to 4.4e-15. Trapezoid vs Bessel agree to 4.4e-15 at nphi ≥ 24, and 2π is counted once.
- The verifier's code mutants were all detected at 0.09–9.3: transport dropped or doubled, force source instead of total, Dxi transposed, pressure sign, γ in place of γ−1, inverse-F term dropped, S-elimination sign, missing conjugate. A hand-checked point with exact rationals matches exactly.
- Driver path with a solved Sstar (45% away from S0): matches finite differences to 2.8e-12. Using S0 instead misses by 3.8e-2; skipping speed elimination misses by 7.1e-2.
- Advisories:
  - (1) The spec's Eulerian delta_v uses Omega0. With base S = Sstar, use sqrt(Sstar).
  - (2) The interior identity requires reference P0 → 0 at the z-ends, because the tests vanish only at R=L. Checking this needs project arrays, so root should check P0 on the outermost z rings.
  - (3) Gate on F3_gradient_replay (driver L205). A Fourier-sign mismatch would silently flip the gravity part of the transport. The sign is correct by the 0455 convention, but nothing enforces it.
  - (4) Add a mass-consistency gate, bincount(q, geo['mass_kg']) == ringmass. A uniform 2π error would leave the JVP and the S solve unchanged but bias the Sigma moments.
  - (5) The radial-family relative tangent/secant metric is noise-dominated after speed elimination.
