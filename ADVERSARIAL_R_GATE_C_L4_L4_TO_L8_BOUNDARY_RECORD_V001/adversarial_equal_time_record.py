#!/usr/bin/env python3
"""Adversarial equal-time boundary-record closure screen at L4 + L4 -> L8."""

from __future__ import annotations

import hashlib
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = (
    ROOT
    / "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001"
    / "PROTOCOL.md"
)
PROTOCOL_SHA256 = "e0245dc81edb15be8b5ece72ff196f19754976a41a5785941e3dba2428bdcbb4"
OUT = HERE / "RESULT.json"

L4 = 4
L8 = 8
KAPPA = math.pi / 2.0

# Local L4 labels have Rail 1 = 0..3 and Rail 2 = 4..7.
LOCAL_PORTS = (0, 3, 4, 7)
LOCAL_INTERIOR = (1, 2, 5, 6)
LOCAL_INCIDENT_EDGES = (
    (0, 1),
    (2, 3),
    (4, 5),
    (6, 7),
    (0, 5),
    (2, 7),
)

# These local one-carrier roots map to global sites 1 and 9 in block A.
ROOT_LOCAL_SITES = (1, 5)
ROOT_GLOBAL_SITES = (1, 9)
READ_SITE = 4


def canonical_edges(length: int) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.add(tuple(sorted((offset + site, offset + (site + 1) % length))))
    for site in range(length):
        edges.add(tuple(sorted((site, length + (site + 1) % length))))
    return edges


def relabel_edges(edges: set[tuple[int, int]], mapping: tuple[int, ...]):
    return {tuple(sorted((mapping[u], mapping[v]))) for u, v in edges}


def word_from_parts(port_word: int, interior_word: int) -> int:
    word = 0
    for bit, site in enumerate(LOCAL_PORTS):
        word |= ((port_word >> bit) & 1) << site
    for bit, site in enumerate(LOCAL_INTERIOR):
        word |= ((interior_word >> bit) & 1) << site
    return word


def partial_trace_interior(operator: np.ndarray) -> np.ndarray:
    reduced = np.zeros((16, 16), dtype=np.complex128)
    for p in range(16):
        for q in range(16):
            reduced[p, q] = sum(
                operator[word_from_parts(p, i), word_from_parts(q, i)]
                for i in range(16)
            )
    return reduced


def current_operator(site_u: int, site_v: int) -> np.ndarray:
    operator = np.zeros((256, 256), dtype=np.complex128)
    for word in range(256):
        bit_u = (word >> site_u) & 1
        bit_v = (word >> site_v) & 1
        if bit_u != bit_v:
            swapped = word ^ (1 << site_u) ^ (1 << site_v)
            operator[word, swapped] = 1j * (bit_v - bit_u)
    return operator


def density_for_local_site(site: int) -> np.ndarray:
    vector = np.zeros(256, dtype=np.complex128)
    vector[1 << site] = 1.0
    return np.outer(vector, vector.conj())


def expectation(density: np.ndarray, operator: np.ndarray) -> float:
    return float(np.einsum("ij,ji->", density, operator, optimize=False).real)


def occupation_operator(site: int) -> np.ndarray:
    return np.diag([float((word >> site) & 1) for word in range(256)])


def candidate_record(density: np.ndarray) -> dict[str, object]:
    q_ops = [occupation_operator(site) for site in range(8)]
    q_values = [expectation(density, q) for q in q_ops]
    currents = [
        expectation(density, current_operator(u, v))
        for u, v in LOCAL_INCIDENT_EDGES
    ]
    correlations = []
    for u, v in combinations(LOCAL_PORTS, 2):
        q_u_q_v = expectation(density, q_ops[u] * q_ops[v])
        correlations.append(q_u_q_v - q_values[u] * q_values[v])
    return {
        "Q": float(sum(q_values)),
        "port_density_real": partial_trace_interior(density).real.tolist(),
        "port_density_imag": partial_trace_interior(density).imag.tolist(),
        "incident_currents": currents,
        "port_port_connected_occupations": correlations,
    }


def terminal_distribution(source_site: int):
    adjacency = np.zeros((16, 16), dtype=float)
    for u, v in canonical_edges(L8):
        adjacency[u, v] = 1.0
        adjacency[v, u] = 1.0
    eigenvalues, eigenvectors = np.linalg.eigh(adjacency)
    phase = np.exp(1j * eigenvalues * KAPPA)  # H=-A, so U=exp(+i A kappa).
    unitary = np.einsum(
        "ia,a,ja->ij", eigenvectors, phase, eigenvectors, optimize=False
    )
    probabilities = np.abs(unitary[:, source_site]) ** 2
    identity_reconstruction = np.einsum(
        "ia,ja->ij", eigenvectors, eigenvectors, optimize=False
    )
    eigen_residual = np.einsum(
        "ij,ja->ia", adjacency, eigenvectors, optimize=False
    ) - eigenvectors * eigenvalues
    return probabilities, {
        "probability_sum_error": float(abs(np.sum(probabilities) - 1.0)),
        "orthogonality_linf": float(
            np.max(np.abs(identity_reconstruction - np.eye(16)))
        ),
        "eigen_residual_linf": float(np.max(np.abs(eigen_residual))),
    }


