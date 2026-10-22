# BH-D step 1: the qualified loop observable and a same-history Bind-dependent response — V001

2026-10-17/18, Claude2 BH-D workflow, step 1. Authority: V004 addendum A29 workstream 4 (cited by name; V004 is open) and A10 in the frozen V003 addendum (5bef6552). Framing: BIND_HISTORY_FRAMING_V001 (1bbdb88c) with the binding corrections of CHECK_V001 (3cd8a0eb). Pre-registration: `PREREG_BHD_STEP1_V001.md`, sha256 2cd25b3d…, sealed at 2026-10-18T01:10:53Z, before any response was evaluated (`results/PREREG_SEAL_V001.txt`).

Run conditions: no production or root launch, and no program producer was executed. The computation used my own code under nice -n 10, one process, single-thread BLAS, with exact integer and Fraction arithmetic, about 50 s of CPU in total. No NGC3198 target was opened. Nothing was imported.

**Verdict: BHD1-NONZERO** (pre-registered rule, PREREG §5) [FORMAL-RESULT].
- The setting is the complete literal-7 Hjoin with the actual W/C history and the reviewed complete-domain hex read F_C.
- The same-history contrast Δ_C(T) = Tr[F_C U(T)(ρ_W−ρ_C)U(T)†] has exact, nonzero, Bind-dependent Taylor coefficients.
- This holds for all 12 simple 6-cycles through the writer site v at L = 4, and for 36 of the 58 cycles on the roster.
- Every control passed. The positive control reproduces A1's +1/448 exactly.
- What this establishes: **non-identity** (nonzero somewhere on an open, unlocated set of the declared coefficient/time family).
- What it does not establish: the LR:29 finite exit, which needs a margin with controlled error at a declared member. That remains UNTESTED (§6).

Path keys: as in PRIMER:11-51 and BIND_HISTORY_FRAMING_V001:7-30, plus the following.
- HXR = C1/READINESS_P26_NATIVE_HEX_READ_AND_GAMMA_QUALIFICATION_PROPOSED_V001.md
- HXRR = its distinct review, C1/READINESS_P26_NATIVE_HEX_READ_DISTINCT_REVIEW_V001.md
- HXC = C1/READINESS_P26_NATIVE_HEX_READ_DIRECT_COMMUTATOR_ADDENDUM_V001.md
- A1 = C1/ACTUAL_WRITER_TO_INCIDENCE_COEFFICIENT_PROPOSED_V001.md
- WR2 = C1/NATIVE_WRITE_EVACUATION_INTERFACE_PROPOSED_V002.md
- MSD = C1/FIRST_NATIVE_CAPABILITY_MILESTONE_REVIEW_AND_Q_DIAGNOSTIC_PROSPECT_V001.md
- P26T = C3/READINESS_P26_BIND_INCIDENCE_TRANSFER_PROPOSED_V001.md
- LPW = C1/READINESS_P26_COMPLETE_LOOP_PROBE_WORK_INTERFACE_PROPOSED_V001.md
- EVJ = HLP/coefficient_method/EVOLVED_FULL_PARENT_LOOP_WORK_JETS_AND_DIAGONAL_FAMILY_NULL_PROPOSED_V001.md
- OPA = X/claude_artifacts/owned_retained_response_0405/owned_parent_operator_v003.py (a04f8795)
- OPB = …/owned_retained_source_columns_v002.py (173f608d)
- UN = …/USAGE_NOTE_0405_V001.md
- FC = …/FINAL_CHECK_0405_V001.md
- PC1 = "FIRST_CHUNK_PREMISE_CARD_V006.md" in the 20260924 Packet Updates folder (74514b8a)

## 1. Definitions from the record

### 1.1 The "qualified loop observable"

