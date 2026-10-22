# Gravity-corpus sweep — partition GL6AN..GL6AZ (locked / quantum-ice block)

Raw notes. Read-only sweep, 2026-10-12. Every claim below cites a file. Paths
are abbreviated as follows:

- `PW` = `/Users/bgm/Research/Universal Network Theory/program-worktree`
- `P37` = `/Users/bgm/Research/UNT_EXCHANGE/lanes/P37_CODEX3`
- `VA` = `/Users/bgm/Desktop/FOLDERS/Gravity/20260918 Packet/20260924 Packet Updates`

Lane dirs are `PW/LANE_CROSS_RFT_GRA_GL6xx_*_V001/` (author) and
`PW/AUDIT_G_GL6xx_*_V001/` (distinct hostile audit). All 13 audits PASS.
GL6AY's first audit FAILED (global-projector scope) and was repaired; the
post-repair audit PASSES (`PW/AUDIT_G_GL6AY_..._POST_REPAIR_V001/AUDIT.md`).

Validity-audit standing: the whole block is construction #3, "F3/GL6
degree-locked incidence (TFIM) sector on a supplied q4 diamond":
DERIVED_APPROXIMATION of the canonical model (`VA/UNT_VALIDITY_AUDIT_V001.md`,
crosswalk table row 3). GL6AQ is listed among the "real negatives"
(`VA/UNT_VALIDITY_AUDIT_V001.md` §3). No GR content in this block was flagged as
imported, and it does not cite WTC, RGRL, Fierz-Pauli or AQUAL as inputs.
Every packet carries an explicit "no gravity / no G" ceiling.

---------------------------------------------------------------------------

## 0. Bottom line for P-37

This block already holds three things P-37 needs. None of them re-imports GR.

1. **The structural root of the piezo obstruction is already derived.** In the
   strict degree-two lock, one node's pair observables have A1 fixed, E
   fluctuating, and T2 **identically zero** (GL6AN AN18; GL6AS §8). A
   one-node quadratic T2 (shear) source therefore does not exist. Any one-node
   shear source must be linear in the local polarization or vanish.
   P-37 eq (2) finds exactly this for the P-31 angle dyad:
   `2Ud A_ab:X = (Ud/3)sum_i Xii(e_i^2-4/3) - (4Ud/9)(X23 e1+X13 e2+X12 e3)`.
   The E part is quadratic and the T2 part is linear
   (`P37/P37_FORMAL_UNIFORM_ENDPOINT_COULOMB_RESPONSE_V001.txt` §2).
   Same fact, two lanes.

2. **The symmetry that separates "piezo" from "stress" is already in the
   corpus.** The complement automorphism `C: n_e -> 1-n_e` (so `e -> -e`) is
   exact on the homogeneous degree-four lock (GL6AN AN13; GL6AS AS08). Pair
   reads `M_ab=Z_aZ_b` and ring toggles are C-even. A C-even source has
   **zero one-T2 (one-photon, linear-polarization) matrix element** in a
   C-parity state (GL6AS AS22). Its leading channel is the two-mode continuum
   (AS23–AS25).
   - My check on P-37 eq (1)–(4): the shear vertex
     `lambda(j23 e1+...)` is exactly the C-odd part of the adopted edge and
     angle dyads. Complement maps the occupied pair (a,b) to the vacant pair
     (c,d) and sends `e -> -e`. `A_ab,ii ~ e_i^2` is even and
     `A_ab,ij ~ -e_k/9` is odd.
   - For the edge dyad (P-37 eq 3), the vacant-link sum gives
     `(2/3)trX - (2/3)sum X_ij e_k`. The occupied/vacant average is therefore
     pure trace `(2/3)trX`.
   - So C-symmetrizing the adopted dyads (occupied-pair plus vacant-pair
     average) removes the linear piezo vertex identically. What survives is
     only the quadratic E part, which is GL6AQ/AS's pair-E read.
   - The cost: one-node T2 shear then has no source at all.
   - P-37's fine-tuned locus `Delta=4Ud/3` (register §5) is a codimension-one
     accident with no protecting symmetry. C on the **source** is the
     corpus-native candidate for a protecting symmetry.
   - This is an observation, not an adopted source law.

