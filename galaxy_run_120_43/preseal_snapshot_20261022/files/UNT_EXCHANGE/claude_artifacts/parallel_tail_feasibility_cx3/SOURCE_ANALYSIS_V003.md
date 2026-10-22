# 0595 source dependency analysis, selected prototype and limits

`date -u`: Sun Oct 18 20:18:59 UTC 2026.

**TESTED source inspection.** Numerical verdicts belong to the separately sealed per-run result and summary records. This source note replaces the historical blocked-execution status and hypothetical projections in V001 and the interim completion/thread-repetition wording in V002. It does not claim future measurements. No production driver or numerical module is modified.

## Independence and exact arithmetic order

| Work | Independence | What must stay unchanged for a bitwise test |
|---|---|---|
| `StarsProfile.radial_transform`, original256-frequency batches | Each batch writes a disjoint output slice. Component and doubling-pass accumulators are separate. | Compute global kmax once; use the same full-profile `_nodes` for every batch; preserve256-row batch boundaries, final short batch, Bessel argument shapes, GEMV shapes, component order and each `+=`. Compute one global doubling certificate and exact-key cache entry. |
| Gas radial factors by annulus | Each annulus produces four independent columns before selecting the present columns. | Keep the full frequency dimension, quadrature-node ordering, four-column GEMM shape and original column ordering. Splitting frequency rows changes a BLAS matrix dimension and needs independent proof. |
| Gas vertical factors by column | Each column's complex exponential transform is independent. | Keep its complete element order and full kz vector; concatenate columns in present-column order. |
| Main tail quadrature blocks | Source contractions, corner slices and each block's ring/shell contributions can be computed independently. | Retain `_block_rows(nz)` boundaries and all original GEMM shapes. Return each raw per-block increment; add ring and shell increments in original increasing s0 order. Concatenate corner slices in that order. Do not sum partial sums per process. |
| Shell grouping | A shell receives contributions from many original blocks. | Repartitioning by shell or reducing per-process shell totals changes floating-point addition order. Preserve each original `np.bincount` and serial block addition. |
| Evaluation-radius partition | Mathematically independent ring rows. | Changing the number of GEMM output rows can select another BLAS kernel. It also duplicates source contractions, shell and corner work if implemented as repeated U.build calls. Mathematical independence alone is not bitwise proof. |
| Spherical residual | Each original4096-entry slice writes disjoint A values; shell contributions overlap. | Preserve4096-entry boundaries, `einsum` operands, original element order and serial shell addition after each slice. |
| Jet points and on-demand corner tables | Different points/radii have independent values. | Preserve per-point azimuth/harmonic/reduction order; caches affect cost and diagnostics, not intended values. Any cold/warm equivalence still needs bytes evidence. |

Shared mutable state is limited mainly to the stellar exact-k cache and certificate list, provider call counters, TailState's LRU evaluation caches and diagnostics. Processes should keep local providers and scratch arrays. State digest includes the record plus every named array's dtype, shape and bytes; provider counts and timing diagnostics are excluded. Matching just a final scalar or a few jets is insufficient: all arrays, records and jets must be compared.

The main block splitter has a large communication cost. At the cited K256 rotation shape (72 radii,102400 positive-kz nodes), one complex128 ring increment is72×3×102400×16=353,894,400 bytes. Returning that for each original block would move hundreds of GB over the complete build. A bounded queue limits peak memory but does not remove this traffic. Reducing blocks locally would violate the proposed exact addition order. A future source-integrated implementation could use shared read-only factors and disjoint output ownership, but shape-preserving BLAS and reduction tests are then essential.

## Selected implementation and timing

The selected out-of-tree prototype is parallel_stars_prototype_cx3v002.py. Each spawned task evaluates one unchanged 256-frequency stellar batch using the original full-grid kmax, nodes, component, and doubling multiplier. The parent consumes results in original batch order, preserves each slice += and computes the native global doubling certificate before filling the original exact-k cache. The unchanged native v002 build then performs all gas factors, source contractions and ring/corner/shell assembly. No partial ring reduction or numerical source patch is used.

