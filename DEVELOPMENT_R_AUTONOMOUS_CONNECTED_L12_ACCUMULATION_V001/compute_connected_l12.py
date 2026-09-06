#!/usr/bin/env python3
"""Order-2L finite-orbit L12 connected BS09 accumulation."""

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


LENGTH = 12
SITES = 24
FULL_DIMENSION = 1 << SITES
COMPONENTS = 72
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
COARSE_STEPS = 512
FINE_STEPS = 1024
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
START_TIME = time.perf_counter()
LOWER_RESULTS = {
    4: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json",
    6: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json",
    8: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json",
    10: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001" / "RESULT.json",
}


@njit
def h_apply(x, src, dst, val, n):
    out = np.zeros(n, np.complex128)
    for k in range(val.size):
        out[dst[k]] += val[k] * x[src[k]]
    return out


@njit
def j_expect(x, left, right, factor):
    out = 0.0j
    for k in range(factor.size):
        out += np.conjugate(x[left[k]]) * (1.0j * factor[k]) * x[right[k]]
    return out.real


edges = []
for layer in range(2):
    for site in range(LENGTH):
        edges.append((layer * LENGTH + site, layer * LENGTH + (site + 1) % LENGTH, "internal"))
for site in range(LENGTH):
    edges.append((site, LENGTH + (site + 1) % LENGTH, "connector"))


def prism_group():
    group = []
    for epsilon in (1, -1):
        for shift in range(LENGTH):
            swap = shift % 2
            permutation = []
            for layer in range(2):
                for site in range(LENGTH):
                    prism_site = (site - layer) % LENGTH
                    moved_layer = layer ^ swap
                    moved_prism = (epsilon * prism_site + shift) % LENGTH
                    moved_site = (moved_prism + moved_layer) % LENGTH
                    permutation.append(moved_layer * LENGTH + moved_site)
            group.append(tuple(permutation))
    if len(set(group)) != 2 * LENGTH:
        raise AssertionError("order-2L group is not faithful")
    return group


def permute_word(word, permutation):
    out = 0
    for source, destination in enumerate(permutation):
        if (word >> source) & 1:
            out |= 1 << destination
    return out


group = prism_group()
edge_set = {frozenset((u, v)) for u, v, _ in edges}
for permutation in group:
    if {frozenset((permutation[u], permutation[v])) for u, v, _ in edges} != edge_set:
        raise AssertionError("group does not preserve support")
    if any(permutation[site] % 2 != site % 2 for site in range(SITES)):
        raise AssertionError("group does not preserve source parity")

orbit_ids = np.full(FULL_DIMENSION, -1, np.int32)
orbit_representatives, orbit_sizes = [], []
for word in range(FULL_DIMENSION):
    if orbit_ids[word] >= 0:
        continue
    orbit = sorted({permute_word(word, permutation) for permutation in group})
    orbit_id = len(orbit_representatives)
    orbit_ids[orbit] = orbit_id
    orbit_representatives.append(word)
    orbit_sizes.append(len(orbit))
orbit_representatives = np.array(orbit_representatives, np.int64)
orbit_sizes = np.array(orbit_sizes, np.int64)
ORBIT_DIMENSION = len(orbit_representatives)

sources, destinations, coefficients = [], [], []
for source, raw_word in enumerate(orbit_representatives):
    word = int(raw_word)
    counts = Counter()
    for u, v, _ in edges:
        if ((word >> u) & 1) != ((word >> v) & 1):
            counts[int(orbit_ids[word ^ (1 << u) ^ (1 << v)])] += 1
    for destination, multiplicity in sorted(counts.items()):
        sources.append(source)
        destinations.append(destination)
        coefficients.append(-multiplicity * math.sqrt(orbit_sizes[source] / orbit_sizes[destination]))
sources = np.array(sources, np.int32)
destinations = np.array(destinations, np.int32)
coefficients = np.array(coefficients, float)

# Check every reverse quotient entry without allocating a dense matrix.
keys = sources.astype(np.int64) * ORBIT_DIMENSION + destinations
order = np.argsort(keys)
sorted_keys = keys[order]
reverse_keys = destinations.astype(np.int64) * ORBIT_DIMENSION + sources
reverse_positions = np.searchsorted(sorted_keys, reverse_keys)
if np.any(reverse_positions == len(sorted_keys)) or np.any(sorted_keys[reverse_positions] != reverse_keys):
    raise AssertionError("quotient reverse entry missing")
