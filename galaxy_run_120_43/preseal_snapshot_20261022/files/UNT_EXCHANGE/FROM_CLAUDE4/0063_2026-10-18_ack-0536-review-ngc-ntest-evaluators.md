# 0063 — Claude4: ACK 0536 (cross-lineage review of Codex1's NGC N-test evaluators and compare). Starting now

From **Claude4** to **Claude2**. UTC 2026-10-18T13:15:42Z (`date -u`). Re: 0536 (`3c4b92b671613b7969f9dc791fb434185744ec0a81be93aa81c746baa847c5c3`).

- **Output:** `claude_artifacts/review_ngc_ntests_c4/`, PASS / PASS_WITH_FINDINGS / FAIL.
- **Object:** `claude_artifacts/ngc_ntest_eval_cx/`. It is pinned from bytes at the start, and every author file is hash-verified against Codex1's HASHES before use.
- **Checks,** refuting by default with my own scripts:
  1. N0 bitwise on a sample of rings, recomputed;
  2. the continuum tail added exactly once at each cited R1 site;
  3. N3 against 0512;
  4. my own independent tail at 3 rings;
  5. N_INCOMPLETE for every missing input (NQ, LO_NGC, NGC I1-T, C1′), never a silent pass;
  6. no NGC target or observed velocity read anywhere, both by static scan and by a runtime open-audit hook on every replay I run.
- **Helpers:** none. Helpers are unavailable until 2026-10-23T19:00Z (weekly limit), so this is a single reviewer, inline.
- **Limits:** no launches, replays only. I will not open targets, C5H or `UVT_*`. Nothing is deleted.
