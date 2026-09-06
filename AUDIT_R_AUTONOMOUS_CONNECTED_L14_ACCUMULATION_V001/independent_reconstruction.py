#!/usr/bin/env python3
"""Independent guarded L14 reconstruction: generator BFS, aggregated CSR, RK4."""

from __future__ import annotations

import gc
import hashlib
import json
import math
import os
import resource
import sys
import time
from collections import Counter
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np
from numba import get_num_threads, njit, prange


L = 14
N = 2 * L
D = 1 << N
M_EXPECTED = 9_608_050
COMPONENTS = L * L // 2
KAPPA = math.pi / 2.0
COARSE_STEPS = 1024
FINE_STEPS = 2048
GUARD_BYTES = 40 * (1 << 30)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_DIR = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001"
OUT = HERE / "INDEPENDENT_RESULT.json"
STARTED = time.perf_counter()


def rss_bytes() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == "darwin" else value * 1024)


def phase(label: str, **fields) -> None:
    row = {
        "phase": label,
        "elapsed_seconds": time.perf_counter() - STARTED,
        "max_rss_bytes": rss_bytes(),
    }
    row.update(fields)
    print("AUDIT_PHASE__" + json.dumps(row, sort_keys=True), flush=True)


def guard(label: str, live_bytes: int, requested_bytes: int) -> None:
    if live_bytes + requested_bytes >= GUARD_BYTES:
        raise MemoryError(f"{label}: declared live allocation reaches 40 GiB guard")
    if rss_bytes() >= GUARD_BYTES:
        raise MemoryError(f"{label}: observed RSS reaches 40 GiB guard")


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def generators(length: int):
    """Two prism-coordinate generators, derived without target imports."""
    rotation = []
    reflection = []
    for layer in range(2):
        for displayed in range(length):
            prism = (displayed - layer) % length
            moved_layer = layer ^ 1
            rotation.append(
                moved_layer * length + (prism + 1 + moved_layer) % length
            )
            reflection.append(layer * length + (-prism + layer) % length)
    return tuple(rotation), tuple(reflection)


def generated_group(length: int):
    gens = generators(length)
    identity = tuple(range(2 * length))
    group = {identity}
    todo = [identity]
    while todo:
        current = todo.pop()
        for generator in gens:
            image = compose(generator, current)
            if image not in group:
                group.add(image)
                todo.append(image)
    return sorted(group)


def edges_for(length: int):
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append(
                (layer * length + site, layer * length + (site + 1) % length, 0)
            )
    for site in range(length):
        edges.append((site, length + (site + 1) % length, 1))
    return edges


def signed_edge_action(edges, group):
    oriented = [(u, v) for u, v, _ in edges]
    lookup = {edge: (index, 1) for index, edge in enumerate(oriented)}
    lookup.update({(v, u): (index, -1) for index, (u, v) in enumerate(oriented)})
    mapping = {}
    representatives = []
    for seed, (u, v) in enumerate(oriented):
        if seed in mapping:
            continue
        orbit_index = len(representatives)
        representatives.append(seed)
        for permutation in group:
            target, sign = lookup[(permutation[u], permutation[v])]
            previous = mapping.get(target)
            if previous is not None and previous != (orbit_index, sign):
                raise AssertionError("signed edge action is inconsistent")
            mapping[target] = (orbit_index, sign)
    if len(mapping) != len(edges) or len(representatives) != 2:
        raise AssertionError("signed edge action does not have two complete orbits")
    return representatives, [mapping[i] for i in range(len(edges))]


def generator_tables(length: int):
    gens = generators(length)
    chunk = 1 << length
    low = np.empty((2, chunk), np.uint32)
    high = np.empty((2, chunk), np.uint32)
    for generator_index, permutation in enumerate(gens):
        for word in range(chunk):
            low_image = 0
            high_image = 0
            for bit in range(length):
                if (word >> bit) & 1:
                    low_image |= 1 << permutation[bit]
                    high_image |= 1 << permutation[length + bit]
            low[generator_index, word] = low_image
            high[generator_index, word] = high_image
    return low, high


