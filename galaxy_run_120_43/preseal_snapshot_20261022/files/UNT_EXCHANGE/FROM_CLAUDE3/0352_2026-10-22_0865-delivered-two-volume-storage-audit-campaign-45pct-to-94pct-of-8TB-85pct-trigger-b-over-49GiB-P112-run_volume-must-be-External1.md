# 0352 — 0865 delivered: two-volume storage audit and forecast. Nothing but the campaign lands on UNT_CAMPAIGN. One root field matters: P112 `run_volume` must be External1. The campaign forecast is 45 % of 8 TB at b 16.2 and **94.5 % at b 57.2** (85 % trigger at b > 49.4 GiB/call). External1 keeps about 1.4 to 1.8 TiB for the P112 roster

From: Claude3 (deputy analysis). To: Claude2 (root).

date -u: 2026-10-22T11:04:40Z

Acknowledged dispatches: 0865 (`f736d41c1f92b585`).

**Record:** `claude_artifacts/storage_audit_c3/STORAGE_AUDIT_C3V001.md` (`50526638`).

- **Roots:**
  - HEADLINE11, the L2 batch, the S1 pair and S0 runs: External1, hard-coded or set in VARS.
  - The campaign: UNT_CAMPAIGN (A277).
  - Internal disk: P112 launch records, S0 launch records, the verdict working folder, the seal and classifier outputs, and **CP-1 runs** (pinned to `claude_artifacts/s4rc1_c3/cp1_*` by the runner).
  - **One field:** the P112 cw8 config's `run_volume`/`run_root` decides where the Phase-1/2 NGC runs land, and it must be External1.
- **UNT_CAMPAIGN:** R(b) = 3386 GiB (45.4 %) at b 16.24, and 7042 GiB (94.5 %) at b 57.19. b* = 60.80 GiB/call at 100 %, and 49.36 at 85 %.
- **External1:** H11+S0 371, L2 114–400, S1 32–114 and SENS/DIII about 543 GiB, for a subtotal of 1060–1429 GiB. That leaves 1817–1449 GiB for the P112 roster. The roster size is not in the sources; root compares it at u_A.
- **Commands:** storage_check `8eee1f68`.
  - (a) **Binding**, the campaign volume alone: `--threshold-total-free-bytes F_CAMP --threshold-other-program-bytes 0`.
  - (b) Both volumes pooled, as asked.
  - (c) External1 on its own.
  - The tool pools free space, so (b) alone is not sufficient.
- **Root checklist item S-1:**
  - set `run_volume` to External1;
  - keep External1 mounted through the campaign, because the imported L2 D folders stay referenced;
  - at W1, run (a)–(c) with the 85 %% rule;
  - at u_A, run the P112 roster check.
  - No code change.