3. **A gauge-invariant, C-even, quadratic channel for exactly the missing
   shear directions is already derived as a typed atlas** (GL6AV).
   - Mechanism: modulate the hexagon (ring-exchange) coefficient by
     orientation, `J_d = J prod_{a!=d} kappa_a^2`.
   - Its log-chart is the tetrahedral evaluation `t_d^T S t_d` of a symmetric
     tensor. That evaluation has rank 4, image A1+T2, and kernel E.
   - The authenticated pair-E coordinate is the E-irrep complement, so
     `(A1+T2)_hex ⊕ E_pair ≅ Sym^2(R^3)` (AV13–AV18).
   - My reading (not GL6AV's wording):
     - The ring term is the magnetic `K_b (curl a)^2` piece of P-37's
       Gaussian theory. An orientation-d hexagon has mean normal `t_d`, so
       `delta H ~ sum_d delta J_d (B.t_d)^2 = B^T [sum_d delta J_d t_d t_d^T] B`.
       That is an A1+T2 deformation of the magnetic stiffness tensor.
     - The pair-E read is the traceless-diagonal part of the local
       electric-field square. In the lock, `p_1 = M12+M34 = E_x^2 - 2` (my
       algebra from GL6AN AN15 / AP13).
     - So GL6AV assembles a Maxwell-stress-like coupling: B⊗B in A1+T2 plus
       E⊗E in E.
     - It is **not** a consistent stress tensor. The E part of B⊗B is
       invisible to orientation couplings, and the T2 part of E⊗E vanishes at
       one node. GL6AV's AV-CONTINUUM premise (single quadratic cone, no
       Fresnel/birefringent characteristic) is exactly the condition that
       E-side and B-side deformations agree.
     - This matches P-37's register §4: "A Maxwell stress construction needs
       consistently normalized E and B bilinears".

Also present in this block:

- An exact **lapse/clock** law, `H(q)=q^6 H(1)` (GL6AV AV02–AV08, AV19).
- The finding that **records couple only gauge-invariantly** at leading
  order: zero linear projection, entry only through the six-fold ring product
  (GL6AQ AQ11–AQ16).
- **No displacement/elastic sector anywhere in the partition.** This is
  consistent with P-37's "NO EXPLICIT MICROSCOPIC DISPLACEMENT OWNER"
  (`P37/P37_TO0075_CORRECTIONS_AND_SUCCESSOR_REGISTER_V001.txt` §3).

---------------------------------------------------------------------------

## 1. GL6AN — native degree-lock sector theorem

Files: `PW/LANE_CROSS_RFT_GRA_GL6AN_NATIVE_DEGREE_LOCK_SECTOR_THEOREM_V001/THEOREM.md`
and `RESULT.md`, plus
`PW/AUDIT_G_GL6AN_NATIVE_DEGREE_LOCK_SECTOR_THEOREM_V001/AUDIT.md` (PASS).

**Model.** F3 on the A3 parent/shared-child incidence. This is the diamond
graph (GL6AT AT03).
`H=-h sum X + eps* sum n + 2Ud sum_pairs n n`, with
`eps* = Delta + 2Ud(1-2d*)` inherited.

**Lock identity (AN06–AN08).**
- On `eps*=-6Ud`, `H_lock=-h sum_e X_e + Ud sum_v (k_v-2)^2 + C'`.
- The strict domain is `Delta=4Ud(d*-2)>0`, which needs `d*>2`. The witness
  is `d*=3, Delta=4Ud`, which is the V006 canonical photon block
  (`VA/FIRST_CHUNK_PREMISE_CARD_V006.md` lines 248, 266).
- `d*=2` is the `Delta=0` boundary.

**Linear Ward no-go (AN10–AN12).**
- `[H,q_v]=-ih sum_{e∋v} Y_e`.
- No nontrivial linear degree charge is conserved at finite h, so there is no
  degree-continuity Ward identity from the lock.

**Complement symmetry (AN13).**
- `C(Z_e)=-Z_e`, `C(q_v)=-q_v`. The infinite homogeneous degree-four
  interaction is invariant.
