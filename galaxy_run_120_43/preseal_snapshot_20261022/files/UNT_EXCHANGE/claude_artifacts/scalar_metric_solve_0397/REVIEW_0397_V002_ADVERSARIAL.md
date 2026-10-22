# REVIEW 0397 V002 (adversarial): input validation, diagnostic overflow and inertness

**Reviewer:** Claude helper, acting as a distinct checker. I am not the author.
**Lens:** adversarial input validation, diagnostic overflow and inertness.
**Date:** 2026-10-15.
**Target:** `scalar_metric_particular_solve_v002.py`, with `USAGE_CONTRACT_0397_V002.md` and `AUTHOR_DELTA_0397_V002.md`.

## Verdict: PASS_WITH_NOTES

All four Codex 0398 items are **CLOSED** as specified. On every admission path in the brief, each input is either admitted correctly or rejected with a recorded failure. The only uncaught exceptions come from hostile user-defined subclasses, which are outside 0398's "no new broad input framework" (N4). On every overflow path in the brief, the call ends in an explicit failure, or it raises under root's fatal-warning policy. No such path ends with ok True and a finite-from-overflow or zero diagnostic. The module is inert under AST inspection.

I found two adjacent paths that are new. On both, an admitted, finite input yields an **exactly zero K0 packaged with ok True** (N1, N2):
- **N1:** a huge G_EH makes 4πG_EH overflow to inf, so the prefactor 1/inf becomes 0.0.
- **N2:** k² or k²/(4πG_EH) underflows to 0.0.

Both need extreme magnitudes in the caller's normalization. They falsify two sentences: "In every case: no value is replaced by zero" in the contract, and "Overflow is fully guarded" in the delta. N2 is silent under any default warning policy. All findings are LOW or INFO, and none blocks the four 0398 items.

## Hashes (sha256 from bytes, recomputed with `shasum -a 256`)

| File | sha256 | Status |
|---|---|---|
| FROM_CODEX/0397_2026-10-15_scalar_metric_particular_solver.md | cf985f80a391d0d0ebb16935186a7a0d0e9ad9dc820823aabb20df0ba5179845 | read |
| FROM_CODEX/0398_2026-10-15_scalar_solver_review_corrections.md | cf798ab64a7ca91733e28dc29ea5491ce9974f5edc4a5f406ff304cbf1d861a5 | matches the brief |
| scalar_metric_particular_solve_v002.py | ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf | matches the author |
| USAGE_CONTRACT_0397_V002.md | e8f8f4fbb75b718e7df09d593d7893c70b1342cea1c59e03fb1df985bf1852b9 | matches the author |
| AUTHOR_DELTA_0397_V002.md | d5a66103777af47e3185ce5f77bc7b17e87ad9f4f13aad44037e7acb9bbdecb8 | matches the author |
| REVIEW_0397_V001.md | 8da4c9c2f2a5b0379602645aa8a54571d26e8573d0fbc576d8035216a7147f68 | matches the brief |
| scalar_metric_particular_solve_v001.py | c7dbbba8ccb5bff025cf874410d769e96b7757b214d77d7f7f2fbf8c420dc0db | unchanged since V001 |
| USAGE_CONTRACT_0397_V001.md | e8ffbf92fd6b0a68568929f07552bf3715318f4c659b151236236f681bc2afbf | unchanged since V001 |
| AUTHOR_NOTES_0397_V001.md | d51f0ad9070a310888aa741e7092d02e46cb897d2882bed74763350b6158cc60 | unchanged since V001 |
| frozen source EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_PROPOSED_V001.md | f5e28809a8ac24212d1d30bf6be92ab0d064407ae139f72f5146334c86308dd7 | matches 0397 |

**Delta check.** I recomputed `diff -u v001 v002` and its body is identical to the diff embedded in AUTHOR_DELTA. The assembly lines are byte-identical to V001 (the K0 formula and the prefactor at L284–L293). N1 and N2 are therefore also present in V001, and REVIEW_0397_V001 did not record them.

## Findings

