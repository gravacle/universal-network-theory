#!/usr/bin/env python3
"""Hard-locked target V012 portable consumer for authenticated storage-only indices."""

from __future__ import annotations

import argparse
import ctypes
import gc
import hashlib
import itertools
import json
import math
import os
import resource
import shutil
import socket
import stat
import struct
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V004_DIR = ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
sys.path.insert(0, str(V004_DIR))
import compute_prefix_history_v004 as v004  # noqa: E402
sys.path.insert(0, str(HERE))
import build_target_cache as builder  # noqa: E402


METHOD = HERE / "METHOD.md"
FREEZE = HERE / "FREEZE.json"
PREFLIGHT = HERE / "validate_preflight.py"
PHYSICAL_GATE = HERE / "PHYSICAL_EXECUTION_GATE_V012.json"
CONTROL_AUTHORIZATION_GATE = HERE / "CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json"
POSTBUILD_PAYLOAD_AUDIT = ROOT / builder.FUTURE_POSTBUILD_AUDIT_PATH
PHYSICAL_GATE_HOSTILE_AUDIT = ROOT / builder.FUTURE_PHYSICAL_GATE_AUDIT_PATH
CACHED_CONTROL_GATE = HERE / "CACHED_CONTROL_L4_L8_GATE_V012.json"
CACHED_CONTROL_GATE_AUDIT = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json"
L10_EXECUTION_AUTHORIZATION_GATE = HERE / "L10_EXECUTION_AUTHORIZATION_GATE_V012.json"
CACHED_L10_GATE = HERE / "CACHED_L10_GATE_V012.json"
CACHED_L10_GATE_AUDIT = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json"
TARGET_L12_EXECUTION_GATE = HERE / "TARGET_L12_EXECUTION_GATE_V012.json"
PARALLEL_L12_SHARED_DIR = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
PARALLEL_L12_SCHEDULE_GATE = PARALLEL_L12_SHARED_DIR / "SHARED_AGGREGATE_SCHEDULE_GATE_V001.json"
PARALLEL_L12_SCHEDULE_AUDIT = PARALLEL_L12_SHARED_DIR / "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json"
TARGET_HOSTILE_L10_CROSS_GATE = PARALLEL_L12_SHARED_DIR / "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
PARALLEL_L12_TELEMETRY = PARALLEL_L12_SHARED_DIR / "SHARED_AGGREGATE_TELEMETRY_V001.json"
HOSTILE_L12_EXECUTION_GATE = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json"
)
HOSTILE_L10_EXECUTION_GATE = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json"
)
DUAL_L12_LAUNCH_HANDSHAKE = PARALLEL_L12_SHARED_DIR / "DUAL_L12_LAUNCH_HANDSHAKE_V002.json"
DUAL_L12_WORKER_RELEASE = PARALLEL_L12_SHARED_DIR / "DUAL_L12_WORKER_RELEASE_V002.json"
PHYSICAL_OUTPUT_PARENT = HERE / "PHYSICAL_OUTPUTS"
WORKSPACE_PARENT = HERE / "WORKSPACES"
WORD_DTYPE = np.dtype("<u4")
OFFSET_DTYPE = np.dtype("<u8")
INDEX_DTYPE = np.dtype("<i4")
ORIGINAL_FIXED_WORDS = v004.sealed.fixed_words
ORIGINAL_SECTOR = v004.sealed.Sector
ORIGINAL_CREATE_ADMITTED = v004.create_admitted
ORIGINAL_TERMINAL_STREAM = v004.terminal_stream
ORIGINAL_ENGINE_WALL_LIMIT = v004.WALL_LIMIT
CACHE: "CacheContext | None" = None
PHYSICAL_STARTED: float | None = None
LAST_RESOURCE_CHECK = 0.0
PROCESS_START_EPOCH = int(time.time())
AUTHORITY_CUSTODY: builder.StableAuthorityCustody | None = None
ORCHESTRATED_SESSION: "OrchestratedWorkerSession | None" = None

WIRE_MAX_BYTES = 16 * 1024
READY_SCHEMA = "V012_L12_WORKER_READY_V001"
RELEASE_SCHEMA = "V012_L12_WORKER_RELEASE_COMMAND_V001"
ACK_SCHEMA = "V012_L12_WORKER_RELEASE_ACK_V001"
COMPLETION_SCHEMA = "V012_L12_WORKER_COMPLETION_V001"
NONCE_DOMAIN = b"V012_L12_WORKER_NONCE_V001\0"
PROCESS_START_DOMAIN = b"V012_L12_PROCESS_START_V001\0"
ACK_DOMAIN = b"V012_DUAL_L12_RELEASE_ACK_V001\0"

HOSTILE_FREEZE_SCHEMA = "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4"
HOSTILE_FREEZE_STATUS = "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT"
HOSTILE_FREEZE_CLAIM = (
    "V004R4_CROSS_BRANCH_STORAGE_CONTROL_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"
)
HOSTILE_PREFLIGHT_SCHEMA = "HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT_V001"
HOSTILE_PREFLIGHT_CLASSIFICATION = "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT"
HOSTILE_PREFLIGHT_CLAIM = (
    "NONPHYSICAL_V004R4_PREFLIGHT_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"
)
HOSTILE_AUDIT_CLAIM = "NONPHYSICAL_V004R4_CONTROL_PLANE_AUDIT_ONLY"
HOSTILE_EXECUTED_DEPENDENCY_NAMES = (
    "independent_prefix_history.py",
    "independent_prefix_history_v002.py",
    "independent_prefix_history_v003.py",
    "independent_prefix_history_v004.py",
    "independent_prefix_history_v004r2.py",
    "v004r2_common.py",
    "validate_v004r4_zero_length_preflight.py",
    "v004r4_cache_io.py",
)
BASE_PHYSICAL_GATE_KEYS = frozenset({
    "schema", "classification", "dual_obstruction_gate_sha256",
    "consumer_sha256", "builder_sha256", "preflight_sha256",
    "method_sha256", "freeze_sha256", "target_v004_sha256",
    "original_target_l12_gate_sha256", "preserved_workspace_custody_sha256",
    "preserved_workspace_cross_diagnostic_sha256",
    "runtime_compatibility_obstruction_sha256",
    "v006_hostile_audit_obstruction_sha256",
    "v007_runtime_compatibility_obstruction_sha256",
    "v008_postbuild_audit_binding_obstruction_sha256",
    "v009_hostile_audit_obstruction_sha256",
    "v010_hostile_audit_obstruction_sha256",
    "v010_audit_record_custody_correction_sha256",
    "v011_hostile_audit_obstruction_sha256",
    "preflight_result_sha256",
    "independent_hostile_audit_sha256", "authorized_lengths",
    "cache_manifest_sha256_by_L", "postbuild_payload_audit",
    "claim_boundary",
})
BASE_PHYSICAL_GATE_KEY_CENSUS_SHA256 = hashlib.sha256(
    json.dumps(sorted(BASE_PHYSICAL_GATE_KEYS), separators=(",", ":")).encode("utf-8")
).hexdigest()
CANONICAL_V004_HISTORY_SHA256 = {
    4: "8bf8f4eb54781c599a9fb3ae407207e08504396128c82e1e838d5b47a1d564b2",
    6: "06ccf6f419b8e743c6aea014c90ba1598786fc5bb28331488cde0f0846215f33",
    8: "affc775a91186883b5dd7c7180340b06105523ad5744c38a470331c1a631868a",
    10: "873e45b6b37654910947711af1d8dc93d0def8ea0ef994587db206ab47b4267c",
}
CANONICAL_V004_HISTORY_PATH = {
    4: V004_DIR / "CONTROL_HISTORY/TARGET_V004_L4.json",
    6: V004_DIR / "CONTROL_HISTORY/TARGET_V004_L6.json",
    8: V004_DIR / "CONTROL_HISTORY/TARGET_V004_L8.json",
    10: V004_DIR / "BENCHMARK/TARGET_V004_QSHARD_L10.json",
}


class Refusal(RuntimeError):
    pass


def _wire_canonical_json(record: object) -> bytes:
    try:
        return (
            json.dumps(
                record, sort_keys=True, separators=(",", ":"),
                ensure_ascii=True, allow_nan=False,
            ) + "\n"
        ).encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("orchestrator wire record is not finite canonical JSON") from error


def _wire_json(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        output: dict[str, object] = {}
        for key, value in items:
            if key in output:
                raise Refusal(f"{label} duplicate JSON key")
            output[key] = value
        return output

    def constant(token: str) -> object:
        raise Refusal(f"{label} nonfinite constant: {token}")

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs, parse_constant=constant,
        )
    except Refusal:
        raise
    except (UnicodeDecodeError, ValueError, TypeError) as error:
        raise Refusal(f"{label} malformed JSON") from error
    if type(value) is not dict or _wire_canonical_json(value) != raw:
        raise Refusal(f"{label} is not one canonical JSON object")
    return value


def _process_start_token(process_id: int) -> str:
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
    stamp = f"{record.start_seconds}.{record.start_microseconds:06d}".encode("ascii")
    return hashlib.sha256(
        PROCESS_START_DOMAIN + str(process_id).encode("ascii") + b"\0" + stamp
    ).hexdigest()


class OrchestratedWorkerSession:
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
        self, *, worker_id: str, control_fd: int, control_channel_id: str,
        executable: Path, workspace: Path, output: Path,
    ) -> None:
        if type(worker_id) is not str or not worker_id or len(worker_id) > 256:
            raise Refusal("target orchestrated worker id is malformed")
        if not _sha256_text(control_channel_id):
            raise Refusal("target control channel id is malformed")
        if type(control_fd) is not int or control_fd < 3:
            raise Refusal("target control descriptor is invalid")
        metadata = os.fstat(control_fd)
        if not stat.S_ISSOCK(metadata.st_mode):
            raise Refusal("target control descriptor is not a socket")
        self.channel = socket.socket(fileno=os.dup(control_fd))
        if self.channel.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE) != socket.SOCK_STREAM:
            self.channel.close()
            raise Refusal("target control channel is not a duplex stream socket")
        try:
            self.channel.getpeername()
        except OSError as error:
            self.channel.close()
            raise Refusal("target control channel has no connected peer") from error
        self.channel.settimeout(300.0)
        self.role = "target_v012"
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
            raise Refusal("target worker workspace/output exists before READY")
        self.process_id = os.getpid()
        self.process_start_token = _process_start_token(self.process_id)
        self.nonce = os.urandom(32)
        self.nonce_commitment_sha256 = hashlib.sha256(
            NONCE_DOMAIN + self.nonce
        ).hexdigest()
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.executable_fd = os.open(executable, flags)
        executable_metadata = os.fstat(self.executable_fd)
        if not stat.S_ISREG(executable_metadata.st_mode):
            self.close()
            raise Refusal("target worker executable is not an ordinary file")
        self.executable_identity = (
            executable_metadata.st_dev, executable_metadata.st_ino,
            executable_metadata.st_size, executable_metadata.st_mtime_ns,
            executable_metadata.st_ctime_ns,
        )
        self.executable_sha256 = descriptor_sha256(self.executable_fd)
        self.ready = {
            "schema": READY_SCHEMA,
            "role": self.role,
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
        if set(self.ready) != self.READY_KEYS:
            self.close()
            raise Refusal("target READY key census mismatch")
        try:
            builder.validate_production_obligation(
                "A22_TARGET_L12_AUTHORIZATION", self.ready,
            )
        except BaseException:
            self.close()
            raise
        self.ready_bytes = _wire_canonical_json(self.ready)
        if len(self.ready_bytes) > WIRE_MAX_BYTES:
            self.close()
            raise Refusal("target READY exceeds wire bound")
        self.ready_sha256 = hashlib.sha256(self.ready_bytes).hexdigest()
        self.release: dict[str, object] | None = None
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
            raise Refusal("target worker executable identity changed")

    def _receive(self) -> tuple[dict[str, object], bytes]:
        data = bytearray()
        while b"\n" not in data:
            try:
                block = self.channel.recv(4096)
            except socket.timeout as error:
                raise Refusal("target worker release command timed out") from error
            if not block:
                raise Refusal("target control channel closed before release")
            data.extend(block)
            if len(data) > WIRE_MAX_BYTES:
                raise Refusal("target worker release command exceeds wire bound")
        line, trailing = bytes(data).split(b"\n", 1)
        if trailing:
            raise Refusal("target control channel sent trailing records")
        raw = line + b"\n"
        return _wire_json(raw, "target worker RELEASE"), raw

    def announce_and_wait(self) -> dict[str, object]:
        self._verify_executable()
        self.channel.sendall(self.ready_bytes)
        record, raw = self._receive()
        if set(record) != self.RELEASE_KEYS or (
            record.get("schema") != RELEASE_SCHEMA
            or record.get("role") != self.role
            or record.get("worker_id") != self.worker_id
            or record.get("process_id") != self.process_id
            or record.get("process_start_token") != self.process_start_token
            or record.get("control_channel_id") != self.control_channel_id
            or record.get("nonce_commitment_sha256") != self.nonce_commitment_sha256
            or not _sha256_text(record.get("handshake_sha256"))
            or not _sha256_text(record.get("worker_release_sha256"))
            or not _positive_integer(record.get("release_epoch"))
        ):
            raise Refusal("target worker RELEASE identity/binding mismatch")
        builder.validate_production_obligation(
            "A22_TARGET_L12_AUTHORIZATION", record,
        )
        self.release = record
        self.release_bytes = raw
        return record

    def acknowledge(self) -> dict[str, object]:
        if self.release is None or self.release_bytes is None or self.acked:
            raise Refusal("target worker release ACK state mismatch")
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
        if set(ack) != self.ACK_KEYS:
            raise Refusal("target release ACK key census mismatch")
        builder.validate_production_obligation(
            "A22_TARGET_L12_AUTHORIZATION", ack,
        )
        self.channel.sendall(_wire_canonical_json(ack))
        self.acked = True
        return ack

    @staticmethod
    def _require_no_symlink_parents(path: Path) -> None:
        if not path.is_absolute():
            raise Refusal("target worker output path is not absolute")
        candidate = path.parent
        while True:
            metadata = os.lstat(candidate)
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                raise Refusal("target worker output has a symlinked/non-directory parent")
            if candidate.parent == candidate:
                return
            candidate = candidate.parent

    def complete(self, output_sha256: str) -> dict[str, object]:
        """Authenticate the published output and block live until coordinator EOF."""
        if self.release is None or not self.acked or self.completed:
            raise Refusal("target worker completion state mismatch")
        if not _sha256_text(output_sha256):
            raise Refusal("target worker completion output hash is malformed")
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
            parent_before = _retained_directory_identity(
                self.output.parent, parent_descriptor,
                "target worker completion",
            )
            descriptor = os.open(
                self.output.name, flags, dir_fd=parent_descriptor,
            )
            opened = os.fstat(descriptor)
            current = os.stat(
                self.output.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            identity = _cache_file_identity(opened)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_mode & 0o222
                or opened.st_nlink != 1
                or identity != _cache_file_identity(current)
            ):
                raise Refusal("target worker completion output authentication failed")
            digest = descriptor_sha256(descriptor)
            opened_after_hash = os.fstat(descriptor)
            current_after_hash = os.stat(
                self.output.name, dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                digest != output_sha256
                or _cache_file_identity(opened_after_hash) != identity
                or _cache_file_identity(current_after_hash) != identity
                or _retained_directory_identity(
                    self.output.parent, parent_descriptor,
                    "target worker completion",
                ) != parent_before
            ):
                raise Refusal("target worker completion output authentication failed")
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
            if set(completion) != self.COMPLETION_KEYS:
                raise Refusal("target worker COMPLETION key census mismatch")
            builder.validate_production_obligation(
                "A22_TARGET_L12_AUTHORIZATION", completion,
            )
            wire = _wire_canonical_json(completion)
            if len(wire) > 2**20:
                raise Refusal("target worker COMPLETION exceeds wire bound")
            self.channel.sendall(wire)
            self.channel.shutdown(socket.SHUT_WR)
            try:
                trailing = self.channel.recv(1)
            except socket.timeout as error:
                raise Refusal(
                    "target orchestrator did not close after worker COMPLETION"
                ) from error
            if trailing:
                raise Refusal("target orchestrator sent bytes after worker COMPLETION")
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
                _retained_directory_identity(
                    self.output.parent, parent_descriptor,
                    "target worker completion",
                ) != parent_before
                or _cache_file_identity(final) != identity
                or _cache_file_identity(final_path) != identity
                or _cache_file_identity(final_after_hash) != identity
                or _cache_file_identity(final_path_after_hash) != identity
                or final.st_mode & 0o222
                or final.st_nlink != 1
                or final_digest != output_sha256
            ):
                raise Refusal("target worker completion output custody changed before EOF")
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


def _cache_file_identity(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int]:
    """Exact identity used by the Stage-1 retained cache/output custody gate."""
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        metadata.st_mode,
    )


