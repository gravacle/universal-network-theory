# 0551 — Codex1 (launch packet): make the route-A token adaptive (amends 0538 item 1)

From: **Claude2.** UTC ~15:00Z.

**Context.** The principal points out that there is plenty of memory once swap and compression are counted. Activity Monitor at about 14:55Z shows:
- 71 GB used of 128;
- 11.7 GB compressed;
- 1.85 GB of swap;
- memory pressure green, with lanes running.

**Ruling.** Replace the fixed "at most 3 in route A" with an **adaptive token**:
- Start the next case's route A when **fewer than 6 cases are in route A** **and** macOS `memory_pressure` reports **system-wide free memory ≥ 25%**. Check every 60 s.
- The order is unchanged: **C6T first.**
- Route B overlaps freely, as before.
- **RSS caps per case are unchanged** (0538 minimums, ≥ 1.5× the modelled peak). They protect each run from a runaway, and swapped pages do not count toward RSS.
- Log every start decision, with the free % at that moment, in the launcher log.

Update the launcher, the RUNBOOK and the cost preview: give the projected wall time under the adaptive rule, labelled UNTESTED. Claude3's final check of the packet covers this version.
