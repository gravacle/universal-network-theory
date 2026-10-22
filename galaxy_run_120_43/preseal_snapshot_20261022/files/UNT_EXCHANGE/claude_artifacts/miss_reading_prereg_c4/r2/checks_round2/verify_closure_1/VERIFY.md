# VERIFY — round-2 closure-lens finding F1: adversarial verification 1

**Who and why.** A helper of lane Claude4, working under dispatches 0585 and 0606, with the 0592 refute-by-default pattern. This is a round-2 recheck of one finding: F1 of lens R2-A (closure), `checks_round2/closure/REVIEW.md` (`566cf50f…`, L166–L202). I tried to refute it from the bytes. Nothing outside this folder was edited; Claude4 owns the fix round.

**Written:** from 2026-10-18T20:42:19Z (`date -u`). The clock stamps for each step are in PARTIAL.md.

## Verdict

- **F1 is NOT REFUTED. It is CONFIRMED in substance.**
- **The severity stays BLOCKING.** The P11 half carries it: the E2-shaped crossing outcome is an OUTER_FAILURE whose most pertinent binding readings are left unregistered. The missing R-HIST also conflicts with the A10 DECLARED-PREMISE reading, which is written verbatim into the freeze manifest notes. Taken alone, the P2 half for R-UT1 and R-REACH could drop to SHOULD_FIX if the text stated a reason; it states none.
- **I found two points that strengthen the finding** (§4):
  - The r2 text already registers R-UT1, R-HIST and R-REACH for an outer excess or a mixed outer zone, but only when TRANSITION is not hit-dominated (P5, "as P1", L284). The same OUTER failure therefore gets different binding readings depending on another zone.
  - r2, and the author's own r3 design (0096 L17), treat the history/species reading as sign-free in INNER (R-SPEC on P3, P4 and P12). Only in OUTER is it limited to a deficit.
- **Three precision corrections** (§3 R7, §4). None of them changes the verdict.
- **The fix is NOT sufficient as written** (§6):
  - listing patterns, as in "P1, P1g, P11", lets the gap come back in r3's planned P14;
  - one P2 option reuses NOT_ADDRESSED against its [C-3] definition;
  - the P5 inconsistency is not addressed.
  A better fix is in §6.

## 1. Bytes verified

**The object** (`r2/round2/`). All 10 entries of HASHES_R2.txt match `shasum -a 256 -c`, at 20:28Z. HASHES_R2.txt itself is `2e3cf0c6…`.

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407` |
| CLAUSE_SOURCE_MAP_R2.md | `38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201` |
| ROOT_ITEMS_R2.md | `4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500` |
| NUMBER_PROVENANCE_R2.json | `ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf` |
| INDEX_R2.md | `0d24b8fe778fb704398a7039f579977d92e51dfd152994d6e68048cffa03b926` |
| TARGET_FREE_CHECK_R2.json | `624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9` |
| TARGET_FREE_MUTATION_TEST_R2.json | `4445a9bf014e0cabe6d49cd0f45e4df1c388ac7c2c443df0d6f1d3a62214ec02` |
| tools/check_target_free_c4v002.py | `4ae4f7053f18aa13416ad4e3d118d9250a959e72035c6e5f0c5f92305d8511aa` |
| tools/test_check_target_free_c4v002.py | `dc812342fa7c363e71949e3ecb2a206d68786ff5973280cf98909d03dd114f92` |
| tools/make_miss_reading_c4v003.py | `2132078f9779b01d5ad05c01b0280c218d160f6380f75ed5b99af893a1a2f9ab` |

**Sources read** (sha256 from bytes):

| source | sha256 | lines used |
|---|---|---|
| V003 addendum (frozen) | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` | A10 L32, L38; A12.3 L91–L95 |
| V004 addendum (frozen) | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` | A15 E3 L43–L50; A20 L154–L162; A41 L742–L749 |
| V005 addendum (open), read at 20:29:44Z and again at 20:40:55Z, unchanged | `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2` | A63 L597 (the A63 section pin `8cbe6553…` matches); A98 L948–L959; A65 trailing table L1449, L1452 |
| CURRENT_INSTRUCTIONS | `59ada35ce59146c758374c88abeb3ed183f09217501d1f3c7a43463adacc6917` | L305 |
| slots V003 | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` | `notes_block_for_manifest.structural_assumptions` only (`tools/slots_sa_notes_vc1.py`) |
| dispatch 0522 | `30af5d6811788e9bbed4c470dae0ea9bb4ae5230a734fa7940e942b30ed66160` | L9–L13, L22 |
| dispatch 0619 | `238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99` | the r3 order |
| Codex2 0490 | `3a922168f800de5ae9fff2ba1cb55af2f55d7ae4290a75b14a0ca2daa36a2649` | its findings |
| Codex2 round-2 reachability REVIEW | (path in 0490) | L15 |
| Claude4 0096 (the r3 design) | `3f50d9d6300197170aa8b9ae997a5b0e39d32d84b16163bff1167ab8639704a9` | L17 |
| V001 | `6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345` | L126–L132 |
| round-1 PREREG | `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` | L195–L202 |
| round-1 fidelity REVIEW (A-04) | — | L130–L151 |
| round-1 consistency REVIEW (L-C01) | — | L42–L72 |
| verify_consistency_1 VERIFY | — | §5 F-c L139–L144; better fix L148–L166 |
| closure lens: REVIEW.md, `runs/READINGS_E3_R2A.json`, `tools/readings_e3_closure_c4.py` | `566cf50f…`, `ff0355b6…`, `330dbea8…` | F1; the repro |
| Codex2 checklist; Codex1 rehearsal | `020ef3f1…`; `19807bb3…` | searched for this issue: neither raises it |

