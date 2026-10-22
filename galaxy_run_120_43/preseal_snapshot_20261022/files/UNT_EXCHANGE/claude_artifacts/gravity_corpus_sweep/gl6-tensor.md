# Gravity corpus sweep: GL6 BA onward (tensor/pair-source partition). Raw notes

Date: 2026-10-12. Reader: Claude subagent (read-only sweep). No project .py was executed.
Root: `/Users/bgm/Research/Universal Network Theory/program-worktree/` (abbrev. `PW/`).

## 0. Model identity (TOY_SEPARATION)

Every GL6 packet in this partition runs on **F3**: `H = U_d sum_v (k_v-2)^2 - h sum_e X_e` on a simple
4-regular bipartite girth-6 incidence graph (diamond/Q4, A3 parent cells x 4 ports). That is the
incidence+degree sector at **d*=2**, with no Delta edge term, carriers, Records/Bind, feedback, Birth, or admission.
Paths: `PW/LANE_CROSS_RFT_GRA_GL6BA_.../THEOREM.md` (BA01), `PW/LANE_CROSS_RFT_GRA_GL6CH_.../THEOREM.md` (CH01),
`PW/LANE_CROSS_RFT_GRA_GL6CN_.../THEOREM.md` (CN01).
- The validity audit classes this sector as DERIVED_APPROXIMATION, "a different model than the prism"
  (`/Users/bgm/Desktop/FOLDERS/Gravity/20260918 Packet/20260924 Packet Updates/UNT_VALIDITY_AUDIT_V001.md` lines 75-76, 150).
- Its low-energy sector is the same quantum-ice/ring-exchange sector that P-37 uses. The ring amplitude is
  J = (63/8) h^6/U_d^5 (GL6BX BX01, GL6CH CH09).
- So GL6 is **not canonical #7**. It is #7's ice sector with a different, C-even, source law.

## 1. The single most important finding for P-37

GL6 used a **different metric-source operator** from P-31 V002, and that choice removes P-37's linear piezo vertex by construction.

- **GL6 source.** At each degree-4 node it inserts the six-pair source `j_v . M_v` with `M_ab = Z_a Z_b` before the Feshbach step
  (GL6BV BV01/BV04, GL6CJ CJ01, GL6CU CU01-02). This operator is **complement-even** (C-even): it is invariant under Z -> -Z.
- **On the ice manifold** z0 z1 z2 z3 = +1, so M_01=M_23, M_02=M_13 and M_03=M_12. Hence `P_T M_v = 0` (GL6CH CH04, GL6CN CN03).
  The T2 (off-diagonal "shear") source therefore has **zero locked-space vertex**. GL6CG goes further: the bare, h^2 and h^4 T2 first vertices
  are pointwise zero (CG.2b), and GL6CN shows the diagonal h^6 T2 vertex is also zero.
  The only first-order T2 action through h^6 is the ring-exchange writer (GL6CH CH16).
- **P-31 V002 source.** It weights the n-basis degree cross terms `n_a n_b`, and also the edge storage term via exp(n^T j n).
  P-37 eq.(2)/(4) shows that its T2 part is LINEAR in polarization: `-(4Ud/9)(X23 e1+...)`, with total lambda = (2/9)(3Delta-4Ud)
  (`/Users/bgm/Research/UNT_EXCHANGE/lanes/P37_CODEX3/P37_FORMAL_UNIFORM_ENDPOINT_COULOMB_RESPONSE_V001.txt` sec.2).
- **The algebra connecting them (my derivation).** `n_a n_b = (1 - z_a - z_b + z_a z_b)/4`. The T2 combination n_a n_b - n_c n_d therefore equals
  -(z_a+z_b)/2 on ice, which is pure linear polarization. GL6's M_ab is the C-even projection of P-31's dyad.
- **The corpus draws the same line.** GL6CG sec.5 separates the native link T2 density `C_a = z_b - z_c`, which is complement-odd,
  conserved and opens at first spatial order, from pair memory, which is complement-even and has T2 projection zero at every k.
  It states: "No link-continuity or gauge conclusion transfers to the pair source."
  (`PW/LANE_CROSS_RFT_GRA_GL6CG_DENSE_PARENT_GLOBAL_H4_SOURCE_OPERATOR_V001/THEOREM.md` sec.5)
