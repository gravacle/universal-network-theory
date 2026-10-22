# INTERFACE_A2_SEED_SCAN_C2V001: A2 anchor (seed) scan, Claude2 lane

Nothing here ran a project calculation. I executed only the synthetic tests, four dry-runs, and one read-only analysis of saved scan outputs. Claude2 launches the real runs.

`R` = `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13`. `D` = this folder. `PY` = `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`.

## 1. Files

| File | Role |
|---|---|
| `a2_seed_scan_c2v001.py` | Scan. Inert at import. CLI `run`, `dry-run`, `analyze-saved`, `replay-v004-reads`. |
| `specs/SCAN_A2_G2_C2V001.json` | The A2 scan: A2 grid, G2 cube, factors 1,3,10,30,100,300,1000, sweep at the failure azimuth. |
| `specs/SCAN_V004_IR64_REPRO_C2V001.json` | Reproduction. Runs the pinned v004 worker with the saved launch arguments, factors 10 and 100. |
| `specs/SCAN_V004_G2_CONTROL_C2V001.json` | Optional control. V004 grid, G2, factors 1, 10 and 100. At factor 1 it must equal route-A RUN_V002 iteration 0 bitwise. |
| `specs/SCAN_SYNTHETIC_SELFTEST_C2V001.json` | Monitor self-test. No project computation. |
| `dryrun/DRYRUN_*_V001/DRYRUN_REPORT.json` | Dry-runs for all four specs: all `ok: true`, 0 problems. |
| `validation/ANALYZE_SAVED_CURRENT_SOURCE_SCAN_V001.json` (+ `_specs/`) | Read-only analysis of the saved v004 scan, status `REPRODUCED`. |
| `tests/tests_c2v001.py`, `test_runs/RUN_V002/TEST_RESULTS.json` | Synthetic tests: 13/13 pass. |
| `superseded/TEST_RUN_V001_FAILED_EXPECTATION` | First test run. One test had a wrong expected sample height (16.8 instead of 17.0 kpc); the code was unchanged. |
| `HASHES.txt` | SHA256 of every deliverable, computed from bytes. |

## 2. Trace: how seed V002 was produced

**No code computes `scale_seed` or the enthalpy margin.** I searched every `.py` under `R` for 43300 and 0.158413 and found nothing. Those numbers appear only in seed JSONs and in ledger prose. I therefore reconstructed the rule from the seed text and checked it against the saved outputs.

- **The scan itself.** `ddo_fixed_source_gamma_scan_v004.py` (fc8abd7b) ran with the IR64 source package (`DDO154_OUTER_COLUMN_COMPOSITE_IR64_RUN_V001/refinement/order_064`), V004 coefficients, base γ = 1.856569929503051e41 and fixed Eref = 9.243506372672262e58. The factors were 10 and 100.
  - Each factor rebuilds the full kernel at every node.
  - It then reads a 641-row column at the failed outer column: column 395, R = 9.667 kpc, z = ±64 kpc in 0.2 kpc steps. The read uses line v001 and the metric evaluator.
  - It also reads 96 DDO midplane points: 12 radii × 8 azimuths.
- **"Inward" means positive.** The signed `c² R dlnN/dR` is positive for all 96 points at both factors, and the ledger calls those 96/96 inward. The older V002 scan factors 1e4 to 1e7 use the same convention.
- **The scale.** s = `statistics.median`(the 96 values of candidate_000) / 43300². This reproduces `0.15841304156288938` **bitwise**.
- **Where 43300 comes from.** It is the median of the 12 `observed_speed_km_s` in `DDO154_CALIBRATION_OBSERVATION_REGION_V001.json` (13c16a63), which is pinned by the seed: 43.3 × 1000 = 43300.0 exactly. The scan derives the value from that file and refuses if it is not 43300.
- **The candidate seed.** Eref' = s·Eref and γ' = s·(10γ). Both are bitwise equal to the seed V002 values 1.4642919592009638e58 and 2.9410488940677744e41.
- **The enthalpy margin.** The procedure checks each side separately. It takes max over 0 < ±z ≤ search limit (32 kpc) of (logN/N0)/s, then subtracts the threshold log1p(Γσ²/((Γ−1)c²)) = 3.3657664e-9.
  - This normalization is exact for the fields: K = Eref·native + γ·EH, so (sE, sγ) scales the response by 1/s. On the toy nodes the deviation from 1/s is 1e-13.
  - For factor 10, the margin is +5.92e-9 (plus side) and +6.35e-9 (minus side), with first crossings at +5.8 and −5.2 kpc. Before normalization the margin is negative (−1.89e-9).
  - For factor 100, the margin is +9.92e-9.
  - So "10 is first and 100 is the alternative" is reproduced.

