# SOURCE CHECK 0399 - completeness, guard support, missing terms - V001

**Role:** distinct checker, not author. I did not write `NATIVE_ENERGY_OWNER_SOURCE_MAP_0399_V001.md` and did not edit it. Lens: COMPLETENESS + GUARD SUPPORT + MISSING TERMS. Read-only on the UNT tree; no code, computation, network or project script. I did not read the sibling fidelity check, to keep this check independent.

**Verdict: CONFIRMED_WITH_CORRECTIONS.** Every primitive Hermitian term of the current owned member, both directions of every off-diagonal term, every forward Birth guard, every reverse image condition and the predecessor-reconnection sum are present. The corrections below are two confirmed line errors, one mis-paraphrased coefficient clause, one misquoted source, missing guard provenance, missing locality qualifiers on two rows, one loose comparison sentence and loose companion bookkeeping. None changes a term, a guard or a projector classification.

## Hashes (shasum -a 256, from bytes, this check)

- Author file `NATIVE_ENERGY_OWNER_SOURCE_MAP_0399_V001.md` - `5edcf7e56d337c9ad9a5911c46789045f4f89007c0b49bf7d25acbe08abde584` (matches the author report)
- Brief 0399 - `e92722fc326ffa12a29304991d16251501a0439c696d0821a4b389f63e25b070` (match)
- [L] `732bc83ec2e599021dcc6533dca54761f9c40979ce7f2a7651a6d19b2f0e97a0`, [G] `8ab3d7a70a02cc55cec8301b5c6c2d880945d7682ccd0c71812feeec00136930`, [D] `cf2b6cc180c0094f4b34ee2185537eff2ed9e7988c678163bf888bad27df0c1d`, [R] `715680458489837d3306bdbb2f05ffb9c56e9fb25fdb5371dafc369743559243` (all match)
- Companions (all match the author's values): LR `cbe54ebb...f9c40`-family as listed by author, i.e. LR `cbe54ebb05b52acd96ed62bddafc48e199853676b273fbf1d542be387f02d9f5`, LR reading `8593e6353ec1e8b897e90208eb5ef4781ab3b356b2ee6c55561984beb32305c6`, GR `0e9725b87cfcab3b6843ce096ab943d7e60616af8d73aca5adf28a216a7eff4c`, GR reading `171b54ab7d66807acd11ba4f1fecf55eadec8edb3288c248848c4be103bf4921`, CC `eebf34cc5d08e2e44c20784398ce7639bb99675b5b23cbe01003800cb7a76316`, DR `fbd9a2945be493378ab3c551f4365042c0f0052826c25d5e7df662862c894ee6`, DR reading `62cbf8d6693795ce32e0feee2b160b7967ebc62f9076be5d423508145e9e67ac`, NDA `3807f0adcc47d20f8611c0216a358ce59a8a787b2d44473096d1820b398f8653`, NDA review `fabd693c410c7fd596b0fba094e804cad490df826891bba066c71198c1238596`, RR `de189193028a2f0b3afa8428623e0e809a36d4720f4069601e473e4a90e9f7fa`, RR reading `c044fccec5ec9864b3aa40639af9b1bd1fc00d5bc0c89f70b834c5aa0df292f6`, G/D/R readings `badd3d86a4df444bb59c4f2abf0ba3b2dc2aa92846ee6d6a294db59ab6a4224f` / `f5b34c90db28c44a24afdf305bb3b284f19ce0004f0a1e400018a6c2e113713d` / `ac8f8f21d0050b0287d6a768da56611bb8b0186fd2bb4a65aed9e8d703aa08d2`
- Same-stem readings the author did not list (read here; no correction content): CC reading `584f066538792f1afe993bdda1b1b23f23c31c98efed6e8ab6e764864182e293`, NDA reading `d0cac85921634a4bbfb6d72a5ff3c89436cec0829d64961011a786b904f8a7f9`, NDA-review reading `53a217c971309f2cbfc05c68a14d5589e9201ad6f8cef4417bd6958ca22da286`
- Primitives: C7 `e6c1c47de8b817a5ecc0fb877e5d95d89b104c255e99b58de0997913b9f6db70`, P26 `103c95d56a3e7897784bfed96d1651a3e09acd83626f2ae5919d17945aa38462`, CL `388621c0ed2b5929ab097a77fa0ba8da576cbbfe4d682840080679671bf7af53`, CLR `dbce5e62c7bee2b74ceeffb5f36fef9e63d2c1c99e91c02243b58df3096c12f5` (all match)

Companion search was a single same-stem filename listing under UPC. No `_V002`, `_CORRECTION` or `_ERRATA` file exists for L, G, D or R. The mandatory companions are CC (named by GR) and NDA (named by DR). Both are applied correctly: all-matchings appears only as a comparison, and the donor row does not claim that native theory has no local donor operator (DR l.13).

## Independent enumeration (from sources only)

`H_own = D_native + H_donor + T_own + T_own†` [L l.16], plus one identity offset common to ALL sectors [G l.38; P26 l.116-117; R l.9]. D_native is the literal H7+Hcell+HA on every (S,G) [L l.20; G l.38], with these terms:

1. `-h X_e`
2. `Delta n_e`
3. `Ud(d_v-dstar)^2`
4. `epsilon_c Nc`
5. `-t n_e T_e(theta)`, Hermitian, with both hop directions [C7 l.13; G l.38]
6. `epsilon_r q_v`
7. `g p_v X_r,v`
8. `-lambda_R d_v q_v`
9. `+lambda_J d_v p_v`
10. `E_I P_I + E_R P_R + E_S P_S`
11. `kappa_v A_v^+`
12. `conj(kappa_v) A_v^-`

These come from C7 l.5-10. The remaining terms are:
- **H_donor:** `e_I P_ID + e_R P_RD` on the 2V0 donor factors [P26 l.53; L l.20].
- **T_own:** forward guards are C in C_loc(G), o_j in W_G(C), j notin S, cut census 2 and donor pair (2j,2j+1)=RR [L l.13-15]. The action copies the cut bits, inserts two `|p=0,q=0,R>` stars and sends RR to II [G l.31-34].
- **T_own†:** sums over at most 24 predecessor pairings [R l.15; G l.57]. Each pairing is zero unless:
  - child pairs are equal and the census is 2;
  - the newborns are p=q=0 and R;
  - the pair is II and slot j is active;
  - no restored edge duplicates an existing edge;
  - o_j witnesses the restored cut in the PREDECESSOR graph [G l.36; R l.15; RR l.9; D l.61].

**Comparison result:** all 16 items, every forward guard and every reverse condition appear in the author's rows 1-9 or the Birth sub-table. No term, Hermitian-conjugate branch, guard or predecessor reconnection is missing.

## Corrections (author file not edited; carry forward)

- **K1 (author-reported, confirmed).** Carrier-hopping row: C7 l.5 should be **C7 l.6**. Line 6 holds `-t sum_e n_e T_e(theta)`.
- **K2 (author-reported, confirmed).** Newborn-existence row: G l.43 should be **G l.42**. Line 42 holds `sum_(j notin S)`, and line 43 is `H=D+T+T†`. The co-cited G l.27 already supports the row.
- **K3. Owned Birth row, column (a).** "with one complex epsilon per channel" misreads the source, because it suggests a separate epsilon for each channel.
  - G l.40 says: "ONE complex epsilon, identical for each channel". L l.15 displays a single epsilon.
  - G l.47 says: "Uniform epsilon per matching AND available donor slot is a NEW amplitude convention."
  - Correct reading: one complex epsilon common to all channels. Any channel-dependent profile is an undeclared family choice [L l.20; P26 l.139 D5].
- **K4. U1 misquotes G l.38.** The source permits; it does not require: "Uniform native coefficients and a fixed declared hopping phase rule may be used". The requirement is in L l.20: "The parameterized family requires a fixed complete coefficient/phase profile before any prediction."
- **K5. Guard provenance is missing from rows 8-9 and the sub-table.** The two guards that give Birth its radius-2 support are counted declared postulates, not native law.
  - L l.28: "CB-LOC-01 — DECLARED WORKING POSTULATE: admissible concurrent cuts are precisely C_loc(G) ... these theorems do not establish physical metric locality."
  - L l.30: "CB-OWN-01 — DECLARED WORKING POSTULATE: resource access is the owner/witness rule above, with the actual RR predicate".
  - LR l.17: the review "does not certify those tests or retire either clause."
  - Column (e) of rows 8-9 should carry these labels.
- **K6. Locality qualifiers are missing from rows 3 and 5-6, column (e).** Row 1 carries R l.9's profile hypothesis; rows 3 and 5-6 assert "Edge-local" or "Site-local" without it.
  - R l.9: "More general bounded profiles must depend only on the affected stable labels/current local factors; no remote-graph/subset, total-count or outcome-dependent coefficient is permitted in this proof."
  - **Hopping (row 3):** the operator form and the phase rule are not found (U1). Edge-locality of the phase factor is therefore a proof hypothesis, not a source fact. R l.27 ("at most one carrier transfer") and R l.33 ("Native assigned owners have radius at most one") hold only inside R's hypotheses.
  - **Admission (rows 5-6) and Bind (row 4):** the operator form is explicitly site-local [C7 l.6, l.9]. The coefficient profile is not fixed by the source; C7 l.13 says: "Uniform kappa versus a spatial magnitude/phase profile is a declaration".
- **K7. Row 3 does not show the reverse hop branch (minor).** It should cite G l.38, "both admission/hopping directions", together with C7 l.13 "Hermitian T_e(theta)".
- **K8. The comparison paragraph mis-scopes alternative A.** A uses the C_loc cut class; D l.7 says: "with candidate C_loc and its deduplicated witness-root set". Its non-locality is in resource access ("distinguishable globally accessible channels", D l.73), not in where the cut is. Only all-matchings lacks cut-location locality (G l.11: "supplies no graph-distance locality").
- **K9. Companion bookkeeping is loose (documentary only).** "Every one is PASS_SCOPED" is not accurate:
  - CC is a scope companion and NDA is a source audit (DR l.13: "source scope, not a correction to the target"). Neither carries a PASS verdict.
  - GR's reading status is `PASS_SCOPED_WITH_MANDATORY_CUT_CLASS_COMPANION`, and the NDA review's verdict is `PASS_SCOPED_SOURCE_APPLICABILITY`.
  - Three reading JSONs are unlisted; their hashes are given above.

## Answers to the check questions

- **Missing or mis-scoped items.** No term, guard, conjugate branch, reconnection or companion correction is missing. The mis-scopes are K3, K5, K6 and K8.
- **Projector classification.** None is misclassified. Rows 1-6 are block-diagonal over (S,G) [G l.38]. In rows 8-9, (S,G) is a block label. The only G-dependence is the witness, census and donor tests, which act within radius 2 of group j row by row [R l.33; RR l.9]. L l.38 says "Changes confined to unrelated distant donor factors cannot supply that channel", and D l.67 says "No factor of the total distant donor stock appears." Nothing in the current member is a global predicate:
  - Simplicity and degree four are preserved by construction [G l.27] and need no projector.
  - The duplicate-edge reverse test is local.
  - The component count is an invariant sector, not a term predicate [CLR l.9].
  - The author correctly calls alternative B's `(K-|S|)^(-1/2)` a global-count coefficient [D l.43, l.53].
- **Locality asserted where the source is ambiguous.** Yes, mildly: K5 and K6. The author's U3 and U4 already state that locality is row-wise and set by labels, which limits the impact.
- **Boundary.** The author stayed within L/G/D/R, their same-stem companions, the named mandatory companions CC and NDA, the cited primitives C7, P26 and CL, and CLR, the review of the primitive CL, which is bounded and harmless.
  - No archive instruction was followed. The C7 V005 appendix directives (S1, P-49) and NDA's LOCAL_RECORD_FEEDBACK files were not opened or acted on.
  - The aborted grep produced nothing, and nothing from it is used.
  - The file contains no proper-time adoption, physical partition, equal-weight rule, energy-density law or covariance claim (author l.4, l.40-46).

## Additions to "Unresolved factor support"

- **U9: Birth-amplitude profile.** Only a single displayed epsilon is given [L l.15; G l.40]. Its magnitude, phase and any (C,j), orientation or witness-multiplicity dependence are undeclared [L l.20; P26 l.139]. G l.47 marks uniform per-channel epsilon as a NEW convention. Radius-bounded dependence holds only under R l.9.
- **U10: Guard provenance.** The C_loc occurrence guard (CB-LOC-01) and the owner/witness/RR access guard (CB-OWN-01) are declared working postulates whose retirement tests are unmet [L l.28-30, l.36-40; LR l.17]. Their radius-2 support is combinatorial: "only combinatorial adjacency, not physical locality" [D l.69].
- **U4 extension (clarification).** "Radius two" in R l.33 and RR l.9 is measured in the label-defined group-adjacency graph [R l.17]. Group j bundles o_j with a_j and b_j, and other owners' rewrites can move a_j and b_j. The sources therefore give no vertex-distance bound between o_j and its newborns: "these vertices need not form a physically local subsystem" [RR l.7].
- **Scope note (not a support gap).** Inserting newborns with blank q=0 and p=0 is literal source content [P26 l.61-62]. Its compatibility with the S1 Record-filled premise is open. C7 l.32 says the rules "insert blank q/I factors in the finite Birth lift; the physical admissibility and dynamical compatibility of the S1 class therefore require an explicit dictionary"; see also LR l.11.
- **Filename-level flag (not read; outside the companion rule).** `UPC/helpers/response_packet_audit/OWNED_READY_PERSISTENT_NEWBORN_DONOR_CURRENT_CONTINUITY_PROPOSED_V001.md` and its distinct review, `UPC/helpers/coefficient_method/OWNED_READY_PERSISTENT_NEWBORN_DONOR_CONTINUITY_DISTINCT_REVIEW_V001.md`, sit beside the sources. They are not same-stem and are not named by L, G, D or R. Their filename marks them PROPOSED, so "newborns get no pair" [L l.18; R l.11] stands for the listed member. If root has adopted any newborn-donor change, rows 8-9 and U5 would need rechecking.

**Not checked here:** the author's 0397 range addendum (`USAGE_CONTRACT_0397_V002_RANGE_ADDENDUM_V001.md`), which is outside this lens.
