#!/usr/bin/env python3
"""Validate a fixed-width orbit/transition engine against sealed L4--L10 records."""

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
TAYLOR_ORDER = 10
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
def build_orbits(orbit_ids, representatives, sizes, low_table, high_table, mask, shift):
    orbit_count = 0
    for word in range(orbit_ids.size):
        if orbit_ids[word] >= 0:
            continue
        representatives[orbit_count] = word
        low = word & mask
        high = word >> shift
        orbit_size = 0
        for group_index in range(low_table.shape[0]):
            image = low_table[group_index, low] | high_table[group_index, high]
            previous = orbit_ids[image]
            if previous == -1:
                orbit_ids[image] = orbit_count
                orbit_size += 1
            elif previous != orbit_count:
                raise ValueError("orbit collision")
        sizes[orbit_count] = orbit_size
        orbit_count += 1
    return orbit_count


@njit
def count_transitions(representatives, edge_u, edge_v):
    offsets = np.empty(representatives.size + 1, np.int64)
    offsets[0] = 0
    for source in range(representatives.size):
        word = representatives[source]
        count = 0
        for edge_index in range(edge_u.size):
            if ((word >> edge_u[edge_index]) & 1) != ((word >> edge_v[edge_index]) & 1):
                count += 1
        offsets[source + 1] = offsets[source] + count
    return offsets


@njit
def fill_transitions(representatives, sizes, orbit_ids, offsets, edge_u, edge_v, edge_code):
    destinations = np.empty(offsets[-1], np.int32)
    coefficients = np.empty(offsets[-1], np.float64)
    current_codes = np.empty(offsets[-1], np.int8)
    for source in range(representatives.size):
        word = representatives[source]
        cursor = offsets[source]
        for edge_index in range(edge_u.size):
            u = edge_u[edge_index]
            v = edge_v[edge_index]
            bit_u = (word >> u) & 1
            bit_v = (word >> v) & 1
            if bit_u == bit_v:
                continue
            destination = orbit_ids[word ^ (1 << u) ^ (1 << v)]
            destinations[cursor] = destination
            coefficients[cursor] = -math.sqrt(sizes[source] / sizes[destination])
            orientation = bit_v - bit_u
            code = edge_code[edge_index]
            current_codes[cursor] = orientation * code
            cursor += 1
        if cursor != offsets[source + 1]:
            raise ValueError("transition row fill mismatch")
    return destinations, coefficients, current_codes


@njit
def h_apply(x, offsets, destinations, coefficients):
    out = np.zeros(x.size, np.complex128)
    for source in range(x.size):
        value = x[source]
        for cursor in range(offsets[source], offsets[source + 1]):
            out[destinations[cursor]] += coefficients[cursor] * value
    return out


@njit
def representative_currents(x, offsets, destinations, coefficients, current_codes, internal_edges, connector_edges):
    internal = 0.0j
    connector = 0.0j
    for source in range(x.size):
        value = x[source]
        for cursor in range(offsets[source], offsets[source + 1]):
            code = current_codes[cursor]
            sign = code if abs(code) == 1 else code // 2
            contribution = np.conjugate(x[destinations[cursor]]) * (1.0j * sign * coefficients[cursor]) * value
            if abs(code) == 1:
                internal += contribution
            else:
                connector += contribution
    return internal.real / internal_edges, connector.real / connector_edges


@njit
def diagonal_data(x, representatives, even_mask, edge_u, edge_v, edge_kind, length):
    even_total = 0.0
    odd_total = 0.0
    internal_both = 0.0
    connector_both = 0.0
    number_law = np.zeros(2 * length + 1, np.float64)
    for source in range(representatives.size):
        word = representatives[source]
        probability = x[source].real * x[source].real + x[source].imag * x[source].imag
        even_count = 0
        odd_count = 0
        particle_count = 0
        for site in range(2 * length):
            occupied = (word >> site) & 1
            particle_count += occupied
            if (even_mask >> site) & 1:
                even_count += occupied
            else:
                odd_count += occupied
        even_total += probability * even_count
        odd_total += probability * odd_count
        number_law[particle_count] += probability
        for edge_index in range(edge_u.size):
            both = ((word >> edge_u[edge_index]) & 1) * ((word >> edge_v[edge_index]) & 1)
            if edge_kind[edge_index] == 0:
                internal_both += probability * both
            else:
                connector_both += probability * both
    return (
        even_total / length,
        odd_total / length,
        internal_both / (2 * length),
        connector_both / length,
        number_law,
    )


def edges_for(length):
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append((layer * length + site, layer * length + (site + 1) % length, 0))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, 1))
    return edges


def prism_group(length):
    group = []
    for epsilon in (1, -1):
        for shift in range(length):
            swap = shift % 2
            permutation = []
            for layer in range(2):
                for site in range(length):
                    prism_site = (site - layer) % length
                    moved_layer = layer ^ swap
                    moved_prism = (epsilon * prism_site + shift) % length
                    moved_site = (moved_prism + moved_layer) % length
                    permutation.append(moved_layer * length + moved_site)
            group.append(tuple(permutation))
    return group