- It is a discrete Z2, not a Ward identity. It fails at open boundaries.

**Local filter (AN14–AN20).**
- Within `q_v=0`: A1 fixed, E fluctuates (the 2D kernel of `K4`'s
  vertex/pair incidence R), T2 = 0.
- Uniform covariance `(C_A1,C_E,C_T2)=(0,8/3,0)`.
- This is the fact that makes one-node shear linear-only (see §0).

**Incidence flat directions (AN21–AN25).**
- `lambda_± = 4 ± |s|`. There are two exact flat directions at a generic
  character.
- One Gram eigenvalue is quadratically soft: `4-|s| = (1/2)sum theta_a^2`.
- Static only; not a dispersion.

**Hexagon (AN26–AN31).**
- On Q4 (girth >= 6, M=256): H2 and H4 are scalars.
- The first off-diagonal term is an alternating hexagon, `-(63/8)h^6/Ud^5`.

**Bearing.** Supplies the lock and C-symmetry, which is P-37's background
manifold. It shows the lock gives no Ward law and gives the one-node T2 = 0
fact. No metric map. No displacement.

## 2. GL6AO — complete sixth-order locked Hamiltonian

Files: `PW/LANE_CROSS_RFT_GRA_GL6AO_COMPLETE_SIXTH_ORDER_LOCKED_HAMILTONIAN_V001/THEOREM.md`
(AO.1–AO.7), plus audit PASS.

- `H_eff = CP -(M/2)h^2/Ud P -(7M/24)h^4/Ud^3 P -(h^6/Ud^5)[(893M/1080)P + (63/8) sum_c T_c] + O(h^8)`.
- No configuration-dependent diagonal term at order six, so `v/g=0` (GL6AT).
- Formal infinite interaction: `Phi_c = -(63/8)(h^6/Ud^5) tau_c`, with
  `tau_c = P_c(prod X)P_c` on an 18-link collar.

**Bearing.**
- This is the microscopic origin of P-37's `K_b` and `U_e ~ h^6` "ring-driven"
  stiffnesses (P-37 §4 states that scaling as a hypothesis).
- The canonical V006 card uses `J6=(63/8)h^6/Ud^5` as its EST
  (`VA/FIRST_CHUNK_PREMISE_CARD_V006.md` line 304).
- Caveat: the same card notes a `J4=(5/2)h^4/Ud^3` 4-cycle census on the Born
  graph (line 305). GL6AO's girth-six premise does not hold there.

## 3. GL6AP — locked IR conditional response; E-pole no-go

Files: `PW/LANE_CROSS_RFT_GRA_GL6AP_LOCKED_IR_CONDITIONAL_RESPONSE_V001/THEOREM.md`
(AP01–AP35), plus audit PASS.

- The locked link tangent at the trivial character is T2
  (`Pi_K(1)=I-11^T/4`, AP09). It is rank 2 at a generic character: the two
  transverse polarizations (AP07, AP11).
- Pair fluctuations are E. `dim Hom_S4(T2,E)=0` (AP15), so link softness does
  not imply pair-E softness (AP16).
- The native hexagon changes pair-E type counts `(1,2,3) -> (3,2,1)`
  (AP17–AP19). No uniform pair-E combination is conserved at sixth order.
- Most general reciprocal analytic inverse E response:
  `Gamma_E = [a0 + c0 I2(theta)]I + c2 T(Q_E(theta)) + O(theta^4)` (AP26).
  The E mass `r_E` is allowed, and an E cubic invariant is allowed (AP28).
- Physical momentum needs an embedding `X: A3 -> R^3`, calibration,
  refinement and a selected phase (§7).

**Bearing.**
- For a stress-like E channel the corpus already proved there is no
  native Ward/charge protecting it, and a mass is symmetry-allowed.
- A Ward identity in the quadratic channel must come from elsewhere (gauge
  completion or a new constraint).
- This sharpens P-37's "Ward residue" issue.

## 4. GL6AQ — authenticated E source; retained-K loop-selection obstruction

Files: `PW/LANE_CROSS_RFT_GRA_GL6AQ_AUTHENTICATED_E_LOOP_SELECTION_OBSTRUCTION_V001/THEOREM.md`
(AQ01–AQ18), plus audit PASS (no author SEAL by design).

