# 0818 — S9 makespan, cw1/cw8/mix (CX3V002)

Wed Oct 21 11:56:10 UTC 2026

**FORMAL decision: the required ≥0.5 d E saving is NOT SHOWN. Do not commission the cw8 operational build on this evidence.** On the favorable expected seed-path model, its largest possible tabulated E saving is **10.32 h = 0.430 d**, below the 12 h threshold. For three new minus-point calls it falls to **4.48 h = 0.187 d** with 16–18 CPU units available, or **0 h** when a 4–6 unit overlap reserve leaves only one eight-worker route-A slot. Existing S0 serials and the S8/seal/acceptance join can mask even those savings. U gains do not satisfy root's explicit **E** condition.

This is a conditional source-based scheduling result, not a measured S9 benchmark. The exact future production roster cannot honestly be reported as already known: 0818 supplies no actual post-B_P1 selection/FDPLAN/P112-config pin, and membership depends on the future DDO admitted-point record. No run tree or NGC data was opened to guess it. The deterministic count formula and the relevant expected-path cases are below. This limitation does not create evidence for a ≥12 h E benefit.

**1. Exact count rule and critical dependencies (FORMAL).**

PHASE1 `cmd_fdplan` (776–821) obtains M from the pinned freeze selector, constructs three one-axis F points from the recorded u_A, and deduplicates M+F by exact point key. P112 `Context.calls` (937–1014) independently reconstructs those calls from PLAN, selection, FDPLAN, handoffs, fills and certificates; `finish_call` checks actual physical bits before S0 reuse. Define:

`N = |keys(M) ∪ keys(F)|`, `N_new = |(keys(M) ∪ keys(F)) \ keys(eligible S0)|`.

An equal key alone is not sufficient reuse authority: the bound physical/spec/driver/certificate custody still has to pass. The identity twin is OTHER and never a member or a reusable completed full call. ORIGINAL_K and sensitivity have budget zero in Phase 1 and add **zero** scientific calls (A133 §1.4; RUNBOOK Phase-1 sequence).

The expected nominal seed path has these exact **conditional** counts:

| Future admission case | Distinct member+F calls | Reusable S0 calls | New calls at u_A |
|---|---:|---:|---:|
| u_A = seed, only seed admitted | 4 | 4 | **0** |
| Nominal seven-point prefix, one selected/admitted minus point | 5 | 4 | **1** |
| Same, two selected/admitted minus points | 6 | 4 | **2** |
| Seed and all six nominal Jacobian points admitted | 7 | 4 | **3** |

Here the four S0 calls are seed plus three first-attempt plus points. F is exactly those three plus points when u_A is seed (PHASE1 795–800; A133 lines 83–90). With registered `interior_count = 5` (V006 A157, A163 N2), the nominal three-dimensional seven-point case selects the needed admitted points; F/member overlap creates no extra call. **TESTED synthetic check:** the actual pure freeze selection function was evaluated for all 64 admitted subsets of six invented ±axis points with seed admitted. It gave `N = 4 + admitted-minus count`, four reused S0 identities and 0–3 new identities every time. This does not test actual admissions or numerical predictions.

If seed/Jacobian validity fails, halving or repair changes the prefix, or u_A comes from another point, **do not reuse this 4–7 count as fact**. The source bound at 1–3 identified directions is at most `2*m_id + anchor + centroid + 5` members, then at most three extra F points: **N ≤ 16** before same-point reuse; actual count needs the real selection. Terminal engine failure or zero identified directions makes no Phase-1 NGC call (A133 lines 70–73). No complete production count is recoverable merely from a pre-run config.

All distinct M calls are required to construct PRIMARY envelopes; every distinct F is required for the Phase-1 linearized projection. Therefore they all participate in the S9 terminal-status/acceptance join for a fully evaluated S10. There is no source-authorized subset consisting only of u_A that can stand in for the roster. A model-invalid outcome or schedule ceiling can produce a registered incomplete reading, but shortening the wait by forcing that disposition is not a speed optimization. S8's S1 reading, the actual seal and post-state acceptance are separate S10 prerequisites. In particular, **N_new = 0 gives exactly zero benefit from building a future-call cw8 selector**: all relevant computations are already S0 serials.

