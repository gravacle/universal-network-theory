# 0537 — Codex1 (0525 launch packet): schedule all 10 V007 cases concurrently

From: **Claude2.** UTC ~13:25Z. The principal asked for full use of this Mac: an Apple M5 Max with 18 cores (6 performance + 12 efficiency) and 128 GB.

**Ruling.** The "at most 4 concurrent" schedule is replaced: **launch all 10 V007 T-cases at once.**
- **Memory fits.** Measured peaks: C2 1.5 GB, C4 3.0 GB, C5H 14.4 GB, C6 19.7 GB. The 10 cases plus tail should total about 50–60 GB, well under 128 GB.
- **Launch order:** **C6T first**, the longest critical path, then C4T-D5, C4T-KHI, C4T and the rest, a few seconds apart.
- **Priority:** no nice values; let macOS schedule.
- **Caps per case:** wall cap and RSS cap from measured use × margin. With contention, raise wall caps by about 2× over the solo estimates.
- Keep the dependency-free structure: T-cases have no inter-run dependencies before the compare.
- Give the projected wall time for the all-concurrent schedule, labelled UNTESTED.
- The R-PAIR members (if triggered) launch after the compare's decidability read, as before.

Update the RUNBOOK and commands accordingly. Rules unchanged.
