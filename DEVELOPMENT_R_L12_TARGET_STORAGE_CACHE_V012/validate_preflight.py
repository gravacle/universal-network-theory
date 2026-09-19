#!/usr/bin/env python3
"""Nonphysical exhaustive index/allocation/compatibility preflight for target V012."""

from __future__ import annotations

import ast
import copy
import hashlib
import itertools
import json
import math
import os
import stat
import sys
import tempfile
import time
import types
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import build_target_cache as builder  # noqa: E402
import consume_target_cache as consumer  # noqa: E402
import production_obligation_validators as obligation_validators  # noqa: E402


FREEZE = HERE / "FREEZE.json"
RESULT = HERE / "PREFLIGHT_RESULT_V001.json"
MUTATION_LEDGER = HERE / "PREFLIGHT_MUTATION_LEDGER_V001.json"
OBLIGATION_MATRIX_RELATIVE = (
    "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/"
    "AUDIT_OBLIGATIONS_V001.json"
)
OBLIGATION_MATRIX = ROOT / OBLIGATION_MATRIX_RELATIVE
OBLIGATION_MATRIX_SHA256 = (
    "49a1a5901249c0476ebd775d60b9342436e4391a2a97b9c08f1082247b719e77"
)
MUTATION_LEDGER_SCHEMA = "TARGET_V012_PREPAYLOAD_MUTATION_LEDGER_V001"
MUTATION_LEDGER_CLASSIFICATION = (
    "PASS_EXECUTED_PREREGISTERED_MUTATION_ASSIGNMENTS"
)
MUTATION_LEDGER_CLAIM_BOUNDARY = (
    "EXECUTED_PRODUCTION_VALIDATOR_MUTATION_EVIDENCE_ONLY__NO_GATE_CACHE_HISTORY_"
    "SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
)
PRODUCTION_FIXTURE_HOOK = "build_target_cache.validate_audit_obligation_fixture"
A22_STATEFUL_HOOK_BY_FIXTURE = {
    "PF_A22_TARGET_AUTH": (
        "dual_launch_coordinator.DualLaunchCoordinator.admit_authorization"
    ),
    "PF_A22_HOSTILE_AUTH": (
        "dual_launch_coordinator.DualLaunchCoordinator.admit_authorization"
    ),
    "PF_A22_READY": (
        "dual_launch_coordinator.DualLaunchCoordinator.commit_handshake"
    ),
    "PF_A22_HANDSHAKE": (
        "dual_launch_coordinator.DualLaunchCoordinator.commit_handshake"
    ),
    "PF_A22_RELEASE": (
        "dual_launch_coordinator.DualLaunchCoordinator.release_workers"
    ),
    "PF_A22_COMMAND": (
        "dual_launch_coordinator.DualLaunchCoordinator.admit_release_ack"
    ),
    "PF_A22_ACK": (
        "dual_launch_coordinator.DualLaunchCoordinator.admit_release_ack"
    ),
    "PF_A22_COMPLETION": (
        "dual_launch_coordinator.DualLaunchCoordinator.admit_worker_completion"
    ),
}
A22_MUTATION_FIXTURE_BY_CLASS = {
    "M01_MISSING_KEY": "PF_A22_TARGET_AUTH",
    "M02_EXTRA_KEY": "PF_A22_HOSTILE_AUTH",
    "M03_WRONG_KEY_SAME_COUNT": "PF_A22_READY",
    "M04_DUPLICATE_JSON_KEY": "PF_A22_TARGET_AUTH",
    "M05_NONFINITE_JSON": "PF_A22_HOSTILE_AUTH",
    "M06_BOOL_FOR_INT": "PF_A22_READY",
    "M07_FLOAT_INT_ALIAS": "PF_A22_COMMAND",
    "M10_IDENTITY_OR_CLAIM": "PF_A22_ACK",
    "M11_HASH_OR_PATH": "PF_A22_READY",
    "M12_SYMLINK_OR_WRITABLE": "PF_A22_HANDSHAKE",
    "M13_DESCRIPTOR_TOCTOU": "PF_A22_RELEASE",
    "M17_PROVENANCE_DROP_SWAP": "PF_A22_HANDSHAKE",
    "M19_STAGE_BYPASS": "PF_A22_HANDSHAKE",
    "M23_HANDSHAKE_TELEMETRY": "PF_A22_ACK",
    "M24_UNLOCK_AUDIT_BINDING": "PF_A22_RELEASE",
    "M28_PREMATURE_ARTIFACT": "PF_A22_ACK",
    "M30_COMPLETION_BOOL_PROCESS_ID": "PF_A22_COMPLETION",
    "M31_COMPLETION_FLOAT_PROCESS_ID": "PF_A22_COMPLETION",
    "M32_COMPLETION_SCHEMA": "PF_A22_COMPLETION",
    "M33_COMPLETION_OUTPUT_HASH": "PF_A22_COMPLETION",
    "M34_COMPLETION_WORKER_IDENTITY": "PF_A22_COMPLETION",
    "M35_COMPLETION_STAGE_BYPASS": "PF_A22_COMPLETION",
    "M36_COMPLETION_EPOCH_WINDOW": "PF_A22_COMPLETION",
}
A22_STATEFUL_EXPECTED_REFUSAL = {
    "M06_BOOL_FOR_INT": "process_id must be an exact integer >= 1",
    "M07_FLOAT_INT_ALIAS": "release command process_id must be an exact integer >= 1",
    "M10_IDENTITY_OR_CLAIM": "worker release ACK schema mismatch",
    "M11_HASH_OR_PATH": "process start token must be a lowercase SHA-256",
    "M17_PROVENANCE_DROP_SWAP": "worker READY hash reconstruction mismatch",
    "M19_STAGE_BYPASS": "handshake authorizations exact key census mismatch",
    "M23_HANDSHAKE_TELEMETRY": "worker release ACK digest mismatch",
    "M24_UNLOCK_AUDIT_BINDING": "release token mismatch",
    "M30_COMPLETION_BOOL_PROCESS_ID": "worker completion process_id must be an exact integer >= 1",
    "M31_COMPLETION_FLOAT_PROCESS_ID": "worker completion process_id must be an exact integer >= 1",
    "M32_COMPLETION_SCHEMA": "worker completion schema mismatch",
    "M33_COMPLETION_OUTPUT_HASH": "worker completion output hash must be a lowercase SHA-256",
    "M34_COMPLETION_WORKER_IDENTITY": "worker completion identity mismatch",
    "M35_COMPLETION_STAGE_BYPASS": "worker completion requires both release ACKs",
    "M36_COMPLETION_EPOCH_WINDOW": "worker completion outside execution wall window",
}
MUTATION_REFUSAL = {
    "M01_MISSING_KEY": "exact key census mismatch",
    "M02_EXTRA_KEY": "exact key census mismatch",
    "M03_WRONG_KEY_SAME_COUNT": "exact key census mismatch",
    "M04_DUPLICATE_JSON_KEY": "duplicate JSON key",
    "M05_NONFINITE_JSON": "nonfinite JSON constant",
    "M06_BOOL_FOR_INT": "exact integer mismatch",
    "M07_FLOAT_INT_ALIAS": "exact integer mismatch",
    "M08_INT_FLOAT_ALIAS": "exact float mismatch",
    "M09_INT_OR_FLOAT_FOR_BOOL": "exact boolean mismatch",
    "M10_IDENTITY_OR_CLAIM": "identity/claim mismatch",
    "M11_HASH_OR_PATH": "path/hash mismatch",
    "M12_SYMLINK_OR_WRITABLE": "immutable ordinary file mismatch",
    "M13_DESCRIPTOR_TOCTOU": "descriptor path identity drift",
    "M14_COUNT_ARITHMETIC": "counter reconstruction mismatch",
    "M15_LIST_CENSUS_ORDER": "ordered census mismatch",
    "M16_CROSS_ROLE_ALIAS": "cross-role alias mismatch",
    "M17_PROVENANCE_DROP_SWAP": "provenance mismatch",
    "M18_CACHE_CENSUS_SEMANTICS": "cache census/semantics mismatch",
    "M19_STAGE_BYPASS": "stage predecessor mismatch",
    "M20_HISTORY_PROJECTION": "history projection mismatch",
    "M21_TERMINAL_SHARD": "terminal-shard mismatch",
    "M22_RESOURCE_FRESHNESS": "resource/freshness mismatch",
    "M23_HANDSHAKE_TELEMETRY": "launch/telemetry mismatch",
    "M24_UNLOCK_AUDIT_BINDING": "unlock/audit binding mismatch",
    "M25_IMPORT_TARGET_VALIDATOR": "target-validator import mismatch",
    "M26_L10_CROSS_MISMATCH": "L10 cross-projection mismatch",
    "M27_L12_CROSS_MISMATCH": "L12 cross-projection mismatch",
    "M28_PREMATURE_ARTIFACT": "premature canonical artifact mismatch",
    "M29_WRONG_ABSENCE_VALUE": "absence census mismatch",
    "M30_COMPLETION_BOOL_PROCESS_ID": "worker completion process_id type mismatch",
    "M31_COMPLETION_FLOAT_PROCESS_ID": "worker completion process_id type mismatch",
    "M32_COMPLETION_SCHEMA": "worker completion schema mismatch",
    "M33_COMPLETION_OUTPUT_HASH": "worker completion output hash mismatch",
    "M34_COMPLETION_WORKER_IDENTITY": "worker completion identity mismatch",
    "M35_COMPLETION_STAGE_BYPASS": "worker completion stage mismatch",
    "M36_COMPLETION_EPOCH_WINDOW": "worker completion epoch mismatch",
}
AUDIT_ARTIFACT_IDS = frozenset(obligation_validators.ARTIFACT_IDS)
EXPECTED_CENSUS = {
    4: (5_204, 816, 60, 56, 6_136, 3_360, 2_808, 2_956, 2_956, 62),
    6: (102_976, 15_184, 252, 248, 118_660, 128_128, 47_000, 50_176, 50_176, 121),
    8: (2_060_948, 271_456, 1_020, 1_016, 2_334_440, 5_116_320, 807_864, 867_436, 867_436, 200),
    10: (39_761_072, 4_743_696, 4_092, 4_088, 44_512_948, 209_969_760, 13_818_936, 14_874_736, 14_874_736, 299),
    12: (744_528_576, 81_676_960, 16_380, 16_376, 826_238_292, 8_773_664_640, 234_782_536, 252_944_080, 252_944_080, 418),
}


class Failure(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(block)
    return digest.hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def expect_refusal(action, fragment: str, message: str) -> None:
    try:
        action()
    except (builder.Refusal, consumer.Refusal) as error:
        check(fragment in str(error), message)
    else:
        raise Failure(message)


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def expected_mutation_refusal(artifact_id: str, mutation_class: str) -> str:
    if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
        return A22_STATEFUL_EXPECTED_REFUSAL.get(
            mutation_class, MUTATION_REFUSAL[mutation_class],
        )
    return obligation_validators.FINAL_NATIVE_MUTATION_REFUSAL.get(
        (artifact_id, mutation_class), MUTATION_REFUSAL[mutation_class],
    )


def exact_refusal_match(actual: object, expected: str) -> bool:
    """Match one native refusal grammar without accepting loose substrings."""
    if not isinstance(actual, str) or not actual or "\n" in actual:
        return False
    if actual.endswith(expected):
        return True
    if expected == "duplicate JSON key":
        marker = expected + ": "
        prefix, separator, detail = actual.partition(marker)
        return bool(separator and prefix and detail and detail.strip() == detail)
    if expected == "nonfinite JSON constant":
        marker = expected + ": "
        prefix, separator, detail = actual.partition(marker)
        return bool(
            separator and prefix
            and detail in {"NaN", "Infinity", "-Infinity"}
        )
    return False


def preregistered_mutated_fixture(
    artifact_id: str, mutation_class: str, variant: int,
) -> tuple[dict[str, object] | bytes, str, str]:
    """Resolve the three matrix-specific mutation targets at this orchestrator."""
    if (
        artifact_id in {
            "A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT",
        }
        and mutation_class == "M21_TERMINAL_SHARD"
    ):
        record = obligation_validators.positive_fixture(artifact_id, variant)
        record["checks"]["terminal_shard_records"] += 1
        record["checks_total"] += 1
        record["checks_passed"] += 1
        description = f"{artifact_id} {mutation_class} native-schema mutation"
        return (
            record,
            obligation_validators.MUTATION_EXPECTED_REFUSAL[mutation_class],
            description,
        )
    if artifact_id == "A14_L10_HISTORY" and mutation_class == "M22_RESOURCE_FRESHNESS":
        record = obligation_validators.positive_fixture(artifact_id, variant)
        record["resource"]["passed"] = False
        description = f"{artifact_id} {mutation_class} native-schema mutation"
        return (
            record,
            obligation_validators.MUTATION_EXPECTED_REFUSAL[mutation_class],
            description,
        )
    return obligation_validators.mutated_fixture(
        artifact_id, mutation_class, variant,
    )


def strict_json_object(raw: bytes, label: str) -> dict[str, object]:
    def exact_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise Failure(f"{label} duplicate JSON key: {key}")
            value[key] = item
        return value

    def reject_constant(token: str) -> object:
        raise Failure(f"{label} nonfinite JSON constant: {token}")

    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=exact_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise Failure(f"{label} exact key census mismatch")
    return value


def descriptor_bytes(descriptor: int) -> bytes:
    raw = bytearray()
    offset = 0
    while block := os.pread(descriptor, 2**20, offset):
        raw.extend(block)
        offset += len(block)
    return bytes(raw)


def descriptor_digest(descriptor: int) -> str:
    return hashlib.sha256(descriptor_bytes(descriptor)).hexdigest()


def immutable_source_bytes(
    path: Path, label: str, expected_sha256: str,
) -> bytes:
    """Read the exact immutable source bytes which will be compiled."""
    if path.is_symlink() or not path.is_file():
        raise Failure(f"{label} immutable ordinary file mismatch")
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_mode & 0o222:
            raise Failure(f"{label} immutable ordinary file mismatch")
        raw = descriptor_bytes(descriptor)
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected_sha256:
            raise Failure(f"{label} path/hash mismatch")
        after = os.fstat(descriptor)
        path_after = os.stat(path, follow_symlinks=False)
        if (
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            or (path_after.st_dev, path_after.st_ino, path_after.st_size)
            != (before.st_dev, before.st_ino, before.st_size)
            or descriptor_bytes(descriptor) != raw
        ):
            raise Failure(f"{label} descriptor path identity drift")
        return raw
    finally:
        os.close(descriptor)


_DUAL_LAUNCH_RUNTIME: tuple[types.ModuleType, types.ModuleType] | None = None


def load_dual_launch_runtime(
    matrix: dict[str, object],
) -> tuple[types.ModuleType, types.ModuleType]:
    """Compile the hash-bound coordinator and fixtures from held source bytes."""
    global _DUAL_LAUNCH_RUNTIME
    if _DUAL_LAUNCH_RUNTIME is not None:
        return _DUAL_LAUNCH_RUNTIME
    fixed = matrix.get("fixed_values")
    if not isinstance(fixed, dict):
        raise Failure("dual-launch fixed-value packet absent")
    hashes = fixed.get("dual_launch_coordinator_sha256_by_file")
    if not isinstance(hashes, dict):
        raise Failure("dual-launch source hash packet absent")
    directory = ROOT / "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001"
    required = ("dual_launch_coordinator.py", "synthetic_fixtures.py")
    raw_by_name: dict[str, bytes] = {}
    for name in required:
        digest = hashes.get(name)
        if not isinstance(digest, str):
            raise Failure(f"dual-launch source hash absent: {name}")
        raw_by_name[name] = immutable_source_bytes(
            directory / name, f"dual-launch {name}", digest,
        )
    coordinator = types.ModuleType("dual_launch_coordinator")
    coordinator.__file__ = str(directory / required[0])
    coordinator.__package__ = ""
    previous = sys.modules.get("dual_launch_coordinator")
    sys.modules["dual_launch_coordinator"] = coordinator
    try:
        exec(compile(
            raw_by_name[required[0]], coordinator.__file__, "exec",
        ), coordinator.__dict__)
        fixtures = types.ModuleType("v012_dual_launch_synthetic_fixtures")
        fixtures.__file__ = str(directory / required[1])
        fixtures.__package__ = ""
        exec(compile(
            raw_by_name[required[1]], fixtures.__file__, "exec",
        ), fixtures.__dict__)
    except Exception:
        if previous is None:
            sys.modules.pop("dual_launch_coordinator", None)
        else:
            sys.modules["dual_launch_coordinator"] = previous
        raise
    _DUAL_LAUNCH_RUNTIME = coordinator, fixtures
    return _DUAL_LAUNCH_RUNTIME


def stable_file_sha256(path: Path, label: str) -> str:
    if path.is_symlink() or not path.is_file():
        raise Failure(f"{label} is not an ordinary file")
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        digest = descriptor_digest(descriptor)
        after = os.fstat(descriptor)
        path_after = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode)
            or (
                before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns,
            )
            != (
                after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns, after.st_ctime_ns,
            )
            or (path_after.st_dev, path_after.st_ino, path_after.st_size)
            != (before.st_dev, before.st_ino, before.st_size)
            or descriptor_digest(descriptor) != digest
        ):
            raise Failure(f"{label} descriptor path identity drift")
        return digest
    finally:
        os.close(descriptor)


def read_strict_immutable_json(
    path: Path, label: str, expected_sha256: str | None = None,
) -> tuple[dict[str, object], str]:
    if path.is_symlink() or not path.is_file():
        raise Failure(f"{label} immutable ordinary file mismatch")
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_mode & 0o222:
            raise Failure(f"{label} immutable ordinary file mismatch")
        raw = descriptor_bytes(descriptor)
        digest = hashlib.sha256(raw).hexdigest()
        if expected_sha256 is not None and digest != expected_sha256:
            raise Failure(f"{label} path/hash mismatch")
        record = strict_json_object(raw, label)
        after = os.fstat(descriptor)
        try:
            path_after = os.stat(path, follow_symlinks=False)
        except FileNotFoundError as error:
            raise Failure(f"{label} descriptor path identity drift") from error
        identity = (before.st_dev, before.st_ino, before.st_size,
                    before.st_mtime_ns, before.st_ctime_ns)
        if (
            identity
            != (after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns, after.st_ctime_ns)
            or (path_after.st_dev, path_after.st_ino, path_after.st_size)
            != (before.st_dev, before.st_ino, before.st_size)
            or descriptor_digest(descriptor) != digest
        ):
            raise Failure(f"{label} descriptor path identity drift")
        return record, digest
    finally:
        os.close(descriptor)


def exact_tree_equal(observed: object, expected: object) -> bool:
    if type(observed) is not type(expected):
        return False
    if isinstance(expected, dict):
        return (
            set(observed) == set(expected)
            and all(exact_tree_equal(observed[key], value) for key, value in expected.items())
        )
    if isinstance(expected, list):
        return len(observed) == len(expected) and all(
            exact_tree_equal(left, right) for left, right in zip(observed, expected)
        )
    return observed == expected


def write_immutable_fixture(path: Path, raw: bytes, mode: int = 0o444) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        os.write(descriptor, raw)
        os.fchmod(descriptor, mode)
    finally:
        os.close(descriptor)


