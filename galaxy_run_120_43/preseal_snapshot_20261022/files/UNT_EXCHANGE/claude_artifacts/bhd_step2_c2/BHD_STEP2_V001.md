# BH-D step 2: Born-sector (U2) and hop t² (U3) Bind-dependent loop-read coefficients — V001

2026-10-18, Claude2 BH-D workflow, step 2. Authority: V004 addendum A29 workstream 4 (cited by name; V004 is open) and A10 in the frozen V003 addendum (5bef6552); V002 17c26616 is not consumed here. Inputs: `bhd_step1_c2/` (BHD_STEP1_V001.md f8df2336, PREREG 2cd25b3d, check/CHECK_V001.md). Pre-registration: `PREREG_BHD_STEP2_V001.md`, sha256 2563b31c…, sealed 2026-10-18T01:57:08Z before any step-2 response was evaluated (`results/PREREG_SEAL_V001.txt`; only graph-only facts and byte-identical pinned copies existed before it).

Run conditions: no production or root launch; no program producer executed (the pinned literal backend `canonical_join_backend_v002.py`, 0d28150f, is a definitions-only module and was used only through its `column_terms` for the K9 conformance check). Own code, `python3 -I -B`, `nice -n 10`, single-thread BLAS, at most 4 concurrent processes, exact integer/Fraction arithmetic (with exact modular CRT plus a redundant prime). Total CPU ≈ 5.7e3 (sum of the recorded runs; about 15 further minutes went to two aborted K6 attempts, §4) s. No NGC3198 target opened; `~/.codex` untouched. Nothing imported, nothing fitted.

**Qualifier on every result (CHECK F2).** V005 literal-7 Hjoin, sparse WR2 W/C, reviewed complete-domain hex read F_C on the step-1 roster, exact monomial extraction at zero degree in every owner not named in the family. **None of this is an owned-parent result** (A29 workstream 4 asks for that; U4 below).

## Verdicts (pre-registered rules, PREREG §5) — all FORMAL-RESULT

1. **U2 (|ε_B|², via Tjoin = F_q4 P_(S_cut=2)).**
   - **BHD2-U2-L0-NONZERO.** In the level-0 read block Φ^(00) (independent of how F_C is defined on the Born level) the Bind-dependent |ε_B|² coefficients are nonzero on 57 of 58 L = 4 cycles, including all 12 through v (W-source chain h^{m_min+4}λ_R²κ²g²|ε_B|²).
   - **BHD2-U2-R1-NONZERO**, but only on cycles whose read support touches the cut fiber. Under rule R1 (the step-1 §1 Born-level block) the total is nonzero on exactly the 11 cut-touching L = 4 cycles (W-source chain on 3 of them), and **exactly zero on the other 47, including all 12 cycles through v.** The pre-stated structural expectation held on every untouched cycle at every L: R1 total = 0 and Φ^(00) = −(step-1 Δ) ⊛ P_Born.
   - Consequence: whether the |ε_B|² sector carries a Bind-dependent loop-read term at the writer is decided by the **level-1 read rule** (R1: transported same-six-edge read → exact cancellation; R0: level 1 unavailable → nonzero leakage term). CHECK F8's framing-gate item now has a measured consequence and must be ruled before any margin includes ε_B monomials.
2. **U3-t² (native hop −t Σ n_e T_e).** **BHD2-T2-NONZERO.** Nonzero W-source t² coefficients (h^m λ_R²κ²g²t²) on 48 of 58 L = 4 cycles, **12 / 12 through v**; at L = 3, 75 / 84 (18 / 18 through v; 25 / 28 winding). L = 2: 128 / 128, 48 / 48 through v, 96 / 96 winding.
   - The WR2 evacuation route (carrier v → u) is not the only route. On every L = 4 cycle through v, the W-arm t² chain is nonzero in all four neighbour clusters w, at m_min or m_min + 2.
   - On cycles through u (m_min = 14) the t² W-source chain is nonzero **at m_min itself** (−8/2025 via route u only), where the t⁰ chain of step 1 first appears at m_min + 2: q written at u by the evacuated carrier couples to the cycle directly.
   - **A new Bind-dependent class appears that is not q-feedback mediated:** λ_R⁰ g² t² monomials (W: κ²g²t²h^m; C: g²t²h^m) are nonzero on all 58 cycles. Bind writes q at the carrier site; that record makes hop branches distinguishable, and the hop term n_e T_e carries the effect to incidence. It is kept separate from the feedback chain (λ_R ≥ 1).