def _retained_directory_identity(
    path: Path, descriptor: int, label: str,
) -> tuple[int, int, int, int, int, int, int]:
    """Bind a retained directory descriptor to its exact unsymlinked path."""
    text = str(path)
    if not path.is_absolute() or str(Path(text)) != text or os.path.normpath(text) != text:
        raise Refusal(f"{label} directory path is not canonical absolute")
    cursor = Path(path.anchor)
    for component in path.parts[1:]:
        cursor /= component
        metadata = os.stat(cursor, follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise Refusal(f"{label} directory path is aliased")
    retained = os.fstat(descriptor)
    current = os.stat(path, follow_symlinks=False)
    retained_identity = _cache_file_identity(retained)
    if (
        not stat.S_ISDIR(retained.st_mode)
        or not stat.S_ISDIR(current.st_mode)
        or retained_identity != _cache_file_identity(current)
    ):
        raise Refusal(f"{label} directory identity changed")
    return retained_identity


def sha256(path: Path) -> str:
    if AUTHORITY_CUSTODY is not None and AUTHORITY_CUSTODY.has(path):
        return AUTHORITY_CUSTODY.digest(path, f"retained authority {path.name}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def open_stable_readonly(path: Path) -> int:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    metadata = os.fstat(descriptor)
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o222:
        os.close(descriptor)
        raise Refusal(f"stable cache member is not an immutable ordinary file: {path.name}")
    return descriptor


def descriptor_sha256(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while block := os.pread(descriptor, 16 * 2**20, offset):
        digest.update(block)
        offset += len(block)
        if PHYSICAL_STARTED is not None:
            guard_consumer()
    return digest.hexdigest()


def descriptor_json(descriptor: int) -> dict[str, object]:
    size = os.fstat(descriptor).st_size
    raw = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(descriptor, min(2**20, size - offset), offset)
        if not block:
            break
        raw.extend(block)
        offset += len(block)
    def exact_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise Refusal(f"duplicate JSON key: {key}")
            value[key] = item
        return value

    def reject_constant(token: str) -> object:
        raise Refusal(f"nonfinite JSON constant: {token}")

    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=exact_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise Refusal("cache manifest is not an object")
    return value


def immutable_json(
    path: Path, label: str, expected_sha256: str | None = None,
    require_immutable_mode: bool = True,
) -> tuple[dict[str, object], str]:
    retained = AUTHORITY_CUSTODY is not None
    if retained:
        try:
            descriptor, digest = AUTHORITY_CUSTODY.authenticate(
                path, label, expected_sha256, require_immutable_mode
            )
        except builder.Refusal as error:
            raise Refusal(str(error)) from error
    else:
        if path.is_symlink() or not path.is_file():
            raise Refusal(f"{label} immutable ordinary file absent")
        if require_immutable_mode:
            descriptor = open_stable_readonly(path)
        else:
            flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(path, flags)
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                os.close(descriptor)
                raise Refusal(f"{label} is not an ordinary file")
    try:
        before = os.fstat(descriptor)
        parsed_digest = descriptor_sha256(descriptor)
        if retained and parsed_digest != digest:
            raise Refusal(f"{label} retained descriptor digest mismatch")
        digest = parsed_digest
        if expected_sha256 is not None and digest != expected_sha256:
            raise Refusal(f"{label} hash mismatch")
        record = descriptor_json(descriptor)
        after = os.fstat(descriptor)
        if (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        ) != (
            after.st_dev, after.st_ino, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        ) or descriptor_sha256(descriptor) != digest:
            raise Refusal(f"{label} descriptor changed during authentication")
        if retained:
            try:
                AUTHORITY_CUSTODY.verify_one(path, label)
            except builder.Refusal as error:
                raise Refusal(str(error)) from error
        return record, digest
    finally:
        if not retained:
            os.close(descriptor)


def close_mapping(array: np.ndarray) -> None:
    mapping = getattr(array, "_mmap", None)
    if mapping is not None:
        mapping.close()


def guard_consumer(force: bool = False) -> None:
    global LAST_RESOURCE_CHECK
    if PHYSICAL_STARTED is None:
        return
    now = time.monotonic()
    if not force and now - LAST_RESOURCE_CHECK < 1.0:
        return
    LAST_RESOURCE_CHECK = now
    if builder.rss_bytes() > v004.RSS_LIMIT:
        raise MemoryError("cached physical consumer RSS guard exceeded")
    if now - PHYSICAL_STARTED > builder.WALL_LIMIT:
        raise TimeoutError("cached physical consumer wall guard exceeded")


def expected_records(length: int) -> dict[str, tuple[str, tuple[int, ...], dict[str, object]]]:
    records: dict[str, tuple[str, tuple[int, ...], dict[str, object]]] = {}
    for q in range(length + 1):
        pair_count = 3 * length * (math.comb(2 * length - 2, q - 1) if q else 0)
        records[f"carrier_q_{q:02d}_words.u32"] = (WORD_DTYPE.str, (math.comb(2 * length, q),), {"kind": "operator", "q": q, "role": "words"})
        records[f"carrier_q_{q:02d}_offsets.u64"] = (OFFSET_DTYPE.str, (3 * length + 1,), {"kind": "operator", "q": q, "role": "offsets"})
        records[f"carrier_q_{q:02d}_sources.i32"] = (INDEX_DTYPE.str, (pair_count,), {"kind": "operator", "q": q, "role": "sources"})
        records[f"carrier_q_{q:02d}_targets.i32"] = (INDEX_DTYPE.str, (pair_count,), {"kind": "operator", "q": q, "role": "targets"})
    for event in range(length):
        for q in range(event + 1):
            shape = (math.comb(2 * length - 1, q),)
            for role in ("blank", "destination"):
                records[f"admission_n_{event:02d}_q_{q:02d}_{role}.i32"] = (
                    INDEX_DTYPE.str,
                    shape,
                    {"kind": "admission", "event": event, "q": q, "role": role},
                )
    for prefix in range(length):
        for q in range(prefix + 1):
            records[f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32"] = (
                WORD_DTYPE.str,
                (math.comb(prefix, q),),
                {"kind": "lineage_mask", "prefix": prefix, "q": q, "role": "words"},
            )
    for prefix in range(length - 1):
        for q in range(prefix + 1):
            for role in ("stay", "accepted"):
                records[f"lineage_n_{prefix:02d}_q_{q:02d}_{role}.i32"] = (
                    INDEX_DTYPE.str,
                    (math.comb(prefix, q),),
                    {"kind": "lineage_map", "prefix": prefix, "q": q, "role": role},
                )
    return records


class CacheContext:
    def __init__(self, root: Path, length: int, manifest_sha256: str):
        self.descriptors: dict[str, int] = {}
        self.identities: dict[
            str, tuple[int, int, int, int, int, int, int]
        ] = {}
        self.manifest_descriptor: int | None = None
        self.root_descriptor = -1
        self.closed = False
        freeze = builder.require_frozen_census()
        expected_root = builder.CACHE_PARENT / f"L{length}"
        if (
            root != expected_root
            or not root.is_absolute()
            or str(Path(str(root))) != str(root)
            or builder.CACHE_PARENT.is_symlink()
            or root.is_symlink()
            or not root.is_dir()
        ):
            raise Refusal("cache root is not the canonical packet-local payload")
        root_flags = (
            os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        self.root_descriptor = os.open(root, root_flags)
        self.directory_identity = _retained_directory_identity(
            root, self.root_descriptor, "target cache root",
        )
        if self.directory_identity[6] & 0o222:
            raise Refusal("cache root is writable")
        self.manifest_descriptor, self.manifest_identity = self._open_cache_member(
            "CACHE_MANIFEST.json", None,
        )
        if descriptor_sha256(self.manifest_descriptor) != manifest_sha256:
            raise Refusal("cache manifest custody mismatch")
        manifest = descriptor_json(self.manifest_descriptor)
        manifest_keys = {
            "schema", "status", "L", "basis_order", "lineage_identity",
            "edge_layout", "hamiltonian_exchange_coefficient", "files",
            "payload", "resource_certificates", "builder_sha256",
            "consumer_sha256", "preflight_sha256", "method_sha256",
            "production_obligation_validators_sha256",
            "freeze_sha256", "dual_obstruction_gate_sha256",
            "target_v004_sha256", "target_v004_original_l12_gate_sha256",
            "hostile_v003_sha256", "target_v004_method_sha256",
            "target_v004_freeze_sha256", "hostile_v003_method_sha256",
            "hostile_v003_freeze_sha256", "preserved_workspace_custody_sha256",
            "preserved_workspace_cross_diagnostic_sha256",
            "runtime_compatibility_obstruction_sha256",
            "v006_hostile_audit_obstruction_sha256",
            "v007_runtime_compatibility_obstruction_sha256",
            "v008_postbuild_audit_binding_obstruction_sha256",
            "v009_hostile_audit_obstruction_sha256",
            "v010_hostile_audit_obstruction_sha256",
            "v010_audit_record_custody_correction_sha256",
            "v011_hostile_audit_obstruction_sha256", "preflight_result_sha256",
            "independent_hostile_audit_sha256", "superseded_v005_dual_gate_sha256",
            "superseded_v005_cache_manifest_sha256_by_L",
            "superseded_v007_dual_gate_sha256",
            "superseded_v007_cache_manifest_sha256_by_L",
            "superseded_v008_dual_gate_sha256",
            "superseded_v008_cache_manifest_sha256_by_L",
            "canonical_cache_root", "claim_boundary",
        }
        if (
            set(manifest) != manifest_keys
            or manifest.get("schema") != "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012"
            or manifest.get("status") != "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE"
            or type(manifest.get("L")) is not int
            or manifest.get("L") != length
            or manifest.get("basis_order") != "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER"
            or manifest.get("lineage_identity") != "FULL_CANONICAL_MASK"
            or type(manifest.get("hamiltonian_exchange_coefficient")) is not int
            or manifest.get("hamiltonian_exchange_coefficient") != -1
            or manifest.get("claim_boundary")
            != "TARGET_V012_PORTABLE_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_OR_GRAVITY"
        ):
            raise Refusal("cache manifest identity mismatch")
        if (
            manifest.get("edge_layout") != [list(edge) for edge in v004.sealed.graph(length)]
            or any(
                not isinstance(edge, list)
                or len(edge) != 3
                or type(edge[0]) is not int
                or type(edge[1]) is not int
                or not isinstance(edge[2], str)
                for edge in manifest.get("edge_layout", [])
            )
        ):
            raise Refusal("cache graph/edge order mismatch")
        required_hashes = {
            "builder_sha256": freeze["files"]["build_target_cache.py"],
            "consumer_sha256": freeze["files"]["consume_target_cache.py"],
            "preflight_sha256": freeze["files"]["validate_preflight.py"],
            "method_sha256": freeze["files"]["METHOD.md"],
            "production_obligation_validators_sha256": freeze["files"][
                "production_obligation_validators.py"
            ],
            "freeze_sha256": sha256(FREEZE),
            "dual_obstruction_gate_sha256": sha256(builder.DUAL_GATE),
            "target_v004_sha256": builder.TARGET_V004_SHA256,
            "hostile_v003_sha256": builder.HOSTILE_V003_SHA256,
            "target_v004_original_l12_gate_sha256": builder.TARGET_L12_GATE_V004_SHA256,
            "target_v004_method_sha256": builder.TARGET_METHOD_V004_SHA256,
            "target_v004_freeze_sha256": builder.TARGET_FREEZE_V004_SHA256,
            "hostile_v003_method_sha256": builder.HOSTILE_METHOD_V003_SHA256,
            "hostile_v003_freeze_sha256": builder.HOSTILE_FREEZE_V003_SHA256,
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
            "preflight_result_sha256": sha256(HERE / "PREFLIGHT_RESULT_V001.json"),
            "independent_hostile_audit_sha256": immutable_json(
                builder.DUAL_GATE, "dual authorization gate"
            )[0]["independent_hostile_audit"]["sha256"],
            "superseded_v005_dual_gate_sha256": builder.V005_DUAL_GATE_SHA256,
            "superseded_v007_dual_gate_sha256": builder.V007_DUAL_GATE_SHA256,
            "superseded_v008_dual_gate_sha256": builder.V008_DUAL_GATE_SHA256,
        }
        for key, expected in required_hashes.items():
            if manifest.get(key) != expected:
                raise Refusal(f"cache manifest does not pin {key}")
        if (
            manifest.get("superseded_v005_cache_manifest_sha256_by_L")
            != builder.V005_CACHE_MANIFEST_SHA256
            or manifest.get("superseded_v007_cache_manifest_sha256_by_L")
            != builder.V007_CACHE_MANIFEST_SHA256
            or manifest.get("superseded_v008_cache_manifest_sha256_by_L")
            != builder.V008_CACHE_MANIFEST_SHA256
            or manifest.get("canonical_cache_root") != str(root)
        ):
            raise Refusal("cache manifest predecessor/canonical-root binding mismatch")
        expected = expected_records(length)
        expected_members = set(expected) | {"CACHE_MANIFEST.json"}
        actual_members = os.listdir(self.root_descriptor)
        if (
            set(actual_members) != expected_members
            or len(actual_members) != len(expected_members)
            or any(
                not stat.S_ISREG(os.stat(
                    name, dir_fd=self.root_descriptor, follow_symlinks=False,
                ).st_mode)
                or os.stat(
                    name, dir_fd=self.root_descriptor, follow_symlinks=False,
                ).st_mode & 0o222
                for name in actual_members
            )
        ):
            raise Refusal("cache directory has extra, missing, non-file, or symlink members")
        rows = manifest.get("files")
        if not isinstance(rows, list) or len(rows) != len(expected):
            raise Refusal("cache file census mismatch")
        records: dict[str, dict[str, object]] = {}
        total_bytes = 0
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("path"), str) or row["path"] in records:
                raise Refusal("cache file record malformed or duplicated")
            name = row["path"]
            specification = expected.get(name)
            if specification is None:
                raise Refusal("unexpected cache file record")
            dtype, shape, metadata = specification
            row_keys = {"path", "dtype", "shape", "bytes", "sha256"} | set(metadata)
            if set(row) != row_keys:
                raise Refusal(f"cache file record key census mismatch: {name}")
            if (
                row.get("dtype") != dtype
                or row.get("shape") != list(shape)
                or any(type(value) is not int for value in row.get("shape", []))
                or not isinstance(row.get("sha256"), str)
                or len(row["sha256"]) != 64
                or any(character not in "0123456789abcdef" for character in row["sha256"])
            ):
                raise Refusal(f"cache dtype/shape mismatch: {name}")
            if any(
                row.get(key) != value or type(row.get(key)) is not type(value)
                for key, value in metadata.items()
            ):
                raise Refusal(f"cache metadata mismatch: {name}")
            expected_bytes = math.prod(shape) * np.dtype(dtype).itemsize
            if type(row.get("bytes")) is not int or row["bytes"] != expected_bytes:
                raise Refusal(f"cache byte record mismatch: {name}")
            descriptor, identity = self._open_cache_member(name, expected_bytes)
            if (
                descriptor_sha256(descriptor) != row.get("sha256")
                or not self._member_identity_matches(name, descriptor, identity)
            ):
                os.close(descriptor)
                raise Refusal(f"cache member custody mismatch: {name}")
            self.descriptors[name] = descriptor
            self.identities[name] = identity
            records[name] = row
            total_bytes += expected_bytes
        if set(records) != set(expected):
            raise Refusal("cache file set is incomplete")
        payload = manifest.get("payload")
        expected_payload = {
            "operator_bytes": builder.operator_bytes(length),
            "admission_bytes": builder.admission_bytes(length),
            "lineage_mask_bytes": builder.lineage_mask_bytes(length),
            "lineage_map_bytes": builder.lineage_map_bytes(length),
            "total_bytes": builder.payload_bytes(length),
            "file_count": builder.expected_file_count(length),
        }
        if (
            payload != expected_payload
            or any(type(value) is not int for value in payload.values())
            or total_bytes != builder.payload_bytes(length)
        ):
            raise Refusal("cache payload arithmetic mismatch")
        resources = manifest.get("resource_certificates")
        expected_resources = {
            "maximum_live_state_bytes": builder.maximum_state_file_bytes(length),
            "state_plus_cache_bytes": builder.maximum_state_file_bytes(length) + builder.payload_bytes(length),
            "overhead_reserve_bytes": builder.OVERHEAD_RESERVE,
            "maximum_cache_window_bytes": builder.maximum_cache_window_bytes(length),
            "terminal_cache_peak_bytes": builder.terminal_cache_peak_bytes(length),
            "authentication_cache_peak_bytes": builder.authentication_cache_peak_bytes(length),
            "mapped_cache_limit_bytes": builder.MAPPED_CACHE_LIMIT,
            "scratch_limit_bytes": builder.SCRATCH_LIMIT,
            "builder_rss_limit_bytes": builder.BUILDER_RSS_LIMIT,
            "consumer_rss_limit_bytes": v004.RSS_LIMIT,
            "wall_limit_seconds": builder.WALL_LIMIT,
        }
        if (
            resources != expected_resources
            or any(
                type(resources[key]) is not type(value)
                for key, value in expected_resources.items()
            )
        ):
            raise Refusal("cache resource certificate mismatch")
        self.root = root
        self.length = length
        self.manifest_sha256 = manifest_sha256
        self.manifest = manifest
        self.records = records
        self.edges = v004.sealed.graph(length)
        self.validate_index_identities()
        self.reauthenticate()

    def _open_cache_member(
        self, name: str, expected_size: int | None,
    ) -> tuple[int, tuple[int, int, int, int, int, int, int]]:
        if (
            type(name) is not str or not name or Path(name).name != name
            or "/" in name or "\x00" in name
        ):
            raise Refusal("cache member name is not one canonical component")
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(name, flags, dir_fd=self.root_descriptor)
        try:
            opened = os.fstat(descriptor)
            current = os.stat(
                name, dir_fd=self.root_descriptor, follow_symlinks=False,
            )
            identity = _cache_file_identity(opened)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_mode & 0o222 or opened.st_nlink != 1
                or _cache_file_identity(current) != identity
                or (expected_size is not None and opened.st_size != expected_size)
            ):
                raise Refusal(f"cache member is not immutable owner-once: {name}")
            return descriptor, identity
        except BaseException:
            os.close(descriptor)
            raise

    def _member_identity_matches(
        self, name: str, descriptor: int,
        identity: tuple[int, int, int, int, int, int, int],
    ) -> bool:
        opened = os.fstat(descriptor)
        current = os.stat(
            name, dir_fd=self.root_descriptor, follow_symlinks=False,
        )
        return (
            stat.S_ISREG(opened.st_mode)
            and not opened.st_mode & 0o222 and opened.st_nlink == 1
            and _cache_file_identity(opened) == identity
            and _cache_file_identity(current) == identity
        )

    def validate_index_identities(self) -> None:
        """Exhaustively authenticate storage-only indices without state evolution."""
        carrier: dict[int, np.memmap] = {}
        try:
            for q in range(self.length + 1):
                words = self.carrier_words(q)
                carrier[q] = words
                direct = ORIGINAL_FIXED_WORDS(2 * self.length, q)
                if not np.array_equal(words, direct):
                    raise Refusal("cached carrier masks changed target order or identity")
                offsets = self.open(f"carrier_q_{q:02d}_offsets.u64", OFFSET_DTYPE)
                sources = self.open(f"carrier_q_{q:02d}_sources.i32", INDEX_DTYPE)
                targets = self.open(f"carrier_q_{q:02d}_targets.i32", INDEX_DTYPE)
                per_edge = math.comb(2 * self.length - 2, q - 1) if q else 0
                expected_offsets = np.arange(3 * self.length + 1, dtype=OFFSET_DTYPE) * per_edge
                if not np.array_equal(offsets, expected_offsets):
                    raise Refusal("cached exchange offsets changed exact edge census")
                for edge_index, (u, v, _label) in enumerate(self.edges):
                    lower = int(offsets[edge_index])
                    upper = int(offsets[edge_index + 1])
                    left = sources[lower:upper]
                    right = targets[lower:upper]
                    if (
                        (len(left) and (int(left[0]) < 0 or int(left[-1]) >= len(words)))
                        or (len(right) and (int(np.min(right)) < 0 or int(np.max(right)) >= len(words)))
                        or (len(left) > 1 and not bool(np.all(left[1:] > left[:-1])))
                        or len(np.unique(right)) != len(right)
                    ):
                        raise Refusal("cached exchange ranks are out of range or non-injective")
                    left_words = np.asarray(words[left])
                    if (
                        not bool(np.all(((left_words >> u) & 1) == 1))
                        or not bool(np.all(((left_words >> v) & 1) == 0))
                        or not np.array_equal(np.asarray(words[right]), left_words ^ ((1 << u) | (1 << v)))
                    ):
                        raise Refusal("cached exchange does not implement exact oriented XOR")
                close_mapping(offsets)
                close_mapping(sources)
                close_mapping(targets)
                del direct
            for event in range(self.length):
                for q in range(event + 1):
                    blank, destination = self.admission(event, q)
                    expected_blank = np.flatnonzero(((carrier[q] >> event) & 1) == 0).astype(INDEX_DTYPE)
                    if (
                        not np.array_equal(blank, expected_blank)
                        or (len(destination) and (int(np.min(destination)) < 0 or int(np.max(destination)) >= len(carrier[q + 1])))
                        or len(np.unique(destination)) != len(destination)
                        or not np.array_equal(
                            np.asarray(carrier[q + 1][destination]),
                            np.asarray(carrier[q][blank]) | (1 << event),
                        )
                    ):
                        raise Refusal("cached admission changed fresh-cell projection or exact write map")
                    close_mapping(blank)
                    close_mapping(destination)
            for prefix in range(self.length):
                for q in range(prefix + 1):
                    words = self.lineage_words(prefix, q)
                    direct = ORIGINAL_FIXED_WORDS(prefix, q)
                    if not np.array_equal(words, direct):
                        raise Refusal("cached lineage masks changed canonical identity/order")
                    if prefix < self.length - 1:
                        stay = self.lineage_map(prefix, q, False)
                        accepted = self.lineage_map(prefix, q, True)
                        same_words = self.lineage_words(prefix + 1, q)
                        accepted_words = self.lineage_words(prefix + 1, q + 1)
                        if (
                            (len(stay) and (int(np.min(stay)) < 0 or int(np.max(stay)) >= len(same_words)))
                            or (len(accepted) and (int(np.min(accepted)) < 0 or int(np.max(accepted)) >= len(accepted_words)))
                            or len(np.unique(stay)) != len(stay)
                            or len(np.unique(accepted)) != len(accepted)
                            or not np.array_equal(np.asarray(same_words[stay]), np.asarray(words))
                            or not np.array_equal(
                                np.asarray(accepted_words[accepted]), np.asarray(words) | (1 << prefix)
                            )
                        ):
                            raise Refusal("cached lineage maps changed owner-once mask identity")
                        close_mapping(stay)
                        close_mapping(accepted)
                        close_mapping(same_words)
                        close_mapping(accepted_words)
                    close_mapping(words)
                    del direct
        finally:
            for words in carrier.values():
                close_mapping(words)

    def open(self, name: str, dtype: np.dtype) -> np.ndarray:
        if self.closed:
            raise Refusal("cache descriptor custody is closed")
        row = self.records.get(name)
        if row is None or row.get("dtype") != dtype.str:
            raise Refusal(f"cache array record absent: {name}")
        shape = tuple(row["shape"])
        descriptor = self.descriptors.get(name)
        if descriptor is None:
            raise Refusal(f"cache descriptor absent: {name}")
        metadata = os.fstat(descriptor)
        if (
            _cache_file_identity(metadata) != self.identities[name]
            or not self._member_identity_matches(
                name, descriptor, self.identities[name],
            )
        ):
            raise Refusal(f"cache descriptor identity drift: {name}")
        if math.prod(shape) == 0:
            if metadata.st_size != 0:
                raise Refusal(f"zero-length cache record has nonzero storage: {name}")
            return np.empty(shape, dtype=dtype)
        with os.fdopen(os.dup(descriptor), "rb") as stream:
            return np.memmap(stream, dtype=dtype, mode="r", shape=shape)

    def reauthenticate(self) -> None:
        if (
            self.closed or self.manifest_descriptor is None
            or self.root_descriptor < 0
        ):
            raise Refusal("cache descriptor custody is closed")
        expected_members = set(self.records) | {"CACHE_MANIFEST.json"}
        if (
            _retained_directory_identity(
                self.root, self.root_descriptor, "target cache root",
            ) != self.directory_identity
            or self.directory_identity[6] & 0o222
        ):
            raise Refusal("cache directory custody drifted after authentication")
        actual_members = os.listdir(self.root_descriptor)
        if (
            set(actual_members) != expected_members
            or len(actual_members) != len(expected_members)
        ):
            raise Refusal("cache directory custody drifted after authentication")
        if (
            not self._member_identity_matches(
                "CACHE_MANIFEST.json", self.manifest_descriptor,
                self.manifest_identity,
            )
            or descriptor_sha256(self.manifest_descriptor)
            != self.manifest_sha256
            or not self._member_identity_matches(
                "CACHE_MANIFEST.json", self.manifest_descriptor,
                self.manifest_identity,
            )
        ):
            raise Refusal("cache manifest changed after authentication")
        for name, descriptor in self.descriptors.items():
            if (
                not self._member_identity_matches(
                    name, descriptor, self.identities[name],
                )
                or descriptor_sha256(descriptor) != self.records[name].get("sha256")
                or not self._member_identity_matches(
                    name, descriptor, self.identities[name],
                )
            ):
                raise Refusal(f"cache member changed after authentication: {name}")

    def close(self) -> None:
        if self.closed:
            return
        for descriptor in self.descriptors.values():
            try:
                os.close(descriptor)
            except OSError:
                pass
        self.descriptors.clear()
        if self.manifest_descriptor is not None:
            try:
                os.close(self.manifest_descriptor)
            except OSError:
                pass
            self.manifest_descriptor = None
        if self.root_descriptor >= 0:
            try:
                os.close(self.root_descriptor)
            except OSError:
                pass
            self.root_descriptor = -1
        self.closed = True

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass

    def carrier_words(self, q: int) -> np.memmap:
        return self.open(f"carrier_q_{q:02d}_words.u32", WORD_DTYPE)

    def lineage_words(self, prefix: int, q: int) -> np.memmap:
        return self.open(f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32", WORD_DTYPE)

    def admission(self, event: int, q: int) -> tuple[np.memmap, np.memmap]:
        return (
            self.open(f"admission_n_{event:02d}_q_{q:02d}_blank.i32", INDEX_DTYPE),
            self.open(f"admission_n_{event:02d}_q_{q:02d}_destination.i32", INDEX_DTYPE),
        )

    def lineage_map(self, prefix: int, q: int, accepted: bool) -> np.memmap:
        role = "accepted" if accepted else "stay"
        return self.open(f"lineage_n_{prefix:02d}_q_{q:02d}_{role}.i32", INDEX_DTYPE)


class CachedSector:
    def __init__(self, length: int, q: int, edges: list[tuple[int, int, str]]):
        if CACHE is None or length != CACHE.length or edges != CACHE.edges or not 0 <= q <= length:
            raise Refusal("cached sector request changed size, charge, or graph")
        self.length = length
        self.q = q
        self.words = CACHE.carrier_words(q)
        self.offsets = CACHE.open(f"carrier_q_{q:02d}_offsets.u64", OFFSET_DTYPE)
        self.sources = CACHE.open(f"carrier_q_{q:02d}_sources.i32", INDEX_DTYPE)
        self.targets = CACHE.open(f"carrier_q_{q:02d}_targets.i32", INDEX_DTYPE)
        if int(self.offsets[0]) != 0 or int(self.offsets[-1]) != len(self.sources) or len(self.sources) != len(self.targets):
            raise Refusal("cached exchange offsets are inconsistent")
        self.pairs = [
            (self.sources[int(self.offsets[index]):int(self.offsets[index + 1])],
             self.targets[int(self.offsets[index]):int(self.offsets[index + 1])])
            for index in range(len(edges))
        ]

    def h(self, vector: np.ndarray) -> np.ndarray:
        guard_consumer()
        result = np.zeros_like(vector)
        for left, right in self.pairs:
            result[:, left] -= vector[:, right]
            result[:, right] -= vector[:, left]
        return result

    def currents(self, vector: np.ndarray) -> np.ndarray:
        guard_consumer()
        answer = np.empty(len(self.pairs), dtype=float)
        for edge, (left, right) in enumerate(self.pairs):
            answer[edge] = 2.0 * float(np.imag(np.vdot(vector[:, left], vector[:, right])))
        return answer

    def close(self) -> None:
        self.pairs = []
        for array in (self.words, self.offsets, self.sources, self.targets):
            close_mapping(array)
        self.words = self.offsets = self.sources = self.targets = np.empty(0)

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass


def cached_fixed_words(width: int, q: int) -> np.ndarray:
    if CACHE is None:
        raise Refusal("cache context is not authenticated")
    if width == 2 * CACHE.length and 0 <= q <= CACHE.length:
        return CACHE.carrier_words(q)
    if 0 <= width < CACHE.length and 0 <= q <= width:
        return CACHE.lineage_words(width, q)
    return ORIGINAL_FIXED_WORDS(width, q)


def cached_create_admitted(length: int, before: Path, prefix: int, event: int, output: Path) -> None:
    if CACHE is None or length != CACHE.length or prefix != event or event >= length - 1:
        raise Refusal("cached nonterminal admission request mismatch")
    output.mkdir(parents=True, exist_ok=False)
    cosine = math.cos(v004.sealed.PHI)
    sine = math.sin(v004.sealed.PHI)
    for out_q in range(prefix + 2):
        guard_consumer(force=True)
        destination = np.lib.format.open_memmap(
            v004.shard_path(output, out_q),
            mode="w+",
            dtype=np.complex128,
            shape=v004.shape(length, prefix + 1, out_q),
        )
        destination[:] = 0.0
        if out_q <= prefix:
            source = v004.open_shard(before, out_q)
            stay_rows = CACHE.lineage_map(prefix, out_q, False)
            blank_columns, accepted_columns = CACHE.admission(event, out_q)
            close_mapping(accepted_columns)
            del accepted_columns
            for source_row, target_row in enumerate(stay_rows):
                row = np.array(source[source_row], copy=True)
                row[blank_columns] *= cosine
                destination[int(target_row)] = row
            close_mapping(source)
            close_mapping(stay_rows)
            close_mapping(blank_columns)
        if out_q and out_q - 1 <= prefix:
            source = v004.open_shard(before, out_q - 1)
            accepted_rows = CACHE.lineage_map(prefix, out_q - 1, True)
            blank_columns, destination_columns = CACHE.admission(event, out_q - 1)
            for source_row, target_row in enumerate(accepted_rows):
                destination[int(target_row), destination_columns] = -1.0j * sine * source[source_row, blank_columns]
            close_mapping(source)
            close_mapping(accepted_rows)
            close_mapping(blank_columns)
            close_mapping(destination_columns)
        destination.flush()
        close_mapping(destination)
        gc.collect()


def cached_terminal_stream(length: int, before: Path, prefix: int, event: int, resolution) -> dict[str, object]:
    if CACHE is None or length != CACHE.length or prefix != length - 1 or event != length - 1:
        raise Refusal("cached terminal stream request mismatch")
    edges = v004.sealed.graph(length)
    admitted_weights = np.zeros(length + 1)
    admitted_occupation = np.zeros(2 * length)
    after_weights = np.zeros(length + 1)
    after_occupation = np.zeros(2 * length)
    null_weights = np.zeros(length + 1)
    actual_current = np.zeros(len(edges))
    null_current = np.zeros(len(edges))
    actual_solver = v004.v3.empty_solver(resolution)
    null_solver = v004.v3.empty_solver(resolution)
    cosine = math.cos(v004.sealed.PHI)
    sine = math.sin(v004.sealed.PHI)
    blocked_error = 0.0
    for q in range(prefix + 1):
        old = v004.open_shard(before, q)
        carrier_words = CACHE.carrier_words(q)
        blank_columns, destination_columns = CACHE.admission(event, q)
        occupied_columns = np.flatnonzero(((carrier_words >> event) & 1) == 1)
        sector = CachedSector(length, q, edges)
        rows = v004.v3.batch_rows(len(carrier_words), resolution, False)
        for lower in range(0, old.shape[0], rows):
            guard_consumer()
            upper = min(old.shape[0], lower + rows)
            source = np.array(old[lower:upper], copy=True)
            child = source.copy()
            child[:, blank_columns] *= cosine
            if len(occupied_columns):
                blocked_error = max(blocked_error, float(np.max(np.abs(child[:, occupied_columns] - source[:, occupied_columns]))))
            weight, occupation = v004.block_statistics(carrier_words, child, 2 * length)
            admitted_weights[q] += weight
            admitted_occupation += occupation
            evolved, flux = v004.route_ephemeral(length, sector, child, resolution, actual_solver)
            weight, occupation = v004.block_statistics(carrier_words, evolved, 2 * length)
            after_weights[q] += weight
            after_occupation += occupation
            actual_current += flux
            null_evolved, flux = v004.route_ephemeral(length, sector, source, resolution, null_solver)
            null_weights[q] += v004.block_statistics(carrier_words, null_evolved, 2 * length)[0]
            null_current += flux
        sector.close()
        del sector
        gc.collect()
        if len(blank_columns):
            destination = CachedSector(length, q + 1, edges)
            rows = v004.v3.batch_rows(len(destination.words), resolution, False)
            for lower in range(0, old.shape[0], rows):
                guard_consumer()
                upper = min(old.shape[0], lower + rows)
                child = np.zeros((upper - lower, len(destination.words)), dtype=np.complex128)
                child[:, destination_columns] = -1.0j * sine * old[lower:upper, blank_columns]
                weight, occupation = v004.block_statistics(destination.words, child, 2 * length)
                admitted_weights[q + 1] += weight
                admitted_occupation += occupation
                evolved, flux = v004.route_ephemeral(length, destination, child, resolution, actual_solver)
                weight, occupation = v004.block_statistics(destination.words, evolved, 2 * length)
                after_weights[q + 1] += weight
                after_occupation += occupation
                actual_current += flux
            destination.close()
            del destination
            gc.collect()
        close_mapping(old)
        close_mapping(carrier_words)
        close_mapping(blank_columns)
        close_mapping(destination_columns)
    return {
        "admitted_weights": admitted_weights,
        "admitted_occupation": admitted_occupation,
        "after_weights": after_weights,
        "after_occupation": after_occupation,
        "null_weights": null_weights,
        "actual_current": actual_current,
        "null_current": null_current,
        "actual_solver": actual_solver,
        "null_solver": null_solver,
        "blocked_error": blocked_error,
    }


def _numeric_tree_close(observed: object, reference: object, tolerance: float, label: str) -> None:
    if type(reference) is bool or isinstance(reference, str) or reference is None:
        if type(observed) is not type(reference) or observed != reference:
            raise Refusal(f"{label} exact value/type mismatch")
        return
    if type(reference) is int:
        if type(observed) is not int or observed != reference:
            raise Refusal(f"{label} exact integer mismatch")
        return
    if type(reference) is float:
        if type(observed) is not float or not math.isfinite(observed) or abs(observed - reference) > tolerance:
            raise Refusal(f"{label} finite numerical projection mismatch")
        return
    if isinstance(reference, list):
        if not isinstance(observed, list) or len(observed) != len(reference):
            raise Refusal(f"{label} list census mismatch")
        for index, (left, right) in enumerate(zip(observed, reference)):
            _numeric_tree_close(left, right, tolerance, f"{label}[{index}]")
        return
    if isinstance(reference, dict):
        if not isinstance(observed, dict) or set(observed) != set(reference):
            raise Refusal(f"{label} object census mismatch")
        for key, value in reference.items():
            _numeric_tree_close(observed[key], value, tolerance, f"{label}.{key}")
        return
    raise Refusal(f"{label} unsupported projection type")


def _validate_solver_record(
    solver: object, label: str, *, require_trivial_zero_steps: bool = False,
) -> None:
    solver = _exact_keys(
        solver,
        {
            "batches", "converged", "low_memory_batches", "maximum_exp_difference",
            "maximum_krylov_steps", "maximum_live_bytes", "maximum_residual_indicator",
            "maximum_subdivisions", "quadrature_nodes",
        },
        label,
    )
    integer_fields = (
        "batches", "low_memory_batches", "maximum_krylov_steps",
        "maximum_live_bytes", "maximum_subdivisions", "quadrature_nodes",
    )
    if (
        solver["converged"] is not True
        or any(type(solver[key]) is not int or solver[key] < 0 for key in integer_fields)
        or solver["batches"] <= 0
        or (
            solver["maximum_krylov_steps"] != 0
            if require_trivial_zero_steps
            else solver["maximum_krylov_steps"] <= 0
        )
        or solver["maximum_live_bytes"] <= 0
        or solver["maximum_live_bytes"] > v004.v3.CAP_BYTES
        or solver["maximum_subdivisions"] <= 0
        or solver["quadrature_nodes"] != 24
        or any(
            type(solver[key]) is not float or not math.isfinite(solver[key]) or solver[key] < 0
            for key in ("maximum_exp_difference", "maximum_residual_indicator")
        )
    ):
        raise Refusal(f"{label} exact type/convergence bound mismatch")


def _v004_reference_peak_state(reference: dict[str, object], length: int) -> int:
    resource_record = _exact_keys(
        reference.get("resource"),
        {
            "maximum_numerical_workset_bytes", "numerical_workset_limit_bytes",
            "passed", "peak_logical_scratch_bytes", "peak_rss_bytes",
            "rss_limit_bytes", "scratch_limit_bytes", "wall_limit_seconds",
            "wall_seconds",
        },
        f"canonical V004 L{length} resource",
    )
    integer_fields = (
        "maximum_numerical_workset_bytes", "numerical_workset_limit_bytes",
        "peak_logical_scratch_bytes", "peak_rss_bytes", "rss_limit_bytes",
        "scratch_limit_bytes",
    )
    if (
        any(type(resource_record.get(key)) is not int for key in integer_fields)
        or any(resource_record[key] <= 0 for key in integer_fields)
        or resource_record.get("passed") is not True
        or type(resource_record.get("passed")) is not bool
        or type(resource_record.get("wall_limit_seconds")) is not float
        or resource_record.get("wall_limit_seconds")
        != builder.HISTORICAL_OBSTRUCTION_WALL_LIMIT
        or type(resource_record.get("wall_seconds")) is not float
        or not math.isfinite(resource_record["wall_seconds"])
        or not 0.0 < resource_record["wall_seconds"]
        <= builder.HISTORICAL_OBSTRUCTION_WALL_LIMIT
        or resource_record["numerical_workset_limit_bytes"] != v004.v3.CAP_BYTES
        or resource_record["rss_limit_bytes"] != v004.RSS_LIMIT
        or resource_record["scratch_limit_bytes"] != builder.SCRATCH_LIMIT
        or resource_record["peak_logical_scratch_bytes"]
        != builder.maximum_state_file_bytes(length)
    ):
        raise Refusal(f"canonical V004 L{length} resource schema/type mismatch")
    return resource_record["peak_logical_scratch_bytes"]


def validate_prior_history(row: object, expected_length: int, cache_sha256: str,
                           physical_gate_sha256: str,
                           freeze: dict[str, object]) -> dict[str, object]:
    if (
        not isinstance(row, dict)
        or set(row) != {"L", "path", "sha256"}
        or type(row.get("L")) is not int
        or row.get("L") != expected_length
    ):
        raise Refusal("staged history row schema/size mismatch")
    expected_path = str(
        (PHYSICAL_OUTPUT_PARENT / f"HISTORY_L{expected_length}.json")
        .relative_to(ROOT)
    )
    if row.get("path") != expected_path:
        raise Refusal("staged history row is not the canonical packet-local output")
    path = builder.safe_repo_file(row.get("path"), row.get("sha256"), f"cached L{expected_length} history")
    record, _history_digest = immutable_json(
        path, f"cached L{expected_length} history", row.get("sha256")
    )
    reference, _reference_digest = immutable_json(
        CANONICAL_V004_HISTORY_PATH[expected_length],
        f"canonical V004 L{expected_length} projection",
        CANONICAL_V004_HISTORY_SHA256[expected_length],
        require_immutable_mode=False,
    )
    exact_top_keys = {
        "schema", "L", "events", "dimension", "preterminal_dimension", "edges",
        "representation", "lineage_authority", "coarse_method", "fine_method",
        "rows", "comparison", "terminal_shards", "cache_manifest_sha256",
        "dual_obstruction_gate_sha256", "physical_execution_gate_sha256",
        "execution_authorization_sha256", "promotion_audit_sha256",
        "cached_control_l4_l8_gate_sha256", "cached_l10_gate_sha256",
        "cached_control_l4_l8_gate_audit_sha256",
        "l10_execution_authorization_gate_sha256",
        "cached_l10_gate_audit_sha256",
        "target_hostile_l10_cross_gate_sha256",
        "shared_aggregate_schedule_gate_sha256", "target_l12_execution_gate_sha256",
        "shared_aggregate_schedule_gate_audit_sha256",
        "original_target_l12_gate_sha256", "preserved_workspace_custody_sha256",
        "preserved_workspace_cross_diagnostic_sha256",
        "runtime_compatibility_obstruction_sha256",
        "v006_hostile_audit_obstruction_sha256",
        "v007_runtime_compatibility_obstruction_sha256",
        "v008_postbuild_audit_binding_obstruction_sha256",
        "v009_hostile_audit_obstruction_sha256",
        "v010_hostile_audit_obstruction_sha256",
        "v010_audit_record_custody_correction_sha256",
        "v011_hostile_audit_obstruction_sha256", "preflight_result_sha256",
        "independent_hostile_audit_sha256", "resource", "consumer_sha256",
        "builder_sha256", "method_sha256",
        "production_obligation_validators_sha256", "freeze_sha256",
        "target_v004_sha256",
        "claim_boundary",
    }
    if (
        set(record) != exact_top_keys
        or record.get("schema") != "TARGET_CACHED_PREFIX_HISTORY_V012"
        or type(record.get("L")) is not int
        or record.get("L") != expected_length
        or type(record.get("events")) is not int
        or record.get("events") != expected_length
        or type(record.get("dimension")) is not int
        or record.get("dimension") != math.comb(3 * expected_length, expected_length)
        or type(record.get("preterminal_dimension")) is not int
        or record.get("preterminal_dimension")
        != math.comb(3 * expected_length - 1, expected_length - 1)
        or type(record.get("edges")) is not int
        or record.get("edges") != 3 * expected_length
        or record.get("representation")
        != "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_INDEX_CACHE"
        or record.get("lineage_authority") != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
        or record.get("coarse_method") != reference.get("coarse_method")
        or record.get("fine_method") != reference.get("fine_method")
        or record.get("cache_manifest_sha256") != cache_sha256
        or record.get("consumer_sha256") != freeze["files"]["consume_target_cache.py"]
        or record.get("builder_sha256") != freeze["files"]["build_target_cache.py"]
        or record.get("method_sha256") != freeze["files"]["METHOD.md"]
        or record.get("production_obligation_validators_sha256")
        != freeze["files"]["production_obligation_validators.py"]
        or record.get("freeze_sha256") != sha256(FREEZE)
        or record.get("physical_execution_gate_sha256") != physical_gate_sha256
        or not isinstance(record.get("execution_authorization_sha256"), str)
        or len(record["execution_authorization_sha256"]) != 64
        or not isinstance(record.get("promotion_audit_sha256"), str)
        or len(record["promotion_audit_sha256"]) != 64
        or record.get("claim_boundary")
        != "FINITE_CACHED_TARGET_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
    ):
        raise Refusal("staged cached history structural identity mismatch")
    expected_provenance = {
        "dual_obstruction_gate_sha256": sha256(builder.DUAL_GATE),
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
        "preflight_result_sha256": sha256(HERE / "PREFLIGHT_RESULT_V001.json"),
        "production_obligation_validators_sha256": freeze["files"][
            "production_obligation_validators.py"
        ],
        "independent_hostile_audit_sha256": immutable_json(
            builder.DUAL_GATE, "dual authorization gate"
        )[0]["independent_hostile_audit"]["sha256"],
        "target_v004_sha256": builder.TARGET_V004_SHA256,
    }
    if any(record.get(key) != value for key, value in expected_provenance.items()):
        raise Refusal("staged cached history provenance mismatch")
    if expected_length in (4, 6, 8):
        control, control_sha256 = immutable_json(
            CONTROL_AUTHORIZATION_GATE, "control execution authorization gate"
        )
        expected_unlock = control_sha256
        expected_audit = control["physical_gate_hostile_audit"]["sha256"]
        expected_stages = (None, None, None, None, None, None, None, None, None)
    else:
        expected_unlock = sha256(L10_EXECUTION_AUTHORIZATION_GATE)
        expected_audit = sha256(CACHED_CONTROL_GATE_AUDIT)
        expected_stages = (
            sha256(CACHED_CONTROL_GATE), sha256(CACHED_CONTROL_GATE_AUDIT),
            sha256(L10_EXECUTION_AUTHORIZATION_GATE), None, None, None,
            None, None, None,
        )
    if (
        record.get("execution_authorization_sha256") != expected_unlock
        or record.get("promotion_audit_sha256") != expected_audit
        or (
            record.get("cached_control_l4_l8_gate_sha256"),
            record.get("cached_control_l4_l8_gate_audit_sha256"),
            record.get("l10_execution_authorization_gate_sha256"),
            record.get("cached_l10_gate_sha256"),
            record.get("cached_l10_gate_audit_sha256"),
            record.get("target_hostile_l10_cross_gate_sha256"),
            record.get("shared_aggregate_schedule_gate_sha256"),
            record.get("shared_aggregate_schedule_gate_audit_sha256"),
            record.get("target_l12_execution_gate_sha256"),
        ) != expected_stages
    ):
        raise Refusal("staged cached history outer unlock/audit binding mismatch")
    _numeric_tree_close(record["coarse_method"], reference["coarse_method"], 0.0, "coarse method")
    _numeric_tree_close(record["fine_method"], reference["fine_method"], 0.0, "fine method")
    rows = record.get("rows")
    reference_rows = reference.get("rows")
    if not isinstance(rows, list) or not isinstance(reference_rows, list) or len(rows) != expected_length:
        raise Refusal("staged cached history row census mismatch")
    for event, (observed, canonical) in enumerate(zip(rows, reference_rows), start=1):
        if not isinstance(observed, dict) or not isinstance(canonical, dict) or set(observed) != set(canonical):
            raise Refusal(f"L{expected_length} event {event} row census mismatch")
        _validate_solver_record(
            observed.get("actual_solver"),
            f"L{expected_length} event {event} actual solver",
        )
        _validate_solver_record(
            observed.get("null_solver"),
            f"L{expected_length} event {event} null solver",
            require_trivial_zero_steps=event == 1,
        )
        projected = {key: value for key, value in observed.items() if key not in {"actual_solver", "null_solver"}}
        canonical_projected = {key: value for key, value in canonical.items() if key not in {"actual_solver", "null_solver"}}
        _numeric_tree_close(projected, canonical_projected, 1.0e-8, f"L{expected_length} event {event}")
    comparison = record.get("comparison")
    if not isinstance(comparison, dict) or comparison.get("resolved") is not True:
        raise Refusal("staged cached history unresolved")
    _numeric_tree_close(comparison, reference.get("comparison"), 1.0e-8, f"L{expected_length} comparison")
    terminal = record.get("terminal_shards")
    canonical_terminal = reference.get("terminal_shards")
    if (
        not isinstance(terminal, list)
        or not isinstance(canonical_terminal, list)
        or len(terminal) != expected_length
        or [item.get("q") for item in terminal if isinstance(item, dict)]
        != list(range(expected_length))
    ):
        raise Refusal("terminal shard q census mismatch")
    canonical_by_q = {item["q"]: item for item in canonical_terminal}
    canonical_root = (WORKSPACE_PARENT / f"L{expected_length}" / "sharp" / f"prefix_{expected_length - 1:02d}").resolve()
    for item in terminal:
        if not isinstance(item, dict) or set(item) != {"q", "path", "shape", "bytes", "sha256"}:
            raise Refusal("terminal shard record schema mismatch")
        q = item["q"]
        expected = canonical_by_q[q]
        if (
            type(q) is not int
            or item.get("shape") != expected["shape"]
            or any(type(value) is not int for value in item.get("shape", []))
            or type(item.get("bytes")) is not int
            or item.get("bytes") != expected["bytes"]
            or item.get("sha256") != expected["sha256"]
        ):
            raise Refusal("terminal shard canonical manifest mismatch")
        shard = _canonical_exact_path(
            item.get("path"), canonical_root / f"q_{q:02d}.npy",
            f"cached L{expected_length} terminal shard q={q}",
        )
        descriptor = open_stable_readonly(shard)
        try:
            if os.fstat(descriptor).st_size != item["bytes"] or descriptor_sha256(descriptor) != item["sha256"]:
                raise Refusal("terminal shard stable descriptor custody mismatch")
        finally:
            os.close(descriptor)
    resource_record = _exact_keys(
        record.get("resource"),
        {
            "peak_live_state_bytes", "cache_payload_bytes", "combined_with_reserve_bytes",
            "scratch_limit_bytes", "maximum_numerical_workset_bytes",
            "numerical_workset_limit_bytes", "terminal_cache_peak_bytes",
            "authentication_cache_peak_bytes", "maximum_cache_window_bytes",
            "mapped_cache_limit_bytes", "peak_rss_bytes", "rss_limit_bytes",
            "wall_seconds", "wall_limit_seconds", "passed",
        },
        "history resource record",
    )
    exact_limits = {
        "cache_payload_bytes": builder.payload_bytes(expected_length),
        "scratch_limit_bytes": builder.SCRATCH_LIMIT,
        "numerical_workset_limit_bytes": v004.v3.CAP_BYTES,
        "rss_limit_bytes": v004.RSS_LIMIT,
        "wall_limit_seconds": builder.WALL_LIMIT,
        "terminal_cache_peak_bytes": builder.terminal_cache_peak_bytes(expected_length),
        "authentication_cache_peak_bytes": builder.authentication_cache_peak_bytes(expected_length),
        "maximum_cache_window_bytes": builder.maximum_cache_window_bytes(expected_length),
        "mapped_cache_limit_bytes": builder.MAPPED_CACHE_LIMIT,
    }
    if (
        resource_record["passed"] is not True
        or any(
            resource_record.get(key) != value
            or type(resource_record.get(key)) is not type(value)
            for key, value in exact_limits.items()
        )
    ):
        raise Refusal("staged cached history resource limits changed")
    expected_peak_state = _v004_reference_peak_state(reference, expected_length)
    expected_workset = max(
        row[solver]["maximum_live_bytes"]
        for row in rows for solver in ("actual_solver", "null_solver")
    )
    canonical_workset = reference["resource"]["maximum_numerical_workset_bytes"]
    if (
        type(resource_record.get("peak_live_state_bytes")) is not int
        or resource_record["peak_live_state_bytes"] != expected_peak_state
        or type(resource_record.get("combined_with_reserve_bytes")) is not int
        or resource_record["combined_with_reserve_bytes"]
        != resource_record["peak_live_state_bytes"]
        + resource_record["cache_payload_bytes"] + builder.OVERHEAD_RESERVE
        or resource_record["combined_with_reserve_bytes"] >= builder.SCRATCH_LIMIT
        or type(resource_record.get("maximum_numerical_workset_bytes")) is not int
        or resource_record["maximum_numerical_workset_bytes"] != expected_workset
        or resource_record["maximum_numerical_workset_bytes"] != canonical_workset
        or resource_record["maximum_numerical_workset_bytes"] > v004.v3.CAP_BYTES
        or type(resource_record.get("peak_rss_bytes")) is not int
        or not 0 < resource_record["peak_rss_bytes"] <= v004.RSS_LIMIT
        or type(resource_record.get("wall_seconds")) is not float
        or not math.isfinite(resource_record["wall_seconds"])
        or not 0.0 < resource_record["wall_seconds"] <= builder.WALL_LIMIT
    ):
        raise Refusal("staged cached history reconstructed resource bound failed")
    artifact_id = (
        "A10_CONTROL_HISTORIES" if expected_length in (4, 6, 8)
        else "A14_L10_HISTORY" if expected_length == 10
        else "A24_TARGET_L12_HISTORY"
    )
    builder.validate_production_obligation(artifact_id, record)
    return record


def require_stage_gate(path: Path, schema: str, classification: str,
                       lengths: tuple[int, ...], cache_hashes: dict[str, str],
                       physical_gate_sha256: str, freeze: dict[str, object],
                       prior_gate_sha256: str | None = None,
                       execution_authorization_sha256: str | None = None,
                       ) -> dict[str, object]:
    if path.is_symlink() or not path.is_file():
        raise Refusal(f"physical history locked: {path.name} absent")
    gate, _stage_digest = immutable_json(path, f"stage gate {path.name}")
    required = {
        "schema": schema,
        "classification": classification,
        "consumer_sha256": freeze["files"]["consume_target_cache.py"],
        "builder_sha256": freeze["files"]["build_target_cache.py"],
        "preflight_sha256": freeze["files"]["validate_preflight.py"],
        "method_sha256": freeze["files"]["METHOD.md"],
        "freeze_sha256": sha256(FREEZE),
        "target_v004_sha256": builder.TARGET_V004_SHA256,
        "physical_execution_gate_sha256": physical_gate_sha256,
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
        "preflight_result_sha256": sha256(HERE / "PREFLIGHT_RESULT_V001.json"),
        "independent_hostile_audit_sha256": immutable_json(
            builder.DUAL_GATE, "dual authorization gate"
        )[0]["independent_hostile_audit"]["sha256"],
    }
    gate_keys = set(required) | {
        "cache_manifest_sha256_by_L", "histories", "claim_boundary",
    }
    if prior_gate_sha256 is not None:
        gate_keys.add("cached_control_l4_l8_gate_sha256")
    if execution_authorization_sha256 is not None:
        gate_keys.add("l10_execution_authorization_gate_sha256")
    if set(gate) != gate_keys:
        raise Refusal(f"staged gate exact key census mismatch: {path.name}")
    if any(
        gate.get(key) != value or type(gate.get(key)) is not type(value)
        for key, value in required.items()
    ):
        raise Refusal(f"staged gate custody mismatch: {path.name}")
    if prior_gate_sha256 is not None and gate.get("cached_control_l4_l8_gate_sha256") != prior_gate_sha256:
        raise Refusal("cached L10 gate does not bind L4-L8 gate")
    if (
        execution_authorization_sha256 is not None
        and gate.get("l10_execution_authorization_gate_sha256")
        != execution_authorization_sha256
    ):
        raise Refusal("cached L10 gate does not bind its distinct authorization")
    expected_claim_boundary = (
        "FINITE_CACHED_CONTROL_STAGE_ONLY__NO_L10_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        if lengths == (4, 6, 8)
        else "FINITE_CACHED_L10_STAGE_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    )
    if gate.get("claim_boundary") != expected_claim_boundary:
        raise Refusal(f"staged gate claim boundary mismatch: {path.name}")
    expected_cache_hashes = {str(length): cache_hashes[str(length)] for length in lengths}
    if gate.get("cache_manifest_sha256_by_L") != expected_cache_hashes:
        raise Refusal(f"staged gate cache census mismatch: {path.name}")
    histories = gate.get("histories")
    if (
        not isinstance(histories, list)
        or [row.get("L") for row in histories if isinstance(row, dict)] != list(lengths)
        or any(
            not isinstance(row, dict)
            or set(row) != {"L", "path", "sha256"}
            or type(row.get("L")) is not int
            for row in histories
        )
    ):
        raise Refusal(f"staged gate history census mismatch: {path.name}")
    for row, length in zip(histories, lengths):
        validate_prior_history(row, length, cache_hashes[str(length)], physical_gate_sha256, freeze)
    artifact_id = (
        "A11_CONTROL_STAGE_GATE"
        if lengths == (4, 6, 8) else "A15_L10_STAGE_GATE"
    )
    builder.validate_production_obligation(artifact_id, gate)
    return gate


def require_stage_gate_audit(
    audit_path: Path, stage_path: Path, stage_gate: dict[str, object],
    schema: str, classification: str, lengths: tuple[int, ...],
    execution_authorization_sha256: str | None = None,
) -> tuple[dict[str, object], str]:
    audit, audit_sha256 = immutable_json(audit_path, f"stage audit {audit_path.name}")
    expected_checks = {
        "stage_gate_exact_schema": 1,
        "history_records": len(lengths),
        "canonical_v004_projection_records": len(lengths),
        "terminal_shard_records": sum(lengths),
        "stable_descriptor_records": 1 + len(lengths) + sum(lengths),
    }
    expected_keys = {
            "schema", "classification", "auditor_role", "audited_packet",
            "sealed_input_commit", "stage_gate_sha256", "history_sha256_by_L",
            "canonical_v004_sha256_by_L", "checks", "checks_passed",
            "checks_total", "failures", "claim_boundary",
    }
    if execution_authorization_sha256 is not None:
        expected_keys.add("l10_execution_authorization_gate_sha256")
    if (
        set(audit) != expected_keys
        or audit.get("schema") != schema
        or audit.get("classification") != classification
        or audit.get("auditor_role") != "INDEPENDENT_HOSTILE_STAGE_GATE_REVIEW"
        or audit.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or audit.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or audit.get("stage_gate_sha256") != sha256(stage_path)
        or audit.get("history_sha256_by_L")
        != {str(row["L"]): row["sha256"] for row in stage_gate["histories"]}
        or audit.get("canonical_v004_sha256_by_L")
        != {str(L): CANONICAL_V004_HISTORY_SHA256[L] for L in lengths}
        or (
            execution_authorization_sha256 is not None
            and audit.get("l10_execution_authorization_gate_sha256")
            != execution_authorization_sha256
        )
        or audit.get("checks") != expected_checks
        or any(type(value) is not int or value <= 0 for value in audit["checks"].values())
        or type(audit.get("checks_total")) is not int
        or type(audit.get("checks_passed")) is not int
        or audit.get("checks_total") != sum(audit["checks"].values())
        or audit.get("checks_passed") != audit["checks_total"]
        or audit.get("failures") != []
        or audit.get("claim_boundary")
        != "FINITE_STAGE_GATE_AUDIT_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal(f"stage hostile audit mismatch: {audit_path.name}")
    artifact_id = (
        "A12_CONTROL_STAGE_AUDIT"
        if lengths == (4, 6, 8) else "A16_L10_STAGE_AUDIT"
    )
    builder.validate_production_obligation(artifact_id, audit)
    return audit, audit_sha256


def require_l10_execution_authorization(
    freeze: dict[str, object], physical_gate_sha256: str,
    cache_hashes: dict[str, str], control_stage: dict[str, object],
    control_audit_sha256: str,
) -> tuple[dict[str, object], str]:
    gate, gate_sha256 = immutable_json(
        L10_EXECUTION_AUTHORIZATION_GATE, "L10 execution authorization gate"
    )
    expected = {
        "schema": "TARGET_V012_L10_EXECUTION_AUTHORIZATION_GATE_V001",
        "classification": "AUTHORIZE_AUDITED_TARGET_V012_L10",
        "authorized_length": 10,
        "physical_execution_gate_sha256": physical_gate_sha256,
        "cached_control_l4_l8_gate_sha256": sha256(CACHED_CONTROL_GATE),
        "cached_control_l4_l8_gate_audit_sha256": control_audit_sha256,
        "l10_cache_manifest_sha256": cache_hashes["10"],
        "consumer_sha256": freeze["files"]["consume_target_cache.py"],
        "builder_sha256": freeze["files"]["build_target_cache.py"],
        "method_sha256": freeze["files"]["METHOD.md"],
        "freeze_sha256": sha256(FREEZE),
        "claim_boundary": "FINITE_L10_PROMOTION_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }
    if gate != expected or type(gate.get("authorized_length")) is not int:
        raise Refusal("L10 execution authorization content mismatch")
    del control_stage  # Already fully reconstructed before this outer unlock is accepted.
    builder.validate_production_obligation("A13_L10_AUTHORIZATION", gate)
    return gate, gate_sha256


def _exact_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise Refusal(f"{label} exact key census mismatch")
    return value


def _positive_integer(value: object) -> bool:
    return type(value) is int and value > 0


def _live_process_identity(process_id: object, label: str) -> int:
    if not _positive_integer(process_id):
        raise Refusal(f"{label} PID is not a positive exact integer")
    try:
        os.kill(process_id, 0)
    except ProcessLookupError as error:
        raise Refusal(f"{label} PID is not live") from error
    except PermissionError:
        # Existence is established even when the process is owned elsewhere.
        pass
    return process_id


def _sha256_text(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _canonical_exact_path(value: object, expected: Path, label: str) -> Path:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise Refusal(f"{label} path must be an exact nonempty string")
    expected_text = str(expected)
    if value != expected_text or os.path.normpath(value) != value:
        raise Refusal(f"{label} path is not the exact canonical path")
    try:
        path = Path(value)
        if not path.is_absolute() or path.resolve() != expected.resolve():
            raise Refusal(f"{label} path is not canonical")
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        if isinstance(error, Refusal):
            raise
        raise Refusal(f"{label} path is malformed") from error
    return path


def _npy_layout(descriptor: int, label: str) -> tuple[tuple[int, ...], int, int]:
    try:
        with os.fdopen(os.dup(descriptor), "rb") as stream:
            version = np.lib.format.read_magic(stream)
            if version == (1, 0):
                shape, fortran, dtype = np.lib.format.read_array_header_1_0(stream)
            elif version in {(2, 0), (3, 0)}:
                shape, fortran, dtype = np.lib.format.read_array_header_2_0(stream)
            else:
                raise Refusal(f"{label} unsupported NPY version")
            offset = stream.tell()
    except (OSError, EOFError, ValueError) as error:
        raise Refusal(f"{label} malformed NPY header") from error
    if fortran or np.dtype(dtype) != np.dtype("<c16"):
        raise Refusal(f"{label} must be C-order little-endian complex128")
    if (
        not isinstance(shape, tuple)
        or any(type(value) is not int or value < 0 for value in shape)
    ):
        raise Refusal(f"{label} NPY shape malformed")
    elements = math.prod(shape)
    return shape, offset, elements


def _authenticate_retained_file(
    path: Path, label: str, expected_sha256: str,
) -> tuple[int, bool]:
    if AUTHORITY_CUSTODY is not None:
        try:
            descriptor, _ = AUTHORITY_CUSTODY.authenticate(
                path, label, expected_sha256, True
            )
        except builder.Refusal as error:
            raise Refusal(str(error)) from error
        return descriptor, False
    descriptor = open_stable_readonly(path)
    if descriptor_sha256(descriptor) != expected_sha256:
        os.close(descriptor)
        raise Refusal(f"{label} hash mismatch")
    return descriptor, True


def _target_to_hostile_basis_permutation(
    width: int, q: int, domain: str,
) -> tuple[np.ndarray, str]:
    if (
        type(width) is not int or width < 0
        or type(q) is not int or not 0 <= q <= width
        or domain not in {"lineage", "carrier"}
    ):
        raise Refusal("target/hostile basis-permutation domain malformed")
    target_words = np.fromiter(
        (
            sum(1 << bit for bit in chosen)
            for chosen in itertools.combinations(range(width), q)
        ),
        dtype=np.uint64,
        count=math.comb(width, q),
    )
    # The hostile order is combinations over the reversed source sequence.
    # It is not, in general, a simple reversal of the target list (for
    # width=4,q=2 the exact map is [5,4,2,3,1,0]).
    hostile_words = np.fromiter(
        (
            sum(1 << bit for bit in chosen)
            for chosen in itertools.combinations(reversed(range(width)), q)
        ),
        dtype=np.uint64,
        count=math.comb(width, q),
    )
    hostile_rank = {int(word): rank for rank, word in enumerate(hostile_words)}
    if len(hostile_rank) != len(target_words):
        raise Refusal("hostile reversed-combination basis is not bijective")
    permutation = np.asarray(
        [hostile_rank[int(word)] for word in target_words], dtype="<u8"
    )
    if (
        len(permutation) != len(target_words)
        or len(set(int(value) for value in permutation)) != len(permutation)
        or not np.array_equal(hostile_words[permutation], target_words)
    ):
        raise Refusal("target/hostile mask-preserving basis bijection failed")
    digest_builder = hashlib.sha256()
    digest_builder.update(b"V001_LE_U64_TARGET_RANK_TO_HOSTILE_RANK\0")
    digest_builder.update(struct.pack("<IIQ", width, q, len(permutation)))
    digest_builder.update(permutation.tobytes(order="C"))
    digest = digest_builder.hexdigest()
    return permutation, digest


def _compare_terminal_target_npy_hostile_raw(
    target_path: Path, target: dict[str, object],
    hostile_path: Path, hostile: dict[str, object], tolerance: float, q: int,
) -> dict[str, object]:
    if type(tolerance) is not float or not math.isfinite(tolerance) or tolerance != 1.0e-8:
        raise Refusal("target/hostile terminal tolerance changed")
    target_fd, close_target = _authenticate_retained_file(
        target_path, "target L10 terminal shard", target["sha256"]
    )
    hostile_fd, close_hostile = _authenticate_retained_file(
        hostile_path, "hostile L10 terminal shard", hostile["sha256"]
    )
    try:
        target_before = os.fstat(target_fd)
        hostile_before = os.fstat(hostile_fd)
        if (
            target_before.st_size != target["bytes"]
            or hostile_before.st_size != hostile["bytes"]
        ):
            raise Refusal("target/hostile L10 terminal shard byte custody mismatch")
        target_shape, target_offset, target_elements = _npy_layout(
            target_fd, "target L10 terminal shard"
        )
        hostile_shape = tuple(hostile["shape"])
        hostile_offset = 0
        hostile_elements = math.prod(hostile_shape)
        lineage_permutation, lineage_digest = _target_to_hostile_basis_permutation(
            9, q, "lineage"
        )
        carrier_permutation, carrier_digest = _target_to_hostile_basis_permutation(
            20, q, "carrier"
        )
        expected_shape = (len(lineage_permutation), len(carrier_permutation))
        if (
            target.get("shape") != list(expected_shape)
            or hostile.get("shape") != list(expected_shape)
            or target_shape != expected_shape
            or hostile_shape != expected_shape
            or target_elements != hostile_elements
            or target_offset + 16 * target_elements != target_before.st_size
            or 16 * hostile_elements != hostile_before.st_size
        ):
            raise Refusal("target-NPY/hostile-raw L10 terminal layout mismatch")
        columns = expected_shape[1]
        row_bytes = 16 * columns
        maximum_error = 0.0
        for target_row, hostile_row in enumerate(lineage_permutation):
            target_raw = os.pread(
                target_fd, row_bytes, target_offset + row_bytes * target_row
            )
            hostile_raw = os.pread(
                hostile_fd, row_bytes,
                hostile_offset + row_bytes * int(hostile_row),
            )
            if len(target_raw) != row_bytes or len(hostile_raw) != row_bytes:
                raise Refusal("target/hostile L10 terminal shard truncated")
            target_values = np.frombuffer(target_raw, dtype="<c16")
            hostile_values = np.frombuffer(hostile_raw, dtype="<c16")[
                carrier_permutation
            ]
            if (
                not np.all(np.isfinite(target_values.real))
                or not np.all(np.isfinite(target_values.imag))
                or not np.all(np.isfinite(hostile_values.real))
                or not np.all(np.isfinite(hostile_values.imag))
            ):
                raise Refusal("target/hostile L10 terminal amplitudes are nonfinite")
            row_error = float(np.max(np.abs(target_values - hostile_values)))
            if not math.isfinite(row_error) or row_error > tolerance:
                raise Refusal("target/hostile L10 terminal amplitudes exceed tolerance")
            maximum_error = max(maximum_error, row_error)
        target_after = os.fstat(target_fd)
        hostile_after = os.fstat(hostile_fd)
        if (
            (target_after.st_dev, target_after.st_ino, target_after.st_size,
             target_after.st_mtime_ns, target_after.st_ctime_ns)
            != (target_before.st_dev, target_before.st_ino, target_before.st_size,
                target_before.st_mtime_ns, target_before.st_ctime_ns)
            or (hostile_after.st_dev, hostile_after.st_ino, hostile_after.st_size,
                hostile_after.st_mtime_ns, hostile_after.st_ctime_ns)
            != (hostile_before.st_dev, hostile_before.st_ino, hostile_before.st_size,
                hostile_before.st_mtime_ns, hostile_before.st_ctime_ns)
            or descriptor_sha256(target_fd) != target["sha256"]
            or descriptor_sha256(hostile_fd) != hostile["sha256"]
        ):
            raise Refusal("target/hostile L10 terminal shard changed during comparison")
        if AUTHORITY_CUSTODY is not None:
            try:
                AUTHORITY_CUSTODY.verify_one(target_path, "target L10 terminal shard")
                AUTHORITY_CUSTODY.verify_one(hostile_path, "hostile L10 terminal shard")
            except builder.Refusal as error:
                raise Refusal(str(error)) from error
        return {
            "lineage_target_to_hostile_permutation_sha256": lineage_digest,
            "carrier_target_to_hostile_permutation_sha256": carrier_digest,
            "linf_abs_error": maximum_error,
        }
    finally:
        if close_target:
            os.close(target_fd)
        if close_hostile:
            os.close(hostile_fd)


def _read_shared_record(binding: dict[str, object], label: str) -> dict[str, object]:
    _exact_keys(
        binding,
        {"path", "sha256", "schema", "identity_field", "identity_value"},
        label,
    )
    path_text = binding["path"]
    digest = binding["sha256"]
    if not isinstance(path_text, str) or not isinstance(digest, str):
        raise Refusal(f"{label} path/hash malformed")
    try:
        path = Path(path_text)
        if (
            os.path.normpath(path_text) != path_text
            or not path.is_absolute()
            or path.resolve() != path
            or not path.is_relative_to(ROOT.resolve())
        ):
            raise Refusal(f"{label} path is not canonical under repository root")
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        if isinstance(error, Refusal):
            raise
        raise Refusal(f"{label} path is malformed") from error
    record, _record_digest = immutable_json(path, label, digest)
    identity_field = binding["identity_field"]
    if (
        not isinstance(record, dict)
        or not isinstance(identity_field, str)
        or identity_field not in {"status", "classification"}
        or record.get("schema") != binding["schema"]
        or record.get(identity_field) != binding["identity_value"]
    ):
        raise Refusal(f"{label} internal identity mismatch")
    return record


def _read_shared_file(binding: object, label: str) -> str:
    binding = _exact_keys(binding, {"path", "sha256"}, label)
    path_text = binding["path"]
    digest = binding["sha256"]
    if (
        not isinstance(path_text, str)
        or not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
    ):
        raise Refusal(f"{label} path/hash malformed")
    try:
        path = Path(path_text)
        if (
            os.path.normpath(path_text) != path_text
            or not path.is_absolute()
            or path.resolve() != path
            or not path.is_relative_to(ROOT.resolve())
        ):
            raise Refusal(f"{label} immutable file path is not canonical")
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        if isinstance(error, Refusal):
            raise
        raise Refusal(f"{label} path is malformed") from error
    try:
        if AUTHORITY_CUSTODY is not None:
            AUTHORITY_CUSTODY.authenticate(path, label, digest, True)
        else:
            builder.stable_file_sha256(path, label, digest, True)
    except builder.Refusal as error:
        raise Refusal(str(error)) from error
    return digest


def _validate_shared_branch(
    binding: object, role: str, expected: dict[str, object] | None = None
) -> dict[str, dict[str, object]]:
    branch = _exact_keys(
        binding,
        {
            "role", "method", "builder", "consumer", "preflight", "freeze",
            "preflight_result", "independent_audit", "cached_L10_gate",
            "L12_cache_manifest",
        },
        f"{role} branch binding",
    )
    if branch["role"] != role:
        raise Refusal(f"{role} branch role mismatch")
    if expected is not None and branch != expected:
        raise Refusal(f"{role} exact branch binding mismatch")
    source_hashes = {
        key: _read_shared_file(branch[key], f"{role} {key}")
        for key in ("method", "builder", "consumer", "preflight")
    }
    records = {
        key: _read_shared_record(branch[key], f"{role} {key}")
        for key in (
            "freeze", "preflight_result", "independent_audit", "cached_L10_gate",
            "L12_cache_manifest",
        )
    }
    audit = records["independent_audit"]
    l10 = records["cached_L10_gate"]
    manifest = records["L12_cache_manifest"]
    frozen_files = records["freeze"].get("files")
    preflight_files = records["preflight_result"].get("files")
    expected_files = {
        Path(branch["method"]["path"]).name: source_hashes["method"],
        Path(branch["builder"]["path"]).name: source_hashes["builder"],
        Path(branch["consumer"]["path"]).name: source_hashes["consumer"],
        Path(branch["preflight"]["path"]).name: source_hashes["preflight"],
    }
    if role == "target_v012":
        freeze_validator_hash = (
            frozen_files.get("production_obligation_validators.py")
            if isinstance(frozen_files, dict) else None
        )
        if not _sha256_text(freeze_validator_hash):
            raise Refusal("target_v012 production validator freeze binding absent")
        expected_files["production_obligation_validators.py"] = freeze_validator_hash
    else:
        hostile_root = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
        for name in HOSTILE_EXECUTED_DEPENDENCY_NAMES:
            dependency_hash = (
                frozen_files.get(name) if isinstance(frozen_files, dict) else None
            )
            if not _sha256_text(dependency_hash):
                raise Refusal(f"hostile_v004r4 executed dependency binding absent: {name}")
            dependency_path = hostile_root / name
            _read_shared_file(
                {"path": str(dependency_path), "sha256": dependency_hash},
                f"hostile_v004r4 executed dependency {name}",
            )
            expected_files[name] = dependency_hash
    expected_preflight_files = {
        "method_sha256": source_hashes["method"],
        "builder_sha256": source_hashes["builder"],
        "consumer_sha256": source_hashes["consumer"],
        "preflight_sha256": source_hashes["preflight"],
        "freeze_sha256": branch["freeze"]["sha256"],
    }
    if role == "target_v012":
        expected_preflight_files["production_obligation_validators_sha256"] = (
            freeze_validator_hash
        )
    if (
        not isinstance(frozen_files, dict)
        or not builder.exact_tree_equal(frozen_files, expected_files)
        or not isinstance(preflight_files, dict)
        or not builder.exact_tree_equal(preflight_files, expected_preflight_files)
        or not _positive_integer(audit.get("checks_total"))
        or type(audit.get("checks_passed")) is not int
        or audit.get("checks_passed") != audit.get("checks_total")
        or audit.get("failures") != []
        or audit.get("audited_freeze_sha256") != branch["freeze"]["sha256"]
        or audit.get("audited_files_sha256") != expected_files
        or audit.get("preflight_result_sha256") != branch["preflight_result"]["sha256"]
        or audit.get("payload_or_history_executed") is not False
        or l10.get("freeze_sha256") != branch["freeze"]["sha256"]
        or l10.get("consumer_sha256") != source_hashes["consumer"]
        or l10.get("independent_hostile_audit_sha256")
        != branch["independent_audit"]["sha256"]
        or type(manifest.get("L")) is not int
        or manifest.get("L") != 12
        or manifest.get("freeze_sha256") != branch["freeze"]["sha256"]
        or manifest.get("builder_sha256") != source_hashes["builder"]
        or manifest.get("consumer_sha256") != source_hashes["consumer"]
        or manifest.get("preflight_sha256") != source_hashes["preflight"]
        or manifest.get("method_sha256") != source_hashes["method"]
        or manifest.get("independent_hostile_audit_sha256")
        != branch["independent_audit"]["sha256"]
    ):
        raise Refusal(f"{role} branch lineage/pass mismatch")
    if role == "hostile_v004r4":
        records["L12_postbuild_audit"] = _validate_hostile_l12_manifest(
            manifest, branch["L12_cache_manifest"]["sha256"], branch,
            source_hashes,
        )
        builder.validate_production_obligation(
            "A17_HOSTILE_L12_ELIGIBILITY", branch
        )
    return records


def _hostile_cache_specs(length: int) -> list[dict[str, object]]:
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


def _hostile_storage_census(length: int) -> dict[str, int]:
    specs = _hostile_cache_specs(length)
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
        builder.operator_q_bytes(length, q)
        + builder.carrier_word_bytes(length, q)
        + (builder.admission_pair_bytes(length, q) if q < length else 0)
        for q in range(length + 1)
    )
    return {
        "raw_cache_bytes_excluding_offsets": actual - offsets,
        "offset_bytes": offsets,
        "actual_cache_array_bytes": actual,
        "maximum_live_state_bytes": state,
        "state_plus_actual_cache_bytes": state + actual,
        "array_file_count": len(specs),
        "state_cache_plus_reserve_bytes": state + actual + builder.OVERHEAD_RESERVE,
        "maximum_q12_cache_plus_admission_bytes": maximum_q_cache_plus_admission,
        "terminal_mapping_bytes": builder.terminal_cache_peak_bytes(length),
        "authentication_peak_bytes": builder.authentication_cache_peak_bytes(length),
    }


def _validate_hostile_l12_manifest(
    manifest: dict[str, object], manifest_sha256: str,
    branch: dict[str, object], source_hashes: dict[str, str],
) -> dict[str, object]:
    exact_keys = {
        "schema", "status", "L", "basis_order", "lineage_identity",
        "edge_layout", "hamiltonian_exchange_coefficient", "files",
        "array_file_count", "manifest_inclusive_file_count", "payload",
        "method_sha256", "builder_sha256", "consumer_sha256", "preflight_sha256",
        "freeze_sha256", "preflight_result_sha256",
        "independent_hostile_audit_sha256", "cache_build_authorization_gate_sha256",
        "postbuild_payload_audit", "canonical_cache_root", "claim_boundary",
    }
    root = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L12"
    specs = _hostile_cache_specs(12)
    storage = _hostile_storage_census(12)
    hostile_edges: list[list[object]] = []
    for site in reversed(range(12)):
        hostile_edges.append([12 + site, 12 + (site + 1) % 12, "rail_2"])
    for site in reversed(range(12)):
        hostile_edges.append([site, 12 + (site + 1) % 12, "connector"])
    for site in reversed(range(12)):
        hostile_edges.append([site, (site + 1) % 12, "rail_1"])
    records = manifest.get("files")
    if (
        set(manifest) != exact_keys
        or manifest.get("schema") != "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4"
        or manifest.get("status") != "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE"
        or type(manifest.get("L")) is not int
        or manifest.get("L") != 12
        or manifest.get("basis_order") != "REVERSED_COMBINATION__FULL_MASK"
        or manifest.get("lineage_identity") != "FULL_CANONICAL_MASK"
        or not builder.exact_tree_equal(manifest.get("edge_layout"), hostile_edges)
        or type(manifest.get("hamiltonian_exchange_coefficient")) is not int
        or manifest.get("hamiltonian_exchange_coefficient") != -1
        or type(manifest.get("array_file_count")) is not int
        or manifest.get("array_file_count") != len(specs)
        or type(manifest.get("manifest_inclusive_file_count")) is not int
        or manifest.get("manifest_inclusive_file_count") != len(specs) + 1
        or not builder.exact_tree_equal(manifest.get("payload"), storage)
        or manifest.get("method_sha256") != source_hashes["method"]
        or manifest.get("builder_sha256") != source_hashes["builder"]
        or manifest.get("consumer_sha256") != source_hashes["consumer"]
        or manifest.get("preflight_sha256") != source_hashes["preflight"]
        or manifest.get("freeze_sha256") != branch["freeze"]["sha256"]
        or manifest.get("preflight_result_sha256") != branch["preflight_result"]["sha256"]
        or manifest.get("independent_hostile_audit_sha256")
        != branch["independent_audit"]["sha256"]
        or not _sha256_text(manifest.get("cache_build_authorization_gate_sha256"))
        or manifest.get("canonical_cache_root") != str(root)
        or manifest.get("claim_boundary")
        != "HOSTILE_V004R4_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"
        or not isinstance(records, list)
        or len(records) != len(specs)
    ):
        raise Refusal("hostile V004R4 L12 manifest exact identity/census mismatch")
    if root.is_symlink() or not root.is_dir() or root.stat().st_mode & 0o222:
        raise Refusal("hostile V004R4 L12 cache root is not immutable")
    for record, spec in zip(records, specs):
        if (
            not isinstance(record, dict)
            or set(record) != set(spec) | {"sha256"}
            or not builder.exact_tree_equal(
                {key: record[key] for key in spec}, spec
            )
            or not _sha256_text(record.get("sha256"))
        ):
            raise Refusal("hostile V004R4 L12 manifest member metadata mismatch")
        member = _canonical_exact_path(
            str(root / str(spec["path"])), root / str(spec["path"]),
            "hostile V004R4 L12 cache member",
        )
        try:
            if AUTHORITY_CUSTODY is not None:
                AUTHORITY_CUSTODY.authenticate(
                    member, f"hostile L12 cache member {spec['path']}",
                    record["sha256"], True,
                )
            else:
                builder.stable_file_sha256(
                    member, f"hostile L12 cache member {spec['path']}",
                    record["sha256"], True,
                )
        except builder.Refusal as error:
            raise Refusal(str(error)) from error
    postbuild_binding = _exact_keys(
        manifest.get("postbuild_payload_audit"),
        {"path", "schema", "identity_field", "identity_value"},
        "hostile V004R4 L12 postbuild payload-audit preregistration",
    )
    expected_postbuild_path = (
        ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
        "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"
    )
    if postbuild_binding != {
        "path": str(expected_postbuild_path),
        "schema": "HOSTILE_V004R4_POSTBUILD_PAYLOAD_AUDIT_V001",
        "identity_field": "classification",
        "identity_value": "PASS_HOSTILE_V004R4_L12_STORAGE_CACHE",
    }:
        raise Refusal("hostile V004R4 postbuild audit path mismatch")
    postbuild, _postbuild_sha256 = immutable_json(
        expected_postbuild_path, "hostile V004R4 L12 postbuild payload audit"
    )
    expected_checks = {
        "manifest_exact_schema": 1,
        "manifest_member_records": len(specs),
        "semantic_index_records": len(specs),
        "stable_descriptor_records": len(specs) + 1,
        "zero_length_operator_records": 2,
    }
    if (
        set(postbuild) != {
            "schema", "classification", "auditor_role", "sealed_input_commit",
            "manifest_sha256", "manifest_file_count", "manifest_payload_bytes",
            "checks", "checks_passed", "checks_total", "failures",
            "no_symlinked_or_writable_inputs", "semantic_cachecontext_passed",
            "physical_history_executed", "claim_boundary",
        }
        or postbuild.get("schema") != "HOSTILE_V004R4_POSTBUILD_PAYLOAD_AUDIT_V001"
        or postbuild.get("classification") != "PASS_HOSTILE_V004R4_L12_STORAGE_CACHE"
        or postbuild.get("auditor_role") != "INDEPENDENT_HOSTILE_POSTBUILD_READ_ONLY_REVIEW"
        or postbuild.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or postbuild.get("manifest_sha256") != manifest_sha256
        or type(postbuild.get("manifest_file_count")) is not int
        or postbuild.get("manifest_file_count") != len(specs)
        or type(postbuild.get("manifest_payload_bytes")) is not int
        or postbuild.get("manifest_payload_bytes") != storage["actual_cache_array_bytes"]
        or not builder.exact_tree_equal(postbuild.get("checks"), expected_checks)
        or type(postbuild.get("checks_total")) is not int
        or postbuild.get("checks_total") != sum(expected_checks.values())
        or type(postbuild.get("checks_passed")) is not int
        or postbuild.get("checks_passed") != postbuild.get("checks_total")
        or postbuild.get("failures") != []
        or postbuild.get("no_symlinked_or_writable_inputs") is not True
        or postbuild.get("semantic_cachecontext_passed") is not True
        or postbuild.get("physical_history_executed") is not False
        or postbuild.get("claim_boundary")
        != "HOSTILE_V004R4_POSTBUILD_STORAGE_AUDIT_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"
    ):
        raise Refusal("hostile V004R4 L12 postbuild audit mismatch")
    return postbuild


def _validate_hostile_l10_gate(
    gate: dict[str, object], branch: dict[str, object],
) -> tuple[dict[str, object], str]:
    expected_checks = {
        "l10_cache_manifest": 1,
        "l10_execution_authorization": 1,
        "l10_history": 1,
        "canonical_v004_projection": 1,
        "terminal_shard_records": 10,
        "stable_descriptor_records": 13,
    }
    if (
        set(gate) != {
            "schema", "classification", "auditor_role", "sealed_input_commit",
            "consumer_sha256", "builder_sha256", "method_sha256",
            "freeze_sha256", "preflight_result_sha256",
            "independent_hostile_audit_sha256", "cache_manifest_sha256_by_L",
            "l10_execution_authorization", "histories", "checks",
            "checks_passed", "checks_total", "failures", "claim_boundary",
        }
        or gate.get("schema") != "HOSTILE_V004R4_CACHED_L10_GATE"
        or gate.get("classification") != "PASS_HOSTILE_V004R4_CACHED_L10"
        or gate.get("auditor_role") != "INDEPENDENT_HOSTILE_STAGE_GATE_REVIEW"
        or gate.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or gate.get("consumer_sha256") != branch["consumer"]["sha256"]
        or gate.get("builder_sha256") != branch["builder"]["sha256"]
        or gate.get("method_sha256") != branch["method"]["sha256"]
        or gate.get("freeze_sha256") != branch["freeze"]["sha256"]
        or gate.get("preflight_result_sha256") != branch["preflight_result"]["sha256"]
        or gate.get("independent_hostile_audit_sha256")
        != branch["independent_audit"]["sha256"]
        or not isinstance(gate.get("cache_manifest_sha256_by_L"), dict)
        or set(gate["cache_manifest_sha256_by_L"]) != {"10"}
        or not _sha256_text(gate["cache_manifest_sha256_by_L"].get("10"))
        or not builder.exact_tree_equal(gate.get("checks"), expected_checks)
        or type(gate.get("checks_total")) is not int
        or gate.get("checks_total") != sum(expected_checks.values())
        or type(gate.get("checks_passed")) is not int
        or gate.get("checks_passed") != gate.get("checks_total")
        or gate.get("failures") != []
        or gate.get("claim_boundary")
        != "FINITE_HOSTILE_V004R4_CACHED_L10_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("hostile V004R4 cached L10 gate exact projection mismatch")
    authorization_binding = gate.get("l10_execution_authorization")
    authorization = _read_shared_record(
        authorization_binding, "hostile V004R4 L10 execution authorization"
    )
    if authorization_binding.get("path") != str(HOSTILE_L10_EXECUTION_GATE):
        raise Refusal("hostile V004R4 L10 authorization path mismatch")
    expected_authorization = {
        "schema": "HOSTILE_V004R4_L10_EXECUTION_AUTHORIZATION_GATE_V001",
        "classification": "AUTHORIZE_AUDITED_HOSTILE_V004R4_L10",
        "role": "hostile_v004r4",
        "authorized_length": 10,
        "l10_cache_manifest_sha256": gate["cache_manifest_sha256_by_L"]["10"],
        "consumer_sha256": branch["consumer"]["sha256"],
        "builder_sha256": branch["builder"]["sha256"],
        "method_sha256": branch["method"]["sha256"],
        "freeze_sha256": branch["freeze"]["sha256"],
        "preflight_result_sha256": branch["preflight_result"]["sha256"],
        "independent_hostile_audit_sha256": branch["independent_audit"]["sha256"],
        "claim_boundary": "FINITE_HOSTILE_V004R4_L10_AUTHORIZATION_ONLY__NO_L12_OR_RESULT",
    }
    if not builder.exact_tree_equal(authorization, expected_authorization):
        raise Refusal("hostile V004R4 L10 authorization content mismatch")
    return authorization, authorization_binding["sha256"]


HOSTILE_NATIVE_ROW_KEYS = {
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
HOSTILE_NATIVE_SOLVER_KEYS = {
    "converged", "batches", "maximum_degree",
    "maximum_endpoint_difference", "maximum_tail_indicator_32", "algorithm",
    "quadrature_group_max", "allocation_vector_slots",
    "maximum_allocation_estimate_bytes", "allocation_limit_bytes",
    "quadrature_nodes", "q_sharded",
}
HOSTILE_NATIVE_TERMINAL_SOLVER_KEYS = HOSTILE_NATIVE_SOLVER_KEYS | {
    "terminal_children_streamed", "terminal_child0_entries",
    "terminal_child1_nonzero_admission_entries",
    "full_terminal_array_allocated",
}
HOSTILE_NATIVE_COMPARISON_KEYS = {
    "resolved", "classification", "epsilon",
    "maximum_admission_accounting_residual",
    "maximum_node_continuity_residual_l1", "maximum_norm_error",
    "maximum_number_drift", "rough_sharp", "sector",
    "admission_acceptance", "routed_acceptance", "connector_ratio",
}
HOSTILE_NATIVE_RESOURCE_KEYS = {
    "peak_logical_state_plus_cache_bytes", "scratch_limit_bytes",
    "maximum_numerical_allocation_estimate_bytes",
    "numerical_workspace_limit_bytes",
    "authentication_peak_certificate_bytes", "peak_rss_bytes",
    "rss_limit_bytes", "wall_seconds_including_authentication",
    "wall_limit_seconds", "passed",
}


def _validate_hostile_native_solver(
    value: object, length: int, event: int, role: str,
) -> dict[str, object]:
    expected = (
        HOSTILE_NATIVE_TERMINAL_SOLVER_KEYS
        if event == length and role == "actual" else HOSTILE_NATIVE_SOLVER_KEYS
    )
    solver = _exact_keys(value, expected, f"hostile L10 event {event} {role} solver")
    integer_keys = {
        "batches", "maximum_degree", "quadrature_group_max",
        "allocation_vector_slots", "maximum_allocation_estimate_bytes",
        "allocation_limit_bytes", "quadrature_nodes",
    }
    if (
        solver.get("converged") is not True
        or solver.get("q_sharded") is not True
        or solver.get("algorithm") != "RECURRENCE_REPLAY_GL_GROUPS"
        or any(type(solver.get(key)) is not int or solver[key] < 0
               for key in integer_keys)
        or solver["batches"] < 1
        or solver["quadrature_nodes"] != 28
        or solver["allocation_limit_bytes"] != 1_400_000_000
        or solver["maximum_allocation_estimate_bytes"] > 1_400_000_000
        or type(solver.get("maximum_endpoint_difference")) is not float
        or not math.isfinite(solver["maximum_endpoint_difference"])
        or type(solver.get("maximum_tail_indicator_32")) is not float
        or not math.isfinite(solver["maximum_tail_indicator_32"])
    ):
        raise Refusal(f"hostile L10 event {event} {role} native solver mismatch")
    if expected == HOSTILE_NATIVE_TERMINAL_SOLVER_KEYS and (
        solver.get("terminal_children_streamed") is not True
        or solver.get("terminal_child0_entries") != math.comb(3 * length - 1, length - 1)
        or solver.get("terminal_child1_nonzero_admission_entries")
        != math.comb(3 * length - 2, length - 1)
        or solver.get("full_terminal_array_allocated") is not False
    ):
        raise Refusal("hostile L10 terminal solver stream certificate mismatch")
    return solver


def _hostile_native_row_projection(
    row: object, length: int, event: int, q_before: float,
) -> tuple[dict[str, object], float]:
    native = _exact_keys(row, HOSTILE_NATIVE_ROW_KEYS, f"hostile L10 event {event}")
    if (
        native.get("event") != event or type(native.get("event")) is not int
        or native.get("input_prefix") != event - 1
        or type(native.get("input_prefix")) is not int
        or native.get("input_prefix_dimension")
        != math.comb(2 * length + event - 1, event - 1)
        or type(native.get("input_prefix_dimension")) is not int
        or native.get("logical_output_prefix_dimension")
        != math.comb(2 * length + event, event)
        or type(native.get("logical_output_prefix_dimension")) is not int
        or native.get("terminal_children_streamed") is not (event == length)
        or type(native.get("sector_weights")) is not list
        or len(native["sector_weights"]) != length + 1
        or any(type(value) is not float or not math.isfinite(value)
               for value in native["sector_weights"])
    ):
        raise Refusal(f"hostile L10 event {event} native row identity mismatch")
    numeric = HOSTILE_NATIVE_ROW_KEYS - {
        "event", "input_prefix", "input_prefix_dimension",
        "logical_output_prefix_dimension", "terminal_children_streamed",
        "sector_weights", "actual_solver", "null_solver",
    }
    if any(type(native.get(key)) is not float or not math.isfinite(native[key])
           for key in numeric):
        raise Refusal(f"hostile L10 event {event} native observable malformed")
    _validate_hostile_native_solver(native["actual_solver"], length, event, "actual")
    _validate_hostile_native_solver(native["null_solver"], length, event, "null")
    q_admitted = q_before + native["W_n"]
    projection = {
        "event": native["event"],
        "cursor_vertex": native["input_prefix"],
        "allow_probability": native["allow_probability"],
        "blocked_probability": native["blocked_probability"],
        "reverse_support_probability": native["reverse_support_probability"],
        "blocked_null_state_error": native["blocked_null_state_error"],
        "W_n": native["W_n"],
        "expected_W_from_allow": 0.5 * native["allow_probability"],
        "q_retained_before": q_before,
        "q_retained_after_admission": q_admitted,
        "q_retained_after_transport": native["q_retained_after_transport"],
        "q_genesis_before": length - q_before,
        "q_genesis_after": native["q_genesis_after"],
        "bandwidth_after": native["q_genesis_after"],
        "lineage_sealed_after": length - native["q_genesis_after"],
        "sector_weights": native["sector_weights"],
        "connector_delta_l1": native["connector_delta_l1"],
        "connector_delta_signed": native["connector_delta_signed"],
        "admission_total_content_residual": native["admission_total_content_residual"],
        "admission_bandwidth_residual": native["admission_bandwidth_residual"],
        "target_owner_residual": native["target_owner_residual"],
        "transport_node_residual_l1": native["transport_node_residual_l1"],
        "transport_node_residual_linf": native["transport_node_residual_linf"],
        "transport_number_drift": native["transport_number_drift"],
        "transport_genesis_drift": 0.0,
        "actual_norm_error": native["actual_norm_error"],
        "null_norm_error": native["null_norm_error"],
        "terminal_children_streamed": native["terminal_children_streamed"],
    }
    return projection, native["q_retained_after_transport"]


def _hostile_native_comparison_projection(value: object, length: int) -> dict[str, object]:
    comparison = _exact_keys(value, HOSTILE_NATIVE_COMPARISON_KEYS, "hostile L10 comparison")
    if (
        comparison.get("resolved") is not True
        or comparison.get("classification") != "RESOLVED_PREFIX_HISTORY_CONTROL"
        or type(comparison.get("epsilon")) is not float
        or not math.isfinite(comparison["epsilon"]) or comparison["epsilon"] <= 0.0
    ):
        raise Refusal("hostile L10 native comparison unresolved/malformed")
    rough_sharp = _exact_keys(
        comparison.get("rough_sharp"),
        {"maximum_disagreement", "observable_linf", "sector_weight_linf"},
        "hostile L10 rough/sharp comparison",
    )
    sector = _exact_keys(
        comparison.get("sector"),
        {"density_interval", "discarded_mass", "enclosed_mass", "late_events", "q_lower", "q_upper"},
        "hostile L10 sector comparison",
    )
    for key in ("admission_acceptance", "routed_acceptance", "connector_ratio"):
        if (type(comparison.get(key)) is not list or len(comparison[key]) != length
                or any(type(item) is not float or not math.isfinite(item)
                       for item in comparison[key])):
            raise Refusal(f"hostile L10 native comparison {key} malformed")
    _numeric_tree_close(rough_sharp, rough_sharp, 1.0e-8, "hostile finite rough/sharp")
    _numeric_tree_close(sector, sector, 1.0e-8, "hostile finite sector")
    return {
        "resolved": comparison["resolved"],
        "coarse_fine": rough_sharp,
        "sector": sector,
        "admission_acceptance": comparison["admission_acceptance"],
        "routed_acceptance": comparison["routed_acceptance"],
        "connector_ratio": comparison["connector_ratio"],
    }


def require_target_hostile_l10_cross_gate(
    freeze: dict[str, object],
    cache_hashes: dict[str, str],
    target_l10_stage: dict[str, object],
    target_l10_stage_audit_sha256: str,
) -> tuple[
    dict[str, object], str, dict[str, object], dict[str, dict[str, object]]
]:
    record, record_sha256 = immutable_json(
        TARGET_HOSTILE_L10_CROSS_GATE,
        "target/hostile L10 cross gate",
    )
    target_projection = _exact_keys(
        record.get("target"),
        {
            "branch", "cached_L10_gate_sha256",
            "cached_L10_gate_audit_sha256", "history_sha256",
        },
        "target L10 cross projection",
    )
    hostile_projection = _exact_keys(
        record.get("hostile"),
        {
            "branch", "cached_L10_gate_sha256",
            "l10_execution_authorization_gate_sha256",
            "independent_prepayload_audit_sha256", "history_sha256",
        },
        "hostile L10 cross projection",
    )
    audit_binding = immutable_json(
        builder.DUAL_GATE, "dual authorization gate"
    )[0]["independent_hostile_audit"]
    expected_target_branch = {
        "role": "target_v012",
        "method": {"path": str(METHOD), "sha256": freeze["files"]["METHOD.md"]},
        "builder": {
            "path": str(HERE / "build_target_cache.py"),
            "sha256": freeze["files"]["build_target_cache.py"],
        },
        "consumer": {
            "path": str(HERE / "consume_target_cache.py"),
            "sha256": freeze["files"]["consume_target_cache.py"],
        },
        "preflight": {
            "path": str(PREFLIGHT),
            "sha256": freeze["files"]["validate_preflight.py"],
        },
        "freeze": {
            "path": str(FREEZE), "sha256": sha256(FREEZE),
            "schema": "TARGET_L12_STORAGE_CACHE_FREEZE_V012",
            "identity_field": "status",
            "identity_value": "FROZEN_BEFORE_NONPHYSICAL_PREFLIGHT_V001_OUTPUT",
        },
        "preflight_result": {
            "path": str(HERE / "PREFLIGHT_RESULT_V001.json"),
            "sha256": sha256(HERE / "PREFLIGHT_RESULT_V001.json"),
            "schema": "TARGET_L12_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT_V012",
            "identity_field": "classification",
            "identity_value": "PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT",
        },
        "independent_audit": {
            "path": str(ROOT / audit_binding["path"]),
            "sha256": audit_binding["sha256"],
            "schema": builder.FUTURE_HOSTILE_AUDIT_SCHEMA,
            "identity_field": "classification",
            "identity_value": builder.FUTURE_HOSTILE_AUDIT_CLASSIFICATION,
        },
        "cached_L10_gate": {
            "path": str(CACHED_L10_GATE), "sha256": sha256(CACHED_L10_GATE),
            "schema": "TARGET_V012_CACHED_L10_GATE",
            "identity_field": "classification",
            "identity_value": "PASS_TARGET_V012_CACHED_L10",
        },
        "L12_cache_manifest": {
            "path": str(builder.CACHE_PARENT / "L12" / "CACHE_MANIFEST.json"),
            "sha256": cache_hashes["12"],
            "schema": "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
            "identity_field": "status",
            "identity_value": "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE",
        },
    }
    target_branch = target_projection["branch"]
    hostile_branch = hostile_projection["branch"]
    _validate_shared_branch(
        target_branch, "target_v012", expected_target_branch
    )
    hostile_records = _validate_shared_branch(
        hostile_branch, "hostile_v004r4"
    )
    role_keys = (
        "method", "builder", "consumer", "preflight", "freeze",
        "preflight_result", "independent_audit", "cached_L10_gate",
        "L12_cache_manifest",
    )
    target_paths = {target_branch[key]["path"] for key in role_keys}
    hostile_paths = {hostile_branch[key]["path"] for key in role_keys}
    target_hashes = {target_branch[key]["sha256"] for key in role_keys}
    hostile_hashes = {hostile_branch[key]["sha256"] for key in role_keys}
    if (
        len(target_paths) != 9 or len(hostile_paths) != 9
        or target_paths & hostile_paths or target_hashes & hostile_hashes
    ):
        raise Refusal("target/hostile nine-role custody is aliased")
    canonical_hostile = {
        "method": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_METHOD.md",
        "builder": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/build_cache_v004r4.py",
        "consumer": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py",
        "preflight": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/validate_cache_preflight_v004r4.py",
        "freeze": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004R4.json",
        "preflight_result": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PREFLIGHT_RESULT.json",
        "independent_audit": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_AUDIT_RESULT_V004R4.json",
        "cached_L10_gate": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
        "L12_cache_manifest": ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L12/CACHE_MANIFEST.json",
    }
    if any(
        hostile_branch[key]["path"] != str(value)
        for key, value in canonical_hostile.items()
    ):
        raise Refusal("hostile_v004r4 canonical path mismatch")
    expected_hostile_identities = {
        "freeze": (
            HOSTILE_FREEZE_SCHEMA, "status", HOSTILE_FREEZE_STATUS,
        ),
        "preflight_result": (
            HOSTILE_PREFLIGHT_SCHEMA, "classification",
            HOSTILE_PREFLIGHT_CLASSIFICATION,
        ),
        "independent_audit": (
            "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001", "classification",
            "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE",
        ),
        "cached_L10_gate": (
            "HOSTILE_V004R4_CACHED_L10_GATE", "classification",
            "PASS_HOSTILE_V004R4_CACHED_L10",
        ),
        "L12_cache_manifest": (
            "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4", "status",
            "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE",
        ),
    }
    for role, (schema, identity_field, identity_value) in (
        expected_hostile_identities.items()
    ):
        binding = hostile_branch[role]
        if (
            binding.get("schema") != schema
            or binding.get("identity_field") != identity_field
            or binding.get("identity_value") != identity_value
        ):
            raise Refusal(f"hostile_v004r4 {role} identity is not registered")
    hostile_freeze = hostile_records["freeze"]
    hostile_preflight = hostile_records["preflight_result"]
    hostile_audit = hostile_records["independent_audit"]
    expected_hostile_absence = {
        "build_gate": False,
        "shared_gate": False,
        "shared_telemetry": False,
        "cache_payloads": False,
        "postbuild_payload_audit": False,
        "workspaces": False,
        "histories": False,
    }
    if (
        hostile_freeze.get("schema") != HOSTILE_FREEZE_SCHEMA
        or hostile_freeze.get("status") != HOSTILE_FREEZE_STATUS
        or hostile_freeze.get("cache_payload_created") is not False
        or hostile_freeze.get("physical_history_executed") is not False
        or hostile_freeze.get("claim_boundary") != HOSTILE_FREEZE_CLAIM
        or hostile_preflight.get("schema") != HOSTILE_PREFLIGHT_SCHEMA
        or hostile_preflight.get("classification")
        != HOSTILE_PREFLIGHT_CLASSIFICATION
        or not _positive_integer(hostile_preflight.get("checks_total"))
        or type(hostile_preflight.get("checks_passed")) is not int
        or hostile_preflight.get("checks_passed")
        != hostile_preflight.get("checks_total")
        or hostile_preflight.get("failures") != []
        or hostile_preflight.get("cache_payload_created") is not False
        or hostile_preflight.get("physical_history_executed") is not False
        or hostile_preflight.get("claim_boundary") != HOSTILE_PREFLIGHT_CLAIM
        or set(hostile_audit) != {
            "schema", "classification", "auditor_role",
            "audited_freeze_sha256", "audited_files_sha256",
            "preflight_result_sha256", "checks_passed", "checks_total", "failures",
            "v004r3_bytes_preserved", "absence_census",
            "payload_or_history_executed", "claim_boundary",
        }
        or hostile_audit.get("schema")
        != "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001"
        or hostile_audit.get("classification")
        != "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE"
        or hostile_audit.get("auditor_role")
        != "INDEPENDENT_HOSTILE_READ_ONLY_REVIEW"
        or hostile_audit.get("audited_freeze_sha256")
        != hostile_branch["freeze"]["sha256"]
        or not builder.exact_tree_equal(
            hostile_audit.get("audited_files_sha256"), hostile_freeze.get("files")
        )
        or hostile_audit.get("preflight_result_sha256")
        != hostile_branch["preflight_result"]["sha256"]
        or not _positive_integer(hostile_audit.get("checks_total"))
        or type(hostile_audit.get("checks_passed")) is not int
        or hostile_audit.get("checks_passed") != hostile_audit.get("checks_total")
        or hostile_audit.get("failures") != []
        or hostile_audit.get("v004r3_bytes_preserved") is not True
        or type(hostile_audit.get("v004r3_bytes_preserved")) is not bool
        or not builder.exact_tree_equal(
            hostile_audit.get("absence_census"), expected_hostile_absence
        )
        or any(
            type(value) is not bool
            for value in hostile_audit.get("absence_census", {}).values()
        )
        or hostile_audit.get("payload_or_history_executed") is not False
        or type(hostile_audit.get("payload_or_history_executed")) is not bool
        or hostile_audit.get("claim_boundary") != HOSTILE_AUDIT_CLAIM
    ):
        raise Refusal("hostile_v004r4 registered control identity/claim mismatch")
    hostile_l10 = hostile_records["cached_L10_gate"]
    hostile_l10_authorization, hostile_l10_authorization_sha256 = (
        _validate_hostile_l10_gate(hostile_l10, hostile_branch)
    )
    hostile_histories = hostile_l10.get("histories")
    if (
        not isinstance(hostile_histories, list)
        or len(hostile_histories) != 1
        or not isinstance(hostile_histories[0], dict)
        or set(hostile_histories[0]) != {"L", "path", "sha256"}
        or type(hostile_histories[0].get("L")) is not int
        or hostile_histories[0].get("L") != 10
    ):
        raise Refusal("hostile cached L10 gate history census mismatch")
    target_history = target_l10_stage["histories"][0]
    hostile_history = hostile_histories[0]
    expected_hostile_history_path = (
        "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
        "V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json"
    )
    if hostile_history.get("path") != expected_hostile_history_path:
        raise Refusal("hostile cached L10 history path mismatch")
    target_history_record, _ = immutable_json(
        builder.safe_repo_file(
            target_history["path"], target_history["sha256"],
            "target cached L10 cross history",
        ),
        "target cached L10 cross history",
        target_history["sha256"],
    )
    hostile_history_record, _ = immutable_json(
        builder.safe_repo_file(
            hostile_history["path"], hostile_history["sha256"],
            "hostile cached L10 cross history",
        ),
        "hostile cached L10 cross history",
        hostile_history["sha256"],
    )
    hostile_history_keys = {
        "schema", "L", "events", "dimension", "preterminal_dimension", "edges",
        "representation", "lineage_authority", "coarse_method", "fine_method",
        "rows", "comparison", "terminal_shards", "cache_manifest_sha256",
        "cache_build_authorization_gate_sha256",
        "l10_execution_authorization_gate_sha256", "resource",
        "consumer_sha256", "builder_sha256", "method_sha256", "preflight_sha256",
        "freeze_sha256", "preflight_result_sha256",
        "independent_hostile_audit_sha256", "claim_boundary",
    }
    exact_scalar_fields = (
        "L", "events", "dimension", "preterminal_dimension", "edges",
        "lineage_authority",
    )
    hostile_coarse_method = {
        "label": "rough", "checkpoints": [16, 24, 32, 48, 64, 80],
        "quadrature_nodes": 18, "tolerance": 3.0e-9,
    }
    hostile_fine_method = {
        "label": "sharp", "checkpoints": [24, 32, 48, 64, 80, 96],
        "quadrature_nodes": 28, "tolerance": 8.0e-11,
    }
    if (
        set(hostile_history_record) != hostile_history_keys
        or hostile_history_record.get("schema")
        != "HOSTILE_CACHED_PREFIX_HISTORY_V004R4"
        or hostile_history_record.get("representation")
        != "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_HOSTILE_INDEX_CACHE"
        or hostile_history_record.get("claim_boundary")
        != "FINITE_CACHED_HOSTILE_V004R4_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
        or hostile_history_record.get("coarse_method") != hostile_coarse_method
        or hostile_history_record.get("fine_method") != hostile_fine_method
        or hostile_history_record.get("cache_manifest_sha256")
        != hostile_l10["cache_manifest_sha256_by_L"]["10"]
        or not _sha256_text(
            hostile_history_record.get("cache_build_authorization_gate_sha256")
        )
        or hostile_history_record.get("l10_execution_authorization_gate_sha256")
        != hostile_l10_authorization_sha256
        or hostile_history_record.get("consumer_sha256")
        != hostile_branch["consumer"]["sha256"]
        or hostile_history_record.get("builder_sha256")
        != hostile_branch["builder"]["sha256"]
        or hostile_history_record.get("method_sha256")
        != hostile_branch["method"]["sha256"]
        or hostile_history_record.get("preflight_sha256")
        != hostile_branch["preflight"]["sha256"]
        or hostile_history_record.get("freeze_sha256")
        != hostile_branch["freeze"]["sha256"]
        or hostile_history_record.get("preflight_result_sha256")
        != hostile_branch["preflight_result"]["sha256"]
        or hostile_history_record.get("independent_hostile_audit_sha256")
        != hostile_branch["independent_audit"]["sha256"]
        or any(
            type(hostile_history_record.get(key))
            is not type(target_history_record.get(key))
            or hostile_history_record.get(key) != target_history_record.get(key)
            for key in exact_scalar_fields
        )
    ):
        raise Refusal("hostile cached L10 structural projection mismatch")
    target_rows = target_history_record.get("rows")
    hostile_rows = hostile_history_record.get("rows")
    if (
        not isinstance(target_rows, list)
        or not isinstance(hostile_rows, list)
        or len(target_rows) != 10
        or len(hostile_rows) != 10
    ):
        raise Refusal("target/hostile cached L10 row census mismatch")
    q_before = 0.0
    for event, (target_row, hostile_row) in enumerate(
        zip(target_rows, hostile_rows), start=1
    ):
        if not isinstance(target_row, dict):
            raise Refusal(f"target L10 event {event} row schema mismatch")
        hostile_physical_projection, q_before = _hostile_native_row_projection(
            hostile_row, 10, event, q_before,
        )
        target_projection = {
            key: value for key, value in target_row.items()
            if key not in {"actual_solver", "null_solver"}
        }
        _numeric_tree_close(
            hostile_physical_projection, target_projection, 1.0e-8,
            f"target/hostile L10 event {event}",
        )
    target_comparison = _exact_keys(
        target_history_record.get("comparison"),
        {"admission_acceptance", "classification", "coarse_fine", "connector_ratio",
         "epsilon", "resolved", "routed_acceptance", "sector"},
        "target L10 comparison",
    )
    hostile_comparison_projection = _hostile_native_comparison_projection(
        hostile_history_record.get("comparison"), 10,
    )
    target_comparison_projection = {
        key: target_comparison[key]
        for key in ("resolved", "coarse_fine", "sector", "admission_acceptance",
                    "routed_acceptance", "connector_ratio")
    }
    _numeric_tree_close(
        hostile_comparison_projection, target_comparison_projection,
        1.0e-8,
        "target/hostile L10 comparison",
    )
    hostile_resource = _exact_keys(
        hostile_history_record.get("resource"),
        HOSTILE_NATIVE_RESOURCE_KEYS,
        "hostile L10 resource record",
    )
    hostile_storage = _hostile_storage_census(10)
    reported_hostile_allocation = max(
        row[solver]["maximum_allocation_estimate_bytes"]
        for row in hostile_rows
        for solver in ("actual_solver", "null_solver")
    )
    expected_hostile_peak_state = hostile_storage["maximum_live_state_bytes"]
    exact_hostile_resource = {
        "peak_logical_state_plus_cache_bytes": (
            expected_hostile_peak_state
            + hostile_storage["actual_cache_array_bytes"]
        ),
        "scratch_limit_bytes": builder.SCRATCH_LIMIT,
        "maximum_numerical_allocation_estimate_bytes": reported_hostile_allocation,
        "numerical_workspace_limit_bytes": 1_400_000_000,
        "authentication_peak_certificate_bytes": hostile_storage["authentication_peak_bytes"],
        "rss_limit_bytes": v004.RSS_LIMIT,
        "wall_limit_seconds": float(builder.WALL_LIMIT),
        "passed": True,
    }
    if (
        hostile_resource["passed"] is not True
        or any(
            hostile_resource.get(key) != value
            or type(hostile_resource.get(key)) is not type(value)
            for key, value in exact_hostile_resource.items()
        )
        or hostile_resource["peak_logical_state_plus_cache_bytes"]
        + builder.OVERHEAD_RESERVE >= builder.SCRATCH_LIMIT
        or hostile_resource["maximum_numerical_allocation_estimate_bytes"]
        > hostile_resource["numerical_workspace_limit_bytes"]
        or type(hostile_resource["peak_rss_bytes"]) is not int
        or not 0 < hostile_resource["peak_rss_bytes"] <= v004.RSS_LIMIT
        or type(hostile_resource["wall_seconds_including_authentication"]) is not float
        or not math.isfinite(hostile_resource["wall_seconds_including_authentication"])
        or not 0.0 < hostile_resource["wall_seconds_including_authentication"] <= float(builder.WALL_LIMIT)
    ):
        raise Refusal("hostile L10 reconstructed resource bound mismatch")
    target_terminal = target_history_record.get("terminal_shards")
    hostile_terminal = hostile_history_record.get("terminal_shards")
    if (
        not isinstance(target_terminal, list)
        or not isinstance(hostile_terminal, list)
        or len(target_terminal) != 10
        or len(hostile_terminal) != 10
    ):
        raise Refusal("target/hostile L10 terminal-shard census mismatch")
    terminal_projection_by_q: list[dict[str, object]] = []
    for q, (target_shard, hostile_shard) in enumerate(
        zip(target_terminal, hostile_terminal)
    ):
        if (
            not isinstance(target_shard, dict)
            or not isinstance(hostile_shard, dict)
            or set(target_shard) != {"q", "path", "shape", "bytes", "sha256"}
            or set(hostile_shard) != {"q", "path", "shape", "bytes", "sha256"}
            or type(target_shard.get("q")) is not int
            or type(hostile_shard.get("q")) is not int
            or target_shard.get("q") != q
            or hostile_shard.get("q") != q
            or not isinstance(target_shard.get("shape"), list)
            or not isinstance(hostile_shard.get("shape"), list)
            or any(type(value) is not int or value < 0 for value in target_shard["shape"])
            or any(type(value) is not int or value < 0 for value in hostile_shard["shape"])
            or target_shard["shape"] != hostile_shard["shape"]
            or type(target_shard.get("bytes")) is not int
            or type(hostile_shard.get("bytes")) is not int
            or target_shard["bytes"] <= 0
            or target_shard["bytes"] != 16 * math.prod(target_shard["shape"]) + 128
            or hostile_shard["bytes"] != 16 * math.prod(hostile_shard["shape"])
            or not _sha256_text(target_shard.get("sha256"))
            or not _sha256_text(hostile_shard.get("sha256"))
        ):
            raise Refusal("target/hostile L10 terminal-shard projection mismatch")
        expected_target_path = (
            WORKSPACE_PARENT / "L10/sharp/prefix_09" / f"q_{q:02d}.npy"
        )
        expected_hostile_path = (
            ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "V004R4_WORKSPACES/L10/sharp/prefix_09" / f"q_{q:02d}.c128"
        )
        target_shard_path = _canonical_exact_path(
            target_shard.get("path"), expected_target_path,
            "target L10 terminal shard",
        )
        hostile_shard_path = _canonical_exact_path(
            hostile_shard.get("path"), expected_hostile_path,
            "hostile L10 terminal shard",
        )
        projection = _compare_terminal_target_npy_hostile_raw(
            target_shard_path, target_shard, hostile_shard_path, hostile_shard,
            1.0e-8, q,
        )
        terminal_projection_by_q.append({
            "q": q,
            "target_sha256": target_shard["sha256"],
            "hostile_sha256": hostile_shard["sha256"],
            **projection,
        })
    discrete_fields = [
        "L", "events", "dimension", "preterminal_dimension", "edges",
        "row_physical_projection", "comparison_physical_projection",
        "terminal_shard_census",
    ]
    comparison_policy = {
        "discrete_fields": discrete_fields,
        "discrete_fields_exact": True,
        "physical_abs_tolerance": 1.0e-8,
        "basis_projection": "INDEPENDENT_MASK_BIJECTION__TARGET_ASCENDING_TO_HOSTILE_REVERSED",
        "terminal_projection_by_q": terminal_projection_by_q,
        "solver_telemetry_policy": "INDEPENDENT_NATIVE_SCHEMAS__TARGET_KRYLOV_AND_HOSTILE_CHEBYSHEV_NOT_RELABELED",
        "terminal_storage_policy": "TARGET_NPY_HEADER_V1__HOSTILE_RAW_C128_OFFSET_ZERO",
    }
    expected_checks = {
        "target_l10_lineage_bindings": 3,
        "hostile_l10_lineage_bindings": 3,
        "exact_discrete_projection_fields": len(discrete_fields),
        "finite_numerical_projection": 1,
        "terminal_shard_records": 20,
        "independent_basis_permutation_records": 20,
        "terminal_chunk_comparisons": 10,
    }
    expected_target = {
        "branch": expected_target_branch,
        "cached_L10_gate_sha256": sha256(CACHED_L10_GATE),
        "cached_L10_gate_audit_sha256": target_l10_stage_audit_sha256,
        "history_sha256": target_history["sha256"],
    }
    expected_hostile = {
        "branch": hostile_branch,
        "cached_L10_gate_sha256": hostile_branch["cached_L10_gate"]["sha256"],
        "l10_execution_authorization_gate_sha256": hostile_l10_authorization_sha256,
        "independent_prepayload_audit_sha256": hostile_branch["independent_audit"]["sha256"],
        "history_sha256": hostile_history["sha256"],
    }
    if (
        set(record) != {
            "schema", "classification", "auditor_role", "sealed_input_commit",
            "L", "target", "hostile", "comparison_policy", "checks",
            "checks_passed", "checks_total", "failures", "claim_boundary",
        }
        or record.get("schema") != "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001"
        or record.get("classification") != "PASS_EXACT_TARGET_HOSTILE_L10_CROSS_BENCHMARK"
        or record.get("auditor_role") != "INDEPENDENT_HOSTILE_L10_CROSS_REVIEW"
        or record.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or type(record.get("L")) is not int
        or record.get("L") != 10
        or record.get("target") != expected_target
        or record.get("hostile") != expected_hostile
        or not builder.exact_tree_equal(
            record.get("comparison_policy"), comparison_policy
        )
        or record.get("checks") != expected_checks
        or any(type(value) is not int or value <= 0 for value in record["checks"].values())
        or type(record.get("checks_total")) is not int
        or record["checks_total"] != sum(record["checks"].values())
        or type(record.get("checks_passed")) is not int
        or record["checks_passed"] != record["checks_total"]
        or record.get("failures") != []
        or record.get("claim_boundary")
        != "FINITE_L10_TARGET_HOSTILE_CROSS_AUDIT_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("target/hostile L10 cross gate content mismatch")
    builder.validate_production_obligation("A18_L10_CROSS_GATE", record)
    return record, record_sha256, hostile_branch, hostile_records


def require_parallel_l12_schedule_gate(
    l10_cross_gate_sha256: str,
) -> tuple[dict[str, object], str]:
    """Authenticate readiness only; this record cannot authorize or release work."""
    gate, schedule_sha256 = immutable_json(
        PARALLEL_L12_SCHEDULE_GATE, "dual L12 readiness schedule"
    )
    _exact_keys(
        gate,
        {
            "schema", "classification", "created_epoch", "expires_epoch",
            "l10_cross_gate_sha256", "resource_snapshot", "schedule", "roles",
            "telemetry", "claim_boundary",
        },
        "dual L12 readiness schedule",
    )
    if (
        gate.get("schema") != "V012_DUAL_L12_READINESS_SCHEDULE_V001"
        or gate.get("classification") != "READY_FOR_INDEPENDENT_SCHEDULE_AUDIT"
        or gate.get("l10_cross_gate_sha256") != l10_cross_gate_sha256
        or not _sha256_text(gate.get("l10_cross_gate_sha256"))
    ):
        raise Refusal("dual L12 readiness schedule identity/binding mismatch")
    snapshot = _exact_keys(
        gate.get("resource_snapshot"),
        {
            "captured_epoch", "host_physical_memory_bytes", "available_memory_bytes",
            "workspace_free_disk_bytes", "workspace_filesystem_device",
            "both_workspace_roots_same_filesystem", "memory_pressure", "passes",
        },
        "dual L12 resource snapshot",
    )
    integer_snapshot_fields = (
        "captured_epoch", "host_physical_memory_bytes", "available_memory_bytes",
        "workspace_free_disk_bytes", "workspace_filesystem_device",
    )
    if (
        any(not _positive_integer(snapshot.get(key)) for key in integer_snapshot_fields)
        or snapshot["host_physical_memory_bytes"] < builder.PARALLEL_HOST_TOTAL_MINIMUM
        or snapshot["available_memory_bytes"] < builder.PARALLEL_AGGREGATE_PEAK
        or snapshot["workspace_free_disk_bytes"] < builder.PARALLEL_FILESYSTEM_MINIMUM
        or snapshot.get("both_workspace_roots_same_filesystem") is not True
        or type(snapshot.get("both_workspace_roots_same_filesystem")) is not bool
        or snapshot.get("memory_pressure") != "NORMAL"
        or type(snapshot.get("memory_pressure")) is not str
        or snapshot.get("passes") is not True
        or type(snapshot.get("passes")) is not bool
    ):
        raise Refusal("dual L12 readiness resource snapshot insufficient")
    created = gate.get("created_epoch")
    expires = gate.get("expires_epoch")
    now = int(time.time())
    if (
        not _positive_integer(created) or not _positive_integer(expires)
        or not created <= snapshot["captured_epoch"] <= expires
        or not 0 < expires - created <= 300
        or not created <= now <= expires
    ):
        raise Refusal("dual L12 readiness freshness window mismatch")
    exact_schedule = {
        "launch_mode": "PRELAUNCHED_BLOCKED_TWO_WORKER",
        "release_only_after_both_l12_authorizations": True,
        "launch_skew_seconds_max": 60,
        "per_process_rss_limit_bytes": v004.RSS_LIMIT,
        "per_process_wall_limit_seconds": 108_000,
        "mapped_peak_limit_bytes_by_role": {
            "target_v012": builder.PARALLEL_TARGET_AUTHENTICATION_PEAK,
            "hostile_v004r4": builder.PARALLEL_HOSTILE_AUTHENTICATION_PEAK,
        },
    }
    if not builder.exact_tree_equal(gate.get("schedule"), exact_schedule):
        raise Refusal("dual L12 readiness schedule controls mismatch")
    roles = _exact_keys(
        gate.get("roles"), {"target_v012", "hostile_v004r4"},
        "dual L12 readiness roles",
    )
    expected_paths = {
        "target_v012": {
            "worker_executable_path": str(HERE / "consume_target_cache.py"),
            "workspace_path": str(WORKSPACE_PARENT / "L12"),
            "output_path": str(PHYSICAL_OUTPUT_PARENT / "HISTORY_L12.json"),
        },
        "hostile_v004r4": {
            "worker_executable_path": str(
                ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py"
            ),
            "workspace_path": str(
                ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES/L12"
            ),
            "output_path": str(
                ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
                "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json"
            ),
        },
    }
    all_paths: set[str] = set()
    for role, paths in expected_paths.items():
        row = _exact_keys(
            roles[role],
            {"role", *paths.keys(), "ready_for_blocked_worker_start"},
            f"dual L12 readiness role {role}",
        )
        if (
            row.get("role") != role
            or row.get("ready_for_blocked_worker_start") is not True
            or type(row.get("ready_for_blocked_worker_start")) is not bool
        ):
            raise Refusal("dual L12 blocked-worker readiness mismatch")
        for key, expected in paths.items():
            _canonical_exact_path(row.get(key), Path(expected), f"{role} {key}")
            all_paths.add(row[key])
    if len(all_paths) != 6:
        raise Refusal("dual L12 readiness role paths are aliased")
    telemetry = {
        "path": str(PARALLEL_L12_TELEMETRY),
        "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
        "must_be_absent_before_release": True,
        "absent_at_schedule_capture": True,
        "sample_interval_seconds_max": 60,
    }
    if (
        not builder.exact_tree_equal(gate.get("telemetry"), telemetry)
        or PARALLEL_L12_TELEMETRY.exists()
        or gate.get("claim_boundary")
        != "READINESS_AND_RESOURCE_SCHEDULING_ONLY__NO_L12_RELEASE_OR_RESULT"
    ):
        raise Refusal("dual L12 readiness telemetry/claim mismatch")
    builder.validate_production_obligation("A20_SHARED_SCHEDULE_GATE", gate)
    return gate, schedule_sha256


def require_shared_schedule_audit(
    schedule_gate: dict[str, object], schedule_sha256: str,
    l10_cross_gate_sha256: str,
) -> tuple[dict[str, object], str]:
    audit, audit_sha256 = immutable_json(
        PARALLEL_L12_SCHEDULE_AUDIT, "independent dual L12 readiness audit"
    )
    expected_checks = {
        "schedule_exact_schema": 1,
        "deep_exact_types": 1,
        "two_role_path_custody": 2,
        "normal_memory_pressure": 1,
        "resource_thresholds": 4,
        "freshness_window": 1,
        "telemetry_prelaunch_absence": 1,
    }
    _exact_keys(
        audit,
        {
            "schema", "classification", "auditor_role", "schedule_sha256",
            "l10_cross_gate_sha256", "checks", "checks_total", "checks_passed",
            "failures", "claim_boundary",
        },
        "independent dual L12 readiness audit",
    )
    if (
        audit.get("schema") != "V012_DUAL_L12_READINESS_SCHEDULE_AUDIT_V001"
        or audit.get("classification")
        != "PASS_INDEPENDENT_PREAUTHORIZATION_READINESS_AUDIT"
        or audit.get("auditor_role")
        != "INDEPENDENT_DUAL_LAUNCH_COORDINATOR_REVIEW"
        or audit.get("schedule_sha256") != schedule_sha256
        or audit.get("l10_cross_gate_sha256") != l10_cross_gate_sha256
        or schedule_gate.get("l10_cross_gate_sha256") != l10_cross_gate_sha256
        or not builder.exact_tree_equal(audit.get("checks"), expected_checks)
        or type(audit.get("checks_total")) is not int
        or audit.get("checks_total") != sum(expected_checks.values())
        or type(audit.get("checks_passed")) is not int
        or audit.get("checks_passed") != audit.get("checks_total")
        or audit.get("failures") != []
        or audit.get("claim_boundary")
        != "INDEPENDENT_READINESS_AUDIT_ONLY__NO_L12_AUTHORIZATION_RELEASE_OR_RESULT"
    ):
        raise Refusal("independent dual L12 readiness audit mismatch")
    builder.validate_production_obligation("A21_SHARED_SCHEDULE_AUDIT", audit)
    return audit, audit_sha256


def require_target_l12_execution_gate(
    freeze: dict[str, object], physical_gate_sha256: str,
    cache_hashes: dict[str, str], control_stage_audit_sha256: str,
    l10_stage_audit_sha256: str, l10_cross_gate_sha256: str,
    shared_schedule_audit_sha256: str,
) -> tuple[dict[str, object], str]:
    path = TARGET_L12_EXECUTION_GATE
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o222:
        raise Refusal("L12 target history locked: target L12 execution gate absent")
    gate, target_gate_digest = immutable_json(path, "target L12 execution gate")
    _exact_keys(
        gate,
        {
            "schema", "classification", "role", "authorized_length",
            "schedule_sha256", "schedule_audit_sha256", "l10_cross_gate_sha256",
            "consumer_sha256", "l12_cache_manifest_sha256", "claim_boundary",
        },
        "target L12 execution gate",
    )
    expected = {
        "schema": "TARGET_V012_L12_ONE_WAY_AUTHORIZATION_V001",
        "classification": "AUTHORIZE_TARGET_V012_L12_AFTER_SCHEDULE_AUDIT",
        "role": "target_v012",
        "authorized_length": 12,
        "schedule_sha256": sha256(PARALLEL_L12_SCHEDULE_GATE),
        "schedule_audit_sha256": shared_schedule_audit_sha256,
        "l10_cross_gate_sha256": l10_cross_gate_sha256,
        "consumer_sha256": freeze["files"]["consume_target_cache.py"],
        "l12_cache_manifest_sha256": cache_hashes["12"],
        "claim_boundary": "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT",
    }
    if not builder.exact_tree_equal(gate, expected):
        raise Refusal("target L12 execution gate custody/identity mismatch")
    del physical_gate_sha256, control_stage_audit_sha256, l10_stage_audit_sha256
    builder.validate_production_obligation(
        "A22_TARGET_L12_AUTHORIZATION", gate
    )
    return gate, target_gate_digest


def require_hostile_l12_execution_gate(
    hostile_branch: dict[str, object], schedule_sha256: str,
    schedule_audit_sha256: str, l10_cross_gate_sha256: str,
) -> tuple[dict[str, object], str]:
    gate, digest = immutable_json(
        HOSTILE_L12_EXECUTION_GATE, "hostile V004R4 L12 one-way authorization"
    )
    expected = {
        "schema": "HOSTILE_V004R4_L12_ONE_WAY_AUTHORIZATION_V001",
        "classification": "AUTHORIZE_HOSTILE_V004R4_L12_AFTER_SCHEDULE_AUDIT",
        "role": "hostile_v004r4",
        "authorized_length": 12,
        "schedule_sha256": schedule_sha256,
        "schedule_audit_sha256": schedule_audit_sha256,
        "l10_cross_gate_sha256": l10_cross_gate_sha256,
        "consumer_sha256": hostile_branch["consumer"]["sha256"],
        "l12_cache_manifest_sha256": hostile_branch["L12_cache_manifest"]["sha256"],
        "claim_boundary": "ONE_WAY_FINITE_L12_EXECUTION_AUTHORIZATION_ONLY__NO_LAUNCH_OR_RESULT",
    }
    if not builder.exact_tree_equal(gate, expected):
        raise Refusal("hostile V004R4 L12 one-way authorization mismatch")
    builder.validate_production_obligation(
        "A22_TARGET_L12_AUTHORIZATION", gate
    )
    return gate, digest


def _wait_for_immutable_record(
    path: Path, label: str, expires_epoch: int,
) -> tuple[dict[str, object], str]:
    if type(expires_epoch) is not int or int(time.time()) > expires_epoch:
        raise Refusal(f"{label} schedule expired before authority read")
    while not path.exists():
        if int(time.time()) > expires_epoch:
            raise Refusal(f"{label} absent at schedule expiry")
        time.sleep(0.1)
    if int(time.time()) > expires_epoch:
        raise Refusal(f"{label} schedule expired before authority read")
    record = immutable_json(path, label)
    if int(time.time()) > expires_epoch:
        raise Refusal(f"{label} schedule expired during authority read")
    return record


def require_dual_l12_launch_handshake(
    schedule: dict[str, object], schedule_sha256: str,
    schedule_audit_sha256: str, target_authorization_sha256: str,
    hostile_authorization_sha256: str,
) -> tuple[dict[str, object], str]:
    handshake, digest = _wait_for_immutable_record(
        DUAL_L12_LAUNCH_HANDSHAKE, "dual L12 blocked-worker handshake",
        schedule["expires_epoch"],
    )
    if set(handshake) != {
        "schema", "classification", "created_epoch", "schedule_sha256",
        "schedule_audit_sha256", "authorization_sha256_by_role",
        "memory_pressure", "workers", "ready_sha256_by_role",
        "observed_readiness_skew_seconds",
        "launch_skew_seconds_max", "telemetry", "claim_boundary",
    }:
        raise Refusal("dual L12 handshake exact key census mismatch")
    auth_hashes = {
        "target_v012": target_authorization_sha256,
        "hostile_v004r4": hostile_authorization_sha256,
    }
    workers = _exact_keys(
        handshake.get("workers"), {"target_v012", "hostile_v004r4"},
        "dual L12 handshake workers",
    )
    if not _positive_integer(handshake.get("created_epoch")):
        raise Refusal("dual L12 handshake creation epoch mismatch")
    expected_paths = {
        "target_v012": (
            HERE / "consume_target_cache.py", WORKSPACE_PARENT / "L12"
        ),
        "hostile_v004r4": (
            ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py",
            ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES/L12",
        ),
    }
    ready_epochs: dict[str, int] = {}
    pids: set[int] = set()
    worker_ids: set[str] = set()
    for role, (executable, workspace) in expected_paths.items():
        worker = _exact_keys(
            workers[role], OrchestratedWorkerSession.READY_KEYS,
            f"dual L12 handshake worker {role}",
        )
        if (
            worker.get("schema") != READY_SCHEMA
            or worker.get("role") != role
            or not isinstance(worker.get("worker_id"), str)
            or not worker["worker_id"]
            or not _positive_integer(worker.get("process_id"))
            or not _sha256_text(worker.get("process_start_token"))
            or worker.get("process_start_token")
            != _process_start_token(worker["process_id"])
            or not _sha256_text(worker.get("executable_sha256"))
            or worker.get("executable_sha256") != sha256(executable)
            or not _sha256_text(worker.get("control_channel_id"))
            or not _sha256_text(worker.get("nonce_commitment_sha256"))
            or worker.get("blocked_on_release") is not True
            or type(worker.get("blocked_on_release")) is not bool
        ):
            raise Refusal("dual L12 handshake worker identity mismatch")
        _canonical_exact_path(worker.get("executable_path"), executable,
                              f"{role} handshake executable")
        _canonical_exact_path(worker.get("workspace_path"), workspace,
                              f"{role} handshake workspace")
        output = (
            PHYSICAL_OUTPUT_PARENT / "HISTORY_L12.json"
            if role == "target_v012" else
            ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json"
        )
        _canonical_exact_path(
            worker.get("output_path"), output, f"{role} handshake output"
        )
        if (
            role == "target_v012"
            and (
                ORCHESTRATED_SESSION is None
                or worker != ORCHESTRATED_SESSION.ready
                or worker["process_id"] != os.getpid()
            )
        ):
            raise Refusal("target worker READY/handshake mismatch")
        _live_process_identity(
            worker["process_id"], f"dual L12 handshake worker {role}"
        )
        if (
            not _positive_integer(worker.get("ready_epoch"))
            or not schedule["created_epoch"] <= worker["ready_epoch"] <= handshake.get("created_epoch", 0)
            or worker["process_id"] in pids
            or worker["worker_id"] in worker_ids
        ):
            raise Refusal("dual L12 handshake worker readiness mismatch")
        ready_epochs[role] = worker["ready_epoch"]
        pids.add(worker["process_id"])
        worker_ids.add(worker["worker_id"])
    ready_hashes = _exact_keys(
        handshake.get("ready_sha256_by_role"),
        {"target_v012", "hostile_v004r4"}, "dual L12 READY hashes",
    )
    for role in ("target_v012", "hostile_v004r4"):
        if (
            not _sha256_text(ready_hashes[role])
            or ready_hashes[role]
            != hashlib.sha256(_wire_canonical_json(workers[role])).hexdigest()
        ):
            raise Refusal("dual L12 READY hash mismatch")
    skew = abs(ready_epochs["target_v012"] - ready_epochs["hostile_v004r4"])
    expected_telemetry = {
        "path": str(PARALLEL_L12_TELEMETRY),
        "schema": "SHARED_TARGET_V012_HOSTILE_V004R4_L12_TELEMETRY_V001",
        "absent_before_release": True,
    }
    if (
        handshake.get("schema") != "V012_DUAL_L12_BLOCKED_WORKER_HANDSHAKE_V002"
        or handshake.get("classification")
        != "BOTH_BLOCKED_WORKERS_READY_AFTER_BOTH_L12_AUTHORIZATIONS"
        or not _positive_integer(handshake.get("created_epoch"))
        or not schedule["created_epoch"] <= handshake["created_epoch"] <= schedule["expires_epoch"]
        or handshake.get("schedule_sha256") != schedule_sha256
        or handshake.get("schedule_audit_sha256") != schedule_audit_sha256
        or not builder.exact_tree_equal(
            handshake.get("authorization_sha256_by_role"), auth_hashes
        )
        or handshake.get("memory_pressure") != "NORMAL"
        or type(handshake.get("memory_pressure")) is not str
        or type(handshake.get("observed_readiness_skew_seconds")) is not int
        or handshake.get("observed_readiness_skew_seconds") != skew
        or skew > 60
        or type(handshake.get("launch_skew_seconds_max")) is not int
        or handshake.get("launch_skew_seconds_max") != 60
        or not builder.exact_tree_equal(handshake.get("telemetry"), expected_telemetry)
        or PARALLEL_L12_TELEMETRY.exists()
        or handshake.get("claim_boundary")
        != "IMMUTABLE_PRELAUNCH_HANDSHAKE_ONLY__NO_WORKER_RELEASE_OR_RESULT"
    ):
        raise Refusal("dual L12 blocked-worker handshake mismatch")
    if (
        ORCHESTRATED_SESSION is None
        or ready_hashes["target_v012"] != ORCHESTRATED_SESSION.ready_sha256
        or ORCHESTRATED_SESSION.release is None
        or ORCHESTRATED_SESSION.release["handshake_sha256"] != digest
    ):
        raise Refusal("target inherited channel is not bound to handshake")
    builder.validate_production_obligation(
        "A22_TARGET_L12_AUTHORIZATION", handshake
    )
    return handshake, digest


def require_dual_l12_worker_release(
    schedule: dict[str, object], handshake: dict[str, object], handshake_sha256: str,
    target_authorization_sha256: str, hostile_authorization_sha256: str,
) -> tuple[dict[str, object], str]:
    release, digest = _wait_for_immutable_record(
        DUAL_L12_WORKER_RELEASE, "dual L12 worker release",
        schedule["expires_epoch"],
    )
    if set(release) != {
        "schema", "classification", "handshake_sha256",
        "authorization_sha256_by_role", "release_epoch_by_role",
        "observed_launch_skew_seconds", "release_by_role", "claim_boundary",
    }:
        raise Refusal("dual L12 worker-release exact key census mismatch")
    auth_hashes = {
        "target_v012": target_authorization_sha256,
        "hostile_v004r4": hostile_authorization_sha256,
    }
    epochs = _exact_keys(
        release.get("release_epoch_by_role"),
        {"target_v012", "hostile_v004r4"}, "dual L12 release epochs",
    )
    if any(not _positive_integer(value) for value in epochs.values()):
        raise Refusal("dual L12 release epoch type mismatch")
    skew = abs(epochs["target_v012"] - epochs["hostile_v004r4"])
    releases = _exact_keys(
        release.get("release_by_role"), {"target_v012", "hostile_v004r4"},
        "dual L12 released workers",
    )
    for role in ("target_v012", "hostile_v004r4"):
        row = _exact_keys(
            releases[role],
            {
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id", "nonce_commitment_sha256",
                "release_token_sha256",
            },
            f"dual L12 release role {role}",
        )
        expected_token = hashlib.sha256(
            f"{handshake_sha256}:{role}:{epochs[role]}".encode("ascii")
        ).hexdigest()
        worker = handshake["workers"][role]
        if (
            row.get("role") != role
            or row.get("worker_id") != worker["worker_id"]
            or type(row.get("process_id")) is not int
            or row.get("process_id") != worker["process_id"]
            or row.get("process_start_token") != worker["process_start_token"]
            or row.get("control_channel_id") != worker["control_channel_id"]
            or row.get("nonce_commitment_sha256")
            != worker["nonce_commitment_sha256"]
            or row.get("release_token_sha256") != expected_token
        ):
            raise Refusal("dual L12 released-worker binding mismatch")
        _live_process_identity(
            row["process_id"], f"dual L12 released worker {role}"
        )
    if (
        release.get("schema") != "V012_DUAL_L12_WORKER_RELEASE_V002"
        or release.get("classification") != "RELEASE_BOTH_AUTHORIZED_BLOCKED_WORKERS"
        or release.get("handshake_sha256") != handshake_sha256
        or not builder.exact_tree_equal(
            release.get("authorization_sha256_by_role"), auth_hashes
        )
        or any(
            not handshake["created_epoch"] <= epoch <= schedule["expires_epoch"]
            for epoch in epochs.values()
        )
        or type(release.get("observed_launch_skew_seconds")) is not int
        or release.get("observed_launch_skew_seconds") != skew
        or skew > 60
        or PARALLEL_L12_TELEMETRY.exists()
        or release.get("claim_boundary")
        != "BARRIER_RELEASE_ONLY__NO_PHYSICAL_RESULT"
    ):
        raise Refusal("dual L12 worker-release record mismatch")
    session = ORCHESTRATED_SESSION
    if session is None or session.release is None:
        raise Refusal("target inherited release channel absent")
    wire = session.release
    target_row = releases["target_v012"]
    if (
        wire["worker_release_sha256"] != digest
        or wire["handshake_sha256"] != handshake_sha256
        or wire["release_epoch"] != epochs["target_v012"]
        or any(
            wire[field] != target_row[field]
            for field in (
                "role", "worker_id", "process_id", "process_start_token",
                "control_channel_id", "nonce_commitment_sha256",
            )
        )
    ):
        raise Refusal("target wire/file release binding mismatch")
    session.acknowledge()
    builder.validate_production_obligation(
        "A22_TARGET_L12_AUTHORIZATION", release
    )
    return release, digest


def require_postbuild_payload_audit(
    specification: object, freeze: dict[str, object], cache_hashes: dict[str, str]
) -> dict[str, object]:
    if not isinstance(specification, dict) or set(specification) != {
        "path", "sha256", "schema", "classification"
    }:
        raise Refusal("postbuild payload-audit binding malformed")
    if (
        specification.get("path") != builder.FUTURE_POSTBUILD_AUDIT_PATH
        or specification.get("schema") != builder.FUTURE_POSTBUILD_AUDIT_SCHEMA
        or specification.get("classification")
        != builder.FUTURE_POSTBUILD_AUDIT_CLASSIFICATION
    ):
        raise Refusal("postbuild payload-audit identity mismatch")
    path = builder.safe_repo_file(
        specification["path"], specification.get("sha256"),
        "V012 postbuild payload audit",
    )
    audit, _audit_digest = immutable_json(
        path, "postbuild payload audit", specification.get("sha256")
    )
    exact_keys = {
        "schema", "classification", "auditor_role", "audited_packet",
        "sealed_input_commit", "prebuild_hostile_audit_sha256",
        "dual_obstruction_and_compatibility_gate_sha256",
        "manifest_sha256_by_L", "payload_census_by_L", "checks",
        "checks_passed", "checks_total", "failures",
        "no_symlinked_or_writable_payload_inputs", "semantic_cachecontext",
        "physical_gate_or_history_executed", "claim_boundary",
    }
    expected_census = {
        str(L): {
            "file_count": builder.expected_file_count(L),
            "total_bytes": builder.payload_bytes(L),
        }
        for L in builder.SUPPORTED
    }
    expected_checks = {
        "cachecontext_clean_close_lengths": 2,
        "cachecontext_descriptor_reauthentication_lengths": 2,
        "cachecontext_full_semantic_lengths": 2,
        "cachecontext_zero_length_arrays": 4,
        "descriptor_stability_records": 1100,
        "dual_gate_authorizations": 5,
        "file_hash_byte_shape_dtype_records": 1100,
        "frozen_source_files": 5,
        "manifest_file_records": 1100,
        "manifest_identity_records": 5,
        "manifest_provenance_fields": 135,
        "no_physical_execution_paths": 8,
        "payload_directories": 5,
        "prebuild_hostile_audit": 1,
        "resource_certificate_records": 5,
        "zero_length_q0_records": 10,
    }
    dual, _dual_digest = immutable_json(builder.DUAL_GATE, "dual authorization gate")
    if (
        set(audit) != exact_keys
        or audit.get("schema") != builder.FUTURE_POSTBUILD_AUDIT_SCHEMA
        or audit.get("classification") != builder.FUTURE_POSTBUILD_AUDIT_CLASSIFICATION
        or audit.get("auditor_role") != "INDEPENDENT_HOSTILE_POSTBUILD_READ_ONLY_REVIEW"
        or audit.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or audit.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or audit.get("prebuild_hostile_audit_sha256")
        != dual["independent_hostile_audit"]["sha256"]
        or audit.get("dual_obstruction_and_compatibility_gate_sha256")
        != sha256(builder.DUAL_GATE)
        or audit.get("manifest_sha256_by_L") != cache_hashes
        or audit.get("payload_census_by_L") != expected_census
        or any(
            type(audit["payload_census_by_L"][str(L)][field]) is not int
            for L in builder.SUPPORTED for field in ("file_count", "total_bytes")
        )
        or audit.get("checks") != expected_checks
        or any(type(value) is not int or value <= 0 for value in audit["checks"].values())
        or type(audit.get("checks_total")) is not int
        or audit["checks_total"] <= 0
        or type(audit.get("checks_passed")) is not int
        or sum(audit["checks"].values()) != audit["checks_total"]
        or audit.get("checks_passed") != audit["checks_total"]
        or audit.get("failures") != []
        or audit.get("no_symlinked_or_writable_payload_inputs") is not True
        or audit.get("physical_gate_or_history_executed") is not False
        or audit.get("semantic_cachecontext")
        != {
            "L4": {
                "descriptor_count": builder.expected_file_count(4),
                "descriptor_reauthentication": "PASS",
                "full_index_identity": "PASS",
                "zero_length_q0_open": "PASS",
            },
            "L12": {
                "descriptor_count": builder.expected_file_count(12),
                "descriptor_reauthentication": "PASS",
                "full_index_identity": "PASS",
                "zero_length_q0_open": "PASS",
            },
        }
        or type(audit["semantic_cachecontext"]["L4"]["descriptor_count"]) is not int
        or type(audit["semantic_cachecontext"]["L12"]["descriptor_count"]) is not int
        or audit.get("claim_boundary")
        != "POSTBUILD_STORAGE_CACHE_AUDIT_ONLY__NO_PHYSICAL_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("postbuild payload-audit content mismatch")
    builder.validate_production_obligation("A06_POSTBUILD_AUDIT", audit)
    return audit


def require_control_execution_authorization(
    length: int, freeze: dict[str, object], physical_gate_sha256: str,
    postbuild_binding: dict[str, object],
) -> dict[str, object]:
    if CONTROL_AUTHORIZATION_GATE.is_symlink() or not CONTROL_AUTHORIZATION_GATE.is_file():
        raise Refusal("physical history locked: audited control authorization gate absent")
    gate, _control_digest = immutable_json(
        CONTROL_AUTHORIZATION_GATE, "control execution authorization gate"
    )
    required_keys = {
        "schema", "classification", "authorized_lengths",
        "physical_execution_gate", "physical_gate_hostile_audit",
        "postbuild_payload_audit", "consumer_sha256", "builder_sha256",
        "method_sha256", "freeze_sha256", "preflight_result_sha256",
        "claim_boundary",
    }
    if set(gate) != required_keys:
        raise Refusal("control authorization gate key census mismatch")
    physical_binding = gate.get("physical_execution_gate")
    audit_binding = gate.get("physical_gate_hostile_audit")
    if (
        gate.get("schema") != "TARGET_V012_CONTROL_EXECUTION_AUTHORIZATION_GATE_V001"
        or gate.get("classification") != "AUTHORIZE_AUDITED_TARGET_V012_CONTROLS_L4_L6_L8"
        or gate.get("authorized_lengths") != [4, 6, 8]
        or any(type(value) is not int for value in gate.get("authorized_lengths", []))
        or length not in gate["authorized_lengths"]
        or physical_binding
        != {
            "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_EXECUTION_GATE_V012.json",
            "sha256": physical_gate_sha256,
        }
        or gate.get("postbuild_payload_audit") != postbuild_binding
        or not isinstance(audit_binding, dict)
        or set(audit_binding) != {"path", "sha256", "schema", "classification"}
        or audit_binding.get("path") != builder.FUTURE_PHYSICAL_GATE_AUDIT_PATH
        or audit_binding.get("schema") != builder.FUTURE_PHYSICAL_GATE_AUDIT_SCHEMA
        or audit_binding.get("classification")
        != builder.FUTURE_PHYSICAL_GATE_AUDIT_CLASSIFICATION
        or gate.get("consumer_sha256") != freeze["files"]["consume_target_cache.py"]
        or gate.get("builder_sha256") != freeze["files"]["build_target_cache.py"]
        or gate.get("method_sha256") != freeze["files"]["METHOD.md"]
        or gate.get("freeze_sha256") != sha256(FREEZE)
        or gate.get("preflight_result_sha256") != sha256(HERE / "PREFLIGHT_RESULT_V001.json")
        or gate.get("claim_boundary")
        != "AUDITED_CONTROL_EXECUTION_AUTHORIZATION_ONLY__NO_L10_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("control authorization gate content mismatch")
    audit_path = builder.safe_repo_file(
        audit_binding["path"], audit_binding.get("sha256"),
        "V012 physical-gate hostile audit",
    )
    audit, _physical_audit_digest = immutable_json(
        audit_path, "physical-gate hostile audit", audit_binding.get("sha256")
    )
    expected_checks = {
        "base_gate_exact_key_census": 1,
        "base_gate_source_bindings": 4,
        "base_gate_cache_manifest_bindings": 5,
        "postbuild_audit_binding": 1,
        "outer_control_authorized_lengths": 3,
    }
    if (
        set(audit)
        != {
            "schema", "classification", "auditor_role", "audited_packet",
            "sealed_input_commit", "physical_execution_gate_sha256",
            "base_gate_exact_key_census_passed",
            "base_gate_exact_key_census_sha256",
            "postbuild_payload_audit_sha256", "consumer_sha256",
            "freeze_sha256", "checks", "checks_passed", "checks_total", "failures",
            "physical_history_executed", "claim_boundary",
        }
        or audit.get("schema") != builder.FUTURE_PHYSICAL_GATE_AUDIT_SCHEMA
        or audit.get("classification") != builder.FUTURE_PHYSICAL_GATE_AUDIT_CLASSIFICATION
        or audit.get("auditor_role") != "INDEPENDENT_HOSTILE_PHYSICAL_GATE_REVIEW"
        or audit.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or audit.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or audit.get("physical_execution_gate_sha256") != physical_gate_sha256
        or audit.get("base_gate_exact_key_census_passed") is not True
        or audit.get("base_gate_exact_key_census_sha256")
        != BASE_PHYSICAL_GATE_KEY_CENSUS_SHA256
        or audit.get("postbuild_payload_audit_sha256") != postbuild_binding["sha256"]
        or audit.get("consumer_sha256") != freeze["files"]["consume_target_cache.py"]
        or audit.get("freeze_sha256") != sha256(FREEZE)
        or audit.get("checks") != expected_checks
        or any(type(value) is not int or value <= 0
               for value in audit["checks"].values())
        or type(audit.get("checks_total")) is not int
        or audit["checks_total"] != sum(audit["checks"].values())
        or type(audit.get("checks_passed")) is not int
        or audit.get("checks_passed") != audit["checks_total"]
        or audit.get("failures") != []
        or audit.get("physical_history_executed") is not False
        or audit.get("claim_boundary")
        != "PHYSICAL_GATE_CONTROL_PLANE_AUDIT_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("physical-gate hostile audit content mismatch")
    builder.validate_production_obligation("A08_PHYSICAL_GATE_AUDIT", audit)
    builder.validate_production_obligation("A09_CONTROL_AUTHORIZATION", gate)
    return gate


def require_physical_gate(length: int, manifest_sha256: str) -> dict[str, object]:
    freeze = builder.require_frozen_census()
    builder.require_original_target_gate()
    builder.require_preserved_workspace_custody()
    builder.require_preserved_workspace_cross_diagnostic()
    builder.require_runtime_compatibility_obstruction()
    dual = builder.require_dual_gate(length)
    if PHYSICAL_GATE.is_symlink() or not PHYSICAL_GATE.is_file():
        raise Refusal("physical history locked: execution gate is absent")
    gate, physical_hash = immutable_json(PHYSICAL_GATE, "base physical execution gate")
    if gate.get("schema") != "TARGET_V012_CACHE_PHYSICAL_EXECUTION_GATE" or gate.get("classification") != "AUTHORIZE_TARGET_V012_CACHED_PHYSICAL_EXECUTION":
        raise Refusal("physical execution classification absent")
    required = {
        "dual_obstruction_gate_sha256": sha256(builder.DUAL_GATE),
        "consumer_sha256": freeze["files"]["consume_target_cache.py"],
        "builder_sha256": freeze["files"]["build_target_cache.py"],
        "preflight_sha256": freeze["files"]["validate_preflight.py"],
        "method_sha256": freeze["files"]["METHOD.md"],
        "freeze_sha256": sha256(FREEZE),
        "target_v004_sha256": builder.TARGET_V004_SHA256,
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
        "preflight_result_sha256": sha256(HERE / "PREFLIGHT_RESULT_V001.json"),
        "independent_hostile_audit_sha256": immutable_json(
            builder.DUAL_GATE, "dual authorization gate"
        )[0]["independent_hostile_audit"]["sha256"],
    }
    for key, expected in required.items():
        if gate.get(key) != expected:
            raise Refusal(f"physical execution gate does not pin {key}")
    if set(gate) != BASE_PHYSICAL_GATE_KEYS:
        raise Refusal("physical execution gate exact key census mismatch")
    if gate.get("claim_boundary") != (
        "BASE_PHYSICAL_GATE_BINDING_ONLY__OUTER_HOSTILE_AUDIT_AUTHORIZATION_REQUIRED__"
        "NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("physical execution gate claim boundary mismatch")
    authorized = gate.get("authorized_lengths")
    if (
        authorized != list(builder.SUPPORTED)
        or any(type(value) is not int for value in authorized)
    ):
        raise Refusal("base physical gate must bind exactly all five cache manifests")
    cache_hashes = gate.get("cache_manifest_sha256_by_L")
    if (
        not isinstance(cache_hashes, dict)
        or set(cache_hashes) != {str(value) for value in authorized}
        or any(
            not isinstance(value, str)
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
            for value in cache_hashes.values()
        )
        or cache_hashes.get(str(length)) != manifest_sha256
    ):
        raise Refusal("physical execution gate cache-manifest census mismatch")
    postbuild = require_postbuild_payload_audit(
        gate.get("postbuild_payload_audit"), freeze, cache_hashes
    )
    if physical_hash != sha256(PHYSICAL_GATE):
        raise Refusal("base physical gate path changed after descriptor authentication")
    builder.validate_production_obligation("A07_BASE_PHYSICAL_GATE", gate)
    execution_authorization: dict[str, object] | None = None
    execution_authorization_sha256: str | None = None
    promotion_audit_sha256: str | None = None
    l10_authorization: dict[str, object] | None = None
    l10_authorization_sha256: str | None = None
    stages: dict[str, object] = {}
    if length in (4, 6, 8):
        execution_authorization = require_control_execution_authorization(
            length, freeze, physical_hash, gate["postbuild_payload_audit"]
        )
        execution_authorization_sha256 = sha256(CONTROL_AUTHORIZATION_GATE)
        promotion_audit_sha256 = execution_authorization[
            "physical_gate_hostile_audit"
        ]["sha256"]
    if length in (10, 12):
        control = require_stage_gate(
            CACHED_CONTROL_GATE,
            "TARGET_V012_CACHED_CONTROL_L4_L8_GATE",
            "PASS_TARGET_V012_CACHED_CONTROLS_L4_L6_L8",
            (4, 6, 8),
            cache_hashes,
            physical_hash,
            freeze,
        )
        stages["control"] = control
        control_audit, control_audit_sha256 = require_stage_gate_audit(
            CACHED_CONTROL_GATE_AUDIT, CACHED_CONTROL_GATE, control,
            "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001",
            "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8",
            (4, 6, 8),
        )
        stages["control_audit"] = control_audit
        stages["control_audit_sha256"] = control_audit_sha256
        l10_authorization, l10_authorization_sha256 = require_l10_execution_authorization(
            freeze, physical_hash, cache_hashes, control, control_audit_sha256
        )
        stages["l10_authorization"] = l10_authorization
        stages["l10_authorization_sha256"] = l10_authorization_sha256
        if length == 10:
            execution_authorization = l10_authorization
            execution_authorization_sha256 = l10_authorization_sha256
            promotion_audit_sha256 = control_audit_sha256
    if length == 12:
        if l10_authorization_sha256 is None:
            raise Refusal("L12 path did not reconstruct distinct L10 authorization")
        l10_stage = require_stage_gate(
            CACHED_L10_GATE,
            "TARGET_V012_CACHED_L10_GATE",
            "PASS_TARGET_V012_CACHED_L10",
            (10,),
            cache_hashes,
            physical_hash,
            freeze,
            sha256(CACHED_CONTROL_GATE),
            l10_authorization_sha256,
        )
        stages["L10"] = l10_stage
        l10_audit, l10_audit_sha256 = require_stage_gate_audit(
            CACHED_L10_GATE_AUDIT, CACHED_L10_GATE, l10_stage,
            "TARGET_V012_CACHED_L10_GATE_AUDIT_V001",
            "PASS_INDEPENDENT_TARGET_V012_CACHED_L10",
            (10,),
            l10_authorization_sha256,
        )
        stages["L10_audit"] = l10_audit
        stages["L10_audit_sha256"] = l10_audit_sha256
        (
            l10_cross, l10_cross_sha256, hostile_branch, hostile_records,
        ) = require_target_hostile_l10_cross_gate(
            freeze, cache_hashes, l10_stage, l10_audit_sha256
        )
        stages["target_hostile_l10_cross"] = l10_cross
        stages["target_hostile_l10_cross_sha256"] = l10_cross_sha256
        schedule, schedule_sha256 = require_parallel_l12_schedule_gate(
            l10_cross_sha256
        )
        stages["parallel_schedule"] = schedule
        stages["parallel_schedule_sha256"] = schedule_sha256
        schedule_audit, schedule_audit_sha256 = require_shared_schedule_audit(
            schedule, schedule_sha256, l10_cross_sha256
        )
        stages["parallel_schedule_audit"] = schedule_audit
        stages["parallel_schedule_audit_sha256"] = schedule_audit_sha256
        l12_authorization, target_l12_authorization_sha256 = (
            require_target_l12_execution_gate(
            freeze, physical_hash, cache_hashes, control_audit_sha256,
            l10_audit_sha256, l10_cross_sha256,
            schedule_audit_sha256,
            )
        )
        stages["target_l12_execution"] = l12_authorization
        stages["target_l12_execution_sha256"] = target_l12_authorization_sha256
        hostile_l12_authorization, hostile_l12_authorization_sha256 = (
            require_hostile_l12_execution_gate(
                hostile_branch, schedule_sha256, schedule_audit_sha256,
                l10_cross_sha256,
            )
        )
        stages["hostile_l12_execution"] = hostile_l12_authorization
        stages["hostile_l12_execution_sha256"] = hostile_l12_authorization_sha256
        handshake, handshake_sha256 = require_dual_l12_launch_handshake(
            schedule, schedule_sha256, schedule_audit_sha256,
            target_l12_authorization_sha256, hostile_l12_authorization_sha256,
        )
        stages["dual_l12_launch_handshake"] = handshake
        stages["dual_l12_launch_handshake_sha256"] = handshake_sha256
        release, release_sha256 = require_dual_l12_worker_release(
            schedule, handshake, handshake_sha256,
            target_l12_authorization_sha256, hostile_l12_authorization_sha256,
        )
        stages["dual_l12_worker_release"] = release
        stages["dual_l12_worker_release_sha256"] = release_sha256
        stages["hostile_records"] = hostile_records
        execution_authorization = l12_authorization
        execution_authorization_sha256 = target_l12_authorization_sha256
        promotion_audit_sha256 = schedule_audit_sha256
    if (
        execution_authorization is None
        or execution_authorization_sha256 is None
        or promotion_audit_sha256 is None
    ):
        raise Refusal("no stage-specific execution authorization")
    return {
        "dual": dual,
        "postbuild_payload_audit": postbuild,
        "physical": gate,
        "execution_authorization": execution_authorization,
        "execution_authorization_sha256": execution_authorization_sha256,
        "promotion_audit_sha256": promotion_audit_sha256,
        "stages": stages,
        "physical_sha256": physical_hash,
    }


def existing_parent(path: Path) -> Path:
    candidate = path.resolve(strict=False)
    while not candidate.exists():
        if candidate.parent == candidate:
            raise Refusal("physical workspace has no existing filesystem parent")
        candidate = candidate.parent
    if candidate.is_symlink() or not candidate.is_dir():
        raise Refusal("physical workspace parent is not an ordinary directory")
    return candidate


def project_native_method_record(method: object) -> dict[str, object]:
    """Project only the sealed resolution checkpoint tuple to native JSON."""
    source = getattr(method, "__dict__", None)
    if (
        type(source) is not dict
        or set(source) != {
            "label", "checkpoints", "quadrature_nodes", "tolerance",
        }
        or type(source.get("label")) is not str
        or not source["label"]
        or type(source.get("checkpoints")) is not tuple
        or not source["checkpoints"]
        or any(
            type(value) is not int or value <= 0
            for value in source["checkpoints"]
        )
        or list(source["checkpoints"])
        != sorted(set(source["checkpoints"]))
        or type(source.get("quadrature_nodes")) is not int
        or source["quadrature_nodes"] <= 0
        or type(source.get("tolerance")) is not float
        or not math.isfinite(source["tolerance"])
        or source["tolerance"] <= 0.0
    ):
        raise Refusal("sealed method native projection source mismatch")
    return {
        "label": source["label"],
        "checkpoints": list(source["checkpoints"]),
        "quadrature_nodes": source["quadrature_nodes"],
        "tolerance": source["tolerance"],
    }


def project_native_history_rows(rows: object) -> list[dict[str, object]]:
    """Project only the known NumPy owner residual to a native JSON float."""
    if type(rows) is not list or not rows:
        raise Refusal("history-row native projection source mismatch")
    projected: list[dict[str, object]] = []
    for row in rows:
        if (
            type(row) is not dict
            or "target_owner_residual" not in row
            or type(row["target_owner_residual"]) is not np.float64
            or not math.isfinite(float(row["target_owner_residual"]))
        ):
            raise Refusal("history-row owner residual projection source mismatch")
        native = dict(row)
        native["target_owner_residual"] = float(
            row["target_owner_residual"]
        )
        if any(
            native[key] is not value
            for key, value in row.items()
            if key != "target_owner_residual"
        ):
            raise AssertionError("history-row projection changed another field")
        projected.append(native)
    return projected


def seal_terminal_shards(length: int, sharp: dict[str, object], workspace: Path) -> None:
    rows = sharp.get("terminal_shards")
    if (
        not isinstance(rows, list)
        or len(rows) != length
        or [row.get("q") for row in rows if isinstance(row, dict)] != list(range(length))
    ):
        raise Refusal("terminal shard census absent before sealing")
    terminal_root = (workspace / "sharp" / f"prefix_{length - 1:02d}").resolve()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"q", "path", "shape", "bytes", "sha256"}:
            raise Refusal("terminal shard record malformed before sealing")
        path = _canonical_exact_path(
            row.get("path"), terminal_root / f"q_{row['q']:02d}.npy",
            f"new L{length} terminal shard q={row['q']}",
        )
        if path.is_symlink() or not path.is_file():
            raise Refusal("terminal shard escaped canonical workspace before sealing")
        if type(row.get("bytes")) is not int or path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
            raise Refusal("terminal shard changed before sealing")
        path.chmod(0o444)
        descriptor, close_descriptor = _authenticate_retained_file(
            path, f"new L{length} terminal shard q={row['q']}",
            row["sha256"],
        )
        try:
            if descriptor_sha256(descriptor) != row["sha256"]:
                raise Refusal("terminal shard changed while sealing")
            # Persist the payload and immutable mode before the JSON history
            # that names this shard can be atomically published.
            os.fsync(descriptor)
        finally:
            if close_descriptor:
                os.close(descriptor)
    terminal_root.chmod(0o555)
    terminal_root.parent.chmod(0o555)
    workspace.chmod(0o555)
    builder._fsync_directory(terminal_root)
    builder._fsync_directory(terminal_root.parent)
    builder._fsync_directory(workspace)
    builder._fsync_directory(workspace.parent)


def _execute_with_retained_authority(
    length: int, cache_root: Path, cache_manifest_sha256: str,
    output: Path, workspace: Path,
) -> None:
    global CACHE, PHYSICAL_STARTED, LAST_RESOURCE_CHECK
    if length not in builder.SUPPORTED:
        raise Refusal("unsupported physical size")
    gates = require_physical_gate(length, cache_manifest_sha256)
    expected_output = PHYSICAL_OUTPUT_PARENT / f"HISTORY_L{length}.json"
    expected_workspace = WORKSPACE_PARENT / f"L{length}"
    if output.resolve() != expected_output.resolve() or workspace.resolve() != expected_workspace.resolve():
        raise Refusal("physical output/workspace must use packet-local canonical paths")
    if (
        (PHYSICAL_OUTPUT_PARENT.exists() and PHYSICAL_OUTPUT_PARENT.is_symlink())
        or (WORKSPACE_PARENT.exists() and WORKSPACE_PARENT.is_symlink())
    ):
        raise Refusal("physical output/workspace parent is symlinked")
    if output.exists() or workspace.exists():
        raise Refusal("refuse to overwrite physical output or workspace")
    required_free = (
        builder.maximum_state_file_bytes(length)
        + builder.payload_bytes(length) + builder.OVERHEAD_RESERVE
    )
    workspace_filesystem = existing_parent(workspace)
    if required_free >= builder.SCRATCH_LIMIT or shutil.disk_usage(workspace_filesystem).free < required_free:
        raise Refusal("physical scratch gate failed")
    if builder.maximum_cache_window_bytes(length) > builder.MAPPED_CACHE_LIMIT:
        raise Refusal("mapped cache window gate failed")
    context: CacheContext | None = None
    patched = False
    started = time.perf_counter()
    PHYSICAL_STARTED = time.monotonic()
    LAST_RESOURCE_CHECK = 0.0
    try:
        context = CacheContext(cache_root, length, cache_manifest_sha256)
        CACHE = context
        v004.sealed.fixed_words = cached_fixed_words
        v004.sealed.Sector = CachedSector
        v004.create_admitted = cached_create_admitted
        v004.terminal_stream = cached_terminal_stream
        # The numerical engine remains byte-for-byte frozen. This authenticated
        # worker adapter owns the bounded wall-policy successor and changes no
        # Hamiltonian, lineage, admission, or accuracy parameter.
        v004.WALL_LIMIT = builder.WALL_LIMIT
        patched = True
        rough_root = workspace / "rough"
        sharp_root = workspace / "sharp"
        workspace.mkdir(parents=True, exist_ok=False)
        rough = v004.history(length, v004.sealed.COARSE, rough_root, retain_terminal=False)
        v004.remove_resolution(rough_root, workspace)
        sharp = v004.history(length, v004.sealed.FINE, sharp_root, retain_terminal=True)
        comparison = v004.sealed.summarize(length, rough, sharp)
        context.reauthenticate()
        guard_consumer(force=True)
        seal_terminal_shards(length, sharp, workspace)
        wall = time.perf_counter() - started
        rss = builder.rss_bytes()
        peak_state = max(int(rough["peak_logical_scratch_bytes"]), int(sharp["peak_logical_scratch_bytes"]))
        maximum_workset = max(int(row[key]["maximum_live_bytes"]) for row in sharp["rows"] for key in ("actual_solver", "null_solver"))
        resource_pass = (
            peak_state + builder.payload_bytes(length) + builder.OVERHEAD_RESERVE < builder.SCRATCH_LIMIT
            and maximum_workset <= v004.v3.CAP_BYTES
            and builder.maximum_cache_window_bytes(length) <= builder.MAPPED_CACHE_LIMIT
            and rss <= v004.RSS_LIMIT
            and wall <= builder.WALL_LIMIT
        )
        if not resource_pass:
            raise Refusal("physical resource reconstruction failed before output publication")
        if not isinstance(comparison, dict) or comparison.get("resolved") is not True:
            raise Refusal("rough/sharp comparison unresolved before output publication")
        coarse_method = project_native_method_record(v004.sealed.COARSE)
        fine_method = project_native_method_record(v004.sealed.FINE)
        history_rows = project_native_history_rows(sharp["rows"])
        reference, _reference_sha256 = immutable_json(
            CANONICAL_V004_HISTORY_PATH[length],
            f"canonical V004 L{length} prepublication projection",
            CANONICAL_V004_HISTORY_SHA256[length],
            require_immutable_mode=False,
        )
        _numeric_tree_close(
            coarse_method, reference.get("coarse_method"), 0.0,
            f"L{length} prepublication coarse method",
        )
        _numeric_tree_close(
            fine_method, reference.get("fine_method"), 0.0,
            f"L{length} prepublication fine method",
        )
        reference_rows = reference.get("rows")
        if (
            not isinstance(reference_rows, list)
            or len(reference_rows) != len(history_rows)
        ):
            raise Refusal("prepublication canonical row census mismatch")
        for event, (observed, canonical) in enumerate(
            zip(history_rows, reference_rows), start=1,
        ):
            if (
                not isinstance(canonical, dict)
                or set(observed) != set(canonical)
            ):
                raise Refusal(
                    f"L{length} prepublication event {event} row census mismatch"
                )
            _numeric_tree_close(
                {
                    key: value for key, value in observed.items()
                    if key not in {"actual_solver", "null_solver"}
                },
                {
                    key: value for key, value in canonical.items()
                    if key not in {"actual_solver", "null_solver"}
                },
                1.0e-8, f"L{length} prepublication event {event}",
            )
        freeze = builder.require_frozen_census()
        result = {
            "schema": "TARGET_CACHED_PREFIX_HISTORY_V012",
            "L": length,
            "events": length,
            "dimension": sharp["dimension"],
            "preterminal_dimension": sharp["preterminal_dimension"],
            "edges": sharp["edges"],
            "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__AUTHENTICATED_INDEX_CACHE",
            "lineage_authority": "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING",
            "coarse_method": coarse_method,
            "fine_method": fine_method,
            "rows": history_rows,
            "comparison": comparison,
            "terminal_shards": sharp["terminal_shards"],
            "cache_manifest_sha256": cache_manifest_sha256,
            "dual_obstruction_gate_sha256": sha256(builder.DUAL_GATE),
            "physical_execution_gate_sha256": gates["physical_sha256"],
            "execution_authorization_sha256": gates["execution_authorization_sha256"],
            "promotion_audit_sha256": gates["promotion_audit_sha256"],
            "cached_control_l4_l8_gate_sha256": (
                sha256(CACHED_CONTROL_GATE) if length >= 10 else None
            ),
            "cached_control_l4_l8_gate_audit_sha256": (
                sha256(CACHED_CONTROL_GATE_AUDIT) if length >= 10 else None
            ),
            "l10_execution_authorization_gate_sha256": (
                sha256(L10_EXECUTION_AUTHORIZATION_GATE) if length >= 10 else None
            ),
            "cached_l10_gate_sha256": sha256(CACHED_L10_GATE) if length == 12 else None,
            "cached_l10_gate_audit_sha256": (
                sha256(CACHED_L10_GATE_AUDIT) if length == 12 else None
            ),
            "target_hostile_l10_cross_gate_sha256": (
                gates["stages"]["target_hostile_l10_cross_sha256"]
                if length == 12 else None
            ),
            "shared_aggregate_schedule_gate_sha256": (
                gates["stages"]["parallel_schedule_sha256"]
                if length == 12 else None
            ),
            "shared_aggregate_schedule_gate_audit_sha256": (
                gates["stages"]["parallel_schedule_audit_sha256"]
                if length == 12 else None
            ),
            "target_l12_execution_gate_sha256": (
                gates["stages"]["target_l12_execution_sha256"]
                if length == 12 else None
            ),
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
            "preflight_result_sha256": sha256(HERE / "PREFLIGHT_RESULT_V001.json"),
            "independent_hostile_audit_sha256": immutable_json(
                builder.DUAL_GATE, "dual authorization gate"
            )[0]["independent_hostile_audit"]["sha256"],
            "resource": {
                "peak_live_state_bytes": peak_state,
                "cache_payload_bytes": builder.payload_bytes(length),
                "combined_with_reserve_bytes": peak_state + builder.payload_bytes(length) + builder.OVERHEAD_RESERVE,
                "scratch_limit_bytes": builder.SCRATCH_LIMIT,
                "maximum_numerical_workset_bytes": maximum_workset,
                "numerical_workset_limit_bytes": v004.v3.CAP_BYTES,
                "terminal_cache_peak_bytes": builder.terminal_cache_peak_bytes(length),
                "authentication_cache_peak_bytes": builder.authentication_cache_peak_bytes(length),
                "maximum_cache_window_bytes": builder.maximum_cache_window_bytes(length),
                "mapped_cache_limit_bytes": builder.MAPPED_CACHE_LIMIT,
                "peak_rss_bytes": rss,
                "rss_limit_bytes": v004.RSS_LIMIT,
                "wall_seconds": wall,
                "wall_limit_seconds": builder.WALL_LIMIT,
                "passed": True,
            },
            "consumer_sha256": freeze["files"]["consume_target_cache.py"],
            "builder_sha256": freeze["files"]["build_target_cache.py"],
            "method_sha256": freeze["files"]["METHOD.md"],
            "production_obligation_validators_sha256": freeze["files"][
                "production_obligation_validators.py"
            ],
            "freeze_sha256": sha256(FREEZE),
            "target_v004_sha256": builder.TARGET_V004_SHA256,
            "claim_boundary": "FINITE_CACHED_TARGET_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
        }
        if length == 12:
            result.update({
                "hostile_l12_execution_gate_sha256": gates["stages"][
                    "hostile_l12_execution_sha256"
                ],
                "dual_l12_launch_handshake_sha256": gates["stages"][
                    "dual_l12_launch_handshake_sha256"
                ],
                "dual_l12_worker_release_sha256": gates["stages"][
                    "dual_l12_worker_release_sha256"
                ],
            })
        if AUTHORITY_CUSTODY is None:
            raise Refusal("retained authority custody absent before publication")
        if length == 12:
            builder.validate_production_obligation(
                "A24_TARGET_L12_HISTORY", result
            )
        try:
            AUTHORITY_CUSTODY.verify_all()
        except builder.Refusal as error:
            raise Refusal(str(error)) from error
        output.parent.mkdir(parents=True, exist_ok=True)
        try:
            published_sha256 = builder.atomic_publish_json(
                output, result, f"target cached L{length} history",
                AUTHORITY_CUSTODY,
            )
        except builder.Refusal as error:
            raise Refusal(str(error)) from error
        if length == 12:
            if ORCHESTRATED_SESSION is None:
                raise Refusal("target worker session absent at L12 completion")
            ORCHESTRATED_SESSION.complete(published_sha256)
        print(comparison["classification"])
        print(f"L={length} cache={builder.payload_bytes(length)} state={peak_state} rss={rss} wall={wall:.3f}")
    finally:
        if patched:
            v004.sealed.fixed_words = ORIGINAL_FIXED_WORDS
            v004.sealed.Sector = ORIGINAL_SECTOR
            v004.create_admitted = ORIGINAL_CREATE_ADMITTED
            v004.terminal_stream = ORIGINAL_TERMINAL_STREAM
            v004.WALL_LIMIT = ORIGINAL_ENGINE_WALL_LIMIT
        CACHE = None
        PHYSICAL_STARTED = None
        LAST_RESOURCE_CHECK = 0.0
        if context is not None:
            context.close()


def execute(
    length: int, cache_root: Path, cache_manifest_sha256: str,
    output: Path, workspace: Path,
) -> None:
    global AUTHORITY_CUSTODY
    if AUTHORITY_CUSTODY is not None or builder.AUTHORITY_CUSTODY is not None:
        raise Refusal("nested retained authority custody session")
    custody = builder.StableAuthorityCustody()
    AUTHORITY_CUSTODY = custody
    builder.AUTHORITY_CUSTODY = custody
    try:
        _execute_with_retained_authority(
            length, cache_root, cache_manifest_sha256, output, workspace
        )
    finally:
        builder.AUTHORITY_CUSTODY = None
        AUTHORITY_CUSTODY = None
        custody.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("execute", choices=("execute",))
    parser.add_argument("--length", type=int, choices=builder.SUPPORTED, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--cache-manifest-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--orchestrated-worker", action="store_true")
    parser.add_argument("--control-fd", type=int)
    parser.add_argument("--control-channel-id")
    parser.add_argument("--worker-id")
    args = parser.parse_args()
    global ORCHESTRATED_SESSION
    try:
        orchestration_values = (
            args.orchestrated_worker, args.control_fd is not None,
            args.control_channel_id is not None, args.worker_id is not None,
        )
        if args.length == 12:
            if not all(orchestration_values):
                raise Refusal("target L12 requires the inherited orchestrator control channel")
            expected_cache = builder.CACHE_PARENT / "L12"
            expected_output = PHYSICAL_OUTPUT_PARENT / "HISTORY_L12.json"
            expected_workspace = WORKSPACE_PARENT / "L12"
            if (
                args.cache_root != expected_cache
                or args.output != expected_output
                or args.workspace != expected_workspace
            ):
                raise Refusal("target L12 orchestrated path identity mismatch")
            ORCHESTRATED_SESSION = OrchestratedWorkerSession(
                worker_id=args.worker_id, control_fd=args.control_fd,
                control_channel_id=args.control_channel_id,
                executable=HERE / "consume_target_cache.py",
                workspace=args.workspace, output=args.output,
            )
            ORCHESTRATED_SESSION.announce_and_wait()
        elif any(orchestration_values):
            raise Refusal("target L4-L10 does not accept L12 orchestration arguments")
        execute(args.length, args.cache_root, args.cache_manifest_sha256, args.output, args.workspace)
    except (AssertionError, MemoryError, OSError, Refusal, builder.Refusal, TimeoutError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    finally:
        if ORCHESTRATED_SESSION is not None:
            ORCHESTRATED_SESSION.close()
            ORCHESTRATED_SESSION = None
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
