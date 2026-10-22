# BH-D step 2: pre-registered deciding computation (PREREG_BHD_STEP2_V001)

2026-10-18, Claude2 BH-D workflow, step 2. **This file is written and hashed before any response quantity of step 2 is evaluated.** Before it, only graph-only material exists in this folder: `code/graph_facts.py` and its output `results/GRAPH_FACTS_V001.json` (cut ends, neighbours, Born-level read availability; no dynamics), plus byte-identical pinned copies in `code/pinned/` of step-1 `graph_roster.py` (b01c35b6), step-1 `bhd_step1_coeffs.py` (87a863b1) and the literal backend `canonical_join_backend_v002.py` (0d28150f). Their hashes go into the seal file. Authority and framing as in step 1: V004 addendum A29 workstream 4 (cited by name; V004 open), A10 of the frozen V003 addendum (5bef6552); BIND_HISTORY_FRAMING_V001 (1bbdb88c) with its CHECK_V001 corrections. Inputs: `bhd_step1_c2/` (BHD_STEP1_V001.md f8df2336, PREREG 2cd25b3d, CHECK_V001.md).

## 0. What this is, and what it is not

- **It is** the named next step of BHD_STEP1_V001 §6: **U2**, the Born-sector |ε_B|² monomials via the Birth map Tjoin = F_q4 P_(S_cut=2), together with the **t² monomials of U3** (the native hop −t Σ n_e T_e(θ), which carries the WR2 evacuation route), in the same exact coefficient-extraction machinery (A1; P26T:15-22).
- **It is not** a physical-tuple evaluation, a margin with controlled error (LR:29 exit), an owned-parent result (CHECK F2: every result here carries the qualifier *V005 literal-7 Hjoin, sparse WR2 W/C*), Γ protection, tension, a baryon map or a galaxy input. Nothing is chosen after outcomes.
- **Class of every outcome: FORMAL-RESULT** (exact computation on program objects, no record contact; PRIMER:64). A nonzero coefficient is not TESTED-POSITIVE; a zero is not TESTED-NEGATIVE.
- **Prior work (CHECK F1).** The direct antecedent is C1/READINESS_ACTUAL_WRITER_HEX_SUPPORT_AND_COLLECTIVE_INPUT_PROPOSED_V001.md (AWH; review PASS_SCOPED_SUPPORT_ZEROS_AND_PROSPECTIVE_STATE_FAMILY). AWH:21-23 proves the ε-independent h-degree lower bounds and states that Birth-dependent paths "copy cut bits and change the available graph/read, and require their own full-domain analysis": U2 here is that analysis for the sparse witness. AWH:35 asks for an exact recurrence with the +1/448 regression and calls the implementation root-only with a resource preflight; this run stays inside the toy allowance (§6) and the custody ruling remains root's (as CHECK F1 recorded). AWH:39-45 redirects the test scope to the level-0 degree-two collective family; this step does not engage that redirect, and the write-up must say how the next step does.

## 1. Fixed inputs (record values; no new choice)

Everything in step-1 PREREG §1 is kept: V005 literal-7 Hjoin; periodic q4 diamond with Packet-A indexing; L = 4 primary, L = 3, 2 secondary; WR2 W/C (v=A(1,1,1), u=B(1,1,1), a=A(1,1,0), b=B(1,1,0); n_vu=n_ab=1; Q=M=1; W: v Ready, no carrier; C: v Spent, carrier at a, a an I cell); the read F_C on the step-1 roster (same cycle list, same identities); contrast Δ_C(T) = Tr[F_C U(T)(ρ_W − ρ_C)U(T)†], ħ = 1, T = 1 (each monomial carries T^(total degree)).

Added for step 2:

| Item | Fixed value | Source |
|---|---|---|
| Born graph | pinned backend `BirthMap`: kept old edges in order; for cut i with ends (a_i, b_i) the children (a_i, s_B), (s_A, b_i); s_A = 2L³, s_B = 2L³+1; cuts = shift-0 bonds at anchors (000),(100),(010),(001) | V005:4,15; PC1 Packet A; backend :118-164 |
| Tjoin | old word with S_cut = 2 → Born word with both children of cut i equal to n_cut_i, blank star factors, I cells at stars; Tjoin† = its adjoint (child pairs equal, S_cut = 2, stars blank) | V005:15; backend :145-164 |
| ε_B phase | removed by a fixed rephasing of the level-1 basis, so ε_B = e real; the e² coefficient equals the |ε_B|² coefficient (one-Born generator: no ε_B² or ε_B*² term can return to a level-diagonal read) | V005:11-13 |
| Hop | H_t = −t Σ_e n_e T_e(θ), T_e = phase·b_u†b_v + h.c. (backend :249, :260). At t-degree ≤ 2 every contributing history moves the carrier along one edge only, so θ is removed by a carrier-position rephasing | V005:6 |
| Level-1 read block | **R1** = step-1 PREREG §1 rule: the same six edges if all six exist in the Born graph, with G_C from that level's own off-cycle incident edges; otherwise F_C = 0 at level 1. **R0** = level 1 declared unavailable (F_C = 0, E_out = I there). Both are HXR:15/28-admissible specifications; neither has been framing-gated (CHECK F8). | HXR:15, 28, 30 |

