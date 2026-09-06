#!/usr/bin/env python3
"""Depth trajectory for the audited 16-record native-support circuit."""

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
MAX_DEPTH = 8
DELTA = 1.0
THETA = math.pi / 8.0
CLUSTERS_IN_L8 = 16
RING_EDGES = [
    (row + i, row + ((i + 1) % 8))
    for row in (0, 8)
    for i in range(8)
]
RUNG_EDGES = [(i, i + 8) for i in range(8)]
EDGES = RING_EDGES + RUNG_EDGES
Q_BITS = np.array(
    [[(mask >> i) & 1 for mask in range(DIM)] for i in range(N)],
    dtype=float,
)
NUMBER = np.array([bin(mask).count("1") for mask in range(DIM)], dtype=int)
NUMBER_LAW_INITIAL = np.array(
    [math.comb(N, k) / float(DIM) for k in range(N + 1)]
)


def occupations(state):
    return np.einsum("im,m->i", Q_BITS, abs(state) ** 2, optimize=False)


def onsite_half_step(state):
    phases = np.empty(DIM, dtype=complex)
    for mask in range(DIM):
        signed = sum(
            (1.0 if i % 2 == 0 else -1.0)
            * (1.0 if i < 8 else -1.0)
            * ((mask >> i) & 1)
            for i in range(N)
        )
        phases[mask] = np.exp(-0.5j * THETA * DELTA * signed)
    state *= phases


def transfer_gate(state, i, j):
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


def checkpoint(depth, state, q_initial, cumulative, event_abs_traffic):
    q_now = occupations(state)
    divergence = np.zeros(N)
    for (i, j), transported in cumulative.items():
        divergence[i] += transported
        divergence[j] -= transported
    residual = q_now - q_initial + divergence
    probs = abs(state) ** 2
    connected = [
        float(np.dot(probs, Q_BITS[i] * Q_BITS[j]) - q_now[i] * q_now[j])
        for i, j in EDGES
    ]
    number_law = np.array(
        [np.sum(probs[NUMBER == k]) for k in range(N + 1)]
    )
    ring_values = np.array([cumulative[edge] for edge in RING_EDGES])
    rung_values = np.array([cumulative[edge] for edge in RUNG_EDGES])
    all_values = np.concatenate((ring_values, rung_values))
    return {
        "depth": depth,
        "expected_retained_per_cluster": float(np.sum(q_now)),
        "L8_expected_retained": float(CLUSTERS_IN_L8 * np.sum(q_now)),
        "q_min": float(np.min(q_now)),
        "q_max": float(np.max(q_now)),
        "first_ring_expected_retained": float(np.sum(q_now[:8])),
        "second_ring_expected_retained": float(np.sum(q_now[8:])),
        "cumulative_net_edge_throughput": float(np.sum(np.abs(all_values))),
        "cumulative_net_ring_throughput": float(np.sum(np.abs(ring_values))),
        "cumulative_net_inter_ring_throughput": float(np.sum(np.abs(rung_values))),
        "gate_event_absolute_traffic": float(event_abs_traffic),
        "active_cumulative_edge_count": int(np.sum(np.abs(all_values) > 1e-12)),
        "active_cumulative_inter_ring_edge_count": int(
            np.sum(np.abs(rung_values) > 1e-12)
        ),
        "max_abs_connected_edge_correlation": float(np.max(np.abs(connected))),
        "record_ledger_residual_l1_per_cluster": float(
            np.sum(np.abs(residual))
        ),
        "record_ledger_residual_linf_per_cluster": float(
            np.max(np.abs(residual))
        ),
        "norm_error": float(abs(np.vdot(state, state).real - 1.0)),
        "number_law_max_change": float(
            np.max(np.abs(number_law - NUMBER_LAW_INITIAL))
        ),
    }


psi = np.ones(DIM, dtype=complex) / math.sqrt(DIM)
q_initial = occupations(psi)
cumulative = {edge: 0.0 for edge in EDGES}
event_abs_traffic = 0.0
trajectory = [checkpoint(0, psi, q_initial, cumulative, event_abs_traffic)]

