#!/usr/bin/env python3
"""Independent hostile audit of the L8 rail-wrap-removal control.

No target code is imported. The audit uses a unitary fourth-order
Suzuki--Yoshida factorization over independently reconstructed commuting edge
matchings, rather than the target's order-ten Taylor propagation.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import resource
import sys
import time
from collections import deque
from fractions import Fraction
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_RESULT.json"
TARGET_DIR = ROOT / "DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001"
TARGET_RESULT = TARGET_DIR / "RESULT.json"
PERIODIC_RESULT = ROOT / "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/RESULT.json"
L = 8
SITES = 16
FULL_WORDS = 1 << SITES
MAX_PARTICLES = 4
PROBE = 0
TARGET_SITE = 4
BACKGROUND = (1, 2, 3)
REMOVED = ((7, 0, "rail_1"), (15, 8, "rail_2"))
CAPACITY_TIME = math.pi / 2.0
SEARCH_TIME = 2.0 * math.pi
PEAK_FLOOR = 1e-8
COARSE_STEPS = 1024
FINE_STEPS = 2048

EXPECTED_SHA256 = {
    "DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001/README.md":
        "179701737928567ed20268f1d4c0beed4907b14429721d3b1be404e2ec6b2df7",
    "DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001/RESULT.json":
        "4e8e4ce50d46f750c086a534c59654cb1bb5e665e4c5edcadc0d78e366135c42",
    "DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001/RESULT.md":
        "8fea1df27a4261acba1c0fc9b762dd2c09b1a8d07aac3b44157a3ba25133772f",
    "DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001/THEOREM.md":
        "e2ca40cebdeea66f854a976bb4c45052e0ac7d6b400a766633e475abbf710bb0",
    "DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001/compute_open_ladder_control.py":
        "1f17152eb1d4f7b6ccca462ba2d3e02e24436bbc6166fa540fc94524ee38db16",
    "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/RESULT.json":
        "14eca704f5e1f65eeaf9cc04a0aa40a9f2dcd8f19ea7a440cf507fb0b76f3759",
    "AUDIT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/INDEPENDENT_RESULT.json":
        "748404604c97434221052272de9cb751e99749e20897fc35f93be7a0d296efde",
    "DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/RESULT.json":
        "e31019933d5465377710336935e2a3607c3185735b871a58f2475f6a7bf14926",
    "AUDIT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/INDEPENDENT_RESULT.json":
        "272c7c80a0eac374768367f1bb02f4cb989e6f64c0336d37223ee9b074133211",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def periodic_edges(length: int):
    edges = []
    for rail in (0, 1):
        offset = rail * length
        for node in range(length):
            edges.append((offset + node, offset + ((node + 1) % length), f"rail_{rail + 1}"))
    for node in range(length):
        edges.append((node, length + ((node + 1) % length), "connector"))
    return edges


def graph_census(edges, blocked=()):
    blocked = set(blocked)
    adjacency = [set() for _ in range(SITES)]
    for u, v, _ in edges:
        if u not in blocked and v not in blocked:
            adjacency[u].add(v)
            adjacency[v].add(u)
    distance = [-1] * SITES
    path_count = [0] * SITES
    if PROBE in blocked or TARGET_SITE in blocked:
        return adjacency, distance, path_count
    distance[PROBE] = 0
    path_count[PROBE] = 1
    queue = deque([PROBE])
    while queue:
        u = queue.popleft()
        for v in sorted(adjacency[u]):
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                path_count[v] = path_count[u]
                queue.append(v)
            elif distance[v] == distance[u] + 1:
                path_count[v] += path_count[u]
    return adjacency, distance, path_count


def shortest_paths(adjacency, distance):
    paths = []

    def visit(path):
        u = path[-1]
        if u == TARGET_SITE:
            paths.append(path)
            return
        for v in sorted(adjacency[u]):
            if distance[v] == distance[u] + 1 and distance[v] <= distance[TARGET_SITE]:
                visit(path + [v])

    visit([PROBE])
    return paths


def written_state(sources, basis_words, lookup):
    state = np.zeros(len(basis_words), dtype=np.complex128)
    scale = 2.0 ** (-0.5 * len(sources))
    for subset in range(1 << len(sources)):
        word = 0
        occupied = 0
        for index, site in enumerate(sources):
            if subset & (1 << index):
                word |= 1 << site
                occupied += 1
        state[lookup[word]] = scale * ((-1j) ** occupied)
    return state


def build_pairs(edges, basis_words, lookup):
    pairs = []
    for u, v, _ in edges:
        bu = (basis_words >> u) & 1
        bv = (basis_words >> v) & 1
        left = np.flatnonzero((bu == 0) & (bv == 1))
        right = lookup[basis_words[left] ^ (1 << u) ^ (1 << v)]
        if np.any(right < 0):
            raise AssertionError("particle-sector closure failed")
        pairs.append((left, right))
    return pairs


def h_action(states, pairs):
    out = np.zeros_like(states)
    for left, right in pairs:
        out[left] -= states[right]
        out[right] -= states[left]
    return out


def edge_currents(states, pairs):
    result = np.empty((states.shape[1], len(pairs)), dtype=float)
    for edge, (left, right) in enumerate(pairs):
        result[:, edge] = np.sum(
            states[left].conj() * (1j * states[right])
            + states[right].conj() * (-1j * states[left]),
            axis=0,
        ).real
    return result


def apply_edge(states, pair, interval):
    left, right = pair
    a = states[left].copy()
    b = states[right].copy()
    c = math.cos(interval)
    s = 1j * math.sin(interval)
    states[left] = c * a + s * b
    states[right] = s * a + c * b


def apply_matching(states, pairs, matching, interval):
    for edge in matching:
        apply_edge(states, pairs[edge], interval)


def second_order(states, pairs, matchings, interval):
    apply_matching(states, pairs, matchings[0], interval / 2.0)
    apply_matching(states, pairs, matchings[1], interval / 2.0)
    apply_matching(states, pairs, matchings[2], interval)
    apply_matching(states, pairs, matchings[1], interval / 2.0)
    apply_matching(states, pairs, matchings[0], interval / 2.0)


W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
W0 = -(2.0 ** (1.0 / 3.0)) / (2.0 - 2.0 ** (1.0 / 3.0))


def fourth_order(states, pairs, matchings, interval):
    second_order(states, pairs, matchings, W1 * interval)
    second_order(states, pairs, matchings, W0 * interval)
    second_order(states, pairs, matchings, W1 * interval)


def occupations(states, site_bits):
    return np.einsum("sw,wh->hs", site_bits, np.abs(states) ** 2, optimize=False)


def target_occupations(states, target_bits):
    return np.einsum("w,wh->h", target_bits, np.abs(states) ** 2, optimize=False)


def evolve(step_count, initial, pairs, matchings, target_bits):
    step = SEARCH_TIME / step_count
    capacity_index = round(CAPACITY_TIME / step)
    if capacity_index % 2 or abs(capacity_index * step - CAPACITY_TIME) > 1e-14:
        raise AssertionError("capacity endpoint is not an even Simpson node")
    states = initial.copy()
    target_trace = np.empty((step_count + 1, states.shape[1]), dtype=float)
    target_trace[0] = target_occupations(states, target_bits)
    current_accumulator = edge_currents(states, pairs)
    capacity_states = None
    for index in range(1, step_count + 1):
        fourth_order(states, pairs, matchings, step)
        target_trace[index] = target_occupations(states, target_bits)
        if index <= capacity_index:
            weight = 1.0 if index == capacity_index else (4.0 if index % 2 else 2.0)
            current_accumulator += weight * edge_currents(states, pairs)
            if index == capacity_index:
                capacity_states = states.copy()
    return {
        "times": np.linspace(0.0, SEARCH_TIME, step_count + 1),
        "target_trace": target_trace,
        "capacity_states": capacity_states,
        "capacity_currents": current_accumulator * (step / 3.0),
        "search_states": states,
    }


def first_positive_peak(times, values):
    for index in range(1, len(values) - 1):
        if values[index] > PEAK_FLOOR and values[index] > values[index - 1] and values[index] >= values[index + 1]:
            denominator = values[index - 1] - 2.0 * values[index] + values[index + 1]
            offset = 0.0
            if denominator != 0.0:
                offset = 0.5 * (values[index - 1] - values[index + 1]) / denominator
                offset = min(0.5, max(-0.5, offset))
            step = times[1] - times[0]
            tau = times[index] + offset * step
            peak = values[index] - 0.25 * (values[index - 1] - values[index + 1]) * offset
            return float(tau), float(peak), index, float(offset)
    raise AssertionError("no positive occupation peak")


started = time.perf_counter()
checks = []


def check(condition, label):
    checks.append((bool(condition), label))


observed_hashes = {relative: sha256(ROOT / relative) for relative in EXPECTED_SHA256}
check(observed_hashes == EXPECTED_SHA256, "target and immutable antecedent SHA-256 custody")
target = json.loads(TARGET_RESULT.read_text())
periodic = json.loads(PERIODIC_RESULT.read_text())
check(target["status"] == "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT", "target remains audit candidate")
check(target["checks_passed"] == target["checks_total"] == 21, "target reports 21/21")
check(target["parameters"]["L"] == 8 and target["parameters"]["full_word_dimension"] == FULL_WORDS, "target bounded to L8")

periodic_support = periodic_edges(L)
edges = [edge for edge in periodic_support if edge not in REMOVED]
adjacency, distance, path_count = graph_census(edges)
avoid_adjacency, avoid_distance, avoid_path_count = graph_census(edges, blocked=BACKGROUND)
main_paths = shortest_paths(adjacency, distance)
bypass_paths = shortest_paths(avoid_adjacency, avoid_distance)
connector_indices = [index for index, edge in enumerate(edges) if edge[2] == "connector"]

check(len(periodic_support) == 24 and len(edges) == 22, "periodic-to-open exact two-edge reduction")
check(set(periodic_support) - set(edges) == set(REMOVED), "only the two declared rail owners removed")
check(all(edge not in edges for edge in REMOVED), "both rail wrap owners absent")
check(len(connector_indices) == 8 and all(edges[i][2] == "connector" for i in connector_indices), "all eight connector owners retained")
degree_census = [len(row) for row in adjacency]
check(degree_census == [2, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 2], "open-support degree census")
check(distance[TARGET_SITE] == 4 and path_count[TARGET_SITE] == 1, "unique shortest path length four")
check(main_paths == [[0, 1, 2, 3, 4]], "unique shortest path identity")
expected_bypasses = [[0, 9, 8, 7, 6, 5, 4], [0, 9, 10, 11, 12, 13, 4]]
check(avoid_distance[TARGET_SITE] == 6 and avoid_path_count[TARGET_SITE] == 2, "two shortest bypasses of length six")
check(bypass_paths == expected_bypasses, "two bypass path identities")
check(target["topology"]["removed_owner_edges"] == [list(edge) for edge in REMOVED], "target removed-edge custody")

# Re-index the three commuting color classes after removal. Group zero remains
# a perfect matching, group one contains the six non-wrap odd rail edges, and
# group two contains all eight connectors.
matchings = (
    tuple(i for i, edge in enumerate(edges) if edge[2].startswith("rail") and (edge[0] % L) % 2 == 0),
    tuple(i for i, edge in enumerate(edges) if edge[2].startswith("rail") and (edge[0] % L) % 2 == 1),
    tuple(connector_indices),
)
check([len(group) for group in matchings] == [8, 6, 8], "open edge-color matching sizes")
for group_index, group in enumerate(matchings):
    endpoints = [site for edge in group for site in edges[edge][:2]]
    check(len(endpoints) == len(set(endpoints)), f"matching {group_index} vertex-disjoint")
check(set(sum((list(group) for group in matchings), [])) == set(range(22)), "matchings cover all 22 owners once")

all_words = np.arange(FULL_WORDS, dtype=np.int64)
particle_number = np.array([bin(int(word)).count("1") for word in all_words])
basis_words = all_words[particle_number <= MAX_PARTICLES]
lookup = np.full(FULL_WORDS, -1, dtype=np.int64)
lookup[basis_words] = np.arange(len(basis_words))
check(len(basis_words) == sum(math.comb(SITES, n) for n in range(5)) == 2517, "complete zero-through-four sector census")
pairs = build_pairs(edges, basis_words, lookup)

labels = []
sources = {}
for n in range(4):
    labels.extend((f"B{n}", f"P{n}"))
    sources[f"B{n}"] = BACKGROUND[:n]
    sources[f"P{n}"] = (PROBE,) + BACKGROUND[:n]
initial = np.column_stack([written_state(sources[label], basis_words, lookup) for label in labels])
label_index = {label: index for index, label in enumerate(labels)}
site_bits = np.array([((basis_words >> site) & 1).astype(float) for site in range(SITES)])
target_bits = site_bits[TARGET_SITE]
q_initial = occupations(initial, site_bits)

write_ledgers = {}
for i, label in enumerate(labels):
    count = len(sources[label])
    exact_residual = Fraction(count, 2) - Fraction(count, 2)
    write_ledgers[label] = {
        "sources": list(sources[label]),
        "delta_Q": str(Fraction(count, 2)),
        "edge_flux_terms_off": "0",
        "total_W_R": str(Fraction(count, 2)),
        "residual": str(exact_residual),
    }
    check(exact_residual == 0, f"{label} exact authenticated write ledger")
    check(abs(float(np.sum(q_initial[i])) - count / 2.0) < 2e-15, f"{label} written occupation total")

coarse = evolve(COARSE_STEPS, initial, pairs, matchings, target_bits)
fine = evolve(FINE_STEPS, initial, pairs, matchings, target_bits)
q_capacity = occupations(fine["capacity_states"], site_bits)
q_capacity_coarse = occupations(coarse["capacity_states"], site_bits)

incidence = np.zeros((SITES, len(edges)))
for edge, (u, v, _) in enumerate(edges):
    incidence[u, edge] = 1.0
    incidence[v, edge] = -1.0
history_residual = q_capacity - q_initial + np.einsum(
    "he,se->hs", fine["capacity_currents"], incidence, optimize=False
)

target_rows = {row["N"]: row for row in target["rows"]}
periodic_rows = {row["N"]: row for row in periodic["rows"]}
rows = []
for n in range(4):
    ib = label_index[f"B{n}"]
    ip = label_index[f"P{n}"]
    signal = fine["target_trace"][:, ip] - fine["target_trace"][:, ib]
    signal_coarse = coarse["target_trace"][:, ip] - coarse["target_trace"][:, ib]
    tau, peak, peak_index, peak_offset = first_positive_peak(fine["times"], signal)
    tau_coarse, peak_coarse, _, _ = first_positive_peak(coarse["times"], signal_coarse)
    delta_current = fine["capacity_currents"][ip] - fine["capacity_currents"][ib]
    delta_current_coarse = coarse["capacity_currents"][ip] - coarse["capacity_currents"][ib]
    delta_q = q_capacity[ip] - q_capacity[ib]
    source_vector = np.zeros(SITES)
    source_vector[PROBE] = 0.5
    probe_residual = delta_q + np.einsum("se,e->s", incidence, delta_current, optimize=False) - source_vector
    connector = delta_current[connector_indices]
    stored = target_rows[n]
    periodic_tau = periodic_rows[n]["tau_first_positive_peak"]
    rows.append({
        "N": n,
        "background_sites": list(BACKGROUND[:n]),
        "tau_open": tau,
        "tau_open_coarse": tau_coarse,
        "tau_coarse_fine_abs": abs(tau - tau_coarse),
        "tau_target": stored["tau_open"],
        "tau_target_abs_error": abs(tau - stored["tau_open"]),
        "peak_delta_q4": peak,
        "peak_delta_q4_coarse": peak_coarse,
        "peak_coarse_fine_abs": abs(peak - peak_coarse),
        "peak_target": stored["first_peak_delta_q4"],
        "peak_target_abs_error": abs(peak - stored["first_peak_delta_q4"]),
        "fine_peak_index": peak_index,
        "fine_peak_offset": peak_offset,
        "periodic_tau": periodic_tau,
        "open_minus_periodic_tau": tau - periodic_tau,
        "periodic_tau_custody_error": abs(periodic_tau - stored["periodic_tau"]),
        "open_minus_periodic_target_error": abs((tau - periodic_tau) - stored["open_minus_periodic_tau"]),
        "connector_delta_l1": float(np.sum(np.abs(connector))),
        "connector_delta_signed": float(np.sum(connector)),
        "connector_delta_vector": [float(value) for value in connector],
        "connector_target_linf": float(np.max(np.abs(connector - np.array(stored["J_connector_probe_delta_vector"])))),
        "background_connector_l1": float(np.sum(np.abs(fine["capacity_currents"][ib, connector_indices]))),
        "probe_plus_background_connector_l1": float(np.sum(np.abs(fine["capacity_currents"][ip, connector_indices]))),
        "connector_l1_target_abs_error": abs(float(np.sum(np.abs(connector))) - stored["J_connector_probe_delta_l1"]),
        "connector_signed_target_abs_error": abs(float(np.sum(connector)) - stored["J_connector_probe_delta_signed"]),
        "background_connector_l1_target_abs_error": abs(float(np.sum(np.abs(fine["capacity_currents"][ib, connector_indices]))) - stored["J_connector_background_l1"]),
        "probe_plus_background_connector_l1_target_abs_error": abs(float(np.sum(np.abs(fine["capacity_currents"][ip, connector_indices]))) - stored["J_connector_probe_plus_background_l1"]),
        "complete_probe_delta_current": [float(value) for value in delta_current],
        "complete_current_target_linf": float(np.max(np.abs(delta_current - np.array(stored["complete_probe_delta_current"])))),
        "complete_current_coarse_fine_linf": float(np.max(np.abs(delta_current - delta_current_coarse))),
        "probe_ledger_residual": [float(value) for value in probe_residual],
        "probe_ledger_residual_l1": float(np.sum(np.abs(probe_residual))),
        "probe_ledger_residual_linf": float(np.max(np.abs(probe_residual))),
    })

initial_norm = np.sum(np.abs(initial) ** 2, axis=0)
capacity_norm = np.sum(np.abs(fine["capacity_states"]) ** 2, axis=0)
search_norm = np.sum(np.abs(fine["search_states"]) ** 2, axis=0)
initial_energy = np.sum(initial.conj() * h_action(initial, pairs), axis=0).real
capacity_energy = np.sum(fine["capacity_states"].conj() * h_action(fine["capacity_states"], pairs), axis=0).real
search_energy = np.sum(fine["search_states"].conj() * h_action(fine["search_states"], pairs), axis=0).real
capacity_number = np.sum(np.abs(fine["capacity_states"]) ** 2 * particle_number[basis_words, None], axis=0)
search_number = np.sum(np.abs(fine["search_states"]) ** 2 * particle_number[basis_words, None], axis=0)
expected_number = np.array([len(sources[label]) / 2.0 for label in labels])
taus = np.array([row["tau_open"] for row in rows])
capacities = np.array([row["connector_delta_l1"] for row in rows])

check(float(np.max(np.abs(initial_norm - 1.0))) < 2e-15, "initial norms")
check(float(np.max(np.abs(capacity_norm - 1.0))) < 3e-12, "capacity norms")
check(float(np.max(np.abs(search_norm - 1.0))) < 7e-12, "search norms")
check(float(np.max(np.abs(capacity_energy - initial_energy))) < 2e-9, "capacity energy stability")
check(float(np.max(np.abs(search_energy - initial_energy))) < 3e-9, "search energy stability")
check(float(np.max(np.abs(capacity_number - expected_number))) < 8e-12, "capacity number conservation")
check(float(np.max(np.abs(search_number - expected_number))) < 8e-12, "search number conservation")
check(float(np.max(np.abs(q_capacity - q_capacity_coarse))) < 2e-8, "capacity occupation coarse/fine stability")
check(float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))) < 2e-7, "all current coarse/fine stability")
check(float(np.max(np.sum(np.abs(history_residual), axis=1))) < 3e-7, "all eight complete transport ledgers")
check(all(row["probe_ledger_residual_l1"] < 2e-7 for row in rows), "all four probe differential ledgers")
check(all(row["connector_target_linf"] < 2e-8 for row in rows), "all 32 connector components versus target")
check(all(row["connector_l1_target_abs_error"] < 2e-8 for row in rows), "all marginal connector L1 values versus target")
check(all(row["connector_signed_target_abs_error"] < 2e-8 for row in rows), "all signed connector sums versus target")
check(all(row["background_connector_l1_target_abs_error"] < 2e-8 for row in rows), "all background connector L1 values versus target")
check(all(row["probe_plus_background_connector_l1_target_abs_error"] < 2e-8 for row in rows), "all probe-plus-background connector L1 values versus target")
check(all(row["complete_current_target_linf"] < 2e-8 for row in rows), "all 88 complete current components versus target")
check(all(row["tau_target_abs_error"] < 5e-9 for row in rows), "all tau open values versus target")
check(all(row["peak_target_abs_error"] < 2e-9 for row in rows), "all first-peak amplitudes versus target")
check(all(row["periodic_tau_custody_error"] == 0.0 for row in rows), "sealed periodic tau row custody")
check(all(row["open_minus_periodic_target_error"] < 5e-9 for row in rows), "open-minus-periodic comparisons versus target")
check(all(row["peak_delta_q4"] > PEAK_FLOOR for row in rows), "positive first peaks above floor")
check(np.all(np.diff(taus) > 0.0), "tau open strictly increases N0 through N3")
check(taus[3] > taus[2] and taus[3] - taus[2] > 0.05, "periodic N3-before-N2 inversion disappears")
check(np.all(np.diff(capacities) < 0.0), "marginal connector L1 strictly decreases")
check(target["trend_screen"]["topology_classification"] == "INVERSION_DISAPPEARS_WITH_PERIODIC_RAIL_WRAP_EDGES_REMOVED__RING_MEDIATED_IN_DECLARED_PERIODIC_VERSUS_OPEN_COMPARISON", "declared topology classification only")

target_prose = "\n".join((
    (TARGET_DIR / "README.md").read_text(),
    (TARGET_DIR / "RESULT.md").read_text(),
    (TARGET_DIR / "THEOREM.md").read_text(),
))
check("two length-six routes avoiding nodes `1,2,3`" in target_prose and "does not establish a unique route" in target_prose, "remaining-bypass limitation")
check(target["protocol"]["lineage_boundary"].endswith("NO_INDIVIDUAL_CARRIER_TAG") and "Background subtraction is not individual lineage" in target_prose, "subtraction is not lineage")
check(all(term in target["not_claimed"] for term in ("UNIQUE_ALL_HISTORY_ROUTE", "INDIVIDUAL_LINEAGE", "METRIC_TIME_DILATION", "SHAPIRO_DELAY", "MACROSCOPIC_GRAVITATIONAL_EMERGENCE", "GRAVITY")), "forbidden promotions remain not claimed")
check("GATE_R_C_AND_A_P" in target["claim_classes"]["open"] and "OTHER_BOUNDARY_CUTS" in target["claim_classes"]["open"], "gates and other boundary controls remain open")
check("No physical\nmetric, time dilation, Shapiro delay, macroscopic emergence, or gravity claim" in target_prose, "no metric or gravity promotion")

failures = [label for passed, label in checks if not passed]
elapsed = time.perf_counter() - started
rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes = int(rss_raw if sys.platform == "darwin" else rss_raw * 1024)

result = {
    "schema": "AUDIT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001",
    "status": "PASS_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "base_commit": "d3c30fac07975bf7546fe7a23e798d06758f0040",
    "scope": "FINITE_L8_ONLY__NO_LARGER_SUPPORT_EXECUTED",
    "target_and_antecedent_sha256": observed_hashes,
    "audit_script_sha256": sha256(Path(__file__)),
    "method": {
        "target": "ORDER_TEN_TAYLOR__1024_2048_STEPS",
        "audit": "UNITARY_FOURTH_ORDER_SUZUKI_YOSHIDA__THREE_EXACT_EDGE_MATCHINGS__SEPARATE_1024_2048_STEP_RUNS",
        "arrival": "FIRST_POSITIVE_BACKGROUND_SUBTRACTED_Q4_PEAK_ABOVE_1E_8__ZERO_TO_TWO_PI",
        "current": "OWNER_ONCE_BACKGROUND_SUBTRACTED_INTEGRATED_VECTOR__SIMPSON_ZERO_TO_PI_OVER_TWO",
    },
    "topology": {
        "periodic_owner_edges": len(periodic_support),
        "open_owner_edges": len(edges),
        "removed_owner_edges": [list(edge) for edge in REMOVED],
        "retained_connectors": len(connector_indices),
        "degree_census": degree_census,
        "unique_shortest_path": main_paths[0],
        "shortest_path_length": distance[TARGET_SITE],
        "bypass_paths_avoiding_1_2_3": bypass_paths,
        "bypass_path_length": avoid_distance[TARGET_SITE],
        "matching_edge_indices": [list(group) for group in matchings],
        "reachable_dimension": len(basis_words),
        "full_word_dimension": FULL_WORDS,
    },
    "authenticated_write_ledgers": write_ledgers,
    "rows": rows,
    "trend_screen": {
        "tau_open_strictly_increases_N0_to_N3": bool(np.all(np.diff(taus) > 0.0)),
        "N3_before_N2": bool(taus[3] < taus[2]),
        "N3_minus_N2": float(taus[3] - taus[2]),
        "connector_l1_strictly_decreases": bool(np.all(np.diff(capacities) < 0.0)),
        "classification": "INVERSION_DISAPPEARS_WITH_TWO_RAIL_WRAP_OWNERS_REMOVED__RING_MEDIATED_ONLY_IN_DECLARED_PERIODIC_VERSUS_OPEN_COMPARISON",
    },
    "numerical_controls": {
        "initial_norm_error_linf": float(np.max(np.abs(initial_norm - 1.0))),
        "capacity_norm_error_linf": float(np.max(np.abs(capacity_norm - 1.0))),
        "search_norm_error_linf": float(np.max(np.abs(search_norm - 1.0))),
        "capacity_energy_drift_linf": float(np.max(np.abs(capacity_energy - initial_energy))),
        "search_energy_drift_linf": float(np.max(np.abs(search_energy - initial_energy))),
        "capacity_number_error_linf": float(np.max(np.abs(capacity_number - expected_number))),
        "search_number_error_linf": float(np.max(np.abs(search_number - expected_number))),
        "capacity_occupation_coarse_fine_linf": float(np.max(np.abs(q_capacity - q_capacity_coarse))),
        "capacity_current_coarse_fine_linf": float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))),
        "history_ledger_residual_l1_max": float(np.max(np.sum(np.abs(history_residual), axis=1))),
        "probe_ledger_residual_l1_max": max(row["probe_ledger_residual_l1"] for row in rows),
        "connector_target_linf_max": max(row["connector_target_linf"] for row in rows),
        "connector_l1_target_abs_max": max(row["connector_l1_target_abs_error"] for row in rows),
        "connector_signed_target_abs_max": max(row["connector_signed_target_abs_error"] for row in rows),
        "background_connector_l1_target_abs_max": max(row["background_connector_l1_target_abs_error"] for row in rows),
        "probe_plus_background_connector_l1_target_abs_max": max(row["probe_plus_background_connector_l1_target_abs_error"] for row in rows),
        "complete_current_target_linf_max": max(row["complete_current_target_linf"] for row in rows),
        "tau_target_abs_max": max(row["tau_target_abs_error"] for row in rows),
        "peak_target_abs_max": max(row["peak_target_abs_error"] for row in rows),
        "tau_coarse_fine_abs_max": max(row["tau_coarse_fine_abs"] for row in rows),
        "peak_coarse_fine_abs_max": max(row["peak_coarse_fine_abs"] for row in rows),
    },
    "conceptual_disposition": {
        "classification": "FINITE_EFFECT_OF_EXACT_TWO_EDGE_CUT_IN_DECLARED_PERIODIC_VERSUS_OPEN_COMPARISON_ONLY",
        "routes": "ONE_LENGTH_FOUR_SHORTEST_PATH__TWO_LENGTH_SIX_BYPASSES_REMAIN",
        "lineage": "BACKGROUND_SUBTRACTION_IS_NOT_INDIVIDUAL_LINEAGE",
        "metric": "NOT_ESTABLISHED__NO_TIME_DILATION_OR_SHAPIRO_DELAY",
        "macroscopic_emergence": "NOT_ESTABLISHED",
        "gravity": "NOT_INFERRED",
    },
    "claim_classes": {
        "proved": "EXACT_TWO_OWNER_EDGE_REMOVAL__OPEN_SUPPORT_AND_PATH_CENSUS__EXACT_AUTHENTICATED_WRITE_LEDGERS__OWNER_ONCE_CONTINUITY",
        "adopted": "OPTION_B_LITERAL_RAIL_WRAP_REMOVAL__COMMON_PHASE__BACKGROUND_SUBTRACTION__WINDOWS__FIRST_PEAK_RULE",
        "conditional": "ALL_BLANK_PARENT__FINITE_NUMERICAL_EVOLUTION__ENSEMBLE_DIFFERENCE",
        "empirical": "INDEPENDENT_FINITE_N0_TO_N3_OPEN_ARRIVAL_AND_CONNECTOR_ROWS__DECLARED_PERIODIC_OPEN_COMPARISON",
        "open": "OTHER_BOUNDARY_CUTS_CONNECTOR_PATTERNS_PHASES_WINDOWS__INDIVIDUAL_LINEAGE__PHYSICAL_METRIC_CLOCK__MACROSCOPIC_EMERGENCE__GATE_R_C_AND_A_P",
    },
    "not_claimed": "UNIQUE_ALL_HISTORY_ROUTE__INDIVIDUAL_LINEAGE__METRIC_TIME_DILATION__SHAPIRO_DELAY__MACROSCOPIC_GRAVITATIONAL_EMERGENCE__GRAVITY",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "resources": {
        "runtime_seconds": elapsed,
        "max_rss_bytes": rss_bytes,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "numpy": np.__version__,
    },
}


def compatible(observed, canonical, path="root"):
    if path == "root.resources":
        return
    if isinstance(canonical, dict):
        if not isinstance(observed, dict) or set(observed) != set(canonical):
            raise AssertionError(f"key mismatch at {path}")
        for key in canonical:
            compatible(observed[key], canonical[key], f"{path}.{key}")
    elif isinstance(canonical, list):
        if not isinstance(observed, list) or len(observed) != len(canonical):
            raise AssertionError(f"list mismatch at {path}")
        for index, (left, right) in enumerate(zip(observed, canonical)):
            compatible(left, right, f"{path}[{index}]")
    elif isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 2e-9:
            raise AssertionError(f"float mismatch at {path}: {observed} != {canonical}")
    elif observed != canonical:
        raise AssertionError(f"value mismatch at {path}: {observed} != {canonical}")


if OUT.exists():
    compatible(result, json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"WROTE_CANONICAL_RESULT={OUT}")

if failures:
    raise AssertionError(failures)
print(f"PASS__AUDIT_R_GATE_C_L8_OPEN_LADDER_CONTROL__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={elapsed:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={rss_bytes}")
