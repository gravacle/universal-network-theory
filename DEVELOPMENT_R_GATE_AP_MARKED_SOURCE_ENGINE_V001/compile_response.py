#!/usr/bin/env python3
"""Compile the available marked-source response ladder and L14 guard."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "RESULT.json"
INPUTS = {
    6: (HERE / "RESULT_L6.json", "2a0d2c957b39b960f8d87b55914efd4a547510e3f2cfc01a2a135a1efb2a967b"),
    8: (HERE / "RESULT_L8.json", "288b007e4a519b1b26e062894c7c42685bf200d924b053c196cefda6014cbcdf"),
    10: (HERE / "RESULT_L10.json", "cdf5dae0b6762ca60e8deefb07ac9f05abf06c7d693cd79415db03e154d6f116"),
    12: (HERE / "RESULT_L12.json", "c7fd23bd73c96df1ca234952cba5d5c3eef5652b1de6f7ea3a0e262ef99c6b8f"),
}
SCREEN_L14 = HERE / "SCREEN_L14.json"
SCREEN_L14_HASH = "384c83d26a1a31ac655771d94ee60facfecbb2ec50fd1a9fb08d6a9d6da392b7"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = {length: json.loads(path.read_text()) for length, (path, _) in INPUTS.items()}
screen_l14 = json.loads(SCREEN_L14.read_text())
hashes = {path.name: digest(path) for path, _ in INPUTS.values()}
hashes[SCREEN_L14.name] = digest(SCREEN_L14)
expected_hashes = {path.name: expected for path, expected in INPUTS.values()}
expected_hashes[SCREEN_L14.name] = SCREEN_L14_HASH

rows = []
for length in sorted(records):
    result = records[length]
    by_radius_l1 = defaultdict(float)
    by_radius_signed = defaultdict(float)
    by_radius_max = defaultdict(float)
    by_radius_kind = {}
    for shell in result["radial_edge_profile"]:
        radius = shell["r"]
        by_radius_l1[radius] += shell["l1_sum_abs_delta_J"]
        by_radius_signed[radius] += shell["signed_sum_delta_J"]
        by_radius_max[radius] = max(by_radius_max[radius], shell["max_abs_delta_J"])
        by_radius_kind[f"r{radius}__{shell['kind']}"] = {
            "edge_count": shell["edge_count"],
            "signed_sum_delta_J": shell["signed_sum_delta_J"],
            "l1_sum_abs_delta_J": shell["l1_sum_abs_delta_J"],
            "mean_abs_delta_J": shell["mean_abs_delta_J"],
            "max_abs_delta_J": shell["max_abs_delta_J"],
        }
    radii = sorted(by_radius_l1)
    summary = result["response_summary"]
    controls = result["numerical_controls"]
    far_radius = radii[-1]
    rows.append({
        "L": length,
        "delta_q_terminal_sum": summary["delta_q_terminal_sum"],
        "delta_J_l1": summary["delta_J_l1"],
        "delta_J_linf": summary["delta_J_linf"],
        "total_absolute_throughput_change": summary["total_absolute_throughput_change"],
        "connector_absolute_throughput_change": summary["connector_absolute_throughput_change"],
        "mean_edge_radius_abs_delta_J": summary["mean_edge_radius_abs_delta_J"],
        "effective_responding_edge_count": summary["effective_responding_edge_count"],
        "edge_profile_l1_by_radius": {str(radius): by_radius_l1[radius] for radius in radii},
        "edge_profile_signed_by_radius": {str(radius): by_radius_signed[radius] for radius in radii},
        "edge_profile_max_by_radius": {str(radius): by_radius_max[radius] for radius in radii},
        "edge_profile_by_radius_and_kind": by_radius_kind,
        "farthest_edge_radius": far_radius,
        "farthest_shell_l1": by_radius_l1[far_radius],
        "farthest_shell_fraction_of_delta_J_l1": by_radius_l1[far_radius] / summary["delta_J_l1"],
        "full_differential_residual_l1": controls["full_differential_residual_l1"],
        "full_differential_residual_linf": controls["full_differential_residual_linf"],
        "baseline_q_reproduction_linf": controls["baseline_q_reproduction_linf"],
        "baseline_current_reproduction_linf": controls["baseline_current_reproduction_linf"],
        "current_refinement_linf": controls["current_refinement_linf"],
    })

far_shells = [row["farthest_shell_l1"] for row in rows]
checks = [
    (hashes == expected_hashes, "canonical input hashes"),
    ([row["L"] for row in rows] == [6, 8, 10, 12], "available row order"),
    ([records[length]["checks_total"] for length in sorted(records)] == [35, 35, 29, 29], "target check totals"),
    (all(records[length]["checks_passed"] == records[length]["checks_total"] for length in records), "target checks pass"),
    (screen_l14["checks_passed"] == screen_l14["checks_total"] == 5, "L14 screen structural checks"),
    (screen_l14["decision"] == "NOT_ELIGIBLE_UNDER_CURRENT_UNAGGREGATED_REPRESENTATION", "L14 current representation rejected"),
    (not screen_l14["resource_upper_bound"]["passes_upper_bound_guard"], "L14 guard fails closed"),
    (screen_l14["resource_upper_bound"]["raw_numeric_payload_upper_gib"] > 40.0, "L14 conservative upper exceeds guard"),
    (all(abs(row["delta_q_terminal_sum"] - 0.5) < 2e-8 for row in rows), "half-record retained"),
    (all(row["full_differential_residual_l1"] < 3e-8 for row in rows), "differential ledger controls"),
    (all(row["baseline_q_reproduction_linf"] < 4e-8 for row in rows), "baseline occupation reproduction"),
    (all(row["baseline_current_reproduction_linf"] < 4e-8 for row in rows), "baseline current reproduction"),
    (all(row["current_refinement_linf"] < 4e-8 for row in rows), "current refinement"),
    (all(abs(sum(row["edge_profile_l1_by_radius"].values()) - row["delta_J_l1"]) < 2e-12 for row in rows), "radial L1 completeness"),
    (all(row["edge_profile_l1_by_radius"]["2"] == max(row["edge_profile_l1_by_radius"].values()) for row in rows), "radius-two aggregate L1 maximum"),
    (all(row["farthest_shell_l1"] < row["edge_profile_l1_by_radius"]["0"] for row in rows), "far shell below source shell"),
    (all(far_shells[index + 1] < far_shells[index] for index in range(len(far_shells) - 1)), "farthest-shell L1 decreases across available ladder"),
    (rows[-1]["farthest_shell_fraction_of_delta_J_l1"] < 3e-4, "L12 far-shell fraction small"),
    (abs(rows[-1]["mean_edge_radius_abs_delta_J"] - rows[-2]["mean_edge_radius_abs_delta_J"]) < 0.006, "L10/L12 mean graph-radius proximity"),
    (abs(rows[-1]["delta_J_l1"] - rows[-2]["delta_J_l1"]) < 0.004, "L10/L12 total differential-current proximity"),
    (all(all(abs(edge["delta_J"]) > 1e-10 for edge in records[length]["edge_records"]) for length in records), "all available finite edges respond"),
    (all(records[length]["residual_status"].endswith("NOT_CALLED_DEFECTS") for length in records), "raw remainder classification"),
    (all(records[length]["profile_status"].endswith("NOT_PHYSICAL_RADIUS_OR_GRID") for length in records), "graph-distance classification"),
]
failures = [label for passed, label in checks if not passed]

out = {
    "schema": "R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD_V001",
    "classification": "FINITE_AUTHENTICATED_WRITE_RESPONSE__AVAILABLE_L6_L8_L10_L12_ROWS__L14_CURRENT_REPRESENTATION_REJECTED_PREALLOCATION",
    "source": "AUTHENTICATED_W_R_EQUALS_ONE_HALF_ON_BASELINE_BLANK_EVEN_SITE_ZERO",
    "input_sha256": hashes,
    "rows": rows,
    "L14_status": {
        "requested_L": 14,
        "marked_source_orbit_dimension": screen_l14["orbit_dimension"],
        "current_representation_upper_gib": screen_l14["resource_upper_bound"]["raw_numeric_payload_upper_gib"],
        "guard_gib": screen_l14["resource_upper_bound"]["guard_gib"],
        "decision": screen_l14["decision"],
        "response_row": None,
        "interpretation": "NO_L14_RESPONSE_VALUE__NO_EXTRAPOLATION__A_DIFFERENT_VALIDATED_REPRESENTATION_WOULD_BE_REQUIRED",
    },
    "finite_profile_description": "AVAILABLE_L6_TO_L12_ROWS_SHOW_NONUNIFORM_GRAPH_LOCAL_CONCENTRATION_WITH_OSCILLATORY_SIGNED_EDGES__RADIUS_TWO_AGGREGATE_L1_MAXIMUM__FARTHEST_SHELL_CONTRIBUTION_DECREASES_WITH_L__NO_FAR_SHELL_ENHANCEMENT_OBSERVED__L14_ROW_UNAVAILABLE",
    "classification_detail": {
        "spatial_localization": "EMPIRICALLY_CONSISTENT_ON_AVAILABLE_FINITE_GRAPH_ROWS__INNER_PROFILE_STABILIZES_WHILE_FARTHEST_SHELL_FRACTION_FALLS_TO_2_52E_4_AT_L12__NOT_A_LOCALITY_LAW",
        "uniform_spreading": "NOT_OBSERVED__SHELL_AND_EDGE_MAGNITUDES_ARE_STRONGLY_NONUNIFORM",
        "boundary_dependent_reflection": "NO_FAR_SHELL_ENHANCEMENT_OBSERVED_ON_AVAILABLE_ROWS__PHYSICAL_BOUNDARY_REFLECTION_UNDEFINED_WITHOUT_GEOMETRY_MAP",
        "periodic_return": "FINITE_GRAPH_PERIODIC_RETURN_CONTAMINATION_IS_LARGEST_AT_SMALLER_L_AND_DECREASES_AT_THE_FARTHEST_SHELL__DESCRIPTIVE_ONLY",
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_DIFFERENTIAL_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "claim_classes": {
        "proved": "AUTHENTICATED_SOURCE_WRITE_LEDGER__EXACT_OWNER_INCIDENCE_TELESCOPING__FINITE_RADIAL_PARTITIONS__MARKED_SOURCE_STABILIZER_AND_RESOURCE_ARITHMETIC",
        "adopted": "F3_MDC_ALPHA_EQUALS_R0__CANONICAL_LOCAL_SOURCE_LABEL",
        "conditional": "CONNECTED_SUPPORT__KAPPA__CONTENT__ROUTING__READ__MARKED_SOURCE_NUMERICAL_REPRESENTATION",
        "empirical": "REFINED_FINITE_L6_L8_L10_L12_RESPONSE_ROWS_AND_AVAILABLE_WINDOW_PROFILE_DESCRIPTION",
        "open": "INDEPENDENT_HOSTILE_AUDIT__L14_RESPONSE_UNDER_A_DIFFERENT_REPRESENTATION__PHYSICAL_DISTANCE_AND_BOUNDARY__LOCALITY_OR_SCALING_LAW__GATE_A_P",
    },
    "not_claimed": "COMPLETE_L6_TO_L14_NUMERICAL_LADDER__L14_RESPONSE__LOCALITY_OR_SCALING_THEOREM__PHYSICAL_BOUNDARY_REFLECTION__UNIFORM_OR_ASYMPTOTIC_PROFILE__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
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
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5e-12:
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
print(f"PASS__R_GATE_AP_MARKED_SOURCE_RESPONSE_L6_L12_WITH_L14_GUARD__{len(checks)}/{len(checks)}")
