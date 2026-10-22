# ROOT_ITEMS_R2 — root items for the miss-reading prereg r2, round 2 (decide before the seal)

Claude4, dispatches 0585 and 0606. Items M-1 to M-5 are the five V001 items that are still pending. Items M-6 to M-14 are new in r2.

Each item gives:
- the question;
- the options with their consequences;
- a **RECOMMENDATION** (only a recommendation; root rules);
- the reasoning.

No item needs a target, a run, or a C5H or `UVT_*` read to decide.

**Timing (M-6).** Every item is ruled, and the text sealed, before anyone reads any step-5 NGC route-A/B output value. If that is not met, every item is adopted exactly as recommended here, with no option switching, and the deviation is disclosed.

**0606 coverage.** These are the rough edges from Codex1's steps 6–7 rehearsal (FROM_CODEX1/0058; `steps6_7_rehearsal_cx1/REHEARSAL_COMPLETE_V001.json`):

| 0606 item | where r2 addresses it |
|---|---|
| 1. An evaluated STAGE0 needs an adopted successor | M-14; text §6.3 (the receipt rule) and DT-S0G |
| 2. A TSR flag and radial-support carrier | M-7; text §1.4 (the derived rule; Q25 flagged) |
| 3. An E1b Newtonian carrier | M-11; text §5.1(b) |
| 4. A P8 C3 consistency carrier | M-13; text §3, the P8 row (the T120L C3 record, A27) |
| 5. Adoption of the unsealed prereg and the production classifier | M-6 (the seal and its timing) and M-12 (a binding classifier) |
| 6. I6, the A66 versus 0512 wording | fixed in the text: I-6 states the gate (0550) and 0512's actual words |

---

## M-1. Tiers, and the NEAR flag (§1.1)

**Question.** The registered score has WITHIN_ERROR and MISS_WORST_TIER, plus the envelope's `band_overlaps_error_bar`. How are rows tiered for the reading, and what is NEAR?

**Options.**
- (a′) Tiers INVALID_AS_MISS / HIT / MISS, plus NEAR as a **flag** on a MISS row (the envelope interval intersects the error bar). A NEAR row stays a MISS in every count and pattern.
- (a) V001: NEAR as a fourth tier, removed from M(Z).
- (b) NEAR as a σ-multiple, for example 1 < |r| ≤ 2.
- (c) No NEAR at all.
- (d) The NEAR flag defined as "some PRIMARY member has `within_error = true` on that row" (frozen fields, no new number).

**RECOMMENDATION: (a′), as written in §1.1.**

**Reasoning.**
- The round-1 lenses showed that (a) was wrong in two ways (A-03, L-C06, L-C25):
  - **Its gloss was false.** An envelope that straddles the error bar overlaps it while no member is within error.
  - **It was lenient.** Removing NEAR rows from M(Z) could switch off the miss-dominated patterns, and with them the E3 verdict.
- (a′) keeps the information and corrects the gloss. A flag cannot change any pattern.
- (b) adds a free number.
- (d) is a sound alternative if root prefers member-level meaning. It would change only the flag's definition, never a count.

## M-2. Zone cuts and membership (§1.3)

**Question.** Keep the cuts at 10.0 and 30.0 kpc, taken from the A15 E1/E2 wording, and the membership by id they give (INNER Q01–Q24, TRANSITION Q25–Q35, OUTER Q36–Q43)?

**RECOMMENDATION: yes.**

**Reasoning.**
- The cuts are A15's own words.
- The OUTER set equals the registered STAGE0 scope and v003g's `_alternative_score_scope`.
- Fixing membership by id removes any later argument about rows near the cuts: Q25 at 10.04 kpc and Q36 at 30.08 kpc each sit just above a cut.
- The alternative, a disc-scale cut such as 2.2 R_d, would add a parameter from the stellar model and break that coincidence.

## M-3. Pattern thresholds, exclusivity, OUTER_FAILURE and the new patterns (§2)

**Question.** Adopt the §2 rule set?
- miss-dominated: M ≥ N_v/2;
- hit-dominated: H > N_v/2 (strict), so the two are exclusive and a tie goes to miss;
- S(Z) at |m| > 1;
- the half-split trend;
- the even-count median;
- "an UNDEFINED quantity makes a condition false";
- no vacuous patterns;
- OUTER_FAILURE := OUTER miss-dominated, of any sign, as the A15 E3 trigger;
- the new patterns P11 OUTER_MIXED, P12 INNER_MIXED and P13 TRANSITION_MISS, which together give the coverage property (every outcome with a MISS has a pattern);
- P8 renamed NO_MISS_AMONG_VALID_ROWS, never "all hit".

**RECOMMENDATION: adopt all of it as written.**

