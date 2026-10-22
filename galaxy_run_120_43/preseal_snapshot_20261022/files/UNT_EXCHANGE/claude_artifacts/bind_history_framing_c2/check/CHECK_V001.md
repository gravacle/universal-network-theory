# CHECK_V001 — independent check of BIND_HISTORY_FRAMING_V001

2026-10-17. Read-only. Nothing was run. No target velocities were read. Inputs: BIND_HISTORY_FRAMING_V001.md (sha256 1bbdb88ca4e639aa1c39c37b60e77dff0bd8db946ffeb051914adc69df3c207a, recomputed from bytes, matches) and every cited source line. Path keys as in the draft and PRIMER:11-51.

## VERDICT: PASS_WITH_CORRECTIONS

All cited files exist. Cited line content matches at: PR:56-62; LAD:50, 212, 214; BBP:3-7; V005:6, 15, 17, 19; LIVE:102; NPSI:49, 51, 56, 58; REG:12168-12179, 12224-12230, 9863-9870; P58H:26-27; ASM:57, 59, 203, 235-262, 1108, 1401-1410, 1497, 1503; MS:8, 12, 16; LR:7, 11, 19, 23-29; CI:68, 72, 131, 159; HO:25; PRIMER:120, 128, 132, 319, 483, 485, 861-864, 902-903, 1068-1071, 1222, §12 #38; PREP:180-181, 210, 249, 266; RBC:221-222; RBO:3; RE:28; DRV:134; FRZ:197-203; SSB:28-30, 87; RSR:110; RDN:49; RDA:40; TM:6, 10, 16; KT:48; GE:83, 290; SL:238; NRP:22-30; T20H:37-47; P47H:11, 13; P47L:13; LB:36; C1/READINESS_NATIVE_RECORD_FIRST_CONDITIONAL_OWNERSHIP_DECISION_2026-10-15_V001.md:21.

Reproduced: there are 41 `.py` files in the three route folders, with zero hits for age, lookback, formation_time, n_spent/nspent, bind_depth or history_weight. "BIND" and "BIND6" appear only as folder-path constants (DRV:134-135, 145-154). F-3 arithmetic reproduces: 0.0272, 0.0292, 0.512. A Bullet Cluster / 1E 0657 grep over the whole program root and UNT_EXCHANGE finds no hits outside this draft. No .30/.70, 3:7 or fitted weight is used as an input. The SA-BH-01 null outcome registers as a result (line 116). No NGC3198 velocity appears.

## Findings

1. **Overstated: C-124/125/131 scope** (summary item 1; §3 line 137 "forbid a classical Bind-count shortcut").
   - What the record shows [FORMAL-RESULT]: it refutes two exact properties of q-population reads, on a stated finite domain with a rank-uniform lift and persistent-old q:
     - exact autonomous continuous-time population closure (REG:12170, 12177);
     - additivity of fine three-read histories (REG:12226).
   - What the record leaves open: it says "not all state/event/scale reductions" (REG:12177). Coarse-time, restricted-state, stroboscopic and enlarged-memory reductions remain open (REG:12172, 12179). It also states "No no-reach/no-Gamma/no-gravity theorem" (REG:12172).
   - The theorems concern population reads, not counts of Bind events. Line 80 is scoped correctly. Rewrite the summary and line 137 to match it.

2. **Overstated: "Any Bind history … is carried by the state's coherent memory … not by a census"** (line 64; summary item 1).
   - The exact projection carries the full memory (ASM:235-262) [FORMAL-RESULT].
   - Whether a coarse census carries it approximately is UNTESTED. The deciding test is the open reductions with error bounds (REG:12172, 12179).
   - BH-c1 is itself such a coarse classical-exposure reduction. g²Tr(pρ)t² is only the leading short-time coefficient of reversible loss (REG:12170). Missing prior work: "g=0 has nonzero exposure but exactly zero writing; at g!=0 return coherences, detuning and backreaction matter" (P47L:13).
   - File BH-c1 as a coarse-reduction candidate under REG:12172, with P47L:13 cited.

3. **Overstated: ASM:1408 cited as already requiring per-species columns** (summary item 6; line 109).
   - ASM:1408 says "independent pressure/current/stress sources require their corresponding response columns". That concerns stress components. It says nothing of species or record history.
   - A history- or species-resolved column is this draft's proposed extension [HYPOTHESIS], not an existing requirement.

4. **Framing narrows the placement of history and conflicts with prior work** (§3 BH-D, chain step 5).
   - The route puts Bind history into a weight per baryon species (w★/w_g), and that needs a map from baryons to χ. The record keeps ordinary stress and retained collective response as separate contributions:
     - ASM:1505;
     - ASM:1108 says the route does not require "constructing microscopic baryon knots first";
     - ASM:1503 says the calculation is not a request for "a microscopic baryon identification";
     - MS:8 and MS:16 identify DM as Bind-generated loop response "un-collapsed into localized baryon knots".
   - Within the record, Bind-generated history can also live in the retained collective (Γ_ret) state that the baryons source. The existing channel for that is the admissible present-state family and its state band (CI:66, CI:108).
   - Add this placement next to the species-weight form, so the computation measures which structure, if any, the response depends on. Do not pre-commit to the species-weight form.

