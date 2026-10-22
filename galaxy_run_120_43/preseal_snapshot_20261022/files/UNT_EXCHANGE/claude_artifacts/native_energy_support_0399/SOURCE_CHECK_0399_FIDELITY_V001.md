# Source check 0399: row-by-row fidelity V001

**Role:** distinct checker, not author. I did not write the source map I checked. I wrote only this file, by exclusive create. I left the author file and the UNT tree untouched (read-only), ran no code, computation or network, and adopted none of the following: the proper-time proposal, a partition, an equal-weight rule, an energy-density law or a covariance claim.

**Target:** `NATIVE_ENERGY_OWNER_SOURCE_MAP_0399_V001.md`. The sha256 computed from bytes, `5edcf7e56d337c9ad9a5911c46789045f4f89007c0b49bf7d25acbe08abde584`, matches the author's report.

**Verdict: CONFIRMED_WITH_CORRECTIONS.**
- The term inventory is complete: every H7 term, Hcell, both HA directions, HD, T_own and T_own†.
- All operator strings match except one symbol.
- Existence and occupation are kept apart.
- Every Birth/reverse condition is present.
- H_j is correctly treated as bookkeeping.
- No adoption, partition, equal-weight or covariance language appears; lines 4 and 46 are negations.
- Four statements need substantive correction (E3–E6), and several citations need repair.
- The author file is not edited; the corrections below are errata to it.

## Hashes verified from bytes (shasum -a 256)

**Task and primary sources**
- Task `FROM_CODEX/0399_…source_map.md` — `e92722fc…5e070`
- [L] — `732bc83e…e0f97a0`
- [G] — `8ab3d7a7…0136930`
- [D] — `cf2b6cc1…62c0d1d`
- [R] — `71568045…59243`

All match the brief. Primary sources were checked before reading.

**Companions:** all hashes the author lists are reproduced exactly.
- LR — `cbe54ebb…`, with its READING — `8593e635…`
- GR — `0e9725b8…`, with its READING — `171b54ab…`
- CC — `eebf34cc…`
- DR — `fbd9a294…`, with its READING — `62cbf8d6…`
- NDA — `3807f0ad…`
- NDA review — `fabd693c…`
- RR — `de189193…`, with its READING — `c044fcce…`
- Same-stem readings for G, D and R — `badd3d86…`, `f5b34c90…`, `ac8f8f21…`

**Primitives:** all match.
- C7 — `e6c1c47d…`
- P26 — `103c95d5…`
- CL — `388621c0…`
- CLR — `dbce5e62…`

**Same-stem READING files the author did not list.** I read all three; none carries a correction.
- `CURRENT_GRAPH_BIRTH_CUT_CLASS_PARAMETERIZATION_SCOPE_COMPANION_V001_READING.json` — `584f066538792f1afe993bdda1b1b23f23c31c98efed6e8ab6e764864182e293`
- `NATIVE_DONOR_ASSIGNMENT_SOURCE_RECOVERY_AND_CONCURRENT_APPLICABILITY_V001_READING.json` — `d0cac85921634a4bbfb6d72a5ff3c89436cec0829d64961011a786b904f8a7f9`
- `NATIVE_DONOR_SOURCE_RECOVERY_CONCURRENT_APPLICABILITY_DISTINCT_REVIEW_V001_READING.json` — `53a217c971309f2cbfc05c68a14d5589e9201ad6f8cef4417bd6958ca22da286`

**Companion rule.** I listed the files under UPC by the four stems. No `*_CORRECTION*` or `*_ERRATA*` file and no V002 exists for any of the four stems, so the companion set above is complete.
- GR's binding companion is CC (GR READING status `PASS_SCOPED_WITH_MANDATORY_CUT_CLASS_COMPANION`). The author applied it correctly: C(G)=C_loc, and all-matchings is only an example (CC l.3, l.5).
- DR's "Mandatory integration companion" is NDA (DR l.13), and the author applied it in the donor row.
- Not every companion carries a PASS_SCOPED verdict, as the author file says. NDA is a source audit with no verdict, CC is a scope companion, and the NDA review's verdict is `PASS_SCOPED_SOURCE_APPLICABILITY`. This mislabelling is minor and does not change the result.

## Per-row results (main table)

