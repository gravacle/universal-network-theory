# PARTIAL — verify_consistency_2 (adversarial verification of L-C02)

Started: 2026-10-18T19:24:01Z (date -u)

Object hashes verified from bytes (shasum -a 256), all match HASHES_R2.txt:
- PREREG_MISS_READING_R2.md 6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143
- CLAUSE_SOURCE_MAP_R2.md b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b
- ROOT_ITEMS_R2.md 1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f
- NUMBER_PROVENANCE_R2.json c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832
- tools/check_target_free_c4v001.py 85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7

Status: reading quotes and evidence. No verdict yet.

## Update 2026-10-18T19:32:49Z (date -u)

V005 read at 2026-10-18T19:29:49Z: 50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477 (last heading A92). V004 487d4449... and V003 5bef6552... match.

Quotes: all five quoted r2 strings are present at the stated lines (L168, L169, L196, L207, L340).
Evidence: the lens's CASES_RESULTS_V2.json reproduces the claimed candidate lists for C01, C16, C21 and 110 'C-3/C-8' events.

Working refutation (to be confirmed by script):
- The 110 events come from the lens's own reading_status() (lensc_classifier.py), which adds 'OPEN' next to 'consistent' for every untested reading by construction and applies none of the text's precedence clauses.
- Precedence clauses present in the bytes: PREREG L169 ("stays OPEN, whatever the score shows"), L201 (R-GEO "stays OPEN by construction"), L207 ("R-TSR stays OPEN"), L284 (R-DRIFT stays OPEN if NOT_EVALUATED), L363, L366; ROOT_ITEMS M-4 L89 ("stay OPEN after the score, whatever it shows").
- R-GRID's deciding test DT-ALT (ORIGINAL_K) is EVALUATED_BEFORE_FREEZE (L44, L185); the lens hard-codes test_run False.
- (iii) R-DRIFT AGAINST: the DT clause L199 assigns the decision to DT-S0G; the consistent column is always true whenever R-DRIFT is reported.
- Residuals: R-DRIFT NOT_DECIDED (already L-C08 (d)); A48 gap-filler inoperative (already L-C24); DT-T1a timing for R-ML/R-SPEC/R-GEFF.
Provisional verdict: core claim refuted; severity NOTE. Not final.

## Update 2026-10-18T19:39:47Z (date -u): FINAL

- tools/reapply_precedence_lc02.py was run, and PRECEDENCE_REAPPLY_LC02.json was written (exclusive create).
  - All 24 quote checks pass.
  - The evidence reproduces: 110 events; C01, C16 and C21 as the finding states.
  - The consistent column holds in 132 of 132 reported reading instances.
  - Event classes: EXPLICIT_OPEN 78; GENERAL_L169_OPEN 13; DT_CLAUSE_STRUCTURAL 3; L169_OPEN_TIMING_DEPENDENT 9; LENS_INPUT_ERROR 2; OTHER_FINDING_L-C01 2; RESIDUAL_UNRULED_ALREADY_L-C08d 3.
- V005 moved during the check: 50fe0f1c (19:29:49Z), then 6145a1f9 (19:36:12Z), then 352e9f7a (19:39:13Z). The cited pins A48, A63, A64, A65 and A66 still match, and A90–A94 contain no reading-status terms.
- Final verdict: REFUTED as stated. Severity NOTE. Fix not sufficient as written; a better fix is in VERIFY.md §4.
- VERIFY.md, REVIEW.md and HASHES.txt are written.