The full V005 bytes I read are kept here as `V005_SNAPSHOT_AT_VERIFY.md`.

## 2. Is the quoted text there?

**Yes, verbatim.** Line numbers are in PREREG r2 (`97d5ce33`):
- **L271:** "| **P1, P1g, P2, P11** (OUTER_FAILURE; expected: A15 E2) | **R-MF:** … TESTED-NEGATIVE for exactly this scope when OUTER_FAILURE holds."
- **L272–L274:** the pattern cell of R-UT1, R-HIST and R-REACH is "P1, P1g".
- **L276–L278:** "| P2, P11 | **R-S1:** …", "| P2, P11 | **R-GRID** …" and "| P11 | **R-NAX:** …".
- **L24:** "**Binding principles** (A10, A12.3, A15 E3, A20, A23, A41, A48) **[C-P]**".
- **L209:** OUTER_FAILURE "is the 'outer-row failure' of A15 E3, registered here as: OUTER is miss-dominated, whatever its sign class. It holds exactly when one of P1, P2 or P11 holds."
- **CSM L83** (A-04): "FIXED. OUTER_FAILURE is sign-agnostic; P11; the E3 verdict line (C-2, C-3, C-5.3)."
- **CSM L110** (L-C01): "FIXED. As A-04, plus the E3 verdict line (the refuter's better fix)."

I searched the round-2 PREREG, CSM, ROOT_ITEMS and INDEX for a reason why R-UT1, R-HIST and R-REACH stop at P1/P1g. **There is none.** ROOT_ITEMS M-3 (L71, L81) only says the old E3 trigger "fired only under P1", and M-4 (L86–L102) does not address reading coverage.

## 3. Is it really defective? Refutation attempts

**R1. "R-UT1, R-HIST and R-REACH are tail readings for a deficit, so P1-only is principled."** This is the strongest attempt. It fails, for five reasons.
1. **Every binding source is sign-free:**
   - A15 E3, V004 L44–L46: "An outer-row failure … Three readings stay open";
   - A12.3, V003 L91: "A miss reads three ways";
   - A10, V003 L38: "Every 120/43 miss is therefore read two ways";
   - A20, V004 L158: "A failure of the NGC3198 outer rows is therefore read two ways";
   - 0522 L9–L13: "outer-row misses … must be read in more than one way. The registered readings include: model failure; the missing Bind-history / collective component …; … (UT-1)";
   - A63, V005 L597, pinned: "a further registered reading for outer-row misses";
   - CURRENT_INSTRUCTIONS L305: "every miss is read two ways".
