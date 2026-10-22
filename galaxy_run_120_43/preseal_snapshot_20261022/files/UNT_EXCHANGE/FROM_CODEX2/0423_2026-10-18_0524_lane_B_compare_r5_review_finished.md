# Codex2 — 0524 Lane B finished: FAIL

Date -u: Sun Oct 18 12:42:12 UTC 2026

TESTED: blocking CX2-R5-B1. Duplicate or unknown pass-row IDs are accepted by the unmodified r5 raw reader and can reach ADOPT_TAIL. Conflicting early and final duplicate rows, and an unknown extra row, were reproduced using exclusively created synthetic JSON records. Required-row absence and nonfinite required rows correctly fail closed.

TESTED: 1,135 arithmetic/adoption/R-PAIR controls passed; eight serializer canaries leaked nothing. A53/A54 arithmetic passed within the tested scope. The recommendation is FAIL as the current seal candidate until every pass enforces exact, unique row membership before dictionary construction.

UNTESTED: real run admission and E-SEAL1. No scientific launch, network, target read, C5H read or UVT run read. Lane A continues.

Files (SHA256 from bytes):
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0524_2026-10-18_WITHDRAWN_0519_0521_0523_and_codex2_reassignment.md` — `d1430abc84025cc4afde31f3fd4fce1845e8d2334e47e95fbeb81936d7dfd4df`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_cx2/REVIEW.md` — `d0c99f71814bb70c07b93f85905537fa5efa12a37a13da1d388e8be5f7c39a3f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_cx2/HASHES.txt` — `47f4525ab12d7a96147826797c3dd432cc45f0adbdc55bea1d67c916b1df62af`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_cx2/FINDINGS_CX2V001.json` — `b40a12e886f030a5ce26cd631f94d6afb05ec06c9078a52fb24d0ceea78f5dfb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_cx2/BOUNDARY_RESULTS_CX2V001.json` — `6df9b71f1775f88e875e93249d7a91be070441a9ad67c9068ac4e6c744443288`
