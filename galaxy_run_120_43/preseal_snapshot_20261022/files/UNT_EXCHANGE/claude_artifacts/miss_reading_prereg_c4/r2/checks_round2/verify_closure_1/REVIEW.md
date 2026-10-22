# REVIEW — verify_closure_1: the verdict on round-2 closure finding F1

**Who.** A helper of lane Claude4, under dispatches 0585 and 0606, with the 0592 refute-by-default pattern. This is an adversarial verification of one round-2 finding: lens R2-A (closure) F1, in `checks_round2/closure/REVIEW.md` (`566cf50f…`).

**Written:** 2026-10-18T20:44:26Z (`date -u`). The full analysis is in `VERIFY.md` in this folder.

**Object:** `r2/round2/`. All 10 entries of HASHES_R2.txt match. PREREG_MISS_READING_R2.md is `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407`; CLAUSE_SOURCE_MAP_R2.md is `38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201`. The open V005 was read at `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2`, and its A63 section pin matches.

## Verdict on F1

**NOT REFUTED; CONFIRMED in substance. The severity stays BLOCKING.**

**What the text says.** [C-2] L209 makes P2 and P11 the "outer-row failure" of A15 E3, and the E3 line then reads TESTED-NEGATIVE ([C-3] L250; [C-5.3]). But [C-3.2] L272–L274 registers R-UT1, R-HIST and R-REACH for "P1, P1g" only.

**Why that is a defect.** For P2, and for P11 when TRANSITION is hit-dominated, the binding E3 readings 2–3, A20's two readings and A10's history reading are unregistered. After targets they could only be EXPLORATORY (L248). The conflicting texts:
- V004 A15 E3, L43–L49: "binding … Three readings stay open";
- V004 A20, L158–L160;
- V003 A10, L38 and A12.3, L91–L94;
- the SA-BH-01 and SA-REACH-01 notes that slots V003 writes into the freeze manifest;
- 0522, L9–L13;
- CURRENT_INSTRUCTIONS L305.

**The closure claim.** CSM rows A-04 (L83) and L-C01 (L110) say FIXED and give no reason. The object contains no reason anywhere.

**Two points that strengthen the finding:**
1. **P5 already gives these readings to an outer excess or a mixed outer zone.** P5 has no OUTER sign condition, and its row reads "as P1" (L224, L284). Cases V5 and V6: the same OUTER rows get R-UT1, R-HIST and R-REACH when TRANSITION is 6/11 MISS, and lose them when TRANSITION is all HIT (V2, V3).
2. **The history/species reading is sign-free in INNER, but not in OUTER.** R-SPEC sits on P3, P4 and P12 (L281), and Claude4 0096 L17 itself calls it a reading "that need[s] no sign".

**Severity.** P11, the E2-shaped crossing that A41 describes, and the omission of R-HIST against A10 carry BLOCKING. For R-UT1 and R-REACH on a pure excess (P2), a written reason could lower that part to SHOULD_FIX; there is none.

## Precision corrections (none changes the verdict)

1. **E3 reading 2 is partly present for P2 and P11.** R-DRIFT is R-REACH's k = 0-drift sub-case. R-HIST and R-UT1 are wholly absent.
2. **The quoted refuter words are from a different section.** They come from verify_consistency_1's better fix, item 3 (L155–L159), not from F-c (L139–L144). The lens REVIEW.md L183 has this right; the finding JSON does not.
3. **The L-C01 closure row over-claims "(the refuter's better fix)".** Only item 1 was adopted, with part of item 2.

## The fix is not sufficient as written

1. **"P1, P1g, P11" lists patterns.** r3's planned P14 OUTER_UNSIGNED (0619; 0096 L17: "R-MF … and no sign-specific reading") would reopen the gap.
2. **The P2 option "NOT_ADDRESSED by an excess" misuses a tuple word.** [C-3] L241 defines NOT_ADDRESSED as "the reading's pattern does not hold". R-HIST also cannot be excused for an excess, because A10 says "every miss".
3. **P11g is optional and under-defined.**
4. **The P5 "as P1" dependence on TRANSITION is not addressed.**

**Better fix** (VERIFY.md §6):
- Attach R-UT1, R-HIST and R-REACH to OUTER_FAILURE itself, which also covers r3's P14, and state an always-report rule.
- Rewrite P5 so that the OUTER rows are read under OUTER_FAILURE.
- If an excess is held not to bear on R-UT1 or R-REACH, register that as a score-step against-condition or a prior-evidence note, as a root option.
- Implement A10's two-way reading by rule for P13, P6 and P7. This is a separate gap, closer to SHOULD_FIX.
- Add V2–V9 and the unsigned case to the M-12 suite.
- Correct the closure table.

## Files in this folder

- PARTIAL.md, VERIFY.md, REVIEW.md, HASHES.txt;
- V005_SNAPSHOT_AT_VERIFY.md (`7f552858…`);
- `tools/vc1_readings_by_zone.py`, with output `runs/VC1_READINGS_BY_ZONE.json`;
- `tools/slots_sa_notes_vc1.py`;
- `tools/v005_section_pin_vc1.py`.
