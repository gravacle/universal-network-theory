#!/usr/bin/env python3
"""Deterministic, in-memory fixtures for the V012 dual-launch coordinator."""

from __future__ import annotations

import hashlib
from copy import deepcopy

from dual_launch_coordinator import (
    ROLES,
    DualLaunchCoordinator,
    LaunchPolicy,
    RolePaths,
    _release_token,
    nonce_commitment,
    record_sha256,
    release_ack_sha256,
)


EPOCH = 1_900_000_100


def _digest(label: str) -> str:
    return hashlib.sha256(label.encode("ascii")).hexdigest()


def synthetic_policy() -> LaunchPolicy:
    return LaunchPolicy(
        target=RolePaths(
            executable="/synthetic/v012/target/consume_target_cache.py",
            workspace="/synthetic/v012/target/workspace_L12",
            output="/synthetic/v012/target/HISTORY_L12.json",
            mapped_peak_limit_bytes=252_944_080,
        ),
        hostile=RolePaths(
            executable="/synthetic/v004r4/hostile/consume_cache_v004r4.py",
            workspace="/synthetic/v004r4/hostile/workspace_L12",
            output="/synthetic/v004r4/hostile/HISTORY_L12.json",
            mapped_peak_limit_bytes=252_944_080,
        ),
        telemetry_path=(
            "/synthetic/AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
            "SHARED_AGGREGATE_TELEMETRY_V001.json"
        ),
    )