2. **r2 itself treats the history/species reading as sign-free in INNER.** R-SPEC ("a species or history weight (SA-BH-01)", L281) is on P3 (excess), P4 (deficit) and P12 (mixed). Claude4's own r3 design (0096 L17) lists R-SPEC among "the P3/P4 readings that need no sign". Yet in OUTER, R-HIST is limited to a deficit.
3. **r2's own P5 row contradicts the restriction.** P5 has no OUTER sign condition (L224), and its readings are "as P1 for the OUTER rows" (L284). So an outer excess or a mixed outer zone gets R-UT1, R-HIST and R-REACH whenever TRANSITION is not hit-dominated, and loses them when TRANSITION is hit-dominated (cases V5 and V6 against V2 and V3, §7). Either way the text is inconsistent:
   - if these readings are sign-free, P2 and P11 must carry them (F1);
   - if they are deficit-only, P5's "as P1" is wrong.
4. **R-REACH's own wording is sign-neutral:** "magnitudes, k = 0-block drift or finite-size effects at larger L or with mixing" (L274). Its drift sub-case, R-DRIFT, is already registered for P2 and P11 (L275).
5. **The crossing case is the failure mode A41 describes.** In P11's E2-shaped crossing, the curve sits above the target near 30 kpc and below it near 44 kpc. A41 (V004 L747–L749) says static present-mass gravity "cannot supply NGC3198's flat outer curve" and leaves "only" U1/U2 (R-REACH) and "the history/collective channel (A10, BH-D)".

*What I concede:* for a pure outer excess (P2), root frames the history channel as "the remaining owned route to a flat outer curve" (V005 L1449, the 0519 plug, in the unpinned A65 trailing block; A41). So an author could argue that E3 readings 2–3 and R-UT1 do not bear on an excess. r2 does not make that argument. A15 E3 does not distinguish signs, and A10's "every miss" leaves R-HIST no sign exception.

**R2. "A20 amended A15, and A20's two readings are about the tail."** A20 L155 narrows reading 2 and does not drop it. A20 L158 is not sign-limited either. More decisively, r2 L209 itself equates OUTER_FAILURE, of any sign, with A15 E3's "outer-row failure", in order to make the verdict sign-free. It cannot read E3 as sign-free for the verdict and as a deficit for the readings without saying so. **The attempt fails.**

**R3. "Nothing is lost: the freeze manifest carries SA-BH-01 and SA-REACH-01 verbatim, and C-P L26 says a miss is never a failure of UNT in general."**
- The slots file does put both readings into the manifest notes. I extracted them from `d3859b42`:
  - SA-BH-01: "Every 120/43 miss is therefore read two ways: as a model failure, or as the missing history/species dependence."
  - SA-REACH-01: "A miss reads three ways: failure of the model at L=4; missing reach …; the missing Bind-history or collective component (SA-BH-01)."
- But the sealed prereg's fixed-list rule (L248) labels every unregistered reading "EXPLORATORY (post-score)", which "never counts as registered". The report lists only registered readings with their tuples ([C-8] item 5).
- So under P2 or P11 the sealed prereg would call R-HIST exploratory, while the same freeze's manifest says the miss reads that way. Two sealed records would disagree.
- E3's "each with its own deciding test" would also lose its link: DT-BHD, DT-U12 and DT-UT1 would not be registered deciding tests of that outcome.
- **The attempt fails.**

**R4. "The A48 gap-filler (C-P L30) settles the silence."** It cannot create a registered reading (L248). It also chooses between readings; it does not decide which readings are registered. **The attempt fails.**

**R5. "Root will catch it when ruling the root items."** No root item puts this question to root. M-3 asks root to "adopt all of it as written" (L75). **The attempt fails.**

**R6. "Codex2's independent round-2 review (0490) did not flag it."**
- Codex2 tested label reachability: "all 13 reading labels have owned synthetic witnesses" (reachability REVIEW L15).
- A label reachable through P1 passes that test. It is not a test of per-pattern coverage against E3.
- The Codex2 checklist and Codex1's rehearsal rough edges are silent on this issue too.
- A missing finding refutes nothing. **The attempt fails.**

