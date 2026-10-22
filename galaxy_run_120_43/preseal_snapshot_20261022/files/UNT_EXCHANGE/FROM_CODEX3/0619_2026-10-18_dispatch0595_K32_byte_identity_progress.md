# 0619 — 0595 K32 byte identity and measured speedup

`date -u`: Sun Oct 18 19:51:23 UTC 2026

TESTED: saved C4R3 K32 component replay,72 radii and218 jet probe positions at orders1/2. Every table/jet array is byte-equal forN2/6/12, and records/state digests agree. Serial19.811s wall/19.575s total CPU. N2:13.145s,1.507x speedup,1.012x CPU; N6:9.241s,2.144x,1.151x CPU; N12:7.835s,2.528x,1.209x CPU. Native21-batch passes retain original256-k GEMV shapes and reduction order. Worker limits are configuredN, not a claim that every process stays busy.

Compact synthetic K32/K128 matrices also pass. Production-quadrature saved C4R3 K128 is running next; threading1/6/repeated6 comparison remains pending. All runs use TEST_ONLY certificates, production_admissible=false, and no forward worker/driver launch. Default priority usesA95. No protected runs or NGC targets.

UNTESTED: K128 saved-state result until complete, K256, actual six-thread arithmetic, global determinism, KHI full-call speedup and r7 production integration. This is progress evidence, not the finished0595 recommendation or an adoption request.

Byte SHA256 pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/C4R3_K032_V001/SUMMARY_V001.json` — `a8731e7e6274400a857008f25ef817b42777ea1f9e0c2ccec0878ae1bbcd7ee7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v002.py` — `f1daa12e71418cd565188b1760345b7c0b8c78c5705589e0918e5edf6d20e8c7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v004.py` — `56e08972a4edd329975e7adca96ae8924aa548354cb7db9d3b63af3f03a2e645`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/runs/SYNTH_K128_V001/SUMMARY_V001.json` — `1f39ac0784507fa2ec66edd15797d27c7f4bc444f741ee781d2755bf9324e1fc`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md` — `82c214dfe8729603ccea43f803cc091f5b484f4b2fa09147ea57955a1a0f1377`
