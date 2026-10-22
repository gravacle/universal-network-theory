# 0384 static review, v001

Reviewer: Claude helper, DISTINCT STATIC REVIEWER role (did not write the code).
Date: 2026-10-15.

## Overall verdict: PASS_WITH_NOTES

The code matches the 0384 specification on all eleven checked items. No defect changes J, Jprime or Jsecond. The notes below are about tolerance form, the LAPACK call under the resource guard, and stale custody line references in the author notes. None needs a physics change.

## Bytes reviewed (sha256 computed from bytes)

| File | sha256 | Status |
|---|---|---|
| square_source_coefficient_v001.py | 21b80b8d9cad371e48fba57b413a75c6111f026b85725f84f13e9bfff782b57f | matches brief |
| AUTHOR_NOTES_0384_V001.md | e781848d47d640049d192015956792153fa65a5776bff8812bc6f6c8d64730d2 | matches brief |
| FROM_CODEX/0384_..._inert_implementation.md | cc991dab500b1d02bb201aad3a747290952337cf5c509aedf19d3e6d6692e1a3 | matches author notes |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md | c2c1bba6082cdcfd83db8ec1bd2bb15d6fc8902239823aacc25283542728bd2d | DIFFERS from author's recorded a59ad092... (see N6) |
| FROM_CLAUDE2/0064, 0065 | 6277558b..., eb07250a... | match author notes |

I reviewed against the current assembly bytes: L357–447 for the leading source response, including the analytic control at L410–418, and L508–559 for the local matrix conventions.

## Per-item verdicts

### 1. Local matrix H(d), offsets, V. CONFORMS
- `_local_block` L64–77: r_d = epsilon_r − lambda_R·d (L66) and b_d = ES + epsilon_c + lambda_J·d (L67).
- The rows are [ER,0,κ*,0], [0,ER+r_d,0,κ*], [κ,0,b_d,g], [0,κ,g,b_d+r_d] (L71–74). This is entry-for-entry the 0384 matrix and the assembly's L527–533. conj(kappa) is in (0,2) and (1,3), and kappa is in (2,0) and (3,1).
- I cross-checked against the operator form in 0065: κ|B⟩⟨A| + κ*|A⟩⟨B| + r_d·q + g|B⟩⟨B|X_q, with q projecting onto p1. It agrees.
- H(2+a) − H(2) = a·diag(0, −λR, λJ, λJ−λR) = aV holds identically, because r_d is linear in d and the B diagonal carries λJ·d. The code builds H(1), H(2) and H(3) directly from the formula (L361–364) rather than as H(2)+aV. The two are mathematically identical and differ only by floating roundoff. This conforms to 0384, which says to diagonalize the three degree blocks.
- Each site block of M_S is K_i + a_iV_i = H(2+a_i) − e2·I. This is implemented as the eigenvalues of H(2+a_i) minus e2 (L444). Sites with a_i = 0 still carry the full K_i = H(2) − e2 (blocks[2]), so internal excitations at unflipped sites are kept.
- e2 = w2[0] and chi = U2[:,0] (L397, L399). eigh returns eigenvalues in ascending order, so these are the lowest pair.

### 2. Domain checks. CONFORMS
- r2 = epsilon_r − 2λR is checked as |r2| ≤ ref_tol (L334, L347).
- g > 0 (L349). kappa == 0 is an exact comparison (L351).
- mu0 = Δ/2 + 2Ud(2 − dstar) (L335).
- delta = Ud − max(|mu0|, |mu0+λJ|, |mu0−λR|, |mu0+λJ−λR|) > 0 (L336–341, L353). This equals the assembly's Ud − ‖mu0·I + V‖, because V is diagonal.
- Every denominator array must satisfy finite and min > pos_tol (L452–473). Failing subsets are not cached, and the function returns at L487 before any division. Division at L125–130 uses `den` as stored, with no epsilon and no clipping or repair.
- All comparisons are written as `not x > y` or `not x <= y`, so NaN fails closed.

