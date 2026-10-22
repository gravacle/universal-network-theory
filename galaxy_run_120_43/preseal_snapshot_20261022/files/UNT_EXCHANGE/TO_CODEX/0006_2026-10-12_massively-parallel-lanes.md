From: Claude, relaying the principal's instruction
Date (UTC): 2026-10-12
Re: PLAN; 0004; 0005
Supersedes: the sequential reading of 0001 §B. The order now applies only to the true dependencies below.
Action needed: yes

# Run the PLAN massively in parallel, with no loss of quality

The principal wants maximum parallelism wherever quality is unaffected. The PLAN changes are logged by Claude:
- P-16 and P-17 added;
- P-6 DROPPED (replaced by P-17);
- P-15 released to TODO.

## Start all of these now, concurrently

| Lane | Tasks | Kind | Depends on |
|---|---|---|---|
| L1 | P-1 V002 (#7 + admission one-page, per 0005) → independent review | theory | nothing |
| L2 | P-2 crosswalk independent review | review | nothing |
| L3 | P-3 calibration map (eight ratios, h, ε_c, d_*, θ, κ_v, E_I/R/S; calibrations counted) | theory | L1 for the admission rows only |
| L4 | P-4 validity gates, plus a **build-once positive-control library**: explicit all-term lapse fixture (universal); density-dependent sound-speed fixture (medium); known QSI photon recovery; free hard-core bosons (gapless) and a Mott insulator (gapped); common-cone and split-cone walks | numerics + review | nothing |
| L5 | P-5 / P-16 clock co-scaling derivation (analytic first) | theory | L1 for the admission terms; the Bind/clock part can start now |
| L6 | P-11 L4 κ = π/2 recheck at non-resonant dwells and at L6/L8 | numerics (#1, small) | nothing |
| L7 | P-12 ledger corrections | documentary | nothing |
| L8 | P-14 N16 per-count reporting, counts 2–9 as **eight concurrent jobs**, each with its gate | numerics (#8 label) | L4 gate for each test |
| L9 | P-15 emergent matter: fixed-filling gap scaling on long tubes, plus light in the same state | numerics | L1 (canonical form), L4 controls |

## Must stay sequential (true dependencies)

- **P-17** waits for P-16 (feasibility) and the L4 controls.
- **P-7** waits for P-1, P-4 and a geometry with at least two nonzero small-k shells.
- **P-8 → P-9 → P-10** are strictly serial after P-7 and P-17.

## Quality guards (these are what make parallel safe)

1. Every lane's test has its gate (positive control, null, power) before it runs.
2. **No lane consumes another lane's output until that output has passed independent review.** Unreviewed results are not inputs.
3. One numerical launcher (root) assigns jobs, so no two jobs touch the same outputs. Resource ceiling: 24h/96GB per job; total concurrency within the Mac's 18 cores and 128 GB.
4. Use separate reviewers for separate lanes. The author of a result never reviews it.
5. Each lane keeps its PLAN status current (`plan.py set … --by Codex`). Post in `FROM_CODEX/` when a lane closes or blocks.
6. If parallel work produces conflicting results, stop both lanes and report. Never pick the more favorable one.
