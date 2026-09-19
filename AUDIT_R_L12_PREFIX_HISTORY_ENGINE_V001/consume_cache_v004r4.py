#!/usr/bin/env python3
"""Independent hostile V004R4 L12 worker and native-record adapter.

This executable consumes the reversed-combination V004R4 storage cache with
the pre-existing hostile Chebyshev/recurrence engine.  It deliberately keeps
that engine's row, solver, comparison, and resource vocabulary: cross-branch
projection belongs to the independent final auditor, not to this writer.

The module is fail-closed before the worker-release barrier and publishes only
one finite L12 history.  It does not calculate a spectrum or make a scaling,
continuum, emergence, or gravity claim.
"""

from __future__ import annotations

import argparse
import ctypes
import gc
import hashlib
import json
import math
import os
import resource
import shutil
import socket
import stat
import sys
import time
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import independent_prefix_history_v004 as legacy
import independent_prefix_history_v004r2 as r2consumer


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
METHOD = HERE / "V004R4_CACHE_METHOD.md"
BUILDER = HERE / "build_cache_v004r4.py"
CONSUMER = Path(__file__).resolve()
PREFLIGHT = HERE / "validate_cache_preflight_v004r4.py"
FREEZE = HERE / "FROZEN_MANIFEST_V004R4.json"
PREFLIGHT_RESULT = HERE / "V004R4_CACHE_PREFLIGHT_RESULT.json"
INDEPENDENT_AUDIT = HERE / "HOSTILE_AUDIT_RESULT_V004R4.json"
CACHE_BUILD_AUTHORIZATION = HERE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
L10_EXECUTION_AUTHORIZATION = HERE / "L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json"
CACHED_L10_GATE = HERE / "CACHED_L10_GATE_V004R4.json"
HOSTILE_L12_AUTHORIZATION = HERE / "HOSTILE_L12_EXECUTION_GATE_V004R4.json"
CACHE_ROOT = HERE / "V004R4_CACHE_PAYLOADS/L12"
WORKSPACE = HERE / "V004R4_WORKSPACES/L12"
OUTPUT = HERE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json"
SHARED = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
L10_CROSS_GATE = SHARED / "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
SCHEDULE_GATE = SHARED / "SHARED_AGGREGATE_SCHEDULE_GATE_V001.json"
SCHEDULE_AUDIT = SHARED / "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json"
HANDSHAKE = SHARED / "DUAL_L12_LAUNCH_HANDSHAKE_V002.json"
WORKER_RELEASE = SHARED / "DUAL_L12_WORKER_RELEASE_V002.json"
TELEMETRY = SHARED / "SHARED_AGGREGATE_TELEMETRY_V001.json"
FINAL_AUDITOR = (
    ROOT / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
    / "independent_final_auditor.py"
)
FINAL_AUDITOR_SHA256 = "c252092ff3a4c10bcfd6055600b18ed2ccd8bed90581cec29108ac6c31f5c7cf"
TARGET_V012_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
TARGET_V012_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
TARGET_V012_FREEZE = TARGET_V012_DIR / "FREEZE.json"
TARGET_V012_AUDIT = TARGET_V012_AUDIT_DIR / "HOSTILE_AUDIT_RESULT_V001.json"
TARGET_V012_CONSUMER = TARGET_V012_DIR / "consume_target_cache.py"
TARGET_V012_L10_GATE = TARGET_V012_DIR / "CACHED_L10_GATE_V012.json"
TARGET_V012_L12_MANIFEST = (
    TARGET_V012_DIR / "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json"
)

# Every packet-local Python source which is executed by the builder, preflight,
# or history worker is part of the frozen source packet.  Keeping this census
# here gives all three executables one exact definition and prevents an
# imported implementation from sitting outside cryptographic custody.
EXECUTED_DEPENDENCY_NAMES = (
    "independent_prefix_history.py",
    "independent_prefix_history_v002.py",
    "independent_prefix_history_v003.py",
    "independent_prefix_history_v004.py",
    "independent_prefix_history_v004r2.py",
    "v004r2_common.py",
    "validate_v004r4_zero_length_preflight.py",
    "v004r4_cache_io.py",
)
EXECUTED_DEPENDENCIES = {
    name: HERE / name for name in EXECUTED_DEPENDENCY_NAMES
}

HOSTILE_AUDIT_KEYS = {
    "schema", "classification", "auditor_role", "audited_freeze_sha256",
    "audited_files_sha256", "preflight_result_sha256", "checks_passed",
    "checks_total", "failures", "v004r3_bytes_preserved", "absence_census",
    "payload_or_history_executed", "claim_boundary",
}
HOSTILE_AUDIT_ABSENCE = {
    "build_gate": False,
    "shared_gate": False,
    "shared_telemetry": False,
    "cache_payloads": False,
    "postbuild_payload_audit": False,
    "workspaces": False,
    "histories": False,
}
TARGET_V012_INTERFACE_KEYS = {
    "freeze_sha256", "freeze_schema", "audit_sha256", "audit_schema",
    "audit_classification", "consumer_sha256", "L10_gate_sha256",
    "L10_gate_schema", "L10_gate_classification",
    "L12_cache_manifest_sha256", "L12_cache_manifest_schema",
}

WIRE_MAX_BYTES = 16 * 1024
READY_SCHEMA = "V012_L12_WORKER_READY_V001"
RELEASE_SCHEMA = "V012_L12_WORKER_RELEASE_COMMAND_V001"
ACK_SCHEMA = "V012_L12_WORKER_RELEASE_ACK_V001"
COMPLETION_SCHEMA = "V012_L12_WORKER_COMPLETION_V001"
NONCE_DOMAIN = b"V012_L12_WORKER_NONCE_V001\0"
CHANNEL_DOMAIN = b"V012_L12_CONTROL_CHANNEL_V001\0"
PROCESS_START_DOMAIN = b"V012_L12_PROCESS_START_V001\0"
ACK_DOMAIN = b"V012_DUAL_L12_RELEASE_ACK_V001\0"

LENGTH = 12
SCRATCH_LIMIT = 21_474_836_480
OVERHEAD_RESERVE = 1_048_576
RSS_LIMIT = 17_179_869_184
WALL_LIMIT = 108_000.0
ORIGINAL_PHYSICAL_WALL_LIMIT = physical.L12_WALL_LIMIT
ORIGINAL_ENGINE_WALL_LIMIT = v3.WALL_LIMIT
NUMERICAL_WORKSPACE_LIMIT = 1_400_000_000
MAPPED_CACHE_LIMIT = 536_870_912
EXPECTED_STATE_BYTES = 8_773_664_640
EXPECTED_CACHE_BYTES = 826_221_912
EXPECTED_STATE_PLUS_CACHE_BYTES = 9_599_886_552
EXPECTED_DISK_MINIMUM_BYTES = 9_600_935_128
EXPECTED_AUTHENTICATION_PEAK_BYTES = 252_944_080
EXPECTED_TERMINAL_MAPPING_BYTES = 234_782_536
PROCESS_START_EPOCH = int(time.time())

ROW_KEYS = {
    "event", "input_prefix", "input_prefix_dimension",
    "logical_output_prefix_dimension", "terminal_children_streamed",
    "allow_probability", "blocked_probability", "reverse_support_probability",
    "blocked_null_state_error", "W_n", "q_retained_after_transport",
    "q_genesis_after", "sector_weights", "connector_delta_l1",
    "connector_delta_signed", "admission_total_content_residual",
    "admission_bandwidth_residual", "target_owner_residual",
    "transport_node_residual_l1", "transport_node_residual_linf",
    "null_transport_node_residual_l1", "transport_number_drift",
    "null_transport_number_drift", "actual_norm_error", "null_norm_error",
    "actual_solver", "null_solver",
}
SOLVER_BASE_KEYS = {
    "converged", "batches", "maximum_degree",
    "maximum_endpoint_difference", "maximum_tail_indicator_32", "algorithm",
    "quadrature_group_max", "allocation_vector_slots",
    "maximum_allocation_estimate_bytes", "allocation_limit_bytes",
    "quadrature_nodes", "q_sharded",
}
SOLVER_TERMINAL_KEYS = SOLVER_BASE_KEYS | {
    "terminal_children_streamed", "terminal_child0_entries",
    "terminal_child1_nonzero_admission_entries",
    "full_terminal_array_allocated",
}
COMPARISON_KEYS = {
    "resolved", "classification", "epsilon",
    "maximum_admission_accounting_residual",
    "maximum_node_continuity_residual_l1", "maximum_norm_error",
    "maximum_number_drift", "rough_sharp", "sector",
    "admission_acceptance", "routed_acceptance", "connector_ratio",
}
RESOURCE_KEYS = {
    "peak_logical_state_plus_cache_bytes", "scratch_limit_bytes",
    "maximum_numerical_allocation_estimate_bytes",
    "numerical_workspace_limit_bytes",
    "authentication_peak_certificate_bytes", "peak_rss_bytes",
    "rss_limit_bytes", "wall_seconds_including_authentication",
    "wall_limit_seconds", "passed",
}
HISTORY_KEYS = {
    "schema", "L", "events", "dimension", "preterminal_dimension", "edges",
    "representation", "lineage_authority", "coarse_method", "fine_method",
    "rows", "comparison", "terminal_shards", "cache_manifest_sha256",
    "cache_build_authorization_gate_sha256",
    "l10_execution_authorization_gate_sha256",
    "postbuild_payload_audit_sha256", "target_hostile_l10_cross_gate_sha256",
    "shared_aggregate_schedule_gate_sha256",
    "shared_aggregate_schedule_gate_audit_sha256",
    "hostile_l12_execution_gate_sha256", "dual_l12_launch_handshake_sha256",
    "dual_l12_worker_release_sha256", "resource", "consumer_sha256",
    "builder_sha256", "method_sha256", "preflight_sha256", "freeze_sha256",
    "preflight_result_sha256", "independent_hostile_audit_sha256",
    "claim_boundary",
}
L12_ONLY_HISTORY_KEYS = {
    "postbuild_payload_audit_sha256", "target_hostile_l10_cross_gate_sha256",
    "shared_aggregate_schedule_gate_sha256",
    "shared_aggregate_schedule_gate_audit_sha256",
    "hostile_l12_execution_gate_sha256", "dual_l12_launch_handshake_sha256",
    "dual_l12_worker_release_sha256",
}
L10_HISTORY_KEYS = HISTORY_KEYS - L12_ONLY_HISTORY_KEYS


class Refusal(RuntimeError):
    """The hostile worker refused an incomplete or changed authority chain."""


