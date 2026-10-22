# 0391 author notes, V001: common_metric_circular_speed V002

Author: Claude helper (AUTHOR role). A different helper does the static review. V001 and its notes and review were not touched.

## Sources (sha256 from bytes)

| Source | sha256 |
|---|---|
| FROM_CODEX/0391_2026-10-15_circular_speed_underflow_correction.md | 5d579be3fb606f2873d0f78840752056d648ec1d8d9e442c997d3491b154b5a6 |
| common_metric_circular_speed_v001.py (unchanged) | 9bfde58f6d2190d1027ffa62269e65806d0145822144d79589476957a583e8f0 |
| AUTHOR_NOTES_0389_V001.md (unchanged) | dd3a830b9e78c329b236446de301fb512ac0fefbd241501dbd85ee943986c883 |
| STATIC_REVIEW_0389_V001.md (unchanged) | c68fcf2ac4825a5397cd9fc15649b3adb38caae5e6316437c18e260757c61ffb |

## Changed lines (V001 → V002); nothing else changed

| # | V001 | V002 | Change |
|---|---|---|---|
| 1 | L1 | L1 | Header label v001 → `v002 (task 0391: sign/underflow safeguards)`. |
| 2 | L30–32 | L30–34 | Docstring equation conditions: EXACT for zero shift; a negligible nonzero shift is an explicitly bounded approximation handled at the higher level; the radial-coordinate identity stays in the higher-level provider context. |
| 3 | L46 | L48–51 | Docstring "Raises" list adds the three new conditions. |
| 4 | — | L63–64 | Docstring Scope paragraph repeats the zero-shift, higher-level bound and coordinate-identity statement. |
| 5 | — | L101–105 | **Sign check before division.** `if dlogN != 0.0 and (dlogN > 0.0) != (dlogR > 0.0): raise ValueError`. It sits after the existing `dlogR == 0.0` rejection, so dlogR is already nonzero. Signs are found by comparison only, with no product. Since −0.0 != 0.0 is False, a −0.0 numerator counts as zero. |
| 6 | — | L112–115 | **Ratio underflow.** After the division and the existing finiteness check: `if dlogN != 0.0 and ratio == 0.0: raise ValueError`. |
| 7 | — | L122–126 | **Speed computed once.** `speed = c * math.sqrt(ratio)`, then `if ratio > 0.0 and speed == 0.0: raise ValueError`. |
| 8 | L109 | L130 | `"v_local_km_s": speed` replaces the inline `c * math.sqrt(ratio)`. The formula is identical. |
| 9 | L128 | L149–152 | Scope string adds the zero-shift, bounded-approximation and coordinate-identity clause. |

**AST confirmation (parse only).**
- Every dict literal has identical keys in V001 and V002, so the output keys are unchanged.
- The function signatures are identical, with no defaults.
- The imports are still only `math` and `numbers`, and module level is still Import, Import, FunctionDef, FunctionDef.
- The numeric literals are the same set, {0, 1.0}.
- No I/O names appear.
- The only multiplication in V002 is `c * math.sqrt(ratio)`.

The full textual change is in `DIFF_common_metric_circular_speed_v001_to_v002.diff`.

**Order of checks, still fail-fast:**
1. c
2. the container
3. per row: dict and keys, id, R, N, dlogN and dlogR finiteness, R > 0, N > 0, dlogR ≠ 0
4. **sign**
5. division
6. finiteness
7. **ratio underflow**
8. domain [0, 1)
9. **speed underflow**

## ±0.0 cases, worked by hand (IEEE 754; no code run)

**Facts used**
- −0.0 == 0.0 is True, so −0.0 counts as zero in every `== 0.0` and `!= 0.0` test.
- ±0.0 > 0.0 is False.
- (±0)/(nonzero) is a zero whose sign is the product of the signs.
- sqrt(−0) = −0, and sqrt(+0) = +0.
- c > 0 times ±0 is ±0.

A zero denominator, dlogR_dr = ±0.0, is rejected by the unchanged `dlogR == 0.0` check.

### Zero numerator (valid zero-speed read)

| dlogN_dr | dlogR_dr | Sign check | ratio | Underflow check | Domain 0 ≤ ratio < 1 | speed | Speed check | Result |
|---|---|---|---|---|---|---|---|---|
| +0.0 | > 0 | skipped (dlogN != 0 is False) | +0.0 | skipped | passes | +0.0 | skipped (ratio > 0 is False) | valid, v = 0 |
| +0.0 | < 0 | skipped | −0.0 | skipped | passes (0.0 ≤ −0.0) | −0.0 | skipped | valid, v = −0.0 (== 0) |
| **−0.0** | **> 0** | **skipped** | **−0.0** | **skipped** | **passes** | **−0.0** | **skipped** | **valid zero read, as 0391 requires** |
| −0.0 | < 0 | skipped | +0.0 | skipped | passes | +0.0 | skipped | valid, v = 0 |

In two of these cases the reported ratio and speed are a signed zero −0.0. It compares equal to 0, and it is not normalized, because 0391 allows no other change. See unresolved point 1.

### Nonzero numerator

- **Opposite signs, any magnitude.** Rejected at the sign check, before division.
  - Example: dlogN = 1e-300 and dlogR = −1e300. In V001 the quotient underflowed to −0.0, passed `0.0 <= ratio`, and gave v = −0.0. That was the reviewer's finding, and V002 closes it.
- **Same signs, quotient underflows to zero.** For example 1e-300 / 1e300 gives +0.0. Rejected by the ratio-underflow check.
- **Same signs, quotient is a positive subnormal or normal below 1.** It passes. The speed is then c·sqrt(ratio). If that product underflows to 0, which needs a very small c, the speed check rejects it. Otherwise the row is returned.
- **Same signs, quotient ≥ 1.** Rejected by the unchanged domain check.

## Unresolved points

1. **Signed-zero outputs.** A zero read whose zero numerator and nonzero denominator have opposite sign bits (+0.0 over a negative value, or −0.0 over a positive value) yields ratio and v_local as −0.0. Normalizing them to +0.0 would be a replacement, which 0391 does not ask for. The campaign driver or provider may treat it as 0.
2. **Higher-level duties.** The zero-shift statement is documentation only. The function cannot test shift. Bounding a negligible shift, and declaring the radial coordinate, remain the higher-level provider's job.
3. **Check placement.** The sign check is placed after the dlogR ≠ 0 rejection, so "both nonzero" needs only the explicit `dlogN != 0.0` test.

## Deliverables (created exclusively in galaxy_motion_0389/)

- common_metric_circular_speed_v002.py
- DIFF_common_metric_circular_speed_v001_to_v002.diff (`diff -u`, V001 → V002)
- this file

## Execution statement

The module was never executed or imported, and no examples or tests were run. The only Python run on the modules was:
- `ast.parse`;
- an AST comparison of dict keys, signatures, imports, module-level nodes, numeric literals, multiplications and I/O names.

The ±0.0 analysis above is by hand. V002 was made from a scratchpad copy of V001, edited only at the lines listed, and created here exclusively. No network was used, and nothing was written under /Users/bgm/Research/Universal Network Theory.
