# 0403 static review: adversarial domain, input and inertness (v001)

**Role:** distinct reviewer, not the author. Lens: adversarial domain, input and inertness.

**Verdict: PASS_WITH_NOTES.** I found no uncaught exception in default CPython. I found no zero exterior, invented tail, clipped or renormalized value, filled missing input or admitted inadmissible configuration. The notes below concern floating-point rounding and underflow inside the domain only.

**Execution statement:** nothing was imported or executed. The module was read as text. The only Python run was `python3 -I` on a helper that calls `ast.parse` on the file bytes. The helper sits in the reviewer scratch directory, outside this folder. No numerical cases were run.

## Pins (sha256 from bytes)

| Item | sha256 |
|---|---|
| 0403 task `FROM_CODEX/0403_2026-10-16_annular_source_kernel_reuse.md` | `eb68862b1651273bb973f2ed49f689226d2ee0643da751a01bc7cc65c4944673` |
| Reviewed `annular_bernstein_source_kernel_v001.py` | `2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e` |
| `PLANAR_DENSITY_CONSTRUCTION_REVIEW.md`, lines 1–47 only | `bbd9a2395f3e619093dddb9ba76e49f9243873c6fd4b4075904427bcd1f7344f` |
| AST helper `scratchpad/r0403/ast_review_0403.py` | `cd92d1ef3869c6efb0bbb1ac3f7ec9b98754c6e0b61eabb4c83eb916df6d0f64` |

## Findings

| # | Severity | Lines | Input | Behaviour |
|---|---|---|---|---|
| 1 | LOW | 224–226, 401–403 | Coefficients near the subnormal range (example: m = d_L = d_R = smallest positive subnormal), or a query offset q − s[i] tiny next to w so that t underflows to 0 | Each Bernstein term underflows, so Sigma or a bin's area comes back as `0.0`, or with no relative precision, while `ok` is True. The exact value is greater than 0. Nothing flags this. It fits the docstring's "rounding is reported as computed", but no line says that `ok` True does not certify relative precision or strict positivity at underflow scale. |
| 2 | LOW (plausible, static reasoning) | 398–403 | A subinterval much narrower than its bin, for example s_hi one or a few ulps above s_lo | The integral is the difference F(t_b) − F(t_a) of two independently rounded cubics. Two outcomes are possible with `ok` True: (a) `t_a == t_b` after the division even though `s_a < s_b`, giving `0.0`; (b) float evaluation of F is not monotone, giving a small negative per-bin value and total, of order eps·m·w·pi. Sigma's nonnegativity holds in float (all coefficients and weights are ≥ 0), but it does not carry over to computed narrow-interval integrals. |
| 3 | INFO | 171, 180, 183, 283, 361 | `-0.0` passed in s, m, d, s_query, s_lo or s_hi | `not x >= 0.0` admits a signed zero, which can then appear in `inputs`, `middle_controls` (b = −0.0 when m = −0.0), `sigma`, `s_from` or `area_integral`. The value is numerically zero, not negative, so the specification is not breached. |
| 4 | INFO | 224, 401, 402 | Subnormal edge width, in a process where a foreign extension has turned on flush-to-zero or denormals-are-zero | Division safety rests on IEEE gradual underflow: s[i+1] > s[i] implies w > 0. Under flush-to-zero, w could become 0 and raise an uncaught `ZeroDivisionError`. This cannot happen in default CPython. Hardening (optional): at admission, also require the computed width `s[j+1] - s[j] > 0.0`. |
| 5 | INFO | 115–135, 201–204 | numpy scalars; `Decimal`/`Fraction`; list or tuple subclasses; ints that are not exactly representable (example: 10**308); admissible m > (max float)/3 | All are rejected with `ok` False. That is stricter than the specification but fail-closed, and the docstring says so. When 3·m overflows, an admissible profile is refused at stage `coefficients`; it is never given a value. |
| 6 | INFO | 56–61, 91–98 | Stellar medians or nodal samples passed as `annular_means` | They are accepted. Applicability is declared only by the keyword name and the documentation, and the kernel cannot tell such values apart. That matches the specification's assignment of the declaration to the caller. |
| 7 | INFO | 232 vs 201 | Any profile | The integral uses (3m − d[i+1]), never the returned b, so the Sigma path and the integral path agree only to rounding. The upside is that F(1) evaluates to exactly m: a whole bin gives `pi*(w*m)` with no rounding through b, which preserves the specification's exact bin mean. |

