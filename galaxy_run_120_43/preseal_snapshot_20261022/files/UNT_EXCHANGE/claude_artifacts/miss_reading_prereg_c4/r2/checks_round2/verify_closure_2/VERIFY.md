# VERIFY — closure lens finding F2 (round 2): adversarial verification 2

**Who and why.** A helper of lane Claude4, under dispatches 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`) and 0606 (`dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e`), with the 0592 refute-by-default pattern. This check tries to refute one finding from the bytes. Nothing outside this folder was edited; Claude4 owns the fix round.

**Written:** started 2026-10-18T20:28:46Z; this file written from 20:46:28Z (`date -u`; step stamps in PARTIAL.md).

## Verdict

- **F2 is CONFIRMED in substance. It is not refuted.** Every quote is verbatim at the cited line, and the contradiction follows from the round-2 rules alone. I reproduced it with my own implementation, written from the round-2 text.
- **The severity stays BLOCKING.** F2 reintroduces the defect class of round-1 BLOCKING L-C01: the one registered verdict has two triggers that disagree on a reachable outcome. Root has already ruled the same item blocking and ordered r3 (V005 A98.2; dispatch 0619; Codex2 0490).
- **Four precision corrections (§5).** None changes the verdict:
  - the null-ratio route is practically unreachable on v003g inputs, and the LATE-gate route is the real one;
  - "every gate row is LATE" holds for gates first registered at RUNBOOK step 4, and LATE-ness has no byte carrier;
  - every late-gate removal goes against the model, except through the U1 contradiction itself;
  - late rows also **add** patterns: P10, P13, zone patterns and P5.
- **The fix is NOT sufficient as written** (§6). It offers option (a) "Alternatively" option (b). Option (a) alone, counts-only OUTER_FAILURE, settles the E3 line, but it leaves:
  - the coverage property false;
  - INNER unread;
  - R-MF reading TESTED-NEGATIVE while its own status tuple reads NOT_ADDRESSED.

  Both halves together close every hole I tested (0/20000). Five more items are needed; the better fix is in §6.

## 1. Bytes verified (sha256 from bytes)

**The object** (`r2/round2/`). All 10 entries of `HASHES_R2.txt` (`2e3cf0c60088f23a9530a3ab5b8d8ec1a2d8c5184a7eeff11f726fafa964c6fd`) match `shasum -a 256` at 20:28Z:

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

**Sources read:**

| source | sha256 | lines used |
|---|---|---|
| closure lens REVIEW.md | `566cf50f5613161c6d1316911a44f2555004144c3e17c62a4c0dce91197f0d48` | F2, L204–L234; closure rows L67, L84, L94, L97, L112, L119 |
| closure runs/PATTERNS_UNDEFINED_SIGN_R2A.json | `be3a8b59776c39fd22bd1f189de8768ed6cf80f93d2a32dd7f000c42ecc6d9f0` | U1, U2, U3, L1–L4 |
| closure tools/patterns_r2_closure_c4.py | `bd253d8cac5ca99041dd03d611d571847b4468d5dee6fb833d4a3c3e6a0e1dca` | read in full; not reused |
| V005 addendum (open), read at 20:35:17Z | `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2` | A98, L948–L959 (kept as `V005_SNAPSHOT_7f552858.md`) |
| V005 addendum, re-read at 20:45:28Z | `70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e` | adds only A101 (B2 record, case block, A90 LO I1-T closed, registry V008); nothing on F2 (kept as `V005_SNAPSHOT_70a48f51.md`) |
| V004 addendum (frozen) | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` | A15 E2 L38–L41, E3 L43–L49 |
| V003 addendum (frozen) | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` | hash only |
| RUNBOOK_V001 | `9557b5aa06d19fa2677ec9af033fd4cdb5a6bff2dfa1f519dd4c0d70718f6d4b` | L7–L16 (steps 1–5) |
| freeze module v003g | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` | `_ladder_row` L4011–L4031; `_score_members` L4036–L4052; target checks L4201–L4214; gate schema L1578; root gates L1709–L1724; `_authorized_row_registration` L1788–L1798; producer rows L1840–L1858 |
| dispatch 0619 | `238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99` | whole file |
| dispatch 0603 | `e4e94fa616457a2df662550febd528ffef46ae203fdec94b0054cb8b5d221a16` | step numbering ("Synthetic step-5 outputs"; freeze = steps 6–7) |
| dispatch 0623 | `3cf31cd8299d75aac555eefa6591ab306f48aec0a9b8205c3d43369df1267cc1` | checked: unrelated (step-4 guard) |
| Codex2 0490 | `3a922168f800de5ae9fff2ba1cb55af2f55d7ae4290a75b14a0ca2daa36a2649` | whole file |
| Codex2 REVIEW_CX2V001.md | `7e3b6211ded52e4212c8534b7dad04bc9334ea5c458cdc8de6c8545c19e5af71` | L6, L8 (CX2-MR2-REACH-B1) |
| Codex1 rehearsal classifier (implementation B) | `28aa1c12915f40b17fe8e45f1feea7a998cce441cf82a8556a7d90a3f5164b1d` | L31–L32, L36–L38 |
| round-1 consistency REVIEW.md | `a586fb877a54a34c82ed5767877fa7ac94825741dce44ceb96c91facbbf9450e` | L-C01 L42–L72; L-C04 L125–L143; L-C19 L357–L361; L-C26 L394–L397 |
| round-1 targetfree REVIEW.md | `2eab55194d7ec2d7783ebed259d8afb2794de45bd9d383cefc3dc5fd3c7537b6` | B-3 L96–L117 |
| round-1 fidelity REVIEW.md | `41cbea3bb48839fa384b9878a247b6e53adbaeba216dd7d76b5b469e59bc3ed0` | A-04 L130–L152 |
| CURRENT_INSTRUCTIONS.md | read at start | program context only |

