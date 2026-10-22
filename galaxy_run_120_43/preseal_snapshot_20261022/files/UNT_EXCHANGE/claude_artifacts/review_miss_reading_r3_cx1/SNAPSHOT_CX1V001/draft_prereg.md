# PREREG_MISS_READING_R3 — how the 43 NGC3198 rows will be read (UNSEALED DRAFT r3; written before any NGC3198 target is opened)

## Status [C-S]

- **What this is.** Draft r3 for root (dispatches 0585, 0606 and 0619; root ruling A98.2). When root seals it, it supersedes V001 (`6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345`). V001 stays as history.
- **History.** r2 round 1 (`r2/round1/`) and round 2 (`r2/round2/`) were each checked by three refute-by-default lenses, each with two refuters. Codex2 reviewed round 2 cross-lineage (0490), and root ruled round 2 FAIL and ordered this r3 (A98.2).
  - Every finding of the round-2 recheck, every Codex2 0490 item, and every round-1 row that the round-2 recheck found only partly closed has a written disposition in `CLOSURE_R3.json`, mirrored in the closure tables of `CLAUSE_SOURCE_MAP_R3.md`.
  - A disposition is FIXED (with the change and its clause tag), NOT_ADOPTED (with the reason), or, for a check-tool item, routed to the r3 tools stage with the change it needs. No row is called closed without one.
- **Author.** Claude4, single author.
- **No target was opened.** No NGC3198 target value, no measured rotation datum and no target-bearing file was opened in writing it. The only NGC3198 records read are target-free:
  - query ids and radii from the query block of slots V003, and the slots' alternatives list, observation rule, STAGE0 registration and structural-assumption notes;
  - the target-free query manifest the slots cite, which the check hashes only;
  - the target-free N-test, node and certificate records named in §11, and the support-record schema in the code of Codex3's carrier extractor.
- **It changes nothing in the score.** Freeze v003g computes the LADDER rows in root's two-pass freeze:
  - module `48a1e48a…`, PASS in Claude4 0071;
  - RUNBOOK_V001 `9557b5aa…`.

  This document classifies and reads those rows afterwards.
- **Clause tags.** Each clause carries a tag in square brackets; for example, the tier rule's tag is C-1.1. The tags key the clause source map (`CLAUSE_SOURCE_MAP_R3.md`).
- **When the seal happens (binding).**
  - Root rules on root items M-1 to M-15 and seals this text, together with the M-12 classifier, before anyone reads any step-5 NGC route-A/B output value. "Anyone" means root, the author, and every reviewer of this text or of the classifier. "Output value" means a prediction, a band, an envelope, a sensitivity row or an alternative row.
  - The preferred timing is to seal before step 5 launches. **Step 5 is never delayed for the seal.** If step 5 runs first, its outputs are read validity-only until the seal.
  - The seal is root's entry registering the sha256 of this text and of the classifier (M-6).
  - **Validity-only reads.** Until the seal, step-5 outputs are read only as validity and admissibility booleans and reason codes, with no output value printed or written: the pattern of A47 I3.
  - **The attestation.** The seal entry lists every validity fact that was seen before the seal: which receipts, valid flags and reason codes, seen by whom. It also records, from each lane that touched this text or the classifier after step 5 launched, a statement that it read no step-5 output value.
  - **The fallback.** If the timing is not met, three versions apply, each the **last candidate whose sha256 was published, in a FROM_CLAUDE4 post or a root entry, before the first step-5 output value was read**: this text, its root-item recommendations, and the classifier. These are the pre-prediction versions.
    - Every root item is adopted exactly as recommended in the pre-prediction version. There is no option switching.
    - The seal entry names each pre-prediction sha and its publication time, and the report header discloses the deviation.
    - Any later wording change, ruling or classifier change is POST-PREDICTION. It is listed with its diff, and the report also gives the classification under the pre-prediction versions. A status that holds only under a later version is EXPLORATORY. A candidate published later is never adopted under the fallback.
    - If no classifier sha was published before the first read, the classifier is built to the pre-prediction text and labelled POST-PREDICTION (CLASSIFIER). Its M-12 agreement suite must still pass before it runs.

**Binding principles** (A10, A12.3, A15 E3, A20, A23, A41, A48) **[C-P]**:
- Every outcome registers; nothing is prescribed.
- A miss is never reported as a failure of UNT in general. Under A15 E3, an outer-row failure is TESTED-NEGATIVE for exactly the present-mass-only lapse response of the L = 4 coefficient method, at the A2 grid and the calibrated θ. §2 defines "outer-row failure" (OUTER_FAILURE), and §5.3 gives the E3 verdict line.
- **The registered readings of a miss.** Every miss is read at least two ways: as a model failure, or as the missing history or species dependence (A10, SA-BH-01). An outer-row failure keeps the three readings of A15 E3, as narrowed by A20, open whatever its sign. §3 makes both rules mechanical.
- Every reading is conditional on:
  - the fixed DDO154 distance 4.04 Mpc and inclination 66°, and the NGC3198 registered geometry (13.8 Mpc, 72°), all NOT_EVALUATED_BEFORE_FREEZE (A23);
  - the registered NGC numerics of I-6.
- Where this text is silent, the reading less favourable to the model as registered is chosen. This is the A48 governing principle, applied to readings. No reading is an adopted hypothesis (A20).

## 0. Invariants

- **I-1. The rows [C-I1].**
  - All 43 rows, NGC3198-Q01 to NGC3198-Q43, are classified in manifest order. Q_ids, radii and validity come only from the frozen manifest and the root-pinned rosters.
  - **Denominators.** 43 for the PRIMARY and for every full-row alternative. STAGE0_GRID_OUTER, if evaluated, uses its registered subset Q36–Q43, with denominator 8 (A65; RUNBOOK_V001 step 10).
  - No row is dropped, merged, re-gridded or substituted (0518 item 1).
- **I-2. Quoted values only [C-I2].**
  - The quoted target values v_q and σ_q are used exactly as quoted. No σ is inflated, floored or re-estimated.
  - Nothing in this document is fitted to the targets.
- **I-3. Frozen quantities only [C-I3].** The classification uses only:
  - the frozen reference member's LADDER rows. REFERENCE_RULE chooses that member at freeze time, before target access;
  - the frozen PRIMARY pointwise-envelope rows. Their label begins with POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE; a mode suffix may follow;
  - the root-pinned row-registration rosters (0531; v003g), and the gate-status list of §4, which says whether each root-listed gate is ON-TIME or LATE;
  - the query radius R_q, bound by query id to the slots V003 query block, with Rad_unit kpc (v003g fixes F2 and F3);
  - the TRUNCATION_SHAPE_RESIDUAL flag ids fixed in §1.4, carried by the root-pinned flag record. §1.4's id list governs, and a disagreement stops the classification before target access;
  - the STAGE0 status of §6.3, with its receipt and step-4 times;
  - the target pair (v_q, σ_q), which appears only inside the output of `score_after_freeze`.
- **I-4. Alternatives [C-I4].** Slots V003 declares six alternatives, in this order:

| alternative | kind | status at writing | how this document reads it |
|---|---|---|---|
| BR_A_F10_PRIMARY | state | EVALUATED_BEFORE_FREEZE | the PRIMARY (§1–§5) |
| ORIGINAL_K | state | EVALUATED_BEFORE_FREEZE | twin rule, separately (§6.1); never replaces the PRIMARY |
| ML_3p6_0.4 | source | NOT_EVALUATED_BEFORE_FREEZE | status reported only (§6.2) |
| ML_3p6_0.6 | source | NOT_EVALUATED_BEFORE_FREEZE | status reported only (§6.2) |
| GL10_SOURCE_GAUSS_ORDER | approximation | NOT_EVALUATED_BEFORE_FREEZE | status reported only; never a repair (0518 item 5) |
| STAGE0_GRID_OUTER | approximation | NOT_EVALUATED_BEFORE_FREEZE; headline false; scope OUTER Q36–Q43 | §6.3 |

  - In the fixed-distance mode, v003g also appends the recorded distance alternative (DDO154_DISTANCE_NUISANCE). It is never scored (A13). Its status is reported only.
  - If root changes ORIGINAL_K to NOT_EVALUATED before step 5 (A16.2), every clause here that uses ORIGINAL_K reads NOT_AVAILABLE.
  - An alternative never replaces, re-tiers or outvotes the PRIMARY classification.
