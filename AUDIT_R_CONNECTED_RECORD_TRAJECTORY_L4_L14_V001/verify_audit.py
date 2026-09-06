#!/usr/bin/env python3
"""Pinned verification for the hostile L4--L14 trajectory append audit."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE_PATH = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L12_V001" / "RESULT.json"
L14_PATH = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001" / "RESULT.json"
L14_AUDIT = ROOT / "AUDIT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001"
TARGET = ROOT / "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001"

PINS = {
    BASE_PATH: "8fe9697c833542812bbda78ea5528265b048d1775ace43a7203e1c583c7b5759",
    L14_PATH: "e8134d5311b9bdfd62ce7df5988da803b110516606ce905a1bc49bd65cdb5fbe",
    L14_AUDIT / "RESULT.json": "cf4301e55f0c911196ecfbd2f02d60ebcfc32def3353472dccb87077ca77d204",
    L14_AUDIT / "INDEPENDENT_RESULT.json": "bfa8fd0eb4ff793662af546408882b84ba55ec0ff38145263d8c9747660919be",
    L14_AUDIT / "verify_audit.py": "9786f8ad17f4d1d851f0b9afec17d675d8e84a9a5d5e6f7a074fb820b9a9bfc2",
    TARGET / "README.md": "c0ab043df521d60bbcc4e4bc643ed0234e1a194528a1cb6544703061d8acfc61",
    TARGET / "RESULT.json": "8a69f780a372ae436ef2fe458af80f7fa1ba70d8c93b21d91524c6e9819d753d",
    TARGET / "THEOREM.md": "8d95a25f5c1cefc45a8825b06686fddac68295708753b481eadd5a6abddfd34f",
    TARGET / "compile_trajectory.py": "a9dde10bf870a9b85d9db3bfea4ae5c42d276416d228f93d1306956ac08b0e46",
    HERE / "README.md": "0b2baef336a35af6363db304c163d84b53e151335660bc6566f7aed84e2b04df",
    HERE / "REPORT.md": "c96b7510f6f5d39fd3436fa8f2f92fe38820104865ace3a29d1255b63799d9a8",
    HERE / "RESULT.json": "c42a94533d9d9795370bb0a997e19b21267d3fc78a4e681f2e07bc83ff6d68a5",
    HERE / "RESULT.md": "b70d4c4907c0c7d623ee40a7285c90d33941e663c9d3a20b0cd1778d548502b3",
    HERE / "independent_reconstruction.py": "7c6fceef93a8d4d269b7728ed69ee5ca55924f331695944fdd11fc0cb3fc2b95",
    HERE / "INDEPENDENT_RESULT.json": "8c2422cd156a99debfd436652b9ec931fed4df4eff2c6507c7001214072d0dd8",
}

NOT_CLAIMED = (
    "MONOTONICITY__TREND__CONVERGENCE__LIMIT__EXPONENT__FIT__SCALING_LAW__"
    "AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY"
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


checks = []


def check(condition, label):
    checks.append((bool(condition), label))


check(all(digest(path) == expected for path, expected in PINS.items()), "all custody pins")
base = json.loads(BASE_PATH.read_text())
l14 = json.loads(L14_PATH.read_text())
l14_audit = json.loads((L14_AUDIT / "RESULT.json").read_text())
l14_detail = json.loads((L14_AUDIT / "INDEPENDENT_RESULT.json").read_text())
target = json.loads((TARGET / "RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
summary = json.loads((HERE / "RESULT.json").read_text())

check(base["checks_passed"] == base["checks_total"] == 16, "base target 16/16")
check(target["checks_passed"] == target["checks_total"] == 18, "append target 18/18")
check(independent["checks_passed"] == independent["checks_total"] == 31, "independent append 31/31")
check(not independent["failures"], "independent failure list empty")
check(independent["verdict"] == "PASS__INDEPENDENT_APPEND_RECONSTRUCTION", "independent verdict")
check(summary["verdict"] == "PASS_AFTER_BOUNDED_LABEL_REPAIR__NO_NUMERICAL_DISCREPANCY", "summary verdict")
check(not summary["numerical_discrepancies"], "no numerical discrepancies")

check(len(base["rows"]) == 5 and [row["L"] for row in base["rows"]] == [4, 6, 8, 10, 12], "base row sequence")
check(len(base["adjacent_comparators"]) == 4, "base comparator count")
check([(row["from_L"], row["to_L"]) for row in base["adjacent_comparators"]]
      == [(4, 6), (6, 8), (8, 10), (10, 12)], "base comparator sequence")
check(target["rows"][:5] == base["rows"], "five prior rows exact")
check(target["adjacent_comparators"][:4] == base["adjacent_comparators"], "four prior comparators exact")
check(canonical_digest(base["rows"]) == "936072342c26b649efce4027a8924d9d51b12650834904256fae0ed2b202d2f6", "base row canonical hash")
check(canonical_digest(base["adjacent_comparators"]) == "8c92d99f535ee3956325cde97c5d09add7aea1e93f90fff4d7352f40276ed334", "base comparator canonical hash")
check(independent["base_prefix"]["exactly_preserved"], "independent prefix disposition")

census = l14["census"]
currents = l14["integrated_oriented_currents"]
q = l14["q_after"]
retained = l14["expected_retained_global"]
total = l14["absolute_oriented_throughput_global"]
connector = l14["absolute_connector_throughput_global"]
row = {
    "L": 14,
    "input_sha256": PINS[L14_PATH],
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
    "internal_current_magnitude": max(abs(value) for value in currents[:28]),
    "connector_current_magnitude": max(abs(value) for value in currents[28:]),
    "q_after_even_mean": sum(q[0::2]) / 14,
    "q_after_odd_mean": sum(q[1::2]) / 14,
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
check(row == target["rows"][-1], "fresh L14 row reconstruction")
check(row == independent["appended_l14_row"], "saved independent L14 row")
check(row["sites"] == 2744 and row["sites_per_F3_layer"] == 1372, "L14 site census")
check(row["connected_components"] == 98 and row["selected_edges_owner_once"] == 4116, "L14 component/edge census")
check(row["prepared_source_lineages"] == 1372, "L14 lineage census")
check(row["active_internal_edges_per_component"] == 28 and row["active_connector_edges_per_component"] == 14, "L14 active support census")
check(len(currents) == 42 and all(abs(value) > 1e-10 for value in currents), "all L14 currents active")
check(abs(98 * sum(abs(value) for value in currents) - total) < 2e-12, "L14 total throughput arithmetic")
check(abs(98 * sum(abs(value) for value in currents[28:]) - connector) < 2e-12, "L14 connector throughput arithmetic")
check(abs(row["expected_retained_per_lineage"] - 0.5) < 1e-12, "L14 retained per lineage")
check(row["record_ledger_residual_l1_per_component"] > 0 and row["record_ledger_residual_linf_per_component"] > 0, "L14 raw residual retained")

previous = base["rows"][-1]
adjacent = {
    "from_L": 12,
    "to_L": 14,
    "site_ratio": row["sites"] / previous["sites"],
    "retained_ratio": row["expected_retained_total"] / previous["expected_retained_total"],
    "total_throughput_ratio": row["absolute_oriented_throughput_global"] / previous["absolute_oriented_throughput_global"],
    "throughput_per_retained_ratio": row["absolute_oriented_throughput_per_retained"] / previous["absolute_oriented_throughput_per_retained"],
    "connector_throughput_ratio": row["absolute_connector_throughput_global"] / previous["absolute_connector_throughput_global"],
    "connector_throughput_per_retained_ratio": row["absolute_connector_throughput_per_retained"] / previous["absolute_connector_throughput_per_retained"],
}
check(adjacent == target["adjacent_comparators"][-1], "fresh L12-to-L14 comparator")
check(adjacent == independent["appended_L12_to_L14_comparator"], "saved independent comparator")
check(adjacent["site_ratio"] > 0 and adjacent["retained_ratio"] > 0, "finite census comparator")
check(adjacent["total_throughput_ratio"] > 0 and adjacent["connector_throughput_ratio"] > 0, "finite raw throughput comparator")
check(adjacent["throughput_per_retained_ratio"] > 0 and adjacent["connector_throughput_per_retained_ratio"] > 0, "finite per-retained comparator")

check(l14["checks_passed"] == l14["checks_total"] == 28, "L14 target 28/28")
check(l14_audit["verdict"] == "PASS__INDEPENDENT_L14_NUMERICAL_RECONSTRUCTION", "L14 hostile verdict")
check(l14_audit["independent_checks"] == "29/29", "L14 hostile summary 29/29")
check(l14_detail["checks_passed"] == l14_detail["checks_total"] == 29, "L14 hostile detail 29/29")
check(l14_detail["target_reproduction"]["current_linf"] < 6e-9, "L14 hostile current reproduction")
check(l14_detail["target_reproduction"]["all_comparator_linf"] < 6e-8, "L14 hostile comparator reproduction")
check(l14["residual_status"].endswith("NOT_CALLED_DEFECTS"), "source residual classification")
check(target["residual_status"].endswith("NOT_CALLED_DEFECTS"), "trajectory residual classification")
check(target["not_claimed"] == independent["not_claimed"] == summary["not_claimed"] == NOT_CLAIMED, "complete structured claim ceiling")
check(summary["target_disposition"] == "ELIGIBLE_AS_FINITE_RAW_RECORD_APPEND_ONLY", "finite-only disposition")
check(summary["bounded_target_repairs"] == [
    "STRUCTURED_NOT_CLAIMED_ADDED_TREND_AND_GENERIC_PHASE",
    "README_CLARIFIED_EXACT_PARSED_DATA_NOT_SERIALIZED_BYTE_IDENTITY",
], "bounded repair disclosure")

report = (HERE / "REPORT.md").read_text()
result_md = (HERE / "RESULT.md").read_text()
check("PASS after a bounded label repair" in report and "no numerical discrepancy" in report, "hostile report verdict")
check("not called defects" in report and "one finite comparison only" in report, "hostile report residual/comparator ceiling")
check(all(term in report for term in ("monotonicity", "trend", "convergence", "limit", "exponent", "fit", "scaling law")), "hostile report numerical ceiling")
check(all(term in report for term in ("autonomous support", "physical", "grid", "continuum", "Ward", "phase", "graviton", "gravity")), "hostile report physical ceiling")
check("31/31" in result_md and "18/18" in result_md and "29/29" in result_md and "56/56" in result_md, "result check custody")

failures = [label for passed, label in checks if not passed]
if failures:
    raise AssertionError(failures)
print(f"PASS__CONNECTED_TRAJECTORY_L4_L14_HOSTILE_AUDIT__{len(checks)}/{len(checks)}")