## 3. Mode `g2_route_a_kernel`: what the scan builds, and from where

The scan builds its inputs exactly as route A does:

1. **Seed.** The pinned driver `galaxy_m0_forward_c2v001.py` (75b0c08a) applies `normalize_spec` and `per_call_seed` to the A2 call template (`CALL_KMAX_C2_C2V001.json`, 7c7330bf), with the scan's coefficients. This gives the seed numerical_inputs: G2 = DIRECT_LAPSE_PANELS72, 72³ = 373248 nodes, cube, kmax 2/kpc. For the A2 template this is seed V002 itself (reused bitwise).
2. **Prep.** Prep V007 (ac905597) is loaded from its pinned bytes. For a non-default grid, `COEFFICIENT` and `COEFFICIENT_SHA` are set after loading, exactly like the driver's module patch. `prepare_inputs(**seed numerical_inputs)` then runs.
3. **Iteration-0 source.** It is formed exactly as the solver does: `solver._supplied_fixed_source(fixed)` + `initial_gas`.
4. **Kernel, per factor f.** The scan builds `cache.make_fourier_module` (7b9816ae) over quadrature v005 (7167a264), which is route A's Fourier module (unit −K⁻¹eₙ solve, then a scalar scale). It uses γ = f·γ_seed and Eref = Eref_seed, as in the v004 rule.
   - The complex binding is wrapped by a numerically transparent `DiagnosticBinding`. It records Hermitian-part eigenvalues and inertia to a compact NPZ.
   - The wrapped and plain bindings give bitwise-identical responses, and the same cache identity.
5. **Reads.**
   - **v004 reads.** These are the v004 reads verbatim, at the failure column (A2: column 442, R = 10.916 kpc, φ = π/2) and at the 96 DDO points. They are written to a v004-format `points.jsonl`.
   - **Sweep reads.** For each sweep column (default: all 72 radii at the failure φ), the scan reads two values at the exact route-A search heights. These are ±(accumulated 0.2 kpc steps) to ±32 kpc, 321 heights in all, identical to `hi_two_sided_free_boundary_v003` (tested against the real module).
     - The legacy read: line v001, metric evaluator, log N − log N0. This is the declared estimate.
     - The route-A stable read: line v002 `lapse_difference`. This is what the HI solver brackets on.
6. **Reference checks.** These are built into the run and are bitwise at factor 1.
   - The source and wavevectors must equal the A2 route-A iteration-0 arrays. A mismatch refuses the run.
   - The unit-scaled weighted responses must equal `000002_weighted_responses`.
   - The stable read at +32 kpc minus the threshold must equal the route-A failure's `actual_log_residual` = −3.3398405645830363e-9 (`route_a_crosscheck.stable_bitwise_equal`).
   - Side fact: the A2 and V004 route-A iteration-0 source NPZ files have the same sha256 (247c242d…), so the source does not depend on the grid.

## 4. Rule, selection and outputs

For each factor, in list order, `rule_pass` requires all three of:

- 96/96 inward;
- s = median/43300²;
- a positive two-sided normalized margin at the failure column, using the legacy read within 32 kpc.

