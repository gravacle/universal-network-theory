#!/usr/bin/env python3
"""Frozen tiny surface-band constitutive gate; no fits or macrohistory."""
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
PROTOCOL = HERE / "SURFACE_BAND_ANISOTROPIC_GATE_V001.md"
ANCHOR = HERE / "SURFACE_BAND_SHARED_ACTION_PROPOSAL_V001.md"
RECEIPT = HERE / "SURFACE_BAND_ANISOTROPIC_GATE_V001_RESULT.json"
if RECEIPT.exists():
    raise SystemExit("Existing receipt preserved; no overwrite or rerun.")

ANALYTIC_TOL = 2e-11
FD_TOL = 2e-7
STEPS = (0.004, 0.002, 0.001)
STRETCHES = (0.75, 1.0, 2.0)
SHAPES = (-0.05, -0.02, -0.01, -0.005, -0.002, -0.001,
          0.001, 0.002, 0.005, 0.01, 0.02, 0.05)
I3 = np.eye(3)
checks = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, error, tolerance=ANALYTIC_TOL):
    error = float(error)
    checks.append({"name": name, "error": error, "tolerance": tolerance,
                   "passed": bool(math.isfinite(error) and error <= tolerance)})


def predicate(name, value):
    checks.append({"name": name, "passed": bool(value)})


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
    weights = weights / (2 * nphi * npsi)
    return {"n": n, "k": k, "l": l, "w": weights,
            "orders": [nmu, nphi, npsi], "shifts": [shift_phi, shift_psi]}


GRIDS = {"low": frames(8, 16, 16, 0.17, 0.23),
         "high": frames(16, 32, 32, 0.31, 0.47)}


def avg(values, grid):
    return float(np.dot(grid["w"], values))


def a_values(F, grid):
    C = F.T @ F
    k, l = grid["k"], grid["l"]
    c11 = np.einsum("ni,ij,nj->n", k, C, k, optimize=False)
    c22 = np.einsum("ni,ij,nj->n", l, C, l, optimize=False)
    c12 = np.einsum("ni,ij,nj->n", k, C, l, optimize=False)
    determinant = c11 * c22 - c12 * c12
    if np.min(determinant) <= 0 or np.linalg.det(F) <= 0:
        raise ValueError("Nonpositive frozen material metric.")
    return np.sqrt(c22 / determinant)


def band_energy(F, grid, b=None):
    a = a_values(F, grid)
    x = 0.0 if b is None else float(np.linalg.norm(F.T @ b))
    r = np.sqrt(a * a + x * x)
    return -avg(r + x * x / (r + x), grid)


def area_energy(F, grid):
    cofactor = np.linalg.det(F) * np.linalg.inv(F).T
    return avg(np.linalg.norm(grid["n"] @ cofactor.T, axis=1), grid)


def chi_tensor(F, grid):
    return F @ F.T * (avg(1 / a_values(F, grid), grid) / np.linalg.det(F))


def pressure_and_bulk(energy, s, grid):
    values = []
    base = energy(s * I3, grid)
    for h in STEPS:
        plus, minus = energy(s * math.exp(h) * I3, grid), energy(s * math.exp(-h) * I3, grid)
        first = (plus - minus) / (2 * h)
        second = (plus + minus - 2 * base) / (h * h)
        values.append((first, second))
    first = (4 * values[2][0] - values[1][0]) / 3
    second = (4 * values[2][1] - values[1][1]) / 3
    V = s ** 3
    return -first / (3 * V), (second - 3 * first) / (9 * V)


def material_derivatives(energy, s, grid):
    F = s * I3
    basis = np.eye(9).reshape(9, 3, 3)
    base = energy(F, grid)
    derivatives = []
    for relative_h in STEPS:
        h = relative_h * s
        plus = [energy(F + h * X, grid) for X in basis]
        minus = [energy(F - h * X, grid) for X in basis]
        gradient = (np.array(plus) - minus) / (2 * h)
        H = np.empty((9, 9))
        for i in range(9):
            H[i, i] = (plus[i] + minus[i] - 2 * base) / (h * h)
            for j in range(i):
                value = (energy(F + h * basis[i] + h * basis[j], grid)
                         - energy(F + h * basis[i] - h * basis[j], grid)
                         - energy(F - h * basis[i] + h * basis[j], grid)
                         + energy(F - h * basis[i] - h * basis[j], grid)) / (4 * h * h)
                H[i, j] = H[j, i] = value
        derivatives.append((gradient, H))
    gradient = (4 * derivatives[2][0] - derivatives[1][0]) / 3
    H = (4 * derivatives[2][1] - derivatives[1][1]) / 3
    return gradient.reshape(3, 3), H


