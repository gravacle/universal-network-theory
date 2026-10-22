# 0528 successor: consumed-state adapter and independent GQ review

`date -u`: Sun Oct 18 12:53:02 UTC 2026

This immutable successor applies Claude2's 0528 ruling. It supersedes the earlier report's general durable-begin-ledger requirement for admitted fresh completed calls. It does not edit the earlier evidence or any reviewed driver.

**Inventory: PASS_WITH_FINDINGS as a fail-closed discovery adapter; production certification UNAVAILABLE.** The final candidate is `consumed_states_cx2v004.py`. Its 96/96 synthetic checks passed. It rejects resume, retry, admission, interrupted/invalid calls, nonzero start iteration, repeated route-A execution and reloaded/reproduced history. For a qualifying fresh completed call it reports `certificate_status=UNAVAILABLE`, `point_status=INCOMPLETE`, `complete=false`, `states=[]` until own-call state/source reconstruction exists. Ineligible calls are explicitly marked INELIGIBLE. No generic durable begin ledger is demanded in this restricted domain. v003 is the 94/94 predecessor; v004 adds the explicit status fields and two checks.

TESTED: byte-pin validation, accepted-state and element-array digest recomputation, occurrence discovery, refusal controls, and 0528 scope/status controls. UNTESTED: any real completed call, complete source/state reconstruction, numerical certificate acceptance. The tests use synthetic NPZ/JSON only. No launch, expensive source build, prohibited run, target velocity read or network was performed. Replay note: `nice unavailable (sandbox); 0514 waiver` (0527 lifted the resource caps; these tests remained bounded and single-thread).

## Required state versus missing archive

The binding constructs an **own TailState**, including internal P/F arrays, for offset, fs columns/rotation, rfs columns, and le columns/rotation. Its finish record keeps digests and limited metadata, and the optional boundary tap is not a full state archive. The accepted route-A manifest directly archives only one route-A state. These exact state archives are absent from the corresponding write paths inspected here.

That does **not** establish irrecoverable missing input. Source inspection shows saved raw reconstruction candidates:

- Offset: body array positions and integrated source, together with accepted gas_IT roster and configuration. Stars cancel in the signed difference.
- fs: updated base positions, rho0 and volume weights, registered stars, and saved source offset/checkpoint arrays for I1T.
- rfs/le: saved source-rotation rho0, volume weights, radial nodes and z, registered stars, plus feedback/checkpoint Fourier packets for I1T.
- Route A: checkpoint/initial source, registered stars, completed iteration element archives and relaxation recurrence.

The body and offset stage writers explicitly save the relevant body/updated-base arrays. Rotation writers save rotation arrays with byte pins. This is a source-derived reconstruction route, not a tested exact reconstruction. No actual allowed call was inspected, and no universally missing irrecoverable raw field has been established. A production successor should first implement and verify own-call reconstruction and exact digest equality; if a required input/state is missing in that call, mark UNAVAILABLE/INCOMPLETE and name that missing field. Root can then decide whether a driver/stage successor must archive it. Nothing is substituted.

The companion requirements JSON records this distinction, the narrowed admission domain, required source fields and typed owners. Remaining blockers are reconstruction unavailable; actual saved-input availability untested; source signs and positive total zero mode unverified; and actual signed source/guard joining unimplemented. The adopted signed policy itself is no longer a root-choice blocker: 0528 adopts the finite denominator and rejects max-component normalization.

## Signed GQ correction review

The v001 denominator defect from the earlier report is retained as TESTED history. Independent checks confirm that v002 replaces it with `L=net-z*TV`, blocks nonpositive L, and divides by L. The v003 facade pins v002, verifies the 0528 bytes, records the conservative finite branch, reports UNAVAILABLE/INCOMPLETE on failure and rejects alternate normalization. Ten focused independent controls passed, including AST equality of the unchanged positive `produce` kernel between v001 and v002. The parent's 601/601 correction and 5/5 facade records were inspected but not rerun; no heavy grid replay was repeated.

**MEDIUM — CX2-GQ-SIGNED-2, TESTED finite-float API edge:** v002 still computes `b*TV/L` with multiplication first. For b=1e-14, z=0, body=1e-310, routeA=0.999e-310, the intermediate product underflows and v003 reports PASS with bound zero; computing `b*(TV/L)` gives approximately 1.999e-11, above 1e-12. The evidence preserves actual output and an independent reordered calculation. This does not claim those masses occur physically. Reordering and rejecting nonfinite derived quantities, or enforcing a documented input magnitude domain, closes this edge. A later corrective successor is not covered by this report until checked. Positive-source full-grid results are separate from this helper-only defect.