**R7. "R-DRIFT already covers reading 2 for P2 and P11."** It does so in part only:
- R-DRIFT is R-REACH's k = 0-drift sub-case, with deciding test DT-S0G;
- the magnitude and finite-size part (DT-U12) has no substitute;
- reading 3 (R-HIST, DT-BHD) and A20's reading 1 (R-UT1, DT-UT1) are wholly absent.

**Precision correction 1:** E3 reading 2 is partly present for P2 and P11 through R-DRIFT. R-HIST and R-UT1 are entirely absent. The verdict is unchanged.

**R8. "A reason is given somewhere."** There is none in the object (§2). The only author statement is 0096 L17, posted after the round-2 bytes and outside the object. It gives r3's planned P14 OUTER_UNSIGNED "R-MF … and no sign-specific reading". That carries the same gap into r3 and supplies no reason.

## 4. Does the evidence say what the finding claims?

**Yes, item by item:**
- **V004 A15 E3 L44–L49:** as quoted. L43 reads "This is binding, and it repeats A10 and A12."
- **V004 A20 L158–L160:** as quoted.
- **V003 A12.3:** L91 is the heading; the three readings are at L92–L94.
- **slots SA-REACH-01 `pre_declared_reading_verbatim`:** present, as quoted. The record labels its section "A12 decision 2", but the text quoted is decision 3. This does not matter here.
- **V003 A10 L38 and CURRENT_INSTRUCTIONS L305:** as quoted.
- **`runs/READINGS_E3_R2A.json` (`ff0355b6`):** as stated. Its TABLE matches PREREG L271–L290 row by row. I reproduced the result independently (§7).

**Precision correction 2.** The finding JSON attributes "P11 'carries R-MF, R-UT1, R-HIST and R-REACH … P2 row should also state E3 readings 2-3'" to "verify_consistency_1 F-c". Those words are in that report's better fix, item 3 (L155–L159). F-c itself (L139–L144) says that R-REACH and R-HIST are left out. The lens REVIEW.md L183 has it right: "§5 F-c and better fix 3".

**Precision correction 3.** A-04's fix (fidelity REVIEW L150) asked for "the R-MF, R-REACH, R-HIST, R-UT1 and R-DRIFT readings as for P1" on P11, as quoted. The closure row for L-C01 also over-claims in a way the finding does not mention. "(the refuter's better fix)" stands for a fix of which only item 1 was adopted, with part of item 2; items 3 to 5 were not adopted.

**Evidence the finding did not cite, and that strengthens it:**
- P5's "as P1" (L284) together with P5's sign-free condition (L224): cases V5 and V6.
- R-SPEC is sign-free on P3, P4 and P12 (L281), and 0096 L17 calls it a reading "that need[s] no sign".
- 0522 L9–L13 and L22. The dispatch that ordered this prereg names the Bind-history and UT-1 readings for "outer-row misses".
- V005 A63 L597 (pinned): R-DRIFT is "a further registered reading for outer-row misses". The base set it is added to is the set of outer-row miss readings.
- V005 L1452: the plug for 0522 is "The two-way reading of outer misses". This line sits in the A65 trailing block after the "**Lanes.**" end-marker (L1418), so §11 does not pin it; it is corroboration only.
- V001 L130 and round-1 L200 labelled P2 "contrary to E2", with no TESTED-NEGATIVE. Round 2 made P2 an E3 failure but did not move the E3 readings with it. This is how the gap arose.

## 5. Is the severity right?

**BLOCKING stands.** The rule is "unsafe or wrong to seal". Five reasons:
1. **The sealed text would contradict binding root text it implements.** A15 E3 is self-declared binding, and A20 amends it; both are listed in [C-P] L24. So are the A10 DECLARED-PREMISE reading and the freeze manifest's own pre-declared readings.
2. **The registered verdict makes it acute.** For two of the three OUTER_FAILURE patterns, the one verdict r2 can register (TESTED-NEGATIVE) would print without the readings that E3 says "stay open" alongside it.
3. **It cannot be repaired after target access.** L248 makes any added reading EXPLORATORY.
4. **A plausible outcome hits it.** The E2/A41-shaped crossing outcome (V3) is a natural result, not an edge case.
5. **The closure claim is false.** This is the residue of a round-1 BLOCKING finding (L-C01). Its refuter predicted exactly this conflict ("P11 as proposed would therefore itself conflict with E3", verify_consistency_1 L144), and the closure calls it FIXED.

