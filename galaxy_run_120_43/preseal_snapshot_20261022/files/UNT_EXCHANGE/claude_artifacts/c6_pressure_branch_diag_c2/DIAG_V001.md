# C6 pressure-branch refusal: diagnostic V001 (Claude2)

**Scope.** This is a read-only study. It replays the pinned route-A readout on saved converged checkpoints. Nothing was launched. C5's call-level result.json was not read, and no NGC3198 target was opened. The numbers are in `DIAG_V001.json`; hashes are in `HASHES.txt`.

**Labels** follow the program convention: TESTED, PLAUSIBLE, UNTESTED.

## 1. Call chain and what the readout is for (TESTED, code)

The failure path runs through five files:

| Step | File | Lines | What happens |
|---|---|---|---|
| 1 | driver v009 `999331af` | L2252–2280, L2276 | Builds the parallel route-A request |
| 2 | worker `9dbdaf11` | L103 | Calls the binding |
| 3 | binding `d81b24b7` | L91–102 | Solves for the checkpointed fixed point |
| 3 | binding `d81b24b7` | L104–115 | Calls prediction v005 with 8 equal azimuths 2πi/8 |
| 4 | prediction v005 `54136c71` | L118–136, L128 | `local(φ)` calls `pressure_streaming_speed` |
| 5 | `galaxy_baryonic_source_forward_v002` `e9be043b` | L189–209 | Computes v²/c² = (dlnN+pgrad)/(dlnR+pgrad); refuses at L207–208 unless 0 ≤ v² < 1 |

**What the readout is.** It is the circular-streaming **trial** row set that prediction v005 computes after convergence:
- `predictions_available_semantics` is `CALCULABLE_TRIAL_ONLY`.
- `dynamics_status` is `UNASSESSED_CIRCULAR_TRIAL`.
- `accepted_for_calibration` is False.

**Who reads it.** The driver only records the rows (v009 L2318–2319, `info.route_a.route_a_rows`). No route-B stage and no compare script reads them. Route B reads the converged checkpoint instead, for example `rotation_v005_gal_c2v004` at L209 and L242.

**Why C6 has no result.** Route A converged at iteration 8 (residual 2.746e56 ≤ bound 3.487e56). The refusal came afterwards, in this diagnostic-only readout. The worker then wrote failure.json and no result.json (L114–118), so the call stopped with `valid=false`. Route B never ran, even though a valid fixed point exists.

## 2. Where it fails (TESTED, bitwise replay)

**Replay checks.**
- The replay rebuilt the readout of C5 query 01 from the saved checkpoint, bitwise equal to the saved C5 node.
- The K2–K5 roster nodes at R = 1.48 kpc also replay bitwise.

**C6 exact replay.** It uses the pinned `prediction.evaluate`, a stub coupled module holding the iteration-8 START prepared response, and a recording streaming wrapper. It raises at **call 86**:
- query `DDO154_SPARC12_03`, **R = 1.48 kpc, φ = π/4**;
- queries 01 and 02, and query 03 at φ = 0, all passed before it.

Values at the failing call:

| Term | Value (per metre) |
|---|---|
| dlnN_dR | **−1.967e-29** |
| dln√gφφ_dR | 2.190e-20 |
| pgrad = dP/(ε+P) | −2.240e-29 |
| numerator | **−4.207e-29** |
| denominator | +2.190e-20 |
| v²/c² | **−1.921e-9** |

**Full C6 sweep** (12 radii × 8 azimuths × 5 including stencils = 480 calls):
- 20 calls refuse, all of them query 03, at the four diagonal azimuths π/4 + jπ/2 and their stencils.
- No radial-resolution test fails.
- The other 11 radii pass everywhere. The smallest margin is at R = 2.96 kpc: numerator 0.42e-28, pressure/lapse ratio 0.39.

**Radial profile at φ = π/4** (dlnN_dR, e-28 /m): the refusal zone is about R ≈ 1.38–1.60 kpc.

