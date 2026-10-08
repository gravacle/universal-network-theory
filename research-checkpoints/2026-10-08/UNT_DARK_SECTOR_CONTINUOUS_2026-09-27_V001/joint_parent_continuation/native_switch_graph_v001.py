"""Prospective N=4,k=2 induced-switch graph; stdout-only, no full BS evolution."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"
import hashlib
import itertools
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE / "NATIVE_SWITCH_GRAPH_V001_FROZEN.json"
CONFIG = dict(N=4, k=2, tolerance=1e-10, exact_tolerance=0.,
    dimensionless_times=(0., math.pi/(32*math.sqrt(5)), math.pi/(16*math.sqrt(5)),
        math.pi/(8*math.sqrt(5)), 3*math.pi/(16*math.sqrt(5)),
        math.pi/(4*math.sqrt(5)), 1.), output_target_bytes=1048576)
PINS = {
    "../recovered_sources/BS_MICRO_ACTION.md":
        "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
    "NATIVE_DEGREE_SWITCH_CHANNEL_V001.md":
        "bd52d3200aa758613471f9d1053a402d8c3e7560420a3da99357787acf082f23",
}


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
            raise RuntimeError("Pinned input differs: " + name)
        files[str(path.relative_to(ROOT))] = expected
    for name in ("native_switch_graph_v001.py", "NATIVE_SWITCH_GRAPH_PROTOCOL_V001.md",
                 "NATIVE_SWITCH_GRAPH_QUOTIENT_V001.md"):
        path = HERE / name
        files[str(path.relative_to(ROOT))] = sha(path)
    return dict(configuration=CONFIG, files=files)


def bits(mask):
    return np.array([[(mask >> (4*i+j)) & 1 for j in range(4)] for i in range(4)], dtype=int)


def components(matrix):
    remaining = set(range(8))
    result = []
    while remaining:
        seed = min(remaining)
        found, queue = {seed}, [seed]
        while queue:
            vertex = queue.pop()
            adjacent = ([4+j for j in range(4) if matrix[vertex,j]] if vertex < 4
                        else [i for i in range(4) if matrix[i,vertex-4]])
            for neighbor in adjacent:
                if neighbor not in found:
                    found.add(neighbor)
                    queue.append(neighbor)
        remaining -= found
        result.append(sorted(found))
    return sorted(result, key=lambda group: (len(group), group))


def run():
    start = time.perf_counter()
    counts, maxima, failures = {}, {}, []

    def check(name, left, right=0., tol=None, tag="", upper=False):
        tolerance = CONFIG["tolerance"] if tol is None else tol
        difference = np.asarray(left)-np.asarray(right)
        error = float(np.max(np.maximum(difference.real, 0.) if upper else np.abs(difference)))
        counts[name] = counts.get(name, 0)+difference.size
        maxima[name] = max(maxima.get(name, 0.), error)
        if not math.isfinite(error) or error > tolerance:
            failures.append(dict(check=name, tag=tag, error=error, tolerance=tolerance))

    row_masks = [sum(1 << j for j in pair) for pair in itertools.combinations(range(4), 2)]
    masks = []
    for row_choice in itertools.product(row_masks, repeat=4):
        mask = sum(row_choice[i] << (4*i) for i in range(4))
        matrix = bits(mask)
        if np.all(np.sum(matrix, axis=0) == 2):
            masks.append(mask)
    masks.sort()
    check("exact_census", len(masks), 90, tol=0.)
    if len(set(masks)) != 90:
        raise RuntimeError("Unexpected duplicate or missing graph")
    lookup = {mask: j for j, mask in enumerate(masks)}
    A = np.zeros((90, 90), dtype=int)
    types, graph_rows = [], []
    for index, mask in enumerate(masks):
        matrix = bits(mask)
        groups = components(matrix)
        sizes = sorted(len(g) for g in groups)
        if sizes not in ([8], [4, 4]):
            raise RuntimeError("Unexpected two-regular topology")
        kind = "C" if sizes == [8] else "D"
        types.append(kind)
        check("regular_row_degree", np.sum(matrix, axis=1), 2, tol=0., tag=str(mask))
        check("regular_column_degree", np.sum(matrix, axis=0), 2, tol=0., tag=str(mask))
        switches = []
        for i, j in itertools.combinations(range(4), 2):
            for a, b in itertools.combinations(range(4), 2):
                pattern = (matrix[i,a],matrix[i,b],matrix[j,a],matrix[j,b])
                if pattern not in ((1,0,0,1),(0,1,1,0)):
                    continue
                edge_mask = sum(1 << (4*v+u) for v,u in ((i,a),(i,b),(j,a),(j,b)))
                target = lookup[mask ^ edge_mask]
                switches.append(dict(rows=[i,j], columns=[a,b], target=target))
                A[index,target] += 1
        graph_rows.append(dict(index=index, mask=mask, topology=kind, components=groups,
                               switches=switches, neighbors=sorted(s["target"] for s in switches)))
        c4, count_formula = 0, 0
        for i, j in itertools.combinations(range(4), 2):
            common = int(matrix[i] @ matrix[j])
            c4 += common*(common-1)//2
            count_formula += (2-common)**2
        check("switch_count_common_neighbors", len(switches), count_formula, tol=0., tag=str(mask))
        check("switch_count_fourcycles", len(switches), 12+2*c4, tol=0., tag=str(mask))
        graph_rows[-1]["four_cycle_count"] = c4
    check("adjacency_symmetric", A, A.T, tol=0.)
    check("adjacency_simple", A*(A-1), tol=0.)
    check("adjacency_no_self_loop", np.diag(A), tol=0.)
    Didx = np.array([i for i, kind in enumerate(types) if kind == "D"], dtype=int)
    Cidx = np.array([i for i, kind in enumerate(types) if kind == "C"], dtype=int)
    check("D_census", len(Didx), 18, tol=0.)
    check("C_census", len(Cidx), 72, tol=0.)
    check("D_to_D", np.sum(A[Didx][:,Didx], axis=1), 0, tol=0.)
    check("D_to_C", np.sum(A[Didx][:,Cidx], axis=1), 16, tol=0.)
    check("C_to_D", np.sum(A[Cidx][:,Didx], axis=1), 4, tol=0.)
    check("C_to_C", np.sum(A[Cidx][:,Cidx], axis=1), 8, tol=0.)
    reached, queue = {0}, [0]
    while queue:
        index = queue.pop()
        for neighbor in graph_rows[index]["neighbors"]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    check("switch_configuration_graph_connected", len(reached), 90, tol=0.)
    orbit = np.zeros((90, 2))
    orbit[Didx,0], orbit[Cidx,1] = 1/math.sqrt(18), 1/math.sqrt(72)
    quotient = np.array(((0.,8.),(8.,8.)))
    check("orbit_isometry", orbit.T @ orbit, np.eye(2))
    check("exact_quotient", orbit.T @ A @ orbit, quotient)
    check("orbit_intertwining", A @ orbit, orbit @ quotient)
    eigenvalues, vectors = np.linalg.eigh(A.astype(float))
    check("full_eigen_residual", A @ vectors, vectors*eigenvalues)
    check("full_eigen_orthonormality", vectors.T @ vectors, np.eye(90))
    check("trace_identity", np.sum(eigenvalues), 0.)
    check("square_trace_identity", eigenvalues @ eigenvalues, 1152.)
    check("row_norm_spectral_bound", np.max(np.abs(eigenvalues)), 16., upper=True)
    lam = 4+4*math.sqrt(5)
    analytic_orbit_ground = np.sqrt(((1-1/math.sqrt(5))/2,(1+1/math.sqrt(5))/2))
    analytic_ground = orbit @ analytic_orbit_ground
    check("analytic_ground_normalized", analytic_ground @ analytic_ground, 1.)
    check("analytic_ground_eigenvector", A @ analytic_ground, lam*analytic_ground)
    check("positive_ground", -np.min(analytic_ground), 0., upper=True)
    ground = vectors[:,-1]
    if ground @ analytic_ground < 0:
        ground = -ground
    check("full_ground_eigenvalue", eigenvalues[-1], lam)
    check("full_ground_vector", ground, analytic_ground)
    connected_ground = float(np.sum(ground[Cidx]**2))
    check("ground_connected_probability", connected_ground, (1+1/math.sqrt(5))/2)
    per_graph_ratio = float((ground[Cidx[0]]/ground[Didx[0]])**2)
    check("per_graph_probability_ratio", per_graph_ratio, ((1+math.sqrt(5))/4)**2)
    initial = orbit[:,0]
    coeff_coherent = float(np.linalg.norm((A @ initial)[Cidx])**2)
    coeff_incoherent = float(np.sum(A[Cidx][:,Didx]**2)/18)
    check("coherent_initial_quadratic_coefficient", coeff_coherent, 64.)
    check("incoherent_initial_quadratic_coefficient", coeff_incoherent, 16.)
    check("coherent_initial_energy", initial @ A @ initial, 0.)
    check("mixture_initial_energy", np.sum(np.diag(A)[Didx])/18, 0., tol=0.)
    dynamics = []
    qvals, qvec = np.linalg.eigh(quotient)
    for tau in CONFIG["dimensionless_times"]:
        tag = str(tau)
        propagator = (vectors*np.exp(1j*tau*eigenvalues)) @ vectors.T
        state = propagator @ initial
        small = (qvec*np.exp(1j*tau*qvals)) @ qvec.T @ np.array((1.,0.))
        check("full_unitarity", propagator.conj().T @ propagator, np.eye(90), tag=tag)
        check("coherent_quotient_vector", state, orbit @ small, tag=tag)
        check("coherent_norm", np.vdot(state,state), 1., tag=tag)
        check("coherent_conserved_energy", np.vdot(state,A @ state), 0., tag=tag)
        probabilities = np.abs(state)**2
        connected = float(np.sum(probabilities[Cidx]))
        exact = .8*math.sin(4*math.sqrt(5)*tau)**2
        check("coherent_analytic_connection", connected, exact, tag=tag)
        mixture_probabilities = np.sum(np.abs(propagator[:,Didx])**2, axis=1)/18
        individual_connections = np.sum(np.abs(propagator[Cidx][:,Didx])**2, axis=0)
        check("mixture_normalized", np.sum(mixture_probabilities), 1., tag=tag)
        check("individual_D_relabeling", individual_connections, individual_connections[0], tag=tag)
        check("mixture_individual_identity", np.sum(mixture_probabilities[Cidx]),
              individual_connections[0], tag=tag)
        dynamics.append(dict(tau=tau, coherent_connected_probability=connected,
            analytic_coherent_connected_probability=exact,
            coherent_graph_probabilities=probabilities.tolist(),
            incoherent_D_connected_probability=float(np.sum(mixture_probabilities[Cidx])),
            incoherent_D_graph_probabilities=mixture_probabilities.tolist(),
            all_individual_D_connected_probabilities=individual_connections.tolist()))
    for row, amplitude in zip(graph_rows, ground):
        row["leading_ground_amplitude"] = float(amplitude)
        row["leading_ground_probability"] = float(amplitude*amplitude)
    return dict(status="COMPLETE" if not failures else "FAILED_NUMERICAL_CONTROLS",
        configuration=CONFIG, check_counts=counts, maximum_errors=maxima, failures=failures,
        graphs=graph_rows, full_adjacency_eigenvalues=eigenvalues.tolist(),
        quotient=quotient.tolist(), orbit_eigenvalues=(4-4*math.sqrt(5),lam),
        leading_ground=dict(adjacency_eigenvalue=float(eigenvalues[-1]),
            dimensionless_energy=-float(eigenvalues[-1]),
            connected_probability=connected_ground, uniform_counting_connected_probability=.8,
            connected_minus_counting=connected_ground-.8,
            C_to_D_per_configuration_probability_ratio=per_graph_ratio,
            full_adjacency_top_gap=float(eigenvalues[-1]-eigenvalues[-2])),
        source_preparation_controls=dict(coherent_D_initial_energy=0.,incoherent_D_initial_energy=0.,
            coherent_initial_quadratic_coefficient=coeff_coherent,
            incoherent_initial_quadratic_coefficient=coeff_incoherent),
        dynamics=dynamics,
        scope="Leading induced switch operator only; tau=g4*t/hbar, no microscopic coefficient chosen, no full-incidence propagation or native formation",
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
        raise RuntimeError("Prospective source freeze differs")
    payload = run()
    print(encode(dict(freeze_sha256=sha(FREEZE),
        payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload,
        within_output_target=len(encode(payload)) <= CONFIG["output_target_bytes"])).decode())
    if payload["status"] != "COMPLETE":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