def exact_keys(value: object, expected: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != expected:
        raise Refusal(f"{label} exact key census mismatch")
    return value


def sha256_text(value: object) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def finite_float(value: object) -> bool:
    return type(value) is float and math.isfinite(value)


def validate_hostile_prepayload_audit(
    record: object, *, freeze_sha256: str, frozen_files: dict[str, str],
    preflight_result_sha256: str,
) -> dict[str, Any]:
    """Validate the one authoritative V004R4 prepayload audit schema.

    Earlier drafts described two disjoint schemas: the build path required a
    preflight digest which the exact-key auditor prohibited.  This function is
    the production intersection used by both cache construction and history
    consumption.
    """
    audit = exact_keys(record, HOSTILE_AUDIT_KEYS, "hostile V004R4 prepayload audit")
    if (
        audit["schema"] != "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001"
        or audit["classification"]
        != "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE"
        or audit["auditor_role"] != "INDEPENDENT_HOSTILE_READ_ONLY_REVIEW"
        or audit["audited_freeze_sha256"] != freeze_sha256
        or audit["audited_files_sha256"] != frozen_files
        or audit["preflight_result_sha256"] != preflight_result_sha256
        or type(audit["checks_total"]) is not int
        or audit["checks_total"] <= 0
        or type(audit["checks_passed"]) is not int
        or audit["checks_passed"] != audit["checks_total"]
        or audit["failures"] != []
        or audit["v004r3_bytes_preserved"] is not True
        or type(audit["v004r3_bytes_preserved"]) is not bool
        or audit["absence_census"] != HOSTILE_AUDIT_ABSENCE
        or any(type(value) is not bool for value in audit["absence_census"].values())
        or audit["payload_or_history_executed"] is not False
        or type(audit["payload_or_history_executed"]) is not bool
        or audit["claim_boundary"] != "NONPHYSICAL_V004R4_CONTROL_PLANE_AUDIT_ONLY"
    ):
        raise Refusal("hostile V004R4 prepayload audit content mismatch")
    return audit


def validate_hostile_build_authorization(
    gate: object, audit: dict[str, Any], *, freeze_sha256: str,
    frozen_files: dict[str, str], audit_sha256: str,
) -> dict[str, Any]:
    authorization = exact_keys(
        gate,
        {
            "schema", "classification", "authorized_cache_lengths",
            "freeze_sha256", "files_sha256", "independent_hostile_audit",
            "target_v012_interface", "dual_obstruction_custody",
            "claim_boundary",
        },
        "hostile V004R4 cache build authorization",
    )
    binding = exact_keys(
        authorization["independent_hostile_audit"],
        {"path", "sha256", "schema", "classification", "checks_passed", "checks_total"},
        "hostile V004R4 cache build audit binding",
    )
    target_interface = exact_keys(
        authorization["target_v012_interface"], TARGET_V012_INTERFACE_KEYS,
        "hostile cache target V012 interface",
    )
    for key in (
        "freeze_sha256", "audit_sha256", "consumer_sha256", "L10_gate_sha256",
        "L12_cache_manifest_sha256",
    ):
        _lower_sha256(target_interface[key], f"target V012 interface {key}")
    if (
        authorization["schema"] != "HOSTILE_V004R4_CACHE_BUILD_AUTHORIZATION_GATE"
        or authorization["classification"]
        != "AUTHORIZE_HOSTILE_V004R4_CACHE_AFTER_INDEPENDENT_AUDIT"
        or authorization["authorized_cache_lengths"] != [4, 6, 8, 10, 12]
        or any(type(value) is not int for value in authorization["authorized_cache_lengths"])
        or authorization["freeze_sha256"] != freeze_sha256
        or authorization["files_sha256"] != frozen_files
        or binding != {
            "path": str(INDEPENDENT_AUDIT),
            "sha256": audit_sha256,
            "schema": audit["schema"],
            "classification": audit["classification"],
            "checks_passed": audit["checks_passed"],
            "checks_total": audit["checks_total"],
        }
        or target_interface["freeze_schema"] != "TARGET_L12_STORAGE_CACHE_FREEZE_V012"
        or target_interface["audit_schema"] != "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001"
        or target_interface["audit_classification"]
        != "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE"
        or target_interface["L10_gate_schema"] != "TARGET_V012_CACHED_L10_GATE"
        or target_interface["L10_gate_classification"] != "PASS_TARGET_V012_CACHED_L10"
        or target_interface["L12_cache_manifest_schema"]
        != "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012"
        or authorization["dual_obstruction_custody"]
        != r2consumer.common.OBSTRUCTION_ROWS
        or authorization["claim_boundary"]
        != "CACHE_BUILD_AUTHORIZATION_ONLY__NO_HISTORY_OR_PHYSICS_RESULT"
    ):
        raise Refusal("hostile V004R4 cache build authorization content mismatch")
    return authorization


def retain_build_authorization_inputs(
    custody: "AuthorityCustody", authorization: dict[str, Any],
) -> None:
    """Retain and reconstruct all cross-packet records named by the build gate."""
    interface = authorization["target_v012_interface"]
    freeze, _ = read_authority(
        custody, TARGET_V012_FREEZE, "target V012 freeze",
        interface["freeze_sha256"],
    )
    audit, _ = read_authority(
        custody, TARGET_V012_AUDIT, "target V012 prepayload audit",
        interface["audit_sha256"],
    )
    _unused, _ = custody.authenticate(
        TARGET_V012_CONSUMER, "target V012 consumer",
        interface["consumer_sha256"],
    )
    l10, _ = read_authority(
        custody, TARGET_V012_L10_GATE, "target V012 cached L10 gate",
        interface["L10_gate_sha256"],
    )
    manifest, _ = read_authority(
        custody, TARGET_V012_L12_MANIFEST, "target V012 L12 cache manifest",
        interface["L12_cache_manifest_sha256"],
    )
    if (
        freeze.get("schema") != interface["freeze_schema"]
        or audit.get("schema") != interface["audit_schema"]
        or audit.get("classification") != interface["audit_classification"]
        or audit.get("audited_freeze_sha256") != interface["freeze_sha256"]
        or audit.get("checks_passed") != audit.get("checks_total")
        or audit.get("failures") != []
        or audit.get("payload_or_history_executed") is not False
        or l10.get("schema") != interface["L10_gate_schema"]
        or l10.get("classification") != interface["L10_gate_classification"]
        or l10.get("consumer_sha256") != interface["consumer_sha256"]
        or l10.get("freeze_sha256") != interface["freeze_sha256"]
        or manifest.get("schema") != interface["L12_cache_manifest_schema"]
        or manifest.get("L") != 12 or type(manifest.get("L")) is not int
        or manifest.get("consumer_sha256") != interface["consumer_sha256"]
        or manifest.get("freeze_sha256") != interface["freeze_sha256"]
    ):
        raise Refusal("target V012 build interface content mismatch")
    for role, row in authorization["dual_obstruction_custody"].items():
        if role not in {"target", "hostile"} or type(row) is not dict:
            raise Refusal("dual obstruction custody role mismatch")
        for path_key, hash_key in (
            ("obstruction_path", "obstruction_sha256"),
            ("log_path", "log_sha256"), ("monitor_path", "monitor_sha256"),
        ):
            path = ROOT / row[path_key]
            _unused, _ = custody.authenticate(
                path, f"{role} obstruction custody {path_key}", row[hash_key],
                immutable=False,
            )
        implementation_paths = {
            "target": (
                ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py",
                ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md",
                ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_METHOD_V004.json",
            ),
            "hostile": (
                HERE / "independent_prefix_history_v003.py",
                HERE / "V003_L12_EXECUTABLE_METHOD.md",
                HERE / "FROZEN_MANIFEST_V003.json",
            ),
        }
        for path, hash_key in zip(
            implementation_paths[role],
            ("implementation_sha256", "method_sha256", "freeze_sha256"),
        ):
            if path in custody.files:
                if custody.files[path].digest != row[hash_key]:
                    raise Refusal(f"{role} obstruction parent hash mismatch")
            else:
                _unused, _ = custody.authenticate(
                    path, f"{role} obstruction parent {hash_key}", row[hash_key],
                    immutable=False,
                )


def descriptor_sha256(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while block := os.pread(descriptor, 16 * 2**20, offset):
        digest.update(block)
        offset += len(block)
    return digest.hexdigest()


def _file_identity(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        metadata.st_mode,
    )


def _descriptor_bytes(descriptor: int, size: int, label: str) -> bytes:
    if type(size) is not int or size < 0:
        raise Refusal(f"{label} descriptor size mismatch")
    raw = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(descriptor, min(16 * 2**20, size - offset), offset)
        if not block:
            raise Refusal(f"{label} descriptor read was short")
        raw.extend(block)
        offset += len(block)
    return bytes(raw)


@dataclass
class RetainedFile:
    descriptor: int
    parent_descriptor: int
    identity: tuple[int, int, int, int, int, int, int]
    parent_identity: tuple[int, int]
    digest: str
    path: Path
    immutable_required: bool


class AuthorityCustody:
    """Retain authenticated descriptors until the history is published."""

    def __init__(self) -> None:
        self.files: dict[Path, RetainedFile] = {}

    def authenticate(
        self, path: Path, label: str, expected_digest: str | None = None,
        immutable: bool = True,
    ) -> tuple[dict[str, Any] | None, str]:
        canonical = path.resolve(strict=False)
        if path != canonical or path.is_symlink() or path in self.files:
            raise Refusal(f"{label} path/custody mismatch")
        _require_no_symlink_parents(path, label)
        parent_flags = (
            os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        parent_descriptor = -1
        descriptor = -1
        try:
            parent_descriptor = os.open(path.parent, parent_flags)
            parent_identity = _directory_identity(
                path.parent, parent_descriptor, label,
            )
            flags = (
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
        except BaseException as error:
            if descriptor >= 0:
                os.close(descriptor)
            if parent_descriptor >= 0:
                os.close(parent_descriptor)
            if isinstance(error, OSError):
                raise Refusal(f"{label} absent") from error
            raise
        try:
            metadata = os.fstat(descriptor)
            current = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
            identity = _file_identity(metadata)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_nlink != 1
                or (immutable and metadata.st_mode & 0o222)
                or _file_identity(current) != identity
            ):
                raise Refusal(f"{label} is not an immutable ordinary file")
            digest = descriptor_sha256(descriptor)
            if expected_digest is not None and digest != expected_digest:
                raise Refusal(f"{label} hash mismatch")
            after = os.fstat(descriptor)
            current_after = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
            if (
                _file_identity(after) != identity
                or _file_identity(current_after) != identity
                or _directory_identity(
                    path.parent, parent_descriptor, label,
                ) != parent_identity
            ):
                raise Refusal(f"{label} changed during authentication")
            value: dict[str, Any] | None = None
            if path.suffix == ".json":
                raw = _descriptor_bytes(descriptor, metadata.st_size, label)
                if hashlib.sha256(raw).hexdigest() != digest:
                    raise Refusal(f"{label} JSON bytes/hash mismatch")
                value = strict_json_object(raw, label)
            retained = RetainedFile(
                descriptor, parent_descriptor, identity, parent_identity,
                digest, path, immutable,
            )
            self.files[path] = retained
            self.verify_one(path, label)
            return value, digest
        except BaseException:
            retained = self.files.pop(path, None)
            if retained is not None:
                for owned in (retained.descriptor, retained.parent_descriptor):
                    os.close(owned)
            else:
                if descriptor >= 0:
                    os.close(descriptor)
                if parent_descriptor >= 0:
                    os.close(parent_descriptor)
            raise

    def authenticate_or_reuse(
        self, path: Path, label: str, expected_digest: str | None = None,
        immutable: bool = True,
    ) -> tuple[dict[str, Any] | None, str]:
        """Reuse one already held authority without reopening a second path."""
        if path not in self.files:
            return self.authenticate(path, label, expected_digest, immutable)
        retained = self.files[path]
        if (
            expected_digest is not None and retained.digest != expected_digest
        ) or (immutable and retained.immutable_required is not True):
            raise Refusal(f"{label} retained custody mismatch")
        self.verify_all()
        value: dict[str, Any] | None = None
        if path.suffix == ".json":
            raw = _descriptor_bytes(
                retained.descriptor, retained.identity[2], label,
            )
            if hashlib.sha256(raw).hexdigest() != retained.digest:
                raise Refusal(f"{label} retained JSON bytes/hash mismatch")
            value = strict_json_object(raw, label)
        self.verify_all()
        return value, retained.digest

    def verify_one(self, path: Path, label: str) -> None:
        retained = self.files[path]
        try:
            _require_no_symlink_parents(retained.path, label)
            if _directory_identity(
                retained.path.parent, retained.parent_descriptor, label,
            ) != retained.parent_identity:
                raise Refusal(f"{label} retained parent identity changed")
            metadata_before = os.fstat(retained.descriptor)
            current_before = os.stat(
                retained.path.name, dir_fd=retained.parent_descriptor,
                follow_symlinks=False,
            )
            observed = descriptor_sha256(retained.descriptor)
            metadata_after = os.fstat(retained.descriptor)
            try:
                current_after = os.stat(
                    retained.path.name, dir_fd=retained.parent_descriptor,
                    follow_symlinks=False,
                )
            except OSError as error:
                raise Refusal(f"retained authority path disappeared: {retained.path}") from error
            if (
                _directory_identity(
                    retained.path.parent, retained.parent_descriptor, label,
                ) != retained.parent_identity
                or not stat.S_ISREG(metadata_before.st_mode)
                or metadata_before.st_nlink != 1
                or (retained.immutable_required and metadata_before.st_mode & 0o222)
                or _file_identity(metadata_before) != retained.identity
                or _file_identity(current_before) != retained.identity
                or _file_identity(metadata_after) != retained.identity
                or _file_identity(current_after) != retained.identity
                or observed != retained.digest
            ):
                raise Refusal(f"retained authority changed: {retained.path}")
        except BaseException as error:
            if isinstance(error, Refusal) and str(error).startswith(
                "retained authority changed:"
            ):
                raise
            raise Refusal(f"retained authority changed: {retained.path}") from error

    def verify_all(self) -> None:
        for path in self.files:
            self.verify_one(path, f"retained authority {path}")

    def close(self) -> None:
        for retained in self.files.values():
            for descriptor in (
                retained.descriptor, retained.parent_descriptor,
            ):
                try:
                    os.close(descriptor)
                except OSError:
                    pass
        self.files.clear()


def strict_json_object(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise Refusal(f"{label} duplicate JSON key")
            result[key] = value
        return result

    def constant(token: str) -> object:
        raise Refusal(f"{label} nonfinite JSON constant: {token}")

    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant,
        )
    except Refusal:
        raise
    except (UnicodeDecodeError, ValueError, TypeError) as error:
        raise Refusal(f"{label} malformed JSON") from error
    if type(value) is not dict:
        raise Refusal(f"{label} must be a JSON object")
    return value


def canonical_json_bytes(record: object) -> bytes:
    try:
        return (
            json.dumps(
                record, sort_keys=True, separators=(",", ":"),
                ensure_ascii=True, allow_nan=False,
            ) + "\n"
        ).encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("history is not finite canonical JSON") from error


def positive_integer(value: object) -> bool:
    return type(value) is int and value > 0


def _lower_sha256(value: object, label: str) -> str:
    if not sha256_text(value):
        raise Refusal(f"{label} is not a lowercase SHA-256")
    return value


def process_start_token(process_id: int) -> str:
    """Return the coordinator-recomputable kernel process-start identity."""
    if type(process_id) is not int or process_id <= 0:
        raise Refusal("process start token PID is invalid")
    class ProcBsdInfo(ctypes.Structure):
        _fields_ = [
            ("flags", ctypes.c_uint32), ("status", ctypes.c_uint32),
            ("xstatus", ctypes.c_uint32), ("pid", ctypes.c_uint32),
            ("ppid", ctypes.c_uint32), ("uid", ctypes.c_uint32),
            ("gid", ctypes.c_uint32), ("ruid", ctypes.c_uint32),
            ("rgid", ctypes.c_uint32), ("svuid", ctypes.c_uint32),
            ("svgid", ctypes.c_uint32), ("reserved", ctypes.c_uint32),
            ("comm", ctypes.c_char * 16), ("name", ctypes.c_char * 32),
            ("nfiles", ctypes.c_uint32), ("pgid", ctypes.c_uint32),
            ("pjobc", ctypes.c_uint32), ("e_tdev", ctypes.c_uint32),
            ("e_tpgid", ctypes.c_uint32), ("nice", ctypes.c_int32),
            ("start_seconds", ctypes.c_uint64),
            ("start_microseconds", ctypes.c_uint64),
        ]
    try:
        library = ctypes.CDLL("/usr/lib/libproc.dylib")
        query = library.proc_pidinfo
        query.argtypes = [
            ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
            ctypes.c_void_p, ctypes.c_int,
        ]
        query.restype = ctypes.c_int
        record = ProcBsdInfo()
        size = query(
            process_id, 3, 0, ctypes.byref(record), ctypes.sizeof(record),
        )
    except (AttributeError, OSError) as error:
        raise Refusal("cannot authenticate kernel process start") from error
    if (
        size != ctypes.sizeof(record) or record.pid != process_id
        or record.start_seconds <= 0 or record.start_microseconds >= 1_000_000
    ):
        raise Refusal("kernel process start record is malformed")
    stamp = (
        f"{record.start_seconds}.{record.start_microseconds:06d}".encode("ascii")
    )
    return hashlib.sha256(
        PROCESS_START_DOMAIN + str(process_id).encode("ascii") + b"\0" + stamp
    ).hexdigest()


def validate_cross_role_identity_distinctness(
    workers: object, authorization_hashes: object,
) -> None:
    """Reject a two-role handshake that aliases either authority or identity."""
    roles = {"target_v012", "hostile_v004r4"}
    worker_rows = exact_keys(workers, roles, "dual L12 distinct worker roles")
    authorizations = exact_keys(
        authorization_hashes, roles, "dual L12 distinct authorization roles",
    )
    if (
        any(not sha256_text(value) for value in authorizations.values())
        or len(set(authorizations.values())) != 2
    ):
        raise Refusal("dual L12 cross-role authorization alias")
    identity_fields = (
        "process_id", "worker_id", "control_channel_id",
        "nonce_commitment_sha256",
    )
    for field in identity_fields:
        values = [worker_rows[role].get(field) for role in sorted(roles)]
        if len(set(values)) != 2:
            raise Refusal(f"dual L12 cross-role {field} alias")


class OrchestratedWorkerSession:
    """One-shot inherited-socket readiness/release protocol for an L12 worker."""

    READY_KEYS = {
        "schema", "role", "worker_id", "process_id", "process_start_token",
        "executable_path", "executable_sha256", "workspace_path", "output_path",
        "control_channel_id", "nonce_commitment_sha256", "ready_epoch",
        "blocked_on_release",
    }
    RELEASE_KEYS = {
        "schema", "role", "worker_id", "process_id", "process_start_token",
        "control_channel_id", "nonce_commitment_sha256", "handshake_sha256",
        "worker_release_sha256", "release_epoch",
    }
    ACK_KEYS = {
        "schema", "role", "worker_id", "process_id", "process_start_token",
        "control_channel_id", "nonce_hex", "ack_sha256",
    }
    COMPLETION_KEYS = {
        "schema", "role", "worker_id", "process_id", "process_start_token",
        "control_channel_id", "output_path", "output_sha256",
        "completion_epoch", "blocked_on_orchestrator_close",
    }

    def __init__(
        self, *, role: str, worker_id: str, control_fd: int,
        control_channel_id: str, executable: Path, workspace: Path, output: Path,
    ) -> None:
        if role not in {"target_v012", "hostile_v004r4"}:
            raise Refusal("orchestrated worker role mismatch")
        if type(worker_id) is not str or not worker_id or len(worker_id) > 256:
            raise Refusal("orchestrated worker id is malformed")
        _lower_sha256(control_channel_id, "control channel id")
        if type(control_fd) is not int or control_fd < 3:
            raise Refusal("control descriptor is invalid")
        metadata = os.fstat(control_fd)
        if not stat.S_ISSOCK(metadata.st_mode):
            raise Refusal("control descriptor is not a socket")
        duplicate = os.dup(control_fd)
        self.channel = socket.socket(fileno=duplicate)
        if self.channel.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE) != socket.SOCK_STREAM:
            self.channel.close()
            raise Refusal("control channel is not a duplex stream socket")
        try:
            self.channel.getpeername()
        except OSError as error:
            self.channel.close()
            raise Refusal("control channel has no connected peer") from error
        self.channel.settimeout(300.0)
        self.role = role
        self.worker_id = worker_id
        self.control_channel_id = control_channel_id
        self.executable = executable
        self.workspace = workspace
        self.output = output
        if (
            workspace.exists() or workspace.is_symlink()
            or output.exists() or output.is_symlink()
        ):
            self.close()
            raise Refusal("worker workspace/output exists before READY")
        self.process_id = os.getpid()
        self.process_start_token = process_start_token(self.process_id)
        self.nonce = os.urandom(32)
        self.nonce_commitment_sha256 = hashlib.sha256(
            NONCE_DOMAIN + self.nonce
        ).hexdigest()
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.executable_fd = os.open(executable, flags)
        executable_metadata = os.fstat(self.executable_fd)
        if not stat.S_ISREG(executable_metadata.st_mode):
            self.close()
            raise Refusal("worker executable is not an ordinary file")
        self.executable_identity = (
            executable_metadata.st_dev, executable_metadata.st_ino,
            executable_metadata.st_size, executable_metadata.st_mtime_ns,
            executable_metadata.st_ctime_ns,
        )
        self.executable_sha256 = descriptor_sha256(self.executable_fd)
        self.ready = {
            "schema": READY_SCHEMA,
            "role": role,
            "worker_id": worker_id,
            "process_id": self.process_id,
            "process_start_token": self.process_start_token,
            "executable_path": str(executable),
            "executable_sha256": self.executable_sha256,
            "workspace_path": str(workspace),
            "output_path": str(output),
            "control_channel_id": control_channel_id,
            "nonce_commitment_sha256": self.nonce_commitment_sha256,
            "ready_epoch": int(time.time()),
            "blocked_on_release": True,
        }
        exact_keys(self.ready, self.READY_KEYS, "worker READY")
        self.ready_bytes = canonical_json_bytes(self.ready)
        if len(self.ready_bytes) > WIRE_MAX_BYTES:
            self.close()
            raise Refusal("worker READY exceeds wire bound")
        self.ready_sha256 = hashlib.sha256(self.ready_bytes).hexdigest()
        self.release: dict[str, Any] | None = None
        self.release_bytes: bytes | None = None
        self.acked = False
        self.completed = False

    def _verify_executable(self) -> None:
        metadata = os.fstat(self.executable_fd)
        identity = (
            metadata.st_dev, metadata.st_ino, metadata.st_size,
            metadata.st_mtime_ns, metadata.st_ctime_ns,
        )
        current = os.stat(self.executable, follow_symlinks=False)
        current_identity = (
            current.st_dev, current.st_ino, current.st_size,
            current.st_mtime_ns, current.st_ctime_ns,
        )
        if (
            not stat.S_ISREG(current.st_mode)
            or identity != self.executable_identity
            or current_identity != self.executable_identity
            or descriptor_sha256(self.executable_fd) != self.executable_sha256
        ):
            raise Refusal("worker executable identity changed")

    def _receive_record(self) -> tuple[dict[str, Any], bytes]:
        data = bytearray()
        while b"\n" not in data:
            try:
                block = self.channel.recv(4096)
            except socket.timeout as error:
                raise Refusal("worker release command timed out") from error
            if not block:
                raise Refusal("control channel closed before worker release")
            data.extend(block)
            if len(data) > WIRE_MAX_BYTES:
                raise Refusal("worker release command exceeds wire bound")
        line, trailing = bytes(data).split(b"\n", 1)
        raw = line + b"\n"
        if trailing:
            raise Refusal("control channel sent multiple or trailing records")
        record = strict_json_object(raw, "worker release command")
        if canonical_json_bytes(record) != raw:
            raise Refusal("worker release command is not canonical JSON")
        return record, raw

    def announce_and_wait(self) -> dict[str, Any]:
        self._verify_executable()
        self.channel.sendall(self.ready_bytes)
        record, raw = self._receive_record()
        exact_keys(record, self.RELEASE_KEYS, "worker RELEASE")
        if (
            record["schema"] != RELEASE_SCHEMA
            or record["role"] != self.role
            or record["worker_id"] != self.worker_id
            or record["process_id"] != self.process_id
            or record["process_start_token"] != self.process_start_token
            or record["control_channel_id"] != self.control_channel_id
            or record["nonce_commitment_sha256"] != self.nonce_commitment_sha256
            or not sha256_text(record["handshake_sha256"])
            or not sha256_text(record["worker_release_sha256"])
            or type(record["release_epoch"]) is not int
            or record["release_epoch"] <= 0
        ):
            raise Refusal("worker RELEASE identity/binding mismatch")
        self.release = record
        self.release_bytes = raw
        return record

    def acknowledge(self) -> dict[str, Any]:
        if self.release is None or self.release_bytes is None or self.acked:
            raise Refusal("worker release ACK state mismatch")
        self._verify_executable()
        ack = {
            "schema": ACK_SCHEMA,
            "role": self.role,
            "worker_id": self.worker_id,
            "process_id": self.process_id,
            "process_start_token": self.process_start_token,
            "control_channel_id": self.control_channel_id,
            "nonce_hex": self.nonce.hex(),
            "ack_sha256": hashlib.sha256(
                ACK_DOMAIN + self.nonce + self.release_bytes
            ).hexdigest(),
        }
        exact_keys(ack, self.ACK_KEYS, "worker release ACK")
        data = canonical_json_bytes(ack)
        if len(data) > WIRE_MAX_BYTES:
            raise Refusal("worker release ACK exceeds wire bound")
        self.channel.sendall(data)
        self.acked = True
        return ack

    @staticmethod
    def _require_no_symlink_parents(path: Path) -> None:
        if not path.is_absolute():
            raise Refusal("worker output path is not absolute")
        candidate = path.parent
        while True:
            metadata = os.lstat(candidate)
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                raise Refusal("worker output has a symlinked/non-directory parent")
            if candidate.parent == candidate:
                return
            candidate = candidate.parent

    def complete(self, output_sha256: str) -> dict[str, Any]:
        """Authenticate the published output and block live until coordinator EOF."""
        if self.release is None or not self.acked or self.completed:
            raise Refusal("worker completion state mismatch")
        _lower_sha256(output_sha256, "worker completion output hash")
        self._verify_executable()
        self._require_no_symlink_parents(self.output)
        parent_flags = (
            os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        parent_descriptor = -1
        descriptor = -1
        try:
            parent_descriptor = os.open(self.output.parent, parent_flags)
            parent_before = _directory_identity(
                self.output.parent, parent_descriptor, "worker completion",
            )
            descriptor = os.open(
                self.output.name, flags, dir_fd=parent_descriptor,
            )
            opened = os.fstat(descriptor)
            current = os.stat(
                self.output.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            identity = _file_identity(opened)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_mode & 0o222
                or opened.st_nlink != 1
                or identity != _file_identity(current)
            ):
                raise Refusal("worker completion output authentication failed")
            digest = descriptor_sha256(descriptor)
            opened_after_hash = os.fstat(descriptor)
            current_after_hash = os.stat(
                self.output.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                digest != output_sha256
                or _file_identity(opened_after_hash) != identity
                or _file_identity(current_after_hash) != identity
                or _directory_identity(
                    self.output.parent, parent_descriptor,
                    "worker completion",
                ) != parent_before
            ):
                raise Refusal("worker completion output authentication failed")
            completion = {
                "schema": COMPLETION_SCHEMA,
                "role": self.role,
                "worker_id": self.worker_id,
                "process_id": self.process_id,
                "process_start_token": self.process_start_token,
                "control_channel_id": self.control_channel_id,
                "output_path": str(self.output),
                "output_sha256": output_sha256,
                "completion_epoch": int(time.time()),
                "blocked_on_orchestrator_close": True,
            }
            exact_keys(completion, self.COMPLETION_KEYS, "worker COMPLETION")
            wire = canonical_json_bytes(completion)
            if len(wire) > 2**20:
                raise Refusal("worker COMPLETION exceeds wire bound")
            self.channel.sendall(wire)
            self.channel.shutdown(socket.SHUT_WR)
            try:
                trailing = self.channel.recv(1)
            except socket.timeout as error:
                raise Refusal("orchestrator did not close after worker COMPLETION") from error
            if trailing:
                raise Refusal("orchestrator sent bytes after worker COMPLETION")
            self._require_no_symlink_parents(self.output)
            final = os.fstat(descriptor)
            final_path = os.stat(
                self.output.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            final_digest = descriptor_sha256(descriptor)
            final_after_hash = os.fstat(descriptor)
            final_path_after_hash = os.stat(
                self.output.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                _directory_identity(
                    self.output.parent, parent_descriptor,
                    "worker completion",
                ) != parent_before
                or _file_identity(final) != identity
                or _file_identity(final_path) != identity
                or _file_identity(final_after_hash) != identity
                or _file_identity(final_path_after_hash) != identity
                or final.st_mode & 0o222
                or final.st_nlink != 1
                or final_digest != output_sha256
            ):
                raise Refusal("worker completion output custody changed before EOF")
            self.completed = True
            return completion
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            if parent_descriptor >= 0:
                os.close(parent_descriptor)

    def close(self) -> None:
        if getattr(self, "executable_fd", -1) >= 0:
            os.close(self.executable_fd)
            self.executable_fd = -1
        if getattr(self, "channel", None) is not None:
            self.channel.close()
            self.channel = None


def fsync_directory(path: Path, retained_descriptor: int | None = None) -> None:
    descriptor = retained_descriptor
    owned = descriptor is None
    if descriptor is None:
        descriptor = os.open(
            path,
            os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0),
        )
    try:
        os.fsync(descriptor)
    finally:
        if owned:
            os.close(descriptor)


def existing_ancestor(path: Path) -> Path:
    candidate = path
    while not candidate.exists():
        if candidate.parent == candidate:
            raise Refusal("workspace has no existing filesystem ancestor")
        candidate = candidate.parent
    if candidate.is_symlink() or not candidate.is_dir():
        raise Refusal("workspace ancestor is not an ordinary directory")
    return candidate


def unlink_if_owned(path: Path, identity: tuple[int, int]) -> bool:
    """Remove only the staging inode created by this process."""
    try:
        metadata = os.lstat(path)
    except FileNotFoundError:
        return False
    if (
        not stat.S_ISREG(metadata.st_mode)
        or (metadata.st_dev, metadata.st_ino) != identity
    ):
        return False
    os.unlink(path)
    return True


def _require_no_symlink_parents(path: Path, label: str) -> None:
    text = str(path)
    if (
        not path.is_absolute() or str(Path(text)) != text
        or os.path.normpath(text) != text or "\x00" in text
    ):
        raise Refusal(f"{label} path is not canonical absolute")
    current = Path(path.anchor)
    for component in path.parts[1:-1]:
        current /= component
        try:
            metadata = os.stat(current, follow_symlinks=False)
        except OSError as error:
            raise Refusal(f"{label} parent path is absent") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise Refusal(f"{label} parent path is aliased")


def _directory_identity(
    path: Path, descriptor: int, label: str,
) -> tuple[int, int]:
    _require_no_symlink_parents(path / "placeholder", label)
    try:
        retained = os.fstat(descriptor)
        current = os.stat(path, follow_symlinks=False)
    except OSError as error:
        raise Refusal(f"{label} parent identity changed") from error
    if (
        not stat.S_ISDIR(retained.st_mode) or not stat.S_ISDIR(current.st_mode)
        or stat.S_ISLNK(current.st_mode)
        or (retained.st_dev, retained.st_ino)
        != (current.st_dev, current.st_ino)
    ):
        raise Refusal(f"{label} parent identity changed")
    return retained.st_dev, retained.st_ino


def _unlink_owned_at(
    parent_descriptor: int, name: str, identity: tuple[int, int],
) -> bool:
    try:
        metadata = os.stat(
            name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
    except FileNotFoundError:
        return False
    if (
        not stat.S_ISREG(metadata.st_mode)
        or (metadata.st_dev, metadata.st_ino) != identity
    ):
        return False
    os.unlink(name, dir_fd=parent_descriptor)
    return True


def _ensure_history_parent(parent: Path) -> None:
    try:
        metadata = os.stat(parent, follow_symlinks=False)
    except FileNotFoundError:
        _require_no_symlink_parents(parent, "hostile history")
        grandparent = parent.parent
        flags = (
            os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(grandparent, flags)
        try:
            before = _directory_identity(
                grandparent, descriptor, "hostile history grandparent",
            )
            os.mkdir(parent.name, 0o755, dir_fd=descriptor)
            os.fsync(descriptor)
            if _directory_identity(
                grandparent, descriptor, "hostile history grandparent",
            ) != before:
                raise Refusal("hostile history grandparent identity changed")
        finally:
            os.close(descriptor)
    else:
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise Refusal("hostile history parent is not an ordinary directory")


def atomic_publish(path: Path, record: dict[str, Any], custody: AuthorityCustody) -> str:
    data = canonical_json_bytes(record)
    parent = path.parent
    _ensure_history_parent(parent)
    _require_no_symlink_parents(path, "hostile history")
    parent_flags = (
        os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(parent, parent_flags)
    except OSError as error:
        raise Refusal("hostile history parent cannot be retained") from error
    try:
        parent_before = _directory_identity(
            parent, parent_descriptor, "hostile history",
        )
        try:
            os.stat(path.name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Refusal("refuse to overwrite hostile history")
    except BaseException:
        os.close(parent_descriptor)
        raise
    staging_name = (
        f".{path.name}.staging-{os.getpid()}-{os.urandom(12).hex()}"
    )
    descriptor = -1
    staging_identity: tuple[int, int] | None = None
    try:
        descriptor = os.open(
            staging_name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400, dir_fd=parent_descriptor,
        )
        opened = os.fstat(descriptor)
        staging_identity = (opened.st_dev, opened.st_ino)
        offset = 0
        while offset < len(data):
            written = os.write(descriptor, data[offset:])
            if written <= 0:
                raise Refusal("short hostile history write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        sealed = os.fstat(descriptor)
        if (
            not stat.S_ISREG(sealed.st_mode)
            or sealed.st_mode & 0o222
            or sealed.st_size != len(data)
            or sealed.st_nlink != 1
            or (sealed.st_dev, sealed.st_ino) != staging_identity
            or descriptor_sha256(descriptor) != hashlib.sha256(data).hexdigest()
        ):
            raise Refusal("hostile history staging authentication failed")
        custody.verify_all()
        if _directory_identity(
            parent, parent_descriptor, "hostile history",
        ) != parent_before:
            raise Refusal("hostile history parent identity changed before link")
        try:
            os.link(
                staging_name, path.name,
                src_dir_fd=parent_descriptor, dst_dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileExistsError as error:
            raise Refusal("hostile history destination appeared before link") from error
        canonical_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        canonical = os.open(
            path.name, canonical_flags, dir_fd=parent_descriptor,
        )
        try:
            observed = os.fstat(canonical)
            observed_path = os.stat(
                path.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(observed.st_mode)
                or observed.st_mode & 0o222
                or observed.st_nlink != 2
                or (observed.st_dev, observed.st_ino)
                != staging_identity
                or (observed_path.st_dev, observed_path.st_ino)
                != staging_identity
                or descriptor_sha256(canonical)
                != hashlib.sha256(data).hexdigest()
            ):
                raise Refusal("hostile history canonical link authentication failed")
        finally:
            os.close(canonical)
        if not _unlink_owned_at(
            parent_descriptor, staging_name, staging_identity,
        ):
            raise Refusal("hostile history staging custody changed after link")
        fsync_directory(parent, parent_descriptor)
        if _directory_identity(
            parent, parent_descriptor, "hostile history",
        ) != parent_before:
            raise Refusal("hostile history parent identity changed after link")
        final_descriptor = os.open(
            path.name, canonical_flags, dir_fd=parent_descriptor,
        )
        try:
            final = os.fstat(final_descriptor)
            final_path = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(final.st_mode)
                or final.st_mode & 0o222
                or final.st_nlink != 1
                or final.st_size != len(data)
                or (final.st_dev, final.st_ino) != staging_identity
                or (final_path.st_dev, final_path.st_ino)
                != staging_identity
                or descriptor_sha256(final_descriptor)
                != hashlib.sha256(data).hexdigest()
            ):
                raise Refusal("hostile history final canonical custody mismatch")
        finally:
            os.close(final_descriptor)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
            descriptor = -1
        if staging_identity is not None:
            _unlink_owned_at(
                parent_descriptor, staging_name, staging_identity,
            )
        # A canonical inode is never removed after the no-clobber link.  Any
        # post-link failure leaves explicit, inspectable evidence and forces a
        # later run to refuse instead of deleting a potentially swapped path.
        raise
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(parent_descriptor)
    output, digest = custody.authenticate(
        path, f"published hostile L{record.get('L')} history",
    )
    if output != record or canonical_json_bytes(output) != data:
        raise Refusal("published hostile history canonical reopen mismatch")
    custody.verify_all()
    return digest


def hostile_edges(length: int) -> list[list[object]]:
    edges: list[list[object]] = []
    for site in reversed(range(length)):
        edges.append([length + site, length + (site + 1) % length, "rail_2"])
    for site in reversed(range(length)):
        edges.append([site, length + (site + 1) % length, "connector"])
    for site in reversed(range(length)):
        edges.append([site, (site + 1) % length, "rail_1"])
    return edges


def cache_specs(length: int) -> list[dict[str, object]]:
    specs: list[dict[str, object]] = []
    edge_count = 3 * length
    for q in range(length + 1):
        words = math.comb(2 * length, q)
        pairs = edge_count * (math.comb(2 * length - 2, q - 1) if q else 0)
        specs.extend([
            {"path": f"q_{q:02d}_words.u32", "dtype": "<u4", "shape": [words],
             "bytes": 4 * words, "kind": "operator", "q": q, "role": "words"},
            {"path": f"q_{q:02d}_offsets.u64", "dtype": "<u8",
             "shape": [edge_count + 1], "bytes": 8 * (edge_count + 1),
             "kind": "operator", "q": q, "role": "offsets"},
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
                    "path": f"event_{event:02d}_q_{q:02d}_{role}.i32",
                    "dtype": "<i4", "shape": [count], "bytes": 4 * count,
                    "kind": "admission", "event": event, "q": q, "role": role,
                })
    for event in range(length - 1):
        for q in range(event + 1):
            count = math.comb(event, q)
            for role in ("same", "added"):
                specs.append({
                    "path": f"prefix_{event:02d}_q_{q:02d}_{role}.i32",
                    "dtype": "<i4", "shape": [count], "bytes": 4 * count,
                    "kind": "lineage", "event": event, "q": q, "role": role,
                })
    return specs


def storage_census(length: int) -> dict[str, int]:
    specs = cache_specs(length)
    actual = sum(int(row["bytes"]) for row in specs)
    offsets = sum(int(row["bytes"]) for row in specs if row["role"] == "offsets")
    dimensions = [
        sum(math.comb(prefix, q) * math.comb(2 * length, q)
            for q in range(prefix + 1))
        for prefix in range(length)
    ]
    state = 16 * max(
        dimensions[index] + dimensions[index + 1]
        for index in range(length - 1)
    )
    maximum_q_cache_plus_admission = max(
        operator_q_bytes(length, q) + 4 * math.comb(2 * length, q)
        + (8 * math.comb(2 * length - 1, q) if q < length else 0)
        for q in range(length + 1)
    )
    terminal_mapping = max(
        operator_q_bytes(length, q + 1)
        + carrier_word_bytes(length, q)
        + admission_pair_bytes(length, q)
        for q in range(length)
    )
    authentication_peak = (
        sum(carrier_word_bytes(length, q) for q in range(length + 1))
        + max(
            operator_q_bytes(length, q) - carrier_word_bytes(length, q)
            for q in range(length + 1)
        )
        + max(admission_pair_bytes(length, q) for q in range(length))
    )
    return {
        "raw_cache_bytes_excluding_offsets": actual - offsets,
        "offset_bytes": offsets,
        "actual_cache_array_bytes": actual,
        "maximum_live_state_bytes": state,
        "state_plus_actual_cache_bytes": state + actual,
        "array_file_count": len(specs),
        "state_cache_plus_reserve_bytes": state + actual + OVERHEAD_RESERVE,
        "maximum_q12_cache_plus_admission_bytes": maximum_q_cache_plus_admission,
        "terminal_mapping_bytes": terminal_mapping,
        "authentication_peak_bytes": authentication_peak,
    }


def operator_q_bytes(length: int, q: int) -> int:
    pairs = 3 * length * (math.comb(2 * length - 2, q - 1) if q else 0)
    return 4 * math.comb(2 * length, q) + 8 * (3 * length + 1) + 8 * pairs


def carrier_word_bytes(length: int, q: int) -> int:
    return 4 * math.comb(2 * length, q)


def admission_pair_bytes(length: int, q: int) -> int:
    return 8 * math.comb(2 * length - 1, q)


class CacheContext(r2consumer.SecureCacheContext):
    """V004R4-rooted stable cache using the hostile semantic implementation."""

    @staticmethod
    def _close(array: np.ndarray) -> None:
        """Close each semantic or production mapping at most once."""
        mapping = getattr(array, "_mmap", None)
        if mapping is not None and getattr(mapping, "closed", False):
            return
        r2consumer.SecureCacheContext._close(array)

    def __init__(
        self, length: int, root: Path, manifest: dict[str, Any], expected_manifest_hash: str,
        source_hashes: dict[str, str], started: float,
    ) -> None:
        self.length = length
        self.root = root
        self.started = started
        self.manifest_hash = expected_manifest_hash
        self.root_fd = -1
        self.fds: dict[str, int] = {}
        self.fingerprints: dict[
            str, tuple[int, int, int, int, int, int, int]
        ] = {}
        self.mappings: list[np.memmap] = []
        expected_root = HERE / f"V004R4_CACHE_PAYLOADS/L{length}"
        if (
            root != expected_root or not root.is_absolute()
            or str(Path(str(root))) != str(root)
        ):
            raise Refusal("V004R4 cache root is not exact canonical authority")
        _require_no_symlink_parents(
            root / "placeholder", "V004R4 cache root",
        )
        flags = (
            os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        self.root_fd = os.open(self.root, flags)
        metadata = os.fstat(self.root_fd)
        current_root = os.stat(self.root, follow_symlinks=False)
        self.root_identity = _file_identity(metadata)
        if (
            not stat.S_ISDIR(metadata.st_mode) or metadata.st_mode & 0o222
            or _file_identity(current_root) != self.root_identity
        ):
            raise Refusal("V004R4 cache root is not immutable")
        expected_names = [row["path"] for row in cache_specs(length)] + ["CACHE_MANIFEST.json"]
        if sorted(os.listdir(self.root_fd)) != sorted(expected_names):
            raise Refusal("V004R4 cache exact member census mismatch")
        manifest_fd = self._stable_open("CACHE_MANIFEST.json", None)
        manifest_size = os.fstat(manifest_fd).st_size
        manifest_bytes = _descriptor_bytes(
            manifest_fd, manifest_size, "V004R4 manifest",
        )
        if hashlib.sha256(manifest_bytes).hexdigest() != expected_manifest_hash:
            raise Refusal("V004R4 cache manifest descriptor hash mismatch")
        self._verify_fd("CACHE_MANIFEST.json")
        if strict_json_object(manifest_bytes, "V004R4 manifest") != manifest:
            raise Refusal("V004R4 cache manifest descriptor/content mismatch")
        self.manifest = manifest
        self._validate_v004r4_manifest(source_hashes)
        for record in manifest["files"]:
            descriptor = self._stable_open(record["path"], record["bytes"])
            if r2consumer._fd_sha256(descriptor, record["bytes"]) != record["sha256"]:
                raise Refusal(f"V004R4 cache member hash mismatch: {record['path']}")
            self._verify_fd(record["path"])
        self.records = {row["path"]: row for row in manifest["files"]}
        self.edges = physical.hostile_edges(length)
        try:
            self._authenticate_semantics()
        except r2consumer.common.Refusal as error:
            raise Refusal(str(error)) from error

    def _stable_open(self, name: str, expected_size: int | None) -> int:
        if (
            type(name) is not str or not name or Path(name).name != name
            or "/" in name or "\x00" in name or name in self.fds
        ):
            raise Refusal("V004R4 cache member name/open census mismatch")
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(name, flags, dir_fd=self.root_fd)
        try:
            opened = os.fstat(descriptor)
            current = os.stat(
                name, dir_fd=self.root_fd, follow_symlinks=False,
            )
            identity = _file_identity(opened)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_mode & 0o222 or opened.st_nlink != 1
                or _file_identity(current) != identity
                or (expected_size is not None and opened.st_size != expected_size)
            ):
                raise Refusal(f"V004R4 cache member custody mismatch: {name}")
            self.fds[name] = descriptor
            self.fingerprints[name] = identity
            return descriptor
        except BaseException:
            os.close(descriptor)
            raise

    def _verify_fd(self, name: str) -> None:
        identity = self.fingerprints[name]
        opened = os.fstat(self.fds[name])
        current = os.stat(
            name, dir_fd=self.root_fd, follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(opened.st_mode)
            or opened.st_mode & 0o222 or opened.st_nlink != 1
            or _file_identity(opened) != identity
            or _file_identity(current) != identity
        ):
            raise Refusal(f"V004R4 cache member changed: {name}")

    def _validate_v004r4_manifest(self, source_hashes: dict[str, str]) -> None:
        keys = {
            "schema", "status", "L", "basis_order", "lineage_identity",
            "edge_layout", "hamiltonian_exchange_coefficient", "files",
            "array_file_count", "manifest_inclusive_file_count", "payload",
            "method_sha256", "builder_sha256", "consumer_sha256", "preflight_sha256",
            "freeze_sha256", "preflight_result_sha256",
            "independent_hostile_audit_sha256",
            "cache_build_authorization_gate_sha256", "postbuild_payload_audit",
            "canonical_cache_root", "claim_boundary",
        }
        specs = cache_specs(self.length)
        expected_postbuild = ({
            "path": str(HERE / "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"),
            "schema": "HOSTILE_V004R4_POSTBUILD_PAYLOAD_AUDIT_V001",
            "identity_field": "classification",
            "identity_value": "PASS_HOSTILE_V004R4_L12_STORAGE_CACHE",
        } if self.length == 12 else None)
        if (
            set(self.manifest) != keys
            or self.manifest["schema"] != "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4"
            or self.manifest["status"] != "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE"
            or type(self.manifest["L"]) is not int or self.manifest["L"] != self.length
            or self.manifest["basis_order"] != "REVERSED_COMBINATION__FULL_MASK"
            or self.manifest["lineage_identity"] != "FULL_CANONICAL_MASK"
            or self.manifest["edge_layout"] != hostile_edges(self.length)
            or type(self.manifest["hamiltonian_exchange_coefficient"]) is not int
            or self.manifest["hamiltonian_exchange_coefficient"] != -1
            or self.manifest["array_file_count"] != len(specs)
            or self.manifest["manifest_inclusive_file_count"] != len(specs) + 1
            or self.manifest["payload"] != storage_census(self.length)
            or self.manifest["canonical_cache_root"] != str(self.root)
            or self.manifest["postbuild_payload_audit"] != expected_postbuild
            or self.manifest["claim_boundary"]
            != "HOSTILE_V004R4_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"
            or any(self.manifest[f"{role}_sha256"] != digest
                   for role, digest in source_hashes.items())
        ):
            raise Refusal("V004R4 cache manifest identity/lineage mismatch")
        for observed, expected in zip(self.manifest["files"], specs):
            if (
                type(observed) is not dict or set(observed) != set(expected) | {"sha256"}
                or {key: observed[key] for key in expected} != expected
                or not sha256_text(observed["sha256"])
            ):
                raise Refusal("V004R4 cache manifest member metadata mismatch")

    def reauthenticate(self) -> None:
        _require_no_symlink_parents(
            self.root / "placeholder", "V004R4 cache root",
        )
        root_opened = os.fstat(self.root_fd)
        root_current = os.stat(self.root, follow_symlinks=False)
        expected_names = set(self.fds)
        if (
            _file_identity(root_opened) != self.root_identity
            or _file_identity(root_current) != self.root_identity
            or root_opened.st_mode & 0o222
            or set(os.listdir(self.root_fd)) != expected_names
        ):
            raise Refusal("V004R4 cache root custody changed during history")
        for name, descriptor in self.fds.items():
            self._verify_fd(name)
            expected_hash = (
                self.manifest_hash if name == "CACHE_MANIFEST.json"
                else self.records[name]["sha256"]
            )
            if (
                r2consumer._fd_sha256(
                    descriptor, self.fingerprints[name][2],
                ) != expected_hash
            ):
                raise Refusal(f"V004R4 cache member changed during history: {name}")
            self._verify_fd(name)


def read_authority(
    custody: AuthorityCustody, path: Path, label: str,
    expected_digest: str | None = None,
) -> tuple[dict[str, Any], str]:
    value, digest = custody.authenticate(path, label, expected_digest)
    if value is None:
        raise Refusal(f"{label} is not JSON")
    return value, digest


def binding_record(
    custody: AuthorityCustody, binding: object, expected_path: Path, label: str,
) -> tuple[dict[str, Any], str]:
    row = exact_keys(binding, {"path", "sha256", "schema", "identity_field", "identity_value"}, label)
    if row["path"] != str(expected_path) or not sha256_text(row["sha256"]):
        raise Refusal(f"{label} canonical path/hash mismatch")
    record, digest = read_authority(custody, expected_path, label, row["sha256"])
    if (
        row["identity_field"] not in {"status", "classification"}
        or record.get("schema") != row["schema"]
        or record.get(row["identity_field"]) != row["identity_value"]
    ):
        raise Refusal(f"{label} bound identity mismatch")
    return record, digest


def authenticate_l10_context(custody: AuthorityCustody) -> dict[str, Any]:
    """Authenticate the acyclic pre-L10 chain without consulting its future gate."""
    freeze, freeze_hash = read_authority(custody, FREEZE, "hostile V004R4 freeze")
    primary_sources = {
        "method": METHOD, "builder": BUILDER, "consumer": CONSUMER,
        "preflight": PREFLIGHT,
    }
    canonical_sources = {**primary_sources, **EXECUTED_DEPENDENCIES}
    hashes: dict[str, str] = {"freeze": freeze_hash}
    expected_files: dict[str, str] = {}
    for role, path in canonical_sources.items():
        expected = freeze.get("files", {}).get(path.name)
        if not sha256_text(expected):
            raise Refusal(f"hostile freeze omits {role}")
        _unused, hashes[role] = custody.authenticate(
            path, f"hostile V004R4 {role}", expected,
        )
        expected_files[path.name] = hashes[role]
    if (
        freeze.get("schema") != "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4"
        or freeze.get("status") != "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT"
        or freeze.get("files") != expected_files
        or freeze.get("cache_payload_created") is not False
        or freeze.get("physical_history_executed") is not False
        or freeze.get("claim_boundary")
        != "V004R4_CROSS_BRANCH_STORAGE_CONTROL_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"
    ):
        raise Refusal("hostile V004R4 freeze/source mismatch")

    preflight, hashes["preflight_result"] = read_authority(
        custody, PREFLIGHT_RESULT, "hostile V004R4 preflight result",
    )
    audit, hashes["independent_audit"] = read_authority(
        custody, INDEPENDENT_AUDIT, "hostile V004R4 independent audit",
    )
    if (
        preflight.get("schema") != "HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT_V001"
        or preflight.get("classification") != "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT"
        or preflight.get("files") != {
            "method_sha256": hashes["method"],
            "builder_sha256": hashes["builder"],
            "consumer_sha256": hashes["consumer"],
            "preflight_sha256": hashes["preflight"],
            "freeze_sha256": hashes["freeze"],
        }
        or preflight.get("checks_passed") != preflight.get("checks_total")
        or preflight.get("failures") != []
        or preflight.get("cache_payload_created") is not False
        or preflight.get("physical_history_executed") is not False
    ):
        raise Refusal("hostile V004R4 preflight mismatch")
    validate_hostile_prepayload_audit(
        audit, freeze_sha256=hashes["freeze"], frozen_files=expected_files,
        preflight_result_sha256=hashes["preflight_result"],
    )

    manifest_path = HERE / "V004R4_CACHE_PAYLOADS/L10/CACHE_MANIFEST.json"
    manifest, hashes["L10_cache_manifest"] = read_authority(
        custody, manifest_path, "hostile V004R4 L10 cache manifest",
    )
    source_hashes = {role: hashes[role] for role in primary_sources}
    if (
        manifest.get("L") != 10
        or manifest.get("freeze_sha256") != hashes["freeze"]
        or manifest.get("preflight_result_sha256") != hashes["preflight_result"]
        or manifest.get("independent_hostile_audit_sha256") != hashes["independent_audit"]
        or any(manifest.get(f"{role}_sha256") != digest
               for role, digest in source_hashes.items())
    ):
        raise Refusal("hostile V004R4 L10 manifest lineage mismatch")
    build_gate, build_hash = read_authority(
        custody, CACHE_BUILD_AUTHORIZATION, "hostile V004R4 build authorization",
        manifest.get("cache_build_authorization_gate_sha256"),
    )
    validate_hostile_build_authorization(
        build_gate, audit, freeze_sha256=hashes["freeze"],
        frozen_files=expected_files, audit_sha256=hashes["independent_audit"],
    )
    retain_build_authorization_inputs(custody, build_gate)

    authorization, authorization_hash = read_authority(
        custody, L10_EXECUTION_AUTHORIZATION,
        "hostile V004R4 L10 execution authorization",
    )
    expected_authorization = {
        "schema": "HOSTILE_V004R4_L10_EXECUTION_AUTHORIZATION_GATE_V001",
        "classification": "AUTHORIZE_AUDITED_HOSTILE_V004R4_L10",
        "role": "hostile_v004r4", "authorized_length": 10,
        "l10_cache_manifest_sha256": hashes["L10_cache_manifest"],
        "consumer_sha256": hashes["consumer"], "builder_sha256": hashes["builder"],
        "method_sha256": hashes["method"], "freeze_sha256": hashes["freeze"],
        "preflight_result_sha256": hashes["preflight_result"],
        "independent_hostile_audit_sha256": hashes["independent_audit"],
        "claim_boundary": "FINITE_HOSTILE_V004R4_L10_AUTHORIZATION_ONLY__NO_L12_OR_RESULT",
    }
    if authorization != expected_authorization:
        raise Refusal("hostile V004R4 L10 authorization mismatch")
    return {
        "manifest": manifest, "hashes": hashes, "source_hashes": source_hashes,
        "cache_build_authorization_gate_sha256": build_hash,
        "l10_execution_authorization_gate_sha256": authorization_hash,
    }


def authenticate_context(
    custody: AuthorityCustody, worker_id: str,
    session: OrchestratedWorkerSession | None = None,
) -> dict[str, Any]:
    if session is None or worker_id != session.worker_id:
        raise Refusal("hostile L12 authenticated orchestrator session absent")
    cross, cross_hash = read_authority(custody, L10_CROSS_GATE, "target/hostile L10 cross gate")
    if (
        cross.get("schema") != "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001"
        or cross.get("classification") != "PASS_EXACT_TARGET_HOSTILE_L10_CROSS_BENCHMARK"
        or cross.get("L") != 10 or type(cross.get("L")) is not int
        or cross.get("failures") != []
        or cross.get("checks_passed") != cross.get("checks_total")
    ):
        raise Refusal("target/hostile L10 cross gate is not an exact all-pass result")
    hostile_projection = exact_keys(
        cross.get("hostile"),
        {"branch", "cached_L10_gate_sha256", "l10_execution_authorization_gate_sha256",
         "independent_prepayload_audit_sha256", "history_sha256"},
        "hostile L10 cross projection",
    )
    branch = exact_keys(
        hostile_projection["branch"],
        {"role", "method", "builder", "consumer", "preflight", "freeze",
         "preflight_result", "independent_audit", "cached_L10_gate", "L12_cache_manifest"},
        "hostile branch",
    )
    if branch["role"] != "hostile_v004r4":
        raise Refusal("hostile branch role mismatch")
    canonical = {
        "method": METHOD, "builder": BUILDER, "consumer": CONSUMER,
        "preflight": PREFLIGHT, "freeze": FREEZE,
        "preflight_result": PREFLIGHT_RESULT, "independent_audit": INDEPENDENT_AUDIT,
        "cached_L10_gate": CACHED_L10_GATE,
        "L12_cache_manifest": CACHE_ROOT / "CACHE_MANIFEST.json",
    }
    records: dict[str, dict[str, Any]] = {}
    hashes: dict[str, str] = {}
    for role, path in canonical.items():
        binding = branch[role]
        if role in {"method", "builder", "consumer", "preflight"}:
            row = exact_keys(binding, {"path", "sha256"}, f"hostile {role}")
            if row["path"] != str(path) or not sha256_text(row["sha256"]):
                raise Refusal(f"hostile {role} binding mismatch")
            _unused, hashes[role] = custody.authenticate(path, f"hostile {role}", row["sha256"])
        else:
            records[role], hashes[role] = binding_record(
                custody, binding, path, f"hostile {role}",
            )
    freeze = records["freeze"]
    expected_files = {
        METHOD.name: hashes["method"], BUILDER.name: hashes["builder"],
        CONSUMER.name: hashes["consumer"], PREFLIGHT.name: hashes["preflight"],
    }
    for name, path in EXECUTED_DEPENDENCIES.items():
        expected = freeze.get("files", {}).get(name)
        if not sha256_text(expected):
            raise Refusal(f"hostile freeze omits executed dependency {name}")
        _unused, hashes[name] = custody.authenticate(
            path, f"hostile executed dependency {name}", expected,
        )
        expected_files[name] = hashes[name]
    if (
        freeze.get("schema") != "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4"
        or freeze.get("status") != "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT"
        or freeze.get("files") != expected_files
        or freeze.get("cache_payload_created") is not False
        or freeze.get("physical_history_executed") is not False
    ):
        raise Refusal("hostile V004R4 freeze/source census mismatch")
    preflight = records["preflight_result"]
    audit = records["independent_audit"]
    cached_l10 = records["cached_L10_gate"]
    if (
        preflight.get("classification") != "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT"
        or preflight.get("files") != {
            "method_sha256": hashes["method"], "builder_sha256": hashes["builder"],
            "consumer_sha256": hashes["consumer"], "preflight_sha256": hashes["preflight"],
            "freeze_sha256": hashes["freeze"],
        }
        or cached_l10.get("schema") != "HOSTILE_V004R4_CACHED_L10_GATE"
        or cached_l10.get("classification") != "PASS_HOSTILE_V004R4_CACHED_L10"
        or cached_l10.get("consumer_sha256") != hashes["consumer"]
        or cached_l10.get("freeze_sha256") != hashes["freeze"]
        or cached_l10.get("independent_hostile_audit_sha256") != hashes["independent_audit"]
        or hashes["cached_L10_gate"] != hostile_projection["cached_L10_gate_sha256"]
        or hashes["independent_audit"]
        != hostile_projection["independent_prepayload_audit_sha256"]
    ):
        raise Refusal("hostile V004R4 preflight/audit lineage mismatch")
    validate_hostile_prepayload_audit(
        audit, freeze_sha256=hashes["freeze"], frozen_files=expected_files,
        preflight_result_sha256=hashes["preflight_result"],
    )
    manifest = records["L12_cache_manifest"]
    source_hashes = {role: hashes[role] for role in ("method", "builder", "consumer", "preflight")}
    if (
        manifest.get("freeze_sha256") != hashes["freeze"]
        or manifest.get("preflight_result_sha256") != hashes["preflight_result"]
        or manifest.get("independent_hostile_audit_sha256") != hashes["independent_audit"]
        or any(manifest.get(f"{role}_sha256") != digest for role, digest in source_hashes.items())
    ):
        raise Refusal("hostile V004R4 cache manifest source lineage mismatch")
    build_gate, build_hash = read_authority(
        custody, CACHE_BUILD_AUTHORIZATION, "hostile cache build authorization",
        manifest.get("cache_build_authorization_gate_sha256"),
    )
    validate_hostile_build_authorization(
        build_gate, audit, freeze_sha256=hashes["freeze"],
        frozen_files=expected_files, audit_sha256=hashes["independent_audit"],
    )
    retain_build_authorization_inputs(custody, build_gate)
    postbuild_binding = exact_keys(
        manifest.get("postbuild_payload_audit"),
        {"path", "schema", "identity_field", "identity_value"},
        "hostile postbuild payload audit binding",
    )
    postbuild_path = HERE / "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"
    if postbuild_binding != {
        "path": str(postbuild_path),
        "schema": "HOSTILE_V004R4_POSTBUILD_PAYLOAD_AUDIT_V001",
        "identity_field": "classification",
        "identity_value": "PASS_HOSTILE_V004R4_L12_STORAGE_CACHE",
    }:
        raise Refusal("hostile postbuild payload audit preregistration mismatch")
    postbuild, postbuild_hash = read_authority(
        custody, postbuild_path, "hostile postbuild payload audit",
    )
    if (
        postbuild.get("classification") != "PASS_HOSTILE_V004R4_L12_STORAGE_CACHE"
        or postbuild.get("manifest_sha256") != hashes["L12_cache_manifest"]
        or postbuild.get("checks_passed") != postbuild.get("checks_total")
        or postbuild.get("failures") != []
        or postbuild.get("physical_history_executed") is not False
    ):
        raise Refusal("hostile postbuild payload audit mismatch")
    l10_authorization, l10_authorization_hash = read_authority(
        custody, L10_EXECUTION_AUTHORIZATION, "hostile L10 authorization",
        hostile_projection["l10_execution_authorization_gate_sha256"],
    )
    if (
        l10_authorization.get("classification") != "AUTHORIZE_AUDITED_HOSTILE_V004R4_L10"
        or l10_authorization.get("authorized_length") != 10
        or l10_authorization.get("consumer_sha256") != hashes["consumer"]
    ):
        raise Refusal("hostile L10 authorization mismatch")
    schedule, schedule_hash = read_authority(custody, SCHEDULE_GATE, "shared L12 schedule")
    exact_keys(schedule, {
        "schema", "classification", "created_epoch", "expires_epoch",
        "l10_cross_gate_sha256", "resource_snapshot", "schedule", "roles",
        "telemetry", "claim_boundary",
    }, "shared L12 schedule")
    snapshot = exact_keys(schedule["resource_snapshot"], {
        "captured_epoch", "host_physical_memory_bytes", "available_memory_bytes",
        "workspace_free_disk_bytes", "workspace_filesystem_device",
        "both_workspace_roots_same_filesystem", "memory_pressure", "passes",
    }, "shared L12 resource snapshot")
    created = schedule["created_epoch"]
    expires = schedule["expires_epoch"]
    if (
        schedule["schema"] != "V012_DUAL_L12_READINESS_SCHEDULE_V001"
        or schedule["classification"] != "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT"
        or schedule["l10_cross_gate_sha256"] != cross_hash
        or not positive_integer(created) or not positive_integer(expires)
        or not 0 < expires - created <= 300
        or not created <= session.ready["ready_epoch"] <= expires
        or any(not positive_integer(snapshot[key]) for key in (
            "captured_epoch", "host_physical_memory_bytes", "available_memory_bytes",
            "workspace_free_disk_bytes", "workspace_filesystem_device",
        ))
        or not created <= snapshot["captured_epoch"] <= expires
        or snapshot["host_physical_memory_bytes"] < 48_000_000_000
        or snapshot["available_memory_bytes"] < 34_865_626_528
        or snapshot["workspace_free_disk_bytes"] < 19_201_889_580
        or snapshot["both_workspace_roots_same_filesystem"] is not True
        or type(snapshot["both_workspace_roots_same_filesystem"]) is not bool
        or snapshot["memory_pressure"] != "NORMAL"
        or snapshot["passes"] is not True or type(snapshot["passes"]) is not bool
        or schedule["schedule"] != {
            "launch_mode": "PRELAUNCHED_BLOCKED_TWO_WORKER",
            "release_only_after_both_l12_authorizations": True,
            "launch_skew_seconds_max": 60,
            "per_process_rss_limit_bytes": RSS_LIMIT,
            "per_process_wall_limit_seconds": 108_000,
            "mapped_peak_limit_bytes_by_role": {
                "target_v012": EXPECTED_AUTHENTICATION_PEAK_BYTES,
                "hostile_v004r4": EXPECTED_AUTHENTICATION_PEAK_BYTES,
            },
        }
        or schedule["roles"] != {
            "target_v012": {
                "role": "target_v012",
                "worker_executable_path": str(
                    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
                ),
                "workspace_path": str(
                    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L12"
                ),
                "output_path": str(
                    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json"
                ),
                "ready_for_blocked_worker_start": True,
            },
            "hostile_v004r4": {
                "role": "hostile_v004r4", "worker_executable_path": str(CONSUMER),
                "workspace_path": str(WORKSPACE), "output_path": str(OUTPUT),
                "ready_for_blocked_worker_start": True,
            },
        }
        or schedule["telemetry"] != {
            "path": str(TELEMETRY),
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "must_be_absent_before_release": True,
            "absent_at_schedule_capture": True,
            "sample_interval_seconds_max": 60,
        }
        or schedule["claim_boundary"]
        != "READINESS_AND_RESOURCE_SCHEDULING_ONLY__NO_L12_RELEASE_OR_RESULT"
        or TELEMETRY.exists()
    ):
        raise Refusal("shared L12 schedule mismatch/expired")
    schedule_audit, schedule_audit_hash = read_authority(
        custody, SCHEDULE_AUDIT, "shared L12 schedule audit",
    )
    exact_keys(schedule_audit, {
        "schema", "classification", "auditor_role", "schedule_sha256",
        "l10_cross_gate_sha256", "checks", "checks_total", "checks_passed",
        "failures", "claim_boundary",
    }, "shared L12 schedule audit")
    expected_schedule_checks = {
        "schedule_exact_schema": 1, "deep_exact_types": 1,
        "two_role_path_custody": 2, "normal_memory_pressure": 1,
        "resource_thresholds": 4, "freshness_window": 1,
        "telemetry_prelaunch_absence": 1,
    }
    if (
        schedule_audit["schema"] != "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001"
        or schedule_audit["classification"]
        != "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT"
        or schedule_audit["auditor_role"]
        != "INDEPENDENT_DUAL_LAUNCH_COORDINATOR_REVIEW"
        or schedule_audit["schedule_sha256"] != schedule_hash
        or schedule_audit["l10_cross_gate_sha256"] != cross_hash
        or schedule_audit["checks"] != expected_schedule_checks
        or type(schedule_audit["checks_total"]) is not int
        or schedule_audit["checks_total"] != sum(expected_schedule_checks.values())
        or type(schedule_audit["checks_passed"]) is not int
        or schedule_audit["checks_passed"] != schedule_audit["checks_total"]
        or schedule_audit["failures"] != []
        or schedule_audit["claim_boundary"]
        != "INDEPENDENT_READINESS_AUDIT_ONLY__NO_L12_AUTHORIZATION_RELEASE_OR_RESULT"
    ):
        raise Refusal("shared L12 schedule audit mismatch")
    authorization, authorization_hash = read_authority(
        custody, HOSTILE_L12_AUTHORIZATION, "hostile L12 authorization",
    )
    expected_authorization = {
        "schema": "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001",
        "classification": "AUTHORIZE_HOSTILE_V004R4_L12_AFTER_SCHEDULE_AUDIT",
        "role": "hostile_v004r4", "authorized_length": 12,
        "schedule_sha256": schedule_hash,
        "schedule_audit_sha256": schedule_audit_hash,
        "l10_cross_gate_sha256": cross_hash,
        "consumer_sha256": hashes["consumer"],
        "l12_cache_manifest_sha256": hashes["L12_cache_manifest"],
        "claim_boundary": "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT",
    }
    if authorization != expected_authorization:
        raise Refusal("hostile L12 one-way authorization mismatch")
    handshake, handshake_hash = wait_authority(
        custody, HANDSHAKE, "dual L12 handshake", schedule["expires_epoch"],
    )
    exact_keys(handshake, {
        "schema", "classification", "created_epoch", "schedule_sha256",
        "schedule_audit_sha256", "authorization_sha256_by_role",
        "memory_pressure", "workers", "ready_sha256_by_role",
        "observed_readiness_skew_seconds", "launch_skew_seconds_max",
        "telemetry", "claim_boundary",
    }, "dual L12 handshake")
    if not positive_integer(handshake["created_epoch"]):
        raise Refusal("dual L12 handshake creation epoch mismatch")
    handshake_authorizations = exact_keys(
        handshake["authorization_sha256_by_role"],
        {"target_v012", "hostile_v004r4"},
        "dual L12 handshake authorizations",
    )
    auth_hashes = {
        "target_v012": handshake_authorizations["target_v012"],
        "hostile_v004r4": authorization_hash,
    }
    workers = exact_keys(
        handshake["workers"], {"target_v012", "hostile_v004r4"},
        "dual L12 handshake workers",
    )
    ready_hashes = exact_keys(
        handshake["ready_sha256_by_role"], {"target_v012", "hostile_v004r4"},
        "dual L12 READY hashes",
    )
    target_executable = (
        ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
    )
    expected_worker_paths = {
        "target_v012": (
            target_executable,
            ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L12",
            ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json",
        ),
        "hostile_v004r4": (CONSUMER, WORKSPACE, OUTPUT),
    }
    ready_epochs: dict[str, int] = {}
    for role, (executable, workspace, output) in expected_worker_paths.items():
        ready = exact_keys(
            workers[role], OrchestratedWorkerSession.READY_KEYS,
            f"dual L12 {role} READY",
        )
        if (
            ready["schema"] != READY_SCHEMA or ready["role"] != role
            or type(ready["worker_id"]) is not str or not ready["worker_id"]
            or not positive_integer(ready["process_id"])
            or ready["process_start_token"] != process_start_token(ready["process_id"])
            or ready["executable_path"] != str(executable)
            or ready["workspace_path"] != str(workspace)
            or ready["output_path"] != str(output)
            or not sha256_text(ready["executable_sha256"])
            or not sha256_text(ready["control_channel_id"])
            or not sha256_text(ready["nonce_commitment_sha256"])
            or ready["blocked_on_release"] is not True
            or type(ready["blocked_on_release"]) is not bool
            or not positive_integer(ready["ready_epoch"])
            or not schedule["created_epoch"] <= ready["ready_epoch"] <= handshake["created_epoch"]
            or ready_hashes[role]
            != hashlib.sha256(canonical_json_bytes(ready)).hexdigest()
        ):
            raise Refusal(f"dual L12 {role} READY mismatch")
        _unused, executable_hash = custody.authenticate_or_reuse(
            executable, f"dual L12 {role} executable",
            ready["executable_sha256"],
        )
        if executable_hash != ready["executable_sha256"]:
            raise Refusal(f"dual L12 {role} executable hash mismatch")
        ready_epochs[role] = ready["ready_epoch"]
    validate_cross_role_identity_distinctness(workers, auth_hashes)
    worker = workers["hostile_v004r4"]
    readiness_skew = abs(ready_epochs["target_v012"] - ready_epochs["hostile_v004r4"])
    if (
        handshake["schema"] != "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002"
        or handshake.get("classification")
        != "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS"
        or not positive_integer(handshake["created_epoch"])
        or not schedule["created_epoch"] <= handshake["created_epoch"] <= schedule["expires_epoch"]
        or handshake.get("schedule_sha256") != schedule_hash
        or handshake.get("schedule_audit_sha256") != schedule_audit_hash
        or handshake.get("authorization_sha256_by_role") != auth_hashes
        or not sha256_text(auth_hashes["target_v012"])
        or worker != session.ready
        or ready_hashes["hostile_v004r4"] != session.ready_sha256
        or handshake["memory_pressure"] != "NORMAL"
        or handshake["observed_readiness_skew_seconds"] != readiness_skew
        or type(handshake["observed_readiness_skew_seconds"]) is not int
        or readiness_skew > 60
        or handshake["launch_skew_seconds_max"] != 60
        or type(handshake["launch_skew_seconds_max"]) is not int
        or handshake["telemetry"] != {
            "path": str(TELEMETRY),
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "absent_before_release": True,
        }
        or handshake["claim_boundary"]
        != "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT"
        or TELEMETRY.exists()
    ):
        raise Refusal("dual L12 hostile worker handshake mismatch")
    release, release_hash = wait_authority(
        custody, WORKER_RELEASE, "dual L12 worker release", schedule["expires_epoch"],
    )
    exact_keys(release, {
        "schema", "classification", "handshake_sha256",
        "authorization_sha256_by_role", "release_epoch_by_role",
        "observed_launch_skew_seconds", "release_by_role", "claim_boundary",
    }, "dual L12 worker release")
    release_rows = exact_keys(
        release["release_by_role"], {"target_v012", "hostile_v004r4"},
        "dual L12 worker release roles",
    )
    release_epochs = exact_keys(
        release["release_epoch_by_role"], {"target_v012", "hostile_v004r4"},
        "dual L12 worker release epochs",
    )
    if any(not positive_integer(epoch) for epoch in release_epochs.values()):
        raise Refusal("dual L12 worker release epoch type mismatch")
    release_row = release_rows["hostile_v004r4"]
    release_epoch = release_epochs["hostile_v004r4"]
    expected_token = hashlib.sha256(
        f"{handshake_hash}:hostile_v004r4:{release_epoch}".encode("ascii")
    ).hexdigest()
    for role in ("target_v012", "hostile_v004r4"):
        row = exact_keys(release_rows[role], {
            "role", "worker_id", "process_id", "process_start_token",
            "control_channel_id", "nonce_commitment_sha256",
            "release_token_sha256",
        }, f"dual L12 {role} release")
        ready = workers[role]
        token = hashlib.sha256(
            f"{handshake_hash}:{role}:{release_epochs[role]}".encode("ascii")
        ).hexdigest()
        if row != {
            "role": role, "worker_id": ready["worker_id"],
            "process_id": ready["process_id"],
            "process_start_token": ready["process_start_token"],
            "control_channel_id": ready["control_channel_id"],
            "nonce_commitment_sha256": ready["nonce_commitment_sha256"],
            "release_token_sha256": token,
        }:
            raise Refusal(f"dual L12 {role} release/READY mismatch")
    release_skew = abs(release_epochs["target_v012"] - release_epochs["hostile_v004r4"])
    if (
        release["schema"] != "V012_DUAL_L12_WORKER_RELEASE_V002"
        or release.get("classification") != "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS"
        or release.get("handshake_sha256") != handshake_hash
        or release.get("authorization_sha256_by_role") != auth_hashes
        or set(release.get("release_by_role", {})) != {"target_v012", "hostile_v004r4"}
        or set(release.get("release_epoch_by_role", {})) != {"target_v012", "hostile_v004r4"}
        or release_row["release_token_sha256"] != expected_token
        or type(release_epoch) is not int
        or not handshake["created_epoch"] <= release_epoch <= schedule["expires_epoch"]
        or any(
            type(epoch) is not int
            or not handshake["created_epoch"] <= epoch <= schedule["expires_epoch"]
            for epoch in release_epochs.values()
        )
        or type(release["observed_launch_skew_seconds"]) is not int
        or release["observed_launch_skew_seconds"] != release_skew
        or release_skew > 60
        or release["claim_boundary"] != "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT"
        or TELEMETRY.exists()
    ):
        raise Refusal("dual L12 hostile worker release mismatch")
    if session.release is None:
        raise Refusal("hostile orchestrated release command absent")
    if (
        session.release["handshake_sha256"] != handshake_hash
        or session.release["worker_release_sha256"] != release_hash
        or session.release["release_epoch"] != release_epoch
        or any(
            session.release[field] != release_row[field]
            for field in (
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id", "nonce_commitment_sha256",
            )
        )
    ):
        raise Refusal("hostile wire/file release binding mismatch")
    return {
        "branch": branch, "records": records, "hashes": hashes,
        "manifest": manifest, "source_hashes": source_hashes,
        "cache_build_authorization_gate_sha256": build_hash,
        "postbuild_payload_audit_sha256": postbuild_hash,
        "l10_execution_authorization_gate_sha256": l10_authorization_hash,
        "target_hostile_l10_cross_gate_sha256": cross_hash,
        "shared_aggregate_schedule_gate_sha256": schedule_hash,
        "shared_aggregate_schedule_gate_audit_sha256": schedule_audit_hash,
        "hostile_l12_execution_gate_sha256": authorization_hash,
        "dual_l12_launch_handshake_sha256": handshake_hash,
        "dual_l12_worker_release_sha256": release_hash,
    }


def wait_authority(
    custody: AuthorityCustody, path: Path, label: str, expires_epoch: int,
) -> tuple[dict[str, Any], str]:
    if type(expires_epoch) is not int or int(time.time()) > expires_epoch:
        raise Refusal(f"{label} schedule expired before authority read")
    while not path.exists():
        if int(time.time()) > expires_epoch:
            raise Refusal(f"{label} absent at schedule expiry")
        time.sleep(0.1)
    if int(time.time()) > expires_epoch:
        raise Refusal(f"{label} schedule expired before authority read")
    record = read_authority(custody, path, label)
    if int(time.time()) > expires_epoch:
        raise Refusal(f"{label} schedule expired during authority read")
    return record


def accuracy_record(value: physical.Accuracy) -> dict[str, object]:
    return {
        "label": value.label, "checkpoints": list(value.checkpoints),
        "quadrature_nodes": value.gauss_order, "tolerance": value.tolerance,
    }


def validate_solver(
    value: object, length: int, event: int, role: str,
) -> dict[str, Any]:
    expected_keys = SOLVER_TERMINAL_KEYS if event == length and role == "actual" else SOLVER_BASE_KEYS
    row = exact_keys(value, expected_keys, f"event {event} {role} solver")
    integer_keys = {
        "batches", "maximum_degree", "quadrature_group_max",
        "allocation_vector_slots", "maximum_allocation_estimate_bytes",
        "allocation_limit_bytes", "quadrature_nodes",
    }
    if (
        row["converged"] is not True or row["q_sharded"] is not True
        or row["algorithm"] != "RECURRENCE_REPLAY_GL_GROUPS"
        or any(type(row[key]) is not int or row[key] < 0 for key in integer_keys)
        or row["batches"] < 1
        or row["quadrature_nodes"] != 28
        or row["allocation_limit_bytes"] != NUMERICAL_WORKSPACE_LIMIT
        or row["maximum_allocation_estimate_bytes"] > NUMERICAL_WORKSPACE_LIMIT
        or not finite_float(row["maximum_endpoint_difference"])
        or not finite_float(row["maximum_tail_indicator_32"])
    ):
        raise Refusal(f"event {event} {role} native solver mismatch")
    if expected_keys == SOLVER_TERMINAL_KEYS and (
        row["terminal_children_streamed"] is not True
        or row["terminal_child0_entries"] != math.comb(3 * length - 1, length - 1)
        or row["terminal_child1_nonzero_admission_entries"] != math.comb(3 * length - 2, length - 1)
        or row["full_terminal_array_allocated"] is not False
    ):
        raise Refusal("terminal actual solver streaming certificate mismatch")
    return row


def validate_native_rows(rows: object, length: int) -> list[dict[str, Any]]:
    if type(rows) is not list or len(rows) != length:
        raise Refusal("hostile native history row census mismatch")
    for index, value in enumerate(rows):
        event = index + 1
        row = exact_keys(value, ROW_KEYS, f"hostile event {event}")
        if (
            type(row["event"]) is not int or row["event"] != event
            or type(row["input_prefix"]) is not int or row["input_prefix"] != index
            or type(row["input_prefix_dimension"]) is not int
            or row["input_prefix_dimension"] != math.comb(2 * length + index, index)
            or type(row["logical_output_prefix_dimension"]) is not int
            or row["logical_output_prefix_dimension"] != math.comb(2 * length + event, event)
            or row["terminal_children_streamed"] is not (event == length)
            or type(row["sector_weights"]) is not list
            or len(row["sector_weights"]) != length + 1
            or any(not finite_float(item) for item in row["sector_weights"])
        ):
            raise Refusal(f"hostile event {event} dimension/type mismatch")
        numeric = ROW_KEYS - {
            "event", "input_prefix", "input_prefix_dimension",
            "logical_output_prefix_dimension", "terminal_children_streamed",
            "sector_weights", "actual_solver", "null_solver",
        }
        if any(not finite_float(row[key]) for key in numeric):
            raise Refusal(f"hostile event {event} nonfinite/non-float observable")
        validate_solver(row["actual_solver"], length, event, "actual")
        validate_solver(row["null_solver"], length, event, "null")
    return rows


def validate_comparison(value: object, length: int) -> dict[str, Any]:
    row = exact_keys(value, COMPARISON_KEYS, "hostile rough/sharp comparison")
    if (
        row["resolved"] is not True
        or row["classification"] != "RESOLVED_PREFIX_HISTORY_CONTROL"
        or not finite_float(row["epsilon"]) or row["epsilon"] <= 0.0
        or any(type(row[key]) is not list or len(row[key]) != length
               or any(not finite_float(item) for item in row[key])
               for key in ("admission_acceptance", "routed_acceptance", "connector_ratio"))
    ):
        raise Refusal("hostile rough/sharp comparison unresolved/malformed")
    exact_keys(row["rough_sharp"], {"maximum_disagreement", "observable_linf", "sector_weight_linf"}, "rough/sharp")
    exact_keys(row["sector"], {"density_interval", "discarded_mass", "enclosed_mass", "late_events", "q_lower", "q_upper"}, "sector")
    canonical_json_bytes(row)
    return row


def seal_terminal_shards(
    length: int, workspace: Path, sharp: dict[str, Any], custody: AuthorityCustody,
) -> list[dict[str, object]]:
    rows = sharp.get("terminal_shards")
    if type(rows) is not list or len(rows) != length:
        raise Refusal("hostile terminal shard census mismatch")
    terminal_root = workspace / "sharp" / f"prefix_{length - 1:02d}"
    normalized: list[dict[str, object]] = []
    for q, native in enumerate(rows):
        expected_relative = f"prefix_{length - 1:02d}/q_{q:02d}.c128"
        shape = [math.comb(length - 1, q), math.comb(2 * length, q)]
        byte_count = 16 * math.prod(shape)
        if native != {"q": q, "path": expected_relative, "shape": shape, "logical_bytes": byte_count}:
            raise Refusal("hostile native terminal descriptor mismatch")
        path = (workspace / "sharp" / expected_relative).resolve()
        if path != (terminal_root / f"q_{q:02d}.c128") or path.is_symlink() or not path.is_file():
            raise Refusal("hostile terminal path escaped canonical workspace")
        if path.stat().st_size != byte_count:
            raise Refusal("hostile terminal byte size mismatch")
        path.chmod(0o444)
        _record, digest = custody.authenticate(path, f"hostile terminal q={q}")
        normalized.append({"q": q, "path": str(path), "shape": shape,
                           "bytes": byte_count, "sha256": digest})
    terminal_root.chmod(0o555)
    terminal_root.parent.chmod(0o555)
    workspace.chmod(0o555)
    for directory in (terminal_root, terminal_root.parent, workspace, workspace.parent):
        fsync_directory(directory)
    custody.verify_all()
    return normalized


def make_result(
    length: int, sharp: dict[str, Any], comparison: dict[str, Any],
    terminals: list[dict[str, object]],
    context: dict[str, Any], peak_state: int, allocation: int, rss: int, wall: float,
) -> dict[str, Any]:
    storage = storage_census(length)
    result: dict[str, Any] = {
        "schema": "HOSTILE_CACHED_PREFIX_HISTORY_V004R4", "L": length,
        "events": length, "dimension": math.comb(3 * length, length),
        "preterminal_dimension": math.comb(3 * length - 1, length - 1),
        "edges": 3 * length,
        "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_HOSTILE_INDEX_CACHE",
        "lineage_authority": "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING",
        "coarse_method": accuracy_record(physical.ROUGH),
        "fine_method": accuracy_record(physical.SHARP),
        "rows": sharp["rows"], "comparison": comparison,
        "terminal_shards": terminals,
        "cache_manifest_sha256": context["hashes"]["L12_cache_manifest"] if length == 12 else context["hashes"]["L10_cache_manifest"],
        "cache_build_authorization_gate_sha256": context["cache_build_authorization_gate_sha256"],
        "l10_execution_authorization_gate_sha256": context["l10_execution_authorization_gate_sha256"],
        "resource": {
            "peak_logical_state_plus_cache_bytes": (
                peak_state + storage["actual_cache_array_bytes"]
            ),
            "scratch_limit_bytes": SCRATCH_LIMIT,
            "maximum_numerical_allocation_estimate_bytes": allocation,
            "numerical_workspace_limit_bytes": NUMERICAL_WORKSPACE_LIMIT,
            "authentication_peak_certificate_bytes": storage["authentication_peak_bytes"],
            "peak_rss_bytes": rss, "rss_limit_bytes": RSS_LIMIT,
            "wall_seconds_including_authentication": wall,
            "wall_limit_seconds": WALL_LIMIT, "passed": True,
        },
        "consumer_sha256": context["hashes"]["consumer"],
        "builder_sha256": context["hashes"]["builder"],
        "method_sha256": context["hashes"]["method"],
        "preflight_sha256": context["hashes"]["preflight"],
        "freeze_sha256": context["hashes"]["freeze"],
        "preflight_result_sha256": context["hashes"]["preflight_result"],
        "independent_hostile_audit_sha256": context["hashes"]["independent_audit"],
        "claim_boundary": "FINITE_CACHED_HOSTILE_V004R4_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    }
    if length == 12:
        result.update({
            "postbuild_payload_audit_sha256": context["postbuild_payload_audit_sha256"],
            "target_hostile_l10_cross_gate_sha256": context["target_hostile_l10_cross_gate_sha256"],
            "shared_aggregate_schedule_gate_sha256": context["shared_aggregate_schedule_gate_sha256"],
            "shared_aggregate_schedule_gate_audit_sha256": context["shared_aggregate_schedule_gate_audit_sha256"],
            "hostile_l12_execution_gate_sha256": context["hostile_l12_execution_gate_sha256"],
            "dual_l12_launch_handshake_sha256": context["dual_l12_launch_handshake_sha256"],
            "dual_l12_worker_release_sha256": context["dual_l12_worker_release_sha256"],
        })
    expected_keys = HISTORY_KEYS if length == 12 else L10_HISTORY_KEYS
    if set(result) != expected_keys or set(result["resource"]) != RESOURCE_KEYS:
        raise Refusal("internal hostile result key census mismatch")
    validate_native_rows(result["rows"], length)
    validate_comparison(result["comparison"], length)
    if (
        peak_state != storage["maximum_live_state_bytes"]
        or result["resource"]["peak_logical_state_plus_cache_bytes"]
        != storage["state_plus_actual_cache_bytes"]
        or result["resource"]["peak_logical_state_plus_cache_bytes"] + OVERHEAD_RESERVE
        != storage["state_cache_plus_reserve_bytes"]
        or allocation > NUMERICAL_WORKSPACE_LIMIT
        or type(rss) is not int or not 0 < rss <= RSS_LIMIT
        or not finite_float(wall) or not 0.0 < wall <= WALL_LIMIT
        or sharp.get("full_dimension") != math.comb(3 * length, length)
        or sharp.get("largest_materialized_dimension")
        != math.comb(3 * length - 1, length - 1)
        or sharp.get("edge_layout") != hostile_edges(length)
    ):
        raise Refusal("hostile native result resource/dimension reconstruction mismatch")
    canonical_json_bytes(result)
    return result


def validate_with_independent_sink(
    result: dict[str, Any], custody: AuthorityCustody,
) -> None:
    if FINAL_AUDITOR.is_symlink() or not FINAL_AUDITOR.is_file():
        raise Refusal("independent A25 validator is absent")
    name = "v004r4_independent_final_auditor"
    _unused, digest = custody.authenticate(
        FINAL_AUDITOR, "independent A25 validator", FINAL_AUDITOR_SHA256,
    )
    retained = custody.files[FINAL_AUDITOR]
    raw = os.pread(retained.descriptor, retained.identity[2], 0)
    if hashlib.sha256(raw).hexdigest() != digest:
        raise Refusal("independent A25 validator descriptor drift")
    module = types.ModuleType(name)
    module.__file__ = str(FINAL_AUDITOR)
    sys.modules[name] = module
    exec(compile(raw, str(FINAL_AUDITOR), "exec"), module.__dict__)
    try:
        module.validate_hostile_l12_history(result, fixture_mode=False)
    except module.Refusal as error:
        raise Refusal(str(error)) from error


def execute_l10() -> None:
    length = 10
    cache_root = HERE / "V004R4_CACHE_PAYLOADS/L10"
    workspace = HERE / "V004R4_WORKSPACES/L10"
    output = HERE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json"
    if output.exists() or output.is_symlink() or workspace.exists() or workspace.is_symlink():
        raise Refusal("refuse to overwrite canonical hostile L10 history/workspace")
    custody = AuthorityCustody()
    cache: CacheContext | None = None
    started = time.perf_counter()
    try:
        context = authenticate_l10_context(custody)
        storage = storage_census(length)
        if shutil.disk_usage(existing_ancestor(workspace)).free < storage["state_cache_plus_reserve_bytes"]:
            raise Refusal("hostile L10 workspace scratch floor failed")
        cache = CacheContext(
            length, cache_root, context["manifest"],
            context["hashes"]["L10_cache_manifest"],
            context["source_hashes"], started,
        )
        legacy.configure(length, cache, started)
        rough_root, sharp_root = workspace / "rough", workspace / "sharp"
        rough = v3.history(length, physical.ROUGH, rough_root, retain_terminal=False)
        v3.remove_resolution(rough_root)
        sharp = v3.history(length, physical.SHARP, sharp_root, retain_terminal=True)
        comparison = physical.compare(length, rough, sharp)
        cache.reauthenticate()
        terminals = seal_terminal_shards(length, workspace, sharp, custody)
        wall = time.perf_counter() - started
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        peak_state = max(
            int(rough["peak_logical_scratch_bytes"]),
            int(sharp["peak_logical_scratch_bytes"]),
        )
        allocation = max(
            int(row[role]["maximum_allocation_estimate_bytes"])
            for row in sharp["rows"] for role in ("actual_solver", "null_solver")
        )
        result = make_result(
            length, sharp, comparison, terminals, context,
            peak_state, allocation, rss, wall,
        )
        custody.verify_all()
        digest = atomic_publish(output, result, custody)
        print(comparison["classification"])
        print(
            f"L=10 output_sha256={digest} state={peak_state} "
            f"cache={storage['actual_cache_array_bytes']} rss={rss} wall={wall:.3f}"
        )
    finally:
        legacy.CACHE = None
        v3.EXECUTION_STARTED = None
        if cache is not None:
            cache.close()
        custody.close()
        gc.collect()


def execute(
    worker_id: str, session: OrchestratedWorkerSession | None = None,
) -> None:
    if session is None or worker_id != session.worker_id:
        raise Refusal("hostile L12 execution is not bound to an orchestrated worker")
    if OUTPUT.exists() or OUTPUT.is_symlink() or WORKSPACE.exists() or WORKSPACE.is_symlink():
        raise Refusal("refuse to overwrite canonical hostile history/workspace")
    custody = AuthorityCustody()
    cache: CacheContext | None = None
    started = time.perf_counter()
    try:
        context = authenticate_context(custody, worker_id, session)
        session.acknowledge()
        if shutil.disk_usage(existing_ancestor(WORKSPACE)).free < EXPECTED_DISK_MINIMUM_BYTES:
            raise Refusal("hostile L12 workspace scratch floor failed")
        cache = CacheContext(
            LENGTH, CACHE_ROOT, context["manifest"],
            context["hashes"]["L12_cache_manifest"],
            context["source_hashes"], started,
        )
        # Preserve the independently frozen engine bytes and change only the
        # authenticated L12 execution envelope owned by this worker adapter.
        physical.L12_WALL_LIMIT = WALL_LIMIT
        v3.WALL_LIMIT = WALL_LIMIT
        legacy.configure(LENGTH, cache, started)
        rough_root, sharp_root = WORKSPACE / "rough", WORKSPACE / "sharp"
        rough = v3.history(LENGTH, physical.ROUGH, rough_root, retain_terminal=False)
        v3.remove_resolution(rough_root)
        sharp = v3.history(LENGTH, physical.SHARP, sharp_root, retain_terminal=True)
        comparison = physical.compare(LENGTH, rough, sharp)
        cache.reauthenticate()
        terminals = seal_terminal_shards(LENGTH, WORKSPACE, sharp, custody)
        wall = time.perf_counter() - started
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        peak_state = max(int(rough["peak_logical_scratch_bytes"]),
                         int(sharp["peak_logical_scratch_bytes"]))
        allocation = max(
            int(row[role]["maximum_allocation_estimate_bytes"])
            for row in sharp["rows"] for role in ("actual_solver", "null_solver")
        )
        result = make_result(
            LENGTH, sharp, comparison, terminals, context,
            peak_state, allocation, rss, wall,
        )
        custody.verify_all()
        validate_with_independent_sink(result, custody)
        digest = atomic_publish(OUTPUT, result, custody)
        session.complete(digest)
        print(comparison["classification"])
        print(f"L=12 output_sha256={digest} state={peak_state} cache={EXPECTED_CACHE_BYTES} rss={rss} wall={wall:.3f}")
    finally:
        legacy.CACHE = None
        v3.EXECUTION_STARTED = None
        physical.L12_WALL_LIMIT = ORIGINAL_PHYSICAL_WALL_LIMIT
        v3.WALL_LIMIT = ORIGINAL_ENGINE_WALL_LIMIT
        if cache is not None:
            cache.close()
        custody.close()
        session.close()
        gc.collect()


def self_test() -> None:
    storage = storage_census(LENGTH)
    l10_storage = storage_census(10)
    if (
        len(cache_specs(LENGTH)) != 338
        or storage["actual_cache_array_bytes"] != EXPECTED_CACHE_BYTES
        or storage["maximum_live_state_bytes"] != EXPECTED_STATE_BYTES
        or storage["state_cache_plus_reserve_bytes"] != EXPECTED_DISK_MINIMUM_BYTES
        or l10_storage["actual_cache_array_bytes"] != 44_508_856
        or l10_storage["maximum_live_state_bytes"] != 209_969_760
        or l10_storage["state_cache_plus_reserve_bytes"] != 255_527_192
        or l10_storage["authentication_peak_bytes"] != 14_874_736
        or accuracy_record(physical.ROUGH) != {
            "label": "rough", "checkpoints": [16, 24, 32, 48, 64, 80],
            "quadrature_nodes": 18, "tolerance": 3.0e-9,
        }
        or accuracy_record(physical.SHARP) != {
            "label": "sharp", "checkpoints": [24, 32, 48, 64, 80, 96],
            "quadrature_nodes": 28, "tolerance": 8.0e-11,
        }
        or len(SOLVER_BASE_KEYS) != 12 or len(SOLVER_TERMINAL_KEYS) != 16
        or len(HISTORY_KEYS) != 32 or len(L10_HISTORY_KEYS) != 25
    ):
        raise Refusal("V004R4 adapter self-test failed")
    print("PASS_V004R4_NATIVE_L12_ADAPTER_SELF_TEST")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("execute", "self-test"))
    parser.add_argument("--length", type=int, default=LENGTH)
    parser.add_argument("--orchestrated-worker", action="store_true")
    parser.add_argument("--control-fd", type=int)
    parser.add_argument("--control-channel-id")
    parser.add_argument("--worker-id")
    arguments = parser.parse_args()
    session: OrchestratedWorkerSession | None = None
    try:
        if arguments.mode == "self-test":
            self_test()
        elif arguments.length == 10:
            if any((arguments.orchestrated_worker, arguments.control_fd is not None,
                    arguments.control_channel_id is not None, arguments.worker_id is not None)):
                raise Refusal("hostile L10 does not accept L12 orchestration arguments")
            execute_l10()
        elif arguments.length == LENGTH:
            if (
                arguments.orchestrated_worker is not True
                or arguments.control_fd is None
                or arguments.control_channel_id is None
                or arguments.worker_id is None
            ):
                raise Refusal("hostile L12 requires the inherited orchestrator control channel")
            session = OrchestratedWorkerSession(
                role="hostile_v004r4", worker_id=arguments.worker_id,
                control_fd=arguments.control_fd,
                control_channel_id=arguments.control_channel_id,
                executable=CONSUMER, workspace=WORKSPACE, output=OUTPUT,
            )
            session.announce_and_wait()
            execute(arguments.worker_id, session)
            session = None
        else:
            raise Refusal("V004R4 production adapter is bounded to L=10 or L=12")
        return 0
    except (
        AssertionError, MemoryError, OSError, TimeoutError, ValueError,
        Refusal, r2consumer.common.Refusal,
    ) as error:
        print(f"REFUSE: {error}", file=sys.stderr)
        return 2
    finally:
        if session is not None:
            session.close()


if __name__ == "__main__":
    raise SystemExit(main())
