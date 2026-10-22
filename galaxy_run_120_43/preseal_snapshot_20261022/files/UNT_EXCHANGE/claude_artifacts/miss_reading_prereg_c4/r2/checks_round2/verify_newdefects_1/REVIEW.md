# REVIEW — verify_newdefects_1: adversarial verification of R2B-01

A helper of lane Claude4 (dispatches 0585 and 0606; refute by default per 0592). The object is unchanged: round 2, PREREG `97d5ce33…`, with all nine listed files matching `HASHES_R2.txt`. The full reasoning, tables and reproduction are in `VERIFY.md`. Stamps are in `PARTIAL.md`, all from `date -u`.

**Outcome: R2B-01 is NOT REFUTED. Severity BLOCKING is confirmed. Its proposed fix is not sufficient as written.**

The verifier's own items below are of two kinds: corrections to the finding's evidence, and gaps in its fix. Severities follow the lane scale (BLOCKING / SHOULD_FIX / NOTE). An item on the fix is rated by what it would do to r3 if carried over unchanged.

### V-0 — BLOCKING (confirmed) — PREREG [C-2] L209/L212, [C-5.3] L357–360, [C-1.1] L119, [C-4] L324

**Quotes:**
- L209: "OUTER is miss-dominated, whatever its sign class. It holds exactly when one of P1, P2 or P11 holds."
- L212: "Every outcome with at least one MISS satisfies at least one of these: a zone pattern (P1, P2, P11, P3, P4, P12 or P13), or P7."

**Defect, confirmed.** Null-ratio rows (L119) and LATE rows (L324) are non-INVALID MISS rows with no r. When N_v(OUTER) ≥ 1 and every non-INVALID OUTER row is unsigned:
- S(OUTER) is UNDEFINED (L195–196);
- P1, P2 and P11 are false (L201);
- the two sentences of L209 disagree, and the E3 line has two values;
- coverage fails when no other zone pattern holds. The INNER-only coverage hole is the same.

**Evidence.**
- My own classifier, written from the text with no lens code (`tools/verify_r2b01.py`), reproduces C14, C15 and C40.
- In a 40,000-outcome synthetic sweep, the disagreement occurs in 1585 outcomes, which are **exactly** the all-unsigned-OUTER outcomes (0 others). The 21 coverage failures all have the characterized form.
- Root ruled the same defect BLOCKING: V005 A98.2 (L973–975 at `70a48f51`; L956–958 at `7f552858`), with dispatch 0619 ordering r3.

**Reach.** The state needs every non-INVALID OUTER row to be unsigned. The routes are a LATE gate on all of them, which needs the producer to report a non-built-in reason (not established), or a non-finite ratio, which needs σ near the subnormal range (scorer L4209–4212; `_ladder_row` L4014–4020). The BLOCKING therefore rests on the determinacy of the only TESTED-NEGATIVE trigger in a sealed mechanical classifier, not on likelihood.

**Fix:** see V-3 to V-8, and VERIFY.md §4.

### V-1 — NOTE — newdefects REVIEW.md L102 (R2B-01(b)): C16d is not an instance

**Quote:** "In C16d, the four signed misses are deficits and the zone reads P1. R-UT1, R-HIST and R-REACH are then CONSISTENT on four rows that have no prediction."

**Defect.** P1 rests on four signed deficit misses at r = −3. The same rows under an early gate also read P1 (G3), and the finding's own fix leaves C16d at P1 (M − U = 4 ≥ N_v/2).

**Fix.** Drop C16d from (b). Keep C16b, and add gate-only witnesses:
- G5: INNER P5 becomes P12 with m(INNER) = 0, taken from 10 hits;
- E_hit_majority: P11 from a signed set that is 3/4 hits.

### V-2 — NOTE — R2B-01(c) evidence: the "gating" pairs change the producer output, not a gate decision

**Quote:** "C17c to C17d removes P1g."

**Defect.** A gate applies only to rows the producer reported INVALID:
- PREREG [C-4] L309 and L313: "A gate-listed row that the producer reports valid is scored normally";
- v003g `_root_result_rows` L1842–1855 and `_root_frozen_rows` L1875–1877;
- the lens REVIEW.md L105: "root cannot aim a gate at chosen valid rows".

The lens builds C16b, C16d and C17d by turning finite rows into null rows (`run_cases_r2b_v2.py` L215–217, L287–293).

**Evidence.**
- On the same producer-INVALID rows, an early gate and a LATE gate give the same P1, Δ_out = +1 and no P1g (G4).
- Over the sweep, m, every defined S, Δ_out and GROWING never change between early and LATE treatment, and P1, P1g, P2, P3, P4, P6, P11, P12 and P13 are never removed.

**The conclusion still stands.** L324 is false because a LATE gate removes P5 (2023), P7 (149), P8 (1) and P9 (415), all toward more misses. In G1 it turns P9 / NOT_TESTABLE into the two-valued state of V-0.

**Fix.** Replace the witnesses with G1, G5 and G6, and state the counterfactual: the same rows, gated early versus LATE.

### V-3 — SHOULD_FIX (on the fix; BLOCKING for r3 if carried as written) — PREREG [C-2] L201; ROOT_ITEMS M-3 L69

