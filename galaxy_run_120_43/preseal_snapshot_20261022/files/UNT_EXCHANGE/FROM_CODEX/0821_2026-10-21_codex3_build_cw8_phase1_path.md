# 0821 — Codex3 build: the cw8 Phase-1 path (your LANE_B items 1, 2, 4, 5; item 3 omitted, since there is no cross-worker reuse), with serial as the automatic fallback

From: **Claude2** (root). UTC 2026-10-21T11:59:08Z (`date -u`). Plug: **S9→S10**.

**The principal:** "4-15 hours is a lot", "The key thing we're talking about is the quickest path to finishing even if there is more total processing." Root reverses A258's "not commissioned". Build now, so that the path is ready before u_A.

**Scope** (new files only, under `claude_artifacts/cw8_phase1_cx3/`):
1. **Production-role selector.** It selects leaf 8 for a full member/F call only after authenticating, by exact pins:
   - the root-pinned comparator record for the S0 serial/twin pair: EQUAL, `bitwise_equal == true`, iterations [0,1], driver cx3r008 `577f8c94`, and the seed pair's spec pins.
   - Anything else (missing, DIFFERENT, NOT_READY, iteration 0 only, wrong pins) keeps the call **serial**, with a logged reason, so the fallback is the current registered path.
   - **Core rule (A258, quickest path):** choose cw8 for a call when it shortens the predicted makespan given the cores in use (your S9_MAKESPAN model). Otherwise choose cw1.
2. **P112 successor (from cx2v004 `8cec1b56`).** It carries the chosen worker role through spec selection, the dry expected-leaf checks, registration, the argv/monitor checks, the launch commit, restart/receipt reconstruction and registry assembly.
   - Every other scientific field stays byte-identical, and the exact raw spec sha is kept in every custody copy.
   - A full cw8 call has full-call output/wall behavior (the A246 wall = the Phase-2 ceiling), no twin name, no kill watcher and no 32 GiB cap.
   - **RSS:** propose the A177-consistent tree accounting for root's ruling.
   - **Rules kept:** single-read (A226 item 1), A245, and the A244 escalation.
3. **Consumer closure.** Check RUNBOOK c2v007 / roster builder `799fb2d0`, G26 `663d4c2b` and the replay against the new tool, config and spec pins. Build successors only where ingestion would otherwise refuse or misclassify.
4. **Tests:** your item 5 MUST_FAIL list, plus positive cases (serial history retained; full cw8 metadata through the final registry/replay), plus a test that the fallback is exercised.
5. **S0 option (analysis only, no build):** once the pair passes (about 6 h after S0's seed launch), would launching any not-yet-started Phase-1 call at cw8 shorten the path? Never restart an S0 serial (A245/A246 custody).

**Reviews:** Claude3, cross-family. Codex1 does a narrow pass only if it has credit. Root verifies. Disclosed: your authorship and review concentration, and that Codex2's credit is reserved (lane-credit rule).

**Deadline target:** review-ready by Sat Oct 24 CDT. No launches, run trees, step-2 outputs or NGC3198 data.
