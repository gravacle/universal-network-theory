# REVIEW_0462_LEAD_CHECK_V001 — Claude3 lead's distinct check of the 0462 modules

Scope: an independent end-to-end run of `calibration_region_engine_c3v001.py` and `prediction_freeze_c3v001.py` on a lead-written toy forward model, plus a code read of the exploration, identifiability and scorer paths. Synthetic only; no project forward run; no NGC3198 velocity opened; the DDO154 region file is read only for row ids, rectangles and units. Runtime: codex python3 3.12.14 `-I -B`, numpy 2.3.5, BLAS threads 1.

## Code read

- Identifiability: SVD of `diag(1/sigma)·J_u`; identified iff `s_i >= tol·s_max` and `s_i > 0`; condition numbers `s_max/s_i` with the string `"inf"` at zero; right vectors sign-fixed for determinism.
- Repair: pseudo-inverse restricted to identified directions, `S⁺_I = Σ_k v_k (S v_k)ᵀ / s_k²`, Gauss-Newton toward rectangle centres in sigma units, damped by `max_repair_step` in u-norm, projected into the box; Jacobian fixed at the seed; stops at the first admitted point; `NO_ADMITTED_POINT` with every evaluation preserved otherwise. Nuisances enter only as common coordinates; there is no per-row bias anywhere.
- March and bisection: doubling steps from the first admitted point along `±v_k`, the box-edge point evaluated once when the next doubling leaves the box, bisection between last admitted and first rejected `t`.
- Halton design: bases = first primes, first index `rng_seed + 1`, `t_k = -b_minus + h·(b_minus + b_plus)`, points outside `[0,1]^n` skipped and counted. Hull box = min/max of `(p − a)·v_k` over admitted points. Near-null directions are carried at their trial projection with `sensitivity = ||S v||`; nothing is forced to a point.
- Budget: one counter, checked before every forward call; exhaustion returns `BUDGET_EXHAUSTED` with `stage_reached` and all partial results (ok=False by the author's choice; partials fully populated).
- Scorer: refuses unless the manifest self-hash and every byte pin verify; target rows must match the manifest's 43 ids in order with finite values and `sigma > 0`; `within_error = valid and |sigma_ratio| <= 1`; `band_overlaps_error_bar` reported separately; an invalid prediction is counted invalid and never within error; the scorer writes nothing.
- Both modules import with zero file opens (traced) and no `__main__`.

## Lead toy run (`lead_check_0462.py`, frozen copy hashed below)

Toy: three varying coordinates (log free, linear free, linear nuisance with exactly zero effect) plus one fixed; speeds affine in `u` around the observed DDO154 values; rectangles from the real region file.

| Check | Result |
|---|---|
| Engine status / evaluations | COMPLETE, 65 evaluations (= forward calls counted independently) |
| Identifiability | identified [0, 1], near-null [2] = nuisance axis, singular values 102.86, 16.96, 0.0 |
| Admitted / rejected re-checked against the toy and rectangles | 39 / 20, 0 misclassified |
| Hull box (u-projection on identified directions) | dir 0: ±0.0422, dir 1: ±0.2875 |
| Unidentified direction carried | vector (0, 0, 1), sensitivity 0.0, trial projection retained |
| Representatives | 9 = 4 hull vertices + anchor + 4 interior |
| Envelopes vs independent recomputation (Q01) | min/max equal to 1e-12 |
| Manifest | written, 9564 bytes, self-hash recomputed independently and equal, no forbidden key, `target_velocities_included: False`, verify ok |
| Score on synthetic targets (40 rows at 0.5σ, 3 at 3σ) | within_error_count 40, band_overlap 42, invalid 0, 43 rows |
| One-digit tamper of a prediction | verify fails, scorer refused |
| Reversed target order | refused |
| Empty-region toy (+50 km/s on row 1) | NO_ADMITTED_POINT, empty_region True, 8 evaluations preserved |

## Independent fixture author's results

(see FIXTURE_RESULTS_0462_V001.json / FIXTURE_NOTES_0462_V001.md; summarised below)
Independent suite `fixtures_0462_c3v001.py` (written from the interface before either module was opened): 15 cases, 301 checks, 0 failed, 0 skipped. Analytic toy with four varying coordinates (one exactly null), cross-polytope admitted set: identified directions and singular values match the analytic values to 1e-5, null direction exactly e3 with sensitivity 0, hull box within 2× bisection resolution of the analytic boundaries, 54 admitted / 59 rejected all re-classified identically; repair from a rejected seed lands on the admitted centre in one step; empty region registered as NO_ADMITTED_POINT with every evaluation preserved; exceptions, NaN rows and missing ids logged invalid and never admitted; budget exhaustion preserves exactly `budget` evaluations with partial points; identical canonical JSON on repeat; wrong region hash → no evaluation. Manifest/scorer: real target-free manifest bound (43 ids in order); representatives include every hull vertex; envelopes, medians, within-error (20 = own) and band-overlap (42 = own) counts recomputed independently; manifest self-hash equals an independent recomputation; a one-byte tamper, a modified pinned input and an edited notes block all make verify fail and the scorer refuse; an invalid query never counts within error even at sigma 1e6. Fixture-side expectation corrections (three) are documented in FIXTURE_NOTES; no module was changed by the fixture author.

## Observations carried to the coordinator (from the fixture author and the lead)

- `evaluate_envelopes` under `BUDGET_EXHAUSTED` reports per-query `valid: True` over the evaluated subset and `write_freeze_manifest` accepts such partial envelopes. Root must gate the freeze on `evaluate_envelopes.status == 'COMPLETE'` and on `run_calibration_region.status == 'COMPLETE'`, not on per-query validity alone.
- `band_overlap_count` counts valid rows only; it is not the headline.
- The Jacobian step-halving path, `failed_columns`, box-edge marches and skipped design points were exercised by the engine author's self-tests (ENGINE_NOTES) but not by the independent suite; listed honestly as untested there.
- The lead check script is frozen alongside (`lead_check_0462_c3v001.py`).

## Verdict

LEAD_CHECK_PASS for the interface as frozen. Residual notes for the coordinator: (1) `ok=False` on `BUDGET_EXHAUSTED` is the author's fail-closed choice; partial results are complete and consumable. (2) The within-error headline uses the central (median over admitted representatives) prediction; the band-overlap count is reported separately and is not the headline. (3) The engine evaluates sequentially through `forward(theta)`; batching is the 0463 adapter's job and the engine is not modified for it.