| ID | Severity | Line | Input | Behaviour |
|---|---|---|---|---|
| N1 | LOW | L285, L295–L304 | G_EH finite with G_EH > DBL_MAX/(4π) ≈ 1.43e307, and k, z finite | **Mechanism:** `4.0*np.pi*np.float64(G_in)` overflows to inf, so `prefactor = 1.0/inf = 0.0`. K0 comes out as exactly [[0, −0], [−0, 0]]. It is finite, so the finite check (L295) passes. A = Pi_eff, the solve proceeds, and ok can be True with K0 reported as zero. The true K0, e.g. k²/(4πG_EH) ≈ 8e-10 for G_EH = 1e308 and k = 1e150, is representable.<br>**Under root's fatal-warning policy:** numpy's scalar-multiply overflow RuntimeWarning is raised out of the call, so this ends fatally with no result dict.<br>**With warnings not escalated:** this is an overflow-to-zero result packaged as valid. That contradicts contract L60 and L74 ("They also apply whenever warnings are not escalated") and the delta's "Overflow is fully guarded". |
| N2 | LOW | L284–L285, L295 | k > 0 admitted, but k² < ~2.5e-324 (k ≲ 1.6e-162), or k²/(4πG_EH) < ~2.5e-324 (k ≲ 5.6e-162 at G_EH = 1; k ≲ 5.6e-12 at G_EH = 1e300, e.g. k = 1e-12) | **Mechanism:** the product underflows to 0.0. numpy's default errstate has `under='ignore'` (numpy 2.0.2 `_ufunc_config.py` L134), so no warning is issued under any default or warnings-as-errors policy. The off-diagonals of K0 become exactly 0. K0 is then [[0, 0], [0, −3z²/(4πG_EH)]], or all zeros when z = 0. That is the k = 0 operator, which the scope excludes, and it is packaged with ok True.<br>**Precision loss:** when prefactor·k² is subnormal (< 2.2e-308), the result also loses precision silently.<br>**Suggested exact fix (no tolerance):** det K0 = −k⁴/(4πG_EH)² ≠ 0 for every admitted k and G_EH, so a zero or non-finite `prefactor`, or `K0[0,1] == 0`, is a provable arithmetic failure. Recording it as `assembly: …` closes both N1 and N2. |
| N3 | LOW (contract) | contract L33–L38, L60 | Normalized inputs whose components are around 1e-150 or smaller | **Mechanism:** the sum-of-squares norms underflow (L122).<br>- A nonzero residual can give residual_norm = 0.0 and `relative_residual_to_F = 0.0` with ok True. This is a spuriously perfect relative residual from underflow.<br>- A nonzero F or q can give F_norm or q_norm = 0.0, and then a ratio of None.<br>**Coverage:** AUTHOR_DELTA open point 1 records this and recommends the range [1e-154, 1e154]. 0398 excluded broader scale coverage, so the code is acceptable as it stands.<br>**Contract gap:** the usage contract, which is what root reads, has no underflow statement and no recommended range (grep for "underflow", "1e-154" and "1e154" finds nothing). It also asserts that a ratio is None "only when its denominator … is exactly 0" and that "no value is replaced by zero". |
| N4 | INFO | L22–L26, L44–L48, L93–L104 | Hostile user-defined subclasses of int, float, complex, list or tuple | **Exceptions not caught:**<br>- A `__float__` or `__complex__` that raises anything other than OverflowError, ValueError or TypeError propagates. So does a DeprecationWarning, when the method returns a subclass and warnings are escalated.<br>- A list or tuple subclass whose `__iter__`, used in the shape check at L93–L94, disagrees with `__getitem__`, used for the elements at L104, can raise an uncaught TypeError or IndexError.<br>**Scope:** these cases are outside 0398's "no new broad input framework". Plain built-ins and numpy types cannot trigger them. |
| N5 | INFO (PLAUSIBLE, not executed) | L17, L38 | A `np.timedelta64` scalar, or a plain `m8` ndarray, for any argument | **Admission:** at runtime numpy defines timedelta64 as a subclass of `np.signedinteger`. The installed stub instead declares `class timedelta64(generic)`, so I could not confirm the hierarchy by reading the installed files, and it is not confirmed by execution. If timedelta64 is a subclass, it passes the `np.integer` type gate.<br>**Conversion:** the units whose `item()` is an int (generic, Y, M, ns, ps, fs, as) convert, so the value is admitted with its unit silently dropped. Other units, and NaT, raise TypeError, which is caught and recorded.<br>**Impact:** no uncaught exception. |
| N6 | INFO | L309–L313, contract L72 | A finite but huge A whose LU overflows internally | **Error mapping:** numpy's solve runs under `errstate(invalid='call', over='ignore')` (`_linalg.py` L408). An internal NaN therefore becomes LinAlgError("Singular matrix"), and the module records "A is singular to working precision". It is an explicit failure, but the stated cause may be wrong.<br>**Warning behaviour:** overflow inside solve and svd never produces a warning (`over='ignore'`, L408 and L1808). Contract L72 ("a numpy overflow warning raised inside the module ends the call") does not apply to them. They are still caught by the q check (L315) and the s_max check (L337–L346). |

