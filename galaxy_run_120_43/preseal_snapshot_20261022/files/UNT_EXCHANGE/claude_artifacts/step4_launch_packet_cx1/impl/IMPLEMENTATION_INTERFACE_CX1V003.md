# Step-4 guarded direct-run interface, Codex1 implementation V003 (0625 and NI-3 successors)

UTC from `date -u`: Sun Oct 18 20:59:48 UTC 2026

**TESTED:** 187/187 checks: 40/40 synthetic admission/process-seam, 21/21 additional binder/path/driver/lock, 43/43 direct-adapter and actual Claude4 structural-spec, 53/53 direct0625 source/loader/lifetime/ordinary-OS-helper controls, and 30/30 actual-native-import/generated-code/registered-source/alias controls. The 43 include all 29 actual tail-ON and four tail-OFF template rows. Scientific process count: zero. **UNTESTED:** actual production adoption/certificates/sensitivity and launch. Template compatibility does not grant admission.

Only the four implementation files listed below are the candidate supported set. Earlier guard through v006, launcher through v007 and binder through v005 remain immutable historical candidates. The full Context-constructor volume/diskutil trap in v004 is replaced by the explicit direct-run adapter inherited from v005; no subprocess exception was added to preflight.

## Runtime authority and root input contract

The launcher requires independent publication of `UNT_STEP4_ADMISSION_PATH` and `UNT_STEP4_ADMISSION_SHA256`. These bind the admission bytes; they are not a cryptographic identity. Merely possessing a file containing Claude2's name does not establish authorization. Root alone publishes and executes.

Admission schema `UNT_STEP4_ADMISSION_CX1V001`, `status: ROOT_AUTHORIZED`, `authority: {identity: Claude2, role: coordinator_and_single_scientific_launch_owner}`. Required fields:

- `plan`: exact final-plan pin; `sources`: absolute source-path to byte-sha mapping for the complete preflight closure and launcher/guard/monitor/drivers; `source_review`: pinned `UNT_STEP4_SOURCE_REVIEW_CX1V001` with `status: TESTED`, `verdict: PASS`, non-Codex1 reviewer, empty `blocking_findings`, and exact `approved_sources` mapping.
- `v007`: pins `seal`, `verdict`, `prereg`, `compare`, `addendum`, `case_block`. The guard checks root seal, r5, prereg/case-block, report script SHA, test_mode false, tests_read true, ADOPT_TAIL, the immutable reviewed policy's exact seal tuple and actual `check_numerics` replay.
- `config`: final C1 pin; `context_module`: reviewed native orchestrator module pin; `adoption_policy`: reviewed immutable registered-tuple successor; `direct_context`: this packet's direct-preflight adapter pin. Current upstream empty tuple, null certificate registry/policy or unavailable per-D comparator remains a refusal. No auto-registration occurs.
- `route_a_admission`: identical to plan; `case_order`: exact case list; `caps`: case to exact positive integer `wall_cap_s`, `rss_cap_bytes`, `output_cap_bytes`; `calls`: case to exactly `{spec, driver, prelaunch}` pins.
- `core_priority`: exactly `{normal_qos_required:true, step2_route_a_inactive:true, campaign_inactive:true, background_noncritical_lanes:true, sleep_assertion_required:true}`. This root attestation supplies external campaign/step-2 occupancy; the packet's flock only excludes other instances of this step-4 launcher. It does not retrofit unrelated launchers.
- DIII additionally needs `tail_off_policy`: root-authorized `UNT_STEP4_DIII_POLICY_CX1V001`, TESTED/PASS, `post_adoption_only:true`, cases binding exact spec/driver pairs. Only the native omitted `uv_tail` schema is eligible. Certificate applicability is explicitly recorded as reviewed tail-OFF identity, not silently skipped by null registry. DIII remains post-adoption under 0620.

