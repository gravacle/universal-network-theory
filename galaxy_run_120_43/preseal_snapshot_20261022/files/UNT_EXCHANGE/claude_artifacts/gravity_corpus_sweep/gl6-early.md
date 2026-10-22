# GL6 early partition (Q through AM): raw sweep notes

Date: 2026-10-12. Read-only sweep. No project code executed. One scratch check of my own (numpy, scratchpad) is reported in section 0.

Roots used:
- PW = `/Users/bgm/Research/Universal Network Theory/program-worktree`
- WA = `/Users/bgm/MB Work/where-atoms-come-from` (holds the lane folders missing from PW: GL6Q lane, GL6R, GL6X, GL6AC, GL6AD, GL6AE, GL6AJ, GL6AL)

Not found anywhere: no other GL6 letters between Q and AM. GL6AN and later are outside this partition.

## 0. Headline crosswalk to P-37 (my inference plus one scratch check)

**The graph and Hamiltonian.** The FPSS bulk used by GL6Y through GL6AM is the q4 diamond lattice.
- GL6AK writes the site set as `L = A3 x {1,2,3,4}`. A site is a link from parent x in S_N to child x+e_a in S_{N+1}.
- Projected onto the 1-perp hyperplane, parents and children form two FCC (A3) sublattices joined along the tetrahedral vectors n_a. That is diamond.
- The bulk link Hamiltonian is `-h sum X + eps* sum n + 2U_d sum_{line-graph pairs} n_e n_f`. That is the #7 incidence term plus the degree energy `U_d sum_v (d_v-d*)^2` over both sublattices, without carriers, Bind/feedback or Birth.
- Gating is by the record-support projector `P^K`.
- Path: PW/LANE_CROSS_RFT_GRA_GL6AK_A3_QUASILOCAL_BULK_DYNAMICS_V001/THEOREM.md, eqs. AK01 to AK06 and AK09.

**Regime.** The partition works at an unlocked witness, not in the ice/Coulomb phase:
- h = U_d = E0 and Delta = 6E0, so eps* = 0 (GL6AB, AG, AH, AJ, AL);
- or h = 1, Delta = 13, U_d = 1, d* = 2 (GL6U, GL6Y).

**The representation split the partition proved repeatedly.** At a q4 vertex the six pair coordinates (port pairs = bond angles) decompose as follows.
- `im P = A1 + T2`. This is the one-body or incidence image, `(Pu)_ab = u_a + u_b`.
- `ker P^T = E`. This is the genuinely two-body part (two-dimensional diagonal shear).
- Sources: GL6S (S09 to S12), GL6Z (Z17, Z18), GL6AB (AB01 to AB07), GL6AH (AH12 to AH21).

**Scratch check.** Script: gl6-early_ice_pairs_check.py in this folder (numpy; run with plain python3). On the six d=2 (ice) states of one q4 vertex, with P-37's polarization `e = sum_a n_a sigma_a`:
- (a) The T2 projection of pair occupations `n_a n_b` (the bond-angle source variable) is exactly linear in e. The fit residual is 3e-16.
- (b) The T2 projection of the pair products `Z_a Z_b` is identically zero.
- (c) The E projection of `Z_a Z_b` is nonzero and even in e (an e_i^2-type quantity).

So on the ice manifold, the GL6 statement that one-body pair data live in A1 + T2 and E needs a genuine pair is the same fact as P-37 eq. (2), where the E-type diagonal source is quadratic and the T2 shear source is linear in polarization. Path: /Users/bgm/Research/UNT_EXCHANGE/lanes/P37_CODEX3/P37_FORMAL_UNIFORM_ENDPOINT_COULOMB_RESPONSE_V001.txt, section 2, eqs. (1) to (4).

The corpus saw the same obstruction from the other side.
- In the unlocked regime, the one-body channel (A1 + T2) is the one that propagates through the bulk.
- E2 is null at first cross-cell order and null at all orders through a single bridge. It opens only through cycles (sibling triangles), and at the orders computed it is boundary-owned: it cancels in the homogeneous interior.
- The relevant lanes are GL6Z, GL6AB, GL6AD, GL6AE and GL6AH.

