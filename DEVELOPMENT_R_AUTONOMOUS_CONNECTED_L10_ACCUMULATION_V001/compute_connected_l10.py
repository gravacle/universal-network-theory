#!/usr/bin/env python3
"""Finite-orbit L10 connected-cycle autonomous BS09 accumulation."""

from __future__ import annotations

import json
import math
import os
import resource
import time
from collections import Counter
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from numba import njit


LENGTH = 10
SITES = 2 * LENGTH
FULL_DIMENSION = 1 << SITES
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
COARSE_STEPS = 1024
FINE_STEPS = 2048
COMPONENTS = 50
ROOT = Path(__file__).resolve().parent.parent
L4_RESULT = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json"
L6_RESULT = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json"
L8_RESULT = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json"
OUT = Path(__file__).with_name("RESULT.json")
START_TIME = time.perf_counter()


@njit
def reduced_h_action(
    vector: np.ndarray,
    sources: np.ndarray,
    destinations: np.ndarray,
    coefficients: np.ndarray,
    dimension: int,
) -> np.ndarray:
    out = np.zeros(dimension, dtype=np.complex128)
    for index in range(coefficients.size):
        out[destinations[index]] += coefficients[index] * vector[sources[index]]
    return out


@njit
def reduced_current(
    vector: np.ndarray,
    left_orbits: np.ndarray,
    right_orbits: np.ndarray,
    factors: np.ndarray,
) -> float:
    value = 0.0j
    for index in range(factors.size):
        value += (
            np.conjugate(vector[left_orbits[index]])
            * (1.0j * factors[index])
            * vector[right_orbits[index]]
        )
    return value.real


def permute_word(word: int, permutation: tuple[int, ...]) -> int:
    out = 0
    for source, destination in enumerate(permutation):
        if (word >> source) & 1:
            out |= 1 << destination
    return out


