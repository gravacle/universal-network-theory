#!/usr/bin/env python3
"""One frozen exact surface-band branch gate; no old producer execution."""
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
START = time.perf_counter()
import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "SURFACE_BAND_NONZERO_JOINT_GATE_V001.md"
RECEIPT = HERE / "SURFACE_BAND_NONZERO_JOINT_GATE_V001_RESULT.json"
CHECKPOINT_DIR = HERE / "surface_band_nonzero_joint_gate_v001_checkpoints"
INPUT_NAMES = ("SURFACE_BAND_SHARED_ACTION_PROPOSAL_V001.md",
               "SURFACE_BAND_ANISOTROPIC_GATE_V001.md",
               "surface_band_anisotropic_gate_v001.py",
               "SURFACE_BAND_ANISOTROPIC_GATE_V001_RESULT.json")
if RECEIPT.exists() or CHECKPOINT_DIR.exists():
    raise SystemExit("Existing receipt/checkpoint attempt preserved; overwrite/repeat refused.")
SIGMA, REF = 8.0, 1.0
EXACT_TOL, GRID_TOL, FD_TOL, NESTED_TOL = 2e-11, 2e-6, 2e-5, 5e-5
MARGIN = 2e-5
EPSILONS = (0., .005, .02, .1, .3, .5)
I3 = np.eye(3)
S = np.zeros((6, 3, 3))
S[0] = np.diag([1., -1., 0.]) / math.sqrt(2)
S[1] = np.diag([1., 1., -2.]) / math.sqrt(6)
for a, (i, j) in enumerate(((0, 1), (0, 2), (1, 2)), 2):
    S[a, i, j] = S[a, j, i] = 1 / math.sqrt(2)
S[5] = I3 / 3
TRACE = np.trace(S, axis1=1, axis2=2)
T = TRACE[:, None, None] * I3 - S
checks = []
PARTIAL_RESULTS = {}
CURRENT_EPSILON = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def peak_rss_bytes():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(peak if sys.platform == "darwin" else peak * 1024)


