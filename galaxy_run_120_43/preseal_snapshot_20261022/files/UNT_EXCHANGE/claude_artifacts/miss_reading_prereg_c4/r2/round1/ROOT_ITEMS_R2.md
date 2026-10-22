# ROOT_ITEMS_R2 — root items for the miss-reading prereg r2 (decide before the seal)

Claude4, dispatch 0585. Items M-1 to M-5 are the five V001 items that are still pending. Items M-6 to M-12 are new in r2.

Each item gives:
- the question;
- the options;
- a **RECOMMENDATION** (only a recommendation; root rules);
- the reasoning;
- what changes in the text if root rules otherwise.

No item needs a target, a run, or a C5H or `UVT_*` read to decide.

---

## M-1. Tiers (§1.1)

**Question.** The registered score has no hit/near/miss tiers. It has WITHIN_ERROR and MISS_WORST_TIER, plus the envelope's `band_overlaps_error_bar`. Should the reading use INVALID_AS_MISS / HIT / NEAR / MISS as §1.1 defines them?

**Options.**
- (a) §1.1 as written: NEAR comes from the frozen PRIMARY pointwise envelope only.
- (b) NEAR as a σ-multiple, for example 1 < |r| ≤ 2.
- (c) No NEAR tier.

**RECOMMENDATION: (a).**

**Reasoning.**
- (a) uses only fields the frozen LADDER already computes, and adds no free number.
- (b) introduces a new free number (the 2) with no registered basis. A free number is exactly what A48 tells us not to add.
- (c) discards real information: whether some admitted state reaches the error bar.
- Two safeguards keep NEAR from hiding misses:
  - NEAR rows are reported individually;
  - the LADDER tier of a NEAR row stays MISS_WORST_TIER, so the score is unchanged.

**If root rules otherwise.** Under (c), drop NEAR from §1.1, from N(Z) in §2 and from P7. Under (b), replace the NEAR row of §1.1 and add the number to the self-check (§9).

## M-2. Zone cuts and membership (§1.3)

**Question.** Keep the cuts at 10.0 and 30.0 kpc, taken from the A15 E1/E2 wording, and the membership by query id that they give: INNER Q01–Q24, TRANSITION Q25–Q35, OUTER Q36–Q43?

**Options.**
- (a) As written.
- (b) Cuts from the frozen stellar disc scale, for example 2.2 R_d.

**RECOMMENDATION: (a).**

**Reasoning.**
- The cuts are A15's own registered words.
- Two registered objects already depend on the 30.0 cut, with the same OUTER set:
  - the STAGE0_GRID_OUTER scope (A65; slots V003);
  - v003g's `_alternative_score_scope`.
- (b) would add a parameter taken from the stellar model and break that coincidence.
- Fixing membership by id removes any later argument about rows near the cuts:
  - Q25 at 10.04 kpc and Q36 at 30.08 kpc each sit just above a cut;
  - a mismatch with the frozen manifest stops the classification.

**If root rules otherwise.** Recompute the table from the same target-free query block, before the seal, and rerun the target-free check.

## M-3. Pattern thresholds and the r2 clarifications (§2)

**Question.** Adopt:
- "miss-dominated" and "hit-dominated" at ≥ half of N_v(Z);
- S(Z) at |m| > 1;
- the half-split outer trend;

together with the three r2 clarifications:
- the median of an even count is the mean of the two middle values;
- a condition using an UNDEFINED quantity is false;
- P5 requires N_v(TRANSITION) ≥ 1.

**RECOMMENDATION: adopt all of them as written.**

**Reasoning.**
- Each threshold sits at the natural break of its own quantity:
  - half of the zone's rows;
  - one σ, the same unit as WITHIN_ERROR_RULE.
- The clarifications close tie and vacuous-truth cases that could otherwise be argued after targets. In V001, an all-INVALID transition zone satisfied "TRANSITION not hit-dominated" vacuously, so P5 could hold with no transition evidence at all.

**If root rules otherwise.** Any changed threshold must still be a number fixed before the seal. List it in §9.

## M-4. Deciding tests NOT SCHEDULED, and the readings that stay OPEN (§3)

**Question.** Register these deciding tests as NOT SCHEDULED:
- DT-UT1 (0521 withdrawn);
- DT-BHD (0519 withdrawn);
- DT-U12 (0523 withdrawn; stage 0 done; P-96 deferred, A63);
- DT-TSR (no test registered).

