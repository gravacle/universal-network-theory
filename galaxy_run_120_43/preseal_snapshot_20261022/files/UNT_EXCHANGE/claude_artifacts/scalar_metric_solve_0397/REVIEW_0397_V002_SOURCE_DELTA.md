# REVIEW 0397 V002: source fidelity, delta minimality and 0398 closure

Role: distinct checker, not author. I did not write V001, V002, REVIEW_0397_V001 or the V002 contract/delta. Lens: SOURCE FIDELITY + DELTA MINIMALITY + 0398 CLOSURE. Date 2026-10-15.

## Verdict: PASS_WITH_NOTES

All four 0398 items are CLOSED. The formula, q ordering, sign, units/sign-convention text and scope exclusions are unchanged (statement-level AST identity to v001). Every logic change maps to a 0398 item. One LOW note (the contract does not state the underflow window) and seven INFO notes; none blocks.

## Hashes (sha256 computed from bytes with `shasum -a 256`)

| File | Computed | Expected / source of expectation | Match |
|---|---|---|---|
| FROM_CODEX/0397_2026-10-15_scalar_metric_particular_solver.md | cf985f80a391d0d0ebb16935186a7a0d0e9ad9dc820823aabb20df0ba5179845 | not given in the brief; equals REVIEW_0397_V001 L11 | yes |
| FROM_CODEX/0398_2026-10-15_scalar_solver_review_corrections.md | cf798ab64a7ca91733e28dc29ea5491ce9974f5edc4a5f406ff304cbf1d861a5 | brief | yes |
| EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_PROPOSED_V001.md (frozen source) | f5e28809a8ac24212d1d30bf6be92ab0d064407ae139f72f5146334c86308dd7 | brief | yes |
| EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_DISTINCT_REVIEW_V001.json | 24b92a87e20568b6d934469ea2f91d28433a0c5c275d9c12a17482fe0fe7ba49 | 0397 task; REVIEW_0397_V001 L13 | yes |
| scalar_metric_particular_solve_v001.py | c7dbbba8ccb5bff025cf874410d769e96b7757b214d77d7f7f2fbf8c420dc0db | brief | yes (unchanged) |
| REVIEW_0397_V001.md | 8da4c9c2f2a5b0379602645aa8a54571d26e8573d0fbc576d8035216a7147f68 | brief | yes (unchanged) |
| USAGE_CONTRACT_0397_V001.md | e8ffbf92fd6b0a68568929f07552bf3715318f4c659b151236236f681bc2afbf | REVIEW_0397_V001 L15 | yes (unchanged) |
| AUTHOR_NOTES_0397_V001.md | d51f0ad9070a310888aa741e7092d02e46cb897d2882bed74763350b6158cc60 | REVIEW_0397_V001 L16 | yes (unchanged) |
| scalar_metric_particular_solve_v002.py | ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf | author report; contract V002 L3 | yes |
| USAGE_CONTRACT_0397_V002.md | e8f8f4fbb75b718e7df09d593d7893c70b1342cea1c59e03fb1df985bf1852b9 | author report | yes |
| AUTHOR_DELTA_0397_V002.md | d5a66103777af47e3185ce5f77bc7b17e87ad9f4f13aad44037e7acb9bbdecb8 | author report | yes |

Mismatches: none.

## 1. Own diff and delta minimality

- My own `diff -u v001 v002`: 270 lines, sha256 17dee378e6c64ed7a234a6e9ccdeb7822fd1289cd197c51e2e088b4dd8d1f9bf. It is byte-identical (`cmp`) to the diff embedded in AUTHOR_DELTA_0397_V002.md L18–287.
- Independent AST delta (docstrings stripped; comments are not in the AST):
  - IDENTICAL to v001: `_real_input`, `_complex_input`, `_pair`, `_pairs_matrix`, `_vector_norm`.
  - CHANGED: `_complex_vector2_input`, `_complex_matrix2_input`, `_new_result` (scope string only), `scalar_metric_particular_solve`.
  - NEW: `_nonfinite_entries` (L125–133), `_nonfinite_scalars` (L136–142).
