#!/usr/bin/env python3
"""Read-only plan for preserving failed L12 launch evidence and retrying once.

This DEVELOPMENT-only program authenticates the first launch attempt, confirms
that no history workspace/output was created, and prints the exact namespace
reserved for a future V002 retry.  It never publishes, deletes, moves, launches,
or creates a canonical record.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
SHARED_V001: Final[Path] = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
SHARED_RETRY_V002: Final[Path] = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002"
TARGET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
RETIREMENT_PACKET: Final[Path] = ROOT / "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001"
RETIREMENT_ROOT: Final[Path] = (
    RETIREMENT_PACKET / "RETIRED_CANONICAL_A01_A17_PRE_A18_REPAIR_V001"
)


class PlanRefusal(RuntimeError):
    """The read-only recovery plan refused a changed or ambiguous tree."""


@dataclass(frozen=True)
class Artifact:
    name: str
    path: Path
    sha256: str
    schema: str | None = None
    classification: str | None = None
    exact_raw: bytes | None = None


PRESENT_ATTEMPT_ARTIFACTS: Final[tuple[Artifact, ...]] = (
    Artifact(
        "A20 schedule",
        SHARED_V001 / "SHARED_AGGREGATE_SCHEDULE_GATE_V001.json",
        "9d87a8bed36c4daa366f956b5103873ad254e7f21bd0d2d67b779eccbb857d67",
        "V012_DUAL_L12_READINESS_SCHEDULE_V001",
        "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT",
    ),
    Artifact(
        "A21 schedule audit",
        SHARED_V001 / "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json",
        "2eee41e771ba228d6461045b282eb250686d790ef01c3030a1e9f55612951297",
        "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001",
        "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT",
    ),
    Artifact(
        "A22 target authorization",
        TARGET / "TARGET_L12_EXECUTION_GATE_V012.json",
        "44ed80086a7f7fbc562961b7723386d61175889a9f6b18dc039ce44f7bff5282",
        "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001",
        "AUTHORIZE_TARGET_V012_L12_AFTER_SCHEDULE_AUDIT",
    ),
    Artifact(
        "A22 hostile authorization",
        HOSTILE / "HOSTILE_L12_EXECUTION_GATE_V004R4.json",
        "ffa8a12657706799d74e9a10d697cff4b24f9648ad36bf363d308cc6a6157ac4",
        "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001",
        "AUTHORIZE_HOSTILE_V004R4_L12_AFTER_SCHEDULE_AUDIT",
    ),
    Artifact(
        "target READY",
        SHARED_V001 / "TARGET_V012_WORKER_READY_V001.json",
        "36f8a5b18d7bc0a296e80f51f9073a607528368588bfc2e635897114a5820b13",
        "V012_L12_WORKER_READY_V001",
    ),
    Artifact(
        "hostile READY",
        SHARED_V001 / "HOSTILE_V004R4_WORKER_READY_V001.json",
        "296ac9b6be0184bb2df5488a3450922647b952533744fe4009ffdcb1e07e2750",
        "V012_L12_WORKER_READY_V001",
    ),
    Artifact(
        "blocked-worker handshake",
        SHARED_V001 / "DUAL_L12_LAUNCH_HANDSHAKE_V002.json",
        "ecc4b3c6eee52af71660551868265adf39faf5176976fcb5913e6578dbed3289",
        "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002",
        "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS",
    ),
    Artifact(
        "dual release",
        SHARED_V001 / "DUAL_L12_WORKER_RELEASE_V002.json",
        "ad9029911ecd73f5ffc3066da796ef6e60ce39528e42ba765ec7dc31cb4f8567",
        "V012_DUAL_L12_WORKER_RELEASE_V002",
        "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS",
    ),
    Artifact(
        "target release command",
        SHARED_V001 / "TARGET_V012_WORKER_RELEASE_COMMAND_V001.json",
        "081bb53255dedcbe56b56f52425cf3827ed7f6f82922884308dbfee01521ef69",
        "V012_L12_WORKER_RELEASE_COMMAND_V001",
    ),
    Artifact(
        "hostile release command",
        SHARED_V001 / "HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json",
        "af5ba939b71ba8112f0c24965b681c8e857265dd5f2ec31f11a5719f91f2a704",
        "V012_L12_WORKER_RELEASE_COMMAND_V001",
    ),
    Artifact(
        "target failure log",
        SHARED_V001 / "TARGET_V012_WORKER_LOG_V001.txt",
        "71c3436ee4d13f096cd07e5bff645fcdf1ded15b0fa8e90b10ed525c297be603",
        exact_raw=b"REFUSED: kernel process start record is malformed\n",
    ),
    Artifact(
        "hostile failure log",
        SHARED_V001 / "HOSTILE_V004R4_WORKER_LOG_V001.txt",
        "012cb342797b3ea04118ad747dcfe78f685aef3fedf41851ab8bc6d59990d63a",
        exact_raw=b"REFUSE: target V012 freeze hash mismatch\n",
    ),
)


UNCHANGED_FINAL_PATHS: Final[dict[str, Path]] = {
    "target_workspace": TARGET / "WORKSPACES/L12",
    "hostile_workspace": HOSTILE / "V004R4_WORKSPACES/L12",
    "target_history": TARGET / "PHYSICAL_OUTPUTS/HISTORY_L12.json",
    "hostile_history": HOSTILE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json",
}

ABSENT_ATTEMPT_PATHS: Final[dict[str, Path]] = {
    "target_ack": SHARED_V001 / "TARGET_V012_WORKER_RELEASE_ACK_V001.json",
    "hostile_ack": SHARED_V001 / "HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
    "target_completion": SHARED_V001 / "TARGET_V012_WORKER_COMPLETION_V001.json",
    "hostile_completion": SHARED_V001 / "HOSTILE_V004R4_WORKER_COMPLETION_V001.json",
    "telemetry": SHARED_V001 / "SHARED_AGGREGATE_TELEMETRY_V001.json",
    **UNCHANGED_FINAL_PATHS,
}

RETRY_CONTROL_PATHS: Final[dict[str, Path]] = {
    "obstruction_custody": SHARED_RETRY_V002 / "FAILED_L12_LAUNCH_OBSTRUCTION_CUSTODY_V001.json",
    "schedule": SHARED_RETRY_V002 / "SHARED_AGGREGATE_SCHEDULE_GATE_RETRY_V002.json",
    "schedule_audit": SHARED_RETRY_V002 / "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_RETRY_V002.json",
    "target_authorization": TARGET / "TARGET_L12_EXECUTION_GATE_RETRY_V002.json",
    "hostile_authorization": HOSTILE / "HOSTILE_L12_EXECUTION_GATE_RETRY_V002.json",
    "target_ready": SHARED_RETRY_V002 / "TARGET_V012_WORKER_READY_RETRY_V002.json",
    "hostile_ready": SHARED_RETRY_V002 / "HOSTILE_V004R4_WORKER_READY_RETRY_V002.json",
    "handshake": SHARED_RETRY_V002 / "DUAL_L12_LAUNCH_HANDSHAKE_RETRY_V002.json",
    "release": SHARED_RETRY_V002 / "DUAL_L12_WORKER_RELEASE_RETRY_V002.json",
    "target_release_command": SHARED_RETRY_V002 / "TARGET_V012_WORKER_RELEASE_COMMAND_RETRY_V002.json",
    "hostile_release_command": SHARED_RETRY_V002 / "HOSTILE_V004R4_WORKER_RELEASE_COMMAND_RETRY_V002.json",
    "target_ack": SHARED_RETRY_V002 / "TARGET_V012_WORKER_RELEASE_ACK_RETRY_V002.json",
    "hostile_ack": SHARED_RETRY_V002 / "HOSTILE_V004R4_WORKER_RELEASE_ACK_RETRY_V002.json",
    "target_completion": SHARED_RETRY_V002 / "TARGET_V012_WORKER_COMPLETION_RETRY_V002.json",
    "hostile_completion": SHARED_RETRY_V002 / "HOSTILE_V004R4_WORKER_COMPLETION_RETRY_V002.json",
    "telemetry": SHARED_RETRY_V002 / "SHARED_AGGREGATE_TELEMETRY_RETRY_V002.json",
    "target_log": SHARED_RETRY_V002 / "TARGET_V012_WORKER_LOG_RETRY_V002.txt",
    "hostile_log": SHARED_RETRY_V002 / "HOSTILE_V004R4_WORKER_LOG_RETRY_V002.txt",
}

TARGET_CONSUMER: Final[Artifact] = Artifact(
    "unchanged target physical consumer",
    TARGET / "consume_target_cache.py",
    "80b2ce08af37bc8cffd91f07146c777f60785883436361ca9521597763fd5a11",
)
HOSTILE_CONSUMER: Final[Artifact] = Artifact(
    "unchanged hostile physical consumer",
    HOSTILE / "consume_cache_v004r4.py",
    "700dce18ec8f50008a9e3022394a55c8d689268e21b80982896d37b92add7b74",
)
HOSTILE_BUILD_AUTHORIZATION: Final[Artifact] = Artifact(
    "hostile cache-build authorization",
    HOSTILE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json",
    "58ae7037de078d1d3cd7ac0de48d4cb15c176274871e90c6d7cf231d1d12dd05",
    "HOSTILE_V004R4_CACHE_BUILD_AUTHORIZATION_GATE",
    "AUTHORIZE_HOSTILE_V004R4_CACHE_AFTER_INDEPENDENT_AUDIT",
)
RETIREMENT_CENSUS: Final[Artifact] = Artifact(
    "A01-A17 retirement census",
    RETIREMENT_PACKET / "RETIREMENT_CENSUS_V001.json",
    "dc63434d16e8fa8722123f79aeef964b49fac864c2ec11984539ff6bdf641357",
    "V012_A01_A17_PRE_A18_RETIREMENT_CENSUS_V001",
    "EXACT_NONEXECUTED_OWNER_ONCE_RETIREMENT_CENSUS",
)

HISTORICAL_TARGET_INTERFACE: Final[tuple[Artifact, ...]] = (
    Artifact(
        "historical target freeze",
        RETIREMENT_ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
        "b3a4ba272c7ed36cb46416443179832e0ddf1c4ac053534369299f9ca019a903",
        "TARGET_L12_STORAGE_CACHE_FREEZE_V012",
    ),
    Artifact(
        "historical target audit",
        RETIREMENT_ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
        "ad5686920481060d9a6208c20367530f6081b1eb40b896fe39db592a19dab764",
        "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001",
        "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE",
    ),
    Artifact(
        "historical target L10 gate",
        RETIREMENT_ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
        "4a0a8959b5a5286bd0d52275fa6ac55ef2be68e7d2c6aa6f98ebf7a306eddd12",
        "TARGET_V012_CACHED_L10_GATE",
        "PASS_TARGET_V012_CACHED_L10",
    ),
    Artifact(
        "historical target L12 manifest",
        RETIREMENT_ROOT / (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json"
        ),
        "f3d632fad10711e519750d4d0332768dc8df13c095eaee40e91ec5c1145f7a63",
        "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
    ),
)

FUTURE_HOSTILE_ADAPTER_PATH: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_FAILED_LAUNCH_RECOVERY_V002"
    / "hostile_historical_interface_adapter.py"
)


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _canonical_under_root(path: Path, label: str) -> None:
    if (
        not path.is_absolute() or path == ROOT or ROOT not in path.parents
        or Path(str(path)) != path or "\x00" in str(path)
    ):
        raise PlanRefusal(f"{label} path is outside the exact repository")
    cursor = ROOT
    for component in path.relative_to(ROOT).parts[:-1]:
        cursor /= component
        if not os.path.lexists(cursor):
            break
        metadata = os.lstat(cursor)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise PlanRefusal(f"{label} parent is aliased or special")


def _strict_json(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise PlanRefusal(f"{label} duplicate JSON key")
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise PlanRefusal(f"{label} nonfinite JSON constant")

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=constant,
        )
    except PlanRefusal:
        raise
    except (UnicodeDecodeError, ValueError, TypeError) as error:
        raise PlanRefusal(f"{label} is not strict ASCII JSON") from error
    if type(value) is not dict:
        raise PlanRefusal(f"{label} is not one JSON object")
    return value


def _authenticate(artifact: Artifact) -> dict[str, object] | None:
    _canonical_under_root(artifact.path, artifact.name)
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(artifact.path, flags)
    try:
        before = os.fstat(descriptor)
        named = os.stat(artifact.path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_mode & 0o222 or before.st_nlink != 1
            or _identity(before) != _identity(named)
        ):
            raise PlanRefusal(f"{artifact.name} is writable, linked, or special")
        raw = bytearray()
        offset = 0
        while offset < before.st_size:
            block = os.pread(descriptor, min(2**20, before.st_size - offset), offset)
            if not block:
                raise PlanRefusal(f"{artifact.name} retained read was short")
            raw.extend(block)
            offset += len(block)
        after = os.fstat(descriptor)
        named_after = os.stat(artifact.path, follow_symlinks=False)
        digest = hashlib.sha256(raw).hexdigest()
        if (
            digest != artifact.sha256 or _identity(after) != _identity(before)
            or _identity(named_after) != _identity(before)
        ):
            raise PlanRefusal(f"{artifact.name} hash or identity mismatch")
        exact = bytes(raw)
        if artifact.exact_raw is not None:
            if exact != artifact.exact_raw:
                raise PlanRefusal(f"{artifact.name} exact failure text mismatch")
            return None
        if artifact.schema is None and artifact.classification is None:
            return None
        record = _strict_json(exact, artifact.name)
        if record.get("schema") != artifact.schema:
            raise PlanRefusal(f"{artifact.name} schema mismatch")
        if (
            artifact.classification is not None
            and record.get("classification") != artifact.classification
        ):
            raise PlanRefusal(f"{artifact.name} classification mismatch")
        return record
    finally:
        os.close(descriptor)


def _require_absent(path: Path, label: str) -> None:
    _canonical_under_root(path, label)
    if os.path.lexists(path):
        raise PlanRefusal(f"{label} is already occupied")


def build_plan() -> dict[str, object]:
    if len(PRESENT_ATTEMPT_ARTIFACTS) != 12 or len(ABSENT_ATTEMPT_PATHS) != 9:
        raise PlanRefusal("failed-attempt census cardinality mismatch")
    for artifact in PRESENT_ATTEMPT_ARTIFACTS:
        _authenticate(artifact)
    for name, path in ABSENT_ATTEMPT_PATHS.items():
        _require_absent(path, f"failed-attempt absence {name}")

    for artifact in (
        TARGET_CONSUMER, HOSTILE_CONSUMER, HOSTILE_BUILD_AUTHORIZATION,
        RETIREMENT_CENSUS, *HISTORICAL_TARGET_INTERFACE,
    ):
        _authenticate(artifact)

    build_gate = _authenticate(HOSTILE_BUILD_AUTHORIZATION)
    if not isinstance(build_gate, dict):
        raise PlanRefusal("hostile build authorization record is absent")
    interface = build_gate.get("target_v012_interface")
    expected_interface_hashes = {
        "freeze_sha256": HISTORICAL_TARGET_INTERFACE[0].sha256,
        "audit_sha256": HISTORICAL_TARGET_INTERFACE[1].sha256,
        "L10_gate_sha256": HISTORICAL_TARGET_INTERFACE[2].sha256,
        "L12_cache_manifest_sha256": HISTORICAL_TARGET_INTERFACE[3].sha256,
        "consumer_sha256": TARGET_CONSUMER.sha256,
    }
    if (
        type(interface) is not dict
        or any(interface.get(key) != value for key, value in expected_interface_hashes.items())
    ):
        raise PlanRefusal("historical target interface hash projection mismatch")

    retry_paths = tuple(RETRY_CONTROL_PATHS.values())
    final_paths = tuple(UNCHANGED_FINAL_PATHS.values())
    prior_paths = tuple(item.path for item in PRESENT_ATTEMPT_ARTIFACTS)
    all_future = retry_paths + final_paths
    if (
        len(RETRY_CONTROL_PATHS) != 18 or len(set(retry_paths)) != len(retry_paths)
        or len(set(all_future)) != 22
        or set(retry_paths) & set(prior_paths)
        or set(retry_paths) & set(final_paths)
    ):
        raise PlanRefusal("retry namespace is incomplete or colliding")
    for name, path in RETRY_CONTROL_PATHS.items():
        _require_absent(path, f"future retry control {name}")

    _require_absent(FUTURE_HOSTILE_ADAPTER_PATH, "future hostile adapter")
    return {
        "schema": "V012_L12_FAILED_LAUNCH_RECOVERY_PLAN_V001",
        "classification": "PASS_DEVELOPMENT_ONLY_FAILED_LAUNCH_CUSTODY_AND_RETRY_PLAN",
        "failed_attempt": {
            "present_count": 12,
            "present_sha256_by_path": {
                str(item.path): item.sha256 for item in PRESENT_ATTEMPT_ARTIFACTS
            },
            "absent_count": 9,
            "absent_paths": [str(path) for path in ABSENT_ATTEMPT_PATHS.values()],
            "worker_release_occurred": True,
            "physical_history_compute_began": False,
            "primary_obstruction": (
                "HOSTILE_HISTORICAL_TARGET_INTERFACE_RESOLVED_AGAINST_"
                "CURRENT_ACTIVE_PATH"
            ),
            "target_failure_classification": "SECONDARY_PEER_EXIT_CASCADE",
        },
        "historical_interface_custody": {
            "hostile_build_authorization_sha256": HOSTILE_BUILD_AUTHORIZATION.sha256,
            "retirement_census_sha256": RETIREMENT_CENSUS.sha256,
            "retired_sha256_by_path": {
                str(item.path): item.sha256 for item in HISTORICAL_TARGET_INTERFACE
            },
            "current_hash_substitution_permitted": False,
        },
        "retry_v002": {
            "control_path_count": len(RETRY_CONTROL_PATHS),
            "control_paths": {name: str(path) for name, path in RETRY_CONTROL_PATHS.items()},
            "unchanged_final_paths": {
                name: str(path) for name, path in UNCHANGED_FINAL_PATHS.items()
            },
            "physical_consumers": {
                "target_v012": {
                    "path": str(TARGET_CONSUMER.path),
                    "sha256": TARGET_CONSUMER.sha256,
                    "must_remain_unchanged": True,
                },
                "hostile_v004r4": {
                    "path": str(HOSTILE_CONSUMER.path),
                    "sha256": HOSTILE_CONSUMER.sha256,
                    "must_remain_unchanged": True,
                },
            },
            "future_hostile_adapter": {
                "path": str(FUTURE_HOSTILE_ADAPTER_PATH),
                "status": "ABSENT_NOT_YET_IMPLEMENTED_OR_FROZEN",
                "required_bindings": {
                    "hostile_physical_consumer_sha256": HOSTILE_CONSUMER.sha256,
                    "hostile_build_authorization_sha256": HOSTILE_BUILD_AUTHORIZATION.sha256,
                    "retirement_census_sha256": RETIREMENT_CENSUS.sha256,
                    "historical_target_interface_sha256": [
                        item.sha256 for item in HISTORICAL_TARGET_INTERFACE
                    ],
                },
                "permitted_change": "CONTROL_PATH_AND_HISTORICAL_CUSTODY_ROUTING_ONLY",
                "physical_operator_change_permitted": False,
            },
            "owner_once_no_delete_no_overwrite": True,
            "execution_ready": False,
            "blocking_preconditions": [
                "PUBLISH_FAILED_ATTEMPT_OBSTRUCTION_CUSTODY_OWNER_ONCE",
                "IMPLEMENT_FREEZE_AND_HOSTILE_SCREEN_FUTURE_ADAPTER",
                "BIND_ADAPTER_AND_UNCHANGED_CONSUMERS_IN_RETRY_AUTHORIZATIONS",
                "INDEPENDENT_SAME_HASH_REVIEW_BEFORE_RETRY_PUBLICATION_OR_LAUNCH",
            ],
        },
        "published": False,
        "launched": False,
        "claim_boundary": (
            "DEVELOPMENT_RECOVERY_PLAN_ONLY__NO_CANONICAL_RECORD_PUBLICATION_"
            "WORKER_LAUNCH_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "plan":
        print("REFUSED: exact DEVELOPMENT mode is plan", file=sys.stderr)
        return 2
    try:
        plan = build_plan()
    except BaseException as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(plan, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
