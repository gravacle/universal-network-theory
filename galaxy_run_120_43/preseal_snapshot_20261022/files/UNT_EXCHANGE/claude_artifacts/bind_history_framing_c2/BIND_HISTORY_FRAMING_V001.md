# Bind-history source framing — FRAMING GATE DRAFT V001

2026-10-17. Claude2 lane, read-only synthesis. This is a framing-gate draft for root/principal sign-off. It is **not a dispatch**. No program script, sampler, solver or worker was run. Nothing here changes the reviewed forward model, the R2 convergence runs, the DDO154 calibration or the NGC3198 prediction. No NGC3198 target velocity was read. Status classes follow PRIMER:55-64.

**Path keys** (PRIMER keys at PRIMER:11-51 also apply: ASM, LIVE, NPSI, V005, REG, SL, LAD, LB, CI, HO, C1, C3, HLP, PW, X).

| Key | Path |
|---|---|
| PRIMER | X/KNOWLEDGE/UNT_COORDINATOR_PRIMER_V002.md |
| MS | C3/READINESS_PRINCIPAL_P26_LINE_A_MECHANISM_SELECTION_V001.md |
| LR | C3/READINESS_LINE_A_BIND_NATIVE_ROUTE_RECOVERY_V001.md |
| BBP | PW/nomenclature/BIND_BIRTH_POLICY.md |
| PREP | X/claude_artifacts/ngc_route_impl_c2/route_a/install/recovered_packet_audit/ngc_actual_initial_source_preparation_v001.py |
| RBC | X/claude_artifacts/ngc_f10_c2/route_b_v006/stages/ddo_fixed_K_free_surface_root_v001_gal_c2v004.py |
| RBO | X/claude_artifacts/ngc_f10_c2/route_b_v006/stages/ddo_body_source_offset_root_v003_gal_c2v004.py |
| RE | HLP/recovered_packet_audit/axisymmetric_initial_rest_energy_fourier_v001.py |
| DRV | X/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py |
| FRZ | X/claude_artifacts/calibration_freeze_c2_v003a/prediction_freeze_c2v003a.py |
| SSB | C1/GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json |
| RSR | C1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json |
| RDA | PC/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_A1_A2_2026-10-17_V001.md |
| RDN | PC/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001.md |
| TM | X/claude_artifacts/lapse_integration_audit_c2/theory_mapping/TERM_MAP_V001.json |
| KT | X/claude_artifacts/lapse_integration_audit_c2/REVIEWER_PROPOSAL_K_TAUQ_ASSESSMENT_V001.md |
| GE | PW/GRAVITY_EMERGENCE_EXPERIMENT_REGISTER_V001.md |
| T20H | X/FROM_CODEX3/0459_2026-10-13_T20-history-Gamma-term-and-accumulation-requirements.md |
| P47H | X/FROM_CODEX3/0126_2026-10-12_P47-history-imprint-and-native-energy-bound.md |
| P47L | X/FROM_CODEX3/0136_2026-10-12_loop-confined-native-history-and-graph-exposure.md |
| P58H | X/FROM_CODEX3/0179_2026-10-13_P58-native-three-read-history-obstruction.md |
| NRP | DS/joint_parent_continuation/NATIVE120_RECORD_PARTITION_INITIALIZATION_ADDENDUM_V001.txt |

## 0. The direction being framed

Principal, 2026-10-17 (relayed in this task): "we need to make sure that we are accounting for the history represented by bind operators over billions of years versus the history associated with more transient gas cloud formation. The 2006 observations of the Bullet Cluster (1E 0657-558) were not a proof of dark matter but rather a proof that ancient records with deep 'Bind' histories is going to carry more gravitational effect than young gas clouds."

- The accounting requirement is a method direction [DECLARED-PREMISE once registered; not yet in PR].
- The Bullet Cluster reading is [HYPOTHESIS]: the model decides it (PR:56-62 precedent). Deciding test BH-T2 (§4).
- The Bullet Cluster appears nowhere in the program record (grep of X/KNOWLEDGE, PC, LAD, FRONTIER_INDEX: no hits other than the word "bullet"). Mergers and lensing are OPEN lanes (LAD:212, 214). FRONTIER_INDEX.md is a version pointer list (FRONTIER_INDEX.md:1-6) and carries no relevant content.

