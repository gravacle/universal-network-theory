# v006r8 build — 0554

`date -u`: Sun Oct 18 15:08:27 UTC 2026

**TESTED build; production UNTESTED and blocked.** Final candidate: wrapper v004, core v003, sensitivity policy v002, and the r8 P128/Ms128 config. Independent controls passed 42/42. Parent static/dry controls passed 131/131: 35 actual r5 normalizations, one actual dry plan, zero executed stages and zero scientific launches. Execution note: `nice unavailable (sandbox); 0514 waiver`.

The reanchor is now the exact pinned A2F10 anchor template's physical values and coefficient pin `2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7`, at D=4.04. This is the registered template, not the slightly different log/exp reconstructed engine seed. No tolerance, old result reuse or anchor alias is allowed. The new target-free registration artifact binds the template and coordinate registration. `config.anchor` contains that registration, the exact physical/coefficient objects and the r5 driver identity. Actual tail-reanchor result, receipt and spec SHA stay null until available.

At deciding-evidence pin time the `reanchor` row must match the registered point exactly and its result, receipt and spec identity must equal `config.anchor`. A different fresh D=4.04 workers-8 run cannot substitute. The actual pinned r5 normalization, completed/valid result, receipt, adjacent finish and named-role checks remain enforced.

A context-local anchor binding covers both initial construction and every inherited `fresh_gates` recheck, with restoration in `finally`. The final core also passes the same parsed config object into the parent constructor. Independent tests exercise actual inherited construction/recheck, two contexts in A→B→A order, ambient-context restoration, injected failures and subsequent reuse. An early draft missed the recheck binding; the final v003 closes that finding without editing earlier files.

Sensitivity review trust now comes from exact review-file bytes in `REGISTERED_DISTINCT_REVIEW_SHA256`, an immutable source allowlist that defaults empty. Names are descriptive and grant no authorization. The review still must bind its evidence, run pair, plan, comparator report and exact distance. A root-reviewed source successor is required to register any review SHA.

**A68 is unresolved.** The retained c2v004-derived comparator still has the known stage-normalization collision and incomplete-result coverage. `COMPARATOR_A68_REVIEWED=False` explicitly blocks both alternate-distance gate admission and direct `compute_pair`/CLI evidence generation before run reads. A reviewed comparator successor is necessary; r8 does not claim to close those holes. The headline D=4.04 exemption is unchanged.

Root-invalid resolution remains disabled for tail-ON; MODEL_INVALID needs a later certified successor. Scientific certificate review remains null, approved producers remain empty, and V007 verdict trust, production timing/capability and actual reanchor results remain pending. Local source tests and dry plans confer no scientific launch authority.

All work was source inspection, target-free registration or synthetic/static/dry verification. No UVT run or receipt, C5H, NGC target velocity, session log or network resource was read by this build helper. All existing artifacts remain unchanged.

Files and SHA256 from bytes:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/calibration_orchestrator_cx2v006r8_v004.py` — `1ddbe6da1b34e84a9a419a0c72e2933a74cd3021cbdb68c91f5691193b9ce488`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/calibration_core_cx2v006r8_v003.py` — `603ab460fb039494659f5b0e03998b28ff2a7f124d9ae7fd7491340523929e08`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py` — `8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/RUN_CONFIG_DDO154_CX2V006R8_P128_MS128.json` — `4d2d19a28104c4e05eb015b6e5ad790b199c5ed75c49a2c5da80d1e000c6df75`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/REGISTERED_ANCHOR_CX2V006R8.json` — `7693959ceca48581a06c1ca439c02bd80fd2ecfb158073270e3d2dc614ea79c3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/STATIC_DRY_RESULTS_CX2V006R8.json` — `07e67a61d58a6f87b40859ad4d36a65e1d10265bf244c1a317f4dea282da951f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/independent_review/run_20261018T150752_67910/REVIEW_RESULTS.json` — `eec9464ae406e53af92e0a625e0e5600c880e95b01111a2fbb6c06438d5604f6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/independent_review/REVIEW_CX2V001.md` — `ff71929671af453e665cfe7c06548e555439ff8d19b61b43783aa11c2a8fb781`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/independent_review/HASHES_CX2V001.txt` — `5cb9f435cf24064bf8ecb97a16a27613e9b8c3a7507d76c147086b1032ce9284`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0554_2026-10-18_codex2_v006r8_reanchor_binding.md` — `a901d034aede5ef4eb091366df56a4a90ad2fd36a6f695cb479ee692ff960dc4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_calib_v006r7_c3/FINDINGS_V006R7_C3.md` — `5d014304f59a10f691f855eea9fd8a88597edd97ac6a2396f0b29946728cfd36`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json` — `50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/adoption_policy_cx2v006r7.py` — `7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/run_identity_compare_c2v004_r5_cx2v002.py` — `5e79c11e4699c311ad2cc419404a1eb28e78bdf03092d5642bc145438a47fb1a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r7/DECIDING_III_PAIR_PLAN_CX2V006R7_V002.json` — `cb42a5a3bf8e26d0aa2a3a4c35784c2301fde7ff6c60170da7536ba8cfd95656`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/specs/CALL_A2_ANCHOR_F10_C2V001.json` — `a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r8/TYPED_BLOCKERS_CX2V006R8.json` — `feba932d539ebacb3734fc47bb4e1e951188e87bf7d6f26c564266de6ec77669`