| R (kpc) | 1.20 | 1.30 | 1.40 | 1.48 | 1.56 | 1.65 | 1.75 | 1.85 |
|---|---|---|---|---|---|---|---|---|
| dlnN_dR | 1.37 | 0.52 | −0.07 | −0.20 | −0.03 | 0.41 | 0.99 | 1.45 |

**Same point vs k_max** (R = 1.48, φ = π/4, numerator e-28 /m):

| K | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| numerator | 1.42 | 1.46 | 1.97 | 0.80 | −0.42 |

C4R3 and C5 pass this readout; C6 refuses.

## 3. Verdict (TESTED unless marked)

**The failing side is v² < 0.** The ≥ 1 side is not involved: the denominator is about 5e8 times the numerator.

**The lapse drives it.**
- The lapse gradient itself is negative at the diagonal azimuths; the lapse decreases outward.
- The HI pressure term has the same sign and supplies 53% of the negative numerator.
- With zero pressure, v² would still be negative.
- So it is not asymmetric-drift-dominated. The azimuthal-mean pressure/lapse ratio at 1.48 kpc is 0.24.

**Harmonic split.** dlnN_dR = a0 + a4 cos4φ + a8 cos8φ, taken from φ = 0, π/8, π/4. The dihedral symmetry holds to 7e-32.

| K | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| a0 | 2.11 | 2.04 | 2.42 | 2.41 | 1.98 |
| a4 | +0.25 | −0.01 | −0.72 | +0.00 | +0.94 |
| a8 | −0.01 | −0.16 | −0.70 | −1.26 | −1.24 |
| numerator a0 | 1.66 | 1.60 | 1.95 | 1.90 | 1.51 |

(e-28 /m.) At φ = π/4 the value is a0 − a4 + a8. For K6 that is 1.98 − 0.94 − 1.24 = −0.20.

**Not a sign artifact.** The same formula and signs apply at every K and azimuth. The isotropic part stays positive with margin at all K.

**A resolution and representation effect.**
- The refusal comes from the azimuthal harmonics:
  - a4, the cube m=4 term, changes sign with K and grows at even K (0.25 → 0.72 → 0.94);
  - a8 grows and then levels at about −1.25 from K5.
- The readout azimuths 2πi/8 coincide with the 8 route-A gas-column azimuths (prep v009 L152, binding L104–105). The nearest gas-column radii are 1.359, 1.526 and 1.633 kpc.
- Route B's le3 midplane field at K4 is built from the body gas on 16 azimuths. At 1.36–1.63 kpc it has |a4| ≤ 0.05 and m0 = 2.24–2.27.

**Attribution (PLAUSIBLE).** I attribute a4/a8 to the discrete 8-azimuth column source under cube truncation. This rests on the contrast with route B; the mechanism itself is not isolated (UNTESTED).

**The thin stellar disc is not the driver here**, since the isotropic part stays bounded.

## 4. Route B and tail-corrected runs

**Route B does not use the readout** (TESTED, code). Its route-B stages read the converged checkpoint.

**Route B has its own m0 equivalent of the refusal** (TESTED, code):
- `owned_free_surface_rotation_v001` (`e1b354ec`) computes Ω² = (C_R − hk/γ)/R at L20 and requires every value to be positive at L31, over 72 radii × 32 heights.
- The rotation stage records the result in finish.json (L273–277).
- `column_mean_v004` refuses at L194 (`positive_rotation_square` must be True) and at L204 (Ω ≤ 0).
- It uses the azimuth-averaged dΦ/dR, so the a4/a8 harmonics that cause the route-A refusal do not enter it.

**Route-B margin, K2–K4** (TESTED). On le3, the support ratio s = −P_R/(ρΦ_R) is:
- max 0.672, 0.653 and 0.652 at R = 12.59 kpc, falling with K;
- 0.07 near 1.5 kpc and 0.08 near 5.4 kpc.

C5 and C6 route B are UNTESTED here.

**k→∞ trend (UNTESTED).** The raw C4→C5→C6 numerator steps are −1.18 and −1.22 (ratio 1.03). The sequence does not contract, so no limit can be extrapolated from these three points. The drop is a4 changing sign plus a8 levelling off; it is not an m0 trend.

