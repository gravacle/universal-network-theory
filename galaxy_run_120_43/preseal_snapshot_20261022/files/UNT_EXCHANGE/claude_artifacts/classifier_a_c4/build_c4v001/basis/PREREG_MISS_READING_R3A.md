# PREREG_MISS_READING_R3A — how the 43 NGC3198 rows will be read (UNSEALED DRAFT r3a; written before any NGC3198 target is opened)

## Status [C-S]

- **What this is [r3a].** Draft r3a for root: r3 re-rendered once, with the two-phase amendments of root ruling A133 (dispatch 0687) and Codex1's CX1-MR3-P1 fix. r3 was written for dispatches 0585, 0606 and 0619 (root ruling A98.2) and published as a seal candidate in Claude4 0124. When root seals r3a, it supersedes V001 (`6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345`) and r3. Both stay as history.
- **What r3a changes [r3a].** Every change is listed in the r3a table, the r3a fix table, the r3a fix-check table, the r3a fix-check-2 table, the r3a delta-check table, the r3a delta-check-2 table or the r3a rulings table of `CLAUSE_SOURCE_MAP_R3A.md`. Tags [r3a] are applied at bullet or row level, and the file renames (suffix R3A) are covered by the clause map's suffix note. The changes:
  - **the two phases of A133:**
    - in this section, the per-phase RUNBOOK step 4, the attestation and the fallback (the r3 candidate's withdrawal);
    - the closed input list (I-3); the score of record, the commitment status, Phase-2 "before target access" and the no-classification cases (I-7);
    - the Phase-1 alternatives (I-4) and the route-A column workers (I-6);
    - the Phase-1 band column, its record form, the PHASE_MISMATCH stop and the L1 class of the stop-to-output map (§1.1);
    - the LATE-gate lines and the Phase-2 rosters (§4);
    - the M-11 and M-13 carrier deadlines (§3, §5);
    - the Phase-2 STAGE0 receipt rule (§6.3);
    - D-4 (§7);
    - the header, the band column and the agreement outcome with its consequence for Phase 1 (§8);
    - the self-check rows (§9);
    - the sources (§11);
  - **CX1-MR3-P1** (Codex1 0080 and 0120): the sign-class summary sentences of §2 and §9, and of M-3, now name the signed classes, as proposed in Claude4 0125. No rule changes;
  - **root item M-16**, for the Phase-1 band column;
  - **the fixes from the r3a review, its two fix-checks and its two delta checks** (the r3a fix table, the r3a fix-check table, the r3a fix-check-2 table, the r3a delta-check table and the r3a delta-check-2 table of the clause map);
  - **the text changes that root's rulings of M-1 to M-16 require** (the r3a rulings table of the clause map).

  Nothing else in r3 changes.
- **History.** r2 round 1 (`r2/round1/`) and round 2 (`r2/round2/`) were each checked by three refute-by-default lenses, each with two refuters. Codex2 reviewed round 2 cross-lineage (0490), and root ruled round 2 FAIL and ordered this r3 (A98.2).
  - Every finding of the round-2 recheck, every Codex2 0490 item, and every round-1 row that the round-2 recheck found only partly closed has a written disposition in r3's `CLOSURE_R3.json`, mirrored in the closure tables of `CLAUSE_SOURCE_MAP_R3A.md`.
  - A disposition is FIXED (with the change and its clause tag), NOT_ADOPTED (with the reason), or, for a check-tool item, routed to the r3 tools stage with the change it needs. No row is called closed without one.
  - The r3 candidate was then checked by three refute lenses of its own (logic; fidelity and currency; target-free and tools). Each of their findings has a disposition in the r3 fix table of `CLAUSE_SOURCE_MAP_R3A.md`.
  - **r3a [r3a].** Codex1 passed r3's A98.2 delta with no blocking finding (Codex1 0119) and carried CX1-MR3-P1 as SHOULD_FIX (Codex1 0120). r3a fixes it and adds the A133 amendments; it is checked by refute lenses before its seal candidate is posted, and its findings have dispositions in the r3a fix table, the r3a fix-check table, the r3a fix-check-2 table, the r3a delta-check table and the r3a delta-check-2 table of `CLAUSE_SOURCE_MAP_R3A.md`, and root's rulings of M-1 to M-16 are carried as the r3a rulings table lists.
- **Author.** Claude4, single author.
- **No target was opened.** No NGC3198 target value, no measured rotation datum and no target-bearing file was opened in writing it. The only NGC3198 records read are target-free:
  - query ids and radii from the query block of slots V003, and the slots' alternatives list, observation rule, STAGE0 registration and structural-assumption notes;
  - the target-free query manifest the slots cite, which the check hashes only;
  - the target-free N-test, node and certificate records named in §11, and the support-record schema in the code of Codex3's carrier extractor.
- **It changes nothing in the score.** Freeze v003g computes the LADDER rows in root's two-pass freeze:
  - module `48a1e48a…`, PASS in Claude4 0071;
  - RUNBOOK_V001 `9557b5aa…`.

  This document classifies and reads those rows afterwards.
  - **RUNBOOK_V002 [r3a].** Under A133 the procedure is RUNBOOK_V002, with the pinned roster builder; root pins both at the Phase-1 scoring gate (A133 §2 step 4). The step numbers in this text are RUNBOOK_V001's. They bind under V002 through a step map that root pins with V002, unless V002 keeps steps 1 to 10 as V001 numbers them. The §8 header records the V002, roster-builder and step-map shas.
- **Clause tags.** Each clause carries a tag in square brackets; for example, the tier rule's tag is C-1.1. The tags key the clause source map (`CLAUSE_SOURCE_MAP_R3A.md`).
- **When the seal happens (binding).**
  - Root rules on root items M-1 to M-16 [r3a] and seals this text, together with the M-12 classifier, before anyone reads any step-5 NGC route-A/B output value of either phase. "Anyone" means root, the author, and every reviewer of this text or of the classifier. "Output value" means a prediction, a band, an envelope, a sensitivity row or an alternative row.
  - The preferred timing is to seal before step 5 launches. **Step 5 is never delayed for the seal.** If step 5 runs first, its outputs are read validity-only until the seal.
  - The seal is root's entry registering the sha256 of this text and of the classifier (M-6). It is a V006 entry, and it names the sha256 of this text as rendered; §11 uses that sha to find it.
  - **Validity-only reads.** Until the seal, and in any case until RUNBOOK step 4 of the phase concerned begins, that phase's step-5 outputs (STAGE0's included) are read only as validity and admissibility booleans and reason codes, with no output value printed or written: the pattern of A47 I3. In Phase 2 this covers the Phase-2-only outputs, meaning the calls not re-bound from Phase 1 [r3a].
    - **Step 4 per phase [r3a]** (A133 §3). In Phase 1, step 4 begins when every Phase-1 NGC call has a terminal receipt. In Phase 2, it begins automatically when every registered Phase-2 step-5 call has a terminal receipt under A133 §3 rule (c). After the Phase-1 score, the Phase-2-only outputs stay validity-only until Phase-2 step 4 begins.
    - So no step-4 start is chosen in either phase. In Phase 1 it waits on every terminal receipt; in Phase 2 it is automatic (§6.3). The STAGE0 status that Phase-2 step 4 fixes is therefore set with no Phase-2-only output value seen.
  - **The attestation.** The seal entry lists every validity fact that was seen before the seal: which receipts, valid flags and reason codes, seen by whom. It also records, from each lane that touched this text or the classifier after step 5 launched, a statement that it read no step-5 output value. If a phase's RUNBOOK step 4 begins after the seal, that phase's score entry gives the same attestation for the time from the seal to the start of its step 4. In Phase 2 the attestation is that no Phase-2-only output value was read, because Phase-1 values are public once the Phase-1 score is made [r3a].
  - **The fallback.** If the timing is not met, the pre-prediction versions apply, and they all come from one post:
    - **A seal candidate** is a FROM_CLAUDE4 post whose title line carries the label SEAL CANDIDATE and that names, each once with its path and sha256: the rendered text, its ROOT_ITEMS file, and the classifier or "classifier: none". It may also name a STAGE0 successor (§6.3). Its publication time is the later of its own `date -u` stamp and its file's birth time. A root entry counts only by naming such a post.
    - **The pre-prediction versions** are the files named in the last seal candidate published before the first step-5 output value was read. A seal candidate that a root entry stamped before that read rules FAIL is withdrawn, and the last candidate not withdrawn is used. If there is none, there are no pre-prediction versions, and the whole classification is EXPLORATORY (post-prediction).
    - **The r3 candidate [r3a].** r3's candidate (Claude4 0124) carries the unamended I-7, which classifies the first successful score, the Phase-1 score. So that the fallback can never revive it in the two-phase run, root rules the 0124 candidate withdrawn through the existing FAIL mechanism, in an entry stamped before the first Phase-1 read (M-6).
    - Every root item is adopted exactly as recommended in the pre-prediction version. There is no option switching.
    - The seal entry names each pre-prediction sha and its publication time, and the report header discloses the deviation.
    - Any later wording change, ruling or classifier change is POST-PREDICTION. It is listed with its diff, and the report also gives the classification under the pre-prediction versions. A status that holds only under a later version is EXPLORATORY. A candidate published later is never adopted under the fallback. A FAIL ruling made after the first read does not withdraw a candidate: the report classifies under it and discloses the ruling.
    - If the seal candidate names no classifier, the classifier is built to the pre-prediction text and labelled POST-PREDICTION (CLASSIFIER). Its M-12 agreement suite must still pass before it runs.

