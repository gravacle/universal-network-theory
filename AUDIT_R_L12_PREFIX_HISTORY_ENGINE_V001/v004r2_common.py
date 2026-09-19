#!/usr/bin/env python3
"""Frozen custody, census, and gate primitives for hostile V004R2.

This module is deliberately non-physical.  It authenticates immutable inputs,
future authorization records, canonical packet-local paths, and exact storage
censuses.  It never creates a cache, history, or workspace.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import stat
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
FREEZE = HERE / "FROZEN_MANIFEST_V004R2.json"
METHOD = HERE / "V004R2_STORAGE_ONLY_CACHE_METHOD.md"
BUILDER = HERE / "build_hostile_v004r2_cache.py"
CONSUMER = HERE / "independent_prefix_history_v004r2.py"
PREFLIGHT = HERE / "validate_v004r2_cache_preflight.py"

CACHE_PARENT = HERE / "V004R2_CACHE_PAYLOADS"
HISTORY_PARENT = HERE / "V004R2_HISTORY_OUTPUTS"
WORKSPACE_PARENT = HERE / "V004R2_WORKSPACES"
DUAL_GATE = HERE / "DUAL_SIX_HOUR_OBSTRUCTION_GATE_V004R2.json"
CONTROL_EXECUTION_GATE = HERE / "CONTROL_EXECUTION_GATE_V004R2.json"
CONTROL_GATE = HERE / "CONTROL_GATE_V004R2.json"
L10_EXECUTION_GATE = HERE / "L10_EXECUTION_GATE_V004R2.json"
L10_GATE = HERE / "L10_GATE_V004R2.json"
L12_EXECUTION_GATE = HERE / "L12_EXECUTION_GATE_V004R2.json"

SUPPORTED = (4, 6, 8, 10, 12)
CONTROL_LENGTHS = (4, 6, 8)
WALL_LIMIT = 21_600
RSS_LIMIT = 16 * 2**30
SCRATCH_LIMIT = 20 * 2**30
NUMERICAL_WORKSPACE_LIMIT = 1_400_000_000
IO_WINDOW_LIMIT = 512 * 2**20
OVERHEAD_RESERVE = 2**20

FREEZE_FILE_PATHS = {
    "method": METHOD,
    "common": Path(__file__).resolve(),
    "builder": BUILDER,
    "consumer": CONSUMER,
    "preflight": PREFLIGHT,
}

SEALED_DEPENDENCIES = {
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history.py":
        "6ea113e5bb25f1c4b00c2ee186b253ce5eb0551773f90e25bdbb52ed1c636af5",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py":
        "e6b1be915a4d490939799e79efc017ab4e3808f1beeb3d984448b2508fb0522b",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v003.py":
        "cc4e1195283f60fddab1d70831965bd14a09435fd4aca2ee7fdde7e2d7e5ba7f",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v004.py":
        "2ca121861820f3bae1d3cc62c2bcf071d22af730dd92c96a6cd0852f2f577d3e",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V003.json":
        "99ef9fca46e7baaa11b6700279a35ff936db3175ca56ea78b936c074dfe3845d",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V003_L12_EXECUTABLE_METHOD.md":
        "32a6f397c586328c07fdefc1aae0b4bb8e98de7783386c209104a68d577b418a",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py":
        "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md":
        "864113577059c5214923d4d1709e0d2a4483131f816b42bc43f7fc14a72b19ef",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_METHOD_V004.json":
        "d98f994572a2830746bbb305bfa0146f417662abebc2bf5861e48c05071e90d2",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json":
        "629ab8bc8e3c2a70c8e79a788ddeb6bafd3503491cef3b331bcc97a1555c2359",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CUSTODY_V002.json":
        "1d9a11359f0ba5298520ff51354badef4173dd070e829652d026b6317007aeb6",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_V001.json":
        "9dfaefcb6db713e03ea0774bb6a044774c0fed9a07aee48be12058e366291000",
}

OBSTRUCTION_ROWS = {
    "target": {
        "obstruction_path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_OBSTRUCTION.json",
        "obstruction_sha256": "9cfd793ded33b561c10ff7c93b8ffcb9cfe272f4efe7966fe8fd6c53413aeb62",
        "log_path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_EXECUTION_LOG.md",
        "log_sha256": "455359f7092acf93845f5494b40215e6264d9123fcc019be5b030f2adc7b79aa",
        "monitor_path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_WALL_MONITOR.json",
        "monitor_sha256": "b0882a97540d822ec96c093c1571d069f379f370a915c33fe213b18d7c118b6d",
        "implementation_sha256": "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7",
        "method_sha256": "864113577059c5214923d4d1709e0d2a4483131f816b42bc43f7fc14a72b19ef",
        "freeze_sha256": "d98f994572a2830746bbb305bfa0146f417662abebc2bf5861e48c05071e90d2",
        "workspace": "/private/tmp/wacf_target_v004_l12",
    },
    "hostile": {
        "obstruction_path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_OBSTRUCTION.json",
        "obstruction_sha256": "9281e055ea3bf8564960e303a2fa84feb99960c028bc0adc75bc2be7ba0a3aac",
        "log_path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_EXECUTION_LOG.md",
        "log_sha256": "9db56f21e55bbf800a07248a6ab67845cf6e5b0648c737d91ea19ac25d9d4c4a",
        "monitor_path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_WALL_MONITOR.json",
        "monitor_sha256": "13ebfe63f7b5b6103b51c3ec2b5a062342c73adc18f77738518834bd04a873c3",
        "implementation_sha256": "cc4e1195283f60fddab1d70831965bd14a09435fd4aca2ee7fdde7e2d7e5ba7f",
        "method_sha256": "32a6f397c586328c07fdefc1aae0b4bb8e98de7783386c209104a68d577b418a",
        "freeze_sha256": "99ef9fca46e7baaa11b6700279a35ff936db3175ca56ea78b936c074dfe3845d",
        "workspace": "/private/tmp/wacf_hostile_v003_l12",
    },
}

FROZEN_STORAGE = {
    "4": {"raw_cache_bytes_excluding_offsets": 5_556, "offset_bytes": 520,
          "actual_cache_array_bytes": 6_076, "maximum_live_state_bytes": 3_360,
          "state_plus_actual_cache_bytes": 9_436, "array_file_count": 50},
    "6": {"raw_cache_bytes_excluding_offsets": 117_344, "offset_bytes": 1_064,
          "actual_cache_array_bytes": 118_408, "maximum_live_state_bytes": 128_128,
          "state_plus_actual_cache_bytes": 246_536, "array_file_count": 98},
    "8": {"raw_cache_bytes_excluding_offsets": 2_331_620, "offset_bytes": 1_800,
          "actual_cache_array_bytes": 2_333_420, "maximum_live_state_bytes": 5_116_320,
          "state_plus_actual_cache_bytes": 7_449_740, "array_file_count": 162},
    "10": {"raw_cache_bytes_excluding_offsets": 44_506_128, "offset_bytes": 2_728,
           "actual_cache_array_bytes": 44_508_856, "maximum_live_state_bytes": 209_969_760,
           "state_plus_actual_cache_bytes": 254_478_616, "array_file_count": 242},
    "12": {"raw_cache_bytes_excluding_offsets": 826_218_064, "offset_bytes": 3_848,
           "actual_cache_array_bytes": 826_221_912, "maximum_live_state_bytes": 8_773_664_640,
           "state_plus_actual_cache_bytes": 9_599_886_552, "array_file_count": 338,
           "state_cache_plus_reserve_bytes": 9_600_935_128,
           "maximum_q12_cache_plus_admission_bytes": 224_797_960,
           "terminal_mapping_bytes": 234_782_536,
           "authentication_peak_bytes": 252_944_080},
}

HARD_LOCKS = {
    "dual_obstruction_gate": DUAL_GATE.name,
    "control_execution_gate": CONTROL_EXECUTION_GATE.name,
    "control_pass_gate": CONTROL_GATE.name,
    "L10_execution_gate": L10_EXECUTION_GATE.name,
    "L10_pass_gate": L10_GATE.name,
    "L12_execution_gate": L12_EXECUTION_GATE.name,
}

PRESERVED_PHYSICS = {
    "basis_order": "REVERSED_COMBINATION__FULL_MASK",
    "lineage_identity": "FULL_CANONICAL_MASK",
    "hostile_edge_order": "FROZEN_HOSTILE_EDGE_ORDER",
    "hamiltonian_exchange_coefficient": -1,
    "current_orientation": "UNCHANGED_V003",
    "allow_require_semantics": "UNCHANGED_V003",
    "owner_once_admission": True,
    "terminal_children_streamed": True,
    "rough_sharp_numerics_changed": False,
    "physics_or_observable_changed": False,
}

CLAIM_BOUNDARY = "STORAGE_SUCCESSOR_AND_NONPHYSICAL_PREFLIGHT_ONLY__NO_CACHE_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"


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
    return HISTORY_PARENT / f"HOSTILE_V004R2_L{length}.json"


def workspace_root(length: int) -> Path:
    return WORKSPACE_PARENT / f"L{length}"


def _existing_ancestor(path: Path) -> Path:
    candidate = path
    while not candidate.exists():
        candidate = candidate.parent
    return candidate


def require_canonical(path: Path, expected: Path, label: str) -> None:
    if path != expected or path.is_symlink() or _existing_ancestor(path).resolve() != _existing_ancestor(expected).resolve():
        raise Refusal(f"{label} is not the canonical packet-local path")


def safe_repo_file(relative: str, expected_hash: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise Refusal("unsafe repository-relative custody path")
    cursor = REPO
    for part in rel.parts:
        cursor = cursor / part
        info = cursor.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise Refusal("symlink in repository custody path")
    if not stat.S_ISREG(cursor.stat().st_mode) or sha256(cursor) != expected_hash:
        raise Refusal("repository custody file hash/type mismatch")
    return cursor


def expected_specs(length: int) -> list[dict[str, Any]]:
    if length not in SUPPORTED:
        raise Refusal("unsupported cache length")
    specs: list[dict[str, Any]] = []
    edge_count = 3 * length
    for q in range(length + 1):
        words = math.comb(2 * length, q)
        pairs = edge_count * (math.comb(2 * length - 2, q - 1) if q else 0)
        specs.extend([
            {"path": f"q_{q:02d}_words.u32", "dtype": "<u4", "shape": [words],
             "bytes": 4 * words, "kind": "operator", "q": q, "role": "words"},
            {"path": f"q_{q:02d}_offsets.u64", "dtype": "<u8", "shape": [edge_count + 1],
             "bytes": 8 * (edge_count + 1), "kind": "operator", "q": q, "role": "offsets"},
        ])
        if q:
            specs.extend([
                {"path": f"q_{q:02d}_sources.i32", "dtype": "<i4", "shape": [pairs],
                 "bytes": 4 * pairs, "kind": "operator", "q": q, "role": "sources"},
                {"path": f"q_{q:02d}_targets.i32", "dtype": "<i4", "shape": [pairs],
                 "bytes": 4 * pairs, "kind": "operator", "q": q, "role": "targets"},
            ])
    for event in range(length):
        for q in range(1, event + 2):
            count = math.comb(2 * length - 1, q - 1)
            for role in ("occupied", "old"):
                specs.append({
                    "path": f"event_{event:02d}_q_{q:02d}_{role}.i32", "dtype": "<i4",
                    "shape": [count], "bytes": 4 * count, "kind": "admission",
                    "event": event, "q": q, "role": role,
                })
    for event in range(length - 1):
        for q in range(event + 1):
            count = math.comb(event, q)
            for role in ("same", "added"):
                specs.append({
                    "path": f"prefix_{event:02d}_q_{q:02d}_{role}.i32", "dtype": "<i4",
                    "shape": [count], "bytes": 4 * count, "kind": "lineage",
                    "event": event, "q": q, "role": role,
                })
    return specs


def calculated_storage(length: int) -> dict[str, int]:
    specs = expected_specs(length)
    offsets = sum(row["bytes"] for row in specs if row["role"] == "offsets")
    actual = sum(row["bytes"] for row in specs)
    raw = actual - offsets
    dims = [sum(math.comb(prefix, q) * math.comb(2 * length, q)
                for q in range(prefix + 1)) for prefix in range(length)]
    state = 16 * (max(dims[i] + dims[i + 1] for i in range(length - 1)) if length > 1 else dims[0])
    result = {
        "raw_cache_bytes_excluding_offsets": raw,
        "offset_bytes": offsets,
        "actual_cache_array_bytes": actual,
        "maximum_live_state_bytes": state,
        "state_plus_actual_cache_bytes": state + actual,
        "array_file_count": len(specs),
    }
    if length == 12:
        result.update({
            "state_cache_plus_reserve_bytes": state + actual + OVERHEAD_RESERVE,
            "maximum_q12_cache_plus_admission_bytes": 224_797_960,
            "terminal_mapping_bytes": 234_782_536,
            "authentication_peak_bytes": 252_944_080,
        })
    return result


def validate_manifest_record_census(manifest: dict[str, Any], length: int) -> None:
    """Pure exact-census check used by both the consumer and adversarial preflight."""
    specs = expected_specs(length)
    records = manifest.get("files")
    if not isinstance(records, list) or len(records) != len(specs):
        raise Refusal("cache manifest record census failed")
    for record, spec in zip(records, specs):
        exact_keys(record, set(spec) | {"sha256"}, f"cache record {spec['path']}")
        if ({key: record[key] for key in spec} != spec
                or not isinstance(record["sha256"], str) or len(record["sha256"]) != 64
                or any(character not in "0123456789abcdef" for character in record["sha256"])):
            raise Refusal(f"cache record metadata/hash mismatch: {spec['path']}")
    storage = FROZEN_STORAGE[str(length)]
    if (manifest.get("array_file_count") != len(specs)
            or manifest.get("manifest_inclusive_file_count") != len(specs) + 1
            or manifest.get("payload") != storage
            or sum(row["bytes"] for row in records) != storage["actual_cache_array_bytes"]):
        raise Refusal("cache manifest exact totals mismatch")


def validate_freeze() -> dict[str, Any]:
    if FREEZE.is_symlink() or not FREEZE.is_file():
        raise Refusal("V004R2 freeze absent or non-ordinary")
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    exact_keys(freeze, {
        "schema", "status", "supersedes_failed_freeze", "files", "sealed_dependencies",
        "dual_obstruction_custody", "preserved_workspace_custody", "hard_locks",
        "storage_census", "resource_limits", "canonical_paths", "preserved",
        "cache_payload_created", "physical_history_executed", "claim_boundary",
    }, "freeze")
    if freeze["schema"] != "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R2" or freeze["status"] != "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT":
        raise Refusal("V004R2 freeze identity failed")
    if freeze["supersedes_failed_freeze"] != {
        "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004.json",
        "sha256": "16c6ce3e2b8af7b5ef83b099dafe2fd0653490fb040cbe812bc827e669f72718",
        "preflight_path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004_CACHE_PREFLIGHT_RESULT.json",
        "preflight_sha256": "e07e1d4cdba7906d5e741af6ae8c27751092150b76241d07abd34c16d7874005",
        "classification": "SUPERSEDED_AFTER_INDEPENDENT_HOSTILE_FAIL__BYTES_PRESERVED",
    }:
        raise Refusal("failed V004 supersession custody mismatch")
    exact_keys(freeze["files"], set(FREEZE_FILE_PATHS), "freeze file roles")
    for role, path in FREEZE_FILE_PATHS.items():
        if sha256(path) != freeze["files"][role]:
            raise Refusal(f"frozen successor file mismatch: {role}")
    if freeze["sealed_dependencies"] != SEALED_DEPENDENCIES:
        raise Refusal("sealed dependency census/pins mismatch")
    for relative, expected in SEALED_DEPENDENCIES.items():
        safe_repo_file(relative, expected)
    if freeze["dual_obstruction_custody"] != OBSTRUCTION_ROWS:
        raise Refusal("frozen obstruction custody mismatch")
    if freeze["preserved_workspace_custody"] != {
        "structural_observation": {
            "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CUSTODY_V002.json",
            "sha256": "1d9a11359f0ba5298520ff51354badef4173dd070e829652d026b6317007aeb6",
            "checks": "48/48"},
        "cross_diagnostic": {
            "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_V001.json",
            "sha256": "9dfaefcb6db713e03ea0774bb6a044774c0fed9a07aee48be12058e366291000",
            "disposition": "Q11_MISMATCH_4.826848E-5__NOT_RESTART_OR_EQUIVALENCE_INPUT"},
        "use": "EVIDENCE_ONLY__DO_NOT_CONSUME_OR_MUTATE__FULL_CACHED_RERUN_ONLY",
    }:
        raise Refusal("preserved workspace custody binding mismatch")
    if freeze["hard_locks"] != HARD_LOCKS or freeze["storage_census"] != FROZEN_STORAGE:
        raise Refusal("hard-lock or exact storage census mismatch")
    if freeze["preserved"] != PRESERVED_PHYSICS or freeze["claim_boundary"] != CLAIM_BOUNDARY:
        raise Refusal("preserved physics or claim boundary mismatch")
    for length in SUPPORTED:
        if calculated_storage(length) != FROZEN_STORAGE[str(length)]:
            raise Refusal(f"calculated storage census mismatch at L={length}")
    resources = {
        "logical_scratch_bytes": SCRATCH_LIMIT, "rss_bytes": RSS_LIMIT,
        "wall_seconds": WALL_LIMIT, "numerical_workspace_bytes": NUMERICAL_WORKSPACE_LIMIT,
        "io_window_bytes": IO_WINDOW_LIMIT, "filesystem_reserve_bytes": OVERHEAD_RESERVE,
    }
    if freeze["resource_limits"] != resources:
        raise Refusal("resource limit census mismatch")
    paths = {
        "cache_parent": str(CACHE_PARENT), "history_parent": str(HISTORY_PARENT),
        "workspace_parent": str(WORKSPACE_PARENT),
    }
    if freeze["canonical_paths"] != paths:
        raise Refusal("canonical path freeze mismatch")
    if freeze["cache_payload_created"] is not False or freeze["physical_history_executed"] is not False:
        raise Refusal("freeze falsely reports output")
    return freeze


def _validate_obstruction(role: str, row: dict[str, Any]) -> None:
    expected = OBSTRUCTION_ROWS[role]
    if row != {"role": role, "path": expected["obstruction_path"],
               "sha256": expected["obstruction_sha256"]}:
        raise Refusal(f"{role} obstruction gate row mismatch")
    path = safe_repo_file(expected["obstruction_path"], expected["obstruction_sha256"])
    record = json.loads(path.read_text(encoding="utf-8"))
    exact_keys(record, {"schema", "classification", "L", "role", "resolved",
                              "physical_output_created", "wall_limit_seconds", "wall_seconds",
                              "implementation_sha256", "method_sha256", "freeze_sha256",
                              "execution_log", "monitor_evidence", "workspace",
                              "workspace_preserved", "claim_boundary"}, f"{role} obstruction")
    required = {
        "schema": "L12_SIX_HOUR_RESOURCE_OBSTRUCTION_V005",
        "classification": "SIX_HOUR_RESOURCE_OBSTRUCTION", "L": 12, "role": role,
        "resolved": False, "physical_output_created": False,
        "wall_limit_seconds": WALL_LIMIT, "wall_seconds": 21_627,
        "implementation_sha256": expected["implementation_sha256"],
        "method_sha256": expected["method_sha256"], "freeze_sha256": expected["freeze_sha256"],
        "execution_log": {"path": expected["log_path"], "sha256": expected["log_sha256"]},
        "monitor_evidence": {"path": expected["monitor_path"], "sha256": expected["monitor_sha256"]},
        "workspace": expected["workspace"], "workspace_preserved": True,
        "claim_boundary": "RESOURCE_OBSTRUCTION_ONLY__NO_L12_HISTORY_OR_PHYSICS_RESULT",
    }
    if record != required:
        raise Refusal(f"{role} obstruction internal semantics mismatch")
    safe_repo_file(expected["log_path"], expected["log_sha256"])
    monitor_path = safe_repo_file(expected["monitor_path"], expected["monitor_sha256"])
    monitor = json.loads(monitor_path.read_text(encoding="utf-8"))
    exact_keys(monitor, {"schema", "L", "role", "implementation_sha256", "wall_limit_seconds",
                         "observed_wall_seconds", "launch_epoch", "termination_epoch",
                         "termination_reason", "physical_output_created", "workspace_preserved"},
               f"{role} monitor")
    if not (monitor["schema"] == "L12_WALL_MONITOR_EVIDENCE_V005" and monitor["L"] == 12
            and monitor["role"] == role and monitor["implementation_sha256"] == expected["implementation_sha256"]
            and monitor["wall_limit_seconds"] == WALL_LIMIT and monitor["observed_wall_seconds"] == 21_627
            and monitor["termination_epoch"] - monitor["launch_epoch"] == 21_627
            and monitor["termination_reason"] == "WALL_LIMIT_REACHED"
            and monitor["physical_output_created"] is False and monitor["workspace_preserved"] is True):
        raise Refusal(f"{role} wall monitor semantics mismatch")


def validate_dual_gate_data(gate: dict[str, Any]) -> None:
    freeze = validate_freeze()
    exact_keys(gate, {"schema", "classification", "authorized_lengths", "obstruction_records",
                      "preserved_workspace_custody", "method_sha256", "common_sha256",
                      "builder_sha256", "consumer_sha256", "freeze_sha256", "claim_boundary"},
               "dual gate")
    if gate["schema"] != "DUAL_SIX_HOUR_OBSTRUCTION_GATE_V004R2" or gate["classification"] != "AUTHORIZE_HOSTILE_V004R2_CACHE_AFTER_EXACT_DUAL_OBSTRUCTION":
        raise Refusal("dual gate identity failed")
    if gate["authorized_lengths"] != list(SUPPORTED):
        raise Refusal("dual gate length census mismatch")
    if not isinstance(gate["obstruction_records"], list) or len(gate["obstruction_records"]) != 2:
        raise Refusal("dual gate requires exactly two obstruction records")
    rows = {row.get("role"): row for row in gate["obstruction_records"] if isinstance(row, dict)}
    if set(rows) != {"target", "hostile"}:
        raise Refusal("dual gate role census mismatch")
    six_paths = [
        OBSTRUCTION_ROWS[role][name]
        for role in ("target", "hostile")
        for name in ("obstruction_path", "log_path", "monitor_path")
    ]
    if len(set(six_paths)) != 6:
        raise Refusal("dual obstruction six-path distinctness failed")
    for role in ("target", "hostile"):
        _validate_obstruction(role, rows[role])
    custody = {
        "structural_observation": {
            "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CUSTODY_V002.json",
            "sha256": SEALED_DEPENDENCIES["AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CUSTODY_V002.json"],
            "checks": "48/48"},
        "cross_diagnostic": {
            "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_V001.json",
            "sha256": SEALED_DEPENDENCIES["AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_V001.json"],
            "disposition": "Q11_MISMATCH_4.826848E-5__NOT_RESTART_OR_EQUIVALENCE_INPUT"},
        "use": "EVIDENCE_ONLY__DO_NOT_CONSUME_OR_MUTATE__FULL_CACHED_RERUN_ONLY",
    }
    if gate["preserved_workspace_custody"] != custody:
        raise Refusal("dual gate preserved-workspace custody mismatch")
    expected_hashes = {"method_sha256": freeze["files"]["method"],
                       "common_sha256": freeze["files"]["common"],
                       "builder_sha256": freeze["files"]["builder"],
                       "consumer_sha256": freeze["files"]["consumer"],
                       "freeze_sha256": sha256(FREEZE)}
    if any(gate[key] != value for key, value in expected_hashes.items()):
        raise Refusal("dual gate frozen successor hash mismatch")
    if gate["claim_boundary"] != "RESOURCE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT":
        raise Refusal("dual gate claim boundary mismatch")


def require_dual_gate(length: int) -> tuple[dict[str, Any], str]:
    if length not in SUPPORTED:
        raise Refusal("unsupported length")
    if DUAL_GATE.is_symlink() or not DUAL_GATE.is_file():
        raise Refusal("cache/history locked: canonical dual obstruction gate absent")
    gate = json.loads(DUAL_GATE.read_text(encoding="utf-8"))
    validate_dual_gate_data(gate)
    if length not in gate["authorized_lengths"]:
        raise Refusal("dual gate does not authorize length")
    return gate, sha256(DUAL_GATE)


def valid_dual_gate_template() -> dict[str, Any]:
    freeze = validate_freeze()
    return {
        "schema": "DUAL_SIX_HOUR_OBSTRUCTION_GATE_V004R2",
        "classification": "AUTHORIZE_HOSTILE_V004R2_CACHE_AFTER_EXACT_DUAL_OBSTRUCTION",
        "authorized_lengths": list(SUPPORTED),
        "obstruction_records": [
            {"role": role, "path": OBSTRUCTION_ROWS[role]["obstruction_path"],
             "sha256": OBSTRUCTION_ROWS[role]["obstruction_sha256"]}
            for role in ("target", "hostile")
        ],
        "preserved_workspace_custody": {
            "structural_observation": {
                "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CUSTODY_V002.json",
                "sha256": SEALED_DEPENDENCIES["AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CUSTODY_V002.json"],
                "checks": "48/48"},
            "cross_diagnostic": {
                "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_V001.json",
                "sha256": SEALED_DEPENDENCIES["AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_V001.json"],
                "disposition": "Q11_MISMATCH_4.826848E-5__NOT_RESTART_OR_EQUIVALENCE_INPUT"},
            "use": "EVIDENCE_ONLY__DO_NOT_CONSUME_OR_MUTATE__FULL_CACHED_RERUN_ONLY",
        },
        "method_sha256": freeze["files"]["method"], "common_sha256": freeze["files"]["common"],
        "builder_sha256": freeze["files"]["builder"], "consumer_sha256": freeze["files"]["consumer"],
        "freeze_sha256": sha256(FREEZE),
        "claim_boundary": "RESOURCE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT",
    }
