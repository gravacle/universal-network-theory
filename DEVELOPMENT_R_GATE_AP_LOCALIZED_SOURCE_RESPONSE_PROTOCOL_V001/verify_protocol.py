#!/usr/bin/env python3
"""Verify the finite W_R=1/2 localized-write response protocol and custody."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
SIZES = (6, 8, 10, 12, 14)
SOURCE_SITE = 0
TRAJECTORY = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001" / "RESULT.json"
TRAJECTORY_AUDIT = ROOT / "AUDIT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001" / "RESULT.json"
SOURCE_THEOREM = ROOT / "DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "THEOREM.md"
SOURCE_AUDIT = ROOT / "AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001" / "INDEPENDENT_RESULT.json"
PARENT_RESULT = ROOT / "DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "RESULT.json"
PARENT_AUDIT = ROOT / "AUDIT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "INDEPENDENT_RESULT.json"
PINNED_HASHES = {
    TRAJECTORY: "8a69f780a372ae436ef2fe458af80f7fa1ba70d8c93b21d91524c6e9819d753d",
    TRAJECTORY_AUDIT: "c42a94533d9d9795370bb0a997e19b21267d3fc78a4e681f2e07bc83ff6d68a5",
    SOURCE_THEOREM: "113ca9798fe60a4afe7bada091d675ebb71608cab30f53b22bbc8ae59d10a06b",
    SOURCE_AUDIT: "560023054d53f171edaf6c20e8f932056a4c9adae09929c443a905e5974aedba",
    PARENT_RESULT: "d5c12520518c54dce228e9aa28b860980685276f84aa52aa065b8c6e1e8d0bb4",
    PARENT_AUDIT: "e19faa594ce1710e251ae0c89d4cedeae4b43216d60105b95979b48f55426bc7",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prism_group(length: int):
    group = []
    for epsilon in (1, -1):
        for shift in range(length):
            swap = shift % 2
            permutation = []
            for layer in range(2):
                for site in range(length):
                    prism_site = (site - layer) % length
                    moved_layer = layer ^ swap
                    moved_prism_site = (epsilon * prism_site + shift) % length
                    moved_site = (moved_prism_site + moved_layer) % length
                    permutation.append(moved_layer * length + moved_site)
            group.append(tuple(permutation))
    return group


def cycle_count(permutation):
    seen = set()
    count = 0
    for start in range(len(permutation)):
        if start in seen:
            continue
        count += 1
        cursor = start
        while cursor not in seen:
            seen.add(cursor)
            cursor = permutation[cursor]
    return count


def edges_for(length: int):
    edges = []
    for layer in range(2):
        for site in range(length):
            edges.append((layer * length + site, layer * length + (site + 1) % length, "internal"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def distances(site_count: int, edges, source: int):
    neighbors = [set() for _ in range(site_count)]
    for u, v, _ in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    distance = [None] * site_count
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if distance[v] is None:
                distance[v] = distance[u] + 1
                queue.append(v)
    return distance


hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in PINNED_HASHES}
expected_hashes = {
    path.relative_to(ROOT).as_posix(): expected for path, expected in PINNED_HASHES.items()
}
trajectory = json.loads(TRAJECTORY.read_text())
trajectory_audit = json.loads(TRAJECTORY_AUDIT.read_text())
source_audit = json.loads(SOURCE_AUDIT.read_text())
parent = json.loads(PARENT_RESULT.read_text())
parent_audit = json.loads(PARENT_AUDIT.read_text())

# Exact authenticated source slice: a blank selected retained site receives
# (|B>-i|x>)/sqrt(2), so Delta Q=W_R=1/2 while all transport edges are off.
blank_q = Fraction(0)
perturbed_q = Fraction(1, 2)
delta_q_write = perturbed_q - blank_q
w_r = Fraction(1, 2)
write_edge_flux = Fraction(0)
write_balance = delta_q_write + write_edge_flux - w_r
perturbed_norm = Fraction(1, 2) + Fraction(1, 2)

rows_by_l = {row["L"]: row for row in trajectory["rows"]}
baselines = []
representations = []
profiles = []
support_checks = []
for length in SIZES:
    row = rows_by_l[length]
    baselines.append({
        "L": length,
        "total_throughput_per_retained": row["absolute_oriented_throughput_per_retained"],
        "connector_throughput_per_retained": row["absolute_connector_throughput_per_retained"],
        "max_abs_connected_edge_correlation": row["max_abs_connected_edge_correlation"],
        "raw_residual_l1_per_component": row["record_ledger_residual_l1_per_component"],
    })
    group = prism_group(length)
    stabilizer = [permutation for permutation in group if permutation[SOURCE_SITE] == SOURCE_SITE]
    burnside_sum = sum(1 << cycle_count(permutation) for permutation in stabilizer)
    representations.append({
        "L": length,
        "full_source_preserving_group_order": len(group),
        "selected_site_stabilizer_order": len(stabilizer),
        "marked_source_burnside_sum": burnside_sum,
        "marked_source_orbit_dimension": burnside_sum // len(stabilizer),
    })
    edges = edges_for(length)
    degrees = Counter(vertex for u, v, _ in edges for vertex in (u, v))
    distance = distances(2 * length, edges, SOURCE_SITE)
    shells = Counter((min(distance[u], distance[v]), kind) for u, v, kind in edges)
    profiles.append({
        "L": length,
        "site_graph_radius": max(distance),
        "edge_shell_rule": "R_E_EQUALS_MIN_DISTANCE_SOURCE_TO_EITHER_ENDPOINT",
        "edge_shell_counts": [
            {"r": radius, "kind": kind, "edges": count}
            for (radius, kind), count in sorted(shells.items())
        ],
    })
    support_checks.append(
        len(group) == 2 * length
        and len(set(group)) == 2 * length
        and {permutation[SOURCE_SITE] for permutation in group} == set(range(0, 2 * length, 2))
        and len(stabilizer) == 2
        and len(edges) == 3 * length
        and all(value == 3 for value in degrees.values())
        and all(value is not None for value in distance)
    )

expected_marked_dimensions = {6: 2176, 8: 33280, 10: 526336, 12: 8396800, 14: 134250496}
checks = [
    (hashes == expected_hashes, "sealed input hashes"),
    (trajectory["checks_passed"] == trajectory["checks_total"] == 18, "sealed trajectory target"),
    (trajectory_audit["target_checks"] == "18/18", "sealed trajectory target audit"),
    (trajectory_audit["independent_checks"] == "31/31", "sealed trajectory reconstruction audit"),
    (trajectory_audit["verdict"].startswith("PASS_AFTER_BOUNDED_LABEL_REPAIR"), "sealed trajectory hostile verdict"),
    (source_audit["disposition"] == "PASS_AT_CONDITIONAL_SINGLE_HISTORY_WITNESS_SCOPE", "authenticated source witness"),
    (source_audit["ledger"]["W_R"] == "1/2" and source_audit["ledger"]["balance"] == "0", "authenticated source ledger"),
    (parent["physical_parent_selection"]["source_status_during_accumulation"] == "OFF", "source-off transport interval"),
    (parent_audit["disposition"] == "PASS_AFTER_REQUIRED_LEDGER_RECLASSIFICATION", "physical-parent hostile disposition"),
    (perturbed_norm == 1, "exact inserted-site state normalization"),
    (delta_q_write == w_r == Fraction(1, 2), "exact source-write amount"),
    (write_balance == 0, "exact terms-off write ledger"),
    ([row["L"] for row in baselines] == list(SIZES), "baseline row order"),
    (all(row["total_throughput_per_retained"] > 0 for row in baselines), "positive baseline total throughputs"),
    (all(row["connector_throughput_per_retained"] > 0 for row in baselines), "positive baseline connector throughputs"),
    (all(support_checks), "finite connected support and localized-site orbit"),
    ([row["selected_site_stabilizer_order"] for row in representations] == [2] * len(SIZES), "localized marker stabilizers"),
    ({row["L"]: row["marked_source_orbit_dimension"] for row in representations} == expected_marked_dimensions, "marked-source orbit dimensions"),
    (all(sum(item["edges"] for item in profile["edge_shell_counts"]) == 3 * profile["L"] for profile in profiles), "radial edge-shell partition"),
    (representations[-1]["marked_source_orbit_dimension"] > 10 * 9608050, "L14 localized representation is separately resource gated"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL_V001",
    "status": "FINITE_PROTOCOL_DEFINED__EXECUTION_REQUIRES_MARKED_SOURCE_ENGINE_VALIDATION_AND_PER_SIZE_RESOURCE_SCREEN",
    "scope": "AUTHENTICATED_W_R_HALF_LOCAL_INSERTION_TO_FINITE_CARRIER_FLOW__L6_L8_L10_L12_L14",
    "sealed_inputs_sha256": hashes,
    "background_reference": {
        "label": "EMPIRICAL_FINITE_WINDOW_REFERENCE_APPROX_0_5213_TOTAL_0_1682_CONNECTOR",
        "evidence_class": "HOSTILE_AUDITED_L4_TO_L14_FINITE_WINDOW__NOT_PROVED_ASYMPTOTE_OR_INVARIANT",
        "response_rows": baselines,
    },
    "localized_source": {
        "selected_component": "CANONICAL_COMPONENT_ZERO__OTHER_DISJOINT_COMPONENTS_CANCEL_IN_DIFFERENCE",
        "selected_site": SOURCE_SITE,
        "baseline_site_state": "B",
        "inserted_site_state": "B_MINUS_I_X_OVER_SQRT2",
        "coordinate_status": "FINITE_SUPPORT_LABEL__NOT_PHYSICAL_GRID_POSITION",
        "raw_source_coefficient": "14441248/6075",
        "pulse": "PHI_EQUALS_PI_OVER_4__EPSILON_EQUALS_PI_OVER_4_R0",
        "write": "W_R_EQUALS_ONE_HALF",
        "write_slice": "ALL_CONNECTED_TRANSPORT_EDGES_OFF__DELTA_Q_PLUS_EDGE_FLUX_MINUS_W_R_EQUALS_HALF_PLUS_ZERO_MINUS_HALF_EQUALS_ZERO",
        "transport_slice": "SOURCE_AND_WRITER_OFF__ORIGINAL_OWNER_ONCE_CONNECTED_SUPPORT_RESTORED",
    },
    "differential_observables": {
        "occupation": "DELTA_Q_I_EQUALS_Q_I_PERTURBED_AFTER_MINUS_Q_I_BASELINE_AFTER",
        "current": "DELTA_J_E_EQUALS_J_E_PERTURBED_MINUS_J_E_BASELINE",
        "full_differential_ledger": "DELTA_Q_AFTER_PLUS_B_DELTA_J_MINUS_W_R_DELTA_SOURCE_SITE_EQUALS_R_NUM_DIFFERENTIAL",
        "global_sum": "SUM_I_DELTA_Q_I_AFTER_EQUALS_W_R_EQUALS_ONE_HALF",
        "total_throughput_change": "SUM_E_ABS_J_E_PERTURBED_MINUS_SUM_E_ABS_J_E_BASELINE",
        "connector_throughput_change": "SUM_CONNECTOR_ABS_J_E_PERTURBED_MINUS_SUM_CONNECTOR_ABS_J_E_BASELINE",
        "radial_edge_rule": "R_E_EQUALS_MIN_GRAPH_DISTANCE_FROM_SOURCE_TO_EDGE_ENDPOINT",
        "radial_fields": "COUNT__SIGNED_SUM_DELTA_J__L1_SUM_ABS_DELTA_J__MEAN_ABS__MAX_ABS__SPLIT_INTERNAL_CONNECTOR",
    },
    "radial_partitions": profiles,
    "marked_source_representation": representations,
    "execution_gates": [
        "REPRODUCE_SEALED_BASELINE_AT_EACH_L_BEFORE_RESPONSE_ACCESS",
        "USE_MARKED_SOURCE_OR_EQUIVALENT_NONINVARIANT_SECTOR__FULL_INVARIANT_BASIS_IS_INVALID_FOR_LOCAL_INSERTION",
        "MATCH_DIRECT_FULL_SPACE_L6_AND_L8_COMPLETE_Q_AND_J_VECTORS_BEFORE_L10_TO_L14",
        "PASS_SEPARATE_MEMORY_SCREEN_AT_EACH_L__DO_NOT_FORCE_L14",
        "RUN_INDEPENDENT_COARSE_FINE_EVOLUTION_AND_CURRENT_QUADRATURE",
        "RETAIN_COMPLETE_SIGNED_EDGE_VECTOR_BESIDE_RADIAL_BINS",
        "CLASSIFY_LOCALIZATION_UNIFORMITY_OR_FINITE_PERIODIC_RETURN_FROM_RAW_PROFILES_WITHOUT_CONTINUUM_FIT",
        "REQUIRE_INDEPENDENT_HOSTILE_AUDIT_BEFORE_PROMOTION",
    ],
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "claim_classes": {
        "proved": "AUTHENTICATED_W_R_HALF_TERMS_OFF_WRITE_LEDGER__FINITE_SUPPORT_AND_RADIAL_PARTITIONS__MARKED_SOURCE_STABILIZER_COUNTS__PROTOCOL_IDENTITIES",
        "adopted": "F3_MDC_ALPHA_EQUALS_R0__CANONICAL_LOCAL_SOURCE_LABEL",
        "conditional": "CONNECTED_SUPPORT__KAPPA__T_AND_TAU__CONTENT__ROUTING__COMPLETE_READ__NUMERICAL_REPRESENTATION",
        "empirical": "SEALED_UNPERTURBED_L4_TO_L14_REFERENCE_ONLY__NO_LOCALIZED_RESPONSE_DATA_YET",
        "open": "MARKED_SOURCE_ENGINE__PER_SIZE_RESOURCE_ELIGIBILITY__ALL_LOCALIZED_RESPONSE_VALUES__PROFILE_CLASSIFICATION__PHYSICAL_DISTANCE_MAP__GLOBAL_RESPONSE_OWNERS__LAWFUL_QUOTIENT__GATE_A_P",
    },
    "not_claimed": "ASYMPTOTIC_OR_INVARIANT_PLATEAU_THEOREM__LOCALIZED_RESPONSE_RESULT__L14_RESPONSE_FEASIBILITY__SCALING_LAW__PHYSICAL_GRID_OR_DISTANCE__CONTINUUM__WARD__CRITICAL_OR_GENERIC_PHASE__GRAVITON__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5.0e-12:
            raise AssertionError(f"canonical float differs at {path}")
    elif observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    compatible(out, json.loads(OUT.read_text()))
else:
    print("RESULT_JSON_BEGIN")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("RESULT_JSON_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL__{len(checks)}/{len(checks)}")
