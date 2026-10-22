# PREREG_MISS_READING_R2 — how the 43 NGC3198 rows will be read (UNSEALED DRAFT r2, round 2; written before any NGC3198 target is opened)

## Status [C-S]

- **What this is.** Draft r2 for root (dispatch 0585, with 0606). When root seals it, it supersedes V001 (`6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345`). V001 stays as history.
- **Rounds.** This is round 2. Round 1 (`r2/round1/`) was checked by three refute-by-default lenses. Every round-1 finding is closed or answered in the closure table of `CLAUSE_SOURCE_MAP_R2.md`.
- **Author.** Claude4, single author.
- **No target was opened.** No NGC3198 target, observed velocity or target-bearing file was opened in writing it. The only NGC3198 data read are:
  - query ids and radii from the target-free query block of slots V003;
  - the target-free N-test and node records named in §11.
- **It changes nothing in the score.** Freeze v003g computes the LADDER rows in root's two-pass freeze:
  - module `48a1e48a…`, PASS in Claude4 0071;
  - RUNBOOK_V001 `9557b5aa…`.

  This document classifies and reads those rows afterwards.
- **Clause tags.** Each clause carries a tag in square brackets; for example, the tier rule's tag is C-1.1. The tags key the clause source map.
- **When the seal happens (binding).**
  - Root rules on root items M-1 to M-14 and seals this text, together with the M-12 classifier, before anyone reads any step-5 NGC route-A/B output value. "Anyone" means root, the author, and every reviewer of this text or of the classifier. "Output value" means a prediction, a band, an envelope, a sensitivity row or an alternative row.
  - The preferred timing is to seal before step 5 launches. A80 put step 5 more than a day away.
  - The seal is root's entry registering this text's sha256 (M-6).
  - Until the seal, step-5 outputs are read in validity-only form, the pattern of A47 I3. The seal entry attests to this.
  - If the timing is not met, every root item is adopted exactly as this text recommends, with no option switching, and the report header discloses the deviation.

**Binding principles** (A10, A12.3, A15 E3, A20, A23, A41, A48) **[C-P]**:
- Every outcome registers; nothing is prescribed.
- A miss is never reported as a failure of UNT in general. Under A15 E3, an outer-row failure is TESTED-NEGATIVE for exactly the present-mass-only lapse response of the L = 4 coefficient method, at the A2 grid and the calibrated θ. §2 defines "outer-row failure" (OUTER_FAILURE), and §5.3 gives the E3 verdict line.
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
  - the root-pinned row-registration rosters (0531; v003g);
  - the query radius R_q, bound by query id to the slots V003 query block, with Rad_unit kpc (v003g fixes F2 and F3);
  - the TRUNCATION_SHAPE_RESIDUAL flag rule of §1.4, applied to the pinned production N-test and node records;
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
    - NGC route A/B is not run unless that record's `n_route_ab_gate` reads OPEN (0550; A66.2–A66.3).
    - The gate is OPEN for N_PASS, and for N_FAIL_N1 confined to TRUNCATION_SHAPE rings (reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66).
    - It is BLOCKED for any of these:
      - a failure of N0, NQ, N2 or N3′;
      - an N1 failure on a ring that is not TRUNCATION_SHAPE;
      - N_INCOMPLETE or N_NO_RUN.
    - With the gate BLOCKED there is no route-A/B run and no score, and this document is not applied.
    - **At writing**, the record reads N_FAIL_N1 with tests read, and the gate is OPEN for the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66.
  - **Certificates.**
    - EPS_NGC, LO_NGC and GQ_NGC are certified to coverage at least √2·64 ≈ 91 /kpc (A64.2). No NGC N-test is read until all three are slotted (A81 RI-23), and the NGC I1-T check passes before any NGC N-test is read (A52).
    - The NGC N-test LO record is LO_NGC_K32_CERT_V001, with coverage to 91 (A90).
    - The LO I1-T precondition (independent tail-domain star-transform convergence, NOT_RUN) is ruled by root before any NGC route-A/B launch (A90). That ruling is recorded in D-4 with its sha.
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
  - **An incomplete freeze.** If root authorizes scoring a FREEZE_INCOMPLETE manifest, the classification is still made and reported in full. Every pattern and reading then carries the label PROVISIONAL (FREEZE_INCOMPLETE), with the manifest's `incomplete_reasons` (root item M-8; the A50 PROVISIONAL rule, by analogy).
  - **NEAR under an incomplete freeze.** If a PRIMARY member is unevaluated, the envelope rows may be invalid. The NEAR flag then cannot be set, and the report says so.

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

- **The NEAR flag** is set on a MISS row when `E_q.band_overlaps_error_bar = true`, meaning the frozen PRIMARY pointwise envelope interval [lo_q, hi_q] intersects the error bar [v_q − σ_q, v_q + σ_q].
  - It does **not** mean that any single member is within error. Members lying on both sides of the bar also produce it.
  - NEAR is reported as "envelope overlaps the error bar". A NEAR row stays a MISS for every count and pattern in §2.
- **The sensitivity band.** The box-limited sensitivity band (`sensitivity.rows`) is never used for a tier, a flag, a pattern or a reading.
  - It is reported in one fixed column for all 43 rows: "sensitivity band overlaps: yes / no / invalid", labelled "conditional on trial values".
  - An invalid sensitivity row is reported as invalid, never as a zero-width band. This applies, for example, when the geometry sensitivity is refused as registered.
