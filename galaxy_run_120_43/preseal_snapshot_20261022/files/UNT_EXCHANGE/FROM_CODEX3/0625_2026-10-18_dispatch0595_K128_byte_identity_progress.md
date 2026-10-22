# Codex3 0595/0617: K128 saved-component byte identity and timing

date -u: Sun Oct 18 20:06:57 UTC 2026

TESTED PASS at K128 on the pinned saved C4R3 rotation component: all table arrays and order1/order2 jet arrays at218 probe positions preserve dtype, shape and direct bytes; record and state digest match. This is component replay with TEST_ONLY certificates and production_admissible=false, not a scientific launch. No production source changed.

| Worker cap | Cold-build wall s | Total CPU s | Wall speedup | CPU ratio to serial |
|---|---:|---:|---:|---:|
| 1 | 233.695 | 230.237 | 1.000 | 1.000 |
| 2 | 140.638 | 222.214 | 1.662 | 0.965 |
| 6 | 88.094 | 242.518 | 2.653 | 1.053 |
| 12 | 75.279 | 260.836 | 3.104 | 1.133 |

One sample per variant; ambient load and CPU timing variability apply. Timed cold-build wall includes pool creation/teardown and native assembly; total CPU includes reaped children. Byte-comparison jets are outside build timing. Worker caps and per-pass PID participation do not prove simultaneous concurrency. Maximum observed parent RSS2,409,627,648 bytes.

K256 is running serial→2→6→12 sequentially, followed by the configured VECLIB6 fresh-child comparison. Compact combined-harness validation passed; independent source/record review passed58/58 accounting checks without a new numerical rerun. Thread status determines pass/fail, not shell exit0.

UNTESTED: K256 outcome, saved-input thread-cap determinism, production adoption, and KHI extrapolation. Those remain pending the final0595 report. No cache savings are added to overlapping process savings. No targets, protected runs, or scientific launches. Minute inbox polling continues.

Byte pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K128_V001/SUMMARY_V001.json` — SHA256 `3ecfcbd2ec0a50268806ad76d27f442dce5166786b4fce3aa5e6418b0c4e6b60`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/MEASUREMENTS_INTERIM_V001.json` — SHA256 `caf3b9b8c37a1b379f0d771be19cb8e4ef6854b78d0dfefb828d7a22d7135199`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v002.py` — SHA256 `f1daa12e71418cd565188b1760345b7c0b8c78c5705589e0918e5edf6d20e8c7`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v004.py` — SHA256 `56e08972a4edd329975e7adca96ae8924aa548354cb7db9d3b63af3f03a2e645`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v007.py` — SHA256 `fa1ee0531243773a7dc4bfaa35d9ac5cdf1f127ce7929a82a45afaf1a2e46629`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K256_V001/INPUTS_V001.json` — SHA256 `daf95df6d8d3f20582a786da1e0359e695dfa703a9e9cac96e2ce1c5cee57988`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_combined_cx3/REVIEW_CX3V001.md` — SHA256 `27cb2fa432b22eb2149aae715fd7b2e333d498cfb8d165e468d8d040631c510f`
