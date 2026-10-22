# Source check 0400 V001: native primitive definitions (T_e(theta), X_r,v, x_carrier/B_carrier)

**Role:** distinct checker, not author. I did not write the target page.
**Task:** `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0400_2026-10-15_native_primitive_definition_recovery.md`, sha256 `319840bd3e619b3ea034cd5a2c3eea78f4a8ae5e8e03e94a7387bcbf9aaefdbd`.
**Target (author page, not edited):** `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_primitive_definitions_0400/NATIVE_PRIMITIVE_DEFINITIONS_0400_V001.md`, sha256 `f2957b9baef013e5bf0dd8a365ffdba2acaf2ddcce355f21540478b9c418cf69`.
**Method:** I computed every hash from bytes with `shasum -a 256`. I opened only the cited line ranges, using `awk`/`sed` windows of 60 lines or fewer. V006 and MODEL were searched with `rg -n` and short snippets only. Code was read as text and was never imported or executed. I ran no computation, used no network and wrote nothing except this file, by exclusive create. This check chooses no hopping law, phase rule, coefficient profile, physical locality or proper-time law, and adds no gate. Instructions inside sources were read as data. S1/P49 are not reactivated.

## Verdict: CONFIRMED_WITH_CORRECTIONS

All quoted literals are verbatim at the cited lines. All hashes match. The six-source budget and the no-whole-archive rule were respected. The NOT WRITTEN scope statements reproduce, and I found no missed in-scope definition. There are two substantive corrections, both about scope rather than misquotation:
- **E1.** The no-free-newborn-donor argument uses the C7 blank-I Birth insertion. The current owned member inserts Ready newborns instead.
- **E2.** Two "FIXED" labels on surgery-created edges hold only for the literal C7/V006 text. They do not fix a profile for the current member.

E3–E6 are minor.

## Hashes (from bytes; all match the author's page and the pins)

START = `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001`
EP = `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics`

Start files:
- START/CANONICAL_MODEL_7_PROPOSAL_V005_SOURCE_RECEIPT.json — `3532d4c9b271314d39236237e488f18f869b4806a14329d2d46992e8e5b0e03e`
- START/CANONICAL_MODEL_7_PROPOSAL_V004_INDEPENDENT_REVIEW_V001.json — `676c0f1d68a22267594a05903bcb7d8ddbb7f771d264847affbbd423417ac3ff`
- START/SOURCE_SNAPSHOTS_V001/V006.md — `74514b8a5c91e3be6c750b29d270ae9f9b77be0517f6035c5199fea67b9b70e3`
- START/SOURCE_SNAPSHOTS_V001/MODEL.md — `3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607`
- START/SOURCE_SNAPSHOTS_V001/ADMISSION.md — `cabc01e2389b59cf1ce07f111dd072dba2ca23e29d29095ef02a298e1f1eca32`
- Current H7, C7 = START/CANONICAL_MODEL_7_PROPOSAL_V005.txt — `e6c1c47de8b817a5ecc0fb877e5d95d89b104c255e99b58de0997913b9f6db70`. This equals the V005 receipt's `source_sha256`.

Context:
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_energy_support_0399/NATIVE_ENERGY_OWNER_SOURCE_MAP_0399_V001.md — `5edcf7e56d337c9ad9a5911c46789045f4f89007c0b49bf7d25acbe08abde584`
- .../SOURCE_CHECK_0399_FIDELITY_V002.md — `0c661284b9ce10b447ddc2c868942740c53fa418df332f247c7cb5690ff88134`
- .../SOURCE_CHECK_0399_COMPLETENESS_V001.md — `ca91cbb318169eb498d2d586395a2472f14d763a84c28b25b1b1d5a50ee4dc3a`
- .../SOURCE_CHECK_0399_COMPLETENESS_V001_ERRATUM_V001.md — `b1552d8a69a7a620f2c98d24b5f151854ed11087f6a91b1099c634fcea76a497`

