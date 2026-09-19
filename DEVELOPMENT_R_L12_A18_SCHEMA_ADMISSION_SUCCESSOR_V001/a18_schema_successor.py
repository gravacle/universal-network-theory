#!/usr/bin/env python3
"""Authenticated A18 schema-admission successor.

This module changes only A18 admission: the target and hostile roles live at
``target.branch.role`` and ``hostile.branch.role``.  It does not alter a V012
source, cache, history, audit, comparison tolerance, or downstream criterion.
The successor path is isolated from every existing V012/hostile namespace.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
CANONICAL_SUCCESSOR_A18: Final[Path] = (
    HERE / "TARGET_HOSTILE_L10_CROSS_GATE_A18_SUCCESSOR_V001.json"
)
A14_PATH: Final[Path] = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "PHYSICAL_OUTPUTS" / "HISTORY_L10.json"
)
A14_SHA256: Final[str] = (
    "4b5665df7448f56ba7125f3f85a1631747710158a8e3131d944a202d0db2128d"
)
A16_PATH: Final[Path] = (
    ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "CACHED_L10_GATE_AUDIT_V001.json"
)
A16_SHA256: Final[str] = (
    "c564088261de61ba84e9dcaa6b3e5f485c7c419263fa822dff2ca28a57d5b1de"
)
A17_CONTAINER_PATH: Final[Path] = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "A18_DUAL_SINK_ROLE_CONTRACT_OBSTRUCTION_V001.json"
)
A17_CONTAINER_SHA256: Final[str] = (
    "52882072cea1413ae2f403770d554f0e3b1654c0f352a026d744d80cd92e4f40"
)
A17_SHA256: Final[str] = (
    "ad9c4c30b6bc199000a5c3f50bde6711adab35cc4bbdcfa19787051bea9ca21e"
)
A18_CANDIDATE_WIRE_SHA256: Final[str] = (
    "116a90eceb86433e972cb7cfa8fb67f4fde45294d40b3014508294f801870084"
)
A18_SCHEMA: Final[str] = "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001"
A18_CLASSIFICATION: Final[str] = "PASS_EXACT_TARGET_HOSTILE_L10_CROSS_BENCHMARK"
A18_CLAIM: Final[str] = (
    "FINITE_L10_TARGET_HOSTILE_CROSS_AUDIT_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
)
AMENDMENT_CLAIM: Final[str] = (
    "A18_SCHEMA_ADMISSION_CORRECTION_ONLY__NO_HISTORY_RECOMPUTATION_"
    "COMPARISON_CHANGE_OR_DOWNSTREAM_AUTHORIZATION"
)
TOP_KEYS: Final[set[str]] = {
    "schema", "classification", "auditor_role", "sealed_input_commit", "L",
    "target", "hostile", "comparison_policy", "checks", "checks_passed",
    "checks_total", "failures", "claim_boundary",
}
TARGET_PROJECTION_KEYS: Final[set[str]] = {
    "branch", "cached_L10_gate_sha256", "cached_L10_gate_audit_sha256",
    "history_sha256",
}
HOSTILE_PROJECTION_KEYS: Final[set[str]] = {
    "branch", "cached_L10_gate_sha256",
    "l10_execution_authorization_gate_sha256",
    "independent_prepayload_audit_sha256", "history_sha256",
}
BRANCH_KEYS: Final[set[str]] = {
    "role", "method", "builder", "consumer", "preflight", "freeze",
    "preflight_result", "independent_audit", "cached_L10_gate",
    "L12_cache_manifest",
}
A17_COMPONENT_LABELS: Final[tuple[str, ...]] = (
    "method", "builder", "consumer", "preflight", "freeze",
    "preflight_result", "independent_audit", "cached_L10_gate",
    "L12_cache_manifest",
)
FROZEN_TARGET_WORKER: Final[Path] = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "consume_target_cache.py"
)
FROZEN_TARGET_WORKER_SHA256: Final[str] = (
    "80b2ce08af37bc8cffd91f07146c777f60785883436361ca9521597763fd5a11"
)
FROZEN_HOSTILE_WORKER: Final[Path] = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "consume_cache_v004r4.py"
)
FROZEN_HOSTILE_WORKER_SHA256: Final[str] = (
    "700dce18ec8f50008a9e3022394a55c8d689268e21b80982896d37b92add7b74"
)
FROZEN_DUAL_LAUNCHER: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001"
    / "production_dual_l12_launcher.py"
)
FROZEN_DUAL_LAUNCHER_SHA256: Final[str] = (
    "095f8cd25499ea4f36cba913038cfbdadfe6e56309046370d4eeb03c347c1d71"
)
OLD_A18_RELATIVE_PATH: Final[bytes] = (
    b'TARGET_HOSTILE_L10_CROSS_GATE_V001.json'
)
FROZEN_SHARED_NAMESPACE: Final[Path] = (
    ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
)
FROZEN_A20: Final[Path] = (
    FROZEN_SHARED_NAMESPACE / "SHARED_AGGREGATE_SCHEDULE_GATE_V001.json"
)
FROZEN_A21: Final[Path] = (
    FROZEN_SHARED_NAMESPACE
    / "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json"
)


class Refusal(RuntimeError):
    """A successor input or publication failed closed."""


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("record is not finite canonical JSON") from error


def publication_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("record is not finite publication JSON") from error


def _strict_json(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise Refusal(f"{label} duplicate JSON key")
            result[key] = value
        return result

    def constant(token: str) -> object:
        raise Refusal(f"{label} nonfinite JSON constant: {token}")

    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=pairs,
            parse_constant=constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{label} malformed JSON") from error
    if type(value) is not dict:
        raise Refusal(f"{label} is not a JSON object")
    return value


def _identity(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        stat.S_IMODE(metadata.st_mode),
    )


def _descriptor_sha256(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while block := os.pread(descriptor, 16 * 2**20, offset):
        digest.update(block)
        offset += len(block)
    return digest.hexdigest()


def _descriptor_bytes(descriptor: int, size: int) -> bytes:
    output = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(descriptor, min(2**20, size - offset), offset)
        if not block:
            raise Refusal("descriptor read made no progress")
        output.extend(block)
        offset += len(block)
    return bytes(output)


def _require_canonical_path(path: Path, label: str) -> None:
    if not path.is_absolute() or path.resolve(strict=False) != path:
        raise Refusal(f"{label} path is not canonical")
    current = Path(path.anchor)
    for part in path.parts[1:-1]:
        current /= part
        try:
            metadata = os.stat(current, follow_symlinks=False)
        except OSError as error:
            raise Refusal(f"{label} parent is absent") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise Refusal(f"{label} parent is aliased or special")


class StableInput:
    """An immutable descriptor retained until the caller closes custody."""

    def __init__(self, path: Path, expected_sha256: str, label: str) -> None:
        self.path = path
        self.expected_sha256 = expected_sha256
        self.label = label
        self.descriptor = -1
        self.identity: tuple[int, int, int, int, int, int, int] | None = None
        self.raw = b""
        self.record: dict[str, object] | None = None

    def open(self, *, json_record: bool) -> None:
        if self.descriptor >= 0:
            raise Refusal(f"{self.label} is already open")
        if (
            type(self.expected_sha256) is not str
            or len(self.expected_sha256) != 64
            or any(c not in "0123456789abcdef" for c in self.expected_sha256)
        ):
            raise Refusal(f"{self.label} expected hash is malformed")
        _require_canonical_path(self.path, self.label)
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        try:
            descriptor = os.open(self.path, flags)
        except OSError as error:
            raise Refusal(f"{self.label} is absent or aliased") from error
        self.descriptor = descriptor
        try:
            held = os.fstat(descriptor)
            named = os.stat(self.path, follow_symlinks=False)
            identity = _identity(held)
            if (
                not stat.S_ISREG(held.st_mode) or held.st_mode & 0o222
                or held.st_nlink != 1 or _identity(named) != identity
            ):
                raise Refusal(f"{self.label} is not immutable owner-once evidence")
            raw = _descriptor_bytes(descriptor, held.st_size)
            digest = _descriptor_sha256(descriptor)
            if digest != self.expected_sha256 or hashlib.sha256(raw).hexdigest() != digest:
                raise Refusal(f"{self.label} hash mismatch")
            self.identity = identity
            self.raw = raw
            if json_record:
                self.record = _strict_json(raw, self.label)
            self.reauthenticate()
        except BaseException:
            self.close()
            raise

    def reauthenticate(self) -> None:
        if self.descriptor < 0 or self.identity is None:
            raise Refusal(f"{self.label} descriptor is not retained")
        try:
            named = os.stat(self.path, follow_symlinks=False)
        except OSError as error:
            raise Refusal(f"{self.label} path changed") from error
        held = os.fstat(self.descriptor)
        if (
            _identity(held) != self.identity or _identity(named) != self.identity
            or _descriptor_sha256(self.descriptor) != self.expected_sha256
        ):
            raise Refusal(f"{self.label} descriptor/path drift")

    def close(self) -> None:
        if self.descriptor >= 0:
            os.close(self.descriptor)
            self.descriptor = -1


class PredecessorCustody:
    """Retain exact A14/A16 and the composite A17 authority."""

    def __init__(self) -> None:
        self.inputs: list[StableInput] = []
        self.a14: dict[str, object] = {}
        self.a16: dict[str, object] = {}
        self.a17: dict[str, object] = {}
        self.candidate: dict[str, object] = {}
        self.a17_components: dict[str, dict[str, object]] = {}

    def __enter__(self) -> "PredecessorCustody":
        self.open()
        return self

    def __exit__(self, *_error: object) -> None:
        self.close()

    def _add(
        self, path: Path, digest: str, label: str, *, json_record: bool,
    ) -> StableInput:
        item = StableInput(path, digest, label)
        item.open(json_record=json_record)
        self.inputs.append(item)
        return item

    def open(self) -> None:
        if self.inputs:
            raise Refusal("predecessor custody already open")
        try:
            a14 = self._add(A14_PATH, A14_SHA256, "A14", json_record=True)
            a16 = self._add(A16_PATH, A16_SHA256, "A16", json_record=True)
            container = self._add(
                A17_CONTAINER_PATH, A17_CONTAINER_SHA256,
                "A17 sealed container", json_record=True,
            )
            if a14.record is None or a16.record is None or container.record is None:
                raise Refusal("predecessor JSON record is absent")
            candidate = container.record.get("candidate_a18_record")
            if type(candidate) is not dict:
                raise Refusal("A17 container candidate is absent")
            if (
                container.record.get("candidate_a18_wire_sha256")
                != A18_CANDIDATE_WIRE_SHA256
                or hashlib.sha256(publication_json_bytes(candidate)).hexdigest()
                != A18_CANDIDATE_WIRE_SHA256
            ):
                raise Refusal("A17 container candidate wire hash mismatch")
            hostile = candidate.get("hostile")
            branch = hostile.get("branch") if type(hostile) is dict else None
            if (
                type(branch) is not dict or set(branch) != BRANCH_KEYS
                or branch.get("role") != "hostile_v004r4"
                or hashlib.sha256(canonical_json_bytes(branch)).hexdigest()
                != A17_SHA256
            ):
                raise Refusal("A17 composite bytes/hash mismatch")
            for label in A17_COMPONENT_LABELS:
                binding = branch.get(label)
                if (
                    type(binding) is not dict
                    or type(binding.get("path")) is not str
                    or type(binding.get("sha256")) is not str
                ):
                    raise Refusal(f"A17 {label} binding malformed")
                component = self._add(
                    Path(binding["path"]), binding["sha256"],
                    f"A17 {label}", json_record=label in {
                        "freeze", "preflight_result", "independent_audit",
                        "cached_L10_gate", "L12_cache_manifest",
                    },
                )
                if component.record is not None:
                    self.a17_components[label] = component.record
            self.a14 = a14.record
            self.a16 = a16.record
            self.a17 = branch
            self.candidate = candidate
            self._validate_predecessors()
            self.reauthenticate()
        except BaseException:
            self.close()
            raise

    def _validate_predecessors(self) -> None:
        hostile_gate = self.a17_components.get("cached_L10_gate")
        if (
            self.a14.get("schema") != "TARGET_CACHED_PREFIX_HISTORY_V012"
            or self.a14.get("L") != 10 or type(self.a14.get("L")) is not int
            or self.a16.get("schema")
            != "TARGET_V012_CACHED_L10_GATE_AUDIT_V001"
            or self.a16.get("classification")
            != "PASS_INDEPENDENT_TARGET_V012_CACHED_L10"
            or self.a16.get("history_sha256_by_L") != {"10": A14_SHA256}
            or type(hostile_gate) is not dict
            or hostile_gate.get("schema") != "HOSTILE_V004R4_CACHED_L10_GATE"
            or hostile_gate.get("classification") != "PASS_HOSTILE_V004R4_CACHED_L10"
        ):
            raise Refusal("A14/A16/A17 predecessor identity mismatch")

    def reauthenticate(self) -> None:
        if len(self.inputs) != 3 + len(A17_COMPONENT_LABELS):
            raise Refusal("A14/A16/A17 descriptor census mismatch")
        for item in self.inputs:
            item.reauthenticate()
        if hashlib.sha256(canonical_json_bytes(self.a17)).hexdigest() != A17_SHA256:
            raise Refusal("A17 composite changed during custody")

    def close(self) -> None:
        for item in reversed(self.inputs):
            item.close()
        self.inputs.clear()


def validate_a18(record: object, custody: PredecessorCustody) -> dict[str, object]:
    custody.reauthenticate()
    if type(record) is not dict or set(record) != TOP_KEYS or "role" in record:
        raise Refusal("A18 exact top-level key census mismatch")
    target = record.get("target")
    hostile = record.get("hostile")
    if type(target) is not dict or set(target) != TARGET_PROJECTION_KEYS:
        raise Refusal("A18 exact target projection key census mismatch")
    if type(hostile) is not dict or set(hostile) != HOSTILE_PROJECTION_KEYS:
        raise Refusal("A18 exact hostile projection key census mismatch")
    target_branch = target.get("branch")
    hostile_branch = hostile.get("branch")
    if (
        type(target_branch) is not dict or set(target_branch) != BRANCH_KEYS
        or target_branch.get("role") != "target_v012"
        or type(hostile_branch) is not dict or set(hostile_branch) != BRANCH_KEYS
        or hostile_branch.get("role") != "hostile_v004r4"
    ):
        raise Refusal("A18 nested branch role mismatch")
    hostile_gate = custody.a17_components["cached_L10_gate"]
    histories = hostile_gate.get("histories")
    authorization = hostile_gate.get("l10_execution_authorization")
    if (
        record.get("schema") != A18_SCHEMA
        or record.get("classification") != A18_CLASSIFICATION
        or record.get("L") != 10 or type(record.get("L")) is not int
        or record.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or record.get("claim_boundary") != A18_CLAIM
        or target.get("history_sha256") != A14_SHA256
        or target.get("cached_L10_gate_audit_sha256") != A16_SHA256
        or target.get("cached_L10_gate_sha256")
        != custody.a16.get("stage_gate_sha256")
        or hostile_branch != custody.a17
        or hostile.get("cached_L10_gate_sha256")
        != custody.a17["cached_L10_gate"]["sha256"]
        or hostile.get("independent_prepayload_audit_sha256")
        != custody.a17["independent_audit"]["sha256"]
        or type(histories) is not list or len(histories) != 1
        or type(histories[0]) is not dict
        or hostile.get("history_sha256") != histories[0].get("sha256")
        or type(authorization) is not dict
        or hostile.get("l10_execution_authorization_gate_sha256")
        != authorization.get("sha256")
        or target.get("history_sha256") == hostile.get("history_sha256")
        or record.get("failures") != []
        or type(record.get("checks_total")) is not int
        or type(record.get("checks_passed")) is not int
        or record.get("checks_total") != 65
        or record.get("checks_passed") != record.get("checks_total")
        or record != custody.candidate
    ):
        raise Refusal("A18 exact predecessor/projection binding mismatch")
    custody.reauthenticate()
    return record


def _parent_identity(parent: Path, descriptor: int) -> tuple[int, int]:
    _require_canonical_path(parent / "placeholder", "A18 output")
    held = os.fstat(descriptor)
    try:
        named = os.stat(parent, follow_symlinks=False)
    except OSError as error:
        raise Refusal("A18 output parent changed") from error
    if (
        not stat.S_ISDIR(held.st_mode) or not stat.S_ISDIR(named.st_mode)
        or (held.st_dev, held.st_ino) != (named.st_dev, named.st_ino)
    ):
        raise Refusal("A18 output parent changed")
    return held.st_dev, held.st_ino


def _unlink_owned(parent_descriptor: int, name: str, identity: tuple[int, int]) -> bool:
    try:
        metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except FileNotFoundError:
        return False
    if (
        not stat.S_ISREG(metadata.st_mode)
        or (metadata.st_dev, metadata.st_ino) != identity
    ):
        return False
    os.unlink(name, dir_fd=parent_descriptor)
    return True


def _atomic_publish_once(destination: Path, raw: bytes, expected: Path) -> str:
    if destination != expected or not destination.is_absolute():
        raise Refusal("A18 output is not the exact successor path")
    _require_canonical_path(destination, "A18 output")
    parent = destination.parent
    parent_descriptor = os.open(
        parent,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    staging_descriptor = -1
    staging_name = f".{destination.name}.staging-{os.getpid()}-{os.urandom(12).hex()}"
    staging_identity: tuple[int, int] | None = None
    digest = hashlib.sha256(raw).hexdigest()
    try:
        _parent_identity(parent, parent_descriptor)
        try:
            os.stat(destination.name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Refusal("A18 successor already exists")
        staging_descriptor = os.open(
            staging_name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400, dir_fd=parent_descriptor,
        )
        staged = os.fstat(staging_descriptor)
        staging_identity = (staged.st_dev, staged.st_ino)
        offset = 0
        while offset < len(raw):
            written = os.write(staging_descriptor, raw[offset:])
            if written <= 0:
                raise Refusal("A18 staging write made no progress")
            offset += written
        os.fsync(staging_descriptor)
        os.fchmod(staging_descriptor, 0o444)
        os.fsync(staging_descriptor)
        staged = os.fstat(staging_descriptor)
        if (
            not stat.S_ISREG(staged.st_mode) or staged.st_mode & 0o222
            or staged.st_nlink != 1 or staged.st_size != len(raw)
            or (staged.st_dev, staged.st_ino) != staging_identity
            or _descriptor_sha256(staging_descriptor) != digest
        ):
            raise Refusal("A18 staging authentication mismatch")
        _parent_identity(parent, parent_descriptor)
        try:
            os.link(
                staging_name, destination.name, src_dir_fd=parent_descriptor,
                dst_dir_fd=parent_descriptor, follow_symlinks=False,
            )
        except FileExistsError as error:
            raise Refusal("A18 successor appeared before commit") from error
        _parent_identity(parent, parent_descriptor)
        committed = os.open(
            destination.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_descriptor,
        )
        try:
            committed_metadata = os.fstat(committed)
            staged_metadata = os.fstat(staging_descriptor)
            named_metadata = os.stat(
                destination.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(committed_metadata.st_mode)
                or committed_metadata.st_mode & 0o222
                or committed_metadata.st_nlink != 2
                or (committed_metadata.st_dev, committed_metadata.st_ino)
                != staging_identity
                or _identity(committed_metadata) != _identity(staged_metadata)
                or _identity(committed_metadata) != _identity(named_metadata)
                or committed_metadata.st_size != len(raw)
                or _descriptor_sha256(committed) != digest
            ):
                raise Refusal("A18 committed hard-link authentication mismatch")
        finally:
            os.close(committed)
        if not _unlink_owned(parent_descriptor, staging_name, staging_identity):
            raise Refusal("A18 staging custody changed after commit")
        try:
            os.stat(staging_name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Refusal("A18 staging name survived commit")
        os.fsync(parent_descriptor)
        _parent_identity(parent, parent_descriptor)
        final = os.open(
            destination.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_descriptor,
        )
        try:
            metadata = os.fstat(final)
            named = os.stat(
                destination.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o222
                or metadata.st_nlink != 1 or _identity(metadata) != _identity(named)
                or metadata.st_size != len(raw)
                or _descriptor_sha256(final) != digest
            ):
                raise Refusal("published A18 successor custody mismatch")
        finally:
            os.close(final)
        return digest
    except BaseException:
        if staging_identity is not None:
            _unlink_owned(parent_descriptor, staging_name, staging_identity)
        raise
    finally:
        if staging_descriptor >= 0:
            os.close(staging_descriptor)
        os.close(parent_descriptor)


def construct_a18_candidate(custody: PredecessorCustody) -> dict[str, object]:
    record = copy.deepcopy(custody.candidate)
    return validate_a18(record, custody)


def publish_a18() -> str:
    """Publish once in the successor namespace; never writes a V012 path."""
    with PredecessorCustody() as custody:
        record = construct_a18_candidate(custody)
        custody.reauthenticate()
        digest = _atomic_publish_once(
            CANONICAL_SUCCESSOR_A18, publication_json_bytes(record),
            CANONICAL_SUCCESSOR_A18,
        )
        custody.reauthenticate()
        output = StableInput(CANONICAL_SUCCESSOR_A18, digest, "A18 successor")
        try:
            output.open(json_record=True)
            if output.record is None:
                raise Refusal("published A18 successor record absent")
            validate_a18(output.record, custody)
            output.reauthenticate()
        finally:
            output.close()
        return digest


def consume_a18(expected_sha256: str) -> dict[str, object]:
    """Authenticate the successor A18 for a later, separately authorized stage."""
    with PredecessorCustody() as custody:
        output = StableInput(
            CANONICAL_SUCCESSOR_A18, expected_sha256, "A18 successor",
        )
        try:
            output.open(json_record=True)
            if output.record is None:
                raise Refusal("A18 successor record absent")
            accepted = validate_a18(output.record, custody)
            output.reauthenticate()
            custody.reauthenticate()
            return accepted
        finally:
            output.close()


def downstream_executability_report() -> dict[str, object]:
    """Authenticate why the frozen A20--worker chain cannot use this path.

    A20 and A21 are content-addressed to an A18 digest, but no such records are
    currently published.  More importantly, the frozen production launcher and
    both frozen workers name the old shared A18 path, while the target worker
    invokes the contradictory frozen A18 obligation.  An A18-only amendment
    therefore cannot honestly authorize or launch L12.  This function retains
    those exact executable bytes while deriving that bounded result.
    """
    specifications = (
        (
            "target worker", FROZEN_TARGET_WORKER,
            FROZEN_TARGET_WORKER_SHA256,
        ),
        (
            "hostile worker", FROZEN_HOSTILE_WORKER,
            FROZEN_HOSTILE_WORKER_SHA256,
        ),
        (
            "dual launcher", FROZEN_DUAL_LAUNCHER,
            FROZEN_DUAL_LAUNCHER_SHA256,
        ),
    )
    retained: list[StableInput] = []
    try:
        if any(path.exists() or path.is_symlink() for path in (FROZEN_A20, FROZEN_A21)):
            raise Refusal("unreviewed A20/A21 record exists at the frozen chain path")
        for label, path, digest in specifications:
            item = StableInput(path, digest, label)
            item.open(json_record=False)
            retained.append(item)
        by_label = {item.label: item for item in retained}
        target_raw = by_label["target worker"].raw
        hostile_raw = by_label["hostile worker"].raw
        launcher_raw = by_label["dual launcher"].raw
        required_target_tokens = (
            OLD_A18_RELATIVE_PATH,
            b'builder.validate_production_obligation(',
            b'"A18_L10_CROSS_GATE", record',
        )
        if any(token not in target_raw for token in required_target_tokens):
            raise Refusal("frozen target A18 dependency signature changed")
        if OLD_A18_RELATIVE_PATH not in hostile_raw:
            raise Refusal("frozen hostile A18 path signature changed")
        if OLD_A18_RELATIVE_PATH not in launcher_raw:
            raise Refusal("frozen launcher A18 path signature changed")
        for item in retained:
            item.reauthenticate()
        return {
            "classification": "INCOMPLETE_FAIL_CLOSED_BEFORE_A20_A21_OR_L12",
            "a20_a21_status": "ABSENT_AND_NOT_AUTHORIZED_BY_THIS_AMENDMENT",
            "successor_a18_path": str(CANONICAL_SUCCESSOR_A18),
            "frozen_chain_a18_path": (
                "AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
                "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
            ),
            "frozen_source_sha256": {
                "target_worker": FROZEN_TARGET_WORKER_SHA256,
                "hostile_worker": FROZEN_HOSTILE_WORKER_SHA256,
                "dual_launcher": FROZEN_DUAL_LAUNCHER_SHA256,
            },
            "obstruction": (
                "FROZEN_LAUNCHER_AND_WORKERS_NAME_OLD_A18_PATH__TARGET_WORKER_"
                "ALSO_INVOKES_CONTRADICTORY_FROZEN_A18_VALIDATOR"
            ),
            "minimum_successor_required": (
                "SEPARATELY_PREREGISTERED_A20_A21_A22_AND_LAUNCH_WORKER_"
                "CONTROL_PLANE_BOUND_TO_SUCCESSOR_A18"
            ),
            "claim_boundary": AMENDMENT_CLAIM,
        }
    finally:
        for item in reversed(retained):
            item.close()


def require_downstream_executable() -> None:
    """Refuse any attempt to treat the A18-only amendment as L12 authority."""
    report = downstream_executability_report()
    raise Refusal(
        "successor A18 is not downstream executable: "
        + str(report["obstruction"])
    )
