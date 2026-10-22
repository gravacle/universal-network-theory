# REVIEW 0392 V002 DELTA: F1/F6 closure check of formation_frequency_coefficient_v002.py

Reviewer: Claude helper (DISTINCT REVIEWER; did not author V002). Date 2026-10-15. This is a delta check only, against REVIEW_0392_V001.md (03791db18ed596f39c08b6bb19e70e4ed2b46db3bd89c2e9361a60144aa5339a).

## Verdict: PASS_WITH_NOTES

F1 and F6 are closed. The formulas, the output keys and every other check are unchanged. Notes N1 to N3 are all INFO.

## Hashes (sha256 from bytes)

- formation_frequency_coefficient_v002.py: 829b2db2f8e845802cadaa91eb8933dfbf9603c52312b88b9e2142f7b73ce265 (matches).
- DIFF_formation_frequency_coefficient_v001_to_v002.diff: f5cd7c9bb72b5a896211b724064037e898b3c4be01386520fc797a95b43cf982 (matches).
- AUTHOR_NOTES_0392_V002_DELTA.md: 5156c2cbc273661c85c9e2d7eedbebc93eaf8a678459156109088661ef3e33e3 (matches).
- Unchanged:
  - V001: a577918048e6df5a72d522ce3131e9ea488ab4ae3692965b5fa76a1435606e41;
  - REVIEW_0392_V001: 03791db1… (full hash above).
- File mtimes show no other file in the directory was modified after 18:37.

## (a) Diff scope

My regenerated `diff -u` hunk bodies are identical to the delivered DIFF; only the header timestamps differ. The hunks are exactly:
- the header (L1);
- the j = 0 wording in the scope string (L168–169) and the docstring (L213–214, L242–244);
- the moment gate (L434–442);
- the bound-intermediate gate (L491–508), with the matching `bound is None` handling in the finiteness test (L513) and the output (L520).

Nothing else changed.

## (b) Unchanged logic (AST, parse only)

On a V002 parse I made five reverts:
- dropped the moment-gate `for` loop and its following early `continue`;
- replaced the m9/az6/one_minus assignments and the `If` with V001's single `bound = 2.0 * az ** 6 / (m ** 9 * (1.0 - ratio))`;
- reverted `bound is None or np.isfinite(bound)` to `np.isfinite(bound)`;
- reverted `None if bound is None else float(bound)` to `float(bound)`;
- normalized all strings.

The result is IDENTICAL to V001's AST. The dict-key sets are identical, and there are still 7 einsum calls, all with optimize=False. MatMult is absent, numpy is the only import, and the module body is unchanged.

## (c) F1 closure, by hand (float64 thresholds; no module code run)

**Bound gate (L491–508).**
- m9 overflows exactly when m_σ > 1.78e34. V001 returned bound = 0.0 with ok=True there; V002 fails closed. **F1 closed.**
- m9 rounds to 0 exactly when m_σ < 1.11e-36. V001 already failed there (inf, or 0/0 = NaN); now the failure message is explicit.
- one_minus ≤ 0 can arise only by rounding, since stage 5 enforces az < m, so ratio ≤ 1. V001 failed there too, through division by zero.
- az6 is always finite when m9 is finite, because az < m < 1.78e34 gives az^6 < 3e205. That test is redundant but harmless.
- So the bound gate newly rejects only the regime where V001's bound was wrong.

**Moment gate (L434–442).**
- Its binding case is D**7: overflow above 1.09e44, and rounding to 0 below 5.89e-47.
- Large side, uniform offset-dominated tables: m > 1.78e34, where V001 was already wrong. The silent loss of r5 and r7 is now rejected.
- Small side: any D below 5.89e-47 means m < 1.11e-36, where V001 already failed. No new rejection here.
- With D**7 normal, every w/D^7 term with O(1) weight is at least about 5e-309 and keeps essentially full precision.

**No valid V001 result is newly rejected, with one exception (N1).**

## (d) F6 closure

"j = 0 reference coefficient" is now stated in:
- the docstring at L214 ("j = 0 reference: there is no source argument and no source shift in D_ab") and L242;
- the scope string at L168–169.

**F6 closed.**

## Notes

| ID | Severity | Line | Note |
|---|---|---|---|
| N1 | INFO | L434–440 | **Narrow over-rejection.** A mixed-scale table with max D_ab > 1.09e44 but m_σ ≤ 1.78e34 is rejected, although V001's r_p, F and bound were meaningful there: the huge-D terms merely underflow. The regime needs all of the following:<br>• a block spread ‖H‖ ≳ 5e43;<br>• resid_tol ≳ eps·‖H‖ ≈ 1e28 to pass the eigen checks at all;<br>• m ≫ 1e28 for m to be meaningful.<br>It is fail-closed and absurd in scale. No change requested. |
| N2 | INFO | AUTHOR_NOTES (V002 delta) | The notes say D**7 "underflows to 0" for D below about 1e-44. In fact D**7 is subnormal (> 0, and passes) for D between 5.89e-47 and 1.12e-44, and is 0 only below 5.89e-47. This is documentation only. |
| N3 | INFO | L501 | For m_σ in [1.11e-36, 6.55e-35), m9 is subnormal and the bound loses precision, as it did in V001. Requiring m9 to be normal would remove this; it is optional. |

## Execution statement

Static only. Neither module was imported or executed. My `python3 -I` runs were a scratchpad AST script over the file text (`ast.parse`, `ast.unparse`, `ast.dump`) and one arithmetic line for float64 power thresholds; no module code was involved. No network was used, no reviewed file was modified, and nothing was written under Universal Network Theory. This file was created exclusively (noclobber).
