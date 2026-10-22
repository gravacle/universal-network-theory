# 0385 static review, v001

Reviewer: Claude helper, DISTINCT STATIC REVIEWER role (did not write the code).
Date: 2026-10-15.

## Overall verdict: PASS_WITH_NOTES

The code matches 0385, which is the formula authority, on all ten checked items. No finding changes J, J_v or J_vw. The notes cover:
- the tolerance form of the Hessian symmetry gate;
- what the uniform-source identities can and cannot detect;
- the optional sign gates.

None of them needs a physics change.

## Bytes reviewed (sha256 computed from bytes)

| File | sha256 | Status |
|---|---|---|
| square_spatial_source_v001.py | 5a8516155e08c281c4031d5111bdcd0c1e1384dd40fe05a202bf33484eec9220 | matches brief |
| AUTHOR_NOTES_0385_V001.md | 6faee5b224fa361b31666507ccbe7487bd478e10e31479e6739d85aa4ce20bb7 | matches brief |
| square_source_coefficient_v001.py (0384) | 21b80b8d9cad371e48fba57b413a75c6111f026b85725f84f13e9bfff782b57f | unchanged |
| AUTHOR_NOTES_0384_V001.md | e781848d47d640049d192015956792153fa65a5776bff8812bc6f6c8d64730d2 | unchanged |
| STATIC_REVIEW_0384_V001.md | c11274f3541c10c59f2a99b4047893391107da5f4c9834770b539cdb1e5d37e2 | unchanged |
| FROM_CODEX/0385_..._inert_implementation.md | e1e0ea13a63a01c3290f57440c8de9d6e087a4a9eb056e7e146e3cc3309e9823 | matches author pin |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md | e904d4b05db0adaa44ce1fe8a6978878a06fc9fdd450a0fa54082bec6e8670a1 | matches author pin; context only |

**Erratum carried from 0384, recorded in FROM_CLAUDE2/0079.** STATIC_REVIEW_0384_V001.md says "q projects onto p1". It should say that q projects onto the q1 component, that is, the states A1 and B1. That is why r_d sits on the (1,1) and (3,3) diagonal entries. The matrix review in that file was correct. The 0384 file is not edited.

## Per-item verdicts

### 1. Parts copied from 0384. FAITHFUL
I ran a plain text `diff` against the 0384 module, which is not execution. It shows only the following differences:
- the header and docstrings;
- the new `_real_vector4_input` (L54–85) and `_pair` (L201–202);
- ellipsis-generalized `_site_apply` specs (L121–128);
- the jet function (L150–186);
- the scalar source lines (L512–514) and the `b` cache entry (L532, L549);
- the jet arrays, contractions and output gates (L601–681).

Everything else is byte-identical in substance:
- `_local_block` (L99–112), the reference checks (L401–425), and the eigensystems, gap and residual checks (L427–488);
- the cycle, sigma, a_v and D (L492–511);
- the Kronecker-sum denominators and pos_tol gate (L515–561), and the U and U† site tuples (L551–552);
- the histories and the D checks (L563–599).

The 0384 static verdicts for items 1, 2, 4, 5, 8 and 10 therefore carry over unchanged. For H(d), r_d is added on the q1 states A1 and B1, as in the erratum above.

### 2. Source scalar and derivative signs. CONFORMS
- b_v = 4a_v² (L512). source_shift = Σ_v j_v·b_v (L513). c = Ud·D + mu0·Σa − source_shift (L514). This is exactly 0385's [Ud·D + mu0·Σa − 4Σ_v j_v a_v²].
- Reference subtraction: O_v = 4[(d_v−2)² − 1] is −4 at each ice endpoint. The source term −Σ j_v O_v at an intermediate state, minus its value at the reference, is −4Σ_v j_v a_v². That matches the code, and chi depends only on H(2), so it is j_vec-independent.
- Derivatives: ∂M_S/∂j_v = −b_v·I. Then R_v = −R(∂_vM)R = b_v·R², and R_vw = b_v(R_w·R + R·R_w) = 2b_v·b_w·R³. The signs are consistent with R being the positive inverse and growing with each j_v.

### 3. Jet update per prefix. CONFORMS
`_apply_resolvent_jet` works in the eigenbasis of M_S, where R acts as 1/den:
- r1 = t/den, r2 = r1/den, r3 = r2/den; r1_v and r2_v for f_v; r1_vw for f_vw (L167–172).
- new_f = R·f (L173).
- new_f_v[v] = b[v]·R²f + R·f_v[v] (L174).
- cross[v,w] = b[v]·R²f_v[w] + b[w]·R²f_v[v] (L175–177). The first einsum, "v,wabcd->vwabcd", gives b_v·R²f_w. The second, "w,vabcd->vwabcd", gives b_w·R²f_v.
- new_f_vw = 2·b_v·b_w·R³f + cross + R·f_vw (L178–180). The factor 2 is present on the R³ term only, as 0385 states.

