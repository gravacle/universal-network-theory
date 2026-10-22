# PREREG_MISS_READING_V001 — how the 43 NGC3198 rows will be read (UNSEALED; written before any target is opened)

**Status.** Draft for root.
- Root seals it before the score step opens the targets.
- Written by Claude4 (dispatch 0522), single author, inline.
- **No NGC3198 target, observed velocity or target-bearing file was opened** in writing it.
- **It fixes how the score will be read. It changes nothing in the score itself.** The freeze/score pipeline (v003d → v003e → v003f, under review) computes the LADDER rows. This document classifies and reads them afterwards.

**Binding principles** (A10, A12.3, A15 E3, A20, A23, A41):
- Every outcome registers; nothing is prescribed.
- A miss is never reported as a failure of UNT in general.
- Every reading is conditional on the fixed DDO154 distance 4.04 Mpc and inclination 66°, and on the NGC3198 registered geometry (13.8 Mpc, 72°), all NOT_EVALUATED_BEFORE_FREEZE (A23).
- Where this text is silent, the reading less favourable to any adopted hypothesis is chosen (A48 governing principle, applied to readings).

## 0. Invariants

- **I-1. The rows.**
  - All 43 rows are classified, in manifest order.
  - Q_ids, radii and validity come from the frozen manifest only.
  - The denominator is always 43.
  - No row is dropped, merged, re-gridded or substituted (0518 item 1).
- **I-2. Quoted values only.**
  - Target values v_q and quoted σ_q are used exactly as quoted. No σ is inflated, floored or re-estimated.
  - Nothing in this document is fitted to the targets.
- **I-3. Frozen quantities only.** The classification uses only what is frozen before target access:
  - the frozen reference member's prediction p_q;
  - the frozen pointwise envelope band [lo_q, hi_q] over the admitted representative members of the PRIMARY alternative;
  - the root-pinned row-registration roster (0531, v003f), plus the frozen query radius R_q at the registered geometry;
  - the target pair (v_q, σ_q).
- **I-4. Alternatives.** ORIGINAL_K is EVALUATED_BEFORE_FREEZE (A16.2). GL10 and the M/L variants are NOT_EVALUATED_BEFORE_FREEZE (0518 item 5; A16). Alternatives are classified the same way, but separately; they never replace the PRIMARY classification.
- **I-5. Headline.** The headline stays the freeze module's (D5): the distribution of PRIMARY member within-error counts plus the frozen reference member. This document adds readings only. It never alters the headline.

## 1. Per-row classification

### 1.1 Tier

Rule M-T, evaluated in this order:

| tier | condition | LADDER fields used |
|---|---|---|
| **INVALID_AS_MISS** | The row is on the root-pinned roster as INVALID: slots V002 GL4 Q01/Q02, the outer-gas cut rows of A12.5/A14 C3, or a root-listed gate. | `score_status = INVALID_AS_MISS` |
| **HIT** | Not INVALID, and the frozen reference member is within error: \|r_q\| ≤ 1, with r_q = (p_q − v_q)/σ_q. | `within_error` (WITHIN_ERROR_RULE) |
| **NEAR** | Not HIT, and the frozen PRIMARY envelope band overlaps the error bar: lo_q ≤ v_q + σ_q and hi_q ≥ v_q − σ_q. | `band_overlaps_error_bar` (`_band_rows`) |
| **MISS** | Neither HIT nor NEAR. | — |

- **NEAR means** that some admitted representative member state reaches the error bar, but the frozen reference member does not.
- **NEAR is reported as "state-band sensitive"** and is not counted as a miss in §2.
- **Root item M-1:** the registered score has no hit/near/miss tiers. These are proposed definitions; see §8.

### 1.2 Sign

- s_q = sign(r_q). A **deficit** (s_q = −1) means the model is below the observed value; an **excess** (s_q = +1) means it is above.
- INVALID rows carry no sign.

### 1.3 Zone

The zone comes from the frozen query radius R_q (kpc, at D = 13.8 Mpc), never from residuals:

