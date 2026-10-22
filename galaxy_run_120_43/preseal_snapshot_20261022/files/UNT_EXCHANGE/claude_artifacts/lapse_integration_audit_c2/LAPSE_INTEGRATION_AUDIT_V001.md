# NGC3198 route A, A2F10: lapse temporal/spatial integration audit (V001)

Claude2 lane, 2026-10-17. This answers the reviewer's request, forwarded by the principal, for a source audit of how the proper-time lapse is computed. The reviewer's three points are H1–H3; the root added H4.

**Scope.** The audit was read-only. Checks used numpy only, ran under nice with single-thread BLAS, and launched no runs. R2 convergence runs were not touched. No target or velocity file was opened, and no forbidden `result.json` was read. It consolidates four audit lanes and their independent verifications, all in this directory (`route_a_lapse/`, `route_b_stages/`, `theory_mapping/`, `m0_and_box/`, each with `verify/VERIFY.md`), and integrates the parallel replay `../ngc_route_a_freeboundary_c2/DIAGNOSIS_V001.md`.

**The case.** Run `NGC3198_ROUTE_A_A2F10_RUN_V001` failed at iteration 0, column 2503 (R 52.655 kpc, azimuth 7 of 32, plus side), with `FREE_BOUNDARY_NOT_BRACKETED` at z = 95 kpc and residual −6.137e-8. The A2F10 anchor is a target-free feasibility point. It is not calibrated for NGC.

**Path abbreviations.**
- H = `UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/`
- HC = H`coefficient_method/`, HR = H`recovered_packet_audit/`, HP = H`response_packet_audit/`
- prep = `ngc_route_impl_c2/route_a/install/recovered_packet_audit/ngc_actual_initial_source_preparation_v001.py`
- solver = `resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py`, sha `44d9c23c` (the file the run pinned)
- primer = `UNT_EXCHANGE/KNOWLEDGE/UNT_COORDINATOR_PRIMER_V002.md`

---

## 0. What the lapse computation is (code facts, TESTED-POSITIVE)

The lapse is one static linear response to the current baryonic source. Nothing in it integrates over time.

**Static metric.** "ds²=-N² c² dt²+g_X,ab dX^a dX^b, zero shift" (HC `owned_fourier_physical_metric_evaluator_v002.py`:9-10), with `N=1.+dx[0]` (:76).

**Source.**
- The source is the current source only: `current=fixed+gas; prepared=fourier_module.prepare(...)` (solver:111-112).
- It is baryonic rest energy only. The updated gas enters as `J=-e['rho_kg_m3']*c_m_s*c_m_s*e['proper_volume_m3']` (solver:190); the stars, H2 and initial HI are analytic J0 rings (prep:288-295).
- All non-lapse source components are exactly 0.

**Per-wave solve.**
- The solve is `x=np.linalg.solve(K,-f)` (HC `owned_complex_symbol_metric_binding_v002.py`:125), with K = Eref·(JᵀΓJ + contact) + K_EH (:81-98).
- The module describes itself as "a static material-chart branch at nonzero k, not temporal completion" (:31).
- The EH block is "NOT a retarded analytic continuation" (HP `owned_static_action_metric_binding_v002.py`:13).

**Coefficient grid.**
- Grid `2e3a36d8` is `F = -(cov + contact)  # beta = 1`, an equal-time covariance pooled from 4 L=4 chains (`pooled4.py`:15-22, 35-36, 62). It is placed on a 4×4×4 lattice-momentum grid with 10×10 field blocks.
- The grid has no time or frequency axis.
- Its sampler integrals run over "the sampler's imaginary-time circle, not physical rates" (`owned_L4_current_graph_cycle_recipe_v001.py`:45).
- The run's IDENTITY digests equal the pooled file's: 0bf5bb6a, C̄ ff264e09, μ̄ dbca72dd.

**The only integration bounds that exist are spatial-spectral.**
- k-space quadrature: a non-periodic composite Gauss cube over [−2, 2]³ /kpc (prep:126-157), G80C, 80 nodes per axis, 512,000 waves.
  - Axis node spacing runs from 2.254e-3 to 1.042e-1 /kpc (ratio 46).
  - The smallest axis node is 1.127e-3 /kpc.
  - k = 0 is excluded (prep:55-56; Fourier v005:84).
  - Boundary perturbations are zero (prep:269-273, 283).
