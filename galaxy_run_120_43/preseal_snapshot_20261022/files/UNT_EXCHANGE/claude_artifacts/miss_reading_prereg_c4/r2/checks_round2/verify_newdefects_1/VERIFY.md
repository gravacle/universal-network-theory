# VERIFY — finding R2B-01 (lens newdefects), adversarial recheck, refute by default

A helper of lane Claude4, under dispatches 0585 and 0606, run as a refute-by-default verifier (0592). This verifier edits nothing in the object; Claude4 owns the fix round. Clock stamps are in PARTIAL.md, all from `date -u` (start 2026-10-18T20:30:57Z).

## Verdict

**NOT REFUTED. Severity BLOCKING confirmed.** The fix is right in direction but **not sufficient as written.**

- **(a) is confirmed from bytes and by an independent classifier.** When N_v(OUTER) ≥ 1 and every non-INVALID OUTER row is unsigned, the two OUTER_FAILURE sentences of L209 disagree, the E3 line has two values, and the coverage claim of L212 fails. The INNER-only coverage hole is confirmed too. In my 40,000-outcome sweep the disagreement occurs in exactly that set of outcomes and in no other.
- **(b) is confirmed, with one wrong example.** C16b holds: P11 is asserted from four hits while all four misses are unsigned. C16d is not an instance: its P1 rests on four signed deficit misses, and the finding's own fix still gives P1 there.
- **(c): the conclusion holds, but the witnesses are misattributed.** The L324 guarantee is false. But C16a→b, C16c→d and C17c→d change the producer output (finite predictions become null). No gate decision can do that: a gate applies only to rows the producer itself reported `valid: false`.
  - On the same producer output, an early gate and a LATE gate give identical m, S, Δ_out and GROWING. So the P1g removal in C17d is not a gate effect.
  - The guarantee fails on other patterns: relative to an early gate, a LATE gate removes P9, P5, P7 and P8. It also turns an all-gated OUTER from P9 / NOT_TESTABLE into the two-valued state of (a).
- **The fix has three substantive gaps.**
  1. Under the text's own L201 rule, P14 and P15 can never hold. Adopted as written, the fix makes the defect worse.
  2. The JSON wording drops the "miss-dominated" qualifier. Read literally, every hit-dominated zone gets S = UNDEFINED, and P6 can fire on an all-hit outcome.
  3. The threshold M − U < N_v/2 makes defined sign classes depend on whether a gate was early or LATE, and R2B-03 shows that status is not mechanically decidable.

  It also leaves four restatements of the old equivalence unedited. A better fix is given in §4.

## Object and sources (sha256 from bytes)

**Object** (all match `round2/HASHES_R2.txt`, whose own sha is `2e3cf0c60088f23a9530a3ab5b8d8ec1a2d8c5184a7eeff11f726fafa964c6fd`):

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

**V005 (open), read twice:**

| read | sha256 | note |
|---|---|---|
| 2026-10-18T20:34:29Z | `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2` (1462 lines) | A98 at L948–960 |
| 2026-10-18T20:48:24Z | `70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e` (1479 lines) | A101 added (B2 and registry, not this prereg) |

At the second read, A98 is at L965–977 with section sha `181248d91db1437786cc8654c4dc82bb3983ea36a069f702f6dfd2acadfd8aa9`. Its text is unchanged from the first read. A99–A101 say nothing about the miss-reading prereg.

**Rulings and reviews:**
- dispatch 0619 `238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99`;
- dispatches 0585 `9003633293ff…`, 0606 `dbb80c77cb08…` and 0592 `b1a5310fcb41…`, all matching bytes;
- 0518 `0748fb2091a6…`;
- Codex2 0490 `3a922168f800de5ae9fff2ba1cb55af2f55d7ae4290a75b14a0ca2daa36a2649` and Codex2 REVIEW_CX2V001 `7e3b6211ded52e4212c8534b7dad04bc9334ea5c458cdc8de6c8545c19e5af71`.

**Freeze v003g:**
- module `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405`;
- RUNBOOK_V001 `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b`;
- slots V003 `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969`.

