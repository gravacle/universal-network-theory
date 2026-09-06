#!/usr/bin/env python3
"""Independent structural/operator attacks on the fixed-width engine."""

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
TARGET = json.loads((ROOT / "DEVELOPMENT_R_CONNECTED_FIXED_WIDTH_ENGINE_V001" / "RESULT.json").read_text())
PRIOR = json.loads((ROOT / "AUDIT_R_CONNECTED_PRISM_ORBIT_REDUCTION_V001" / "INDEPENDENT_RESULT.json").read_text())


def permute_word(word, permutation):
    image = 0
    for old, new in enumerate(permutation):
        image |= ((word >> old) & 1) << new
    return image


def group_for(length):
    out = []
    for sign in (1, -1):
        for shift in range(length):
            permutation = []
            for layer in range(2):
                for native in range(length):
                    prism = (native - layer) % length
                    new_layer = layer ^ (shift & 1)
                    new_prism = (sign * prism + shift) % length
                    permutation.append(new_layer * length + (new_prism + new_layer) % length)
            out.append(tuple(permutation))
    return out


def edges_for(length):
    return ([(i, (i + 1) % length, 0) for i in range(length)]
            + [(length + i, length + (i + 1) % length, 0) for i in range(length)]
            + [(i, length + (i + 1) % length, 1) for i in range(length)])


L = 4
D = 1 << (2 * L)
group = group_for(L)
edges = edges_for(L)
assert len(set(group)) == 2 * L

# Direct full-image orbit partition; no chunk tables and no target functions.
orbit_id = np.full(D, -1, np.int32)
representatives = []
sizes = []
for seed in range(D):
    if orbit_id[seed] >= 0:
        continue
    images = sorted({permute_word(seed, permutation) for permutation in group})
    index = len(representatives)
    representatives.append(seed)
    sizes.append(len(images))
    for image in images:
        assert orbit_id[image] in (-1, index)
        orbit_id[image] = index
assert np.all(orbit_id >= 0) and sum(sizes) == D and len(representatives) == 55
representatives = np.array(representatives, np.uint32)
sizes = np.array(sizes, np.uint8)

# Independently emulate the two L-bit chunk tables, then demand exact agreement.
for permutation in group:
    low = np.array([permute_word(word, permutation) for word in range(1 << L)], np.uint32)
    high = np.array([permute_word(word << L, permutation) for word in range(1 << L)], np.uint32)
    for word in range(D):
        assert int(low[word & 15] | high[word >> L]) == permute_word(word, permutation)

# Assemble the unaggregated fixed-width action and compare it to direct full-space
# projection for arbitrary complex invariant vectors.
M = len(representatives)
H = np.zeros((M, M), np.float64)
unaggregated = []
for a, word0 in enumerate(representatives):
    word = int(word0)
    for edge_index, (u, v, _) in enumerate(edges):
        if ((word >> u) & 1) == ((word >> v) & 1):
            continue
        b = int(orbit_id[word ^ (1 << u) ^ (1 << v)])
        coefficient = -math.sqrt(float(sizes[a]) / float(sizes[b]))
        unaggregated.append((a, b, edge_index, coefficient))
        H[b, a] += coefficient
assert len(unaggregated) == 330
assert np.max(np.abs(H - H.T)) < 2e-15

rng = np.random.default_rng(20260906)
x = rng.normal(size=M) + 1j * rng.normal(size=M)
x /= np.linalg.norm(x)
phi = x[orbit_id] / np.sqrt(sizes.astype(np.float64)[orbit_id])
full_out = np.zeros(D, np.complex128)
for word in range(D):
    for u, v, _ in edges:
        if ((word >> u) & 1) != ((word >> v) & 1):
            full_out[word ^ (1 << u) ^ (1 << v)] -= phi[word]
projected = np.array([
    sum(full_out[orbit_id == orbit]) / math.sqrt(float(sizes[orbit]))
    for orbit in range(M)
])
compressed_out = np.sum(H * x[np.newaxis, :], axis=1)
action_error = float(np.max(np.abs(compressed_out - projected)))
assert action_error < 3e-15

