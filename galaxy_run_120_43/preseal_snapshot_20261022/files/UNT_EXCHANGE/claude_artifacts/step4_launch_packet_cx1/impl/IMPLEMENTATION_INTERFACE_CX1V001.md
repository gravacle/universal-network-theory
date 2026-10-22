# Step-4 guarded direct-run interface, Codex1 implementation V001

UTC from `date -u`: Sun Oct 18 20:47:19 UTC 2026

**TESTED:** 40/40 synthetic admission/process-seam checks, 21/21 additional binder/path/driver/lock probes, 43/43 direct-adapter and actual Claude4 structural-spec checks. The 43 include all 29 actual tail-ON and four tail-OFF template rows. Scientific process count: zero. **UNTESTED:** actual production adoption/certificates/sensitivity and launch. Template compatibility does not grant admission.

Only the four implementation files listed below are the candidate supported set. Earlier v001–v004 guards/launchers and v001–v003 binders remain immutable historical candidates. The full Context-constructor volume/diskutil trap in v004 is replaced by the explicit direct-run adapter in v005; no subprocess exception was added to preflight.

## Runtime authority and root input contract

The launcher requires independent publication of `UNT_STEP4_ADMISSION_PATH` and `UNT_STEP4_ADMISSION_SHA256`. These bind the admission bytes; they are not a cryptographic identity. Merely possessing a file containing Claude2's name does not establish authorization. Root alone publishes and executes.

Admission schema `UNT_STEP4_ADMISSION_CX1V001`, `status: ROOT_AUTHORIZED`, `authority: {identity: Claude2, role: coordinator_and_single_scientific_launch_owner}`. Required fields:

- `plan`: exact final-plan pin; `sources`: absolute source-path to byte-sha mapping for the complete preflight closure and launcher/guard/monitor/drivers; `source_review`: pinned `UNT_STEP4_SOURCE_REVIEW_CX1V001` with `status: TESTED`, `verdict: PASS`, non-Codex1 reviewer, empty `blocking_findings`, and exact `approved_sources` mapping.
- `v007`: pins `seal`, `verdict`, `prereg`, `compare`, `addendum`, `case_block`. The guard checks root seal, r5, prereg/case-block, report script SHA, test_mode false, tests_read true, ADOPT_TAIL, the immutable reviewed policy's exact seal tuple and actual `check_numerics` replay.
- `config`: final C1 pin; `context_module`: reviewed native orchestrator module pin; `adoption_policy`: reviewed immutable registered-tuple successor; `direct_context`: this packet's direct-preflight adapter pin. Current upstream empty tuple, null certificate registry/policy or unavailable per-D comparator remains a refusal. No auto-registration occurs.
- `route_a_admission`: identical to plan; `case_order`: exact case list; `caps`: case to exact positive integer `wall_cap_s`, `rss_cap_bytes`, `output_cap_bytes`; `calls`: case to exactly `{spec, driver, prelaunch}` pins.
- `core_priority`: exactly `{normal_qos_required:true, step2_route_a_inactive:true, campaign_inactive:true, background_noncritical_lanes:true, sleep_assertion_required:true}`. This root attestation supplies external campaign/step-2 occupancy; the packet's flock only excludes other instances of this step-4 launcher. It does not retrofit unrelated launchers.
- DIII additionally needs `tail_off_policy`: root-authorized `UNT_STEP4_DIII_POLICY_CX1V001`, TESTED/PASS, `post_adoption_only:true`, cases binding exact spec/driver pairs. Only the native omitted `uv_tail` schema is eligible. Certificate applicability is explicitly recorded as reviewed tail-OFF identity, not silently skipped by null registry. DIII remains post-adoption under 0620.

All fields above are root-reviewed inputs, not populated automatically from Claude4's provisional files. Every source the native preflight reads under Research must be in `sources`; existing .pyc there is rejected. r5's normalization includes its pinned tail library source. The source review must cover that full closure. The synthetic tests use explicitly synthetic source adapters; their files and purported review markers are never production authority.

## Plan and PRELAUNCH

Final plan schema `UNT_STEP4_LAUNCH_PLAN_CX1V001`, `binding_status: ROOT_BOUND`, batch HEADLINE/DIII/SENS_LO/SENS_HI/POST_S1; launcher, guard and monitor pins; launcher_log; nonempty calls. Each call binds case, family, tail_on, driver_role, distance_Mpc, spec pin, `spec_status: ROOT_FINAL`, `pending: []`, PRELAUNCH pin, driver pin, three positive integer caps, outdir/receipt/monitor_log. Main/root callers must create output parent directories beforehand; no reuse/retry is admitted. Outputs are canonicalized and alias/nested conflicts rejected.