LR:23 states the requirement:
- "Keep the existing full Hjoin, actual W/C states, source history, resource accounting and prospectively fixed read interval."
- "specifying an actual closed-loop incidence effect or coherent loop operator on both complete old/Born sectors, including its action outside the eligible image."
- "Qualify its preparation/read meaning and distinguish contractible loop changes from a claimed Gamma-level protected class."
- "A count of occupied edges or a ring term in an effective generator is not by itself this qualification."

The response is LR:25: "the SAME-history contrast Tr[O_loop U_H(T)(rho_W−rho_C)U_H(T)^dag], with native q-mediated insertions and other owner contributions kept separate. First determine whether a Bind-dependent coefficient survives actual loop support/orientation/symmetry."

The comparison references are LR:27. H0 = Hjoin − g p_v X_qv and H1 = H0 + λ_R d_v q_v are "mathematical references, never resets or physical switches" (the same text is at MSD:15-19).

The exit is LR:29: "an explicitly qualified loop observable plus a nonzero same-history Bind-dependent response with its competing channels and controlled error on the retained preparation."

**The record's instance of O_loop** is the complete-domain hex read (HXR:15-28) [DECLARED-PREMISE: interface; distinct review PASS_SCOPED_COMPLETE_DOMAIN_READ_AND_DIRECT_COMMUTATORS, HXRR:12].
- C is a prospectively fixed simple six-cycle; no cycle may be chosen after a response is measured (HXR:15).
- a_C and b_C are its two alternating words. G_C is the projector onto "exactly ONE of the two off-cycle incident edges is occupied at each cycle vertex" (HXR:17).
- Π_C = G_C(|a_C><a_C|+|b_C><b_C|) and F_C = G_C(|a_C><b_C|+|b_C><a_C|) act on the complete incidence cube. They are tensored with identity on every q, carrier, cell and donor factor (HXR:19-26).
- The effects E_{C,±} = (Π_C ± F_C)/2 and E_out = I − Π_C are orthogonal and sum to the full identity (HXR:24-26; HXRR:14).
- On unavailable levels, E_out = I. "This is a complete finite-domain incidence-coherence measurement even on off-image Born states, failed reverse states and depleted donors" (HXR:28).
- **Direct commutators.** F_C commutes with Bind, admission, every d_v and −λ_R Σ d q. "A Bind-dependent loop-read contrast, if one exists … must arise through intermediate dynamics and nested commutators" (HXC:7-13; HXRR:16-18).
- **Read meaning and protection.** A hex is a contractible loop. F_C "is not evidence for a nonlocal protected class" (HXR:36). It "would establish only a source-sensitive native loop read" (HXR:44). The qualification therefore separates contractible loop changes from Γ-protection, as LR:23 asks, by declaring that the read claims no protection.
- **The work-conjugate companion** is W_θ = Tr[ρ(U_θ†H U_θ − H)] with ΔW_θ(t) defined on the same W/C (LPW:13-22). Its first time-jet vanishes exactly for incidence-diagonal inputs (EVJ:34-46).

### 1.2 "Both complete sectors"

- These are the old block and the one-Born block of Hjoin = [[H7_old+Hcell_old+HA_old, ε_B* Tjoin†],[ε_B Tjoin, H7_new+…]] (V005:11-12).
- The full sector space keeps "all Nc=0..Nv and all Born off-image states" (V005:4).
- The Born block adds two stars and four edges (V005:4; PC1 Packet A "Sectors": ℋ0 with N_birth = 0 and ℋ1 with N_birth = 1).
- "Outside the eligible image" means the Born-sector states not in the range of Tjoin = F_q4 P_(S_cut=2) (V005:15).
- Any reference offset "must act identically on both complete sectors and their complements" (V005:15).
- On the loaded P26 parent the same requirement becomes every level of the direct sum H_K, with E_out = I on unavailable levels (HXR:28; P26T:7).

### 1.3 The retained preparation

