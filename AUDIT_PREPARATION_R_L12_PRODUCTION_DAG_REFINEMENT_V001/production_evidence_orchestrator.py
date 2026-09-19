#!/usr/bin/env python3
"""Fail-closed A23/A26/A27 production evidence orchestration.

This module does not launch either L12 worker. It retains immutable A23--A25
and A27 inputs, then permits A26 validation and one-time atomic publication.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Final


PREDECESSOR_IDS: Final[tuple[str, ...]] = (
    "A23_POSTRUN_TELEMETRY", "A24_TARGET_L12_HISTORY",
    "A25_HOSTILE_L12_HISTORY", "A27_MUTATION_LEDGER",
)
ROOT: Final[Path] = Path(__file__).resolve().parent.parent
CANONICAL_PREDECESSOR_PATHS: dict[str, str] = {
    "A23_POSTRUN_TELEMETRY": str(
        ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json"
    ),
    "A24_TARGET_L12_HISTORY": str(
        ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json"
    ),
    "A25_HOSTILE_L12_HISTORY": str(
        ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json"
    ),
    "A27_MUTATION_LEDGER": str(
        ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_MUTATION_LEDGER_V001.json"
    ),
}
CANONICAL_OUTPUT_PATHS: dict[str, str] = {
    "A23_POSTRUN_TELEMETRY": CANONICAL_PREDECESSOR_PATHS[
        "A23_POSTRUN_TELEMETRY"
    ],
    "A27_MUTATION_LEDGER": CANONICAL_PREDECESSOR_PATHS[
        "A27_MUTATION_LEDGER"
    ],
    "A26_FINAL_L12_AUDIT": str(
        ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/FINAL_L12_TARGET_HOSTILE_AUDIT_V001.json"
    ),
}


class OrchestrationRefusal(RuntimeError):
    """Production evidence could not be authenticated or ordered."""


def canonical_json_bytes(record: object) -> bytes:
    try:
        return (json.dumps(
            record, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise OrchestrationRefusal("noncanonical/nonfinite record") from error


def _descriptor_sha256(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while block := os.pread(descriptor, 16 * 2**20, offset):
        digest.update(block)
        offset += len(block)
    return digest.hexdigest()


def _complete_identity(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        stat.S_IMODE(metadata.st_mode),
    )


def _descriptor_bytes(descriptor: int, size: int) -> bytes:
    if type(size) is not int or size < 0:
        raise OrchestrationRefusal("authority descriptor size is invalid")
    result = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(descriptor, min(16 * 2**20, size - offset), offset)
        if not block:
            raise OrchestrationRefusal("authority descriptor read was short")
        result.extend(block)
        offset += len(block)
    return bytes(result)


def _canonical_absolute_path(value: object, label: str) -> Path:
    if (
        type(value) is not str or not value.startswith("/") or "\x00" in value
        or os.path.normpath(value) != value or str(Path(value)) != value
    ):
        raise OrchestrationRefusal(f"{label} path malformed")
    return Path(value)


def _require_no_symlink_parents(path: Path, label: str) -> None:
    current = Path(path.anchor)
    for part in path.parts[1:-1]:
        current /= part
        try:
            metadata = os.stat(current, follow_symlinks=False)
        except OSError as error:
            raise OrchestrationRefusal(f"{label} parent is absent") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise OrchestrationRefusal(f"{label} parent is aliased/special")


def _parent_identity(parent: Path, descriptor: int, label: str) -> tuple[int, int]:
    _require_no_symlink_parents(parent / "placeholder", label)
    held = os.fstat(descriptor)
    try:
        current = os.stat(parent, follow_symlinks=False)
    except OSError as error:
        raise OrchestrationRefusal(f"{label} canonical parent changed") from error
    if (
        not stat.S_ISDIR(held.st_mode) or not stat.S_ISDIR(current.st_mode)
        or stat.S_ISLNK(current.st_mode)
        or (held.st_dev, held.st_ino) != (current.st_dev, current.st_ino)
    ):
        raise OrchestrationRefusal(f"{label} canonical parent changed")
    return held.st_dev, held.st_ino


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


def _atomic_publish_once(
    output: str, payload: bytes, expected_output: str,
) -> str:
    destination = _canonical_absolute_path(output, "evidence output")
    if output != expected_output:
        raise OrchestrationRefusal("evidence output is not the canonical artifact path")
    _require_no_symlink_parents(destination, "evidence output")
    parent = destination.parent
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(parent, parent_flags)
    except OSError as error:
        raise OrchestrationRefusal("evidence parent directory is absent or aliased") from error
    descriptor = -1
    staging_name = f".{destination.name}.staging-{os.getpid()}-{os.urandom(12).hex()}"
    staging_identity: tuple[int, int] | None = None
    expected = hashlib.sha256(payload).hexdigest()
    try:
        _parent_identity(parent, parent_descriptor, "evidence output")
        try:
            os.stat(
                destination.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            pass
        else:
            raise OrchestrationRefusal("evidence destination already exists")
        descriptor = os.open(
            staging_name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400, dir_fd=parent_descriptor,
        )
        opened = os.fstat(descriptor)
        staging_identity = (opened.st_dev, opened.st_ino)
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            if written <= 0:
                raise OrchestrationRefusal("short evidence write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        sealed = os.fstat(descriptor)
        if (
            not stat.S_ISREG(sealed.st_mode) or sealed.st_mode & 0o222
            or sealed.st_nlink != 1 or sealed.st_size != len(payload)
            or (sealed.st_dev, sealed.st_ino) != staging_identity
            or _descriptor_sha256(descriptor) != expected
        ):
            raise OrchestrationRefusal("evidence staging authentication failed")
        _parent_identity(parent, parent_descriptor, "evidence output")
        try:
            os.link(
                staging_name, destination.name,
                src_dir_fd=parent_descriptor, dst_dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileExistsError as error:
            raise OrchestrationRefusal(
                "evidence destination appeared before no-clobber commit"
            ) from error
        canonical = os.open(
            destination.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_descriptor,
        )
        try:
            linked = os.fstat(canonical)
            if (
                not stat.S_ISREG(linked.st_mode) or linked.st_mode & 0o222
                or linked.st_nlink != 2
                or (linked.st_dev, linked.st_ino) != staging_identity
                or _descriptor_sha256(canonical) != expected
            ):
                raise OrchestrationRefusal(
                    "evidence canonical link authentication failed"
                )
        finally:
            os.close(canonical)
        if not _unlink_owned_at(
            parent_descriptor, staging_name, staging_identity,
        ):
            raise OrchestrationRefusal("evidence staging custody changed after link")
        os.fsync(parent_descriptor)
        _parent_identity(parent, parent_descriptor, "evidence output")
        verify_fd = os.open(
            destination.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_descriptor,
        )
        try:
            metadata = os.fstat(verify_fd)
            path_metadata = os.stat(
                destination.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o222
                or metadata.st_nlink != 1 or metadata.st_size != len(payload)
                or (metadata.st_dev, metadata.st_ino) != staging_identity
                or (path_metadata.st_dev, path_metadata.st_ino)
                != staging_identity
                or _descriptor_sha256(verify_fd) != expected
            ):
                raise OrchestrationRefusal("published evidence custody mismatch")
        finally:
            os.close(verify_fd)
        return expected
    except BaseException:
        if staging_identity is not None:
            _unlink_owned_at(parent_descriptor, staging_name, staging_identity)
        # Never delete the canonical name after the no-clobber link.  A
        # post-link failure remains durable evidence and forces retry refusal.
        raise
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(parent_descriptor)


class StageEvidencePublisher:
    """Create A23 and A27 once through their exact live validation sinks."""

    def __init__(self, validator: Callable[..., dict[str, object]]):
        if not callable(validator):
            raise OrchestrationRefusal("validator must be callable")
        self._validator = validator
        self._published: set[str] = set()

    def publish_a23(
        self, output: str, record: dict[str, object], coordinator: object,
    ) -> str:
        if "A23_POSTRUN_TELEMETRY" in self._published:
            raise OrchestrationRefusal("A23 has already been published")
        try:
            stage = coordinator.stage
            accepted = coordinator.accepted_record("telemetry")
            accepted_sha = coordinator.accepted_sha256("telemetry")
        except (AttributeError, TypeError, RuntimeError) as error:
            raise OrchestrationRefusal("A23 coordinator authority absent") from error
        payload = canonical_json_bytes(record)
        if (
            stage != "TELEMETRY_ACCEPTED" or accepted != record
            or accepted_sha != hashlib.sha256(payload).hexdigest()
        ):
            raise OrchestrationRefusal("A23 is not the coordinator-accepted telemetry")
        self._validator("A23_POSTRUN_TELEMETRY", record, fixture_mode=False)
        digest = _atomic_publish_once(
            output, payload, CANONICAL_OUTPUT_PATHS["A23_POSTRUN_TELEMETRY"],
        )
        self._published.add("A23_POSTRUN_TELEMETRY")
        return digest

    def publish_a27(self, output: str, record: dict[str, object]) -> str:
        if "A27_MUTATION_LEDGER" in self._published:
            raise OrchestrationRefusal("A27 has already been published")
        self._validator("A27_MUTATION_LEDGER", record, fixture_mode=False)
        digest = _atomic_publish_once(
            output, canonical_json_bytes(record),
            CANONICAL_OUTPUT_PATHS["A27_MUTATION_LEDGER"],
        )
        self._published.add("A27_MUTATION_LEDGER")
        return digest


@dataclass
class RetainedAuthority:
    artifact_id: str
    path: str
    digest: str
    descriptor: int
    identity: tuple[int, int, int, int, int, int, int]
    parent_descriptor: int
    parent_identity: tuple[int, int]
    record: dict[str, object]

    def verify(self) -> None:
        path = Path(self.path)
        _require_no_symlink_parents(path, f"retained {self.artifact_id}")
        if _parent_identity(
            path.parent, self.parent_descriptor,
            f"retained {self.artifact_id}",
        ) != self.parent_identity:
            raise OrchestrationRefusal(
                f"retained authority parent drift: {self.artifact_id}"
            )
        metadata_before = os.fstat(self.descriptor)
        try:
            current_before = os.stat(
                path.name, dir_fd=self.parent_descriptor,
                follow_symlinks=False,
            )
        except OSError as error:
            raise OrchestrationRefusal(
                f"retained authority path drift: {self.artifact_id}"
            ) from error
        observed_digest = _descriptor_sha256(self.descriptor)
        metadata_after = os.fstat(self.descriptor)
        try:
            current_after = os.stat(
                path.name, dir_fd=self.parent_descriptor,
                follow_symlinks=False,
            )
        except OSError as error:
            raise OrchestrationRefusal(
                f"retained authority path drift: {self.artifact_id}"
            ) from error
        if _parent_identity(
            path.parent, self.parent_descriptor,
            f"retained {self.artifact_id}",
        ) != self.parent_identity:
            raise OrchestrationRefusal(
                f"retained authority parent drift: {self.artifact_id}"
            )
        if (
            _complete_identity(metadata_before) != self.identity
            or _complete_identity(current_before) != self.identity
            or _complete_identity(metadata_after) != self.identity
            or _complete_identity(current_after) != self.identity
            or not stat.S_ISREG(metadata_before.st_mode)
            or not stat.S_ISREG(current_before.st_mode)
            or observed_digest != self.digest
        ):
            raise OrchestrationRefusal(f"retained authority drift: {self.artifact_id}")

    def close(self) -> None:
        if self.descriptor >= 0:
            os.close(self.descriptor)
            self.descriptor = -1
        if self.parent_descriptor >= 0:
            os.close(self.parent_descriptor)
            self.parent_descriptor = -1


def open_authority(
    artifact_id: str, path: str, digest: str,
    validator: Callable[..., dict[str, object]],
) -> RetainedAuthority:
    if artifact_id not in PREDECESSOR_IDS:
        raise OrchestrationRefusal("unknown final predecessor id")
    canonical = _canonical_absolute_path(path, "authority")
    if (
        path != CANONICAL_PREDECESSOR_PATHS[artifact_id]
        or type(digest) is not str or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
    ):
        raise OrchestrationRefusal("authority canonical path/hash mismatch")
    _require_no_symlink_parents(canonical, f"authority {artifact_id}")
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(canonical.parent, parent_flags)
    except OSError as error:
        raise OrchestrationRefusal("authority parent open refused") from error
    try:
        parent_identity = _parent_identity(
            canonical.parent, parent_descriptor, f"authority {artifact_id}",
        )
    except BaseException:
        os.close(parent_descriptor)
        raise
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(
            canonical.name, flags, dir_fd=parent_descriptor,
        )
    except OSError as error:
        os.close(parent_descriptor)
        raise OrchestrationRefusal("authority open refused") from error
    try:
        metadata = os.fstat(descriptor)
        current = os.stat(
            canonical.name, dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o222
            or metadata.st_nlink != 1
            or (
                metadata.st_dev, metadata.st_ino, metadata.st_size,
                metadata.st_mtime_ns, metadata.st_ctime_ns,
                metadata.st_nlink, stat.S_IMODE(metadata.st_mode),
            ) != (
                current.st_dev, current.st_ino, current.st_size,
                current.st_mtime_ns, current.st_ctime_ns,
                current.st_nlink, stat.S_IMODE(current.st_mode),
            )
        ):
            raise OrchestrationRefusal("authority is symlinked/writable/special")
        observed_digest = _descriptor_sha256(descriptor)
        if observed_digest != digest:
            raise OrchestrationRefusal("authority descriptor hash mismatch")
        raw = _descriptor_bytes(descriptor, metadata.st_size)
        metadata_after = os.fstat(descriptor)
        current_after = os.stat(
            canonical.name, dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if (
            _complete_identity(metadata_after) != _complete_identity(metadata)
            or _complete_identity(current_after) != _complete_identity(metadata)
            or hashlib.sha256(raw).hexdigest() != digest
            or _parent_identity(
                canonical.parent, parent_descriptor, f"authority {artifact_id}",
            ) != parent_identity
        ):
            raise OrchestrationRefusal("authority changed during authentication")
        try:
            record = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            raise OrchestrationRefusal("authority JSON malformed") from error
        if type(record) is not dict or canonical_json_bytes(record) != raw:
            raise OrchestrationRefusal("authority is not exact canonical JSON")
        validator(artifact_id, record, fixture_mode=False)
        identity = _complete_identity(metadata)
        retained = RetainedAuthority(
            artifact_id, path, digest, descriptor, identity,
            parent_descriptor, parent_identity, record,
        )
        retained.verify()
        return retained
    except BaseException:
        os.close(descriptor)
        os.close(parent_descriptor)
        raise


class FinalEvidenceOrchestrator:
    """Retain the complete final predecessor set and publish A26 once."""

    def __init__(self, validator: Callable[..., dict[str, object]]):
        if not callable(validator):
            raise OrchestrationRefusal("validator must be callable")
        self._validator = validator
        self._accepted: dict[str, RetainedAuthority] = {}
        self._published = False

    @property
    def stage(self) -> str:
        if self._published:
            return "A26_PUBLISHED"
        if set(self._accepted) == set(PREDECESSOR_IDS):
            return "PREDECESSORS_RETAINED"
        return "PREDECESSORS_PARTIAL" if self._accepted else "EMPTY"

    def admit(self, artifact_id: str, path: str, digest: str) -> None:
        if artifact_id in self._accepted or self._published:
            raise OrchestrationRefusal("duplicate/out-of-order predecessor")
        self._accepted[artifact_id] = open_authority(
            artifact_id, path, digest, self._validator,
        )

    def publish_a26(self, output: str, record: dict[str, object]) -> str:
        if self.stage != "PREDECESSORS_RETAINED":
            raise OrchestrationRefusal("A26 requires A23-A25 and A27")
        if output != CANONICAL_OUTPUT_PATHS["A26_FINAL_L12_AUDIT"]:
            raise OrchestrationRefusal("A26 output path is not canonical")
        for retained in self._accepted.values():
            retained.verify()
        self._validator("A26_FINAL_L12_AUDIT", record, fixture_mode=False)
        for retained in self._accepted.values():
            retained.verify()
        payload = canonical_json_bytes(record)
        digest = _atomic_publish_once(
            output, payload, CANONICAL_OUTPUT_PATHS["A26_FINAL_L12_AUDIT"],
        )
        for retained in self._accepted.values():
            retained.verify()
        self._published = True
        return digest

    def close(self) -> None:
        first_error: BaseException | None = None
        for retained in self._accepted.values():
            try:
                retained.close()
            except BaseException as error:
                if first_error is None:
                    first_error = error
        if first_error is not None:
            raise first_error

    def __enter__(self) -> "FinalEvidenceOrchestrator":
        return self

    def __exit__(self, *_error: object) -> None:
        self.close()
