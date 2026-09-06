#!/usr/bin/env python3
"""Marked-source quotient response on the finite connected carrier component.

The source stabilizer has order two.  L6/L8 are numerical parity targets;
L10/L12 are eligible only after their fixed-width resource screen passes.
L14 can be screened without allocating its quotient.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import sys
import time
from collections import Counter, deque
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from numba import get_num_threads, njit, prange


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--length", type=int, choices=(6, 8, 10, 12, 14), required=True)
PARSER.add_argument("--screen-only", action="store_true")
ARGS = PARSER.parse_args()
LENGTH = ARGS.length
SITES = 2 * LENGTH
FULL_DIMENSION = 1 << SITES
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
SOURCE_SITE = 0
COARSE_STEPS = 1024 if LENGTH <= 10 else 512
FINE_STEPS = 2048 if LENGTH <= 10 else 1024
GUARD_BYTES = 40 * (1 << 30)
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = HERE / f"RESULT_L{LENGTH}.json"
BASELINES = {
    length: ROOT / f"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L{length}_ACCUMULATION_V001" / "RESULT.json"
    for length in (6, 8, 10, 12, 14)
}
BASELINE_HASHES = {
    6: "e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
    8: "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
    10: "06256f48fb39df0b5121ea01b38893ffeb84ba1bc7f842d22935ccd5279cdcbf",
    12: "154c9195b8ea516e4e637c1f4d66422ab82603163119f9b4451e7c2eb7ff5184",
    14: "e8134d5311b9bdfd62ce7df5988da803b110516606ce905a1bc49bd65cdb5fbe",
}
DIRECT = {
    6: HERE.parent / "DEVELOPMENT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001" / "RESULT_L6.json",
    8: HERE.parent / "DEVELOPMENT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001" / "RESULT_L8.json",
}
DIRECT_HASHES = {
    6: "8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a",
    8: "b73ba9e1c660a5285a075fd8c040c6b04621e4badc0dbecf42483d5c0a1c72fb",
}
STARTED = time.perf_counter()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_bytes() -> int:
    observed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(observed if sys.platform == "darwin" else observed * 1024)


def phase(label: str, extra=None) -> None:
    payload = {
        "phase": label,
        "elapsed_seconds": time.perf_counter() - STARTED,
        "max_rss_bytes": rss_bytes(),
    }
    if extra:
        payload.update(extra)
    print("PHASE__" + json.dumps(payload, sort_keys=True), flush=True)


def edges_for(length: int):
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append((layer * length + site, layer * length + (site + 1) % length, "internal"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def prism_group(length: int):
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


def source_stabilizer(length: int):
    return [permutation for permutation in prism_group(length) if permutation[SOURCE_SITE] == SOURCE_SITE]


def chunk_tables(group, length: int):
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


def cycle_count(permutation) -> int:
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
    return cycles


def burnside_dimension(group) -> int:
    fixed_sum = sum(1 << cycle_count(permutation) for permutation in group)
    if fixed_sum % len(group):
        raise AssertionError("invalid marked-source Burnside sum")
    return fixed_sum // len(group)


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
        raise AssertionError("incomplete signed edge reconstruction")
    return representatives, reconstruction


def resource_screen(orbit_dimension: int, edge_count: int, edge_orbit_count: int):
    transition_entries_upper = orbit_dimension * edge_count
    payload = {
        "orbit_ids_int32": 4 * FULL_DIMENSION,
        "orbit_representatives_uint32": 4 * orbit_dimension,
        "orbit_sizes_uint8": orbit_dimension,
        "csr_offsets_int64": 8 * (orbit_dimension + 1),
        "transition_destinations_int32_upper": 4 * transition_entries_upper,
        "transition_coefficients_float64_upper": 8 * transition_entries_upper,
        "transition_current_codes_int8_upper": transition_entries_upper,
        "six_two_history_complex128_vectors": 6 * orbit_dimension * 2 * 16,
        "current_reduction_blocks_float64": 8 * max(1, get_num_threads() * 8) * edge_orbit_count * 2,
    }
    total = sum(payload.values())
    return {
        "guard_bytes": GUARD_BYTES,
        "guard_gib": GUARD_BYTES / (1 << 30),
        "payload_bytes_by_array_upper": payload,
        "raw_numeric_payload_upper_bytes": total,
        "raw_numeric_payload_upper_gib": total / (1 << 30),
        "headroom_bytes": GUARD_BYTES - total,
        "passes_upper_bound_guard": total < GUARD_BYTES,
        "transition_entries_upper": transition_entries_upper,
        "status": "CONSERVATIVE_UNAGGREGATED_FIXED_WIDTH_UPPER_BOUND__NOT_PROCESS_RSS_OR_RUNTIME",
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
def count_unassigned(values):
    count = 0
    for value in values:
        if value < 0:
            count += 1
    return count


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
def fill_transitions(representatives, sizes, orbit_ids, offsets, edge_u, edge_v, edge_codes):
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
            current_codes[cursor] = orientation * edge_codes[edge_index]
            cursor += 1
        if cursor != offsets[source + 1]:
            raise ValueError("transition row fill mismatch")
    return destinations, coefficients, current_codes


@njit(parallel=True)
def h_apply_two_into(x, out, offsets, destinations, coefficients):
    for row in prange(x.shape[0]):
        value0 = 0.0j
        value1 = 0.0j
        for cursor in range(offsets[row], offsets[row + 1]):
            destination = destinations[cursor]
            coefficient = coefficients[cursor]
            value0 += coefficient * x[destination, 0]
            value1 += coefficient * x[destination, 1]
        out[row, 0] = value0
        out[row, 1] = value1


@njit
def h_apply_two_scatter(x, offsets, destinations, coefficients):
    out = np.zeros_like(x)
    for source in range(x.shape[0]):
        for cursor in range(offsets[source], offsets[source + 1]):
            destination = destinations[cursor]
            coefficient = coefficients[cursor]
            out[destination, 0] += coefficient * x[source, 0]
            out[destination, 1] += coefficient * x[source, 1]
    return out


@njit(parallel=True)
def current_partial_blocks(x, offsets, destinations, coefficients, current_codes, partial):
    block_count = partial.shape[0]
    edge_orbit_count = partial.shape[1]
    row_count = x.shape[0]
    for block in prange(block_count):
        for edge_orbit in range(edge_orbit_count):
            partial[block, edge_orbit, 0] = 0.0
            partial[block, edge_orbit, 1] = 0.0
        start = (block * row_count) // block_count
        stop = ((block + 1) * row_count) // block_count
        for source in range(start, stop):
            for cursor in range(offsets[source], offsets[source + 1]):
                code = current_codes[cursor]
                edge_orbit = abs(code) - 1
                sign = 1.0 if code > 0 else -1.0
                destination = destinations[cursor]
                coefficient = coefficients[cursor]
                for history in range(2):
                    contribution = (
                        np.conjugate(x[destination, history])
                        * (1.0j * sign * coefficient)
                        * x[source, history]
                    ).real
                    partial[block, edge_orbit, history] += contribution


@njit(parallel=True)
def occupations_two(x, representatives, inverse_sites):
    sites = inverse_sites.shape[1]
    group_order = inverse_sites.shape[0]
    out = np.zeros((2, sites), np.float64)
    for site in prange(sites):
        value0 = 0.0
        value1 = 0.0
        for orbit in range(representatives.size):
            word = representatives[orbit]
            average = 0.0
            for group_index in range(group_order):
                average += (word >> inverse_sites[group_index, site]) & 1
            average /= group_order
            probability0 = x[orbit, 0].real ** 2 + x[orbit, 0].imag ** 2
            probability1 = x[orbit, 1].real ** 2 + x[orbit, 1].imag ** 2
            value0 += probability0 * average
            value1 += probability1 * average
        out[0, site] = value0
        out[1, site] = value1
    return out


@njit
def number_laws_two(x, representatives, site_count):
    out = np.zeros((2, site_count + 1), np.float64)
    for orbit in range(representatives.size):
        word = representatives[orbit]
        count = 0
        cursor = word
        while cursor:
            count += cursor & 1
            cursor >>= 1
        for history in range(2):
            probability = x[orbit, history].real ** 2 + x[orbit, history].imag ** 2
            out[history, count] += probability
    return out


group = source_stabilizer(LENGTH)
edges = edges_for(LENGTH)
edge_set = {frozenset((u, v)) for u, v, _ in edges}
if len(group) != 2 or len(set(group)) != 2:
    raise AssertionError("marked-source stabilizer is not faithful order two")
if any(permutation[SOURCE_SITE] != SOURCE_SITE for permutation in group):
    raise AssertionError("source label is not fixed")
if any({frozenset((p[u], p[v])) for u, v, _ in edges} != edge_set for p in group):
    raise AssertionError("stabilizer does not preserve support")
if any(p[site] % 2 != site % 2 for p in group for site in range(SITES)):
    raise AssertionError("stabilizer does not preserve baseline source parity")
edge_representatives, reconstruction = edge_reconstruction(edges, group)
edge_orbit_sizes = np.bincount(
    np.array([representative for representative, _ in reconstruction]),
    minlength=len(edge_representatives),
).astype(np.float64)
orbit_dimension = burnside_dimension(group)
screen = resource_screen(orbit_dimension, len(edges), len(edge_representatives))
screen_checks = [
    (orbit_dimension == {6: 2176, 8: 33280, 10: 526336, 12: 8396800, 14: 134250496}[LENGTH], "marked-source orbit dimension"),
    (len(edges) == 3 * LENGTH, "owner-once edge census"),
    (len(edge_representatives) == {6: 10, 8: 13, 10: 16, 12: 19, 14: 22}[LENGTH], "signed edge orbit census"),
    (sum(edge_orbit_sizes) == len(edges), "edge reconstruction census"),
    (digest(BASELINES[LENGTH]) == BASELINE_HASHES[LENGTH], "sealed baseline hash"),
]
screen_failures = [label for passed, label in screen_checks if not passed]
screen_out = {
    "schema": f"R_GATE_AP_MARKED_SOURCE_RESOURCE_SCREEN_L{LENGTH}_V001",
    "classification": "EXACT_MARKED_SOURCE_STABILIZER_COUNT__CONSERVATIVE_FIXED_WIDTH_RESOURCE_UPPER_BOUND",
    "parameters": {"L": LENGTH, "source_site": SOURCE_SITE, "declared_host_capacity_gib": 48},
    "full_dimension": FULL_DIMENSION,
    "stabilizer_order": len(group),
    "orbit_dimension": orbit_dimension,
    "signed_edge_orbits": len(edge_representatives),
    "resource_upper_bound": screen,
    "decision": "ELIGIBLE_FOR_GUARDED_EXECUTION" if screen["passes_upper_bound_guard"] else "NOT_ELIGIBLE_UNDER_CURRENT_UNAGGREGATED_REPRESENTATION",
    "checks_passed": len(screen_checks) - len(screen_failures),
    "checks_total": len(screen_checks),
    "failures": screen_failures,
    "not_claimed": "PROCESS_RSS__RUNTIME__L14_RESPONSE__LOCALITY_OR_SCALING_LAW__PHYSICAL_DISTANCE_OR_BOUNDARY__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
}

if ARGS.screen_only:
    print("RESULT_JSON_BEGIN")
    print(json.dumps(screen_out, indent=2, sort_keys=True))
    print("RESULT_JSON_END")
    if screen_failures:
        raise AssertionError(screen_failures)
    print(f"PASS__R_GATE_AP_MARKED_SOURCE_RESOURCE_SCREEN_L{LENGTH}__{len(screen_checks)}/{len(screen_checks)}")
    raise SystemExit(0)

if not screen["passes_upper_bound_guard"]:
    raise MemoryError("current unaggregated representation fails the 40 GiB pre-allocation guard")
if screen_failures:
    raise AssertionError(screen_failures)

phase("RESOURCE_SCREEN_PASS", {"orbit_dimension": orbit_dimension, "upper_bound_gib": screen["raw_numeric_payload_upper_gib"]})
low_table, high_table = chunk_tables(group, LENGTH)
orbit_ids = np.full(FULL_DIMENSION, -1, np.int32)
representatives = np.empty(orbit_dimension, np.uint32)
sizes = np.empty(orbit_dimension, np.uint8)
observed_orbits = build_orbits(
    orbit_ids, representatives, sizes, low_table, high_table, (1 << LENGTH) - 1, LENGTH
)
if observed_orbits != orbit_dimension or count_unassigned(orbit_ids) != 0:
    raise AssertionError("compiled orbit partition differs from exact marked-source count")
unique_sizes, size_counts = np.unique(sizes, return_counts=True)
if int(np.dot(unique_sizes.astype(np.int64), size_counts)) != FULL_DIMENSION:
    raise AssertionError("orbit partition does not cover the full word space")
orbit_histogram = {str(int(key)): int(value) for key, value in zip(unique_sizes, size_counts)}
del low_table, high_table
phase("ORBIT_PARTITION_COMPLETE", {"orbit_histogram": orbit_histogram})

edge_u = np.array([u for u, _, _ in edges], np.uint8)
edge_v = np.array([v for _, v, _ in edges], np.uint8)
edge_codes = np.array(
    [(representative + 1) * sign for representative, sign in reconstruction], np.int8
)
offsets = count_transitions(representatives, edge_u, edge_v)
destinations, coefficients, current_codes = fill_transitions(
    representatives, sizes, orbit_ids, offsets, edge_u, edge_v, edge_codes
)
transition_payload_bytes = int(
    offsets.nbytes + destinations.nbytes + coefficients.nbytes + current_codes.nbytes
)
del orbit_ids
phase("TRANSITION_BUILD_COMPLETE", {"transition_entries": int(destinations.size), "transition_payload_bytes": transition_payload_bytes})

inverse_sites = np.empty((len(group), SITES), np.uint8)
for group_index, permutation in enumerate(group):
    for old_site, new_site in enumerate(permutation):
        inverse_sites[group_index, new_site] = old_site

even_mask = sum(1 << site for site in range(0, SITES, 2))
other_even_mask = even_mask ^ (1 << SOURCE_SITE)
initial = np.zeros((orbit_dimension, 2), np.complex128)
baseline_valid = (representatives & even_mask) == 0
perturbed_valid = (representatives & other_even_mask) == 0
size_roots = np.sqrt(sizes.astype(np.float64))
initial[baseline_valid, 0] = size_roots[baseline_valid] / math.sqrt(1 << LENGTH)
initial[perturbed_valid, 1] = size_roots[perturbed_valid] / math.sqrt(1 << (LENGTH + 1))
source_occupied = perturbed_valid & ((representatives & (1 << SOURCE_SITE)) != 0)
initial[source_occupied, 1] *= -1.0j
del size_roots, sizes

block_count = max(1, get_num_threads() * 8)
current_partial = np.empty((block_count, len(edge_representatives), 2), np.float64)


def currents(states):
    current_partial_blocks(
        states, offsets, destinations, coefficients, current_codes, current_partial
    )
    representative_values = np.sum(current_partial, axis=0) / edge_orbit_sizes[:, None]
    return np.array([
        sign * representative_values[representative]
        for representative, sign in reconstruction
    ]).T


def H(states):
    out = np.empty_like(states)
    h_apply_two_into(states, out, offsets, destinations, coefficients)
    return out


h_initial = H(initial)
probe = initial + 0.125j * h_initial
if LENGTH <= 8:
    gather_scatter_linf = float(np.max(np.abs(H(probe) - h_apply_two_scatter(probe, offsets, destinations, coefficients))))
else:
    gather_scatter_linf = None
initial_q = occupations_two(initial, representatives, inverse_sites)
initial_number_laws = number_laws_two(initial, representatives, SITES)
initial_norms = np.sum(np.abs(initial) ** 2, axis=0)
initial_energies = np.sum(np.conjugate(initial) * h_initial, axis=0)
initial_currents = currents(initial)
phase("STRUCTURAL_ACTION_COMPLETE", {"gather_scatter_linf": gather_scatter_linf, "numba_threads": get_num_threads()})


def evolve(step_count: int, label: str):
    step = KAPPA / step_count
    states = initial.copy()
    out = np.empty_like(states)
    term = np.empty_like(states)
    work = np.empty_like(states)
    integrated = currents(states)
    for index in range(1, step_count + 1):
        np.copyto(out, states)
        np.copyto(term, states)
        for order in range(1, TAYLOR_ORDER + 1):
            h_apply_two_into(term, work, offsets, destinations, coefficients)
            work *= -1.0j * step / order
            out += work
            term, work = work, term
        states, out = out, states
        weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
        integrated += weight * currents(states)
        if index % 128 == 0 or index == step_count:
            phase(f"{label}_PROGRESS", {"step": index, "steps": step_count})
    return states.copy(), integrated * step / 3.0


states_coarse, currents_coarse = evolve(COARSE_STEPS, "COARSE")
states, integrated_currents = evolve(FINE_STEPS, "FINE")
q_after_coarse = occupations_two(states_coarse, representatives, inverse_sites)
q_after = occupations_two(states, representatives, inverse_sites)
number_laws_after = number_laws_two(states, representatives, SITES)
h_final = H(states)
norms = np.sum(np.abs(states) ** 2, axis=0)
energies_final = np.sum(np.conjugate(states) * h_final, axis=0)

baseline = json.loads(BASELINES[LENGTH].read_text())
target_q = np.array(baseline["q_after"], dtype=float)
target_current = np.array(baseline["integrated_oriented_currents"], dtype=float)
baseline_q_linf = float(np.max(np.abs(q_after[0] - target_q)))
baseline_current_linf = float(np.max(np.abs(integrated_currents[0] - target_current)))
delta_q = q_after[1] - q_after[0]
delta_q_coarse = q_after_coarse[1] - q_after_coarse[0]
delta_current = integrated_currents[1] - integrated_currents[0]
delta_current_coarse = currents_coarse[1] - currents_coarse[0]

incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0
history_residual = q_after - initial_q + integrated_currents @ incidence.T
source_vector = np.zeros(SITES)
source_vector[SOURCE_SITE] = 0.5
full_differential_residual = delta_q + incidence @ delta_current - source_vector
full_differential_residual_coarse = delta_q_coarse + incidence @ delta_current_coarse - source_vector

neighbors = [set() for _ in range(SITES)]
for u, v, _ in edges:
    neighbors[u].add(v)
    neighbors[v].add(u)
distances = [None] * SITES
distances[SOURCE_SITE] = 0
queue = deque([SOURCE_SITE])
while queue:
    u = queue.popleft()
    for v in neighbors[u]:
        if distances[v] is None:
            distances[v] = distances[u] + 1
            queue.append(v)

shells = []
for radius in sorted(set(min(distances[u], distances[v]) for u, v, _ in edges)):
    for kind in ("internal", "connector"):
        indices = [
            index for index, (u, v, edge_kind) in enumerate(edges)
            if edge_kind == kind and min(distances[u], distances[v]) == radius
        ]
        if not indices:
            continue
        values = delta_current[indices]
        shells.append({
            "r": radius,
            "kind": kind,
            "edge_count": len(indices),
            "edge_indices": indices,
            "signed_sum_delta_J": float(np.sum(values)),
            "l1_sum_abs_delta_J": float(np.sum(np.abs(values))),
            "mean_abs_delta_J": float(np.mean(np.abs(values))),
            "max_abs_delta_J": float(np.max(np.abs(values))),
        })

kinds = np.array([kind for _, _, kind in edges])
connector = kinds == "connector"
profile_l1 = float(np.sum(np.abs(delta_current)))
profile_weighted_radius = float(
    sum(min(distances[u], distances[v]) * abs(delta_current[index]) for index, (u, v, _) in enumerate(edges))
    / profile_l1
) if profile_l1 else 0.0
effective_edges = float(profile_l1 ** 2 / np.sum(delta_current ** 2)) if np.any(delta_current) else 0.0

direct_controls = None
if LENGTH in DIRECT:
    direct = json.loads(DIRECT[LENGTH].read_text())
    direct_q = np.array([row["perturbed_q_after"] for row in direct["site_records"]])
    direct_current = np.array([row["perturbed_J"] for row in direct["edge_records"]])
    direct_delta_q = np.array([row["delta_q_after"] for row in direct["site_records"]])
    direct_delta_current = np.array([row["delta_J"] for row in direct["edge_records"]])
    direct_controls = {
        "sha256": digest(DIRECT[LENGTH]),
        "perturbed_q_linf": float(np.max(np.abs(q_after[1] - direct_q))),
        "perturbed_current_linf": float(np.max(np.abs(integrated_currents[1] - direct_current))),
        "delta_q_linf": float(np.max(np.abs(delta_q - direct_delta_q))),
        "delta_current_linf": float(np.max(np.abs(delta_current - direct_delta_current))),
    }

checks = list(screen_checks)
checks.extend([
    (screen["passes_upper_bound_guard"], "fixed-width resource upper-bound guard"),
    (observed_orbits == orbit_dimension, "compiled orbit count"),
    (int(destinations.size) <= screen["transition_entries_upper"], "transition entry ceiling"),
    (abs(initial_norms[0] - 1.0) < 2e-11 and abs(initial_norms[1] - 1.0) < 2e-11, "initial norms"),
    (float(np.max(np.abs(initial_currents[0]))) < 2e-11, "terms-restored baseline initial current zero"),
    (np.all(np.isfinite(initial_currents[1])), "terms-restored perturbed initial current finite"),
    (abs(initial_q[1, SOURCE_SITE] - initial_q[0, SOURCE_SITE] - 0.5) < 2e-11, "authenticated source amount"),
    (abs(float(np.sum(initial_q[1] - initial_q[0])) - 0.5) < 2e-10, "initial global source amount"),
    (baseline_q_linf < (4e-8 if LENGTH >= 12 else 4e-10), "sealed baseline occupation reproduction"),
    (baseline_current_linf < (4e-8 if LENGTH >= 12 else 4e-10), "sealed baseline current reproduction"),
    (float(np.max(np.abs(states - states_coarse))) < 4e-8, "state refinement"),
    (float(np.max(np.abs(q_after - q_after_coarse))) < 4e-8, "occupation refinement"),
    (float(np.max(np.abs(integrated_currents - currents_coarse))) < 4e-8, "current refinement"),
    (float(np.sum(np.abs(history_residual[0]))) < 2e-8, "baseline transport ledger"),
    (float(np.sum(np.abs(history_residual[1]))) < 2e-8, "perturbed transport ledger"),
    (float(np.sum(np.abs(full_differential_residual))) < 3e-8, "full differential ledger"),
    (abs(float(np.sum(delta_q)) - 0.5) < 2e-8, "terminal global source retention"),
    (float(np.max(np.abs(norms - 1.0))) < 2e-8, "terminal norms"),
    (float(np.max(np.abs(energies_final.real - initial_energies.real))) < 2e-7, "energy conservation"),
    (float(np.max(np.abs(energies_final.imag))) < 2e-8, "energy reality"),
    (float(np.max(np.abs(number_laws_after - initial_number_laws))) < 2e-8, "number-law conservation"),
    (len({index for shell in shells for index in shell["edge_indices"]}) == len(edges), "radial shell partition"),
    (profile_l1 > 1e-8, "nonzero current response"),
    (np.all(np.isfinite(delta_current)) and np.all(np.isfinite(delta_q)), "finite response record"),
])
if gather_scatter_linf is not None:
    checks.append((gather_scatter_linf < 2e-11, "quotient gather/scatter crosscheck"))
if direct_controls is not None:
    checks.extend([
        (direct_controls["sha256"] == DIRECT_HASHES[LENGTH], "direct response hash"),
        (direct_controls["perturbed_q_linf"] < 4e-10, "direct perturbed occupation parity"),
        (direct_controls["perturbed_current_linf"] < 4e-10, "direct perturbed current parity"),
        (direct_controls["delta_q_linf"] < 4e-10, "direct differential occupation parity"),
        (direct_controls["delta_current_linf"] < 4e-10, "direct differential current parity"),
    ])
failures = [label for passed, label in checks if not passed]

out = {
    "schema": f"R_GATE_AP_MARKED_SOURCE_RESPONSE_L{LENGTH}_V001",
    "classification": "FINITE_ORDER_TWO_MARKED_SOURCE_QUOTIENT__TWO_HISTORY_BASELINE_AND_AUTHENTICATED_W_R_HALF_RESPONSE",
    "scope": "FINITE_SUPPORT_GRAPH_PROFILE__NO_PHYSICAL_DISTANCE_OR_CONTINUUM_INFERENCE",
    "sealed_inputs_sha256": {
        BASELINES[LENGTH].relative_to(ROOT).as_posix(): digest(BASELINES[LENGTH]),
        **({DIRECT[LENGTH].relative_to(ROOT).as_posix(): digest(DIRECT[LENGTH])} if LENGTH in DIRECT else {}),
    },
    "parameters": {
        "L": LENGTH,
        "sites_per_component": SITES,
        "source_site": SOURCE_SITE,
        "W_R": 0.5,
        "r0": "14441248/6075",
        "phi": "pi/4",
        "kappa": KAPPA,
        "taylor_order": TAYLOR_ORDER,
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
    },
    "resource_screen": screen_out,
    "finite_marked_source_basis": {
        "full_dimension": FULL_DIMENSION,
        "stabilizer_order": len(group),
        "orbit_dimension": orbit_dimension,
        "orbit_size_histogram": orbit_histogram,
        "signed_edge_orbits": len(edge_representatives),
        "unaggregated_transition_entries": int(destinations.size),
        "transition_payload_bytes": transition_payload_bytes,
        "numba_threads": get_num_threads(),
    },
    "source_write_ledger": "DELTA_Q_PLUS_EDGE_FLUX_MINUS_W_R_EQUALS_ONE_HALF_PLUS_ZERO_MINUS_ONE_HALF_EQUALS_ZERO",
    "edge_records": [
        {
            "edge_index": index,
            "u": u,
            "v": v,
            "kind": kind,
            "r": min(distances[u], distances[v]),
            "baseline_J": float(integrated_currents[0, index]),
            "perturbed_J": float(integrated_currents[1, index]),
            "delta_J": float(delta_current[index]),
        }
        for index, (u, v, kind) in enumerate(edges)
    ],
    "site_records": [
        {
            "site": site,
            "r": distances[site],
            "baseline_q_before": float(initial_q[0, site]),
            "perturbed_q_before": float(initial_q[1, site]),
            "baseline_q_after": float(q_after[0, site]),
            "perturbed_q_after": float(q_after[1, site]),
            "delta_q_after": float(delta_q[site]),
        }
        for site in range(SITES)
    ],
    "radial_edge_profile": shells,
    "response_summary": {
        "delta_q_terminal_sum": float(np.sum(delta_q)),
        "delta_J_l1": profile_l1,
        "delta_J_linf": float(np.max(np.abs(delta_current))),
        "total_absolute_throughput_change": float(np.sum(np.abs(integrated_currents[1])) - np.sum(np.abs(integrated_currents[0]))),
        "connector_absolute_throughput_change": float(np.sum(np.abs(integrated_currents[1, connector])) - np.sum(np.abs(integrated_currents[0, connector]))),
        "mean_edge_radius_abs_delta_J": profile_weighted_radius,
        "effective_responding_edge_count": effective_edges,
        "max_site_graph_distance": max(distances),
        "profile_classification": "RAW_FINITE_SUPPORT_PROFILE__FULL_REQUESTED_LADDER_CLASSIFICATION_REQUIRES_AVAILABLE_AUDITED_ROWS",
    },
    "numerical_controls": {
        "baseline_q_reproduction_linf": baseline_q_linf,
        "baseline_current_reproduction_linf": baseline_current_linf,
        "state_refinement_linf": float(np.max(np.abs(states - states_coarse))),
        "occupation_refinement_linf": float(np.max(np.abs(q_after - q_after_coarse))),
        "current_refinement_linf": float(np.max(np.abs(integrated_currents - currents_coarse))),
        "differential_occupation_refinement_linf": float(np.max(np.abs(delta_q - delta_q_coarse))),
        "differential_current_refinement_linf": float(np.max(np.abs(delta_current - delta_current_coarse))),
        "baseline_transport_residual_l1": float(np.sum(np.abs(history_residual[0]))),
        "perturbed_transport_residual_l1": float(np.sum(np.abs(history_residual[1]))),
        "full_differential_residual_l1": float(np.sum(np.abs(full_differential_residual))),
        "full_differential_residual_linf": float(np.max(np.abs(full_differential_residual))),
        "coarse_full_differential_residual_l1": float(np.sum(np.abs(full_differential_residual_coarse))),
        "norm_error_max": float(np.max(np.abs(norms - 1.0))),
        "energy_error_max": float(np.max(np.abs(energies_final.real - initial_energies.real))),
        "energy_imag_abs_max": float(np.max(np.abs(energies_final.imag))),
        "number_law_max_change": float(np.max(np.abs(number_laws_after - initial_number_laws))),
        "gather_scatter_linf": gather_scatter_linf,
        "direct_full_space_parity": direct_controls,
        "terms_restored_initial_current_linf": [
            float(np.max(np.abs(initial_currents[history]))) for history in range(2)
        ],
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_DIFFERENTIAL_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "profile_status": "FINITE_SUPPORT_GRAPH_DISTANCE_ONLY__NOT_PHYSICAL_RADIUS_OR_GRID",
    "claim_classes": {
        "proved": "AUTHENTICATED_SOURCE_WRITE_LEDGER__FINITE_OWNER_INCIDENCE_AND_PROFILE_PARTITIONS__EXACT_MARKED_SOURCE_ORBIT_COUNT",
        "adopted": "F3_MDC_ALPHA_EQUALS_R0__CANONICAL_SOURCE_LABEL",
        "conditional": "SUPPORT__KAPPA__CONTENT__ROUTING__READ__NUMERICAL_REPRESENTATION",
        "empirical": f"FINITE_REFINED_L{LENGTH}_DIFFERENTIAL_OCCUPATION_CURRENT_AND_RADIAL_PROFILE",
        "open": "INDEPENDENT_HOSTILE_AUDIT__UNAVAILABLE_LADDER_ROWS__FULL_LADDER_PROFILE_CLASSIFICATION__PHYSICAL_DISTANCE__GATE_A_P",
    },
    "not_claimed": "LOCALITY_OR_SCALING_LAW__UNIFORM_OR_ASYMPTOTIC_PROFILE__PHYSICAL_BOUNDARY_REFLECTION__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5e-9:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    print("RESULT_JSON_BEGIN")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("RESULT_JSON_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_GATE_AP_MARKED_SOURCE_RESPONSE_L{LENGTH}__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={rss_bytes()}")
