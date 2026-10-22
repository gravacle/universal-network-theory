"""UNT 0438 -- conservative density projection on the reviewed 32-point free-surface mesh (c2v002).

c2v002 is c2v001 (sha256 b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112) brought under the
standing lane numerics convention (Codex 0354/0397/0414). Every matrix/vector product is an explicit
numpy.einsum(..., optimize=False) instead of @ / numpy.dot / BLAS (including the hidden dot inside
numpy.linalg.norm). There is no local floating-point suppression: the caller's numpy errstate and warnings
filters govern. A FloatingPointError, or a RuntimeWarning raised as an exception by the caller's warnings
filter, inside the arithmetic returns status "failed_closed_floating_point" with completed blocks retained.
numpy.linalg.solve per 8x8 block and numpy.linalg.svd for diagnostics are unchanged. Every explicit isfinite
decision is unchanged.

Pure inert module. Imports numpy only; defines constants and functions; performs no computation and no I/O at
import; every outcome is returned as a dict (fail-closed). It never imports project workers and never reads data.

Binding equation (task 0438, verbatim; see EQUATION_VERBATIM):
    M=V^H W V;
    b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z);
    M*a=b;
    delta_rho=V*a.

Block layout (read from the TEXT of owned_free_surface_32q8trial_maps_v001.py, sha256
3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943; never imported): V is built with shape
(72, 32, 72, 8), V[i, :, i, :] = P[i], then reshaped in C order to (2304, 576). Hence row = 32*i + l
(radius i, actual quadrature node l) and column = 8*j + a (radius j, Legendre coefficient a); radial block i
is rows 32*i .. 32*i+31 by columns 8*i .. 8*i+7. weights_RdRdz = (wr[:, None] * wz).reshape(-1) uses the
same row index and already is the complete R dR dz measure, so W enters each integral exactly once and no
2*pi or annular factor is added here.

Explicit assumptions of the supplied weak domain (stated, NOT verified by this routine):
  * physical-vacuum vanishing density on the free surfaces (no surface term in the weak form);
  * root-enforced radial boundary flux (no radial boundary term is added).

Not computed: pressure, velocity, source response, equilibrium, modal solution, physical acceptance.
"""
import numpy as np

N_RADII = 72
N_NODES_PER_RADIUS = 32
N_COEFFS_PER_RADIUS = 8
MODE_MIN = 0
MODE_MAX = 8

EQUATION_VERBATIM = (
    "M=V^H W V;\n"
    "b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z);\n"
    "M*a=b;\n"
    "delta_rho=V*a."
)

ASSUMPTIONS_NOT_VERIFIED = (
    "Physical-vacuum vanishing density on the free surfaces: the weak form carries no surface term. "
    "Assumption of the supplied weak domain; not verified here.",
    "Root-enforced radial boundary flux: no radial boundary term is added. "
    "Assumption of the supplied weak domain; not verified here.",
)

NOT_COMPUTED = (
    "pressure", "velocity", "source response", "equilibrium", "modal solution", "physical acceptance",
)

INPUT_DTYPE_RULES = (
    "value, partial_R, partial_z, weights, radius, rho: numpy.ndarray (exact type, no subclasses) of real "
    "floating dtype with itemsize <= 8 (float16/float32/float64), upcast exactly to float64; complex, integer, "
    "bool and object dtypes are rejected, so no imaginary part is ever dropped.",
    "xi_R, xi_phi, xi_z: numpy.ndarray (exact type) of complex dtype with itemsize <= 16 "
    "(complex64/complex128), upcast exactly to complex128; REAL-dtype xi inputs are REJECTED, not promoted.",
    "mode: Python int or numpy integer in 0..8 inclusive; bool and numpy.bool_ are rejected.",
    "provenance: str that is non-empty after stripping whitespace.",
)