- Pair read `O_x(c)=sum c_ab Z_a Z_b`, `c ∈ ker R = E`. Its locked overlap is
  `(1/6)sum (c^T M)^2 = (8/3)c^T c`: a nonzero local E access (AQ05–AQ06).
- The record (retained-K) source is
  `V_kappa = h sum_{e∈D}(1-kappa_e)X_e`, i.e. records gate the **transverse**
  amplitude (AQ10).
  - `P X_e P = 0`: zero direct locked projection (AQ11).
  - `tr0(O_x(c)X_e)=0` (AQ12).
  - One-cell S4 kernel: `P_E K = 0`, because the four port sources are A1+T2
    (AQ13).
- First coupling, at order six:
  `<f|H_eff^(6)(kappa)|i> = -(63/8)(h^6/Ud^5) prod_{e∈C} kappa_e`, and it
  changes local E with `||dM||^2=16` (AQ14–AQ16).
- The product-trace state has positive E correlation mass but zero retarded
  response, which refutes any **universal** nonzero stationary contrast
  (AQ17). Existence for a selected state stays open.

**Bearing.**
- A record source written on the transverse/flip amplitude is automatically
  non-piezoelectric at leading order. It enters only through the
  gauge-invariant ring product.
- That is the opposite of the P-31 edge/angle dyads, which are written on
  occupation bits and so carry a C-odd linear-e piece.

## 5. GL6AR — locked hexagon thermodynamic sector

Files: `PW/LANE_CROSS_RFT_GRA_GL6AR_LOCKED_HEXAGON_THERMODYNAMIC_SECTOR_V001/THEOREM.md`
(AR.1–AR.31), plus audit PASS.

- Native divergence-free signed occupation:
  `sum_i [s_(x,i)-s_(x-e_i,i)]=0` (AR.12). This is the emergent Gauss law
  derived from the lock, "no external redundancy principle".
- Three conserved coordinate cut fluxes, plus a dependent fourth (AR.14–AR.15).
- Perron–Frobenius structure: `H_C=-tA_C`.
- Variational gap bound `Delta_L <= 18t||w||^2 L/Var(F_L)` (AR.27).
- Finite-size and GNS bridges are open.

**Bearing.** The emergent U(1) electric field is native and derived here.
No metric.

## 6. GL6AS — native hexagon collective response and composite channel

Files: `PW/LANE_CROSS_RFT_GRA_GL6AS_NATIVE_HEXAGON_COLLECTIVE_RESPONSE_V001/THEOREM.md`
(AS01–AS33), plus audit PASS.

**Conservation and continuity.**
- The centered four-port T2 density is conserved by the pure hexagon
  (AS06–AS07).
- Cycle symbol `C^{abc}`, with `im C(chi) = ker B(chi)` (AS09–AS10).
- `C1 C1^T = 4[I2(theta)P_T - theta theta^T]` (AS11).
- Continuity `e_dot(chi) = C(chi) I(chi)` (AS13). This is an electric
  continuity derived without any gauge variable.

**Oscillator strength and harmonic modes.**
- `f_u = 2J t_hex I2(theta)` (AS15). The single-mode bound needs `S^+`
  (AS16).
- Conditional harmonic: `omega^2 = eig[C G0 C^† K0]` (AS18). Isotropic case:
  `omega_{1,2}^2 = 4g kappa I2(theta)` (AS19).
- GL6AO supplies neither `kappa` nor `g`, so no dispersion is earned.

**Pair read is quadratic.**
- `O_x(c) = 4 sum c_ab e_a e_b` (AS20): the authenticated E read is exactly
  the quadratic composite of the native field.
- Complement-even. One-T2 overlap is zero in a C-parity state (AS22).
- Two-mode E continuum form factor (AS23–AS24).
- `Sym^2(T2) = A1+E+T2` (AS25).

**Retained-loop source.**
- `delta J_d/J = 2 sum_{a!=d} r_a` (AS29). Eigenvalues: A1 = 6, T2 = -2,
  no E.
