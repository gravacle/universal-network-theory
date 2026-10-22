# CHECK_V001: independent check of the P-88 k_max / truncation kit (dispatch 0470)

**Verdict: PASS_WITH_CORRECTIONS.**

The kit can launch as designed once P1 is met. Three corrections to the comparison criteria (D1–D3) must be sealed as `KMAX_MATRIX_PREREG_V002` before the first case `result.json` exists. That deadline is about 1.7 h after the wave-1 launch, when C2 completes. The compare-script pin has to move to the new sha at the same time.

None of the corrections changes a spec, a cap, a grid or a launch command, so wave 1 does not wait for them. The remaining items are textual or advisory.

**Who checked, and how.** The checker works in the Claude2 lane and did not write the kit. All scripts and outputs are in `../kmax_convergence_check/`; their hashes, computed from bytes, are in `HASHES_CHECK_V001.txt` there.

The check used numpy only, single thread (thread env vars set to 1), and launched nothing. No NGC3198 file was opened. From the DDO154 observation region, only `rows[*].id` and `rows[*].quoted_random_sigma_km_s` were extracted.

The coordinator's `REPRO_PINNED_*` runs were started at 08:24:44 under `CLAUDE2/runs/`. They are not from this kit or this check.

## What reproduces

| Claim | Result | Evidence |
|---|---|---|
| All 25 hashes in `HASHES.txt`, the prereg pin in the compare script, and the A2 / seed / binding / σ-source shas | All verify from bytes | `K01_REDERIVE_V001.json` |
| Tests, 28/28 | Reproduced. The rerun `TEST_RESULTS.json` is byte-identical (`42efa198…`) | `rerun_tests_V001/` |
| `GRID_CHECK_V001.json` | The rerun is byte-identical (`3bfda534…`) | `GRID_CHECK_RERUN_V001.json` |
| Generated wave-1 specs and the 10 templates | Regenerate byte-identically | `rerun_tests_V001/gen_*` |
| P1: v007:130 refuses more than 80 nodes; v008 differs only at that line; the driver `AUX['prep']` and the route-A worker `LOCAL['prep']` (`ddo_composite_stable_cached_root_worker_v002.py:18`) pin v007; review `aa12d69f…` is PASS_SCOPED | Confirmed | K01 |
| Axes 72/84/96/92; kept-node counts 344048/362592, 525992/567504 and 755080/834048; G2⊂G3⊂G4 bitwise; GR outer = G2 outer | Confirmed by independent code. The kit's `expected_axis` equals a prep-v008 float64 transcription bitwise on all 4 grids | K01 |
| σ list, σ_min = 0.2 (rows 06–08), τ = 0.05, Bonferroni z = 2.8653, band shift 8.7%, τ/floor = 5.26, relative equivalents 4.3e-3 and 1.0e-3 | Confirmed | K01 |
| Inner-refinement evidence: max 4.48e-5 relative radial dlnN (96 points), about 0.0011 km/s | Confirmed | K01 |
| Fit p = 1.0428, B0 = −46.7 MB. Hours C2 1.74, S2 0.99, C3 2.82, S3 1.61, C4 4.28, S4 2.45, R 3.75. Route-A peak at 96³ is 2.77 GB (L) and 1.90 GB (A). Critical path 4.29 h; total 22.7 core-h. 120³: 5.46 GB, 8.6 h | Confirmed. A third memory model (96³ prepare peak plus the route-A overhead at 72³) gives 2.34 GB, which is also above 2 GiB, so the 4 GiB cap conclusion is model-robust | K01 |
| V3 does not false-fail when given real driver normalization | All 10 cases pass V3 when `normalized_spec` comes from the driver's own `normalize_spec()` on the generated specs | K02 A10 |
| Masks | The kit's `driver_mask` equals the driver's `truncation_mask` bitwise on the real G2, G3 and G4 grids, for all 6 sphere and cylinder cases | K02 A11 |
| Ring diagnostic | Matches an independent loop to 4e-16. On the saved V002 route-A packet it reproduces the reviewed `v002_ring_force.json` g0 to 4.4e-16 and m4 to 2.3e-14 | K02 A12–A13 |
| V4/V5 on the saved real 72³ field packet | Pass. All 373248 rows are nonzero. The same packet tested as sphere-2 fails V5, as it should | K02 A14 |
| Admission is bitwise-safe | Confirmed: the driver passes `mask=None` to reference and body (driver lines 918–944) as well as to route A | Driver source |

