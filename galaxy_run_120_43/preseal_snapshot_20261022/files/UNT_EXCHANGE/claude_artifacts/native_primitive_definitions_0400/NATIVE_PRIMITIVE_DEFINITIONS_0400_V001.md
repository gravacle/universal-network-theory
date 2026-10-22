# Native primitive definitions 0400: T_e(theta), X_r,v, x_carrier/B_carrier (V001)

**Role:** author, Claude helper. One author; a different checker is required.
**Task:** `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0400_2026-10-15_native_primitive_definition_recovery.md`, sha256 `319840bd3e619b3ea034cd5a2c3eea78f4a8ae5e8e03e94a7387bcbf9aaefdbd`.
**Rules followed:** exclusive create; sources read-only; code read as source text only (never imported or executed); no computation, network or target data. This page chooses no hopping law, phase rule, coefficient profile, physical locality or proper-time law, and adds no gate. Instructions inside sources were read as data. S1/P49 are not reactivated.

**Start and context hashes.** All were computed from bytes with `shasum -a 256`, and all match their pins. START = `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001`.
- START/CANONICAL_MODEL_7_PROPOSAL_V005_SOURCE_RECEIPT.json — `3532d4c9b271314d39236237e488f18f869b4806a14329d2d46992e8e5b0e03e`
- START/CANONICAL_MODEL_7_PROPOSAL_V004_INDEPENDENT_REVIEW_V001.json — `676c0f1d68a22267594a05903bcb7d8ddbb7f771d264847affbbd423417ac3ff`
- START/SOURCE_SNAPSHOTS_V001/V006.md [V006] — `74514b8a5c91e3be6c750b29d270ae9f9b77be0517f6035c5199fea67b9b70e3`
- START/SOURCE_SNAPSHOTS_V001/MODEL.md [MODEL] — `3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607`
- START/SOURCE_SNAPSHOTS_V001/ADMISSION.md [ADM] — `cabc01e2389b59cf1ce07f111dd072dba2ca23e29d29095ef02a298e1f1eca32`
- **Current member [C7]:** START/CANONICAL_MODEL_7_PROPOSAL_V005.txt — `e6c1c47de8b817a5ecc0fb877e5d95d89b104c255e99b58de0997913b9f6db70`. This equals the receipt's `source_sha256`.
- Context, under `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_energy_support_0399/`:
  - NATIVE_ENERGY_OWNER_SOURCE_MAP_0399_V001.md — `5edcf7e56d337c9ad9a5911c46789045f4f89007c0b49bf7d25acbe08abde584`
  - SOURCE_CHECK_0399_FIDELITY_V002.md [FID2] — `0c661284b9ce10b447ddc2c868942740c53fa418df332f247c7cb5690ff88134`
  - SOURCE_CHECK_0399_COMPLETENESS_V001.md — `ca91cbb318169eb498d2d586395a2472f14d763a84c28b25b1b1d5a50ee4dc3a`
  - Its erratum, SOURCE_CHECK_0399_COMPLETENESS_V001_ERRATUM_V001.md — `b1552d8a69a7a620f2c98d24b5f151854ed11087f6a91b1099c634fcea76a497`

**Status labels.** FIXED = the convention is fixed by the cited source. DECL = C7 lists the item as an additional declaration. UNCHOSEN = an extension that no source in scope fixes. NOT WRITTEN = absent from the bounded scope below; this is not an archive-wide negative.