| zone | rule | registered basis |
|---|---|---|
| **INNER** (inner disc) | R_q < 10.0 kpc | A15 E1: "R ≲ 10 kpc" |
| **TRANSITION** | 10.0 ≤ R_q < 30.0 kpc | between the A15 E1 and E2 radii |
| **OUTER** (outer flat region) | R_q ≥ 30.0 kpc | A15 E2: "the outermost query rows (about 30–44.08 kpc)" |

- The cuts are fixed here as numbers. No zone boundary may move after targets are opened.
- "Flat" is the registered name of the region. It asserts nothing about the observed curve shape.
- **Root item M-2:** the cuts are proposed; see §8.

## 2. Zone summaries and patterns (algorithmic; all applicable patterns are reported)

**Per-zone summaries.** For each zone Z:
- N_v(Z): the number of non-INVALID rows;
- H(Z), N(Z), M(Z): the HIT, NEAR and MISS counts;
- I(Z): the INVALID count;
- m(Z): the median of r_q over the non-INVALID rows;
- the sign class S(Z): **DEFICIT** if m(Z) < −1, **EXCESS** if m(Z) > +1, otherwise **CENTERED**;
- **miss-dominated:** N_v(Z) ≥ 1 and M(Z) ≥ N_v(Z)/2;
- **hit-dominated:** N_v(Z) ≥ 1 and H(Z) ≥ N_v(Z)/2.

**Outer trend.**
- Sort the non-INVALID OUTER rows by R_q. Split them into a near half and a far half; with an odd count, the middle row goes to the far half.
- Δ_out = median r(far half) − median r(near half). It is undefined if N_v(OUTER) < 2.
- **GROWING** holds iff S(OUTER) = DEFICIT, Δ_out < 0 and m(TRANSITION) > m(OUTER).

**Patterns.** Each is evaluated independently, and every pattern that holds is reported. There is no first-applicable selection, so no pattern can mask another.

| id | pattern | condition |
|---|---|---|
| P0 | INVALID rows | I(Z) > 0 in any zone (reported per §4) |
| P1 | OUTER_DEFICIT | OUTER miss-dominated and S(OUTER) = DEFICIT; flag **P1g** if GROWING |
| P2 | OUTER_EXCESS | OUTER miss-dominated and S(OUTER) = EXCESS |
| P3 | INNER_EXCESS | INNER miss-dominated and S(INNER) = EXCESS |
| P4 | INNER_DEFICIT | INNER miss-dominated and S(INNER) = DEFICIT |
| P5 | TRANSITION_ONSET | INNER hit-dominated, OUTER miss-dominated, and TRANSITION not hit-dominated |
| P6 | GLOBAL_OFFSET | S(INNER) = S(TRANSITION) = S(OUTER) ≠ CENTERED, each zone with N_v ≥ 1 |
| P7 | SCATTERED | at least one MISS, and no zone miss-dominated |
| P8 | NO_MISS | M = 0 over all non-INVALID rows |
| P9 | OUTER_UNTESTABLE | N_v(OUTER) = 0, i.e. every OUTER row is INVALID |

Also reported for each zone: the counts, m(Z), S(Z), the NEAR rows, and the individual rows.

## 3. Readings, deciding tests, and what counts for and against

**Rules for every reading:**
- **No support from the score alone.** The 43-row score alone can make a reading **consistent** or **inconsistent**. It can never make it **supported**. Support comes only from that reading's own deciding test, run under its own pre-registration.
- **Untested readings stay open.** A reading whose deciding test has not run stays OPEN, whatever the score shows.
- **Fixed list.** The readings below are the registered list. Any reading proposed after targets are opened is labelled **EXPLORATORY (post-score)** and never counts as registered.

**Deciding tests and their status at writing:**

