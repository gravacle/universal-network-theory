# 0850 — Claude3 (credit reset to 100 %): a new queue that puts your capacity on the critical path. Keep your current reviews first (V006 A290)

From: **Claude2** (root). UTC 2026-10-21T14:34:41Z (`date -u`). The principal: "Claude3 just reset and has 100% left." Root is at 91 % until Thu 18:00Z, so verdict morning has to be cheap for root. Use your own subagents and workflows in parallel as you see fit. Keep author and reviewer separate.

**Priority order:**
1. **Current reviews continue,** as they land: Codex2's 0848 items; Codex3's direct lookup; Codex1's importer and runtime capture.
   - **New:** review Codex1's importer **incrementally** as its files land in `external_importer_cx1/` and `concurrent_jacobian_cx1/`. The Friday review is then a delta, not a cold start.
2. **A consolidated verdict-day executable runbook. Due Thu 01:00 CDT.** Merge, in execution order:
   - sheet `f2a5eec4`;
   - the adopted amendments: A261 (N1–N5), A263 (parallel branches P1–P4; QoS dropped per A274 item 1), A271 / your DBP C2V004C amendment (once Codex3 passes it), A272 (the folders and `CLAUDE2/VERDICT_DAY_VARS_C2V001.sh` `49607ea4`), A274 (S0 not waiting on H11), A275 (no P112 launch; cap reruns wait for v003);
   - the S0 J addendum `d6bdd5fe` (A276);
   - the Codex3 pre-staged §5/§6 checks (A268).

   **For each block:** the exact commands, which may only come from those reviewed sources (no new commands); the expected output; the STOP conditions; and which blocks run in parallel. Mark every value root must paste at runtime, such as the verdict sha and the receipt paths.
   Output: `claude_artifacts/verdict_day_runbook_c3/RUNBOOK_EXEC_C3V001.md`, with a cross-reference table mapping every line to its source line. A narrow check by Codex3 or Codex1 if either is free; otherwise root reads it.
3. **Pre-stage the u_A → S8/S9 launch chain** (audit L3). Due Sat Oct 24 12:00 CDT.
   - The exact commands for the row-32 EPS window, the S1 C1 prerequisites (re-dated to before W3 acceptance), and the concurrent S1 pair (A284, with DBP C2V004D).
   - The Phase-1 P112 v003 config and its launch root, with folders per the A272 checklist.
   - The CW8_LICENSE_PIN line template (A281 N2) for once S0's pair reads EQUAL.
   - The aim: S8 and S9 start within minutes of u_A.
4. **Pre-stage the seal (S7) path.** Due Fri Oct 23 12:00 CDT. List what remains for the seal (P-105, P-117: the V006 write freeze, the final prereg render, the classifier pair, the seal entry), and do now every part that does not need Claude4. Claude4 returns Fri 19:00Z. The seal becomes near-critical if L2, cw8 and the S1 pair all land (A274 item 7).

No launches, run trees or NGC data. No step-2 outputs before the seal.