def _result(status, reason, provenance):
    return {
        "status": status,
        "reason": reason,
        "provenance": provenance,
        "equation": EQUATION_VERBATIM,
        "assumptions_not_verified": list(ASSUMPTIONS_NOT_VERIFIED),
        "not_computed": list(NOT_COMPUTED),
        "a": None,
        "delta_rho": None,
    }


def _reject(field, reason, provenance=None):
    out = _result("rejected_input", reason, provenance)
    out["field"] = field
    return out


def _check_real(name, x, shape, positive):
    if type(x) is not np.ndarray:
        return "%s must be a numpy.ndarray (subclasses rejected); got %s" % (name, type(x).__name__)
    if x.dtype.kind != "f" or x.dtype.itemsize > 8:
        return "%s must have real floating dtype float16/float32/float64; got %s" % (name, x.dtype)
    if x.shape != shape:
        return "%s must have shape %s exactly; got %s" % (name, shape, x.shape)
    if not np.all(np.isfinite(x)):
        return "%s must be finite" % name
    if positive and not np.all(x > 0):
        return "%s must be strictly positive" % name
    return None


def _check_complex(name, x, shape):
    if type(x) is not np.ndarray:
        return "%s must be a numpy.ndarray (subclasses rejected); got %s" % (name, type(x).__name__)
    if x.dtype.kind != "c" or x.dtype.itemsize > 16:
        return ("%s must have complex dtype complex64/complex128 (real dtype rejected, not promoted); got %s"
                % (name, x.dtype))
    if x.shape != shape:
        return "%s must have shape %s exactly; got %s" % (name, shape, x.shape)
    if not np.all(np.isfinite(x)):
        return "%s must be finite (real and imaginary parts)" % name
    return None


def _is_plain_int(x):
    if isinstance(x, (bool, np.bool_)):
        return False
    return isinstance(x, (int, np.integer))


def _value_block_mask(n_radii, n_nodes, n_coeffs):
    """True on radial block i: rows n_nodes*i .. n_nodes*i+n_nodes-1, columns n_coeffs*i .. n_coeffs*i+n_coeffs-1."""
    mask = np.zeros((n_radii * n_nodes, n_radii * n_coeffs), dtype=bool)
    for i in range(n_radii):
        mask[n_nodes * i:n_nodes * (i + 1), n_coeffs * i:n_coeffs * (i + 1)] = True
    return mask


def _coeff_block_mask(n_radii, n_coeffs):
    mask = np.zeros((n_radii * n_coeffs, n_radii * n_coeffs), dtype=bool)
    for i in range(n_radii):
        mask[n_coeffs * i:n_coeffs * (i + 1), n_coeffs * i:n_coeffs * (i + 1)] = True
    return mask


def _validate(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode, provenance,
              n_radii, n_nodes, n_coeffs):
    if not isinstance(provenance, str) or not provenance.strip():
        return _reject("provenance", "provenance must be a non-empty str"), None
    if not _is_plain_int(mode):
        return _reject("mode", "mode must be a Python int or numpy integer (bool rejected); got %s"
                       % type(mode).__name__, provenance), None
    mode_int = int(mode)
    if mode_int < MODE_MIN or mode_int > MODE_MAX:
        return _reject("mode", "mode must lie in %d..%d; got %d" % (MODE_MIN, MODE_MAX, mode_int),
                       provenance), None
    n_rows = n_radii * n_nodes
    n_cols = n_radii * n_coeffs
    for name, x in (("value", value), ("partial_R", partial_R), ("partial_z", partial_z)):
        msg = _check_real(name, x, (n_rows, n_cols), positive=False)
        if msg is not None:
            return _reject(name, msg, provenance), None
    for name, x in (("weights", weights), ("radius", radius), ("rho", rho)):
        msg = _check_real(name, x, (n_rows,), positive=True)
        if msg is not None:
            return _reject(name, msg, provenance), None
    for name, x in (("xi_R", xi_R), ("xi_phi", xi_phi), ("xi_z", xi_z)):
        msg = _check_complex(name, x, (n_rows,))
        if msg is not None:
            return _reject(name, msg, provenance), None
    V = np.asarray(value, dtype=np.float64)
    off = ~_value_block_mask(n_radii, n_nodes, n_coeffs)
    bad = np.argwhere(off & (V != 0))
    if bad.shape[0] != 0:
        r0, c0 = (int(bad[0, 0]), int(bad[0, 1]))
        out = _reject("value", "value must be exactly zero outside its %d diagonal %dx%d radial blocks; "
                      "%d nonzero off-block entries, first at (row %d, col %d)"
                      % (n_radii, n_nodes, n_coeffs, bad.shape[0], r0, c0), provenance)
        out["offblock_nonzero_count"] = int(bad.shape[0])
        out["offblock_first_nonzero"] = (r0, c0)
        return out, None
    arrays = dict(
        V=V,
        VR=np.asarray(partial_R, dtype=np.float64),
        VZ=np.asarray(partial_z, dtype=np.float64),
        W=np.asarray(weights, dtype=np.float64),
        R=np.asarray(radius, dtype=np.float64),
        rho=np.asarray(rho, dtype=np.float64),
        xi_R=np.asarray(xi_R, dtype=np.complex128),
        xi_phi=np.asarray(xi_phi, dtype=np.complex128),
        xi_z=np.asarray(xi_z, dtype=np.complex128),
        mode=mode_int,
    )
    return None, arrays


