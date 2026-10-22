# Usage contract 0397, V002: scalar_metric_particular_solve

Module: `scalar_metric_particular_solve_v002.py` (sha256 ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf). It needs numpy only and does nothing at import.

This contract updates USAGE_CONTRACT_0397_V001.md for the four Codex 0398 corrections. Everything V001 states that is not changed below still holds: the call, units, sign convention, formula and scope.

## Unchanged from V001

- **Call.** `scalar_metric_particular_solve(*, k, z, G_EH, Pi_eff, F_eff, cond_tol)`. All six arguments are keyword-only and required, with no defaults.
- **Formula.** K0 = (4πG_EH)⁻¹ [[0, −k²], [−k², k² − 3z²]] with q = (n, ψ) in that order. A = K0 + Pi_eff, and the module solves **A q = −F_eff** with `numpy.linalg.solve`.
- **No alteration of A.** There is no symmetrization, Hermitization, real projection, clipping, regularization or pseudoinverse.
- **Units and signs.** Units are c = 1, in the caller's single consistent normalization. The sign convention is that of the frozen source (sha256 f5e28809…).

## Inputs (one change)

| Arg | Admitted |
|---|---|
| k | finite real > 0 |
| z | finite complex, Im z ≥ 0 |
| G_EH | finite real > 0 (not laboratory G) |
| Pi_eff | finite complex 2×2: a nested list/tuple or a **plain** `numpy.ndarray` of shape (2,2) |
| F_eff | finite complex length 2: a list/tuple or a **plain** `numpy.ndarray` of shape (2,) |
| cond_tol | finite real > 0; it only flags ill-conditioning |

**New in V002: ndarray subclasses are rejected.** Any ndarray subclass, such as `np.matrix`, is rejected for Pi_eff and F_eff with the failure `input <name>: ndarray subclass <type> is not admitted`. Convert to a plain ndarray before calling. Each element still goes through the scalar admission check: booleans, non-numeric values and non-finite values are rejected.

## Outputs (keys unchanged from V001)

- `ok`, `stage_reached`, `failures`, `flags`, `ill_conditioned`, `q_order` = ["n", "psi"], `q`, `K0`, `A`, `diagnostics`, `inputs`, `units`, `sign_convention`, `scope`.
- `diagnostics` has the keys `residual`, `residual_norm`, `F_norm`, `q_norm`, `relative_residual_to_F`, `relative_residual_to_A_norm_q_norm`, `singular_values`, `A_norm_2`, `cond_2` and `cond_tol`.
- Complex values are given as {real, imag}.

**What a filled field means.** Every number in the result is finite, so the result is strict-JSON serializable. A field is filled only after its values pass the finite check. Otherwise it stays None and a failure explains why.

**When ok is True:**
- `cond_2` is always a finite float, because s_min > 0.
- A relative residual is None **only** when its denominator (`F_norm`, or s_max·q_norm) is exactly 0. For example, F_eff = 0 gives q = 0, and both ratios are then None.
- `ill_conditioned` is True or False.

**When ok is False:** every filled field is failure evidence only, and nothing in the result is a valid solution. `ill_conditioned` stays None.

## Failure cases (ok = False, fail closed)

1. **Input not admitted** (stage `inputs`). This now includes ndarray subclasses.
2. **Non-finite K0 or A** (stage `assembly`).
   - The non-finite array is left None. A finite K0 is still reported.
   - The failure names the stage, the array and each entry, for example `assembly: A left None; non-finite A[1][1] real inf`. The kind is nan or inf.
3. **`numpy.linalg.solve` raises LinAlgError** (stage `solve`).
4. **Non-finite q** (stage `solve`). `q` is left None, and the failure names each entry and its kind.
5. **SVD does not converge** (stage `diagnostics`).
6. **New: s_min == 0** (stage `diagnostics`).
   - The smallest singular value is not strictly > 0, even though the LU solve returned. A is rejected as singular.
   - cond_2 is not computed, and `diagnostics` is None.
   - The q that was already reported is failure evidence, not a solution.
7. **New: an unrepresentable diagnostic** (stage `diagnostics`).
   - This applies when any of the following is non-finite: residual_norm, F_norm, q_norm, s_max, s_min, s_max·q_norm, cond_2, or a non-None relative residual.
   - The failure reads `diagnostics: unrepresentable <name> (<kind>), …`, and `diagnostics` is None.
   - So an overflow can never appear as a zero relative residual or as a finite cond_2.

In every case: no value is replaced by zero, and there is no pseudoinverse, regularization or physical cutoff. No tolerance has been added; cond_tol is the only one.

## Ill-conditioning: needs a caller decision

When cond_2 is finite and cond_2 > cond_tol, the module sets `ill_conditioned = True`, adds a flag and leaves `ok` unchanged. The module does not decide whether such a result is usable.

**Before any use of a result with `ill_conditioned = True`**, the caller must make an explicit, recorded decision about it. This applies especially when cond_2 approaches 1/eps (about 4.5e15).

cond_tol is the caller's flagging threshold. It is not a physical acceptance rule.

## Warnings

Warnings are not suppressed. The root caller treats them as fatal, so a numpy overflow warning raised inside the module ends the call before these checks run.

The checks are still needed for Python-float arithmetic, which overflows to inf without a warning: s_max·q_norm, s_max/s_min and the relative residuals. They also apply whenever warnings are not escalated.

## Scope exclusions (unchanged)

- Particular solution only, on the translation-stationary scalar branch. Excluded:
  - homogeneous, boundary and initial-data modes, and k = 0 modes;
  - general nonstationary convolution;
  - retained-block elimination. The caller supplies Pi_eff and F_eff already eliminated on the admitted causal quotient.
- Pi_eff is a matched residual ACTION Hessian, not a raw susceptibility. F_eff = F_b + ell_eff, in the reviewed sign convention.
- G_EH is not equated to laboratory G.
- There is no galaxy data and there are no fit parameters, and no 43 velocities are computed.
