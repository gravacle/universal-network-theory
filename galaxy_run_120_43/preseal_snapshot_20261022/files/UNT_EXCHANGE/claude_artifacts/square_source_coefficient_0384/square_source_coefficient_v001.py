# UNT support task 0384 -- inert author implementation, v001.
# One public function, square_source_coefficient, plus private helpers.
# Module-level code is limited to the numpy import and function definitions:
# no constants, no work at import, no I/O, no subprocesses, no CLI.
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
    """new[..k..] = sum_m mat[k, m] f[..m..] on tensor axis `axis` of a (4,4,4,4) array."""
    if axis == 0:
        spec = "km,mbcd->kbcd"
    elif axis == 1:
        spec = "km,amcd->akcd"
    elif axis == 2:
        spec = "km,abmd->abkd"
    elif axis == 3:
        spec = "km,abcm->abck"
    else:
        raise ValueError(f"tensor axis must be 0, 1, 2 or 3, got {axis!r}")
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


def _apply_resolvent_with_derivatives(f, fp, fpp, entry):
    """One R = M_S(j)^(-1) with the exact product rule, all three in the eigenbasis of M_S.

    new_f   = R f
    new_fp  = R' f + R fp,                    R'  = 4 D R^2
    new_fpp = R'' f + 2 R' fp + R fpp,        R'' = 32 D^2 R^3
    Powers of R are repeated elementwise division by the same denominator array.
    """
    den = entry["den"]
    D = float(entry["D"])
    uh_sites = entry["uh_sites"]
    t_f = _to_eigenbasis(f, uh_sites)
    t_fp = _to_eigenbasis(fp, uh_sites)
    t_fpp = _to_eigenbasis(fpp, uh_sites)
    r1_f = t_f / den
    r2_f = r1_f / den
    r3_f = r2_f / den
    r1_fp = t_fp / den
    r2_fp = r1_fp / den
    r1_fpp = t_fpp / den
    new_f = r1_f
    new_fp = (4.0 * D) * r2_f + r1_fp
    new_fpp = (32.0 * D * D) * r3_f + 2.0 * (4.0 * D) * r2_fp + r1_fpp
    u_sites = entry["u_sites"]
    return (
        _from_eigenbasis(new_f, u_sites),
        _from_eigenbasis(new_fp, u_sites),
        _from_eigenbasis(new_fpp, u_sites),
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


def _new_result():
    return {
        "ok": False,
        "stage_reached": None,
        "failures": [],
        "J": None,
        "Jprime": None,
        "Jsecond": None,
        "raw_sums": None,
        "max_abs_imag": None,
        "max_abs_imag_single_history": None,
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
        "units": {"J": "E^-3", "Jprime": "E^-4", "Jsecond": "E^-5"},
        "static_notes": [
            "H(2+a) = H(2) + a V with V = diag(0, -lambda_R, lambda_J, lambda_J - lambda_R) "
            "holds identically (r_d = epsilon_r - lambda_R d; B diagonal carries lambda_J d). "
            "H(1), H(2), H(3) are built from the displayed formula; the identity is not "
            "tested numerically beyond the listed residuals.",
            "M_S(j) = c(S,j) I + sum_i (H_i(2+a_i) - e2 I_i) is a Kronecker sum; its 256 "
            "eigenvalues c + sum_i (w_{2+a_i}[k_i] - e2) are all treated as used denominators.",
            "Edge flips act on incidence only; internal states and the exterior edges are "
            "exact spectators. The global phase of chi cancels in <psi|...|psi>.",
            "Histories: lexicographic orders of edges (0,1),(1,2),(2,3),(3,0); S1 acts first.",
        ],
        "scope": (
            "native finite coefficient only; no calibration, physical state, speed or geometry"
        ),
    }


def square_source_coefficient(
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
    j,
    ref_tol,
    pos_tol,
    herm_tol,
    resid_tol,
    imag_tol,
):
    """Exact finite native square-loop coefficient J(j) and its first two j-derivatives.

    Sources (read-only):
      * Task: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
        0384_2026-10-15_square_source_coefficient_inert_implementation.md
        (explicit formulas; followed where wording differs).
      * Reviewed specification: /Users/bgm/Research/Universal Network Theory/
        UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/
        GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md, section "The leading
        collective source response precedes the mixed correction", with the local
        matrix conventions of "Connected mixed coefficient reduced to explicit local
        inverses and graph Grams".
      * Ingredient custody (context): UNT_EXCHANGE/FROM_CLAUDE2/0064_*, 0065_*.

    Definition (0384):
      Local basis (A0, A1, B0, B1); r_d = epsilon_r - lambda_R d;
      H(d) = [[ER, 0, conj(kappa), 0], [0, ER + r_d, 0, conj(kappa)],
              [kappa, 0, ES + epsilon_c + lambda_J d, g],
              [0, kappa, g, ES + epsilon_c + lambda_J d + r_d]].
      chi, e2: unique lowest eigenpair of H(2). psi = chi x chi x chi x chi.
      Four-cycle edges (0,1),(1,2),(2,3),(3,0); initial bits (1,0,1,0);
      sigma = (-1, +1, -1, +1). For a nonempty proper edge subset S:
      a_i(S) = sum of sigma_e over selected edges incident to vertex i,
      D(S) = sum_i a_i^2, mu0 = Delta/2 + 2 Ud (2 - dstar),
      M_S(j) = [Ud D + mu0 sum_i a_i - 4 j D] I + sum_i (H_i(2 + a_i) - e2 I_i).
      J(j) = sum over 24 edge orders of <psi| M_S3^-1 M_S2^-1 M_S1^-1 |psi>,
      with S1, S2, S3 the ordered prefixes; R' = 4 D R^2, R'' = 32 D^2 R^3,
      propagated by the exact product rule. Units: J E^-3, Jprime E^-4,
      Jsecond E^-5.

    Every argument is keyword-only and required; there are no defaults.
    Tolerances: ref_tol (|r2| <= ref_tol, r2 = epsilon_r - 2 lambda_R),
    pos_tol (every used denominator and the local H(2) gap must exceed it),
    herm_tol (max |H - H^dagger|), resid_tol (max |H U - U diag(w)| and
    max |U^dagger U - I|), imag_tol (|Im X| <= imag_tol * max(1, |Re X|)).

    Fail closed: returns a plain dict. "ok" is True only if every check passes;
    then J, Jprime, Jsecond are the checked real parts. Otherwise they are None,
    "failures" lists every violated check and "stage_reached" names where the
    computation stopped. Raw complex sums are always reported unaltered as
    (real, imag) pairs once computed. Nothing is repaired, regularized, dropped
    or silently projected to its real part.

    Working arrays: length-256 vectors held as (4,4,4,4) complex128 tensors
    (axis i = vertex i), 4x4 local blocks, and 14 cached (4,4,4,4) float64
    denominator arrays. No 256x256 matrix is formed. All contractions and basis
    transforms use numpy.einsum(..., optimize=False); the 4x4 blocks use
    numpy.linalg.eigh.

    Scope: native finite coefficient only; no calibration, physical state,
    speed or geometry.
    """
    result = _new_result()
    failures = result["failures"]

    # ---- Stage 1: declared inputs and explicit tolerances --------------------
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
        ("j", j),
    )
    x = {}
    for name, value in real_given:
        x[name] = _real_input(name, value, failures)
    kap = _complex_input("kappa", kappa, failures)
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
    j = x["j"]
    kappa = kap
    ref_tol = tol["ref_tol"]
    pos_tol = tol["pos_tol"]
    herm_tol = tol["herm_tol"]
    resid_tol = tol["resid_tol"]
    imag_tol = tol["imag_tol"]

    # ---- Stage 2: declared reference and degree condition --------------------
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

    # ---- Stage 3: complete local eigensystems of H(1), H(2), H(3) -------------
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

    # ---- Stage 4: the 14 nonempty proper edge subsets and their denominators --
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
        c = Ud * D + mu0 * sum_a - 4.0 * j * D
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
    zero = np.zeros((4, 4, 4, 4), dtype=np.complex128)
    sums = [0j, 0j, 0j]
    history_report = []
    single_imag = []
    for order, masks, adjacent, found in plan:
        f, fp, fpp = psi, zero, zero
        for mask in masks:
            f, fp, fpp = _apply_resolvent_with_derivatives(f, fp, fpp, cache[mask])
        values = [
            complex(np.einsum("abcd,abcd->", psi_bra, arr, optimize=False))
            for arr in (f, fp, fpp)
        ]
        for k in range(3):
            sums[k] = sums[k] + values[k]
            single_imag.append(abs(values[k].imag))
        history_report.append(
            {
                "order": order,
                "prefix_masks": masks,
                "adjacent_first_pair": adjacent,
                "D": found,
                "J": (values[0].real, values[0].imag),
                "Jprime": (values[1].real, values[1].imag),
                "Jsecond": (values[2].real, values[2].imag),
            }
        )
    result["histories"] = history_report
    result["max_abs_imag_single_history"] = float(np.max(np.array(single_imag)))

    # ---- Stage 6: output checks; no alteration of the computed sums ----------
    result["stage_reached"] = "outputs"
    names = ("J", "Jprime", "Jsecond")
    raw = {names[k]: sums[k] for k in range(3)}
    result["raw_sums"] = {n: (raw[n].real, raw[n].imag) for n in names}
    result["max_abs_imag"] = float(np.max(np.array([abs(raw[n].imag) for n in names])))
    for n in names:
        value = raw[n]
        if not (np.isfinite(value.real) and np.isfinite(value.imag)):
            failures.append(f"output: {n} is not finite")
            continue
        if not abs(value.imag) <= imag_tol * max(1.0, abs(value.real)):
            failures.append(
                f"output: |Im {n}| = {abs(value.imag)!r} exceeds imag_tol * max(1, |Re {n}|)"
            )
        if not value.real > 0.0:
            failures.append(f"output: Re {n} = {value.real!r} is not > 0")
    if failures:
        return result

    result["J"] = raw["J"].real
    result["Jprime"] = raw["Jprime"].real
    result["Jsecond"] = raw["Jsecond"].real
    result["ok"] = True
    result["stage_reached"] = "complete"
    return result