The benchmark whole-build timer starts before fresh roster creation and includes grid/preparation, worker creation and teardown, and native build. Total CPU is self plus reaped-child CPU. Direct state/record/digest and order1/order2 jet comparisons occur after the build timer and are separately timed. Measured task PIDs are reported per component/doubling pool; N is a pool cap, not measured simultaneous worker activity. Native task counts also bound possible utilization.

The selected combined runner v007 compares a fresh process configured VECLIB_MAXIMUM_THREADS=6 with its retained same-invocation serial1 build. The separate selected thread runner v003 performs one fresh configured1 child and one fresh configured6 child for each saved K32/K128 case. Each child sets its environment before importing NumPy. The remaining numerical thread controls stay1; the emitted environment records contain the five PROTO.THREAD_KEYS, while BLIS is additionally fixed1. Thread child build timing excludes interpreter startup/imports, jet evaluation, and IPC. The whole experiment elapsed time is separate. Actual Accelerate thread utilization is not instrumented, so finite byte equality is not a universal determinism claim.

Scratch estimates and observed process RSS are checked; these are not OS hard allocation limits. Parent/child peak records may precede later IPC allocation. All requested variants remain constrained below8 GiB/process. One registered stellar component and rotation-stage grid are exercised; other stage/source classes and spherical residual need separate byte evidence.

## Cache interaction and follow-on scope

At this direct directory inspection, driver_r6 BUILD-prefixed names are []. The v003 module is inspected as source only. Its optional star cache includes numerical/config/source/provider/runtime custody. Prepopulating the native cache causes BYPASS_IN_PROCESS_CACHE, so a future integrated process splitter must execute inside the cold-cache miss path before publishing a persistent entry. The current cache store uses rename and temporary-directory cleanup, which conflict with this session's immutable-write rule; no persistent-cache execution is performed. Cache hits and parallel cold-star savings overlap and must not be added. This feasibility result neither adopts r6 nor delays the r5 seal.

A future r7 successor would add an optional cold-star process-count parameter, default1; preserve original batches, shapes, component/doubling/addition order, certificates and BLAS1; bound outstanding tasks; and propagate new source/driver pins. Estimated engineering cost is one narrow implementation pass and one independent source/byte-replay review pass plus measured replay time, not a promised elapsed duration. Cache integration, failure behavior, parameter refusals, other saved stage/source classes and outside-feature parity require review before adoption.

The final KHI projection must use measured process ratios only after byte validation, scale only the inherited rotation-equivalent cold-build term, and label the full-call transfer UNTESTED. The prior A89 full-call hours are a component-based model using measured components, not a measured complete KHI run. No extra cache saving is subtracted.

## File pins, SHA256 from bytes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v002.py` — `f1daa12e71418cd565188b1760345b7c0b8c78c5705589e0918e5edf6d20e8c7`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/benchmark_tail_cx3v007.py` — `fa1ee0531243773a7dc4bfaa35d9ac5cdf1f127ce7929a82a45afaf1a2e46629`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/threading_tail_cx3v003.py` — `78d54f9bfd6b60b2b9f8405ecdb0e0d3372263a4a2de0ebf06d6eb65ee7134cc`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py` — `2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/uv_tail_source_roster_c2v001.py` — `4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/posix_libm_bessel_jn_provider_c2v001.py` — `d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py` — `e733eb1ebfe2137a6f58d0e35caa345525756e3896ca729c1ba15a39204c7155`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json` — `3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/tools/assemble_timing_v003.py` — `a154e3b22c25bc9fb4c6c95255c081d75981f683dc4e44355b781b27f6a9875d`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0613_2026-10-18_all_lanes_taskpolicy_preferred_not_required.md` — `82c214dfe8729603ccea43f803cc091f5b484f4b2fa09147ea57955a1a0f1377`.