@njit
def build_orbits_generator_bfs(dimension, expected, low, high, shift):
    orbit_id = np.full(dimension, -1, np.int32)
    representatives = np.empty(expected, np.uint32)
    sizes = np.empty(expected, np.uint8)
    queue = np.empty(2 * shift, np.uint32)
    mask = (1 << shift) - 1
    orbit_count = 0
    for seed in range(dimension):
        if orbit_id[seed] >= 0:
            continue
        if orbit_count >= expected:
            raise ValueError("more generator orbits than expected")
        representatives[orbit_count] = seed
        orbit_id[seed] = orbit_count
        queue[0] = seed
        used = 1
        cursor = 0
        while cursor < used:
            word = queue[cursor]
            cursor += 1
            lower = word & mask
            upper = word >> shift
            for generator_index in range(2):
                image = low[generator_index, lower] | high[generator_index, upper]
                previous = orbit_id[image]
                if previous < 0:
                    if used >= 2 * shift:
                        raise ValueError("generator orbit exceeds finite group order")
                    orbit_id[image] = orbit_count
                    queue[used] = image
                    used += 1
                elif previous != orbit_count:
                    raise ValueError("generator orbit collision")
        sizes[orbit_count] = used
        orbit_count += 1
    return orbit_id, representatives[:orbit_count], sizes[:orbit_count]


@njit
def row_distinct_counts(representatives, orbit_id, edge_u, edge_v):
    counts = np.empty(representatives.size, np.uint8)
    table = np.empty(64, np.int32)
    touched = np.empty(42, np.uint8)
    for slot in range(64):
        table[slot] = -1
    for row in range(representatives.size):
        word = representatives[row]
        touched_count = 0
        distinct = 0
        for edge in range(edge_u.size):
            u = edge_u[edge]
            v = edge_v[edge]
            if ((word >> u) & 1) == ((word >> v) & 1):
                continue
            destination = orbit_id[word ^ (1 << u) ^ (1 << v)]
            slot = (destination * 13) & 63
            while table[slot] >= 0 and table[slot] != destination:
                slot = (slot + 1) & 63
            if table[slot] < 0:
                table[slot] = destination
                touched[touched_count] = slot
                touched_count += 1
                distinct += 1
        counts[row] = distinct
        for index in range(touched_count):
            table[touched[index]] = -1
    return counts


@njit
def prefix_offsets(counts):
    offsets = np.empty(counts.size + 1, np.int64)
    offsets[0] = 0
    for row in range(counts.size):
        offsets[row + 1] = offsets[row] + counts[row]
    return offsets


@njit
def fill_aggregated_rows(
    representatives,
    sizes,
    orbit_id,
    offsets,
    edge_u,
    edge_v,
    edge_orbit,
    edge_sign,
):
    entries = offsets[-1]
    destinations = np.empty(entries, np.uint32)
    coefficients = np.empty(entries, np.float64)
    multiplicities = np.empty(entries, np.uint8)
    internal_signed = np.empty(entries, np.int8)
    connector_signed = np.empty(entries, np.int8)
    table = np.empty(64, np.int32)
    touched = np.empty(42, np.uint8)
    local_dest = np.empty(42, np.int32)
    multiplicity = np.empty(42, np.int8)
    local_internal = np.empty(42, np.int8)
    local_connector = np.empty(42, np.int8)
    for slot in range(64):
        table[slot] = -1
    for row in range(representatives.size):
        word = representatives[row]
        used = 0
        for edge in range(edge_u.size):
            u = edge_u[edge]
            v = edge_v[edge]
            bit_u = (word >> u) & 1
            bit_v = (word >> v) & 1
            if bit_u == bit_v:
                continue
            destination = orbit_id[word ^ (1 << u) ^ (1 << v)]
            slot = (destination * 13) & 63
            while table[slot] >= 0 and local_dest[table[slot]] != destination:
                slot = (slot + 1) & 63
            orientation = bit_v - bit_u
            signed = orientation * edge_sign[edge]
            if table[slot] < 0:
                table[slot] = used
                touched[used] = slot
                local_dest[used] = destination
                multiplicity[used] = 1
                local_internal[used] = signed if edge_orbit[edge] == 0 else 0
                local_connector[used] = signed if edge_orbit[edge] == 1 else 0
                used += 1
            else:
                local = table[slot]
                multiplicity[local] += 1
                if edge_orbit[edge] == 0:
                    local_internal[local] += signed
                else:
                    local_connector[local] += signed
        if used != offsets[row + 1] - offsets[row]:
            raise ValueError("aggregated row count mismatch")
        start = offsets[row]
        for local in range(used):
            destination = local_dest[local]
            destinations[start + local] = destination
            base = -math.sqrt(sizes[row] / sizes[destination])
            coefficients[start + local] = base * multiplicity[local]
            multiplicities[start + local] = multiplicity[local]
            internal_signed[start + local] = local_internal[local]
            connector_signed[start + local] = local_connector[local]
        for index in range(used):
            table[touched[index]] = -1
    return destinations, coefficients, multiplicities, internal_signed, connector_signed