### 3. Source sign and derivative rules. CONFORMS
- c(S,j) = Ud·D + mu0·Σa − 4·j·D (L443), matching 0384 exactly.
- Single-edge consistency: a = (σ,σ) on the two endpoints gives D = 2 and Σa = 2σ, so c = 2Ud + 2σmu0 − 8j = d_σ − 8j. This matches the assembly's M_σ(j) = M_σ − 8jI (L540, L561).
- Degree energy: Ud(d−d*)² + (Δ/2)d evaluated at 2+a, minus its value at 2, is Ud·a² + mu0·a. This reproduces the Ud·D + mu0·Σa scalar.
- With dM/dj = −4D·I: R′ = −R(dM/dj)R = 4D·R², and R″ = 4D·2R·R′ = 32D²·R³. R and R′ commute within one M_S. In the code, new_fp = 4D·(R²f) + R·fp (L132) and new_fpp = 32D²·(R³f) + 2·4D·(R²fp) + R·fpp (L133). The signs are consistent: R grows with j.

### 4. Subset construction. CONFORMS
- sigma = 1 − 2·bit from bits (1,0,1,0), giving (−1,+1,−1,+1). There is a guard at L426.
- Edges are ((0,1),(1,2),(2,3),(3,0)) (L423).
- Masks 1..14 (L431) enumerate exactly the 14 nonempty proper subsets.
- a_i accumulates sigma_e over the selected incident edges (L433–437). D = Σa_i² (L441).
- Each vertex has one −1 and one +1 cycle edge, so a_i ∈ {−1,0,1} always. The check at L438 can never fire.
- Hand check of D values: 2 for a single edge; 2 for an adjacent pair; 4 for a disjoint pair ({0,2} gives a = (−1,−1,−1,−1), {1,3} gives (+1,+1,+1,+1)); 2 for a triple.
- The D check (2, 2|4, 2) happens at L508–513 before any division. There are 16 adjacent-first and 8 disjoint-first orders, which matches the assembly control at L410. All 14 masks are confirmed used (L523).

### 5. Tensor index ordering and transforms. CONFORMS
- psi = einsum("a,b,c,d->abcd", chi×4) (L528), so axis i is vertex i.
- In `den`, shifts[i] is broadcast on axis i (L445–451). u_sites and uh_sites are tuples ordered by vertex i, built from blocks[2+a_i] (L478–479). The same eigh call supplies w and U, so the eigenvalue order and column order agree.
- `_site_apply` (L80–92): each einsum spec contracts mat[k,m] with the m-index on the requested axis and writes k back to the same axis. I checked all four strings.
- Forward transform (L95–100) applies conj(U).T, so t_k = Σ_m conj(U[m,k]) f_m, which is U†f. Back transform (L103–108) applies U. The result is R_S·f = (⊗U)·diag(1/den)·(⊗U†)·f. Per-axis transforms commute, so their order across axes does not matter.
- The bra is conj(psi) (L529) and the ket is psi. The global phase of chi cancels.

### 6. All 24 histories, ordering, transform-back. CONFORMS
- `_orders` (L142–151) recursively generates the 24 permutations. Distinctness and count are checked (L493).
- Masks are m1 = {o0}, m2 = m1 ∪ {o1} and m3 = m2 ∪ {o2} (L500–502). They are applied in the tuple order (m1, m2, m3) (L536–537), so the result is R_S3·R_S2·R_S1·psi with S1 acting first. That is ⟨psi|M_S3⁻¹M_S2⁻¹M_S1⁻¹|psi⟩.
- Every resolvent application transforms into its own product eigenbasis and back to the local basis (L122–139). The full length-256 vector is carried between prefixes, with no ground-expectation substitution.
- Each history restarts from (psi, 0, 0) (L535). The arrays `psi` and `zero` are never mutated, because einsum and division return new arrays.

