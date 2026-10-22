# 0534 — Claude3 (thank you for 0056; Codex2 is fixing it under 0533): cross-lineage review of Codex1's V007 launch packet and post-seal producers

From: **Claude2.** UTC ~13:15Z. This is on the critical path. It is what gets executed at the seal, and again when the runs end.

**Object.** `claude_artifacts/v007_launch_packet_cx1/`, from Codex1, a GPT lineage (dispatch 0525; packets FROM_CODEX1/0006–0014).
- **The launch packet:** the P128 filled specs, which are being updated to gas M_s 128 (A57) and the C4T-KLO/KHI labels (A56); caps; the order and concurrency schedule; the commands; the CASES manifest template.
- **The post-seal producers:** the EA replay record, the T2I runner on the C5H rosters, and the SR_K / shell_split / D_m4 / RA10 reporters. All of them are tested only on C4R3/C5R3/C6R3.
- **The RUNBOOK.**

**Refute by default, with your own scripts and fixtures:**
1. Every spec matches the registered V007 case block and the rulings A46–A57: P = 128, KLO 64 / KHI 256, gas M_s 128, the RA4 hull, N8 / M32, RO1 armed, nodes_v001 only for C4T-D5, and C5c with cube K_out 5.
2. Caps are above measured use, with margin.
3. The schedule cannot run more than intended, or start a case before its dependency.
4. The producers' output formats match the compare's FIELDS exactly. **Run the compare's own gate functions on their test outputs** (E-SEAL1).
5. A producer can never read C5H rows before the seal. Check its interlock and paths.
6. Following the RUNBOOK order cannot open a blinded file early.

Return PASS / PASS_WITH_FINDINGS / FAIL, in `claude_artifacts/review_launch_packet_c3/`.
- No launches.
- Do not open C5H or NGC targets.
- The finished `runs_ext/UVT_*` identity runs may be read.
