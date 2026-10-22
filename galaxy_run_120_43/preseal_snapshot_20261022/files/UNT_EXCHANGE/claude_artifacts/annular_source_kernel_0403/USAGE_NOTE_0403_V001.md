# 0403 usage note: annular Bernstein source kernel, v001

Role: author, Claude helper. Written statically. The module was never imported or executed. The only check run was `python3 -I` `ast.parse` on its text. A distinct helper still has to do the static review.

## Pins (sha256 from bytes)

- Task: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0403_2026-10-16_annular_source_kernel_reuse.md`, `eb68862b1651273bb973f2ed49f689226d2ee0643da751a01bc7cc65c4944673`
- Section 1 only (lines 1–47) of `.../halogas_source_candidate/PLANAR_DENSITY_CONSTRUCTION_REVIEW.md`, `bbd9a2395f3e619093dddb9ba76e49f9243873c6fd4b4075904427bcd1f7344f`
- 0363 note, section 3 item 1 (ring averaging) and the file list only: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/leroy_conventions_0363/LEROY_CONVENTIONS_ANSWER_0363_V001.md`, `a81477be7980e2b7ec0cb7949d77a6d1b709ef8f356ed25e6e9d63118180f958`
- Style reference, read as text and not imported: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/scalar_metric_solve_0397/scalar_metric_particular_solve_v002.py`, `ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf`
- Module: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py`, `2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e`

## Step 1: reuse search. Result: no directly reusable callable

Method:
- Listed names under `halogas_source_candidate` with `ls -R`. It has no subdirectories.
- Searched each `.py` file's text for imports, `def`s and the patterns Bernstein, `1-t`, control, primitive, endpoint, exterior, `1e6` and helium.
- Section 1 names no file or callable. It mentions only a "proposed cubic primitive".
- The 0363 ring-averaging item names no callable. Its file list names only PDF locator and reader scripts, which are not candidates and were not opened.

| Candidate (in `halogas_source_candidate/`) | sha256 | Verdict |
|---|---|---|
| `extract_planar_source.py` | `1d6f87baf468360e9b75657582aa4cbda9fb880c2f425a39fb158708511d3970` | Not reusable. It is a FITS-pixel annular extraction worker that uses numpy, argparse and file I/O, with built-in distance and column-to-mass conversions and a helium multiplier. It produces profile records upstream of the kernel. It has no Bernstein evaluation, no control logic and no primitive. |
| `fits_source_audit.py` | `6ae74a15c173cfd3ec3a6daad67ee18045a7d7bfe4bf3ffb2eb2a5e7a733fd59` | Not reusable. It is a FITS header and retained-signal audit that uses numpy and has hard-coded conversions. It has no kernel. Its name contains the lowercase format name "fits", which passes the case-sensitive "FIT" rule. It was inspected only through matching grep lines. |
| `planar_saved_audit.py` | `007c48bacb9b85ee5e14ac5280527a4b87dd8adb655fb36e47ebec7a51e59db2` | Not reusable. It is a saved-results arithmetic audit (sealed-JSON checks with a tolerance). It has no kernel. |

v001 inherits none of the following from the section-1 construction or from these files:
- the fixed zero last control;
- the exterior-zero join;
- the `1e6` factor;
- helium;
- distance or column conversion;
- any wrapper, force law or calibrated value.

## Callables (keyword-only, all required, no defaults)

The module imports `math` only. Import it yourself; it has no CLI.

```
annular_bernstein_sigma(*, s_edges, annular_means, boundary_controls, s_query)
annular_bernstein_area_integral(*, s_edges, annular_means, boundary_controls, s_lo, s_hi)
```

Inputs:
- `s_edges` = s[0..n], strictly increasing and ≥ 0.
- `annular_means` = m[0..n-1], ≥ 0, with n ≥ 1.
- `boundary_controls` = d[0..n], one per shared edge. For each bin i, d[i] and d[i+1] must lie in [0, m[i]]. Comparisons are exact.
- Containers must be a built-in list or tuple.
- Values must be built-in int or float, finite, and an int must be exactly representable as a float.
- bool, None, str, NaN, inf, numpy scalars and wrong lengths are rejected. Nothing is filled, clipped or renormalized.