def _unlink_staging_if_owned_at(
    parent_descriptor: int, name: str, identity: tuple[int, int],
) -> bool:
    try:
        metadata = os.stat(
            name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
    except FileNotFoundError:
        return False
    if (
        stat.S_ISREG(metadata.st_mode)
        and (metadata.st_dev, metadata.st_ino) == identity
    ):
        os.unlink(name, dir_fd=parent_descriptor)
        return True
    return False


def atomic_publish_immutable_json(
    path: Path, record: dict[str, object], label: str,
) -> tuple[dict[str, object], str]:
    """Durably publish authenticated JSON at an absent canonical path."""
    parent = path.parent
    builder.StableAuthorityCustody._require_canonical_path(
        os.path.abspath(os.fspath(parent)), f"{label} parent",
    )
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor = os.open(parent, parent_flags)
    try:
        try:
            destination = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
        except FileNotFoundError:
            destination = None
        parent_before = os.fstat(parent_descriptor)
        parent_path_before = os.stat(parent, follow_symlinks=False)
        if (
            destination is not None
            or not stat.S_ISDIR(parent_before.st_mode)
            or (parent_path_before.st_dev, parent_path_before.st_ino)
            != (parent_before.st_dev, parent_before.st_ino)
        ):
            raise Failure(f"{label} canonical destination is not absent")
        try:
            raw = (json.dumps(
                record, indent=2, sort_keys=True, ensure_ascii=True,
                allow_nan=False,
            ) + "\n").encode("ascii")
        except (TypeError, ValueError, UnicodeEncodeError) as error:
            raise Failure(f"{label} finite canonical JSON mismatch") from error
        if not exact_tree_equal(strict_json_object(raw, label), record):
            raise Failure(f"{label} JSON round-trip changed exact values")
        temporary_name = (
            f".{path.name}.staging-{os.getpid()}-{time.time_ns()}"
        )
        flags = (
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(
            temporary_name, flags, 0o400, dir_fd=parent_descriptor,
        )
        identity = (os.fstat(descriptor).st_dev, os.fstat(descriptor).st_ino)
        try:
            offset = 0
            while offset < len(raw):
                written = os.write(descriptor, raw[offset:])
                if written <= 0:
                    raise Failure(f"{label} staging write made no progress")
                offset += written
            os.fsync(descriptor)
            os.fchmod(descriptor, 0o444)
            os.fsync(descriptor)
            staged = os.fstat(descriptor)
            expected_digest = hashlib.sha256(raw).hexdigest()
            if (
                not stat.S_ISREG(staged.st_mode)
                or staged.st_mode & 0o222
                or staged.st_nlink != 1
                or staged.st_size != len(raw)
                or descriptor_digest(descriptor) != expected_digest
            ):
                raise Failure(f"{label} staging descriptor authentication failed")
            builder.StableAuthorityCustody._require_canonical_path(
                os.path.abspath(os.fspath(parent)), f"{label} parent",
            )
            parent_now = os.stat(parent, follow_symlinks=False)
            if (parent_now.st_dev, parent_now.st_ino) != (
                parent_before.st_dev, parent_before.st_ino,
            ):
                raise Failure(f"{label} canonical parent identity drift")
            try:
                os.link(
                    temporary_name, path.name,
                    src_dir_fd=parent_descriptor,
                    dst_dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
            except FileExistsError as error:
                raise Failure(f"{label} canonical destination appeared") from error
            canonical_descriptor = os.open(
                path.name,
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=parent_descriptor,
            )
            try:
                linked_canonical = os.fstat(canonical_descriptor)
                if (
                    not stat.S_ISREG(linked_canonical.st_mode)
                    or linked_canonical.st_mode & 0o222
                    or linked_canonical.st_nlink != 2
                    or (linked_canonical.st_dev, linked_canonical.st_ino)
                    != identity
                    or descriptor_digest(canonical_descriptor) != expected_digest
                ):
                    raise Failure(
                        f"{label} canonical link authentication failed"
                    )
                if not _unlink_staging_if_owned_at(
                    parent_descriptor, temporary_name, identity,
                ):
                    raise Failure(f"{label} staging custody changed after link")
                os.fsync(parent_descriptor)
                canonical = os.stat(
                    path.name, dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                canonical_held = os.fstat(canonical_descriptor)
                builder.StableAuthorityCustody._require_canonical_path(
                    os.path.abspath(os.fspath(parent)), f"{label} parent",
                )
                parent_after = os.stat(parent, follow_symlinks=False)
                if (
                    (canonical.st_dev, canonical.st_ino) != identity
                    or (canonical_held.st_dev, canonical_held.st_ino) != identity
                    or canonical.st_nlink != 1
                    or canonical_held.st_nlink != 1
                    or canonical.st_mode & 0o222
                    or not stat.S_ISDIR(parent_after.st_mode)
                    or (parent_after.st_dev, parent_after.st_ino)
                    != (parent_before.st_dev, parent_before.st_ino)
                ):
                    raise Failure(
                        f"{label} canonical publication identity mismatch"
                    )
                accepted = strict_json_object(
                    descriptor_bytes(canonical_descriptor), label,
                )
                observed_digest = descriptor_digest(canonical_descriptor)
                if (
                    observed_digest != expected_digest
                    or not exact_tree_equal(accepted, record)
                ):
                    raise Failure(
                        f"{label} canonical publication content mismatch"
                    )
                return accepted, observed_digest
            finally:
                os.close(canonical_descriptor)
        finally:
            os.close(descriptor)
            _unlink_staging_if_owned_at(
                parent_descriptor, temporary_name, identity,
            )
    finally:
        os.close(parent_descriptor)


def validate_held_descriptor_identity(
    descriptor: int, path: Path, before: os.stat_result, digest: str,
) -> None:
    after = os.fstat(descriptor)
    path_after = os.stat(path, follow_symlinks=False)
    if (
        (after.st_dev, after.st_ino, after.st_size)
        != (before.st_dev, before.st_ino, before.st_size)
        or (path_after.st_dev, path_after.st_ino, path_after.st_size)
        != (before.st_dev, before.st_ino, before.st_size)
        or descriptor_digest(descriptor) != digest
    ):
        raise Failure("production custody descriptor path identity drift")


def require_artifacts_absent(paths: tuple[Path, ...], label: str) -> None:
    """Production absence contract used before any canonical publication."""
    if not paths or any(not isinstance(path, Path) for path in paths):
        raise Failure(f"{label} absence census mismatch")
    present = [path for path in paths if path.exists() or path.is_symlink()]
    if present:
        raise Failure(f"{label} premature canonical artifact mismatch")


def validate_independent_auditor_source_bytes(raw: bytes, label: str) -> None:
    """Production independence sink for auditor source before hash freeze."""
    if type(raw) is not bytes:
        raise Failure(f"{label} target-validator import mismatch")
    try:
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=f"<{label}>")
    except (UnicodeDecodeError, SyntaxError) as error:
        raise Failure(f"{label} target-validator import mismatch") from error
    forbidden = {
        "build_target_cache", "consume_target_cache", "validate_preflight",
        "production_obligation_validators", "compute_prefix_history_v004",
        "independent_prefix_history_v003", "build_cache_v004r4",
        "consume_cache_v004r4", "validate_cache_preflight_v004r4",
    }
    imported: set[str] = set()
    dynamic = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            function = node.func
            dynamic = dynamic or (
                isinstance(function, ast.Name) and function.id == "__import__"
            ) or (
                isinstance(function, ast.Attribute)
                and function.attr == "import_module"
            )
    if imported & forbidden or dynamic:
        raise Failure(f"{label} target-validator import mismatch")


def protected_canonical_artifacts() -> tuple[Path, ...]:
    return (
        builder.DUAL_GATE,
        consumer.PHYSICAL_GATE,
        consumer.CONTROL_AUTHORIZATION_GATE,
        consumer.CACHED_CONTROL_GATE,
        consumer.CACHED_CONTROL_GATE_AUDIT,
        consumer.L10_EXECUTION_AUTHORIZATION_GATE,
        consumer.CACHED_L10_GATE,
        consumer.CACHED_L10_GATE_AUDIT,
        consumer.TARGET_L12_EXECUTION_GATE,
        consumer.HOSTILE_L12_EXECUTION_GATE,
        consumer.TARGET_HOSTILE_L10_CROSS_GATE,
        consumer.PARALLEL_L12_SCHEDULE_GATE,
        consumer.PARALLEL_L12_SCHEDULE_AUDIT,
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_READY_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_READY_V001.json",
        consumer.DUAL_L12_LAUNCH_HANDSHAKE,
        consumer.DUAL_L12_WORKER_RELEASE,
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_COMMAND_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_ACK_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
        builder.ROOT / (
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
            "TARGET_V012_WORKER_COMPLETION_V001.json"
        ),
        builder.ROOT / (
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
            "HOSTILE_V004R4_WORKER_COMPLETION_V001.json"
        ),
        consumer.PARALLEL_L12_TELEMETRY,
        consumer.PARALLEL_L12_SHARED_DIR / "FINAL_L12_TARGET_HOSTILE_AUDIT_V001.json",
        consumer.HOSTILE_L10_EXECUTION_GATE,
        builder.ROOT / (
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
        ),
        builder.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS",
        builder.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS",
        builder.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES",
        builder.CACHE_PARENT,
        consumer.PHYSICAL_OUTPUT_PARENT,
        consumer.WORKSPACE_PARENT,
        *(builder.ROOT / relative for relative in (
            builder.FUTURE_HOSTILE_AUDIT_PATH,
            builder.FUTURE_POSTBUILD_AUDIT_PATH,
            builder.FUTURE_PHYSICAL_GATE_AUDIT_PATH,
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json",
        )),
    )


def current_source_sha256() -> dict[str, str]:
    return {
        "METHOD.md": stable_file_sha256(HERE / "METHOD.md", "V012 method"),
        "build_target_cache.py": stable_file_sha256(
            HERE / "build_target_cache.py", "V012 builder",
        ),
        "consume_target_cache.py": stable_file_sha256(
            HERE / "consume_target_cache.py", "V012 consumer",
        ),
        "production_obligation_validators.py": stable_file_sha256(
            HERE / "production_obligation_validators.py",
            "V012 production obligation validators",
        ),
        "validate_preflight.py": stable_file_sha256(
            Path(__file__), "V012 preflight",
        ),
    }


def load_obligation_matrix() -> tuple[dict[str, object], str]:
    matrix, digest = read_strict_immutable_json(
        OBLIGATION_MATRIX, "V012 obligation matrix", OBLIGATION_MATRIX_SHA256,
    )
    required_top = {
        "schema", "status", "scope", "independence_contract", "fixed_values",
        "shared_profiles", "mutation_catalog", "V011_findings", "V012_checklist",
        "stages", "artifacts", "coverage_requirements",
    }
    artifacts = matrix.get("artifacts")
    mutation_catalog = matrix.get("mutation_catalog")
    if (
        set(matrix) != required_top
        or matrix.get("schema") != "TARGET_V012_PREREGISTERED_AUDIT_OBLIGATIONS_V001"
        or matrix.get("status")
        != "PREREGISTERED_OBLIGATIONS_ONLY__NO_AUTHORITY_GRANTED"
        or not isinstance(artifacts, list)
        or len(artifacts) != 26
        or not isinstance(mutation_catalog, dict)
        or set(mutation_catalog) != set(MUTATION_REFUSAL)
    ):
        raise Failure("V012 obligation matrix exact census mismatch")
    artifact_ids: set[str] = set()
    fixture_ids: set[str] = set()
    assignments = 0
    assigned_classes: set[str] = set()
    required_artifact_keys = {
        "id", "stage_id", "kind", "canonical_paths", "profiles",
        "schema_rules", "type_rules", "value_rules", "provenance_rules",
        "custody_rules", "reconstruction_rules", "positive_fixture",
        "mutation_classes", "maps_to",
    }
    for artifact in artifacts:
        expected_keys = set(required_artifact_keys)
        if artifact.get("id") == "A22_TARGET_L12_AUTHORIZATION":
            expected_keys |= {
                "positive_fixture_variants", "mutation_fixture_by_class",
            }
        if not isinstance(artifact, dict) or set(artifact) != expected_keys:
            raise Failure("V012 obligation artifact exact key census mismatch")
        artifact_id = artifact.get("id")
        positive = artifact.get("positive_fixture")
        classes = artifact.get("mutation_classes")
        if (
            not isinstance(artifact_id, str)
            or artifact_id in artifact_ids
            or not isinstance(positive, dict)
            or set(positive) != {"id", "form", "acceptance"}
            or not isinstance(positive.get("id"), str)
            or positive["id"] in fixture_ids
            or not isinstance(classes, list)
            or not classes
            or any(not isinstance(value, str) for value in classes)
            or len(classes) != len(set(classes))
            or any(value not in mutation_catalog for value in classes)
        ):
            raise Failure("V012 obligation artifact identity/assignment mismatch")
        artifact_ids.add(artifact_id)
        fixture_ids.add(positive["id"])
        variants = artifact.get("positive_fixture_variants", [])
        if (
            not isinstance(variants, list)
            or (len(variants) != 7 if artifact_id == "A22_TARGET_L12_AUTHORIZATION" else bool(variants))
            or any(
                not isinstance(value, dict)
                or set(value) != {"id", "form", "acceptance"}
                or not isinstance(value.get("id"), str)
                or value["id"] in fixture_ids
                for value in variants
            )
        ):
            raise Failure("V012 obligation fixture variant census mismatch")
        fixture_ids.update(value["id"] for value in variants)
        mutation_fixture_map = artifact.get("mutation_fixture_by_class", {})
        if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
            if (
                not isinstance(mutation_fixture_map, dict)
                or mutation_fixture_map != A22_MUTATION_FIXTURE_BY_CLASS
            ):
                raise Failure("A22 mutation fixture assignment mismatch")
        elif mutation_fixture_map:
            raise Failure("unexpected mutation fixture assignment")
        assignments += len(classes)
        assigned_classes.update(classes)
    if (
        assignments != 477
        or assigned_classes != set(mutation_catalog)
        or artifact_ids != set(AUDIT_ARTIFACT_IDS)
    ):
        raise Failure("V012 obligation mutation assignment census mismatch")

    # V001 preregistered the complete obligation/mutation structure under the
    # former six-hour launch policy.  The authorized 30-hour successor changes
    # only the runtime wall and the exact hashes of the wall-policy control
    # plane.  Project those fixed values from the hash-frozen current builder;
    # do not change any artifact, mutation, physics, tolerance, or lineage rule.
    fixed = matrix.get("fixed_values")
    old_hashes = fixed.get("dual_launch_coordinator_sha256_by_file") \
        if isinstance(fixed, dict) else None
    if (
        not isinstance(fixed, dict)
        or fixed.get("wall_limit_seconds") != 21_600
        or not isinstance(old_hashes, dict)
        or set(old_hashes)
        != {
            Path(path).name for path in builder.DUAL_LAUNCH_COORDINATOR_SHA256
            if Path(path).name != "MANIFEST.sha256"
        }
    ):
        raise Failure("V001-to-30-hour fixed-value projection precondition mismatch")
    fixed["wall_limit_seconds"] = int(builder.WALL_LIMIT)
    fixed["dual_launch_coordinator_manifest_sha256"] = (
        builder.DUAL_LAUNCH_COORDINATOR_SHA256[
            "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/MANIFEST.sha256"
        ]
    )
    fixed["dual_launch_coordinator_sha256_by_file"] = {
        Path(path).name: digest
        for path, digest in builder.DUAL_LAUNCH_COORDINATOR_SHA256.items()
        if Path(path).name != "MANIFEST.sha256"
    }
    return matrix, digest


def a22_positive_fixture(
    fixtures: types.ModuleType, fixture_id: str,
) -> dict[str, object]:
    bundle = fixtures.fresh_bundle()
    records = {
        "PF_A22_TARGET_AUTH": bundle["target_authorization"],
        "PF_A22_HOSTILE_AUTH": bundle["hostile_authorization"],
        "PF_A22_READY": bundle["handshake"]["workers"]["target_v012"],
        "PF_A22_HANDSHAKE": bundle["handshake"],
        "PF_A22_RELEASE": bundle["release"],
        "PF_A22_COMMAND": bundle["release_commands"]["target_v012"],
        "PF_A22_ACK": bundle["release_acks"]["target_v012"],
        "PF_A22_COMPLETION": bundle["completions"]["target_v012"],
    }
    if fixture_id not in records:
        raise Failure("A22 stateful fixture identity mismatch")
    return copy.deepcopy(records[fixture_id])


def a22_mutated_fixture(
    fixtures: types.ModuleType, fixture_id: str, mutation_class: str,
) -> tuple[dict[str, object] | bytes, str]:
    """Apply the preregistered mutation to the coordinator's native record."""
    record = a22_positive_fixture(fixtures, fixture_id)
    description = (
        "A22_TARGET_L12_AUTHORIZATION "
        f"{mutation_class} native coordinator mutation"
    )
    if mutation_class == "M04_DUPLICATE_JSON_KEY":
        raw = canonical_json_bytes(record).decode("ascii").strip()
        duplicated_key = next(iter(record))
        prefix = json.dumps(duplicated_key, ensure_ascii=True) + ":null,"
        return ("{" + prefix + raw[1:] + "\n").encode("ascii"), description
    if mutation_class == "M05_NONFINITE_JSON":
        raw = canonical_json_bytes(record).decode("ascii").strip()
        return (raw[:-1] + ",\"nonfinite_probe\":NaN}\n").encode("ascii"), description
    if mutation_class == "M01_MISSING_KEY":
        del record["claim_boundary"]
    elif mutation_class == "M02_EXTRA_KEY":
        record["unregistered_authority"] = True
    elif mutation_class == "M03_WRONG_KEY_SAME_COUNT":
        record["wrong_role"] = record.pop("role")
    elif mutation_class == "M06_BOOL_FOR_INT":
        record["process_id"] = True
    elif mutation_class == "M07_FLOAT_INT_ALIAS":
        record["process_id"] = float(record["process_id"])
    elif mutation_class == "M10_IDENTITY_OR_CLAIM":
        record["schema"] = "V012_L12_WORKER_RELEASE_ACK_UNAUTHENTICATED"
    elif mutation_class == "M11_HASH_OR_PATH":
        record["process_start_token"] = record["process_start_token"][:-1]
    elif mutation_class == "M17_PROVENANCE_DROP_SWAP":
        record["ready_sha256_by_role"]["target_v012"] = hashlib.sha256(
            b"A22:wrong-ready-provenance"
        ).hexdigest()
    elif mutation_class == "M19_STAGE_BYPASS":
        del record["authorization_sha256_by_role"]["target_v012"]
    elif mutation_class == "M23_HANDSHAKE_TELEMETRY":
        record["ack_sha256"] = hashlib.sha256(
            b"A22:wrong-release-ack"
        ).hexdigest()
    elif mutation_class == "M24_UNLOCK_AUDIT_BINDING":
        record["release_by_role"]["target_v012"][
            "release_token_sha256"
        ] = hashlib.sha256(b"A22:wrong-release-token").hexdigest()
    elif mutation_class == "M30_COMPLETION_BOOL_PROCESS_ID":
        record["process_id"] = True
    elif mutation_class == "M31_COMPLETION_FLOAT_PROCESS_ID":
        record["process_id"] = float(record["process_id"])
    elif mutation_class == "M32_COMPLETION_SCHEMA":
        record["schema"] = "V012_L12_WORKER_COMPLETION_UNAUTHENTICATED"
    elif mutation_class == "M33_COMPLETION_OUTPUT_HASH":
        record["output_sha256"] = record["output_sha256"][:-1]
    elif mutation_class == "M34_COMPLETION_WORKER_IDENTITY":
        record["control_channel_id"] = hashlib.sha256(
            b"A22:wrong-completion-channel"
        ).hexdigest()
    elif mutation_class == "M35_COMPLETION_STAGE_BYPASS":
        # The native bytes remain a valid completion; its preregistered
        # mutation is admission at the wrong live coordinator stage.
        pass
    elif mutation_class == "M36_COMPLETION_EPOCH_WINDOW":
        record["completion_epoch"] = 1
    elif mutation_class not in {
        "M12_SYMLINK_OR_WRITABLE", "M13_DESCRIPTOR_TOCTOU",
        "M28_PREMATURE_ARTIFACT",
    }:
        raise Failure("A22 stateful mutation implementation mismatch")
    return record, description


def validate_a22_stateful_fixture(
    coordinator_module: types.ModuleType, fixtures: types.ModuleType,
    fixture_id: str, raw: bytes,
    mutation_class: str = "POSITIVE_CONTROL",
) -> None:
    """Execute an A22 record at its live coordinator state transition."""
    record = strict_json_object(raw, f"A22 {fixture_id}")
    bundle = fixtures.fresh_bundle()
    coordinator = coordinator_module.DualLaunchCoordinator(
        bundle["policy"], bundle["evaluation_epoch"],
    )
    try:
        coordinator.admit_schedule(bundle["schedule"])
        coordinator.admit_schedule_audit(bundle["schedule_audit"])
        if fixture_id == "PF_A22_TARGET_AUTH":
            coordinator.admit_authorization(record)
            return
        if fixture_id == "PF_A22_HOSTILE_AUTH":
            coordinator.admit_authorization(record)
            return
        coordinator.admit_authorization(bundle["target_authorization"])
        coordinator.admit_authorization(bundle["hostile_authorization"])
        if fixture_id == "PF_A22_READY":
            handshake = copy.deepcopy(bundle["handshake"])
            handshake["workers"]["target_v012"] = record
            handshake["ready_sha256_by_role"]["target_v012"] = (
                coordinator_module.record_sha256(record)
            )
            coordinator.commit_handshake(handshake)
            return
        if fixture_id == "PF_A22_HANDSHAKE":
            coordinator.commit_handshake(record)
            return
        coordinator.commit_handshake(bundle["handshake"])
        if fixture_id == "PF_A22_RELEASE":
            coordinator.release_workers(record)
            return
        coordinator.release_workers(bundle["release"])
        command = bundle["release_commands"]["target_v012"]
        ack = bundle["release_acks"]["target_v012"]
        if fixture_id == "PF_A22_COMMAND":
            coordinator.admit_release_ack(record, ack)
            return
        if fixture_id == "PF_A22_ACK":
            coordinator.admit_release_ack(command, record)
            return
        if fixture_id == "PF_A22_COMPLETION":
            if mutation_class == "M35_COMPLETION_STAGE_BYPASS":
                coordinator.admit_worker_completion(record)
                return
            for role in ("target_v012", "hostile_v004r4"):
                coordinator.admit_release_ack(
                    bundle["release_commands"][role],
                    bundle["release_acks"][role],
                )
            coordinator.admit_worker_completion(record)
            coordinator.admit_worker_completion(
                bundle["completions"]["hostile_v004r4"]
            )
            return
        raise Failure("A22 stateful fixture identity mismatch")
    except coordinator_module.Refusal as error:
        # Preserve the coordinator's native refusal text verbatim.
        raise Failure(str(error)) from error


def execute_obligation_mutations(
    freeze: dict[str, object],
) -> tuple[dict[str, object], dict[str, int]]:
    matrix, matrix_digest = load_obligation_matrix()
    coordinator_module, coordinator_fixtures = load_dual_launch_runtime(matrix)
    source_sha256 = current_source_sha256()
    if not exact_tree_equal(source_sha256, freeze.get("files")):
        raise Failure("mutation suite source hashes drifted from freeze")
    protected = protected_canonical_artifacts()
    if any(path.exists() for path in protected):
        raise Failure("mutation suite found a premature canonical artifact")
    positive_hashes: dict[str, str] = {}
    mutated_hashes: dict[str, str] = {}
    rows: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="target_v012_obligation_mutations_") as directory:
        temporary_root = Path(directory)
        for artifact in matrix["artifacts"]:
            artifact_id = artifact["id"]
            fixture_specs = [artifact["positive_fixture"]] + artifact.get(
                "positive_fixture_variants", []
            )
            fixture_index = {
                fixture["id"]: index for index, fixture in enumerate(fixture_specs)
            }
            for index, fixture in enumerate(fixture_specs):
                fixture_id = fixture["id"]
                positive = (
                    a22_positive_fixture(coordinator_fixtures, fixture_id)
                    if artifact_id == "A22_TARGET_L12_AUTHORIZATION"
                    else obligation_validators.positive_fixture(artifact_id, index)
                )
                raw = obligation_validators.canonical_json_bytes(positive)
                positive_path = temporary_root / f"{fixture_id}.json"
                write_immutable_fixture(positive_path, raw)
                _accepted, positive_digest = read_strict_immutable_json(
                    positive_path, f"positive fixture {fixture_id}"
                )
                if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
                    validate_a22_stateful_fixture(
                        coordinator_module, coordinator_fixtures, fixture_id, raw,
                    )
                else:
                    builder.validate_audit_obligation_fixture(
                        artifact_id, raw, mutation_class="POSITIVE_CONTROL",
                    )
                positive_hashes[fixture_id] = positive_digest
            for mutation_class in artifact["mutation_classes"]:
                fixture_id = artifact.get(
                    "mutation_fixture_by_class", {}
                ).get(mutation_class, artifact["positive_fixture"]["id"])
                case_id = f"MCASE_{len(rows) + 1:04d}"
                case_root = temporary_root / case_id
                case_root.mkdir(mode=0o700)
                if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
                    mutated, byte_mutation = a22_mutated_fixture(
                        coordinator_fixtures, fixture_id, mutation_class,
                    )
                else:
                    mutated, _delegated_expectation, byte_mutation = (
                        preregistered_mutated_fixture(
                            artifact_id, mutation_class, fixture_index[fixture_id],
                        )
                    )
                mutated_raw = (
                    mutated if type(mutated) is bytes
                    else obligation_validators.canonical_json_bytes(mutated)
                )
                mutated_path = case_root / "mutated.json"
                write_immutable_fixture(mutated_path, mutated_raw)
                _held, mutated_digest = read_strict_immutable_json(
                    mutated_path, f"mutation receipt {case_id}",
                ) if mutation_class not in {
                    "M04_DUPLICATE_JSON_KEY", "M05_NONFINITE_JSON",
                } else (None, hashlib.sha256(mutated_raw).hexdigest())
                production_hook = PRODUCTION_FIXTURE_HOOK
                validator_function = obligation_validators.VALIDATOR_FUNCTION_BY_ARTIFACT[
                    artifact_id
                ]
                if artifact_id == "A22_TARGET_L12_AUTHORIZATION":
                    production_hook = A22_STATEFUL_HOOK_BY_FIXTURE[fixture_id]
                    validator_function = production_hook
                mutation_evidence: dict[str, object] = {
                    "kind": "native_json_bytes",
                    "sha256": mutated_digest,
                }
                try:
                    if mutation_class == "M12_SYMLINK_OR_WRITABLE":
                        mutated_path.chmod(0o644)
                        production_hook = "validate_preflight.read_strict_immutable_json"
                        validator_function = "validate_preflight.read_strict_immutable_json"
                        mutation_evidence = {
                            "kind": "writable_native_record",
                            "mode": 0o644,
                            "sha256": mutated_digest,
                        }
                        read_strict_immutable_json(
                            mutated_path, f"{artifact_id} writable native fixture",
                        )
                    elif mutation_class == "M13_DESCRIPTOR_TOCTOU":
                        descriptor = os.open(
                            mutated_path,
                            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                            | getattr(os, "O_NOFOLLOW", 0),
                        )
                        try:
                            before = os.fstat(descriptor)
                            held_digest = descriptor_digest(descriptor)
                            replacement = case_root / "replacement.json"
                            write_immutable_fixture(replacement, mutated_raw)
                            os.replace(replacement, mutated_path)
                            production_hook = "validate_preflight.validate_held_descriptor_identity"
                            validator_function = "validate_preflight.validate_held_descriptor_identity"
                            mutation_evidence = {
                                "kind": "descriptor_path_replacement",
                                "held_sha256": held_digest,
                                "replacement_sha256": mutated_digest,
                                "identity_changed": True,
                            }
                            validate_held_descriptor_identity(
                                descriptor, mutated_path, before, held_digest,
                            )
                        finally:
                            os.close(descriptor)
                    elif mutation_class == "M25_IMPORT_TARGET_VALIDATOR":
                        auditor_source = (
                            f"# {case_id} {artifact_id}\n"
                            "import build_target_cache\n"
                        ).encode("utf-8")
                        source_digest = hashlib.sha256(auditor_source).hexdigest()
                        production_hook = (
                            "validate_preflight."
                            "validate_independent_auditor_source_bytes"
                        )
                        validator_function = production_hook
                        mutation_evidence = {
                            "kind": "forbidden_target_import_source",
                            "case_id": case_id,
                            "artifact_id": artifact_id,
                            "forbidden_module": "build_target_cache",
                            "sha256": source_digest,
                        }
                        validate_independent_auditor_source_bytes(
                            auditor_source,
                            f"{artifact_id} independent auditor source {case_id}",
                        )
                    elif mutation_class == "M28_PREMATURE_ARTIFACT":
                        premature = case_root / "canonical-artifact-analogue.json"
                        write_immutable_fixture(premature, mutated_raw)
                        production_hook = "validate_preflight.require_artifacts_absent"
                        validator_function = "validate_preflight.require_artifacts_absent"
                        mutation_evidence = {
                            "kind": "premature_artifact_presence",
                            "case_relative_path": (
                                f"{case_id}/canonical-artifact-analogue.json"
                            ),
                            "sha256": mutated_digest,
                        }
                        require_artifacts_absent(
                            (premature,), f"{artifact_id} canonical publication",
                        )
                    elif artifact_id == "A22_TARGET_L12_AUTHORIZATION":
                        validate_a22_stateful_fixture(
                            coordinator_module, coordinator_fixtures,
                            fixture_id, mutated_raw, mutation_class,
                        )
                    else:
                        builder.validate_audit_obligation_fixture(
                            artifact_id, mutated_raw, mutation_class=mutation_class,
                        )
                except (Failure, builder.Refusal) as error:
                    actual_refusal = str(error)
                    expected_evidence = expected_mutation_refusal(
                        artifact_id, mutation_class,
                    )
                    check(
                        exact_refusal_match(actual_refusal, expected_evidence),
                        f"{case_id} refused without artifact-specific evidence",
                    )
                else:
                    raise Failure(
                        f"{artifact_id} {mutation_class} production validator accepted mutation"
                    )
                mutation_evidence_sha256 = hashlib.sha256(
                    obligation_validators.canonical_json_bytes(
                        mutation_evidence
                    )
                ).hexdigest()
                raw_mutated_sha256 = mutated_digest
                mutated_digest = hashlib.sha256(
                    obligation_validators.canonical_json_bytes({
                        "artifact_id": artifact_id,
                        "mutation_class": mutation_class,
                        "raw_mutated_sha256": raw_mutated_sha256,
                        "mutation_evidence_sha256": mutation_evidence_sha256,
                    })
                ).hexdigest()
                mutated_hashes[case_id] = mutated_digest
                rows.append({
                    "case_id": case_id,
                    "artifact_id": artifact_id,
                    "fixture_id": fixture_id,
                    "mutation_class": mutation_class,
                    "byte_mutation": byte_mutation,
                    "expected_refusal": expected_mutation_refusal(
                        artifact_id, mutation_class,
                    ),
                    "actual_refusal": actual_refusal,
                    "positive_fixture_sha256": positive_hashes[fixture_id],
                    "mutated_fixture_sha256": mutated_digest,
                    "mutation_evidence_sha256": mutation_evidence_sha256,
                    "production_hook": production_hook,
                    "validator_function": validator_function,
                    "production_sink_calls": 1,
                    "canonical_artifact_created": False,
                    "passed": True,
                })
    if any(path.exists() for path in protected):
        raise Failure("mutation suite created a canonical artifact")
    if not exact_tree_equal(current_source_sha256(), source_sha256):
        raise Failure("mutation suite invalidated by source hash drift")
    builder.validate_freeze_document(freeze)
    ledger = {
        "schema": MUTATION_LEDGER_SCHEMA,
        "classification": MUTATION_LEDGER_CLASSIFICATION,
        "audited_packet": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012",
        "sealed_input_commit": "42f1ea3301ccf98802c07f3330d52999385cba0b",
        "obligation_matrix_path": OBLIGATION_MATRIX_RELATIVE,
        "obligation_matrix_sha256": matrix_digest,
        "freeze_sha256": sha256(FREEZE),
        "source_sha256": source_sha256,
        "positive_fixture_sha256_by_id": positive_hashes,
        "mutated_fixture_sha256_by_case_id": mutated_hashes,
        "validator_module": {
            "path": (
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                "production_obligation_validators.py"
            ),
            "sha256": source_sha256["production_obligation_validators.py"],
        },
        "production_hook": PRODUCTION_FIXTURE_HOOK,
        "positive_sink_call_count": len(positive_hashes),
        "mutation_sink_call_count": len(rows),
        "case_count": len(rows),
        "checks_passed": len(rows),
        "checks_total": len(rows),
        "canonical_artifact_created": False,
        "cases": rows,
        "claim_boundary": MUTATION_LEDGER_CLAIM_BOUNDARY,
    }
    validate_mutation_ledger(ledger, matrix, freeze)
    return ledger, {
        "artifacts": len(matrix["artifacts"]),
        "positive_fixtures": len(positive_hashes),
        "mutation_classes": len(matrix["mutation_catalog"]),
        "mutation_assignments": len(rows),
        "positive_sink_calls": len(positive_hashes),
        "mutation_sink_calls": len(rows),
    }


def validate_mutation_ledger(
    ledger: dict[str, object], matrix: dict[str, object],
    freeze: dict[str, object],
) -> None:
    required_keys = {
        "schema", "classification", "audited_packet", "sealed_input_commit",
        "obligation_matrix_path", "obligation_matrix_sha256", "freeze_sha256",
        "source_sha256", "positive_fixture_sha256_by_id",
        "mutated_fixture_sha256_by_case_id", "validator_module",
        "production_hook", "positive_sink_call_count", "mutation_sink_call_count",
        "case_count", "checks_passed", "checks_total",
        "canonical_artifact_created", "cases", "claim_boundary",
    }
    rows = ledger.get("cases")
    expected_order = [
        (
            artifact["id"],
            artifact.get("mutation_fixture_by_class", {}).get(
                mutation_class, artifact["positive_fixture"]["id"]
            ),
            mutation_class,
        )
        for artifact in matrix["artifacts"]
        for mutation_class in artifact["mutation_classes"]
    ]
    if (
        set(ledger) != required_keys
        or ledger.get("schema") != MUTATION_LEDGER_SCHEMA
        or ledger.get("classification") != MUTATION_LEDGER_CLASSIFICATION
        or ledger.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or ledger.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or ledger.get("obligation_matrix_path") != OBLIGATION_MATRIX_RELATIVE
        or ledger.get("obligation_matrix_sha256") != OBLIGATION_MATRIX_SHA256
        or ledger.get("freeze_sha256") != sha256(FREEZE)
        or not exact_tree_equal(ledger.get("source_sha256"), freeze.get("files"))
        or ledger.get("validator_module") != {
            "path": (
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                "production_obligation_validators.py"
            ),
            "sha256": freeze["files"]["production_obligation_validators.py"],
        }
        or ledger.get("production_hook") != PRODUCTION_FIXTURE_HOOK
        or type(ledger.get("positive_sink_call_count")) is not int
        or ledger.get("positive_sink_call_count") != 33
        or type(ledger.get("mutation_sink_call_count")) is not int
        or ledger.get("mutation_sink_call_count") != 477
        or type(ledger.get("case_count")) is not int
        or ledger.get("case_count") != 477
        or type(ledger.get("checks_passed")) is not int
        or ledger.get("checks_passed") != 477
        or type(ledger.get("checks_total")) is not int
        or ledger.get("checks_total") != 477
        or ledger.get("canonical_artifact_created") is not False
        or ledger.get("claim_boundary") != MUTATION_LEDGER_CLAIM_BOUNDARY
        or not isinstance(rows, list)
        or len(rows) != 477
    ):
        raise Failure("mutation ledger identity/count/source binding mismatch")
    positive_hashes = ledger.get("positive_fixture_sha256_by_id")
    mutated_hashes = ledger.get("mutated_fixture_sha256_by_case_id")
    expected_positive_ids = {
        fixture["id"]
        for artifact in matrix["artifacts"]
        for fixture in [artifact["positive_fixture"]] + artifact.get(
            "positive_fixture_variants", []
        )
    }
    if (
        not isinstance(positive_hashes, dict)
        or set(positive_hashes) != expected_positive_ids
        or len(set(positive_hashes.values())) != 33
        or not isinstance(mutated_hashes, dict)
        or set(mutated_hashes) != {f"MCASE_{index:04d}" for index in range(1, 478)}
        or len(set(mutated_hashes.values())) != 477
        or any(
            not isinstance(value, str) or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
            for value in list(positive_hashes.values()) + list(mutated_hashes.values())
        )
    ):
        raise Failure("mutation ledger fixture-hash census mismatch")
    row_keys = {
        "case_id", "artifact_id", "fixture_id", "mutation_class",
        "byte_mutation", "expected_refusal", "actual_refusal",
        "positive_fixture_sha256", "mutated_fixture_sha256",
        "mutation_evidence_sha256", "production_hook", "validator_function",
        "production_sink_calls",
        "canonical_artifact_created", "passed",
    }
    for index, (row, expected) in enumerate(zip(rows, expected_order), start=1):
        artifact_id, fixture_id, mutation_class = expected
        custody_hook = {
            "M12_SYMLINK_OR_WRITABLE": "validate_preflight.read_strict_immutable_json",
            "M13_DESCRIPTOR_TOCTOU": "validate_preflight.validate_held_descriptor_identity",
            "M25_IMPORT_TARGET_VALIDATOR": (
                "validate_preflight.validate_independent_auditor_source_bytes"
            ),
            "M28_PREMATURE_ARTIFACT": "validate_preflight.require_artifacts_absent",
        }.get(mutation_class)
        expected_hook = custody_hook or (
            A22_STATEFUL_HOOK_BY_FIXTURE[fixture_id]
            if artifact_id == "A22_TARGET_L12_AUTHORIZATION"
            else PRODUCTION_FIXTURE_HOOK
        )
        expected_validator = expected_hook if custody_hook or (
            artifact_id == "A22_TARGET_L12_AUTHORIZATION"
        ) else obligation_validators.VALIDATOR_FUNCTION_BY_ARTIFACT[artifact_id]
        if (
            not isinstance(row, dict)
            or set(row) != row_keys
            or row.get("case_id") != f"MCASE_{index:04d}"
            or row.get("artifact_id") != artifact_id
            or row.get("fixture_id") != fixture_id
            or row.get("mutation_class") != mutation_class
            or not isinstance(row.get("byte_mutation"), str)
            or not row["byte_mutation"]
            or row.get("expected_refusal")
            != expected_mutation_refusal(artifact_id, mutation_class)
            or not isinstance(row.get("actual_refusal"), str)
            or not row["actual_refusal"]
            or not exact_refusal_match(
                row["actual_refusal"], row["expected_refusal"],
            )
            or row.get("positive_fixture_sha256") != positive_hashes[fixture_id]
            or row.get("mutated_fixture_sha256")
            != mutated_hashes[f"MCASE_{index:04d}"]
            or not isinstance(row.get("mutation_evidence_sha256"), str)
            or len(row["mutation_evidence_sha256"]) != 64
            or any(character not in "0123456789abcdef"
                   for character in row["mutation_evidence_sha256"])
            or row.get("production_hook") != expected_hook
            or row.get("validator_function") != expected_validator
            or type(row.get("production_sink_calls")) is not int
            or row["production_sink_calls"] != 1
            or row.get("canonical_artifact_created") is not False
            or row.get("passed") is not True
        ):
            raise Failure(f"mutation ledger row mismatch: MCASE_{index:04d}")


RESULT_CHECK_KEYS = {
    "syntax_files", "portable_os_stat_runtime_checks",
    "zero_length_cache_runtime_checks", "strict_json_descriptor_checks",
    "v011_exact_type_repairs", "authenticated_dependency_records",
    "audit_obligation_artifacts", "audit_obligation_positive_fixtures",
    "audit_obligation_mutation_classes", "audit_obligation_mutation_assignments",
    "audit_obligation_positive_sink_calls", "audit_obligation_mutation_sink_calls",
    "authorization_dag_states", "authorization_dag_invalid_state_action_refusals",
    "authorization_dag_legal_reachable_states", "freeze_mutation_refusals",
    "obstruction_custody_and_global_alias_checks",
    "future_hostile_audit_gate_refusals",
    "target_fixed_words_width_0_through_16_comparisons",
    "L4_oriented_edge_charge_pair_checks", "L4_admission_event_charge_checks",
    "L4_lineage_prefix_charge_checks", "allocation_lengths",
    "parallel_resource_certificate_checks", "hard_lock_entrypoints",
}


def expected_allocation_census() -> list[dict[str, int]]:
    return [
        {
            "L": length,
            "operator_bytes": expected[0],
            "admission_bytes": expected[1],
            "lineage_mask_bytes": expected[2],
            "lineage_map_bytes": expected[3],
            "payload_bytes": expected[4],
            "maximum_state_bytes": expected[5],
            "state_plus_cache_plus_reserve_bytes": (
                expected[4] + expected[5] + builder.OVERHEAD_RESERVE
            ),
            "terminal_cache_peak_bytes": expected[6],
            "authentication_cache_peak_bytes": expected[7],
            "maximum_cache_window_bytes": expected[8],
            "file_count": expected[9],
        }
        for length, expected in EXPECTED_CENSUS.items()
    ]


def expected_resource_limits() -> dict[str, object]:
    return {
        "numerical_workset_bytes": builder.v004.v3.CAP_BYTES,
        "mapped_cache_bytes": builder.MAPPED_CACHE_LIMIT,
        "builder_rss_bytes": builder.BUILDER_RSS_LIMIT,
        "consumer_rss_bytes": builder.v004.RSS_LIMIT,
        "scratch_bytes": builder.SCRATCH_LIMIT,
        "overhead_reserve_bytes": builder.OVERHEAD_RESERVE,
        "wall_seconds": int(builder.WALL_LIMIT),
        "parallel_l12": {
            "target_rss_limit_bytes": builder.v004.RSS_LIMIT,
            "target_authentication_peak_bytes": builder.PARALLEL_TARGET_AUTHENTICATION_PEAK,
            "hostile_rss_limit_bytes": builder.PARALLEL_HOSTILE_RSS_LIMIT,
            "hostile_authentication_peak_bytes": builder.PARALLEL_HOSTILE_AUTHENTICATION_PEAK,
            "combined_conservative_peak_bytes": builder.PARALLEL_AGGREGATE_PEAK,
            "minimum_host_total_bytes": builder.PARALLEL_HOST_TOTAL_MINIMUM,
            "minimum_host_headroom_bytes": builder.PARALLEL_HOST_HEADROOM_MINIMUM,
            "target_scratch_minimum_bytes": builder.PARALLEL_TARGET_SCRATCH_MINIMUM,
            "hostile_scratch_minimum_bytes": builder.PARALLEL_HOSTILE_SCRATCH_MINIMUM,
            "hostile_peak_live_raw_c128_shard_count": 23,
            "hostile_container_header_bytes": 0,
            "combined_filesystem_minimum_bytes": builder.PARALLEL_FILESYSTEM_MINIMUM,
            "maximum_telemetry_age_seconds": 300,
        },
    }


def expected_result_files(freeze: dict[str, object]) -> dict[str, str]:
    frozen = freeze.get("files")
    if not isinstance(frozen, dict) or set(frozen) != {
        "METHOD.md", "build_target_cache.py", "consume_target_cache.py",
        "production_obligation_validators.py", "validate_preflight.py",
    }:
        raise Failure("preflight frozen file census mismatch")
    return {
        "method_sha256": frozen["METHOD.md"],
        "builder_sha256": frozen["build_target_cache.py"],
        "consumer_sha256": frozen["consume_target_cache.py"],
        "production_obligation_validators_sha256": frozen[
            "production_obligation_validators.py"
        ],
        "preflight_sha256": frozen["validate_preflight.py"],
        "freeze_sha256": sha256(FREEZE),
    }


def validate_preflight_result_document(
    result: object, freeze: dict[str, object], ledger_sha256: str,
) -> dict[str, object]:
    """Fully reconstruct the evidence document before immutable publication."""
    required_keys = {
        "schema", "classification", "physical_cache_payload_created",
        "physical_history_executed", "checks", "L4_differential",
        "allocation_census", "resource_limits", "files", "mutation_ledger",
        "compatibility", "claim_boundary",
    }
    if not isinstance(result, dict) or set(result) != required_keys:
        raise Failure("preflight result exact top-level census mismatch")
    if (
        result.get("schema") != "TARGET_L12_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT_V012"
        or result.get("classification")
        != "PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT"
        or result.get("physical_cache_payload_created") is not False
        or result.get("physical_history_executed") is not False
        or result.get("claim_boundary")
        != "V012_PORTABLE_NONPHYSICAL_STORAGE_INDEX_PROOF_ONLY__NO_CACHE_PAYLOAD_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
    ):
        raise Failure("preflight result identity/nonexecution/claim mismatch")
    checks = result.get("checks")
    if (
        not isinstance(checks, dict) or set(checks) != RESULT_CHECK_KEYS
        or any(type(value) is not int or value <= 0 for value in checks.values())
        or checks["syntax_files"] != 4
        or checks["audit_obligation_artifacts"] != 26
        or checks["audit_obligation_positive_fixtures"] != 33
        or checks["audit_obligation_mutation_classes"] != 36
        or checks["audit_obligation_mutation_assignments"] != 477
        or checks["audit_obligation_positive_sink_calls"] != 33
        or checks["audit_obligation_mutation_sink_calls"] != 477
        or checks["authorization_dag_states"] != 262144
        or checks["authorization_dag_invalid_state_action_refusals"] != 4718124
        or checks["authorization_dag_legal_reachable_states"] != 26
        or checks["allocation_lengths"] != 5
        or checks["hard_lock_entrypoints"] != 12
    ):
        raise Failure("preflight result check census/type/reconstruction mismatch")
    differential = result.get("L4_differential")
    if (
        not isinstance(differential, dict)
        or set(differential) != {
            "maximum_h_error", "maximum_signed_current_error",
        }
        or any(type(value) is not float or not math.isfinite(value)
               for value in differential.values())
        or any(value > 1.0e-12 for value in differential.values())
    ):
        raise Failure("preflight result L4 differential mismatch")
    allocation = result.get("allocation_census")
    expected_allocation = expected_allocation_census()
    if not exact_tree_equal(allocation, expected_allocation):
        raise Failure("preflight result allocation census mismatch")
    for row in allocation:
        if any(type(value) is not int for value in row.values()):
            raise Failure("preflight result allocation exact integer mismatch")
    if not exact_tree_equal(result.get("resource_limits"), expected_resource_limits()):
        raise Failure("preflight result resource-limit census mismatch")
    if not exact_tree_equal(result.get("files"), expected_result_files(freeze)):
        raise Failure("preflight result frozen-file binding mismatch")
    expected_ledger = {
        "path": str(MUTATION_LEDGER.relative_to(ROOT)),
        "sha256": ledger_sha256,
        "schema": MUTATION_LEDGER_SCHEMA,
        "classification": MUTATION_LEDGER_CLASSIFICATION,
        "case_count": 477,
        "positive_sink_call_count": 33,
        "mutation_sink_call_count": 477,
        "obligation_matrix_sha256": OBLIGATION_MATRIX_SHA256,
        "validator_module_sha256": freeze["files"][
            "production_obligation_validators.py"
        ],
    }
    if not exact_tree_equal(result.get("mutation_ledger"), expected_ledger):
        raise Failure("preflight result mutation-ledger binding mismatch")
    expected_compatibility = {
        "superseded_v005_payloads_consumed": False,
        "portable_os_stat_follow_symlinks_supported": True,
        "fresh_v012_cache_root": str(builder.CACHE_PARENT),
        "superseded_v006_payloads_consumed": False,
        "superseded_v007_payloads_consumed": False,
        "superseded_v008_payloads_consumed": False,
        "superseded_v009_payloads_consumed": False,
        "superseded_v010_payloads_consumed": False,
        "superseded_v011_payloads_consumed": False,
    }
    if not exact_tree_equal(result.get("compatibility"), expected_compatibility):
        raise Failure("preflight result compatibility/nonconsumption mismatch")
    obligation_validators.validate_record(
        "A02_NONPHYSICAL_PREFLIGHT", result,
        mutation_class="PRODUCTION_NATIVE_RECORD", fixture_mode=False,
    )
    return result


def validate_existing_result_state() -> None:
    if not MUTATION_LEDGER.exists() and not RESULT.exists():
        return
    if MUTATION_LEDGER.exists():
        try:
            ledger, _ = read_strict_immutable_json(
                MUTATION_LEDGER, "existing V012 mutation ledger"
            )
        except (Failure, OSError, ValueError, json.JSONDecodeError) as error:
            raise Failure(f"existing mutation ledger is invalid: {error}") from error
        if not exact_tree_equal(ledger.get("source_sha256"), current_source_sha256()):
            raise Failure("prior mutation ledger invalidated by source hash drift")
    if RESULT.exists() and not MUTATION_LEDGER.exists():
        raise Failure("preflight result exists without its immutable mutation ledger")
    if MUTATION_LEDGER.exists() and not RESULT.exists():
        raise Failure("partial prior mutation ledger exists without preflight result")
    raise Failure("preflight result already exists for the current source hashes")


def independent_words(width: int, weight: int) -> np.ndarray:
    values: list[int] = []
    for chosen in itertools.combinations(range(width), weight):
        word = 0
        for bit in chosen:
            word |= 1 << bit
        values.append(word)
    return np.asarray(values, dtype=np.uint32)


def validate_freeze() -> dict[str, object]:
    check(FREEZE.is_file(), "freeze absent")
    freeze, _freeze_sha256 = read_strict_immutable_json(FREEZE, "V012 freeze")
    check(builder.validate_freeze_document(freeze) == freeze, "complete immutable freeze census")
    return freeze


def validate_dependencies() -> int:
    check(
        obligation_validators.FINAL_AUDITOR_SHA256
        == builder.TRACK_C_REFINEMENT_SHA256[
            "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/"
            "independent_final_auditor.py"
        ],
        "production final-auditor pin disagrees with frozen dependency",
    )
    check(
        obligation_validators.MUTATION_EXPECTED_REFUSAL == MUTATION_REFUSAL,
        "production/preflight mutation refusal catalogs disagree",
    )
    check(
        len(obligation_validators.FINAL_NATIVE_MUTATION_REFUSAL) == 73,
        "production final-native refusal map census drift",
    )
    check(
        getattr(
            obligation_validators._final_auditor(),
            "FINAL_NATIVE_MUTATION_REFUSAL",
            None,
        ) == obligation_validators.FINAL_NATIVE_MUTATION_REFUSAL,
        "target/final-auditor native refusal maps disagree",
    )
    a03_fixture = obligation_validators.positive_fixture(
        "A03_PREPAYLOAD_AUDIT"
    )
    frozen, _freeze_sha256 = read_strict_immutable_json(
        FREEZE, "V012 freeze for A03 shape assertion"
    )
    check(
        set(a03_fixture["audited_files_sha256"])
        == set(frozen["files"])
        == set(obligation_validators.FROZEN_SOURCE_FILENAMES)
        and all(
            isinstance(digest, str) and len(digest) == 64
            and all(character in "0123456789abcdef" for character in digest)
            for digest in a03_fixture["audited_files_sha256"].values()
        ),
        "A03 audited frozen-source hash-map shape mismatch",
    )
    obligation_validators.validate_record(
        "A03_PREPAYLOAD_AUDIT", a03_fixture,
        mutation_class="PRODUCTION_NATIVE_RECORD", fixture_mode=True,
    )
    custody = {
        builder.TARGET_V004: builder.TARGET_V004_SHA256,
        builder.TARGET_METHOD_V004: builder.TARGET_METHOD_V004_SHA256,
        builder.TARGET_FREEZE_V004: builder.TARGET_FREEZE_V004_SHA256,
        builder.TARGET_L12_GATE_V004: builder.TARGET_L12_GATE_V004_SHA256,
        builder.HOSTILE_V003: builder.HOSTILE_V003_SHA256,
        builder.HOSTILE_METHOD_V003: builder.HOSTILE_METHOD_V003_SHA256,
        builder.HOSTILE_FREEZE_V003: builder.HOSTILE_FREEZE_V003_SHA256,
        builder.PRESERVED_WORKSPACE_CUSTODY: builder.PRESERVED_WORKSPACE_CUSTODY_SHA256,
        builder.PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC:
            builder.PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        builder.TARGET_V004_INVARIANTS: builder.TARGET_V004_INVARIANTS_SHA256,
        builder.INDEPENDENT_L10_GATE_V002: builder.INDEPENDENT_L10_GATE_V002_SHA256,
        builder.RUNTIME_COMPATIBILITY_OBSTRUCTION:
            builder.RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
        builder.V006_HOSTILE_OBSTRUCTION: builder.V006_HOSTILE_OBSTRUCTION_SHA256,
        builder.V007_RUNTIME_OBSTRUCTION: builder.V007_RUNTIME_OBSTRUCTION_SHA256,
        builder.V008_BINDING_OBSTRUCTION: builder.V008_BINDING_OBSTRUCTION_SHA256,
        builder.V009_HOSTILE_OBSTRUCTION: builder.V009_HOSTILE_OBSTRUCTION_SHA256,
        builder.V010_HOSTILE_OBSTRUCTION: builder.V010_HOSTILE_OBSTRUCTION_SHA256,
        builder.V010_CUSTODY_CORRECTION: builder.V010_CUSTODY_CORRECTION_SHA256,
        builder.V011_HOSTILE_OBSTRUCTION: builder.V011_HOSTILE_OBSTRUCTION_SHA256,
        **{
            path: builder.CANONICAL_V004_HISTORY_SHA256[length]
            for length, path in builder.CANONICAL_V004_HISTORY_PATH.items()
        },
        **{builder.ROOT / relative: digest
           for relative, digest in builder.AUDIT_OBLIGATION_CONTRACT_SHA256.items()},
        **{builder.ROOT / relative: digest
           for relative, digest in builder.AUTHORIZATION_DAG_MODEL_SHA256.items()},
        **{builder.ROOT / relative: digest
           for relative, digest in builder.DUAL_LAUNCH_COORDINATOR_SHA256.items()},
        **{builder.ROOT / relative: digest
           for relative, digest in builder.TRACK_C_REFINEMENT_SHA256.items()},
    }
    check(
        all(not path.is_symlink() and path.is_file() and sha256(path) == digest for path, digest in custody.items()),
        "V004 custody",
    )
    builder.require_original_target_gate()
    builder.require_preserved_workspace_custody()
    builder.require_preserved_workspace_cross_diagnostic()
    builder.require_runtime_compatibility_obstruction()
    builder.require_v006_hostile_audit_obstruction()
    builder.require_v007_runtime_compatibility_obstruction()
    builder.require_v008_postbuild_binding_obstruction()
    builder.require_v009_hostile_audit_obstruction()
    builder.require_v010_hostile_audit_obstruction_and_correction()
    builder.require_v011_hostile_audit_obstruction()
    builder.require_audit_preparation_contracts()
    return len(custody)


def validate_freeze_mutation_refusals(freeze: dict[str, object]) -> int:
    mutations: list[tuple[dict[str, object], str]] = []
    missing_file = copy.deepcopy(freeze)
    del missing_file["files"]["consume_target_cache.py"]
    mutations.append((missing_file, "file census"))
    wrong_peak = copy.deepcopy(freeze)
    wrong_peak["storage_census_including_offsets_and_full_masks"]["12"][
        "authentication_cache_peak_bytes"
    ] -= 1
    mutations.append((wrong_peak, "storage/resource census"))
    wrong_dependency = copy.deepcopy(freeze)
    wrong_dependency["sealed_dependencies"]["preserved_workspace_cross_diagnostic_v001"] = "0" * 64
    mutations.append((wrong_dependency, "dependency census"))
    missing_evidence = copy.deepcopy(freeze)
    del missing_evidence["obstruction_evidence"][
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_WALL_MONITOR.json"
    ]
    mutations.append((missing_evidence, "obstruction-evidence census"))
    wrong_predecessor = copy.deepcopy(freeze)
    wrong_predecessor["predecessor_compatibility_custody"][
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V005/TARGET_V005_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001.json"
    ] = "0" * 64
    mutations.append((wrong_predecessor, "predecessor-compatibility census"))
    wrong_v006 = copy.deepcopy(freeze)
    wrong_v006["predecessor_v006_obstruction_custody"][
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V006/HOSTILE_AUDIT_OBSTRUCTION_V001.json"
    ] = "0" * 64
    mutations.append((wrong_v006, "predecessor-V006 obstruction census"))
    wrong_v007 = copy.deepcopy(freeze)
    wrong_v007["predecessor_v007_obstruction_custody"][
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V007/TARGET_V007_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001.json"
    ] = "0" * 64
    mutations.append((wrong_v007, "predecessor-V007 obstruction census"))
    wrong_v008 = copy.deepcopy(freeze)
    wrong_v008["predecessor_v008_obstruction_custody"][
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V008/V008_POSTBUILD_AUDIT_BINDING_OBSTRUCTION_V001.json"
    ] = "0" * 64
    mutations.append((wrong_v008, "predecessor-V008 obstruction census"))
    wrong_v009 = copy.deepcopy(freeze)
    wrong_v009["predecessor_v009_obstruction_custody"][
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V009/HOSTILE_AUDIT_OBSTRUCTION_V001.json"
    ] = "0" * 64
    mutations.append((wrong_v009, "predecessor-V009 obstruction census"))
    wrong_v010 = copy.deepcopy(freeze)
    wrong_v010["predecessor_v010_obstruction_custody"][
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V010/HOSTILE_AUDIT_OBSTRUCTION_V001.json"
    ] = "0" * 64
    mutations.append((wrong_v010, "predecessor-V010 obstruction census"))
    wrong_v011 = copy.deepcopy(freeze)
    wrong_v011["predecessor_v011_obstruction_custody"][
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V011/HOSTILE_AUDIT_OBSTRUCTION_V001.json"
    ] = "0" * 64
    mutations.append((wrong_v011, "predecessor-V011 obstruction census"))
    for mutated, fragment in mutations:
        expect_refusal(
            lambda candidate=mutated: builder.validate_freeze_document(candidate),
            fragment,
            f"freeze mutation was accepted: {fragment}",
        )
    return len(mutations)


def valid_obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "role": "target",
            "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_OBSTRUCTION.json",
            "sha256": builder.EVIDENCE_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_OBSTRUCTION.json"],
        },
        {
            "role": "hostile",
            "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_OBSTRUCTION.json",
            "sha256": builder.EVIDENCE_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_OBSTRUCTION.json"],
        },
    ]


