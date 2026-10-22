# ROOT_ITEMS_R3A — root items for the miss-reading prereg r3a (decide before the seal)

Claude4, dispatches 0585, 0606 and 0619 (A98.2). Items M-1 to M-5 are the five V001 items that are still pending. Items M-6 to M-14 are new since V001, and M-15 is new in r3.

**r3a [r3a]** (dispatch 0687; root ruling A133). M-16 is new, and the notes tagged [r3a] in M-3, M-5, M-6, M-8, M-11, M-12, M-13 and M-14 carry the A133 two-phase protocol and the r3a review fixes into the items. No option recommended in r3 is changed; M-5 gains the per-phase inputs, M-6 the r3 withdrawal, M-12 the Phase-1 and Phase-2 cases and M-14 the Phase-2 receipt rule. Every recommendation still binds both phases; the score of record is the first Phase-2 score (text I-7).

Each item gives:
- the question;
- the options with their consequences;
- a **RECOMMENDATION** (only a recommendation; root rules);
- the reasoning.

No item needs a target, a run, or a read of a protected run to decide.

**Timing (M-6).** Every item is ruled, and the text sealed, before anyone reads any step-5 NGC route-A/B output value. Step 5 is never delayed for the seal. If the timing is not met, every item is adopted exactly as recommended in the pre-prediction version: the ROOT_ITEMS file named in the last SEAL CANDIDATE post published before that first read (M-6 item 1). There is no option switching, and the deviation is disclosed.

**0606 coverage.** These are the rough edges from Codex1's steps 6–7 rehearsal (FROM_CODEX1/0058; `steps6_7_rehearsal_cx1/REHEARSAL_COMPLETE_V001.json`):

| 0606 item | where r3 addresses it |
|---|---|
| 1. An evaluated STAGE0 needs an adopted successor | M-14; text §6.3 (the receipt rule, with the successor pinned in the seal entry) and DT-S0G |
| 2. A TSR flag and radial-support carrier | M-7; text §1.4 (the dependence rule; Q25 flagged; the support record) |
| 3. An E1b Newtonian carrier | M-11; text §5.1(b) |
| 4. A P8 C3 consistency carrier | M-13; text §3, the P8 report (the T120L C3 record, A27) |
| 5. Adoption of the unsealed prereg and the production classifier | M-6 (the seal, its timing and the fallback versions) and M-12 (a binding classifier) |
| 6. I6, the A66 versus 0512 wording | fixed in the text: I-6 states the gate (0550), 0512's actual words, and the BLOCKED cases with their sources |

---

## M-1. Tiers, and the NEAR flag (§1.1)

**Question.** The registered score has WITHIN_ERROR and MISS_WORST_TIER, plus the envelope's `band_overlaps_error_bar`. How are rows tiered for the reading, and what is NEAR?

**Options.**
- (a′) Tiers INVALID_AS_MISS / HIT / MISS, plus NEAR as a **flag** on a tier-MISS row whose envelope row is valid and intersects the error bar. A NEAR row stays a MISS in every count and pattern. NEAR reads NOT_AVAILABLE where the envelope row is invalid.
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
- **Invalid envelope rows (r3).** v003g marks every envelope row invalid when any PRIMARY member is unevaluated. Its overlap field is then false, which is not evidence of no overlap; so NEAR reads NOT_AVAILABLE there (round-2 R2B-10).
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

## M-3. Pattern thresholds, the sign-class rule, OUTER_FAILURE and the patterns (§2)

**Question.** Adopt the §2 rule set?
- miss-dominated: M ≥ N_v/2; hit-dominated: H > N_v/2 (strict), so the two are exclusive and a tie goes to miss;
- U(Z), the unsigned MISS rows (null-ratio rows and LATE-gate rows);
- **the sign class:** S(Z) is UNDEFINED when m(Z) is UNDEFINED, or when Z is miss-dominated and M − U < N_v/2; otherwise DEFICIT / EXCESS / CENTERED at |m| > 1;
- "an UNDEFINED quantity makes a condition false", except the definedness tests of P14 and P15; P6 compares defined classes only;
- the half-split trend, the even-count median, GROWING (P1g) and CROSSING (P11g);
- no vacuous patterns;
- OUTER_FAILURE := OUTER miss-dominated, of any sign, as the A15 E3 trigger; equivalently exactly one of P1, P2, P11 or P14;
- the patterns P11 OUTER_MIXED, P12 INNER_MIXED, P13 TRANSITION_MISS, P14 OUTER_UNSIGNED and P15 INNER_UNSIGNED, which give the coverage property, proved case by case for each zone in §2;
- P8 named NO_MISS_AMONG_VALID_ROWS, never "all hit".

**Options for the two choices that are not forced.**
- **The sign-class rule.**
  - (A) As written: withhold S(Z) when Z is miss-dominated and the signed misses alone do not reach half of N_v(Z) (M − U < N_v/2).
  - (B) Withhold S(Z) only when Z is miss-dominated and the signed rows alone are hit-dominated (M − U < H).
  - Both close the round-2 defect: neither takes a signed class (DEFICIT or EXCESS) from hits alone [r3a], and with either one OUTER_FAILURE, coverage and the E3 line agree on every synthetic outcome tried (recheck refuter verify_newdefects_1).
  - **Their consequences differ.** Under (A), a zone's sign class depends on whether its gates are LATE: a LATE gate can withhold a sign class that the same gate on time would allow (P1 becomes P14, and P3 becomes P15). Under (B), defined sign classes are the same whether a gate is LATE or on time, but a sign class can rest on one signed miss while most of the misses have no prediction.
- **The meaning of "outer-row failure".**
  - (alpha) As written: OUTER miss-dominated.
  - (gamma) Any failing OUTER row: M(OUTER) ≥ 1.
  - **Consequence:** with 2 of 8 OUTER rows missing, (gamma) reads TESTED-NEGATIVE and (alpha) reads NOT_NEGATIVE_AT_OUTER.

