#!/usr/bin/env python3
"""Unfrozen V004R4 cross-branch audit/build/schedule contract draft.

Every function is validation-only.  Target V012 identities are intentionally
unbound, so this module cannot authorize construction or physical execution.
"""

from __future__ import annotations

import hashlib
import json
import math
import stat
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
R4_FREEZE = HERE / "FROZEN_MANIFEST_V004R4.json"
R4_AUDIT = HERE / "HOSTILE_AUDIT_RESULT_V004R4.json"
R4_PREFLIGHT_RESULT = HERE / "V004R4_CACHE_PREFLIGHT_RESULT.json"
R4_BUILD_GATE = HERE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
SHARED_DIR = REPO / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
SHARED_GATE = SHARED_DIR / "SHARED_AGGREGATE_SCHEDULE_GATE_V001.json"
SHARED_TELEMETRY = SHARED_DIR / "SHARED_AGGREGATE_TELEMETRY_V001.json"

TARGET_V012_DIR = REPO / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
TARGET_V012_AUDIT_DIR = REPO / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
TARGET_V012_FREEZE = TARGET_V012_DIR / "FREEZE.json"
TARGET_V012_AUDIT = TARGET_V012_AUDIT_DIR / "HOSTILE_AUDIT_RESULT_V001.json"
TARGET_V012_L10_GATE = TARGET_V012_DIR / "CACHED_L10_GATE_V012.json"
TARGET_V012_L12_CACHE_MANIFEST = TARGET_V012_DIR / "CACHE_PAYLOADS/L12/CACHE_MANIFEST.json"

HOSTILE_R4_L10_GATE = HERE / "CACHED_L10_GATE_V004R4.json"
HOSTILE_R4_L12_CACHE_MANIFEST = HERE / "V004R4_CACHE_PAYLOADS/L12/CACHE_MANIFEST.json"

TARGET_V012_INTERFACE = {
    "freeze_sha256": "UNBOUND_TARGET_V012_FREEZE_SHA256",
    "freeze_schema": "UNBOUND_TARGET_V012_FREEZE_SCHEMA",
    "audit_sha256": "UNBOUND_TARGET_V012_AUDIT_SHA256",
    "audit_schema": "UNBOUND_TARGET_V012_AUDIT_SCHEMA",
    "audit_classification": "UNBOUND_TARGET_V012_AUDIT_CLASSIFICATION",
    "consumer_sha256": "UNBOUND_TARGET_V012_CONSUMER_SHA256",
    "L10_gate_sha256": "UNBOUND_TARGET_V012_L10_GATE_SHA256",
    "L10_gate_schema": "UNBOUND_TARGET_V012_L10_GATE_SCHEMA",
    "L10_gate_classification": "UNBOUND_TARGET_V012_L10_GATE_CLASSIFICATION",
    "L12_cache_manifest_sha256": "UNBOUND_TARGET_V012_L12_CACHE_MANIFEST_SHA256",
    "L12_cache_manifest_schema": "UNBOUND_TARGET_V012_L12_CACHE_MANIFEST_SCHEMA",
}

AGGREGATE_CERTIFICATE = {
    "combined_conservative_rss_plus_mapped_peak_bytes": 34_865_626_528,
    "per_process_rss_limit_bytes": 17_179_869_184,
    "target_mapped_peak_bytes": 252_944_080,
    "hostile_mapped_peak_bytes": 252_944_080,
    "target_disk_minimum_bytes": 9_600_954_452,
    "hostile_disk_minimum_bytes": 9_600_935_128,
    "combined_disk_minimum_bytes": 19_201_889_580,
    "minimum_host_physical_memory_bytes": 48_000_000_000,
    "nominal_memory_margin_bytes": 13_134_373_472,
    "nominal_memory_margin_gib": 12.232338517904282,
}

TELEMETRY_FIELDS = [
    "schema", "classification", "shared_gate_sha256", "launch_epoch_by_role",
    "completion_epoch_by_role", "wall_seconds_by_role", "peak_rss_bytes_by_role",
    "peak_mapped_bytes_by_role", "free_disk_bytes_samples", "exit_code_by_role",
    "output_sha256_by_role",
]


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
        raise Refusal(f"{label} exact key census mismatch")


def positive_integer(value: Any) -> bool:
    return type(value) is int and value > 0


def finite_number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(float(value))