## Admission trace (static, per argument)

### k, G_EH and cond_tol (`_real_input` L12–L30, then the > 0 checks at L262, L266 and L268)

| Input | Path | Class |
|---|---|---|
| Python bool, np.bool_ | L14 | rejected, recorded |
| int | L17 admits, then L23 float(); 10**400 raises OverflowError, caught at L24 | admitted correctly, or rejected and recorded |
| float or numpy int/uint/float scalar (longdouble is float64 on this arm64 host) | L17, L23 | admitted correctly |
| nan, ±inf (Python or numpy) | L27 | rejected, recorded |
| 0, −0.0, negative | L262, L266, L268 (`not x > 0.0`) | rejected, recorded |
| complex, np.complex128 (even with zero imaginary part) | L17 | rejected, recorded |
| str, None, list, 0-d ndarray, np.ma.masked, Decimal, Fraction | L17 | rejected, recorded |
| timedelta64 | L17 (see N5) | PLAUSIBLE unit drop |
| hostile float/int subclass | L23 (see N4) | UNCAUGHT (INFO) |

### z (`_complex_input` L33–L52, then L264)

| Input | Path | Class |
|---|---|---|
| bool, np.bool_ | L35 | rejected, recorded |
| int, float, complex, numpy numeric scalar | L39, L45 | admitted correctly |
| nan or inf in either part; huge int | L49; L46 | rejected, recorded |
| str, None, 0-d ndarray | L39 | rejected, recorded |
| Im z < 0 | L264 | rejected, recorded |
| Im z == 0, including −0.0 | L264 (`-0.0 >= 0.0` is True) | admitted as the boundary that 0397 allows; K0 is unaffected apart from signed zeros |

### Pi_eff (L81–L109) and F_eff (L55–L78)

| Input | Path | Class |
|---|---|---|
| correct nested list/tuple of admitted scalars | L92 or L66, then per-element `_complex_input` | admitted correctly |
| wrong length, ragged, rows that are not list/tuple (ndarray row, str row) | L93–L97, L67–L69 | rejected, recorded |
| plain ndarray of wrong shape: (), (2,1), (1,2), (2,2,1), (3,) | L89, L63 | rejected, recorded |
| plain ndarray with int dtype | elements are np.integer | admitted correctly |
| plain ndarray with bool dtype | elements are np.bool_, rejected at L35 | rejected, recorded |
| plain ndarray with object dtype | per element: list, ndarray, None, Decimal rejected; huge int caught | rejected, recorded |
| plain ndarray with str, bytes, void (structured) or datetime64 dtype | element type check at L39 | rejected, recorded |
| np.matrix, np.ma.MaskedArray, memmap, recarray, user ndarray subclass | L58, L84 (`type(value) is not np.ndarray`) | rejected, recorded |
| ndarray nested in a list, as a row or as an element | L94, or L39 per element | rejected, recorded |
| dict, range, generator, str, None | L70, L98 | rejected, recorded |
| nan or inf element | L49 | rejected, recorded |

**Call binding.** A missing argument, a positional call or an extra keyword raises TypeError at call binding, before any result dict exists. This follows from the required keyword-only design; there are no defaults.

## Numerical extremes (static trace; Python floats overflow to inf without a warning; numpy scalars and ufuncs warn on overflow by default)

