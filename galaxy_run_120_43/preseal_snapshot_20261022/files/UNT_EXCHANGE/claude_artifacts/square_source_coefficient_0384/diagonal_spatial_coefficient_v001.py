# UNT support task 0387 -- inert author implementation, v001.
# One public function, diagonal_spatial_coefficient, plus private helpers.
# Helpers are copied (not imported) from the 0384/0385 modules in this directory,
# so this module is self-contained. Module-level code is limited to the numpy
# import and function definitions: no constants, no work at import, no I/O,
# no subprocesses, no CLI. Written statically; never executed or imported by its author.

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


def _tolerance_input(name, value, failures):
    """Admit an explicit finite tolerance >= 0, or record a failure and return None."""
    out = _real_input(name, value, failures)
    if out is None:
        return None
    if not out >= 0.0:
        failures.append(f"tolerance {name}: must be >= 0, got {out!r}")
        return None
    return out


def _sigma_input(name, value, failures):
    """Admit a tuple of length 1 or 2 whose entries are integers exactly +1 or -1."""
    if not isinstance(value, tuple):
        failures.append(f"input {name}: type {type(value).__name__} is not a tuple")
        return None
    if len(value) not in (1, 2):
        failures.append(f"input {name}: length {len(value)} is not 1 or 2")
        return None
    out = []
    for k in range(len(value)):
        item = value[k]
        if isinstance(item, (bool, np.bool_)) or not isinstance(item, (int, np.integer)):
            failures.append(
                f"input {name}[{k}]: type {type(item).__name__} is not an integer +1 or -1"
            )
            return None
        if int(item) not in (-1, 1):
            failures.append(f"input {name}[{k}]: value {int(item)!r} is not +1 or -1")
            return None
        out.append(int(item))
    return tuple(out)


def _real_vector_input(name, value, lengths, failures):
    """Admit a finite real list, tuple or 1-D array whose length is in `lengths`.

    Scalars, other shapes, other container types and non-real elements are
    rejected. Nothing is broadcast, coerced or repaired.
    """
    if isinstance(value, np.ndarray):
        if value.ndim != 1 or value.shape[0] not in lengths:
            failures.append(
                f"input {name}: array shape {value.shape!r} is not one of "
                f"{[(n,) for n in lengths]!r}"
            )
            return None
    elif isinstance(value, (list, tuple)):
        if len(value) not in lengths:
            failures.append(f"input {name}: length {len(value)} is not one of {list(lengths)!r}")
            return None
    else:
        failures.append(
            f"input {name}: type {type(value).__name__} is not a list, tuple or 1-D array"
        )
        return None
    out = []
    admitted = True
    for k in range(len(value)):
        item = _real_input(f"{name}[{k}]", value[k], failures)
        if item is None:
            admitted = False
        out.append(item)
    if not admitted:
        return None
    return tuple(out)


def _local_block(ER, ES, epsilon_c, epsilon_r, lambda_J, lambda_R, g, kappa, d):
    """H(d) in the ordered local basis (A0, A1, B0, B1), exactly as displayed in 0384."""
    r_d = epsilon_r - lambda_R * d
    b_d = ES + epsilon_c + lambda_J * d
    kappa_c = kappa.conjugate()
    return np.array(
        [
            [ER, 0.0, kappa_c, 0.0],
            [0.0, ER + r_d, 0.0, kappa_c],
            [kappa, 0.0, b_d, g],
            [0.0, kappa, g, b_d + r_d],
        ],
        dtype=np.complex128,
    )


def _site_spec(n_sites, axis):
    """einsum spec contracting mat[k, m] into site axis `axis` of an n-site tensor (n = 2, 3)."""
    if n_sites not in (2, 3) or axis not in range(n_sites):
        raise ValueError(f"unsupported site tensor: n_sites={n_sites!r}, axis={axis!r}")
    letters = "abc"[:n_sites]
    src = letters[:axis] + "m" + letters[axis + 1:]
    dst = letters[:axis] + "k" + letters[axis + 1:]
    return f"km,{src}->{dst}"


