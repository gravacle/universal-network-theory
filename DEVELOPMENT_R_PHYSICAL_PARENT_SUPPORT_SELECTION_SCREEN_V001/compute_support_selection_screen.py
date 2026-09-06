#!/usr/bin/env python3
"""Exact finite checks for the F3 physical-parent support-selection screen.

This script does not add a selector.  It checks the L4/L8 cycle-cover census,
an explicit symmetry-related competitor, the classical BS06 degree-two
window, a small exact transverse-field example, and the incidence commutators
of BS09/BS11.
"""

from __future__ import annotations

import json
from collections import deque
from itertools import product
from pathlib import Path

import numpy as np


OUT = Path(__file__).with_name("RESULT.json")
TOL = 2.0e-11


def cycle_cover(size: int) -> tuple[np.ndarray, list[tuple[int, int]], list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    left = [(x, y, z) for x, y, z in product(range(size), repeat=3) if x % 2 == 0]
    right = [(x, y, z) for x, y, z in product(range(size), repeat=3) if x % 2 == 1]
    li = {v: i for i, v in enumerate(left)}
    ri = {v: i for i, v in enumerate(right)}
    edges: set[tuple[int, int]] = set()
    for u in left:
        x, y, z = u
        for xp in ((x - 1) % size, (x + 1) % size):
            edges.add((li[u], ri[(xp, y, z)]))
    adjacency = np.zeros((len(left), len(right)), dtype=np.int8)
    for i, j in edges:
        adjacency[i, j] = 1
    return adjacency, sorted(edges), left, right


def component_sizes(adjacency: np.ndarray) -> list[int]:
    m, n = adjacency.shape
    graph: list[list[int]] = [[] for _ in range(m + n)]
    for i, j in zip(*np.nonzero(adjacency)):
        graph[int(i)].append(m + int(j))
        graph[m + int(j)].append(int(i))
    seen: set[int] = set()
    sizes: list[int] = []
    for start in range(m + n):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        count = 0
        while queue:
            node = queue.popleft()
            count += 1
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        sizes.append(count)
    return sorted(sizes)


def swapped_right(adjacency: np.ndarray, a: int, b: int) -> tuple[np.ndarray, np.ndarray]:
    m = adjacency.shape[1]
    permutation = np.eye(m, dtype=np.int8)
    permutation[[a, b]] = permutation[[b, a]]
    return adjacency @ permutation.T, permutation


def classical_energy(adjacency: np.ndarray, delta: float, u_degree: float, d_star: int) -> float:
    edges = float(np.sum(adjacency))
    degrees = np.concatenate((adjacency.sum(axis=1), adjacency.sum(axis=0)))
    return delta * edges + u_degree * float(np.sum((degrees - d_star) ** 2))


def small_transverse_example() -> dict[str, float | int]:
    m = 3
    edge_count = m * m
    dimension = 1 << edge_count
    delta = 1.0
    u_degree = 1.0
    h_flip = 0.25
    diagonal = np.zeros(dimension)
    degree_two_words: list[int] = []
    for word in range(dimension):
        bits = np.array([(word >> edge) & 1 for edge in range(edge_count)], dtype=int)
        matrix = bits.reshape(m, m)
        diagonal[word] = classical_energy(matrix, delta, u_degree, 2)
        if np.all(matrix.sum(axis=0) == 2) and np.all(matrix.sum(axis=1) == 2):
            degree_two_words.append(word)

    hamiltonian = np.diag(diagonal)
    for word in range(dimension):
        for edge in range(edge_count):
            hamiltonian[word, word ^ (1 << edge)] = -h_flip
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    ground = eigenvectors[:, 0]
    if np.sum(ground) < 0:
        ground = -ground
    ground_probabilities = np.abs(ground) ** 2
    selected_probabilities = ground_probabilities[degree_two_words]

    return {
        "possible_edges": edge_count,
        "hilbert_dimension": dimension,
        "classical_ground_energy": float(np.min(diagonal)),
        "classical_ground_multiplicity": int(np.sum(np.isclose(diagonal, np.min(diagonal)))),
        "degree_two_word_count": len(degree_two_words),
        "transverse_h": h_flip,
        "transverse_ground_gap": float(eigenvalues[1] - eigenvalues[0]),
        "transverse_ground_min_amplitude": float(np.min(ground)),
        "transverse_ground_probability_spread_on_degree_two_orbit": float(
            np.max(selected_probabilities) - np.min(selected_probabilities)
        ),
        "transverse_ground_total_probability_outside_one_word": float(
            1.0 - np.max(ground_probabilities)
        ),
    }


def incidence_commutators() -> dict[str, float]:
    n_link = np.diag([0.0, 1.0])
    x_link = np.array([[0.0, 1.0], [1.0, 0.0]])
    transfer = np.array([[0.0, 1.0], [1.0, 0.0]])
    carrier_projector = np.diag([0.0, 1.0])
    incidence_observable = np.kron(n_link, np.eye(2))
    h_car = -np.kron(n_link, transfer)
    h_fb = np.kron(n_link, carrier_projector)
    h_form = np.kron(np.eye(2), transfer)
    h_flip = -np.kron(x_link, np.eye(2))

    def norm_commutator(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.max(np.abs(a @ b - b @ a)))

    return {
        "BS09_with_n_linf": norm_commutator(h_car, incidence_observable),
        "BS11_with_n_linf": norm_commutator(h_fb, incidence_observable),
        "BS10_with_n_linf": norm_commutator(h_form, incidence_observable),
        "BS06_flip_with_n_linf": norm_commutator(h_flip, incidence_observable),
    }


checks: list[tuple[bool, str]] = []
rows = []
for size in (4, 8):
    adjacency, edges, left, right = cycle_cover(size)
    m = size**3 // 2
    right_index = {v: i for i, v in enumerate(right)}
    swap_a = right_index[(1, 0, 0)]
    swap_b = right_index[(1, 0, 1)]
    competitor, permutation = swapped_right(adjacency, swap_a, swap_b)
    block_permutation = np.block(
        [
            [np.eye(m, dtype=np.int8), np.zeros((m, m), dtype=np.int8)],
            [np.zeros((m, m), dtype=np.int8), permutation],
        ]
    )
    full = np.block(
        [
            [np.zeros((m, m), dtype=np.int8), adjacency],
            [adjacency.T, np.zeros((m, m), dtype=np.int8)],
        ]
    )
    full_competitor = np.block(
        [
            [np.zeros((m, m), dtype=np.int8), competitor],
            [competitor.T, np.zeros((m, m), dtype=np.int8)],
        ]
    )
    source_occupations = np.concatenate((np.zeros(m), np.full(m, 0.5)))
    source_occupations_swapped = source_occupations.copy()
    source_occupations_swapped[m + swap_a], source_occupations_swapped[m + swap_b] = (
        source_occupations[m + swap_b],
        source_occupations[m + swap_a],
    )

    checks.extend(
        [
            (len(left) == m and len(right) == m, f"L{size} equal F3 layer census"),
            (len(edges) == size**3 == 2 * m, f"L{size} cycle-cover edge census"),
            (np.all(adjacency.sum(axis=0) == 2) and np.all(adjacency.sum(axis=1) == 2), f"L{size} degree two"),
            (component_sizes(adjacency) == [size] * (size**2), f"L{size} cycle decomposition"),
            (not np.array_equal(adjacency, competitor), f"L{size} explicit distinct relabeling"),
            (np.all(competitor.sum(axis=0) == 2) and np.all(competitor.sum(axis=1) == 2), f"L{size} competitor degree two"),
            (classical_energy(adjacency, 1.0, 1.0, 2) == classical_energy(competitor, 1.0, 1.0, 2), f"L{size} exact BS06 diagonal degeneracy"),
            (np.array_equal(full_competitor, block_permutation @ full @ block_permutation.T), f"L{size} parent covariance"),
            (np.array_equal(source_occupations, source_occupations_swapped), f"L{size} source pattern does not break competitor symmetry"),
        ]
    )
    rows.append(
        {
            "L": size,
            "sites_total": size**3,
            "sites_per_F3_layer": m,
            "possible_F3_links": m * m,
            "selected_cycle_edges": len(edges),
            "selected_cycles": size**2,
            "selected_degree": 2,
            "BS06_diagonal_energy_at_Delta_eq_Ud_eq_1": classical_energy(adjacency, 1.0, 1.0, 2),
            "explicit_distinct_equal_energy_competitor": True,
        }
    )

# For 0 < Delta < 2 Ud, d=2 is the unique minimum of the per-vertex
# classical BS06 cost f(d)=Ud(d-2)^2+(Delta/2)d.  This selects a degree class,
# not a labeled member of that class.
delta = 1.0
u_degree = 1.0
costs = [u_degree * (degree - 2) ** 2 + 0.5 * delta * degree for degree in range(257)]
checks.append((int(np.argmin(costs)) == 2 and costs.count(min(costs)) == 1, "classical degree-two parameter window"))

small = small_transverse_example()
checks.extend(
    [
        (small["classical_ground_multiplicity"] == 6, "K3,3 classical degree-two multiplicity"),
        (small["degree_two_word_count"] == 6, "K3,3 degree-two census"),
        (small["transverse_ground_gap"] > 1.0e-8, "active-flip finite ground uniqueness"),
        (small["transverse_ground_min_amplitude"] > 1.0e-12, "active-flip ground has every-word support"),
        (small["transverse_ground_probability_spread_on_degree_two_orbit"] < TOL, "active-flip symmetry orbit equality"),
        (small["transverse_ground_total_probability_outside_one_word"] > 0.5, "active-flip ground is not one support word"),
    ]
)

commutators = incidence_commutators()
checks.extend(
    [
        (commutators["BS09_with_n_linf"] == 0.0, "BS09 conserves incidence"),
        (commutators["BS11_with_n_linf"] == 0.0, "BS11 conserves incidence"),
        (commutators["BS10_with_n_linf"] == 0.0, "BS10 acts trivially on incidence"),
        (commutators["BS06_flip_with_n_linf"] > 0.0, "only screened BS06 term changes incidence"),
    ]
)

failures = [label for ok, label in checks if not ok]
result = {
    "schema": "R_PHYSICAL_PARENT_SUPPORT_SELECTION_SCREEN_V001",
    "classification": "EXACT_NON_SELECTION_SCREEN__DEGREE_CLASS_CAN_BE_FAVORED__LABELED_CYCLE_COVER_NOT_AUTONOMOUSLY_SELECTED",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "rows": rows,
    "classical_degree_costs_Delta_eq_Ud_eq_1": {str(i): costs[i] for i in range(7)},
    "small_exact_transverse_example": small,
    "incidence_commutators": commutators,
    "proved_boundary": {
        "BS06_h_eq_0": "TARGET_HAS_DISTINCT_SYMMETRY_RELATED_EQUAL_ENERGY_SUPPORT_WORD",
        "BS06_h_gt_0": "FINITE_IRREDUCIBLE_STOQUASTIC_GROUND_STATE_IS_UNIQUE_POSITIVE_AND_PERMUTATION_INVARIANT__NOT_AN_EXACT_WORD",
        "BS09_BS10_BS11": "COMMUTE_WITH_EVERY_INCIDENCE_OCCUPATION__DO_NOT_PREPARE_SUPPORT",
        "FPSS": "CONDITIONALLY_PREPARES_AND_PASSIVELY_RETAINS_A_SUPPLIED_PROGRAM",
    },
    "conditional_escape": "A_LABEL_ANCHORED_PORT_OR_PROGRAM_CAN_SELECT_THE_WORD_BUT_IS_THEN_THE_SELECTOR_AND_REQUIRES_COMPLETE_OWNERSHIP",
    "open": "AUTONOMOUS_LABEL_ANCHORED_SUPPORT_SELECTION_AND_COEFFICIENT_OR_CLOCK_SELECTION",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

if failures:
    raise AssertionError(failures)
print(f"PASS__R_PHYSICAL_PARENT_SUPPORT_SELECTION_SCREEN__{len(checks)}/{len(checks)}")
