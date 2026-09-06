#!/usr/bin/env python3
"""Independent append reconstruction for the sealed connected L4--L14 trajectory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "INDEPENDENT_RESULT.json"
BASE = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L12_V001" / "RESULT.json"
L14 = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001" / "RESULT.json"
L14_AUDIT = ROOT / "AUDIT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001"
TARGET = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001"

PINS = {
    BASE: "8fe9697c833542812bbda78ea5528265b048d1775ace43a7203e1c583c7b5759",
    L14: "e8134d5311b9bdfd62ce7df5988da803b110516606ce905a1bc49bd65cdb5fbe",
    L14_AUDIT / "RESULT.json": "cf4301e55f0c911196ecfbd2f02d60ebcfc32def3353472dccb87077ca77d204",
    L14_AUDIT / "INDEPENDENT_RESULT.json": "bfa8fd0eb4ff793662af546408882b84ba55ec0ff38145263d8c9747660919be",
    L14_AUDIT / "verify_audit.py": "9786f8ad17f4d1d851f0b9afec17d675d8e84a9a5d5e6f7a074fb820b9a9bfc2",
    TARGET / "README.md": "c0ab043df521d60bbcc4e4bc643ed0234e1a194528a1cb6544703061d8acfc61",
    TARGET / "RESULT.json": "8a69f780a372ae436ef2fe458af80f7fa1ba70d8c93b21d91524c6e9819d753d",
    TARGET / "THEOREM.md": "8d95a25f5c1cefc45a8825b06686fddac68295708753b481eadd5a6abddfd34f",
    TARGET / "compile_trajectory.py": "a9dde10bf870a9b85d9db3bfea4ae5c42d276416d228f93d1306956ac08b0e46",
}

NOT_CLAIMED = (
    "MONOTONICITY__TREND__CONVERGENCE__LIMIT__EXPONENT__FIT__SCALING_LAW__"
    "AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY"
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


if any(digest(path) != expected for path, expected in PINS.items()):
    raise AssertionError("sealed input or target custody mismatch")

base = json.loads(BASE.read_text())
l14 = json.loads(L14.read_text())
l14_audit_summary = json.loads((L14_AUDIT / "RESULT.json").read_text())
l14_audit_detail = json.loads((L14_AUDIT / "INDEPENDENT_RESULT.json").read_text())
target = json.loads((TARGET / "RESULT.json").read_text())

length = 14
census = l14["census"]
currents = l14["integrated_oriented_currents"]
occupations = l14["q_after"]
retained = l14["expected_retained_global"]
total = l14["absolute_oriented_throughput_global"]
connector = l14["absolute_connector_throughput_global"]

row = {
    "L": length,
    "input_sha256": PINS[L14],
    "hostile_audit_sha256": PINS[L14_AUDIT / "RESULT.json"],
    "sites": census["sites_global"],
    "sites_per_F3_layer": census["sites_per_F3_layer"],
    "possible_F3_links": census["possible_F3_links"],
    "connected_components": census["components"],
    "sites_per_component": census["sites_per_component"],
    "selected_edges_owner_once": census["selected_edges_global_owner_once"],
    "prepared_source_lineages": census["prepared_source_lineages"],
    "expected_retained_total": retained,
    "expected_retained_per_lineage": retained / census["prepared_source_lineages"],
    "active_internal_edges_per_component": l14["active_internal_supports_per_component"],
    "active_connector_edges_per_component": l14["active_connector_supports_per_component"],
    "internal_current_magnitude": max(abs(value) for value in currents[: 2 * length]),
    "connector_current_magnitude": max(abs(value) for value in currents[2 * length :]),
    "q_after_even_mean": sum(occupations[0::2]) / length,
    "q_after_odd_mean": sum(occupations[1::2]) / length,
    "absolute_oriented_throughput_global": total,
    "absolute_oriented_throughput_per_retained": total / retained,
    "absolute_connector_throughput_global": connector,
    "absolute_connector_throughput_per_retained": connector / retained,
    "connector_share_of_absolute_throughput": connector / total,
    "max_abs_connected_edge_correlation": l14["max_abs_connected_edge_correlation"],
    "record_ledger_residual_l1_per_component": l14["record_ledger_residual_l1_per_component"],
    "record_ledger_residual_linf_per_component": l14["record_ledger_residual_linf_per_component"],
    "record_ledger_residual_l1_global_bound": l14["record_ledger_residual_l1_global_bound"],
}

previous = base["rows"][-1]
adjacent = {
    "from_L": previous["L"],
    "to_L": length,
    "site_ratio": row["sites"] / previous["sites"],
    "retained_ratio": row["expected_retained_total"] / previous["expected_retained_total"],
    "total_throughput_ratio": row["absolute_oriented_throughput_global"]
    / previous["absolute_oriented_throughput_global"],
    "throughput_per_retained_ratio": row["absolute_oriented_throughput_per_retained"]
    / previous["absolute_oriented_throughput_per_retained"],
    "connector_throughput_ratio": row["absolute_connector_throughput_global"]
    / previous["absolute_connector_throughput_global"],
    "connector_throughput_per_retained_ratio": row["absolute_connector_throughput_per_retained"]
    / previous["absolute_connector_throughput_per_retained"],
}

reconstructed = {
    "schema": "R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001",
    "classification": "HOSTILE_AUDITED_INPUT_APPEND__FINITE_RAW_RECORD_TRAJECTORY",
    "scope": "CONDITIONAL_CONNECTED_SUPPORT_AT_KAPPA_PI_OVER_TWO__NO_FIT_OR_EXTRAPOLATION",
    "base_trajectory_sha256": PINS[BASE],
    "rows": base["rows"] + [row],
    "adjacent_comparators": base["adjacent_comparators"] + [adjacent],
    "checks_passed": 18,
    "checks_total": 18,
    "failures": [],
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_RECORD_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "not_claimed": NOT_CLAIMED,
}

readme = (TARGET / "README.md").read_text()
theorem = (TARGET / "THEOREM.md").read_text()
compiler = (TARGET / "compile_trajectory.py").read_text()
checks = [
    (base["checks_passed"] == base["checks_total"] == 16, "sealed base 16/16"),
    ([item["L"] for item in base["rows"]] == [4, 6, 8, 10, 12], "base row order"),
    ([(item["from_L"], item["to_L"]) for item in base["adjacent_comparators"]]
     == [(4, 6), (6, 8), (8, 10), (10, 12)], "base comparator order"),
    (target["rows"][:5] == base["rows"], "prior rows exactly preserved"),
    (target["adjacent_comparators"][:4] == base["adjacent_comparators"], "prior comparators exactly preserved"),
    (canonical_digest(target["rows"][:5]) == canonical_digest(base["rows"]), "prior row canonical bytes"),
    (canonical_digest(target["adjacent_comparators"][:4])
     == canonical_digest(base["adjacent_comparators"]), "prior comparator canonical bytes"),
    (row == target["rows"][-1], "independent L14 row"),
    (adjacent == target["adjacent_comparators"][-1], "independent L12-to-L14 comparator"),
    (reconstructed == target, "complete target result reconstruction"),
    (census["sites_global"] == 2744 and census["components"] == 98, "L14 site/component census"),
    (census["prepared_source_lineages"] == 1372 and census["selected_edges_global_owner_once"] == 4116, "L14 lineage/edge census"),
    (len(currents) == 42 and all(abs(value) > 1e-10 for value in currents), "L14 active current census"),
    (abs(row["expected_retained_per_lineage"] - 0.5) < 1e-12, "L14 retained per lineage"),
    (abs(98 * sum(abs(value) for value in currents) - total) < 2e-12, "L14 total throughput"),
    (abs(98 * sum(abs(value) for value in currents[28:]) - connector) < 2e-12, "L14 connector throughput"),
    (row["record_ledger_residual_l1_per_component"] > 0 and row["record_ledger_residual_linf_per_component"] > 0, "raw residual values retained"),
    (l14["residual_status"].endswith("NOT_CALLED_DEFECTS"), "L14 residual classification"),
    (l14_audit_summary["verdict"] == "PASS__INDEPENDENT_L14_NUMERICAL_RECONSTRUCTION", "L14 hostile summary PASS"),
    (l14_audit_summary["independent_checks"] == "29/29", "L14 hostile summary 29/29"),
    (l14_audit_detail["checks_passed"] == l14_audit_detail["checks_total"] == 29, "L14 hostile detail 29/29"),
    (l14_audit_detail["target_reproduction"]["current_linf"] < 6e-9, "L14 all-current hostile reproduction"),
    (l14_audit_detail["target_reproduction"]["all_comparator_linf"] < 6e-8, "L14 comparator hostile reproduction"),
    (target["checks_passed"] == target["checks_total"] == 18, "target trajectory 18/18"),
    (target["not_claimed"] == NOT_CLAIMED, "structured claim ceiling"),
    ("exactly as parsed data" in readme and "byte-for-byte as parsed data" not in readme, "README parsed-data custody wording"),
    ("not defects" in readme and "No monotonicity" in readme, "README residual and finite-comparison ceiling"),
    ("not a fit" in theorem and "not renamed defects" in theorem, "THEOREM residual and finite-comparison ceiling"),
    ("physical grid" in theorem and "graviton" in theorem and "gravity" in theorem, "THEOREM physical claim ceiling"),
    (NOT_CLAIMED in compiler, "compiler structured claim ceiling"),
    (PINS[BASE] in compiler and PINS[L14] in compiler and PINS[L14_AUDIT / "RESULT.json"] in compiler, "compiler input pins"),
]
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "AUDIT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001",
    "verdict": "PASS__INDEPENDENT_APPEND_RECONSTRUCTION" if not failures else "FAIL_CLOSED",
    "method": "SEALED_JSON_INPUTS__INDEPENDENT_ROW_AND_ADJACENT_ARITHMETIC__EXACT_PREFIX_COMPARISON",
    "input_sha256": {path.relative_to(ROOT).as_posix(): expected for path, expected in PINS.items()},
    "base_prefix": {
        "row_count": len(base["rows"]),
        "adjacent_comparator_count": len(base["adjacent_comparators"]),
        "rows_canonical_json_sha256": canonical_digest(base["rows"]),
        "adjacent_comparators_canonical_json_sha256": canonical_digest(base["adjacent_comparators"]),
        "exactly_preserved": True,
    },
    "appended_l14_row": row,
    "appended_L12_to_L14_comparator": adjacent,
    "complete_target_result_canonical_json_sha256": canonical_digest(reconstructed),
    "target_result_exactly_reconstructed": reconstructed == target,
    "l14_hostile_basis": {
        "verdict": l14_audit_summary["verdict"],
        "independent_checks": l14_audit_summary["independent_checks"],
        "packet_verifier": "56/56__SEPARATELY_REPLAYED",
        "target_reproduction": l14_audit_detail["target_reproduction"],
    },
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_RECORD_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "claim_ceiling": "FINITE_RAW_RECORD_APPEND_ONLY",
    "not_claimed": NOT_CLAIMED,
}

if OUT.exists():
    if out != json.loads(OUT.read_text()):
        raise AssertionError("saved independent result differs")
else:
    print("INDEPENDENT_RESULT_BEGIN")
    print(json.dumps(out, indent=2, sort_keys=True))
    print("INDEPENDENT_RESULT_END")
if failures:
    raise AssertionError(failures)
print(f"PASS__HOSTILE_CONNECTED_TRAJECTORY_L4_L14__{len(checks)}/{len(checks)}")
