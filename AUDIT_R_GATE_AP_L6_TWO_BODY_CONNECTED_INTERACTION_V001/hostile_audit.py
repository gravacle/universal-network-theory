#!/usr/bin/env python3
"""Independent full-word hostile audit of the finite L6 two-write packet.

This verifier deliberately does not import or execute target code.  It builds
the 4096-word Hamiltonian action from raw bit swaps, advances all histories by
an eighth-order Taylor polynomial, and integrates currents by nested composite
Simpson rules.  The target instead uses a 79-dimensional eigensystem and an
analytic spectral current integral.
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
L = 6
SITE_COUNT = 12
WORD_COUNT = 1 << SITE_COUNT
FINAL_TIME = math.pi / 2.0
FINE_INTERVALS = 512
COARSE_INTERVALS = FINE_INTERVALS // 2
TAYLOR_ORDER = 8
TARGET_DIR = ROOT / "DEVELOPMENT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001"
TARGET_RESULT = TARGET_DIR / "RESULT.json"
LEDGER = ROOT / "GRAVITY_VERIFICATION_LEDGER.md"
SECTION_START = "### Gate A-P single-source prism diagnostic"
SECTION_END = "\n### Gate A-P — CONTINUUM/MACROSCOPIC RESPONSE"
EXPECTED_LEDGER_SECTION_SHA256 = "477525ad068f2cb9ec5ffbd07834bf94b7c1cb2f47fabacc5d06fb8476d83553"

EXPECTED_SHA256 = {
    "DEVELOPMENT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001/README.md":
        "36fd928991ebfcea38e05f13ee519b0f1be5f3069b2889c9becb3c12a428f490",
    "DEVELOPMENT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001/RESULT.json":
        "852029b5bdb1714f3031cabd191fa86d6ffe4ac912fc625e39b9e4084733168b",
    "DEVELOPMENT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001/RESULT.md":
        "cad023e568eaf99ba340b9119ffb46de2702cd3335690f0b88a237d4b5d48020",
    "DEVELOPMENT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001/THEOREM.md":
        "d8b768f747d79c60eb0edecc32c5d490940c3ecff5318923d8227cf695fa7827",
    "DEVELOPMENT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001/compute_two_body_connected.py":
        "c704ab6b1d0a7e62a006acb4b54e4b7e593038c731cc50a76e51868d3c09e884",
    "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/THEOREM.md":
        "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/INDEPENDENT_RESULT.json":
        "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    "DEVELOPMENT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001/RESULT.json":
        "315efc89e91ccb2816787716f7a724e76f292a9a689a11f80f18f4dd337deb90",
    "DEVELOPMENT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001/RESULT_L6.json":
        "8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a",
    "AUDIT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001/RESULT.json":
        "45b88fe34d459b81246ed289040a8b9824e45f75caa47b9c0836c2ff7772060a",
    "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001/RESULT.json":
        "eca3197740059226fa9665fd92b7556a653e698867af3ce6116ba17c3453b538",
    "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001/RESULT_L6.json":
        "2a0d2c957b39b960f8d87b55914efd4a547510e3f2cfc01a2a135a1efb2a967b",
    "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001/RESULT_L8.json":
        "288b007e4a519b1b26e062894c7c42685bf200d924b053c196cefda6014cbcdf",
    "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001/RESULT_L10.json":
        "cdf5dae0b6762ca60e8deefb07ac9f05abf06c7d693cd79415db03e154d6f116",
    "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001/RESULT_L12.json":
        "c7fd23bd73c96df1ca234952cba5d5c3eef5652b1de6f7ea3a0e262ef99c6b8f",
    "AUDIT_R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD_V001/RESULT.json":
        "14db7c3a3b8abeca83686423631bcf57e9a13a906464d26d4461ce825dc58fcd",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_edges(length: int) -> list[tuple[int, int, str]]:
    """Construct the documented prism without consulting target topology."""
    result: list[tuple[int, int, str]] = []
    for ring in (0, 1):
        offset = ring * length
        for s in range(length):
            result.append((offset + s, offset + ((s + 1) % length), "ring"))
    for s in range(length):
        result.append((s, length + ((s + 1) % length), "seam"))
    return result


def distances_from_zero(edges: list[tuple[int, int, str]], vertex_count: int) -> list[int]:
    adjacency = [set() for _ in range(vertex_count)]
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    distance = [-1] * vertex_count
    distance[0] = 0
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in sorted(adjacency[u]):
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                queue.append(v)
    return distance


def make_history(sources: tuple[int, ...]) -> np.ndarray:
    """Build the declared tensor-product write directly in all 4096 words."""
    vector = np.zeros(WORD_COUNT, dtype=np.complex128)
    scale = 2.0 ** (-0.5 * len(sources))
    for subset in range(1 << len(sources)):
        word = 0
        occupied = 0
        for j, site in enumerate(sources):
            if subset & (1 << j):
                word |= 1 << site
                occupied += 1
        vector[word] = scale * ((-1j) ** occupied)
    return vector


def raw_swap_tables(edges: list[tuple[int, int, str]]):
    words = np.arange(WORD_COUNT, dtype=np.int64)
    tables = []
    for u, v, _ in edges:
        bu = (words >> u) & 1
        bv = (words >> v) & 1
        active = np.flatnonzero(bu != bv)
        partner = active ^ (1 << u) ^ (1 << v)
        current_coefficient = 1j * (bv[active] - bu[active])
        tables.append((active, partner, current_coefficient))
    return tables


def h_action(states: np.ndarray, tables) -> np.ndarray:
    """Raw full-word action of minus one hop on every owner-once edge."""
    out = np.zeros_like(states)
    for active, partner, _ in tables:
        out[active, :] -= states[partner, :]
    return out


def current_expectations(states: np.ndarray, tables) -> np.ndarray:
    result = np.empty((states.shape[1], len(tables)), dtype=float)
    for e, (active, partner, coefficient) in enumerate(tables):
        terms = states[active, :].conj() * coefficient[:, None] * states[partner, :]
        result[:, e] = np.sum(terms, axis=0).real
    return result


def advance_taylor(states: np.ndarray, dt: float, tables) -> np.ndarray:
    accumulated = states.copy()
    term = states.copy()
    for order in range(1, TAYLOR_ORDER + 1):
        term = (-1j * dt / order) * h_action(term, tables)
        accumulated += term
    return accumulated


def simpson(samples: np.ndarray, spacing: float) -> np.ndarray:
    intervals = samples.shape[0] - 1
    if intervals % 2:
        raise AssertionError("Simpson rule requires an even interval count")
    return (spacing / 3.0) * (
        samples[0]
        + samples[-1]
        + 4.0 * np.sum(samples[1:-1:2], axis=0)
        + 2.0 * np.sum(samples[2:-1:2], axis=0)
    )


def occupations(states: np.ndarray) -> np.ndarray:
    probabilities = np.abs(states) ** 2
    words = np.arange(WORD_COUNT, dtype=np.int64)
    bits = np.array([((words >> s) & 1).astype(float) for s in range(SITE_COUNT)])
    return np.einsum("wh,sw->hs", probabilities, bits, optimize=False)


def energy(states: np.ndarray, tables) -> np.ndarray:
    return np.sum(states.conj() * h_action(states, tables), axis=0)


def connected(array: np.ndarray, labels: list[str], d: int) -> np.ndarray:
    location = {label: i for i, label in enumerate(labels)}
    return (
        array[location[f"11_d{d}"]]
        - array[location[f"10_d{d}"]]
        - array[location[f"01_d{d}"]]
        + array[location["00"]]
    )


def cubic_torus_green(length: int):
    modes = np.arange(length)
    kx, ky, kz = np.meshgrid(modes, modes, modes, indexing="ij")
    denominator = 6.0 - 2.0 * (
        np.cos(2.0 * np.pi * kx / length)
        + np.cos(2.0 * np.pi * ky / length)
        + np.cos(2.0 * np.pi * kz / length)
    )
    inverse = np.zeros_like(denominator)
    nonzero = denominator > 1e-14
    inverse[nonzero] = 1.0 / denominator[nonzero]
    green = np.fft.ifftn(inverse).real
    max_r = length // 2
    axis = {r: float(green[r, 0, 0]) for r in range(2, max_r + 1)}
    shell = {}
    for r in range(2, max_r + 1):
        values = []
        for x in range(length):
            for y in range(length):
                for z in range(length):
                    manhattan = sum(min(c, length - c) for c in (x, y, z))
                    if manhattan == r:
                        values.append(green[x, y, z])
        shell[r] = float(np.mean(values))
    return axis, shell


def extract_ledger_section() -> str:
    text = LEDGER.read_text()
    start = text.index(SECTION_START)
    end = text.index(SECTION_END, start)
    return text[start:end].rstrip() + "\n"


started = time.perf_counter()
checks: list[tuple[bool, str]] = []


def check(condition, label: str):
    checks.append((bool(condition), label))


observed_hashes = {relative: sha256(ROOT / relative) for relative in EXPECTED_SHA256}
check(observed_hashes == EXPECTED_SHA256, "target and antecedent SHA-256 custody")
ledger_section = extract_ledger_section()
ledger_section_sha = hashlib.sha256(ledger_section.encode()).hexdigest()
check(ledger_section_sha == EXPECTED_LEDGER_SECTION_SHA256, "bounded ledger paragraph custody")

target = json.loads(TARGET_RESULT.read_text())
check(target["status"] == "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT", "target remains audit candidate")
check(target["checks_passed"] == target["checks_total"] == 25, "target reports 25/25")
check(target["parameters"]["L"] == L and target["parameters"]["full_word_dimension"] == WORD_COUNT, "target declares only L6 full-word scope")

edges = graph_edges(L)
distance = distances_from_zero(edges, SITE_COUNT)
degree = [0] * SITE_COUNT
for u, v, _ in edges:
    degree[u] += 1
    degree[v] += 1
check(len(edges) == 18 and len(set((u, v) for u, v, _ in edges)) == 18, "independent owner-once 18-edge census")
check(degree == [3] * SITE_COUNT, "independent degree-three prism census")
check(distance == [0, 1, 2, 3, 2, 1, 2, 1, 2, 3, 4, 3], "independent source-zero BFS distances")
target_edges = [(row["u"], row["v"]) for row in target["topology"]["edges"]]
check(target_edges == [(u, v) for u, v, _ in edges], "target edge order matches independent prism")
check({d: distance[d] for d in (1, 2, 3)} == {1: 1, 2: 2, 3: 3}, "canonical A0-A1/A2/A3 graph separations")

labels = ["00"]
source_map: dict[str, tuple[int, ...]] = {"00": ()}
for d in (1, 2, 3):
    source_map[f"10_d{d}"] = (0,)
    source_map[f"01_d{d}"] = (d,)
    source_map[f"11_d{d}"] = (0, d)
    labels.extend((f"10_d{d}", f"01_d{d}", f"11_d{d}"))
initial = np.column_stack([make_history(source_map[label]) for label in labels])
tables = raw_swap_tables(edges)

# Terms-off ledgers are exact rational counts: probability weights are 1/2
# per single target and 1/4 per term of the two-target tensor product.
exact_write_ledgers = {
    "00": "0+0-0=0",
    "10": "1/2+0-1/2=0",
    "01": "1/2+0-1/2=0",
    "11": "1+0-1/2-1/2=0",
}
exact_write_residuals = {
    "00": Fraction(0) + Fraction(0) - Fraction(0),
    "10": Fraction(1, 2) + Fraction(0) - Fraction(1, 2),
    "01": Fraction(1, 2) + Fraction(0) - Fraction(1, 2),
    "11": Fraction(1) + Fraction(0) - Fraction(1, 2) - Fraction(1, 2),
}
q_initial = occupations(initial)
q_initial_sum = np.sum(q_initial, axis=1)
expected_write_total = np.array([0.5 * len(source_map[label]) for label in labels])
check(np.max(np.abs(q_initial_sum - expected_write_total)) < 4e-16, "terms-off numerical occupation totals")
check(all(value == 0 for value in exact_write_residuals.values()), "terms-off exact rational write ledgers")
check(all(np.max(np.abs(connected(q_initial, labels, d))) < 4e-16 for d in (1, 2, 3)), "initial occupation inclusion-exclusion cancellation")

energy_initial = energy(initial, tables)
expected_connected_energy = {1: -0.5, 2: 0.0, 3: 0.0}
for d in (1, 2, 3):
    check(abs(connected(energy_initial, labels, d).real - expected_connected_energy[d]) < 4e-16, f"d{d} direct initial connected energy")
check(np.max(np.abs(energy_initial.imag)) < 1e-16, "initial energy reality")

dt = FINAL_TIME / FINE_INTERVALS
states = initial.copy()
current_samples = np.empty((FINE_INTERVALS + 1, len(labels), len(edges)), dtype=float)
current_samples[0] = current_expectations(states, tables)
for step in range(1, FINE_INTERVALS + 1):
    states = advance_taylor(states, dt, tables)
    current_samples[step] = current_expectations(states, tables)

fine_current = simpson(current_samples, dt)
coarse_current = simpson(current_samples[::2], 2.0 * dt)
q_final = occupations(states)
energy_final = energy(states, tables)
norm_final = np.sum(np.abs(states) ** 2, axis=0)

incidence = np.zeros((SITE_COUNT, len(edges)))
for e, (u, v, _) in enumerate(edges):
    incidence[u, e] = 1.0
    incidence[v, e] = -1.0
history_residual = q_final - q_initial + np.einsum(
    "he,se->hs", fine_current, incidence, optimize=False
)

target_histories = {row["label"]: row for row in target["histories"]}
target_current = np.array([target_histories[label]["integrated_edge_currents"] for label in labels])
target_q_initial = np.array([target_histories[label]["q_initial_sum"] for label in labels])
target_q_final = np.array([target_histories[label]["q_final"] for label in labels])
target_energy_initial = np.array([target_histories[label]["energy_initial"] for label in labels])
target_energy_final = np.array([target_histories[label]["energy_final"] for label in labels])

fine_target_current_linf = float(np.max(np.abs(fine_current - target_current)))
coarse_target_current_linf = float(np.max(np.abs(coarse_current - target_current)))
coarse_fine_current_linf = float(np.max(np.abs(coarse_current - fine_current)))
check(fine_target_current_linf < 2e-10, "fine full-word currents versus target spectral analytic vectors")
check(coarse_target_current_linf < 3e-9, "coarse full-word currents versus target spectral analytic vectors")
check(coarse_fine_current_linf < 3e-9, "nested coarse/fine current quadrature control")
check(float(np.max(np.abs(q_initial_sum - target_q_initial))) < 5e-16, "all initial totals versus target")
check(float(np.max(np.abs(q_final - target_q_final))) < 2e-12, "all terminal occupation vectors versus target")
check(float(np.max(np.abs(energy_initial.real - target_energy_initial))) < 5e-16, "all initial energies versus target")
check(float(np.max(np.abs(energy_final.real - target_energy_final))) < 3e-12, "all final energies versus target")
check(float(np.max(np.abs(norm_final - 1.0))) < 3e-13, "full-word terminal norms")
particle_number = np.array([bin(word).count("1") for word in range(WORD_COUNT)])
outside_reachable_probability = float(np.max(np.sum(np.abs(states[particle_number > 2]) ** 2, axis=0)))
check(outside_reachable_probability == 0.0, "full-word propagation remains in complete zero/one/two sectors")
check(float(np.max(np.abs(energy_final.real - energy_initial.real))) < 3e-12, "full-word energy conservation")
check(float(np.max(np.sum(np.abs(history_residual), axis=1))) < 2e-9, "all independent owner-once history ledgers")

target_connected = {row["d"]: row for row in target["connected_rows"]}
connected_rows = []
all_connected_current_errors = []
all_target_sign_rebuild_errors = []
for d in (1, 2, 3):
    delta_j = connected(fine_current, labels, d)
    delta_j_coarse = connected(coarse_current, labels, d)
    delta_q_before = connected(q_initial, labels, d)
    delta_q_after = connected(q_final, labels, d)
    delta_e_initial = connected(energy_initial, labels, d)
    delta_e_final = connected(energy_final, labels, d)
    residual = delta_q_after - delta_q_before + np.einsum(
        "se,e->s", incidence, delta_j, optimize=False
    )
    stored = target_connected[d]
    stored_j = np.array(stored["delta12_J"])
    current_error = float(np.max(np.abs(delta_j - stored_j)))
    all_connected_current_errors.append(current_error)

    # Recombine target history rows too, testing that the stored connected row
    # actually uses the declared signs +11,-10,-01,+00.
    target_rebuilt_j = connected(target_current, labels, d)
    target_rebuilt_q = connected(target_q_final, labels, d)
    all_target_sign_rebuild_errors.append(float(max(
        np.max(np.abs(target_rebuilt_j - stored_j)),
        np.max(np.abs(target_rebuilt_q - np.array(stored["delta12_q_after"]))),
    )))
    connected_rows.append({
        "d": d,
        "pair": f"A0-A{d}",
        "delta12_E_initial": float(delta_e_initial.real),
        "delta12_E_final": float(delta_e_final.real),
        "delta12_E_target": float(stored["delta12_E_final"]),
        "delta12_E_target_abs_error": float(abs(delta_e_final.real - stored["delta12_E_final"])),
        "delta12_J_fine": [float(x) for x in delta_j],
        "delta12_J_coarse": [float(x) for x in delta_j_coarse],
        "delta12_J_target": [float(x) for x in stored_j],
        "delta12_J_target_linf_error": current_error,
        "delta12_J_coarse_fine_linf": float(np.max(np.abs(delta_j_coarse - delta_j))),
        "delta12_J_l1": float(np.sum(np.abs(delta_j))),
        "delta12_J_linf": float(np.max(np.abs(delta_j))),
        "delta12_q_before_linf": float(np.max(np.abs(delta_q_before))),
        "delta12_q_after": [float(x) for x in delta_q_after],
        "connected_ledger_residual": [float(x) for x in residual],
        "connected_ledger_residual_l1": float(np.sum(np.abs(residual))),
        "connected_ledger_residual_linf": float(np.max(np.abs(residual))),
    })

check(max(all_connected_current_errors) < 4e-10, "all 54 complete connected-current components versus target")
check(max(all_target_sign_rebuild_errors) < 5e-16, "target inclusion-exclusion signs and connected rows")
check(max(row["connected_ledger_residual_l1"] for row in connected_rows) < 5e-9, "all connected continuity ledgers")
check(all(row["delta12_J_linf"] > 1e-3 for row in connected_rows), "nonzero connected current at all three pairs")
check(abs(connected_rows[0]["delta12_E_final"] + 0.5) < 3e-12, "d1 conserved contact energy minus one half")
check(all(abs(row["delta12_E_final"]) < 3e-12 for row in connected_rows[1:]), "d2/d3 connected energy zero")

# Audit the new bounded single-source ledger paragraph from pinned marked-source
# results.  The carrier shells and cubic-torus kernels are deliberately kept as
# differently typed objects; this is only a comparator screen.
marked = json.loads((ROOT / "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001/RESULT.json").read_text())
marked_rows = {row["L"]: row for row in marked["rows"]}
raw_profiles = {}
for length in (6, 8, 10, 12):
    raw = json.loads((ROOT / f"DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001/RESULT_L{length}.json").read_text())
    raw_edges = graph_edges(length)
    raw_distances = distances_from_zero(raw_edges, 2 * length)
    l1_profile = {}
    signed_profile = {}
    check(len(raw["edge_records"]) == 3 * length, f"L{length} raw single-source edge census")
    check([(row["u"], row["v"]) for row in raw["edge_records"]] == [(u, v) for u, v, _ in raw_edges], f"L{length} raw single-source prism endpoints")
    for row in raw["edge_records"]:
        radius = min(raw_distances[row["u"]], raw_distances[row["v"]])
        check(row["r"] == radius, f"L{length} edge {row['edge_index']} shortest-path radius")
        l1_profile[radius] = l1_profile.get(radius, 0.0) + abs(row["delta_J"])
        signed_profile[radius] = signed_profile.get(radius, 0.0) + row["delta_J"]
    compiled_l1 = {int(r): float(v) for r, v in marked_rows[length]["edge_profile_l1_by_radius"].items()}
    compiled_signed = {int(r): float(v) for r, v in marked_rows[length]["edge_profile_signed_by_radius"].items()}
    check(max(abs(l1_profile[r] - compiled_l1[r]) for r in l1_profile) < 3e-16, f"L{length} raw-to-compiled shell L1 reconstruction")
    check(max(abs(signed_profile[r] - compiled_signed[r]) for r in signed_profile) < 3e-16, f"L{length} raw-to-compiled signed-shell reconstruction")
    raw_profiles[length] = {"l1": l1_profile, "signed": signed_profile}

l12_r2 = raw_profiles[12]["l1"][2]
l12_r6 = raw_profiles[12]["l1"][6]
screen_factor = l12_r2 / l12_r6
check(screen_factor == 1439.7290468123826, "ledger 1439.729 factor from stored L12 values")
check("1439.7290468123826" in ledger_section and "approximately `1,440`" in ledger_section, "ledger prints audited factor")
check(all(max(raw_profiles[length]["l1"], key=raw_profiles[length]["l1"].get) == 2 for length in raw_profiles), "r2 is L1 maximum for every L6-L12 row")

green_rows = {}
strict_signed_axis = []
strict_signed_shell = []
strict_l1_axis = []
strict_l1_shell = []
axis_sign_mismatches = []
for length in (6, 8, 10, 12):
    axis, shell = cubic_torus_green(length)
    signed = raw_profiles[length]["signed"]
    l1 = raw_profiles[length]["l1"]
    axis_ratio = {r: axis[r] / axis[2] for r in axis}
    shell_ratio = {r: shell[r] / shell[2] for r in shell}
    signed_ratio = {r: signed[r] / signed[2] for r in range(2, length // 2 + 1)}
    l1_ratio = {r: l1[r] / l1[2] for r in range(2, length // 2 + 1)}
    for r in range(3, length // 2):
        strict_signed_axis.append(signed_ratio[r] - axis_ratio[r])
        strict_signed_shell.append(signed_ratio[r] - shell_ratio[r])
        strict_l1_axis.append(l1_ratio[r] - abs(axis_ratio[r]))
        strict_l1_shell.append(l1_ratio[r] - shell_ratio[r])
    for r in range(3, length // 2 + 1):
        if math.copysign(1.0, signed_ratio[r]) != math.copysign(1.0, axis_ratio[r]):
            axis_sign_mismatches.append([length, r])
    green_rows[str(length)] = {
        "signed_record_ratio_r2_normalized": {str(k): v for k, v in signed_ratio.items()},
        "l1_record_ratio_r2_normalized": {str(k): v for k, v in l1_ratio.items()},
        "axis_green_ratio_r2_normalized": {str(k): v for k, v in axis_ratio.items()},
        "periodic_manhattan_shell_green_ratio_r2_normalized": {str(k): v for k, v in shell_ratio.items()},
    }

def rms(values):
    return float(math.sqrt(sum(x * x for x in values) / len(values)))


green_metrics = {
    "strict_interior_points": "N8:r3; N10:r3,r4; N12:r3,r4,r5",
    "signed_vs_axis_rms": rms(strict_signed_axis),
    "signed_vs_axis_max_abs": float(max(map(abs, strict_signed_axis))),
    "signed_vs_shell_mean_rms": rms(strict_signed_shell),
    "signed_vs_shell_mean_max_abs": float(max(map(abs, strict_signed_shell))),
    "l1_vs_abs_axis_rms": rms(strict_l1_axis),
    "l1_vs_abs_axis_max_abs": float(max(map(abs, strict_l1_axis))),
    "l1_vs_shell_mean_rms": rms(strict_l1_shell),
    "l1_vs_shell_mean_max_abs": float(max(map(abs, strict_l1_shell))),
    "axis_sign_mismatches": axis_sign_mismatches,
}
check(axis_sign_mismatches == [[8, 4], [10, 5], [12, 6]], "finite axis-kernel sign mismatches")
check(green_metrics["signed_vs_axis_rms"] > 0.1 and green_metrics["signed_vs_shell_mean_rms"] > 0.25, "signed profile does not reproduce either torus comparator")
check(green_metrics["l1_vs_abs_axis_rms"] > 0.06 and green_metrics["l1_vs_shell_mean_rms"] > 0.16, "L1 profile does not reproduce either torus comparator")
check("shortest-path edge shells on a degree-three prism" in ledger_section and "degree-six `L^3` cubic torus" in ledger_section, "ledger preserves prism/torus type distinction")
check("not a proved exact exponential" in ledger_section and "No grid or\ncontinuum premise" in ledger_section, "ledger bounds empirical screening claim")

# Hostile conceptual gates: require narrow language in both machine result and
# prose.  A connected current is not itself an exchange potential, and the
# contact/noncontact energy pattern is not a binding result.
all_target_prose = "\n".join((
    (TARGET_DIR / "README.md").read_text(),
    (TARGET_DIR / "RESULT.md").read_text(),
    (TARGET_DIR / "THEOREM.md").read_text(),
))
check(target["interpretation"]["exchange_potential"].startswith("NOT_ESTABLISHED"), "machine claim rejects exchange-potential promotion")
check(target["interpretation"]["binding_test"].startswith("NO_MUTUAL_ATTRACTIVE_BINDING"), "machine claim rejects mutual-binding promotion")
check("A connected coherent current is not" in all_target_prose and "long-range exchange potential" in all_target_prose, "prose preserves current/potential distinction")
check("not evidence of mutual attractive binding" in all_target_prose, "prose preserves contact-energy/binding distinction")
check("GATE_A_P" in target["claim_classes"]["open"] and "GRAVITY" in target["not_claimed"], "Gate A-P and gravity remain open/not claimed")
check("LARGER_L" in target["claim_classes"]["open"] and "OTHER_PAIR_ORBITS" in target["claim_classes"]["open"], "larger supports and other pair orbits remain open")

failures = [label for passed, label in checks if not passed]
elapsed = time.perf_counter() - started
max_rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
max_rss_bytes = int(max_rss_raw if sys.platform == "darwin" else max_rss_raw * 1024)

result = {
    "schema": "AUDIT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001",
    "status": "PASS_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "base_commit": "54eec6c4766cc8a2b593153b6e45a3019ef22e07",
    "scope": "FINITE_L6_ONLY__NO_LARGER_SUPPORT_EXECUTED",
    "target_and_antecedent_sha256": observed_hashes,
    "ledger_section_sha256": ledger_section_sha,
    "audit_script_sha256": sha256(Path(__file__)),
    "method": {
        "state_space": "ALL_4096_WORDS",
        "hamiltonian": "RAW_OWNER_ONCE_BIT_SWAP_ACTION__NO_TARGET_CODE_IMPORTED",
        "propagation": f"ORDER_{TAYLOR_ORDER}_DIRECT_POLYNOMIAL__{FINE_INTERVALS}_INTERVALS",
        "current_quadrature": f"NESTED_COMPOSITE_SIMPSON__COARSE_{COARSE_INTERVALS}__FINE_{FINE_INTERVALS}",
        "target_method": target["numerical_controls"]["method"],
    },
    "topology": {
        "sites": SITE_COUNT,
        "owner_once_edges": len(edges),
        "degree_census": degree,
        "source_zero_distances": distance,
        "pairs": {"1": [0, 1], "2": [0, 2], "3": [0, 3]},
    },
    "terms_off_write_ledgers": exact_write_ledgers,
    "numerical_controls": {
        "fine_target_complete_history_current_linf": fine_target_current_linf,
        "coarse_target_complete_history_current_linf": coarse_target_current_linf,
        "coarse_fine_complete_history_current_linf": coarse_fine_current_linf,
        "terminal_q_target_linf": float(np.max(np.abs(q_final - target_q_final))),
        "final_energy_target_linf": float(np.max(np.abs(energy_final.real - target_energy_final))),
        "terminal_norm_error_linf": float(np.max(np.abs(norm_final - 1.0))),
        "history_energy_conservation_linf": float(np.max(np.abs(energy_final.real - energy_initial.real))),
        "outside_reachable_probability": outside_reachable_probability,
        "history_ledger_residual_l1_max": float(np.max(np.sum(np.abs(history_residual), axis=1))),
        "connected_current_target_linf_max": max(all_connected_current_errors),
        "target_connected_sign_rebuild_linf_max": max(all_target_sign_rebuild_errors),
        "connected_ledger_residual_l1_max": max(row["connected_ledger_residual_l1"] for row in connected_rows),
    },
    "history_observations": [
        {
            "label": label,
            "sources": list(source_map[label]),
            "q_initial_sum": float(q_initial_sum[i]),
            "q_final_sum": float(np.sum(q_final[i])),
            "energy_initial": float(energy_initial[i].real),
            "energy_final": float(energy_final[i].real),
            "ledger_residual_l1": float(np.sum(np.abs(history_residual[i]))),
        }
        for i, label in enumerate(labels)
    ],
    "connected_rows": connected_rows,
    "single_source_ledger_paragraph_audit": {
        "L12_r2_l1": l12_r2,
        "L12_r6_l1": l12_r6,
        "stored_binary64_ratio": screen_factor,
        "profile_maximum_radius_all_L6_L12": 2,
        "raw_profiles": {
            str(length): {
                "l1": {str(r): value for r, value in raw_profiles[length]["l1"].items()},
                "signed": {str(r): value for r, value in raw_profiles[length]["signed"].items()},
            }
            for length in raw_profiles
        },
        "carrier_topology": "2L_SITE_3L_EDGE_DEGREE_THREE_PRISM__SHORTEST_PATH_EDGE_SHELLS",
        "comparator_topology": "L_CUBED_SITE_3L_CUBED_EDGE_DEGREE_SIX_CUBIC_TORUS__COMPARATOR_ONLY",
        "green_rows": green_rows,
        "green_residual_metrics": green_metrics,
        "disposition": "PASS_BOUNDED_EMPIRICAL_NON_TORUS_CLAIM",
    },
    "conceptual_disposition": {
        "connected_current": "REJECTS_STRICT_OBSERVABLE_SUPERPOSITION_FOR_THIS_FINITE_CONDITIONAL_PROTOCOL",
        "exchange_potential": "NOT_ESTABLISHED_BY_NONZERO_CONNECTED_CURRENT",
        "energy": "DIRECT_CONTACT_DELTA12_E_MINUS_ONE_HALF__D2_D3_ZERO",
        "binding": "NOT_ESTABLISHED_ACROSS_SEPARATIONS",
        "gate": "GATE_A_P_REMAINS_OPEN",
        "not_claimed": "PHYSICAL_DISTANCE__LONG_RANGE_POTENTIAL__BINDING__SCALING__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
    },
    "claim_classes": {
        "proved": "INDEPENDENT_PRISM_CENSUS__EXACT_TERMS_OFF_WRITE_LEDGERS__DECLARED_INCLUSION_EXCLUSION_SIGNS__FULL_4096_WORD_RAW_ACTION",
        "adopted": "F3_MDC_ALPHA_R0__KAPPA_PI_OVER_2__CANONICAL_A_RING_PAIR_REPRESENTATIVES",
        "conditional": "ALL_BLANK_VACUUM_PARENT__COMMON_WRITE_PHASE__PAIR_ORIENTATION__WRITE_AND_TRANSPORT_SCHEDULE",
        "empirical": "INDEPENDENT_BINARY64_L6_FULL_WORD_PROPAGATION__CURRENT_QUADRATURE__ENERGY_AND_LEDGER_VALUES__FINITE_GREEN_COMPARATOR_MISMATCH",
        "open": "OTHER_PAIR_ORBITS_AND_PHASES__LARGER_SUPPORTS__PHYSICAL_DISTANCE__NONCONTACT_POTENTIAL__BINDING__GATE_A_P",
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "resources": {
        "runtime_seconds": elapsed,
        "max_rss_bytes": max_rss_bytes,
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
        for i, (left, right) in enumerate(zip(observed, canonical)):
            compatible(left, right, f"{path}[{i}]")
    elif isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 2e-11:
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
print(f"PASS__AUDIT_R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={elapsed:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={max_rss_bytes}")
