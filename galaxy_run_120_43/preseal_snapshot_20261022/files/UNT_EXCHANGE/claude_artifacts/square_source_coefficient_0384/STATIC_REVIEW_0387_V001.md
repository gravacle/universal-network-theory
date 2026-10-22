# 0387 static review, v001

Reviewer: Claude helper, DISTINCT STATIC REVIEWER role (did not write the code).
Date: 2026-10-15.

## Overall verdict: PASS_WITH_NOTES

The code matches 0387, the formula authority, on all eleven checked items. No finding changes d, dprime or dsecond.

The notes concern three things:
- a precision point in 0387's limiting statement, which needs mu0 = 0;
- a domain point the author left open, which resolves in the code's favour;
- the parts of the code that the limiting member cannot exercise.

## Bytes reviewed (sha256 computed from bytes)

| File | sha256 | Status |
|---|---|---|
| diagonal_spatial_coefficient_v001.py | 099176e1e4e899515417b72b295c5e159d243c3c336df5c470ffb8fd7044b49f | matches brief |
| AUTHOR_NOTES_0387_V001.md | 1951cf32ade2d0674528c549e851ab729cdb7d6654ff24b39c2eca6258bdc12d | matches brief |
| square_source_coefficient_v001.py (0384) | 21b80b8d9cad371e48fba57b413a75c6111f026b85725f84f13e9bfff782b57f | unchanged |
| AUTHOR_NOTES_0384_V001.md | e781848d47d640049d192015956792153fa65a5776bff8812bc6f6c8d64730d2 | unchanged |
| STATIC_REVIEW_0384_V001.md | c11274f3541c10c59f2a99b4047893391107da5f4c9834770b539cdb1e5d37e2 | unchanged |
| square_spatial_source_v001.py (0385) | 5a8516155e08c281c4031d5111bdcd0c1e1384dd40fe05a202bf33484eec9220 | unchanged |
| AUTHOR_NOTES_0385_V001.md | 6faee5b224fa361b31666507ccbe7487bd478e10e31479e6739d85aa4ce20bb7 | unchanged |
| STATIC_REVIEW_0385_V001.md | c1f7a79eba14e10e2c8a6654d4c139e75d07e52bc8330df50a60f4b9a9c80018 | unchanged |
| FROM_CODEX/0387_..._inert_implementation.md | 9b9183f939f214b37b3b7e00f464003de8cb08af37bb61a3b6c5bbca673aa835 | matches author pin |
| CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md | 1f42d6a4d772b2f10282592ac0d3ac196ceadb1d64dc57a268eae6f845373813 | context only; mutable, and changed since the author's af124319… pin |

In the current assembly, L470–492 restate the same d_e and d_ef formulas and the same crosswalk as 0387. I found no formula conflict.

## Per-item verdicts

### 1. Inputs. CONFORMS
- **sigma** (`_sigma_input`, L65–85): must be a `tuple` of length 1 or 2. Each entry must be a non-bool Python or NumPy integer equal to exactly +1 or −1.
- **j_vec and c_vec** (`_real_vector_input`, L88–119): each must be a list, tuple or 1-D ndarray of length exactly len(sigma)+1 (L478–480). Each element passes `_real_input`, which requires a finite real and rejects bool and complex. Nothing is broadcast.
- **Signature**: 19 required keyword-only arguments, no defaults (checked by AST).
- **0384 reference and domain checks** (L518–542): a text diff against 0384 shows them byte-identical.

### 2. Local blocks. CONFORMS
- `_local_block` (L122–135) is identical to 0384's (text diff). As noted in the 0384 erratum, r_d is added on the q1 states A1 and B1.
- The degrees used are {2} ∪ {2+a_v}, kept within 0..4 (L564–572). One complete `eigh` runs per needed degree (L577–592).
- chi = U2[:,0] and e2 = w2[0] come from the complete H(2) (L613–615). The gap and residual gates match 0384 (L596–635; diff identical apart from the loop variable).
- mu0 is computed at L521.
- K and V enter only through the identity K_v + a_v·V_v = H(2+a_v) − e2·I, which holds for every integer a_v because r_d and the B diagonal are linear in d. For a_v = ±2 this is H(4) or H(0).