**Tail-corrected runs (PLAUSIBLE, UNTESTED).**
- The V007 tail is continuum_v001, cylinder K_big 32 minus cube K, lapse-only. Route A gets it at jet order 1, so the readout runs in every T-run.
- A continuum-source tail cannot remove harmonics that the discrete-column field carries inside cube K.
- The expected numerator at 1.48 kpc, φ = π/4, is a0 − a4 + a8 + pgrad(π/4):

| Run | Expected numerator (e-28) | Expected outcome |
|---|---|---|
| C4T | ≈ a0 + 0.02 − 0.46 | passes |
| C5T | ≈ a0 − 1.26 − 0.34 | passes if a0 > 1.60 |
| C6T | ≈ a0 − 2.18 − 0.22 | refuses unless the tail lifts a0 above 2.40 (+21%) |
| C4T-D6 | reproduces the G6 discrete roster | expected to reproduce C6 and refuse |

**Deciding test.** Replay this readout on the T-run checkpoints, or on the saved C4R3/C6 states plus the module tail, before V007 is sealed.

## 5. Recommendation for V007 T2

1. **Re-specify T2 and T2I on G5.** As drafted, T2 is "C4T-D6 vs C6 direct", and it has no reference: C6 is registered invalid with no route-B rows. T2I is also unsatisfiable, because C6's offset and feedback sources never ran.
   - **T2 = C4T-D5 vs C5 direct** (sealed V006 R1). C4T-D5 is K4 cube plus the nodes_v001 tail on G5\G4. Its numerics must be byte-equal to C5's except `composite_grid_spec` and `uv_tail`. Keep the threshold at ≤ τ/4 and decidable.
   - **T2I = the replicas against the C5 rosters on G5\G4.**
   - C5 route A passed this readout: the minimum roster numerator is 0.57e-28 at 1.97 kpc. C5's route-B validity is decided by V006 R1, not here.
2. **Declare a readout rule before sealing, as RO1.** The refusal is expected in C6T (T1_H) and in any D6-type run. The rule:
   - A `NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH` or `DEGENERATE_RADIAL_EULER` refusal raised by the prediction-v005 readout after `CONVERGED_FINITE_FIXED_POINT` is recorded as `ROUTE_A_READOUT_NO_CIRCULAR_BRANCH`, with query, φ, R, numerator and denominator.
   - Route B then proceeds on the converged checkpoint.
   - The route-B Ω² > 0 refusal stays the decision-relevant branch test.
   - `route_a_rows` never enter T1–T3.

   **Implementation need.** RO1 requires a reviewed worker/driver successor that persists the converged result together with the readout-failure record, catching only these two refusals and only after convergence. Today no result.json exists in this case, and `admit.route_a` needs a `result_sha256`.
3. **Leave V006 R1 unchanged; C6 stays a registered failure.** Rerunning the same spec under gate V1(v) would reproduce the refusal: the saved-checkpoint replay raised at the identical call bitwise. Report it as a deterministic defect, not a rerun candidate.
4. **MT_monitor needs no change.** It uses v_ref = A2F10 route_a_rows (K2), and the K2 margin at 1.48 kpc is 1.42e-28.

## Files

**Tools** (`tools/`):
- `extract_saved_readout_c2.py`
- `replay_readout_c2.py` (exact and sweep), with `_v002` (adds `--radii-kpc`) and `_v003` (adds `--phis s16:`)
- `route_b_margin_c2.py`
- `analyze_c2.py`
- `make_diag_c2.py`
- `show_partial_c2.py`

**Outputs** (`out/`):
- `EXACT_C6_IT8_V001.json`
- `SWEEP_C6_IT8_Q*_V001.json`
- `RADIAL_C6_IT8_V001.json`
- `AZ16_C6_IT8_V001.json`
- `AZ16R_K{2..5}_IT*_V001.json`
- `SAVED_READOUT_K2_K5_V001.json`
- `ROUTE_B_MARGIN_C2R3_C4R3_V001.json`
- `FIDELITY_C5_Q0_PHI0_V001.json`
- `ANALYSIS_V001.json`