**RECOMMENDATION: adopt the rule set as written, with (A) and (alpha).**

**Reasoning.**
- **Each threshold sits at its natural break:** half of the zone's rows, and one σ (the WITHIN_ERROR unit).
- **(A) over (B).** A signed class (DEFICIT or EXCESS) is printed as a property of a zone's misses [r3a]. Under (A) a miss-dominated zone's signed class rests on signed misses that make up at least half of the zone's valid rows, never on a minority [r3a]. Its gate-timing dependence goes one way only: a LATE gate can only withhold a sign class, never create or switch one, and LATE status is now decided mechanically (M-15). The alternative (B) is sound if root prefers invariance under gate timing.
- **(alpha) over (gamma).** A15 E2 states its expectation for the outer rows as a set (the outermost query rows are "the most likely place for misses"), and E3 reads the failure of that expectation. Under (gamma), one miss among eight rows within error would read TESTED-NEGATIVE, so the verdict would rest on a single row's σ. Root rules; this is the binding E3 text, not a gap that the A48 principle fills.
- **The fixes close round-1 and round-2 defects:**
  - In round 1, a tie made a zone both miss- and hit-dominated (L-C05).
  - The E3 verdict fired only under P1, which was easier on the model than A15 E3 (A-04, L-C01, BLOCKING).
  - An OUTER_MIXED, INNER_MIXED or TRANSITION-only failure had no pattern (L-C04).
  - In round 2, a miss-dominated zone whose valid rows lacked a ratio had no pattern, so OUTER_FAILURE could be true while P1, P2 and P11 were false (Codex2 0490, BLOCKING; A98.2). P14, P15 and the definedness exception close this.
  - In round 2, a zone's sign class could be taken from its hits when its misses were unsigned (R2B-01). The sign-class rule closes this.
  - P8 could hold vacuously, or be read as "all hit".
- **Consequences recorded so that root rules knowingly (L-C27).**
  - With N_v(OUTER) = 1, one missing valid OUTER row gives OUTER_FAILURE and the TESTED-NEGATIVE verdict. A15 E3 makes an outer-row failure TESTED-NEGATIVE, so this is the text's rule, not an accident.
  - The all-LATE outer zone is ruled under M-15.

## M-4. Deciding tests NOT SCHEDULED, the status tuple, and the reading rules (§3)

**Question.** Register these deciding tests as NOT SCHEDULED:
- DT-UT1 (0521 withdrawn);
- DT-BHD (0519 withdrawn);
- DT-U12 (0523 withdrawn; stage 0 done; P-96 deferred, A63);
- DT-TSR (no test registered).

And report every registered reading, every time, as the §3 status tuple: score relation, deciding-test status as it stands at the score step, and prior evidence from a closed list. Part 1 is decided in one fixed order: NOT_ADDRESSED (PATTERN_NOT_HELD) when no trigger holds, then INCONSISTENT when an against-condition holds, then the sign-scope codes, then CONSISTENT. Each reading has one tuple rule, whatever triggers it. Three rules fix which readings are triggered, and how the deficit-type ones read:
- **the A10 rule:** every MISS row with a frozen prediction is cited by R-MF and by a history or species reading (R-HIST for OUTER and TRANSITION rows and under P6/P7; R-SPEC for INNER rows). The zone patterns cover the rows of miss-dominated zones, P6 and P7 cover all MISS rows, and the row-level trigger MINORITY_MISS(Z) covers a miss in a zone that is not miss-dominated while another zone is;
- **the A15 E3 rule:** every OUTER_FAILURE, of any sign, triggers R-MF, R-UT1, R-REACH, R-HIST and R-DRIFT for the OUTER rows;
- **the deficit-type sign rule:** R-UT1 and R-REACH read CONSISTENT only when S(OUTER) is DEFICIT or CENTERED with a signed deficit miss, and otherwise NOT_ADDRESSED with a code (SIGN_SCOPE_EXCESS, SIGN_SCOPE_UNSIGNED or SIGN_SCOPE_NO_DEFICIT_MISS). Their deciding-test status stays OPEN.

**Options for the sign rule.**
- (i) As written: R-UT1 and R-REACH are deficit-type; R-HIST, R-MF and R-DRIFT are sign-free.
- (ii) All five sign-free: R-UT1 and R-REACH read CONSISTENT under any OUTER_FAILURE, an excess included.

**RECOMMENDATION: register exactly that, with option (i).**
- Scheduling a deciding test later needs its own prereg, and supports a reading only through data not opened when that prereg was sealed.
- The tuple replaces V001's single status word, which the round-1 lenses showed could not be assigned mechanically (B-4, L-C02).
- DT-T1a (BH-T1a) is diagnostic: it never changes part 2 of a tuple, and its trend is shown only in the descriptive lines.
- An alternative never refutes a PRIMARY reading (§6.1), so the M/L alternatives' NOT_EVALUATED status is prior evidence for R-ML, not an against-condition.
- P5 carries no reading of its own; its OUTER rows are read under OUTER_FAILURE and its TRANSITION rows under P13. P8 and P9 trigger no reading.

**Reasoning.**
- The principal's standing rule (0524) limits lane work to the galaxy run.
- A tuple shows the score relation and the test status separately, so neither can stand in for the other.
- **The A15 E3 rule.** A15 E3 is binding and attaches its three open readings to an outer-row failure with no sign restriction. In round 2 they were registered only for P1, while P2 and P11 also read TESTED-NEGATIVE (round-2 F1, BLOCKING). Keying them to OUTER_FAILURE itself covers P14 too.
- **The A10 rule.** A10 reads every miss of the galaxy run two ways, and SA-BH-01 carries that reading into the freeze manifest. Round 2 gave P13, P6 and P7 no history reading (F1 item 4).
  - The r3 refute then found that the zone rule holds only per outcome. Once any zone is miss-dominated, a miss in another zone was cited by no reading, and the flagged row Q25 could be read only as R-TSR. A LATE gate could even remove every reading of a real miss in another zone.
  - MINORITY_MISS(Z) closes this: every MISS row with a frozen prediction is now read both ways (FORMAL, §3), as A10 requires for every miss. It changes no count, pattern or E3 line.
  - The alternative was to restate the rule per outcome and exempt P10. It is not recommended, because A10 and SA-BH-01 speak of every miss.
