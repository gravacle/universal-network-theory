# 0387 author notes, v001

Author: Claude helper (AUTHOR role). A different helper does the static review.

The artifact is `diagonal_spatial_coefficient_v001.py` in this directory. It exposes one public function, `diagonal_spatial_coefficient(*, ...)`, with 19 required keyword-only arguments and no defaults.

The 0384 and 0385 files were not modified. The helpers this module needs were copied into it rather than imported.

## Sources (sha256 computed from bytes at authoring time)

| Source | Role | sha256 |
|---|---|---|
| FROM_CODEX/0387_2026-10-15_diagonal_spatial_coefficient_inert_implementation.md | formula authority | 9b9183f939f214b37b3b7e00f464003de8cb08af37bb61a3b6c5bbca673aa835 |
| square_source_coefficient_0384/square_source_coefficient_v001.py | local block, reference checks, structure (copied) | 21b80b8d9cad371e48fba57b413a75c6111f026b85725f84f13e9bfff782b57f |
| square_source_coefficient_0384/square_spatial_source_v001.py | input admission and jet pattern (copied/adapted) | 5a8516155e08c281c4031d5111bdcd0c1e1384dd40fe05a202bf33484eec9220 |
| square_source_coefficient_0384/STATIC_REVIEW_0385_V001.md | read for carried notes | c1f7a79eba14e10e2c8a6654d4c139e75d07e52bc8330df50a60f4b9a9c80018 |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md | context only (mutable; not consulted for formulas) | af1243190bee8c9a93a10728b23c5564054bec2170c50d47c9762a9152f38c45 |

## Spec-to-code mapping (line numbers in v001)

**Inputs and reference**

| 0387 item | Code |
|---|---|
| 0384 native inputs and tolerances; no defaults | signature L378–399 |
| sigma: a tuple of length 1 or 2, entries exactly ±1 (integers) | `_sigma_input` L65–85; L477 |
| j_vec, c_vec: finite real, length len(sigma)+1, never broadcast | `_real_vector_input` L88–119; L478–480 |
| 0384 reference and domain conditions: \|r2\| ≤ ref_tol, g > 0, κ ≠ 0, delta > 0 | L518–542 |

**Support and local blocks**

| 0387 item | Code |
|---|---|
| Supports: one edge e=(0,1); adjacent e=(0,1), f=(1,2); S ∈ {e}, {f}, {e,f}; a_v and D on the union support | L544–566 |
| Needed degrees d = 2 + a_v ⊂ 0..4 | L564–572 |
| H(d) exactly as in 0384, one complete eigh per needed d | `_local_block` L122–135; L574–594 |
| χ and e2 from H(2); uniqueness, gap and residual checks | L596–635 |

**Operators**

| 0387 item | Code |
|---|---|
| M_S scalar: Ud·D + mu0·Σa − 4·Σ j_v a_v²; Kronecker-sum denominators; every one > pos_tol | L637–684 (scalar L645–647; denominators L649) |
| b_S = 4·Σ c_v a_v² | L648 |
| R0: removes only the all-χ index (0,…,0) of the H(2) product eigenbasis; retained denominators > pos_tol; zero source derivatives | L686–711; `_apply_reference_jet` L227–241 |
| R_S on the jet: R′ = bR², R″ = 2b²R³, powers of R by repeated division | `_apply_resolvent_jet` L194–224 |

**Coefficient**

| 0387 item | Code |
|---|---|
| Ordered chains with the operator product rule, steps[0] acting first, contracted with conj(Ω) | `_ordered_chain` L244–262 |
| Ω = χ^⊗n | L715–719 |
| Moments r_m,S = ⟨Ω\|R_S^m\|Ω⟩, m = 1..4 (eigenbasis contraction) | `_moments` L265–274 |
| r_m′ = m·b·r_(m+1) and r_m″ = m(m+1)·b²·r_(m+2) | `_moment_jets` L277–281 |
| Folds via the scalar product rule | `_product_jet` L284–290 |
| d_e = r2,e·r1,e − ⟨R_e R0 R_e⟩ | L731–738 |
| d_ef = r2,e·r1,f + r2,f·r1,e − Σ_{x,y∈{e,f}} ⟨R_x R_ef R_y⟩ − ⟨R_f R0 R_e⟩ − ⟨R_e R0 R_f⟩ | L739–766 |

**Outputs**

| 0387 item | Code |
|---|---|
| Separate fold, double-flip and restored chain diagnostics; all 1 or 6 histories kept | L755–773 |
| Gates: finite and \|Im\| ≤ imag_tol·max(1,\|Re\|) on d, dprime, dsecond; no sign gate | L775–798 |
| Units, static notes, scope | `_new_result` L342–375 |

## Static limiting checks (claims for a later check, not run)

**Assumptions.** H(d) is degree-independent (λJ = λR = 0, so V = 0), j_v = j, and mu0 = 0 (see unresolved point 1).

**Why the R0 terms vanish.** Each M_S then reduces to c_S·I + Σ_v K_v with c_S = u·D, where u = Ud − 4j. Ω is an eigenvector of every M_S with eigenvalue u·D. R0·Ω = 0, so every R0 term vanishes.