**Reasoning.**
- **Each threshold sits at its natural break:** half of the zone's rows, and one σ (the WITHIN_ERROR unit).
- **The fixes close round-1 defects:**
  - In round 1, a tie made a zone both miss- and hit-dominated (L-C05).
  - The E3 verdict fired only under P1, which was easier on the model than A15 E3 (A-04, L-C01, BLOCKING).
  - An OUTER_MIXED, INNER_MIXED or TRANSITION-only failure had no pattern (L-C04).
  - P8 could hold vacuously, or be read as "all hit".
- **Consequences recorded so that root rules knowingly (L-C27).** With N_v(OUTER) = 1, one missing valid OUTER row gives OUTER_FAILURE and the TESTED-NEGATIVE verdict. A15 E3 makes any outer-row failure TESTED-NEGATIVE, so this is the text's rule, not an accident.

## M-4. Deciding tests NOT SCHEDULED, and the readings that stay OPEN (§3)

**Question.** Register these deciding tests as NOT SCHEDULED:
- DT-UT1 (0521 withdrawn);
- DT-BHD (0519 withdrawn);
- DT-U12 (0523 withdrawn; stage 0 done; P-96 deferred, A63);
- DT-TSR (no test registered).

Each reading is then reported as the §3 status tuple: score relation, deciding-test status and prior evidence, with against taking precedence.

**RECOMMENDATION: register exactly that.**
- Scheduling a deciding test later needs its own prereg, and supports a reading only through data not opened when that prereg was sealed.
- The tuple replaces V001's single status word, which the round-1 lenses showed could not be assigned mechanically (B-4, L-C02).

**Reasoning.**
- The principal's standing rule (0524) limits lane work to the galaxy run.
- A tuple shows the score relation and the test status separately, so neither can stand in for the other.

## M-5. Score inputs and field names

**Question.** Bind the classification to freeze v003g (`48a1e48a…`) with slots V003 (`d3859b42…`), using these fields:
- `headline.reference_member_id` and `reference_member_log_index`;
- `members[]`: `member_id`, `log_index`, `member_valid`, `rows[].{score_status, within_error, sigma_ratio, registered_reason, status}`;
- `pointwise_envelope.label` (matched by prefix) and `rows[].band_overlaps_error_bar`;
- `sensitivity.rows`;
- `alternatives[]`: `members`, `scoring_scope`, `status`;
- `freeze_status` and `incomplete_reasons`.

**RECOMMENDATION: bind to v003g and slots V003.**
- Any successor adopted before the freeze carries a field map, reviewed before the seal. The rules never change.
- An evaluated-STAGE0 successor (M-14) is re-checked against §1.1 and §6 before the seal.

**Reasoning.** v003g is the reviewed freeze of record: Claude4 0071 PASS, and the A70 note that step 6's freeze code is ready.

## M-6. The seal: vehicle, timing, cited entries and later entries

**RECOMMENDATION.**
1. **Timing.**
   - Root rules on every item here and seals the text, together with the M-12 classifier, before anyone reads any step-5 NGC route-A/B output value. "Anyone" means root, the author, and every reviewer.
   - Preferred: seal before step 5 launches. A80 put step 5 more than a day away.
   - Until the seal, step-5 outputs are read validity-only (A47 I3), and the seal entry attests to this.
2. **Vehicle.** The seal is a root entry registering the sha256 of this text and of the classifier: in V005 if before its freeze, otherwise in the V006 addendum (A82).
3. **Cited entries.** The seal check confirms that every cited V005 entry's **section sha** equals the pin in §11 (the RI-26 rule of A81). Presence alone is not enough. The cited entries are A48, A50, A52, A56, A60, A62, A63, A64, A65, A66, A70, A81, A82 and A90.
4. **Later entries.** Any root entry after the assembly read that touches the reading needs a revision of this text, or an explicit no-change note in the seal entry. This covers entries in V005 until its freeze, and in V006 after it. Check T7 lists them mechanically.
5. **At the score step,** root verifies the sealed shas from bytes before the classifier runs.

**Reasoning.**
- The round-1 lenses showed three gaps:
  - "before targets" alone left every rule open to tuning once the predictions were readable, and NGC3198's flat outer curve is public (B-1);
  - later V005 entries were uncovered (A-11, B-6, L-C11);
  - section-sha checks were missing.
- This is the same acyclic, fail-closed pattern as A81 RI-26 and A82.

## M-7. The TRUNCATION_SHAPE_RESIDUAL overlap rule and its carrier

**Question.** A66 and 0550 require the freeze to flag the rows "overlapping" a failing TRUNCATION_SHAPE ring. The registered compare stores the ring's radial support as a single sampled radius. Which rows are flagged, and what carries the flag?

