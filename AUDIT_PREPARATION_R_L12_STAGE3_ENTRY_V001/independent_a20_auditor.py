#!/usr/bin/env python3
"""Independent raw A20-to-A21 reconstruction and live custody observation.

This module does not import the A20 producer or target production validators.
It parses canonical A20 bytes itself, reconstructs the frozen schedule and
resource predicates, and observes cross-gate, source/cache, workspace/output,
and telemetry state directly.  No producer-supplied custody or absence Boolean
is accepted by this interface.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import stat
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from dual_launch_coordinator import (
    ROLES, DualLaunchCoordinator, LaunchPolicy,
)


CHECKS = {
    "schedule_exact_schema": 1,
    "deep_exact_types": 1,
    "two_role_path_custody": 2,
    "normal_memory_pressure": 1,
    "resource_thresholds": 4,
    "freshness_window": 1,
    "telemetry_prelaunch_absence": 1,
}


class IndependentAuditRefusal(RuntimeError):
    """Canonical A20 cannot support the exact independent A21 certificate."""


@dataclass(frozen=True)
class ObservationPaths:
    l10_cross_gate: Path
    executable_by_role: dict[str, Path]
    cache_manifest_by_role: dict[str, Path]


def _reject_constant(value: str) -> object:
    raise IndependentAuditRefusal(f"nonfinite JSON constant: {value}")


def _object_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise IndependentAuditRefusal(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _canonical_json(value: object) -> bytes:
    try:
        return (json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise IndependentAuditRefusal("A20 is not finite canonical JSON") from error


def parse_canonical_schedule(raw: bytes) -> dict[str, object]:
    if type(raw) is not bytes or not raw.endswith(b"\n"):
        raise IndependentAuditRefusal("A20 raw framing mismatch")
    try:
        value = json.loads(
            raw, object_pairs_hook=_object_no_duplicates,
            parse_float=Decimal, parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise IndependentAuditRefusal("A20 raw JSON mismatch") from error
    if type(value) is not dict or _canonical_json(value) != raw:
        raise IndependentAuditRefusal("A20 is not one canonical raw record")
    return value


def _identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_mode,
        metadata.st_nlink,
    )


def _parent_identity(metadata: os.stat_result) -> tuple[int, int, int]:
    return metadata.st_dev, metadata.st_ino, metadata.st_mode


def _canonical_absolute(path: Path, label: str) -> None:
    if not path.is_absolute() or Path(str(path)) != path or "\x00" in str(path):
        raise IndependentAuditRefusal(f"{label}: path is not canonical absolute")
    cursor = Path(path.anchor)
    for component in path.parts[1:-1]:
        cursor /= component
        metadata = os.stat(cursor, follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise IndependentAuditRefusal(f"{label}: parent is aliased or special")


def _read_immutable(path: Path, label: str) -> tuple[str, int]:
    _canonical_absolute(path, label)
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent = os.open(path.parent, parent_flags)
    descriptor = -1
    try:
        parent_before = os.fstat(parent)
        parent_named = os.stat(path.parent, follow_symlinks=False)
        if _parent_identity(parent_before) != _parent_identity(parent_named):
            raise IndependentAuditRefusal(f"{label}: parent identity mismatch")
        descriptor = os.open(path.name, file_flags, dir_fd=parent)
        before = os.fstat(descriptor)
        named = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_mode & 0o222 or before.st_nlink != 1
            or _identity(before) != _identity(named)
        ):
            raise IndependentAuditRefusal(f"{label}: immutable custody mismatch")
        digest = hashlib.sha256()
        offset = 0
        while offset < before.st_size:
            block = os.pread(descriptor, min(1024 * 1024, before.st_size - offset), offset)
            if not block:
                raise IndependentAuditRefusal(f"{label}: short descriptor read")
            digest.update(block)
            offset += len(block)
        after = os.fstat(descriptor)
        named_after = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        if _identity(after) != _identity(before) or _identity(named_after) != _identity(before):
            raise IndependentAuditRefusal(f"{label}: descriptor/name drift")
        return digest.hexdigest(), before.st_dev
    except OSError as error:
        raise IndependentAuditRefusal(f"{label}: custody observation failed") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(parent)


def _observe_absent(path: Path, label: str) -> int:
    _canonical_absolute(path, label)
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path.parent, flags)
    try:
        held = os.fstat(descriptor)
        named = os.stat(path.parent, follow_symlinks=False)
        if _parent_identity(held) != _parent_identity(named):
            raise IndependentAuditRefusal(f"{label}: parent identity mismatch")
        try:
            os.lstat(path.name, dir_fd=descriptor)
        except FileNotFoundError:
            pass
        else:
            raise IndependentAuditRefusal(f"{label}: destination name is present")
        after = os.fstat(descriptor)
        if _parent_identity(after) != _parent_identity(held):
            raise IndependentAuditRefusal(f"{label}: parent drift")
        return held.st_dev
    except OSError as error:
        raise IndependentAuditRefusal(f"{label}: absence observation failed") from error
    finally:
        os.close(descriptor)


def _finite_int(value: object, label: str) -> int:
    if type(value) is not int or value < 0:
        raise IndependentAuditRefusal(f"{label}: exact nonnegative integer required")
    return value


def _reconstruct_resource_gate(
    schedule: dict[str, object], policy: LaunchPolicy, evaluation_epoch: int,
) -> int:
    snapshot = schedule.get("resource_snapshot")
    if type(snapshot) is not dict or type(evaluation_epoch) is not int:
        raise IndependentAuditRefusal("independent resource record is malformed")
    required = {
        "captured_epoch", "host_physical_memory_bytes", "available_memory_bytes",
        "workspace_free_disk_bytes", "workspace_filesystem_device",
        "both_workspace_roots_same_filesystem", "memory_pressure", "passes",
    }
    if set(snapshot) != required:
        raise IndependentAuditRefusal("independent resource key census mismatch")
    captured = _finite_int(snapshot["captured_epoch"], "capture epoch")
    total = _finite_int(snapshot["host_physical_memory_bytes"], "physical memory")
    available = _finite_int(snapshot["available_memory_bytes"], "available memory")
    free = _finite_int(snapshot["workspace_free_disk_bytes"], "free disk")
    device = _finite_int(snapshot["workspace_filesystem_device"], "filesystem device")
    reconstructed = (
        snapshot["memory_pressure"] == "NORMAL"
        and snapshot["both_workspace_roots_same_filesystem"] is True
        and total >= policy.minimum_host_physical_memory_bytes
        and available >= policy.minimum_available_memory_bytes
        and free >= policy.minimum_workspace_free_disk_bytes
        and 0 <= evaluation_epoch - captured <= policy.maximum_schedule_age_seconds
    )
    if not reconstructed or snapshot["passes"] is not reconstructed:
        raise IndependentAuditRefusal("independent resource/freshness reconstruction failed")
    return device


def audit_canonical_schedule(
    schedule_raw: bytes, policy: LaunchPolicy, evaluation_epoch: int,
    observations: ObservationPaths,
) -> dict[str, object]:
    if type(observations) is not ObservationPaths:
        raise IndependentAuditRefusal("independent observation-path census mismatch")
    schedule = parse_canonical_schedule(schedule_raw)
    coordinator = DualLaunchCoordinator(policy, evaluation_epoch)
    schedule_sha256 = coordinator.admit_schedule(schedule)
    scheduled_device = _reconstruct_resource_gate(schedule, policy, evaluation_epoch)

    cross_digest, cross_device = _read_immutable(
        observations.l10_cross_gate, "independent A18 L10 cross gate",
    )
    if schedule.get("l10_cross_gate_sha256") != cross_digest:
        raise IndependentAuditRefusal("independent A18 binding mismatch")
    if (
        type(observations.executable_by_role) is not dict
        or set(observations.executable_by_role) != set(ROLES)
        or type(observations.cache_manifest_by_role) is not dict
        or set(observations.cache_manifest_by_role) != set(ROLES)
    ):
        raise IndependentAuditRefusal("independent role observation census mismatch")

    observed_hashes = {cross_digest}
    observed_paths = {str(observations.l10_cross_gate)}
    observed_devices = {cross_device}
    for role in ROLES:
        executable = observations.executable_by_role[role]
        cache = observations.cache_manifest_by_role[role]
        if (
            schedule["roles"][role]["worker_executable_path"] != str(executable)
            or str(executable) != policy.role_paths(role).executable
        ):
            raise IndependentAuditRefusal(f"independent {role} executable path mismatch")
        for label, path in (("executable", executable), ("cache manifest", cache)):
            digest, device = _read_immutable(path, f"independent {role} {label}")
            observed_hashes.add(digest)
            observed_paths.add(str(path))
            observed_devices.add(device)
        for label, path in (
            ("workspace", Path(policy.role_paths(role).workspace)),
            ("output", Path(policy.role_paths(role).output)),
        ):
            observed_devices.add(_observe_absent(path, f"independent {role} {label}"))
    telemetry_path = Path(policy.telemetry_path)
    if schedule["telemetry"]["path"] != str(telemetry_path):
        raise IndependentAuditRefusal("independent telemetry path mismatch")
    observed_devices.add(_observe_absent(telemetry_path, "independent telemetry"))
    if len(observed_paths) != 5 or len(observed_hashes) != 5:
        raise IndependentAuditRefusal("independent cross-role alias mismatch")
    if observed_devices != {scheduled_device}:
        raise IndependentAuditRefusal("independent destination filesystem mismatch")

    return {
        "schema": "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001",
        "classification": "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT",
        "auditor_role": "INDEPENDENT_DUAL_LAUNCH_COORDINATOR_REVIEW",
        "schedule_sha256": schedule_sha256,
        "l10_cross_gate_sha256": cross_digest,
        "checks": dict(CHECKS),
        "checks_total": sum(CHECKS.values()),
        "checks_passed": sum(CHECKS.values()),
        "failures": [],
        "claim_boundary": (
            "INDEPENDENT_READINESS_AUDIT_ONLY__NO_L12_AUTHORIZATION_RELEASE_OR_RESULT"
        ),
    }
