# Parent source review: combined K256/thread harness successor

`date -u`: Sun Oct 18 19:59:06 UTC 2026

TESTED by source diff: v007 retains v004 process-matrix arithmetic and timing, then optionally spawns a fresh process configured with VECLIB_MAXIMUM_THREADS=6. The same-invocation cold serial1 state remains available for direct dtype/shape/byte, record and digest comparisons. The private spawn environment flag is restored; the parent remains under the BLAS1 guard before/after the optional comparison. Thread work starts only after the process matrix. Protected-input, exclusive-output and observed-memory checks remain.

Parent found an aggregate reporting defect in unexecuted v005: top-level status remained PASS even if optional thread comparisons failed. v007 propagates that failure and explicitly distinguishes native child build timing from process-matrix outer timing and total study elapsed. Both requested corrections are present in the inspected bytes. No further blocking issue observed in this bounded delta.

UNTESTED here: numerical execution of v007, true six-thread activity, universal determinism, hard memory enforcement and r6 cache behavior. Builder must validate the harness on compact inputs before K256. CPU/wall timings are single samples under ambient load, and thread-child timing excludes interpreter/import/jet/IPC costs. Earlier independent31-predicate source review applies to its pinnedv004/v002 objects; this note reviews only the successor delta.

Byte SHA256 pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v004.py` — `56e08972a4edd329975e7adca96ae8924aa548354cb7db9d3b63af3f03a2e645`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v005.py` — `d0d6921b6d823fdb01767b38bf28809141141c5c2839285a05435e7bf2ca780a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v007.py` — `fa1ee0531243773a7dc4bfaa35d9ac5cdf1f127ce7929a82a45afaf1a2e46629`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_cx3/REVIEW_CX3V001.md` — `0ac6837d9599fd40f3e320321681788f85da27609e84f30c53697ef311b968d4`