`selection.first` is the first factor that passes and `selection.next` is the second. With no passing factor the status is `COMPLETED_NO_CANDIDATE` and `registered_result` is set. Nothing is picked and no spec is written.

`result.json` contains, per factor:

- the rule, s and the candidate seed (s·E, s·fγ, ℓ_F);
- the failure-column margins: normalized within the limit, over the full ±64 kpc roster, and unnormalized;
- the margin against radius from the sweep: `sweep[]` rows with legacy and stable normalized two-sided margins, first crossings and unavailable reads;
- `sweep_summary`, listing the columns whose margin is negative or missing;
- the inertia counts, and the number of nodes whose inertia changed since the previous factor (a pole-crossing indicator);
- the reference checks.

**Route-B specs.** These are written to `OUT/route_b_specs/CALL_A2_SEEDSCAN_{FIRST,NEXT}_C2V001.json`. Each is the A2 template with only `label` and `physical` changed: Eref_J = Eref_eval, gamma = f·γ_seed, common_scale_s = s, ℓ_F unchanged. The pinned driver's `normalize_spec` and `per_call_seed` then check that the driver seed equals the candidate bitwise. Each spec also carries the factor's sweep flags.

Before launching route B, check `sweep_all_positive_stable`. The declared rule tests only the failure column, so another radius may still fail to bracket.

Files written per candidate:

- `input.json`, `report.json`, `points.jsonl` and `complex_field_jet.npz`;
- `sweep_reads.npz`;
- `kernel_diagnostics.npz`;
- `weighted_responses.npz` (60 MB);
- the cache facade's own `node_diagnostics/`. These are 537 MB per factor; the reviewed module writes them unconditionally.

At the top level the run writes `call_spec.json`, `start.json`, `progress.jsonl`, `scan_context.json`, `wavevectors.npz`, `result.json` and `finish.json`. `finish.json` holds the status and `result_sha256`. A candidate exception stops the scan, keeps the completed prefix, gives status `FAILED_AT_CANDIDATE`, and writes no specs.

## 5. Proposed factor list and cost

**The list.** The factors are 1, 3, 10, 30, 100, 300 and 1000, relative to the seed V002 γ/Eref of 2.0085e-17 (A2 call s = 1). The list ascends, as in the original procedure, which picked the first passing factor going up from the current ratio.

**Why factor 1 is included.** Renormalizing s on the A2 kernel alone may already bracket the outer columns. The A2 route-A failure is at iteration 0, before any re-equilibration. The failing value was logN/N0 = 2.59e-11 at +32 kpc on column 442, against a threshold of 3.37e-9. The minus side of that column did bracket.

**Cost per factor (estimate, single thread).** About 260 s per factor:

- about 150 s for the unit solve, from the A2 route-A receipt: 175 s covered prep, the unit solve and the scaled logs;
- 10–20 s for the eigen diagnostics;
- 20–40 s for the 96-point read;
- 30–70 s for the 72-column sweep.

The output is about 0.7 GB per factor and peak RSS about 1.0–1.4 GB.

**Whole scan.** Prep is about 60 s once, so 7 factors take about 31 min and 4.9 GB. Suggested caps: wall 3760 s, RSS 3 GiB, output 7.2 GiB (see the dry-run plan).

## 6. Launch commands for Claude2 (recommended order)

Monitor: the reused, unchanged `root_monitor_c2v001.py` (ba031c23). It runs `<script> run --spec S --outdir O`, and a synthetic end-to-end run under it passed.