def validate_obstruction_custody_and_alias_rejection() -> int:
    rows = valid_obstruction_rows()
    records = builder.validate_obstruction_rows(rows)
    check(len(records) == 2, "valid target/hostile obstruction pair rejected")
    alias = copy.deepcopy(rows)
    alias[1]["path"] = (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/"
        "TARGET_V004_EXECUTION_LOG.md"
    )
    alias[1]["sha256"] = builder.EVIDENCE_SHA256[
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_EXECUTION_LOG.md"
    ]
    expect_refusal(
        lambda: builder.validate_obstruction_rows(alias),
        "globally distinct",
        "cross-row obstruction/evidence alias was accepted",
    )
    return 2


def candidate_dual_gate(freeze: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "TARGET_V012_DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE",
        "classification": "AUTHORIZE_TARGET_V012_FRESH_CACHE_AFTER_V005_V006_V007_V008_V009_V010_AND_V011_CONTROL_PLANE_OBSTRUCTIONS",
        "method_sha256": freeze["files"]["METHOD.md"],
        "builder_sha256": freeze["files"]["build_target_cache.py"],
        "consumer_sha256": freeze["files"]["consume_target_cache.py"],
        "preflight_sha256": freeze["files"]["validate_preflight.py"],
        "freeze_sha256": sha256(FREEZE),
        "preflight_result_sha256": "0" * 64,
        "target_v004_sha256": builder.TARGET_V004_SHA256,
        "hostile_v003_sha256": builder.HOSTILE_V003_SHA256,
        "preserved_workspace_custody_sha256": builder.PRESERVED_WORKSPACE_CUSTODY_SHA256,
        "preserved_workspace_cross_diagnostic_sha256": builder.PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        "runtime_compatibility_obstruction_sha256": builder.RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
        "superseded_v005_dual_gate_sha256": builder.V005_DUAL_GATE_SHA256,
        "superseded_v005_cache_manifest_sha256_by_L": builder.V005_CACHE_MANIFEST_SHA256,
        "v006_hostile_audit_obstruction_sha256": builder.V006_HOSTILE_OBSTRUCTION_SHA256,
        "v007_runtime_compatibility_obstruction_sha256": builder.V007_RUNTIME_OBSTRUCTION_SHA256,
        "superseded_v007_dual_gate_sha256": builder.V007_DUAL_GATE_SHA256,
        "superseded_v007_cache_manifest_sha256_by_L": builder.V007_CACHE_MANIFEST_SHA256,
        "v008_postbuild_audit_binding_obstruction_sha256": builder.V008_BINDING_OBSTRUCTION_SHA256,
        "superseded_v008_dual_gate_sha256": builder.V008_DUAL_GATE_SHA256,
        "superseded_v008_cache_manifest_sha256_by_L": builder.V008_CACHE_MANIFEST_SHA256,
        "v009_hostile_audit_obstruction_sha256": builder.V009_HOSTILE_OBSTRUCTION_SHA256,
        "v010_hostile_audit_obstruction_sha256": builder.V010_HOSTILE_OBSTRUCTION_SHA256,
        "v010_audit_record_custody_correction_sha256": builder.V010_CUSTODY_CORRECTION_SHA256,
        "v011_hostile_audit_obstruction_sha256": builder.V011_HOSTILE_OBSTRUCTION_SHA256,
        "independent_hostile_audit": {
            "path": builder.FUTURE_HOSTILE_AUDIT_PATH,
            "sha256": "0" * 64,
        },
        "authorized_cache_lengths": list(builder.SUPPORTED),
        "obstructions": valid_obstruction_rows(),
        "claim_boundary": "CONTROL_PLANE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT",
    }


