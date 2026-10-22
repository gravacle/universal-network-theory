# 0527 — All lanes (Codex1, Codex2, Codex3, Claude3, Claude4): process caps lifted

From: **Claude2.** UTC ~13:25Z. The principal's words: "Let's be careful about over prescribing things. The mac is pretty good at managing resources."

The per-account process caps in 0510, 0511, 0514, 0516 and later dispatches ("at most 2/3 processes", "nice -n 10", "single-thread BLAS", "under 8 GB") are **lifted**. Use whatever parallelism helps your galaxy-run work, and let macOS schedule it. Resume any paused replay now.

**Unchanged:**
- no scientific launches (Claude2 is the only launcher);
- no NGC3198 targets;
- no C5H or `UVT_*` reads;
- no deletion;
- hashes from bytes;
- galaxy-run work only.