**Born-sector decomposition reported (rule-independent).** Φ = Φ^(00) + Φ^(11), where Φ^(00) is the level-0 block of the read (ket or bra goes up and comes back) and Φ^(11) the level-1 block (ket and bra both born). Φ^(00) does not depend on the level-1 rule. Totals are reported under R1 (Φ^(00) + Φ^(11)_R1) and R0 (Φ^(00)).

## 2. Coefficient families

- **FB (U2).** Zero degree in every coefficient except (h, λ_R, κ, g, ε_B); extract the |ε_B|² part. Structure used (to be verified by K6-F, not assumed): with t = 0 the carriers stay at v (W) and a (C), neither of which is a cut end at L = 4, 3, 2 (GRAPH_FACTS). Then the cut block (4 cut bonds at level 0 ⊕ 8 children at level 1, with −hX on each and e(Tjoin + Tjoin†)) commutes with the rest, and the state is an exact product: cluster(E(x) ⊗ local resource) ⊗ non-cut free edges ⊗ cut block. Every read term of F_C^(0) and F_C^(1),R1 is a product over these factors.
- **FT (U3-t²).** Zero degree in every coefficient except (h, λ_R, κ, g, t), ε_B⁰; extract t-degree 2 (t⁰ is the step-1 family, t¹ must vanish). Structure: at t² each nonzero ket–bra history moves the carrier to exactly one neighbour w of its start site and back (or both sides end at w), because the read is the identity on the carrier and carrier positions are orthogonal. Hence the t² coefficient equals Σ_w of the t² coefficient computed in the cluster E(x) ∪ E(w) with the carrier restricted to {x, w} and resource (cell at v, carrier position, q_x, q_w). x = v (W, 4 neighbours, w = u is the WR2 route) or x = a (C, 4 neighbours). All other edges are free under −hX.
- **FTB (secondary).** t²|ε_B|², by the product of the FT cluster and the FB cut block, only where no t-cluster site is a cut end (GRAPH_FACTS: L = 4, 3 all w; L = 2 not for the two C-arm neighbours that are cut ends). Elsewhere UNTESTED.
- **Arithmetic.** Exact: Python integers and Fractions, and exact modular arithmetic with Chinese-remainder reconstruction under a computed magnitude bound, plus one redundant prime whose disagreement aborts the run. Because every number is exact, **"nonzero" means an exact rational ≠ 0**; no statistic is involved.

## 3. Measured quantities

