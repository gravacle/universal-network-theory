#!/usr/bin/env python3
"""Nonphysical custody and exact gate primitives for hostile V004R3."""

from __future__ import annotations

import hashlib
import json
import math
import os
import stat
from pathlib import Path
from typing import Any

import v004r2_common as r2


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
FREEZE = HERE / "FROZEN_MANIFEST_V004R3.json"
METHOD = HERE / "V004R3_STORAGE_ONLY_CACHE_METHOD.md"
BUILDER = HERE / "build_hostile_v004r3_cache.py"
CONSUMER = HERE / "independent_prefix_history_v004r3.py"
PREFLIGHT = HERE / "validate_v004r3_cache_preflight.py"
CACHE_PARENT = HERE / "V004R3_CACHE_PAYLOADS"
HISTORY_PARENT = HERE / "V004R3_HISTORY_OUTPUTS"
WORKSPACE_PARENT = HERE / "V004R3_WORKSPACES"
DUAL_GATE = HERE / "DUAL_SIX_HOUR_OBSTRUCTION_GATE_V004R3.json"
CONTROL_EXECUTION_GATE = HERE / "CONTROL_EXECUTION_GATE_V004R3.json"
CONTROL_GATE = HERE / "CONTROL_GATE_V004R3.json"
L10_EXECUTION_GATE = HERE / "L10_EXECUTION_GATE_V004R3.json"
L10_GATE = HERE / "L10_GATE_V004R3.json"
L12_EXECUTION_GATE = HERE / "L12_EXECUTION_GATE_V004R3.json"
PARALLEL_L12_GATE = HERE / "PARALLEL_L12_EXECUTION_GATE_V004R3.json"
PARALLEL_L12_TELEMETRY = HERE / "PARALLEL_L12_TELEMETRY_V004R3.json"
CONTROL_COMPARISON = HERE / "CONTROL_COMPARISON_V004R3.json"
L10_COMPARISON = HERE / "L10_COMPARISON_V004R3.json"

SUPPORTED = r2.SUPPORTED
CONTROL_LENGTHS = r2.CONTROL_LENGTHS
WALL_LIMIT = r2.WALL_LIMIT
RSS_LIMIT = r2.RSS_LIMIT
SCRATCH_LIMIT = r2.SCRATCH_LIMIT
NUMERICAL_WORKSPACE_LIMIT = r2.NUMERICAL_WORKSPACE_LIMIT
IO_WINDOW_LIMIT = r2.IO_WINDOW_LIMIT
OVERHEAD_RESERVE = r2.OVERHEAD_RESERVE
FROZEN_STORAGE = r2.FROZEN_STORAGE
OBSTRUCTION_ROWS = r2.OBSTRUCTION_ROWS

R2_CUSTODY = {
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004R2.json":
        "01da8655d4c86c39a7e6a8dd8d938dea7699424b396cc4bb0e4a4fcc48b45e11",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R2_CACHE_PREFLIGHT_RESULT.json":
        "9377eae8e1a0732ff97e5e6f8b1d8705802cc9ea87799aa4cc6088cf6d9142f3",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R2_STORAGE_ONLY_CACHE_METHOD.md":
        "407da1e97c9c749a0a9d002e89d4fd8231fbbd161545c160601bacdc6e61dc33",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/v004r2_common.py":
        "e39529a2008018a1ede1b6f2deaef50e5843d489c8decd30163d60b408630689",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/build_hostile_v004r2_cache.py":
        "d1dec7a125e809501b642eb78c909d8549f830645992062214231e929f642541",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v004r2.py":
        "e0e6d858711ce568ff973ff325a4a13f4dc9f7d35664157df4aadfb2247fdf87",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/validate_v004r2_cache_preflight.py":
        "ec227545993881afb1937315ce91d5f76dc7aa934ad79477edbf0117e5d35a04",
}

FREEZE_FILES = {
    "method": METHOD, "common": Path(__file__).resolve(), "builder": BUILDER,
    "consumer": CONSUMER, "preflight": PREFLIGHT,
}