- Real-space inverse: an exact finite sum δn(z) = Σ e^{ik_z z}·line (HR `owned_fixed_xy_fourier_line_v001.py`:46-53).

**Free boundary** (HC `hi_two_sided_free_boundary_v002.py`).
- Threshold: `h0=g*sig*sig/(g-1); threshold=math.log1p(h0/(c*c))` (:41), which gives 3.3658e-9.
- Residual: `logratio(z)-threshold` with `logratio = ln N(z) − ln N(0)` (:60-62).
- Search: outward steps of 0.2 kpc out to `hi_search_limit` 95 kpc (:64-77).
- Edge condition: `u=1+(1+c*c/h0)*math.expm1(-lr)` reaches 0 (:97).

---

## H1: Artificial temporal truncation. TESTED-NEGATIVE (no counterpart)

**Lines and bounds.** No time variable, lookback, history convolution, retardation or memory cutoff exists anywhere in the lapse path.
- Files searched: the 19 pinned route-A modules, prep, solver, worker and binding, and the route-B drivers v006/v007/v008 with their 11 stages.
- The citations in §0 (:31, :13, :9-10, :111-112) are the governing lines.

**False hits.**
- `history` is the iteration-residual list (solver:81).
- `chunk` is exact memory blocking of complete sums. Loops have the form `range(0,len,chunk)` capped by `min` (HR `axisymmetric_initial_rest_energy_fourier_v001.py`:31-34; HR `baryonic_metric_source_columns_v003.py`:194-204). `_chunks` splits route-B workers (v008:1555).
- `BIND` is a path constant (v008:134).
- The STAT:15 "mode convolution" pairs Fourier modes. It has no time axis.

**"120 chunks".** This is not a memory limit. "Historical 120 is the former four-column/thirty-chunk partition, not a mandatory current run count" (primer:884). The word `120` has 0 hits in the drivers and stages.

**"Bind".**
- In code, Bind is a native sampler move that "flips one record bit q_v" (`owned_collective_worldline_static_response_pairallk_v003.py`:214). Its trial amplitude is g = 0.1, inside the equilibrium sample only (`owned_L4_admission_family_recipe_DRAFT_v001.py`:44-46).
- In program documents, the dark-matter identification "Γ-level macro-loop tension generated by the Bind operator" is [HYPOTHESIS] (primer:103) and [UNTESTED] (primer:131). The primer lists "P-c: the 120/43 kernel carries no Γ" as an open conflict (primer:765-768).

**"Bind deficit", "Γ-strain wake", "topological wake".** These have no counterpart in code. The only related "wake" is an earlier reviewer proposal that the root assessed and did not adopt (CURRENT_INSTRUCTIONS.md:161).

**Conclusion.** Route A counts zero Bind history by construction. Nothing is cut off inside a history integral, because no such integral exists.

**Open.** Whether adding a Bind-history term would confine the outer gas is UNTESTED. Deciding test: no derived term exists. The precondition is the Line-A first finite exit (primer:131).

## H2: Quantum record relaxation τ. TESTED-NEGATIVE (no counterpart)

**Lines and bounds.** No decay rate, τ, or diffusion constant parameterises the lapse (§0 modules; v006–v008).

**The only "relaxation"** is numerical damping of the source iterate: `gas=_finite((1-relaxation)*gas+relaxation*updated,'relaxed gas')` (solver:215), with seed value 0.5 and a guard at solver:66. It is applied after a full column pass, and the failure happened inside the first pass. It therefore never acted.

**The only τ** in the chain is the sampler's MCMC autocorrelation time (`tau_ceiling.py`). It is a convergence statistic and failed its criterion (0/36 blocks, SAMPLER_EVALUATION_V001.md:11-12, 22). It is not a physical rate.

**Reviewer terms.**
- "Hadron" has 0 hits outside vendored CLASS/HyRec files.
- "Gamma-protected record" appears only as an unbuilt stability goal (Line-A V013:5; PRINCIPAL_PREMISES_REGISTER_V001.md:61). It is a different term from "gauge protection", and the two were not mapped onto each other.

**The τ_Q memory kernel the reviewer proposed separately** (`REVIEWER_PROPOSAL_K_TAUQ_ASSESSMENT_V001.md`) is TESTED-NEGATIVE as a mechanism. τ_Q = t_P·e^{1/α_s} ≈ 2.6e-40 s, about 52 orders of magnitude below the needed memory time.

