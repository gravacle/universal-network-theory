"""Inert pure-numpy kinematic density map (dispatch 0447, Claude3, module version c3v001).

Root contract: UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/
KINEMATIC_DENSITY_COMPARISON_CHOICE_V001.json,
sha256 9e4c070e88bf431cac9e001958016f9ca022f8cdef2c0c4f039fb7cd1128e14d.
Physical status: not_assessed.  This is a numerical representation comparison
only; it adds no force, state, source, geometry or acceptance.

Equation (exactly the contract's):
    Gkin = -rho[:,None]*divU - rho_R[:,None]*U_R - rho_z[:,None]*U_z

Physical reading (no additional content): delta_rho = -div(rho xi)
= -rho div(xi) - xi.grad(rho) for xi = U y, evaluated pointwise at the supplied
points.  The background rho(R, z) is axisymmetric, so grad(rho) has no phi
component.  divU is root's full cylindrical divergence
partial_R U_R + U_R/R + i*m*U_phi/R + partial_z U_z, so the azimuthal term
enters once, through divU.  No phi term is added a second time, no derivative
is taken here, and no projection, inverse, quadrature or source change is made.
rho_R and rho_z are root's supplied EOS/lagged derivatives, used as given.

Interface:
    kinematic_density_map(*, rho, rho_R, rho_z, U_R, U_z, divU) -> numpy.ndarray
* Keyword-only and required; a missing, positional or unknown argument raises
  Python's native TypeError.
* rho, rho_R, rho_z: exactly 1-D with shape (npoints,), npoints >= 1;
  integer or floating dtype (bool, complex, object and string are rejected);
  finite; returned as float64; rho > 0 everywhere.
* U_R, U_z, divU: exactly 2-D with identical shape (npoints, nfree),
  nfree >= 1 (U_R fixes nfree); integer, floating or complex dtype (bool,
  object and string are rejected); finite; cast losslessly to complex128.
  Real-dtype maps such as root's helicity U_R and U_z are accepted.
* Returns a new complex128 array of shape (npoints, nfree).  An invalid input
  raises ValueError naming the parameter; a non-finite result (overflow)
  raises ValueError with no clipping or repair.  Inputs are never modified.
  The function is pure: no I/O, printing or global state.
"""

import numpy as np

__all__ = ["kinematic_density_map", "CONTRACT_SHA256", "MODULE_VERSION"]

CONTRACT_SHA256 = "9e4c070e88bf431cac9e001958016f9ca022f8cdef2c0c4f039fb7cd1128e14d"
MODULE_VERSION = "c3v001"


def _array(name, value, kinds, kind_text, shape, dtype):
    """Validate dtype kind, exact shape (None = any size >= 1) and finiteness; cast without mutating."""
    try:
        a = np.asarray(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"parameter '{name}' cannot be converted to a numpy array ({type(exc).__name__})"
        ) from exc
    if a.dtype.kind not in kinds:
        raise ValueError(
            f"parameter '{name}' must have {kind_text} dtype; got dtype {a.dtype}"
        )
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


def _vector(name, value, npoints):
    return _array(name, value, ("i", "u", "f"),
                  "an integer or floating (not bool, complex, object or string)",
                  (npoints,), np.float64)


def _map(name, value, shape):
    return _array(name, value, ("i", "u", "f", "c"),
                  "an integer, floating or complex (not bool, object or string)",
                  shape, np.complex128)


def kinematic_density_map(*, rho, rho_R, rho_z, U_R, U_z, divU):
    """Return Gkin = -rho[:,None]*divU - rho_R[:,None]*U_R - rho_z[:,None]*U_z (complex128)."""
    rho = _vector("rho", rho, None)
    if not (rho > 0.0).all():
        raise ValueError("parameter 'rho' must be strictly positive everywhere")
    npoints = rho.shape[0]
    rho_R = _vector("rho_R", rho_R, npoints)
    rho_z = _vector("rho_z", rho_z, npoints)
    U_R = _map("U_R", U_R, (npoints, None))
    nfree = U_R.shape[1]
    U_z = _map("U_z", U_z, (npoints, nfree))
    divU = _map("divU", divU, (npoints, nfree))

    # Floating-point errors are not raised or printed here; the explicit
    # finiteness check below fails closed independently of np.seterr.
    with np.errstate(all="ignore"):
        Gkin = -rho[:, None] * divU   # -rho div(xi)
        Gkin -= rho_R[:, None] * U_R  # -xi_R d(rho)/dR
        Gkin -= rho_z[:, None] * U_z  # -xi_z d(rho)/dz   (no phi gradient of rho)
    if not np.isfinite(Gkin).all():
        raise ValueError(
            "returned array 'Gkin' is not finite (overflow or invalid operation); "
            "failing closed without clipping or repair"
        )
    return Gkin
