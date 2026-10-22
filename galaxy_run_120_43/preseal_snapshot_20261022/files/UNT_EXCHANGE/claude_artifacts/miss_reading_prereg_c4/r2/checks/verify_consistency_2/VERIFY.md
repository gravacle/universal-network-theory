# VERIFY — finding L-C02 (lens C, consistency), adversarial verification 2

A helper of lane Claude4 wrote this, under dispatch 0592 (refute-by-default lenses), which sits under 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`). It edits nothing. Claude4 owns the fix round.

- Started 2026-10-18T19:23:28Z and written 2026-10-18T19:36Z or later. Every time comes from `date -u`; PARTIAL.md has the stamps.
- The finding under test is lens report `checks/consistency/REVIEW.md` (`a586fb877a54a34c82ed5767877fa7ac94825741dce44ceb96c91facbbf9450e`), lines 74–101.

## Verdict

**REFUTED as stated. My severity is NOTE; the lens gave SHOULD_FIX. The proposed fix is not sufficient as written, and a smaller fix is given in §4.**

The finding says three things:
- C-8 item 5 asks for one status word;
- "several conditions hold at once and no precedence is given";
- "the reporter picks the word after targets are opened".

The bytes contradict the second and third claims. The r2 text already gives a precedence, in this order:
- OPEN wins, "whatever the score shows", for any reading whose deciding test has not run;
- several readings carry their own explicit "stays OPEN" clause;
- for R-DRIFT, the deciding test is the thing that decides.

The 110 AMBIGUITY events come from the lens's own classifier, which applies none of these clauses. I re-applied the text's own clauses to the same 110 events:
- 91 get a unique status from explicit text;
- 3 get one from the R-DRIFT deciding-test clause;
- the other 16 are a lens input error (2), conflicts filed elsewhere (2 under L-C01, 3 under L-C08 (d)), or a DT-T1a timing question the finding does not raise (9).

What survives is a drafting point, NOTE level:
- the precedence is stated in C-3 and per reading, but not at C-8 item 5;
- the R-DRIFT AGAINST mapping is implicit;
- the two registered caveats (A41 item 3; A66.2) need not be printed in the report.

## Object and sources (sha256 from bytes)

| file | sha256 | check |
|---|---|---|
| round1/PREREG_MISS_READING_R2.md | `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` | = HASHES_R2.txt |
| round1/CLAUSE_SOURCE_MAP_R2.md | `b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b` | = HASHES_R2.txt |
| round1/ROOT_ITEMS_R2.md | `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f` | = HASHES_R2.txt |
| round1/NUMBER_PROVENANCE_R2.json | `c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832` | = HASHES_R2.txt |
| round1/TARGET_FREE_CHECK_R2.json | `aab683236116bc3562df86f3b9542a54eec3446c44a8f0e5569ff2b305d2180b` | = HASHES_R2.txt |
| round1/TARGET_FREE_MUTATION_TEST_R2.json | `2a8202b823beb5cd0bc03c9e1e2b0377d9de59410a698c8d185f39739d66bc41` | = HASHES_R2.txt |
| round1/tools/check_target_free_c4v001.py | `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7` | = HASHES_R2.txt |
| V001 PREREG_MISS_READING_V001.md | `6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345` | as cited |
| V004 addendum (frozen) | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` | as cited |
| V003 addendum (frozen) | `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` | as cited |
| V005 addendum (open; root keeps appending) | `50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477` at 19:29:49Z (last entry A92); `6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c` at 19:36:12Z (adds A93); `352e9f7acf10ea76d2253cfdf8805edce3e827a5f5da38ea73062d933ab53ef5` at 19:39:13Z (adds A94) | the r2 section pins for A48, A63, A64, A65 and A66 still match the 352e9f7a bytes; A90–A94 contain no reading-status terms |
| lens C REVIEW.md | `a586fb877a54a34c82ed5767877fa7ac94825741dce44ceb96c91facbbf9450e` | = lens HASHES.txt |
| lens C CASES_RESULTS_V2.json (synthetic) | `73adc286a5edb8e6e81a53da3304e1a57d18064e1281b4149b327caffb090576` | = lens HASHES.txt |
| lens C tools/lensc_classifier.py | `a890c8fd468bc5efe544e895ab66ede7c2c58e6a6065a52cbdec3f1ffadf7533` | = lens HASHES.txt |

## 1. Is the quoted r2 text there, and is it defective?

