# UT1_REACH_V001 — independent Claude2-lane derivation of UT-1 (typing of the uniform-lapse / k = 0 block)

Lane: Claude2 workflow (`ut1_reach_c2/`), reassigned from Claude4 by V4A A38 table row "R-H (UT-1)". Dispatch: `FROM_CODEX/0497` (f1779659…, verified from bytes). Mandate: V4A A29 workstream 3 (principal sign-off). Written 2026-10-18 from 04:04Z to 04:22Z (`date -u`).

**Status: V001, COMPLETE.** This is theory plus read-only toys. It is not a model version, a launch or an adoption.

**Scope kept.**
- Writes only under `ut1_reach_c2/`. Claude4's `ut1_reach_c4/` was read-only.
- No launch. No NGC3198 target, velocity, rotmod, MassModels, SPARC or NGC run file was opened. `lwr_common_v001.py` was read as text and never executed, because its module level reads an NGC run checkpoint.
- Nothing under `~/.codex` was touched.
- Runtime: pinned codex python with `-I -B`, `nice -n 10`, single-thread BLAS. K1 ran as 4 concurrent processes; every other script ran alone. Peak memory was 2.9 GB (K3); the longest wall time was 25 s.
- Author modules were imported only as byte-verified copies in `copies/`: CARD 4d123c1f, CB 701095f9, SAB 7130a277.

**Grades:** FORMAL (algebra or an exact record or code fact, cited file:line), TESTED-POSITIVE / TESTED-NEGATIVE (a computation on bytes, hashed in HASHES.txt), UNTESTED (with its deciding computation), HYPOTHESIS, DECLARED-PREMISE. GR, G and T_N appear only as COMPARATORs. Every sign and exponent verdict below is G-free.

**Order of work, and disclosure.**
1. I read the Claude4 helper reports (H1 PARTIAL, H2a, H2b, H3, H4) first, because verifying them is the task.
2. I wrote and ran my own scripts K1–K4 and R0.
3. Only after K4 did I read V4A A38–A40 and Claude4's concurrent `synthesis/UT1_REACH_V001.md` (473497f9, written at 04:06Z while I worked). My computations therefore do not depend on A39 or the synthesis.
4. V4A is an open file. It is now 9b88e8a1 (715 lines); the helpers cite eade847c (569 lines).

---

## 0. Verdict

| # | Result | Grade |
|---|---|---|
| V1 | **The record's adopted premises type the uniform-lapse mode (k = 0) as a constraint (fixed-H / fixed-preparation null direction), not as a canonical thermodynamic variable.** The uniform lapse is a time reparametrization (H[N̄] = N̄H). Its retarded response is zero. The global energy and the homogeneous data come from the separate background / normal-constraint solve. The canonical (−βVar(H)) value is a property of the counted computational branch, now CA-34. It does not follow from a premise. Citations are in §3. | FORMAL |
| V2 | **The k = 0 typing alone does not decide the 1/r tail.** The far field is set by the k → 0⁺ limit of the k ≠ 0 kernel. In the counted CA-28 cardinal closure that limit is the grid[0,0,0] entry itself (1 − w₀ = (L²−1)/12·Σq², exactly). This contradicts the adopted CRS:33 ("not substituting k=0 into the k>0 annular transfer"). | FORMAL |
| V3 | **Schur bound: no gate-consistent typing is attractive below κ₁.** Below the first zero κ₁ of det K_jj, the response satisfies T(k) ≤ 0 for any typing that keeps the source Hessian negative semidefinite (NSD). Measured: 0 violations at ~98,000 premise points per typing on the 25 admissible estimates. Violations occur only in the gate-violating RD3 probe (44,956 points). | FORMAL + TESTED-POSITIVE |
| V4 | **Every typing measured on 37 estimates × 13 rays gives either finite reach or a repulsive power law. No attractive tail occurs in any gate-consistent typing** (table §5). | TESTED-NEGATIVE (as a tail route) |
| V5 | **An attractive Newtonian tail needs C1 (F_nn(0⁺) = 0) and C2 (vanishing native uniform chart stiffness) together.** C2 alone, with the isothermal lapse kept, gives a real-k pole at k_p = √(4πG Q∞/(c⁴\|T(0)\|)), i.e. \|T(0)\| = T_EH(k_p) (to ≤ 1.2%). Below the pole the response is finite and repulsive. Correction: H4's and A39 item 4's "if C2 holds, the tail is Q∞-Newtonian" is wrong as stated (§2.2). | TESTED-POSITIVE (K4) + FORMAL |
| V6 | **Q∞ = c⁴/(16πGγ_eff) = 8.0623 is unchanged by every typing:** \|Q(1000/kpc)/Q∞ − 1\| ≤ 8.1e-9. The A21 short-wavelength results move by ≤ 2.1e-4 at \|k\| ≥ 2 /kpc (continuation typings) and by ≤ 4.8e-5 (lapse-only typings). | TESTED-POSITIVE |
| V7 | **Whether the model has a 1/r tail is UNTESTED.** It is decided by U1 (the small-k limit of the k ≠ 0 lapse and chart entries in mixed L ≥ 6 captures) and U2 (the order of limits, i.e. energy relaxation at k_g compared with the galaxy age). Within CA-28 only finite, 1/r and linear far fields are representable; any other far-field form needs a non-analytic infinite-volume response, which is UNTESTED (LIVE:41). | UNTESTED |