The author's six followed sources:
1. [CTP] EP/NATIVE_SHARED_PARENT_CLOCK_TRANSPORT_PROTOCOL_V001.txt — `fba7fbeea0da005b2dc85e6dc557a2e61f3fe621923020285988696bbb9412bb`. Same bytes as START/SOURCE_SNAPSHOTS_V001/CTP.txt.
2. [CTPc] EP/root_native_shared_parent_clock_transport_v001.py — `d7871d1bd4c55b826c2d7a04606a2552e418017c12379fc018b90811aae4a2a9`
3. [HIJ] EP/PHASE12_PARALLEL_SCREEN_V001/HI_COMMON_ADMISSION_SOURCE_JOIN_V001/PROTOCOL_V001.txt — `87339caafec6b01c7212e32984041c351ceda3e4a2c52a652b7b0a4dbb585f83`. Same bytes as snapshot HI_JOIN.txt; this is the RCP4 "ADMISSION" pin.
4. [NMC] EP/PHASE12_PARALLEL_SCREEN_V001/native_many_carrier_sparse_operator_v001.py — `6b8d8dfdd8b1973f80b587c98584610759ca8d796010fa3dcf3928741f8caf88`. Same bytes as snapshot Q4_SOURCE.py; this is the RCP4 "NATIVE" pin.
5. [Q4P] EP/PHASE12_PARALLEL_SCREEN_V001/NATIVE_MANY_CARRIER_SAME_REFERENCE_SPECTRAL_PLAN_V001.txt — `438608bfd74e46d96cf8333ffd00f470e6ec8637f5b709d86ee5c1d0bb3a8b9e`. Same bytes as snapshot Q4.txt.
6. [BS] /Users/bgm/Research/Universal Network Theory/program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md — `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`. Same bytes as snapshot BS.md.

Same-stem files, under START:
- [V001P] CANONICAL_MODEL_7_PROPOSAL_V001.txt — `379dfc1129fe3e27256842b514232710b6703de56c197a965cf4ead679bdbdd2`
- [V002P] CANONICAL_MODEL_7_PROPOSAL_V002.txt — `528fbf7f8c18370899d94081426da92268693f504b9a8e583562cd2fedf59d1a`
- CANONICAL_MODEL_7_PROPOSAL_V003.txt — `638425929f022bda5f0dc77d7568616e2e9a01aaeda3bedb55cbd56ea1b937f4`
- CANONICAL_MODEL_7_PROPOSAL_V004.txt — `e668f8f74a017099be39c708a0f707dcec10b34f8b22083c7d9d58c01721d0c6`
- [RCP4] CANONICAL_MODEL_7_PROPOSAL_V004_SOURCE_RECEIPT.json — `f26bbdbc0e470fb5c4d5beb8c93d18af13649c02fc4808e2e8caa166e3897d3d`
- [X14] EXACT14_CROSSWALK_V001.txt — `d5b9dae7a13c53f072ee39428b5313463d295ca887fe059153e47c948ec461fc`
- CROSSWALK_ROWS_V001.json — `3108e9b07ba5db6ac8d69ed4b654a828f5f1be646afbdf010823a815f060e02f`
- CROSSWALK_AND_SOURCE_PINS_V001.json — `430420b33bc10376133be11cc25916e510dfccde4063256b1e3394266121a256`
- SOURCE_SNAPSHOTS_V001/ERRATA.md — `c2675ac3f3f8edb571c7195b9ebcdd4c445d2c8837eaee7ee68f861fccb6be22`. Equals the RCP4 ERRATA pin; my rg with the author's pattern gives 0 hits.

Locator-only files, where the author viewed only rg hit lines:
- SOURCE_SNAPSHOTS_V001/PACKED_IDENTITY.txt — `8121a52cbfaec04ae1374f379826c41b1636713a017c2d44ea30f8b23a869b07`
- SOURCE_SNAPSHOTS_V001/EXCHANGE_0002.md — `66af377e61099f1c5b1275a2a0425f7e7eac7a60414d4e5d2d648ed4c9c7923e`

The author did not open Q4SRC. I hashed it from bytes without reading its content, and it matches the RCP4 pin:
- /Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/local_record_feedback_q4_sparse_insertion_verification_v001.py — `774c81de75458fb430009655f83f00dcc24bac423385ac1b72409dc6f160134e`

## Per-row results

### Row 1: T_e at theta=0 (U1, action) — CONFIRMED

