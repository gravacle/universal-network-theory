# 0822 — Claude3: a critical-path wall-clock audit, S3 → S11. Find every place where more compute, earlier work or removed latency shortens the time to the result

From: **Claude2** (root). UTC 2026-10-21T12:00:23Z (`date -u`). **Priority:** after your 0813 item 1 (the verdict-day sheet dry check), ahead of the 0813 verifies. The cw8 build review (0821, when Codex3 posts it) slots in after this.

**The principal (verbatim):**
- "The key thing we're talking about is the quickest path to finishing even if there is more total processing."
- "4-15 hours is a lot."
- "We should explore any other areas like that if we can save total time to a result."

Root's rule (V006 A258): the objective is wall clock to the PROVISIONAL score (S10), then to the score of record (S11). Extra compute is fine. Physics, custody and blinding are unchanged, and any lever that changes a value or the engine's path is a FAIL.

**Already in flight (do not redo these):**
- **L1:** CP-1 certification of the 3 W3-minus points, plus a hedge on all 24 conditional points (A257, A258).
- **L2:** the concurrent Jacobian and the earliest start beside HEADLINE11 (Codex1 0816/0820).
- **W1 launch:** pre-staged to go at drive mount (A256).
- **cw8 Phase-1 path:** Codex3 0821 build (A259).
- **Ruled out:** a campaign that migrates between volumes (A256).

**Audit.** Use `plan/STEPS.md`, V006 (A184-A259, read as needed), the verdict-day sheet (`verdict_day_sheet_cx1/` `f2a5eec4`), README_CAMPAIGN_CERT C2V001/C2V004, RUNBOOK_V002_C2V007 and the P112 kit. For each step S3 → S11, list:
- **(a)** every serial dependency and whether it is inherent;
- **(b)** every latency: a lane review, a root act, a fixed wait or poll, an operator step at night;
- **(c)** every self-imposed throttle: `taskpolicy -b`, max_active, admission holds, single-file ordering;
- **(d)** every compute-for-time trade: speculative or early runs, more concurrency.

Give each one an estimated wall saving (E/U), its cost, the risk, and whether it needs a build. Cite file:line.

**Candidates root already sees. Verify or refute each one:**
1. **CP-1 between waves.** The pinned list runner hard-codes `taskpolicy -b` in the worker argv (`cp1_points_runner_c2v001.py` L60), which keeps workers on the 12 E-cores. The design map gives about 2.25 h at background priority against about 1.1 h at normal priority (CAMPAIGN_CERT_DESIGN_MAP L126, L141). Every march0+ wave pays that on the critical path. Is a one-flag QoS successor worth building, given the waves to u_A? If so, scope it as a Claude3 build with a Codex1 review.
2. **EPS review latency per wave** (Codex3 standing signer, A202). Can it be overlapped or pre-requested? A review is a quality gate, so do not remove it.
3. **The verdict-day sequence.** Are any steps parallelizable? Which ones wait on a lane at about 3 am CDT? Can S0 launch before HEADLINE11's PRELAUNCH/binder chain?
4. **S10 replay passes** (PASS_ONE, PASS_K) and the freeze. How long do they take? Can they run per call as each call finishes, instead of after all of them?
5. **Phase 2 (S11).** Which Phase-2 work could start during Phase 1, once its inputs exist?
6. **The seal (S7).** Does it become critical if S9 moves earlier? Claude4's render is after Fri 19:00Z.

**Output:** `claude_artifacts/critical_path_audit_c3/AUDIT_C3V001.md`, ranked by expected saving. Read-only: no launches, no run trees, no step-2 outputs, no NGC3198 data.
