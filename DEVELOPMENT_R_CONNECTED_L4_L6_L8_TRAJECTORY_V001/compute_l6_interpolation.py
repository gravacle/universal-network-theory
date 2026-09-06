#!/usr/bin/env python3
"""Insert an L=6 connected-component record between audited L4 and L8 rows."""

import hashlib
import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_RESULT = (
    ROOT
    / "DEVELOPMENT_R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_V001"
    / "RESULT.json"
)
DEPTH = 3
DELTA = 1.0
THETA = math.pi / 8.0
SIZE = 6


def run_l6():
    size = SIZE
    n = 2 * size
    dim = 1 << n
    ring_edges = [
        (row + i, row + ((i + 1) % size))
        for row in (0, size)
        for i in range(size)
    ]
    rung_edges = [(i, i + size) for i in range(size)]
    edges = ring_edges + rung_edges
    q_bits = np.array(
        [[(mask >> i) & 1 for mask in range(dim)] for i in range(n)],
        dtype=float,
    )
    number = np.array([bin(mask).count("1") for mask in range(dim)], dtype=int)
    number_law_initial = np.array(
        [math.comb(n, k) / float(dim) for k in range(n + 1)]
    )

    def occupations(state):
        return np.einsum("im,m->i", q_bits, abs(state) ** 2, optimize=False)

    def onsite_half_step(state):
        phases = np.empty(dim, dtype=complex)
        for mask in range(dim):
            signed = sum(
                (1.0 if i % 2 == 0 else -1.0)
                * (1.0 if i < size else -1.0)
                * ((mask >> i) & 1)
                for i in range(n)
            )
            phases[mask] = np.exp(-0.5j * THETA * DELTA * signed)
        state *= phases

    def transfer_gate(state, i, j):
        before = np.dot(q_bits[i], abs(state) ** 2)
        c = math.cos(THETA)
        s = 1j * math.sin(THETA)
        for mask in range(dim):
            if ((mask >> i) & 1) == 1 and ((mask >> j) & 1) == 0:
                swapped = mask ^ (1 << i) ^ (1 << j)
                a = state[mask]
                b = state[swapped]
                state[mask] = c * a + s * b
                state[swapped] = s * a + c * b
        after = np.dot(q_bits[i], abs(state) ** 2)
        return float(before - after)

    state = np.ones(dim, dtype=complex) / math.sqrt(dim)
    q_initial = occupations(state)
    cumulative = {edge: 0.0 for edge in edges}
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
    divergence = np.zeros(n)
    for (i, j), transported in cumulative.items():
        divergence[i] += transported
        divergence[j] -= transported
    residual = q_final - q_initial + divergence
    currents = np.array([cumulative[edge] for edge in edges])
    rung_currents = np.array([cumulative[edge] for edge in rung_edges])
    connected = [
        float(np.dot(probs, q_bits[i] * q_bits[j]) - q_final[i] * q_final[j])
        for i, j in edges
    ]
    number_law = np.array(
        [np.sum(probs[number == k]) for k in range(n + 1)]
    )
    clusters = size * size // 4
    retained_heads = size ** 3 // 2
    retained_component = float(np.sum(q_final))
    event_total = float(clusters * event_traffic)
    net_component = float(np.sum(np.abs(currents)))
    net_total = float(clusters * net_component)
    rung_component = float(np.sum(np.abs(rung_currents)))
    rung_total = float(clusters * rung_component)
    return {
        "L": size,
        "cells": size ** 3,
        "prepared_source_lineages": retained_heads,
        "retained_heads": retained_heads,
        "sites_per_connected_component": n,
        "hilbert_dimension_per_component": dim,
        "connected_components": clusters,
        "owned_supports_per_component_per_depth": len(edges),
        "owner_once_gate_events_per_component": DEPTH * len(edges),
        "active_cumulative_supports_per_component": int(
            np.sum(np.abs(currents) > 1e-12)
        ),
        "active_cumulative_inter_cycle_supports_per_component": int(
            np.sum(np.abs(rung_currents) > 1e-12)
        ),
        "expected_retained_per_component": retained_component,
        "expected_retained_total": float(clusters * retained_component),
        "gate_event_absolute_traffic_per_component": float(event_traffic),
        "gate_event_absolute_traffic_total": event_total,
        "gate_event_absolute_traffic_per_retained_head": float(
            event_total / retained_heads
        ),
        "cumulative_net_edge_throughput_per_component": net_component,
        "cumulative_net_edge_throughput_total": net_total,
        "cumulative_net_edge_throughput_per_retained_head": float(
            net_total / retained_heads
        ),
        "cumulative_net_inter_cycle_throughput_per_component": rung_component,
        "cumulative_net_inter_cycle_throughput_total": rung_total,
        "cumulative_net_inter_cycle_throughput_per_retained_head": float(
            rung_total / retained_heads
        ),
        "max_abs_connected_edge_correlation": float(np.max(np.abs(connected))),
        "record_ledger_residual_l1_per_component": float(
            np.sum(np.abs(residual))
        ),
        "record_ledger_residual_linf_per_component": float(
            np.max(np.abs(residual))
        ),
        "record_ledger_residual_l1_tiled_bound": float(
            clusters * np.sum(np.abs(residual))
        ),
        "norm_error": float(abs(np.vdot(state, state).real - 1.0)),
        "number_law_max_change": float(
            np.max(np.abs(number_law - number_law_initial))
        ),
    }


