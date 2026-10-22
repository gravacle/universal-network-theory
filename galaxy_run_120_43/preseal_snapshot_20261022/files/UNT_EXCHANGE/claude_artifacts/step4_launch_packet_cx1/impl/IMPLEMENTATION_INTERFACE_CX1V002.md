# Step-4 guarded direct-run interface, Codex1 implementation V002 (0625 successor)

UTC from `date -u`: Sun Oct 18 20:54:46 UTC 2026

**TESTED:** 157/157 checks: 40/40 synthetic admission/process-seam, 21/21 additional binder/path/driver/lock, 43/43 direct-adapter and actual Claude4 structural-spec, and 53/53 direct0625 source/loader/lifetime/ordinary-OS-helper controls. The 43 include all 29 actual tail-ON and four tail-OFF template rows. Scientific process count: zero. **UNTESTED:** actual production adoption/certificates/sensitivity and launch. Template compatibility does not grant admission.

Only the four implementation files listed below are the candidate supported set. Earlier guard through v005, launcher through v006 and binder through v004 remain immutable historical candidates. The full Context-constructor volume/diskutil trap in v004 is replaced by the explicit direct-run adapter inherited from v005; no subprocess exception was added to preflight.

## Runtime authority and root input contract

The launcher requires independent publication of `UNT_STEP4_ADMISSION_PATH` and `UNT_STEP4_ADMISSION_SHA256`. These bind the admission bytes; they are not a cryptographic identity. Merely possessing a file containing Claude2's name does not establish authorization. Root alone publishes and executes.

Admission schema `UNT_STEP4_ADMISSION_CX1V001`, `status: ROOT_AUTHORIZED`, `authority: {identity: Claude2, role: coordinator_and_single_scientific_launch_owner}`. Required fields:

- `plan`: exact final-plan pin; `sources`: absolute source-path to byte-sha mapping for the complete preflight closure and launcher/guard/monitor/drivers; `source_review`: pinned `UNT_STEP4_SOURCE_REVIEW_CX1V001` with `status: TESTED`, `verdict: PASS`, non-Codex1 reviewer, empty `blocking_findings`, and exact `approved_sources` mapping.
- `v007`: pins `seal`, `verdict`, `prereg`, `compare`, `addendum`, `case_block`. The guard checks root seal, r5, prereg/case-block, report script SHA, test_mode false, tests_read true, ADOPT_TAIL, the immutable reviewed policy's exact seal tuple and actual `check_numerics` replay.
- `config`: final C1 pin; `context_module`: reviewed native orchestrator module pin; `adoption_policy`: reviewed immutable registered-tuple successor; `direct_context`: this packet's direct-preflight adapter pin. Current upstream empty tuple, null certificate registry/policy or unavailable per-D comparator remains a refusal. No auto-registration occurs.
- `route_a_admission`: identical to plan; `case_order`: exact case list; `caps`: case to exact positive integer `wall_cap_s`, `rss_cap_bytes`, `output_cap_bytes`; `calls`: case to exactly `{spec, driver, prelaunch}` pins.
- `core_priority`: exactly `{normal_qos_required:true, step2_route_a_inactive:true, campaign_inactive:true, background_noncritical_lanes:true, sleep_assertion_required:true}`. This root attestation supplies external campaign/step-2 occupancy; the packet's flock only excludes other instances of this step-4 launcher. It does not retrofit unrelated launchers.
- DIII additionally needs `tail_off_policy`: root-authorized `UNT_STEP4_DIII_POLICY_CX1V001`, TESTED/PASS, `post_adoption_only:true`, cases binding exact spec/driver pairs. Only the native omitted `uv_tail` schema is eligible. Certificate applicability is explicitly recorded as reviewed tail-OFF identity, not silently skipped by null registry. DIII remains post-adoption under 0620.

All fields above are root-reviewed inputs, not populated automatically from Claude4's provisional files. Every source the native preflight reads under Research must be in `sources`. During the scoped fence, SourceFileLoader.get_code for Research source is replaced with exact verified-buffer compilation: it never probes .pyc, whether cached bytes exist or not. The original method is restored at fence exit. Every Research compile audit also verifies the actual source buffer hash, closing the transitive prehash/import gap; direct pyc reads remain refused. r5's normalization includes its pinned tail library source. The source review must cover that full closure. The synthetic tests use explicitly synthetic source adapters; their files and purported review markers are never production authority.