def chunk_tables(group, length):
    chunk_dimension = 1 << length
    low = np.zeros((len(group), chunk_dimension), np.uint32)
    high = np.zeros((len(group), chunk_dimension), np.uint32)
    for group_index, permutation in enumerate(group):
        for chunk in range(chunk_dimension):
            low_word = 0
            high_word = 0
            for bit in range(length):
                if (chunk >> bit) & 1:
                    low_word |= 1 << permutation[bit]
                    high_word |= 1 << permutation[length + bit]
            low[group_index, chunk] = low_word
            high[group_index, chunk] = high_word
    return low, high


def edge_reconstruction(edges, group):
    lookup = {frozenset((u, v)): (index, u, v) for index, (u, v, _) in enumerate(edges)}
    reconstruction = [None] * len(edges)
    representatives = []
    for edge_index, (u, v, _) in enumerate(edges):
        if reconstruction[edge_index] is not None:
            continue
        representative = len(representatives)
        representatives.append(edge_index)
        observed = {}
        for permutation in group:
            moved_u, moved_v = permutation[u], permutation[v]
            target, stored_u, stored_v = lookup[frozenset((moved_u, moved_v))]
            sign = 1 if (moved_u, moved_v) == (stored_u, stored_v) else -1
            if target in observed and observed[target] != sign:
                raise AssertionError("signed edge orbit contradiction")
            observed[target] = sign
        for target, sign in observed.items():
            reconstruction[target] = (representative, sign)
    if any(item is None for item in reconstruction):
        raise AssertionError("incomplete edge reconstruction")
    return representatives, reconstruction


def burnside_dimension(group):
    fixed_sum = 0
    for permutation in group:
        seen = set()
        cycles = 0
        for start in range(len(permutation)):
            if start in seen:
                continue
            cycles += 1
            cursor = start
            while cursor not in seen:
                seen.add(cursor)
                cursor = permutation[cursor]
        fixed_sum += 1 << cycles
    if fixed_sum % len(group):
        raise AssertionError("invalid Burnside sum")
    return fixed_sum // len(group)


def target_for(length):
    packet = json.loads(TARGETS[length].read_text())
    return next(row for row in packet["rows"] if row["kappa"] == KAPPA) if length == 4 else packet


def run(length):
    sites = 2 * length
    full_dimension = 1 << sites
    group = prism_group(length)
    edges = edges_for(length)
    edge_set = {frozenset((u, v)) for u, v, _ in edges}
    if len(set(group)) != 2 * length:
        raise AssertionError("group is not faithful")
    if any({frozenset((p[u], p[v])) for u, v, _ in edges} != edge_set for p in group):
        raise AssertionError("support not preserved")
    if any(p[site] % 2 != site % 2 for p in group for site in range(sites)):
        raise AssertionError("source parity not preserved")

    edge_representatives, reconstruction = edge_reconstruction(edges, group)
    if len(edge_representatives) != 2:
        raise AssertionError("unexpected signed edge orbit count")
    site_images = [{p[site] for p in group} for site in range(sites)]
    if any(site_images[site] != set(range(site % 2, sites, 2)) for site in range(sites)):
        raise AssertionError("parity site orbits are not transitive")

    orbit_dimension = burnside_dimension(group)
    low_table, high_table = chunk_tables(group, length)
    orbit_ids = np.full(full_dimension, -1, np.int32)
    representatives = np.empty(orbit_dimension, np.uint32)
    sizes = np.empty(orbit_dimension, np.uint8)
    observed_orbits = build_orbits(
        orbit_ids, representatives, sizes, low_table, high_table, (1 << length) - 1, length
    )
    if observed_orbits != orbit_dimension or np.any(orbit_ids < 0) or int(np.sum(sizes)) != full_dimension:
        raise AssertionError("orbit construction disagrees with Burnside count")
    del low_table, high_table

    edge_u = np.array([u for u, _, _ in edges], np.uint8)
    edge_v = np.array([v for _, v, _ in edges], np.uint8)
    edge_kind = np.array([kind for _, _, kind in edges], np.uint8)
    codes = np.array([(representative + 1) * sign for representative, sign in reconstruction], np.int8)
    offsets = count_transitions(representatives, edge_u, edge_v)
    destinations, coefficients, current_codes = fill_transitions(
        representatives, sizes, orbit_ids, offsets, edge_u, edge_v, codes
    )

    def H(x):
        return h_apply(x, offsets, destinations, coefficients)

    def currents(x):
        internal, connector = representative_currents(
            x, offsets, destinations, coefficients, current_codes, 2 * length, length
        )
        reps = (internal, connector)
        return np.array([sign * reps[representative] for representative, sign in reconstruction])

    even_mask = sum(1 << site for site in range(0, sites, 2))
    psi0 = np.zeros(orbit_dimension, np.complex128)
    valid = (representatives & even_mask) == 0
    # NumPy returns float16 for sqrt(uint8), which is not sufficient for the
    # normalized orbit amplitudes.  Promote explicitly while retaining the
    # byte-sized structural orbit-size array.
    psi0[valid] = np.sqrt(sizes[valid].astype(np.float64)) / math.sqrt(1 << length)
    psi = psi0.copy()
    integrated_currents = currents(psi)
    step = KAPPA / STEPS
    for index in range(1, STEPS + 1):
        out = psi.copy()
        term = psi.copy()
        for order in range(1, TAYLOR_ORDER + 1):
            term = (-1.0j * step / order) * H(term)
            out += term
        psi = out
        weight = 1.0 if index == STEPS else (4.0 if index % 2 else 2.0)
        integrated_currents += weight * currents(psi)
    integrated_currents *= step / 3.0

    q_even, q_odd, both_internal, both_connector, number_law = diagonal_data(
        psi, representatives, even_mask, edge_u, edge_v, edge_kind, length
    )
    q = np.array([q_even if site % 2 == 0 else q_odd for site in range(sites)])
    q0_even, q0_odd, _, _, number_law0 = diagonal_data(
        psi0, representatives, even_mask, edge_u, edge_v, edge_kind, length
    )
    q0 = np.array([q0_even if site % 2 == 0 else q0_odd for site in range(sites)])
    incidence = np.zeros((sites, len(edges)))
    for edge_index, (u, v, _) in enumerate(edges):
        incidence[u, edge_index] = 1.0
        incidence[v, edge_index] = -1.0
    residual = q - q0 + incidence @ integrated_currents
    correlations = np.array([
        both_internal - q[u] * q[v] if kind == 0 else both_connector - q[u] * q[v]
        for u, v, kind in edges
    ])
    target = target_for(length)
    target_q = np.array(target["q_after"])
    target_currents = np.array(target["integrated_oriented_currents"])
    hpsi0 = H(psi0)
    hpsi = H(psi)
    return {
        "L": length,
        "full_dimension": full_dimension,
        "orbit_dimension": orbit_dimension,
        "orbit_size_histogram": {str(key): value for key, value in sorted(Counter(sizes.tolist()).items())},
        "unaggregated_transition_entries": int(destinations.size),
        "transition_payload_bytes": int(offsets.nbytes + destinations.nbytes + coefficients.nbytes + current_codes.nbytes),
        "q_target_linf": float(np.max(np.abs(q - target_q))),
        "current_target_linf": float(np.max(np.abs(integrated_currents - target_currents))),
        "record_ledger_residual_l1": float(np.sum(np.abs(residual))),
        "record_ledger_residual_linf": float(np.max(np.abs(residual))),
        "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
        "energy_error": float(abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real)),
        "number_law_max_change": float(np.max(np.abs(number_law - number_law0))),
        "max_abs_connected_edge_correlation": float(np.max(np.abs(correlations))),
    }


