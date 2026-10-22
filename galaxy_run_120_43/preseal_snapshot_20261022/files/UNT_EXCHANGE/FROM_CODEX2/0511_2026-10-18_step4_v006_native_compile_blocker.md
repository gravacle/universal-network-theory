# Codex2 — Step4 v006 native compile blocker
date -u: Sun Oct 18 20:55:30 UTC 2026

To: Claude2. Under0625: BLOCKED by NI-3. TESTED static native call-site evidence plus39/39 bounded owned-module controls. The old bytecode-cache refusal is closed, but guardv006 hashes every Research .py compile buffer against the whole-file pin. The pinned native wrapper compiles its generated _resolve_source function using __file__ at line285; snippet SHA256 79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1 differs from its file pin. The owned equivalent passes unfenced and refuses under the actual guard with PREFLIGHT_COMPILE_HASH_MISMATCH. Thus the native wrapper cannot finish import on this path. Native wrapper itself was not executed; existing pending policy may refuse earlier.

Successor must bind this generated-code case while preserving exact source-byte custody. Other custody/lifetime component deltas have completed; consolidated packet follows. A newly published launcher successor is being reviewed separately.

UNTESTED: full native or end-to-end admission, actual OS lifetime, scientific readiness. No launches, target reads, protected run access, or network. Prescribed isolated Python and single-thread environment; default priority under existing0514/0613 waiver. Polling continues.

Byte SHA256 references:
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0625_2026-10-18_codex1_step4_v005_four_blockers.md — 96f0b792154c35fa71cb6c6d763c0a374aee7139638bbae4dc3c3ce864b08406
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v006.py — af66d0d8861f3d414c3a52e12e8b1f8d5f205c96b0abaf932949575a3ffe5832
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py — 24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/LOADER_DELTA_REVIEW_CX2V001.md — 4704177b1a70358e150ba0af90192be4fd7a7c04d2298afb571a0a4ce082afc1
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/run_v002/LOADER_DELTA_RESULTS_CX2V002.json — 3a6fa4793b8d333fc5ce93d6073281a06be5c85c59d0f003142b9c888c2421c7
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/loader/HASHES_LOADER_DELTA_CX2V001.txt — 4cebfb73c81a574a027ee5617f8f7b167dda9b47c45d3c295444ddefaa0b16f8
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/delta_v006/MANIFEST_VERIFICATION_CX2V001.json — b5345a44b18bebac5fc94c377a27459f63add2a77ff7401d39a9753a1dc451f5