def _site_apply(mat, f, axis):
    """new[..k..] = sum_m mat[k, m] f[..m..] on site axis `axis` of a (4,)*n tensor."""
    return np.einsum(_site_spec(f.ndim, axis), mat, f, optimize=False)


def _to_eigenbasis(f, uh_sites):
    """Site by site, apply conj(U_v)^T on site axis v (local basis -> product eigenbasis)."""
    out = f
    for axis in range(len(uh_sites)):
        out = _site_apply(uh_sites[axis], out, axis)
    return out


def _from_eigenbasis(t, u_sites):
    """Site by site, apply U_v on site axis v (product eigenbasis -> local basis)."""
    out = t
    for axis in range(len(u_sites)):
        out = _site_apply(u_sites[axis], out, axis)
    return out


def _contract(bra, ket):
    """sum over all site indices of bra * ket (bra already conjugated)."""
    if bra.ndim == 2:
        spec = "ab,ab->"
    elif bra.ndim == 3:
        spec = "abc,abc->"
    else:
        raise ValueError(f"unsupported site tensor rank {bra.ndim!r}")
    return np.einsum(spec, bra, ket, optimize=False)


def _kron_sum_denominator(c, shifts):
    """c + sum_v shifts[v][k_v] on the (4,)*n product index, n = 2 or 3 (broadcast sum)."""
    if len(shifts) == 2:
        return c + shifts[0][:, np.newaxis] + shifts[1][np.newaxis, :]
    if len(shifts) == 3:
        return (
            c
            + shifts[0][:, np.newaxis, np.newaxis]
            + shifts[1][np.newaxis, :, np.newaxis]
            + shifts[2][np.newaxis, np.newaxis, :]
        )
    raise ValueError(f"unsupported number of sites {len(shifts)!r}")


def _apply_resolvent_jet(f, fp, fpp, entry):
    """One R_S = M_S^-1 (positive inverse) on the directional jet (f, f', f'').

    R' = b R^2 and R'' = 2 b^2 R^3 with b = b_S, so
      new_f   = R f
      new_fp  = b R^2 f + R f'
      new_fpp = 2 b^2 R^3 f + 2 b R^2 f' + R f''.
    Powers of R are repeated elementwise division by the same denominator array
    in the complete product eigenbasis of M_S.
    """
    den = entry["den"]
    b = entry["b"]
    uh_sites = entry["uh_sites"]
    t = _to_eigenbasis(f, uh_sites)
    tp = _to_eigenbasis(fp, uh_sites)
    tpp = _to_eigenbasis(fpp, uh_sites)
    r1 = t / den
    r2 = r1 / den
    r3 = r2 / den
    r1p = tp / den
    r2p = r1p / den
    r1pp = tpp / den
    new_f = r1
    new_fp = b * r2 + r1p
    new_fpp = (2.0 * b * b) * r3 + (2.0 * b) * r2p + r1pp
    u_sites = entry["u_sites"]
    return (
        _from_eigenbasis(new_f, u_sites),
        _from_eigenbasis(new_fp, u_sites),
        _from_eigenbasis(new_fpp, u_sites),
    )


def _apply_reference_jet(f, fp, fpp, ref):
    """R0 = Q0 (M_empty restricted to Q0)^-1 Q0 on the jet; R0' = R0'' = 0.

    In the product eigenbasis of H(2) at every site, Q0 removes only the all-chi
    index (0,...,0); every other component is divided by its M_empty denominator.
    """
    keep = ref["keep"]
    den = ref["den"]
    out = []
    for x in (f, fp, fpp):
        t = _to_eigenbasis(x, ref["uh_sites"])
        q = np.zeros(t.shape, dtype=np.complex128)
        q[keep] = t[keep] / den[keep]
        out.append(_from_eigenbasis(q, ref["u_sites"]))
    return out[0], out[1], out[2]


