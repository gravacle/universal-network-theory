#!/usr/bin/env python3
"""Independent hostile audit of the finite L8 accumulation-latency packet.

No target code is imported.  The target uses a tenth-order Taylor propagator;
this audit uses a unitary fourth-order Suzuki--Yoshida product formula over
three independently reconstructed commuting edge matchings.
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
TARGET_DIR = ROOT / "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001"
TARGET_RESULT = TARGET_DIR / "RESULT.json"
L = 8
SITES = 2 * L
FULL_WORDS = 1 << SITES
MAX_PARTICLES = 4
PROBE = 0
TARGET = 4
BACKGROUND = (1, 2, 3)
CAPACITY_TIME = math.pi / 2.0
SEARCH_TIME = 2.0 * math.pi
PEAK_FLOOR = 1e-8
COARSE_STEPS = 1024
FINE_STEPS = 2048

EXPECTED_SHA256 = {
    "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/README.md":
        "0aef1c417715484c151c029f254b750d281191316d6fce87dc8efe289556cbc7",
    "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/RESULT.json":
        "14eca704f5e1f65eeaf9cc04a0aa40a9f2dcd8f19ea7a440cf507fb0b76f3759",
    "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/RESULT.md":
        "b62ef4757ce2a830a9b2528a0c8bc0059f91c8ecf23b34e735a8211c5ea79b9d",
    "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/THEOREM.md":
        "6fe85a7e2416d604b9f882f374d182b64a40dea728dc2f63d2eea25635dd48bf",
    "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/compute_accumulation_latency.py":
        "acee648850fdf78344a140c627dfa6b064ef580308964bf3f959dda339139003",
    "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/THEOREM.md":
        "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/INDEPENDENT_RESULT.json":
        "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001/RESULT.json":
        "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
    "AUDIT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001/INDEPENDENT_RESULT.json":
        "5151b0deabf01ef0a7dc3dc604e6e638837df5537a01a0cc8361bf040e27091d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prism_edges(length: int):
    edges = []
    for rail in (0, 1):
        offset = rail * length
        for s in range(length):
            edges.append((offset + s, offset + ((s + 1) % length), f"rail_{rail + 1}"))
    for s in range(length):
        edges.append((s, length + ((s + 1) % length), "connector"))
    return edges


def bfs(edges, source: int):
    adjacency = [set() for _ in range(SITES)]
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    distance = [-1] * SITES
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in sorted(adjacency[u]):
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                queue.append(v)
    return adjacency, distance


def history_state(sources, basis_words, lookup):
    vector = np.zeros(len(basis_words), dtype=np.complex128)
    scale = 2.0 ** (-0.5 * len(sources))
    for subset in range(1 << len(sources)):
        word = 0
        occupied = 0
        for index, site in enumerate(sources):
            if subset & (1 << index):
                word |= 1 << site
                occupied += 1
        vector[lookup[word]] = scale * ((-1j) ** occupied)
    return vector


def build_edge_pairs(edges, basis_words, lookup):
    pairs = []
    for u, v, _ in edges:
        bu = (basis_words >> u) & 1
        bv = (basis_words >> v) & 1
        left = np.flatnonzero((bu == 0) & (bv == 1))
        partner_words = basis_words[left] ^ (1 << u) ^ (1 << v)
        right = lookup[partner_words]
        if np.any(right < 0):
            raise AssertionError("particle-number closure failed")
        pairs.append((left, right))
    return pairs


def raw_h_action(states, edge_pairs):
    out = np.zeros_like(states)
    for left, right in edge_pairs:
        out[left] -= states[right]
        out[right] -= states[left]
    return out


def edge_currents(states, edge_pairs):
    values = np.empty((states.shape[1], len(edge_pairs)), dtype=float)
    for edge, (left, right) in enumerate(edge_pairs):
        # For the stored orientation u->v, left denotes u blank/v occupied.
        # J[left,right]=+i and J[right,left]=-i.
        values[:, edge] = np.sum(
            states[left].conj() * (1j * states[right])
            + states[right].conj() * (-1j * states[left]),
            axis=0,
        ).real
    return values


def apply_edge_exponential(states, pair, interval):
    left, right = pair
    a = states[left].copy()
    b = states[right].copy()
    cosine = math.cos(interval)
    sine_i = 1j * math.sin(interval)
    states[left] = cosine * a + sine_i * b
    states[right] = sine_i * a + cosine * b


def apply_matching(states, edge_pairs, edge_indices, interval):
    # Edges in each matching are vertex-disjoint, hence their hopping terms
    # commute.  Sequential application here is the exact matching exponential.
    for edge in edge_indices:
        apply_edge_exponential(states, edge_pairs[edge], interval)


def second_order_step(states, edge_pairs, matchings, interval):
    apply_matching(states, edge_pairs, matchings[0], interval / 2.0)
    apply_matching(states, edge_pairs, matchings[1], interval / 2.0)
    apply_matching(states, edge_pairs, matchings[2], interval)
    apply_matching(states, edge_pairs, matchings[1], interval / 2.0)
    apply_matching(states, edge_pairs, matchings[0], interval / 2.0)


YOSHIDA_W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
YOSHIDA_W0 = -(2.0 ** (1.0 / 3.0)) / (2.0 - 2.0 ** (1.0 / 3.0))


def fourth_order_step(states, edge_pairs, matchings, interval):
    second_order_step(states, edge_pairs, matchings, YOSHIDA_W1 * interval)
    second_order_step(states, edge_pairs, matchings, YOSHIDA_W0 * interval)
    second_order_step(states, edge_pairs, matchings, YOSHIDA_W1 * interval)


def occupations(states, site_bits):
    probabilities = np.abs(states) ** 2
    return np.einsum("sw,wh->hs", site_bits, probabilities, optimize=False)


def target_occupation(states, target_bits):
    probabilities = np.abs(states) ** 2
    return np.einsum("w,wh->h", target_bits, probabilities, optimize=False)


def simpson_finish(accumulator, step):
    return accumulator * (step / 3.0)


def propagate(step_count, initial, edge_pairs, matchings, target_bits):
    step = SEARCH_TIME / step_count
    capacity_index = round(CAPACITY_TIME / step)
    if capacity_index % 2 or abs(capacity_index * step - CAPACITY_TIME) > 1e-14:
        raise AssertionError("capacity endpoint is not an even Simpson node")
    states = initial.copy()
    trace = np.empty((step_count + 1, states.shape[1]), dtype=float)
    trace[0] = target_occupation(states, target_bits)
    current_accumulator = edge_currents(states, edge_pairs)
    capacity_states = None
    for index in range(1, step_count + 1):
        fourth_order_step(states, edge_pairs, matchings, step)
        trace[index] = target_occupation(states, target_bits)
        if index <= capacity_index:
            weight = 1.0 if index == capacity_index else (4.0 if index % 2 else 2.0)
            current_accumulator += weight * edge_currents(states, edge_pairs)
            if index == capacity_index:
                capacity_states = states.copy()
    if capacity_states is None:
        raise AssertionError("capacity state missing")
    return {
        "times": np.linspace(0.0, SEARCH_TIME, step_count + 1),
        "target_trace": trace,
        "capacity_states": capacity_states,
        "capacity_currents": simpson_finish(current_accumulator, step),
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
            return float(tau), float(peak), index
    raise AssertionError("no positive first peak")


def linear_fit(values):
    x = np.arange(4, dtype=float)
    mean_x = 1.5
    mean_y = float(np.mean(values))
    slope = float(np.sum((x - mean_x) * (values - mean_y)) / np.sum((x - mean_x) ** 2))
    intercept = mean_y - slope * mean_x
    prediction = intercept + slope * x
    residual = float(np.sum((values - prediction) ** 2))
    total = float(np.sum((values - mean_y) ** 2))
    return intercept, slope, 1.0 - residual / total, -intercept / slope


started = time.perf_counter()
checks = []


def check(condition, label):
    checks.append((bool(condition), label))


observed_hashes = {relative: sha256(ROOT / relative) for relative in EXPECTED_SHA256}
check(observed_hashes == EXPECTED_SHA256, "target and immutable antecedent SHA-256 custody")
target = json.loads(TARGET_RESULT.read_text())
check(target["status"] == "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT", "target remains candidate")
check(target["checks_passed"] == target["checks_total"] == 17, "target reports 17/17")
check(target["parameters"]["L"] == 8 and target["parameters"]["full_word_dimension"] == 65536, "target bounded to L8")

edges = prism_edges(L)
adjacency, distance = bfs(edges, PROBE)
connector_indices = [index for index, edge in enumerate(edges) if edge[2] == "connector"]
check(len(edges) == 24 and len(set((u, v) for u, v, _ in edges)) == 24, "independent owner-once edge census")
check(connector_indices == list(range(16, 24)), "independent connector census and order")
check([len(row) for row in adjacency] == [3] * SITES, "independent degree-three census")
check(distance[TARGET] == 4, "probe-target graph distance four")
check(BACKGROUND == (1, 2, 3), "declared adjacent accumulation cluster")

# The even and odd edges on both rails are disjoint perfect matchings; the
# connector set is the third perfect matching.
matchings = (
    tuple(index for index in range(16) if (index % 8) % 2 == 0),
    tuple(index for index in range(16) if (index % 8) % 2 == 1),
    tuple(connector_indices),
)
check([len(group) for group in matchings] == [8, 8, 8], "three eight-edge matching partition")
for group_index, group in enumerate(matchings):
    endpoints = [site for edge in group for site in edges[edge][:2]]
    check(len(endpoints) == len(set(endpoints)) == SITES, f"matching {group_index} is vertex-disjoint")
check(set(sum((list(group) for group in matchings), [])) == set(range(24)), "matchings cover every owner edge once")

all_words = np.arange(FULL_WORDS, dtype=np.int64)
particle_number_full = np.array([bin(int(word)).count("1") for word in all_words])
basis_words = all_words[particle_number_full <= MAX_PARTICLES]
lookup = np.full(FULL_WORDS, -1, dtype=np.int64)
lookup[basis_words] = np.arange(len(basis_words))
check(len(basis_words) == sum(math.comb(SITES, n) for n in range(5)) == 2517, "complete zero-through-four sector census")
edge_pairs = build_edge_pairs(edges, basis_words, lookup)

labels = []
sources = {}
for n in range(4):
    labels.extend((f"B{n}", f"P{n}"))
    sources[f"B{n}"] = BACKGROUND[:n]
    sources[f"P{n}"] = (PROBE,) + BACKGROUND[:n]
initial = np.column_stack([history_state(sources[label], basis_words, lookup) for label in labels])
label_index = {label: index for index, label in enumerate(labels)}
site_bits = np.array([((basis_words >> site) & 1).astype(float) for site in range(SITES)])
target_bits = site_bits[TARGET]
q_initial = occupations(initial, site_bits)
q_initial_sum = np.sum(q_initial, axis=1)

write_ledgers = {}
for i, label in enumerate(labels):
    write_count = len(sources[label])
    residual = Fraction(write_count, 2) - Fraction(write_count, 2)
    write_ledgers[label] = {
        "source_sites": list(sources[label]),
        "delta_Q": str(Fraction(write_count, 2)),
        "edge_flux_terms_off": "0",
        "total_W_R": str(Fraction(write_count, 2)),
        "exact_residual": str(residual),
    }
    check(residual == 0, f"{label} exact authenticated terms-off write ledger")
    check(abs(q_initial_sum[i] - write_count / 2.0) < 2e-15, f"{label} initial written occupation total")
check(np.max(np.abs(initial[:, label_index["B0"]] - np.eye(len(basis_words), 1)[:, 0])) == 0.0, "all-blank B0 parent")

coarse = propagate(COARSE_STEPS, initial, edge_pairs, matchings, target_bits)
fine = propagate(FINE_STEPS, initial, edge_pairs, matchings, target_bits)
q_capacity_coarse = occupations(coarse["capacity_states"], site_bits)
q_capacity = occupations(fine["capacity_states"], site_bits)

incidence = np.zeros((SITES, len(edges)))
for edge, (u, v, _) in enumerate(edges):
    incidence[u, edge] = 1.0
    incidence[v, edge] = -1.0
history_residual = q_capacity - q_initial + np.einsum(
    "he,se->hs", fine["capacity_currents"], incidence, optimize=False
)

energy_initial = np.sum(initial.conj() * raw_h_action(initial, edge_pairs), axis=0).real
energy_capacity = np.sum(
    fine["capacity_states"].conj() * raw_h_action(fine["capacity_states"], edge_pairs), axis=0
).real
capacity_norm = np.sum(np.abs(fine["capacity_states"]) ** 2, axis=0)
search_norm = np.sum(np.abs(fine["search_states"]) ** 2, axis=0)

target_rows = {row["N"]: row for row in target["rows"]}
rows = []
for n in range(4):
    background_index = label_index[f"B{n}"]
    probe_index = label_index[f"P{n}"]
    signal = fine["target_trace"][:, probe_index] - fine["target_trace"][:, background_index]
    signal_coarse = coarse["target_trace"][:, probe_index] - coarse["target_trace"][:, background_index]
    tau, peak, peak_index = first_positive_peak(fine["times"], signal)
    tau_coarse, peak_coarse, peak_index_coarse = first_positive_peak(coarse["times"], signal_coarse)
    delta_current = fine["capacity_currents"][probe_index] - fine["capacity_currents"][background_index]
    delta_current_coarse = coarse["capacity_currents"][probe_index] - coarse["capacity_currents"][background_index]
    delta_q = q_capacity[probe_index] - q_capacity[background_index]
    source_vector = np.zeros(SITES)
    source_vector[PROBE] = 0.5
    probe_residual = delta_q + np.einsum("se,e->s", incidence, delta_current, optimize=False) - source_vector
    connector = delta_current[connector_indices]
    stored = target_rows[n]
    rows.append({
        "N": n,
        "background_sites": list(BACKGROUND[:n]),
        "tau_first_positive_peak": tau,
        "tau_coarse": tau_coarse,
        "tau_coarse_fine_abs": abs(tau - tau_coarse),
        "tau_target": stored["tau_first_positive_peak"],
        "tau_target_abs_error": abs(tau - stored["tau_first_positive_peak"]),
        "peak": peak,
        "peak_coarse": peak_coarse,
        "peak_target": stored["first_peak_incremental_target_occupation"],
        "peak_target_abs_error": abs(peak - stored["first_peak_incremental_target_occupation"]),
        "peak_index_fine": peak_index,
        "peak_index_coarse": peak_index_coarse,
        "connector_delta_vector": [float(value) for value in connector],
        "connector_delta_target": stored["J_connector_probe_delta_vector"],
        "connector_delta_target_linf": float(np.max(np.abs(connector - np.array(stored["J_connector_probe_delta_vector"])))),
        "connector_delta_l1": float(np.sum(np.abs(connector))),
        "connector_delta_signed": float(np.sum(connector)),
        "complete_probe_delta_current": [float(value) for value in delta_current],
        "complete_probe_delta_target_linf": float(np.max(np.abs(delta_current - np.array(stored["complete_probe_delta_current"])))),
        "complete_probe_delta_coarse_fine_linf": float(np.max(np.abs(delta_current - delta_current_coarse))),
        "probe_ledger_residual": [float(value) for value in probe_residual],
        "probe_ledger_residual_l1": float(np.sum(np.abs(probe_residual))),
        "probe_ledger_residual_linf": float(np.max(np.abs(probe_residual))),
    })

capacities = np.array([row["connector_delta_l1"] for row in rows])
taus = np.array([row["tau_first_positive_peak"] for row in rows])
fit_intercept, fit_slope, fit_r2, fit_zero = linear_fit(capacities)
stored_fit = target["trend_screen"]["linear_capacity_fit"]

check(float(np.max(np.abs(capacity_norm - 1.0))) < 2e-12, "capacity state norms")
check(float(np.max(np.abs(search_norm - 1.0))) < 6e-12, "search state norms")
check(float(np.max(np.abs(energy_capacity - energy_initial))) < 2e-9, "capacity energy stability")
check(float(np.max(np.abs(q_capacity - q_capacity_coarse))) < 2e-8, "capacity occupation coarse/fine stability")
check(float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))) < 2e-7, "complete current coarse/fine stability")
check(float(np.max(np.sum(np.abs(history_residual), axis=1))) < 2e-7, "all eight complete transport ledgers")
check(all(row["probe_ledger_residual_l1"] < 3e-7 for row in rows), "all four background-subtracted probe ledgers")
check(all(row["connector_delta_target_linf"] < 2e-8 for row in rows), "all 32 connector-vector components versus target")
check(all(row["complete_probe_delta_target_linf"] < 2e-8 for row in rows), "all 96 complete probe-current components versus target")
check(all(row["tau_target_abs_error"] < 3e-5 for row in rows), "all first-positive-peak times versus target")
check(all(row["peak_target_abs_error"] < 2e-8 for row in rows), "all first-positive-peak heights versus target")
check(all(row["tau_coarse_fine_abs"] < 5e-5 for row in rows), "first-positive-peak coarse/fine stability")
check(all(row["peak"] > PEAK_FLOOR for row in rows), "first peaks are positive above declared floor")
check(np.all(np.diff(capacities) < 0.0), "connector capacity strictly decreases N0 through N3")
check(not np.all(np.diff(taus) > 0.0) and taus[3] < taus[2], "operational latency is nonmonotone")
check(abs(fit_intercept - stored_fit["intercept"]) < 2e-8, "linear-fit intercept")
check(abs(fit_slope - stored_fit["slope_per_write"]) < 2e-8, "linear-fit slope")
check(abs(fit_r2 - stored_fit["r_squared"]) < 2e-7, "linear-fit R squared")
check(abs(fit_zero - stored_fit["zero_crossing"]) < 5e-6, "linear-fit formal zero")
check(fit_zero > 6.0 and stored_fit["finite_support_max_background_writes"] == 6, "formal zero lies beyond finite rail capacity")
check(stored_fit["N_crit_admissible"] is False and "N_CRIT_UNDEFINED" in stored_fit["status"], "Ncrit and pinch-off remain undefined")

target_prose = "\n".join((
    (TARGET_DIR / "README.md").read_text(),
    (TARGET_DIR / "RESULT.md").read_text(),
    (TARGET_DIR / "THEOREM.md").read_text(),
))
check(target["protocol"]["lineage_boundary"].endswith("NO_INDIVIDUAL_LINEAGE_TAG_AFTER_MIXING"), "machine result denies individual lineage tag")
check("Individual carrier lineage is not available" in target_prose and "background-subtracted" in target_prose, "prose preserves lineage/subtraction boundary")
check(target["interpretation"]["metric"].startswith("UNDEFINED") and target["interpretation"]["gravity"].startswith("NOT_INFERRED"), "machine result denies metric/gravity promotion")
check(all(term in target["not_claimed"] for term in ("INDIVIDUAL_LINEAGE_TRANSIT", "PHYSICAL_METRIC_STRAIN", "TIME_DILATION", "SHAPIRO_DELAY", "GRAVITY")), "forbidden promotions remain not claimed")
check("PINCH_OFF" in target["claim_classes"]["open"] and "GATE_R_C_AND_A_P" in target["claim_classes"]["open"], "pinch-off and gates remain open")
check("not a clock\nmetric" in target_prose and "not gravitational time dilation or\nShapiro delay" in target_prose, "operational tau is not promoted")

failures = [label for passed, label in checks if not passed]
elapsed = time.perf_counter() - started
rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes = int(rss_raw if sys.platform == "darwin" else rss_raw * 1024)

result = {
    "schema": "AUDIT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001",
    "status": "PASS_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "base_commit": "1c3e88e7b5c7792d83cdaa60f49995f3f92b0ee6",
    "scope": "FINITE_L8_ONLY__NO_LARGER_SUPPORT_EXECUTED",
    "target_and_antecedent_sha256": observed_hashes,
    "audit_script_sha256": sha256(Path(__file__)),
    "method": {
        "target": "ORDER_TEN_TAYLOR_PROPAGATION__1024_2048_STEPS",
        "audit": "UNITARY_FOURTH_ORDER_SUZUKI_YOSHIDA__THREE_COMMUTING_EDGE_MATCHINGS__SEPARATE_1024_2048_STEP_RUNS",
        "current_integration": "SEPARATE_NESTED_COMPOSITE_SIMPSON_RUNS_OVER_ZERO_TO_PI_OVER_TWO",
        "first_peak": "FIRST_POSITIVE_LOCAL_MAXIMUM_ABOVE_1E_8__THREE_POINT_PARABOLIC_VERTEX__ZERO_TO_TWO_PI",
    },
    "topology": {
        "sites": SITES,
        "edges": len(edges),
        "connectors": len(connector_indices),
        "degree_census": [len(row) for row in adjacency],
        "probe_target_graph_distance": distance[TARGET],
        "matching_edge_indices": [list(group) for group in matchings],
        "reachable_dimension": len(basis_words),
        "full_word_dimension": FULL_WORDS,
    },
    "authenticated_write_ledgers": write_ledgers,
    "history_controls": [
        {
            "label": label,
            "sources": list(sources[label]),
            "q_initial_sum": float(q_initial_sum[i]),
            "q_capacity_sum": float(np.sum(q_capacity[i])),
            "energy_initial": float(energy_initial[i]),
            "energy_capacity": float(energy_capacity[i]),
            "norm_capacity": float(capacity_norm[i]),
            "norm_search": float(search_norm[i]),
            "transport_ledger_residual_l1": float(np.sum(np.abs(history_residual[i]))),
        }
        for i, label in enumerate(labels)
    ],
    "rows": rows,
    "linear_fit": {
        "intercept": fit_intercept,
        "slope_per_write": fit_slope,
        "r_squared": fit_r2,
        "formal_zero": fit_zero,
        "finite_support_max_background_writes": 6,
        "Ncrit": "UNDEFINED__FORMAL_ZERO_OUTSIDE_FINITE_WRITE_CAPACITY",
        "pinch_off": "UNMEASURED",
    },
    "numerical_controls": {
        "capacity_norm_error_linf": float(np.max(np.abs(capacity_norm - 1.0))),
        "search_norm_error_linf": float(np.max(np.abs(search_norm - 1.0))),
        "capacity_energy_drift_linf": float(np.max(np.abs(energy_capacity - energy_initial))),
        "capacity_occupation_coarse_fine_linf": float(np.max(np.abs(q_capacity - q_capacity_coarse))),
        "capacity_current_coarse_fine_linf": float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))),
        "history_ledger_residual_l1_max": float(np.max(np.sum(np.abs(history_residual), axis=1))),
        "probe_ledger_residual_l1_max": max(row["probe_ledger_residual_l1"] for row in rows),
        "connector_target_linf_max": max(row["connector_delta_target_linf"] for row in rows),
        "complete_probe_current_target_linf_max": max(row["complete_probe_delta_target_linf"] for row in rows),
        "tau_target_abs_max": max(row["tau_target_abs_error"] for row in rows),
        "tau_coarse_fine_abs_max": max(row["tau_coarse_fine_abs"] for row in rows),
        "peak_target_abs_max": max(row["peak_target_abs_error"] for row in rows),
    },
    "conceptual_disposition": {
        "capacity": "STRICTLY_DECREASING_ONLY_ON_MEASURED_N0_TO_N3_WINDOW",
        "latency": "NONMONOTONE_OPERATIONAL_FIRST_POSITIVE_PEAK",
        "formal_zero": "8_POINT_6204_BEYOND_SIX_AVAILABLE_BACKGROUND_SITES__NO_NCRIT",
        "pinch_off": "UNDEFINED_AND_UNMEASURED",
        "lineage": "BACKGROUND_SUBTRACTION_ONLY__NO_INDIVIDUAL_TAG",
        "metric": "UNDEFINED__NO_STRAIN_TIME_DILATION_OR_SHAPIRO_PROMOTION",
        "gravity": "NOT_INFERRED",
    },
    "claim_classes": {
        "proved": "OWNER_ONCE_L8_PRISM_CENSUS__EXACT_AUTHENTICATED_TERMS_OFF_WRITE_LEDGERS__DECLARED_SUBTRACTION_IDENTITIES",
        "adopted": "F3_MDC_ALPHA_R0__CAPACITY_AND_SEARCH_WINDOWS__CANONICAL_CLUSTER__FIRST_PEAK_RULE",
        "conditional": "ALL_BLANK_PARENT__COMMON_WRITE_PHASE__BACKGROUND_SUBTRACTION__FINITE_NUMERICAL_REPRESENTATION",
        "empirical": "INDEPENDENT_FINITE_N0_TO_N3_CAPACITY_AND_TRANSIT_ROWS__MONOTONE_CAPACITY__NONMONOTONE_LATENCY__FORMAL_LINEAR_ZERO",
        "open": "OTHER_CLUSTERS_PHASES_RULES_WINDOWS__LARGER_N_AND_L__INDIVIDUAL_LINEAGE__PHYSICAL_METRIC_CLOCK__NCRIT__PINCH_OFF__GATE_R_C_AND_A_P",
    },
    "not_claimed": "INDIVIDUAL_LINEAGE_TRANSIT__CRITICAL_MASS__PINCH_OFF__METRIC_STRAIN__TIME_DILATION__SHAPIRO_DELAY__GRID__CONTINUUM__WARD__GRAVITY",
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
print(f"PASS__AUDIT_R_GATE_C_L8_ACCUMULATION_LATENCY__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={elapsed:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={rss_bytes}")
