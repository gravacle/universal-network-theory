# DOUBLING_MERGED_C3V001 independent review — PASS

date -u: Sun Oct 18 18:56:01 UTC 2026

**TESTED: 48/48 assertions.** Record `ea48ac2bc429a1b6f7ae9b2cf96964a42bbedfd64afab21f724259114d8b0f7b` is admitted by the actual r11 `evaluate_gate` at comparator SHA256 `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`. This verdict covers the merged doubling arithmetic and its gate admission.

The independent script strictly parses and byte-verifies all ten record inputs, then uses scalar loops to recompute both halves. It does not execute the merged producer or its underlying scientific producers.

- **DDO:** all twelve row changes at each K_big 128 and 256 match the merged record bitwise. Maxima are 3.7969627442180354e-13 and 4.671818487622659e-13 of tau; the merged maximum is **4.671818487622659e-13**, below 1/20. State hash, row identity/order, radii, state speeds, positive tau, M_s128, configuration pins and the order+4/width-halving relation agree.
- **NGC:** recomputed max absolute lnN(z=0) change and max dL change over heights +/-10, +/-20, +/-30 kpc are both **0.0**. The ratio is **0.0 theta**, below 1/20, with the registered operator and theta=3.3657664138980042e-09. The 100 rings, 32 azimuths, nine stored heights, radius ordering and kept-reference identity agree. Coarse/fine build digests differ and fine node counts increase. All 28,800 stored lnN entries are bitwise equal. This is equality of stored rounded values, not a claim of zero continuum error.

The actual r11 gate uses the unchanged record and actual V002 DOUBLING producer/record registration, with an explicit scoped case context P128 and M_s128. V003's DOUBLING registration is identical. r11 validates registry syntax with `verify_bytes=False` to scope this lane to DOUBLING; its `evaluate_gate` still hashes the actual DOUBLING producer bytes. Full registry closure belongs to the parent’s separate review.

Ten newly written synthetic records exercise over-threshold DDO/NGC maxima, foreign state/operator, M_s64, missing/duplicate K_big, invalid numeric types/ranges and contradictory verdicts. Their test-only record hashes are rebound in owned context so registry rejection cannot masquerade as semantic rejection. All fail their intended gate checks. Removing record registration and changing the context to M_s64 also refuse. No broader ADOPT_TAIL decision or full case-block validation is asserted.

**UNTESTED:** regeneration of the underlying field/spectrum calculations, reconstruction from saved C4R3 state, actual run/receipt custody and full scientific acceptance. The task was satisfied from permitted stored artifact outputs; no protected run tree was opened, stat-ed or listed, and no observed/target NGC velocity was read. No blocking finding in the reviewed scope. The stored DDO proxies are static replay outputs, not new production calls.

Guard installed before comparator import: open/stat/lstat/readlink/listdir/scandir; protected-root constants replaced with owned surrogates. Zero protected-access attempts and zero scientific launches. Prescribed Python -I -B, stdlib/NumPy, single-thread settings; `nice unavailable (sandbox); 0514 waiver`. No network or overwrites. All consumed source/input byte pins were rehashed after checking and remain equal.

## Evidence and cited bytes

RESULTS_CX2V001.json contains each assertion, raw owning-gate outcomes and the per-row recomputation. HASHES_CX2V001.txt also covers every owned synthetic file.

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0605_2026-10-18_codex2_crosscheck_seal_records_while_waiting.md` — SHA256 `9c66a457d38debc1646c3a45aa2dd64bbf0164a93a62a2ec19d32662c5b61635`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/assemble_k32_records_cxv002.py` — SHA256 `23a45a7eb302acbd81c5bd618294817d637fbfd759dc37610255f1282140b097`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/CUBE32_STORED_V001.json` — SHA256 `c3470be5d92b918fcfee1c495a087e9c038a94900ce71fb191f513bad07fddde`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K16_RECORDS_COMPLETE_V001_NQ.json` — SHA256 `060de86d4004e33a801f7707a3e4776d7ab02ef34be83a2c2f1acdbae2163c55`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_PARTIAL_V005_NQ.json` — SHA256 `ed837c49e012d6aedf300d1211ea84b4fa509d5cb2cb5b38e2eb948dd37204d8`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/NQ32_FINE_STORED_V001.json` — SHA256 `69b054d4ae06edf671e2a741fe13fb1db05a2c39e04b44066ef462efff5b35a9`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/DOUBLING_MERGED_C3V001.json` — SHA256 `ea48ac2bc429a1b6f7ae9b2cf96964a42bbedfd64afab21f724259114d8b0f7b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V002.json` — SHA256 `3b38c794a1a434537d16cc039beeffe8b91dde3c3713401031c83c75f86277e8`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V003.json` — SHA256 `6b6f76ae301d75878156e7b8f2641215d215ada9017dbcba3b805a99589701a3`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/scripts/doubling_merged_c3v001.py` — SHA256 `92603482e448ba3fb82a47391106fa44e9c5b26994817819624605879eae0b9b`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/doubling/RESULTS_CX2V001.json` — SHA256 `1e0b95aae2e7f9904ff7a40cec2d09af278d63543a6632e29dd393d193cede4a`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/doubling/check_doubling_cx2v001.py` — SHA256 `a449a1467ed9f41498f16af581c42ac09ddd891fea5e64d9cd679b2bf57d15e9`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v001/tools/certs_common_c2v001.py` — SHA256 `1946a394c0c36754c0fb9fbc39fb9e2243e042dfcab977c0d4c360313aa5ec99`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/doubling_v001/DOUBLING_K128_V001.json` — SHA256 `ec169d43cdd116ee663bcbf08719c0d70706f4f2501155701a27dc6a79fb6439`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/doubling_v001/DOUBLING_K256_V001.json` — SHA256 `1ba4773d9ccc927bc0499f9e57bc6ad3c72d0ff1be1afaa035c910246eb57ab6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/doubling_v001/out/PROXY_C4R3_KB128_dbl_MS128_V001.json` — SHA256 `0c358cdb558fa4e39954a30b7891344aa0f1797be78e4f184540ecbd78a777de`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/doubling_v001/out/PROXY_C4R3_KB128_prod_MS128_V001.json` — SHA256 `603f607672faca02c2d2a4eada091560060f7fd14cb6fec703b657aabbd400c0`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/doubling_v001/out/PROXY_C4R3_KB256_dbl_MS128_V001.json` — SHA256 `c3aac6b6fec6b0c7b40a82219b0b2682978a774f0991751a2961fa3b22c3c88f`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/doubling_v001/out/PROXY_C4R3_KB256_prod_MS128_V001.json` — SHA256 `782a7c0259a6566b0304b2a844b7b920ceeaa0c7d117e10fc1091b03a6934cdf`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/doubling_v001/tools/doubling_proxy_c2v001.py` — SHA256 `a0b2dc396bc955814229207f04e7bd35c5e163caf62743508aaf2091a58d00c3`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py` — SHA256 `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`.
