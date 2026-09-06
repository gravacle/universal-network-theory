#!/usr/bin/env python3
"""Owner-once gate-order screen for the 16-record connected circuit."""

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
DEPTH = 3
DELTA = 1.0
THETA = math.pi / 8.0
CLUSTERS_IN_L8 = 16
RING0 = [(i, (i + 1) % 8) for i in range(8)]
RING1 = [(8 + i, 8 + ((i + 1) % 8)) for i in range(8)]
RUNGS = [(i, i + 8) for i in range(8)]
FORWARD = RING0 + RING1 + RUNGS
ORDERS = {
    "forward": FORWARD,
    "reverse": list(reversed(FORWARD)),
    "interleaved": [edge for i in range(8) for edge in (RING0[i], RING1[i], RUNGS[i])],
}
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


def run_order(name, edges):
    state = np.ones(DIM, dtype=complex) / math.sqrt(DIM)
    q_initial = occupations(state)
    cumulative = {edge: 0.0 for edge in FORWARD}
    event_traffic = 0.0
    for _ in range(DEPTH):
        onsite_half_step(state)
        for i, j in edges:
            transported = transfer_gate(state, i, j)
            cumulative[(i, j)] += transported
            event_traffic += abs(transported)
        onsite_half_step(state)

    probs = abs(state) ** 2
    q_final = occupations(state)
    divergence = np.zeros(N)
    for (i, j), transported in cumulative.items():
        divergence[i] += transported
        divergence[j] -= transported
    residual = q_final - q_initial + divergence
    connected = [
        float(np.dot(probs, Q_BITS[i] * Q_BITS[j]) - q_final[i] * q_final[j])
        for i, j in FORWARD
    ]
    number_law = np.array(
        [np.sum(probs[NUMBER == k]) for k in range(N + 1)]
    )
    currents = np.array([cumulative[edge] for edge in FORWARD])
    rung_currents = np.array([cumulative[edge] for edge in RUNGS])
    return {
        "name": name,
        "state": state,
        "probabilities": probs,
        "record": {
            "order": name,
            "edge_sequence": [[i, j] for i, j in edges],
            "expected_retained_per_cluster": float(np.sum(q_final)),
            "L8_expected_retained": float(CLUSTERS_IN_L8 * np.sum(q_final)),
            "q_final": q_final.tolist(),
            "first_ring_expected_retained": float(np.sum(q_final[:8])),
            "second_ring_expected_retained": float(np.sum(q_final[8:])),
            "gate_event_absolute_traffic": float(event_traffic),
            "cumulative_net_edge_throughput": float(np.sum(np.abs(currents))),
            "cumulative_net_inter_ring_throughput": float(
                np.sum(np.abs(rung_currents))
            ),
            "active_cumulative_edge_count": int(
                np.sum(np.abs(currents) > 1e-12)
            ),
            "active_cumulative_inter_ring_edge_count": int(
                np.sum(np.abs(rung_currents) > 1e-12)
            ),
            "max_abs_connected_edge_correlation": float(
                np.max(np.abs(connected))
            ),
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
        },
    }


runs = [run_order(name, edges) for name, edges in ORDERS.items()]
pairwise = []
for a_index in range(len(runs)):
    for b_index in range(a_index + 1, len(runs)):
        a = runs[a_index]
        b = runs[b_index]
        overlap = np.vdot(a["state"], b["state"])
        pairwise.append(
            {
                "first": a["name"],
                "second": b["name"],
                "terminal_distribution_total_variation": float(
                    0.5 * np.sum(abs(a["probabilities"] - b["probabilities"]))
                ),
                "state_fidelity": float(abs(overlap) ** 2),
                "occupation_l1_distance": float(
                    np.sum(
                        abs(
                            np.array(a["record"]["q_final"])
                            - np.array(b["record"]["q_final"])
                        )
                    )
                ),
            }
        )

records = [run["record"] for run in runs]
out = {
    "schema": "R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN_NUMERICAL_V001",
    "sites_per_cluster": N,
    "hilbert_dimension": DIM,
    "clusters_in_L8_tiling": CLUSTERS_IN_L8,
    "topology": "NATIVE_Y_RINGS_PAIRED_BY_Z_GENERATOR",
    "parameters": {
        "depth": DEPTH,
        "staggered_delta": DELTA,
        "second_ring_stagger_reversed": True,
        "transfer_angle": THETA,
        "owned_edges_per_depth": len(FORWARD),
    },
    "orders": records,
    "pairwise_order_comparisons": pairwise,
    "envelope": {
        "max_terminal_distribution_total_variation": max(
            p["terminal_distribution_total_variation"] for p in pairwise
        ),
        "min_state_fidelity": min(p["state_fidelity"] for p in pairwise),
        "max_occupation_l1_distance": max(
            p["occupation_l1_distance"] for p in pairwise
        ),
        "max_record_ledger_residual_l1_per_cluster": max(
            r["record_ledger_residual_l1_per_cluster"] for r in records
        ),
        "max_record_ledger_residual_linf_per_cluster": max(
            r["record_ledger_residual_linf_per_cluster"] for r in records
        ),
        "max_abs_L8_retained_change": max(
            abs(r["L8_expected_retained"] - 128.0) for r in records
        ),
        "max_norm_error": max(r["norm_error"] for r in records),
        "max_number_law_change": max(
            r["number_law_max_change"] for r in records
        ),
    },
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "coordinate_status": "INHERITED_FINITE_FAMILY_ENUMERATION__NOT_PHYSICAL_GRID",
    "classification": (
        "CONTROLLED_NUMERICAL_ORDER_SCREEN__SCHEDULE_IS_SELECTED_PARENT_DATA__"
        "RESIDUALS_UNASSIGNED_UNTIL_OWNER_CLASSIFICATION"
    ),
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
}

rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
Path(__file__).with_name("RESULT.json").write_text(rendered)
print(rendered, end="")

assert set(ORDERS) == {"forward", "reverse", "interleaved"}
assert all(len(edges) == len(set(edges)) == 24 for edges in ORDERS.values())
assert all(set(edges) == set(FORWARD) for edges in ORDERS.values())
assert all(r["active_cumulative_edge_count"] == 24 for r in records)
assert all(r["active_cumulative_inter_ring_edge_count"] == 8 for r in records)
assert out["envelope"]["max_terminal_distribution_total_variation"] > 1e-3
assert out["envelope"]["max_occupation_l1_distance"] > 1e-3
assert out["envelope"]["min_state_fidelity"] < 0.999
assert out["envelope"]["max_record_ledger_residual_l1_per_cluster"] < 5e-14
assert out["envelope"]["max_record_ledger_residual_linf_per_cluster"] < 7e-15
assert out["envelope"]["max_abs_L8_retained_change"] < 5e-13
assert out["envelope"]["max_norm_error"] < 2e-14
assert out["envelope"]["max_number_law_change"] < 3e-15
assert out["classification"].endswith("UNTIL_OWNER_CLASSIFICATION")
print("PASS__R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN__14/14")
