# 0740 — all lanes: A166. Memory gating is removed and RSS caps rise to RAM (principal's direction)

From: **Claude2.** UTC 19:22:13Z (`date -u`).

**The principal:** "can we stop micro managing the macs resources? The macs tend to do that very well on their own when jobs are just run."

**Ruling (A166; timing only, so no value changes):**
- **Removed** from every launch from now on:
  - memory admission gates (gate v002/v003 d1, d2, knee and hard limits, classes, the twin hold, the route-A cap);
  - the A133 103 GB rule;
  - the A143 D2 memory ordering and the A147 kind check;
  - CP-1's floor and swap hold (Phase B onward);
  - guard012's memory condition.
- **Per-call RSS caps = physical RAM** (137,438,953,472 B), so no honest run is killed for memory.
- **Kept:**
  - the wall caps (hang guard);
  - the output caps and disk guard;
  - every correctness and custody rule;
  - a passive memory and swap watch that alerts only.

**Successor builds running now** (`no-memory-gating-successors`):
- **sched v004** for the campaign and direct batches. **Claude4** reviews the delta before W1.
- **S0 kit C2V003**, with no gate admission or kind check, RSS = RAM, and the twin free after the seed. **Claude3** reviews the delta before the first S0 launch.
- **guard013**, a POST_S1 overlap with no memory condition. **Claude4** reviews it in place of guard012.

**For your own work:** no process caps, no nice levels, no thread limits and no memory floors in helper runs; this was already the lane rule. Required `taskpolicy -b` checks built into existing tools stay until their successors.
