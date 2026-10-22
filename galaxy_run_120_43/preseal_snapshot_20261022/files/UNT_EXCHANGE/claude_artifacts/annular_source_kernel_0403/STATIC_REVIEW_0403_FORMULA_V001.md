# 0403 static review: formula, units, scope (v001)

Role: distinct reviewer, not author. Lens: FORMULA, UNITS, SCOPE.
Nothing was imported or executed. The module and all historical workers were read as text only. The one program run was a `python3 -I` `ast.parse` and AST walk of the module text, using a helper in the reviewer's scratch dir: `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0403f/ast_scan.py`. There were no numerical cases, no tests and no network.

## Verdict: PASS_WITH_NOTES

The formula, Jacobian, pi factor, domain handling, units and scope text match the 0403 root specification and section 1 of the source. No finding blocks use. The notes below are wording and informational only.

## Pins (sha256 recomputed from bytes; all match the author report)

- 0403 task `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0403_2026-10-16_annular_source_kernel_reuse.md`: `eb68862b1651273bb973f2ed49f689226d2ee0643da751a01bc7cc65c4944673`
- `PLANAR_DENSITY_CONSTRUCTION_REVIEW.md` (reviewer read lines 1-47 only): `bbd9a2395f3e619093dddb9ba76e49f9243873c6fd4b4075904427bcd1f7344f`
- Module `annular_bernstein_source_kernel_v001.py`: `2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e`
- `USAGE_NOTE_0403_V001.md`: `dcd8e0c75d99d2d6487194dfe4ac1de77c4080e9270a80892ca83812ecf9a97d`
- 0363 note `LEROY_CONVENTIONS_ANSWER_0363_V001.md` (hashed, not read by reviewer): `a81477be7980e2b7ec0cb7949d77a6d1b709ef8f356ed25e6e9d63118180f958`
- 0397 style file `scalar_metric_particular_solve_v002.py` (hashed, not read by reviewer): `ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf`
- `extract_planar_source.py`: `1d6f87baf468360e9b75657582aa4cbda9fb880c2f425a39fb158708511d3970`
- `fits_source_audit.py`: `6ae74a15c173cfd3ec3a6daad67ee18045a7d7bfe4bf3ffb2eb2a5e7a733fd59`
- `planar_saved_audit.py`: `007c48bacb9b85ee5e14ac5280527a4b87dd8adb655fb36e47ebec7a51e59db2`

## Formula checks (hand algebra)

**F1. t, b and Sigma: PASS.**

| Quantity | Code (line) | Specification |
|---|---|---|
| t | L224: `t = (q - s[i]) / (s[i + 1] - s[i])` | t = (s-s[i])/(s[i+1]-s[i]) |
| b | L201: `3.0 * m[i] - d[i] - d[i + 1]` | b[i] = 3m[i] - d[i] - d[i+1] |
| Sigma | L225-226: `u = 1-t`; `d[i]*(u*u) + 2.0*(b[i]*(t*u)) + d[i+1]*(t*t)` | Sigma = d[i](1-t)^2 + 2b[i]t(1-t) + d[i+1]t^2 |

Section 1 of the source agrees:
- L16: "b=3m-d_L-d_R lies in [m,3m]".
- L18: "quadratic Bernstein weights `(1-t)^2, 2t(1-t), t^2`".
- L12 places the bin in "`s=R^2`". The source does not write t explicitly; 0403 defines it, and the code follows 0403.

**F2. Bin area mean: PASS.**
- Over [0,1], (1-t)^2, 2t(1-t) and t^2 each integrate to 1/3. The 2t(1-t) case is 2(1/2 - 1/3) = 1/3.
- So the mean over t is (d_i + b_i + d_{i+1})/3 = (d_i + 3m_i - d_i - d_{i+1} + d_{i+1})/3 = m_i.
- dA = 2 pi R dR = pi ds, so the annulus area is pi w_i and the annulus integral is pi w_i m_i. The area mean is exactly m_i.
- This matches source L26-27 ("`(d_L+b+d_R)/3=m`", "`R dR=ds/2`").

**F3. C0: PASS.**
- Sigma(t=0) = d_i and Sigma(t=1) = d_{i+1}.
- d has length n+1 (L167) and is indexed d[i], d[i+1] by bin i. Both bins adjacent to an internal edge therefore read the same d[k], which is source L20-21 ("same value d_i from either side").
- In floating point, t=0 gives u=1.0, and with b finite (L202) the result is exactly d[i]. So the internal-edge bin rule (L105-110, `_bin_of` L209-219) does not change the value.

**F4. Nonnegativity: PASS.**
- d_i, d_{i+1} in [0, m_i] gives b_i in [3m_i - 2m_i, 3m_i] = [m_i, 3m_i].
- All three coefficients and all three weights are >= 0. The weights sum to 1, so 0 <= Sigma <= 3m_i.
- The admission checks are exact comparisons with no tolerance: L171 (s[0]), L174 (strictly increasing), L180 (m), L183 (d >= 0) and L186-187 (d[j] <= m[i] for j in {i, i+1}).