**Lens:**
- REVIEW.md `5b7c8b488f85bff551b47df5d83ed4904d86936cd51188c32dd5840bf4e4b3f3`;
- CASES_R2B_V2.json `8c96ecea80a096919222a460f1193f352bc044bc10efcffd5e1a85baaebafbdc`;
- tools/classify_r2b.py `b3f43a5f…` and tools/run_cases_r2b_v2.py `7d7310a7…`;
- PARTIAL.md `9ef129e0…`.

**Other sources:**
- round 1 PREREG `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143`;
- the round-1 targetfree REVIEW (B-3);
- the rehearsal record `19807bb3…`;
- the Codex2 checklist `020ef3f1…`;
- one forward-driver file, `ngc_route_tail_readiness_cx3/v011/cx3v005/galaxy_m0_forward_c2v011_cx3v005_cx3r003.py` `8c11a8a6…`. I read only its reason-string lines.

**Not read:** no NGC3198 target, observed velocity, rotmod/Vobs/MassModels/SPARC path, runs_ext path or UVT_* item. No sibling round-2 verifier folder. No recursive content search. Nothing launched.

## 1. Is the quoted text there? Yes, at every cited line

- [C-1.1] L119: "A VALID row whose `sigma_ratio` is null (v003g NON_FINITE_SIGMA_RATIO) is a MISS with sign UNDEFINED. It counts in N_v(Z) and M(Z), and it is left out of m(Z) and Δ_out."
- [C-2] L195: m(Z) "is UNDEFINED when there is no such row".
- [C-2] L196: S(Z) "is UNDEFINED when m(Z) is UNDEFINED".
- [C-2] L201: "Any condition that uses an UNDEFINED quantity is false, and it is reported as UNDEFINED."
- [C-2] L209: "OUTER is miss-dominated, whatever its sign class. It holds exactly when one of P1, P2 or P11 holds."
- [C-2] L212: the coverage sentence.
- [C-4] L324: "each LATE-gate row counts as a non-INVALID MISS row with sign UNDEFINED. A late gate can therefore never remove a pattern or create P9."
- [C-5.3] L357–360: the E3 line.
- [C-9] L487: "The coverage property holds (§2)".
- [C-9] L492: "A gate added after the predictions removes a pattern | LATE-gate rows count as MISS rows for this document (§4)."

**The same equivalence and coverage claims are restated in four places the finding does not name:**
- [C-5.2] L351: "OUTER_FAILURE (P1/P2/P11, with the sign class)".
- ROOT_ITEMS M-3 L69: root is asked to adopt "an UNDEFINED quantity makes a condition false".
- ROOT_ITEMS M-3 L71: "OUTER_FAILURE := OUTER miss-dominated, of any sign".
- ROOT_ITEMS M-3 L72: P11, P12 and P13 "together give the coverage property (every outcome with a MISS has a pattern)".

**The defect is new in round 2.** Round 1 (`6437ea33`) had no null-ratio rule, no LATE rule, no OUTER_FAILURE and no coverage claim (its L136: m(Z) is over the non-INVALID rows, UNDEFINED only when N_v(Z) = 0). The defect arises where the round-2 fixes for L-C19, B-3, A-04/L-C01 and L-C04 interact.

## 2. Is it really defective?

### (a) The two OUTER_FAILURE sentences, the E3 line and coverage: CONFIRMED, BLOCKING

**The chain in the text.**
- Unsigned rows are non-INVALID MISS rows (L119, L324). So if every non-INVALID OUTER row is unsigned, M(OUTER) = N_v(OUTER) ≥ 1, and OUTER is miss-dominated (L197).
- m(OUTER) has no input, so m and S(OUTER) are UNDEFINED (L195–196).
- P1, P2 and P11 compare S(OUTER) with a label, so they are false (L201, L217–219).
- OUTER_FAILURE is then true by the first sentence of L209 and false by its second. The E3 line (L357–359) reads TESTED-NEGATIVE under the first and NOT_NEGATIVE_AT_OUTER under the second.
- P7 is false, because a zone is miss-dominated (L227). If INNER and TRANSITION carry no zone pattern, no pattern of the coverage list holds (L212).

**Extra consequence.** Take the first sentence as the definition, as ROOT_ITEMS M-3 L71 does. E3 then prints TESTED-NEGATIVE, but no pattern that lists R-MF holds: the R-MF row L271 is keyed to P1, P1g, P2 and P11. So R-MF's verdict (L250) is printed without the status tuple that L237 requires for it.

