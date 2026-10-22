# PARTIAL — Lens C (rule consistency and steerability), miss-reading prereg r2 round1

started: 2026-10-18T18:48:27Z; updated: 2026-10-18T19:01:35Z
object hashes verified from bytes (all 9 match HASHES_R2.txt).
V005 read at 0753f2d8dc437592a4ad70140f309c774837cb07e9c04e2c213c4421eeb8e87e (A90, A91 added after assembly at 17cb4fd4…); all 11 cited section pins still match (tools/v005_section_pins_lensc.py -> v005_section_pins_out.json).
Sources read: v003g module (score format), slots V003 (alternatives, query block), RUNBOOK_V001, V001, V003 A10/A12, V004 A14-A17/A20-A23/A41, V005 A47-A91, dispatches 0512 0518 0522 0531 0535 0545 0546 0548 0550 0585 0592 0594 0603.

## status (2026-10-18T19:13:33Z)
- classifier built (tools/lensc_classifier.py), synthetic generator cross-checked against v003g helpers (FORMAT_CROSSCHECK.json: 200 comparisons, 0 mismatches)
- 38 synthetic cases run: 38/38 behave as the r2 text dictates (CASES_RESULTS.json); events confirm the candidate findings below
- next: cross-file mechanical check, then REVIEW.md

## candidate findings (to be confirmed by the classifier / bytes)
- B? R-MF TESTED-NEGATIVE trigger: C-P "an outer-row failure" (sign-agnostic, A15 E3) vs C-3.2 "If P1 holds"; P2 silent; OUTER miss-dominated + CENTERED has no pattern.
- SF reading status single-valued (consistent/inconsistent/OPEN) vs rules; R-UT1 against already true (A41 item 3).
- SF C-I6 "only N_PASS is an input" misreads 0512 ("N_PASS licenses nothing by itself"); conflicts with A66.2 and A90 (N_FAIL_N1, gate OPEN).
- SF NEAR gloss over-claims (pointwise min/max straddle: no member within error).
- SF sensitivity band "is only reported" but no slot in C-8.
- SF M-10 claim contradicted by v003g L3644/L3184 (alternative members = selected points, same log_index); "twin not valid" field undefined; C-6.3 silent on evaluated STAGE0 with NO_TWIN.
- SF undefined against-terms: P2 "same excess" (and ORIGINAL_K is an entropy-K state alt, not a grid), P5 "onset radius", P8 "agree", R-ML "by the miss", P7 "otherwise".
- SF C-I6 "only registered numerical reading is R-TSR" vs R-GRID (A17 C3) under P2/P8.
- SF M-6 later-entry rule covers V006 only; V005 still open, A90 touches I-6/1.4/D-3/D-4.
- SF CSM no-change list includes A62, A70 (cited in PREREG 11); omits A89.
- SF hit/miss-dominated overlap at exactly half; pattern gaps (TRANSITION-only, INNER CENTERED).
- SF fail-closed stops give root an unconstrained post-target ruling.
- NOTES: P10 vs C-4 INVALID exclusion; C-5.2 "P8 for OUTER"; FREEZE_INCOMPLETE kills NEAR; D-2 notes column; 7th alternative (A13 distance) in score output; M-1 P7 reference; null sigma_ratio; reading scopes; A48 gap principle wording; NEAR excluded from M(Z).

## confirmed by reproduction (CASES_RESULTS.json)
- C08: 8/8 OUTER misses, mixed sign, S(OUTER)=CENTERED -> patterns [P0] only; no R-MF verdict (GAP + C-P vs C-3.2 CONFLICT)
- C09: TRANSITION 11/11 misses -> patterns [P0] only (GAP)
- C12: P2 -> R-MF consistent (P2 row) and against (P1 row) at once; TESTED-NEGATIVE withheld though C-P says an outer-row failure is TESTED-NEGATIVE
- C01: R-UT1 meets consistent + inconsistent (A41 item 3) + OPEN; R-HIST/R-REACH/R-DRIFT consistent + OPEN
- C06: NEAR with no member within error (straddle)
- C07: sensitivity-only overlap row has no C-8 slot
- C10/C11: exact-half tie, zone both hit- and miss-dominated; P3 with P5
- C17/C25: "twin not valid" field undefined; evaluated STAGE0 with NO_TWIN unruled
- C20-C24, C37, C38: evaluated STAGE0 twin has 8 rows -> C-1.1 fail-closed id check conflicts with C-6.1; comparison boundaries behave as written
- C24: P8 vacuous for an all-INVALID STAGE0 scope
- C14: FREEZE_INCOMPLETE (unevaluated member) -> envelope invalid -> NEAR silently impossible
- C16: P10 reports an INVALID flagged row (conflict with C-4)
- C27: 7th alternative (DDO154_DISTANCE_NUISANCE) in the score output
- C28: null sigma_ratio on a VALID row is not covered by fail-closed

## update 2026-10-18T19:17:08Z
- CASES_RESULTS_V2.json supersedes CASES_RESULTS.json (adds the R-TSR standing-fact and the gate-reason gloss events); 38/38 behave as the text dictates
- INNER_CENTERED_PROBE.json: 12/22 INNER misses, mixed sign -> patterns [P0] only (GAP)
- crossfile_out.json: tags 30/30 mapped both ways; M-1..M-12 consistent; "no change" lists disagree (A62, A70, A89); A50 used, not pinned
- severity plan: 1 BLOCKING (R-MF TESTED-NEGATIVE trigger), 12 SHOULD_FIX, 14 NOTE
- next: REVIEW.md, HASHES.txt

## done 2026-10-18T19:21:17Z
- REVIEW.md written: verdict FAIL (1 BLOCKING L-C01, 12 SHOULD_FIX L-C02..L-C13, 14 NOTE L-C14..L-C27)
- HASHES.txt from bytes follows