1. **Native diagonal — CONFIRMED.**
   - The six diagonal H7 terms are extracted exactly from C7 l.5–7: "Delta sum_e n_e+Ud sum_v(d_v-dstar)^2+epsilon_c Nc", "+epsilon_r sum_v q_v", "-lambda_R sum_v d_v q_v+lambda_J sum_v d_v p_v".
   - Hcell matches C7 l.8, and C7 l.13 says "all constants … are retained".
   - G l.38 is the anchor that it applies on every G: "direct sum of the literal native H7+Hcell+Hadmission on EACH G".
   - R l.33 supports the radius: "Native assigned owners have radius at most one."
   - It changes nothing, it queries O and E correctly, and the sector-index reading is correct.
2. **Incidence flip — CONFIRMED.** C7 l.5: "H7=-h sum_e X_e". It changes n_e only, and edge existence is the sector label.
3. **Carrier hopping — CONFIRMED_WITH_CORRECTION (E1).**
   - The operator is on C7 **l.6** ("-t sum_e n_e T_e(theta)+epsilon_r sum_v q_v…"), not l.5.
   - The other citations are verified:
     - C7 l.13: "hop phases enter through the Hermitian T_e(theta)"
     - L l.20: "occupied-edge carrier hopping"
     - R l.27: "at most one carrier transfer"
     - P26 l.88: "Bind / native transport 0 0 0 0"
     - C7 l.4: "hard-core carrier p_v"
   - Because T_e is not given (U1), the hard-core guard is an inference, and the row presents it as one.
4. **Bind — CONFIRMED.**
   - C7 l.6: "g sum_v p_v X_r,v"
   - C7 l.17: "Bind g p X_r rotates q, including at a spent site, and commutes P_S." This supports "does not test the cell".
5. **Admission — CONFIRMED (wording note E13).**
   - C7 l.9: "A_v^+=|S,x_carrier><R,B_carrier| tensor I_q"
   - C7 l.10: "kappa_v A_v^+"
   - C7 l.17: "Forward admission transfers R/B to S/x without writing q"
   - P26 l.84: "forward admission +1 -1 +1 0"
6. **Admission reverse — CONFIRMED_WITH_CORRECTION (E8).** The source writes `conjugate(kappa_v) A_v^-` (C7 l.10), not `conj(kappa_v)`. The reverse inventory is correct: P26 l.85 "reverse admission -1 +1 -1 0".
7. **Donor energy — CONFIRMED (citation E11).**
   - P26 l.53: "HD=sum_(j=0..2K-1) [e_I P_ID,j + e_R P_RD,j]"
   - L l.20: "H_donor retains both e_R and e_I"
   - G l.19: "Every donor configuration occurs in every summand"
   - P26 l.41: "no carrier and no q"
   - P26 l.56: "Donors have no additional hopping/reset/irreversible generator"
   - D l.11
   - "No graph projector" is correct.
8. **Owned Birth — CONFIRMED_WITH_CORRECTION (E3, E12).**
   - L l.15 matches verbatim: "T_own=epsilon sum_(G,C,j) 1_{o_j in W_G(C)} B_(G,C,j)".
   - The guards match L l.13: "Permit channel(G,C,j) exactly when slotj is absent, o_j belongs toW_G(C), the cut census is2 and the actual donor pair isRR."
   - The surgery matches G l.27, and the map matches G l.31–34.
   - G l.36: "No test on old cell/record content is added."
   - D l.59 gives T_C.
   - The changes (4 cut edges deleted, 8 star edges created, a_j and b_j present, Rg +2, Rd −2) match G l.27 and l.61, and P26 l.86.
9. **Owned un-Birth — CONFIRMED (clarity note E18).**
   - L l.13: "Its literal adjoint retains every image condition and all valid predecessor reconnections; eligibility is never reevaluated as a fresh forward test on the target."
   - G l.21: "Slots may be reused after exact un-Birth"
   - G l.57 and R l.15
   - D l.61: "same ownership condition on its predecessor graph, not a fresh target-side test"
   - RR l.9: "likewise require at most radius2"

## Birth and reverse sub-table

- **Cut endpoints — CONFIRMED.**
  - G l.7: "four distinct A endpoints and four distinct B endpoints"
  - G l.27: "connect its four A endpoints to b_j and a_j to its four B endpoints"
  - R l.15: "the four A endpoints adjacent to b_j and four B endpoints adjacent to a_j"