**Binding principles** (A10, A12.3, A15 E3, A20, A23, A41, A48) **[C-P]**:
- Every outcome registers; nothing is prescribed.
- A miss is never reported as a failure of UNT in general. Under A15 E3, an outer-row failure is TESTED-NEGATIVE for exactly the present-mass-only lapse response of the L = 4 coefficient method, at the A2 grid and the calibrated θ. §2 defines "outer-row failure" (OUTER_FAILURE), and §5.3 gives the E3 verdict line.
- **The registered readings of a miss.** Every miss is read at least two ways: as a model failure, or as the missing history or species dependence (A10, SA-BH-01). This holds row by row: every MISS row with a frozen prediction is cited by R-MF and by R-HIST or R-SPEC, including a minority miss in a zone that is not miss-dominated (MINORITY_MISS, §3). An outer-row failure keeps the three readings of A15 E3, as narrowed by A20, open whatever its sign. §3 makes both rules mechanical.
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
  - the target pair (v_q, σ_q), which appears only inside the output of `score_after_freeze`. [r3a] It is read from the reference member's score rows, used only for the Phase-1 band column, and never a stop input (§1.1);
  - [r3a] the phase inputs of §1.1 (PHASE_MISMATCH), and in Phase 1 the L1 band rows (§1.1), used only for the Phase-1 band column; in Phase 2, the commitment status (I-7), the A133 `agree` record and the sealed Phase-1 classification output, the last two by the shas that the Phase-2 score entry pins and used only for §8 item 11. None of the three is a stop input (§1.1).
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
  - **Phase 1 [r3a].** Phase 1 runs ORIGINAL_K and the sensitivity calls with budget 0 (A133 §1.4). In the Phase-1 classification:
    - ORIGINAL_K is NOT_AVAILABLE, so every clause here that uses ORIGINAL_K reads NOT_AVAILABLE;
    - every sensitivity row reads invalid, never a zero-width band (§1.1);
    - STAGE0_GRID_OUTER reads NOT_EVALUATED_BEFORE_FREEZE (§6.3).

    Phase 2 runs the alternatives as registered, and the table above applies to it.
  - An alternative never replaces, re-tiers or outvotes the PRIMARY classification.
- **I-5. Headline [C-I5].** The headline stays the freeze module's (v003g HEADLINE_RULE): the distribution of the PRIMARY members' within-error counts, plus the frozen reference member's count. This document adds readings only and never alters the headline.
- **I-6. Numerics conditions [C-I6].** Every reading is conditional on the registered NGC numerics, all fixed before any target is opened. The report header records each, with its record sha (D-4). [r3a] For the per-point certificate records below, what is fixed in advance is the producer (by sha), its settings and its rule for the lowest shells, before the first per-point record is made and so before any target is opened; each record is then made from them at its call's θ.
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
  - **Route-A column workers [r3a].** Route A runs serially unless the A133 identity pair, the first NGC launch, has read byte-equal over the iterations that the pinned identity comparator compares. That makes the serial = parallel identity TESTED, and later calls of either phase may then run with 8 column workers (A133 §1.4). The report header records each call's column-worker count and the identity-pair record sha (D-4).
  - **Per-point EPS certificates [r3a].** Each NGC call carries its own per-point EPS certificate record at its θ. The tail library uses it numerically, so it is a numerics condition of that call. Its producer (by sha), the producer's settings and the rule for the lowest shells that the producer applies and each record states are fixed before the first per-point record is made, and so before any target is opened. Each record is made from them, mechanically, at its call's θ. A later successor or re-pin of any of them is a change, disclosed in the window lists of §8 and §9. Producing one at a θ that becomes known after the Phase-1 score is therefore not a choice, and the "None of these is chosen" clause below is met. D-4 lists each call's record.
  - **None of these is chosen, changed or re-run after targets are opened.**
  - **Numerical readings.** Exactly two registered readings attribute a miss to numerics, and each has registered prior evidence against it (§3):
    - R-GRID, k-grid fidelity of the in-use T120L grid;
    - R-TSR, the A66 residual.

    No other reading attributes a miss to a certified numerical quantity.
- **I-7. Freeze status and the score of record [C-I7].**
  - **Two phases [r3a]** (A133). Phase 1 is a provisional score on the Phase-1 manifest, frozen FREEZE_INCOMPLETE by design (A133 §1.6). Phase 2 is the registered step 4 plus the full step-5 point set, committed to run and be scored whatever Phase 1 shows.
  - **The score of record [r3a]** is the **first** successful `score_after_freeze` on NGC3198 targets of a Phase-2 manifest. This text classifies it. The classification is made on a FREEZE_COMPLETE manifest, or, if Phase 2 ends FREEZE_INCOMPLETE, under the incomplete-freeze rule below.
  - **The Phase-1 score [r3a].** The first successful `score_after_freeze` on the Phase-1 manifest is also classified in full, under this text and the sealed classifier, and published automatically (A133 §2).
    - Every pattern, reading and zone summary, the E3 verdict line and the DT-S0G comparison carry **PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE)**, with the manifest's `incomplete_reasons`: M-8's labels, with the phase named.
    - It is never the score of record, and no Phase-2 rule is chosen from it.
    - If Phase 1 makes no NGC call (an engine terminal status, or NO_IDENTIFIED_DIRECTION; A133 §1.3), there is no Phase-1 classification, and the report gives the code.
  - **Phase 2 is not a later re-score [r3a]** when its inputs were fixed before the Phase-1 score by the A133 §3 rules: the mechanical rules (a) to (f), the re-binding rule and the commitment. Any stop or change after the Phase-1 score makes Phase 2 EXPLORATORY (A133 §3).
    - **The commitment status [r3a].** Root records it in the Phase-2 score entry: COMMITTED, or EXPLORATORY with each stop or change and the entry that recorded it. It is a classifier input (M-5). Under EXPLORATORY, Phase 2 remains the score of record (A133 §3, §4), and every Phase-2 output carries "EXPLORATORY (PHASE 2 NOT AS COMMITTED)". A missing or malformed commitment status reads EXPLORATORY, with the code COMMITMENT_STATUS_DEFECT: the conservative label, which never presents an unverified commitment as COMMITTED.
    - **"Before target access" in Phase 2 [r3a].** The Phase-1 score opens the targets before Phase 2 is frozen. So, for Phase 2 only, these clauses mean "before the Phase-2 `score_after_freeze`": the pre-score checks of §1.1, REFERENCE_RULE, the stop checks and the roster registration of §4. They are allowed after the Phase-1 score only because they are mechanical under A133 §3: the Phase-2 freeze, REFERENCE_RULE's choice of member, the cut records and the rosters. Nothing in them is chosen. Every other "before any target is opened" in this text, the I-6 numerics included, keeps its literal meaning: before the Phase-1 score opened the targets.
    - **No classification, or no score of record [r3a]** (A133 §1.3, §3 and §4):
      - an engine terminal status, or NO_IDENTIFIED_DIRECTION, ends both phases the same way: there is no NGC call, no classification in either phase and no score of record, and the report gives the code;
      - an AT-0a failure stops Phase 1 with AGREEMENT_DEFECT (prefix), and there is then no Phase-1 classification;
      - a campaign halt under A133 §3 rule (c) leaves Phase 2 reported HALTED.
  - **Later scores.** Any other later freeze, re-registration or re-score after target access is EXPLORATORY (post-score). No roster, cut or reference may be chosen after targets are seen (RUNBOOK_V001 step 9). The Phase-2 rosters of §4 are made by the pinned roster builder, not chosen [r3a].
  - **An incomplete freeze.** Whether a FREEZE_INCOMPLETE manifest may be scored is recorded in a root entry before any step-5 output value is read, or fixed by the seal (root item M-8). A FREEZE_INCOMPLETE score authorized later is EXPLORATORY (post-prediction).
    - If a FREEZE_INCOMPLETE manifest is scored, the classification is still made and reported in full.
    - Every pattern, reading and zone summary, the E3 verdict line and the DT-S0G comparison then carry PROVISIONAL (FREEZE_INCOMPLETE), with the manifest's `incomplete_reasons` (the A50 PROVISIONAL rule, by analogy). In Phase 1 the label is the PHASE-1 form above [r3a].
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
- **The Phase-1 band [r3a]** (A133 §1.5; Phase 1 only; root item M-16) is the linearised projection of the admitted region, written to the pinned L1 record at the Phase-1 freeze. It is never used for a tier, a flag, a pattern, a reading or an uncertainty claim.
  - It is reported in one fixed column for all 43 rows: "Phase-1 band overlaps: yes / no / NOT_AVAILABLE", labelled PHASE1_LINEARISED_ADMITTED_SET_PROJECTION_TRUNCATED_LOWER_BOUND_ON_SPREAD_NOT_A_TIER, conditional on A13 (the fixed DDO154 distance 4.04 Mpc and inclination 66°).
  - "yes" means the record's band [lo_q, hi_q] intersects the error bar [v_q − σ_q, v_q + σ_q]. The FD-noise term is not added, because widening could only add overlaps (the A48 principle). A row whose record prints FD_NOISE_NOT_BOUNDED carries that flag beside its entry.
  - A row the record gives as NOT_AVAILABLE (a non-OPTIMAL program, or a row INVALID at u_A or at an F point) reads NOT_AVAILABLE, never a zero-width band.
  - **The record's form.** The L1 rows are read as the pinned A133 `band` command writes them (root's Phase-1 tool, by the sha that the seal entry pins). The classifier binds that command's keys and value encodings, so the L1 schema is fixed at the seal. A defect in an L1 row affects only this column (the stop-to-output map below). [r3a] Every L1 row has an `id` and a `status` (AVAILABLE or NOT_AVAILABLE); `lo`, `hi` and `fd_noise` are required only when the status is AVAILABLE, so an honest NOT_AVAILABLE row without them is not a defect. Q01 and Q02 always read NOT_AVAILABLE in this column. The FD_NOISE_NOT_BOUNDED flag is set only when `fd_noise` is that string; an object means bounded, and its values are never used. The target pair (v_q, σ_q) for this column comes from the reference member's score rows; a defect in it, as in an L1 row, blanks only this column.