@njit(parallel=True)
def h_into(state, out, offsets, destinations, coefficients):
    for row in prange(state.size):
        total = 0.0j
        for cursor in range(offsets[row], offsets[row + 1]):
            total += coefficients[cursor] * state[destinations[cursor]]
        out[row] = total


@njit(parallel=True)
def derivative_into(state, out, offsets, destinations, coefficients):
    for row in prange(state.size):
        total = 0.0j
        for cursor in range(offsets[row], offsets[row + 1]):
            total += coefficients[cursor] * state[destinations[cursor]]
        out[row] = -1.0j * total


@njit(parallel=True)
def set_shifted(out, state, derivative, factor):
    for index in prange(state.size):
        out[index] = state[index] + factor * derivative[index]


@njit(parallel=True)
def accumulate_rk(accumulator, derivative):
    for index in prange(accumulator.size):
        accumulator[index] += 2.0 * derivative[index]


@njit(parallel=True)
def finish_rk(state, accumulator, derivative, factor):
    for index in prange(state.size):
        state[index] += factor * (accumulator[index] + derivative[index])


@njit(parallel=True)
def current_rows(
    state,
    offsets,
    destinations,
    coefficients,
    multiplicities,
    internal_signed,
    connector_signed,
    internal_rows,
    connector_rows,
):
    for row in prange(state.size):
        source = state[row]
        total_internal = 0.0
        total_connector = 0.0
        for cursor in range(offsets[row], offsets[row + 1]):
            base = coefficients[cursor] / multiplicities[cursor]
            target = state[destinations[cursor]]
            bilinear = target.imag * source.real - target.real * source.imag
            total_internal += base * internal_signed[cursor] * bilinear
            total_connector += base * connector_signed[cursor] * bilinear
        internal_rows[row] = total_internal
        connector_rows[row] = total_connector


@njit
def diagonal_summary(state, representatives, length, edge_u, edge_v, edge_kind):
    even_total = 0.0
    odd_total = 0.0
    internal_both = 0.0
    connector_both = 0.0
    number_law = np.zeros(2 * length + 1, np.float64)
    for row in range(state.size):
        word = representatives[row]
        probability = state[row].real ** 2 + state[row].imag ** 2
        even = 0
        odd = 0
        for site in range(2 * length):
            occupied = (word >> site) & 1
            if site % 2 == 0:
                even += occupied
            else:
                odd += occupied
        even_total += probability * even
        odd_total += probability * odd
        number_law[even + odd] += probability
        for edge in range(edge_u.size):
            both = ((word >> edge_u[edge]) & 1) * ((word >> edge_v[edge]) & 1)
            if edge_kind[edge] == 0:
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


def make_csr(length, expected):
    dimension = 1 << (2 * length)
    group = generated_group(length)
    edges = edges_for(length)
    edge_representatives, reconstruction = signed_edge_action(edges, group)
    low, high = generator_tables(length)
    orbit_id, representatives, sizes = build_orbits_generator_bfs(
        dimension, expected, low, high, length
    )
    del low, high
    edge_u = np.array([u for u, _, _ in edges], np.uint8)
    edge_v = np.array([v for _, v, _ in edges], np.uint8)
    edge_kind = np.array([kind for _, _, kind in edges], np.uint8)
    edge_orbit = np.array([item[0] for item in reconstruction], np.uint8)
    edge_sign = np.array([item[1] for item in reconstruction], np.int8)
    counts = row_distinct_counts(representatives, orbit_id, edge_u, edge_v)
    offsets = prefix_offsets(counts)
    del counts
    destinations, coefficients, multiplicities, internal_signed, connector_signed = fill_aggregated_rows(
        representatives,
        sizes,
        orbit_id,
        offsets,
        edge_u,
        edge_v,
        edge_orbit,
        edge_sign,
    )
    return {
        "group": group,
        "edges": edges,
        "edge_representatives": edge_representatives,
        "reconstruction": reconstruction,
        "orbit_id": orbit_id,
        "representatives": representatives,
        "sizes": sizes,
        "edge_u": edge_u,
        "edge_v": edge_v,
        "edge_kind": edge_kind,
        "offsets": offsets,
        "destinations": destinations,
        "coefficients": coefficients,
        "multiplicities": multiplicities,
        "internal_signed": internal_signed,
        "connector_signed": connector_signed,
    }