def validate_future_audit_gate_refusals(freeze: dict[str, object]) -> int:
    candidate = candidate_dual_gate(freeze)
    cases: list[tuple[dict[str, object], str]] = []
    missing = copy.deepcopy(candidate)
    del missing["independent_hostile_audit"]
    cases.append((missing, "key census"))
    wrong_obstruction = copy.deepcopy(candidate)
    wrong_obstruction["v006_hostile_audit_obstruction_sha256"] = "0" * 64
    cases.append((wrong_obstruction, "v006_hostile_audit_obstruction_sha256"))
    wrong_v007_obstruction = copy.deepcopy(candidate)
    wrong_v007_obstruction["v007_runtime_compatibility_obstruction_sha256"] = "0" * 64
    cases.append((wrong_v007_obstruction, "v007_runtime_compatibility_obstruction_sha256"))
    wrong_v008_obstruction = copy.deepcopy(candidate)
    wrong_v008_obstruction["v008_postbuild_audit_binding_obstruction_sha256"] = "0" * 64
    cases.append((wrong_v008_obstruction, "v008_postbuild_audit_binding_obstruction_sha256"))
    wrong_v009_obstruction = copy.deepcopy(candidate)
    wrong_v009_obstruction["v009_hostile_audit_obstruction_sha256"] = "0" * 64
    cases.append((wrong_v009_obstruction, "v009_hostile_audit_obstruction_sha256"))
    wrong_v010_obstruction = copy.deepcopy(candidate)
    wrong_v010_obstruction["v010_hostile_audit_obstruction_sha256"] = "0" * 64
    cases.append((wrong_v010_obstruction, "v010_hostile_audit_obstruction_sha256"))
    wrong_v010_correction = copy.deepcopy(candidate)
    wrong_v010_correction["v010_audit_record_custody_correction_sha256"] = "0" * 64
    cases.append((wrong_v010_correction, "v010_audit_record_custody_correction_sha256"))
    wrong_v011_obstruction = copy.deepcopy(candidate)
    wrong_v011_obstruction["v011_hostile_audit_obstruction_sha256"] = "0" * 64
    cases.append((wrong_v011_obstruction, "v011_hostile_audit_obstruction_sha256"))
    absent_audit = copy.deepcopy(candidate)
    cases.append((absent_audit, "custody mismatch"))
    extra_audit_key = copy.deepcopy(candidate)
    extra_audit_key["independent_hostile_audit"]["classification"] = "PASS"
    cases.append((extra_audit_key, "specification malformed"))
    wrong_audit_path = copy.deepcopy(candidate)
    wrong_audit_path["independent_hostile_audit"]["path"] = (
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V006/HOSTILE_AUDIT_OBSTRUCTION_V001.json"
    )
    wrong_audit_path["independent_hostile_audit"]["sha256"] = builder.V006_HOSTILE_OBSTRUCTION_SHA256
    cases.append((wrong_audit_path, "path mismatch"))
    for mutated, fragment in cases:
        expect_refusal(
            lambda value=mutated: builder.validate_dual_gate_document(
                value, 4, freeze, "0" * 64
            ),
            fragment,
            f"V012 audit-gate mutation accepted: {fragment}",
        )
    return len(cases)