for depth in range(1, MAX_DEPTH + 1):
    onsite_half_step(psi)
    for i, j in EDGES:
        transported = transfer_gate(psi, i, j)
        cumulative[(i, j)] += transported
        event_abs_traffic += abs(transported)
    onsite_half_step(psi)
    trajectory.append(
        checkpoint(depth, psi, q_initial, cumulative, event_abs_traffic)
    )

out = {
    "schema": "R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_NUMERICAL_V001",
    "depths": list(range(MAX_DEPTH + 1)),
    "sites_per_cluster": N,
    "hilbert_dimension": DIM,
    "clusters_in_L8_tiling": CLUSTERS_IN_L8,
    "topology": "NATIVE_Y_RINGS_PAIRED_BY_Z_GENERATOR",
    "parameters": {
        "staggered_delta": DELTA,
        "second_ring_stagger_reversed": True,
        "transfer_angle": THETA,
        "owned_edges_per_depth": len(EDGES),
        "maximum_depth": MAX_DEPTH,
    },
    "trajectory": trajectory,
    "envelope": {
        "max_gate_event_absolute_traffic": max(
            p["gate_event_absolute_traffic"] for p in trajectory
        ),
        "max_cumulative_net_edge_throughput": max(
            p["cumulative_net_edge_throughput"] for p in trajectory
        ),
        "max_cumulative_net_inter_ring_throughput": max(
            p["cumulative_net_inter_ring_throughput"] for p in trajectory
        ),
        "max_abs_connected_edge_correlation": max(
            p["max_abs_connected_edge_correlation"] for p in trajectory
        ),
        "max_record_ledger_residual_l1_per_cluster": max(
            p["record_ledger_residual_l1_per_cluster"] for p in trajectory
        ),
        "max_record_ledger_residual_linf_per_cluster": max(
            p["record_ledger_residual_linf_per_cluster"] for p in trajectory
        ),
        "max_abs_L8_retained_change": max(
            abs(p["L8_expected_retained"] - 128.0) for p in trajectory
        ),
        "max_norm_error": max(p["norm_error"] for p in trajectory),
        "max_number_law_change": max(
            p["number_law_max_change"] for p in trajectory
        ),
    },
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "current_definition": "GATE_OWNED_EXPECTED_OCCUPATION_TRANSFER",
    "coordinate_status": "INHERITED_FINITE_FAMILY_ENUMERATION__NOT_PHYSICAL_GRID",
    "classification": (
        "CONTROLLED_NUMERICAL_DEPTH_TRAJECTORY__RESIDUALS_UNASSIGNED_"
        "UNTIL_OWNER_CLASSIFICATION"
    ),
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
}

rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
Path(__file__).with_name("RESULT.json").write_text(rendered)
print(rendered, end="")

assert len(trajectory) == 9
assert trajectory[0]["gate_event_absolute_traffic"] == 0.0
assert all(p["active_cumulative_edge_count"] == 24 for p in trajectory[1:])
assert all(
    p["active_cumulative_inter_ring_edge_count"] == 8
    for p in trajectory[1:]
)
assert all(
    b["gate_event_absolute_traffic"] > a["gate_event_absolute_traffic"]
    for a, b in zip(trajectory[1:], trajectory[2:])
)
assert out["envelope"]["max_cumulative_net_inter_ring_throughput"] > 0.1
assert out["envelope"]["max_abs_connected_edge_correlation"] > 1e-3
assert out["envelope"]["max_record_ledger_residual_l1_per_cluster"] < 8e-14
assert out["envelope"]["max_record_ledger_residual_linf_per_cluster"] < 9e-15
assert out["envelope"]["max_abs_L8_retained_change"] < 1e-12
assert out["envelope"]["max_norm_error"] < 5e-14
assert out["envelope"]["max_number_law_change"] < 5e-14
assert out["classification"].endswith("UNTIL_OWNER_CLASSIFICATION")
print("PASS__R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY__12/12")
