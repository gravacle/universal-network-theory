#!/usr/bin/env python3
"""Hostile V004R3 consumer with complete staged-result authentication."""

from __future__ import annotations

import argparse
import gc
import json
import math
import os
import resource
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import independent_prefix_history_v004r2 as r2consumer
import v004r3_common as common


# Reuse only V004R2's frozen stable-descriptor/mapping and physical adapter
# implementation.  Its gate validators are never called.
r2consumer.common = common

ROW_KEYS = {
    "event", "input_prefix", "input_prefix_dimension", "logical_output_prefix_dimension",
    "terminal_children_streamed", "allow_probability", "blocked_probability",
    "reverse_support_probability", "blocked_null_state_error", "W_n",
    "q_retained_after_transport", "q_genesis_after", "sector_weights",
    "connector_delta_l1", "connector_delta_signed", "admission_total_content_residual",
    "admission_bandwidth_residual", "target_owner_residual", "transport_node_residual_l1",
    "transport_node_residual_linf", "null_transport_node_residual_l1",
    "transport_number_drift", "null_transport_number_drift", "actual_norm_error",
    "null_norm_error", "actual_solver", "null_solver",
}
SOLVER_KEYS = {"converged", "batches", "maximum_degree", "maximum_endpoint_difference",
               "maximum_tail_indicator_32", "algorithm", "quadrature_group_max",
               "allocation_vector_slots", "maximum_allocation_estimate_bytes",
               "allocation_limit_bytes"}
COMPARISON_KEYS = {"resolved", "classification", "epsilon", "maximum_admission_accounting_residual",
                   "maximum_node_continuity_residual_l1", "maximum_norm_error",
                   "maximum_number_drift", "rough_sharp", "sector", "admission_acceptance",
                   "routed_acceptance", "connector_ratio"}
RESOURCE_KEYS = {"peak_logical_state_plus_cache_bytes", "scratch_limit_bytes",
                 "maximum_numerical_allocation_estimate_bytes", "numerical_workspace_limit_bytes",
                 "authentication_peak_certificate_bytes", "peak_rss_bytes", "rss_limit_bytes",
                 "wall_seconds_including_authentication", "wall_limit_seconds", "passed"}
HISTORY_KEYS = {"schema", "L", "representation", "rows", "comparison", "terminal_shards",
                "cache_manifest_path", "cache_manifest_sha256", "semantic_cache_authentication_checks",
                "prerequisite_hashes", "resource", "implementation_sha256", "method_sha256",
                "freeze_sha256", "claim_boundary"}


def finite_number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(float(value))


def semantic_check_count(length: int) -> int:
    return 3 * length * (length + 1) + length * (length + 1) // 2 + length * (length - 1) // 2