The A48 gap-filler (L30) does not rescue this. It applies "where this text is silent", and here the text says two different things.

**Independent reproduction.** `tools/verify_r2b01.py` is my own classifier, written from the r2 text alone. It imports no lens code and reads no file. Results are in `VERIFY_R2B01_RESULTS.json`.

| case | patterns | OUTER_FAILURE (miss-dominated / P1∨P2∨P11) | E3 | coverage |
|---|---|---|---|---|
| C14-like (all OUTER null-ratio) | P0 | true / false | TESTED-NEGATIVE / NOT_NEGATIVE_AT_OUTER | fails |
| C15-like (all OUTER LATE) | P0 | true / false | same split | fails |
| C40-like (all INNER valid rows LATE) | P0 | false / false | NOT_NEGATIVE_AT_OUTER | fails |

**Sweep.** 40,000 random synthetic outcomes under the r2 rules, seed 20261018:
- the two sentences disagree in 1585 outcomes, which is **exactly** the set with N_v(OUTER) ≥ 1 and every non-INVALID OUTER row unsigned (0 others);
- E3 disagrees on the same 1585;
- coverage fails in 21 outcomes, all of the characterized form: every miss-dominated zone is INNER or OUTER with all rows unsigned, and TRANSITION is not miss-dominated.

The lens's CASES_R2B_V2.json agrees: C14 and C15 each record CONFLICT 'C-2 OUTER_FAILURE', GAP 'C-2 coverage property' and CONFLICT 'C-5.3 E3 verdict line', and C40 records GAP 'C-2 coverage property'.

**How the state is reached.** It needs every non-INVALID OUTER row to be unsigned, by one of two routes.
- **Null ratio.** v003g `_ladder_row` L4014–4020 marks NON_FINITE_SIGMA_RATIO only when (p − v)/σ is non-finite. The scorer requires the velocity finite and σ finite and > 0 (L4209–4212), and a valid prediction finite (L1856). A null ratio therefore needs σ near the subnormal range, or |p − v| near 1e308: Codex2 used σ = 1e-320, the lens σ = 5e-324. That is reachable in the code's input domain, but not with physical σ values.
- **LATE gates.** Every non-INVALID OUTER row would have to be producer-INVALID with a non-built-in reason and gated after step 5. Whether the production producer can emit any non-built-in reason was not established. In the one forward-driver file I sampled, only the three built-in reasons appear.

**Severity: BLOCKING stands.** OUTER_FAILURE is the only trigger of the only TESTED-NEGATIVE line. The sealed M-12 classifier (ROOT_ITEMS M-12) must implement this branch, and the two sentences give two verdicts on it. Root ruled exactly this defect as the r2 blocking item: V005 A98.2 ("allowed undefined-sign MISS rows count in Nv/M, so an OUTER zone can be miss-dominated with OUTER_FAILURE true while P1, P2, P11 and every named MISS pattern read false. The INNER-only case is the same, and the C-4 LATE gates can remove a pattern"), and 0619 orders r3. The BLOCKING rests on the text's determinacy, not on how likely the state is with real data. Parts (b) and (c) alone would be SHOULD_FIX.

### (b) A sign class taken from hits: CONFIRMED, but C16d is not an instance

**C16b reproduced.** OUTER has N_v = 8, M = 4 and U = 4, with m = 0 from four hits at r = 0. It reads P11, so R-S1, R-GRID, R-NAX, R-MF and R-DRIFT are CONSISTENT. P11's gloss (L219) is "(misses of both signs, or small residuals)". The "small residuals" belong to the hits, and no miss has any residual.

**Witnesses that need no change of producer output** (§2(c) explains why that matters):
- **G5.** INNER has 12 producer-INVALID gated rows and 10 hits. With an early gate it reads P5. With a LATE gate it reads P12 with m(INNER) = 0, taken from the 10 hits alone, and P5 is gone.
- **E_hit_majority.** OUTER has 1 deficit miss, 3 hits and 4 gated rows. LATE gives P11, from a signed set that is 3/4 hits.
- **Sweep.** 3712 outcomes have an OUTER or INNER sign-class pattern with zero signed misses.

