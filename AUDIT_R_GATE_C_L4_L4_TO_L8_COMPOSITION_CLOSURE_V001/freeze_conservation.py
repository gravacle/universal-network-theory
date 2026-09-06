#!/usr/bin/env python3
"""Freeze independent Suzuki current and conservation records for L4/L8."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import resource
import sys
import time
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PROTOCOL = ROOT / "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/PROTOCOL.md"
OUT = HERE / "FROZEN_CONSERVATION.json"
EXPECTED_PROTOCOL_SHA256 = "e0245dc81edb15be8b5ece72ff196f19754976a41a5785941e3dba2428bdcbb4"
KAPPA = math.pi / 2.0
STEPS = {4: (256, 512), 8: (512, 1024)}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_for(length):
    edges = []
    for rail in (0, 1):
        offset = rail * length
        for node in range(length):
            edges.append((offset + node, offset + (node + 1) % length))
    for node in range(length):
        edges.append((node, length + (node + 1) % length))
    return edges


def source(length):
    sites = 2 * length
    odd_sites = [rail * length + node for rail in (0, 1) for node in range(length) if node % 2]
    state = np.zeros(1 << sites, dtype=np.complex128)
    scale = 2.0 ** (-0.5 * len(odd_sites))
    for subset in range(1 << len(odd_sites)):
        word = 0
        for index, site in enumerate(odd_sites):
            if subset & (1 << index):
                word |= 1 << site
        state[word] = scale
    return state


def edge_pairs(edges, sites):
    words = np.arange(1 << sites, dtype=np.int64)
    result = []
    for u, v in edges:
        bu = (words >> u) & 1
        bv = (words >> v) & 1
        left = np.flatnonzero((bu == 0) & (bv == 1))
        result.append((left, left ^ (1 << u) ^ (1 << v)))
    return result


def h_action(state, pairs):
    out = np.zeros_like(state)
    for left, right in pairs:
        out[left] -= state[right]
        out[right] -= state[left]
    return out


def currents(state, pairs):
    result = np.empty(len(pairs), dtype=float)
    for index, (left, right) in enumerate(pairs):
        result[index] = np.sum(
            state[left].conj() * (1j * state[right])
            + state[right].conj() * (-1j * state[left])
        ).real
    return result


def apply_edge(state, pair, interval):
    left, right = pair
    a = state[left].copy()
    b = state[right].copy()
    c = math.cos(interval)
    s = 1j * math.sin(interval)
    state[left] = c * a + s * b
    state[right] = s * a + c * b


def apply_group(state, pairs, group, interval):
    for edge in group:
        apply_edge(state, pairs[edge], interval)


def second_order(state, pairs, groups, interval):
    apply_group(state, pairs, groups[0], interval / 2.0)
    apply_group(state, pairs, groups[1], interval / 2.0)
    apply_group(state, pairs, groups[2], interval)
    apply_group(state, pairs, groups[1], interval / 2.0)
    apply_group(state, pairs, groups[0], interval / 2.0)


W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
W0 = -(2.0 ** (1.0 / 3.0)) / (2.0 - 2.0 ** (1.0 / 3.0))


def evolve(length, steps):
    edges = edges_for(length)
    pairs = edge_pairs(edges, 2 * length)
    groups = (
        tuple(index for index in range(2 * length) if (index % length) % 2 == 0),
        tuple(index for index in range(2 * length) if (index % length) % 2 == 1),
        tuple(range(2 * length, 3 * length)),
    )
    initial = source(length)
    state = initial.copy()
    interval = KAPPA / steps
    integral = currents(state, pairs)
    for step in range(1, steps + 1):
        second_order(state, pairs, groups, W1 * interval)
        second_order(state, pairs, groups, W0 * interval)
        second_order(state, pairs, groups, W1 * interval)
        integral += (1.0 if step == steps else 4.0 if step % 2 else 2.0) * currents(state, pairs)
    return initial, state, integral * (interval / 3.0), edges, pairs


def diagnostics(length, initial, state, integrated_current, edges, pairs):
    words = np.arange(len(state), dtype=np.int64)
    number = np.array([bin(int(word)).count("1") for word in words])
    q_initial = np.array([np.sum(np.abs(initial) ** 2 * ((words >> site) & 1)) for site in range(2 * length)])
    q_final = np.array([np.sum(np.abs(state) ** 2 * ((words >> site) & 1)) for site in range(2 * length)])
    incidence = np.zeros((2 * length, len(edges)))
    for edge, (u, v) in enumerate(edges):
        incidence[u, edge] = 1.0
        incidence[v, edge] = -1.0
    residual = q_final - q_initial + np.einsum("se,e->s", incidence, integrated_current, optimize=False)
    correlations = []
    probability = np.abs(state) ** 2
    for u, v in edges:
        joint = np.sum(probability * ((words >> u) & 1) * ((words >> v) & 1))
        correlations.append(float(joint - q_final[u] * q_final[v]))
    return {
        "q_initial": [float(value) for value in q_initial],
        "q_final": [float(value) for value in q_final],
        "integrated_owner_currents": [float(value) for value in integrated_current],
        "ledger_residual": [float(value) for value in residual],
        "ledger_l1": float(np.sum(np.abs(residual))),
        "ledger_linf": float(np.max(np.abs(residual))),
        "norm_error": float(abs(np.vdot(state, state).real - 1.0)),
        "number_initial": float(np.sum(np.abs(initial) ** 2 * number)),
        "number_final": float(np.sum(np.abs(state) ** 2 * number)),
        "energy_initial": float(np.vdot(initial, h_action(initial, pairs)).real),
        "energy_final": float(np.vdot(state, h_action(state, pairs)).real),
        "connected_edge_correlations": correlations,
        "max_abs_connected_edge_correlation": float(np.max(np.abs(correlations))),
    }


started = time.perf_counter()
if OUT.exists():
    raise AssertionError("refusing to overwrite frozen conservation record")
if sha256(PROTOCOL) != EXPECTED_PROTOCOL_SHA256:
    raise AssertionError("protocol custody failure")
rows = {}
for length in (4, 8):
    coarse_data = evolve(length, STEPS[length][0])
    fine_data = evolve(length, STEPS[length][1])
    coarse = diagnostics(length, *coarse_data)
    fine = diagnostics(length, *fine_data)
    rows[str(length)] = {
        "coarse_steps": STEPS[length][0],
        "fine_steps": STEPS[length][1],
        "coarse": coarse,
        "fine": fine,
        "q_coarse_fine_linf": float(np.max(np.abs(np.array(coarse["q_final"]) - np.array(fine["q_final"])))),
        "current_coarse_fine_linf": float(np.max(np.abs(np.array(coarse["integrated_owner_currents"]) - np.array(fine["integrated_owner_currents"])))),
        "correlation_coarse_fine_linf": float(np.max(np.abs(np.array(coarse["connected_edge_correlations"]) - np.array(fine["connected_edge_correlations"])))),
    }
elapsed = time.perf_counter() - started
rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes = int(rss_raw if sys.platform == "darwin" else rss_raw * 1024)
result = {
    "schema": "FROZEN_INDEPENDENT_CONSERVATION_R_GATE_C_L4_L8_COMPOSITION_V001",
    "freeze_status": "INDEPENDENT_CONSERVATION_RECORD",
    "protocol_sha256": sha256(PROTOCOL),
    "method": "UNITARY_FOURTH_ORDER_SUZUKI_YOSHIDA__SIMPSON_CURRENT_QUADRATURE",
    "rows": rows,
    "resources": {
        "runtime_seconds": elapsed,
        "max_rss_bytes": rss_bytes,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "numpy": np.__version__,
    },
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(f"FROZEN_CONSERVATION={OUT}")
for length in (4, 8):
    row = rows[str(length)]
    print(f"L{length}_CURRENT_COARSE_FINE_LINF={row['current_coarse_fine_linf']:.17g}")
    print(f"L{length}_LEDGER_L1={row['fine']['ledger_l1']:.17g}")
print(f"RUNTIME_SECONDS={elapsed:.9f}")
print(f"MAX_RSS_BYTES={rss_bytes}")
