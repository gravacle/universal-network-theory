# UNT support task 0397 -- inert author implementation, v002.
# v002 applies the four Codex 0398 corrections to v001 (listed in the docstring of
# scalar_metric_particular_solve); formula, ordering, sign and scope are unchanged.
# One public function, scalar_metric_particular_solve, plus private helpers.
# numpy only. Module-level code is limited to the numpy import and function
# definitions: no constants, no work at import, no I/O, no subprocesses, no CLI.
# Written statically; never executed or imported by its author.

import numpy as np


def _real_input(name, value, failures):
    """Admit a finite real scalar as float, or record a failure and return None."""
    if isinstance(value, (bool, np.bool_)):
        failures.append(f"input {name}: a boolean is not an admitted real scalar")
        return None
    if not isinstance(value, (int, float, np.integer, np.floating)):
        failures.append(
            f"input {name}: type {type(value).__name__} is not an admitted real scalar"
        )
        return None
    try:
        out = float(value)
    except (OverflowError, ValueError, TypeError):
        failures.append(f"input {name}: not representable as a float64 value")
        return None
    if not np.isfinite(out):
        failures.append(f"input {name}: not finite ({out!r})")
        return None
    return out


def _complex_input(name, value, failures):
    """Admit a finite complex scalar as complex, or record a failure and return None."""
    if isinstance(value, (bool, np.bool_)):
        failures.append(f"input {name}: a boolean is not an admitted complex scalar")
        return None
    admitted = (int, float, complex, np.integer, np.floating, np.complexfloating)
    if not isinstance(value, admitted):
        failures.append(
            f"input {name}: type {type(value).__name__} is not an admitted complex scalar"
        )
        return None
    try:
        out = complex(value)
    except (OverflowError, ValueError, TypeError):
        failures.append(f"input {name}: not representable as a complex128 value")
        return None
    if not (np.isfinite(out.real) and np.isfinite(out.imag)):
        failures.append(f"input {name}: not finite ({out!r})")
        return None
    return out


def _complex_vector2_input(name, value, failures):
    """Admit a length-2 list/tuple or plain shape-(2,) ndarray of finite complex scalars."""
    if isinstance(value, np.ndarray):
        if type(value) is not np.ndarray:
            failures.append(
                f"input {name}: ndarray subclass {type(value).__name__} is not admitted"
            )
            return None
        if value.shape != (2,):
            failures.append(f"input {name}: array shape {value.shape!r} is not (2,)")
            return None
    elif isinstance(value, (list, tuple)):
        if len(value) != 2:
            failures.append(f"input {name}: length {len(value)} is not 2")
            return None
    else:
        failures.append(
            f"input {name}: type {type(value).__name__} is not a length-2 list, tuple or array"
        )
        return None
    out = [_complex_input(f"{name}[{i}]", value[i], failures) for i in range(2)]
    if any(v is None for v in out):
        return None
    return np.array(out, dtype=np.complex128)


def _complex_matrix2_input(name, value, failures):
    """Admit a 2x2 nested list/tuple or plain shape-(2,2) ndarray of finite complex scalars."""
    if isinstance(value, np.ndarray):
        if type(value) is not np.ndarray:
            failures.append(
                f"input {name}: ndarray subclass {type(value).__name__} is not admitted"
            )
            return None
        if value.shape != (2, 2):
            failures.append(f"input {name}: array shape {value.shape!r} is not (2, 2)")
            return None
    elif isinstance(value, (list, tuple)):
        if len(value) != 2 or any(
            not isinstance(row, (list, tuple)) or len(row) != 2 for row in value
        ):
            failures.append(f"input {name}: not a 2x2 nested list or tuple")
            return None
    else:
        failures.append(
            f"input {name}: type {type(value).__name__} is not a 2x2 list, tuple or array"
        )
        return None
    out = [
        [_complex_input(f"{name}[{i}][{j}]", value[i][j], failures) for j in range(2)]
        for i in range(2)
    ]
    if any(v is None for row in out for v in row):
        return None
    return np.array(out, dtype=np.complex128)


def _pair(z):
    return {"real": float(z.real), "imag": float(z.imag)}


def _pairs_matrix(M):
    return [[_pair(M[i, j]) for j in range(2)] for i in range(2)]


def _vector_norm(v):
    """Euclidean norm of a complex 2-vector by explicit elementwise arithmetic."""
    return float(np.sqrt(np.sum(v.real * v.real + v.imag * v.imag)))


