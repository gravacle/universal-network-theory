#!/usr/bin/env python3
"""Bounded L8 accumulated-write connector-capacity and transit diagnostic."""

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
CAPACITY_TIME = math.pi / 2.0
SEARCH_TIME = 2.0 * math.pi
TAYLOR_ORDER = 10
COARSE_STEPS = 1024
FINE_STEPS = 2048
FIRST_PEAK_FLOOR = 1e-8
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = HERE / "RESULT.json"
STARTED = time.perf_counter()

ANTECEDENTS = {
    ROOT / "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "THEOREM.md":
        "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    ROOT / "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "INDEPENDENT_RESULT.json":
        "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json":
        "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
    ROOT / "AUDIT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "INDEPENDENT_RESULT.json":
        "5151b0deabf01ef0a7dc3dc604e6e638837df5537a01a0cc8361bf040e27091d",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_for(length: int):
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


def graph_distances(vertex_count: int, edges, source: int):
    neighbors = [set() for _ in range(vertex_count)]
    for u, v, _ in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    distance = [-1] * vertex_count
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                queue.append(v)
    return neighbors, distance


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
    """First positive local maximum, with a fixed three-point vertex rule."""
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
            return float(tau), float(peak), index
    raise AssertionError("no positive first-arrival peak in declared search window")


edges = edges_for(LENGTH)
neighbors, distances = graph_distances(SITES, edges, PROBE_SITE)
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
    background_label = f"B{accumulated_count}"
    probe_label = f"P{accumulated_count}"
    history_labels.extend((background_label, probe_label))
    history_sources[background_label] = background
    history_sources[probe_label] = (PROBE_SITE,) + background

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
    times = np.linspace(0.0, SEARCH_TIME, step_count + 1)
    if capacity_states is None:
        raise AssertionError("capacity state missing")
    return {
        "times": times,
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
    tau, first_peak, first_peak_index = first_positive_peak(fine["times"], signal)
    tau_coarse, first_peak_coarse, _ = first_positive_peak(coarse["times"], signal_coarse)
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
    rows.append({
        "N": accumulated_count,
        "accumulated_write_sites": list(BACKGROUND_SITES[:accumulated_count]),
        "probe_site": PROBE_SITE,
        "target_site": TARGET_SITE,
        "tau_first_positive_peak": tau,
        "tau_first_positive_peak_coarse": tau_coarse,
        "tau_refinement_abs": abs(tau - tau_coarse),
        "first_peak_incremental_target_occupation": first_peak,
        "first_peak_incremental_target_occupation_coarse": first_peak_coarse,
        "capacity_window": CAPACITY_TIME,
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
        "search_peak_index": first_peak_index,
    })

connector_values = np.array([row["J_connector_probe_delta_l1"] for row in rows])
tau_values = np.array([row["tau_first_positive_peak"] for row in rows])
connector_monotone = bool(np.all(np.diff(connector_values) < 0.0))
tau_monotone = bool(np.all(np.diff(tau_values) > 0.0))

# The linear zero is a predeclared finite-window diagnostic only. It is
# admissible as N_crit only when the measured capacity is strictly monotone,
# the fitted slope is negative, and the zero lies beyond the observed window.
design = np.column_stack((np.ones(4), np.arange(4, dtype=float)))
fit_coefficients, _, _, _ = np.linalg.lstsq(design, connector_values, rcond=None)
fit_intercept, fit_slope = (float(value) for value in fit_coefficients)
fit_prediction = design @ fit_coefficients
fit_r2 = float(1.0 - np.sum((connector_values - fit_prediction) ** 2)
               / np.sum((connector_values - np.mean(connector_values)) ** 2))
linear_zero = float(-fit_intercept / fit_slope) if fit_slope < 0.0 else None
finite_support_max_background_writes = LENGTH - 2
ncrit_admissible = bool(
    connector_monotone
    and linear_zero is not None
    and linear_zero > 3.0
    and linear_zero <= finite_support_max_background_writes
)

capacity_norms = np.sum(np.abs(fine["capacity_states"]) ** 2, axis=0)
search_norms = np.sum(np.abs(fine["search_states"]) ** 2, axis=0)
h_initial = h_action(initial)
h_capacity = h_action(fine["capacity_states"])
energy_initial = np.array([
    np.vdot(initial[:, index], h_initial[:, index]).real
    for index in range(initial.shape[1])
])
energy_capacity = np.array([
    np.vdot(fine["capacity_states"][:, index], h_capacity[:, index]).real
    for index in range(initial.shape[1])
])

antecedent_hashes = {str(path.relative_to(ROOT)): digest(path) for path in ANTECEDENTS}
expected_hashes = {str(path.relative_to(ROOT)): expected for path, expected in ANTECEDENTS.items()}
checks = [
    (antecedent_hashes == expected_hashes, "immutable antecedent hashes"),
    (len(edges) == 24 and len(connector_indices) == 8, "owner-once edge census"),
    (all(len(item) == 3 for item in neighbors), "degree-three L8 prism"),
    (distances[TARGET_SITE] == 4, "rail endpoint graph distance"),
    (BACKGROUND_SITES == (1, 2, 3), "adjacent accumulation cluster"),
    (dimension == sum(math.comb(SITES, count) for count in range(MAX_PARTICLES + 1)) == 2517, "complete reachable sector census"),
    (float(np.max(np.abs(capacity_norms - 1.0))) < 2e-12, "capacity-window norms"),
    (float(np.max(np.abs(search_norms - 1.0))) < 5e-12, "search-window norms"),
    (float(np.max(np.abs(energy_capacity - energy_initial))) < 2e-11, "capacity-window energy conservation"),
    (float(np.max(np.abs(q_capacity - q_capacity_coarse))) < 2e-9, "capacity occupation refinement"),
    (float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))) < 2e-8, "complete current refinement"),
    (float(np.max(np.sum(np.abs(history_residuals), axis=1))) < 2e-8, "all capacity history ledgers"),
    (all(row["probe_ledger_residual_l1"] < 2e-8 for row in rows), "all probe differential ledgers"),
    (all(row["tau_refinement_abs"] < 0.01 for row in rows), "transit-time refinement"),
    (all(row["first_peak_incremental_target_occupation"] > FIRST_PEAK_FLOOR for row in rows), "positive first-arrival peaks"),
    (all(row["J_connector_probe_delta_l1"] > 1e-8 for row in rows), "nonzero probe connector response"),
    (np.all(np.isfinite(connector_values)) and np.all(np.isfinite(tau_values)), "finite diagnostics"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "R_GATE_C_L8_ACCUMULATION_LATENCY_V001",
    "classification": "FINITE_L8_OPERATIONAL_CONNECTOR_CAPACITY_AND_FIRST_ARRIVAL_DIAGNOSTIC",
    "status": "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "antecedent_sha256": antecedent_hashes,
    "topology": {
        "description": "OWNER_ONCE_DEGREE_THREE_L8_PRISM__TWO_EIGHT_NODE_RAILS_PLUS_EIGHT_CONNECTORS",
        "sites": SITES,
        "edges": len(edges),
        "connectors": len(connector_indices),
        "probe_to_target_graph_distance": distances[TARGET_SITE],
        "coordinate_status": "FINITE_SUPPORT_LABELS_ONLY__NOT_A_PHYSICAL_METRIC_OR_GRID",
    },
    "protocol": {
        "parent": "ALL_BLANK_CONDITIONAL_VACUUM_ON_THE_AUDITED_OWNER_ONCE_L8_PRISM",
        "probe": "AUTHENTICATED_W_R_ONE_HALF_AT_RAIL_1_NODE_0",
        "accumulation": "N_AUTHENTICATED_W_R_ONE_HALF_WRITES_AT_ADJACENT_RAIL_1_NODES_1_THROUGH_N",
        "target": "RAIL_1_NODE_4",
        "lineage_boundary": "PROBE_IS_BACKGROUND_SUBTRACTION__NO_INDIVIDUAL_LINEAGE_TAG_AFTER_MIXING",
        "transit_observable": "FIRST_POSITIVE_LOCAL_MAXIMUM_OF_Q_TARGET_BACKGROUND_PLUS_PROBE_MINUS_Q_TARGET_BACKGROUND",
        "transit_search_window": SEARCH_TIME,
        "first_peak_floor": FIRST_PEAK_FLOOR,
        "connector_capacity_observable": "L1_OF_BACKGROUND_SUBTRACTED_TIME_INTEGRATED_CONNECTOR_CURRENT_VECTOR",
        "connector_capacity_window": CAPACITY_TIME,
        "signed_connector_sum_retained": True,
    },
    "parameters": {
        "L": LENGTH,
        "kappa_capacity": CAPACITY_TIME,
        "kappa_search": SEARCH_TIME,
        "taylor_order": TAYLOR_ORDER,
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
        "r0": "14441248/6075",
        "phi": "pi/4",
        "W_R_each": "1/2",
        "full_word_dimension": FULL_DIMENSION,
        "complete_reachable_sector_dimension": dimension,
    },
    "rows": rows,
    "trend_screen": {
        "connector_capacity_strictly_decreases_N0_to_N3": connector_monotone,
        "transit_time_strictly_increases_N0_to_N3": tau_monotone,
        "linear_capacity_fit": {
            "intercept": fit_intercept,
            "slope_per_write": fit_slope,
            "r_squared": fit_r2,
            "zero_crossing": linear_zero,
            "finite_support_max_background_writes": finite_support_max_background_writes,
            "N_crit_admissible": ncrit_admissible,
            "status": (
                "FINITE_WINDOW_LINEAR_ZERO_DIAGNOSTIC_ONLY" if ncrit_admissible
                else "N_CRIT_UNDEFINED__LINEAR_ZERO_OUTSIDE_FINITE_L8_WRITE_CAPACITY_OR_MONOTONE_DEPLETION_NOT_ESTABLISHED"
            ),
        },
    },
    "numerical_controls": {
        "capacity_norm_error_max": float(np.max(np.abs(capacity_norms - 1.0))),
        "search_norm_error_max": float(np.max(np.abs(search_norms - 1.0))),
        "capacity_energy_error_max": float(np.max(np.abs(energy_capacity - energy_initial))),
        "capacity_occupation_refinement_linf": float(np.max(np.abs(q_capacity - q_capacity_coarse))),
        "capacity_current_refinement_linf": float(np.max(np.abs(fine["capacity_currents"] - coarse["capacity_currents"]))),
        "history_ledger_residual_l1_max": float(np.max(np.sum(np.abs(history_residuals), axis=1))),
        "transit_time_refinement_abs_max": float(max(row["tau_refinement_abs"] for row in rows)),
    },
    "interpretation": {
        "capacity": (
            "MONOTONE_DEPLETION_OBSERVED_ON_N0_TO_N3" if connector_monotone
            else "MONOTONE_DEPLETION_NOT_OBSERVED_ON_N0_TO_N3"
        ),
        "latency": (
            "MONOTONE_OPERATIONAL_DELAY_OBSERVED_ON_N0_TO_N3" if tau_monotone
            else "MONOTONE_OPERATIONAL_DELAY_NOT_OBSERVED_ON_N0_TO_N3"
        ),
        "metric": "UNDEFINED__FINITE_GRAPH_FIRST_ARRIVAL_ONLY",
        "gravity": "NOT_INFERRED__NO_PHYSICAL_CLOCK_METRIC_OR_GEODESIC_MAP",
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "claim_classes": {
        "proved": "OWNER_ONCE_L8_PRISM_CENSUS__AUTHENTICATED_TERMS_OFF_WRITE_LEDGERS__DECLARED_OPERATIONAL_OBSERVABLES",
        "adopted": "F3_MDC_ALPHA_R0__KAPPA_WINDOWS__CANONICAL_RAIL_CLUSTER__FIRST_PEAK_RULE",
        "conditional": "ALL_BLANK_PARENT__COMMON_WRITE_PHASE__BACKGROUND_SUBTRACTION__NUMERICAL_EVOLUTION",
        "empirical": "FINITE_N0_TO_N3_CONNECTOR_AND_TRANSIT_ROWS",
        "open": "INDEPENDENT_HOSTILE_AUDIT__OTHER_CLUSTERS_PHASES_AND_ARRIVAL_RULES__LARGER_N_AND_L__PHYSICAL_METRIC_CLOCK__PINCH_OFF__GATE_R_C_AND_A_P",
    },
    "not_claimed": "INDIVIDUAL_LINEAGE_TRANSIT__CRITICAL_MASS_WITHOUT_ADMISSIBLE_FIT__PHYSICAL_METRIC_STRAIN__TIME_DILATION__SHAPIRO_DELAY__GRID__CONTINUUM__WARD__GRAVITY",
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
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"WROTE_CANONICAL_RESULT={OUT}")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_GATE_C_L8_ACCUMULATION_LATENCY__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
