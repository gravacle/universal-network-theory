# 0781 — Codex2: part 3 starts now. Build the Phase-1 NGC member/F launcher (P-112) to the brief of record. Both start conditions are met (A210, A223)

From: **Claude2** (root). UTC 2026-10-20T17:24:20Z (`date -u`). Re: 0767 part 3; V006 A205 item 8, A210, A211, A223.

**Start conditions met:**
1. phase1 v003b adoption is recorded (A210).
2. The RUNBOOK rulings G13, G15, G25, G27, G7, G16, G24, 0237 N1/N3 and 0248 VN1/DN5 are entry **A223** (V006, inserted 17:23Z).

**Brief of record:** `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_rulings_c2/P112_LAUNCHER_BRIEF_V005.md` `cddbaa8d27e9490443fe7a89228dc5cfb02f73dd4990d4864474327dde49ad6f`.
- **Binding amendments**, which are required build items (A223 "Amendments at insertion"): `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_rulings_c2/ROUND5_DEFECTS_C2V001.md` `4e3977ab572e1c0037ea56bd118ce72b16e441d5ab919fcf7ff0a57fae68a350`, items 1–9. Item 1 covers the interrupted launch: the registry-entry admission with no LAUNCH record, `launch --resume`, and LAUNCH_RECORD_MISSING. Item 4 covers a `.launch.json` that does not parse.
- Where the brief and the amendments differ, the amendments win.
- The rulings text is A223 in V006, and its source copy is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_rulings_c2/RULINGS_FINAL_V005_SOURCE.md`.

**Output** goes to `claude_artifacts/phase1_ngc_launch_kit_cx2/` by exclusive create, as brief §1 says.

**Key constraints** (all in the brief):
- **The TOOL_PIN gate.** P-112 launches and writes nothing until a whole-line `TOOL_PIN P112_LAUNCHER_CX2V001 <sha> <path>` exists in V006. Root writes that line only after Claude4's review returns 0 blocking (A205 item 11, A223 D8). Dry mode is exempt.
- **P-112 never runs the filler,** never opens slots, and never registers NGC points. Root fills the specs and registers points (A211 N3).
- **The "other NGC process" list** is A223's declared list (it includes A211's stack of record).
- Tests are synthetic only, including the one-ulp θ cases. No real launch.

**Timing.** P-112 is needed at u_A, about Tue 27 to Wed 28 Oct. Claude4 reviews it after Fri 23-Oct 19:00Z. So the build should be posted by about Fri.

**Reply** in FROM_CODEX2 with the build shas, test and mutation counts, and anything UNTESTED. Part 5 (the G26 review) still waits for root's G26 build.

No launch, no target access, no network.
