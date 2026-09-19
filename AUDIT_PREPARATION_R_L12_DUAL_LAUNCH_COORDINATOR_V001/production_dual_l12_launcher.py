#!/usr/bin/env python3
"""Exact owner-once launcher for the two authenticated L12 workers.

This is an execution-boundary component.  It performs no physics itself.  It
retains the schedule, audit, authorizations, manifests, executables and L10
cross-gate; starts exactly two inherited-socket workers; publishes every wire
record once; samples live RSS/disk; and refuses without deleting workspaces or
physical outputs.  The caller must provide a freshly prepared Stage-2 tree.
"""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
import selectors
import signal
import socket
import stat
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
FINAL_PACKET: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
)
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(FINAL_PACKET) not in sys.path:
    sys.path.insert(0, str(FINAL_PACKET))

from dual_launch_coordinator import (  # noqa: E402
    ROLES, DualLaunchCoordinator, LaunchPolicy, RolePaths,
    Refusal as CoordinatorRefusal, _release_token, canonical_json_bytes,
    parse_strict_json, record_sha256,
)
from production_evidence_orchestrator import (  # noqa: E402
    StageEvidencePublisher, _atomic_publish_once,
)
from independent_final_auditor import validate_artifact  # noqa: E402


SHARED: Final[Path] = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
TARGET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
TARGET_EXECUTABLE: Final[Path] = TARGET / "consume_target_cache.py"
HOSTILE_EXECUTABLE: Final[Path] = HOSTILE / "consume_cache_v004r4.py"
TARGET_CACHE_ROOT: Final[Path] = TARGET / "CACHE_PAYLOADS_V012/L12"
HOSTILE_CACHE_ROOT: Final[Path] = HOSTILE / "V004R4_CACHE_PAYLOADS/L12"
TARGET_WORKSPACE: Final[Path] = TARGET / "WORKSPACES/L12"
HOSTILE_WORKSPACE: Final[Path] = HOSTILE / "V004R4_WORKSPACES/L12"
TARGET_OUTPUT: Final[Path] = TARGET / "PHYSICAL_OUTPUTS/HISTORY_L12.json"
HOSTILE_OUTPUT: Final[Path] = (
    HOSTILE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json"
)
SCHEDULE: Final[Path] = SHARED / "SHARED_AGGREGATE_SCHEDULE_GATE_V001.json"
SCHEDULE_AUDIT: Final[Path] = (
    SHARED / "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json"
)
L10_CROSS_GATE: Final[Path] = SHARED / "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
TARGET_AUTHORIZATION: Final[Path] = TARGET / "TARGET_L12_EXECUTION_GATE_V012.json"
HOSTILE_AUTHORIZATION: Final[Path] = (
    HOSTILE / "HOSTILE_L12_EXECUTION_GATE_V004R4.json"
)
TELEMETRY: Final[Path] = SHARED / "SHARED_AGGREGATE_TELEMETRY_V001.json"
WIRE_MAX: Final[int] = 2**20
SAMPLE_SECONDS: Final[int] = 30
MAPPED_CERTIFICATE: Final[int] = 252_944_080
RSS_PEAK_SEMANTICS: Final[str] = (
    "LAUNCHER_SAMPLED_CURRENT_RSS_AT_MOST_30_SECONDS__NOT_OS_HIGH_WATER"
)