- **d*=2 connection.** At d*=2 the degree penalty is itself pure pair products:
  `sum_{a<b} Z_a Z_b = 2(n-2)^2 - 2` (GL6CL CL33). Equivalently Ud(d-d*)^2 = Ud[(2-d*)^2+1-(2-d*)Sum z + (1/2)Sum_{a<b} z_a z_b].
  The second form is my expansion; the linear-in-z term vanishes at d*=2. This bears on P-37's "d*=2 locus" rescuer.
  P-31's principle of "reweighting the cross terms already in the degree penalty" yields the GL6 source when the cross terms are written in the z basis rather than the n basis.

## 2. Mechanism notes (one block per packet cluster)

### M1. Tetrahedral pair-to-Sym^2 solder

Packets: GL6CR, GL6CO, GL6BQ, GL6CS.
- `D_C(e_ab) = v_a (.) v_b`, with v_a = T_a/2 and T = (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1). It has rank 6.
  It is an exactly S4-equivariant isomorphism: `D_C P_g = rho_sym(R_g) D_C` (GL6CR CR03-CR05).
- Audit form `S(j) = 1/4 sum j_ab (T_a T_b^T + T_b T_a^T)` maps the A1 trace to -I and T2 to minus the off-diagonal entries
  (`PW/AUDIT_G_GL6CO_.../AUDIT_REPORT.md` A-CO04/05).
- Gram: `D^*D = (1/2)P_A + 2P_E + P_T`. The equal-spatial-normalization (isotropy) condition is therefore **h_E/2 = h_T**
  (GL6BQ BQ09-BQ10; GL6CS CS13 + audit).
  My note: this is the cubic Zener-type condition.
- **Status: adopted chart.** The coordinates are an "inherited tetrahedral coordinate embedding ... has not independently derived
  physical distance or spacetime" (GL6CL sec.1; GL6CG sec.7; GL6CQ sec.1). The solder is inherited from the EW/GJ pair-memory lanes
  (outside this partition): `PW/LANE_CROSS_RFT_GRA_EW_Q4_PAIR_MEMORY_METRIC_DEFORMATION_CLOSURE_V001`,
  `PW/LANE_CROSS_RFT_GRA_GJ_Q4_PAIR_MEMORY_INTRINSIC_CURVATURE_SYMBOL_V001`.
- The probe space and the field space are distinct: `j = D_C^* h` (probe) versus `delta C = D_C^{-1} h` (retained field) (GL6CY CY17).

### M2. C-even six-pair source and its locked/diagonal read

Packets: GL6BV, GL6CJ, GL6CL, GL6CG.
- **Locked diagonal read** `D: j -> j.M(s)`. It has rank 3 on A1+E with `D^*D = 4P_A + 16P_E` (CJ07).
- **First-source hierarchy** (CG.2a): `V2 = -M`, `V4 = -(4/9)1 - (37/12)M`.
- **A1 channel.** A uniform A1 source is the same thing as `U_d -> U_d + 2q`.
  The derivative d/dq[-63/8 h^6/(U_d+2q)^5] = 315/4 h^6/U_d^6 equals the sum of the six scalar writer vertices (CL33-CL35).
  This links storage energy (degree stiffness) to the future ring writer, i.e. a trace/"lapse-like" channel.
- **Every ring move is E2.** It changes a nonzero pure-E2 diagonal pair coordinate:
  P_A dM = 0, P_T dM = 0, ||dM||^2 = 16 (GL6CS CS02).

### M3. Strict-lock T2 contact

Packet: GL6BV, with GL6BX.
- Exact h^2 functional F2(j) (BV05). Onsite Hessian `-2h^2/U_d^3 P_T` (BV06). Edge block rank one and state-dependent (BV07).
  Full form `F'' = -(h^2/4U_d^3) A^* A` (BV19).
- The retained gapped response is at 2U_d, so there is **no low-energy T2 pole** (BV08, BV23).
- Translation/S4 parametrization: `C_a = beta P_T + (2/3 - beta) Q_a` with `p = Pr[same partner]` (BV25-BV31).
  The Q4 orbit witness gives p = 109/128 (BV32).
- The contact carries a nonzero k^0 term (8+gamma)P_T. In GL6BX the k=0 energy contacts are (h_A, h_E, h_T) = (-24, -72, -56) r^2/U_d,
  and the CTP assembly does **not** cancel the k^0 contact. "No Ward identity is present." (BX08)

