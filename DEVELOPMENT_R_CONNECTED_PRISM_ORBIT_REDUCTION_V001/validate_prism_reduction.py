#!/usr/bin/env python3
"""Validate the order-2L source-preserving prism orbit basis on L4--L10."""

from __future__ import annotations

import json
import math
import os
from collections import Counter
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from numba import njit


KAPPA = math.pi / 2.0
ORDER = 10
STEPS = 2048
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
TARGETS = {
    4: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json",
    6: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json",
    8: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json",
    10: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001" / "RESULT.json",
}


@njit
def h_apply(x, src, dst, val, n):
    out = np.zeros(n, np.complex128)
    for k in range(val.size):
        out[dst[k]] += val[k] * x[src[k]]
    return out


@njit
def j_expect(x, left, right, factor):
    out = 0.0j
    for k in range(factor.size):
        out += np.conjugate(x[left[k]]) * (1.0j * factor[k]) * x[right[k]]
    return out.real


def edges_for(length):
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append((layer * length + site, layer * length + (site + 1) % length, "internal"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def prism_group(length):
    # Prism coordinate is x=i-a; return to the original shifted-connector label
    # with i=x+a.  Source parity forces layer swap parity = k mod 2.
    group = []
    for epsilon in (1, -1):
        for shift in range(length):
            swap = shift % 2
            permutation = []
            for layer in range(2):
                for site in range(length):
                    prism_site = (site - layer) % length
                    moved_layer = layer ^ swap
                    moved_prism_site = (epsilon * prism_site + shift) % length
                    moved_site = (moved_prism_site + moved_layer) % length
                    permutation.append(moved_layer * length + moved_site)
            group.append(tuple(permutation))
    if len(set(group)) != 2 * length:
        raise AssertionError("prism group is not faithful")
    return group


def permute_word(word, permutation):
    out = 0
    for source, destination in enumerate(permutation):
        if (word >> source) & 1:
            out |= 1 << destination
    return out


def orbit_partition(length, group):
    full_dimension = 1 << (2 * length)
    orbit_ids = np.full(full_dimension, -1, np.int32)
    representatives, sizes = [], []
    for word in range(full_dimension):
        if orbit_ids[word] >= 0:
            continue
        orbit = sorted({permute_word(word, permutation) for permutation in group})
        orbit_id = len(representatives)
        orbit_ids[orbit] = orbit_id
        representatives.append(word)
        sizes.append(len(orbit))
    return orbit_ids, np.array(representatives, np.int64), np.array(sizes, np.int64)


def quotient(edges, orbit_ids, representatives, sizes):
    src, dst, val = [], [], []
    for source, raw_word in enumerate(representatives):
        word = int(raw_word)
        counts = Counter()
        for u, v, _ in edges:
            if ((word >> u) & 1) != ((word >> v) & 1):
                counts[int(orbit_ids[word ^ (1 << u) ^ (1 << v)])] += 1
        for destination, multiplicity in sorted(counts.items()):
            src.append(source)
            dst.append(destination)
            val.append(-multiplicity * math.sqrt(sizes[source] / sizes[destination]))
    src = np.array(src, np.int32)
    dst = np.array(dst, np.int32)
    val = np.array(val, float)
    n = len(representatives)
    keys = src.astype(np.int64) * n + dst
    order = np.argsort(keys)
    sorted_keys = keys[order]
    reverse = dst.astype(np.int64) * n + src
    positions = np.searchsorted(sorted_keys, reverse)
    if np.any(positions == len(sorted_keys)) or np.any(sorted_keys[positions] != reverse):
        raise AssertionError("quotient reverse entry missing")
    hermiticity_error = float(np.max(np.abs(val - val[order][positions])))
    return src, dst, val, hermiticity_error


def signed_edge_orbits(edges, group):
    lookup = {frozenset((u, v)): (index, u, v) for index, (u, v, _) in enumerate(edges)}
    reconstruction = [None] * len(edges)
    representatives = []
    for edge_index, (u, v, _) in enumerate(edges):
        if reconstruction[edge_index] is not None:
            continue
        representative_index = len(representatives)
        representatives.append(edge_index)
        observed = {}
        for permutation in group:
            moved_u, moved_v = permutation[u], permutation[v]
            target, stored_u, stored_v = lookup[frozenset((moved_u, moved_v))]
            sign = 1 if (moved_u, moved_v) == (stored_u, stored_v) else -1
            if target in observed and observed[target] != sign:
                raise AssertionError("edge orbit contains an orientation contradiction")
            observed[target] = sign
        for target, sign in observed.items():
            reconstruction[target] = (representative_index, sign)
    if any(value is None for value in reconstruction):
        raise AssertionError("edge reconstruction incomplete")
    return representatives, reconstruction


def current_kernel(u, v, words, orbit_ids, sizes):
    active = words[(((words >> u) & 1) != ((words >> v) & 1))]
    swapped = active ^ (1 << u) ^ (1 << v)
    left, right = orbit_ids[active], orbit_ids[swapped]
    sign = ((active >> v) & 1) - ((active >> u) & 1)
    return left, right, sign / np.sqrt(sizes[left] * sizes[right])


def run(length):
    sites = 2 * length
    full_dimension = 1 << sites
    edges = edges_for(length)
    group = prism_group(length)
    edge_set = {frozenset((u, v)) for u, v, _ in edges}
    for permutation in group:
        if {frozenset((permutation[u], permutation[v])) for u, v, _ in edges} != edge_set:
            raise AssertionError("group does not preserve support")
        if any(permutation[site] % 2 != site % 2 for site in range(sites)):
            raise AssertionError("group does not preserve source parity")
    orbit_ids, orbit_representatives, orbit_sizes = orbit_partition(length, group)
    src, dst, val, hermiticity = quotient(edges, orbit_ids, orbit_representatives, orbit_sizes)
    n = len(orbit_representatives)
    words = np.arange(full_dimension, dtype=np.int64)
    edge_representatives, reconstruction = signed_edge_orbits(edges, group)
    kernels = [current_kernel(edges[e][0], edges[e][1], words, orbit_ids, orbit_sizes) for e in edge_representatives]

    def H(x):
        return h_apply(x, src, dst, val, n)

    def currents(x):
        representatives = [j_expect(x, *kernel) for kernel in kernels]
        return np.array([sign * representatives[rep] for rep, sign in reconstruction])

    psi0 = np.zeros(n, np.complex128)
    even_mask = sum(1 << site for site in range(0, sites, 2))
    valid = (orbit_representatives & even_mask) == 0
    psi0[valid] = np.sqrt(orbit_sizes[valid]) / math.sqrt(1 << length)
    psi = psi0.copy()
    step = KAPPA / STEPS
    J = currents(psi)
    for index in range(1, STEPS + 1):
        out, term = psi.copy(), psi.copy()
        for order in range(1, ORDER + 1):
            term = (-1.0j * step / order) * H(term)
            out += term
        psi = out
        weight = 1.0 if index == STEPS else (4.0 if index % 2 else 2.0)
        J += weight * currents(psi)
    J *= step / 3.0

    probability = np.abs(psi[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
    probability0 = np.abs(psi0[orbit_ids]) ** 2 / orbit_sizes[orbit_ids]
    q = np.array([np.sum(probability[((words >> site) & 1) == 1]) for site in range(sites)])
    q0 = np.array([np.sum(probability0[((words >> site) & 1) == 1]) for site in range(sites)])
    incidence = np.zeros((sites, len(edges)))
    for index, (u, v, _) in enumerate(edges):
        incidence[u, index] = 1.0
        incidence[v, index] = -1.0
    residual = q - q0 + incidence @ J
    particle_number = np.array([bin(int(word)).count("1") for word in orbit_representatives])
    law0 = np.array([np.sum(np.abs(psi0[particle_number == value]) ** 2) for value in range(sites + 1)])
    law = np.array([np.sum(np.abs(psi[particle_number == value]) ** 2) for value in range(sites + 1)])

    target_packet = json.loads(TARGETS[length].read_text())
    target = next(row for row in target_packet["rows"] if row["kappa"] == KAPPA) if length == 4 else target_packet
    return {
        "L": length,
        "full_dimension": full_dimension,
        "finite_group_order": len(group),
        "orbit_dimension": n,
        "orbit_size_histogram": {str(k): v for k, v in sorted(Counter(orbit_sizes.tolist()).items())},
        "quotient_nonzero_entries": len(val),
        "quotient_hermiticity_error": hermiticity,
        "signed_edge_orbits": len(edge_representatives),
        "q_target_linf": float(np.max(np.abs(q - np.array(target["q_after"])))),
        "current_target_linf": float(np.max(np.abs(J - np.array(target["integrated_oriented_currents"])))),
        "record_ledger_residual_l1": float(np.sum(np.abs(residual))),
        "record_ledger_residual_linf": float(np.max(np.abs(residual))),
        "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
        "energy_error": float(abs(np.vdot(psi, H(psi)).real - np.vdot(psi0, H(psi0)).real)),
        "number_law_max_change": float(np.max(np.abs(law - law0))),
    }


rows = [run(length) for length in (4, 6, 8, 10)]
checks = []
for row in rows:
    length = row["L"]
    checks.extend([
        (row["finite_group_order"] == 2 * length, f"L{length} group order"),
        (row["orbit_dimension"] < row["full_dimension"], f"L{length} compression"),
        (row["quotient_hermiticity_error"] < 1.0e-14, f"L{length} Hermiticity"),
        (row["signed_edge_orbits"] == 2, f"L{length} signed edge orbits"),
        (row["q_target_linf"] < 3.0e-11, f"L{length} occupations"),
        (row["current_target_linf"] < 3.0e-11, f"L{length} currents"),
        (row["record_ledger_residual_l1"] < 5.0e-10, f"L{length} ledger"),
        (row["norm_error"] < 5.0e-10, f"L{length} norm"),
        (row["energy_error"] < 5.0e-9, f"L{length} energy"),
        (row["number_law_max_change"] < 5.0e-10, f"L{length} number law"),
    ])
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_CONNECTED_PRISM_ORBIT_REDUCTION_V001",
    "classification": "EXACT_ORDER_2L_SOURCE_PRESERVING_FINITE_PRISM_GROUP__NUMERICAL_EVOLUTION_CROSSCHECK",
    "scope": "COMPUTATIONAL_COMPRESSION_OF_DECLARED_FINITE_SUPPORT__NO_NEW_PHYSICS",
    "parameters": {"kappa": KAPPA, "taylor_order": ORDER, "steps": STEPS},
    "rows": rows,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "not_claimed": "MAXIMAL_GRAPH_AUTOMORPHISM_GROUP__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__CRITICAL_PHASE__GRAVITY",
}


def compatible(observed, canonical, path="root"):
    if isinstance(canonical, dict):
        if not isinstance(observed, dict) or set(observed) != set(canonical):
            raise AssertionError(f"canonical keys differ at {path}")
        for key in canonical:
            compatible(observed[key], canonical[key], f"{path}.{key}")
    elif isinstance(canonical, list):
        if not isinstance(observed, list) or len(observed) != len(canonical):
            raise AssertionError(f"canonical list differs at {path}")
        for index, (left, right) in enumerate(zip(observed, canonical)):
            compatible(left, right, f"{path}[{index}]")
    elif isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 8.0e-10:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_CONNECTED_PRISM_ORBIT_REDUCTION__{len(checks)}/{len(checks)}")
