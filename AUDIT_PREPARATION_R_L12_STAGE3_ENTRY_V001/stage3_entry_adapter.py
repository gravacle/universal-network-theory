#!/usr/bin/env python3
"""Prepare and publish the exact A20/A21/two-A22 Stage-3 entry records.

The adapter performs no physics and never launches a worker.  ``fixture`` and
``dry-run`` do not publish.  ``publish`` is the only mutating mode and is
owner-once: all four records are constructed and validated before the first
canonical name is created, then each canonical byte string is linked into
place without replacement through the already frozen publication primitive.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
import types
from contextlib import contextmanager
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import ClassVar, Final, Iterable


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
COORDINATOR_PACKET: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001"
)
FINAL_PACKET: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
)
TARGET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
SHARED: Final[Path] = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
SOURCE_FREEZE: Final[Path] = HERE / "SOURCE_FREEZE.json"
PACKET_FILE_NAMES: Final[frozenset[str]] = frozenset({
    "README.md", "independent_a20_auditor.py", "stage3_entry_adapter.py",
    "test_stage3_entry_adapter.py", "production_dual_l12_launcher_candidate.py",
})
LAUNCHER_CANDIDATE: Final[Path] = (
    HERE / "production_dual_l12_launcher_candidate.py"
)
TRANSITIVE_DEPENDENCY_SHA256: Final[dict[Path, str]] = {
    COORDINATOR_PACKET / "dual_launch_coordinator.py":
        "9f70c3b05dfd9ca0045858f43065d6958872a066551ff74e899eb0a19b496af7",
    LAUNCHER_CANDIDATE:
        "e4a170df60c32a7be9e2583304e666bf40f53e0a1161d014ece18f4c12553acb",
    FINAL_PACKET / "production_evidence_orchestrator.py":
        "d85275417f92961a2809822bcfc635d9e23e16bc7ad4fde43183ddcb78620b20",
    FINAL_PACKET / "independent_final_auditor.py":
        "cb1681c870b8382d9e7a83bec9df0830699d7b1015ed19b24360a3dbd4ae207e",
    TARGET / "production_obligation_validators.py":
        "c1a0b6d8a39dc418523d988ddd97a5a30234cee4923efac654ab3ab48d7a93f7",
    HERE / "independent_a20_auditor.py":
        "9074ef86d28457f93db9976615639a5a6915dbcae8c6db505aa61d2bc82f7b25",
}
TRANSITIVE_MODULE_ORDER: Final[tuple[tuple[str, Path], ...]] = (
    ("dual_launch_coordinator", COORDINATOR_PACKET / "dual_launch_coordinator.py"),
    ("production_evidence_orchestrator", FINAL_PACKET / "production_evidence_orchestrator.py"),
    ("independent_final_auditor", FINAL_PACKET / "independent_final_auditor.py"),
    ("production_dual_l12_launcher", LAUNCHER_CANDIDATE),
    ("production_obligation_validators", TARGET / "production_obligation_validators.py"),
    ("independent_a20_auditor", HERE / "independent_a20_auditor.py"),
)

L10_CROSS_GATE: Final[Path] = SHARED / "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
TARGET_EXECUTABLE: Final[Path] = TARGET / "consume_target_cache.py"
HOSTILE_EXECUTABLE: Final[Path] = HOSTILE / "consume_cache_v004r4.py"
TARGET_CACHE_MANIFEST: Final[Path] = (
    TARGET / "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json"
)
HOSTILE_CACHE_MANIFEST: Final[Path] = (
    HOSTILE / "V004R4_CACHE_PAYLOADS/L12/CACHE_MANIFEST.json"
)
TARGET_WORKSPACE: Final[Path] = TARGET / "WORKSPACES/L12"
HOSTILE_WORKSPACE: Final[Path] = HOSTILE / "V004R4_WORKSPACES/L12"
TARGET_OUTPUT: Final[Path] = TARGET / "PHYSICAL_OUTPUTS/HISTORY_L12.json"
HOSTILE_OUTPUT: Final[Path] = (
    HOSTILE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json"
)
TELEMETRY: Final[Path] = SHARED / "SHARED_AGGREGATE_TELEMETRY_V001.json"
SCHEDULE: Final[Path] = SHARED / "SHARED_AGGREGATE_SCHEDULE_GATE_V001.json"
SCHEDULE_AUDIT: Final[Path] = (
    SHARED / "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json"
)
TARGET_AUTHORIZATION: Final[Path] = TARGET / "TARGET_L12_EXECUTION_GATE_V012.json"
HOSTILE_AUTHORIZATION: Final[Path] = (
    HOSTILE / "HOSTILE_L12_EXECUTION_GATE_V004R4.json"
)
OUTPUT_PATHS: Final[tuple[Path, ...]] = (
    SCHEDULE, SCHEDULE_AUDIT, TARGET_AUTHORIZATION, HOSTILE_AUTHORIZATION,
)
PRELAUNCH_ABSENCES: Final[tuple[Path, ...]] = (
    *OUTPUT_PATHS, TARGET_WORKSPACE, HOSTILE_WORKSPACE, TARGET_OUTPUT,
    HOSTILE_OUTPUT, TELEMETRY,
)
EXECUTION_ABSENCES: Final[tuple[Path, ...]] = (
    TARGET_WORKSPACE, HOSTILE_WORKSPACE, TARGET_OUTPUT, HOSTILE_OUTPUT,
    TELEMETRY,
)
DESTINATION_PARENT_CENSUS: Final[tuple[Path, ...]] = tuple(dict.fromkeys((
    *OUTPUT_PATHS, TARGET_WORKSPACE, HOSTILE_WORKSPACE, TARGET_OUTPUT,
    HOSTILE_OUTPUT, TELEMETRY,
)))
LAUNCH_WIRE_PATHS: Final[dict[str, Path]] = {
    "ready:target_v012": SHARED / "TARGET_V012_WORKER_READY_V001.json",
    "ready:hostile_v004r4": SHARED / "HOSTILE_V004R4_WORKER_READY_V001.json",
    "handshake": SHARED / "DUAL_L12_LAUNCH_HANDSHAKE_V002.json",
    "release": SHARED / "DUAL_L12_WORKER_RELEASE_V002.json",
    "command:target_v012": SHARED / "TARGET_V012_WORKER_RELEASE_COMMAND_V001.json",
    "command:hostile_v004r4": SHARED / "HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json",
    "ack:target_v012": SHARED / "TARGET_V012_WORKER_RELEASE_ACK_V001.json",
    "ack:hostile_v004r4": SHARED / "HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
    "completion:target_v012": SHARED / "TARGET_V012_WORKER_COMPLETION_V001.json",
    "completion:hostile_v004r4": SHARED / "HOSTILE_V004R4_WORKER_COMPLETION_V001.json",
    "telemetry": TELEMETRY,
}
LAUNCH_LOG_PATHS: Final[tuple[Path, ...]] = tuple(
    SHARED / f"{role.upper()}_WORKER_LOG_V001.txt"
    for role in ("target_v012", "hostile_v004r4")
)
LAUNCH_DESTINATIONS: Final[tuple[Path, ...]] = tuple(dict.fromkeys((
    *LAUNCH_WIRE_PATHS.values(), *LAUNCH_LOG_PATHS,
    TARGET_WORKSPACE, HOSTILE_WORKSPACE, TARGET_OUTPUT, HOSTILE_OUTPUT,
)))
MAPPED_CERTIFICATE: Final[int] = 252_944_080
MEMORY_PRESSURE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"The system has ([1-9][0-9]*) \(([1-9][0-9]*) pages with a page size of "
    r"([1-9][0-9]*)\)\.\nSystem-wide memory free percentage: "
    r"([0-9]{1,3})%\n?"
)


class EntryRefusal(RuntimeError):
    """The Stage-3 entry boundary refused without launching workers."""


def _reject_constant(value: str) -> object:
    raise EntryRefusal(f"nonfinite source-freeze JSON constant: {value}")


def _object_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise EntryRefusal(f"duplicate source-freeze JSON key: {key}")
        result[key] = value
    return result


def _strict_json(raw: bytes, label: str) -> dict[str, object]:
    try:
        value = json.loads(
            raw, object_pairs_hook=_object_no_duplicates,
            parse_float=Decimal, parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise EntryRefusal(f"{label} is not strict JSON") from error
    if type(value) is not dict:
        raise EntryRefusal(f"{label} is not an object")
    return value


def _source_identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_mode,
        metadata.st_nlink,
    )


@dataclass
class AuthenticatedSource:
    path: Path
    descriptor: int
    parent_descriptor: int
    identity: tuple[int, ...]
    parent_identity: tuple[int, int, int]
    raw: bytes
    sha256: str

    @classmethod
    def open(cls, path: Path, expected_sha256: str | None, label: str) -> "AuthenticatedSource":
        root = ROOT.resolve()
        if (
            not path.is_absolute() or root not in path.parents
            or Path(str(path)) != path or "\x00" in str(path)
        ):
            raise EntryRefusal(f"{label}: path is outside the canonical repository")
        cursor = root
        for component in path.relative_to(root).parts[:-1]:
            cursor /= component
            metadata = os.stat(cursor, follow_symlinks=False)
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                raise EntryRefusal(f"{label}: parent is aliased or special")
        parent_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        file_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        parent_descriptor = os.open(path.parent, parent_flags)
        descriptor = -1
        try:
            parent = os.fstat(parent_descriptor)
            parent_named = os.stat(path.parent, follow_symlinks=False)
            parent_identity = (parent.st_dev, parent.st_ino, parent.st_mode)
            if parent_identity != (
                parent_named.st_dev, parent_named.st_ino, parent_named.st_mode,
            ):
                raise EntryRefusal(f"{label}: parent identity mismatch")
            descriptor = os.open(path.name, file_flags, dir_fd=parent_descriptor)
            before = os.fstat(descriptor)
            named = os.stat(path.name, dir_fd=parent_descriptor, follow_symlinks=False)
            identity = _source_identity(before)
            if (
                not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
                or before.st_mode & 0o222 or before.st_nlink != 1
                or identity != _source_identity(named)
            ):
                raise EntryRefusal(f"{label}: immutable source custody mismatch")
            chunks: list[bytes] = []
            offset = 0
            while offset < before.st_size:
                block = os.pread(
                    descriptor, min(1024 * 1024, before.st_size - offset), offset,
                )
                if not block:
                    raise EntryRefusal(f"{label}: short source read")
                chunks.append(block)
                offset += len(block)
            raw = b"".join(chunks)
            digest = hashlib.sha256(raw).hexdigest()
            after = os.fstat(descriptor)
            named_after = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
            if (
                _source_identity(after) != identity
                or _source_identity(named_after) != identity
                or (expected_sha256 is not None and digest != expected_sha256)
            ):
                raise EntryRefusal(f"{label}: retained source/hash mismatch")
            return cls(
                path, descriptor, parent_descriptor, identity,
                parent_identity, raw, digest,
            )
        except BaseException:
            if descriptor >= 0:
                os.close(descriptor)
            os.close(parent_descriptor)
            raise

    def verify(self) -> None:
        held = os.fstat(self.descriptor)
        named = os.stat(
            self.path.name, dir_fd=self.parent_descriptor,
            follow_symlinks=False,
        )
        parent = os.fstat(self.parent_descriptor)
        parent_named = os.stat(self.path.parent, follow_symlinks=False)
        if (
            _source_identity(held) != self.identity
            or _source_identity(named) != self.identity
            or (parent.st_dev, parent.st_ino, parent.st_mode) != self.parent_identity
            or (parent_named.st_dev, parent_named.st_ino, parent_named.st_mode)
            != self.parent_identity
            or hashlib.sha256(self.raw).hexdigest() != self.sha256
        ):
            raise EntryRefusal(f"retained source changed: {self.path}")

    def close(self) -> None:
        os.close(self.descriptor)
        os.close(self.parent_descriptor)
        self.descriptor = -1
        self.parent_descriptor = -1


@dataclass
class RetainedDestinationCensus:
    """Stable no-follow authority over every Stage3/launch destination parent."""

    parents: dict[Path, tuple[int, tuple[int, int, int]]]

    @classmethod
    def open(cls, destinations: tuple[Path, ...]) -> "RetainedDestinationCensus":
        if not destinations:
            raise EntryRefusal("destination-parent census is empty")
        opened: dict[Path, tuple[int, tuple[int, int, int]]] = {}
        try:
            for destination in destinations:
                if (
                    not destination.is_absolute() or ROOT not in destination.parents
                    or Path(str(destination)) != destination
                ):
                    raise EntryRefusal("destination is outside canonical repository")
                parent = destination.parent
                if parent in opened:
                    continue
                cursor = ROOT
                for component in parent.relative_to(ROOT).parts:
                    cursor /= component
                    metadata = os.stat(cursor, follow_symlinks=False)
                    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                        raise EntryRefusal("destination parent is aliased or special")
                flags = (
                    os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                    | getattr(os, "O_DIRECTORY", 0)
                    | getattr(os, "O_NOFOLLOW", 0)
                )
                descriptor = os.open(parent, flags)
                held = os.fstat(descriptor)
                named = os.stat(parent, follow_symlinks=False)
                identity = (held.st_dev, held.st_ino, held.st_mode)
                if (
                    not stat.S_ISDIR(held.st_mode) or stat.S_ISLNK(named.st_mode)
                    or identity != (named.st_dev, named.st_ino, named.st_mode)
                ):
                    os.close(descriptor)
                    raise EntryRefusal("destination parent identity mismatch")
                opened[parent] = (descriptor, identity)
            result = cls(opened)
            result.verify_parents()
            if len(result.devices()) != 1:
                raise EntryRefusal("destination parents span filesystems")
            return result
        except BaseException:
            for descriptor, _identity_value in opened.values():
                os.close(descriptor)
            raise

    def verify_parents(self) -> None:
        for path, (descriptor, identity) in self.parents.items():
            held = os.fstat(descriptor)
            named = os.stat(path, follow_symlinks=False)
            if (
                not stat.S_ISDIR(held.st_mode) or stat.S_ISLNK(named.st_mode)
                or (held.st_dev, held.st_ino, held.st_mode) != identity
                or (named.st_dev, named.st_ino, named.st_mode) != identity
            ):
                raise EntryRefusal("retained destination parent changed")

    def devices(self) -> set[int]:
        self.verify_parents()
        return {os.fstat(descriptor).st_dev for descriptor, _identity in self.parents.values()}

    def require_absent(self, destinations: tuple[Path, ...], label: str) -> None:
        self.verify_parents()
        for destination in destinations:
            retained = self.parents.get(destination.parent)
            if retained is None:
                raise EntryRefusal(f"{label}: destination parent was not retained")
            try:
                os.lstat(destination.name, dir_fd=retained[0])
            except FileNotFoundError:
                continue
            raise EntryRefusal(f"{label}: destination name is already present: {destination}")
        self.verify_parents()

    def leaf_metadata(self, destination: Path) -> os.stat_result | None:
        self.verify_parents()
        retained = self.parents.get(destination.parent)
        if retained is None:
            raise EntryRefusal("destination parent was not retained")
        try:
            metadata = os.lstat(destination.name, dir_fd=retained[0])
        except FileNotFoundError:
            return None
        if stat.S_ISLNK(metadata.st_mode):
            raise EntryRefusal(f"destination is a symlink: {destination}")
        return metadata

    def require_exact_names(
        self, destinations: tuple[Path, ...], present: frozenset[Path], label: str,
    ) -> None:
        if not present.issubset(frozenset(destinations)):
            raise EntryRefusal(f"{label}: expected-name set is outside census")
        for destination in destinations:
            metadata = self.leaf_metadata(destination)
            if destination in present:
                if metadata is None:
                    raise EntryRefusal(f"{label}: expected destination is absent: {destination}")
                if destination in (TARGET_WORKSPACE, HOSTILE_WORKSPACE):
                    valid = stat.S_ISDIR(metadata.st_mode)
                else:
                    valid = stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1
                if not valid:
                    raise EntryRefusal(f"{label}: expected destination is special: {destination}")
            elif metadata is not None:
                raise EntryRefusal(f"{label}: unexpected destination is present: {destination}")
        self.verify_parents()

    def filesystem_state(self) -> tuple[int, int]:
        devices = self.devices()
        if len(devices) != 1:
            raise EntryRefusal("retained destination filesystem changed")
        descriptor = next(iter(self.parents.values()))[0]
        filesystem = os.fstatvfs(descriptor)
        free = int(filesystem.f_bavail) * int(filesystem.f_frsize)
        if free < 0:
            raise EntryRefusal("retained free-disk result is invalid")
        return next(iter(devices)), free

    def close(self) -> None:
        failure: BaseException | None = None
        try:
            self.verify_parents()
        except BaseException as error:
            failure = error
        for descriptor, _identity in self.parents.values():
            os.close(descriptor)
        self.parents.clear()
        if failure is not None:
            raise failure


@dataclass
class Stage3ExecutionGuard:
    """Retained-parent capability required by the patched physical launcher."""

    census: RetainedDestinationCensus
    next_phase: int = 0

    PHASES: ClassVar[tuple[str, ...]] = (
        "initial", "pre_handshake", "pre_release", "final",
    )

    @classmethod
    def open(cls) -> "Stage3ExecutionGuard":
        return cls(RetainedDestinationCensus.open(LAUNCH_DESTINATIONS))

    def _expected(self, phase: str) -> frozenset[Path]:
        logs = frozenset(LAUNCH_LOG_PATHS)
        ready = frozenset({
            LAUNCH_WIRE_PATHS["ready:target_v012"],
            LAUNCH_WIRE_PATHS["ready:hostile_v004r4"],
        })
        if phase == "initial":
            return frozenset()
        if phase == "pre_handshake":
            return logs | ready
        if phase == "pre_release":
            return logs | ready | frozenset({LAUNCH_WIRE_PATHS["handshake"]})
        if phase == "final":
            return frozenset(LAUNCH_DESTINATIONS)
        raise EntryRefusal("unknown Stage3 execution-guard phase")

    def verify_phase(self, phase: str) -> None:
        if (
            self.next_phase >= len(self.PHASES)
            or phase != self.PHASES[self.next_phase]
        ):
            raise EntryRefusal("Stage3 execution-guard phase order mismatch")
        self.census.require_exact_names(
            LAUNCH_DESTINATIONS, self._expected(phase),
            f"Stage3 immediate {phase} name census",
        )
        self.next_phase += 1

    def disk_state(self) -> tuple[int, int]:
        if self.next_phase != 3:
            raise EntryRefusal("Stage3 disk custody sampled outside execution phase")
        return self.census.filesystem_state()

    def close(self) -> None:
        self.census.close()


@dataclass(frozen=True)
class FrozenRuntime:
    coordinator: types.ModuleType
    launcher: types.ModuleType
    evidence: types.ModuleType
    validators: types.ModuleType
    a20_auditor: types.ModuleType


_RUNTIME: FrozenRuntime | None = None


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _authenticate_source_closure() -> tuple[AuthenticatedSource, dict[Path, AuthenticatedSource]]:
    freeze_source = AuthenticatedSource.open(SOURCE_FREEZE, None, "Stage3 SOURCE_FREEZE")
    retained: dict[Path, AuthenticatedSource] = {}
    try:
        freeze = _strict_json(freeze_source.raw, "Stage3 SOURCE_FREEZE")
        if (
            freeze.get("schema")
            != "AUDIT_PREPARATION_R_L12_STAGE3_ENTRY_SOURCE_FREEZE_V002"
            or freeze.get("status") != "FROZEN_BEFORE_CANONICAL_A20_A22_PUBLICATION"
            or freeze.get("canonical_a20_a21_a22_records_published") is not False
            or freeze.get("canonical_worker_or_physical_output_created") is not False
        ):
            raise EntryRefusal("Stage3 SOURCE_FREEZE identity mismatch")
        packet_files = freeze.get("files")
        dependency_files = freeze.get("dependency_sha256")
        expected_dependencies = {
            _relative(path): digest
            for path, digest in TRANSITIVE_DEPENDENCY_SHA256.items()
        }
        if (
            type(packet_files) is not dict or set(packet_files) != set(PACKET_FILE_NAMES)
            or type(dependency_files) is not dict
            or dependency_files != expected_dependencies
            or freeze.get("transitive_executed_import_closure")
            != [_relative(path) for _name, path in TRANSITIVE_MODULE_ORDER]
        ):
            raise EntryRefusal("Stage3 SOURCE_FREEZE source census mismatch")
        specifications = [
            (HERE / name, str(packet_files[name]), f"Stage3 packet source {name}")
            for name in sorted(PACKET_FILE_NAMES)
        ] + [
            (path, digest, f"Stage3 transitive dependency {_relative(path)}")
            for path, digest in TRANSITIVE_DEPENDENCY_SHA256.items()
        ]
        for path, digest, label in specifications:
            existing = retained.get(path)
            if existing is not None:
                if existing.sha256 != digest:
                    raise EntryRefusal(
                        f"Stage3 duplicate source census digest mismatch: {_relative(path)}"
                    )
                existing.verify()
                continue
            retained[path] = AuthenticatedSource.open(path, digest, label)
        for source in retained.values():
            source.verify()
        freeze_source.verify()
        return freeze_source, retained
    except BaseException:
        for source in retained.values():
            source.close()
        freeze_source.close()
        raise


def _execute_authenticated_module(
    name: str, source: AuthenticatedSource,
) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__file__ = str(source.path)
    module.__package__ = None
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        exec(compile(source.raw, str(source.path), "exec"), module.__dict__)
    except BaseException:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise
    return module


def frozen_runtime() -> FrozenRuntime:
    global _RUNTIME
    if _RUNTIME is not None:
        return _RUNTIME
    freeze_source, retained = _authenticate_source_closure()
    loaded: dict[str, types.ModuleType] = {}
    try:
        # Every repository source in the executed import closure is retained and
        # authenticated before the first byte of dependency code executes.
        for name, path in TRANSITIVE_MODULE_ORDER:
            for source in retained.values():
                source.verify()
            freeze_source.verify()
            loaded[name] = _execute_authenticated_module(name, retained[path])
        _RUNTIME = FrozenRuntime(
            loaded["dual_launch_coordinator"],
            loaded["production_dual_l12_launcher"],
            loaded["production_evidence_orchestrator"],
            loaded["production_obligation_validators"],
            loaded["independent_a20_auditor"],
        )
        return _RUNTIME
    finally:
        for source in retained.values():
            source.close()
        freeze_source.close()


@dataclass(frozen=True)
class ResourceCapture:
    captured_epoch: int
    host_physical_memory_bytes: int
    available_memory_bytes: int
    workspace_free_disk_bytes: int
    workspace_filesystem_device: int
    both_workspace_roots_same_filesystem: bool
    memory_pressure: str
    passes: bool

    def record(self) -> dict[str, object]:
        return {
            "captured_epoch": self.captured_epoch,
            "host_physical_memory_bytes": self.host_physical_memory_bytes,
            "available_memory_bytes": self.available_memory_bytes,
            "workspace_free_disk_bytes": self.workspace_free_disk_bytes,
            "workspace_filesystem_device": self.workspace_filesystem_device,
            "both_workspace_roots_same_filesystem": (
                self.both_workspace_roots_same_filesystem
            ),
            "memory_pressure": self.memory_pressure,
            "passes": self.passes,
        }


@dataclass(frozen=True)
class InputDigests:
    l10_cross_gate: str
    target_executable: str
    hostile_executable: str
    target_cache_manifest: str
    hostile_cache_manifest: str


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(16 * 2**20):
            digest.update(block)
    return digest.hexdigest()


def verify_frozen_dependencies() -> None:
    frozen_runtime()


def exact_policy():
    runtime = frozen_runtime()
    return runtime.coordinator.LaunchPolicy(
        target=runtime.coordinator.RolePaths(
            str(TARGET_EXECUTABLE), str(TARGET_WORKSPACE),
            str(TARGET_OUTPUT), MAPPED_CERTIFICATE,
        ),
        hostile=runtime.coordinator.RolePaths(
            str(HOSTILE_EXECUTABLE), str(HOSTILE_WORKSPACE),
            str(HOSTILE_OUTPUT), MAPPED_CERTIFICATE,
        ),
        telemetry_path=str(TELEMETRY),
    )


def parse_memory_pressure(raw: str, captured_epoch: int) -> tuple[int, int]:
    if type(raw) is not str or type(captured_epoch) is not int or captured_epoch <= 0:
        raise EntryRefusal("memory-pressure capture arguments are malformed")
    match = MEMORY_PRESSURE_PATTERN.fullmatch(raw)
    if match is None:
        raise EntryRefusal("macOS memory_pressure output is not exact")
    total, pages, page_size, percentage = map(int, match.groups())
    if total != pages * page_size or not 0 <= percentage <= 100:
        raise EntryRefusal("macOS memory-pressure arithmetic mismatch")
    # `memory_pressure -Q` reports an integer percentage.  Subtract one full
    # point before converting it to bytes so rounding can only refuse a viable
    # launch; it cannot falsely admit a threshold-edge launch.
    conservative_percentage = max(0, percentage - 1)
    available = total * conservative_percentage // 100
    return total, available


def capture_live_resources(
    epoch: int | None = None, destination_census=None,
    absence_paths: tuple[Path, ...] = PRELAUNCH_ABSENCES,
) -> ResourceCapture:
    captured = int(time.time()) if epoch is None else epoch
    if type(captured) is not int or captured <= 0:
        raise EntryRefusal("resource capture epoch is invalid")
    try:
        process = subprocess.run(
            ["/usr/bin/memory_pressure", "-Q"], check=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            timeout=15.0,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise EntryRefusal("macOS memory_pressure capture failed") from error
    if process.returncode != 0 or process.stderr != "":
        raise EntryRefusal("macOS memory_pressure refused or wrote stderr")
    total, available = parse_memory_pressure(process.stdout, captured)
    owned_census = None
    try:
        if destination_census is None:
            owned_census = RetainedDestinationCensus.open(
                DESTINATION_PARENT_CENSUS,
            )
            destination_census = owned_census
        device, free = destination_census.filesystem_state()
        destination_census.require_absent(
            absence_paths, "Stage3 live prelaunch absence census",
        )
    except BaseException as error:
        raise EntryRefusal("workspace resource capture failed") from error
    finally:
        if owned_census is not None:
            owned_census.close()
    same = True
    policy = exact_policy()
    passes = (
        total >= policy.minimum_host_physical_memory_bytes
        and available >= policy.minimum_available_memory_bytes
        and free >= policy.minimum_workspace_free_disk_bytes
        and same
    )
    return ResourceCapture(
        captured, total, available, free, device, same,
        "NORMAL" if passes else "NOT_NORMAL", passes,
    )


def require_absent(paths: Iterable[Path]) -> None:
    for path in paths:
        if os.path.lexists(path):
            raise EntryRefusal(f"prelaunch destination is already present: {path}")


def _validate_native(artifact_id: str, record: dict[str, object]) -> None:
    try:
        frozen_runtime().validators.validate_record(
            artifact_id, record, mutation_class="PRODUCTION_NATIVE_RECORD",
            fixture_mode=False,
        )
    except BaseException as error:
        raise EntryRefusal(f"{artifact_id} production validation refused") from error


def build_schedule(
    capture: ResourceCapture, digests: InputDigests, created_epoch: int,
    *, policy=None,
) -> dict[str, object]:
    policy = exact_policy() if policy is None else policy
    if type(created_epoch) is not int or created_epoch <= 0:
        raise EntryRefusal("schedule epoch is invalid")
    record = {
        "schema": "V012_DUAL_L12_READINESS_SCHEDULE_V001",
        "classification": "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT",
        "created_epoch": created_epoch,
        "expires_epoch": created_epoch + policy.maximum_schedule_age_seconds,
        "l10_cross_gate_sha256": digests.l10_cross_gate,
        "resource_snapshot": capture.record(),
        "schedule": {
            "launch_mode": "PRELAUNCHED_BLOCKED_TWO_WORKER",
            "release_only_after_both_l12_authorizations": True,
            "launch_skew_seconds_max": policy.maximum_launch_skew_seconds,
            "per_process_rss_limit_bytes": policy.per_process_rss_limit_bytes,
            "per_process_wall_limit_seconds": policy.per_process_wall_limit_seconds,
            "mapped_peak_limit_bytes_by_role": {
                role: policy.role_paths(role).mapped_peak_limit_bytes
                for role in frozen_runtime().coordinator.ROLES
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
            for role in frozen_runtime().coordinator.ROLES
        },
        "telemetry": {
            "path": policy.telemetry_path,
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "must_be_absent_before_release": True,
            "absent_at_schedule_capture": True,
            "sample_interval_seconds_max": policy.maximum_sample_interval_seconds,
        },
        "claim_boundary": (
            "READINESS_AND_RESOURCE_SCHEDULING_ONLY__NO_L12_RELEASE_OR_RESULT"
        ),
    }
    _validate_native("A20_SHARED_SCHEDULE_GATE", record)
    coordinator = frozen_runtime().coordinator.DualLaunchCoordinator(
        policy, created_epoch,
    )
    coordinator.admit_schedule(record)
    return record


def independent_schedule_audit(
    schedule: dict[str, object], evaluation_epoch: int,
    *, policy=None, observations=None,
) -> dict[str, object]:
    """Independently parse A20 raw bytes and observe every A21 input."""
    runtime = frozen_runtime()
    return _independent_schedule_audit_raw(
        runtime.coordinator.canonical_json_bytes(schedule), evaluation_epoch,
        policy=policy, observations=observations,
    )


def _independent_schedule_audit_raw(
    schedule_raw: bytes, evaluation_epoch: int,
    *, policy=None, observations=None,
) -> dict[str, object]:
    runtime = frozen_runtime()
    policy = exact_policy() if policy is None else policy
    observations = (
        runtime.a20_auditor.ObservationPaths(
            L10_CROSS_GATE,
            {
                "target_v012": TARGET_EXECUTABLE,
                "hostile_v004r4": HOSTILE_EXECUTABLE,
            },
            {
                "target_v012": TARGET_CACHE_MANIFEST,
                "hostile_v004r4": HOSTILE_CACHE_MANIFEST,
            },
        )
        if observations is None else observations
    )
    record = runtime.a20_auditor.audit_canonical_schedule(
        schedule_raw,
        policy, evaluation_epoch, observations,
    )
    _validate_native("A21_SHARED_SCHEDULE_AUDIT", record)
    coordinator = runtime.coordinator.DualLaunchCoordinator(
        policy, evaluation_epoch,
    )
    schedule = runtime.a20_auditor.parse_canonical_schedule(schedule_raw)
    coordinator.admit_schedule(schedule)
    coordinator.admit_schedule_audit(record)
    return record


def build_authorization(
    role: str, coordinator, digests: InputDigests,
) -> dict[str, object]:
    if coordinator.stage not in {"SCHEDULE_AUDITED", "AUTHORIZATIONS_PARTIAL"}:
        raise EntryRefusal("one-way authorization is premature")
    target = role == "target_v012"
    if role not in frozen_runtime().coordinator.ROLES:
        raise EntryRefusal("authorization role is unknown")
    record = {
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
        "schedule_sha256": coordinator.accepted_sha256("schedule"),
        "schedule_audit_sha256": coordinator.accepted_sha256("schedule_audit"),
        "l10_cross_gate_sha256": coordinator.accepted_record(
            "schedule"
        )["l10_cross_gate_sha256"],
        "consumer_sha256": (
            digests.target_executable if target else digests.hostile_executable
        ),
        "l12_cache_manifest_sha256": (
            digests.target_cache_manifest if target
            else digests.hostile_cache_manifest
        ),
        "claim_boundary": (
            "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT"
        ),
    }
    _validate_native("A22_TARGET_L12_AUTHORIZATION", record)
    coordinator.admit_authorization(record)
    return record


def validate_authorization_bindings(
    target: dict[str, object], hostile: dict[str, object], digests: InputDigests,
) -> None:
    expected = {
        "target_v012": (digests.target_executable, digests.target_cache_manifest),
        "hostile_v004r4": (
            digests.hostile_executable, digests.hostile_cache_manifest,
        ),
    }
    records = {"target_v012": target, "hostile_v004r4": hostile}
    for role in frozen_runtime().coordinator.ROLES:
        consumer, cache = expected[role]
        if (
            records[role].get("consumer_sha256") != consumer
            or records[role].get("l12_cache_manifest_sha256") != cache
        ):
            raise EntryRefusal(f"{role} authorization input binding mismatch")


def build_all_records(
    capture: ResourceCapture, digests: InputDigests, evaluation_epoch: int,
    *, policy=None, observations=None,
) -> dict[str, dict[str, object]]:
    policy = exact_policy() if policy is None else policy
    schedule = build_schedule(
        capture, digests, evaluation_epoch, policy=policy,
    )
    audit = independent_schedule_audit(
        schedule, evaluation_epoch,
        policy=policy, observations=observations,
    )
    coordinator = frozen_runtime().coordinator.DualLaunchCoordinator(
        policy, evaluation_epoch,
    )
    coordinator.admit_schedule(schedule)
    coordinator.admit_schedule_audit(audit)
    target = build_authorization("target_v012", coordinator, digests)
    hostile = build_authorization("hostile_v004r4", coordinator, digests)
    validate_authorization_bindings(target, hostile, digests)
    if coordinator.stage != "AUTHORIZATIONS_COMPLETE":
        raise EntryRefusal("A20-A22 coordinator did not reach authorization completion")
    return {
        "schedule": schedule, "schedule_audit": audit,
        "target_authorization": target, "hostile_authorization": hostile,
    }


def fixture_bundle(epoch: int = 2_000_000_000) -> tuple[
    ResourceCapture, InputDigests,
]:
    return (
        ResourceCapture(
            epoch, 64_000_000_000, 48_000_000_000, 40_000_000_000,
            1, True, "NORMAL", True,
        ),
        InputDigests(*(
            hashlib.sha256(f"stage3-fixture-{index}".encode("ascii")).hexdigest()
            for index in range(5)
        )),
    )


@contextmanager
def fixture_environment(epoch: int = 2_000_000_000):
    """Create source/absence observations for nonphysical hostile tests."""
    runtime = frozen_runtime()
    with tempfile.TemporaryDirectory(prefix="stage3_fixture_", dir=HERE) as directory:
        base = Path(directory).resolve()
        target = base / "target"
        hostile = base / "hostile"
        shared = base / "shared"
        for path in (
            target / "workspaces", target / "outputs",
            hostile / "workspaces", hostile / "outputs", shared,
        ):
            path.mkdir(parents=True, exist_ok=True)

        def immutable(path: Path, raw: bytes) -> Path:
            path.write_bytes(raw)
            os.chmod(path, 0o444)
            return path

        cross = immutable(shared / "A18.json", b'{"fixture":"cross"}\n')
        target_executable = immutable(target / "worker.py", b"# target fixture\n")
        hostile_executable = immutable(hostile / "worker.py", b"# hostile fixture\n")
        target_cache = immutable(target / "cache.json", b'{"fixture":"target"}\n')
        hostile_cache = immutable(hostile / "cache.json", b'{"fixture":"hostile"}\n')
        policy = runtime.coordinator.LaunchPolicy(
            target=runtime.coordinator.RolePaths(
                str(target_executable), str(target / "workspaces/L12"),
                str(target / "outputs/HISTORY_L12.json"), MAPPED_CERTIFICATE,
            ),
            hostile=runtime.coordinator.RolePaths(
                str(hostile_executable), str(hostile / "workspaces/L12"),
                str(hostile / "outputs/HISTORY_L12.json"), MAPPED_CERTIFICATE,
            ),
            telemetry_path=str(shared / "telemetry.json"),
        )
        observations = runtime.a20_auditor.ObservationPaths(
            cross,
            {"target_v012": target_executable, "hostile_v004r4": hostile_executable},
            {"target_v012": target_cache, "hostile_v004r4": hostile_cache},
        )
        digests = InputDigests(
            sha256_path(cross), sha256_path(target_executable),
            sha256_path(hostile_executable), sha256_path(target_cache),
            sha256_path(hostile_cache),
        )
        device = os.stat(base, follow_symlinks=False).st_dev
        capture = ResourceCapture(
            epoch, 64_000_000_000, 48_000_000_000, 40_000_000_000,
            device, True, "NORMAL", True,
        )
        yield capture, digests, policy, observations


def _open_production_inputs() -> list[object]:
    specifications = (
        ("A18 L10 cross gate", L10_CROSS_GATE, True),
        ("target executable", TARGET_EXECUTABLE, False),
        ("hostile executable", HOSTILE_EXECUTABLE, False),
        ("target L12 cache manifest", TARGET_CACHE_MANIFEST, True),
        ("hostile L12 cache manifest", HOSTILE_CACHE_MANIFEST, True),
    )
    opened: list[object] = []
    try:
        for label, path, json_record in specifications:
            opened.append(
                frozen_runtime().launcher.StableInput.open(
                    label, path, json_record=json_record,
                    json_encoding=(
                        "publication"
                        if label in {
                            "A18 L10 cross gate",
                            "target L12 cache manifest",
                        }
                        else "compact"
                    ),
                )
            )
        return opened
    except BaseException as error:
        for item in opened:
            item.close()
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            raise
        raise EntryRefusal("production A18/source/cache input custody refused") from error


def _verify_a18_bindings(inputs: list[object]) -> InputDigests:
    by_label = {item.label: item for item in inputs}
    cross = by_label["A18 L10 cross gate"]
    if not isinstance(cross.record, dict):
        raise EntryRefusal("A18 record is absent")
    _validate_native("A18_L10_CROSS_GATE", cross.record)
    bindings = {
        "target": (
            by_label["target executable"],
            by_label["target L12 cache manifest"],
        ),
        "hostile": (
            by_label["hostile executable"],
            by_label["hostile L12 cache manifest"],
        ),
    }
    for branch, (executable, cache) in bindings.items():
        branch_record = cross.record[branch]["branch"]
        for name, held in (("consumer", executable), ("L12_cache_manifest", cache)):
            binding = branch_record[name]
            if binding["path"] != str(held.path) or binding["sha256"] != held.digest:
                raise EntryRefusal(f"A18 {branch} {name} binding mismatch")
        cache_record = cache.record
        cache_binding = branch_record["L12_cache_manifest"]
        if (
            not isinstance(cache_record, dict)
            or cache_record.get("schema") != cache_binding["schema"]
            or cache_record.get(cache_binding["identity_field"])
            != cache_binding["identity_value"]
        ):
            raise EntryRefusal(f"A18 {branch} cache identity mismatch")
    return InputDigests(
        cross.digest,
        by_label["target executable"].digest,
        by_label["hostile executable"].digest,
        by_label["target L12 cache manifest"].digest,
        by_label["hostile L12 cache manifest"].digest,
    )


def _verify_inputs(inputs: list[object]) -> None:
    for item in inputs:
        item.verify()


def _close_inputs(inputs: list[object]) -> None:
    first: BaseException | None = None
    for item in inputs:
        try:
            item.verify()
        except BaseException as error:
            if first is None:
                first = error
        finally:
            item.close()
    if first is not None:
        raise first


def _retained_raw(item) -> bytes:
    item.verify()
    size = int(item.identity[2])
    chunks: list[bytes] = []
    offset = 0
    while offset < size:
        block = os.pread(item.descriptor, min(1024 * 1024, size - offset), offset)
        if not block:
            raise EntryRefusal(f"short retained canonical read: {item.label}")
        chunks.append(block)
        offset += len(block)
    raw = b"".join(chunks)
    if hashlib.sha256(raw).hexdigest() != item.digest:
        raise EntryRefusal(f"retained canonical hash mismatch: {item.label}")
    item.verify()
    return raw


def _census_presence(destination_census, path: Path) -> bool:
    destination_census.verify_parents()
    retained = destination_census.parents.get(path.parent)
    if retained is None:
        raise EntryRefusal(f"canonical destination parent was not retained: {path}")
    try:
        os.lstat(path.name, dir_fd=retained[0])
    except FileNotFoundError:
        return False
    return True


def _publish_or_resume(
    path: Path, label: str, expected_record: dict[str, object],
    destination_census,
):
    runtime = frozen_runtime()
    expected_raw = runtime.coordinator.canonical_json_bytes(expected_record)
    present = _census_presence(destination_census, path)
    if not present:
        try:
            runtime.evidence._atomic_publish_once(
                str(path), expected_raw, str(path),
            )
        except BaseException as error:
            raise EntryRefusal(f"{label} owner-once publication refused") from error
    try:
        retained = runtime.launcher.StableInput.open(
            label, path, json_record=True,
        )
    except BaseException as error:
        raise EntryRefusal(f"{label} canonical custody refused") from error
    raw = _retained_raw(retained)
    if raw != expected_raw:
        retained.close()
        raise EntryRefusal(f"{label} restart predecessor mismatch")
    return retained, not present


def _production_observations():
    runtime = frozen_runtime()
    return runtime.a20_auditor.ObservationPaths(
        L10_CROSS_GATE,
        {
            "target_v012": TARGET_EXECUTABLE,
            "hostile_v004r4": HOSTILE_EXECUTABLE,
        },
        {
            "target_v012": TARGET_CACHE_MANIFEST,
            "hostile_v004r4": HOSTILE_CACHE_MANIFEST,
        },
    )


def prepare_production(*, publish: bool) -> dict[str, object]:
    runtime = frozen_runtime()
    destination_census = RetainedDestinationCensus.open(
        DESTINATION_PARENT_CENSUS,
    )
    inputs: list[object] = []
    canonical: list[object] = []
    primary: BaseException | None = None
    try:
        destination_census.require_absent(
            EXECUTION_ABSENCES, "Stage3 pre-A20 execution absence census",
        )
        present = {path: _census_presence(destination_census, path) for path in OUTPUT_PATHS}
        if present[SCHEDULE_AUDIT] and not present[SCHEDULE]:
            raise EntryRefusal("A21 exists without canonical A20")
        if (
            (present[TARGET_AUTHORIZATION] or present[HOSTILE_AUTHORIZATION])
            and not present[SCHEDULE_AUDIT]
        ):
            raise EntryRefusal("A22 exists without canonical A21")

        inputs = _open_production_inputs()
        digests = _verify_a18_bindings(inputs)
        capture = capture_live_resources(
            destination_census=destination_census,
            absence_paths=EXECUTION_ABSENCES,
        )
        if not capture.passes:
            raise EntryRefusal("live resources do not satisfy the frozen launch policy")
        policy = exact_policy()
        observations = _production_observations()

        if present[SCHEDULE]:
            schedule_input = runtime.launcher.StableInput.open(
                "canonical A20 schedule", SCHEDULE, json_record=True,
            )
            canonical.append(schedule_input)
            schedule_raw = _retained_raw(schedule_input)
            schedule = schedule_input.record
            if not isinstance(schedule, dict):
                raise EntryRefusal("canonical A20 record is absent")
            _validate_native("A20_SHARED_SCHEDULE_GATE", schedule)
            if schedule.get("l10_cross_gate_sha256") != digests.l10_cross_gate:
                raise EntryRefusal("canonical A20 restart A18 binding mismatch")
            runtime.coordinator.DualLaunchCoordinator(
                policy, capture.captured_epoch,
            ).admit_schedule(schedule)
            schedule_created = False
        else:
            schedule = build_schedule(
                capture, digests, capture.captured_epoch, policy=policy,
            )
            if publish:
                schedule_input, schedule_created = _publish_or_resume(
                    SCHEDULE, "canonical A20 schedule", schedule,
                    destination_census,
                )
                canonical.append(schedule_input)
                schedule_raw = _retained_raw(schedule_input)
                schedule = schedule_input.record
                assert isinstance(schedule, dict)
            else:
                schedule_created = False
                schedule_raw = runtime.coordinator.canonical_json_bytes(schedule)

        audit = _independent_schedule_audit_raw(
            schedule_raw, capture.captured_epoch,
            policy=policy, observations=observations,
        )
        if publish:
            audit_input, audit_created = _publish_or_resume(
                SCHEDULE_AUDIT, "canonical A21 schedule audit", audit,
                destination_census,
            )
            canonical.append(audit_input)
            audit_raw = _retained_raw(audit_input)
            if audit_raw != runtime.coordinator.canonical_json_bytes(audit):
                raise EntryRefusal("canonical A21 independent reconstruction mismatch")
            audit = audit_input.record
            assert isinstance(audit, dict)
        else:
            audit_created = False

        coordinator = runtime.coordinator.DualLaunchCoordinator(
            policy, capture.captured_epoch,
        )
        coordinator.admit_schedule(schedule)
        coordinator.admit_schedule_audit(audit)
        target = build_authorization("target_v012", coordinator, digests)
        hostile = build_authorization("hostile_v004r4", coordinator, digests)
        validate_authorization_bindings(target, hostile, digests)
        if coordinator.stage != "AUTHORIZATIONS_COMPLETE":
            raise EntryRefusal("A20-A22 coordinator did not reach authorization completion")
        records = {
            "schedule": schedule, "schedule_audit": audit,
            "target_authorization": target,
            "hostile_authorization": hostile,
        }
        _verify_inputs(inputs)
        destination_census.require_absent(
            EXECUTION_ABSENCES, "Stage3 post-A21 execution absence census",
        )
        if not publish:
            return {
                "classification": "PASS_STAGE3_A20_A22_PRODUCTION_DRY_RUN",
                "published": False,
                "resource_snapshot": capture.record(),
                "sha256_by_record": {
                    name: runtime.coordinator.record_sha256(record)
                    for name, record in records.items()
                },
                "claim_boundary": "PREPARATION_ONLY__NO_RECORD_PUBLISHED_OR_WORKER_LAUNCHED",
            }
        published: dict[str, str] = {
            "schedule": runtime.coordinator.record_sha256(schedule),
            "schedule_audit": runtime.coordinator.record_sha256(audit),
        }
        created = {
            "schedule": schedule_created,
            "schedule_audit": audit_created,
        }
        for name, path in (
            ("target_authorization", TARGET_AUTHORIZATION),
            ("hostile_authorization", HOSTILE_AUTHORIZATION),
        ):
            _verify_inputs(inputs)
            destination_census.require_absent(
                EXECUTION_ABSENCES,
                f"Stage3 immediate pre-{name} execution absence census",
            )
            item, was_created = _publish_or_resume(
                path, f"canonical {name}", records[name], destination_census,
            )
            canonical.append(item)
            published[name] = item.digest
            created[name] = was_created
        _verify_inputs(inputs)
        destination_census.require_absent(
            EXECUTION_ABSENCES, "Stage3 post-A22 execution absence census",
        )
        reconstructed = runtime.coordinator.DualLaunchCoordinator(
            policy, capture.captured_epoch,
        )
        by_path = {item.path: item for item in canonical}
        reconstructed.admit_schedule(by_path[SCHEDULE].record)
        reconstructed.admit_schedule_audit(by_path[SCHEDULE_AUDIT].record)
        reconstructed.admit_authorization(by_path[TARGET_AUTHORIZATION].record)
        reconstructed.admit_authorization(by_path[HOSTILE_AUTHORIZATION].record)
        if reconstructed.stage != "AUTHORIZATIONS_COMPLETE":
            raise EntryRefusal("published A20-A22 reconstruction failed")
        return {
            "classification": "PASS_STAGE3_A20_A22_OWNER_ONCE_PUBLICATION",
            "published": True,
            "sha256_by_record": published,
            "created_in_this_invocation": created,
            "claim_boundary": "A20_A22_ENTRY_RECORDS_ONLY__NO_WORKER_LAUNCH_OR_RESULT",
        }
    except BaseException as error:
        primary = error
        raise
    finally:
        for item in canonical:
            try:
                item.verify()
            except BaseException:
                if primary is None:
                    primary = EntryRefusal("canonical predecessor changed while retained")
            finally:
                item.close()
        try:
            _close_inputs(inputs)
        except BaseException:
            if primary is None:
                primary = EntryRefusal("production input changed while retained")
        try:
            destination_census.close()
        except BaseException:
            if primary is None:
                primary = EntryRefusal("destination parent changed while retained")
        if primary is not None and sys.exc_info()[0] is None:
            raise primary


def launch_authenticated_l12() -> dict[str, object]:
    """Invoke the patched launcher only through retained Stage3 custody."""
    runtime = frozen_runtime()
    guard = Stage3ExecutionGuard.open()
    primary: BaseException | None = None
    try:
        digest = runtime.launcher.execute(guard)
        return {
            "classification": "PASS_STAGE3_GUARDED_DUAL_L12_LAUNCH",
            "telemetry_sha256": digest,
            "claim_boundary": "EXECUTION_TELEMETRY_ONLY__NO_FINAL_L12_ADJUDICATION",
        }
    except BaseException as error:
        primary = error
        raise
    finally:
        try:
            guard.close()
        except BaseException as error:
            if primary is None:
                raise EntryRefusal("Stage3 execution guard lost parent custody") from error


def main() -> int:
    try:
        frozen_runtime()
    except Exception as error:
        print(f"REFUSED: Stage3 SOURCE_FREEZE/import closure: {error}", file=sys.stderr)
        return 2
    if len(sys.argv) != 2 or sys.argv[1] not in {
        "fixture", "dry-run", "publish", "launch",
    }:
        print(
            "REFUSED: exact mode is fixture, dry-run, publish, or launch",
            file=sys.stderr,
        )
        return 2
    try:
        if sys.argv[1] == "fixture":
            with fixture_environment() as fixture:
                capture, digests, policy, observations = fixture
                records = build_all_records(
                    capture, digests, capture.captured_epoch,
                    policy=policy, observations=observations,
                )
                result = {
                    "classification": "PASS_STAGE3_A20_A22_FIXTURE",
                    "published": False,
                    "sha256_by_record": {
                        name: frozen_runtime().coordinator.record_sha256(record)
                        for name, record in records.items()
                    },
                    "claim_boundary": "SYNTHETIC_FIXTURE_ONLY__NO_CANONICAL_RECORD_OR_LAUNCH",
                }
        elif sys.argv[1] in {"dry-run", "publish"}:
            result = prepare_production(publish=sys.argv[1] == "publish")
        else:
            result = launch_authenticated_l12()
    except Exception as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