## 1. What the record says Bind is and does

### 1.1 Operator facts

| Claim | Status | Cite |
|---|---|---|
| Naming only: Bind "names the action that locks phase space to maintain Records"; renaming "does not supply a missing physical vertex" | DECLARED-PREMISE (naming) | BBP:3-7 |
| Physics: Bind is g Σ_v p_v X_{r,v}, the carrier-controlled Pauli X on q; coherent and Hermitian, so it un-writes as well as writes | DECLARED-PREMISE (model) | V005:6; LIVE:102 via PRIMER:554 |
| Bind conserves N_c; admission changes N_c and N_ready oppositely; Q and M conserved | DECLARED-PREMISE | V005:15 |
| Bind rotates q at a spent site too; N_spent and N_q are distinct censuses; neither is asserted monotone | FORMAL-RESULT (distinctness) | V005:17 |
| After admission is off, P_S is retained by Bind, transport and the blank-I Birth lift, but "this conditional retention is not an imposed law" | FORMAL-RESULT (conditional) | V005:17 |
| No permanence imposed | DECLARED-PREMISE | V005:19 |
| N_S = N_c + M − Q: within fixed Q/M the Spent count "is not an independent cumulative record counter"; Bind changes N_q and leaves N_c, N_S unchanged | FORMAL-RESULT | NPSI:56 |
| Active-cell placement is conserved fragmentation, "not a variable that will automatically thermalize away"; it "is not conserved q, accessible history content, Gamma protection" | FORMAL-RESULT | NPSI:49, 51 |
| Full spectral distribution of an autonomous Hjoin is conserved; mean E does not fix a state or its late-time readout | FORMAL-RESULT | NPSI:58 |
| Under active Bind, retained-q loss "starts at g^2 Tr(p rho)t^2 and is reversible"; population closure is an exact semigroup only if reads commute with H | FORMAL-RESULT (C-124) | REG:12168-12172 |
| Exact projected dynamics keeps the full memory convolution; nontrivial Bind refutes exact autonomous population reduction on its domain | FORMAL-RESULT (C-125) | REG:12175-12179 |
| Fine three-read q histories are nonadditive under active Bind, coefficient g^2 × carrier/outcome exposure | FORMAL-RESULT (C-131) | REG:12224-12230; P58H:26-27 |
| Owned parent includes Bind, incidence changes, hopping, admission, concurrent Birth and all reverses; exact Volterra projection with full memory | DECLARED-PREMISE / FORMAL-RESULT | ASM:203; ASM:235-262 via PRIMER:569 |
| DM working identification: "distributed, non-local Γ-level macro-loop tension generated by the Bind operator, specifically un-collapsed into localized baryon knots" | HYPOTHESIS | MS:8 |
| Writer→incidence coefficient +T⁸/(448ħ⁸) (admission → Bind → q-feedback → incidence); "No tension, baryon species, metric or gravity follows" | FORMAL-RESULT | LR:7, 11 |
| Line-A first finite exit: a qualified loop observable plus a nonzero same-history Bind-dependent response | UNTESTED | LR:23-29 |
| "Actual Bound-Record identity, conserved energy and physical source readout remain model-specific requirements" | DECLARED-PREMISE (requirement) | LAD:50 |

**What is cumulative and what is not.** Q, M, N_c (under Bind alone), the active-cell mask and the spectral distribution are conserved. N_S is locked to N_c at fixed Q/M. N_q changes under Bind and is not asserted monotone. The record therefore contains no conserved or monotone "Bind counter". Any Bind history in the owned parent is carried by the state's coherent memory (C-125 convolution, Volterra kernel). It is not carried by a census.

### 1.2 Candidate operational meanings of "Bind history / Bind depth" (record-only; each UNTESTED)