**Present: yes.** All five quotes appear at the stated lines. `tools/reapply_precedence_lc02.py` checks them against the sha-verified bytes; see `quotes` in `PRECEDENCE_REAPPLY_LC02.json`.

**The C-8 quote is cut short.** PREREG [C-8] L340 reads in full:

> "5. **For each pattern,** its registered readings, each with the status consistent, inconsistent or OPEN, plus each deciding test's status."

The finding stops before "plus each deciding test's status". That omitted half already prints the deciding-test status beside every reading, which is the second element of the finding's own tuple.

**Claim (i), consistent + OPEN for every untested reading. Refuted.** The precedence is in the text, and the finding itself quotes one of the clauses that give it:
- PREREG [C-3] L169: "A reading whose deciding test has not run stays OPEN, **whatever the score shows**."
- ROOT_ITEMS M-4, L89, which the finding cites in its own file_and_tag: "Their readings (R-UT1, R-HIST, R-REACH and R-TSR) then stay OPEN after the score, whatever it shows."
- PREREG [C-9] L363: "They are NOT SCHEDULED, and their readings stay OPEN (§3)."
- Per reading:
  - [C-3.2] L201 (R-GEO): "DT-GEO is not evaluated, so this reading stays OPEN by construction.";
  - L207 (R-TSR): "DT-TSR (NOT SCHEDULED): R-TSR stays OPEN";
  - [C-6.3] L284 (R-DRIFT, STAGE0 not evaluated): "and R-DRIFT stays OPEN.";
  - [C-9] L366: "R-TSR may cite only flagged rows, and it stays OPEN."
- The precedence has been explicit since V001: V001 L106 has the same sentence, and V001 L207 reads "The readings R-UT1, R-HIST and R-REACH therefore stay OPEN after the score, whatever it shows."

**A structural argument says the same.** The "consistent with the reading if" column holds in 132 of 132 reported reading instances across the 38 cases (`consistent_column_true_in_reported_instances`), because each reading is registered only under the patterns that trigger it. If that column set the status, no reported reading could ever be OPEN or inconsistent. L169, L201, L207, L284 and every against-cell would then be void. The only reading that gives every clause effect is: OPEN, or the test outcome, takes precedence over the score relation.

**Claim (ii), R-UT1 and R-TSR also "inconsistent" through A41 item 3 and A66.2. Refuted.**
- [C-3] L168 limits the two words to what "the 43-row score can make": "The 43-row score can make a reading **consistent** or **inconsistent**." A41 item 3 (V004 L729–730) and A66.2 (V005 L634) are facts registered before the score. They are not the score, so under the text they do not produce "inconsistent".
- The r2 frames A66.2 as a caveat, not as an inconsistency trigger. L207 says "R-TSR is therefore registered as an open possibility, not an expected cause." The same row's deciding-test cell says "R-TSR stays OPEN".
- M-4 (L89) names both R-UT1 and R-TSR as OPEN.
- The "inconsistent" candidate exists only because the lens classifier passes these facts in as `against`:
  - `FACT_A41_ITEM3 = True` and `FACT_A66_2_AZIMUTHAL = True` at L224–225;
  - used at L266 and L307.

**Claim (iii), R-DRIFT both consistent and inconsistent under P1 with DT-S0G AGAINST. Refuted as a free choice; a wording point remains.** PREREG [C-3.2] L199 has three cells:
- consistent: "OUTER miss-dominated (P1, P1g or P2)";
- against: "the DT-S0G comparison reads AGAINST (§6.3)";
- deciding test: "DT-S0G; it can make R-DRIFT consistent or inconsistent, never supported (§6.3)".

R-DRIFT is registered only under P1/P1g, P2 and P5 (L199, L200, L202), and each of these requires OUTER miss-dominated. So the consistent cell holds every time R-DRIFT is reported. If that cell decided the status, DT-S0G could never "make R-DRIFT … inconsistent", which contradicts the deciding-test cell in the same row. The deciding-test cell therefore decides: AGAINST gives inconsistent.

Even a reporter who writes "consistent" must also print "DT-S0G: AGAINST", because L340 says "plus each deciding test's status". The word choice cannot hide the outcome.

What remains is that the text never states the mapping in one sentence. The C-P L21 gap-filler cannot supply it: the lens's own L-C24 shows that no reading is an adopted hypothesis, so the gap-filler has nothing to act on here.

**"The reporter picks the word after targets are opened." Refuted** for (i) and (ii). For (iii) the residual is wording only, and the outcome is printed either way.

