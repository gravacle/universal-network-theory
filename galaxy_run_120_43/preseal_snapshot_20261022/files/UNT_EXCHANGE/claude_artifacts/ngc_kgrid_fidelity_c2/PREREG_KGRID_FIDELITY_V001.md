# PREREG_KGRID_FIDELITY_V001: NGC3198 route-A k-grid fidelity (preregistration only)

**Status.** Preregistration only. At write time no refined-grid operator, field, replay or criterion value exists.
- Machine-readable twin: `PREREG_KGRID_FIDELITY_V001.json`, sha256 `4c2eefeb8a4e191d20173036fe0aa5e641799c70a97b96d354d0984742449869`.
- That JSON was written by `tools/build_prereg_v001.py` (`e50e4efa…`). The builder does only arithmetic on the grid definitions plus sha256 of the 38 cited inputs, taken from bytes. It refuses on any digest mismatch.
- The JSON is authoritative wherever the two files differ.
- Mandate: root decision A11 item 2 (V003 addendum `84e993d2`).
- Diagnosis: `ngc_route_a_freeboundary_c2/DIAGNOSIS_V001.md` (`bdb02a64`). Its check: `check/CHECK_V001.md` (`1a2d29ff`).

**Fixed, not varied.**
- kmax = 2 /kpc on the full signed cube.
- The A2 pooled coefficient grid `2e3a36d8`.
- Seed `88ef386d`: every value except `composite_grid_spec`.
- The HI controls.

The coefficient-grid dependence of the k→0 sign change belongs to `long_wavelength_response_c2/` and is not duplicated here.

**Hygiene.**
- No NGC3198 target or velocity file is opened.
- No speed or radial derivative of the program operator is computed at any radius. C3 is evaluated on synthetic known fields only.
- No KMAX_/D7R/V005/V006/V007/DECIDING `result.json` is opened. The G80C run's own `result.json` is not opened either: its timing comes from `progress.jsonl` and the receipt.
- Nothing is launched.
- Runtime: codex python `-I -B`, numpy only, `nice -n 10`, BLAS threads 1, at most 6 processes.

## Grid-ranking evidence behind G80C (read)

**Why G80C was chosen.** Root N4 chose G80C, "ranked first by the checker on the derivative metric". That ranking is 0473 CHECK D3 (`5c748489`). It used max|ΔdU|/max|dU_ref| on N2-B toys, where G80C beat G80D.

**What later reviews found:**
- NG2 F9 (`8f57560c`): the metric is normalized by the inner maximum, so it hides the outer error.
- NG2 measured G80C, all synthetic:
  - ≤ 0.07% out to 32.1 kpc;
  - 9.5% speed error at Q43;
  - a field dominated by grid error beyond 45 kpc.
- N2 (`d1e723e7`) defined G80E14. It is not installed in any seed or code, and the prep v001 guard accepts it (`0bad3976`).
- NG2 reports that adequacy at 44 or 66.9 kpc needs about 120–160 nodes per axis, which is over the prep v001:142 cap.

## Measured G80C baseline (RUN_V001; progress.jsonl and receipt)

| Quantity | Value |
|---|---|
| Iteration-0 preparation | 418.47 s |
| Waves | 512,000 |
| Peak RSS | 1.123e9 B |
| Time per metric call | 4.378 ms (229,102 calls over 2503 columns in 1003 s) |

## (1) Candidate grids

- Breaks per side: [0, .01, .03, .1, .3, 1, 2] /kpc. Orders are listed per side, from k = 0 outward.
- W = n_x·n_y·n_z.
- Cost columns are linear-in-W estimates from the G80C baseline (premise P2, UNTESTED). "Eval s" is the upper bound for one full evaluation.
- Heights use the N2 formula X ≈ 8n/(eΔ), for the [0.3,1] and [1,2] panels. They are FORMAL properties of the grid definition, not results.

| Id | Tier | Axes (x,y,z) | Orders per side | W | Prep s | RSS GiB | Eval s | X [0.3,1] / [1,2] kpc |
|---|---|---|---|---|---|---|---|---|
| G80C (control) | 1 | 80³ | 3,3,4,5,10,15 | 512,000 | 418 | 1.05 | 1898 | 42.0 / 44.2 |
| G80E14 | 1 | 80³ | 2,2,3,5,12,16 | 512,000 | 418 | 1.05 | 1898 | 50.5 / 47.1 |
| G80L | 1 | 80³ | 2,**6**,3,5,10,14 | 512,000 | 418 | 1.05 | 1898 | 42.0 / 41.2 |
| G80EL | 1 | 80³ | 2,4,3,5,11,15 | 512,000 | 418 | 1.05 | 1898 | 46.3 / 44.2 |
| G96F | 2 | 96³ | 3,3,4,6,13,19 | 884,736 | 723 | 1.81 | 3279 | 54.7 / 55.9 |
| G96FL | 2 | 96³ | 3,6,4,6,12,17 | 884,736 | 723 | 1.81 | 3279 | 50.5 / 50.0 |
| T120L | 2 | 120²×80 (z = G80L) | 3,6,5,8,16,22 | 1,152,000 | 942 | 2.35 | 4270 | 67.3 / 64.8 |
| G120L | 2 | 120³ | 3,6,5,8,16,22 | 1,728,000 | 1412 | 3.53 | 6405 | 67.3 / 64.8 |
| T160L | 2 | 160²×80 (z = G80L) | 3,8,6,10,22,31 | 2,048,000 | 1674 | 4.18 | 7591 | 92.5 / 91.2 |
| G160L (reference) | 2 | 160³ | 3,8,6,10,22,31 | 4,096,000 | 3348 | 8.37 | 15182 | 92.5 / 91.2 |