def build_fixture_bundle() -> dict[str, object]:
    policy = synthetic_policy()
    schedule = {
        "schema": "V012_DUAL_L12_READINESS_SCHEDULE_V001",
        "classification": "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT",
        "created_epoch": EPOCH - 100,
        "expires_epoch": EPOCH + 200,
        "l10_cross_gate_sha256": _digest("l10-cross-gate"),
        "resource_snapshot": {
            "captured_epoch": EPOCH - 90,
            "host_physical_memory_bytes": 48_000_000_000,
            "available_memory_bytes": 34_865_626_528,
            "workspace_free_disk_bytes": 19_201_889_580,
            "workspace_filesystem_device": 17,
            "both_workspace_roots_same_filesystem": True,
            "memory_pressure": "NORMAL",
            "passes": True,
        },
        "schedule": {
            "launch_mode": "PRELAUNCHED_BLOCKED_TWO_WORKER",
            "release_only_after_both_l12_authorizations": True,
            "launch_skew_seconds_max": 60,
            "per_process_rss_limit_bytes": 17_179_869_184,
            "per_process_wall_limit_seconds": 108_000,
            "mapped_peak_limit_bytes_by_role": {
                role: policy.role_paths(role).mapped_peak_limit_bytes for role in ROLES
            },
        },
        "roles": {
            role: {
                "role": role,
                "worker_executable_path": policy.role_paths(role).executable,
                "workspace_path": policy.role_paths(role).workspace,
                "output_path": policy.role_paths(role).output,
                "ready_for_blocked_worker_start": True,
            }
            for role in ROLES
        },
        "telemetry": {
            "path": policy.telemetry_path,
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "must_be_absent_before_release": True,
            "absent_at_schedule_capture": True,
            "sample_interval_seconds_max": 60,
        },
        "claim_boundary": "READINESS_AND_RESOURCE_SCHEDULING_ONLY__NO_L12_RELEASE_OR_RESULT",
    }
    schedule_sha = record_sha256(schedule)
    checks = {
        "schedule_exact_schema": 1,
        "deep_exact_types": 1,
        "two_role_path_custody": 2,
        "normal_memory_pressure": 1,
        "resource_thresholds": 4,
        "freshness_window": 1,
        "telemetry_prelaunch_absence": 1,
    }
    audit = {
        "schema": "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001",
        "classification": "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT",
        "auditor_role": "INDEPENDENT_DUAL_LAUNCH_COORDINATOR_REVIEW",
        "schedule_sha256": schedule_sha,
        "l10_cross_gate_sha256": schedule["l10_cross_gate_sha256"],
        "checks": checks,
        "checks_total": sum(checks.values()),
        "checks_passed": sum(checks.values()),
        "failures": [],
        "claim_boundary": "INDEPENDENT_READINESS_AUDIT_ONLY__NO_L12_AUTHORIZATION_RELEASE_OR_RESULT",
    }
    audit_sha = record_sha256(audit)
    authorizations = {}
    for role in ROLES:
        target = role == "target_v012"
        authorizations[role] = {
            "schema": (
                "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001" if target
                else "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001"
            ),
            "classification": (
                "AUTHORIZE_TARGET_V012_L12_AFTER_SCHEDULE_AUDIT" if target
                else "AUTHORIZE_HOSTILE_V004R4_L12_AFTER_SCHEDULE_AUDIT"
            ),
            "role": role,
            "authorized_length": 12,
            "schedule_sha256": schedule_sha,
            "schedule_audit_sha256": audit_sha,
            "l10_cross_gate_sha256": schedule["l10_cross_gate_sha256"],
            "consumer_sha256": _digest(f"{role}-consumer"),
            "l12_cache_manifest_sha256": _digest(f"{role}-l12-cache"),
            "claim_boundary": "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT",
        }
    auth_hashes = {
        role: record_sha256(authorizations[role]) for role in ROLES
    }
    nonces = {
        "target_v012": bytes(range(32)),
        "hostile_v004r4": bytes(range(32, 64)),
    }
    workers = {}
    for index, role in enumerate(ROLES):
        paths = policy.role_paths(role)
        workers[role] = {
            "schema": "V012_L12_WORKER_READY_V001",
            "role": role,
            "worker_id": f"synthetic-{role}-worker",
            "process_id": 41001 + index,
            "process_start_token": _digest(f"{role}-process-start"),
            "executable_path": paths.executable,
            "executable_sha256": _digest(f"{role}-executable"),
            "workspace_path": paths.workspace,
            "output_path": paths.output,
            "control_channel_id": _digest(f"{role}-channel"),
            "nonce_commitment_sha256": nonce_commitment(nonces[role]),
            "ready_epoch": EPOCH + 10 * index,
            "blocked_on_release": True,
        }
    handshake = {
        "schema": "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002",
        "classification": "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS",
        "created_epoch": EPOCH + 10,
        "schedule_sha256": schedule_sha,
        "schedule_audit_sha256": audit_sha,
        "authorization_sha256_by_role": auth_hashes,
        "memory_pressure": "NORMAL",
        "workers": workers,
        "ready_sha256_by_role": {
            role: record_sha256(workers[role]) for role in ROLES
        },
        "observed_readiness_skew_seconds": 10,
        "launch_skew_seconds_max": 60,
        "telemetry": {
            "path": policy.telemetry_path,
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "absent_before_release": True,
        },
        "claim_boundary": "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT",
    }
    handshake_sha = record_sha256(handshake)
    release_epochs = {"target_v012": EPOCH + 11, "hostile_v004r4": EPOCH + 12}
    release = {
        "schema": "V012_DUAL_L12_WORKER_RELEASE_V002",
        "classification": "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS",
        "handshake_sha256": handshake_sha,
        "authorization_sha256_by_role": auth_hashes,
        "release_epoch_by_role": release_epochs,
        "observed_launch_skew_seconds": 1,
        "release_by_role": {
            role: {
                "role": role,
                "worker_id": handshake["workers"][role]["worker_id"],
                "process_id": handshake["workers"][role]["process_id"],
                "process_start_token": handshake["workers"][role]["process_start_token"],
                "control_channel_id": handshake["workers"][role]["control_channel_id"],
                "nonce_commitment_sha256": handshake["workers"][role]["nonce_commitment_sha256"],
                "release_token_sha256": _release_token(
                    handshake_sha, role, release_epochs[role]
                ),
            }
            for role in ROLES
        },
        "claim_boundary": "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT",
    }
    release_sha = record_sha256(release)
    commands = {}
    acks = {}
    for role in ROLES:
        worker = workers[role]
        commands[role] = {
            "schema": "V012_L12_WORKER_RELEASE_COMMAND_V001",
            "role": role,
            "worker_id": worker["worker_id"],
            "process_id": worker["process_id"],
            "process_start_token": worker["process_start_token"],
            "control_channel_id": worker["control_channel_id"],
            "nonce_commitment_sha256": worker["nonce_commitment_sha256"],
            "handshake_sha256": handshake_sha,
            "worker_release_sha256": release_sha,
            "release_epoch": release_epochs[role],
        }
        acks[role] = {
            "schema": "V012_L12_WORKER_RELEASE_ACK_V001",
            "role": role,
            "worker_id": worker["worker_id"],
            "process_id": worker["process_id"],
            "process_start_token": worker["process_start_token"],
            "control_channel_id": worker["control_channel_id"],
            "nonce_hex": nonces[role].hex(),
            "ack_sha256": release_ack_sha256(nonces[role], commands[role]),
        }
    identities = {
        role: {
            key: workers[role][key] for key in (
                "worker_id", "process_id", "process_start_token",
                "executable_path", "executable_sha256", "control_channel_id",
                "nonce_commitment_sha256",
            )
        }
        for role in ROLES
    }
    completion_epochs = {
        "target_v012": EPOCH + 111,
        "hostile_v004r4": EPOCH + 132,
    }
    completions = {
        role: {
            "schema": "V012_L12_WORKER_COMPLETION_V001",
            "role": role,
            "worker_id": workers[role]["worker_id"],
            "process_id": workers[role]["process_id"],
            "process_start_token": workers[role]["process_start_token"],
            "control_channel_id": workers[role]["control_channel_id"],
            "output_path": policy.role_paths(role).output,
            "output_sha256": _digest(f"{role}-output"),
            "completion_epoch": completion_epochs[role],
            "blocked_on_orchestrator_close": True,
        }
        for role in ROLES
    }
    telemetry = {
        "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
        "classification": "COMPLETE_SHARED_L12_TELEMETRY",
        "shared_gate_sha256": schedule_sha,
        "schedule_audit_sha256": audit_sha,
        "dual_launch_handshake_sha256": handshake_sha,
        "worker_release_sha256": release_sha,
        "authorization_sha256_by_role": auth_hashes,
        "worker_identity_by_role": identities,
        "release_command_sha256_by_role": {
            role: record_sha256(commands[role]) for role in ROLES
        },
        "release_ack_sha256_by_role": {
            role: record_sha256(acks[role]) for role in ROLES
        },
        "completion_sha256_by_role": {
            role: record_sha256(completions[role]) for role in ROLES
        },
        "launch_epoch_by_role": release_epochs,
        "completion_epoch_by_role": completion_epochs,
        "wall_seconds_by_role": {
            "target_v012": 100.0,
            "hostile_v004r4": 120.0,
        },
        "peak_rss_bytes_by_role": {
            "target_v012": 16_000_000_000,
            "hostile_v004r4": 16_100_000_000,
        },
        "rss_peak_semantics": (
            "LAUNCHER_SAMPLED_CURRENT_RSS_AT_MOST_30_SECONDS__"
            "NOT_OS_HIGH_WATER"
        ),
        "peak_mapped_bytes_by_role": {
            role: policy.role_paths(role).mapped_peak_limit_bytes
            for role in ROLES
        },
        "mapped_peak_semantics": (
            "CONSERVATIVE_AUTHENTICATION_CACHE_CERTIFICATE__"
            "NOT_OS_VIRTUAL_MEMORY"
        ),
        "runtime_samples_by_role": {
            "target_v012": [
                {"captured_epoch": EPOCH + 11, "rss_bytes": 15_000_000_000,
                 **{key: identities["target_v012"][key] for key in ("process_id", "process_start_token", "executable_path", "executable_sha256")}},
                {"captured_epoch": EPOCH + 71, "rss_bytes": 16_000_000_000,
                 **{key: identities["target_v012"][key] for key in ("process_id", "process_start_token", "executable_path", "executable_sha256")}},
                {"captured_epoch": EPOCH + 111, "rss_bytes": 15_500_000_000,
                 **{key: identities["target_v012"][key] for key in ("process_id", "process_start_token", "executable_path", "executable_sha256")}},
            ],
            "hostile_v004r4": [
                {"captured_epoch": EPOCH + 12, "rss_bytes": 15_100_000_000,
                 **{key: identities["hostile_v004r4"][key] for key in ("process_id", "process_start_token", "executable_path", "executable_sha256")}},
                {"captured_epoch": EPOCH + 72, "rss_bytes": 16_100_000_000,
                 **{key: identities["hostile_v004r4"][key] for key in ("process_id", "process_start_token", "executable_path", "executable_sha256")}},
                {"captured_epoch": EPOCH + 132, "rss_bytes": 15_600_000_000,
                 **{key: identities["hostile_v004r4"][key] for key in ("process_id", "process_start_token", "executable_path", "executable_sha256")}},
            ],
        },
        "free_disk_bytes_samples": [
            {"captured_epoch": EPOCH + 11, "workspace_filesystem_device": 17,
             "free_bytes": 19_201_889_580},
            {"captured_epoch": EPOCH + 71, "workspace_filesystem_device": 17,
             "free_bytes": 19_201_889_580},
            {"captured_epoch": EPOCH + 131, "workspace_filesystem_device": 17,
             "free_bytes": 19_201_889_580},
            {"captured_epoch": EPOCH + 132, "workspace_filesystem_device": 17,
             "free_bytes": 19_201_889_580},
        ],
        "exit_code_by_role": {role: 0 for role in ROLES},
        "output_path_by_role": {
            role: policy.role_paths(role).output for role in ROLES
        },
        "output_sha256_by_role": {
            role: _digest(f"{role}-output") for role in ROLES
        },
        "claim_boundary": "POSTRUN_RUNTIME_EVIDENCE_ONLY__NO_FINAL_L12_ADJUDICATION",
    }
    return {
        "policy": policy,
        "evaluation_epoch": EPOCH,
        "schedule": schedule,
        "schedule_audit": audit,
        "target_authorization": authorizations["target_v012"],
        "hostile_authorization": authorizations["hostile_v004r4"],
        "handshake": handshake,
        "release": release,
        "release_commands": commands,
        "release_acks": acks,
        "completions": completions,
        "telemetry": telemetry,
    }


