# 0397 author notes, V001: scalar_metric_particular_solve_v001.py

Author: Claude helper (AUTHOR role). A different checker does the review.

## Sources (sha256 from bytes, verified)

| Source | sha256 |
|---|---|
| FROM_CODEX/0397_2026-10-15_scalar_metric_particular_solver.md | cf985f80a391d0d0ebb16935186a7a0d0e9ad9dc820823aabb20df0ba5179845 |
| helpers/coefficient_method/EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_PROPOSED_V001.md (frozen formula) | f5e28809a8ac24212d1d30bf6be92ab0d064407ae139f72f5146334c86308dd7 (matches the 0397 pin) |
| helpers/response_packet_audit/EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_DISTINCT_REVIEW_V001.json (PASS_SCOPED, no mandatory corrections) | 24b92a87e20568b6d934469ea2f91d28433a0c5c275d9c12a17482fe0fe7ba49 (matches the 0397 pin) |

## Source versus 0397: no discrepancy

- **K0.** The source has K0 = (4πG_EH)⁻¹[[0, −k²], [−k², k² − 3z²]] for q = (n, ψ). That is identical to 0397, including the q ordering.
- **Sign.** The source writes K0 q = −F_b, and with retained fields (K0 + Pi_eff) q = −(F_b + ell_eff). Its Dyson form is G = −(K0 + Pi_eff)⁻¹ and q = G(F_b + ell_eff) + q_hom.
- **What that means for F_eff.** F_eff in 0397 equals F_b + ell_eff, and the particular solution is −A⁻¹F_eff, as 0397 states.
- **Remaining conventions.** The source's c = 1, signature (−+++), Fourier exp(−iωt + ik·x) and z = ω + i0 are recorded in `sign_convention`.

Nothing needed flagging.

## Spec-to-code mapping (v001 line numbers)

| 0397 item | Code |
|---|---|
| numpy only; inert; one public function; keyword-only arguments, all required | L7; L154 |
| k finite real > 0; z finite complex with Im ≥ 0; G_EH finite real > 0; cond_tol finite real > 0; bools rejected | `_real_input` L10–28, `_complex_input` L31–50; L199–212 |
| Pi_eff 2×2 and F_eff length 2, finite complex; wrong shapes rejected | `_complex_matrix2_input` L74–97, `_complex_vector2_input` L53–71; L202–203 |
| Inputs echoed | L213–220 |
| K0 = (4πG_EH)⁻¹[[0, −k²], [−k², k² − 3z²]]; A = K0 + Pi_eff, not symmetrized or made real | L224–241 |
| Solve A q = −F_eff with numpy.linalg.solve; LinAlgError reported as singular; non-finite q is a failure; no pinv or regularization | L243–254 |
| Residual A q + F by einsum(optimize=False); 2-norm; relative to \|F\| and ‖A‖₂\|q\| | L256–260, L271–285 |
| cond₂ from numpy.linalg.svd(compute_uv=False), a LAPACK call rather than a matmul | L262–269 |
| Ill-conditioning: flag only | L290–296 |
| Return dict with {real, imag} pairs, units, sign convention, scope, failures and ok | `_new_result` L113–151 |

## Choice: ill-conditioning is a flag, not a failure

0397 asks for ill-conditioning to be "surfaced explicitly", with the tolerance "supplied or reported rather than selected as a physical acceptance rule". Making cond₂ > cond_tol fail the call would turn cond_tol into an acceptance rule. So the module does this instead:
- sets `ill_conditioned = True`;
- appends an explicit entry to `flags`;
- reports cond₂ next to cond_tol;
- leaves `ok` unchanged.

Exact singularity is still a failure, through LinAlgError. When s_min = 0 but the LU solve did not raise, cond₂ = inf and the case is flagged.

## Unresolved points

1. **Requirements on cond_tol.** cond_tol must be finite and > 0. There is no ≥ 1 requirement, even though cond₂ ≥ 1 always, so a cond_tol below 1 simply flags every call.
2. **Zero source.** With F_eff = 0, q = 0 and both relative residuals are None, because their denominators are 0. The call is still ok.
3. **What "singular" means.** numpy.linalg.solve (LAPACK gesv) raises only on an exactly zero pivot. Near-singularity is reported through cond₂ and the flag, not rejected.
4. **Two library routines.** svd is used for the 2-norm and cond₂, and solve for the system. Both are LAPACK routines, not matmul. Root's thread pinning applies as before.
5. **Real-axis z and singularity.** Allowing Im z = 0 on the real axis follows 0397's "or its boundary". K0 alone is never singular for k > 0, because det K0 = −k⁴/(4πG_EH)² does not depend on z. Singularity of A can therefore arise only through Pi_eff, and it is then reported.
6. **Caller responsibilities.** The caller must supply Pi_eff and F_eff consistent with the source's c = 1 normalization and the once-only EH/residual split. The module cannot check that.

## Execution statement

The module was never executed or imported, and no tests or examples were run. The only Python run on it was AST parsing:
- `ast.parse`;
- a walk listing module-level nodes, imports, the solve, svd and einsum calls with their keyword arguments, forbidden attributes and names, defaults and the signature.

The walk found numpy as the only import, one einsum call with optimize=False, one solve call and one svd call, no MatMult, no dot, pinv or lstsq, and no I/O or warning suppression.

The sources were read with `sed`, `cat` and a `python3 -I` JSON printer. The files were drafted in the session scratchpad and then created exclusively in a new directory. No network was used, and nothing was written under /Users/bgm/Research/Universal Network Theory.
