"""W1 independent loop reference for the 0453 induced-field weak load (review 0454).

Helper W1 inside the Claude4 independent review lane (dispatch 0454).  Review
artifact only: synthetic use, no project data, no physical claim.

Operation (0453 text; stated to be identical to the forcing slice b of the
frozen 0439 kernel weak_euler_assembly_c3v001.py, lines 307-323):

    delta_b = -( U_R^H (w*rho*g_R) + U_phi^H (w*rho*g_phi) + U_z^H (w*rho*g_z) ) / s

    ^H     conjugate transpose of the (n, k) reduced maps U_R, U_phi, U_z
    w      volume_weights (n,) = R dR dz, WITHOUT 2 pi, finite and > 0
    rho    real background density (n,), finite and > 0
    g      grad (n, 3), columns (g_R, g_phi, g_z): complex mode-m Fourier
           coefficients of the induced cylindrical gradient, taken by root as
           numpy.fft.fft over the 16 angles, bin m, divided by 16 (synthesis
           exp(+i m phi)); g_phi already means (1/R) d_phi deltaPhi
    s      normalization_scale, explicit, finite and > 0

No factor 2, no 2 pi, no extra 1/R, no sign reversal, no FFT or angle
selection, no solve and no state update.  m (1..6) labels the retained mode;
the formula itself does not contain m.

The kernel uses explicit Python loops over maps, columns and points with
Python complex scalars only: no matrix product and no numpy reduction.
Validation follows W1's reading of the 0453 text.  Type rules the text leaves
open (numpy integer m, integer dtypes, bool) are reference choices here, not
requirements of 0453.

MUTATIONS and make_mutant() give single-change variants of the same kernel.
W1_fixtures_v001.py --mutation-study uses them to show the fixtures detect
each change.  A mutant accepts an extra keyword R (per-point radius) because
three mutations need it; the 0453 operation itself has no R input.
"""

import math
import numbers

import numpy as np

__all__ = ["induced_field_weak_load_reference", "make_mutant", "MUTATIONS",
           "R_DEPENDENT_MUTATIONS", "REFERENCE_VERSION"]

REFERENCE_VERSION = "W1_reference_v001"

_COMPONENTS = ("R", "phi", "z")


# ----------------------------------------------------------------- validation
def _mode(m):
    if isinstance(m, bool) or not isinstance(m, numbers.Integral):
        raise ValueError("parameter 'm' must be an integer mode (bool rejected); got %r of type %s"
                         % (m, type(m).__name__))
    if not 1 <= int(m) <= 6:
        raise ValueError("parameter 'm' must satisfy 1 <= m <= 6; got %r" % (m,))
    return int(m)


def _map(name, value, n=None, k=None):
    a = np.asarray(value)
    if a.dtype.kind not in "iufc":
        raise ValueError("parameter '%s' must have an integer, floating or complex dtype; got %s"
                         % (name, a.dtype))
    if a.ndim != 2 or a.shape[0] < 1 or a.shape[1] < 1:
        raise ValueError("parameter '%s' must be a 2-D (n, k) array with n, k >= 1; got shape %s"
                         % (name, a.shape))
    if (n is not None and a.shape[0] != n) or (k is not None and a.shape[1] != k):
        raise ValueError("parameter '%s' must have shape (%s, %s); got %s" % (name, n, k, a.shape))
    a = np.array(a, dtype=np.complex128)  # private copy; the caller's array is only read
    for row in a:
        for v in row:
            if not (math.isfinite(v.real) and math.isfinite(v.imag)):
                raise ValueError("parameter '%s' must be finite everywhere" % name)
    return a


def _positive_vector(name, value, n):
    a = np.asarray(value)
    if a.dtype.kind not in "iuf":
        raise ValueError("parameter '%s' must be real (integer or floating dtype); got %s"
                         % (name, a.dtype))
    if a.ndim != 1 or a.shape[0] != n:
        raise ValueError("parameter '%s' must have shape (%d,); got %s" % (name, n, a.shape))
    a = np.array(a, dtype=np.float64)
    for v in a:
        if not (math.isfinite(v) and v > 0.0):
            raise ValueError("parameter '%s' must be finite and > 0 everywhere" % name)
    return a