Their readings (R-UT1, R-HIST, R-REACH and R-TSR) then stay OPEN after the score, whatever it shows.

**RECOMMENDATION: register exactly that.** Scheduling any of these tests later needs its own prereg. It does not reopen this text.

**Reasoning.**
- The principal's standing rule (0524) limits lane work to the galaxy run.
- A63 defers the P-96 decision until after the galaxy run.
- A reading must not be read as tested when its test has not run.

## M-5. Score inputs and field names

**Question.** Bind the classification to freeze v003g (`48a1e48a…`) with slots V003 (`d3859b42…`), using the field names in §1.1:
- `members[ref].rows[q]`: `score_status`, `within_error`, `sigma_ratio`, `registered_reason`, `status`;
- `pointwise_envelope.rows[q].band_overlaps_error_bar`;
- `headline.reference_member_id`;
- `alternatives[].members` and `scoring_scope`.

**RECOMMENDATION: bind to v003g and slots V003.**
- Any successor freeze module or slots record adopted before the freeze must carry a field map, reviewed before the seal, from these names to its own. The rules never change; only the field map may.
- If root adopts an evaluated STAGE0 successor (A65.2; Claude4 0071 N2), §1.1 and §6 are re-checked against it before the seal.

**Reasoning.** v003g is the reviewed freeze of record (Claude4 0071 PASS; the A70 entry: "Step 6's freeze code is ready"). V001's field names came from v003d/v003f, and every one of them is checked here against v003g's bytes.

## M-6. The seal vehicle, cited entries and later entries (new)

**Question.** How is this text sealed, and how are later root entries handled?