Return keys:
- **Common:** `ok`, `stage_reached` (`inputs` → `coefficients` → `evaluation` or `integration` → `complete`), `failures`, `inputs` (the admitted floats plus `n_bins`), `middle_controls` (b), `units`, `domain`, `scope`.
- **`annular_bernstein_sigma` adds:** `bin_rule`, `bin_index`, `sigma`. The last two are lists with one entry per query, and they are None unless `ok`.
- **`annular_bernstein_area_integral` adds:** `per_bin` (a list of `{bin, s_from, s_to, area_integral}`) and `area_integral`. Both are None unless `ok`.

## Domain and rejection

- The domain is only the closed interval [s[0], s[n]].
- One query outside it rejects the whole `sigma` call.
- `s_lo < s[0]`, `s_hi > s[n]` or `s_lo > s_hi` rejects the integral call.
- Nothing outside the edges is returned as zero, and no tail is added. Nonzero first and last controls are supported.
- `s_lo == s_hi` gives 0.
- A non-finite b, Sigma, bin contribution or total is a failure and returns no value.

Bin rule: a query at an internal edge s[k] is evaluated in bin k, and s[n] is evaluated in bin n−1. At t = 0, bin k gives exactly d[k], so by C0 the value does not depend on this rule.

## Units

Units are the caller's, used consistently:
- Sigma has the units of m and d.
- s has squared-radius units.
- π∫Σ ds has the units of m times the units of s.

No `1e6`, helium, distance, mass-to-light, inclination or other conversion is applied. Conversions stay in the root source layer.

## Applicability

The kernel is for declared area means of disjoint annuli with explicit edges in s = R².

The 0363 note records gas quantities as ring means and stars as ring medians, in tilted rings whose neighbours are correlated. Ring values become admissible here only after root declares them disjoint-annulus area means with s edges. Stellar medians and nodal or ring-centre samples are not silently admitted.

The kernel makes no claim of monotonicity, C1 smoothness, unique reconstruction, deconvolution, physical completeness or observational error. It makes no choice about geometry, vertical shape, unsampled or outer material, or calibration.

## Identities by inspection

With w_i = s[i+1] − s[i], t = (s − s[i])/w_i, b_i = 3m_i − d_i − d_{i+1}, and Σ = d_i(1−t)² + 2b_i t(1−t) + d_{i+1}t²:

1. **Bin mean.** Each quadratic Bernstein basis function integrates to 1/3 over [0, 1]. So (1/w_i)∫Σ ds = (d_i + b_i + d_{i+1})/3 = m_i.
2. **C0.** Σ(s_i) = d_i from both sides, because the control is shared and not duplicated.
3. **Nonnegativity.** d_i, d_{i+1} ∈ [0, m_i] gives b_i ∈ [m_i, 3m_i]. All coefficients are therefore ≥ 0, and 0 ≤ Σ ≤ 3m_i in the bin.
4. **Zero-mean bin.** If m_i = 0, admissibility forces d_i = d_{i+1} = 0, and then b_i = 0.
5. **Antiderivative.** The code uses F_i(t) = d_i t(1−t)² + (3m_i − d_{i+1}) t²(1−t) + m_i t³.
   - Its derivative dF_i/dt equals the Bernstein quadratic above.
   - The coefficient 3m_i − d_{i+1} equals d_i + b_i.
   - F_i(0) = 0 and F_i(1) = m_i.
   - The integral over [s_a, s_b] ⊆ bin i is π w_i (F_i(t_b) − F_i(t_a)).
   - A whole bin gives π w_i m_i, the exact area mean.
   - Contributions are summed with `math.fsum`. Rounding is reported as computed.

## AST check

Run with `python3 -I`, `ast.parse` on the module text. The checker is in the author's scratch directory, outside this folder.

- The only import is `math`, using `fsum`, `isfinite` and `pi`.
- The top level holds only the docstring, the import, 4 string-constant assignments and 10 defs.
- Both public functions are keyword-only and have no defaults.
- There is no print, open, eval, exec, compile, `__import__`, threading, os, sys, subprocess, class, lambda, `with` or global.
- The checker's dunder-attribute scan reported only `type(value).__name__`, which is used inside failure-message strings.
