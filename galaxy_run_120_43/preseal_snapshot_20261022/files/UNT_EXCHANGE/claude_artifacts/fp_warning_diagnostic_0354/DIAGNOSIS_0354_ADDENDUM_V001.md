# 0354 diagnosis addendum V001: independent-review refinements and the corrected patch proposal V005

**Author:** CLAUDE2 main lane.
**Reviewer whose findings are incorporated:** Claude helper ab750e45705a5599e, verdict PASS_WITH_NOTES.

This addendum amends `DIAGNOSIS_0354_V001.md` (a83200b6…). That file is retained unchanged. As before, only generic matrices were used.

## Refinements to the diagnosis (review N4)

1. **Type dependence.**
   - float64 C-ordered square products flag at N ≥ 15.
   - float32, complex64 and complex128 flag at N ≥ 16.
   - int64 never flags, because it does not use BLAS.
2. **Shape dependence.** The trigger tracks the output shape, not the square size.
   - Flag: 40×7 @ 7×40, 64×2 @ 2×64, 16×16 @ 16×17.
   - No flag: 15×40 @ 40×7, 1×24 @ 24×24, 24×24 @ 24×1, 3×24 @ 24×3.
3. **Flag kinds carry no information at N ≥ 15.**
   - At N = 2, a genuine overflow raises only `overflow`.
   - At N = 16, a genuine overflow, a NaN input and a genuine underflow each raise all four flags.
   - So finiteness and independent verification, not flag kinds, are what distinguish a genuine event.
4. **Rounding is ordinary.** For random non-integer floats at N = 16 and 24, the maximum error against exact Fraction arithmetic is 0.09–0.14 of the standard γ_k·|A||B| bound.
5. **Not sticky.** An elementwise operation right after a flagged matmul raises no flags.
6. **`np.dot` stays silent even on a genuine overflow.** Switching to it would hide real events, so it is rejected as a remedy. einsum is rejected because it would change the numerics.
7. **Site attribution of the saved warnings is partly inferred.** The saved output kept only the first 50 entries, all at V002 line 136 (`eig`). The attribution of the remaining 958 warnings to the spectral-inverse and inverse-residual sites is inferred from the count. The inference is consistent with every generic run: 1008 per case when the inverse loop runs, 512 when it is skipped.

## Patch proposal V005 (supersedes V003; V003 and V004 retained)

Numerics are unchanged: each site still calls the same `A @ B`. Only the accounting and labels changed.

| Note | Change |
|---|---|
| N1 | Per-site counters `nonfinite_products`, `bound_evaluated_products`, `bound_failed_products`. `all_within_nonblas_bound` is `null` whenever any flagged product was non-finite (the bound was not evaluated); it never reads `true` in that case. The deviation maximum is taken over finite deviations only, and the field is renamed `max_abs_deviation_over_finite_deviations`. |
| N2 | The verified label is renamed `FLAGGED_PRODUCTS_FINITE_WITHIN_NONBLAS_ROUNDING_BOUND`. It is assigned only if nothing was non-finite, nothing failed, and the bound was evaluated for every flagged call. Otherwise the label is `FLAGGED_PRODUCT_NOT_VERIFIED`. A `classification_meaning` text matching the assigned label states that verification does **not** establish the flags were spurious. |
| N3 | The bound gains an absolute underflow term: 64·k·eps·(|A||B|) + 64·k·smallest_subnormal. |
| — | Output schema label: `BIND_COUPLING_REFERENCE_OUTPUT_V005_PROPOSAL`. |

V004 carried N1–N3, but its `classification_meaning` always described the verified label. V005 matches the meaning to the label actually assigned. V004 is retained as superseded.

## Evidence V005 (`patch_evidence_v005.py`, 14/14, stderr empty)

**E1–E7, E6b, E6c:** the V003 set re-run against V005, with the new labels and the N1 null asserted.

**N5 additions:**

| Test | Check | Result |
|---|---|---|
| E8 | In-pipeline non-finite flagged product. A TEST-ONLY injection places an inf in a full-inverse `solve` after `eigh` succeeded. | The `inverse_residual` site reports `nonfinite_products ≥ 1`, `all_within_nonblas_bound` null and NOT_VERIFIED. L4 gives CASE_ERROR, the run FAILED with exit 1, and L6 is unaffected. |
| E9a | `errstate` / `seterrcall` after an exception inside `mm` | Restored |
| E9b | Inside an outer `errstate(all='raise')` | `mm` does not raise, and a plain flagged matmul afterwards still raises |
| E10 | One injected out-of-site 1/0 | Stays visible: the proposal captures L4 1 and L6 0, against V002's 1009 and 1008. Content is identical to the clean run. |
| E11 | Subnormal-result product | Bit-identical to the plain matmul, flagged and verified via the absolute term |

## Remedy options for root

| Option | Effect |
|---|---|
| No code change | V002 already records the warnings without gating on them. The diagnosis explains them; numerical acceptance remains root's. |
| Adopt the V005 pattern | Bit-identical numerics, with every flagged product verified and reported. It needs a separately reviewed producer version on fresh immutable paths, a new launcher pin and a root decision. |

0355's shared-junction producer declares its dependence on this V005 pattern, pending delta review.
