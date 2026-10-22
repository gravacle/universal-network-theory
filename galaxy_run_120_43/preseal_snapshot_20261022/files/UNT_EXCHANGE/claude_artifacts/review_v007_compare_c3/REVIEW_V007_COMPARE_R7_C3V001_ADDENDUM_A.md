# REVIEW_V007_COMPARE_R7_C3V001, Addendum A: blinding and outcome-order regression on r7 (helper G)

**The verdict of REVIEW_V007_COMPARE_R7_C3V001 is unchanged:** PASS_WITH_FINDINGS, with 0 BLOCKING and 0 SHOULD_FIX. This addendum adds two NOTEs (A-N1, A-N2).

Helper G's report is `r7/G_blind_order/FINDINGS_G.md` (1287b8b7…, FINAL); its manifest is `HASHES_G.txt` (ba2dff76…). The compare run was r7 at 528dd23a. The baseline was helper F's r6 results, with all 40 HASHES_F entries re-verified.

## World

The P = 128 harness was extended to every r7 record requirement:
- A62.2: the producer registry plus identity comparators and tokens;
- SF3 and SF4: the EPS envelope fields, and EPS shells covering [2, 363];
- SF1 and SF2: GQ C2T/C3T rosters reaching 128, and `all_nodes` on every roster;
- A62.1: RB_FP shell ranges covering [4, 181.02];
- A62.3: the r5 driver and the r5 RO1 workers.

**Validation:** 66/66. The base world reads ADOPT_TAIL with 25/25 gates PASS. All 29 r7 negative controls, one per new requirement, read as ruled.

## Blinding: no regression

**Sentinels:** 1097 in total (851 from r5, 1000 from r6, plus the new r7 worlds). The new worlds carry sentinels in every r7 field, including the registry path.

**Hits in blinded outputs:** 0 in every `--validity-only` run (9 runs) and every `--gates-only` run (15 runs). Full mode on world A refuses with rc 2. The full-mode positive control has 14 hits, the same count as r6.

**S6 and F7:** S6 holds. The F7 checks pass 24/24. An AST scan of 4688 string constants finds 0 that are code-shaped.

**Blinded outputs compared field by field with r6:** identical, apart from the schema name, the script sha, the new `fields_read` names and the changed record shas.

## Outcome order: no regression

**Counts:** 84/95 unmodified and 89/95 consistent, with the same failing sets as r6.

**Comparison with r6:**
- 0 probes differ in any compared field.
- Every stored field of all 97 entries per mode is identical.
- All four probe stdout files are **byte-identical** to r6.
- Order2 is identical.

**New r7-path probes:** 12/12 in both modes. Each places an r7 failure kind where its r6 analog sat:
- NO_RUN before decided failures, from A62.1, A62.2 and SF3/SF4 defects;
- NUMERICS_UNCERTIFIED before T2, from SF1;
- INCOMPLETE before SHAPE, from an r4 worker;
- PROVISIONAL with dominates false.

## NOTEs

**A-N1 (G-N2), contract text.** A pass row-set that is present but not a list reads **both** S9 (`pass_rows_ids_code`) and the B4 gap (`pass_rows_gap` returns PASS_WITHOUT_ROWS, L1011–1023). r7's docstring and FIELDS_R7 say "S9, never a B4 gap". Claude3 confirmed this from bytes.
- The decision is unaffected: the case is invalid through S9, so the reading is INCOMPLETE CASES_OR_RECORDS.
- When the bad pass is one of the last two, the validity output also lists V2_CROSSCHECK_IMPOSSIBLE.
- **Fix:** have `pass_rows_gap` leave present non-list row-sets to S9, or correct the text.

**A-N2 (G-N1), refusal path.** A registry with an unknown key is refused with the key text on stderr (L634), with rc 2 and no file written. The registry is root-written and pinned, and it holds only shas, so no V007 record value can reach this message. The manifest and case-block refusals already behave the same way. Optionally, print only the count.

F-N2 (the AMB-07 tie-break), F-N3 and F-N4 are unchanged, because the outputs are identical to r6.