def validate_history_serialization_projection_regression() -> None:
    """Exercise the two fixed-field native projections used by A10/A14/A24."""
    coarse_source = consumer.v004.sealed.COARSE.__dict__
    fine_source = consumer.v004.sealed.FINE.__dict__
    owner = np.float64(1.25e-14)
    sentinel = {"unchanged": [1, 2, 3]}
    source_rows = [{
        "target_owner_residual": owner,
        "sentinel": sentinel,
    }]
    projected = {
        "coarse_method": consumer.project_native_method_record(
            consumer.v004.sealed.COARSE
        ),
        "fine_method": consumer.project_native_method_record(
            consumer.v004.sealed.FINE
        ),
        "rows": consumer.project_native_history_rows(source_rows),
    }
    check(
        type(coarse_source["checkpoints"]) is tuple
        and type(fine_source["checkpoints"]) is tuple
        and type(projected["coarse_method"]["checkpoints"]) is list
        and type(projected["fine_method"]["checkpoints"]) is list,
        "history method checkpoint projection mismatch",
    )
    check(
        type(source_rows[0]["target_owner_residual"]) is np.float64
        and type(projected["rows"][0]["target_owner_residual"]) is float
        and projected["rows"][0]["sentinel"] is sentinel,
        "history owner-residual fixed-field projection mismatch",
    )
    decoded = strict_json_object(
        canonical_json_bytes(projected),
        "history native projection round trip",
    )
    differences: list[tuple[str, str, str]] = []

    def enumerate_type_differences(
        before: object, after: object, path: tuple[str, ...] = (),
    ) -> None:
        if type(before) is not type(after):
            differences.append(
                (".".join(path), type(before).__name__, type(after).__name__)
            )
            return
        if type(before) is dict:
            for key in before:
                enumerate_type_differences(
                    before[key], after[key], path + (key,)
                )
        elif type(before) is list:
            for index, (left, right) in enumerate(zip(before, after)):
                enumerate_type_differences(
                    left, right, path + (str(index),)
                )

    enumerate_type_differences(projected, decoded)
    check(
        differences == [] and builder.exact_tree_equal(projected, decoded),
        f"history native projection round-trip differences: {differences}",
    )
    expect_refusal(
        lambda: consumer.project_native_method_record(types.SimpleNamespace(
            label="coarse", checkpoints=[12, 18], quadrature_nodes=16,
            tolerance=2.0e-9,
        )),
        "method native projection source mismatch",
        "history checkpoint list source unexpectedly accepted",
    )
    expect_refusal(
        lambda: consumer.project_native_method_record(types.SimpleNamespace(
            label="coarse", checkpoints=(12, 18.0), quadrature_nodes=16,
            tolerance=2.0e-9,
        )),
        "method native projection source mismatch",
        "history non-integer checkpoint source unexpectedly accepted",
    )
    expect_refusal(
        lambda: consumer.project_native_history_rows([{
            "target_owner_residual": float(owner), "sentinel": sentinel,
        }]),
        "owner residual projection source mismatch",
        "history native owner-residual source unexpectedly accepted",
    )
    for artifact_id in (
        "A10_CONTROL_HISTORIES", "A14_L10_HISTORY",
        "A24_TARGET_L12_HISTORY",
    ):
        fixture = obligation_validators.positive_fixture(artifact_id)
        obligation_validators.validate_record(
            artifact_id, fixture,
            mutation_class="POSITIVE_CONTROL", fixture_mode=True,
        )
        expected_nulls = (
            obligation_validators.SANCTIONED_NULL_STAGE_HASH_KEYS[artifact_id]
        )
        check(
            {
                key for key in obligation_validators.HISTORY_STAGE_HASH_KEYS
                if fixture[key] is None
            } == expected_nulls,
            f"{artifact_id} sanctioned null stage-hash pattern mismatch",
        )

    def expect_history_obligation_refusal(
        artifact_id: str, record: dict[str, object], fragment: str, label: str,
    ) -> None:
        try:
            obligation_validators.validate_record(
                artifact_id, record, mutation_class="PROJECTION_REGRESSION",
                fixture_mode=True,
            )
        except obligation_validators.Refusal as error:
            check(
                fragment in str(error),
                f"{label}: wrong refusal: {error}",
            )
        else:
            raise Failure(f"{label}: malformed stage-hash pattern accepted")

    a10_missing_none = obligation_validators.positive_fixture(
        "A10_CONTROL_HISTORIES"
    )
    a10_missing_none[
        obligation_validators.HISTORY_STAGE_HASH_KEYS[0]
    ] = hashlib.sha256(b"A10 missing expected None").hexdigest()
    expect_history_obligation_refusal(
        "A10_CONTROL_HISTORIES", a10_missing_none,
        "stage predecessor mismatch", "A10 missing expected None",
    )
    a14_extra_none = obligation_validators.positive_fixture(
        "A14_L10_HISTORY"
    )
    a14_extra_none[
        obligation_validators.HISTORY_STAGE_HASH_KEYS[0]
    ] = None
    expect_history_obligation_refusal(
        "A14_L10_HISTORY", a14_extra_none,
        "path/hash mismatch", "A14 extra None",
    )
    a10_wrong_stage = obligation_validators.positive_fixture(
        "A10_CONTROL_HISTORIES"
    )
    for key in obligation_validators.HISTORY_STAGE_HASH_KEYS[:3]:
        a10_wrong_stage[key] = hashlib.sha256(
            f"A10 wrong-stage {key}".encode("ascii")
        ).hexdigest()
    expect_history_obligation_refusal(
        "A10_CONTROL_HISTORIES", a10_wrong_stage,
        "stage predecessor mismatch", "A10 admitted A14 stage pattern",
    )
    a14_noncanonical_hash = obligation_validators.positive_fixture(
        "A14_L10_HISTORY"
    )
    a14_noncanonical_hash[
        obligation_validators.HISTORY_STAGE_HASH_KEYS[0]
    ] = "c" * 63
    expect_history_obligation_refusal(
        "A14_L10_HISTORY", a14_noncanonical_hash,
        "path/hash mismatch", "A14 noncanonical predecessor hash",
    )

    nested_null_cases = 0
    for artifact_id in (
        "A10_CONTROL_HISTORIES", "A14_L10_HISTORY",
    ):
        for key in sorted(
            obligation_validators.SANCTIONED_NULL_STAGE_HASH_KEYS[artifact_id]
        ):
            for container in (
                "rows", "comparison", "resource", "terminal_shards",
            ):
                candidate = obligation_validators.positive_fixture(artifact_id)
                nested = (
                    candidate[container][0]
                    if container in {"rows", "terminal_shards"}
                    else candidate[container]
                )
                check(
                    type(nested) is dict and key not in nested,
                    f"{artifact_id} nested-null fixture collision",
                )
                nested[key] = None
                try:
                    obligation_validators.validate_record(
                        artifact_id, candidate,
                        mutation_class="NESTED_NULL_REGRESSION",
                        fixture_mode=False,
                    )
                except obligation_validators.Refusal as error:
                    check(
                        "path/hash mismatch" in str(error),
                        f"{artifact_id} {container}.{key}: wrong refusal: {error}",
                    )
                else:
                    raise Failure(
                        f"{artifact_id} accepted nested sanctioned null "
                        f"at {container}.{key}"
                    )
                nested_null_cases += 1
    check(
        nested_null_cases == 60,
        "nested sanctioned-null adverse census mismatch",
    )

    final_auditor = obligation_validators._final_auditor()
    upstream = final_auditor._upstream_fixture_records()
    independent_a10 = upstream[("A10_CONTROL_HISTORIES", 1)]
    independent_a14 = upstream[("A14_L10_HISTORY", 1)]
    final_auditor._validate_independent_upstream_record(
        "A10_CONTROL_HISTORIES", independent_a10,
        "A26_FINAL_L12_AUDIT", fixture_mode=True,
    )
    final_auditor._validate_independent_upstream_record(
        "A14_L10_HISTORY", independent_a14,
        "A26_FINAL_L12_AUDIT", fixture_mode=True,
    )
    obligation_validators.validate_record(
        "A26_FINAL_L12_AUDIT",
        obligation_validators.positive_fixture("A26_FINAL_L12_AUDIT"),
        mutation_class="PROJECTION_REGRESSION", fixture_mode=True,
    )

    def expect_independent_history_refusal(
        artifact_id: str, record: dict[str, object], fragment: str, label: str,
    ) -> None:
        try:
            final_auditor._validate_independent_upstream_record(
                artifact_id, record, "A26_FINAL_L12_AUDIT",
                fixture_mode=True,
            )
        except final_auditor.Refusal as error:
            check(fragment in str(error), f"{label}: wrong refusal: {error}")
        else:
            raise Failure(f"{label}: malformed independent pattern accepted")

    independent_a10_missing_none = copy.deepcopy(independent_a10)
    independent_a10_missing_none[
        final_auditor.UPSTREAM_HISTORY_STAGE_HASH_KEYS[0]
    ] = hashlib.sha256(b"independent A10 missing None").hexdigest()
    expect_independent_history_refusal(
        "A10_CONTROL_HISTORIES", independent_a10_missing_none,
        "stage predecessor mismatch", "independent A10 missing expected None",
    )
    independent_a14_extra_none = copy.deepcopy(independent_a14)
    independent_a14_extra_none[
        final_auditor.UPSTREAM_HISTORY_STAGE_HASH_KEYS[0]
    ] = None
    expect_independent_history_refusal(
        "A14_L10_HISTORY", independent_a14_extra_none,
        "must be an exact nonempty string", "independent A14 extra None",
    )
    independent_a14_wrong_stage = copy.deepcopy(independent_a14)
    independent_a14_wrong_stage[
        final_auditor.UPSTREAM_HISTORY_STAGE_HASH_KEYS[3]
    ] = hashlib.sha256(b"independent A14 wrong stage").hexdigest()
    expect_independent_history_refusal(
        "A14_L10_HISTORY", independent_a14_wrong_stage,
        "stage predecessor mismatch", "independent A14 wrong-stage hash",
    )
    independent_a14_noncanonical = copy.deepcopy(independent_a14)
    independent_a14_noncanonical[
        final_auditor.UPSTREAM_HISTORY_STAGE_HASH_KEYS[0]
    ] = "d" * 63
    expect_independent_history_refusal(
        "A14_L10_HISTORY", independent_a14_noncanonical,
        "must be a lowercase SHA-256", "independent A14 noncanonical hash",
    )
    independent_a24_none = obligation_validators.positive_fixture(
        "A24_TARGET_L12_HISTORY"
    )
    independent_a24_none[
        final_auditor.UPSTREAM_HISTORY_STAGE_HASH_KEYS[0]
    ] = None
    try:
        final_auditor.validate_artifact(
            "A24_TARGET_L12_HISTORY", independent_a24_none,
            fixture_mode=True,
        )
    except final_auditor.Refusal as error:
        check(
            "must be an exact nonempty string" in str(error),
            f"independent A24 None: wrong refusal: {error}",
        )
    else:
        raise Failure("independent A24 sanctioned a null stage hash")


