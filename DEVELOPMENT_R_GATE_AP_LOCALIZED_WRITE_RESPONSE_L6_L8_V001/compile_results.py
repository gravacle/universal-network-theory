#!/usr/bin/env python3
"""Compile the direct L6/L8 localized-write response records."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "RESULT.json"
INPUTS = {
    6: (HERE / "RESULT_L6.json", "8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a"),
    8: (HERE / "RESULT_L8.json", "b73ba9e1c660a5285a075fd8c040c6b04621e4badc0dbecf42483d5c0a1c72fb"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = {length: json.loads(path.read_text()) for length, (path, _) in INPUTS.items()}
hashes = {f"RESULT_L{length}.json": digest(path) for length, (path, _) in INPUTS.items()}
expected_hashes = {f"RESULT_L{length}.json": expected for length, (_, expected) in INPUTS.items()}
rows = []
for length in sorted(records):
    result = records[length]
    by_radius = defaultdict(float)
    by_radius_kind = {}
    for shell in result["radial_edge_profile"]:
        by_radius[shell["r"]] += shell["l1_sum_abs_delta_J"]
        by_radius_kind[f"r{shell['r']}__{shell['kind']}"] = shell["l1_sum_abs_delta_J"]
    rows.append({
        "L": length,
        "delta_q_terminal_sum": result["response_summary"]["delta_q_terminal_sum"],
        "delta_J_l1": result["response_summary"]["delta_J_l1"],
        "delta_J_linf": result["response_summary"]["delta_J_linf"],
        "total_absolute_throughput_change": result["response_summary"]["total_absolute_throughput_change"],
        "connector_absolute_throughput_change": result["response_summary"]["connector_absolute_throughput_change"],
        "mean_edge_radius_abs_delta_J": result["response_summary"]["mean_edge_radius_abs_delta_J"],
        "effective_responding_edge_count": result["response_summary"]["effective_responding_edge_count"],
        "edge_profile_l1_by_radius": {str(radius): by_radius[radius] for radius in sorted(by_radius)},
        "edge_profile_l1_by_radius_and_kind": by_radius_kind,
        "full_differential_residual_l1": result["numerical_controls"]["full_differential_residual_l1"],
        "full_differential_residual_linf": result["numerical_controls"]["full_differential_residual_linf"],
    })

checks = [
    (hashes == expected_hashes, "direct result hashes"),
    ([row["L"] for row in rows] == [6, 8], "row order"),
    (all(records[length]["checks_passed"] == records[length]["checks_total"] == 24 for length in records), "direct check counts"),
    (all(records[length]["parameters"]["W_R"] == 0.5 for length in records), "source normalization"),
    (all(len(records[length]["edge_records"]) == 3 * length for length in records), "complete edge records"),
    (all(len(records[length]["site_records"]) == 2 * length for length in records), "complete site records"),
    (all(abs(row["delta_q_terminal_sum"] - 0.5) < 1e-10 for row in rows), "retained source amount"),
    (all(row["delta_J_l1"] > 0.0 and row["delta_J_linf"] > 0.0 for row in rows), "nonzero current response"),
    (all(all(abs(edge["delta_J"]) > 1e-10 for edge in records[length]["edge_records"]) for length in records), "all finite edges respond"),
    (all(row["full_differential_residual_l1"] < 2e-11 for row in rows), "differential ledger controls"),
    (all(records[length]["numerical_controls"]["baseline_current_reproduction_linf"] < 2e-11 for length in records), "baseline current reproduction"),
    (all(records[length]["numerical_controls"]["baseline_q_reproduction_linf"] < 2e-11 for length in records), "baseline occupation reproduction"),
    (all(records[length]["residual_status"].endswith("NOT_CALLED_DEFECTS") for length in records), "residual classification"),
    (all(records[length]["profile_status"].endswith("NOT_PHYSICAL_RADIUS_OR_GRID") for length in records), "distance classification"),
    (all(abs(sum(row["edge_profile_l1_by_radius"].values()) - row["delta_J_l1"]) < 1e-12 for row in rows), "radial L1 completeness"),
    (all(row["edge_profile_l1_by_radius"]["2"] > row["edge_profile_l1_by_radius"][str(max(map(int, row["edge_profile_l1_by_radius"]))) ] for row in rows), "radius-two response exceeds far-edge shell"),
]
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8_V001",
    "classification": "DIRECT_FULL_SPACE_FINITE_RESPONSE_ROWS__LOWER_SIZE_MARKED_SOURCE_ENGINE_REFERENCE",
    "input_sha256": hashes,
    "source": "AUTHENTICATED_W_R_EQUALS_ONE_HALF_ON_BASELINE_BLANK_EVEN_SITE_ZERO",
    "rows": rows,
    "finite_profile_description": "NONUNIFORM_OSCILLATORY_SPREADING_ACROSS_ALL_EDGE_SHELLS__RADIUS_TWO_L1_EXCEEDS_FARTHEST_EDGE_SHELL_AT_L6_AND_L8__NO_PHYSICAL_BOUNDARY_CLASSIFICATION",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_DIFFERENTIAL_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "claim_classes": {
        "proved": "AUTHENTICATED_SOURCE_WRITE_LEDGER__FINITE_OWNER_INCIDENCE_AND_PROFILE_PARTITIONS",
        "conditional": "SUPPORT__KAPPA__CONTENT__ROUTING__READ",
        "empirical": "DIRECT_REFINED_L6_AND_L8_DIFFERENTIAL_OCCUPATION_CURRENT_AND_RADIAL_PROFILES",
        "open": "INDEPENDENT_HOSTILE_AUDIT__L10_L12_L14_RESPONSE__FULL_LADDER_PROFILE_CLASSIFICATION__PHYSICAL_DISTANCE__GATE_A_P",
    },
    "not_claimed": "LOCALITY_OR_SCALING_LAW__UNIFORM_OR_ASYMPTOTIC_PROFILE__PHYSICAL_BOUNDARY_REFLECTION__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
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
print(f"PASS__R_GATE_AP_LOCALIZED_WRITE_RESPONSE_L6_L8__{len(checks)}/{len(checks)}")
