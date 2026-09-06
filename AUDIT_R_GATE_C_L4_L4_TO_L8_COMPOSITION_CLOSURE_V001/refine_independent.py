#!/usr/bin/env python3
"""Pre-target high-resolution Suzuki refinement of the frozen L8 spectrum."""

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
FROZEN = HERE / "FROZEN_INDEPENDENT.json"
OUT = HERE / "FROZEN_REFINEMENT.json"
PROTOCOL = ROOT / "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/PROTOCOL.md"
EXPECTED_PROTOCOL_SHA256 = "e0245dc81edb15be8b5ece72ff196f19754976a41a5785941e3dba2428bdcbb4"
STEPS = 2048
KAPPA = math.pi / 2.0


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges():
    result = []
    for rail in (0, 1):
        offset = 8 * rail
        for node in range(8):
            result.append((offset + node, offset + (node + 1) % 8, f"rail_{rail + 1}"))
    for node in range(8):
        result.append((node, 8 + (node + 1) % 8, "connector"))
    return result


def initial_state():
    odd_sites = (1, 3, 5, 7, 9, 11, 13, 15)
    state = np.zeros(1 << 16, dtype=np.complex128)
    for subset in range(1 << 8):
        word = 0
        for index, site in enumerate(odd_sites):
            if subset & (1 << index):
                word |= 1 << site
        state[word] = 1.0 / 16.0
    return state


def pairs_for(edge_list):
    words = np.arange(1 << 16, dtype=np.int64)
    pairs = []
    for u, v, _ in edge_list:
        bu = (words >> u) & 1
        bv = (words >> v) & 1
        left = np.flatnonzero((bu == 0) & (bv == 1))
        pairs.append((left, left ^ (1 << u) ^ (1 << v)))
    return pairs


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


def matrix_from_state(state):
    left_sites = (0, 1, 2, 3, 8, 9, 10, 11)
    right_sites = (4, 5, 6, 7, 12, 13, 14, 15)
    words = np.arange(len(state), dtype=np.int64)
    left = np.zeros(len(state), dtype=np.int64)
    right = np.zeros(len(state), dtype=np.int64)
    for index, site in enumerate(left_sites):
        left |= ((words >> site) & 1) << index
    for index, site in enumerate(right_sites):
        right |= ((words >> site) & 1) << index
    matrix = np.zeros((256, 256), dtype=np.complex128)
    matrix[left, right] = state
    return matrix


started = time.perf_counter()
if OUT.exists():
    raise AssertionError("refusing to overwrite frozen refinement")
if sha256(PROTOCOL) != EXPECTED_PROTOCOL_SHA256:
    raise AssertionError("protocol custody failure")
frozen = json.loads(FROZEN.read_text())
edge_list = edges()
pairs = pairs_for(edge_list)
groups = (
    tuple(index for index in range(16) if (index % 8) % 2 == 0),
    tuple(index for index in range(16) if (index % 8) % 2 == 1),
    tuple(range(16, 24)),
)
state = initial_state()
interval = KAPPA / STEPS
for _ in range(STEPS):
    second_order(state, pairs, groups, W1 * interval)
    second_order(state, pairs, groups, W0 * interval)
    second_order(state, pairs, groups, W1 * interval)
singular = np.linalg.svd(matrix_from_state(state), compute_uv=False)
primary = np.array(frozen["observations"]["8"]["lanczos_interface"]["singular_values"])
difference = np.abs(singular - primary)
elapsed = time.perf_counter() - started
rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes = int(rss_raw if sys.platform == "darwin" else rss_raw * 1024)
result = {
    "schema": "FROZEN_INDEPENDENT_REFINEMENT_R_GATE_C_L8_COMPOSITION_V001",
    "freeze_status": "HIGH_RESOLUTION_CROSS_SOLVER_FROZEN_BEFORE_TARGET_INSPECTION",
    "protocol_sha256": sha256(PROTOCOL),
    "antecedent_frozen_sha256": sha256(FROZEN),
    "method": "UNITARY_FOURTH_ORDER_SUZUKI_YOSHIDA__2048_STEPS",
    "steps": STEPS,
    "norm_error": float(abs(np.linalg.norm(state) - 1.0)),
    "singular_values": [float(value) for value in singular],
    "smallest_five": [float(value) for value in singular[-5:]],
    "primary_lanczos_smallest_five": [float(value) for value in primary[-5:]],
    "singular_value_linf_vs_primary_lanczos": float(np.max(difference)),
    "smallest_five_abs_difference": [float(value) for value in difference[-5:]],
    "ranks_by_absolute_threshold": {
        f"threshold_{threshold:.0e}": int(np.count_nonzero(singular > threshold))
        for threshold in (1e-8, 1e-10, 1e-12, 1e-13, 1e-14)
    },
    "rank_255_separation_ratio": float(singular[-2] / max(difference[-2], 2e-15)),
    "last_value_to_cross_solver_difference": float(singular[-1] / max(difference[-1], 2e-15)),
    "resources": {
        "runtime_seconds": elapsed,
        "max_rss_bytes": rss_bytes,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "numpy": np.__version__,
    },
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(f"FROZEN_REFINEMENT={OUT}")
print(f"SINGULAR_LINF_VS_LANCZOS={result['singular_value_linf_vs_primary_lanczos']:.17g}")
print(f"SMALLEST_FIVE={result['smallest_five']}")
print(f"RANKS={result['ranks_by_absolute_threshold']}")
print(f"RUNTIME_SECONDS={elapsed:.9f}")
print(f"MAX_RSS_BYTES={rss_bytes}")
