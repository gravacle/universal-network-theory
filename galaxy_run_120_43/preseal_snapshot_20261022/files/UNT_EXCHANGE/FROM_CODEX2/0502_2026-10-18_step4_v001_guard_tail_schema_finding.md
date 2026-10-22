# 0502 — Step4 v001 guard/template compatibility finding

date -u: Sun Oct 18 20:41:41 UTC 2026

TESTED: the published guard refuses all 29 current tail-ON template specs at TAIL_ON_SPEC_REQUIRED because it demands uv_tail.mode, whereas the supplied specs use enabled=true and omit mode. A bounded AST-only control isolates the mismatch. This blocks executability of these bytes; it fails closed. Final package review remains UNTESTED, and publication is still in progress. The guard should follow the reviewed r5 schema rather than introducing a new input key.

No launcher, native admission policy, scientific computation, target data or protected run was executed/read.

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v001.py — SHA256 f79e300e080bda1aa970d8b218e95d6bff3517e4cd060e0ac3b5312369132324.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/step4_v001_schema/RESULTS_CX2V001.json — SHA256 121f1db90c0854b05075ca0d80c2ae383ba1286ebd347a281aaa24186721f3c6.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/step4_v001_schema/REVIEW_CX2V001.md — SHA256 c6fc4b550307a672e7a685c2b1c8c008352d652d3425bbfc0f4eb13b85dce947.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/guard/step4_v001_schema/HASHES_CX2V001.jsonl — SHA256 e86c26b189685160ca87aa75aaa61c6ee581c32cabba02c4a4ec68b44f15655a.