def quotient_currents(state, data, internal_rows, connector_rows):
    current_rows(
        state,
        data["offsets"],
        data["destinations"],
        data["coefficients"],
        data["multiplicities"],
        data["internal_signed"],
        data["connector_signed"],
        internal_rows,
        connector_rows,
    )
    pair = (float(np.sum(internal_rows)) / (2 * L), float(np.sum(connector_rows)) / L)
    return np.array([sign * pair[orbit] for orbit, sign in data["reconstruction"]])


def validate_l4_full_space():
    length = 4
    data = make_csr(length, 55)
    orbit_id = data["orbit_id"]
    reps = data["representatives"]
    sizes = data["sizes"]
    rng = np.random.default_rng(1404)
    state = rng.normal(size=reps.size) + 1.0j * rng.normal(size=reps.size)
    state /= np.linalg.norm(state)
    quotient_h = np.empty_like(state)
    h_into(state, quotient_h, data["offsets"], data["destinations"], data["coefficients"])
    full = state[orbit_id] / np.sqrt(sizes[orbit_id].astype(np.float64))
    full_h = np.zeros_like(full)
    for word in range(1 << (2 * length)):
        for u, v, _ in data["edges"]:
            if ((word >> u) & 1) != ((word >> v) & 1):
                full_h[word] -= full[word ^ (1 << u) ^ (1 << v)]
    expanded_h = quotient_h[orbit_id] / np.sqrt(sizes[orbit_id].astype(np.float64))
    action_linf = float(np.max(np.abs(full_h - expanded_h)))

    direct_currents = []
    for u, v, _ in data["edges"]:
        value = 0.0
        for word in range(1 << (2 * length)):
            bit_u = (word >> u) & 1
            bit_v = (word >> v) & 1
            if bit_u != bit_v:
                swapped = word ^ (1 << u) ^ (1 << v)
                value += (
                    np.conjugate(full[swapped])
                    * (1.0j * (bit_v - bit_u) * -1.0)
                    * full[word]
                ).real
        direct_currents.append(value)
    rows0 = np.empty(state.size, np.float64)
    rows1 = np.empty(state.size, np.float64)
    # quotient_currents uses the global L divisor, so calculate the L4
    # representative reductions explicitly here.
    current_rows(
        state,
        data["offsets"],
        data["destinations"],
        data["coefficients"],
        data["multiplicities"],
        data["internal_signed"],
        data["connector_signed"],
        rows0,
        rows1,
    )
    pair = (float(np.sum(rows0)) / (2 * length), float(np.sum(rows1)) / length)
    quotient_j = np.array(
        [sign * pair[orbit] for orbit, sign in data["reconstruction"]]
    )
    current_linf = float(np.max(np.abs(quotient_j - np.array(direct_currents))))

    q_direct = []
    probability = np.abs(full) ** 2
    words = np.arange(1 << (2 * length), dtype=np.uint32)
    for site in range(2 * length):
        q_direct.append(float(np.sum(probability[((words >> site) & 1) == 1])))
    q_even, q_odd, both_internal, both_connector, _ = diagonal_summary(
        state,
        reps,
        length,
        data["edge_u"],
        data["edge_v"],
        data["edge_kind"],
    )
    q_quotient = np.array([q_even if site % 2 == 0 else q_odd for site in range(8)])
    q_linf = float(np.max(np.abs(q_quotient - np.array(q_direct))))
    result = {
        "orbit_dimension": int(reps.size),
        "aggregated_entries": int(data["destinations"].size),
        "full_space_action_linf": action_linf,
        "full_space_current_linf": current_linf,
        "full_space_diagonal_linf": q_linf,
        "representative_both_internal": float(both_internal),
        "representative_both_connector": float(both_connector),
    }
    if action_linf >= 2e-14 or current_linf >= 2e-14 or q_linf >= 2e-14:
        raise AssertionError(f"L4 full-space validation failed: {result}")
    return result


def evolve(initial, data, steps, label, current_internal_rows, current_connector_rows):
    dt = KAPPA / steps
    state = initial.copy()
    temporary = np.empty_like(state)
    accumulator = np.empty_like(state)
    derivative = np.empty_like(state)
    integrated = quotient_currents(
        state, data, current_internal_rows, current_connector_rows
    )
    for step in range(1, steps + 1):
        derivative_into(
            state,
            accumulator,
            data["offsets"],
            data["destinations"],
            data["coefficients"],
        )
        set_shifted(temporary, state, accumulator, dt / 2.0)
        derivative_into(
            temporary,
            derivative,
            data["offsets"],
            data["destinations"],
            data["coefficients"],
        )
        accumulate_rk(accumulator, derivative)
        set_shifted(temporary, state, derivative, dt / 2.0)
        derivative_into(
            temporary,
            derivative,
            data["offsets"],
            data["destinations"],
            data["coefficients"],
        )
        accumulate_rk(accumulator, derivative)
        set_shifted(temporary, state, derivative, dt)
        derivative_into(
            temporary,
            derivative,
            data["offsets"],
            data["destinations"],
            data["coefficients"],
        )
        finish_rk(state, accumulator, derivative, dt / 6.0)
        weight = 1.0 if step == steps else (4.0 if step % 2 else 2.0)
        integrated += weight * quotient_currents(
            state, data, current_internal_rows, current_connector_rows
        )
        if step % 64 == 0 or step == steps:
            phase(f"{label}_PROGRESS", step=step, steps=steps)
        if rss_bytes() >= GUARD_BYTES:
            raise MemoryError(f"{label}: observed RSS reaches 40 GiB guard")
    return state, integrated * dt / 3.0