def validate_history_document(record: dict[str, Any], length: int, cache_hash: str,
                              prerequisite_hashes: dict[str, str], freeze: dict[str, Any]) -> None:
    common.exact_keys(record, HISTORY_KEYS, "history result")
    if not (record["schema"] == "INDEPENDENT_STORAGE_CACHED_PREFIX_HISTORY_V004R3"
            and record["L"] == length
            and record["representation"] == "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS__IMMUTABLE_STORAGE_INDEX_CACHE"
            and record["cache_manifest_path"] == str(common.cache_root(length) / "CACHE_MANIFEST.json")
            and record["cache_manifest_sha256"] == cache_hash
            and record["semantic_cache_authentication_checks"] == semantic_check_count(length)
            and record["prerequisite_hashes"] == prerequisite_hashes
            and record["implementation_sha256"] == freeze["files"]["consumer"]
            and record["method_sha256"] == freeze["files"]["method"]
            and record["freeze_sha256"] == common.sha256(common.FREEZE)
            and record["claim_boundary"] == "INDEPENDENT_FINITE_CACHED_PREFIX_HISTORY_ONLY__NO_CONTINUUM_OR_GRAVITY"):
        raise common.Refusal("history result identity/lineage mismatch")
    rows = record["rows"]
    if not isinstance(rows, list) or len(rows) != length:
        raise common.Refusal("history result row census mismatch")
    for event, row in enumerate(rows):
        common.exact_keys(row, ROW_KEYS, f"history row {event}")
        if not (row["event"] == event + 1 and row["input_prefix"] == event
                and row["input_prefix_dimension"] == math.comb(2 * length + event, event)
                and row["logical_output_prefix_dimension"] == math.comb(2 * length + event + 1, event + 1)
                and row["terminal_children_streamed"] is (event == length - 1)
                and isinstance(row["sector_weights"], list) and len(row["sector_weights"]) == length + 1):
            raise common.Refusal("history row event/dimension/sector identity mismatch")
        numeric = ROW_KEYS - {"event", "input_prefix", "input_prefix_dimension",
                              "logical_output_prefix_dimension", "terminal_children_streamed",
                              "sector_weights", "actual_solver", "null_solver"}
        if any(not finite_number(row[key]) for key in numeric) or any(not finite_number(x) for x in row["sector_weights"]):
            raise common.Refusal("history row contains nonfinite/non-numeric observable")
        for role in ("actual_solver", "null_solver"):
            solver = row[role]
            common.exact_keys(solver, SOLVER_KEYS, f"{role} row {event}")
            if not (solver["converged"] is True and type(solver["batches"]) is int and solver["batches"] >= 0
                    and type(solver["maximum_degree"]) is int and solver["maximum_degree"] >= 0
                    and finite_number(solver["maximum_endpoint_difference"])
                    and finite_number(solver["maximum_tail_indicator_32"])
                    and solver["algorithm"] == "RECURRENCE_REPLAY_GL_GROUPS"
                    and solver["quadrature_group_max"] == r2consumer.legacy.replay.QUADRATURE_GROUP
                    and solver["allocation_vector_slots"] == r2consumer.legacy.replay.ALLOCATION_VECTOR_SLOTS
                    and solver["quadrature_group_max"] == r2consumer.legacy.replay.QUADRATURE_GROUP
                    and solver["allocation_vector_slots"] == r2consumer.legacy.replay.ALLOCATION_VECTOR_SLOTS
                    and type(solver["maximum_allocation_estimate_bytes"]) is int
                    and 0 <= solver["maximum_allocation_estimate_bytes"] <= common.NUMERICAL_WORKSPACE_LIMIT
                    and solver["allocation_limit_bytes"] == common.NUMERICAL_WORKSPACE_LIMIT):
                raise common.Refusal("history solver record incomplete/invalid")
    comparison = record["comparison"]
    common.exact_keys(comparison, COMPARISON_KEYS, "history comparison")
    if not (comparison["resolved"] is True and comparison["classification"] == "RESOLVED_PREFIX_HISTORY_CONTROL"
            and finite_number(comparison["epsilon"]) and comparison["epsilon"] > 0
            and all(finite_number(comparison[key]) for key in (
                "maximum_admission_accounting_residual", "maximum_node_continuity_residual_l1",
                "maximum_norm_error", "maximum_number_drift"))
            and all(isinstance(comparison[key], list) and len(comparison[key]) == length
                    and all(finite_number(value) for value in comparison[key])
                    for key in ("admission_acceptance", "routed_acceptance", "connector_ratio"))):
        raise common.Refusal("history comparison is not a complete resolved comparison")
    common.exact_keys(comparison["rough_sharp"], {"maximum_disagreement", "observable_linf", "sector_weight_linf"}, "rough/sharp")
    common.exact_keys(comparison["sector"], {"density_interval", "discarded_mass", "enclosed_mass", "late_events", "q_lower", "q_upper"}, "sector")
    if any(not finite_number(value) for value in comparison["rough_sharp"].values()):
        raise common.Refusal("rough/sharp comparison contains nonfinite value")
    sector = comparison["sector"]
    if not (isinstance(sector["density_interval"], list) and len(sector["density_interval"]) == 2
            and all(finite_number(value) for value in sector["density_interval"])
            and finite_number(sector["discarded_mass"]) and finite_number(sector["enclosed_mass"])
            and isinstance(sector["late_events"], list)
            and all(type(value) is int for value in sector["late_events"])
            and type(sector["q_lower"]) is int and type(sector["q_upper"]) is int
            and 0 <= sector["q_lower"] <= sector["q_upper"] <= length):
        raise common.Refusal("history sector comparison schema/value mismatch")
    terminal = record["terminal_shards"]
    if not isinstance(terminal, list) or len(terminal) != length:
        raise common.Refusal("terminal shard census mismatch")
    for q, row in enumerate(terminal):
        common.exact_keys(row, {"q", "path", "shape", "logical_bytes"}, "terminal shard")
        expected_shape = [math.comb(length - 1, q), math.comb(2 * length, q)]
        if row != {"q": q, "path": f"prefix_{length - 1:02d}/q_{q:02d}.c128",
                   "shape": expected_shape, "logical_bytes": 16 * math.prod(expected_shape)}:
            raise common.Refusal("terminal shard exact identity mismatch")
    resource_record = record["resource"]
    common.exact_keys(resource_record, RESOURCE_KEYS, "history resource")
    actual_cache = common.FROZEN_STORAGE[str(length)]["actual_cache_array_bytes"]
    if not (resource_record["passed"] is True
            and type(resource_record["peak_logical_state_plus_cache_bytes"]) is int
            and actual_cache <= resource_record["peak_logical_state_plus_cache_bytes"] <= common.SCRATCH_LIMIT
            and resource_record["scratch_limit_bytes"] == common.SCRATCH_LIMIT
            and type(resource_record["maximum_numerical_allocation_estimate_bytes"]) is int
            and 0 <= resource_record["maximum_numerical_allocation_estimate_bytes"] <= common.NUMERICAL_WORKSPACE_LIMIT
            and resource_record["numerical_workspace_limit_bytes"] == common.NUMERICAL_WORKSPACE_LIMIT
            and resource_record["authentication_peak_certificate_bytes"] == common.FROZEN_STORAGE["12"]["authentication_peak_bytes"]
            and type(resource_record["peak_rss_bytes"]) is int and 0 <= resource_record["peak_rss_bytes"] <= common.RSS_LIMIT
            and resource_record["rss_limit_bytes"] == common.RSS_LIMIT
            and finite_number(resource_record["wall_seconds_including_authentication"])
            and 0 <= resource_record["wall_seconds_including_authentication"] <= common.WALL_LIMIT
            and resource_record["wall_limit_seconds"] == common.WALL_LIMIT):
        raise common.Refusal("history exact resource result mismatch")
    maximum_row_allocation = max(row[role]["maximum_allocation_estimate_bytes"]
                                 for row in rows for role in ("actual_solver", "null_solver"))
    if resource_record["maximum_numerical_allocation_estimate_bytes"] != maximum_row_allocation:
        raise common.Refusal("history resource allocation does not reconstruct from rows")


