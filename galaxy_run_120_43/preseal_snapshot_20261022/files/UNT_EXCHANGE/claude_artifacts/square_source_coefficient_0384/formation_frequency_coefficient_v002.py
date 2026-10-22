# UNT support task 0392 -- inert author implementation, v002 (review F1/F6: intermediate finiteness, j = 0).
# One public function, formation_frequency_coefficient, plus private helpers.
# Helpers are copied (not imported) from the reviewed 0390 V002 modules in this
# directory. Module-level code is limited to the numpy import and function
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


def _tolerance_input(name, value, failures):
    """Admit an explicit finite tolerance >= 0, or record a failure and return None."""
    out = _real_input(name, value, failures)
    if out is None:
        return None
    if not out >= 0.0:
        failures.append(f"tolerance {name}: must be >= 0, got {out!r}")
        return None
    return out


def _z_values_input(name, value, failures):
    """Admit 1..32 finite complex frequencies with Im(z) >= 0 from a list, tuple or 1-D array.

    Scalars, bools, other shapes and non-finite entries are rejected; nothing is
    broadcast, coerced from strings, clipped or repaired.
    """
    if isinstance(value, np.ndarray):
        if value.ndim != 1:
            failures.append(f"input {name}: array shape {value.shape!r} is not 1-D")
            return None
    elif not isinstance(value, (list, tuple)):
        failures.append(
            f"input {name}: type {type(value).__name__} is not a list, tuple or 1-D array"
        )
        return None
    if not 1 <= len(value) <= 32:
        failures.append(f"input {name}: length {len(value)} is not in 1..32")
        return None
    out = []
    admitted = True
    for k in range(len(value)):
        z = _complex_input(f"{name}[{k}]", value[k], failures)
        if z is None:
            admitted = False
        elif not z.imag >= 0.0:
            failures.append(f"input {name}[{k}]: Im(z) = {z.imag!r} is negative")
            admitted = False
        out.append(z)
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


def _pair(z):
    return {"real": float(z.real), "imag": float(z.imag)}


def _new_result():
    return {
        "ok": False,
        "stage_reached": None,
        "failures": [],
        "r2": None,
        "mu0": None,
        "delta": None,
        "e2": None,
        "local_gap": None,
        "local_spectra": None,
        "eigen_residual": None,
        "eigenvector_orthonormality_residual": None,
        "hermiticity_residual": None,
        "sectors": None,
        "frequencies": None,
        "declared_inputs": None,
        "declared_tolerances": None,
        "units": {
            "z": "E",
            "D_ab": "E",
            "m_sigma": "E",
            "r_p": "E^-p",
            "F": "E^-3",
            "F4": "E^-3",
            "frequency_remainder_bound": "E^-3",
            "q_a": "dimensionless",
            "w_ab": "dimensionless",
        },
        "static_notes": [
            "r2 is epsilon_r - 2 lambda_R (reported only; any finite value is admitted). "
            "The moments are reported separately as r_2, r_3, r_5, r_7.",
            "For sigma = -1, +1 and d = 2 + sigma: q_a = |sum_i conj(U_d[i,a]) chi[i]|^2, "
            "w_ab = q_a q_b, D_ab = 2 Ud + 2 sigma mu0 + E_a(d) + E_b(d) - 2 e2 (evaluated "
            "as (2 Ud + 2 sigma mu0) + (E_a - e2) + (E_b - e2)); weights are never "
            "renormalized.",
            "F_sigma(z) = 2 sum w_ab / [D_ab (D_ab^2 - z^2)] already includes the factor 2; "
            "the graph/read factor h^2 Delta_A Delta_B is NOT applied here.",
            "F4_sigma(z) = 2 (r_3 + z^2 r_5 + z^4 r_7); "
            "bound_sigma(z) = 2 |z|^6 / [m_sigma^9 (1 - |z|^2 / m_sigma^2)].",
        ],
        "scope": (
            "order-h^2 eliminated single-flip (high-sector) contribution for a consistently "
            "dressed low-band stationary/adiabatic reference with unoccupied high sector; "
            "not the full collective response, not a physical-state selection, not a "
            "metric kernel and not a galaxy prediction. At z = 0, F equals the existing "
            "static contact (2 r_3): the caller REPLACES that contact with F(z), or adds "
            "only F(z) - F(0), never both. The remainder bound controls only this "
            "coefficient's frequency expansion, not omitted coupling orders, other owners "
            "or collective poles. Bare nonstationary preparation needs the two-time "
            "kernel. No causal lapse-inverse shortcut is authorized. This is the j = 0 "
            "reference coefficient: there is no source argument and no source shift in D_ab."
        ),
    }