All fields above are root-reviewed inputs, not populated automatically from Claude4's provisional files. Every source the native preflight reads under Research must be in `sources`. The scoped fence canonicalizes registered source paths through the protected-name-first `safe_path`; legacy symlink aliases remain usable, and conflicting hashes for the same canonical source are refused. SourceFileLoader.get_code for every registered source, regardless of directory, and every Research .py source is replaced with exact verified-buffer compilation. It never probes .pyc; associated registered caches and Research caches are refused. The original loader method is restored at fence exit. Compile auditing checks the actual source buffer hash for the same scope, closing the transitive prehash/import gap. The only generated-buffer allowance is the exact reviewed native-wrapper owner SHA plus exact literal snippet SHA listed below, with the owner bytes verified again at generated compile time. Changed snippets, changed owner bytes and absent/different owner pins fail closed. r5's normalization includes its pinned tail library source. The source review must cover that full closure. The synthetic tests use explicitly synthetic source adapters; their files and purported review markers are never production authority.

## Plan and PRELAUNCH

Final plan schema `UNT_STEP4_LAUNCH_PLAN_CX1V001`, `binding_status: ROOT_BOUND`, batch HEADLINE/DIII/SENS_LO/SENS_HI/POST_S1; launcher, guard and monitor pins; launcher_log; nonempty calls. Each call binds case, family, tail_on, driver_role, distance_Mpc, spec pin, `spec_status: ROOT_FINAL`, `pending: []`, PRELAUNCH pin, driver pin, three positive integer caps, outdir/receipt/monitor_log. Main/root callers must create output parent directories beforehand; no reuse/retry is admitted. Outputs are canonicalized and alias/nested conflicts rejected.

Driver is exact r5 b5cc62af for tail-ON and new DIII; v009-GEO 237ef3d4 is eligible only for tail-OFF DECIDING_III with `driver_role: REFERENCE_V009GEO`. The fixed monitor is ba031c23. No future r6 is silently substituted.

The PRELAUNCH file is exactly the deterministic return of `native_preflight(admission, call)`, schema `UNT_STEP4_PRELAUNCH_CX1V001`, binding spec/driver/C1/adoption-verdict and the actual native certificate_policy_gate, certificate_check(prelaunch), sensitivity_gate and normalized-spec digest. Root may obtain it by a controlled in-process, read-only call after final inputs exist; it must be published under a new name. The launcher's independent repeat must equal those bytes semantically. A PASS label is insufficient.

The explicit `DirectPreflightContext` reconstructs the native coordinate template with adopted numerics, validates target-free anchor registration, C1 schema, non-synthetic mode, r5, template identity, inclination, A7 and native normalization. It preserves the native prelaunch/certificate/sensitivity methods unchanged. Its state is exactly cfg/numerics/D/norm_base. It does not construct campaign observations, work-volume/cache/engine state or future deciding results. It is not a substitute for campaign Context admission, and this launcher has no campaign execution path.

## Ramp and process boundary

Root-approved max_active must be integer 1..6; Claude4's proposal is 3. Free memory must be >=25%, including the first call. The previous call's first complete route-A iteration gates every later call, one start per 60-second poll. Unknown memory waits. Malformed complete progress, missing/systemic receipts, caps/setup refusal and an ended predecessor with no first iteration halt new starts. Ordinary scientific failure is retained; no automatic retry. Existing monitors are not killed by later admission refusal.