**Considered and rejected.**
- *"No count, tier, pattern, headline or verdict changes; the missing tuples would all read CONSISTENT / OPEN."* That is true. But the readings are this document's purpose (0522 L5–L13). The status of the Bind-history reading of the main expected failure mode cannot be left to post-score labelling.
- *"Only the P2 half is open."* For R-UT1 and R-REACH on a pure excess, that part could be SHOULD_FIX if a reason were written. It does not lower the P11 or R-HIST parts.

## 6. Would the proposed fix work?

| fix item | works? | problem |
|---|---|---|
| 1. R-UT1/R-HIST/R-REACH on "P1, P1g, P11" | yes, for P11 today | Listing patterns does not hold up. r3 (0619, 0096) adds P14 OUTER_UNSIGNED, an OUTER_FAILURE pattern, and 0096 L17 gives it "R-MF … and no sign-specific reading". The gap reopens there. |
| 2. P2: status OPEN, or "NOT_ADDRESSED by an excess" with a reason | option (a) yes | Option (b) clashes with [C-3] L241, where NOT_ADDRESSED means "the reading's pattern does not hold". Under P2 the pattern holds, so a second meaning would break the mechanical tuple and the M-12 classifier. R-HIST also cannot be excused for an excess: A10 says "every miss", and SA-BH-01 is in the manifest. |
| 3. a P11g flag (Δ_out < 0) | optional | Not needed to close the defect. "Δ_out < 0" alone is not a full definition (P1g also needs m(TRANSITION) > m(OUTER), L207). If added, it must also go into [C-8] and M-12. |
| 4. P13, P6, P7: model-failure and history/species readings (A10), or a reason | yes | Valid. Cases V7–V9 show the gap: P13 has neither R-MF nor a history reading; P6 and P7 have no history reading outside INNER. This is a separate A10 gap, closer to SHOULD_FIX, and is best handled by one general rule (below). |
| 5. P2 and P11 cases in the M-12 suite | yes | Also add P2+P5 and P11+P5 (V5, V6), and r3's all-unsigned OUTER case. |
| 6. A-04 and L-C01 re-marked PARTLY | yes | Also narrow L-C01's "(the refuter's better fix)" to the items actually adopted, and give a reason for each item not adopted. |
| (missing) | — | The P5 "as P1" dependence on TRANSITION (V5, V6) is not addressed. |

**Better fix:**
1. **Key the E3 readings to OUTER_FAILURE, not to sign patterns.** In [C-3.2], set the pattern cell of the R-UT1, R-HIST and R-REACH rows (L272–L274) to "OUTER_FAILURE (P1, P1g, P2, P11, and any r3 unsigned OUTER pattern)". That is R-MF's trigger. Scope: OUTER rows. Their deciding tests stay DT-UT1, DT-BHD and DT-U12, all NOT SCHEDULED. R-HIST keeps "P1g makes it more specific".
2. **Add one rule to [C-3]**, after L250: "Whenever OUTER_FAILURE holds, R-MF, R-REACH (with R-DRIFT), R-HIST and R-UT1 are reported for the OUTER rows, whatever S(OUTER) and whatever the other zones show." Then rewrite L284 to: "P5: the OUTER rows are read under OUTER_FAILURE; P5 adds R-NAX for the transition zone." That removes the V5/V6 dependence.
3. **If the author holds that an outer excess cannot bear on R-UT1 or R-REACH,** register that mechanically. It can be a score-step against-condition on those two rows ("S(OUTER) = EXCESS", with its source), so the tuple reads INCONSISTENT; or it can be a note in the prior-evidence column. Offer it to root as an option under M-3/M-4. Do not reuse NOT_ADDRESSED. R-HIST stays on every OUTER_FAILURE pattern without condition (A10 L38; the SA-BH-01 manifest note), as R-SPEC does on P3, P4 and P12.
4. **Implement A10's two-way reading by rule.** Every zone that holds a MISS row covered by a pattern carries:
   - R-MF: CONSISTENT only, unless OUTER_FAILURE holds;
   - a history/species reading: R-HIST for OUTER rows; R-SPEC, with DT-T1a, for INNER and TRANSITION rows.

   This covers P13, P6, P7 and the TRANSITION rows of P5. Otherwise, the text must give a reason for each pattern.