What this implies for P-37 (inference):
- A pair source whose T2 component is nonzero will couple linearly to polarization on ice. That is forced by the incidence image, not an accident of the P31 coefficients.
- The genuinely quadratic single-vertex channel (`Z_a Z_b`, which the GL6V/GL6W apparatus sources and reads) carries only A1 + E on ice. It has no T2 at all.
- So a gauge-invariant stress-like T2 (off-diagonal) component must come from products of polarization at different vertices, or from cycle/ring operators.
- GL6AB already proved that two distinct ports at both endpoints, meaning a cycle, are the minimal requirement for E-sector transport. A diamond hexagon uses two distinct ports at each of its six vertices.
- That makes the hexagon ring-exchange (magnetic, curl) channel the natural carrier in the locked phase. This is a pointer, not a corpus result.
- GL6R separately shows an alternating-sign hexagon sum that annihilates single-node (one-body) write sectors and passes only the joint two-node sector.

**Isotropy condition derived from GL6W (W27, W28).**
- Every S4-covariant six-pair kernel is `K = k_d I + k_a A_L + k_b A_O`.
- `K_E - K_T2 = 2(k_b - k_a)`, so E/T2 spin-2 isotropy holds if and only if `k_a = k_b`.
- For the GL6T factorized kernel (T11, T12), `K_E / K_T2 = 1 - z^2`. It is isotropic if and only if `z = <Z> = 0`, i.e. half-filled links, mean vertex degree 2, the ice filling.
- This is an entrance-slope property of a transient, not a static stiffness. Derived by me from the corpus formulas.

## 1. GL6Q: lifecycle write to incidence (one link)
- Paths: WA/LANE_CROSS_RFT_GRA_GL6Q_F3_LIFECYCLE_TO_INCIDENCE_RESPONSE_V001/{THEOREM,RESULT}.md; audit PW/AUDIT_G_GL6Q_F3_LIFECYCLE_TO_INCIDENCE_RESPONSE_V001/AUDIT.md (PASS).
- BU hold Hamiltonian: `H_R = eps_r q_r - h_N X_a + (E0 - lambda_R q_r) n_a` (Q08).
- Partial write: `D_TV = sin^2 Phi`. Incidence response: `Delta n(Phi,T) = sin^2 Phi * Delta n_full(T)`. Ordered response: `B_e^R = sin(2Phi)/hbar * Delta n_full(T) * 1_{I_W}`.
- A positive lambda_R gain is required. The validity audit (V001, rung 1) flags that arrangement dependence in BS/F3 holding-cell results is "put in by the lambda_R coupling".
- No geometry. It is the first record-to-incidence arrow.

## 2. GL6R: lifecycle writes into the alternating hexagon causal block
- Paths: WA/LANE_CROSS_RFT_GRA_GL6R_F3_LIFECYCLE_TO_LOCAL_CAUSAL_BLOCK_V001/{THEOREM,RESULT}.md; audit WA/AUDIT_G_GL6R_*/ (PASS). Parent: WA/DISCOVERY_GL5ZZT_F3_RECORD_DIAGONAL_CAUSAL_BRIDGE_V001/RESULT.md.
- Partner splitting: `Delta D(r) = sum_e s_e 2 lambda_R Q_e / (4U_d^2 - lambda_R^2 Q_e^2)`, with `s = (-1,+1,-1,+1,-1,+1)` (R09).
- Witness U_d = 1, lambda_R = 1/2, h = 1 gives `Delta D_00 = Delta D_10 = Delta D_01 = 0` and `Delta D_11 = -2/15` (R10).
- The single-write sectors cancel by the adjacent alternating sign. Only the joint write survives, through the nonlinearity in edge load (Q_4 = 2).
- Response: `bar chi = -(2/15) eps^3 C^(11) sin^2 Phi4 sin^2 Phi5` (R13).
- The paper says explicitly that this does not close the q4 pair-deformation solder (R17 discussion).
- Bearing: a ring-curl structure that kills one-body (gauge-like) inputs and passes a two-body one. Model: effective O(h^2) RCRS diagonal, not the #7 tuple.

