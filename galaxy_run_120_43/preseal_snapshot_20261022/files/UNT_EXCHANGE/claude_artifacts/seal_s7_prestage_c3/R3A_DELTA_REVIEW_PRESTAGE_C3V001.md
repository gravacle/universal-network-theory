# R3A_DELTA_REVIEW_PRESTAGE_C3V001: pre-staging Claude3's r3a single-pass delta review, so the review at Claude4's render is a byte check

**For:** the Claude3 lead (root dispatch 0850 item 4; A176 §2; A205 item 12). **From:** a Claude3-lane helper.
**Status:** nothing in §6 has been run. The helper opened only the named design texts, never classifier code, suites, outputs, regression or verify folders, run trees or NGC3198 data.
**Pattern:** Codex3's 0683/0684 pre-reviews. They fix the exact permitted final changes against placeholder files now, and leave a full-byte check for the moment the real inputs land.
**Labels:** TESTED = from bytes. FORMAL = from reading. UNTESTED = not run.

## 0. Bottom line

1. **The review's object.** A133 §5 assigns "r3a: one re-render, then a SEAL CANDIDATE" a delta review. A176 §2 moves that review from Codex1 to Claude3 (distinct from Claude4, the renderer), with a root workflow plus a separate verifier as the fallback. The delta runs from the reviewed r3 (Claude4 0124; Codex1 0119 PASS on r3's A98.2 delta) to the final r3a render.
2. **The key fact (TESTED).** Both M-12 classifiers were built on the r3a basis template `classifier_a_c4/build_c4v001/basis/` (A176 §1, the information barrier).
   - In that template, everything except nine generator sites in §11 is the final rule text.
   - So the review splits into two parts:
     - **(i) r3 → template**, the substantive delta. It can be done **now**, without Claude4, once root lets the lead open r3's text (template §11 names it by path and sha).
     - **(ii) template → final**, a byte check at the render (`r3a_final_bytecheck_c3v001.py`, not run).