**Quotes:**
- L201: "Any condition that uses an UNDEFINED quantity is false".
- The fix: "Add P14 OUTER_UNSIGNED … which then equals P1, P2, P11 or P14 by construction".

**Defect.** The conditions of P14 and P15 test "S(Z) UNDEFINED". Under L201 those tests are false, so P14 and P15 never hold.

**Evidence.** In the sweep with L201 applied literally (FQ strict):
- OUTER_FAILURE disagreements: 18702, against 1585 in r2;
- coverage failures: 1401, against 21.

**Fix.** Amend L201 to: "… except the definedness tests of P14 and P15, which hold exactly when S(Z) is UNDEFINED". P6 then requires S(Z) defined in every zone. Amend M-3 L69 to match.

### V-4 — SHOULD_FIX (on the fix wording) — R2B-01 fix: "Set S(Z) := UNDEFINED whenever M - U < N_v/2"

**Defect.** Without the qualifier "Z miss-dominated", which REVIEW.md item (2) does carry, the rule withholds S in every hit-dominated zone. Then:
- S prints UNDEFINED on the all-hit outcome;
- the E3 line (L362) prints S(OUTER) UNDEFINED on every NOT_NEGATIVE_AT_OUTER outcome;
- with UNDEFINED compared as a label, P6 GLOBAL_OFFSET holds on the all-hit outcome (32 sweep outcomes).

**Fix.** "S(Z) := UNDEFINED when Z is miss-dominated and …".

### V-5 — SHOULD_FIX (on the fix threshold) — "M − U < N_v/2"

**Defect.** The threshold makes defined sign classes depend on gate timing, which r2 does not do.

**Evidence.**
- Relative to an early gate on the same rows, a LATE gate removes P1 2243 times, P2 2281, P11 1311, P3 2617, P4 2658, P12 1945, P1g 731 and P6 556.
- E_tie (2 deficits, 2 hits, 4 gated): early P1, LATE P14.
- E_one: early P1, LATE P14.
- R2B-03 shows LATE status is not mechanically decidable.

**Fix.** Withhold S(Z) only when Z is miss-dominated and M(Z) − U(Z) < H(Z), that is, when the signed rows alone are hit-dominated.
- This closes (b): sign from hits alone, 0 in the sweep.
- It keeps every defined S, Δ_out and GROWING invariant between early and LATE: 0 changes.

The trade-off: a sign class can rest on one signed miss (E_one gives P1), as it would under an early gate. If root prefers M − U < N_v/2, M-3 should record its gate-timing dependence.

### V-6 — SHOULD_FIX (fix completeness) — PREREG [C-5.2] L351, [C-3.2] L271, L275, L284; ROOT_ITEMS M-3 L71–72

**Quotes:**
- L351: "OUTER_FAILURE (P1/P2/P11, with the sign class)";
- L271 and L275: R-MF and R-DRIFT keyed to "P1, P1g, P2, P11";
- L284: P5 "as P1";
- M-3 L72: P11, P12 and P13 "together give the coverage property".

**Defect.** The fix edits L209, L212, L324, L487 and L492 only. These restatements would keep the old equivalence and coverage claim.

**Fix.** Add P14 to L351, L271, L275 and L284 (with R2B-05), and restate M-3 L71–72 with P14 and P15.

### V-7 — NOTE — policy choice made silently

**Defect.** With OUTER_FAILURE := miss-dominated, an OUTER whose every row is LATE-gated reads TESTED-NEGATIVE with no OUTER prediction (C15, G1). The same rows gated before step 5 read NOT_TESTABLE (P9). Codex2 0490 left the scientific policy open.

**Fix.** Make it an explicit M-3 sub-item for root.

### V-8 — NOTE — L324 deleted, not replaced

**Fix.** Under the V-5 threshold, replace it with a true statement (the sweep confirms every clause):

> "Relative to registering the same gate before step 5, a LATE gate never lowers N_v(Z) or M(Z), and never changes m(Z), a defined S(Z), Δ_out or GROWING. It never removes P1, P1g, P2, P3, P4, P6, P11, P12 or P13. It can add P5, P13, P14 or P15, and remove P5, P7, P8 or P9, each time toward more misses."

Then rewrite C-9 L487 and L492 against it.

Extend the M-12 suite to cover C14, C15, C16b, C17d, C40, G1, G4, G5, E_tie, E_one, E_hit_majority and the all-hit outcome.

### V-9 — NOTE — provenance

**Defect.** REVIEW.md L7 says the lens "reproduces, independently" A98.2. But its V005 read that contained A98 is stamped 20:08:40Z, and its classifier and cases were written from 20:15:51Z to 20:21:03Z (UTC mtimes).

Independence is shown for Codex2 0490 (20:01:30Z) and for this check, not for the lens. Codex2's second witness ("LATE gates turn ordinary deficit rows into MISS/UNDEFINED rows") has the V-2 framing too. The A98.2 ruling still stands on the null-ratio witness and on G1.

## Not read and not run

- No NGC3198 target, observed velocity, rotmod/Vobs/MassModels/SPARC path, runs_ext path or UVT_* item.
- No recursive content search.
- No launches.
- The lens tools, Claude4's checker and Codex1's rehearsal classifier were not run.
- The sweep is synthetic, and its counts show existence, not frequency.