| # | Candidate | Native source | Measuring computation | Deciding test |
|---|---|---|---|---|
| BH-c1 | Accumulated Bind exposure E_B(T) = g² ∫₀ᵀ Tr(p_v ρ(t)) dt over a region | the coefficient that sets retained-q loss (C-124) and fine-history nonadditivity (C-131) | real-time evolution of a fixed preparation on the owned parent | whether loop response Δ_loop (BH-c2) depends on E_B at fixed Q/M, energy and N_q |
| BH-c2 | Same-history Bind-dependent loop response Δ_loop(T) = Tr[O_loop U(T)(ρ_W − ρ_C)U(T)†], read at several prospectively fixed T | Line-A first exit | same as LR:25, with the retained-q references H0 = Hjoin − g p X_q, H1 = H0 + λ_R d q as mathematical comparisons only (LR:27) | a qualified O_loop and a nonzero Bind-dependent part with controlled error (LR:29) |
| BH-c3 | Written-record census N_q(t) and its rate | V005:17 | P-18 S and q censuses from declared all-blank and all-written preparations (V005:19) | P-18 itself |
| BH-c4 | Active retained-memory topology at fixed formation and active-record counts | Lineage B: "equal record count does not fix response: active retained-memory topology matters" (GE:290); GE-X48 (GE:83) | transfer of the GE-X48 contrast to the owned parent | same-count, different-topology response on the owned parent |
| BH-c5 | Active-cell placement mask (conserved fragmentation) | NPSI:49 | static or real-time response at equal Q/M and energy, different masks | mask-dependence of the response columns |
| BH-c6 | Written-record density f and its effect on loop stiffness | P-40: blank-to-written ring shift +7.71 % to −20.59 %, sign change at f = 1/4 (PRIMER:485) | ring/loop coefficient vs f on the owned parent | P-40 is perturbative and uncertified at the physical tuple (PRIMER:483) |
| BH-c7 | Encoding class (occupancy accumulates, orientation screens) | C-88 (REG:9863-9870, line 9865) | Lineage A, single carrier | second-carrier C-88 rerun |

**Already ruled out by the record:**
- N_S as an independent cumulative Bind counter (NPSI:56).
- A classical count of Bind events as an exact autonomous history variable at fine resolution (C-124, C-125, C-131). Coarse, restricted-state, stroboscopic and enlarged-memory reductions remain open (REG:12172, 12179, 12230).
- Provenance alone in the GE-X48 venue: "F3 reads occupation rather than provenance" (GE:83).
- Sampler τ or MCMC events as physical time: "imaginary-time/MCMC events are not physical rates" (CI:159 via PRIMER:319).
- Calendar lookback as a galaxy-route variable: it exists only as cosmological lookback scaling (TM:10).

## 2. What the 120/43 forward route does with source records

**Code facts** [FORMAL-RESULT: code read].
- Stars: Σ★ from 3.6 µm nodes at M/L3.6 = 0.5, with 0.4/0.6 population alternatives (SSB:28). Each stellar mass element becomes a ten-channel column `[[-mass*c*c]]+[[0.]]*9` (PREP:210): lapse channel only. Stars are "held in the physical frozen-background chart… not updated as a full metric fluid" (PREP:180-181). In route B, "Fixed stars cancel only because they are unchanged" (RBO:3).
- HI: annular means with "factor1.36 applied once" (RSR:110); HI/(HI+He) = 1/1.36 for NGC3198 (RDN:49). Gas columns are `-c²·mass` in channel 0 (PREP:266; RBC:221-222).
- H2: helium already included, same `-mass·c²` column (PREP:249; SSB:87).
- The axisymmetric analytic source uses `energy=mass*c*c` (RE:28).
- Response: one source-Hessian grid from a static β = 1 equal-time sample of the owned L4 parent, applied identically to every column. "No time/frequency axis exists in the grid" (TM:16; ASM:59 "Static sampling is NOT real-time evolution or cosmological history").
- The audit found "no Bind variable, history or operator in route A/B code" (TM:6). My own grep confirms this. Across all 41 `.py` files under DRV's folder, route_b_v006/stages and route_a/install there are zero hits for age, lookback, history weight, formation time, N_spent or Bind depth. "BIND" occurs only as a folder-path constant (DRV:134).
- Linearity: v_i² = Σ_j C_ij Σ_j + v²_ext + v²_hom at fixed response and background (ASM:1405-1408). The route is the stationary m = 0 member (RDA:40).

