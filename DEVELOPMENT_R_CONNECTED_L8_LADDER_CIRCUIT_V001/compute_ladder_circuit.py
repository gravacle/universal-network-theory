#!/usr/bin/env python3
"""Connected 16-record ladder circuit with gate-owned transfer ledger."""

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


N = 16
DIM = 1 << N
DELTA = 1.0
THETA = math.pi / 8.0
DEPTH = 3
CLUSTERS_IN_L8 = 16


Q_BITS = np.array(
    [[(mask >> i) & 1 for mask in range(DIM)] for i in range(N)],
    dtype=float,
)


def occupations(state):
    probs = abs(state) ** 2
    return np.einsum("im,m->i", Q_BITS, probs, optimize=False)


def onsite_half_step(state):
    phases = np.empty(DIM, dtype=complex)
    for mask in range(DIM):
        staggered = sum(
            (1.0 if i % 2 == 0 else -1.0)
            * (1.0 if i < 8 else -1.0)
            * ((mask >> i) & 1)
            for i in range(N)
        )
        phases[mask] = np.exp(-0.5j * THETA * DELTA * staggered)
    state *= phases


def transfer_gate(state, i, j):
    """Apply exp(+i theta T_ij); return occupation transported i -> j."""
    before = np.dot(Q_BITS[i], abs(state) ** 2)
    c = math.cos(THETA)
    s = 1j * math.sin(THETA)
    for mask in range(DIM):
        if ((mask >> i) & 1) == 1 and ((mask >> j) & 1) == 0:
            swapped = mask ^ (1 << i) ^ (1 << j)
            a = state[mask]
            b = state[swapped]
            state[mask] = c * a + s * b
            state[swapped] = s * a + c * b
    after = np.dot(Q_BITS[i], abs(state) ** 2)
    return float(before - after)


# Two 8-site rings plus eight rungs. The explicit order is part of the circuit
# parent; every edge has one owner in each depth step.
RING_EDGES = [(row + i, row + ((i + 1) % 8)) for row in (0, 8) for i in range(8)]
RUNG_EDGES = [(i, i + 8) for i in range(8)]
EDGES = RING_EDGES + RUNG_EDGES

psi = np.ones(DIM, dtype=complex) / math.sqrt(DIM)
q_initial = occupations(psi)
cumulative = {edge: 0.0 for edge in EDGES}
gate_records = []

for depth in range(DEPTH):
    onsite_half_step(psi)
    for edge_index, (i, j) in enumerate(EDGES):
        transported = transfer_gate(psi, i, j)
        cumulative[(i, j)] += transported
        gate_records.append(
            {
                "depth": depth,
                "edge_index": edge_index,
                "source": i,
                "target": j,
                "transported_source_to_target": transported,
            }
        )
    onsite_half_step(psi)

q_final = occupations(psi)
divergence = np.zeros(N)
for (i, j), transported in cumulative.items():
    divergence[i] += transported
    divergence[j] -= transported
residual = q_final - q_initial + divergence

probs = abs(psi) ** 2
number = np.array([bin(mask).count("1") for mask in range(DIM)], dtype=int)
number_law_initial = np.array(
    [math.comb(N, k) / float(DIM) for k in range(N + 1)]
)
number_law_final = np.array(
    [np.sum(probs[number == k]) for k in range(N + 1)]
)

connected = []
for i, j in EDGES:
    both = np.dot(probs, Q_BITS[i] * Q_BITS[j])
    connected.append(float(both - q_final[i] * q_final[j]))

transport_values = np.array(list(cumulative.values()))
out = {
    "schema": "R_CONNECTED_L8_LADDER_CIRCUIT_NUMERICAL_V001",
    "sites_per_cluster": N,
    "hilbert_dimension": DIM,
    "clusters_in_L8_tiling": CLUSTERS_IN_L8,
    "topology": "NATIVE_Y_RINGS_PAIRED_BY_Z_GENERATOR",
    "parameters": {
        "staggered_delta": DELTA,
        "second_ring_stagger_reversed": True,
        "transfer_angle": THETA,
        "depth": DEPTH,
        "owned_edges_per_depth": len(EDGES),
    },
    "q_initial": q_initial.tolist(),
    "q_final": q_final.tolist(),
    "total_retained_initial_per_cluster": float(np.sum(q_initial)),
    "total_retained_final_per_cluster": float(np.sum(q_final)),
    "L8_total_retained_initial": float(CLUSTERS_IN_L8 * np.sum(q_initial)),
    "L8_total_retained_final": float(CLUSTERS_IN_L8 * np.sum(q_final)),
    "cumulative_edge_currents": [
        {"source": i, "target": j, "transported": cumulative[(i, j)]}
        for i, j in EDGES
    ],
    "gate_records": gate_records,
    "absolute_owned_throughput_per_cluster": float(
        np.sum(np.abs(transport_values))
    ),
    "active_edge_count": int(np.sum(np.abs(transport_values) > 1e-12)),
    "max_abs_connected_edge_correlation": float(
        np.max(np.abs(connected))
    ),
    "record_ledger_residuals": residual.tolist(),
    "record_ledger_residual_l1_per_cluster": float(np.sum(np.abs(residual))),
    "record_ledger_residual_linf_per_cluster": float(np.max(np.abs(residual))),
    "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
    "number_law_max_change": float(
        np.max(np.abs(number_law_final - number_law_initial))
    ),
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "current_definition": "GATE_OWNED_EXPECTED_OCCUPATION_TRANSFER",
    "coordinate_status": "INHERITED_FINITE_FAMILY_ENUMERATION__NOT_PHYSICAL_GRID",
    "classification": (
        "CONTROLLED_NUMERICAL_CONNECTED_CIRCUIT__RESIDUALS_UNASSIGNED_"
        "UNTIL_OWNER_CLASSIFICATION"
    ),
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
}

rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
Path(__file__).with_name("RESULT.json").write_text(rendered)
print(rendered, end="")

assert len(EDGES) == 24
assert len(gate_records) == 72
assert out["active_edge_count"] == 24
assert min(abs(cumulative[edge]) for edge in RUNG_EDGES) > 1e-4
assert out["absolute_owned_throughput_per_cluster"] > 0.1
assert out["max_abs_connected_edge_correlation"] > 1e-4
assert abs(out["L8_total_retained_final"] - 128.0) < 2e-12
assert out["record_ledger_residual_l1_per_cluster"] < 2e-12
assert out["record_ledger_residual_linf_per_cluster"] < 3e-13
assert out["norm_error"] < 2e-13
assert out["number_law_max_change"] < 2e-13
assert out["terminal_instrument"].startswith("COMPLETE_FAILURE")
assert out["classification"].endswith("UNTIL_OWNER_CLASSIFICATION")
print("PASS__R_CONNECTED_L8_LADDER_CIRCUIT__12/12")