| symbol | recovered literal definition (quoted) | physical factors / support | source (key, lines; full path and sha256 in the citation list) | applicability to current member (C7 = V005 H7) | what remains actually unspecified |
|---|---|---|---|---|---|
| **T_e at theta=0** (U1, action) | "Off-diagonal physical entries are -h for every incidence flip, -t for every occupied-edge hard-core XOR hop" and "Parallel labeled edges give separate hop channels and summed matrix entries" [Q4P l.25-27]. "Local carrier and Record factors are the owned invariant common-content {B,x} restriction. No CAR signs" [Q4P l.10-11]. Code: `if p.hopping and (state.incidence>>e)&1 and ((state.carriers>>u)&1)!=((state.carriers>>v)&1): yield Event('hop',e,State(state.incidence,state.carriers^(1<<u)^(1<<v),state.records),p.hopping)`, with the physical entry `-event.rate` [NMC l.137-138, l.150]. "T_e transfers the one carrier content between occupied/blank endpoints." [V001P l.19]. Parent: "T_{uv}=\sum_{x=0}^1(\|B,x\rangle\langle x,B\|+\|x,B\rangle\langle B,x\|)" [BS l.177-185, BS07] | **Endpoint factors:** the two hard-core carrier factors C^2_p at u and v, each holding blank B or the one common content x. **Action** (author's reading of the quotes): \|x,B⟩⟨B,x\| + \|B,x⟩⟨x,B\| on (p_u,p_v). It is zero on BB and xx. It carries no fermionic string sign, so it is hard-core exchange. It is identity on q, the cells and all other factors. **Support:** edge-local, one labelled edge at a time | Q4P, NMC, V001P, BS | Same symbol and the same t. The renames are V006 N_car,v → C7 p_v and ε_car → ε_c [V006 l.346-348; C7 l.4-6]. The domain matches C7's "all Nc=0..Nv" [HIJ l.5]. NMC's primary completion is restored_bs11 (#8), but completion changes only the diagonal current [NMC l.115]. The hop channel is the same in both completions, and C7's literal +λ_J Σ d_v p_v [C7 l.7, l.13, l.23] is untouched. **FIXED** | Nothing at theta=0 |
| **theta** (U1, phase entry) | "H_car = ε_carN̂_c − tΣ_en_eT_e(θ), with the sum over every bond of the sector's graph" [V006 l.346]. "Carrier connection θ (first): ∂H/∂θ = −Î, the carrier current [CTP]. DP-θ sets θ = 0" [V006 l.416]. "DP-θ. θ_ext = 0." [V006 l.1060]. Code: `phase=np.exp(1j*self.theta[m][a,b])`, `o[:,m+b,:]-=p.hop*phase*mask*s[:,a,:]`, `o[:,a,:]-=p.hop*phase.conjugate()*mask*s[:,m+b,:]` [CTPc l.77-79]. "Native edge current u->v is J_e=i t n_e(b_v^dagger b_u-b_u^dagger b_v)" [HIJ l.12]. "For a native hop phase, partial_theta_e H=-J_e." [HIJ l.24] | One real phase θ_e per oriented edge. It enters as e^{+iθ_e} on the tail→head transfer and e^{−iθ_e} on the reverse. In CTPc the edge runs from A-side site a to B-side site m+b. The result is Hermitian. Orientation is part of the edge label, "e:u→v" [BS l.204, BS09] | V006, CTPc, HIJ, BS | C7: "hop phases enter through the Hermitian T_e(theta)" [C7 l.13]. C7 also says "dstar,theta and the phases/profile ... are additional declarations" [C7 l.21]. The literal V006 value is θ=0, and "The card holds ... theta=0" [V001P l.39]. V002–V005 do not restate a value. Entry form: **FIXED** for one carrier [CTPc]. Values: **DECL** | (i) The θ_e values for C7 (DECL; not chosen here). (ii) **NOT WRITTEN:** an explicit many-carrier matrix at θ≠0. CTPc is a one-carrier sector, Q4P/NMC are "at theta0" [Q4P l.9; NMC l.6], and HIJ gives only ∂_θ at zero source. (iii) **NOT WRITTEN:** the sign of θ_e relative to the q4 bond listing "joins A(r) to B(r + e_s)" [V006 l.319] |
| **n_e** (U1) | "Every edge has incidence bit n_e"; "d_v=sum_(e incident at v)n_e" [C7 l.4]. H_inc = −hΣ_eX_e + ΔΣ_en_e + … [V006 l.345]. Gate in code: `(state.incidence>>e)&1` [NMC l.137]; `mask=d['masks'][a,b]` [CTPc l.77]. "unchanged BS09 hopping follows its occupied `G_n`" [MODEL l.250] | The C^2 incidence factor of edge e. In the hop term it is a diagonal gate: a hop occurs only if n_e=1. T_e does not change n_e; −hX_e flips it | C7, V006, NMC, CTPc, MODEL | Same symbol. **FIXED** | Nothing |
| **T_e on surgery-created edges** (U1) | "the children are (a_i, s_B) and (s_A, b_i), appended in cut order. Star s_B … joins the four A-ends, and star s_A … joins the four B-ends" [V006 l.330]. "Both stars receive blank Records, and the carrier is never on a star at Birth (J_blank)." [V006 l.332]. The V004 receipt anchor reads "Inclusion.encode_word copies each cut bit to both children" [RCP4]. F2 only: "Current source phases pull back through the actual F2 three-edge path." [CTP l.27]; `self.theta={3:theta,2:np.array([[theta[0,2]-theta[2,2]+theta[2,0],theta[0,1]],[theta[1,0],theta[1,1]]])}` [CTPc l.31-32] | Each child edge has its own n_e, which copies the cut bit at Birth. The new stars enter with a blank carrier, blank q and an I cell [C7 l.15]. The hop on children uses the same −t n_e T_e [V006 l.346: "every bond of the sector's graph"] | V006, RCP4, CTP, CTPc, C7 | Structure: H7_new contains −t n_e T_e(θ) on every child edge with the same real t (**FIXED**). At the literal V006 θ=0, child edges carry zero phase (**FIXED**). CTP's path pullback is fixed only for the one-carrier F2 K2,2→K3,3 member. C7 uses F_q4, not F2 [C7 l.4, l.15] | **UNCHOSEN:** a phase rule on the q4 child and star edges at θ≠0, including any relation to the deleted cut-edge phase. No such rule was found in scope. 0399 corrections: G l.38 says such a rule "may be used", and L l.20 says the family "requires a fixed complete coefficient/phase profile before any prediction" [FID2 E4] |
| **X_r,v** (U8) | "Every site carries a binary Record q_r,v." [V006 l.321]. "H_form = ε_rΣ_vq_r,v + gΣ_vN_car,vX_r,v" [V006 l.347]. "U_Z := Π_vZ_r,v maps gN_car,vX_r,v to −gN_car,vX_r,v" [V006 l.677]. "One carrier of fixed content x, with all Record targets initially B. The active Record alphabet at each site remains {B,x} under BS08." [CTP l.12-13]. Code: `o[:,v,:]+=p.bind*s[:,v,:][:,d['record_words']^(1<<v)]` and `elif kind=='x':o[:]=s[:,:,d['record_words']^(1<<v)]` [CTPc l.81, l.94]. "+g for a Record flip at a carrier site" [Q4P l.26]. "U_R X_record,v U_R=-X_record,v" [Q4P l.40]. Parent: "K_{a\to b}=\sum_x \|x\rangle\langle x\|_a\otimes(\|x\rangle\langle B\|_b+\|B\rangle\langle x\|_b)" [BS l.189-193, BS08]; "q=1 is physical occupation of a record-bearing register" [BS l.79] | Acts only on the native Record factor C^2_q at v: X_r,v = \|x⟩⟨B\| + \|B⟩⟨x\|, that is σ^x in the q basis, with q=0↔B and q=1↔x. It is controlled by p_v (formerly N_car,v). It is identity on the cell, the edges and other sites. **Support:** site-local | V006, CTP, CTPc, Q4P, BS, NMC l.141-142, l.150 | Same symbol. Renames: N_car,v → p_v and q_r,v → q_v. The physical sign is +g: "positive physical Bind sign" [HIJ l.5]. C7: "Bind g p X_r rotates q, including at a spent site, and commutes P_S" [C7 l.17]. Preserved corrections: "Rung-1 circuit and g p X_r are not proven equivalent on a common full domain" [X14 l.66], and "Bare native Record parity fails the g p_v X_r term" [HIJ l.14]. **FIXED** | No operator element is open. Only g's value remains, as an allowed magnitude [C7 l.21] |
| **x_carrier, B_carrier** (U7) | "For a loaded cell `w` co-located with retained target `r`, define K_rel(w,r) = \|S,x><R,B\| + \|R,B><S,x\|." [ADM l.65-68]. "ALLOW(w,r) = 1 iff cell_w=R and target_r=B." [ADM l.75]. "K_rel \|R,x> = 0, K_rel \|I,B> = K_rel \|I,x> = 0. Thus an occupied-target or inactive-cell attempt is exactly null." [ADM l.83-87]. "for a loaded cell `w` and blank retained target `r`" [MODEL l.1490-1491]. HIJ l.5: "A_v^+=\|S,x><R,B\| … We transplant that operator … into the COMPLETE binary one-content q4 domain with all Nc=0..Nv". "Q_v=p_v+P_R,v; … Admission gives dot p_v=I_A,v, dot P_R,v=-I_A,v, dot P_S,v=I_A,v" [HIJ l.12]. "Successful admission transfers Ready content to the carrier" [V002P l.17] | B_carrier is the blank carrier, p_v=0, which is the unique blank of [BS l.63-81, BS01]. x_carrier is the carrier holding the one common content x, p_v=1 [CTP l.12; Q4P l.10-11]. Both live on C^2_p at the same site v as the cell, with I_q on q_v. **Support:** site-local | ADM, MODEL, HIJ, V002P, BS, CTP, Q4P | The letters match ADM/HIJ. V002–V005 add the subscript "_carrier" to separate them from q's own {B,x} alphabet; this is a rename. The support changes from ADM's prism retained target r to the q4 site carrier p_v: "Its original prism transport/cursor are NOT identified with q4" [HIJ l.5]. **FIXED.** Newborn stars enter as a blank carrier in an I cell [C7 l.15], and ADM l.84 "K_rel \|I,B> = 0" applies: no free newborn donor supply. ADM's "Delta B" [l.100, l.144] is bandwidth bookkeeping, not this label. ε_B (Birth) is also distinct | The labels have no open items. The κ_v magnitude and phase profile is DECL: "Uniform kappa versus a spatial magnitude/phase profile is a declaration, not silently chosen here" [C7 l.13]. HIJ's χ_v is a source chart [HIJ l.22-23]. The E_I/E_R/E_S values are DECL. The identity of HIJ's "OWNER_PROTOCOL lines49-68" with ADM is **NOT WRITTEN** in scope: ADM holds the same K_rel at l.65-87, but no path is given |

## Search scope

- **Read in full** (small, non-archive): C7; the V005 receipt; the V004 review JSON; ADM.
- **V006** (rg -n, ≤60-line sed windows):
  - Patterns:
    - `T_e|T_\{e\}|X_r|X_\{r|theta|θ`
    - `hop|hard-core|N_car|e\^\{?i|c†|c\^†|a†|σ\+|σ⁺|sigma|Pauli|\bZ_r|q_r,v|\[CTP\]|\[MODEL|\[Q4|\[NAND|\[GKSL|\[PHOTON|\[R2`
    - `CTP`
    - `^#|DP-θ|DP-THETA|θ_ext`
    - `(?i)pull ?back|pullback|path phase|connection phase|phase rule|hopping phase|child.*phase|phase.*child|star.*phase`
    - `BS08|alphabet|\{B,x\}|\{B, ?x\}`
    - `(?i)admission|A_v|x_carrier|B_carrier|K_rel`
    - `J_blank`
  - Windows: l.150-182 (reference key), l.312-360, l.388-394, l.408-420, l.1056-1062. The last window is the DP-θ line; its neighbouring lines were geometric definitions, with no result values.
- **MODEL** (rg -n plus windows l.246-256, 1258-1268, 1482-1500):
  - `T_e|X_r|theta|θ|x_carrier|B_carrier|\|S,x|\|R,B|A_v|hard-core|N_car`
  - `(?i)bind|\bhop|carrier_hop|record_flip|admission|K_rel|\bB_carrier|x_carrier|Ready|Spent|peierls|exp\(1j|e\^\{i|e\^\(i`
  - the pullback pattern above
  - `(?i)K_rel|x_carrier|B_carrier|A_v\^|blank retained target|\|S,x|\|R,B`
- **SOURCE_SNAPSHOTS_V001, non-recursive, used only to locate sources:**
  - `rg -c` with `BS08|X_r|X_\(r|N_car|T\(theta\)|T_e\(|x_carrier|B_carrier|\|R,B\||\|S,x`, excluding GALAXY*, CALIBRATION* and BUDGET.json.
  - Hits were in ADMISSION, BS, CTP, EXCHANGE_0002, HI_JOIN, PACKED_IDENTITY, Q4 and V006.
  - Only the hit lines of PACKED_IDENTITY.txt (`8121a52cbfaec04ae1374f379826c41b1636713a017c2d44ea30f8b23a869b07`) and EXCHANGE_0002.md (`66af377e61099f1c5b1275a2a0425f7e7eac7a60414d4e5d2d648ed4c9c7923e`) were viewed. Neither file was followed.
- **Same-stem files and corrections** (rg `T_e|X_r|x_carrier|B_carrier|theta|hard-core|\|S,x`):
  - CANONICAL_MODEL_7_PROPOSAL_V001–V004. V001 l.1-40 was read.
  - V002 was also searched with `theta|hop|carrier`.
  - EXACT14_CROSSWALK_V001.txt and CROSSWALK_ROWS_V001.json.
  - The V006 ERRATA (rg `T_e|X_r|θ|theta|N_car|carrier|Record|hop|phase|Bind|H_car|H_form`): 0 hits.
  - The V004 receipt was parsed for display only.
  - CROSSWALK_AND_SOURCE_PINS_V001.json was used only for hash→path lookup.
- **Followed sources:**
  - CTPc: rg `^import|^from|def |theta|phase|exp\(|1j|hop|bind|X_r|flip|record|carrier|B|x`, plus l.6-98.
  - NMC: rg `^import|^from|def |class |theta|phase|exp\(|1j|hop|bind|flip|record|carrier|sign|fermi|boson|hard`, plus l.1-8 and l.58-153.
  - HIJ: outline rg `^[0-9]+\.|^[A-Z]`, l.4-15 and l.20-26, and `(?i)theta|phase|b_v|bdag|b_u|orient|\{B,x\}`.
  - Q4P: l.1-60, plus the same pattern as HIJ.
  - BS: rg `\bB\b|\|x|alphabet|blank|content|BS0[0-9]|tag`, plus l.61-82 and l.170-242.
  - CTP: read in full (74 lines).
- **Not opened (budget):** Q4SRC `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/local_record_feedback_q4_sparse_insertion_verification_v001.py` (`774c81de75458fb430009655f83f00dcc24bac423385ac1b72409dc6f160134e`, as pinned in RCP4; not re-hashed). Its child-bit copy is cited only through the RCP4 anchor.
- **Scope of the three NOT WRITTEN items:**
  - Many-carrier θ≠0 matrix: all files above with the θ patterns.
  - q4 child-edge phase rule: V006 and MODEL with the pullback pattern, plus CTP, CTPc, HIJ and Q4P in full or windowed.
  - OWNER_PROTOCOL path: HIJ, plus `OWNER_PROTOCOL` in CROSSWALK_AND_SOURCE_PINS_V001.json and EXACT14_CROSSWALK_V001.txt.

## Citation list

Followed primitive-definition sources: six beyond the start files. All hashes were computed from bytes and match the pins in RCP4 or CROSSWALK_AND_SOURCE_PINS_V001.json. EP = `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics`.
1. [CTP] EP/NATIVE_SHARED_PARENT_CLOCK_TRANSPORT_PROTOCOL_V001.txt — `fba7fbeea0da005b2dc85e6dc557a2e61f3fe621923020285988696bbb9412bb`. It is byte-identical to START/SOURCE_SNAPSHOTS_V001/CTP.txt and is cited as [CTP] at V006 l.174 and l.323.
2. [CTPc] EP/root_native_shared_parent_clock_transport_v001.py — `d7871d1bd4c55b826c2d7a04606a2552e418017c12379fc018b90811aae4a2a9`, cited at V006 l.174.
3. [HIJ] EP/PHASE12_PARALLEL_SCREEN_V001/HI_COMMON_ADMISSION_SOURCE_JOIN_V001/PROTOCOL_V001.txt — `87339caafec6b01c7212e32984041c351ceda3e4a2c52a652b7b0a4dbb585f83`. It is RCP4's "ADMISSION" entry and is identical to snapshot HI_JOIN.txt.
4. [NMC] EP/PHASE12_PARALLEL_SCREEN_V001/native_many_carrier_sparse_operator_v001.py — `6b8d8dfdd8b1973f80b587c98584610759ca8d796010fa3dcf3928741f8caf88`. It is RCP4's "NATIVE" entry and is identical to snapshot Q4_SOURCE.py.
5. [Q4P] EP/PHASE12_PARALLEL_SCREEN_V001/NATIVE_MANY_CARRIER_SAME_REFERENCE_SPECTRAL_PLAN_V001.txt — `438608bfd74e46d96cf8333ffd00f470e6ec8637f5b709d86ee5c1d0bb3a8b9e`. It is NMC's own protocol and is identical to snapshot Q4.txt.
6. [BS] /Users/bgm/Research/Universal Network Theory/program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md — `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`. It holds BS01/07/08/09, is cited as "BS08" at CTP l.13, and is identical to snapshot BS.md.

Same-stem files and corrections, under START:
- [V001P] CANONICAL_MODEL_7_PROPOSAL_V001.txt — `379dfc1129fe3e27256842b514232710b6703de56c197a965cf4ead679bdbdd2`
- [V002P] CANONICAL_MODEL_7_PROPOSAL_V002.txt — `528fbf7f8c18370899d94081426da92268693f504b9a8e583562cd2fedf59d1a`
- CANONICAL_MODEL_7_PROPOSAL_V003.txt — `638425929f022bda5f0dc77d7568616e2e9a01aaeda3bedb55cbd56ea1b937f4`
- CANONICAL_MODEL_7_PROPOSAL_V004.txt — `e668f8f74a017099be39c708a0f707dcec10b34f8b22083c7d9d58c01721d0c6`
- [RCP4] CANONICAL_MODEL_7_PROPOSAL_V004_SOURCE_RECEIPT.json — `f26bbdbc0e470fb5c4d5beb8c93d18af13649c02fc4808e2e8caa166e3897d3d`
- [X14] EXACT14_CROSSWALK_V001.txt — `d5b9dae7a13c53f072ee39428b5313463d295ca887fe059153e47c948ec461fc`
- CROSSWALK_ROWS_V001.json — `3108e9b07ba5db6ac8d69ed4b654a828f5f1be646afbdf010823a815f060e02f`
- CROSSWALK_AND_SOURCE_PINS_V001.json (lookup only) — `430420b33bc10376133be11cc25916e510dfccde4063256b1e3394266121a256`
- V006 ERRATA, SOURCE_SNAPSHOTS_V001/ERRATA.md — `c2675ac3f3f8edb571c7195b9ebcdd4c445d2c8837eaee7ee68f861fccb6be22`. It is identical to RCP4's ERRATA pin; 0 relevant hits.

**What this page does not change.**
- The #8 restored_bs11 term is not identified with #7. C7's literal +λ_J d p, the canonical corrections and the 0399 corrections stand as accepted.
- This page supplies source definitions that the bounded 0399 packet did not contain. It does not revise the 0399 map.