def _ordered_chain(steps, omega, omega_bra, zero):
    """<Omega| X_k ... X_2 X_1 |Omega> and its two directional derivatives.

    steps[0] acts first on |Omega>. Each step is ("R", entry) or ("R0", ref);
    the exact ordered operator product rule is carried by the jet.
    """
    f, fp, fpp = omega, zero, zero
    for kind, entry in steps:
        if kind == "R":
            f, fp, fpp = _apply_resolvent_jet(f, fp, fpp, entry)
        elif kind == "R0":
            f, fp, fpp = _apply_reference_jet(f, fp, fpp, entry)
        else:
            raise ValueError(f"unknown chain step {kind!r}")
    return (
        complex(_contract(omega_bra, f)),
        complex(_contract(omega_bra, fp)),
        complex(_contract(omega_bra, fpp)),
    )


def _moments(omega, entry, m_max):
    """r_m = <Omega|R_S^m|Omega> for m = 1..m_max, as sum_k conj(t_k) t_k / den_k^m, t = U^dagger Omega."""
    t = _to_eigenbasis(omega, entry["uh_sites"])
    t_bra = np.conj(t)
    out = {}
    q = t
    for m in range(1, m_max + 1):
        q = q / entry["den"]
        out[m] = complex(_contract(t_bra, q))
    return out


def _moment_jets(r, b):
    """(r_1, r_1', r_1'') and (r_2, r_2', r_2'') from r_m' = m b r_(m+1), r_m'' = m(m+1) b^2 r_(m+2)."""
    r1 = (r[1], 1.0 * b * r[2], 2.0 * b * b * r[3])
    r2 = (r[2], 2.0 * b * r[3], 6.0 * b * b * r[4])
    return r1, r2


def _product_jet(x, y):
    """Scalar product rule: (xy, x'y + xy', x''y + 2x'y' + xy'')."""
    return (
        x[0] * y[0],
        x[1] * y[0] + x[0] * y[1],
        x[2] * y[0] + 2.0 * x[1] * y[1] + x[0] * y[2],
    )


def _jet_add(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2])


def _jet_sub(x, y):
    return (x[0] - y[0], x[1] - y[1], x[2] - y[2])


def _pair(z):
    return (float(z.real), float(z.imag))


def _jet_pairs(x):
    return {"value": _pair(x[0]), "first": _pair(x[1]), "second": _pair(x[2])}


def _new_result():
    return {
        "ok": False,
        "stage_reached": None,
        "failures": [],
        "case": None,
        "d": None,
        "dprime": None,
        "dsecond": None,
        "raw_sums": None,
        "fold": None,
        "chain_double_flip": None,
        "chain_restored": None,
        "chain_histories": None,
        "moments": None,
        "max_abs_imag": None,
        "max_abs_imag_components": None,
        "min_used_denominator": None,
        "reference_gap": None,
        "removed_reference_denominator": None,
        "local_gap": None,
        "e2": None,
        "local_degrees": None,
        "local_spectra": None,
        "eigen_residual": None,
        "eigenvector_orthonormality_residual": None,
        "hermiticity_residual": None,
        "r2": None,
        "mu0": None,
        "delta": None,
        "subsets": None,
        "declared_inputs": None,
        "declared_tolerances": None,
        "units": {
            "d": "E^-3",
            "dprime": "E^-4",
            "dsecond": "E^-5",
            "j_vec": "E",
            "c_vec": "dimensionless",
            "t": "E",
        },
        "static_notes": [
            "Coefficient multiplying h^4, canonical Hermitian convention with POSITIVE "
            "inverses. One edge e=(0,1): d_e = r2_e r1_e - <R_e R0 R_e>. Adjacent edges "
            "e=(0,1), f=(1,2): d_ef = r2_e r1_f + r2_f r1_e - <(R_e+R_f) R_ef (R_e+R_f)> "
            "- <R_f R0 R_e + R_e R0 R_f>. Unit fold factors; no extra factor of 2.",
            "All operators of a call act on the same union support (2 or 3 sites); in the "
            "adjacent case R_e carries K_2 on site 2 and R_f carries K_0 on site 0.",
            "M_S = [Ud D + mu0 sum a_v - 4 sum j_v a_v^2] I + sum_v (H_v(2 + a_v) - e2 I_v), "
            "using K_v + a_v V_v = H_v(2 + a_v) - e2 I_v with H(d) built from the 0384 formula.",
            "R0 = Q0 (M_empty|Q0)^-1 Q0 removes only the all-chi product index; it is "
            "source independent (R0' = R0'' = 0).",
            "Directional derivatives along j_vec -> j_vec + t c_vec: b_S = 4 sum_v c_v a_v^2, "
            "R_S' = b_S R_S^2, R_S'' = 2 b_S^2 R_S^3, r_m' = m b r_(m+1), "
            "r_m'' = m(m+1) b^2 r_(m+2); ordered operator product rule for chains, scalar "
            "product rule for folds.",
            "No sign gate: d, dprime and dsecond may be negative.",
            "Not implemented by design: vertex-disjoint pairs (cancel analytically), degree "
            "counts, global sums over edges or pairs, galaxy sums.",
        ],
        "scope": (
            "local finite-order (h^4) pure-flip diagonal coefficient only; no physical "
            "ground, geometry or calibration selected; the complete spatial response also "
            "contains lower-order contacts, state response, the separate square and Birth "
            "operators, all separately retained terms and a controlled remainder"
        ),
    }