**Correction.** In the REVIEW.md L102 example, C16d "reads P1. R-UT1, R-HIST and R-REACH are then CONSISTENT on four rows that have no prediction". That is not an instance of the defect.
- C16d's four signed rows are deficit misses at r = −3, and P1 rests on them.
- The same rows under an early gate also give P1 (G3).
- The finding's own fix leaves C16d at P1, since M − U = 4 ≥ N_v/2.
- The finding itself leaves C16d out of its suite list.

The example should be dropped from (b). C16d belongs only to (c), and there it is a change of producer output.

### (c) The L324 guarantee and the C-9 rows: CONCLUSION CONFIRMED, WITNESSES MISATTRIBUTED

**A gate cannot invalidate a producer-valid row.**
- PREREG L309: a gate covers "rows the producer reported INVALID **and** that the pinned gate document lists". L313: "A gate-listed row that the producer reports valid is scored normally."
- v003g `_root_result_rows` consults `_authorized_row_registration` only when the producer row reads `valid` False (L1842–1852). A valid row with gate metadata refuses (L1853–1855). A frozen valid row with any registration refuses (`_root_frozen_rows` L1875–1877). An unlisted producer-INVALID row refuses (`V010_INVALID_NOT_ROOT_ROSTERED`, L1795–1797).
- So root's only decisions about a producer-INVALID row are early gate, LATE gate, or refusal.

**The lens builds its three "gating" pairs by editing the producer output.** In `run_cases_r2b_v2.py` L215–217 (C16a/b) and L287–293 (C16c/d, C17c/d), the "after" rows become `('INV', 'SYNTH_GATE_LATE')` where the "before" rows had finite ratios. The lens's own REVIEW.md L105 concedes the point: "root cannot aim a gate at chosen valid rows". So C17c→C17d shows that P1g depends on whether Q42 and Q43 have predictions. It does not show that a gate removes P1g.

**The gate decision, isolated.** I compared the same producer-INVALID rows under an early gate and under a LATE gate.

| case | early gate | LATE gate |
|---|---|---|
| G4 (the C17d rows) | P1, Δ_out = +1 | P1, Δ_out = +1 |
| G3 (the C16d rows) | P1 | P1 |
| G1 (every OUTER row gated) | P8 and P9, E3 NOT_TESTABLE | P0 only, E3 two-valued, coverage fails |
| G6 (3 INNER rows gated, rest HIT) | P8 | P7 |

Over the 40,000-outcome sweep, under r2:
- m, every defined S, Δ_out and GROWING are unchanged in every outcome;
- P1, P1g, P2, P3, P4, P6, P11, P12 and P13 are never removed;
- P5 is removed 2023 times, P7 149, P8 1 and P9 415.

**So L324's sentence is false,** but because a LATE gate removes P5, P7, P8 and P9, and because it creates the state of (a) from what would have been P9 (G1). Every such change goes toward more misses, so the steering risk of the C-9 row at L492 is closed in direction, though not as worded. L487 is false through (a).

**"Every gate is LATE in practice."** RUNBOOK_V001 supports this, provided any gate exists:
- L9: step 1 saves the raw forward results;
- L11: step 3 gathers the "run-produced … gate registrations";
- L15: step 4 adopts the "approved gates".

**Provenance note.**
- REVIEW.md L7 says the lens "reproduces, independently" the A98.2 defect. But its V005 read that contained A98 is stamped 20:08:40Z (V005_PINS_R2B.json mtime 20:08:32Z), and its classifier and cases were written between 20:15:51Z and 20:21:03Z (file mtimes, UTC). The record does not show that the lens found it independently.
- Codex2 0490 (20:01:30Z, another lane) is independent, and so is this check.
- Codex2's second witness has the same framing: "LATE gates turn ordinary deficit rows into MISS/UNDEFINED rows" (REVIEW_CX2V001 L8). The A98.2 ruling still stands on the null-ratio witness and on G1.

## 3. Would the fix work? In direction yes; as written no

I ran three readings of the fix:
- **FJ:** the finding JSON's words, "S(Z) := UNDEFINED whenever M − U < N_v/2".
- **FQ:** the REVIEW.md words, which add "Z is miss-dominated".
- **FB:** my alternative (§4).

Each ran under three semantics for UNDEFINED:
- **strict:** L201 as written, applied to P14/P15's own test;
- **value:** UNDEFINED compared as a label;
- **explicit:** P14/P15 test definedness, and P6 requires a defined S in every zone.