### M4. Global H6 tensor writer

Packets: GL6CH, plus GL6CN and GL6CU.
- 720-history enumeration: source-free sum -63/8.
- Canonical gradient `(105/8)e_ab`; its T2 projection is `(105/16)Theta_{v,c}`, with Theta = e_ab - e_cd (CH09-CH12).
- Global operator (CH16): `[H_eff(j_T)]_off^(6) = -(63/8)h^6/U_d^5 sum_c T_c + (105/16)h^6/U_d^6 sum_c T_c sum_{v in c} j_v . Theta_{v,c}`.
- **Orientation tetrahedron**: u_d = 2(1,1,-1), ..., with `sum_d u_d u_d^T = 32 P_T` (CH19).
- GL6CN closes the complete pure-T2 first vertex through h^6 as this writer alone (no diagonal h^6 T2 potential).
  GL6CU V002 gives the full raw source jet (first plus mixed second derivatives) through h^6, audited PASS.
- **My crosswalk (not a corpus claim).** The hexagon whose missing port is d has its plane normal along T_d,
  and `u_d = -2 offdiag(T_d T_d^T)`, checked for d=0 and d=3.
  Since T_c ~ cos(curl a) ~ 1 - B_d^2/2, the T2 writer couples j_ij to roughly B_i B_j (off-diagonal),
  while the E2 locked read couples to e_i^2 - e^2/3 (diagonal electric).
  So GL6 realizes a split Maxwell-stress-like coupling: E2 is electric and diagonal, T2 is magnetic and off-diagonal.
  The corpus never names it "Maxwell stress": a grep of the partition for maxwell/stress/photon finds no such identification.

### M5. Faithful six-direction access and Fourier writer

Packets: GL6CJ, GL6CL.
- Combined map: `C^*C = 4P_A + 16P_E + 8P_T`, rank 6, with explicit inverse (CJ17-CJ18).
- Fourier rows `B_d^+(k) = 2 sum cos(k.rho)e_p^T`. The rank is preserved for `|k|^4 < 32/363` (CL20).
- Common T2 normal (CL23): `N_T(k) = 8I - 2|k|^2 I + 12kk^T - 28 diag(k^2) + O(k^4)`. This is cubic and not isotropic by itself.
- Relative parent/child sector:
  - B_-(0) = 0, and the rank drops to 2 on the face diagonals.
  - With independent parent and child fields the map has rank at most 10 of 12, so it needs a "physical common-field/soldering law".
- At the Brillouin-zone boundary q = (pi,0,0) the writer has rank 1 (CL31-CL32).

### M6. Overlap stationary writer response

Packets: GL6CK, GL6CM.
- An isolated ring has E'' = 0: the writer commutes with the Hamiltonian.
- A two-overlap star gives `-E'' = sqrt2/(4J) (w0-w1)^2`. The literal value is `175 sqrt2/32 h^6/U_d^7` (CK.10, CK.14).
- Bilinear form `K_spec = 2 lambda_T^2 Re<B_j R B_k>`. It is positive semidefinite and reciprocal, with the common-rescaling null K1 = 0 (CM07-CM12).
- Legendre transform: `Gamma'' = K^{-1}`. The resulting "stiffness" is derived, not imported (CM18-CM19).

### M7. Cycle-response tensor matching and moment sum rules

Packets: GL6CO (read closely), GL6CQ.
- **Invariant symbol.** The cycle symbol (CO06) has one constant κ and five quadratic coefficients: α, η, b, c, d.
- **Pullback.** It is CO11-12: `8κI + (-2κ+8b)r^2 I + (-16κ+8c)D + (12κ+8d)O`.
- **SO(3) tensor extension.** It holds iff `c + d = κ/2` (CO17).
- **Fierz-Pauli reference shape.** Matching it additionally requires `b = κ/4` (CO21).
- **Full-solder kill test.** It has rank 3 and nonzero A1/E2-T2 cross blocks at k = (2,3,5) (CO23).
  T2 alone cannot close a Ricci claim.
- **Contact mismatch.** It is `Delta_ct = (8/3)(2p-1)` (CO27).
- **Same-state test.** It is (CO29).
- **Power counting.** The cycle block scales as h^6/U_d^7 and the contact as h^2/U_d^3, so isolated strong lock cannot match.
  A finite-ratio or collective regime is needed (CO31).
