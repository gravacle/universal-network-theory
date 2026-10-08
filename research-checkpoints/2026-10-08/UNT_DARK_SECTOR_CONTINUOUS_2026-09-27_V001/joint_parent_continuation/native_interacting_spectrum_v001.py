"""Exact native N=2 incidence/source census; prospective stdout-only worker."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE / "NATIVE_INTERACTING_SPECTRUM_V001_FROZEN.json"
CONFIG = dict(record_occupancies=(0, 1), flip_strengths=(.5, .025, .0125, .00625),
    U=1., Delta=4., d_star=1., epsilon_r=1., lambda_R=.5, hbar=1.,
    operator_tolerance=1e-11, spectral_tolerance=1e-10,
    degeneracy_tolerance=1e-10, ratio_denominator_floor=1e-24,
    output_target_bytes=1048576)
PINS = {
    "../recovered_sources/BS_MICRO_ACTION.md":
        "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
    "NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md":
        "335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c",
    "native_carrier_ruler_v001.py":
        "00a09a8c3caffc0ffe8df76a54787ddc010ec4d5196bedf773c34258d656b252",
}
ORBIT_MASKS = ((0,), (1, 2, 4, 8), (6, 9), (3, 5, 10, 12),
               (7, 11, 13, 14), (15,))
ORBIT_LABELS = ("empty", "one", "two_opposite", "two_adjacent", "three", "four")


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(path):
    path = path.resolve()
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    files = {}
    for name, expected in PINS.items():
        path = (HERE / name).resolve()
        if sha(path) != expected:
            raise RuntimeError("Pinned source differs: " + name)
        files[str(path.relative_to(ROOT))] = expected
    for name in ("native_interacting_spectrum_v001.py",
                 "NATIVE_INTERACTING_SPECTRUM_PROTOCOL_V001.md",
                 "NATIVE_INTERACTING_COLLECTIVE_MODE_V001.md",
                 "NATIVE_INTERACTING_COLLECTIVE_MODE_REVIEW_V001.md"):
        path = HERE / name
        files[str(path.relative_to(ROOT))] = sha(path)
    return dict(configuration=CONFIG, orbit_masks=ORBIT_MASKS, files=files)


def comm(a, b):
    return a @ b - b @ a


def upper(a):
    return a[np.triu_indices(len(a))].tolist()


def full_operators(q, h):
    bits = np.array([[(mask >> edge) & 1 for edge in range(4)]
                     for mask in range(16)], dtype=float)
    degrees = np.column_stack((bits[:, 0] + bits[:, 1], bits[:, 2] + bits[:, 3],
                               bits[:, 0] + bits[:, 2], bits[:, 1] + bits[:, 3]))
    count = np.sum(bits, axis=1)
    # Direct BS degree/onsite/feedback construction, independent of the bright matrix.
    diagonal = (CONFIG["Delta"] * count
        + CONFIG["U"] * np.sum((degrees - CONFIG["d_star"]) ** 2, axis=1)
        + 4 * CONFIG["epsilon_r"] * q - 2 * CONFIG["lambda_R"] * q * count)
    flip = np.zeros((16, 16))
    for mask in range(16):
        for edge in range(4):
            flip[mask ^ (1 << edge), mask] += 1.
    return np.diag(diagonal) - h * flip, np.diag(count), flip, diagonal


def bright_operators(q, h):
    kappa = CONFIG["Delta"] + 2 * CONFIG["U"] * (1 - 2 * CONFIG["d_star"]) \
        - 2 * CONFIG["lambda_R"] * q
    constant = 4 * CONFIG["U"] * CONFIG["d_star"] ** 2 + 4 * CONFIG["epsilon_r"] * q
    U = CONFIG["U"]
    diagonal = constant + np.array((0, kappa, 2*kappa, 2*kappa+2*U,
                                    3*kappa+4*U, 4*kappa+8*U))
    flip = np.zeros((6, 6))
    for i, j, value in ((0, 1, 2), (1, 2, math.sqrt(2)), (1, 3, 2),
                        (2, 4, math.sqrt(2)), (3, 4, 2), (4, 5, 2)):
        flip[i, j] = flip[j, i] = value
    return np.diag(diagonal) - h * flip, np.diag((0., 1., 2., 2., 3., 4.)), flip, constant, kappa


def symmetry_bases():
    V = np.zeros((16, 6))
    for column, masks in enumerate(ORBIT_MASKS):
        V[list(masks), column] = 1 / math.sqrt(len(masks))
    W = []
    for j in range(16):
        vector = np.eye(16)[:, j].copy()
        for _ in range(2):
            vector -= V @ (V.T @ vector)
            for prior in W:
                vector -= prior * (prior @ vector)
        norm = float(np.linalg.norm(vector))
        if norm > CONFIG["operator_tolerance"]:
            W.append(vector / norm)
    if len(W) != 10:
        raise RuntimeError("Complement basis has wrong dimension")
    return V, np.column_stack(W)


def run():
    start = time.perf_counter()
    counts, maxima, failures = {}, {}, []
    rows = []

    def check(name, lhs, rhs=0., tolerance=None, tag="", upper_bound=False):
        tol = CONFIG["operator_tolerance"] if tolerance is None else float(tolerance)
        difference = np.asarray(lhs) - np.asarray(rhs)
        error = float(np.max(np.maximum(difference, 0.) if upper_bound else np.abs(difference)))
        counts[name] = counts.get(name, 0) + difference.size
        maxima[name] = max(maxima.get(name, 0.), error)
        if not math.isfinite(error) or error > tol:
            failures.append(dict(check=name, tag=tag, error=error, tolerance=tol))

    def spectrum(H, M, X, h, tag):
        energies, vectors = np.linalg.eigh(H)
        check("eigen_residual", H @ vectors, vectors * energies,
              CONFIG["spectral_tolerance"], tag)
        check("eigen_orthonormality", vectors.T @ vectors, np.eye(len(H)), tag=tag)
        groups = []
        first = 0
        while first < len(energies):
            last = first + 1
            while last < len(energies) and energies[last] - energies[first] <= CONFIG["degeneracy_tolerance"]:
                last += 1
            block = vectors[:, first:last]
            P = block @ block.T
            energy = float(np.mean(energies[first:last]))
            groups.append(dict(energy=energy, rank=last-first, P=P,
                               spread=float(energies[last-1]-energies[first])))
            first = last
        strengths = np.array([[float(np.trace(a["P"] @ M @ b["P"] @ M))
                               for b in groups] for a in groups])
        check("source_strength_positive", -strengths, upper_bound=True, tag=tag)
        check("source_strength_symmetric", strengths, strengths.T, tag=tag)
        check("projector_resolution", sum(g["P"] for g in groups), np.eye(len(H)), tag=tag)
        output_groups = []
        for j, a in enumerate(groups):
            P, E = a["P"], a["energy"]
            check("cluster_projector", P @ P, P, tag=tag)
            check("cluster_energy", H @ P, E * P, CONFIG["spectral_tolerance"], tag)
            check("source_strength_closure", np.sum(strengths[j]), np.trace(P @ M @ M), tag=tag)
            sumrule = 2 * sum((b["energy"]-E) * strengths[j, k] for k, b in enumerate(groups))
            moment = h * float(np.trace(P @ X))
            check("signed_source_sum_rule", sumrule, moment, CONFIG["spectral_tolerance"], tag)
            # Trace of the cluster's second energy derivative for H-fM. Degenerate
            # splitting is retained as a whole cluster, not assigned an eigh basis.
            curvature = 2 * sum(strengths[j, k] / (E-b["energy"])
                                for k, b in enumerate(groups) if k != j)
            output_groups.append(dict(energy=E, rank=a["rank"], spread=a["spread"],
                projector_upper=upper(P), source_expectation_trace=float(np.trace(P @ M)),
                source_energy_second_derivative_trace=float(curvature),
                source_impulse_energy_second_derivative_per_equal_mixture=moment/a["rank"]/CONFIG["hbar"]**2,
                moment_trace=moment, sumrule_trace=float(sumrule)))
        return dict(dimension=len(H), eigenvalues=energies.tolist(),
                    clusters=output_groups, source_strengths=strengths.tolist()), energies, vectors, groups

    V, W = symmetry_bases()
    PB = V @ V.T
    check("bright_isometry", V.T @ V, np.eye(6))
    check("dark_isometry", W.T @ W, np.eye(10))
    check("bright_dark_orthogonal", V.T @ W)
    check("complete_basis", PB + W @ W.T, np.eye(16))
    for q in CONFIG["record_occupancies"]:
        for h in CONFIG["flip_strengths"]:
            tag = f"q{q}:h{h}"
            H, M, X, diagonal = full_operators(q, h)
            B, MB, XB, constant, kappa = bright_operators(q, h)
            D, MD, XD = W.T @ H @ W, W.T @ M @ W, W.T @ X @ W
            check("full_Hermitian", H, H.T, tag=tag)
            check("bright_intertwining", H @ V, V @ B, tag=tag)
            check("source_intertwining", M @ V, V @ MB, tag=tag)
            check("flip_intertwining", X @ V, V @ XB, tag=tag)
            check("dark_H_leakage", V.T @ H @ W, tag=tag)
            check("dark_source_leakage", V.T @ M @ W, tag=tag)
            check("native_double_commutator", comm(M, comm(H, M)), h*X, tag=tag)
            check("source_bare_contact", np.zeros_like(H), tag=tag)
            check("flip_norm", np.linalg.norm(X, 2), 4., tag=tag)
            # Independently expand the diagonal pair cost.
            pair_diagonal = np.array([constant + kappa*mask.bit_count()
                + 2*CONFIG["U"]*sum(((mask >> i)&1)*((mask >> j)&1)
                                    for i, j in ((0,1),(0,2),(1,3),(2,3)))
                                     for mask in range(16)])
            check("degree_pair_identity", diagonal, pair_diagonal, tag=tag)
            full, ef, uf, gf = spectrum(H, M, X, h, tag+":full")
            bright, eb, ub, gb = spectrum(B, MB, XB, h, tag+":bright")
            dark, ed, _, _ = spectrum(D, MD, XD, h, tag+":dark")
            check("full_bright_dark_spectrum", ef, np.sort(np.concatenate((eb, ed))),
                  CONFIG["spectral_tolerance"], tag)
            for data, group in zip(full["clusters"], gf):
                bright_rank = float(np.trace(group["P"] @ PB))
                check("integer_bright_cluster_rank", bright_rank, round(bright_rank),
                      CONFIG["spectral_tolerance"], tag)
                data["bright_rank"] = int(round(bright_rank))
                data["dark_rank"] = data["rank"] - data["bright_rank"]
            check("ground_bright", uf[:,0] @ PB @ uf[:,0], 1., tag=tag)
            ground = uf[:,0]
            ground_mean = float(ground @ M @ ground)
            rhs = (M-ground_mean*np.eye(16)) @ ground
            derivative = np.linalg.solve(H-ef[0]*np.eye(16)+np.outer(ground,ground), rhs)
            check("ground_tangent_orthogonal", ground @ derivative, tag=tag)
            check("ground_tangent_equation", (H-ef[0]*np.eye(16)) @ derivative, rhs, tag=tag)
            susceptibility_solve = float(2*rhs @ derivative)
            susceptibility_spectral = -full["clusters"][0]["source_energy_second_derivative_trace"]
            check("ground_susceptibility_independent", susceptibility_solve, susceptibility_spectral,
                  CONFIG["spectral_tolerance"], tag)
            # Source matrix entries below have unambiguous magnitude only for simple bright levels.
            if any(g["rank"] != 1 for g in gb):
                raise RuntimeError("Unexpected bright degeneracy; retain groups and revise readout prospectively")
            bright_source = ub.T @ MB @ ub
            check("bright_source_strength_entries", np.square(bright_source),
                  bright["source_strengths"], CONFIG["spectral_tolerance"], tag)
            denominator = float(bright_source[0,1]**2)
            ratios = None if denominator <= CONFIG["ratio_denominator_floor"] else \
                (np.square(bright_source[1])/denominator).tolist()
            U = CONFIG["U"]
            coefficient = -8*U*(kappa+6*U)/(kappa*(kappa+2*U)*(kappa+4*U))
            curvature = float(eb[2]-2*eb[1]+eb[0])
            shifts = np.array((-4/kappa, 2/kappa-4/(kappa+2*U), 2/kappa-2/(kappa+4*U)))
            reference = constant + np.array((0., kappa, 2*kappa))
            gmin = min(kappa, 2*U)
            radius = gmin/16
            remainder = None
            if h < radius:
                remainder = 16*radius*(h/radius)**4/(1-(h/radius)**2)
                check("weak_flip_curvature_Cauchy", abs(curvature-coefficient*h*h), remainder,
                      CONFIG["spectral_tolerance"], tag, upper_bound=True)
                individual_bound = remainder/4
                check("weak_flip_energy_Cauchy", np.abs(eb[:3]-reference-shifts*h*h),
                      individual_bound, CONFIG["spectral_tolerance"], tag, upper_bound=True)
            empty = np.eye(16)[:,0]
            mean = float(empty @ H @ empty)
            variance = float(np.linalg.norm((H-mean*np.eye(16)) @ empty)**2)
            check("blank_link_absolute_energy", mean, constant, tag=tag)
            check("blank_link_energy_variance", variance, 4*h*h, tag=tag)
            record_delta = full_operators(1,h)[0]-full_operators(0,h)[0]
            check("record_preparation_energy_difference", record_delta, 4*np.eye(16)-M, tag=tag)
            rows.append(dict(record_occupancy=q, flip_strength=h,
                role="inherited_main" if h == .5 else "changed_flip_asymptotic_control",
                constants=dict(absolute=constant, kappa=kappa, U=U),
                full_H_upper=upper(H), bright_H_upper=upper(B), dark_H_upper=upper(D),
                dark_M_upper=upper(MD), full=full, bright=bright, dark=dark,
                ground_diagnostic=dict(mean_incidence=ground_mean,
                    passive_susceptibility=susceptibility_spectral,
                    bordered_solve_susceptibility=susceptibility_solve,
                    energy_first_source_derivative=-ground_mean,
                    energy_second_source_derivative=-susceptibility_spectral),
                blank_link_state=dict(mean_energy=mean, energy_variance=variance),
                collective_readout=dict(first_three_ordered_bright_curvature=curvature,
                    weak_flip_curvature_coefficient=coefficient,
                    curvature_divided_h_squared=curvature/(h*h),
                    curvature_remainder_bound=remainder,
                    weak_flip_energy_coefficients=shifts.tolist(),
                    observed_energy_shifts_divided_h_squared=((eb[:3]-reference)/(h*h)).tolist(),
                    source_01_squared=denominator,
                    source_from_level1_strength_ratios=ratios,
                    observed_abs_source_entries_divided_h=[abs(float(bright_source[0,1]))/h,
                        abs(float(bright_source[1,2]))/h,abs(float(bright_source[1,3]))/h],
                    weak_flip_abs_source_coefficients=[2/kappa,math.sqrt(2)/kappa,2/(kappa+2*U)])))
    check("case_census", len(rows), 8, tolerance=0.)
    return dict(status="COMPLETE" if not failures else "FAILED_NUMERICAL_CONTROLS",
        configuration=CONFIG, check_counts=counts, maximum_errors=maxima, failures=failures,
        basis=dict(full_masks=list(range(16)), edge_order=("L0R0","L0R1","L1R0","L1R1"),
            orbit_labels=ORBIT_LABELS, orbit_masks=ORBIT_MASKS, V=V.tolist(), W=W.tolist(),
            symmetric_matrix_encoding="upper triangle in numpy.triu_indices order; reflect to lower"),
        cases=rows,
        scope="Exact finite quantum spectrum and native incidence source; no formation, classical action curvature, continuum or metric identification",
        seconds=time.perf_counter()-start,
        peak_self_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("freeze", "run"):
        raise SystemExit("Use freeze or run; stdout only")
    state = snapshot()
    if sys.argv[1] == "freeze":
        print(encode(state).decode())
        return
    if encode(json.loads(FREEZE.read_text())) != encode(state):
        raise RuntimeError("Prospective freeze differs")
    payload = run()
    output = dict(freeze_sha256=sha(FREEZE),
        payload_sha256=hashlib.sha256(encode(payload)).hexdigest(), payload=payload,
        within_output_target=len(encode(payload)) <= CONFIG["output_target_bytes"])
    print(encode(output).decode())
    if payload["status"] != "COMPLETE":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