Sweep counts over 40,000 outcomes, with the LATE gate:

| variant | OUTER_FAILURE disagree | E3 disagree | coverage fails | sign from hits alone | P6 with no zone miss-dominated | LATE vs early: removes P1 / P1g / P6 |
|---|---|---|---|---|---|---|
| r2 as written | 1585 | 1585 | 21 | 3712 | 0 | 0 / 0 / 0 |
| FJ strict | 18702 | 18702 | 1401 | 0 | 0 | 2243 / 731 / 556 |
| FJ value | 0 | 0 | 0 | 0 | **32** | 2243 / 731 / 535 |
| FJ explicit | 0 | 0 | 0 | 0 | 0 | 2243 / 731 / 556 |
| FQ strict | 18702 | 18702 | 1401 | 0 | 0 | 2243 / 731 / 556 |
| FQ explicit | 0 | 0 | 0 | 0 | 0 | 2243 / 731 / 556 |
| FB strict | 7428 | 7428 | 260 | 0 | 0 | 0 / 0 / 0 |
| **FB explicit** | **0** | **0** | **0** | **0** | **0** | **0 / 0 / 0** |

**F-1. The L201 trap (SHOULD_FIX on the fix; it makes r3 BLOCKING again if carried as written).**
- P14/P15 hold when "S(Z) UNDEFINED", but L201, which M-3 L69 asks root to adopt, makes any condition that uses an UNDEFINED quantity false.
- Read literally, P14 and P15 never hold, and "OUTER_FAILURE … equals P1, P2, P11 or P14 by construction" is false.
- Because the new S rule withholds S more often, disagreements rise from 1585 to 18702 and coverage failures from 21 to 1401.
- **Fix:** exempt the P14/P15 definedness test from L201 in so many words, and make P6 require a defined S in every zone.

**F-2. The unqualified S rule (SHOULD_FIX on the JSON wording).**
- "Whenever M − U < N_v/2" also covers every hit-dominated zone (there M − U ≤ M < N_v/2). Then:
  - S(Z) prints UNDEFINED for the all-hit outcome;
  - the E3 line (L362, "always prints S(OUTER)") prints UNDEFINED on every NOT_NEGATIVE_AT_OUTER outcome;
  - under value semantics, P6 GLOBAL_OFFSET holds on the all-hit outcome (UNDEFINED = UNDEFINED = UNDEFINED ≠ CENTERED; 32 sweep outcomes have P6 with no zone miss-dominated).
- REVIEW.md's "(2) S(Z) := UNDEFINED whenever Z is miss-dominated only because of unsigned rows (M − U < N_v/2)" carries the qualifier. The JSON wording must match it.

**F-3. Gate-timing dependence (SHOULD_FIX on the threshold).**
- Under r2, early and LATE treatment of the same rows give the same defined S. Under FQ they do not.
- Relative to an early gate, a LATE gate removes P1 2243 times, P2 2281, P11 1311, P3 2617, P4 2658, P12 1945, P1g 731 and P6 556 (sweep), turning them into P14/P15.
- Edge cases:
  - E_tie (2 deficits, 2 hits, 4 gated): early P1, LATE P14.
  - E_one (1 deficit, 7 gated): early P1, LATE P14.
- R2B-03 shows LATE status is not mechanically decidable from any input. The fix would carry that undecidability into the sign class, which r2 does not do.

**F-4. Incomplete edits (SHOULD_FIX).** Besides L209, L212, L324, L487 and L492, r3 must also update:
- L351 (C-5.2, "P1/P2/P11");
- L271 and L275 (the R-MF and R-DRIFT rows, keyed to "P1, P1g, P2, P11");
- L284 (P5 "as P1"; see R2B-05);
- ROOT_ITEMS M-3 L69, L71–72, and its recommendation "adopt all of it as written".

**F-5. A policy choice made silently (NOTE; put to root).** With OUTER_FAILURE := miss-dominated, an OUTER whose every row is LATE-gated has no prediction at all, yet reads TESTED-NEGATIVE (G1, C15). The same rows gated before step 5 read NOT_TESTABLE (P9). This follows B-3's intent and the A48 direction, but Codex2 0490 left the scientific policy open ("this review does not choose the scientific policy"). r3 should put it to root as an explicit M-3 sub-item.

