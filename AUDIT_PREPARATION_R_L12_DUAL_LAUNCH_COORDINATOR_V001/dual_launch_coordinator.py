#!/usr/bin/env python3
"""Pure, fail-closed model of the V012 dual-L12 launch boundary.

This module never opens files, creates artifacts, or starts processes.  It is an
integration contract and synthetic state machine for the required ordering:

    readiness schedule -> schedule audit -> both one-way authorizations
    -> immutable blocked-worker handshake -> worker release -> two nonce ACKs
    -> telemetry

The production integrator is responsible for stable-descriptor file custody and
for translating the returned release tokens into an actual barrier release.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import math
import posixpath
import re
import time
from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Mapping, Tuple


ROLES: Tuple[str, str] = ("target_v012", "hostile_v004r4")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class Refusal(RuntimeError):
    """A controlled, fail-closed validation refusal."""


@dataclass(frozen=True)
class RolePaths:
    executable: str
    workspace: str
    output: str
    mapped_peak_limit_bytes: int


@dataclass(frozen=True)
class LaunchPolicy:
    target: RolePaths
    hostile: RolePaths
    telemetry_path: str
    minimum_host_physical_memory_bytes: int = 48_000_000_000
    minimum_available_memory_bytes: int = 34_865_626_528
    minimum_workspace_free_disk_bytes: int = 19_201_889_580
    per_process_rss_limit_bytes: int = 17_179_869_184
    per_process_wall_limit_seconds: int = 108_000
    maximum_schedule_age_seconds: int = 300
    maximum_launch_skew_seconds: int = 60
    maximum_sample_interval_seconds: int = 60

    def role_paths(self, role: str) -> RolePaths:
        if role == "target_v012":
            return self.target
        if role == "hostile_v004r4":
            return self.hostile
        raise Refusal("unknown role")


@dataclass(frozen=True)
class ReleaseDecision:
    record_sha256: str
    handshake_sha256: str
    release_token_sha256_by_role: Mapping[str, str]


NONCE_DOMAIN = b"V012_L12_WORKER_NONCE_V001\0"
ACK_DOMAIN = b"V012_DUAL_L12_RELEASE_ACK_V001\0"


def parse_strict_json(payload: str) -> object:
    """Parse JSON while rejecting duplicate keys and non-finite constants."""
    if type(payload) is not str:
        raise Refusal("JSON payload must be an exact string")

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise Refusal("duplicate JSON key")
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise Refusal("non-finite JSON constant")

    try:
        return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)
    except Refusal:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise Refusal("malformed JSON") from exc


def canonical_json_bytes(record: object) -> bytes:
    try:
        return (json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as exc:
        raise Refusal("record is not finite canonical JSON") from exc


def record_sha256(record: object) -> str:
    return hashlib.sha256(canonical_json_bytes(record)).hexdigest()


def _dict(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise Refusal(f"{label} must be an exact object")
    return value


def _keys(value: object, expected: set[str], label: str) -> dict[str, object]:
    record = _dict(value, label)
    if set(record) != expected or any(type(key) is not str for key in record):
        raise Refusal(f"{label} exact key census mismatch")
    return record


def _integer(value: object, label: str, *, minimum: int = 1) -> int:
    if type(value) is not int or value < minimum:
        raise Refusal(f"{label} must be an exact integer >= {minimum}")
    return value


def _boolean(value: object, label: str) -> bool:
    if type(value) is not bool:
        raise Refusal(f"{label} must be an exact boolean")
    return value


def _finite_float(value: object, label: str) -> float:
    if type(value) is not float or not math.isfinite(value):
        raise Refusal(f"{label} must be an exact finite float")
    return value


def _string(value: object, label: str) -> str:
    if type(value) is not str or not value:
        raise Refusal(f"{label} must be a nonempty exact string")
    return value


def _sha256(value: object, label: str) -> str:
    text = _string(value, label)
    if SHA256_RE.fullmatch(text) is None:
        raise Refusal(f"{label} must be a lowercase SHA-256")
    return text


def _path(value: object, expected: str, label: str) -> str:
    text = _string(value, label)
    if "\x00" in text or not text.startswith("/") or posixpath.normpath(text) != text:
        raise Refusal(f"{label} must be an absolute normalized path")
    if text != expected:
        raise Refusal(f"{label} canonical path mismatch")
    return text


def _role_map(value: object, label: str) -> dict[str, object]:
    return _keys(value, set(ROLES), label)


def _exact_tree_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return (
            set(left) == set(right)
            and all(_exact_tree_equal(left[key], right[key]) for key in left)
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            _exact_tree_equal(a, b) for a, b in zip(left, right)
        )
    return left == right


def _release_token(handshake_sha256: str, role: str, release_epoch: int) -> str:
    material = f"{handshake_sha256}:{role}:{release_epoch}".encode("ascii")
    return hashlib.sha256(material).hexdigest()


def nonce_commitment(nonce: bytes) -> str:
    if type(nonce) is not bytes or len(nonce) != 32:
        raise Refusal("worker nonce must be exactly 32 bytes")
    return hashlib.sha256(NONCE_DOMAIN + nonce).hexdigest()


def release_ack_sha256(nonce: bytes, command: object) -> str:
    if type(nonce) is not bytes or len(nonce) != 32:
        raise Refusal("worker nonce must be exactly 32 bytes")
    return hashlib.sha256(ACK_DOMAIN + nonce + canonical_json_bytes(command)).hexdigest()


class DualLaunchCoordinator:
    """In-memory coordinator whose accepted nodes are frozen canonical bytes."""

    def __init__(self, policy: LaunchPolicy, evaluation_epoch: int):
        if type(policy) is not LaunchPolicy:
            raise Refusal("policy must be an exact LaunchPolicy")
        self.policy = policy
        self.evaluation_epoch = _integer(evaluation_epoch, "evaluation_epoch")
        self._constructed_monotonic = time.monotonic()
        self._validate_policy()
        self._accepted: Dict[str, bytes] = {}
        self._authorization_by_role: Dict[str, bytes] = {}
        self._release_ack_by_role: Dict[str, bytes] = {}
        self._completion_by_role: Dict[str, bytes] = {}

    @property
    def stage(self) -> str:
        if "telemetry" in self._accepted:
            return "TELEMETRY_ACCEPTED"
        if len(self._completion_by_role) == 2:
            return "COMPLETIONS_COMPLETE"
        if len(self._completion_by_role) == 1:
            return "COMPLETIONS_PARTIAL"
        if len(self._release_ack_by_role) == 2:
            return "RELEASE_ACKS_COMPLETE"
        if len(self._release_ack_by_role) == 1:
            return "RELEASE_ACKS_PARTIAL"
        if "release" in self._accepted:
            return "WORKERS_RELEASED"
        if "handshake" in self._accepted:
            return "HANDSHAKE_COMMITTED"
        if len(self._authorization_by_role) == 2:
            return "AUTHORIZATIONS_COMPLETE"
        if len(self._authorization_by_role) == 1:
            return "AUTHORIZATIONS_PARTIAL"
        if "schedule_audit" in self._accepted:
            return "SCHEDULE_AUDITED"
        if "schedule" in self._accepted:
            return "SCHEDULE_ACCEPTED"
        return "EMPTY"

    def state_snapshot(self) -> tuple[object, ...]:
        return (
            self.stage,
            tuple(sorted((key, hashlib.sha256(value).hexdigest())
                         for key, value in self._accepted.items())),
            tuple(sorted((key, hashlib.sha256(value).hexdigest())
                         for key, value in self._authorization_by_role.items())),
            tuple(sorted((key, hashlib.sha256(value).hexdigest())
                         for key, value in self._release_ack_by_role.items())),
            tuple(sorted((key, hashlib.sha256(value).hexdigest())
                         for key, value in self._completion_by_role.items())),
        )

    def accepted_sha256(self, node: str) -> str:
        if node.startswith("release_ack:"):
            role = node.removeprefix("release_ack:")
            if role in self._release_ack_by_role:
                return hashlib.sha256(self._release_ack_by_role[role]).hexdigest()
        if node.startswith("completion:"):
            role = node.removeprefix("completion:")
            if role in self._completion_by_role:
                return hashlib.sha256(self._completion_by_role[role]).hexdigest()
        if node in self._accepted:
            return hashlib.sha256(self._accepted[node]).hexdigest()
        if node in self._authorization_by_role:
            return hashlib.sha256(self._authorization_by_role[node]).hexdigest()
        raise Refusal("requested node has not been accepted")

    def accepted_record(self, node: str) -> dict[str, object]:
        if node.startswith("release_ack:"):
            role = node.removeprefix("release_ack:")
            if role not in self._release_ack_by_role:
                raise Refusal("requested node has not been accepted")
            payload = self._release_ack_by_role[role]
        elif node.startswith("completion:"):
            role = node.removeprefix("completion:")
            if role not in self._completion_by_role:
                raise Refusal("requested node has not been accepted")
            payload = self._completion_by_role[role]
        elif node in self._accepted:
            payload = self._accepted[node]
        elif node in self._authorization_by_role:
            payload = self._authorization_by_role[node]
        else:
            raise Refusal("requested node has not been accepted")
        result = parse_strict_json(payload.decode("ascii"))
        return _dict(result, "accepted record")

    def admit_schedule(self, record: object) -> str:
        if self.stage != "EMPTY":
            raise Refusal("readiness schedule is duplicate or out of order")
        schedule = self._validate_schedule(record)
        return self._freeze("schedule", schedule)

    def admit_schedule_audit(self, record: object) -> str:
        if self.stage != "SCHEDULE_ACCEPTED":
            raise Refusal("schedule audit requires exactly one accepted schedule")
        self._require_fresh_schedule()
        audit = self._validate_schedule_audit(record)
        return self._freeze("schedule_audit", audit)

    def admit_authorization(self, record: object) -> str:
        if self.stage not in {
            "SCHEDULE_AUDITED", "AUTHORIZATIONS_PARTIAL",
        }:
            raise Refusal("one-way authorization requires the schedule audit")
        self._require_fresh_schedule()
        authorization = self._validate_authorization(record)
        role = authorization["role"]
        if role in self._authorization_by_role:
            raise Refusal("duplicate one-way authorization role")
        frozen = canonical_json_bytes(authorization)
        self._authorization_by_role[role] = frozen
        return hashlib.sha256(frozen).hexdigest()

    def commit_handshake(self, record: object) -> str:
        if self.stage != "AUTHORIZATIONS_COMPLETE":
            raise Refusal("handshake requires both one-way authorizations")
        self._require_fresh_schedule()
        handshake = self._validate_handshake(record)
        return self._freeze("handshake", handshake)

    def release_workers(self, record: object) -> ReleaseDecision:
        """Validate a barrier release and return tokens; never launches a process."""
        if self.stage != "HANDSHAKE_COMMITTED":
            raise Refusal("worker release requires an immutable handshake")
        self._require_fresh_schedule()
        release = self._validate_release(record)
        digest = self._freeze("release", release)
        tokens = {
            role: release["release_by_role"][role]["release_token_sha256"]
            for role in ROLES
        }
        return ReleaseDecision(
            record_sha256=digest,
            handshake_sha256=self.accepted_sha256("handshake"),
            release_token_sha256_by_role=MappingProxyType(tokens),
        )

    def release_command(self, role: str) -> dict[str, object]:
        """Construct the non-circular command sent over the retained channel."""
        if "release" not in self._accepted:
            raise Refusal("release command requires accepted worker release")
        self._require_fresh_schedule()
        return self._release_command_record(role)

    def _release_command_record(self, role: str) -> dict[str, object]:
        """Reconstruct an accepted command without reopening authorization."""
        if role not in ROLES:
            raise Refusal("release command role mismatch")
        handshake = self.accepted_record("handshake")
        release = self.accepted_record("release")
        worker = handshake["workers"][role]
        return {
            "schema": "V012_L12_WORKER_RELEASE_COMMAND_V001",
            "role": role,
            "worker_id": worker["worker_id"],
            "process_id": worker["process_id"],
            "process_start_token": worker["process_start_token"],
            "control_channel_id": worker["control_channel_id"],
            "nonce_commitment_sha256": worker["nonce_commitment_sha256"],
            "handshake_sha256": self.accepted_sha256("handshake"),
            "worker_release_sha256": self.accepted_sha256("release"),
            "release_epoch": release["release_epoch_by_role"][role],
        }

    def admit_release_ack(self, command: object, record: object) -> str:
        if self.stage not in {"WORKERS_RELEASED", "RELEASE_ACKS_PARTIAL"}:
            raise Refusal("release ACK requires accepted worker release")
        self._require_fresh_schedule()
        command_row = self._validate_release_command(command)
        ack = self._validate_release_ack(command_row, record)
        role = ack["role"]
        if role in self._release_ack_by_role:
            raise Refusal("duplicate worker release ACK role")
        payload = canonical_json_bytes(ack)
        self._release_ack_by_role[role] = payload
        return hashlib.sha256(payload).hexdigest()

    def admit_worker_completion(self, record: object) -> str:
        if self.stage not in {
            "RELEASE_ACKS_COMPLETE", "COMPLETIONS_PARTIAL",
        }:
            raise Refusal("worker completion requires both release ACKs")
        completion = self._validate_worker_completion(record)
        role = completion["role"]
        if role in self._completion_by_role:
            raise Refusal("duplicate worker completion role")
        payload = canonical_json_bytes(completion)
        self._completion_by_role[role] = payload
        return hashlib.sha256(payload).hexdigest()

    def admit_postrun_telemetry(self, record: object) -> str:
        if self.stage != "COMPLETIONS_COMPLETE":
            raise Refusal("postrun telemetry requires both worker completions")
        telemetry = self._validate_telemetry(record)
        return self._freeze("telemetry", telemetry)

    def _freeze(self, node: str, record: dict[str, object]) -> str:
        if node in self._accepted:
            raise Refusal("duplicate accepted node")
        payload = canonical_json_bytes(record)
        self._accepted[node] = payload
        return hashlib.sha256(payload).hexdigest()

    def _current_evaluation_epoch(self) -> int:
        elapsed = time.monotonic() - self._constructed_monotonic
        if not math.isfinite(elapsed) or elapsed < 0:
            raise Refusal("coordinator monotonic clock mismatch")
        return self.evaluation_epoch + int(elapsed)

    def _require_fresh_schedule(self) -> None:
        if "schedule" not in self._accepted:
            raise Refusal("accepted schedule is absent")
        schedule = self.accepted_record("schedule")
        current = self._current_evaluation_epoch()
        if not schedule["created_epoch"] <= current <= schedule["expires_epoch"]:
            raise Refusal("accepted schedule expired during orchestration")

    def _validate_policy(self) -> None:
        for role in ROLES:
            paths = self.policy.role_paths(role)
            if type(paths) is not RolePaths:
                raise Refusal(f"{role} policy paths must be exact RolePaths")
            _path(paths.executable, paths.executable, f"{role} policy executable")
            _path(paths.workspace, paths.workspace, f"{role} policy workspace")
            _path(paths.output, paths.output, f"{role} policy output")
            _integer(paths.mapped_peak_limit_bytes, f"{role} mapped limit")
        _path(self.policy.telemetry_path, self.policy.telemetry_path, "policy telemetry")
        path_census = {
            self.policy.target.executable, self.policy.target.workspace,
            self.policy.target.output, self.policy.hostile.executable,
            self.policy.hostile.workspace, self.policy.hostile.output,
            self.policy.telemetry_path,
        }
        if len(path_census) != 7:
            raise Refusal("policy paths are aliased")
        for name in (
            "minimum_host_physical_memory_bytes", "minimum_available_memory_bytes",
            "minimum_workspace_free_disk_bytes", "per_process_rss_limit_bytes",
            "per_process_wall_limit_seconds", "maximum_schedule_age_seconds",
            "maximum_launch_skew_seconds", "maximum_sample_interval_seconds",
        ):
            _integer(getattr(self.policy, name), f"policy {name}")

    def _validate_schedule(self, value: object) -> dict[str, object]:
        record = _keys(value, {
            "schema", "classification", "created_epoch", "expires_epoch",
            "l10_cross_gate_sha256", "resource_snapshot", "schedule", "roles",
            "telemetry", "claim_boundary",
        }, "readiness schedule")
        if record["schema"] != "V012_DUAL_L12_READINESS_SCHEDULE_V001":
            raise Refusal("readiness schedule schema mismatch")
        if record["classification"] != "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT":
            raise Refusal("readiness schedule classification mismatch")
        created = _integer(record["created_epoch"], "schedule created_epoch")
        expires = _integer(record["expires_epoch"], "schedule expires_epoch")
        if not 0 < expires - created <= self.policy.maximum_schedule_age_seconds:
            raise Refusal("schedule freshness window mismatch")
        if not created <= self._current_evaluation_epoch() <= expires:
            raise Refusal("schedule is not current at evaluation epoch")
        _sha256(record["l10_cross_gate_sha256"], "schedule L10 cross gate")

        snapshot = _keys(record["resource_snapshot"], {
            "captured_epoch", "host_physical_memory_bytes", "available_memory_bytes",
            "workspace_free_disk_bytes", "workspace_filesystem_device",
            "both_workspace_roots_same_filesystem", "memory_pressure", "passes",
        }, "resource snapshot")
        captured = _integer(snapshot["captured_epoch"], "snapshot captured_epoch")
        if not created <= captured <= expires:
            raise Refusal("resource snapshot outside schedule window")
        if _integer(snapshot["host_physical_memory_bytes"], "host memory") \
                < self.policy.minimum_host_physical_memory_bytes:
            raise Refusal("host physical memory below threshold")
        if _integer(snapshot["available_memory_bytes"], "available memory") \
                < self.policy.minimum_available_memory_bytes:
            raise Refusal("available memory below threshold")
        if _integer(snapshot["workspace_free_disk_bytes"], "workspace free disk") \
                < self.policy.minimum_workspace_free_disk_bytes:
            raise Refusal("workspace disk below threshold")
        _integer(snapshot["workspace_filesystem_device"], "filesystem device")
        if _boolean(snapshot["both_workspace_roots_same_filesystem"], "same filesystem") is not True:
            raise Refusal("workspace roots are not on the same filesystem")
        if snapshot["memory_pressure"] != "NORMAL" or type(snapshot["memory_pressure"]) is not str:
            raise Refusal("memory pressure is not NORMAL")
        if _boolean(snapshot["passes"], "resource passes") is not True:
            raise Refusal("resource snapshot does not pass")

        schedule = _keys(record["schedule"], {
            "launch_mode", "release_only_after_both_l12_authorizations",
            "launch_skew_seconds_max", "per_process_rss_limit_bytes",
            "per_process_wall_limit_seconds", "mapped_peak_limit_bytes_by_role",
        }, "schedule controls")
        expected_schedule = {
            "launch_mode": "PRELAUNCHED_BLOCKED_TWO_WORKER",
            "release_only_after_both_l12_authorizations": True,
            "launch_skew_seconds_max": self.policy.maximum_launch_skew_seconds,
            "per_process_rss_limit_bytes": self.policy.per_process_rss_limit_bytes,
            "per_process_wall_limit_seconds": self.policy.per_process_wall_limit_seconds,
            "mapped_peak_limit_bytes_by_role": {
                role: self.policy.role_paths(role).mapped_peak_limit_bytes for role in ROLES
            },
        }
        if not _exact_tree_equal(schedule, expected_schedule):
            raise Refusal("schedule controls mismatch")

        roles = _role_map(record["roles"], "schedule roles")
        for role in ROLES:
            role_record = _keys(roles[role], {
                "role", "worker_executable_path", "workspace_path", "output_path",
                "ready_for_blocked_worker_start",
            }, f"schedule role {role}")
            paths = self.policy.role_paths(role)
            if role_record["role"] != role:
                raise Refusal("schedule role identity mismatch")
            _path(role_record["worker_executable_path"], paths.executable, "worker executable")
            _path(role_record["workspace_path"], paths.workspace, "workspace")
            _path(role_record["output_path"], paths.output, "output")
            if _boolean(role_record["ready_for_blocked_worker_start"], "worker readiness") is not True:
                raise Refusal("worker is not ready for blocked start")

        telemetry = _keys(record["telemetry"], {
            "path", "schema", "must_be_absent_before_release",
            "absent_at_schedule_capture", "sample_interval_seconds_max",
        }, "telemetry interface")
        _path(telemetry["path"], self.policy.telemetry_path, "telemetry path")
        if telemetry["schema"] != "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001":
            raise Refusal("telemetry schema mismatch")
        if _boolean(telemetry["must_be_absent_before_release"], "telemetry absence policy") is not True:
            raise Refusal("telemetry absence policy mismatch")
        if _boolean(telemetry["absent_at_schedule_capture"], "telemetry absence evidence") is not True:
            raise Refusal("telemetry exists before release")
        if _integer(telemetry["sample_interval_seconds_max"], "sample interval") \
                != self.policy.maximum_sample_interval_seconds:
            raise Refusal("telemetry sample interval mismatch")
        if record["claim_boundary"] != "READINESS_AND_RESOURCE_SCHEDULING_ONLY__NO_L12_RELEASE_OR_RESULT":
            raise Refusal("schedule claim boundary mismatch")
        return record

    def _validate_schedule_audit(self, value: object) -> dict[str, object]:
        record = _keys(value, {
            "schema", "classification", "auditor_role", "schedule_sha256",
            "l10_cross_gate_sha256", "checks", "checks_total", "checks_passed",
            "failures", "claim_boundary",
        }, "schedule audit")
        schedule = self.accepted_record("schedule")
        expected_checks = {
            "schedule_exact_schema": 1,
            "deep_exact_types": 1,
            "two_role_path_custody": 2,
            "normal_memory_pressure": 1,
            "resource_thresholds": 4,
            "freshness_window": 1,
            "telemetry_prelaunch_absence": 1,
        }
        if record["schema"] != "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001":
            raise Refusal("schedule audit schema mismatch")
        if record["classification"] != "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT":
            raise Refusal("schedule audit classification mismatch")
        if record["auditor_role"] != "INDEPENDENT_DUAL_LAUNCH_COORDINATOR_REVIEW":
            raise Refusal("schedule audit role mismatch")
        if _sha256(record["schedule_sha256"], "audited schedule") != self.accepted_sha256("schedule"):
            raise Refusal("schedule audit binding mismatch")
        if _sha256(record["l10_cross_gate_sha256"], "audited L10 cross gate") \
                != schedule["l10_cross_gate_sha256"]:
            raise Refusal("schedule audit L10 cross binding mismatch")
        if record["checks"] != expected_checks:
            raise Refusal("schedule audit check census mismatch")
        for name, count in _dict(record["checks"], "audit checks").items():
            _string(name, "audit check name")
            _integer(count, "audit check count")
        total = sum(expected_checks.values())
        if _integer(record["checks_total"], "checks_total") != total:
            raise Refusal("schedule audit total mismatch")
        if _integer(record["checks_passed"], "checks_passed") != total:
            raise Refusal("schedule audit did not fully pass")
        if type(record["failures"]) is not list or record["failures"] != []:
            raise Refusal("schedule audit failures mismatch")
        if record["claim_boundary"] != "INDEPENDENT_READINESS_AUDIT_ONLY__NO_L12_AUTHORIZATION_RELEASE_OR_RESULT":
            raise Refusal("schedule audit claim boundary mismatch")
        return record

    def _validate_authorization(self, value: object) -> dict[str, object]:
        record = _keys(value, {
            "schema", "classification", "role", "authorized_length",
            "schedule_sha256", "schedule_audit_sha256", "l10_cross_gate_sha256",
            "consumer_sha256", "l12_cache_manifest_sha256", "claim_boundary",
        }, "one-way L12 authorization")
        role = _string(record["role"], "authorization role")
        if role not in ROLES:
            raise Refusal("authorization role mismatch")
        expected_schema = {
            "target_v012": "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001",
            "hostile_v004r4": "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001",
        }[role]
        expected_classification = {
            "target_v012": "AUTHORIZE_TARGET_V012_L12_AFTER_SCHEDULE_AUDIT",
            "hostile_v004r4": "AUTHORIZE_HOSTILE_V004R4_L12_AFTER_SCHEDULE_AUDIT",
        }[role]
        if record["schema"] != expected_schema or record["classification"] != expected_classification:
            raise Refusal("authorization identity mismatch")
        if _integer(record["authorized_length"], "authorized_length") != 12:
            raise Refusal("authorization is not L12-only")
        schedule = self.accepted_record("schedule")
        if _sha256(record["schedule_sha256"], "authorization schedule") \
                != self.accepted_sha256("schedule"):
            raise Refusal("authorization schedule binding mismatch")
        if _sha256(record["schedule_audit_sha256"], "authorization schedule audit") \
                != self.accepted_sha256("schedule_audit"):
            raise Refusal("authorization audit binding mismatch")
        if _sha256(record["l10_cross_gate_sha256"], "authorization L10 cross gate") \
                != schedule["l10_cross_gate_sha256"]:
            raise Refusal("authorization L10 cross binding mismatch")
        _sha256(record["consumer_sha256"], "authorization consumer")
        _sha256(record["l12_cache_manifest_sha256"], "authorization cache")
        if record["claim_boundary"] != "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT":
            raise Refusal("authorization claim boundary mismatch")
        return record

    def _authorization_hashes(self) -> dict[str, str]:
        if set(self._authorization_by_role) != set(ROLES):
            raise Refusal("both authorization hashes are not available")
        return {
            role: hashlib.sha256(self._authorization_by_role[role]).hexdigest()
            for role in ROLES
        }

    def _validate_worker_ready(
        self, value: object, role: str, schedule: dict[str, object],
        handshake_created_epoch: int,
    ) -> dict[str, object]:
        worker = _keys(value, {
            "schema", "role", "worker_id", "process_id",
            "process_start_token", "executable_path", "executable_sha256",
            "workspace_path", "output_path", "control_channel_id",
            "nonce_commitment_sha256", "ready_epoch", "blocked_on_release",
        }, f"handshake worker {role}")
        if worker["schema"] != "V012_L12_WORKER_READY_V001":
            raise Refusal("worker READY schema mismatch")
        if worker["role"] != role:
            raise Refusal("handshake worker role mismatch")
        _string(worker["worker_id"], "worker_id")
        _integer(worker["process_id"], "process_id")
        _sha256(worker["process_start_token"], "process start token")
        paths = self.policy.role_paths(role)
        _path(worker["executable_path"], paths.executable, "handshake executable")
        _sha256(worker["executable_sha256"], "worker executable SHA-256")
        _path(worker["workspace_path"], paths.workspace, "handshake workspace")
        _path(worker["output_path"], paths.output, "handshake output")
        _sha256(worker["control_channel_id"], "control channel id")
        _sha256(worker["nonce_commitment_sha256"], "worker nonce commitment")
        ready = _integer(worker["ready_epoch"], "worker ready_epoch")
        if not schedule["created_epoch"] <= ready <= handshake_created_epoch:
            raise Refusal("worker readiness outside pre-handshake window")
        if _boolean(worker["blocked_on_release"], "blocked worker state") is not True:
            raise Refusal("worker is not blocked on release")
        return worker

    def _validate_handshake(self, value: object) -> dict[str, object]:
        record = _keys(value, {
            "schema", "classification", "created_epoch", "schedule_sha256",
            "schedule_audit_sha256", "authorization_sha256_by_role",
            "memory_pressure", "workers", "ready_sha256_by_role",
            "observed_readiness_skew_seconds",
            "launch_skew_seconds_max", "telemetry", "claim_boundary",
        }, "dual-launch handshake")
        if record["schema"] != "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002":
            raise Refusal("handshake schema mismatch")
        if record["classification"] != "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS":
            raise Refusal("handshake classification mismatch")
        schedule = self.accepted_record("schedule")
        created = _integer(record["created_epoch"], "handshake created_epoch")
        if not schedule["created_epoch"] <= created <= schedule["expires_epoch"]:
            raise Refusal("handshake outside schedule window")
        if _sha256(record["schedule_sha256"], "handshake schedule") \
                != self.accepted_sha256("schedule"):
            raise Refusal("handshake schedule binding mismatch")
        if _sha256(record["schedule_audit_sha256"], "handshake schedule audit") \
                != self.accepted_sha256("schedule_audit"):
            raise Refusal("handshake audit binding mismatch")
        auth_hashes = _role_map(record["authorization_sha256_by_role"], "handshake authorizations")
        if auth_hashes != self._authorization_hashes():
            raise Refusal("handshake authorization hash census mismatch")
        for role, digest in auth_hashes.items():
            _sha256(digest, f"{role} handshake authorization")
        if record["memory_pressure"] != "NORMAL" or type(record["memory_pressure"]) is not str:
            raise Refusal("handshake memory pressure is not NORMAL")
        workers = _role_map(record["workers"], "handshake workers")
        ready_hashes = _role_map(
            record["ready_sha256_by_role"], "handshake READY hashes"
        )
        ready_epochs: dict[str, int] = {}
        pids: set[int] = set()
        worker_ids: set[str] = set()
        process_tokens: set[str] = set()
        channel_ids: set[str] = set()
        nonce_commitments: set[str] = set()
        for role in ROLES:
            worker = self._validate_worker_ready(
                workers[role], role, schedule, created,
            )
            if _sha256(ready_hashes[role], f"{role} READY hash") != record_sha256(worker):
                raise Refusal("worker READY hash reconstruction mismatch")
            worker_id = worker["worker_id"]
            pid = worker["process_id"]
            token = worker["process_start_token"]
            channel = worker["control_channel_id"]
            commitment = worker["nonce_commitment_sha256"]
            if (
                worker_id in worker_ids or pid in pids
                or token in process_tokens or channel in channel_ids
                or commitment in nonce_commitments
            ):
                raise Refusal("handshake worker identities are aliased")
            worker_ids.add(worker_id)
            pids.add(pid)
            process_tokens.add(token)
            channel_ids.add(channel)
            nonce_commitments.add(commitment)
            ready_epochs[role] = worker["ready_epoch"]
        skew = abs(ready_epochs[ROLES[0]] - ready_epochs[ROLES[1]])
        if _integer(record["observed_readiness_skew_seconds"], "readiness skew", minimum=0) != skew:
            raise Refusal("readiness skew reconstruction mismatch")
        if skew > self.policy.maximum_launch_skew_seconds:
            raise Refusal("worker readiness skew exceeds launch bound")
        if _integer(record["launch_skew_seconds_max"], "launch skew maximum") \
                != self.policy.maximum_launch_skew_seconds:
            raise Refusal("handshake launch skew policy mismatch")
        telemetry = _keys(record["telemetry"], {
            "path", "schema", "absent_before_release",
        }, "handshake telemetry")
        _path(telemetry["path"], self.policy.telemetry_path, "handshake telemetry path")
        if telemetry["schema"] != "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001":
            raise Refusal("handshake telemetry schema mismatch")
        if _boolean(telemetry["absent_before_release"], "handshake telemetry absence") is not True:
            raise Refusal("telemetry is not absent before release")
        if record["claim_boundary"] != "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT":
            raise Refusal("handshake claim boundary mismatch")
        return record

    def _validate_release(self, value: object) -> dict[str, object]:
        record = _keys(value, {
            "schema", "classification", "handshake_sha256",
            "authorization_sha256_by_role", "release_epoch_by_role",
            "observed_launch_skew_seconds", "release_by_role", "claim_boundary",
        }, "worker release")
        if record["schema"] != "V012_DUAL_L12_WORKER_RELEASE_V002":
            raise Refusal("worker release schema mismatch")
        if record["classification"] != "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS":
            raise Refusal("worker release classification mismatch")
        if _sha256(record["handshake_sha256"], "release handshake") \
                != self.accepted_sha256("handshake"):
            raise Refusal("release handshake binding mismatch")
        auth_hashes = _role_map(record["authorization_sha256_by_role"], "release authorizations")
        if auth_hashes != self._authorization_hashes():
            raise Refusal("release authorization binding mismatch")
        epochs = _role_map(record["release_epoch_by_role"], "release epochs")
        release_epochs = {role: _integer(epochs[role], f"{role} release_epoch") for role in ROLES}
        handshake = self.accepted_record("handshake")
        schedule = self.accepted_record("schedule")
        if any(not handshake["created_epoch"] <= epoch <= schedule["expires_epoch"]
               for epoch in release_epochs.values()):
            raise Refusal("release epoch outside post-handshake schedule window")
        skew = abs(release_epochs[ROLES[0]] - release_epochs[ROLES[1]])
        if _integer(record["observed_launch_skew_seconds"], "observed launch skew", minimum=0) != skew:
            raise Refusal("launch skew reconstruction mismatch")
        if skew > self.policy.maximum_launch_skew_seconds:
            raise Refusal("launch skew exceeds 60 seconds")
        releases = _role_map(record["release_by_role"], "release records")
        workers = handshake["workers"]
        for role in ROLES:
            release = _keys(releases[role], {
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id", "nonce_commitment_sha256",
                "release_token_sha256",
            }, f"release record {role}")
            if (
                release["role"] != role
                or release["worker_id"] != workers[role]["worker_id"]
                or release["process_id"] != workers[role]["process_id"]
                or type(release["process_id"]) is not int
                or release["process_start_token"] != workers[role]["process_start_token"]
                or release["control_channel_id"] != workers[role]["control_channel_id"]
                or release["nonce_commitment_sha256"]
                != workers[role]["nonce_commitment_sha256"]
            ):
                raise Refusal("released worker identity mismatch")
            expected_token = _release_token(
                self.accepted_sha256("handshake"), role, release_epochs[role]
            )
            if _sha256(release["release_token_sha256"], "release token") != expected_token:
                raise Refusal("release token mismatch")
        if record["claim_boundary"] != "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT":
            raise Refusal("release claim boundary mismatch")
        return record

    def _validate_release_command(self, value: object) -> dict[str, object]:
        command = _keys(value, {
            "schema", "role", "worker_id", "process_id",
            "process_start_token", "control_channel_id",
            "nonce_commitment_sha256", "handshake_sha256",
            "worker_release_sha256", "release_epoch",
        }, "worker release command")
        if command["schema"] != "V012_L12_WORKER_RELEASE_COMMAND_V001":
            raise Refusal("worker release command schema mismatch")
        role = _string(command["role"], "release command role")
        if role not in ROLES:
            raise Refusal("release command role mismatch")
        _integer(command["process_id"], "release command process_id")
        _integer(command["release_epoch"], "release command release_epoch")
        if not _exact_tree_equal(command, self.release_command(role)):
            raise Refusal("release command reconstruction mismatch")
        return command

    def _validate_release_ack(
        self, command: dict[str, object], value: object,
    ) -> dict[str, object]:
        ack = _keys(value, {
            "schema", "role", "worker_id", "process_id",
            "process_start_token", "control_channel_id", "nonce_hex",
            "ack_sha256",
        }, "worker release ACK")
        if ack["schema"] != "V012_L12_WORKER_RELEASE_ACK_V001":
            raise Refusal("worker release ACK schema mismatch")
        for key in (
            "role", "worker_id", "process_id", "process_start_token",
            "control_channel_id",
        ):
            if ack[key] != command[key] or type(ack[key]) is not type(command[key]):
                raise Refusal("worker release ACK identity mismatch")
        nonce_hex = _string(ack["nonce_hex"], "worker nonce")
        if re.fullmatch(r"[0-9a-f]{64}", nonce_hex) is None:
            raise Refusal("worker nonce must be lowercase 32-byte hex")
        nonce = bytes.fromhex(nonce_hex)
        if nonce_commitment(nonce) != command["nonce_commitment_sha256"]:
            raise Refusal("worker nonce commitment mismatch")
        if _sha256(ack["ack_sha256"], "worker release ACK digest") \
                != release_ack_sha256(nonce, command):
            raise Refusal("worker release ACK digest mismatch")
        return ack

    def _validate_worker_completion(self, value: object) -> dict[str, object]:
        completion = _keys(value, {
            "schema", "role", "worker_id", "process_id",
            "process_start_token", "control_channel_id", "output_path",
            "output_sha256", "completion_epoch",
            "blocked_on_orchestrator_close",
        }, "worker completion")
        if completion["schema"] != "V012_L12_WORKER_COMPLETION_V001":
            raise Refusal("worker completion schema mismatch")
        role = _string(completion["role"], "worker completion role")
        if role not in ROLES:
            raise Refusal("worker completion role mismatch")
        worker = self.accepted_record("handshake")["workers"][role]
        _integer(completion["process_id"], "worker completion process_id")
        for key in (
            "worker_id", "process_id", "process_start_token",
            "control_channel_id",
        ):
            if (
                completion[key] != worker[key]
                or type(completion[key]) is not type(worker[key])
            ):
                raise Refusal("worker completion identity mismatch")
        _path(
            completion["output_path"], self.policy.role_paths(role).output,
            "worker completion output",
        )
        _sha256(completion["output_sha256"], "worker completion output hash")
        completed = _integer(
            completion["completion_epoch"], "worker completion epoch",
        )
        released = self.accepted_record("release")[
            "release_epoch_by_role"
        ][role]
        if not (
            released < completed
            <= released + self.policy.per_process_wall_limit_seconds
        ):
            raise Refusal("worker completion outside execution wall window")
        if _boolean(
            completion["blocked_on_orchestrator_close"],
            "worker completion blocked state",
        ) is not True:
            raise Refusal("worker is not retained after completion")
        return completion

    def _validate_telemetry(self, value: object) -> dict[str, object]:
        record = _keys(value, {
            "schema", "classification", "shared_gate_sha256",
            "schedule_audit_sha256", "dual_launch_handshake_sha256",
            "worker_release_sha256", "authorization_sha256_by_role",
            "worker_identity_by_role", "release_command_sha256_by_role",
            "release_ack_sha256_by_role", "completion_sha256_by_role",
            "launch_epoch_by_role", "completion_epoch_by_role",
            "wall_seconds_by_role", "peak_rss_bytes_by_role",
            "rss_peak_semantics",
            "peak_mapped_bytes_by_role", "mapped_peak_semantics",
            "runtime_samples_by_role",
            "free_disk_bytes_samples", "exit_code_by_role", "output_path_by_role",
            "output_sha256_by_role", "claim_boundary",
        }, "postrun telemetry")
        if record["schema"] != "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001":
            raise Refusal("telemetry schema mismatch")
        if record["classification"] != "COMPLETE_SHARED_L12_TELEMETRY":
            raise Refusal("telemetry classification mismatch")
        if record["mapped_peak_semantics"] != (
            "CONSERVATIVE_AUTHENTICATION_CACHE_CERTIFICATE__"
            "NOT_OS_VIRTUAL_MEMORY"
        ):
            raise Refusal("telemetry mapped peak semantics mismatch")
        if record["rss_peak_semantics"] != (
            "LAUNCHER_SAMPLED_CURRENT_RSS_AT_MOST_30_SECONDS__"
            "NOT_OS_HIGH_WATER"
        ):
            raise Refusal("telemetry RSS peak semantics mismatch")
        exact_bindings = {
            "shared_gate_sha256": self.accepted_sha256("schedule"),
            "schedule_audit_sha256": self.accepted_sha256("schedule_audit"),
            "dual_launch_handshake_sha256": self.accepted_sha256("handshake"),
            "worker_release_sha256": self.accepted_sha256("release"),
        }
        for key, expected in exact_bindings.items():
            if _sha256(record[key], key) != expected:
                raise Refusal("telemetry DAG binding mismatch")
        auth_hashes = _role_map(record["authorization_sha256_by_role"], "telemetry authorizations")
        if auth_hashes != self._authorization_hashes():
            raise Refusal("telemetry authorization binding mismatch")
        handshake = self.accepted_record("handshake")
        identities = _role_map(
            record["worker_identity_by_role"], "telemetry worker identities"
        )
        command_hashes = _role_map(
            record["release_command_sha256_by_role"],
            "telemetry release command hashes",
        )
        ack_hashes = _role_map(
            record["release_ack_sha256_by_role"], "telemetry release ACK hashes"
        )
        completion_hashes = _role_map(
            record["completion_sha256_by_role"],
            "telemetry worker completion hashes",
        )
        identity_keys = {
            "worker_id", "process_id", "process_start_token", "executable_path",
            "executable_sha256", "control_channel_id", "nonce_commitment_sha256",
        }
        for role in ROLES:
            identity = _keys(
                identities[role], identity_keys, f"{role} telemetry identity",
            )
            worker = handshake["workers"][role]
            if not _exact_tree_equal(
                identity, {key: worker[key] for key in identity_keys},
            ):
                raise Refusal("telemetry worker identity binding mismatch")
            if _sha256(command_hashes[role], f"{role} release command hash") \
                    != record_sha256(self._release_command_record(role)):
                raise Refusal("telemetry release command binding mismatch")
            if _sha256(ack_hashes[role], f"{role} release ACK hash") \
                    != self.accepted_sha256(f"release_ack:{role}"):
                raise Refusal("telemetry release ACK binding mismatch")
            if _sha256(
                completion_hashes[role], f"{role} worker completion hash",
            ) != self.accepted_sha256(f"completion:{role}"):
                raise Refusal("telemetry worker completion binding mismatch")
        release = self.accepted_record("release")
        launches = _role_map(record["launch_epoch_by_role"], "telemetry launch epochs")
        completions = _role_map(record["completion_epoch_by_role"], "telemetry completion epochs")
        walls = _role_map(record["wall_seconds_by_role"], "telemetry walls")
        rss = _role_map(record["peak_rss_bytes_by_role"], "telemetry RSS")
        mapped = _role_map(record["peak_mapped_bytes_by_role"], "telemetry mapped bytes")
        runtime_samples = _role_map(
            record["runtime_samples_by_role"], "telemetry runtime samples"
        )
        exits = _role_map(record["exit_code_by_role"], "telemetry exits")
        output_paths = _role_map(record["output_path_by_role"], "telemetry output paths")
        output_hashes = _role_map(record["output_sha256_by_role"], "telemetry output hashes")
        launch_values: dict[str, int] = {}
        completion_values: dict[str, int] = {}
        for role in ROLES:
            launch = _integer(launches[role], f"{role} launch epoch")
            if launch != release["release_epoch_by_role"][role]:
                raise Refusal("telemetry launch epoch does not equal barrier release")
            completion = _integer(completions[role], f"{role} completion epoch")
            completion_record = self.accepted_record(f"completion:{role}")
            if completion <= launch:
                raise Refusal("telemetry completion is not after launch")
            if (
                completion != completion_record["completion_epoch"]
                or output_paths[role] != completion_record["output_path"]
                or output_hashes[role] != completion_record["output_sha256"]
            ):
                raise Refusal("telemetry worker completion projection mismatch")
            wall = _finite_float(walls[role], f"{role} wall seconds")
            if wall != float(completion - launch) or wall > self.policy.per_process_wall_limit_seconds:
                raise Refusal("telemetry wall reconstruction/limit mismatch")
            if _integer(rss[role], f"{role} peak RSS") > self.policy.per_process_rss_limit_bytes:
                raise Refusal("telemetry RSS exceeds limit")
            if _integer(mapped[role], f"{role} peak mapped bytes") \
                    != self.policy.role_paths(role).mapped_peak_limit_bytes:
                raise Refusal("telemetry mapped peak certificate mismatch")
            if type(exits[role]) is not int or exits[role] != 0:
                raise Refusal("telemetry exit code is not exact zero")
            _path(output_paths[role], self.policy.role_paths(role).output, f"{role} output")
            _sha256(output_hashes[role], f"{role} output SHA-256")
            launch_values[role] = launch
            completion_values[role] = completion
            samples = runtime_samples[role]
            if type(samples) is not list or not samples:
                raise Refusal("runtime samples must be a nonempty exact list")
            sample_epochs: list[int] = []
            sample_rss: list[int] = []
            for index, value in enumerate(samples):
                sample = _keys(value, {
                    "captured_epoch", "rss_bytes",
                    "process_id", "process_start_token", "executable_path",
                    "executable_sha256",
                }, f"{role} runtime sample {index}")
                if (
                    sample["process_id"] != identities[role]["process_id"]
                    or type(sample["process_id"]) is not int
                    or sample["process_start_token"]
                    != identities[role]["process_start_token"]
                    or sample["executable_path"] != identities[role]["executable_path"]
                    or sample["executable_sha256"]
                    != identities[role]["executable_sha256"]
                ):
                    raise Refusal("runtime sample worker identity mismatch")
                sample_epochs.append(_integer(
                    sample["captured_epoch"], f"{role} runtime sample epoch"
                ))
                sample_rss.append(_integer(
                    sample["rss_bytes"], f"{role} runtime sample RSS"
                ))
            if sample_epochs != sorted(set(sample_epochs)):
                raise Refusal("runtime sample epochs are not strictly ordered")
            if sample_epochs[0] > launch or sample_epochs[-1] < completion:
                raise Refusal("runtime samples do not cover the role execution")
            if any(later - earlier > self.policy.maximum_sample_interval_seconds
                   for earlier, later in zip(sample_epochs, sample_epochs[1:])):
                raise Refusal("runtime sample interval exceeds limit")
            if max(sample_rss) != rss[role]:
                raise Refusal("runtime RSS peak does not reconstruct")
            if any(value > self.policy.per_process_rss_limit_bytes
                   for value in sample_rss):
                raise Refusal("runtime RSS sample exceeds limit")
        if abs(launch_values[ROLES[0]] - launch_values[ROLES[1]]) \
                > self.policy.maximum_launch_skew_seconds:
            raise Refusal("telemetry launch skew exceeds limit")

        samples = record["free_disk_bytes_samples"]
        if type(samples) is not list or not samples:
            raise Refusal("disk samples must be a nonempty exact list")
        sample_epochs: list[int] = []
        for index, value in enumerate(samples):
            sample = _keys(value, {
                "captured_epoch", "workspace_filesystem_device", "free_bytes",
            }, f"disk sample {index}")
            epoch = _integer(sample["captured_epoch"], "disk sample epoch")
            _integer(sample["workspace_filesystem_device"], "disk sample device")
            if _integer(sample["free_bytes"], "disk sample free bytes") \
                    < self.policy.minimum_workspace_free_disk_bytes:
                raise Refusal("disk sample is below limit")
            if sample["workspace_filesystem_device"] \
                    != self.accepted_record("schedule")["resource_snapshot"]["workspace_filesystem_device"]:
                raise Refusal("disk sample filesystem changed")
            sample_epochs.append(epoch)
        if sample_epochs != sorted(set(sample_epochs)):
            raise Refusal("disk sample epochs are not strictly ordered")
        if sample_epochs[0] > min(launch_values.values()) \
                or sample_epochs[-1] < max(completion_values.values()):
            raise Refusal("disk samples do not cover the run")
        if any(later - earlier > self.policy.maximum_sample_interval_seconds
               for earlier, later in zip(sample_epochs, sample_epochs[1:])):
            raise Refusal("disk sample interval exceeds limit")
        if record["claim_boundary"] != "POSTRUN_RUNTIME_EVIDENCE_ONLY__NO_FINAL_L12_ADJUDICATION":
            raise Refusal("telemetry claim boundary mismatch")
        return record


def public_signature_census() -> dict[str, tuple[str, ...]]:
    """Return the coordinator API signature used by integration checks."""
    names = (
        "admit_schedule", "admit_schedule_audit", "admit_authorization",
        "commit_handshake", "release_workers", "release_command",
        "admit_release_ack", "admit_worker_completion",
        "admit_postrun_telemetry",
    )
    return {
        name: tuple(inspect.signature(getattr(DualLaunchCoordinator, name)).parameters)
        for name in names
    }