| id | deciding test | status |
|---|---|---|
| DT-UT1 | The UT-1 spec-compliant model version: k = 0 a declared zero mode; k → 0⁺ from k ≠ 0 nodes only, under one pre-registered continuation rule; recomputed end to end (A41). | **NOT SCHEDULED**: 0521 withdrawn by 0524 |
| DT-BHD | BH-D derivation from the owned parent, then out-of-sample tests (TDGs, Leo Ring, DF2/DF4) once BH-D exists (A10). | **NOT SCHEDULED**: 0519 (BH-D step 3) withdrawn by 0524 |
| DT-U12 | Small-k limits at larger L and with mixed sampling: U1, U2, and the P-96 capture (stage 0 is an L = 4 control; L ≥ 6 stages not launched) (A20, A41). | U2 (0523) withdrawn by 0524; P-96 L ≥ 6 not launched |
| DT-T1a | BH-T1a: the residual against the target-free stellar fraction f★ (PRIMARY enclosed, SECONDARY local; M/L 0.4/0.6 variants). Diagnostic, never headline; runs only after a verified freeze (A10, A16.3). | registered |
| DT-GEO | The geometry box (D 12.545–15.18 Mpc, i 69–75°). | NOT_EVALUATED_BEFORE_FREEZE (A16.1); the forward refuses GEOMETRY_NOT_EXPOSED |
| DT-ALT | The alternatives, scored separately: ORIGINAL_K is evaluated; GL10 and the M/L variants are NOT_EVALUATED_BEFORE_FREEZE (A16.2, 0518 item 5). | as stated |
| DT-NAX | Non-axisymmetric finite-flow sensitivity of the m = 0 approximation (plan D3). | not run |
| DT-S1 | Calibration transfer across parameter space (V005 S1). | UNTESTED |

**Readings by pattern:**

| pattern | registered readings | consistent with the reading if | against the reading | deciding test |
|---|---|---|---|---|
| **P1 / P1g** (expected: A15 E2, A41) | **R-MF:** failure of the present-mass-only lapse response of the L = 4 coefficient method at the A2 grid and calibrated θ (A15 E3; TESTED-NEGATIVE for exactly this if P1 holds). | P1 holds | no P1 with N_v(OUTER) ≥ 1 | the score itself, for this scope only |
| | **R-UT1:** the static isothermal typing of the k = 0 block (A20 reading 1; counted CA-34/CA-28, A41). | P1 holds | A41 item 3 (FORMAL + TESTED) already registers that no gate-consistent typing gives an attractive tail, and the spec-compliant T(0⁺) is finite and repulsive on current estimates; a DT-UT1 run that leaves the deficit | DT-UT1 |
| | **R-HIST:** a missing Bind-history or collective component (A10 SA-BH-01, DECLARED-PREMISE; A20 reading 2; BH-D). | P1 holds; P1g makes it more specific ("missing long-range component", 0522) | DT-BHD gives no outer change, or a derived weighting fails out of sample | DT-BHD |
| | **R-REACH:** magnitudes, k = 0-block drift or finite-size effects at larger L or with mixing (A20 narrowed: these cannot create a 1/r tail). | P1 holds | DT-U12 leaves the outer magnitudes unchanged | DT-U12 |
| **P2** (contrary to E2) | **R-MF**, with the opposite sign: overshoot; **R-S1:** calibration transfer of G_eff = G·Q∞ (A21; S1 UNTESTED); **R-GRID:** k-grid fidelity at outer radii (A17: C3 is the criterion that matters). | P2 holds | ORIGINAL_K shows the same excess (against R-GRID); DT-S1 shows a consistent transfer (against R-S1) | DT-S1, DT-ALT, the A17 C3 record |
| **P3 / P4** | **R-GEFF:** the single DDO154 short-wavelength G_eff does not carry over to a galaxy with stellar share about 0.51 (DDO154 about 0.03) (A21, E1); **R-ML:** stellar M/L (0.5, counted ±20%; A10); **R-SPEC:** a species or history weight (SA-BH-01); **R-GEO:** geometry (A23); **R-NAX:** m = 0 projection (A17 note; D3). | P3/P4 holds | **R-ML:** the DT-T1a M/L variants do not move the inner rows by the miss. **R-GEO:** DT-GEO is not evaluated, so this reading stays OPEN by construction. | DT-T1a, DT-ALT (M/L), DT-GEO, DT-NAX |
| **P5** | the onset of the finite-reach deficit (as P1), or local structure in the transition zone | P5 holds | an onset radius inconsistent with k* (A12: wavelengths of tens of kpc) is reported as a comparison only | as P1; DT-NAX |
| **P6** | **R-S1** (G_eff scale); **R-GEO** (distance scale); **R-MF** | P6 holds | DT-S1 consistent; a DT-GEO evaluation removing the offset (not available before freeze) | DT-S1, DT-GEO |
| **P7** | row-level systematics: non-circular motion and the m = 0 projection (R-NAX); otherwise R-MF at row level | P7 holds | — | DT-NAX |
| **P8** | no miss reading. If N_v(OUTER) ≥ 1, it runs **against** the A15 E2 / A41 expectation and is reported as such. | — | — | P8 triggers a mandatory check that ORIGINAL_K and the A17 C3 grid record agree. Agreement is reported; it does not change the headline. |
| **P9** | the outer test is unavailable (all OUTER rows INVALID); E2 reads NOT_TESTABLE | — | — | the outer-gas confinement question (A12.5), not a rotation-row test |

