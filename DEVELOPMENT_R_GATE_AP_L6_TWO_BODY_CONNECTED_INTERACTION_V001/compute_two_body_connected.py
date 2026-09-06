#!/usr/bin/env python3
"""Exact finite L6 two-write connected response on the owner-once prism."""

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


LENGTH = 6
SITES = 2 * LENGTH
FULL_DIMENSION = 1 << SITES
KAPPA = math.pi / 2.0
SOURCE_1 = 0
SOURCE_2_BY_DISTANCE = {1: 1, 2: 2, 3: 3}
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = HERE / "RESULT.json"
STARTED = time.perf_counter()

ANTECEDENTS = {
    ROOT / "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "THEOREM.md":
        "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    ROOT / "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "INDEPENDENT_RESULT.json":
        "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    ROOT / "DEVELOPMENT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001" / "RESULT.json":
        "315efc89e91ccb2816787716f7a724e76f292a9a689a11f80f18f4dd337deb90",
    ROOT / "DEVELOPMENT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001" / "RESULT_L6.json":
        "8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a",
    ROOT / "AUDIT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001" / "RESULT.json":
        "45b88fe34d459b81246ed289040a8b9824e45f75caa47b9c0836c2ff7772060a",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_for(length: int):
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append((
                layer * length + site,
                layer * length + (site + 1) % length,
                "internal",
            ))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def graph_distances(vertex_count: int, edges, source: int):
    neighbors = [set() for _ in range(vertex_count)]
    for u, v, _ in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    distances = [None] * vertex_count
    distances[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if distances[v] is None:
                distances[v] = distances[u] + 1
                queue.append(v)
    return neighbors, distances


def prepared_state(source_sites, basis_words, basis_index):
    """Tensor product of (|B>-i|x>)/sqrt(2) on declared blank sites."""
    state = np.zeros(len(basis_words), dtype=np.complex128)
    source_sites = tuple(source_sites)
    normalization = math.sqrt(1 << len(source_sites))
    for subset in range(1 << len(source_sites)):
        word = 0
        occupied = 0
        for index, site in enumerate(source_sites):
            if (subset >> index) & 1:
                word |= 1 << site
                occupied += 1
        state[basis_index[word]] = (-1j) ** occupied / normalization
    return state


def stable_integral(omega: np.ndarray, time_value: float) -> np.ndarray:
    out = np.empty_like(omega, dtype=np.complex128)
    small = np.abs(omega) < 1e-12
    out[small] = time_value
    out[~small] = np.expm1(1j * omega[~small] * time_value) / (1j * omega[~small])
    return out


edges = edges_for(LENGTH)
neighbors, distances = graph_distances(SITES, edges, SOURCE_1)
all_words = np.arange(FULL_DIMENSION, dtype=np.int64)
particle_number = np.array([bin(int(word)).count("1") for word in all_words])

# Every requested history has at most two excitations and the Hamiltonian
# conserves number. These complete 0/1/2 sectors therefore exhaust the full
# 2^12-word evolution; embedding checks below retain the unreduced word map.
basis_words = all_words[particle_number <= 2]
basis_index = {int(word): index for index, word in enumerate(basis_words)}
dimension = len(basis_words)

hamiltonian = np.zeros((dimension, dimension), dtype=np.complex128)
current_operators = []
for u, v, _ in edges:
    current = np.zeros_like(hamiltonian)
    for row, word_value in enumerate(basis_words):
        word = int(word_value)
        bit_u = (word >> u) & 1
        bit_v = (word >> v) & 1
        if bit_u == bit_v:
            continue
        swapped = word ^ (1 << u) ^ (1 << v)
        column = basis_index[swapped]
        hamiltonian[row, column] -= 1.0
        current[row, column] = 1j * (bit_v - bit_u)
    current_operators.append(current)

occupation_diagonals = np.array([
    ((basis_words >> site) & 1).astype(float)
    for site in range(SITES)
])

history_sources = {"00": ()}
for distance, source_2 in SOURCE_2_BY_DISTANCE.items():
    history_sources[f"10_d{distance}"] = (SOURCE_1,)
    history_sources[f"01_d{distance}"] = (source_2,)
    history_sources[f"11_d{distance}"] = (SOURCE_1, source_2)

history_labels = list(history_sources)
initial = np.column_stack([
    prepared_state(history_sources[label], basis_words, basis_index)
    for label in history_labels
])

eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
coefficients = np.einsum(
    "ji,jh->ih", eigenvectors.conj(), initial, optimize=False
)
phases = np.exp(-1j * eigenvalues * KAPPA)
final = np.einsum(
    "ji,ih->jh", eigenvectors, phases[:, None] * coefficients, optimize=False
)

omega = eigenvalues[:, None] - eigenvalues[None, :]
time_integral = stable_integral(omega, KAPPA)
integrated_currents = np.empty((len(history_labels), len(edges)), dtype=float)
for edge_index, current in enumerate(current_operators):
    current_times_eigenvectors = np.einsum(
        "jk,kl->jl", current, eigenvectors, optimize=False
    )
    current_eigen = np.einsum(
        "ji,jl->il", eigenvectors.conj(), current_times_eigenvectors,
        optimize=False,
    )
    kernel = current_eigen * time_integral
    for history_index in range(len(history_labels)):
        c = coefficients[:, history_index]
        integrated_currents[history_index, edge_index] = float(
            np.sum(c.conj()[:, None] * c[None, :] * kernel).real
        )


def occupations(states: np.ndarray) -> np.ndarray:
    probabilities = np.abs(states) ** 2
    return np.array([
        [float(np.dot(occupation_diagonals[site], probabilities[:, history]))
         for site in range(SITES)]
        for history in range(states.shape[1])
    ])


q_before = occupations(initial)
q_after = occupations(final)
energies_before = np.array([
    np.vdot(
        initial[:, history],
        np.einsum("ij,j->i", hamiltonian, initial[:, history], optimize=False),
    )
    for history in range(initial.shape[1])
])
energies_after = np.array([
    np.vdot(
        final[:, history],
        np.einsum("ij,j->i", hamiltonian, final[:, history], optimize=False),
    )
    for history in range(final.shape[1])
])
norms_before = np.sum(np.abs(initial) ** 2, axis=0)
norms_after = np.sum(np.abs(final) ** 2, axis=0)

incidence = np.zeros((SITES, len(edges)))
for edge_index, (u, v, _) in enumerate(edges):
    incidence[u, edge_index] = 1.0
    incidence[v, edge_index] = -1.0

history_residuals = q_after - q_before + np.einsum(
    "he,se->hs", integrated_currents, incidence, optimize=False
)
label_index = {label: index for index, label in enumerate(history_labels)}


def linear_combination(array, distance: int):
    return (
        array[label_index[f"11_d{distance}"]]
        - array[label_index[f"10_d{distance}"]]
        - array[label_index[f"01_d{distance}"]]
        + array[label_index["00"]]
    )


connected_rows = []
for distance, source_2 in SOURCE_2_BY_DISTANCE.items():
    delta_e_before = linear_combination(energies_before, distance)
    delta_e_after = linear_combination(energies_after, distance)
    delta_j = linear_combination(integrated_currents, distance)
    delta_q_before = linear_combination(q_before, distance)
    delta_q_after = linear_combination(q_after, distance)
    ledger_residual = delta_q_after - delta_q_before + np.einsum(
        "se,e->s", incidence, delta_j, optimize=False
    )
    if delta_e_after.real < -1e-12:
        energy_sign = "NEGATIVE"
    elif delta_e_after.real > 1e-12:
        energy_sign = "POSITIVE"
    else:
        energy_sign = "ZERO_TO_1E_12"
    connected_rows.append({
        "d": distance,
        "source_1": SOURCE_1,
        "source_2": source_2,
        "pair_representative": f"A0_A{distance}_ALONG_INTERNAL_RING",
        "delta12_E_initial": float(delta_e_before.real),
        "delta12_E_final": float(delta_e_after.real),
        "delta12_E_imag_abs_max": float(max(abs(delta_e_before.imag), abs(delta_e_after.imag))),
        "delta12_E_conservation_abs": float(abs(delta_e_after.real - delta_e_before.real)),
        "delta12_E_sign": energy_sign,
        "delta12_J": [float(value) for value in delta_j],
        "delta12_J_l1": float(np.sum(np.abs(delta_j))),
        "delta12_J_linf": float(np.max(np.abs(delta_j))),
        "delta12_J_signed_sum": float(np.sum(delta_j)),
        "delta12_q_before": [float(value) for value in delta_q_before],
        "delta12_q_after": [float(value) for value in delta_q_after],
        "delta12_q_terminal_sum": float(np.sum(delta_q_after)),
        "connected_ledger_residual_l1": float(np.sum(np.abs(ledger_residual))),
        "connected_ledger_residual_linf": float(np.max(np.abs(ledger_residual))),
        "current_interaction_status": (
            "NONZERO_CONNECTED_EDGE_CURRENT" if np.max(np.abs(delta_j)) > 1e-12
            else "ZERO_CONNECTED_EDGE_CURRENT_TO_1E_12"
        ),
    })

# Direct full-word action check at the evolved states. The active-sector
# result is embedded in all 4096 words and compared with the physical raw-hop
# action, without constructing a dense 4096-by-4096 matrix.
full_final = np.zeros((FULL_DIMENSION, len(history_labels)), dtype=np.complex128)
full_final[basis_words, :] = final
full_action = np.zeros_like(full_final)
for u, v, _ in edges:
    bit_u = (all_words >> u) & 1
    bit_v = (all_words >> v) & 1
    active = all_words[bit_u != bit_v]
    swapped = active ^ (1 << u) ^ (1 << v)
    full_action[active, :] -= full_final[swapped, :]
sector_action = np.einsum("ij,jh->ih", hamiltonian, final, optimize=False)
full_action_embedding_linf = float(np.max(np.abs(full_action[basis_words, :] - sector_action)))
outside_sector_action_linf = float(np.max(np.abs(full_action[particle_number > 2, :])))

antecedent_hashes = {str(path.relative_to(ROOT)): digest(path) for path in ANTECEDENTS}
expected_hashes = {str(path.relative_to(ROOT)): expected for path, expected in ANTECEDENTS.items()}
degree_census = [len(item) for item in neighbors]
checks = [
    (antecedent_hashes == expected_hashes, "immutable antecedent hashes"),
    (len(edges) == 3 * LENGTH, "owner-once edge census"),
    (degree_census == [3] * SITES, "degree-three prism"),
    (all(value is not None for value in distances), "connected support"),
    ({distance: distances[site] for distance, site in SOURCE_2_BY_DISTANCE.items()} == {1: 1, 2: 2, 3: 3}, "declared pair separations"),
    (dimension == 1 + SITES + SITES * (SITES - 1) // 2 == 79, "complete zero-one-two sector census"),
    (np.max(np.abs(hamiltonian - hamiltonian.conj().T)) == 0.0, "Hamiltonian Hermitian"),
    (all(np.max(np.abs(current - current.conj().T)) == 0.0 for current in current_operators), "edge currents Hermitian"),
    (float(np.max(np.abs(norms_before - 1.0))) < 5e-15, "initial norms"),
    (float(np.max(np.abs(norms_after - 1.0))) < 5e-14, "terminal norms"),
    (np.max(np.abs(energies_after.real - energies_before.real)) < 2e-14, "history energy conservation"),
    (np.max(np.abs(energies_after.imag)) < 2e-14, "history energy reality"),
    (np.max(np.sum(np.abs(history_residuals), axis=1)) < 2e-13, "all history ledgers"),
    (full_action_embedding_linf < 2e-15, "full-word Hamiltonian action embedding"),
    (outside_sector_action_linf == 0.0, "number-sector closure in full word space"),
    (all(abs(np.sum(q_before[label_index[f"10_d{distance}"]]) - 0.5) < 2e-15 for distance in SOURCE_2_BY_DISTANCE), "source-one authenticated half write"),
    (all(abs(np.sum(q_before[label_index[f"01_d{distance}"]]) - 0.5) < 2e-15 for distance in SOURCE_2_BY_DISTANCE), "source-two authenticated half write"),
    (all(abs(np.sum(q_before[label_index[f"11_d{distance}"]]) - 1.0) < 2e-15 for distance in SOURCE_2_BY_DISTANCE), "commuting two-write total"),
    (all(max(abs(value) for value in row["delta12_q_before"]) < 2e-15 for row in connected_rows), "additive initial occupation cancellation"),
    (all(abs(row["delta12_q_terminal_sum"]) < 2e-13 for row in connected_rows), "connected global number cancellation"),
    (all(row["connected_ledger_residual_l1"] < 3e-13 for row in connected_rows), "connected owner-once ledgers"),
    (all(row["delta12_E_conservation_abs"] < 2e-14 for row in connected_rows), "connected energy conservation"),
    (connected_rows[0]["delta12_E_sign"] == "NEGATIVE", "nearest-neighbor connected energy negative"),
    (all(row["delta12_E_sign"] == "ZERO_TO_1E_12" for row in connected_rows[1:]), "nonadjacent connected energies zero"),
    (all(row["current_interaction_status"] == "NONZERO_CONNECTED_EDGE_CURRENT" for row in connected_rows), "nonzero connected currents"),
]
failures = [label for passed, label in checks if not passed]

history_rows = []
for history, label in enumerate(history_labels):
    history_rows.append({
        "label": label,
        "source_sites": list(history_sources[label]),
        "source_write_total": 0.5 * len(history_sources[label]),
        "q_initial_sum": float(np.sum(q_before[history])),
        "q_final_sum": float(np.sum(q_after[history])),
        "energy_initial": float(energies_before[history].real),
        "energy_final": float(energies_after[history].real),
        "energy_imag_abs": float(abs(energies_after[history].imag)),
        "integrated_edge_currents": [float(value) for value in integrated_currents[history]],
        "q_final": [float(value) for value in q_after[history]],
        "ledger_residual_l1": float(np.sum(np.abs(history_residuals[history]))),
        "ledger_residual_linf": float(np.max(np.abs(history_residuals[history]))),
    })

out = {
    "schema": "R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION_V001",
    "classification": "FINITE_L6_VACUUM_TWO_AUTHENTICATED_WRITES__FOUR_HISTORY_CONNECTED_RESPONSE",
    "status": "PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT" if not failures else "FAIL_CLOSED",
    "antecedent_sha256": antecedent_hashes,
    "parameters": {
        "L": LENGTH,
        "sites": SITES,
        "full_word_dimension": FULL_DIMENSION,
        "exhaustive_active_sector_dimension": dimension,
        "kappa": KAPPA,
        "W_1": "1/2",
        "W_2": "1/2",
        "r0": "14441248/6075",
        "phi": "pi/4",
        "source_1": SOURCE_1,
        "source_2_by_graph_distance": {str(key): value for key, value in SOURCE_2_BY_DISTANCE.items()},
        "pair_orientation": "CANONICAL_A_RING_GEODESIC",
    },
    "topology": {
        "description": "DEGREE_THREE_PRISM__TWO_L_CYCLES_PLUS_L_DIAGONAL_CONNECTORS",
        "edges": [
            {"edge_index": index, "u": u, "v": v, "kind": kind}
            for index, (u, v, kind) in enumerate(edges)
        ],
        "source_1_distances": distances,
    },
    "write_protocol": {
        "baseline": "ALL_BLANK_VACUUM_ON_SAME_OWNER_ONCE_L6_PRISM",
        "local_map": "B_TO_B_MINUS_I_X_OVER_SQRT2",
        "terms_off_single_write_ledger": "DELTA_Q_PLUS_EDGE_FLUX_MINUS_W_EQUALS_ONE_HALF_PLUS_ZERO_MINUS_ONE_HALF_EQUALS_ZERO",
        "terms_off_double_write_ledger": "DELTA_Q_PLUS_EDGE_FLUX_MINUS_W1_MINUS_W2_EQUALS_ONE_PLUS_ZERO_MINUS_ONE_HALF_MINUS_ONE_HALF_EQUALS_ZERO",
        "transport": "WRITERS_AND_SOURCES_OFF__OWNER_ONCE_PRISM_HAMILTONIAN_ON_FOR_KAPPA_PI_OVER_2",
    },
    "connected_definition": {
        "observable": "DELTA12_O_EQUALS_O11_MINUS_O10_MINUS_O01_PLUS_O00",
        "energy": "EXPECTATION_OF_COMPLETE_OWNER_ONCE_NETWORK_HAMILTONIAN",
        "edge_current": "COMPLETE_VECTOR_OF_TIME_INTEGRATED_ORIENTED_OWNER_EDGE_CURRENTS",
        "ledger": "DELTA12_Q_AFTER_MINUS_DELTA12_Q_BEFORE_PLUS_B_DELTA12_J_EQUALS_RAW_NUMERICAL_REMAINDER",
    },
    "histories": history_rows,
    "connected_rows": connected_rows,
    "numerical_controls": {
        "method": "EXACT_HERMITIAN_SPECTRAL_EVOLUTION_AND_ANALYTIC_CURRENT_TIME_INTEGRAL_ON_THE_COMPLETE_REACHABLE_0_1_2_NUMBER_SECTORS__EMBEDDED_IN_ALL_4096_WORDS",
        "history_norm_error_max": float(max(np.max(np.abs(norms_before - 1.0)), np.max(np.abs(norms_after - 1.0)))),
        "history_energy_error_max": float(np.max(np.abs(energies_after.real - energies_before.real))),
        "history_ledger_residual_l1_max": float(np.max(np.sum(np.abs(history_residuals), axis=1))),
        "full_word_action_embedding_linf": full_action_embedding_linf,
        "outside_active_sector_action_linf": outside_sector_action_linf,
        "connected_ledger_residual_l1_max": float(max(row["connected_ledger_residual_l1"] for row in connected_rows)),
    },
    "interpretation": {
        "connected_current": "NONZERO_AT_ALL_THREE_CANONICAL_SEPARATIONS_ON_THIS_FINITE_TIME_SLICE",
        "connected_energy": "NEGATIVE_DIRECT_CONTACT_AT_D1__ZERO_TO_1E_12_AT_D2_AND_D3",
        "binding_test": "NO_MUTUAL_ATTRACTIVE_BINDING_ACROSS_D1_D2_D3__ONLY_NEAREST_NEIGHBOR_CONTACT_ENERGY_IS_NEGATIVE",
        "exchange_potential": "NOT_ESTABLISHED__A_NONZERO_FINITE_CONNECTED_CURRENT_IS_NOT_BY_ITSELF_A_SEPARATION_DEPENDENT_ENERGY_POTENTIAL",
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "claim_classes": {
        "proved": "OWNER_ONCE_L6_PRISM_CENSUS__EXACT_BLANK_TARGET_WRITE_LEDGERS__FOUR_HISTORY_INCLUSION_EXCLUSION_IDENTITY__NUMBER_SECTOR_COMPLETENESS",
        "adopted": "F3_MDC_ALPHA_EQUALS_R0__CANONICAL_A_RING_PAIR_REPRESENTATIVES__KAPPA_PI_OVER_2",
        "conditional": "ALL_BLANK_VACUUM_PARENT__DECLARED_PAIR_ORIENTATION__SOURCE_AND_TRANSPORT_SCHEDULE",
        "empirical": "BINARY64_FINITE_L6_ENERGY_CURRENT_AND_LEDGER_VALUES",
        "open": "INDEPENDENT_HOSTILE_AUDIT__OTHER_PAIR_ORBITS__LARGER_L__PHYSICAL_DISTANCE__SEPARATION_POTENTIAL__BINDING__GATE_A_P",
    },
    "not_claimed": "LONG_RANGE_EXCHANGE_POTENTIAL__MUTUAL_BINDING__SCALING_LAW__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5e-13:
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
print(f"PASS__R_GATE_AP_L6_TWO_BODY_CONNECTED_INTERACTION__{len(checks)}/{len(checks)}")
print(f"OBSERVED_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"OBSERVED_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