**Agreement with the Claude4 interim (A39).**
- Items 1, 2, 3 and 5 are independently confirmed.
- Item 4 needs the correction in V5: C1 ∧ C2 is required, and "flatness … points at BH-D" is not a consequence of anything computed here.
- Root registrations (b), (c) and (e) are confirmed from bytes.

## 1. Verification of H2b (17b72917) and H4 (b9ce950e) from bytes

**Byte integrity: PASS.**
- Every line of HASHES_H2B_V001.txt and HASHES_H4_V001.txt re-hashes OK (0 mismatches).
- The full Claude4 tree hashes are in `out/C4_INPUT_TREE_SHA256_V001.txt` (130 files). They include H2a md cefd4a08, H2a json 41cc30b2, H3 md 0fdf0479 and H1 PARTIAL e55c2524. H2a and H3 have no manifest of their own.

**Claims re-derived.** "Re-derived" means own code (K1/K3/K4/R0) or own algebra. K1's transcription of the read-off matches the module path (CARD → CB.bind_symbol → CB.solve_symbol, using the copies) to ≤ 4.9e-13 at 1,776 random points, with 0 refusals.

| Claim | Source | My check | Status |
|---|---|---|---|
| h_NN(0) = −βVar(H)/L³; T(0) = v/(Eref h_NN(0)) | A20; H2b, H4 | A2 −3.5510 → T(0) = −39.7329 m³/J; birthk_c1 −394.1871. The 37 estimates span −878.1 to −5.73. The toy gives iso(H,H) = βVar(H) to 1e-15 | **VERIFIED** |
| Record selects T-FIX/T-GAUGE at k = 0 | H2b F1–F7 | Quotes verified from bytes (R0). CRS:26/31/33/34 strengthen it; H2b does not cite them | **VERIFIED, strengthened** |
| iso − retarded = zero-energy-block term; all of βVar(H) at k = 0; only a degeneracy term at k ≠ 0 | H2b §3.2 | K3 toy (N = 8/10/12): retarded(H,H)/N ≤ 5e-29; block fraction at m = 1 ≤ 3e-25; at m = 2 it is 3.2%, 2.1%, 0.76% | **VERIFIED** (comparator) |
| 1 − w₀ = (L²−1)/12·ε² | H2b S2 | Fejér expansion \|Σₐe^{iaq}\|²/L² = 1 − (L²−1)q²/12 + O(q⁴); L = 4 gives 1.25 | **VERIFIED** (FORMAL) |
| h_NN(shell1)/h_NN(0): median 0.53, range 0.05–2.13 | H2b S1 | 8-node shell: 0.0532 / 0.534 / 2.135 (A2 0.570). 6-node: 0.058 / 0.525 / 2.04 (A2 0.623) | **VERIFIED** |
| Γ_nn(0) < 0 in 11/37; gate fails on 12/37 | H2b; H3, H4 | 11 and 12. The 12th (NEAR_ENDPOINT pooled) fails at node (1,0,0), not at k = 0. Both statements are right | **VERIFIED** |
| Continuation (V4/V5): finite and repulsive on 481/481; T(0⁺) −63.6 to −1256 | H2b S4 | CONT8: 481/481 finite repulsive, T(0⁺) −1255.7 to −63.59 (A2 −69.75). CONT6: −1512 to −54.4 | **VERIFIED** |
| RD3 probe: 173/481 attractive rays, each with a pole | H2b V1; H3 | 173/481 (107/325 admissible), all with poles. The node is indefinite on 37/37 (A2 λ_max +0.300) | **VERIFIED.** LOW omission in H2b: it does not say the probe violates GATE:100 |
| T-FIX finite on 481/481 | H2b table | True only under a continuation rule that the record does not own (CARD:124; LIVE:41). With the node typed T-FIX inside CA-28: repulsive k⁻² on 481/481 | **SCOPE NOTE** (H2b §5 acknowledges it) |
| H4-T1 Schur bound | H4 §1 | Algebra re-derived (§2.1). TESTED with 0 violations | **VERIFIED** |
| "T-FIX gives a repulsive 1/r tail on every ray" | H4 v2 | Reproduced (FIXN and FIXH: 481/481 k⁻² repulsive). It is a property of interpolating a T-FIX node through CA-28, which is the substitution CRS:33 forbids. It is not a property of T-FIX on an unbounded medium | **DEFECT (MEDIUM, framing)** |
| T-LOC gives T ∝ −1/k⁴ | H4 | LOC: 481/481 k⁻⁴ repulsive; k* unchanged exactly | **VERIFIED** |
| "If C2 holds, the tail is Q∞-Newtonian"; "can arise inside T-ISO"; "soft chart: no binding change; the existing T-ISO binding produces the Q∞-Newtonian tail by itself" (H4 v3, §3 T-OTHER a, §6) | H4 | **TESTED-NEGATIVE.** SOFT6ISO (D(0) × 1e6, isothermal lapse kept): pole on 481/481 rays at k_p (§2.2), T(0⁺) = T_ISO(0) < 0. The Q∞-Newtonian band exists only above k_p (A2: 0.0045 /kpc, about 220 kpc). With C1 ∧ C2 (SOFT4/6 on FIXH): k* ∝ λ^−1/2, still repulsive below k* | **DEFECT (HIGH, physics)** |
| No logarithmic tail is representable | H4-T2 | FORMAL for CA-28: Fejér weights are trigonometric polynomials and D⁻¹ is analytic, so T is meromorphic in k² along a ray. It is a closure property, not a model property | **VERIFIED, scope-limited** |
| Q∞ untouched; image aliasing | H4 §4 | Q∞ = 8.0623, deviation ≤ 8.1e-9. Weight 1 on node 0 at k_prim ∈ 2πℤ³ follows from CARD:91 (q = k mod 2π). Shifts at \|k\| ≥ 2–3 /kpc are ≤ 2.1e-4 (13 rays × 37) | **VERIFIED** |
| 25/37 admissible | H4 §2 | 25 | **VERIFIED** |
| FIX needs an IR-tail prescription (H4 §5, §6) | H4 | Only if the T-FIX node is interpolated (the artefact above). Under the spec-compliant version (§6), T(0⁺) is finite and no IR prescription is needed | **DEFECT (MEDIUM, implementation)** |
| T-FIXC is UNTESTED, and decides the far field | H4 U1; H2b U4 | The S reads are not conserved (FORMAL, §3.4). The status of the uniform R read is UNTESTED. Under H4-T1, either outcome is non-attractive, so U4 cannot decide the tail | **RE-GRADED:** not a tail decider |
| Real-space proxy numbers (g/(Q∞g_N) at 10–500 kpc) | H4 §3 | Not re-run (no real-space transform done here) | **REUSED, UNVERIFIED** |
| Recomputation table | H4 §5 | Spot-checked DRV v008:336-340 and 1441-1447, QV5:84 and CS (no typing CA). Corrected in §6 | **PARTLY VERIFIED** |