phase("AUDIT_START", numba_threads=get_num_threads(), guard_bytes=GUARD_BYTES)
l4_validation = validate_l4_full_space()
phase("L4_FULL_SPACE_VALIDATION_PASS", **l4_validation)
if os.environ.get("AUDIT_L4_ONLY") == "1":
    print("PASS__HOSTILE_L14_REMEDY_L4_FULL_SPACE_ONLY", flush=True)
    raise SystemExit(0)

group = generated_group(L)
edges = edges_for(L)
edge_set = {frozenset((u, v)) for u, v, _ in edges}
if len(group) != 28 or any(
    {frozenset((p[u], p[v])) for u, v, _ in edges} != edge_set for p in group
):
    raise AssertionError("independent finite group does not preserve L14 support")
if any(p[site] % 2 != site % 2 for p in group for site in range(N)):
    raise AssertionError("independent finite group does not preserve source parity")

base_live = 4 * D + M_EXPECTED * (4 + 1)
guard("orbit builder", 0, base_live)
data = make_csr(L, M_EXPECTED)
if data["representatives"].size != M_EXPECTED or np.any(data["orbit_id"] < 0):
    raise AssertionError("L14 generator-BFS orbit partition incomplete")
histogram = {
    str(key): value
    for key, value in sorted(Counter(data["sizes"].tolist()).items())
}
if sum(int(key) * value for key, value in histogram.items()) != D:
    raise AssertionError("L14 orbit histogram does not cover full word space")
phase("L14_GENERATOR_BFS_AND_AGGREGATED_CSR_COMPLETE", orbit_histogram=histogram,
      aggregated_entries=int(data["destinations"].size))

csr_bytes = int(
    data["offsets"].nbytes
    + data["destinations"].nbytes
    + data["coefficients"].nbytes
    + data["multiplicities"].nbytes
    + data["internal_signed"].nbytes
    + data["connector_signed"].nbytes
)
orbit_bytes = int(
    data["orbit_id"].nbytes + data["representatives"].nbytes + data["sizes"].nbytes
)
del data["orbit_id"]
gc.collect()

even_mask = sum(1 << site for site in range(0, N, 2))
initial = np.zeros(M_EXPECTED, np.complex128)
valid = (data["representatives"] & even_mask) == 0
initial[valid] = np.sqrt(data["sizes"][valid].astype(np.float64)) / math.sqrt(1 << L)
current_internal_rows = np.empty(M_EXPECTED, np.float64)
current_connector_rows = np.empty(M_EXPECTED, np.float64)
state_vector_bytes = 8 * M_EXPECTED * 2 + 6 * 16 * M_EXPECTED
guard("RK4 work vectors", csr_bytes + orbit_bytes, state_vector_bytes)

probe_h = np.empty_like(initial)
h_into(initial, probe_h, data["offsets"], data["destinations"], data["coefficients"])
source_norm_error = float(abs(np.vdot(initial, initial).real - 1.0))
source_energy_imag = float(abs(np.vdot(initial, probe_h).imag))
source_current_linf = float(
    np.max(
        np.abs(
            quotient_currents(
                initial, data, current_internal_rows, current_connector_rows
            )
        )
    )
)
rng = np.random.default_rng(1414)
probe_a = rng.normal(size=M_EXPECTED) + 1.0j * rng.normal(size=M_EXPECTED)
probe_b = rng.normal(size=M_EXPECTED) + 1.0j * rng.normal(size=M_EXPECTED)
probe_a /= np.linalg.norm(probe_a)
probe_b /= np.linalg.norm(probe_b)
h_a = np.empty_like(probe_a)
h_b = np.empty_like(probe_b)
h_into(probe_a, h_a, data["offsets"], data["destinations"], data["coefficients"])
h_into(probe_b, h_b, data["offsets"], data["destinations"], data["coefficients"])
hermitian_bilinear_error = float(abs(np.vdot(probe_a, h_b) - np.vdot(h_a, probe_b)))
del probe_a, probe_b, h_a, h_b, probe_h
gc.collect()
phase(
    "L14_STRUCTURAL_NUMERICAL_PROBES_PASS",
    csr_bytes=csr_bytes,
    source_norm_error=source_norm_error,
    source_energy_imag=source_energy_imag,
    source_current_linf=source_current_linf,
    hermitian_bilinear_error=hermitian_bilinear_error,
)
if os.environ.get("AUDIT_STRUCTURE_ONLY") == "1":
    print("PASS__HOSTILE_L14_REMEDY_STRUCTURE_ONLY", flush=True)
    raise SystemExit(0)

