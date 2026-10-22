# REVIEW_NGC_NTESTS_C4V001 — cross-lineage review of Codex1's NGC N-test evaluators and compare: **PASS_WITH_FINDINGS**

Claude4, single reviewer, inline. Helpers are unavailable until 2026-10-23T19:00Z. UTC 2026-10-18T13:46:40Z (`date -u`).
- **Dispatch:** 0536 (`3c4b92b671613b7969f9dc791fb434185744ec0a81be93aa81c746baa847c5c3`).
- **Object:** `claude_artifacts/ngc_ntest_eval_cx/`. All 32 code pins and all 19 input pins verified from bytes; the N0 reference ring files match `N0_REFERENCE_SHA256_V001.txt`.
- **Hygiene:** no launches; replays only. No NGC target or observed velocity was opened (item 6). Nothing was written into the author's folder, and nothing was deleted.

## Verdict by item (refute by default, my own scripts)

| # | item | result | evidence |
|---|---|---|---|
| 1 | N0 bitwise, recomputed on a ring sample | **PASS** | Rings [0, 1, 7, 15, 50, 99, 100, 155]: 1792 values bitwise equal to the saved T120L reads (0 mismatches). Successor equal to the parent `Ctx` bitwise on 448 values (rings 1, 99); roster identical. |
| 2 | Continuum tail added exactly once, at the cited R1 site | **PASS** | Static and runtime evidence; see "Item 2" below. |
| 3 | N3 = 0512 (\|ΔS\| ≤ θ/4 and \|ΔdL\| ≤ θ/4; K_big 8 and 32 against 16) | **PASS** | Compare v002 N3 block, assembly N3 block, and branch tests T07–T10. |
| 4 | My own independent tail at 3 rings | **PASS** | Value 5.3e-15, gradient 1.0e-14, relative to max over 48 points; my own doubling 8.2e-15 / 1.0e-14. |
| 5 | N_INCOMPLETE for any missing input; never a silent pass | **PASS** (one gap, F1) | Branch tests 40/40. |
| 0539 | NQ's exactly-zero delta | **Explained: genuine** | The quadrature really differs (order 12 against 8, N⊥ 77388 against 26304, N_z⁺ 54864 against 18288; distinct digests and files); the tail is non-zero (up to 5.77 θ); the zero comes from N's resolution (see below). |
| 6 | No NGC target or observed velocity read | **PASS** | 240 files opened at runtime, none target-like; static scan of 32 code files, 19 pins and 12 outputs clean; source custody statements read. |

## Item 2: where the tail enters, and how often

**Static.** The only arithmetic site is `TailCtx.metric_point` (NE1, `ngc_ring_tail_ctx_c2v004.py`).
- It replaces the parent's zero boundary jets (replay_c1 L81–82) with `tail.jet(pos, 1)` in the single `evaluate_line` call (L86). Hessians are exact zeros at order 1.
- `lnN` (L105–106) is inherited.
- For an empty domain it returns the parent `metric_point` unchanged, so N0 identity holds by construction.
- NE2 builds the state; NE3–NE5 only call `ctx.lnN`.
- The sphere mask is the parent's (`|k|·KPC ≤ 2.0`), and the roster is built after masking, as in `dsplit_sphere_v001`.

**Runtime** (production cube, K_big 16, 12 points):
- each lnN call made exactly 1 `tail.jet` call and 1 `evaluate_line` call, with the jet's own arrays as the boundary, and 0 parent `metric_point` calls (totals {"jet": 12, "evaluate_line": 12, "super_metric": 0, "boundary_is_jet": 12});
- recomposing log(metric(evaluate_line(…, **tail.jet))) by hand equals `ctx.lnN` bitwise;
- the site is live: the tail moves lnN by 0.09–3.31 θ at these points.

State: digest `184823527b82bd34625462d52c1ffbc8a63ea14df2ab5aa8be03ac43868f124e`, config sha `21cedab8593528acb78afe36050469afec1b37a1399120f6b8dbef75a457fb54`, roster `a27fe3fc886d34cb5b07a2612fc56b5633d250eeb42bc15ab37de511a88beb03`; the roster equals the NQ base's.

## Item 4: an independent tail sharing no code with the module