## 2. Is the quoted text there?

Yes. All of it is verbatim in PREREG r2 (`97d5ce33…`):
- **[C-2] L209:** "**OUTER_FAILURE.** This is the "outer-row failure" of A15 E3, registered here as: OUTER is miss-dominated, whatever its sign class. It holds exactly when one of P1, P2 or P11 holds."
- **[C-2] L212:** "**Coverage.** Every outcome with at least one MISS satisfies at least one of these: a zone pattern (P1, P2, P11, P3, P4, P12 or P13), or P7."
- **[C-1.1] L119:** "A VALID row whose `sigma_ratio` is null (v003g NON_FINITE_SIGMA_RATIO) is a MISS with sign UNDEFINED. It counts in N_v(Z) and M(Z), and it is left out of m(Z) and Δ_out."
- **[C-4] L324:** "For this document's counts and patterns, each LATE-gate row counts as a non-INVALID MISS row with sign UNDEFINED. A late gate can therefore never remove a pattern or create P9."
- **[C-9] L487:** "| Choosing which pattern to report | Every applicable pattern is reported. The coverage property holds (§2), undefined quantities make conditions false, and ties go to the stricter side. |"
- **[C-9] L492:** "| A gate added after the predictions removes a pattern | LATE-gate rows count as MISS rows for this document (§4). |"

The closure rows the finding names all read FIXED in `CLAUSE_SOURCE_MAP_R2.md`:
- A-04, L83;
- B-3, L100;
- L-C01, L110;
- L-C04, L113;
- L-C19, L128;
- L-C26, L135.

## 3. Is it really defective? Refutation attempts