def validate_a11_a16_three_sink_parity_regression() -> dict[str, int]:
    """Hold A11--A16 to the same bounded contract at all three ingress sinks."""
    artifact_ids = (
        "A11_CONTROL_STAGE_GATE", "A12_CONTROL_STAGE_AUDIT",
        "A13_L10_AUTHORIZATION", "A14_L10_HISTORY",
        "A15_L10_STAGE_GATE", "A16_L10_STAGE_AUDIT",
    )
    final_auditor = obligation_validators._final_auditor()
    validate_independent_auditor_source_bytes(
        Path(final_auditor.__file__).read_bytes(),
        "A26 independent final auditor",
    )
    independent = final_auditor._upstream_fixture_records()
    production: dict[str, dict[str, object]] = {}
    independent_records: dict[str, dict[str, object]] = {}

    def adverse_records(
        artifact_id: str, source: dict[str, object], *, synthetic: bool,
    ) -> list[tuple[str, dict[str, object]]]:
        cases: list[tuple[str, dict[str, object]]] = []

        def add(label: str, mutation) -> None:
            value = copy.deepcopy(source)
            mutation(value)
            cases.append((label, value))

        if artifact_id in {
            "A11_CONTROL_STAGE_GATE", "A15_L10_STAGE_GATE",
        }:
            add("missing preflight binding", lambda value: value.pop("preflight_sha256"))
            add("missing V004 binding", lambda value: value.pop("target_v004_sha256"))
            add("wrong preflight binding", lambda value: value.__setitem__("preflight_sha256", "0" * 64))
            add("wrong V004 binding", lambda value: value.__setitem__("target_v004_sha256", "0" * 64))
            add("nested history surplus", lambda value: value["histories"][0].__setitem__("surplus", 1))
            add(
                "noncanonical history path",
                lambda value: value["histories"][0].__setitem__(
                    "path",
                    (
                        "/synthetic/../HISTORY.json" if synthetic
                        else "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                             "PHYSICAL_OUTPUTS/../HISTORY.json"
                    ),
                ),
            )
        elif artifact_id in {
            "A12_CONTROL_STAGE_AUDIT", "A16_L10_STAGE_AUDIT",
        }:
            def fabricated_checks(value: dict[str, object]) -> None:
                value["checks"] = {"fabricated_positive": 1}
                value["checks_total"] = 1
                value["checks_passed"] = 1
            add("fabricated positive check map", fabricated_checks)
        elif artifact_id == "A13_L10_AUTHORIZATION":
            add("authorized length 11", lambda value: value.__setitem__("authorized_length", 11))
            add("boolean authorized length", lambda value: value.__setitem__("authorized_length", True))
            add("float authorized length", lambda value: value.__setitem__("authorized_length", 10.0))
        elif artifact_id == "A14_L10_HISTORY":
            add("event row surplus", lambda value: value["rows"][0].__setitem__("surplus", 1))
            add("comparison surplus", lambda value: value["comparison"].__setitem__("surplus", 1))
            add("resource surplus", lambda value: value["resource"].__setitem__("surplus", 1))
            add("terminal shard surplus", lambda value: value["terminal_shards"][0].__setitem__("surplus", 1))
            add(
                "canonical V004 numeric mismatch",
                lambda value: value["rows"][0].__setitem__(
                    "allow_probability", value["rows"][0]["allow_probability"] + 0.001,
                ),
            )
        return cases

    positive_calls = 0
    adverse_calls = 0
    for artifact_id in artifact_ids:
        production_record = obligation_validators.positive_fixture(artifact_id)
        independent_record = independent[(artifact_id, 1)]
        obligation_validators.validate_record(
            artifact_id, production_record,
            mutation_class="A11_A16_PARITY_POSITIVE", fixture_mode=True,
        )
        final_auditor._validate_independent_upstream_record(
            artifact_id, independent_record, "A26_FINAL_L12_AUDIT",
            fixture_mode=True,
        )
        check(
            set(production_record) == set(independent_record),
            f"{artifact_id} production/A26 positive keyset mismatch",
        )
        production[artifact_id] = production_record
        independent_records[artifact_id] = independent_record
        positive_calls += 2
        for _label, candidate in adverse_records(
            artifact_id, production_record, synthetic=True,
        ):
            try:
                obligation_validators.validate_record(
                    artifact_id, candidate,
                    mutation_class="A11_A16_PARITY_ADVERSE", fixture_mode=True,
                )
            except obligation_validators.Refusal:
                adverse_calls += 1
            else:
                raise Failure(f"{artifact_id} production parity mutation accepted")
        for _label, candidate in adverse_records(
            artifact_id, independent_record, synthetic=True,
        ):
            try:
                final_auditor._validate_independent_upstream_record(
                    artifact_id, candidate, "A26_FINAL_L12_AUDIT",
                    fixture_mode=True,
                )
            except final_auditor.Refusal:
                adverse_calls += 1
            else:
                raise Failure(f"{artifact_id} A26 parity mutation accepted")

    exact_checks = {
        "A12_CONTROL_STAGE_AUDIT": {
            "stage_gate_exact_schema": 1, "history_records": 3,
            "canonical_v004_projection_records": 3,
            "terminal_shard_records": 18, "stable_descriptor_records": 22,
        },
        "A16_L10_STAGE_AUDIT": {
            "stage_gate_exact_schema": 1, "history_records": 1,
            "canonical_v004_projection_records": 1,
            "terminal_shard_records": 10, "stable_descriptor_records": 12,
        },
    }
    for artifact_id, expected in exact_checks.items():
        check(
            production[artifact_id]["checks"] == expected
            and independent_records[artifact_id]["checks"] == expected,
            f"{artifact_id} positive check-map parity mismatch",
        )
    for artifact_id, lengths in {
        "A11_CONTROL_STAGE_GATE": (4, 6, 8),
        "A15_L10_STAGE_GATE": (10,),
    }.items():
        expected_paths = [f"/synthetic/HISTORY_L{length}.json" for length in lengths]
        check(
            [row["path"] for row in production[artifact_id]["histories"]]
            == expected_paths
            == [row["path"] for row in independent_records[artifact_id]["histories"]],
            f"{artifact_id} fixture path parity mismatch",
        )

    # The direct consumer has a production-only path contract.  Exercise its
    # exact record predicates with temporary canonical paths and strict spies
    # for already-covered predecessor I/O.  No history solver is launched.
    with tempfile.TemporaryDirectory(
        prefix="target_v012_a11_a16_parity_"
    ) as directory:
        root = Path(directory).resolve()
        here = root / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        physical_output = here / "PHYSICAL_OUTPUTS"
        workspace = here / "WORKSPACES"
        audit_root = root / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
        here.mkdir(parents=True)
        physical_output.mkdir()
        workspace.mkdir()
        audit_root.mkdir()
        paths = {
            "freeze": here / "FREEZE.json",
            "preflight_result": here / "PREFLIGHT_RESULT_V001.json",
            "dual": here / "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
            "a11": here / "CACHED_CONTROL_L4_L8_GATE_V012.json",
            "a12": audit_root / "CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
            "a13": here / "L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
            "a14": physical_output / "HISTORY_L10.json",
            "a15": here / "CACHED_L10_GATE_V012.json",
            "a16": audit_root / "CACHED_L10_GATE_AUDIT_V001.json",
        }
        for path in paths.values():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"{}\n")
            path.chmod(0o444)

        direct = {
            artifact_id: copy.deepcopy(independent_records[artifact_id])
            for artifact_id in artifact_ids
        }
        live_inherited = {
            "original_target_l12_gate_sha256": builder.TARGET_L12_GATE_V004_SHA256,
            "preserved_workspace_custody_sha256": builder.PRESERVED_WORKSPACE_CUSTODY_SHA256,
            "preserved_workspace_cross_diagnostic_sha256": builder.PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
            "runtime_compatibility_obstruction_sha256": builder.RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
            "v006_hostile_audit_obstruction_sha256": builder.V006_HOSTILE_OBSTRUCTION_SHA256,
            "v007_runtime_compatibility_obstruction_sha256": builder.V007_RUNTIME_OBSTRUCTION_SHA256,
            "v008_postbuild_audit_binding_obstruction_sha256": builder.V008_BINDING_OBSTRUCTION_SHA256,
            "v009_hostile_audit_obstruction_sha256": builder.V009_HOSTILE_OBSTRUCTION_SHA256,
            "v010_hostile_audit_obstruction_sha256": builder.V010_HOSTILE_OBSTRUCTION_SHA256,
            "v010_audit_record_custody_correction_sha256": builder.V010_CUSTODY_CORRECTION_SHA256,
            "v011_hostile_audit_obstruction_sha256": builder.V011_HOSTILE_OBSTRUCTION_SHA256,
            "target_v004_sha256": builder.TARGET_V004_SHA256,
        }
        for artifact_id in (
            "A11_CONTROL_STAGE_GATE", "A14_L10_HISTORY",
            "A15_L10_STAGE_GATE",
        ):
            direct[artifact_id].update(live_inherited)
        source_gate = direct["A11_CONTROL_STAGE_GATE"]
        frozen_files = {
            "consume_target_cache.py": source_gate["consumer_sha256"],
            "build_target_cache.py": source_gate["builder_sha256"],
            "validate_preflight.py": source_gate["preflight_sha256"],
            "METHOD.md": source_gate["method_sha256"],
            "production_obligation_validators.py": direct[
                "A14_L10_HISTORY"
            ]["production_obligation_validators_sha256"],
        }
        freeze = {"files": frozen_files}
        physical_sha = source_gate["physical_execution_gate_sha256"]
        freeze_sha = source_gate["freeze_sha256"]
        preflight_result_sha = source_gate["preflight_result_sha256"]
        independent_audit_sha = source_gate["independent_hostile_audit_sha256"]
        dual_sha = direct["A14_L10_HISTORY"]["dual_obstruction_gate_sha256"]

        for artifact_id, lengths in {
            "A11_CONTROL_STAGE_GATE": (4, 6, 8),
            "A15_L10_STAGE_GATE": (10,),
        }.items():
            for row, length in zip(direct[artifact_id]["histories"], lengths):
                row["path"] = (
                    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                    f"PHYSICAL_OUTPUTS/HISTORY_L{length}.json"
                )
        direct_sha = lambda value: hashlib.sha256(canonical_json_bytes(value)).hexdigest()
        a11_sha = direct_sha(direct["A11_CONTROL_STAGE_GATE"])
        direct["A12_CONTROL_STAGE_AUDIT"].update({
            "stage_gate_sha256": a11_sha,
            "history_sha256_by_L": {
                str(row["L"]): row["sha256"]
                for row in direct["A11_CONTROL_STAGE_GATE"]["histories"]
            },
        })
        a12_sha = direct_sha(direct["A12_CONTROL_STAGE_AUDIT"])
        direct["A13_L10_AUTHORIZATION"].update({
            "physical_execution_gate_sha256": physical_sha,
            "cached_control_l4_l8_gate_sha256": a11_sha,
            "cached_control_l4_l8_gate_audit_sha256": a12_sha,
            "l10_cache_manifest_sha256": direct[
                "A15_L10_STAGE_GATE"
            ]["cache_manifest_sha256_by_L"]["10"],
        })
        a13_sha = direct_sha(direct["A13_L10_AUTHORIZATION"])
        a14 = direct["A14_L10_HISTORY"]
        a14.update({
            "cache_manifest_sha256": direct[
                "A15_L10_STAGE_GATE"
            ]["cache_manifest_sha256_by_L"]["10"],
            "physical_execution_gate_sha256": physical_sha,
            "cached_control_l4_l8_gate_sha256": a11_sha,
            "cached_control_l4_l8_gate_audit_sha256": a12_sha,
            "execution_authorization_sha256": a13_sha,
            "l10_execution_authorization_gate_sha256": a13_sha,
            "promotion_audit_sha256": a12_sha,
            "consumer_sha256": frozen_files["consume_target_cache.py"],
            "builder_sha256": frozen_files["build_target_cache.py"],
            "method_sha256": frozen_files["METHOD.md"],
            "production_obligation_validators_sha256": frozen_files[
                "production_obligation_validators.py"
            ],
            "freeze_sha256": freeze_sha,
            "preflight_result_sha256": preflight_result_sha,
            "independent_hostile_audit_sha256": independent_audit_sha,
            "dual_obstruction_gate_sha256": dual_sha,
            "target_v004_sha256": builder.TARGET_V004_SHA256,
        })
        shard_digest_by_fd: dict[int, str] = {}
        shard_digest_by_path: dict[Path, str] = {}
        for item in a14["terminal_shards"]:
            shard = (
                workspace / "L10/sharp/prefix_09"
                / f"q_{item['q']:02d}.npy"
            )
            shard.parent.mkdir(parents=True, exist_ok=True)
            with shard.open("wb") as stream:
                stream.truncate(item["bytes"])
            shard.chmod(0o444)
            item["path"] = str(shard)
            shard_digest_by_path[shard] = item["sha256"]
        a14_sha = direct_sha(a14)
        direct["A15_L10_STAGE_GATE"].update({
            "physical_execution_gate_sha256": physical_sha,
            "cached_control_l4_l8_gate_sha256": a11_sha,
            "l10_execution_authorization_gate_sha256": a13_sha,
        })
        direct["A15_L10_STAGE_GATE"]["histories"][0]["sha256"] = a14_sha
        a15_sha = direct_sha(direct["A15_L10_STAGE_GATE"])
        direct["A16_L10_STAGE_AUDIT"].update({
            "stage_gate_sha256": a15_sha,
            "history_sha256_by_L": {"10": a14_sha},
            "l10_execution_authorization_gate_sha256": a13_sha,
        })

        hash_by_path = {
            paths["freeze"]: freeze_sha,
            paths["preflight_result"]: preflight_result_sha,
            paths["dual"]: dual_sha,
            paths["a11"]: a11_sha,
            paths["a12"]: a12_sha,
            paths["a13"]: a13_sha,
            paths["a14"]: a14_sha,
            paths["a15"]: a15_sha,
        }
        active_records: dict[Path, dict[str, object]] = {}
        original_consumer = {
            name: getattr(consumer, name) for name in (
                "HERE", "ROOT", "FREEZE", "PHYSICAL_OUTPUT_PARENT",
                "WORKSPACE_PARENT", "CACHED_CONTROL_GATE",
                "CACHED_CONTROL_GATE_AUDIT", "L10_EXECUTION_AUTHORIZATION_GATE",
                "CACHED_L10_GATE", "CACHED_L10_GATE_AUDIT", "immutable_json",
                "sha256", "validate_prior_history", "open_stable_readonly",
                "descriptor_sha256",
            )
        }
        original_builder_dual = builder.DUAL_GATE
        original_safe_repo_file = builder.safe_repo_file
        original_production_obligation = builder.validate_production_obligation
        original_immutable_json = consumer.immutable_json
        original_open_stable = consumer.open_stable_readonly
        canonical_reference, canonical_reference_sha = original_immutable_json(
            consumer.CANONICAL_V004_HISTORY_PATH[10],
            "A11--A16 canonical V004 L10 fixture", None, False,
        )

        def fake_sha256(path: Path) -> str:
            resolved = Path(path)
            if resolved in hash_by_path:
                return hash_by_path[resolved]
            return original_consumer["sha256"](resolved)

        def fake_immutable_json(
            path: Path, label: str, expected_sha256: str | None = None,
            require_immutable_mode: bool = True,
        ) -> tuple[dict[str, object], str]:
            candidate = Path(path)
            if candidate in active_records:
                value = copy.deepcopy(active_records[candidate])
                digest = direct_sha(value)
                if expected_sha256 is not None and expected_sha256 != digest:
                    raise consumer.Refusal(f"{label} hash mismatch")
                return value, digest
            if candidate == paths["dual"]:
                return {
                    "independent_hostile_audit": {
                        "sha256": independent_audit_sha,
                    },
                }, dual_sha
            if candidate == consumer.CANONICAL_V004_HISTORY_PATH[10]:
                return copy.deepcopy(canonical_reference), canonical_reference_sha
            return original_immutable_json(
                candidate, label, expected_sha256, require_immutable_mode,
            )

        expected_history_hashes = {
            row["L"]: row["sha256"]
            for artifact_id in (
                "A11_CONTROL_STAGE_GATE", "A15_L10_STAGE_GATE",
            )
            for row in direct[artifact_id]["histories"]
        }

        def strict_history_spy(
            row: object, length: int, cache_sha: str,
            gate_sha: str, freeze_record: dict[str, object],
        ) -> dict[str, object]:
            expected_path = (
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                f"PHYSICAL_OUTPUTS/HISTORY_L{length}.json"
            )
            if (
                type(row) is not dict
                or set(row) != {"L", "path", "sha256"}
                or row.get("L") != length
                or row.get("path") != expected_path
                or row.get("sha256") != expected_history_hashes[length]
                or gate_sha != physical_sha
                or freeze_record is not freeze
                or cache_sha != direct[
                    "A11_CONTROL_STAGE_GATE" if length < 10
                    else "A15_L10_STAGE_GATE"
                ]["cache_manifest_sha256_by_L"][str(length)]
            ):
                raise consumer.Refusal("strict predecessor history mismatch")
            return {}

        def fake_safe_repo_file(
            relative: object, expected_sha: object, label: str,
        ) -> Path:
            if (
                relative
                != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                   "PHYSICAL_OUTPUTS/HISTORY_L10.json"
                or expected_sha != direct_sha(active_records[paths["a14"]])
            ):
                raise builder.Refusal(f"{label} path/hash mismatch")
            return paths["a14"]

        def fake_open_stable(path: Path) -> int:
            descriptor = original_open_stable(path)
            shard_digest_by_fd[descriptor] = shard_digest_by_path[Path(path)]
            return descriptor

        def fake_descriptor_sha256(descriptor: int) -> str:
            if descriptor in shard_digest_by_fd:
                return shard_digest_by_fd.pop(descriptor)
            return original_consumer["descriptor_sha256"](descriptor)

        try:
            consumer.HERE = here
            consumer.ROOT = root
            consumer.FREEZE = paths["freeze"]
            consumer.PHYSICAL_OUTPUT_PARENT = physical_output
            consumer.WORKSPACE_PARENT = workspace
            consumer.CACHED_CONTROL_GATE = paths["a11"]
            consumer.CACHED_CONTROL_GATE_AUDIT = paths["a12"]
            consumer.L10_EXECUTION_AUTHORIZATION_GATE = paths["a13"]
            consumer.CACHED_L10_GATE = paths["a15"]
            consumer.CACHED_L10_GATE_AUDIT = paths["a16"]
            consumer.immutable_json = fake_immutable_json
            consumer.sha256 = fake_sha256
            consumer.validate_prior_history = strict_history_spy
            consumer.open_stable_readonly = fake_open_stable
            consumer.descriptor_sha256 = fake_descriptor_sha256
            builder.DUAL_GATE = paths["dual"]
            builder.safe_repo_file = fake_safe_repo_file
            builder.validate_production_obligation = lambda artifact_id, value: None

            def direct_call(artifact_id: str, record: dict[str, object]) -> None:
                active_records.clear()
                base = direct[artifact_id]
                if artifact_id == "A11_CONTROL_STAGE_GATE":
                    active_records[paths["a11"]] = record
                    consumer.require_stage_gate(
                        paths["a11"], base["schema"], base["classification"],
                        (4, 6, 8), base["cache_manifest_sha256_by_L"],
                        physical_sha, freeze,
                    )
                elif artifact_id == "A12_CONTROL_STAGE_AUDIT":
                    active_records[paths["a12"]] = record
                    consumer.require_stage_gate_audit(
                        paths["a12"], paths["a11"],
                        direct["A11_CONTROL_STAGE_GATE"], base["schema"],
                        base["classification"], (4, 6, 8),
                    )
                elif artifact_id == "A13_L10_AUTHORIZATION":
                    active_records[paths["a13"]] = record
                    consumer.require_l10_execution_authorization(
                        freeze, physical_sha,
                        {"10": base["l10_cache_manifest_sha256"]},
                        direct["A11_CONTROL_STAGE_GATE"], a12_sha,
                    )
                elif artifact_id == "A14_L10_HISTORY":
                    active_records[paths["a14"]] = record
                    consumer.validate_prior_history = original_consumer[
                        "validate_prior_history"
                    ]
                    try:
                        row = {
                            "L": 10,
                            "path": (
                                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                                "PHYSICAL_OUTPUTS/HISTORY_L10.json"
                            ),
                            "sha256": direct_sha(record),
                        }
                        consumer.validate_prior_history(
                            row, 10, base["cache_manifest_sha256"],
                            physical_sha, freeze,
                        )
                    finally:
                        consumer.validate_prior_history = strict_history_spy
                elif artifact_id == "A15_L10_STAGE_GATE":
                    active_records[paths["a15"]] = record
                    consumer.require_stage_gate(
                        paths["a15"], base["schema"], base["classification"],
                        (10,), base["cache_manifest_sha256_by_L"],
                        physical_sha, freeze, a11_sha, a13_sha,
                    )
                else:
                    active_records[paths["a16"]] = record
                    consumer.require_stage_gate_audit(
                        paths["a16"], paths["a15"],
                        direct["A15_L10_STAGE_GATE"], base["schema"],
                        base["classification"], (10,), a13_sha,
                    )

            for artifact_id in artifact_ids:
                direct_call(artifact_id, direct[artifact_id])
                positive_calls += 1
                for _label, candidate in adverse_records(
                    artifact_id, direct[artifact_id], synthetic=False,
                ):
                    try:
                        direct_call(artifact_id, candidate)
                    except (builder.Refusal, consumer.Refusal):
                        adverse_calls += 1
                    else:
                        raise Failure(
                            f"{artifact_id} direct-consumer parity mutation accepted"
                        )
        finally:
            for name, value in original_consumer.items():
                setattr(consumer, name, value)
            builder.DUAL_GATE = original_builder_dual
            builder.safe_repo_file = original_safe_repo_file
            builder.validate_production_obligation = original_production_obligation

    check(positive_calls == 18, "A11--A16 positive sink-call census mismatch")
    check(adverse_calls == 66, "A11--A16 adverse sink-call census mismatch")
    return {
        "positive_sink_calls": positive_calls,
        "adverse_sink_calls": adverse_calls,
    }


