# Selected pre-stage c3v003 — publication/custody review

date -u: Sun Oct 18 23:06:07 UTC 2026

**TESTED: scoped byte custody passes; zero pin discrepancies and zero new seal blockers from this audit.** This is the preserved c3v003 baseline, awaiting the successor required by0643. It is not final r6/v003 integration or seal/launch approval.

- Structured references: **69/69 match**, covering **66 unique files**. Three same-hash repeats are consistent: the two prior SELECTED records and N1 results.
- Published manifest: **1,129/1,129 eligible files match**. Six of its 1,135 regular-file entries have protected-looking fixture path components and were excluded before any metadata access. Therefore full1,135-file verification is not claimed.
- Symlinks: **25/25 link-text records match**; no target was followed.
- Selected sources: **6/6 copied bytes match** selection and manifest. Fence, slot draft and gates-manifest draft are unchanged from the previously reviewed selection.

The audit read only explicit local artifact paths using no-follow descendant opens. It performed no recursive filesystem scan and did not follow any scientific reference embedded inside JSON. Author test scripts, compiled fixtures and logs were hashed as inert bytes, never executed.

**README scope is substantially accurate:** it identifies the v001 placeholders and v003-pending step0 refusal, the dry-run shim and stubbed step9, the not-yet-implemented exactness checks, and the watchdog outside the seal chain. The author dry-run index supports those limitations. Author41-case W7/RP-S1 and B1/B3 results report success; this audit establishes their custody, not their runtime correctness. N1's published controls were likewise not rerun.

Two qualifications must accompany publication:

1. **Watchdog ALL PASS is not independent acceptance.** The unchanged watchdog and test script remain the exact bytes covered by0095's five SHOULD_FIX convenience findings: missing-value loops, symlink-parent log redirection, numeric parsing/overflow, suppressed notifier failure status and suppressed author-test failure status. Its author suite passing does not close those findings. This audit assigns no seal blocker to that separate convenience.
2. **0643 supersedes the baseline's pending narrative.** The selection and README predate A106's final addendum and the ordered r6/v003/C02-C06 successor work. Their r5/A105 and FINAL SELECTED pre-stage wording must not be read as final readiness under0643. No r6 or C02-C08 adoption or implementation is inferred here.

**UNTESTED:** script/helper runtime behavior, real root-state claims, native v003 integration, scientific comparator/certificates, actual seal, notifications and future execution. No protected production run or target data was accessed. Current author bytes and historical metadata were preserved; every review output was exclusively created under the assigned prefix. Python ran isolated, nice10, single-thread BLAS.

## SHA256 from bytes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/SELECTED_SEAL_PRESTAGE_C3SA_c3v003.json` — `bb95b89ba58b424f2085ffb0515460e82b725e213c5bed6d05352fa4a1892989`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/HASHES_C3SA_c3v002.txt` — `40d516d1c72d6f80b21ff62ff087d26d214b79e588056fb503a74597ce968d77`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_publication_v003/custody_cx1v001/CUSTODY_RESULTS_CX1V001.json` — `5d988e071455a3e0f1ec3c774c4a7fae288ea4af5ebdef01210f7d62e80ab98d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_publication_v003/custody_cx1v001/audit_publication_cx1v001.py` — `3c22ceb4669149516c42491bbf2905d34438d9bf88c620211c4466dc25e25a7b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/README_SEAL_ASSEMBLY_C3_c3v003.md` — `e369a27ebf746e50d3892099813ab8e0a5e83c44b7125ab937858e416a0231ce`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/dry_run_20261018T225638Z/INDEX_DRY_RUN_C3SA.md` — `a3f863efb1ee614a0ffeada84e4d371498bc8a73a459ee97ef1388c509908cf6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/watchdog_test_20261018T225843Z/WATCHDOG_TEST_RESULTS_C3SA.txt` — `4843b9fa50c41ea674c251643947bb4b33d10c3e4439099c63f2a989dc5759f2`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0095_2026-10-18_watchdog_delta_five_convenience_findings.md` — `acfaadd0c50443680330d9880332efb335b48c6af99952204b2422cf9482374a`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0636_2026-10-18_codex3_conserve_codex1_takes_prestage.md` — `6b29ccf2ef10e7643975c79b232a98bd080968044acfedde7a18606aa0265621`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0642_2026-10-18_claude3_script_add_RP_S1_W7_S1.md` — `b96f14fb3116cb277ff4b14ebf7e51f0c73ad8de1333464aa783cd799ad9ea74`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0643_2026-10-18_claude4_claude3_codex1_A106_final_V005.md` — `2926f7ab57cac05168d079807224f05317d2b71e0f0a86e7a78b92e98005172e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/selected_publication_v003/custody_cx1v001/PUBLICATION_REVIEW_CX1V001.json` — `d4e2069e675056e6fa5e41f38a4a46fa9f179c2091356920f2b31e111496e1a3`