def history_binding(length: int, output_hash: str, cache_hash: str) -> dict[str, Any]:
    return {"L": length, "path": str(common.history_output(length)), "sha256": output_hash,
            "cache_manifest_sha256": cache_hash}


def validate_comparison_document(record: dict[str, Any], schema: str,
                                 bindings: dict[str, Any]) -> None:
    common.exact_keys(record, {"schema", "classification", "resolved", "history_bindings",
                               "checks_passed", "checks_total", "maximum_observable_difference",
                               "maximum_sector_weight_difference", "tolerance", "claim_boundary"},
                      "stage comparison")
    if not (record["schema"] == schema and record["classification"] == "PASS" and record["resolved"] is True
            and record["history_bindings"] == bindings
            and type(record["checks_total"]) is int and record["checks_total"] > 0
            and record["checks_passed"] == record["checks_total"]
            and finite_number(record["tolerance"]) and record["tolerance"] > 0
            and finite_number(record["maximum_observable_difference"])
            and finite_number(record["maximum_sector_weight_difference"])
            and 0 <= record["maximum_observable_difference"] <= record["tolerance"]
            and 0 <= record["maximum_sector_weight_difference"] <= record["tolerance"]
            and record["claim_boundary"] == "FINITE_SAME_PATH_COMPARISON_ONLY"):
        raise common.Refusal("stage comparison not an actual positive all-pass comparison")


def base_gate_hashes(freeze: dict[str, Any], dual_hash: str) -> dict[str, str]:
    return {"consumer_sha256": freeze["files"]["consumer"], "method_sha256": freeze["files"]["method"],
            "freeze_sha256": common.sha256(common.FREEZE), "dual_gate_sha256": dual_hash}