Axis and index ordering:
- f_v has shape (v, a,b,c,d) and f_vw has shape (v, w, a,b,c,d). Source axes always lead.
- `_site_apply` uses "km,...mbcd->...kbcd" and its three siblings (L121–128). The ellipsis takes the leading source axes, and the four explicit labels are the last four axes, which are vertices 0..3. The transform therefore acts only on the site axes, and the source axes pass through in order.
- Division `t_v/den` and `t_vw/den` broadcasts the (4,4,4,4) den array over the leading source axes, because NumPy aligns trailing axes.
- No einsum string reuses a label within one operand.
- `b` is the per-prefix float64 (4,) array from the cache (L549). It is indexed by vertex, so b_v pairs with j_v and with the source axis v.

### 4. Histories, ordering, transform-back, contraction. CONFORMS
- Prefix order is (m1, m2, m3), applied first to last (L610–613). This gives R_S3·R_S2·R_S1 on the jet, with all 24 orders and D checks as in 0384.
- Each step transforms into the complete product eigenbasis of its own prefix and back again (L164–166, L182–186).
- Each history starts from (psi, zero_v, zero_vw) (L611), and these arrays are never mutated.
- Contractions with conj(psi): "abcd,abcd->", "abcd,vabcd->v" and "abcd,vwabcd->vw" (L614–616). They are summed over all 24 histories (L617–619).

### 5. Hessian: ordinary, unsymmetrized, gated. CONFORMS (gate scale: note N1)
- R depends on j_vec only through the scalar s = Σ_v b_v j_v. So ∂_v∂_w R = b_v·b_w·d²R/ds² = 2b_v·b_w·R³ is the ordinary mixed partial derivative. No extra factor of 2 appears off the diagonal.
- The returned J_vw is sum_J_vw[v,w].real entry by entry (L678). It is never symmetrized.
- Symmetry holds by construction:
  - The b_v·b_w factors are 0 or 16, so they are exact.
  - cross[v,w] and cross[w,v] add the same two addends in swapped order, and IEEE addition is commutative.
  - Each transform applies the same arithmetic to every [v,w] slice.

  The residual should therefore be zero or at roundoff level.
- The gate max|J_vw − J_wv| ≤ resid_tol·max(1, max|J_vw|) (L664–669) catches asymmetric coding errors, such as a wrong pairing in the cross term. It cannot catch symmetric errors, which are left to the identities in item 7.
- The gate scale is the author's choice; see N1. Reusing resid_tol conforms, because 0385 says to keep the 0384 tolerance set.

### 6. j_vec validation. CONFORMS
`_real_vector4_input` (L54–85) does the following:
- An ndarray must have shape exactly (4,), so 0-d, (1,4) and other shapes are rejected (L60–64). A list or tuple must have length exactly 4 (L65–69). Everything else is rejected, including scalars, other sequence types and strings (L70–75).
- Each element passes `_real_input`, which rejects bool, complex, non-numeric and non-finite values.
- There is no broadcast, no coercion of complex values and no default. `j_vec` is a required keyword-only argument (AST: 17 keyword-only arguments, 0 defaults).
- The result is a tuple of floats in vertex order 0..3 (L85). It is recorded in declared_inputs (L378).

### 7. Static identities, by reasoning. HOLD
Set j_v = j for every v, and let F = Σ_v f_v and G = Σ_vw f_vw.
- **J matches 0384.** Σ_v b_v = 4D, so c = Ud·D + mu0·Σa − 4jD, which is the 0384 scalar. f follows the same recursion, so J equals the 0384 J.
- **Σ_v J_v equals Jprime.** Summing L174 over v gives F_new = 4D·R²f + R·F. This is the 0384 recursion new_fp = 4D·R²f + R·fp (0384 L132).
- **Σ_vw J_vw equals Jsecond.** Summing L178–180 over v and w gives G_new = 2(4D)²R³f + 4D·R²F + 4D·R²F + R·G = 32D²R³f + 8D·R²F + R·G. This is 0384's new_fpp (0384 L133).
- With the shared initial values (psi, 0, 0), these identities hold exactly in exact arithmetic. In floating point, the code computes Σ j·b_v while 0384 computes 4·j·D, so agreement is to roundoff. See N2 for what these identities cannot detect.

### 8. Notes and qualification. CONFORMS
- AUTHOR_NOTES L53–57 state −∂_c²E^(2) = 32h²·Σ_edges r_(3,σ_e)(c_u+c_v)² in exactly 0385's form. They add that uniform incidence can make it scalar and a nonuniform source need not. This is consistent with the current assembly L333.
- L59–66 say the square is NOT the sole leading spatial response. They list the h² diagonal contact, the fourth-order diagonal terms, state redistribution, coupled-field terms and physical-map terms as separate and not set to zero, and they keep the separate diagonal folds in the full action.
- The module's `scope` string (L259–264) and `static_notes` (L240–258) repeat the scope and fold statements. The explicit contact formula appears only in the author notes, which is where 0385 asks for it ("in notes").