def analytic_hessian(s, kind):
    A = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    ijkl = I3[i, j] * I3[k, l]
                    ikjl = I3[i, k] * I3[j, l]
                    iljk = I3[i, l] * I3[j, k]
                    if kind == "band":
                        A[i, j, k, l] = -(ijkl + ikjl + 6 * iljk) / (15 * s ** 3)
                    else:
                        A[i, j, k, l] = (4 * ikjl - 6 * iljk + 4 * ijkl) / 15
    return A.reshape(9, 9)


def rotation():
    axis = np.array([1., 2., 3.]) / math.sqrt(14)
    X = np.array([[0., -axis[2], axis[1]], [axis[2], 0., -axis[0]],
                  [-axis[1], axis[0], 0.]])
    return I3 + math.sin(0.37) * X + (1 - math.cos(0.37)) * (X @ X)


def source_second(F, direction, grid):
    base = band_energy(F, grid)
    D = []
    for h in STEPS:
        plus = band_energy(F, grid, h * direction)
        minus = band_energy(F, grid, -h * direction)
        D.append((plus + minus - 2 * base) / h ** 2)
    L0 = 2 * D[1] - D[0]
    L1 = 2 * D[2] - D[1]
    return (4 * L1 - L0) / 3


def run():
    result = {"grid_metadata": {}, "material": [], "isotropic_source": [],
              "angular_series": [], "anisotropic_source": [],
              "source_hessian": [], "combined_material": []}
    for label, grid in GRIDS.items():
        result["grid_metadata"][label] = {"orders": grid["orders"],
              "shifts": grid["shifts"], "frame_count": len(grid["w"])}
        check(label + "/weight", abs(np.sum(grid["w"]) - 1))
        for vname in ("n", "k", "l"):
            v = grid[vname]
            check(label + "/unit/" + vname, np.max(np.abs(np.sum(v * v, axis=1) - 1)))
            for i in range(3):
                for j in range(3):
                    check(f"{label}/{vname}/moment2/{i}{j}", abs(avg(v[:, i] * v[:, j], grid) - I3[i, j] / 3))
        for vname, wname in (("n", "k"), ("n", "l"), ("k", "l")):
            check(f"{label}/orthogonal/{vname}{wname}", np.max(np.abs(np.sum(grid[vname] * grid[wname], axis=1))))
        for i in range(3):
            check(f"{label}/k/fourth/{i}", abs(avg(grid["k"][:, i] ** 4, grid) - 1 / 5))
        for s in STRETCHES:
            F = s * I3
            check(f"{label}/iso/chi/{s}", np.max(np.abs(chi_tensor(F, grid) - I3)))
            for b in (0., .01, .1, 1., 10.):
                u = s * s * b
                r = math.sqrt(1 + u * u)
                exact = -(r + u * u / (r + u)) / s
                measured = band_energy(F, grid, np.array([b, 0., 0.]))
                check(f"{label}/iso/energy/{s}/{b}", abs(measured - exact) / max(1, abs(exact)))
                result["isotropic_source"].append({"grid": label, "s": s, "b": b,
                      "energy": measured, "analytic": exact})

    high = GRIDS["high"]
    for kind, energy in (("band", band_energy), ("area", area_energy)):
        for s in STRETCHES:
            gradient, H = material_derivatives(energy, s, high)
            exact_H = analytic_hessian(s, kind)
            exact_gradient = (I3 / (3 * s * s) if kind == "band" else 2 * s * I3 / 3)
            scale_H = max(1., np.max(np.abs(exact_H)))
            scale_gradient = max(1., np.max(np.abs(exact_gradient)))
            for i in range(9):
                check(f"{kind}/{s}/gradient/{i}", abs(gradient.ravel()[i] - exact_gradient.ravel()[i]) / scale_gradient, FD_TOL)
                for j in range(9):
                    check(f"{kind}/{s}/hessian/{i}/{j}", abs(H[i, j] - exact_H[i, j]) / scale_H, FD_TOL)
            p, K = pressure_and_bulk(energy, s, high)
            V = s ** 3
            exact_p = (-1 / (3 * V * s) if kind == "band" else -2 * s * s / (3 * V))
            exact_K = (-4 / (9 * V * s) if kind == "band" else -2 * s * s / (9 * V))
            check(f"{kind}/{s}/pressure", abs(p - exact_p) / max(1, abs(exact_p)), FD_TOL)
            check(f"{kind}/{s}/bulk", abs(K - exact_K) / max(1, abs(exact_K)), FD_TOL)
            G = s * s * H[1, 1] / V
            M = s * s * H[0, 0] / V
            exact_G = (-1 / (15 * V * s) if kind == "band" else 4 * s * s / (15 * V))
            exact_M = (-8 / (15 * V * s) if kind == "band" else 2 * s * s / (15 * V))
            check(f"{kind}/{s}/G", abs(G - exact_G), FD_TOL)
            check(f"{kind}/{s}/M", abs(M - exact_M), FD_TOL)
            check(f"{kind}/{s}/M_identity", abs(M - K - 4 * G / 3), FD_TOL)
            result["material"].append({"kind": kind, "s": s, "p": p, "K": K,
               "G": G, "M": M, "gradient": gradient.tolist(), "hessian": H.tolist(),
               "analytic_hessian": exact_H.tolist(),
               "max_normalized_H_error": float(np.max(np.abs(H - exact_H)) / scale_H)})

    for label, grid in GRIDS.items():
        series = []
        for epsilon in (.02, .01, .005):
            F = np.diag(np.exp([epsilon, -epsilon, 0.]))
            a = a_values(F, grid)
            series.append([(avg(a, grid) - 1) / (2 * epsilon ** 2),
                           (avg(1 / a, grid) - 1) / (2 * epsilon ** 2)])
        extrapolated = (4 * np.array(series[2]) - series[1]) / 3
        for j, name in enumerate(("a", "inverse_a")):
            check(f"{label}/series/{name}", abs(extrapolated[j] - 1 / 15), FD_TOL)
        result["angular_series"].append({"grid": label, "steps": [.02, .01, .005],
             "coefficients": series, "extrapolated": extrapolated.tolist(), "analytic": 1 / 15})

    for epsilon in SHAPES:
        F = np.diag(np.exp([epsilon, -epsilon, 0.]))
        lo, hi = chi_tensor(F, GRIDS["low"]), chi_tensor(F, high)
        check(f"shape/{epsilon}/grid", np.max(np.abs(hi - lo)))
        eigenvalues = np.linalg.eigvalsh(hi)
        stiffness = np.linalg.eigvalsh(I3 - hi)
        predicate(f"shape/{epsilon}/expected_supercritical", eigenvalues[-1] > 1 + abs(epsilon))
        predicate(f"shape/{epsilon}/expected_negative_field_direction", stiffness[0] < -abs(epsilon))
        result["anisotropic_source"].append({"epsilon": epsilon, "F": F.tolist(),
            "chi": hi.tolist(), "chi_eigenvalues": eigenvalues.tolist(),
            "bare_field_stiffness_eigenvalues": stiffness.tolist(),
            "positive_semidefinite": bool(stiffness[0] >= -ANALYTIC_TOL)})

    shape = np.diag(np.exp([.02, -.02, 0.]))
    R = rotation()
    check("source/left_rotation_covariance", np.max(np.abs(chi_tensor(R @ shape, high) - R @ chi_tensor(shape, high) @ R.T)))
    directions = list(I3) + [np.array([1., 1., 0.]) / math.sqrt(2),
                           np.array([1., 0., 1.]) / math.sqrt(2),
                           np.array([0., 1., 1.]) / math.sqrt(2)]
    for name, F in (("iso", I3), ("shape", shape), ("rotated_shape", R @ shape)):
        chi = chi_tensor(F, high)
        Hessian = -3 * np.linalg.det(F) * chi
        for j, direction in enumerate(directions):
            measured = source_second(F, direction, high)
            exact = float(direction @ Hessian @ direction)
            check(f"source/{name}/direction/{j}", abs(measured - exact) / max(1, abs(exact)), FD_TOL)
            result["source_hessian"].append({"state": name, "direction": direction.tolist(),
                  "measured": measured, "analytic": exact})

    for Sigma, Rvalue in ((1., 0.), (4., 0.), (8., 0.), (8., 1.), (19., 0.), (32., 0.)):
        energy = Rvalue + Sigma - 1
        h = Rvalue + Sigma / 3 - 4 / 3
        G = (4 * Sigma - 1) / 15
        M = (2 * Sigma - 8) / 15
        positive_M = M > ANALYTIC_TOL
        positive_h = h > ANALYTIC_TOL
        causal_T = G <= h + ANALYTIC_TOL
        causal_L = M <= h + ANALYTIC_TOL
        predicate(f"combined/{Sigma}/{Rvalue}/M_gate", positive_M == (Sigma > 4))
        predicate(f"combined/{Sigma}/{Rvalue}/T_gate", causal_T == (15 * Rvalue + Sigma >= 19))
        predicate(f"combined/{Sigma}/{Rvalue}/L_implication", not positive_M or causal_L)
        predicate(f"combined/{Sigma}/{Rvalue}/h_implication", not positive_M or positive_h)
        result["combined_material"].append({"Sigma": Sigma, "R": Rvalue, "s": 1.,
           "energy": energy, "active_energy": Rvalue - Sigma - 2, "h": h, "G": G, "M": M,
           "positive_M": positive_M, "positive_h": positive_h,
           "causal_T": causal_T, "causal_L": causal_L,
           "cT_squared": G / h if positive_h else None,
           "cL_squared": M / h if positive_h else None})
    return result


