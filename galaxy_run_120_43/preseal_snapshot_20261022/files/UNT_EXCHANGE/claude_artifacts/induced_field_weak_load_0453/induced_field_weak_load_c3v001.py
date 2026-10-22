"""Inert pure-numpy induced-field weak Euler load (dispatch 0453, Claude3, module version c3v001).

    delta_b = -(U_R^H (w*rho*grad_R) + U_phi^H (w*rho*grad_phi) + U_z^H (w*rho*grad_z)) / normalization_scale

This is exactly the forcing slice of the frozen 0439 kernel
(claude_artifacts/weak_euler_0439/weak_euler_assembly_c3v001.py,
sha256 8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da, b lines 308-322),
with (f_R, f_phi, f_z) = (grad[:,0], grad[:,1], grad[:,2]).  The operation sequence is
identical, so for matching inputs delta_b equals that b bitwise.  Physical status:
not_assessed.

Conventions (root-supplied; nothing here re-derives them):
* grad is (n,3) complex: the exp(+i m phi) Fourier coefficient of the induced
  cylindrical gradient, columns [R, phi, z], taken by root after FFT/16 over all
  16 angles.  grad[:,1] already is (1/R) d/dphi deltaPhi: no extra 1/R division.
* w = volume_weights = R dR dz WITHOUT 2 pi.  No factor 2, extra azimuthal weight,
  sign reversal, FFT, angle selection or interpolation is applied here.
* m labels the retained mode (1..6); it does not enter the projection.

Scope: assembly of one load increment only; no solve, density/y/background/gas
update or accumulation.  In a fixed F2 linearization the total right-hand side is
the original b0 plus this increment, not a sum over earlier increments (root owns
the iteration).  The density -> real field -> positive-mode chain is generally
real-linear in complex coefficients (both signs / complex conjugates), so this
complex-linear projection does not certify complex-linearity of the coupled
operator.

Interface:
    induced_field_weak_load(*, m, U_R, U_phi, U_z, rho, volume_weights, grad,
                            normalization_scale) -> dict
* All keyword-only and required; a missing, positional or unknown argument
  raises Python's native TypeError.
* m: type(m) is int with 1 <= m <= 6.
* U_R, U_phi, U_z: exactly 2-D, identical shape (n, k), n, k >= 1; integer,
  floating or complex dtype (bool, object, string rejected); finite; cast
  losslessly to complex128 (root's real U_R, U_z helicity maps are accepted).
* rho, volume_weights: exactly 1-D (n,); integer or floating dtype (complex,
  bool, object, string rejected); finite; strictly positive.
* grad: exactly (n, 3); integer, floating or complex dtype; finite; complex128.
* normalization_scale: numbers.Real (not bool), finite, > 0.
* Invalid input raises ValueError naming the parameter; a non-finite operand or
  result raises ValueError (fail closed, no clipping).  Inputs are never modified.
* Returns a new dict: 'delta_b' (k,) complex128; component loads 'load_R',
  'load_phi', 'load_z' (k,) complex128, each -U_c^H(w*rho*grad_c)/normalization_scale
  (diagnostic; their sum equals delta_b up to rounding order); 'm', 'n', 'k',
  'normalization_scale', 'physical_status' ('not_assessed'), 'grad_columns'
  (('R','phi','z')), 'reference_0439_sha256', 'module_version'.
"""

import math
import numbers

import numpy as np

__all__ = ["induced_field_weak_load", "MODULE_VERSION", "REFERENCE_0439_SHA256", "GRAD_COLUMNS"]

MODULE_VERSION = "c3v001"
REFERENCE_0439_SHA256 = "8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da"
GRAD_COLUMNS = ("R", "phi", "z")


def _array(name, value, kinds, kind_text, shape, dtype):
    """Validate dtype kind, exact shape (None = any size >= 1) and finiteness; cast without mutating."""
    try:
        a = np.asarray(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"parameter '{name}' cannot be converted to a numpy array ({type(exc).__name__})"
        ) from exc
    if a.dtype.kind not in kinds:
        raise ValueError(f"parameter '{name}' must have {kind_text} dtype; got dtype {a.dtype}")
    if a.ndim != len(shape) or any(
        size < 1 if want is None else size != want for size, want in zip(a.shape, shape)
    ):
        raise ValueError(
            f"parameter '{name}' must be exactly {len(shape)}-D with shape {shape} "
            f"(None = any size >= 1); got shape {a.shape}"
        )
    a = a.astype(dtype, copy=False)  # no copy if already of dtype; never written
    if not np.isfinite(a).all():
        raise ValueError(f"parameter '{name}' must be finite everywhere")
    return a