| Input | Path | End state |
|---|---|---|
| huge k (k² overflows) | L284, then K0 inf at L295 | warning raised (fatal), or `assembly: K0 left None; non-finite …` and A left None. ok False. |
| tiny G_EH < ~4.4e-310 (prefactor overflows) | L285; K0[0][0] = inf·0.0 = nan | warning raised, or assembly failure naming `K0[0][0] real nan` and the inf entries |
| prefactor·k² overflows | L286–L292 | assembly failure |
| huge z (z² overflows) | L289 | assembly failure |
| K0 finite, K0 + Pi_eff overflows | L293, L296 | K0 reported, A left None, assembly failure |
| **huge G_EH > 1.43e307** | L285 gives prefactor 0 | **N1**: warning raised, or K0 = 0 with ok True |
| **k² or k²/(4πG_EH) below the subnormal range** | L284–L285 | **N2**: K0 off-diagonals 0 with ok True, and no warning |
| huge Pi_eff or F_eff making q overflow | solve ignores overflow (L408 in `_linalg`); L315 | `solve: q left None; non-finite …`, or LinAlgError recorded (N6) |
| q finite with \|q_i\| > ~1.3e154 | L328 | warning raised, or `unrepresentable q_norm (inf)` |
| \|F_i\| > ~1.3e154 | L327 | warning raised, or `unrepresentable F_norm (inf)` |
| s_max > DBL_MAX | svd ignores overflow (L1808); L337–L346 | `unrepresentable s_max (inf)` |
| s_min > 0 tiny, so s_max/s_min overflows | L358, a Python division giving inf; L361–L367 | `unrepresentable cond_2 (inf)`. ill_conditioned stays None and ok is False; cond_2 is never reported as finite. |
| s_min == 0 (or −0.0) while LU returned | L347–L353 | `diagnostics: A is singular …`. ok False, and no division (no ZeroDivisionError). |
| s_min nan | L337–L346 (`singular` is False because of the isfinite guard) | `unrepresentable s_min (nan)` |
| s_max·q_norm overflows | L336, a Python multiplication giving inf; L344 | `unrepresentable s_max*q_norm (inf)` |
| tiny F_norm > 0, so residual_norm/F_norm overflows | L359; L364 | `unrepresentable relative_residual_to_F (inf)` |
| tiny s_max·q_norm > 0, so the ratio overflows | L360; L365 | `unrepresentable relative_residual_to_A_norm_q_norm (inf)` |
| finite cond_2 > cond_tol | L387–L394 | flag only, ok True, ill_conditioned True; matches 0398 item 1 |
| F_eff == 0 exactly | L359–L360 | q = 0 and both ratios None; matches the contract |
| underflowed norms | L122 | **N3**: residual_norm, F_norm or q_norm is 0.0 (ok True) |

**No finite-from-overflow diagnostic.** I found no path that reports one.
- Every diagnostic is either a LAPACK value, which numpy reports as inf rather than a finite wrong value, or a Python float operation on finite operands, which gives the correctly rounded value or inf.
- Any inf·0 in assembly (L288, or 0·inf at L289 when N1 meets a non-finite bracket) gives nan, which is caught.
- There is no x/inf in the diagnostics. The only 1/inf in the module is at L285 (N1).

## Result-dict consistency

- The main function has 7 returns: L279 (inputs), L304 (assembly), L313 (solve, LinAlgError), L318 (solve, non-finite q), L333 (svd), L374 (diagnostics) and L398 (complete).
- All 7 return the dict built by `_new_result()` (14 keys).
- The function only assigns existing keys (AST list: stage_reached, inputs, K0, A, q, diagnostics, ill_conditioned, ok) and never adds or deletes a key.
- `diagnostics` is filled at exactly one place, L375, with a fixed set of 10 keys, and only after `if failures: return`.
- `ok = True` is set only at L396, after `ill_conditioned` is set to a Python bool.
- On the diagnostics-stage failures, q is still populated. The contract documents it as failure evidence.
- Every populated number is a finite Python float, so the result is strict-JSON serializable, subject to N1, N2 and N3 for meaning (not for finiteness).

## Per-0398 closure

