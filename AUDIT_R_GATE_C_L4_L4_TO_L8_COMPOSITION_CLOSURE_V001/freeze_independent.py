#!/usr/bin/env python3
"""Freeze independent L4/L8 composition-closure data from PROTOCOL.md only."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import resource
import sys
import time
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PROTOCOL = ROOT / "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/PROTOCOL.md"
OUT = HERE / "FROZEN_INDEPENDENT.json"
EXPECTED_PROTOCOL_SHA256 = "e0245dc81edb15be8b5ece72ff196f19754976a41a5785941e3dba2428bdcbb4"
KAPPA = math.pi / 2.0
LANCZOS_DIMENSIONS = {4: (32, 64), 8: (64, 96)}
SUZUKI_STEPS = {4: (256, 512), 8: (256, 512)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_edges(length: int):
    edges = []
    for rail in (0, 1):
        offset = rail * length
        for node in range(length):
            edges.append((offset + node, offset + ((node + 1) % length), f"rail_{rail + 1}"))
    for node in range(length):
        edges.append((node, length + ((node + 1) % length), "connector"))
    return edges


def relabeled_l4_block(rail_one, rail_two):
    edges = []
    for rail_name, sites in (("rail_1", rail_one), ("rail_2", rail_two)):
        for index in range(4):
            edges.append((sites[index], sites[(index + 1) % 4], rail_name))
    for index in range(4):
        edges.append((rail_one[index], rail_two[(index + 1) % 4], "connector"))
    return edges


def graph_degree(edges, sites):
    degree = [0] * sites
    for u, v, _ in edges:
        degree[u] += 1
        degree[v] += 1
    return degree


def source_state(length: int):
    sites = 2 * length
    odd_sites = [rail * length + node for rail in (0, 1) for node in range(length) if node % 2 == 1]
    state = np.zeros(1 << sites, dtype=np.complex128)
    scale = 2.0 ** (-0.5 * len(odd_sites))
    for subset in range(1 << len(odd_sites)):
        word = 0
        for index, site in enumerate(odd_sites):
            if subset & (1 << index):
                word |= 1 << site
        state[word] = scale
    return state, odd_sites


def edge_pairs(edges, sites):
    words = np.arange(1 << sites, dtype=np.int64)
    result = []
    for u, v, _ in edges:
        bu = (words >> u) & 1
        bv = (words >> v) & 1
        left = np.flatnonzero((bu == 0) & (bv == 1))
        right = left ^ (1 << u) ^ (1 << v)
        result.append((left, right))
    return result


def h_action(vector, pairs):
    out = np.zeros_like(vector)
    for left, right in pairs:
        out[left] -= vector[right]
        out[right] -= vector[left]
    return out


def build_lanczos(initial, pairs, max_dimension):
    norm = float(np.linalg.norm(initial))
    v = initial / norm
    previous = np.zeros_like(v)
    beta_previous = 0.0
    vectors = []
    alphas = []
    betas = []
    beta_next = 0.0
    for index in range(max_dimension):
        vectors.append(v.copy())
        w = h_action(v, pairs)
        if index:
            w -= beta_previous * previous
        alpha = float(np.vdot(v, w).real)
        alphas.append(alpha)
        w -= alpha * v
        basis = np.column_stack(vectors)
        # Two full reorthogonalization passes keep the projected Hermitian
        # recurrence stable without using a target-specific symmetry basis.
        for _ in range(2):
            projection = np.einsum("ij,i->j", basis.conj(), w, optimize=False)
            w -= np.einsum("ij,j->i", basis, projection, optimize=False)
        beta_next = float(np.linalg.norm(w))
        if beta_next < 2e-15 or index == max_dimension - 1:
            break
        betas.append(beta_next)
        previous = v
        v = w / beta_next
        beta_previous = beta_next
    return np.column_stack(vectors), np.array(alphas), np.array(betas), beta_next, norm


def lanczos_evolve(initial, pairs, dimension):
    basis, alphas, betas, beta_next, initial_norm = build_lanczos(initial, pairs, dimension)
    actual = len(alphas)
    tridiagonal = np.diag(alphas)
    if actual > 1:
        use_betas = betas[:actual - 1]
        tridiagonal += np.diag(use_betas, 1) + np.diag(use_betas, -1)
    values, vectors = np.linalg.eigh(tridiagonal)
    small = np.einsum(
        "ij,j->i",
        vectors,
        np.exp(-1j * values * KAPPA) * vectors[0].conj(),
        optimize=False,
    )
    state = initial_norm * np.einsum("ij,j->i", basis, small, optimize=False)
    residual_estimate = float(abs(initial_norm * beta_next * small[-1]))
    return state, {
        "requested_dimension": dimension,
        "actual_dimension": actual,
        "beta_next": beta_next,
        "exponential_residual_estimate": residual_estimate,
        "orthogonality_linf": float(np.max(np.abs(
            np.einsum("ij,ik->jk", basis.conj(), basis, optimize=False) - np.eye(actual)
        ))),
    }


def matching_indices(edges, length):
    return (
        tuple(i for i, edge in enumerate(edges) if edge[2].startswith("rail") and (edge[0] % length) % 2 == 0),
        tuple(i for i, edge in enumerate(edges) if edge[2].startswith("rail") and (edge[0] % length) % 2 == 1),
        tuple(i for i, edge in enumerate(edges) if edge[2] == "connector"),
    )


def apply_edge(state, pair, interval):
    left, right = pair
    a = state[left].copy()
    b = state[right].copy()
    c = math.cos(interval)
    s = 1j * math.sin(interval)
    state[left] = c * a + s * b
    state[right] = s * a + c * b


def apply_matching(state, pairs, matching, interval):
    for edge in matching:
        apply_edge(state, pairs[edge], interval)


def second_order(state, pairs, matchings, interval):
    apply_matching(state, pairs, matchings[0], interval / 2.0)
    apply_matching(state, pairs, matchings[1], interval / 2.0)
    apply_matching(state, pairs, matchings[2], interval)
    apply_matching(state, pairs, matchings[1], interval / 2.0)
    apply_matching(state, pairs, matchings[0], interval / 2.0)


Y1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
Y0 = -(2.0 ** (1.0 / 3.0)) / (2.0 - 2.0 ** (1.0 / 3.0))


def suzuki_evolve(initial, pairs, matchings, steps):
    state = initial.copy()
    interval = KAPPA / steps
    for _ in range(steps):
        second_order(state, pairs, matchings, Y1 * interval)
        second_order(state, pairs, matchings, Y0 * interval)
        second_order(state, pairs, matchings, Y1 * interval)
    return state


def block_matrix(state, left_sites, right_sites):
    words = np.arange(len(state), dtype=np.int64)
    left = np.zeros(len(state), dtype=np.int64)
    right = np.zeros(len(state), dtype=np.int64)
    for index, site in enumerate(left_sites):
        left |= ((words >> site) & 1) << index
    for index, site in enumerate(right_sites):
        right |= ((words >> site) & 1) << index
    matrix = np.zeros((1 << len(left_sites), 1 << len(right_sites)), dtype=np.complex128)
    matrix[left, right] = state
    return matrix


def interface_observation(state, left_sites, right_sites, solver_error_bound):
    matrix = block_matrix(state, left_sites, right_sites)
    u, singular, vh = np.linalg.svd(matrix, full_matrices=False)
    reconstruction = np.einsum("ij,j,jk->ik", u, singular, vh, optimize=False)
    tail = [float(np.linalg.norm(singular[dimension:])) for dimension in range(len(singular) + 1)]
    ranks = {
        f"threshold_{threshold:.0e}": int(np.count_nonzero(singular > threshold))
        for threshold in (1e-8, 1e-10, 1e-12, 1e-14)
    }
    return {
        "half_hilbert_dimension": len(singular),
        "singular_values": [float(value) for value in singular],
        "smallest_singular_value": float(singular[-1]),
        "largest_singular_value": float(singular[0]),
        "sum_squares": float(np.sum(singular * singular)),
        "ranks_by_absolute_threshold": ranks,
        "solver_error_bound": solver_error_bound,
        "minimum_singular_to_solver_error": float(singular[-1] / solver_error_bound),
        "full_rank_separated_from_solver_error": bool(singular[-1] > 20.0 * solver_error_bound),
        "full_rank_reconstruction_error": float(np.linalg.norm(matrix - reconstruction)),
        "optimal_frobenius_tail_error_by_retained_D": tail,
    }


def one_particle_future(edges, source_site):
    vertex_count = 1 + max(max(u, v) for u, v, _ in edges)
    hamiltonian = np.zeros((vertex_count, vertex_count), dtype=float)
    for u, v, _ in edges:
        hamiltonian[u, v] = -1.0
        hamiltonian[v, u] = -1.0
    values, vectors = np.linalg.eigh(hamiltonian)
    initial = np.zeros(vertex_count)
    initial[source_site] = 1.0
    coefficients = np.einsum("ij,i->j", vectors.conj(), initial, optimize=False)
    return np.einsum(
        "ij,j->i", vectors, np.exp(-1j * values * KAPPA) * coefficients, optimize=False
    )


started = time.perf_counter()
if sha256(PROTOCOL) != EXPECTED_PROTOCOL_SHA256:
    raise AssertionError("frozen protocol custody failure")

canonical_l8 = canonical_edges(8)
isolated = relabeled_l4_block((0, 1, 2, 3), (8, 9, 10, 11)) + relabeled_l4_block(
    (4, 5, 6, 7), (12, 13, 14, 15)
)
removed = [
    (3, 0, "rail_1"), (11, 8, "rail_2"), (3, 8, "connector"),
    (7, 4, "rail_1"), (15, 12, "rail_2"), (7, 12, "connector"),
]
added = [
    (3, 4, "rail_1"), (7, 0, "rail_1"), (11, 12, "rail_2"),
    (15, 8, "rail_2"), (3, 12, "connector"), (7, 8, "connector"),
]
composed = [edge for edge in isolated if edge not in removed] + added

topology = {
    "isolated_owner_count": len(isolated),
    "isolated_owner_unique_count": len(set(isolated)),
    "removed_owner_edges": [list(edge) for edge in removed],
    "added_owner_edges": [list(edge) for edge in added],
    "removed_all_present": all(edge in isolated for edge in removed),
    "added_all_absent_before": all(edge not in isolated for edge in added),
    "composed_owner_count": len(composed),
    "composed_unique_owner_count": len(set(composed)),
    "canonical_owner_count": len(canonical_l8),
    "composed_equals_canonical_owner_set": set(composed) == set(canonical_l8),
    "composition_order_equals_canonical": composed == canonical_l8,
    "canonical_degree_census": graph_degree(canonical_l8, 16),
    "unchanged_owner_count": len(set(isolated) & set(canonical_l8)),
    "removed_set_is_exact_difference": set(isolated) - set(canonical_l8) == set(removed),
    "added_set_is_exact_difference": set(canonical_l8) - set(isolated) == set(added),
}

source_factorization = {}
observations = {}
states = {}
for length in (4, 8):
    edges = canonical_edges(length)
    initial, odd_sites = source_state(length)
    pairs = edge_pairs(edges, 2 * length)
    matchings = matching_indices(edges, length)
    coarse_dimension, fine_dimension = LANCZOS_DIMENSIONS[length]
    lanczos_coarse, coarse_control = lanczos_evolve(initial, pairs, coarse_dimension)
    lanczos_fine, fine_control = lanczos_evolve(initial, pairs, fine_dimension)
    suzuki_coarse = suzuki_evolve(initial, pairs, matchings, SUZUKI_STEPS[length][0])
    suzuki_fine = suzuki_evolve(initial, pairs, matchings, SUZUKI_STEPS[length][1])
    lanczos_difference = float(np.linalg.norm(lanczos_fine - lanczos_coarse))
    suzuki_difference = float(np.linalg.norm(suzuki_fine - suzuki_coarse))
    cross_solver_difference = float(np.linalg.norm(lanczos_fine - suzuki_fine))
    solver_bound = max(
        fine_control["exponential_residual_estimate"],
        lanczos_difference,
        cross_solver_difference,
        2e-15,
    )
    if length == 4:
        left_sites = (0, 1, 4, 5)
        right_sites = (2, 3, 6, 7)
    else:
        left_sites = (0, 1, 2, 3, 8, 9, 10, 11)
        right_sites = (4, 5, 6, 7, 12, 13, 14, 15)
    interface = interface_observation(lanczos_fine, left_sites, right_sites, solver_bound)
    suzuki_interface = interface_observation(suzuki_fine, left_sites, right_sites, solver_bound)
    h_initial = h_action(initial, pairs)
    h_final = h_action(lanczos_fine, pairs)
    words = np.arange(len(initial), dtype=np.int64)
    numbers = np.array([bin(int(word)).count("1") for word in words])
    observations[str(length)] = {
        "L": length,
        "sites": 2 * length,
        "full_state_dimension": 1 << (2 * length),
        "boundary_state_dimension_each_side": 1 << length,
        "owner_edges": len(edges),
        "degree_census": graph_degree(edges, 2 * length),
        "source_odd_sites": odd_sites,
        "initial_norm": float(np.linalg.norm(initial)),
        "final_norm": float(np.linalg.norm(lanczos_fine)),
        "initial_number": float(np.sum(np.abs(initial) ** 2 * numbers)),
        "final_number": float(np.sum(np.abs(lanczos_fine) ** 2 * numbers)),
        "initial_energy": float(np.vdot(initial, h_initial).real),
        "final_energy": float(np.vdot(lanczos_fine, h_final).real),
        "lanczos_coarse_control": coarse_control,
        "lanczos_fine_control": fine_control,
        "lanczos_coarse_fine_state_l2": lanczos_difference,
        "suzuki_steps_coarse_fine": list(SUZUKI_STEPS[length]),
        "suzuki_coarse_fine_state_l2": suzuki_difference,
        "lanczos_fine_vs_suzuki_fine_state_l2": cross_solver_difference,
        "lanczos_interface": interface,
        "suzuki_interface": suzuki_interface,
        "singular_value_cross_solver_linf": float(np.max(np.abs(
            np.array(interface["singular_values"]) - np.array(suzuki_interface["singular_values"])
        ))),
    }
    states[length] = lanczos_fine

# Exact factorization of the L8 source into the two relabeled L4 blocks.
l4_initial, _ = source_state(4)
l8_initial, _ = source_state(8)
matrix_l8_initial = block_matrix(
    l8_initial,
    (0, 1, 2, 3, 8, 9, 10, 11),
    (4, 5, 6, 7, 12, 13, 14, 15),
)
factorized = np.einsum("i,j->ij", l4_initial, l4_initial, optimize=False)
source_factorization = {
    "matrix_linf_error": float(np.max(np.abs(matrix_l8_initial - factorized))),
    "matrix_l2_error": float(np.linalg.norm(matrix_l8_initial - factorized)),
    "left_factor_norm": float(np.linalg.norm(l4_initial)),
    "right_factor_norm": float(np.linalg.norm(l4_initial)),
}

# Lower-order equal-time boundary-record counterexample in block A. The two
# roots are computational-basis projectors with one internal particle at site
# 1 or 2. Both have vacuum on ports {0,3,8,11}, Q=1, zero currents, and zero
# connected port-occupation correlations. Their joined future port records
# differ under the canonical owner action.
ports = (0, 3, 8, 11)
root_sites = (1, 2)
port_vacuum_rdm = np.zeros((16, 16), dtype=float)
port_vacuum_rdm[0, 0] = 1.0
future_states = [one_particle_future(canonical_l8, site) for site in root_sites]
future_port_q = [[float(abs(state[site]) ** 2) for site in ports] for state in future_states]
future_q_difference = np.array(future_port_q[0]) - np.array(future_port_q[1])
counterexample = {
    "block": "A",
    "ports": list(ports),
    "internal_root_sites": list(root_sites),
    "rho_type": "COMPUTATIONAL_BASIS_PURE_PROJECTOR__POSITIVE_TRACE_ONE",
    "total_Q_both": 1,
    "port_reduced_density_matrix_both": port_vacuum_rdm.tolist(),
    "incident_owner_currents_both": "ALL_ZERO_EXACTLY_FOR_DIAGONAL_BASIS_PROJECTORS",
    "port_port_connected_occupation_correlations_both": "ALL_ZERO_EXACTLY",
    "future_time": KAPPA,
    "future_port_occupations_root_site_1": future_port_q[0],
    "future_port_occupations_root_site_2": future_port_q[1],
    "future_port_occupation_difference": [float(value) for value in future_q_difference],
    "future_port_record_linf_difference": float(np.max(np.abs(future_q_difference))),
    "verdict": "LOWER_ORDER_EQUAL_TIME_RECORD_DOES_NOT_CLOSE_FUTURE_JOINED_OUTPUT",
    "root_boundary": "LAWFUL_FINITE_BLOCK_COUNTEREXAMPLES__NOT_CLAIMED_SOURCE_SELECTED_ROOTS",
}

d4 = observations["4"]["lanczos_interface"]["ranks_by_absolute_threshold"]["threshold_1e-12"]
d8 = observations["8"]["lanczos_interface"]["ranks_by_absolute_threshold"]["threshold_1e-12"]
full_rank_certified = bool(
    observations["4"]["lanczos_interface"]["full_rank_separated_from_solver_error"]
    and observations["8"]["lanczos_interface"]["full_rank_separated_from_solver_error"]
    and d4 == 16
    and d8 == 256
)
classification = (
    "EXPONENTIAL_OBSTRUCTION__D4_16__D8_256__STOP_FOR_THEORY_REVIEW"
    if full_rank_certified
    else "UNRESOLVED__NUMERICAL_RANK_NOT_SEPARATED_FROM_SOLVER_ERROR"
)

elapsed = time.perf_counter() - started
rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes = int(rss_raw if sys.platform == "darwin" else rss_raw * 1024)
result = {
    "schema": "FROZEN_INDEPENDENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001",
    "freeze_status": "INDEPENDENT_DATA_FROZEN_BEFORE_TARGET_INSPECTION",
    "protocol_sha256": sha256(PROTOCOL),
    "base_commit": "c81241f615ada0b66ae25347286071808ecba06c",
    "scope": "L4_AND_L8_ONLY__NO_L6_OR_L12",
    "topology": topology,
    "source_factorization": source_factorization,
    "observations": observations,
    "summary": {
        "D4": d4,
        "D8": d8,
        "D8_over_D4": float(d8 / d4),
        "D4_over_2_to_L4": float(d4 / 16),
        "D8_over_2_to_L8": float(d8 / 256),
        "full_rank_certified_against_solver_error": full_rank_certified,
        "classification": classification,
        "stop_rule": "STOP_AFTER_RECORDING_AND_HOSTILE_AUDIT__NO_TRUNCATION_OR_ADDITIONAL_CLOSURE_MACHINERY",
    },
    "lower_order_boundary_record_attack": counterexample,
    "claim_boundary": {
        "owner_surgery": "ADOPTED_CONDITIONAL_JOIN__NOT_AUTONOMOUS_CROSS_SCALE_OPERATION",
        "singular_values_and_ranks": "FINITE_NUMERICAL_UNLESS_EXACT_CERTIFICATE_ADDED",
        "counterexample_roots": "LAWFUL_ALGEBRAIC_ROOTS__NOT_UNIFORM_SOURCE_ROOTS",
        "not_claimed": "CONTINUUM__WARD__METRIC__GRAVITON__MACROSCOPIC_EMERGENCE__GRAVITY",
    },
    "resources": {
        "runtime_seconds": elapsed,
        "max_rss_bytes": rss_bytes,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "numpy": np.__version__,
    },
}

if OUT.exists():
    raise AssertionError("refusing to overwrite frozen independent record")
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(f"FROZEN_INDEPENDENT_RESULT={OUT}")
print(f"CLASSIFICATION={classification}")
print(f"D4={d4}")
print(f"D8={d8}")
print(f"RUNTIME_SECONDS={elapsed:.9f}")
print(f"MAX_RSS_BYTES={rss_bytes}")