**Facts from bytes** (target-free model records):
- **The failure.** The production compare `K32_COMPARE_COMPLETE_V001.json` (`6f095f64…`; Codex1 0056; A90) reads N_FAIL_N1. One TRUNCATION_SHAPE ring fails: ordinal 15, R = 10.540847… kpc, S/θ = 1.014818…. Its `radial_support` is `{"kind": "sampled_ring", "R_kpc": 10.540847…}`.
- **The rings.** The N1 record `K32_RECORDS_COMPLETE_V001_N1.json` (`8867c376…`) lists 100 ring radii. They equal, bitwise, the 100 GL4 node radii of `REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (`ec1dcca5…`), so the rings are the registered route-B nodes. Ring 14 is at 9.901811 kpc and ring 16 at 10.911722 kpc.
- **The observation rule** registered in slots V003 is "piecewise-linear interpolation of mean onto the supplied 43 manifest radii without extrapolation".

**Options and what each flags:**

| support definition | rows flagged |
|---|---|
| **(i) dependence (derived):** rows whose route-B value depends on ring 15 under the registered interpolation, that is r_14 < R_q < r_16 | **NGC3198-Q25** (10.04 kpc) only |
| (ii) the stored point, R_q = 10.540847… | none |
| (iii) the ring's sampling cell, between the midpoints to rings 14 and 16 (about 10.22 to 10.73 kpc) | none |
| (iv) the two query rows bracketing the ring | Q25 and Q26 |

**RECOMMENDATION: (i), as written in §1.4.**
- **Carrier:** a separate root-pinned, target-free flag record listing the failing rings, the rule and the flagged ids, pinned among the freeze manifest's input files.
- **Codex3's step-5 extractor** (0618, `extract_carriers_cx3v005.py` `50c7db5f…`) already emits the 43 flags from an adopted support. It holds them UNAVAILABLE until root adopts one, and it requires the support to contain its native ring; (i) does.

**Reasoning.**
- **(i) is not a choice.** It follows from two registered facts: the rings are the route-B nodes, and rows are linear interpolants of the node means. A row depends on node k only when it lies strictly between nodes k − 1 and k + 1.
  - Q25, at 10.04 kpc, lies between rings 14 and 15, so it depends on ring 15.
  - Q26, at 11.04 kpc, lies between rings 16 and 17, so it does not.
- **It removes the knife-edge.** Round 1 rightly noted that any width "chosen" here sits on a knife-edge, and that a broader flag widens an excuse reading. R-TSR can be CONSISTENT for a flagged MISS row (A-02, B-2). (i) removes the choice.
- **The other options.** (ii) and (iii) flag nothing and would empty the row-level disclosure that A66 and 0550 require. (iv) flags a row that cannot depend on the ring.
- **Its cost.** R-TSR has registered prior evidence against it (A66.2: route B consumes the azimuthal mean), and it may cite only Q25. The exposure is one TRANSITION row.

## M-8. Scoring a FREEZE_INCOMPLETE manifest

**RECOMMENDATION.** If root authorizes such a score:
- the classification and every table are made in full;
- every pattern and reading carries "PROVISIONAL (FREEZE_INCOMPLETE)", with the `incomplete_reasons`;
- if envelope rows are invalid, the report states that the NEAR flag could not be set.

**Reasoning.** Every outcome registers (A10/A15). The label keeps an incomplete freeze from being over-read; it follows the A50 PROVISIONAL rule, by analogy.

## M-9. The DT-S0G comparison rule (§6.3)

**RECOMMENDATION: §6.3 as written.** On the OUTER rows that are valid under both members and have a defined r_q under both:
- **CONSISTENT** if H_S > H_P;
- **AGAINST** if H_S ≤ H_P and the twin's median |r| is at least the reference member's;
- **NOT_DECIDED** otherwise.

TWIN_INVALID and NOT_DECIDED leave R-DRIFT OPEN, and the comparison never makes R-DRIFT supported.

**Reasoning.**
- The rule uses only counts and medians, with no new tolerance.
- Round 1's AGAINST condition ("same sign class") read AGAINST even when the twin shrank every residual four times without gaining a hit (L-C27). The median-|r| test fixes that: such a twin now reads NOT_DECIDED.
- "Never supported" follows from S0-FAIL-RHAT and A65 check R-3.
- **Recorded consequence:** a twin that gains one hit reads CONSISTENT whatever happens to the other rows.

## M-10. Alternative classification: the twin rule (§6.1)

**RECOMMENDATION: §6.1 as written.**
- **The twin.** The alternative's member with the same `log_index` as the reference member. v003g guarantees one exists, because every evaluated alternative's members equal the PRIMARY's selected representatives.
- **Valid twin.** A valid twin has `member_valid = true`; otherwise the alternative reads TWIN_INVALID.
- **Ids.** The twin's ids must equal its scope: Q01–Q43, or the STAGE0 `scoring_scope.query_ids`.
- **No NEAR flag** for alternatives.

**Reasoning.**
- Round 1's premise that a twin might be missing was wrong (A-13, L-C08). The correction makes the rule exact.
- An alternative's NEAR flag would need a band-scoring step that the reviewed freeze module does not perform.

## M-11. The A15 E1(b) baryonic-Newtonian carrier (§5.1)

**RECOMMENDATION: report E1(b) as NOT_AVAILABLE**, unless root wants a target-free carrier pinned before the freeze and an owner can build it in time. Codex3's extractor (0618) already marks the E1b carrier UNAVAILABLE when no Newtonian reference is supplied.

**Reasoning.**
- A15 E1's own deciding observable, the inner rows against their bands, is reported in E1(a) with no new input.
- E1(b) is model-internal, but it would be new computation on the step-6 path.
- It is a COMPARISON only.

## M-12. A mechanical, sealed classifier, binding at the score step

**RECOMMENDATION: binding, as the text now requires (§1.1, §8).** The classification comes from two independent implementations that must agree.

- **Implementation A.** Claude4 builds a target-blind classifier implementing §1–§6 exactly on v003g's `score_after_freeze` format.
  - **Strict parsing (A71).** It refuses duplicate keys and non-finite constants, and nothing in it is last-wins.
  - **Envelope label.** It matches the envelope label by prefix.
  - **Pre-score checks.** It runs the §1.1 stop checks on a synthetic score built from the frozen member arrays.
- **Implementation B.** Codex1's rehearsal classifier (`steps6_7_rehearsal_cx1/miss_reading_rehearsal_cx1v001.py`; 0058) is rehearsal-only (0606). It is brought to the final text, as the second lineage.
- **Agreement.** Both run on one shared synthetic suite, and every output must agree:
  - every tier, flag and pattern, including P10–P13;
  - the E3 verdict line;
  - the status tuples;
  - the twin rule and TWIN_INVALID;
  - PROVISIONAL;
  - every stop condition;
  - the DT-S0G boundaries;
  - the boundary cases Codex2's r2 prep checklist lists: half-count ties, the trend split, missing carriers, and status changes of alternatives.

  A disagreement means the text is ambiguous; the text is fixed before the seal.
- **Seal.** A is sealed with the text, and the agreement record is pinned. Root runs A on the real score, and A's tables are the report's tables. B is not run on real data. There is no hand classification.

**Reasoning.**
- The classifier removes discretion at the one step that sees targets.
- Round 1 showed that a text alone leaves status words and against-conditions to the reporter (B-4, L-C02).

## M-13. A pinned T120L C3 record for the P8 report (§3)

**Question.** If P8 holds, §3 requires a report of the in-use grid's C3 record beside ORIGINAL_K's twin classification. Round 1 named the A17 tier-1 C3 record, which belongs to grids not in use (A-07).

**RECOMMENDATION.**
- Root names the T120L C3 record of A27 (T120L passes C2, C3, C4 and C1′) by path and sha in the seal entry.
- If none is pinned before the freeze, that half of the P8 report reads NOT_AVAILABLE, and the ORIGINAL_K half is still reported. Codex3's extractor (0618) already marks the P8/C3 carrier UNAVAILABLE when no C3 record is supplied.

**Reasoning.**
- The report is a consistency disclosure. It never changes the headline or any status.
- A record chosen after targets are opened could be chosen selectively.

## M-14. The STAGE0 receipt rule, and the evaluated-STAGE0 successor (§6.3)

**Question.** Slots V003 registers STAGE0_GRID_OUTER as NOT_EVALUATED_BEFORE_FREEZE, and v003g refuses an evaluated STAGE0 under it (Claude4 0071 N2; Codex1 0058). When is STAGE0 evaluated, and what admits it?

**RECOMMENDATION.**
1. **The receipt rule, as written in §6.3.** STAGE0 is evaluated if and only if every registered STAGE0 member has a FINISHED receipt before the freeze manifest is written.
   - Root decides on receipts and validity booleans only, reads no prediction value, and records the receipt times.
   - A result available only after the freeze is EXPLORATORY, and R-DRIFT stays OPEN.
2. **Prepare the successor now,** target-free.
   - Its only change permits EVALUATED_BEFORE_FREEZE for STAGE0, with scope, grid pin and `headline: false` unchanged.
   - My 0071 STAGE0 checks are repeated end to end, and it gets an independent review.
   - It is adopted exactly when rule 1 says STAGE0 is evaluated.

**Reasoning.**
- Round 1 left STAGE0's adoption to root approval after the predictions exist (B-3). A receipt-only rule removes that discretion.
- Preparing the successor in advance means the outcome depends only on whether the runs finish.