5. **Missing prior work** (§5).
   - CI:66: "Keep formation history on the derivation list and test state sensitivity."
   - CI:108: the state band is evaluated during 120/43.
   - CI:114: full formation history is not a blanket prerequisite.
   - UNT_DERIVATION_BACKLOG_V001.md:71: **F1 Formation history of the galaxy state**, with the clause "do not choose a history from the target velocity residuals". BH-D should be registered as building on F1, not as a new item.
   - GE:82 (GE-X47): "As retained storage accumulates, is there one scalar density trigger or does placement/pair topology control the response?" This is directly on point for BH-c4/c5/c6.
   - PR:76-78 (F10, F12: accumulation of gamma terms).
   - C1/READINESS_CONCURRENT_BIRTH_PRINCIPAL_DECISION_2026-10-15_V001.md:48 (bound-structure suppression UNTESTED) and C1/READINESS_OWNED_READY_FALLBACK_ADOPTION_AND_POSTULATE_LEDGER_V001.md:44 ("Bound structure resists Birth: required test carried forward").
   - C-77 shared-origin (REG:9539-9565, via T20H:29).

6. **Import missing from the ledger, and a prescription** (line 158; summary item 7).
   - "The intracluster gas is billions of years old" is an uncited external astrophysical claim. It drives a "must be" conclusion, yet the imports ledger says none.
   - Either enter it as OBSERVATION, entering at BH-T2 with primary provenance, or drop it. Native grounds already suffice: calendar lookback has no galaxy-route counterpart (TM:10), and the record has no monotone Bind counter (§1.1).
   - Replace "the operative variable must be … such as BH-c1, BH-c4 or BH-c5" with "the record-structure variable, if any, on which the computed response depends (candidates BH-c1–c7)".
   - The claim also implicitly corrects the principal's wording "young gas clouds". That belongs in the premise-registration note, not in a draft conclusion.

7. **FORMAL claim imprecise** (line 155, moment identity).
   - For κ = K∗Σ with K even, ∫xκ = K̂(0)∫xΣ. So it is the normalized centroid that coincides, not "the first moment".
   - It also holds only if K is integrable with finite K̂(0), and first moments converge. The static limit's existence is itself a requirement (ASM:1410).
   - No convergence projection exists yet (PRIMER:1222).
   - State the conditions, and mark it as a draft derivation that has not been independently checked.

8. **Heuristic presented under the FORMAL heading** (line 148).
   - "Calibration absorbs ≈(w★/w_g−1)·0.03 … ≈(w★/w_g−1)·0.48 transfers" uses mass fractions as lever arms. The velocity-weighted leverage differs.
   - What DDO154 calibration can absorb depends on which shared parameter it fixes, and on whether that parameter acts as a scale.
   - Mark this as an order-of-magnitude HYPOTHESIS. The exact statement is line 147.

9. **BH-T1a definition not yet target-safe in precision** (line 149).
   - PREP:246 appends H2 ring masses into the `star_R/star_z/star_mass` fixed-source arrays used at PREP:292-293. Stellar and molecular totals are separated only at PREP:211/242/302.
   - "From source arrays only" must name stellar_quadrature_mass and molecular_quadrature_mass explicitly. Otherwise f★ for NGC3198 silently includes H2 (SSB:87).
   - F-3 excludes H2 while the route includes it. Declare that difference.

10. **Scope of the Krylov custody not stated** (line 123).
    - KRYLOV_FULL_N2_C1 is the P49_CODEX2 N2 old-carrier-site producer (KRYLOV_FULL_N2_C1_PRODUCER_SPEC_V001.json, jobs[].runner lanes/P49_CODEX2/…). Its file is dated 2026-10-13, before the owned-parent definition (ASM:203; ASM dated 2026-10-15).
    - State its domain. Its transfer to the owned parent is UNTESTED, in addition to its O_loop fitness.

11. **KT disposition incomplete** (line 178).
    - KT:49 records that a revised τ_Q form, with a UNT-derived clock and a derived D, can re-enter through the framing gate. Write "excluded as written; revised form open (KT:49)".
    - KT:48's TESTED-NEGATIVE is arithmetic on a formula against a required length, which is FORMAL-RESULT under PRIMER:66. This is a consistency note only.

12. **Unsupported qualifiers.**
    - "Lineage A, single carrier" (BH-c7): REG:9863-9870 has no carrier-count statement.
    - "FORMAL-RESULT on a supplied sheet" (line 165): GE:83 describes actual FPMH formation-lineage episodes with a hostile audit.
    - Cite a source for each qualifier, or remove it.

No finding blocks principal registration of the 2026-10-17 statement (accounting requirement as DECLARED-PREMISE, Bullet Cluster reading as HYPOTHESIS). Findings 1–4 and 6 must be applied before root enters SA-BH-01 and pre-registers BH-T1a. Finding 9 must be applied before BH-T1a is frozen.