- **A row with no ratio.** A VALID row whose `sigma_ratio` is null (v003g NON_FINITE_SIGMA_RATIO) is a MISS with sign UNDEFINED. It counts in N_v(Z), M(Z) and U(Z) (§2), and it is left out of m(Z) and Δ_out.
- **Pre-score checks (binding).** Every stop condition below is target-free.
  - **When they run.** Each is checked on the frozen manifest, slots and pinned records **before any target is opened**, through the sealed classifier (M-12) run on a synthetic score built from the frozen member arrays. The result goes in the seal or score entry.
  - **The stop conditions:**
    - the reference member's row status is UNEVALUATED_OR_REFUSED (REFERENCE_RULE excludes this);
    - the reference member named in the score (`headline.reference_member_id`, `reference_member_log_index`) differs from the frozen manifest's (REFERENCE_MEMBER_MISMATCH);
    - a field named here or in M-5 is missing, has the wrong type, or is non-finite where a finite value is required. [r3a] The three Phase-2 inputs of §8 item 11 and the label (the A133 `agree` record, the sealed Phase-1 classification and the commitment status) are never stop inputs and never make the classification NOT_READ: a missing or defective one affects only item 11 or the label, as the map below says. When there is no Phase-1 classification (an AT-0a failure, or no Phase-1 score), the cross-phase items of item 11 read NOT_AVAILABLE with the code NO_PHASE_1_CLASSIFICATION. That is not a defect, and Phase 2 stands. [r3a] Likewise, the target pair (v_q, σ_q) and, in Phase 1, the L1 band rows are band-column-only inputs: a missing or defective one blanks only the Phase-1 band column, with its code, and never makes the classification NOT_READ;
    - the reference member's ids are not Q01 to Q43 in order, or an id is repeated;
    - the envelope label prefix differs;
    - the zone table of §1.3 differs;
    - **TSR_FLAG_TABLE_MISMATCH:** the freeze's pinned N-test compare is not `6f095f64…`; or its failing TRUNCATION_SHAPE rings are not exactly {ordinal 15}; or its failing non-TRUNCATION_SHAPE rings are not empty; or the N1 record is not `8867c376…`; or the GL-node record is not `ec1dcca5…`; or the flag record's 43 flags are not exactly {NGC3198-Q25} (§1.4);
    - **GATE_STATUS_LIST_DEFECT:** the gate-status list of §4 is missing, or a root-listed gate of the rosters is not on it;
    - **SEAL_SHA_MISMATCH:** a sealed sha (this text, the classifier, the flag record, the STAGE0 successor if pinned) does not match its bytes. This check runs before RUNBOOK step 9.
    - **PHASE_MISMATCH [r3a]:** the phase that the score entry names is not the phase of the frozen manifest. Phase 1 writes its calibration record into its own registry (A133 §1.2), so the manifest's phase is PHASE_1 if and only if its `input_bindings.calibration_record` path, resolved to an absolute real path, lies under the resolved Phase-1 registry root that the seal entry names by path, and PHASE_2 otherwise. The Phase-1 root must be disjoint from the Phase-2 registry (neither contains the other). The phase is derived from those two values; no manifest field is required for it.

    Any of these stops the classification with CLASSIFICATION_INPUT_DEFECT and its code, before target access.
  - **After target access,** the sealed classifier re-runs every stop condition above on the real score. Root has one permitted act:
    - **Rename a field.** A field map renames keys only; it never changes a value. It is pinned, with its diff, before the classifier output is read, and the sealed M-12 suite must reproduce byte for byte through it. When such a map clears a stop, root must apply it.
  - **NOT_READ is mechanical.** If a re-run stop fires and no pinned field map clears it, the classification is NOT_READ with the stop code. The classifier emits it, and root makes no choice. If no stop fires, NOT_READ is unavailable.
  - **What NOT_READ prints.** The classifier output is still computed and published, labelled NOT_READ with the stop code. Which outputs carry a value is fixed by the stop, through this closed map:
    - **A field of a row of the reference member.** The defective rows D are the rows whose field check fired.
      - **Count-level outputs** are printed when they take the same value for every assignment of a kind to the rows of D (HIT, signed MISS or null-ratio MISS; INVALID_AS_MISS for a row the roster registers INVALID), and otherwise read NOT_AVAILABLE with the code. They are: N_v, H, M, U and I per zone; miss- and hit-domination; the test "S(Z) is UNDEFINED"; OUTER_FAILURE; the E3 value; P0, P5, P7, P8, P9, P10, P13, P14 and P15; MINORITY_MISS (§3); and the onset radius.
      - **Every other output computed from a row of D** reads NOT_AVAILABLE with the code, unless one of these deductions from printed count-level outputs fixes it: P1, P2 and P11 (P3, P4 and P12) are false when their zone's miss-domination is printed false or its "S(Z) is UNDEFINED" is printed true; GROWING, CROSSING, P1g and P11g are false when "S(OUTER) is UNDEFINED" is printed true; P6 is false when any "S(Z) is UNDEFINED" is printed true. These outputs are the row's own entries; m(Z), the sign class and N(Z) of its zone; Δ_out, GROWING and CROSSING for a TRANSITION or OUTER row; the signed patterns of its zone; P6; and the DT-S0G comparison for an OUTER row.
      - **Each part of a reading's tuple** is printed when the printed outputs fix it under §3 and §6.3, and otherwise reads NOT_AVAILABLE with the code. For example, R-MF's part 1 is CONSISTENT when a printed trigger holds, and its part 2 is the printed E3 value.
      - The E3 line prints each of its fields under the same rule.
    - **A field of an envelope row or a sensitivity row:** only NEAR and N(Z), or only the sensitivity column, read NOT_AVAILABLE, on the rows concerned.
    - **A field of an L1 band row or of the target pair, or L1 bytes that do not hash to the L1 sha logged at the Phase-1 freeze (A133 §1.6) [r3a]** (Phase 1): only the Phase-1 band column reads NOT_AVAILABLE, with the code, on the rows concerned (all 43 for a sha mismatch). These are band-column-only inputs, so the classification is never NOT_READ for them.
    - **A field of the A133 `agree` record, or of the sealed Phase-1 classification input [r3a]** (Phase 2): only §8 item 11 reads NOT_AVAILABLE, or only its cross-phase items for the Phase-1 input. The A133 `agree` record's keys and value encodings are those of the `agree` command at the sha the seal entry pins. Under AGREEMENT_DEFECT, the fields of a test that `agree` did not run (AT-0b or AT-1) may be absent, and that is not a defect. The classification is never NOT_READ for these fields.
    - **The commitment status [r3a]** (Phase 2): a missing or malformed status reads EXPLORATORY with COMMITMENT_STATUS_DEFECT (I-7). It blanks no output.
    - **A field of an alternative:** that alternative reads TWIN_INPUT_DEFECT (§6.1), and R-DRIFT follows §6.3.
    - **TSR_FLAG_TABLE_MISMATCH:** only P10, R-TSR and the flag column read NOT_AVAILABLE.
    - **GATE_STATUS_LIST_DEFECT:** the rows of every gate missing from the list are the rows D, each with the two kinds INVALID_AS_MISS and LATE-gate MISS, and the row rule above applies.
    - **Every other stop** (the reference member's status or identity, the ids, the envelope label, the zone table, a field outside the rows, SEAL_SHA_MISMATCH, PHASE_MISMATCH [r3a]): every output reads NOT_AVAILABLE with the code, the E3 line included.
    - **Several stops [r3a].** When more than one stop fires, every code fired is printed, and an output carries a value only if the class of each fired stop lets it print.
    - Values that cannot be classified may be shown descriptively, labelled "not read" (the A48 AMB-18 pattern).

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
  - **Each node's value is local to its ring.** The route-B column value at node k depends only on ring k: the rotation module forms Ω squared column by column, and its radial derivative enters only the shear. Round-2 recheck lens R2-B TESTED this from the module bytes (its report is pinned in §11; not re-run here).
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
  - **UNDEFINED** when m(Z) is UNDEFINED, or when Z is miss-dominated and M(Z) − U(Z) < N_v(Z)/2, that is, when the signed misses alone do not reach half of the zone's non-INVALID rows. A signed class (DEFICIT or EXCESS) is therefore never taken from hits, or from a minority of signed misses [r3a].
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
  1. **score relation:** CONSISTENT, INCONSISTENT or NOT_ADDRESSED. NOT_ADDRESSED means that the score does not bear on the reading, in exactly two registered cases, each printed with its code. Part 1 is decided in this order, the first that applies:
     - NOT_ADDRESSED (PATTERN_NOT_HELD) when no trigger of the reading holds, whatever its against-condition reads. A deciding test that reads against the reading still shows in part 2 (§6.3 for R-DRIFT).
     - INCONSISTENT when any registered against-condition of the reading holds. **Against takes precedence** over CONSISTENT and over the sign-scope codes.
     - NOT_ADDRESSED with a sign-scope code when the reading is deficit-type and the OUTER signs are outside its scope (SIGN_SCOPE_EXCESS, SIGN_SCOPE_UNSIGNED or SIGN_SCOPE_NO_DEFICIT_MISS, §3.2).
     - CONSISTENT otherwise.
  2. **deciding-test status,** as it stands at the score step: OPEN when the deciding test is NOT SCHEDULED, not run, UNTESTED or NOT_EVALUATED_BEFORE_FREEZE; otherwise the test's registered outcome. Two readings have their own rule: R-MF's part 2 is the value of the E3 verdict line (§5.3), and R-DRIFT's part 2 follows the §6.3 mapping. A deciding test that runs after the score step changes no part 2; its result is reported separately, under the support rule below.
  3. **prior evidence:** exactly the entries in the prior-evidence column of §3.2, which is the closed list. It never changes parts 1 and 2.

  "CONSISTENT" is never reported without the deciding-test status beside it.
- **No support from the score alone.** The 43-row score can make a reading CONSISTENT or INCONSISTENT. It can never make it supported. Support comes only from that reading's own deciding test, run under its own pre-registration.
  - A deciding test registered after NGC3198 target access can support a reading only through data not opened when its prereg was sealed.
- **Fixed list.** The readings below are the registered list. Any reading proposed after targets are opened is labelled **EXPLORATORY (post-score)** and never counts as registered.
- **The A10 rule: every miss is read two ways.** Every MISS row with a frozen prediction is cited by R-MF and by one history or species reading.
  - **The zone patterns.** OUTER_FAILURE carries R-MF and R-HIST for the OUTER rows, and P13 carries them for the TRANSITION rows. P3, P4, P12 and P15 carry R-MF and R-SPEC for the INNER rows. P6 and P7 carry R-MF and R-HIST for all MISS rows.
  - **MINORITY_MISS(Z)**, a row-level trigger, covers the rest. It holds for a zone Z when some zone is miss-dominated, Z is not miss-dominated, and Z has at least one MISS row with a frozen prediction. It triggers R-MF, and R-SPEC for Z = INNER or R-HIST for Z = TRANSITION or OUTER, for those rows of Z only. It is not a pattern: it changes no count, pattern, flag or E3 line.
  - **FORMAL.** Take a MISS row with a frozen prediction, in zone Z. If no zone is miss-dominated, P7 holds. If Z is miss-dominated, its zone pattern holds (the coverage proof of §2). Otherwise some other zone is miss-dominated, so MINORITY_MISS(Z) holds. In each case R-MF and R-HIST or R-SPEC cite the row. This includes the flagged row Q25, which R-TSR may also cite, and a real miss beside a zone of LATE-gate rows (§4).
- **The A15 E3 rule: an outer-row failure keeps three readings open.** Whenever OUTER_FAILURE holds, R-MF, R-UT1, R-REACH, R-HIST and R-DRIFT are triggered for the OUTER rows, whatever S(OUTER) and whatever the other zones show (A15 E3; A12.3; A20; A63). R-MF, R-HIST and R-DRIFT are sign-free. R-UT1 and R-REACH are deficit-type, and their score relation follows the sign rule of §3.2; they are never dropped.
- **Scope: which rows a reading may cite.** A reading may cite only rows of the zones its triggering patterns name:
  - OUTER rows under OUTER_FAILURE, P2, P11 and P14; INNER rows under P3, P4, P12 and P15; TRANSITION rows under P13; all MISS rows under P6 and P7; the MISS rows of Z that have a frozen prediction, under MINORITY_MISS(Z); flagged MISS rows only, for R-TSR.
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
| **R-MF** | failure of the present-mass-only lapse response of the L = 4 coefficient method at the A2 grid and the calibrated θ (A15 E3); at row level, the model-failure reading of A10. TESTED-NEGATIVE for exactly the E3 scope when OUTER_FAILURE holds. | OUTER_FAILURE (P1, P2, P11, P14); P3, P4, P12, P15; P13; P6; P7; MINORITY_MISS(Z), any zone | sign-free | — | for: A15 E2, which expected an outer deficit; A41 | the score itself, for the E3 scope only: part 2 is the E3 line value |
| **R-UT1** | the static isothermal typing of the k = 0 block (A20 reading 1; counted CA-34/CA-28, A41) | OUTER_FAILURE | deficit-type | — | against: A41 item 3 (FORMAL + TESTED). No gate-consistent typing gives an attractive tail, and the spec-compliant T(0⁺) is finite and repulsive on current estimates. | DT-UT1 (NOT SCHEDULED) |
| **R-REACH** | magnitudes, k = 0-block drift or finite-size effects at larger L or with mixing (A12.3 reading 2, "missing reach"; A15 E3 reading 2; narrowed by A20: these cannot create a 1/r tail) | OUTER_FAILURE | deficit-type | — | — | DT-U12 (NOT SCHEDULED) |
| **R-HIST** | a missing Bind-history or collective component (A10 SA-BH-01, DECLARED-PREMISE; A15 E3 reading 3; A20 reading 2; BH-D). P1g or P11g makes it more specific: "missing long-range component" (0522). | OUTER_FAILURE; P13; P6; P7; MINORITY_MISS(TRANSITION); MINORITY_MISS(OUTER) | sign-free (A10: every miss) | — | — | DT-BHD (NOT SCHEDULED) |
| **R-DRIFT** | A2's k = 0 entry, which enters the k → 0⁺ transfer under CA-34, is drift-inflated (A63, A65) | OUTER_FAILURE | sign-free | DT-S0G reads AGAINST (§6.3) | for: the sealed k = 0 drift reading is SUPPORTED (A63). Against: its causal gloss is UNTESTED (A65 check R-3). | DT-S0G, by the §6.3 mapping; it never makes R-DRIFT supported |
| **R-S1** | calibration transfer of G_eff = G·Q∞ (A21): the G_eff scale | P2; P11; P6 | — | — | — | DT-S1 (UNTESTED) |
| **R-GRID** (numerical) | k-grid fidelity of the in-use T120L grid at outer radii (A17) | P2; P11 | — | — | against: T120L passes C2, C3, C4 and C1′ (A27). The production N-tests N0, NQ, N2 and N3′ pass (A90). | none registered: OPEN |
| **R-NAX** | non-axisymmetric flow and the m = 0 projection (A17 note; plan D3) | P11; P14; P3, P4, P12, P15; P13; P7 | — | — | — | DT-NAX (not run) |
| **R-GEFF** | the single DDO154 short-wavelength G_eff does not carry over to a galaxy with stellar share about 0.51 (DDO154: about 0.03; A10) (A21, E1) | P3, P4, P12, P15 | — | — | — | DT-S1 |
| **R-ML** | stellar M/L (0.5, counted ±20%; A10) | P3, P4, P12, P15 | — | — | the ML_3p6 alternatives are NOT_EVALUATED_BEFORE_FREEZE (slots V003) | DT-ALT (M/L; NOT_EVALUATED, so OPEN); DT-T1a (diagnostic, jointly with R-SPEC) |
| **R-SPEC** | a species or history weight (SA-BH-01) | P3, P4, P12, P15; MINORITY_MISS(INNER) | — | — | — | DT-T1a (diagnostic, jointly with R-ML) |
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
  - That record must be pinned before the freeze, and in either phase no later than the Phase-1 score [r3a]; otherwise that half reads NOT_AVAILABLE (M-13).
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
  - **Both phases [r3a].** The first step-5 launch receipt is that of the first NGC launch of either phase: the A133 identity pair (A133 §1.4). A gate's status is the same in both phases.
  - Under RUNBOOK_V001, gates are approved at step 4, after step 1 has saved the step-5 raw results. So **every gate first adopted at RUNBOOK step 4 of either phase is LATE** [r3a].
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
  - It never removes the A10 readings of a MISS row with a frozen prediction: under either status, R-MF and R-HIST or R-SPEC cite every such row (§3).
  - So every change goes toward more misses, or from a signed to an unsigned reading of the same failure.

**Scoring and reporting.**
- INVALID rows are scored as worst-tier misses and counted in the 43 (0518 items 1–2). D1 is applied over the registered-valid rows only (0518 item 3).
- INVALID rows are listed separately, per reason, with each row's zone and, for gate rows, the gate's status.
- For the outer-gas cut, the report also gives the pinned cut record's truncation radius and dropped HI mass fraction (the V001 §4 requirement).

**No part in the readings.**
- INVALID rows are excluded from N_v(Z), from m(Z), and from every pattern except P0 and P9. Every INVALID OUTER row counts toward P9. (A LATE-gate row is counted as above, not as INVALID.)
- The only statement made about an INVALID row is its roster reason. No reading cites an INVALID row as evidence for or against anything.
- No roster change is allowed after targets are opened. Any later root ruling on a roster row is recorded as post-score and does not change this classification.
- **Phase-2 rosters [r3a].** The Phase-2 rosters are registered after the Phase-1 score has opened the targets. They are not roster changes when the pinned roster builder makes them under A133 §3 rule (a), from the run-produced cut records and from gate documents pinned before the Phase-1 score.
  - A gate document first pinned after the Phase-1 score is LATE, as is every gate pinned after the first step-5 launch receipt. It is not a roster-builder input, and any root listing of it is recorded as post-score.
  - A RUNBOOK step-7 discrepancy makes that member UNEVALUATED, under A133 §3 rule (b), and it is never resolved by a successor made by root.

## 5. Comparison with the A15 expectations (after the score; labelled COMPARISON, never a fit)

**E1, inner disc [C-5.1].**
- **(a) The deciding observable A15 E1 names:** the inner rows against their bands.
  - Report H(INNER), M(INNER) and N(INNER).
  - As a sub-table, report the rows Q03–Q15, which A15 E1 names "or so".
  - Label: "COMPARISON with A15 E1".
- **(b) The expectation itself:** whether the frozen model rotation exceeds the frozen baryonic-Newtonian rotation at the INNER rows.
  - This is model-internal; it involves no target.
  - It is made only from a target-free carrier pinned before the freeze, and in either phase no later than the Phase-1 score [r3a] (root item M-11). v003g has no such field. Without a carrier, part (b) reads NOT_AVAILABLE.
  - It is never computed after targets are opened, in Phase 1. In Phase 2 it is computed from a carrier that meets the deadline in the line above, and from nothing chosen after it [r3a]. No baryon column of the observational data table is ever used.

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

**Phase 1 [r3a].** STAGE0 is not in the Phase-1 set (A133 §1.4 and §3). In the Phase-1 classification it reads NOT_EVALUATED_BEFORE_FREEZE with the reason NOT_IN_PHASE_1, and the rules below apply to Phase 2 only.

**When it is evaluated (the receipt rule; root item M-14 states the same rule).**
- STAGE0 is EVALUATED_BEFORE_FREEZE if and only if both of these hold and the adopted successor refuses no STAGE0 record:
  - **(a) [r3a]** every registered STAGE0 member's terminal receipt under A133 §3 rule (c) is FINISHED;
  - **(b)** the prepared STAGE0 slots/module successor is pinned by sha256 in the seal entry, or, under the Status fallback, it is named in the seal candidate that gives the pre-prediction versions. Pinning it there is what registers STAGE0 as a Phase-2 step-5 call (A133 §3).
- **The Phase-2 step-4 start [r3a].** Phase-2 step 4 begins automatically (Status), so its start is not chosen. Its recorded start time is the write time of the last registered terminal receipt. A receipt written at that instant counts as before step 4.
- Root records the Phase-2 step-4 start time and every receipt time. No Phase-2-only output value, STAGE0's included, is read before Phase-2 step 4 begins (the validity-only rule of the Status section). The seal or score entry attests it [r3a].
- When (a) and (b) hold, the pinned successor is adopted with no further decision. If it refuses a STAGE0 record, STAGE0 reads EVALUATED_REFUSED.
- Otherwise STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (A65.2), with every reason that applies [r3a]:
  - STAGE0_RECEIPT_NOT_FINISHED, if (a) fails: a registered member's terminal receipt is not FINISHED (for example, marked invalid under rule (c));
  - NO_SEALED_SUCCESSOR, if (b) fails: STAGE0 is then not registered for Phase 2.
- Validity booleans and output values never change the status, and root reads no prediction value to decide it.
- A STAGE0 result that first becomes available after Phase-2 RUNBOOK step 4 begins (RECEIPTS_AFTER_STEP4) is EXPLORATORY (post-score), and R-DRIFT stays OPEN [r3a].

**If it is evaluated:**
- It is scored on its 8 rows, denominator 8, separately from the headline.
- It is labelled "SENSITIVITY: coefficient-grid sensitivity at fixed calibrated parameters (A65), not a recalibration". The label is used only when it is evaluated.
- It never enters the headline, and never re-tiers a PRIMARY row (A65.1).

**Comparison rule** (registered here; root item M-9). Restrict to the OUTER rows that are non-INVALID under both the PRIMARY reference member and the valid STAGE0 twin, and have a defined r_q under both. On those rows:
- H_P and H_S are the HIT counts of the reference member and of the twin;
- A_P and A_S are the medians of |r_q| for each.

The comparison reads:
- **CONSISTENT** with R-DRIFT if and only if H_S > H_P and A_S < A_P [r3a].
- **AGAINST** R-DRIFT, as an explanation of the outer misses at fixed calibrated parameters, if and only if H_S ≤ H_P and A_S ≥ A_P.
- **NOT_DECIDED** otherwise: in both mixed cases (H_S > H_P with A_S ≥ A_P, and H_S ≤ H_P with A_S < A_P), and when no row qualifies [r3a].

**The mapping to R-DRIFT's tuple** (closed). Part 1 follows the order of §3: it is NOT_ADDRESSED (PATTERN_NOT_HELD) whenever OUTER_FAILURE does not hold, whatever DT-S0G reads; otherwise it is the middle column below. Part 2 is always the last column, so an AGAINST still shows as AGAINST (DT-S0G) when OUTER_FAILURE does not hold.

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
- the record that closes the A90 LO I1-T precondition (A101; Codex1 0066), with its stated scope;
- each NGC call's route-A column-worker count, and the A133 identity-pair record with its outcome: byte-equal over the compared iterations, or not, in which case every call is serial [r3a];
- each NGC call's per-point EPS certificate record, by sha, its producer sha and the rule for the lowest shells that it states (I-6), and its GQ binding [r3a].

## 8. Report format (score step) [C-8]

The report gives:
1. **The header:**
   - the phase, PHASE_1 or PHASE_2 [r3a]. For Phase 1 it also gives:
     - the label PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE);
     - B_P1 and u_A's log index;
     - the Phase-1 record sha and the L1 sha (A133 §1.6);
   - the sealed sha of this text;
   - the freeze manifest sha, the registration sha, and the expected manifest sha logged at the freeze;
   - the slots, module and roster shas;
   - RUNBOOK_V002, the roster builder and the step map, by the shas pinned in the seal or score entry; and, in Phase 2, the commitment status (COMMITTED or EXPLORATORY, with each stop or change; I-7) and the A133 `agree` record [r3a];
   - in both phases, every change made in the window between the first readable Phase-1 value and the Phase-1 score: an A133 §3 rule change; a first pin of the roster builder, RUNBOOK_V002, the step map or an M-11/M-13 carrier; a successor or re-pin of the Phase-1 tool (`band`, `agree`), which the seal entry first pins (M-6); or a successor or re-pin of the per-point certificate producer, its settings or its shell rule (I-6). Each is labelled POST-PREDICTION, with the entry that made it (§9) [r3a];
   - the TSR records: the flag record and the support record, the compare (`6f095f64…`), the N1 record (`8867c376…`) and the GL-node record (`ec1dcca5…`);
   - the classifier sha (M-12);
   - the gate-status list (§4);
   - the STAGE0 status with its reason, the step-4 start time and the receipt times (§6.3);
   - the V005 whole-file sha at assembly and the sha of `V005_ENTRY_TABLE_R3A.json`, and the V006 whole-file sha read at assembly and the sha of `V006_ENTRY_TABLE_R3A.json` (§11);
   - the I-6 values, with their record shas (D-4), each call's column-worker count and the identity-pair record sha [r3a];
   - the freeze status (I-7);
   - disclosures D-1 to D-4;
   - the timing attestation of the Status section, with the validity facts seen before the seal (and before the phase's RUNBOOK step 4, if it began later; in Phase 2, for the Phase-2-only values [r3a]), and, under the fallback, the seal candidate post and the pre-prediction shas it names.
2. **The per-row table:** Q_id, zone, R_q, tier, r_q, sign, whether the row has a frozen prediction, the NEAR flag, the TRUNCATION_SHAPE_RESIDUAL flag, INVALID reason (with GATE_AFTER_PREDICTIONS where it applies), sensitivity band overlap (yes / no / invalid, conditional on trial values), in Phase 1 the Phase-1 band overlap (yes / no / NOT_AVAILABLE, with FD_NOISE_NOT_BOUNDED where it applies, under its §1.1 label) [r3a], and notes (the D-2 counted uncertainty).
3. **The zone summaries** (U(Z) included), OUTER_FAILURE, and the E3 verdict line (§5.3).
4. **Every pattern and flag that holds.**
5. **Every registered reading,** in §3.2 order, with its triggers that hold (MINORITY_MISS included, with its zone), its row scope and its full status tuple, with any NOT_ADDRESSED code, and each deciding test's status.
6. **The INVALID list,** per reason, with the cut record's truncation radius and dropped mass fraction.
7. **The A15 comparisons** (§5).
8. **The alternatives** (§6). STAGE0_GRID_OUTER comes last, labelled SENSITIVITY only if evaluated.
9. **Any EXPLORATORY (post-score) readings,** labelled as such.
10. **Under the fallback:** the classification under the pre-prediction versions, and every POST-PREDICTION change with its diff.
11. **In Phase 2 only [r3a]:** the A133 §4 agreement outcome and what it means for the Phase-1 classification.
    - **The outcome.** COVERED, SUPERSEDED or AGREEMENT_DEFECT, with its NON_DISCRIMINATING rows, as the pinned A133 `agree` command computes them from target-free inputs. That command also gives the target-free always-reported items: the Phase-2 envelope width against the Phase-1 band width per row, the NGC linearity residual, the largest DDO linearity excess, and the identified projection ranges.
    - **The target-dependent always-reported items** come from this text's two sealed classifications, one per phase: both headlines, both E3 lines, both pattern classifications, and the rows whose tier changed between the phases. A row's tier is compared by its LADDER tier, with INVALID_AS_MISS rows compared by their reason and LATE-gate rows by kind.
    - **The consequence for Phase 1** (A133 §4):
      - **COVERED:** the Phase-1 classification is reported as standing, as an early statement of the score of record.
      - **SUPERSEDED:** every Phase-1 pattern, reading, zone summary, E3 line and band entry is reported WITHDRAWN (A133 §4). Each one except the band entries is replaced by Phase 2's; Phase 2 has no band column. The report lists each failing (member, row) with its excess, its |n_m| and its category.
      - **AGREEMENT_DEFECT:** Phase 2 stands, and root investigates.
      - **No Phase-1 classification [r3a]** (an AT-0a failure, or no Phase-1 score): the cross-phase items read NOT_AVAILABLE with the code NO_PHASE_1_CLASSIFICATION. That is not a defect: Phase 2 is classified and printed in full.
      - **A defective A133 `agree` record [r3a]** (§1.1): item 11 reads NOT_AVAILABLE, and no outcome is stated. The Phase-1 classification keeps its PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) label and is reported neither as standing nor as WITHDRAWN, and Phase 2 is the score of record.
      - **A defective Phase-1 classification input [r3a]** (§1.1): the outcome is stated, and its consequence above applies to the Phase-1 classification as a whole (COVERED: standing; SUPERSEDED: WITHDRAWN, with the failing (member, row) list of the `agree` record). Only the cross-phase items read NOT_AVAILABLE. If the A133 `agree` record is also defective, the bullet above applies instead. Under AGREEMENT_DEFECT the consequence is that row's: Phase 2 stands.
    - The agreement outcome never recomputes a tier, flag, pattern or status tuple of either phase. Phase 2 is the result of record in every outcome.