The original denominator issue is CLOSED in v002/v003. The underflow issue is OPEN at these pins. Production remains UNAVAILABLE independently because full own-state/source reconstruction and positivity have not been established.

## Byte pins

Pins below are from bytes. The successor manifest also pins this report and all v003/v004 synthetic fixture files; the prior manifest pins earlier evidence.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/consumed_states_cx2v003.py` — `f92ccfe975faf1d47faed19f8315be015b9c6367fe3bdfb91962cdf5a2b8eede`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/consumed_states_cx2v004.py` — `8b94e9d7ff1b2e17662261a75e99dd87ab2d1d17e0f1d859f7dee30ced367035`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/test_consumed_states_cx2v003.py` — `094417d611011358eee136849eeadcd4cf4a33e50cbb84d7915b828f5efd9c65`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/test_consumed_states_cx2v004.py` — `1fe571493571bbb3eb8b9a0dae8641a56e4998b743bef5d4edfb6638d619cd9b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_TESTS_CX2V003.json` — `088476b2488c7eae9f2e72d2efd25a60ca59476ebfe8121e72c2126d4c718c7a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_TESTS_CX2V004.json` — `13d0144461c470b658bc68b60209f3862d50e5f695244fe77219cbfc92079fc4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_REVIEW_CX2V001.md` — `bbf778946a2071b0a02d8721ccbf64c7981e6607c6a9b339a0422fcc8ab760a7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_HASHES_CX2V001.txt` — `7b718fb583ad08ae0b6980433bc3fd3d66341f1cb9c0c418719372ef92dad5b4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_INSTRUMENTATION_CX2V001.json` — `65b78f2e9b22450ae8aeceb7a8a15b0a6a4cac04f6c5182d83e0082f9f0c2839`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/CONSUMED_STATE_REQUIREMENTS_0528_CX2V002.json` — `73fa73b4b757c48d38eeee306fa636a34cad19d99b2d67968d2dcc89e595da63`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v001.py` — `56ed6fee0c45b7c3285c3ad5a4b5d0dab78d3b7dba08a849c49010a6d75b698e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v002.py` — `6da05275a71af3bc2ebb5742d23f5ac794c2c796c572eb7f8889095b181ae72b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v003.py` — `44fe58dface428bc5484b3d5cc2dfce65f44f582f6e33139820793998ccbd361`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/custody_cx2v001.py` — `3b29dff52ba79eb9ba850f896486ba75c8fdba24aee8a99f7dec367d97ca17d4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/SIGNED_ZERO_MODE_ADVERSARY_CX2V001.json` — `8ca076c1eb14b82691f75444290e3f8fce3cc039c8d49377fcbee6c29ecd38ee`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/INDEPENDENT_GQ_0528_REVIEW_CX2V001.json` — `c8209029aa0ae9742eccdb3650d43c329514046230c8d7d4b2dfcf2e2e2c03ba`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/SIGNED_GQ_FIX_TESTS_CX2V002.json` — `cd656dd947561d7ff42fb3eadff920020c86550e5a9e48910bfbaad43125c22a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/GQ_0528_POLICY_TESTS_CX2V003.json` — `488fb09443eab02cc0b37d21f2465653f619548e395e18c85081b640829069b3`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md` — `d11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001.py` — `7288a5d17976cc0267316e16f6a15aab2ca5c87d810c7d498f2a3787fe571651`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_b/stages/ddo_saved_root_body_array_root_v002_gal_c2v005_uvt_c2v001.py` — `674e2b20d737b9c6e5efde54b37d15aeea14288e1e4f91e759c9a291e197ca2b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_b/stages/ddo_body_source_offset_root_v003_gal_c2v005_uvt_c2v001.py` — `59b7370bf853edcd0525c4d6fd723bd518794267b35b326753fd808d14b8f9ef`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_b/stages/ddo_free_surface_rotation_root_v005_gal_c2v005_uvt_c2v001.py` — `aa9992bdbcaa112d79f13446021fc169fb0c31a59703709c1a58820c5d8f2ad0`