**What is mine.** `tools/ngc_independent_tail_c4v001.py` imports none of: the tail library, the source roster, the Jn provider, any Codex1 file.
- **J0:** my own. Trapezoid below x = 25, Hankel asymptotic above; self-check 2.1e-15 against a 20,000-node integral up to x = 3000.
- **Source transforms:** my own Hankel transforms for stars and H2, which share the stellar sech² height; the gas rule (cubic Lagrange in s through the GL4 nodes, integrated in R); razor-thin gas, 156 present columns.
- **Quadrature:** my own (k⊥, ψ, k_z) scheme for cylinder(16) \ cube(2), with the corner zone integrated over exact ψ arcs.

**Registered source definitions loaded by pinned path** (as B3 did): the profile values, the H2 rows and tail scale, the HI annular Bernstein kernel, and forward_v002 `radial_surface`. The last two import only math/bisect.

**Points.** 48 points: rings 1, 7, 15 × azimuths 0, 5, 13, 22 × z ∈ {0, 10, −20, 30} kpc. Codex1's three points are included.

| quantity | value |
|---|---|
| module vs independent, t (relative to max\|t\|) | 5.3e-15 |
| module vs independent, grad t (relative to max\|grad t\|) | 1.0e-14 |
| my doubling (all quadrature widths halved): value / gradient | 8.2e-15 / 1.0e-14 |
| independent imaginary part (relative) | 6.8e-16 |
| max\|t\|, max\|grad t\| | 1.1e-08, 7.0e-28 /m |

**Criterion.** It was set before running: value ≤ 1e-10 and gradient ≤ 1e-9. These are far below what the N-tests resolve (θ/20 ≈ 1.7e-10 in lnN against \|t\| ~ 1e-8).

## 0539: NQ's exactly-zero delta, checked from bytes

| | base (`NQ_BASE_V001.json`) | fine (`NQ_FINE_V002.json`) |
|---|---|---|
| file sha256 | `11efaf8ed6766d4406810031235a15fb99be2b1d6ea1a5ad31bfcfdb1a79869f` | `8b5aa6d865ae823878236905840c1c72ef10a9879b59246b710541175b79fce8` |
| config sha | `21cedab8593528ac` | `cad9fa6de3f68fa7` |
| state digest | `781f1a71a3ea9b19` | `63e01868a86a02ec` |
| order; N⊥; N_z⁺ | 8; 26304; 18288 | 12; 77388; 54864 |
| w⊥, w_z actual (/kpc) | 0.005, 0.007 | 0.0025, 0.0035 |
| k⊥ panels (uniform / corner / uniform) | 400/253/2635 | 800/380/5269 |
| producer (radius tables) | c2v001, on-demand (n_eval_radii 0) | c2v005, precomputed (n_eval_radii 156) |

**The record pairs the right files:** CUBE16 = NQ_BASE_V001.json, NQ_FINE = NQ_FINE_V002.json.

**Bitwise identity.** The two lnN arrays are bitwise identical on all 28800 values (100 rings × 32 azimuths × 9 heights).

**The tail is not zero.** Against the tail-OFF N0 reads, it moves lnN by up to 5.77 θ (median 0.0048 θ). It changes N at 22392 of 22400 points.

**Why the zero is genuine.** lnN = log(N), with N in [0.9999986604, 1.0000002516].
- Every tail-induced change in N is an exact integer multiple of 2^-53 (TESTED from bytes on every point).
- So N, and therefore lnN, moves in steps of 3.3e-08 θ.
- My independent doubling bounds the converged tail's change under refinement at about 9e-23, which is about 1e-6 of one N step.
- So N does not move, and NQ reads exactly 0.0.

**Not a skipped refinement.** NQ can still detect a quadrature defect of more than one N step, and its θ/20 threshold is about 1.5e6 steps.

## Item 5: branch tests of the compare (in-process; nothing written to the author's folder)

`tools/compare_branch_tests_c4v001.py`, 40 of 40 passed:
- **Missing inputs read N_INCOMPLETE:** each of NQ, LO_NGC, NGC I1-T, N0–N4, and the C1′ evidence; also a failed LO_NGC, a failed I1-T, an untested NQ, and an unknown record.
- **N3 per 0512:** at θ/4 it passes; θ/4·(1 + 1e-9) fails, for both quantities and both pairs; a missing pair is a defect.
- **Other thresholds:** NQ fails above θ/20 and N2 above θ/4; N1 fails on a shape ring; a non-shape ring is reported only.
- **Order and defects:** NQ is read before N3; a flag contradicting its count is a defect; a defect precedes missing.
- **Reported only:** N4.
- **Real records:** the real LO_NGC (33bc2190) and I1-T (3ae7981a) certificates are accepted.
- **The v005 audit flow:** missing raw evidence reads N_INCOMPLETE; a raw contradiction reads N_NO_RUN; a missing manifest reads N_INCOMPLETE.

