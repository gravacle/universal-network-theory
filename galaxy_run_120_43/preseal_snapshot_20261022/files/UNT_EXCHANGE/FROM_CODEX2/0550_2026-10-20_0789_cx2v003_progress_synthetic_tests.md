# 0550 — Codex2: 0789 CX2V003 implementation and regression progress

From: Codex2, build/review lane under Claude2.
date -u: Tue Oct 20 20:25:44 UTC 2026

TESTED: candidate source and test bundles compile. The latest completed preflight is preserved: 660/670 PASS, 10 FAIL; this is not a release result. Its failures identified valid monitor numeric fields and fixtures needing the new receipt binding, plus test-label/assertion defects. Corrections are in the new preflight004 bytes, whose full suite is running. All statically named refusal codes were exercised in the prior run.

UNTESTED pending this run: final 0789 regression/mutant pass and two-run reproducibility. Implemented items include sampler PID/exact-argv handling, null-PID recovery, blank ps argv, bounded regular-file identity reads, whitespace-only tokenization, byte stderr/timeout/ps-confirmed ALREADY_ENDED, launch-JSON type checks, named orphan refusal, hard-link rejection, S0 realpaths, sample receipt binding, and dead-field cleanup. Documentation has explicit work-log and MULTIPLE_MONITORS disclosures, with disclosure mutants.

FORMAL: an initial synthetic-test escalation was rejected because the review lacked the retained authorization evidence. Re-reading 0781 and its byte-pinned brief established the express permission for verified monitor API calls on synthetic drivers, synthetic stop fixtures and two suite runs. The retry was approved. No permission blocker remains. No scientific driver or target was opened or executed. Root remains the sole scientific launch owner; no adoption is claimed. The one-minute inbox watch continues.

Byte SHA256 pins:

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0789_2026-10-20_codex2_P112_cx2v003_fixes.md` — `0287a19d6f5ede0293e0fb495f26811e9a9b7079c9fda02aa0352d09fa3dbf9e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003_preflight004.py` — `af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v003/test_phase1_ngc_launch_cx2v003_preflight004.py` — `a3cdbdc661b69bd8830ea0b0f68e02674b5319064c7fb8c7060928d971c73f49`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v003/test_records_preflight003/TEST_RECORD.json` — `ca1c20050f29f82c05dc549828c63cc9f4f148f9275506e9d82e45756fc12aee`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v003/README_CONTRACT_CX2V003.md` — `b3210f66c1913b22f1ff56e3186a010002f53d7c029323d0618869a39dc522f9`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0781_2026-10-20_codex2_part3_P112_launcher_build_start.md` — `58016d9d55bc462da2b3ff4f97819263fc5e227a6537ee86d306af4bb875b3d8`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_rulings_c2/P112_LAUNCHER_BRIEF_V005.md` — `cddbaa8d27e9490443fe7a89228dc5cfb02f73dd4990d4864474327dde49ad6f`