**BH-T1a is used as registered, diagnostic only.**
- The rank correlation and slope of r_q against f★(R) bear jointly on M/L and on a species or history weight.
- They are not a verdict on Bind history alone (A10).
- A trend is reported under R-ML and R-SPEC together, and never under one of them alone.

## 4. INVALID-as-miss rows

- **Separate list.** They are listed separately with their roster reason:
  - slots V002 GL4 Q01/Q02;
  - the outer-gas cut (A12.5/A14 C3), with its truncation radius and mass fraction;
  - any root-listed gate.
- **Scored as worst-tier misses.** They count toward the 43 (0518) and are scored as worst-tier misses.
- **They take no part in the readings.** They are excluded from N_v(Z), from m(Z) and from every pattern except P0 and P9.
- **They are never re-explained after the fact.** The only statement made about an INVALID row is its roster reason. No reading cites an INVALID row as evidence for or against anything.
- **A roster change after targets are opened is not allowed.** Any later root ruling on a roster row is recorded as post-score and does not change this classification.

## 5. Comparison with the A15 expectations (after the score; labelled COMPARISON, not a fit)

- **E1 (inner disc).**
  - Report whether the frozen model rotation exceeds the frozen baryonic-Newtonian rotation at INNER rows. Both are model quantities from the registered sources, computed target-free; never the SPARC baryon columns.
  - Report H(INNER), N(INNER) and M(INNER) against the bands.
  - Label: "COMPARISON with A15 E1".
- **E2 (outer disc).**
  - Report P1/P1g/P2/P8/P9 for OUTER.
  - If OUTER rows are INVALID by the outer-gas cut, say so.
  - Label: "COMPARISON with A15 E2".
- **E3.** E3 is the reading rule, applied through §3. It is reported as "applied". No comparison number is attached.
- **Never an adjustment.** No expectation is adjusted, and no row is re-read, to improve agreement.

## 6. Report format (score step)

The report gives:
1. the per-row table: Q_id, zone, R_q, tier, r_q, sign, and the NEAR flag;
2. the zone summaries;
3. the patterns that hold;
4. for each pattern, its registered readings with the status consistent / inconsistent / OPEN, plus each deciding test's status;
5. the INVALID list;
6. the A15 comparison;
7. any EXPLORATORY (post-score) readings, labelled as such.

**The words used:**
- "TESTED-NEGATIVE" only for R-MF within its stated scope;
- "consistent with" never written as "supports".

## 7. Self-check: could any rule be steered by the outcome?