def validate_syntax_and_static_locks() -> int:
    for name in (
        "build_target_cache.py", "consume_target_cache.py",
        "production_obligation_validators.py", "validate_preflight.py",
    ):
        ast.parse((HERE / name).read_text(encoding="utf-8"), filename=name)
    builder_source = (HERE / "build_target_cache.py").read_text(encoding="utf-8")
    consumer_source = (HERE / "consume_target_cache.py").read_text(encoding="utf-8")
    preflight_source = (HERE / "validate_preflight.py").read_text(encoding="utf-8")
    build_source = builder_source.split("def build(", 1)[1]
    builder_publication_source = builder_source.split(
        "def atomic_publish_json(", 1
    )[1].split("def exact_int(", 1)[0]
    builder_mutation_ledger_source = builder_source.split(
        "def require_preflight_mutation_ledger(", 1
    )[1].split("def require_future_v012_hostile_audit(", 1)[0]
    retained_custody_source = builder_source.split(
        "class StableAuthorityCustody:", 1
    )[1].split("AUTHORITY_CUSTODY:", 1)[0]
    physical_gate_source = consumer_source.split("def require_physical_gate(", 1)[1].split("def existing_parent(", 1)[0]
    l10_cross_source = consumer_source.split(
        "def require_target_hostile_l10_cross_gate(", 1
    )[1].split("def require_parallel_l12_schedule_gate(", 1)[0]
    parallel_schedule_source = consumer_source.split(
        "def require_parallel_l12_schedule_gate(", 1
    )[1].split("def require_shared_schedule_audit(", 1)[0]
    execute_source = consumer_source.split(
        "def _execute_with_retained_authority(", 1
    )[1].split("def execute(", 1)[0]
    worker_session_source = consumer_source.split(
        "class OrchestratedWorkerSession:", 1
    )[1].split("\ndef sha256(", 1)[0]
    worker_completion_source = worker_session_source.split(
        "def complete(self, output_sha256: str)", 1
    )[1].split("def close(self)", 1)[0]
    publication_source = preflight_source.split(
        "def atomic_publish_immutable_json(", 1
    )[1].split("def validate_held_descriptor_identity(", 1)[0]
    preflight_main_source = preflight_source.split("\ndef main() -> int:\n", 1)[1]
    check(build_source.index("require_original_target_gate()") < build_source.index("require_dual_gate(length)"), "builder original-gate order")
    check(
        build_source.index("require_dual_gate(length)")
        < build_source.index("open_cache_output_roots(output)"),
        "builder dual-gate order",
    )
    check(execute_source.index("require_physical_gate(length, cache_manifest_sha256)") < execute_source.index("CacheContext(cache_root"), "consumer gate/cache order")
    check(execute_source.index("require_physical_gate(length, cache_manifest_sha256)") < execute_source.index("workspace.mkdir"), "consumer gate/workspace order")
    check(physical_gate_source.count("require_stage_gate(") == 2, "staged cached gate calls")
    check(physical_gate_source.count("require_parallel_l12_schedule_gate(") == 1,
          "parallel L12 schedule gate call")
    check(physical_gate_source.count("require_shared_schedule_audit(") == 1,
          "parallel L12 schedule audit call")
    check(physical_gate_source.count("require_target_l12_execution_gate(") == 1,
          "target L12 one-way authorization call")
    check(physical_gate_source.count("require_hostile_l12_execution_gate(") == 1,
          "hostile L12 one-way authorization call")
    check(physical_gate_source.count("require_dual_l12_launch_handshake(") == 1,
          "dual L12 blocked-worker handshake call")
    check(physical_gate_source.count("require_dual_l12_worker_release(") == 1,
          "dual L12 worker-release call")
    schedule_position = physical_gate_source.index(
        "require_parallel_l12_schedule_gate("
    )
    audit_position = physical_gate_source.index("require_shared_schedule_audit(")
    target_authorization_position = physical_gate_source.index(
        "require_target_l12_execution_gate("
    )
    hostile_authorization_position = physical_gate_source.index(
        "require_hostile_l12_execution_gate("
    )
    handshake_position = physical_gate_source.index(
        "require_dual_l12_launch_handshake("
    )
    release_position = physical_gate_source.index(
        "require_dual_l12_worker_release("
    )
    check(schedule_position < audit_position,
          "readiness schedule/audit order")
    check(audit_position < target_authorization_position < handshake_position,
          "target authorization/handshake order")
    check(audit_position < hostile_authorization_position < handshake_position,
          "hostile authorization/handshake order")
    check(handshake_position < release_position,
          "blocked-worker handshake/release order")
    check("launch_handshake" not in parallel_schedule_source,
          "readiness schedule embeds a launch handshake")
    check("V012_DUAL_L12_READINESS_SCHEDULE_V001" in parallel_schedule_source,
          "readiness schedule schema absent")
    check(physical_gate_source.count("require_stage_gate_audit(") == 2,
          "stage-gate hostile audit calls")
    check(physical_gate_source.count("require_l10_execution_authorization(") == 1,
          "L10 outer authorization call")
    check(physical_gate_source.count("require_postbuild_payload_audit(") == 1,
          "postbuild payload audit gate call")
    check(physical_gate_source.count("require_control_execution_authorization(") == 1,
          "independent physical-gate audit authorization call")
    check(physical_gate_source.index("require_postbuild_payload_audit(")
          < physical_gate_source.index("require_control_execution_authorization("),
          "postbuild/gate-audit authorization order")
    check("audit.get(\"checks\") != expected_checks" in consumer_source,
          "postbuild audit exact check census absent")
    check("sum(audit[\"checks\"].values()) != audit[\"checks_total\"]" in consumer_source,
          "postbuild audit check total is not reconstructed")
    check("type(value) is not int or value <= 0" in consumer_source,
          "postbuild audit exact positive-integer type checks absent")
    check("set(gate) != BASE_PHYSICAL_GATE_KEYS" in physical_gate_source,
          "base physical gate exact key census absent")
    check("base_gate_exact_key_census_passed" in consumer_source,
          "physical-gate audit exact-census assertion absent")
    check("BASE_PHYSICAL_GATE_KEY_CENSUS_SHA256" in consumer_source,
          "physical-gate audit exact-census digest absent")
    check("def immutable_json(" in builder_source and "def immutable_json(" in consumer_source,
          "stable immutable JSON readers absent")
    check("object_pairs_hook=exact_object" in builder_source + consumer_source,
          "duplicate-key refusal absent")
    check("parse_constant=reject_constant" in builder_source + consumer_source,
          "nonfinite JSON refusal absent")
    check("getattr(os, \"O_NOFOLLOW\"" in builder_source + consumer_source,
          "no-follow descriptor opening absent")
    check(retained_custody_source.count("self._require_canonical_path(key, label)") >= 3
          and "absolute.resolve(strict=False)" in retained_custody_source,
          "retained authority permits a symlinked parent alias")
    check("dir_fd=parent_descriptor" in publication_source
          and "getattr(os, \"O_DIRECTORY\"" in publication_source,
          "preflight held-parent staging publication absent")
    check("os.fsync(descriptor)" in publication_source
          and "os.fchmod(descriptor, 0o444)" in publication_source,
          "preflight durable immutable staging absent")
    check("src_dir_fd=parent_descriptor" in publication_source
          and "dst_dir_fd=parent_descriptor" in publication_source,
          "preflight held-parent atomic no-clobber commit absent")
    check("if not _unlink_staging_if_owned_at(" in publication_source
          and "os.unlink(temporary" not in publication_source,
          "preflight staging cleanup is not held-inode constrained")
    check("staged.st_nlink != 1" in publication_source
          and "linked_canonical.st_nlink != 2" in publication_source
          and "canonical.st_nlink != 1" in publication_source
          and "parent_after.st_ino" in publication_source,
          "preflight publication link/parent custody is incomplete")
    check("if not _unlink_if_owned_at(" in builder_publication_source
          and "os.unlink(temporary" not in builder_publication_source
          and "_unlink_if_owned_at(\n                    parent_descriptor, path.name" not in builder_publication_source,
          "builder publication can delete unowned staging or canonical evidence")
    check("src_dir_fd=parent_descriptor" in builder_publication_source
          and "dst_dir_fd=parent_descriptor" in builder_publication_source
          and "dir_fd=parent_descriptor" in builder_publication_source,
          "builder publication is not held-parent descriptor relative")
    check("before.st_nlink != 1" in builder_publication_source
          and "observed.st_nlink != 2" in builder_publication_source
          and "canonical_after.st_nlink != 1" in builder_publication_source
          and "parent_after.st_ino" in builder_publication_source,
          "builder publication link/parent custody is incomplete")
    check("_unlink_if_owned(manifest_path" not in build_source
          and "no later failure deletes it" in build_source,
          "builder can erase a canonical manifest after publication")
    check("positive_fixture_variants" in builder_mutation_ledger_source
          and "mutation_fixture_by_class" in builder_mutation_ledger_source
          and '"positive_sink_call_count": 33' in builder_mutation_ledger_source
          and "a22_hook_by_fixture" in builder_mutation_ledger_source
          and '"M25_IMPORT_TARGET_VALIDATOR": "validate_preflight.validate_independent_auditor_source_bytes"'
          in builder_mutation_ledger_source
          and "exact_refusal_match(" in builder_mutation_ledger_source,
          "builder mutation-ledger reconstruction omits expanded stateful evidence")
    check("os.fsync(parent_descriptor)" in publication_source
          and "descriptor_bytes(canonical_descriptor)" in publication_source
          and "descriptor_digest(canonical_descriptor)" in publication_source,
          "preflight postcommit custody authentication absent")
    check(preflight_main_source.count("atomic_publish_immutable_json(") == 2,
          "preflight evidence does not use exactly two atomic publications")
    check(preflight_main_source.count("validate_dependencies()") == 3,
          "preflight dependencies are not reauthenticated around publication")
    check("os.open(RESULT, os.O_WRONLY" not in preflight_main_source,
          "legacy direct result publication remains")
    check("(4, 6, 8)" in physical_gate_source and "(10,)" in physical_gate_source, "staged cached gate sizes")
    check("authorized != list(builder.SUPPORTED)" in physical_gate_source,
          "base physical gate does not bind all five manifests")
    check("validate_prior_history(row" in consumer_source,
          "prior-history reconstruction absent")
    check("seal_terminal_shards(length" in execute_source,
          "terminal-shard immutable sealing absent")
    check("expected_peak_state" in consumer_source and "expected_workset" in consumer_source,
          "history resource reconstruction absent")
    check("len(target_paths) != 9" in l10_cross_source
          and "len(hostile_paths) != 9" in l10_cross_source,
          "L10 cross gate does not attest exactly nine roles per branch")
    check("snapshot.get(\"memory_pressure\") != \"NORMAL\"" in parallel_schedule_source,
          "NORMAL memory-pressure gate absent")
    check("observed_launch_skew_seconds" in consumer_source,
          "launch-handshake skew verification absent")
    check(execute_source.index("context.reauthenticate()") < execute_source.index("resource_pass ="), "post-history cache reauthentication")
    check(execute_source.index("if not resource_pass:") < execute_source.index("result = {"), "resource refusal before result")
    check(execute_source.index("comparison.get(\"resolved\") is not True") < execute_source.index("result = {"), "numerical refusal before result")
    check(
        execute_source.index("project_native_method_record(")
        < execute_source.index("result = {")
        and execute_source.index("project_native_history_rows(")
        < execute_source.index("result = {"),
        "fixed-field native history projection is not prepublication",
    )
    check(execute_source.index("result = {")
          < execute_source.index("builder.atomic_publish_json("),
          "result publication order")
    completion_position = execute_source.index(
        "ORCHESTRATED_SESSION.complete(published_sha256)"
    )
    check(execute_source.index("builder.atomic_publish_json(")
          < completion_position < execute_source.index("print(comparison"),
          "L12 terminal-live completion order")
    check("if length == 12:" in execute_source[:completion_position]
          and "V012_L12_WORKER_COMPLETION_V001" in consumer_source
          and "self.channel.shutdown(socket.SHUT_WR)" in worker_session_source
          and "trailing = self.channel.recv(1)" in worker_session_source
          and "if trailing:" in worker_session_source,
          "L12 worker completion/EOF custody protocol absent")
    check(worker_completion_source.index(
              'builder.validate_production_obligation(\n                "A22_TARGET_L12_AUTHORIZATION", completion,'
          ) < worker_completion_source.index("self.channel.sendall(wire)")
          < worker_completion_source.index("self.channel.shutdown(socket.SHUT_WR)"),
          "L12 completion bypasses the production sink or one-way close order")
    check(worker_completion_source.index("digest = descriptor_sha256(descriptor)")
          < worker_completion_source.index("completion = {")
          and worker_completion_source.index("if trailing:")
          < worker_completion_source.rindex("final_digest = descriptor_sha256(descriptor)"),
          "L12 completion output custody is not authenticated before send and after EOF")
    check("os.fdopen(os.dup(descriptor), \"rb\")" in consumer_source, "stable descriptor-backed memmap")
    check("if math.prod(shape) == 0:" in consumer_source, "zero-length cache compatibility branch absent")
    check("return np.empty(shape, dtype=dtype)" in consumer_source, "zero-length cache return absent")
    check(
        "self.directory_identity[6] & 0o222" in consumer_source,
        "read-only canonical cache root",
    )
    check("descriptor_sha256(descriptor)" in consumer_source, "stable descriptor reauthentication")
    check(".stat(follow_symlinks=False)" not in consumer_source, "unsupported pathlib stat keyword remains")
    check(consumer_source.count("os.stat(") >= 4, "portable os.stat custody calls absent")
    check("import independent_prefix_history_v004" not in builder_source + consumer_source, "hostile payload import")
    exact_type_guards = (
        "type(audit.get(\"checks_passed\")) is not int",
        "type(audit.get(\"checks_total\")) is not int",
        "type(value) is not bool or value is not False",
        "type(audit[\"payload_census_by_L\"][str(L)][field]) is not int",
        "type(audit[\"semantic_cachecontext\"][\"L4\"][\"descriptor_count\"]) is not int",
        "any(type(value) is not int for value in gate.get(\"authorized_lengths\", []))",
    )
    for guard in exact_type_guards:
        check(guard in builder_source + consumer_source,
              f"V011 exact-type repair absent: {guard}")
    validate_history_serialization_projection_regression()
    validate_a11_a16_three_sink_parity_regression()
    validate_retained_custody_parent_alias_rejection()
    validate_atomic_publication_parent_alias_rejection()
    return len(exact_type_guards)


def validate_retained_custody_parent_alias_rejection() -> None:
    """Exercise both initial and post-authentication parent-symlink attacks."""
    with tempfile.TemporaryDirectory(
        prefix="target_v012_parent_alias_custody_"
    ) as directory:
        # The platform scratch root may itself be reached through `/var` ->
        # `/private/var`; use its canonical spelling so the control isolates
        # only the alias introduced below.
        root = Path(directory).resolve()
        canonical_parent = root / "authority"
        canonical_parent.mkdir(mode=0o700)
        authority = canonical_parent / "record.json"
        authority.write_bytes(b"{}\n")
        authority.chmod(0o444)

        initial_alias = root / "initial-alias"
        initial_alias.symlink_to(canonical_parent.name, target_is_directory=True)
        initial_custody = builder.StableAuthorityCustody()
        try:
            expect_refusal(
                lambda: initial_custody.authenticate(
                    initial_alias / authority.name,
                    "initial parent-symlink authority", None, True,
                ),
                "path traverses a symlink alias",
                "initial parent-symlink alias entered retained custody",
            )
        finally:
            initial_custody.close()

        insertion_custody = builder.StableAuthorityCustody()
        canonical_path_check = insertion_custody._require_canonical_path
        call_count = 0

        def inject_post_open_alias_refusal(key: str, label: str) -> None:
            nonlocal call_count
            call_count += 1
            canonical_path_check(key, label)
            if call_count == 2:
                raise builder.Refusal(
                    f"{label} path traverses a symlink alias"
                )

        insertion_custody._require_canonical_path = inject_post_open_alias_refusal
        try:
            expect_refusal(
                lambda: insertion_custody.authenticate(
                    authority, "concurrent parent-symlink authority", None, True,
                ),
                "path traverses a symlink alias",
                "concurrent parent-symlink alias entered retained custody",
            )
            check(
                not insertion_custody._entries,
                "failed authentication retained a closed custody descriptor",
            )
        finally:
            insertion_custody.close()

        retained_custody = builder.StableAuthorityCustody()
        retained_custody.authenticate(
            authority, "retained parent-symlink authority", None, True,
        )
        renamed_parent = root / "authority-held"
        canonical_parent.rename(renamed_parent)
        canonical_parent.symlink_to(renamed_parent.name, target_is_directory=True)
        try:
            expect_refusal(
                lambda: retained_custody.verify_one(
                    authority, "retained parent-symlink authority",
                ),
                "path traverses a symlink alias",
                "post-authentication parent-symlink alias retained authority",
            )
        finally:
            retained_custody.close()


def validate_atomic_publication_parent_alias_rejection() -> None:
    """Prove both target publishers stay bound to a held parent directory."""
    publishers = (
        (
            "builder",
            lambda path: builder.atomic_publish_json(
                path, {"probe": "builder"}, "builder alias regression",
                builder.StableAuthorityCustody(),
            ),
            (builder.Refusal,),
        ),
        (
            "preflight",
            lambda path: atomic_publish_immutable_json(
                path, {"probe": "preflight"}, "preflight alias regression",
            ),
            (Failure, builder.Refusal),
        ),
    )
    for publisher_name, publish, refusal_types in publishers:
        with tempfile.TemporaryDirectory(
            prefix=f"target_v012_{publisher_name}_parent_alias_",
            dir="/private/tmp",
        ) as directory:
            root = Path(directory)
            parent = root / "authority"
            parent.mkdir(mode=0o700)
            moved = root / "moved-authority"
            destination = parent / "record.json"
            original_link = os.link
            attacked = False

            def alias_before_link(source, target, *args, **kwargs):
                nonlocal attacked
                if not attacked:
                    parent.rename(moved)
                    parent.symlink_to(moved, target_is_directory=True)
                    attacked = True
                return original_link(source, target, *args, **kwargs)

            os.link = alias_before_link
            try:
                try:
                    publish(destination)
                except refusal_types:
                    pass
                else:
                    raise Failure(
                        f"{publisher_name} parent-alias publication accepted"
                    )
            finally:
                os.link = original_link
            check(attacked, f"{publisher_name} parent-alias injection absent")
            evidence = moved / destination.name
            check(
                evidence.is_file()
                and evidence.stat().st_mode & 0o222 == 0
                and evidence.stat().st_nlink == 1,
                f"{publisher_name} parent-alias evidence not preserved",
            )


def validate_hostile_raw_c128_resource_identity(resource: object) -> None:
    required = {
        "hostile_scratch_minimum_bytes",
        "hostile_peak_live_raw_c128_shard_count",
        "hostile_container_header_bytes",
    }
    if not isinstance(resource, dict) or set(resource) != required:
        raise Failure("hostile raw-c128 resource census mismatch")
    if (
        type(resource["hostile_container_header_bytes"]) is not int
        or resource["hostile_container_header_bytes"] != 0
    ):
        raise Failure("hostile raw-c128 header mismatch")
    if (
        type(resource["hostile_peak_live_raw_c128_shard_count"]) is not int
        or resource["hostile_peak_live_raw_c128_shard_count"] != 23
    ):
        raise Failure("hostile raw-c128 peak-live-shard mismatch")
    if (
        type(resource["hostile_scratch_minimum_bytes"]) is not int
        or resource["hostile_scratch_minimum_bytes"] != 9_600_935_128
    ):
        raise Failure("hostile raw-c128 resource/freshness mismatch")


def validate_parallel_resource_certificate() -> int:
    expected_aggregate = 2 * (17_179_869_184 + 252_944_080)
    check(builder.PARALLEL_TARGET_AUTHENTICATION_PEAK == 252_944_080,
          "target authentication peak changed")
    check(builder.PARALLEL_HOSTILE_AUTHENTICATION_PEAK == 252_944_080,
          "hostile authentication peak changed")
    check(builder.v004.RSS_LIMIT == 17_179_869_184, "target RSS cap changed")
    check(builder.PARALLEL_HOSTILE_RSS_LIMIT == 17_179_869_184,
          "hostile RSS cap changed")
    check(builder.PARALLEL_AGGREGATE_PEAK == expected_aggregate,
          "parallel aggregate arithmetic")
    check(builder.PARALLEL_HOST_TOTAL_MINIMUM == 48_000_000_000,
          "parallel host minimum")
    check(builder.PARALLEL_HOST_HEADROOM_MINIMUM == 13_134_373_472,
          "parallel decimal-48GB headroom")
    check(builder.PARALLEL_TARGET_SCRATCH_MINIMUM == 9_600_954_452,
          "target scratch minimum")
    check(builder.PARALLEL_HOSTILE_SCRATCH_MINIMUM == 9_600_935_128,
          "hostile scratch minimum")
    check(builder.PARALLEL_FILESYSTEM_MINIMUM == 19_201_889_580,
          "parallel filesystem arithmetic")
    hostile_resource = {
        "hostile_scratch_minimum_bytes": builder.PARALLEL_HOSTILE_SCRATCH_MINIMUM,
        "hostile_peak_live_raw_c128_shard_count": 23,
        "hostile_container_header_bytes": 0,
    }
    validate_hostile_raw_c128_resource_identity(hostile_resource)
    check(
        hostile_resource["hostile_scratch_minimum_bytes"]
        + hostile_resource["hostile_peak_live_raw_c128_shard_count"]
        * hostile_resource["hostile_container_header_bytes"]
        == 9_600_935_128,
        "hostile raw-c128 zero-header arithmetic",
    )
    check(
        builder.PARALLEL_TARGET_SCRATCH_MINIMUM
        + hostile_resource["hostile_scratch_minimum_bytes"]
        == builder.PARALLEL_FILESYSTEM_MINIMUM,
        "independent target/hostile scratch sum",
    )
    wrong_header = dict(hostile_resource)
    wrong_header["hostile_container_header_bytes"] = 23 * 128
    try:
        validate_hostile_raw_c128_resource_identity(wrong_header)
    except Failure as error:
        check(
            str(error) == "hostile raw-c128 header mismatch",
            "hostile target-header mutation wrong refusal",
        )
    else:
        raise Failure("hostile target-header mutation was accepted")
    return 14


def validate_runtime_stat_portability() -> int:
    paths = (
        HERE,
        HERE / "METHOD.md",
        builder.RUNTIME_COMPATIBILITY_OBSTRUCTION,
        builder.V005_DIR / "CACHE_PAYLOADS" / "L12" / "CACHE_MANIFEST.json",
    )
    for path in paths:
        metadata = os.stat(path, follow_symlinks=False)
        check(metadata.st_mode != 0, f"portable os.stat failed: {path}")
    return len(paths)