**Other partials reused.** Every reuse below was hash-verified.

- **H2a (cefd4a08).**
  - Lemma §7 (T-FIX changes only the k = 0 node; at k = 0 it is the Schur complement on the reads): VERIFIED by K3. The explicit fixed-H protocol equals the Schur form to ≤ 1e-9, and FIX − ISO at k ≠ 0 is ≤ 1e-33.
  - TB/TC: VERIFIED by K1 (same classes).
  - "T-LOC is algebraically KUBO:60's proper-temperature rule": VERIFIED for the lapse covariance block. With a fixed proper β in every cell, Tr exp(−Σβ_p/N_α·N_αE_α) does not depend on N; K3 gives d²lnZ/dN² = 0. Only one-point contacts −β⟨O⟩ remain (K3: 0.25397 = 0.25397).
- **H3 (0fdf0479).**
  - Results A, B, the V0–V4 counts and k* ∝ λ^−1/2: VERIFIED by K1.
  - The Result C coefficient formula s₂ was not re-derived. Its sign predictions agree with K1.
- **H1 PARTIAL (e55c2524).** F-5…F-18 were spot-verified from bytes (R0 plus greps): KUBO, S4, SAB, CB, ASMB, QV5, V002, ADOPT, LEDGER:28/30, CRS:26-34, SPEC:2/61, FLOAT:103-111, REVIEW_0407:71/109, WTC:139/162, 0405 :1971-1975, CONSERVED_SCALAR :3/55/65 and FROM_CODEX3/0032:16. All quoted text matches. F-12's reading of WTC was not re-derived.

## 2. Kernel algebra (FORMAL; numbers TESTED in K1/K4)

Definitions (CB:9-11, 81-101; SAB:168-206; CARD:83-133):
- K = Eref·JᵀΓJ + EH, with J = diag(1, J′), det J′ = 1, and contact 0 at j̄ = 0.
- T = −v[K⁻¹]_nn = −v/S, where S = K_nn − K_nj K_jj⁻¹ K_jn.