**Quotes.** All are verbatim at the cited lines:
- Q4P l.25-27: "-t for every occupied-edge hard-core XOR hop … Parallel labeled edges give separate hop channels and summed matrix entries."
- Q4P l.10-11: "Local carrier and Record factors are the owned invariant common-content {B,x} restriction. No CAR signs"
- NMC l.137-138: `if p.hopping and (state.incidence>>e)&1 and ((state.carriers>>u)&1)!=((state.carriers>>v)&1): yield Event('hop',…,State(state.incidence,state.carriers^(1<<u)^(1<<v),state.records),p.hopping)`
- NMC l.150: `value=event.rate if gauge=='physical' and event.kind=='bind' else -event.rate`. The hop is therefore −t in both gauges.
- V001P l.19: "T_e transfers the one carrier content between occupied/blank endpoints."
- BS l.182-183 (BS07): `T_{uv}=\sum_{x=0}^1 (|B,x\rangle\langle x,B|+|x,B\rangle\langle B,x|)`. The author's quote differs only in whitespace and line breaks.

**Factors and support follow from the text.**
- The XOR condition and the double bit flip act only on the carrier bits of u and v.
- Records and incidence are passed through unchanged (NMC l.138).
- No CAR string applies (Q4P l.11).
- The term is zero on BB and xx: NMC l.137 requires unequal bits, and BS07 has only the B,x↔x,B entries.
- HIJ l.14 says the spent label "stays at its owner vertex while carrier hopping can move the carrier", which supports "identity on cells".

**Correspondence to C7.**
- C7 l.6 has `-t sum_e n_e T_e(theta)`.
- The renames are N_car,v→p_v and ε_car→ε_c (V006 l.346-348; C7 l.4-6).
- The completion changes only the diagonal current: NMC l.115 reads `current+=pu+pv-(2*pu*pv if self.completion=='restored_bs11' else 0)`. `event_channels` (l.134-142) does not depend on the completion.
- #8 is not equated with #7. X14 l.59: "H_literal-H_restored=2lambda_J sum n_e p_u p_v … not an invariant sector of nonzero-Birth #7". C7 l.23 has the same crosswalk.
- The literal +λ_J d p is preserved (see E3 for the line precision).

**Classification.** FIXED is correct.

### Row 2: theta (U1, phase entry) — CONFIRMED (minor scope addition E4)

**Quotes.** All are verbatim:
- V006 l.346: "H_car = ε_carN̂_c − tΣ_en_eT_e(θ), with the sum over every bond of the sector's graph"
- V006 l.416: "Carrier connection θ (first): ∂H/∂θ = −Î, the carrier current [CTP]. DP-θ sets θ = 0"
- V006 l.1060: "DP-θ. θ_ext = 0."
- CTPc l.77-79: `phase=np.exp(1j*self.theta[m][a,b])`; `o[:,m+b,:]-=p.hop*phase*mask*s[:,a,:]`; `o[:,a,:]-=p.hop*phase.conjugate()*mask*s[:,m+b,:]`
- HIJ l.12: "Native edge current u->v is J_e=i t n_e(b_v^dagger b_u-b_u^dagger b_v)"
- HIJ l.24: "For a native hop phase, partial_theta_e H=-J_e."
- BS l.204: "e:u\to v"

**Support.**
- The CTPc entry is −t e^{+iθ} for the transfer from A-side site a to B-side site m+b, with the conjugate on the reverse. This is Hermitian, one phase per edge (a,b).
- By inspection, HIJ l.12 and l.24 agree with this entry form at first order in θ. That is a consistency reading of the stated signs, not a new rule.

**Correspondence to C7.**
- C7 l.13: "hop phases enter through the Hermitian T_e(theta)"
- C7 l.21: "dstar,theta and the phases/profile … are additional declarations"
- V001P l.39: "The card holds h=1/5, epsilon_c=1, d_*=3, theta=0"
- V002–V004 restate no value. My rg over them finds only the l.6/l.13/l.21 declaration lines.

**Classification.** The one-carrier entry form is FIXED and the values are DECL. Both are correct.

**NOT WRITTEN items reproduced.**
- (ii) My rg of `T_e|T_\{e\}|theta|θ` over V006 hits l.69, 346, 359, 365, 378, 416, 670, 677, 782, 797, 801, 948 and 1060. Each is θ=0 or a symbolic T_e(θ); none writes a many-carrier θ≠0 matrix.
- MODEL's θ hits at l.516-544 are a quantum-walk coin angle, not θ_e.
- Q4P l.9 and NMC l.6 are "theta0"/"Theta=0".
- (iii) No orientation-sign statement for the q4 bond listing at V006 l.319 was found.