WIRE_PATHS: Final[dict[str, Path]] = {
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


class LaunchRefusal(RuntimeError):
    """The executable dual-launch boundary refused closed."""


def _sha256_fd(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while True:
        block = os.pread(descriptor, 16 * 2**20, offset)
        if not block:
            return digest.hexdigest()
        digest.update(block)
        offset += len(block)


def _read_exact_fd(descriptor: int, size: int) -> bytes:
    if type(size) is not int or size < 0:
        raise LaunchRefusal("retained input size is invalid")
    result = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(descriptor, min(16 * 2**20, size - offset), offset)
        if not block:
            raise LaunchRefusal("retained input read was short")
        result.extend(block)
        offset += len(block)
    return bytes(result)


def _identity(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        stat.S_IMODE(metadata.st_mode),
    )


def _parent_identity(metadata: os.stat_result) -> tuple[int, int, int]:
    return metadata.st_dev, metadata.st_ino, stat.S_IFMT(metadata.st_mode)


def _require_canonical_repository_path(path: Path, label: str) -> None:
    text = str(path)
    if (
        not path.is_absolute() or Path(text) != path or "\x00" in text
        or path == ROOT or ROOT not in path.parents
    ):
        raise LaunchRefusal(f"{label} is outside the canonical repository")
    if ROOT.resolve() != ROOT:
        raise LaunchRefusal("repository root is symlinked")
    cursor = ROOT
    for component in path.relative_to(ROOT).parts[:-1]:
        cursor = cursor / component
        try:
            metadata = os.lstat(cursor)
        except OSError as error:
            raise LaunchRefusal(f"{label} parent is absent") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise LaunchRefusal(f"{label} parent is symlinked or non-directory")


@dataclass
class StableInput:
    label: str
    path: Path
    descriptor: int
    parent_descriptor: int
    digest: str
    identity: tuple[int, int, int, int, int, int, int]
    parent_identity: tuple[int, int, int]
    record: dict[str, object] | None

    @classmethod
    def open(cls, label: str, path: Path, *, json_record: bool) -> "StableInput":
        _require_canonical_repository_path(path, label)
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        parent_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_DIRECTORY", 0)
        )
        parent_descriptor = -1
        descriptor = -1
        try:
            parent_descriptor = os.open(path.parent, parent_flags)
            parent_opened = os.fstat(parent_descriptor)
            parent_current = os.stat(path.parent, follow_symlinks=False)
            if (
                not stat.S_ISDIR(parent_opened.st_mode)
                or not stat.S_ISDIR(parent_current.st_mode)
                or _parent_identity(parent_opened) != _parent_identity(parent_current)
            ):
                raise LaunchRefusal(f"{label} parent identity mismatch")
            descriptor = os.open(path.name, flags, dir_fd=parent_descriptor)
        except BaseException as error:
            if descriptor >= 0:
                os.close(descriptor)
            if parent_descriptor >= 0:
                os.close(parent_descriptor)
            if isinstance(error, OSError):
                raise LaunchRefusal(f"{label} cannot be opened") from error
            raise
        try:
            metadata = os.fstat(descriptor)
            current = os.stat(path, follow_symlinks=False)
            if (
                not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o222
                or metadata.st_nlink != 1 or _identity(metadata) != _identity(current)
            ):
                raise LaunchRefusal(f"{label} is writable, aliased, or special")
            digest = _sha256_fd(descriptor)
            after_hash = os.fstat(descriptor)
            path_after_hash = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
            parent_after_hash = os.fstat(parent_descriptor)
            parent_path_after_hash = os.stat(path.parent, follow_symlinks=False)
            if (
                _identity(after_hash) != _identity(metadata)
                or _identity(path_after_hash) != _identity(metadata)
                or _parent_identity(parent_after_hash)
                != _parent_identity(parent_opened)
                or _parent_identity(parent_path_after_hash)
                != _parent_identity(parent_opened)
            ):
                raise LaunchRefusal(f"{label} changed during authentication")
            record = None
            if json_record:
                raw = _read_exact_fd(descriptor, metadata.st_size)
                if hashlib.sha256(raw).hexdigest() != digest:
                    raise LaunchRefusal(f"{label} read/hash mismatch")
                try:
                    value = parse_strict_json(raw.decode("ascii"))
                except (UnicodeDecodeError, CoordinatorRefusal) as error:
                    raise LaunchRefusal(f"{label} is not strict JSON") from error
                if type(value) is not dict or canonical_json_bytes(value) != raw:
                    raise LaunchRefusal(f"{label} is not canonical JSON")
                record = value
            retained = cls(
                label, path, descriptor, parent_descriptor, digest,
                _identity(metadata),
                _parent_identity(parent_opened), record,
            )
            try:
                retained.verify()
            except BaseException:
                retained.close()
                descriptor = -1
                parent_descriptor = -1
                raise
            return retained
        except BaseException:
            if descriptor >= 0:
                os.close(descriptor)
            if parent_descriptor >= 0:
                os.close(parent_descriptor)
            raise

    def verify(self) -> None:
        _require_canonical_repository_path(self.path, self.label)
        parent_opened = os.fstat(self.parent_descriptor)
        parent_current = os.stat(self.path.parent, follow_symlinks=False)
        opened = os.fstat(self.descriptor)
        current = os.stat(
            self.path.name, dir_fd=self.parent_descriptor,
            follow_symlinks=False,
        )
        if (
            _parent_identity(parent_opened) != self.parent_identity
            or _parent_identity(parent_current) != self.parent_identity
            or _identity(opened) != self.identity
            or _identity(current) != self.identity
            or opened.st_mode & 0o222 or opened.st_nlink != 1
        ):
            raise LaunchRefusal(f"retained input changed: {self.label}")
        digest = _sha256_fd(self.descriptor)
        after = os.fstat(self.descriptor)
        path_after = os.stat(
            self.path.name, dir_fd=self.parent_descriptor,
            follow_symlinks=False,
        )
        parent_after = os.fstat(self.parent_descriptor)
        parent_path_after = os.stat(self.path.parent, follow_symlinks=False)
        if (
            digest != self.digest
            or _identity(after) != self.identity
            or _identity(path_after) != self.identity
            or _parent_identity(parent_after) != self.parent_identity
            or _parent_identity(parent_path_after) != self.parent_identity
        ):
            raise LaunchRefusal(f"retained input changed: {self.label}")

    def close(self) -> None:
        if self.descriptor >= 0:
            os.close(self.descriptor)
            self.descriptor = -1
        if self.parent_descriptor >= 0:
            os.close(self.parent_descriptor)
            self.parent_descriptor = -1


def _close_all(inputs: list[StableInput]) -> None:
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


class _ProcBsdInfo(ctypes.Structure):
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


class _ProcTaskInfo(ctypes.Structure):
    _fields_ = [
        ("virtual_size", ctypes.c_uint64), ("resident_size", ctypes.c_uint64),
        ("total_user", ctypes.c_uint64), ("total_system", ctypes.c_uint64),
        ("threads_user", ctypes.c_uint64), ("threads_system", ctypes.c_uint64),
        ("policy", ctypes.c_int32), ("faults", ctypes.c_int32),
        ("pageins", ctypes.c_int32), ("cow_faults", ctypes.c_int32),
        ("messages_sent", ctypes.c_int32),
        ("messages_received", ctypes.c_int32),
        ("syscalls_mach", ctypes.c_int32), ("syscalls_unix", ctypes.c_int32),
        ("csw", ctypes.c_int32), ("threadnum", ctypes.c_int32),
        ("numrunning", ctypes.c_int32), ("priority", ctypes.c_int32),
    ]


def _proc_query(pid: int, flavor: int, record: ctypes.Structure) -> None:
    if type(pid) is not int or pid <= 0:
        raise LaunchRefusal("process id is invalid")
    try:
        library = ctypes.CDLL("/usr/lib/libproc.dylib")
        query = library.proc_pidinfo
        query.argtypes = [
            ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
            ctypes.c_void_p, ctypes.c_int,
        ]
        query.restype = ctypes.c_int
        size = query(pid, flavor, 0, ctypes.byref(record), ctypes.sizeof(record))
    except (AttributeError, OSError) as error:
        raise LaunchRefusal("cannot query kernel process identity") from error
    if size != ctypes.sizeof(record):
        raise LaunchRefusal("kernel process query returned the wrong record size")


def process_start_token(pid: int) -> str:
    record = _ProcBsdInfo()
    _proc_query(pid, 3, record)
    if (
        record.pid != pid or record.start_seconds <= 0
        or record.start_microseconds >= 1_000_000
    ):
        raise LaunchRefusal("kernel process start record is malformed")
    stamp = f"{record.start_seconds}.{record.start_microseconds:06d}".encode("ascii")
    return hashlib.sha256(
        b"V012_L12_PROCESS_START_V001\0" + str(pid).encode("ascii")
        + b"\0" + stamp
    ).hexdigest()


def live_rss(pid: int, expected_token: str) -> int:
    if process_start_token(pid) != expected_token:
        raise LaunchRefusal("live process start identity changed")
    record = _ProcTaskInfo()
    _proc_query(pid, 4, record)
    if record.resident_size <= 0:
        raise LaunchRefusal("live process RSS is invalid")
    return int(record.resident_size)


def _strict_frame(raw: bytes, label: str) -> dict[str, object]:
    if type(raw) is not bytes or not raw.endswith(b"\n") or len(raw) > WIRE_MAX:
        raise LaunchRefusal(f"{label} wire framing mismatch")
    try:
        value = parse_strict_json(raw.decode("ascii"))
    except (UnicodeDecodeError, CoordinatorRefusal) as error:
        raise LaunchRefusal(f"{label} wire JSON mismatch") from error
    if type(value) is not dict or canonical_json_bytes(value) != raw:
        raise LaunchRefusal(f"{label} is not one canonical record")
    return value


def receive_frame(channel: socket.socket, label: str) -> tuple[dict[str, object], bytes]:
    data = bytearray()
    while b"\n" not in data:
        try:
            block = channel.recv(4096)
        except socket.timeout as error:
            raise LaunchRefusal(f"{label} timed out") from error
        if not block:
            raise LaunchRefusal(f"{label} channel closed before a record")
        data.extend(block)
        if len(data) > WIRE_MAX:
            raise LaunchRefusal(f"{label} exceeds the wire bound")
    line, trailing = bytes(data).split(b"\n", 1)
    if trailing:
        raise LaunchRefusal(f"{label} contains trailing records")
    raw = line + b"\n"
    return _strict_frame(raw, label), raw


def build_handshake(
    coordinator: DualLaunchCoordinator,
    ready: dict[str, dict[str, object]],
) -> dict[str, object]:
    epochs = {role: ready[role]["ready_epoch"] for role in ROLES}
    created = max(int(time.time()), *(int(value) for value in epochs.values()))
    return {
        "schema": "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002",
        "classification": "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS",
        "created_epoch": created,
        "schedule_sha256": coordinator.accepted_sha256("schedule"),
        "schedule_audit_sha256": coordinator.accepted_sha256("schedule_audit"),
        "authorization_sha256_by_role": {
            role: coordinator.accepted_sha256(role) for role in ROLES
        },
        "memory_pressure": "NORMAL",
        "workers": ready,
        "ready_sha256_by_role": {
            role: record_sha256(ready[role]) for role in ROLES
        },
        "observed_readiness_skew_seconds": abs(
            int(epochs[ROLES[0]]) - int(epochs[ROLES[1]])
        ),
        "launch_skew_seconds_max": 60,
        "telemetry": {
            "path": coordinator.policy.telemetry_path,
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "absent_before_release": True,
        },
        "claim_boundary": "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT",
    }


def build_release(
    coordinator: DualLaunchCoordinator,
    release_epochs: dict[str, int],
) -> dict[str, object]:
    handshake = coordinator.accepted_record("handshake")
    handshake_sha = coordinator.accepted_sha256("handshake")
    return {
        "schema": "V012_DUAL_L12_WORKER_RELEASE_V002",
        "classification": "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS",
        "handshake_sha256": handshake_sha,
        "authorization_sha256_by_role": {
            role: coordinator.accepted_sha256(role) for role in ROLES
        },
        "release_epoch_by_role": release_epochs,
        "observed_launch_skew_seconds": abs(
            release_epochs[ROLES[0]] - release_epochs[ROLES[1]]
        ),
        "release_by_role": {
            role: {
                "role": role,
                "worker_id": handshake["workers"][role]["worker_id"],
                "process_id": handshake["workers"][role]["process_id"],
                "process_start_token": handshake["workers"][role]["process_start_token"],
                "control_channel_id": handshake["workers"][role]["control_channel_id"],
                "nonce_commitment_sha256": handshake["workers"][role]["nonce_commitment_sha256"],
                "release_token_sha256": _release_token(
                    handshake_sha, role, release_epochs[role],
                ),
            }
            for role in ROLES
        },
        "claim_boundary": "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT",
    }


def _publish(path: Path, record: dict[str, object]) -> str:
    _require_canonical_repository_path(path, "owner-once evidence output")
    expected = WIRE_PATHS.get(next(
        (key for key, value in WIRE_PATHS.items() if value == path), ""
    ))
    if expected != path:
        raise LaunchRefusal("evidence output is outside the exact registry")
    try:
        return _atomic_publish_once(
            str(path), canonical_json_bytes(record), str(path),
        )
    except BaseException as error:
        raise LaunchRefusal("owner-once evidence publication failed") from error


@dataclass
class Worker:
    role: str
    process: subprocess.Popen[bytes]
    channel: socket.socket
    channel_id: str
    worker_id: str
    ready: dict[str, object] | None = None
    token: str | None = None
    completed: bool = False


def _worker_argv(role: str, child_fd: int, channel_id: str, worker_id: str,
                 target_manifest_sha: str) -> list[str]:
    common = [
        "--orchestrated-worker", "--control-fd", str(child_fd),
        "--control-channel-id", channel_id, "--worker-id", worker_id,
    ]
    if role == "target_v012":
        return [
            sys.executable, str(TARGET_EXECUTABLE), "execute", "--length", "12",
            "--cache-root", str(TARGET_CACHE_ROOT),
            "--cache-manifest-sha256", target_manifest_sha,
            "--output", str(TARGET_OUTPUT), "--workspace", str(TARGET_WORKSPACE),
            *common,
        ]
    return [
        sys.executable, str(HOSTILE_EXECUTABLE), "execute", "--length", "12",
        *common,
    ]


def _terminate_exact(worker: Worker) -> None:
    if worker.process.poll() is not None:
        return
    if worker.token is None:
        # The Popen handle is still a waitable child handle.  poll() above
        # proves it has not been reaped/reused; use TERM only and never widen
        # this pre-authentication cleanup to KILL.
        worker.process.terminate()
        worker.process.wait(timeout=10)
        return
    if process_start_token(worker.process.pid) != worker.token:
        raise LaunchRefusal(f"refuse to signal unauthenticated {worker.role} process")
    worker.process.send_signal(signal.SIGTERM)
    try:
        worker.process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        if process_start_token(worker.process.pid) != worker.token:
            raise LaunchRefusal(f"refuse to kill reused {worker.role} PID")
        worker.process.kill()
        worker.process.wait(timeout=10)


def _append_epoch_sample(rows: list[dict[str, object]], row: dict[str, object]) -> None:
    if rows and rows[-1]["captured_epoch"] == row["captured_epoch"]:
        if "rss_bytes" in row:
            if int(row["rss_bytes"]) > int(rows[-1]["rss_bytes"]):
                rows[-1] = row
        else:
            rows[-1] = row
    else:
        rows.append(row)


def _sample_worker(
    worker: Worker,
    epoch: int,
    policy: LaunchPolicy,
    rows: list[dict[str, object]],
) -> None:
    if worker.ready is None or worker.token is None:
        raise LaunchRefusal(f"{worker.role} is not authenticated for RSS sampling")
    if worker.process.poll() is not None:
        raise LaunchRefusal(f"{worker.role} exited before authenticated completion")
    rss = live_rss(worker.process.pid, worker.token)
    if rss > policy.per_process_rss_limit_bytes:
        raise LaunchRefusal(f"{worker.role} live RSS exceeds the execution limit")
    _append_epoch_sample(rows, {
        "captured_epoch": epoch,
        "rss_bytes": rss,
        **{
            key: worker.ready[key] for key in (
                "process_id", "process_start_token", "executable_path",
                "executable_sha256",
            )
        },
    })


def _sample_disk(
    epoch: int,
    expected_device: int,
    policy: LaunchPolicy,
    rows: list[dict[str, object]],
    execution_guard: object,
) -> None:
    sampler = getattr(execution_guard, "disk_state", None)
    if not callable(sampler):
        raise LaunchRefusal("authenticated Stage-3 disk guard is absent")
    state = sampler()
    if (
        type(state) is not tuple or len(state) != 2
        or type(state[0]) is not int or type(state[1]) is not int
    ):
        raise LaunchRefusal("authenticated Stage-3 disk guard is malformed")
    device, free = state
    if device != expected_device:
        raise LaunchRefusal("live workspace filesystem differs from the schedule")
    if free < policy.minimum_workspace_free_disk_bytes:
        raise LaunchRefusal("live workspace free disk is below the execution limit")
    _append_epoch_sample(rows, {
        "captured_epoch": epoch,
        "workspace_filesystem_device": device,
        "free_bytes": free,
    })


def _guard_phase(execution_guard: object | None, phase: str) -> None:
    checker = getattr(execution_guard, "verify_phase", None)
    if not callable(checker):
        raise LaunchRefusal("authenticated Stage-3 execution guard is absent")
    checker(phase)


def execute(execution_guard: object | None = None) -> str:
    """Run both exact L12 workers and publish accepted A23 telemetry once."""
    _guard_phase(execution_guard, "initial")
    if ROOT.resolve() != ROOT or not SHARED.is_dir() or SHARED.is_symlink():
        raise LaunchRefusal("shared evidence directory is absent or aliased")
    for path in WIRE_PATHS.values():
        if path.exists() or path.is_symlink():
            raise LaunchRefusal(f"owner-once evidence already exists: {path.name}")
    for path in (TARGET_WORKSPACE, HOSTILE_WORKSPACE, TARGET_OUTPUT, HOSTILE_OUTPUT):
        if path.exists() or path.is_symlink():
            raise LaunchRefusal(f"worker workspace/output is not fresh: {path}")

    specifications = (
        ("schedule", SCHEDULE, True),
        ("schedule audit", SCHEDULE_AUDIT, True),
        ("L10 cross gate", L10_CROSS_GATE, True),
        ("target authorization", TARGET_AUTHORIZATION, True),
        ("hostile authorization", HOSTILE_AUTHORIZATION, True),
        ("target cache manifest", TARGET_CACHE_ROOT / "CACHE_MANIFEST.json", True),
        ("hostile cache manifest", HOSTILE_CACHE_ROOT / "CACHE_MANIFEST.json", True),
        ("target executable", TARGET_EXECUTABLE, False),
        ("hostile executable", HOSTILE_EXECUTABLE, False),
    )
    retained: list[StableInput] = []
    workers: dict[str, Worker] = {}
    log_descriptors: list[int] = []
    selector: selectors.BaseSelector | None = None
    primary_error: BaseException | None = None
    try:
        for label, path, is_json in specifications:
            retained.append(StableInput.open(label, path, json_record=is_json))
        by_label = {item.label: item for item in retained}
        records = {label: item.record for label, item in by_label.items()}
        schedule = records["schedule"]
        audit = records["schedule audit"]
        target_auth = records["target authorization"]
        hostile_auth = records["hostile authorization"]
        assert isinstance(schedule, dict) and isinstance(audit, dict)
        assert isinstance(target_auth, dict) and isinstance(hostile_auth, dict)
        if schedule["l10_cross_gate_sha256"] != by_label["L10 cross gate"].digest:
            raise LaunchRefusal("schedule does not bind the retained L10 cross gate")
        if (
            target_auth["consumer_sha256"] != by_label["target executable"].digest
            or hostile_auth["consumer_sha256"] != by_label["hostile executable"].digest
            or target_auth["l12_cache_manifest_sha256"]
            != by_label["target cache manifest"].digest
            or hostile_auth["l12_cache_manifest_sha256"]
            != by_label["hostile cache manifest"].digest
        ):
            raise LaunchRefusal("authorization source/cache binding mismatch")

        policy = LaunchPolicy(
            target=RolePaths(
                str(TARGET_EXECUTABLE), str(TARGET_WORKSPACE), str(TARGET_OUTPUT),
                MAPPED_CERTIFICATE,
            ),
            hostile=RolePaths(
                str(HOSTILE_EXECUTABLE), str(HOSTILE_WORKSPACE), str(HOSTILE_OUTPUT),
                MAPPED_CERTIFICATE,
            ),
            telemetry_path=str(TELEMETRY),
        )
        coordinator = DualLaunchCoordinator(policy, int(time.time()))
        coordinator.admit_schedule(schedule)
        coordinator.admit_schedule_audit(audit)
        coordinator.admit_authorization(target_auth)
        coordinator.admit_authorization(hostile_auth)

        for role in ROLES:
            parent, child = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
            parent.settimeout(300.0)
            channel_id = os.urandom(32).hex()
            worker_id = f"{role}-{os.urandom(16).hex()}"
            log_path = SHARED / f"{role.upper()}_WORKER_LOG_V001.txt"
            _require_canonical_repository_path(log_path, "worker log")
            log_fd = os.open(
                log_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                | getattr(os, "O_CLOEXEC", 0), 0o600,
            )
            log_descriptors.append(log_fd)
            argv = _worker_argv(
                role, child.fileno(), channel_id, worker_id,
                by_label["target cache manifest"].digest,
            )
            try:
                process = subprocess.Popen(
                    argv, cwd=str(ROOT), stdin=subprocess.DEVNULL,
                    stdout=log_fd, stderr=log_fd, close_fds=True,
                    pass_fds=(child.fileno(),),
                )
            except BaseException:
                parent.close()
                raise
            finally:
                child.close()
            worker = Worker(role, process, parent, channel_id, worker_id)
            workers[role] = worker
            worker.token = process_start_token(process.pid)

        ready: dict[str, dict[str, object]] = {}
        for role in ROLES:
            worker = workers[role]
            record, _raw = receive_frame(worker.channel, f"{role} READY")
            assert worker.token is not None
            token = process_start_token(worker.process.pid)
            executable = by_label[
                "target executable" if role == "target_v012" else "hostile executable"
            ]
            if (
                record.get("process_id") != worker.process.pid
                or record.get("process_start_token") != token
                or record.get("control_channel_id") != worker.channel_id
                or record.get("worker_id") != worker.worker_id
                or record.get("executable_sha256") != executable.digest
            ):
                raise LaunchRefusal(f"{role} READY live identity mismatch")
            executable.verify()
            worker.ready = record
            ready[role] = record
            _publish(WIRE_PATHS[f"ready:{role}"], record)

        _guard_phase(execution_guard, "pre_handshake")
        handshake = build_handshake(coordinator, ready)
        coordinator.commit_handshake(handshake)
        _publish(WIRE_PATHS["handshake"], handshake)

        release_epochs: dict[str, int] = {}
        runtime: dict[str, list[dict[str, object]]] = {role: [] for role in ROLES}
        disk: list[dict[str, object]] = []
        for role in ROLES:
            worker = workers[role]
            assert worker.ready is not None and worker.token is not None
            epoch = max(int(time.time()), int(handshake["created_epoch"]))
            release_epochs[role] = epoch
            _sample_worker(worker, epoch, policy, runtime[role])
        release = build_release(coordinator, release_epochs)
        _guard_phase(execution_guard, "pre_release")
        coordinator.release_workers(release)
        _publish(WIRE_PATHS["release"], release)
        first_release = min(release_epochs.values())
        expected_filesystem = int(
            schedule["resource_snapshot"]["workspace_filesystem_device"]
        )
        _sample_disk(first_release, expected_filesystem, policy, disk, execution_guard)

        commands: dict[str, dict[str, object]] = {}
        acks: dict[str, dict[str, object]] = {}
        for role in ROLES:
            command = coordinator.release_command(role)
            commands[role] = command
            _publish(WIRE_PATHS[f"command:{role}"], command)
            workers[role].channel.sendall(canonical_json_bytes(command))
        deadlines = {
            role: time.monotonic() + policy.per_process_wall_limit_seconds
            for role in ROLES
        }
        for role in ROLES:
            ack, _raw = receive_frame(workers[role].channel, f"{role} ACK")
            coordinator.admit_release_ack(commands[role], ack)
            acks[role] = ack
            _publish(WIRE_PATHS[f"ack:{role}"], ack)

        selector = selectors.DefaultSelector()
        for role in ROLES:
            selector.register(workers[role].channel, selectors.EVENT_READ, role)
        completions: dict[str, dict[str, object]] = {}
        while len(completions) != 2:
            incomplete = tuple(role for role in ROLES if role not in completions)
            remaining = min(deadlines[role] - time.monotonic() for role in incomplete)
            if remaining <= 0:
                raise LaunchRefusal("exact L12 execution wall deadline exceeded")
            events = selector.select(timeout=min(float(SAMPLE_SECONDS), remaining))
            epoch = int(time.time())
            for role, worker in workers.items():
                if role in completions:
                    continue
                if time.monotonic() >= deadlines[role]:
                    raise LaunchRefusal(f"{role} exact execution wall deadline exceeded")
                _sample_worker(worker, epoch, policy, runtime[role])
            _sample_disk(epoch, expected_filesystem, policy, disk, execution_guard)
            for key, _mask in events:
                role = key.data
                worker = workers[role]
                remaining = deadlines[role] - time.monotonic()
                if remaining <= 0:
                    raise LaunchRefusal(f"{role} exact execution wall deadline exceeded")
                worker.channel.settimeout(min(5.0, remaining))
                completion, _raw = receive_frame(worker.channel, f"{role} COMPLETION")
                coordinator.admit_worker_completion(completion)
                _publish(WIRE_PATHS[f"completion:{role}"], completion)
                assert worker.token is not None and worker.ready is not None
                final_epoch = int(time.time())
                _sample_worker(worker, final_epoch, policy, runtime[role])
                try:
                    if worker.channel.recv(1) != b"":
                        raise LaunchRefusal(f"{role} sent trailing completion bytes")
                except socket.timeout as error:
                    raise LaunchRefusal(f"{role} did not half-close after completion") from error
                selector.unregister(worker.channel)
                worker.channel.close()
                completions[role] = completion
                worker.completed = True

        final_epoch = int(time.time())
        _sample_disk(final_epoch, expected_filesystem, policy, disk, execution_guard)
        exit_codes: dict[str, int] = {}
        for role in ROLES:
            try:
                exit_codes[role] = workers[role].process.wait(timeout=30)
            except subprocess.TimeoutExpired as error:
                raise LaunchRefusal(f"{role} did not exit after completion EOF") from error

        telemetry = {
            "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
            "classification": "COMPLETE_SHARED_L12_TELEMETRY",
            "shared_gate_sha256": coordinator.accepted_sha256("schedule"),
            "schedule_audit_sha256": coordinator.accepted_sha256("schedule_audit"),
            "dual_launch_handshake_sha256": coordinator.accepted_sha256("handshake"),
            "worker_release_sha256": coordinator.accepted_sha256("release"),
            "authorization_sha256_by_role": {
                role: coordinator.accepted_sha256(role) for role in ROLES
            },
            "worker_identity_by_role": {
                role: {
                    key: ready[role][key] for key in (
                        "worker_id", "process_id", "process_start_token",
                        "executable_path", "executable_sha256", "control_channel_id",
                        "nonce_commitment_sha256",
                    )
                } for role in ROLES
            },
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
            "completion_epoch_by_role": {
                role: completions[role]["completion_epoch"] for role in ROLES
            },
            "wall_seconds_by_role": {
                role: float(
                    int(completions[role]["completion_epoch"]) - release_epochs[role]
                ) for role in ROLES
            },
            "peak_rss_bytes_by_role": {
                role: max(int(row["rss_bytes"]) for row in runtime[role])
                for role in ROLES
            },
            "rss_peak_semantics": RSS_PEAK_SEMANTICS,
            "peak_mapped_bytes_by_role": {
                role: MAPPED_CERTIFICATE for role in ROLES
            },
            "mapped_peak_semantics": (
                "CONSERVATIVE_AUTHENTICATION_CACHE_CERTIFICATE__"
                "NOT_OS_VIRTUAL_MEMORY"
            ),
            "runtime_samples_by_role": runtime,
            "free_disk_bytes_samples": disk,
            "exit_code_by_role": exit_codes,
            "output_path_by_role": {
                role: completions[role]["output_path"] for role in ROLES
            },
            "output_sha256_by_role": {
                role: completions[role]["output_sha256"] for role in ROLES
            },
            "claim_boundary": "POSTRUN_RUNTIME_EVIDENCE_ONLY__NO_FINAL_L12_ADJUDICATION",
        }
        coordinator.admit_postrun_telemetry(telemetry)
        publisher = StageEvidencePublisher(validate_artifact)
        digest = publisher.publish_a23(str(TELEMETRY), telemetry, coordinator)
        for item in retained:
            item.verify()
        _guard_phase(execution_guard, "final")
        return digest
    except BaseException as error:
        primary_error = error
        for worker in workers.values():
            try:
                _terminate_exact(worker)
            except BaseException:
                pass
        raise
    finally:
        if selector is not None:
            selector.close()
        for worker in workers.values():
            try:
                worker.channel.close()
            except OSError:
                pass
        for descriptor in log_descriptors:
            try:
                os.fsync(descriptor)
                os.fchmod(descriptor, 0o444)
                os.close(descriptor)
            except OSError:
                pass
        try:
            _close_all(retained)
        except BaseException:
            if primary_error is None:
                raise


def main() -> int:
    if sys.argv[1:] != ["execute"]:
        print("REFUSED: exact invocation is production_dual_l12_launcher.py execute", file=sys.stderr)
        return 2
    try:
        digest = execute()
    except BaseException as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(f"PASS_DUAL_L12_LAUNCH telemetry_sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
