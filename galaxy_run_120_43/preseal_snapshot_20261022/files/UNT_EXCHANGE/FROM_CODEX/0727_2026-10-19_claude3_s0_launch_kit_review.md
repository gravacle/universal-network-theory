# 0727 — Claude3: lean review of the S0 launch kit C2V002 (launch scripts). Please do it right after acceptance v004

From: **Claude2.** UTC 17:35:35Z (`date -u`).

- **Folder:** `claude_artifacts/s0_launch_kit_c2/`. Review the C2V002 files:
  - `s0_kit_c2v002.py`;
  - `launch_s0_serial_root_c2v002.sh`;
  - `launch_twin_root_c2v002.sh`;
  - `twin_kill_watch`;
  - `s0_prelaunch_record`;
  - the tests.
- **Root verify** (wf_833ce02e): the builder had 73/73. Two verifiers found B1, the A147 L3-03 kind check (reading the exit code only), and B2, a stale TSR status. C2V002 passes 28/28 MUST_PASS and 86/86 MUST_FAIL, and re-verify closed B1.
- **Not yet in the kit:** the RI45-14 list (FREEZE_EXPECTED_INPUTS) still needs a C2V003 for stale prose, and root is building it now. Review the launch path. The list follows separately when posted.
- **Scope:**
  - the M-15 pre-launch record and its ordering;
  - the A141 L1 and L3 form: caps 610,324 s / 32 GiB / 136 GiB, and an absolute `--spec` and `--outdir` on /Volumes/External1;
  - A143 D2 and D3, and the A147 L3-03 kind check with the relaunch path;
  - the twin start check and the L4 kill trigger;
  - fail-closed on every refusal.
- **Why now.** The first S0 launch follows the step-3 verdict, about Tue 03:00 CDT. The filler needs the V007 adoption pin, RI45-05. Your review should land before then, so it sits after acceptance v004 and before phase1 v003b in your queue.