**The logic, from the text alone.** Take an OUTER zone whose non-INVALID rows all have r_q undefined.
- By L119/L324 every such row is a MISS, so M(OUTER) = N_v(OUTER) ≥ 1, and OUTER is miss-dominated (L197).
- m(OUTER) has no defined value, so it is UNDEFINED (L195), and so is S(OUTER) (L196).
- P1, P2 and P11 each need S(OUTER) to equal a class (L217–L219), and "Any condition that uses an UNDEFINED quantity is false" (L201). So all three are false.
- The first sentence of L209 is then true and the second false. E3 (L358–L359) reads TESTED-NEGATIVE under the first and NOT_NEGATIVE_AT_OUTER under the second.
- P7 needs "no zone miss-dominated" (L226), so it is false too. L212 then fails whenever no other zone is miss-dominated.

**R1. "The first sentence of L209 is the definition; the second is only a remark."** This fails. Even with that reading:
- L250 makes R-MF TESTED-NEGATIVE "if and only if OUTER_FAILURE holds".
- R-MF's status tuple is NOT_ADDRESSED "when the reading's pattern does not hold" (L241). R-MF's patterns are P1/P1g/P2/P11 (L271), P5 through "as P1" (L284), P6 (L286) and P7 (L287), and none of them holds.
- So the report would print an R-MF TESTED-NEGATIVE whose own tuple reads NOT_ADDRESSED.
- L212 stays false, and so does M-3's claim (ROOT_ITEMS L72) that P11–P13 "together give the coverage property".

**R2. "L201 also falsifies the sign-agnostic sentence, so there is no conflict."** This fails. "Whatever its sign class" uses no sign quantity; it uses only N_v and M. And if L201 did apply:
- OUTER_FAILURE would be "reported as UNDEFINED" (L201), but the E3 line has no UNDEFINED value (L358–L360);
- 8/8 OUTER misses would read NOT_NEGATIVE_AT_OUTER, against the binding A15 E3 (V004 L44: "An outer-row failure would be TESTED-NEGATIVE") and against M-3 L71 ("OUTER_FAILURE := OUTER miss-dominated, of any sign").

**R3. "The A48 gap-filler ([C-P] L30) picks the less favourable reading."** This fails:
- A48 applies "Where this text is silent". Here the text speaks twice and contradicts itself, and the mechanical classifier (M-12) needs one rule, not a principle applied after the score.
- Even if A48 picked TESTED-NEGATIVE, the coverage property and the R-MF tuple conflict (R1) would remain, and an all-undefined INNER zone would still have no pattern and no reading.

**R4. "The binding M-12 classifier removes the ambiguity."** This fails:
- ROOT_ITEMS L233: "A disagreement means the text is ambiguous; the text is fixed before the seal". M-12 itself requires the text fix.
- The agreement list (L224–L231) has no undefined-sign or late-gate case.
- Two implementations could both code the first sentence, agree, and still violate L209 and L212.
- Implementation B today (`28aa1c12…` L32) stops with CLASSIFICATION_INPUT_DEFECT on a non-numeric r. That is the stop round-1 L-C19 proposed, not round 2's MISS-with-sign-UNDEFINED rule, so A and B would disagree on null-ratio rows. B also has no LATE-gate branch.

**R5. "An all-undefined zone is unreachable."** This partly succeeds, but it does not refute.
- **Null ratios are practically unreachable on real inputs.** The module refuses a target velocity that is not finite and a σ that is not finite and > 0 (`48a1e48a…` L4209–L4212). It refuses a non-finite valid prediction (L1856–L1857). So `r = residual / sigma` (L4016) is non-finite only on overflow: Codex2's witness needed σ = 1e-320 (REVIEW_CX2V001 L6).
- **The LATE-gate route is ordinary.**
  - RUNBOOK_V001 L9 (step 1) saves each member's raw forward result. Step 4 (L15) is where "Root adopts … registration roster", binding the "approved gates". These forward results are the step-5 outputs (dispatch 0603 item 1 calls them "Synthetic step-5 outputs").
  - By [C-4] L322, any gate first registered at RUNBOOK step 4 is a LATE gate.
  - A producer row that is INVALID for a non-built-in reason refuses unless a root gate lists it (`V010_INVALID_NOT_ROOT_ROSTERED`, L1797). Root must then register the gate late, or have no score at all.
  - One concrete configuration: OUTER rows Q40–Q43 beyond a built-in cut, and Q36–Q39 under one late gate. That gives the U1 state (case `U1Lc` below). Gating the same rows on time gives P9 and NOT_TESTABLE.