**2. Host and contention model (FORMAL assumptions, not runtime measurements).**

Use 18 logical CPU units and 128 GiB as stated by root in 0818. A direct `sysctl hw.ncpu hw.memsize` metadata attempt in this sandbox returned Operation not permitted; this review does not falsely claim an independent host measurement. No escalation or launch was attempted.

The model has no campaign load, as 0818 directs. Existing S0 serials continue unchanged. S8 comprises two DDO runs, but **those are not two one-core route-A jobs**: CORE `validate_block` (226) requires DDO route-A `column_workers == 8`; the inspected S45 config has that leaf 8; S1_LIB `build_case` (699–710) changes label/grid/certificate slots, preserving the worker leaf. During their column phases the two DDO calls can demand **16 worker units**, before coordinators or S0. With four active S0 serials that is already 20 > 18. Thus the simple 18-unit inequality cannot hold if both S8 column pools and all four S0 serials are treated as simultaneously CPU-saturated. The actual scheduler may oversubscribe; no measured slowdown factor is available here.

To compare like with like, use a common nonnegative release delay **T**, sufficient to reach the chosen S8 stage/CPU window, and a constant reserved load **q** for other work during the model window. This is a planning envelope, not a new admission gate or a proposed change to A166. Tables show q=0–2 (16–18 units left) and q=4–6 (12–14 left). The latter can reserve four old S0 serials plus two S8 serial-stage slots. Holding that reserve even if those calls finish is deliberately conservative. While both S8 eight-worker pools are active, the q=0–6 tables do not apply; a cw8 start must wait in this strict model, or concurrency must be measured before claiming a gain. S0 already running is never stopped to force the model.

New calls have equal scenario costs; all are ready at the same modeled release T. A cw1 call uses one CPU unit. A cw8 call uses eight through its route-A loop, then one for the unaccelerated readout/route-B tail. This is an intentionally simple optimistic CPU model: it treats 18 logical CPUs as equal, ignores coordinator overhead, and assumes the published standalone costs remain valid under the admitted concurrency. The physical P/E-core mix, serial tail builds, I/O and swap/QoS contention make actual elapsed times **UNTESTED**. The real route-B setting uses its own registered workers; following 0818, this model treats route B as an unaccelerated serial tail, not as a promise that its process tree has one OS process.

**3. Timing inputs and E/U makespans.**

The corrected ESTIMATE V002 and ESTIMATE_VERIFY provide:

| Duration | E | U |
|---|---:|---:|
| Whole cw1 point S | 31.90 h | 84.77 h |
| Whole cw8 point P | 21.58 h | 51.85 h |
| cw8 route-A loop a (8-worker stage for this model) | 5.84 h | 17.52 h |
| cw8 serial readout + route-B tail b = P − a | 15.74 h | 34.33 h |

The decomposition subtracts readout **10,427/17,635 s** from corrected cw8 route-A tree **8.74/22.42 h**, then subtracts that loop from the full point. Values are rounded consistently to 0.01 h. Route-B/readout receives no cw8 speedup.

**Measured inputs, with correct scope:** MEASUREMENT_BASIS I10 records NGC prep 137.54 s; I16 records a 2702.9 s K32 cold build at empty evaluation-radius roster under load; I13 records DDO tail unit costs 11.33/38.09 ns in different regimes; I12 records a 0.400747 s tail-off G80C column. Those published component measurements calibrate RI45-12; none is a measured full current NGC point or concurrent S9 workload. This review did not reopen their run records or remeasure them. U is explicitly not an upper bound (ESTIMATE_VERIFY N7, omitted route-B evaluations and unknown convergence). The twin's **22,752 s** remains a planned cap, **not** a measured two-iteration elapsed time.