def _positive_vector(name, value, n):
    a = _array(name, value, ("i", "u", "f"),
               "an integer or floating (not bool, complex, object or string)", (n,), np.float64)
    if not (a > 0.0).all():
        raise ValueError(f"parameter '{name}' must be strictly positive everywhere")
    return a


def _complex_map(name, value, shape):
    return _array(name, value, ("i", "u", "f", "c"),
                  "an integer, floating or complex (not bool, object or string)", shape, np.complex128)


def _require_finite(name, array, description):
    if not np.isfinite(array).all():
        raise ValueError(
            f"returned array '{name}' would not be finite: {description} is not finite "
            "(overflow); failing closed without clipping or repair"
        )


def induced_field_weak_load(*, m, U_R, U_phi, U_z, rho, volume_weights, grad, normalization_scale):
    """Return delta_b = -(sum_c U_c^H (w*rho*grad_c)) / normalization_scale and component loads."""
    if type(m) is not int or not 1 <= m <= 6:
        raise ValueError(
            "parameter 'm' must be a Python int with 1 <= m <= 6 (bool, float and numpy "
            f"integers are rejected); got {m!r} of type {type(m).__name__}"
        )
    U_R = _complex_map("U_R", U_R, (None, None))
    n, k = U_R.shape
    U_phi = _complex_map("U_phi", U_phi, (n, k))
    U_z = _complex_map("U_z", U_z, (n, k))
    rho = _positive_vector("rho", rho, n)
    volume_weights = _positive_vector("volume_weights", volume_weights, n)
    grad = _complex_map("grad", grad, (n, 3))
    if isinstance(normalization_scale, bool) or not isinstance(normalization_scale, numbers.Real):
        raise ValueError("parameter 'normalization_scale' must be a real number (numbers.Real, not bool)")
    try:
        normalization_scale = float(normalization_scale)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(
            f"parameter 'normalization_scale' cannot be converted to float ({type(exc).__name__})"
        ) from exc
    if not (math.isfinite(normalization_scale) and normalization_scale > 0.0):
        raise ValueError(
            f"parameter 'normalization_scale' must be finite and > 0; got {normalization_scale!r}"
        )

    w = volume_weights  # R dR dz without 2 pi, used exactly once
    with np.errstate(all="ignore"):
        # Identical sequence to frozen 0439 lines 313-322 with f_c = grad[:, c].
        w_rho = w * rho
        w_rho_f_R = w_rho * grad[:, 0]    # grad_R
        w_rho_f_phi = w_rho * grad[:, 1]  # grad_phi = (1/R) d/dphi deltaPhi, no extra 1/R
        w_rho_f_z = w_rho * grad[:, 2]    # grad_z
        _require_finite("delta_b", w_rho_f_R, "w*rho*grad_R")
        _require_finite("delta_b", w_rho_f_phi, "w*rho*grad_phi")
        _require_finite("delta_b", w_rho_f_z, "w*rho*grad_z")
        # True conjugate transposes (Galerkin test maps), as in 0439.
        t_R = U_R.conj().T @ w_rho_f_R
        t_phi = U_phi.conj().T @ w_rho_f_phi
        t_z = U_z.conj().T @ w_rho_f_z
        delta_b = -t_R
        delta_b -= t_phi
        delta_b -= t_z
        delta_b /= normalization_scale    # only the load is scaled
        load_R = -t_R / normalization_scale
        load_phi = -t_phi / normalization_scale
        load_z = -t_z / normalization_scale
    for name, array in (("delta_b", delta_b), ("load_R", load_R), ("load_phi", load_phi), ("load_z", load_z)):
        if not np.isfinite(array).all():
            raise ValueError(
                f"returned array '{name}' is not finite (overflow or invalid operation); "
                "failing closed without clipping or repair"
            )
    return {
        "delta_b": delta_b,
        "load_R": load_R,
        "load_phi": load_phi,
        "load_z": load_z,
        "m": m,
        "n": n,
        "k": k,
        "normalization_scale": normalization_scale,
        "physical_status": "not_assessed",
        "grad_columns": GRAD_COLUMNS,
        "reference_0439_sha256": REFERENCE_0439_SHA256,
        "module_version": MODULE_VERSION,
    }
