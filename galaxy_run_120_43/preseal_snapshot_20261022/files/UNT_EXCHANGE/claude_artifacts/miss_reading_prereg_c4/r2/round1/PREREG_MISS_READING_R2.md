# PREREG_MISS_READING_R2 — how the 43 NGC3198 rows will be read (UNSEALED DRAFT r2; written before any NGC3198 target is opened)

**Status.**
- Draft r2 for root (dispatch 0585). When root seals it, it supersedes V001 (`6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345`). V001 stays as history.
- Author: Claude4, single author, inline. The independent checks run on this text are listed in `INDEX_R2.md`; they do not change authorship.
- **No NGC3198 target, observed velocity or target-bearing file was opened in writing it.** The only NGC3198 data read are the query ids and radii in the target-free query block of slots V003.
- **It fixes how the score will be read. It changes nothing in the score.** Freeze v003g computes the LADDER rows in root's two-pass freeze:
  - module `48a1e48a…`, PASS in Claude4 0071;
  - runbook RUNBOOK_V001 `9557b5aa…`.

  This document classifies and reads those rows afterwards.
- **Seal.** Root seals this text before any NGC3198 target is opened (A60; 0585), by registering its sha256 in a root entry (root item M-6).
- Each clause carries a tag in square brackets (for example, the tier rule's tag is C-1.1). The tags key the clause source map (`CLAUSE_SOURCE_MAP_R2.md`).

**Binding principles** (A10, A12.3, A15 E3, A20, A23, A41, A48) **[C-P]**:
- Every outcome registers; nothing is prescribed.
- A miss is never reported as a failure of UNT in general. Under A15 E3 an outer-row failure is TESTED-NEGATIVE for exactly the present-mass-only lapse response of the L = 4 coefficient method, at the A2 grid and the calibrated θ.
- **Every reading is conditional on:**
  - the fixed DDO154 distance 4.04 Mpc and inclination 66°, and the NGC3198 registered geometry (13.8 Mpc, 72°), all NOT_EVALUATED_BEFORE_FREEZE (A23);
  - the registered NGC numerics of I-6.
- Where this text is silent, the reading less favourable to any adopted hypothesis is chosen (the A48 governing principle, applied to readings).

## 0. Invariants

- **I-1. The rows [C-I1].**
  - All 43 rows, NGC3198-Q01 to NGC3198-Q43, are classified in manifest order. Q_ids, radii and validity come only from the frozen manifest and the root-pinned rosters.
  - **Denominators.** 43 for the PRIMARY alternative and for every full-row alternative. STAGE0_GRID_OUTER, if evaluated, uses its registered subset Q36–Q43, with denominator 8 (A65; RUNBOOK_V001 step 10).
  - No row is dropped, merged, re-gridded or substituted (0518 item 1).
- **I-2. Quoted values only [C-I2].**
  - The quoted target values v_q and σ_q are used exactly as quoted. No σ is inflated, floored or re-estimated.
  - Nothing in this document is fitted to the targets.
- **I-3. Frozen quantities only [C-I3].** The classification uses only:
  - the frozen reference member's LADDER row for each query. REFERENCE_RULE chooses that member at freeze time, before target access;
  - the frozen PRIMARY pointwise envelope rows (label POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE);
  - the root-pinned row-registration rosters (0531; v003g), which give each INVALID row its registered reason;
  - the query radius R_q, bound by query id to the slots V003 query block, with Rad_unit kpc (v003g fixes F2 and F3);
  - the row-flag record of root item M-7 (TRUNCATION_SHAPE_RESIDUAL);
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

  An alternative never replaces, re-tiers or outvotes the PRIMARY classification.
- **I-5. Headline [C-I5].** The headline stays the freeze module's (v003g HEADLINE_RULE): the distribution of the PRIMARY members' within-error counts, plus the frozen reference member's count. This document adds readings only and never alters the headline.
- **I-6. Numerics conditions [C-I6].** Every reading is conditional on the registered NGC numerics. All of them are fixed before any target is opened, and the report header records each one with its record sha:
  - **K_big.** NGC production K_big = 32 /kpc (A64, after the formal N3 at 16 failed, TESTED), with N3′ = {16, 64} against 32. N1, N2, N4 and NQ are evaluated at 32.
  - **N-test outcome.** It is decided by the registered compare (A66.1): N_PASS, or N_FAIL_N1 confined to TRUNCATION_SHAPE rings (A66.2).
    - A failure of N0, NQ, N2 or N3′, or an N1 failure on a ring that is not TRUNCATION_SHAPE, blocks NGC route A/B (A66.3).
    - Under the 0512 ruling logged in V005, only N_PASS is an input to route A/B. So any other outcome, such as N_INCOMPLETE or N_NO_RUN, also gives no route-A/B run.
    - With no route-A/B run there is no score, and this document is not applied.
  - **Certificates.** EPS_NGC, LO_NGC and GQ_NGC are certified to coverage at least √2·64 ≈ 91 /kpc (A64.2). No NGC N-test is read until all three are slotted (A81 RI-23).
  - **Gas M_s.** The NGC gas M_s is 96, or 128 if GQ_NGC at 96 fails anywhere on [2, 91] (A81 RI-23). At 128, LO_NGC and the DOUBLING NGC half are recomputed. The DOUBLING NGC half's bound is θ/20 (A81 RI-22).
  - **C1 and C1′.** C1′ applies only on NOT_GRID rings. C1 is kept on TRUNCATION_SHAPE and QUADRATURE_LIMITED rings (A64.1).
  - **None of these is chosen, changed or re-run after targets are opened.** No reading attributes a miss to a certified numerical quantity. The only registered numerical reading is R-TSR (§3), which A66 created.
- **I-7. Freeze status [C-I7].**
  - The classification is made on a FREEZE_COMPLETE manifest.
  - If root authorizes scoring a FREEZE_INCOMPLETE manifest, the classification is still made and reported in full. Every pattern and reading then carries the label PROVISIONAL (FREEZE_INCOMPLETE), together with the manifest's `incomplete_reasons` (root item M-8).

## 1. Per-row classification (PRIMARY)

### 1.1 Tier [C-1.1]

Rule M-T applies to the output of `score_after_freeze`. Let:
- ref = `headline.reference_member_id`;
- L_q = the row for query q in the `rows` of the entry in `members` whose `member_id` is ref;
- E_q = the row for q in `pointwise_envelope.rows`.

The tiers are evaluated in this order:

| tier | condition | fields used |
|---|---|---|
| **INVALID_AS_MISS** | `L_q.score_status = INVALID_AS_MISS`. In v003g this holds exactly when the root-pinned roster registers q INVALID with one of the three registered reasons (§4). The row then has tier MISS_WORST_TIER, a null prediction, and its `registered_reason`. | `score_status`, `registered_reason` |
| **HIT** | Not INVALID, and `L_q.within_error = true`: \|r_q\| ≤ 1 with r_q = `L_q.sigma_ratio` = (p_q − v_q)/σ_q (WITHIN_ERROR_RULE). In v003g: score_status HIT, tier WITHIN_ERROR. | `within_error`, `sigma_ratio` |
| **NEAR** | Not INVALID and not HIT, and `E_q.band_overlaps_error_bar = true`: lo_q ≤ v_q + σ_q and hi_q ≥ v_q − σ_q over the frozen PRIMARY pointwise envelope. | `band_overlaps_error_bar` |
| **MISS** | Neither HIT nor NEAR (v003g score_status MISS). | `score_status` |

- **What NEAR means.** Some admitted representative member state reaches the error bar, but the frozen reference member does not.
  - NEAR is reported as "state-band sensitive". It is not counted as a miss in §2.
  - A NEAR row's LADDER tier stays MISS_WORST_TIER. The tiers here are reading tiers only and never change the score (I-5).
- **The sensitivity band.** The box-limited sensitivity band (`sensitivity.rows`) is never used for a tier. It is conditional on trial values and is only reported.
- **Fail-closed.** The classification stops with CLASSIFICATION_INPUT_DEFECT in any of these cases:
  - `L_q.status` is UNEVALUATED_OR_REFUSED. REFERENCE_RULE excludes this, because the reference member is finite on every registered-valid row;
  - a field named here is missing;
  - the ids in that member's `rows` are not Q01 to Q43 in order.

  Root then rules before any reading is reported. The score stands as computed.
- Root item **M-1**: these tiers are proposed definitions.

### 1.2 Sign [C-1.2]

- s_q = sign(r_q), one of −1, 0, +1. **Deficit** (−1): the model is below the quoted value. **Excess** (+1): the model is above it.
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
- **No zone moves after targets.** If the frozen manifest's radii, bound by id, put any row in a different zone, the classification stops with ZONE_TABLE_MISMATCH, and root rules. No zone boundary or membership moves after targets are opened.
- **The rows nearest the cuts** are Q24 and Q25 (9.04 and 10.04 kpc), and Q35 and Q36 (28.16 and 30.08 kpc). This is recorded now so that no row can later be argued into the other zone.
- "Flat" is the registered name of the outer region. It asserts nothing about the observed curve shape.
- Root item **M-2**.

### 1.4 Row flags [C-1.4]

- **NEAR flag:** from §1.1.
- **TRUNCATION_SHAPE_RESIDUAL** (A66.2). This is a disclosure flag, not INVALID.
  - A row carries the flag if and only if the root-pinned flag record of root item M-7 lists it. For each flagged row, the record gives the failing TRUNCATION_SHAPE ring (its ordinal), the ring's radial support, and the measured S/θ.
  - A flagged row is classified by M-T like any other row.
  - **At writing** (A66; Codex1 0031, TESTED), N1 fails strictly at one ring: TRUNCATION_SHAPE ordinal 15, at R = 10.54 kpc, with S/θ = 1.0148 at both K_big 16 and K_big 32.
  - **The formal compare decides** (A66.1). The flag record follows the formal reading, never this paragraph.
  - **No carrier yet.** The flag has no field in v003g or in slots V003 (root item M-7).

## 2. Zone summaries and patterns (algorithmic; every applicable pattern is reported) [C-2]

**Per-zone summaries.** For each zone Z:
- **Counts.** N_v(Z) is the number of non-INVALID rows. H(Z), N(Z) and M(Z) are the HIT, NEAR and MISS counts. I(Z) is the INVALID count, also given per registered reason.
- **m(Z):** the median of r_q over the non-INVALID rows. For an even count it is the mean of the two middle values. It is UNDEFINED when N_v(Z) = 0.
- **Sign class S(Z):** DEFICIT if m(Z) < −1, EXCESS if m(Z) > +1, otherwise CENTERED. It is UNDEFINED when m(Z) is UNDEFINED.
- **Miss-dominated:** N_v(Z) ≥ 1 and M(Z) ≥ N_v(Z)/2.
- **Hit-dominated:** N_v(Z) ≥ 1 and H(Z) ≥ N_v(Z)/2.
- **Clarification (r2).** Any condition that uses an UNDEFINED quantity is false, and it is reported as UNDEFINED.

**Outer trend.**
- Sort the non-INVALID OUTER rows by R_q and split them into a near half and a far half. With an odd count, the middle row goes to the far half.
- Δ_out = median r(far half) − median r(near half). It is UNDEFINED if N_v(OUTER) < 2.
- **GROWING** holds if and only if S(OUTER) = DEFICIT, Δ_out < 0, and m(TRANSITION) > m(OUTER).

**Patterns.** Each pattern is evaluated independently, and every one that holds is reported. There is no first-applicable selection, so no pattern can mask another.

| id | pattern | condition |
|---|---|---|
| P0 | INVALID rows | I(Z) > 0 in any zone; reported per zone and per registered reason (§4) |
| P1 | OUTER_DEFICIT | OUTER miss-dominated and S(OUTER) = DEFICIT; flag **P1g** if GROWING |
| P2 | OUTER_EXCESS | OUTER miss-dominated and S(OUTER) = EXCESS |
| P3 | INNER_EXCESS | INNER miss-dominated and S(INNER) = EXCESS |
| P4 | INNER_DEFICIT | INNER miss-dominated and S(INNER) = DEFICIT |
| P5 | TRANSITION_ONSET | INNER hit-dominated, OUTER miss-dominated, N_v(TRANSITION) ≥ 1, and TRANSITION not hit-dominated |
| P6 | GLOBAL_OFFSET | S(INNER) = S(TRANSITION) = S(OUTER) ≠ CENTERED, with N_v ≥ 1 in each zone |
| P7 | SCATTERED | at least one MISS, and no zone miss-dominated |
| P8 | NO_MISS | M = 0 over all non-INVALID rows |
| P9 | OUTER_UNTESTABLE | N_v(OUTER) = 0: every OUTER row is INVALID |
| P10 | TSR_MISS | at least one MISS row carries TRUNCATION_SHAPE_RESIDUAL; reported with the tier of every flagged row, hits included |

Also reported for each zone: the counts, m(Z), S(Z), the NEAR rows, and the individual rows.

## 3. Readings, deciding tests, and what counts for and against [C-3]

**Rules for every reading:**
- **No support from the score alone.** The 43-row score can make a reading **consistent** or **inconsistent**. It can never make it **supported**. Support comes only from that reading's own deciding test, run under its own pre-registration.
- **Untested readings stay open.** A reading whose deciding test has not run stays OPEN, whatever the score shows.
- **Fixed list.** The readings below are the registered list. Any reading proposed after targets are opened is labelled **EXPLORATORY (post-score)** and never counts as registered.
- **Scope (r2).** A reading may cite only rows inside its own scope:
  - R-TSR cites only flagged rows;
  - R-DRIFT cites only OUTER rows;
  - no reading cites an INVALID row (§4).

**Deciding tests and their status at writing [C-3.1]:**

| id | deciding test | status |
|---|---|---|
| DT-UT1 | The UT-1 spec-compliant model version: k = 0 a declared zero mode; k → 0⁺ from k ≠ 0 nodes only, under one pre-registered continuation rule; recomputed end to end (A41). | **NOT SCHEDULED**: 0521 withdrawn by 0524 |
| DT-BHD | BH-D derivation from the owned parent, then out-of-sample tests (TDGs, Leo Ring, DF2/DF4) once BH-D exists (A10). | **NOT SCHEDULED**: 0519 withdrawn by 0524 |
| DT-U12 | Small-k limits at larger L and with mixed sampling: U1, U2 and the P-96 capture (A20, A41). | **NOT SCHEDULED**. U2 (0523) was withdrawn by 0524. Stage 0, the L = 4 control, is complete: S0-FAIL-RHAT, TESTED-NEGATIVE as sealed, with wiring WIRING_CHAIN_SPECIFIC (A63). P-96 at L ≥ 6 needs a root decision, which is not pursued during the galaxy run (A63, per the principal). |
| DT-T1a | BH-T1a: the residual against the target-free stellar fraction f★ (PRIMARY enclosed, SECONDARY local; M/L 0.4 and 0.6 variants). Diagnostic, never headline; runs only after a verified freeze (A10, A16.3). | registered |
| DT-GEO | The geometry box (D 12.545–15.18 Mpc, i 69–75°). | NOT_EVALUATED_BEFORE_FREEZE (A16.1); the forward refuses with GEOMETRY_NOT_EXPOSED |
| DT-ALT | The alternatives, scored separately (§6). ORIGINAL_K is evaluated. ML_3p6_0.4, ML_3p6_0.6 and GL10_SOURCE_GAUSS_ORDER are NOT_EVALUATED_BEFORE_FREEZE (A16.2; 0518 item 5). | as stated |
| DT-NAX | Non-axisymmetric finite-flow sensitivity of the m = 0 approximation (plan D3). | not run |
| DT-S1 | Calibration transfer across parameter space (V005 S1). | UNTESTED |
| **DT-S0G** | **STAGE0_GRID_OUTER** (A65.2): the NGC route-A/B prediction at the headline admitted DDO154 calibration point(s), with the coefficient grid swapped from A2 (`2e3a36d8…`) to the stage-0 pooled grid (`bdb9016c…`). Everything else is identical. It is a coefficient-grid sensitivity at fixed calibrated parameters, not a recalibration. Read by §6.3. | NOT_EVALUATED_BEFORE_FREEZE in slots V003. It is evaluated only if its runs finish before the freeze and root adopts an evaluated slots/module successor (A65.2; Claude4 0071 N2). |
| **DT-TSR** | A kept-cube corner-shape variation that removes the residual on the flagged rows. No such test is registered. | **NOT SCHEDULED** |

**Readings by pattern [C-3.2]:**

| pattern | registered readings | consistent with the reading if | against the reading | deciding test |
|---|---|---|---|---|
| **P1 / P1g** (expected: A15 E2, A41) | **R-MF:** failure of the present-mass-only lapse response of the L = 4 coefficient method at the A2 grid and calibrated θ (A15 E3). If P1 holds, this is TESTED-NEGATIVE for exactly this scope. | P1 holds | no P1 with N_v(OUTER) ≥ 1 | the score itself, for this scope only |
| | **R-UT1:** the static isothermal typing of the k = 0 block (A20 reading 1; counted CA-34/CA-28, A41). | P1 holds | A41 item 3 (FORMAL + TESTED) already registers that no gate-consistent typing gives an attractive tail, and the spec-compliant T(0⁺) is finite and repulsive on current estimates. Also against: a DT-UT1 run that leaves the deficit. | DT-UT1 |
| | **R-HIST:** a missing Bind-history or collective component (A10 SA-BH-01, DECLARED-PREMISE; A20 reading 2; BH-D). | P1 holds. P1g makes it more specific ("missing long-range component", 0522). | DT-BHD gives no outer change, or a derived weighting fails out of sample | DT-BHD |
| | **R-REACH:** magnitudes, k = 0-block drift or finite-size effects at larger L or with mixing (A20 narrowed: these cannot create a 1/r tail). | P1 holds | DT-U12 leaves the outer magnitudes unchanged | DT-U12 |
| | **R-DRIFT** (new, A63/A65): A2's k = 0 entry, which enters the k → 0⁺ transfer under CA-34, is drift-inflated. The registered k = 0 lapse drift reading is SUPPORTED (A63), but its causal gloss "drift inflated A2" is UNTESTED (A65 check R-3). | OUTER miss-dominated (P1, P1g or P2) | the DT-S0G comparison reads AGAINST (§6.3) | DT-S0G; it can make R-DRIFT consistent or inconsistent, never supported (§6.3) |
| **P2** (contrary to E2) | **R-MF**, with the opposite sign: overshoot. **R-S1:** calibration transfer of G_eff = G·Q∞ (A21; S1 UNTESTED). **R-GRID:** k-grid fidelity at outer radii (A17: C3 is the criterion that matters). **R-DRIFT**, as above. | P2 holds | ORIGINAL_K shows the same excess (against R-GRID). DT-S1 shows a consistent transfer (against R-S1). DT-S0G reads AGAINST (against R-DRIFT). | DT-S1, DT-ALT, the A17 C3 record, DT-S0G |
| **P3 / P4** | **R-GEFF:** the single DDO154 short-wavelength G_eff does not carry over to a galaxy with stellar share about 0.51 (DDO154: about 0.03) (A21, E1). **R-ML:** stellar M/L (0.5, counted ±20%; A10). **R-SPEC:** a species or history weight (SA-BH-01). **R-GEO:** geometry (A23). **R-NAX:** the m = 0 projection (A17 note; D3). | P3/P4 holds | **R-ML:** the DT-T1a M/L variants do not move the inner rows by the miss. **R-GEO:** DT-GEO is not evaluated, so this reading stays OPEN by construction. | DT-T1a, DT-ALT (M/L), DT-GEO, DT-NAX |
| **P5** | The onset of the finite-reach deficit (as P1, including R-DRIFT for the OUTER rows), or local structure in the transition zone. | P5 holds | An onset radius inconsistent with k* (A12: wavelengths of tens of kpc) is reported, as a comparison only. | as P1; DT-NAX |
| **P6** | **R-S1** (G_eff scale); **R-GEO** (distance scale); **R-MF**. | P6 holds | DT-S1 consistent; a DT-GEO evaluation removing the offset (not available before the freeze) | DT-S1, DT-GEO |
| **P7** | Row-level systematics: non-circular motion and the m = 0 projection (R-NAX); otherwise R-MF at row level. | P7 holds | — | DT-NAX |
| **P8** | No miss reading. If N_v(OUTER) ≥ 1, it runs **against** the A15 E2 / A41 expectation and is reported as such. | — | — | P8 triggers a mandatory check that ORIGINAL_K and the A17 C3 grid record agree. Agreement is reported; it does not change the headline. |
| **P9** | The outer test is unavailable (every OUTER row INVALID); E2 reads NOT_TESTABLE. R-DRIFT stays OPEN, because DT-S0G is uninformative when every OUTER row is INVALID. | — | — | the outer-gas confinement question (A12.5), not a rotation-row test |
| **P10** (new, A66) | **R-TSR:** a miss on a TRUNCATION_SHAPE_RESIDUAL row may reflect the residual cube-corner anisotropy of the kept cube (K = 2) (A66.2). | P10 holds, for the flagged MISS rows only | Route B consumes the azimuthal mean, so the φ-spread S enters no row directly (A66.2; A42 TESTED). R-TSR is therefore registered as an open possibility, not an expected cause. Misses on unflagged rows are outside its scope. | DT-TSR (NOT SCHEDULED): R-TSR stays OPEN |

**BH-T1a is used as registered, diagnostic only [C-3.3].**
- The rank correlation and slope of r_q against f★(R) bear jointly on M/L and on a species or history weight.
- They are not a verdict on Bind history alone (A10).
- A trend is reported under R-ML and R-SPEC together, never under one of them alone.

## 4. INVALID-as-miss rows [C-4]

**The INVALID set** is exactly the set of rows the root-pinned roster registers INVALID (0531, ruled in A56: the v003f B1 closure; v003g). Each row carries one of two kinds of reason:
- one of the three built-in reasons, the v003g REGISTERED_INVALID_REASONS, which derive only from their own rules;
- or the reason of a root-listed gate.

| reason | rows | source |
|---|---|---|
| QUERY_INSIDE_INNERMOST_NODE | primary GL4, slots V002/V003: Q01, Q02 | root decisions V001 N1 and V002 A4; slots `invalid_primary_GL4` |
| QUERY_BEYOND_OUTER_GAS_CUT | the outer-gas cut rows: {R_q ≥ first_unconfined_R} from the pinned v011 cut record | A12.5, A14 C3; the A60 cut binding |
| QUERY_OUTSIDE_RETAINED_SUPPORT | the gap rows: queries between the last retained route-B node and the pinned outer cut | A60, gap rows |
| a root-listed gate's own reason | the query ids the gate document lists | 0518 item 2 ("any row a registered gate invalidates"); v003g `root_gates` |

**How rows get onto the roster:**
- **A root-listed gate** registers rows INVALID only through a pinned gate document. The document must have schema INVALID_GATE_SCHEMA and registration_status REGISTERED, and must list its own `registered_reasons` and `query_ids`.
  - A gate may not use a built-in reason. v003g refuses it with ROOT_ROSTER_BUILTIN_REASON_MUST_DERIVE_FROM_RULE.
  - v003g invents no rule of its own.
- Root registers the roster during the two-pass freeze, before any target access (RUNBOOK_V001 steps 1–8; 0545 F5; ruled in A62):
  1. the first pass saves the raw results and the v011 cut records;
  2. root registers the rosters;
  3. the second pass replays exactly.

**Integrity (v003f/v003g).** A finite value on a roster-INVALID row refuses. An unrostered INVALID refuses. Reasons and gates come from the roster only (0531). So `score_status = INVALID_AS_MISS` can be taken as the roster's statement.

**Scoring.** INVALID rows are scored as worst-tier misses and counted in the 43 (0518 items 1–2). D1 is applied over the registered-valid rows only (0518 item 3).

**Reporting.** INVALID rows are listed separately, per reason, with each row's zone.

**No part in the readings:**
- INVALID rows are excluded from N_v(Z), from m(Z), and from every pattern except P0 and P9. Every INVALID OUTER row counts toward P9.
- The only statement made about an INVALID row is its roster reason. No reading cites an INVALID row as evidence for or against anything.
- No roster change is allowed after targets are opened. Any later root ruling on a roster row is recorded as post-score and does not change this classification.

## 5. Comparison with the A15 expectations (after the score; labelled COMPARISON, never a fit)

**E1, inner disc [C-5.1].** Two parts:
- **(a) The deciding observable A15 E1 names:** the inner rows against their bands. Report H(INNER), N(INNER) and M(INNER). As a sub-table, report the rows Q03–Q15, which A15 E1 names "or so". Label: "COMPARISON with A15 E1".
- **(b) The expectation itself:** whether the frozen model rotation exceeds the frozen baryonic-Newtonian rotation at the INNER rows.
  - Both are model quantities, and the comparison involves no target.
  - It is made only from a target-free carrier pinned before the freeze (root item M-11). v003g has no such field. Without a carrier, part (b) reads NOT_AVAILABLE.
  - It is never computed after targets are opened. No baryon column of the observational data table is ever used.

**E2, outer disc [C-5.2].**
- Report P1/P1g/P2/P8/P9 for OUTER, with the OUTER INVALID counts per reason. A15 E2 foresaw outer rows becoming INVALID through route-A outer-gas unconfinement.
- Label: "COMPARISON with A15 E2".

**E3 [C-5.3].** E3 is the reading rule, applied through §3. It is reported as "applied", with no comparison number attached.

**Never an adjustment [C-5.4].** No expectation is adjusted, and no row is re-read, to improve agreement.

## 6. Alternatives (scored separately; never the headline)

### 6.1 Evaluated non-PRIMARY alternatives: the twin rule [C-6.1]

v003g scores an alternative's members, but it selects no reference member and band-scores no alternative envelope. So:
- **The twin.** An alternative's twin is its member with the same `log_index` as the frozen PRIMARY reference member.
- **Classification.** The twin's rows are classified INVALID_AS_MISS, HIT or MISS by M-T, with no NEAR tier.
- **No twin.** If there is no twin, or the twin is not valid, the alternative reads NO_TWIN. Only its scored member distribution is then reported.
- **Summaries and patterns** for an alternative use the same rules (§2, with N(Z) = 0) and are reported under its name.
- **Limits on use.** They never trigger, confirm or refute a PRIMARY reading. The only exceptions are the R-GRID and P8 entries of §3, which name ORIGINAL_K, and §6.3 for STAGE0_GRID_OUTER and R-DRIFT.
- Root item **M-10**.

### 6.2 Alternatives not evaluated before the freeze [C-6.2]

Only the status is reported: "NOT_EVALUATED_BEFORE_FREEZE: sensitivity only, never scored as the headline". This applies to ML_3p6_0.4, ML_3p6_0.6, GL10_SOURCE_GAUSS_ORDER, and STAGE0_GRID_OUTER unless it is evaluated.

### 6.3 STAGE0_GRID_OUTER [C-6.3]

**At writing:** NOT_EVALUATED_BEFORE_FREEZE; headline false; scope OUTER Q36–Q43 (R ≥ 30 kpc, inclusive); grid `bdb9016c…`.

**If it stays NOT_EVALUATED.** The report says "STAGE0_GRID_OUTER: NOT_EVALUATED_BEFORE_FREEZE (A65.2)", and R-DRIFT stays OPEN.

**If it is evaluated** (only through a successor adopted before the freeze):
- It is scored on its 8 rows, denominator 8, separately from the headline.
- It is labelled "SENSITIVITY: coefficient-grid sensitivity at fixed calibrated parameters (A65), not a recalibration".
- It never enters the headline, and never re-tiers a PRIMARY row (A65.1).

**Comparison rule** (registered here; root item M-9). Restrict to the OUTER rows that are not INVALID under the PRIMARY reference member, and not INVALID under the STAGE0 twin (§6.1). On those rows:
- H_P is the number of PRIMARY reference-member HIT rows.
- H_S is the number of twin HIT rows.
- S_P and S_S are the sign classes, with the §2 rule, of the two members' r_q.

The comparison then reads:
- **CONSISTENT** with R-DRIFT if H_S > H_P.
- **AGAINST** R-DRIFT, as an explanation of the outer misses at fixed calibrated parameters, if H_S ≤ H_P and S_S = S_P.
- **NOT_DECIDED** otherwise, including when no OUTER row is valid under both.

**Limits:**
- The comparison never reads SUPPORTED. The stage-0 grid failed its R-hat criterion (S0-FAIL-RHAT), and A65 check R-3 leaves the causal gloss UNTESTED.
- Row by row, the report also gives r_q under both members, and the STAGE0 member within-error distribution.

## 7. Disclosures required by A63, A65.4 and A66 [C-7]

**D-1. The stage-0 outcome** (A63; A65.4):
- **Outcome.** S0-FAIL-RHAT, TESTED-NEGATIVE as sealed. Analysis v003 completed 8/8. The maximum R-hat is 1.48, and 95 of 778 columns have R-hat above 1.1. The wiring reads WIRING_CHAIN_SPECIFIC.
- **The k = 0 lapse drift reading is SUPPORTED.** Its precondition holds: census/U is flat in all 8 processes. Stage-0 \|h_NN(0)\| is 1.90 ± 0.11, against A2's 3.551, which is below A2 − 2 SE.
- **Its causal gloss, "drift inflated A2", is UNTESTED.** Stage 0 differs from the same-kernel BIRTHK about as much (relative distance 0.451) (A65 check R-3).

**D-2. The coefficient-grid difference** (A65):
- **Distance from A2.** The stage-0 pooled grid (`bdb9016c…`) differs from A2 (`2e3a36d8…`) by relative distance 0.477 globally and 0.483 at the k = 0 node. 93.6% of its entries lie more than 2 band-SE from A2.
- **h_NN(0).** It is −1.899 ± 0.106 against −3.551, a gap of 15.6 SE.
- **A2 stays the headline grid.**
- **A counted uncertainty.** A65.4 makes D-1 and D-2 together a counted coefficient-grid uncertainty for every row.
  - The report states it in its header and in every row's notes.
  - It is not converted into a number. It does not widen σ_q (I-2), and it changes no tier.

**D-3. The N1 residual** (A66):
- **Where N1 fails.** N1 fails strictly at one ring: TRUNCATION_SHAPE ordinal 15, R = 10.54 kpc, S/θ 1.0148 at K_big 16 and at 32.
- **Why.** The residual comes from the kept-cube (K = 2) corner shape, not from the tail. The other TRUNCATION_SHAPE rings pass. Without the tail, these rings were at 1.1–3.7 θ (A14 C4 / A17).
- **When it was ruled.** The A66 consequence was ruled after the N1 diagnostic had been seen, and A66 labels it so. R-TSR is registered after that diagnostic and before any target is opened.

**D-4. The NGC numerics:** the values of I-6, together with the gas M_s actually used and the certificate record shas. They are filled at score time from the slotted records.

## 8. Report format (score step) [C-8]

The report gives:
1. **The header:**
   - the sealed sha of this text;
   - the freeze manifest sha, the registration sha, and the expected manifest sha logged at the freeze;
   - the slots, module, roster and flag-record shas;
   - the I-6 values, with their record shas;
   - the freeze status (I-7);
   - disclosures D-1 to D-4.
2. **The per-row table:** Q_id, zone, R_q, tier, r_q, sign, NEAR flag, TRUNCATION_SHAPE_RESIDUAL flag with its S/θ, and INVALID reason.
3. **The zone summaries.**
4. **Every pattern that holds.**
5. **For each pattern,** its registered readings, each with the status consistent, inconsistent or OPEN, plus each deciding test's status.
6. **The INVALID list,** per reason.
7. **The A15 comparisons** (§5).
8. **The alternatives** (§6), with STAGE0_GRID_OUTER last, labelled SENSITIVITY.
9. **Any EXPLORATORY (post-score) readings,** labelled as such.

**The words used:**
- "TESTED-NEGATIVE" only for R-MF, within its stated scope;
- "consistent with", never written as "supports";
- "SUPPORTED" only when quoting the sealed k = 0 drift reading of A63.

## 9. Self-check: could any rule be steered by the outcome? [C-9]

| risk | how it is closed here |
|---|---|
| Moving the zone boundaries or memberships to put misses inside or outside a zone | The cuts are numbers fixed in §1.3, and membership is fixed by query id. A mismatch stops the classification. |
| Redefining HIT or NEAR after seeing residuals | The tiers use only frozen LADDER fields and the quoted σ (§1.1). No tolerance is a free parameter. |
| Choosing which member is scored | The frozen reference member, plus the frozen PRIMARY envelope. Alternatives use the twin rule (§6.1). |
| Choosing which pattern to report | Every applicable pattern is reported (§2); none masks another. Undefined quantities make conditions false (§2). |
| Upgrading "consistent" to "supported" | Prohibited (§3). DT-S0G never reads SUPPORTED (§6.3). |
| Re-explaining INVALID rows to rescue or condemn a reading | Prohibited (§4). |
| Adding a favourable reading after the fact | It is labelled EXPLORATORY and is never registered (§3). |
| Dropping rows or inflating σ | Prohibited (I-1, I-2). The grid uncertainty does not widen σ (D-2). |
| Reading the withdrawn or deferred deciding tests as done | They are NOT SCHEDULED, and their readings stay OPEN (§3). |
| Evaluating STAGE0_GRID_OUTER only if it helps | It is evaluated only before the freeze, or it reads NOT_EVALUATED_BEFORE_FREEZE (A65.2). The comparison rule is fixed here (§6.3). |
| Using the stage-0 grid to rescue the headline | It is never the headline and never re-tiers a PRIMARY row (A65.1; §6.3). |
| Flagging rows TRUNCATION_SHAPE_RESIDUAL after seeing misses | The flag record is root-pinned and target-free before the freeze (M-7). R-TSR may cite only flagged rows, and it stays OPEN. |
| Choosing K_big, M_s or certificates after targets | All are fixed before step 5 (A64; A81 RI-23). The header records them (I-6). |
| Scoring an incomplete freeze quietly | The PROVISIONAL label applies (I-7). |
| **Residual risk (not closed).** The thresholds "miss-dominated ≥ half", S(Z) at \|m\| > 1 and the half-split trend rule are choices made here. | They are fixed now, before targets. Root may change them only before the seal (M-3). |
| **Residual risk (not closed).** NEAR depends on the width of the frozen envelope band, which depends on the member-selection rule. | That rule is frozen with the manifest, so NEAR cannot be steered after targets. A wide band could hide misses as NEAR, which is why NEAR rows are reported individually. |
| **Residual risk (not closed).** The definition of a ring's radial support decides which rows are flagged. | Root fixes it before the seal (M-7). |
| **Residual risk (not closed).** The DT-S0G comparison uses choices made here: a strict count increase, and the same sign class. | They are fixed before the seal (M-9). |

## 10. Root items for this prereg (decide before the seal) [C-10]

Each item's recommended ruling, with its reasoning, is in `ROOT_ITEMS_R2.md`. Items M-1 to M-5 are V001's five pending items; M-6 to M-12 are new in r2.

| item | subject |
|---|---|
| M-1 | Tiers (§1.1) |
| M-2 | Zone cuts and the membership table (§1.3) |
| M-3 | Pattern thresholds and the r2 clarifications (§2) |
| M-4 | Deciding tests NOT SCHEDULED, and the readings that stay OPEN (§3) |
| M-5 | Score inputs and field names (v003g) |
| M-6 | The seal vehicle, cited entries and later entries |
| M-7 | A carrier for the TRUNCATION_SHAPE_RESIDUAL flag, and the definition of radial support |
| M-8 | Scoring a FREEZE_INCOMPLETE manifest |
| M-9 | The DT-S0G comparison rule |
| M-10 | Alternative classification: the twin rule, without NEAR |
| M-11 | The A15 E1(b) baryonic-Newtonian carrier |
| M-12 | A mechanical, sealed classifier for the score step |

## 11. Sources (sha256 from bytes at writing) [C-11]

**Dispatches** (`/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/`):

| item | sha256 |
|---|---|
| 0518 | `0748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279` |
| 0522 | `30af5d6811788e9bbed4c470dae0ea9bb4ae5230a734fa7940e942b30ed66160` |
| 0524 | `d1430abc84025cc4afde31f3fd4fce1845e8d2334e47e95fbeb81936d7dfd4df` |
| 0531 | `7233faf3be6d498a662f9f3dcc743c12420bbc6fa997e606aeb72e7d16ca3cd6` |
| 0535 | `e4bf99106e2d4eae00e2be0ed1b596b0450225bfffe2ac717386f0c13db22f54` |
| 0545 | `4049a3f81b524f5622e0eda6510eeee60c7a6b10fea97ea6c648d0b9698b84a5` |
| 0546 | `5390d9c3c9e7a76bfbfe97de6806b2aa922aa4e53115dcff11bbe0fe39540ca6` |
| 0548 | `7bf03716c95fc9d9ae06ebb038c69b6e9ed8452f2414919b35cae20365decace` |
| 0585 | `9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd` |

**Root decisions** (`…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00n[_ADDENDUM].md`):

| addendum | entries used | sha256 |
|---|---|---|
| V003 (frozen) | A10, A12 | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` |
| V004 (frozen) | A14, A15, A16, A17, A20, A21, A23, A41 | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| V005 (open; it closes at the V007 freeze, A82) | the entries in the next table | `17cb4fd496845823227562682341eb605304d0ec14842d3e26369215e49d538b` (whole file, read at assembly) |

**V005 cited entries.** The V005 file is still open, and root keeps adding entries to it. So each cited entry is pinned by the sha256 of its own section: the bytes from its `## A<n>:` heading line up to the next `## ` heading line, or to the end of the file. The target-free check (T5) re-extracts these sections from the current bytes.

| entry | used for | section sha256 |
|---|---|---|
| A48 | the governing principle: where the text is silent, the stricter reading | `526cfceacade31d16dc4f5c7fd023573515898692d4f40d22bfebc9216008ee6` |
| A56 | the 0531 roster-binding ruling (v003f B1) | `0e0ef14377f12b3326beb6b1ae0d0ce9c262aeb6fd3c03ce89851a941aa51a47` |
| A60 | gap rows; cut binding; the V001 summary and its open root items | `42c5870ff48dddd19ddddd70d3705ced8231a42011f5c4455b1fdfa7e50b67b8` |
| A62 | the two-pass freeze procedure | `1e3bbebc12dffcb7e965fec0f99004d3969513152f25e0e84b193420447b8084` |
| A63 | the stage-0 outcome; the SUPPORTED k = 0 drift reading; R-DRIFT; the disclosure | `8cbe65538dc03ffe1c7f8c84088ce5e7c05791c9b36471ed7f1f2631330f169f` |
| A64 | the C1′ scope; NGC K_big 32; N3′; coverage 91 | `9984d5819d5a86b47d18ebe1747364b71abba146421b65d1ab692f551d14d015` |
| A65 | STAGE0_GRID_OUTER; the grid differences; check R-3; the disclosure (its trailing block also logs the 0518 contract) | `290eac4af1f43d01c2c66a5c5981d0f43d73a7a9bf06388821d5ffd2f6a24e9c` |
| A66 | the N1 consequence; TRUNCATION_SHAPE_RESIDUAL; R-TSR | `3446953179e036f3e77872dc3e192af6e83b18f7c0486df6a4963643c29224c9` |
| A70 | the v003g PASS note ("Step 6's freeze code is ready") | `f6b6e253b02e0e41c8fd7d142ff0e205152786db35965e11d5c0ed3f9693d5b2` |
| A81 | RI-22, the DOUBLING NGC half; RI-23, the M_s 128 condition, slotting and LO_NGC | `3829e30c497fcf6b6779379a1eb89070a84a87da31ef35589770f496a906a84e` |
| A82 | V005 closes at the freeze | `8a45e4a9378e5c51e5d410f007af5040840cbfa7404f52220bb4db37130ddedc` |

The following entries were read with no change to this text: A61, A67–A69, A71–A80 and A83–A89. Every other V005 entry predates V001 and was used there through V001's citations.

**Freeze and slots** (`/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/`):

| file | sha256 |
|---|---|
| `prediction_freeze_c2v003g_cx3v001.py` (`_ladder_row`, `_score_members`, `_band_rows`, `_alternative_score_scope`, `_score_members_on_rows`, REGISTERED_INVALID_REASONS, WITHIN_ERROR_RULE, HEADLINE_RULE, REFERENCE_RULE) | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| `slots/NGC3198_FREEZE_SLOTS_CX3V003.json` (alternatives; query block) | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` |
| `RUNBOOK_V001.md` | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` |

**Target-free query manifest** (the source the slots cite): `…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json`, `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494`.

**Coefficient grids:**

| grid | path | sha256 |
|---|---|---|
| A2 (headline) | `…/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz` | `2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7` |
| stage-0 pooled (STAGE0_GRID_OUTER) | `claude_artifacts/stage0_grid_gate_c2/candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz` | `bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5` |

**Claude4's own:**

| file | sha256 |
|---|---|
| `claude_artifacts/miss_reading_prereg_c4/PREREG_MISS_READING_V001.md` | `6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345` |
| `claude_artifacts/review_freeze_v003g_c4/REVIEW_FREEZE_V003G_C4V001.md` | `575f872c00c22a00eb29a97eac7e594562b1e07843354baa110674702c4c68a4` |