3. **Controls: all pass** (K1, K2, K3, K4, K5, K7, K8, KB1, KB2, KT1, K6-B, K6-T, K9). **One declared deviation:** the pre-registered K6-F was infeasible (§4) and was replaced by K6-F′, run on 9 of the 11 cut-touching cycles.

What this establishes: non-identity of the same-history Bind-dependent loop-read contrast in two further coefficient families (Born sector; hop), with the competing channels identified and separated by exact monomial label. What it does not establish: the LR:29 finite exit (margin with controlled error at a declared member) — UNTESTED; next step §7.

## 1. What was computed (summary of the PREREG)

| Family | Variables (all others at zero degree) | Extracted | L | Orders |
|---|---|---|---|---|
| FB (U2) | h, λ_R, κ, g, ε_B | \|ε_B\|² (ε_B phase removed by level-1 rephasing) | 4, 3, 2 | m ∈ [0, m_min+4], a, b, c ≤ 2 |
| FT (U3-t²) | h, λ_R, κ, g, t | t² (θ removed by carrier rephasing) | 4, 3, 2 | m ∈ [0, m_min+2], a ≤ 2, b, c ∈ {0,2} |
| FTB (P3) | h, λ_R, κ, g, t, ε_B | t²\|ε_B\|² | 4, 3 | m ≤ m_min+4 |
| PJ | h, λ_J, κ (+ε_B or t), λ_R = g = 0 | competing λ_J channel | 4 | as FB / FT |

Exact structure used (each verified, §4):
- **FB:** with t = 0 the carriers stay at v (W) and a (C), neither a cut end at any L. The cut block (4 cut bonds at level 0 ⊕ 8 children at level 1, −hX on each bit, e(Tjoin + Tjoin†)) commutes with the rest, so the state is an exact product: cluster ⊗ non-cut free edges ⊗ cut block. Every term of F_C^(0) and F_C^(1) factorizes over these.
- **FT:** at t², each nonzero ket–bra history moves the carrier to exactly one neighbour w and back (the read is the identity on carrier position). So the t² coefficient is Σ_w over clusters E(x) ∪ E(w) with the carrier on {x, w}.

Born-sector decomposition: Φ = Φ^(00) (ket or bra goes up and comes back; read at level 0) + Φ^(11) (both born; read at level 1). R1 total = Φ^(00) + Φ^(11)_R1; R0 total = Φ^(00).

## 2. Results

### 2.1 U2: Born sector, |ε_B|² [FORMAL-RESULT]

| L | Cycles | Touch cut fiber | Bind-dep. nonzero, Φ^(00) | Bind-dep. nonzero, R1 total | W-source, Φ^(00) | W-source, R1 | Through v: W-source Φ^(00) / R1 |
|---|---|---|---|---|---|---|---|
| 4 | 58 | 11 | 57 | 11 | 33 | 3 | 12/12 / **0/12** |
| 3 | 84 | 33 | 82 | 33 | 48 | 15 | 18/18 / 3/18 (the 3 touching) |
| 2 | 128 | 125 | 123 | 121 | 102 | 99 | 48/48 / 45/48 |

- On the 47 / 51 / 3 untouched cycles (L = 4 / 3 / 2) the R1 total vanishes exactly, and Φ^(00) equals −(step-1 Δ) ⊛ (Born probability, leading [h⁴|ε_B|²] = 2/3). This is a level-leakage term, not a new Bind path.
- Examples, L = 4 (coefficient of h^m λ_R^a κ^b g^c |ε_B|² T^n):
  - Cycle 81,144,147,85,84,83 (through v and a), (20,2,2,2): Φ^(00) = −4/21, Φ^(11)_R1 = +4/21, R1 = 0.
  - Cut-touching 17,80,83,21,20,19 (through a; a gate edge is a cut bond): W-source (20,2,2,2): Φ^(00) = 1/35, Φ^(11) = −1/42, **R1 = 1/210**. C-arm (18,2,0,2): **R1 = 64/675**, at m_min + 2. When the gate already needs a cut bond, a Birth path costs only two extra flips.
  - Cut bond on the cycle (F_C^(1) = 0 under R1): 1,64,66,17,16,2: (18,2,0,2) = 16/135 under both rules.
  - L = 3, cut-touching winding cycle 21,55,53,87,85,23: W-source (18,2,2,2) R1 = 1/210.