def diagonal_spatial_coefficient(
    *,
    ER,
    ES,
    epsilon_c,
    epsilon_r,
    lambda_J,
    lambda_R,
    g,
    kappa,
    Delta,
    Ud,
    dstar,
    sigma,
    j_vec,
    c_vec,
    ref_tol,
    pos_tol,
    herm_tol,
    resid_tol,
    imag_tol,
):
    """Local pure-flip fourth-order diagonal coefficient d and its directional derivatives.

    Sources (read-only):
      * Formula authority: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
        0387_2026-10-15_diagonal_spatial_coefficient_inert_implementation.md
      * Local block, reference checks and fail-closed structure copied from:
        /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/square_source_coefficient_0384/
        square_source_coefficient_v001.py (0384) and square_spatial_source_v001.py (0385).

    Definition (0387):
      H(d) = [[ER, 0, conj(kappa), 0], [0, ER + r_d, 0, conj(kappa)],
              [kappa, 0, ES + epsilon_c + lambda_J d, g],
              [0, kappa, g, ES + epsilon_c + lambda_J d + r_d]], r_d = epsilon_r - lambda_R d,
      for every needed d = 2 + a_v in 0..4. chi, e2: unique lowest eigenpair of H(2);
      K = H(2) - e2 I; V = diag(0, -lambda_R, lambda_J, lambda_J - lambda_R);
      mu0 = Delta/2 + 2 Ud (2 - dstar); Omega = chi^(tensor n), n = len(sigma) + 1.
      sigma = (sigma_e,) for e = (0,1), or (sigma_e, sigma_f) for e = (0,1), f = (1,2):
      initial flip increments, each exactly +1 or -1.
      For S in {e}, {f}, {e,f}: a_v = sum of selected incident sigma, D = sum a_v^2,
      M_S = [Ud D + mu0 sum_v a_v - 4 sum_v j_v a_v^2] I + sum_v (K_v + a_v V_v),
      R_S = M_S^-1. M_empty = sum_v K_v, Q0 = I - |Omega><Omega|,
      R0 = Q0 (M_empty|Q0)^-1 Q0. r_m,S = <Omega|R_S^m|Omega>.
        one edge:  d_e  = r2_e r1_e - <R_e R0 R_e>
        adjacent:  d_ef = r2_e r1_f + r2_f r1_e - <(R_e+R_f) R_ef (R_e+R_f)>
                          - <R_f R0 R_e + R_e R0 R_f>
      Directional derivatives along j_vec -> j_vec + t c_vec (t in E, c dimensionless):
      b_S = 4 sum_v c_v a_v^2, R_S' = b_S R_S^2, R_S'' = 2 b_S^2 R_S^3, R0' = R0'' = 0,
      r_m' = m b r_(m+1), r_m'' = m(m+1) b^2 r_(m+2).
      Units: d E^-3, dprime E^-4, dsecond E^-5.

    Inputs: every argument is keyword-only and required; there are no defaults.
    sigma must be a tuple of length 1 or 2 with integer entries exactly +1 or -1.
    j_vec and c_vec must be finite real lists, tuples or 1-D arrays of length
    len(sigma) + 1 (site order 0, 1[, 2]); nothing is broadcast.
    Tolerances: ref_tol (|r2| <= ref_tol, r2 = epsilon_r - 2 lambda_R), pos_tol
    (local H(2) gap, every M_S denominator and every retained R0 denominator must
    exceed it), herm_tol (max |H - H^dagger|), resid_tol (max |H U - U diag(w)|
    and max |U^dagger U - I| over every computed block), imag_tol
    (|Im X| <= imag_tol * max(1, |Re X|) for X = d, dprime, dsecond).

    Fail closed: returns a plain dict. "ok" is True only if every check passes;
    then d, dprime and dsecond hold the checked real parts, whatever their sign.
    Otherwise they are None, "failures" lists every violated check and
    "stage_reached" names where the computation stopped. Raw complex values of
    the totals, the fold, the chain terms, every chain history and the moments
    are reported as (real, imag) pairs once computed.

    Working arrays: (4,)*n complex128 site tensors (at most 64 entries for n = 3),
    4x4 local blocks and (4,)*n float64 denominator arrays. No 64x64 (or 16x16)
    matrix is formed and no M_S is diagonalized as a whole. All contractions and
    basis transforms use numpy.einsum(..., optimize=False); the 4x4 blocks use
    numpy.linalg.eigh.

    Scope: local finite-order coefficient only; no physical ground, geometry or
    calibration; not the complete spatial response.
    """
    result = _new_result()
    failures = result["failures"]

    # ---- Stage 1: declared inputs, sign pattern, vectors and tolerances -------
    result["stage_reached"] = "inputs"
    real_given = (
        ("ER", ER),
        ("ES", ES),
        ("epsilon_c", epsilon_c),
        ("epsilon_r", epsilon_r),
        ("lambda_J", lambda_J),
        ("lambda_R", lambda_R),
        ("g", g),
        ("Delta", Delta),
        ("Ud", Ud),
        ("dstar", dstar),
    )
    x = {}
    for name, value in real_given:
        x[name] = _real_input(name, value, failures)
    kap = _complex_input("kappa", kappa, failures)
    sig = _sigma_input("sigma", sigma, failures)
    lengths = (2, 3) if sig is None else (len(sig) + 1,)
    jv = _real_vector_input("j_vec", j_vec, lengths, failures)
    cv = _real_vector_input("c_vec", c_vec, lengths, failures)
    tol_given = (
        ("ref_tol", ref_tol),
        ("pos_tol", pos_tol),
        ("herm_tol", herm_tol),
        ("resid_tol", resid_tol),
        ("imag_tol", imag_tol),
    )
    tol = {}
    for name, value in tol_given:
        tol[name] = _tolerance_input(name, value, failures)
    declared = dict(x)
    declared["kappa"] = None if kap is None else (kap.real, kap.imag)
    declared["sigma"] = None if sig is None else list(sig)
    declared["j_vec"] = None if jv is None else list(jv)
    declared["c_vec"] = None if cv is None else list(cv)
    result["declared_inputs"] = declared
    result["declared_tolerances"] = dict(tol)
    if failures:
        return result

    ER = x["ER"]
    ES = x["ES"]
    epsilon_c = x["epsilon_c"]
    epsilon_r = x["epsilon_r"]
    lambda_J = x["lambda_J"]
    lambda_R = x["lambda_R"]
    g = x["g"]
    Delta = x["Delta"]
    Ud = x["Ud"]
    dstar = x["dstar"]
    kappa = kap
    ref_tol = tol["ref_tol"]
    pos_tol = tol["pos_tol"]
    herm_tol = tol["herm_tol"]
    resid_tol = tol["resid_tol"]
    imag_tol = tol["imag_tol"]

    # ---- Stage 2: declared reference and degree condition (as 0384) ----------
    result["stage_reached"] = "reference"
    r2 = epsilon_r - 2.0 * lambda_R
    mu0 = Delta / 2.0 + 2.0 * Ud * (2.0 - dstar)
    delta = Ud - max(
        abs(mu0),
        abs(mu0 + lambda_J),
        abs(mu0 - lambda_R),
        abs(mu0 + lambda_J - lambda_R),
    )
    result["r2"] = r2
    result["mu0"] = mu0
    result["delta"] = delta
    if not (np.isfinite(r2) and np.isfinite(mu0) and np.isfinite(delta)):
        failures.append("reference: r2, mu0 or delta is not finite")
    if not abs(r2) <= ref_tol:
        failures.append(f"reference: |r2| = {abs(r2)!r} exceeds ref_tol = {ref_tol!r}")
    if not g > 0.0:
        failures.append(f"reference: g = {g!r} is not > 0")
    if kappa == 0:
        failures.append("reference: kappa is zero")
    if not delta > 0.0:
        failures.append(f"reference: delta = {delta!r} is not > 0")
    if failures:
        return result

    # ---- Stage 3: support, subsets S, a-vectors and needed local degrees -------
    result["stage_reached"] = "support"
    n_sites = len(sig) + 1
    if n_sites == 2:
        result["case"] = "one_edge"
        edge_ends = {"e": (0, 1)}
        edge_sigma = {"e": sig[0]}
        subset_defs = (("e", ("e",)),)
    else:
        result["case"] = "adjacent_edges"
        edge_ends = {"e": (0, 1), "f": (1, 2)}
        edge_sigma = {"e": sig[0], "f": sig[1]}
        subset_defs = (("e", ("e",)), ("f", ("f",)), ("ef", ("e", "f")))
    shapes = {}
    for label, selected in subset_defs:
        a = [0] * n_sites
        for edge in selected:
            for site in edge_ends[edge]:
                a[site] += edge_sigma[edge]
        shapes[label] = (selected, tuple(a))
    degrees = {2}
    for label in shapes:
        for av in shapes[label][1]:
            degrees.add(2 + av)
    degrees = tuple(sorted(degrees))
    result["local_degrees"] = list(degrees)
    if any(dd not in (0, 1, 2, 3, 4) for dd in degrees):
        failures.append(f"support: local degrees {degrees!r} outside 0..4")
        return result

    # ---- Stage 4: complete local eigensystems of every needed H(d) ------------
    result["stage_reached"] = "local_blocks"
    blocks = {}
    for dd in degrees:
        H = _local_block(
            ER, ES, epsilon_c, epsilon_r, lambda_J, lambda_R, g, kappa, float(dd)
        )
        if not np.all(np.isfinite(H)):
            failures.append(f"local: H({dd}) has a non-finite entry")
            continue
        try:
            w, U = np.linalg.eigh(H, UPLO="L")
        except np.linalg.LinAlgError as exc:
            failures.append(f"local: eigh of H({dd}) failed ({exc})")
            continue
        if not (np.all(np.isfinite(w)) and np.all(np.isfinite(U))):
            failures.append(f"local: eigensystem of H({dd}) is not finite")
            continue
        blocks[dd] = (H, w, U)
    if failures:
        return result

    eye4 = np.eye(4, dtype=np.complex128)
    herm_list = []
    resid_list = []
    ortho_list = []
    spectra = {}
    for dd in degrees:
        H, w, U = blocks[dd]
        herm_list.append(np.max(np.abs(H - np.conj(H).T)))
        HU = np.einsum("mn,nk->mk", H, U, optimize=False)
        resid_list.append(np.max(np.abs(HU - U * w[np.newaxis, :])))
        UhU = np.einsum("mk,ml->kl", np.conj(U), U, optimize=False)
        ortho_list.append(np.max(np.abs(UhU - eye4)))
        spectra[f"H({dd})"] = [float(v) for v in w]
    herm = float(np.max(np.array(herm_list)))
    resid = float(np.max(np.array(resid_list)))
    ortho = float(np.max(np.array(ortho_list)))
    w2 = blocks[2][1]
    e2 = float(w2[0])
    gap = float(w2[1] - w2[0])
    chi = blocks[2][2][:, 0]
    result["hermiticity_residual"] = herm
    result["eigen_residual"] = resid
    result["eigenvector_orthonormality_residual"] = ortho
    result["local_spectra"] = spectra
    result["e2"] = e2
    result["local_gap"] = gap
    if not herm <= herm_tol:
        failures.append(f"local: Hermiticity residual {herm!r} exceeds herm_tol {herm_tol!r}")
    if not resid <= resid_tol:
        failures.append(f"local: eigen residual {resid!r} exceeds resid_tol {resid_tol!r}")
    if not ortho <= resid_tol:
        failures.append(
            f"local: eigenvector orthonormality residual {ortho!r} exceeds resid_tol {resid_tol!r}"
        )
    if not gap > pos_tol:
        failures.append(
            f"local: H(2) gap {gap!r} does not exceed pos_tol {pos_tol!r} (lowest level not unique)"
        )
    if failures:
        return result

    # ---- Stage 5: M_S denominators and the reduced reference inverse R0 --------
    result["stage_reached"] = "operators"
    entries = {}
    subset_report = []
    for label, selected in subset_defs:
        a = shapes[label][1]
        D = sum(av * av for av in a)
        sum_a = sum(a)
        weights = tuple(4.0 * av * av for av in a)
        source_shift = sum(jv[v] * weights[v] for v in range(n_sites))
        c = Ud * D + mu0 * sum_a - source_shift
        b = sum(cv[v] * weights[v] for v in range(n_sites))
        den = _kron_sum_denominator(c, [blocks[2 + av][1] - e2 for av in a])
        finite = bool(np.all(np.isfinite(den)))
        min_den = float(np.min(den))
        subset_report.append(
            {
                "label": label,
                "edges": [edge_ends[edge] for edge in selected],
                "a": a,
                "D": D,
                "sum_a": sum_a,
                "c": c,
                "b": b,
                "min_denominator": min_den,
            }
        )
        if not finite:
            failures.append(f"denominator: M_{label} has a non-finite denominator")
            continue
        if not min_den > pos_tol:
            failures.append(
                f"denominator: M_{label} minimum {min_den!r} does not exceed pos_tol {pos_tol!r}"
            )
            continue
        entries[label] = {
            "a": a,
            "D": D,
            "b": b,
            "den": den,
            "u_sites": tuple(blocks[2 + av][2] for av in a),
            "uh_sites": tuple(np.conj(blocks[2 + av][2]).T for av in a),
        }
    result["subsets"] = subset_report
    if subset_report:
        result["min_used_denominator"] = float(
            np.min(np.array([s["min_denominator"] for s in subset_report]))
        )

    shift2 = w2 - e2
    den0 = _kron_sum_denominator(0.0, [shift2] * n_sites)
    keep = np.ones(den0.shape, dtype=bool)
    ground_index = (0,) * n_sites
    keep[ground_index] = False
    result["removed_reference_denominator"] = float(den0[ground_index])
    kept = den0[keep]
    if not bool(np.all(np.isfinite(kept))):
        failures.append("reference inverse: a retained M_empty denominator is not finite")
    else:
        ref_gap = float(np.min(kept))
        result["reference_gap"] = ref_gap
        if not ref_gap > pos_tol:
            failures.append(
                f"reference inverse: minimum retained M_empty denominator {ref_gap!r} "
                f"does not exceed pos_tol {pos_tol!r}"
            )
    if failures:
        return result
    U2 = blocks[2][2]
    ref = {
        "den": den0,
        "keep": keep,
        "u_sites": tuple(U2 for _ in range(n_sites)),
        "uh_sites": tuple(np.conj(U2).T for _ in range(n_sites)),
    }

    # ---- Stage 6: folds, ordered chains and their directional derivatives ----
    result["stage_reached"] = "coefficient"
    if n_sites == 2:
        omega = np.einsum("a,b->ab", chi, chi, optimize=False)
    else:
        omega = np.einsum("a,b,c->abc", chi, chi, chi, optimize=False)
    omega_bra = np.conj(omega)
    zero = np.zeros(omega.shape, dtype=np.complex128)

    moments = {}
    moment_jets = {}
    fold_labels = ("e",) if n_sites == 2 else ("e", "f")
    for label in fold_labels:
        r = _moments(omega, entries[label], 4)
        moments[label] = {f"r{m}": _pair(r[m]) for m in (1, 2, 3, 4)}
        moment_jets[label] = _moment_jets(r, entries[label]["b"])
    result["moments"] = moments

    if n_sites == 2:
        r1e, r2e = moment_jets["e"]
        fold = _product_jet(r2e, r1e)
        double_specs = ()
        restored_specs = (
            ("R_e R0 R_e", (("R", entries["e"]), ("R0", ref), ("R", entries["e"]))),
        )
    else:
        r1e, r2e = moment_jets["e"]
        r1f, r2f = moment_jets["f"]
        fold = _jet_add(_product_jet(r2e, r1f), _product_jet(r2f, r1e))
        double_specs = tuple(
            (
                f"R_{left} R_ef R_{right}",
                (("R", entries[right]), ("R", entries["ef"]), ("R", entries[left])),
            )
            for left in ("e", "f")
            for right in ("e", "f")
        )
        restored_specs = (
            ("R_f R0 R_e", (("R", entries["e"]), ("R0", ref), ("R", entries["f"]))),
            ("R_e R0 R_f", (("R", entries["f"]), ("R0", ref), ("R", entries["e"]))),
        )

    history_report = []
    chain_double = (0j, 0j, 0j)
    for name, steps in double_specs:
        jet = _ordered_chain(steps, omega, omega_bra, zero)
        chain_double = _jet_add(chain_double, jet)
        history_report.append({"history": name, "kind": "double_flip", **_jet_pairs(jet)})
    chain_restored = (0j, 0j, 0j)
    for name, steps in restored_specs:
        jet = _ordered_chain(steps, omega, omega_bra, zero)
        chain_restored = _jet_add(chain_restored, jet)
        history_report.append({"history": name, "kind": "restored", **_jet_pairs(jet)})
    total = _jet_sub(_jet_sub(fold, chain_double), chain_restored)

    result["fold"] = _jet_pairs(fold)
    result["chain_double_flip"] = _jet_pairs(chain_double) if double_specs else None
    result["chain_restored"] = _jet_pairs(chain_restored)
    result["chain_histories"] = history_report
    component_imag = [abs(z.imag) for z in fold + chain_double + chain_restored]
    result["max_abs_imag_components"] = float(np.max(np.array(component_imag)))

    # ---- Stage 7: output checks; no sign gate, no alteration of the totals ----
    result["stage_reached"] = "outputs"
    names = ("d", "dprime", "dsecond")
    result["raw_sums"] = {names[k]: _pair(total[k]) for k in range(3)}
    result["max_abs_imag"] = float(np.max(np.array([abs(z.imag) for z in total])))
    for k in range(3):
        z = total[k]
        if not (np.isfinite(z.real) and np.isfinite(z.imag)):
            failures.append(f"output: {names[k]} is not finite")
            continue
        if not abs(z.imag) <= imag_tol * max(1.0, abs(z.real)):
            failures.append(
                f"output: |Im {names[k]}| = {abs(z.imag)!r} exceeds "
                f"imag_tol * max(1, |Re {names[k]}|)"
            )
    if failures:
        return result

    result["d"] = float(total[0].real)
    result["dprime"] = float(total[1].real)
    result["dsecond"] = float(total[2].real)
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result