## 3. GL6S: independent-write q4 solder-rank boundary
- Paths: PW/LANE_CROSS_RFT_GRA_GL6S_F3_INDEPENDENT_WRITE_Q4_SOLDER_RANK_BOUNDARY_V001/THEOREM.md; PW/AUDIT_G_GL6S_*/AUDIT.md (PASS).
- `m_ab = C_ab p_a p_b` (S04). `rank D_p f_C <= 4` (S07). The image has empty interior in R^6.
- At the S4 point: `D_p f_C = C p A`, `A^T A = 2I + J`, `im A = A1 + T2`, `(im A)^perp = E2` (S10, S11).
- The EW map sends E2 to the two tetrahedral diagonal-shear directions of Sym^2(V).
- The missing datum is a same-parent response with nonzero E2 projection. It is parametrized as `h_A = a+4b+c`, `h_E = a-2b+c`, `h_T = a-c` (S15).
- Context, outside the partition: EW = PW/LANE_CROSS_RFT_GRA_EW_Q4_PAIR_MEMORY_METRIC_DEFORMATION_CLOSURE_V001/THEOREM.md.
  - It defines the metric as a localization Fisher/QFI tensor on V = 1-perp.
  - With nine-parameter exponential-family pair memory J_ab, it gives `D_J F_theta(0): R^6 -> Sym^2(V)` as an isomorphism (EW05 to EW13).
  - One-body softmax alone gives T2 only. Scalar rescaling adds A1. E is missing (EW10).
  - This is the only metric solder map in this lineage. The EW paper itself says it is "not physical space without localization/soldering".

## 4. GL6T and GL6U: lineage-gated q4 pair response, plus the degree interaction
- Paths: PW/LANE_CROSS_RFT_GRA_GL6T_F3_LINEAGE_GATED_Q4_E2_RESPONSE_V001/{THEOREM,RESULT,README}.md; PW/LANE_CROSS_RFT_GRA_GL6U_F3_DEGREE_INTERACTION_Q4_RESPONSE_V001/{THEOREM,RESULT}.md; audits PASS.
- GL6T: `H_star = sum_a [-h P^K_a X_a + Delta n_a]` (T05). `D_KEEP = -8hx I_6 - 4hx z^2 A_L(K4)` (T11).
  - Sectors (T12): `D_A1 = -8hx(1+2z^2)`, `D_E2 = -8hx(1-z^2)`, `D_T2 = -8hx`. BREAK gives 0 (T14).
  - Onset (T16): the E2 term is O(tau^4) while A1 and T2 are O(tau^2). E2 is a multi-link pair-coordinate response.
- GL6U restores `U_d[(d-d*)^2 + sum (n_a-d*)^2]` (U04).
  - Dicke reduction (U07). `D = -8hx I - 4hy A_L` (U12).
  - Interaction-owned factorization defect: `y - x z^2 = -(16/3) h^3 U_d (tau/hbar)^4` (U16).
  - Open full-rank domain: U_d > 0, delta1 > 0, 2delta2 - delta1 > 0 (U19).
- Both papers note that the Hamiltonian reads physical P^K, not REC. The validity audit (rung 5) separately flags that "lineage changes future dynamics" follows algebraically from the adopted lineage-conditioned write and lacks a negative control. The K-gating here is the same kind of construction.

## 5. GL6V, GL6W and GL6X: physical pair source/read and normalized CTP kernel
- Paths: PW/LANE_CROSS_RFT_GRA_GL6V_Q4_PAIR_PHASE_SOURCE_READ_DILATION_V001/THEOREM.md; PW/LANE_CROSS_RFT_GRA_GL6W_Q4_NORMALIZED_OPERATOR_NEUTRAL_CTP_KERNEL_V001/THEOREM.md; WA/LANE_CROSS_RFT_GRA_GL6X_SELECTED_APPARATUS_SPECTATOR_CANCELLATION_V001/RESULT.md; audits PASS.
- GL6V:
  - Copy, phase, uncopy: `U_src(j)|psi>|0^6> = exp((i/2) sum_A j_A Z_a Z_b)|psi>|0^6>` (V07).
  - System source: `H_src = -(hbar/2) sum_A j_A f_A(t) M_A` (V08).
  - Seagull: `d^2 H_src / dj dj = 0` (V12).
  - This is a quadratic (pair-product) source, but as external probe apparatus, not a bulk force.