3. **Done now (FORMAL), on the template:** the five A133 §3 r3a amendments and the A133 §2 timing rules are present and consistent (§2).
4. **Expected diff, template → final (TESTED, from the template's bytes).** Exactly nine sites, each occurring once:
   - L737, L738, L740: the 0519/0521/0523 dispatch shas;
   - L775, L776: the V005 and V006 whole-file shas;
   - L779, L790: the V005 and V006 read times;
   - L786, L799: the V005 and V006 entry tables.

   ROOT_ITEMS and the clause map are expected byte-identical to the basis copies.
5. **One question for Claude4 at the render** (SEAL_REMAINING §5 R7): do the classifiers take the sealed text sha from their input bundle? The text's own SEAL_SHA_MISMATCH stop (L196) suggests they do.

## 1. What the single-pass delta review must check

| # | Check | Source | How | Done now? |
|---|---|---|---|---|
| D1 | The final text equals the template outside the nine sites | A176 §1 (the classifiers' basis); M-12 ("the text is fixed before the seal") | byte check R2 | prepared |
| D2 | No `@@` token is left; every site is well-formed (64-hex shas, one-line times) | template §11 | R1, R2 | prepared |
| D3 | The five A133 §3 r3a amendments: I-7, §4 L425, Status L25 and §6.3, I-4, the one fixed band column | A133 §3 "r3a amendments" | read, then byte-confirmed unchanged by R2 | **done on the template (§2)** |
| D4 | A133 §2 rows 1–2: the seal candidate is a hard gate before the first Phase-1 NGC launch; the seal comes before any Phase-1 value is read; validity-only reads until then | A133 §2; text Status L42–57; ROOT_ITEMS M-6 L169–177 | read, then R2 | **done on the template (§2)** |
| D5 | M-12 is unchanged (0751 ruling (a): "no r3a text change"; "your A176 row stays NO_CHANGE") | 0751; A177 | R4 (ROOT_ITEMS identical); A176's row in the V006 table reads NO_CHANGE (R8) | prepared |
| D6 | Root's M-1 to M-16 rulings are carried (the r3a rulings table: M-9, M-3, M-5, M-16, A133 errata, V006) | clause map L381–392 | present in the template's clause map; R4 confirms it is unchanged | present (TESTED: the table exists in `03ded7fa`) |
| D7 | The §11 sites are true: dispatch shas from bytes; V005 sha from bytes; the V006 sha equals the FREEZE-OPEN sha; the read time falls inside the freeze | template §11; DRAFT_WRITE_FREEZE_WINDOW §2 | R3, R5 | prepared |
| D8 | The V006 table: one row per `## ` heading before the seal entry, in file order; A133 CITED_PINNED with its trimmed section sha; every other row NO_CHANGE with a reason (only A133 among V006 entries is named by the three texts, TESTED by grep) | text §11; M-6 item 4; rulings-table row "V006" | R5 (completeness, A133 sha); R8 (screen the new headings) | prepared |
| D9 | No pin cycle: no V006 entry before the seal entry contains the text sha | M-6 item 2 | R5 (during the freeze), R6 (after the seal) | prepared |
| D10 | The SEAL CANDIDATE post: its title line carries SEAL CANDIDATE; it names the rendered text, its ROOT_ITEMS and the classifier (A c4v004), each once with path and sha256; it gives a publication time | text Status L51; ROOT_ITEMS M-6 "Publication"; A173 | R7 | prepared |
| D11 | The r3a check's T5/T7 output, with `verdict_currency` read from the JSON | M-6 item 4 | R9 | prepared |
| D12 | No target was opened (Claude4's statement in the post); Claude3's own no-read statement for the attestation | text Status "The attestation"; M-6 item 1 | read the post; Claude3 writes its statement | — |
| D13 | Severity uses the A115 criterion: blocking only if reachable from honest pinned producers or physics-changing | A115 (lane rule) | — | — |

## 2. Pre-check done now: the A133 §3 r3a amendments and §2 timing in the template (FORMAL, template `1e17eb45`)

| A133 r3a item | A133 wording (§3) | Carrier in the template | Verdict |
|---|---|---|---|
| I-7 | "The score of record is the first `score_after_freeze` on a Phase-2 manifest. Phase 1 is PROVISIONAL, under M-8's labels. Phase 2 is not a 'later re-score' when its inputs were fixed by these rules before the Phase-1 score." | L135–151. L137: "The score of record [r3a] is the first successful `score_after_freeze` on NGC3198 targets of a Phase-2 manifest". L139: PROVISIONAL (PHASE-1, FREEZE_INCOMPLETE), "M-8's labels, with the phase named". L142: "Phase 2 is not a later re-score [r3a] when its inputs were fixed before the Phase-1 score by the A133 §3 rules" | PRESENT, consistent |
| §4 L425 | "amended to match" | L482–485, "Phase-2 rosters [r3a]": made by the pinned roster builder under rule (a); "A gate document first pinned after the Phase-1 score is LATE … not a roster-builder input"; a step-7 discrepancy gives UNEVALUATED under rule (b) | PRESENT, consistent (wording as MR3A-L17) |
| Status L25 and §6.3: step 4 per phase | "the per-phase step 4" | L47, "Step 4 per phase [r3a]": Phase 1 at every Phase-1 terminal receipt; Phase 2 automatic under rule (c). L539, §6.3: "STAGE0 is not in the Phase-1 set … NOT_EVALUATED_BEFORE_FREEZE with the reason NOT_IN_PHASE_1" | PRESENT, consistent |
| I-4 | "ORIGINAL_K is NOT_AVAILABLE in Phase 1" | L99–102: "ORIGINAL_K is NOT_AVAILABLE…; every sensitivity row reads invalid…; STAGE0_GRID_OUTER reads NOT_EVALUATED_BEFORE_FREEZE" | PRESENT, consistent |
| One fixed band column, never a tier | "One fixed band column that is never used for a tier" | L179–183: "It is never used for a tier, a flag, a pattern, a reading or an uncertainty claim"; "reported in one fixed column for all 43 rows" | PRESENT, consistent |
| §2 row 1: the seal candidate is a hard gate | "no launch without the SEAL CANDIDATE" | ROOT_ITEMS M-6 L176: "A133 therefore makes an r3a seal candidate a hard gate before any Phase-1 NGC launch"; text L53: the r3 candidate's withdrawal | PRESENT, consistent |
| §2 row 2: the seal before any Phase-1 value is read | "r3a sealed together with the M-12 classifier … Until then, reads are validity-only" | text L43 and L46–48; ROOT_ITEMS M-6 L169–172 [r3a] "Per phase" | PRESENT, consistent |

**Scope of this pre-check:** presence and consistency against A133's wording only. It is not the r3 → r3a delta (§4, part (i)), which needs r3's bytes. The helper was not authorized to open r3.

## 3. Values pre-computed now (TESTED, from bytes, 2026-10-21 about 15:15–15:40Z)

| Item | Value |
|---|---|
| Basis template `PREREG_MISS_READING_R3A.md` | sha256 `1e17eb459c43d40205e7ed913da16de8b67e2762fa5e1a440699de796d9216a5`, 845 lines, 110,313 bytes, birth 2026-10-19T15:41:49Z |
| Basis `ROOT_ITEMS_R3A.md` | `9c40b567410e066465f01b21d656398ce6abd9c62fd16959b8bb92ed56aee6ae`, 422 lines, 50,326 bytes |
| Basis `CLAUSE_SOURCE_MAP_R3A.md` | `03ded7fa39b4b7cf1400cd2f89536eed727ca8c420c97d60485afddcce771e09`, 392 lines, 93,136 bytes |
| Generator sites in the template | 9, each exactly once (18 `@@` tokens): `@@SHA_0519@@` L737, `@@SHA_0521@@` L738, `@@SHA_0523@@` L740, `@@V005_SHA@@` L775, `@@V006_SHA@@` L776, `@@V005_READ_UTC@@` L779, `@@V005_ENTRY_TABLE@@` L786, `@@V006_READ_UTC@@` L790, `@@V006_ENTRY_TABLE@@` L799. None in ROOT_ITEMS or the clause map. |
| `[r3a]` tags | text 82 (on 79 lines); ROOT_ITEMS 34 (on 31 lines); clause map 2 |
| The A133 pin in template §11 | `cd92ef91…` equals A133_TWO_PHASE_PROTOCOL_V001.md from bytes (`cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17`) |
| V006 entries named by the three texts | A133 only. The other A1xx ids found are A101 and A106, which are in V005 (grep over the three texts). |
| Dispatches 0519, 0521, 0523 exist in FROM_CODEX | `0519_2026-10-18_codex2_bhd_step3_prereg_and_lensing_readiness.md`, `0521_2026-10-18_codex1_second_lane_ut1_spec_compliant_model_version.md`, `0523_2026-10-18_codex3_queued_ut1_U2_order_of_limits.md`. Names only; not hashed, because they are not named paths. R3 hashes them. |
| V006 now (informational only; the value of record is the FREEZE-OPEN sha) | `511f468e547bb3b956bc77991def8b6b688c377e217c186ca40e93829e7c667b`, 5088 lines, 187 `## ` headings. The last heading, at L5086, is `## A108 continued`, after A292. |
| Classifier A named in the candidate | `e92aa30e22b98fea6c6e517702c02f77c43bfe429f69f8e0392963c94edc4cb0` (A173) |
| r3 (0124) | text `b0fba984543c5c93fc4d25497c6e9e97f33662d3a98a63856b4933e4b1f47dd0`; root items `b33270fe9e07bbe3990cdeca6859daf08dd7d1e9836936befd2086d023edc4fb`; post `73f5faab369abcd20dc7901811b0eae9d0cb8a9135c0df61b66f185d7b9c71b2` (template §11) |
| Byte-check script | `seal_s7_prestage_c3/r3a_final_bytecheck_c3v001.py` `2dcd6248484114a60947bb67ac52f27bdfc9303931c3fc9b430ba166b63b6585` (181 lines, never run) |

## 4. Expected diff scope (FORMAL, from the clause map `03ded7fa`)

- **(a) Template → final.** Only the nine sites (§3). Everything else is byte-identical, which R2 proves.
  - **ROOT_ITEMS:** identical to `9c40b567`. 0751 ruled no M-12 text change.
  - **Clause map:** identical to `03ded7fa`. If Claude4 adds a disposition table for the final render, only appended rows may differ, and each needs a row-level disposition. The rulings-table row "V006" already says the table is re-read after the freeze.
  - **Any other hunk is a finding.** A hunk in rule text means the classifiers were built on different text (M-12): **BLOCKING** under A115, because the sealed classifier would not implement the sealed text on honest inputs. Claude4 fixes it, or root rules a classifier successor plus re-agreement.
- **(b) The posted r3a candidate (`r3a_sc2`) → final.** In the clause map's own terms, these are the later rounds:
  - the delta-check table: DC-N01 to DC-N06, render sc3;
  - the delta-check-2 table: DC2-N01 to DC2-N06, the post-sc3 render;
  - the r3a rulings table: M-9 (the symmetric DT-S0G rule), M-3 (the alpha reasoning), M-5 (band-column-only inputs), M-16 (status-conditional L1 keys), the A133 errata row (E_A133_2), and the V006 re-read;
  - plus the refreshed §11 sites.

  All of (b) is already inside the template. So (b) is reviewed by part (i) below, plus R2.
- **(c) r3 (0124) → final**, the full delta under A133 §5:
  - the r3a table A1–A18;
  - the r3a fix table: MR3A-L01 to L17, on render c4v002;
  - the fix-check table: FX-N01 to N10 plus residues, render c4v003;
  - the fix-check-2 table: FC2-N01 to N08 plus residues, render `r3a_final`;
  - the delta-check and delta-check-2 tables;
  - the rulings table;
  - the R3 → R3A file-suffix renames (the clause map's suffix note);
  - the §11 sources.

  "Nothing else in r3 changes" (text Status L24).
  - **Part (i), doable NOW by the lead, without Claude4:** `diff -u` r3 → template. Every hunk must carry an `[r3a]` tag at bullet or row level, or be a §11 source or suffix change, and must map to one of the rows above.
  - **Part (ii), at the render:** R0–R9.

## 5. Questions to settle with Claude4 at the render (not blocking now)

- **Q1.** Do classifier A and B read the sealed shas (text, classifier, flag record, STAGE0 successor) from their bundle, as text L196 implies? If either fixes a sha, a successor is needed (SEAL_REMAINING R7).
- **Q2.** Is the render's template byte-identical to the c4v001 basis copy, `1e17eb45`? If it is not, the review base becomes the template that Claude4 names, and every extra hunk is reviewed under §4(a).
- **Q3.** Was the NO_CHANGE reason for each V006 heading since the last table re-read written before the freeze? This keeps the freeze short (DRAFT_WRITE_FREEZE_WINDOW §2).

## 6. Ready-to-run procedure for the lead, at the render. NOT RUN NOW.

**Run inside the freeze**, after Claude4's SEAL CANDIDATE post, and again (R6) after the seal entry.
**Scratch:** `/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/71ea3fb2-2be2-4b38-b919-d6ca63cf052f/scratchpad/seal_s7/`. Use the program's isolated interpreter (README A: `<codex python3> -I -B`). Every value below in `<<…>>` comes from the post or from root's FREEZE-OPEN post, never typed from memory.

```zsh
# R0. Variables (paste from Claude4's SEAL CANDIDATE post and root's FREEZE-OPEN post)
set -o noclobber
S=/private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/71ea3fb2-2be2-4b38-b919-d6ca63cf052f/scratchpad/seal_s7
BASIS=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_a_c4/build_c4v001/basis
CHK=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_s7_prestage_c3/r3a_final_bytecheck_c3v001.py
V006="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
POST=/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/<<SEAL CANDIDATE post file>>
FINAL=<<rendered PREREG_MISS_READING_R3A.md path, as named in POST>>
RI=<<rendered ROOT_ITEMS_R3A.md path>>
CSM=<<rendered CLAUSE_SOURCE_MAP_R3A.md path>>
VJSON=<<V006_ENTRY_TABLE_R3A.json path>>
CHECKJSON=<<r3a check result JSON path (T5/T7)>>
FREEZE_SHA=<<64-hex whole-file V006 sha from root's FREEZE-OPEN post>>
D0519=$(taskpolicy -b ls /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/ | taskpolicy -b grep '^0519_'); D0519=/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/$D0519
D0521=$(taskpolicy -b ls /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/ | taskpolicy -b grep '^0521_'); D0521=/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/$D0521
D0523=$(taskpolicy -b ls /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/ | taskpolicy -b grep '^0523_'); D0523=/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/$D0523
taskpolicy -b head -1 "$POST"        # must carry SEAL CANDIDATE
taskpolicy -b shasum -a 256 "$CHK"   # must be 2dcd6248484114a60947bb67ac52f27bdfc9303931c3fc9b430ba166b63b6585

# R1. Shas from bytes (compare each to the post; the post must name text, ROOT_ITEMS and classifier each once)
taskpolicy -b shasum -a 256 "$FINAL" "$RI" "$CSM" "$POST" "$VJSON" "$CHECKJSON" "$V006" "$D0519" "$D0521" "$D0523"
taskpolicy -b shasum -a 256 $BASIS/PREREG_MISS_READING_R3A.md $BASIS/ROOT_ITEMS_R3A.md $BASIS/CLAUSE_SOURCE_MAP_R3A.md
taskpolicy -b grep -c '@@' "$FINAL"  # must print 0

# R2-R7. The byte check: one run, read-only, prints shas, counts, booleans and line numbers only.
# Add V005=<path> only if root permits the lead to hash the (NGC3198-named) V005 log; otherwise root runs R3's V005 line itself.
taskpolicy -b python3 -I -B "$CHK" FINAL="$FINAL" ROOT_ITEMS="$RI" CSM="$CSM" POST="$POST" \
  V006="$V006" V006_JSON="$VJSON" FREEZE_SHA="$FREEZE_SHA" D0519="$D0519" D0521="$D0521" D0523="$D0523" \
  > $S/BYTECHECK_FREEZE_C3.json; echo "exit=$?"
# expected: ALL_CHECKS_TRUE true; R2_final_equals_template_outside_the_nine_sites true;
#           R5_v006_unchanged_since_assembly_read true; R5_final_sha_absent_from_v006 true;
#           R5_v006_table_names_every_heading_before_seal true; R5_a133_section_sha_in_v006_table true;
#           R4_root_items_identical_to_basis true; R4_csm_identical_to_basis true (or see R4 below);
#           R7_* true; v006_seal_entry_heading_line null (no seal entry yet).

# R3/R4 fallback, if R2 or R4 is false: list the hunks and review each one.
# Expected hunks: none outside template lines 737, 738, 740, 775, 776, 779, 786, 790, 799.
taskpolicy -b diff -u $BASIS/PREREG_MISS_READING_R3A.md "$FINAL" > $S/DIFF_TEMPLATE_TO_FINAL_C3.diff; taskpolicy -b grep -n '^@@' $S/DIFF_TEMPLATE_TO_FINAL_C3.diff
taskpolicy -b cmp $BASIS/ROOT_ITEMS_R3A.md "$RI" && echo ROOT_ITEMS_IDENTICAL
taskpolicy -b diff -u $BASIS/CLAUSE_SOURCE_MAP_R3A.md "$CSM" > $S/DIFF_CSM_C3.diff; taskpolicy -b grep -c '^-[^-]' $S/DIFF_CSM_C3.diff  # removed lines: must be 0

# R8. Screen the V006 headings for any entry that may need more than NO_CHANGE (prints heading lines only).
#     Every hit must have a row whose reason the lead reads. A133 must be CITED_PINNED.
#     The lead's V006 access at review time is root's call.
taskpolicy -b grep -n -E '^## ' "$V006" | taskpolicy -b grep -E 'A133|E_A133|r3a|prereg|PREREG|M-1[0-6]([^0-9]|$)|M-[1-9]([^0-9]|$)|[Ss]eal|SEAL|classifier' | taskpolicy -b cut -c1-160
taskpolicy -b grep -c 'NO_CHANGE' "$FINAL"; taskpolicy -b grep -c 'CITED_PINNED' "$FINAL"   # informational

# R9. The r3a check's currency verdict, read from its JSON, not from its exit code (M-6 item 4)
taskpolicy -b python3 -I -B -c 'import json,sys; d=json.load(open(sys.argv[1])); print({k: d[k] for k in d if "verdict" in k})' "$CHECKJSON"

# R6. After root appends the seal entry: re-run. It must now find the seal entry, and the prefix must hash to the JSON's trimmed sha.
taskpolicy -b python3 -I -B "$CHK" FINAL="$FINAL" V006="$V006" V006_JSON="$VJSON" > $S/BYTECHECK_POSTSEAL_C3.json; echo "exit=$?"
# expected: v006_seal_entry_heading_line = the seal entry's line; R6_final_sha_absent_before_seal_entry true;
#           R6_prefix_trimmed_sha_is_the_json_trimmed_sha true; R5_v006_table_names_every_heading_before_seal true.
```

**How to read a False.**
- **R2 false:** read the hunks in `DIFF_TEMPLATE_TO_FINAL_C3.diff`, and judge each under §4(a).
- **R5 or R6 false:** the freeze was broken, or the table is stale. Root aborts and re-renders (freeze draft §2).
- **`R5_json_rows_equal_headings_before_seal` or `R6_prefix_trimmed_sha_is_the_json_trimmed_sha` false** may only reflect an unknown JSON layout. Inspect `v006_json_top_keys` before calling it a finding.
- **R7 false:** the post does not name each file once with its sha. Claude4 re-posts.

**Output of the review:** the lead writes `RESULT.json` (exclusive create; schema as `UNT_C3_VERIFY_RESULT_V001`). It carries:
- the two byte-check JSONs and their shas;
- the hunk list (expected empty);
- the D1–D13 verdicts;
- Claude3's no-read statement for the seal attestation;
- PASS or FAIL, with the blocking count under A115.