def _norm2(x):
    """2-norm of a 1-D vector by numpy.linalg.norm's own formula (square root of the summed squares of the real
    and imaginary parts), with einsum(..., optimize=False) in place of the BLAS dot that norm uses internally."""
    xr = x.real
    xi = x.imag
    return np.sqrt(np.einsum("i,i->", xr, xr, optimize=False) + np.einsum("i,i->", xi, xi, optimize=False))


def _compute(**kwargs):
    """Arithmetic on already-validated arrays. No local floating-point suppression: the caller's numpy errstate
    and warnings filters govern, and every decision is an explicit isfinite check. A FloatingPointError (caller
    errstate "raise") or a RuntimeWarning raised as an exception (caller warnings filter "error") inside the
    arithmetic is returned fail-closed as status "failed_closed_floating_point", with the stage, the block in
    progress, completed_blocks and solved_coefficients retained. Nothing is suppressed, retried or recomputed."""
    state = {"stage": "assembly of M and b", "failed_block": None, "completed": 0, "fail": None}
    try:
        return _arithmetic(state=state, **kwargs)
    except (FloatingPointError, RuntimeWarning) as exc:
        text = "%s: %s" % (type(exc).__name__, exc)
        # state["fail"] is registered by _arithmetic before any arithmetic statement.
        out = state["fail"]("failed_closed_floating_point",
                            "%s raised under the caller's numpy errstate / warnings filter during %s"
                            % (text, state["stage"]), state["failed_block"], state["completed"])
        out["failed_stage"] = state["stage"]
        out["floating_point_exception"] = text
        return out