# Derive signed edge orbits and compare their compressed formula directly with
# each full-space oriented current operator. No incidence matrix, continuity
# equation, ledger residual, or Ward relation is used in this test.
oriented = [(u, v) for u, v, _ in edges]
lookup = {pair: (i, 1) for i, pair in enumerate(oriented)}
lookup.update({(v, u): (i, -1) for i, (u, v) in enumerate(oriented)})
mapping = {}
edge_reps = []
for seed in range(len(edges)):
    if seed in mapping:
        continue
    edge_reps.append(seed)
    rep = len(edge_reps) - 1
    for permutation in group:
        index, sign = lookup[(permutation[oriented[seed][0]], permutation[oriented[seed][1]])]
        assert index not in mapping or mapping[index] == (rep, sign)
        mapping[index] = (rep, sign)
assert len(edge_reps) == 2 and len(mapping) == len(edges)

sums = np.zeros(2, np.complex128)
for a, b, edge_index, coefficient in unaggregated:
    rep, sign = mapping[edge_index]
    word = int(representatives[a]); u, v, _ = edges[edge_index]
    orientation = ((word >> v) & 1) - ((word >> u) & 1)
    sums[rep] += np.conjugate(x[b]) * (1j * sign * orientation * coefficient) * x[a]
compressed_reps = np.array([sums[0].real / (2 * L), sums[1].real / L])
full_currents = []
for u, v, _ in edges:
    value = 0j
    for word in range(D):
        bu, bv = (word >> u) & 1, (word >> v) & 1
        if bu != bv:
            swapped = word ^ (1 << u) ^ (1 << v)
            value += np.conjugate(phi[swapped]) * (-1j * (bv - bu)) * phi[word]
    full_currents.append(value.real)
reconstructed = np.array([mapping[i][1] * compressed_reps[mapping[i][0]] for i in range(len(edges))])
current_error = float(np.max(np.abs(reconstructed - np.array(full_currents))))
assert current_error < 3e-16

# The repair is materially necessary on this NumPy build and mathematically
# correct: byte storage is retained, but amplitude arithmetic is float64.
assert np.sqrt(np.array([8], dtype=np.uint8)).dtype == np.float16
valid = (representatives & sum(1 << i for i in range(0, 2 * L, 2))) == 0
repaired = np.sqrt(sizes[valid].astype(np.float64)) / math.sqrt(1 << L)
expected_amplitudes = np.array([math.sqrt(int(v)) / math.sqrt(1 << L) for v in sizes[valid]])
amplitude_error = float(np.max(np.abs(repaired - expected_amplitudes)))
assert repaired.dtype == np.float64 and amplitude_error == 0.0

# Numerical parity comes from a distinct, hostile-audited generator-BFS,
# destination-normalized quotient and RK4(4096)+Simpson implementation.
prior_rows = {row["L"]: row for row in PRIOR["rows"]}
target_rows = {row["L"]: row for row in TARGET["rows"]}
for length in (4, 6, 8, 10):
    p, t = prior_rows[length], target_rows[length]
    assert p["q_target_linf"] < 3e-12 and p["current_target_linf"] < 2e-12
    assert t["q_target_linf"] < 4e-11 and t["current_target_linf"] < 4e-11
    sealed = json.loads((ROOT / ({4:"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001",6:"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001",8:"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001",10:"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001"}[length]) / "RESULT.json").read_text())
    sealed = next(row for row in sealed["rows"] if row["kappa"] == math.pi / 2) if length == 4 else sealed
    assert max(abs(a-b) for a,b in zip(p["q_after"], sealed["q_after"])) < 3e-12
    assert max(abs(a-b) for a,b in zip(p["integrated_oriented_currents"], sealed["integrated_oriented_currents"])) < 2e-12
    assert abs(t["max_abs_connected_edge_correlation"] - sealed["max_abs_connected_edge_correlation"]) < 4e-11

print(json.dumps({"action_error_L4": action_error, "current_error_L4": current_error,
                  "amplitude_error_L4": amplitude_error, "independent_lower_size_parity": "PASS"}, sort_keys=True))
print("PASS__INDEPENDENT_FIXED_WIDTH_ENGINE_ATTACKS")