**2.1 The bound.**
- EH_nn ≡ 0 (SAB:194, tensors[0] = 0), so K_nn = Eref·Γ_nn with Γ_nn = −F_nn + F_nj D⁻¹F_jn.
- If F ⪯ 0 and D ≺ 0, Γ_nn ≥ 0, because it is minus the Schur complement of an NSD matrix.
- If also K_jj ≺ 0, then −K_nj K_jj⁻¹K_jn ⪰ 0.
- So S ≥ Eref·Γ_nn ≥ 0 and T ≤ 0.
- K_jj(0⁺) = Eref J′ᵀD(0⁺)⁻¹J′ ≺ 0 holds until κ₁. With EH removed, S = −Eref·F_nn exactly, so T(0⁺) = v/(Eref F_nn(0⁺)).

**2.2 What a tail needs.**
- **(C1) F_nn(0⁺) = 0.** Otherwise T(0⁺) is finite and negative, whatever D does.
- **(C2) Vanishing native chart stiffness, K_jj ⊁ 0 at small k.** Otherwise the bound applies.
- **C2 alone (K4).** The native chart part vanishes, so K_jj → EH_jj, which is indefinite. Then S ≈ −Eref F_nn − (EH-eliminated term) = −Eref F_nn − v/T_EH(k), and S changes sign where |T(0)| = T_EH(k).
  - The closed form is k_p² = 4πG Q∞/(c⁴|T(0)|), which is G-free when written as |T(0)| = T_EH(k_p).
  - Found against predicted: A2 0.004478 vs 0.004479; birthk_c1 0.001413 vs 0.001422; worm_c1 0.006477 vs 0.006528; worm_pooled 0.005511 vs 0.005538 /kpc.
  - The result is independent of λ for λ = 1e4–1e8.
- **C1 ∧ C2 at finite softness λ.** k* ∝ λ^−1/2 (k*/k*_ISO = 0.0100–0.0275 at λ = 1e4 and 0.0010–0.0028 at λ = 1e6), repulsive below k*. A strict 1/r tail needs an infinite uniform chart susceptibility (H3 C2) and F_nn(0⁺) = 0 (C1), plus C3.
- **What would make C1 hold.**
  - Under T-ISO, C1 fails at every L (A20).
  - Under T-FIX/T-GAUGE, F_nn(0⁺) is the k → 0⁺ limit of the k ≠ 0 entries. It is the isothermal intensive value under H-CL (HYPOTHESIS) and the static order of limits.
  - C1 can therefore hold only if H-CL fails, or if the retarded order applies at galaxy scales: energy at k_g does not relax within the galaxy's age (COMPARATOR: hydrodynamics, χ^R(k,ω) = χ_T Dk²/(Dk² − iω)).

## 3. H2a deliverable — which typing the owned record selects (cited lines, R0 file)

**3.1 What the parent's dynamics makes the uniform lapse** (FORMAL; DECLARED-PREMISE where marked).
- **Closed parent.** The generator is time-independent and Hermitian, H = ΣE_α (KUBO:5; LEDGER:15-16; OP:118-128). DECLARED-PREMISE (model).
- **Placement of the lapse.** H[N] = ΣN_αE_α with Σ_α w_αX = 1, so H[N̄] = N̄H (V002:10-13). The V002 rule is adopted and counted (ADOPT:2, 15; CI:122-126).
- **Retarded response.** Chi_HH = 0 (KUBO:13). For stationary ρ, every energy-index row and column sum vanishes (KUBO:28, 50). A uniform lapse at fixed preparation is a time-reparametrization tangent (KUBO:37). It is "a conserved uniform direction … Keep global energy/initial data separately, or use the admitted constrained quotient" (KUBO:52).
- **Adopted calculation.** It is CTP/causal: "Gamma_nn=Chi_EE-Chi_EO Chi_OO^-1 Chi_OE, with actual causal/CTP typing, … background and initialization terms" (V002:20; CEPL:10, 18, 32 "Singular/conserved directions require constraints or retained variables, not a fabricated inverse").

**3.2 What the adopted state and boundary specification fixes.** CRS 032a564b is ROOT_ADOPTED (ASM:77, in the earlier 2026-10-16 section).
- :26 "full positive trace-one owned-parent density family … No ice/product-chi/Gibbs/ground state substitution."
- :27 "spectral-block stationary states … arbitrary PSD weights/coherences in degenerate energy blocks."
- :31 "Retarded response about the chosen independently conditioned background … consistent with the normal constraints."
- :33 "Match galaxy perturbations to the same-action homogeneous background rather than substituting k=0 into the k>0 annular transfer."
- :34 "Solve initial normal constraints … Never use retarded Green functions alone to … fix a missed conserved mode."
- The binding layer agrees:
  - SAB:178 and :189-190 ("k=0 normal/background constraints require separate solve");
  - CB:16, 31, 108;
  - ASMB:7, 55, 59-60;
  - QV5:84 ("k=0 handled by explicit boundary/normal solution");
  - OCK:40 ("constrained inverse or bordered system … do not replace physical null directions by arbitrary small diagonal terms");
  - and the 0405 `partial_legendre_blocks` already accepts `declared_zero_modes` "(e.g. uniform energy)" (owned_retained_source_columns_v002.py:1971-1975, sha 173f608d).