- **A row with no ratio.** A VALID row whose `sigma_ratio` is null (v003g NON_FINITE_SIGMA_RATIO) is a MISS with sign UNDEFINED. It counts in N_v(Z) and M(Z), and it is left out of m(Z) and Δ_out.
- **Pre-score checks (binding).** Every stop condition below is target-free.
  - **When they run.** Each is checked on the frozen manifest and slots **before any target is opened**, through the sealed classifier (M-12) run on a synthetic score built from the frozen member arrays. The result goes in the seal or score entry.
  - **The stop conditions:**
    - the reference member's row status is UNEVALUATED_OR_REFUSED (REFERENCE_RULE excludes this);
    - a field named here is missing;
    - the reference member's ids are not Q01 to Q43 in order;
    - the envelope label prefix differs;
    - the zone table of §1.3 differs.

    Any of these stops the classification with CLASSIFICATION_INPUT_DEFECT, before target access.
  - **After target access,** root may only:
    - correct a field map without changing any value; or
    - declare the classification NOT_READ.

    Root may never change a tier, zone, pattern, member or reading rule after target access.
- Root item **M-1**.

### 1.2 Sign [C-1.2]

- s_q = sign(r_q), one of −1, 0, +1, or UNDEFINED when r_q is null. **Deficit** (−1): the model is below the quoted value. **Excess** (+1): the model is above it.
- INVALID rows carry no sign.

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
- **The overlap rule is derived, not chosen** (root item M-7):
  - The N1 rings are the registered GL4 route-B nodes. The 100 ring radii of the production N1 record equal, bitwise, the 100 GL4 node radii of `REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (`ec1dcca5…`).
  - The registered observation rule (slots V003) is piecewise-linear interpolation of the azimuthal mean onto the 43 manifest radii, without extrapolation.
  - So a query value depends on node k if and only if its R_q lies strictly between nodes k − 1 and k + 1.
  - **A query row is flagged if and only if r_{k−1} < R_q < r_{k+1} for a failing TRUNCATION_SHAPE ring k.** Its R_q is bound by id, and the ring radii come from the production N1 record.
- **At writing** (Codex1 0056; A90; records pinned in §11):
  - the production compare reads N_FAIL_N1, with tests read;
  - exactly one TRUNCATION_SHAPE ring fails: ordinal 15, at R = 10.54 kpc, with S/θ = 1.0148 and criterion C1;
  - no ring of any other class fails;
  - N0, NQ, N2 and N3′ pass;
  - the gate reads OPEN.
- **The flagged rows, fixed here by id.**
  - The neighbouring rings are at 9.90 and 10.91 kpc, so exactly one row is flagged: **NGC3198-Q25** (10.04 kpc, TRANSITION).
  - NGC3198-Q26 (11.04 kpc) lies beyond ring 16, so it does not depend on ring 15 and is not flagged.
  - If the formal record changes before the seal, the flagged ids are recomputed from target-free data and listed here before the seal.
- **The carrier.**
  - The flag record is root-pinned and target-free. It lists the failing rings, the rule above and the flagged ids, and it is pinned among the freeze manifest's input files.
  - Codex3's step-5 carrier extractor (0618) emits the 43 flags from an adopted support. It leaves them UNAVAILABLE until root adopts one, and it requires the support to contain its native ring. The interval above contains ring 15.
  - v003g has no flag field (M-7).

## 2. Zone summaries and patterns (algorithmic; every applicable pattern is reported) [C-2]

**Per-zone summaries.** For each zone Z:
- **Counts.**
  - N_v(Z) is the number of non-INVALID rows.
  - H(Z) and M(Z) are the HIT and MISS counts. NEAR-flagged rows are MISS rows.
  - N(Z) is the number of NEAR-flagged rows.
  - I(Z) is the INVALID count, also given per registered reason.
- **m(Z):** the median of r_q over the non-INVALID rows that have a defined r_q. For an even count it is the mean of the two middle values. It is UNDEFINED when there is no such row.
- **Sign class S(Z):** DEFICIT if m(Z) < −1, EXCESS if m(Z) > +1, otherwise CENTERED. It is UNDEFINED when m(Z) is UNDEFINED.
- **Miss-dominated:** N_v(Z) ≥ 1 and M(Z) ≥ N_v(Z)/2.
- **Hit-dominated:** N_v(Z) ≥ 1 and H(Z) > N_v(Z)/2, a strict majority.
  - The two are exclusive. A tie reads miss-dominated, the reading less favourable to the model (A48 principle).
- **Clarifications.**
  - Any condition that uses an UNDEFINED quantity is false, and it is reported as UNDEFINED.
  - A pattern whose condition is about rows needs at least one non-INVALID row; it never holds vacuously.

**Outer trend.**
- Sort the OUTER rows that are non-INVALID and have a defined r_q by R_q, and split them into a near half and a far half. With an odd count, the middle row goes to the far half.
- Δ_out = median r(far half) − median r(near half). It is UNDEFINED if fewer than 2 such rows exist.
- **GROWING** holds if and only if S(OUTER) = DEFICIT, Δ_out < 0, and m(TRANSITION) > m(OUTER).

**OUTER_FAILURE.** This is the "outer-row failure" of A15 E3, registered here as: OUTER is miss-dominated, whatever its sign class. It holds exactly when one of P1, P2 or P11 holds.

**Patterns.** Each pattern is evaluated independently, and every one that holds is reported. No pattern masks another.
- **Coverage.** Every outcome with at least one MISS satisfies at least one of these: a zone pattern (P1, P2, P11, P3, P4, P12 or P13), or P7.

| id | pattern | condition |
|---|---|---|
| P0 | INVALID rows | I(Z) > 0 in any zone; reported per zone and per registered reason (§4) |
| P1 | OUTER_DEFICIT | OUTER miss-dominated and S(OUTER) = DEFICIT; flag **P1g** if GROWING |
| P2 | OUTER_EXCESS | OUTER miss-dominated and S(OUTER) = EXCESS |
| P11 | OUTER_MIXED | OUTER miss-dominated and S(OUTER) = CENTERED (misses of both signs, or small residuals) |
| P3 | INNER_EXCESS | INNER miss-dominated and S(INNER) = EXCESS |
| P4 | INNER_DEFICIT | INNER miss-dominated and S(INNER) = DEFICIT |
| P12 | INNER_MIXED | INNER miss-dominated and S(INNER) = CENTERED |
| P13 | TRANSITION_MISS | TRANSITION miss-dominated, with S(TRANSITION) reported |
| P5 | TRANSITION_ONSET | INNER hit-dominated, OUTER miss-dominated, N_v(TRANSITION) ≥ 1, and TRANSITION not hit-dominated |
| P6 | GLOBAL_OFFSET | S(INNER) = S(TRANSITION) = S(OUTER) ≠ CENTERED, with N_v ≥ 1 in each zone |
| P7 | SCATTERED | at least one MISS, and no zone miss-dominated |
| P8 | NO_MISS_AMONG_VALID_ROWS | at least one non-INVALID row, and M = 0 over all non-INVALID rows. Never reported as "all hit": INVALID rows still score as misses (§4). It is always reported with I and N, and it can hold together with P0 and P9. |
| P9 | OUTER_UNTESTABLE | N_v(OUTER) = 0: every OUTER row is INVALID |
| P10 | TSR_MISS | at least one non-INVALID MISS row carries the TRUNCATION_SHAPE_RESIDUAL flag |

- **Also reported for each zone:** the counts, m(Z), S(Z), the NEAR-flagged rows, and the individual rows.
- **The flagged-row list.** Whenever any row is flagged, the report lists every flagged row with its tier, INVALID included. This is a disclosure, not a pattern input.

## 3. Readings, deciding tests, and the status of each reading [C-3]

**Rules for every reading:**
- **A status tuple.** Each registered reading of every pattern that holds is reported as a fixed tuple of three parts:
  1. **score relation:** CONSISTENT, INCONSISTENT or NOT_ADDRESSED.
     - It is CONSISTENT when the reading's pattern holds and none of its against-conditions holds.
     - It is INCONSISTENT when any registered against-condition holds. **Against takes precedence.**
     - It is NOT_ADDRESSED when the reading's pattern does not hold.
  2. **deciding-test status:** OPEN when the deciding test is NOT SCHEDULED or has not run; otherwise the test's registered outcome.
  3. **prior evidence:** the evidence for and against the reading registered before the score, named by entry. It never changes parts 1 and 2.

  "CONSISTENT" is never reported without the deciding-test status beside it.
- **No support from the score alone.** The 43-row score can make a reading CONSISTENT or INCONSISTENT. It can never make it supported. Support comes only from that reading's own deciding test, run under its own pre-registration.
  - A deciding test registered after NGC3198 target access can support a reading only through data not opened when its prereg was sealed.
- **Fixed list.** The readings below are the registered list. Any reading proposed after targets are opened is labelled **EXPLORATORY (post-score)** and never counts as registered.
- **Scope.** A reading may cite only rows of the zones named by the pattern that triggers it. R-TSR cites only flagged rows, and no reading cites an INVALID row (§4).
- **R-MF's verdict.** R-MF is TESTED-NEGATIVE, for exactly the A15 E3 scope, if and only if OUTER_FAILURE holds (the E3 verdict line, §5.3). The sign class is reported with it.

**Deciding tests and their status at writing [C-3.1]:**

| id | deciding test | status |
|---|---|---|
| DT-UT1 | The UT-1 spec-compliant model version: k = 0 a declared zero mode; k → 0⁺ from k ≠ 0 nodes only, under one pre-registered continuation rule; recomputed end to end (A41). | **NOT SCHEDULED**: 0521 withdrawn by 0524 |
| DT-BHD | BH-D derivation from the owned parent, then out-of-sample tests (TDGs, Leo Ring, DF2/DF4) once BH-D exists (A10). | **NOT SCHEDULED**: 0519 withdrawn by 0524 |
| DT-U12 | Small-k limits at larger L and with mixed sampling: U1, U2 and the P-96 capture (A20, A41). | **NOT SCHEDULED**. U2 (0523) was withdrawn by 0524. Stage 0, the L = 4 control, is complete; its sealed outcome is S0-FAIL-RHAT (A63). P-96 at L ≥ 6 needs a root decision, which is not pursued during the galaxy run (A63, per the principal). |
| DT-T1a | BH-T1a: the residual against the target-free stellar fraction f★ (PRIMARY enclosed, SECONDARY local; f★ variants at M/L 0.4 and 0.6). Diagnostic, never headline; runs only after a verified freeze (A10, A16.3). It moves no prediction. | registered |
| DT-GEO | The geometry box (D 12.545–15.18 Mpc, i 69–75°). | NOT_EVALUATED_BEFORE_FREEZE (A16.1). The forward refuses with GEOMETRY_NOT_EXPOSED (A16, item 4). Any geometry evaluated after the freeze is EXPLORATORY. |
| DT-ALT | The alternatives, scored separately (§6). ORIGINAL_K is evaluated. ML_3p6_0.4, ML_3p6_0.6 and GL10_SOURCE_GAUSS_ORDER are NOT_EVALUATED_BEFORE_FREEZE (A16.2; 0518 item 5). | as stated |
| DT-NAX | Non-axisymmetric finite-flow sensitivity of the m = 0 approximation (plan D3). | not run |
| DT-S1 | Calibration transfer of G_eff = G·Q∞ across parameter space (A21: S1 UNTESTED). | UNTESTED |
| **DT-S0G** | **STAGE0_GRID_OUTER** (A65.2): the NGC route-A/B prediction at the headline admitted DDO154 calibration point(s), with the coefficient grid swapped from A2 (`2e3a36d8…`) to the stage-0 pooled grid (`bdb9016c…`). Everything else is identical. It is a coefficient-grid sensitivity at fixed calibrated parameters, not a recalibration. Read by §6.3. | NOT_EVALUATED_BEFORE_FREEZE in slots V003. Evaluated only under the receipt rule of §6.3 (M-14). |
| **DT-TSR** | A kept-cube corner-shape variation that removes the residual on the flagged rows. No such test is registered. | **NOT SCHEDULED** |

**Readings by pattern [C-3.2].** "Against" lists only conditions that can be decided at the score step. Prior evidence is listed separately.

| pattern | reading | against (decided at the score step) | prior evidence (registered before the score) | deciding test |
|---|---|---|---|---|
| **P1, P1g, P2, P11** (OUTER_FAILURE; expected: A15 E2) | **R-MF:** failure of the present-mass-only lapse response of the L = 4 coefficient method at the A2 grid and the calibrated θ (A15 E3). TESTED-NEGATIVE for exactly this scope when OUTER_FAILURE holds. | OUTER not miss-dominated, with N_v(OUTER) ≥ 1 | for: A15 E2, A41 | the score itself, for this scope only |
| P1, P1g | **R-UT1:** the static isothermal typing of the k = 0 block (A20 reading 1; counted CA-34/CA-28, A41) | — | against: A41 item 3 (FORMAL + TESTED). No gate-consistent typing gives an attractive tail, and the spec-compliant T(0⁺) is finite and repulsive on current estimates. | DT-UT1 (NOT SCHEDULED) |
| P1, P1g | **R-HIST:** a missing Bind-history or collective component (A10 SA-BH-01, DECLARED-PREMISE; A20 reading 2; BH-D). P1g makes it more specific ("missing long-range component", 0522). | — | — | DT-BHD (NOT SCHEDULED) |
| P1, P1g | **R-REACH:** magnitudes, k = 0-block drift or finite-size effects at larger L or with mixing (A20 narrowed: these cannot create a 1/r tail) | — | — | DT-U12 (NOT SCHEDULED) |
| P1, P1g, P2, P11 | **R-DRIFT** (A63/A65): A2's k = 0 entry, which enters the k → 0⁺ transfer under CA-34, is drift-inflated | DT-S0G reads AGAINST (§6.3) | for: the sealed k = 0 drift reading is SUPPORTED (A63). Against: its causal gloss is UNTESTED (A65 check R-3). | DT-S0G; it never makes R-DRIFT supported |
| P2, P11 | **R-S1:** calibration transfer of G_eff = G·Q∞ (A21) | — | — | DT-S1 (UNTESTED) |
| P2, P11 | **R-GRID** (numerical): k-grid fidelity of the in-use T120L grid at outer radii (A17) | — | against: T120L passes C2, C3, C4 and C1′ (A27). The production N-tests N0, NQ, N2 and N3′ pass (A90). | none registered: OPEN |
| P11 | **R-NAX:** non-axisymmetric flow and the m = 0 projection (A17 note; D3) | — | — | DT-NAX (not run) |
| **P3, P4, P12** | **R-GEFF:** the single DDO154 short-wavelength G_eff does not carry over to a galaxy with stellar share about 0.51 (DDO154: about 0.03; A10) (A21, E1) | — | — | DT-S1 |
| P3, P4, P12 | **R-ML:** stellar M/L (0.5, counted ±20%; A10) | The ML_3p6 alternatives, if evaluated before the freeze, leave every INNER MISS a MISS. They are NOT_EVALUATED_BEFORE_FREEZE, so this reads NOT_AVAILABLE. | — | DT-ALT (M/L); DT-T1a (diagnostic, jointly with R-SPEC) |
| P3, P4, P12 | **R-SPEC:** a species or history weight (SA-BH-01) | — | — | DT-T1a (diagnostic, jointly with R-ML) |
| P3, P4, P12, P6 | **R-GEO:** geometry (A23) | — | — | DT-GEO (NOT_EVALUATED; stays OPEN by construction) |
| P3, P4, P12, P7, P13 | **R-NAX** | — | — | DT-NAX (not run) |
| **P5** | as P1 for the OUTER rows (including R-DRIFT), and R-NAX for the transition zone | as P1 | as P1 | as P1; DT-NAX |
| **P13** | **R-NAX** for the transition zone; R-TSR for flagged rows (via P10) | — | — | DT-NAX; DT-TSR |
| **P6** | **R-S1** (the G_eff scale); **R-GEO** (the distance scale); **R-MF** at all radii (CONSISTENT only; TESTED-NEGATIVE only through OUTER_FAILURE) | — | — | DT-S1, DT-GEO |
| **P7** | **R-NAX** and **R-MF** at row level, both always reported | — | — | DT-NAX |
| **P8** | No miss reading. If N_v(OUTER) ≥ 1 and M(OUTER) = 0 (OUTER_NO_MISS), it runs **against** the A15 E2 expectation and is reported as such. | — | — | **A mandatory report:** ORIGINAL_K's twin classification for OUTER (§6.1), and the T120L C3 record (A27). That record must be pinned before the freeze; otherwise that half reads NOT_AVAILABLE (M-13). Neither half changes the headline or any status. |
| **P9** | The outer test is unavailable (every OUTER row INVALID); E2 reads NOT_TESTABLE. R-DRIFT stays OPEN. | — | — | the outer-gas confinement question (A12.5), not a rotation-row test |
| **P10** | **R-TSR** (numerical): a MISS on a flagged row may reflect the residual cube-corner anisotropy of the kept cube (K = 2) (A66.2) | — | against: route B consumes the azimuthal mean, so the φ-spread S enters no row directly (A66.2; A42 TESTED) | DT-TSR (NOT SCHEDULED) |

**Descriptive lines (no status effect).**
- **Onset radius:** the smallest R_q of a MISS row in TRANSITION ∪ OUTER. It is reported with k* (A12: wavelengths of tens of kpc) as a comparison only.
- **R-ML and R-SPEC:** a DT-T1a trend is reported under both together, never under one alone. DT-T1a varies f★ for a correlation and moves no prediction (A10, A16.3).

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
- **Late gates.** A root-listed gate registered after any step-5 output value exists is a LATE gate.
  - Its rows still score INVALID_AS_MISS in LADDER.
  - For this document's counts and patterns, each LATE-gate row counts as a non-INVALID MISS row with sign UNDEFINED. A late gate can therefore never remove a pattern or create P9.
  - The report marks such rows GATE_AFTER_PREDICTIONS. Built-in reasons are unaffected.

**Scoring and reporting.**
- INVALID rows are scored as worst-tier misses and counted in the 43 (0518 items 1–2). D1 is applied over the registered-valid rows only (0518 item 3).
- INVALID rows are listed separately, per reason, with each row's zone.
- For the outer-gas cut, the report also gives the pinned cut record's truncation radius and dropped HI mass fraction (the V001 §4 requirement).

**No part in the readings.**
- INVALID rows are excluded from N_v(Z), from m(Z), and from every pattern except P0 and P9. Every INVALID OUTER row counts toward P9.
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
  - OUTER_FAILURE (P1/P2/P11, with the sign class);
  - OUTER_NO_MISS (N_v(OUTER) ≥ 1 and M(OUTER) = 0);
  - P9;
  - the OUTER INVALID counts per reason. A15 E2 foresaw outer rows becoming INVALID through route-A outer-gas unconfinement.
- Label: "COMPARISON with A15 E2".

**E3, the verdict line [C-5.3].** One line, always reported, computed on the frozen reference member. Its value is one of:
- **TESTED-NEGATIVE (A15 E3 scope)**, if and only if OUTER_FAILURE holds;
- **NOT_NEGATIVE_AT_OUTER**, if N_v(OUTER) ≥ 1 and OUTER_FAILURE does not hold;
- **NOT_TESTABLE**, if N_v(OUTER) = 0 (P9).

The line always prints S(OUTER), Δ_out, and N_v, H, M, N and I per reason for OUTER.

**Never an adjustment [C-5.4].** No expectation is adjusted, and no row is re-read, to improve agreement.

## 6. Alternatives (scored separately; never the headline)

### 6.1 Evaluated non-PRIMARY alternatives: the twin rule [C-6.1]

v003g requires every evaluated alternative's members to equal the PRIMARY's selected representatives, in log_index, role and order. It scores those members, but selects no reference member and band-scores no alternative envelope. So:
- **The twin.** An alternative's twin is its member with the same `log_index` as the frozen PRIMARY reference member. One exists by construction.
- **A valid twin** has `member_valid = true`. Otherwise the alternative reads TWIN_INVALID, and only its scored member distribution is reported.
- **Classification.** A valid twin's rows are classified INVALID_AS_MISS, HIT or MISS by M-T, using the twin's own INVALID set. There is no NEAR flag.
- **Id check.** The twin's ids must equal its scope: Q01 to Q43 for a full-row alternative, or `scoring_scope.query_ids` for STAGE0. A mismatch reads TWIN_INPUT_DEFECT.
- **Summaries and patterns** for an alternative use the §2 rules (with N(Z) = 0) and are reported under its name.
- **Limits on use.** They never trigger, confirm or refute a PRIMARY reading. The only exceptions are the P8 report, which names ORIGINAL_K, and §6.3 for STAGE0_GRID_OUTER and R-DRIFT.
- Root item **M-10**.

### 6.2 Alternatives not evaluated before the freeze [C-6.2]

Only the status is reported: "NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline". This covers:
- ML_3p6_0.4, ML_3p6_0.6 and GL10_SOURCE_GAUSS_ORDER;
- any recorded distance alternative;
- STAGE0_GRID_OUTER, unless it is evaluated under §6.3.

### 6.3 STAGE0_GRID_OUTER [C-6.3]

**At writing:** NOT_EVALUATED_BEFORE_FREEZE; headline false; scope OUTER Q36–Q43 (R ≥ 30 kpc, inclusive); grid `bdb9016c…`.

**When it is evaluated (the receipt rule; root item M-14).**
- STAGE0 is EVALUATED_BEFORE_FREEZE if and only if every registered STAGE0 member has a FINISHED receipt before the freeze manifest is written, and an adopted successor admits it.
- Root decides on receipts and validity booleans only, reads no prediction value, and records the receipt times.
- Otherwise it reads NOT_EVALUATED_BEFORE_FREEZE (A65.2), and R-DRIFT stays OPEN.
- A STAGE0 result that first becomes available after the freeze is EXPLORATORY (post-score), and R-DRIFT stays OPEN.

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

**Limits:**
- TWIN_INVALID and NOT_DECIDED leave R-DRIFT OPEN.
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
- the root ruling on the A90 LO I1-T precondition.

## 8. Report format (score step) [C-8]

The report gives:
1. **The header:**
   - the sealed sha of this text;
   - the freeze manifest sha, the registration sha, and the expected manifest sha logged at the freeze;
   - the slots, module, roster and flag-record shas;
   - the classifier sha (M-12);
   - the I-6 values, with their record shas (D-4);
   - the freeze status (I-7);
   - disclosures D-1 to D-4;
   - the timing attestation of the Status section.
2. **The per-row table:** Q_id, zone, R_q, tier, r_q, sign, the NEAR flag, the TRUNCATION_SHAPE_RESIDUAL flag, INVALID reason (with GATE_AFTER_PREDICTIONS where it applies), sensitivity band overlap (yes / no / invalid, conditional on trial values), and notes (the D-2 counted uncertainty).
3. **The zone summaries,** OUTER_FAILURE, and the E3 verdict line (§5.3).
4. **Every pattern that holds.**
5. **For each pattern,** every registered reading with its full status tuple (§3), and each deciding test's status.
6. **The INVALID list,** per reason, with the cut record's truncation radius and dropped mass fraction.
7. **The A15 comparisons** (§5).
8. **The alternatives** (§6). STAGE0_GRID_OUTER comes last, labelled SENSITIVITY only if evaluated.
9. **Any EXPLORATORY (post-score) readings,** labelled as such.

**The words used:**
- "TESTED-NEGATIVE" is used only for R-MF, within its stated scope. The one exception is quoting a registered outcome name verbatim.
- "consistent with" is never written as "supports".
- "SUPPORTED" is used only when quoting the sealed k = 0 drift reading of A63.

## 9. Self-check: could any rule be steered by the outcome? [C-9]

| risk | how it is closed here |
|---|---|
| Ruling the root items, or sealing, after the predictions are readable | The Status timing rule: seal before anyone reads any step-5 output value, with validity-only reads until then. Otherwise every item is adopted as recommended and the deviation disclosed. |
| Moving the zone boundaries or memberships | The cuts are numbers fixed in §1.3, and membership is fixed by query id. A mismatch stops before target access. |
| Redefining HIT, MISS or NEAR after seeing residuals | The tiers use only frozen LADDER fields and the quoted σ (§1.1). NEAR is a flag and changes no count. |
| Choosing which member is scored | The frozen reference member. Alternatives use the twin rule (§6.1). |
| Choosing which pattern to report | Every applicable pattern is reported. The coverage property holds (§2), undefined quantities make conditions false, and ties go to the stricter side. |
| Choosing a reading's status word | A fixed status tuple, with against taking precedence (§3). |
| Upgrading "consistent" to "supported" | Prohibited (§3). DT-S0G never makes R-DRIFT supported (§6.3). |
| Choosing whether the R-MF verdict applies | One sign-agnostic trigger, OUTER_FAILURE, printed in the E3 verdict line (§2, §5.3). |
| Re-explaining INVALID rows | Prohibited (§4). |
| A gate added after the predictions removes a pattern | LATE-gate rows count as MISS rows for this document (§4). |
| Evaluating STAGE0 only if it helps | The receipt rule: receipts and validity booleans only, no prediction value read (§6.3). |
| Flagging rows TRUNCATION_SHAPE_RESIDUAL after seeing misses | The overlap rule is derived from the registered node and interpolation rules, and the flagged ids are fixed by id in §1.4. |
| Choosing K_big, M_s or certificates after targets | All are fixed before step 5 (A64; A81 RI-23; Codex1 0032; A90). The header records them (I-6, D-4). |
| Root discretion after a stop condition | Every stop is checked before target access. Afterwards, only a value-preserving field map or NOT_READ (§1.1). |
| A later re-score | Only the first successful score is classified; later ones are EXPLORATORY (I-7). |
| Selective display of the sensitivity band | One fixed column for all 43 rows; never used for a tier or reading (§1.1, §8). |
| Dropping rows or inflating σ | Prohibited (I-1, I-2). The grid uncertainty does not widen σ (D-2). |
| **Residual risk (not closed): consequences of registered choices.** | They are recorded so that root rules knowingly (M-3, M-9). (i) With N_v(OUTER) = 1, one missing valid OUTER row gives OUTER_FAILURE and the TESTED-NEGATIVE verdict. (ii) A twin that gains one hit reads CONSISTENT, whatever happens to the other rows. (iii) A twin that shrinks every residual but gains no hit reads NOT_DECIDED, not AGAINST. |
| **Residual risk (not closed): NEAR depends on the envelope width,** which depends on the member-selection rule. | That rule is frozen with the manifest. NEAR is a flag and changes no pattern. |

## 10. Root items for this prereg (decide before the seal) [C-10]

Each item's recommended ruling, with its reasoning, is in `ROOT_ITEMS_R2.md`. Items M-1 to M-5 are V001's five pending items; M-6 to M-14 are new in r2.

| item | subject |
|---|---|
| M-1 | Tiers, and the NEAR flag (§1.1) |
| M-2 | Zone cuts and the membership table (§1.3) |
| M-3 | Pattern thresholds, exclusivity, OUTER_FAILURE and the new patterns (§2) |
| M-4 | Deciding tests NOT SCHEDULED, and the readings that stay OPEN (§3) |
| M-5 | Score inputs and field names (v003g) |
| M-6 | The seal: vehicle, timing, cited entries and later entries |
| M-7 | The TRUNCATION_SHAPE_RESIDUAL overlap rule and its carrier |
| M-8 | Scoring a FREEZE_INCOMPLETE manifest |
| M-9 | The DT-S0G comparison rule |
| M-10 | Alternative classification: the twin rule |
| M-11 | The A15 E1(b) baryonic-Newtonian carrier |
| M-12 | A mechanical, sealed classifier, binding at the score step |
| M-13 | A pinned T120L C3 record for the P8 report |
| M-14 | The STAGE0 receipt rule, and the evaluated-STAGE0 successor |

## 11. Sources (sha256 from bytes at writing) [C-11]

**Dispatches** (`/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/`):

| item | sha256 |
|---|---|
| 0512 | `adac97bbf1884f932b1b046f2d1f04b404a15d019ea840f000b34b58ad45d190` |
| 0518 | `0748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279` |
| 0519 | `1cfa78b3c56fd3bdccfc2cf285b53b6f05a76766db0824289fa722125f0c5f5e` |
| 0521 | `27fb0a0e8a2e18d2ec762e42d0c621bec4a71a444af8a72d51dbc5e98736211b` |
| 0522 | `30af5d6811788e9bbed4c470dae0ea9bb4ae5230a734fa7940e942b30ed66160` |
| 0523 | `3a484695e82b957ed880af8269f70fdffea732413f97cff2c92a5d7e97f2150e` |
| 0524 | `d1430abc84025cc4afde31f3fd4fce1845e8d2334e47e95fbeb81936d7dfd4df` |
| 0531 | `7233faf3be6d498a662f9f3dcc743c12420bbc6fa997e606aeb72e7d16ca3cd6` |
| 0535 | `e4bf99106e2d4eae00e2be0ed1b596b0450225bfffe2ac717386f0c13db22f54` |
| 0545 | `4049a3f81b524f5622e0eda6510eeee60c7a6b10fea97ea6c648d0b9698b84a5` |
| 0546 | `5390d9c3c9e7a76bfbfe97de6806b2aa922aa4e53115dcff11bbe0fe39540ca6` |
| 0548 | `7bf03716c95fc9d9ae06ebb038c69b6e9ed8452f2414919b35cae20365decace` |
| 0550 | `5c686ae8fd82cea995fcdd1ed5bff2d0d688514c45582871cb2b97f231b8b457` |
| 0585 | `9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd` |
| 0606 | `dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e` |

**Lane posts:**

| post | path | sha256 |
|---|---|---|
| Codex1 0032 (GQ_NGC at M_s 96 holds) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0032_2026-10-18_gq91_pass_and_latest_rulings.md` | `3e8c9fc9e65a10791f8ecbda3702556a851391350f06ed013222bd12876ab2f7` |
| Codex1 0056 (the formal K32 result) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0056_2026-10-18_ngc_k32_complete_n_fail_n1_a66_open.md` | `4b67319dddb4799e71420881f6624fdcd1640cd5f560a4adce06cd2030af72aa` |
| Codex1 0058 (the steps 6–7 rehearsal) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0058_2026-10-18_0603_synthetic_steps6_7_finished.md` | `fc5af8318febd8dd86037d7aeddff9a590ea8e436deb15f002b9c4775c65cea2` |
| Codex3 0618 (the step-5 carriers) | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0618_2026-10-18_dispatch0606_carriers_finished.md` | `8939c004e4bea1728eed610e4d98b98dffbe4333be1433c539feb16159de60a7` |

**Root decisions** (`…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00n[_ADDENDUM].md`):

| addendum | entries used | sha256 |
|---|---|---|
| V003 (frozen) | A10, A12 | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` |
| V004 (frozen) | A13, A14, A15, A16, A17, A20, A21, A23, A27, A41, A42 | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| V005 (open; it closes at the V007 freeze, A82) | the entries in the next table | `991cc242e30eeea5118058e0f60862f7f50f1cb2cf434a85d92f4055413848c8` (whole file, read at assembly) |

