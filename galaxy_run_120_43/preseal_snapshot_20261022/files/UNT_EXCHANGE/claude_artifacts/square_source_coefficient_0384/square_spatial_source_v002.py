# UNT support task 0385 -- inert author implementation, v002 (task 0390: |r2| gate removed).
# One public function, square_spatial_source, plus private helpers.
# Helpers are copied (not imported) from square_source_coefficient_v001.py (0384),
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


def _real_vector4_input(name, value, failures):
    """Admit a finite real length-4 list, tuple or shape-(4,) array, element by element.

    Scalars, other shapes, other container types and non-real elements are
    rejected. Nothing is broadcast, coerced or repaired.
    """
    if isinstance(value, np.ndarray):
        if value.shape != (4,):
            failures.append(f"input {name}: array shape {value.shape!r} is not (4,)")
            return None
        items = [value[k] for k in range(4)]
    elif isinstance(value, (list, tuple)):
        if len(value) != 4:
            failures.append(f"input {name}: length {len(value)} is not 4")
            return None
        items = [value[k] for k in range(4)]
    else:
        failures.append(
            f"input {name}: type {type(value).__name__} is not a length-4 list, tuple "
            "or shape-(4,) array"
        )
        return None
    out = []
    admitted = True
    for k in range(4):
        item = _real_input(f"{name}[{k}]", items[k], failures)
        if item is None:
            admitted = False
        out.append(item)
    if not admitted:
        return None
    return tuple(out)


def _tolerance_input(name, value, failures):
    """Admit an explicit finite tolerance >= 0, or record a failure and return None."""
    out = _real_input(name, value, failures)
    if out is None:
        return None
    if not out >= 0.0:
        failures.append(f"tolerance {name}: must be >= 0, got {out!r}")
        return None
    return out


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


def _site_apply(mat, f, axis):
    """new[..., k on vertex axis] = sum_m mat[k, m] f[..., m on vertex axis].

    The last four axes of f are vertices 0..3; any leading axes are source
    indices (v, or v and w) and are carried unchanged.
    """
    if axis == 0:
        spec = "km,...mbcd->...kbcd"
    elif axis == 1:
        spec = "km,...amcd->...akcd"
    elif axis == 2:
        spec = "km,...abmd->...abkd"
    elif axis == 3:
        spec = "km,...abcm->...abck"
    else:
        raise ValueError(f"vertex axis must be 0, 1, 2 or 3, got {axis!r}")
    return np.einsum(spec, mat, f, optimize=False)


def _to_eigenbasis(f, uh_sites):
    """Site by site, apply conj(U_i)^T on vertex axis i (local basis -> product eigenbasis)."""
    out = f
    for axis in range(4):
        out = _site_apply(uh_sites[axis], out, axis)
    return out


def _from_eigenbasis(t, u_sites):
    """Site by site, apply U_i on vertex axis i (product eigenbasis -> local basis)."""
    out = t
    for axis in range(4):
        out = _site_apply(u_sites[axis], out, axis)
    return out