**3.3 Where the canonical typing comes from.**
- ASM:57, later the same day: "explicitly COUNTED quasi-static maximum-entropy equilibrium galaxy branch … a chosen computable method, not evaluated physical response."
- S4:351-352: "STATIC ISOTHERMAL … (fixed beta, re-prepared canonical state), not fixed-preparation retarded response."
- SPEC:61 names the alternative at the point where the typing was introduced: "At fixed mean energy beta must adjust; the associated constrained covariance is projected/Schur-reduced."
- KUBO:60: "No such rule is selected here."
- ASM:701: "No bath, Gibbs temperature … is adopted."
- The calibration spec CS (fdeb5eb9) CA-01..CA-32 has no matching entry. A grep for isotherm, re-prepar, canonical, Kubo, retarded, zero mode, uniform lapse, maximum-entropy and quasi-static found nothing. A39(b) has now registered it as CA-34.

**3.4 Selection, by candidate.**

| Candidate (0497 list) | Record status | Grade |
|---|---|---|
| Thermodynamic variable with canonical fluctuations (T-ISO, h_NN(0) = −βVar(H)/L³) | Counted computational branch only (ASM:57; now CA-34). In tension with CRS:26 and :33 and KUBO:60. **Not selected by a premise** | FORMAL |
| **Constraint, fixed H / fixed preparation (T-FIX = T-GAUGE at the point)** | **Selected at k = 0** by KUBO:13/37/50/52, V002:13/20, CRS:31/33/34 and the binding-layer exclusions. The uniform lapse carries no fluctuation entry. Its value is fixed by the homogeneous background / normal-constraint solve, which is the owned WTC normal-constraint route (CI:114; ASM:1507, 1524; OCK:44). The consistent static form at k = 0 is: lapse row and column → 0, D(0) → D − F_jnF_nn⁻¹F_nj (H2a lemma; K3) | FORMAL |
| Local Lagrange multiplier at every k (T-LOC, "as in GR") | **Not selected.** V002 makes the lapse an affine local source with nonzero nonuniform E_α response (KUBO:28 "does not imply individual nonuniform-energy entries vanish"). Its owned-named realization, a cellwise fixed proper temperature (KUBO:60; FLOAT:106-111), is named but explicitly unselected. As a GR Hamiltonian-constraint multiplier it is an IMPORT CANDIDATE. Either way it gives repulsive −1/k⁴ | FORMAL + TESTED |
| T-FIXC (conserved uniform chart reads quotiented) | The S reads are **not** conserved. Reads are diagonal functions of n_e (OP:159-167); flip is an H term changing n_e with amplitude −h_e ≠ 0 (OP:124; TRIAL h = 0.1); so ⟨y\|[H,O]\|x⟩ = H_yx(O_x − O_y) ≠ 0 for S. For the uniform R read, H2a §4's flip increments (t_a −2Zf, t_b +2Zf under B = −A frames, OP:165) cancel pairwise when both endpoint cells have equal m_α. Its conservation then rests on Birth surgery and the cell weights. **UNTESTED.** Deciding computation: matrix elements of [H, Σ_α R_α] for the Birth primitive on OP's reachable component. Either outcome is non-attractive (H4-T1 restricted). HYPOTHESIS: V004's near-singular D(0) (0 hop/bind/admit) reflects a nearly conserved R | FORMAL / UNTESTED |
| Other: fixed proper β at k = 0 only (KUBO:60 rule b) | Gives 0 for the uniform EE entry, like T-FIX (K3: d²lnZ/dN² = 0), with a one-point EO contact −β⟨O⟩. Unselected | FORMAL + TESTED (toy) |

**Answer to 0497 item 2.**
- At the point k = 0 the record selects the constraint typing.
- The record does **not** decide the far field, because the far field is the k → 0⁺ limit of the k ≠ 0 response (§2).
- Under the selected typing, T(0) at the point is not a kernel value: k = 0 goes to the background solve.
- T(0⁺) = v/(Eref F_nn(0⁺)) depends on the continuation. That makes it **UNTESTED**, with the deciding computations U1 and U2 (§7).

**One more consequence, not in the helpers.**
- CRS:27 and :31 type the k ≠ 0 entries as retarded static responses of a stationary state, not as isothermal Kubo–Mori entries. The difference is the degenerate-block term (ASM:693-699).
- On the comparator it is 0 at odd m and 0.8–3% at even m, falling with N.
- On the owned parent it is UNTESTED. Its k → 0⁺ limit is H2a's frozen fraction f_E (U2).

