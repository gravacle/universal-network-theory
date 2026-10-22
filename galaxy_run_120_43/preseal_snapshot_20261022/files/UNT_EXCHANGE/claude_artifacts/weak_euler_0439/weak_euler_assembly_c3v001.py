"""Inert pure-numpy assembly of the supplied 32q8 weak Euler operator (dispatch 0439).

Module version c3v001 (Claude3 lane, sole author of this kernel).
Root contract: UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/
ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json,
sha256 5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe.
Physical status: not_assessed.  The module makes no physical claim; root owns
every model choice, scientific launch and acceptance.

Scope
-----
* Stationary perturbations proportional to exp(+i m phi), m = 1..6, of gas
  rotating with angular velocity Omega(R, z).  Every m uses the same
  contraction: no per-mode branch and no m = 0 (axisymmetric) forcing.
* The pressure surface term is dropped: the same continuum weak-domain
  pressure-surface / zero-flux assumption that root adopted.  This routine does
  not certify boundary traces.
* Geometry, the hard-constraint nullspace (already inside the supplied maps),
  signs and quadrature are root-supplied, as are the density map G, the
  divergence map divU and the forcing gradients f.  Nothing is reconstructed,
  re-differentiated or reset here.
* Assembly only: no solve, inverse, pseudoinverse, ridge, clipping, spectrum
  repair, solution, tolerance or acceptance.  Only A and b are divided by
  normalization_scale; E, PM, VR, VP, VZ are returned exactly unscaled.

Pure function: inputs are never modified; no I/O, printing, logging, global
state or randomness.  numpy only (no numpy.linalg, no diagonal matrices, no
npoints x npoints array).  Interface: INTERFACE_0439_V001.md.
"""

import math
import numbers

import numpy as np

__all__ = ["assemble_weak_euler", "CONTRACT_SHA256", "MODULE_VERSION"]

CONTRACT_SHA256 = "5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe"
MODULE_VERSION = "c3v001"

_REAL_KINDS = ("i", "u", "f")  # signed integer, unsigned integer, floating
_MAP_KINDS = ("i", "u", "f", "c")  # the same, or complex


def _as_array(name, value):
    """np.asarray(value); a conversion failure becomes ValueError naming the parameter."""
    try:
        return np.asarray(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"parameter '{name}' cannot be converted to a numpy array ({type(exc).__name__})"
        ) from exc


def _shape_matches(actual, expected):
    """True if actual equals expected, where an expected None means any size >= 1."""
    return len(actual) == len(expected) and all(
        size >= 1 if want is None else size == want for size, want in zip(actual, expected)
    )


def _real_array(name, value, shape, *, positive=False):
    """Required real array: integer or floating dtype, finite; returned as float64.

    Complex dtype is rejected so that no imaginary part is ever silently discarded.
    """
    a = _as_array(name, value)
    if a.dtype.kind not in _REAL_KINDS:
        raise ValueError(
            f"parameter '{name}' must have an integer or floating dtype "
            f"(bool, complex, object and string are rejected); got dtype {a.dtype}"
        )
    if not _shape_matches(a.shape, shape):
        raise ValueError(
            f"parameter '{name}' must be exactly {len(shape)}-D with shape {shape} "
            f"(None = any size >= 1); got shape {a.shape}"
        )
    a = a.astype(np.float64, copy=False)
    if not np.isfinite(a).all():
        raise ValueError(f"parameter '{name}' must be finite everywhere")
    if positive and not (a > 0.0).all():
        raise ValueError(f"parameter '{name}' must be strictly positive everywhere")
    return a


def _complex_array(name, value, shape):
    """Required integer, floating or complex array, finite; returned as complex128.

    Real-dtype maps are accepted because root's helicity-map module returns U_R
    and U_z as real float arrays; a real value is an exact complex value.
    """
    a = _as_array(name, value)
    if a.dtype.kind not in _MAP_KINDS:
        raise ValueError(
            f"parameter '{name}' must have an integer, floating or complex dtype "
            f"(bool, object and string are rejected); got dtype {a.dtype}"
        )
    if not _shape_matches(a.shape, shape):
        raise ValueError(
            f"parameter '{name}' must be exactly {len(shape)}-D with shape {shape} "
            f"(None = any size >= 1); got shape {a.shape}"
        )
    a = a.astype(np.complex128, copy=False)
    if not np.isfinite(a).all():
        raise ValueError(f"parameter '{name}' must be finite everywhere")
    return a