- **I-5. Headline [C-I5].** The headline stays the freeze module's (v003g HEADLINE_RULE): the distribution of the PRIMARY members' within-error counts, plus the frozen reference member's count. This document adds readings only and never alters the headline.
- **I-6. Numerics conditions [C-I6].** Every reading is conditional on the registered NGC numerics, all fixed before any target is opened. The report header records each, with its record sha (D-4).
  - **K_big.** NGC production K_big = 32 /kpc (A64, after the formal N3 at 16 failed, TESTED), with N3′ = {16, 64} against 32. N1, N2, N4 and NQ are evaluated at 32.
  - **The N-test record of record** is the production compare `ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` (Codex1 0056; A90). A successor replaces it only through a root entry made before any target is opened, and the seal entry names it.
  - **The gate.**
    - The N-test outcomes keep their 0512 names. Under 0512, N_PASS licenses nothing by itself; it is an input to the route-A/B step.
    - NGC route A/B is not run unless that record's `n_route_ab_gate` reads OPEN (0550; A66.2–A66.3). The gate is not launch authorization: the record's own `n_route_ab_ruling` says so.
    - The gate is OPEN for N_PASS, and for N_FAIL_N1 confined to TRUNCATION_SHAPE rings (reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66).
    - It is BLOCKED for:
      - a failure of N0, NQ, N2 or N3′, or an N1 failure on a ring that is not TRUNCATION_SHAPE (0550; A66.3);
      - N_INCOMPLETE or N_NO_RUN. This is the compare producer's behaviour and 0512's rule: "Unknown or missing input reads N_INCOMPLETE, never a pass."
    - **If a route-A/B score exists, this document applies to it in full.** If the record of record's gate was not OPEN when that route-A/B run launched, every pattern, reading, zone summary and verdict line carries PROVISIONAL (N_GATE_NOT_OPEN).
    - **At writing**, the record reads N_FAIL_N1 with tests read, and the gate is OPEN for the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66.
  - **Certificates.**
    - EPS_NGC, LO_NGC and GQ_NGC are certified to coverage at least √2·64 ≈ 91 /kpc (A64.2). No NGC N-test is read until all three are slotted (A81 RI-23), and the NGC I1-T check passes before any NGC N-test is read (A52).
    - The NGC N-test LO record is LO_NGC_K32_CERT_V001, with coverage to 91 (A90).
    - The LO I1-T precondition (independent tail-domain star-transform convergence), which A90 left open for step 5, is closed in A101: Codex1 0066 reports it TESTED PASS. Its scope, in 0066's own words, is finite-grid evidence, not a uniform certificate. D-4 records it with its sha.
  - **Gas M_s.**
    - The NGC gas M_s is 96, or 128 if GQ_NGC at 96 fails anywhere on [2, 91] (A81 RI-23). At 128, LO_NGC and the DOUBLING NGC half are recomputed. The DOUBLING NGC half's bound is θ/20 (A81 RI-22).
    - **At writing**, GQ_NGC at M_s 96 holds on [2, 91] (Codex1 0032, TESTED), so the M_s is 96 unless root rules otherwise.
  - **C1 and C1′.** C1′ applies only on NOT_GRID rings. C1 is kept on TRUNCATION_SHAPE and QUADRATURE_LIMITED rings (A64.1).
  - **None of these is chosen, changed or re-run after targets are opened.**
  - **Numerical readings.** Exactly two registered readings attribute a miss to numerics, and each has registered prior evidence against it (§3):
    - R-GRID, k-grid fidelity of the in-use T120L grid;
    - R-TSR, the A66 residual.

    No other reading attributes a miss to a certified numerical quantity.
- **I-7. Freeze status and the score of record [C-I7].**
  - **Which score is classified.** The classification is made on a FREEZE_COMPLETE manifest. This text classifies the **first** successful `score_after_freeze` on NGC3198 targets.
  - **Later scores.** Any later freeze, re-registration or re-score after target access is EXPLORATORY (post-score). No roster, cut or reference may be chosen after targets are seen (RUNBOOK_V001 step 9).
  - **An incomplete freeze.** Whether a FREEZE_INCOMPLETE manifest may be scored is recorded in a root entry before any step-5 output value is read, or fixed by the seal (root item M-8). A FREEZE_INCOMPLETE score authorized later is EXPLORATORY (post-prediction).
    - If a FREEZE_INCOMPLETE manifest is scored, the classification is still made and reported in full.
    - Every pattern, reading and zone summary, the E3 verdict line and the DT-S0G comparison then carry PROVISIONAL (FREEZE_INCOMPLETE), with the manifest's `incomplete_reasons` (the A50 PROVISIONAL rule, by analogy).
  - **NEAR when envelope rows are invalid.** v003g marks every envelope row invalid when any PRIMARY member is unevaluated, and a row's envelope is also invalid when no member is valid on it. On a row whose envelope row is invalid, NEAR reads NOT_AVAILABLE; N(Z) then reads NOT_AVAILABLE for that zone, and the report says so.

## 1. Per-row classification (PRIMARY)

### 1.1 Tier, and the NEAR flag [C-1.1]

Rule M-T applies to the output of `score_after_freeze`. Let:
- ref = `headline.reference_member_id`;
- L_q = the row for query q in the `rows` of the entry in `members` whose `member_id` is ref;
- E_q = the row for q in `pointwise_envelope.rows`.

The tiers are evaluated in this order:

| tier | condition | fields used |
|---|---|---|
| **INVALID_AS_MISS** | `L_q.score_status = INVALID_AS_MISS`. In v003g this holds exactly when the reference member's frozen row carries a roster-authorized INVALID registration (§4). The row then has tier MISS_WORST_TIER, a null prediction, and its `registered_reason`. | `score_status`, `registered_reason` |
| **HIT** | Not INVALID, and `L_q.within_error = true`: \|r_q\| ≤ 1 with r_q = `L_q.sigma_ratio` = (p_q − v_q)/σ_q (WITHIN_ERROR_RULE). In v003g: score_status HIT, tier WITHIN_ERROR. | `within_error`, `sigma_ratio` |
| **MISS** | Not INVALID and not HIT (v003g score_status MISS). | `score_status` |

- **The NEAR flag** is set on a tier-MISS row when `E_q.valid = true` and `E_q.band_overlaps_error_bar = true`, meaning the frozen PRIMARY pointwise envelope interval [lo_q, hi_q] intersects the error bar [v_q − σ_q, v_q + σ_q].
  - It does **not** mean that any single member is within error. Members lying on both sides of the bar also produce it.
  - NEAR is reported as "envelope overlaps the error bar". A NEAR row stays a MISS for every count and pattern in §2.
  - A row of tier INVALID_AS_MISS never carries NEAR, LATE-gate rows included (§4). When `E_q.valid = false`, NEAR reads NOT_AVAILABLE (I-7).
- **The sensitivity band.** The box-limited sensitivity band (`sensitivity.rows`) is never used for a tier, a flag, a pattern or a reading.
  - It is reported in one fixed column for all 43 rows: "sensitivity band overlaps: yes / no / invalid", labelled "conditional on trial values".
  - An invalid sensitivity row (`sensitivity.rows[].valid = false`) is reported as invalid, never as a zero-width band. This applies, for example, when the geometry sensitivity is refused as registered.
- **A row with no ratio.** A VALID row whose `sigma_ratio` is null (v003g NON_FINITE_SIGMA_RATIO) is a MISS with sign UNDEFINED. It counts in N_v(Z), M(Z) and U(Z) (§2), and it is left out of m(Z) and Δ_out.
- **Pre-score checks (binding).** Every stop condition below is target-free.
  - **When they run.** Each is checked on the frozen manifest, slots and pinned records **before any target is opened**, through the sealed classifier (M-12) run on a synthetic score built from the frozen member arrays. The result goes in the seal or score entry.
  - **The stop conditions:**
    - the reference member's row status is UNEVALUATED_OR_REFUSED (REFERENCE_RULE excludes this);
    - the reference member named in the score (`headline.reference_member_id`, `reference_member_log_index`) differs from the frozen manifest's (REFERENCE_MEMBER_MISMATCH);
    - a field named here or in M-5 is missing, has the wrong type, or is non-finite where a finite value is required;
    - the reference member's ids are not Q01 to Q43 in order, or an id is repeated;
    - the envelope label prefix differs;
    - the zone table of §1.3 differs;
    - **TSR_FLAG_TABLE_MISMATCH:** the freeze's pinned N-test compare is not `6f095f64…`; or its failing TRUNCATION_SHAPE rings are not exactly {ordinal 15}; or its failing non-TRUNCATION_SHAPE rings are not empty; or the N1 record is not `8867c376…`; or the GL-node record is not `ec1dcca5…`; or the flag record's 43 flags are not exactly {NGC3198-Q25} (§1.4);
    - **GATE_STATUS_LIST_DEFECT:** the gate-status list of §4 is missing, or a root-listed gate of the rosters is not on it;
    - **SEAL_SHA_MISMATCH:** a sealed sha (this text, the classifier, the flag record, the STAGE0 successor if pinned) does not match its bytes. This check runs before RUNBOOK step 9.

    Any of these stops the classification with CLASSIFICATION_INPUT_DEFECT and its code, before target access.
  - **After target access,** root has only two permitted acts:
    - **Rename a field.** A field map renames keys only; it never changes a value. It is pinned, with its diff, before the classifier output is read, and the sealed M-12 suite must reproduce byte for byte through it. When such a map clears a stop, root must apply it, and NOT_READ is then not available for that stop.
    - **Declare NOT_READ,** and only if a stop condition above, re-run on the real score, fires. The classifier output is still computed on every input that is intact and published, labelled NOT_READ with the stop code. Each output whose own input is defective reads NOT_AVAILABLE with the code. The E3 verdict line is printed with its value, or NOT_AVAILABLE with the code when one of its own inputs is defective. Values that cannot be classified may be shown descriptively, labelled "not read" (the A48 AMB-18 pattern).

    Root may never change a tier, zone, pattern, member or reading rule after target access.
- Root item **M-1**.

### 1.2 Sign [C-1.2]

- s_q = sign(r_q), one of −1, 0, +1, or UNDEFINED when r_q is null. **Deficit** (−1): the model is below the quoted value. **Excess** (+1): the model is above it.
- INVALID rows carry no sign. LATE-gate rows carry no sign (§4).

### 1.3 Zone [C-1.3]

**The rule is unchanged from V001.** The zone comes from the frozen query radius R_q (kpc, at D = 13.8 Mpc), never from residuals:
- **INNER:** R_q < 10.0 kpc (A15 E1: "R ≲ 10 kpc");
- **TRANSITION:** 10.0 ≤ R_q < 30.0 kpc;
- **OUTER:** R_q ≥ 30.0 kpc (A15 E2: "about 30–44.08 kpc").

**Membership, fixed here by query id.** It is computed from the target-free slots V003 query block (`Rad_text`, Rad_unit kpc), whose source is the target-free query manifest `a2936517…`:

| zone | query ids | n | radius range at writing (kpc) |
|---|---|---|---|
| INNER | NGC3198-Q01 to NGC3198-Q24 | 24 | 0.32 to 9.04 |
| TRANSITION | NGC3198-Q25 to NGC3198-Q35 | 11 | 10.04 to 28.16 |
| OUTER | NGC3198-Q36 to NGC3198-Q43 | 8 | 30.08 to 44.08 |