def _gradient(value, n):
    a = np.asarray(value)
    if a.dtype.kind not in "iufc":
        raise ValueError("parameter 'grad' must have an integer, floating or complex dtype; got %s"
                         % a.dtype)
    if a.shape != (n, 3):
        raise ValueError("parameter 'grad' must have shape (%d, 3) = (n, [R, phi, z]); got %s"
                         % (n, a.shape))
    a = np.array(a, dtype=np.complex128)
    for row in a:
        for v in row:
            if not (math.isfinite(v.real) and math.isfinite(v.imag)):
                raise ValueError("parameter 'grad' must be finite everywhere")
    return a


def _scale(value):
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError("parameter 'normalization_scale' must be a real number (bool rejected); "
                         "got type %s" % type(value).__name__)
    s = float(value)
    if not (math.isfinite(s) and s > 0.0):
        raise ValueError("parameter 'normalization_scale' must be finite and > 0; got %r" % (value,))
    return s


# ---------------------------------------------------------------------- kernel
_IDENTITY = {
    "conj_maps": (True, True, True),  # U^H: conjugate every map entry
    "conj_grad": False,               # the gradient coefficient is used as supplied
    "sign": -1.0,                     # leading minus
    "norm_power": 1,                  # divide once by s
    "factor": 1.0,                    # no 2, no 2 pi
    "phi_R_power": 0,                 # g_phi used as supplied (already (1/R) d_phi)
    "measure_R_power": 0,             # w already contains R
    "perm": (0, 1, 2),                # U_R <-> column 0, U_phi <-> 1, U_z <-> 2
    "use_w": True,
    "use_rho": True,
    "wrho_power": 1,
    "conj_output": False,
    "real_output": False,
    "phi_m_factor": False,
}


def _kernel(m, maps, rho, w, grad, s, R, opts):
    """Explicit loops, Python complex scalars; returns (delta_b list, three load lists)."""
    n, k = len(maps[0]), len(maps[0][0])
    raw = [[0j] * k for _ in range(3)]
    for c in range(3):
        U = maps[c]
        col = opts["perm"][c]
        for j in range(k):
            acc = 0j
            for p in range(n):
                u = complex(U[p][j])
                if opts["conj_maps"][c]:
                    u = u.conjugate()
                g = complex(grad[p][col])
                if opts["conj_grad"]:
                    g = g.conjugate()
                if c == 1 and opts["phi_R_power"]:
                    g = g * (float(R[p]) ** opts["phi_R_power"])
                if c == 1 and opts["phi_m_factor"]:
                    g = g * m
                weight = 1.0
                if opts["use_w"]:
                    weight = weight * float(w[p])
                if opts["use_rho"]:
                    weight = weight * float(rho[p])
                if opts["wrho_power"] != 1:
                    weight = weight ** opts["wrho_power"]
                if opts["measure_R_power"]:
                    weight = weight * (float(R[p]) ** opts["measure_R_power"])
                acc += u * complex(weight * g.real, weight * g.imag)
            raw[c][j] = acc

    def finish(t):
        t = complex(opts["sign"] * opts["factor"] * t.real, opts["sign"] * opts["factor"] * t.imag)
        for _ in range(opts["norm_power"]):
            t = complex(t.real / s, t.imag / s)
        if opts["conj_output"]:
            t = t.conjugate()
        if opts["real_output"]:
            t = complex(t.real, 0.0)
        return t

    total = [finish(raw[0][j] + raw[1][j] + raw[2][j]) for j in range(k)]
    loads = [[finish(raw[c][j]) for j in range(k)] for c in range(3)]
    return total, loads


