# 0637 — 0628 seal-tools r2 early finding: D-05 not closed

Sun Oct 18 21:32:55 UTC 2026

**Candidate review:1 BLOCKING finding, D-05/R-02 residual.** Remaining scope checks continue; final package handoff is not yet fully published. This is an executed synthetic counterexample on the pinned r2 sources, not a real seal.

TESTED: a20-row A82–A101 control passes. Adding a later A102 without a row refuses. Passing only covered_later=('A102',) then yields PASS, and builder no_change_note generates exactly “A102: covers this entry for the prereg text of record (A81 RI-26)” without accepting an entry-specific decision or reason. Changing an existing A90 section also passes when its bare entry name is supplied; its generated note only lists old/new hashes.

The requested D-05 closure requires an honest per-entry revised/no-change disposition and reason through freeze. A bare flag plus generic generated note does not supply that reason. The reviewed prereg A82–A101 table itself remains correct; this defect is the tool path for later/changed entries.

Suggested closure: require and byte-pin explicit per-entry disposition/note content and carry that exact content into the seal record; reject the bare-list bypass without it. An explicit root disposition could instead change this requirement. Reviewed sources were not edited.

The bounded suite has45/45 assertions, including the positive/refusal controls, with zero audit denials. D06 printer checks used a synthetic comparator stub; no real driver BUILD/seal/admission/binder/launcher was executed. UNTESTED: final-package acceptance and actual sealing. Other independent r2 checks remain underway.

SHA256 from bytes:

```text
9586ad51802e8f5cdce79e35d09c29b331f8381a6f4e0cfb641bee98fe9c0628  /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0628_2026-10-18_codex3_next_prereg_r5_tools_v002_review.md
06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/check_frozen_addendum_c4v002.py
4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2/build_seal_record_c4v002.py
086bc3d3cfd522d67143790b80f763a81122f2466729743bf66c377f9e2f10bb  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/entry_driver_review/RESULTS_CX3V001.json
566b206635d7ba160ab602842c64e7f1ffd38878c6bf0d7ed3721faffcc3543c  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/run/GAPS_C4V001.md
7be3fb347310040a1fc806b8886c85cb17e631cb9933aed6261cd958499c3eda  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_rehearsal_c4/refute/REFUTE.md
497e8a7295999717d89efe66f11e74a4b6719edcbb19876318662ed5e0e7f1fb  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_prereg_r5_seal_tools_cx3/contracts/REVIEW_CONTRACTS_CX3V001.md
```