def _nonfinite_entries(name, Z):
    """Name each non-finite part of a complex array as 'name[i][j] part kind'."""
    out = []
    for index in np.ndindex(Z.shape):
        label = name + "".join(f"[{n}]" for n in index)
        for part, x in (("real", Z[index].real), ("imag", Z[index].imag)):
            if not np.isfinite(x):
                out.append(f"{label} {part} {'nan' if np.isnan(x) else 'inf'}")
    return out


def _nonfinite_scalars(named):
    """Name each non-finite (name, float) pair as 'name (kind)'; None is skipped."""
    return [
        f"{n} ({'nan' if np.isnan(v) else 'inf'})"
        for n, v in named
        if v is not None and not np.isfinite(v)
    ]


def _new_result():
    return {
        "ok": False,
        "stage_reached": None,
        "failures": [],
        "flags": [],
        "ill_conditioned": None,
        "q_order": ["n", "psi"],
        "q": None,
        "K0": None,
        "A": None,
        "diagnostics": None,
        "inputs": None,
        "units": (
            "c = 1 in one consistent normalization chosen by the caller: k and z (time "
            "frequency) share one inverse-length unit; G_EH, Pi_eff and F_eff are in the "
            "matching normalization of the action (K0 has the units of k^2/G_EH; F_eff is "
            "the source covector with A q = -F_eff); q = (n, psi) are dimensionless metric "
            "potentials. No unit conversion is performed."
        ),
        "sign_convention": (
            "signature (-+++), ds^2 = -(1+2n)dt^2 + (1-2psi)dx^2, Fourier "
            "exp(-i omega t + i k.x), z = omega + i0 (Im z >= 0). "
            "K0 = (4 pi G_EH)^-1 [[0, -k^2], [-k^2, k^2 - 3 z^2]], A = K0 + Pi_eff, "
            "A q = -F_eff, so q_particular = -A^-1 F_eff = G F_eff with G = -A^-1; the "
            "ordinary part of F_eff is F_b = (-epsilon, -T_ii) and F_eff = F_b + ell_eff."
        ),
        "scope": (
            "translation-stationary scalar branch, particular solution only. Excluded: "
            "homogeneous, boundary/initial-data and k = 0 modes, general nonstationary "
            "convolution, and retained-block elimination (Pi_eff and F_eff are supplied "
            "already eliminated). Pi_eff is a correctly matched residual ACTION Hessian, "
            "not a raw susceptibility; F_eff already contains the ordinary and retained "
            "first derivatives in the reviewed sign convention. G_EH is not equated to "
            "laboratory G. No galaxy data, fit parameters or 43 velocities are computed "
            "here. cond_tol only flags finite ill-conditioning; it is not a physical "
            "acceptance rule. An exactly singular A (LU failure or s_min == 0) is a "
            "failure."
        ),
    }


