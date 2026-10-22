# REVIEW — round-2 recheck lens R2-B (regressions and new defects): miss-reading prereg r2, round 2

A helper of lane Claude4, under dispatches 0585 and 0606, run as a refute-by-default recheck lens (0592). This lens edits nothing in the object; Claude4 owns the fix round. Clock stamps are in PARTIAL.md (all from `date -u`).

**Verdict: FAIL.** 1 BLOCKING, 6 SHOULD_FIX, 6 NOTE.

The BLOCKING item reproduces, independently, the defect that root already recorded in V005 A98.2 from Codex2 0490, and it shows the defect reaches further than the 0619 description: the sign class itself. Every other finding is outside A98.2 and 0619, so r3 needs to carry them too.

## Object (verified from bytes against round2/HASHES_R2.txt; all match)

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407` |
| CLAUSE_SOURCE_MAP_R2.md | `38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201` |
| ROOT_ITEMS_R2.md | `4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500` |
| NUMBER_PROVENANCE_R2.json | `ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf` |
| TARGET_FREE_CHECK_R2.json | `624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9` |
| TARGET_FREE_MUTATION_TEST_R2.json | `4445a9bf014e0cabe6d49cd0f45e4df1c388ac7c2c443df0d6f1d3a62214ec02` |
| tools/check_target_free_c4v002.py | `4ae4f7053f18aa13416ad4e3d118d9250a959e72035c6e5f0c5f92305d8511aa` |
| tools/test_check_target_free_c4v002.py | `dc812342fa7c363e71949e3ecb2a206d68786ff5973280cf98909d03dd114f92` |
| tools/make_miss_reading_c4v003.py | `2132078f9779b01d5ad05c01b0280c218d160f6380f75ed5b99af893a1a2f9ab` |
| INDEX_R2.md | `0d24b8fe778fb704398a7039f579977d92e51dfd152994d6e68048cffa03b926` |

## Sources read (sha256 from bytes)

**V005 (open), read three times, because root kept writing to it during this review:**

| time | sha256 | what was new |
|---|---|---|
| 19:59:28Z | `991cc242…` | equal to the assembly read |
| 20:08:40Z | `cf9bbf19…` | A97, A98 |
| 20:26:07Z | `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2` | A99, A100 |

All 14 cited section pins match all three versions; my own byte-level extractor is `tools/v005_pins_r2b.py`, with outputs `V005_PINS_R2B.json` and `V005_PINS_R2B_2.json`.

**Root decisions:** V004 `487d4449…` (A14–A17, A27); V003 `5bef6552…`.

**Freeze v003g:** module `48a1e48a…`, slots V003 `d3859b42…`, RUNBOOK_V001 `9557b5aa…`.

**Records:**
- GL4 nodes `ec1dcca5…`;
- K32 compare `6f095f64…` and N1 record `8867c376…`;
- GQ_NGC_91_MS96 `be148bab…`.

**Route-B readout code, for the TSR premise:**
- `owned_free_surface_rotation_v001.py` `e1b354ec…`;
- `owned_column_mean_streaming_observation_v002.py` `6790e28e…`;
- stage `ddo_free_surface_rotation_root_v005_gal_c2v005.py`, which calls them.

**Dispatches and lane posts:**
- every dispatch pinned in §11 matches its stated sha; 0592 is `b1a5310f…`, and 0619 is `238858d1…`;
- Codex1 0032 `3e8c9fc9…`, 0056 `4b67319d…` and 0058 `fc5af831…`;
- Codex3 0618 `8939c004…` and its extractor `50c7db5f…`;
- Codex2 0490 `3a922168…` and the checklist `020ef3f1…`;
- the rehearsal record `19807bb3…`.

**Round 1:** the three lens reviews and the refuter reports (fidelity and targetfree §5–§7).

**Not read:** no NGC3198 target, observed velocity, rotmod/Vobs/MassModels/SPARC path, runs_ext path or UVT_* item. The sibling round-2 lens folders were not read. Nothing was launched.

## Method

1. **My own classifier**, `tools/classify_r2b.py`, written from the r2 text §0–§6 alone. It never chooses silently:
   - a case with no unique answer records AMBIGUITY, with every option;
   - a disagreement between clauses records CONFLICT;
   - a reachable case that no rule covers records GAP.
2. **Synthetic score outputs** in the `score_after_freeze` format, from `tools/synth_r2b.py`.
   - The rows are produced by v003g's own pure helpers, `_score_members`, `_score_members_on_rows`, `_pointwise_envelope`, `_band_rows` and `_distribution`. The module has no import-time side effects.
   - Independent replicas of those helpers were cross-checked against the module: **0 mismatches**.
   - Velocities are 1000 + 10·j km/s and σ is 2 km/s, both deliberately implausible.
3. **48 cases**, in `CASES_R2B_V2.json` (run by `tools/run_cases_r2b_v2.py`). `CASES_R2B.json` is the first run, 42 cases, superseded. The runs used an audit-hook fence:
   - reads only from an allowlist;
   - writes only in this folder;
   - no subprocess or network;
   - forbidden name classes refused.

   **0 fence events.**
4. **The TSR rule recomputed from bytes**, in `TSR_RECOMPUTE_R2B_V2.json`.

## Findings (most severe first)

### R2B-01 — BLOCKING — PREREG [C-2], [C-1.1], [C-4], [C-5.3], [C-9]: undefined-sign MISS rows break OUTER_FAILURE, the E3 line and coverage, and they set the sign class from hits alone

**Quotes:**
- [C-2] L209: "OUTER is miss-dominated, whatever its sign class. It holds exactly when one of P1, P2 or P11 holds."
- [C-2] L212: "Every outcome with at least one MISS satisfies at least one of these: a zone pattern (P1, P2, P11, P3, P4, P12 or P13), or P7."
- [C-1.1] L119: a null-ratio row "counts in N_v(Z) and M(Z), and it is left out of m(Z) and Δ_out."
- [C-4] L324: "each LATE-gate row counts as a non-INVALID MISS row with sign UNDEFINED. A late gate can therefore never remove a pattern or create P9."
- [C-9] L487: "The coverage property holds (§2)".
- [C-9] L492: "A gate added after the predictions removes a pattern | LATE-gate rows count as MISS rows for this document (§4)."

**Defect.** LATE-gate rows and null-ratio rows count in N_v and M but have no r. Three things follow.

- **(a) The two definitions of OUTER_FAILURE disagree.** When every non-INVALID OUTER row is unsigned, OUTER is miss-dominated while S(OUTER) is UNDEFINED. Then:
  - OUTER_FAILURE is true by "miss-dominated" and false by "P1, P2 or P11";
  - the E3 line can read TESTED-NEGATIVE or NOT_NEGATIVE_AT_OUTER;
  - the coverage property fails.

  The same hole exists for INNER.
- **(b) The sign class can come from hits alone.** When the unsigned rows are the misses, m(Z) and S(Z) are computed from the signed rows, which can all be hits.
  - In C16b, OUTER has 4 unsigned LATE misses and 4 hits at r = 0. It reads P11 ("misses of both signs, or small residuals"), with R-S1, R-GRID and R-NAX CONSISTENT, although no miss has a sign at all.
  - In C16d, the four signed misses are deficits and the zone reads P1. R-UT1, R-HIST and R-REACH are then CONSISTENT on four rows that have no prediction.
- **(c) The guarantee sentence is false.** C17c→C17d: gating the two far rows turns Δ_out from −1 to +1 and removes P1g, a trigger entry in C-3.2.

**Practical reach.** A gate may only list rows the producer reported INVALID, so root cannot aim a gate at chosen valid rows. But every root-listed gate adopted at RUNBOOK step 4 comes after the step-5 raw results exist (R2B-03). So unsigned MISS rows are the normal case for any gate, not a corner.

**Evidence.**
- CASES_R2B_V2.json:
  - C14 (all OUTER rows null-ratio): CONFLICT 'C-2 OUTER_FAILURE', GAP 'coverage', CONFLICT 'C-5.3';
  - C15 (all OUTER rows LATE): the same three events;
  - C40 (all INNER rows LATE): GAP 'coverage';
  - C16a/C16b: P1 becomes P11;
  - C16c/C16d: P11 becomes P1;
  - C17c/C17d: P1g is removed.
- The same core defect is independently recorded as BLOCKING by Codex2 0490 and ruled in V005 A98.2 ("allowed undefined-sign MISS rows count in Nv/M … the C-4 LATE gates can remove a pattern"); dispatch 0619 orders r3.

**Fix.**
- (1) Define U(Z) as the number of non-INVALID MISS rows with undefined r.
- (2) S(Z) := UNDEFINED whenever Z is miss-dominated only because of unsigned rows (M − U < N_v/2). This means a sign class is never taken from hits alone.
- (3) Add P14 OUTER_UNSIGNED and P15 INNER_UNSIGNED: zone miss-dominated with S(Z) UNDEFINED.
  - P14 carries R-MF and R-DRIFT.
  - P15 carries R-GEFF, R-GEO and R-NAX.
- (4) OUTER_FAILURE := OUTER miss-dominated, which then equals P1 ∨ P2 ∨ P11 ∨ P14 by construction. Restate coverage with P14 and P15.
- (5) Delete the false sentence in L324, and rewrite the C-9 rows at L487 and L492.
- (6) Add C14, C15, C16b, C17d and C40 to the M-12 agreement suite.

### R2B-02 — SHOULD_FIX — PREREG [C-1.1] L130–134 vs [C-9] L496, [C-5.3] L357, [C-P] L25: after the targets are opened, NOT_READ has no condition

**Quotes:**
- [C-1.1] L130–132: "**After target access,** root may only: correct a field map without changing any value; or declare the classification NOT_READ."
- [C-9] L496: "Root discretion after a stop condition | … Afterwards, only a value-preserving field map or NOT_READ (§1.1)."
- [C-5.3] L357: "One line, always reported".
- [C-P] L25: "Every outcome registers".

**Defect.** C-9 scopes NOT_READ to the case after a stop condition. §1.1, the binding text, does not: after seeing the targets, root may declare the whole classification NOT_READ, with no trigger and no stated reason. That suppresses the patterns and the E3 TESTED-NEGATIVE line that §5.3 says is always reported. It is an outcome-dependent veto. The round-2 rewrite of L-C13 replaced an unconstrained ruling with an unconditioned escape.

**Evidence.**
- PREREG L130–134, L357, L496.
- Every §1.1 stop is target-free and is run before target access, so a legitimate post-target NOT_READ needs a specific trigger, and none is named.

**Fix.**
- "After target access, NOT_READ is allowed only if a §1.1 stop condition, re-run on the real score, fires. The classifier output is still computed and published, labelled NOT_READ with the stop reason, and the E3 line is printed."
- "A field-map correction must leave every target-free output field byte-identical, and is pinned with its diff."

### R2B-03 — SHOULD_FIX — PREREG [C-4] L322; ROOT_ITEMS M-5: whether a gate is LATE cannot be decided mechanically, and in practice every gate is LATE

**Quote.** [C-4] L322: "A root-listed gate registered after any step-5 output value exists is a LATE gate."

**Defect.**
- **No input carries the decision.** None of these has a registration time, or the time the first step-5 output existed:
  - the score output;
  - the roster (v003g `_load_row_roster` L1658: schema, scope, alternative, slots, query_manifest, query_mapping, root_gates, outer_cut);
  - the gate schema (L1713–1716: schema, registration_status, registered_reasons, query_ids).
- **"Registered" is undefined.** It could mean the creation of the gate document or its listing in the step-4 roster.
- **The classifier cannot decide.** M-5 names no LATE input, so the M-12 classifier cannot apply C-4 (C20: GAP).
- **Every gate is LATE in practice.** RUNBOOK_V001 saves the step-5 raw results at step 1 and adopts gates at step 4. So every gate written in response to a producer INVALID row is LATE, and the text never says so.

**Evidence.**
- v003g L1658 and L1711–1726.
- RUNBOOK_V001 steps 1, 3 and 4.
- C20.

**Fix.**
- "A gate is LATE unless its gate document was pinned in a root entry dated before the first step-5 launch receipt."
- The seal or score entry lists every gate pin with its LATE status, and that list is an M-12 input (add it to M-5).
- State that gates adopted at RUNBOOK step 4 are LATE.

### R2B-04 — SHOULD_FIX — PREREG [C-6.3] L391–392 vs ROOT_ITEMS M-14 L257, L263, L116 and M-6 L127: two different STAGE0 receipt rules; one is circular, and the successor is not sealed

**Quotes:**
- PREREG L391: "STAGE0 is EVALUATED_BEFORE_FREEZE if and only if every registered STAGE0 member has a FINISHED receipt before the freeze manifest is written, and an adopted successor admits it."
- PREREG L392: "Root decides on receipts and validity booleans only".
- ROOT_ITEMS L257: "STAGE0 is evaluated if and only if every registered STAGE0 member has a FINISHED receipt before the freeze manifest is written."
- ROOT_ITEMS L263: the successor "is adopted exactly when rule 1 says STAGE0 is evaluated."
- ROOT_ITEMS M-6 L127: the seal registers "the sha256 of this text and of the classifier".

**Defect.**
- **(a) The files disagree.** The PREREG adds "and an adopted successor admits it"; M-14 rule 1 does not.
- **(b) The PREREG version is circular.** Evaluated requires an adopted successor, and the successor is adopted exactly when STAGE0 is evaluated. So both statuses are self-consistent, and root's adoption step, taken after step-5 values exist, decides the status. This reopens the B-3 channel the rule was meant to close.
- **(c) "Validity booleans" are in neither iff,** yet L392 says root decides on them.
- **(d) The successor is not sealed.** ROOT_ITEMS L116 has it re-checked before the seal, but M-6 seals only the text and the classifier. So the successor's admission code can be written or changed after predictions are readable.
- **(e) The cut-off is not where the results are needed.** The cut-off is the manifest write (RUNBOOK step 8), but the STAGE0 raw results, cut contexts and roster are needed at steps 1–4. Whether to redo step 4 for late STAGE0 results is left to root.

**Evidence.**
- PREREG L391–394.
- ROOT_ITEMS L116, L127, L256–263.
- RUNBOOK steps 1–8.
- slots V003 `stage0_registration.evaluated_status_transition`: "Requires a root-approved immutable slots successor".

**Fix.** Put one identical rule in both files:
- "STAGE0 is EVALUATED_BEFORE_FREEZE iff every registered STAGE0 member has a FINISHED receipt before RUNBOOK step 4 begins (its start time is recorded)."
- "The successor, sha pinned in the seal entry, is then adopted with no further decision. If it refuses a STAGE0 record, STAGE0 reads EVALUATED_REFUSED and R-DRIFT stays OPEN. Validity booleans never change the status."

### R2B-05 — SHOULD_FIX — PREREG [C-3.2] L284 (P5): "as P1" is undefined when the OUTER sign is not DEFICIT

**Quote.** L284: "| **P5** | as P1 for the OUTER rows (including R-DRIFT), and R-NAX for the transition zone | as P1 | as P1 | as P1; DT-NAX |".

**Defect.** P5 needs only "OUTER miss-dominated", of any sign. With S(OUTER) = EXCESS or CENTERED, P1 does not hold. "as P1" then has three readings:
- import P1's deficit readings (R-UT1, R-HIST, R-REACH) as CONSISTENT for an excess or mixed outer;
- use the readings of the OUTER pattern that does hold;
- import nothing.

This is not mechanical. The P5 definition is unchanged from round 1 (L156/L202 there) and no round-1 lens raised it, but the r2 rewrite made OUTER_FAILURE sign-agnostic without updating P5's readings.

**Evidence.** C13: INNER hit-dominated, TRANSITION and OUTER excess misses. Patterns P2, P13, P5 and P10 hold, with AMBIGUITY 'C-3.2 P5 row'.

**Fix.** "P5: the readings of the OUTER pattern that holds (P1, P2, P11, or P14 of R2B-01), including R-DRIFT, and R-NAX for the transition zone."

### R2B-06 — SHOULD_FIX — PREREG [C-3] and [C-3.2] L271, L280, L285–289, with [C-6.1] L376: the status tuple is still not mechanical for five readings

**(a) R-MF under P7, and P6.**
- Quotes:
  - L287: "| **P7** | **R-NAX** and **R-MF** at row level, both always reported | — | — | DT-NAX |";
  - L286: P6 lists "DT-S1, DT-GEO" only;
  - L271: R-MF's own row has against "OUTER not miss-dominated, with N_v(OUTER) ≥ 1" and the test "the score itself".
- Defect:
  - R01's against-condition can never hold while R01 is reported, so it is dead there.
  - Under P7 with N_v(OUTER) ≥ 1, the condition holds. Part 1 is then CONSISTENT by the row rule or INCONSISTENT by the reading rule.
  - Part 2 is "the score itself → NOT_NEGATIVE_AT_OUTER" or OPEN.
  - P7 is the generic scattered outcome. Cases C11, C18, C20 and C21.

**(b) R-ML.**
- Quote, L280: "They are NOT_EVALUATED_BEFORE_FREEZE, so this reads NOT_AVAILABLE."
- Defect:
  - Part 1 must be CONSISTENT, INCONSISTENT or NOT_ADDRESSED, so it is either CONSISTENT or an unregistered NOT_AVAILABLE (C08, C12).
  - Using the ML alternatives to refute R-ML also conflicts with L376: alternatives "never trigger, confirm or refute a PRIMARY reading", with exceptions only for P8 and §6.3.

**(c) R-TSR.**
- Quote, L285: "R-TSR for flagged rows (via P10)".
- Defect:
  - With P13 true and P10 false (Q25 a HIT or INVALID), R-TSR is CONSISTENT (P13 holds) or NOT_ADDRESSED (C10).
  - With Q25 LATE-gated, P10 holds on a row whose prediction is null, and R-TSR reads CONSISTENT. This contradicts L249, "no reading cites an INVALID row" (C18, CONFLICT).

**(d) P9.**
- Quote, L289: "R-DRIFT stays OPEN."
- Defect: R-DRIFT is reported as (CONSISTENT, OPEN) under P9, or not reported (C06, C36).

**(e) DT-T1a.**
- BH-T1a needs r_q, so it can run only after the score, and the classifier has no input for its outcome.
- Part 2 is OPEN, or the trend that L294 says is "reported under both together".

**Fix.** Give each reading one tuple rule, independent of the row that triggers it:
- **R-MF:** part 1 is INCONSISTENT iff N_v(OUTER) ≥ 1 and OUTER is not miss-dominated; part 2 is the E3 line value. Drop the dead R01 against.
- **R-ML:** part 1 is CONSISTENT; print "ML_3p6 NOT_EVALUATED" as prior evidence.
- **R-TSR:** reported only when P10 holds; a LATE row never carries P10.
- **P9:** R-DRIFT is not reported (the E2 NOT_TESTABLE line covers it).
- **DT-T1a:** OPEN in the tuple; the trend in the descriptive lines only.

Put each case in the M-12 suite.

### R2B-07 — SHOULD_FIX — PREREG [C-1.4] L179/L183, [C-1.1] stop list; ROOT_ITEMS M-5: the TSR flags have two sources of truth and no fail-closed stop

**Quotes:**
- L179: "exactly one row is flagged: **NGC3198-Q25**".
- L183: "The flag record … lists the failing rings, the rule above and the flagged ids".

**Defect.**
- **Two sources, no precedence.** The text's id list and the carrier record both state the flagged ids, and nothing says which governs.
- **No stop.** §1.1 has no TSR_FLAG_TABLE_MISMATCH stop. The round-1 refuters asked for one (verify_targetfree_2 §5 R2; verify_fidelity_2 §6.3 and §7.4), and the closure table marks A-02 and B-2 FIXED.
- **No classifier input.** M-5 names no flag input for the M-12 classifier.
- **The support values are not stated.** Codex3's extractor (0618) admits flags only from a support record {lower_kpc, upper_kpc, lower_inclusive, upper_inclusive} (extract_carriers_cx3v005.py L218–236), and r2 never gives those values.

**Evidence.**
- PREREG L120–129 (the stop list), L178–185.
- ROOT_ITEMS L104–112.
- The extractor lines above.

**Fix.**
- Add a stop TSR_FLAG_TABLE_MISMATCH, before targets. It fires if any of these holds:
  - the freeze's pinned compare is not `6f095f64…`;
  - its failing rings ≠ {ordinal 15};
  - the N1 record is not `8867c376…`;
  - the carrier's 43 flags ≠ {Q25}.
- State the support record: ordinal 15; lower 9.901810628740723 kpc, exclusive; upper 10.911721936765339 kpc, exclusive.
- The text's id list governs.
- Add the carrier pin and its flag field to M-5.

### R2B-08 — NOTE — PREREG [C-1.4] L167–170; ROOT_ITEMS M-7 L162: the derived rule's premises are misquoted or uncited, though its result {Q25} is right

**Quotes:**
- L169: "piecewise-linear interpolation of the azimuthal mean onto the 43 manifest radii".
- L167: "The overlap rule is derived, not chosen".
- M-7 L162: "(i) is not a choice."

**Defect.**
- **(a) Misquote.** Slots V003 reads: "HI-weighted mean of R*Omega, then piecewise-linear interpolation of mean onto the supplied 43 manifest radii without extrapolation". The interpolated mean is the vertical HI-weighted column mean; the azimuthal mean is taken earlier.
- **(b) A third premise is uncited.** The "if and only if" also needs the route-B column value at node k to depend only on ring k. I checked it from bytes, and it holds:
  - `owned_free_surface_rotation_v001.py` (`e1b354ec`) forms Ω² column by column (B = Σ w·ρ/h·pr);
  - its derivative matrix D enters only C_RR, the shear;
  - the adapter (`6790e28e`) uses `bisect_left` with weights on nodes j−1 and j, and emits `query_support.radial_support_m`.
- **(c) "Not chosen" overstates.** A66.2 says "within the radial support of a failing TRUNCATION_SHAPE ring". The compare's own `radial_support` is a point, `{"kind": "sampled_ring", "R_kpc": 10.540847…}`, and M-7 lists four options.
- **(d) Edge rings are undefined.** The rule has no form for a failing ring at ordinal 0 or 99.
- **(e) The arithmetic form is unstated.** kpc versus the RUNBOOK's metre authority is not said; both give the same set.

**Evidence.** TSR_RECOMPUTE_R2B_V2.json:
- ring radii equal the GL4 radii_kpc (100/100), and equal radii_m/kpc_m (100/100);
- rule (i) in kpc, in metres, and through the adapter's dependence all give {Q25};
- Q25's weight on ring 15 is 0.216.

**Fix.**
- Quote the slots rule exactly.
- Cite the rotation and adapter modules for column-locality.
- Call the rule "the dependence reading of A66.2's 'radial support' (M-7 option i)".
- Add the end-ring forms: k = 0, R_q ∈ [r_0, r_1); k = 99, R_q ∈ (r_98, r_99].
- State "kpc; the metre form gives the same set".

### R2B-09 — NOTE — PREREG [C-11] L577 (the A65 end-marker `**Lanes.**`): the trailing block is now pinned by nothing

**Quote.** L577: "| A65 | … | `**Lanes.**` | `87e74156…` |".

**Defect.** The pin is right: it matches the bytes on all three V005 reads, and the marker occurs once. But the bytes after the marker are now covered by no pin and no check:
- the span is V005 L1418–1463 at `7f552858`;
- it is the root log of the 0512 N3 ruling, the 0518 contract, Codex2's review and the 0524 withdrawal;
- T5 checks only the cited sections, and T7 only heading numbers.

In round 1 the A65 pin ran to EOF and covered this block (A-18). An edit there would now go undetected. The impact is small, since r2 relies on 0512, 0518 and 0524 through their own dispatch pins.

**Evidence.** V005_PINS_R2B.json and V005_PINS_R2B_2.json: the tail sha is `6fac291817528a458c96ab17f31308cb1ed75e222e80bd5b905b156cd9b1f1bb` at both `cf9bbf19` (L1360–1405) and `7f552858` (L1418–1463); the marker hit is the only one.

**Fix.** Pin the tail as its own row ("A65 tail, from `**Lanes.**` to EOF", with its sha), or list it with its sha in the no-change list, and let T5 check it.

### R2B-10 — NOTE — PREREG [C-I7] L93–94: FREEZE_INCOMPLETE leaves the E3 line and N(Z) unlabelled, and authorizing an incomplete score is a choice made after predictions exist

**Quotes:**
- L93: "Every pattern and reading then carries the label PROVISIONAL (FREEZE_INCOMPLETE)".
- L94: "the envelope rows may be invalid. The NEAR flag then cannot be set".

**Defect.**
- **The E3 line is unlabelled.** It is neither a pattern nor a reading, so whether TESTED-NEGATIVE prints with PROVISIONAL is unstated (C22, C42).
- **"May be" should be "are".** v003g L2087 marks every envelope row invalid when any member is unevaluated.
- **N(Z) is undefined.** In the zone summaries and the E3 line, N(Z) reads 0 or NOT_AVAILABLE (C22).
- **The authorization is a free choice.** Root's authorization to score an incomplete manifest makes it the score of record (I-7), and that choice is made when predictions can be read.

**Fix.**
- The E3 line, the zone summaries and DT-S0G also carry PROVISIONAL.
- NEAR and N(Z) read NOT_AVAILABLE when E_q.valid is false.
- The authorization to score FREEZE_INCOMPLETE is recorded before any step-5 value is read, or the seal fixes the rule.

### R2B-11 — NOTE — ROOT_ITEMS M-5 L106–112 vs the closure of round-1 L-C18(c): the field list still omits fields the rules use

**Defect.** L-C18(c) named six missing fields. r2 added five but still omits `pointwise_envelope.rows[].valid`, which the I-7 NEAR rule needs. It also omits:
- `alternatives[].name`, `role` and `scored`;
- `sensitivity.rows[].valid` and `band_overlaps_error_bar`;
- the flag carrier (R2B-07);
- the LATE list (R2B-03).

The closure table says FIXED.

**Fix.** Add them. "A field named here is missing" is a stop, so the list must be complete.

### R2B-12 — NOTE — PREREG [C-6.1] L375 and [C-6.3] L411; [C-3.2] L271: alternatives and labels

**Defect.**
- **(a) Flags for alternatives.** "Summaries and patterns … use the §2 rules" does not say whether the TSR flag applies to an alternative's rows. This decides P10 for ORIGINAL_K and STAGE0; the N-tests were run on the PRIMARY operator and grid (AMBIGUITY in C27–C31, C34 and C41).
- **(b) TWIN_INPUT_DEFECT.** L411 names only TWIN_INVALID and NOT_DECIDED as leaving R-DRIFT OPEN. This is unreachable under the v003g format, but unruled.
- **(c) The "expected" label.** L271's "(OUTER_FAILURE; expected: A15 E2)" puts E2's expectation, which V004 L38 states as "fall below flat", on P2 and P11 as well. That partly undoes the round-1 B-12 fix.

**Fix.**
- "No TSR flag applies to an alternative."
- Add TWIN_INPUT_DEFECT to the OPEN list.
- Put "expected: A15 E2" on P1 only.

### R2B-13 — NOTE — currency: V005 grew three times during this review

**Defect.**
- V005 went from `991cc242` to `cf9bbf19` (A97, A98) and then to `7f552858` (A99, A100).
- The 14 cited pins still match, but T7 would now FAIL on A97–A100.
- A98.2 rules r2 FAIL; A99 and A100 concern V007 only.

**Fix.** r3 cites A98 and lists A97, A99 and A100 as no-change, per M-6 item 4.

## Source checks with no defect found (refute-by-default, from bytes)

- **TSR derived rule.**
  - The rings equal the GL4 nodes bitwise (100/100).
  - The slots rule is piecewise-linear "of mean" without extrapolation, and the adapter code agrees.
  - The flag set is exactly {Q25}: r14 9.901810628740723 < 10.04 < r16 10.911721936765339, while Q24 at 9.04 < r14 and Q26 at 11.04 > r16.
  - The premise caveats are in R2B-08.
- **The 0550/0512 gate wording (I-6).**
  - "N_PASS licenses nothing by itself. It is an input" matches 0512 L16.
  - The blocking list matches 0550 and A66.3.
  - The compare reads `n_route_ab_gate` OPEN with `TRUNCATION_SHAPE_RESIDUAL_ONLY_A66`.
  - "OPEN for N_PASS" and "BLOCKED for N_INCOMPLETE/N_NO_RUN" are inferences, but the binding sentence is keyed to the field.
- **The receipt rule's sources.** A65.2 ("If they cannot finish before the freeze … NOT_EVALUATED_BEFORE_FREEZE … never delays the headline") and the slots `evaluated_status_transition` are both consistent with its intent (defects in R2B-04).
- **The timing rule's sources.**
  - A60: "seals the prereg before targets are opened, in the freeze step";
  - A47 I3: validity/admissibility booleans only;
  - A80: "Step 5 is more than a day away".
  - Codex2 0490's SHOULD_FIX on the late-seal fallback pins is not repeated here.
- **The A65 end-marker pin.** It equals the bytes on all three reads, and the marker is unique (tail caveat in R2B-09).
- **Codex1 0032, M_s 96.** GQ_NGC at M_s 96 against 192 on [2, 91] /kpc: max/P0 1.219e-15 and the every-kperp bound 2.335e-14, both below 1e-12; verdict PASS. This matches I-6 and A81 RI-23 (`be148bab…`).
- **Other checks:** A52.4, A81 RI-22 (θ/20), A90 (OPEN; LO I1-T NOT_RUN), and the A63/A65 numbers in D-1 and D-2 all match.

## Steerability (choices left after predictions exist, or after targets are opened)

| choice | when | status |
|---|---|---|
| NOT_READ with no condition | after targets | open (R2B-02) |
| STAGE0 successor adoption and admission code; the step-4/step-8 cut-off | after predictions | open (R2B-04) |
| LATE status of each gate | after predictions | not mechanical (R2B-03) |
| Sign class of a zone set by its hits when its misses are unsigned | at the score | defect (R2B-01) |
| Authorizing a FREEZE_INCOMPLETE score as the score of record | after predictions | open (R2B-10) |
| Late-seal fallback pins | after predictions | Codex2 0490 SHOULD_FIX |
| Zone cuts, tiers, TSR ids, K_big, M_s, first-score rule, post-score readings | — | closed |

## Tested and not tested

- **Tested,** on 48 synthetic v003g-format outputs:
  - ties at N_v/2; N_v = 0; all-INVALID zones; a null ratio;
  - NEAR straddle and NOT_AVAILABLE;
  - OUTER_FAILURE of each sign and UNDEFINED; all three E3 values;
  - P11, P12 and P13, and coverage;
  - LATE gates (all and partial) and an unknown LATE status;
  - Q25 as a HIT, a MISS, early-gate INVALID and LATE;
  - a valid twin and TWIN_INVALID, for ORIGINAL_K and STAGE0;
  - DT-S0G at each boundary (CONSISTENT, the AGAINST tie, NOT_DECIDED twice, no qualifying rows, TWIN_INVALID, not evaluated) and with LATE PRIMARY rows;
  - FREEZE_INCOMPLETE, with and without P8;
  - four pre-score stops;
  - |r| = 1 exactly; a valid sensitivity column.
- **Also tested:** the module-helper cross-check, the V005 pins, and the TSR recompute.
- **Not tested:** real score outputs or any target; Claude4's target-free checker; Codex1's rehearsal classifier (not run); the BH-T1a prereg.

## Files in this folder

- PARTIAL.md, REVIEW.md, HASHES.txt;
- CASES_R2B_V2.json, and CASES_R2B.json (superseded);
- TSR_RECOMPUTE_R2B_V2.json, and TSR_RECOMPUTE_R2B.json (identical content, from the first run);
- V005_PINS_R2B.json (`cf9bbf19`) and V005_PINS_R2B_2.json (`7f552858`);
- tools/: classify_r2b.py, synth_r2b.py, run_cases_r2b.py, run_cases_r2b_v2.py, v005_pins_r2b.py.