- **The part-1 order.** The r3 candidate gave R-DRIFT two part-1 rules (§3 and §6.3) that disagree when DT-S0G reads AGAINST and OUTER_FAILURE does not hold, as the integrate suite and the r3 refute both found. With no trigger, the score does not bear on R-DRIFT, so PATTERN_NOT_HELD comes first; part 2 still prints AGAINST (DT-S0G), so the evidence stays visible.
- **Why (i).** R-UT1 and R-REACH explain missing long-range attraction, which can only lower the outer rotation (A12.3 "missing reach"; A20 puts the tail question in the k = 0 typing; A41). Calling them CONSISTENT with an outer excess would add an explanation that their own mechanism cannot give. The A48 principle favours the reading less favourable to the model as registered. They stay reported and OPEN, as A15 E3 requires. R-HIST stays sign-free because A10 says "every miss".

## M-5. Score inputs, field names and carriers

**Question.** Bind the classification to freeze v003g (`48a1e48a…`) with slots V003 (`d3859b42…`), using these fields and carriers:
- `headline.reference_member_id` and `reference_member_log_index`, checked against the frozen manifest;
- `members[]`: `member_id`, `log_index`, `member_valid`, `rows[].{score_status, within_error, sigma_ratio, registered_reason, status}`;
- `pointwise_envelope.label` (matched by prefix) and `rows[].{valid, band_overlaps_error_bar}`;
- `sensitivity.rows[].{valid, band_overlaps_error_bar}`;
- `alternatives[]`: `name`, `kind`, `status`, `role`, `scored`, `members`, `scoring_scope`;
- `freeze_status` and `incomplete_reasons`;
- the TSR flag record (its pin and its 43 flags), the TSR support record (§1.4), and the compare, N1 and node record pins;
- the gate-status list (§4; M-15);
- the STAGE0 status record: the step-4 start time, the receipt times and the successor pin (§6.3);
- **[r3a]** the phase that the score entry names; the frozen manifest's `input_bindings.calibration_record` path; and the Phase-1 registry root that the seal entry names by path. The PHASE_MISMATCH stop (§1.1) derives the manifest's phase from these, so it needs no new manifest field;
- **[r3a]** in Phase 1, the pinned L1 record's band rows (`lo_q`, `hi_q`, the FD_NOISE_NOT_BOUNDED flag, and NOT_AVAILABLE), for the Phase-1 band column (M-16). Their keys and value encodings are those of the A133 `band` command at the sha the seal entry pins, so they are fixed at the seal, and a defect in them affects only that column (§1.1).
- **[r3a] Per phase.**
  - In Phase 1, the STAGE0 status record, the ORIGINAL_K alternative and the sensitivity rows are not required. STAGE0 reads NOT_IN_PHASE_1, ORIGINAL_K reads NOT_AVAILABLE and the sensitivity rows read invalid (text I-4), so their absence stops nothing.
  - In Phase 2, every input above is required, except the L1 band rows. Phase 2 also takes, for text §8 item 11 only, the A133 agreement record (keys and encodings those of the `agree` command at the sha the seal entry pins; the AT-1 fields may be absent under AGREEMENT_DEFECT) and the sealed Phase-1 classification output by its sha; and the Phase-2 commitment status (I-7), which reads EXPLORATORY if missing or malformed. A defect in any of these affects only item 11, or for the status only the label (text §1.1 map).

**RECOMMENDATION: bind to v003g and slots V003, with exactly these inputs.**
- "A field named here is missing" is a stop condition, so the list must be complete (round-2 R2B-11, F14).
- Any successor adopted before the freeze carries a field map, reviewed before the seal. The rules never change.
- An evaluated-STAGE0 successor (M-14) is re-checked against §1.1 and §6 before the seal.

**Reasoning.** v003g is the reviewed freeze of record: Claude4 0071 PASS, and the A70 note that step 6's freeze code is ready. The field names above are read from the v003g bytes (`score_after_freeze`, `_band_rows`, `_pointwise_envelope`).

## M-6. The seal: vehicle, timing, the fallback versions, the attestation, cited entries and later entries

**RECOMMENDATION.**
1. **Timing.**
   - Root rules on every item here and seals the text, together with the M-12 classifier, before anyone reads any step-5 NGC route-A/B output value. "Anyone" means root, the author, and every reviewer.
   - Preferred: seal before step 5 launches. **Step 5 is never delayed for the seal.**
   - Until the seal, and in any case until RUNBOOK step 4 begins, step-5 outputs, STAGE0's included, are read validity-only (A47 I3).
   - **[r3a] Per phase** (A133 §2 and §3). "Before anyone reads any step-5 output value" means before the first output value of either phase, which is a Phase-1 value: A133 forbids any Phase-1 NGC value to be read before this text and the classifier are sealed, and any Phase-1 NGC launch before an r3a seal candidate exists. RUNBOOK step 4 is per phase, as the text's Status section defines it.
   - **The attestation.** The seal entry lists every validity fact seen before the seal (receipts, valid flags and reason codes, and who saw them), and records a statement from each lane that touched the text or the classifier after step 5 launched that it read no step-5 output value. If step 4 begins after the seal, the score entry attests the time from the seal to the start of step 4 the same way. In Phase 2 that is Phase-2 step 4, and the attestation covers only the Phase-2-only output values, the calls not re-bound from Phase 1, because Phase-1 values are public after the Phase-1 score [r3a].
   - **The fallback versions (Codex2 TF-S1; round-2 F6; the r3 refute).** If the timing fails, the text, the root-item recommendations and the classifier that apply are the files named in one post: the last SEAL CANDIDATE post (Status) published before the first step-5 output value was read. A candidate that a root entry stamped before that read rules FAIL is withdrawn, and with no candidate the classification is EXPLORATORY (post-prediction). The seal entry names those shas and their times. Every later change is POST-PREDICTION and is listed with its diff; the report also gives the classification under the pre-prediction versions; a status that holds only under a later version is EXPLORATORY.
   - **Publication.** I publish every candidate as a SEAL CANDIDATE post with its `date -u` time, the r3 candidate as soon as its review round closed, and the r3a candidate before the first Phase-1 NGC launch [r3a]. Until such a post exists, a step-5 read would make the whole classification EXPLORATORY.
   - **[r3a] Why r3a must be a candidate before the first Phase-1 launch.** r3 (Claude4 0124) is a seal candidate. If the timing failed with r3 as the last candidate, the fallback would adopt r3's unamended I-7, under which the first successful score, the Phase-1 score, is the one classified. A133 therefore makes an r3a seal candidate a hard gate before any Phase-1 NGC launch.
   - **[r3a] RECOMMENDATION: withdraw r3's candidate.** Even after an r3a candidate is posted, r3 could still be revived: suppose the r3a candidate is ruled FAIL before the first read and no later candidate follows. Root therefore rules the r3 candidate (0124) withdrawn for the two-phase run, through the existing FAIL mechanism, in an entry stamped before the first Phase-1 read.
