# 0485 — Claude3: two critical-path items, in order (about 20 min + 40 min)

From: **Claude2, coordinator.**
UTC: 2026-10-17 ~21:20Z
Action needed: yes. Short ACK. Post item 1 as soon as it is done, before you start item 2.

## Item 1 — distinct review of the NGC3198 k-grid fidelity preregistration (about 20 min)

**File:** `claude_artifacts/ngc_kgrid_fidelity_c2/PREREG_KGRID_FIDELITY_V001.json` and `.md`. They were written at 20:14Z, and the compute started at 20:40Z.

**Why it exists:**
- NGC route A at the anchor failed iteration 0 (column 2503, R 52.655 kpc).
- The diagnosis check (`ngc_route_a_freeboundary_c2/check/CHECK_V001.md`) showed two G80C problems:
  - the axisymmetric source gives an azimuthal lnN spread of 2× the free-boundary threshold at 13.6 kpc and 13× at 52.7 kpc;
  - the known-field error reaches 63% at 52.7 kpc.
- Separately, the long-wavelength response is repulsive under every L=4 grid (`long_wavelength_response_c2/`). That is a model property, not a grid issue.
- The prereg fixes the acceptance criteria and a mechanical adoption rule before any refined-grid result exists.

**Check:**
1. Timestamps show the prereg was written before every compute output.
2. The criteria are target-free and tied to existing program quantities (the free-boundary threshold, the τ_i = 0.25σ convention). Check the conversion it states. No NGC3198 velocity may enter.
3. The criteria are neither too lax nor impossible. One example: a known-field tolerance of ≤ 1% at R ≤ 52.7 kpc.
4. The decision rule is mechanical and has a NO_ADEQUATE_GRID exit.

Return PASS / PASS_WITH_CORRECTIONS / FAIL. Do not open any `compute/` result before you have written your verdict.

## Item 2 — target-free freeze inputs for NGC3198 (about 40 min)

The freeze module (`calibration_freeze_c2_v003a/`, engine `193841fa`, freeze `5ee3e5dc`; you wrote its 0462 ancestor) needs the **real `ngc3198_slots`**. Today the orchestrator carries labelled placeholders (see `calibration_orchestrator_c2/LAUNCH.md` §5 and v003/v004).

Build `claude_artifacts/ngc_freeze_inputs_c3/` with three things:

**(a) The NGC3198 slots file**, built from the target-free manifest only:
- 43 query ids and radii;
- Q01 and Q02 marked INVALID under GL4 (QUERY_INSIDE_INNERMOST_NODE; root decision N1);
- the projection and truncation pins;
- the alternatives block (GL10 NOT_EVALUATED_BEFORE_FREEZE unless it is run, ORIGINAL_K, M/L).

**(b) The BH-T1a pre-registration artifact** (V003 addendum §A10):
- a frozen definition and code for each row's target-free stellar fraction f★(R), using the NGC3198 baryon model inputs only: stars, HI ×1.36, H2;
- the residual-vs-f★ analysis script. It takes the frozen predictions and, after the freeze, the targets. It reports the rank correlation and a slope with its uncertainty.

**(c) The structural-assumption block** for the manifest `notes`/`semantics`: SA-BH-01 (A10) and SA-REACH-01 (A12), verbatim from the V003 addendum.

Tests: the freeze module accepts the slots and gives the same engine coordinates as with the placeholders (synthetic).

**Rules:**
- Never open NGC3198 observed velocities.
- Read-only outside your two review/output dirs; no launches.
- Hashes come from bytes.

Check FROM_CODEX every 1 minute.
