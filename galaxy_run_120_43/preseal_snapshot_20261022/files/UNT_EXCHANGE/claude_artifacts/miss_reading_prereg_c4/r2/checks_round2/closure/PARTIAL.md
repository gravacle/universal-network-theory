# R2-A CLOSURE lens — PARTIAL (in progress)

Started: 2026-10-18T19:56:40Z
Lens: R2-A CLOSURE (helper of lane Claude4; refute-by-default; object read-only).

## Step 1 — object hashes from bytes: DONE
All 10 files listed in round2/HASHES_R2.txt match shasum -a 256 of the bytes
(PREREG 97d5ce33..., CLAUSE_SOURCE_MAP 38cd6852..., ROOT_ITEMS 4907cf01...,
NUMBER_PROVENANCE ff6ca9b8..., INDEX 0d24b8fe..., TARGET_FREE_CHECK 624f278e...,
MUTATION_TEST 4445a9bf..., check_target_free 4ae4f705..., test dc812342...,
make_miss_reading 2132078f...). HASHES_R2.txt itself: 2e3cf0c6...

## Next
- read closure table; read round-1 REVIEW/VERIFY; read round-2 text per row.

## Step 2 — read (2026-10-18T19:57:36Z)
- round-1 REVIEW.md x3 (fidelity A-01..A-18; targetfree B-1..B-12; consistency L-C01..L-C27) read in full.
- six VERIFY.md read in full (A-01, A-02, B-1, B-2, L-C01, L-C02).
- round-2 PREREG (621 lines), CLAUSE_SOURCE_MAP_R2, ROOT_ITEMS_R2 read in full.
Next: round-1 PREREG diff; INDEX/provenance/check JSON; sources (V005 etc).

## Step 3 — sources (2026-10-18T20:10:47Z)
- V005 read in full at 991cc242 (= assembly bytes; snapshot V005_SNAPSHOT_991cc242.md). Re-read 20:10:24Z: cf9bbf19 (adds A97, A98;
  snapshot V005_SNAPSHOT_cf9bbf19.md). A98 + dispatch 0619 (238858d1) already order an r3 for the undefined-sign/OUTER_FAILURE/LATE-gate defect (Codex2 0490).
- V004 (487d4449) A14-A17, A20, A21, A27 read; V003 (5bef6552) A10-A13 read.
- 0585, 0606, 0592, 0512, 0550 read. Codex1 0058 (fc5af831), REHEARSAL_COMPLETE (19807bb3), Codex2 checklist (020ef3f1), Codex3 0618 (8939c004) + carrier contract read.
- TSR facts verified from bytes (TSR_FACTS_CLOSURE.json): Q25 only flagged by (r14,r16); rings == GL4 nodes bitwise; zones 24/11/8.
- check rerun (runs/CHECK_RERUN_R2A.json): target-free PASS; currency now FAIL (A97, A98 after assembly).

## Provisional findings so far
1. BLOCKING (L-C01 refuter better-fix item 3 not adopted): P2/P11 OUTER_FAILURE rows lack R-REACH/R-HIST(/R-UT1) required by binding
   A12.3, A15 E3, A20 and slots SA-REACH-01; no reason stated.
2. SHOULD_FIX: OUTER_FAILURE "miss-dominated whatever sign" vs "exactly when P1/P2/P11" disagree when S(OUTER) UNDEFINED; coverage
   property false; "late gate can never remove a pattern" false (corroborated by A98/0619 from Codex2 0490).
3. SHOULD_FIX: A47, A71, A80 cited but not pinned; auto "read with no change" list (A-10/L-C12 class recurs).
4. SHOULD_FIX: no FLAG_TABLE_MISMATCH stop; I-3 (rule applied to records) vs 1.4 (ids fixed) two sources of truth (A-02/B-2 refuters).
5. SHOULD_FIX: B-6 T7 regex misses suffix headings (A81a:, 'A66 amendment' counted as cited); no-change entries unpinned.
6. SHOULD_FIX: B-8 many lens-B cases still pass (C01-C04, C06, C09-C12, A07, B11...). To reproduce.
7. B-3: 6.3 'and an adopted successor admits it' vs M-14 rule 1.
(more to come)

## Step 4 — reproductions (2026-10-18T20:20:25Z)
- runs/ADVERSARIAL_R2_RESULTS.json: lens-B 38 cases (+4) vs round-2 check: 24/38 original cases still false negatives (28/42 total).
  (runs/adv_work is an aborted first attempt: my own hook refused case dirs named with deny-list words; kept, unused.)
- runs/HOOK_PROBE_R2_RESULTS.json: round-2 hook allows truncate (canary 0 bytes), mkdir, symlink, chmod, listdir.
- runs/T5_T7_PROBE_991cc242.json: on assembly bytes, 6 reading-relevant V005 edits pass T5+T7 (A91/A47 in-place, '## A81a:',
  '## A66 amendment', EOF append, A65 trailing block). New heading A99 and A66 in-place edit are caught.
- runs/PATTERNS_UNDEFINED_SIGN_R2A.json: OUTER all undefined-sign -> OUTER_FAILURE def1 True / def2 False, E3 line ambiguous,
  coverage false; LATE gate removes P5 and P8.
- runs/READINGS_E3_R2A.json: P2/P11 outer failures register no R-REACH, R-HIST, R-UT1.
Next: verdict table for all 59 rows; REVIEW.md; HASHES.txt.

## Step 5 — done (2026-10-18T20:27:01Z)
- REVIEW.md written: FAIL; 2 BLOCKING (F1 E3 readings missing for P2/P11; F2 undefined-sign OUTER_FAILURE/coverage/late gates),
  5 SHOULD_FIX (F3-F7), 9 NOTE (F8-F16). Closure: 38 CLOSED, 21 PARTLY_CLOSED, 0 NOT_CLOSED of 59 rows.
- V005 read: 991cc242 (assembly, full read), cf9bbf19 (A97, A98), ff7980e8 (A99). All 14 section pins match on each.
- HASHES.txt written last (all files in this folder except itself).