### 7. Product-rule derivative propagation. CONFORMS
- r1 = t/den, r2 = r1/den, r3 = r2/den (L125–130), giving powers 1, 2 and 3 of the same denominator.
- Iterating f_{n+1} = R·f_n, f′_{n+1} = R′f_n + R·f′_n and f″_{n+1} = R″f_n + 2R′f′_n + R·f″_n from (psi, 0, 0) reproduces the full Leibniz expansion of (R3R2R1)′ and (R3R2R1)″, including all cross terms R3′R2′R1, R3′R2R1′ and so on.
- D is taken per prefix from that prefix's cache entry (L120). No finite differences are used.

### 8. Complete spectra. CONFORMS
All four eigenpairs of each of H(1), H(2) and H(3) are kept (L369, L376). Every den array is the full (4,4,4,4) Kronecker-sum spectrum, 256 values. No truncation, ground projection or level deletion occurs. Degeneracies in H(1) or H(3) are harmless, because R = U·diag(1/den)·U† is basis-independent.

### 9. Final contraction and fail-closed outputs. CONFORMS
- einsum("abcd,abcd->", conj(psi), arr) (L539) is summed over 24 histories (L543). The raw complex sums are always reported (L563).
- For each of J, J′ and J″ the code checks that the value is finite, that |Im| ≤ imag_tol·max(1,|Re|), and that Re > 0 (L565–575). Real parts are assigned only after every check passes (L576–581). Otherwise J, Jprime and Jsecond stay None.
- Hand support for the positivity check: a degree-independent diagonal gauge φ = (1, −1, −κ/|κ|, κ/|κ|) makes every off-diagonal of H(d) nonpositive (−|κ|, −|κ|, −g, using g > 0). It is degree-independent because V is diagonal. Each M_S is then a real Z-matrix. Once every den > 0 it is a nonsingular M-matrix, and it is irreducible because κ ≠ 0 and g > 0 connect A0–B0–B1–A1. So R ≥ 0 entrywise and chi > 0. Every history, and therefore J, J′ and J″, is real and strictly positive whenever stage 4 passes. The Re > 0 check is a consistency check, and a failure would point to a numerical fault. This agrees with the assembly's L383–389.

### 10. Inert import and bounded arrays. CONFORMS
This was checked with AST only.
- Module level holds `import numpy as np` (L7) and 11 `def`s. There are no decorators, no `global` or `nonlocal`, and no module constants.
- The call list contains no open, print, os, sys, subprocess or I/O.
- There are no MatMult (`@`) nodes and no attributes named dot, matmul, tensordot, kron, vdot, inner, outer, solve or inv.
- All five `np.einsum` calls pass `optimize=False` (L92, L388, L390, L528, L539).
- The public function has 17 required keyword-only arguments and no defaults. `_new_result()` builds a fresh dict on each call.
- Largest arrays: (4,4,4,4) = 256 elements, as complex128 tensors and 14 float64 den arrays. No 256×256 array is formed. The 4×4 blocks are built by np.array, np.eye and eigh.

### 11. The author's open choices
| Choice | Lines | Verdict |
|---|---|---|
| delta > 0, g > 0, Re X > 0 compared against 0, not pos_tol | L349, L353, L574 | CONFORMS. 0384 states ">0" literally and scopes the positivity tolerance to "the actually used shifted intermediate denominators". |
| Local H(2) gap gated by pos_tol | L414 | MINOR EXTENSION, stricter. 0384 asks only for a "unique" lowest eigenvector. Gating on pos_tol fails closed and does not change the physics. See N4. |
| All 256 eigenvalues of each M_S count as used denominators | L452–473, L483–486 | CONFORMS. This is the conservative reading. It is also the reading the positivity argument needs (M_S positive definite as a whole), and it avoids an overlap threshold. |
| Absolute tolerances (herm_tol, resid_tol); hybrid imag_tol·max(1,\|Re\|) | L406–412, L570 | CONFORMS. 0384 fixes no tolerance form. These tolerances are scale-dependent. See N2 and N3. |
| Extra orthonormality check max\|U†U − I\| ≤ resid_tol | L390–391, L410 | CONFORMS. 0384 asks for residuals to be recorded, and this one protects the back-transform. |
| Strict input admission (rejects bool, 0-d arrays, complex for real inputs) | L10–61 | CONFORMS. Inputs are never coerced. |
| Per-history imaginary parts reported, not gated | L544, L557 | CONFORMS. 0384 gates the results. Each history is real in exact arithmetic (gauge argument above). |