def _evaluate(m, U_R, U_phi, U_z, rho, volume_weights, grad, normalization_scale, R, mutation):
    m = _mode(m)
    U_R = _map("U_R", U_R)
    n, k = U_R.shape
    U_phi = _map("U_phi", U_phi, n, k)
    U_z = _map("U_z", U_z, n, k)
    rho = _positive_vector("rho", rho, n)
    w = _positive_vector("volume_weights", volume_weights, n)
    grad = _gradient(grad, n)
    s = _scale(normalization_scale)
    opts = dict(_IDENTITY)
    opts.update(mutation)
    if R is not None:
        R = _positive_vector("R", R, n)
    elif opts["phi_R_power"] or opts["measure_R_power"]:
        raise ValueError("this mutant needs the per-point radius R")
    maps = [U_R.tolist(), U_phi.tolist(), U_z.tolist()]
    total, loads = _kernel(m, maps, rho.tolist(), w.tolist(), grad.tolist(), s,
                           None if R is None else R.tolist(), opts)
    for t in total + loads[0] + loads[1] + loads[2]:
        if not (math.isfinite(t.real) and math.isfinite(t.imag)):
            raise ValueError("returned load is not finite (overflow or invalid operation)")
    out = {"delta_b": np.array(total, dtype=np.complex128)}
    for c, name in enumerate(_COMPONENTS):
        out["load_" + name] = np.array(loads[c], dtype=np.complex128)
    out.update({"m": m, "normalization_scale": s, "npoints": n, "nfree": k,
                "reference_version": REFERENCE_VERSION})
    return out


def induced_field_weak_load_reference(*, m, U_R, U_phi, U_z, rho, volume_weights, grad,
                                      normalization_scale):
    """Loop reference of the 0453 operation.

    Returns a new dict: delta_b (k,) complex128 and the component loads
    load_R, load_phi, load_z, each -U_c^H (w*rho*g_c) / s, so that
    delta_b = load_R + load_phi + load_z up to rounding.  Raises ValueError
    naming the parameter for an invalid or non-finite input, and ValueError for
    a non-finite result.  No input is modified.
    """
    return _evaluate(m, U_R, U_phi, U_z, rho, volume_weights, grad, normalization_scale,
                     None, {})


# -------------------------------------------------------------------- mutants
MUTATIONS = {
    "missing_conj": {"conj_maps": (False, False, False)},
    "missing_conj_phi_only": {"conj_maps": (True, False, True)},
    "missing_conj_R_z_only": {"conj_maps": (False, True, False)},
    "conj_on_gradient_instead_of_maps": {"conj_maps": (False, False, False), "conj_grad": True},
    "extra_conj_on_gradient": {"conj_grad": True},
    "sign_flipped": {"sign": 1.0},
    "normalization_omitted": {"norm_power": 0},
    "normalization_applied_twice": {"norm_power": 2},
    "extra_2pi": {"factor": 2.0 * math.pi},
    "factor_2": {"factor": 2.0},
    "extra_1_over_R_on_grad_phi": {"phi_R_power": -1},
    "R_instead_of_1_on_grad_phi": {"phi_R_power": 1},
    "R_instead_of_1_in_measure": {"measure_R_power": 1},
    "components_swapped_R_z": {"perm": (2, 1, 0)},
    "components_swapped_phi_R": {"perm": (1, 0, 2)},
    "w_omitted": {"use_w": False},
    "rho_omitted": {"use_rho": False},
    "w_rho_squared": {"wrho_power": 2},
    "output_conjugated": {"conj_output": True},
    "real_part_only": {"real_output": True},
    "grad_phi_times_m": {"phi_m_factor": True},
}

R_DEPENDENT_MUTATIONS = ("extra_1_over_R_on_grad_phi", "R_instead_of_1_on_grad_phi",
                         "R_instead_of_1_in_measure")


def make_mutant(name):
    """Return the reference with exactly one change (MUTATIONS[name]); '' gives no change."""
    mutation = dict(MUTATIONS[name]) if name else {}

    def mutant(*, m, U_R, U_phi, U_z, rho, volume_weights, grad, normalization_scale, R=None):
        return _evaluate(m, U_R, U_phi, U_z, rho, volume_weights, grad, normalization_scale,
                         R, mutation)

    mutant.__name__ = "mutant_" + (name or "none")
    return mutant