### 3. Supports. CONFORMS
- One edge: e = (0,1) on 2 sites. Adjacent edges: e = (0,1) and f = (1,2) on 3 sites (L546–556).
- a_v is accumulated per subset S over the full union support (L557–563), so the adjacent case gives:
  - {e}: a = (σe, σe, 0)
  - {f}: a = (0, σf, σf)
  - {e,f}: a = (σe, σe+σf, σf)
- Every operator is built on the union support. R_e carries H(2) − e2 = K_2 on site 2 (a_2 = 0), and R_f carries K_0 on site 0. The U and U† tuples have length n_sites (L677–678).
- D is computed per S (L643).

### 4. M_S scalar and Kronecker sum. CONFORMS
- weights_v = 4a_v². c = Ud·D + mu0·Σa − Σ_v j_v·weights_v (L645–647), which equals 0387's Ud·D + mu0·Σa − 4Σ j_v a_v².
- Hand check of the scalar: the degree energy Ud(d−d*)² + (Δ/2)d gives Ud·a² + mu0·a for any integer a. The source term contributes −4j_v·a_v² relative to the O_v = −4 reference.
- den = c + Σ_v (w_{2+a_v} − e2) on the (4,)^n product index (L649; `_kron_sum_denominator` L180–191, with axis v = site v).
- Every denominator must be finite and above pos_tol (L664–671), with no epsilon and no repair. A failure here returns at L703, before any entry is used.

### 5. R0. CONFORMS
- den0 = Σ_v (w2[k_v] − e2) with no scalar (L686–687), so it is M_empty = Σ K_v and independent of the source.
- Exactly one index is removed: `keep` is all True except (0,…,0) (L688–690). Because chi is the same array as U2[:,0], that index is exactly |Ω⟩ in the H(2)^⊗n product eigenbasis.
- Q0 commutes with M_empty, so R0 = Σ_{k≠0} |k⟩⟨k| / den0_k. `_apply_reference_jet` (L227–241) implements this: transform, zero the ground component, divide the retained components, transform back.
- The retained denominators are gated above pos_tol (L692–702).
- R0 is applied to f, fp and fpp with no derivative terms, so R0′ = R0″ = 0.

### 6. Formulas and ordering. CONFORMS
`_ordered_chain` applies steps[0] first (L250–255) and contracts with conj(Ω) (L259–261).

One edge:
- fold = r2,e·r1,e (L733)
- restored = steps (R_e, R0, R_e), giving ⟨R_e R0 R_e⟩ (L735–737). This is the eeee history.
- total = fold − restored (L766).

Adjacent edges:
- fold = r2,e·r1,f + r2,f·r1,e (L741)
- double-flip: the four specs with steps (R_right, R_ef, R_left) for left, right ∈ {e,f} (L742–749). Their sum is ⟨(R_e+R_f) R_ef (R_e+R_f)⟩ and covers the histories effe, feef, efef and fefe.
- restored: steps (R_e, R0, R_f), giving ⟨R_f R0 R_e⟩ (history eeff), and steps (R_f, R0, R_e), giving ⟨R_e R0 R_f⟩ (history ffee) (L750–753).
- total = fold − double − restored (L766).

All fold factors are 1, and there are no vertex-disjoint terms, degree counts or global sums.

The moments are r_m = Σ conj(t)·t/den^m with t = U†Ω, for m = 1..4 (`_moments` L265–274), which is ⟨Ω|R^m|Ω⟩. In the adjacent case they are evaluated on the 3-site union support. That is equal to the 2-site value, because chi is a null vector of the spectator K.

### 7. Directional derivatives. CONFORMS
- b_S = Σ_v c_v·4a_v² (L648). Since dM_S/dt = −b_S·I, R′ = b·R² and R″ = 2b²·R³.
- In the jet (L216–218): new_fp = b·R²f + R·f′ and new_fpp = 2b²·R³f + 2b·R²f′ + R·f″.
- Iterating the jet through a chain reproduces the full ordered product rule. For R_f R0 R_e the second derivative is R_f″R0R_e + 2R_f′R0R_e′ + R_fR0R_e″, which includes both cross terms. The double-flip chains give all six cross pairs.
- Moment jets (L277–281):
  - r1: (r1, b·r2, 2b²·r3)
  - r2: (r2, 2b·r3, 6b²·r4)

  These agree with r_m′ = m·b·r_(m+1) and r_m″ = m(m+1)·b²·r_(m+2).
- Folds use the scalar product rule (L284–290).
- No ground-expectation substitution is made. The full site tensors are propagated between noncommuting inverses.