def _arithmetic(*, V, VR, VZ, W, R, rho, xi_R, xi_phi, xi_z, mode, provenance, n_radii, n_coeffs, state):
    """Arithmetic of the binding equation. ^H is written as .conj().T. Every product is an explicit
    numpy.einsum(..., optimize=False), never @ / dot / matmul (no BLAS). state records progress for _compute."""
    n_cols = n_radii * n_coeffs
    out = _result("computed", None, provenance)
    out["mode"] = mode
    out["n_blocks"] = n_radii
    out["block_size"] = n_coeffs
    a = np.zeros(n_cols, dtype=np.complex128)

    def fail(status, reason, failed_block, completed):
        out["status"] = status
        out["reason"] = reason
        out["failed_block"] = failed_block
        out["completed_blocks"] = completed
        out["solved_coefficients"] = a[:n_coeffs * completed].copy()
        out["a"] = None
        out["delta_rho"] = None
        return out

    state["fail"] = fail

    VH = V.conj().T
    # M=V^H W V  (W used once)
    M = np.einsum("il,lj->ij", VH, W[:, None] * V, optimize=False)
    # b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z)  (W used once in each integral)
    b_radial = np.einsum("il,l->i", VR.conj().T, W * (rho * xi_R), optimize=False)
    b_azimuthal = (-1j * mode) * np.einsum("il,l->i", VH, W * (rho * xi_phi / R), optimize=False)
    b_vertical = np.einsum("il,l->i", VZ.conj().T, W * (rho * xi_z), optimize=False)
    b = b_radial + b_azimuthal + b_vertical

    out["b"] = b
    out["b_terms"] = {"radial": b_radial, "azimuthal": b_azimuthal, "vertical": b_vertical}

    state["stage"] = "off-block check and block diagnostics"
    off = M[~_coeff_block_mask(n_radii, n_coeffs)]
    out["M_offblock_max_abs"] = float(np.max(np.abs(off))) if off.size else 0.0

    blocks = [slice(n_coeffs * i, n_coeffs * (i + 1)) for i in range(n_radii)]
    M_blocks = np.stack([M[s, s].copy() for s in blocks])
    out["M_blocks"] = M_blocks

    # Diagnostics only (no threshold): singular values, their range, and 2-norm condition number per block.
    sv = np.full((n_radii, n_coeffs), np.nan)
    for i in range(n_radii):
        if np.all(np.isfinite(M_blocks[i])):
            try:
                sv[i] = np.linalg.svd(M_blocks[i], compute_uv=False)
            except np.linalg.LinAlgError:
                pass
    sv_min = np.min(sv, axis=1)
    sv_max = np.max(sv, axis=1)
    # inf where the smallest singular value is exactly zero, without evaluating a division by zero.
    cond = np.full(n_radii, np.inf)
    nonzero = sv_min != 0
    cond[nonzero] = sv_max[nonzero] / sv_min[nonzero]
    out["block_singular_values"] = sv
    out["block_singular_value_min"] = sv_min
    out["block_singular_value_max"] = sv_max
    out["block_condition_number"] = cond

    if off.size and not np.all(off == 0):
        return fail("failed_closed_solve",
                    "assembled M is not exactly block diagonal (non-finite or nonzero off-block entries); "
                    "separate block solves would not be the stated equation", None, 0)

    # M*a=b, solved as the separate diagonal blocks with ordinary direct solves.
    state["stage"] = "block solves"
    for i, s in enumerate(blocks):
        state["failed_block"] = i
        state["completed"] = i
        Mi = M_blocks[i]
        bi = b[s]
        if not (np.all(np.isfinite(Mi)) and np.all(np.isfinite(bi))):
            return fail("failed_closed_solve", "non-finite M block or b block at block %d" % i, i, i)
        try:
            ai = np.linalg.solve(Mi, bi)
        except np.linalg.LinAlgError as exc:
            return fail("failed_closed_solve", "singular M block %d (%s)" % (i, exc), i, i)
        if not np.all(np.isfinite(ai)):
            return fail("failed_closed_solve", "non-finite solve result at block %d" % i, i, i)
        a[s] = ai

    state["stage"] = "delta_rho, residual and their diagnostics"
    state["failed_block"] = None
    state["completed"] = n_radii
    # delta_rho=V*a
    delta_rho = np.einsum("ij,j->i", V, a, optimize=False)
    # Directly computed residual M*a-b with the assembled M.
    residual = np.einsum("ij,j->i", M, a, optimize=False) - b
    if not (np.all(np.isfinite(delta_rho)) and np.all(np.isfinite(residual))):
        return fail("failed_closed_solve", "non-finite delta_rho or residual after all block solves",
                    None, n_radii)

    # Computed before any result key is set, so a floating-point exception here leaves no partial result keys.
    residual_block_norm = np.array([_norm2(residual[s]) for s in blocks])
    residual_global_norm = float(_norm2(residual))
    # Complex diagnostic, not forced to zero (unconjugated, as numpy.dot(W, delta_rho) in c2v001).
    dot_W_delta_rho = complex(np.einsum("l,l->", W, delta_rho, optimize=False))

    out["completed_blocks"] = n_radii
    out["failed_block"] = None
    out["a"] = a
    out["delta_rho"] = delta_rho
    out["residual"] = residual
    out["residual_block_norm"] = residual_block_norm
    out["residual_global_norm"] = residual_global_norm
    out["dot_W_delta_rho"] = dot_W_delta_rho
    return out