**F5. Antiderivative: PASS.**
- The code's antiderivative (L232) is F(t) = d_i t u^2 + c t^2 u + m_i t^3, with u = 1-t and c = 3m_i - d_{i+1}.
- Differentiating by hand gives F' = d_i[u^2 - 2tu] + c[2tu - t^2] + 3m_i t^2 = d_i u^2 + 2(c - d_i)tu + (3m_i - c)t^2.
- Here c - d_i = 3m_i - d_i - d_{i+1} = b_i and 3m_i - c = d_{i+1}. So F' = Sigma.
- Also c = d_i + b_i, F(0) = 0 and F(1) = m_i.
- Jacobian: ds = w_i dt, with w_i = s[i+1]-s[i] (L400). So pi * integral_{s_a}^{s_b} Sigma ds = pi * w_i * (F(t_b) - F(t_a)), which is L403.
- The overlap limits (L396-399) and the domain bounds (L361-372) make the overlapped bins tile [s_lo, s_hi] exactly. s_lo == s_hi gives fsum([]) = 0.
- For a whole bin, t_b = w/w = 1.0 exactly and t_a = 0.0, so F(1) evaluates to exactly m_i. The bin gives pi*(w_i*m_i) up to the two final products, as L337 says.

**F6. Zero-mean bin: PASS.** If m_i = 0, then L183 and L187 force d_i = d_{i+1} = 0, so b_i = 0 (L201) and Sigma is identically 0 in that bin. Nothing is interpolated into it, which is source L21-22.

## Units

**U1: PASS.**
- The module text has the numeric constants {0, 0.0, 1, 1.0, 2, 2.0, 3.0} and nothing else.
- Its only import is `math`, and only fsum, isfinite and pi are used.
- "1e6", "helium", "distance" and "mass-to-light" appear only in negating prose (L53, L87-88).
- Source L28 "`pi*1e6*Delta_s*m`" is reduced to pi*w_i*m_i with no 1e6.
- The result is in caller units: (units of m) x (units of s). This matches 0403 and the usage note L70-75.

## Domain and scope

**S1. Domain: PASS.**
- The domain is the closed [s[0], s[n]]. Any query or limit outside it rejects the call (L283, L361-370), with no value, no zero and no tail.
- Nonzero first and last controls are admitted, since only the [0, m] bounds are checked.
- Source L14 "explicit last endpoint zero" and L30-31 "exterior zero" are not inherited.

**S2. Missing and invalid values: PASS.** None, bool, str, NaN, inf, non-list/tuple containers and wrong lengths are rejected (L113-150, L161-170). No fill, clip, renormalization or default is applied anywhere.

**S3. Defaults and keyword-only signatures: PASS.** By AST walk, both public callables take keyword-only arguments only, with no defaults, *args or **kwargs. No private helper has a default either. There are no global, class, lambda or with nodes.

**S4. Claims: PASS.** The docstring (L28-38), `_SCOPE` (L91-98) and the usage note (L79-83) claim only C0, nonnegativity and the exact bin mean. They explicitly disclaim monotonicity, C1, unique reconstruction, deconvolution, physical completeness and observational error. The note that the 3m bound is not a precision statement mirrors source L35-36.

**S5. Applicability: PASS.** Stellar medians and nodal or ring-centre samples are explicitly not admitted by default (L56-61, usage note L79-81). See N2.

## Step-1 candidates

**C1: PASS.** The reviewer used only `ls` names, `def`/import lines and grep pattern counts:
- `extract_planar_source.py` imports numpy, argparse, os and resource and defines read_primary, geometry, accumulate, profiles and run. It has zero matches for Bernstein, primitive, control, endpoint, exterior and 1e6, and two for helium. It is an extraction worker, not a kernel.
- `planar_saved_audit.py` defines only `sealed` and `close` and has zero pattern matches.
- `fits_source_audit.py` defines `read_primary` and `main` and has zero Bernstein, primitive or control matches.

The "not reusable" verdicts are sound. The module contains no wrapper, force law, calibrated value, helium, 1e6 or exterior convention.

**C2: forbidden reads, PASS with N3.** The files the author reports reading or grepping have names that contain no forbidden token under case-sensitive matching. The 0363 file list's PDF scripts were not opened.

## Notes (non-blocking)

- **N1 (wording).** In module docstring L25-26, "the integral of Sigma over [s_a, s_b] ... is w_i * (F_i(t_b) - F_i(t_a))" is integral Sigma ds, without pi. The same sentence continues "and a whole bin gives pi * w_i * m[i]", which is the area integral, with pi. Each statement is correct for its own referent, but the sentence shifts subject mid-way. The code (L403) and the usage note (L97) are consistent. If revised, this could read "pi * w_i * (F_i(t_b) - F_i(t_a))" for the area integral.
- **N2 (informational).** Applicability rests on the caller's declaration, through the argument name `annular_means` and the scope text. The kernel cannot detect medians or nodal samples, and 0403 asks for no declaration field (no new schema). The usage note L81 states the 0363 gas-mean/stellar-median convention; the reviewer did not read the 0363 note.
- **N3 (custody, informational).** `fits_source_audit.py` contains lowercase "fits", the file-format name. The rule lists "FIT" in uppercase only, while it lists both cases for other tokens, so case-sensitive reading admits the file. Both author and reviewer read it only through grep lines or counts. Root may wish to confirm that reading.
- **N4 (informational).** `bin_index` at an internal edge reports the right-hand bin by documented convention (L105-110). It is output metadata only and is not a delegated parameter. Sigma is unaffected (F3).
