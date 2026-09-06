#!/usr/bin/env python3
"""Compile the hostile-audited connected L4/L6/L8/L10 record trajectory."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_name("RESULT.json")
KAPPA = math.pi / 2.0
INPUTS = {
    4: (
        ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json",
        "043c85675cfc4956fa2e5216a324e941bf84523bf4abd0054ed2be07f378bbdc",
    ),
    6: (
        ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json",
        "e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
    ),
    8: (
        ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json",
        "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
    ),
    10: (
        ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001" / "RESULT.json",
        "06256f48fb39df0b5121ea01b38893ffeb84ba1bc7f842d22935ccd5279cdcbf",
    ),
}


rows = []
for length, (path, expected_hash) in INPUTS.items():
    observed_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed_hash != expected_hash:
        raise AssertionError(f"input custody mismatch at L={length}")
    packet = json.loads(path.read_text())
    if length == 4:
        record = next(row for row in packet["rows"] if row["kappa"] == KAPPA)
    else:
        record = packet
    census = packet["census"]
    currents = record["integrated_oriented_currents"]
    q_after = record["q_after"]
    retained = record["expected_retained_global"]
    total = record["absolute_oriented_throughput_global"]
    connector = record["absolute_connector_throughput_global"]
    rows.append(
        {
            "L": length,
            "input_sha256": observed_hash,
            "sites": census["sites_global"],
            "sites_per_F3_layer": census["sites_per_F3_layer"],
            "possible_F3_links": census["possible_F3_links"],
            "connected_components": census["components"],
            "sites_per_component": census["sites_per_component"],
            "selected_edges_owner_once": census["selected_edges_global_owner_once"],
            "prepared_source_lineages": census["prepared_source_lineages"],
            "expected_retained_total": retained,
            "expected_retained_per_lineage": retained / census["prepared_source_lineages"],
            "active_internal_edges_per_component": record["active_internal_supports_per_component"],
            "active_connector_edges_per_component": record["active_connector_supports_per_component"],
            "internal_current_magnitude": max(abs(value) for value in currents[: 2 * length]),
            "connector_current_magnitude": max(abs(value) for value in currents[2 * length :]),
            "q_after_even_mean": sum(q_after[0::2]) / length,
            "q_after_odd_mean": sum(q_after[1::2]) / length,
            "absolute_oriented_throughput_global": total,
            "absolute_oriented_throughput_per_retained": total / retained,
            "absolute_connector_throughput_global": connector,
            "absolute_connector_throughput_per_retained": connector / retained,
            "connector_share_of_absolute_throughput": connector / total,
            "max_abs_connected_edge_correlation": record["max_abs_connected_edge_correlation"],
            "record_ledger_residual_l1_per_component": record["record_ledger_residual_l1_per_component"],
            "record_ledger_residual_linf_per_component": record["record_ledger_residual_linf_per_component"],
            "record_ledger_residual_l1_global_bound": record["record_ledger_residual_l1_global_bound"],
        }
    )

adjacent_comparators = []
for previous, current in zip(rows, rows[1:]):
    adjacent_comparators.append(
        {
            "from_L": previous["L"],
            "to_L": current["L"],
            "site_ratio": current["sites"] / previous["sites"],
            "retained_ratio": current["expected_retained_total"] / previous["expected_retained_total"],
            "total_throughput_ratio": current["absolute_oriented_throughput_global"] / previous["absolute_oriented_throughput_global"],
            "throughput_per_retained_ratio": current["absolute_oriented_throughput_per_retained"] / previous["absolute_oriented_throughput_per_retained"],
            "connector_throughput_ratio": current["absolute_connector_throughput_global"] / previous["absolute_connector_throughput_global"],
            "connector_throughput_per_retained_ratio": current["absolute_connector_throughput_per_retained"] / previous["absolute_connector_throughput_per_retained"],
        }
    )

checks = []
for row in rows:
    length = row["L"]
    checks.extend(
        [
            (row["sites"] == length**3, f"L{length} site census"),
            (row["sites_per_F3_layer"] == length**3 // 2, f"L{length} F3 layers"),
            (row["possible_F3_links"] == (length**3 // 2) ** 2, f"L{length} possible links"),
            (row["connected_components"] == length**2 // 2, f"L{length} components"),
            (row["selected_edges_owner_once"] == 3 * length**3 // 2, f"L{length} selected edges"),
            (abs(row["expected_retained_per_lineage"] - 0.5) < 2.0e-13, f"L{length} retained/lineage"),
            (row["active_internal_edges_per_component"] == 2 * length and row["active_connector_edges_per_component"] == length, f"L{length} active support"),
        ]
    )
checks.extend(
    [
        (all(row["absolute_oriented_throughput_global"] > 0.0 for row in rows), "positive total throughputs"),
        (all(row["absolute_connector_throughput_global"] > 0.0 for row in rows), "positive connector throughputs"),
        (all(abs(item["site_ratio"] - item["retained_ratio"]) < 1.0e-12 for item in adjacent_comparators), "prepared retention tracks finite census"),
        (all(item["throughput_per_retained_ratio"] > 0.0 for item in adjacent_comparators), "positive adjacent per-retained comparators"),
        (all(item["connector_throughput_per_retained_ratio"] > 0.0 for item in adjacent_comparators), "positive adjacent connector comparators"),
    ]
)
failures = [label for passed, label in checks if not passed]
out = {
    "schema": "R_CONNECTED_RECORD_TRAJECTORY_L4_L10_V001",
    "classification": "HOSTILE_AUDITED_INPUT_COMPILATION__FINITE_RAW_RECORD_TRAJECTORY",
    "scope": "CONDITIONAL_CONNECTED_SUPPORT_AT_KAPPA_PI_OVER_TWO__NO_FIT_OR_EXTRAPOLATION",
    "rows": rows,
    "adjacent_comparators": adjacent_comparators,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_NUMERICAL_RECORD_LEDGER_TERMS__NOT_CALLED_DEFECTS",
    "not_claimed": "MONOTONICITY__LIMIT__EXPONENT__SCALING_LAW__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__CRITICAL_PHASE__GRAVITY",
}


def assert_compatible(observed: object, canonical: object, path: str = "root") -> None:
    if isinstance(canonical, dict):
        if not isinstance(observed, dict) or set(observed) != set(canonical):
            raise AssertionError(f"canonical keys differ at {path}")
        for key in canonical:
            assert_compatible(observed[key], canonical[key], f"{path}.{key}")
        return
    if isinstance(canonical, list):
        if not isinstance(observed, list) or len(observed) != len(canonical):
            raise AssertionError(f"canonical list differs at {path}")
        for index, (left, right) in enumerate(zip(observed, canonical)):
            assert_compatible(left, right, f"{path}[{index}]")
        return
    if isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 5.0e-12:
            raise AssertionError(f"canonical float differs at {path}")
        return
    if observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    assert_compatible(out, json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
if failures:
    raise AssertionError(failures)
print(f"PASS__R_CONNECTED_RECORD_TRAJECTORY_L4_L10__{len(checks)}/{len(checks)}")
