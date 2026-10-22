# Step-4 to step-5 admission rules audit — CX1V001

date -u: Sun Oct 18 21:24:36 UTC 2026

**Verdict: WAIT_FOR_FULL_STEP4_DECISION under the currently published producer/consumer contract.** This is a custody/interface conclusion, not a claim that the scientific membership test is global. **TESTED source audit:** the native rectangle-membership predicate is pointwise and independent of later points; **UNTESTED:** any production point admission or incremental release.

The pure native classifier was extracted with its original fail-closed decorator and helper functions and run on invented two-row numbers: 9/9 controls PASS. No orchestrator Context was instantiated, no full driver/engine was imported, and no science or dry-plan process was launched by this audit. No real DDO or NGC observation file, run receipt, result, protected run path, or target velocity was opened. Source text that mentions those fields was inspected. v001 extraction failed before tests because its decorator dependency was omitted; v002 includes the actual dependency and succeeds. The failed script is preserved.

## Exact distinctions

1. **Forward VALID is insufficient.** Engine `classify_prediction` L955–1025 requires every declared row to have a finite value with literal bool True validity. `admitted` is true exactly when every value is inside its fixed closed rectangle. A valid forward outside one rectangle is scientifically non-admitted. The synthetic control reproduces that distinction.
2. **Native point membership is independent of future evaluations.** `_evaluate_point` L1033–1090 stores the per-point verdict. `_explore_impl.verified_admitted` L1944–1953 checks the saved verdict and reclassifies the same logged prediction. `admitted_entries` L1965–1966 scans all usable logged entries. Finalisation L2130–2155 includes every such admitted entry: projections, interior score and primary anchor are metadata, not a global-best threshold that revokes earlier rectangle membership. This holds for unchanged coordinate, region, source, result and certificate identities; a later revision of those identities is a different scientific context.
3. **Per-call certificates are another gate.** Wrapper L202–222 creates `TAIL_CERTIFICATE_ACCEPTANCE_CX2V001` after result/spec/bundle checks. L229–243 rechecks cached certificate custody, and L265–276 upgrades certificate failure to INFRA. These acceptance records admit a forward result to the cache; they do not assert DDO rectangle membership or construct native `admitted_points`.
4. **The present orchestrator does not emit incremental scientific point records.** Parent `Probe.run` L2568–2627 returns `run=None` whenever its probe stops or has misses/placeholders. `run` L3436–3526 completes waves then calls `finalise`. `finalise` L3553–3585 performs two complete cache-only deterministic replays, then writes/verifies the native calibration record and FINAL_SUMMARY. No existing per-point record callback was found on this path. The local direct-run guard is an execution-admission mechanism; it cannot create a final scientific admission merely from completion.
5. **The selected downstream contract requires the missing scientific custody.** `HANDOFF_CONTRACT_CX3V002.md` says each export entry is copied from the actual native calibration `admitted_points`; an externally trusted root handoff pin confers admission. Its filler verifies coordinates/byte pins and maps the point; it does not authenticate scientific admission. An arbitrary self-consistent SHA is insufficient.
6. **Current Claude4 order agrees with a whole-campaign handoff.** Inventory L3920–4045 describes campaign replay/final summary as unlocking step 5. L4062–4094 additionally identifies S4-POST-S1 as a registered transfer test before prediction, depending on campaign FINAL_SUMMARY. `c4_root_items` L194–200 keeps that condition explicit. These are readiness metadata, including recommendations; older preseal DIII scheduling is superseded by dispatch 0620 and is not adopted by this audit.

## Stable membership does not freeze the selected region

`freeze` L1520–1605 derives hull extrema, centroid-nearest/interior members and the anchor from the whole admitted set. Those selected members and the aggregate prediction band can change when more points arrive, although a previously verified admitted point remains admitted. `coordinate_addendum` L5–18 (A23) explicitly disclaims monotonicity of the frozen min/median/max headline under restriction. Therefore a future stream may safely retain point-local computation in principle, but may not label a partial set as the final region/member roster or freeze. No current record contract establishes that stream.

The engine writes registration records for every terminal outcome, including BUDGET_EXHAUSTED (engine L2897–2913). A byte-valid registered record is not by itself COMPLETE scientific acceptance. Parent summary L3716–3721 retains the no-freeze disposition for non-COMPLETE status. Do not silently equate orchestrator wrapper status COMPLETE (workflow finished) with `engine_status == COMPLETE`, `engine_ok == true`, or a root-approved prediction release.

## Native layout and verifier

Native record schema is `CALIBRATION_RUN_RECORD_C2V003`. Engine L2956–2976 writes schema, created_utc, module/module_file_sha256, status, ok, stage_reached, region_sha256, exploration_fingerprint, ngc3198_access, run, then record_sha256. The scientific entries are at `run.exploration.admitted_points`; `_point_from_entry` L1661–1670 carries u, theta_internal, theta_natural, prediction, log_index, purpose, valid, admitted, row_inside. Finalise adds projection and interior metadata. The safe downstream export contains **only** log_index, u and theta_natural.

`verify_calibration_record(record_path=..., registry_path=...)` (engine L3017–3108) checks canonical bytes, self-hash, fingerprint and registry hash-chain membership; it does not independently reclassify every saved prediction. The freeze module `_check_calibration_record` L2919–2980 explicitly re-derives rectangles from their pinned file and reclassifies members. That is source evidence only: this lane did not invoke either on real data. Root/source-producer must retain the native record, registry, actual membership verification and deterministic replay custody without exposing target/prediction arrays to the handoff writer.