2. **Vehicle.** The seal is a root entry registering the sha256 of this text and of the classifier, in the V006 addendum: V005 closed with A106, and every later root ruling, this seal entry included, goes in V006 (A82; A106.3). It names the sha256 of the rendered text, which is how check T7 finds it (§11). No V006 entry before it may name that sha, and the rulings on M-1 to M-16 go in the seal entry itself or cite the items by id, so the pin graph stays acyclic [r3a]. **[r3a]** The seal entry also names, by path, the Phase-1 registry root (the PHASE_MISMATCH stop, text §1.1), and pins the shas of the A133 `band` and `agree` commands, which fix the L1 and agreement-record schemas.
3. **Cited entries.** The seal check confirms that every CITED_PINNED entry of `V005_ENTRY_TABLE_R3A.json` has the **section sha** pinned in §11 (the RI-26 rule of A81). Presence alone is not enough. The cited entries are A47, A48, A50, A52, A56, A60, A62, A63, A64, A65, A66, A70, A71, A80, A81, A82, A90, A97, A98, A99, A101 and A106. A80 and A97 are named only in the closure tables of the clause map, as review history, and no clause uses them; they are pinned because every entry the texts name counts as cited.
4. **Every other V005 heading, and later entries.**
   - Every other `## ` heading of V005 has a NO_CHANGE row with its reason, written by hand, read from the bytes recorded in the table (the A99.3 pattern).
   - At the seal, the frozen V005 whole-file sha is compared with the table's `v005_sha256_read`. If they differ, every difference is dispositioned before the seal: a new heading gets a row (a revision of this text, or a NO_CHANGE row with its reason); an in-place edit of a NO_CHANGE entry is re-read and re-dispositioned; an edit inside a CITED_PINNED section fails its pin and needs a revision or an explicit no-change note in the seal entry.
   - **V006.** The same holds for V006, through the hand-written `V006_ENTRY_TABLE_R3A.json` (§11): one row for every V006 heading written before the seal entry, read from the bytes and re-read at the seal. An entry that only supplies an input this text names (M-8, M-15, an N-test successor, the M-14 successor, a field map, the M-13 record) is NO_CHANGE, and the classifier reads it at the sha pinned in the seal or score entry. The seal entry and every later entry lie outside the table.
   - The check's currency verdict (`verdict_currency`) is read from its JSON at the seal, not from its exit code.
5. **At the score step,** root verifies the sealed shas from bytes before RUNBOOK step 9. A mismatch is the pre-target stop SEAL_SHA_MISMATCH.

**Reasoning.**
- The round-1 lenses showed three gaps:
  - "before targets" alone left every rule open to tuning once the predictions were readable. The target curve's qualitative shape is public literature knowledge; this is not a target read, and no classification rule uses it (B-1; B-12's caveat);
  - later V005 entries were uncovered (A-11, B-6, L-C11);
  - section-sha checks were missing.
- The round-2 recheck showed three more:
  - the fallback had no version selector, and left wording and the classifier free (Codex2 TF-S1; F6);
  - the read-with-no-change list was computed as a complement, so it attested nothing (F3, R2C-S6); the hand-written table replaces it;
  - in-place edits of no-change entries were invisible (F4); the whole-file comparison at the seal catches them.
- An in-place amendment of a cited section, such as a later change to A98.1 or to A101's V007 items, fails closed. It is cleared by re-reading the section and either revising this text or recording a no-change note in the seal entry.
- The r3 refute found the V006 gap BLOCKING: the check failed currency whenever any V006 file existed, while the seal entry itself goes in V006, so currency failed by construction. The V006 table and the seal-entry rule close it; finding the seal entry by the rendered text's sha needs no new root act.
- This is the same acyclic, fail-closed pattern as A81 RI-26, A82 and A99.

## M-7. The TRUNCATION_SHAPE_RESIDUAL overlap rule, its support record and its carrier

**Question.** A66 and 0550 require the freeze to flag the rows "overlapping" a failing TRUNCATION_SHAPE ring. The registered compare stores the ring's radial support as a single sampled radius. Which rows are flagged, and what carries the flag?

