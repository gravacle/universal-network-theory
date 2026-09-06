#!/usr/bin/env python3
"""Option-A L8 forward-edge arrival control for the Gate R-C screen."""

from __future__ import annotations

import hashlib
import json
import math
import os
import resource
import time
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
FORWARD_EDGE = (3, 4)
BACKGROUND_SITES = (1, 2, 3)
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
    ROOT / "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "THEOREM.md":
        "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    ROOT / "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "INDEPENDENT_RESULT.json":
        "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    ROOT / "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001" / "RESULT.json":
        "14eca704f5e1f65eeaf9cc04a0aa40a9f2dcd8f19ea7a440cf507fb0b76f3759",
    ROOT / "AUDIT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001" / "INDEPENDENT_RESULT.json":
        "748404604c97434221052272de9cb751e99749e20897fc35f93be7a0d296efde",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prism_edges(length: int):
    edges = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((
                offset + site,
                offset + (site + 1) % length,
                f"rail_{rail + 1}",
            ))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


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


def parabolic_peak(times: np.ndarray, values: np.ndarray):
    """First positive local maximum and its fractional sample coordinate."""
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
    raise AssertionError("no positive directed-current peak in declared window")


def quadratic_value(values: np.ndarray, index: int, offset: float) -> float:
    """Evaluate the local three-point quadratic at a fractional index."""
    center = values[index]
    slope = 0.5 * (values[index + 1] - values[index - 1])
    curvature = 0.5 * (values[index + 1] - 2.0 * center + values[index - 1])
    return float(center + offset * slope + offset * offset * curvature)


edges = prism_edges(LENGTH)
forward_edge_index = edges.index((FORWARD_EDGE[0], FORWARD_EDGE[1], "rail_1"))
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


def edge_current(states: np.ndarray, edge_index: int) -> np.ndarray:
    active, swapped, coefficients, _ = edge_actions[edge_index]
    return np.sum(
        np.conjugate(states[active, :])
        * coefficients[:, None]
        * states[swapped, :],
        axis=0,
    ).real


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


def target_occupations(states: np.ndarray) -> np.ndarray:
    probabilities = np.abs(states) ** 2
    return np.einsum("w,wh->h", target_bits, probabilities, optimize=False)


def evolve(step_count: int):
    step = SEARCH_TIME / step_count
    states = initial.copy()
    current_trace = np.empty((step_count + 1, initial.shape[1]), dtype=float)
    target_trace = np.empty_like(current_trace)
    current_trace[0] = edge_current(states, forward_edge_index)
    target_trace[0] = target_occupations(states)
    for index in range(1, step_count + 1):
        states = taylor_step(states, step)
        current_trace[index] = edge_current(states, forward_edge_index)
        target_trace[index] = target_occupations(states)
    return {
        "times": np.linspace(0.0, SEARCH_TIME, step_count + 1),
        "current_trace": current_trace,
        "target_trace": target_trace,
        "final_states": states,
    }


