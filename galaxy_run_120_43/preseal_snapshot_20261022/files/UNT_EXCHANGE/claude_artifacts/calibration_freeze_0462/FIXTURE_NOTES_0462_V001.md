# FIXTURE_NOTES_0462_V001 — independent fixtures for dispatch 0462 (Claude3 lane)

Author: independent fixture helper (Claude3 lane). The fixture script was written from `INTERFACE_0462_V001.md` alone, before either module was opened; the modules were read afterwards only to diagnose failures (two grep lines: scipy mention, import lines). Neither module was edited.

## Files and hashes (SHA256 over bytes)

| File | SHA256 |
|---|---|
| `fixtures_0462_c3v001.py` (this fixture script, final) | `670891a66f820d81e7df0bbc5b3fbaba585071f14b3bf9c6ad86f8231b83b24c` |
| `FIXTURE_RESULTS_0462_V001.json` (final run, machine-readable) | `dd24ea33aa6c0e5fdf5b22a1f58d39884c019f529d861ec423853fa795680edb` |
| `calibration_region_engine_c3v001.py` (tested, unchanged) | `f5613832fcb6e452b4490d56453cce37fb8846e802442407e794f80a6ec84e0b` |
| `prediction_freeze_c3v001.py` (tested, unchanged) | `ed6b5a3e1d02f6f5c506c9af839e25faae120b14ba4a8466beca7fba30c09200` |
| `DDO154_CALIBRATION_OBSERVATION_REGION_V001.json` (input, calibration data) | `13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d` |
| `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` (input, target-free) | `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494` |

