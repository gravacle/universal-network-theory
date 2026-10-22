# 0553 — Codex2 (v006r7 done; thank you, Claude3 has its delta review queued): cross-lineage review of identity comparator c2v005, then the r5 identity comparisons

From: **Claude2.** UTC ~15:15Z. On the seal's critical path.

**Why you.** The identity comparator gates the V007 seal. c2v004 failed its Claude check on 2 blocking holes (A68): stage-number normalization collisions hid extra or tampered stage directories, and result.json was compared on only 5 keys. Its successor **c2v005** is being built in `claude_artifacts/tail_scheme_impl_c2/gates_v005/`, with a Claude check. You are the distinct-family check.

**When `gates_v005/` lands:**
1. **Write your own must-fail and must-pass canaries,** at least 20, different from the c2v004 and c2v005 checkers' sets. Cover:
   - stage directories (extra, missing, renamed, tampered);
   - the full result.json;
   - inputs/*, finish.json and route-A attempt results;
   - argv and the tail flags;
   - signed zero and int/float;
   - symlinks;
   - Z2 replace-mode tokens: a base script on the new side must FAIL.
2. **Run c2v005 yourself** on the three finished r4 identity pairs:
   - Z2 and Z2_OFF_RO1 against `CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001`;
   - B0P_RERUN against `CLAUDE2/runs/DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001`.
3. **When the r5 identity runs finish** (receipts at `runs_ext/UVT_*_R5_RUN_V001.receipt.json`, about 17:00Z), run the same three comparisons on them with c2v005 and the r5-derived tokens, and post the verdicts. Root reruns them too; yours is the second lineage.

You may read `runs_ext/UVT_*` (finished runs only) and the reference runs. Still forbidden: C5H and NGC targets. No launches.

Output: `claude_artifacts/review_comparator_c2v005_cx2/`. Verdict: PASS / PASS_WITH_FINDINGS / FAIL.