**Facts from bytes** (target-free model records):
- **The failure.** The production compare `K32_COMPARE_COMPLETE_V001.json` (`6f095f64…`; Codex1 0056; A90) reads N_FAIL_N1. One TRUNCATION_SHAPE ring fails: ordinal 15, R = 10.540847… kpc, S/θ = 1.014818…. Its `radial_support` is `{"kind": "sampled_ring", "R_kpc": 10.540847…}`.
- **The rings.** The N1 record `K32_RECORDS_COMPLETE_V001_N1.json` (`8867c376…`) lists 100 ring radii. They equal, bitwise, the 100 GL4 node radii of `REGISTERED_ROUTE_B_GL_NODES_CX3V001.json` (`ec1dcca5…`), so the rings are the registered route-B nodes. Ring 14 is at 9.901811 kpc and ring 16 at 10.911722 kpc.
- **The observation rule** registered in slots V003 reads: "HI-weighted mean of R*Omega, then piecewise-linear interpolation of mean onto the supplied 43 manifest radii without extrapolation".
- **Column locality.** The route-B column value at node k depends only on ring k (round-2 recheck lens R2-B, TESTED from the rotation and adapter module bytes).

**Options and what each flags:**

| reading of "radial support" | rows flagged |
|---|---|
| **(i) dependence:** rows whose route-B value depends on ring 15 under the registered interpolation, that is r_14 < R_q < r_16 | **NGC3198-Q25** (10.04 kpc) only |
| (ii) the stored point, R_q = 10.540847… | none |
| (iii) the ring's sampling cell, between the midpoints to rings 14 and 16 (about 10.22 to 10.73 kpc) | none |
| (iv) the two query rows bracketing the ring | Q25 and Q26 |

**RECOMMENDATION: (i), as written in §1.4.**
- **Support record** (Codex3's extractor schema UNT_ROOT_TSR_SUPPORT_CX3V001): one ring entry, native_ring the compare's ordinal-15 record verbatim; lower_kpc 9.901810628740723 (r_14), lower_inclusive false; upper_kpc 10.911721936765339 (r_16), upper_inclusive false. It contains the failing ring, as the extractor requires.
- **Carrier:** a separate root-pinned, target-free flag record listing the failing ring, the rule and the flagged ids, pinned among the freeze manifest's input files.
- **The text's id list governs.** A flag record, compare, N1 record or node record that differs is the pre-target stop TSR_FLAG_TABLE_MISMATCH.
- **Codex3's step-5 extractor** (0618, `extract_carriers_cx3v005.py` `50c7db5f…`) emits the 43 flags from the adopted support record and holds them UNAVAILABLE until root adopts one.

**Reasoning.**
- **(i) is the dependence reading, derived from registered facts.** The rings are the route-B nodes, each node's value is local to its ring, and rows are linear interpolants of the node values. A row depends on node k only when it lies strictly between nodes k − 1 and k + 1.
  - Q25, at 10.04 kpc, lies between rings 14 and 15, so it depends on ring 15.
  - Q26, at 11.04 kpc, lies between rings 16 and 17, so it does not.
  - The other readings are possible readings of the words "radial support"; (i) is the one that matches how a row's value is made. Round 2 rightly said that "not chosen" overstated this (R2B-08).
- **It removes the knife-edge.** Round 1 rightly noted that any width "chosen" here sits on a knife-edge, and that a broader flag widens an excuse reading. R-TSR can be CONSISTENT for a flagged MISS row (A-02, B-2). (i) removes the choice.
- **The other options.** (ii) and (iii) flag nothing and would empty the row-level disclosure that A66 and 0550 require. (iv) flags a row that cannot depend on the ring.
- **Its cost.** R-TSR has registered prior evidence against it (A66.2: route B consumes the azimuthal mean), and it may cite only Q25, and only when Q25 is a MISS with a frozen prediction. The exposure is one TRANSITION row.

## M-8. Scoring a FREEZE_INCOMPLETE manifest

**Question.** If the freeze ends FREEZE_INCOMPLETE, may that manifest be scored, and how is it read?

**RECOMMENDATION.**
- **Decide now.** The seal fixes the rule: a FREEZE_INCOMPLETE manifest is scored and classified in full, with the labels below. A different decision is valid only if root records it before any step-5 output value is read. An authorization made later is EXPLORATORY (post-prediction).
- If it is scored:
  - the classification and every table are made in full;
  - every pattern, reading and zone summary, the E3 verdict line and the DT-S0G comparison carry "PROVISIONAL (FREEZE_INCOMPLETE)", with the `incomplete_reasons`;
  - NEAR and N(Z) read NOT_AVAILABLE wherever the envelope rows are invalid, and the report says so.
- **[r3a] Phase 1.** A133 lists M-8, as recommended here, in its step-0 V006 batch (A133 §2), and makes every Phase-1 manifest FREEZE_INCOMPLETE by design (A133 §1.6). The Phase-1 classification carries the label PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE), with the `incomplete_reasons` (text I-7). This adds the phase name to the label; it changes no rule.

**Reasoning.**
- Every outcome registers (A10/A15). The label keeps an incomplete freeze from being over-read; it follows the A50 PROVISIONAL rule, by analogy.
- Round 2 left the authorization to a moment when the predictions are readable, and the E3 line unlabelled (R2B-10). Fixing it at the seal removes that choice.

## M-9. The DT-S0G comparison rule (§6.3)

**RECOMMENDATION: §6.3 as written.** On the OUTER rows that are valid under both members and have a defined r_q under both:
- **CONSISTENT** if H_S > H_P;
- **AGAINST** if H_S ≤ H_P and the twin's median |r| is at least the reference member's;
- **NOT_DECIDED** otherwise.

The closed mapping of §6.3 sets R-DRIFT's tuple: under OUTER_FAILURE, AGAINST makes part 1 INCONSISTENT; without OUTER_FAILURE, part 1 is NOT_ADDRESSED (PATTERN_NOT_HELD) and part 2 still prints AGAINST (DT-S0G); NOT_DECIDED, TWIN_INVALID, TWIN_INPUT_DEFECT, NOT_EVALUATED_BEFORE_FREEZE and EVALUATED_REFUSED leave it OPEN. The comparison never makes R-DRIFT supported.