**The words used:**
- "TESTED-NEGATIVE" is used only for R-MF, within its stated scope. The one exception is quoting a registered outcome name verbatim.
- "consistent with" is never written as "supports".
- "SUPPORTED" is used only when quoting the sealed k = 0 drift reading of A63.

## 9. Self-check: could any rule be steered by the outcome? [C-9]

| risk | how it is closed here |
|---|---|
| Ruling the root items, or sealing, after the predictions are readable | The Status timing rule: seal before anyone reads any step-5 output value, with validity-only reads until then and an attestation listing the validity facts seen. Step 5 is never delayed for the seal. Otherwise the pre-prediction versions (text, root items, classifier) apply by sha, all from one SEAL CANDIDATE post: the last published before the first read, where a candidate ruled FAIL before that read is withdrawn and no candidate means EXPLORATORY. Later changes are POST-PREDICTION with their diff, and the deviation is disclosed. |
| A root ruling made after assembly changes a rule unseen | The V005 and V006 entry tables: every heading before the seal entry has a row read from the bytes, and T7 fails on an uncovered heading or a changed section (§11). Inputs named by the text are pinned by sha in the seal or score entry. |
| Moving the zone boundaries or memberships | The cuts are numbers fixed in §1.3, and membership is fixed by query id. A mismatch stops before target access. |
| Redefining HIT, MISS or NEAR after seeing residuals | The tiers use only frozen LADDER fields and the quoted σ (§1.1). NEAR is a flag on tier-MISS rows with a valid envelope row, and it changes no count. |
| Choosing which member is scored | The frozen reference member, checked against the manifest (REFERENCE_MEMBER_MISMATCH). Alternatives use the twin rule (§6.1). |
| Choosing which pattern to report | Every applicable pattern is reported. The coverage property is proved case by case for each zone (§2): the unsigned patterns P14 and P15 cover a miss-dominated zone whose signed misses do not reach half, and ties go to the stricter side. |
| Taking a zone's sign from its hits | A signed class (DEFICIT or EXCESS) needs a miss-dominated zone whose signed misses alone reach half of N_v(Z); in a miss-dominated zone where they do not, S(Z) is UNDEFINED (§2) [r3a]. |
| Choosing a reading's status word | One tuple rule per reading, independent of the trigger. Every registered reading is listed every time. Part 1 is decided in one fixed order (PATTERN_NOT_HELD, then against, then the sign scope), which §6.3 follows for R-DRIFT, and NOT_ADDRESSED occurs only in its coded cases (§3). |
| Dropping an outer-row reading for an awkward sign | The A15 E3 rule: R-MF, R-UT1, R-REACH, R-HIST and R-DRIFT are triggered by every OUTER_FAILURE. A deficit-type reading under an excess or an unsigned outer reads NOT_ADDRESSED with its code; it is never omitted (§3). |
| Leaving a minority miss unread, or reading it only as a numerical residual | MINORITY_MISS(Z) (§3): every MISS row with a frozen prediction is cited by R-MF and by R-HIST or R-SPEC (FORMAL), the flagged row Q25 included, and a LATE gate never removes those readings (§4). |
| Upgrading "consistent" to "supported" | Prohibited (§3). DT-S0G never makes R-DRIFT supported (§6.3). |
| Choosing whether the R-MF verdict applies | One sign-free trigger, OUTER_FAILURE, equivalent to exactly one of P1, P2, P11 or P14 and printed in the E3 verdict line (§2, §5.3). |
| Re-explaining INVALID rows | Prohibited (§4). |
| A gate added after the predictions changes the reading | LATE is decided mechanically: a gate not pinned before the first step-5 launch receipt of either phase is LATE, and every gate first adopted at RUNBOOK step 4 of either phase is LATE [r3a]. LATE rows count as unsigned MISS rows. Relative to the same gate on time, a LATE gate never removes miss-domination or OUTER_FAILURE, never creates or switches a sign class, never moves the E3 line toward a favourable value, never makes a deficit-type reading CONSISTENT, and never removes the A10 readings of a real miss; §4 lists its effects on counts, patterns, the E3 line, the deficit-type readings and the A10 readings. |
| Suppressing the classification after the targets are seen | NOT_READ is mechanical: the classifier emits it when a stop condition, re-run on the real score, fires and no pinned field map clears it, and never otherwise; root makes no choice. The output is still computed and published, and a closed stop-to-output map fixes which outputs print a value, the E3 line included (§1.1). |
| Evaluating STAGE0 only if it helps | The receipt rule: FINISHED receipts before Phase-2 RUNBOOK step 4 and a successor pinned in the seal entry, then adoption with no further decision; validity booleans and values never change the status. No Phase-2-only output value is read before Phase-2 step 4 begins, and its start is not chosen, because Phase-2 step 4 begins automatically on the last terminal receipt; the seal or score entry attests it (Status, §6.3) [r3a]. |
| Flagging rows TRUNCATION_SHAPE_RESIDUAL after seeing misses | The overlap rule is derived from the registered node, interpolation and column-locality facts, the flagged ids are fixed by id in §1.4, and any disagreement is the pre-target stop TSR_FLAG_TABLE_MISMATCH. |
| Choosing K_big, M_s or certificates after targets | All are fixed before step 5 (A64; A81 RI-23; Codex1 0032; A90; A101). The per-point certificate records are made later, mechanically, at each call's θ, from a producer, settings and shell rule fixed before the first such record (I-6) [r3a]. The header records them (I-6, D-4). |
| Root discretion after a stop condition | Every stop is checked before target access. Afterwards, root's only act is a key-renaming field map; NOT_READ follows mechanically from a re-run stop (§1.1). |
| Authorizing a FREEZE_INCOMPLETE score after the predictions are readable | The decision is recorded before any step-5 output value is read, or fixed by the seal; a later authorization is EXPLORATORY (I-7). |
| A later re-score | Only the first successful score of each phase is classified, and the score of record is the first Phase-2 score; later ones are EXPLORATORY (I-7) [r3a]. |
| Choosing the score of record after Phase 1 is seen [r3a] | It is fixed now as the first Phase-2 score (I-7). Phase 2 is committed: it runs and is scored whatever Phase 1 shows, and any stop or change after the Phase-1 score makes it EXPLORATORY (A133 §3). Its rosters come from the pinned roster builder, with gate documents pinned before the Phase-1 score (§4). |
| Reading Phase-2 outputs early once Phase 1 is public [r3a] | Phase-2-only outputs stay validity-only until Phase-2 step 4, which begins automatically on terminal receipts (Status, §6.3). |
| Selective display of the sensitivity band | One fixed column for all 43 rows; never used for a tier or reading (§1.1, §8). |
| Selective display of the Phase-1 band [r3a] | One fixed column for all 43 rows in Phase 1; never used for a tier, flag, pattern, reading or uncertainty claim (§1.1, §8). |
| Dropping rows or inflating σ | Prohibited (I-1, I-2). The grid uncertainty does not widen σ (D-2). |
| **Residual risk (not closed): consequences of registered choices.** | They are recorded so that root rules knowingly (M-3, M-9, M-15). (i) With N_v(OUTER) = 1, one missing valid OUTER row gives OUTER_FAILURE and the TESTED-NEGATIVE verdict. (ii) A twin that gains a hit while its median |r| does not fall reads NOT_DECIDED [r3a]. (iii) A twin that shrinks every residual but gains no hit reads NOT_DECIDED, not AGAINST. (iv) An OUTER zone whose non-INVALID rows are all LATE-gate rows reads P14 and TESTED-NEGATIVE with no OUTER prediction, while the same rows gated on time read P9 and NOT_TESTABLE. (v) Under the §2 sign rule, a zone's sign class depends on whether its gates are LATE: a LATE gate can only withhold a sign class (M-3 records the alternative rule). |
| **Residual risk (not closed) [r3a]: the window between the first readable Phase-1 value and the Phase-1 score.** | After the seal and the Phase-1 freeze, Phase-1 prediction values are readable before the Phase-1 score is made. Within that window, Phase 2 is still the score of record after any of these: an A133 §3 rule change; a first pin of the roster builder, RUNBOOK_V002, its step map or an M-11/M-13 carrier; a successor or re-pin of the Phase-1 tool (`band`, `agree`), which the seal entry first pins (M-6); or a successor or re-pin of the per-point certificate producer, its settings or its shell rule (I-6). The report header of both phases discloses each such change, labelled POST-PREDICTION, with the entry that made it (§8). The roster builder also shapes the Phase-1 rosters. |
| **Residual risk (not closed) [r3a]: a stop or change after Phase-2-only values are readable.** | It makes Phase 2 EXPLORATORY (I-7), and Phase 2 stays the score of record under that label. Each such stop or change is listed in the commitment status with the entry that made it, and a missing status reads EXPLORATORY. |
| **Residual risk (not closed): NEAR depends on the envelope width,** which depends on the member-selection rule. | That rule is frozen with the manifest. NEAR is a flag and changes no pattern. |

