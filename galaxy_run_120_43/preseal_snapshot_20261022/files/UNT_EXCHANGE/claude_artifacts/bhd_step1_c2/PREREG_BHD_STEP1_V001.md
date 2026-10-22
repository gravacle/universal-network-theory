# BH-D step 1: pre-registered deciding computation (PREREG V001)

2026-10-17, Claude2 BH-D workflow, step 1. **This file was written and hashed before any response quantity was evaluated.** Only the graph-only roster `results/ROSTER_V001.json` (code `code/graph_roster.py`) existed before this file. It lists cycles and their minimum flip counts and contains no dynamics. Authority: V004 addendum A29 workstream 4 (cited by name; V004 is open) and A10 in the frozen V003 addendum (5bef6552). Framing: BIND_HISTORY_FRAMING_V001 (1bbdb88c) with the binding corrections of CHECK_V001 (3cd8a0eb).

## 0. What this computation is, and what it is not

- **It is** the record's own first finite question for Line A: "First determine whether a Bind-dependent coefficient survives actual loop support/orientation/symmetry" (LR:25). Its narrow form is READINESS_P26_NATIVE_HEX_READ_AND_GAMMA_QUALIFICATION_PROPOSED_V001.md:42 (HXR): "on the retained actual loaded W/C history, and a prospectively fixed cycle touching the writer region, does the complete same-parent expansion of Delta<F> contain a nonzero admission/Bind/q-feedback contribution after every support/orientation cancellation?"
- **Method.** Exact multivariate Taylor-coefficient extraction inside the complete generator. This is the reviewed method of ACTUAL_WRITER_TO_INCIDENCE_COEFFICIENT_PROPOSED_V001.md (A1, PASS) and READINESS_P26_BIND_INCIDENCE_TRANSFER_PROPOSED_V001.md:15-22 (P26T). It is not a physical switch-off of any owner and not a truncation of the dynamics.
- **It is not** an evaluation at a physical tuple. It is not a margin with controlled error (the LR:29 exit). It is not Gamma protection, tension, a baryon map or a galaxy input. No tuple, state or cycle is chosen after outcomes.
- **Class of every outcome:** FORMAL-RESULT. It is an exact computation on the program's own objects with no real-record contact (PRIMER:64). A nonzero coefficient is not TESTED-POSITIVE. A zero coefficient is not TESTED-NEGATIVE.

## 1. Fixed inputs (all from the record; no new choice)

| Item | Fixed value | Source |
|---|---|---|
| Generator | literal-7 Hjoin: old block, one-Born block, Tjoin and its adjoint | V005:4-15 |
| Graph | periodic q4 diamond supercell with the Packet-A indexing | FIRST_CHUNK_PREMISE_CARD_V006.md Packet A |
| Sizes | L = 4 primary (the first L whose 6-cycles are all contractible; roster). L = 3 and L = 2 secondary | roster |
| W/C | v=A(1,1,1), u=B(1,1,1), a=A(1,1,0), b=B(1,1,0); n_vu=n_ab=1, all other n_e=0, all q=0, Q=M=1, active cell only at v. W: v Ready, no carrier. C: v Spent, one carrier at a, a an I cell | NATIVE_WRITE_EVACUATION_INTERFACE_PROPOSED_V002.md:17-26 |
| Read | F_C = G_C(\|a_C><b_C\| + \|b_C><a_C\|) ⊗ I_rest on each level; E_{C,±} = (Π_C ± F_C)/2, E_out = I − Π_C | HXR:17-28; review PASS_SCOPED (READINESS_P26_NATIVE_HEX_READ_DISTINCT_REVIEW_V001.md:12) |
| Born-level block of F_C | The same six edges, if all six exist in the Born graph, with G_C built from that level's own off-cycle incident edges. Otherwise F_C = 0 at that level (E_out = I) | HXR:28 rule, instantiated here prospectively |
| Contrast | Δ_C(T) = Tr[F_C U_H(T)(ρ_W − ρ_C)U_H(T)†], one autonomous H, ħ = 1 | LR:25 |

**Cycle roster (prospective, graph-derived, HXR:15).** At each L, use every simple 6-cycle C of the old graph whose read support (cycle edges plus gate edges) meets E(v) ∪ E(a). Report every cycle with its identity. Nothing is averaged. Counts from the roster: L=4 has 58 cycles (12 contain v, 12 contain a, all contractible); L=3 has 84 (28 winding); L=2 has 128 (96 winding). Winding cycles are labelled non-contractible and reported separately. Neither class is called Gamma-protected (LR:23).

## 2. Coefficient family

Φ_C(T; h, λ_R, κ, g) is the part of Δ_C at **zero degree** in every other independent coefficient: Δ, U_d (and with it every d* term), ε_c, t and θ, ε_r, λ_J, E_I, E_R, E_S and ε_B. Equivalently, it is Δ_C evaluated at zero for those coefficients, read only as monomial extraction (P26T:20-22). The admission phase is fixed by the A1 basis rephasing (A1:20, A1:43), with κ real. Each monomial h^m λ_R^a κ^b g^c carries exactly T^(m+a+b+c), so its coefficient is one pure number c_C(m,a,b,c).