- **The OUTER set equals the registered STAGE0_GRID_OUTER scope.** The same set is computed by the v003g scope function `_alternative_score_scope`.
- **The rows nearest the cuts** are Q24 and Q25 (9.04 and 10.04 kpc), and Q35 and Q36 (28.16 and 30.08 kpc). This is recorded now so that no row can later be argued into the other zone.
- **A mismatch stops the classification** before target access (§1.1).
- Root item **M-2**.

### 1.4 The TRUNCATION_SHAPE_RESIDUAL flag [C-1.4]

- **What the flag is.** A disclosure flag, not INVALID (A66.2; 0550).
  - The registered compare lists the failing TRUNCATION_SHAPE rings, with S/θ and radial support. The freeze flags the overlapping rows.
  - A flagged row is classified by M-T like any other row.
- **The overlap rule: the dependence reading of A66.2's "radial support"** (root item M-7, option (i)). A66.2 flags every row "whose radius lies within the radial support of a failing TRUNCATION_SHAPE ring", and the registered compare stores that support as a single sampled ring. This text reads "radial support" as dependence, from three registered facts:
  - **The rings are the route-B nodes.** The 100 ring radii of the production N1 record equal, bitwise, the 100 GL4 node radii of `REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (`ec1dcca5…`).
  - **The observation rule** registered in slots V003 reads: "HI-weighted mean of R*Omega, then piecewise-linear interpolation of mean onto the supplied 43 manifest radii without extrapolation".
  - **Each node's value is local to its ring.** The route-B column value at node k depends only on ring k: the rotation module forms Ω² column by column, and its radial derivative enters only the shear. Round-2 recheck lens R2-B TESTED this from the module bytes (its report is pinned in §11; not re-run here).
  - So a query value depends on node k if and only if its R_q lies strictly between nodes k − 1 and k + 1. For the first node (k = 0) the interval is r_0 ≤ R_q < r_1, and for the last (k = 99) it is r_98 < R_q ≤ r_99.
  - **A query row is flagged if and only if r_{k−1} < R_q < r_{k+1} for a failing TRUNCATION_SHAPE ring k**, with the end forms above. R_q is bound by id and read from Rad_text in kpc; the RUNBOOK's metre form gives the same set (TESTED in the round-2 recheck). The ring radii come from the production N1 record.
  - M-7 records the other readings of "radial support" and what each would flag.
- **At writing** (Codex1 0056; A90; records pinned in §11):
  - the production compare reads N_FAIL_N1, with tests read;
  - exactly one TRUNCATION_SHAPE ring fails: ordinal 15, at R = 10.54 kpc, with S/θ = 1.0148 and criterion C1;
  - no ring of any other class fails;
  - N0, NQ, N2 and N3′ pass;
  - the gate reads OPEN.
- **The flagged rows, fixed here by id.**
  - The neighbouring rings are at 9.90 and 10.91 kpc, so exactly one row is flagged: **NGC3198-Q25** (10.04 kpc, TRANSITION).
  - NGC3198-Q26 (11.04 kpc) lies beyond ring 16, so it does not depend on ring 15 and is not flagged.
  - **This id list governs.** The flag record must equal it. Any difference, or any change to the pinned compare, N1 record or node record, is the pre-target stop TSR_FLAG_TABLE_MISMATCH (§1.1).
  - If the formal record changes before the seal, the flagged ids are recomputed from target-free data and listed here before the seal.
- **The carrier.**
  - The flag record is root-pinned and target-free. It lists the failing ring, the rule above and the flagged ids, and it is pinned among the freeze manifest's input files. Its sha, and those of the compare, the N1 record and the node record, go in the report header (§8).
  - Codex3's step-5 carrier extractor (0618; `extract_carriers_cx3v005.py`, pinned in §11) emits the 43 flags only from a root-adopted support record, and it requires that record to contain the failing ring. The support record that implements this rule is:
    - schema UNT_ROOT_TSR_SUPPORT_CX3V001, with one ring entry;
    - its native_ring is the compare's ordinal-15 record, verbatim;
    - lower_kpc 9.901810628740723 (r_14), lower_inclusive false;
    - upper_kpc 10.911721936765339 (r_16), upper_inclusive false.

    It contains the failing ring, and it flags exactly Q25: Q24 (9.04 kpc) and Q26 (11.04 kpc) lie outside it.
  - v003g has no flag field (M-7).
- **Where the flag applies.** The flag belongs to the PRIMARY operator and grid, on which the N-tests ran. No TSR flag applies to an alternative's rows (§6.1). A LATE-gate row carries no P10 and no reading (§4), but the flagged-row list still names it with its tier.

## 2. Zone summaries and patterns (algorithmic; every applicable pattern is reported) [C-2]

**Per-zone summaries.** For each zone Z:
- **Counts.**
  - N_v(Z) is the number of non-INVALID rows.
  - H(Z) and M(Z) are the HIT and MISS counts. NEAR-flagged rows are MISS rows.
  - U(Z) is the number of non-INVALID MISS rows with no defined r_q: null-ratio rows (§1.1) and LATE-gate rows (§4). M(Z) − U(Z) is the number of signed MISS rows.
  - N(Z) is the number of NEAR-flagged rows (NOT_AVAILABLE under I-7).
  - I(Z) is the INVALID count, also given per registered reason.
- **m(Z):** the median of r_q over the non-INVALID rows that have a defined r_q (the HIT rows and the signed MISS rows). For an even count it is the mean of the two middle values. It is UNDEFINED when there is no such row.
- **Miss-dominated:** N_v(Z) ≥ 1 and M(Z) ≥ N_v(Z)/2.
- **Hit-dominated:** N_v(Z) ≥ 1 and H(Z) > N_v(Z)/2, a strict majority.
  - The two are exclusive, and for N_v(Z) ≥ 1 exactly one of them holds. A tie reads miss-dominated, the reading less favourable to the model (A48 principle).
- **Sign class S(Z):**
  - **UNDEFINED** when m(Z) is UNDEFINED, or when Z is miss-dominated and M(Z) − U(Z) < N_v(Z)/2, that is, when the signed misses alone do not reach half of the zone's non-INVALID rows. A sign class is therefore never taken from hits, or from a minority of signed misses.
  - Otherwise **DEFICIT** if m(Z) < −1, **EXCESS** if m(Z) > +1, and **CENTERED** otherwise.
  - FORMAL: \|m(Z)\| > 1 implies that Z is miss-dominated, because at least half of the rows with a defined r_q are then misses of that sign. So DEFICIT and EXCESS occur only in miss-dominated zones.
- **Clarifications.**
  - Any condition that uses an UNDEFINED quantity is false, and it is reported as UNDEFINED. **The one exception** is the test "S(Z) is UNDEFINED" of P14 and P15, which holds exactly when S(Z) is UNDEFINED. A comparison between sign classes (P6) requires every compared class to be defined.
  - A pattern whose condition is about rows needs at least one non-INVALID row; it never holds vacuously.

**Outer trend.**
- Sort the OUTER rows that are non-INVALID and have a defined r_q by R_q, and split them into a near half and a far half. With an odd count, the middle row goes to the far half.
- Δ_out = median r(far half) − median r(near half). It is UNDEFINED if fewer than 2 such rows exist.
- **GROWING** holds if and only if S(OUTER) = DEFICIT, Δ_out < 0, and m(TRANSITION) > m(OUTER).
- **CROSSING** holds if and only if S(OUTER) = CENTERED, Δ_out < 0, m(TRANSITION) > m(OUTER), and median r(far half) < −1: the outermost rows are a deficit while the zone as a whole is centred.

**OUTER_FAILURE.** This is the "outer-row failure" of A15 E3, registered here as: **OUTER is miss-dominated**, that is, N_v(OUTER) ≥ 1 and M(OUTER) ≥ N_v(OUTER)/2, whatever S(OUTER). Equivalently, exactly one of P1, P2, P11 or P14 holds (FORMAL: S(OUTER) is exactly one of DEFICIT, EXCESS, CENTERED or UNDEFINED).

**Patterns.** Each pattern is evaluated independently, and every one that holds is reported. No pattern masks another.

| id | pattern | condition |
|---|---|---|
| P0 | INVALID rows | I(Z) > 0 in any zone; reported per zone and per registered reason (§4) |
| P1 | OUTER_DEFICIT (the outcome A15 E2 expected) | OUTER miss-dominated and S(OUTER) = DEFICIT; flag **P1g** if GROWING |
| P2 | OUTER_EXCESS | OUTER miss-dominated and S(OUTER) = EXCESS |
| P11 | OUTER_MIXED | OUTER miss-dominated and S(OUTER) = CENTERED (misses of both signs, or small residuals); flag **P11g** if CROSSING |
| P14 | OUTER_UNSIGNED | OUTER miss-dominated and S(OUTER) = UNDEFINED: the signed OUTER misses alone do not reach half of N_v(OUTER), or no non-INVALID OUTER row has a defined ratio |
| P3 | INNER_EXCESS | INNER miss-dominated and S(INNER) = EXCESS |
| P4 | INNER_DEFICIT | INNER miss-dominated and S(INNER) = DEFICIT |
| P12 | INNER_MIXED | INNER miss-dominated and S(INNER) = CENTERED |
| P15 | INNER_UNSIGNED | INNER miss-dominated and S(INNER) = UNDEFINED |
| P13 | TRANSITION_MISS | TRANSITION miss-dominated, with S(TRANSITION) reported (any class, UNDEFINED included) |
| P5 | TRANSITION_ONSET | INNER hit-dominated, OUTER miss-dominated, N_v(TRANSITION) ≥ 1, and TRANSITION not hit-dominated |
| P6 | GLOBAL_OFFSET | S(INNER), S(TRANSITION) and S(OUTER) all defined, all equal, and not CENTERED |
| P7 | SCATTERED | at least one MISS, and no zone miss-dominated |
| P8 | NO_MISS_AMONG_VALID_ROWS | at least one non-INVALID row, and M = 0 over all non-INVALID rows. Never reported as "all hit": INVALID rows still score as misses (§4). It is always reported with I and N, and it can hold together with P0 and P9. |
| P9 | OUTER_UNTESTABLE | N_v(OUTER) = 0: every OUTER row is INVALID |
| P10 | TSR_MISS | at least one non-INVALID MISS row with a frozen prediction carries the TRUNCATION_SHAPE_RESIDUAL flag. A LATE-gate row never counts here. |

- **Coverage.** Every outcome with at least one MISS satisfies at least one zone pattern (P1, P2, P11, P14, P3, P4, P12, P15 or P13), or P7.
  - **Proof.** A MISS row is non-INVALID, so its zone has N_v ≥ 1.
    - If no zone is miss-dominated, P7 holds.
    - If a zone is miss-dominated, its sign class is exactly one of DEFICIT, EXCESS, CENTERED or UNDEFINED. Then:
      - OUTER gives exactly one of P1, P2, P11 or P14;
      - INNER gives exactly one of P4, P3, P12 or P15;
      - TRANSITION gives P13, which holds for any sign class.
  - The same case split proves the OUTER_FAILURE equivalence above.
- **P5 in terms of the others (FORMAL).** For N_v ≥ 1, "not hit-dominated" means "miss-dominated". So P5 holds exactly when INNER is hit-dominated, OUTER_FAILURE holds and P13 holds. P5 carries no reading of its own (§3).
- **P6 in terms of the others (FORMAL).** A DEFICIT or EXCESS zone is miss-dominated, so P6 implies P1 or P2, P3 or P4, and P13.
- **Also reported for each zone:** the counts (U(Z) included), m(Z), S(Z), the NEAR-flagged rows, and the individual rows.
- **The flagged-row list.** Whenever any row is flagged, the report lists every flagged row with its tier, INVALID included. This is a disclosure, not a pattern input.

## 3. Readings, deciding tests, and the status of each reading [C-3]

**Rules for every reading:**
- **One tuple rule per reading.** The report lists every registered reading of §3.2, every time, in table order. Each is reported once, as a fixed tuple of three parts that depends only on the outcome, never on which trigger fired:
  1. **score relation:** CONSISTENT, INCONSISTENT or NOT_ADDRESSED.
     - INCONSISTENT when any registered against-condition of the reading holds. **Against takes precedence.**
     - NOT_ADDRESSED when the score does not bear on the reading, in exactly two registered cases, each printed with its code: no trigger of the reading holds (PATTERN_NOT_HELD); or the reading is deficit-type and the OUTER signs are outside its scope (SIGN_SCOPE_EXCESS, SIGN_SCOPE_UNSIGNED or SIGN_SCOPE_NO_DEFICIT_MISS, §3.2).
     - CONSISTENT otherwise.
  2. **deciding-test status,** as it stands at the score step: OPEN when the deciding test is NOT SCHEDULED, not run, UNTESTED or NOT_EVALUATED_BEFORE_FREEZE; otherwise the test's registered outcome. Two readings have their own rule: R-MF's part 2 is the value of the E3 verdict line (§5.3), and R-DRIFT's part 2 follows the §6.3 mapping. A deciding test that runs after the score step changes no part 2; its result is reported separately, under the support rule below.
  3. **prior evidence:** exactly the entries in the prior-evidence column of §3.2, which is the closed list. It never changes parts 1 and 2.

  "CONSISTENT" is never reported without the deciding-test status beside it.
- **No support from the score alone.** The 43-row score can make a reading CONSISTENT or INCONSISTENT. It can never make it supported. Support comes only from that reading's own deciding test, run under its own pre-registration.
  - A deciding test registered after NGC3198 target access can support a reading only through data not opened when its prereg was sealed.
- **Fixed list.** The readings below are the registered list. Any reading proposed after targets are opened is labelled **EXPLORATORY (post-score)** and never counts as registered.
- **The A10 rule: every miss is read two ways.** Every pattern that names MISS rows carries R-MF and one history or species reading: R-HIST for OUTER rows (under OUTER_FAILURE), for TRANSITION rows (under P13), and for all MISS rows under P6 and P7; R-SPEC for INNER rows (under P3, P4, P12 and P15). With the coverage property of §2, every outcome with a MISS therefore triggers R-MF and at least one history or species reading.
- **The A15 E3 rule: an outer-row failure keeps three readings open.** Whenever OUTER_FAILURE holds, R-MF, R-UT1, R-REACH, R-HIST and R-DRIFT are triggered for the OUTER rows, whatever S(OUTER) and whatever the other zones show (A15 E3; A12.3; A20; A63). R-MF, R-HIST and R-DRIFT are sign-free. R-UT1 and R-REACH are deficit-type, and their score relation follows the sign rule of §3.2; they are never dropped.
- **Scope: which rows a reading may cite.** A reading may cite only rows of the zones its triggering patterns name:
  - OUTER rows under OUTER_FAILURE, P2 and P11; INNER rows under P3, P4, P12 and P15; TRANSITION rows under P13; all MISS rows under P6 and P7; flagged MISS rows only, for R-TSR.
  - P5 adds no scope (§2). P0, P8 and P9 trigger no reading.
  - **No reading cites a row with no frozen prediction:** an INVALID row, or a LATE-gate row (§4). A null-ratio row may be cited as a MISS, never by its sign.
- **R-MF's verdict.** R-MF is TESTED-NEGATIVE, for exactly the A15 E3 scope, if and only if OUTER_FAILURE holds (the E3 verdict line, §5.3). The sign class and the unsigned counts are printed with it.

**Deciding tests and their status at writing [C-3.1]:**

| id | deciding test | status |
|---|---|---|
| DT-UT1 | The UT-1 spec-compliant model version: k = 0 a declared zero mode; k → 0⁺ from k ≠ 0 nodes only, under one pre-registered continuation rule; recomputed end to end (A41). | **NOT SCHEDULED**: 0521 withdrawn by 0524 |
| DT-BHD | BH-D derivation from the owned parent, then out-of-sample tests (TDGs, Leo Ring, DF2/DF4) once BH-D exists (A10). | **NOT SCHEDULED**: 0519 withdrawn by 0524 |
| DT-U12 | Small-k limits at larger L and with mixed sampling: U1, U2 and the P-96 capture (A20, A41). | **NOT SCHEDULED**. U2 (0523) was withdrawn by 0524. Stage 0, the L = 4 control, is complete; its sealed outcome is S0-FAIL-RHAT (A63). P-96 at L ≥ 6 needs a root decision, which is not pursued during the galaxy run (A63, per the principal). |
| DT-T1a | BH-T1a: the residual against the target-free stellar fraction f★ (PRIMARY enclosed, SECONDARY local; f★ variants at M/L 0.4 and 0.6). Diagnostic, never headline; runs only after a verified freeze (A10, A16.3). It moves no prediction. | registered; diagnostic. It needs r_q, so it can run only after the score. It never changes part 2 of a tuple, which stays OPEN, and its trend appears only in the descriptive lines. |
| DT-GEO | The geometry box (D 12.545–15.18 Mpc, i 69–75°). | NOT_EVALUATED_BEFORE_FREEZE (A16.1). The forward refuses with GEOMETRY_NOT_EXPOSED (A16, item 4). Any geometry evaluated after the freeze is EXPLORATORY. |
| DT-ALT | The alternatives, scored separately (§6). ORIGINAL_K is evaluated. ML_3p6_0.4, ML_3p6_0.6 and GL10_SOURCE_GAUSS_ORDER are NOT_EVALUATED_BEFORE_FREEZE (A16.2; 0518 item 5). | as stated. An alternative never refutes a PRIMARY reading (§6.1); the NOT_EVALUATED status of the M/L alternatives is prior evidence for R-ML. |
| DT-NAX | Non-axisymmetric finite-flow sensitivity of the m = 0 approximation (plan D3). | not run |
| DT-S1 | Calibration transfer of G_eff = G·Q∞ across parameter space (A21: S1 UNTESTED). | UNTESTED |
| **DT-S0G** | **STAGE0_GRID_OUTER** (A65.2): the NGC route-A/B prediction at the headline admitted DDO154 calibration point(s), with the coefficient grid swapped from A2 (`2e3a36d8…`) to the stage-0 pooled grid (`bdb9016c…`). Everything else is identical. It is a coefficient-grid sensitivity at fixed calibrated parameters, not a recalibration. Read by §6.3. | NOT_EVALUATED_BEFORE_FREEZE in slots V003. Evaluated only under the receipt rule of §6.3 (M-14); its outcome sets R-DRIFT's tuple by the §6.3 mapping. |
| **DT-TSR** | A kept-cube corner-shape variation that removes the residual on the flagged rows. No such test is registered. | **NOT SCHEDULED** |

**Readings [C-3.2].** "Against" lists only conditions that can be decided at the score step. Prior evidence is listed separately and is the closed list.

| reading | what it says | triggers (any one) | sign scope | against (decided at the score step) | prior evidence (closed list) | deciding test |
|---|---|---|---|---|---|---|
| **R-MF** | failure of the present-mass-only lapse response of the L = 4 coefficient method at the A2 grid and the calibrated θ (A15 E3); at row level, the model-failure reading of A10. TESTED-NEGATIVE for exactly the E3 scope when OUTER_FAILURE holds. | OUTER_FAILURE (P1, P2, P11, P14); P3, P4, P12, P15; P13; P6; P7 | sign-free | — | for: A15 E2, which expected an outer deficit; A41 | the score itself, for the E3 scope only: part 2 is the E3 line value |
| **R-UT1** | the static isothermal typing of the k = 0 block (A20 reading 1; counted CA-34/CA-28, A41) | OUTER_FAILURE | deficit-type | — | against: A41 item 3 (FORMAL + TESTED). No gate-consistent typing gives an attractive tail, and the spec-compliant T(0⁺) is finite and repulsive on current estimates. | DT-UT1 (NOT SCHEDULED) |
| **R-REACH** | magnitudes, k = 0-block drift or finite-size effects at larger L or with mixing (A12.3 reading 2, "missing reach"; A15 E3 reading 2; narrowed by A20: these cannot create a 1/r tail) | OUTER_FAILURE | deficit-type | — | — | DT-U12 (NOT SCHEDULED) |
| **R-HIST** | a missing Bind-history or collective component (A10 SA-BH-01, DECLARED-PREMISE; A15 E3 reading 3; A20 reading 2; BH-D). P1g or P11g makes it more specific: "missing long-range component" (0522). | OUTER_FAILURE; P13; P6; P7 | sign-free (A10: every miss) | — | — | DT-BHD (NOT SCHEDULED) |
| **R-DRIFT** | A2's k = 0 entry, which enters the k → 0⁺ transfer under CA-34, is drift-inflated (A63, A65) | OUTER_FAILURE | sign-free | DT-S0G reads AGAINST (§6.3) | for: the sealed k = 0 drift reading is SUPPORTED (A63). Against: its causal gloss is UNTESTED (A65 check R-3). | DT-S0G, by the §6.3 mapping; it never makes R-DRIFT supported |
| **R-S1** | calibration transfer of G_eff = G·Q∞ (A21): the G_eff scale | P2; P11; P6 | — | — | — | DT-S1 (UNTESTED) |
| **R-GRID** (numerical) | k-grid fidelity of the in-use T120L grid at outer radii (A17) | P2; P11 | — | — | against: T120L passes C2, C3, C4 and C1′ (A27). The production N-tests N0, NQ, N2 and N3′ pass (A90). | none registered: OPEN |
| **R-NAX** | non-axisymmetric flow and the m = 0 projection (A17 note; plan D3) | P11; P14; P3, P4, P12, P15; P13; P7 | — | — | — | DT-NAX (not run) |
| **R-GEFF** | the single DDO154 short-wavelength G_eff does not carry over to a galaxy with stellar share about 0.51 (DDO154: about 0.03; A10) (A21, E1) | P3, P4, P12, P15 | — | — | — | DT-S1 |
| **R-ML** | stellar M/L (0.5, counted ±20%; A10) | P3, P4, P12, P15 | — | — | the ML_3p6 alternatives are NOT_EVALUATED_BEFORE_FREEZE (slots V003) | DT-ALT (M/L; NOT_EVALUATED, so OPEN); DT-T1a (diagnostic, jointly with R-SPEC) |
| **R-SPEC** | a species or history weight (SA-BH-01) | P3, P4, P12, P15 | — | — | — | DT-T1a (diagnostic, jointly with R-ML) |
| **R-GEO** | geometry (A23): the distance scale | P3, P4, P12, P15; P6 | — | — | — | DT-GEO (NOT_EVALUATED; OPEN by construction) |
| **R-TSR** (numerical) | a MISS on a flagged row may reflect the residual cube-corner anisotropy of the kept cube (K = 2) (A66.2) | P10 | — | — | against: route B consumes the azimuthal mean, so the φ-spread S enters no row directly (A66.2; A42 TESTED) | DT-TSR (NOT SCHEDULED) |

**The sign rule for the deficit-type readings, R-UT1 and R-REACH.**
- **Why they are deficit-type.** Their registered content is missing long-range attraction, which can only lower the outer rotation: "missing reach" (A12.3); A20 places "the tail question" in the k = 0 typing; and A41 names the small-k limits at larger L as one of the two routes left to supply outer rotation that static present-mass gravity cannot.
- **The rule.** When OUTER_FAILURE holds, their score relation is CONSISTENT if S(OUTER) is DEFICIT or CENTERED and at least one non-INVALID OUTER MISS row has s_q = −1. Otherwise it is NOT_ADDRESSED with one code:
  - SIGN_SCOPE_EXCESS, under P2;
  - SIGN_SCOPE_UNSIGNED, under P14;
  - SIGN_SCOPE_NO_DEFICIT_MISS, under P11 when no OUTER MISS row is a signed deficit.
- **They stay open.** Part 2 is still the deciding-test status (OPEN), so both readings stay open for every outer-row failure, as A15 E3 requires. They are always reported, never dropped. R-HIST, the third E3 reading, is sign-free, because A10 reads every miss two ways.
- Root item M-4 offers the alternative: both readings sign-free.
- **The INNER readings are sign-free.** An error in G_eff transfer, M/L, a species weight, the geometry or the m = 0 projection can move the inner rows either way, so P3, P4, P12 and P15 carry the same readings.

**Patterns with no reading of their own.**
- **P5.** Its OUTER rows are read under OUTER_FAILURE, that is, by the readings of the OUTER pattern that holds (P1, P2, P11 or P14). Its TRANSITION rows are read under P13. P5 implies both (§2).
- **P8.** No miss reading. If N_v(OUTER) ≥ 1 and M(OUTER) = 0 (OUTER_NO_MISS), the result runs **against** the A15 E2 expectation and is reported as such.
  - **A mandatory report:** ORIGINAL_K's twin classification for OUTER (§6.1), and the T120L C3 record (A27).
  - That record must be pinned before the freeze; otherwise that half reads NOT_AVAILABLE (M-13).
  - Neither half changes the headline or any status.
- **P9.** The outer test is unavailable: every OUTER row is INVALID. E2 reads NOT_TESTABLE, and so does the E3 line. No reading is triggered under P9 alone. DT-S0G, if evaluated, is still reported in §6.3. Answering it is the outer-gas confinement question (A12.5), not a rotation-row test.
- **P0.** No reading (§4).

**Descriptive lines (no status effect).**
- **Onset radius:** the smallest R_q of a MISS row in TRANSITION ∪ OUTER. It is reported with k* (A12: wavelengths of tens of kpc) as a comparison only.
- **R-ML and R-SPEC:** a DT-T1a trend, when it has been computed before the report, is shown here under both together, never under one alone, and labelled diagnostic. DT-T1a varies f★ for a correlation and moves no prediction (A10, A16.3).

**BH-T1a is used as registered, diagnostic only [C-3.3].**
- The rank correlation and slope of r_q against f★(R) bear jointly on M/L and on a species or history weight.
- They are not a verdict on Bind history alone (A10).

## 4. INVALID-as-miss rows [C-4]

**What makes a row INVALID.** A row is INVALID_AS_MISS exactly when the reference member's frozen row carries a roster-authorized INVALID registration (0531, ruled in A56: the v003f B1 closure; v003g `_authorized_row_registration`). There are two kinds:

| kind | rows | source |
|---|---|---|
| built-in QUERY_INSIDE_INNERMOST_NODE | primary GL4, slots V002/V003: Q01, Q02 | root decisions V001 N1 and V002 A4; slots `invalid_primary_GL4` |
| built-in QUERY_BEYOND_OUTER_GAS_CUT | the outer-gas cut rows: {R_q ≥ first_unconfined_R} from the pinned v011 cut record | A12.5, A14 C3; the A60 cut binding |
| built-in QUERY_OUTSIDE_RETAINED_SUPPORT | the gap rows: queries between the last retained route-B node and the pinned outer cut | A60, gap rows |
| a root-listed gate's own reason | rows the producer reported INVALID **and** that the pinned gate document lists for that reason | 0518 item 2; v003g `root_gates`. A gate may not use a built-in reason (ROOT_ROSTER_BUILTIN_REASON_MUST_DERIVE_FROM_RULE). |

**Rules for the INVALID set:**
- Built-in reasons derive only from their rules.
- A gate authorizes INVALID; it does not require it. A gate-listed row that the producer reports valid is scored normally.
- **Per member.** Under PER_THETA cut contexts the INVALID set can differ between members. The PRIMARY classification uses the reference member's set, and a twin uses its own.
- **Integrity (v003f/v003g).** A finite value on a row the rules make INVALID refuses. An unrostered INVALID refuses. Reasons and gates come from the roster only (0531).

**Registration timing.**
- Root registers the rosters during the two-pass freeze, before any target access (RUNBOOK_V001 steps 1–8; 0545 F5; ruled in A62):
  1. the first pass saves the raw results and the v011 cut records;
  2. root registers the rosters;
  3. the second pass replays exactly.
- **ON-TIME and LATE gates.** A root-listed gate is ON-TIME if and only if the sha256 of its gate document is pinned in a root entry stamped (`date -u`) before the first step-5 launch receipt. Every other root-listed gate is LATE.
  - Under RUNBOOK_V001, gates are approved at step 4, after step 1 has saved the step-5 raw results. So **every gate first adopted at RUNBOOK step 4 is LATE.**
  - **The gate-status list.** The seal or score entry lists every gate pin, with its status (ON-TIME or LATE) and the entry that pinned it. The list is a classifier input (M-5, M-15). A root-listed gate missing from it stops the classification before target access (GATE_STATUS_LIST_DEFECT, §1.1).
- **How a LATE gate is read.**
  - Its rows still score INVALID_AS_MISS in LADDER, and the report marks them GATE_AFTER_PREDICTIONS.
  - For this document's counts and patterns, each LATE-gate row is a non-INVALID MISS row with no defined ratio. It counts in N_v(Z), M(Z) and U(Z), and it is left out of m(Z) and Δ_out. It carries no sign, no NEAR flag and no P10, and no reading cites it.
  - Built-in reasons are unaffected. The same rule applies to a twin's gate rows (§6.1).
- **What a LATE gate changes, relative to registering the same gate on time** (FORMAL; TESTED on synthetic outcomes, see the clause map):
  - It never lowers N_v(Z) or M(Z), and never changes H(Z), m(Z), Δ_out or a row's LADDER tier. It never removes miss-domination or OUTER_FAILURE; it can remove hit-domination.
  - A defined S(Z) stays the same or becomes UNDEFINED, and an UNDEFINED S(Z) stays UNDEFINED. A LATE gate never creates or switches a sign class; it can only withhold one.
  - It can remove P0, P1, P1g, P2, P3, P4, P5, P6, P7, P8, P9, P11, P11g or P12, and it can add P5, P7, P13, P14 or P15.
  - It never adds P0, P1, P1g, P2, P3, P4, P6, P8, P9, P11, P11g or P12. It never removes P13, P14 or P15, and it never changes P10.
  - A signed zone pattern it removes is replaced by its zone's unsigned pattern: P1, P2 or P11 by P14, and P3, P4 or P12 by P15.
  - The E3 line can move from NOT_NEGATIVE_AT_OUTER or NOT_TESTABLE to TESTED-NEGATIVE, never the other way. A deficit-type reading can lose CONSISTENT, never gain it.
  - So every change goes toward more misses, or from a signed to an unsigned reading of the same failure.

**Scoring and reporting.**
- INVALID rows are scored as worst-tier misses and counted in the 43 (0518 items 1–2). D1 is applied over the registered-valid rows only (0518 item 3).
- INVALID rows are listed separately, per reason, with each row's zone and, for gate rows, the gate's status.
- For the outer-gas cut, the report also gives the pinned cut record's truncation radius and dropped HI mass fraction (the V001 §4 requirement).

**No part in the readings.**
- INVALID rows are excluded from N_v(Z), from m(Z), and from every pattern except P0 and P9. Every INVALID OUTER row counts toward P9. (A LATE-gate row is counted as above, not as INVALID.)
- The only statement made about an INVALID row is its roster reason. No reading cites an INVALID row as evidence for or against anything.
- No roster change is allowed after targets are opened. Any later root ruling on a roster row is recorded as post-score and does not change this classification.

## 5. Comparison with the A15 expectations (after the score; labelled COMPARISON, never a fit)

**E1, inner disc [C-5.1].**
- **(a) The deciding observable A15 E1 names:** the inner rows against their bands.
  - Report H(INNER), M(INNER) and N(INNER).
  - As a sub-table, report the rows Q03–Q15, which A15 E1 names "or so".
  - Label: "COMPARISON with A15 E1".
- **(b) The expectation itself:** whether the frozen model rotation exceeds the frozen baryonic-Newtonian rotation at the INNER rows.
  - This is model-internal; it involves no target.
  - It is made only from a target-free carrier pinned before the freeze (root item M-11). v003g has no such field. Without a carrier, part (b) reads NOT_AVAILABLE.
  - It is never computed after targets are opened. No baryon column of the observational data table is ever used.

**E2, outer disc [C-5.2].**
- Report:
  - OUTER_FAILURE (P1, P2, P11 or P14, with the sign class);
  - OUTER_NO_MISS (N_v(OUTER) ≥ 1 and M(OUTER) = 0);
  - P9;
  - the OUTER INVALID counts per reason, and the OUTER LATE-gate count. A15 E2 foresaw outer rows becoming INVALID through route-A outer-gas unconfinement.
- Label: "COMPARISON with A15 E2".

**E3, the verdict line [C-5.3].** One line, always reported, computed on the frozen reference member. Its value is one of:
- **TESTED-NEGATIVE (A15 E3 scope)**, if and only if OUTER_FAILURE holds;
- **NOT_NEGATIVE_AT_OUTER**, if N_v(OUTER) ≥ 1 and OUTER_FAILURE does not hold;
- **NOT_TESTABLE**, if N_v(OUTER) = 0 (P9).

The line always prints S(OUTER) and Δ_out; N_v, H, M, U, N and I per reason for OUTER; and how many OUTER rows have a defined ratio, how many are LATE-gate rows and how many are null-ratio rows. Under FREEZE_INCOMPLETE or N_GATE_NOT_OPEN it carries PROVISIONAL with its reason. It is printed even when the classification reads NOT_READ (§1.1).

**Never an adjustment [C-5.4].** No expectation is adjusted, and no row is re-read, to improve agreement.

## 6. Alternatives (scored separately; never the headline)

### 6.1 Evaluated non-PRIMARY alternatives: the twin rule [C-6.1]

v003g requires every evaluated alternative's members to equal the PRIMARY's selected representatives, in log_index, role and order. It scores those members, but selects no reference member and band-scores no alternative envelope. So:
- **The twin.** An alternative's twin is its member with the same `log_index` as the frozen PRIMARY reference member. One exists by construction.
- **A valid twin** has `member_valid = true`. Otherwise the alternative reads TWIN_INVALID, and only its scored member distribution is reported.
- **Classification.** A valid twin's rows are classified INVALID_AS_MISS, HIT or MISS by M-T, using the twin's own INVALID set and the §4 LATE rule for its gate rows. There is no NEAR flag, and no TSR flag: P10 is never evaluated for an alternative, because the N-tests ran on the PRIMARY operator and grid.
- **Id check.** The twin's ids must equal its scope: Q01 to Q43 for a full-row alternative, or `scoring_scope.query_ids` for STAGE0. A mismatch reads TWIN_INPUT_DEFECT.
- **Summaries and patterns** for an alternative use the §2 rules (with N(Z) = 0 and no P10) and are reported under its name.
- **Limits on use.** They never trigger, confirm or refute a PRIMARY reading. The only exceptions are the P8 report, which names ORIGINAL_K, and §6.3 for STAGE0_GRID_OUTER and R-DRIFT. TWIN_INVALID and TWIN_INPUT_DEFECT leave R-DRIFT OPEN (§6.3).
- Root item **M-10**.

### 6.2 Alternatives not evaluated before the freeze [C-6.2]

Only the status is reported: "NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline". This covers:
- ML_3p6_0.4, ML_3p6_0.6 and GL10_SOURCE_GAUSS_ORDER;
- any recorded distance alternative;
- STAGE0_GRID_OUTER, unless it is evaluated under §6.3.

### 6.3 STAGE0_GRID_OUTER [C-6.3]

**At writing:** NOT_EVALUATED_BEFORE_FREEZE; headline false; scope OUTER Q36–Q43 (R ≥ 30 kpc, inclusive); grid `bdb9016c…`.

**When it is evaluated (the receipt rule; root item M-14 states the same rule).**
- STAGE0 is EVALUATED_BEFORE_FREEZE if and only if both hold:
  - **(a)** every registered STAGE0 member has a FINISHED receipt before RUNBOOK step 4 begins;
  - **(b)** the prepared STAGE0 slots/module successor is pinned by sha256 in the seal entry, or, under the Status fallback, its sha was published before the first step-5 output value was read.
- Root records the step-4 start time and every receipt time.
- When (a) and (b) hold, the pinned successor is adopted with no further decision. If it refuses a STAGE0 record, STAGE0 reads EVALUATED_REFUSED.
- Otherwise STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (A65.2), with the reason RECEIPTS_AFTER_STEP4 if (a) fails, or NO_SEALED_SUCCESSOR if (b) fails.
- Validity booleans and output values never change the status, and root reads no prediction value to decide it.
- A STAGE0 result that first becomes available after RUNBOOK step 4 begins is EXPLORATORY (post-score), and R-DRIFT stays OPEN.

**If it is evaluated:**
- It is scored on its 8 rows, denominator 8, separately from the headline.
- It is labelled "SENSITIVITY: coefficient-grid sensitivity at fixed calibrated parameters (A65), not a recalibration". The label is used only when it is evaluated.
- It never enters the headline, and never re-tiers a PRIMARY row (A65.1).

**Comparison rule** (registered here; root item M-9). Restrict to the OUTER rows that are non-INVALID under both the PRIMARY reference member and the valid STAGE0 twin, and have a defined r_q under both. On those rows:
- H_P and H_S are the HIT counts of the reference member and of the twin;
- A_P and A_S are the medians of |r_q| for each.

The comparison reads:
- **CONSISTENT** with R-DRIFT if H_S > H_P.
- **AGAINST** R-DRIFT, as an explanation of the outer misses at fixed calibrated parameters, if H_S ≤ H_P and A_S ≥ A_P.
- **NOT_DECIDED** otherwise, including when no row qualifies.

**The mapping to R-DRIFT's tuple** (closed). Part 1 is shown for an outcome where OUTER_FAILURE holds; otherwise part 1 is NOT_ADDRESSED (PATTERN_NOT_HELD).

| STAGE0 status or comparison | R-DRIFT part 1 | R-DRIFT part 2 |
|---|---|---|
| CONSISTENT | CONSISTENT | CONSISTENT (DT-S0G) |
| AGAINST | INCONSISTENT | AGAINST (DT-S0G) |
| NOT_DECIDED | CONSISTENT | OPEN (NOT_DECIDED) |
| TWIN_INVALID or TWIN_INPUT_DEFECT | CONSISTENT | OPEN, with the code |
| NOT_EVALUATED_BEFORE_FREEZE or EVALUATED_REFUSED | CONSISTENT | OPEN, with the code |

**Limits:**
- TWIN_INVALID, TWIN_INPUT_DEFECT and NOT_DECIDED leave R-DRIFT OPEN.
- The comparison never makes R-DRIFT supported. The stage-0 grid failed its R-hat criterion (S0-FAIL-RHAT), and A65 check R-3 leaves the causal gloss UNTESTED.
- Row by row, the report also gives r_q under both members, and the STAGE0 member within-error distribution.

## 7. Disclosures required by A63, A65.4 and A66 [C-7]

**D-1. The stage-0 outcome** (A63; A65.4):
- **Outcome.** S0-FAIL-RHAT, the sealed outcome name. Analysis v003 completed 8/8.
  - The maximum R-hat is 1.48, and 95 of 778 columns have R-hat above 1.1.
  - R-LIT and R-MA fail; the background passes.
  - The wiring reads WIRING_CHAIN_SPECIFIC.
- **The sealed k = 0 lapse drift reading is SUPPORTED.** Its precondition holds: census/U is flat in all 8 processes.
  - Stage-0 |h_NN(0)| is 1.90 ± 0.11.
  - A2's value is 3.551.
  - The stage-0 value is below A2's value minus 2 SE.
- **Its causal gloss, "drift inflated A2", is UNTESTED.** Stage 0 differs from the same-kernel BIRTHK about as much (relative distance 0.451) (A65 check R-3).

**D-2. The coefficient-grid difference** (A65):
- **Distance from A2.** The stage-0 pooled grid (`bdb9016c…`) differs from A2 (`2e3a36d8…`) by relative distance 0.477 globally and 0.483 at the k = 0 node. 93.6% of its entries lie more than 2 band-SE from A2.
- **h_NN(0).** It is −1.899 ± 0.106 against −3.551.
  - The gap is 15.6 SE, counting only the stage-0 SE.
  - A2's own single chains span −5.20 to −1.76, which brackets the stage-0 value.
- **A2 stays the headline grid.**
- **A counted uncertainty.** A65.4 makes D-1 and D-2 together a counted coefficient-grid uncertainty for every row.
  - The report states it in its header and in the notes column of every row.
  - It is not converted into a number. It does not widen σ_q (I-2), and it changes no tier.

**D-3. The N1 residual** (A66; 0550; A90):
- **Where N1 fails.** N1 fails strictly at one ring: TRUNCATION_SHAPE ordinal 15, R = 10.54 kpc, S/θ 1.0148 at K_big 16 and at 32.
- **Why.** The residual comes from the kept-cube (K = 2) corner shape, not from the tail. The other TRUNCATION_SHAPE rings pass. Without the tail, these rings were at 1.1–3.7 θ (A14 C4 / A17).
- **Flagged rows.** Under the §1.4 rule, the one flagged row is Q25. Q26 is not flagged.
- **When it was ruled.** The A66 consequence was ruled after the N1 diagnostic had been seen, and A66 labels it so. R-TSR and the §1.4 rule are registered after that diagnostic, and before any prediction or target exists.

**D-4. The NGC numerics.** The I-6 values at the score step, with their record shas:
- the production compare: outcome, gate and reason codes;
- LO_NGC_K32_CERT_V001;
- GQ_NGC_91_MS96, and the gas M_s used;
- EPS_CERT_NGC91;
- I1T_NGC_T120L;
- the DOUBLING NGC half;
- the record that closes the A90 LO I1-T precondition (A101; Codex1 0066), with its stated scope.

## 8. Report format (score step) [C-8]

The report gives:
1. **The header:**
   - the sealed sha of this text;
   - the freeze manifest sha, the registration sha, and the expected manifest sha logged at the freeze;
   - the slots, module and roster shas;
   - the TSR records: the flag record and the support record, the compare (`6f095f64…`), the N1 record (`8867c376…`) and the GL-node record (`ec1dcca5…`);
   - the classifier sha (M-12);
   - the gate-status list (§4);
   - the STAGE0 status with its reason, the step-4 start time and the receipt times (§6.3);
   - the V005 whole-file sha at assembly and the sha of `V005_ENTRY_TABLE_R3.json` (§11);
   - the I-6 values, with their record shas (D-4);
   - the freeze status (I-7);
   - disclosures D-1 to D-4;
   - the timing attestation of the Status section, with the validity facts seen before the seal, and, under the fallback, the pre-prediction shas.
2. **The per-row table:** Q_id, zone, R_q, tier, r_q, sign, whether the row has a frozen prediction, the NEAR flag, the TRUNCATION_SHAPE_RESIDUAL flag, INVALID reason (with GATE_AFTER_PREDICTIONS where it applies), sensitivity band overlap (yes / no / invalid, conditional on trial values), and notes (the D-2 counted uncertainty).
3. **The zone summaries** (U(Z) included), OUTER_FAILURE, and the E3 verdict line (§5.3).
4. **Every pattern and flag that holds.**
5. **Every registered reading,** in §3.2 order, with its triggers that hold, its row scope and its full status tuple, with any NOT_ADDRESSED code, and each deciding test's status.
6. **The INVALID list,** per reason, with the cut record's truncation radius and dropped mass fraction.
7. **The A15 comparisons** (§5).
8. **The alternatives** (§6). STAGE0_GRID_OUTER comes last, labelled SENSITIVITY only if evaluated.
9. **Any EXPLORATORY (post-score) readings,** labelled as such.
10. **Under the fallback:** the classification under the pre-prediction versions, and every POST-PREDICTION change with its diff.

**The words used:**
- "TESTED-NEGATIVE" is used only for R-MF, within its stated scope. The one exception is quoting a registered outcome name verbatim.
- "consistent with" is never written as "supports".
- "SUPPORTED" is used only when quoting the sealed k = 0 drift reading of A63.

## 9. Self-check: could any rule be steered by the outcome? [C-9]

| risk | how it is closed here |
|---|---|
| Ruling the root items, or sealing, after the predictions are readable | The Status timing rule: seal before anyone reads any step-5 output value, with validity-only reads until then and an attestation listing the validity facts seen. Step 5 is never delayed for the seal. Otherwise the pre-prediction versions (text, root items, classifier) apply by sha; later changes are POST-PREDICTION with their diff, and the deviation is disclosed. |
| Moving the zone boundaries or memberships | The cuts are numbers fixed in §1.3, and membership is fixed by query id. A mismatch stops before target access. |
| Redefining HIT, MISS or NEAR after seeing residuals | The tiers use only frozen LADDER fields and the quoted σ (§1.1). NEAR is a flag on tier-MISS rows with a valid envelope row, and it changes no count. |
| Choosing which member is scored | The frozen reference member, checked against the manifest (REFERENCE_MEMBER_MISMATCH). Alternatives use the twin rule (§6.1). |
| Choosing which pattern to report | Every applicable pattern is reported. The coverage property is proved case by case for each zone (§2): the unsigned patterns P14 and P15 cover a miss-dominated zone whose signed misses do not reach half, and ties go to the stricter side. |
| Taking a zone's sign from its hits | S(Z) is UNDEFINED unless the signed misses alone reach half of N_v(Z) (§2). |
| Choosing a reading's status word | One tuple rule per reading, independent of the trigger. Every registered reading is listed every time, against takes precedence, and NOT_ADDRESSED occurs only in its coded cases (§3). |
| Dropping an outer-row reading for an awkward sign | The A15 E3 rule: R-MF, R-UT1, R-REACH, R-HIST and R-DRIFT are triggered by every OUTER_FAILURE. A deficit-type reading under an excess or an unsigned outer reads NOT_ADDRESSED with its code; it is never omitted (§3). |
| Upgrading "consistent" to "supported" | Prohibited (§3). DT-S0G never makes R-DRIFT supported (§6.3). |
| Choosing whether the R-MF verdict applies | One sign-free trigger, OUTER_FAILURE, equivalent to exactly one of P1, P2, P11 or P14 and printed in the E3 verdict line (§2, §5.3). |
| Re-explaining INVALID rows | Prohibited (§4). |
| A gate added after the predictions changes the reading | LATE is decided mechanically: a gate not pinned before the first step-5 launch receipt is LATE, and every gate first adopted at RUNBOOK step 4 is LATE. LATE rows count as unsigned MISS rows. Relative to the same gate on time, a LATE gate never removes miss-domination or OUTER_FAILURE, never creates or switches a sign class, never moves the E3 line toward a favourable value, and never makes a deficit-type reading CONSISTENT; its exact effects are listed in §4. |
| Suppressing the classification after the targets are seen | NOT_READ is allowed only when a stop condition, re-run on the real score, fires. The output is still computed and published, and the E3 line is printed (§1.1). |
| Evaluating STAGE0 only if it helps | The receipt rule: FINISHED receipts before RUNBOOK step 4 and a successor pinned in the seal entry, then adoption with no further decision; validity booleans and values never change the status (§6.3). |
| Flagging rows TRUNCATION_SHAPE_RESIDUAL after seeing misses | The overlap rule is derived from the registered node, interpolation and column-locality facts, the flagged ids are fixed by id in §1.4, and any disagreement is the pre-target stop TSR_FLAG_TABLE_MISMATCH. |
| Choosing K_big, M_s or certificates after targets | All are fixed before step 5 (A64; A81 RI-23; Codex1 0032; A90; A101). The header records them (I-6, D-4). |
| Root discretion after a stop condition | Every stop is checked before target access. Afterwards, only a key-renaming field map or a triggered NOT_READ (§1.1). |
| Authorizing a FREEZE_INCOMPLETE score after the predictions are readable | The decision is recorded before any step-5 output value is read, or fixed by the seal; a later authorization is EXPLORATORY (I-7). |
| A later re-score | Only the first successful score is classified; later ones are EXPLORATORY (I-7). |
| Selective display of the sensitivity band | One fixed column for all 43 rows; never used for a tier or reading (§1.1, §8). |
| Dropping rows or inflating σ | Prohibited (I-1, I-2). The grid uncertainty does not widen σ (D-2). |
| **Residual risk (not closed): consequences of registered choices.** | They are recorded so that root rules knowingly (M-3, M-9, M-15). (i) With N_v(OUTER) = 1, one missing valid OUTER row gives OUTER_FAILURE and the TESTED-NEGATIVE verdict. (ii) A twin that gains one hit reads CONSISTENT, whatever happens to the other rows. (iii) A twin that shrinks every residual but gains no hit reads NOT_DECIDED, not AGAINST. (iv) An OUTER zone whose non-INVALID rows are all LATE-gate rows reads P14 and TESTED-NEGATIVE with no OUTER prediction, while the same rows gated on time read P9 and NOT_TESTABLE. (v) Under the §2 sign rule, a zone's sign class depends on whether its gates are LATE: a LATE gate can only withhold a sign class (M-3 records the alternative rule). |
| **Residual risk (not closed): NEAR depends on the envelope width,** which depends on the member-selection rule. | That rule is frozen with the manifest. NEAR is a flag and changes no pattern. |

## 10. Root items for this prereg (decide before the seal) [C-10]

Each item's recommended ruling, with its reasoning, is in `ROOT_ITEMS_R3.md`. Items M-1 to M-5 are V001's five pending items; M-6 to M-14 are new in r2; M-15 is new in r3.

| item | subject |
|---|---|
| M-1 | Tiers, and the NEAR flag (§1.1) |
| M-2 | Zone cuts and the membership table (§1.3) |
| M-3 | Pattern thresholds, exclusivity, the sign-class rule, OUTER_FAILURE, the patterns P11–P15 with their flags, and the coverage proof (§2) |
| M-4 | Deciding tests NOT SCHEDULED; the status tuple, the A10 and A15 E3 rules, and the deficit-type sign rule (§3) |
| M-5 | Score inputs and field names (v003g), and the carriers |
| M-6 | The seal: vehicle, timing, the fallback versions, the attestation, cited entries and later entries |
| M-7 | The TRUNCATION_SHAPE_RESIDUAL overlap rule, its support record and its carrier |
| M-8 | Scoring a FREEZE_INCOMPLETE manifest |
| M-9 | The DT-S0G comparison rule |
| M-10 | Alternative classification: the twin rule |
| M-11 | The A15 E1(b) baryonic-Newtonian carrier |
| M-12 | A mechanical, sealed classifier, binding at the score step |
| M-13 | A pinned T120L C3 record for the P8 report |
| M-14 | The STAGE0 receipt rule, and the evaluated-STAGE0 successor |
| M-15 | LATE gates: the definition, the gate-status list, and an all-LATE outer zone |

## 11. Sources (sha256 from bytes at writing) [C-11]

**Dispatches** (`/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/`):

| item | sha256 |
|---|---|
| 0512 | `adac97bbf1884f932b1b046f2d1f04b404a15d019ea840f000b34b58ad45d190` |
| 0518 | `0748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279` |
| 0519 | `@@SHA_0519@@` |
| 0521 | `@@SHA_0521@@` |
| 0522 | `30af5d6811788e9bbed4c470dae0ea9bb4ae5230a734fa7940e942b30ed66160` |
| 0523 | `@@SHA_0523@@` |
| 0524 | `d1430abc84025cc4afde31f3fd4fce1845e8d2334e47e95fbeb81936d7dfd4df` |
| 0531 | `7233faf3be6d498a662f9f3dcc743c12420bbc6fa997e606aeb72e7d16ca3cd6` |
| 0535 | `e4bf99106e2d4eae00e2be0ed1b596b0450225bfffe2ac717386f0c13db22f54` |
| 0545 | `4049a3f81b524f5622e0eda6510eeee60c7a6b10fea97ea6c648d0b9698b84a5` |
| 0546 | `5390d9c3c9e7a76bfbfe97de6806b2aa922aa4e53115dcff11bbe0fe39540ca6` |
| 0548 | `7bf03716c95fc9d9ae06ebb038c69b6e9ed8452f2414919b35cae20365decace` |
| 0550 | `5c686ae8fd82cea995fcdd1ed5bff2d0d688514c45582871cb2b97f231b8b457` |
| 0585 | `9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd` |
| 0606 | `dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e` |
| 0619 | `238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99` |

**Lane posts:**

| post | path | sha256 |
|---|---|---|
| Codex1 0032 (GQ_NGC at M_s 96 holds) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0032_2026-10-18_gq91_pass_and_latest_rulings.md` | `3e8c9fc9e65a10791f8ecbda3702556a851391350f06ed013222bd12876ab2f7` |
| Codex1 0056 (the formal K32 result) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0056_2026-10-18_ngc_k32_complete_n_fail_n1_a66_open.md` | `4b67319dddb4799e71420881f6624fdcd1640cd5f560a4adce06cd2030af72aa` |
| Codex1 0058 (the steps 6–7 rehearsal) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0058_2026-10-18_0603_synthetic_steps6_7_finished.md` | `fc5af8318febd8dd86037d7aeddff9a590ea8e436deb15f002b9c4775c65cea2` |
| Codex1 0066 (the LO I1-T star-transform convergence, TESTED PASS) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0066_2026-10-18_tail_transform_finite_convergence_finished.md` | `f2d946559d6b2abb0563f10c2e0c297a3e004477b87e7cd9958c2cca679647ff` |
| Codex2 0490 (the cross-lineage review of r2 round 2) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0490_2026-10-18_miss_reading_r2_round2_review_finished.md` | `3a922168f800de5ae9fff2ba1cb55af2f55d7ae4290a75b14a0ca2daa36a2649` |
| Codex3 0618 (the step-5 carriers) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0618_2026-10-18_dispatch0606_carriers_finished.md` | `8939c004e4bea1728eed610e4d98b98dffbe4333be1433c539feb16159de60a7` |

**Root decisions** (`…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00n[_ADDENDUM].md`):

| addendum | entries used | sha256 |
|---|---|---|
| V003 (frozen) | A10, A12 | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` |
| V004 (frozen) | A13, A14, A15, A16, A17, A20, A21, A23, A27, A41, A42 | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| V005 (open; it closes at the V007 freeze, A82) | the entries in the next table | `@@V005_SHA@@` (whole file, read at assembly) |