metadata = {"source_sha256": sha(Path(__file__)), "protocol_sha256": sha(PROTOCOL),
            "anchor_sha256": sha(ANCHOR), "pid": os.getpid(), "ppid": os.getppid(),
            "utc_started": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "numpy_version": np.__version__, "platform": sys.platform,
            "thread_environment": {key: os.environ.get(key) for key in
                ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                 "VECLIB_MAXIMUM_THREADS", "PYTHONDONTWRITEBYTECODE")}}
try:
    results = run()
    status = "ARITHMETIC_QUALIFIED_PENDING_ROOT_REVIEW" if all(c["passed"] for c in checks) else "ARITHMETIC_FAILED_PRESERVED"
    error = None
except Exception as exc:
    results = {}
    status = "EXECUTION_FAILED_PRESERVED"
    error = {"type": type(exc).__name__, "message": str(exc)}
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
peak_bytes = int(peak if sys.platform == "darwin" else peak * 1024)
payload = {"schema": "surface_band_anisotropic_gate_v001", "status": status,
           "scientific_status": "ANISOTROPIC_SOURCE_ZERO_GATE_FAILED" if results.get("anisotropic_source") and
                any(not row["positive_semidefinite"] for row in results["anisotropic_source"]) else "UNRESOLVED",
           "metadata": metadata, "wall_seconds": time.perf_counter() - START,
           "peak_rss_bytes": peak_bytes, "checks_count": len(checks),
           "checks_passed": sum(c["passed"] for c in checks), "checks": checks,
           "results": results, "execution_error": error}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
payload["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
with RECEIPT.open("x", encoding="utf-8") as stream:
    json.dump(payload, stream, indent=2, sort_keys=True, allow_nan=False)
    stream.write("\n")
    stream.flush()
    os.fsync(stream.fileno())
print(json.dumps({"status": status, "scientific_status": payload["scientific_status"],
      "checks": len(checks), "passed": payload["checks_passed"],
      "pid": metadata["pid"], "wall_seconds": payload["wall_seconds"],
      "peak_rss_bytes": peak_bytes, "canonical_payload_sha256": payload["canonical_payload_sha256"]}))
raise SystemExit(0 if status == "ARITHMETIC_QUALIFIED_PENDING_ROOT_REVIEW" else 1)