## 10. Root items for this prereg (decide before the seal) [C-10]

Each item's recommended ruling, with its reasoning, is in `ROOT_ITEMS_R3A.md`. Items M-1 to M-5 are V001's five pending items; M-6 to M-14 are new in r2; M-15 is new in r3, and M-16 in r3a [r3a].

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
| M-16 | The Phase-1 band column (§1.1, §8) [r3a] |

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
| 0687 | `60c9595d50fc4884c5444607e1f95d15e21936eff026f67d9e2d3871508b206b` |

**Lane posts:**

| post | path | sha256 |
|---|---|---|
| Codex1 0032 (GQ_NGC at M_s 96 holds) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0032_2026-10-18_gq91_pass_and_latest_rulings.md` | `3e8c9fc9e65a10791f8ecbda3702556a851391350f06ed013222bd12876ab2f7` |
| Codex1 0056 (the formal K32 result) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0056_2026-10-18_ngc_k32_complete_n_fail_n1_a66_open.md` | `4b67319dddb4799e71420881f6624fdcd1640cd5f560a4adce06cd2030af72aa` |
| Codex1 0058 (the steps 6–7 rehearsal) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0058_2026-10-18_0603_synthetic_steps6_7_finished.md` | `fc5af8318febd8dd86037d7aeddff9a590ea8e436deb15f002b9c4775c65cea2` |
| Codex1 0066 (the LO I1-T star-transform convergence, TESTED PASS) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0066_2026-10-18_tail_transform_finite_convergence_finished.md` | `f2d946559d6b2abb0563f10c2e0c297a3e004477b87e7cd9958c2cca679647ff` |
| Codex2 0490 (the cross-lineage review of r2 round 2) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0490_2026-10-18_miss_reading_r2_round2_review_finished.md` | `3a922168f800de5ae9fff2ba1cb55af2f55d7ae4290a75b14a0ca2daa36a2649` |
| Codex3 0618 (the step-5 carriers) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0618_2026-10-18_dispatch0606_carriers_finished.md` | `8939c004e4bea1728eed610e4d98b98dffbe4333be1433c539feb16159de60a7` |
| Codex1 0080 (CX1-MR3-P1 raised) [r3a] | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0080_2026-10-18_miss_reading_r3_preparation_two_shouldfix_pending.md` | `f423415cd07a871241ed2842dcd4c21da5fcb2f5f9a0ac40dce136372f3a8a0a` |
| Codex1 0119 (the r3 A98.2 delta, no blocking finding) [r3a] | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0119_2026-10-18_miss_reading_r3_A98_delta_PASS_0.md` | `ae2374c47fd4f71ca4e59321238daf3ec68d415e2a4719451e33a3aef468db3a` |
| Codex1 0120 (CX1-MR3-P1 carried as SHOULD_FIX) [r3a] | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0120_2026-10-18_ack_0125_carry_MR3_P1_shouldfix.md` | `27d2bd750f0161446c7474bbcaeab59edff9a937d85600a67ce0e470a2a0dfcf` |
| Claude4 0124 (the r3 seal candidate) [r3a] | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0124_2026-10-19_SEAL_CANDIDATE_miss_reading_prereg_r3.md` | `73f5faab369abcd20dc7901811b0eae9d0cb8a9135c0df61b66f185d7b9c71b2` |
| Claude4 0125 (the CX1-MR3-P1 fix proposed) [r3a] | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0125_2026-10-19_miss_reading_r3_built_for_codex1_delta.md` | `a58d1804234004676bfee1741ae36d758150f7a2a9b599d122bd913a7d8387f4` |

**Root decisions** (`…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00n[_ADDENDUM].md`):

| addendum | entries used | sha256 |
|---|---|---|
| V003 (frozen) | A10, A12 | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` |
| V004 (frozen) | A13, A14, A15, A16, A17, A20, A21, A23, A27, A41, A42 | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| V005 (closed with A106, its last entry; later root rulings go in V006, A82 and A106.3) | the entries in the next table | `@@V005_SHA@@` (whole file, read at assembly) |
| V006 (open; every root ruling after A106, this text's seal entry included, A82 and A106.3) | the entries in the V006 entry table below | `@@V006_SHA@@` (whole file, read at assembly) |
| `…/CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` (the A133 text of record, adopted as written in A133; r3a) | its §1 to §5 | `cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17` |

**V005 entries: the entry table** (read at @@V005_READ_UTC@@).
- **The record.** `V005_ENTRY_TABLE_R3A.json` is hand-written. It has one row for every heading line of V005 that starts with `## `, each exactly once and in file order, suffix and amendment forms included. Each row is either CITED_PINNED, with the sha256 of its section and the reason this text cites it, or NO_CHANGE, with the reason it changes nothing here. It records the V005 whole-file sha256 and the `date -u` time at which it was read. The generator renders it below and verifies it; it never writes a reason.
- **Why per-entry pins.** The V005 file stayed open while this text was written, and root kept adding entries to it until A106 closed it (A106.3). So each cited entry is pinned by the sha256 of its own section: the bytes from its heading line up to the next `## ` heading line, or up to the end-marker shown. For a NO_CHANGE row, the sha shown is that of its section as read.
- **The checks.**
  - The target-free check (T5) re-extracts the cited sections from the current bytes. Any V005 entry that one of the three texts names outside these tables counts as cited and must be CITED_PINNED, including an entry named only in the closure tables of `CLAUSE_SOURCE_MAP_R3A.md`.
  - Check T7 (currency) fails on any `## ` heading line that has no row, more than one row, a row out of file order or a row that differs from it; on any section, NO_CHANGE ones included, that changed since the table was read; and on a changed whole-file sha.

@@V005_ENTRY_TABLE@@

From V005, V001 cited only the A48 principle and the 0518 log, which sits in the pinned A65 section.

**V006 entries: the V006 entry table** (read at @@V006_READ_UTC@@).
- **The record.** `V006_ENTRY_TABLE_R3A.json` is hand-written, with the rows of the V005 table, the V006 whole-file sha256 it was read at, that sha with trailing newlines removed, and the `date -u` read time. It has one row for every `## ` heading line of V006 written before this text's seal entry, each exactly once and in file order: CITED_PINNED, with its section sha256 and the reason this text cites it, or NO_CHANGE, with the reason it changes nothing here. The generator renders it below and verifies it; it never writes a reason. A V006 section sha256 is taken over the section with its trailing newlines removed, so that appending a later entry leaves it unchanged.
- **The seal entry and later entries.** The seal entry is the first V006 heading whose section contains the sha256 of this text as rendered. It and every later V006 heading lie outside the table, so no entry pins a table that pins it. No earlier V006 entry may name that sha, since that would be a pin cycle.
- **Inputs are not changes.** Some V006 entries only supply an input that this text names: the M-8 decision on a FREEZE_INCOMPLETE score, the gate pins and statuses of M-15, an N-test successor (I-6), the STAGE0 successor (M-14), a field map (§1.1), the M-13 C3 record, and in r3a [r3a] a carriers successor (M-5), the Phase-1 tool whose `band` and `agree` shas the seal entry pins (M-6), and the per-point certificate records of each NGC call (I-6, D-4). The classifier reads each at the sha that the seal or score entry pins. Such an entry is never read as a change to this text; if it comes before the seal entry, its row is NO_CHANGE with that reason. A carriers successor adopted after the seal is read only through a key-only field map pinned before the classifier output is read (§1.1). If it changes a value encoding, the carrier's fields are defective under §1.1: a carrier that is a stop input (the TSR flag record or the TSR support record) fires each stop that its fields trip, and any other carrier reads NOT_AVAILABLE where it is used [r3a].
- **The checks.**
  - T5 treats a V006 entry that the three texts name like a V005 entry: it must be CITED_PINNED, with its section sha.
  - Check T7 (currency) fails on any V006 heading before the seal entry that has no row, more than one row, a row out of file order or a row that differs from it, and on any such section, NO_CHANGE ones included, that changed since the table was read.
  - Before the seal entry exists, T7 also fails on a changed whole-file sha. Once it exists, the bytes before its heading, with trailing newlines removed, must hash to the trimmed sha read at assembly.

@@V006_ENTRY_TABLE@@

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
| `claude_artifacts/miss_reading_prereg_c4/r3/PREREG_MISS_READING_R3.md` (r3 as rendered, the 0124 seal candidate; r3a) | `b0fba984543c5c93fc4d25497c6e9e97f33662d3a98a63856b4933e4b1f47dd0` |
| `claude_artifacts/miss_reading_prereg_c4/r3/ROOT_ITEMS_R3.md` (r3's root items, the 0124 seal candidate; r3a) | `b33270fe9e07bbe3990cdeca6859daf08dd7d1e9836936befd2086d023edc4fb` |
| `claude_artifacts/review_freeze_v003g_c4/REVIEW_FREEZE_V003G_C4V001.md` | `575f872c00c22a00eb29a97eac7e594562b1e07843354baa110674702c4c68a4` |