def fresh_bundle() -> dict[str, object]:
    return deepcopy(build_fixture_bundle())


def valid_coordinator_through(node: str = "telemetry") -> DualLaunchCoordinator:
    bundle = fresh_bundle()
    coordinator = DualLaunchCoordinator(bundle["policy"], bundle["evaluation_epoch"])
    order = (
        "schedule", "schedule_audit", "target_authorization",
        "hostile_authorization", "handshake", "release", "target_ack",
        "hostile_ack", "target_completion", "hostile_completion", "telemetry",
    )
    methods = {
        "schedule": coordinator.admit_schedule,
        "schedule_audit": coordinator.admit_schedule_audit,
        "target_authorization": coordinator.admit_authorization,
        "hostile_authorization": coordinator.admit_authorization,
        "handshake": coordinator.commit_handshake,
        "release": coordinator.release_workers,
        "target_ack": lambda _record: coordinator.admit_release_ack(
            bundle["release_commands"]["target_v012"],
            bundle["release_acks"]["target_v012"],
        ),
        "hostile_ack": lambda _record: coordinator.admit_release_ack(
            bundle["release_commands"]["hostile_v004r4"],
            bundle["release_acks"]["hostile_v004r4"],
        ),
        "target_completion": lambda _record: coordinator.admit_worker_completion(
            bundle["completions"]["target_v012"],
        ),
        "hostile_completion": lambda _record: coordinator.admit_worker_completion(
            bundle["completions"]["hostile_v004r4"],
        ),
        "telemetry": coordinator.admit_postrun_telemetry,
    }
    for name in order:
        methods[name](bundle.get(name))
        if name == node:
            return coordinator
    raise ValueError(f"unknown fixture node: {node}")