```
R="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13"
D=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/a2_anchor_scan_c2
PY="/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B"   # use as: $PY ... (quote paths: R has spaces)
M=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py
S=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/a2_anchor_scan_c2/a2_seed_scan_c2v001.py
H=328c731efc3ae8834f4915fb9ca9a8efd97eef4febdcb00fe8ab1ca084925108
O="$R"/CLAUDE2/runs
# 1. replay of the copied v004 reads on saved prepared waves (no kernel; ~1 min each; must print REPLAY_BITWISE_EQUAL)
$PY $S replay-v004-reads --candidate-dir "$R"/CODEX1/DDO154_CURRENT_SOURCE_GAMMA_RUN_V001/scan/candidate_000 \
   --outdir "$O"/A2_SEED_SCAN_REPLAY_C000_V001 --launch "$R"/CODEX1/DDO154_CURRENT_SOURCE_GAMMA_RUN_V001/launch.json \
   --launch-sha256 28e130729b3343f389f85b22aa2c5af18825e3c2f30831a4bd39c6791516285a
#    (same with candidate_001 -> A2_SEED_SCAN_REPLAY_C001_V001)
# 2. v004 reproduction (~5 min, 1.8 GB): expect status REPRODUCED (files bitwise, s, seed V002, route-B spec reuses seed V002)
$PY $M --driver $S --driver-sha256 $H --spec $D/specs/SCAN_V004_IR64_REPRO_C2V001.json --outdir "$O"/A2_SEED_SCAN_V004_REPRO_RUN_V001 \
   --receipt "$O"/A2_SEED_SCAN_V004_REPRO_RUN_V001.receipt.json --wall-cap-s 1800 --rss-cap-bytes 2147483648 --output-cap-bytes 4294967296 --poll-s 2
# 3. the A2 scan (~31 min, ~4.9 GB)
$PY $M --driver $S --driver-sha256 $H --spec $D/specs/SCAN_A2_G2_C2V001.json --outdir "$O"/A2_SEED_SCAN_G2_RUN_V001 \
   --receipt "$O"/A2_SEED_SCAN_G2_RUN_V001.receipt.json --wall-cap-s 3760 --rss-cap-bytes 3221225472 --output-cap-bytes 7707033600 --poll-s 2
# 4. optional V004/G2 control (~14 min, ~2.1 GB)
$PY $M --driver $S --driver-sha256 $H --spec $D/specs/SCAN_V004_G2_CONTROL_C2V001.json --outdir "$O"/A2_SEED_SCAN_V004_G2_CONTROL_RUN_V001 \
   --receipt "$O"/A2_SEED_SCAN_V004_G2_CONTROL_RUN_V001.receipt.json --wall-cap-s 1800 --rss-cap-bytes 3221225472 --output-cap-bytes 4294967296 --poll-s 2
```

**Acceptance for step 3:** `custody.reference_*_bitwise_equal` true; factor-1 `reference_check` true; and `route_a_crosscheck.stable_bitwise_equal` true. If any of these fails, the kernel differs from route A and no selection should be used.

**Route-B launch:** the monitor of `galaxy_m0_forward_c2v001.py` on `OUT/route_b_specs/CALL_A2_SEEDSCAN_FIRST_C2V001.json`. The caps are as for KMAX_C2: wall 14400 s, RSS 3 GiB, output 8 GiB.

## 7. Scope and limits

- **Fixed source.** The source is the iteration-0 analytic source. The gas re-equilibration changes it, so passing the rule is a seed criterion, not an equilibrium.
- **Estimated margin.** The margin is a linear estimate; logN at ~1e-8 is linear to about 1e-16 relative. It is sampled at 0.2 kpc, which proves no first-root resolution.
- **Sweep coverage.** The sweep covers one azimuth (π/2). All 576 columns can be listed in `sweep.columns`, at about 8× the sweep cost.
- **Route-B blocker (driver c2v001 §11.1).** Route A must converge at exactly iteration 4. A candidate that brackets but converges at another iteration ends BLOCKED.
- **Next step if no candidate passes.** `COMPLETED_NO_CANDIDATE` is a registered result. The next step is a new declared scan: either above 1000, or below 1 (the ratio is not monotone in its effect; see the V001 fixed-source scan, where factors 1 and 1000 were mixed-sign). This is never an automatic extension.
- **Physics.** No physics is new: every equation, tolerance and guard comes from the pinned reviewed modules. The changes are versioned orchestration, compact diagnostics, the sweep, the declared rule and the spec writer.