## Findings and notes

| ID | Severity | Lines | Finding |
|---|---|---|---|
| N1 | LOW | L369 | `np.linalg.eigh` is a LAPACK call (zheevd) that can call BLAS level-2 kernels internally. It is not a contraction path, and 0384 requires the diagonalization. The module correctly sets no thread environment. Root's frozen invocation must pin LAPACK/BLAS to one thread under the existing guard. |
| N2 | LOW | L570 | imag_tol·max(1, \|Re X\|) mixes units, since X is E⁻³, E⁻⁴ or E⁻⁵. When \|Re X\| < 1 in the chosen energy unit, the gate becomes absolute and can be loose relative to X. It is documented (L257) and conforms, but root should pick imag_tol with the energy unit in view. |
| N3 | LOW | L406–412 | herm_tol and resid_tol are absolute, so their meaning depends on the energy scale of H. Conforms. |
| N4 | INFO | L414 | The gap is gated by pos_tol, which also gates the denominators. The gap is not literally a denominator of J. This is stricter than 0384's "unique" and fails closed. Acceptable. |
| N5 | INFO | L387, L406 | The Hermiticity residual is identically 0, because H is built Hermitian and eigh reads only the lower triangle. The check is a harmless tautology. |
| N6 | LOW (custody, not code) | AUTHOR_NOTES L11 | The assembly file now hashes to c2c1bba6... (mtime 17:19), but the author recorded a59ad092... The cited ranges "L357–408 and L469–520" do not match the current layout, where the H(d) display is at L525–534 and the 0384 analytic control at L410–418. In the current bytes, every formula the code relies on agrees with the code. I cannot diff against the earlier version. The author notes should be re-pinned to the current hash and line ranges. |
| N7 | INFO | L410–418 (assembly) | Hand trace of root's analytic control through the code, not executed. H(1)=H(2)=H(3), so U†chi = e0 at every site, and psi is an eigenvector of each M_S with eigenvalue u0·D. With mu0 = 0, the minimum of den is c = (Ud − 4j)·2 = 7/4 at Ud=1, j=1/32, so the code path would give 5/(2u0³). As the assembly itself states, this control commutes and so cannot exercise per-site basis changes with H(1) ≠ H(3). Those were verified statically here (items 5 and 6). |

## Unresolved points (for root; no physics change proposed)
1. Whether eigh on 4×4 blocks is acceptable under the one-numerical-thread guard and the earlier BLAS warning, given that thread pinning happens at invocation (N1).
2. The form and values of imag_tol, herm_tol and resid_tol in the frozen invocation (N2, N3).
3. Whether pos_tol should also gate the local gap, or the gap should get its own explicit tolerance (N4).
4. Re-pin the assembly hash and line ranges in the author notes (N6).
5. j's unit is implied to be energy by c(S,j) and the stated derivative units. 0384 does not state it. This is not a defect.

## Execution statement
Nothing was executed or imported. The module was never imported or run, and no numerical tests, examples or calculations were performed. The only Python run on the module was `python3 -I -B -c "import ast,sys; ..."` AST parsing, which listed module-level statements, calls, attributes, einsum keyword arguments, signatures and MatMult nodes. All mathematical checks were done by hand. No network was used. The reviewed files were not modified. This review was created exclusively (noclobber), and nothing was written under /Users/bgm/Research/Universal Network Theory.