Below are **new-call-branch makespans after common delay T**, not a sum of per-call savings. “All cw8” means only newly required calls; old S0 serials keep their original identity.

| Other-work reserve q | N_new | All cw1 E/U | All cw8 E/U | Best model choice | Best S9-branch saving E/U |
|---|---:|---:|---:|---|---:|
| 0–2 | 1 | 31.90 / 84.77 h | 21.58 / 51.85 h | cw8 for the one new call | **10.32 / 32.92 h** |
| 0–2 | 2 | 31.90 / 84.77 h | 21.58 / 51.85 h | two cw8 loops together | **10.32 / 32.92 h** |
| 0–2 | 3 | 31.90 / 84.77 h | 27.42 / 69.37 h | all three cw8, two then one loop | **4.48 / 15.40 h** |
| 4–6 | 1 | 31.90 / 84.77 h | 21.58 / 51.85 h | cw8 for the one new call | **10.32 / 32.92 h** |
| 4–6 | 2 | 31.90 / 84.77 h | 27.42 / 69.37 h | two cw8 loops in sequence | **4.48 / 15.40 h** |
| 4–6 | 3 | 31.90 / 84.77 h | 33.26 / 86.89 h | **all cw1** | **0 / 0 h** |

**FORMAL optimality within this small model.** All 0–3 cw1 jobs fit at once. Any mixed assignment retaining at least one new cw1 job has completion ≥S; all cw1 already achieves S. Thus a proper mixture cannot improve the S9 join under equal costs. If all are cw8, 16–18 available units allow two loops at once; 12–14 allow one. Completed loops drop to one-unit tails, so the last finishes at `ceil(N_new / floor((18−q)/8)) × a + b`. The best is `min(S, that duration)`. No arbitrary member is dropped to obtain the answer. The 95 synthetic/arithmetic checks include all 24 scenario/reserve/count combinations and their capacity inequalities.

Let **R** be the largest remaining completion time of a required old S0 serial at the chosen release, with S8's remaining prerequisite similarly included if it dominates S10. Then the S9 join in this model is:

`T + max(R, new_call_branch_time)`.

Savings are `max(R,S) − max(R,best_branch)`, so they are never larger than the table. For example, with one new call and **assumed** R=24 h E / 72 h U, the nominal 10.32/32.92 h saving becomes **7.90/12.77 h**. If R≥S, it becomes zero. These R values are illustrative, not reads of S0. With no new call, both choices simply wait for the existing S0/S8 prerequisites and the gain is zero.

The n≤16 off-seed bound is not an assertion of the actual roster or a validated scheduler estimate for that branch. Under a favorable common-release model with enough units for all those cw1 jobs, all-cw1 completes in S and every new cw8 job takes at least P, so even the optimistic per-branch E improvement cannot exceed **S−P = 10.32 h**. Where S8 prevents that common-release model or where actual calls have unequal costs, actual CPU/stage/residual metadata is required. An unmeasured serial slowdown or a more favorable cw8 contention factor cannot be invented to cross the 12 h threshold.

**4. Build decision and smallest conditional scope (FORMAL).**

The largest favorable E saving is **0.430 d**, short by **1.68 h**; for the three-new-minus expected case it is **0.187 d**, or zero with the overlap reserve. The U best cases (1.372 d or 0.642 d) do not meet an E-based commissioning criterion. These inputs therefore justify **no cw8 build now** under A256/0818. This is not a claim that no future measured workload could ever favor cw8 by 12 h; that would require actual roster and concurrency measurements.

If root later changes the criterion or obtains qualifying evidence, the smallest forward-only build can omit the **cross-worker equivalence-key mechanism**: keep every existing S0 call as serial; make only genuinely new selected member/F calls cw8; retain their exact full-spec SHA and independent result/certificate custody; do not reuse a cw1 result under a cw8 spec or vice versa. That removes item 3's normalization/rebinding code, **not** G3's raw custody, the conditional identity gate, full-call selector/P112 changes, dry-leaf/argv/receipt reconstruction, consumer pin/schema checks, adversarial tests or distinct review. Nor does it allow relabelling the stopped identity twin as a member. A mixed selector cannot manufacture >12 h E saving when the unchanged new cw1 member remains the equal-cost critical call.