**R6. "A late gate cannot remove a pattern in the sense that matters (steering)."** This partly succeeds, but it does not refute.
- Relative to on-time registration, the removals I found are P5, P7, P8 and P9 (§4). Each moves the reading against the model, since late rows add only MISS rows.
- The one exception is the U1 contradiction itself: under the second sentence of L209, a late gate turns NOT_TESTABLE into NOT_NEGATIVE_AT_OUTER, which is favourable to the model.
- The literal guarantees at L324 and L492 are false. On its own this sub-part would be SHOULD_FIX. It is the E3 and coverage contradiction that makes F2 BLOCKING.

**R7. "A pre-score stop catches it."** This fails. The stop list ([C-1.1] L122–L127) has no undefined-sign condition. LATE status is target-free, so a stop could catch the all-LATE case before target access, but none is registered.

## 4. Reproduction (independent, synthetic only)

- **Tool:** `tools/verify_f2_patterns_vc2b.py` (`952efb9af7da7b1b48a1558ad1d7fdff50892c06c1a183b2a2dd224493185ec8`). I wrote it from the round-2 text: [C-1.1], [C-1.3] membership by id, [C-2], [C-3] R-MF tuple and verdict, [C-4] late gates, and [C-5.3].
- **Inputs:** synthetic row kinds and r values, with R_q = q.
- **Fence:** an audit hook refuses every open except its own exclusive output.
- **Output:** `runs/F2_PATTERNS_VC2B.json` (`0174e00919a8f03a9ee736ba79eaa8adb837d9a031b9534b610c0e6a098ea9c2`).
- **An earlier run is superseded.** The first version (`verify_f2_patterns_vc2.py` `d5fd13f7…` → `runs/F2_PATTERNS_VC2.json` `969ba3fa…`) left P5 out of R-MF's patterns. It is kept, but not of record.

Each run uses INNER Q01–Q02 as built-in INVALID; other rows are hits at r = 0.3 unless stated.

| case (R2 rules) | patterns | OUTER_FAILURE, sentence 1 / sentence 2 | E3 | R-MF tuple | L212 holds | miss-dominated zone with no zone pattern |
|---|---|---|---|---|---|---|
| U1N: OUTER 8 null-ratio rows | P0 | True / False | TESTED-NEGATIVE / NOT_NEGATIVE_AT_OUTER | NOT_ADDRESSED | False | OUTER |
| U1L: OUTER 8 late-gate rows | P0 | True / False | the same split | NOT_ADDRESSED | False | OUTER |
| U1G: the same rows gated on time | P0, P8, P9 | False / False | NOT_TESTABLE | NOT_ADDRESSED | True | — |
| U1Lc: Q40–Q43 built-in cut, Q36–Q39 late gate | P0 | True / False | the same split | NOT_ADDRESSED | False | OUTER |
| U1Lt: as U1L, with TRANSITION 6/11 misses | P0, P5, P10, P13 | True / False | the same split | CONSISTENT (via P5) | True | **OUTER** (L212 holds through P13 while OUTER has no pattern) |
| U2L / U2N: INNER 22 late or null rows | P0 | False / False | NOT_NEGATIVE_AT_OUTER | NOT_ADDRESSED | False | INNER |
| controls C1–C3: one defined OUTER row or more | P11 or P1 | equal | equal | CONSISTENT | True | — |

Late gate against the same rows gated on time:

| pair | removed by the late gate | added | E3, on time → late |
|---|---|---|---|
| U1G → U1L | P8, P9 | — | NOT_TESTABLE → TESTED-NEGATIVE / NOT_NEGATIVE_AT_OUTER |
| P5G → P5L (11 INNER gate rows) | P5 | P12 | TESTED-NEGATIVE both |
| P8G → P8L (2 OUTER gate rows) | P8 | P7 | NOT_NEGATIVE_AT_OUTER both |
| P7G → P7L (OUTER: 1 miss, 4 hits, 3 gate rows) | P7 | P11 | NOT_NEGATIVE_AT_OUTER → TESTED-NEGATIVE |
| P10G → P10L (Q25 gated) | P8 | **P10, P7** | NOT_NEGATIVE_AT_OUTER both |

This agrees with the lens's U1, U2, L1/L2 (P5 removed) and L3/L4 (P8 removed), with different numbers.

**Random sweep.** 20,000 synthetic outcomes, seed 20261018. The counts reflect the generator, not real-world odds.

| rule set | sentence 1 ≠ sentence 2 | L212 false | miss-dominated zone with no zone pattern | R-MF TESTED-NEGATIVE but tuple NOT_ADDRESSED |
|---|---|---|---|---|
| R2 as written | 6231 | 91 | 6991 | 6196 |
| fix option (a) only (FIXA) | 0 | 91 | 6991 | 6196 |
| fix (a) + (b): P14 OUTER_UNSIGNED, P15 INNER_UNSIGNED | 0 | 0 | 0 | 0 |

- Every R2 mismatch had no defined OUTER row (0 counterexamples), and every L212 failure had an all-undefined miss-dominated zone (0 counterexamples). So the hole is exactly the "all-undefined zone" class.
- In 35 of the 20,000 outcomes, P5 holds with S(OUTER) UNDEFINED, under R2 and under the fix alike.

## 5. Precision corrections to the finding (none changes the verdict)

1. **Null-ratio rows.** "(a null sigma_ratio or a LATE gate)" is correct as text, but the null-ratio route needs overflow on v003g inputs (§3, R5). The realistic trigger is LATE gates.
2. **Every gate row LATE.** "Under RUNBOOK_V001 gates are approved at step 4 …, so every gate row is a LATE, undefined-sign row" holds for gates first registered at RUNBOOK step 4, the only gate step the runbook has.
   - A gate document registered before step 5 launches would be on time. The finding's own fix item 3 says so.
   - A gate document (schema `REGISTERED_INVALID_ROW_GATE_CX3V001`; module L1578, L1713–L1716) has no time field, and the producer's gate pin is "optional redundant metadata, never authority" (L1848).
   - So nothing in the bytes yet lets M-12 decide LATE against on time.
3. **Removals.** "A LATE gate does remove P5, P7 and P8" is right, and P9 too (U1G → U1L). By the same rule, but not run here, P0 can go in a scope with no built-in INVALID row, such as a STAGE0 twin. Every one of these removals is against the model except through U1 (§3, R6).
4. **Additions.** Late rows also add patterns:
   - **P10**, when Q25 is gated late. R-TSR then cites a row that has no prediction ([C-3.2] L290).
   - **P13** and zone patterns.
   - **P5**, with an unsigned OUTER (U1Lt). P5 then brings P1's deficit-specific readings (R-UT1, R-HIST, R-REACH; L284 "as P1") onto rows with no sign.

## 6. Would the fix work?

- **Option (a) alone is insufficient.** "Define OUTER_FAILURE on counts only … Alternatively, add P14 … P15": the sweep's FIXA row shows that (a) settles the E3 line but leaves L212 false, INNER unread, and R-MF TESTED-NEGATIVE while NOT_ADDRESSED.
- **Both halves together are sufficient for the logic.** All counters read 0/20000.
- **The "Restate C-4 L324" item is incomplete.** It lists removals only; late rows also add P10, P13, P5 and zone patterns (§5.4).
- **One consequence is new as a determinate reading.** With the fix, an E3 TESTED-NEGATIVE can rest entirely on late-gate rows that have no prediction, where the same rows gated on time read P9 and NOT_TESTABLE (U1L against U1G). That follows the B-3 anti-steering intent, and it is the less favourable reading. But it should be recorded for root to rule on knowingly, like the L-C27 consequences at [C-9] L500.