- **GL6CQ coefficients.** Each coefficient is a measurable moment of the connected Euclidean ring-ring correlator.
  κ = Z_T/3, b = -M_perp/12, and so on (CQ14-CQ17).
  The sum rules are CQ26/CQ28.
- **Critical caveat (sec.7).** If the second moment diverges, the analytic k^2 test fails and "the nonanalytic leading kernel must be measured directly".
  - My note, an inference: in a Coulomb phase the ring operator's fluctuation is about quadratic in the photon.
  - The two-photon static correlator should decay roughly as r^-7.
  - Its second moment would then converge and the analytic k^2 coefficients would exist. That is unlike P-37's linear chi_lin, which is degree 0 and nonlocal.

### M8. Rotational completion and Ward-null classifier

Packet: GL6CR.
- The response space has dimension 9 under cubic symmetry, 4 under rotations, and 1 after the Ward relations (CR20).
- The direct Ward null `K D_C^{-1}(k(.)xi) = 0` has a rank-8 constraint matrix and a unique Einstein/Fierz-Pauli ray (CR22-CR25).
- This is a **target classifier**. The validity audit says: "The 'From below' Ward route is Fierz-Pauli uniqueness, with no record information."
  The packet itself agrees: "Imposing (CR22) by hand would merely insert the desired answer."
- P-37 already uses this CR family as its membership test (P-37 sec.5).

### M9. Displacement/reembedding sector

Packets: GL6CY target, GL6CY development, and its audit.
- **Kinematics.** Displacement field eta on the A3 cells and literal ports: `p_a = v_a + [eta(x+T_a) - eta(x)]/2`, `e_a = F v_a`.
  The affine coframe is F = I + A (from GL6CX V002). The center offset is `d = (1/8) sum_y [eta(y) - eta(x)]`, a discrete Laplacian (CY04-CY08).
- **Relational source.** `eta^phys_ab(F,d) = I:E_ab - g^{-1}:(p^_a (.) p^_b) = -2 rho.(v_a+v_b) - 2|rho|^2`, with g = F F^T (CY10).
  - It is identically zero for centered (pure-affine) ports.
  - Its first jet is pure T2, `-2 b_r.(v_a+v_b)` (CY13/CY15).
  - Its second jet has an A1 piece (CY14).
- **Raw composition.** `R^raw = H_,AB eta_A,s eta_B,r + H_,A eta_A,sr`, evaluated at k=0 on the Q4 regulator:
  `H4 = (32128/27) S`, `H6 diag+cyc = (7212448/6075) S`, which is nonzero.
  Sources: `PW/GL6CY_DEVELOPMENT_CU_V002_RAW_SOURCE_COMPOSITION/ADDENDUM.md`; audit `PW/AUDIT_G_GL6CY_RAW_SOURCE_COMPOSITION_V001/INDEPENDENT_RESULT.json` (PASS, 983 checks).
- The owner schema marks positions, support, GD recoil, state, quotient and "retained_field_shell (incl. 'Maxwell sector')" as UNDEFINED.
  It says: "Current F3 does not yet authenticate those positions as its physical support variables." (TARGET.md sec.2; OWNER_SCHEMA.json)
- **Cross-reference outside this partition.** The GD auxiliary mechanical torus owns flip recoil (`PW/LANE_GRA_GD_F3_Q4_TRANSLATION_OWNING_RECOIL_PARENT_V001/RESULT.md`).
  GJ shows that the bare GD momentum density does not close the supplied-embedding Ward test (`PW/LANE_GRA_GJ_F3_Q4_FLIP_RECOIL_EMBEDDING_WARD_OBSTRUCTION_V001/RESULT.md`).

### M10. Obstructions

**Scale separation (GL6CS).**
- `K_EE : K_ET : K_TT^ct : K_TT^wr ~ r^-6 : r^0 : r^2 : r^6` (CS12).
- h_E/2 = h_T fails on any fixed component. Matching needs a contact enhancement of r^-8, a writer enhancement of r^-12, orientation accumulation, finite r, or a new block.
- Audit: PASS. The ladder misreported this as a scale limit (validity audit V001 line 76).

**Single-collar no-tuning (GL6BX).**
- The contact defect `D_ct(r) = r^2[-2 + (409/27)r^2 - (2146938851/729000) r^4] < 0` for every r > 0 (BX04).
- The truncated stationary surrogate D_6(r) < 0 by a Sturm test (BX33).