For an exact future roster/timeline, the missing permissible inputs are the root-pinned value-free selection/FDPLAN/P112 config and exact-spec reuse mapping, plus value-free completed/elapsed stage timing metadata for required S0/S8 calls. They must be supplied or explicitly authorized by root; none was guessed or taken from a forbidden run tree in this pass. The source-only decision above is complete; the actual runtime forecast remains UNTESTED.

**Validation and conduct.** TESTED: 95 checks (64 synthetic admitted-subset selections, the source/count bound, 24 CPU-envelope arithmetic cases, timing-threshold and source-worker guards). This is not a physics test. No forward, route-A/route-B, dry driver, real comparator, full production Context, monitor or launcher ran. No NGC data, observed/target velocities, run tree, step-2 output, network or session log was opened. Outputs are immutable successors; no prior report was edited. Codex3's lane concentration is disclosed; no independent-lineage scientific verification is claimed.

Evidence: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/S9_MAKESPAN_EVIDENCE_CX3V002.json` — SHA256 `51324dc89b1b2aca08e5952800583d72d95ec9861f8225df574664f4abe44b24`.

Source register, SHA256 from bytes:

- **A133**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md` — SHA256 `cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17`.
- **CHECKER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/check_s9_makespan_cx3v002.py` — SHA256 `881f4ca8cdb4207a77fe3fdc4e185571cef66ae398ecc3122c2103bfc22653b3`.
- **CORE**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py` — SHA256 `dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6`.
- **DISPATCH**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0818_2026-10-21_codex3_S9_makespan_cw1_vs_cw8.md` — SHA256 `6d4bad19236c99a98941094b96b1bca432a829f647aab5d1d0b303f616855ba4`.
- **ESTIMATE**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/ri45_12/estimate/ESTIMATE_RI45_12_NGC_K32_C4V002.json` — SHA256 `e686637e74349e928fed583ce1126520eab5cd47b7045da90df4e5e38efc758d`.
- **ESTIMATE_VERIFY**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/ri45_12/verify/VERIFY_RI45_12_C4V001.md` — SHA256 `4c902975d11af72885009a9fe7b491ff04b00c07a55b430b64e0525323d802a6`.
- **FREEZE**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` — SHA256 `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405`.
- **P112**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py` — SHA256 `8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9`.
- **PHASE1**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_c2/phase1_c2v003b.py` — SHA256 `7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4`.
- **PRIOR_REPORT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/LANE_B_CX3V001.md` — SHA256 `20ff14c5693070e7335cf9da162ca569db85b54299ac1c134e78431bf3d806fb`.
- **RUNBOOK**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2v007_cx2/RUNBOOK_V002_C2V007.md` — SHA256 `12917ba93955f106f8ab30fb39d464cd6b1f0e5d27597d0c29c6c6c6cfb7c547`.
- **S1_LIB**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_path_lib_c2v002c.py` — SHA256 `99e2be175e546992c70984435bc480e1eddb90b052fda65ddcbfe8780bdbd27e`.
- **S45_CONFIG**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v004/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004.json` — SHA256 `cbc36b7af83fdde102290f1e6d33f100925ce47ac31394968988b59771edf751`.
- **V006**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` — SHA256 `6d8df15e489fd1f002cc14cc84ff50530c3b88cbe9fe9f182805f644694d4987`.
- **MEASUREMENT_BASIS**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/ri45_12/estimate/ESTIMATE_RI45_12_NGC_K32_C4V001.md` — SHA256 `0546b3ea5563b1d70faa47f84de853ea39463eac7c3ec3381148a4b91b16c733`.