def _apply_resolvent_jet(f, f_v, f_vw, entry):
    """One R = M_S(j_vec)^(-1) (positive inverse) on the ordered-vector jet.

    With b_v = 4 a_v^2:  R_v = b_v R^2,  R_vw = 2 b_v b_w R^3, and
      new_f    = R f
      new_f_v  = b_v R^2 f + R f_v
      new_f_vw = 2 b_v b_w R^3 f + b_v R^2 f_w + b_w R^2 f_v + R f_vw.
    Shapes: f (4,4,4,4); f_v (4, 4,4,4,4) indexed [v]; f_vw (4,4, 4,4,4,4)
    indexed [v, w]. Powers of R are repeated elementwise division by the same
    denominator array in the product eigenbasis of M_S.
    """
    den = entry["den"]
    b = entry["b"]
    uh_sites = entry["uh_sites"]
    t = _to_eigenbasis(f, uh_sites)
    t_v = _to_eigenbasis(f_v, uh_sites)
    t_vw = _to_eigenbasis(f_vw, uh_sites)
    r1 = t / den
    r2 = r1 / den
    r3 = r2 / den
    r1_v = t_v / den
    r2_v = r1_v / den
    r1_vw = t_vw / den
    new_f = r1
    new_f_v = np.einsum("v,abcd->vabcd", b, r2, optimize=False) + r1_v
    cross = np.einsum("v,wabcd->vwabcd", b, r2_v, optimize=False) + np.einsum(
        "w,vabcd->vwabcd", b, r2_v, optimize=False
    )
    new_f_vw = (
        2.0 * np.einsum("v,w,abcd->vwabcd", b, b, r3, optimize=False) + cross + r1_vw
    )
    u_sites = entry["u_sites"]
    return (
        _from_eigenbasis(new_f, u_sites),
        _from_eigenbasis(new_f_v, u_sites),
        _from_eigenbasis(new_f_vw, u_sites),
    )


def _orders(items):
    """All orderings of a tuple, lexicographic in input position (24 for four edges)."""
    if len(items) <= 1:
        return [tuple(items)]
    out = []
    for idx in range(len(items)):
        rest = items[:idx] + items[idx + 1:]
        for tail in _orders(rest):
            out.append((items[idx],) + tail)
    return out


def _pair(z):
    return (float(z.real), float(z.imag))


def _new_result():
    return {
        "ok": False,
        "stage_reached": None,
        "failures": [],
        "J": None,
        "J_v": None,
        "J_vw": None,
        "raw_sums": None,
        "max_abs_imag": None,
        "max_abs_imag_single_history": None,
        "hessian_symmetry_residual": None,
        "min_real_J_v": None,
        "min_real_J_vw": None,
        "min_used_denominator": None,
        "local_gap": None,
        "e2": None,
        "local_spectra": None,
        "eigen_residual": None,
        "eigenvector_orthonormality_residual": None,
        "hermiticity_residual": None,
        "r2": None,
        "mu0": None,
        "delta": None,
        "n_histories": None,
        "n_subsets_cached": None,
        "n_subsets_used": None,
        "D_values": None,
        "n_adjacent_first_pair_histories": None,
        "n_disjoint_first_pair_histories": None,
        "subsets": None,
        "histories": None,
        "declared_inputs": None,
        "declared_tolerances": None,
        "ref_tol_note": (
            "ref_tol is a legacy admitted argument (V002, task 0390): validated finite and "
            ">= 0 but no longer restricts r2 = epsilon_r - 2 lambda_R, which is reported only"
        ),
        "units": {"J": "E^-3", "J_v": "E^-4", "J_vw": "E^-5", "j_vec": "E"},
        "static_notes": [
            "Same a_v, D, mu0, K, V, chi, complete local spectra and per-prefix tensor "
            "eigenbases as 0384; only the scalar shift of M_S depends on j_vec: "
            "c(S, j_vec) = Ud D + mu0 sum_v a_v - 4 sum_v j_v a_v^2.",
            "Both ice endpoints have O_v = -4, so the reference energy shifts by "
            "4 sum_v j_v; c(S, j_vec) is already relative to that reference. "
            "chi does not depend on j_vec.",
            "b_Sv = 4 a_v^2; R_v = b_v R^2 and R_vw = 2 b_v b_w R^3 hold exactly although "
            "consecutive prefix matrices do not commute, because j_vec enters each M_S "
            "only through a multiple of the identity.",
            "J_vw is the ordinary Hessian (no extra factor of 2 off the diagonal). It is "
            "never symmetrized; its symmetry residual is reported and gated.",
            "No canonical fold contributes to this four-edge off-diagonal entry; the "
            "separate diagonal folds still belong to the full action.",
            "H(2+a) = H(2) + a V with V = diag(0, -lambda_R, lambda_J, lambda_J - lambda_R) "
            "holds identically; H(1), H(2), H(3) are built from the displayed formula.",
            "All 256 eigenvalues of each M_S(j_vec) are treated as used denominators.",
            "Histories: lexicographic orders of edges (0,1),(1,2),(2,3),(3,0); S1 acts first.",
        ],
        "scope": (
            "exact-r pure-flip reference coefficients only (spatial-source derivatives of "
            "the square off-diagonal), not full-parent validity; "
            "not the complete spatial response (the h^2 diagonal contact, fourth-order "
            "diagonal, state-redistribution, coupled-field and physical-map terms remain "
            "separate); no calibration, physical state, speed or geometry"
        ),
    }