**F-6. A deletion with no true replacement (NOTE).** Deleting L324's sentence leaves the C-9 row at L492 without support. Under FB a true statement exists (§4, item 5).

**F-7. P15's readings (NOTE).** P15 carries R-GEFF, R-GEO and R-NAX and drops R-ML and R-SPEC from the P3/P4/P12 list. That may be right, but the text should say why.

## 4. Better fix

**1. U(Z), as proposed:** the number of non-INVALID MISS rows with undefined r (null-ratio and LATE rows).

**2. Withhold the sign class only when the signed rows alone are hit-dominated:**
- the rule: S(Z) := UNDEFINED when Z is miss-dominated and M(Z) − U(Z) < H(Z);
- it never bites when U(Z) = 0, so every outcome without unsigned rows is unchanged;
- a sign class is then never taken from hits alone or from a hit majority, which closes (b);
- every defined S(Z), Δ_out and GROWING stays identical under early and LATE treatment (sweep: 0 changes).

**The trade-off for root (M-3).**
- FB asserts a sign class from as few as one signed miss when the other misses are unsigned (E_one → P1), which is what the same rows give under an early gate.
- FQ's stricter M − U < N_v/2 withholds it, but makes the sign class depend on gate timing (F-3).

**3. P14 and P15 as definedness tests:**
- **P14 OUTER_UNSIGNED:** OUTER miss-dominated and S(OUTER) UNDEFINED. **P15 INNER_UNSIGNED:** the same for INNER.
- **Amend L201** to: "… is false, except the definedness tests of P14 and P15, which hold exactly when S(Z) is UNDEFINED."
- **P6** requires S(Z) defined in every zone.

**4. One definition of OUTER_FAILURE:** OUTER miss-dominated.
- Replace "It holds exactly when one of P1, P2 or P11 holds" with: "Equivalently, exactly one of P1, P2, P11 or P14 holds."
- Restate coverage with P14 and P15.
- Edit L351, L271, L275 and L284 (with R2B-05), and ROOT_ITEMS M-3 L69 and L71–72.

**5. Replace the second sentence of L324 with a true one:**

> "Relative to registering the same gate before step 5, a LATE gate never lowers N_v(Z) or M(Z), and never changes m(Z), a defined S(Z), Δ_out or GROWING. It never removes P1, P1g, P2, P3, P4, P6, P11, P12 or P13. It can add P5, P13, P14 or P15, and remove P5, P7, P8 or P9, each time toward more misses."

The sweep confirms every clause under FB:
- removed only P5 2023, P7 149, P8 1 and P9 415;
- added only P13 2958, P14 3153, P15 3048 and P5 458.

Then rewrite the C-9 rows at L487 and L492 against it.

**6. M-3 sub-item:** state, for root's ruling, that an OUTER whose every non-INVALID row is unsigned reads TESTED-NEGATIVE (F-5).

**7. M-12 agreement suite:**
- C14, C15, C16b, C17d and C40, as proposed;
- the early/LATE pairs G1, G4 and G5;
- the threshold boundaries E_tie, E_one and E_hit_majority;
- the all-hit outcome, checking the printed S and that P6 is false.

All are in `VERIFY_R2B01_RESULTS.json` and `VERIFY_R2B01_EDGES.json`.

## 5. Tested and not tested

**Tested (synthetic only):**
- 9 named cases;
- 7 early/LATE counterfactual pairs;
- 5 threshold edge cases;
- a 40,000-outcome sweep under r2 and under 7 fix-and-semantics combinations;
- byte checks of every quoted line and of the cited v003g lines.

The script runs under an audit-hook fence: forbidden name classes are refused, writes go only to this folder, and there is no subprocess or socket.

**Not tested:**
- real producer outputs, and whether a production producer can emit a non-built-in INVALID reason;
- the lens's classifier, which I read but did not run;
- Claude4's checker;
- Codex1's rehearsal classifier.

The sweep's row distribution is arbitrary. Its counts show existence and the characterization, not how often any case occurs.

## Files in this folder

- VERIFY.md (this file), REVIEW.md, PARTIAL.md and HASHES.txt;
- VERIFY_R2B01_RESULTS.json and VERIFY_R2B01_EDGES.json;
- tools/verify_r2b01.py and tools/verify_r2b01_edges.py.