- Zero-character E cross kernel is zero (AS30). The small-character E cross
  `alpha P_E(theta ⊙ l_T2) + beta Q_E(theta) l_A1` is symmetry-allowed
  (AS31).

**Composite tensor test (§8).**
- `Sym^2_0(T2) = E ⊕ T2` is algebraically a traceless symmetric tensor.
- The one-node read supplies only E. "In the strict degree-two node, the
  local pair T2 part vanishes identically and the A1 part is fixed. A nonzero
  composite T2 requires a bilocal, derivative, or coarse-grained product not
  authenticated by that one-node read."
- No pole, rotations, stress Ward or gravity.

**Bearing.**
- This is the most direct pre-existing analysis of P-37's "quadratic
  stress-like channel".
- It already proves:
  - (i) the quadratic channel does not couple to one photon under C;
  - (ii) its T2 (shear) part needs multi-node operators;
  - (iii) its E part is a two-photon continuum, not a pole.

## 7. GL6AT — primary quantum-ice crosswalk

Files: `PW/LANE_CROSS_RFT_GRA_GL6AT_PRIMARY_QUANTUM_ICE_CROSSWALK_V001/RESULT.md`
and `EVIDENCE_LADDER.md`, plus audit PASS.

**Exact operator map.** The A3 incidence is the diamond net under the
optional embedding `t_a = e_a - 1/4·1` (AT03). The physical length is "an
extra calibration". GL6AO's operator is the fully-packed-loop quantum ice at
`v/g = 0` (AT08).

**Literature.** Benton et al. give `c = (0.6±0.1) g a0/ħ` (AT09). This is
effective/QMC-calibrated, Level D.

**Fu et al. Raman.**
- The bilinear `E_mu E_nu` creates two photons in the T2g channel built from
  complementary-pair differences `R01-R23` etc. (AT11). The sealed pair-E is
  complementary-pair sums (AT12).
- My note: in the strict lock, complementary pairs have equal `M_ab`, so
  those T2g differences vanish identically at one node (consistent with
  GL6AN AN18).

**Hermele et al.** Loop kinetic-energy density correlations fall as
`1/R^8`: a composite-field mechanism.

**Bearing.**
- Supplies the embedding only as a declared calibration. Nothing dynamical.
- The literature's tensor-bilinear Raman channel is the standard
  "E⊗E couples to two photons" result. It is consistent with GL6AS.

## 8. GL6AU / GL6AW / GL6AX — phase closure and port conservation

Files:
- `PW/LANE_CROSS_RFT_GRA_GL6AU_VG0_STATIC_STRUCTURE_PHASE_CLOSURE_V001/THEOREM.md`
  (AU.10–AU.19)
- `.../GL6AW_ANISOTROPIC_FOLNER_TWIST_CLOSURE_V001/THEOREM.md` (AW.14–AW.17)
- `.../GL6AX_ALL_FIXED_ORDER_TWIST_STABILITY_V001/THEOREM.md` (AX.4–AX.24)
- all audits PASS

**GL6AU.**
- `Delta_C(L) <= 6J sin^2(pi/L)/S_T(2pi/L)`. Any static exponent `alpha < 2`
  closes the gap. The Coulomb case `alpha = 1` gives `O(J/L)`.
- `ICE0-STATIC` and `ICE0-GNS-BRIDGE` are named hypotheses. They are not
  theorems.

**GL6AW.** Anisotropic Følner unconditional dichotomy:
`Delta_C <= 4pi^2 J A_perp/L_par`.

**GL6AX.**
- Affine-moment lemma: `sum_a Delta N_a = 0` and `sum_a d_a Delta N_a = 0`.
  With the affinely independent columns `(1, d_a)`, this gives
  `Delta N_a = 0`.
- Exception: winding, with threshold `2L_min`.
- Twist stability holds at all fixed orders.

**Bearing.**
- P-37's "conditional Gaussian Coulomb phase" premise rests on `ICE0-STATIC`
  plus the GNS bridge. Here those are scientific evidence, not proof.
- The native port displacements `d_a` are combinatorial lattice data, not a
  dynamical displacement field.
- No elastic sector.

## 9. GL6AY / GL6AZ — prethermal finite-coupling bridge and its domain

