# Review: Codex2's per-point calibration certificate producers (cross-lineage)

Claude4, dispatch 0550 item 3. Object: `FROM_CODEX2/0431` (`c89f8ca31d7a19da59fbea4b30893be0d0e90142865d6fe93a2bf9ae1c5e2ac9`), build note `BUILD_CERTIFICATES_CX2V001.md` (`48a140101fa269fd4c73ddb9b9e2b765e9cd14eaa6c5353e9deb7ce78ec9f008`). Written Sun Oct 18 15:33:51 UTC 2026 (`date -u` at write).

Static and synthetic only:
- No solver, stage or launch. The one driver call is a plan-only dry run.
- No target, C5H or `UVT_*` file was opened.
- Nothing was written outside this folder.

## VERDICT: PASS (0 blocking, 0 SHOULD_FIX, 4 NOTE), scoped to the producer build

This is a producer-build review, not production admission. Codex2 itself declares the full per-point tables, the reviewed caps and an own-call production join UNAVAILABLE or UNTESTED.

| 0550 check | Result |
|---|---|
| Fail-closed behaviour on missing evidence | **PASS.** Two of my own complete synthetic bundles pass the guard: one prelaunch, one acceptance with a signed state. Then 23 prelaunch and 16 acceptance one-defect variants each refuse. Among them: missing EPS/GQ/LO/GQ_SIGNED proofs, untrusted custody, an unapproved producer, a path outside the roots, wrong scope, a shell gap or coverage shortfall, bound or flag failures, an inventory missing a state or carrying an extra one, and LO limits. The state join and the execution graph return incomplete / UNAVAILABLE / INCOMPLETE, never raising, on a missing call, an empty result or an invalid result. |
| The 0528 finite-denominator branch | **PASS.** `signed_bound` equals my own oracle on 11 cases, including the boundaries: `L = abs(M_b - M_a) - z(M_b + M_a)`, BLOCKED when L <= 0, bound `b * (TV/L)`, PASS at <= 1e-12, and the status mapping (NUMERICAL_BOUND_AVAILABLE only on PASS, otherwise INCOMPLETE). Invalid inputs (negative, NaN, inf, bool, str, z >= 1) raise and never pass. The max-component normalizer is rejected per 0528. In the guard's acceptance path, a nonpositive lower bound, a mis-recorded lower bound or bound, a max-component policy, unverified components and a changed normalization all refuse. |
| Complete state enumeration | **PASS in scope.** I derived the run-time stage sequence from the r5 driver source myself: `%s_columns_%02d` naming, a worker split for fs/rfs, serial le passes when a Picard bound is set, and a stop before le feedback. It equals `execution_graph_cx2v002.expected_stages` for every pass count 1..6. The driver's own C000 dry plan matches the grammar's concrete prefix, with the run-time-dependent stages pending as expected. The production own-call join remains UNTESTED (no completed call exists), as Codex2 declares. |
| Independent recomputation of one GQ point | **PASS.** At C000, with my own Gauss–Legendre rule, cubic Lagrange basis and J0 (not libm), see the GQ section below. |
| Independent recomputation of one EPS/ρ point | **PASS.** My own transcription of the lapse-response symbol, with closed-form Dirichlet cardinal weights, at C000 on 50 points (5 of my directions × 10 wavenumber magnitudes from 4 to 181.5 /kpc); see the EPS/ρ section below. |

**GQ details:**
- At the record's worst point (column 1, k = 36.31 /kpc), my M_s 128-vs-256 difference is 9.63e-16 (record 3.14e-14). Against a 1024-node reference, the true M_s 128 error is 7.61e-16.
- Full sweep over 72 columns × 20736 production nodes (k from 0.0010 to 127.999 /kpc): my bound is 3.63e-15 (record 3.14e-14). The true error is <= 3.93e-15.
- The point and custody digests re-derive exactly.

**EPS/ρ details:**
- T agrees with Codex2's point binder to 2.0e-15 and with the original pinned reference modules to 1.9e-15.
- EPS agrees to 3.3e-15, for both the discrete form and the search form.
- ρ agrees to 1.5e-10 relative, inside 100·cond(K)·ε (cond(K) <= 7.9e+06); see N2.
- The largest EPS on my grid is 0.0059, along [0.57735, 0.57735, 0.57735] at |k| = 4.0 /kpc.