## H3: m=0 axisymmetric eradication. TESTED-NEGATIVE, and reversed

**Route A does not use an m=0 projection.**
- The solver states "No axisymmetry imposed on response" (solver:50).
- Columns are φ-resolved at (R cos φ, R sin φ, z) (solver:129-150; line v001:28-31).
- Only the iteration-0 source is axisymmetric, by declaration (prep:288-295). The response is a full 3-D sum.

**The m=0 projection is a route-B operation** (root decision A1:40-46). It averages over φ at fixed (R, z), `'logN':math.fsum(logs)/n_phi` (reference v003_gal_c2v001:37, 44-61). It never averages over polar angle, so it cannot spherise the field, and the z-dependence is kept exactly.

**Measured at R = 52.655 kpc.**
- The 32-azimuth m=0 mean of ln N(z) − ln N(0) is +4.69e-9 at 10 kpc, +1.54e-8 at 30 kpc and +1.67e-8 at 38 kpc.
- 31 of 32 azimuths bracket on the plus side. Only azimuth 7 (plus side) fails, along with its inversion image, azimuth 23 (minus side).
- So the m=0 average helps bracketing on this cube.
- Caveat (TESTED-POSITIVE): the cube error is 1.4× the threshold here. In an isotropic continuum the m=0 margin is about 1.03× rather than about 5×, so this cube cannot decide the size of that margin.

**The reviewer's premise is also contradicted.** A smeared spherical halo would make the lapse rise with distance and help bracketing. The observed profile instead falls: ln N(95) − ln N(0) = −5.80e-8.

**Open.** Whether the per-azimuth route-A column solve is what A1 intends for a route feeding m=0 route B is a route-A design question (UNTESTED).

## H4: Periodic box / k_max truncation. Periodic images TESTED-NEGATIVE; quadrature error TESTED-POSITIVE as a secondary factor

**No box.**
- The cube is a non-uniform Gauss quadrature (spacing ratio 46), so it has no period.
- Replay check: max |lnN(z + 272.97) − lnN(z)| is 2.3e-7, against max |lnN| of 1.1e-7 (DIAGNOSIS §2).
- 272.97 kpc is only the k_min coverage length, "kmin check only…nonperiodic Gauss cube" (v008:3675-3703). It is not a period.

**Low-k content is resolved in z.** The z-phase of the |k| < 0.1 panels is resolved out to 89–361 kpc (DIAGNOSIS §2). The large-z fall is therefore not z-aliasing.

**k_max (2 /kpc).** Keeping only |k| ≤ 0.3 changes ln N(95)/N(0) from −5.80e-8 to −5.62e-8. The far-field fall is a low-k effect and is insensitive to k_max (TESTED-POSITIVE).

**Transverse under-resolution exists (TESTED-POSITIVE).**
- At R ≳ 50 kpc the transverse coordinates exceed the resolution heights of the [0.1, 2] panels.
- On cube-axis columns, a Newtonian point mass through G80C is off by +396% to −1603% in δn (R 52.7–120 kpc, az 0/4). At column 2503 (az 7) it is within 4.2%.
- 124 failing columns (az 0/8/16/24, R 69.8–136.3 kpc, 1.1% of failing mass; column 2503 not among them) still fail with a purely attractive 8.06·T_N symbol.
- At thresholds near 52.7 kpc, cube errors are comparable to the threshold.

**Open.** Whether those 124 columns confine under an accurate quadrature is UNTESTED. Deciding test: a refined transverse quadrature (refined [0.005, 0.3] panels or G80E14), or a direction-by-direction real-space evaluation on those columns.

---

## What the failure is most consistent with (verified evidence)

### 1. Primary cause: the lapse symbol turns repulsive at long wavelength

**Status:** TESTED-POSITIVE as a measured property of the installed operator. Whether it is response physics or a coefficient artefact is UNTESTED.

