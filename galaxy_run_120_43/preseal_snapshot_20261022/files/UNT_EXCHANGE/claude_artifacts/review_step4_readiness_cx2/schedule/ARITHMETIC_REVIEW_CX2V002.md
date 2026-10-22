# Step-4 schedule arithmetic review — CX2 V002

Literal date -u: **Sun Oct 18 20:10:21 UTC 2026**. Test completed 2026-10-18T20:10:11.175552Z. Policy: **nice unavailable (sandbox); 0514 waiver**.

**PASS_WITH_FINDINGS for the bounded schedule arithmetic/source-model slice.** TESTED: 90/90 independent checks pass; all 11 input byte pins match before and after the calculation. One SHOULD_FIX endpoint defect remains. This is not a launch-readiness or empirical performance verdict.

The own harness `recompute_schedule_cx2v001.py` reconstructs the declared phase costs and a 30-second fluid processor-sharing model with 60-second admission polls. It imports no reviewed scheduler, producer, driver, or scientific module. Inputs are named static sources and saved summaries only; no saved run trees, run metadata, target velocities, network, or scientific launch was accessed. The final-named order/docs/manifest were copied into immutable owned `SNAPSHOT_200805_*` files because earlier versions changed in place. Previous partial-review files remain untouched.

## Independently reproduced projections

E means I=7/P=3; U_ADJ means I=32/P=6. These are conditional scenarios, not demonstrated bounds on real runtime.

| Scenario | E hours | U_ADJ hours |
|---|---:|---:|
| Four DIII tail-OFF calls, direct ramp | 4.61 | 7.77 |
| Ten headline tail-ON calls, direct ramp | 7.23 | 15.55 |
| Eighteen sensitivity calls, direct ramp | 11.16 | 22.64 |
| Two post-S1 calls | 5.42 | 8.97 |
| 120-call campaign, max_concurrent=1, budget=17 | 624.00 | 1051.83 |
| 120-call campaign, max_concurrent=6, budget=17 | 209.75 | 356.49 |
| Published mixed nine-headline/eighteen-sensitivity queue | 15.76 | 31.58 |
| Own additional ten-headline/eighteen-sensitivity queue | 16.09 | 33.39 |

The 120-call model uses 21 waves: one seed, nineteen six-call waves, and one five-call wave. This assumes that adaptive progression actually supplies those wave sizes. The 90 checks include solo-call totals, the selected batches and campaign metrics, mixed-queue totals/headline completion, critical-path sums, process-hour totals, and the endpoint witness. They do not exhaust every optional policy/core-count row in the supplied simulator record.

The headline + max_concurrent=6 campaign + post-S1 sum is 222.4 h E / 381.0 h U_ADJ. Sequential sensitivity adds 11.16/22.64 h, giving 233.6/403.7 h after rounding. Process-hours are 1339/2745 for 150 tail-ON and four tail-OFF calls. DIII is modeled before T0; root review, certificate production, failure handling and other waits are excluded.

## Finding S-1 — SHOULD_FIX: exact cap endpoint is not counted

`schedule_sim_c4v002.py:203` counts starts using `start - wave_start > 172800.0`. The actual `campaign_c2v005.py:200` permits admission only while elapsed time is strictly `< cap`. Thus a start exactly at 48 h is inadmissible but is omitted from the simulator's late-start count. The own pure witness [0, 16 h, 32 h, 48 h] gives metric count 0 and inadmissible count 1. Use `>=` for the reported inadmissible-start metric; preserving running calls beyond the admission cap is a separate behavior.

No checked published start reaches this endpoint. The single-call upper scenario can have a 52.59 h six-call wave while every call starts before 48 h; that is consistent with an admission cap rather than a forced termination cap. The endpoint issue therefore does not change the reproduced totals above.

## Operational interpretation and limits

