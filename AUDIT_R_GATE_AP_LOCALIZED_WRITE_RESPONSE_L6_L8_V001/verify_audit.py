#!/usr/bin/env python3
"""Pinned hostile verifier for the direct finite L6/L8 response audit."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from collections import defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
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
    DIRECT[6]: "8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a",
    DIRECT[8]: "b73ba9e1c660a5285a075fd8c040c6b04621e4badc0dbecf42483d5c0a1c72fb",
    TARGET / "RESULT.json": "eb6dd30ddba32c9278dfc54794d4b3bc374a38568d867c9ed00c1004e64dbe49",
    PROTOCOL: "315efc89e91ccb2816787716f7a724e76f292a9a689a11f80f18f4dd337deb90",
    PROTOCOL_AUDIT: "5edd62c053e28fa5b17475df533a4e732c29533792ea9da96e5e664b96f003b9",
    BASELINES[6]: "e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
    BASELINES[8]: "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
    HERE / "README.md": "4e7c7b0a0671e6bea032211b48fcd62a4d9a64d59bcc931c8e3d9f82ea439c9e",
    HERE / "REPORT.md": "1320fed787d2e47b74687b87eede1ca2c9fb78c6bc3097b1fd7101ae9a427843",
    HERE / "RESULT.md": "f055d56fc562200b3a9ec309611e1f412ccadba5a5c0c559378f4d87535bfac0",
    HERE / "RESULT.json": "45b88fe34d459b81246ed289040a8b9824e45f75caa47b9c0836c2ff7772060a",
    HERE / "INDEPENDENT_RESULT.json": "43d0fc947022b1a316b838c94d1fdc8f659b68b44a8fcb052d1c79c07bce0238",
    HERE / "independent_reconstruction.py": "7be8866f651aa11fff5282fc481c02b942841f01d30db8513faef3372932a294",
}
DIRECT_NOT_CLAIMED = (
    "FULL_L6_TO_L14_PROFILE_CLASSIFICATION__SCALING_LAW__LOCALITY_LAW__"
    "PHYSICAL_BOUNDARY_REFLECTION__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY"
)
AUDIT_NOT_CLAIMED = (
    "LOCALITY_OR_SCALING_LAW__PHYSICAL_BOUNDARY_REFLECTION__"
    "GRID_OR_PHYSICAL_DISTANCE__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def edges_for(length: int):
    edges = []
    for ring in range(2):
        for site in range(length):
            edges.append((ring * length + site,
                          ring * length + (site + 1) % length,
                          "internal"))
    edges.extend((site, length + (site + 1) % length, "connector")
                 for site in range(length))
    return edges


def distances_for(site_count, edges):
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


checks = []


def check(condition, label):
    checks.append((bool(condition), label))


check(all(digest(path) == expected for path, expected in PINS.items()), "all custody pins")
protocol = json.loads(PROTOCOL.read_text())
protocol_audit = json.loads(PROTOCOL_AUDIT.read_text())
target_direct = {length: json.loads(DIRECT[length].read_text()) for length in (6, 8)}
target_compiled = json.loads((TARGET / "RESULT.json").read_text())
baselines = {length: json.loads(BASELINES[length].read_text()) for length in (6, 8)}
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
summary = json.loads((HERE / "RESULT.json").read_text())

check(protocol["checks_passed"] == protocol["checks_total"] == 20, "protocol target 20/20")
check(protocol_audit["independent_checks"] == "35/35", "protocol hostile audit 35/35")
check(protocol_audit["Gate_A_P"] == "OPEN", "protocol Gate A-P open")
check(independent["checks_passed"] == independent["checks_total"] == 30, "independent reconstruction 30/30")
check(independent["verdict"] == "PASS__INDEPENDENT_FULL_SPACE_L6_L8_RESPONSE_RECONSTRUCTION", "independent verdict")
check(not independent["failures"], "independent failures empty")
check(summary["verdict"] == independent["verdict"], "summary verdict")
check(summary["independent_checks"] == "30/30", "summary independent count")

independent_rows = {row["L"]: row for row in independent["rows"]}
recompiled_rows = []
for length in (6, 8):
    target = target_direct[length]
    row = independent_rows[length]
    edges = edges_for(length)
    neighbors, distances = distances_for(2 * length, edges)
    site_records = target["site_records"]
    edge_records = target["edge_records"]
    q0 = [item["baseline_q_after"] for item in site_records]
    q1 = [item["perturbed_q_after"] for item in site_records]
    dq = [item["delta_q_after"] for item in site_records]
    q0_before = [item["baseline_q_before"] for item in site_records]
    q1_before = [item["perturbed_q_before"] for item in site_records]
    j0 = [item["baseline_J"] for item in edge_records]
    j1 = [item["perturbed_J"] for item in edge_records]
    dj = [item["delta_J"] for item in edge_records]
    incidence = [[0.0] * len(edges) for _ in range(2 * length)]
    for edge_index, (left, right, _) in enumerate(edges):
        incidence[left][edge_index] = 1.0
        incidence[right][edge_index] = -1.0
    residual0 = [
        q0[site] - q0_before[site]
        + sum(incidence[site][edge] * j0[edge] for edge in range(len(edges)))
        for site in range(2 * length)
    ]
    residual1 = [
        q1[site] - q1_before[site]
        + sum(incidence[site][edge] * j1[edge] for edge in range(len(edges)))
        for site in range(2 * length)
    ]
    differential_residual = [
        dq[site]
        + sum(incidence[site][edge] * dj[edge] for edge in range(len(edges)))
        - (0.5 if site == 0 else 0.0)
        for site in range(2 * length)
    ]
    controls = target["numerical_controls"]

    check(target["checks_passed"] == target["checks_total"] == 24, f"L{length} target 24/24")
    check(not target["failures"], f"L{length} target failures empty")
    check(target["sealed_baseline_sha256"] == PINS[BASELINES[length]], f"L{length} baseline pin")
    check(len(site_records) == 2 * length and len(edge_records) == 3 * length, f"L{length} complete vector census")
    check([(item["u"], item["v"], item["kind"]) for item in edge_records] == edges, f"L{length} edge order")
    check(all(item["r"] == distances[item["site"]] for item in site_records), f"L{length} site BFS radii")
    check(all(item["r"] == min(distances[item["u"]], distances[item["v"]]) for item in edge_records), f"L{length} edge BFS radii")
    check(all(len(item) == 3 for item in neighbors) and all(value is not None for value in distances), f"L{length} support connected degree three")
    check(max(abs(q1[index] - q0[index] - dq[index]) for index in range(2 * length)) == 0.0, f"L{length} q difference identity")
    check(max(abs(j1[index] - j0[index] - dj[index]) for index in range(3 * length)) == 0.0, f"L{length} J difference identity")
    expected_q0_before = [0.0 if site % 2 == 0 else 0.5 for site in range(2 * length)]
    expected_q1_before = expected_q0_before.copy()
    expected_q1_before[0] = 0.5
    check(max(abs(left - right) for left, right in zip(q0_before, expected_q0_before)) < 1e-14, f"L{length} baseline initial occupations")
    check(max(abs(left - right) for left, right in zip(q1_before, expected_q1_before)) < 1e-14, f"L{length} inserted initial occupations")
    check(abs(sum(dq) - target["response_summary"]["delta_q_terminal_sum"]) < 2e-15, f"L{length} terminal source arithmetic")
    check(abs(sum(dq) - 0.5) < 1e-10, f"L{length} half-record retention")
    check(abs(sum(abs(value) for value in residual0) - controls["baseline_transport_residual_l1"]) < 3e-15, f"L{length} baseline ledger recomputation")
    check(abs(sum(abs(value) for value in residual1) - controls["perturbed_transport_residual_l1"]) < 3e-15, f"L{length} perturbed ledger recomputation")
    check(abs(sum(abs(value) for value in differential_residual) - controls["full_differential_residual_l1"]) < 3e-15, f"L{length} differential ledger L1 recomputation")
    check(abs(max(abs(value) for value in differential_residual) - controls["full_differential_residual_linf"]) < 3e-15, f"L{length} differential ledger Linf recomputation")
    check(controls["full_differential_residual_l1"] < 2e-11, f"L{length} target ledger control")
    check(max(controls["state_refinement_linf"], controls["occupation_refinement_linf"], controls["current_refinement_linf"]) < 2e-10, f"L{length} target refinement")
    check(max(controls["norm_error_max"], controls["energy_error_max"], controls["energy_imag_abs_max"], controls["number_law_max_change"]) < 2e-10, f"L{length} target conservation")
    check(max(abs(q0[index] - baselines[length]["q_after"][index]) for index in range(2 * length)) < 2e-11, f"L{length} sealed baseline q")
    check(max(abs(j0[index] - baselines[length]["integrated_oriented_currents"][index]) for index in range(3 * length)) < 2e-11, f"L{length} sealed baseline J")
    check(all(abs(value) > 1e-10 for value in dj), f"L{length} every edge response nonzero")

    independent_vectors = row["vectors"]
    target_vectors = {
        "baseline_q_after": q0,
        "perturbed_q_after": q1,
        "delta_q_after": dq,
        "baseline_J": j0,
        "perturbed_J": j1,
        "delta_J": dj,
    }
    for key, target_vector in target_vectors.items():
        check(len(independent_vectors[key]) == len(target_vector), f"L{length} independent {key} length")
        check(max(abs(left - right) for left, right in zip(independent_vectors[key], target_vector)) < 4e-11, f"L{length} independent {key} values")
    check(max(row["target_reproduction"].values()) < 4e-11, f"L{length} saved target reproduction bounds")
    check(row["independent_controls"]["full_differential_residual_l1"] < 4e-11, f"L{length} independent differential ledger")
    check(row["independent_controls"]["q_coarse_fine_linf"] < 4e-10, f"L{length} independent q refinement")
    check(row["independent_controls"]["J_coarse_fine_linf"] < 2e-10, f"L{length} independent J refinement")
    check(abs(row["summary"]["delta_q_terminal_sum"] - 0.5) < 1e-10, f"L{length} independent source retention")

    covered = []
    for target_shell, independent_shell in zip(target["radial_edge_profile"], row["radial_edge_profile"]):
        check(target_shell["r"] == independent_shell["r"]
              and target_shell["kind"] == independent_shell["kind"]
              and target_shell["edge_indices"] == independent_shell["edge_indices"], f"L{length} shell identity r{target_shell['r']} {target_shell['kind']}")
        indices = target_shell["edge_indices"]
        covered.extend(indices)
        values = [dj[index] for index in indices]
        check(abs(sum(values) - target_shell["signed_sum_delta_J"]) < 2e-15, f"L{length} shell signed sum r{target_shell['r']} {target_shell['kind']}")
        check(abs(sum(abs(value) for value in values) - target_shell["l1_sum_abs_delta_J"]) < 2e-15, f"L{length} shell L1 r{target_shell['r']} {target_shell['kind']}")
        check(max(abs(independent_shell[key] - target_shell[key]) for key in ("signed_sum_delta_J", "l1_sum_abs_delta_J", "mean_abs_delta_J", "max_abs_delta_J")) < 4e-11, f"L{length} independent shell numerics r{target_shell['r']} {target_shell['kind']}")
    check(sorted(covered) == list(range(3 * length)), f"L{length} shell partition complete")

    response = target["response_summary"]
    connector_indices = [index for index, edge in enumerate(edge_records) if edge["kind"] == "connector"]
    check(abs(sum(abs(value) for value in dj) - response["delta_J_l1"]) < 2e-15, f"L{length} delta J L1")
    check(abs(max(abs(value) for value in dj) - response["delta_J_linf"]) < 2e-15, f"L{length} delta J Linf")
    check(abs((sum(abs(value) for value in j1) - sum(abs(value) for value in j0)) - response["total_absolute_throughput_change"]) < 2e-15, f"L{length} total throughput change")
    check(abs((sum(abs(j1[index]) for index in connector_indices) - sum(abs(j0[index]) for index in connector_indices)) - response["connector_absolute_throughput_change"]) < 2e-15, f"L{length} connector throughput change")
    check(target["residual_status"].endswith("NOT_CALLED_DEFECTS"), f"L{length} raw residual classification")
    check(target["profile_status"].endswith("NOT_PHYSICAL_RADIUS_OR_GRID"), f"L{length} finite distance classification")
    check(target["not_claimed"] == DIRECT_NOT_CLAIMED, f"L{length} direct claim ceiling")

    by_radius = defaultdict(float)
    by_radius_kind = {}
    for shell in target["radial_edge_profile"]:
        by_radius[shell["r"]] += shell["l1_sum_abs_delta_J"]
        by_radius_kind[f"r{shell['r']}__{shell['kind']}"] = shell["l1_sum_abs_delta_J"]
    recompiled_rows.append({
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
    farthest = max(by_radius)
    check(by_radius[2] > by_radius[farthest], f"L{length} radius-two exceeds farthest shell")

recompiled = {
    "schema": "R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001",
    "classification": "DIRECT_FULL_SPACE_FINITE_RESPONSE_ROWS__LOWER_SIZE_MARKED_SOURCE_ENGINE_REFERENCE",
    "input_sha256": {"RESULT_L6.json": PINS[DIRECT[6]], "RESULT_L8.json": PINS[DIRECT[8]]},
    "source": "AUTHENTICATED_W_R_EQUALS_ONE_HALF_ON_BASELINE_BLANK_EVEN_SITE_ZERO",
    "rows": recompiled_rows,
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
check(recompiled == target_compiled, "exact target compilation")
check(canonical_digest(recompiled) == independent["compiled_result"]["canonical_json_sha256"], "compiled canonical digest")
check(independent["compiled_result"]["exactly_reconstructed"], "saved compilation disposition")

run = independent["run_observation_custody"]
run_doc = (TARGET / "RUN_OBSERVATION.md").read_text()
check(run["document_sha256"] == PINS[TARGET / "RUN_OBSERVATION.md"], "run observation pin")
check(run["document_contains_all_declared_values"], "run values documented")
check(run["classification"] == "PINNED_SINGLE_ENVIRONMENT_OBSERVATIONS__NOT_COMPLEXITY_LAWS", "run observation ceiling")
check(run["environment_matches_current_host"] and platform.system() == "Darwin" and platform.machine() == "arm64" and sys.version_info[:3] == (3, 9, 6), "declared environment match")
check(run["python_3_9_int_bit_count_absent"] and not hasattr(int, "bit_count"), "Python 3.9 compatibility cause")
check(not run["failed_attempt_independently_replayable"] and "NO_FAILED_VALUE_PROMOTED" in run["failed_attempt_status"], "failed attempt custody boundary")
check("failed closed before result emission" in run_doc and "No value from that failed" in run_doc, "failed attempt target wording")

check(independent["profile_conclusion"] == summary["profile_conclusion"] == "LOWER_SIZE_NONUNIFORM_OSCILLATORY_SPREADING_ONLY__FULL_LADDER_CLASSIFICATION_OPEN", "bounded profile conclusion")
check(independent["residual_status"] == summary["residual_status"] and independent["residual_status"].endswith("NOT_CALLED_DEFECTS"), "audit residual ceiling")
check(independent["Gate_A_P"] == summary["Gate_A_P"] == "OPEN", "Gate A-P open")
check(independent["not_claimed"] == summary["not_claimed"] == AUDIT_NOT_CLAIMED, "audit structured claim ceiling")
check(summary["target_disposition"] == "ELIGIBLE_AS_DIRECT_LOWER_SIZE_REFERENCE_FOR_MARKED_SOURCE_VALIDATION", "lower-size reference disposition")

report = (HERE / "REPORT.md").read_text()
readme = (HERE / "README.md").read_text()
result_md = (HERE / "RESULT.md").read_text()
check("PASS at direct finite L6/L8 response scope" in report and "No target correction" in report, "report verdict")
check("raw and unassigned" in report and "not defects" in readme, "report remainder ceiling")
check("nonuniform" in report and "oscillatory" in report and "lower-size" in report, "report finite profile conclusion")
check("not physical distance" in report and "not a physical boundary reflection" in report, "report support-distance ceiling")
check(all(term in report for term in ("locality", "scaling", "continuum", "Ward", "phase", "graviton", "gravity")), "report physical claim ceiling")
check("not complexity laws" in report and "document-custodied" in report, "report run custody ceiling")
check("30/30" in result_md and "24/24" in result_md and "16/16" in result_md, "result check custody")

failures = [label for passed, label in checks if not passed]
if failures:
    raise AssertionError(failures)
print(f"PASS__LOCALIZED_WRITE_RESPONSE_L6_L8_HOSTILE_AUDIT__{len(checks)}/{len(checks)}")
