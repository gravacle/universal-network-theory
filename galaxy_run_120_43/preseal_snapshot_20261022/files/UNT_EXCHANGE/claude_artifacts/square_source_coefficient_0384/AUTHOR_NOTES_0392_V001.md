# 0392 author notes, V001: formation_frequency_coefficient_v001.py

Author: Claude helper (AUTHOR role). A different helper does the static review.

There is one public function, `formation_frequency_coefficient(*, ...)`. It takes 15 required keyword-only arguments, has no defaults, and has no ref_tol or imag_tol.

The module is self-contained. Its helpers are copied from the 0390 V002 modules, with nothing imported locally. No existing file in the directory was touched.

## Sources (sha256 from bytes)

| Source | Role | sha256 |
|---|---|---|
| FROM_CODEX/0392_2026-10-15_dynamic_formation_coefficient_implementation.md | formula authority | d004ad3d1bfe4b5b6599d7afd3919f3d94e2b65c8904feebf19cdaecb2c897c8 |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md (live; section at L768–791) | context | f287e487b50a4d14fdba7bec7e95331258a0261106fab8db057bb9a61905f565 |
| helpers/response_packet_audit/DYNAMIC_SINGLE_FLIP_HIGH_CONTACT_DISTINCT_REVIEW_V001.json | distinct review (PASS_SCOPED) | b0a9275dc8cfc81b51ddf8e7433294a99c570cddde28143ef0f0d190d7453b53 (matches the 0392 pin) |
| square_source_coefficient_v002.py (0390) | helpers copied: `_real_input`, `_complex_input`, `_tolerance_input`, `_local_block`, the eigensystem and residual block, the reference checks | e7741d4ec08640a66fff13045b6f92762208892c19d82bc8928e78a5f935fd43 |

## Spec-to-code mapping (v001 line numbers)

| 0392 item | Code |
|---|---|
| Signature (15 required keyword-only arguments, no defaults) | L173–190 |
| Finite real and complex admission; tolerances finite and ≥ 0 | L11–62; stage 1 L245–293 |
| z_values: list, tuple or 1-D array; 1–32 entries; finite complex; Im(z) ≥ 0; scalars and bools rejected | `_z_values_input` L65–95; L263 |
| r2 reported, any finite value admitted; mu0; delta as in 0390; g > 0; κ ≠ 0; delta > 0 | L295–317 |
| H(d) as in 0384/0390; complete eigh at d = 1, 2, 3 | `_local_block` L98–111; L319–339 |
| Hermiticity, eigen-residual and orthonormality checks; actual e2 and χ from H(2); gap > pos_tol | L341–380 (e2, gap, χ at L358–360) |
| q_a = \|Σ_i conj(U_d[i,a])·χ[i]\|² | L390–391 |
| w_ab = q_a·q_b | L392 |
| D_ab = 2Ud + 2σ·mu0 + E_a + E_b − 2e2 | L393–395 |
| All 16 D finite and > pos_tol (min D > pos_tol); \|Σw − 1\| ≤ resid_tol without renormalization; m_σ = min D | L410–429 |
| r_p = Σ w/D^p for p = 2, 3, 5, 7, by repeated division | L430–440 |
| \|z\| < m_σ for both σ, checked for every z before any F | L445–457 |
| F_σ(z) = 2Σ w/[D(D² − z²)]; F4_σ = 2(r3 + z²r5 + z⁴r7); bound_σ = 2\|z\|⁶/[m⁹(1 − \|z\|²/m²)]; finiteness | L459–498 |
| Complex outputs and exact z as {real, imag}; spectra, gaps, D, w, q, residuals, inputs, tolerances, failures, stage_reached | `_pair` L114–115; `_new_result` L118–170; reports L397–408, L486–498 |
| Units, scope (replace-or-add-difference rule; bound scope; no lapse shortcut) | L136–170; docstring L235–240 |

## Static identities (claims to be checked later, not run)