def formation_frequency_coefficient(
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
    z_values,
    pos_tol,
    herm_tol,
    resid_tol,
):
    """Frequency-dependent single-flip formation coefficient F_sigma(z), sigma = -1, +1.

    Sources (read-only):
      * Formula authority: /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/
        0392_2026-10-15_dynamic_formation_coefficient_implementation.md
      * Context: CODEX1/GALAXY_COLLECTIVE_MODEL_ASSEMBLY_2026-10-15.md, section
        "Frequency-dependent formation contribution for the collective kernel";
        distinct review helpers/response_packet_audit/
        DYNAMIC_SINGLE_FLIP_HIGH_CONTACT_DISTINCT_REVIEW_V001.json (PASS_SCOPED).
      * Helpers copied from square_source_coefficient_0384/*_v002.py (task 0390).

    Definition (0392):
      H(d) = [[ER, 0, conj(kappa), 0], [0, ER + r_d, 0, conj(kappa)],
              [kappa, 0, ES + epsilon_c + lambda_J d, g],
              [0, kappa, g, ES + epsilon_c + lambda_J d + r_d]], r_d = epsilon_r - lambda_R d,
      complete eigensystems at d = 1, 2, 3; e2, chi: actual unique ground of H(2).
      mu0 = Delta/2 + 2 Ud (2 - dstar); delta as in 0390 (must be > 0).
      For sigma = -1, +1 and d = 2 + sigma:
        q_a  = |sum_i conj(U_d[i,a]) chi[i]|^2,   w_ab = q_a q_b,
        D_ab = 2 Ud + 2 sigma mu0 + E_a(d) + E_b(d) - 2 e2   (all 16 > pos_tol),
        |sum w - 1| <= resid_tol (no renormalization),  m_sigma = min D_ab,
        r_p  = sum w_ab / D_ab^p,  p = 2, 3, 5, 7  (every D_ab^p must be finite and > 0).
      j = 0 reference: there is no source argument and no source shift in D_ab.
      For every z (|z| < m_sigma for BOTH sigma):
        F_sigma(z)  = 2 sum w_ab / [D_ab (D_ab^2 - z^2)],
        F4_sigma(z) = 2 (r_3 + z^2 r_5 + z^4 r_7),
        bound_sigma(z) = 2 |z|^6 / [m_sigma^9 (1 - |z|^2 / m_sigma^2)].
      Units: z, D, m in E; r_p in E^-p; F, F4 and the bound in E^-3.

    Inputs: every argument is keyword-only and required; there are no defaults.
    z_values: 1..32 finite complex energies (list, tuple or 1-D array), Im(z) >= 0.
    Tolerances: pos_tol (local H(2) gap and every D_ab must exceed it), herm_tol
    (max |H - H^dagger|), resid_tol (max |H U - U diag(w)|, max |U^dagger U - I| and
    |sum w - 1|). General finite r2 = epsilon_r - 2 lambda_R is admitted and reported.

    Fail closed: returns a plain dict; "ok" is True only if every check passes.
    Otherwise "failures" lists every violated check and "stage_reached" names where
    the computation stopped. Complex values are reported as {"real", "imag"} fields,
    including every exact input z. Inputs and weights are never clipped,
    substituted or renormalized.

    Working arrays: 4x4 local blocks, 4-element overlaps and 4x4 (16-entry) pair
    tables. Contractions use numpy.einsum(..., optimize=False); the 4x4 blocks use
    numpy.linalg.eigh. Floating-point warnings are not suppressed.

    Scope: order-h^2 eliminated single-flip contribution for a dressed low-band
    stationary/adiabatic reference; not the full collective response, a state
    selection, a metric kernel or a prediction. At z = 0 it equals the static
    contact; the caller REPLACES that contact with F(z) or adds only F(z) - F(0),
    never both. The bound controls only the frequency expansion. No lapse-inverse
    shortcut. This is the j = 0 reference coefficient. The bound's intermediates
    m_sigma^9, |z|^6 and 1 - |z|^2/m_sigma^2 must be finite, with m_sigma^9 > 0 and
    1 - |z|^2/m_sigma^2 > 0, or the call fails closed.
    """
    result = _new_result()
    failures = result["failures"]

    # ---- Stage 1: declared inputs, frequencies and explicit tolerances -------
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
    zs = _z_values_input("z_values", z_values, failures)
    tol_given = (
        ("pos_tol", pos_tol),
        ("herm_tol", herm_tol),
        ("resid_tol", resid_tol),
    )
    tol = {}
    for name, value in tol_given:
        tol[name] = _tolerance_input(name, value, failures)
    declared = dict(x)
    declared["kappa"] = None if kap is None else _pair(kap)
    declared["z_values"] = None if zs is None else [_pair(z) for z in zs]
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
    pos_tol = tol["pos_tol"]
    herm_tol = tol["herm_tol"]
    resid_tol = tol["resid_tol"]

    # ---- Stage 2: reference and degree condition (as 0390 V002) -------------
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
            w_d, U_d = np.linalg.eigh(H, UPLO="L")
        except np.linalg.LinAlgError as exc:
            failures.append(f"local: eigh of H({d}) failed ({exc})")
            continue
        if not (np.all(np.isfinite(w_d)) and np.all(np.isfinite(U_d))):
            failures.append(f"local: eigensystem of H({d}) is not finite")
            continue
        blocks[d] = (H, w_d, U_d)
    if failures:
        return result

    eye4 = np.eye(4, dtype=np.complex128)
    herm_list = []
    resid_list = []
    ortho_list = []
    spectra = {}
    for d in (1, 2, 3):
        H, w_d, U_d = blocks[d]
        herm_list.append(np.max(np.abs(H - np.conj(H).T)))
        HU = np.einsum("mn,nk->mk", H, U_d, optimize=False)
        resid_list.append(np.max(np.abs(HU - U_d * w_d[np.newaxis, :])))
        UhU = np.einsum("mk,ml->kl", np.conj(U_d), U_d, optimize=False)
        ortho_list.append(np.max(np.abs(UhU - eye4)))
        spectra[f"H({d})"] = [float(v) for v in w_d]
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

    # ---- Stage 4: 16-entry pair tables, weights and moments per sigma ---------
    result["stage_reached"] = "pair_tables"
    sectors = {}
    sector_report = []
    for sigma in (-1, 1):
        n_failures_before = len(failures)
        d = 2 + sigma
        _, E_d, U_d = blocks[d]
        overlap = np.einsum("ia,i->a", np.conj(U_d), chi, optimize=False)
        q = overlap.real * overlap.real + overlap.imag * overlap.imag
        w = np.einsum("a,b->ab", q, q, optimize=False)
        shifts = E_d - e2
        offset = 2.0 * Ud + 2.0 * sigma * mu0
        D = offset + shifts[:, np.newaxis] + shifts[np.newaxis, :]
        weight_sum = float(np.einsum("ab->", w, optimize=False))
        report = {
            "sigma": sigma,
            "d": d,
            "offset_2Ud_plus_2sigma_mu0": offset,
            "q": [float(v) for v in q],
            "w": [[float(w[a, b]) for b in range(4)] for a in range(4)],
            "D": [[float(D[a, b]) for b in range(4)] for a in range(4)],
            "weight_sum": weight_sum,
            "weight_sum_residual": abs(weight_sum - 1.0),
            "m_sigma": None,
            "r_p": None,
        }
        sector_report.append(report)
        if not (np.all(np.isfinite(q)) and np.all(np.isfinite(w))):
            failures.append(f"pair table sigma={sigma:+d}: weights are not finite")
            continue
        if not np.all(np.isfinite(D)):
            failures.append(f"pair table sigma={sigma:+d}: a denominator is not finite")
            continue
        m_sigma = float(np.min(D))
        report["m_sigma"] = m_sigma
        if not m_sigma > pos_tol:
            failures.append(
                f"pair table sigma={sigma:+d}: minimum denominator {m_sigma!r} does not "
                f"exceed pos_tol {pos_tol!r}"
            )
        if not abs(weight_sum - 1.0) <= resid_tol:
            failures.append(
                f"pair table sigma={sigma:+d}: |sum w - 1| = {abs(weight_sum - 1.0)!r} "
                f"exceeds resid_tol {resid_tol!r}"
            )
        if len(failures) > n_failures_before:
            continue
        for p in (2, 3, 5, 7):
            D_p = D ** p
            if not (np.all(np.isfinite(D_p)) and np.all(D_p > 0.0)):
                failures.append(
                    f"pair table sigma={sigma:+d}: D**{p} has a zero or non-finite entry "
                    "(overflow or underflow)"
                )
        if len(failures) > n_failures_before:
            continue
        r_p = {}
        t = w
        for p in range(1, 8):
            t = t / D
            if p in (2, 3, 5, 7):
                r_p[p] = np.float64(np.einsum("ab->", t, optimize=False))
        report["r_p"] = {f"r_{p}": float(r_p[p]) for p in (2, 3, 5, 7)}
        if not all(np.isfinite(r_p[p]) for p in (2, 3, 5, 7)):
            failures.append(f"pair table sigma={sigma:+d}: a moment r_p is not finite")
            continue
        sectors[sigma] = {"w": w, "D": D, "m": np.float64(m_sigma), "r": r_p}
    result["sectors"] = sector_report
    if failures:
        return result

    # ---- Stage 5: frequency domain |z| < m_sigma for both sigma ---------------
    result["stage_reached"] = "frequency_domain"
    for k in range(len(zs)):
        az = abs(zs[k])
        for sigma in (-1, 1):
            m_sigma = float(sectors[sigma]["m"])
            if not az < m_sigma:
                failures.append(
                    f"frequency: |z[{k}]| = {az!r} is not < m_sigma = {m_sigma!r} "
                    f"(sigma={sigma:+d})"
                )
    if failures:
        return result

    # ---- Stage 6: F, F4 and the remainder bound for every z ------------------
    result["stage_reached"] = "frequencies"
    frequency_report = []
    for k in range(len(zs)):
        z = np.complex128(zs[k])
        z2 = z * z
        z4 = z2 * z2
        az = np.abs(z)
        per_sigma = []
        for sigma in (-1, 1):
            sec = sectors[sigma]
            w = sec["w"]
            D = sec["D"]
            m = sec["m"]
            r = sec["r"]
            denom = D * (D * D - z2)
            F = 2.0 * np.einsum("ab->", w / denom, optimize=False)
            F4 = 2.0 * (r[3] + z2 * r[5] + z4 * r[7])
            ratio = (az * az) / (m * m)
            m9 = m ** 9
            az6 = az ** 6
            one_minus = 1.0 - ratio
            if (
                np.isfinite(m9)
                and m9 > 0.0
                and np.isfinite(az6)
                and np.isfinite(one_minus)
                and one_minus > 0.0
            ):
                bound = 2.0 * az6 / (m9 * one_minus)
            else:
                bound = None
                failures.append(
                    f"frequency: bound intermediate m**9 = {float(m9)!r}, |z|**6 = "
                    f"{float(az6)!r} or 1 - |z|^2/m^2 = {float(one_minus)!r} is non-finite "
                    f"or not > 0 at z[{k}], sigma={sigma:+d}"
                )
            finite = bool(
                np.all(np.isfinite(denom))
                and np.isfinite(F)
                and np.isfinite(F4)
                and (bound is None or np.isfinite(bound))
            )
            per_sigma.append(
                {
                    "sigma": sigma,
                    "F": _pair(F),
                    "F4": _pair(F4),
                    "frequency_remainder_bound": None if bound is None else float(bound),
                }
            )
            if not finite:
                failures.append(f"frequency: non-finite value at z[{k}], sigma={sigma:+d}")
        frequency_report.append(
            {"index": k, "z": _pair(zs[k]), "abs_z": float(az), "per_sigma": per_sigma}
        )
    result["frequencies"] = frequency_report
    if failures:
        return result

    result["ok"] = True
    result["stage_reached"] = "complete"
    return result