- **Panel refinement of [0.01, 0.03].** This panel contains the A0(k) sign change (checker F3). It is refined in every `L` variant and in G80EL.
- **G80E14 coarsens that panel to order 2** (FORMAL).
- **Tier 1** stays inside prep v001 (`c54c7cc9`). It needs only a seed-level `composite_grid_spec`, set through a seed-builder successor, because build_seed_v002 has no grid flag.
- **Tier 2** needs a reviewed NGC prep successor: :142 caps nk ≤ 80, and :155 uses one axis for kx, ky and kz. For diagnostic evaluation it is prepared through the H-OVR harness, defined in the JSON as the k-set override plus a recompute of the analytic sources. The checker must review the H-OVR diff before it is used.
- **Nominal total for all ten:** 13.2 CPU-hours.

## (2) Acceptance criteria (all four must pass)

**θ** = log1p(h0/c²) = 3.3657664138980042e-9, the HI free-boundary threshold (hi v002:41).

**C1 — ring φ-spread.**
- For each ring, S = max_φ lnN0 − min_φ lnN0 over the 32 roster azimuths of the iteration-0 operator.
- Pass: S < θ for **all 100 roster rings with R ≤ 66.904 kpc** (N2 domain; 0.705–66.722 kpc).
- Known on G80C: FAIL (TESTED), with S/θ = 2.04 at 13.584 kpc and 12.78 at 52.655 kpc.

**C2 — known-field 30 kpc vertical difference.**
- Statistic: max over the 79 rings with R ≤ 52.7 kpc and the 32 azimuths of |Dq − Dx|/|Dx|, where D = Φ(R,φ,30) − Φ(R,φ,0).
- Pass: ≤ 1% for every field.
- Fields:
  - **K1:** a Gaussian-smoothed point mass, 4π e^{−k²a²/2}/k², with a = 3, 5 and 10 kpc.
  - **K2:** the actual-shaped isotropic symbol T_iso(|k|)·e^{−k²a²/2}. T_iso is T along ẑ, computed with the pinned modules on A2 `2e3a36d8` (method of verify_lapse_v002 (b)). Its reference is a 1D radial integral converged to ≤ 1e-6.
  - A zero guard applies where |Dx| < 0.05·max|Dx|.
- Known on G80C: FAIL. K1 a = 3 gives 63% at 52.655 kpc and 20% at 46 kpc.

**C3 — known-field radial derivative D = R dΦ/dR at z = 0.**
- Radii: 175 target-free radii, 0.70 + 0.25j kpc up to 43.95, plus 44.08 kpc.
- Estimator: E12, the mean over the 12 observation azimuths.
- Fields: K1 and K2 as in C2.
- Pass: relative error ≤ **0.5%**.

How the 0.5% follows from the τ convention:
- Convention: τ_i = 0.25 σ_i (KMAX prereg V005 `dbddc02c`, root decision (a)).
- Speed proxy: v² = c² R dlnN/dR, so ε_v = ε_D/2.
- Requiring ε_v·v ≤ σ/4 gives ε_D ≤ σ/(2v).
- No NGC σ or v is read. Declaring σ_ref/v = 1% (premise P3, DECLARED) gives ε_v ≤ 0.25% and ε_D ≤ 0.5%.
- For any later-scored row with σ_i/v_i < 1%, the bound exceeds τ_i by 0.01·v_i/σ_i. That check is registered for the post-freeze scoring lane.

**C4 — vertical-profile convergence on the operator itself.**
- Statistic: e4 = max |dL_G − dL_ref|, with dL = lnN(z) − lnN(0) at z = ±10, ±20, ±30 kpc, over all 100 rings and 32 azimuths.
- Pass: e4 < θ/2.
- Reference: G160L. G160L itself is compared against G120L.
- Why C4 is needed: C1–C3 do not test the vertical lapse profile that the free boundary reads.
- Agreement here is necessary, not a certificate. G160L must itself pass C2 and C3.

