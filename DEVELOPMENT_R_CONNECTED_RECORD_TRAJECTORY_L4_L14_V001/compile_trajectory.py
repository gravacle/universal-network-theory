#!/usr/bin/env python3
"""Append the hostile-audited connected L14 row to the sealed L4--L12 trajectory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
BASE = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L12_V001" / "RESULT.json"
L14 = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001" / "RESULT.json"
AUDIT = ROOT / "AUDIT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001" / "RESULT.json"
BASE_HASH = "8fe9697c833542812bbda78ea5528265b048d1775ace43a7203e1c583c7b5759"
L14_HASH = "e8134d5311b9bdfd62ce7df5988da803b110516606ce905a1bc49bd65cdb5fbe"
AUDIT_HASH = "cf4301e55f0c911196ecfbd2f02d60ebcfc32def3353472dccb87077ca77d204"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if (digest(BASE), digest(L14), digest(AUDIT)) != (BASE_HASH, L14_HASH, AUDIT_HASH):
    raise AssertionError("sealed input custody mismatch")
base = json.loads(BASE.read_text())
packet = json.loads(L14.read_text())
audit = json.loads(AUDIT.read_text())
if audit["verdict"] != "PASS__INDEPENDENT_L14_NUMERICAL_RECONSTRUCTION":
    raise AssertionError("L14 hostile audit is not PASS")
census = packet["census"]
currents = packet["integrated_oriented_currents"]
q_after = packet["q_after"]
retained = packet["expected_retained_global"]
total = packet["absolute_oriented_throughput_global"]
connector = packet["absolute_connector_throughput_global"]
length = 14
l14_row = {
    "L": length,
    "input_sha256": L14_HASH,
    "hostile_audit_sha256": AUDIT_HASH,
    "sites": census["sites_global"],
    "sites_per_F3_layer": census["sites_per_F3_layer"],
    "possible_F3_links": census["possible_F3_links"],
    "connected_components": census["components"],
    "sites_per_component": census["sites_per_component"],
    "selected_edges_owner_once": census["selected_edges_global_owner_once"],
    "prepared_source_lineages": census["prepared_source_lineages"],
    "expected_retained_total": retained,
    "expected_retained_per_lineage": retained / census["prepared_source_lineages"],
    "active_internal_edges_per_component": packet["active_internal_supports_per_component"],
    "active_connector_edges_per_component": packet["active_connector_supports_per_component"],
    "internal_current_magnitude": max(abs(value) for value in currents[: 2 * length]),
    "connector_current_magnitude": max(abs(value) for value in currents[2 * length :]),
    "q_after_even_mean": sum(q_after[0::2]) / length,
    "q_after_odd_mean": sum(q_after[1::2]) / length,
    "absolute_oriented_throughput_global": total,
    "absolute_oriented_throughput_per_retained": total / retained,
    "absolute_connector_throughput_global": connector,
    "absolute_connector_throughput_per_retained": connector / retained,
    "connector_share_of_absolute_throughput": connector / total,
    "max_abs_connected_edge_correlation": packet["max_abs_connected_edge_correlation"],
    "record_ledger_residual_l1_per_component": packet["record_ledger_residual_l1_per_component"],
    "record_ledger_residual_linf_per_component": packet["record_ledger_residual_linf_per_component"],
    "record_ledger_residual_l1_global_bound": packet["record_ledger_residual_l1_global_bound"],
}

previous = base["rows"][-1]
adjacent = {
    "from_L": previous["L"],
    "to_L": length,
    "site_ratio": l14_row["sites"] / previous["sites"],
    "retained_ratio": l14_row["expected_retained_total"] / previous["expected_retained_total"],
    "total_throughput_ratio": l14_row["absolute_oriented_throughput_global"] / previous["absolute_oriented_throughput_global"],
    "throughput_per_retained_ratio": l14_row["absolute_oriented_throughput_per_retained"] / previous["absolute_oriented_throughput_per_retained"],
    "connector_throughput_ratio": l14_row["absolute_connector_throughput_global"] / previous["absolute_connector_throughput_global"],
    "connector_throughput_per_retained_ratio": l14_row["absolute_connector_throughput_per_retained"] / previous["absolute_connector_throughput_per_retained"],
}
rows = base["rows"] + [l14_row]
adjacent_comparators = base["adjacent_comparators"] + [adjacent]

checks = [
    ([row["L"] for row in rows] == [4, 6, 8, 10, 12, 14], "six-size row order"),
    (base["rows"] == rows[:5], "sealed base rows unchanged"),
    (base["adjacent_comparators"] == adjacent_comparators[:4], "sealed base comparators unchanged"),
    (l14_row["sites"] == length**3, "L14 site census"),
    (l14_row["sites_per_F3_layer"] == length**3 // 2, "L14 F3 layers"),
    (l14_row["possible_F3_links"] == (length**3 // 2) ** 2, "L14 possible links"),
    (l14_row["connected_components"] == length**2 // 2, "L14 components"),
    (l14_row["selected_edges_owner_once"] == 3 * length**3 // 2, "L14 selected edges"),
    (abs(l14_row["expected_retained_per_lineage"] - 0.5) < 1.0e-12, "L14 retained/lineage"),
    (l14_row["active_internal_edges_per_component"] == 28, "L14 internal supports"),
    (l14_row["active_connector_edges_per_component"] == 14, "L14 connector supports"),
    (l14_row["absolute_oriented_throughput_global"] > 0.0, "L14 total throughput"),
    (l14_row["absolute_connector_throughput_global"] > 0.0, "L14 connector throughput"),
    (abs(adjacent["site_ratio"] - adjacent["retained_ratio"]) < 1.0e-12, "L12/L14 prepared census ratio"),
    (adjacent["throughput_per_retained_ratio"] > 0.0, "L12/L14 total comparator"),
    (adjacent["connector_throughput_per_retained_ratio"] > 0.0, "L12/L14 connector comparator"),
    (packet["residual_status"].endswith("NOT_CALLED_DEFECTS"), "L14 residual classification"),
    (audit["target_disposition"] == "ELIGIBLE_FOR_PROMOTION_WITH_CLAIM_CEILINGS", "L14 audit disposition"),
]
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001",
    "classification": "HOSTILE_AUDITED_INPUT_APPEND__FINITE_RAW_RECORD_TRAJECTORY",
    "scope": "CONDITIONAL_CONNECTED_SUPPORT_AT_KAPPA_PI_OVER_TWO__NO_FIT_OR_EXTRAPOLATION",
    "base_trajectory_sha256": BASE_HASH,
    "rows": rows,
    "adjacent_comparators": adjacent_comparators,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_RECORD_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "not_claimed": "MONOTONICITY__TREND__CONVERGENCE__LIMIT__EXPONENT__FIT__SCALING_LAW__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
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
print(f"PASS__R_CONNECTED_RECORD_TRAJECTORY_L4_L14__{len(checks)}/{len(checks)}")