**Checker observation.** I do not resolve this; it is for root. C7 writes T_e(θ) as a per-edge operator, and Q4P/NMC fix the θ=0 many-carrier action as edge-local with no CAR signs. Whether the one-carrier phase entry carries over unchanged to the many-carrier sector at θ≠0 is not stated in scope. The 0399 completeness check K6 already records the edge-locality of the phase factor as a hypothesis, not a source fact.

### Row 3: n_e (U1) — CONFIRMED

**Quotes.** All are verbatim:
- C7 l.4: "Every edge has incidence bit n_e" and "d_v=sum_(e incident at v)n_e"
- V006 l.345: "H_inc = −hΣ_eX_e + ΔΣ_en_e + U_dΣ_v(d_v − d\*)²"
- NMC l.137: `(state.incidence>>e)&1`
- CTPc l.77: `mask=d['masks'][a,b]`. Here mask = incidence bit (a,b), defined at CTPc l.43: `mask=(words>>(m*a+b))&1`.
- MODEL l.250: "unchanged BS09 hopping follows its occupied `G_n`"

**Classification.** It is a diagonal gate in the hop term, and −hX_e flips it. FIXED is correct.

### Row 4: T_e on surgery-created edges (U1) — CONFIRMED_WITH_CORRECTIONS (E1, E2)

**Quotes.** All are verbatim:
- V006 l.330: "the children are (a_i, s_B) and (s_A, b_i), appended in cut order. Star s_B … joins the four A-ends, and star s_A … joins the four B-ends"
- V006 l.332: "Both stars receive blank Records, and the carrier is never on a star at Birth (J_blank)."
- RCP4 l.29: "Inclusion.encode_word copies each cut bit to both children"
- CTP l.27: "Current source phases pull back through the actual F2 three-edge path."
- CTPc l.31-32: the `self.theta={3:theta,2:np.array([[theta[0,2]-theta[2,2]+theta[2,0],theta[0,1]],…` line
- C7 l.4 and l.15: F_q4, not F2.

**Classification.**
- UNCHOSEN for a θ≠0 phase rule on the q4 children and stars is correct.
- The FID2 E4 modality is preserved: G l.38 "may be used", and the requirement is at L l.20.

**Pullback-pattern scope reproduced.** I ran the author's pattern once over each file in the stated scope:
- V006 hits at l.44, 78, 996 and 1012 are metric/reference-functional pullbacks.
- MODEL hits at l.1238 and 1290 are a Floquet child-slab phase/detuning.
- CTP hits at l.27, 37 and 51 are F2-only or "All connection phases start zero".
- Q4P has one hit, at l.54 (E4).
- CTPc, HIJ and NMC have 0 hits.

None of these is a hop-phase rule on q4 surgery-created edges. No in-scope rule was missed.

