#!/usr/bin/env python3
"""Connected native-component record trajectory at L=4 and L=8."""

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


DEPTH = 3
DELTA = 1.0
THETA = math.pi / 8.0
SIZES = (4, 8)


def run_size(size):
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
    retained_per_cluster = float(np.sum(q_final))
    net_throughput_per_cluster = float(np.sum(np.abs(currents)))
    rung_throughput_per_cluster = float(np.sum(np.abs(rung_currents)))
    total_event_traffic = float(clusters * event_traffic)
    total_net_throughput = float(clusters * net_throughput_per_cluster)
    total_rung_throughput = float(clusters * rung_throughput_per_cluster)
    retained_heads = size ** 3 // 2
    return {
        "L": size,
        "cells": size ** 3,
        "prepared_source_lineages": size ** 3 // 2,
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
        "expected_retained_per_component": retained_per_cluster,
        "expected_retained_total": float(clusters * retained_per_cluster),
        "gate_event_absolute_traffic_per_component": float(event_traffic),
        "gate_event_absolute_traffic_total": total_event_traffic,
        "gate_event_absolute_traffic_per_retained_head": float(
            total_event_traffic / retained_heads
        ),
        "cumulative_net_edge_throughput_per_component": net_throughput_per_cluster,
        "cumulative_net_edge_throughput_total": total_net_throughput,
        "cumulative_net_edge_throughput_per_retained_head": float(
            total_net_throughput / retained_heads
        ),
        "cumulative_net_inter_cycle_throughput_per_component": (
            rung_throughput_per_cluster
        ),
        "cumulative_net_inter_cycle_throughput_total": total_rung_throughput,
        "cumulative_net_inter_cycle_throughput_per_retained_head": float(
            total_rung_throughput / retained_heads
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


rows = [run_size(size) for size in SIZES]
l4, l8 = rows
ratio_fields = (
    "cells",
    "prepared_source_lineages",
    "retained_heads",
    "connected_components",
    "expected_retained_total",
    "gate_event_absolute_traffic_total",
    "cumulative_net_edge_throughput_total",
    "cumulative_net_inter_cycle_throughput_total",
)
ratios = {field: l8[field] / l4[field] for field in ratio_fields}
per_head_ratio_fields = (
    "gate_event_absolute_traffic_per_retained_head",
    "cumulative_net_edge_throughput_per_retained_head",
    "cumulative_net_inter_cycle_throughput_per_retained_head",
)
per_head_ratios = {
    field: l8[field] / l4[field] for field in per_head_ratio_fields
}
out = {
    "schema": "R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_NUMERICAL_V001",
    "sizes": list(SIZES),
    "selected_recipe": {
        "component": "TWO_NATIVE_Y_CYCLES_PAIRED_BY_Z_GENERATOR",
        "preparation_pattern": "reversed",
        "gate_order": "forward",
        "depth": DEPTH,
        "staggered_delta": DELTA,
        "transfer_angle": THETA,
    },
    "rows": rows,
    "raw_L8_over_L4_ratios": ratios,
    "raw_L8_over_L4_per_head_ratios": per_head_ratios,
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "coordinate_status": "INHERITED_FINITE_FAMILY_ENUMERATION__NOT_PHYSICAL_GRID",
    "classification": (
        "CONTROLLED_NUMERICAL_CONNECTED_FINITE_SIZE_TRAJECTORY__RAW_RATIOS_"
        "ONLY__RESIDUALS_UNASSIGNED_UNTIL_OWNER_CLASSIFICATION"
    ),
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
}

rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
Path(__file__).with_name("RESULT.json").write_text(rendered)
print(rendered, end="")

assert [row["connected_components"] for row in rows] == [4, 16]
assert [row["retained_heads"] for row in rows] == [32, 256]
assert all(
    row["active_cumulative_supports_per_component"]
    == row["owned_supports_per_component_per_depth"]
    for row in rows
)
assert all(
    row["active_cumulative_inter_cycle_supports_per_component"] == row["L"]
    for row in rows
)
assert abs(l4["expected_retained_total"] - 16.0) < 1e-13
assert abs(l8["expected_retained_total"] - 128.0) < 5e-13
assert ratios["expected_retained_total"] > 7.9999999999999
assert ratios["gate_event_absolute_traffic_total"] > 1.0
assert ratios["cumulative_net_edge_throughput_total"] > 1.0
assert ratios["cumulative_net_inter_cycle_throughput_total"] > 1.0
assert all(row["max_abs_connected_edge_correlation"] > 1e-3 for row in rows)
assert max(row["record_ledger_residual_l1_per_component"] for row in rows) < 5e-14
assert max(row["record_ledger_residual_linf_per_component"] for row in rows) < 7e-15
assert max(row["norm_error"] for row in rows) < 3e-14
assert max(row["number_law_max_change"] for row in rows) < 3e-15
assert out["classification"].endswith("UNTIL_OWNER_CLASSIFICATION")
print("PASS__R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY__14/14")