- **Root/witness — CONFIRMED.**
  - CL l.7: "four matching edges ending on exactly those neighbors, with four distinct A endpoints, exactly one of which is a"
  - L l.13, which also requires "deduplicate each unordered cut and each witness"
  - R l.7, D l.61: "a given (C,j) is counted once"
  - R l.15: "missing witness membership"
- **Donor ownership — CONFIRMED.**
  - L l.13: "Original vertexo_j owns donor pairj"
  - L l.18 and R l.11 (newborns get no pair)
  - Reverse: G l.36 "assigned donors depleted" and P26 l.74–75 "depleted donor pair I_D"
- **Newborn existence — CONFIRMED_WITH_CORRECTION (E2, E12).**
  - `j notin S` is on G **l.42** ("sum_(j notin S) epsilon B_(G,C,j)"). G l.43 is "H=D+T+T†".
  - G l.27 is correct: "EACH j notin S … a_j,b_j were absent".
  - The reverse cell has no citation.
- **Copy / blank / image — CONFIRMED (citation E10).**
  - G l.32–34
  - G l.36: "Its adjoint requires the paired child bits to agree, census two, the designated new stars Ready/p=q=0, and assigned donors depleted; otherwise it is zero. All failed reverse inputs remain full states."
  - P26 l.61: "|p=0,q=0,R>_(sA)"
  - GR l.7
- **Predecessor reconnections — CONFIRMED.** This list is complete.
  - R l.15: "paired in at most4! ways … Pairings causing duplicate old edges, missing witness membership, unequal child bits or nonblank newborns contribute zero."
  - G l.57: "It is NOT a 'reverse last event' algorithm … their sum need not be a partial isometry"
  - GR l.9
  - Census two and donor depletion are kept in the image row.

## Other blocks

- **Common identity offset — CONFIRMED.**
  - G l.38: "common to ALL graph/donor sectors"
  - P26 l.116: "permitted only across ALL complete levels and donor states"
  - R l.9: "one common identity reference"
- **Birth contact — CONFIRMED (E9).** The expression matches G l.68 and P26 l.110 verbatim.
- **Bookkeeping H_j — CONFIRMED.**
  - R l.19 allocation is reproduced exactly.
  - R l.17: "only a combinatorial dependency device, not physical space"
  - RR l.7: "Grouping is bookkeeping"
  - The author keeps it separate from any physical energy-density law and adopts no partition or equal-weight rule. RR l.19 calls the half-degree Delta split "exact": it is an algebraic identity used for allocation, which U6 correctly labels a proof convention.
- **Comparison members — CONFIRMED_WITH_CORRECTION (E6, E7).** "B is rejected" matches L l.3: "Option2 collective/background reservoir is rejected as the shared route."
- **Component count (CLR l.9) — CONFIRMED.** CLR l.9: "the operation preserves component count". This is an invariant, not a guard inside any term.

## Unresolved list

- **U1 — CONFIRMED NOT FOUND, with modality erratum E4.** C7 gives only "the Hermitian T_e(theta)".
- **U2 — CONFIRMED.** The R l.9 quote is exact.
- **U3 — CONFIRMED.** R l.31: "One must NOT count nonzero operator commutators by fixed group labels".
- **U4 — CONFIRMED.** The RR l.7 quote is exact.
- **U5 — CORRECTION E5.**
- **U6 — CONFIRMED.**
- **U7 — CONFIRMED.** C7 l.9 defines no x or B, and the C7 l.15 quote is exact.
- **U8 — CONFIRMED, with addition E14.**

## Errata (record against V001; author file not edited)

**Citation errata confirmed from the author's report**
- **E1.** Carrier-hopping operator: C7 l.5 → **C7 l.6**.
- **E2.** Newborn existence, `j notin S`: G l.43 → **G l.42**. G l.27 is also correct.