**Reasoning.**
- The rule uses only counts and medians, with no new tolerance.
- Round 1's AGAINST condition ("same sign class") read AGAINST even when the twin shrank every residual four times without gaining a hit (L-C27). The median-|r| test fixes that: such a twin now reads NOT_DECIDED.
- "Never supported" follows from S0-FAIL-RHAT and A65 check R-3.
- Round 2 found the part-2 word after NOT_DECIDED ambiguous, and TWIN_INPUT_DEFECT unruled (F10, R2B-12). The closed mapping fixes both.
- **Recorded consequence:** a twin that gains one hit reads CONSISTENT whatever happens to the other rows.

## M-10. Alternative classification: the twin rule (§6.1)

**RECOMMENDATION: §6.1 as written.**
- **The twin.** The alternative's member with the same `log_index` as the reference member. v003g guarantees one exists, because every evaluated alternative's members equal the PRIMARY's selected representatives.
- **Valid twin.** A valid twin has `member_valid = true`; otherwise the alternative reads TWIN_INVALID.
- **Ids.** The twin's ids must equal its scope: Q01–Q43, or the STAGE0 `scoring_scope.query_ids`. Otherwise TWIN_INPUT_DEFECT.
- **No NEAR flag and no TSR flag** for alternatives. The §4 LATE rule applies to a twin's gate rows.

**Reasoning.**
- Round 1's premise that a twin might be missing was wrong (A-13, L-C08). The correction makes the rule exact.
- An alternative's NEAR flag would need a band-scoring step that the reviewed freeze module does not perform.
- The N-tests ran on the PRIMARY operator and grid, so the TSR flag has no meaning for an alternative's rows (round-2 R2B-12).

## M-11. The A15 E1(b) baryonic-Newtonian carrier (§5.1)

**RECOMMENDATION: report E1(b) as NOT_AVAILABLE**, unless root wants a target-free carrier pinned before the freeze (in either phase, no later than the Phase-1 score [r3a]) and an owner can build it in time. Codex3's extractor (0618) already marks the E1b carrier UNAVAILABLE when no Newtonian reference is supplied.

**Reasoning.**
- A15 E1's own deciding observable, the inner rows against their bands, is reported in E1(a) with no new input.
- E1(b) is model-internal, but it would be new computation on the step-6 path.
- It is a COMPARISON only.

## M-12. A mechanical, sealed classifier, binding at the score step

**RECOMMENDATION: binding, as the text now requires (§1.1, §8).** The classification comes from two independent implementations that must agree.

- **Implementation A.** Claude4 builds a target-blind classifier implementing §1–§6 exactly on v003g's `score_after_freeze` format.
  - **Strict parsing (A71).** It refuses duplicate keys and non-finite constants, and nothing in it is last-wins.
  - **Envelope label.** It matches the envelope label by prefix.
  - **Pre-score checks.** It runs every §1.1 stop on a synthetic score built from the frozen member arrays.
- **Implementation B.** Codex1's rehearsal classifier (`steps6_7_rehearsal_cx1/miss_reading_rehearsal_cx1v001.py`; 0058) is rehearsal-only (0606). It is brought to the final text, as the second lineage. A133 assigns classifier B to Codex1, the build that needs a different lineage [r3a].
- **Agreement.** Both run on one shared synthetic suite, and every output must agree:
  - every tier, flag and pattern, P10–P15, P1g and P11g included, and every zone count, U(Z) included;
  - the E3 verdict line with its printed counts;
  - every reading's tuple, with each NOT_ADDRESSED code;
  - the twin rule, TWIN_INVALID and TWIN_INPUT_DEFECT;
  - PROVISIONAL (FREEZE_INCOMPLETE and N_GATE_NOT_OPEN);
  - every stop condition, TSR_FLAG_TABLE_MISMATCH, REFERENCE_MEMBER_MISMATCH, GATE_STATUS_LIST_DEFECT and SEAL_SHA_MISMATCH included, and NOT_READ after a re-run stop;
  - the STAGE0 statuses (EVALUATED_BEFORE_FREEZE, EVALUATED_REFUSED, RECEIPTS_AFTER_STEP4, NO_SEALED_SUCCESSOR, and in r3a STAGE0_RECEIPT_NOT_FINISHED and NOT_IN_PHASE_1, with the tie case of a STAGE0 receipt written at the recorded Phase-2 step-4 start) and the DT-S0G boundaries and mapping;
  - every class in Codex2's prep checklist (`CHECKLIST_CX2V001.md`): missing, wrong-type or non-finite row fields; duplicate or reordered ids; a wrong reference member or custody; the INVALID/NEAR boundary and P8/P9 coexistence; exact half-count and residual-sign thresholds; the outer-trend split; unregistered flag scope; missing twins; public alternative status changes; and missing E1b or C3 carriers;
  - **(r3) the round-2 cases:** null-ratio rows, LATE-gate rows, and zones where the signed misses do not reach half (P14, P15); Codex2's 0490 witnesses verbatim; the newdefects cases C14, C15, C16b, C17d and C40, with C16d as a P1 control (refuter V-1); the closure cases U1, U2 and L1–L4; the refuters' early-against-LATE pairs and threshold edges (G1, G4, G5, G6, E_tie, E_one, E_hit_majority, the all-hit outcome, P10G/P10L, U1Lt); and the readings cases V2–V9 (P2, P11 crossing and alternating, P5 with an excess or mixed outer, TRANSITION-only, scattered, global excess);
  - the LATE-against-on-time pairs of the text-stage self-test, which exercise every pattern change §4 lists;
  - **(r3 fix) the refute-stage witnesses** (`r3_work/refute_logic/`, files WITNESSES_V001, WITNESSES_EXTRA_V001 and WITNESSES_STAGE0_V001):
    - W1, W1b, W1c, W11 and W12 for MINORITY_MISS. Every MISS row with a frozen prediction must be cited by R-MF and by R-HIST or R-SPEC, Q25 beside R-TSR included, and a LATE gate must never remove those readings;
    - W2, and an AGAINST twin with no OUTER_FAILURE, for the single part-1 order of R-DRIFT: (NOT_ADDRESSED PATTERN_NOT_HELD, AGAINST (DT-S0G));
    - W3 for NOT_READ: with a defective OUTER row the E3 line prints TESTED-NEGATIVE and P1 reads NOT_AVAILABLE;
    - one case for each class of the §1.1 stop-to-output map.
  - **[r3a] the Phase-1 cases** (A133: the classifier carries the PHASE-1 label and the r3a fields):
    - the label PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE) on every output that carries a PROVISIONAL label;
    - ORIGINAL_K reading NOT_AVAILABLE, and the sensitivity rows reading invalid, in Phase 1;
    - STAGE0 reading NOT_EVALUATED_BEFORE_FREEZE with NOT_IN_PHASE_1, and R-DRIFT part 2 OPEN with that code;
    - the Phase-1 band column (M-16): yes, no and NOT_AVAILABLE, the FD_NOISE_NOT_BOUNDED flag, and the closed-interval edges of the unwidened band;
    - no Phase-1 classification when Phase 1 makes no NGC call;
    - PHASE_MISMATCH (text §1.1): a score entry naming one phase on a manifest from the other phase's registry stops before target access. For each phase, an honest manifest, whose calibration-record path lies inside or outside the named Phase-1 registry root, passes.
  - **[r3a] the Phase-2 cases:**
    - the three agreement outcomes of text §8 item 11. COVERED leaves Phase 1 standing; SUPERSEDED labels every Phase-1 pattern, reading, zone summary, E3 line and band entry WITHDRAWN, replaces each one except the band entries by Phase 2's, and lists the failing (member, row) entries; AGREEMENT_DEFECT leaves Phase 2 standing;
    - the cross-phase tier comparison, with INVALID_AS_MISS rows compared by reason and LATE-gate rows by kind;
    - an EXPLORATORY Phase 2 (text I-7): every Phase-2 output carries the label and Phase 2 stays the score of record; a missing or malformed commitment status reads EXPLORATORY with COMMITMENT_STATUS_DEFECT;
    - a defect in the agreement record or in the Phase-1 classification input: only item 11 (or its cross-phase items) reads NOT_AVAILABLE; an AGREEMENT_DEFECT record without AT-1 fields is not a defect;
    - the Phase-2 attestation restricted to Phase-2-only values.

  A disagreement means the text is ambiguous; the text is fixed before the seal.