def validate_control_execution_document(gate: dict[str, Any], cache_hashes: dict[str, str],
                                        freeze: dict[str, Any], dual_hash: str) -> None:
    common.exact_keys(gate, {"schema", "classification", "authorized_lengths", "cache_manifest_sha256_by_L",
                             "output_path_by_L", "workspace_path_by_L", "consumer_sha256", "method_sha256",
                             "freeze_sha256", "dual_gate_sha256", "claim_boundary"}, "control execution gate")
    if not (gate["schema"] == "HOSTILE_V004R3_CONTROL_EXECUTION_GATE"
            and gate["classification"] == "AUTHORIZE_HOSTILE_V004R3_CONTROLS_L4_L8"
            and gate["authorized_lengths"] == list(common.CONTROL_LENGTHS)
            and gate["cache_manifest_sha256_by_L"] == cache_hashes
            and gate["output_path_by_L"] == {str(L): str(common.history_output(L)) for L in common.CONTROL_LENGTHS}
            and gate["workspace_path_by_L"] == {str(L): str(common.workspace_root(L)) for L in common.CONTROL_LENGTHS}
            and all(gate[key] == value for key, value in base_gate_hashes(freeze, dual_hash).items())
            and gate["claim_boundary"] == "CONTROL_EXECUTION_AUTHORIZATION_ONLY"):
        raise common.Refusal("control execution gate exact binding mismatch")


def validate_control_pass_document(gate: dict[str, Any], histories: dict[str, tuple[str, dict[str, Any]]],
                                   comparison_hash: str, comparison: dict[str, Any],
                                   cache_hashes: dict[str, str], execution_hash: str,
                                   freeze: dict[str, Any], dual_hash: str) -> None:
    common.exact_keys(gate, {"schema", "classification", "histories", "comparison_report", "prerequisites",
                             "consumer_sha256", "method_sha256", "freeze_sha256", "dual_gate_sha256",
                             "claim_boundary"}, "control pass gate")
    bindings = {str(L): history_binding(L, histories[str(L)][0], cache_hashes[str(L)]) for L in common.CONTROL_LENGTHS}
    if not (gate["schema"] == "HOSTILE_V004R3_CONTROL_PASS_GATE"
            and gate["classification"] == "PASS_HOSTILE_V004R3_CACHED_CONTROLS_L4_L8"
            and gate["histories"] == bindings
            and gate["comparison_report"] == {"path": str(common.CONTROL_COMPARISON), "sha256": comparison_hash}
            and gate["prerequisites"] == {"dual_gate_sha256": dual_hash,
                                           "control_execution_gate_sha256": execution_hash}
            and all(gate[key] == value for key, value in base_gate_hashes(freeze, dual_hash).items())
            and gate["claim_boundary"] == "FINITE_CONTROL_PASS_ONLY"):
        raise common.Refusal("control pass gate exact binding mismatch")
    prerequisites = {"dual_gate_sha256": dual_hash, "control_execution_gate_sha256": execution_hash}
    for L in common.CONTROL_LENGTHS:
        validate_history_document(histories[str(L)][1], L, cache_hashes[str(L)], prerequisites, freeze)
    validate_comparison_document(comparison, "HOSTILE_V004R3_CONTROL_COMPARISON", bindings)


def validate_l10_execution_document(gate: dict[str, Any], cache_hash: str, control_hash: str,
                                    freeze: dict[str, Any], dual_hash: str) -> None:
    common.exact_keys(gate, {"schema", "classification", "authorized_length", "cache_manifest_sha256",
                             "output_path", "workspace_path", "prerequisites", "consumer_sha256",
                             "method_sha256", "freeze_sha256", "dual_gate_sha256", "claim_boundary"},
                      "L10 execution gate")
    if not (gate["schema"] == "HOSTILE_V004R3_L10_EXECUTION_GATE"
            and gate["classification"] == "AUTHORIZE_HOSTILE_V004R3_L10" and gate["authorized_length"] == 10
            and gate["cache_manifest_sha256"] == cache_hash and gate["output_path"] == str(common.history_output(10))
            and gate["workspace_path"] == str(common.workspace_root(10))
            and gate["prerequisites"] == {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash}
            and all(gate[key] == value for key, value in base_gate_hashes(freeze, dual_hash).items())
            and gate["claim_boundary"] == "L10_EXECUTION_AUTHORIZATION_ONLY"):
        raise common.Refusal("L10 execution gate exact binding mismatch")