**Substantive errata**
- **E3.** Owned Birth (a) says "one complex epsilon per channel". This misstates G l.40, which says "ONE complex epsilon, identical for each channel" (see also R l.9: "Uniform coefficients epsilon (Birth)"). Read: one complex epsilon, identical for every channel.
- **E4.** U1 says G l.38 "requires" a fixed declared hopping phase rule. G l.38 says such a rule "may be used". The requirement is L l.20: "The parameterized family requires a fixed complete coefficient/phase profile before any prediction."
- **E5.** U5 says "The donor register has no graph site". This contradicts D l.57 ("place one pair at each original vertex") and D l.69 ("All pairs are located at original sites in this finite example"). Read: each donor pair is assigned to original vertex o_j by the ownership relation [D l.57, l.69; L l.13], and as a Hilbert-space factor it lies outside H_native(G) [G l.17, l.19]. D l.69 calls the tie "only combinatorial adjacency, not physical locality", and its physical meaning and supply are undeclared [P26 l.135]. The residual U5 ambiguity, where e_I and e_R reside physically, stands.
- **E6.** The comparison block says alternative A "[D l.17]" has "no graph-distance locality". A uses C_loc cuts (D l.7). Its non-locality is in resource access: any inactive slot can serve any cut [D l.17; D l.73 "globally accessible channels"; RR l.27 "all-to-all resource access"]. For all-matchings, the locality denial is G l.11 ("supplies no graph-distance locality"); G l.42 is only the formula.

**Wording, symbol and citation errata**
- **E7.** B's `(K-|S|)^(-1/2)` and R_D/R_U are global coefficients and operators that depend on count or reservoir number [D l.47, l.53: "global K-N normalization"], not 0/1 predicates. The "global, not sector index" classification is correct; "predicate" is loose.
- **E8.** Symbols:
  - `conj(kappa_v)` should be `conjugate(kappa_v)` [C7 l.10].
  - The header H_K^graph omits "G in G(S)" [G l.17].
- **E9.** Birth contact:
  - "Matrix-element comparison" is P26 **l.111**; add the citation.
  - "Not an operator / not a local energy assignment" is an unsourced gloss. The sources' own negations are P26 l.112–113 ("not the full spectral detuning or a proof of resonant dynamics") and G l.68 ("not a spectral detuning, a resonance prescription or energy creation").
- **E10.** The source for "canonical blank-I insertion … comparison only" is P26 l.128–130 ("This is a comparison model") and l.113–114. P26 l.61–62 and C7 l.15 only define the inserted states.
- **E11.** Donor row, "different law, not substituted": cite NDA l.13–15 and DR l.13 ("cannot be silently substituted"). NDA l.13 alone only defines T=F2 b_w.
- **E12.** Missing citations:
  - Newborn-existence reverse: G l.29 ("(S,G) block to (S union{j},G')") and R l.15 ("An output graph with slot j active").
  - Owned Birth "no global count": R l.9 ("no remote-graph/subset, total-count … coefficient") and D l.67 ("No factor of the total distant donor stock appears").
  - "Radius 2" should carry the combinatorial qualifier: CL l.9 ("a combinatorial statement, not a physical radius") and R l.17.
- **E13.** "Uniform kappa allowed only as a control member" (row 5) and "zero phases licensed only as a control member" (U1) go beyond L l.20, which says these "may be used as an explicitly declared finite control member". C7 l.13 adds that uniform kappa "is a declaration, not silently chosen here". Drop "only".
- **E14.** Add R l.27 ("one Bind flip") to U8. The explicit X_r,v matrix is still not written in the sources.
- **E15.** Three same-stem READING files are not listed (hashes above), and the "all PASS_SCOPED" label is slightly inaccurate (see the companion rule above).
- **E16.** Length: the body (lines 1–59) is about 1,900 words and 11.0 KB, with two wide tables. This exceeds the brief's target of "at most two pages plus source citations". The citations (lines 61–86) are about 245 words. This is non-blocking.
- **E17.** The author's report says the owned-Birth row cites G l.29–36; the file cites G l.29–34, and l.36 sits in column (d). The file is correct as written.
- **E18.** Un-Birth (a) expands to `epsilon* B_(G,C,j)†` without the real owner indicator 1_{o_j in W_G(C)}, which is evaluated on the predecessor G. Column (e) states the condition, so no content is lost.

## Scope and prohibited-content scan

The author file contains no invented local factorization: U3 and U4 record the ambiguity instead. It contains no adoption language, physical partition, equal-weight rule, energy-density law, covariance claim or use of the proper-time proposal. I opened no file whose name contains Newton, FIELD_, ROTATION, FIT, TRIAL, MOM1, rotmod or MassModels.