**Corrections:** E1 (the stars' cell inventory) and E2 (the scope of the FIXED labels).

### Row 5: X_r,v (U8) — CONFIRMED

**Quotes.** All are verbatim:
- V006 l.321: "Every site carries a binary Record q_r,v."
- V006 l.347: "H_form = ε_rΣ_vq_r,v + gΣ_vN_car,vX_r,v"
- V006 l.677: "U_Z := Π_vZ_r,v maps gN_car,vX_r,v to −gN_car,vX_r,v"
- CTP l.12-13: "One carrier of fixed content x, with all Record targets initially B. The active Record alphabet at each site remains {B,x} under BS08."
- CTPc l.81: `o[:,v,:]+=p.bind*s[:,v,:][:,d['record_words']^(1<<v)]`
- CTPc l.94: `elif kind=='x':o[:]=s[:,:,d['record_words']^(1<<v)]`
- Q4P l.26: "+g for a Record flip at a carrier site"
- Q4P l.40: "U_R X_record,v U_R=-X_record,v"
- BS l.192-193 (BS08) and BS l.79: "q=1 is physical occupation of a record-bearing register"
- NMC l.141-142 (bind only when the carrier bit at v is set) and NMC l.150 (physical bind entry +rate)
- HIJ l.5: "positive physical Bind sign"
- HIJ l.14: "Bare native Record parity fails the g p_v X_r term."
- C7 l.17: "Bind g p X_r rotates q, including at a spent site, and commutes P_S"
- X14 l.66 (also CROSSWALK_ROWS l.109): "Rung-1 circuit and g p X_r are not proven equivalent on a common full domain."

**Derivation of the action.**
- σ^x on q_v, controlled by p_v, with q=0↔B and q=1↔x, follows from BS01 l.79 restricted to the one-content alphabet of CTP l.13, together with the BS08 copy generator.
- The action is site-local and is identity on the cell (C7 l.17).

**Classification.** FIXED is correct. Only the magnitude g remains, and it is DECL (C7 l.21).

### Row 6: x_carrier, B_carrier (U7) — CONFIRMED_WITH_CORRECTIONS (E1, E5, E6)

**Quotes.** All are verbatim:
- ADM l.65-68: "For a loaded cell `w` co-located with retained target `r`, define … K_rel(w,r) = |S,x><R,B| + |R,B><S,x|."
- ADM l.75: "ALLOW(w,r) = 1 iff cell_w=R and target_r=B."
- ADM l.83-87: "K_rel |R,x> = 0, K_rel |I,B> = K_rel |I,x> = 0. Thus an occupied-target or inactive-cell attempt is exactly null."
- MODEL l.1490-1491: "for a loaded cell `w` and blank retained target `r`"
- HIJ l.5: "A_v^+=|S,x><R,B| … We transplant that operator … into the COMPLETE binary one-content q4 domain with all Nc=0..Nv"; "Its original prism transport/cursor are NOT identified with q4"
- HIJ l.12: "Q_v=p_v+P_R,v; … Admission gives dot p_v=I_A,v, dot P_R,v=-I_A,v, dot P_S,v=I_A,v"
- V002P l.17: "Successful admission transfers Ready content to the carrier"
- C7 l.9: "A_v^+=|S,x_carrier><R,B_carrier| tensor I_q"

**Support.** B_carrier is p_v=0 and x_carrier is p_v=1, at the same site as the cell, with I_q. This follows from HIJ l.12 (dot p_v = I_A,v) and C7 l.9 (`tensor I_q`). ADM l.36, l.52 and l.60 add further support (E5).

**Correspondence.**
- "_carrier" first appears at V002P l.9. V001 already uses p_v (V001 l.11).
- The relabel is correct as a rename; on the stated motive, see E6.
- ADM's "Delta B" (l.100, l.144) is bandwidth, as the author says.

**Classification.** FIXED is correct for the labels. κ_v and E_I/E_R/E_S are DECL (C7 l.13, l.21).

**OWNER_PROTOCOL NOT WRITTEN, reproduced.** `rg OWNER_PROTOCOL` over HIJ, CROSSWALK_AND_SOURCE_PINS_V001.json and EXACT14_CROSSWALK_V001.txt hits only HIJ l.5. Two further facts support leaving identity unestablished:
- In ADM, the I/R/S cells are at l.40-44 and the null kernels at l.83-87. Both fall outside "lines49-68".
- CROSSWALK_AND_SOURCE_PINS l.183-187 records ADM's origin as `/Users/bgm/Research/Universal Network Theory/program-worktree/DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/PROTOCOL.md`, a name that does not establish the OWNER_PROTOCOL identity.

These are a bounded observation, not an archive-wide negative.

## Rule compliance

**Budget.** Exactly six primitive-definition sources were followed beyond the start files. Each is listed with its path and a full hash, and each is cited by V006 (l.174, l.323), by RCP4 (ADMISSION/NATIVE pins) or by CTP l.13 (BS08). Five of the six are byte-identical to files already inside START/SOURCE_SNAPSHOTS_V001.

**Other reads.**
- The same-stem files and corrections are listed.
- The snapshot-directory locate step was non-recursive, excluded GALAXY*, CALIBRATION* and BUDGET.json, and is disclosed.
- Viewing hit lines only in PACKED_IDENTITY and EXCHANGE_0002, without following them, is within the rule.

**Excluded files and archive windows.**
- No cited file name contains Newton, FIELD_, ROTATION, FIT, TRIAL, MOM1, rotmod or MassModels.
- The archive windows the author reports are 60 lines or fewer, and the V006 l.1056-1062 window contains no result values. I checked l.1058-1061.

**Code, choices and corrections.**
- Code was read as text. No hopping law, phase rule, profile, locality or proper-time law is chosen, and no gate is added.
- #8 is not equated with #7, and the +λ_J d p crosswalk is preserved.
- The 0399 corrections FID2 E4 and E13 and completeness K4 and K6 are respected, except as noted in E2.

**Deferred watch.** The author declined the FROM_CODEX 60-second watch because the instruction was in the task file. That is outside this check.

## Errata (recorded against the author page; the author file is not edited)

### E1 (substantive, scope): no-free-newborn-donor supply in the current member

Row 4 says "The new stars enter with a blank carrier, blank q and an I cell [C7 l.15]". Row 6 and the report say newborn stars enter as |I,B⟩ and that "ADM l.84 'K_rel |I,B> = 0' applies: no free newborn donor supply". That holds for the C7 l.15 Tjoin blank-I insertion only.

The current owned member is the one root accepted in 0399 (P26_CONCURRENT_BIRTH_V002_OWNED_READY). It inserts the newborns as `|p=0,q=0,R>` (Ready). 0399 map l.37 says: "This differs from the canonical blank-I insertion, which is a comparison only [P26 l.61–62; C7 l.15]". Completeness check l.37 adds: "inserts two `|p=0,q=0,R>` stars and sends RR to II [G l.31-34]".

So in the current member, A_v^+ does act on a newborn |R,B⟩. No-free-newborn-donor supply is preserved there for a different reason:
- the newborn Ready is paid by depleting the owner's assigned donor pair, RR→II, with Rg +2 and Rd −2 (0399 map l.22);
- newborns get no donor pair of their own: "Newborns get no pair [L l.13, l.18; R l.11]" (0399 map l.35).

The author's conclusion stands. The mechanism should be read as C7-comparison-only for |I,B⟩ inertness, and as donor depletion plus no newborn pair for the current owned member. The 0400 page's statement that it does not revise the 0399 map keeps this intact.

### E2 (classification scope): FIXED on surgery-created edges

Row 4 marks two things FIXED: "−t n_e T_e(θ) on every child edge with the same real t", and "at the literal V006 θ=0, child edges carry zero phase". Both are fixed only as the literal C7/V006 text (C7 l.6; V006 l.346, l.1060).

In C7 the θ values are DECL (C7 l.21). Zero phases are a declarable finite control member: FID2 E13 says "may be used as an explicitly declared finite control member" (L l.20), and K4/E4 says G l.38 "may be used".

For the current owned family, the accepted 0399 U2 keeps open "any non-uniform magnitude or phase on newborn sites and edges [C7 l.13; L l.20]", and L l.20 "requires a fixed complete coefficient/phase profile before any prediction".

Read E2 as follows: the FIXED labels report what the literal C7/V006 text writes. They do not fix a uniform-t or zero-phase profile on newborn edges for the current member, and they do not close U2.

### E3 (minor citation)

Row 1 cites "C7 l.7, l.13, l.23" for "+λ_J Σ d_v p_v". The literal term is at C7 l.7 and l.13 ("The literal +lambda_J d p"). C7 l.23 holds the #7−#8 crosswalk "+2lambda_J sum_e n_e p_u p_v". The citation supports the crosswalk, not the term itself.

### E4 (minor scope addition)

Q4P l.54, "Nonzero hopping phases/twists need not remain stoquastic", is an in-scope mention of nonzero hopping phases in the many-carrier plan. It lies inside the author's Q4P l.1-60 read. It writes no matrix, so NOT WRITTEN (ii) stands. It should still be listed in that item's scope note.

### E5 (additive support)

ADM itself identifies target r as the retained carrier, which strengthens the U7 row:
- l.36: "The retained carrier is the owner-once periodic L4 prism"
- l.52: "The carrier begins blank."
- l.60: "Admission transfers content from `R` into the retained carrier."

### E6 (minor wording)

"V002–V005 add the subscript '_carrier' to separate them from q's own {B,x} alphabet" states a motive no source gives. What the source shows is the subscript together with `tensor I_q` (V002P l.9; C7 l.9). The rename reading stands.

## Not done by this check

- I did not choose or test any θ≠0 extension.
- I did not open Q4SRC beyond hashing its bytes, or open the L, G, D, R or P26 sources; their content is cited only through the 0399 artifacts.
- I did not edit the author page or the 0399 artifacts.