## Plan and PRELAUNCH

Final plan schema `UNT_STEP4_LAUNCH_PLAN_CX1V001`, `binding_status: ROOT_BOUND`, batch HEADLINE/DIII/SENS_LO/SENS_HI/POST_S1; launcher, guard and monitor pins; launcher_log; nonempty calls. Each call binds case, family, tail_on, driver_role, distance_Mpc, spec pin, `spec_status: ROOT_FINAL`, `pending: []`, PRELAUNCH pin, driver pin, three positive integer caps, outdir/receipt/monitor_log. Main/root callers must create output parent directories beforehand; no reuse/retry is admitted. Outputs are canonicalized and alias/nested conflicts rejected.

Driver is exact r5 b5cc62af for tail-ON and new DIII; v009-GEO 237ef3d4 is eligible only for tail-OFF DECIDING_III with `driver_role: REFERENCE_V009GEO`. The fixed monitor is ba031c23. No future r6 is silently substituted.

The PRELAUNCH file is exactly the deterministic return of `native_preflight(admission, call)`, schema `UNT_STEP4_PRELAUNCH_CX1V001`, binding spec/driver/C1/adoption-verdict and the actual native certificate_policy_gate, certificate_check(prelaunch), sensitivity_gate and normalized-spec digest. Root may obtain it by a controlled in-process, read-only call after final inputs exist; it must be published under a new name. The launcher's independent repeat must equal those bytes semantically. A PASS label is insufficient.

The explicit `DirectPreflightContext` reconstructs the native coordinate template with adopted numerics, validates target-free anchor registration, C1 schema, non-synthetic mode, r5, template identity, inclination, A7 and native normalization. It preserves the native prelaunch/certificate/sensitivity methods unchanged. Its state is exactly cfg/numerics/D/norm_base. It does not construct campaign observations, work-volume/cache/engine state or future deciding results. It is not a substitute for campaign Context admission, and this launcher has no campaign execution path.

## Ramp and process boundary

Root-approved max_active must be integer 1..6; Claude4's proposal is 3. Free memory must be >=25%, including the first call. The previous call's first complete route-A iteration gates every later call, one start per 60-second poll. Unknown memory waits. Malformed complete progress, missing/systemic receipts, caps/setup refusal and an ended predecessor with no first iteration halt new starts. Ordinary scientific failure is retained; no automatic retry. Existing monitors are not killed by later admission refusal.

Every worker/monitor creation follows byte/admission/native revalidation. After admission, main and worker apply normal QoS with the actual macOS PID syntax `/usr/sbin/taskpolicy -B -p <ownpid>` and require success. Children inherit that state. Python uses -I -B and single-thread BLAS; root command uses nice -n10. The earlier /usr/bin path and -B utility-wrapper form were wrong; an ordinary OS control exposed both and launcher v007 fixes them. The worker starts caffeinate -i -w ownpid before any scientific monitor. Each monitor additionally runs as a caffeinate -i utility, inheriting the lock descriptor with pass_fds. Catchable SIGINT/SIGTERM/SIGHUP, KeyboardInterrupt/SystemExit and ordinary loop errors stop admission permanently and drain active monitors while retaining the lock. Assertion loss permits one bounded safety-only restoration; existing per-monitor utility assertions remain independent. Failure diagnostics are de-duplicated. Persistent empty flock inode is never deleted or rewritten. One ordinary short-lived OS helper verified correct taskpolicy PID reset, inherited FD across caffeinate, retained flock after parent FD closure, and forwarded exit7. Actual scientific monitor execution, live signal delivery, assertion observability/energy behavior and SIGKILL survival remain UNTESTED; the helper is not a scientific run.

## Binder

`step4_bind_cx1v005.py --final-plan INPUT --admission-candidate INPUT --plan-out NEW --admission-out NEW --command-out NEW` snapshots the plan exactly once, validates that same buffer with candidate admission `plan:null` and native checks, and emits exactly those validated bytes; serializes before any write; exclusive-creates three packet-local outputs. The output admission embeds the actual new plan pin. The command does not export/self-authenticate the admission digest. Root must independently review/publish it. Interrupted publication leaves any created prefix intact; choose new names, never overwrite.

## Test scope and preserved failures