**The symbol.** Define T(k) = x̃_n/f_n. It reproduces the saved iteration-0 responses to ≤2.6e-14.
- For |k| ≥ 0.3 /kpc, T/T_N ≈ 7.9–8.06 (attractive), where T_N = 4πG/(c⁴k²).
- T changes sign at about 0.017 /kpc along z, 0.021 along x/y, 0.031 along [110] and 0.037–0.040 along [111]/[101].
- T(0) is finite: −39.73 m³/J in every direction. The field therefore has no 1/r tail. T/T_N ∝ k² holds only for k ≲ 0.003 /kpc and levels off near −8 to −11 at 0.005–0.01 /kpc.
- The low-k solves are well conditioned (condition number ≤ 87).

**For a point mass.** The effective coupling changes sign at r ≈ 18 kpc, and the lapse peaks at about 53 kpc. Beyond that the potential turns over.

**This produces the monotone large-z fall.**
- The |k| < 0.03 shell alone gives −6.1e-8 at 95 kpc in column 2503.
- An isotropic continuum evaluation with no cube shows the same fall.

**Counterfactuals on the same quadrature and source** (diagnostic only):

| Change to the symbol | Effect |
|---|---|
| Zero the T<0 nodes | Confines column 2503 (+14.0 / −9.8 kpc) and 94.6% of the failing mass |
| Replace \|k\|<0.1 by 8.06·T_N | Confines 98.9% of the failing mass |
| Same Newtonian-shape symbol (column 2503 only) | Crosses the threshold at 26.6 kpc |

**Scope of the failure** (DIAGNOSIS §3).
- 1808 of 2489 replayed columns are unconfined to 500 kpc. Raising the search limit to 136.5 kpc rescues 0. Option (a) is not viable (TESTED-NEGATIVE).
- The failing columns cover R = 52.655–136.3 kpc and a mass fraction of 2.55e-4.

**Source of the sign.**
- The EH block has an exactly zero nn entry; its other terms are O(k²) (HP static v002:168-206). So γ reaches the lapse only by mixing with the other 9 fields.
- The k → 0 limit is set by the sampled native block at the L=4 uniform mode `grid[0,0,0]`.
- The superseded V004 grid also reverses sign (T(0) = −159.3, crossing at 0.003–0.020 /kpc).
- Single-chain N–N entries range from −5.20 to −1.76 (SAMPLER_EVALUATION_V001.md:88).
- The sampler's equilibrium is not established: the Birth census is non-stationary (:75).

### 2. Column-2503-specific margin: a z-odd operator component

**Status:** TESTED-POSITIVE. The carrier within the operator is UNTESTED.

**Column 2503's own profile.**
- The plus-side rise peaks at 3.205e-9 (0.952 of threshold) at 30 kpc and then turns over (cause 1).
- The minus side brackets at 9.0 kpc.

**The response is mirror-asymmetric; the source is not.**
- The source is z-even and real to 7e-18.
- The response changes by 0.22 under kz → −kz, 0.30 under kx → −kx and 0.38 under a 90° rotation.
- Only full inversion holds (8e-16).
- Nodes and weights are mirror-symmetric, so the asymmetry is in the operator.

**Symmetrising the operator restores the crossing.** Symmetrising over z-reflection alone gives a plus-side crossing at 13.5 kpc (D4h: 12.5; Oh: 13.5). This was checked at the lapse level for column 2503 only; it was not a gas re-solve.

**Candidate carriers (UNTESTED).**
- C̄ off-diagonal yz = 4.36e-3
- background μ (0.0118, 0.0012, 0.0105)
- Im parts of the grid, up to 0.223
- 4³ Monte Carlo noise

**The exact 52.7 kpc onset is sensitive at about 5%.** Several perturbations each rescue column 2503: symmetrisation, |k| ≤ 0.3 truncation, and zeroing T<0. Its individual failure is therefore overdetermined. The outer-disk unconfinement is robust (cause 1). The isotropic continuum places the loss of confinement between 52.7 and 56.4 kpc.

### 3. Secondary: cube-axis quadrature error (H4 above)

This is TESTED-POSITIVE for 124 columns, or 1.1% of the failing mass.

### Not supported by any evidence

Temporal truncation, a relaxation rate, m=0 spherisation and periodic images (H1–H4 above).

---

## Open items and deciding tests (all target-free, none launched)