def exclusive_json(path, data):
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    sealed = dict(data)
    sealed["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    with path.open("x", encoding="utf-8") as stream:
        json.dump(sealed, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    return {"file": path.name, "raw_sha256": sha(path),
            "canonical_payload_sha256": sealed["canonical_payload_sha256"]}


def journal(event):
    with (CHECKPOINT_DIR / "journal.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, sort_keys=True, allow_nan=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def check(name, error, tol=EXACT_TOL):
    error = float(error)
    checks.append({"name": name, "error": error, "tolerance": tol,
                   "passed": bool(math.isfinite(error) and error <= tol)})


def predicate(name, value):
    checks.append({"name": name, "passed": bool(value)})


def normalized_difference(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.max(np.abs(a - b)) / max(1., np.max(np.abs(b))))


def frames(nmu, nphi, npsi, shift_phi, shift_psi):
    mu0, w0 = np.polynomial.legendre.leggauss(nmu)
    phi0 = 2 * np.pi * (np.arange(nphi) + shift_phi) / nphi
    psi0 = 2 * np.pi * (np.arange(npsi) + shift_psi) / npsi
    mu, phi, psi = np.meshgrid(mu0, phi0, psi0, indexing="ij")
    mu, phi, psi = mu.ravel(), phi.ravel(), psi.ravel()
    q = np.sqrt(1 - mu * mu)
    n = np.column_stack((q * np.cos(phi), q * np.sin(phi), mu))
    t1 = np.column_stack((mu * np.cos(phi), mu * np.sin(phi), -q))
    t2 = np.column_stack((-np.sin(phi), np.cos(phi), np.zeros_like(phi)))
    k = np.cos(psi)[:, None] * t1 + np.sin(psi)[:, None] * t2
    l = -np.sin(psi)[:, None] * t1 + np.cos(psi)[:, None] * t2
    weights = np.broadcast_to(w0[:, None, None], (nmu, nphi, npsi)).ravel()
    return {"n": n, "k": k, "l": l, "w": weights / (2 * nphi * npsi),
            "orders": [nmu, nphi, npsi], "shifts": [shift_phi, shift_psi]}


GRIDS = {}


def avg(v, grid):
    return float(np.dot(grid["w"], v))


def geometry(F, grid):
    t1, t2 = grid["k"] @ F.T, grid["l"] @ F.T
    c11 = np.sum(t1 * t1, axis=1)
    c22 = np.sum(t2 * t2, axis=1)
    c12 = np.sum(t1 * t2, axis=1)
    det = c11 * c22 - c12 * c12
    if np.min(det) <= 0 or np.linalg.det(F) <= 0:
        raise ValueError("Nonpositive retained material metric.")
    inv11, inv22, inv12 = c22 / det, c11 / det, -c12 / det
    return t1, t2, inv11, inv22, inv12, np.sqrt(inv11)


def energy(F, b, grid):
    a = geometry(F, grid)[-1]
    x = float(np.linalg.norm(F.T @ b))
    r = np.sqrt(a * a + x * x)
    V = float(np.linalg.det(F))
    cofactor = V * np.linalg.inv(F).T
    area = SIGMA * avg(np.linalg.norm(grid["n"] @ cofactor.T, axis=1), grid)
    band = -avg(r + x * x / (r + x), grid)
    field = 1.5 * V * float(b @ b)
    return REF + area + band + field


def exp_symmetric(Q):
    eigenvalues, eigenvectors = np.linalg.eigh(Q)
    return (eigenvectors * np.exp(eigenvalues)) @ eigenvectors.T


def energy_chart(F, b, y, grid):
    Q = np.einsum("a,aij->ij", y[:6], S)
    return energy(exp_symmetric(Q) @ F, b + y[6:], grid)


def field_root(F, grid):
    FF = F @ F.T
    eigenvalues, eigenvectors = np.linalg.eigh(FF)
    direction = eigenvectors[:, -1]
    if direction[np.argmax(np.abs(direction))] < 0:
        direction = -direction
    lamb = math.sqrt(float(eigenvalues[-1]))
    V = float(np.linalg.det(F))
    a = geometry(F, grid)[-1]
    coefficient = lamb * lamb / V
    def f(x):
        return coefficient * avg(1 / (np.sqrt(a * a + x * x) + x), grid)
    if f(0) <= 1 + EXACT_TOL:
        return np.zeros(3), 0., f(0) - 1
    lo, hi = 0., 1.
    for _ in range(32):
        if f(hi) < 1:
            break
        hi *= 2
    else:
        raise ValueError("Frozen positive-root bracket exhausted.")
    for _ in range(80):
        middle = (lo + hi) / 2
        if f(middle) > 1:
            lo = middle
        else:
            hi = middle
    x = (lo + hi) / 2
    return direction * (x / lamb), x, f(x) - 1


def derivatives(F, b, grid):
    V = float(np.linalg.det(F))
    t1, t2, inv11, inv22, inv12, a = geometry(F, grid)
    v = inv11[:, None] * t1 + inv12[:, None] * t2
    sv = np.einsum("aij,nj->ani", S, v, optimize=False)
    zq = -2 * np.einsum("ni,ani->an", v, sv, optimize=False)
    aq = zq / (2 * a)
    w1 = 2 * np.einsum("ni,ani->an", t1, sv, optimize=False)
    w2 = 2 * np.einsum("ni,ani->an", t2, sv, optimize=False)
    h = F.T @ b
    x = float(np.linalg.norm(h))
    r = np.sqrt(a * a + x * x)
    z = x * x / (r + x)
    band = -avg(r + z, grid)
    band_grad = np.zeros(9)
    band_H = np.zeros((9, 9))
    if x > 0:
        ha = np.vstack([F.T @ (S[A] @ b) for A in range(6)] + [F.T @ I3[i] for i in range(3)])
        yq = 2 * (ha @ h)
        xq = yq / (2 * x)
        xH = np.empty((9, 9))
        for A in range(9):
            for B in range(9):
                if A < 6 and B < 6:
                    hab = F.T @ ((S[A] @ S[B] + S[B] @ S[A]) @ b) / 2
                elif A < 6:
                    hab = F.T @ S[A] @ I3[B - 6]
                elif B < 6:
                    hab = F.T @ S[B] @ I3[A - 6]
                else:
                    hab = np.zeros(3)
                yH = 2 * float(ha[A] @ ha[B] + h @ hab)
                xH[A, B] = yH / (2 * x) - yq[A] * yq[B] / (4 * x ** 3)
        Ka = a * (r + 2 * x) / (r + x) ** 2
        Kx = 3 * x / (r + x)
        prefactor = 3 / (r * (r + x) ** 2)
        Kaa, Kax, Kxx = prefactor * x * x, -prefactor * a * x, prefactor * a * a
    else:
        xq, xH = np.zeros(9), np.zeros((9, 9))
        Ka, Kx = np.ones_like(a), np.zeros_like(a)
        Kaa, Kax, Kxx = np.zeros_like(a), np.zeros_like(a), np.zeros_like(a)
    for A in range(9):
        da = aq[A] if A < 6 else 0.
        band_grad[A] = -avg(Ka * da + Kx * xq[A], grid)
        for B in range(A + 1):
            db = aq[B] if B < 6 else 0.
            if A < 6 and B < 6:
                inverse_product = (w1[A] * (inv11 * w1[B] + inv12 * w2[B])
                                   + w2[A] * (inv12 * w1[B] + inv22 * w2[B]))
                zH = 2 * inverse_product - 4 * np.sum(sv[A] * sv[B], axis=1)
                aH = zH / (2 * a) - zq[A] * zq[B] / (4 * a ** 3)
            else:
                aH = 0.
            value = -avg(Ka * aH + Kx * xH[A, B] + Kaa * da * db
                         + Kax * (da * xq[B] + db * xq[A]) + Kxx * xq[A] * xq[B], grid)
            band_H[A, B] = band_H[B, A] = value
    if x == 0:
        band_H[6:, 6:] = -3 * (F @ F.T) * avg(1 / a, grid)

    cofactor = V * np.linalg.inv(F).T
    m = grid["n"] @ cofactor.T
    rm = np.linalg.norm(m, axis=1)
    tm = np.einsum("aij,nj->ani", T, m, optimize=False)
    mq = np.einsum("ni,ani->an", m, tm, optimize=False)
    area = SIGMA * avg(rm, grid)
    gradient, H = band_grad.copy(), band_H.copy()
    for A in range(6):
        gradient[A] += SIGMA * avg(mq[A] / rm, grid)
        for B in range(6):
            H[A, B] += SIGMA * avg(2 * np.sum(tm[A] * tm[B], axis=1) / rm
                                    - mq[A] * mq[B] / rm ** 3, grid)
    field = 1.5 * V * float(b @ b)
    gradient[:6] += TRACE * field
    gradient[6:] += 3 * V * b
    H[:6, :6] += np.outer(TRACE, TRACE) * field
    H[:6, 6:] += np.outer(TRACE, 3 * V * b)
    H[6:, :6] += np.outer(3 * V * b, TRACE)
    H[6:, 6:] += 3 * V * I3
    return {"energy": REF + area + band + field, "gradient": gradient, "H": H,
            "area": area, "band": band, "field": field, "x": x,
            "volume_identity": (2 * area + avg(r - z / 2, grid)) / 3,
            "field_energy_identity": 1.5 * avg(z, grid)}


def finite_derivatives(F, b, grid):
    nonzero = float(np.linalg.norm(b)) > 0
    steps = np.full(9, .002)
    if nonzero:
        steps[6:] = min(.002, .04 * np.linalg.norm(b))
    base = energy(F, b, grid)
    levels = []
    eye = np.eye(9)
    for level in range(3):
        h = steps / (2 ** level)
        plus = [energy_chart(F, b, h[i] * eye[i], grid) for i in range(9)]
        minus = [energy_chart(F, b, -h[i] * eye[i], grid) for i in range(9)]
        g = (np.array(plus) - minus) / (2 * h)
        H = np.zeros((9, 9))
        for i in range(9):
            H[i, i] = (plus[i] + minus[i] - 2 * base) / h[i] ** 2
            for j in range(i):
                pp = energy_chart(F, b, h[i] * eye[i] + h[j] * eye[j], grid)
                pm = energy_chart(F, b, h[i] * eye[i] - h[j] * eye[j], grid)
                mp = energy_chart(F, b, -h[i] * eye[i] + h[j] * eye[j], grid)
                mm = energy_chart(F, b, -h[i] * eye[i] - h[j] * eye[j], grid)
                H[i, j] = H[j, i] = (pp - pm - mp + mm) / (4 * h[i] * h[j])
        levels.append((g, H))
    g = (4 * levels[2][0] - levels[1][0]) / 3
    H = (4 * levels[2][1] - levels[1][1]) / 3
    if not nonzero:
        # Remove the source |b|^3 cusp error without altering material FD.
        L0 = 2 * levels[1][1][6:, 6:] - levels[0][1][6:, 6:]
        L1 = 2 * levels[2][1][6:, 6:] - levels[1][1][6:, 6:]
        H[6:, 6:] = (4 * L1 - L0) / 3
    return g, H, steps


def reduced_direction(F, b, direction, epsilon, grid):
    h0 = min(.002, .1 * epsilon)
    base = energy(F, b, grid)
    values = []
    for level in range(3):
        h = h0 / (2 ** level)
        Fp, Fm = exp_symmetric(h * direction) @ F, exp_symmetric(-h * direction) @ F
        bp = field_root(Fp, grid)[0]
        bm = field_root(Fm, grid)[0]
        values.append((energy(Fp, bp, grid) + energy(Fm, bm, grid) - 2 * base) / h ** 2)
    return (4 * values[2] - values[1]) / 3


def classification(values):
    minimum = float(np.min(values))
    return "POSITIVE" if minimum > MARGIN else "NEGATIVE" if minimum < -MARGIN else "UNRESOLVED_OR_DEGENERATE"


def run():
    global PARTIAL_RESULTS, CURRENT_EPSILON
    GRIDS.update({"low": frames(24, 48, 48, .17, .23),
                  "high": frames(32, 64, 64, .31, .47)})
    out = {"coefficients": {"B": 1., "V0": 1., "eta": 1., "Sigma": SIGMA,
            "R": REF, "four_pi_G": 1 / 3}, "states": [], "cubic_controls": [],
            "grid_metadata": {}, "source_zero_failure_preserved": True}
    PARTIAL_RESULTS = out
    old = json.loads((HERE / INPUT_NAMES[-1]).read_text())
    predicate("custody/prior_scientific_failure", old["scientific_status"] == "ANISOTROPIC_SOURCE_ZERO_GATE_FAILED")
    for label, grid in GRIDS.items():
        out["grid_metadata"][label] = {"orders": grid["orders"], "shifts": grid["shifts"], "frames": len(grid["w"])}
        check(label + "/weight", abs(np.sum(grid["w"]) - 1))
        for name in ("n", "k", "l"):
            v = grid[name]
            check(label + "/unit/" + name, np.max(np.abs(np.sum(v * v, axis=1) - 1)))
            for i in range(3):
                for j in range(3):
                    check(f"{label}/{name}/moment/{i}{j}", abs(avg(v[:, i] * v[:, j], grid) - I3[i, j] / 3))
                check(f"{label}/{name}/moment4/{i}", abs(avg(v[:, i] ** 4, grid) - .2))
        for a, b in (("n", "k"), ("n", "l"), ("k", "l")):
            check(label + "/orthogonal/" + a + b, np.max(np.abs(np.sum(grid[a] * grid[b], axis=1))))
        cubic_trace = float(np.trace(S[1] @ S[1] @ S[1]))
        quotients = []
        for h in (.02, .01, .005):
            values = []
            for sign in (1, -1):
                F = exp_symmetric(sign * h * S[1])
                a = geometry(F, grid)[-1]
                cofactor = np.linalg.det(F) * np.linalg.inv(F).T
                values.append([avg(np.linalg.norm(grid["n"] @ cofactor.T, axis=1), grid),
                               avg(a, grid), avg(1 / a, grid)])
            quotients.append((np.array(values[0]) - values[1]) / (2 * h ** 3 * cubic_trace))
        extrapolated = (4 * quotients[2] - quotients[1]) / 3
        targets = np.array([-8 / 63, 32 / 315, -32 / 315])
        for j in range(3):
            check(f"{label}/cubic/{j}", abs(extrapolated[j] - targets[j]), GRID_TOL)
        out["cubic_controls"].append({"grid": label, "trace_S_cubed": cubic_trace,
             "steps": [.02, .01, .005], "quotients": [q.tolist() for q in quotients],
             "extrapolated": extrapolated.tolist(), "targets": targets.tolist()})

    for row_index, epsilon in enumerate(EPSILONS):
        CURRENT_EPSILON = epsilon
        row_start = time.perf_counter()
        row_check_start = len(checks)
        print(json.dumps({"progress": "state", "epsilon": epsilon, "pid": os.getpid()}), flush=True)
        F = np.diag(np.exp([epsilon, -epsilon, 0.]))
        records = {}
        for label, grid in GRIDS.items():
            b, x, residual = field_root(F, grid)
            check(f"{epsilon}/{label}/root_residual", abs(residual))
            d = derivatives(F, b, grid)
            check(f"{epsilon}/{label}/energy_consistency", abs(d["energy"] - energy(F, b, grid)))
            check(f"{epsilon}/{label}/source_gradient", np.max(np.abs(d["gradient"][6:])))
            check(f"{epsilon}/{label}/volume_work_identity", abs(d["gradient"][5] - d["volume_identity"]))
            check(f"{epsilon}/{label}/field_energy_identity", abs(d["field"] - d["field_energy_identity"]))
            predicate(f"{epsilon}/{label}/nonzero_volume_support", d["gradient"][5] > EXACT_TOL)
            Hbb = d["H"][6:, 6:]
            evbb = np.linalg.eigvalsh(Hbb)
            if epsilon == 0:
                check(f"{label}/reference/source_degenerate", np.max(np.abs(Hbb)))
                check(f"{label}/reference/STF_hessian", np.max(np.abs(d["H"][:5, :5] - 62 / 15 * np.eye(5))))
                check(f"{label}/reference/volume_gradient", abs(d["gradient"][5] - 17 / 3))
                schur = None
            else:
                predicate(f"{epsilon}/{label}/positive_field_hessian", evbb[0] > MARGIN)
                singular_squared = np.diag(F @ F.T)
                a = geometry(F, grid)[-1]
                r = np.sqrt(a * a + x * x)
                radial = 3 * singular_squared[0] * x * avg(1 / (r * (r + x)), grid)
                expected_field = np.diag([radial,
                    3 * np.linalg.det(F) * (1 - singular_squared[1] / singular_squared[0]),
                    3 * np.linalg.det(F) * (1 - singular_squared[2] / singular_squared[0])])
                check(f"{epsilon}/{label}/exact_radial_transverse_field", normalized_difference(Hbb, expected_field))
                schur = d["H"][:6, :6] - d["H"][:6, 6:] @ np.linalg.solve(Hbb, d["H"][6:, :6])
            source_free = energy(F, np.zeros(3), grid)
            if epsilon > 0:
                predicate(f"{epsilon}/{label}/lower_than_same_shape_zero_field", d["energy"] < source_free)
            records[label] = {"b": b, "x": x, "d": d, "schur": schur, "source_free": source_free}
        lo, hi = records["low"], records["high"]
        for key in ("b", "x", "source_free"):
            check(f"{epsilon}/cross_grid/{key}", normalized_difference(lo[key], hi[key]), GRID_TOL)
        for key in ("energy", "gradient", "H"):
            check(f"{epsilon}/cross_grid/{key}", normalized_difference(lo["d"][key], hi["d"][key]), GRID_TOL)
        if epsilon > 0:
            check(f"{epsilon}/cross_grid/schur", normalized_difference(lo["schur"], hi["schur"]), GRID_TOL)
        fdg, fdH, steps = finite_derivatives(F, hi["b"], GRIDS["high"])
        d = hi["d"]
        scale_g = max(1., np.max(np.abs(d["gradient"])))
        scale_H = max(1., np.max(np.abs(d["H"])))
        for i in range(9):
            check(f"{epsilon}/FD/gradient/{i}", abs(fdg[i] - d["gradient"][i]) / scale_g, FD_TOL)
            for j in range(9):
                check(f"{epsilon}/FD/H/{i}/{j}", abs(fdH[i, j] - d["H"][i, j]) / scale_H, FD_TOL)
        nested = []
        if epsilon > 0:
            for A in range(5):
                measured = reduced_direction(F, hi["b"], S[A], epsilon, GRIDS["high"])
                exact = float(hi["schur"][A, A])
                check(f"{epsilon}/nested/STF/{A}", abs(measured - exact) / max(1., abs(exact)), NESTED_TOL)
                nested.append({"direction": A, "measured": measured, "analytic": exact})
        stress = sum(d["gradient"][A] * S[A] for A in range(5)) + d["gradient"][5] * I3
        stress /= np.linalg.det(F)
        full_eigs = np.linalg.eigvalsh(d["H"])
        field_eigs = np.linalg.eigvalsh(d["H"][6:, 6:])
        reduced_eigs = np.linalg.eigvalsh(hi["schur"]) if epsilon > 0 else None
        stf_eigs = np.linalg.eigvalsh(hi["schur"][:5, :5]) if epsilon > 0 else None
        out["states"].append({"epsilon": epsilon, "F": F.tolist(), "b": hi["b"].tolist(),
            "x": hi["x"], "energy": d["energy"], "area": d["area"], "band": d["band"],
            "field": d["field"], "source_free_energy_same_shape": hi["source_free"],
            "energy_difference_same_shape": d["energy"] - hi["source_free"],
            "energy_difference_isotropic_reference": d["energy"] - 8,
            "gradient": d["gradient"].tolist(), "support_stress": stress.tolist(),
            "joint_hessian": d["H"].tolist(), "FD_gradient": fdg.tolist(), "FD_hessian": fdH.tolist(),
            "FD_base_steps": steps.tolist(), "joint_eigenvalues": full_eigs.tolist(),
            "field_eigenvalues": field_eigs.tolist(), "field_curvature_status": classification(field_eigs),
            "material_schur": hi["schur"].tolist() if epsilon > 0 else None,
            "material_schur_eigenvalues": reduced_eigs.tolist() if epsilon > 0 else None,
            "STF_schur_eigenvalues": stf_eigs.tolist() if epsilon > 0 else None,
            "STF_curvature_status": classification(stf_eigs) if epsilon > 0 else "SOURCE_DEGENERATE_NO_SCHUR",
            "full_material_curvature_status": classification(reduced_eigs) if epsilon > 0 else "SOURCE_DEGENERATE_NO_SCHUR",
            "nested_controls": nested, "volume_support_gradient": d["gradient"][5],
            "tracefree_support_gradient_norm": float(np.linalg.norm(d["gradient"][:5])),
            "unforced_static_stationary": bool(np.max(np.abs(d["gradient"])) <= EXACT_TOL),
            "physical_phase_qualification": "UNQUALIFIED_SUPPORT_COMPATIBILITY_FORMATION_KINETICS"})
        row_peak = peak_rss_bytes()
        predicate(f"{epsilon}/resource/below_512MiB", row_peak < 512 * 1024 ** 2)
        checkpoint = {"schema": "surface_band_nonzero_joint_gate_v001_completed_state",
             "metadata": metadata, "row_index": row_index, "epsilon": epsilon,
             "row_wall_seconds": time.perf_counter() - row_start,
             "total_wall_seconds": time.perf_counter() - START,
             "peak_rss_bytes": row_peak, "state": out["states"][-1],
             "checks": checks[row_check_start:]}
        seal = exclusive_json(CHECKPOINT_DIR / f"state_{row_index:03d}.json", checkpoint)
        journal({"event": "completed_state", "pid": os.getpid(), "epsilon": epsilon,
                 "row_index": row_index, "row_wall_seconds": checkpoint["row_wall_seconds"],
                 "peak_rss_bytes": row_peak, **seal})
        print(json.dumps({"progress": "checkpoint_sealed", "epsilon": epsilon,
                          "row_wall_seconds": checkpoint["row_wall_seconds"],
                          "peak_rss_bytes": row_peak, **seal}), flush=True)
        if row_peak >= 512 * 1024 ** 2:
            raise MemoryError("Row sealed; 512 MiB cap reached; subsequent rows stopped.")
    return out


metadata = {"source_sha256": sha(Path(__file__)), "protocol_sha256": sha(PROTOCOL),
            "inputs_sha256": {name: sha(HERE / name) for name in INPUT_NAMES},
            "pid": os.getpid(), "ppid": os.getppid(), "platform": sys.platform,
            "utc_started": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "numpy_version": np.__version__, "thread_environment": {key: os.environ.get(key) for key in
                ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "PYTHONDONTWRITEBYTECODE")}}
print(json.dumps({"ownership": metadata, "execution": "frozen_single_worker"}), flush=True)
CHECKPOINT_DIR.mkdir()
manifest_seal = exclusive_json(CHECKPOINT_DIR / "manifest.json",
             {"schema": "surface_band_nonzero_joint_gate_v001_manifest", "metadata": metadata,
              "epsilons": EPSILONS, "coefficient_example": {"Sigma": SIGMA, "R": REF,
                    "B": 1., "V0": 1., "eta": 1., "four_pi_G": 1 / 3},
              "memory_cap_bytes": 512 * 1024 ** 2,
              "ownership": "observer_cosmography_single_local_worker",
              "automatic_resume": False})
journal({"event": "started", "pid": os.getpid(), "metadata": metadata, **manifest_seal})
try:
    results = run()
    status = "ARITHMETIC_QUALIFIED_PENDING_ROOT_REVIEW" if all(c["passed"] for c in checks) else "ARITHMETIC_FAILED_PRESERVED"
    error = None
except Exception as exc:
    results, status = PARTIAL_RESULTS, "EXECUTION_FAILED_PRESERVED"
    error = {"type": type(exc).__name__, "message": str(exc)}
    error_seal = exclusive_json(CHECKPOINT_DIR / "error.json",
          {"metadata": metadata, "epsilon_in_progress": CURRENT_EPSILON,
           "execution_error": error, "checks": checks,
           "completed_state_count": len(results.get("states", [])),
           "wall_seconds": time.perf_counter() - START, "peak_rss_bytes": peak_rss_bytes()})
    journal({"event": "execution_error", "pid": os.getpid(), **error_seal})
peak_bytes = peak_rss_bytes()
predicate("execution/memory_cap_512MiB", peak_bytes < 512 * 1024 ** 2)
if status == "ARITHMETIC_QUALIFIED_PENDING_ROOT_REVIEW" and not checks[-1]["passed"]:
    status = "ARITHMETIC_FAILED_PRESERVED"
payload = {"schema": "surface_band_nonzero_joint_gate_v001", "status": status,
           "scientific_status": "HELD_FIELD_BRANCH_TEST_UNFORCED_STATIC_VOLUME_GATE_FAILED" if results else "UNRESOLVED",
           "metadata": metadata, "wall_seconds": time.perf_counter() - START, "peak_rss_bytes": peak_bytes,
           "checks_count": len(checks), "checks_passed": sum(c["passed"] for c in checks),
           "checks": checks, "results": results, "execution_error": error}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
payload["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
with RECEIPT.open("x", encoding="utf-8") as stream:
    json.dump(payload, stream, sort_keys=True, indent=2, allow_nan=False)
    stream.write("\n")
    stream.flush()
    os.fsync(stream.fileno())
journal({"event": "completed_receipt", "pid": os.getpid(), "status": status,
         "receipt": RECEIPT.name, "raw_sha256": sha(RECEIPT),
         "canonical_payload_sha256": payload["canonical_payload_sha256"],
         "peak_rss_bytes": peak_bytes, "wall_seconds": payload["wall_seconds"]})
print(json.dumps({"status": status, "scientific_status": payload["scientific_status"],
      "checks": len(checks), "passed": payload["checks_passed"], "pid": metadata["pid"],
      "wall_seconds": payload["wall_seconds"], "peak_rss_bytes": peak_bytes,
      "canonical_payload_sha256": payload["canonical_payload_sha256"]}), flush=True)
raise SystemExit(0 if status == "ARITHMETIC_QUALIFIED_PENDING_ROOT_REVIEW" else 1)