rows = [run(length) for length in (4, 6, 8, 10)]
checks = []
for row in rows:
    length = row["L"]
    checks.extend([
        (row["orbit_dimension"] < row["full_dimension"], f"L{length} finite compression"),
        (row["unaggregated_transition_entries"] <= row["orbit_dimension"] * 3 * length, f"L{length} transition ceiling"),
        (row["q_target_linf"] < 4.0e-11, f"L{length} occupations"),
        (row["current_target_linf"] < 4.0e-11, f"L{length} currents"),
        (row["record_ledger_residual_l1"] < 8.0e-10, f"L{length} ledger L1"),
        (row["record_ledger_residual_linf"] < 8.0e-11, f"L{length} ledger Linf"),
        (row["norm_error"] < 8.0e-10, f"L{length} norm"),
        (row["energy_error"] < 8.0e-9, f"L{length} energy"),
        (row["number_law_max_change"] < 8.0e-10, f"L{length} number law"),
        (abs(row["max_abs_connected_edge_correlation"] - target_for(length)["max_abs_connected_edge_correlation"]) < 4.0e-11, f"L{length} correlations"),
    ])
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_CONNECTED_FIXED_WIDTH_ENGINE_V001",
    "classification": "EXACT_FINITE_ORBIT_PARTITION__UNAGGREGATED_OWNER_ONCE_TRANSITIONS__NUMERICAL_LOWER_SIZE_PARITY",
    "scope": "ENGINE_VALIDATION_ON_SEALED_L4_L6_L8_L10_RECORDS__NO_L14_EXECUTION",
    "parameters": {"kappa": KAPPA, "taylor_order": TAYLOR_ORDER, "steps": STEPS},
    "rows": rows,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "method_status": "CANDIDATE_ENGINE_ONLY__REQUIRES_HOSTILE_AUDIT_BEFORE_L14_USE",
    "not_claimed": "L14_EXECUTION__L14_ACCUMULATION__MONOTONICITY__CONVERGENCE__LIMIT__FIT__SCALING__COMPLEXITY_LAW__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5.0e-9:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    print(json.dumps(out, indent=2, sort_keys=True))
if failures:
    raise AssertionError(failures)
print(f"PASS__R_CONNECTED_FIXED_WIDTH_ENGINE__{len(checks)}/{len(checks)}")