## 4. H1 deliverable — framing gate

**4.1 Lineage: PASS.**
- One model throughout: owned parent P26 (OP a04f8795), TRIAL couplings, β = 1, the S4 estimator (7d079892), the CARD/CB/SAB read-off and the 37 registered L = 4 estimates (INV 1833cca4 + CHK 153d4ad0, with RAW_REWEIGHT excluded as element-identical to V004, max |Δ| = 0.0, TESTED).
- The typing entered at SPEC:2/61 (915e8a43, 2026-10-16) and was implemented at S4:351-352. Its uniform consequence was recorded at REVIEW_0407:71/109 (f8627adb). Its reach consequence was first drawn on 2026-10-17 (A12/RD3/RD4/A20).
- No result from a different construction is used as evidence (CI:93):
  - FLOAT (84a212a3, the C8 construction) is cited only for algebra that I re-derived on the current objects (K3);
  - the Codex3 constraint constructions (H1 P-C3a–e) are prior work only.

**4.2 Prior-work ledger (what this work did not repeat and what it built on).**
- PR:62 H2: "Reach is measured … any coupling (Γ-priced, Bind-priced or other) … on equal footing". This work measures; it does not select a coupling.
- KUBO (a7d048c1; PASS_SCOPED at ASM:179).
- ASM:674-703 (fixed-occupation vs Gibbs split).
- LIVE:142.
- FSPK:5-25 (finite-parent z⁴ limit; "No interchange of limits is established here").
- CEPL:32/54.
- CRS (032a564b).
- SPEC:61.
- FLOAT:103-111 (2026-10-05: fixed proper β gives zero uniform curvature, and the fixed-coordinate −βVar(H) is not "gravity").
- FROM_CODEX3/0032:16 ("Uniform-lapse retarded and isothermal responses are correctly different").
- RD3, RD4 and A12/A20/A21.
- Label correction to 0497:20: CB-LOC-01 and CB-OWN-01 are the concurrent-Birth occurrence and ownership postulates (LEDGER:28, 30), **not** the lapse assumption. The proper-time rule is V002 (494d0124), adopted at b5e7c2e3 and counted as CA-27 (FORMAL).

**4.3 Imports ledger: new load-bearing imports = none.**

| Item | Class | Use |
|---|---|---|
| H-CL (continuity of static correlations at k → 0⁺; ensemble equivalence) | HYPOTHESIS, not owned (LIVE:41) | Every conclusion that uses it is conditional and graded UNTESTED (U1) |
| Hydrodynamic order of limits for conserved densities | COMPARATOR / IMPORT CANDIDATE | Frames U2 only |
| GR lapse multiplier and Hamiltonian constraint | COMPARATOR; IMPORT CANDIDATE if adopted for the native block | T-LOC row only. TESTED to give −1/k⁴, so adopting it would not restore a tail |
| Continuation rules CONT6 / CONT8 | IMPORT CANDIDATE or new counted closure (CARD:124 requires every point) | Illustration, and the proposed version's declared rule (§6) |
| Mixed-field spin ring (K3) | COMPARATOR model | Algebra checks only |
| G = 6.67430e-11, c | COMPARATOR | Q = T/T_N and the closed form for k_p only |
| kpc = 3.0856775814913673e19 m | unit | — |
| Eref, γ, ℓ_F (LWRJ anchor block) | calibrated UNT parameters, counted | Read-off only |

**Gate result: PASS.** No GR answer is used as a premise. The constraint typing at k = 0 is derived from owned lines (§3).

## 5. H3 deliverable — kernel limits per typing (K1; 37 estimates × 13 rays = 481 rays; 25 admissible = 325 rays)

Every edit acts on a copy. The verdict is the small-k exponent p = dln|T|/dln k at 1e-7–1e-6 /kpc, with sign; T > 0 is attractive.

