# Usage contract 0397, V001: scalar_metric_particular_solve

Module: `scalar_metric_particular_solve_v001.py`. It needs numpy only and does nothing at import.

Call: `scalar_metric_particular_solve(*, k, z, G_EH, Pi_eff, F_eff, cond_tol)`. All six arguments are keyword-only and required. There are no defaults and no built-in physical values.

## Inputs

| Arg | Admitted | Meaning |
|---|---|---|
| k | finite real > 0 | spatial wavenumber; k = 0 is excluded |
| z | finite complex, Im z ≥ 0 | time frequency z = ω + i0 (upper half plane or its real boundary) |
| G_EH | finite real > 0 | the matched EH coupling of the adopted action. It is **not** laboratory G. |
| Pi_eff | finite complex 2×2 (nested list/tuple or shape-(2,2) array) | the matched residual retained **action Hessian**, already eliminated. It is not a raw susceptibility. |
| F_eff | finite complex length 2 (list/tuple or shape-(2,) array) | the complete action source covector F_b + ell_eff, in the reviewed sign convention |
| cond_tol | finite real > 0 | the caller's threshold for **flagging** ill-conditioning. It is not a physical acceptance rule. |

Booleans, other shapes and non-finite values are rejected. Nothing is defaulted, coerced or substituted.

## Units

Use c = 1 and one consistent normalization chosen by the caller:
- k and z share one inverse-length unit.
- K0 has the units of k²/G_EH, and Pi_eff and F_eff must match that normalization of the action.
- q = (n, ψ) are dimensionless metric potentials.

No unit conversion is done.

## Sign convention (frozen source, coefficient_method EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_PROPOSED_V001, sha256 f5e28809…)

- Signature (−+++). The metric is ds² = −(1+2n)dt² + (1−2ψ)dx². The Fourier convention is exp(−iωt + ik·x).
- K0 = (4πG_EH)⁻¹ [[0, −k²], [−k², k² − 3z²]], with q = (n, ψ) in that order.
- A = K0 + Pi_eff, and the equation is **A q = −F_eff**. So q_particular = −A⁻¹F_eff = G·F_eff, where G = −A⁻¹.
- The ordinary source part is F_b = (−ε, −T_ii), and F_eff = F_b + ell_eff.

## Outputs (plain dict)

- `ok`, `stage_reached`, `failures`.
- `flags` and `ill_conditioned`, which is set when cond₂ > cond_tol. This flag does **not** change `ok`.
- `q_order` = ["n", "psi"] and `q` as [{real, imag}, {real, imag}].
- `K0` and `A` as 2×2 nested {real, imag}. A is used exactly as assembled: never symmetrized, Hermitized, made real or clipped.
- `diagnostics`:
  - residual A q + F_eff, and its 2-norm;
  - |F_eff| and |q|;
  - relative residual to |F_eff| and to ‖A‖₂|q|, each None if its denominator is 0;
  - the singular values of A, ‖A‖₂, and cond₂ = s_max/s_min (inf if s_min = 0).
- `inputs` (echoed), `units`, `sign_convention`, `scope`.

**Failure cases** (ok = False, fail closed):
- input not admitted;
- non-finite K0 or A;
- `numpy.linalg.solve` raises LinAlgError (exactly singular A);
- non-finite q;
- the SVD does not converge;
- non-finite diagnostics.

There is no pseudoinverse and no regularization. Warnings are not suppressed; the root caller treats them as fatal.

## Scope exclusions

This is the particular solution only, on the translation-stationary scalar branch. It excludes:
- homogeneous, boundary and initial-data modes, and k = 0 modes;
- general nonstationary convolution;
- retained-block elimination. The caller supplies Pi_eff and F_eff already eliminated on the admitted causal quotient.

It takes no galaxy data and no fit parameters, and it computes no 43 velocities. G_EH is not equated to laboratory G.