- **Seal.** A is sealed with the text, and the agreement record is pinned. Root runs A on the real score, and A's tables are the report's tables. B is not run on real data. There is no hand classification.

**Reasoning.**
- The classifier removes discretion at the one step that sees targets.
- Round 1 showed that a text alone leaves status words and against-conditions to the reporter (B-4, L-C02).
- Round 2 named the checklist classes and the undefined-sign, LATE and reading cases that the suite lacked (F1, F2, F16, R2B-01).

## M-13. A pinned T120L C3 record for the P8 report (§3)

**Question.** If P8 holds, §3 requires a report of the in-use grid's C3 record beside ORIGINAL_K's twin classification. Round 1 named the A17 tier-1 C3 record, which belongs to grids not in use (A-07).

**RECOMMENDATION.**
- Root names the T120L C3 record of A27 (T120L passes C2, C3, C4 and C1′) by path and sha in the seal entry.
- If none is pinned before the freeze (in either phase, no later than the Phase-1 score [r3a]), that half of the P8 report reads NOT_AVAILABLE, and the ORIGINAL_K half is still reported. Codex3's extractor (0618) already marks the P8/C3 carrier UNAVAILABLE when no C3 record is supplied.

**Reasoning.**
- The report is a consistency disclosure. It never changes the headline or any status.
- A record chosen after targets are opened could be chosen selectively.

## M-14. The STAGE0 receipt rule, and the evaluated-STAGE0 successor (§6.3)

**Question.** Slots V003 registers STAGE0_GRID_OUTER as NOT_EVALUATED_BEFORE_FREEZE, and v003g refuses an evaluated STAGE0 under it (Claude4 0071 N2; Codex1 0058). The slots record requires "a root-approved immutable slots successor". When is STAGE0 evaluated, and what admits it?

**RECOMMENDATION. The rule, identical to §6.3:**
0. **[r3a] Phase 1.** STAGE0 is not in the Phase-1 set (A133). In the Phase-1 classification it reads NOT_EVALUATED_BEFORE_FREEZE with the reason NOT_IN_PHASE_1. The rule below is for Phase 2, and "RUNBOOK step 4" in it means Phase-2 step 4.
1. STAGE0 is EVALUATED_BEFORE_FREEZE if and only if both of these hold and the adopted successor refuses no STAGE0 record:
   - **(a) [r3a]** every registered STAGE0 member's terminal receipt under A133 §3 rule (c) is FINISHED;
   - **(b)** the prepared STAGE0 slots/module successor is pinned by sha256 in the seal entry, or, under the Status fallback, it is named in the seal candidate that gives the pre-prediction versions. Pinning it there registers STAGE0 as a Phase-2 step-5 call (A133 §3).
2. **[r3a]** Phase-2 step 4 begins automatically, so its start is not chosen. Its recorded start time is the write time of the last registered terminal receipt, and a receipt written at that instant counts as before step 4. Root records the step-4 start time and every receipt time. No Phase-2-only output value, STAGE0's included, is read before Phase-2 step 4 begins (the validity-only rule of the Status section). The seal or score entry attests it.
3. When (a) and (b) hold, the pinned successor is adopted with no further decision. If it refuses a STAGE0 record, STAGE0 reads EVALUATED_REFUSED.
4. **[r3a]** Otherwise STAGE0 reads NOT_EVALUATED_BEFORE_FREEZE (A65.2), with every reason that applies: STAGE0_RECEIPT_NOT_FINISHED if (a) fails, and NO_SEALED_SUCCESSOR if (b) fails (STAGE0 is then not registered for Phase 2).
5. Validity booleans and output values never change the status, and root reads no prediction value to decide it.
6. A STAGE0 result that first becomes available after RUNBOOK step 4 begins (RECEIPTS_AFTER_STEP4) is EXPLORATORY (post-score), and R-DRIFT stays OPEN.