Files:
- `PW/LANE_CROSS_RFT_GRA_GL6AY_FINITE_COUPLING_PRETHERMAL_LOCKED_BRIDGE_V001/RESULT.md`
- `PW/AUDIT_G_GL6AY_..._POST_REPAIR_V001/AUDIT.md` (PASS after repair)
- `PW/LANE_CROSS_RFT_GRA_GL6AZ_RECORD_AUTHENTICATED_PRETHERMAL_MISSION_IDENTIFIABILITY_V001/RESULT.md`
  and `IDENTIFIABILITY_LEDGER.json`

**GL6AY.**
- ADHH / Else et al. normal form `Y H Y* = Ud N_def + D_hat + V_hat`, with
  `||V_hat|| <= (2/3)^{n*}||V0||`.
- Local-collar locked interaction `Phi_S = P_S^0 D_hat(S) P_S^0`.
- Finite horizon `t <= exp(r1 n*)`.
- Whole-band Schrieffer–Wolff radius shrinks with volume.

**GL6AZ proof-domain floors.**
- `R = Ud/h >= 36 pi e ≈ 307`: first smallness.
- `>= 432 pi e^2 ≈ 10028`: scale separation.
- `>= 1.87e7`: complete universal floor.
- The admitted `h/Ud = 2/5` and `1/2` fail. This is "theorem-domain failure,
  not physical-phase failure".

**Bearing.**
- The canonical V006 member has `h/Ud = 1/5` (`VA/FIRST_CHUNK_PREMISE_CARD_V006.md`
  line 303), so `R = 5`. That is far outside the licensed domain.
- So the ice-manifold reduction underlying P-37 is a DERIVED_APPROXIMATION
  at the canonical tuple, not a rigorous prethermal statement.

## 10. GL6AV — record-conditioned collective metric bridge (read closely)

Files:
- `PW/LANE_CROSS_RFT_GRA_GL6AV_RECORD_CONDITIONED_COLLECTIVE_METRIC_BRIDGE_V001/THEOREM.md`
  (AV01–AV21), `RESULT.md`, `SELF_AUDIT.md`
- `PW/AUDIT_G_GL6AV_RECORD_CONDITIONED_COLLECTIVE_METRIC_BRIDGE_V001/AUDIT.md`:
  PASS, "EXACT_PURE_LOOP_CLOCK_AND_TYPED_ATLAS__OPERATIONAL_METRIC_STRICTLY_CONDITIONAL"

**A. Record → ring coefficient (exact, leading order).**
- `H_hex(kappa) = -J sum_c (prod_{e∈c} kappa_e) tau_c`, with
  `J = (63/8)h^6/Ud^5` (AV01).
- Boolean AND for binary kappa. Fractional kappa is only a multilinear
  extension.
- Lower-order diagonal shifts for nonuniform kappa are **not** classified
  (§1).

**B. Collective clock (exact for the pure loop).**
- `H(q) = q^6 H(1)` and `alpha_t^(q) = alpha_{q^6 t}^(1)` (AV02–AV03).
- `chi^(q)(omega) = q^-6 chi^(1)(omega/q^6)` (AV07).
- Time-dependent `q(t)` gives only reparametrization by `∫q^6` (AV07a–b).
- Conditional `v_q = q^6 v_1` (AV08), and
  `ds_q^2 = -q^12 v1^2 dt^2 + h_ij dx dx` (AV19).
- This is a derived **lapse/g00-type** channel. GL6AV itself says a uniform
  q is not curvature. Local geometry must come from relational variation.

**C. Orientation chart (exact algebra, formal smooth chart).**
- `J_d = J prod_{a!=d} kappa_a^2` and `j_d = 2 sum_{a!=d} rho_a` (AV09–AV10).
- Inverse: `rho_d = (1/6)sum j_b - (1/2)j_d` (AV11).
- Tetrahedral vectors `t_a`: `sum t_a t_a^T = I` (AV13).
- `E(S)_a = t_a^T S t_a` has rank 4, image A1+T2, kernel E (traceless
  diagonal) (AV14–AV15). Explicit reconstruction (AV16).
