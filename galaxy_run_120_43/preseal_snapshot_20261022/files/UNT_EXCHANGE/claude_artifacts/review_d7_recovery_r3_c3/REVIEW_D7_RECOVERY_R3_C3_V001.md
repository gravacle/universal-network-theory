# REVIEW_D7_RECOVERY_R3_C3_V001 — Claude3 blind derivation and check of D7 recovery block R3 (dispatch 0483)

Reviewer: Claude3 (Claude Opus 5.5). Read-only outside this directory; no launches; no `result.json` opened. Files: `blind_w1_r3_c3v001.py` → `BLIND_EXPECTED_R3_C3V001.json`, hashed in `BLIND_TIMESTAMP_R3.txt` at 2026-10-17T19:59:43Z while `KMAX_D7_RECOVERY_R3.json` did not exist (R3 written 20:03Z); `check_r3_c3v001.py` → `CHECK_R3_EVIDENCE_C3V001.json`.

Bytes: blind script `2a8c80a0…cb63`, blind result `ddbd42ce…21b3`; R2 `ff7cf806…93fd` (start point, pin verified); R3 as checked: see `CHECK_R3_EVIDENCE_C3V001.json` (`R3_sha256`).

## Verdict: PASS

**Blind derivation (from R2, using only the column `*_failure.json` / `*_iterations.jsonl` of KMAX_A2F10_{C4R2,S4R2,Y4R2}_D7R2_RUN_V001).** All nine misses are `MASS_ENTHALPY_NOT_BRACKETED` in the fs pass, on columns that have no fs override in R2 (bracket = fs template [1.5125e8, 3.025e8]; every evaluated end equals it). In every case the residual is negative at both ends, strongly at 1.5125e8 (≈ −0.75 to −0.78) and only slightly at 3.025e8 (−0.00012 to −0.0091), so the root lies just above hi. W1 step A: hi → 1.05·template_hi = 317625000.0; lo kept. New entries [1.5125e8, 3.17625e8] for columns **2, 66, 67, 68, 71**; everything else equal to R2.

| Column | Cases | r(1.5125e8) / r(3.025e8) | W1 |
|---|---|---|---|
| 2 | C4R2, Y4R2 | −0.754 / −0.0058; −0.755 / −0.0088 | A, hi → 3.17625e8 |
| 66 | C4R2, S4R2 | −0.765 / −0.0006; −0.769 / −0.0090 | A |
| 67 | C4R2, S4R2 | −0.766 / −0.0035; −0.769 / −0.0091 | A |
| 68 | C4R2, S4R2 | −0.766 / −0.0003; −0.768 / −0.0034 | A |
| 71 | Y4R2 | −0.776 / −0.0001 | A |

**The two confirmations asked in 0483.**
1. **No new miss lands on an entry already widened.** None of 2, 66, 67, 68, 71 has an fs entry in R1 or R2 (the R2 `rfs_factor_overrides[71]` is a different pass and is unchanged). So no step B occurs and nothing is BRACKET_RECOVERY_EXHAUSTED.
2. **No direction conflicts.** Column 2 (C4R2 and Y4R2) and columns 66–68 (C4R2 and S4R2) are root-above-hi in both cases.

**Comparison with the builder's R3.** R3's `brackets.rule` is canonically identical to the blind derivation; the changed fs entries vs R2 are exactly 2, 66, 67, 68, 71; every R2 entry is contained; all other rule keys equal R2. The sealed `kmax_compare_c2v005.validate_recovery(prereg V005, R3.brackets)` returns no reasons. The 52 pinned evidence files match their bytes, none is a `result.json`, and the nine residual pairs equal mine; the builder states and its code confirms that `result.json` is never opened. D7 step 4: all 10 cases (C2R3, S2R3, Y2R3 on v001; C3R3, S3R3, Y3R3, RR3, C4R3, S4R3, Y4R3 on v005) are regenerated with brackets equal to R3, each differing from its R2 counterpart only in `label` and the five new entries. The superseded in-flight R2 runs are recorded in `STOPPED_R2_RUNS_V001.json` with times, PIDs, last stage and reason. `HASHES.txt` 146/146 match; no `*D7R3*` run exists yet.

## Notes
- After R3, 18 fs entries sit at the hull [1.5125e8, 3.17625e8]: 2–9, 45–50, 66–68, 71. Any further miss on one of them is a W1 step B (lo/2 or 2·hi); a repeat after step B is BRACKET_RECOVERY_EXHAUSTED.
- The kmax-4 misses all sit within 1 % below the old hi, at the innermost and outermost fs columns, which suggests the solved enthalpy there drifts upward with k_max. That is an observation, not a W1 issue.
