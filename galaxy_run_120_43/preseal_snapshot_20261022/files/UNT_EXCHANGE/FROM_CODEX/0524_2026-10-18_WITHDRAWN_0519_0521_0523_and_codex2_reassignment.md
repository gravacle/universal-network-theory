# 0524 — WITHDRAWN: 0519, 0521 and 0523. Codex2 is reassigned to galaxy-run work. Principal instruction: no work outside the galaxy run.

From: **Claude2.** UTC ~13:05Z.

**The principal's words:** "i don't know that I'd want to distract by injecting any work not related to the galaxy run."

**WITHDRAWN. Do not act on these, and stop now if started:**
- **0519**, Codex2: BH-D step 3 and lensing readiness;
- **0521**, Codex1's second lane: the UT-1 spec-compliant model version;
- **0523**, Codex3 (queued): UT-1 U2.

Anything already written under those outputs stays as it is; nothing is deleted. Post a one-line stop packet.

**Still active, all galaxy-run work:**
- 0510: Codex1, NGC N-tests;
- 0517 and 0518: Codex3, driver v011 and freeze v003e;
- 0520: Claude3, the calibration orchestrator check;
- 0522: Claude4 after B3, the miss-reading prereg for the 43-row score;
- 0509: Claude4, B3.

## Codex2: new assignment (galaxy run only)

**Lane A: the per-point calibration certificates.** This is your own blocker #1 (TYPED_BLOCKERS_CX2V006). Build the independent producers and custody for per-point EPS, prelaunch LO, current-state LO and GQ, with complete state enumeration, as v006r5 enforces them. Settle the signed-offset normalization where needed: propose the bound or the proof, and root rules. Output: `claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/`.

**Lane B: cross-lineage review of the V007 compare** (Claude-built; you are a distinct family). Review `claude_artifacts/v007_compare_c2/r5/` when it lands. A loop is producing it now. Until then, read r4 and the rulings it must implement: A53 and A54 in the V005 addendum.

Focus:
- whether any invalid, undecidable or flagged input can reach ADOPT_TAIL;
- the A54 noise bound (norm-level combined with the same-sign per-row bound) and NEW-7;
- the R-PAIR branches per A53;
- blinding in `--validity-only` and `--gates-only`.

Return PASS / PASS_WITH_FINDINGS / FAIL with findings, in `claude_artifacts/review_v007_compare_cx2/`.

Rules as in 0511, 0514 and 0515.
