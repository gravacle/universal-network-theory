# 0348 distinct review record (V002: adds round 3)

Reviewer: CLAUDE2 helper 0348-review. It is a separate Claude helper and did not write the adapter. It used synthetic inputs only and never ran the adapter on real inputs.

| Round | Reviewed | Verdict | Outcome |
|---|---|---|---|
| 1 | adapter V003 f22cff00…, contract V004 7cd80070…, harness 3d5b1625…, receipt e4dbc855… | PASS_WITH_NOTES. SHOULD-FIX: #1 unguarded post-link samefile; #3/#4 stale contract exit and write text. Plus 8 NOTEs. | Adapter V004 + contract V005 |
| 2 | adapter V004 1a06446c…, contract V005 50e2b7e3…, harness bf8ca50f…, receipt 182abdb7… | PASS_WITH_NOTES: 10 FIXED, 1 PARTIAL (aliasing; wording). New SHOULD-FIX N1: abspath applied after preflight (symlink/.. could make preflight and publication use different paths). NOTEs N2–N5. | Adapter V005 + contract V006 fix N1 (path made absolute once in main before preflight), N2 (actual mode reported), N3 (post-link steps catch any exception), N4/N5 (wording) |
| 3 | adapter V005 fc9cdcfa…, contract V006 1e8a9a7c…, harness 17b70cd7… | **PASS**: N1–N5 FIXED, no new findings; harness 96/96 reproduced; all 27 earlier probes re-run (P1–P19, P23, P24 OK; three stale checks reflect now-documented behaviour) plus new N1/N2/N3 probes | Candidate for root: adapter V005 + contract V006 |

Supersedes REVIEW_RECORD_0348_V001.md (preserved), which predates round 3.