Structure used. On this family the only incidence–resource coupling is −λ_R d q. With t = 0 the W carrier stays at v and the C carrier stays at a. Edges outside E(v) (W) or E(a) (C) evolve under −hX alone. The arm state is therefore an exact tensor product: (4 edges at the active site ⊗ local resource) ⊗ free edges. Free-edge factors have exact rational series. Cluster amplitudes are exact integer word sums. **All arithmetic is exact (Python integers and Fractions).** Because every number is exact, no statistic or error bar is involved: "nonzero" means an exact rational ≠ 0.

Born sector. Every monomial with zero ε_B degree has no level-changing insertion, so it lives in the level-0 block (P26T:22). The Born-level block of F_C (§1) therefore does not enter these coefficients. **Monomials containing |ε_B|² are outside this computation. They are UNTESTED** (launch plan in BHD_STEP1_V001.md).

## 3. Measured quantities

- **P1 (primary).** For every roster cycle, c_C(m,a,b,c) for m ∈ {m_min(C), m_min(C)+2}, a ∈ {0,1,2}, b ∈ {0,1,2}, c ∈ {0,1,2}. Here m_min(C) is the roster's minimum pure-incidence flip count. Below m_min the read is structurally zero, since only h changes incidence in this family. Odd-parity m is structurally zero as well.
  - The **W-source Bind chain** at v is b=2, c=2, a≥1. It is the analog of A1 (admission → Bind → q-feedback).
  - The **C-arm control-carrier Bind channel** is b=0, c=2, a≥1. It is Bind of the relocated carrier at a; it is Bind-dependent but not the source chain at v.
  - Each arm's coefficients are also reported separately.
- **P2 (competing non-Bind channel, kept separate, LR:25).** The same extraction in variables (h, λ_J, κ) at λ_R = g = 0, for all L=4 roster cycles that contain v or a. Coefficients are c_J(m,a,b), a ∈ {1,2}, b ∈ {0,2}, m ∈ {m_min, m_min+2}.
- **P3 (retained-q diagnostic, conditional on budget).** The milestone's Γ(r) = D0(r) − D1(r) (FIRST_NATIVE_CAPABILITY_MILESTONE_REVIEW_AND_Q_DIAGNOSTIC_PROSPECT_V001.md:13-27). The checkpoint at T0 = 1 comes from the full family generator. Stage two runs for time r ∈ {1/4, 1, 4} under H0 = H − g p_v X_qv and under H1 = H0 + λ_R d_v q_v. The read is F_C, on the L=4 cycles that contain v, and the leading monomials are reported. P3 runs only if P1 at L=4 finishes within 20 minutes wall time. That decision depends on runtime alone, never on results. If P3 does not run it is UNTESTED, not negative.

## 4. Controls (pre-registered, same estimator)

- **K1, positive control (A1 reproduction).** O = n_vu ⊗ I in both arms. The coefficient of h²λ_R²κ²g² in Δ must equal **+1/448 exactly** (A1:12-18). If it differs, the whole run is registered **PIPELINE_FAIL**, and P1–P3 are reported as void, not as zeros.
- **K2, g = 0 (P47L:13: "g=0 has nonzero exposure but exactly zero writing").**
  - (i) The W exposure Tr(p_v ρ_W(T)) has a nonzero κ²T² coefficient at g⁰.
  - (ii) Every g⁰ coefficient of Tr(q_v ρ_W(T)) is exactly 0.
  - (iii) Every g⁰ coefficient of Φ_C is reported. The expectation is all zero on this family, and whatever is found registers.
- **K3, decoupling.** At λ_R = 0 (a = 0) every Φ_C coefficient is reported. The expectation is all zero, since incidence is then decoupled from resources on this family.
- **K4, unitarity.** In each arm, Tr ρ has only the constant term 1 through the computed degrees.
- **K5, reality.** Every Φ_C coefficient has an exactly zero imaginary part (F_C is Hermitian).
- **K6, independent factorization check.** For the first L=4 roster cycle that contains v, compute ⟨F_C⟩_W at one fixed real point by brute-force state-vector propagation on the full support space (2^|S| × 4) in float64. Compare it with the factorized evaluation at the same point. The point is h=0.3, λ_R=0.7, κ=0.5, g=0.6, T=1. It is a numerical test point only, not a physical tuple. Agreement means |difference| < 1e-9.

## 5. Decision rule (every outcome registers)

- **BHD1-NONZERO.** At least one roster cycle at L=4 has a nonzero W-source Bind-chain coefficient (b=2, c=2, a≥1) at m ≤ m_min+2. Reading: in the complete generator, with the actual W/C history and the qualified complete-domain hex read, the same-history Bind-dependent loop contrast is **not identically zero**. By analyticity it is nonzero on an open, unlocated subset of the declared coefficient/time family (A1:79-85 argument). [FORMAL-RESULT]
  - This does not supply a margin, a sign at a member, controlled error, q-exclusivity, Gamma protection, tension or DM.
- **BHD1-ZERO-AT-ORDER.** All W-source Bind-chain coefficients vanish through m_min+2 for every L=4 cycle. This registers as an exact zero at those orders on this family. It is not a no-go. Higher h orders and the U_d, t, ε_r, λ_J and ε_B monomials remain open, and the next order is named.
- **Mixed.** Nonzero only in the C-arm channel, or only at L≠4, or only on winding cycles: each is reported as found, with no reclassification.
- No outcome changes the cycle roster, the W/C states, the read or the family after the fact.

## 6. Imports ledger

None. Native operators, the actual W/C preparation and the actual graph; exact series of cos and sin; integer word counting. No fitted weight, no ΛCDM fraction and no t_P/α_s-type constant. No NGC3198 data is opened.