**Values.**
- One edge (D = 2): d_e = (2u)⁻²(2u)⁻¹ = **1/(8u³)**.
- Same-sign adjacent pair (D_e = D_f = 2, D_ef = 6): fold = 2/(8u³) and double chain = 4/(2u·6u·2u). This gives d_same = 1/(4u³) − 1/(6u³) = **1/(12u³)**.
- Opposite-sign adjacent pair (D_ef = 2): d_opposite = 1/(4u³) − 4/(8u³) = **−1/(4u³)**.

**Derivatives.** Along the uniform direction c_v = 1, b_S = 4·D_S, and every term is homogeneous of degree −3 in u, with u′ = −4. So A/u³ has first and second derivatives **12A/u⁴** and **192A/u⁵**. The code obtains them from b_S·R² and 2b_S²·R³, which reproduce exactly these values in this limit.

**Global value.** With 2V edges, 2V same-sign pairs and 4V opposite-sign pairs:

V[2/8 + 2/12 − 4/4]/u³ = **−7V/(12u³)**.

This global sum is not implemented in the function, by design.

These are manual correspondences to the old GL6CG limit. The populated code keeps R0, the internal returns and all H(d) feedback.

## Scope

- This is a local finite-order (h⁴) pure-flip diagonal coefficient only.
- No physical ground state, geometry or calibration is selected.
- A complete spatial response also contains the lower-order contacts, state response, the separate square and Birth operators, every separately retained term, and a controlled remainder.
- The function does not implement:
  - vertex-disjoint pairs, which cancel analytically;
  - degree counts;
  - global edge or pair sums;
  - galaxy sums.

## Working-array sizes

- Site tensors are (4,4) or (4,4,4) complex128, at most 64 entries (1 KiB).
- Denominator arrays have the same shapes, in float64.
- The local blocks are 4×4, one per needed degree (at most five: d = 0..4).
- No 64×64 or 16×16 matrix is ever formed, and no M_S is diagonalized as a whole.
- Peak memory is a few KiB.
- The three-site adjacent call needs about 6 chains × 3 steps × 6 transforms × 3 einsum calls on 64-entry tensors, plus moments. That is about 10⁵ multiply-adds.

## Choices beyond the literal text (for the reviewer)

1. **Strict sigma.** sigma must be a `tuple`, as 0387 writes it. Each entry must be a non-bool integer (Python or NumPy) exactly equal to +1 or −1. Lists and floats are rejected.
2. **Imaginary gate.** The 0384 gate applies to d, dprime and dsecond. The fold, chains, histories and moments report raw imaginary parts but are not gated.
3. **Moments.** They are computed in the eigenbasis as Σ conj(t)·t/den^m on the union support. In the adjacent case this equals the two-site value, since χ on the extra site is a null vector of K.
4. **Double-flip chains.** They are evaluated as the four explicit histories (x, y) ∈ {e, f}², with R_y first, then R_ef, then R_x. This is equivalent by linearity to ⟨(R_e+R_f) R_ef (R_e+R_f)⟩ and keeps per-history diagnostics.
5. **Carried over from 0384.** Gap > pos_tol, the orthonormality residual, absolute herm and resid tolerances, and strict scalar admission.

## Unresolved points

1. **The limits assume mu0 = 0.** 0387 states them for degree-independent H(d) with j_v = j only. With mu0 ≠ 0, each single flip has c = 2u + 2σ·mu0, so d_e = 1/(8(u + σ·mu0)³), and the pair values shift too. Root should confirm that the GL6CG correspondence assumes mu0 = 0, or Δ/2 + 2Ud(2 − dstar) = 0.
2. **a_v = ±2 is outside delta's coverage.** In a same-sign adjacent pair, the shared vertex has a_v = ±2 in M_ef, which uses H(0) or H(4). The 0384 sufficient condition delta > 0 controls only |a_v| ≤ 1 per vertex. Here only the actual M_ef denominators are gated, which is what 0387 requires.
3. **Removed R0 denominator.** It is exactly 0 by construction (e2 = w2[0]). It is reported, not gated.
4. **reference_gap equals the local gap.** Mathematically, reference_gap = min over non-ground indices of Σ_v(w2[k_v] − e2) = w2[1] − e2. Both are gated by pos_tol.
5. **Carried from the 0384 and 0385 reviews.** Thread pinning for eigh at launch, and the tolerance forms and units.
6. **A later numerical check needs the right inputs.** It should use a nonuniform c_vec and j_vec, and both sigma patterns. The uniform limiting checks above cannot detect site-label errors.

## Execution statement

The module was never executed or imported. No tests, numerical examples or calculations were run.

The only Python applied was AST parsing:
- `ast.parse` as a syntax check, which passed;
- an AST walk listing einsum calls and their keyword arguments, MatMult nodes, forbidden attribute and name uses, module-level node types, defaults and the signature.

It found 6 einsum call sites, all with optimize=False. Two of them, `_site_apply` and `_contract`, take a spec built from the tensor rank. There is no MatMult and no dot, matmul, tensordot, kron, outer, inner, solve, inv or reshape. Module level holds only Import and FunctionDef nodes. No function has a default.

The files were drafted in the session scratchpad and then created here exclusively. No network was used, and nothing was written under /Users/bgm/Research/Universal Network Theory.