- GL6W:
  - `G^R = (i/2hbar) Theta <[Q_B(t),Q_A(s)]>` and `G^R = -(E*^2/2) chi^R_MM` (W08, W09).
  - Closed U_d = 0 kernels (W15 to W19). Spectral compiler with J = 2, 1, 0 blocks giving A1, T2, E (W25, W26).
  - General kernel `K = k_d I + k_a A_L + k_b A_O`. Sectors `(k_d+4k_a+k_b, k_d-2k_a+k_b, k_d-k_b)` (W27, W28).
- GL6X:
  - Spectators cancel exactly under source-independent hypotheses: `K_eff = K_JJ`.
  - Counterexample: a source-dependent spectator adds the contact `i hbar lambda_z^2/4`.

## 6. GL6Y: FPSS cell graph and shared-child connector
- Paths: PW/LANE_CROSS_RFT_GRA_GL6Y_FPSS_SHARED_CHILD_CONNECTOR_V001/THEOREM.md; PW/AUDIT_G_GL6Y_*/AUDIT.md (PASS).
- `m ~ n iff n = m + e_a - e_b`. `deg <= 12`. `d(m,n) = ||m-n||_1 / 2`. `|S_N| ~ N^3/6`, with cubic ball bounds (Y04 to Y08). This is combinatorial three-dimensionality of a supplied program.
- Connector: `2U_d n_e n_f = (U_d/2) Z_e Z_f - (U_d/2)(Z_e + Z_f) + U_d/2` (Y11).
- Cubic cross-cell jet: `[ad_H^3 B, A] = -8 h^2 U_d X_e X_f Z_p Z_q` (Y16).
- Scalar witness: `<O> = (h^2/3) A* B* (tau/hbar)^4`, with `A* = Delta + (3-4d*)U_d` and `B* = 3Delta + (8-12d*)U_d` (Y24, Y25).
- A shared node does not by itself give an atlas (Y28).

## 7. GL6Z: multicell CTP k^2 jet
- Paths: PW/LANE_CROSS_RFT_GRA_GL6Z_MULTICELL_CTP_K2_JET_V001/THEOREM.md; PW/AUDIT_G_GL6Z_*/AUDIT.md (PASS).
- `[tau^4 t^3] G^R_{nB,mA} = C* P_Bb P_Aa`, with `C* = -2 E*^2 h^4 U_d A* B* / (9 hbar^8)` (Z13).
- Program-frame symbol: `K(k) = P [z z^dagger - I] P^T`, with `z_a = exp(-i a* k.n_a)` (Z16).
- `rank K = 4` and `ker K = ker P^T = E2` for all k (Z18). `K_A1(0) = 18`, `K_E2(0) = 0`, `K_T2(0) = -2` (Z19).
- Isotropic A1 seed: `+(16/9) E*^2 h^4 U_d A* B* / hbar^8 * a*^2 |k|^2` (Z23). The program-frame chart is `X(m) = a* sum_a m_a n_a` (Z15a), with a* uncalibrated.

## 8. GL6AA: record-authenticated shared-child atlas
- Paths: PW/LANE_CROSS_RFT_GRA_GL6AA_RECORD_AUTHENTICATED_SHARED_CHILD_ATLAS_V001/{THEOREM,RESULT}.md; audit PASS.
- The old pairwise query is non-identifying: 3! extensions per port match, plus a holonomy counterexample (AA02, AA03).
- Selected completion: node-ID records and port-label records, compared against an independently copied expected tuple, under a MATCH/MISMATCH/BLANK/COLLISION query.
- `J^1_e = J^1_f iff` same physical child (AA12). `delta_nm = e_a - e_b`, antisymmetric, with an all-cycle cocycle (AA13 to AA15).
- Frames `lambda_m in S4`, `g_nm = lambda_n^{-1} lambda_m`, `T^(6)_nm = rho_6(g_nm)`, with inverse and cocycle laws (AA16, AA17).
- This gives a discrete flat chart and frame field with records as ancestry. There is no length and no dynamical displacement.

