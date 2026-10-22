# Point EPS/LO producers — bounded test and integration contract

UTC generated: 2026-10-18T12:53:25.179528+00:00
`date -u` captured during this finalization: Sun Oct 18 12:50:49 UTC 2026.

TESTED: 76 bounded assertions/checks (46 numerical and adversarial; 26 grid/cap/adapter; 4 root-0528 status assertions). No scientific launches, network, forbidden runs, or observed/target velocities were used. All files below were created under new names; predecessors remain unchanged. Resource caps were lifted by dispatch 0527. Tests still used the prescribed Python with `-I -B`, NumPy/stdlib and single-thread environment.

The EPS producer accepts an actual point spec, derives its custody, evaluates its own physical Binder, and checks four nodes against the original pinned symbol modules. Common Eref/gamma scaling reproduces q bitwise on the test sample; changing gamma/Eref or ell changes q. The discrete 26/52/104-direction refinement result reproduced the registered implementation exactly. Full defaults cover every unit shell through ceil(sqrt(2) Kbig), with cardinal-torus grid/local search and dense audit. No finite numerical maximum is claimed to be a rigorous supremum enclosure.

Actual C000 smoke results: (4,5] EPS estimate 0.016370508679282691; (8,9] 0.0041002678025954253. Both registered discrete tests used zero further refinements. These are **TESTED numerical search diagnostics only**, not complete EPS certificates. The primary test took 0.951 s with 122,601,472 bytes peak RSS. The second suite took 0.108 s with 84,541,440 bytes peak RSS. No full-point runtime is inferred.

LO recomputes point-dependent sampled/envelope rho and combines it with pinned saved B1/state/actual row metadata. The real saved-source smoke gave rho 6.5216060101308653 and shell max/tau 0.00040752607320412713. That diagnostic holds the old source fixed and is explicitly blocked: it does not solve the new point. The current-state path requires TailState digest reconstruction, exact normalized configuration and actual production node arrays, B1 replay from P/F, approved source reconstruction, I1-T and reviewed row policy. Checks reject one-ulp changes to each of kp/kz/wkp/wz, config/domain/jet changes, B1 tampering and altered state digests.

The conditional source envelope uses actual radial factors: |S| <= c^2 sum_i |Pi_i| sum_c M_ci_max/(2 pi rdr_i), plus the fixed stellar factor. Absolute radial interpolation coefficients are retained; total gas mass alone is insufficient. A 12-case check against explicit complex source sums at actual DDO radial factors verified the TV inequality, including signed component differences. Cap enforcement computes TV from actual element arrays and rejects extra components, mass/speed/star/extent violations, geometry/tau changes and NaNs. The function has **not** been integrated into the production build or independently reviewed.

0528 is applied: prelaunch LO is **UNAVAILABLE / NOT_ADMITTED** until caps are enforced by the build and reviewed by a distinct lane. Missing own-run source archives yield **UNAVAILABLE / INCOMPLETE**; nothing is substituted. Calls must be fresh, without resume or retry; interrupted route-A calls are invalid. The preferred facade records the root's **CONSERVATIVE_FINITE_DENOMINATOR** signed-GQ branch; its numerical normalization belongs to the parent GQ implementation. No max-component alternative is applied here.

Use `point_response_producer_cx2v001.py` for EPS/rho, `lo_producer_cx2v003.py` for root-ruling-aware LO, and `point_response_admission_adapter_cx2v001.py` for EPS conversion. The EPS adapter requires full registered evidence plus independently approved producer/adapter/review bytes. The returned guard proof points to the separate real numeric driver record; smoke fails before any approval check. No positive admission was fabricated. Current/prelaunch LO conversion to a driver slot remains a typed blocker until complete evidence and review exist.

The accompanying machine-readable CONTRACTS file gives the exact APIs, state/source/row/cap/review schemas, approved-producer boundaries and blocker codes. Full registered EPS/rho, all points, a real current-state positive path, the reviewed conditional envelope, integrated cap enforcement and positive admission remain **UNTESTED**. This helper cannot identify an always-missing route-B archive from its synthetic/saved-B1 work; the parent's complete-state enumerator must name that exact state for root's successor decision.

## Byte SHA256 inventory

Every local file mentioned in this report or its contracts is identified below. Paths in the first table are relative to this report's directory.

| File | SHA256 from bytes |
|---|---|
| lo_producer_cx2v001.py | `688ff215e72da3846b4baa399fbfc7fcf33304bbd27f8096227114372e6b1487` |
| lo_producer_cx2v001_TEST_CONDITIONAL_BLOCKED.json | `866525b027aeb4ac667e126d7c582c237697aab9e5e4403012d196865878f1bd` |
| lo_producer_cx2v001_TEST_SAVED_B1_C000.json | `813859c85bc8b8c261d308c1506ce6eefa7df6b1b5fd770c829005367a8467f2` |
| lo_producer_cx2v002.py | `1819667288c8b63178181c252541b4314abc7c4866b5aedad5e4cb7222cf93a5` |
| lo_producer_cx2v002_TEST.py | `3dea8f196715a554b5cf8dccbf33b8f6912db113e680b45e6e6d034d4f2e6131` |
| lo_producer_cx2v002_TEST_RESULT.json | `a3d3920596b90457e30f7f0e98030f454aa4e5caf6f193aa36bce8268b075f8c` |
| lo_producer_cx2v003.py | `3a5df160db84f3feabb4e6c36aa40ffa69522957537ec97517982806854ce25f` |
| lo_producer_cx2v003_TEST_RESULT.json | `b68bcaebc26ecad2c0e8a9696efd59de69d01eee1de8d836d07a0858136a7371` |
| point_response_admission_adapter_cx2v001.py | `7016a0581aa0768479d65209942732193913a94544455b70e12607e4f21c4d1d` |
| point_response_producer_cx2v001.py | `c6a8ee6f6ffc2e890c9047f8a789a7c86c7d930f8b0c337d8f90c9b87a1085c1` |
| point_response_producer_cx2v001_TEST.py | `fe38e53f24232068f9dea1ff227678f92a70cacbc305184acf3166ad2cb70649` |
| point_response_producer_cx2v001_TEST_ADAPTER_REFUSAL.json | `b6e544608237a0d312ca16079abf17b61981ccecf2c70c62a00057b000176774` |
| point_response_producer_cx2v001_TEST_CONTRACTS.json | `e59509f8db241625c30fd3db4e9e7027ced4015b3250a30ebac110d6d4be9d6a` |
| point_response_producer_cx2v001_TEST_EPS_C000.json | `9f9bdffb7c94bcd59ad5f4b183513242f36a5fa7ce957029bba52d1db9d7fee9` |
| point_response_producer_cx2v001_TEST_FINALIZE.py | `378ff3374da04d148836a285b1106845df8da943f366fe7cc430b3ca9c4d87ae` |
| point_response_producer_cx2v001_TEST_RESULT.json | `2c47757f061cb94b47eac292e27abb6472ef9a788b2bf49337d4b4783d7cd616` |

| External dependency/ruling | SHA256 from bytes |
|---|---|
| /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0527_2026-10-18_all_lanes_process_caps_lifted.md | `e662fd4d176f71b0d422f24a640f88b6dcccbeca5e4148a9fe3fc7062710a2e4` |
| /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md | `d11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/custody_cx2v001.py | `3b29dff52ba79eb9ba850f896486ba75c8fdba24aee8a99f7dec367d97ca17d4` |
