"""One frozen C6/Q2 source test; exact record sectors, no probe target refit."""
import os
import sys
sys.dont_write_bytecode = True
for key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "NATIVE_SAME_CONTENT_STATIC_SOURCE_PROTOCOL_V001.md"
OUTPUT = HERE / "NATIVE_SAME_CONTENT_STATIC_SOURCE_V001_RESULT.json"
PIN = "8692ac563d831111dde8150f56f3ac323baeb81910200acf131da014bc7b5c63"
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
RAW_F = np.array([[1, -1, 0, 0, 0, 0], [0, 0, 1, 0, 0, -1],
                  [0, 0, 0, 1, -1, 0]], dtype=float)
F = np.array([RAW_F[0], RAW_F[1] - RAW_F[2]])
CAL = [.5, 1., 1.5, 2.]
VAL = [.75, 1.25, 1.75]
AGES = sorted(set(CAL + VAL))
PROBE_AGES = [j / 4 for j in range(1, 10)]
OP_TOL, FD_TOL, MATCH_TOL = 1e-10, 3e-7, 1e-8


def comm(a, b):
    return a @ b - b @ a


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def real_trace(a):
    return float(np.trace(a).real)


def propagator(h, x):
    e, s = np.linalg.eigh(h)
    return (s * np.exp(-1j * e * x)) @ s.T.conj()


def evolution(e, s, vs, x):
    phase = np.exp(-1j * e * x)
    u = (s * phase) @ s.T.conj()
    divided = (-1j * x * np.exp(-.5j * (e[:, None] + e[None, :]) * x)
               * np.sinc((e[:, None] - e[None, :]) * x / (2 * np.pi)))
    du = [s @ ((s.T.conj() @ v @ s) * divided) @ s.T.conj() for v in vs]
    return u, du