## Traces confirmed clean (by reading)

- **Admission (lines 153–194):**
  - n = 0 or empty lists are rejected. Mismatched lengths are rejected before any indexing. Equal or decreasing edges, a negative s0 and negative m are rejected.
  - d is checked against [0, m[i]] for both adjacent bins with exact `>=` and `<=`, so an excess on either side of a shared edge is rejected. A zero-mean bin forces its controls to zero.
  - bool, None, NaN, ±inf, str, complex, numpy scalars and nested lists are all rejected by exact-type and `isfinite` checks.
  - An admitted int equals its float exactly, so the comparisons stay exact. The int repr runs only after `float()` has succeeded (at most 309 digits), so the string-conversion limit in newer Python versions cannot raise.
- **Queries (lines 281–287, 209–219):**
  - s0 → bin 0 with t = 0 → d[0] exactly. An internal edge s[k] → bin k with t = 0 → d[k]. In bin k−1 it would be t = w/w = 1 → d[k], so the bin rule cannot change the value even in floating point.
  - s[n] → bin n−1 with t = 1 → d[n].
  - One ulp outside either edge, or NaN, is rejected and the whole call fails. For in-domain queries, monotone rounding gives 0 ≤ t ≤ 1, so t cannot overflow.
- **Integral (lines 361–372):** reversed, partially outside and wholly outside bounds are all rejected; nothing is partially integrated. NaN is rejected. Equal bounds give `0.0` with `per_bin == []`, which is the true integral of a degenerate interval, not a manufactured value. A whole bin gives t_a = 0 and t_b = 1 exactly, and F(1) evaluates to exactly m.
- **Overflow:**
  - Non-finite b (line 202), Sigma (line 312), per-bin value (line 404) and an `fsum` overflow (lines 410–417) each give `ok` False with the value left None.
  - Edge widths cannot overflow because s ≥ 0.
  - Python float `*` and `+` return inf instead of raising, and these checks catch it.
- **Result keys:**
  - Each callable builds every key in `_new_result` plus its own fields before any return, and all 5 (Sigma) and 7 (integral) return paths return that same dict.
  - Value fields are filled only immediately before `ok = True`.
  - No module state is mutated; the module constants are strings.
- **Formula:** dF/dt = d(1−t)² + 2(3m − d − d′)t(1−t) + d′t², which matches the specified Sigma. b = 3m − d − d′. The integral is `pi*w*(F(t_b) − F(t_a))`. No 1e6, helium, distance or exterior-zero factor is inherited from section 1.

## AST check (python3 -I, `ast.parse` of file text; Python 3.9.6)

- Imports: only `import math`. It uses `math.fsum`, `math.isfinite` and `math.pi`.
- The top level holds only the docstring, the import, 4 string-constant assignments and 10 `def`s, so nothing runs at import.
- Absent: print, open, eval, exec, compile, `__import__`, globals, locals, getattr, setattr, os, sys, subprocess, threading, socket, class, lambda, `with`, `global`, `nonlocal`, yield, async, raise and assert.
- Dunder use: `type(...).__name__` on lines 121 and 144, which only builds failure-message text.
- Numeric constants are only 0, 1, 2, 0.0, 1.0, 2.0 and 3.0.
- Division sites:
  - lines 224, 401 and 402 divide by w > 0;
  - line 214 is an integer `// 2`.
- Both public callables are keyword-only with no positional arguments, no `*args` or `**kwargs` and no defaults. No function anywhere has a default.

## Scope of this review

- Of the review file I read section 1 only (lines 1–47) and never opened section 2.
- I opened no other historical file, force, oracle, fit or velocity material, PDF or source data.
- No source-data values are reproduced here.