def square_spatial_source(
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
    j_vec,
    ref_tol,
    pos_tol,
    herm_tol,
    resid_tol,
    imag_tol,
):
    """Square-loop coefficient J(j_vec), its four source gradients J_v and Hessian J_vw.

    Sources (read-only):
      * Formula authority: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
        0385_2026-10-15_square_spatial_source_inert_implementation.md
      * Structure and helpers copied from: /Users/bgm/Research/UNT_EXCHANGE/
        claude_artifacts/square_source_coefficient_0384/square_source_coefficient_v001.py
        (0384 task: FROM_CODEX/0384_2026-10-15_square_source_coefficient_inert_implementation.md)
      * Context: /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/
        FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md,
        section "The leading collective source response precedes the mixed correction"
        and the local matrix conventions of the connected mixed-coefficient section.

    Definition (0385, on the 0384 construction):
      Local basis (A0, A1, B0, B1); r_d = epsilon_r - lambda_R d;
      H(d) = [[ER, 0, conj(kappa), 0], [0, ER + r_d, 0, conj(kappa)],
              [kappa, 0, ES + epsilon_c + lambda_J d, g],
              [0, kappa, g, ES + epsilon_c + lambda_J d + r_d]].
      chi, e2: unique lowest eigenpair of H(2); psi = chi x chi x chi x chi.
      Four-cycle edges (0,1),(1,2),(2,3),(3,0); initial bits (1,0,1,0);
      sigma = (-1, +1, -1, +1); a_v(S), D(S) = sum_v a_v^2, mu0 = Delta/2 + 2 Ud (2 - dstar).
      M_S(j_vec) = [Ud D + mu0 sum_v a_v - 4 sum_v j_v a_v^2] I + sum_v (K_v + a_v V_v),
      with K_v + a_v V_v = H_v(2 + a_v) - e2 I_v. b_Sv = 4 a_v^2, R = M_S^-1 (positive).
      Jet from (psi, 0, 0), each prefix S1, S2, S3 in order:
        f <- R f;  f_v <- b_v R^2 f + R f_v;
        f_vw <- 2 b_v b_w R^3 f + b_v R^2 f_w + b_w R^2 f_v + R f_vw.
      J = sum over 24 edge orders of <psi|f>, J_v = sum <psi|f_v>, J_vw = sum <psi|f_vw>.
      Units: J E^-3, J_v E^-4, J_vw E^-5; j_vec in native energy units.

    j_vec: required finite real length-4 list, tuple or shape-(4,) array in vertex
    order 0, 1, 2, 3. Scalars and other shapes are rejected, never broadcast.

    Every argument is keyword-only and required; there are no defaults.
    Tolerances: ref_tol (legacy admitted argument since V002, task 0390: validated
    finite and >= 0, but it no longer restricts r2 = epsilon_r - 2 lambda_R, which
    is reported only; exact-r basis: response_packet_audit/POPULATED_EXACT_R_LOCAL_
    GROUND_DEFECT_HEX_AND_CONTACT_EXTENSION_PROPOSED_V001.md),
    pos_tol (every used denominator and the local H(2) gap must exceed it),
    herm_tol (max |H - H^dagger|), resid_tol (max |H U - U diag(w)|,
    max |U^dagger U - I|, and the Hessian symmetry residual
    max |J_vw - J_wv| <= resid_tol * max(1, max |J_vw|)), imag_tol
    (|Im X| <= imag_tol * max(1, |Re X|) for J and every entry of J_v and J_vw).

    Fail closed: returns a plain dict. "ok" is True only if every check passes;
    then J, J_v (list of 4) and J_vw (4x4 nested list, not symmetrized) hold the
    checked real parts. Otherwise they are None, "failures" lists every violated
    check and "stage_reached" names where the computation stopped. Raw complex
    sums are always reported unaltered as (real, imag) pairs once computed.

    Working arrays: (4,4,4,4) tensors for f, (4,4,4,4,4) for f_v and
    (4,4,4,4,4,4) for f_vw (at most 4096 complex128 elements, 64 KiB), 4x4 local
    blocks and 14 cached (4,4,4,4) float64 denominator arrays. No 256x256 array is
    formed. All contractions, outer products and basis transforms use
    numpy.einsum(..., optimize=False); the 4x4 blocks use numpy.linalg.eigh.

    Scope: exact-r pure-flip reference coefficients only (spatial-source
    derivatives of the square off-diagonal), not full-parent validity; not the
    complete spatial response; no calibration, physical state, speed or geometry.
    """
    result = _new_result()
    failures = result["failures"]

    # ---- Stage 1: declared inputs, source vector and explicit tolerances -----
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
    jv = _real_vector4_input("j_vec", j_vec, failures)
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
    declared["j_vec"] = None if jv is None else list(jv)
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
    if not g > 0.0:
        failures.append(f"reference: g = {g!r} is not > 0")
    if kappa == 0:
        failures.append("reference: kappa is zero")
    if not delta > 0.0:
        failures.append(f"reference: delta = {delta!r} is not > 0")
    if failures:
        return result

    # ---- Stage 3: complete local eigensystems of H(1), H(2), H(3) (as 0384) --
    result["stage_reached"] = "local_blocks"
    blocks = {}
    for d in (1, 2, 3):
        H = _local_block(
            ER, ES, epsilon_c, epsilon_r, lambda_J, lambda_R, g, kappa, float(d)
        )
        if not np.all(np.isfinite(H)):
            failures.append(f"local: H({d}) has a non-finite entry")
            continue
        try:
            w, U = np.linalg.eigh(H, UPLO="L")
        except np.linalg.LinAlgError as exc:
            failures.append(f"local: eigh of H({d}) failed ({exc})")
            continue
        if not (np.all(np.isfinite(w)) and np.all(np.isfinite(U))):
            failures.append(f"local: eigensystem of H({d}) is not finite")
            continue
        blocks[d] = (H, w, U)
    if failures:
        return result

    eye4 = np.eye(4, dtype=np.complex128)
    herm_list = []
    resid_list = []
    ortho_list = []
    spectra = {}
    for d in (1, 2, 3):
        H, w, U = blocks[d]
        herm_list.append(np.max(np.abs(H - np.conj(H).T)))
        HU = np.einsum("mn,nk->mk", H, U, optimize=False)
        resid_list.append(np.max(np.abs(HU - U * w[np.newaxis, :])))
        UhU = np.einsum("mk,ml->kl", np.conj(U), U, optimize=False)
        ortho_list.append(np.max(np.abs(UhU - eye4)))
        spectra[f"H({d})"] = [float(v) for v in w]
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

    # ---- Stage 4: 14 nonempty proper edge subsets, source weights, denominators
    result["stage_reached"] = "subsets"
    edges = ((0, 1), (1, 2), (2, 3), (3, 0))
    initial_bits = (1, 0, 1, 0)
    sigma = tuple(1 - 2 * bit for bit in initial_bits)
    if sigma != (-1, 1, -1, 1):
        failures.append(f"cycle: flip increments {sigma!r} differ from (-1, 1, -1, 1)")
        return result
    cache = {}
    subset_report = []
    for mask in range(1, 15):
        selected = tuple(e for e in range(4) if (mask >> e) & 1)
        a = [0, 0, 0, 0]
        for e in selected:
            for vertex in edges[e]:
                a[vertex] += sigma[e]
        a = tuple(a)
        if any(ai not in (-1, 0, 1) for ai in a):
            failures.append(f"cycle: subset {selected!r} has a-vector {a!r} outside {{-1,0,1}}")
            continue
        D = sum(ai * ai for ai in a)
        sum_a = sum(a)
        b = tuple(4.0 * ai * ai for ai in a)
        source_shift = sum(jv[v] * b[v] for v in range(4))
        c = Ud * D + mu0 * sum_a - source_shift
        shifts = [blocks[2 + ai][1] - e2 for ai in a]
        den = (
            c
            + shifts[0][:, np.newaxis, np.newaxis, np.newaxis]
            + shifts[1][np.newaxis, :, np.newaxis, np.newaxis]
            + shifts[2][np.newaxis, np.newaxis, :, np.newaxis]
            + shifts[3][np.newaxis, np.newaxis, np.newaxis, :]
        )
        finite = bool(np.all(np.isfinite(den)))
        min_den = float(np.min(den))
        subset_report.append(
            {
                "mask": mask,
                "edges": selected,
                "a": a,
                "D": D,
                "sum_a": sum_a,
                "b": b,
                "c": c,
                "min_denominator": min_den,
            }
        )
        if not finite:
            failures.append(f"denominator: subset {selected!r} has a non-finite denominator")
            continue
        if not min_den > pos_tol:
            failures.append(
                f"denominator: subset {selected!r} minimum {min_den!r} does not exceed "
                f"pos_tol {pos_tol!r}"
            )
            continue
        cache[mask] = {
            "a": a,
            "D": D,
            "b": np.array(b, dtype=np.float64),
            "den": den,
            "u_sites": tuple(blocks[2 + ai][2] for ai in a),
            "uh_sites": tuple(np.conj(blocks[2 + ai][2]).T for ai in a),
        }
    result["subsets"] = subset_report
    result["n_subsets_cached"] = len(cache)
    if subset_report:
        result["min_used_denominator"] = float(
            np.min(np.array([s["min_denominator"] for s in subset_report]))
        )
    if failures:
        return result

    # ---- Stage 5: the 24 ordered histories, D checks before any inversion -----
    result["stage_reached"] = "histories"
    orders = _orders((0, 1, 2, 3))
    if len(orders) != 24 or len(set(orders)) != 24:
        failures.append(f"histories: {len(orders)} orders generated, 24 distinct required")
        return result
    plan = []
    n_adjacent = 0
    n_disjoint = 0
    for order in orders:
        m1 = 1 << order[0]
        m2 = m1 | (1 << order[1])
        m3 = m2 | (1 << order[2])
        adjacent = len(set(edges[order[0]]) & set(edges[order[1]])) > 0
        if adjacent:
            n_adjacent += 1
        else:
            n_disjoint += 1
        expected = (2, 2 if adjacent else 4, 2)
        found = (cache[m1]["D"], cache[m2]["D"], cache[m3]["D"])
        if found != expected:
            failures.append(
                f"histories: order {order!r} has D(S1,S2,S3) = {found!r}, expected {expected!r}"
            )
        plan.append((order, (m1, m2, m3), adjacent, found))
    used = set()
    for _, masks, _, _ in plan:
        used.update(masks)
    result["n_histories"] = len(plan)
    result["n_subsets_used"] = len(used)
    result["D_values"] = sorted({cache[m]["D"] for m in used})
    result["n_adjacent_first_pair_histories"] = n_adjacent
    result["n_disjoint_first_pair_histories"] = n_disjoint
    if len(used) != 14:
        failures.append(f"histories: {len(used)} distinct prefix subsets used, 14 expected")
    if failures:
        return result

    psi = np.einsum("a,b,c,d->abcd", chi, chi, chi, chi, optimize=False)
    psi_bra = np.conj(psi)
    zero_v = np.zeros((4, 4, 4, 4, 4), dtype=np.complex128)
    zero_vw = np.zeros((4, 4, 4, 4, 4, 4), dtype=np.complex128)
    sum_J = 0j
    sum_J_v = np.zeros(4, dtype=np.complex128)
    sum_J_vw = np.zeros((4, 4), dtype=np.complex128)
    history_report = []
    single_imag = []
    for order, masks, adjacent, found in plan:
        f, f_v, f_vw = psi, zero_v, zero_vw
        for mask in masks:
            f, f_v, f_vw = _apply_resolvent_jet(f, f_v, f_vw, cache[mask])
        h_J = complex(np.einsum("abcd,abcd->", psi_bra, f, optimize=False))
        h_J_v = np.einsum("abcd,vabcd->v", psi_bra, f_v, optimize=False)
        h_J_vw = np.einsum("abcd,vwabcd->vw", psi_bra, f_vw, optimize=False)
        sum_J = sum_J + h_J
        sum_J_v = sum_J_v + h_J_v
        sum_J_vw = sum_J_vw + h_J_vw
        single_imag.append(abs(h_J.imag))
        single_imag.append(float(np.max(np.abs(h_J_v.imag))))
        single_imag.append(float(np.max(np.abs(h_J_vw.imag))))
        history_report.append(
            {
                "order": order,
                "prefix_masks": masks,
                "adjacent_first_pair": adjacent,
                "D": found,
                "J": _pair(h_J),
                "J_v": [_pair(h_J_v[v]) for v in range(4)],
                "J_vw": [[_pair(h_J_vw[v, w]) for w in range(4)] for v in range(4)],
            }
        )
    result["histories"] = history_report
    result["max_abs_imag_single_history"] = float(np.max(np.array(single_imag)))

    # ---- Stage 6: output checks; no alteration or symmetrization of the sums --
    result["stage_reached"] = "outputs"
    result["raw_sums"] = {
        "J": _pair(sum_J),
        "J_v": [_pair(sum_J_v[v]) for v in range(4)],
        "J_vw": [[_pair(sum_J_vw[v, w]) for w in range(4)] for v in range(4)],
    }
    entries = [("J", sum_J)]
    for v in range(4):
        entries.append((f"J_v[{v}]", sum_J_v[v]))
    for v in range(4):
        for w in range(4):
            entries.append((f"J_vw[{v},{w}]", sum_J_vw[v, w]))
    result["max_abs_imag"] = float(np.max(np.array([abs(z.imag) for _, z in entries])))
    all_finite = True
    for label, z in entries:
        if not (np.isfinite(z.real) and np.isfinite(z.imag)):
            failures.append(f"output: {label} is not finite")
            all_finite = False
            continue
        if not abs(z.imag) <= imag_tol * max(1.0, abs(z.real)):
            failures.append(
                f"output: |Im {label}| = {abs(z.imag)!r} exceeds imag_tol * max(1, |Re {label}|)"
            )
    if not sum_J.real > 0.0:
        failures.append(f"output: Re J = {sum_J.real!r} is not > 0")
    if all_finite:
        sym = float(np.max(np.abs(sum_J_vw - sum_J_vw.T)))
        scale = max(1.0, float(np.max(np.abs(sum_J_vw))))
        result["hessian_symmetry_residual"] = sym
        if not sym <= resid_tol * scale:
            failures.append(
                f"output: Hessian symmetry residual {sym!r} exceeds resid_tol * max(1, max|J_vw|)"
            )
        result["min_real_J_v"] = float(np.min(sum_J_v.real))
        result["min_real_J_vw"] = float(np.min(sum_J_vw.real))
    if failures:
        return result

    result["J"] = float(sum_J.real)
    result["J_v"] = [float(sum_J_v[v].real) for v in range(4)]
    result["J_vw"] = [[float(sum_J_vw[v, w].real) for w in range(4)] for v in range(4)]
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result