## 2. Does the cited evidence say what the finding claims?

**The numbers reproduce.** I recounted from the lens's synthetic `CASES_RESULTS_V2.json`:
- C01: R-UT1 has candidates ['consistent', 'inconsistent', 'OPEN'] and R-HIST has ['consistent', 'OPEN'];
- C16: R-TSR has ['consistent', 'inconsistent', 'OPEN'];
- C21: R-DRIFT has ['consistent', 'inconsistent'];
- there are 110 'C-3/C-8' AMBIGUITY events.

**They do not show that the text is ambiguous.** They are the output of the lens's `reading_status()` (lensc_classifier.py L230–245), which adds one candidate word for each condition that holds:
- L237–238 (`if not test_run: cands.append('OPEN')`) adds OPEN next to 'consistent' for every untested reading. It never applies L169's "whatever the score shows", M-4, or the per-reading "stays OPEN" clauses. The lens report never discusses L169 as a precedence; grepping REVIEW.md and PARTIAL.md for "whatever", "precedence", "L169" and "M-4" finds only the L-C02 text itself.
- Pre-score facts are passed in as against-conditions (L224–225, L266, L307).
- L282 hard-codes R-GRID's `test_run` to False. But R-GRID's decider, DT-ALT on ORIGINAL_K, is evaluated:
  - PREREG L44: "| ORIGINAL_K | state | EVALUATED_BEFORE_FREEZE |";
  - L185: "ORIGINAL_K is evaluated.";
  - L200: "ORIGINAL_K shows the same excess (against R-GRID)".

  So the finding is wrong to list R-GRID among the "untested readings" in (i).

**The same 110 events under the text's own clauses** (`tools/reapply_precedence_lc02.py`, output `PRECEDENCE_REAPPLY_LC02.json`):

| class | events | readings | status under the text |
|---|---|---|---|
| EXPLICIT_OPEN | 78 | R-UT1 20, R-HIST 20, R-REACH 20 (L169 + M-4 L89 + L363); R-TSR 1 (L207, L366); R-GEO 3 (L201); R-DRIFT with STAGE0 NOT_EVALUATED 14 (L284) | OPEN, unique |
| GENERAL_L169_OPEN | 13 | R-NAX 9 (DT-NAX "not run"); R-S1 2 (DT-S1 "UNTESTED"); P5 onset 2 | OPEN, unique |
| DT_CLAUSE_STRUCTURAL | 3 | R-DRIFT with DT-S0G AGAINST (C21, C23, C38) | inconsistent (L199) |
| L169_OPEN_TIMING_DEPENDENT | 9 | R-ML 3, R-SPEC 3, R-GEFF 3 | OPEN while DT-T1a ("registered"; "runs only after a verified freeze", L183) has not run; not raised by the finding |
| LENS_INPUT_ERROR | 2 | R-GRID (C12, C32) | decided by ORIGINAL_K; the residual is the undefined "same excess", which is L-C09 |
| OTHER_FINDING_L-C01 | 2 | R-MF under P2 (C12, C32) | the cross-row P1/P2 conflict, which is L-C01 |
| RESIDUAL_UNRULED_ALREADY_L-C08d | 3 | R-DRIFT with DT-S0G NOT_DECIDED (C22, C24, C25) | unruled; L-C08 (d) already proposes "R-DRIFT stays OPEN" |

## 3. Severity

**NOTE.** It does not meet SHOULD_FIX:
- No choice of status word can change a tier, a pattern, the headline, the score, or R-MF's TESTED-NEGATIVE.
- "Supported" is barred in every case (L168; the word rules at L347–349).
- The precedence exists (§1). The DT-S0G outcome is printed either way (L340).
- The one unruled outcome, NOT_DECIDED, is a real gap, but it belongs to L-C08 (d), which is SHOULD_FIX.
- The inoperative L21 gap-filler is L-C24 (NOTE).

What L-C02 adds beyond those findings is the drafting point in the Verdict.

## 4. Would the proposed fix work without creating a new problem?