hermiticity_error = float(np.max(np.abs(coefficients - coefficients[order][reverse_positions])))
del keys, order, sorted_keys, reverse_keys, reverse_positions


def signed_edge_orbits():
    lookup = {frozenset((u, v)): (index, u, v) for index, (u, v, _) in enumerate(edges)}
    reconstruction = [None] * len(edges)
    representatives = []
    for edge_index, (u, v, _) in enumerate(edges):
        if reconstruction[edge_index] is not None:
            continue
        representative = len(representatives)
        representatives.append(edge_index)
        observed = {}
        for permutation in group:
            moved_u, moved_v = permutation[u], permutation[v]
            target, stored_u, stored_v = lookup[frozenset((moved_u, moved_v))]
            sign = 1 if (moved_u, moved_v) == (stored_u, stored_v) else -1
            if target in observed and observed[target] != sign:
                raise AssertionError("signed edge orbit contradiction")
            observed[target] = sign
        for target, sign in observed.items():
            reconstruction[target] = (representative, sign)
    if any(value is None for value in reconstruction):
        raise AssertionError("edge reconstruction incomplete")
    return representatives, reconstruction


edge_representatives, edge_reconstruction = signed_edge_orbits()
words = np.arange(FULL_DIMENSION, dtype=np.int64)


def current_kernel(edge_index):
    u, v, _ = edges[edge_index]
    active = words[(((words >> u) & 1) != ((words >> v) & 1))]
    swapped = active ^ (1 << u) ^ (1 << v)
    left, right = orbit_ids[active], orbit_ids[swapped]
    sign = ((active >> v) & 1) - ((active >> u) & 1)
    return left, right, sign / np.sqrt(orbit_sizes[left] * orbit_sizes[right])


kernels = [current_kernel(edge_index) for edge_index in edge_representatives]


def H(x):
    return h_apply(x, sources, destinations, coefficients, ORBIT_DIMENSION)


def currents(x):
    representative_values = [j_expect(x, *kernel) for kernel in kernels]
    return np.array([sign * representative_values[rep] for rep, sign in edge_reconstruction])


psi0 = np.zeros(ORBIT_DIMENSION, np.complex128)
even_mask = sum(1 << site for site in range(0, SITES, 2))
valid_source_orbits = (orbit_representatives & even_mask) == 0
psi0[valid_source_orbits] = np.sqrt(orbit_sizes[valid_source_orbits]) / math.sqrt(1 << LENGTH)


def step_taylor(x, step):
    out, term = x.copy(), x.copy()
    for order_index in range(1, TAYLOR_ORDER + 1):
        term = (-1.0j * step / order_index) * H(term)
        out += term
    return out


def evolve(step_count):
    step = KAPPA / step_count
    psi = psi0.copy()
    J = currents(psi)
    for index in range(1, step_count + 1):
        psi = step_taylor(psi, step)
        weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
        J += weight * currents(psi)
    return psi, J * step / 3.0


psi_coarse, currents_coarse = evolve(COARSE_STEPS)
psi, integrated_currents = evolve(FINE_STEPS)
state_refinement_linf = float(np.max(np.abs(psi - psi_coarse)))
current_refinement_linf = float(np.max(np.abs(integrated_currents - currents_coarse)))

