#!/usr/bin/env python3
"""L8 rail-wrap-removed topological control for Gate R-C."""

from __future__ import annotations

import hashlib
import json
import math
import os
import resource
import time
from collections import deque
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


LENGTH = 8
SITES = 2 * LENGTH
FULL_DIMENSION = 1 << SITES
MAX_PARTICLES = 4
PROBE_SITE = 0
TARGET_SITE = 4
BACKGROUND_SITES = (1, 2, 3)
REMOVED_EDGES = ((7, 0), (15, 8))
CAPACITY_TIME = math.pi / 2.0
SEARCH_TIME = 2.0 * math.pi
FIRST_PEAK_FLOOR = 1e-8
TAYLOR_ORDER = 10
COARSE_STEPS = 1024
FINE_STEPS = 2048
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = HERE / "RESULT.json"
STARTED = time.perf_counter()

ANTECEDENTS = {
    ROOT / "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001" / "RESULT.json":
        "14eca704f5e1f65eeaf9cc04a0aa40a9f2dcd8f19ea7a440cf507fb0b76f3759",
    ROOT / "AUDIT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001" / "INDEPENDENT_RESULT.json":
        "748404604c97434221052272de9cb751e99749e20897fc35f93be7a0d296efde",
    ROOT / "DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001" / "RESULT.json":
        "e31019933d5465377710336935e2a3607c3185735b871a58f2475f6a7bf14926",
    ROOT / "AUDIT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001" / "INDEPENDENT_RESULT.json":
        "272c7c80a0eac374768367f1bb02f4cb989e6f64c0336d37223ee9b074133211",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def periodic_edges(length: int):
    result = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            result.append((
                offset + site,
                offset + (site + 1) % length,
                f"rail_{rail + 1}",
            ))
    for site in range(length):
        result.append((site, length + (site + 1) % length, "connector"))
    return result


def open_edges(length: int):
    return [
        edge for edge in periodic_edges(length)
        if edge[:2] not in REMOVED_EDGES
    ]


def graph_census(vertex_count: int, edges, source: int, target: int, blocked=()):
    blocked = set(blocked)
    adjacency = [set() for _ in range(vertex_count)]
    for u, v, _ in edges:
        if u not in blocked and v not in blocked:
            adjacency[u].add(v)
            adjacency[v].add(u)
    distance = [-1] * vertex_count
    path_count = [0] * vertex_count
    if source in blocked or target in blocked:
        return adjacency, distance, path_count
    distance[source] = 0
    path_count[source] = 1
    queue = deque([source])
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


def prepared_state(source_sites, basis_words, basis_index):
    """Product of authenticated (B-iX)/sqrt(2) writes on blank sites."""
    state = np.zeros(len(basis_words), dtype=np.complex128)
    source_sites = tuple(source_sites)
    scale = 2.0 ** (-0.5 * len(source_sites))
    for subset in range(1 << len(source_sites)):
        word = 0
        occupied = 0
        for index, site in enumerate(source_sites):
            if (subset >> index) & 1:
                word |= 1 << site
                occupied += 1
        state[basis_index[word]] = scale * ((-1j) ** occupied)
    return state


def first_positive_peak(times: np.ndarray, values: np.ndarray):
    for index in range(1, len(values) - 1):
        if (
            values[index] > FIRST_PEAK_FLOOR
            and values[index] > values[index - 1]
            and values[index] >= values[index + 1]
        ):
            denominator = values[index - 1] - 2.0 * values[index] + values[index + 1]
            offset = 0.0
            if denominator != 0.0:
                offset = 0.5 * (values[index - 1] - values[index + 1]) / denominator
                offset = min(0.5, max(-0.5, offset))
            step = times[1] - times[0]
            tau = times[index] + offset * step
            peak = values[index] - 0.25 * (
                values[index - 1] - values[index + 1]
            ) * offset
            return float(tau), float(peak), index, float(offset)
    raise AssertionError("no positive target-occupation peak in declared window")


edges_periodic = periodic_edges(LENGTH)
edges = open_edges(LENGTH)
adjacency, distance, path_count = graph_census(
    SITES, edges, PROBE_SITE, TARGET_SITE
)
_, distance_avoiding_cluster, path_count_avoiding_cluster = graph_census(
    SITES, edges, PROBE_SITE, TARGET_SITE, blocked=BACKGROUND_SITES
)
all_words = np.arange(FULL_DIMENSION, dtype=np.int64)
particle_number = np.array([bin(int(word)).count("1") for word in all_words])
basis_words = all_words[particle_number <= MAX_PARTICLES]
basis_index = {int(word): index for index, word in enumerate(basis_words)}
dimension = len(basis_words)

edge_actions = []
for u, v, kind in edges:
    bit_u = (basis_words >> u) & 1
    bit_v = (basis_words >> v) & 1
    active = np.flatnonzero(bit_u != bit_v)
    swapped_words = basis_words[active] ^ (1 << u) ^ (1 << v)
    swapped = np.array([basis_index[int(word)] for word in swapped_words], dtype=np.int64)
    coefficients = 1j * (bit_v[active] - bit_u[active])
    edge_actions.append((active, swapped, coefficients, kind))


def h_action(states: np.ndarray) -> np.ndarray:
    out = np.zeros_like(states)
    for active, swapped, _, _ in edge_actions:
        out[active, :] -= states[swapped, :]
    return out


def current_expectations(states: np.ndarray) -> np.ndarray:
    result = np.empty((states.shape[1], len(edges)), dtype=float)
    for edge_index, (active, swapped, coefficients, _) in enumerate(edge_actions):
        result[:, edge_index] = np.sum(
            np.conjugate(states[active, :])
            * coefficients[:, None]
            * states[swapped, :],
            axis=0,
        ).real
    return result


def taylor_step(states: np.ndarray, step: float) -> np.ndarray:
    updated = states.copy()
    term = states.copy()
    for order in range(1, TAYLOR_ORDER + 1):
        term = (-1j * step / order) * h_action(term)
        updated += term
    return updated


history_labels = []
history_sources = {}
for accumulated_count in range(4):
    background = BACKGROUND_SITES[:accumulated_count]
    history_labels.extend((f"B{accumulated_count}", f"P{accumulated_count}"))
    history_sources[f"B{accumulated_count}"] = background
    history_sources[f"P{accumulated_count}"] = (PROBE_SITE,) + background

initial = np.column_stack([
    prepared_state(history_sources[label], basis_words, basis_index)
    for label in history_labels
])
label_index = {label: index for index, label in enumerate(history_labels)}
target_bits = ((basis_words >> TARGET_SITE) & 1).astype(float)
all_site_bits = np.array([
    ((basis_words >> site) & 1).astype(float) for site in range(SITES)
])


def occupations(states: np.ndarray):
    probabilities = np.abs(states) ** 2
    return np.einsum("sw,wh->hs", all_site_bits, probabilities, optimize=False)


def target_occupations(states: np.ndarray):
    probabilities = np.abs(states) ** 2
    return np.einsum("w,wh->h", target_bits, probabilities, optimize=False)


def evolve(step_count: int):
    step = SEARCH_TIME / step_count
    capacity_index = int(round(CAPACITY_TIME / step))
    if capacity_index % 2 or abs(capacity_index * step - CAPACITY_TIME) > 1e-14:
        raise AssertionError("capacity endpoint must be an even Simpson index")
    states = initial.copy()
    target_trace = np.empty((step_count + 1, initial.shape[1]), dtype=float)
    target_trace[0] = target_occupations(states)
    current_integral = current_expectations(states)
    capacity_states = None
    for index in range(1, step_count + 1):
        states = taylor_step(states, step)
        target_trace[index] = target_occupations(states)
        if index <= capacity_index:
            weight = 1.0 if index == capacity_index else (4.0 if index % 2 else 2.0)
            current_integral += weight * current_expectations(states)
            if index == capacity_index:
                capacity_states = states.copy()
    current_integral *= step / 3.0
    if capacity_states is None:
        raise AssertionError("capacity state missing")
    return {
        "times": np.linspace(0.0, SEARCH_TIME, step_count + 1),
        "target_trace": target_trace,
        "capacity_states": capacity_states,
        "capacity_currents": current_integral,
        "search_states": states,
    }


coarse = evolve(COARSE_STEPS)
fine = evolve(FINE_STEPS)
q_initial = occupations(initial)
q_capacity = occupations(fine["capacity_states"])
q_capacity_coarse = occupations(coarse["capacity_states"])

incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0
history_residuals = q_capacity - q_initial + np.einsum(
    "he,se->hs", fine["capacity_currents"], incidence, optimize=False
)
connector_indices = [index for index, edge in enumerate(edges) if edge[2] == "connector"]

periodic_result = json.loads(
    (ROOT / "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001" / "RESULT.json").read_text()
)
periodic_rows = {row["N"]: row for row in periodic_result["rows"]}
rows = []
for accumulated_count in range(4):
    background_index = label_index[f"B{accumulated_count}"]
    probe_index = label_index[f"P{accumulated_count}"]
    signal = (
        fine["target_trace"][:, probe_index]
        - fine["target_trace"][:, background_index]
    )
    signal_coarse = (
        coarse["target_trace"][:, probe_index]
        - coarse["target_trace"][:, background_index]
    )
    tau, first_peak, first_peak_index, first_peak_offset = first_positive_peak(
        fine["times"], signal
    )
    tau_coarse, first_peak_coarse, _, _ = first_positive_peak(
        coarse["times"], signal_coarse
    )
    delta_current = (
        fine["capacity_currents"][probe_index]
        - fine["capacity_currents"][background_index]
    )
    delta_current_coarse = (
        coarse["capacity_currents"][probe_index]
        - coarse["capacity_currents"][background_index]
    )
    delta_q_capacity = q_capacity[probe_index] - q_capacity[background_index]
    source_vector = np.zeros(SITES)
    source_vector[PROBE_SITE] = 0.5
    probe_ledger = delta_q_capacity + incidence @ delta_current - source_vector
    connector_delta = delta_current[connector_indices]
    periodic_row = periodic_rows[accumulated_count]
    rows.append({
        "N": accumulated_count,
        "accumulated_write_sites": list(BACKGROUND_SITES[:accumulated_count]),
        "tau_open": tau,
        "tau_open_coarse": tau_coarse,
        "tau_refinement_abs": abs(tau - tau_coarse),
        "first_peak_delta_q4": first_peak,
        "first_peak_delta_q4_coarse": first_peak_coarse,
        "peak_amplitude_refinement_abs": abs(first_peak - first_peak_coarse),
        "fine_peak_index": first_peak_index,
        "fine_peak_offset": first_peak_offset,
        "periodic_tau": periodic_row["tau_first_positive_peak"],
        "open_minus_periodic_tau": tau - periodic_row["tau_first_positive_peak"],
        "J_connector_probe_delta_l1": float(np.sum(np.abs(connector_delta))),
        "J_connector_probe_delta_signed": float(np.sum(connector_delta)),
        "J_connector_probe_delta_vector": [float(value) for value in connector_delta],
        "J_connector_background_l1": float(np.sum(np.abs(
            fine["capacity_currents"][background_index, connector_indices]
        ))),
        "J_connector_probe_plus_background_l1": float(np.sum(np.abs(
            fine["capacity_currents"][probe_index, connector_indices]
        ))),
        "complete_probe_delta_current": [float(value) for value in delta_current],
        "current_refinement_linf": float(np.max(np.abs(delta_current - delta_current_coarse))),
        "probe_ledger_residual_l1": float(np.sum(np.abs(probe_ledger))),
        "probe_ledger_residual_linf": float(np.max(np.abs(probe_ledger))),
    })

tau_values = np.array([row["tau_open"] for row in rows])
connector_values = np.array([row["J_connector_probe_delta_l1"] for row in rows])
tau_strictly_increasing = bool(np.all(np.diff(tau_values) > 0.0))
inversion_3_lt_2 = bool(tau_values[3] < tau_values[2])
connector_strictly_decreasing = bool(np.all(np.diff(connector_values) < 0.0))
if inversion_3_lt_2:
    topology_classification = (
        "INVERSION_PERSISTS_WITH_BOTH_PERIODIC_RAIL_WRAP_EDGES_REMOVED__"
        "NOT_PERIODIC_RAIL_WRAP_MEDIATED__FINITE_OPEN_SUPPORT_MODE_REORGANIZATION"
    )
elif tau_strictly_increasing:
    topology_classification = (
        "INVERSION_DISAPPEARS_WITH_PERIODIC_RAIL_WRAP_EDGES_REMOVED__"
        "RING_MEDIATED_IN_DECLARED_PERIODIC_VERSUS_OPEN_COMPARISON"
    )
else:
    topology_classification = (
        "N3_N2_INVERSION_DISAPPEARS_BUT_OTHER_NONMONOTONICITY_REMAINS__"
        "BINARY_CLASSIFICATION_UNRESOLVED"
    )

capacity_norms = np.sum(np.abs(fine["capacity_states"]) ** 2, axis=0)
search_norms = np.sum(np.abs(fine["search_states"]) ** 2, axis=0)
energy_initial = np.sum(np.conjugate(initial) * h_action(initial), axis=0).real
energy_capacity = np.sum(
    np.conjugate(fine["capacity_states"]) * h_action(fine["capacity_states"]), axis=0
).real
number_capacity = np.sum(
    np.abs(fine["capacity_states"]) ** 2 * particle_number[basis_words, None], axis=0
)
number_expected = np.array([len(history_sources[label]) / 2.0 for label in history_labels])

antecedent_hashes = {str(path.relative_to(ROOT)): digest(path) for path in ANTECEDENTS}
expected_hashes = {str(path.relative_to(ROOT)): expected for path, expected in ANTECEDENTS.items()}
degree_census = [len(neighbors) for neighbors in adjacency]
checks = [
    (antecedent_hashes == expected_hashes, "immutable audited antecedent hashes"),
    (len(edges_periodic) == 24 and len(edges) == 22, "exact two-edge decoupling"),
    (all(edge not in edges for edge in ((7, 0, "rail_1"), (15, 8, "rail_2"))), "both rail wraps absent"),
    (set(edges_periodic) - set(edges) == {(7, 0, "rail_1"), (15, 8, "rail_2")}, "no other owner edge changed"),
    (len(connector_indices) == 8, "all connector owners retained"),
    (degree_census.count(2) == 4 and degree_census.count(3) == 12, "open-support degree census"),
    (distance[TARGET_SITE] == 4 and path_count[TARGET_SITE] == 1, "unique shortest forward path length four"),
    (distance_avoiding_cluster[TARGET_SITE] == 6 and path_count_avoiding_cluster[TARGET_SITE] == 2, "retained longer connector-rail bypass census"),
    (dimension == sum(math.comb(SITES, count) for count in range(5)) == 2517, "complete reachable sector census"),
    (float(np.max(np.abs(capacity_norms - 1.0))) < 3e-12, "capacity norms"),
    (float(np.max(np.abs(search_norms - 1.0))) < 7e-12, "search norms"),
    (float(np.max(np.abs(energy_capacity - energy_initial))) < 3e-11, "capacity energy conservation"),
    (float(np.max(np.abs(number_capacity - number_expected))) < 3e-11, "capacity retained-number conservation"),
    (float(np.max(np.abs(q_capacity - q_capacity_coarse))) < 2e-9, "capacity occupation refinement"),
    (float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))) < 2e-8, "complete current refinement"),
    (float(np.max(np.sum(np.abs(history_residuals), axis=1))) < 2e-8, "all complete history ledgers"),
    (all(row["probe_ledger_residual_l1"] < 2e-8 for row in rows), "all probe differential ledgers"),
    (all(row["tau_refinement_abs"] < 0.01 for row in rows), "open-arrival time refinement"),
    (all(row["peak_amplitude_refinement_abs"] < 2e-6 for row in rows), "open-arrival amplitude refinement"),
    (all(row["first_peak_delta_q4"] > FIRST_PEAK_FLOOR for row in rows), "positive open-arrival peaks"),
    (np.all(np.isfinite(tau_values)) and np.all(np.isfinite(connector_values)), "finite diagnostics"),
]
failures = [label for passed, label in checks if not passed]