| # | Claim | Status | Deciding test |
|---|---|---|---|
| U1 | The low-k sign change is faithful response, not an L=4 `grid[0,0,0]` finite-size/ensemble artefact | UNTESTED | Per-node T(k) from the 4 single-chain grids in `CANDIDATE_4CHAIN_POOLED_GRID_V001.npz` (per-node symbol solves only); then a larger-L capture and compare the k=0 block and k_c |
| U2 | How k_c depends on the anchor (Eref, γ) | UNTESTED | Run `route_a_lapse/tools/transfer_scan_v001.py` across the A2 sweep and the factor-3 anchor, tracking the near-singular 9×9 mode (σ_min/σ_max ≈ 1.2e-3 at the z crossing) |
| U3 | The carrier of the z-odd component | UNTESTED | Rebuild the response with C̄ off-diagonals zeroed, then μ̄ = 0, then a z-mirror-symmetrised grid, one at a time; re-read azimuth 7 |
| U4 | The axis columns confine under accurate quadrature | UNTESTED | Refined [0.005, 0.3] panels / G80E14 re-prepare, or real-space evaluation on az 0/8/16/24 |
| U5 | The failing set is the same in iterations ≥ 1 | UNTESTED | Needs an iteration-1 operator; none exists |
| U6 | Disk orientation sensitivity (A1-orientation) | UNTESTED | Rerun with the disk axis along each C̄ principal axis and along [111] |

---

## Classification of candidate fixes (classification only; no adoption recommended)

### Counted numerics (target-free; same operator and source law)

| Candidate | Classification |
|---|---|
| Refine low-k / transverse panels, G80E14, k_max extension | Numerics, already under A1-numerics. Expected to address cause 3 and the margin of cause 2; it cannot remove cause 1, because the continuum shows the same fall |
| Direction-by-direction or real-space evaluation of the same symbol | Numerics |
| Raise `hi_search_limit` (N4) | Numerics, TESTED-NEGATIVE (0/1808 rescued) |
| Truncate the route-A gas roster at R ≲ 51.7 kpc (mirrors N2) | Counted domain choice. Needs prep v002 and review. Viability is UNTESTED, and its effect on the field at R ≤ 44 kpc is UNTESTED |
| Better estimate of the same coefficient functional (per-chain comparison, larger L, longer chains) | Estimation numerics, target-free. Adopting a replacement grid is a root decision, as A2 was |
| Disk tilt family | Counted orientation sensitivity (A1:45) |

### Model changes (new physics or construction changes; framing gate and review required)

| Candidate | Classification |
|---|---|
| Symmetrising the kernel over z-reflection or the cube group | Modifies the kernel, against "the kernel is unmodified" (A1-response). Numerics only if U3 shows the asymmetry is sampling noise |
| Zeroing T<0 or splicing a Newtonian/8.06·T_N low-k tail | Imposes a far-field law. Model change; diagnostic counterfactual only |
| Moving the k→0 native susceptibility out of the dynamical kernel into the once-only matching (CPLX:29-30) | Construction change requiring review |
| Changing σ0 or Γ | Adopted physics assumptions. Not numerics |
| A Bind-history / Γ-strain wake source, or a τ_Q memory kernel (reviewer H1/H2) | New physics with no derived term. Requires the framing gate (lineage, prior work, imports ledger, principal sign-off). τ_Q as written is TESTED-NEGATIVE |

---

## Errors register (corrections absorbed from verification)

1. The zero-mode guard is at prep:55-56, not :57.
2. The "Rise error ≤ 30% at small z" claim is refuted. The error is 85× at 1 kpc, 9× at 5 kpc and 3× at 10 kpc; 28% applies only at 30 kpc.
3. "The quadrature reproduces the far field" holds only off-axis (az 7). It fails on cube-axis columns.
4. The continuum value −5.68e-8 agrees with the cube only on the sign of the fall. Compared with the cube's m=0 mean (−3.74e-8), it differs by 34%.
5. "The native term couples only up to 3 cells" is wrong for the kernel. F(k) stops at 3 cells, but F_jj⁻¹ gives an exponential tail of about 2e-4 at 12 cells (≈ 26 kpc).
6. Route-B gating is sequential. In v007/v008 a failed route A ends as `ROUTE_A_NO_FIXED_POINT` (v008:1455) before the strict reader (v008:1461) runs. v006 stops at v006:1315.
7. The "route B would lose confinement at 65 kpc" survey is withdrawn. The cube creates spurious brackets at large R.
8. "Sampled in thermal equilibrium" is overstated. The sample is equal-time at β = 1, but equilibrium is not established.