### 8. Gates and diagnostics. CONFORMS
- Gated: finite inputs; residuals and Hermiticity; gap > pos_tol; M_S denominators; R0 retained denominators; and totals that are finite and satisfy |Im| ≤ imag_tol·max(1,|Re|) (L780–789).
- There is no sign gate on d, dprime or dsecond. No comparison of any total against 0 exists (AST and reading).
- Reported separately: the fold (L768), the double-flip chain (L769, None for one edge), the restored chain (L770), every history (L771), the moments (L729), the component imaginary maximum (L772–773), the subsets with min denominators (L680–684), reference_gap (L697) and removed_reference_denominator (L691).
- declared_inputs include sigma, j_vec and c_vec.

### 9. Inert import and array sizes. CONFORMS
Checked by AST only:
- Module level holds `import numpy as np` (L8) and 24 `def`s. There are no decorators, no `global` or `nonlocal`, and no constants.
- There is no I/O and no MatMult. No dot, matmul, tensordot, kron, vdot, inner, outer, solve, inv, reshape or broadcast_to appears as an attribute or a name.
- All 6 `np.einsum` call sites pass `optimize=False` (L150, L177, L604, L606, L716, L718).
- The runtime specs from `_site_spec` are "km,mb->kb", "km,am->ak", "km,mbc->kbc", "km,amc->akc" and "km,abm->abk". There are no repeated labels.
- The largest tensor is (4,4,4), 64 entries, as are its float64 denominator and its boolean mask. No 16×16 or 64×64 matrix is formed, and no M_S is diagonalized as a whole.
- `eigh` is limited to 4×4 blocks; thread pinning at launch carries over.

### 10. Limiting correspondences (hand only)
Take H(d) degree-independent, so λJ = λR = 0 and V = 0, with j_v = j and u = Ud − 4j. Each M_S is then c_S·I + Σ K_v, and Ω is an eigenvector with eigenvalue c_S, so every R0·R_S·Ω vanishes.

With **mu0 = 0** (c_S = D_S·u) I reproduce 0387's values:
- d_e = (2u)⁻³ = 1/(8u³).
- Same-sign pair (D_ef = 6): fold = 1/(4u³), double = 4/(2u·6u·2u) = 1/(6u³), so d = 1/(12u³).
- Opposite-sign pair (D_ef = 2): double = 1/(2u³), so d = −1/(4u³).
- Global: V(2/8 + 2/12 − 4/4)/u³ = −7V/(12u³).
- With c_v = 1, b_S = 4D_S and du/dt = −4. Then A/u³ has first derivative 12A/u⁴ and second derivative 192A/u⁵.

The author's claim with **mu0 ≠ 0 is confirmed**. c_e = 2Ud + 2σ·mu0 − 8j = 2(u + σ·mu0), so d_e = 1/(8(u + σ·mu0)³). The pair scalars become:
- c_ef = 6u + 4σ·mu0 for the same-sign pair;
- c_ef = 2u for the opposite-sign pair, where mu0 cancels;
- c_e,f = 2(u ± mu0) for the single flips.

**Does degree independence make mu0 vanish? No.** Degree independence of H(d) sets λJ = λR = 0. mu0 = Δ/2 + 2Ud(2 − dstar) involves neither, and it enters only the scalar c, not H(d). 0387's limiting statement (and assembly L492) therefore implicitly assumes mu0 = 0, for example Δ = 0 and dstar = 2 as in the 0384 analytic control. With mu0 ≠ 0 the edge sum becomes (V/8)[(u+mu0)⁻³ + (u−mu0)⁻³] ≠ V/(4u³), and the global −7V/(12u³) fails.

GL6CG is a "degree-lock parent", which is consistent with mu0 = 0. I did not read the GL6CG theorem file to confirm this. See N1.

