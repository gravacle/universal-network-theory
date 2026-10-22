# VERIFY — finding L-C01 (lens consistency): adversarial verification 1

**Who and why.** A helper of lane Claude4, working under dispatch 0592 (which falls under 0585). This check is refute-by-default: it tries to refute one finding from the bytes. It edits nothing outside this folder; Claude4 owns the fix round.

**Written:** 2026-10-18T19:36:10Z (`date -u`). The clock stamps for each step are in PARTIAL.md.

## Verdict

- **L-C01 is CONFIRMED in substance. It is not refuted.**
- **The severity stays BLOCKING.**
- **The finding needs four precision corrections (§3).** None of them changes the verdict.
- **The fix is NOT sufficient as written** (§5):
  - one part does not cure the defect it targets;
  - two parts create or leave a conflict with the binding A15 E3;
  - one part leaves the verdict open to NEAR dilution.
- A better fix is in §5.

## 1. Object and sources (sha256 from bytes)

**The object** (`r2/round1/`). All 10 files listed in HASHES_R2.txt match it, including these:

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` |
| CLAUSE_SOURCE_MAP_R2.md | `b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b` |
| ROOT_ITEMS_R2.md | `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f` |
| NUMBER_PROVENANCE_R2.json | `c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832` |
| tools/check_target_free_c4v001.py | `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7` |

**Sources read:**

| source | sha256 | used |
|---|---|---|
| V004 addendum (frozen) | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` | A15, L26–L50 |
| V003 addendum (frozen) | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` | A10 L38; A12.3 L91–L95 |
| V005 addendum (open), read at 19:26:54Z | `50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477` | A48 L34; A60 L507–L513; A63 L597 |
| V005 addendum, re-read at 19:36:10Z (A93 added) | `6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c` | the same lines; no entry rules on R-MF or the patterns |
| V001 | `6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345` | L9–L13; L126; L164 |
| 0585 | `9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd` | the task |
| 0522 | `30af5d6811788e9bbed4c470dae0ea9bb4ae5230a734fa7940e942b30ed66160` | L22 |
| Lens C REVIEW.md | `a586fb877a54a34c82ed5767877fa7ac94825741dce44ceb96c91facbbf9450e` | L42–L72 |
| Lens C CASES_RESULTS_V2.json | `73adc286a5edb8e6e81a53da3304e1a57d18064e1281b4149b327caffb090576` | C08, C12, C32 |
| Lens C tools/lensc_classifier.py | `a890c8fd468bc5efe544e895ab66ede7c2c58e6a6065a52cbdec3f1ffadf7533` | L248–L263 |

## 2. Is the quoted r2 text there?

Yes. Every quote is verbatim in PREREG r2 (the finding writes "≥" as ">="):
- **[C-P] L17:** "Under A15 E3 an outer-row failure is TESTED-NEGATIVE for exactly the present-mass-only lapse response of the L = 4 coefficient method, at the A2 grid and the calibrated θ."
- **[C-3.2] L195:** "If P1 holds, this is TESTED-NEGATIVE for exactly this scope. | P1 holds | no P1 with N_v(OUTER) ≥ 1 |".
- **[C-3.2] L200:** "**R-MF**, with the opposite sign: overshoot."
- **[C-8] L347:** "\"TESTED-NEGATIVE\" only for R-MF, within its stated scope".

## 3. Is it really defective? Refutation attempts

**R1. "C-3.2 says *if*, not *only if*, so the two clauses do not conflict."**
- Literally true: L195 states a sufficient condition.
- The operational text, however, gives no other path to the verdict:
  - [C-5.3] L260: "E3 is the reading rule, applied through §3."
  - [C-8] L339–L340: readings are reported only "For each pattern" in "Every pattern that holds".
  - ROOT_ITEMS M-12, L218: the sealed classifier implements "§1–§6 exactly". C-P is not in §1–§6.
- So P1 is the only route to TESTED-NEGATIVE that the text makes operational.
- **The attempt fails.** Correction 1: the finding's "grants the verdict only under P1" describes the operational text accurately, but it overstates the literal wording of L195.

**R2. "C-P alone still gives the verdict under P2 and in the mixed case."**
- C-P is a statement of principle. It has no slot in the report (C-8), and C-5.3 routes E3 through §3.
- In the mixed case, R-MF is attached to no pattern that holds. Yet C-8 L347 allows the word "TESTED-NEGATIVE" only for R-MF.
- **The attempt fails, but it narrows claim (b).** Correction 2: (b) should read "no registered path to the verdict", not "no verdict". The verdict is indeterminate, not absent.

**R3. "The A48 gap-filler (C-P L21) settles it."**
- L21 applies only "Where this text is silent".
- Under P2 the text is not silent: L17 speaks generally and L195 speaks for P1.
- In the mixed case, a gap-filler cannot create registered readings. L170 says: "Any reading proposed after targets are opened is labelled **EXPLORATORY (post-score)** and never counts as registered."
- **The attempt fails.**

**R4. "A15 E3 means the E2 deficit only, so a P1-only trigger is faithful."**
- Every binding source is sign-agnostic:
  - V004 L44: "An outer-row failure would be TESTED-NEGATIVE for exactly this";
  - V003 A10 L38: "Every 120/43 miss is therefore read two ways";
  - V003 A12.3 L91: "A miss reads three ways";
  - r2's own L17.
- The internal conflict in r2 exists whatever E3 intends.
- **The attempt fails.**

**R5. "Claim (a), that R-MF is consistent and against at once, is the lens's own interpretation."**
- This is partly true. Lens C's classifier, at L259 and L263, evaluates the P1-row against-column whenever P1, P2 or P6 holds. Under pattern-level semantics (C-8 L339–L340), R-MF under P2 is only "consistent".
- But under that semantics the P1-row against-column is dead. In my enumeration (§6), it is true while the P1 row is reported in 0 of 1,679,616 outcomes.
- The column's own wording ("no P1") only makes sense if it is evaluated per reading. The text never says which semantics applies.
- **The attempt fails.** (a) and (c) are the two horns of one ambiguity. Correction 3: (a) should be stated as an ambiguity between the two semantics, not as a fact.

**R6. "(b) is an exotic edge case."**
- No. Take a model curve that falls through a flat target inside OUTER: excess near 30 kpc, deficit near 44 kpc. This is the shape A15 E2 expects (V004 L38: "will fall below flat at large R").
  - My case V2 builds it with synthetic r = +3, +2, +1.5, +0.5, −0.5, −1.5, −2, −3 in radius order, with INNER and TRANSITION all HIT.
  - Result: OUTER has 6/8 MISS, S = CENTERED, Δ_out = −3.5, and the patterns are **[P0] only**.
  - P1g cannot fire either, because GROWING needs S(OUTER) = DEFICIT (L145).
- The enumeration (§6) puts **835,380 of the 1,531,904 miss-dominated OUTER vectors** in the gap. The fraction depends on the grid, but the gap is a region, not a knife edge.
- When TRANSITION is not hit-dominated, P5 covers the case (my V3). So the finding's "can" is correct.
- Correction 4: the finding JSON says "P5 needs INNER hit-dominated". In C08 INNER *is* hit-dominated; the condition that fails is "TRANSITION not hit-dominated" (L156). The lens REVIEW.md L54 has this right.

**R7. Does the cited evidence say what the finding claims?**
- **V004 A15 L43–L44:** yes, verbatim (L43 heading "E3, how a failure is read. This is binding, and it repeats A10 and A12."; L44 as quoted).
- **CASES_RESULTS_V2.json:** yes.
  - C08: patterns [P0]; OUTER M = 8, S = CENTERED; a GAP event.
  - C12: [P0, P2]; R-MF candidates ['consistent', 'inconsistent']; TESTED_NEGATIVE_per_C32 false.
  - C32: [P0, P2, P3, P6]; the same R-MF result.
- **Caveat:** the CONFLICT 'C-P vs C-3.2' event is a fixed rule. It fires whenever OUTER is miss-dominated without P1 (lensc_classifier.py L252–L256). It restates the finding; it is not independent evidence.
- The patterns themselves are mechanical. I reproduced C08 and C12 independently (V1, V4).
- Immaterial: C08's m is −7.8e-16 (floating point), not exactly 0.0.

**Evidence that strengthens the finding (the lens did not cite it):**
- **L170 + V004 L46–L49.** In the mixed case, every reading of the OUTER misses is EXPLORATORY, so none of the "Three readings [that] stay open" under binding E3 is registered for it.
- **L199.** R-DRIFT's own consistent-if is the sign-agnostic "OUTER miss-dominated", narrowed by a parenthesis "(P1, P1g or P2)". V005 A63 L597 registers R-DRIFT for "outer-row misses".
- **0522 L22:** "For each miss pattern, give its candidate readings and the **deciding test**".
- **History.** V001 L126 already had the P1-only trigger, and V001 L164 already routed E3 "through §3". V001 L9–L13 had no E3 sentence in its principles. r2 added the sentence (CSM L15: "quotes the A15 E3 scope"), which makes the conflict visible. Root never ruled on the trigger: V005 A60 L507–L513 records only V001's open items.

## 4. Is the severity right?

**BLOCKING stands.** The rule is "the prereg would be wrong or unsafe to seal", and that holds here:
1. TESTED-NEGATIVE is the only verdict this text can register (L347). E3 (V004 L43) is binding.
2. If the text is sealed as written, the binding E3 verdict has no operational trigger under P2 or in the mixed case. A sealed M-12 classifier built from §1–§6 would print no verdict there. A hand reader would have to choose, after the targets are opened, between C-P and §3.
3. In the mixed case, the outer misses get no registered reading at all, against A10, A12.3, A15 E3 and 0522.
4. That case includes the E2-shaped outcome (V2), not only scatter.

**Considered and rejected:** "the score and headline are unaffected (I-5)". That is true, but the readings are this document's whole purpose.

## 5. Would the proposed fix work?

**F-a. A sign-agnostic trigger, "iff OUTER miss-dominated".** It closes P2 and the mixed case. Two problems remain:
- **(i) C-P L17 is not in the fix's edit list.** If L17 keeps "an outer-row failure is TESTED-NEGATIVE", the conflict comes back in a new form.
  - V5 has 2 of 8 OUTER rows MISS. Literal C-P gives TESTED-NEGATIVE; the fix gives no verdict.
  - The trigger is an operational reading of a binding root text, so root should rule on it as such, not only under M-3.
- **(ii) NEAR dilution.** M(OUTER) excludes NEAR rows, yet the reference member fails on those rows (L86: "A NEAR row's LADDER tier stays MISS_WORST_TIER").
  - V6: the reference member fails 5/8 OUTER rows with S = DEFICIT, but M = 3 < 4. The fix gives no verdict, and only P7 holds.
  - P1 already has this problem, but the fix makes this test the sole trigger of the one verdict.

**F-b. The replacement against-column ("OUTER not miss-dominated, with N_v(OUTER) ≥ 1") does not cure (c).**
- P1 implies OUTER miss-dominated, so the new column is false whenever the P1 row is reported.
- The enumeration confirms it: **0 of 1,679,616** outcomes, the same as for the current column.

**F-c. P11 OUTER_MIXED, carrying R-MF, R-NAX and R-DRIFT.** It closes the OUTER hole, but it leaves out two of the three readings that binding E3 says "stay open" for an outer-row failure:
- V004 L48: finite reach (R-REACH);
- V004 L49: a missing Bind-history component (R-HIST);
- A12.3 (V003 L91–L94) gives the same three-way reading.

For the E2-shaped crossing case (V2), these are the most pertinent readings. P11 as proposed would therefore itself conflict with E3. It must also be propagated to L199 (the R-DRIFT parenthesis), L257 (the E2 list "P1/P1g/P2/P8/P9") and the §9 row.

**F-d. Pointing C-8 to the trigger.** This part is fine.

**Better fix:**
1. **One E3 verdict line, outside the pattern table, always reported** (add it to C-5.3 and to the C-8 list), for the frozen reference member:
   - **TESTED-NEGATIVE (A15 E3 scope)** iff N_v(OUTER) ≥ 1 and OUTER is failure-dominated: M(OUTER) + N(OUTER) ≥ N_v(OUTER)/2. This is the stricter A48 side; if root prefers M alone, the choice goes in the §9 residual risks.
   - **NOT_NEGATIVE_AT_OUTER** iff N_v(OUTER) ≥ 1 and the trigger is false.
   - **NOT_TESTABLE** iff N_v(OUTER) = 0 (P9).
   - The line always prints S(OUTER), Δ_out, N_v, H, N, M, and I per reason.
2. **Rewrite C-P L17 and C-3.2 L195** to cite that line. Delete the P1-row against-column. In the P2, P6 and P7 rows, R-MF cross-references the line.
3. **Add P11 OUTER_MIXED** (OUTER miss-dominated and S(OUTER) = CENTERED):
   - it carries R-MF, R-UT1, R-HIST and R-REACH (as in P1, with their deciding tests), plus R-DRIFT and R-NAX;
   - flag **P11g** when Δ_out < 0;
   - add P11 to L199, L257 and §9.
   - Now that P2 becomes an E3 failure, the P2 row should also state E3 readings 2–3 explicitly, as OPEN or as "not addressed by an excess".
4. **Add a root item** for the operational meaning of A15 E3's "an outer-row failure". Options:
   - (α) M-dominated;
   - (β) non-HIT-dominated;
   - (γ) any failing OUTER row.

   Root rules on it before the seal, together with M-3.
5. **Add to the M-12 synthetic tests:** P2; P11 (alternating and crossing); V5; V6.

**Inherited, not new:** INVALID OUTER rows stay outside the trigger. This is consistent with A15 E2 (V004 L40) and with P9, but root may want the verdict line to say so explicitly.

## 6. Independent reproduction

**The script:** `tools/vc1_patterns.py` (`c40fe674…`).
- Written from the r2 text only: L79–L82, L134–L161 and L195–L207. It does not import or read the Lens C tools.
- Synthetic r and NEAR flags only. The radii are synthetic and ascending; only their order matters.

**Output:** `VC1_CASES.json` (`e2a5039a…`), written with an exclusive create.

| case | OUTER (M/N/H of N_v) | S(OUTER) | patterns | explicit C-3.2 TN | literal C-P TN | fix TN |
|---|---|---|---|---|---|---|
| V1 C08 replica | 8/0/0 of 8 | CENTERED | P0 | no | yes | yes |
| V2 crossing inside OUTER | 6/0/2 of 8 | CENTERED | P0 | no | yes | yes |
| V3 crossing, TRANSITION not hit-dominated | 6/0/2 of 8 | CENTERED | P0, P5 | no | yes | yes |
| V4 C12 replica | 8/0/0 of 8 | EXCESS | P0, P2 | no | yes | yes |
| V5 two OUTER misses | 2/0/6 of 8 | CENTERED | P0, P7 | no | yes | **no** |
| V6 NEAR dilution | 3/2/3 of 8 | DEFICIT | P0, P7 | no | yes | **no** |
| V7 P1/P1g | 8/0/0 of 8 | DEFICIT | P0, P1, P1g | yes | yes | yes |

**Enumeration.** Every OUTER vector over the grid {−3, −2, −0.5, 0.5, 2, 3}^8, with INNER and TRANSITION all HIT: 1,679,616 outcomes.

| count | outcomes |
|---|---|
| miss-dominated | 1,531,904 |
| P1 | 348,262 |
| P2 | 348,262 |
| gap (miss-dominated with no OUTER pattern) | 835,380 |
| P1-row against-column true while P1 is reported (current text, and the fix's replacement) | 0 |

## 7. Rules kept

- No NGC3198 target, observed velocity or data table was opened. No rotmod, Vobs, MassModels or SPARC path, no runs_ext path and no UVT_* item was touched. Nothing was launched.
- Writes were made only in this folder. The object and every other file are unchanged.
- Python ran as `-I -B` with the four thread variables set to 1, on synthetic data only.