def assert_ready_for_freeze() -> None:
    unresolved = [key for key, value in TARGET_V012_INTERFACE.items()
                  if not isinstance(value, str) or value.startswith("UNBOUND_TARGET_V012_")]
    if unresolved:
        raise Refusal("V004R4 freeze forbidden until target V012 interface is bound: " + ",".join(unresolved))
    for path in (TARGET_V012_FREEZE, TARGET_V012_AUDIT, TARGET_V012_L10_GATE,
                 TARGET_V012_L12_CACHE_MANIFEST):
        if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o222:
            raise Refusal(f"target V012 immutable interface file absent: {path}")


def read_immutable(path: Path, expected_hash: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o222:
        raise Refusal(f"immutable record absent: {path}")
    if sha256(path) != expected_hash:
        raise Refusal(f"immutable record hash mismatch: {path}")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise Refusal(f"record is not an object: {path}")
    return record


def validate_target_v012_interface() -> dict[str, dict[str, Any]]:
    assert_ready_for_freeze()
    freeze = read_immutable(TARGET_V012_FREEZE, TARGET_V012_INTERFACE["freeze_sha256"])
    audit = read_immutable(TARGET_V012_AUDIT, TARGET_V012_INTERFACE["audit_sha256"])
    l10 = read_immutable(TARGET_V012_L10_GATE, TARGET_V012_INTERFACE["L10_gate_sha256"])
    cache = read_immutable(TARGET_V012_L12_CACHE_MANIFEST,
                           TARGET_V012_INTERFACE["L12_cache_manifest_sha256"])
    if freeze.get("schema") != TARGET_V012_INTERFACE["freeze_schema"]:
        raise Refusal("target V012 freeze schema mismatch")
    if not (audit.get("schema") == TARGET_V012_INTERFACE["audit_schema"]
            and audit.get("classification") == TARGET_V012_INTERFACE["audit_classification"]
            and positive_integer(audit.get("checks_total"))
            and audit.get("checks_passed") == audit.get("checks_total")
            and audit.get("failures") == []
            and audit.get("audited_freeze_sha256") == TARGET_V012_INTERFACE["freeze_sha256"]):
        raise Refusal("target V012 independent audit interface mismatch")
    if not (l10.get("schema") == TARGET_V012_INTERFACE["L10_gate_schema"]
            and l10.get("classification") == TARGET_V012_INTERFACE["L10_gate_classification"]
            and l10.get("consumer_sha256") == TARGET_V012_INTERFACE["consumer_sha256"]
            and l10.get("freeze_sha256") == TARGET_V012_INTERFACE["freeze_sha256"]):
        raise Refusal("target V012 cached L10 gate interface mismatch")
    if not (cache.get("schema") == TARGET_V012_INTERFACE["L12_cache_manifest_schema"]
            and cache.get("L") == 12
            and cache.get("consumer_sha256") == TARGET_V012_INTERFACE["consumer_sha256"]
            and cache.get("freeze_sha256") == TARGET_V012_INTERFACE["freeze_sha256"]):
        raise Refusal("target V012 L12 cache interface mismatch")
    return {"freeze": freeze, "audit": audit, "L10_gate": l10, "L12_cache_manifest": cache}


def validate_own_future_hostile_audit(record: dict[str, Any], freeze: dict[str, Any]) -> None:
    exact_keys(record, {"schema", "classification", "auditor_role", "audited_freeze_sha256",
                         "audited_files_sha256", "preflight_result_sha256",
                         "checks_passed", "checks_total", "failures",
                         "v004r3_bytes_preserved", "absence_census", "payload_or_history_executed",
                         "claim_boundary"}, "V004R4 hostile audit")
    if not (record["schema"] == "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001"
            and record["classification"] == "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE"
            and record["auditor_role"] == "INDEPENDENT_HOSTILE_READ_ONLY_REVIEW"
            and record["audited_freeze_sha256"] == sha256(R4_FREEZE)
            and record["audited_files_sha256"] == freeze["files"]
            and record["preflight_result_sha256"] == sha256(R4_PREFLIGHT_RESULT)
            and positive_integer(record["checks_total"])
            and record["checks_passed"] == record["checks_total"] and record["failures"] == []
            and record["v004r3_bytes_preserved"] is True
            and record["absence_census"] == {
                "build_gate": False, "shared_gate": False, "shared_telemetry": False,
                "cache_payloads": False, "postbuild_payload_audit": False,
                "workspaces": False, "histories": False}
            and record["payload_or_history_executed"] is False
            and record["claim_boundary"] == "NONPHYSICAL_V004R4_CONTROL_PLANE_AUDIT_ONLY"):
        raise Refusal("V004R4 hostile audit content/identity mismatch")


def validate_build_authorization_gate(gate: dict[str, Any], freeze: dict[str, Any]) -> None:
    exact_keys(gate, {"schema", "classification", "authorized_cache_lengths", "freeze_sha256",
                      "files_sha256", "independent_hostile_audit", "target_v012_interface",
                      "dual_obstruction_custody", "claim_boundary"}, "V004R4 build gate")
    audit_binding = gate["independent_hostile_audit"]
    exact_keys(audit_binding, {"path", "sha256", "schema", "classification", "checks_passed",
                               "checks_total"}, "V004R4 audit binding")
    if not (gate["schema"] == "HOSTILE_V004R4_CACHE_BUILD_AUTHORIZATION_GATE"
            and gate["classification"] == "AUTHORIZE_HOSTILE_V004R4_CACHE_AFTER_INDEPENDENT_AUDIT"
            and gate["authorized_cache_lengths"] == [4, 6, 8, 10, 12]
            and gate["freeze_sha256"] == sha256(R4_FREEZE) and gate["files_sha256"] == freeze["files"]
            and audit_binding["path"] == str(R4_AUDIT)
            and audit_binding["schema"] == "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001"
            and audit_binding["classification"] == "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE"
            and positive_integer(audit_binding["checks_total"])
            and audit_binding["checks_passed"] == audit_binding["checks_total"]
            and gate["target_v012_interface"] == TARGET_V012_INTERFACE
            and gate["claim_boundary"] == "CACHE_BUILD_AUTHORIZATION_ONLY__NO_HISTORY_OR_PHYSICS_RESULT"):
        raise Refusal("V004R4 build gate exact audit/interface binding mismatch")
    audit = read_immutable(R4_AUDIT, audit_binding["sha256"])
    validate_own_future_hostile_audit(audit, freeze)
    if audit["checks_passed"] != audit_binding["checks_passed"] or audit["checks_total"] != audit_binding["checks_total"]:
        raise Refusal("V004R4 build gate audit check count mismatch")
    validate_target_v012_interface()


def validate_branch_binding(binding: dict[str, Any], role: str, expected: dict[str, Any]) -> None:
    exact_keys(binding, {"role", "freeze", "independent_audit", "consumer_sha256",
                         "cached_L10_gate", "L12_cache_manifest"}, f"{role} branch binding")
    if binding["role"] != role or binding["consumer_sha256"] != expected["consumer_sha256"]:
        raise Refusal(f"{role} branch role/consumer mismatch")
    for key in ("freeze", "independent_audit", "cached_L10_gate", "L12_cache_manifest"):
        exact_keys(binding[key], {"path", "sha256", "schema", "identity_field", "identity_value"}, f"{role} {key}")
        if binding[key] != expected[key]:
            raise Refusal(f"{role} {key} exact binding mismatch")
        record = read_immutable(Path(binding[key]["path"]), binding[key]["sha256"])
        if (binding[key]["identity_field"] not in {"status", "classification"}
                or record.get("schema") != binding[key]["schema"]
                or record.get(binding[key]["identity_field"]) != binding[key]["identity_value"]):
            raise Refusal(f"{role} {key} internal identity mismatch")
    audit = read_immutable(Path(binding["independent_audit"]["path"]), binding["independent_audit"]["sha256"])
    if not positive_integer(audit.get("checks_total")) or audit.get("checks_passed") != audit.get("checks_total"):
        raise Refusal(f"{role} independent audit is not a positive all-pass result")
    l10 = read_immutable(Path(binding["cached_L10_gate"]["path"]), binding["cached_L10_gate"]["sha256"])
    cache = read_immutable(Path(binding["L12_cache_manifest"]["path"]), binding["L12_cache_manifest"]["sha256"])
    if l10.get("freeze_sha256") != binding["freeze"]["sha256"] or l10.get("consumer_sha256") != binding["consumer_sha256"]:
        raise Refusal(f"{role} L10 lineage mismatch")
    if cache.get("L") != 12 or cache.get("freeze_sha256") != binding["freeze"]["sha256"] or cache.get("consumer_sha256") != binding["consumer_sha256"]:
        raise Refusal(f"{role} L12 cache lineage mismatch")


def validate_shared_aggregate_gate(gate: dict[str, Any], target_expected: dict[str, Any],
                                   hostile_expected: dict[str, Any], now_epoch: int | None = None) -> None:
    exact_keys(gate, {"schema", "classification", "created_epoch", "expires_epoch", "branches",
                      "resource_certificate", "resource_snapshot", "schedule", "telemetry",
                      "claim_boundary"}, "shared aggregate gate")
    if gate["schema"] != "SHARED_TARGET_V012_HOSTILE_V004R4_AGGREGATE_SCHEDULE_GATE_V001" or gate["classification"] != "AUTHORIZE_CONTEMPORANEOUS_L12_AFTER_BOTH_CACHED_L10_PASS":
        raise Refusal("shared aggregate gate identity mismatch")
    exact_keys(gate["branches"], {"target_v012", "hostile_v004r4"}, "shared branches")
    validate_branch_binding(gate["branches"]["target_v012"], "target_v012", target_expected)
    validate_branch_binding(gate["branches"]["hostile_v004r4"], "hostile_v004r4", hostile_expected)
    if gate["resource_certificate"] != AGGREGATE_CERTIFICATE:
        raise Refusal("shared aggregate resource certificate mismatch")
    snapshot = gate["resource_snapshot"]
    exact_keys(snapshot, {"captured_epoch", "host_physical_memory_bytes", "available_memory_bytes",
                          "workspace_free_disk_bytes", "workspace_filesystem_device",
                          "both_workspace_roots_same_filesystem", "passes"}, "shared resource snapshot")
    if not (positive_integer(snapshot["captured_epoch"])
            and positive_integer(snapshot["host_physical_memory_bytes"])
            and snapshot["host_physical_memory_bytes"] >= AGGREGATE_CERTIFICATE["minimum_host_physical_memory_bytes"]
            and positive_integer(snapshot["available_memory_bytes"])
            and snapshot["available_memory_bytes"] >= AGGREGATE_CERTIFICATE["combined_conservative_rss_plus_mapped_peak_bytes"]
            and positive_integer(snapshot["workspace_free_disk_bytes"])
            and snapshot["workspace_free_disk_bytes"] >= AGGREGATE_CERTIFICATE["combined_disk_minimum_bytes"]
            and positive_integer(snapshot["workspace_filesystem_device"])
            and snapshot["both_workspace_roots_same_filesystem"] is True and snapshot["passes"] is True):
        raise Refusal("shared current RAM/disk snapshot insufficient")
    created, expires = gate["created_epoch"], gate["expires_epoch"]
    if not (positive_integer(created) and positive_integer(expires) and created <= snapshot["captured_epoch"] <= expires
            and 0 < expires - created <= 900):
        raise Refusal("shared gate freshness window mismatch")
    if now_epoch is not None and not (created <= now_epoch <= expires):
        raise Refusal("shared gate expired/not-yet-valid")
    if gate["schedule"] != {"launch_mode": "CONTEMPORANEOUS_TWO_PROCESS",
                             "launch_only_after_both_cached_L10_pass": True,
                             "launch_skew_seconds_max": 60,
                             "per_process_rss_limit_bytes": 17_179_869_184,
                             "per_process_wall_limit_seconds": 21_600}:
        raise Refusal("shared schedule mismatch")
    if gate["telemetry"] != {"path": str(SHARED_TELEMETRY),
                              "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
                              "required_fields": TELEMETRY_FIELDS,
                              "must_be_absent_before_launch": True,
                              "sample_interval_seconds_max": 60}:
        raise Refusal("shared telemetry interface mismatch")
    if SHARED_TELEMETRY.exists():
        raise Refusal("shared telemetry must be absent before launch")
    if gate["claim_boundary"] != "SHARED_L12_SCHEDULING_AND_RESOURCE_AUTHORIZATION_ONLY":
        raise Refusal("shared gate claim boundary mismatch")


def require_unfrozen_draft_lock() -> None:
    if R4_FREEZE.exists() or R4_BUILD_GATE.exists() or SHARED_GATE.exists():
        raise Refusal("V004R4 draft lock violated: freeze/build/shared gate exists")
    assert_ready_for_freeze()  # intentionally refuses until target V012 is available


if __name__ == "__main__":
    try:
        require_unfrozen_draft_lock()
    except Refusal as error:
        print(f"LOCKED_DRAFT: {error}")
        raise SystemExit(2)