### 11. The author's open points
| Point | Verdict |
|---|---|
| a_v = ±2 outside delta's coverage (author UP2) | **Resolvable in the code's favour.** For any integer a ≠ 0, the source-free per-site block is Ud·a² + a(mu0·I + V) + K ≥ \|a\|(Ud·\|a\| − ‖mu0·I + V‖) ≥ \|a\|·delta. This holds because K ≥ 0, Ud > 0 and ‖mu0·I + V‖ is exactly the max in delta's definition. delta > 0 therefore already gives M_S(j=0) ≥ Σ\|a_v\|·delta ≥ 2·delta, including the a = ±2 shared vertex. Only the source shift −4Σ j_v a_v² can lower a denominator; it carries weight 16·j_v at the shared vertex. The actual-denominator gate (L667) controls that, as 0387 requires. No code change. See N2. |
| Strict sigma admission (tuple only, integer ±1) | CONFORMS. It is literal to 0387 ("a length1 or2 tuple ... exactly±1"). It is stricter than necessary, since lists are rejected, but it fails closed. |
| Imaginary gate on totals only | CONFORMS. Every history is real in exact arithmetic. The 0384 gauge φ = (1, −1, −κ/\|κ\|, κ/\|κ\|) makes every H(d) real, so every M_S, R_S and R0 is real symmetric and Ω is real. Component imaginary parts are therefore roundoff diagnostics, and they are reported (L772–773). |
| Removed R0 denominator reported, not gated | CONFORMS. It is exactly 0.0 by construction (e2 = float(w2[0])). The gap gate already guarantees that only one index is removed, since every other den0 ≥ w2[1] − e2. reference_gap equals local_gap exactly in floating point, so the reference gate duplicates the gap gate. That is harmless. |
| Later numerical check needs nonuniform j_vec and c_vec | AGREE, and the requirement is broader. See N3. |

## Findings

| ID | Severity | Lines | Finding |
|---|---|---|---|
| N1 | LOW (spec precision, not code) | 0387 L29; assembly L492 | The degree-independent limiting values (1/(8u³), 1/(12u³), −1/(4u³), −7V/(12u³)) hold only with mu0 = 0. Degree independence of H(d) does not set mu0, which enters the scalar c. The code is correct either way. Root should state mu0 = 0 explicitly in the correspondence. |
| N2 | INFO | AUTHOR_NOTES UP2; L667 | delta > 0 does cover a_v = ±2 at zero source, with per-site bound \|a\|·delta. Only the source shift is left to the actual denominator gate, which is the required gate. The author's note is more pessimistic than necessary. |
| N3 | LOW (verification scope) | L227–241, L686–711 | In the degree-independent limit, Ω is an eigenvector of every M_S. Every R0 term is then zero, and every resolvent acts as a scalar on Ω. That member therefore does not exercise any of: the R0 path (keep mask and M_empty denominators), the noncommuting chain transforms, H(d) feedback through V, or mu0. It is also symmetric under site relabelling: 0↔1 for one edge, and 0↔2 with e↔f for a pair. These paths were verified statically here. A later numerical check would need V ≠ 0 (or mu0 ≠ 0), nonuniform j_vec and c_vec, and both sigma patterns. |
| N4 | INFO | L772–789 | The imaginary gate applies to totals only. Components are real in exact arithmetic (gauge argument), and their imaginary parts are reported. Conforms. |
| N5 | INFO | L686–702 | The removed denominator is exactly 0 and the reference_gap gate duplicates the local gap gate. Harmless. |
| N6 | INFO | L680–703 | After an M_S denominator failure, Stage 5 still computes the R0 arrays before returning at L703. No missing entry is used. Harmless. |
| N7 | INFO | — | Carried over from the 0384 and 0385 reviews: eigh thread pinning at launch, and the tolerance forms and units of imag_tol and resid_tol. |

## Unresolved points (for root; no physics change proposed)
1. State mu0 = 0 explicitly in 0387's and the assembly's degree-independent crosswalk (N1). Confirm against the GL6CG degree-lock parent, which I did not read.
2. Any later numerical check needs a member that exercises R0, V and mu0 feedback, nonuniform j_vec and c_vec, and both sigma patterns (N3).
3. Carried over: thread pinning and tolerance forms.

## Execution statement
Nothing was executed or imported. The module was never imported or run, and no numerical tests, examples or calculations were performed.

The only Python run on the module was `python3 -I -B -c "import ast,sys; ..."` AST parsing. It listed:
- module-level nodes, decorators, imports and global statements;
- calls and attributes, and forbidden attributes and names;
- every einsum call with its keyword arguments;
- array constructors, signatures and MatMult nodes.

Plain text `diff` compared the copied helpers and stages against the 0384 module. All mathematical checks were done by hand.

No network was used and no reviewed file was modified. This review was created exclusively (noclobber). Nothing was written under /Users/bgm/Research/Universal Network Theory.