result = {
    "schema": "R_GATE_C_L8_OPEN_LADDER_CONTROL_V001",
    "classification": "FINITE_L8_PERIODIC_RAIL_WRAP_REMOVAL_CONTROL",
    "status": "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "antecedent_sha256": antecedent_hashes,
    "topology": {
        "periodic_edges": len(edges_periodic),
        "open_edges": len(edges),
        "removed_owner_edges": [list(edge) for edge in ((7, 0, "rail_1"), (15, 8, "rail_2"))],
        "retained_connectors": len(connector_indices),
        "degree_census": degree_census,
        "probe_target_distance": distance[TARGET_SITE],
        "probe_target_shortest_path_count": path_count[TARGET_SITE],
        "distance_avoiding_nodes_1_2_3": distance_avoiding_cluster[TARGET_SITE],
        "shortest_path_count_avoiding_nodes_1_2_3": path_count_avoiding_cluster[TARGET_SITE],
        "path_boundary": "PERIODIC_RAIL_WRAP_REMOVED__TWO_LONGER_SECOND_RAIL_OR_CONNECTOR_PATHS_REMAIN",
    },
    "protocol": {
        "selected_control": "OPTION_B_LITERAL_REMOVAL_OF_RAIL_EDGES_7_TO_0_AND_15_TO_8",
        "parent": "ALL_BLANK_CONDITIONAL_PARENT",
        "probe": "AUTHENTICATED_W_R_ONE_HALF_AT_RAIL_1_NODE_0",
        "background": "N_AUTHENTICATED_W_R_ONE_HALF_WRITES_AT_RAIL_1_NODES_1_THROUGH_N",
        "target": "RAIL_1_NODE_4",
        "arrival_observable": "BACKGROUND_SUBTRACTED_TARGET_OCCUPATION_Q4",
        "tau_open": "FIRST_POSITIVE_LOCAL_MAXIMUM_ABOVE_1E_8_ON_ZERO_TO_TWO_PI__THREE_POINT_PARABOLIC_VERTEX",
        "connector_observable": "L1_OF_BACKGROUND_SUBTRACTED_INTEGRATED_CONNECTOR_CURRENT_VECTOR_ON_ZERO_TO_PI_OVER_TWO",
        "lineage_boundary": "ENSEMBLE_BACKGROUND_SUBTRACTION__NO_INDIVIDUAL_CARRIER_TAG",
    },
    "parameters": {
        "L": LENGTH,
        "capacity_window": CAPACITY_TIME,
        "search_window": SEARCH_TIME,
        "first_peak_floor": FIRST_PEAK_FLOOR,
        "taylor_order": TAYLOR_ORDER,
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
        "W_R_each": "1/2",
        "full_word_dimension": FULL_DIMENSION,
        "complete_reachable_sector_dimension": dimension,
    },
    "rows": rows,
    "trend_screen": {
        "tau_open_strictly_increases_N0_to_N3": tau_strictly_increasing,
        "tau_open_3_less_than_tau_open_2": inversion_3_lt_2,
        "connector_l1_strictly_decreases_N0_to_N3": connector_strictly_decreasing,
        "topology_classification": topology_classification,
    },
    "numerical_controls": {
        "capacity_norm_error_linf": float(np.max(np.abs(capacity_norms - 1.0))),
        "search_norm_error_linf": float(np.max(np.abs(search_norms - 1.0))),
        "capacity_energy_drift_linf": float(np.max(np.abs(energy_capacity - energy_initial))),
        "capacity_number_error_linf": float(np.max(np.abs(number_capacity - number_expected))),
        "capacity_occupation_refinement_linf": float(np.max(np.abs(q_capacity - q_capacity_coarse))),
        "capacity_current_refinement_linf": float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))),
        "history_ledger_residual_l1_max": float(np.max(np.sum(np.abs(history_residuals), axis=1))),
        "tau_refinement_abs_max": max(row["tau_refinement_abs"] for row in rows),
        "peak_amplitude_refinement_abs_max": max(row["peak_amplitude_refinement_abs"] for row in rows),
    },
    "claim_classes": {
        "proved": "EXACT_TWO_OWNER_EDGE_REMOVAL__OPEN_SUPPORT_CENSUS__AUTHENTICATED_WRITE_LEDGERS__OWNER_ONCE_CONTINUITY",
        "adopted": "OPTION_B_LITERAL_RAIL_WRAP_REMOVAL__COMMON_PHASE__BACKGROUND_SUBTRACTION__WINDOWS__FIRST_PEAK_RULE",
        "conditional": "ALL_BLANK_PARENT__FINITE_SOLVER__ENSEMBLE_DIFFERENCE",
        "empirical": "FINITE_N0_TO_N3_OPEN_ARRIVAL_AND_CONNECTOR_ROWS__TOPOLOGY_COMPARISON",
        "open": "INDEPENDENT_HOSTILE_AUDIT__OTHER_BOUNDARY_CUTS_CONNECTOR_PATTERNS_PHASES_AND_WINDOWS__INDIVIDUAL_LINEAGE__GATE_R_C_AND_A_P",
    },
    "not_claimed": "UNIQUE_ALL_HISTORY_ROUTE__INDIVIDUAL_LINEAGE__METRIC_TIME_DILATION__SHAPIRO_DELAY__MACROSCOPIC_GRAVITATIONAL_EMERGENCE__GRAVITY",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
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
            raise AssertionError(f"canonical float differs at {path}: {observed} != {canonical}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}: {observed} != {canonical}")


if OUT.exists():
    compatible(result, json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"WROTE_CANONICAL_RESULT={OUT}")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_GATE_C_L8_OPEN_LADDER_CONTROL__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
