# Raw notes: non-GL6 cross lanes and bridges (deformation, solder, constraint, curvature)

Sweep date 2026-10-12. Read-only. No project code executed.
Root: `/Users/bgm/Research/Universal Network Theory/program-worktree/` (written PW below).

Partition read in full: ES, EW, EX, GL5ZZF, GJ(cross), GK(cross), EI, EQ, ER, EU, EZ, FB
(all `LANE_CROSS_RFT_GRA_*` minus GL6; 12 lanes), plus
`DEVELOPMENT_R_OWNER_ONCE_L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_V001`.
Only GL5 lane present on disk: GL5ZZF. Its cited upstreams GL5ZZA, GL5ZZE, GL5ZF have no
directory in PW or under /Users/bgm/Research (custody gap, noted).

The upstream F-lanes that GK and GL5ZZF compose (FT, FU, FV, FX, FY, FZ, GB, GD, GJ-flip, FR)
are `LANE_GRA_*`, so they fall outside this partition. I read their RESULT.md files (and FV's
THEOREM.md) only because they decide the P-37 question.

---------------------------------------------------------------------------------------------

## 0. Headline for P-37 (my synthesis; each premise cited)

1. **Same source-off Hamiltonian, different source law.**
   - The V006 canonical photon block is `H_gamma = -h SUM X + Delta SUM n + U_d SUM(d - d*)^2`,
     with `Delta = 4U_d(d*-2)`, `d* = 3`, `U_d = 1`.
   - By the degree-lock identity this is `U_d SUM_v (d_v - 2)^2 + 5U_d * (#sites)`, so
     `d_eff = d* - Delta/(4U_d) = 2` (`.../20260924 Packet Updates/FIRST_CHUNK_PREMISE_CARD_V006.md`
     lines 266, 806, 811).
   - That is exactly construction #3 (`-h SUM X + U_d SUM (k-2)^2`) of the validity audit
     (`UNT_VALIDITY_AUDIT_V001.md` App. A).
   - The F3 source chain FT -> FU -> FV -> FX -> FY -> GL5ZZF/GK lives on that block.