coarse = evolve(COARSE_STEPS)
fine = evolve(FINE_STEPS)
rows = []
for accumulated_count in range(4):
    background_index = label_index[f"B{accumulated_count}"]
    probe_index = label_index[f"P{accumulated_count}"]
    forward_signal = (
        fine["current_trace"][:, probe_index]
        - fine["current_trace"][:, background_index]
    )
    forward_signal_coarse = (
        coarse["current_trace"][:, probe_index]
        - coarse["current_trace"][:, background_index]
    )
    occupation_signal = (
        fine["target_trace"][:, probe_index]
        - fine["target_trace"][:, background_index]
    )
    occupation_signal_coarse = (
        coarse["target_trace"][:, probe_index]
        - coarse["target_trace"][:, background_index]
    )
    tau, current_peak, peak_index, offset = parabolic_peak(
        fine["times"], forward_signal
    )
    tau_coarse, current_peak_coarse, coarse_index, coarse_offset = parabolic_peak(
        coarse["times"], forward_signal_coarse
    )
    target_amplitude = quadratic_value(occupation_signal, peak_index, offset)
    target_amplitude_coarse = quadratic_value(
        occupation_signal_coarse, coarse_index, coarse_offset
    )
    rows.append({
        "N": accumulated_count,
        "accumulated_write_sites": list(BACKGROUND_SITES[:accumulated_count]),
        "probe_site": PROBE_SITE,
        "forward_edge": list(FORWARD_EDGE),
        "target_site": TARGET_SITE,
        "tau_fwd": tau,
        "tau_fwd_coarse": tau_coarse,
        "tau_refinement_abs": abs(tau - tau_coarse),
        "peak_delta_J_3_to_4": current_peak,
        "peak_delta_J_3_to_4_coarse": current_peak_coarse,
        "peak_current_refinement_abs": abs(current_peak - current_peak_coarse),
        "delta_q4_at_tau_fwd": target_amplitude,
        "delta_q4_at_tau_fwd_coarse": target_amplitude_coarse,
        "target_amplitude_refinement_abs": abs(target_amplitude - target_amplitude_coarse),
        "fine_peak_index": peak_index,
        "fine_peak_offset": offset,
    })

tau_values = np.array([row["tau_fwd"] for row in rows])
tau_strictly_increasing = bool(np.all(np.diff(tau_values) > 0.0))
fine_norms = np.sum(np.abs(fine["final_states"]) ** 2, axis=0)
coarse_norms = np.sum(np.abs(coarse["final_states"]) ** 2, axis=0)
fine_energies = np.sum(
    np.conjugate(fine["final_states"]) * h_action(fine["final_states"]), axis=0
).real
initial_energies = np.sum(np.conjugate(initial) * h_action(initial), axis=0).real
fine_numbers = np.sum(
    np.abs(fine["final_states"]) ** 2 * particle_number[basis_words, None], axis=0
)
expected_numbers = np.array([len(history_sources[label]) / 2.0 for label in history_labels])

antecedent_hashes = {str(path.relative_to(ROOT)): digest(path) for path in ANTECEDENTS}
expected_hashes = {str(path.relative_to(ROOT)): expected for path, expected in ANTECEDENTS.items()}
checks = [
    (antecedent_hashes == expected_hashes, "immutable audited antecedent hashes"),
    (len(edges) == 24, "owner-once edge census"),
    (forward_edge_index == 3 and edges[forward_edge_index] == (3, 4, "rail_1"), "directed forward-edge custody"),
    (dimension == sum(math.comb(SITES, count) for count in range(5)) == 2517, "complete reachable sector census"),
    (history_sources["P3"] == (0, 1, 2, 3), "declared forward-sector accumulation cluster"),
    (float(np.max(np.abs(fine_norms - 1.0))) < 6e-12, "fine final norms"),
    (float(np.max(np.abs(coarse_norms - 1.0))) < 6e-12, "coarse final norms"),
    (float(np.max(np.abs(fine_energies - initial_energies))) < 3e-11, "fine energy conservation"),
    (float(np.max(np.abs(fine_numbers - expected_numbers))) < 3e-11, "fine retained-number conservation"),
    (all(row["tau_refinement_abs"] < 0.01 for row in rows), "forward-arrival time refinement"),
    (all(row["peak_current_refinement_abs"] < 2e-6 for row in rows), "forward-current peak refinement"),
    (all(row["target_amplitude_refinement_abs"] < 2e-6 for row in rows), "target-amplitude refinement"),
    (all(row["peak_delta_J_3_to_4"] > FIRST_PEAK_FLOOR for row in rows), "positive forward-current peaks"),
    (np.all(np.isfinite(tau_values)), "finite forward-arrival times"),
]
failures = [label for passed, label in checks if not passed]

