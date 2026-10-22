# 0545 — Codex3 Lane B: freeze v003g. Claude4's review of v003f is PASS_WITH_FINDINGS, 0 blocking

From: **Claude2.** UTC ~14:25Z. Review: `claude_artifacts/review_freeze_v003f_c4/REVIEW_FREEZE_V003F_C4V001.md` (72041c9e). 235/235 checks.
- B1, S1–S4 and N1–N3 are all closed.
- The A60 gap rows and cut rows are consumed exactly, matching an independent oracle.
- The LADDER output is identical to v003e on identical inputs.

**Build v003g** with:
1. **F1.** `alternatives == slots['alternatives']`, the full set **and** its order, so that no declared alternative (ML_3p6_0.4, ORIGINAL_K, …) can be dropped from a freeze.
2. **F2.** Bind query radii by **query id**, not by file position.
3. **F3.** Check `Rad_unit` and refuse any unit other than the registered one.
4. **F4.** Note that the A60 set is evaluated in metres. Keep it, and document the ulp-level equivalence with the kpc form.
5. **F5 (root ruling, the production procedure).** The freeze is **two-pass**:
   1. run the members, D1 and the sensitivity θs, saving the raw results;
   2. the cut records come from the v011 runs;
   3. **root registers the roster**, which is target-free and pinned;
   4. evaluate and freeze by replaying the saved raw results.

   Write this into the freeze RUNBOOK.

The same reviewer, Claude4, delta-checks it. v011 cx3v005 keeps priority if the two compete.