def _project_density_sized(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode,
                           provenance, n_radii, n_nodes, n_coeffs):
    """Private: same validation and arithmetic with parameterized block sizes (reduced-size test stubs only)."""
    for nm, n in (("n_radii", n_radii), ("n_nodes", n_nodes), ("n_coeffs", n_coeffs)):
        if not _is_plain_int(n) or int(n) < 1:
            return _reject(nm, "%s must be a positive int" % nm)
    n_radii, n_nodes, n_coeffs = int(n_radii), int(n_nodes), int(n_coeffs)
    try:
        rejected, arr = _validate(value=value, partial_R=partial_R, partial_z=partial_z, weights=weights,
                                  radius=radius, rho=rho, xi_R=xi_R, xi_phi=xi_phi, xi_z=xi_z, mode=mode,
                                  provenance=provenance, n_radii=n_radii, n_nodes=n_nodes, n_coeffs=n_coeffs)
        if rejected is not None:
            return rejected
        out = _compute(provenance=provenance, n_radii=n_radii, n_coeffs=n_coeffs, **arr)
    except Exception as exc:  # fail closed on anything unexpected
        prov = provenance if isinstance(provenance, str) else None
        return _result("failed_closed_internal", "%s: %s" % (type(exc).__name__, exc), prov)
    out["layout"] = {
        "rows": "row = %d*i + l (radius i, quadrature node l)" % n_nodes,
        "columns": "column = %d*j + a (radius j, trial coefficient a)" % n_coeffs,
        "block_i": "rows %d*i..%d*i+%d, columns %d*i..%d*i+%d" % (n_nodes, n_nodes, n_nodes - 1,
                                                                n_coeffs, n_coeffs, n_coeffs - 1),
        "shape_value": (n_radii * n_nodes, n_radii * n_coeffs),
    }
    return out


def project_density(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode, provenance):
    """Conservative density projection on the 72 x (32 nodes, 8 trial coefficients) free-surface mesh.

    value=V, partial_R=VR, partial_z=VZ: real finite (2304, 576); V exactly zero outside its 72 diagonal 32x8
    radial blocks (VR, VZ need not be block diagonal). weights=W, radius=R, rho: positive finite real (2304,).
    xi_R, xi_phi, xi_z: finite complex (2304,). mode: integer 0..8. provenance: non-empty str.

    Returns a dict. status "computed": a (576,), delta_rho (2304,), b (576,) and its three terms, M blocks,
    per-block singular values / ranges / condition numbers (diagnostics, no threshold), residual M*a-b with
    per-block and global norms, dot(W, delta_rho) (complex diagnostic). status "rejected_input",
    "failed_closed_solve" (completed_blocks and solved_coefficients retained), "failed_closed_floating_point"
    (a FloatingPointError or escalated RuntimeWarning under the caller's errstate / warnings filter; same
    retention plus failed_stage and floating_point_exception) or "failed_closed_internal" otherwise. There is no
    physical acceptance flag. Products are numpy.einsum(..., optimize=False); no floating-point suppression.
    """
    return _project_density_sized(value=value, partial_R=partial_R, partial_z=partial_z, weights=weights,
                                  radius=radius, rho=rho, xi_R=xi_R, xi_phi=xi_phi, xi_z=xi_z, mode=mode,
                                  provenance=provenance, n_radii=N_RADII, n_nodes=N_NODES_PER_RADIUS,
                                  n_coeffs=N_COEFFS_PER_RADIUS)