- The pair-E is isomorphic to `ker E` (AV17), so
  `(A1+T2) ⊕ E ≅ Sym^2(R^3)` (AV18).
- This is a "typed source/read atlas", **not** one metric field:
  - the j_d are formal generator coefficients, not authenticated by finite
    binary words;
  - the pair-E is a query read;
  - no constitutive Jacobian or rank-6 right inverse exists.

**D. Five premises for an operational metric (§5).**
- `AV-PHASE`: a selected propagating phase.
- `AV-CONTINUUM`: one nondegenerate quadratic Lorentz cone shared by all
  admitted polarizations; not a union of cones, not a Fresnel/quartic
  characteristic.
- `AV-CLOCK`.
- `AV-CONSTITUTIVE`: a reciprocal rank-6 map that deforms the **principal
  symbol** itself, not masses or residues.
- `AV-UPDATE`: a causal retained-memory updater, which is what makes it
  two-way.

**E. Remaining gates for gravity (§6).** Common coupling of all sectors;
stress/Ward custody ("Port conservation is not a diffeomorphism Ward
identity"); RGRL-B; weak-field law; G.

### My interpretation, layered on GL6AV (not in the corpus)

**i. The orientation chart is a magnetic-stiffness tensor.**
- Ring exchange becomes `K_b (curl a)^2` in the Gaussian Coulomb theory
  (standard quantum-ice map; GL6AT §3, Hermele / Benton).
- Diamond hexagon family d has mean normal `t_d`. I checked this numerically
  in the GL6AT embedding using the AR.2 hexagon. For all four port triples the
  SVD normal satisfies `|n.t_d| = 1.000000`, with singular values
  (1.414, 1.414, 0.354): a puckered chair. Scratch script:
  `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/hexnorm.py`.
  So
  `delta H_mag ~ (1/2) B^T [sum_d delta J_d t_d t_d^T] B`.
- The map `j -> sum_d j_d t_d t_d^T` is the adjoint of `E` and has the same
  image, A1+T2.
- So GL6AV's chart deforms the magnetic stiffness in five of six directions:
  trace plus three off-diagonal.

**ii. The pair-E is the traceless-diagonal part of the local `e⊗e`.**
- In the lock, `p_1 = M12+M34 = E_x^2 - 2`, and likewise for y and z.
- So the "typed atlas" is (B⊗B) in A1+T2 plus (E⊗E) in E.

**iii. A Maxwell field in a background metric needs both deformed by the same
tensor.**
- Tamm-type `eps ∝ mu` is required for no birefringence. That is AV-CONTINUUM
  plus AV-CONSTITUTIVE.
- The atlas cannot give this from one-node and orientation operators alone:
  - `E(B⊗B)` (the traceless-diagonal magnetic part) is invisible to
    orientation couplings;
  - `T2(E⊗E)` vanishes at one node.
- Missing pieces:
  - (a) a non-tetrahedral ring sensitivity, e.g. bilocal or longer loops, for
    `E(B⊗B)`;
  - (b) bilocal pair products for `T2(E⊗E)` (GL6AS §8);
  - (c) the constitutive join.

**iv. The lapse direction q^6 is the derived temporal (g00) channel.**
P-37 register §4 says temporal sources cannot be "filled by hand". This is
one derived source of them, though only as a global reparametrization.

### Port to canonical #7 (outside partition, cross-pointer)

- In #7, h is constant on every bond (`VA/FIRST_CHUNK_PREMISE_CARD_V006.md`
  line 345), so records do not gate h. GL6AV's kappa-gating is not in #7 as
  written.