result = {
    "schema": "R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001",
    "classification": "FINITE_L8_OPTION_A_BACKGROUND_SUBTRACTED_DIRECTED_EDGE_CURRENT_CONTROL",
    "status": "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "antecedent_sha256": antecedent_hashes,
    "topology": {
        "description": "UNCHANGED_AUDITED_OWNER_ONCE_DEGREE_THREE_L8_PRISM",
        "sites": SITES,
        "edges": len(edges),
        "forward_edge": list(FORWARD_EDGE),
        "forward_edge_index": forward_edge_index,
        "wraparound_edges_retained": True,
    },
    "protocol": {
        "selected_control": "OPTION_A_DIRECTIONAL_INFLOW",
        "parent": "ALL_BLANK_CONDITIONAL_PARENT",
        "probe": "AUTHENTICATED_W_R_ONE_HALF_AT_RAIL_1_NODE_0",
        "background": "N_AUTHENTICATED_W_R_ONE_HALF_WRITES_AT_RAIL_1_NODES_1_THROUGH_N",
        "observable": "BACKGROUND_SUBTRACTED_INSTANTANEOUS_DIRECTED_CURRENT_J_3_TO_4",
        "tau_fwd": "FIRST_POSITIVE_LOCAL_MAXIMUM_ABOVE_1E_8_ON_ZERO_TO_TWO_PI__THREE_POINT_PARABOLIC_VERTEX",
        "forward_arrival_amplitude": "PEAK_DELTA_J_3_TO_4_AND_BACKGROUND_SUBTRACTED_Q4_EVALUATED_AT_TAU_FWD",
        "lineage_boundary": "ENSEMBLE_BACKGROUND_SUBTRACTION__NO_INDIVIDUAL_CARRIER_TAG",
    },
    "parameters": {
        "L": LENGTH,
        "search_window": SEARCH_TIME,
        "first_peak_floor": FIRST_PEAK_FLOOR,
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
        "tau_fwd_strictly_increases_N0_to_N3": tau_strictly_increasing,
        "status": (
            "STRICT_MONOTONE_FORWARD_EDGE_DELAY_OBSERVED_ON_N0_TO_N3"
            if tau_strictly_increasing
            else "STRICT_MONOTONE_FORWARD_EDGE_DELAY_NOT_OBSERVED_ON_N0_TO_N3"
        ),
    },
    "numerical_controls": {
        "fine_norm_error_linf": float(np.max(np.abs(fine_norms - 1.0))),
        "coarse_norm_error_linf": float(np.max(np.abs(coarse_norms - 1.0))),
        "fine_energy_drift_linf": float(np.max(np.abs(fine_energies - initial_energies))),
        "fine_number_error_linf": float(np.max(np.abs(fine_numbers - expected_numbers))),
        "tau_refinement_abs_max": max(row["tau_refinement_abs"] for row in rows),
        "peak_current_refinement_abs_max": max(row["peak_current_refinement_abs"] for row in rows),
        "target_amplitude_refinement_abs_max": max(row["target_amplitude_refinement_abs"] for row in rows),
    },
    "claim_classes": {
        "proved": "UNCHANGED_OWNER_ONCE_SUPPORT__FORWARD_EDGE_CUSTODY__AUTHENTICATED_TERMS_OFF_WRITES",
        "adopted": "OPTION_A__COMMON_PHASE__BACKGROUND_SUBTRACTION__SEARCH_WINDOW__FIRST_POSITIVE_PEAK_RULE",
        "conditional": "ALL_BLANK_PARENT__FINITE_NUMERICAL_EVOLUTION__ENSEMBLE_DIFFERENCE",
        "empirical": "FINITE_N0_TO_N3_FORWARD_EDGE_TIMES_AND_AMPLITUDES",
        "open": "INDEPENDENT_HOSTILE_AUDIT__OTHER_EDGES_CLUSTERS_PHASES_AND_PEAK_RULES__OPEN_BOUNDARY_CONTROL__PHYSICAL_METRIC_CLOCK__GATE_R_C_AND_A_P",
    },
    "not_claimed": "INDIVIDUAL_LINEAGE__BYPASS_ELIMINATION__METRIC_STRAIN__TIME_DILATION__SHAPIRO_DELAY__GRAVITY",
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
print(f"PASS__R_GATE_C_L8_FORWARD_EDGE_ARRIVAL__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