2. **FT proves the source derivative is not fixed by source-off dynamics.**
   - The same `H[j=0]` admits the rank-4 FS source and a rank-6 root-pair source
     (PW/LANE_GRA_FT_.../RESULT.md: "source-off dynamics plus observable availability cannot
     determine the source derivative").
   - P-37 itself notes: "Crosswalking source-OFF constants does not license reweighting their sources".

3. **The two source laws dress different terms.**
   - The corpus F3 source (FV01, PW/LANE_GRA_FV_.../THEOREM.md §2) is
     `H[j] = H_C[j] - h SUM_e (1 - 1/2 j:D_a(e)) X~_e`, with
     `H_C[j] = H_C[0] - (U_d lambda/2) SUM_v SUM_{a<b} (j:R^_ab) Z_a Z_b + H_id`.
   - It dresses only the **pair Z_aZ_b** (signed, +/-1 basis) and the **flip amplitude h**.
   - Both commute with the global incidence flip `G = PROD_e X_e` (E -> -E, charge conjugation).
   - So the corpus source has **no G-odd (linear-in-polarization) term, by symmetry.**
   - P-31 V002 instead dresses the storage `Delta n_e` (edge owner) and the 0/1 cross products
     `n_a n_b = (1 + Z_a + Z_b + Z_aZ_b)/4` (angle owner)
     (`UNT_EXCHANGE/lanes/P31_CODEX3/P31_BOND_ANGLE_SOURCE_SUCCESSOR_V002.md` lines 115-116).
     Both carry G-odd linear Z pieces.
   - That yields P-37's `lambda = (2/9)(3 Delta - 4U_d) = 16U_d/9` at the canonical tuple
     (`P37_FORMAL_UNIFORM_ENDPOINT_COULOMB_RESPONSE_V001.txt` eqs (2)-(4)).

4. **What the flip-even route keeps and removes.**
   - With the F3 law: E (diagonal-traceless) comes from the direct pair. It is quadratic in
     polarization, the same as P-37 eq (5).
   - A1+T2 come only from the **differentiated H6 ring**,
     `T^bar_C = (21/8)(8 - 15 lambda) I - (63/8)(2 - 5 lambda) D_d`
     (FV10, all 720 histories, Hermitian average).
   - This is a gauge-invariant ring (magnetic) channel at order `h^6`.
   - Projected nonidentity rank = 2_E + 1_A1 + 3_T2 = 6 (FV15; det W = -4678629417/256).
   - The linear k^0 piezo block chi_lin and its Ward residue `2 lambda^2 k1k2k3/(U_e k^2)`
     scale as lambda^2. They are therefore **absent identically**.
   - This is P-37's "gauge-invariant quadratic stress-like (Maxwell-stress) channel", and it
     already exists in the corpus.

4a. **Symmetry caveat: G versus winding sectors.**
   - G maps a fixed winding/flux component to its complement partner. GL5ZZF's
     occupation-complement isometry `F: H_+ -> H_-` (ZZF09) is G restricted.
   - So inside one nonzero-winding finite component, G does not forbid a mixed linear response.
     The forbidding statement holds for the G-invariant (zero-flux / complement-doubled) sector.
   - That is the sector P-37's Gaussian k != 0 calculation uses. P-37 itself notes that odd
     Gaussian moments kill the linear/quadratic mixed covariance there.
   - Check also: P(-hX)P = 0. Every single flip from ice costs exactly `2U_d`
     (V006 card line 268), so the h^2 term reduces to identity. G5 has girth 6, so there is no
     h^4 ring. FX shows the H2/H4/H6 diagonals reduce to pair + identity.
   - So no linear-e operator appears in the F3 source through h^6.

5. **Status of that route. It is not a gravity result.**
   - FV-PURE (S10) and FU S1-S9 (signed terminal charges, grounded elastance, reservoir-dressed
     flips FU09b) are conditional or adopted completion premises.
   - FX: complete homogeneous source, H2-H6 diagonal reduces to the pair:
     `f_E(x) = 1 - x^2 - (37/12)x^4 - (16247/900)x^6`; response ranks 5 -> 3 -> 2 -> 2 (homogeneous).
   - FY: m = 1 response ranks 6 -> 6 -> 6 -> 6 -> 6 at x = 2/5 and 1/2; TT rank 2; gapped finite poles.
   - FZ: source nontransverse under the supplied embedding contraction; Ward **undecided, not failed**.
   - GB/GD/GJ: momentum ownership is open; the bare recoil density fails the supplied-embedding Ward test.
   - GL5ZZF: member-identifiability stop (`a(x)D1 + R1`).
   - Canonical x = h/U_d = 1/5 has never been run in this chain (samples were x = 2/5, 1/2).
   - G-evenness holds in P-37's Q0 vacuum domain (carriers vanish, Records blank). Outside Q0,
     carriers/Bind/Records may break G. Not checked.

6. **Second cross-link: the EW/GK/PMICS "metric" is the vertex polarization covariance.**
   - `F_theta = Cov(X) = <XX^T> = I_V + SUM C_ab (v_a (.) v_b)`, with `X = Ps`.
   - GK identifies s with Z (`P_ab = Z_aZ_b`). P-37's `e = SUM n_occ,a sigma_a` gives
     `SUM Z_a sigma_a = 2e`, so X is proportional to e.
   - So the corpus already has an explicit **metric solder map from network observables**:
     `h_ij = l_F^2 <e_i e_j>`, the electric-stress / inverse-electric-stiffness (dielectric-type)
     tensor.
   - GK's reciprocity `d_j F = (beta/2) d_theta^2 <Q>` is an electrostriction-type Maxwell
     relation: quadratic, not piezo.
   - In pure ice (`a = e^{-beta U_d} -> 0`) the pair covariance is rank 2, E only (GK29):
     `g_A1 -> 0, g_E -> 8/3, g_T2 = 8a/D -> 0`.
   - T2 and A1 metric deformations in this channel need charge-defect (monopole) population.
     That is a direct corpus bearing on P-37's "Debye screening" rescuer.

7. **Displacement sector.**
   - The PMICS curvature kernel is exactly the pure gradients `h = k (.) xi`. This is the
     linearized displacement/diffeo sector, present only as gauge.
   - A physical displacement/recoil field exists only as GD's auxiliary mechanical-torus
     existence witness.
   - GJ shows that the bare GD momentum density cannot close the supplied-embedding Ward test.
     Its recommendation is one pre-projection `H[h00, h0i, hij; ports]` owning flip recoil and FU
     pair field/support momentum.

8. **Constraint propagation (EX/SDCP).**
   - Six spatial deformations plus the complete Ward identity (EX05) plus zero initial
     constraints give all ten equations.
   - This is imported GR (contracted Bianchi). It sharpens P-37: rank 6 is not the issue,
     (EX05) is. P-37's nonzero static Ward residue is exactly a failure of EX05 for P-31's response.

9. **The other lanes are kinematic and conditional.**
   - GSGB, SCGQA, RMLB, TROV, RFCD, RTHW, BQ4RSW all feed RGRL A/B/C (ADOPT).
   - GSGB-4/EX/PMICS invoke RIEHB (induced Einstein-Hilbert, imported) or Malament/HKMM (imported).
   - None derives an Einstein kernel.

---------------------------------------------------------------------------------------------

## 1. Per-lane notes

### ES -- GSGB gamma-soldering-gravity bridge
Path: PW/LANE_CROSS_RFT_GRA_ES_GAMMA_SOLDERING_GRAVITY_BRIDGE_V001/THEOREM.md.
Audit: INDEPENDENT_HOSTILE_AUDIT.md, ACCEPT, 121/121.

**Three typed gammas.**
- `gamma_Q`, record query (ES01-02): `D_TV >= B_rec -> gamma_Q <= 1 - B^2`.
- `gamma_IF = exp(-N(f,f)/hbar^2)`, influence functional (ES03).
- `gamma_state`, Uhlmann (ES03a).

**GSGB-2 coframe.**
- `F_ij = -2 d_i d_j log gamma_state` on the A3 tangent `V = 1^perp`.
- `s_ij = l_gamma^2 F_ij = delta_AB e^A_i e^B_j`, so `ds^2 = -c^2 dT^2 + s_ij dxi dxi` (ES07-ES12).
- S4 Schur gives `F|_V = fP`. The lock `l^2 = 4a^2/(3f)` reproduces the EO tetrahedral Gram (ES13).

**GSGB-1.** A record-controlled common Lorentz holonomy (from ER).

**GSGB-3.** `gamma_IF -> N -> D_R'' -> D_R` (KMS/FDT); a spin-2 pole only under sealed gates (ES17a).

**GSGB-4.** `G-SOLDER` + RIEHB IBP.1-4 -> EH action/Einstein (ES19-20). These are imported conditionals.

The `G-SOLDER` gate is adopted. The disposition admits "physical soldering torsion-free refinement"
is the next step.

**P-37.** It supplies a solder-map template (metric = QFI Hessian x l^2). It has no displacement
sector, no stress coupling, and no dynamics.

### EU -- SCGQA S4 categorical gamma-QFI
Path: PW/LANE_CROSS_RFT_GRA_EU_.../THEOREM.md. Builder: SOURCE_FROZEN_PENDING_INDEPENDENT_HOSTILE_AUDIT;
no audit file in dir.
- Softmax family `p_a = e^{lambda theta_a}/Z` on a 4-level carrier.
- `gamma_Q = gamma_state` exactly (EU09).
- `F = lambda^2 (diag p - pp^T)`, rank 3; `F(0) = (lambda^2/4) P` (EU12-13).
- Product marks give `F_N = N F`; the q4 count is sufficient; `Delta m in A_3`.
- EO Gram lock: `l^2 lambda^2 = 64a^2/3` (EU31), with chart-dependent variants (EU33, EU36).
- Its first variation only spans A1 + T2 (EW §3). It misses E.

**P-37.** None, beyond the template. The isotropic categorical metric has no shear-E.

### EW -- PMMDC pair-memory metric-deformation closure
Path: PW/LANE_CROSS_RFT_GRA_EW_.../THEOREM.md. Audit:
`ACCEPT__CLEAN_EXACT_FINITE_SPATIAL_TANGENT_THEOREM`, verifier 3108/3108.

**PMMDC-1.** SCGQA tangent `delta F = lambda^2 P diag(dp) P` has rank 3, image T2 (EW06-10).

**Family.** `p ~ exp[theta.X + SUM J_ab Y_ab]` with `X = Ps`, `Y_ab = s_a s_b` (EW11-12).
- Global flip: one-port marginals stay 1/2 for all J (EW15).
- `F_theta(J) = Cov_J(X)`, `F_theta(0) = I_V`.

**PMMDC-2.** `dF_theta/dJ_ab |_0 = v_a v_b^T + v_b v_a^T` is a basis of `Sym^2(V)` (EW20-21).
IFT gives local diffeo onto a neighbourhood of `I_V`.

**Mode census.** Edge rep = A1 + E + T2 (EW25-26).

**Edge-quadratic reconstruction.**
- `y_ab = (n_a - n_b)^T q (n_a - n_b)`, det = -2^19, with explicit inverse (EW28-31).
- This is the same "edge-pair -> metric" map as P-31's bond family.

**P-37.**
- The metric candidate is the polarization second moment, a quadratic object.
- The flip-even pair coupling deforms it. No linear polarization is needed.

### GJ(cross) -- PMICS pair-memory intrinsic curvature symbol
Path: PW/LANE_CROSS_RFT_GRA_GJ_Q4_PAIR_MEMORY_INTRINSIC_CURVATURE_SYMBOL_V001/.
Hostile audit: PASS 112/112 at the flat/principal-symbol ceiling.
- Statewise `XX^T = I_V + SUM (v_a (.) v_b) Y_ab` (PMICS00a), so `F(C) = I + SUM C_ab (v_a (.) v_b)`.
- `C = <Y>`; J is control only.
- Riemann symbol `R_anbn = (k^2/2) H_ab` (PMICS05). Rank 3.
- Kernel = pure gradients `k (.) xi` (PMICS08-09): the displacement/gauge sector.
- Quotient = 1 scalar `(3)R = k^2 tr(P dh P)` + 2 tidal (PMICS10-12).
- Physical only under adopted RGRL-B-C. FZ's TT source response is NOT a metric perturbation
  (§7, no substitution).

### GK(cross) -- PMSR pair-memory/source reciprocity
Path: PW/LANE_CROSS_RFT_GRA_GK_.../.
Hostile audit: PASS 209/209 (`INDEPENDENT_HOSTILE_AUDIT/INDEPENDENT_HOSTILE_AUDIT.md`).

**Metric map.** `F = I_V + B C`; `D_C F = B` is an isomorphism (GK07-10).

**Physical solder (conditional).** `GK-S1..S5`: Gibbs `p ~ exp[theta.X - beta H_C(j)]`, FU
completion, and complete DPAR tangent `d_j K_e = -(U_d lambda/2) M_eA` with root-dyad M (GK12-16).
- `D_j F = (beta U_d lambda/2) B G M` (GK17); rank 6 at finite beta (GK18).

**Pair-sector source.** `Q_A = U_d lambda SUM_e M_eA Y_e + q_id I` (GK19). It is quadratic (Y = ZZ).

**Reciprocity.** `d_{j_A} F_mn = (beta/2) d_theta_m d_theta_n <Q_A>` (GK22).

**Thermal spectrum.**
- `g_A1 = 8a(3a^4 + 4a^3 + 1)/D^2`, `g_E = 8/D`, `g_T2 = 8a/D`, with `D = a^4 + 4a + 3`,
  `a = e^{-beta U_d}` (GK28).
- Pure ice gives rank 2, E only (GK29), "matches FV".

**FY.** It has operator custody only. A noncommuting Hessian is BKM, not SLD (§7).

### EX -- SDCP spatial deformation & constraint propagation
Path: PW/LANE_CROSS_RFT_GRA_EX_.../THEOREM.md. Hostile audit: ACCEPT/CLEAN (conditional).
- Premises: Gaussian-normal patch `ds^2 = -dtau^2 + h dx dx` on an already earned metric (P1);
  complete Noether identity, on-shell `nabla_mu E^{mu nu} = 0` (EX04a-05); six fields
  `J_A(tau,x)` with rank `M_Aij = 6` (EX06-07); zero initial `E^{00}, E^{0i}` (EX08).
- Result: `E^ij = 0` (EX09). Then `d_tau(sqrt h E^{0j}) = -2 sqrt h K^j_i E^{0i}` (EX14), and all
  ten components vanish (EX11). The reduced RIEHB injectivity condition is (EX18).
- This is standard GR constraint propagation (imported). Control #3: without EX05, `E^ij = 0`
  says nothing about `E^{0mu}`.

**P-37.** The P-31 rank-6 spatial source satisfies the rank premise. P-37's nonlocal Ward residue
means EX05 fails for that response, so SDCP cannot be invoked.

### GL5ZZF -- H6DRMSB doubled-real metric source / member identifiability
Path: PW/LANE_CROSS_RFT_GRA_GL5ZZF_.../THEOREM.md. Hostile audit:
`CLEAN WITHIN THE MEMBER-IDENTIFIABILITY BOUNDARY` (99/99).

**Source at m = 1.** `Q_eff^(<=6)(1;x)/J_6 = a(x) D_1 + R_1` (ZZF01).
- `a(x) = 8/(63x^6) * (1 - x^2 - (37/12)x^4 - (16247/900)x^6)` (ZZF02).
- `D_1 = Q_pair/U_d` is diagonal (pair, E-type electric).
- `R_1 = Q_ring/J_6` is off-diagonal (differentiated ring, gauge-invariant `B_C` channel).

**Identifiability stop.**
- `H_6 = -J_6 SUM_C B_C` with `J_6 = (63/8) U_d x^6` is the same for x = 2/5 and x = 1/2 at
  fixed `J_6`.
- Yet `Q(2/5) - Q(1/2) = J_6 (3203/168) D_1 != 0` (ZZF03-06).
- So the source-free H6 effective theory does not fix the metric source.

**Remaining construction.**
- Hermitian real quadratures from `Q_29 = Q_1^dagger` (ZZF07-08).
- A complement-copied 360-state doubled candidate (ZZF09). It is prospectively selected, not derived.
- Frobenius dual pairing with off-diagonal factor 2 (ZZF12-13).
- Bulk crossed response `L = -(J_6/2)[a(x) L^D + L^R]` (ZZF15).
- Missing state, projector, boundary and nuisance Schur terms are enumerated.

**P-37.** This is the corpus's explicit two-owner quadratic (electric pair + magnetic ring) metric
source. It shows that the ratio of the two owners is member-dependent.

### ER -- RTHW record tetrahedral holonomy
Path: PW/LANE_CROSS_RFT_GRA_ER_.../THEOREM.md. Builder: SOURCE_FROZEN_PENDING_INDEPENDENT_HOSTILE_AUDIT;
no audit file.
- Quaternion lifts of tetrahedral rotations (234),(134) give Lorentz links `diag(1,R_i)`.
- A record-controlled swap gives `H_K = (142)`, `H_B = I` with identical gate inventory
  (ER11-ER20). Spin-sign loophole closed (ER17).
- The natural constant coframe fails torsion-free (ER22-23, RTHW-4). The connection is not
  Levi-Civita.
- Next step: `H(eps) = I + eps^2[J_1,J_2]` refinement (ER25).

**P-37.** None directly. It is a connection without a metric or stress.

### EI -- RFCD record-front causal diamond
Path: PW/LANE_CROSS_RFT_GRA_EI_.../THEOREM.md. No audit file.
- Front merger gives the count quotient `(u,v)`, causal order `Delta t >= |Delta x|`, 1+1 diamond (EI06).
- `tau^2 = 4(|I| - l - 1)` (EI12).
- For q >= 3, the orthant cone is not linearly equivalent to the Lorentz cone (EI14, RFCD-3).
- BREAK gives exponential fronts `2^n`.

**P-37.** None (causal kinematics only).

### EQ -- BQ4RSW bounded q4 record streams
Path: PW/LANE_CROSS_RFT_GRA_EQ_.../THEOREM.md. No audit file.
- Explicit unitary-dilatable four-stream model. KEEP descends to count fronts `C(d+3,3)`;
  BREAK gives `4^d`.
- S4 covariance. It closes EO's q = 4 merger antecedent within a finite cap (EQ14-18, EQ24).

**P-37.** None (substrate for the A3 tetrahedral contrast used by EU/EW).

### EZ -- RMLB record-mediated localization boundary
Path: PW/LANE_CROSS_RFT_GRA_EZ_.../THEOREM.md; INDEPENDENT_HOSTILE_AUDIT.md present.
- Proved: AURFT/U-DCL + TRL give per-instrument record factorization (EZ01) and per-instrument
  Fisher with DPI (EZ03-04).
- Countermodels:
  - C1: no universal classical query (Z/X incompatibility).
  - C2: noisy record does not saturate QFI (EZ13-14).
  - C3: Fisher `1/(1-x^2)` is not equal to a proper metric `L^2` for any constant `l_F` (EZ15-18).
- Residual law: RLS (Blackwell-sufficient query + FERS naturality) gives `q = l_F^2 F`.

**P-37.** A warning that a Fisher/QFI metric is not the proper metric without an independent solder law.

### FB -- TROV terminal record order-volume bypass
Path: PW/LANE_CROSS_RFT_GRA_FB_.../THEOREM.md; INDEPENDENT_HOSTILE_AUDIT.md present.
- Record-influence arrows give a minimal preorder (TROV-1). Cross-mission union is not acyclic
  or complete (FB04-05).
- HKMM/Malament (imported) fix the conformal class. Physical 4-volume gives `g = f^{1/2} g_0` (FB07).
- RCV law; adopted as RGRL-A (`PW/GRAVITY_RGRL_ADOPTION_V001.md` lines 23-29).

**P-37.** None (kinematic metric; no dynamics, no stress).

### DEVELOPMENT_R_OWNER_ONCE_L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_V001
Paths: PROTOCOL.md, README.md, FREEZE.json, PREPRODUCTION_RUN_RECORD.json.

**Model.** Owner-once prism (#1, a separate model). Support from primitive generators:
`F_e--C_e` admission edges plus 3L transport edges.

**Weights and statistic.**
- Conductance `g = <K_a^2>`.
- Lazy Ollivier-Ricci (alpha = 1/2).
- Predictor `X_e = kappa_actual - kappa_same-q-product`.
- Spearman vs a sealed L8 carrier-TV response, exact 8! null.

**Status.**
- L8 never run: `scientific_status: L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_UNRESOLVED`.
- L4 dev predictor = [0.0554, -0.0182, 0.0442, -0.0077].
- The older L8 formation-order ORC "null" (rho = 0.154) was retyped as uninformative (path graph)
  in `UNT_LADDER_V001.md` lines 150, 229.

**P-37.** None (graph-combinatorial curvature on a different model).

---------------------------------------------------------------------------------------------

## 2. Upstream F/G-lane facts used above (outside partition; RESULT.md read)
- FT `LANE_GRA_FT_F3_Q4_DEGREE_PAIR_GEOMETRIC_STRAIN_BOUNDARY_V001/RESULT.md`:
  - `U_d(d-2)^2 = U_d I + (U_d/2) SUM Z_aZ_b`.
  - FS source rank 4 (A1+T2), E missing.
  - DPAR `(U_d/2) g(|F r_ab|^2/|r_ab|^2) Z_aZ_b`.
  - Exact underdetermination of the source derivative.
  - Direct ice-projected pair = A1+E.
- FU `.../LANE_GRA_FU_F3_Q4_PAIR_RESOLVED_MAXWELL_DPAR_DERIVATION_V001/RESULT.md`:
  - Lumped capacitor gives A1 only.
  - Signed terminal charges `q_a = q* Z_a` with central elastance `V(|F r_ab|)` derive DPAR.
  - Ideal Coulomb `lambda = -1/2`, `U_d = 2 kappa^2 alpha hbar c/(eps_r r_0)`.
  - Requires reservoir-dressed flips (FU09b) and a full grounded kernel.
- FV: THEOREM.md read in full (see §0 item 3).
- FX/FY/FZ: RESULT.md read (see §0 item 5).
- FR: additive edge dyads give rank 4, A1+T2; the E null is exact. Listed as a VALID obstruction
  in the validity audit (§3).
- GB/GD/GJ: momentum/recoil ownership (see §0 item 7).

## 3. Audit-status cross-reference
- `UNT_VALIDITY_AUDIT_V001.md` §3 lists FR and GJ (flip-recoil) among the real exact negatives.
- `UNT_LADDER_V001.md` line 163: "PMICS curvature capacity, PMSR reciprocity (209/209), RIEHB, EX",
  EXACT at stated ceilings.
- RGRL is ADOPT (line 160). RGRL-B is literally "pair-memory controls -> six spatial metric
  variations + EX Ward packet" (`PW/GRAVITY_RGRL_ADOPTION_V001.md` lines 31-39).
- EU, ER, EI, EQ show no independent audit file in their directories.
