# Independent 0595 source review

date -u: Sun Oct 18 19:51:49 UTC 2026

**PASS_WITH_FINDINGS for the bounded source review.** No blocking arithmetic discrepancy was found. Numerical bitwise equality, speedup and per-process peak usage are UNTESTED independently here.

The pinned source preserves full-grid kmax-derived nodes, original 256-row Bessel/GEMV shapes, component and doubling order, per-slice additions, native cache key/certificate effects, and unchanged native table assembly. The comparator covers every saved table and returned order-1/order-2 jet key at the supplied probes, including dtype/shape/bytes, record and state digest.

Timing uses full build wall and parent plus reaped-child CPU; pool creation/teardown are included by the outer timer. Jet comparisons are outside build timing. The historical 353,894,400-byte ring-increment and optimistic projection arithmetic check out; the projected cache-sensitive fraction is not measured parallel work.

## Findings and limits

- NOTE_N_CONCURRENCY: max_workers=N is a cap. Global unique PIDs union separate component/pass pools. Use per-pass PID and block counts; do not infer simultaneous active N.
- NOTE_MEMORY: Scratch estimate and after-allocation RSS checks do not enforce a hard memory limit before _nodes/provider/allocation. Only observed bounded runs can substantiate per-process usage; v002 threading adds missing parent/jet checkpoints.
- NOTE_THREADING: VECLIB_MAXIMUM_THREADS=6 and backend metadata are configuration evidence, not measured six-thread activity or universal determinism.
- NOTE_CACHE: No r6 persistent-cache behavior is exercised; prepopulation bypasses its star-store path. Cache-enabled integration requires separate source/build review.
- NOTE_HISTORY: SOURCE_ANALYSIS_V001 predates A95 and numerical execution; its blocked status must remain historical, not the final current verdict.

The builder acknowledged the reporting limits and supplied threading v002 with post-jet/post-receive/post-compare RSS checks. That successor is included in this source review. No hard preallocation bound or r6 adoption is inferred.

This review did not import or execute the tail/prototype/benchmark modules, open saved-state arrays, duplicate a C4 replay, read protected metadata or NGC targets, or launch scientific work. The 31 predicates are TESTED static/accounting checks, not numerical tests.

## Byte pins

- prototype: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v002.py — sha256 f1daa12e71418cd565188b1760345b7c0b8c78c5705589e0918e5edf6d20e8c7
- benchmark: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v004.py — sha256 56e08972a4edd329975e7adca96ae8924aa548354cb7db9d3b63af3f03a2e645
- threading: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/threading_tail_cx3v002.py — sha256 dbe34a571a7c3ba07bce6c921bb8c33be1ba7baa60caf2dc4d0722493772e747
- analysis: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/SOURCE_ANALYSIS_V001.md — sha256 9d848522e32f1fc1c33e87ad541a40e2bd45cebf29462f0b9a1607d4a73d79b8
- native: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py — sha256 2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54
- roster: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/uv_tail_source_roster_c2v001.py — sha256 4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2
- provider: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/posix_libm_bessel_jn_provider_c2v001.py — sha256 d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171
- r6: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py — sha256 e733eb1ebfe2137a6f58d0e35caa345525756e3896ca729c1ba15a39204c7155
- timing: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json — sha256 3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925
- dispatch: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0595_2026-10-18_codex3_parallel_tail_build_feasibility.md — sha256 72c05307e6011d8e410c560429c83b1dcb0f752df23f9e5364d92692070f99dd
- waiver: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md — sha256 82c214dfe8729603ccea43f803cc091f5b484f4b2fa09147ea57955a1a0f1377
- Results: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/independent_cx3/SOURCE_REVIEW_RESULTS_CX3V001.json — sha256 c6f1ea9912bf644fe99ea9ccea9c4a7af6e63aaa45cd3cd2c56e8f39dd6a789e