## 9. GL6AB and GL6AC: one-bridge E2 null, cycle escape, rank-two observability
- Paths: PW/LANE_CROSS_RFT_GRA_GL6AB_E2_MULTI_CONNECTOR_TRIANGLE_V001/THEOREM.md; WA/LANE_CROSS_RFT_GRA_GL6AC_STACKED_OUTGOING_E2_OBSERVABILITY_V001/RESULT.md; audits PASS.
- `W^{H_a} ∩ E = {0}`. Under the H_a x H_b equivariance premise, `K_nm Pi_E = 0` at every order (AB07 to AB11).
- Two distinct ports per endpoint are necessary: `||Pi_E w^{ac}||^2 = 1/3` (AB14).
- The minimal motif is the A3 sibling triangle (a 3-cycle of cells) (AB15 to AB17).
- Full N = 1 block: `Q_{p,r} = 0` for p + r <= 18. The first nonzero coefficient is at order 19, `Q_{16,3} = -67530641899520`, rank 1 in E x E (AB27 to AB29).
- `[tau^16 t^3] G^R = -(103043582/383107725) E*^2 E0^19 / hbar^20` (AB35).
- GL6AC: three neighbor blocks, `K10 ∝ [[1,1],[1,1]]`, `K20 ∝ diag(1,0)`, `K30 ∝ diag(0,1)`. The stacked rank is 2.

## 10. GL6AD, GL6AE and GL6AH: bulk versus boundary ownership
- Paths: WA/LANE_CROSS_RFT_GRA_GL6AD_BRIDGE_CLUSTER_PERSISTENCE_V001/RESULT.md; WA/LANE_CROSS_RFT_GRA_GL6AE_INTERIOR_DEGREE4_E2_SUPPORT_V001/RESULT.md; PW/LANE_CROSS_RFT_GRA_GL6AH_BULK_BOUNDARY_IRREP_SEPARATION_V001/THEOREM.md; audits PASS.
- GL6AD:
  - `Q^{E,[3]}_{16,3;nm} = q3 [xi_n^(b)]^T xi_m^(a)`, with `xi_m^(a) = sum_{c != a} r_{m,c} E_{{a,c},:}`. Here `r_{m,c}` counts the other parents of the child reached through port c (AH25).
  - In the homogeneous interior `r = 3` and `xi = 0`, so the cubic piece cancels in the bulk.
  - The paper notes that "uniform formed memory is cubic-flat; port-multiplicity imbalance sources E2".
- GL6AE: the bridge-degree-4 E2 component is 0 on every interior edge (2971 embeddings, 26 classes, 104/104 zero).
- GL6AH:
  - Direct edge: `Delta Q_{n,6} = -128 h^4 U_d^2 u_b^in`, where `u_b^in = (1 + s_b)/2`, i.e. equal A1 and T2 (AH09, AH14, AH15).
  - The E-null holds at all orders by Reynolds averaging (AH19 to AH21).
  - The order-12 and order-16 E terms come from helper chains, `eta_n^(b) = sum_{d != b} r_{n,d} w_bd`, and `eta = 0` in the homogeneous interior (AH26 to AH28, AH32).
- Net result: at the computed orders, homogeneous-bulk pair propagation lives in the one-body A1 + T2 channel. E2 is boundary-, imbalance- or cycle-owned.

## 11. GL6AF and GL6AG: formation pattern as an E-plane source, and neighbor propagation
- Paths: PW/LANE_CROSS_RFT_GRA_GL6AF_FORMATION_PATTERN_E2_SOURCE_V001/{THEOREM,RESULT}.md; PW/LANE_CROSS_RFT_GRA_GL6AG_N1_FORMATION_NEIGHBOR_PROPAGATION_V001/{THEOREM,RESULT}.md; audits PASS.
- GL6AF:
  - Zero or one formed lineage gives `E^T D E = 0`.
  - Two formed lineages give `E^T D^(ab) E = -16hx(1-z) w_ab^T w_ab`, which is rank 1. Which pair forms selects the direction (AF10, AF11, AF13).
  - Three or four formed lineages give rank 2 (AF14, AF15).
