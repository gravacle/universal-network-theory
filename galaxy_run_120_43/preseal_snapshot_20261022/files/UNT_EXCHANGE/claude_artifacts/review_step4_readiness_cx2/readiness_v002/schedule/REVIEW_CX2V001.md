# Step4 corrected schedule v003 — arithmetic delta

Sun Oct 18 21:18:56 UTC 2026

Verdict: **PASS for the isolated schedule/source arithmetic**, zero new blocking findings. TESTED 643/643 checks: 236 metric comparisons across 13 independently reconstructed rows; 40 static-memory calculations; 124 gate-summary joins; 24 boundary-summary joins and 24 wave-assumption checks; 168 saved predecessor reproduction assertions; three owned boundary/memory controls; four solo totals and the remaining pin/label/cap checks. These categories overlap in coverage and are not independent scientific validations.

The prior S-1 endpoint defect is closed. The selected pure producer scheduling slice counts offset >=172800 seconds. An owned two-wave fixture with starts at0,16,32 and48 hours within the second wave gives one inadmissible start under >= and zero under the predecessor > metric. The published24 campaign rows contain no start within one model tick of48 hours and no differing > versus >= count. The simulator explicitly counts late starts; it does not suppress them or terminate active calls.

The memory gate now applies to the first admission too. An owned fixture admits at exactly25% and reaches5% after the start; a first call below25% remains unstarted and hits the deliberately bounded synthetic timeout. New model constants are18.79 GiB for tail-ON route A and4.095 GiB afterward,9.7501/2.805 GiB for tail-OFF. Independent arithmetic uses those declared constants. Their empirical provenance through old run measurements was not re-audited or reopened.

Representative conditional projections (18 modeled cores,17 GiB background except where stated):

| Saved scenario | Hours | Minimum before admission | Minimum after start |
|---|---:|---:|---:|
| 11 headline E | 7.52 | 31.77% | 17.09% |
| 11 headline U_ADJ | 16.11 | 31.77% | 17.09% |
| 11 headline U_ADJ,48 GiB background | 18.42 | 25.43% | 10.75% |
| 9 sensitivity U_ADJ | 13.81 | 38.16% | 23.48% |
| 18 sensitivity U_ADJ comparison queue | 23.01 | 25.37% | 10.69% |
| 4 DIII U_ADJ | 7.77 | 69.29% | 61.68% |

The hypothetical cap6 static rows use max_route_b_calls_at_admission=-1 when even five concurrent route-A calls leave less than25% free. Their negative hypothetical post-start memory percentages do not describe an admissible start. Cap2/cap3 also permit post-start minima below25%; no post-start floor follows.

The independently calculated upper solo tail-ON duration is 8.752181563 hours. This still exceeds the inherited8-hour cap assumption identified by the prior review. This slice did not inspect or approve a new runtime cap/config. The model has no per-call wall/RSS/output-cap termination, failure, retry or root-review delays. The120 calls in21 waves and homogeneous processor-sharing costs are assumptions; actual adaptive behavior, memory pressure and performance remain UNTESTED.

The own scheduler uses dictionaries and reconstructs phases from permitted saved timing summaries; it imports no producer/driver. Only the producer Call/simulate AST definitions were selected for the three tiny synthetic controls; its main and loaders never ran. Exact source/input pins were stable. No protected run/target metadata, actual process, scientific simulation or network was accessed. Final corrected order documents and coordinator adoption remain pending outside this isolated-artifact review.

Evidence pins:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/v002_work/order/SCHEDULE_SIM_C4V003.json` — SHA256 `987801b258863e8be07497605c45e7112fcea5a9164f04e71b149852f7417150`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/v002_work/order/tools/schedule_sim_c4v003.py` — SHA256 `0b6b7db21e4c872fe7392c2bc9872af9bbdb7fec86adc2baae8277c2e49db19c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json` — SHA256 `3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/results/projection_c2v001.json` — SHA256 `cffa3150a2aac120bad1fdb045a93f645b938f76f22c3e8ff0bce56f387eaad2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/launch_order/work/SCHEDULE_SIM_C4V002.json` — SHA256 `2723042e704a04ae7dd90c7aeec848e210f2895bbeb6985823b11a864f22029b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/ARITHMETIC_RESULTS_CX2V001.json` — SHA256 `dc37f73cde412c5fcc236893912c3bd67f5b1f6cb89e32c9e1fc5b08fbc190ed`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/schedule/ARITHMETIC_REVIEW_CX2V002.md` — SHA256 `d8f7c3ee44893647c642d85419e0b30c960f3b5d4aab0ece05cb4fbc581f68fb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/DOCUMENT_REVIEW_CHECKPOINT_CX2V001.md` — SHA256 `70ed2e9f340d8af6786df2f3e3951dc33c8b076b28a4116a784556d5ffbe2205`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/readiness_v002/schedule/recompute_schedule_cx2v001.py` — SHA256 `f9e6b8bfebf042086ac99d03121a9aeefcd0662a52d32618ea43407a40eadbb3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/readiness_v002/schedule/RESULTS_CX2V001.json` — SHA256 `2d936af968c3680b0a46a1cee9118ea4aedc108fb6539e94c1058fafaa88f856`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_step4_readiness_cx2/readiness_v002/schedule/SUMMARY_CX2V001.json` — SHA256 `d747be1019d50858e219a5cfe5756b9c7bd536230a8f68293419c2830e163ee3`