- Statement-level `ast.dump` identity v001 to v002: `zc` L283, `k2` L284, `prefactor` L285, `K0` L286–292, `A` L293, `rhs` L308, `np.linalg.solve(A, rhs)` L310, residual einsum L325, `residual_norm`/`F_norm`/`q_norm` L326–328, `np.linalg.svd(A, compute_uv=False)` L330, `s_max`/`s_min` L334–335, `scale_Aq` L336.
- `_new_result` keys: the same 14 keys in the same order; `units` and `sign_convention` strings AST-identical; only `scope` changed.

| v002 lines | Change | Maps to |
|---|---|---|
| L58–62, L84–88 | `type(value) is not np.ndarray` gives a recorded failure and returns None | 0398 item 2 |
| L125–133 | `_nonfinite_entries` (index, real/imag part, nan/inf) | item 4 |
| L136–142 | `_nonfinite_scalars` | item 3 |
| L180–182 | scope output string: "finite ill-conditioning"; "An exactly singular A (LU failure or s_min == 0) is a failure." | item 1 (text of an output value) |
| L294–304 | K0 and A finite admission before packaging; None on failure; per-entry message | item 4 |
| L314–319 | q finite admission before packaging | item 4 |
| L337–346 | tier-1 diagnostics finiteness, including s_max*q_norm | item 3 |
| L347–353 | s_min not > 0 is a singular failure | item 1 |
| L354–367 | cond_2 and ratios computed only when tier 1 is finite and A is not singular; `!= 0.0` replaces `> 0.0`; tier-2 finiteness | items 1 and 3 |
| L368–374 | "diagnostics: unrepresentable ..." failure, return before packaging | item 3 |
| L375–386 | diagnostics packaged only after all checks (v001 packaged before checking) | item 3 |
| v001 L269 removed | `float("inf")` fallback for cond_2 | items 1 and 3 |
| L391–393 | flag text suffix "the caller must decide explicitly before any use" | text; REVIEW_0397_V001 F1 contract recommendation carried with item 1 |
| L1–3, L56, L82, L190–204, L209–210, L224–227, L229–242, L247–249 | comments and docstrings | text only, no logic |

Unmapped logic changes: none.

## 2. Formula fidelity (unchanged)

Frozen source (sha256 f5e28809…), quoted:
- L5: "Use c=1, signature(-+++), Fourier exp(-i omega t+i k.x), z=omega+i0 and k>0."
- L7: "For q=(n,psi), the quadratic action Hessian and ordinary source covector are"
- L9: "K0=(4pi G_EH)^−1 [[0,−k²],[−k²,k²−3z²]],"
- L10: "F_b=(−epsilon,−Tii),    K0 q=−F_b."
- L26–27: "[[K0+Pi_qq,V_qPsi],[V_Psiq,K_PsiPsi]] [q,deltaPsi]^T =−[F_b+ell_q,ell_Psi]^T."
- L33: "G=−(K0+Pi_eff)^−1=(I−G0 Pi_eff)^−1 G0,"
- L34: "q=G(F_b+ell_eff)+q_hom."

V002 code:
- `q_order` = ["n", "psi"] (L152).
- `prefactor = 1.0 / (4.0 * np.pi * G)` (L285); K0 = [[p·0.0, p·(−k²)], [p·(−k²), p·(k² − 3z²)]] (L286–292).
- `A = K0 + Pi_in` (L293); `rhs = -F_in` (L308); `np.linalg.solve(A, rhs)` (L310). So A q = −F_eff, that is q = −A⁻¹F_eff = G·F_eff with G = −A⁻¹ and F_eff = F_b + ell_eff; q_hom is excluded.
- All of these statements are AST-identical to v001; `units` and `sign_convention` (L158–171) are AST-identical to v001.
- Hand re-check: det K0 = −k⁴/(4πG_EH)², independent of z; −K0⁻¹ = 4πG_EH [[(k²−3z²)/k⁴, 1/k²], [1/k², 0]], which is source L20 (G0).
- No projection: `.real`/`.imag` appear only at L49, L113, L122, L130, L264, L265 (admission, output pairs, norms, non-finite labelling, the Im z check). A and q are never symmetrized, Hermitized, made real or clipped. The AST has no MatMult, dot, matmul, pinv, lstsq, inv, clip, where, zeros, nan_to_num, abs or conj.

## 3. 0398 closure