Driver is exact r5 b5cc62af for tail-ON and new DIII; v009-GEO 237ef3d4 is eligible only for tail-OFF DECIDING_III with `driver_role: REFERENCE_V009GEO`. The fixed monitor is ba031c23. No future r6 is silently substituted.

The PRELAUNCH file is exactly the deterministic return of `native_preflight(admission, call)`, schema `UNT_STEP4_PRELAUNCH_CX1V001`, binding spec/driver/C1/adoption-verdict and the actual native certificate_policy_gate, certificate_check(prelaunch), sensitivity_gate and normalized-spec digest. Root may obtain it by a controlled in-process, read-only call after final inputs exist; it must be published under a new name. The launcher's independent repeat must equal those bytes semantically. A PASS label is insufficient.

The explicit `DirectPreflightContext` reconstructs the native coordinate template with adopted numerics, validates target-free anchor registration, C1 schema, non-synthetic mode, r5, template identity, inclination, A7 and native normalization. It preserves the native prelaunch/certificate/sensitivity methods unchanged. Its state is exactly cfg/numerics/D/norm_base. It does not construct campaign observations, work-volume/cache/engine state or future deciding results. It is not a substitute for campaign Context admission, and this launcher has no campaign execution path.

## Ramp and process boundary

Root-approved max_active must be integer 1..6; Claude4's proposal is 3. Free memory must be >=25%, including the first call. The previous call's first complete route-A iteration gates every later call, one start per 60-second poll. Unknown memory waits. Malformed complete progress, missing/systemic receipts, caps/setup refusal and an ended predecessor with no first iteration halt new starts. Ordinary scientific failure is retained; no automatic retry. Existing monitors are not killed by later admission refusal.

Every worker/monitor creation follows byte/admission/native revalidation. Worker and monitors are wrapped in taskpolicy -B for normal QoS, Python -I -B, single-thread BLAS; root command uses nice -n10. The worker starts caffeinate -i -w ownpid before any scientific monitor and admits no further monitors if it dies. Persistent empty flock inode is never deleted or rewritten. All test process creation is mocked; actual macOS QoS/assertion behavior is UNTESTED.

## Binder

`step4_bind_cx1v004.py --final-plan INPUT --admission-candidate INPUT --plan-out NEW --admission-out NEW --command-out NEW` validates final-plan and native checks using candidate admission with `plan:null`; serializes before any write; exclusive-creates three packet-local outputs. The output admission embeds the actual new plan pin. The command does not export/self-authenticate the admission digest. Root must independently review/publish it. Interrupted publication leaves any created prefix intact; choose new names, never overwrite.

## Test scope and preserved failures

Main/extra suites use synthetic adoption/policy/context modules and narrowly mocked processes. The direct-adapter suite uses actual Claude4 specs, actual r5 normalization and unmodified AST-extracted native parent prelaunch/A7/diff functions; anchor registration is stubbed in that suite. Actual certificate scientific proofs and post-adoption report tuples are pending, so no production preflight PASS is claimed. Test v001 syntax failure, synthetic v002 incomplete source closure and direct v001 missing tail-library source closure are preserved; successors corrected fixture/source inventory, not scientific expectations.

## Byte pins

- `11a31edd2cbbb0adb6738360bacecc6363b5cada4f91c0cd976276fd72c7e2d8`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v005.py`
- `f9e4888dc8fc5c638581730651a7e19f0945fd7fa89a7f32391298f20dd0a66b`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_launcher_cx1v005.py`
- `7f7add8545f95f4a3f0881dada86259911e8f43b0aa2073abeb186dff29613cd`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_bind_cx1v004.py`
- `eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py`
- `2578581e6b777f2fda4d1173452e855c61d4323b9c59bb68b0263a73270a49f5`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_step4_cx1v004.py`
- `35db95303a3b55f6818c17d78641df51e22e71e8297b352e20e21d447d07ce91`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_step4_extra_cx1v002.py`
- `18b674cf3f6d1e3cc8f418ad87632c8d5872c27f79d8b58d6b72dd389c8919cc`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_direct_adapter_cx1v002.py`
- `39083f66537dffa050fe5ee458e858148e06e5b42daa5bb5055d8046f6be3e2e`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/SYNTH_V004/RESULTS.json`
- `150e4bb951b676c045674347af706cb37d48715635a02b5a10559cb85a096406`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/EXTRA_V002/RESULTS.json`
- `cb5e9487cdb5bece42088c07ad3fcc224f86ccd0ad38776230b1e6dbc535bfe5`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/DIRECT_V002/RESULTS.json`