Main/extra suites use synthetic adoption/policy/context modules and narrowly mocked processes. The direct-adapter suite uses actual Claude4 specs, actual r5 normalization and unmodified AST-extracted native parent prelaunch/A7/diff functions; anchor registration is stubbed in that suite. Actual certificate scientific proofs and post-adoption report tuples are pending, so no production preflight PASS is claimed. Test v001 syntax failure, synthetic v002 incomplete source closure and direct v001 missing tail-library source closure are preserved; successors corrected fixture/source inventory, not scientific expectations.

## 0625 closure boundary

- S4-GUARD-METADATA-1: lexical protected names are rejected before lstat/resolve/readlink. Componentwise symlink resolution rejects a protected target before any metadata probe of that target. Virtual-path tests verify zero protected probes; no actual protected path was tested.
- S4-BINDER-PIN-1: launcher and binder embed guard v006 byte SHA and compile the same verified bootstrap buffer. Wrong adjacent guard controls execute the entire entrypoint bootstrap and show no sentinel side effect.
- S4-BINDER-REREAD-1: one plan snapshot supplies digest, parse, validation and output; an injected later changed source cannot change publication, and the read-count test is exactly one.
- S4-NATIVE-LOADER-1: the actual native load_pinned_module function, AST-extracted without running native initialization, successfully loads owned inert source through real importlib SourceFileLoader under the fence with cached bytecode both absent and present. Verified source executes in both cases.
- S4-TRANSITIVE-PIN-1: compile auditing rejects a changed actual buffer after a good prehash. Source membership alone no longer confers execution authority.
- CX2-S4-LIFETIME-1/2: seven inert interruption/assertion/poll fault scenarios stop starts, retain the lock until terminal and bound restoration. Ordinary OS descriptor/exit control supports the independent lifetime-owner design at its exact tested scope; actual signal/SIGKILL and scientific monitor execution remain untested.
- S4-SCHEMA-DOC-1: stale mode-versus-enabled comment removed; enabled/omitted-block schema behavior unchanged.

Preserved0625 harness failure: v001 reached the ordinary OS helper and then failed on the incorrect taskpolicy utility wrapper before recording results. OS_DIAG_V001 records the exact invalid -B utility invocation and passing caffeinate-only FD controls. Test v002 uses the corrected PID operation and records53/53. No earlier source or result was overwritten.

## Byte pins

- `af66d0d8861f3d414c3a52e12e8b1f8d5f205c96b0abaf932949575a3ffe5832`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v006.py`
- `f0443f33eaf3fda78fd7d36cb8f093e2a04edf5aa73876a6a39c298065f7faef`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_launcher_cx1v007.py`
- `30ca87c77c82f33e880b9c42665d1c5a62eea739d5b32e5de42e631ef00f9d7a`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_bind_cx1v005.py`
- `eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py`
- `fcff3af9553052e262249c82bc1b12d7ab816acc4ae1d5c378beb8cab68befec`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_step4_cx1v006.py`
- `6bdad13055a3440ed098ed8b57ea901885b0547eacd298a38278e205f0736dc3`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_step4_extra_cx1v004.py`
- `1eeb2cd1d615fca4ecd1b915297d7f2d38d5e5e0ebe0fa9a5925ecb1e25a5f2b`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_direct_adapter_cx1v003.py`
- `f7411d6d2095d1dc6493ede229225303618a674c5979bf4d8489f4cc3f24549f`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_0625_controls_cx1v002.py`
- `ded6d1b8edc0c621a5c77dd8de552c022cad8855f3a1eddf358821f6f6fc8310`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/SYNTH_V006/RESULTS.json`
- `3323520f26cb5a76021a868e21132acf95d2356dbb25d6adc1ae3fd1eb62a3e4`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/EXTRA_V004/RESULTS.json`
- `502705ed527eda65d4c1ec74a19bdfc0002ecc5abcb9b7c92fd369c9c4cc85ed`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/DIRECT_V003/RESULTS.json`
- `0a9f3bf514db4edc67ed0a9c54555e98f93d14cfbde7e2fe6427ae5af613cd4e`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/FIX0625_V002/RESULTS.json`
- `ed438da5cb135dbd4b83779b3d7d54e2bd44ba89cd4832ad2a58f4d5e76bb7d1`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/OS_DIAG_V001.json`