def validate_l10_pass_document(gate: dict[str, Any], history_hash: str, history: dict[str, Any],
                               comparison_hash: str, comparison: dict[str, Any], cache_hash: str,
                               control_hash: str, execution_hash: str, freeze: dict[str, Any], dual_hash: str) -> None:
    common.exact_keys(gate, {"schema", "classification", "history", "comparison_report", "prerequisites",
                             "consumer_sha256", "method_sha256", "freeze_sha256", "dual_gate_sha256",
                             "claim_boundary"}, "L10 pass gate")
    binding = history_binding(10, history_hash, cache_hash)
    prerequisites = {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash,
                     "L10_execution_gate_sha256": execution_hash}
    if not (gate["schema"] == "HOSTILE_V004R3_L10_PASS_GATE"
            and gate["classification"] == "PASS_HOSTILE_V004R3_CACHED_L10"
            and gate["history"] == binding
            and gate["comparison_report"] == {"path": str(common.L10_COMPARISON), "sha256": comparison_hash}
            and gate["prerequisites"] == prerequisites
            and all(gate[key] == value for key, value in base_gate_hashes(freeze, dual_hash).items())
            and gate["claim_boundary"] == "FINITE_L10_PASS_ONLY"):
        raise common.Refusal("L10 pass gate exact binding mismatch")
    validate_history_document(history, 10, cache_hash, prerequisites, freeze)
    validate_comparison_document(comparison, "HOSTILE_V004R3_L10_COMPARISON", {"10": binding})