def validate_zero_length_cache_open() -> int:
    with tempfile.TemporaryDirectory(prefix="target_v012_zero_") as directory:
        path = Path(directory) / "zero.i32"
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
        os.fchmod(descriptor, 0o444)
        os.close(descriptor)
        descriptor = consumer.open_stable_readonly(path)
        root_descriptor = os.open(
            Path(directory), os.O_RDONLY | os.O_DIRECTORY
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            metadata = os.fstat(descriptor)
            context = consumer.CacheContext.__new__(consumer.CacheContext)
            context.closed = False
            context.root_descriptor = root_descriptor
            context.records = {
                path.name: {
                    "dtype": consumer.INDEX_DTYPE.str,
                    "shape": [0],
                }
            }
            context.descriptors = {path.name: descriptor}
            context.identities = {
                path.name: consumer._cache_file_identity(metadata)
            }
            array = context.open(path.name, consumer.INDEX_DTYPE)
            check(isinstance(array, np.ndarray), "zero-length cache open type")
            check(not isinstance(array, np.memmap), "zero-length cache was memmapped")
            check(array.shape == (0,), "zero-length cache shape")
            check(array.dtype == consumer.INDEX_DTYPE, "zero-length cache dtype")
            check(array.size == 0, "zero-length cache size")
        finally:
            os.close(descriptor)
            os.close(root_descriptor)
    return 5


def validate_strict_json_refusals() -> int:
    payloads = {
        "valid": b'{"a":1}\n',
        "duplicate": b'{"a":1,"a":2}\n',
        "nan": b'{"a":NaN}\n',
        "infinity": b'{"a":Infinity}\n',
    }
    checks = 0
    with tempfile.TemporaryDirectory(prefix="target_v012_json_") as directory:
        root = Path(directory)
        paths: dict[str, Path] = {}
        for name, raw in payloads.items():
            path = root / f"{name}.json"
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
            try:
                os.write(descriptor, raw)
            finally:
                os.close(descriptor)
            path.chmod(0o444)
            paths[name] = path
        for label, reader in (
            ("builder", builder.immutable_json),
            ("consumer", consumer.immutable_json),
        ):
            record, _digest = reader(paths["valid"], f"{label} valid JSON")
            check(record == {"a": 1} and type(record["a"]) is int,
                  f"{label} valid strict JSON rejected")
            checks += 1
            for name in ("duplicate", "nan", "infinity"):
                expect_refusal(
                    lambda candidate=paths[name], load=reader, kind=name: load(
                        candidate, f"{label} {kind} JSON"
                    ),
                    "duplicate JSON key" if name == "duplicate" else "nonfinite JSON constant",
                    f"{label} accepted {name} JSON",
                )
                checks += 1
    return checks


def validate_word_orders() -> int:
    comparisons = 0
    for width in range(17):
        for weight in range(width + 1):
            target = builder.v004.sealed.fixed_words(width, weight)
            independent = independent_words(width, weight)
            check(np.array_equal(target, independent), f"fixed_words identity width={width} q={weight}")
            check(len(target) == math.comb(width, weight), "fixed_words census")
            check(len(np.unique(target)) == len(target), "fixed_words uniqueness")
            comparisons += 1
    return comparisons


def validate_l4_operator() -> tuple[int, float, float]:
    length = 4
    edges = builder.v004.sealed.graph(length)
    pair_checks = 0
    max_h_error = 0.0
    max_current_error = 0.0
    for q in range(length + 1):
        words, offsets, sources, targets = builder.exact_operator_arrays(length, q, edges)
        direct = builder.v004.sealed.Sector(length, q, edges)
        check(np.array_equal(words, direct.words), "L4 operator word order")
        cached = consumer.CachedSector.__new__(consumer.CachedSector)
        cached.length = length
        cached.q = q
        cached.words = words
        cached.offsets = offsets
        cached.sources = sources
        cached.targets = targets
        cached.pairs = []
        for edge_index, direct_pair in enumerate(direct.pairs):
            lower = int(offsets[edge_index])
            upper = int(offsets[edge_index + 1])
            cached_pair = (sources[lower:upper], targets[lower:upper])
            check(np.array_equal(cached_pair[0], direct_pair[0]), "L4 source ranks")
            check(np.array_equal(cached_pair[1], direct_pair[1]), "L4 target ranks")
            cached.pairs.append(cached_pair)
            pair_checks += 1
        columns = len(words)
        real = np.arange(3 * columns, dtype=float).reshape(3, columns) + 1.0
        imag = np.arange(3 * columns, dtype=float).reshape(3, columns)[:, ::-1] + 0.25
        probe = (real + 1.0j * imag) / max(1, columns)
        direct_h = direct.h(probe)
        cached_h = consumer.CachedSector.h(cached, probe)
        direct_current = direct.currents(probe)
        cached_current = consumer.CachedSector.currents(cached, probe)
        max_h_error = max(max_h_error, float(np.max(np.abs(direct_h - cached_h))) if direct_h.size else 0.0)
        max_current_error = max(max_current_error, float(np.max(np.abs(direct_current - cached_current))) if direct_current.size else 0.0)
        check(np.array_equal(direct_h, cached_h), "L4 cached h differential")
        check(np.array_equal(direct_current, cached_current), "L4 signed current differential")
        cached.close()
    return pair_checks, max_h_error, max_current_error


def validate_l4_admission_lineage() -> tuple[int, int]:
    length = 4
    carrier = {q: builder.carrier_words(length, q) for q in range(length + 1)}
    admission_checks = 0
    for event in range(length):
        for q in range(event + 1):
            blank, destination = builder.exact_admission_arrays(length, event, q, carrier[q], carrier[q + 1])
            independent_blank = np.asarray(
                [rank for rank, word in enumerate(carrier[q]) if not ((int(word) >> event) & 1)],
                dtype=builder.INDEX_DTYPE,
            )
            lookup = {int(word): rank for rank, word in enumerate(carrier[q + 1])}
            independent_destination = np.asarray(
                [lookup[int(carrier[q][rank]) | (1 << event)] for rank in independent_blank],
                dtype=builder.INDEX_DTYPE,
            )
            check(np.array_equal(blank, independent_blank), "L4 admission ALLOW indices")
            check(np.array_equal(destination, independent_destination), "L4 admission SELECT destination")
            admission_checks += 1
    lineage = {(prefix, q): builder.lineage_words(prefix, q) for prefix in range(length) for q in range(prefix + 1)}
    lineage_checks = 0
    for prefix in range(length - 1):
        for q in range(prefix + 1):
            stay, accepted = builder.exact_lineage_maps(
                prefix,
                q,
                lineage[(prefix, q)],
                lineage[(prefix + 1, q)],
                lineage[(prefix + 1, q + 1)],
            )
            check(
                np.array_equal(lineage[(prefix + 1, q)][stay], lineage[(prefix, q)]),
                "L4 lineage stay identity",
            )
            check(
                np.array_equal(
                    lineage[(prefix + 1, q + 1)][accepted],
                    lineage[(prefix, q)] | (1 << prefix),
                ),
                "L4 lineage write identity",
            )
            lineage_checks += 1
    return admission_checks, lineage_checks


def validate_allocation_census() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for length, expected in EXPECTED_CENSUS.items():
        observed = (
            builder.operator_bytes(length),
            builder.admission_bytes(length),
            builder.lineage_mask_bytes(length),
            builder.lineage_map_bytes(length),
            builder.payload_bytes(length),
            builder.maximum_state_bytes(length),
            builder.terminal_cache_peak_bytes(length),
            builder.authentication_cache_peak_bytes(length),
            builder.maximum_cache_window_bytes(length),
            builder.expected_file_count(length),
        )
        check(observed == expected, f"allocation census L{length}")
        check(observed[4] + observed[5] + builder.OVERHEAD_RESERVE < builder.SCRATCH_LIMIT, "scratch certificate")
        check(observed[8] <= builder.MAPPED_CACHE_LIMIT, "mapped cache certificate")
        rows.append(
            {
                "L": length,
                "operator_bytes": observed[0],
                "admission_bytes": observed[1],
                "lineage_mask_bytes": observed[2],
                "lineage_map_bytes": observed[3],
                "payload_bytes": observed[4],
                "maximum_state_bytes": observed[5],
                "state_plus_cache_plus_reserve_bytes": observed[4] + observed[5] + builder.OVERHEAD_RESERVE,
                "terminal_cache_peak_bytes": observed[6],
                "authentication_cache_peak_bytes": observed[7],
                "maximum_cache_window_bytes": observed[8],
                "file_count": observed[9],
            }
        )
    return rows


def validate_absent_gate_locks(freeze: dict[str, object]) -> None:
    check(freeze.get("cache_payload_created") is False, "freeze payload flag")
    check(freeze.get("physical_history_executed") is False, "freeze physical flag")
    for path in (
        builder.DUAL_GATE,
        consumer.PHYSICAL_GATE,
        consumer.CONTROL_AUTHORIZATION_GATE,
        consumer.CACHED_CONTROL_GATE,
        consumer.CACHED_CONTROL_GATE_AUDIT,
        consumer.L10_EXECUTION_AUTHORIZATION_GATE,
        consumer.CACHED_L10_GATE,
        consumer.CACHED_L10_GATE_AUDIT,
        consumer.TARGET_L12_EXECUTION_GATE,
        consumer.HOSTILE_L12_EXECUTION_GATE,
        consumer.TARGET_HOSTILE_L10_CROSS_GATE,
        consumer.PARALLEL_L12_SCHEDULE_GATE,
        consumer.PARALLEL_L12_SCHEDULE_AUDIT,
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_READY_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_READY_V001.json",
        consumer.DUAL_L12_LAUNCH_HANDSHAKE,
        consumer.DUAL_L12_WORKER_RELEASE,
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_COMMAND_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_ACK_V001.json",
        builder.ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
        builder.ROOT / (
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
            "TARGET_V012_WORKER_COMPLETION_V001.json"
        ),
        builder.ROOT / (
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
            "HOSTILE_V004R4_WORKER_COMPLETION_V001.json"
        ),
        consumer.PARALLEL_L12_TELEMETRY,
        consumer.PARALLEL_L12_SHARED_DIR / "FINAL_L12_TARGET_HOSTILE_AUDIT_V001.json",
        consumer.HOSTILE_L10_EXECUTION_GATE,
        builder.ROOT / (
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
        ),
        builder.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS",
        builder.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
        builder.ROOT / (
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"
        ),
        builder.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS",
        builder.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES",
        builder.ROOT / builder.FUTURE_HOSTILE_AUDIT_PATH,
        builder.ROOT / builder.FUTURE_POSTBUILD_AUDIT_PATH,
        builder.ROOT / builder.FUTURE_PHYSICAL_GATE_AUDIT_PATH,
        builder.CACHE_PARENT,
        consumer.PHYSICAL_OUTPUT_PARENT,
        consumer.WORKSPACE_PARENT,
    ):
        check(not path.exists(), f"freeze lock/payload path unexpectedly present: {path.name}")
    cache = builder.CACHE_PARENT / "L4"
    output = consumer.PHYSICAL_OUTPUT_PARENT / "HISTORY_L4.json"
    workspace = consumer.WORKSPACE_PARENT / "L4"
    expect_refusal(
        lambda: builder.build(4, cache),
        "V012 dual obstruction/compatibility gate is absent",
        "builder did not refuse absent dual gate",
    )
    expect_refusal(
        lambda: consumer.execute(4, cache, "0" * 64, output, workspace),
        "V012 dual obstruction/compatibility gate is absent",
        "consumer did not refuse absent dual gate",
    )
    expect_refusal(
        lambda: consumer.require_parallel_l12_schedule_gate("0" * 64),
        "absent",
        "parallel L12 path did not refuse absent schedule gate",
    )
    expect_refusal(
        lambda: consumer.require_stage_gate(
            consumer.CACHED_CONTROL_GATE,
            "TARGET_V012_CACHED_CONTROL_L4_L8_GATE",
            "PASS_TARGET_V012_CACHED_CONTROLS_L4_L6_L8",
            (4, 6, 8), {}, "0" * 64, freeze,
        ),
        "absent", "control stage path did not refuse absent gate",
    )
    expect_refusal(
        lambda: consumer.require_stage_gate_audit(
            consumer.CACHED_CONTROL_GATE_AUDIT,
            consumer.CACHED_CONTROL_GATE, {},
            "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001",
            "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8",
            (4, 6, 8),
        ),
        "absent", "control stage audit path did not refuse absent audit",
    )
    expect_refusal(
        lambda: consumer.require_l10_execution_authorization(
            freeze, "0" * 64, {}, {}, "0" * 64
        ),
        "absent", "L10 path did not refuse absent distinct authorization",
    )
    expect_refusal(
        lambda: consumer.require_target_l12_execution_gate(
            freeze, "0" * 64, {}, "0" * 64, "0" * 64,
            "0" * 64, "0" * 64,
        ),
        "absent", "L12 path did not refuse absent distinct authorization",
    )
    expect_refusal(
        lambda: consumer.require_hostile_l12_execution_gate(
            {}, "0" * 64, "0" * 64, "0" * 64,
        ),
        "absent", "hostile L12 path did not refuse absent authorization",
    )
    expect_refusal(
        lambda: consumer.require_dual_l12_launch_handshake(
            {"expires_epoch": 0}, "0" * 64, "0" * 64,
            "0" * 64, "0" * 64,
        ),
        "schedule expired before authority read",
        "dual L12 path did not refuse absent blocked-worker handshake",
    )
    expect_refusal(
        lambda: consumer.require_dual_l12_worker_release(
            {"expires_epoch": 0}, {}, "0" * 64, "0" * 64, "0" * 64,
        ),
        "schedule expired before authority read",
        "dual L12 path did not refuse absent worker release",
    )
    expect_refusal(
        lambda: consumer.require_shared_schedule_audit(
            {}, "0" * 64, "0" * 64,
        ),
        "absent", "shared schedule path did not refuse absent audit",
    )
    expect_refusal(
        lambda: consumer.require_target_hostile_l10_cross_gate(
            freeze, {}, {}, "0" * 64,
        ),
        "absent", "L10 cross path did not refuse absent cross gate",
    )
    check(not cache.exists() and not output.exists() and not workspace.exists(), "lock test created physical state")


def main() -> int:
    try:
        validate_existing_result_state()
        freeze = validate_freeze()
        dependency_checks = validate_dependencies()
        freeze_mutation_checks = validate_freeze_mutation_refusals(freeze)
        obstruction_checks = validate_obstruction_custody_and_alias_rejection()
        future_audit_refusals = validate_future_audit_gate_refusals(freeze)
        v011_exact_type_repairs = validate_syntax_and_static_locks()
        parallel_resource_checks = validate_parallel_resource_certificate()
        portable_stat_checks = validate_runtime_stat_portability()
        zero_length_cache_checks = validate_zero_length_cache_open()
        strict_json_checks = validate_strict_json_refusals()
        word_comparisons = validate_word_orders()
        pair_checks, h_error, current_error = validate_l4_operator()
        admission_checks, lineage_checks = validate_l4_admission_lineage()
        allocation = validate_allocation_census()
        validate_absent_gate_locks(freeze)
        mutation_ledger, mutation_counts = execute_obligation_mutations(freeze)
        result = {
            "schema": "TARGET_L12_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT_V012",
            "classification": "PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT",
            "physical_cache_payload_created": False,
            "physical_history_executed": False,
            "checks": {
                "syntax_files": 4,
                "portable_os_stat_runtime_checks": portable_stat_checks,
                "zero_length_cache_runtime_checks": zero_length_cache_checks,
                "strict_json_descriptor_checks": strict_json_checks,
                "v011_exact_type_repairs": v011_exact_type_repairs,
                "authenticated_dependency_records": dependency_checks,
                "audit_obligation_artifacts": mutation_counts["artifacts"],
                "audit_obligation_positive_fixtures": mutation_counts["positive_fixtures"],
                "audit_obligation_mutation_classes": mutation_counts["mutation_classes"],
                "audit_obligation_mutation_assignments": mutation_counts["mutation_assignments"],
                "audit_obligation_positive_sink_calls": mutation_counts[
                    "positive_sink_calls"
                ],
                "audit_obligation_mutation_sink_calls": mutation_counts[
                    "mutation_sink_calls"
                ],
                "authorization_dag_states": 262144,
                "authorization_dag_invalid_state_action_refusals": 4718124,
                "authorization_dag_legal_reachable_states": 26,
                "freeze_mutation_refusals": freeze_mutation_checks,
                "obstruction_custody_and_global_alias_checks": obstruction_checks,
                "future_hostile_audit_gate_refusals": future_audit_refusals,
                "target_fixed_words_width_0_through_16_comparisons": word_comparisons,
                "L4_oriented_edge_charge_pair_checks": pair_checks,
                "L4_admission_event_charge_checks": admission_checks,
                "L4_lineage_prefix_charge_checks": lineage_checks,
                "allocation_lengths": len(allocation),
                "parallel_resource_certificate_checks": parallel_resource_checks,
                "hard_lock_entrypoints": 12,
            },
            "L4_differential": {
                "maximum_h_error": h_error,
                "maximum_signed_current_error": current_error,
            },
            "allocation_census": allocation,
            "resource_limits": expected_resource_limits(),
            "files": {
                "method_sha256": sha256(HERE / "METHOD.md"),
                "builder_sha256": sha256(HERE / "build_target_cache.py"),
                "consumer_sha256": sha256(HERE / "consume_target_cache.py"),
                "production_obligation_validators_sha256": sha256(
                    HERE / "production_obligation_validators.py"
                ),
                "preflight_sha256": sha256(Path(__file__)),
                "freeze_sha256": sha256(FREEZE),
            },
            "mutation_ledger": {
                "path": str(MUTATION_LEDGER.relative_to(ROOT)),
                "sha256": None,
                "schema": MUTATION_LEDGER_SCHEMA,
                "classification": MUTATION_LEDGER_CLASSIFICATION,
                "case_count": mutation_counts["mutation_assignments"],
                "positive_sink_call_count": mutation_counts["positive_sink_calls"],
                "mutation_sink_call_count": mutation_counts["mutation_sink_calls"],
                "obligation_matrix_sha256": OBLIGATION_MATRIX_SHA256,
                "validator_module_sha256": freeze["files"][
                    "production_obligation_validators.py"
                ],
            },
            "compatibility": {
                "superseded_v005_payloads_consumed": False,
                "portable_os_stat_follow_symlinks_supported": True,
                "fresh_v012_cache_root": str(builder.CACHE_PARENT),
                "superseded_v006_payloads_consumed": False,
                "superseded_v007_payloads_consumed": False,
                "superseded_v008_payloads_consumed": False,
                "superseded_v009_payloads_consumed": False,
                "superseded_v010_payloads_consumed": False,
                "superseded_v011_payloads_consumed": False,
            },
            "claim_boundary": "V012_PORTABLE_NONPHYSICAL_STORAGE_INDEX_PROOF_ONLY__NO_CACHE_PAYLOAD_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
        }
        if not exact_tree_equal(current_source_sha256(), freeze["files"]):
            raise Failure("preflight source hashes drifted before evidence publication")
        ledger_raw = canonical_json_bytes(mutation_ledger)
        predicted_ledger_sha256 = hashlib.sha256(ledger_raw).hexdigest()
        result["mutation_ledger"]["sha256"] = predicted_ledger_sha256
        validate_preflight_result_document(
            result, freeze, predicted_ledger_sha256,
        )
        builder.validate_freeze_document(freeze)
        if validate_dependencies() != dependency_checks:
            raise Failure("dependency census drifted before evidence publication")
        sealed_ledger, mutation_ledger_sha256 = atomic_publish_immutable_json(
            MUTATION_LEDGER, mutation_ledger, "sealed V012 mutation ledger",
        )
        if mutation_ledger_sha256 != predicted_ledger_sha256:
            raise Failure("sealed mutation ledger changed during publication")
        matrix, _matrix_digest = load_obligation_matrix()
        validate_mutation_ledger(sealed_ledger, matrix, freeze)
        result["mutation_ledger"]["sha256"] = mutation_ledger_sha256
        validate_preflight_result_document(result, freeze, mutation_ledger_sha256)
        builder.validate_freeze_document(freeze)
        if validate_dependencies() != dependency_checks:
            raise Failure("dependency census drifted during evidence publication")
        if not exact_tree_equal(current_source_sha256(), freeze["files"]):
            raise Failure("preflight source hashes drifted during evidence publication")
        atomic_publish_immutable_json(
            RESULT, result, "sealed V012 preflight result",
        )
    except (AssertionError, Failure, OSError, builder.Refusal, consumer.Refusal,
            obligation_validators.Refusal,
            ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 2
    print("PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