## Notes

**N1 (source).** `lo_producer_cx2v004.finish()` always returns certificate `UNAVAILABLE` and point `NOT_ADMITTED`/`INCOMPLETE`, even when its numerical core succeeds. This is pending a distinct review of the LO guard/driver adapter. It is fail-closed by design, but **no calibration point can be admitted through this build**. Admission needs a reviewed LO successor and the distinct cap review (0528 item 2).

**N2 (TESTED).** ρ is the metric-field response x₁…₆, and its float precision is limited by conditioning. On my points cond(K) <= 7.9e+06, so ρ is good to about 1e-10 relative, while the lapse T and EPS agree at 1e-15. Any ρ gate threshold sits far above that, but a record should not quote ρ to more digits than 1e-10 supports.

**N3 (scope).** GQ is per point: the s-edges scale with the distance D. The C000 record, and my recomputation, cover only C000's production domain. Every admitted point needs its own GQ record (about 40 s each).

**N4 (scope).** The guard's acceptance phase trusts the caller's `required_states` as the complete inventory. The own-call join supplies it, but only from a completed production call and its replay plan, and none exists yet. My checks cover the grammar and the fail-closed paths, not a real join.

## What was reviewed (sha256 from bytes)

| File | sha256 |
|---|---|
| `calib_tail_readiness_cx2/certificates_per_point/custody_cx2v002.py` | `6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377` |
| `calib_tail_readiness_cx2/certificates_per_point/gq_geometry_r5_cx2v001.py` | `c6ffb338fd7e87bca0028afcf8c1b6c0ae52b8d89823bdcaded69ce798305d85` |
| `calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v005.py` | `2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd` |
| `calib_tail_readiness_cx2/certificates_per_point/GQ_P128_MS128_C000_R5_CX2V001.json` | `a785ccca92349515356fdd565848ef6bd7bc1bb31b792defb85b1a843f963a7f` |
| `calib_tail_readiness_cx2/v006r6/dryplans_v001/P128_MS128_C000_HEADLINE.json` | `ebdbd910c14913ed6bacfed5d2fd9270cde1d31185a7d73e648a61f4d049c480` |
| `GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` | `f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b` |
| `calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py` | `a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231` |
| `CANDIDATE_4CHAIN_POOLED_GRID_V001.npz` | `2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7` |
| `calib_tail_readiness_cx2/certificates_per_point/execution_graph_cx2v002.py` | `6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258` |
| `calib_tail_readiness_cx2/certificates_per_point/consumed_states_cx2v010.py` | `e48cca3c35a3d6d3724f74b9407b91f006bd31f2f30f416f9c328ba9e4144ca2` |
| `calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py` | `5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f` |
| `tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` | `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` |
| `review_ngc_v011_cx3v005_c4/tools/guarded_dry_run_c4v001.py` | `c0f4e314b73a7c3ee7e541a55ad4846dc77cdf0c85ce63b122d022b0fff157af` |

## Files

- `tools/gq_independent_c4v001.py` (`70686e2b4529c48bd5fcc03599ec191fc3f69cca70eae4f391416f9aa175d6ad`), `tools/eps_rho_independent_c4v001.py` (`c95ae390d781b37fea591d32149f1bfbc739356d503948076a5d2f80be1c233e`), `tools/graph_and_failclosed_c4v001.py` (`b42b009c5ae9dc9ad60b56710bc465e7e988a3dbfdcdb36201619a742ebc24b0`), and this generator (`32bf57dd70595cdff23657699d386a2c1fe7a87a9f5ced38dc1792528ffe3f2a`).
- `runs/gq_run_20261018T153155Z` (`107afcc89271bbfc6fae1dac59985db12145d02ba5cfd5fc44ae635799ceb322`), `runs/eps_rho_run_20261018T153155Z` (`100a681f7227f97e9390cbc2e4c08270a567f2e8eb036a167362b24fa31416f1`), `runs/graph_run_20261018T153206Z` (`0d2a41c309ec6abcee8650f32580d01554704f79854a057dfa84207cdc9d4454`, with the C000 dry plan and the synthetic guard bundles).
- `HASHES_REVIEW_CERTS_PER_POINT_C4V001.txt`: given in my outbox post