def _real_scalar(name, value):
    """Required real scalar: numbers.Real but not bool; returned as float."""
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(
            f"parameter '{name}' must be a real number (numbers.Real, not bool); "
            f"got type {type(value).__name__}"
        )
    try:
        return float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(
            f"parameter '{name}' cannot be converted to float ({type(exc).__name__})"
        ) from exc


def _require_finite_result(name, array):
    """Fail closed: every returned array must be finite (no clipping or repair)."""
    if not np.isfinite(array).all():
        raise ValueError(
            f"returned array '{name}' is not finite (overflow or invalid operation); "
            "failing closed without clipping or repair"
        )


def _require_finite_operand(result_name, operand, description):
    """Fail closed before a BLAS product.

    A BLAS may skip multiplications by an exact zero, so a non-finite entry of an
    operand need not reach the product; the operand itself is therefore checked.
    """
    if not np.isfinite(operand).all():
        raise ValueError(
            f"returned array '{result_name}' would not be finite: {description} is not "
            "finite (overflow); failing closed without clipping or repair"
        )


def assemble_weak_euler(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z,
                        volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z,
                        m, gamma, normalization_scale, provenance):
    """Assemble the 0439 weak Euler matrix and forcing; return A, b (scaled) and maps.

    Every argument is a required keyword-only argument without a default; Python
    raises TypeError for a missing, positional or unknown argument.  Every
    validation failure raises ValueError whose message names the offending
    parameter.  Shapes, dtype rules, conventions and return keys are listed in
    INTERFACE_0439_V001.md.  Returns a new dict; no input is modified.
    """
    # ------------------------------------------------------------------ inputs
    # Validated in signature order.  R fixes npoints.  U_R is validated first
    # among the maps and fixes nfree, so a map whose shape differs from U_R is
    # the one named in the error.  An array already of the target dtype is used
    # without a copy and is only read, never written.
    R = _real_array("R", R, (None,), positive=True)
    npoints = R.shape[0]
    rho = _real_array("rho", rho, (npoints,), positive=True)
    P = _real_array("P", P, (npoints,), positive=True)
    K_R = _real_array("K_R", K_R, (npoints,))
    K_z = _real_array("K_z", K_z, (npoints,))
    P_R = _real_array("P_R", P_R, (npoints,))
    P_z = _real_array("P_z", P_z, (npoints,))
    Omega = _real_array("Omega", Omega, (npoints,))
    Omega_R = _real_array("Omega_R", Omega_R, (npoints,))
    Omega_z = _real_array("Omega_z", Omega_z, (npoints,))
    volume_weights = _real_array("volume_weights", volume_weights, (npoints,), positive=True)
    U_R = _complex_array("U_R", U_R, (npoints, None))
    nfree = U_R.shape[1]
    U_phi = _complex_array("U_phi", U_phi, (npoints, nfree))
    U_z = _complex_array("U_z", U_z, (npoints, nfree))
    divU = _complex_array("divU", divU, (npoints, nfree))
    G = _complex_array("G", G, (npoints, nfree))
    f_R = _complex_array("f_R", f_R, (npoints,))
    f_phi = _complex_array("f_phi", f_phi, (npoints,))
    f_z = _complex_array("f_z", f_z, (npoints,))
    if type(m) is not int or not 1 <= m <= 6:
        raise ValueError(
            "parameter 'm' must be a Python int with 1 <= m <= 6 (bool, float and numpy "
            f"integers are rejected); got {m!r} of type {type(m).__name__}"
        )
    gamma = _real_scalar("gamma", gamma)
    if gamma != 5.0 / 3.0:
        raise ValueError(
            f"parameter 'gamma' must equal 5/3 exactly (float(gamma) == 5.0/3.0); got {gamma!r}"
        )
    normalization_scale = _real_scalar("normalization_scale", normalization_scale)
    if not (math.isfinite(normalization_scale) and normalization_scale > 0.0):
        raise ValueError(
            f"parameter 'normalization_scale' must be finite and > 0; got {normalization_scale!r}"
        )
    if not isinstance(provenance, str) or not provenance.strip():
        raise ValueError(
            "parameter 'provenance' must be a str containing at least one non-whitespace character"
        )

    w = volume_weights  # contract shorthand: w enters each integral exactly once

    # Physical reading (comments only; adds nothing to the contract): the
    # displacement is xi = U y, and the same maps U serve as trial and test
    # functions (Galerkin).  Every field is proportional to exp(+i m phi), so
    # d/dphi -> +i m, and the background flow is v0 = R*Omega(R, z) phi_hat.
    #
    # Inside this block floating-point errors are neither raised nor printed.
    # Instead every returned array and every product operand is checked
    # explicitly, and the function fails closed with ValueError.  This keeps the
    # behaviour independent of the caller's np.seterr state, which np.errstate
    # restores on exit.
    with np.errstate(all="ignore"):
        i_m_Omega = 1j * m * Omega  # i*m*Omega: v0.grad acting on exp(+i m phi)

        # ----------------------------------------- physical maps (unscaled)
        # E = -K_R[:,None]*U_R - K_z[:,None]*U_z
        # Eulerian perturbation of K (P = K rho**gamma) carried by xi: -xi.grad K.
        E = -K_R[:, None] * U_R
        E -= K_z[:, None] * U_z
        _require_finite_result("E", E)

        # PM = (gamma*P/rho)[:,None]*G + (rho**gamma)[:,None]*E
        # Eulerian pressure perturbation.  G (conservative weak density map,
        # -div(rho xi), from the 0438 projection) is used exactly as supplied.
        PM = (gamma * P / rho)[:, None] * G
        PM += (rho**gamma)[:, None] * E
        _require_finite_result("PM", PM)

        # Eulerian velocity perturbation dv = (v0.grad)xi - (xi.grad)v0:
        # VR = i*m*Omega[:,None]*U_R
        VR = i_m_Omega[:, None] * U_R
        _require_finite_result("VR", VR)

        # VP = -(R*Omega_R)[:,None]*U_R + i*m*Omega[:,None]*U_phi - (R*Omega_z)[:,None]*U_z
        VP = -(R * Omega_R)[:, None] * U_R
        VP += i_m_Omega[:, None] * U_phi
        VP -= (R * Omega_z)[:, None] * U_z
        _require_finite_result("VP", VP)

        # VZ = i*m*Omega[:,None]*U_z
        VZ = i_m_Omega[:, None] * U_z
        _require_finite_result("VZ", VZ)

        # ------------------------------------------------ weak matrix A
        # Contract A (X^H = conjugate transpose; diag(d) = diagonal weights):
        #   A = + U_R^H   diag(w*rho)      AR    (term 1)
        #       + U_phi^H diag(w*rho)      AP    (term 2)
        #       + U_z^H   diag(w*rho)      AZ    (term 3)
        #       - divU^H  diag(w)          PM    (term 4)
        #       - U_R^H   diag(w*P_R/rho)  G     (term 5)
        #       - U_z^H   diag(w*P_z/rho)  G     (term 6)
        # Physical reading: weak form of rho*a = -grad(dP) + (drho/rho) grad(P)
        # - rho*grad(dPhi) with the pressure surface term dropped; the arrays
        # AR, AP, AZ are (v0.grad)dv + (dv.grad)v0 in cylindrical components.
        #
        # Grouped by test map, using X^H diag(d) Y = X^H (d[:,None]*Y) and
        # distributivity, so each group is ONE (npoints x nfree)^H @
        # (npoints x nfree) product, four in total:
        #   group R   = U_R^H   [(w*rho)[:,None]*AR - (w*P_R/rho)[:,None]*G]  terms 1 + 5
        #   group phi = U_phi^H [(w*rho)[:,None]*AP]                           term  2
        #   group z   = U_z^H   [(w*rho)[:,None]*AZ - (w*P_z/rho)[:,None]*G]  terms 3 + 6
        #   group div = divU^H  [w[:,None]*PM], subtracted                     term  4
        # Each integrand Y is built in private scratch, contracted with a true
        # conjugate transpose (X.conj().T is a transient conjugated copy; no input
        # is conjugated in place), and released with del before the next one.
        w_rho = w * rho

        # group R (terms 1 + 5), with AR = i*m*Omega[:,None]*VR - 2*Omega[:,None]*VP
        Y = i_m_Omega[:, None] * VR
        Y -= 2 * Omega[:, None] * VP  # Y = AR
        Y *= w_rho[:, None]  # (w*rho)[:,None]*AR
        Y -= (w * P_R / rho)[:, None] * G  # - (w*P_R/rho)[:,None]*G
        _require_finite_operand("A", Y, "the U_R test-map integrand")
        A = U_R.conj().T @ Y
        del Y

        # group phi (term 2), with
        # AP = i*m*Omega[:,None]*VP + (2*Omega + R*Omega_R)[:,None]*VR + (R*Omega_z)[:,None]*VZ
        Y = i_m_Omega[:, None] * VP
        Y += (2 * Omega + R * Omega_R)[:, None] * VR
        Y += (R * Omega_z)[:, None] * VZ  # Y = AP
        Y *= w_rho[:, None]  # (w*rho)[:,None]*AP
        _require_finite_operand("A", Y, "the U_phi test-map integrand")
        A += U_phi.conj().T @ Y
        del Y

        # group z (terms 3 + 6), with AZ = i*m*Omega[:,None]*VZ
        Y = i_m_Omega[:, None] * VZ  # Y = AZ
        Y *= w_rho[:, None]  # (w*rho)[:,None]*AZ
        Y -= (w * P_z / rho)[:, None] * G  # - (w*P_z/rho)[:,None]*G
        _require_finite_operand("A", Y, "the U_z test-map integrand")
        A += U_z.conj().T @ Y
        del Y

        # group div (term 4): - divU^H diag(w) PM
        Y = w[:, None] * PM
        _require_finite_operand("A", Y, "the divU test-map integrand")
        A -= divU.conj().T @ Y
        del Y

        A /= normalization_scale  # returned A = contract A / normalization_scale
        _require_finite_result("A", A)

        # --------------------------------------------------- weak forcing b
        # b = -U_R^H (w*rho*f_R) - U_phi^H (w*rho*f_phi) - U_z^H (w*rho*f_z)
        # Physical reading: minus the test-map projection of rho*grad(dPhi); f is
        # the modal grad(dPhi) supplied once by root (native angular forcing plus
        # separately declared lagged feedback).  No m = 0 forcing is added.
        # Matrix-vector products with true conjugate transposes.
        w_rho_f_R = w_rho * f_R
        w_rho_f_phi = w_rho * f_phi
        w_rho_f_z = w_rho * f_z
        _require_finite_operand("b", w_rho_f_R, "w*rho*f_R")
        _require_finite_operand("b", w_rho_f_phi, "w*rho*f_phi")
        _require_finite_operand("b", w_rho_f_z, "w*rho*f_z")
        b = -(U_R.conj().T @ w_rho_f_R)
        b -= U_phi.conj().T @ w_rho_f_phi
        b -= U_z.conj().T @ w_rho_f_z
        b /= normalization_scale  # returned b = contract b / normalization_scale
        _require_finite_result("b", b)

    return {
        "A": A,
        "b": b,
        "E": E,
        "PM": PM,
        "VR": VR,
        "VP": VP,
        "VZ": VZ,
        "m": m,
        "gamma": gamma,
        "normalization_scale": normalization_scale,
        "provenance": provenance,
        "npoints": npoints,
        "nfree": nfree,
        "physical_status": "not_assessed",
        "scaled_outputs": ("A", "b"),
        "unscaled_outputs": ("E", "PM", "VR", "VP", "VZ"),
        "contract_sha256": CONTRACT_SHA256,
        "module_version": MODULE_VERSION,
    }
