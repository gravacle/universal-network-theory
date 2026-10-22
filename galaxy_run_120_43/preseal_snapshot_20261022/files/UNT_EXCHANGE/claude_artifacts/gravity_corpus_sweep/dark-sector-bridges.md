# Gravity corpus sweep: dark-sector bridges + P27/P31/P32 (raw notes)

Partition: `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation` (top level and `ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics`), plus `UNT_EXCHANGE/lanes/P27_CODEX3`, `P31_CODEX3`, `P32_CODEX3`. There is no P33 lane and `P32_OPEN` is empty.
Method: everything was read-only. I scanned the first 600 characters of all 5,533 .md/.txt files under 2 MB, ran a content grep for solder, piezo, Maxwell stress, graviton, ring exchange, displacement, elastic and bond angle, and read the hits in full. I did not execute any .py file.

Abbreviations: J = `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation`, X = `J/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics`, L = `/Users/bgm/Research/UNT_EXCHANGE/lanes`.

---

## A. How the main line chose its source law

1. **P-27 port** (`L/P27_CODEX3/GRAVITY_BRIDGE_CANONICAL_V004_PORT_V002.md`) classifies 34 bridge premises (B01–B34) and 6 obstructions (O1–O6). All the physical metric bridges (RGRL A–C, WTC-H1..H5, GL6CR, EIR, F3) are STILL ADOPTED. The only derived items are algebraic lemmas:
   - PMICS (pair memory to a symmetric tensor; curvature symbol of rank 3 at k≠0);
   - PMSR (rank-6 pair reciprocity under commuting conditions);
   - the GL6CS strict-lock scaling obstruction;
   - the FR edge-dyad rank obstruction;
   - the GJ-W diagonal-commutator Ward obstruction.

   It routes "Full gravity source family" to P-31 and the "Same-state kernel/Ward" to P-32.
2. **P-31 V001** (`L/P31_CODEX3/P31_FULL_CANONICAL_SOURCE_FAMILY_AND_RANK_V001.md`) is an additive source law:
   - edges get `l_e = alpha_u + n_a^T j_u n_a`;
   - nodes and Birth get trace only;
   - shift enters as a hop phase.

   Results: rank 8m, a 2m E-null (FR survives), spatial rank 4m. The Ward test W4 fails because the hop-only momentum annihilates the carrier vacuum while the strain still sources incidence flips.
3. **TO_CODEX/0024** (`/Users/bgm/Research/UNT_EXCHANGE/TO_CODEX/0024_2026-10-12_review-Codex3-P31-and-bond-angle-successor.md`). Claude's review proposes a Keating-type bond-bending term, citing the diamond-lattice precedent: "weights each pair product by its bond-angle metric factor". **The only criterion given is that it restores rank 6 (evades FR).**
4. **P-31 V002** (`L/P31_CODEX3/P31_BOND_ANGLE_SOURCE_SUCCESSOR_V002.md`):
   - The degree-penalty cross terms become `2Ud exp(l_v + c_ab(bar j_v)) n_va n_vb`, with a normalized cosine and exponent coefficient 1 (A1–A3).
   - Rank is 10m, spatial rank 6m (R1'–R6'). The angle-only map has rank 5 (the conformal null).
   - **The W4' Ward failure is unchanged** (§8).
5. **TO_CODEX/0026** passed V002 as a candidate on rank grounds only. In **TO_CODEX/0027** the principal adopts it "for testing", revisable. That is recorded in `L/P32_CODEX3/PRINCIPAL_SOURCE_LAW_ADOPTION_ENTRY_V001.json`, and the kernel setup is `L/P32_CODEX3/P32_ADOPTED_NATIVE_KERNEL_SETUP_V001.txt`.
6. **What the selection never examined:**
   - whether the source couples to the emergent gauge field linearly or through gauge-invariant bilinears;
   - the corpus's already-worked *geometric* strain law (the plate/coframe charging law in §C1 below), whose traceless jet has no linear polarization term.

   P-37 then found λ = 2Δ/3 − 8Ud/9 ≠ 0. The source is `X/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/EXTERNAL_CODEX3_P37_FORMAL_ENDPOINT_SOURCE_REVIEW_V001/INDEPENDENT_FORMAL_THEORY_REVIEW_V001.txt` §2: "2Ud A:X gives Ud/3 times the diagonal-traceless quadratic expression and -4Ud/9 times the shear linear polarization ... lambda=2Delta/3-8Ud/9".

   My check of the algebra: the linear part of `n_a n_b = (1 - Z_a - Z_b + Z_a Z_b)/4`, weighted by `dc_ab`, sums to `(Ud/3) sum_a u_a(X) Z_a` for traceless X. Here `sum_{b≠a} dc_ab = -2u_a/3`. **The piezo term comes from weighting occupation products, which contain linear Z, rather than deforming a quadratic form in Z.**