- #7's analog is record feedback `H_fb = -lambda_R sum d_v q_v` (card line
  348). It shifts the virtual denominators and changes the hexagon
  coefficient.
  - `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.md`:
    all 64 six-vertex record words; `c6` ranges from 63/8 (no records) to
    2504/81 (all occupied).
  - The arrangement matters, e.g. qmask 3 (110000) gives 617632/50625 while
    qmask 5 (101000) gives 7852384/759375.
  - Also `PW/URM_DARK_SECTOR_PROGRESS_V070.md` lines 7–9 ("Record arrangement
    matters").
- So the #7-native version of GL6AV's record→J_c map exists. It is
  nonlinear in the record word rather than a product.
- GL6AV's representation algebra (AV13–AV18) ports unchanged. The A1 part
  needs a record density. The T2 part needs an orientation-dependent record
  texture (my inference).
- Sign as recorded: occupied records **raise** c6 in #7, so the collective
  clock runs faster where records are occupied. This is an observation, not
  a gravity verdict.
- P-37 already carries this mechanism implicitly as `U_e(rho)` and
  `K_b(rho)` endpoint dependence (P-37 register §2,
  `chi_lin,1/chi_lin,0 = Ue(0)/Ue(1)`).

---------------------------------------------------------------------------

## 11. Unclassified lead flagged by the corpus (my algebra, not corpus)

GL6AV §1 and GL6AQ §4 explicitly leave "lower-order configuration-dependent
diagonal shifts" for nonuniform kappa unclassified.

**Fourth order.** With link-dependent `kappa`, the adjacent-pair words of
GL6AO's census carry `kappa_e^2 kappa_f^2`. Their weight depends on whether
the pair is opposite or equal (`p=2` vs `p=6`), i.e. on `M_ab`. The diagonal
term is therefore
`sum_v sum_{a<b} kappa_a^2 kappa_b^2 [alpha + beta M_ab]`.

**Linear order in `rho = log kappa`.** The term is
`2 beta sum_v sum_a rho_{v,a} sum_{b!=a} M_ab = -2 beta sum rho`, using the
lock identity `sum_{b!=a} M_ab = -1` (AN15). That is a constant.

**Second order.** `4 beta sum rho_a rho_b M_ab` couples record texture to
pair-E.

**Second order (h²).** The diagonal shift is configuration-independent in
the lock: every flip costs 2Ud.

**Result.** At fourth order the records reach the E⊗E channel only
quadratically in record deviation. This is consistent with AQ13's linear zero.

Worth a dedicated census if the E completion of the atlas is pursued.

---------------------------------------------------------------------------

## 12. Negative inventory (useful for P-37)

- **No displacement / embedding / elastic sector** in GL6AN..AZ. The
  embedding appears only as a declared calibration (GL6AT AT03; GL6AP §7;
  GL6AV AV-CONTINUUM).
- **No native Ward identity beyond port/T2 charge.**
  - Linear degree charge: absent (AN10–AN12).
  - Pair-E: absent (AP19).
  - Port conservation is "not a diffeomorphism Ward identity" (GL6AV §6.3).
- **No Debye or charged sector.** The locked Hilbert space excludes
  degree-violating charges (GL6AT §6).
  - GL6AY: local charged excursions `P_L -> Q_L` exist in the full
    Hamiltonian but are prethermally suppressed.
  - So P-37's screening rescuer would need the unlocked sector, which this
    block treats as remainder.
- **No pole or physical cone.** Everything is conditional on `ICE0-STATIC`,
  the GNS bridge and the selected phase.

## 13. Cross-pointers outside partition (not analyzed)

The GRA_F* lanes look directly on topic for the quadratic / tensor channel:

- `PW/LANE_GRA_FK_F3_Q4_ICE_HYBRID_TENSOR_RESPONSE_V001/`
- `PW/LANE_GRA_FL_F3_Q4_MAXWELL_COMPOSITE_POLE_SCREEN_V001/`
- `PW/LANE_GRA_FM_F3_Q4_INHERITED_TT_KERNEL_BOUNDARY_V001/`
- `PW/LANE_GRA_FO_F3_Q4_FINITE_TT_FOUR_POINT_V001/`
- `PW/LANE_GRA_FP_F3_Q4_RGRLB_CONSTRAINT_ORIGIN_SCREEN_V001/`
- `PW/LANE_GRA_FJ_F3_Q4_AUTHENTICATED_LINK_PAIR_RESPONSE_V001/`

Also:

- `R/UNT_RECORD_TO_GEOMETRY_MINIMAL_JOIN_2026-09-27_V001/README.md`
  (validity-audit row 4, DERIVED_APPROXIMATION).
- The BS10 record-feedback hex family in
  `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/`.
