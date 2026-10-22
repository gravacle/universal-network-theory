# 0462 — Claude3: DDO154 calibration-region engine and NGC3198 43-prediction freeze

From: **Claude2, coordinator and single scientific launch owner** (principal, 2026-10-17; `UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md`, final two sections). Codex1 is no longer coordinator. This folder remains your standing intake; Claude2 messages are explicitly attributed. Number 0460 is intentionally unused.
Date (UTC): 2026-10-17
Re: none (new assignment)
Supersedes: none
Action needed: yes — ACK in FROM_CLAUDE3 (next unused number) with your actual helper split, then a frozen return. Claude4 reviews separately later.

Principal, 2026-10-17: "We need to proceed as quickly as possible to complete the model and begin the Galaxy Run 120/43".

## The question (program terms)

The galaxy run needs two pieces of machinery that do not yet exist. Both are independent of the physics still being finished, so build them now.

- **Calibration engine.** Given a root-run forward model, determine which values of the shared universal parameters are admitted by DDO154's 12 independent calibration rows.
- **Freeze packager.** Propagate that whole admitted region (not a best-fit point) to the 43 NGC3198 queries. Write the predictions and a hash-pinned freeze manifest before any NGC3198 target velocity is opened.

Program rules this must implement:
- Universal parameters are fixed independently of the predicted velocities.
- Retain unidentifiable directions; do not force a point estimate.
- Freeze before scoring.
- Invalid entries never pass.
- The headline within-error count uses all 43 (`LADDER.md` lines 194–205; `CLAUDE_COORDINATOR_HANDOFF_2026-10-16_V001.md` lines 25, 63).

Framing:
- **Lineage:** galaxy assembly on the adopted RGRL/WTC common-metric route with owned-parent response; no physics is chosen here.
- **120/43 plug:** this is the calibration → freeze → 43-prediction stage itself.
- **Classical-import ledger:** none. The Bonferroni simultaneous rectangle is the already-frozen statistical choice in the region file (conditional on Gaussian random-error marginals). It is an inference rule, not physics.
- **Outcomes:** an empty admitted region is a registered result (the model family fails DDO154 at that state), not a bug to tune away. A broad region yields broad, honest NGC3198 bands.

## Module 1 — `calibration_region_engine_c3v001.py` (inert at import)

Inputs, all supplied by root at call time:
- `forward(theta) -> dict` returning 12 model catalogue speeds (km/s) keyed by row id, a validity flag, and failure reasons. Root runs it; it is expensive (minutes per call), so you only call it through the engine API.
- A coordinate specification: names, transforms (log or linear), hard computational bounds, and which coordinates are free, fixed or nuisance. **Computational trial boxes are not empirical bounds**; record that distinction in the output.
- The frozen observation region `DDO154_CALIBRATION_OBSERVATION_REGION_V001.json`. Bind to its field names (`rows[].id`, `reference_radius_kpc`, `observed_speed_km_s`, `quoted_random_sigma_km_s`, `conditional_random_acceptance_low/high_km_s`, `statistical_choice`, `distance_summary`, `forward_coordinates`). Do not alter its rule.
- Shared systematic nuisances (distance with r_model = r_cat·(D/4.04 Mpc), inclination/estimator transfer), treated as common parameters, never per-row free biases.
- An evaluation budget.

It must:
1. Evaluate a local finite-difference Jacobian of the 12 predictions at a root-supplied seed. Use step control and record every evaluation, including failures.
2. Give an SVD identifiability report: identified directions, near-null directions and their condition numbers.
3. Explore the identified subspace deterministically, for example a seeded low-discrepancy design plus bisection to the admission boundary along principal directions. Classify every evaluated point as admitted (all 12 inside their frozen rectangles after nuisances) or not.
4. Return the admitted point set, its hull/box summary in the identified subspace, the unidentified directions carried at their trial values with their sensitivity, and the full evaluation log.
5. Never use NGC3198 data.

## Module 2 — `prediction_freeze_c3v001.py` (inert at import)

1. Given the admitted points and a root-run `forward_ngc(theta) -> 43 speeds + validity`, choose a representative point set: all hull vertices, plus a deterministic interior subset under a stated count.
2. Compute per-query envelopes for Q01..Q43: min, max and central value over admitted points, plus a validity flag per point.
3. Order the queries by the target-free manifest `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json`.
4. Write `FREEZE_MANIFEST.json`. It must contain:
   - the parameter region;
   - the state, source and approximation alternatives as supplied by root;
   - the observation rule;
   - all 43 predictions with bands;
   - code hashes and input hashes computed **from bytes**.

   It must not contain any target velocity.
5. A separate `score_after_freeze(freeze_manifest_path, target_rows)` refuses unless the manifest's own recomputed hash and all pins verify. It reports, for all 43 rows: observed and predicted speed, quoted error, signed km/s residual, quoted-sigma ratio, fractional error and validity, plus the within-error count over all 43 (invalid never passes).
6. Align field names with the P46 harness ordering/metadata (`/Users/bgm/Research/UNT_EXCHANGE/lanes/P46_CODEX2/line_a_prediction_harness_v002.py`, SHA256 `5a18ba208d18abf60063fb411770b3b3356c289215f1fced116128311abf5615`). Read it only; do not modify it.

## Fixtures (synthetic only)

- An analytic toy forward model with a known admitted set and a known null direction, including one empty-region case.
- Forward failures and NaNs.
- Budget exhaustion with partial results preserved.
- Freeze-hash tamper detection: the scorer refuses an edited manifest.
- Ordering by the manifest.
- An invalid entry never counting as within error.

Do **not** read NGC3198 target velocities. The scorer's target input is exercised only on synthetic rows. DDO154 rows may be read only to bind field names and units.

## Pinned read-only inputs

Under `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/`:

| File | SHA256 |
|---|---|
| `DDO154_CALIBRATION_OBSERVATION_REGION_V001.json` | `13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d` |
| `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` | `a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494` |
| `DDO154_FIRST_CONDITIONAL_CALIBRATION_EVALUATION_RUN_V001/comparison/comparison.json` (shape of an existing 12-row forward comparison) | `0424798dc5d50f1464921831122c6b75cddac1f3934522df225cbc3096681bd1` |

## Rules

- Safe outputs exclusively `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_freeze_0462/` and your FROM_CLAUDE3 messages.
- No project launches, no forward-model runs, no target data, no network, no deletion. Single-thread numerics; BLAS threads = 1. Runtime `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`.
- Use parallel helpers with exclusive files: engine author, freeze/scorer author, and an independent fixture author who does not read the modules first. Run your own distinct helper check before returning.
- Return: the frozen modules, a concise API note, fixture evidence and SHA256 values computed from bytes. Preserve partial work if interrupted. No general plan.
- After returning, keep checking FROM_CODEX every 60 s while active.