**V005 entries: the entry table.**
- **The record.** `V005_ENTRY_TABLE_R3.json` is hand-written. It has one row for every heading line of V005 that starts with `## `, each exactly once and in file order, suffix and amendment forms included. Each row is either CITED_PINNED, with the sha256 of its section, or NO_CHANGE, with the reason it changes nothing here. It records the V005 whole-file sha256 and the `date -u` time at which it was read. The generator renders it below and verifies it; it never writes a reason.
- **Why per-entry pins.** The V005 file is still open, and root keeps adding entries to it. So each cited entry is pinned by the sha256 of its own section: the bytes from its heading line up to the next `## ` heading line, or up to the end-marker shown.
- **The checks.** The target-free check (T5) re-extracts the cited sections from the current bytes. Check T7 fails on any `## ` heading line that has no row, or that differs from its row.

| entry | used for | ends before | section sha256 |
|---|---|---|---|
@@V005_ENTRY_ROWS@@

**Read with no change to this text:** @@V005_UNCITED@@. From V005, V001 cited only the A48 principle and the 0518 log, which sits in the pinned A65 section.

**Freeze, slots, nodes and carriers** (`/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/`):

| file | sha256 |
|---|---|
| `freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` (`_ladder_row`, `_score_members`, `_band_rows`, `_pointwise_envelope`, `_alternative_score_scope`, `_score_members_on_rows`, `_authorized_row_registration`, REGISTERED_INVALID_REASONS, WITHIN_ERROR_RULE, HEADLINE_RULE, REFERENCE_RULE) | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| `freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` (alternatives; query block; observation rule; STAGE0 registration) | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` |
| `freeze_score_readiness_cx3/v003g/RUNBOOK_V001.md` | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` |
| `ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (the GL4 node radii) | `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` |
| `step5_ngc_route_ab_readiness_cx3/carriers_0606_v001/tools/extract_carriers_cx3v005.py` (Codex3's carrier extractor; the TSR support-record schema) | `50c7db5fbc2eb2cce17dcbb53ba1186bfdbc635a4098b0eb33ebd1402829732f` |

**Target-free query manifest** (the source the slots cite): `…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json`, `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494`.

**Coefficient grids:**

| grid | path | sha256 |
|---|---|---|
| A2 (headline) | `…/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz` | `2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7` |
| stage-0 pooled (STAGE0_GRID_OUTER) | `claude_artifacts/stage0_grid_gate_c2/candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz` | `bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5` |

**NGC N-test and certificate records** (target-free model numerics):

| record | path | sha256 |
|---|---|---|
| the production-K_big compare (the N-test record of record) | `claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json` | `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9` |
| the production-K_big N1 record (ring radii) | `claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json` | `8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70` |
| GQ_NGC to 91 at M_s 96 | `claude_artifacts/ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json` | `be148bab4d80ef412d55d2011cac2e3a1d44725a0ba21a4d2bf43c7ffbdc1a76` |
| LO_NGC to 91 (the N-test record, A90) | `claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json` | `07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382` |
| EPS_NGC to 91 | `claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json` | `1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d` |
| NGC I1-T (T120L) | `claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json` | `3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6` |

**Review records:**

| record | path | sha256 |
|---|---|---|
| round-2 recheck lens R2-B (column locality of the route-B node values, TESTED from the module bytes) | `claude_artifacts/miss_reading_prereg_c4/r2/checks_round2/newdefects/REVIEW.md` | `5b7c8b488f85bff551b47df5d83ed4904d86936cd51188c32dd5840bf4e4b3f3` |
| Codex2's r2 prep checklist (the M-12 case classes) | `claude_artifacts/review_miss_reading_r2_cx2/prep/CHECKLIST_CX2V001.md` | `020ef3f18e125c59bf417cc143b571f44683d43e7fc8735440de4defd7d8399a` |

**Claude4's own:**

| file | sha256 |
|---|---|
| `claude_artifacts/miss_reading_prereg_c4/PREREG_MISS_READING_V001.md` | `6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345` |
| `claude_artifacts/review_freeze_v003g_c4/REVIEW_FREEZE_V003G_C4V001.md` | `575f872c00c22a00eb29a97eac7e594562b1e07843354baa110674702c4c68a4` |
