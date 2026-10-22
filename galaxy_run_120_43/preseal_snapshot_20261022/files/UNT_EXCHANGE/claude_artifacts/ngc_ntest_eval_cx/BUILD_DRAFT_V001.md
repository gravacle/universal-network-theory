# NGC N-test evaluator build — in progress

Scope: dispatch0510 source/build and saved-operator replays. No forward or route-A/route-B launch. NGC M_s remains96. NGC observed/target velocities are not inputs. This draft precedes completion of the fine NQ replay; BUILD.md will report its actual result.

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
- NQ base replay completed on100 rings. Fine replay is running; NQ is not yet claimed PASS.

Final compare entry is ntests_compare_c2v005.py, backed by the0512 rule implementation in v002, path/pin restrictions in v003, and raw-data statistic auditing in v004. assemble_ntests_c2v002.py validates raw configurations and derives evidence records. Input defects precede missing evidence. Missing NQ, LO_NGC, I1-T or C1prime evidence yields N_INCOMPLETE; defects yield N_NO_RUN. N3 uses absolute changes of S and dL against theta/4 for8vs16 and32vs16; S/theta is reporting only. N4 is reported, not an acceptance gate.

UNTESTED: full scientific N1–N4 campaign, sphere replay convergence, NGC fixed points and target comparison. Missing full-test evidence must remain N_INCOMPLETE even if N0 and NQ pass. No fixture or synthetic result substitutes for those readings. Input hashes are recorded in INPUT_PINS_V001.json and N0_REFERENCE_SHA256_V001.txt; source hashes are recorded in CODE_PINS_V001.json. Final HASHES.txt will hash the completed build files from bytes.