## B. Alternative channels the bridge documents considered

- `J/NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`. An ADOPTED weak-lapse postulate `L_v = 1 + a_ext x_v/c^2`. The source is the energy dipole `Z_X = ell D_X/(2c^2)`, with `D0 = (1+n/4)DeltaP + (1-n/2)DeltaR + g Pc DeltaX`.
  - Exact results: initial null `S_Z(0) = 0`; law A's insertion is Q-independent (`Z_A = gamma0 D0`).
  - The current-square allocation changes the gradient source but not H. The note itself says: "candidate weak-lapse bridge, not derived gravity".
- `J/HARD_LIMIT_GRAVITATIONAL_INTERFACE_RESULT_V001.md`. Under an ADOPTED covariant mechanical parent with a preferred clock, stored hard-mode excitation plus signed polarization obeys pressureless-dust scalar stress equations. This is a metric-based result and is conditional.
- `J/SHARED_GRAVITY_NORMALIZATION_RESULT_V001.md`. In an ADOPTED preferred-clock action, `rG = (1-KB/2) lambda_s/(1+lambda_s)`. BBN (Alvey et al.) excludes KB = λs = 1 and requires `lambda_s >= .92/(.08-KB/2)`. Purely effective-model.
- P-27 B28–B34. The count/Birth-volume dictionary `V = Voff + nu<N>`, `g* = 3 nu c^2 Eunit/(8 pi G hbar^2)`, and the T3 reaction chart: all STILL ADOPTED.
- `J/UNIFIED_PHYSICAL_GEOMETRY_AND_CAUSAL_FORMATION_BRIDGE_CANDIDATES_V001.txt`, two members:
  - **Member A:** an explicit memory-to-metric map `L(C) = Gamma_ref^1/2 exp[k sum B_ab (C_ab - 1)] Gamma_ref^1/2`.
  - **Member B:** the metric responds via the action stress `T_complete`.
  - Also rejects the Fisher-solder shortcut. The QFI of a translation-invariant eigenstate is zero.
- `X/NATIVE_SHARED_PARENT_TO_ADOPTED_GRAVITY_CROSSWALK_V001.txt`. States plainly that the gravity used is WTC/RGRL adopted. Lists the reusable pieces (§2 A–G, including **E: record-pattern stiffness / optical response**). Exact pair-memory chart in §3.

## C. Mechanisms (details)

### C1. Complete charging-strain law via plate coframe. Native parent plus a declared apparatus geometry.
Files:
- `J/LOCAL_RECORD_FEEDBACK_COMPLETE_STRAIN_SOURCE_CONTRACT_V001.md`
- `J/LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md`
- `J/LOCAL_RECORD_FEEDBACK_COMMON_COFRAME_OPTICAL_BINDING_V001.md`
- `J/LOCAL_RECORD_FEEDBACK_MAXWELL_LIGHT_SOURCE_CONTRACT_V001.md`
- `J/NATIVE_METRIC_MAP_CHARGING_DISCRIMINATOR_V001.md`
- result: `J/LOCAL_RECORD_FEEDBACK_3D_SIX_STRAIN_CHARGING_STIFFNESS_V001_RESULT.md`

How it is built:
- **Parent.** The record-feedback degree energy is realized exactly as a passive five-island charging form, `1/2 Q^T E5 Q = U c^2 - lambda_R q c + A_R q + 2 q*^2 e_d I` (five-island eq. 10). The port charges are `x_a = eta q* Z_a` and the record island is `x_R = eta q_R q`.
- **Strain law.** Strain enters only through the capacitances, via ideal plates transported by one affine F: `C_b(F) = C_b0 det F |F^-T n_b|^2`.
- **Result, eq. (4):** `Hcap,eps = -(tau/3) Jcap + mu[epsT_xx(Y12+Y34) + ... + (2/3)eps_yz(Y12-Y34) + ...]`, with `mu = q*^2 ed^2 C_m`.
  - The passive identities `C_gp em + C_pr(em-gcap) = ed C_m` and `C_gp gcap + C_pr(gcap-eR) = 0` give the "cancellation of every traceless qZ term".
  - The discriminator note confirms: "No direct record/qZ shear remains".
