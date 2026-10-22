# 0392 author notes, V002 delta: formation_frequency_coefficient_v002.py

Author: Claude helper (AUTHOR role). A different helper does the review.

This version responds to REVIEW_0392_V001.md (sha256 03791db18ed596f39c08b6bb19e70e4ed2b46db3bd89c2e9361a60144aa5339a): F1 (LOW) and F6 (INFO).

V001 is untouched: formation_frequency_coefficient_v001.py is `a577918048e6df5a72d522ce3131e9ea488ab4ae3692965b5fa76a1435606e41` and AUTHOR_NOTES_0392_V001.md is `7d2e9f21ccf578ecaad6e516c45ab9a29d6863457ba64fadb9cf579ce44fc5cf`. The full change is in `DIFF_formation_frequency_coefficient_v001_to_v002.diff`.

## Changed lines (V001 → V002)

| # | V001 | V002 | Change |
|---|---|---|---|
| 1 | L1 | L1 | Header label v001 → `v002 (review F1/F6: …)`. |
| 2 | L168 | L168–169 | Scope string adds that this is the j = 0 reference coefficient, with no source argument and no source shift in D_ab (F6). |
| 3 | L212 | L213–214 | Docstring: every D_ab^p must be finite and > 0, and the j = 0 reference is stated (F6). |
| 4 | L240 | L242–244 | Docstring scope: j = 0 reference; the bound's intermediates must be finite and positive, or the call fails closed. |
| 5 | — | L434–442 | **Moment check (F1, related).** Before r_p is computed, for each p ∈ {2, 3, 5, 7}, `D_p = D ** p` must be finite with every entry > 0. A zero entry (underflow) or a non-finite entry (overflow) records a failure and skips that σ, which fails closed. r_p is still computed by the unchanged repeated division. |
| 6 | L478 | L491–508 | **Bound intermediates (F1).** `m9 = m ** 9`, `az6 = az ** 6` and `one_minus = 1.0 - ratio` are computed once. The bound is computed only if all three are finite, m9 > 0 and one_minus > 0. Otherwise `bound = None` and an explicit failure is recorded, giving ok = False. The formula is unchanged: bound = 2·az6/(m9·one_minus). |
| 7 | L483 | L513 | The finiteness gate tests the bound only when it was computed. A missing bound has already produced its own failure. |
| 8 | L490 | L520 | `"frequency_remainder_bound"` is None when the bound was not computed. The output key set is unchanged. |

## Nothing else changed (parse-only confirmation)

- The diff contains only the hunks listed above.
- AST checks:
  - Every dict literal has the same keys in V001 and V002.
  - The signatures are identical, with no defaults.
  - Module level is still the numpy import plus 8 defs.
  - There are still 7 einsum calls, all with optimize=False.
  - There is no @, dot, matmul, errstate or warnings use, and no I/O.
- Unchanged:
  - the formulas for q, w, D, r_p, F, F4 and the bound;
  - admission, reference, eigensystem, gap, weight-sum and |z| < m_σ checks;
  - all other outputs.

## Effect, by hand (not executed)

- **Large m.** For m_σ > ~1.78e34, m**9 overflows to inf (with an unsuppressed RuntimeWarning). V001 returned a 0.0 bound with ok = True. V002 now fails closed.
- **Small m.** For m_σ < ~1.2e-36, m**9 underflows to 0, so m9 > 0 fails and the call fails closed. V001 also failed here, through 0/0 → NaN.
- **Large or small D.** For D_ab > ~1e44, D**7 overflows; for D_ab < ~1e-44 (above pos_tol), D**7 underflows to 0. V002 fails closed in both cases, before r_5 or r_7 can silently lose meaning.

## Unresolved

V001 points 1–8 are unchanged: the bound has no Σw factor, F is evaluated at the exact z, |z| < m_σ is strict, and so on. The D**p arrays are used only as a domain check and are not reused in r_p. This keeps the reviewed repeated-division arithmetic unchanged.

## Execution statement

Nothing was executed or imported. The only Python run on the modules was `ast.parse` and an AST comparison of dict keys, signatures, module-level nodes, einsum keyword arguments and forbidden names. V002 was made from a scratchpad copy of V001, edited only at the listed lines, and created here exclusively. No network was used, and nothing was written under /Users/bgm/Research/Universal Network Theory.
