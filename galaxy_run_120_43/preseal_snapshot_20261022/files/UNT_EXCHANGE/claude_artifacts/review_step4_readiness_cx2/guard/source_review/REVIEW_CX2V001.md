# Step 4 launch-order source guard review — FAIL for fallback use

Date from `date -u`: **Sun Oct 18 20:04:06 UTC 2026**.

**Scope:** staged publication, not a frozen final package. The parent initially supplied order `056defdfec427bc11625b876f9f1ce987e83bd6f7e991ccd82643c837bc7812a` and root-items `218b5574428a96c8f759e6d379306937866362a229b51b42d61aaeeee75d3d74`. Those names changed during publication. This review preserves and evaluates the subsequently observed order `facda76c008d2bc5ff29588fc14e7424803815753b6c3616895b535bcda781cd` and root-items `3d9f70f3b457c2b71436a41c9f73ef7dd2104d61290e2f1ef60cee84b577c729`. Only the latter pair was unchanged during the bounded harness. The final packet/helper remains outside this review.

**52/52 checks passed; one fallback-use blocker and one documentation correction.** Passing checks confirm the findings, not launch readiness.

**CX2-S4-GUARD-B1, BLOCKING for the recommended fallback.** Latest `ramp.fallback_zero_build` and R-B6 still recommend invoking the raw `campaign_c2v005` CLI if the new launcher is not reviewed. Source inspection follows `main → run_campaign → subprocess.Popen` (campaign source line 224). Its pre-process checks cover caller-supplied monitor/driver/spec byte hashes and resource limits. They do not check sealed V007 ADOPT_TAIL bytes, a published STEP4 admission, a pinned per-spec PRELAUNCH record, the r5 allowlist, per-point certificates, or sensitivity eligibility. The ordinary monitor also lacks these checks. It is therefore not a guard-equivalent fallback.

The real orchestrator path is different: `Orchestrator.run` first requires `ctx.gates_ok()`, and `make_plan` calls `self.ctx.prelaunch_check` for every planned spec. Raw campaign CLI bypasses these callers. An earlier manual check cannot establish that the same admitted bytes still govern process creation. Remove/disable the fallback for Step4 or provide a separately reviewed wrapper retaining the mandatory checks. No CLI or subprocess was executed to establish this source-level finding, and no unauthorized launch is alleged.

**CX2-S4-GUARD-S1, SHOULD_FIX.** R-C8 prose still quotes cache prefixes `4555ce79 → b3839787`. The exact saved probe and launch-order JSON agree on `4f0521aafcf281e88586180737ae28370bde4afd6e6452ebbd2af7e95f9c1877 → b370470ac66256cc27f64b280c88a4bafc9058155b86e6c9bd95c6f2e65fc14c`. Correct that citation in a successor. The technical conclusion survives this documentation drift.

Other conclusions:

- **Registry growth is substantiated.** Source shows the full tail_readiness block in the wrapper cache identity, exact point-registry lookup at prelaunch, prelaunch invoked for every wave call, and C4-2 refusing committed plans with a changed cache id. TESTED independently: the exact pure hashing definitions and cache-id expression, with owned in-memory registry pins, change identity when a registry pin changes; the exact C4-2 method refuses a mismatched owned committed-wave fixture. The Context and supplied registry probe were never executed. Its saved result is corroborating reported evidence, not a rerun. An append-only ledger remains a recommended future design, not implemented authority.
- **A96/r5:** the latest documents correctly carry r5 as the production driver and defer unfinished r6. The current wrapper independently rejects a driver SHA other than r5. A new direct guard must enforce this itself; raw campaign CLI merely accepts a supplied matching driver hash. The DIII reference side explicitly remains v009-GEO in the proposed plan, so the broad phrase “every step-4 call on r5” must be read with that declared reference-side exception; no driver substitution is authorized here.
- **Necessary seal dependencies are retained:** tail-ON starts after sealed ADOPT_TAIL; C1 contains adopted block/pins; the reviewed seal tuple includes verdict hash; the allowlist is still empty in shipped policy; C4-6/capability/deciding/uncertainty/certificate gates remain campaign prerequisites. PRELAUNCH alone is not the numerics-verdict gate. The planned STEP4 admission is supposed to supply the missing direct-path seal binding.
- **Pre-seal DIII is a recommendation needing a ruling.** R-D5/R-D14 expressly call for a tail-OFF exception. The proposed P2 schedule is not an already-authorized exception or a dispatch to this lane. No recommended owner's work was implemented.

Only source text, snapshots and one saved synthetic probe result were read. No production references in those documents were followed. Guards protected open/list/stat/lstat/readlink before pure-AST execution; zero blocked attempts. No Context construction, supplied script import, launch helper, monitor, driver, producer, or supplied suite ran. Actual new launcher process-boundary behavior and final-package readiness remain **UNTESTED**.

The first harness selected the first method named `run` in the parent AST, which was not `Orchestrator.run`; its one failed reviewer assertion is preserved. Successor v002 selects the class explicitly and passes all 52 checks. Final totals use v002 only.

Reproduction:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/source_review/probe_source_guard_cx2v002.py` — SHA256 `e7c0286f5ca57b4f819a14cbc7c4c88cf6ef89b29f1f3df0724f914f9204646a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/source_review/RESULTS_CX2V002.json` — SHA256 `fef1692d4ca633c06daba03b258db2d9eb2b4a9e30f3faa81e7ba15e98c6e55e`.
- Owned observed document snapshots are preserved; all owned files are byte-pinned in `HASHES_CX2V001.txt`.

Input byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/LAUNCH_ORDER_C4V001.json` — SHA256 `facda76c008d2bc5ff29588fc14e7424803815753b6c3616895b535bcda781cd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V001.md` — SHA256 `3d9f70f3b457c2b71436a41c9f73ef7dd2104d61290e2f1ef60cee84b577c729`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/work/registry_probe_v002/REGISTRY_GROWTH_PROBE_C4V002.json` — SHA256 `4cfc628366c0931bc63dd94f171772e602adb384c6d253440b3f29dc3a74c353`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py` — SHA256 `24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py` — SHA256 `a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` — SHA256 `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/campaign_c2v005.py` — SHA256 `d35d5d4a62e6e5b632eb10c59bf4c82c2b1d744f6ceba609399c02baa5ecfeb2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py` — SHA256 `ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/adoption_policy_cx2v006r7.py` — SHA256 `7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/source_snapshots/V005_ADDENDUM_snapshot_1952Z.md` — SHA256 `991cc242e30eeea5118058e0f60862f7f50f1cb2cf434a85d92f4055413848c8`.