**RECOMMENDATION.**
1. **Where the seal is registered.** Root registers the sha256 of the final text (r2, or an r3 if root's rulings change wording) in a root entry made before any target access. A82 closes V005 at the V007 freeze, so that entry belongs in the **V006** addendum.
2. **The seal check.** It confirms that every V005 entry this text cites is present in the frozen V005 copy:
   - the cited entries are A48, A56, A60, A62, A63, A64, A65, A66, A70, A81 and A82;
   - this is the RI-26 rule of A81, applied to this prereg.
   - Claude4 can adapt seal tool 1 (`check_frozen_addendum_c4v001.py`) to this text's citations. It is read-only.
3. **Later entries.** Any V006 entry made before target access that touches the reading needs either a revision of this text or an explicit no-change note in the seal entry.
4. **At the score step,** root verifies the sealed sha from bytes before the classification runs.

**Reasoning.** This is the same acyclic, fail-closed pattern A81 RI-26 and A82 established for V007. It costs nothing, and it closes the "text changed after the seal" path.

## M-7. A carrier for the TRUNCATION_SHAPE_RESIDUAL flag, and the definition of "radial support" (new)

**Question.** A66 requires the flag "in the freeze manifest". Neither v003g nor slots V003 has a field for it. What carries the flag, and when does a row count as lying "within the radial support" of a failing ring?

**Options.**
- (a) A separate root-pinned, target-free flag record.
- (b) A v003h freeze successor with a flag field.

**RECOMMENDATION: (a).**
- **Contents.** The record is produced from the production-K_big (32) N1 record of the registered NGC N-test compare; A64.3 says N1 is read only on production-K_big records. For each failing TRUNCATION_SHAPE ring it lists:
  - the ordinal;
  - the radial support [r_lo, r_hi], exactly as stored in that record;
  - S/θ.
- **The rule.** A query q is flagged if and only if r_lo ≤ R_q ≤ r_hi. This is a closed interval, with R_q bound by id.
- **When.** The record is registered with the rosters (RUNBOOK_V001 step 4), before any target access, and the freeze manifest pins it.

**Reasoning.**
- (a) avoids reopening the reviewed v003g bytes.
- The closed interval is the broader choice for a disclosure. A broader flag cannot ease any reading, because R-TSR stays OPEN (DT-TSR is NOT SCHEDULED) and may cite only flagged rows.
- If the formal N-test reading differs from A66's diagnostic, the record follows the formal reading.

**If root rules (b).** §1.4 reads the field instead of the record. Everything else is unchanged.

## M-8. Scoring a FREEZE_INCOMPLETE manifest (new)

**Question.** v003g can stamp FREEZE_INCOMPLETE (`allow_incomplete`). How is the reading done then?

**RECOMMENDATION.** If root authorizes such a score:
- the classification and every table are made and reported in full;
- every pattern and reading carries "PROVISIONAL (FREEZE_INCOMPLETE)", with the manifest's `incomplete_reasons`;
- no reading is written as consistent or inconsistent without that label.

**Reasoning.**
- Every outcome registers (A10/A15), so suppressing the reading would drop information.
- The label keeps an incomplete freeze from being over-read. It follows the PROVISIONAL rule A50 uses for pending steps.

## M-9. The DT-S0G comparison rule (new)

**Question.** If STAGE0_GRID_OUTER is evaluated before the freeze, how does it bear on R-DRIFT?

**RECOMMENDATION: §6.3 as written.** On the OUTER rows that are valid under both:
- **CONSISTENT** if the twin has strictly more HITs than the PRIMARY reference member;
- **AGAINST** if it has no more HITs and the OUTER sign class is unchanged;
- **NOT_DECIDED** otherwise.
- **Never SUPPORTED.**
- If the alternative stays NOT_EVALUATED, R-DRIFT stays OPEN.

**Reasoning.**
- The rule uses only counts and the registered sign classes, with no new tolerance. A strict increase is the smallest decidable change.
- "Never SUPPORTED" follows from two facts:
  - the stage-0 grid failed its own R-hat criterion (S0-FAIL-RHAT);
  - A65 check R-3 shows that stage 0 differs from BIRTHK about as much as from A2, so the causal gloss is UNTESTED.

  A single grid swap at fixed calibrated parameters cannot establish the causal claim.

**If root rules otherwise.** A different rule must also be count- or class-based, fixed before the seal, and listed in §9.

## M-10. Alternative classification: the twin rule, without NEAR (new)

**Question.** V001 said alternatives are "classified the same way". v003g, however, scores alternative members without choosing a reference member, and it band-scores no alternative envelope. How is an evaluated alternative classified?

**RECOMMENDATION: the twin rule of §6.1.**
- **The twin.** The alternative's member with the same `log_index` as the frozen PRIMARY reference member.
- **Tiers.** INVALID_AS_MISS / HIT / MISS, with no NEAR.
- **Fallback.** NO_TWIN, if no valid twin exists.

**Reasoning.**
- The twin is the alternative's counterpart of the PRIMARY reference, at the same admitted calibration point. That is what A65.2 defines for STAGE0_GRID_OUTER.
- A NEAR tier for an alternative would need a band-scoring step that the reviewed freeze module does not perform, and this document should not add computation.
- **This is UNTESTED against real alternative members.** Whether ORIGINAL_K's members share log_index values with the PRIMARY's is known only after the freeze. NO_TWIN handles the case where they do not.

## M-11. The A15 E1(b) baryonic-Newtonian carrier (new)

**Question.** A15 E1's expectation is that the model exceeds the baryonic-Newtonian rotation at R ≲ 10 kpc. Its deciding observable is the inner rows against their bands, which §5.1(a) reports with no new input. The model-to-baryonic-Newtonian comparison itself, §5.1(b), needs a frozen baryonic-Newtonian rotation per row, and v003g has no such field.

**Options.**
- (a) Pin a target-free carrier before the freeze: the Newtonian rotation of the same registered baryonic sources at the reference member's parameters.
- (b) Report §5.1(b) as NOT_AVAILABLE.

**RECOMMENDATION: (b), unless root wants (a) and an owner can build it before the freeze.**

**Reasoning.**
- §5.1(b) is model-internal and needs no target, but it would be new computation on the step-6 path.
- It is a COMPARISON only and feeds no reading, so NOT_AVAILABLE loses nothing that the reading depends on.
- It must never be computed after targets are opened.

## M-12. A mechanical, sealed classifier for the score step (new)

**Question.** Should the classification be done by hand from this text, or by a sealed tool?

**RECOMMENDATION: a sealed tool.**
- **Build.** Claude4 builds a target-blind classifier implementing §1–§6 exactly, on v003g's `score_after_freeze` output format.
- **Tests.** It is tested on synthetic score outputs only, covering every tier, every pattern, P10, the twin rule, NO_TWIN, PROVISIONAL, and every fail-closed stop.
- **Check and seal.** An independent lane checks it, and it is sealed together with this text (its sha in the same seal entry).
- **Use.** At the score step, root runs it on the real score output. Its tables are the report's tables, and no hand classification is used.

**Reasoning.**
- A mechanical classifier removes discretion at the one step that sees targets.
- It also turns this text's rules into tested behaviour before the seal, rather than after.
- It costs a few hours of target-free work, off the critical path until step 6.