5. **Extend the M-12 agreement suite** with V2–V9 below and r3's all-unsigned OUTER case. The expected output of each OUTER_FAILURE case lists all the E3 readings.
6. **Correct the closure table.** A-04 and L-C01 read PARTLY. L-C01's reference narrows to "the refuter's item 1, and item 2 in part". Each item not adopted gets a reason; for example, P11g is optional.
7. **Carry this into r3.** r3 is now being drafted (0619/0096). P14 must carry the same OUTER_FAILURE readings, contrary to 0096 L17's "no sign-specific reading".

## 7. Independent reproduction

**The script:** `tools/vc1_readings_by_zone.py` (`f47abc22…`).
- It is written from the r2 text only: L105–L119, L187–L229, L249 (the zone-scope rule) and L267–L290. It does not import or read the closure-lens tools.
- Inputs are synthetic dimensionless ratios only. Q01 and Q02 are INVALID in every case, and the zone counts are 24/11/8 by index.

**The output:** `runs/VC1_READINGS_BY_ZONE.json` (`09fc0081…`), written with an exclusive create.

| case | patterns | E3 line | readings that may cite OUTER rows | E3 readings 2–3 on OUTER | A20 readings on OUTER |
|---|---|---|---|---|---|
| V1 P1 control | P0, P1 | TESTED-NEGATIVE | R-DRIFT, R-HIST, R-MF, R-REACH, R-UT1 | yes | yes |
| V2 P2 alone | P0, P2 | TESTED-NEGATIVE | R-DRIFT, R-GRID, R-MF, R-S1 | **no** | **no** |
| V3 P11 E2-shaped crossing | P0, P11 | TESTED-NEGATIVE | R-DRIFT, R-GRID, R-MF, R-NAX, R-S1 | **no** | **no** |
| V4 P11 alternating | P0, P11 | TESTED-NEGATIVE | R-DRIFT, R-GRID, R-MF, R-NAX, R-S1 | **no** | **no** |
| V5 the V2 OUTER rows, TRANSITION 6/11 MISS | P0, P2, P13, P5 | TESTED-NEGATIVE | V2's set plus R-HIST, R-REACH, R-UT1 (from P5) | yes | yes |
| V6 the V3 OUTER rows, TRANSITION 6/11 MISS | P0, P11, P13, P5 | TESTED-NEGATIVE | V3's set plus R-HIST, R-REACH, R-UT1 (from P5) | yes | yes |
| V7 TRANSITION-only failure | P0, P13 | NOT_NEGATIVE_AT_OUTER | none | — | — |
| V8 scattered | P0, P7 | NOT_NEGATIVE_AT_OUTER | R-MF, R-NAX | no | no |
| V9 global excess | P0, P2, P3, P13, P6 | TESTED-NEGATIVE | R-DRIFT, R-GEO, R-GRID, R-MF, R-S1 | **no** | **no** |

**A10 two-way check** (a history or species reading in each zone that holds a MISS):
- V7: TRANSITION has neither R-MF nor a history reading.
- V8: no zone has a history reading.
- V9: only INNER has one (R-SPEC). Under the L249 scope rule it cannot cite OUTER or TRANSITION rows.

This agrees with the closure lens's `READINGS_E3_R2A.json` on its four cases. V5–V9 are new.

## 8. Rules kept

- **No target data.** No NGC3198 target, observed velocity or data table was opened. No path containing rotmod, Vobs, MassModels or SPARC was touched.
- **Forbidden paths.** runs_ext/KMAX_A2F10_C5H_RUN_V001 was not read, listed or stat'ed, and no UVT_* item was read.
- **Slots file.** Only its structural-assumption notes subtree was printed, after its sha was checked.
- **Searches.** There was no recursive content search. Files were found by name, with the forbidden name classes pruned, and grep ran only on single named files.
- **Python.** It ran as `-I -B` with the four thread variables set to 1, on synthetic values only. Nothing was launched, and no project calculation was run.
- **Writes.** They went only to this folder. The object and every other file are unchanged. There were no deletes, no moves and no network use.