def group_permutations() -> list[tuple[int, ...]]:
    permutations = []
    for reflected in (False, True):
        for shift in range(LENGTH // 2):
            permutation = []
            for layer in range(2):
                for site in range(LENGTH):
                    moved_site = (site + 2 * shift) % LENGTH
                    if reflected:
                        moved_layer = 1 - layer
                        moved_site = (-moved_site) % LENGTH
                    else:
                        moved_layer = layer
                    permutation.append(moved_layer * LENGTH + moved_site)
            permutations.append(tuple(permutation))
    if len(set(permutations)) != LENGTH:
        raise AssertionError("finite group action is not faithful")
    return permutations


edges: list[tuple[int, int, str]] = []
for layer in range(2):
    offset = layer * LENGTH
    for site in range(LENGTH):
        edges.append((offset + site, offset + (site + 1) % LENGTH, f"cycle_{layer}"))
for site in range(LENGTH):
    edges.append((site, LENGTH + (site + 1) % LENGTH, "connector"))

permutations = group_permutations()
edge_set = {frozenset((u, v)) for u, v, _ in edges}
for permutation in permutations:
    moved_edges = {
        frozenset((permutation[u], permutation[v])) for u, v, _ in edges
    }
    if moved_edges != edge_set:
        raise AssertionError("finite group does not preserve support")
if any(
    permutation[site] % 2 != site % 2
    for permutation in permutations
    for site in range(SITES)
):
    raise AssertionError("finite group does not preserve source parity")

orbit_ids = np.full(FULL_DIMENSION, -1, dtype=np.int32)
orbit_representatives = []
orbit_sizes = []
for word in range(FULL_DIMENSION):
    if orbit_ids[word] >= 0:
        continue
    orbit = sorted({permute_word(word, permutation) for permutation in permutations})
    orbit_index = len(orbit_representatives)
    orbit_ids[orbit] = orbit_index
    orbit_representatives.append(word)
    orbit_sizes.append(len(orbit))
if np.any(orbit_ids < 0):
    raise AssertionError("orbit partition incomplete")
orbit_representatives = np.array(orbit_representatives, dtype=np.int64)
orbit_sizes = np.array(orbit_sizes, dtype=np.int64)
ORBIT_DIMENSION = len(orbit_representatives)

sources = []
destinations = []
coefficients = []
for source, word_value in enumerate(orbit_representatives):
    word = int(word_value)
    counts: Counter[int] = Counter()
    for u, v, _ in edges:
        if ((word >> u) & 1) != ((word >> v) & 1):
            swapped = word ^ (1 << u) ^ (1 << v)
            counts[int(orbit_ids[swapped])] += 1
    for destination, multiplicity in sorted(counts.items()):
        sources.append(source)
        destinations.append(destination)
        coefficients.append(
            -multiplicity * math.sqrt(orbit_sizes[source] / orbit_sizes[destination])
        )
sources = np.array(sources, dtype=np.int32)
destinations = np.array(destinations, dtype=np.int32)
coefficients = np.array(coefficients, dtype=float)

# Vectorized all-entry Hermiticity check without a dense matrix.
entry_keys = sources.astype(np.int64) * ORBIT_DIMENSION + destinations
entry_order = np.argsort(entry_keys)
sorted_keys = entry_keys[entry_order]
reverse_keys = destinations.astype(np.int64) * ORBIT_DIMENSION + sources
reverse_positions = np.searchsorted(sorted_keys, reverse_keys)
if np.any(reverse_positions == len(sorted_keys)) or np.any(
    sorted_keys[reverse_positions] != reverse_keys
):
    raise AssertionError("reduced Hamiltonian has a missing reverse entry")
hermiticity_error = float(
    np.max(np.abs(coefficients - coefficients[entry_order][reverse_positions]))
)

words = np.arange(FULL_DIMENSION, dtype=np.int64)


def current_kernel(u: int, v: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    bit_u = (words >> u) & 1
    bit_v = (words >> v) & 1
    active = words[bit_u != bit_v]
    swapped = active ^ (1 << u) ^ (1 << v)
    left = orbit_ids[active]
    right = orbit_ids[swapped]
    signs = ((active >> v) & 1) - ((active >> u) & 1)
    factors = signs / np.sqrt(orbit_sizes[left] * orbit_sizes[right])
    return left, right, factors


kernels = [
    current_kernel(0, 1),
    current_kernel(1, 2),
    current_kernel(0, LENGTH + 1),
]


def h_action(vector: np.ndarray) -> np.ndarray:
    return reduced_h_action(
        vector, sources, destinations, coefficients, ORBIT_DIMENSION
    )


def current_representatives(vector: np.ndarray) -> np.ndarray:
    return np.array([reduced_current(vector, *kernel) for kernel in kernels])


def reconstruct_currents(representatives: np.ndarray) -> np.ndarray:
    cycle_even, cycle_odd, connector_even = representatives
    currents = []
    for layer in range(2):
        for site in range(LENGTH):
            if layer == 0:
                currents.append(cycle_even if site % 2 == 0 else cycle_odd)
            else:
                currents.append(-cycle_odd if site % 2 == 0 else -cycle_even)
    for site in range(LENGTH):
        currents.append(connector_even if site % 2 == 0 else -connector_even)
    return np.array(currents)


psi0 = np.zeros(ORBIT_DIMENSION, dtype=np.complex128)
even_mask = sum(1 << site for site in range(0, SITES, 2))
valid_source_orbits = (orbit_representatives & even_mask) == 0
psi0[valid_source_orbits] = (
    np.sqrt(orbit_sizes[valid_source_orbits]) / math.sqrt(1 << LENGTH)
)


def taylor_step(vector: np.ndarray, step: float) -> np.ndarray:
    out = vector.copy()
    term = vector.copy()
    for order in range(1, TAYLOR_ORDER + 1):
        term = (-1.0j * step / order) * h_action(term)
        out += term
    return out


def evolve(step_count: int) -> tuple[np.ndarray, np.ndarray]:
    step = KAPPA / step_count
    state = psi0.copy()
    representative_integrals = current_representatives(state)
    for index in range(1, step_count + 1):
        state = taylor_step(state, step)
        weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
        representative_integrals += weight * current_representatives(state)
    representative_integrals *= step / 3.0
    return state, reconstruct_currents(representative_integrals)


psi_coarse, currents_coarse = evolve(COARSE_STEPS)
psi, currents = evolve(FINE_STEPS)
state_refinement_linf = float(np.max(np.abs(psi - psi_coarse)))
current_refinement_linf = float(np.max(np.abs(currents - currents_coarse)))

probabilities0_by_word = np.abs(psi0[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
probabilities_by_word = np.abs(psi[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
probabilities_coarse_by_word = (
    np.abs(psi_coarse[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
)
q0 = np.array(
    [np.sum(probabilities0_by_word[((words >> site) & 1) == 1]) for site in range(SITES)]
)
q1 = np.array(
    [np.sum(probabilities_by_word[((words >> site) & 1) == 1]) for site in range(SITES)]
)
q1_coarse = np.array(
    [np.sum(probabilities_coarse_by_word[((words >> site) & 1) == 1]) for site in range(SITES)]
)
occupation_refinement_linf = float(np.max(np.abs(q1 - q1_coarse)))

incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0
residuals = q1 - q0 + incidence @ currents
residuals_coarse = q1_coarse - q0 + incidence @ currents_coarse

particle_numbers = np.array(
    [bin(int(word)).count("1") for word in orbit_representatives], dtype=int
)
number_law0 = np.array(
    [np.sum(np.abs(psi0[particle_numbers == count]) ** 2) for count in range(SITES + 1)]
)
number_law = np.array(
    [np.sum(np.abs(psi[particle_numbers == count]) ** 2) for count in range(SITES + 1)]
)
hpsi0 = h_action(psi0)
hpsi = h_action(psi)

connected = []
for u, v, _ in edges:
    both = ((words >> u) & 1) * ((words >> v) & 1)
    connected.append(float(np.dot(probabilities_by_word, both) - q1[u] * q1[v]))

kinds = np.array([kind for _, _, kind in edges])
connector_mask = kinds == "connector"
internal_mask = ~connector_mask
throughput_component = float(np.sum(np.abs(currents)))
connector_throughput_component = float(np.sum(np.abs(currents[connector_mask])))

l4 = json.loads(L4_RESULT.read_text())
l4_active = next(row for row in l4["rows"] if row["kappa"] == KAPPA)
l6 = json.loads(L6_RESULT.read_text())
l8 = json.loads(L8_RESULT.read_text())


def ratio_against(global_throughput: float, retained: float) -> dict[str, float]:
    this_global = COMPONENTS * throughput_component
    return {
        "throughput_total": this_global / global_throughput,
        "throughput_per_retained_record": (
            (this_global / 250.0) / (global_throughput / retained)
        ),
    }


l10_over_l4 = ratio_against(l4_active["absolute_oriented_throughput_global"], 16.0)
l10_over_l6 = ratio_against(l6["absolute_oriented_throughput_global"], 54.0)
l10_over_l8 = ratio_against(l8["absolute_oriented_throughput_global"], 128.0)

neighbors = [set() for _ in range(SITES)]
for u, v, _ in edges:
    neighbors[u].add(v)
    neighbors[v].add(u)
visited = {0}
frontier = [0]
while frontier:
    vertex = frontier.pop()
    for neighbor in neighbors[vertex] - visited:
        visited.add(neighbor)
        frontier.append(neighbor)

expected_histogram = {1: 4, 2: 6, 5: 1020, 10: 104346}
observed_histogram = dict(sorted(Counter(orbit_sizes.tolist()).items()))
checks = [
    (SITES == 20 and FULL_DIMENSION == 1048576, "full component census"),
    (len(edges) == 30 and np.sum(connector_mask) == 10, "owner-once edge census"),
    (all(len(neighbors[vertex]) == 3 for vertex in range(SITES)), "degree-three support"),
    (len(visited) == SITES, "component connected"),
    (len(permutations) == 10 and ORBIT_DIMENSION == 105376, "finite group orbit census"),
    (observed_histogram == expected_histogram, "complete orbit histogram"),
    (len(coefficients) == 1570516 and hermiticity_error < 1.0e-14, "reduced Hamiltonian structure"),
    (COMPONENTS * SITES == 1000, "global L10 site census"),
    (COMPONENTS * len(edges) == 1500, "global owner-once edge census"),
    (int(np.sum(np.abs(currents[internal_mask]) > 1.0e-10)) == 20, "all internal currents active"),
    (int(np.sum(np.abs(currents[connector_mask]) > 1.0e-10)) == 10, "all connector currents active"),
    (connector_throughput_component > 1.0e-6, "nonzero connector throughput"),
    (abs(COMPONENTS * np.sum(q1) - 250.0) < 3.0e-8, "global retained total"),
    (state_refinement_linf < 3.0e-10, "state refinement"),
    (occupation_refinement_linf < 3.0e-10, "occupation refinement"),
    (current_refinement_linf < 3.0e-10, "current refinement"),
    (float(np.sum(np.abs(residuals))) < 8.0e-10, "fine ledger L1"),
    (float(np.max(np.abs(residuals))) < 6.0e-11, "fine ledger Linf"),
    (float(np.sum(np.abs(residuals))) <= float(np.sum(np.abs(residuals_coarse))) + 3.0e-11, "ledger refinement nonworsening"),
    (abs(np.vdot(psi, psi).real - 1.0) < 3.0e-10, "norm"),
    (abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real) < 3.0e-9, "energy"),
    (float(np.max(np.abs(number_law - number_law0))) < 3.0e-10, "number law"),
    (all(item["throughput_total"] > 0.0 for item in (l10_over_l4, l10_over_l6, l10_over_l8)), "total comparators"),
    (all(item["throughput_per_retained_record"] > 0.0 for item in (l10_over_l4, l10_over_l6, l10_over_l8)), "per-retained comparators"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001",
    "classification": "CONDITIONAL_CONNECTED_SUPPORT__UNIFORM_F3_MDC_SOURCE__AUTONOMOUS_SIMULTANEOUS_BS09__EXACT_FINITE_ORBIT_BASIS__REFINED_NUMERICAL_CURRENT_INTEGRATION",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "census": {
        "L": 10,
        "sites_global": 1000,
        "sites_per_F3_layer": 500,
        "possible_F3_links": 250000,
        "components": COMPONENTS,
        "sites_per_component": SITES,
        "internal_edges_per_component": 20,
        "connector_edges_per_component": 10,
        "selected_edges_global_owner_once": COMPONENTS * len(edges),
        "prepared_source_lineages": 500,
        "expected_retained_global": 250,
    },
    "finite_orbit_basis": {
        "full_dimension": FULL_DIMENSION,
        "finite_group_order": len(permutations),
        "orbit_dimension": ORBIT_DIMENSION,
        "orbit_size_histogram": {str(key): value for key, value in observed_histogram.items()},
        "reduced_hamiltonian_nonzero_entries": len(coefficients),
        "reduced_hamiltonian_hermiticity_error": hermiticity_error,
    },
    "parameters": {
        "kappa": KAPPA,
        "taylor_order": TAYLOR_ORDER,
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
    },
    "q_before": q0.tolist(),
    "q_after": q1.tolist(),
    "integrated_oriented_currents": currents.tolist(),
    "active_internal_supports_per_component": int(np.sum(np.abs(currents[internal_mask]) > 1.0e-10)),
    "active_connector_supports_per_component": int(np.sum(np.abs(currents[connector_mask]) > 1.0e-10)),
    "absolute_oriented_throughput_per_component": throughput_component,
    "absolute_oriented_throughput_global": COMPONENTS * throughput_component,
    "absolute_connector_throughput_per_component": connector_throughput_component,
    "absolute_connector_throughput_global": COMPONENTS * connector_throughput_component,
    "expected_retained_per_component": float(np.sum(q1)),
    "expected_retained_global": float(COMPONENTS * np.sum(q1)),
    "max_abs_connected_edge_correlation": float(np.max(np.abs(connected))),
    "record_ledger_residual_l1_per_component": float(np.sum(np.abs(residuals))),
    "record_ledger_residual_linf_per_component": float(np.max(np.abs(residuals))),
    "record_ledger_residual_l1_global_bound": float(COMPONENTS * np.sum(np.abs(residuals))),
    "coarse_record_ledger_residual_l1_per_component": float(np.sum(np.abs(residuals_coarse))),
    "state_refinement_linf": state_refinement_linf,
    "occupation_refinement_linf": occupation_refinement_linf,
    "current_refinement_linf": current_refinement_linf,
    "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
    "energy_error": float(abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real)),
    "number_law_max_change": float(np.max(np.abs(number_law - number_law0))),
    "L10_over_L4": l10_over_l4,
    "L10_over_L6": l10_over_l6,
    "L10_over_L8": l10_over_l8,
    "owner_once_action": "H_EQUALS_MINUS_T_SUM_OVER_1500_UNIQUE_EDGES_T_E__50_IDENTICAL_CONNECTED_COMPONENTS",
    "ctp_bookkeeping": "ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE",
    "support_status": "CONDITIONAL_FIXED_CONNECTED_PROGRAM__NOT_AUTONOMOUSLY_SELECTED",
    "source_status": "UNIFORM_RIGHT_HEADS_AND_BLANK_LEFT_TAILS__NO_EXTRA_ROUTING_ASYMMETRY",
    "parameter_status": "KAPPA_EQUALS_PI_OVER_TWO_IS_CONDITIONAL__T_AND_TAU_NOT_SELECTED",
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "not_claimed": "EXACT_TIME_EVOLUTION__EXACT_CURRENT_QUADRATURE__GENERIC_CONNECTED_PHASE__GRID__CONTINUUM__WARD__GRAVITY",
}


def assert_compatible(observed: object, canonical: object, path: str = "root") -> None:
    if isinstance(canonical, dict):
        if not isinstance(observed, dict) or set(observed) != set(canonical):
            raise AssertionError(f"canonical keys differ at {path}")
        for key in canonical:
            assert_compatible(observed[key], canonical[key], f"{path}.{key}")
        return
    if isinstance(canonical, list):
        if not isinstance(observed, list) or len(observed) != len(canonical):
            raise AssertionError(f"canonical list differs at {path}")
        for index, (left, right) in enumerate(zip(observed, canonical)):
            assert_compatible(left, right, f"{path}[{index}]")
        return
    if isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 8.0e-10:
            raise AssertionError(f"canonical float differs at {path}")
        return
    if observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    assert_compatible(out, json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION__{len(checks)}/{len(checks)}")
if os.environ.get("REPORT_RESOURCES") == "1":
    print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - START_TIME:.9f}")
    print(f"OBSERVED_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