**Formal consequences** [FORMAL-RESULT: algebra on the code above].
- F-1. The predicted 43 velocities depend on baryons only through the total rest-energy density. A star kilogram and a gas kilogram at the same position carry identical source weight and see the same kernel.
- F-2. At fixed response, a species weight w★ on stars is exactly degenerate with Υ★ (w★·Υ★ enters PREP:210 as one number). Inside the counted ±20 % population band (0.4/0.6, SSB:28), a stellar-only Bind-history weight cannot be separated from M/L on velocities alone.
- F-3. Baryonic stellar mass fraction (HI+He and stellar reference; H2 excluded): DDO154 f★ = 0.0272 (1.1925e7 stellar, composed) or 0.0292 (1.2853e7, 64° reduction; PRIMER:863-864, conflict §12 #38), against 4.27e8 gas. NGC3198 f★ = 0.512 (1.459e10 stellar, 1.39e10 gas; PRIMER:861-863). These are arithmetic on cited numbers.

**Counted structural assumption to declare in the freeze manifest** [DECLARED-PREMISE once entered]:

> **SA-BH-01.** Every baryonic source element enters the common-metric source as rest-energy density −ρc² in the lapse channel only, with one universal weight per unit mass. This covers stars at Υ★3.6 = 0.5 (0.4/0.6 alternatives), HI×1.36 with helium once, and H2 with helium included. One response kernel, computed from a single static β = 1 equal-time owned-L4 state, acts on all of it. Source and response have no dependence on record history, Bind exposure, retention or lock state, formation epoch or source species. Alternatives to SA-BH-01 are UNTESTED; deciding tests are BH-T1 to BH-T3 of BIND_HISTORY_FRAMING_V001.

Placement: put it under the existing `semantics` and `notes` keys. MANIFEST_KEYS is a frozenset (FRZ:197-203); adding a key would be a reviewed-module change. Under CI:131 this is a root theory decision. It costs nothing on the critical path.

## 3. Derivation route: Bind history into the galaxy source without fitting (worked backward from the plug)

**Plug (120/43).** ASM:1408 states: "independent pressure/current/stress sources require their corresponding response columns". The plug is a record-structure-resolved response column, built as follows:
- C_ij^(χ) = −c² R_i ∫ k dk J₁(kR_i) B_j(k) Z_j^(χ)(k), with Z_j^(χ)(k) = ∫ dk_z/2π 𝓡^(χ)(k,k_z) F_j(k_z) (ASM:1401-1405).
- Each source species s carries its native record-structure variable χ_s.
- The kernel 𝓡^(χ) comes from Γ_ret's state response. Γ_ret is "the retained loop/Birth action… its state and response to the same metric" (ASM:1108).

This is the concrete remaining assembly operation ASM:1503, with history retained. A per-species scalar multiplier at PREP:210/249/266 would be the degenerate form (F-2). It is admissible only if the derivation delivers a k-independent ratio.

**Delivered quantity.** An effective source-response weight w(χ; k) is the Bind-dependent retained collective response per unit observed baryonic stress, as a function of the record-history variable χ. It is normalized against the same-state reference and pushed to the metric through the adopted RGRL map j_C = Aᵀj_g, χ_gg = A χ_CC Aᵀ (ASM:1497). One computed outcome is w independent of χ. That outcome confirms SA-BH-01 as the model's own law and registers as a result.

**Parent observable.** Δ_loop(T) (BH-c2), read against BH-c1 / BH-c4 / BH-c5 as candidate χ.

**Computation in existing machinery.**
- The instrument is the fixed-preparation real-time provider, "a distinct finite-domain/reference operation" (ASM:57).
- The static closed-worldline sampler cannot measure history: it has no time axis (TM:16; ASM:59), and its mixing is TESTED-NEGATIVE in every assessed run (PRIMER:128, 132, 1068-1071).
- Real-time Krylov producer custody exists (X/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/KRYLOV_FULL_N2_C1_COMPLETE_COMPARISON_CUSTODY_V001.json, status PASS_FIVE_COMPLETE_CHUNKS_AND_ORIGINAL_CUSTODY). Its fitness for O_loop is UNTESTED.
- The Volterra full-memory projection (ASM:235-262) is the formal carrier of history into the collective state.

**Chain** (each step UNTESTED):
1. Qualify O_loop on both complete sectors (LR:23).
2. Evaluate Δ_loop at fixed T on W/C preparations with the H0/H1 separation (LR:25, 27).
3. Repeat across a preparation family that varies χ at fixed Q/M and energy distribution.
4. Convert the coupling to work/tension (LR:29; MS:16).
5. Supply the baryon-to-record map from stars, HI, H2 and ionized gas to χ (T20H:37, 47: "C135 baryons must map to the native record/source object with all conversion assumptions counted").
6. Compute 𝓡^(χ) and the plug.

**Recorded blockers.**
- No qualified O_loop yet (LR:23-29).
- μ and g are not tension coefficients (LR:19).
- C-124, C-125 and C-131 forbid a classical Bind-count shortcut (REG:12168-12230).
- Sampler mixing is TESTED-NEGATIVE (PRIMER:132).
- The baryon-to-record map is missing (T20H:37).
- Real-time finite domains are tiny relative to galaxy scale. The controlled change of scale is open (T20H:41).
- Line A, B and C must meet on one parent: "joining results from different parents by relabeling is insufficient" (MS:12).
- Energy bound: in fixed-ice Q1, finite energy excludes an uncut 1/r erasure tail (P47H:13). Any history-carried reach must respect it.

## 4. Deciding tests (every outcome registers; none tunes to targets)

**BH-T1, DDO154 to NGC3198 calibration transfer.**
- Prediction-difference structure, at fixed response shape: δ(v_i²) = (w★/w_g − 1) Σ_j C_ij Σ★,j (ASM:1405-1408).
- DDO154 calibration sees the stellar channel at f★ ≈ 0.027-0.029. NGC3198 carries it at f★ ≈ 0.51 (F-3). To leading mass-weighted order, calibration absorbs about (w★/w_g − 1)·0.03 of the source. About (w★/w_g − 1)·0.48 transfers uncalibrated into the stellar-dominated NGC3198 rows.
- **BH-T1a** (pre-register before targets are opened). Define a target-free per-row f★(R_i) = M★(<R_i)/M_b(<R_i) from source arrays only. After freeze, report the correlation of standardized residuals with f★(R_i) over valid rows. Report it against the spread of the Υ★ 0.4/0.6 alternatives.
- Two readings must both be registered. Correlated residuals bear on SA-BH-01 and on Υ★ jointly (F-2). Residuals uncorrelated beyond the Υ★ band give no SA-BH-01 signal at that resolution. Neither reading is a verdict on Bind history alone.
- **BH-T1b** (after BH-D delivers 𝓡^(χ)). Freeze the 43-row δv_i vector before scoring. It is separable from M/L only if its radial shape differs from the stellar column's, through k-dependence or χ varying within the disk.
- Status: UNTESTED.

**BH-T2, Bullet Cluster lensing-centroid offset** (lensing phase, frozen parameters, no separate response function; CI:72).
- Under SA-BH-01 with a stationary, even, translation-invariant kernel and 𝓡̂(0) ≠ 0, the global first moment of the predicted convergence equals the baryonic-mass first moment (FORMAL-RESULT: convolution moment identity). The per-clump peak offsets are not fixed by that identity.
- The merger is nonstationary. The current branch does not apply: "Nonstationary states require the full temporal convolution and initial terms" (ASM:1410).
- Deciding test: with frozen DDO154/NGC3198 parameters, compute each subcluster's convergence-peak offset from the X-ray gas peak under the derived w(χ) and the full temporal convolution. Compare with the observed offsets. Every sign and magnitude registers.
- Definitional point: the intracluster gas is billions of years old. Calendar age therefore does not separate gas from galaxies. The operative variable must be a record-structure (Bind/lock) variable such as BH-c1, BH-c4 or BH-c5, mapped from observed baryon phases (T20H:37).
- Blockers: no nonstationary branch, no lensing projection (Q-g, PRIMER:1222), mergers lane OPEN (LAD:214).
- Status: UNTESTED.

**BH-T3, record-level tests already in the program.**
- C-71: the accumulated source-like quantity of a formed record surface depends on encoding. Occupancy-encoded NAND charge is one-signed. Orientation-encoded real data tracks screen (measured ratio 0.00096) (SL:238). [TESTED-POSITIVE: two device-physics models.] A program-run device measurement is UNTESTED (PRIMER:120).
- P-18: S and q censuses from all-blank and all-written preparations (V005:19). [UNTESTED.] This is the native test of whether Bind writing accumulates (BH-c3).
- GE-X48: equal counts, different retained-memory topology, different response (GE:83). [FORMAL-RESULT on a supplied sheet.] Owned-parent transfer is UNTESTED.
- "Mass resists Birth" bound versus non-bound availability comparison. It needs "a justified native binding predicate" (C1/READINESS_NATIVE_RECORD_FIRST_CONDITIONAL_OWNERSHIP_DECISION_2026-10-15_V001.md:21). [UNTESTED.] It is the same predicate χ needs, so both should share one definition on one parent.

## 5. Imports ledger, lineage, prior work, sign-off

**Imports ledger.** New load-bearing imports: **none**.

| Item | Disposition |
|---|---|
| Bullet Cluster lensing, X-ray and galaxy maps | OBSERVATION. Enters only at BH-T2 with primary provenance (CI:72). Not used here. |
| Stellar-population ages or age-dependent M/L as the history proxy | EXCLUDED: imports classical stellar evolution as χ |
| ΛCDM fractions (.30/.70), halos, fitted weights | EXCLUDED (CI:68; HO:25 via PRIMER:902-903) |
| 3:7 Dense Bound Record partition | EXCLUDED: "SUPPLIED_PREMISE", must not become Ω_A = .7 (NRP:22-30) |
| Reviewer τ_Q = t_P·exp(1/α_s) memory kernel | EXCLUDED: TESTED-NEGATIVE as a mechanism (KT:48) |
| Υ★ = 0.5, ×1.36, h★ = R_d/7.3 | Pre-existing counted source choices (SSB:28-30; RSR:110); not new |

**Lineage.**
- A: the Line-A DM identification and its new Bind reading (LR:13-19), C-88, C-124/125/131.
- B: the galaxy route under RGRL/WTC, and GE-X48. "the 120/43 kernel carries no Γ" (LB:36 P-c).
- C: V005 / the owned parent, NPSI, P-18.
- The route must close on the owned parent (ASM:203; MS:12).

**Prior work** (build on these; no restart, M2):
- T20H:37-39: "Keep a structured operator or history-dependent object if that is what the dynamics supplies"; accumulation must carry "history where present".
- P47H:11: "History can have a different range from the bound cloud" (stochastic control, not a field law).
- P47L:11-13: g = 0 has exposure but zero writing.
- P58H and C-131: the fine-history obstruction.
- GE-X48.
- NRP: the earlier Dense Bound Record fiber proposal (HELD; its ratio is excluded).
- KT: τ_Q assessed.

**Sign-off needed.**
- Principal: register the 2026-10-17 statement in PR verbatim, with the two classes in §0. This draft does not alter PR.
- Root (CI:131):
  - enter SA-BH-01 in the freeze manifest;
  - pre-register BH-T1a before any target is opened;
  - pass this gate before any BH-D dispatch. BH-D is the existing ASM:1503 / LR:29 work with history retained, not a new framework.
- Named next step: qualify O_loop on both complete sectors (LR:23).
