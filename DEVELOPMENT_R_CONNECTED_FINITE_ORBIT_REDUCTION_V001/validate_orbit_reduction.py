#!/usr/bin/env python3
"""Exact finite-group orbit reduction, cross-checked on full L4/L6/L8 records."""

from __future__ import annotations

import json
import math
import os
from collections import Counter
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from numba import njit


KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
STEPS = 2048
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
TARGETS = {
    4: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json",
    6: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json",
    8: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json",
}


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


def group_permutations(length: int) -> list[tuple[int, ...]]:
    permutations = []
    for reflected in (False, True):
        for shift in range(length // 2):
            permutation = []
            for layer in range(2):
                for site in range(length):
                    moved_site = (site + 2 * shift) % length
                    if reflected:
                        moved_layer = 1 - layer
                        moved_site = (-moved_site) % length
                    else:
                        moved_layer = layer
                    permutation.append(moved_layer * length + moved_site)
            permutations.append(tuple(permutation))
    if len(set(permutations)) != length:
        raise AssertionError("finite group action is not faithful")
    return permutations


def component_edges(length: int) -> list[tuple[int, int, str]]:
    edges = []
    for layer in range(2):
        offset = layer * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length, f"cycle_{layer}"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def build_orbits(length: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[tuple[int, ...]]]:
    dimension = 1 << (2 * length)
    permutations = group_permutations(length)
    orbit_ids = np.full(dimension, -1, dtype=np.int32)
    representatives = []
    sizes = []
    for word in range(dimension):
        if orbit_ids[word] >= 0:
            continue
        orbit = sorted({permute_word(word, permutation) for permutation in permutations})
        orbit_index = len(representatives)
        orbit_ids[orbit] = orbit_index
        representatives.append(word)
        sizes.append(len(orbit))
    if np.any(orbit_ids < 0):
        raise AssertionError("orbit partition incomplete")
    return (
        orbit_ids,
        np.array(representatives, dtype=np.int64),
        np.array(sizes, dtype=np.int64),
        permutations,
    )


def build_reduced_hamiltonian(
    edges: list[tuple[int, int, str]],
    orbit_ids: np.ndarray,
    representatives: np.ndarray,
    sizes: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    sources = []
    destinations = []
    coefficients = []
    for source, word_value in enumerate(representatives):
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
                -multiplicity * math.sqrt(sizes[source] / sizes[destination])
            )
    source_array = np.array(sources, dtype=np.int32)
    destination_array = np.array(destinations, dtype=np.int32)
    coefficient_array = np.array(coefficients, dtype=float)
    entries = {
        (int(source), int(destination)): float(coefficient)
        for source, destination, coefficient in zip(
            source_array, destination_array, coefficient_array
        )
    }
    hermiticity_error = max(
        abs(coefficient - entries.get((destination, source), math.inf))
        for (source, destination), coefficient in entries.items()
    )
    return source_array, destination_array, coefficient_array, hermiticity_error


def current_kernel(
    u: int,
    v: int,
    words: np.ndarray,
    orbit_ids: np.ndarray,
    sizes: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    bit_u = (words >> u) & 1
    bit_v = (words >> v) & 1
    active = words[bit_u != bit_v]
    swapped = active ^ (1 << u) ^ (1 << v)
    left = orbit_ids[active]
    right = orbit_ids[swapped]
    signs = ((active >> v) & 1) - ((active >> u) & 1)
    factors = signs / np.sqrt(sizes[left] * sizes[right])
    return left, right, factors


def reconstruct_currents(length: int, representatives: np.ndarray) -> np.ndarray:
    cycle_even, cycle_odd, connector_even = representatives
    currents = []
    for layer in range(2):
        for site in range(length):
            if layer == 0:
                currents.append(cycle_even if site % 2 == 0 else cycle_odd)
            else:
                currents.append(-cycle_odd if site % 2 == 0 else -cycle_even)
    for site in range(length):
        currents.append(connector_even if site % 2 == 0 else -connector_even)
    return np.array(currents)


def run_length(length: int) -> dict[str, object]:
    sites = 2 * length
    dimension = 1 << sites
    edges = component_edges(length)
    words = np.arange(dimension, dtype=np.int64)
    orbit_ids, orbit_representatives, orbit_sizes, permutations = build_orbits(length)

    edge_set = {frozenset((u, v)) for u, v, _ in edges}
    for permutation in permutations:
        moved = {
            frozenset((permutation[u], permutation[v])) for u, v, _ in edges
        }
        if moved != edge_set:
            raise AssertionError("group does not preserve the support")
    if any(permutation[site] % 2 != site % 2 for permutation in permutations for site in range(sites)):
        raise AssertionError("group does not preserve source parity")

    sources, destinations, coefficients, hermiticity_error = build_reduced_hamiltonian(
        edges, orbit_ids, orbit_representatives, orbit_sizes
    )
    reduced_dimension = len(orbit_representatives)
    state = np.zeros(reduced_dimension, dtype=np.complex128)
    even_mask = sum(1 << site for site in range(0, sites, 2))
    source_amplitude = 1.0 / math.sqrt(1 << length)
    valid = (orbit_representatives & even_mask) == 0
    state[valid] = np.sqrt(orbit_sizes[valid]) * source_amplitude
    state0 = state.copy()

    kernels = [
        current_kernel(0, 1, words, orbit_ids, orbit_sizes),
        current_kernel(1, 2, words, orbit_ids, orbit_sizes),
        current_kernel(0, length + 1, words, orbit_ids, orbit_sizes),
    ]

    def current_representatives(vector: np.ndarray) -> np.ndarray:
        return np.array([reduced_current(vector, *kernel) for kernel in kernels])

    def h_action(vector: np.ndarray) -> np.ndarray:
        return reduced_h_action(
            vector, sources, destinations, coefficients, reduced_dimension
        )

    step = KAPPA / STEPS
    integrals = current_representatives(state)
    for index in range(1, STEPS + 1):
        out = state.copy()
        term = state.copy()
        for order in range(1, TAYLOR_ORDER + 1):
            term = (-1.0j * step / order) * h_action(term)
            out += term
        state = out
        weight = 1.0 if index == STEPS else (4.0 if index % 2 else 2.0)
        integrals += weight * current_representatives(state)
    integrals *= step / 3.0
    currents = reconstruct_currents(length, integrals)

    probabilities_by_word = np.abs(state[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
    probabilities0_by_word = np.abs(state0[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
    q0 = np.array(
        [np.sum(probabilities0_by_word[((words >> site) & 1) == 1]) for site in range(sites)]
    )
    q1 = np.array(
        [np.sum(probabilities_by_word[((words >> site) & 1) == 1]) for site in range(sites)]
    )
    incidence = np.zeros((sites, len(edges)))
    for edge_index, (u, v, _) in enumerate(edges):
        incidence[u, edge_index] = 1.0
        incidence[v, edge_index] = -1.0
    residual = q1 - q0 + incidence @ currents

    correlations = []
    for u, v, _ in edges:
        both = ((words >> u) & 1) * ((words >> v) & 1)
        correlations.append(float(np.dot(probabilities_by_word, both) - q1[u] * q1[v]))
    particle_numbers = np.array([bin(word).count("1") for word in orbit_representatives])
    number_law0 = np.array(
        [np.sum(np.abs(state0[particle_numbers == count]) ** 2) for count in range(sites + 1)]
    )
    number_law = np.array(
        [np.sum(np.abs(state[particle_numbers == count]) ** 2) for count in range(sites + 1)]
    )
    energy0 = float(np.vdot(state0, h_action(state0)).real)
    energy = float(np.vdot(state, h_action(state)).real)

    target = json.loads(TARGETS[length].read_text())
    if length == 4:
        target = next(row for row in target["rows"] if row["kappa"] == KAPPA)
    target_q = np.array(target["q_after"])
    target_currents = np.array(target["integrated_oriented_currents"])
    return {
        "L": length,
        "full_dimension": dimension,
        "finite_group_order": len(permutations),
        "reduced_orbit_dimension": reduced_dimension,
        "orbit_size_histogram": {
            str(size): count for size, count in sorted(Counter(orbit_sizes.tolist()).items())
        },
        "reduced_hamiltonian_nonzero_entries": len(coefficients),
        "reduced_hamiltonian_hermiticity_error": hermiticity_error,
        "q_after": q1.tolist(),
        "integrated_oriented_currents": currents.tolist(),
        "q_target_linf": float(np.max(np.abs(q1 - target_q))),
        "current_target_linf": float(np.max(np.abs(currents - target_currents))),
        "record_ledger_residual_l1": float(np.sum(np.abs(residual))),
        "record_ledger_residual_linf": float(np.max(np.abs(residual))),
        "norm_error": float(abs(np.vdot(state, state).real - 1.0)),
        "energy_error": abs(energy - energy0),
        "number_law_max_change": float(np.max(np.abs(number_law - number_law0))),
        "max_abs_connected_edge_correlation": float(np.max(np.abs(correlations))),
    }


rows = [run_length(length) for length in (4, 6, 8)]
checks = []
for row in rows:
    checks.extend(
        [
            (row["finite_group_order"] == row["L"], f"L{row['L']} group order"),
            (row["reduced_orbit_dimension"] < row["full_dimension"], f"L{row['L']} reduction"),
            (row["reduced_hamiltonian_hermiticity_error"] < 1.0e-14, f"L{row['L']} Hermiticity"),
            (row["q_target_linf"] < 2.0e-11, f"L{row['L']} occupations"),
            (row["current_target_linf"] < 2.0e-11, f"L{row['L']} currents"),
            (row["record_ledger_residual_l1"] < 3.0e-10, f"L{row['L']} ledger"),
            (row["norm_error"] < 3.0e-10, f"L{row['L']} norm"),
            (row["energy_error"] < 3.0e-9, f"L{row['L']} energy"),
            (row["number_law_max_change"] < 3.0e-10, f"L{row['L']} number law"),
        ]
    )
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_CONNECTED_FINITE_ORBIT_REDUCTION_V001",
    "classification": "EXACT_FINITE_AUTOMORPHISM_ORBIT_BASIS__NUMERICAL_EVOLUTION_CROSSCHECK",
    "scope": "COMPUTATIONAL_COMPRESSION_OF_DECLARED_FINITE_SUPPORT__NO_NEW_PHYSICS",
    "parameters": {"kappa": KAPPA, "taylor_order": TAYLOR_ORDER, "steps": STEPS},
    "rows": rows,
    "group_action": "EVEN_CYCLE_TRANSLATIONS_AND_LAYER_SWAP_REFLECTION",
    "source_invariance": "UNIFORM_EVEN_TAIL_BLANK_ODD_HEAD_SUPERPOSITION_PATTERN",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "not_claimed": "AUTONOMOUS_SUPPORT_SELECTION__GRID__CONTINUUM__WARD__CRITICAL_PHASE__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5.0e-10:
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
print(f"PASS__R_CONNECTED_FINITE_ORBIT_REDUCTION__{len(checks)}/{len(checks)}")
