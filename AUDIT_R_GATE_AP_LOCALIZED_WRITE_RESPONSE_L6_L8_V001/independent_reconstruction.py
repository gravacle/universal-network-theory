#!/usr/bin/env python3
"""Independent RK4 reconstruction of direct finite L6/L8 response histories."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import resource
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "INDEPENDENT_RESULT.json"
TARGET = ROOT / "DEVELOPMENT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001"
PROTOCOL = ROOT / "DEVELOPMENT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001" / "RESULT.json"
PROTOCOL_AUDIT = ROOT / "AUDIT_R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001" / "RESULT.json"
BASELINES = {
    6: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json",
    8: ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json",
}
DIRECT = {length: TARGET / f"RESULT_L{length}.json" for length in (6, 8)}
PINS = {
    TARGET / "README.md": "d31e7c40a1df78b10e799fa6b082c6a5cd0d8e36e58bc7a8b9d423ce13395421",
    TARGET / "THEOREM.md": "50f0bbdb39a72ca4f1297a66e297aeae6f0347c5762de3d0feb25f2826ccab0e",
    TARGET / "RUN_OBSERVATION.md": "2583c60769379f72cd18bbca71ed4bf3785fd348186031da6637a5255b02c892",
    TARGET / "compute_direct_response.py": "2050a2f73de7cca0d2c1c59e4737e11a89bf125177eceedf292e5fcef2626368",
    TARGET / "compile_results.py": "1160081f62a6419b7f4592fd2f54ecfd005b79b18235d4717f1ff8befc7eac47",
    TARGET / "RESULT_L6.json": "8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a",
    TARGET / "RESULT_L8.json": "b73ba9e1c660a5285a075fd8c040c6b04621e4badc0dbecf42483d5c0a1c72fb",
    TARGET / "RESULT.json": "eb6dd30ddba32c9278dfc54794d4b3bc374a38568d867c9ed00c1004e64dbe49",
    PROTOCOL: "315efc89e91ccb2816787716f7a724e76f292a9a689a11f80f18f4dd337deb90",
    PROTOCOL_AUDIT: "5edd62c053e28fa5b17475df533a4e732c29533792ea9da96e5e664b96f003b9",
    BASELINES[6]: "e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
    BASELINES[8]: "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
}
NOT_CLAIMED = (
    "FULL_L6_TO_L14_PROFILE_CLASSIFICATION__SCALING_LAW__LOCALITY_LAW__"
    "PHYSICAL_BOUNDARY_REFLECTION__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY"
)
KAPPA = math.pi / 2.0
COARSE_STEPS = 1024
FINE_STEPS = 2048
STARTED = time.perf_counter()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def support_edges(length: int):
    """Two directed cycles followed by the owner-once diagonal matching."""
    edges = []
    for ring in range(2):
        for site in range(length):
            edges.append((ring * length + site,
                          ring * length + (site + 1) % length,
                          "internal"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def graph_data(site_count: int, edges):
    neighbors = [set() for _ in range(site_count)]
    for left, right, _ in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    distances = [None] * site_count
    distances[0] = 0
    queue = deque([0])
    while queue:
        left = queue.popleft()
        for right in neighbors[left]:
            if distances[right] is None:
                distances[right] = distances[left] + 1
                queue.append(right)
    return neighbors, distances


def compatible(observed, expected, tolerance=5e-9, path="root"):
    if isinstance(expected, dict):
        if not isinstance(observed, dict) or set(observed) != set(expected):
            raise AssertionError(f"keys differ at {path}")
        for key in expected:
            compatible(observed[key], expected[key], tolerance, f"{path}.{key}")
    elif isinstance(expected, list):
        if not isinstance(observed, list) or len(observed) != len(expected):
            raise AssertionError(f"list differs at {path}")
        for index, (left, right) in enumerate(zip(observed, expected)):
            compatible(left, right, tolerance, f"{path}[{index}]")
    elif isinstance(expected, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - expected) > tolerance:
            raise AssertionError(f"float differs at {path}: {observed} vs {expected}")
    elif observed != expected:
        raise AssertionError(f"value differs at {path}: {observed} vs {expected}")


def reconstruct(length: int):
    site_count = 2 * length
    dimension = 1 << site_count
    words = np.arange(dimension, dtype=np.int64)
    edges = support_edges(length)
    neighbors, distances = graph_data(site_count, edges)

    # Store each hopping pair only once (u occupied, v blank).  This differs
    # from the target's doubled active-index current contraction.
    pairs = []
    for left, right, kind in edges:
        left_one = ((words >> left) & 1) == 1
        right_zero = ((words >> right) & 1) == 0
        ten = words[left_one & right_zero]
        zero_one = ten ^ (1 << left) ^ (1 << right)
        pairs.append((ten, zero_one, kind))

    def hamiltonian(states):
        result = np.zeros_like(states)
        for ten, zero_one, _ in pairs:
            result[ten] -= states[zero_one]
            result[zero_one] -= states[ten]
        return result

    def currents(states):
        result = np.empty((states.shape[1], len(edges)), dtype=float)
        for edge_index, (ten, zero_one, _) in enumerate(pairs):
            # <J_uv> = 2 Im(conj(psi_10) psi_01) for the target orientation.
            product = np.conjugate(states[ten]) * states[zero_one]
            result[:, edge_index] = 2.0 * np.sum(product.imag, axis=0)
        return result

    def rk4(initial, step_count, label):
        step = KAPPA / step_count
        states = initial.copy()
        integrated = currents(states)
        quarter = max(1, step_count // 4)
        for index in range(1, step_count + 1):
            k1 = -1j * hamiltonian(states)
            k2 = -1j * hamiltonian(states + 0.5 * step * k1)
            k3 = -1j * hamiltonian(states + 0.5 * step * k2)
            k4 = -1j * hamiltonian(states + step * k3)
            states += (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
            integrated += weight * currents(states)
            if index % quarter == 0:
                print(f"PROGRESS_L{length}_{label}={index}/{step_count}", flush=True)
        return states, integrated * step / 3.0

    # The baseline has blank even tails and (B+X)/sqrt(2) on odd heads.
    # The perturbed history independently tensors (B-iX)/sqrt(2) at site zero.
    even_mask = sum(1 << site for site in range(0, site_count, 2))
    baseline = np.zeros(dimension, dtype=np.complex128)
    baseline[(words & even_mask) == 0] = 1.0 / math.sqrt(1 << length)
    perturbed = np.zeros(dimension, dtype=np.complex128)
    allowed = (words & (even_mask ^ 1)) == 0
    normalization = math.sqrt(1 << (length + 1))
    perturbed[allowed] = np.where((words[allowed] & 1) == 0, 1.0, -1.0j) / normalization
    initial = np.column_stack((baseline, perturbed))

    coarse_states, coarse_integrated = rk4(initial, COARSE_STEPS, "COARSE")
    fine_states, fine_integrated = rk4(initial, FINE_STEPS, "FINE")

    bit_columns = [((words >> site) & 1).astype(float) for site in range(site_count)]

    def occupations(states):
        probabilities = abs(states) ** 2
        return np.array([
            [float(np.dot(bit_columns[site], probabilities[:, history]))
             for site in range(site_count)]
            for history in range(states.shape[1])
        ])

    q_initial = occupations(initial)
    q_coarse = occupations(coarse_states)
    q_fine = occupations(fine_states)
    delta_q = q_fine[1] - q_fine[0]
    delta_current = fine_integrated[1] - fine_integrated[0]
    incidence = np.zeros((site_count, len(edges)))
    for edge_index, (left, right, _) in enumerate(edges):
        incidence[left, edge_index] = 1.0
        incidence[right, edge_index] = -1.0
    history_residual = q_fine - q_initial + fine_integrated @ incidence.T
    source = np.zeros(site_count)
    source[0] = 0.5
    differential_residual = delta_q + incidence @ delta_current - source

    shells = []
    for radius in sorted(set(min(distances[left], distances[right])
                             for left, right, _ in edges)):
        for kind in ("internal", "connector"):
            indices = [
                index for index, (left, right, edge_kind) in enumerate(edges)
                if edge_kind == kind
                and min(distances[left], distances[right]) == radius
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
                "l1_sum_abs_delta_J": float(np.sum(abs(values))),
                "mean_abs_delta_J": float(np.mean(abs(values))),
                "max_abs_delta_J": float(np.max(abs(values))),
            })

    kinds = [kind for _, _, kind in edges]
    connector_indices = [index for index, kind in enumerate(kinds) if kind == "connector"]
    delta_j_l1 = float(np.sum(abs(delta_current)))
    summary = {
        "delta_q_terminal_sum": float(np.sum(delta_q)),
        "delta_J_l1": delta_j_l1,
        "delta_J_linf": float(np.max(abs(delta_current))),
        "total_absolute_throughput_change": float(
            np.sum(abs(fine_integrated[1])) - np.sum(abs(fine_integrated[0]))
        ),
        "connector_absolute_throughput_change": float(
            np.sum(abs(fine_integrated[1, connector_indices]))
            - np.sum(abs(fine_integrated[0, connector_indices]))
        ),
        "mean_edge_radius_abs_delta_J": float(sum(
            min(distances[left], distances[right]) * abs(delta_current[index])
            for index, (left, right, _) in enumerate(edges)
        ) / delta_j_l1),
        "effective_responding_edge_count": float(
            delta_j_l1 ** 2 / np.sum(delta_current ** 2)
        ),
        "max_site_graph_distance": max(distances),
    }

    target = json.loads(DIRECT[length].read_text())
    target_baseline_q = np.array([row["baseline_q_after"] for row in target["site_records"]])
    target_perturbed_q = np.array([row["perturbed_q_after"] for row in target["site_records"]])
    target_delta_q = np.array([row["delta_q_after"] for row in target["site_records"]])
    target_baseline_j = np.array([row["baseline_J"] for row in target["edge_records"]])
    target_perturbed_j = np.array([row["perturbed_J"] for row in target["edge_records"]])
    target_delta_j = np.array([row["delta_J"] for row in target["edge_records"]])
    shell_numeric_linf = max(
        abs(float(observed[key]) - float(expected[key]))
        for observed, expected in zip(shells, target["radial_edge_profile"])
        for key in ("signed_sum_delta_J", "l1_sum_abs_delta_J",
                    "mean_abs_delta_J", "max_abs_delta_J")
    )
    baseline_record = json.loads(BASELINES[length].read_text())
    baseline_q_reference = np.array(baseline_record["q_after"])
    baseline_j_reference = np.array(baseline_record["integrated_oriented_currents"])

    h_initial = hamiltonian(initial)
    h_final = hamiltonian(fine_states)
    energy_initial = np.sum(np.conjugate(initial) * h_initial, axis=0)
    energy_final = np.sum(np.conjugate(fine_states) * h_final, axis=0)
    norms = np.sum(abs(fine_states) ** 2, axis=0)
    popcount = np.array([bin(int(word)).count("1") for word in words])
    number_before = np.array([
        [np.sum(abs(initial[popcount == number, history]) ** 2)
         for number in range(site_count + 1)]
        for history in range(2)
    ])
    number_after = np.array([
        [np.sum(abs(fine_states[popcount == number, history]) ** 2)
         for number in range(site_count + 1)]
        for history in range(2)
    ])

    target_reproduction = {
        "baseline_q_linf": float(np.max(abs(q_fine[0] - target_baseline_q))),
        "perturbed_q_linf": float(np.max(abs(q_fine[1] - target_perturbed_q))),
        "delta_q_linf": float(np.max(abs(delta_q - target_delta_q))),
        "baseline_J_linf": float(np.max(abs(fine_integrated[0] - target_baseline_j))),
        "perturbed_J_linf": float(np.max(abs(fine_integrated[1] - target_perturbed_j))),
        "delta_J_linf": float(np.max(abs(delta_current - target_delta_j))),
        "baseline_sealed_q_linf": float(np.max(abs(q_fine[0] - baseline_q_reference))),
        "baseline_sealed_J_linf": float(np.max(abs(fine_integrated[0] - baseline_j_reference))),
        "radial_shell_numeric_linf": shell_numeric_linf,
    }
    independent_controls = {
        "state_coarse_fine_linf": float(np.max(abs(fine_states - coarse_states))),
        "q_coarse_fine_linf": float(np.max(abs(q_fine - q_coarse))),
        "J_coarse_fine_linf": float(np.max(abs(fine_integrated - coarse_integrated))),
        "baseline_transport_residual_l1": float(np.sum(abs(history_residual[0]))),
        "perturbed_transport_residual_l1": float(np.sum(abs(history_residual[1]))),
        "full_differential_residual_l1": float(np.sum(abs(differential_residual))),
        "full_differential_residual_linf": float(np.max(abs(differential_residual))),
        "norm_error_linf": float(np.max(abs(norms - 1.0))),
        "energy_change_linf": float(np.max(abs(energy_final.real - energy_initial.real))),
        "energy_imag_linf": float(np.max(abs(energy_final.imag))),
        "number_law_change_linf": float(np.max(abs(number_after - number_before))),
    }
    structure_checks = {
        "edge_count": len(edges),
        "connector_count": sum(kind == "connector" for kind in kinds),
        "degree_set": sorted(set(len(item) for item in neighbors)),
        "all_sites_reached": all(distance is not None for distance in distances),
        "incidence_column_sum_linf": float(np.max(abs(np.sum(incidence, axis=0)))),
        "shell_edge_count": sum(shell["edge_count"] for shell in shells),
        "all_delta_J_nonzero_at_1e_minus_10": bool(np.all(abs(delta_current) > 1e-10)),
    }
    vectors = {
        "baseline_q_after": q_fine[0].tolist(),
        "perturbed_q_after": q_fine[1].tolist(),
        "delta_q_after": delta_q.tolist(),
        "baseline_J": fine_integrated[0].tolist(),
        "perturbed_J": fine_integrated[1].tolist(),
        "delta_J": delta_current.tolist(),
    }
    print(f"COMPLETE_L{length}", flush=True)
    return {
        "L": length,
        "method": "MATRIX_FREE_CLASSICAL_RK4__SINGLE_HOPPING_PAIR_CONTRACTION__COMPOSITE_SIMPSON_CURRENT",
        "steps": {"coarse": COARSE_STEPS, "fine": FINE_STEPS},
        "vectors": vectors,
        "radial_edge_profile": shells,
        "summary": summary,
        "target_reproduction": target_reproduction,
        "independent_controls": independent_controls,
        "structure_checks": structure_checks,
    }


if any(digest(path) != expected for path, expected in PINS.items()):
    raise AssertionError("target or antecedent custody mismatch")
protocol = json.loads(PROTOCOL.read_text())
protocol_audit = json.loads(PROTOCOL_AUDIT.read_text())
target_compiled = json.loads((TARGET / "RESULT.json").read_text())
target_direct = {length: json.loads(DIRECT[length].read_text()) for length in (6, 8)}

rows = [reconstruct(length) for length in (6, 8)]

# Recompile the target summary without importing its compiler.
compiled_rows = []
for length in (6, 8):
    result = target_direct[length]
    by_radius = defaultdict(float)
    by_radius_kind = {}
    for shell in result["radial_edge_profile"]:
        by_radius[shell["r"]] += shell["l1_sum_abs_delta_J"]
        by_radius_kind[f"r{shell['r']}__{shell['kind']}"] = shell["l1_sum_abs_delta_J"]
    response = result["response_summary"]
    controls = result["numerical_controls"]
    compiled_rows.append({
        "L": length,
        "delta_q_terminal_sum": response["delta_q_terminal_sum"],
        "delta_J_l1": response["delta_J_l1"],
        "delta_J_linf": response["delta_J_linf"],
        "total_absolute_throughput_change": response["total_absolute_throughput_change"],
        "connector_absolute_throughput_change": response["connector_absolute_throughput_change"],
        "mean_edge_radius_abs_delta_J": response["mean_edge_radius_abs_delta_J"],
        "effective_responding_edge_count": response["effective_responding_edge_count"],
        "edge_profile_l1_by_radius": {str(radius): by_radius[radius] for radius in sorted(by_radius)},
        "edge_profile_l1_by_radius_and_kind": by_radius_kind,
        "full_differential_residual_l1": controls["full_differential_residual_l1"],
        "full_differential_residual_linf": controls["full_differential_residual_linf"],
    })

recompiled = {
    "schema": "R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001",
    "classification": "DIRECT_FULL_SPACE_FINITE_RESPONSE_ROWS__LOWER_SIZE_MARKED_SOURCE_ENGINE_REFERENCE",
    "input_sha256": {
        "RESULT_L6.json": PINS[DIRECT[6]],
        "RESULT_L8.json": PINS[DIRECT[8]],
    },
    "source": "AUTHENTICATED_W_R_EQUALS_ONE_HALF_ON_BASELINE_BLANK_EVEN_SITE_ZERO",
    "rows": compiled_rows,
    "finite_profile_description": "NONUNIFORM_OSCILLATORY_SPREADING_ACROSS_ALL_EDGE_SHELLS__RADIUS_TWO_L1_EXCEEDS_FARTHEST_EDGE_SHELL_AT_L6_AND_L8__NO_PHYSICAL_BOUNDARY_CLASSIFICATION",
    "checks_passed": 16,
    "checks_total": 16,
    "failures": [],
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_DIFFERENTIAL_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "claim_classes": {
        "proved": "AUTHENTICATED_SOURCE_WRITE_LEDGER__FINITE_OWNER_INCIDENCE_AND_PROFILE_PARTITIONS",
        "conditional": "SUPPORT__KAPPA__CONTENT__ROUTING__READ",
        "empirical": "DIRECT_REFINED_L6_AND_L8_DIFFERENTIAL_OCCUPATION_CURRENT_AND_RADIAL_PROFILES",
        "open": "INDEPENDENT_HOSTILE_AUDIT__L10_L12_L14_RESPONSE__FULL_LADDER_PROFILE_CLASSIFICATION__PHYSICAL_DISTANCE__GATE_A_P",
    },
    "not_claimed": "LOCALITY_OR_SCALING_LAW__UNIFORM_OR_ASYMPTOTIC_PROFILE__PHYSICAL_BOUNDARY_REFLECTION__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
}

checks = [
    (protocol["checks_passed"] == protocol["checks_total"] == 20, "protocol target 20/20"),
    (protocol_audit["independent_checks"] == "35/35", "protocol hostile audit 35/35"),
    (protocol_audit["Gate_A_P"] == "OPEN", "protocol Gate A-P open"),
    (all(target_direct[length]["checks_passed"] == target_direct[length]["checks_total"] == 24 for length in (6, 8)), "direct targets 24/24"),
    (target_compiled["checks_passed"] == target_compiled["checks_total"] == 16, "compiled target 16/16"),
    (recompiled == target_compiled, "independent exact compilation"),
    (all(row["structure_checks"]["edge_count"] == 3 * row["L"] for row in rows), "owner-once edge census"),
    (all(row["structure_checks"]["connector_count"] == row["L"] for row in rows), "connector census"),
    (all(row["structure_checks"]["degree_set"] == [3] and row["structure_checks"]["all_sites_reached"] for row in rows), "connected degree-three supports"),
    (all(row["structure_checks"]["incidence_column_sum_linf"] == 0.0 for row in rows), "owner-once incidence telescope"),
    (all(row["structure_checks"]["shell_edge_count"] == 3 * row["L"] for row in rows), "complete radial partitions"),
    (all(row["structure_checks"]["all_delta_J_nonzero_at_1e_minus_10"] for row in rows), "every finite edge responds"),
    (all(max(row["target_reproduction"].values()) < 2e-8 for row in rows), "complete target vector/profile reproduction"),
    (all(row["target_reproduction"]["baseline_sealed_q_linf"] < 2e-8 for row in rows), "sealed baseline q reproduction"),
    (all(row["target_reproduction"]["baseline_sealed_J_linf"] < 2e-8 for row in rows), "sealed baseline J reproduction"),
    (all(row["independent_controls"]["state_coarse_fine_linf"] < 2e-8 for row in rows), "independent state refinement"),
    (all(row["independent_controls"]["q_coarse_fine_linf"] < 2e-8 for row in rows), "independent q refinement"),
    (all(row["independent_controls"]["J_coarse_fine_linf"] < 2e-8 for row in rows), "independent J refinement"),
    (all(row["independent_controls"]["baseline_transport_residual_l1"] < 2e-8 for row in rows), "independent baseline ledgers"),
    (all(row["independent_controls"]["perturbed_transport_residual_l1"] < 2e-8 for row in rows), "independent perturbed ledgers"),
    (all(row["independent_controls"]["full_differential_residual_l1"] < 2e-8 for row in rows), "independent full differential ledgers"),
    (all(abs(row["summary"]["delta_q_terminal_sum"] - 0.5) < 2e-8 for row in rows), "global source retention"),
    (all(row["independent_controls"]["norm_error_linf"] < 2e-8 for row in rows), "independent norm control"),
    (all(row["independent_controls"]["energy_change_linf"] < 2e-8 for row in rows), "independent energy control"),
    (all(row["independent_controls"]["number_law_change_linf"] < 2e-8 for row in rows), "independent number-law control"),
    (all(sum(shell["l1_sum_abs_delta_J"] for shell in row["radial_edge_profile"] if shell["r"] == 2)
         > sum(shell["l1_sum_abs_delta_J"] for shell in row["radial_edge_profile"] if shell["r"] == max(item["r"] for item in row["radial_edge_profile"])) for row in rows), "radius-two aggregate exceeds farthest shell"),
    (all(target_direct[length]["residual_status"].endswith("NOT_CALLED_DEFECTS") for length in (6, 8)), "raw residual classification"),
    (all(target_direct[length]["profile_status"].endswith("NOT_PHYSICAL_RADIUS_OR_GRID") for length in (6, 8)), "finite support distance classification"),
    (all(target_direct[length]["not_claimed"] == NOT_CLAIMED for length in (6, 8)), "direct structured claim ceiling"),
    ("LOCALITY_OR_SCALING_LAW" in target_compiled["not_claimed"] and "GRAVITY" in target_compiled["not_claimed"], "compiled structured claim ceiling"),
]
failures = [label for passed, label in checks if not passed]

run_observation = (TARGET / "RUN_OBSERVATION.md").read_text()
out = {
    "schema": "AUDIT_R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001",
    "verdict": "PASS__INDEPENDENT_FULL_SPACE_L6_L8_RESPONSE_RECONSTRUCTION" if not failures else "FAIL_CLOSED",
    "method": "MATRIX_FREE_CLASSICAL_RK4__ONE_HOPPING_PAIR_PER_EDGE__COMPOSITE_SIMPSON__NO_TARGET_COMPUTE_IMPORT",
    "input_sha256": {path.relative_to(ROOT).as_posix(): expected for path, expected in PINS.items()},
    "rows": rows,
    "compiled_result": {
        "exactly_reconstructed": recompiled == target_compiled,
        "canonical_json_sha256": canonical_digest(recompiled),
    },
    "run_observation_custody": {
        "document_sha256": PINS[TARGET / "RUN_OBSERVATION.md"],
        "environment_matches_current_host": platform.system() == "Darwin" and platform.machine() == "arm64" and sys.version_info[:3] == (3, 9, 6),
        "python_3_9_int_bit_count_absent": not hasattr(int, "bit_count"),
        "failed_attempt_independently_replayable": False,
        "failed_attempt_status": "DOCUMENTED_FAIL_CLOSED_BEFORE_RESULT_EMISSION__NO_FAILED_VALUE_PROMOTED",
        "declared_runs": {
            "L6_canonical": {"runtime_seconds": 24.111255334, "max_rss_bytes": 28655616},
            "L6_optimized_replay": {"runtime_seconds": 22.340707750, "max_rss_bytes": 28819456},
            "L8_canonical_optimized": {"runtime_seconds": 451.841224708, "max_rss_bytes": 88162304},
            "L8_prior_allocation_heavy": {"runtime_seconds": 492.273888208, "max_rss_bytes": 85032960},
        },
        "document_contains_all_declared_values": all(token in run_observation for token in (
            "24.111255334", "28,655,616", "22.340707750", "28,819,456",
            "451.841224708", "88,162,304", "492.273888208", "85,032,960",
        )),
        "classification": "PINNED_SINGLE_ENVIRONMENT_OBSERVATIONS__NOT_COMPLEXITY_LAWS",
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "profile_conclusion": "LOWER_SIZE_NONUNIFORM_OSCILLATORY_SPREADING_ONLY__FULL_LADDER_CLASSIFICATION_OPEN",
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_DIFFERENTIAL_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "Gate_A_P": "OPEN",
    "not_claimed": "LOCALITY_OR_SCALING_LAW__PHYSICAL_BOUNDARY_REFLECTION__GRID_OR_PHYSICAL_DISTANCE__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
}

if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    print("INDEPENDENT_RESULT_BEGIN")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("INDEPENDENT_RESULT_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__HOSTILE_LOCALIZED_WRITE_RESPONSE_L6_L8__{len(checks)}/{len(checks)}")
print(f"INDEPENDENT_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"INDEPENDENT_MAX_RSS_BYTES={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