**Orientation (GL6BQ).**
- S4 is not a spherical design: the 4th moment is 1/3 versus Haar 1/5, and the 6th is 1/3 versus 1/7.
- Isotropy needs a degree-6 SO(3) design over physical coframe orientations. The parent does not supply one, and inserting it would be a new law (BQ06, BQ13, BQ15).
- The Ricci-ray residual survives the joint S4 orbit average (BQ05). That fact comes from GL6BO, outside this partition.

**Orientation accumulation (GL6CP).**
- The audit is REPAIR_REQUIRED: its raw coordinate moments are not functions on SO(3)/Gamma (`PW/AUDIT_G_GL6CP_.../AUDIT_REPORT.md`).
- The representation-theory core survives: the Haar projection of the 9-dimensional cubic space has rank 4.

### M11. Records and the reciprocal future writer

Packets: GL6BA, GL6BB, GL6BC.
- **GL6BA.** A Lieb-Robinson collar for full F3 at any finite R = U_d/h, so R = 2 and R = 5/2 are computable directly.
  Bound: `D_TV <= (3L^2+3L+1) T_{2L+1}(48 R |sigma|)`.
- **GL6BB.** The selected-mission inputs (R, sigma, omega_L) are unselected. Prepared-blank Dicke bound: `q_0 >= 1 - 1/(3R)`.
- **GL6BC.** Retained support-word projectors commute with F3 and with every pair source/read operation, so the reciprocal retarded response is exactly zero.
  The missing law is a same-parent future writer, `B_{A->K_new} = d/dj Pr_{W_j}(Q_new = 1)` (BC21).
- The validity audit lists GL6BC as a real obstruction (V001 line 36).
- GL6CH then supplies the first candidate-field-dependent writer. In the corpus's own words it is "not yet a self-generated record field".

### M12. Numerical full-response harness

Packet: GL6FJ.
- The full response of 24 real channels (300 rays) at L=4, m = (0,0,1), with six owners: stay/writer contact, stay/writer spectral, interference, disconnected.
- Result-level audit PASS. The eigenvalue interval is [3.3147, 177.5396] and the anomalous/normal ratio is 0.0569.
- No quotient, no Ward rank and no Einstein claim are made. The design pairs m001 with m123 (GL6FE, outside the partition) to keep the GL6CR rank-8 screen.
- Sources: `PW/AUDIT_G_GL6FJ_M001_RESULT_V001/AUDIT_REPORT.md`, `PW/RESULT_G_GL6FJ_M001_FULL_CU_C64_RESPONSE_V003/FULL_RESPONSE_RECONSTRUCTION.json`.

## 3. Bottom line for P-37 (my synthesis; inferences marked)

1. **Rescuer (b), the gauge-invariant quadratic stress-like channel, is already built at operator level, audited, on the same ice sector.**
   It is the C-even pair source M = ZZ:
   - E2: locked diagonal, quadratic electric.
   - T2: the H6 ring writer (plaquette/magnetic) plus the gapped h^2 contact.
   - A1: the U_d modulation.
   It removes P-37's linear T2 piezo vertex by construction (P M_T P = 0). Porting it to #7 means **declaring a different source law**
   (the C-even projection of P-31's dyads), which requires principal sign-off. The edge-storage exp(n^T j n) linear term must also be dropped or projected.
2. **The program already found what happens next.** The response is then analytic (CO/CQ). Three things block gravity:
   - (i) a nonzero k^0 local susceptibility (κ and contact): the BX k^0 contact is not cancelled.
     Inference: in induced-gravity language this is the one-point/tadpole term a Ward identity must tie to <T>.
   - (ii) E2/T2 scale separation r^-6 versus r^6 on fixed components (CS), and single-collar no-tuning (BX).
   - (iii) no derived longitudinal null. This needs a displacement field xi with h -> h + k(.)xi. The corpus states it as the GL6CR/GL6CY target,
     but no authenticated position variable exists, which is the same "lawful metric solder map" gap P-37 names.
3. **Inference.** The single-vertex split puts E2 and T2 in different microscopic channels with scales about r^-12 apart.
   A coarse Maxwell-stress coupling would get its off-diagonal electric part from **inter-vertex** correlations, which M_v cannot see.
   GL6CS's "another same-order block" slot is where such a two-vertex (edge-shared) C-even source would enter.
   This is not computed anywhere in this partition.
