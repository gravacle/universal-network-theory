#!/usr/bin/env python3
"""Append the audited connected L12 row to the sealed L4--L10 trajectory."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
BASE = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L10_V001" / "RESULT.json"
L12 = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION_V001" / "RESULT.json"
BASE_HASH = "1bb1ee2bceb242c32d97b89e45160d2983de18aaaa802a68034528df8d5db5df"
L12_HASH = "154c9195b8ea516e4e637c1f4d66422ab82603163119f9b4451e7c2eb7ff5184"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if digest(BASE) != BASE_HASH or digest(L12) != L12_HASH:
    raise AssertionError("sealed input custody mismatch")
base = json.loads(BASE.read_text())
packet = json.loads(L12.read_text())
census = packet["census"]
currents = packet["integrated_oriented_currents"]
q_after = packet["q_after"]
retained = packet["expected_retained_global"]
total = packet["absolute_oriented_throughput_global"]
connector = packet["absolute_connector_throughput_global"]
length = 12
l12_row = {
    "L": length,
    "input_sha256": L12_HASH,
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
    "site_ratio": l12_row["sites"] / previous["sites"],
    "retained_ratio": l12_row["expected_retained_total"] / previous["expected_retained_total"],
    "total_throughput_ratio": l12_row["absolute_oriented_throughput_global"] / previous["absolute_oriented_throughput_global"],
    "throughput_per_retained_ratio": l12_row["absolute_oriented_throughput_per_retained"] / previous["absolute_oriented_throughput_per_retained"],
    "connector_throughput_ratio": l12_row["absolute_connector_throughput_global"] / previous["absolute_connector_throughput_global"],
    "connector_throughput_per_retained_ratio": l12_row["absolute_connector_throughput_per_retained"] / previous["absolute_connector_throughput_per_retained"],
}
rows = base["rows"] + [l12_row]
adjacent_comparators = base["adjacent_comparators"] + [adjacent]

checks = [
    ([row["L"] for row in rows] == [4, 6, 8, 10, 12], "five-size row order"),
    (base["rows"] == rows[:4], "sealed base rows unchanged"),
    (base["adjacent_comparators"] == adjacent_comparators[:3], "sealed base comparators unchanged"),
    (l12_row["sites"] == length**3, "L12 site census"),
    (l12_row["sites_per_F3_layer"] == length**3 // 2, "L12 F3 layers"),
    (l12_row["possible_F3_links"] == (length**3 // 2) ** 2, "L12 possible links"),
    (l12_row["connected_components"] == length**2 // 2, "L12 components"),
    (l12_row["selected_edges_owner_once"] == 3 * length**3 // 2, "L12 selected edges"),
    (abs(l12_row["expected_retained_per_lineage"] - 0.5) < 1.0e-12, "L12 retained/lineage"),
    (l12_row["active_internal_edges_per_component"] == 24, "L12 internal supports"),
    (l12_row["active_connector_edges_per_component"] == 12, "L12 connector supports"),
    (l12_row["absolute_oriented_throughput_global"] > 0.0, "L12 total throughput"),
    (l12_row["absolute_connector_throughput_global"] > 0.0, "L12 connector throughput"),
    (abs(adjacent["site_ratio"] - adjacent["retained_ratio"]) < 1.0e-12, "L10/L12 prepared census ratio"),
    (adjacent["throughput_per_retained_ratio"] > 0.0, "L10/L12 total comparator"),
    (adjacent["connector_throughput_per_retained_ratio"] > 0.0, "L10/L12 connector comparator"),
]
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_CONNECTED_RECORD_TRAJECTORY_L4_L12_V001",
    "classification": "HOSTILE_AUDITED_INPUT_APPEND__FINITE_RAW_RECORD_TRAJECTORY",
    "scope": "CONDITIONAL_CONNECTED_SUPPORT_AT_KAPPA_PI_OVER_TWO__NO_FIT_OR_EXTRAPOLATION",
    "base_trajectory_sha256": BASE_HASH,
    "rows": rows,
    "adjacent_comparators": adjacent_comparators,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_RECORD_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "not_claimed": "MONOTONICITY__CONVERGENCE__LIMIT__EXPONENT__SCALING_LAW__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__CRITICAL_PHASE__GRAVITY",
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
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_CONNECTED_RECORD_TRAJECTORY_L4_L12__{len(checks)}/{len(checks)}")