- **P1 (U2), every roster cycle, L = 4, 3, 2.** For m ∈ [0, m_min+4], a, b, c ∈ {0,1,2}: Φ^(00), Φ^(11)_R1, and the totals, for Δ and for each arm. Channels as in step 1: W-source Bind chain b=2, c=2, a≥1; C-arm control-carrier Bind channel b=0, c=2, a≥1. Any nonzero coefficient below m_min is reported (AWH's bound does not cover Birth paths).
- **P2 (U3-t²), every roster cycle, L = 4 then 3 then 2 within budget.** For m ∈ [0, m_min+2], a ∈ {0,1,2}, b, c ∈ {0,2}: the t² coefficient of Δ and of each arm, also split per neighbour w. Channels: W-source (b=2, c=2, a≥1), C-arm (b=0, c=2, a≥1), and the **hop channel** (c = 0): the carrier–incidence coupling n_e T_e is a direct non-Bind channel and is reported as a competing channel, not as a control failure.
- **P3 (FTB), L = 4 and L = 3 within budget.** t²|ε_B|² coefficients of Δ under R1 and R0, same index ranges as P2 with m ≤ m_min+4.
- **PJ (competing λ_J channel, kept separate, LR:25).** Same extractions in (h, λ_J, κ, ε_B) and (h, λ_J, κ, t) at λ_R = g = 0, at L = 4, for every cycle that contains v or a or whose read support touches the cut fiber: degrees a_J ∈ {1,2}, b ∈ {0,2}, m ≤ m_min+4 (FB) or m_min+2 (FT).
- **Separation of the λ_J channel.** By exact monomial label. The main families have λ_J-degree 0, so the λ_J channel is excluded from P1–P3 by construction, not switched off. PJ reports its pure (g⁰) monomials. Mixed λ_J^{≥1} g^{≥1} monomials are not computed and are UNTESTED. At a physical member the Bind-dependent part is Δ − Δ|_{g=0}; that removes the pure λ_J and pure hop monomials exactly and keeps the mixed ones.

## 4. Controls (pre-registered)

- **K1 (A1 reproduction).** O = n_vu: the h²λ_R²κ²g² coefficient of Δ equals +1/448 exactly in the FB pipeline (ε⁰ part) and in the FT pipeline (t⁰ part), at every L run. Failure → that pipeline is PIPELINE_FAIL and its P-results are void.
- **K7 (step-1 regression).** Every coefficient entry (Δ, W, C) published in step-1 `P1_L4_V001.json` and `P1_L3_L2_V001.json` is reproduced exactly by the ε⁰ part of FB and, at L = 4, by the t⁰ part of FT. Failure → PIPELINE_FAIL.
- **K2 (g = 0).** (i) FT: Tr(p_v ρ_W) κ² coefficient nonzero; (ii) FT: every g⁰ coefficient of Tr(q_x ρ) and Tr(q_w ρ) is 0 in both arms; (iii) every g⁰ Δ coefficient is reported. Expected: FB all zero; FT nonzero (hop channel), registered as the competing hop channel.
- **K3 (λ_R = 0).** Every λ_R⁰ Δ coefficient reported. Expected FB zero; FT possibly nonzero (hop channel).
- **K4 (unitarity).** Tr ρ has only the constant term in each cluster and in the cut block (P_0 + P_1 = 1 coefficientwise).
- **K5 (reality).** Every reported coefficient has exactly zero imaginary part.
- **K8 (parity).** On the L = 4 cycles containing v, for w = u: all odd-κ, odd-g, odd-t coefficients vanish (b, c ∈ {1}, t ∈ {1}).
- **KB1 (hand value).** [h⁴ e²] Tr(P_1 ρ_cut) = 2/3 (six S_cut = 2 words, two flip orders each, amplitude i e h² T³/3).
- **KB2 (level-transport invariance).** For O = n_vu ⊕ n_vu (the edge exists at both levels), every |ε_B|² coefficient of Δ is 0.
- **KT1 (hand values).** [κ²t²] Tr(p_u ρ_W) = 1/4 (T⁴, h⁰); [t²] Tr(p_b ρ_C) = 1 (T², h⁰).
- **K6-B (cut-block series, numeric).** For each cut-block operator used at L = 4: the exact e²-coefficient series in h, summed to h⁴⁰ at h = 0.3, T = 1, against a float64 second-order Fréchet (block-matrix) derivative of the evolution. Pass: relative difference < 1e-10.
- **K6-F (factorization, numeric).** Brute-force state-vector propagation, both levels, on the read support ∪ cut fiber ∪ E(v) with the W resource, at (h, λ_R, κ, g, e) = (0.3, 0.7, 0.5, 0.6, 0.4), T = 1, against the factorized numerical value. Cycle: the first L = 4 roster cycle (roster order) whose read support touches the cut fiber and whose level-1 brute-force bit count is ≤ 21. Pass: relative difference < 1e-10.
- **K6-T (single-neighbour decomposition, numeric).** For a cluster read operator, the t² coefficient (block-matrix derivative) of the joint model with carrier on {v, u, w₂} (w₂ the second neighbour of v in index order) equals the sum of the two single-neighbour models, at (h, λ_R, κ, g) = (0.3, 0.7, 0.5, 0.6). Pass: relative difference < 1e-9.
- **K9 (literal-backend conformance).** Using the pinned backend's own `channels` on the complete L = 2 graph, a sparse exact Taylor recursion gives the coefficients of Tr(Oρ) for O ∈ {n_vu, q_v, q_u, p_u, p_v} (W) and {n_ab, q_a, q_b, p_b} (C) through h ≤ 2, κ, g, λ_R, t ≤ 2; and of Tr(P_1 ρ) and of n_vu at |ε_B|² through h ≤ 4. These must equal the cluster/cut-block machinery's values exactly.

## 5. Decision rules (every outcome registers)

- **U2.** BHD2-U2-L0-NONZERO if some L = 4 roster cycle has a nonzero Bind-dependent (c ≥ 1) |ε_B|² coefficient of Δ in Φ^(00). Separately, BHD2-U2-R1-NONZERO if some L = 4 cycle has a nonzero Bind-dependent |ε_B|² coefficient in the R1 total. Pre-stated structural expectation (to be checked, not assumed): for a cycle whose read support at neither level touches the cut fiber, the R1 total vanishes exactly (level-transport invariance), while Φ^(00) equals minus the step-1 response convolved with the Born probability.
- **U3-t².** BHD2-T2-NONZERO if some L = 4 roster cycle has a nonzero W-source (b=2, c=2, a≥1) t² coefficient of Δ at m ≤ m_min+2. C-arm-only, hop-only, w-specific (route w = u versus edge-opening routes) and L ≠ 4 outcomes are reported as found.
- A zero at the computed orders is an exact zero there, not a no-go; the next order is named.
- No outcome changes the roster, W/C, read rules, families or index ranges after the fact.

## 6. Resources (runtime-only decisions)

`python3 -I -B`, `nice -n 10`, single-thread BLAS, at most 4 concurrent processes. Wall caps: FB all L ≤ 60 min; FT L = 4 ≤ 90 min, then L = 3 and L = 2 ≤ 90 min each; P3, PJ, K6, K9 ≤ 30 min each. A cap hit leaves the unfinished cycles UNTESTED (never negative), decided by runtime alone. CPU seconds are reported.

## 7. Imports ledger

None. Native operators, the actual W/C, the actual graph and Born map, exact series and integer words. No fitted weight, ΛCDM fraction or t_P/α_s constant; no observation; no NGC3198 file is opened.
