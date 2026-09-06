#!/usr/bin/env python3
"""Direct full-space localized W_R=1/2 response for connected L6 or L8."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import time
from collections import Counter, deque
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--length", type=int, choices=(6, 8), required=True)
ARGS = PARSER.parse_args()
LENGTH = ARGS.length
SITES = 2 * LENGTH
DIMENSION = 1 << SITES
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
COARSE_STEPS = 1024
FINE_STEPS = 2048
SOURCE_SITE = 0
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = HERE / f"RESULT_L{LENGTH}.json"
TARGETS = {
    6: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json",
    8: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json",
}
TARGET_HASHES = {
    6: "e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
    8: "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
}
STARTED = time.perf_counter()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_for(length: int):
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append((layer * length + site, layer * length + (site + 1) % length, "internal"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


edges = edges_for(LENGTH)
words = np.arange(DIMENSION, dtype=np.int64)
edge_actions = []
for u, v, kind in edges:
    bit_u = (words >> u) & 1
    bit_v = (words >> v) & 1
    active = words[bit_u != bit_v]
    swapped = active ^ (1 << u) ^ (1 << v)
    coefficients = 1j * (((active >> v) & 1) - ((active >> u) & 1))
    edge_actions.append((active, swapped, coefficients, kind))


def h_action(states: np.ndarray) -> np.ndarray:
    out = np.zeros_like(states)
    for active, swapped, _, _ in edge_actions:
        out[active, :] -= states[swapped, :]
    return out


def current_expectations(states: np.ndarray) -> np.ndarray:
    out = np.empty((states.shape[1], len(edges)), dtype=float)
    for edge_index, (active, swapped, coefficients, _) in enumerate(edge_actions):
        for history in range(states.shape[1]):
            out[history, edge_index] = float(
                np.vdot(
                    states[active, history],
                    coefficients * states[swapped, history],
                ).real
            )
    return out


def evolve(initial: np.ndarray, step_count: int):
    step = KAPPA / step_count
    states = initial.copy()
    integrated = current_expectations(states)
    for index in range(1, step_count + 1):
        updated = states.copy()
        term = states.copy()
        for order in range(1, TAYLOR_ORDER + 1):
            term = (-1j * step / order) * h_action(term)
            updated += term
        states = updated
        weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
        integrated += weight * current_expectations(states)
    return states, integrated * step / 3.0


even_mask = sum(1 << site for site in range(0, SITES, 2))
other_even_mask = even_mask ^ (1 << SOURCE_SITE)
baseline = np.zeros(DIMENSION, dtype=np.complex128)
baseline[(words & even_mask) == 0] = 1.0 / math.sqrt(1 << LENGTH)
perturbed = np.zeros(DIMENSION, dtype=np.complex128)
allowed = (words & other_even_mask) == 0
perturbed[allowed] = np.where(
    ((words[allowed] >> SOURCE_SITE) & 1) == 0,
    1.0,
    -1.0j,
) / math.sqrt(1 << (LENGTH + 1))
initial = np.column_stack((baseline, perturbed))

states_coarse, currents_coarse = evolve(initial, COARSE_STEPS)
states, currents = evolve(initial, FINE_STEPS)


def occupations(states_in: np.ndarray) -> np.ndarray:
    probabilities = np.abs(states_in) ** 2
    return np.array([
        np.dot(((words >> site) & 1).astype(float), probabilities)
        for site in range(SITES)
    ]).T


q_before = occupations(initial)
q_after_coarse = occupations(states_coarse)
q_after = occupations(states)
incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0
history_residual = q_after - q_before + currents @ incidence.T
history_residual_coarse = q_after_coarse - q_before + currents_coarse @ incidence.T
delta_q = q_after[1] - q_after[0]
delta_q_coarse = q_after_coarse[1] - q_after_coarse[0]
delta_current = currents[1] - currents[0]
delta_current_coarse = currents_coarse[1] - currents_coarse[0]
source_vector = np.zeros(SITES)
source_vector[SOURCE_SITE] = 0.5
full_differential_residual = delta_q + incidence @ delta_current - source_vector
full_differential_residual_coarse = delta_q_coarse + incidence @ delta_current_coarse - source_vector

neighbors = [set() for _ in range(SITES)]
for u, v, _ in edges:
    neighbors[u].add(v)
    neighbors[v].add(u)
distances = [None] * SITES
distances[SOURCE_SITE] = 0
queue = deque([SOURCE_SITE])
while queue:
    u = queue.popleft()
    for v in neighbors[u]:
        if distances[v] is None:
            distances[v] = distances[u] + 1
            queue.append(v)

shells = []
for radius in sorted(set(min(distances[u], distances[v]) for u, v, _ in edges)):
    for kind in ("internal", "connector"):
        indices = [
            index for index, (u, v, edge_kind) in enumerate(edges)
            if edge_kind == kind and min(distances[u], distances[v]) == radius
        ]
        if not indices:
            continue
        values = delta_current[indices]
        shells.append({
            "r": radius,
            "kind": kind,
            "edge_count": len(indices),
            "edge_indices": indices,
            "signed_sum_delta_J": float(np.sum(values)),
            "l1_sum_abs_delta_J": float(np.sum(np.abs(values))),
            "mean_abs_delta_J": float(np.mean(np.abs(values))),
            "max_abs_delta_J": float(np.max(np.abs(values))),
        })

number = np.array([bin(int(word)).count("1") for word in words])
number_laws_before = np.array([
    [np.sum(np.abs(initial[number == count, history]) ** 2) for count in range(SITES + 1)]
    for history in range(2)
])
number_laws_after = np.array([
    [np.sum(np.abs(states[number == count, history]) ** 2) for count in range(SITES + 1)]
    for history in range(2)
])
h_initial = h_action(initial)
h_final = h_action(states)
energies_initial = np.sum(np.conjugate(initial) * h_initial, axis=0)
energies_final = np.sum(np.conjugate(states) * h_final, axis=0)
norms = np.sum(np.abs(states) ** 2, axis=0)

target_path = TARGETS[LENGTH]
target = json.loads(target_path.read_text())
target_q = np.array(target["q_after"])
target_current = np.array(target["integrated_oriented_currents"])
baseline_q_linf = float(np.max(np.abs(q_after[0] - target_q)))
baseline_current_linf = float(np.max(np.abs(currents[0] - target_current)))

kinds = np.array([kind for _, _, kind in edges])
connector = kinds == "connector"
total_change = float(np.sum(np.abs(currents[1])) - np.sum(np.abs(currents[0])))
connector_change = float(np.sum(np.abs(currents[1, connector])) - np.sum(np.abs(currents[0, connector])))
profile_l1 = float(np.sum(np.abs(delta_current)))
profile_weighted_radius = float(
    sum(min(distances[u], distances[v]) * abs(delta_current[index]) for index, (u, v, _) in enumerate(edges))
    / profile_l1
) if profile_l1 else 0.0
effective_edges = float(profile_l1**2 / np.sum(delta_current**2)) if np.any(delta_current) else 0.0

checks = [
    (digest(target_path) == TARGET_HASHES[LENGTH], "sealed baseline hash"),
    (len(edges) == 3 * LENGTH and sum(connector) == LENGTH, "edge census"),
    (all(len(item) == 3 for item in neighbors), "degree-three support"),
    (all(distance is not None for distance in distances), "connected support"),
    (abs(np.vdot(initial[:, 0], initial[:, 0]).real - 1.0) < 2e-13, "baseline initial norm"),
    (abs(np.vdot(initial[:, 1], initial[:, 1]).real - 1.0) < 2e-13, "perturbed initial norm"),
    (abs(q_before[1, SOURCE_SITE] - q_before[0, SOURCE_SITE] - 0.5) < 2e-13, "authenticated source amount"),
    (abs(np.sum(q_before[1] - q_before[0]) - 0.5) < 2e-13, "initial global source amount"),
    (baseline_q_linf < 2e-11, "sealed baseline occupation reproduction"),
    (baseline_current_linf < 2e-11, "sealed baseline current reproduction"),
    (float(np.max(np.abs(states - states_coarse))) < 2e-10, "state refinement"),
    (float(np.max(np.abs(q_after - q_after_coarse))) < 2e-10, "occupation refinement"),
    (float(np.max(np.abs(currents - currents_coarse))) < 2e-10, "current refinement"),
    (float(np.sum(np.abs(history_residual[0]))) < 5e-10, "baseline transport ledger"),
    (float(np.sum(np.abs(history_residual[1]))) < 5e-10, "perturbed transport ledger"),
    (float(np.sum(np.abs(full_differential_residual))) < 1e-9, "full differential ledger"),
    (abs(float(np.sum(delta_q)) - 0.5) < 5e-10, "terminal global source retention"),
    (float(np.max(np.abs(norms - 1.0))) < 2e-10, "terminal norms"),
    (float(np.max(np.abs(energies_final.real - energies_initial.real))) < 2e-9, "energy conservation"),
    (float(np.max(np.abs(energies_final.imag))) < 2e-10, "energy reality"),
    (float(np.max(np.abs(number_laws_after - number_laws_before))) < 2e-10, "number-law conservation"),
    (len({index for shell in shells for index in shell["edge_indices"]}) == len(edges), "radial shell partition"),
    (profile_l1 > 1e-8, "nonzero current response"),
    (np.all(np.isfinite(delta_current)) and np.all(np.isfinite(delta_q)), "finite response record"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": f"R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L{LENGTH}_DIRECT_V001",
    "classification": "FINITE_AUTHENTICATED_W_R_HALF_LOCAL_WRITE__DIRECT_FULL_SPACE_PERTURBED_MINUS_BASELINE_RESPONSE",
    "scope": "FINITE_SUPPORT_GRAPH_PROFILE__NO_PHYSICAL_DISTANCE_OR_CONTINUUM_INFERENCE",
    "sealed_baseline_sha256": digest(target_path),
    "parameters": {
        "L": LENGTH,
        "sites_per_component": SITES,
        "hilbert_dimension": DIMENSION,
        "source_site": SOURCE_SITE,
        "W_R": 0.5,
        "r0": "14441248/6075",
        "phi": "pi/4",
        "kappa": KAPPA,
        "taylor_order": TAYLOR_ORDER,
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
    },
    "source_write_ledger": "DELTA_Q_PLUS_EDGE_FLUX_MINUS_W_R_EQUALS_ONE_HALF_PLUS_ZERO_MINUS_ONE_HALF_EQUALS_ZERO",
    "edge_records": [
        {
            "edge_index": index,
            "u": u,
            "v": v,
            "kind": kind,
            "r": min(distances[u], distances[v]),
            "baseline_J": float(currents[0, index]),
            "perturbed_J": float(currents[1, index]),
            "delta_J": float(delta_current[index]),
        }
        for index, (u, v, kind) in enumerate(edges)
    ],
    "site_records": [
        {
            "site": site,
            "r": distances[site],
            "baseline_q_before": float(q_before[0, site]),
            "perturbed_q_before": float(q_before[1, site]),
            "baseline_q_after": float(q_after[0, site]),
            "perturbed_q_after": float(q_after[1, site]),
            "delta_q_after": float(delta_q[site]),
        }
        for site in range(SITES)
    ],
    "radial_edge_profile": shells,
    "response_summary": {
        "delta_q_terminal_sum": float(np.sum(delta_q)),
        "delta_J_l1": profile_l1,
        "delta_J_linf": float(np.max(np.abs(delta_current))),
        "total_absolute_throughput_change": total_change,
        "connector_absolute_throughput_change": connector_change,
        "mean_edge_radius_abs_delta_J": profile_weighted_radius,
        "effective_responding_edge_count": effective_edges,
        "max_site_graph_distance": max(distances),
        "profile_classification": "RAW_LOWER_SIZE_PROFILE__FULL_L6_TO_L14_LADDER_CLASSIFICATION_OPEN",
    },
    "numerical_controls": {
        "baseline_q_reproduction_linf": baseline_q_linf,
        "baseline_current_reproduction_linf": baseline_current_linf,
        "state_refinement_linf": float(np.max(np.abs(states - states_coarse))),
        "occupation_refinement_linf": float(np.max(np.abs(q_after - q_after_coarse))),
        "current_refinement_linf": float(np.max(np.abs(currents - currents_coarse))),
        "differential_occupation_refinement_linf": float(np.max(np.abs(delta_q - delta_q_coarse))),
        "differential_current_refinement_linf": float(np.max(np.abs(delta_current - delta_current_coarse))),
        "baseline_transport_residual_l1": float(np.sum(np.abs(history_residual[0]))),
        "perturbed_transport_residual_l1": float(np.sum(np.abs(history_residual[1]))),
        "full_differential_residual_l1": float(np.sum(np.abs(full_differential_residual))),
        "full_differential_residual_linf": float(np.max(np.abs(full_differential_residual))),
        "coarse_full_differential_residual_l1": float(np.sum(np.abs(full_differential_residual_coarse))),
        "norm_error_max": float(np.max(np.abs(norms - 1.0))),
        "energy_error_max": float(np.max(np.abs(energies_final.real - energies_initial.real))),
        "energy_imag_abs_max": float(np.max(np.abs(energies_final.imag))),
        "number_law_max_change": float(np.max(np.abs(number_laws_after - number_laws_before))),
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_DIFFERENTIAL_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "profile_status": "FINITE_SUPPORT_GRAPH_DISTANCE_ONLY__NOT_PHYSICAL_RADIUS_OR_GRID",
    "not_claimed": "FULL_L6_TO_L14_PROFILE_CLASSIFICATION__SCALING_LAW__LOCALITY_LAW__PHYSICAL_BOUNDARY_REFLECTION__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5e-11:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    print("RESULT_JSON_BEGIN")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("RESULT_JSON_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L{LENGTH}__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