The W/C histories are the exact states of WR2:17-26. The parent is sharp Q = M = 1, with one active cell at v = A(1,1,1). The incidence starts as n_vu = n_ab = 1 with every other n_e = 0, and all q are 0.
- **W:** v Ready, with no carrier.
- **C:** v Spent, with one carrier at a = A(1,1,0).

These are the states of the reviewed coefficient A1 (+T⁸/(448ħ⁸), LR:7) [FORMAL-RESULT, reviewed].

## 2. Can existing owned-parent code evaluate it now?

**No, not at any admissible L, for the finite-coupling quantity** [FORMAL-RESULT: code read and dimension count].

| Code | What it is | Can it evaluate Δ_C? | Cost at the smallest admissible size |
|---|---|---|---|
| OPA `build_owned_operator`/`apply_H` (0405 module A) | Sparse H of the owned populated parent: M_v = 1 at every site, 8 local states, N_c = S_g (UN:23). It requires a 4-regular bipartite G0 (UN:44). The basis is "the structural reachable component … whatever the coefficient values" (UN:60, 133). Its reads are diagonal (UN:113) | No. F_C is off-diagonal and is not among the reads. The domain contains no I cells, so the actual V005 W/C preparation cannot be represented | With h ≠ 0 the reachable space is the full incidence cube, of dimension at least 2^E·2^V·C(2V,V). At K = 0 slots: K_{4,4} gives 2.16e11; the L=2 diamond (32 bonds) gives 1.69e23; L=4 gives about 10^191 |
| OPB `propagate_source_columns` (0405 module B) | The fixed-preparation real-time provider: Taylor stepper, linear retarded response at n = 0, j = 0 (UN:27). Status "UNTESTED: neither has ever been executed" (FC:15, 167) | No. It has the reads of OPA only, and it inherits OPA's dimension | Same as above |
| Static worldline sampler (owned_collective_worldline_static_response_pairallk_v00x) | Static β = 1 closed-worldline sampling. "Static sampling is NOT real-time evolution" (ASM:57-59) | No. It has no time axis (TM:16), and its mixing is TESTED-NEGATIVE (PRIMER:128) | — |
| P49 Krylov N2 (lanes/P49_CODEX2) | Certified real-time evolution on a fixed 10432-state component (krylov_full_n2_chunk_math_v001.py:25). Its reads are four two-bit words and six diagonal censuses (same file:7-8). It predates the owned parent (CHECK_V001:72) | No. It has no six-cycle read, and its parent differs | — |

Exact real-time evolution on the complete space is out of reach at every admissible L. The record's own method for this question is exact coefficient extraction inside the complete generator: "No huge basis is needed" (P26T:22; A1). The pre-registered deciding computation uses that method (§3). It runs in seconds, so it ran.

## 3. Pre-registered deciding computation (summary of PREREG_BHD_STEP1_V001)

- **Family.** Φ_C is the part of Δ_C at zero degree in every coefficient except (h, λ_R, κ, g). The excluded coefficients are Δ, U_d (with d*), ε_c, t and θ, ε_r, λ_J, E_I, E_R, E_S and ε_B. This is monomial extraction inside the complete Hjoin (P26T:20-22), not a physical switch-off.
- **Monomials.** Each monomial h^m λ_R^a κ^b g^c carries T^(m+a+b+c); its coefficient c_C(m,a,b,c) is an exact rational. The admission phase is fixed by the A1 rephasing (A1:43).
- **Exact structure used.** In this family the arm state factorizes: (4 edges at the active site ⊗ local resource) ⊗ free edges under −hX.
- **Roster.** At L = 4 (primary) and L = 3, 2 (secondary), every simple 6-cycle whose read support meets E(v) ∪ E(a). The roster is graph-derived and fixed before any evaluation.
- **Orders.** m ∈ {m_min, m_min+2}. Below m_min the read is structurally zero.
- **Measured quantities:**
  - P1: the W-source Bind chain (b=2, c=2, a≥1) and the C-arm control-carrier Bind channel (b=0, c=2).
  - P2: the competing λ_J d p channel, kept separate.
  - P3: the retained-q diagnostic Γ = D0 − D1 (MSD:13-27).