| Typing (edit) | h_NN(0) | T(0) / T(0⁺) | Small-k law | 1/r tail? | Zeros / poles | k*/k*_ISO | Gate | Q∞ effect |
|---|---|---|---|---|---|---|---|---|
| **T-ISO** (registered) | −βVar(H)/L³: −24.4 … −0.157 (A2 −3.551) | −878 … −5.73 m³/J (adm −537 … −5.73; A2 −39.73) | finite, repulsive 481/481 | **No** (finite reach) | 1 zero per ray, 0 poles; k* 0.00253–0.0995 /kpc (A2 z 0.01655) | 1 | 25/37 pass | none |
| T-FIX at the node, D kept (FIXN; also PT at k = 0) | 0 (row and column 0) | diverges | k⁻², **repulsive** 481/481 | repulsive 1/r (CA-28 interpolation artefact) | 1 zero, 0 poles | 1.000 exactly | marginal (λ_max = 0) | dQ(2) ≤ 1.2e-5 |
| **T-FIX consistent quotient** (FIXH: lapse row/col 0, D → Schur) | 0 | diverges | k⁻², repulsive 481/481 | repulsive 1/r (artefact) | 1 zero; 0 poles on admissible | 1.00–2.67 (adm) | marginal | dQ(2) ≤ 3.6e-5 |
| **T-FIX/T-GAUGE + continuation** (CONT6 / CONT8: node from k ≠ 0 shell) | not used (quotiented) | CONT6 −1512 … −54.4 (A2 −63.76); CONT8 −1256 … −63.6 (A2 −69.75) | finite, repulsive 481/481 | **No** (finite reach) | 1 zero, 0 poles | CONT6 0.52–2.02, CONT8 0.54–1.89 (adm) | pass | dQ(2) ≤ 2.1e-4; dQ(0.3) ≤ 3.2% |
| T-LOC (lapse row/col 0 at every node; = cellwise PT) | 0 | diverges | k⁻⁴, repulsive 481/481 | no; repulsive linear potential | 1 zero, 0 poles | 1.000 | marginal | dQ(2) ≤ 4.8e-5 |
| RD3 probe (h_NN(0) := 0 only) | 0, cross terms kept | diverges | k⁻²: 173 attractive / 308 repulsive | attractive only with a pole on every such ray | 481 zeros, 173 poles | 1 | **violated 37/37** | — |
| Illustration: C2 only (SOFT6ISO, D(0) × 1e6) | ISO | = T_ISO(0) | finite repulsive | **No.** Pole at k_p (§2.2) | zero removed on 479, pole on 481 | — | pass | Q ≈ Q∞ only above k_p |
| Illustration: C1 + C2 (SOFT4/6 on FIXH) | 0 | diverges | repulsive below k* | Q∞-Newtonian only above k* ∝ λ^−1/2 | 1 zero | 0.010–0.028 (1e4); 0.0010–0.0028 (1e6) | marginal | Q → Q∞ |

Over all typings, |Q(1000/kpc)/Q∞ − 1| ≤ 8.1e-9, with Q∞ = 8.0623. The A21 lapse entry −1/4 and Q∞ are grid-free (SAB EH block; V4A A21), so no typing reaches them.

## 6. Consequences and implementation note (new model version only; no code)