- Budget 17 with weight 8 through route A and 2 afterward permits at most two simultaneous route-A calls, even when max_concurrent is six. It is not a six-way route-A launch. The proposed budgets 24/48 need a reviewed successor of the hard-coded budget validator; they are not available current settings.
- The direct-ramp 25% free-memory rule checks current free memory before admission. It does not reserve the next call's memory. The reproduced sensitivity/mixed minima are 14.296875% after admission; this is consistent with the modeled rule and is not evidence of a guaranteed 25% floor.
- The published mixed queue explicitly uses nine headline calls. It must not be substituted for the default ten-headline schedule. The own ten-call comparison is labeled above.
- The adjusted solo upper tail-ON estimate is about 8.75 h, already beyond the shipped eight-hour per-call cap. The supplied readiness documents identify this cap problem. No cap change or real runtime guarantee is certified here.
- CPU sharing uses a homogeneous fluid approximation (including 1.5 busy-CPU equivalents during route B), fixed cost/RSS assumptions, and 30-second time quantization. TESTED arithmetic does not validate those empirical assumptions. Actual iteration counts, resource demand, contention, adaptive scheduling, process accounting, cancellation and guarded admission are UNTESTED.

The reviewed snapshot still contains the raw campaign fallback in ROOT_ITEMS R-B6. Dispatch 0620 explicitly removes it; this review does not authorize it. The corrected guarded launcher and its readiness review remain separate, parent-owned work. Neither these arithmetic results nor a matching schedule authorizes a launch.

V002 corrects only the root-item label from R-B5 to R-B6; V001 remains unchanged.

## Byte pins

Every cited file is pinned below. The owned snapshots have the same bytes as the corresponding reviewed input version. The manifest is a pinned document only; its referenced files were not traversed blindly.

| File | SHA-256 from bytes |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/LAUNCH_ORDER_C4V001.json` | `2b4dd6a0bdb0f541793a43f6b2091b586ffbed45532999b99103ae66b01bd6ab` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/LAUNCH_ORDER_C4V001.md` | `c276c4d9e3c5552d26ae600eac01d97489aaf766daf2abf5e6fe69185a795938` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V001.md` | `5d83f0672f9b45fdae31772b2c29c5f786159aa960f0855cc1e258291353ee36` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/HASHES.txt` | `be7f811dc5381bbf3c4ba217c1d6f2ff0a111426454a00589dc07ad4b0b2186c` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/tools/schedule_sim_c4v002.py` | `94a0aa32797a3be359905e9b12f1a941342859356687538008c602ea8ef4c6a6` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/work/SCHEDULE_SIM_C4V002.json` | `2723042e704a04ae7dd90c7aeec848e210f2895bbeb6985823b11a864f22029b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json` | `3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/results/projection_c2v001.json` | `cffa3150a2aac120bad1fdb045a93f645b938f76f22c3e8ff0bce56f387eaad2` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/campaign_c2v005.py` | `d35d5d4a62e6e5b632eb10c59bf4c82c2b1d744f6ceba609399c02baa5ecfeb2` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json` | `721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0620_2026-10-18_claude4_codex1_step4_no_unguarded_fallback.md` | `037a2a61998d511e398f10f7e8c9203597a48e768bbf09d148ae209d94658e99` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/recompute_schedule_cx2v001.py` | `d48fd0fc810492ea73bc5def797e9907f51d651161517cc54950a4628d636f25` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/ARITHMETIC_RESULTS_CX2V001.json` | `dc37f73cde412c5fcc236893912c3bd67f5b1f6cb89e32c9e1fc5b08fbc190ed` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/SNAPSHOT_200805_LAUNCH_ORDER_C4V001.json` | `2b4dd6a0bdb0f541793a43f6b2091b586ffbed45532999b99103ae66b01bd6ab` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/SNAPSHOT_200805_LAUNCH_ORDER_C4V001.md` | `c276c4d9e3c5552d26ae600eac01d97489aaf766daf2abf5e6fe69185a795938` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/SNAPSHOT_200805_ROOT_ITEMS_FINAL_C4V001.md` | `5d83f0672f9b45fdae31772b2c29c5f786159aa960f0855cc1e258291353ee36` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/SNAPSHOT_200805_HASHES.txt` | `be7f811dc5381bbf3c4ba217c1d6f2ff0a111426454a00589dc07ad4b0b2186c` |