- **Meaning.** The traceless strain couples only to the vertex pair dyad. By the exact identity `X X^T = P + sum B_ab y_ab` (`J/LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001.md` eq. 3), that dyad is dev of the local E⊗E: a Maxwell-stress-type bilinear. The trace couples to the total charging energy Jcap.
- **Same coframe gives light.** `L_EM = (eps sqrtG/2) E^T G^-1 E - B^T G B/(2 mu sqrtG)`, `omega^2 = (eps mu)^-1 k^T G^-1 k`, and `delta log C_b = tr(strain) - 2 n_b^T strain n_b` reproduce the plate jet. This is one coframe for both the charging law and the cone.
- **Measured (L3 diamond, 54 vertices, q1, h = 1/5).**
  - Trace curvature is −2.79 to −4.57 (SE about 0.01–0.05).
  - Eigenvalues are indefinite: minimum about −1.27 to −1.63, maximum about +0.73 to +0.84.
  - The file says this is "not full mechanical stiffness".
  - The minimal-dilation pressure `p = <Jcap>/(3 Vref a^4) >= 0` gives no acceleration.
- **Status.** The plate geometry is a DECLARED apparatus chart: "not an emergent 3D phase or a calibrated network ruler". Under that premise the algebra is derived and was checked by native and observer review.

### C2. Pair-memory chart as a solder map. Algebra derived; physical identification adopted.
Files: `X/NATIVE_SHARED_PARENT_TO_ADOPTED_GRAVITY_CROSSWALK_V001.txt` §3; P-27 B09, PMICS, PMSR; `J/LOCAL_RECORD_FEEDBACK_DYNAMIC_MEMORY_COUNT_COMMON_METRIC_ACTION_V001.md`.
- Chart: `X = sum v_a s_a`, `XX^T = I3 + sum Y_ab B_ab`, `M2 = I3 + sum C_ab B_ab`. The six B_ab span Sym2.
- The centered version needs `mu = <X>` because the prepared states are not flip-symmetric.
- Dynamic action: `+N lambda:[gamma - L(y)]` with reaction `j = L_y^dagger lambda`, inclusive memory-work identity (4) and count/memory reaction matrix (8).
- Native evidence (rank up to 6 depending on time) is in `X/NATIVE_SIX_SOURCE_PAIR_RESPONSE_INDEPENDENT_REVIEW_V001.txt`:
  - singular values at tau = 1 run from 1.156 down to 4.27e-8;
  - directions above the allowance at tau = .5–1 are [1,5,5,5,4,6];
  - the sixth direction is poorly conditioned.
- Member A initial-jet compatibility (`J/READONLY_ALPHA_BS12_REGIONAL_COUNT_MEMORY_JET_COMPATIBILITY_SAVED_OUTPUT_REVIEW_V002.json`):
  - vacuum cases give `k_output = 5.547e-5 = alpha_fs^2/(24 h^2)`;
  - full-support fixtures do not match (residual of order 1e-3).
- **Observation.** V002's quadratic piece is conjugate to the same `Y_ab` operators as this chart. A source with the linear part removed would make the source law and the readout chart reciprocal, as in PMSR.

### C3. Record-conditioned ring (magnetic) stiffness and optical geometry. Native exact coefficient; optical map conditional.
- `J/BS10_RECORD_FEEDBACK_HEX_RING_V001_RESULT.md` gives the exact c6 for all 64 record words, `J6 = c6 h^6`. Blank is `63/8`, all occupied is `2504/81` (add cost 1, remove cost 3); 9222/9222 controls passed.
- Cross-partition pointers (cited by the crosswalk §2E):
  - `program-worktree/GRAVITY_EMERGENCE_EXPERIMENT_REGISTER_V001.md` GE-X29, `J_square(r) = h^4 sum_pi[Delta(S1)Delta(S2)Delta(S3)]^-1`;
  - GE-X30, `c = sqrt(kE kB)/hbar` and `g^2 = sqrt(kE/kB)`: an exact optical metric giving tidal curvature, **but `G_00 = 0` for the lapse-only representative and Maxwell conformal invariance leaves A(x) invisible**.
  - The primary lane RESULT files for these entries are missing from the resident checkout (crosswalk §6; I confirmed they are absent).