def scalar_metric_particular_solve(*, k, z, G_EH, Pi_eff, F_eff, cond_tol):
    """Particular solution q = (n, psi) of (K0 + Pi_eff) q = -F_eff on the scalar branch.

    Version v002. The v001 formula, ordering, sign, scope and output keys are kept.
    Four corrections from Codex 0398 (REVIEW_0397_V001 F1, F2, F4, F5) are applied:
      1. s_min == 0 from the SVD is rejected as singular (failure, ok False) even
         when numpy.linalg.solve returned. A finite cond_2 > cond_tol stays a
         report-only flag that does not change ok.
      2. ndarray subclasses (e.g. np.matrix) are rejected for Pi_eff and F_eff, so
         an admitted array is a plain ndarray and chained indexing cannot escape.
      3. residual_norm, F_norm, q_norm, s_max, s_min, s_max*q_norm, cond_2 and each
         non-None relative residual are checked. Any non-finite one is the failure
         "diagnostics: unrepresentable ..." (stage 'diagnostics', ok False) and the
         diagnostics field stays None, so an overflow can never read as a zero
         residual or as a finite cond_2.
      4. K0 and A after assembly, and q after the solve, are finite-checked before
         they are packaged. A non-finite array is left None and its entries (index,
         part, nan or inf) are named in the failure. Nothing is replaced by zero.

    Sources (read-only):
      * Task: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
        0397_2026-10-15_scalar_metric_particular_solver.md
      * Corrections: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
        0398_2026-10-15_scalar_solver_review_corrections.md
      * Frozen formula: helpers/coefficient_method/
        EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_PROPOSED_V001.md (sha256 f5e28809...)
      * Distinct review: helpers/response_packet_audit/
        EH_RETAINED_SCALAR_METRIC_DYSON_SYSTEM_DISTINCT_REVIEW_V001.json (PASS_SCOPED)

    Definition (c = 1, q = (n, psi) in that order):
      K0 = (4 pi G_EH)^-1 [[0, -k^2], [-k^2, k^2 - 3 z^2]],  A = K0 + Pi_eff,
      solve A q = -F_eff  (q = -A^-1 F_eff = G F_eff, G = -A^-1).
    A is used exactly as assembled: never symmetrized, Hermitized, projected to real
    parts, clipped or regularized; no pseudoinverse.

    Arguments (keyword-only, required, no defaults):
      k: finite real > 0.  z: finite complex, Im(z) >= 0.  G_EH: finite real > 0.
      Pi_eff: finite complex 2x2 (nested list/tuple or plain shape-(2,2) ndarray).
      F_eff: finite complex length-2 (list/tuple or plain shape-(2,) ndarray).
      cond_tol: finite real > 0, the caller's threshold for FLAGGING ill-conditioning.
    Booleans, ndarray subclasses, other shapes and non-finite values are rejected.

    Returns a plain dict. "ok" is True only if inputs are admitted, K0 and A are
    finite, numpy.linalg.solve succeeds (exact singularity raises LinAlgError and is
    reported as a failure), q is finite, the smallest singular value of A is > 0, and
    every diagnostic is finite. A field is filled only with finite values: a
    non-finite K0, A or q stays None, and diagnostics stays None unless all of its
    values are finite. If the finite 2-norm condition number exceeds cond_tol,
    "ill_conditioned" is True and a flag is recorded, but ok is NOT changed: cond_tol
    is reported, never a physical acceptance rule, and the caller must decide
    explicitly before using such a result. When ok is False, every populated field is
    failure evidence only. Complex values are {"real", "imag"} fields. Diagnostics:
    residual A q + F_eff (einsum, optimize=False), its 2-norm, relative to |F_eff|
    and to ||A||_2 |q| (each None only when its denominator is exactly 0), the
    singular values of A (numpy.linalg.svd, compute_uv=False; a LAPACK call, not a
    matrix product) and cond_2 = s_max / s_min.

    Scope: translation-stationary scalar branch, particular solution only; no
    homogeneous, boundary or k = 0 modes, nonstationary convolution or retained-block
    elimination. Pi_eff is a matched residual ACTION Hessian, not a raw
    susceptibility. F_eff = F_b + ell_eff in the reviewed sign convention. G_EH is
    not laboratory G. No 43 velocities, galaxy data or fit parameters. Warnings are
    not suppressed.
    """
    result = _new_result()
    failures = result["failures"]

    # ---- Stage 1: admission ---------------------------------------------------
    result["stage_reached"] = "inputs"
    k_in = _real_input("k", k, failures)
    z_in = _complex_input("z", z, failures)
    G_in = _real_input("G_EH", G_EH, failures)
    Pi_in = _complex_matrix2_input("Pi_eff", Pi_eff, failures)
    F_in = _complex_vector2_input("F_eff", F_eff, failures)
    tol_in = _real_input("cond_tol", cond_tol, failures)
    if k_in is not None and not k_in > 0.0:
        failures.append(f"input k: must be > 0, got {k_in!r}")
    if z_in is not None and not z_in.imag >= 0.0:
        failures.append(f"input z: Im(z) = {z_in.imag!r} is negative")
    if G_in is not None and not G_in > 0.0:
        failures.append(f"input G_EH: must be > 0, got {G_in!r}")
    if tol_in is not None and not tol_in > 0.0:
        failures.append(f"input cond_tol: must be > 0, got {tol_in!r}")
    result["inputs"] = {
        "k": k_in,
        "z": None if z_in is None else _pair(z_in),
        "G_EH": G_in,
        "Pi_eff": None if Pi_in is None else _pairs_matrix(Pi_in),
        "F_eff": None if F_in is None else [_pair(F_in[i]) for i in range(2)],
        "cond_tol": tol_in,
    }
    if failures:
        return result

    # ---- Stage 2: assembly A = K0 + Pi_eff (no symmetrization or projection) --
    result["stage_reached"] = "assembly"
    zc = np.complex128(z_in)
    k2 = np.float64(k_in) * np.float64(k_in)
    prefactor = 1.0 / (4.0 * np.pi * np.float64(G_in))
    K0 = np.array(
        [
            [prefactor * 0.0, prefactor * (-k2)],
            [prefactor * (-k2), prefactor * (k2 - 3.0 * zc * zc)],
        ],
        dtype=np.complex128,
    )
    A = K0 + Pi_in
    # Finite admission before packaging: a non-finite array stays None.
    K0_bad = _nonfinite_entries("K0", K0)
    A_bad = _nonfinite_entries("A", A)
    result["K0"] = None if K0_bad else _pairs_matrix(K0)
    result["A"] = None if A_bad else _pairs_matrix(A)
    if K0_bad:
        failures.append("assembly: K0 left None; non-finite " + ", ".join(K0_bad))
    if A_bad:
        failures.append("assembly: A left None; non-finite " + ", ".join(A_bad))
    if failures:
        return result

    # ---- Stage 3: solve A q = -F_eff ------------------------------------------
    result["stage_reached"] = "solve"
    rhs = -F_in
    try:
        q = np.linalg.solve(A, rhs)
    except np.linalg.LinAlgError as exc:
        failures.append(f"solve: A is singular to working precision ({exc})")
        return result
    # Finite admission before packaging: a non-finite q stays None.
    q_bad = _nonfinite_entries("q", q)
    if q_bad:
        failures.append("solve: q left None; non-finite " + ", ".join(q_bad))
        return result
    result["q"] = [_pair(q[i]) for i in range(2)]

    # ---- Stage 4: residual and conditioning diagnostics -----------------------
    # Every value is checked before diagnostics is packaged; on any failure here
    # diagnostics stays None. A finite residual_norm implies a finite residual.
    result["stage_reached"] = "diagnostics"
    residual = np.einsum("ij,j->i", A, q, optimize=False) + F_in
    residual_norm = _vector_norm(residual)
    F_norm = _vector_norm(F_in)
    q_norm = _vector_norm(q)
    try:
        singular_values = np.linalg.svd(A, compute_uv=False)
    except np.linalg.LinAlgError as exc:
        failures.append(f"diagnostics: singular values of A did not converge ({exc})")
        return result
    s_max = float(singular_values[0])
    s_min = float(singular_values[-1])
    scale_Aq = s_max * q_norm
    unrepresentable = _nonfinite_scalars(
        [
            ("residual_norm", residual_norm),
            ("F_norm", F_norm),
            ("q_norm", q_norm),
            ("s_max", s_max),
            ("s_min", s_min),
            ("s_max*q_norm", scale_Aq),
        ]
    )
    singular = bool(np.isfinite(s_min)) and not s_min > 0.0
    if singular:
        failures.append(
            f"diagnostics: A is singular: smallest singular value s_min = {s_min!r} "
            "although numpy.linalg.solve returned; rejected (no pseudoinverse, "
            "regularization or cutoff); the q above is failure evidence, not a solution"
        )
    cond_2 = None
    relative_to_F = None
    relative_to_Aq = None
    if not unrepresentable and not singular:
        cond_2 = s_max / s_min
        relative_to_F = residual_norm / F_norm if F_norm != 0.0 else None
        relative_to_Aq = residual_norm / scale_Aq if scale_Aq != 0.0 else None
        unrepresentable = _nonfinite_scalars(
            [
                ("cond_2", cond_2),
                ("relative_residual_to_F", relative_to_F),
                ("relative_residual_to_A_norm_q_norm", relative_to_Aq),
            ]
        )
    if unrepresentable:
        failures.append(
            "diagnostics: unrepresentable " + ", ".join(unrepresentable)
            + "; diagnostics left None (no value is reported as finite)"
        )
    if failures:
        return result
    result["diagnostics"] = {
        "residual": [_pair(residual[i]) for i in range(2)],
        "residual_norm": residual_norm,
        "F_norm": F_norm,
        "q_norm": q_norm,
        "relative_residual_to_F": relative_to_F,
        "relative_residual_to_A_norm_q_norm": relative_to_Aq,
        "singular_values": [s_max, s_min],
        "A_norm_2": s_max,
        "cond_2": cond_2,
        "cond_tol": tol_in,
    }
    ill = not cond_2 <= tol_in
    result["ill_conditioned"] = ill
    if ill:
        result["flags"].append(
            f"ill_conditioned: cond_2 = {cond_2!r} exceeds cond_tol = {tol_in!r} "
            "(reported only; not a physical acceptance rule; the caller must decide "
            "explicitly before any use)"
        )

    result["ok"] = True
    result["stage_reached"] = "complete"
    return result