HARD_LOCKS = {
    "dual_obstruction_gate": DUAL_GATE.name,
    "control_execution_gate": CONTROL_EXECUTION_GATE.name,
    "control_pass_gate": CONTROL_GATE.name,
    "L10_execution_gate": L10_EXECUTION_GATE.name,
    "L10_pass_gate": L10_GATE.name,
    "L12_execution_gate": L12_EXECUTION_GATE.name,
    "parallel_L12_execution_gate": PARALLEL_L12_GATE.name,
}

PARALLEL_L12_CERTIFICATE = {
    "execution_mode": "CONTEMPORANEOUS_TARGET_V005_AND_HOSTILE_V004R3_AFTER_BOTH_L10_PASS",
    "per_process_rss_limit_bytes": 17_179_869_184,
    "target_mapped_peak_bytes": 252_944_080,
    "hostile_mapped_peak_bytes": 252_944_080,
    "combined_conservative_rss_plus_mapped_peak_bytes": 34_865_626_528,
    "nominal_host_memory_bytes": 48_000_000_000,
    "nominal_remaining_bytes": 13_134_373_472,
    "nominal_remaining_gib": 12.232338517904282,
    "target_disk_minimum_bytes": 9_600_951_508,
    "hostile_disk_minimum_bytes": 9_600_935_128,
    "combined_disk_minimum_bytes": 19_201_886_636,
    "observed_free_disk_floor_bytes": 44_735_000_000,
    "telemetry_path": str(PARALLEL_L12_TELEMETRY),
    "telemetry_required_fields": ["schema", "classification", "launch_epoch_by_role",
                                  "completion_epoch_by_role", "peak_rss_bytes_by_role",
                                  "peak_mapped_bytes_by_role", "free_disk_bytes_samples",
                                  "wall_seconds_by_role", "exit_code_by_role", "output_sha256_by_role"],
}

CLAIM_BOUNDARY = "V004R3_STORAGE_AND_STRICT_STAGED_GATE_SUCCESSOR_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"


