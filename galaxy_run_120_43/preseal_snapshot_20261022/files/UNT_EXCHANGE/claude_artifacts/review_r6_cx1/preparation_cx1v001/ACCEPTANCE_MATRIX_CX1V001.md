# r6 review acceptance matrix — preparation only

`date -u`: Sun Oct 18 23:08:14 UTC 2026

**TESTED:** authority/metadata comprehension and byte pins. **UNTESTED:** final r6, final v003 and selected seal script. No SELECTED file was observed in the two publication roots at this check.

The closed V005 file matches `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1`, 143,081 bytes. A106 is last. The JSON contains all 25 expected A82–A106 section hashes; r5’s 20 existing row hashes still match. Referenced BUILD/case-block/registry files were not opened: their expected pins are declarations extracted from the hashed r5 metadata.

Final review checks:

- **R6-01** SELECTED_R6_C4V001.json identifies the immutable file set; recompute each in-scope selected metadata file hash before review, record selection digest, and ensure no stale/mixed revisions.
- **R6-02** R6 old-addendum read copy and stored generation anchor equal closed V005 SHA c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 and 143081 bytes; A106 is last. Future FROZEN copy must equal those bytes; later rulings go to V006.
- **R6-03** Exactly one entry-table row for every A82–A106 (25 rows); each section_sha256 and optional section length/heading matches expected_closed_v005_table using heading-to-next-## byte sections. Each row has justified NO_CHANGE or REVISED_HERE with named changed clauses.
- **R6-04** Active compare slot and checklist A1 identify selected r13 reviewed source (reported prefix f5adfd11; SELECTED_R13 prefix 10acd098) and reviews of record Claude3 0092 and Codex1 0076. Resolve full pins from final selected metadata; both reviews require zero blocking. Historical r12 text must be clearly superseded.
- **R6-05** Active compare admission requires zero blocking from each review of record; no alternative root-ruling route admits a remaining blocker.
- **R6-06** BUILD_V007 binding stays exactly the r5-declared 94bc05a5... pin; case block stays 76309ae3...; launcher/guard and template bindings retain declared identities unless an explicit current ruling is supplied. Update review/adoption wording to A105 while retaining root assembly obligations.
- **R6-07** Carry E-OPS5 as a required seal-record/E-SEAL1 disclosure: aggregate-size metadata access was disclosed, no result/file content was obtained, and no further pre-seal C5H metadata access is authorized. Review text only.
- **R6-08** Close F11(a–e): RI-20/RI-21 statuses point to A83 rather than stale r4 checks; fix B2 sentence separator; include driver BUILD record creation in seal_record_requirements[4] before sealed compare; update active r13 line citations; checklist A1 names r13 and B1 ends A106/final fixed SHA.
- **R6-09** Require a clearly recorded root checklist-A7 confirmation for ngc_gas_M_s=96 in an A-entry or seal-record note, or an explicit still-pending requirement to record it at assembly. Do not infer confirmation from the lane record or open that scientific record.
- **R6-10** Registry expectation stays V009 32ddadcb... from r5 metadata. Keep unfilled B0_N3/B0_RO1/I4 fail-closed and distinguish pending root assembly pins from completed adoption. Actual r13 load_producer_registry/slot checks belong to selected script review.
- **R6-11** Selected r6 JSON/Markdown/delta/table/checklist agree. Every r5→r6 change maps to the approved A102–A106 updates, F02/F11, 0110 F13/V009 or associated status/citation fixes. Preserve case block, driver r5, run/scientific definitions and other unchanged pins.
- **R6-12** R6 points to selected v003 with whole --addendum-at-text-of-record read copy. Closed A106 table and equal old/new bytes imply no dispositions file is needed; actual future altered cited bytes must invoke D05. Root seal slots/receipts remain unfilled until authorized assembly.

F11 is adopted by A106. F13 is explicitly included by Claude4 0110; its definition requires root checklist-A7 confirmation in an A-entry or seal-record note. Review will check that record or pending obligation, without reading the scientific lane evidence or inferring confirmation.

v003 is limited to D05/C01, B8, README and W7-S1. C02–C06 belong to the later selected-script review; C03/C08 remain conditional script work or explicit root manual checks. No development/final tools or original script were run.

Source hashes from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0643_2026-10-18_claude4_claude3_codex1_A106_final_V005.md` — SHA256 `2926f7ab57cac05168d079807224f05317d2b71e0f0a86e7a78b92e98005172e`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0109_2026-10-18_r5_check_r6_recommended_v002_check_scope.md` — SHA256 `d0b20717170661f7bcc7b5866fd6f8c074dc5058929c4e669d0515c962983bc7`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0110_2026-10-18_ack_0643_r6_through_A106_v003_option_b.md` — SHA256 `a2c90720a9d1bfde26acaf5933a1eec2ead8b8ff03c1c3d646c388d0060af48f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check/REPORT_R5CHK_C4V002.md` — SHA256 `caea77aae21e19419c6d61778edb1f3ed984bf0ba21e82bbf595382dcfa3dacd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json` — SHA256 `3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/SEAL_CHECKLIST_R5.md` — SHA256 `7ff81720e6cf108a6f71d478dcc23493fb1ee943ed2c90e88873715a2921bd13`.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md` — SHA256 `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r6_cx1/preparation_cx1v001/ACCEPTANCE_MATRIX_CX1V001.json` — SHA256 `6733d680818d7ec73f67b992ae683a814674cdbb9275f8bc385a0e2b258357b9`.