The finding's fix is a fixed tuple: score relation (consistent | inconsistent | not addressed), deciding-test status (OPEN | the test's registered outcome), and the against-evidence registered before the score. Separating the axes would work, but as written it has these problems:
1. **It moves OPEN into the test-status slot.** The text uses OPEN as a reading status at L169, L201, L206, L207, L284, L363 and L366, and in ROOT_ITEMS L89 (M-4) and L172 (M-9). A partial migration would itself create the kind of inconsistency this lens hunts for.
2. **Slot 1 carries almost no information.** It reads "consistent" in 132 of 132 reported instances. "Inconsistent" is reachable only through R-MF (L-C01), and "not addressed" has no defined trigger. Printing "consistent" on every reading, including R-UT1, also invites the over-reading that §9 guards against.
3. **Slot 2 needs a map from each reading to its deciding test, and the text lacks one.** Three rows list their tests jointly:
   - P2, L200: "DT-S1, DT-ALT, the A17 C3 record, DT-S0G";
   - P3/P4, L201: "DT-T1a, DT-ALT (M/L), DT-GEO, DT-NAX";
   - P6, L203.

   R-GEFF has no named test, and R-SPEC shares DT-T1a with R-ML ([C-3.3] L212). Without a map, the reporter fills slot 2, which is new discretion.
4. **Slot 3 is an open list.** "Registered before the score" admits entries added after the seal. It must be a closed list fixed at the seal. Also, the R-GEO and P5 against-cells are status or comparison notes, not evidence.
5. **"'Consistent' never appears without its test status" is already the text.** L340 says "plus each deciding test's status".
6. **It does not settle DT-T1a timing**, which governs R-ML and R-SPEC.

**Better fix.** Keep the existing vocabulary and make the existing precedence operational in [C-8] item 5:
- **Format.** Each reading on one line: `<reading>: <status> (score: consistent via <pattern>; <deciding test>: <its C-3.1 status word, or its registered outcome>; registered caveat: <entry, or none>)`.
- **Status, assigned in this order and only so:**
  1. R-MF: by the C-3.2 R-MF rule, as fixed under L-C01.
  2. If the reading's own deciding test has a registered outcome at the score step, that outcome decides:
     - DT-S0G: CONSISTENT gives consistent, AGAINST gives inconsistent, NOT_DECIDED gives OPEN (with L-C08 (d));
     - ORIGINAL_K, for R-GRID: by its defined condition (L-C09).
  3. Otherwise OPEN, whatever the score shows (§3).
- **Caveats, exactly these:**
  - R-UT1: V004 A41 item 3 (FORMAL + TESTED);
  - R-TSR: A66.2 (A42 TESTED), "an open possibility, not an expected cause".

  No caveat is added after the seal.
- **Deciding-test map** (add to [C-3.1]):

  | reading | deciding test |
  |---|---|
  | R-MF | the score itself |
  | R-UT1 | DT-UT1 |
  | R-HIST | DT-BHD |
  | R-REACH | DT-U12 |
  | R-DRIFT | DT-S0G |
  | R-S1 | DT-S1 |
  | R-GRID | DT-ALT (ORIGINAL_K) |
  | R-ML | DT-T1a and the ML_3p6 alternatives |
  | R-SPEC | DT-T1a, jointly with R-ML |
  | R-GEO | DT-GEO |
  | R-NAX | DT-NAX |
  | R-TSR | DT-TSR |
  | P5 onset | as P1, plus DT-NAX |
  | R-GEFF | none named; root names one (DT-S1 is the natural choice), or it reads OPEN |

- **Timing.** Test statuses are those at the score step. An outcome that arrives later goes in a labelled later addendum and never changes this report.
- **§9.** Point the "Upgrading 'consistent' to 'supported'" row to this order.

## 5. Observations beyond the finding (offered for the fix round; not new findings)

- **DT-T1a timing.** Whether R-ML and R-SPEC read OPEN depends on whether DT-T1a has run by the time of the report. The text does not fix that order (L183).
- **R-GEFF has no individually named deciding test.** L201 lists the P3/P4 tests jointly.
- **The R-GRID input error** affects only L-C02's list of readings and the event count. L-C09 and L-C10 handle R-GRID on their own terms.

## Rules kept

- No NGC3198 target, observed velocity, rotmod/Vobs/MassModels/SPARC path or NGC3198 data table was opened.
- Nothing under runs_ext was read, listed or stat'ed, and no UVT_* item was read.
- Nothing was launched, and no project calculation was run.
- The only data used are lens C's synthetic case results.
- Writes went only to this folder, with no edits, deletes, moves or network use.
- Python ran as `python3 -I -B` from the codex runtime, with the four thread variables set to 1, and used the standard library only.

## Files in this folder

- PARTIAL.md
- VERIFY.md (this file)
- REVIEW.md (pointer to this file)
- PRECEDENCE_REAPPLY_LC02.json
- tools/reapply_precedence_lc02.py
- HASHES.txt
