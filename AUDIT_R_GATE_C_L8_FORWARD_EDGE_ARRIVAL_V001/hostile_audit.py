#!/usr/bin/env python3
"""Independent hostile audit of the finite L8 Option-A edge arrival.

No target code is imported. Evolution uses a unitary fourth-order
Suzuki--Yoshida factorization of three reconstructed edge matchings, rather
than the target's order-ten Taylor polynomial.
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
TARGET_DIR = ROOT / "DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001"
TARGET_RESULT = TARGET_DIR / "RESULT.json"
L = 8
SITES = 16
FULL_WORDS = 1 << SITES
MAX_PARTICLES = 4
PROBE = 0
TARGET_SITE = 4
FORWARD_EDGE = (3, 4)
BACKGROUND = (1, 2, 3)
SEARCH_TIME = 2.0 * math.pi
PEAK_FLOOR = 1e-8
COARSE_STEPS = 1024
FINE_STEPS = 2048

EXPECTED_SHA256 = {
    "DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/README.md":
        "8ab317656e54939c0b140e1f7ad981283c1b7d2e638db5208d99dbdaf4decd36",
    "DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/RESULT.json":
        "e31019933d5465377710336935e2a3607c3185735b871a58f2475f6a7bf14926",
    "DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/THEOREM.md":
        "ef5b2a0c6796706c3190a81e05d24434529542d1ee6b2b62b146a4f1d66661ba",
    "DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/compute_forward_edge_arrival.py":
        "bedb56334d88afc00dfe1cc3934479938ac68d242385deded2d1e1cce533c965",
    "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/THEOREM.md":
        "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/INDEPENDENT_RESULT.json":
        "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    "DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/RESULT.json":
        "14eca704f5e1f65eeaf9cc04a0aa40a9f2dcd8f19ea7a440cf507fb0b76f3759",
    "AUDIT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/INDEPENDENT_RESULT.json":
        "748404604c97434221052272de9cb751e99749e20897fc35f93be7a0d296efde",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prism_edges(length: int):
    edges = []
    for rail in (0, 1):
        offset = rail * length
        for node in range(length):
            edges.append((offset + node, offset + ((node + 1) % length), f"rail_{rail + 1}"))
    for node in range(length):
        edges.append((node, length + ((node + 1) % length), "connector"))
    return edges


def topology_census(edges):
    adjacency = [set() for _ in range(SITES)]
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    distance = [-1] * SITES
    distance[PROBE] = 0
    queue = deque([PROBE])
    while queue:
        u = queue.popleft()
        for v in sorted(adjacency[u]):
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                queue.append(v)
    return adjacency, distance


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


def edge_pairs(edges, basis_words, lookup):
    result = []
    for u, v, _ in edges:
        bit_u = (basis_words >> u) & 1
        bit_v = (basis_words >> v) & 1
        left = np.flatnonzero((bit_u == 0) & (bit_v == 1))
        right = lookup[basis_words[left] ^ (1 << u) ^ (1 << v)]
        if np.any(right < 0):
            raise AssertionError("number-sector closure failure")
        result.append((left, right))
    return result


def raw_h_action(states, pairs):
    out = np.zeros_like(states)
    for left, right in pairs:
        out[left] -= states[right]
        out[right] -= states[left]
    return out


def directed_current(states, pair):
    """Expectation of the owner-oriented current for one edge u->v."""
    left, right = pair  # left: u blank/v occupied; right: u occupied/v blank
    return np.sum(
        states[left].conj() * (1j * states[right])
        + states[right].conj() * (-1j * states[left]),
        axis=0,
    ).real


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


def target_occupation(states, target_bits):
    return np.einsum("w,wh->h", target_bits, np.abs(states) ** 2, optimize=False)


def evolve(step_count, initial, pairs, matchings, forward_index, target_bits):
    step = SEARCH_TIME / step_count
    states = initial.copy()
    currents = np.empty((step_count + 1, states.shape[1]), dtype=float)
    occupations = np.empty_like(currents)
    currents[0] = directed_current(states, pairs[forward_index])
    occupations[0] = target_occupation(states, target_bits)
    for index in range(1, step_count + 1):
        fourth_order(states, pairs, matchings, step)
        currents[index] = directed_current(states, pairs[forward_index])
        occupations[index] = target_occupation(states, target_bits)
    return {
        "times": np.linspace(0.0, SEARCH_TIME, step_count + 1),
        "current_trace": currents,
        "occupation_trace": occupations,
        "final_states": states,
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
    raise AssertionError("no positive directed-current peak")


def quadratic_value(values, index, offset):
    center = values[index]
    slope = 0.5 * (values[index + 1] - values[index - 1])
    curvature = 0.5 * (values[index + 1] - 2.0 * center + values[index - 1])
    return float(center + offset * slope + offset * offset * curvature)


started = time.perf_counter()
checks = []


def check(condition, label):
    checks.append((bool(condition), label))


observed_hashes = {relative: sha256(ROOT / relative) for relative in EXPECTED_SHA256}
check(observed_hashes == EXPECTED_SHA256, "target and immutable antecedent SHA-256 custody")
target = json.loads(TARGET_RESULT.read_text())
check(target["status"] == "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT", "target remains audit candidate")
check(target["checks_passed"] == target["checks_total"] == 14, "target reports 14/14")
check(target["parameters"]["L"] == 8 and target["parameters"]["full_word_dimension"] == FULL_WORDS, "target bounded to L8")

edges = prism_edges(L)
adjacency, distance = topology_census(edges)
forward_index = edges.index((3, 4, "rail_1"))
check(len(edges) == 24 and len(set((u, v) for u, v, _ in edges)) == 24, "independent owner-once edge census")
check([len(row) for row in adjacency] == [3] * SITES, "independent degree-three prism")
check(distance[TARGET_SITE] == 4, "probe-target graph distance four")
check(forward_index == 3 and edges[forward_index] == (3, 4, "rail_1"), "directed edge 3-to-4 custody")
check(target["topology"]["forward_edge_index"] == forward_index and target["topology"]["forward_edge"] == [3, 4], "target directed-edge index and orientation")
check(target["topology"]["wraparound_edges_retained"] is True and edges[7][:2] == (7, 0), "forward selector retains rail-one wraparound")

matchings = (
    tuple(index for index in range(16) if (index % 8) % 2 == 0),
    tuple(index for index in range(16) if (index % 8) % 2 == 1),
    tuple(range(16, 24)),
)
for group_index, group in enumerate(matchings):
    endpoints = [site for edge in group for site in edges[edge][:2]]
    check(len(group) == 8 and len(endpoints) == len(set(endpoints)) == SITES, f"matching {group_index} exact and vertex-disjoint")
check(set(sum((list(group) for group in matchings), [])) == set(range(24)), "three matchings cover owner edges once")

all_words = np.arange(FULL_WORDS, dtype=np.int64)
particle_number = np.array([bin(int(word)).count("1") for word in all_words])
basis_words = all_words[particle_number <= MAX_PARTICLES]
lookup = np.full(FULL_WORDS, -1, dtype=np.int64)
lookup[basis_words] = np.arange(len(basis_words))
check(len(basis_words) == sum(math.comb(SITES, n) for n in range(5)) == 2517, "complete zero-through-four sector census")
pairs = edge_pairs(edges, basis_words, lookup)

labels = []
sources = {}
for n in range(4):
    labels.extend((f"B{n}", f"P{n}"))
    sources[f"B{n}"] = BACKGROUND[:n]
    sources[f"P{n}"] = (PROBE,) + BACKGROUND[:n]
initial = np.column_stack([written_state(sources[label], basis_words, lookup) for label in labels])
label_index = {label: i for i, label in enumerate(labels)}
target_bits = ((basis_words >> TARGET_SITE) & 1).astype(float)

write_ledgers = {}
for i, label in enumerate(labels):
    count = len(sources[label])
    exact_residual = Fraction(count, 2) - Fraction(count, 2)
    initial_number = float(np.sum(np.abs(initial[:, i]) ** 2 * particle_number[basis_words]))
    write_ledgers[label] = {
        "sources": list(sources[label]),
        "delta_Q": str(Fraction(count, 2)),
        "edge_flux_terms_off": "0",
        "total_W_R": str(Fraction(count, 2)),
        "residual": str(exact_residual),
    }
    check(exact_residual == 0, f"{label} exact authenticated write ledger")
    check(abs(initial_number - count / 2.0) < 2e-15, f"{label} written number expectation")

coarse = evolve(COARSE_STEPS, initial, pairs, matchings, forward_index, target_bits)
fine = evolve(FINE_STEPS, initial, pairs, matchings, forward_index, target_bits)
target_rows = {row["N"]: row for row in target["rows"]}
rows = []
for n in range(4):
    ib = label_index[f"B{n}"]
    ip = label_index[f"P{n}"]
    current_fine = fine["current_trace"][:, ip] - fine["current_trace"][:, ib]
    current_coarse = coarse["current_trace"][:, ip] - coarse["current_trace"][:, ib]
    occupation_fine = fine["occupation_trace"][:, ip] - fine["occupation_trace"][:, ib]
    occupation_coarse = coarse["occupation_trace"][:, ip] - coarse["occupation_trace"][:, ib]
    tau, peak, index, offset = first_positive_peak(fine["times"], current_fine)
    tau_coarse, peak_coarse, coarse_index, coarse_offset = first_positive_peak(coarse["times"], current_coarse)
    delta_q4 = quadratic_value(occupation_fine, index, offset)
    delta_q4_coarse = quadratic_value(occupation_coarse, coarse_index, coarse_offset)
    stored = target_rows[n]
    rows.append({
        "N": n,
        "background_sites": list(BACKGROUND[:n]),
        "tau_fwd": tau,
        "tau_fwd_coarse": tau_coarse,
        "tau_coarse_fine_abs": abs(tau - tau_coarse),
        "tau_target": stored["tau_fwd"],
        "tau_target_abs_error": abs(tau - stored["tau_fwd"]),
        "peak_delta_J_3_to_4": peak,
        "peak_delta_J_3_to_4_coarse": peak_coarse,
        "peak_coarse_fine_abs": abs(peak - peak_coarse),
        "peak_target": stored["peak_delta_J_3_to_4"],
        "peak_target_abs_error": abs(peak - stored["peak_delta_J_3_to_4"]),
        "delta_q4_at_tau_fwd": delta_q4,
        "delta_q4_at_tau_fwd_coarse": delta_q4_coarse,
        "delta_q4_coarse_fine_abs": abs(delta_q4 - delta_q4_coarse),
        "delta_q4_target": stored["delta_q4_at_tau_fwd"],
        "delta_q4_target_abs_error": abs(delta_q4 - stored["delta_q4_at_tau_fwd"]),
        "fine_peak_index": index,
        "fine_peak_offset": offset,
    })

initial_norms = np.sum(np.abs(initial) ** 2, axis=0)
fine_norms = np.sum(np.abs(fine["final_states"]) ** 2, axis=0)
coarse_norms = np.sum(np.abs(coarse["final_states"]) ** 2, axis=0)
initial_energy = np.sum(initial.conj() * raw_h_action(initial, pairs), axis=0).real
fine_energy = np.sum(fine["final_states"].conj() * raw_h_action(fine["final_states"], pairs), axis=0).real
coarse_energy = np.sum(coarse["final_states"].conj() * raw_h_action(coarse["final_states"], pairs), axis=0).real
fine_numbers = np.sum(
    np.abs(fine["final_states"]) ** 2 * particle_number[basis_words, None], axis=0
)
expected_numbers = np.array([len(sources[label]) / 2.0 for label in labels])
taus = np.array([row["tau_fwd"] for row in rows])

check(float(np.max(np.abs(initial_norms - 1.0))) < 2e-15, "initial norms")
check(float(np.max(np.abs(fine_norms - 1.0))) < 6e-12, "fine final norms")
check(float(np.max(np.abs(coarse_norms - 1.0))) < 6e-12, "coarse final norms")
check(float(np.max(np.abs(fine_energy - initial_energy))) < 2e-9, "fine energy stability")
check(float(np.max(np.abs(coarse_energy - initial_energy))) < 3e-8, "coarse energy stability")
check(float(np.max(np.abs(fine_numbers - expected_numbers))) < 8e-12, "fine retained-number conservation")
check(all(row["tau_coarse_fine_abs"] < 1e-5 for row in rows), "tau forward coarse/fine stability")
check(all(row["peak_coarse_fine_abs"] < 2e-8 for row in rows), "peak current coarse/fine stability")
check(all(row["delta_q4_coarse_fine_abs"] < 6e-7 for row in rows), "delta q4 coarse/fine stability")
check(all(row["tau_target_abs_error"] < 5e-9 for row in rows), "all tau forward values versus target")
check(all(row["peak_target_abs_error"] < 2e-10 for row in rows), "all peak directed currents versus target")
check(all(row["delta_q4_target_abs_error"] < 2e-9 for row in rows), "all interpolated delta q4 values versus target")
check(all(row["peak_delta_J_3_to_4"] > PEAK_FLOOR for row in rows), "positive directed-current peaks")
check(not np.all(np.diff(taus) > 0.0), "tau forward is not strictly monotone")
check(taus[3] < taus[2] and taus[2] - taus[3] > 0.15, "N3-before-N2 inversion survives numerical control")

target_prose = "\n".join((
    (TARGET_DIR / "README.md").read_text(),
    (TARGET_DIR / "THEOREM.md").read_text(),
))
check(target["protocol"]["lineage_boundary"].endswith("NO_INDIVIDUAL_CARRIER_TAG"), "machine result denies individual lineage")
check(target["topology"]["wraparound_edges_retained"] is True and "does not remove the\ncounter-clockwise support" in target_prose, "Option A does not delete wraparound")
check("does not\ndelete the counter-clockwise route, identify an individual packet, or prove\nwhich earlier route" in target_prose, "final-edge selector does not identify earlier route")
check(all(term in target["not_claimed"] for term in ("INDIVIDUAL_LINEAGE", "BYPASS_ELIMINATION", "METRIC_STRAIN", "TIME_DILATION", "SHAPIRO_DELAY", "GRAVITY")), "forbidden promotions remain not claimed")
check("PHYSICAL_METRIC_CLOCK" in target["claim_classes"]["open"] and "GATE_R_C_AND_A_P" in target["claim_classes"]["open"], "metric and gates remain open")
check("It would not\nbe metric strain, gravitational time dilation, Shapiro delay, or gravity" in target_prose, "operational control is not promoted to gravity")

failures = [label for passed, label in checks if not passed]
elapsed = time.perf_counter() - started
rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes = int(rss_raw if sys.platform == "darwin" else rss_raw * 1024)

result = {
    "schema": "AUDIT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001",
    "status": "PASS_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "base_commit": "7b3a78484d7da8585e2aa1b293b8941e6d20d45c",
    "scope": "FINITE_L8_ONLY__NO_LARGER_SUPPORT_EXECUTED",
    "target_and_antecedent_sha256": observed_hashes,
    "audit_script_sha256": sha256(Path(__file__)),
    "method": {
        "target": "ORDER_TEN_TAYLOR__1024_2048_STEPS",
        "audit": "UNITARY_FOURTH_ORDER_SUZUKI_YOSHIDA__THREE_EXACT_EDGE_MATCHINGS__SEPARATE_1024_2048_STEP_RUNS",
        "observable": "INSTANTANEOUS_OWNER_ORIENTED_J_3_TO_4__BACKGROUND_SUBTRACTED",
        "peak_rule": "FIRST_POSITIVE_LOCAL_MAXIMUM_ABOVE_1E_8__THREE_POINT_PARABOLA",
    },
    "topology": {
        "sites": SITES,
        "owner_once_edges": len(edges),
        "degree_census": [len(row) for row in adjacency],
        "forward_edge": [3, 4],
        "forward_edge_index": forward_index,
        "probe_target_graph_distance": distance[TARGET_SITE],
        "wraparound_edge_retained": list(edges[7][:2]),
        "matching_edge_indices": [list(group) for group in matchings],
        "reachable_dimension": len(basis_words),
        "full_word_dimension": FULL_WORDS,
    },
    "authenticated_write_ledgers": write_ledgers,
    "rows": rows,
    "trend_screen": {
        "tau_fwd_strictly_increases_N0_to_N3": bool(np.all(np.diff(taus) > 0.0)),
        "N3_before_N2": bool(taus[3] < taus[2]),
        "N2_minus_N3": float(taus[2] - taus[3]),
        "status": "STRICT_MONOTONE_FORWARD_EDGE_DELAY_NOT_OBSERVED__INVERSION_SURVIVES",
    },
    "numerical_controls": {
        "initial_norm_error_linf": float(np.max(np.abs(initial_norms - 1.0))),
        "fine_norm_error_linf": float(np.max(np.abs(fine_norms - 1.0))),
        "coarse_norm_error_linf": float(np.max(np.abs(coarse_norms - 1.0))),
        "fine_energy_drift_linf": float(np.max(np.abs(fine_energy - initial_energy))),
        "coarse_energy_drift_linf": float(np.max(np.abs(coarse_energy - initial_energy))),
        "fine_number_error_linf": float(np.max(np.abs(fine_numbers - expected_numbers))),
        "tau_coarse_fine_abs_max": max(row["tau_coarse_fine_abs"] for row in rows),
        "peak_coarse_fine_abs_max": max(row["peak_coarse_fine_abs"] for row in rows),
        "delta_q4_coarse_fine_abs_max": max(row["delta_q4_coarse_fine_abs"] for row in rows),
        "tau_target_abs_max": max(row["tau_target_abs_error"] for row in rows),
        "peak_target_abs_max": max(row["peak_target_abs_error"] for row in rows),
        "delta_q4_target_abs_max": max(row["delta_q4_target_abs_error"] for row in rows),
    },
    "conceptual_disposition": {
        "lineage": "BACKGROUND_SUBTRACTION_IS_NOT_AN_INDIVIDUAL_TAG",
        "option_A": "SELECTS_FINAL_EDGE_INFLOW_ONLY__WRAPAROUND_RETAINED__EARLIER_ROUTE_UNIDENTIFIED",
        "tau": "FINITE_OPERATIONAL_DIRECTED_EDGE_PEAK_ONLY",
        "metric": "NOT_ESTABLISHED__NO_STRAIN_TIME_DILATION_OR_SHAPIRO_DELAY",
        "gravity": "NOT_INFERRED",
    },
    "claim_classes": {
        "proved": "UNCHANGED_OWNER_ONCE_L8_PRISM__DIRECTED_EDGE_CUSTODY__EXACT_AUTHENTICATED_TERMS_OFF_WRITE_LEDGERS",
        "adopted": "OPTION_A__COMMON_PHASE__BACKGROUND_SUBTRACTION__SEARCH_WINDOW__FIRST_POSITIVE_PEAK_RULE",
        "conditional": "ALL_BLANK_PARENT__FINITE_NUMERICAL_EVOLUTION__ENSEMBLE_DIFFERENCE",
        "empirical": "INDEPENDENT_FINITE_N0_TO_N3_FORWARD_EDGE_TIMES_CURRENTS_AND_Q4_AMPLITUDES__N3_N2_INVERSION",
        "open": "OTHER_EDGES_CLUSTERS_PHASES_PEAK_RULES__OPEN_BOUNDARY_CONTROL__INDIVIDUAL_ROUTE_OR_LINEAGE__PHYSICAL_METRIC_CLOCK__GATE_R_C_AND_A_P",
    },
    "not_claimed": "INDIVIDUAL_LINEAGE__BYPASS_ELIMINATION__EARLIER_ROUTE_IDENTIFICATION__METRIC_STRAIN__TIME_DILATION__SHAPIRO_DELAY__GRAVITY",
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
print(f"PASS__AUDIT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={elapsed:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={rss_bytes}")
