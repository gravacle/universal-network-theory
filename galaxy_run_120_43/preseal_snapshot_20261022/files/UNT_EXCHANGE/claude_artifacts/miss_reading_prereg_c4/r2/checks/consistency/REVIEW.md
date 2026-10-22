# REVIEW — Lens C (rule consistency and steerability): miss-reading prereg r2, round 1

**Lens C**, a refute-by-default check run by a helper of lane Claude4 (dispatch 0592, under 0585). Written 2026-10-18 (UTC; see PARTIAL.md for the clock stamps). This lens edits nothing; Claude4 owns the fix round.

**Verdict: FAIL** — 1 BLOCKING, 12 SHOULD_FIX, 14 NOTE.

## Object (verified from bytes; all match HASHES_R2.txt)

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` |
| CLAUSE_SOURCE_MAP_R2.md (CSM) | `b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b` |
| ROOT_ITEMS_R2.md | `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f` |
| NUMBER_PROVENANCE_R2.json | `c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832` |
| TARGET_FREE_CHECK_R2.json | `aab683236116bc3562df86f3b9542a54eec3446c44a8f0e5569ff2b305d2180b` |
| TARGET_FREE_MUTATION_TEST_R2.json | `2a8202b823beb5cd0bc03c9e1e2b0377d9de59410a698c8d185f39739d66bc41` |
| tools/check_target_free_c4v001.py | `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7` |

**V005 as read** (2026-10-18T18:50:50Z): `0753f2d8dc437592a4ad70140f309c774837cb07e9c04e2c213c4421eeb8e87e`. A90 and A91 were added after assembly; r2 assembled at `17cb4fd4…`, last entry A89. All 11 cited section pins still match the current bytes (`v005_section_pins_out.json`).

**Other sources read:**
- V004 `487d4449…` (A14–A17, A20–A23, A41);
- V003 `5bef6552…` (A10, A12);
- v003g module `48a1e48a…`, slots V003 `d3859b42…`, RUNBOOK_V001 `9557b5aa…`;
- V001 `6aecf0cb…`;
- dispatches 0512, 0518, 0522, 0531, 0535, 0545, 0546, 0548, 0550, 0585, 0592, 0594 and 0603.

**Not read:** no NGC3198 target, observed velocity, rotmod/Vobs/MassModels/SPARC file, runs_ext path or UVT_* item was opened. Nothing was launched.

## Method

1. **An independent classifier** (`tools/lensc_classifier.py`), written from the r2 text §0–§6 only. Where the text gives no unique answer, it records an AMBIGUITY event; where two clauses or a cited source disagree, a CONFLICT; where a reachable outcome is covered by no rule, a GAP. It never chooses silently.
2. **Synthetic score outputs in the v003g `score_after_freeze` format** (`tools/lensc_synth.py`). The generator replicates `_ladder_row`, `_score_members`, `_score_members_on_rows`, `_pointwise_envelope` and `_band_rows`. These replicas were cross-checked against the module's own pure helpers: **200 comparisons, 0 mismatches** (`FORMAT_CROSSCHECK.json`).
   - The radii are the target-free slots V003 query block (sha checked).
   - Every velocity and σ is a synthetic number.
3. **38 cases** (`tools/lensc_cases.py`, results in `CASES_RESULTS_V2.json`; `CASES_RESULTS.json` is the superseded first run). All 38 behave exactly as the r2 text dictates. One extra probe is in `INNER_CENTERED_PROBE.json`.
   - The cases cover every edge case asked for: all-INVALID zones; N_v = 0; a zero residual; even and odd counts; m(TRANSITION) undefined under P1g; no twin and an invalid twin; STAGE0 evaluated and not evaluated at each comparison boundary; FREEZE_INCOMPLETE; flagged HIT, MISS and INVALID rows; NEAR rows; and sensitivity-only overlap.
4. **A cross-file mechanical check** (`tools/crossfile_lensc.py`, results in `crossfile_out.json`).

## Findings (most severe first)

### L-C01 — BLOCKING — PREREG [C-P] vs [C-3.2] vs [C-8]: R-MF TESTED-NEGATIVE, the one registered verdict, has two triggers that disagree on reachable outcomes

**Quotes:**
- [C-P] L17: "Under A15 E3 an outer-row failure is TESTED-NEGATIVE for exactly the present-mass-only lapse response of the L = 4 coefficient method, at the A2 grid and the calibrated θ."
- [C-3.2] L195, R-MF: "If P1 holds, this is TESTED-NEGATIVE for exactly this scope. | P1 holds | no P1 with N_v(OUTER) ≥ 1 |".
- [C-3.2] L200, P2: "**R-MF**, with the opposite sign: overshoot."
- [C-8] L347: "'TESTED-NEGATIVE' only for R-MF, within its stated scope".

**Defect.** C-P, following the binding A15 E3, makes any outer-row failure TESTED-NEGATIVE. C-3.2 grants the verdict only under P1 (miss-dominated **and** DEFICIT). The two disagree in three ways:
- **(a) Under P2,** the text does not say whether R-MF is TESTED-NEGATIVE. R-MF is also "consistent" (P2 row) and "against" (P1 row) at the same time.
- **(b) With OUTER miss-dominated and S(OUTER) = CENTERED** (misses of both signs), no pattern holds at all:
  - P1 and P2 need a sign class;
  - P5 needs INNER hit-dominated and TRANSITION not hit-dominated;
  - P7 needs "no zone miss-dominated".

  So 8/8 outer misses can yield no pattern, no reading and no verdict.
- **(c) The P1-row against-condition** ("no P1") can never be true while that row is being reported.

After the targets are opened, the reporter can choose whether the verdict applies.

**Evidence.**
- V004 A15, L43–44: "E3, how a failure is read. This is binding… An outer-row failure would be TESTED-NEGATIVE for exactly this".
- Case C08: OUTER r = −3, +3, −2.5, +2.5, −2, +2, −1.5, +1.5; M = 8, m = 0.0, S = CENTERED. Patterns: [P0] only, plus a GAP event and CONFLICT 'C-P vs C-3.2'.
- Case C12: OUTER excess. Patterns [P0, P2]; R-MF candidates are ['consistent', 'inconsistent']; TESTED-NEGATIVE per C-3.2 is false.
- Case C32: P6 global excess shows the same conflict.

**Fix.** Use one sign-agnostic trigger:
- "R-MF is TESTED-NEGATIVE (A15 E3 scope) iff OUTER is miss-dominated (N_v(OUTER) ≥ 1); the sign class is reported with the verdict."
- Replace the P1-row against-condition with "OUTER not miss-dominated, with N_v(OUTER) ≥ 1".
- Add **P11 OUTER_MIXED** (OUTER miss-dominated and S(OUTER) = CENTERED), carrying R-MF (TESTED-NEGATIVE), R-NAX and R-DRIFT.
- Make C-8 point to this trigger. Root rules under M-3.

### L-C02 — SHOULD_FIX — PREREG [C-3], [C-3.2], [C-8] item 5; ROOT_ITEMS M-4: a reading's status is not unique

**Quotes:**
- L168: "The 43-row score can make a reading **consistent** or **inconsistent**."
- L169: "A reading whose deciding test has not run stays OPEN, whatever the score shows."
- L340: "each with the status consistent, inconsistent or OPEN".
- L196, R-UT1 against-column: "A41 item 3 (FORMAL + TESTED) already registers that no gate-consistent typing gives an attractive tail…".
- L207, R-TSR against-column: "Route B consumes the azimuthal mean, so the φ-spread S enters no row directly (A66.2; A42 TESTED)."

**Defect.** C-8 asks for one of three words, but several conditions hold at once and no precedence is given:
- **(i)** Every untested reading of a pattern that holds is both "consistent" (from the score) and "OPEN" (its deciding test has not run). This applies to R-HIST, R-REACH, R-S1, R-GRID, R-GEFF, R-ML, R-SPEC, R-GEO, R-NAX and R-TSR, and to R-DRIFT when DT-S0G is not evaluated.
- **(ii)** R-UT1 and R-TSR also meet their against-condition already, through facts registered before the score (A41 item 3; A66.2). So each is consistent, inconsistent and OPEN at once.
- **(iii)** Under P1 with DT-S0G AGAINST, R-DRIFT is both consistent and inconsistent.

The reporter picks the word.

**Evidence.**
- C01: R-UT1 → ['consistent', 'inconsistent', 'OPEN']; R-HIST → ['consistent', 'OPEN'].
- C16: R-TSR → ['consistent', 'inconsistent', 'OPEN'].
- C21: R-DRIFT → ['consistent', 'inconsistent'].
- Across the 38 cases, 110 AMBIGUITY 'C-3/C-8' events.

**Fix.** Print every reading as a fixed tuple, never as one word:
- the score relation: consistent | inconsistent | not addressed;
- the deciding-test status: OPEN | that test's registered outcome;
- the against-evidence registered before the score, named by entry (for example, A41 item 3; A66.2).

Require the full tuple for every reading of every pattern that holds.

### L-C03 — SHOULD_FIX — PREREG [C-I6]; CSM C-I6: 0512 is misread, and the clause conflicts with A66.2 and with the outcome now recorded in A90

**Quotes:**
- L56: "Under the 0512 ruling logged in V005, only N_PASS is an input to route A/B. So any other outcome, such as N_INCOMPLETE or N_NO_RUN, also gives no route-A/B run."
- L57: "With no route-A/B run there is no score, and this document is not applied."
- CSM L21: "(N_PASS is the only input to route A/B)".

**Defect.** 0512 says N_PASS licenses nothing **by itself** and is an input. It does not say that N_PASS is the **only** input. Read literally, "any other outcome" includes N_FAIL_N1, which A66.2 (and L54 of this same clause) lets through. A90 records that N_FAIL_N1 is the actual outcome, with the gate OPEN. A literal reader could therefore argue that this document "is not applied".

**Evidence.**
- 0512 L16: "`N_PASS` licenses nothing by itself. It is an input to the NGC route-A/B step."
- V005 L1245: "N_PASS is only an input to NGC route A/B."
- V005 L634: "N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block NGC route A/B."
- V005 L913 and L916: "N_FAIL_N1, tests_read = true" … "Under A66 the route A/B gate reads OPEN, for the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66."
- 0550 L14: "Add a field `n_route_ab_gate: OPEN|BLOCKED`".

**Fix.** Key the clause on the compare's gate field:
- "Route A/B runs only if the NGC N-test compare's `n_route_ab_gate` reads OPEN: N_PASS, or N_FAIL_N1 confined to TRUNCATION_SHAPE rings (A66.2)."
- "Every other outcome blocks it: N_NO_RUN, N_INCOMPLETE, or any other N_FAIL_* (A66.3; 0512)."

Cite A90 for the outcome at writing, and correct the CSM paraphrase.

### L-C04 — SHOULD_FIX — PREREG [C-2] (and the [C-9] row "Choosing which pattern to report"): the pattern set has holes

**Quotes:**
- L147: "every one that holds is reported… no pattern can mask another."
- L158: "P7 | SCATTERED | at least one MISS, and no zone miss-dominated".
- L159: "P8 | NO_MISS | M = 0 over all non-INVALID rows".

**Defect.** Beyond the OUTER case of L-C01, three more holes exist:
- **(a)** A TRANSITION-only failure matches no pattern. No TRANSITION pattern exists, P5 needs OUTER miss-dominated, and P7 needs no zone miss-dominated.
- **(b)** INNER miss-dominated with S(INNER) = CENTERED matches no pattern.
- **(c)** P8 has no N_v ≥ 1 guard, so it holds vacuously when every scored row is INVALID. This is reachable for the 8-row STAGE0 scope through §6.1.

No pattern masks another, but some failures get no reading at all.

**Evidence.**
- C09: TRANSITION 11/11 misses → patterns [P0] only.
- `INNER_CENTERED_PROBE.json`: INNER 12/22 misses of mixed sign, m = 0.2 → [P0] only.
- C24: STAGE0 P8 holds vacuously (GAP).

**Fix.** Add P12 TRANSITION_MISS and P13 INNER_MIXED, each with registered readings. Alternatively, add one catch-all pattern, "UNPATTERNED: a zone is miss-dominated and no zone pattern covers it", that carries that zone's readings. Add "N_v ≥ 1 over the scored rows" to P8.

### L-C05 — SHOULD_FIX — PREREG [C-2]; ROOT_ITEMS M-3: at exactly half, a zone is both miss-dominated and hit-dominated

**Quotes:**
- L138: "Miss-dominated: N_v(Z) ≥ 1 and M(Z) ≥ N_v(Z)/2."
- L139: "Hit-dominated: N_v(Z) ≥ 1 and H(Z) ≥ N_v(Z)/2."
- M-3 L77: "The clarifications close tie and vacuous-truth cases that could otherwise be argued after targets."

**Defect.** When N(Z) = 0 and H = M = N_v/2, both predicates hold. Two consequences:
- P1, and with it R-MF TESTED-NEGATIVE, holds while half the OUTER rows are hits;
- P3/P4 (INNER miss-dominated) hold together with P5 (INNER hit-dominated, read as the "onset of the finite-reach deficit").

**Evidence.**
- C10: OUTER 4 HIT and 4 MISS, m = −1.4 → both predicates true; P1 and TESTED-NEGATIVE.
- C11: INNER 11 rows at r = 0.99 and 11 at r = 1.2, m = 1.095 → P3 and P5 together.

**Fix.** Keep miss-dominated at M ≥ N_v/2 (the stricter side), and make hit-dominated strict: H > N_v/2. Correct M-3.

### L-C06 — SHOULD_FIX — PREREG [C-1.1]; ROOT_ITEMS M-1: the registered meaning of NEAR is false for a pointwise envelope

**Quotes:**
- L84: "What NEAR means. Some admitted representative member state reaches the error bar, but the frozen reference member does not."
- M-1 L30: "(c) discards real information: whether some admitted state reaches the error bar."

**Defect.** The envelope is a per-row min/max over the valid members. If the members straddle the error bar, `band_overlaps_error_bar` is true although no member is within error. The gloss over-states what NEAR shows, and so does M-1's reason for choosing option (a).

**Evidence.**
- v003g L2081–2087: the band is the min/max over members with row_valid.
- v003g L4104: the overlap test.
- C06: at Q40 the members sit at r = −2.0, −2.3, +2.0 and +2.4 → NEAR, with no member within error (CONFLICT 'C-1.1 / M-1'). At Q41, where one member sits at −0.5, NEAR has a member within error and no event fires.

**Fix.** Choose one:
- define NEAR as "some PRIMARY member has `within_error` true at q" (readable from `members[*].rows`); or
- keep the envelope test and change the gloss to "the frozen PRIMARY pointwise envelope interval meets the error bar; no single member need be within error".

Correct M-1 to match.

### L-C07 — SHOULD_FIX — PREREG [C-1.1] vs [C-8]: the sensitivity band "is only reported", but the report format has no place for it

**Quotes:**
- L87: "The box-limited sensitivity band (`sensitivity.rows`) is never used for a tier. It is conditional on trial values and is only reported."
- L337: "The per-row table: Q_id, zone, R_q, tier, r_q, sign, NEAR flag, TRUNCATION_SHAPE_RESIDUAL flag with its S/θ, and INVALID reason."

**Defect.** Nothing fixes where, for which rows, or in what form the band is reported. After the targets are opened, it could be shown only where it "rescues" a miss. This is selective emphasis permitted by an unformatted reporting clause.

**Evidence.** C07: Q42 is a MISS; the envelope (−3.2σ to −2.8σ) does not overlap the error bar, but the sensitivity band (−3.5σ to −0.5σ) does. Event: AMBIGUITY 'C-1.1 vs C-8'.

**Fix.** Choose one:
- add a fixed column for all 43 rows: "sensitivity band overlaps: yes / no / invalid", labelled conditional on trial values, never a tier and never cited by a reading; or
- state that the band is not part of this reading.

### L-C08 — SHOULD_FIX — PREREG [C-6.1], [C-6.3]; ROOT_ITEMS M-10: the twin rule rests on a premise the v003g bytes contradict, and four of its cases are unruled

**Quotes:**
- M-10 L196: "Whether ORIGINAL_K's members share log_index values with the PRIMARY's is known only after the freeze. NO_TWIN handles the case where they do not."
- L271: "If there is no twin, or the twin is not valid, the alternative reads NO_TWIN."
- L270: "The twin's rows are classified INVALID_AS_MISS, HIT or MISS by M-T".

**Defect.**
- **(a)** The v003g writer and verifier require every evaluated alternative's members to equal the PRIMARY's selected representatives (log_index, role and order). A twin therefore always exists: "no twin" is unreachable, and the uncertainty M-10 states is false.
- **(b)** "Not valid" names no field. `member_valid`, `evaluated` and the row statuses can disagree.
- **(c)** M-T's fail-closed id check ("not Q01 to Q43 in order") fires on the 8-row STAGE0 twin.
- **(d)** Two cases are unruled: an evaluated STAGE0 whose twin reads NO_TWIN, and the R-DRIFT status after a NOT_DECIDED comparison.

**Evidence.**
- v003g L3644–3647: "…members %s are not exactly the selected representatives … (log_index, role, order)".
- v003g L3184–3185: the same check in the verifier.
- C18: a forced log_index mismatch, which v003g refuses at the freeze, reads NO_TWIN.
- C17 and C25: AMBIGUITY 'C-6.1' (evaluated True, member_valid False); C25 also gives AMBIGUITY 'C-6.3'.
- C20–C24, C37 and C38: CONFLICT 'C-6.1 vs C-1.1'.
- C22, C24 and C25: AMBIGUITY 'C-3.2/C-6.3'.

**Fix.**
- Correct M-10.
- Define a valid twin as `member_valid = true`.
- Apply the C-1.1 id-order stop to the PRIMARY only. The twin's ids must equal `scoring_scope.query_ids` (STAGE0) or Q01–Q43 (full-row alternatives).
- Add: "If STAGE0 is evaluated and its twin is NO_TWIN, or the comparison reads NOT_DECIDED, R-DRIFT stays OPEN."

### L-C09 — SHOULD_FIX — PREREG [C-3.2]: several against-conditions use undefined terms

**Quotes:**
- L200: "ORIGINAL_K shows the same excess (against R-GRID)".
- L201: "the DT-T1a M/L variants do not move the inner rows by the miss".
- L202: "An onset radius inconsistent with k* … is reported, as a comparison only."
- L204: "otherwise R-MF at row level".
- L205: "ORIGINAL_K and the A17 C3 grid record agree. Agreement is reported".

**Defect.** These terms have no definition:
- "the same excess": same rows, same sign class, or the twin's P2?
- "by the miss": by what measure?
- "onset radius" and "inconsistent with k*";
- "otherwise": in which case?
- "agree": on what? And what is reported if they disagree?

Three conditions also rest on a premise that does not hold:
- ORIGINAL_K is an entropy-K state alternative, not a k-grid alternative.
- DT-T1a's M/L variants vary f★ for a correlation; they do not move any prediction. The M/L prediction alternatives are NOT_EVALUATED_BEFORE_FREEZE.
- The P5 condition sits in the against-column, yet it is "reported, as a comparison only".

**Evidence.**
- slots V003 L11: "entropy_K_factor 1.0 … instead of 64/121".
- PREREG L183: DT-T1a is "the residual against the target-free stellar fraction f★".
- Cases C12, C34, C35, C33 and C06 give AMBIGUITY 'C-3.2' events.

**Fix.** Define each term, or remove the condition:
- "ORIGINAL_K shows the same excess" := the ORIGINAL_K twin's §6.1 patterns include P2. Give R-GRID's link to it a reason, or drop the link.
- R-ML: "the ML_3p6 alternatives, if evaluated, leave every INNER MISS a MISS; otherwise R-ML stays OPEN".
- P5: move the k* item to a descriptive line, with onset radius := the smallest R_q of a MISS row in TRANSITION ∪ OUTER.
- P7: report both R-NAX and R-MF always.
- P8: define "agree", and say what is reported on disagreement.

### L-C10 — SHOULD_FIX — PREREG [C-I6] vs [C-3.2]: "the only registered numerical reading is R-TSR", yet R-GRID is a numerical reading tied to a superseded record

**Quotes:**
- L61: "No reading attributes a miss to a certified numerical quantity. The only registered numerical reading is R-TSR (§3), which A66 created."
- L200: "R-GRID: k-grid fidelity at outer radii (A17: C3 is the criterion that matters)", with the deciding test "the A17 C3 record".

**Defect.** Either R-GRID is a second numerical reading, which contradicts L61, or it attributes a miss to numerics that are now certified (A90: N0, NQ, N2 and N3′ pass), which contradicts the first sentence. Moreover, the A17 C3 record concerns A17's tier-1 grids, all of which failed; it is not a record of the production numerics. This part was not brought up to date for A64/A66, as 0585 requires.

**Evidence.**
- V004 L74: "All four tier-1 grids fail C1, C2 and C3".
- V004 L90.
- V005 L914.
- C12: CONFLICT 'C-I6 vs C-3.2'.

**Fix.** Remove R-GRID and the P8 "A17 C3" check. Or re-register R-GRID against a production record (the K32 N-test compare) and amend L61.

### L-C11 — SHOULD_FIX — ROOT_ITEMS M-6 item 3; PREREG [C-11]: the later-entry rule covers V006 only, but V005 is still open and has grown

**Quotes:**
- M-6 L122: "Any V006 entry made before target access that touches the reading needs either a revision of this text or an explicit no-change note in the seal entry."
- L433: "read with no change to this text: A61, A67–A69, A71–A80 and A83–A89".

**Defect.** V005 stays open until the V007 freeze (A82) and has gained A90 and A91 since assembly. A90 records:
- the K32 N-test outcome: N_FAIL_N1, with the A/B gate OPEN;
- LO_NGC_K32_CERT_V001 (07745bbf), with coverage to 91;
- an open step-5 root item.

These facts bear on C-I6, C-1.4, D-3 and D-4. Neither M-6 nor §11 covers V005 entries after A89, and a seal check that only confirms the cited entries are present would not notice them.

**Evidence.**
- V005 at 18:50:50Z hashes to `0753f2d8…`.
- V005 L890 is "## A91"; L904 is "## A90"; see L913–917.
- The 11 cited section pins still match.

**Fix.** M-6: "any root entry after A89, in V005 or V006, made before target access". The fix round cites A90 in C-I6 and C-1.4, and lists A91 as no-change.

### L-C12 — SHOULD_FIX — CSM, PREREG [C-11], ROOT_ITEMS M-6/M-8: the cited-entry lists disagree

**Quotes:**
- CSM L66: "A61, A62, A67–A80 (… does not alter how rows are read);"
- CSM L67: "A83–A88".
- PREREG L424 pins A62; L429 pins A70; L433 lists A89 as no-change.
- CSM L22 and M-8 L161 cite "A50".

**Defect.**
- The CSM calls A62 and A70 "no change", though the PREREG cites and pins both, and the CSM's own C-4 row cites A62.
- The CSM omits A89.
- A50 is used as a source (C-I7, M-8) but is neither pinned in §11 nor in the M-6 seal-check list. §11's "every other V005 entry … was used there through V001's citations" is false for A50.

**Evidence.**
- `crossfile_out.json`: entries used but not pinned include A50.
- V001 §9 cites V005 only for "A48 principle, 0518 / A55 log".

**Fix.** Keep one list, in the PREREG, and quote it in the CSM. Pin A50 and add it to M-6, or drop the analogy.

### L-C13 — SHOULD_FIX — PREREG [C-1.1], [C-1.3]: the fail-closed stops leave root an unconstrained ruling after targets are opened

**Quotes:**
- L93: "Root then rules before any reading is reported. The score stands as computed."
- L117: "…the classification stops with ZONE_TABLE_MISMATCH, and root rules."

**Defect.** Every stop condition is target-free (field presence, row order, status, radii by id) and could be checked before any target is opened. The text does not require that, and it puts no limit on what root may rule after seeing the targets.

**Evidence.** C29–C31 reproduce the stops on synthetic data, using only ids, radii and field presence.

**Fix.** Run every stop check before target access: the frozen manifest plus slots, through the sealed M-12 classifier on a synthetic score built from the frozen member arrays. Record the result in the seal entry. After the targets are opened, root may only correct a field map, with no value changing, or declare the classification NOT_READ. Root may never change a tier, zone, pattern or reading rule.

### L-C14 — NOTE — [C-2] P10 vs [C-4]

L161 reports "the tier of every flagged row, hits included", while L243 excludes INVALID rows "from every pattern except P0 and P9".
- Evidence: C16 (Q27 is flagged and gate-INVALID).
- Fix: "every non-INVALID flagged row; an INVALID flagged row is listed with its roster reason only".

### L-C15 — NOTE — [C-5.2] "Report P1/P1g/P2/P8/P9 for OUTER" (L257)

P8 is a global pattern. When OUTER has no misses but another zone does, nothing marks OUTER as running against E2.
- Evidence: C09, C13, C16 and C34 (AMBIGUITY 'C-5.2').
- Fix: define OUTER_NO_MISS := N_v(OUTER) ≥ 1 and M(OUTER) = 0, and use it for E2.

### L-C16 — NOTE — [C-1.1]/[C-I7]: under FREEZE_INCOMPLETE with an unevaluated PRIMARY member, every envelope row is invalid

v003g L2087 requires n_uneval == 0 for a valid envelope row. So NEAR silently becomes impossible, and NEAR candidates read MISS.
- Evidence: C14.
- Fix: when E_q.valid is false on a non-INVALID row, report NEAR as NOT_AVAILABLE, and say so in the PROVISIONAL label.

### L-C17 — NOTE — report-format wording

- (a) D-2 (L317) puts the uncertainty "in every row's notes", but the C-8 per-row table (L337) has no notes column.
- (b) D-1 (L308) and DT-U12 (L182) use "TESTED-NEGATIVE" for the stage-0 outcome, while L347 allows that word "only for R-MF".
- (c) L343 labels STAGE0 "SENSITIVITY" even when it is NOT_EVALUATED.

Fix: add a notes column; add a quoting exception for D-1 to the words rule; label STAGE0 by its actual status.

### L-C18 — NOTE — [C-I4]/[C-6.2]; ROOT_ITEMS M-5: lists that do not match the score output

- (a) In the fixed-distance mode, v003g appends a seventh alternative, DDO154_DISTANCE_NUISANCE (L4295–4299), which the text never names (C27).
- (b) A16.2 (V004 L60) can turn ORIGINAL_K into NOT_EVALUATED, which would leave the R-GRID and P8 checks unruled.
- (c) M-5's field list omits `reference_member_log_index`/`log_index`, `member_valid`, `freeze_status`, `incomplete_reasons`, `pointwise_envelope.rows[].valid` and `sensitivity.rows`.

Fix: name all of these.

### L-C19 — NOTE — [C-1.1]: a VALID row can carry a null `sigma_ratio`

This happens in v003g (L4016–4020, NON_FINITE_SIGMA_RATIO) even with a finite σ > 0. The fail-closed list names only a missing field.
- Evidence: C28 (synthetic σ = 5e-324).
- Fix: add this case to the stops.

### L-C20 — NOTE — [C-1.1] vs [C-4]: L79 says INVALID_AS_MISS holds "exactly when … one of the three registered reasons"

v003g also scores gate-registered rows INVALID_AS_MISS (L4042), as C-4 itself says (L216–218).
- Evidence: CONFLICT 'C-1.1 vs C-4' in C02, C04 and C16.
- Fix: add "or a root-listed gate reason".

### L-C21 — NOTE — [C-1.4] vs ROOT_ITEMS M-7: is the flag record a list of rows or of rings?

L126 describes a list of rows. M-7 (L136–140) and 0550 L11 ("list the failing TRUNCATION_SHAPE rings … flags the overlapping rows") describe a list of rings plus an overlap rule.
- Fix: put the closed-interval rule into §1.4, state its arithmetic (kpc, or the RUNBOOK's metre form), and register the derived list of rows before any target is opened.

### L-C22 — NOTE — ROOT_ITEMS M-1 L35 "…and from P7"

P7 (L158) does not use NEAR.
- Fix: delete the reference.

### L-C23 — NOTE — [C-3] L171–174 scopes

Scopes are defined only for R-TSR and R-DRIFT, so for every other reading "cite only rows inside its own scope" is vacuous.
- Fix: give each pattern's readings a row scope.

### L-C24 — NOTE — [C-P] L21 "less favourable to any adopted hypothesis"

No reading is adopted (A20: "Neither UT-1 nor BH-D is adopted"), so this gap-filler has nothing to act on for reading statuses.
- Fix: state it operationally: the larger MISS count; UNDEFINED over a value; OPEN over consistent; NOT_DECIDED over CONSISTENT.

### L-C25 — NOTE — [C-1.1]/[C-2] L85: NEAR "is not counted as a miss in §2"

NEAR rows, including straddle rows (L-C06), lower M(Z) and can suppress P1–P4, and with them the R-MF verdict.
- Fix: also report the miss-dominance test with NEAR counted as MISS, labelled as such.

### L-C26 — NOTE — [C-9]: the self-check over-claims

The self-check lists as closed risks that L-C01, L-C02, L-C07, L-C09 and L-C13 leave open. It also never rules on a STAGE0 result that first becomes available after the freeze.
- Fix: add those rows, and add "never compared under this text; R-DRIFT stays OPEN".

### L-C27 — NOTE — behaviour that follows from registered choices (M-3, M-9), recorded so that root rules knowingly

- C36: a single valid OUTER row (the other seven cut) carries P1 and TESTED-NEGATIVE.
- C37: a STAGE0 twin that turns the deficit into an excess, with one row crossing the error bar, reads CONSISTENT.
- C38: a twin that shrinks every deficit from −6σ to −1.5σ but gains no hit reads AGAINST.

Fix: report N_v and I next to every verdict. Consider requiring S_S ∈ {S_P, CENTERED} for CONSISTENT.

## §9 self-check against what the rules allow

| §9 risk | closed? |
|---|---|
| Zone boundaries | Yes: membership is fixed by id, and C29 stops on a mismatch. The ruling after a stop is open (L-C13). |
| Redefining HIT or NEAR | The tier test is closed; NEAR's stated meaning is wrong (L-C06). |
| Choice of member | Closed. The twin always exists (L-C08 corrects M-10). |
| Choice of pattern | Masking is closed. Coverage and the reading-status choice are open (L-C01, L-C02, L-C04, L-C05). |
| Upgrading "consistent" to "supported" | Closed by the words rule. The choice between "consistent" and "OPEN" is open (L-C02). |
| Re-explaining INVALID rows | Closed, except that P10 lists INVALID flagged rows (L-C14). |
| Readings added afterwards, dropped rows, inflated σ, withdrawn tests | Closed. |
| STAGE0 "only if it helps" | Adoption before the freeze is closed. A result arriving after the freeze, and an evaluated STAGE0 with NO_TWIN, are unruled (L-C26, L-C08). |
| TSR flags after misses | Closed if M-7 is adopted; the record's shape is inconsistent (L-C21). |
| K_big, M_s, certificates | Closed. A90 must be integrated (L-C11). |
| Incomplete freeze | The label is closed; NEAR is lost silently (L-C16). |
| Not listed in §9 at all | Sensitivity-band reporting (L-C07), undefined against-terms (L-C09), and root rulings after targets are opened (L-C13). |

## Cross-file consistency

- All 30 clause tags map both ways between the PREREG and the CSM, with no duplicates.
- Root items M-1 to M-12 are numbered consistently in the PREREG and ROOT_ITEMS.
- The inconsistencies are L-C08 (the M-10 premise), L-C11, L-C12, L-C21 and L-C22.

## Tested and not tested

- **Tested:** every rule in §1–§6, on 38 synthetic v003g-format outputs plus one probe. The format fidelity of the synthetic outputs against v003g's own helpers. The V005 section pins against the current bytes. The cross-file lists.
- **Not tested:** real score outputs; any target. Claude4's own target-free checker and generator (other lenses). The semantics of the BH-T1a prereg (not opened, to avoid any data table).

## Files in this folder

PARTIAL.md, REVIEW.md, HASHES.txt, FORMAT_CROSSCHECK.json, CASES_RESULTS.json (first run, superseded), CASES_RESULTS_V2.json, INNER_CENTERED_PROBE.json, crossfile_out.json, v005_section_pins_out.json, and in tools/: lensc_classifier.py, lensc_synth.py, lensc_cases.py, crossfile_lensc.py, v005_section_pins_lensc.py.
