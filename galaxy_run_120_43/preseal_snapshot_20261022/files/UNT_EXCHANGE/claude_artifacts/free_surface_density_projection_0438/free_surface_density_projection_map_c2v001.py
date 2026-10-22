"""UNT 0441 -- batched density-projection MAP on the reviewed 32-point free-surface mesh (Claude2, map c2v001).

The 0438 conservative density projection applied column-wise to root-supplied displacement maps (task 0441).
It is the same specified linear projection, not a new physical equation. The 0438 vector API (project_density in
free_surface_density_projection_c2v001.py, sha256 b07fd00875e90e92c396b31103f3306dd8d85fbb1a10a44725f809a1553c6112,
and its convention-only successor c2v002) is preserved unchanged and is NOT imported here.

Pure inert module. Imports numpy only; defines constants and functions; performs no computation and no I/O at
import; every outcome after argument binding is returned as a dict (fail closed). It never imports project
workers and never reads data.

Binding equations (0441, verbatim; there '@' denotes the mathematical product):
    M = V.conj().T @ (W[:,None]*V)
    B = VR.conj().T @ ((W*rho)[:,None]*xi_R) - 1j*mode*V.conj().T @ ((W*rho/R)[:,None]*xi_phi)
        + VZ.conj().T @ ((W*rho)[:,None]*xi_z)
    the same 72 independent 8x8 mass blocks solved against multiple right-hand sides (M coefficients = B)
    G = V @ coefficients
Parent (0438, verbatim): M=V^H W V; b=VR^H W(rho*xi_R) - i*mode*V^H W(rho*xi_phi/R) + VZ^H W(rho*xi_z);
M*a=b; delta_rho=V*a.  Column j of the map is exactly that vector projection with xi = xi_*[:, j].

Lane numerics convention (binding): every product is numpy.einsum(..., optimize=False) with explicit subscripts;
no @ / dot / matmul / vdot / inner / tensordot / linalg.norm. numpy.linalg.solve per 8x8 block (multiple RHS)
and numpy.linalg.svd (diagnostics) are the only LAPACK calls. No floating-point suppression: the caller's numpy
errstate and warnings filters govern. A FloatingPointError (or a RuntimeWarning escalated by the caller's
warnings filter) is returned as status "failed_closed_floating_point" with completed (block, batch) work retained.
Every decision is an explicit isfinite / exact-zero test. No ridge, clipping, pseudoinverse, full dense inverse,
tolerance, hidden weight, rescaling or acceptance flag.

Block layout (as in c2v001, read from the TEXT of owned_free_surface_32q8trial_maps_v001.py, sha256
3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943; never imported): row = 32*i + l, column =
8*j + a; radial block i is rows 32*i..32*i+31 by columns 8*i..8*i+7; W is the complete R dR dz measure on the
same row index, entering each integral exactly once (no 2*pi or annular factor).

Batching: RHS columns are processed in caller-supplied blocks of rhs_batch_size (never chosen here). M and its
72 diagonal blocks are formed once, before the first batch, and reused by every batch. Order: batch k assembles
B[:, batch k], then solves blocks 0..71 for it, then forms G, the residual, its norms and the mass integral.

Retention: after validation every stop (LinAlgError or non-finite test -> "failed_closed_solve"; FloatingPointError
/ escalated RuntimeWarning -> "failed_closed_floating_point"; KeyboardInterrupt -> "interrupted", returned and not
re-raised; any other exception -> "failed_closed_internal") returns completed_block_batch (n_blocks, n_batches),
B_assembled_batches, completed_batches, failed_stage / failed_batch / failed_block and partial_<key> arrays that
are NaN wherever the entry was not completed and checked. The primary result keys are then None. An interruption
during validation, before any work exists, propagates unchanged.

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
    "M = V.conj().T @ (W[:,None]*V)\n"
    "B = VR.conj().T @ ((W*rho)[:,None]*xi_R) - 1j*mode*V.conj().T @ ((W*rho/R)[:,None]*xi_phi) "
    "+ VZ.conj().T @ ((W*rho)[:,None]*xi_z)\n"
    "Solve the same 72 independent 8-by-8 mass blocks against multiple right-hand sides, forming each mass "
    "block only once.\n"
    "G=V@coefficients"
)

PARENT_EQUATION_0438_VERBATIM = (
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
    "(complex64/complex128), identical shape (2304, nfree) with nfree >= 1, upcast exactly to complex128 one "
    "batch at a time; REAL-dtype xi inputs are REJECTED, not promoted.",
    "mode: Python int or numpy integer in 0..8 inclusive; bool and numpy.bool_ are rejected.",
    "rhs_batch_size: Python int or numpy integer >= 1 supplied by the caller (values > nfree mean one batch); "
    "bool and numpy.bool_ are rejected.",
    "provenance: str that is non-empty after stripping whitespace.",
)

RESULT_ARRAY_KEYS = (
    "coefficients", "G", "B", "residual", "residual_block_column_norm", "residual_column_norm", "mass_integral",
)


def _result(status, reason, provenance):
    out = {
        "status": status,
        "reason": reason,
        "provenance": provenance,
        "equation": EQUATION_VERBATIM,
        "parent_equation_0438": PARENT_EQUATION_0438_VERBATIM,
        "assumptions_not_verified": list(ASSUMPTIONS_NOT_VERIFIED),
        "not_computed": list(NOT_COMPUTED),
    }
    for key in RESULT_ARRAY_KEYS:
        out[key] = None
    return out


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


def _check_complex_map(name, x, n_rows, shape_required, batch):
    """Complex map (n_rows, nfree), nfree >= 1; finiteness checked one rhs batch of columns at a time."""
    if type(x) is not np.ndarray:
        return "%s must be a numpy.ndarray (subclasses rejected); got %s" % (name, type(x).__name__)
    if x.dtype.kind != "c" or x.dtype.itemsize > 16:
        return ("%s must have complex dtype complex64/complex128 (real dtype rejected, not promoted); got %s"
                % (name, x.dtype))
    if x.ndim != 2 or x.shape[0] != n_rows or x.shape[1] < 1:
        return "%s must have shape (%d, nfree) with nfree >= 1; got %s" % (name, n_rows, x.shape)
    if shape_required is not None and x.shape != shape_required:
        return "%s must have shape identical to xi_R %s; got %s" % (name, shape_required, x.shape)
    for c0 in range(0, x.shape[1], batch):
        if not np.all(np.isfinite(x[:, c0:c0 + batch])):
            return ("%s must be finite (real and imaginary parts); non-finite entry in columns %d..%d"
                    % (name, c0, min(x.shape[1], c0 + batch) - 1))
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
              rhs_batch_size, n_radii, n_nodes, n_coeffs):
    if not isinstance(provenance, str) or not provenance.strip():
        return _reject("provenance", "provenance must be a non-empty str"), None
    if not _is_plain_int(mode):
        return _reject("mode", "mode must be a Python int or numpy integer (bool rejected); got %s"
                       % type(mode).__name__, provenance), None
    mode_int = int(mode)
    if mode_int < MODE_MIN or mode_int > MODE_MAX:
        return _reject("mode", "mode must lie in %d..%d; got %d" % (MODE_MIN, MODE_MAX, mode_int),
                       provenance), None
    if not _is_plain_int(rhs_batch_size):
        return _reject("rhs_batch_size", "rhs_batch_size must be a Python int or numpy integer supplied by the "
                       "caller (bool rejected); got %s" % type(rhs_batch_size).__name__, provenance), None
    batch = int(rhs_batch_size)
    if batch < 1:
        return _reject("rhs_batch_size", "rhs_batch_size must be >= 1; got %d" % batch, provenance), None
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
    shape_required = None
    for name, x in (("xi_R", xi_R), ("xi_phi", xi_phi), ("xi_z", xi_z)):
        msg = _check_complex_map(name, x, n_rows, shape_required, batch)
        if msg is not None:
            return _reject(name, msg, provenance), None
        shape_required = x.shape
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
        xi_R=xi_R,
        xi_phi=xi_phi,
        xi_z=xi_z,
        mode=mode_int,
        rhs_batch_size=batch,
    )
    return None, arrays


def _norm2_columns(x):
    """Column 2-norms of a 2-D complex array: sqrt(sum re^2 + sum im^2) over axis 0, by einsum (no BLAS dot)."""
    xr = x.real
    xi = x.imag
    return np.sqrt(np.einsum("ik,ik->k", xr, xr, optimize=False) + np.einsum("ik,ik->k", xi, xi, optimize=False))


def _norm2_block_columns(x, n_blocks, n_coeffs):
    """Per (block, column) 2-norms of a (n_blocks*n_coeffs, k) complex array, by einsum (no BLAS dot)."""
    k = x.shape[1]
    xr = x.real.reshape(n_blocks, n_coeffs, k)
    xi = x.imag.reshape(n_blocks, n_coeffs, k)
    return np.sqrt(np.einsum("bak,bak->bk", xr, xr, optimize=False)
                   + np.einsum("bak,bak->bk", xi, xi, optimize=False))


def _compute(*, V, VR, VZ, W, R, rho, xi_R, xi_phi, xi_z, mode, rhs_batch_size, provenance, n_radii, n_coeffs):
    """Run the arithmetic and convert every way it can stop into a fail-closed dict with completed work retained.

    LinAlgError / non-finite test -> "failed_closed_solve"; FloatingPointError or escalated RuntimeWarning ->
    "failed_closed_floating_point"; KeyboardInterrupt -> "interrupted" (returned, not re-raised); any other
    exception -> "failed_closed_internal". Nothing is suppressed, retried or recomputed."""
    nfree = xi_R.shape[1]
    ranges = [(c0, min(nfree, c0 + rhs_batch_size)) for c0 in range(0, nfree, rhs_batch_size)]
    n_batches = len(ranges)
    out = _result("computed", None, provenance)
    out["mode"] = mode
    out["nfree"] = nfree
    out["rhs_batch_size"] = rhs_batch_size
    out["n_batches"] = n_batches
    out["batch_column_ranges"] = ranges
    out["n_blocks"] = n_radii
    out["block_size"] = n_coeffs
    out["completed_block_batch"] = np.zeros((n_radii, n_batches), dtype=bool)
    out["B_assembled_batches"] = []
    out["completed_batches"] = []
    store = {}
    prog = {"stage": "allocation of result arrays", "batch": None, "block": None}
    try:
        stop = _arithmetic(out=out, store=store, prog=prog, ranges=ranges, V=V, VR=VR, VZ=VZ, W=W, R=R,
                           rho=rho, xi_R=xi_R, xi_phi=xi_phi, xi_z=xi_z, mode=mode, n_radii=n_radii,
                           n_coeffs=n_coeffs)
    except (FloatingPointError, RuntimeWarning) as exc:
        text = "%s: %s" % (type(exc).__name__, exc)
        stop = ("failed_closed_floating_point",
                "%s raised under the caller's numpy errstate / warnings filter" % text)
        out["floating_point_exception"] = text
    except KeyboardInterrupt:
        stop = ("interrupted", "KeyboardInterrupt caught and returned (not re-raised); completed work retained")
    except Exception as exc:  # fail closed on anything unexpected, keeping completed work
        stop = ("failed_closed_internal", "%s: %s" % (type(exc).__name__, exc))
    out["n_completed_columns"] = int(sum(ranges[k][1] - ranges[k][0] for k in out["completed_batches"]))
    if stop is None:
        for key in RESULT_ARRAY_KEYS:
            out[key] = store[key]
        out["failed_stage"] = None
        out["failed_batch"] = None
        out["failed_block"] = None
        return out
    out["status"], out["reason"] = stop
    out["reason"] = "%s [stage: %s; batch: %s; block: %s]" % (out["reason"], prog["stage"], prog["batch"],
                                                             prog["block"])
    out["failed_stage"] = prog["stage"]
    out["failed_batch"] = prog["batch"]
    out["failed_block"] = prog["block"]
    for key in RESULT_ARRAY_KEYS:
        out[key] = None
        out["partial_" + key] = store.get(key)
    return out


def _arithmetic(*, out, store, prog, ranges, V, VR, VZ, W, R, rho, xi_R, xi_phi, xi_z, mode, n_radii, n_coeffs):
    """Arithmetic of the binding equations, batch by batch. ^H is written .conj().T. Returns None when every
    batch completed, else (status, reason). Result arrays are NaN until an entry is completed and checked."""
    n_rows = V.shape[0]
    n_cols = n_radii * n_coeffs
    nfree = xi_R.shape[1]
    completed = out["completed_block_batch"]
    nan_c = complex(np.nan, np.nan)
    store["coefficients"] = np.full((n_cols, nfree), nan_c, dtype=np.complex128)
    store["G"] = np.full((n_rows, nfree), nan_c, dtype=np.complex128)
    store["B"] = np.full((n_cols, nfree), nan_c, dtype=np.complex128)
    store["residual"] = np.full((n_cols, nfree), nan_c, dtype=np.complex128)
    store["residual_block_column_norm"] = np.full((n_radii, nfree), np.nan)
    store["residual_column_norm"] = np.full(nfree, np.nan)
    store["mass_integral"] = np.full(nfree, nan_c, dtype=np.complex128)

    prog["stage"] = "assembly of M"
    VH = V.conj().T
    # M = V.conj().T @ (W[:,None]*V)   -- formed once; W used once
    M = np.einsum("il,lj->ij", VH, W[:, None] * V, optimize=False)

    prog["stage"] = "off-block check and block diagnostics"
    off = M[~_coeff_block_mask(n_radii, n_coeffs)]
    out["M_offblock_max_abs"] = float(np.max(np.abs(off))) if off.size else 0.0
    m_not_block_diagonal = bool(off.size) and not bool(np.all(off == 0))
    del off
    blocks = [slice(n_coeffs * i, n_coeffs * (i + 1)) for i in range(n_radii)]
    # The 72 diagonal 8x8 mass blocks, copied once and reused by every batch.
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
    cond = np.full(n_radii, np.inf)
    nonzero = sv_min != 0
    cond[nonzero] = sv_max[nonzero] / sv_min[nonzero]
    out["block_singular_values"] = sv
    out["block_singular_value_min"] = sv_min
    out["block_singular_value_max"] = sv_max
    out["block_condition_number"] = cond
    if m_not_block_diagonal:
        return ("failed_closed_solve", "assembled M is not exactly block diagonal (non-finite or nonzero "
                "off-block entries); separate block solves would not be the stated equation")

    VRH = VR.conj().T
    VZH = VZ.conj().T
    Wrho = W * rho                 # (W*rho)
    Wrho_over_R = W * rho / R      # (W*rho/R)
    for k, (c0, c1) in enumerate(ranges):
        prog["batch"] = k
        prog["block"] = None
        prog["stage"] = "assembly of B"
        # B = VR.conj().T @ ((W*rho)[:,None]*xi_R) - 1j*mode*V.conj().T @ ((W*rho/R)[:,None]*xi_phi)
        #     + VZ.conj().T @ ((W*rho)[:,None]*xi_z)          (columns c0..c1-1; W used once per term)
        X = Wrho[:, None] * np.asarray(xi_R[:, c0:c1], dtype=np.complex128)
        b_radial = np.einsum("il,lk->ik", VRH, X, optimize=False)
        X = Wrho_over_R[:, None] * np.asarray(xi_phi[:, c0:c1], dtype=np.complex128)
        b_azimuthal = (-1j * mode) * np.einsum("il,lk->ik", VH, X, optimize=False)
        X = Wrho[:, None] * np.asarray(xi_z[:, c0:c1], dtype=np.complex128)
        b_vertical = np.einsum("il,lk->ik", VZH, X, optimize=False)
        del X
        Bk = b_radial + b_azimuthal + b_vertical
        del b_radial, b_azimuthal, b_vertical
        store["B"][:, c0:c1] = Bk
        out["B_assembled_batches"].append(k)

        prog["stage"] = "block solves"
        Ck = np.empty((n_cols, c1 - c0), dtype=np.complex128)
        for i, s in enumerate(blocks):
            prog["block"] = i
            Mi = M_blocks[i]
            Bi = Bk[s]
            if not (np.all(np.isfinite(Mi)) and np.all(np.isfinite(Bi))):
                return ("failed_closed_solve", "non-finite M block or B block")
            # M coefficients = B on diagonal block i, all columns of this batch: ordinary direct solve.
            try:
                Ci = np.linalg.solve(Mi, Bi)
            except np.linalg.LinAlgError as exc:
                return ("failed_closed_solve", "singular M block (%s)" % exc)
            if not np.all(np.isfinite(Ci)):
                return ("failed_closed_solve", "non-finite block solve result")
            Ck[s] = Ci
            store["coefficients"][s, c0:c1] = Ci
            completed[i, k] = True

        prog["block"] = None
        prog["stage"] = "G, residual and mass integral"
        # G = V @ coefficients
        Gk = np.einsum("ij,jk->ik", V, Ck, optimize=False)
        # Direct residual M coefficients - B with the assembled M.
        Rk = np.einsum("ij,jk->ik", M, Ck, optimize=False) - Bk
        if not (np.all(np.isfinite(Gk)) and np.all(np.isfinite(Rk))):
            return ("failed_closed_solve", "non-finite G or residual")
        Rk_block_norm = _norm2_block_columns(Rk, n_radii, n_coeffs)
        Rk_column_norm = _norm2_columns(Rk)
        # Complex mass integral dot(W, G[:, j]) per column; unconjugated, not forced to zero.
        mass_k = np.einsum("l,lk->k", W, Gk, optimize=False)
        if not (np.all(np.isfinite(Rk_block_norm)) and np.all(np.isfinite(Rk_column_norm))
                and np.all(np.isfinite(mass_k))):
            return ("failed_closed_solve", "non-finite residual norm or mass integral")
        store["G"][:, c0:c1] = Gk
        store["residual"][:, c0:c1] = Rk
        store["residual_block_column_norm"][:, c0:c1] = Rk_block_norm
        store["residual_column_norm"][c0:c1] = Rk_column_norm
        store["mass_integral"][c0:c1] = mass_k
        out["completed_batches"].append(k)
    prog["batch"] = None
    prog["stage"] = "done"
    return None


def _project_density_map_sized(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode,
                               provenance, rhs_batch_size, n_radii, n_nodes, n_coeffs):
    """Private: same validation and arithmetic with parameterized block sizes (reduced-size test stubs only)."""
    for nm, n in (("n_radii", n_radii), ("n_nodes", n_nodes), ("n_coeffs", n_coeffs)):
        if not _is_plain_int(n) or int(n) < 1:
            return _reject(nm, "%s must be a positive int" % nm)
    n_radii, n_nodes, n_coeffs = int(n_radii), int(n_nodes), int(n_coeffs)
    try:
        rejected, arr = _validate(value=value, partial_R=partial_R, partial_z=partial_z, weights=weights,
                                  radius=radius, rho=rho, xi_R=xi_R, xi_phi=xi_phi, xi_z=xi_z, mode=mode,
                                  provenance=provenance, rhs_batch_size=rhs_batch_size, n_radii=n_radii,
                                  n_nodes=n_nodes, n_coeffs=n_coeffs)
        if rejected is not None:
            return rejected
        out = _compute(provenance=provenance, n_radii=n_radii, n_coeffs=n_coeffs, **arr)
    except Exception as exc:  # fail closed on anything unexpected outside _compute's own retention handler
        prov = provenance if isinstance(provenance, str) else None
        return _result("failed_closed_internal", "%s: %s (outside the batch arithmetic; nothing completed)"
                       % (type(exc).__name__, exc), prov)
    out["layout"] = {
        "rows": "row = %d*i + l (radius i, quadrature node l)" % n_nodes,
        "columns": "coefficient row = %d*j + a (radius j, trial coefficient a); map column = displacement map j"
                   % n_coeffs,
        "block_i": "rows %d*i..%d*i+%d, columns %d*i..%d*i+%d" % (n_nodes, n_nodes, n_nodes - 1,
                                                                n_coeffs, n_coeffs, n_coeffs - 1),
        "shape_value": (n_radii * n_nodes, n_radii * n_coeffs),
    }
    return out


def project_density_map(*, value, partial_R, partial_z, weights, radius, rho, xi_R, xi_phi, xi_z, mode,
                        provenance, rhs_batch_size):
    """Batched 0438 density projection on the 72 x (32 nodes, 8 trial coefficients) free-surface mesh (0441).

    value=V, partial_R=VR, partial_z=VZ: real finite (2304, 576); V exactly zero outside its 72 diagonal 32x8
    radial blocks (VR, VZ need not be block diagonal). weights=W, radius=R, rho: positive finite real (2304,).
    xi_R, xi_phi, xi_z: finite complex maps of identical shape (2304, nfree), nfree >= 1. mode: integer 0..8.
    provenance: non-empty str. rhs_batch_size: caller-supplied integer >= 1 (columns per batch).

    Returns a dict. status "computed": coefficients (576, nfree), G = V coefficients (2304, nfree), B (576, nfree),
    residual = M coefficients - B (576, nfree) with residual_block_column_norm (72, nfree) and
    residual_column_norm (nfree,), mass_integral = dot(W, G[:, j]) (nfree,) complex (not forced to zero),
    M_blocks (72, 8, 8) and per-block singular values / ranges / condition numbers (diagnostics, no threshold),
    plus batch bookkeeping. Otherwise status "rejected_input", "failed_closed_solve",
    "failed_closed_floating_point", "failed_closed_internal" or "interrupted"; after validation the failure
    statuses keep completed_block_batch (72, n_batches), B_assembled_batches, completed_batches, failed_stage /
    failed_batch / failed_block and partial_<key> arrays (NaN where not completed), with the primary result keys
    None. There is no physical acceptance flag.
    """
    return _project_density_map_sized(value=value, partial_R=partial_R, partial_z=partial_z, weights=weights,
                                      radius=radius, rho=rho, xi_R=xi_R, xi_phi=xi_phi, xi_z=xi_z, mode=mode,
                                      provenance=provenance, rhs_batch_size=rhs_batch_size, n_radii=N_RADII,
                                      n_nodes=N_NODES_PER_RADIUS, n_coeffs=N_COEFFS_PER_RADIUS)