**Better fix (for r3).**
1. **Do both halves, not either.**
   - Keep the counts-only OUTER_FAILURE: N_v(OUTER) ≥ 1 and M(OUTER) ≥ N_v(OUTER)/2.
   - Add **P14 OUTER_UNSIGNED** (OUTER miss-dominated, S(OUTER) UNDEFINED) and **P15 INNER_UNSIGNED**.
   - Restate L209's second sentence as "It holds exactly when one of P1, P2, P11 or P14 holds".
   - Extend L212's list with P14 and P15, and state coverage per zone: every miss-dominated zone has a zone pattern.
2. **Readings.**
   - P14 carries R-MF (TESTED-NEGATIVE through OUTER_FAILURE), R-DRIFT, and the E3 readings 2–3 (R-REACH, R-HIST; this is F1's fix) as OPEN, with no sign-specific gloss.
   - P15 carries INNER's readings (R-GEFF, R-ML, R-SPEC, R-GEO, R-NAX).
   - Re-key P5's OUTER readings to "as the OUTER pattern that holds (P1, P2, P11 or P14)", not "as P1".
3. **Restate [C-4] L324 truthfully.** Suggested text: "late-gate rows add MISS rows only. Relative to on-time registration they can remove P0, P5, P7, P8 and P9, and add zone patterns, P5, P10 and P13. Every such change is toward the less favourable reading. They never add a HIT." Also state whether a reading may cite a late-gate row; the recommendation is that R-TSR and P7's row-level R-MF may not cite a row that has no prediction.
4. **Make LATE-ness mechanical.**
   - A gate is on time if and only if its document sha256 is pinned in a root entry stamped (`date -u`) before the first step-5 output exists.
   - The seal or freeze entry lists those shas, and M-12 takes the list as an input. Every other root-listed gate is LATE.
   - State that under RUNBOOK_V001 a gate first registered at step 4 is LATE.
5. **E3 disclosure.** The E3 line also prints n_defined(OUTER), the late-gate count and the null-ratio count. Add to [C-9] L500 a fourth recorded consequence: "an OUTER zone whose non-INVALID rows are all late-gate rows reads P14 and TESTED-NEGATIVE; the same rows gated on time read P9 and NOT_TESTABLE". Root rules it under M-3.
6. **Correct the claims and the closure table.** Correct [C-9] L487 and L492. Correct ROOT_ITEMS M-3 L72 ("together give the coverage property"). Re-mark A-04, L-C01, L-C04, L-C19, B-3 and L-C26 as PARTLY in the closure table.
7. **The M-12 agreement suite.** Add U1N, U1L, U1Lc, U1Lt, U2L, U2N and the on-time/late pairs for P5, P7, P8, P9 and P10, with a per-zone coverage assertion. Bring implementation B's null-ratio stop (`28aa1c12…` L32) to the final rule.

## 7. Outside F2 (for the fix round, one line)

V005 A101 (in `70a48f51…`) closes the A90 step-5 LO I1-T item as TESTED PASS (Codex1 0066). PREREG [C-I6] L79 and D-4 L451 still describe it as to be ruled, so M-6 item 4 needs a revision or a no-change note.

## 8. Rules kept

- **Data.** No NGC3198 target or observed-velocity data was opened, and no path containing rotmod, Vobs, MassModels or SPARC. runs_ext/KMAX_A2F10_C5H_RUN_V001 was not read, listed or stat'ed. No UVT_* file was read.
- **Search.** There was no recursive content search. Every grep ran on a single named, checked file.
- **Actions.** Nothing was launched, there was no project calculation, and there was no network access. Nothing was deleted or moved outside this folder; the two V005 snapshots were renamed inside it with `mv -n`.
- **Python.** It ran as `-I -B`, numpy only, with the four thread variables set to 1, on synthetic data. `taskpolicy -b` was accepted.
- **Writes.** Writes went only to this folder.