| Item | Status | Evidence |
|---|---|---|
| 1. Reject s_min == 0 even when LU returned; keep finite near-singular cases as flags; no pinv, regularization or cutoff; no new tolerance | **CLOSED** | L347–L353: an exact `not s_min > 0.0` test on a finite s_min gives a failure at stage diagnostics with ok False. L357–L358: cond_2 is computed only when s_min > 0. L387–L394: the flag leaves ok unchanged. No pinv or lstsq in the AST. |
| 2. Fix or reject ndarray subclasses; scalar admission still applies; no broad framework | **CLOSED** | L58–L62 and L84–L88 reject any subclass with a recorded failure. Elements still go through `_complex_input`. No subclass can reach `value[i][j]`: rows must be list/tuple, and elements are type-checked. |
| 3. Guard s_max·q_norm and the relative residuals; no spuriously zero residual from overflow; non-finite diagnostic means an explicit failure; cond_2 never finite from overflow; ratio None only for an exactly zero denominator; keys and contract consistent | **CLOSED** (overflow) | All 9 named quantities are checked (L337–L346, L361–L367) and lead to failure at stage diagnostics with diagnostics None (L368–L374). `!= 0.0` is used at L359–L360. Keys are unchanged. Underflow is outside the item (N3, contract wording). |
| 4. Finite admission of K0 and A after assembly and of q after solve, before packaging; name stage, array, indices and kind; never replace with zero | **CLOSED** (as specified) | L295–L304 and L315–L319 use `_nonfinite_entries`, which reports index, part and nan/inf. The array is left None and the code never substitutes zero. N1 and N2 are adjacent arithmetic paths (1/inf and underflow) that produce a finite zero K0 upstream of this check. They are recorded separately. |

## Inertness (AST over the file text only; `python3 -I` on a scratchpad script outside the artifact directory)

**Module structure and imports.**
- Top level: `import numpy as np` (L9) plus 11 FunctionDefs. There are no other statements: no constants, no executable code and no `if __name__` block.
- Imports: numpy only.

**Forbidden constructs.**
- MatMult nodes: 0.
- No call or name is any of: dot, matmul, pinv, lstsq, inv, tensordot, inner, vdot, conj, transpose, clip, nan_to_num, errstate, seterr, filterwarnings, simplefilter, catch_warnings, warnings, open, print, os, sys, subprocess, threading, multiprocessing, `__import__`, eval, exec, compile, getattr, setattr or globals.
- No Lambda, Global, Nonlocal, async, With, Yield, ClassDef, Raise or Assert nodes.

**Solver calls.**
- `np.linalg.solve` ×1 (L310).
- `np.einsum` ×1 (L325, `optimize=False`).
- `np.linalg.svd` ×1 (L330, `compute_uv=False`).
- Exception handlers: only `(OverflowError, ValueError, TypeError)` (L22, L44) and `np.linalg.LinAlgError` (L309, L329).

**Public callable.**
- One: `scalar_metric_particular_solve` (L187).
- Its arguments are k, z, G_EH, Pi_eff, F_eff and cond_tol, all keyword-only.
- It has no positional arguments, no defaults, no `*args`/`**kwargs` and no decorators.
- No helper has defaults either.

**Uses of `.real`/`.imag`:** L49, L113, L122, L130, L264 and L265. They appear only in admission, output pairs, norms and the finite check; A and q are never projected.

## Statements

- **Role:** distinct checker, not author.
- **Nothing was imported or executed.** Neither `scalar_metric_particular_solve_v001.py` nor `_v002.py` was imported or executed, and no UNT, Codex or producer script was run.
- **Python runs.**
  - The AST script (`ast.parse`/`ast.unparse` over the file text) under `python3 -I`, located in my scratchpad.
  - Two lookups under `python3 -I`, used to locate numpy's installed source text: a `sys.version`/`sys.path` print, and an `importlib.util.find_spec('numpy')` lookup. The lookup does not import numpy, and under -I it found nothing.
- **Static reading only.** numpy 2.0.2 behaviour (errstate defaults, and the linalg errstate in solve and svd) was read from the installed `.py` and `.pyi` text, not executed.
- **Other tools.** Everything else was shasum, diff, grep, sed and cat.
- **Write rules.** No file was modified, moved or deleted. Nothing was written under Universal Network Theory. No network was used. This file was created exclusively (noclobber).
