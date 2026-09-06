#!/usr/bin/env python3
"""Smallest connected two-cycle autonomous BS09 accumulation witness."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


LENGTH = 4
KAPPAS = (0.0, math.pi / 2.0)
COMPONENTS = 8
ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "RESULT.json"
OUT = Path(__file__).with_name("RESULT.json")


def q_diagonal(size: int, site: int) -> np.ndarray:
    return np.array([(word >> site) & 1 for word in range(1 << size)], dtype=float)


def edge_current(size: int, u: int, v: int) -> np.ndarray:
    current = np.zeros((1 << size, 1 << size), dtype=complex)
    for word in range(1 << size):
        if ((word >> u) & 1) == 1 and ((word >> v) & 1) == 0:
            swapped = word ^ (1 << u) ^ (1 << v)
            current[swapped, word] += 1j
            current[word, swapped] += -1j
    return current


sites = 2 * LENGTH
edges: list[tuple[int, int, str]] = []
for cycle in range(2):
    offset = cycle * LENGTH
    for site in range(LENGTH):
        edges.append((offset + site, offset + (site + 1) % LENGTH, f"cycle_{cycle}"))
for site in range(LENGTH):
    edges.append((site, LENGTH + (site + 1) % LENGTH, "connector"))

dimension = 1 << sites
h0 = np.zeros((dimension, dimension), dtype=float)
for u, v, _ in edges:
    for word in range(dimension):
        if ((word >> u) & 1) != ((word >> v) & 1):
            swapped = word ^ (1 << u) ^ (1 << v)
            h0[swapped, word] += -1.0

q_ops = [q_diagonal(sites, site) for site in range(sites)]
psi0 = np.zeros(dimension, dtype=complex)
amplitude = 1.0 / math.sqrt(1 << LENGTH)
for word in range(dimension):
    if all(((word >> site) & 1) == 0 for site in range(0, sites, 2)):
        psi0[word] = amplitude

eigenvalues, eigenvectors = np.linalg.eigh(h0)
coefficients = np.einsum("ia,i->a", eigenvectors.conj(), psi0, optimize=False)
differences = eigenvalues[:, None] - eigenvalues[None, :]
energy_currents = []
for u, v, _ in edges:
    current = edge_current(sites, u, v)
    acted = np.einsum("ij,jb->ib", current, eigenvectors, optimize=False)
    energy_currents.append(
        np.einsum("ia,ib->ab", eigenvectors.conj(), acted, optimize=False)
    )

probabilities0 = np.abs(psi0) ** 2
q0 = np.array([np.dot(probabilities0, q) for q in q_ops])
number = np.array([bin(word).count("1") for word in range(dimension)], dtype=int)
number_law0 = np.array(
    [np.sum(probabilities0[number == count]) for count in range(sites + 1)]
)
hpsi0 = np.einsum("ij,j->i", h0, psi0, optimize=False)
initial_energy = float(np.vdot(psi0, hpsi0).real)
total_q = np.diag(number.astype(float))
onsite_commutator = np.einsum(
    "ij,jk->ik", h0, total_q, optimize=False
) - np.einsum("ij,jk->ik", total_q, h0, optimize=False)

incidence = np.zeros((sites, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0

rows = []
for kappa in KAPPAS:
    phase = np.exp(-1j * eigenvalues * kappa)
    psi = np.einsum("ia,a->i", eigenvectors, phase * coefficients, optimize=False)
    probabilities = np.abs(psi) ** 2
    q1 = np.array([np.dot(probabilities, q) for q in q_ops])
    factor = np.empty_like(differences, dtype=complex)
    near = np.abs(differences) < 1.0e-12
    factor[near] = kappa
    factor[~near] = (
        np.exp(1j * differences[~near] * kappa) - 1.0
    ) / (1j * differences[~near])
    currents = np.array(
        [
            float(
                np.sum(
                    coefficients.conj()[:, None]
                    * coefficients[None, :]
                    * energy_current
                    * factor
                ).real
            )
            for energy_current in energy_currents
        ]
    )
    residuals = q1 - q0 + incidence @ currents
    connected = []
    for u, v, _ in edges:
        connected.append(
            float(np.dot(probabilities, q_ops[u] * q_ops[v]) - q1[u] * q1[v])
        )
    number_law = np.array(
        [np.sum(probabilities[number == count]) for count in range(sites + 1)]
    )
    hpsi = np.einsum("ij,j->i", h0, psi, optimize=False)
    kinds = [kind for _, _, kind in edges]
    connector_mask = np.array([kind == "connector" for kind in kinds])
    internal_mask = ~connector_mask
    throughput_component = float(np.sum(np.abs(currents)))
    connector_throughput_component = float(np.sum(np.abs(currents[connector_mask])))
    rows.append(
        {
            "kappa": kappa,
            "q_before": q0.tolist(),
            "q_after": q1.tolist(),
            "integrated_oriented_currents": currents.tolist(),
            "active_internal_supports_per_component": int(np.sum(np.abs(currents[internal_mask]) > 1.0e-12)),
            "active_connector_supports_per_component": int(np.sum(np.abs(currents[connector_mask]) > 1.0e-12)),
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
            "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
            "energy_error": float(abs(np.vdot(psi, hpsi).real - initial_energy)),
            "number_law_max_change": float(np.max(np.abs(number_law - number_law0))),
            "uniform_onsite_commutator_linf": float(np.max(np.abs(onsite_commutator))),
        }
    )

zero, active = rows
baseline = json.loads(BASELINE.read_text())
baseline_l4 = next(row for row in baseline["rows"] if row["L"] == 4)
connected_over_disjoint = (
    active["absolute_oriented_throughput_global"]
    / baseline_l4["absolute_oriented_throughput_total"]
)

neighbors = [set() for _ in range(sites)]
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
    (sites == 8 and dimension == 256, "component census"),
    (len(edges) == 12 and sum(kind == "connector" for _, _, kind in edges) == 4, "owner-once edge census"),
    (COMPONENTS * sites == 64, "global L4 site census"),
    (COMPONENTS * len(edges) == 96, "global owner-once action census"),
    (all(len(neighbors[vertex]) == 3 for vertex in range(sites)), "degree-three support"),
    (len(visited) == sites, "component connected"),
    (zero["active_internal_supports_per_component"] == 0 and zero["active_connector_supports_per_component"] == 0, "zero-kappa control"),
    (active["active_internal_supports_per_component"] == 8, "all internal supports active"),
    (active["active_connector_supports_per_component"] == 4, "all connectors active"),
    (active["absolute_connector_throughput_global"] > 1.0e-6, "nonzero transported connector current"),
    (abs(active["expected_retained_global"] - 16.0) < 2.0e-12, "global retained total"),
    (max(row["record_ledger_residual_l1_per_component"] for row in rows) < 2.0e-11, "ledger L1"),
    (max(row["record_ledger_residual_linf_per_component"] for row in rows) < 3.0e-12, "ledger Linf"),
    (max(row["norm_error"] for row in rows) < 4.0e-14, "norm"),
    (max(row["energy_error"] for row in rows) < 4.0e-13, "energy"),
    (max(row["number_law_max_change"] for row in rows) < 4.0e-14, "number law"),
    (max(row["uniform_onsite_commutator_linf"] for row in rows) == 0.0, "uniform onsite commutator"),
    (connected_over_disjoint > 0.0, "connected/disjoint comparator"),
]
failures = [label for ok, label in checks if not ok]

out = {
    "schema": "R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001",
    "classification": "CONDITIONAL_CONNECTED_SUPPORT__UNIFORM_F3_MDC_SOURCE_PREPARATION__AUTONOMOUS_SIMULTANEOUS_BS09_EVOLUTION",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "census": {
        "L": 4,
        "sites_global": 64,
        "sites_per_F3_layer": 32,
        "possible_F3_links": 1024,
        "components": COMPONENTS,
        "sites_per_component": sites,
        "internal_edges_per_component": 8,
        "connector_edges_per_component": 4,
        "selected_edges_global_owner_once": COMPONENTS * len(edges),
        "prepared_source_lineages": 32,
        "expected_retained_global": 16,
    },
    "edge_order": [
        {"u": u, "v": v, "owner": kind} for u, v, kind in edges
    ],
    "rows": rows,
    "pi_over_2_connected_over_disjoint_throughput_total": connected_over_disjoint,
    "owner_once_action": "H_EQUALS_MINUS_T_SUM_OVER_96_UNIQUE_EDGES_T_E__8_IDENTICAL_CONNECTED_COMPONENTS",
    "ctp_bookkeeping": "Z_ETA_PLUS_ETA_MINUS_EQUALS_TRACE_U_PLUS_RHO_U_MINUS_DAGGER__Z_0_0_EQUALS_ONE",
    "support_status": "CONDITIONAL_FIXED_CONNECTED_PROGRAM__NOT_AUTONOMOUSLY_SELECTED",
    "source_status": "UNIFORM_RIGHT_HEADS_AND_BLANK_LEFT_TAILS__NO_EXTRA_ROUTING_ASYMMETRY",
    "parameter_status": "KAPPA_EQUALS_PI_OVER_TWO_IS_CONDITIONAL__T_AND_TAU_NOT_SELECTED",
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "not_claimed": "GENERIC_CONNECTED_PHASE__GRID__CONTINUUM__WARD__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 8.0e-12:
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
print(f"PASS__R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION__{len(checks)}/{len(checks)}")