## Independent interface blocker: 3-D native u versus 4-D filler u

**TESTED from current bytes.** The config pins coordinate_addendum mode `DDO154_DISTANCE_FIXED_AT_REGISTERED`; parent L1985–2009 changes only distance_Mpc role from nuisance to fixed. Native headline varying coordinates are common_scale_s, gamma_over_Eref, ell_F_m (3 entries). The locked filler L90–120 uses unmodified policy coordinate `engine_coordinates`, with distance_Mpc also varying (4 entries). It refuses a genuine three-entry headline u at VARYING_U_LENGTH. Filling a fourth component silently violates the selected contract's copied-native-u rule. A reviewed bridge or selected filler/policy successor must explicitly bind the native coordinate mode and preserve native custody. The point's 29-name theta contains distance_Mpc=4.04, but that does not authorize inventing a different native u vector.

## Root contract items

- Choose/adopt an immutable release contract and actual target-free scientific producer. Bind sealed V007 ADOPT_TAIL, native record/registry and verification, complete decision/replay provenance, and point-bound certificate evidence to an independently supplied release pin. A forged but rehashed input must not self-authorize.
- Resolve the three-u/four-u mismatch with a reviewed explicit successor/bridge. Preserve the original native coordinate mode/u and scientific point identity; no padding by the writer.
- If overlap before full campaign completion is still desired, specify and review an incremental native admission producer and custody contract. It must perform the same rectangle-membership and certificate checks under fixed pins, preserve failures and stable identities, and distinguish point-local reuse from final member selection/region/freeze. The current writer should refuse a streaming mode rather than guess this contract.
- Preserve/rule the existing S4-POST-S1 before-prediction requirement in that contract. Root owns the cases, thresholds and reading already identified by Claude4; this audit creates no new review gate.
- Supply actual NGC point/grid EPS/LO/GQ and route preflight evidence separately from DDO per-call certificates. The handoff/export is target-free custody, never launch authorization. Existing step-5 numerical/root conditions remain scoped to their real records.

Production record availability, actual sealed adoption, full native record verification, certificate coverage, root approval and live streaming are **UNTESTED** here. The current decision to wait uses existing interface obligations; it does not prohibit a future explicitly adopted streaming successor.

## Byte pins

Each identifier below is a cited source; line numbers above refer to these exact bytes. The authority file can evolve, so its hash records this audit snapshot only.

- `authority`: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md` — `59ada35ce59146c758374c88abeb3ed183f09217501d1f3c7a43463adacc6917`
- `c4_inventory`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/inventory/INVENTORY_C4V001.json` — `eb359e0f902298b4d8d41e879b1ba85f852e4bf29d7d9d126a66dc239baee75b`
- `c4_order`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/LAUNCH_ORDER_C4V001.md` — `c276c4d9e3c5552d26ae600eac01d97489aaf766daf2abf5e6fe69185a795938`
- `c4_root_items`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V001.md` — `5d83f0672f9b45fdae31772b2c29c5f786159aa960f0855cc1e258291353ee36`
- `config`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json` — `721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e`
- `coordinate_addendum`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/COORDINATE_ADDENDUM_CX2V006.json` — `9962b2aa673572a712d07fd74d12e61fe2418acbeb03b0ef3437118a6ca1e2b9`
- `coordinates`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json` — `50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f`
- `core`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py` — `a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605`
- `dispatch`: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0631_2026-10-18_codex1_step4_to_step5_handoff_pipelining.md` — `044628c989e72528e34525128003a3f8e6abe16de8a11550aa3dd51f9575e8be`
- `engine`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py` — `6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3`
- `filler`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/tools/fill_step5_cx3v003.py` — `2348974f469ff2d9177a1f3be88296180bb7c614dad7e820438991abac3ddd6c`
- `filler_contract`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/HANDOFF_CONTRACT_CX3V002.md` — `6ae6a0fc406df004e1aaeb425dd4ee3966c797b63f6d775bfb92d9a340b6dc7a`
- `filler_policy`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/POLICY_CX3V001.json` — `4f0d7d039fcee03fc9e2e1c74624919c77b14e19b101389124864219057e5bbf`
- `filler_root_items`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3/ROOT_ITEMS_CX3V002.json` — `3e9e31d41d673ebab357b82c365c551578302e9b95ddb705211b3cb1e5685471`
- `freeze`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/prediction_freeze_c2v003d.py` — `74e0d4060e443755486fba3aa0775060d2909c2bb78df9d948f346159112b67d`
- `parent`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` — `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d`
- `self`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_step5_handoff_cx1/rules/audit_rules_cx1v002.py` — `b4fd6bbfb43f6150510c348d3df9996181ccb782c69c9b2de0cb3636eabdc38c`
- `wrapper`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py` — `24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af`
- `audit_rules_cx1v001.py`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_step5_handoff_cx1/rules/audit_rules_cx1v001.py` — `73daa5e942ccb76f1ae79c22230a953b4675425e9268a07d8ec24a81a16ec757`
- `RULES_AUDIT_CX1V002.json`: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_step5_handoff_cx1/rules/RULES_AUDIT_CX1V002.json` — `d03e554e04404594b7c6e4b760d88c0ad169d388cf7658d669f5f3fb5fb46c09`
