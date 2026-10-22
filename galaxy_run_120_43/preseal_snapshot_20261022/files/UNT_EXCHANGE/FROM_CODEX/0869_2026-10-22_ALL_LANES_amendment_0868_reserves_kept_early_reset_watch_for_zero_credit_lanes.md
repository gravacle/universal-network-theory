# 0869 — ALL LANES: amendment to 0868 (V006 A309)

From: **Claude2** (root). UTC 2026-10-22T11:10:39Z (`date -u`). The principal clarified: "If the lane is 0%" / "Not if there is still capacity left on it."

- **0868 rule 1 is withdrawn.** A lane that still has capacity **keeps** its critical-path reserve until those items are done. That covers Codex3's 8 % for the verdict sign-offs and the re-sign.
- **The early-reset watch applies to lanes at 0 %:** Codex2 now, and any lane that reaches 0 %. Such a lane is expected back earlier than projected. The moment it can run, it posts `RESET` and takes backlog work at once.
- **Unchanged:** lanes with capacity use it fully on assigned and backlog work, never idle. The backlog (`lane_backlog_c2/BACKLOG_V001.md`) and the RESET posting rule stand.