class Refusal(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_keys(value: Any, keys: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise Refusal(f"{label} exact key census failed")


def cache_root(length: int) -> Path:
    return CACHE_PARENT / f"L{length}"


def history_output(length: int) -> Path:
    return HISTORY_PARENT / f"HOSTILE_V004R3_L{length}.json"


def workspace_root(length: int) -> Path:
    return WORKSPACE_PARENT / f"L{length}"


def existing_ancestor(path: Path) -> Path:
    cursor = path
    while not cursor.exists():
        cursor = cursor.parent
    return cursor


def require_canonical(path: Path, expected: Path, label: str) -> None:
    if path != expected or path.is_symlink() or existing_ancestor(path).resolve() != existing_ancestor(expected).resolve():
        raise Refusal(f"{label} is not canonical packet-local path")


def safe_repo_file(relative: str, expected_hash: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise Refusal("unsafe repository path")
    cursor = REPO
    for part in rel.parts:
        cursor = cursor / part
        info = cursor.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise Refusal("symlink in repository custody path")
    if not stat.S_ISREG(cursor.stat().st_mode) or sha256(cursor) != expected_hash:
        raise Refusal("repository custody hash/type mismatch")
    return cursor


def expected_specs(length: int) -> list[dict[str, Any]]:
    return r2.expected_specs(length)


def calculated_storage(length: int) -> dict[str, int]:
    return r2.calculated_storage(length)


def validate_manifest_record_census(manifest: dict[str, Any], length: int) -> None:
    try:
        r2.validate_manifest_record_census(manifest, length)
    except r2.Refusal as error:
        raise Refusal(str(error)) from error


def validate_freeze() -> dict[str, Any]:
    if FREEZE.is_symlink() or not FREEZE.is_file():
        raise Refusal("V004R3 freeze absent/nonordinary")
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    exact_keys(freeze, {"schema", "status", "supersedes_v004r2", "files", "sealed_v004r2_custody",
                        "hard_locks", "storage_census", "resource_limits", "parallel_L12_certificate", "canonical_paths",
                        "preserved", "cache_payload_created", "physical_history_executed",
                        "claim_boundary"}, "V004R3 freeze")
    if freeze["schema"] != "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R3" or freeze["status"] != "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT":
        raise Refusal("V004R3 freeze identity failed")
    if freeze["supersedes_v004r2"] != {
        "freeze_sha256": R2_CUSTODY["AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004R2.json"],
        "preflight_sha256": R2_CUSTODY["AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R2_CACHE_PREFLIGHT_RESULT.json"],
        "classification": "SUPERSEDED_AFTER_INDEPENDENT_HOSTILE_STAGED_GATE_FAIL__ALL_BYTES_PRESERVED",
        "blocking_proof": "SYNTHETIC_PARTIAL_HISTORY_ACCEPTED_BY_V004R2_VERIFY_OUTPUT_BINDING",
    }:
        raise Refusal("V004R2 supersession custody mismatch")
    exact_keys(freeze["files"], set(FREEZE_FILES), "V004R3 file roles")
    for role, path in FREEZE_FILES.items():
        if sha256(path) != freeze["files"][role]:
            raise Refusal(f"V004R3 frozen file mismatch: {role}")
    if freeze["sealed_v004r2_custody"] != R2_CUSTODY:
        raise Refusal("V004R2 frozen byte census mismatch")
    for relative, digest in R2_CUSTODY.items():
        safe_repo_file(relative, digest)
    r2.validate_freeze()
    r2_result = json.loads((HERE / "V004R2_CACHE_PREFLIGHT_RESULT.json").read_text(encoding="utf-8"))
    if not (r2_result.get("classification", "").startswith("PASS_V004R2_NONPHYSICAL_PREFLIGHT")
            and r2_result.get("checks_passed") == r2_result.get("checks_total") == 131_327):
        raise Refusal("V004R2 preflight custody mismatch")
    if freeze["hard_locks"] != HARD_LOCKS or freeze["storage_census"] != FROZEN_STORAGE:
        raise Refusal("V004R3 gate/storage census mismatch")
    for length in SUPPORTED:
        if calculated_storage(length) != FROZEN_STORAGE[str(length)]:
            raise Refusal("V004R3 calculated storage mismatch")
    resources = {"logical_scratch_bytes": SCRATCH_LIMIT, "rss_bytes": RSS_LIMIT,
                 "wall_seconds": WALL_LIMIT, "numerical_workspace_bytes": NUMERICAL_WORKSPACE_LIMIT,
                 "io_window_bytes": IO_WINDOW_LIMIT, "filesystem_reserve_bytes": OVERHEAD_RESERVE}
    if freeze["resource_limits"] != resources:
        raise Refusal("V004R3 resources mismatch")
    if freeze["parallel_L12_certificate"] != PARALLEL_L12_CERTIFICATE:
        raise Refusal("V004R3 aggregate L12 certificate mismatch")
    if freeze["canonical_paths"] != {"cache_parent": str(CACHE_PARENT),
                                      "history_parent": str(HISTORY_PARENT),
                                      "workspace_parent": str(WORKSPACE_PARENT)}:
        raise Refusal("V004R3 canonical path census mismatch")
    if freeze["preserved"] != r2.PRESERVED_PHYSICS or freeze["claim_boundary"] != CLAIM_BOUNDARY:
        raise Refusal("V004R3 physics/claim preservation mismatch")
    if freeze["cache_payload_created"] is not False or freeze["physical_history_executed"] is not False:
        raise Refusal("V004R3 freeze falsely reports output")
    return freeze


def validate_dual_gate_data(gate: dict[str, Any]) -> None:
    freeze = validate_freeze()
    exact_keys(gate, {"schema", "classification", "authorized_lengths", "obstruction_records",
                      "preserved_workspace_disposition", "method_sha256", "common_sha256",
                      "builder_sha256", "consumer_sha256", "freeze_sha256", "claim_boundary"},
               "V004R3 dual gate")
    if gate["schema"] != "DUAL_SIX_HOUR_OBSTRUCTION_GATE_V004R3" or gate["classification"] != "AUTHORIZE_HOSTILE_V004R3_CACHE_AFTER_EXACT_DUAL_OBSTRUCTION" or gate["authorized_lengths"] != list(SUPPORTED):
        raise Refusal("V004R3 dual gate identity/lengths mismatch")
    rows = gate["obstruction_records"]
    if not isinstance(rows, list) or len(rows) != 2 or [row.get("role") for row in rows if isinstance(row, dict)] != ["target", "hostile"]:
        raise Refusal("V004R3 exact ordered obstruction roles absent")
    paths = [OBSTRUCTION_ROWS[role][key] for role in ("target", "hostile")
             for key in ("obstruction_path", "log_path", "monitor_path")]
    hashes = [OBSTRUCTION_ROWS[role][key] for role in ("target", "hostile")
              for key in ("obstruction_sha256", "log_sha256", "monitor_sha256")]
    if len(set(paths)) != 6 or len(set(hashes)) != 6:
        raise Refusal("V004R3 obstruction evidence distinctness failed")
    for row, role in zip(rows, ("target", "hostile")):
        try:
            r2._validate_obstruction(role, row)
        except r2.Refusal as error:
            raise Refusal(str(error)) from error
    if gate["preserved_workspace_disposition"] != "EVIDENCE_ONLY__DO_NOT_CONSUME_OR_MUTATE__FULL_CACHED_RERUN_ONLY":
        raise Refusal("V004R3 preserved-workspace disposition mismatch")
    expected = {"method_sha256": freeze["files"]["method"], "common_sha256": freeze["files"]["common"],
                "builder_sha256": freeze["files"]["builder"], "consumer_sha256": freeze["files"]["consumer"],
                "freeze_sha256": sha256(FREEZE)}
    if any(gate[key] != value for key, value in expected.items()):
        raise Refusal("V004R3 dual gate frozen hash mismatch")
    if gate["claim_boundary"] != "RESOURCE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT":
        raise Refusal("V004R3 dual gate claim mismatch")


def valid_dual_gate_template() -> dict[str, Any]:
    freeze = validate_freeze()
    return {
        "schema": "DUAL_SIX_HOUR_OBSTRUCTION_GATE_V004R3",
        "classification": "AUTHORIZE_HOSTILE_V004R3_CACHE_AFTER_EXACT_DUAL_OBSTRUCTION",
        "authorized_lengths": list(SUPPORTED),
        "obstruction_records": [{"role": role, "path": OBSTRUCTION_ROWS[role]["obstruction_path"],
                                  "sha256": OBSTRUCTION_ROWS[role]["obstruction_sha256"]}
                                 for role in ("target", "hostile")],
        "preserved_workspace_disposition": "EVIDENCE_ONLY__DO_NOT_CONSUME_OR_MUTATE__FULL_CACHED_RERUN_ONLY",
        "method_sha256": freeze["files"]["method"], "common_sha256": freeze["files"]["common"],
        "builder_sha256": freeze["files"]["builder"], "consumer_sha256": freeze["files"]["consumer"],
        "freeze_sha256": sha256(FREEZE),
        "claim_boundary": "RESOURCE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT",
    }


def require_dual_gate(length: int) -> tuple[dict[str, Any], str]:
    if length not in SUPPORTED or DUAL_GATE.is_symlink() or not DUAL_GATE.is_file():
        raise Refusal("V004R3 cache/history locked: canonical dual gate absent")
    gate = json.loads(DUAL_GATE.read_text(encoding="utf-8"))
    validate_dual_gate_data(gate)
    if length not in gate["authorized_lengths"]:
        raise Refusal("V004R3 dual gate length mismatch")
    return gate, sha256(DUAL_GATE)
