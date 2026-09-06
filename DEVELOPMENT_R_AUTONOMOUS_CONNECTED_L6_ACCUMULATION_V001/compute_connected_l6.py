#!/usr/bin/env python3
"""Matrix-free L6 connected-cycle autonomous BS09 accumulation."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


LENGTH = 6
SITES = 2 * LENGTH
DIMENSION = 1 << SITES
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
COARSE_STEPS = 1024
FINE_STEPS = 2048
COMPONENTS = 18
ROOT = Path(__file__).resolve().parent.parent
L4_RESULT = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json"
OUT = Path(__file__).with_name("RESULT.json")


edges: list[tuple[int, int, str]] = []
for cycle in range(2):
    offset = cycle * LENGTH
    for site in range(LENGTH):
        edges.append((offset + site, offset + (site + 1) % LENGTH, f"cycle_{cycle}"))
for site in range(LENGTH):
    edges.append((site, LENGTH + (site + 1) % LENGTH, "connector"))

words = np.arange(DIMENSION, dtype=np.int64)
edge_actions = []
for u, v, kind in edges:
    bit_u = (words >> u) & 1
    bit_v = (words >> v) & 1
    active = words[bit_u != bit_v]
    swapped = active ^ (1 << u) ^ (1 << v)
    current_coefficients = 1j * (
        ((active >> v) & 1) - ((active >> u) & 1)
    )
    edge_actions.append((active, swapped, current_coefficients, kind))


def h_action(vector: np.ndarray) -> np.ndarray:
    out = np.zeros_like(vector)
    for active, swapped, _, _ in edge_actions:
        out[active] -= vector[swapped]
    return out


def current_expectations(vector: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.vdot(vector[active], coefficients * vector[swapped]).real)
            for active, swapped, coefficients, _ in edge_actions
        ]
    )


def taylor_step(vector: np.ndarray, step: float) -> np.ndarray:
    out = vector.copy()
    term = vector.copy()
    for order in range(1, TAYLOR_ORDER + 1):
        term = (-1j * step / order) * h_action(term)
        out += term
    return out


def evolve(step_count: int) -> tuple[np.ndarray, np.ndarray]:
    step = KAPPA / step_count
    state = psi0.copy()
    integral = current_expectations(state)
    # Composite Simpson weights: endpoints 1, odd nodes 4, even interior 2.
    for index in range(1, step_count + 1):
        state = taylor_step(state, step)
        weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
        integral += weight * current_expectations(state)
    integral *= step / 3.0
    return state, integral


psi0 = np.zeros(DIMENSION, dtype=complex)
amplitude = 1.0 / math.sqrt(1 << (SITES // 2))
for word in range(DIMENSION):
    if all(((word >> site) & 1) == 0 for site in range(0, SITES, 2)):
        psi0[word] = amplitude

psi_coarse, currents_coarse = evolve(COARSE_STEPS)
psi, currents = evolve(FINE_STEPS)
state_refinement_linf = float(np.max(np.abs(psi - psi_coarse)))
current_refinement_linf = float(np.max(np.abs(currents - currents_coarse)))

q_ops = [((words >> site) & 1).astype(float) for site in range(SITES)]
probabilities0 = np.abs(psi0) ** 2
probabilities = np.abs(psi) ** 2
q0 = np.array([np.dot(probabilities0, q) for q in q_ops])
q1 = np.array([np.dot(probabilities, q) for q in q_ops])
q1_coarse = np.array([np.dot(np.abs(psi_coarse) ** 2, q) for q in q_ops])
occupation_refinement_linf = float(np.max(np.abs(q1 - q1_coarse)))

incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0
residuals = q1 - q0 + incidence @ currents
residuals_coarse = q1_coarse - q0 + incidence @ currents_coarse

number = np.array([bin(word).count("1") for word in range(DIMENSION)], dtype=int)
number_law0 = np.array(
    [np.sum(probabilities0[number == count]) for count in range(SITES + 1)]
)
number_law = np.array(
    [np.sum(probabilities[number == count]) for count in range(SITES + 1)]
)
hpsi0 = h_action(psi0)
hpsi = h_action(psi)

connected = []
for u, v, _ in edges:
    connected.append(
        float(np.dot(probabilities, q_ops[u] * q_ops[v]) - q1[u] * q1[v])
    )

kinds = np.array([kind for _, _, kind in edges])
connector_mask = kinds == "connector"
internal_mask = ~connector_mask
throughput_component = float(np.sum(np.abs(currents)))
connector_throughput_component = float(np.sum(np.abs(currents[connector_mask])))
l4 = json.loads(L4_RESULT.read_text())
l4_active = next(row for row in l4["rows"] if row["kappa"] == KAPPA)
l6_over_l4_total = (
    COMPONENTS * throughput_component
    / l4_active["absolute_oriented_throughput_global"]
)
l6_over_l4_per_retained = (
    (COMPONENTS * throughput_component / 54.0)
    / (l4_active["absolute_oriented_throughput_global"] / 16.0)
)

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

checks = [
    (SITES == 12 and DIMENSION == 4096, "component census"),
    (len(edges) == 18 and np.sum(connector_mask) == 6, "owner-once edge census"),
    (all(len(neighbors[vertex]) == 3 for vertex in range(SITES)), "degree-three support"),
    (len(visited) == SITES, "component connected"),
    (COMPONENTS * SITES == 216, "global L6 site census"),
    (COMPONENTS * len(edges) == 324, "global owner-once edge census"),
    (int(np.sum(np.abs(currents[internal_mask]) > 1.0e-10)) == 12, "all internal currents active"),
    (int(np.sum(np.abs(currents[connector_mask]) > 1.0e-10)) == 6, "all connector currents active"),
    (connector_throughput_component > 1.0e-6, "nonzero connector throughput"),
    (abs(COMPONENTS * np.sum(q1) - 54.0) < 2.0e-9, "global retained total"),
    (state_refinement_linf < 2.0e-11, "state refinement"),
    (occupation_refinement_linf < 2.0e-11, "occupation refinement"),
    (current_refinement_linf < 1.0e-11, "current refinement"),
    (float(np.sum(np.abs(residuals))) < 2.0e-11, "fine ledger L1"),
    (float(np.max(np.abs(residuals))) < 4.0e-12, "fine ledger Linf"),
    (float(np.sum(np.abs(residuals))) <= float(np.sum(np.abs(residuals_coarse))) + 2.0e-12, "ledger refinement nonworsening"),
    (abs(np.vdot(psi, psi).real - 1.0) < 2.0e-11, "norm"),
    (abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real) < 2.0e-10, "energy"),
    (float(np.max(np.abs(number_law - number_law0))) < 2.0e-11, "number law"),
    (l6_over_l4_total > 0.0 and l6_over_l4_per_retained > 0.0, "L6/L4 comparator"),
]
failures = [label for ok, label in checks if not ok]

out = {
    "schema": "R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001",
    "classification": "CONDITIONAL_CONNECTED_SUPPORT__UNIFORM_F3_MDC_SOURCE__AUTONOMOUS_SIMULTANEOUS_BS09__REFINED_NUMERICAL_CURRENT_INTEGRATION",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "census": {
        "L": 6,
        "sites_global": 216,
        "sites_per_F3_layer": 108,
        "possible_F3_links": 11664,
        "components": COMPONENTS,
        "sites_per_component": SITES,
        "internal_edges_per_component": 12,
        "connector_edges_per_component": 6,
        "selected_edges_global_owner_once": COMPONENTS * len(edges),
        "prepared_source_lineages": 108,
        "expected_retained_global": 54,
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
    "L6_over_L4": {
        "throughput_total": l6_over_l4_total,
        "throughput_per_retained_record": l6_over_l4_per_retained,
    },
    "owner_once_action": "H_EQUALS_MINUS_T_SUM_OVER_324_UNIQUE_EDGES_T_E__18_IDENTICAL_CONNECTED_COMPONENTS",
    "ctp_bookkeeping": "ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE",
    "support_status": "CONDITIONAL_FIXED_CONNECTED_PROGRAM__NOT_AUTONOMOUSLY_SELECTED",
    "source_status": "UNIFORM_RIGHT_HEADS_AND_BLANK_LEFT_TAILS__NO_EXTRA_ROUTING_ASYMMETRY",
    "parameter_status": "KAPPA_EQUALS_PI_OVER_TWO_IS_CONDITIONAL__T_AND_TAU_NOT_SELECTED",
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "not_claimed": "EXACT_CURRENT_QUADRATURE__GENERIC_CONNECTED_PHASE__GRID__CONTINUUM__WARD__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 2.0e-11:
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
print(f"PASS__R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION__{len(checks)}/{len(checks)}")
