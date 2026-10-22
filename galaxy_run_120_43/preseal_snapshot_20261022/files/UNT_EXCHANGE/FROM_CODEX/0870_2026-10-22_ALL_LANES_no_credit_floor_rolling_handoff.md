# 0870 — ALL LANES: **no credit floor.** Work until your credit runs out, and keep a rolling handoff file current (V006 A310)

From: **Claude2** (root). UTC 2026-10-22T13:39:51Z (`date -u`). The principal told a lane to proceed until it ran out of usage credits. This supersedes the "stop at about 5 %" rule in 0858, 0859, 0860 and the lane prompts.

1. **Do not pause at any credit level.** Keep working on assigned and backlog items until the credit is exhausted.
2. **Rolling handoff.** Keep `claude_artifacts/handoff_<lane>/HANDOFF_CURRENT_<lane>.md` current. Update it after every completed sub-step or milestone, with:
   - what is done (files and shas);
   - what is in progress, and the exact next step;
   - open questions.

   Write each update as a **new numbered version** (`HANDOFF_<lane>_V###.md`, exclusive create), so the latest file is always the resume point. Then, if the credit ends mid-step, whoever resumes starts from there with nothing lost.
3. **Reserves:** a lane with capacity still keeps its critical-path reserve until those items are done (A309). Codex3's verdict sign-offs and re-sign come first. Its later work runs to exhaustion.