def validate_l12_execution_document(gate: dict[str, Any], cache_hash: str, control_hash: str,
                                    l10_hash: str, target_hash: str, freeze: dict[str, Any],
                                    dual_hash: str, parallel_hash: str) -> None:
    common.exact_keys(gate, {"schema", "classification", "authorized_length", "cache_manifest_sha256",
                             "output_path", "workspace_path", "prerequisites", "target_prerequisite",
                             "consumer_sha256", "method_sha256", "freeze_sha256", "dual_gate_sha256",
                             "claim_boundary"}, "L12 execution gate")
    target = {"path": str(common.REPO / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json"),
              "sha256": target_hash, "classification": "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004",
              "checks_passed": 273, "checks_total": 273}
    prerequisite = {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash,
                    "L10_pass_gate_sha256": l10_hash, "target_gate_sha256": target_hash,
                    "parallel_L12_execution_gate_sha256": parallel_hash}
    if not (gate["schema"] == "HOSTILE_V004R3_L12_EXECUTION_GATE"
            and gate["classification"] == "AUTHORIZE_HOSTILE_V004R3_L12" and gate["authorized_length"] == 12
            and gate["cache_manifest_sha256"] == cache_hash and gate["output_path"] == str(common.history_output(12))
            and gate["workspace_path"] == str(common.workspace_root(12))
            and gate["prerequisites"] == prerequisite and gate["target_prerequisite"] == target
            and all(gate[key] == value for key, value in base_gate_hashes(freeze, dual_hash).items())
            and gate["claim_boundary"] == "L12_EXECUTION_AUTHORIZATION_ONLY"):
        raise common.Refusal("L12 execution gate exact binding mismatch")


def validate_parallel_l12_document(gate: dict[str, Any], control_hash: str, l10_hash: str,
                                   target_hash: str, freeze: dict[str, Any], dual_hash: str) -> None:
    common.exact_keys(gate, {"schema", "classification", "authorized_length", "schedule",
                             "resource_certificate", "telemetry", "prerequisites", "consumer_sha256",
                             "method_sha256", "freeze_sha256", "dual_gate_sha256", "claim_boundary"},
                      "parallel L12 execution gate")
    prerequisites = {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash,
                     "hostile_L10_pass_gate_sha256": l10_hash, "target_gate_sha256": target_hash}
    telemetry = {"path": str(common.PARALLEL_L12_TELEMETRY),
                 "required_fields": common.PARALLEL_L12_CERTIFICATE["telemetry_required_fields"],
                 "must_be_absent_before_launch": True, "sample_interval_seconds_max": 60}
    schedule = {"mode": common.PARALLEL_L12_CERTIFICATE["execution_mode"],
                "target_role": "TARGET_V005", "hostile_role": "HOSTILE_V004R3",
                "launch_skew_seconds_max": 60, "launch_only_after_both_L10_pass": True}
    if not (gate["schema"] == "HOSTILE_V004R3_PARALLEL_L12_EXECUTION_GATE"
            and gate["classification"] == "AUTHORIZE_CONTEMPORANEOUS_TARGET_V005_HOSTILE_V004R3_L12"
            and gate["authorized_length"] == 12 and gate["schedule"] == schedule
            and gate["resource_certificate"] == common.PARALLEL_L12_CERTIFICATE
            and gate["telemetry"] == telemetry and gate["prerequisites"] == prerequisites
            and all(gate[key] == value for key, value in base_gate_hashes(freeze, dual_hash).items())
            and gate["claim_boundary"] == "PARALLEL_L12_SCHEDULING_AND_RESOURCE_AUTHORIZATION_ONLY"):
        raise common.Refusal("parallel L12 schedule/resource/telemetry binding mismatch")


class CacheContext(r2consumer.SecureCacheContext):
    def _validate_manifest(self) -> None:
        freeze = common.validate_freeze()
        common.exact_keys(self.manifest, {"schema", "status", "L", "basis_order", "edge_layout",
                          "hamiltonian_exchange_coefficient", "files", "array_file_count",
                          "manifest_inclusive_file_count", "payload", "method_sha256", "common_sha256",
                          "builder_sha256", "consumer_sha256", "freeze_sha256",
                          "dual_obstruction_gate_sha256", "canonical_cache_root", "claim_boundary"}, "cache manifest")
        if not (self.manifest["schema"] == "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R3"
                and self.manifest["status"] == "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE"
                and self.manifest["L"] == self.length and self.manifest["basis_order"] == "REVERSED_COMBINATION__FULL_MASK"
                and self.manifest["edge_layout"] == [list(edge) for edge in physical.hostile_edges(self.length)]
                and self.manifest["hamiltonian_exchange_coefficient"] == -1
                and self.manifest["canonical_cache_root"] == str(self.root)
                and self.manifest["claim_boundary"] == "STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"):
            raise common.Refusal("cache manifest identity mismatch")
        expected = {"method_sha256": freeze["files"]["method"], "common_sha256": freeze["files"]["common"],
                    "builder_sha256": freeze["files"]["builder"], "consumer_sha256": freeze["files"]["consumer"],
                    "freeze_sha256": common.sha256(common.FREEZE)}
        if any(self.manifest[key] != value for key, value in expected.items()):
            raise common.Refusal("cache manifest frozen lineage mismatch")
        if not common.DUAL_GATE.is_file() or self.manifest["dual_obstruction_gate_sha256"] != common.sha256(common.DUAL_GATE):
            raise common.Refusal("cache manifest dual-gate lineage mismatch")
        common.require_dual_gate(self.length)
        common.validate_manifest_record_census(self.manifest, self.length)


def read_record(path: Path) -> tuple[dict[str, Any], str]:
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o222:
        raise common.Refusal(f"required immutable record absent: {path.name}")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise common.Refusal(f"required record is not an object: {path.name}")
    return record, common.sha256(path)


def cache_manifest_hash(length: int) -> str:
    path = common.cache_root(length) / "CACHE_MANIFEST.json"
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o222:
        raise common.Refusal(f"canonical immutable L{length} cache manifest absent")
    return common.sha256(path)


def read_history(length: int, expected_hash: str) -> dict[str, Any]:
    record, actual_hash = read_record(common.history_output(length))
    if actual_hash != expected_hash:
        raise common.Refusal(f"L{length} history output hash mismatch")
    return record


def validate_target_prerequisite() -> str:
    relative = "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json"
    target_hash = common.r2.SEALED_DEPENDENCIES[relative]
    path = common.safe_repo_file(relative, target_hash)
    gate = json.loads(path.read_text(encoding="utf-8"))
    if not (gate.get("schema") == "R_TARGET_Q_SHARDED_HISTORY_GATE_V004"
            and gate.get("classification") == "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004"
            and gate.get("checks_passed") == gate.get("checks_total") == 273
            and gate.get("implementation_sha256") == common.OBSTRUCTION_ROWS["target"]["implementation_sha256"]
            and set(gate.get("histories", {})) == {"4", "6", "8", "10"}):
        raise common.Refusal("target L12 prerequisite internal result mismatch")
    return target_hash


def require_execution_gate(length: int, current_cache_hash: str) -> dict[str, str]:
    freeze = common.validate_freeze()
    _dual, dual_hash = common.require_dual_gate(length)
    control_cache_hashes = {str(L): cache_manifest_hash(L) for L in common.CONTROL_LENGTHS}
    control_exec, control_exec_hash = read_record(common.CONTROL_EXECUTION_GATE)
    validate_control_execution_document(control_exec, control_cache_hashes, freeze, dual_hash)
    if length in common.CONTROL_LENGTHS:
        if current_cache_hash != control_cache_hashes[str(length)]:
            raise common.Refusal("current control cache manifest mismatch")
        return {"dual_gate_sha256": dual_hash, "control_execution_gate_sha256": control_exec_hash}

    control_gate, control_hash = read_record(common.CONTROL_GATE)
    control_bindings = control_gate.get("histories")
    if not isinstance(control_bindings, dict) or set(control_bindings) != {str(L) for L in common.CONTROL_LENGTHS}:
        raise common.Refusal("control gate history binding census absent")
    control_histories: dict[str, tuple[str, dict[str, Any]]] = {}
    for L in common.CONTROL_LENGTHS:
        binding = control_bindings[str(L)]
        if not isinstance(binding, dict) or not isinstance(binding.get("sha256"), str):
            raise common.Refusal("control history binding malformed")
        control_histories[str(L)] = (binding["sha256"], read_history(L, binding["sha256"]))
    control_comparison, control_comparison_hash = read_record(common.CONTROL_COMPARISON)
    validate_control_pass_document(control_gate, control_histories, control_comparison_hash,
                                   control_comparison, control_cache_hashes, control_exec_hash,
                                   freeze, dual_hash)

    l10_cache_hash = cache_manifest_hash(10)
    l10_exec, l10_exec_hash = read_record(common.L10_EXECUTION_GATE)
    validate_l10_execution_document(l10_exec, l10_cache_hash, control_hash, freeze, dual_hash)
    if length == 10:
        if current_cache_hash != l10_cache_hash:
            raise common.Refusal("current L10 cache manifest mismatch")
        return {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash,
                "L10_execution_gate_sha256": l10_exec_hash}

    l10_gate, l10_hash = read_record(common.L10_GATE)
    l10_binding = l10_gate.get("history")
    if not isinstance(l10_binding, dict) or not isinstance(l10_binding.get("sha256"), str):
        raise common.Refusal("L10 history binding malformed")
    l10_history = read_history(10, l10_binding["sha256"])
    l10_comparison, l10_comparison_hash = read_record(common.L10_COMPARISON)
    validate_l10_pass_document(l10_gate, l10_binding["sha256"], l10_history,
                               l10_comparison_hash, l10_comparison, l10_cache_hash,
                               control_hash, l10_exec_hash, freeze, dual_hash)
    target_hash = validate_target_prerequisite()
    parallel_gate, parallel_hash = read_record(common.PARALLEL_L12_GATE)
    validate_parallel_l12_document(parallel_gate, control_hash, l10_hash, target_hash, freeze, dual_hash)
    if common.PARALLEL_L12_TELEMETRY.exists():
        raise common.Refusal("parallel L12 telemetry path must be absent before launch")
    l12_cache_hash = cache_manifest_hash(12)
    l12_gate, l12_gate_hash = read_record(common.L12_EXECUTION_GATE)
    validate_l12_execution_document(l12_gate, l12_cache_hash, control_hash, l10_hash,
                                    target_hash, freeze, dual_hash, parallel_hash)
    if length != 12 or current_cache_hash != l12_cache_hash:
        raise common.Refusal("current L12 cache/length mismatch")
    return {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash,
            "L10_pass_gate_sha256": l10_hash, "L12_execution_gate_sha256": l12_gate_hash,
            "target_gate_sha256": target_hash, "parallel_L12_execution_gate_sha256": parallel_hash}


def execute(length: int) -> None:
    started = time.perf_counter()
    freeze = common.validate_freeze()
    output, workspace = common.history_output(length), common.workspace_root(length)
    common.require_canonical(output, common.history_output(length), "history output")
    common.require_canonical(workspace, common.workspace_root(length), "history workspace")
    if output.exists() or workspace.exists():
        raise common.Refusal("refuse overwrite canonical history output/workspace")
    manifest_path = common.cache_root(length) / "CACHE_MANIFEST.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise common.Refusal("canonical cache manifest absent")
    manifest_hash = common.sha256(manifest_path)
    prerequisite_hashes = require_execution_gate(length, manifest_hash)
    cache = CacheContext(length, manifest_hash, started)
    try:
        workspace_fs = common.existing_ancestor(common.WORKSPACE_PARENT)
        if workspace_fs.stat().st_dev != cache.root.stat().st_dev:
            raise common.Refusal("cache/workspace filesystem mismatch")
        required = common.FROZEN_STORAGE[str(length)]["state_plus_actual_cache_bytes"] + common.OVERHEAD_RESERVE
        if required > common.SCRATCH_LIMIT or shutil.disk_usage(workspace_fs).free < required:
            raise common.Refusal(f"workspace-filesystem scratch preflight failed: required={required}")
        elapsed = time.perf_counter() - started
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if elapsed > common.WALL_LIMIT or rss > common.RSS_LIMIT:
            raise common.Refusal("cache/gate authentication exhausted resource guard")
        common.WORKSPACE_PARENT.mkdir(mode=0o755, exist_ok=True)
        common.HISTORY_PARENT.mkdir(mode=0o755, exist_ok=True)
        r2consumer.legacy.configure(length, cache, started)
        rough_root, sharp_root = workspace / "rough", workspace / "sharp"
        rough = v3.history(length, physical.ROUGH, rough_root, retain_terminal=False)
        v3.remove_resolution(rough_root)
        sharp = v3.history(length, physical.SHARP, sharp_root, retain_terminal=True)
        comparison = physical.compare(length, rough, sharp)
        wall = time.perf_counter() - started
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        cache_bytes = common.FROZEN_STORAGE[str(length)]["actual_cache_array_bytes"]
        peak_scratch = max(int(rough["peak_logical_scratch_bytes"]), int(sharp["peak_logical_scratch_bytes"])) + cache_bytes
        allocation = max(int(row[key]["maximum_allocation_estimate_bytes"])
                         for row in sharp["rows"] for key in ("actual_solver", "null_solver"))
        passed = (comparison.get("resolved") is True and peak_scratch <= common.SCRATCH_LIMIT
                  and allocation <= common.NUMERICAL_WORKSPACE_LIMIT and rss <= common.RSS_LIMIT
                  and wall <= common.WALL_LIMIT)
        if not passed:
            raise common.Refusal("physical result failed comparison/resource gates; no result written")
        result = {
            "schema": "INDEPENDENT_STORAGE_CACHED_PREFIX_HISTORY_V004R3", "L": length,
            "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS__IMMUTABLE_STORAGE_INDEX_CACHE",
            "rows": sharp["rows"], "comparison": comparison, "terminal_shards": sharp["terminal_shards"],
            "cache_manifest_path": str(manifest_path), "cache_manifest_sha256": manifest_hash,
            "semantic_cache_authentication_checks": cache.semantic_checks,
            "prerequisite_hashes": prerequisite_hashes,
            "resource": {"peak_logical_state_plus_cache_bytes": peak_scratch,
                         "scratch_limit_bytes": common.SCRATCH_LIMIT,
                         "maximum_numerical_allocation_estimate_bytes": allocation,
                         "numerical_workspace_limit_bytes": common.NUMERICAL_WORKSPACE_LIMIT,
                         "authentication_peak_certificate_bytes": common.FROZEN_STORAGE["12"]["authentication_peak_bytes"],
                         "peak_rss_bytes": rss, "rss_limit_bytes": common.RSS_LIMIT,
                         "wall_seconds_including_authentication": wall,
                         "wall_limit_seconds": common.WALL_LIMIT, "passed": True},
            "implementation_sha256": freeze["files"]["consumer"], "method_sha256": freeze["files"]["method"],
            "freeze_sha256": common.sha256(common.FREEZE),
            "claim_boundary": "INDEPENDENT_FINITE_CACHED_PREFIX_HISTORY_ONLY__NO_CONTINUUM_OR_GRAVITY",
        }
        validate_history_document(result, length, manifest_hash, prerequisite_hashes, freeze)
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o444)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    finally:
        cache.close(); r2consumer.legacy.CACHE = None; gc.collect()


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("execute", choices=("execute",))
    parser.add_argument("--length", type=int, choices=common.SUPPORTED, required=True)
    args = parser.parse_args()
    try:
        execute(args.length)
    except (AssertionError, MemoryError, OSError, common.Refusal, r2consumer.common.Refusal,
            TimeoutError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
