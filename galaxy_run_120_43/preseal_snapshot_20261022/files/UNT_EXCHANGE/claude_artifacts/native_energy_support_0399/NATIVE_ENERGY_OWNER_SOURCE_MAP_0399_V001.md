# Native energy-owner source map 0399 V001

**Author role:** Claude helper, AUTHOR for UNT 0399. I am not the source checker, and the checker must be a different agent. **Task:** `FROM_CODEX/0399_2026-10-15_native_energy_owner_support_source_map.md`, sha256 `e92722fc326ffa12a29304991d16251501a0439c696d0821a4b389f63e25b070`. **Sources:** every sha256 was verified from bytes before reading (full list at the end): [L] `732bc83e…`, [G] `8ab3d7a7…`, [D] `cf2b6cc1…`, [R] `71568045…`.
**Status: SOURCE EXTRACTION ONLY.** This is not an adoption. It does not propose a physical partition, an equal-weight rule, an energy-density law or a covariance claim. The principal's proper-time proposal is NOT adopted, and it is not used here.

**The model extracted.** This is the CURRENT owned member, P26_CONCURRENT_BIRTH_V002_OWNED_READY [L l.3, l.11–20]. Its Hamiltonian is `H_own=D_native+H_donor+T_own+T_own†` [L l.16]. It acts on `H_K^graph = direct_sum_(S,G) H_native(G) tensor H_donors` [G l.17].
- K = V0.
- Each original vertex o_j has one donor pair (2j,2j+1) and one potential newborn pair (a_j,b_j) [L l.13; R l.7; G l.15].
- **E** means existence: the vertex, edge, active slot or resource register is present.
- **O** means occupation: incidence n_e, carrier p, record q, cell I/R/S, or donor I_D/R_D.
- Line numbers refer to `cat -n` lines. The sources write one paragraph per line.