**Rules compliance.**
- No physics was chosen beyond A1, A2 and the A1-numerics test. The physical block equals the seed V002 values; T2 shows `per_call_seed` changes only grid fields. The shapes are the driver's declared numerical options. The adoption tie-break uses a numerical artifact.
- No target access and no scipy.
- Nothing was launched: `test_runs/` holds only mocks, and no `P-88` call spec exists outside the kit.
- The criteria are pinned by sha, and no result exists yet.
- The "fixed source" reading is disclosed (prereg `fixed_across_all_cases.what_fixed_source_means`; MD L41): the gas is re-solved and K0, body and roots come from route A at each grid edge. ROOT_DECISIONS A1.5 says "at a fixed source under the reviewed route-B driver". The driver always re-solves the gas, so this reading is consistent and it is what calibration uses.

## Defects

### Must be sealed as PREREG V002 before the first result

**D1. The pass test does not bound the distance to the limit.**
- Where: prereg L74 `shape_pass`; MD L101; `kmax_compare_c2v001.py:235`.
- Problem: "contracting" (D34 < D23) accepts any ratio q < 1.
- Fixture K02 A1: D23 = 0.051 and D34 = 0.0485, so q = 0.95. The kit returns ADOPT with u_01 = 0.05 km/s, while the geometric tail D34·q/(1−q) = 0.94 km/s, about 19τ.
- Prior evidence makes slow contraction plausible. Review row 30 shows row 01 at −40.5%, −28.4% and −18.8% with no plateau.
- Fix: require D34 ≤ τ **and** D34 ≤ ½·D23. Then the geometric tail is at most D34 ≤ τ, and no tail is adopted.
- Also report D34·q/(1−q) per row as a diagnostic. Reporting a tail is not adopting one, so it stays inside the LIVE:41 limit.

**D2. The carried uncertainty omits the measured spread between shapes.**
- Where: prereg L82 rule 6; MD L110; `kmax_compare_c2v001.py:284`.
- Problem: rule 4 lets passing shapes differ at K = 4 by up to 2τ = 0.10 km/s, but u_i does not include that spread.
- Fix: add max over passing shapes A of |v_i(A,4) − v_i(A*,4)| to u_i.

**D3. The second clause of V5 is vacuous.**
- Where: prereg L71; `kmax_compare_c2v001.py:127`.
- Problem: `m.sum() == expect_kept` compares the mask applied to the packet's axis with the mask applied to the registered axis. Once V4 holds, the two are identical. The computed `nonzero_rows_in_packet` is never gated.
- Fixture K02 A2: an over-masked S4 packet (280 nonzero rows of 2200 expected) passes and is ADOPTED.
- Fixture K02 A3: a sphere-masked cube packet passes.
- Fix: gate `nonzero_rows_in_packet == mask_kept_expected`. This is safe on real data: the saved 72³ packet has 373248/373248 nonzero rows (A14).

### Should be corrected (rationale and remedies; same V002)

**D4. The why_tau claim about the A1-m≥1 indicator is false and mislabels the indicator.**
- Where: prereg L87; MD L85.
- Claim: "τ is below the carried A1-m≥1 indicator range 0.015–0.272".
- The comparison is false. τ = 0.05 lies inside the range: the values at rows 01–03 are 0.015, 0.032 and 0.0498.
- The label is wrong. The quantity is the A4 m2 forcing amplitude 0.5ε₂v. Review row 34 calls it "an amplitude… an indicator, not a UNT result".
- ROOT_DECISIONS A1.4 carries the m≥1 *response* as UNTESTED and non-perturbative (19.26% folded mass), so it is not a sensitivity budget.
- Fix: withdraw the bullet.

**D5. The χ² claim holds only for the bias-squared term.**
- Where: prereg L86; MD L84.
- Claim: "adds at most 0.75 to χ²". That bound holds only for Σ(b/σ_i)².
- The cross term 2Σr_i·b/σ_i² is not bounded; it is +6.0 at r_i = +σ_min.
- Fix: state the bound as a bound on Σ(b/σ_i)².

**D6. The INCOMPLETE remedy does not work for deterministic failures.**
- Where: prereg L77; MD L105; `kmax_compare_c2v001.py:256`.
- Problem: the remedy "rerun only the named case, same spec" cannot fix a deterministic failure (K02 A8). Examples:
  - V2: Picard change not ≤ 0.0125 within 4 passes;
  - a bracket miss, which ends FAILED_AT_STAGE;
  - route A not converging at iteration 4 (BLOCKED, INTERFACE §11.1);
  - a mask defect.
- Fix: pre-name a next step per gate.
- For V2 specifically, set `picard.passes` to 6 now (`make_kmax_specs_c2v001.py:36`) with the 0.01 bound unchanged. This costs nothing for cases that stop at pass 3 and removes the path to a deterministic V2 failure.

**D7. A precondition is missing from the §1 blocker table.**
- Where: MD L7–13.
- Missing item P6: the bracket rule is UNTESTED under the A2 coefficients and the new grids.
- The FS absolute bracket [1.5125e8, 3.025e8] and its 11 overrides were derived on the V004 chain. INTERFACE §6 warns the rule may not bracket elsewhere, and A2 changes the route-A state.
- Consequence: a miss fails the call after its prefix, at about 0.75–1.84 h.
- Recovery is cheap: admit the failed call's own route-A checkpoint, reference and body (admission checks parameters, not brackets). Then regenerate every case with the same corrected overrides, using `--base-spec`.
- Deciding test: the FS pass of the first A2 call.