- GL6AG:
  - Source cell: `Delta_ab mu_0^E = 4 u^4 w_ab`. Neighbor: `Delta_kappa mu_c^E = -(5626/42525) u^12 kappa_c w_0c` (AG01, AG02).
  - Additive up to u^16 (AG22 to AG24). Ablating the shared-child terms makes it exactly zero (AG26).
- GL6AH (above) later shows that this E is helper-chain and boundary-owned.

## 12. GL6AI: relational influence (Lieb-Robinson) envelope
- Path: PW/LANE_CROSS_RFT_GRA_GL6AI_F3_RELATIONAL_INFLUENCE_ENVELOPE_V001/THEOREM.md; audit PASS.
- `H = H_on + sum 2U_d n_e n_f` (AI04 to AI06). `deg_L <= 6` (AI08).
- `||[tau_t(A_e), B_f]|| <= 2 ||A|| ||B|| T_{d_L}(48|U_d| |t|/hbar)` (AI15).
- `v_mu = 48|U_d| e^mu / (mu hbar)` (AI21), using `d_L >= ||m-n||_1 / 2`.
- The envelope speed is set by U_d, not by the emergent photon speed `sqrt(U_e K_b)`.

## 13. GL6AK and GL6AM: thermodynamic-limit bulk and authenticated windows
- Paths: PW/LANE_CROSS_RFT_GRA_GL6AK_A3_QUASILOCAL_BULK_DYNAMICS_V001/THEOREM.md (post-freeze audit PASS); PW/LANE_CROSS_RFT_GRA_GL6AM_AUTHENTICATED_BULK_RESPONSE_FUNCTIONAL_V001/THEOREM.md (audit PASS).
- GL6AK:
  - Boundary series (AK17), norm-Cauchy dynamics (AK19), `A3 x| S4` covariance (AK21).
  - Invariant states exist (AK25).
  - Positive spectral measure `mu = mu_A1 P_A1 + mu_E P_E + mu_T2 P_T2` (AK33).
  - The character is not physical momentum (AK34, AK35).
- GL6AM:
  - Pulse-word limits (AM07, AM08) and retarded kernel (AM10).
  - A K-word is a local defect, `V = h sum (1-kappa) X` (AM20), with a cocycle limit (AM24) and a defect tail (AM25a).

## 14. GL6AJ and GL6AL: stationary spectra
- Paths: WA/LANE_CROSS_RFT_GRA_GL6AJ_N1_STATIONARY_PAIR_KRYLOV_EXPLORATION_V001/RESULT.md (audit: PASS as a mutable exploration); WA/LANE_CROSS_RFT_GRA_GL6AL_SIGN_FREE_IMAGINARY_TIME_PRESCREEN_V001/{RESULT,COMPARATOR,METHOD}.md (no audit).
- GL6AJ at N = 1:
  - Perron-Frobenius unique ground state. S4 orbit form `C = c_d I + c_a A_L + c_o A_opp`.
  - Variances: A1 1.49, E 0.43, T2 1.10.
  - Lowest source-visible gaps: A1 2.07, E 2.43, T2 1.94. No soft mode.
- GL6AL, sign-free QMC at N = 4 (first graph with degree-6 interior links): no slow A1, E or T2 feature at (r_eps, r_U) = (0, 1).
- GL6AL degree-locked comparators (-6, 1) and (-12, 2), uniform source: equal-time weight moves from A1 to E (E: 0.35 to 1.22 to 1.30; A1: 1.49 to 0.54 to 0.33).
  - These comparators are unadopted, and the run is autocorrelation-limited.

## 15. What is not in the partition
- No dynamical displacement or embedding field (delta u = xi).
- No elastic modulus or Keating term.
- No Debye screening.
- No d* = 2 locus where the linear coupling vanishes.
- No ring-exchange (H6) source writer. The H6 tensor writers and cycle-response tensors are GL6CH to GL6CQ, outside this partition.
- The one solder map, EW's Fisher/QFI pair-memory map, is outside the partition and is not physically calibrated (GL6V, section 6).
- The A3 chart `X(m) = a* sum m_a n_a` is a supplied program frame. GL6AA authenticates it with records but does not make it dynamical.