**V005 cited entries.**
- **Why per-entry pins.** The V005 file is still open, and root keeps adding entries to it. So each cited entry is pinned by the sha256 of its own section: the bytes from its `## A<n>:` heading line up to the next `## ` heading line, or up to the end-marker shown.
- **The checks.** The target-free check (T5) re-extracts these sections from the current bytes. Check T7 lists every heading in the file that is neither cited here nor in the read-with-no-change list.

| entry | used for | ends before | section sha256 |
|---|---|---|---|
| A48 | the governing principle: where the text is silent, the stricter reading | next heading | `526cfceacade31d16dc4f5c7fd023573515898692d4f40d22bfebc9216008ee6` |
| A50 | the PROVISIONAL rule (used by analogy in I-7) | next heading | `981a67c6137edb1a8ce9cf0700280f8eaed93183912e012ec0116af88bf29def` |
| A52 | item 4: LO_NGC is the readout-coupled share; NGC I1-T before any NGC N-test is read | next heading | `70510fa1d1c5efbf55b6f4b24a4983befa2a1661a21e552777799de82b50c935` |
| A56 | the 0531 roster-binding ruling (v003f B1) | next heading | `0e0ef14377f12b3326beb6b1ae0d0ce9c262aeb6fd3c03ce89851a941aa51a47` |
| A60 | gap rows; cut binding; the V001 summary and its open root items | next heading | `42c5870ff48dddd19ddddd70d3705ced8231a42011f5c4455b1fdfa7e50b67b8` |
| A62 | the two-pass freeze procedure | next heading | `1e3bbebc12dffcb7e965fec0f99004d3969513152f25e0e84b193420447b8084` |
| A63 | the stage-0 outcome; the SUPPORTED k = 0 drift reading; R-DRIFT; the disclosure | next heading | `8cbe65538dc03ffe1c7f8c84088ce5e7c05791c9b36471ed7f1f2631330f169f` |
| A64 | the C1′ scope; NGC K_big 32; N3′; coverage 91; N1 on production records | next heading | `9984d5819d5a86b47d18ebe1747364b71abba146421b65d1ab692f551d14d015` |
| A65 | STAGE0_GRID_OUTER; the grid differences and single-chain range; check R-3; the disclosure | `**Lanes.**` | `87e74156706e41e748e427c168c8d0d8635ac18fa44db4b7199091c8ba8fd9d2` |
| A66 | the N1 consequence; TRUNCATION_SHAPE_RESIDUAL; R-TSR | next heading | `3446953179e036f3e77872dc3e192af6e83b18f7c0486df6a4963643c29224c9` |
| A70 | the v003g PASS note ("Step 6's freeze code is ready") | next heading | `f6b6e253b02e0e41c8fd7d142ff0e205152786db35965e11d5c0ed3f9693d5b2` |
| A81 | RI-22, the DOUBLING NGC half; RI-23, the M_s 128 condition, slotting and LO_NGC | next heading | `3829e30c497fcf6b6779379a1eb89070a84a87da31ef35589770f496a906a84e` |
| A82 | V005 closes at the freeze | next heading | `8a45e4a9378e5c51e5d410f007af5040840cbfa7404f52220bb4db37130ddedc` |
| A90 | the formal K32 N-test result (N_FAIL_N1, gate OPEN); LO_NGC_K32_CERT_V001 coverage to 91; the step-5 LO I1-T item | next heading | `b1fce9a94cea5217ad474b5c72a802772bb53ec0ffcabcb44f42b147cec41232` |

**Read with no change to this text:** A47, A49, A51, A53–A55, A57–A59, A61, A67–A69, A71–A80, A83–A89, A91–A96. From V005, V001 cited only the A48 principle and the 0518/A55 log.

**Freeze, slots and nodes** (`/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/`):

| file | sha256 |
|---|---|
| `freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` (`_ladder_row`, `_score_members`, `_band_rows`, `_alternative_score_scope`, `_score_members_on_rows`, `_authorized_row_registration`, REGISTERED_INVALID_REASONS, WITHIN_ERROR_RULE, HEADLINE_RULE, REFERENCE_RULE) | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| `freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` (alternatives; query block; observation rule) | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` |
| `freeze_score_readiness_cx3/v003g/RUNBOOK_V001.md` | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` |
| `ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (the GL4 node radii) | `ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d` |

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

**Claude4's own:**

| file | sha256 |
|---|---|
| `claude_artifacts/miss_reading_prereg_c4/PREREG_MISS_READING_V001.md` | `6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345` |
| `claude_artifacts/review_freeze_v003g_c4/REVIEW_FREEZE_V003G_C4V001.md` | `575f872c00c22a00eb29a97eac7e594562b1e07843354baa110674702c4c68a4` |