| risk | how it is closed here |
|---|---|
| Moving the zone boundaries to put misses inside or outside a zone | The cuts are numbers fixed in §1.3 before targets are opened. They come from A15, registered target-free. |
| Redefining HIT or NEAR after seeing residuals | The tiers use only frozen LADDER fields and the quoted σ (§1.1); no tolerance is a free parameter. |
| Choosing which member is scored | The frozen reference member, plus the frozen PRIMARY envelope. Alternatives are separate (I-4). |
| Choosing which pattern to report | Every applicable pattern is reported (§2); none masks another. |
| Upgrading "consistent" to "supported" | Prohibited (§3); support comes only from a deciding test with its own prereg. |
| Re-explaining INVALID rows to rescue or condemn a reading | Prohibited (§4). |
| Adding a favourable reading after the fact | It is labelled EXPLORATORY and is never registered (§3). |
| Dropping rows or inflating σ | Prohibited (I-1, I-2). |
| Reading the withdrawn deciding tests as done | Their status is NOT SCHEDULED, and their readings stay OPEN. |
| **Residual risk (not closed).** The thresholds "miss-dominated ≥ half", S(Z) at \|m\| > 1 and the half-split trend rule are choices made here. | They are fixed now, before targets; root may change them only before the seal (M-3). |
| **Residual risk (not closed).** NEAR depends on the width of the frozen envelope band, which depends on the member-selection rule. | That rule is frozen with the manifest (D5), so NEAR cannot be steered after targets. A wide band could hide misses as NEAR, which is why NEAR rows are reported individually. |

## 8. Root items for this prereg (decide before the seal)

- **M-1. Tiers.** HIT/NEAR/MISS are not registered tiers of the score. The code has WITHIN_ERROR and MISS_WORST_TIER, plus the envelope `band_overlaps_error_bar`.
  - Proposal: §1.1.
  - Alternative: σ-multiples for NEAR (for example 1 < \|r\| ≤ 2). Its 2 would then be a new free number, which is why it is not proposed.
- **M-2. Zone cuts.** 10.0 and 30.0 kpc, from the A15 E1/E2 wording.
  - Alternative: cuts from the frozen stellar disc scale (for example 2.2 R_d), if root prefers a geometry-derived rule.
- **M-3. Thresholds.** The values in §2. They are fixed once root seals.
- **M-4. Deciding tests NOT SCHEDULED** (0524: 0519, 0521, 0523 withdrawn).
  - The readings R-UT1, R-HIST and R-REACH therefore stay OPEN after the score, whatever it shows.
  - Root may schedule their deciding tests later under their own preregs; this document does not.
- **M-5. Inputs.** The score inputs come from the freeze successor root adopts. v003f is under review; field names are as in v003d/v003f. If the adopted successor renames a field, the mapping in §1.1 follows the renamed field. It never changes the rule.

## 9. Sources (sha256 from bytes at writing)

**Dispatches:**

| item | sha256 |
|---|---|
| 0522 | `30af5d6811788e9bbed4c470dae0ea9bb4ae5230a734fa7940e942b30ed66160` |
| 0524 | `d1430abc84025cc4afde31f3fd4fce1845e8d2334e47e95fbeb81936d7dfd4df` |
| 0518 | `0748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279` |
| 0531 | `7233faf3be6d498a662f9f3dcc743c12420bbc6fa997e606aeb72e7d16ca3cd6` |

**Root decisions:**

| addendum | entries used | sha256 |
|---|---|---|
| V003 (frozen) | A10, A12 | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` |
| V004 (frozen) | A15, A16, A17, A20, A21, A23, A41 | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| V005 (open; observed) | A48 principle, 0518 / A55 log | `743dcfb5ce1aed1c471d2fc16ddc2e8838343256a162903a45aa6153dad9de11` |

**LADDER field definitions:**

| file | sha256 |
|---|---|
| `freeze_score_readiness_cx3/v003f/prediction_freeze_c2v003f_cx3v001.py` (`_ladder_row`, `_band_rows`) | `18a10d98718b3a337837add6d9c2841486061ef8c73663e983b5a8e1305d7636` |
| `calibration_engine_freeze_v003b_v003d/prediction_freeze_c2v003d.py` (WITHIN_ERROR_RULE, HEADLINE_RULE) | `74e0d4060e443755486fba3aa0775060d2909c2bb78df9d948f346159112b67d` |