- **Controls:**
  - K1: A1 reproduction, which must give exactly 1/448, or the run is void.
  - K2: g = 0, nonzero exposure with exactly zero writing (P47L:13).
  - K3: λ_R = 0 decoupling.
  - K4: unitarity.
  - K5: reality.
  - K6: brute-force check of the factorization.
- **Statistics.** None are needed, because every number is exact; "nonzero" means an exact rational ≠ 0.
- **Born sector.** Monomials at zero ε_B degree live in level 0 (P26T:22). The Born-level F_C block is fixed in PREREG §1 but enters only the |ε_B|² monomials, which are not computed here.

## 4. Results

### 4.1 Controls (all PASS)

| Control | Result | Status |
|---|---|---|
| K1 | Coefficient of h²λ_R²κ²g² in Δ[n_vu] = **1/448 exactly**, at L = 4, 3 and 2. This is an independent implementation reproducing the reviewed A1 | FORMAL-RESULT |
| K2(i) | Exposure Tr(p_v ρ_W): κ²T² coefficient = 1 at g⁰. Exposure is nonzero | FORMAL-RESULT |
| K2(ii) | Tr(q_v ρ_W): every g⁰ coefficient = 0. Writing is exactly zero, matching P47L:13 | FORMAL-RESULT |
| K2(iii) and K3 | No nonzero Δ monomial with g⁰ or with λ_R⁰, on every cycle at every L | FORMAL-RESULT |
| K4 and K5 | Tr ρ = 1 with no other terms; every Δ coefficient is real | FORMAL-RESULT |
| K6 | Brute-force 2^18×4 propagation against the factorized evaluation at the test point (0.3, 0.7, 0.5, 0.6). \|diff\| = 2.8e-22 on values near 8.7e-8. W−C = −2.1629001492489e-10 in both methods. A supplementary point (0.8, 1.1, 0.9, 1.3), not pre-registered, gives W−C = −1.18820832543e-6 in both | FORMAL-RESULT (numerical check) |

### 4.2 P1: Bind-dependent coefficients [FORMAL-RESULT]

| L | Roster cycles | With nonzero W-source Bind chain | Cycles through v that are nonzero | Winding cycles that are nonzero | With a nonzero C-arm control-carrier channel |
|---|---|---|---|---|---|
| 4 | 58 (all contractible) | 36 | **12 / 12** | — | 36 |
| 3 | 84 (28 winding) | 54 | 18 / 18 | 18 / 28 | 54 |
| 2 | 128 (96 winding) | 102 | 48 / 48 | 74 / 96 | 102 |

Example L = 4 cycles. Edge labels are the PC1 bond codes; every value is the coefficient of the stated monomial times T^n/ħ^n.

| Cycle edges | v on C | a on C | m_min | Δ: h^m λ_R² κ² g² (W-source chain) | Δ: h^m λ_R² g² (C-arm) |
|---|---|---|---|---|---|
| 81,144,147,85,84,83 | yes | yes | 16 | m=16: **+2/7**; m=18: −316/81 | m=16: −64/45; m=18: +20992/945 |
| 25,87,86,37,39,26 | yes | no | 16 | m=16: **−1/7**; m=18: +1268/567 | 0 |
| 21,84,86,37,36,22 | yes | no | 18 | m=18: +4/7; m=20: −4208/567 | m=18: −64/45 |
| 21,83,82,33,35,22 | no (through u) | yes | 14 | m=16: +1/14 | m=14: +32/45 |

Census of Δ monomials at L = 4, over all cycles and computed orders: only (m,2,2,2) and (m,2,0,2) occur. Two exact nulls hold everywhere at every computed order:
- **every λ_R-odd coefficient vanishes**;
- every coefficient odd in κ or g vanishes.

This is an observed exact null at these orders, not a general theorem.