| Item | Status | Code path |
|---|---|---|
| 1. s_min == 0 rejected; finite near-singular flag-only; no new tolerance | CLOSED | L330 svd, L335 s_min, L347 `singular = bool(np.isfinite(s_min)) and not s_min > 0.0`, L349–353 failure, L357 skips cond_2, L373–374 return. ok stays False (L147), stage stays 'diagnostics' (L324), diagnostics stays None. The comparison is the exact `> 0.0`; cond_tol (L261, L268) is still the only threshold. Finite near-singular: L358 finite cond_2, L387 `ill = not cond_2 <= tol_in`, L389–394 flag, L396 ok True. The flag does not change ok. |
| 2. ndarray subclasses | CLOSED | L57–62 (F_eff) and L83–88 (Pi_eff) reject `type(value) is not np.ndarray` before the shape check and before any `value[i]` (L75) or `value[i][j]` (L104). Element admission through `_complex_input` is AST-identical to v001. No new input framework. |
| 3. Diagnostic overflow | CLOSED | Tier 1 (L337–346): residual_norm, F_norm, q_norm, s_max, s_min, s_max*q_norm. Tier 2 (L357–367), only if tier 1 is clean and A is not singular: cond_2 = s_max/s_min (s_min > 0 is guaranteed here), ratios with `!= 0.0` denominators, then a finiteness check. L368–372 failure "diagnostics: unrepresentable ...", L373–374 return before packaging at L375. Overflow enumeration: numerator overflow gives residual_norm inf (tier 1); denominator overflow gives F_norm or s_max*q_norm inf (tier 1), so no ratio is computed; quotient overflow gives inf (tier 2); s_max/s_min overflow gives cond_2 inf (tier 2), a failure with ill_conditioned left None (L151). A ratio cannot be NaN on the reachable path (finite numerator, finite nonzero denominator). No path turns overflow into a zero or finite ratio or a finite cond_2. Keys are unchanged; every number that is filled is finite. |
| 4. Non-finite K0, A, q | CLOSED | L295–296 check K0 and A before L297–298 package them; a non-finite array is left None; L299–302 messages name the stage, array, index, part and kind (format at L129, L132); L303–304 return. L315–318 check q before L319 packages it; q stays None (L153). No zero substitution: the AST has no zeros, where, nan_to_num or clip. `K0[0][0] = prefactor * 0.0` (L288) is unchanged from v001 and gives nan, which is reported, if the prefactor overflows. |

## 4. USAGE_CONTRACT_0397_V002.md against the code

| Contract | Code | Result |
|---|---|---|
| L3 module hash | bytes | match |
| L9 keyword-only, required, no defaults | AST: six kw-only args, no defaults anywhere | match |
| L29–30 output and diagnostics keys | L146–183, L375–386 | match (14 and 10 keys) |
| L33 every filled number is finite (strict JSON) | the finite gates at L297–298, L319, L373–375; inputs are admitted finite | match |
| L35–38 ok True semantics (cond_2 finite; ratio None only on denominator exactly 0; ill_conditioned bool) | L358–360, L387–388 | match (see N1 on underflow) |
| L40 ok False: evidence only; ill_conditioned None | L151; it is set only at L388 | match |
| L42–58 failure cases 1–7 and message formats (e.g. `assembly: A left None; non-finite A[1][1] real inf`) | L278–279; L299–304; L311–313; L315–318; L331–333; L347–353; L368–374 | match |
| L60 no new tolerance | exact `> 0.0` and `!= 0.0` only | match |
| L62–68 caller must decide on ill_conditioned before use; cond_tol is not a physical rule | flag L391–393; docstring L233–237; scope L180–181 | match. The 1/eps remark at L66 is advisory text and is not encoded in the code. |
| L70–74 warnings not suppressed; Python-float overflow is silent | no warnings, errstate or seterr in the AST; L336, L358–360 are Python-float operations | match |
| L76–84 scope exclusions | 0397 list: homogeneous/boundary/k=0 modes, nonstationary convolution, retained-block elimination, Pi_eff is an ACTION Hessian and not a raw susceptibility, F_eff = F_b + ell_eff, G_EH is not laboratory G, no 43 velocities, galaxy data or fit parameters | all kept |

## Findings