**D8. V3 can blame the wrong cases.**
- Where: `kmax_compare_c2v001.py:185,199–202`.
- Problem: the common-block reference is the first registered case present, C4. If C4 itself is the odd case, C4 passes and all nine good cases are named as failed (K02 A4). The outcome, INCOMPLETE, is still correct.
- Fix: use the modal block and name the minority.

### Textual or advisory

**D9. The admission citation is incomplete (MD L39).**
- The claim is correct.
- But the cited reason ("route A is not masked") covers only part of the prefix. Also cite driver lines 918–944: reference and body are unmasked too.

**D10. MD L48–49 uses N for total wave nodes.**
- The §2 table header defines N as nodes per axis.
- Read as nodes per axis, the formulas give 1.35× time and 1.52 GB instead of 2.46× and 2.77 GB. The code itself is correct.

**D11. One grid check is a constant, not a computation.**
- Where: `kmax_grid_check_c2v001.py:137`.
- `all_inner_nodes_kept_by_every_mask_K>=2` is the constant expression √3 < 2.
- The claim is true: the maximum inner |k_i| is 0.976/kpc, so the corner is at 1.69/kpc. Compute it from the nodes instead.

**D12. Two prior-evidence citations need qualifiers (MD L120–121).**
- "Fixed G4 source" collides with the grid name G4; the source here is route A's iteration-4 source at 2/kpc.
- The cited audit's scope is omitted: "Not an error bound, gas re-equilibration, pressure-supported speed".
- The review's 1.5/kpc point is labelled "iso".
- All three numbers are gravity-only m0 force changes relative to the full cube.

**D13. The m4 tie-break rule is ambiguous with three shapes.**
- Where: prereg L81; `kmax_compare_c2v001.py:280–281`.
- Problem: rule 5 is ambiguous when three shapes are within 10% (K02 A6). The code adopts sphere; the reading "any shape within 10% of the minimum, then the smallest D34" adopts cylinder.
- The statistic is also off-target. The driver's `global_max` m4 on the saved chain sits at R = 12.8 kpc, outside the 0.49–5.92 kpc rows: 0.0200 overall against 0.0089 inside the row range (`K03_M4_STATISTIC_V001.json`).
- Fix: use m4 at the row radii.

**D14. Sequences already converged at the noise floor fail as non-contracting.**
- With D23 = 0.002 and D34 = 0.003, the kit returns NOT_CONVERGED (K02 A7).
- This is unlikely given the prior evidence. Optionally add a floor clause to D1.

**D15. Single-thread operation is not enforced.**
- No kit script and no §6 command sets the thread env vars, and `-I` does not clear them.
- Fix: export `OMP/OPENBLAS/MKL/VECLIB/NUMEXPR_NUM_THREADS=1` in the §6 commands.

## Scope (UNTESTED, each with a deciding test)

- **S1. Transfer across the parameter space.** The adoption is measured only at the seed V002 point. ℓ_F sets the periodic native-symbol span in k_prim: 2.08 periods at 2/kpc (review row 7), about 4.2 at 4/kpc. Deciding test: rerun the adopted shape at K = 3 and K = 4 at the calibrated point before prediction.
- **S2. NGC3198.** P-88 covers DDO154 only, and the NGC route is unsupported by the driver. Deciding test: the same matrix on the NGC route once it exists.
- **S3. Outer-panel order.** The order of the [2,4] panels is uncontrolled; R controls only |k| ≤ 1. Deciding test: the adopted shape with order-8 outer panels, which needs 104 nodes.
- **S4. Route-A source azimuths.** The count is 8, with m8 bias −10.6% to +5.5% (review row 18). It is held fixed and is outside P-88's binding scope.

## Speed (consistent with the above)

1. Seal V002 (D1–D6 and D13) in parallel with the P1 driver review. It must be in place before the first result exists, and needs no new run.
2. P1 is the critical path: the driver successor plus its review. Stage the prep successor with a node budget of at least 120 for review now. It is a one-line diff like v008, and it is required by both pre-named contingencies (NOT_CONVERGED needs 108/120; INNER_UNRESOLVED needs 116) and by S3. NOT_CONVERGED is a live outcome on the kit's own prior evidence.
3. If the production A2 base call equals C2's spec, run it once.
4. Optional, decided before any result: a per-row τ_i = 0.25σ_i satisfies the kit's own band and Σ(b/σ)² rationale on every row. It is 2–8× looser at rows 01–05 and 10–12, which lowers the chance of the costly 5–6/kpc extension without weakening the bound on calibration impact.