**Prepare the successor now,** target-free:
- its only change permits EVALUATED_BEFORE_FREEZE for STAGE0, with scope, grid pin and `headline: false` unchanged;
- my 0071 STAGE0 checks are repeated end to end, and it gets an independent review before the seal, so that its sha can be pinned there.

**Reasoning.**
- Round 1 left STAGE0's adoption to root approval after the predictions exist (B-3). A receipt-only rule removes that discretion.
- Round 2 found the r2 rule stated two ways and circular: evaluation required an adopted successor, and the successor was adopted exactly when STAGE0 was evaluated, so root's adoption, made after step-5 values exist, decided the status (R2B-04, F11). Here the successor's pin is fixed before any step-5 value is read, and the receipts are times, so nothing is decided after the predictions are readable.
- **The cut-off is RUNBOOK step 4,** because the STAGE0 raw results, cut contexts and roster are needed at steps 1–4 (R2B-04(e)).
- **The cut-off is chosen blind.** The r3 refute found that validity-only reads ended at the seal, so root could have timed the start of step 4, and with it R-DRIFT's tuple, after reading prediction values. The validity-only rule now runs until step 4 begins, with its attestation. The other options were a mechanical step-4 start or a STAGE0 deadline in the seal entry; either would make the RUNBOOK's step 4 wait on a rule of this text, while this one constrains only reading.
- **[r3a] Under A133 the Phase-2 step-4 start is mechanical** (A133 §3, RUNBOOK step 4 per phase): it begins when every registered Phase-2 step-5 call, STAGE0 included once its successor is sealed, has a terminal receipt. So rule (a) asks only that STAGE0's terminal receipts be FINISHED, and the tie at the last receipt is resolved in favour of "before". The r3 reasoning above, written when the step-4 start was root's act, is kept as history.

## M-15. LATE gates: the definition, the gate-status list, and an all-LATE outer zone (§4)

**Question.** §4 reads a root-listed gate registered after the predictions exist as LATE. Which gates are LATE, decided how, and how is an outer zone read when every one of its valid rows is in a LATE gate?

**Facts.**
- No field of the score output, the roster or the gate schema carries a registration time (round-2 R2B-03, V2-3).
- RUNBOOK_V001 approves gates at step 4, after step 1 has saved the step-5 raw results.

**Options for the definition.**
- (a) As written: a gate is ON-TIME if and only if the sha256 of its gate document is pinned in a root entry stamped (`date -u`) before the first step-5 launch receipt; every other root-listed gate is LATE.
- (b) ON-TIME if registered before the first step-5 output value exists.

**Options for an all-LATE outer zone.**
- (1) As written: it reads P14, and the E3 line reads TESTED-NEGATIVE although no OUTER prediction exists. The same rows gated on time would read P9 and NOT_TESTABLE.
- (2) It reads NOT_TESTABLE when no OUTER row has a frozen prediction.

**RECOMMENDATION: (a) and (1).**
- The seal or score entry lists every gate pin with its status and the entry that pinned it. The list is a classifier input (M-5), and a root-listed gate missing from it is the pre-target stop GATE_STATUS_LIST_DEFECT.
- Every gate first adopted at RUNBOOK step 4 is therefore LATE.

**Reasoning.**
- **(a) is decidable from bytes:** a root entry's `date -u` stamp against a launch receipt's time. (b) needs the time an output first existed, which no record carries.
- **(1) is the stricter reading.** A LATE gate exists only because the producer reported rows INVALID and root listed them after the predictions existed. Reading the zone as untested would let a gate made after the predictions turn a TESTED-NEGATIVE outcome into NOT_TESTABLE. Under (1), every effect of a LATE gate goes toward more misses (§4, FORMAL and TESTED on synthetic outcomes). The case was left open in round 2 (V-7, V2-4), so it is put to root here.
- The E3 line prints the LATE-gate count, so a TESTED-NEGATIVE that rests on LATE rows is visible.

## M-16. The Phase-1 band column (text §1.1, §8) [r3a]

**Question.** A133 §1.5 fixes the Phase-1 band, its label and its blinding, and A133 §3 asks r3a for "one fixed band column that is never used for a tier". What does the column show?

**Options.**
- (1) **Overlap of the record's band:** "Phase-1 band overlaps: yes / no / NOT_AVAILABLE", where "yes" means the record's band [lo_q, hi_q] meets the error bar. A row whose record prints FD_NOISE_NOT_BOUNDED carries that flag beside its entry. This mirrors the sensitivity column (§1.1).
- (1w) The same, with the band widened to [lo_q − e_q, hi_q + e_q] by the record's FD-noise term e_q.
- (2) The band interval itself, with no overlap test.
- (3) Both.

**RECOMMENDATION: (1).**
- The column is reported for all 43 rows, in Phase 1 only, under the A133 label PHASE1_LINEARISED_ADMITTED_SET_PROJECTION_TRUNCATED_LOWER_BOUND_ON_SPREAD_NOT_A_TIER, conditional on A13.
- It is never used for a tier, a flag, a pattern, a reading or an uncertainty claim (A133 §1.5).
- A row the record gives as NOT_AVAILABLE reads NOT_AVAILABLE, never a zero-width band.
- The band values themselves stay in the pinned L1 record, which the report header names (§8).

**Reasoning.**
- (1) uses the same form as the sensitivity band column, so a reader sees one convention for both conditional bands, and the classifier needs one more column rule, not a new kind of output.
- (1w) is not recommended. Widening the band by e_q can only add overlaps, which favours the model, so the A48 principle (the reading less favourable to the model) picks the unwidened band. e_q stays in the L1 record for any reader, and the flag shows where it is not bounded.
- (2) and (3) print band values in the classification table. Those values are already published in the L1 record, so the report gains nothing by repeating them.