probability = np.abs(psi[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
q1 = np.array([np.sum(probability[((words >> site) & 1) == 1]) for site in range(SITES)])
probability_coarse = np.abs(psi_coarse[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
q1_coarse = np.array([np.sum(probability_coarse[((words >> site) & 1) == 1]) for site in range(SITES)])
del probability_coarse
q0 = np.array([0.0 if site % 2 == 0 else 0.5 for site in range(SITES)])
occupation_refinement_linf = float(np.max(np.abs(q1 - q1_coarse)))

incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0
residual = q1 - q0 + incidence @ integrated_currents
residual_coarse = q1_coarse - q0 + incidence @ currents_coarse

particle_number = np.array([bin(int(word)).count("1") for word in orbit_representatives])
law0 = np.array([np.sum(np.abs(psi0[particle_number == value]) ** 2) for value in range(SITES + 1)])
law = np.array([np.sum(np.abs(psi[particle_number == value]) ** 2) for value in range(SITES + 1)])
hpsi0, hpsi = H(psi0), H(psi)
correlations = []
for u, v, _ in edges:
    both = ((words >> u) & 1) * ((words >> v) & 1)
    correlations.append(float(np.dot(probability, both) - q1[u] * q1[v]))

kinds = np.array([kind for _, _, kind in edges])
connector_mask = kinds == "connector"
internal_mask = ~connector_mask
throughput_component = float(np.sum(np.abs(integrated_currents)))
connector_throughput_component = float(np.sum(np.abs(integrated_currents[connector_mask])))
this_global = COMPONENTS * throughput_component


def lower_row(length):
    packet = json.loads(LOWER_RESULTS[length].read_text())
    return next(row for row in packet["rows"] if row["kappa"] == KAPPA) if length == 4 else packet


comparators = {}
for length, retained in ((4, 16.0), (6, 54.0), (8, 128.0), (10, 250.0)):
    lower = lower_row(length)
    lower_global = lower["absolute_oriented_throughput_global"]
    comparators[f"L12_over_L{length}"] = {
        "throughput_total": this_global / lower_global,
        "throughput_per_retained_record": (this_global / 432.0) / (lower_global / retained),
    }

neighbors = [set() for _ in range(SITES)]
for u, v, _ in edges:
    neighbors[u].add(v)
    neighbors[v].add(u)
seen, todo = {0}, [0]
while todo:
    vertex = todo.pop()
    for neighbor in neighbors[vertex] - seen:
        seen.add(neighbor)
        todo.append(neighbor)

expected_histogram = {1: 4, 2: 6, 3: 12, 4: 30, 6: 142, 8: 15, 12: 10316, 24: 693845}
histogram = dict(sorted(Counter(orbit_sizes.tolist()).items()))
checks = [
    (FULL_DIMENSION == 16777216 and ORBIT_DIMENSION == 704370, "basis census"),
    (len(group) == 24 and histogram == expected_histogram, "group orbit census"),
    (len(coefficients) == 12582508 and hermiticity_error < 1.0e-14, "quotient structure"),
    (len(edge_representatives) == 2, "signed edge orbit census"),
    (len(edges) == 36 and np.sum(connector_mask) == 12, "component edge census"),
    (all(len(neighbors[site]) == 3 for site in range(SITES)) and len(seen) == SITES, "connected cubic support"),
    (COMPONENTS * SITES == 1728 and COMPONENTS * len(edges) == 2592, "global site/edge census"),
    (int(np.sum(np.abs(integrated_currents[internal_mask]) > 1.0e-10)) == 24, "all internal currents active"),
    (int(np.sum(np.abs(integrated_currents[connector_mask]) > 1.0e-10)) == 12, "all connector currents active"),
    (connector_throughput_component > 1.0e-6, "nonzero connector throughput"),
    (abs(COMPONENTS * np.sum(q1) - 432.0) < 8.0e-8, "global retained total"),
    (state_refinement_linf < 2.0e-8, "state refinement"),
    (occupation_refinement_linf < 2.0e-8, "occupation refinement"),
    (current_refinement_linf < 2.0e-8, "current refinement"),
    (float(np.sum(np.abs(residual))) < 8.0e-9, "fine ledger L1"),
    (float(np.max(np.abs(residual))) < 8.0e-10, "fine ledger Linf"),
    (float(np.sum(np.abs(residual))) <= float(np.sum(np.abs(residual_coarse))) + 3.0e-10, "ledger refinement nonworsening"),
    (abs(np.vdot(psi, psi).real - 1.0) < 8.0e-9, "norm"),
    (abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real) < 8.0e-8, "energy"),
    (float(np.max(np.abs(law - law0))) < 8.0e-9, "number law"),
    (all(item["throughput_total"] > 0 for item in comparators.values()), "total comparators"),
    (all(item["throughput_per_retained_record"] > 0 for item in comparators.values()), "per-retained comparators"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION_V001",
    "classification": "CONDITIONAL_CONNECTED_SUPPORT__UNIFORM_F3_MDC_SOURCE__AUTONOMOUS_SIMULTANEOUS_BS09__EXACT_ORDER_2L_FINITE_ORBIT_BASIS__REFINED_NUMERICAL_CURRENT_INTEGRATION",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "census": {
        "L": 12, "sites_global": 1728, "sites_per_F3_layer": 864,
        "possible_F3_links": 746496, "components": COMPONENTS,
        "sites_per_component": SITES, "internal_edges_per_component": 24,
        "connector_edges_per_component": 12,
        "selected_edges_global_owner_once": 2592,
        "prepared_source_lineages": 864, "expected_retained_global": 432,
    },
    "finite_orbit_basis": {
        "full_dimension": FULL_DIMENSION, "finite_group_order": len(group),
        "orbit_dimension": ORBIT_DIMENSION,
        "orbit_size_histogram": {str(key): value for key, value in histogram.items()},
        "quotient_nonzero_entries": len(coefficients),
        "quotient_array_bytes": int(sources.nbytes + destinations.nbytes + coefficients.nbytes),
        "quotient_hermiticity_error": hermiticity_error,
        "signed_edge_orbits": len(edge_representatives),
    },
    "parameters": {"kappa": KAPPA, "taylor_order": TAYLOR_ORDER, "coarse_steps": COARSE_STEPS, "fine_steps": FINE_STEPS},
    "q_before": q0.tolist(), "q_after": q1.tolist(),
    "integrated_oriented_currents": integrated_currents.tolist(),
    "active_internal_supports_per_component": int(np.sum(np.abs(integrated_currents[internal_mask]) > 1.0e-10)),
    "active_connector_supports_per_component": int(np.sum(np.abs(integrated_currents[connector_mask]) > 1.0e-10)),
    "absolute_oriented_throughput_per_component": throughput_component,
    "absolute_oriented_throughput_global": this_global,
    "absolute_connector_throughput_per_component": connector_throughput_component,
    "absolute_connector_throughput_global": COMPONENTS * connector_throughput_component,
    "expected_retained_per_component": float(np.sum(q1)),
    "expected_retained_global": float(COMPONENTS * np.sum(q1)),
    "max_abs_connected_edge_correlation": float(np.max(np.abs(correlations))),
    "record_ledger_residual_l1_per_component": float(np.sum(np.abs(residual))),
    "record_ledger_residual_linf_per_component": float(np.max(np.abs(residual))),
    "record_ledger_residual_l1_global_bound": float(COMPONENTS * np.sum(np.abs(residual))),
    "coarse_record_ledger_residual_l1_per_component": float(np.sum(np.abs(residual_coarse))),
    "state_refinement_linf": state_refinement_linf,
    "occupation_refinement_linf": occupation_refinement_linf,
    "current_refinement_linf": current_refinement_linf,
    "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
    "energy_error": float(abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real)),
    "number_law_max_change": float(np.max(np.abs(law - law0))),
    "comparators": comparators,
    "owner_once_action": "H_EQUALS_MINUS_T_SUM_OVER_2592_UNIQUE_EDGES_T_E__72_IDENTICAL_CONNECTED_COMPONENTS",
    "ctp_bookkeeping": "ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE",
    "support_status": "CONDITIONAL_FIXED_CONNECTED_PROGRAM__NOT_AUTONOMOUSLY_SELECTED",
    "source_status": "UNIFORM_RIGHT_HEADS_AND_BLANK_LEFT_TAILS__NO_EXTRA_ROUTING_ASYMMETRY",
    "parameter_status": "KAPPA_EQUALS_PI_OVER_TWO_IS_CONDITIONAL__T_AND_TAU_NOT_SELECTED",
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "checks_passed": len(checks) - len(failures), "checks_total": len(checks), "failures": failures,
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "not_claimed": "EXACT_TIME_EVOLUTION__EXACT_CURRENT_QUADRATURE__MONOTONICITY__LIMIT__SCALING_LAW__GENERIC_CONNECTED_PHASE__GRID__CONTINUUM__WARD__GRAVITY",
}


def compatible(observed, canonical, path="root"):
    if isinstance(canonical, dict):
        if not isinstance(observed, dict) or set(observed) != set(canonical):
            raise AssertionError(f"canonical keys differ at {path}")
        for key in canonical:
            compatible(observed[key], canonical[key], f"{path}.{key}")
    elif isinstance(canonical, list):
        if not isinstance(observed, list) or len(observed) != len(canonical):
            raise AssertionError(f"canonical list differs at {path}")
        for index, (left, right) in enumerate(zip(observed, canonical)):
            compatible(left, right, f"{path}[{index}]")
    elif isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 3.0e-9:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION__{len(checks)}/{len(checks)}")
if os.environ.get("REPORT_RESOURCES") == "1":
    print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - START_TIME:.9f}")
    print(f"OBSERVED_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