- The main line already pursues the canonical analog (P-39 g_ring(q), P-42). For P-37, a strain that changes the virtual-defect denominators changes kB. That is a gauge-invariant B^2 coupling: the magnetic half of a Maxwell-stress channel.

### C4. Held-hexagon lapse source: gradient-squared response, no linear term. Native, exact plus certified.
- Files: `J/HELD_HEX_NATIVE_DIPOLE_SOURCE_GATE_V001.md`, `J/HELD_HEX_DIPOLE_FORMAL_FOURTH_ORDER_V001.md`, `J/BS10_RECORD_FEEDBACK_HEX_SOURCE_V001_RESULT.md`.
- The midpoint source scales each flip and its gap together. The first virtual amplitude h/δ is source-independent, and the second-order self-energy is linear in L. The leading curvature is `W_AR = -2L/9 - 8L^2/[9(x+3y)]`, giving `chi0 = (7/12) h^4` from `[w_v - (w_add+3 w_remove)/4]^2`.
- The exact pair block is zero: `<partner|A|ground> = 0` by momentum.
- Finite certificate: energy drop in [5.90157e-7, 5.90161e-7], `STRICT_FINITE_DROP_CERTIFIED_CHI0_POSITIVE`, 1882/1882 controls.
- The exterior degree-2 identity cancels for every profile (eq. 1).
- **Lesson.** The linear coupling to polarization vanishes when the source rescales each flip together with its own gap. The P-37 λ is a mismatch between owner weights: edge Δ against node Ud pairs, while the flip −hX is weighted only by l_e.

### C5. Adopted continuum displacement/elastic sectors (none native)
- `J/ELASTIC_SHARED_STATE_V001.md` and `_RESULT.md`:
  - material coordinates X^I, `B^IJ`, `C = B/detB^(1/3)`, shear energy `mu_sh/4 [trC^2 - (trC)^2/3]`;
  - `cT^2 = kappa`, `cL^2 = 4kappa/3`;
  - `Phi - Psi = 16 pi G a^2 kappa m_g n pi_m`;
  - local stiffness strongly changes growth (Weyl ratio .068/.012).
- `J/POLARIZATION_GENERATED_RIGIDITY_V001.md`:
  - `gamma A2 I(C)/4`, so the shear modulus `gamma A2` is quadratic in polarization and zero in the unexcited vacuum;
  - the regular centre fails (R log R).
- `J/KINETIC_COULOMB_BOND_RIGIDITY_V001.md` and `_RESULT.md`:
  - isotropic bond sphere `E = Eref + T0<(n.C.n)^-1 - 2(n.C.n)^-1/2>`;
  - `G = 2T0(2s-1)/(15V0 s^5)`, `M = B + 4G/3`;
  - strongly elliptic for 1/2 < s < 7/4;
  - the prestress term is required.
- `J/KINETIC_COULOMB_SHARED_STRAIN_V001_RESULT.md`: no relativistic acceleration.
- `J/LOCAL_RECORD_FEEDBACK_TOLMAN_AND_SPATIAL_STRESS_IDENTIFIABILITY_V001.md`: **lapse-only data cannot identify spatial stress**. The witness is `eps (n-n0)^2`, which changes `Gamma_psipsi` by `18 eps V0 n0^2` while every lapse-only response is unchanged. It also gives the `3J` vs `2J` chain-rule contact.
- `J/SHARED_NETWORK_STRAIN_PREDICTION_V001.md`: conserved cell current `xi = -(1/3) ln(n_g/n_g0)`; the similarity closure gives `rho ~ a^-2` and no acceleration.
- `J/BS10_SHARED_STRAIN_GATE_V001_RESULT.md`: native BS10 eigensystems under an adopted homothety `H_s = 1 + (H-1)/s`; p > 0 and no acceleration.

### C6. Kinetic-coframe (principal-symbol) solder proposal. Unexecuted.
`X/NATIVE_ACTION_KINETIC_COFRAME_AND_VOLUME_CLOSURE_CANDIDATE_V001.txt`:
- `C_AB^{mu nu} = Z_AB D^{mu nu}` (7); `g = sqrt(-det D) D^-1` in n = 4 (9); source variations (11)–(14);
- the stress work equality (16) annihilates the null directions of J;
- the information-only conjecture `C = zeta F D` is refuted for a single oscillator: `C_qq/F_qq = hbar/(2 omega)`.