parent_bytes = PARENT_RESULT.read_bytes()
parent = json.loads(parent_bytes)
assert parent["schema"] == "R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_NUMERICAL_V001"
l4, l8 = parent["rows"]
l6 = run_l6()
rows = [l4, l6, l8]

total_fields = (
    "cells",
    "retained_heads",
    "expected_retained_total",
    "gate_event_absolute_traffic_total",
    "cumulative_net_edge_throughput_total",
    "cumulative_net_inter_cycle_throughput_total",
)
per_head_fields = (
    "gate_event_absolute_traffic_per_retained_head",
    "cumulative_net_edge_throughput_per_retained_head",
    "cumulative_net_inter_cycle_throughput_per_retained_head",
)


def ratios(numerator, denominator, fields):
    return {field: numerator[field] / denominator[field] for field in fields}


out = {
    "schema": "R_CONNECTED_L4_L6_L8_TRAJECTORY_NUMERICAL_V001",
    "sizes": [4, 6, 8],
    "parent_L4_L8_result_sha256": hashlib.sha256(parent_bytes).hexdigest(),
    "selected_recipe": parent["selected_recipe"],
    "rows": rows,
    "raw_adjacent_total_ratios": {
        "L6_over_L4": ratios(l6, l4, total_fields),
        "L8_over_L6": ratios(l8, l6, total_fields),
    },
    "raw_adjacent_per_head_ratios": {
        "L6_over_L4": ratios(l6, l4, per_head_fields),
        "L8_over_L6": ratios(l8, l6, per_head_fields),
    },
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "coordinate_status": "INHERITED_FINITE_FAMILY_ENUMERATION__NOT_PHYSICAL_GRID",
    "classification": (
        "CONTROLLED_NUMERICAL_THREE_SIZE_RECORD_TRAJECTORY__NO_FIT__"
        "RESIDUALS_UNASSIGNED_UNTIL_OWNER_CLASSIFICATION"
    ),
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
}

rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
HERE.joinpath("RESULT.json").write_text(rendered)
print(rendered, end="")

assert [row["L"] for row in rows] == [4, 6, 8]
assert [row["connected_components"] for row in rows] == [4, 9, 16]
assert [row["retained_heads"] for row in rows] == [32, 108, 256]
assert l6["owned_supports_per_component_per_depth"] == 18
assert l6["active_cumulative_supports_per_component"] == 18
assert l6["active_cumulative_inter_cycle_supports_per_component"] == 6
assert l6["owner_once_gate_events_per_component"] == 54
assert abs(l6["expected_retained_total"] - 54.0) < 3e-13
assert l6["max_abs_connected_edge_correlation"] > 1e-3
assert l6["record_ledger_residual_l1_per_component"] < 3e-14
assert l6["record_ledger_residual_linf_per_component"] < 5e-15
assert l6["norm_error"] < 2e-14
assert l6["number_law_max_change"] < 2e-15
assert all(
    value > 0.0
    for group in out["raw_adjacent_total_ratios"].values()
    for value in group.values()
)
assert all(
    value > 0.0
    for group in out["raw_adjacent_per_head_ratios"].values()
    for value in group.values()
)
assert out["classification"].endswith("UNTIL_OWNER_CLASSIFICATION")
print("PASS__R_CONNECTED_L4_L6_L8_TRAJECTORY__15/15")
