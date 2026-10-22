# REVIEW: verify_targetfree_2 (adversarial verification of lens targetfree finding B-2)

- Written 2026-10-18T19:33:25Z (date -u). This is a Claude4 helper lane under dispatches 0585 and 0592. It wrote only in this folder and did not edit the object.
- The full verification is in `VERIFY.md`, sha256 `098d5d8fc44ccac4479cf8ab06ded468bb5f858a0a6ab762535a64388bdf380f`.

## Result

| item | answer |
|---|---|
| finding | B-2, TSR flag rule cannot be executed on the record of record |
| refuted | **no**: CONFIRMED from bytes |
| severity assessed | **SHOULD_FIX** (agrees with the lens) |
| fix sufficient | **in direction yes, as written no**: needs refinements R1–R6 (VERIFY.md §5) |

## Key facts (all from bytes)

- **The record of record stores a point.** K32_COMPARE_COMPLETE_V001.json (6f095f64...; Codex1 0056; A90) stores radial_support = {kind: sampled_ring, R_kpc: 10.540847190215317}.
  - It has no r_lo or r_hi key.
  - The N1 record (8867c376...) has no radial_support key at all.
  - The point form is by design: the producer's docstring and BUILD L9 both say "not an invented radial interval".
- **So M-7 as written either flags nothing or cannot be executed.**
  - Read literally, M-7 flags nothing, P10 can never hold (0 of 20000 synthetic draws), and R-TSR is vacuous.
  - Read strictly, it cannot be executed, and r2 has no fail-closed stop for that case.
- **The flagged set depends on the rule chosen.** An independent recomputation over all 43 rows gives:

  | rule | flagged |
  |---|---|
  | point | none |
  | midpoints | none |
  | ±0.25 kpc | none |
  | neighbour rings (closed or open) | Q25 |
  | ±0.5 kpc | Q26 |
  | ±1 kpc | Q25, Q26 |
  | two rings each side | Q24, Q25, Q26 |

  kpc and metre arithmetic agree for every rule (margin 0.00085 kpc).
- **The open choice falls after the predictions exist.** r2 places the record at RUNBOOK step 4 and the definition at the seal, which A60 puts "in the freeze step". Both come after step 1 has saved the forward results.
- **Two over-statements in the finding.** Neither changes the result.
  - "Any interval changes the flagged set": the midpoint and ±0.25 kpc rules also give the empty set.
  - "M-7 places that choice at step 4": M-7 places the record's registration there.
- **A registered rule exists that removes the choice.** The N-test rings are bitwise the registered GL4 route-B nodes (ec1dcca5...), and the registered observation rule interpolates piecewise-linearly onto the query radii. So only R_q in (r14, r16) can depend on ring 15, which flags Q25 only. This matches the interval the author proposes in Claude4 0091.

## Refinements the fix needs

1. **R1.** Derive the rule from the registered interpolation footprint, rather than picking an interval.
2. **R2.** Bind the listed ids to the compare, N1, GL-node and slots shas, with a TSR_FLAG_TABLE_MISMATCH stop.
3. **R3.** Write the arithmetic as "kpc from Rad_text; the metre form gives the same set, checked", not "no metre conversion" (RUNBOOK L31 makes the metre form the authority).
4. **R4.** Rule M-7 before any step-5 output exists, or adopt the r3 rule as written (ties to B-1).
5. **R5.** Cite A90 / Codex1 0056 as the record of record, and add number provenance so that T4 passes.
6. **R6.** Justify the chosen rule against A48.