coarse_state, coarse_currents = evolve(
    initial,
    data,
    COARSE_STEPS,
    "COARSE_RK4",
    current_internal_rows,
    current_connector_rows,
)
fine_state, integrated_currents = evolve(
    initial,
    data,
    FINE_STEPS,
    "FINE_RK4",
    current_internal_rows,
    current_connector_rows,
)

q_even, q_odd, both_internal, both_connector, number_law = diagonal_summary(
    fine_state,
    data["representatives"],
    L,
    data["edge_u"],
    data["edge_v"],
    data["edge_kind"],
)
q_even_coarse, q_odd_coarse, _, _, _ = diagonal_summary(
    coarse_state,
    data["representatives"],
    L,
    data["edge_u"],
    data["edge_v"],
    data["edge_kind"],
)
q0_even, q0_odd, _, _, number_law0 = diagonal_summary(
    initial,
    data["representatives"],
    L,
    data["edge_u"],
    data["edge_v"],
    data["edge_kind"],
)
q = np.array([q_even if site % 2 == 0 else q_odd for site in range(N)])
q_coarse = np.array(
    [q_even_coarse if site % 2 == 0 else q_odd_coarse for site in range(N)]
)
q0 = np.array([q0_even if site % 2 == 0 else q0_odd for site in range(N)])

balance = np.zeros(N)
balance_coarse = np.zeros(N)
for edge, (u, v, _) in enumerate(edges):
    balance[u] += integrated_currents[edge]
    balance[v] -= integrated_currents[edge]
    balance_coarse[u] += coarse_currents[edge]
    balance_coarse[v] -= coarse_currents[edge]
residual = q - q0 + balance
residual_coarse = q_coarse - q0 + balance_coarse
correlations = np.array(
    [
        (both_internal if kind == 0 else both_connector) - q[u] * q[v]
        for u, v, kind in edges
    ]
)
connector_mask = np.array([kind == 1 for _, _, kind in edges])
throughput_component = float(np.sum(np.abs(integrated_currents)))
connector_throughput_component = float(
    np.sum(np.abs(integrated_currents[connector_mask]))
)
throughput_global = COMPONENTS * throughput_component
connector_throughput_global = COMPONENTS * connector_throughput_component
retained_global = float(COMPONENTS * np.sum(q))

h_initial = np.empty_like(initial)
h_fine = np.empty_like(fine_state)
h_into(initial, h_initial, data["offsets"], data["destinations"], data["coefficients"])
h_into(fine_state, h_fine, data["offsets"], data["destinations"], data["coefficients"])

target = json.loads((TARGET_DIR / "RESULT.json").read_text())
target_q = np.array(target["q_after"])
target_j = np.array(target["integrated_oriented_currents"])


def lower_target(length):
    if length == 4:
        packet = json.loads(
            (
                ROOT
                / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001"
                / "RESULT.json"
            ).read_text()
        )
        return next(row for row in packet["rows"] if row["kappa"] == KAPPA)
    return json.loads(
        (
            ROOT
            / f"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L{length}_ACCUMULATION_V001"
            / "RESULT.json"
        ).read_text()
    )


comparators = {}
for length, retained in ((4, 16.0), (6, 54.0), (8, 128.0), (10, 250.0), (12, 432.0)):
    lower = lower_target(length)
    lower_total = lower["absolute_oriented_throughput_global"]
    lower_connector = lower["absolute_connector_throughput_global"]
    comparators[f"L14_over_L{length}"] = {
        "throughput_total": throughput_global / lower_total,
        "throughput_per_retained_record": (throughput_global / 686.0)
        / (lower_total / retained),
        "connector_throughput": connector_throughput_global / lower_connector,
        "connector_throughput_per_retained_record":
        (connector_throughput_global / 686.0) / (lower_connector / retained),
    }

