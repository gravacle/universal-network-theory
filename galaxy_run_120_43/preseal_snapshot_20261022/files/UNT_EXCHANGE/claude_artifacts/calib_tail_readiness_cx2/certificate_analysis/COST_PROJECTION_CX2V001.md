# Cost projection — tail components, not complete calls

UTC: 2026-10-18 12:11:35 UTC. TESTED extraction/arithmetic from saved timing records; complete production cost UNTESTED.

| K_big | A cold build s | A warm build s | B rotation cold s | A later lapse pair ms |
|---|---:|---:|---:|---:|
| 64 | 79.32 | 31.96 | 60.62 | 0.292 |
| 128 | 284.82 | 103.43 | 232.75 | 0.577 |

S13 builds the initial source, then one next-source state per completed route-A iteration. begin_iteration reuses that pending state. Thus a cold uninterrupted call has I+1 builds, modeled as cold + I*warm. S17's K128 initial-source sample is 260.28s cold / 76.87s warm, compared with 284.82/103.43 at saved iteration6; the latter is used below, without claiming an upper bound.

| K_big | Completed A iterations | Cache-miss calls | A build subtotal minutes |
|---|---:|---:|---:|
| 64 | 6 | 1 | 4.52 |
| 64 | 6 | 7 | 31.63 |
| 64 | 6 | 12 | 54.22 |
| 64 | 32 | 1 | 18.37 |
| 64 | 32 | 7 | 128.57 |
| 64 | 32 | 12 | 220.41 |
| 128 | 6 | 1 | 15.09 |
| 128 | 6 | 7 | 105.63 |
| 128 | 6 | 12 | 181.08 |
| 128 | 32 | 1 | 59.91 |
| 128 | 32 | 7 | 419.37 |
| 128 | 32 | 12 | 718.92 |

Per call add n_B*60.62s (K64) or n_B*232.75s (K128) as a **rotation-stage build proxy only**, plus tail evaluations, kept-cube computation, certificates, serialization, stage setup and I/O. Exact n_B is not yet available from an executed candidate plan. The 7-call and 12-call rows are wave scenarios; substitute actual uncached calls from the Jacobian/exploration plan. Neither row is a measured whole wave. For unequal calls, sum each call's I and stage costs. Do not divide serial controller/build terms by eight: workers8 parallelizes column solving; the measured build is in the controller.

Saved route-A iterations have roughly 60,000 metric calls each. Warm pair costs imply roughly 17.5s/34.6s of additional pair CPU per 60,000 calls, before approximately 18ms first-line setup, jets, monitors, IPC and parallel efficiency. This is only a workload illustration; exact invocation/cache counts are unmeasured. Eight-worker aggregate memory is unmeasured; measured single-build RSS cannot be multiplied into a validated whole-run bound. S15/S16 report about 1.61/2.90 GB process peak; S18/S19 about 0.83/1.27 GB. The module's smaller memory estimates omit important temporaries/process duplication.

No forward, route-A or route-B launch occurred. No forbidden run was opened. The coordinator must set the production K_big and operational caps after actual call-plan accounting and admitted production evidence. These projections do not authorize launches.

Timing/source pins:

- S13_A_controller: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001.py`, SHA256 `51d32e7b2b8c83c7544c24d64ea3161007fbec35769a64a869972efac055cb68`.
- S14_B_binding: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001.py`, SHA256 `7288a5d17976cc0267316e16f6a15aab2ca5c87d810c7d498f2a3787fe571651`.
- S15_timing_A64: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_a_KB0064_n6_V002.json`, SHA256 `34481edf97ffe489676c3c2863554f02c5f38a17ae8b85ec079f1e0422f2e7c6`.
- S16_timing_A128: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_a_KB0128_n6_V002.json`, SHA256 `e4e6d217832697a360141aca382b1e169b5af73e186f04a31dfcac50bdbdac5b`.
- S17_timing_A128_initial: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_a_KB0128_n0_V002.json`, SHA256 `24701f38de4f180c44396cf1530f890eb07336938fe577a010dc20d52a870122`.
- S18_timing_B64: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_b_KB0064_V002.json`, SHA256 `02ddb9be18ef356b9ed901744f135cbb271b6770189615fe9658bbbe660f0ce1`.
- S19_timing_B128: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_b_KB0128_V002.json`, SHA256 `0d1365b9a39b7d84223fd10b52eb779203d25acb337e092368f228f64eb32b7a`.