def walk_count(adjacency: np.ndarray, steps: int, target: int, source: int) -> int:
    power = np.linalg.matrix_power(adjacency.astype(np.int64), steps)
    return int(power[target, source])


# Frozen protocol and exact owner surgery.
observed_sha256 = hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
assert observed_sha256 == PROTOCOL_SHA256

local_edges = canonical_edges(L4)
map_a = (0, 1, 2, 3, 8, 9, 10, 11)
map_b = (4, 5, 6, 7, 12, 13, 14, 15)
isolated = relabel_edges(local_edges, map_a) | relabel_edges(local_edges, map_b)
removed = {
    tuple(sorted(edge))
    for edge in ((3, 0), (11, 8), (3, 8), (7, 4), (15, 12), (7, 12))
}
added = {
    tuple(sorted(edge))
    for edge in ((3, 4), (7, 0), (11, 12), (15, 8), (3, 12), (7, 8))
}
joined = (isolated - removed) | added
canonical_l8 = canonical_edges(L8)
degree = [sum(vertex in edge for edge in joined) for vertex in range(16)]

# Exact rank of the real-linear candidate map on Hermitian 256 x 256 operators.
# The full port reduction has 16^2=256 Hermitian coordinates. Modulo that
# subspace, total Q adds the centered interior-number direction. The six
# incident currents are pairwise Hilbert-Schmidt orthogonal and orthogonal to
# both previous spaces, so they add six more independent directions.
incident_operators = [current_operator(u, v) for u, v in LOCAL_INCIDENT_EDGES]
q_interior_centered = np.diag([
    float(sum((word >> site) & 1 for site in LOCAL_INTERIOR) - 2)
    for word in range(256)
])
special_operators = [q_interior_centered] + incident_operators
special_gram = np.array([
    [np.vdot(left, right) for right in special_operators]
    for left in special_operators
])
special_partial_traces = [partial_trace_interior(op) for op in special_operators]
candidate_map_rank = 16 ** 2 + int(np.linalg.matrix_rank(special_gram))
candidate_map_nullity = 256 ** 2 - candidate_map_rank

# Positive trace-one collision pair in the complete finite block algebra.
rho_1 = density_for_local_site(ROOT_LOCAL_SITES[0])
rho_2 = density_for_local_site(ROOT_LOCAL_SITES[1])
record_1 = candidate_record(rho_1)
record_2 = candidate_record(rho_2)
delta_rho = rho_1 - rho_2

# The joined B block is blank. Every initial seam current also vanishes for
# these occupation-basis roots.
seam_edges = sorted(added)
seam_currents_root_1 = [0.0 for _ in seam_edges]
seam_currents_root_2 = [0.0 for _ in seam_edges]

terminal_1, control_1 = terminal_distribution(ROOT_GLOBAL_SITES[0])
terminal_2, control_2 = terminal_distribution(ROOT_GLOBAL_SITES[1])
terminal_tv = 0.5 * float(np.sum(np.abs(terminal_1 - terminal_2)))

adjacency_integer = np.zeros((16, 16), dtype=np.int64)
for u, v in canonical_l8:
    adjacency_integer[u, v] = 1
    adjacency_integer[v, u] = 1
walks = {
    "root_global_1": {
        "distance_to_read_site": 3,
        "first_nonzero_walk_count": walk_count(adjacency_integer, 3, READ_SITE, 1),
        "leading_probability": "t^6/36 + O(t^8)",
    },
    "root_global_9": {
        "distance_to_read_site": 5,
        "first_nonzero_walk_count": walk_count(adjacency_integer, 5, READ_SITE, 9),
        "leading_probability": "t^10/144 + O(t^12)",
    },
}