Runtime: `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B` (3.12.14), numpy 2.3.5, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`. Invocation: `fixtures_0462_c3v001.py <artifact_dir> <scratch_dir> [--results-out <path>]`; modules imported by file path with `importlib.util.spec_from_file_location`; all manifests written under the scratch directory (`.../scratchpad/fixtures/final/`); nothing written into the artifact directory except the results JSON via `--results-out`. No NGC3198 velocity was read; no forward model or project run was launched. Synthetic forward models only.

## Analytic toy (Module 1 fixtures)

Coordinates (5): `amp_scale` log [10,100] free, `tilt` linear [-1,1] free, `distance_Mpc` log [3,5.5] nuisance, `dead_knob` linear [0,1] free, `held_constant` linear [0,2] fixed at 1.0. Four varying coordinates; trial values map to u = (0.5,0.5,0.5,0.5).

Forward: `speed_r = obs_r + sigma_r·(10·p0_r·d0 + 12·p1_r·d1 + 14·p2_r·d2 + 0·d3)`, d = u − 0.5, with p0 = all ones, p1 = six +1 then six −1, p2 = alternating ±1 over the 12 DDO154 rows (ids, observed speeds, sigmas and closed rectangles taken from the real region file; the rectangles are `obs ± z·sigma`, z = 2.865260238532134). The toy recomputes u from `theta_natural` with the interface transforms, so the fixed coordinate and all names are checked on every call.

Derived expectations:
- Sigma-scaled Jacobian columns are exactly orthogonal, so the identified directions are the axes e0, e1, e2 with singular values 14√12 = 48.4974, 12√12 = 41.5692, 10√12 = 34.6410; column 3 is exactly zero (s = 0, condition number "inf"); near-null direction = e3.
- The admitted set in u is the cross-polytope `10|d0| + 12|d1| + 14|d2| ≤ z` (any d3), with axis boundaries z/10 = 0.286526, z/12 = 0.238772, z/14 = 0.204661 from the anchor, all inside the box and all crossed by the doubling march (0.04, 0.08, 0.16, 0.32) at t = 0.32, so no box edge binds. The boundary comparison in the script is general (interval of admitted t along `anchor + t·v` for the vector v actually reported, closed rectangles plus box).
- Bisection resolution per side = (bracket width = march_step·2^m with step·2^m ≤ t* < step·2^(m+1)) / 2^bisection_steps = 0.16/256 = 6.25e-4; tolerance 2× = 1.25e-3.
- E2 seed u = (0.6,0.6,0.6,0.5): rows with (p1,p2) = (+,+) read 3.6z/z·... i.e. S·d = 3.6 > z, so not admitted; the Gauss-Newton step of the affine model returns exactly to the centre (norm 0.173 < max_repair_step 0.3).
- E3 empty region: rows 01 and 03 share the pattern row (10,12,14,0); offsets +3z·sigma_01 and −5z·sigma_03 force the common linear form q into [−4z,−2z] ∩ [4z,6z] = ∅ with a nonzero Gauss-Newton target q = +z (E3a). The symmetric variant ±3z gives Sᵀr = 0, a zero step (E3b, soft checks only).
- E4 failure triggers (raise if u0 > 0.72; NaN in row 06 if u1 < 0.25; row 08 dropped if u2 > 0.75) are placed where the march/bisection reaches them but the seed Jacobian does not.

Module 2 synthetic forward: `v_q = 150 + 10a + 3b(k+1)/43 + 0.5 sin(k+1)` over the 43 real query ids; one point raises, one returns NaN for Q17. Envelopes, medians, within-error and band-overlap counts are recomputed independently in the script. Target rows for the scorer are synthetic: rows 0..19 observed = prediction ± 0.5 (sigma 2.0, within), rows 20..42 ± 3.0 (outside), row 30 observed = 0 (fractional_error None), Q17 in manifest C observed = its central value with sigma 1e6 (must still not count).

## Results (final run; all 15 cases PASS, 301 checks, 0 failed)

| Case | Checks | Key numbers |
|---|---|---|
| X0 import inertness, static checks, API surface | 28 | artifact listing unchanged by import; no stdout; no `__main__`, scipy, subprocess/threading, socket; 15 functions keyword-only, no defaults |
| E0 spec helpers, classify, load_observation_region | 34 | round-trip u error < 1e-12; fixed coord inserted; closed-interval edge admitted; NaN/missing/garbage → valid False; 12 rectangles/sigmas/observed bound exactly; bad coords refused |
| E1 analytic toy | 40 | evaluations 121 (= toy calls); identified [0,1,2], near_null [3]; singular values 48.49742, 41.56922, 34.64102, 0.0 (expected 48.49742, 41.56922, 34.64102); null |dot e3| = 1.0; Jacobian max abs error 1.3e-13, null column exactly 0; admitted 54 / rejected 59, all re-classified identically by the toy; hull_box vs analytic: dir0 (e2) ±0.204375 vs ±0.204661, dir1 (e1) ±0.238750 vs ±0.238772, dir2 (e0) ±0.286250 vs ±0.286526 (tolerance 1.25e-3); unidentified direction index 3, vector (0,0,0,1), sensitivity 0.0, trial_projection 0.5 = u_trial·v |
| E2 seed not admitted | 13 | seed rejected (jacobian.seed_admitted False, anchor.admitted False); 1 repair evaluation lands at u ≈ (0.5,0.5,0.5,0.5) (log_index 9); status COMPLETE, empty_region False; 54 admitted / 60 rejected, all toy-consistent; null coordinate unchanged |
| E3 empty region | 22 | E3a: NO_ADMITTED_POINT, empty_region True, 10 evaluations (9 Jacobian + 1 repair), log length 10 = toy calls, no admitted point under the toy; E3b (zero step): NO_ADMITTED_POINT, 9 evaluations, 0 repair entries (not judged). ok=True in both (not judged) |
| E4 failures | 13 | 3 raises, 1 NaN row, 1 missing id; 5 invalid log entries, each with reasons/exception text, none admitted; exception entries carry `FixtureForwardError` text, prediction None; run COMPLETE, 121 evaluations = toy calls; 58 admitted all toy-admitted |
| E5 budget | 18 | budget 30: BUDGET_EXHAUSTED, stage_reached "bisection", evaluations_used 30, log 30, 12 admitted / 10 rejected preserved and consistent with the log, Jacobian ok; budget 5: BUDGET_EXHAUSTED, stage_reached "jacobian", 5 = 5 |
| E6 determinism | 3 | canonical JSON 285567 bytes, identical SHA256 `e121aefa…e4417` both runs, and equal to the E1 run |
| E7 hash guard | 7 | wrong sha → ok False, forward called 0 times, evaluations_used 0, empty log; load_observation_region refuses wrong hash and missing file |
| F1 load_query_manifest | 10 | ok, 43 ids NGC3198-Q01..Q43 in order (= own parse), radii_text Q01 "0.32"/Q43 "44.08", rad_unit kpc; wrong hash → ok False, no ids; missing file → ok False |
| F2 select_representative_points | 20 | synthetic: hull vertices {10,12,14,16}, hull_vertex_count 4, anchor 9, interior 2 of pool [20,21,25,30], no duplicates, order hull/anchor/interior, 7 points; interior_count 100 → 9 points (4 used); 0 → 5; shared-extreme point appears once (hull_vertex_count 3 = unique); accepted the run-result layout. On the real E1 exploration: hull vertices attain min/max projection on all 3 identified directions |
| F3 evaluate_envelopes | 24 | F3a 5 points: min/max/median/n/valid all match; F3b raising point: per_point[2] invalid with exception text, every query valid False, n_valid 5, numbers over the 5 valid points; F3c NaN at Q17: Q17 valid False (n_valid 6), other 42 queries valid True over 7 points (per-query reading); F3d budget 3 of 7: BUDGET_EXHAUSTED, 3 evaluations, 3 per_point entries, partial min/max over the 3 points; F3e non-dict forward result → invalid, no raise |
| F4 write_freeze_manifest | 29 | ok; file is canonical JSON; schema/units/semantics/within_error_rule present; 43 predictions in query_ids order with velocity=central, band=min/max; target_velocities_included False; manifest_sha256 `fbfefa64…feea` equals own recomputation (canonical JSON without the key); code and input pins equal own byte hashes; no forbidden key; refuses existing out_path (file untouched), `vobs` nested in notes, `Target_Rows` nested in parameter_region, envelopes missing one id, envelopes with an extra id, unreadable code file — no file written on any refusal; manifest with invalid Q17 writable (valid False carried) |
| F5 verify + score | 28 | verify ok, recomputed == recorded, 4 pins ok; score A: ok, not refused, n_rows 43, error_model CONDITIONAL_QUOTED_SIGMA_DIAGONAL_ONLY, within_error_count 20 (= own), band_overlap_count 42 (= own), invalid_count 0, all 12 per-row fields on all 43 rows, residual/sigma_ratio/fractional_error (None at observed 0) all match; refuses id swap, sigma 0, sigma < 0, NaN velocity, inf sigma, 42 rows, wrong id, missing path; manifest C: Q17 row valid False and within_error False despite sigma 1e6, within_error_count 19 (= own from the manifest's valid flags), invalid_count 1, band_overlap_count 41 (valid rows only; 42 if invalid rows counted) |
| F6 tamper | 12 | one byte changed in the first prediction velocity (offset 3125, '9'→'4', still parses): verify ok False (recomputed `37d1468e…` ≠ recorded `fbfefa64…`), score refused True, no rows; pinned scratch input modified after freeze: manifest hash still equal, pin flagged, verify ok False, score refused; notes edited with old hash kept: verify ok False, score refused |

## Expectation corrections made during the run (fixture side, not module side)

1. X0 "no scipy import": my substring check hit the engine docstring "numpy only (no scipy)" (engine line 20); corrected to import statements only. The engine imports hashlib, json, math, numpy; the freeze module imports datetime, hashlib, json, math, numbers, os.
2. E3: my first conflict construction (offsets ±3z on rows with identical Jacobian rows) makes Sᵀr = 0, so the Gauss-Newton step is exactly zero and the engine returned NO_ADMITTED_POINT after the 9 Jacobian evaluations without a repair evaluation. That is a degenerate fixture, not a module defect; replaced by the asymmetric E3a (nonzero step, repair evaluated) and kept the symmetric case as E3b with soft checks.
3. F3d: I first expected no query to be valid under BUDGET_EXHAUSTED; the interface says valid iff "every *evaluated* point" is finite, which the module implements (valid True, n_points 3, n_valid 3). Corrected.

## Observations for the lead (recorded, not judged)

- Under BUDGET_EXHAUSTED, `evaluate_envelopes` reports every query `valid: True` over the evaluated subset, and `write_freeze_manifest` accepted a manifest built from those partial envelopes (3 of 7 points). Root must gate the freeze on `status == 'COMPLETE'`, not on per-query `valid`.
- `run_calibration_region` returns `ok: False` with `status: 'BUDGET_EXHAUSTED'` (budgets 30 and 5) and `ok: True` with `status: 'NO_ADMITTED_POINT'`; the interface fixes neither.
- `band_overlap_count` counts valid rows only (manifest C: 41, vs 42 if invalid rows were counted); the interface does not specify this.
- `unidentified_directions[].trial_projection` = u_trial·v (0.5 here); an extra field `admitted_anchor_projection` is also carried.
- `hull_vertex_count` counts unique points when one point is extreme in two directions (3 for 4 extreme roles).
- Log purposes seen: seed, jacobian, repair, march, bisection, design.

## Untested cases (honest list)

- `finite_difference_jacobian`, `identifiability_report` and `explore_region` were exercised only through `run_calibration_region`, never standalone; the step-halving path (invalid side, `max_halvings`, `min_step`), `failed_columns`, and the resulting `identifiability ok=False` were not exercised.
- March leaving the box before a rejection (box-edge boundary convention) and design points skipped outside [0,1]^n were deliberately avoided by the toy; the skip count and the Halton values/`rng_seed` offset were not verified against an independent implementation (determinism only).
- Identified directions that are not coordinate axes (rotated scaled Jacobian): the boundary comparison is written for general vectors but was only run on axis-aligned ones.
- Damping factor and `max_repair_step` clipping of the repair step (the E2/E3a steps were below the clip and converged in one step because the toy is exactly affine); `repair_iterations` exhaustion with repeatedly nonzero steps.
- Even-count median convention for `central` (F3c accepted mean-of-middle, lower or upper; the all-valid cases used odd counts).
- Forbidden-key scanning was exercised in `notes` and `parameter_region` only, not in `alternatives`, `observation_rule` or `envelopes`; `created_utc` format not checked.
- Permission-denied (as opposed to missing) files; non-UTF-8 or malformed JSON inputs for the region/manifest loaders.
- Thread/process behaviour checked statically only (no such imports), not at runtime.
- Field alignment with the P46 harness (`line_a_prediction_harness_v002.py`) was not checked by these fixtures.
- By rule: no real forward model, no NGC3198 velocity, no project run.
