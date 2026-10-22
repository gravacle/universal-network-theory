# 0350 query-coverage adapter: distinct review record

Reviewer: CLAUDE2 helper 0348/0350-review, a separate Claude helper that did not write the adapter. It worked on synthetic data only and never read the real bundle or the root review file.

| Round | Reviewed | Verdict | Outcome |
|---|---|---|---|
| 1 | adapter V001 813c9915…, contract V001 1dec8b7b…, harness 32/32 | **PASS_WITH_NOTES**: F1 settings wildcard, F2 partial correction refs (SHOULD-FIX); F3–F8 notes | V002 |
| 2 | adapter V002 980662d6…, contract V002 843bc166…, harness 42/42 | **PASS**: F1–F8 FIXED (F3/F4 by documentation); one cosmetic note (the name `ids` is reused for a helper and later a list inside context(); correct as ordered; left unchanged) | Candidate for root |

Round-2 evidence:
- An independent Fraction oracle matches on the base bundle and on a tricky query set.
- 3068 emitted pointers all resolve.
- 2064 emitted numbers are byte-identical to the stored JSON tokens.
- Degenerate grids fail closed.
- Publication behaves exactly as adapter V005.
- No leaks.