**6.1 Far field per admissible typing.**
- T-ISO (baseline, CA-34): finite reach, repulsive below k*.
- Spec-compliant T-FIX/T-GAUGE: finite reach with the magnitudes set by the continuation rule. CONT6/CONT8 move T(0⁺) by ×0.47–18.8 relative to T-ISO (H3's three rules: ×0.39–27) and k* by ×0.52–3.6 per estimate; the sign is unchanged.
- T-LOC (not owned): repulsive linear.
- A 1/r tail exists only if C1 ∧ C2 ∧ C3 hold in the infinite-volume k ≠ 0 response (U1, U2).

**6.2 Recomputation.** The baseline is unaffected: it is the control (A29, A39). The list below is H4 §5, corrected.

| Item | Spec-compliant version (k = 0 quotiented, k → 0⁺ from k ≠ 0 data) |
|---|---|
| 37 raw L = 4 grids | unchanged (raw source Hessians); node 0 is no longer consumed |
| Read-off (T(k), k*, t2/t4; t3 needs the NGC cube, not opened here) | re-read (done here for t2/t4-type numbers) |
| DDO154 calibration, CS, freeze, NGC route A/B, 120/43 predictions, lensing (P-87) | recompute; new CS entry for the declared continuation rule |
| C5/C6 and R3 UV results; tail-scheme formula | carry over within dQ ≤ 2.1e-4 at \|k\| ≥ 2 /kpc. EPS/LO certificates are re-evaluated (cheap) |
| IR treatment | **not needed:** T(0⁺) is finite. H4's IR requirement applies only to the rejected node-interpolated T-FIX |
| NGC k-grid fidelity | re-read (no new IR singularity) |
| P-96 stage 0 | capture unchanged. The read-off rule is re-sealed, because PREREG_STAGE0 readings are T-ISO-specific (H4; not re-verified) |
| BH-D | unaffected |

**6.3 Implementation (version tag, for example `UNT-GAL-M0-K0SPEC-V001`).**
1. **k = 0.** Never enter the native kernel. The uniform energy direction is a declared zero mode, passed through the existing 0405 `declared_zero_modes` / `energy_quotient` inputs that SAB leaves trivial (SAB:130-133). The homogeneous background and global energy come from the separate background / normal-constraint solve (SAB:190; QV5:84 already refuses k = 0; CRS:33-34). Use a bordered system if any uniform source column is needed (OCK:40). No regulator, no pseudoinverse.
2. **CARD successor.** The k → 0⁺ symbol and the reciprocal-lattice images take their values from k ≠ 0 nodes only, under one pre-registered continuation rule, counted as a new CA. CRS:33 requires this, and CARD:124 / LIVE:41 forbid an invented rule, so the rule must be declared. Candidates: node-excluded renormalized Fejér weights; a first-shell mean; or, once L ≥ 6 exists, a multi-shell extrapolation in |k|². Report the rule spread (here ×0.5–3.6 in k*) as closure uncertainty.
3. **Estimator.** S4 bytes are unchanged at k ≠ 0. Declare the isothermal k ≠ 0 entries as the estimator of CRS:31's retarded static entries. That is a counted approximation; its error is the degenerate-block term (U2).
4. **Gate.** GATE:100 applies at the consumed nodes only. The 12 failing estimates stay excluded (A39(e)).
5. **Custody.**
   - a typed-closure module sha;
   - a driver successor allowlist entry (v008:336-340 lineage, after v010);
   - a new seed record;
   - new route-A runs (the checkpoint digest at v008:1441-1447);
   - then DDO154 recalibration → freeze → out-of-sample 120/43 alongside the baseline. Never fitted, never relabelled as an `approximation`.
6. **Pre-registered expectation** (from §5): finite reach on every ray, the same Q∞, and outer-row depth changed only in magnitude. The tail question is not addressed by this version. It needs U1/U2.

**Not recommended:** T-FIX at the node inside CA-28 (FIXN/FIXH). It substitutes across typings (KUBO:60), violates CRS:33, and produces a ~10⁵ repulsive interpolation artefact.

## 7. UNTESTED items and deciding computations

- **U1 (decides C1 and C2 under H-CL).**
  - Data: mixed captures at an L = 4 control and L ≥ 6 (P-96 stage 0 running; stages 1–2 later).
  - Compute per shell: h_NN(q), Γ_nn(q), the transverse-trace chart susceptibility u_TTᵀD(q)u_TT and the soft eigenvalue of −D(q).
  - Rules: if F_nn(0⁺) ≠ 0 or the chart stiffness is nonzero beyond 2 SE (RD4 P6), the prediction is finite reach. If both vanish as q², compute the tail coefficient and its sign.
- **U2 (decides C1 when H-CL holds).**
  - Compute the energy-density relaxation rate Γ_E(k) of the owned parent at the smallest accessible k, using the fixed-preparation real-time provider (ASM:57) in native time T₀ (ASM:61) converted with Eref. Alternatively, compute the frozen fraction f_E(k) by exact diagonalization of small owned domains (H2a D1).
  - Rule: the static order holds at k_g ≈ 0.02–0.03 /kpc only if Γ_E(k_g)·t_gal ≫ 1. Otherwise rebuild the kernel in the retarded order.
  - A k² extrapolation of Γ_E is an import candidate unless several k are measured.
- **U3 (T-FIXC bookkeeping; not a tail decider).** Exact [H, Σ_α R_α] for the Birth primitive on OP.
- **U4.** The H4 real-space proxies, re-run under the spec-compliant continuation rule. This needs t3 on the NGC iteration-0 cube (root-run; not opened here).
- **U5.** Within CA-28 only analytic forms in k² are representable. Whether the infinite-volume response is non-analytic at k → 0 is not decidable from L = 4/6/8 alone (LIVE:41).

## 8. Manifest

`HASHES.txt` (written last) lists the sha256 of every file in this directory, except itself. This report cannot hold its own hash. Main inputs:

| Input | sha256 |
|---|---|
| 0497 | f1779659fab3f6d44323ba2a593d3cde4bd2da12b7eea1192f688f3b7a18147d |
| H2b md / H4 md (verified) | 17b72917763dfef11bd750ad4de2608413f49ad218316cce4d1a6af7e75558ca / b9ce950e409b08b4b57273ab8888a911e2a99e0c14faa7a713da9ab6e49c9ec4 |
| H2a md / H3 md / H1 PARTIAL / C4 synthesis (read after K4) | cefd4a08… / 0fdf0479… / e55c2524… / 473497f9… (full hashes in `out/C4_INPUT_TREE_SHA256_V001.txt`) |
| GRID_INVENTORY / CHK_E / LWRJ | 1833cca4… / 153d4ad0… / d3f32335… |
| CARD / CB / SAB (copies = pins) | 4d123c1f… / 701095f9… / 7130a277… |
| CRS / V002 / KUBO / S4 / ASM / CS / V4A (as read) | 032a564b… / 494d0124… / a7d048c1… / 7d079892… / 06a75173… / fdeb5eb9… / 9b88e8a1… |
| Other record files | sha256 as printed in `out/R0_RECORD_LINES_V001.txt` |