### C7. Intrinsic Hodge–Dirac complex. Algebra derived; weights undetermined.
`X/PHASE12_PARALLEL_SCREEN_V001/F_INTRINSIC_HODGE_CANDIDATE_V001/ASSESSMENT_V001.txt`:
- `B C = 0` (the q4 incidence and the hexagon boundary), `C C^dag = ell P_kerB`;
- with counting weights the scalar and transverse branches have rate ratio 8, so the Hodge star (metric) weights are the missing physical input.
- In DEC terms, a metric would enter as edge and hexagon Hodge weights: kE per link, kB per hexagon. That is a quadratic, gauge-invariant entry point.

### C8. Other native constraints relevant to sources
- `J/NATIVE_SOURCE_BRIDGE_DECISION.md`: exact sum rule `[n_e,[H,n_f]] = h_N delta_ef X_e` (the incidence/E oscillator strength).
- `J/NATIVE_MIDPOINT_SOURCE_CLOCK_CONSTRAINT_V001.md`: two allocations of the same H differ by an occupied-graph Laplacian `(lambda_R/2)(L_n L)_v`. Nonuniform sources are not fixed by H.
- `J/LOCAL_RECORD_FEEDBACK_COMMON_COFRAME_OPTICAL_BINDING_V001.md` eq. (7): equilibrium gauge-family contact `<H_aa> - chi_II(0) = 0` (diamagnetic/f-sum cancellation). Dropping the contact produces a spurious static optical stiffness.
- `J/UNIFIED_PARENT_HOMOGENEOUS_MAXWELL_WARD_AND_BACKGROUND_MATCHING_V001.md` and `J/NATIVE_INCIDENCE_MAXWELL_PAIR_SOURCE_V002.md`:
  - ADOPTED dilaton-type coupling `Z(O) F^2`, `O = sum chi_e n_e`, with source-held Ward identity `nabla T = -F^2 nabla Z/(4 mu0)`;
  - the Maxwell trace is zero;
  - this couples an external ordinary photon, not the emergent one.

## D. Synthesis for P-37 (my reading; not verified)

1. **The quadratic stress-like channel already has a worked, geometrically motivated source law in the corpus (C1).** The traceless shear jet is pure pair dyad (E⊗E-like). The linear traceless polarization coupling cancels identically by passive-circuit identities, not by tuning d*. Porting it means rewriting `Ud(d - d*)^2 + Delta n + record terms` of #7 as a charging form with explicit offset/record islands, applying the plate law, and checking whether the traceless linear coefficient vanishes for d* = 3. The cost:
   - it is a new declared source law, needing principal sign-off;
   - its premise (plate geometry) is an apparatus chart;
   - the trace sector still couples to Jcap;
   - the measured charging curvature was indefinite.
2. **The magnetic half (C3) exists natively.** Records and virtual-defect denominators modulate the ring coefficient. A strain-dependent denominator gives a B^2 coupling.
3. **Known ceilings carried over:**
   - Maxwell conformal invariance means any photon-only quadratic channel cannot fix the trace/volume (GE-X30), and `G_00 = 0` for the optical lapse;
   - Tolman: lapse-only data cannot identify spatial stress;
   - every displacement sector in this partition is ADOPTED continuum, which agrees with P-37's "no explicit microscopic displacement owner";
   - the GL6CS strict-lock powers (`K_EE ~ r^-6/Ud` vs tensor writer `r^6/Ud`) would need re-derivation for any H6 tensor-writer route.
4. **Structural note.** The dark-sector galaxy action is itself a linearly coupled polarization medium (h(a)·B, AQUAL-type). P-37's linear coupling of the source to the emergent polarization has the same structure, but in the shear (tensor) channel rather than the lapse-gradient (vector) channel. Whether a lapse gradient couples linearly to the emergent E via the energy dipole (NATIVE_ENERGY_DIPOLE) is unchecked. C4 suggests the midpoint lapse allocation gives no linear term in the held ice background.
5. **Imports flagged in this partition:**
   - every metric/EH/G normalization (WTC/RGRL);
   - the preferred-clock galaxy actions (AQUAL-type), BBN rG, the hard-limit dust interface, the energy-dipole weak lapse;
   - the elastic X^I sectors and the plate geometry;
   - the Birth-volume dictionary;
   - Member A's L(C) map.