**Never criteria.**
- Replay confinement and roots.
- Anything at query radii on the operator.

**Reported, not decisive:**
- Replays of rings **2496 (52.655 kpc), 2560 (53.714 kpc) and 3360 (81.178 kpc)**: 96 columns, at (95 kpc, 1024 calls) and (136.5 kpc, 2048 calls), using checker replay_c1. Ring 3360 is the first roster ring ≥ 80 kpc that fails on all 32 columns on G80C. Ring 3328 (80.474 kpc) is reported as INFO.
- S/θ beyond 66.904 kpc.
- Harmonics m = 1–16, including the share in m = 4, 8, 12 and 16.
- C2 at 95 and 136.5 kpc.

**Gates before any criterion is read.** If any gate fails, the result is GATE_FAIL and nothing is read.

| Gate | Requirement |
|---|---|
| V1 | The tier-1 path on G80C reproduces the run's iteration-0 START blobs bitwise |
| V2 | H-OVR on G80C and on G80E14 reproduces the tier-1 arrays bitwise |
| V3 | Ring 2496 lnN0 equals RING_PHI_C1, and column 2503 fails byte for byte |
| V4 | ANISO_C1 is reproduced to 1e-12 |
| V5 | The roster digest equals IDENTITY `gas_columns` |

**Premise P1.**
- The claim: the true lnN0 of an axisymmetric source does not depend on φ.
- Status: UNTESTED.
- Why it is open: root A1 says the kernel is anisotropic, and declares only the cube-corner m = 4 and m = 8 structure numerical.
- Deciding observation: D-SPLIT, which classifies each ring that fails C1 using the two finest grids and a sphere-masked G160L:

| Class | Condition |
|---|---|
| QUADRATURE_LIMITED | S drops by ≥ θ/4 on refinement |
| TRUNCATION_SHAPE | Otherwise, and the sphere mask lowers S by > θ/2 |
| NOT_GRID | Neither of the above |

## (3) Decision rule

**Evaluation order:**
1. **Phase 0:** gates.
2. **Phase 1:** the four tier-1 grids.
3. **Phase 2:** G160L.
4. **Phase 3:** only if no tier-1 grid passes, the tier-2 grids in ascending W (G96F with G96FL, then T120L, G120L, T160L). Stop after the first W level that contains a passer. G120L is always run if G160L is the only grid passing C1–C3.

Nothing in this prereg changes after Phase 0 starts. Any change is a new version with a new sha.

**Adoption.**
- A candidate passes when V1–V5, C1, C2, C3 and C4 all pass.
- Cost is W. Ties go to tier 1 first, then to list order.
- **The minimal-cost passing grid is adopted for NGC route A.**
  - `ADOPT_<id>` (tier 1): seed-level grid change. Any relaunch stays gated by root A8/A11, which wait on the long_wavelength verdict.
  - `ADOPT_PENDING_PREP_SUCCESSOR_<id>` (tier 2): next step is prep v002 plus pins and review. The projected per-iteration cost is reported against the 21600 s wall cap.

**Compute cap.**

| Limit | Value |
|---|---|
| CPU | 36 CPU-hours |
| Wall | 12 h from the start of Phase 0 |
| Processes | at most 6 |
| RSS per process | 12 GiB, checked by a pre-probe; a grid over the cap is NOT_EVALUATED_OVER_CAP |
| RSS in total | 32 GiB |

Grids not evaluated before the cap count as not passing.

**If nothing passes: `NO_ADEQUATE_GRID` (or `_WITHIN_CAP`).**
- Per A11, option (b), truncating the route-A gas roster, becomes the counted fallback.
- Registered limit of (b): on G80C, C1 already fails from 13.584 kpc (TESTED), so (b) does not remove the φ-error inside its 51.746 kpc cut.
- The next step depends on the D-SPLIT class:

| Class | Next step |
|---|---|
| QUADRATURE_LIMITED, or failures only in C2/C3/C4 | Axes of ≥ 200 nodes (needs a prep successor), or a spherical-shell reference on the same operator |
| TRUNCATION_SHAPE | The A1-numerics kmax 3–4 / sphere test for NGC, which is not covered for NGC3198 (NG2 F4) |
| NOT_GRID | Register in-plane response anisotropy as an operator property (P1 falsified). The next deciding item becomes the route-A question of per-azimuth versus m=0 columns (audit H3) |

## Files

| File | sha256 |
|---|---|
| `PREREG_KGRID_FIDELITY_V001.json` | `4c2eefeb8a4e191d20173036fe0aa5e641799c70a97b96d354d0984742449869` |
| `tools/build_prereg_v001.py` | `e50e4efa8d2396259e0747aadc70c5f72654032870f391db66b7a64d153e6cdb` |

This md is not self-hashed. Its sha256 is in `HASHES.txt`. `check/` is empty and left for the checker.