### 9. Inert import and bounded arrays. CONFORMS
This was checked with AST only.
- Module level holds `import numpy as np` (L8) and 13 `def`s. There are no decorators, no `global` or `nonlocal`, and no module constants.
- There is no I/O, os, sys or subprocess call, no MatMult node, and no dot, matmul, tensordot, kron, vdot, inner, outer, solve, inv, reshape or broadcast_to attribute.
- All 11 `np.einsum` calls pass `optimize=False` (L131, L174, L175 ×2, L179, L457, L459, L601, L614, L615, L616).
- The largest arrays are (4,4,4,4,4,4) = 4096 complex128 elements, 64 KiB: f_vw, cross, the outer-product term and their transforms. A 3-operand c_einsum with optimize=False builds no larger intermediate. No 65536-element array exists.
- My static work estimate is about 1.2×10⁷ complex multiply-adds, which agrees with the author.
- `eigh` (L438) is the 4×4 LAPACK call that 0385 L24 explicitly allows, subject to thread pinning by root at launch.

### 10. The author's open choices
| Choice | Lines | Verdict |
|---|---|---|
| Positivity gated on Re J only | L661–662 | CONFORMS. 0385 states no sign for J_v or J_vw. See N3. |
| J_v and J_vw reported but not sign-gated (min real parts reported) | L671–672 | CONFORMS. See N3. |
| Imaginary-part gate imag_tol·max(1,\|Re\|) on all 21 sums | L644–660 | CONFORMS. 0385 says to fail closed on imaginary violations. The unit-scale caveat of 0384 N2 carries over. |
| Hessian symmetry gate scaled by resid_tol·max(1, max\|J_vw\|) | L664–669 | CONFORMS. It mixes units; see N1. |
| Strict j_vec admission | L54–85 | CONFORMS. |

## Findings

| ID | Severity | Lines | Finding |
|---|---|---|---|
| N1 | LOW | L664–669 | The Hessian symmetry gate reuses resid_tol, an absolute tolerance in E for the eigen-residuals, against a quantity in E⁻⁵. The max(1, max\|J_vw\|) factor makes it relative only when max\|J_vw\| > 1 in the chosen unit. Because the construction is symmetric (item 5), the gate is a structural check against asymmetric errors, and any reasonable resid_tol should pass. Acceptable under the fixed tolerance set. |
| N2 | LOW (verification scope) | L512–514, L549, L174–180, L615–616 | All three uniform-source identities are invariant under relabeling the source vertices. Two reflections of the square preserve sigma, 0↔1 with 2↔3 and 1↔2 with 0↔3, and they act transitively on the vertices, so at uniform j all four J_v are equal by symmetry. These identities therefore cannot detect a vertex-label error in the mapping from j_vec to b to the source axis. I verified statically that the mapping is consistent (b_v = 4a_v², with a indexed by vertex and j_vec in vertex order). A numerical check of per-vertex labeling would need a nonuniform j_vec. In the existing commuting analytic control, psi remains an eigenvector of every M_S with eigenvalue c_S(j_vec), so J, J_v and J_vw have closed forms there. |
| N3 | LOW | L661–672 | The 0384 gauge argument (φ = (1, −1, −κ/\|κ\|, κ/\|κ\|)) does not depend on j_vec, because the source enters only the scalar. So with every den > 0, all jets are entrywise nonnegative in gauge, and J_v > 0 and J_vw > 0 strictly. Each vertex is an endpoint of some first edge, and every pair (v,w) is reached through b_v and b_w at the same prefix or at successive prefixes, for example v=0, w=2 through S1={(0,1)} and S2={(0,1),(1,2)}. Sign gates on J_v and J_vw would be consistent with the theory, but 0385 does not require them, so reporting only conforms. Root may decide. |
| N4 | INFO | L657 | The imaginary-part gate form carries over from 0384 (0384 review N2). |
| N5 | INFO | L438 | The 0384 review's N1 (eigh thread pinning) is now explicitly acknowledged by 0385 L24. N3–N5 of the 0384 review carry over unchanged. |
| N6 | INFO | AUTHOR_NOTES L80 | "about 1.8×10³ einsum calls": my static count is about 2.1×10³. That is 72 resolvent steps × 28 einsum calls each, plus 72 contractions and a few setup calls. This is immaterial. The multiply-add estimate agrees. |

## Unresolved points (for root; no physics change proposed)
1. The Hessian symmetry gate scale and units (N1). 0385 fixes the tolerance set, so a dedicated tolerance would be a signature change.
2. Whether to gate J_v > 0 and J_vw > 0, which the gauge argument implies (N3).
3. Any later numerical verification needs a nonuniform j_vec to exercise per-vertex labeling (N2). The uniform identities alone cannot.
4. Carried over: eigh thread pinning at launch, and the tolerance forms and units from the 0384 review.

## Execution statement
Nothing was executed or imported. The module was never imported or run, and no numerical tests, examples or calculations were performed.

The only Python run on the module was `python3 -I -B -c "import ast,sys; ..."` AST parsing. It listed:
- module-level nodes, decorators, imports and global statements;
- calls and attributes;
- every einsum call with its keyword arguments;
- array constructors, signatures and MatMult nodes.

A plain text `diff` compared the 0384 and 0385 module sources. All mathematical checks were done by hand. No network was used, and no reviewed file was modified. This review was created exclusively (noclobber). Nothing was written under /Users/bgm/Research/Universal Network Theory.