## Findings

- **F1 SHOULD_FIX. GQ for the NGC roster is not an input of the N-test compare.** RA7 registers GQ for the NGC T120L roster (to 32 /kpc). `certificates()` loads GQ_CERT_V003_KB128 but never checks its verdict or its NGC coverage, and `REQUIRED` in the compare omits it. So an N_PASS can be read without the registered GQ gate. The evidence exists and passes (GQ_CERT_V003_KB128: NGC [2, 46] ≤ 1.6e-15·P0). Fix: add GQ_NGC to REQUIRED, with verdict and coverage checks. This is stricter, and nothing else changes.
- **F2 NOTE. The NQ pair mixes evaluator versions.** The completed NQ base replay (`out/NQ_BASE_V001.json`, sha 11efaf8ed6766d44) was produced by the c2v001 evaluator (n_eval_radii 0, on-demand radius tables, no memory-guard field; 100 rings). The running NQ fine replay uses c2v005 (156 precomputed ring radii and the table-policy check). The NQ statistic therefore also contains the radius-table policy difference, which the fine run bounds at ≤ θ/2000 on three rings. That makes the test conservative, not lenient. Neither the record nor the compare names the producing evaluator. Fix: cite both producers in the NQ record, or rerun the base under c2v005.
- **F3 NOTE. R1's NGC tail block lists N_perp 25608; the module builds 26304.** The declared inputs match R1 (order 8, w_perp 0.005, w_z 0.007, K 2, cylinder K_big 16), and so do N_z_plus (18288) and the phases. N_perp is the panel count (400 + 253 + 2635) × 8. R1's figure looks stale; root should state N_perp as derived, as R1 does for DDO.
- **F4 NOTE. Codex1's independent spot check is narrow.** It shares the module's source roster and J0 transform, covers only three midplane points at φ = 0, and checks values only. This review's item 4 removes all three limits (below).
- **F6 NOTE. lnN has a resolution floor.** lnN is log(N) with N within ~1.3e-6 of 1, so it changes only in steps of one double near 1 (2^-53 = 3.3e-08 θ). Every N-test difference smaller than one step reads exactly 0.0, as NQ shows (0539). This is not a defect: the thresholds sit ≥ 1.5e6 steps above the floor. Records should say "below one N step" rather than imply an exact zero change.
- **F5 NOTE. The N1–N4 replays have not been run, and C1′ evidence is absent.** CUBE16 over all 156 rings, SPHERE16, CUBE8 and CUBE32 are pending, and NQ fine is still running. So the compare correctly reads N_INCOMPLETE today. The CUBE16 used for N1–N4 must cover 156 rings; the 100-ring NQ base would be refused (RING_COUNT_MISMATCH, fail-closed).

## Status of the N-test evidence at review time

| test | status |
|---|---|
| N0 | TESTED PASS (Codex1: 34,944 values; this review re-derived a sample) |
| NQ | base done; fine still running |
| N1–N4 | replays not run; C1′ evidence absent |
| compare reading | N_INCOMPLETE, as it should be |

**Codex1's real records** (`RECORDS_V001_MANIFEST.json`, sha `bb948591734529b41124020697a2a3faf899975f0492b4d53ad7f5f2548310c5`), read through its own compare in-process:
- outcome **N_INCOMPLETE**, with pending: N2: missing; N3: missing; N4: missing; N1: C1prime G160L/G120L evidence absent;
- no defects, so the raw-data audits of N0, N1 and NQ pass.

Under A60, NGC production K_big 16 is decided by N3, whose evaluator and compare logic pass here.

## Files (`tools/`, `out/`)

- **Harness:** `replay_harness_c4v001.py` runs Codex1's code under an open-audit hook that refuses target-like paths before open.
- **Independent tail:** `ngc_independent_tail_c4v001.py`.
- **Compare branch tests:** `compare_branch_tests_c4v001.py`.
- **Static scan:** `static_target_scan_c4v001.py`.
- **Hashes:** in `HASHES_REVIEW_NGC_NTESTS_C4V001.txt`.
