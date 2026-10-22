# 0595 parallel cold-tail feasibility — source analysis and execution block

`date -u`: Sun Oct 18 18:48:41 UTC 2026.

Status: **TESTED source inspection and background-policy preflight; numerical feasibility UNTESTED / BLOCKED.** The exact preflight `taskpolicy -b /usr/bin/true` exited 70 with `taskpolicy: setpriority(): Operation not permitted`. No numerical build, worker pool, target read, protected-run read or fallback execution followed. There are no measured speedups from this lane. All numerical comparisons requested by 0595 remain outstanding.

The r5 library source pin is 2026f2b6 and its driver pin is b5cc62af. The r6 module exists at e733eb1e, but no `driver_r6/BUILD*` existed at the inspected time. Inspection of that module is source-only and does not establish its adoption or completed build evidence. This work does not delay the r5 seal; dispatch0601's no-delay rule remains applicable.

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

## Prepared prototype — UNTESTED

`parallel_stars_prototype_cx3v001.py` is an out-of-tree, inert prototype. It dispatches the existing256-frequency stellar batches to N spawned processes, gathers batch results in serial index order and populates the native exact-k cache/certificate. It then calls the unchanged native U.build, preserving its source contractions and ring/corner/shell reductions. It includes an all-array byte comparator plus order1/order2 jet comparisons, prescribed interpreter/environment guards, bounded outstanding work and a conservative scratch estimate. Neither execution nor syntax validation was attempted after the background-policy refusal; it is not reviewed production code.

This split targets a major cold cost while returning small vectors rather than partial ring tables. It leaves `_nodes`, gas factors, source contractions and native assembly serial. Worker task CPU is recorded separately; a future benchmark harness must additionally measure total child-process CPU, including pool initialization and teardown, and total wall time. No speedup can be claimed until those measurements and byte comparisons pass.

The v003 persistent cache interacts with this prototype: `_stars` sees the populated native cache and returns `BYPASS_IN_PROCESS_CACHE`, so that call would not publish a persistent stars entry. An r7 integration should put parallel cold computation inside the native cold-cache path, preserving certificate/store behavior. The current v003 store also calls `os.rename` and removes private temporary directories. Those operations conflict with this session's no-renames/deletion rule; cache-enabled execution is not permitted here without an explicit exception. `table_cache=None` does not exercise storage.

## Provenance and next calibration

No source-state arrays have been opened for this study. The first proposed workload is a newly saved, explicitly synthetic registered-profile fixture with declared test-only certificates,72 evaluation radii and controlled rank. It must be labeled synthetic rather than evidence for production source cost. A second replay can use the permitted C4R3 rotation arrays named in the already-pinned timing source, after exact resolved paths and hashes are sent to the parent. No generic saved-state loader is needed or authorized merely because it exists. Any indirect C5H/UVT/target path must refuse.

After the background-policy block is resolved: calibrate K32 serial first; then run N2/6/12 sequentially against the same saved inputs, rather than overlapping benchmark cases. Retain only array hashes/byte-comparison summaries and compact timing records. Increase to K128 after measured memory and cost are known. K256 remains conditional on machine load. The requested VECLIB1-versus6 experiment is separately deferred pending the parent's instruction about the binding BLAS1 constraint.

## Cost and projection — UNTESTED

The cited timing summary reports r5 rotation K256 cold1275.90 CPU seconds and same-star warm358.51 CPU seconds. These are Claude2's existing measurements, not this lane's measurements. Their difference917.39 seconds is only an approximate cache-sensitive cost, not a profile of this proposed split. If that entire difference parallelized perfectly and all remaining cost stayed fixed, ideal cold CPU-equivalent time would be817.21 seconds at N2,511.41 at N6 and434.96 at N12: ideal speedups1.56,2.49 and2.93. Startup, contention, serial node construction and memory traffic can reduce or erase those gains.

An illustrative KHI scenario using the existing cache-saving budget gives `T(N)=T_r5-S_cache*(1-1/N)`. With the summary's expected7.84h and1.83h cache saving, this gives6.93h/6.32h/6.16h for N2/6/12; with upper13.86h and2.80h,12.46h/11.53h/11.29h. **These are UNTESTED optimistic scenario calculations, not measured projections of the prototype:** caching removes more than stellar transform work, warm builds need no such work, and critical-path contention is not modeled. Cache and parallel savings cannot simply be added. The only accepted current timings remain those in the cited summary.

Recommendation: keep the no-delay r5/r6 seal decision intact. Resolve the background-policy block, test the small stellar-batch split first, and only commission r7 integration after actual bitwise and timing results. A narrowly integrated r7 would add a bounded cold-stars process map with preserved nodes/batches/certification, an explicit process-count setting in the driver, unchanged BLAS1, and successor pins/custody. Review obligations include exact all-array/record/jet comparison on saved inputs, source-dependent cache isolation, failure cleanup consistent with policy, process-count refusal cases, memory limits and outside-feature parity. Estimated engineering/review cost is1–2 focused build/review passes plus the measured benchmark runtime; no reliable wall-clock completion estimate exists while execution is blocked.

## File pins from bytes

- Dispatch0595: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0595_2026-10-18_codex3_parallel_tail_build_feasibility.md` — SHA256 `72c05307e6011d8e410c560429c83b1dcb0f752df23f9e5364d92692070f99dd`.
- Dispatch0601: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0601_2026-10-18_all_KHI_measured_r6_no_delay_rule_A89.md` — SHA256 `1f6421564922755445ae3b5c558242f1e89995f49141e60db4d436e77d99b019`.
- r5 driver: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` — SHA256 `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`.
- v002 module: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py` — SHA256 `2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54`.
- Roster source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/uv_tail_source_roster_c2v001.py` — SHA256 `4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2`.
- Provider: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/posix_libm_bessel_jn_provider_c2v001.py` — SHA256 `d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171`.
- Pending v003 module: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py` — SHA256 `e733eb1ebfe2137a6f58d0e35caa345525756e3896ca729c1ba15a39204c7155`.
- Existing timing source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/tools/kbig_build_timing_c2v003.py` — SHA256 `d14b828fbb333947b5b8911c2c230edca4ff1749901fc77698ce4bef65ffbf09`.
- Existing timing summary: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json` — SHA256 `3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925`.
- Block evidence: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/BLOCKED_V001.json` — SHA256 `2c2a3c41cae5117f97e54711862fd37e14971770b9ad0ae5e87969882274e7b0`.
- Unexecuted prototype: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_tail_feasibility_cx3/parallel_stars_prototype_cx3v001.py` — SHA256 `3b92bb26dae611af928dbc7f935cb808a364a8bbc634f9ce2a99c29f1f9c3a09`.