def main():
    if OUTPUT.exists():
        raise RuntimeError("Result exists; refusing overwrite")
    source = HERE / "NATIVE_SAME_CONTENT_OPERATIONAL_PROBE_V001.md"
    if sha(source) != PIN:
        raise RuntimeError("The source derivation changed")
    start = time.perf_counter()
    maxima, counts, failures = {}, {}, []

    def check(name, a, b=0., tol=OP_TOL):
        err = float(np.max(np.abs(np.asarray(a, dtype=complex) - b)))
        maxima[name] = max(maxima.get(name, 0.), err)
        counts[name] = counts.get(name, 0) + np.size(a)
        if not math.isfinite(err) or err > tol:
            failures.append(dict(name=name, error=err, tolerance=tol))

    masks = [m for m in range(64) if m.bit_count() == 2]
    index = {m: k for k, m in enumerate(masks)}
    dim = len(masks)
    eye = np.eye(dim)
    occ = np.array([[(m >> v) & 1 for m in masks] for v in range(6)])
    p = np.array([np.diag(v) for v in occ], dtype=float)
    transfers = []
    for u, v in EDGES:
        transfer = np.zeros((dim, dim))
        for col, m in enumerate(masks):
            if not ((m >> u) & 1) and ((m >> v) & 1):
                transfer[index[m ^ (1 << u) ^ (1 << v)], col] = 1
        transfers.append(transfer)
    hops = [a + a.T for a in transfers]
    ma, mb = occ[0] - occ[1], occ[3] - occ[4]
    wab = ma * mb
    r0, ra, rb, rab = eye / dim, np.diag(ma) / dim, np.diag(mb) / dim, np.diag(wab) / dim
    check("mixed_trace", np.trace(rab))
    check("mixed_trace_norm", np.sum(np.abs(wab)) / dim, 4 / 15)
    check("mixed_one_body_initial", occ @ wab / dim)
    check("four_arm_initial", ((1 + .2 * ma) * (1 + .3 * mb)
          - (1 + .2 * ma) - (1 + .3 * mb) + 1) / dim, .06 * wab / dim)
    source_y = np.zeros(len(AGES))
    source_k = np.zeros((len(AGES), 2))
    source_a = np.zeros(len(AGES))
    baseline_e = 0.
    # Exact integer nested commutators: column 0 native AB, 1..3 raw sources.
    exact_sums = [[0 for _ in range(4)] for _ in range(9)]
    sectors = []
    for signs in itertools.product((-1, 1), repeat=6):
        h = []
        for v in range(6):
            neighbors = [(v - 1) % 6, (v + 1) % 6]
            hv = 1.5 * p[v] - .25 * p[v] @ (p[neighbors[0]] + p[neighbors[1]])
            for k, edge in enumerate(EDGES):
                if v in edge:
                    hv = hv - .25 * hops[k]
            h.append(hv + signs[v] * (eye + p[v]) + 5 * eye)
        h = np.array(h)
        H, E = np.sum(h, axis=0), h[0] + h[1]
        direct = (1.5 * 2 * eye + 30 * eye - .5 * sum(p[u] @ p[v] for u, v in EDGES)
                  - .5 * sum(hops) + sum(signs[v] * (eye + p[v]) for v in range(6)))
        check("allocated_complete_H", H, direct)
        check("Hermitian", H, H.T)
        vs = np.einsum("av,vij->aij", F, h)
        raw_vs = np.einsum("av,vij->aij", RAW_F, h)
        e, s = np.linalg.eigh(H)
        check("eigen_residual", H @ s, s * e)
        check("eigen_orthonormal", s.T @ s, eye)
        sectors.append((H, E, vs, e, s))
        baseline_e += real_trace(r0 @ E) / 64
        check("initial_mixed_E", real_trace(rab @ E))
        # Integer controls remain exact despite constants in the energy allocation.
        check("quarter_grid_H", H * 4, np.rint(H * 4))
        H4 = np.rint(H * 4).astype(object)
        E4 = np.rint(E * 4).astype(object)
        V4 = [np.rint(v * 4).astype(object) for v in raw_vs]
        # Convert numpy's float objects to arbitrary-precision Python integers.
        H4 = np.vectorize(int, otypes=[object])(H4)
        E4 = np.vectorize(int, otypes=[object])(E4)
        V4 = [np.vectorize(int, otypes=[object])(v) for v in V4]
        A, D = E4, [np.zeros((dim, dim), dtype=object) for _ in range(3)]
        for n in range(9):
            exact_sums[n][0] += sum(int(wab[k]) * A[k, k] for k in range(dim))
            for mu in range(3):
                exact_sums[n][mu + 1] += sum(int(mb[k]) * D[mu][k, k] for k in range(dim))
            if n < 8:
                D = [comm(v, A) + comm(H4, d) for v, d in zip(V4, D)]
                A = comm(H4, A)
        for age_i, x in enumerate(AGES):
            u, du = evolution(e, s, vs, x)
            check("unitarity", u @ u.T.conj(), eye)
            abx = u @ rab @ u.T.conj()
            source_y[age_i] += real_trace(abx @ E) / 64
            source_a[age_i] += real_trace(u @ ra @ u.T.conj() @ E) / 64
            check("complete_energy_conservation", real_trace(abx @ H), real_trace(rab @ H))
            for mu, derivative in enumerate(du):
                check("unitary_derivative", derivative @ u.T.conj() + u @ derivative.T.conj())
                derivative_b = derivative @ rb @ u.T.conj() + u @ rb @ derivative.T.conj()
                source_k[age_i, mu] += real_trace(derivative_b @ E) / 64
                check("ordinary_source_null", derivative @ r0 @ u.T.conj() + u @ r0 @ derivative.T.conj())
                if x == 1.:
                    step = 2. ** -17
                    finite = (propagator(H + step * vs[mu], x)
                              - propagator(H - step * vs[mu], x)) / (2 * step)
                    check("Frechet_central_difference", derivative, finite, FD_TOL)
            # Uniform whole-system lapse: bulk derivative minus x times age derivative.
            _, dh = evolution(e, s, [H], x)
            check("uniform_dU", dh[0], -1j * x * H @ u)
            rho_bx = u @ rb @ u.T.conj()
            uniform_b = dh[0] @ rb @ u.T.conj() + u @ rb @ dh[0].T.conj()
            check("uniform_relational_clock", uniform_b, -1j * x * comm(H, rho_bx))
    check("source_A_E_reflection", source_a)
    exact = []
    for n, sums in enumerate(exact_sums):
        if n % 2:
            check("odd_Taylor_zero", sums)
            coefficients = [Fraction(0) for _ in sums]
        else:
            coefficients = [Fraction((-1) ** (n // 2) * int(v),
                            64 * dim * 4 ** (n + 1) * math.factorial(n)) for v in sums]
        exact.append(coefficients)
    check("native_E_second_coefficient", float(exact[2][0]))
    check("raw_source_second_coefficients", [float(a) for a in exact[2][1:]], [0., -1 / 120, -1 / 120])
    cal_i, val_i = [AGES.index(x) for x in CAL], [AGES.index(x) for x in VAL]
    matrix, target = source_k[cal_i], source_y[cal_i]
    left, singular, right = np.linalg.svd(matrix, full_matrices=True)
    cutoff = 1e-12 + 1e-9 * singular[0]
    rank = int(np.count_nonzero(singular > cutoff))
    condition = None if rank == 0 else float(singular[0] / singular[rank - 1])
    coefficients = np.zeros(2) if rank == 0 else right[:rank].T @ ((left[:, :rank].T @ target) / singular[:rank])
    residual = source_k @ coefficients - source_y
    max_cal, max_val = float(np.max(np.abs(residual[cal_i]))), float(np.max(np.abs(residual[val_i])))
    gate = (not failures and rank > 0 and condition <= 1e8
            and max_cal <= MATCH_TOL and max_val <= MATCH_TOL)
    result = dict(
        configuration=dict(V=6, Q=2, sector_count=64, sector_dimension=15,
            edges=EDGES, preparation_A=[0, 1], preparation_B=[3, 4], source_basis=F.tolist(),
            calibration_ages=CAL, validation_ages=VAL, probe_ages=PROBE_AGES,
            operator_tolerance=OP_TOL, finite_difference_tolerance=FD_TOL,
            source_and_probe_tolerance=MATCH_TOL, rank_absolute=1e-12, rank_relative=1e-9,
            maximum_condition=1e8, source_null_probe_tolerance=1e-10),
        evidence_hashes={p.name: sha(p) for p in (PROTOCOL, Path(__file__), source)},
        controls=dict(maxima=maxima, counts=counts, failures=failures),
        exact_energy_Taylor=[dict(power=n, native_AB=str(row[0]),
            raw_source_coefficients=[str(a) for a in row[1:]],
            reduced_source_coefficients=[str(row[1]), str(row[2] - row[3])]) for n, row in enumerate(exact)],
        source=dict(ages=AGES, baseline_E=baseline_e, target_AB=source_y.tolist(),
            ordinary_A=source_a.tolist(), matrix=source_k.tolist(), singular_values=singular.tolist(),
            rank_cutoff=float(cutoff), rank=rank, effective_condition=condition,
            least_squares_coefficients=coefficients.tolist(), residual=residual.tolist(),
            max_calibration_residual=max_cal, max_validation_residual=max_val,
            controls_and_source_gate_pass=gate),
        probe=dict(status="NOT_EVALUATED_SOURCE_GATE_FAILED", native_targets_evaluated=False))
    if gate:
        ops, names = [p[3], p[4]], ["p3", "p4"]
        for edge_idx in (2, 3, 4):
            a = transfers[edge_idx]
            ops += [(a + a.T) / 2, (a - a.T) / (2j)]
            names += [f"Re{EDGES[edge_idx]}", f"Im{EDGES[edge_idx]}"]
        pk = np.zeros((len(PROBE_AGES), len(ops), 2))
        for H, E, vs, e, s in sectors:
            for ti, x in enumerate(PROBE_AGES):
                u, du = evolution(e, s, vs, x)
                for mu, derivative in enumerate(du):
                    dr = derivative @ rb @ u.T.conj() + u @ rb @ derivative.T.conj()
                    pk[ti, :, mu] += np.array([real_trace(dr @ op) for op in ops]) / 64
        null = right[rank:].T
        null_error = float(np.max(np.abs(pk @ null))) if null.size else 0.
        if null_error > OP_TOL:
            result["probe"] = dict(status="NOT_IDENTIFIABLE", null_error=null_error,
                                   native_targets_evaluated=False)
        else:
            py = np.zeros((len(PROBE_AGES), len(ops)))
            for H, E, vs, e, s in sectors:
                for ti, x in enumerate(PROBE_AGES):
                    u, _ = evolution(e, s, [], x)
                    dr = u @ rab @ u.T.conj()
                    py[ti] += np.array([real_trace(dr @ op) for op in ops]) / 64
            prediction = pk @ coefficients
            error = float(np.max(np.abs(prediction - py)))
            result["probe"] = dict(status="PASS" if error <= MATCH_TOL else "FAIL",
                native_targets_evaluated=True, names=names, ages=PROBE_AGES,
                kernels=pk.tolist(), native=py.tolist(), prediction=prediction.tolist(),
                null_error=null_error, max_absolute_error=error)
    result["timing"] = dict(seconds=time.perf_counter() - start,
        peak_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    result["numpy_version"] = np.__version__
    result["scope"] = "Fixed six-cycle NODE reference; not full dynamic incidence or physical gravity"
    with OUTPUT.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    print(json.dumps(dict(output=str(OUTPUT), result_sha256=sha(OUTPUT),
        controls_failed=len(failures), source_gate_pass=gate, rank=rank,
        max_calibration_residual=max_cal, max_validation_residual=max_val,
        probe_status=result["probe"]["status"], seconds=result["timing"]["seconds"]), sort_keys=True))


if __name__ == "__main__":
    main()
