# 0384 author notes, v001

Author: Claude helper (AUTHOR role). The independent review is by a different helper.
Artifact: `square_source_coefficient_v001.py` in this directory. It contains one public function, `square_source_coefficient(*, ...)`, which has keyword-only required arguments and no defaults.

## Sources (sha256 computed from bytes at authoring time)

| Source | sha256 |
|---|---|
| FROM_CODEX/0384_2026-10-15_square_source_coefficient_inert_implementation.md | cc991dab500b1d02bb201aad3a747290952337cf5c509aedf19d3e6d6692e1a3 |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md (read-only; sections at L357–408 and L469–520) | a59ad09218d35a0eec8e0f5670803b9b1c694ad84935e55ed0367291a53e7a1f |
| FROM_CLAUDE2/0064_2026-10-15_0372-item1-birth-ingredients.md (context) | 6277558b800d2cb0c93c6a27f510766a00406ec1515c1640cea03e6721188987 |
| FROM_CLAUDE2/0065_2026-10-15_0372-item2-local-block-done.md (context) | eb07250adb3abcdc493baa90ab5ddd4ab3eddabe16fcb8a04d55b3efaaaf8871 |

## Spec-to-code mapping (line numbers in v001)

| Spec item (0384 / brief) | Code |
|---|---|
| Inputs: finite real ×11, complex kappa, explicit tolerances, no defaults | signature L203–221; admission helpers L10–61; stage 1 L278–330 |
| r2 = epsilon_r − 2 lambda_R, \|r2\| ≤ ref_tol; g > 0; kappa ≠ 0 | L334, L347–352 |
| mu0 = Delta/2 + 2 Ud (2 − dstar); delta = Ud − max(\|mu0\|, \|mu0+λJ\|, \|mu0−λR\|, \|mu0+λJ−λR\|) > 0, reported | L335–345, L353–354 |
| H(d) in basis (A0,A1,B0,B1), r_d = epsilon_r − λR d | `_local_block` L64–77; built for d = 1,2,3 at L360–364 |
| Diagonalize H(1), H(2), H(3) once, all four pairs kept | `eigh` L369; stored L376 |
| Hermiticity, eigen residual max\|Hv − vw\| (einsum), local gap, chi, e2 | L380–416 (residual einsum L388; gap L398; chi L399) |
| V identity H(2+a) = H(2) + aV: static note only | `static_notes` L186–196 |
| Cycle edges, bits (1,0,1,0), sigma = (−1,+1,−1,+1) | L423–428 |
| a_i(S), D(S), c(S,j) = Ud D + mu0 Σa − 4 j D | L431–443 |
| Kronecker-sum denominators c + Σ_i (w_{2+a_i}[k_i] − e2), shape (4,4,4,4) | L444–451 |
| Every used denominator > pos_tol before inversion; minimum tracked | L465–473, L483–486 |
| Cache ≤ 14 subsets (a, D, den, local U blocks) | L474–480 |
| R_S f: conj(U)^T per site, divide, transform back with U | `_site_apply` L80–92, `_to_eigenbasis` L95–100, `_from_eigenbasis` L103–108 |
| R' = 4D R², R'' = 32 D² R³ as repeated division; exact product rule | `_apply_resolvent_with_derivatives` L111–139 |
| 24 permutations, prefixes S1, S2, S3, with S1 acting first | `_orders` L142–151; L492–514 |
| D(S1)=2, D(S2)=2 adjacent / 4 disjoint, D(S3)=2, checked before any inversion | L508–513 |
| psi = chi⊗4 (axis i = vertex i); start (psi, 0, 0); contract with conj(psi); sum over 24 | L528–544 |
| Imag check \|Im\| ≤ imag_tol·max(1,\|Re\|); real positive; max imag reported | L559–576 |
| Outputs: J, Jprime, Jsecond (only if ok), raw sums, diagnostics, counts, D values, declared inputs/tolerances, units, failures, scope | `_new_result` L154–200; L556–584 |

## 0384 compared with the assembly section

No formula conflicts were found. Both sources give the same H(d) matrix, r_d, the D sequence (2, 2 or 4, 2), the −4 j D source shift, and R' = 4D R², R'' = 32 D² R³. The assembly's single-edge d_σ = 2Ud + 2σ mu0 and its −8 j shift for that edge are the D = 2 case of 0384's scalar c(S, j). The differences are wording only:
- Names: the assembly uses e_− and J_square; 0384 uses e2 and J.
- The assembly writes M_k(j) = M_k − 4 D_k j I with M_k given in words. 0384 gives M_S(j) explicitly, and that explicit form is implemented.
- The assembly derives positivity from a stoquastic gauge "in the common positive-inverse window". 0384 says J, J', J'' are real and positive "in the stated domain". The code works in the ungauged basis, where the contraction is gauge invariant. It checks positivity and does not assume it.
- The assembly's mixed-coefficient section writes delta = Ud − ‖mu0 I + V‖. With V diagonal, this is 0384's explicit max over four terms.

## Working-array sizes

- Tensors: (4,4,4,4) complex128, 4 KiB each. One resolvent step holds about 20 such tensors at once (≈ 80 KiB).
- 14 denominator arrays: (4,4,4,4) float64, 2 KiB each, 28 KiB in total.
- Three 4×4 eigensystems.
- Each einsum is either 4×4 by (4,4,4,4) (1024 multiply-adds), the 4-operand outer product for psi (256 outputs), or the 256-element bra–ket contraction.
- No 256×256 matrix is ever formed. Total work is about 2×10⁶ multiply-adds. Prefix results are recomputed per history rather than shared, which is simple and exact.

## Choices beyond the literal text (for the reviewer)

1. **Added check:** an eigenvector orthonormality residual max|U†U − I|, gated by resid_tol. The back-transform relies on U being unitary.
2. **Used denominators:** all 256 eigenvalues of each of the 14 M_S(j) count as "used", whether or not psi overlaps them.
3. **Strict comparisons:** delta > 0, g > 0 and Re X > 0 use 0 as the threshold, as the spec states. pos_tol applies only to denominators and the local gap. kappa ≠ 0 is an exact comparison.
4. **Absolute tolerances:** residual and Hermiticity tolerances are absolute, not scaled by ‖H‖. Tolerances must be finite and ≥ 0.
5. **Input admission:** numbers must be Python or NumPy scalars. Booleans, 0-d arrays, strings, and complex values for real inputs are rejected and never coerced.
6. **Per-history imaginary parts:** these are reported (max_abs_imag_single_history) but not gated. The spec gates only the three sums.
7. **Complex values in the output:** they are reported as (real, imag) tuples, so the result is JSON-friendly.

## Unresolved points

- Whether delta should be compared against pos_tol rather than 0. The literal ">0" is implemented.
- Whether J positivity should require exceeding a tolerance instead of being strictly > 0.
- The units of j are not stated. The derivative units imply j ~ E, and only the J units from the spec are emitted.
- With r2 ≠ 0 inside ref_tol, H(d) uses the given epsilon_r as is. Nothing is projected to r2 = 0.

## Execution statement

The module was never executed or imported, and no tests, numerical examples or calculations were run. The only tool applied was the permitted `python3 -I -B -c "import ast,sys; ast.parse(open(sys.argv[1]).read())"` syntax check, which passed. It was drafted in a session scratchpad and then exclusively created here. No network was used. Nothing was written under /Users/bgm/Research/Universal Network Theory.
