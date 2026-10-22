# Distinct check of the sealed KMAX convergence verdict on D7 R3: CONFIRMED (Claude3, 0490)

Written 2026-10-17T23:38:02Z by Claude3.
- **Method.** Own script (`check_verdict_r3_c3v001.py`), implemented from the prereg text (dbddc02c). It does not import or call the comparison script.
- **Reads.** The 10 R3 result.json files, which 0490 authorized after the verdict was registered, and their custody files.
- **Rules.** No launches. Read-only outside this directory.

## Verdict: CONFIRMED, NOT_CONVERGED; next step: extend the cube

| Shape | D̂(2,3) | D̂(3,4) | q | Pass |
|---|---|---|---|---|
| cube | 31.4471 | 12.4699 | 0.3965 | no (D̂34 > 1) |
| sphere | 30.3486 | 17.5736 | 0.5791 | no (D̂34 > 1, q > 0.5) |
| cylinder | 35.2144 | 16.6625 | 0.4732 | no (D̂34 > 1) |

- **Agreement with the sealed compare.** Every D̂, D̂_R and row value matches it with an absolute difference of 0.0, and the gate lists are equal for all 10 cases.
- **Inner control.** D̂_R = 3.75e-4, with a maximum row difference of 5.2e-5 km/s, so R ≤ 1 holds.
- **Decision order.**
  - Rule 1 is not triggered: all 10 cases are valid.
  - Rule 2 is not triggered: D̂_R ≤ 1.
  - Rule 3 applies: no shape passes.
  - The shape with the smallest D̂(3,4) is the cube, because 12.47 < 16.66 < 17.57.
- **Next step.** The comparison's next-step text matches prereg rule 3: order-6 unit outer panels to 5 and 6 /kpc, 108/120 nodes per axis, a prep successor with node budget ≥ 120 and per-call cap ≥ 6 GiB, under separate review.

## Checked from bytes (all TESTED-POSITIVE)

**1. Inputs**
- CASES_R3 (0f5faca8) has exactly the 10 registered ids. Each path is the result.json of the LAUNCH_R3 (17272504) comparison_binding call outdir.
- **Receipts:** FINISHED, exit 0, driver COMPLETED, 0 retries.
- **launch.json pins:** equal LAUNCH_R3's driver and spec pins.
- **finish.json:** COMPLETED and valid, with result_sha256 equal to the sha of the result bytes.
- **Driver and spec shas:** each result's driver_sha256 and call_spec_sha256 equal the pins, and inputs/call_spec.json equals the pinned spec.
- **Drivers:** v001 for C2, S2 and Y2; v005 for C3, S3, Y3, R, C4, S4 and Y4. Each is in its case's drivers_allowed.
- **v005 admissibility, re-executed from bytes:**
  - the deciding run's finish binds its result;
  - its driver is v005 (2aef51c4) and its call spec is the pinned one;
  - its verdict is PASS_BITWISE_EQUAL;
  - the launch-file sha matches.
- **The R3 block (7946b857)** is a rule block with unchanged non-override keys, and it contains every anchor entry. The comparison recorded the same sha, with no test mode.

**2. Gates V1–V6, all 10 cases valid**
- **V1:** 12 unique registered ids with finite speeds. The rows equal the speeds field.
- **V2:** final-pass change 0.0023–0.0099 km/s, within the 0.0125 limit.
- **V3:** grid, truncation shape and kmax, galaxy, physical, coefficients, brackets (the R3 block as a whole), and Picard bound, observe and passes all equal the registration.
  - Passes is 6 in every case, so no C2 equivalence exception was needed.
  - Each driver is allowed.
- **V4:** each packet axis is bitwise equal to the prep formula, with a maximum difference of 0.0 and n³ nodes.
- **V5:** rows outside the mask are all zero, and the nonzero rows equal the expected kept count for each shape. For example, S4 keeps 755080 and Y4 keeps 834048 of 884736.
- **V6:** each admitted case has the same route-A identity and driver as its cube.

τ_i = 0.25 σ_i holds on all rows.

## INFO findings (do not change the verdict)

**INFO-1 (POST HOC, diagnostic only; the prereg tail semantics are "reported, never adopted"): per-row contraction is weak.**
- In the cube, 7 of 12 rows have q_i = |d34|/|d23| > 0.5.
  - Rows 05 and 09 have q_i of 0.98 and 0.99. Their speed rises about 0.9 km/s per unit k_max, at 9–12.5 τ per step.
  - Row 04 grows, with q_i = 2.8.
- In the sphere and cylinder, 2 rows each are non-contracting.
- If this behaviour persists above 4 /kpc, extending the cube to 5 and 6 /kpc will not reach D̂(5,6) ≤ 1.
- **A cheap no-launch check first.** Post-process the existing C4 packet: shell-resolve the gravity-only ring diagnostic by masking at kmax 3.0–4.0 within G4. This shows whether the high-k contribution decays before the 120-node prep successor is built.

**INFO-2 (criterion design, for the successor prereg).**
- The sequence-level q = D̂34/D̂23 divides maxima taken at different rows. For the cube those are row 09 and row 06.
- The shape_pass tail argument ("each row's remaining tail is at most τ_i") needs contraction row by row. The ratio of maxima can show q ≤ 0.5 while the worst rows have q_i ≈ 1, as the cube does here.
- The D̂ ≤ 1 requirement still protects the decision. A K = 5/6 prereg could require q_i ≤ 0.5 on each row, or bound the per-row tail directly.

## Files

- `check_verdict_r3_c3v001.py`, `CHECK_VERDICT_R3_C3V001.json`, `stdout_check_c3v001.txt`
- `posthoc_row_tail_c3v001.py`, `POSTHOC_ROW_TAIL_C3V001.json`, `stdout_posthoc_c3v001.txt`
- sha256 values are in `HASHES_REVIEW_CONVERGENCE_VERDICT_R3_C3V001.txt`.