Reading [FORMAL-RESULT]:
- Δ_C and its Bind-dependent part Δ_C − Δ_C|_{g=0} are real-analytic and have nonzero Taylor coefficients.
- They are therefore not identically zero, and they are nonzero on an open, unlocated subset of the declared coefficient/time family (A1:79-85 argument).
- The leading W-source term has the A1 structure: two admission, two Bind and two feedback insertions, together with the m flips that build the gated alternating coherence.
- This is an admission → Bind → q-feedback → loop-coherence contribution in the actual history.
- Sign is cycle-dependent: +2/7 against −1/7 on two cycles through v.

### 4.3 P2: competing non-Bind channel [FORMAL-RESULT]

The λ_J d p channel (g = 0) is nonzero at the same h orders. On the first cycle above it gives h^16 λ_J²: −16/3 and h^16 λ_J²κ²: +128/45. Every cycle through v has a nonzero h^m λ_J²κ² coefficient.
- At a general member the Bind part is therefore not isolated by order counting. It has to be separated by its g-dependence or by the H0/H1 references (LR:25-27).

### 4.4 P3: retained-q diagnostic Γ = D0 − D1 [FORMAL-RESULT]

The checkpoint is at T0 = 1 under the full family generator. Stage two runs for time r under H0 (Bind at v removed) and H1 (feedback at v also removed). In this family the C arm cancels exactly from Γ, since p_v = q_v = 0 there.

Leading coefficients, h^16 λ_R² κ² g², for cycles through v with m_min = 16:
- the two cycles through both v and a: r = 1/4 gives 396728515625/25769803776; r = 1 gives **2²⁰/3**; r = 4 gives 27343750000000/3;
- the other six such cycles: r = 1 gives **−2¹⁹/3**;
- for m_min = 18 cycles, the h^18 coefficient at r = 1 is 2²³/3.

Reading: q_v, written by Bind during [0, T0] and then held conserved, changes the later loop read relative to the q-decoupled reference. Γ is not identically zero. This is the record's "retained source-q feedback" contribution (MSD:27), here on a loop read rather than on n_e. It is a sufficient-diagnostic coefficient, not the MSD:39-45 certificate: no exposure margin ε_W, ε_C is evaluated, and no member is chosen.

## 5. Claim classes

| Claim | Class |
|---|---|
| The qualified loop observable is the reviewed complete-domain F_C (HXR:15-28) and the "both sectors" definition of §1.2 | DECLARED-PREMISE (record interface, PASS_SCOPED) |
| No existing owned-parent code can evaluate Δ_C at finite coupling at any admissible L (§2) | FORMAL-RESULT (code read and counting) |
| Nonzero same-history Bind-dependent Taylor coefficients of Δ_C in the complete Hjoin with the actual W/C, at L = 4, 3, 2; non-identity on an open, unlocated set | FORMAL-RESULT |
| λ_R-odd null at the computed orders | FORMAL-RESULT (observed at these orders; no general proof) |
| A nonzero retained-q Γ on the loop read | FORMAL-RESULT |
| The competing λ_J channel is nonzero at the same orders | FORMAL-RESULT |
| The LR:29 exit: a margin with controlled error at a declared member | UNTESTED. Deciding test U1 |
| Born-sector (\|ε_B\|²) monomials and the U_d, Δ, t and ε_r monomials | UNTESTED. U2, U3 |
| Transfer to the owned parent (ASM:203) | UNTESTED. U4 |
| Γ-protection, tension, baryon map, 120/43 plug | UNTESTED. U5-U7 |
| DM working identification (MS:8) | HYPOTHESIS (unchanged) |

Scope:
- The results are exact computations on the program's own objects, with no record contact; under PRIMER:64 they are FORMAL-RESULT, not TESTED-POSITIVE.
- No result here is a statement about galaxies.
- The read is an incidence-coherence read of the collective state, not a baryon weight. This keeps CHECK_V001 finding 4: history may live in the Γ_ret collective state.
- C-124/125/131 are untouched; they refute exact closures only (CHECK_V001 finding 1). Nothing here is a Bind count.