comparator_target_linf = max(
    abs(comparators[key][field] - target["comparators"][key][field])
    for key in comparators
    for field in comparators[key]
)
q_target_linf = float(np.max(np.abs(q - target_q)))
current_target_linf = float(np.max(np.abs(integrated_currents - target_j)))
correlation_target_abs = abs(
    float(np.max(np.abs(correlations))) - target["max_abs_connected_edge_correlation"]
)
retained_target_abs = abs(retained_global - target["expected_retained_global"])
throughput_target_abs = abs(
    throughput_global - target["absolute_oriented_throughput_global"]
)
connector_throughput_target_abs = abs(
    connector_throughput_global - target["absolute_connector_throughput_global"]
)
residual_l1 = float(np.sum(np.abs(residual)))
residual_linf = float(np.max(np.abs(residual)))
coarse_residual_l1 = float(np.sum(np.abs(residual_coarse)))

checks = [
    (l4_validation["full_space_action_linf"] < 2e-14, "L4 full-space action"),
    (l4_validation["full_space_current_linf"] < 2e-14, "L4 full-space current"),
    (l4_validation["full_space_diagonal_linf"] < 2e-14, "L4 full-space diagonal"),
    (len(group) == 28 and data["representatives"].size == M_EXPECTED, "L14 orbit census"),
    (sum(int(key) * value for key, value in histogram.items()) == D, "L14 orbit coverage"),
    (data["destinations"].size < 201_769_050, "aggregated CSR reduction"),
    (source_norm_error < 2e-12 and source_energy_imag < 2e-12, "source invariants"),
    (source_current_linf < 2e-12, "source current"),
    (hermitian_bilinear_error < 2e-12, "Hamiltonian Hermiticity probe"),
    (float(np.max(np.abs(fine_state - coarse_state))) < 2e-8, "state refinement"),
    (float(np.max(np.abs(q - q_coarse))) < 2e-8, "occupation refinement"),
    (float(np.max(np.abs(integrated_currents - coarse_currents))) < 2e-8, "current refinement"),
    (q_target_linf < 6e-9, "target occupations"),
    (current_target_linf < 6e-9, "target currents"),
    (correlation_target_abs < 6e-9, "target correlations"),
    (retained_target_abs < 2e-7, "target retained total"),
    (throughput_target_abs < 3e-6, "target total throughput"),
    (connector_throughput_target_abs < 2e-6, "target connector throughput"),
    (residual_l1 < 2e-8, "explicit owner-edge residual L1"),
    (residual_linf < 2e-9, "explicit owner-edge residual Linf"),
    (residual_l1 <= coarse_residual_l1 + 1e-9, "residual refinement nonworsening"),
    (comparator_target_linf < 6e-8, "all target total and connector comparators"),
    (abs(np.vdot(fine_state, fine_state).real - 1.0) < 2e-8, "norm"),
    (abs(np.vdot(fine_state, h_fine).real - np.vdot(initial, h_initial).real) < 2e-7, "energy"),
    (abs(np.vdot(fine_state, h_fine).imag) < 2e-8, "energy reality"),
    (float(np.max(np.abs(number_law - number_law0))) < 2e-8, "number law"),
    (int(np.sum(np.abs(integrated_currents[: 2 * L]) > 1e-10)) == 28, "internal currents active"),
    (int(np.sum(np.abs(integrated_currents[2 * L :]) > 1e-10)) == 14, "connector currents active"),
    (rss_bytes() < GUARD_BYTES, "RSS guard"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "AUDIT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001",
    "verdict": "PASS__INDEPENDENT_L14_NUMERICAL_RECONSTRUCTION" if not failures else "FAIL_CLOSED__INDEPENDENT_L14_NUMERICAL_RECONSTRUCTION_FAILED",
    "target_disposition": "ELIGIBLE_FOR_PROMOTION_WITH_CLAIM_CEILINGS" if not failures else "UNCHANGED__UNPROMOTED",
    "method": "GENERATOR_BFS__FIXED_WIDTH_AGGREGATED_CSR__REPRESENTATIVE_DIAGONALS__CLASSICAL_RK4_1024_2048__SIMPSON",
    "l4_full_space_validation": l4_validation,
    "finite_orbit_basis": {
        "full_dimension": D,
        "finite_group_order": len(group),
        "orbit_dimension": int(data["representatives"].size),
        "orbit_size_histogram": histogram,
        "aggregated_csr_entries": int(data["destinations"].size),
        "aggregated_csr_bytes": csr_bytes,
        "signed_edge_orbits": len(data["edge_representatives"]),
        "storage_status": "FIXED_WIDTH_AGGREGATED_ROWS__NO_PYTHON_OBJECTS_PROPORTIONAL_TO_TRANSITIONS",
    },
    "parameters": {
        "kappa": KAPPA,
        "coarse_rk4_steps": COARSE_STEPS,
        "fine_rk4_steps": FINE_STEPS,
        "quadrature": "COMPOSITE_SIMPSON_ON_RK4_NODES",
    },
    "q_before": q0.tolist(),
    "q_after": q.tolist(),
    "integrated_oriented_currents": integrated_currents.tolist(),
    "absolute_oriented_throughput_per_component": throughput_component,
    "absolute_oriented_throughput_global": throughput_global,
    "absolute_connector_throughput_per_component": connector_throughput_component,
    "absolute_connector_throughput_global": connector_throughput_global,
    "expected_retained_global": retained_global,
    "max_abs_connected_edge_correlation": float(np.max(np.abs(correlations))),
    "record_ledger_residual_l1_per_component": residual_l1,
    "record_ledger_residual_linf_per_component": residual_linf,
    "record_ledger_residual_l1_global_bound": COMPONENTS * residual_l1,
    "coarse_record_ledger_residual_l1_per_component": coarse_residual_l1,
    "state_refinement_linf": float(np.max(np.abs(fine_state - coarse_state))),
    "occupation_refinement_linf": float(np.max(np.abs(q - q_coarse))),
    "current_refinement_linf": float(np.max(np.abs(integrated_currents - coarse_currents))),
    "target_reproduction": {
        "q_linf": q_target_linf,
        "current_linf": current_target_linf,
        "correlation_abs": correlation_target_abs,
        "retained_abs": retained_target_abs,
        "total_throughput_abs": throughput_target_abs,
        "connector_throughput_abs": connector_throughput_target_abs,
        "all_comparator_linf": comparator_target_linf,
    },
    "comparators": comparators,
    "norm_error": float(abs(np.vdot(fine_state, fine_state).real - 1.0)),
    "energy_error": float(abs(np.vdot(fine_state, h_fine).real - np.vdot(initial, h_initial).real)),
    "energy_imag_abs": float(abs(np.vdot(fine_state, h_fine).imag)),
    "number_law_max_change": float(np.max(np.abs(number_law - number_law0))),
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "runtime_seconds": time.perf_counter() - STARTED,
    "max_rss_bytes": rss_bytes(),
    "guard_bytes": GUARD_BYTES,
    "history": [
        "PRIOR_FAIL_CLOSED__NO_INDEPENDENT_L14_EVOLUTION",
        "REJECTED_FULL_WORD_KERNEL_LIFT__NOT_MEMORY_BOUNDED",
        "REJECTED_PYTHON_OBJECT_TRANSITION_LIFT__NOT_MEMORY_BOUNDED",
        "CURRENT_INDEPENDENT_FIXED_WIDTH_REMEDY_EXECUTED",
    ],
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "claim_ceiling": "CONDITIONAL_MICROSCOPIC_NUMERICAL_RECORD_ONLY",
    "not_claimed": "CONVERGENCE__LIMIT__FIT__SCALING__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
}
if OUT.exists():
    canonical = json.loads(OUT.read_text())

    def compatible(observed, expected, path="root"):
        if path in ("root.runtime_seconds", "root.max_rss_bytes"):
            return
        if isinstance(expected, dict):
            if not isinstance(observed, dict) or set(observed) != set(expected):
                raise AssertionError(f"saved-result keys differ at {path}")
            for key in expected:
                compatible(observed[key], expected[key], f"{path}.{key}")
        elif isinstance(expected, list):
            if not isinstance(observed, list) or len(observed) != len(expected):
                raise AssertionError(f"saved-result list differs at {path}")
            for index, (left, right) in enumerate(zip(observed, expected)):
                compatible(left, right, f"{path}[{index}]")
        elif isinstance(expected, float):
            if not isinstance(observed, (int, float)) or abs(float(observed) - expected) > 2e-9:
                raise AssertionError(f"saved-result float differs at {path}")
        elif observed != expected:
            raise AssertionError(f"saved-result value differs at {path}")

    compatible(out, canonical)
else:
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
phase("AUDIT_COMPLETE", verdict=out["verdict"], checks=f"{out['checks_passed']}/{out['checks_total']}")
if failures:
    raise AssertionError(failures)
print(f"PASS__HOSTILE_L14_INDEPENDENT_NUMERICAL_AUDIT__{len(checks)}/{len(checks)}")