Every worker/monitor creation follows byte/admission/native revalidation. After admission, main and worker apply normal QoS with the actual macOS PID syntax `/usr/sbin/taskpolicy -B -p <ownpid>` and require success. Children inherit that state. Python uses -I -B and single-thread BLAS; root command uses nice -n10. The earlier /usr/bin path and -B utility-wrapper form were wrong; an ordinary OS control exposed both and launcher v007 fixes them. The worker starts caffeinate -i -w ownpid before any scientific monitor. Each monitor additionally runs as a caffeinate -i utility, inheriting the lock descriptor with pass_fds. Catchable SIGINT/SIGTERM/SIGHUP, KeyboardInterrupt/SystemExit and ordinary loop errors stop admission permanently and drain active monitors while retaining the lock. Assertion loss permits one bounded safety-only restoration; existing per-monitor utility assertions remain independent. Failure diagnostics are de-duplicated. Persistent empty flock inode is never deleted or rewritten. One ordinary short-lived OS helper verified correct taskpolicy PID reset, inherited FD across caffeinate, retained flock after parent FD closure, and forwarded exit7. Actual scientific monitor execution, live signal delivery, assertion observability/energy behavior and SIGKILL survival remain UNTESTED; the helper is not a scientific run.

## Binder

`step4_bind_cx1v006.py --final-plan INPUT --admission-candidate INPUT --plan-out NEW --admission-out NEW --command-out NEW` snapshots the plan exactly once, validates that same buffer with candidate admission `plan:null` and native checks, and emits exactly those validated bytes; serializes before any write; exclusive-creates three packet-local outputs. The output admission embeds the actual new plan pin. The command does not export/self-authenticate the admission digest. Root must independently review/publish it. Interrupted publication leaves any created prefix intact; choose new names, never overwrite.

## Test scope and preserved failures

Main/extra suites use synthetic adoption/policy/context modules and narrowly mocked processes. The direct-adapter suite uses actual Claude4 specs, actual r5 normalization and unmodified AST-extracted native parent prelaunch/A7/diff functions; anchor registration is stubbed in that suite. Actual certificate scientific proofs and post-adoption report tuples are pending, so no production preflight PASS is claimed. Test v001 syntax failure, synthetic v002 incomplete source closure and direct v001 missing tail-library source closure are preserved; successors corrected fixture/source inventory, not scientific expectations.

## 0625 closure boundary

- S4-GUARD-METADATA-1: lexical protected names are rejected before lstat/resolve/readlink. Componentwise symlink resolution rejects a protected target before any metadata probe of that target. Virtual-path tests verify zero protected probes; no actual protected path was tested.
- S4-BINDER-PIN-1: launcher and binder embed guard v007 byte SHA and compile the same verified bootstrap buffer. Wrong adjacent guard controls execute the entire entrypoint bootstrap and show no sentinel side effect.
- S4-BINDER-REREAD-1: one plan snapshot supplies digest, parse, validation and output; an injected later changed source cannot change publication, and the read-count test is exactly one.
- S4-NATIVE-LOADER-1: the actual native load_pinned_module function, AST-extracted without running native initialization, successfully loads owned inert source through real importlib SourceFileLoader under the fence with cached bytecode both absent and present. Verified source executes in both cases.
- S4-TRANSITIVE-PIN-1: compile auditing rejects a changed actual buffer after a good prehash. Source membership alone no longer confers execution authority.
- CX2-S4-LIFETIME-1/2: seven inert interruption/assertion/poll fault scenarios stop starts, retain the lock until terminal and bound restoration. Ordinary OS descriptor/exit control supports the independent lifetime-owner design at its exact tested scope; actual signal/SIGKILL and scientific monitor execution remain untested.
- S4-SCHEMA-DOC-1: stale mode-versus-enabled comment removed; enabled/omitted-block schema behavior unchanged.

Preserved0625 harness failure: v001 reached the ordinary OS helper and then failed on the incorrect taskpolicy utility wrapper before recording results. OS_DIAG_V001 records the exact invalid -B utility invocation and passing caffeinate-only FD controls. Test v002 uses the corrected PID operation and records53/53. No earlier source or result was overwritten.

## NI-3 native import closure

The production native wrapper imports five pinned source files without constructing Context. The builder integration test and independent review both executed that actual import under the source fence. The builder added a second independent Research-open allowlist restricted to those five source paths and observed no configuration/data reads or processes. Import success is not a production certificate, adoption or sensitivity PASS.