| Term | (a) Operator / coefficient as specified | (b) Source | (c) What it CHANGES | (d) What it QUERIES (guards) | (e) Whole-graph projector |
|---|---|---|---|---|---|
| Native diagonal | `Delta sum_e n_e + Ud sum_v(d_v-dstar)^2 + epsilon_c Nc + epsilon_r sum_v q_v - lambda_R sum_v d_v q_v + lambda_J sum_v d_v p_v`; `Hcell=sum_v(E_I P_I,v+E_R P_R,v+E_S P_S,v)`; "all constants" retained | C7 l.5–8, l.13. Applies on every G [G l.38; L l.20] | Nothing | O: n_e; `d_v=sum_(e incident at v)n_e`; p_v; q_v; the cell of v. E: which edges are incident at v | SECTOR INDEX. It is block-diagonal over (S,G) [G l.38]. It reads only edges at v (radius ≤1 [R l.33]), under the local/uniform profile hypothesis [R l.9] |
| Incidence flip | `-h sum_e X_e` | C7 l.5 | O: n_e of one existing edge, and through it d_u and d_v. E: none, because edge existence is the sector label | E: e∈E(G). No occupation guard | SECTOR INDEX. Edge-local |
| Carrier hopping | `-t sum_e n_e T_e(theta)`; "hop phases enter through the Hermitian T_e(theta)" | C7 l.5, l.13. "occupied-edge carrier hopping" [L l.20] | O: the carrier p at the endpoints of e. The source says "at most one carrier transfer" [R l.27]. Nc does not change [P26 l.88] | O: n_e (the n_e factor); the endpoint hard-core p [C7 l.4]. E: e∈E(G) | SECTOR INDEX. Edge-local. The explicit T_e is NOT FOUND (U1) |
| Bind | `g sum_v p_v X_r,v`; "Bind g p X_r rotates q, including at a spent site, and commutes P_S" | C7 l.6, l.17 | O: q_v | O: p_v. It does not test the cell | SECTOR INDEX. Site-local |
| Admission | `kappa_v A_v^+`, with `A_v^+=\|S,x_carrier><R,B_carrier\| tensor I_q` | C7 l.9–10, l.17 | O at v: cell R→S and carrier B→x. Nc +1, Rg −1, Sg +1 [P26 l.84]. q is untouched | O: cell = R and carrier = B at v | SECTOR INDEX. Site-local. The kappa_v profile is undeclared; uniform kappa is allowed only as a control member [L l.20] |
| Admission reverse | `conj(kappa_v) A_v^-`, with `A_v^-=(A_v^+)dagger`. "both admission directions" [L l.20] | C7 l.9–10 | O at v: cell S→R and carrier x→B. Nc −1, Rg +1, Sg −1 [P26 l.85] | O: cell = S and carrier = x | SECTOR INDEX. Site-local |
| Donor energy | `HD=sum_(j=0..2K-1)[e_I P_ID,j + e_R P_RD,j]`; "H_donor retains both e_R and e_I" | P26 l.52–53; L l.20 | Nothing | O: each donor factor (I_D or R_D). E: donor factors exist in every summand [G l.19]. They carry no carrier or q, and have no hopping or reset [P26 l.41, l.56; D l.11] | NO GRAPH PROJECTOR. It is the identity on every (S,G) and acts only on donor tensor factors. The old native-record donor `T=F2 b_w` is a different law and is not substituted for it [NDA l.13; L l.7] |
| Owned Birth | `T_own=epsilon sum_(G,C,j) 1_{o_j in W_G(C)} B_(G,C,j)`, with one complex epsilon per channel | L l.13–15; G l.29–34, l.40–43; D l.59 | E: slot j becomes active, so a_j and b_j exist; the 4 cut edges are deleted; 8 star edges are created. O: the child bits are copied; the newborns get p=q=0 and cell R; the donor pair goes RR→II (Rg +2, Rd −2) | j∉S; C∈C_loc(G) with o_j∈W_G(C); `sum_(e in C)n_e=2`; donor pair (2j,2j+1) = R_D,R_D. It does NOT test old cell or record content [G l.36] | SECTOR INDEX between blocks, (S,G)→(S∪{j},G') [G l.29]. The guards are current-adjacency and resource predicates within radius 2 of group j [R l.33; CL l.9]. The owned law contains no global count |
| Owned un-Birth | `T_own†`: the literal adjoint `epsilon* B_(G,C,j)†`, summed over ALL valid predecessor channels | L l.13; G l.36, l.57; R l.15 | E: a_j and b_j are removed, which frees slot j for reuse [G l.21]; the 8 star edges are deleted; the 4 cut edges are restored. O: each restored bit takes the common child bit; the donor pair goes II→RR (Rg −2, Rd +2) | The image test and the predecessor witness test (sub-table below) | SECTOR INDEX. The tests stay within radius 2 of group j [R l.33; RR l.9]. The owner test is applied to the PREDECESSOR graph, never as a fresh test on the target [L l.13; D l.61] |

**Common identity offset.** An offset is allowed only if it is common to ALL graph and donor sectors [G l.38; P26 l.116–117; R l.9]. It is a global constant, not a predicate.

**Birth contact.** The basis-diagonal Birth contact `2Delta+2Ud(2-dstar)^2+2E_R+2(e_I-e_R)` [G l.68; P26 l.110] is a matrix-element comparison. It is not an operator, and it is not a local energy assignment.

**Birth and its reverse: retained conditions**

| Item | Forward B_(G,C,j) | Reverse B_(G,C,j)†, for each predecessor channel |
|---|---|---|
| Cut endpoints | C is an unordered four-edge matching with 4 distinct A and 4 distinct B endpoints. The surgery removes C, joins each A endpoint to b_j, and joins a_j to each B endpoint [G l.7, l.27] | The 4 A neighbours of b_j and the 4 B neighbours of a_j in the target [R l.15] |
| Root/witness test | For a root a in A, its four B neighbours are exactly the cut's B endpoints, and exactly one cut edge meets a. B roots are the mirror case. Witnesses are deduplicated over roots and orientations [CL l.7; L l.13]. The gate is `1_{o_j in W_G(C)}`, and each (C,j) is counted once [R l.7; D l.61] | "missing witness membership" gives zero. The same ownership condition is applied to the predecessor graph [R l.15; D l.61] |
| Donor ownership | Pair j is owned by the original vertex o_j. Newborns get no pair [L l.13, l.18; R l.11] | The assigned pair must be I_D,I_D [G l.36; P26 l.74–75] |
| Newborn existence | Requires j∉S, that is, a_j and b_j are absent [G l.27, l.43] | Requires slot j to be active. The reverse removes a_j and b_j |
| Copy / blank / image | Each removed bit is copied into both of its children. Every old site factor and every uncut bit is kept. The newborns are inserted as `\|p=0,q=0,R>` (Ready). This differs from the canonical blank-I insertion, which is a comparison only [P26 l.61–62; C7 l.15] | Each pair of child bits must be equal; the census must be two; the newborns must be Ready with p=q=0; the donors must be depleted. On failure the term gives zero, and the input stays a full domain state [G l.36; GR l.7; P26 l.74–75] |
| Predecessor reconnections | Not applicable: the surgery discards the old A–B pairing [G l.57] | At most 4! = 24 pairings per owner. Each pairing fixes the predecessor graph, the copied word and the donor/internal state. A pairing gives zero if it creates a duplicate old edge, fails the witness test, has unequal child bits or non-blank newborns. T† sums every valid channel. It is not "reverse last event". The sum need not be a partial isometry [G l.57; R l.15; GR l.9] |

**BOOKKEEPING, NOT PHYSICAL.** The rewrite-bound proof writes `H=sum_j H_j` plus the common identity [R l.19]. It allocates the terms as follows:
- site diagonal, Bind and admission go to the group of their site;
- each edge flip and hop goes to the group of its A endpoint;
- donor energy and `T_j+T_j†` go to j;
- the diagonal is split by `Delta sum_e n_e=(Delta/2)sum_v d_v`.

Group j is the original vertex j, its two potential newborns and its donor pair. The source calls it "only a combinatorial dependency device, not physical space" [R l.17; RR l.7]. The allocation exists to bound row sums (D_site and A, [R l.21–25]). It is not a physical energy-density law, a partition, an equal-weight rule or an input to proper time.

**Comparison members that are not current.** The all-matchings T [G l.42] and the all-to-all alternative A [D l.17] have no graph-distance locality. Alternative B uses `(K-|S|)^(-1/2)` and R_D/R_U [D l.33–45]. These are ACTUAL global predicates, depending on the total active count or the reservoir number. B is rejected as the shared route [L l.3].

## Unresolved factor support

- **U1 — T_e(theta).** Its explicit matrix, the carrier factors it acts on, and the phase rule on edges created by surgery are all NOT FOUND. I looked in C7 l.4–13, P26 §2, G l.38, L l.20 and R §2. G l.38 requires "a fixed declared hopping phase rule". Zero phases are licensed only as a control member [L l.20].
- **U2 — Coefficient profiles.** kappa_v and any non-uniform magnitude or phase on newborn sites and edges are unspecified [C7 l.13; L l.20]. Radius-bounded dependence holds only under the proof hypothesis that profiles "depend only on the affected stable labels/current local factors" [R l.9].
- **U3 — Adjacency.** Adjacency is a direct-sum label, not a tensor factor [G l.17, l.21]. No source gives a fixed-subsystem support for "e∈E(G)" or for Birth. Locality holds only row-wise on basis configurations. The sources explicitly deny commutator locality by fixed labels [R l.31].
- **U4 — Group j.** Group j is defined by labels, not by adjacency. Its vertices "need not form a physically local subsystem" [RR l.7]. As a result, H_j has no stated spatial support.
- **U5 — Donor register.** The donor register has no graph site. Its only tie to the graph is ownership by o_j, which the source calls "only combinatorial adjacency, not physical locality" [D l.69]. Its meaning and supply are undeclared (P26 D1, l.135). Where e_I and e_R reside is therefore unresolved.
- **U6 — Allocation conventions.** Allocating each edge to its A endpoint and splitting Delta by half the degree are conventions of the proof [R l.19]. No source selects a physical allocation.
- **U7 — Carrier labels.** `x_carrier` and `B_carrier` are not defined verbatim. Reading x as occupied rests on "Admission changes Nc and Nready oppositely" [C7 l.15] and on P26 l.84.
- **U8 — Bind operator.** `X_r,v` is described only as "rotates q" [C7 l.17]. Its explicit operator is not written in the sources I read.

## Source citations

All sha256 values below were computed from bytes with `shasum -a 256`. UPC = `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13`, and NCA = `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001`.

**Primary sources**
- [L] UPC/CODEX1/READINESS_OWNED_READY_FALLBACK_ADOPTION_AND_POSTULATE_LEDGER_V001.md — `732bc83ec2e599021dcc6533dca54761f9c40979ce7f2a7651a6d19b2f0e97a0`
- [G] UPC/helpers/coefficient_method/CURRENT_GRAPH_ALL_MATCHING_LOADED_BIRTH_GENERATOR_PROPOSED_V001.md — `8ab3d7a70a02cc55cec8301b5c6c2d880945d7682ccd0c71812feeec00136930`
- [D] UPC/helpers/coefficient_method/CURRENT_GRAPH_CONCURRENT_BIRTH_DONOR_CHANNEL_ALTERNATIVES_PROPOSED_V001.md — `cf2b6cc180c0094f4b34ee2185537eff2ed9e7988c678163bf888bad27df0c1d`
- [R] UPC/helpers/coefficient_method/OWNED_READY_CURRENT_GRAPH_LOCAL_REWRITE_BOUND_AND_NATIVE_CLOCK_WINDOW_PROPOSED_V001.md — `715680458489837d3306bdbb2f05ffb9c56e9fb25fdb5371dafc369743559243`

**Correction companions read and applied.** Every one is PASS_SCOPED, and none contains a mandatory correction.
- [LR] UPC/helpers/recovered_packet_audit/OWNED_READY_FALLBACK_ADOPTION_POSTULATE_LEDGER_DISTINCT_REVIEW_V001.md — `cbe54ebb05b52acd96ed62bddafc48e199853676b273fbf1d542be387f02d9f5`. Its `_READING.json` — `8593e6353ec1e8b897e90208eb5ef4781ab3b356b2ee6c55561984beb32305c6`
- [GR] UPC/helpers/response_packet_audit/CURRENT_GRAPH_LOADED_BIRTH_GENERATOR_AND_CUT_CLASS_DISTINCT_REVIEW_V001.md — `0e9725b87cfcab3b6843ce096ab943d7e60616af8d73aca5adf28a216a7eff4c`. Its `_READING_V001.json` — `171b54ab7d66807acd11ba4f1fecf55eadec8edb3288c248848c4be103bf4921`
- [CC] UPC/helpers/coefficient_method/CURRENT_GRAPH_BIRTH_CUT_CLASS_PARAMETERIZATION_SCOPE_COMPANION_V001.md — `eebf34cc5d08e2e44c20784398ce7639bb99675b5b23cbe01003800cb7a76316`. This is GR's mandatory companion. I applied it: all-matchings is only an example, and the cut class comes from C(G) = C_loc per [L].
- [DR] UPC/helpers/recovered_packet_audit/CURRENT_GRAPH_CONCURRENT_BIRTH_DONOR_ALTERNATIVES_DISTINCT_REVIEW_V001.md — `fbd9a2945be493378ab3c551f4365042c0f0052826c25d5e7df662862c894ee6`. Its `_READING.json` — `62cbf8d6693795ce32e0feee2b160b7967ebc62f9076be5d423508145e9e67ac`
- [NDA] UPC/helpers/recovered_packet_audit/NATIVE_DONOR_ASSIGNMENT_SOURCE_RECOVERY_AND_CONCURRENT_APPLICABILITY_V001.md — `3807f0adcc47d20f8611c0216a358ce59a8a787b2d44473096d1820b398f8653`. This is DR's mandatory companion, and I applied it in the donor row. Its review, UPC/helpers/coefficient_method/NATIVE_DONOR_SOURCE_RECOVERY_CONCURRENT_APPLICABILITY_DISTINCT_REVIEW_V001.md — `fabd693c410c7fd596b0fba094e804cad490df826891bba066c71198c1238596`
- [RR] UPC/helpers/response_packet_audit/OWNED_READY_DYNAMIC_GRAPH_REWRITE_BOUND_DISTINCT_REVIEW_V001.md — `de189193028a2f0b3afa8428623e0e809a36d4720f4069601e473e4a90e9f7fa`. Its `_READING.json` — `c044fccec5ec9864b3aa40639af9b1bd1fc00d5bc0c89f70b834c5aa0df292f6`
- Same-stem reading files:
  - G: `CURRENT_GRAPH_ALL_MATCHING_LOADED_BIRTH_GENERATOR_V001_READING.json` — `badd3d86a4df444bb59c4f2abf0ba3b2dc2aa92846ee6d6a294db59ab6a4224f`
  - D: `CURRENT_GRAPH_CONCURRENT_BIRTH_DONOR_CHANNEL_ALTERNATIVES_V001_READING.json` — `f5b34c90db28c44a24afdf305bb3b284f19ce0004f0a1e400018a6c2e113713d`
  - R: `OWNED_READY_CURRENT_GRAPH_LOCAL_REWRITE_BOUND_AND_NATIVE_CLOCK_WINDOW_V001_READING.json` — `ac8f8f21d0050b0287d6a768da56611bb8b0186fd2bb4a65aed9e8d703aa08d2`

**Directly needed primitive definitions.** These are cited by the sources and were read for definitions only. No instruction in them was followed.
- [CL] UPC/CODEX1/READINESS_CURRENT_GRAPH_ROOT_NEIGHBOR_MATCHING_AND_SCALING_PROPOSED_V001.md — `388621c0ed2b5929ab097a77fa0ba8da576cbbfe4d682840080679671bf7af53`. Its review [CLR] UPC/helpers/recovered_packet_audit/CURRENT_GRAPH_ROOT_NEIGHBOR_MATCHING_AND_SCALING_DISTINCT_REVIEW_V001.md — `dbce5e62c7bee2b74ceeffb5f36fef9e63d2c1c99e91c02243b58df3096c12f5`. CLR l.9 shows that Birth preserves the number of connected components. That is a global invariant sector; it is not a predicate inside any term.
- [P26] NCA/EXTERNAL_CODEX3_RECORD_ACCUMULATION_PROTOCOL_V001/P26_REPEATED_BIRTH_READY_LOADING_DRAFT_V001.txt — `103c95d56a3e7897784bfed96d1651a3e09acd83626f2ae5919d17945aa38462`
- [C7] NCA/CANONICAL_V006_SELECTION_AND_EXACT14_CROSSWALK_V001/CANONICAL_MODEL_7_PROPOSAL_V005.txt — `e6c1c47de8b817a5ecc0fb877e5d95d89b104c255e99b58de0997913b9f6db70`. It defines H7, Hcell, A_v^± and HA.
