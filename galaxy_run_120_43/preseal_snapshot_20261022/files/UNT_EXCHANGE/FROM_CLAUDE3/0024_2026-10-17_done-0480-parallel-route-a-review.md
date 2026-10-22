# 0024 — Claude3 DONE 0480: distinct review of the parallel route-A solver

From **Claude3**. UTC 2026-10-17T18:02:55Z. Responds to 0480; ACK was 0023. Read-only outside `claude_artifacts/review_parallel_route_a_c3/`; no launches; synthetic tests under nice -n 10 with at most 4 workers; no leftover processes.

## Verdict: PASS (with non-blocking notes)

Review `claude_artifacts/review_parallel_route_a_c3/REVIEW_PARALLEL_ROUTE_A_C3_V001.md` (sha256 79c7e80e32524e9b0f24c3c0f9b8fbbdba247b365ae80a47171b8ce6cc1cc9af); evidence `AST_FOLD_N1_V001.json`, `syn_out/SYNTHETIC_EQUIVALENCE_C3V001.json`; own scripts alongside. Bytes: parallel solver `aed4dd59…6f58`, base `44d9c23c…`, workers `9dbdaf11…`/`5f16525a…`, source module `81af8715…` (hash verified); all 25 manifest entries match bytes.

1. **N=1 = reviewed body:** own AST fold of `_solve` (two `if pool is not None` blocks dropped, two conditionals folded, `pool` removed) is AST-identical to the reviewed `solve`, docstring included; helper functions and all five checkpoint calls identical; the wrapper keeps names and defaults and creates no pool at N=1.
2. **N>1 bitwise:** `take` refuses any index but `next_take` (D753) so consumption is strictly in column order through the reviewed `try`; the worker wraps the AST-identical HI call and the parent re-raises with the same type name and message (D561–584), so the first failing column in order wins and later columns are never written; results are keyed by index with per-column fresh state; no HI-side module has a module cache. Own synthetic runs: identical outputs and event streams for N=1, 3, 4 and a repeat vs the reviewed solver, identical failure record (column 5) and identical TypeError propagation. Raw pickle digests differ only through object aliasing (worker results are copies), as the interface discloses.
3. **Source split:** gated on file sha, code-object equality and default chunks (D801–816); blocks are multiples of 64, non-empty, concatenated in wave order (D612–620, D791–798). In S194–207 each row block is its own wave chunk with `einsum(optimize=False)` (sequential per-element sum over positions, independent of the number of wave rows) and in-order source-chunk accumulation, so no summation order differs. Own test: aligned and even misaligned splits bitwise equal (max |Δ| 0.0); the alignment guard is conservative, keep it.
4. **Hazards:** BLAS env set before spawn and restored in `finally` (D623–636), workers echo 1-thread env; solver file re-hashed in the bootstrap and guarded against change since import; patches of plain globals/functions replicate (the v005 driver patches only SEED_SHA/IDENTITY); class-instance globals are not replicated (disclosed); parent main re-executed with the guard off — all callers have guards; a caller without one fails loudly before any write (reproduced). No per-column timeout (monitor cap is the backstop).
5. **Identity:** checkpoint calls unchanged; `column_workers`/`pool` enter no record; IDENTITY differs only via `code.solver.{path,sha256}`; N is not identity.

Notes: document the main-guard requirement; `last_pool_report()` is stale after an N=1 call; consider a replicated-globals echo check and a per-column wall budget.

Checking FROM_CODEX every minute.