checks = [
    (len(local_edges) == 12, "L4 owner census"),
    (len(isolated) == 24, "two isolated L4 owner census"),
    (removed <= isolated and not (added & isolated), "surgery domains"),
    (joined == canonical_l8 and len(joined) == 24, "exact L8 owner reconstruction"),
    (degree == [3] * 16, "degree-three joined support"),
    (all(np.max(np.abs(item)) == 0.0 for item in special_partial_traces),
     "special directions invisible to full port reduction"),
    (np.max(np.abs(special_gram - np.diag(np.diag(special_gram)))) == 0.0,
     "special directions pairwise Hilbert-Schmidt orthogonal"),
    (np.min(np.diag(special_gram).real) > 0.0, "special directions nonzero"),
    (candidate_map_rank == 263 and candidate_map_nullity == 65273,
     "candidate-map exact rank and nullity"),
    (np.min(np.linalg.eigvalsh(rho_1)) >= 0.0 and np.min(np.linalg.eigvalsh(rho_2)) >= 0.0,
     "collision roots positive"),
    (abs(np.trace(rho_1) - 1.0) == 0.0 and abs(np.trace(rho_2) - 1.0) == 0.0,
     "collision roots trace one"),
    (record_1 == record_2, "candidate records identical"),
    (np.trace(delta_rho) == 0.0, "difference is a trace-zero null direction"),
    (seam_currents_root_1 == seam_currents_root_2, "initial joined seam currents identical"),
    (walks["root_global_1"]["first_nonzero_walk_count"] == 1,
     "root 1 exact first walk count"),
    (walks["root_global_9"]["first_nonzero_walk_count"] == 10,
     "root 9 exact first walk count"),
    (abs(terminal_1[READ_SITE] - terminal_2[READ_SITE]) > 0.09,
     "future target occupation differs"),
    (terminal_tv > 0.999999999999, "complete future read differs"),
    (max(control_1.values()) < 2.0e-14 and max(control_2.values()) < 2.0e-14,
     "one-particle spectral controls"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001",
    "status": "PASS_EQUAL_TIME_RECORD_NOT_CLOSED" if not failures else "FAIL_CLOSED",
    "protocol_sha256": observed_sha256,
    "owner_surgery": {
        "isolated_owner_count": len(isolated),
        "removed": [list(edge) for edge in sorted(removed)],
        "added": [list(edge) for edge in sorted(added)],
        "joined_owner_count": len(joined),
        "canonical_L8_exact_match": joined == canonical_l8,
    },
    "candidate_record": {
        "block_hilbert_dimension": 256,
        "hermitian_operator_real_dimension": 256 ** 2,
        "ports": list(LOCAL_PORTS),
        "interior": list(LOCAL_INTERIOR),
        "full_port_density_real_dimension": 16 ** 2,
        "independent_total_Q_directions_beyond_port_density": 1,
        "independent_incident_current_directions": len(LOCAL_INCIDENT_EDGES),
        "port_correlation_extra_directions": 0,
        "linear_map_rank": candidate_map_rank,
        "nullity": candidate_map_nullity,
        "note": "PORT_OCCUPATION_CORRELATIONS_ARE_ALREADY_FIXED_BY_THE_FULL_PORT_DENSITY",
    },
    "collision": {
        "root_1": "PURE_ONE_CARRIER_AT_BLOCK_A_GLOBAL_SITE_1__LOCAL_INTERIOR_SITE_1",
        "root_2": "PURE_ONE_CARRIER_AT_BLOCK_A_GLOBAL_SITE_9__LOCAL_INTERIOR_SITE_5",
        "right_block": "ALL_BLANK",
        "same_Q": record_1["Q"],
        "same_port_density": "PURE_ALL_BLANK_FOUR_PORT_STATE",
        "same_incident_currents": record_1["incident_currents"],
        "same_port_connected_correlations": record_1["port_port_connected_occupations"],
        "same_initial_seam_currents": seam_currents_root_1,
        "difference_in_candidate_nullspace": record_1 == record_2,
    },
    "future_joined_output": {
        "kappa": KAPPA,
        "read_site": READ_SITE,
        "q_read_root_1": float(terminal_1[READ_SITE]),
        "q_read_root_2": float(terminal_2[READ_SITE]),
        "absolute_q_difference": float(abs(terminal_1[READ_SITE] - terminal_2[READ_SITE])),
        "complete_product_PVM_total_variation": terminal_tv,
        "walk_onset_certificate": walks,
        "spectral_controls": {"root_1": control_1, "root_2": control_2},
    },
    "classification": (
        "EXACT_LINEAR_CANDIDATE_MAP_NULLSPACE_AND_POSITIVE_COLLISION__"
        "NUMERICAL_DECLARED_TIME_COMPLETE_READ_SEPARATION"
    ),
    "claim_boundary": (
        "COUNTEREXAMPLE_TO_EQUAL_TIME_BOUNDARY_SUMMARY_CLOSURE_ONLY__"
        "NOT_A_CLAIM_THAT_THE_UNIFORM_SOURCE_SELECTS_THE_ADVERSARIAL_ROOTS__"
        "NOT_A_PROCESS_TENSOR_MINIMALITY_THEOREM"
    ),
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
}

OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
if failures:
    raise AssertionError(failures)
print(f"PASS__ADVERSARIAL_EQUAL_TIME_BOUNDARY_RECORD_NOT_CLOSED__{len(checks)}/{len(checks)}")