**1. F at zero frequency is the static contact.**
F_σ(0) = 2Σ_ab w_ab/D_ab³ = 2·r_3. Here r_3 = ⟨χχ|M_σ⁻³|χχ⟩ with M_σ = (2Ud + 2σ·mu0)I + K_u + K_v + σ(V_u + V_v), the 16-dimensional complete one-edge defect operator at j = 0. That holds because K + σV = H(2+σ) − e2·I, so the product eigenbasis of H(2+σ)⊗H(2+σ) diagonalizes M_σ with eigenvalues D_ab, and w_ab = |⟨u_a u_b|χχ⟩|².
- So h²·Δ_A·Δ_B·F_σ(0) = 2h²·Δ_A·Δ_B·r_{3,σ}, which is the existing static contact (assembly L313 and L768–791; review "static_limit").

**2. F4 is the Taylor expansion of F through z⁴.**
For |z| < D:
- 1/[D(D² − z²)] = D⁻³·Σ_{n≥0}(z²/D²)ⁿ = Σ_{n≥0} z^{2n}·D^{−(2n+3)}.
- Hence F = 2Σ_{n≥0} z^{2n}·r_{2n+3}.
- The terms n = 0, 1, 2 give 2(r3 + z²r5 + z⁴r7) = F4.

**3. The remainder bound.**
- F − F4 = 2Σ_ab w_ab·z⁶·D⁻⁹/(1 − z²/D²).
- For complex z, \|1 − z²/D²\| ≥ 1 − \|z\|²/D² > 0.
- The map x ↦ x⁻⁹/(1 − \|z\|²/x²) decreases for x > \|z\|, so each term is bounded by its value at D = m_σ.
- With w ≥ 0 and Σw = 1, this gives \|F − F4\| ≤ 2\|z\|⁶/[m_σ⁹(1 − \|z\|²/m_σ²)].
- This matches the review's "low_frequency" check. It bounds only this coefficient's frequency expansion.

**4. Weight sum.**
Σ_a q_a = ‖U_d†χ‖² = 1, so Σw = (Σq)² = 1 exactly in exact arithmetic. The resid_tol check tests the floating-point realization; the weights are never renormalized.

## Unresolved points

1. **Remainder bound and the weight sum.** The bound has no Σw factor, exactly as in 0392. Since \|Σw − 1\| ≤ resid_tol, the exact tail bound is the reported bound times Σw, so it can exceed the reported value by a relative amount of at most resid_tol.
2. **No source shift.** F has no source argument j (none was specified), so it is the j = 0 reference coefficient. Source derivatives of F are not part of this task.
3. **Evaluation at the exact z.** F is evaluated at the supplied z with no +i0 limit taken. For real z with \|z\| < m_σ the point is pole-free, so +i0 is immaterial there.
4. **Strict \|z\| < m_σ with no margin.** As \|z\| approaches m_σ the bound can become non-finite, which the finiteness gate rejects. One out-of-domain z fails the whole call, by fail-closed design, with no partial frequencies.
5. **Order of the denominator sums.** D_ab is evaluated as (2Ud + 2σ·mu0) + (E_a − e2) + (E_b − e2). That is the same formula as 0392 but a different floating-point summation order, chosen to avoid cancellation against 2e2.
6. **r_2 is reported but unused.** It is reported as 0392 requests, but neither F, F4 nor the bound uses it.
7. **Graph factor not applied.** The factor h²·Δ_A·Δ_B is not applied, as 0392 directs. F already contains the factor 2.
8. **Inherited from the 0384/0385 reviews.** Thread pinning for eigh at launch, and the tolerance forms and units.

## Working arrays

- Three 4×4 complex blocks and their eigensystems.
- Per σ: one 4-element overlap, and 4×4 tables q⊗q, D and t (16 entries each).
- At most 32 frequencies × 2 σ evaluations of 16-entry tables.

There is no 16×16 or larger matrix and no sweep, so total work is negligible.

## Execution statement

The module was never executed or imported, and no tests, examples or numerical calls were run. The only Python run on it was AST parsing:
- `ast.parse`;
- a walk listing einsum calls with their keyword arguments, MatMult nodes, forbidden attributes (dot, matmul, errstate, seterr, warnings and similar), I/O names, defaults and the signature.

The walk found 7 einsum calls, all with optimize=False, and nothing forbidden. The source JSON was read with a `python3 -I` printer.

The file was drafted in the session scratchpad and then created here exclusively. No network was used, and nothing was written under /Users/bgm/Research/Universal Network Theory.
