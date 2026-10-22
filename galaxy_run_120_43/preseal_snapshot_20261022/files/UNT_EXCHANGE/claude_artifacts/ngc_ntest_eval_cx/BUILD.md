# NGC N-test evaluator build — completed dispatch0510

Scope: dispatch0510 source/build and saved-operator replays. No forward or route-A/route-B launch. NGC M_s remains96. NGC observed/target velocities are not inputs. TESTED build checks completed. The scientific campaign reading remains N_INCOMPLETE; this is not a launch or N_PASS.

| Site | Public successor | Difference and validation |
|---|---|---|
| NE1 replay_c1 metric_point L79–93 | ngc_ring_tail_ctx_c2v003.py TailCtx | Supplies TailBoundary once to evaluate_line, before the unchanged metric evaluator. Empty tail delegates directly to parent arithmetic. Exact kept delta uses the saved prepared line. |
| NE2 kg_lib checker/ctx_with L163–201 | ngc_ring_tail_ctx_c2v003.py ctx_with_tail | Verifies registered T120L/hovr operator, matching kept mask and admitted tail; returns checker, roster module, context. Solver explicitly unavailable. |
| NE3 ringeval L12,23–31 | ringeval_uvt_c2v003.py | Registered tail-config CLI; same roster, 32 azimuths, seven acceptance heights, optional ±95kpc diagnostics and kept packet. |
| NE4 dsplit_sphere L34,46 | sphere_eval_uvt_c2v003.py | Spherical mask on the same saved operator with matching sphere tail. A cylinder with K_big=K is not an empty spherical tail; N0 is the registered cube-empty identity. |
| NE5 run_p23 L19,59–70 | run_ntests_c2v003.py | Verifies CODE_PINS_V001 bytes and permits only the two public replay evaluators. No solve/forward dispatch path. |

Internal replay versions preserve their history. run_ntests_c2v001 produced N0/base NQ; run_ntests_c2v005 uses ringeval_uvt_c2v005 and ngc_ring_tail_ctx_c2v004 for the fine replay. These share the same metric arithmetic. The fine path precomputes radial tables; its demand-vs-precomputed policy check returned exactly0.0 at six points over three rings. It raises the in-process table cap only to4GiB under dispatch0513; the reviewed module file remains unchanged. The earlier default-cap refusal remains recorded.

TESTED so far:
- N0:156 rings ×32 azimuths ×7 heights =34,944 values, zero bitwise mismatches against all12 reviewed reference files.
- Public API:47/47; synthetic compare branches:43/43; public runner CLI/pins/allowlist:3/3.
- Synthetic tail-on sanity: maximum relative difference1.2666429347809853e-14.
- Independent three-ring spot integration: maximum relative difference2.4105266730377716e-15. The spot integration does not import the tail module; it shares the declared source and installed libm Bessel provider, so it is not an independent validation of that provider or source physics.
- NQ base and fine replays completed on100 rings ×32 azimuths ×7 acceptance heights. Maximum absolute changes in lnN0 and dL are both0.0 in stored floating-point values, meeting theta/20 = 1.6828832069490022e-10. This tests quadrature refinement at these points; it is not an analytic zero-error claim.
- Raw-evidence audit:7/7, including rejection of contradictory statistics, mismatched bit counts and outside paths. Final byte-pin audit:51/51 inputs and sources unchanged.
- Final full compare: N_INCOMPLETE, tests_read=false, pending N2/N3/N4 and N1 C1prime G160L/G120L evidence. No omitted test is silently passed.

Final compare entry is ntests_compare_c2v005.py, backed by the0512 rule implementation in v002, path/pin restrictions in v003, and raw-data statistic auditing in v004. assemble_ntests_c2v002.py validates raw configurations and derives evidence records. Input defects precede missing evidence. Missing NQ, LO_NGC, I1-T or C1prime evidence yields N_INCOMPLETE; defects yield N_NO_RUN. N3 uses absolute changes of S and dL against theta/4 for8vs16 and32vs16; S/theta is reporting only. N4 is reported, not an acceptance gate.

UNTESTED: full scientific N1–N4 campaign, sphere replay convergence, NGC fixed points and target comparison. Missing full-test evidence must remain N_INCOMPLETE even if N0 and NQ pass. No fixture or synthetic result substitutes for those readings. Input hashes are recorded in INPUT_PINS_V001.json and N0_REFERENCE_SHA256_V001.txt; source hashes are recorded in CODE_PINS_V001.json. HASHES.txt hashes all completed build files from bytes, excluding itself. Subsequent review fixes require new successor names and a new hash manifest.


## Reproduction and output map

Use the dispatch Python executable with -I -B, nice10, single-thread BLAS and at most3 replay processes. No commands here authorize a launch. Public runner syntax is `run_ntests_c2v003.py ringeval_uvt_c2v003.py|sphere_eval_uvt_c2v003.py ...`; each evaluator documents its registered tail-config arguments via --help. Internal N0/base/fine replay results are retained under out/; expensive replays must use fresh output names if repeated.

The pinned raw manifest out/N0_NQ_RAW_MANIFEST_V001.json feeds assemble_ntests_c2v002.py. Use a fresh relative output prefix. The resulting *_MANIFEST.json feeds ntests_compare_c2v005.py with a fresh output path under this directory. Current results are out/RECORDS_V001_N0.json, out/RECORDS_V001_NQ.json and out/BUILD_COMPARE_V001.json. out/DATA_AUDIT_TESTS_V001.json records7 adversarial evidence checks. out/PUBLIC_RUNNER_TESTS_V001.json records3 CLI checks. The default-cap refusal out/NQ_FINE_REFUSAL_V001.json remains part of the history; the successful fine replay is out/NQ_FINE_V002.json.

The independent spot test imports no tail-module implementation, but shares source definitions and libm J0. Its three-ring agreement is a finite integration cross-check only. The precomputed-table fine replay has a separate six-point demand-policy identity check in its raw record. The4GiB override applies only to this saved replay process under0513, never to a production driver or reviewed module bytes.