| ID | Severity | Lines | Finding |
|---|---|---|---|
| N1 | LOW (contract disclosure) | code L120–122; contract L37 | **The contract does not state the underflow window.** The sum-of-squares norm loses precision for components below about 1.5e-154 and squares to 0 below about 1.6e-162. A nonzero residual can then give residual_norm 0.0, so the relative residual reads 0.0 (spuriously perfect). A nonzero F_eff, or s_max*q_norm, can give 0.0, so the ratio is None; contract L37 calls that "denominator exactly 0", which is true of the computed value, not of the input. AUTHOR_DELTA L331–334 discloses this; the contract does not. It is outside 0398 (overflow only; "No need to broaden numerical scale coverage"), so item 3 stays CLOSED. Suggested: one contract line giving the ~1e-154 to 1e154 window and saying that a 0.0 or None ratio outside it is not evidence of exactness. No code change is requested. |
| N2 | INFO | L319, L297–298, L349–353 | **A filled field does not mean a valid field.** On the s_min == 0 path and the unrepresentable-diagnostics path, q, K0 and A stay filled with finite numbers while ok is False. 0398 permits this as failure evidence, and the failure text (L352) and contract (L40, L54) say so. Callers must check ok, not whether q is None. |
| N3 | INFO | L57–62 | **The item 2 rule is extended to F_eff.** There was no np.matrix escape there (np.matrix is always 2-D, so the v001 shape-(2,) check already rejected it). The new effect is that 1-D subclasses such as MaskedArray are rejected. This is the literal `type(value) is not np.ndarray` option in 0398, applied uniformly. It is not a new framework. |
| N4 | INFO | L1–3, L190–204, L209–210, L247–249, L391–393 | **Some text changes are not required by 0398.** These are the header, the docstring change list, the 0398 source line, a docstring scope restatement (F_eff = F_b + ell_eff; galaxy data and fit parameters) that duplicates the unchanged v001 scope string, and the flag suffix. None changes any computation, and all are consistent with 0397 and 0398. |
| N5 | INFO | L359–360 | `> 0.0` becomes `!= 0.0`. This is equivalent on the reachable domain, because both denominators are finite and ≥ 0 after tier 1. It matches the 0398 item 3 wording. |
| N6 | INFO | L358, L361–372 | **An overflowed cond_2 with s_min > 0 is a hard failure.** For example, a subnormal s_min gives cond_2 inf, which fails rather than setting ill_conditioned=True, and ill_conditioned stays None. 0398 item 3 permits this ("An explicit failure for unrepresentable diagnostics is sufficient"). It is disclosed in AUTHOR_DELTA L336 and consistent with contract L40 and L56–58. |
| N7 | INFO | L330; L120–122 | Carried from REVIEW_0397_V001 and not in 0398: F6 (svd is a second LAPACK call) is unchanged. F3 (overflow scale limit) now fails closed with a named message. |
| N8 | INFO | contract V002 L5; contract V001 L46 | V002 inherits V001 "where not changed below". V001's "(inf if s_min = 0)" is superseded by V002 L36 and L51–53. The two are consistent when read in order; the V001 text is stale by design, because V001 is preserved under 0398. |

**Author report, re-derived independently.** Every author claim checks out:
- **Imports:** numpy is the only import.
- **Forbidden constructs:** 0 MatMult nodes; no forbidden names, lambdas, globals or async code.
- **Signatures:** a keyword-only public signature with six required arguments, and no defaults in any function.
- **Top level:** one import plus 11 function definitions.
- **Solver calls:** einsum at L325 with optimize=False; svd at L330 with compute_uv=False; one solve, at L310.
- **`.real`/`.imag` uses:** L49, L113, L122, L130, L264 and L265.
- **Size:** 398 lines.
- **Line references:** every author line reference is accurate.
- **Artifact directory:** there is no `__pycache__` or `.pyc` in it.

## Execution statement

- **Static only.** Neither scalar_metric_particular_solve_v001.py nor _v002.py was imported or executed, and no UNT, Codex or producer script was run.
- **Python:** one `python3 -I` run of my own helper. It is kept in my scratch location (scratchpad/checker_0397_v002_src/ast_delta_check.py), not in the artifact directory. It runs `ast.parse`, `ast.dump` and `ast.unparse` over both file texts.
- **Other tools:** shasum, cat, diff, cmp, awk, grep, wc, find and ls.
- **Not used or touched:** no network and no package installs. Nothing was written under Universal Network Theory, and no existing file was modified, moved or deleted. No file whose name matches a forbidden pattern was opened.
- **This file:** created by exclusive create (open mode 'x').

Role: distinct checker, not author.
