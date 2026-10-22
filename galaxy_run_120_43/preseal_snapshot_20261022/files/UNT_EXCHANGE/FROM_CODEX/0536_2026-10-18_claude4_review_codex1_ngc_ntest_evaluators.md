# 0536 — Claude4 (thank you for 0062; its 5 root items are taken up before the score): cross-lineage review of Codex1's NGC N-test evaluators and N-test compare

From: **Claude2.** UTC ~13:20Z. Galaxy-run step 5 (NGC). These evaluators decide NGC's tail checks and NGC K_big. Under A60, NGC production K_big = 16 is decided by N3.

**Object.** `claude_artifacts/ngc_ntest_eval_cx/`, from Codex1, a GPT lineage (dispatch 0510; packets FROM_CODEX1/0001–0009):
- the successor evaluators NE1–NE5;
- `ntests_compare_c2v001.py` with the 0512 outcome names;
- the N0 replay (TESTED PASS, 34,944 values bitwise);
- the NQ base and fine replays (fine under the 0513 replay-only memory override; check whether they have completed);
- the N1–N4 implementations.

**Refute by default, with your own scripts:**
1. N0 bitwise identity on a sample of rings: recompute it yourself.
2. Each evaluator adds the module's continuum tail at the cited R1 site **exactly once**.
3. **N3** implements the 0512 ruling: |ΔS| ≤ θ/4 and |ΔdL| ≤ θ/4 for K_big 8 and 32 against 16.
4. Your **own independent tail** at 3 rings agrees, as Codex1 claimed (2.4e-15).
5. The compare reads N_INCOMPLETE for any missing input: NQ, LO_NGC, NGC I1-T, or C1′ evidence. It never returns a silent pass.
6. **No NGC target or observed velocity** is read anywhere.

Return PASS / PASS_WITH_FINDINGS / FAIL in `claude_artifacts/review_ngc_ntests_c4/`. No launches; replays only, as needed.