The generated-code contract is the exact owner SHA `24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af` and snippet SHA `79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1`. The test verifies from the pinned owner AST that `_resolve_source` is that literal string and the compile call uses `_resolve_source`, `__file__`, and `exec`. No AST, string-generation or arbitrary owner exception is admitted at runtime. A new native owner or generated literal requires a reviewed guard successor.

Additional tests cover a real registered standard-library source outside Research using actual SourceFileLoader, forced rejection of the original cached loader path, changed compile bytes, cached and legacy .pyc refusal, real owned source symlinks, conflicting alias hashes, and protected source-map names refused before metadata. All checks preserve the production fence itself.

Preserved NI-3 harness failure: native-import test V001 completed the actual import but its generated-function assertion mistakenly looked for `O.CampaignExecutor.resolve`; the native wrapper installs `O.resolve`. Test V002 corrects that assertion and passes30/30. No implementation source changed because of this harness error. The V001 result remains29/30, never rewritten.

## Byte pins

- `42bf0ce9dcd48f734299ace4f07cb92a15563e57a39f5ae40be451e481d1c3de`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v007.py`
- `bf2d535fe8eb1a83a7e3c92751a5baeaf19bb7d3abef72bb3db964b8e36ba041`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_launcher_cx1v008.py`
- `3db8c72a36a1574ba0908da323effe49ded106aecc1c67f8a76152b6b54ad9cb`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_bind_cx1v006.py`
- `eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py`
- `0df4d723fb3f3cb0fab3cb91a0d71f4a6c5ac0f918beb66b558a949be7309163`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_step4_cx1v007.py`
- `b0d3f7bac66c2790d3a9dd236b5d07ec8105f9fa3c3127e8b01203a6cc7b7e6b`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_step4_extra_cx1v005.py`
- `324b653d262b0f7591414ec228b58c31fc77e854a5959721928059e2c3ed6635`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_direct_adapter_cx1v004.py`
- `dd75f768edd03472295c381492f78ef95e75e2d9bfce3a041a938620868b59f7`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_0625_controls_cx1v003.py`
- `8c65d9452c92218f125ac5c6566180ecdfe2fbedbf4c9c619658d38273f7b7a3`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_native_import_cx1v002.py`
- `87cdbd59d322feb08f2e6705b46a2d6bb4b126ed36b805c394574177af81cb17`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/SYNTH_V007/RESULTS.json`
- `13f095443161cd8323767f978d657b806a03b6ffae4d0f1402ab10dd0fc26a80`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/EXTRA_V005/RESULTS.json`
- `caccf3ec67f1447022495de044a549493155be4e149c31e82350b97a148bead0`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/DIRECT_V004/RESULTS.json`
- `3eedfcebb2e9490d485f91831b4034b8d9bdaa1fdcade8e59d322505e64bac39`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/FIX0625_V003/RESULTS.json`
- `d5f2840390d52cc98a737f2ad790b12df94ce5a39bac6c29296e2d231829a767`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/NATIVE_IMPORT_V002/RESULTS.json`
- `133fb00c4c3b9b9389f85a2f7af38cb07a5a2111943afbf341490b7cc9f08e47`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/test_native_import_cx1v001.py`
- `1c4b0dac7ce93001571b2849ea17e2278f56620ae8e15c8ea7fa781c1420d2cb`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/NATIVE_IMPORT_V001/RESULTS.json`
- `ed438da5cb135dbd4b83779b3d7d54e2bd44ba89cd4832ad2a58f4d5e76bb7d1`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/tests/OS_DIAG_V001.json`
- `8229c74ed9f63c9ee2005dce37b24e6dfe59d1ece2d6046eb1cf9e59347f1efc`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/review/NATIVE_IMPORT_INDEPENDENT_V001/RESULTS.json`
- `5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py`
- `8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py`
- `a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py`
- `24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py`
- `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d`  `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py`