## 6. What remains for the LR:29 exit, and the launch plan

None of these is a production launch. Each needs its own framing gate under A29.

- **U1, finite margin.** A writer-style certificate (WR2:101-125; MSD:29-45):
  - Choose a declared small-coupling neighbourhood under the framing gate, with no tuple chosen from outcomes.
  - Bound every monomial outside the computed family (B4-type remainders, WR2:73-78), and subtract the λ_J channel through the H0/H1 references.
  - Show |Γ| − ε_W − ε_C − remainder > 0.
  - This is analytic work for a distinct reviewer. A numerical full-space run is impossible (§2).
- **U2, Born sector.** Extend the extraction to |ε_B|² monomials. Birth first needs S_cut = 2 on the four cut bonds, i.e. h-flips there. The Born-level F_C block follows the PREREG §1 rule. It still factorizes in this family, so the cost is minutes.
- **U3, non-factorizing owners.** U_d, Δ, t and ε_r at low degree, by a linked-cluster coefficient extraction. U_d couples the four edges at each vertex.
  - The t² monomials carry the evacuation route of WR2.
  - The physical regime h/U_d = 1/5 (PC1 DP-h) instead needs the strong-coupling side. That side is the populated hex coefficient J(λ,g), which is "NOT CONSTANT in g" (HLP/coefficient_method/POPULATED_HEX_CENTERED_RECORD_FEEDBACK_AND_BIND_DEPENDENCE_PROPOSED_V001.md:80; proposed, and its review status was not established in this read). Joining the two is the open step.
- **U4, owned parent.** The owned inventory has M_i = 1 at every site and no I cells (UN:23). The V005 W/C cannot be embedded. An owned-parent W/C analog must be specified at a framing gate; it is not selected here (LR:29; HXR:42). The extraction then repeats.
- **U5-U7.** The record/protection qualification (G1-G3, P-60), the work/tension conversion (LPW; EVJ:62-66 second jet), and the baryon-to-record map with the 𝓡^(χ) plug (BIND_HISTORY_FRAMING_V001 §3 steps 3-6). These are unchanged.

**Named next step: U2 together with the U3 t² monomials** in the same exact machinery, pre-registered the same way. They complete the "both sectors" requirement and bring in the evacuation path.

## 7. Prior work built on (no restart)

- LR:23-29; HXR, HXRR and HXC; A1; P26T; WR2; MSD; LPW; EVJ.
- P47L:13 (the g = 0 control).
- CHECK_V001's additions: CI:66 ("test state sensitivity"), BL:71 F1 (formation history; nothing here chooses a history from residuals), GE-X47 (placement/topology). The roster dependence of sign and magnitude is placement-resolved evidence on that question at the coefficient level.

## 8. Imports ledger

None. The inputs are native operators, the actual W/C, the actual graph, exact cos/sin series and integer word counts. No fitted weight, ΛCDM fraction or t_P/α_s constant is used, and no observation.

## 9. Files (sha256 in HASHES.txt)

- `PREREG_BHD_STEP1_V001.md` (sealed before evaluation) and `results/PREREG_SEAL_V001.txt`
- `code/graph_roster.py`, `code/bhd_step1_coeffs.py` (P1, K1-K5), `code/bhd_step1_p2p3k6.py` (P2, P3, K6), `code/k6b_supplementary.py`, `code/summarize.py`
- `results/ROSTER_V001.json`, `results/P1_L4_V001.json`, `results/P1_L3_L2_V001.json`, `results/P2_P3_K6_L4_V001.json`, `results/K6B_SUPPLEMENTARY_V001.json`, `results/SUMMARY_V001.json`
- `BHD_STEP1_V001.json`; `check/` is left empty for checkers