- No coefficient below m_min (AWH's bound did not need to hold for Birth paths; it does at these orders). No g⁰, no λ_R⁰, no imaginary part, no level-1 term at ε_B⁰.

### 2.2 U3: hop t² [FORMAL-RESULT]

| L | Cycles done | W-source t² nonzero | Through v | Winding | C-arm t² nonzero | Hop channel (g⁰) nonzero | W-source at m_min |
|---|---|---|---|---|---|---|---|
| 4 | 58/58 | 48 | 12/12 | — | 43 | 58 | 40 |
| 3 | 84/84 | 75 | 18/18 | 25/28 | 71 | 84 | 60 |
| 2 | 128/128 | 128 | 48/48 | 96/96 | 128 | 124 | 116 |

Census of nonzero Δ t² monomials at L = 4, as (a, b, c) = (λ_R, κ, g) degrees: (0,0,0), (0,2,0) [hop channel]; (0,0,2), (0,2,2) [Bind which-path, no feedback]; (2,0,2), (2,2,2) [feedback chains]. Every odd degree vanishes (K8, verified for κ, g, t and λ_R). Examples, L = 4, coefficient of h^m λ_R²κ²g²t² T^(m+8):
- 81,144,147,85,84,83: m = 16: −4729/49896; m = 18: +1811269/1351350. The C-arm (16,2,0,2) is +275/378; the hop channel (16,0,0,0) is −64/3.
- 25,87,86,37,39,26: m = 16: +251/4725; m = 18: −80203/93555.
- m_min = 18 cycles through v: m = 18: −4729/24948.
- Through u, 21,83,82,33,35,22 (m_min = 14): m = 14: −8/2025 (route u only); m = 16: 21584/467775.
- On the edge read n_vu itself: h²λ_R²κ²g²t² coefficient = −383/907200 (the t² companion of A1's +1/448).

### 2.3 P3: joint t²|ε_B|² [FORMAL-RESULT]

- L = 4, all 58 cycles: W-source nonzero in Φ^(00) on 40 cycles and under R1 on 5. The R1 total is zero on every untouched cycle again.
- Example, 17,80,83,21,20,19, (18,2,2,2): Φ^(00) = −16/10125, R1 = −8/30375.
- L = 3: all 84 cycles. W-source nonzero in Φ^(00) on 69, under R1 on 28; the R1 total is zero on every one of the 51 untouched cycles.

### 2.4 Competing channels, kept separate (LR:25)

| Channel | Where | Status |
|---|---|---|
| λ_J d p (PJ) | FB-J: \|ε_B\|² λ_J monomials nonzero on 29/29 tested L = 4 cycles in Φ^(00), and on 11 (all cut-touching) under R1. FT-J: t² λ_J monomials nonzero on 22/22 cycles containing v or a | FORMAL-RESULT; ε_B⁰ t⁰ parts reproduce step-1 P2 exactly (660 entries) |
| Hop n_e T_e at g⁰ | FT: nonzero on every cycle at L = 4 and 3 | FORMAL-RESULT; direct carrier–incidence channel, non-Bind |
| Bind which-path (g², λ_R⁰, t²) | FT: all 58 L = 4 cycles | FORMAL-RESULT; Bind-dependent, not q-feedback |
| C-arm control-carrier Bind | FB, FT, P3 | FORMAL-RESULT; Bind-dependent, not the source chain at v |
| Born level leakage | Φ^(00) on untouched cycles | FORMAL-RESULT; read-rule dependent (R0 ≠ 0, R1 = 0) |
| Mixed λ_J^{≥1} g^{≥1}; U_d, Δ, ε_r, E_*, ε_c, θ monomials | not computed | UNTESTED (§7) |

Separation rule: by exact monomial label. At a physical member, Δ − Δ|_{g=0} removes the pure λ_J and pure hop monomials exactly. It keeps the which-path, C-arm and mixed monomials, which a margin must bound or attribute.

## 3. Controls (all PASS)

| Control | Result |
|---|---|
| K1 (A1 reproduction) | +1/448 exactly in the FB pipeline (ε⁰) at L = 4, 3, 2 and in the FT pipeline (t⁰) at L = 4, 3, 2 |
| K7 (step-1 regression) | FB ε⁰: 9396 + 13608 + 20736 published entries, 0 mismatches. FT t⁰ at L = 4: 4176 entries, 0 mismatches. PJ: 396 + 264 step-1 P2 entries, 0 mismatches |
| K2 | (i) [κ²]Tr(p_v ρ_W) = 1. (ii) Every g⁰ coefficient of Tr(q ρ) = 0 in every cluster. (iii) FB g⁰ Δ = 0; FT g⁰ Δ ≠ 0, registered as the hop channel |
| K3 | FB λ_R⁰ = 0; FT λ_R⁰ ≠ 0 (hop and which-path), registered |
| K4 / K5 | Tr ρ constant in every cluster and in the cut block; no imaginary part anywhere |
| K8 (parity, L = 4, 12 cycles through v, w = u, b) | every odd κ, g, t and λ_R coefficient vanishes |
| KB1 | [h⁴ e²] Tr(P_1 ρ_cut) = 2/3 |
| KB2 | n_vu ⊕ n_vu: no \|ε_B\|² term (9 nonzero level-0-only terms cancel exactly) |
| KT1 | [κ²t²]Tr(p_u ρ_W) = 1/4; [t²]Tr(p_b ρ_C) = 1 |
| t⁰ consistency | the t⁰ part is identical across all 4 neighbour clusters of each arm |
| K6-B | 38 cut-block operators: exact series vs float block-matrix derivative at h = 0.3, worst rel. 1.6e-14 |
| K6-T | joint {v, u, w₂} model vs sum of single-neighbour models, 3 operators: worst rel. 3.1e-11 |
| K6-F′ | 9 cut-touching L = 4 cycles: joint brute force vs factorized, worst rel. 1.4e-15 |
| K9 (literal backend, complete L = 2 graph) | 56 FT and 15 FB coefficients from the backend's own `column_terms`: 0 mismatches. Conventions of hop, admission, Bind, feedback and the Birth map are confirmed |

## 4. Deviation (declared)

- **K6-F as pre-registered was infeasible.** It needed a cut-touching L = 4 cycle with a full level-1 brute-force word of ≤ 21 bits; the graph-only minimum is 27. I should have checked this before the seal.
- **K6-F′ (run instead).** It propagates jointly, in one state vector with the Birth map acting on the tracked word, the cut bonds/children, E(v) with the W resource, and every read-support edge incident to a cut end. The remaining support edges are free in both evaluations.
- **Scope of K6-F′.** It was run on every cut-touching L = 4 cycle whose tracked level-1 word has ≤ 19 bits: 9 of 11 (graph-only criterion, set by runtime). Skipped: 1,64,66,17,16,2 (25 bits) and 5,67,66,17,19,6 (21 bits).
- **Other runtime fixes.** Two crashes, a key error and a JSON type error, were fixed and rerun. No number changed.

## 5. CHECK_V001 findings addressed

- **F1 (prior work, MEDIUM).**
  - AWH and its review are the antecedent and are now cited (PREREG §0). AWH:21's ε-independent bounds hold in every family here. AWH:23's Birth caveat is now resolved for the sparse witness: no Birth-path coefficient below m_min at these orders.
  - The AWH:31-33 "first feasible" targets, all resolved as nonzero:
    - W h¹⁶κ²g²λ_R² at T²² (step 1);
    - C-arm h¹⁶g²λ_R² at T²⁰ (step 1);
    - their t² and \|ε_B\|² companions (here).
  - The custody condition (AWH:35, "root-only implementation") remains root's ruling. This run stayed in the toy allowance. Code, cases and hashes are in place for the separate code/case review the AWH review asks for.
  - The AWH:39-45 redirect to the level-0 degree-two collective family is not engaged by this step. It is the U4′ target after U1 (§7).
- **F2 (scope, MEDIUM).** The qualifier is carried at the top and in every claim row. The return summary does not call this "the program's own model".
- **F3.** The parity nulls are now verified for t as well. The argument extends: the read is the identity on carrier position, so t-odd terms vanish.
- **F4.** Tolerances were tightened to relative 1e-10, and an independent backend check (K9) was added.
- **F6.** No P3-type Γ was computed here.
- **F7.** Not reused.
- **F8.** Now quantified (verdict 1).

## 6. Claim classes

| Claim | Class |
|---|---|
| All coefficients, counts and censuses in §2 | FORMAL-RESULT (exact; controls §3) |
| U2: Bind-dependent \|ε_B\|² terms nonzero in Φ^(00); under R1 nonzero only on cut-touching cycles and exactly zero on untouched ones | FORMAL-RESULT |
| Which level-1 read rule (R0/R1) is the physical complete-domain instrument | DECLARED-PREMISE pending; framing gate needed (F8) |
| U3: nonzero t² W-source chain on all cycles through v (L = 4, 3); which-path λ_R⁰ g² channel exists | FORMAL-RESULT |
| t²\|ε_B\|² (P3) at L = 4 | FORMAL-RESULT |
| Owned-parent transfer (A29 ws4) | UNTESTED; deciding test U4 |
| LR:29 exit (margin with controlled error at a declared member) | UNTESTED; deciding test U1-M (§7) |
| U_d, Δ, ε_r, E_*, ε_c, θ and mixed λ_J·g monomials | UNTESTED; census in U1-M (i) |
| Γ-protection, tension, baryon map, 120/43 plug | UNTESTED (U5-U7) |
| DM working identification (MS:8) | HYPOTHESIS (unchanged) |

None of this is TESTED-POSITIVE: there is no record contact (PRIMER:64). No statement about galaxies.

## 7. Next named step toward the LR:29 controlled-error exit

**U1-M: lowest-degree census plus connected-word majorant margin on a declared ray** (sparse witness, V005 Hjoin, L = 4, full step-1 roster, every cycle reported).
- **(i) Census.** By AWH-type selection rules over **all** owners (U_d, Δ, ε_r, λ_J, E_I/R/S, ε_c, ε_B, t, θ), find the minimal total time degree N_C at which a g-dependent monomial of Δ_C can occur.
  - Step 2 already shows the leading Bind-dependent coefficient on a uniform ray is a sum over channels, not the A1-type chain alone. The which-path terms enter at the same total degree as the feedback chains: C-arm g²t²h^m with λ_R²g²h^m at m+4, and W κ²g²t²h^m with λ_R²κ²g²h^m at m+6.
  - Mixed λ_J·g² monomials (also degree m+4) must be enumerated.
- **(ii) Exact values.** The exact coefficients at N_C, from this machinery extended with the mixed λ_J·g and diagonal-owner monomials.
- **(iii) Remainder bound.** A volume-independent remainder bound for all degrees > N_C. It comes from a connected-word (linked-cluster) majorant built from per-term operator norms of every owner. The rigorous path-count bound vectors A ≥ |v| already in `exact_taylor.py` are the local ingredient.
- **(iv) Deciding inequality.** On a ray x = s·x̂ fixed at a framing gate before evaluation (direction from record declarations such as PC1 DP-h where they exist, never from outcomes), show |c_{N_C}| s^{N_C} − R(s) > 0 for 0 < s < s*. The Bind-dependent part is isolated as Δ − Δ|_{g=0}, and the which-path, C-arm and leakage parts are carried as named competing terms.
- **Prerequisites at the same gate:**
  - the R0/R1 level-1 read rule (F8);
  - root's AWH:35 custody ruling.
- **Every outcome registers.** A margin > 0 is the LR:29 exit for the sparse witness. A failure names the next order.
- After U1-M, U4′ applies the same certificate to the AWH:41-45 level-0 degree-two collective family. That is the owned-parent-facing step A29 asks for.

## 8. Imports ledger

None (native operators, actual W/C, actual graph and Born map, exact series and integer words).

## 9. Files (sha256 in HASHES.txt)

- `PREREG_BHD_STEP2_V001.md`, `results/PREREG_SEAL_V001.txt`, `results/GRAPH_FACTS_V001.json`
- `code/`: `graph_facts.py`, `exact_taylor.py`, `clusters.py`, `common.py`, `run_fb.py`, `run_ft.py`, `run_p3_pj_k8.py`, `k6_numeric.py`, `k9_backend.py`, `summarize.py`; `code/pinned/` (step-1 `graph_roster.py` b01c35b6, `bhd_step1_coeffs.py` 87a863b1; backend 0d28150f)
- `results/`: `FB_L4_V001.json`, `FB_L3_L2_V001.json`, `FT_L4_V001.json`, `FT_L3_V001.json`, `FT_L2_V001.json`, `P3_L4_V001.json`, `P3_L3_V001.json`, `PJ_L4_V001.json`, `K8_L4_V001.json`, `K6_NUMERIC_V001.json`, `K9_BACKEND_V001.json`, `SUMMARY_V001.json`, and the run logs
- `BHD_STEP2_V001.json`; `check/` is left empty for checkers
