#!/usr/bin/env python3
"""Exact streamed target adapter for the held-out L10/L12 joint witness.

This module deliberately separates preparation from physical execution.  The
streaming accumulator and all input-authentication machinery can be tested on
synthetic states.  The independently frozen held-out protocol is hash-bound,
but production execution still requires its exact role authorization and
fresh resource telemetry.

No L10/L12 witness value is computed when this module is imported or when its
synthetic test suite is run.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import importlib.util
import json
import math
import mmap
import os
import resource
import shutil
import stat
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

HELDOUT_PACKET_DIR = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_EXECUTION_V001"
)
HELDOUT_PROTOCOL_RELATIVE_PATH = f"{HELDOUT_PACKET_DIR}/PROTOCOL.md"
HELDOUT_PROTOCOL_SHA256 = (
    "8250e17405067deabbfe7dc4ff00864d26bef66cabfeef628f9f6df63829d9a7"
)
HELDOUT_GATE_RELATIVE_PATH = f"{HELDOUT_PACKET_DIR}/INPUT_AND_RESOURCE_GATE.json"
HELDOUT_GATE_SHA256 = (
    "2f38a50e530476e1f33647b49afc95d118738efb1ed53b6ba96335888a44432c"
)
HELDOUT_GATE_VALIDATOR_RELATIVE_PATH = f"{HELDOUT_PACKET_DIR}/validate_heldout_gate.py"
HELDOUT_GATE_VALIDATOR_SHA256 = (
    "4c138bcee4bd2230c369fab0592a3ba9430470c69a7c196e25680ca196f28a09"
)

SEED_DISPOSITION_RELATIVE_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_RECONCILIATION_V001/"
    "FINAL_DISPOSITION_V001.json"
)
SEED_DISPOSITION_SHA256 = (
    "2ce9852ef40d16d50b7a6553d0173e041c9cfdcc59925819f900f21f8a684f14"
)
SEED_CLASSIFICATION = "RESOLVED_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L4_L8"

TARGET_CACHE_DIR = "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
TARGET_CONSUMER_RELATIVE_PATH = f"{TARGET_CACHE_DIR}/consume_target_cache.py"
TARGET_CONSUMER_SHA256 = (
    "307b7232603f4de3937e4f8fad5aa281ff1f4cc33beaec28be6e18d9d8cc63fa"
)
TARGET_V004_RELATIVE_PATH = (
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py"
)
TARGET_V004_SHA256 = (
    "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7"
)
TARGET_V003_REPAIR_RELATIVE_PATH = (
    "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V003/repair_kernels.py"
)
TARGET_V003_REPAIR_SHA256 = (
    "5b04ae50ce3c9392e7a6be401625d580f4892e151578749bf7dba4ea1a1c6b37"
)
TARGET_V003_CAPACITY_PROFILE_RELATIVE_PATH = (
    "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_HELDOUT_TARGET_V001/"
    "TARGET_V003_CAPACITY_PROFILE.json"
)
TARGET_V003_CAPACITY_PROFILE_SHA256 = (
    "d2d5a83847af5fb671beb599950a48ad12bc925dd34c2fed1681d78cd73e2c58"
)

TARGET_V012_FREEZE_RELATIVE_PATH = f"{TARGET_CACHE_DIR}/FREEZE.json"
TARGET_V012_FREEZE_SHA256 = (
    "e3d13499135ffad51ffa0aa80f045902459d75a1fbd4f636e9e8dc963c76590b"
)
TARGET_V012_VALIDATORS_RELATIVE_PATH = (
    f"{TARGET_CACHE_DIR}/production_obligation_validators.py"
)
TARGET_V012_VALIDATORS_SHA256 = (
    "c1a0b6d8a39dc418523d988ddd97a5a30234cee4923efac654ab3ab48d7a93f7"
)
TARGET_V012_PREFLIGHT_RELATIVE_PATH = f"{TARGET_CACHE_DIR}/validate_preflight.py"
TARGET_V012_PREFLIGHT_SHA256 = (
    "56d0c6249f355ec4ba9b5c5bd6ddb44002ff91344b2aecc00457ddfb6711a2f1"
)
TARGET_V012_CACHE_MANIFEST_SHA256 = {
    f"{TARGET_CACHE_DIR}/CACHE_PAYLOADS_V012/L10/CACHE_MANIFEST.json":
        "80f52efaa4b455c7d68f4abef4b413a65c5a81633ec25f30c87fbbb4f2b3e743",
    f"{TARGET_CACHE_DIR}/CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json":
        "c8efb9b36ab18a3727aab4548109256640c92b63c121a07d9993999e4c570d6a",
}

CANONICAL_AUDITOR_PACKET_DIR = (
    "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
)
CANONICAL_AUDITOR_MANIFEST_RELATIVE_PATH = (
    f"{CANONICAL_AUDITOR_PACKET_DIR}/MANIFEST.sha256"
)
CANONICAL_AUDITOR_MANIFEST_SHA256 = (
    "fee085c6fb9e2166d752eaf0dc24a131fa0c8c40956fddb4199794fca07e1381"
)
CANONICAL_AUDITOR_ADJUDICATION_RELATIVE_PATH = (
    f"{CANONICAL_AUDITOR_PACKET_DIR}/ADJUDICATION_RECORD_V001.json"
)
CANONICAL_AUDITOR_ADJUDICATION_SHA256 = (
    "a05fef88aa0633958ac9f583fec00ab41dbcd10e3ddeae77b5ffc52d61f993e7"
)
CANONICAL_AUDITOR_REPLAY_NOTE_RELATIVE_PATH = (
    "L12_PRODUCTION_DAG_HISTORICAL_REPLAY_NOTE_2026-09-19.md"
)
CANONICAL_AUDITOR_REPLAY_NOTE_SHA256 = (
    "cf9cab4461e2a002cdfd671101c7906e5a00090d7b7196a914158c437081e037"
)
CANONICAL_AUDITOR_GIT_FOUNDATION_COMMIT = (
    "b5fc80e9da011e7e46c3dfe2d86b91a3b4f440cc"
)
CANONICAL_AUDITOR_FILENAME = "independent_final_auditor.py"
CANONICAL_AUDITOR_RELATIVE_PATH = (
    f"{CANONICAL_AUDITOR_PACKET_DIR}/{CANONICAL_AUDITOR_FILENAME}"
)
CANONICAL_AUDITOR_SHA256 = (
    "99677ffabeedc6db84047bd3637fd292e137d66c2de02eef66633ed789a92f2f"
)
STALE_V012_AUDITOR_SHA256 = (
    "cb1681c870b8382d9e7a83bec9df0830699d7b1015ed19b24360a3dbd4ae207e"
)
V012_AUDITOR_TRACK_KEY = CANONICAL_AUDITOR_RELATIVE_PATH
V012_STALE_TRACK_C_REFINEMENT_SHA256 = {
    V012_AUDITOR_TRACK_KEY: STALE_V012_AUDITOR_SHA256,
    f"{CANONICAL_AUDITOR_PACKET_DIR}/production_dag_refinement.py":
        "ec84094f6d4df6cb22a6fbae2205242f51e8217261e47b5b0fb460d245da5d56",
    f"{CANONICAL_AUDITOR_PACKET_DIR}/production_evidence_orchestrator.py":
        "d85275417f92961a2809822bcfc635d9e23e16bc7ad4fde43183ddcb78620b20",
}
CANONICAL_AUDITOR_PACKET_SHA256 = {
    "README.md": "e05b732f392d55d5d835071e44fc3701287a4fc7f92d52cf6e97a60d3678cbe0",
    "ADJUDICATION_RECORD_V001.json": CANONICAL_AUDITOR_ADJUDICATION_SHA256,
    "VERIFICATION.txt": "04f627cce60cdffad44b5772676c821663921a13627389e6c0465983a0182049",
    CANONICAL_AUDITOR_FILENAME: CANONICAL_AUDITOR_SHA256,
    "production_dag_refinement.py":
        "ec84094f6d4df6cb22a6fbae2205242f51e8217261e47b5b0fb460d245da5d56",
    "production_evidence_orchestrator.py":
        "d85275417f92961a2809822bcfc635d9e23e16bc7ad4fde43183ddcb78620b20",
    "stage1_artifact_census.py":
        "bb3d32b273be05716706510687b6760272a053fe4aa541b95e9850b5156f9f65",
    "synthetic_upstream_authority_fixtures.py":
        "ce2160f90951bb1c7c8c4f3b715101234adf9b04831e35f598a11cd2005568cb",
    "test_production_dag_refinement.py":
        "776695f55350c2d3c4a837497471a2b425840565bcd34585f14dccabb935e62a",
}

# Target-only numerical-capacity settings authenticated by the V003 repair
# source above.  They are repeated here instead of importing repair_kernels.py
# because that module also imports the independently held hostile branch.
# These settings enlarge approximation capacity only; the graph, Hamiltonian,
# route time, quadrature rules, and convergence tolerances remain unchanged.
TARGET_V003_MAX_SUBDIVISIONS = 256
TARGET_V003_COARSE_CHECKPOINTS = (12, 18, 24, 32, 48, 64, 80)
TARGET_V003_FINE_CHECKPOINTS = (16, 24, 32, 48, 64, 80, 96)
TARGET_V003_COARSE_QUADRATURE_NODES = 16
TARGET_V003_FINE_QUADRATURE_NODES = 24
TARGET_V003_COARSE_TOLERANCE = 2.0e-9
TARGET_V003_FINE_TOLERANCE = 5.0e-11

TARGET_TRANSITIVE_SOURCE_SHA256: dict[str, str] = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py":
        "307b7232603f4de3937e4f8fad5aa281ff1f4cc33beaec28be6e18d9d8cc63fa",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py":
        "bde9eb6f917291e78e8b8747e3b0f306e56ad6152c82f636dd90593a83e6b246",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py":
        "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v002.py":
        "71458cd4b958d5b38cb24409ed769e790d9a83e1da8ac71fd2d3098fdb779694",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history.py":
        "8bc59c363c638edd35db12fccb953a2590464b8f422f8a71f5ed4f3972951515",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py":
        "2cce210fff77ceb4ea91bce6fdd50ea75e1c7c5027471eaf4264ae794cc03b16",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/METHOD.md":
        "02c9fdbc4d784d3c9ae6e091b7351626dd9b524c15d13a5546bf31acb670271e",
    TARGET_V012_FREEZE_RELATIVE_PATH: TARGET_V012_FREEZE_SHA256,
    TARGET_V012_VALIDATORS_RELATIVE_PATH: TARGET_V012_VALIDATORS_SHA256,
    TARGET_V012_PREFLIGHT_RELATIVE_PATH: TARGET_V012_PREFLIGHT_SHA256,
    TARGET_V003_REPAIR_RELATIVE_PATH: TARGET_V003_REPAIR_SHA256,
    **TARGET_V012_CACHE_MANIFEST_SHA256,
}

COARSE_LABEL = "adaptive_expm_krylov_coarse"
FINE_LABEL = "adaptive_expm_krylov_sharp"
PHI = math.pi / 4.0
TERMINAL_ACCUMULATOR_WINDOW_BYTES = 128 * 2**20
RSS_LIMIT_BYTES = 16 * 2**30
SCRATCH_LIMIT_BYTES = 20 * 2**30

OUTPUT_NAME = "TARGET_HELDOUT_WITNESS_RESULT_V001.json"
EXECUTION_AUTHORIZATION = (
    "AUTHORIZE_EXACT_HELDOUT_TARGET_L10_L12_JOINT_WITNESS_V001"
)


class HeldoutRefusal(RuntimeError):
    """A custody, chronology, numerical, or resource predicate failed."""


class ResourceMonitor(Protocol):
    def check(self, stage: str, *, force: bool = False) -> None: ...


def _monitor(monitor: ResourceMonitor | None, stage: str, *, force: bool = False) -> None:
    if monitor is not None:
        monitor.check(stage, force=force)


def _stat_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _open_regular_nofollow(path: Path, *, require_readonly: bool) -> tuple[int, os.stat_result]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise HeldoutRefusal(f"cannot stably open required file: {path}: {error}") from error
    opened = os.fstat(descriptor)
    if not stat.S_ISREG(opened.st_mode) or (require_readonly and opened.st_mode & 0o222):
        os.close(descriptor)
        raise HeldoutRefusal(f"required file is nonregular or writable: {path}")
    return descriptor, opened


def _verify_descriptor_path(path: Path, descriptor: int, original: os.stat_result) -> None:
    current = os.fstat(descriptor)
    try:
        named = os.stat(path, follow_symlinks=False)
    except OSError as error:
        raise HeldoutRefusal(f"authenticated path disappeared: {path}") from error
    if _stat_identity(current) != _stat_identity(original):
        raise HeldoutRefusal(f"authenticated descriptor changed: {path}")
    if (named.st_dev, named.st_ino) != (original.st_dev, original.st_ino):
        raise HeldoutRefusal(f"authenticated path was replaced: {path}")


def _sha256_descriptor(
    descriptor: int,
    byte_count: int,
    *,
    window: int = 16 * 2**20,
    monitor: ResourceMonitor | None = None,
    stage: str = "hash",
) -> str:
    digest = hashlib.sha256()
    offset = 0
    while offset < byte_count:
        _monitor(monitor, stage)
        block = os.pread(descriptor, min(window, byte_count - offset), offset)
        if not block:
            raise HeldoutRefusal(f"short read during {stage}")
        digest.update(block)
        offset += len(block)
    _monitor(monitor, stage, force=True)
    return digest.hexdigest()


def sha256_file(
    path: Path,
    window: int = 16 * 2**20,
    *,
    monitor: ResourceMonitor | None = None,
    require_readonly: bool = False,
) -> str:
    descriptor, opened = _open_regular_nofollow(path, require_readonly=require_readonly)
    try:
        answer = _sha256_descriptor(
            descriptor,
            opened.st_size,
            window=window,
            monitor=monitor,
            stage=f"hash:{path.name}",
        )
        _verify_descriptor_path(path, descriptor, opened)
        return answer
    finally:
        os.close(descriptor)


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    answer: dict[str, object] = {}
    for key, value in pairs:
        if key in answer:
            raise HeldoutRefusal(f"duplicate JSON key: {key}")
        answer[key] = value
    return answer


def _reject_constant(token: str) -> object:
    raise HeldoutRefusal(f"nonfinite JSON constant: {token}")


def strict_json(
    path: Path,
    expected_sha256: str | None = None,
    *,
    monitor: ResourceMonitor | None = None,
) -> dict[str, object]:
    descriptor, opened = _open_regular_nofollow(path, require_readonly=False)
    try:
        raw = bytearray()
        offset = 0
        while offset < opened.st_size:
            _monitor(monitor, f"read-json:{path.name}")
            block = os.pread(descriptor, min(1 << 20, opened.st_size - offset), offset)
            if not block:
                raise HeldoutRefusal(f"short JSON read: {path}")
            raw.extend(block)
            offset += len(block)
        digest = hashlib.sha256(raw).hexdigest()
        _verify_descriptor_path(path, descriptor, opened)
    finally:
        os.close(descriptor)
    if expected_sha256 is not None and digest != expected_sha256:
        raise HeldoutRefusal(
            f"JSON SHA-256 mismatch for {path}: expected={expected_sha256} actual={digest}"
        )
    value = json.loads(
        bytes(raw).decode("utf-8"),
        object_pairs_hook=_strict_object,
        parse_constant=_reject_constant,
    )
    if not isinstance(value, dict):
        raise HeldoutRefusal(f"JSON input is not an object: {path}")
    return value


def _authenticated_bytes(
    path: Path,
    expected_sha256: str,
    *,
    monitor: ResourceMonitor | None = None,
    require_readonly: bool = False,
) -> bytes:
    descriptor, opened = _open_regular_nofollow(
        path, require_readonly=require_readonly
    )
    try:
        raw = bytearray()
        offset = 0
        while offset < opened.st_size:
            _monitor(monitor, f"read-authenticated:{path.name}")
            block = os.pread(descriptor, min(1 << 20, opened.st_size - offset), offset)
            if not block:
                raise HeldoutRefusal(f"short authenticated read: {path}")
            raw.extend(block)
            offset += len(block)
        actual = hashlib.sha256(raw).hexdigest()
        _verify_descriptor_path(path, descriptor, opened)
    finally:
        os.close(descriptor)
    if actual != expected_sha256:
        raise HeldoutRefusal(
            f"authenticated source SHA-256 mismatch for {path}: "
            f"expected={expected_sha256} actual={actual}"
        )
    return bytes(raw)


def authenticate_canonical_final_auditor(
    root: Path = ROOT,
    *,
    monitor: ResourceMonitor | None = None,
) -> dict[str, str]:
    """Authenticate the sole historical cb1681 -> 99677 provenance correction."""
    manifest_path = root / CANONICAL_AUDITOR_MANIFEST_RELATIVE_PATH
    raw_manifest = _authenticated_bytes(
        manifest_path,
        CANONICAL_AUDITOR_MANIFEST_SHA256,
        monitor=monitor,
        require_readonly=True,
    )
    try:
        lines = raw_manifest.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise HeldoutRefusal("canonical auditor manifest is not ASCII") from error
    manifest: dict[str, str] = {}
    for line in lines:
        fields = line.split("  ")
        if (
            len(fields) != 2
            or len(fields[0]) != 64
            or any(character not in "0123456789abcdef" for character in fields[0])
            or not fields[1]
            or "/" in fields[1]
            or fields[1] in manifest
        ):
            raise HeldoutRefusal("canonical auditor manifest syntax/census drift")
        manifest[fields[1]] = fields[0]
    if manifest != CANONICAL_AUDITOR_PACKET_SHA256:
        raise HeldoutRefusal("canonical auditor manifest content drift")

    observed = {
        CANONICAL_AUDITOR_MANIFEST_RELATIVE_PATH:
            CANONICAL_AUDITOR_MANIFEST_SHA256,
    }
    for filename, expected in manifest.items():
        relative = f"{CANONICAL_AUDITOR_PACKET_DIR}/{filename}"
        actual = sha256_file(
            root / relative,
            monitor=monitor,
            require_readonly=True,
        )
        if actual != expected:
            raise HeldoutRefusal(f"canonical auditor packet drift: {relative}")
        observed[relative] = actual

    adjudication = strict_json(
        root / CANONICAL_AUDITOR_ADJUDICATION_RELATIVE_PATH,
        CANONICAL_AUDITOR_ADJUDICATION_SHA256,
        monitor=monitor,
    )
    source_sha256 = adjudication.get("source_sha256")
    if (
        not isinstance(source_sha256, dict)
        or source_sha256.get(CANONICAL_AUDITOR_FILENAME)
        != CANONICAL_AUDITOR_SHA256
    ):
        raise HeldoutRefusal("canonical auditor adjudication does not pin 99677")

    replay_note = root / CANONICAL_AUDITOR_REPLAY_NOTE_RELATIVE_PATH
    replay_actual = sha256_file(replay_note, monitor=monitor)
    if replay_actual != CANONICAL_AUDITOR_REPLAY_NOTE_SHA256:
        raise HeldoutRefusal("canonical auditor Git-era replay evidence drift")
    observed[CANONICAL_AUDITOR_REPLAY_NOTE_RELATIVE_PATH] = replay_actual
    return observed


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
                allow_nan=False,
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise HeldoutRefusal("record is not finite canonical JSON") from error


def canonical_digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def repository_relative(path: Path, root: Path = ROOT) -> str:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except (OSError, ValueError) as error:
        raise HeldoutRefusal(f"path escapes repository: {path}") from error
    if not relative.parts or ".." in relative.parts:
        raise HeldoutRefusal(f"unsafe repository-relative path: {path}")
    return relative.as_posix()


def require_no_symlink_chain(path: Path, root: Path = ROOT) -> Path:
    root_resolved = root.resolve()
    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError as error:
        raise HeldoutRefusal(f"path is outside repository spelling: {path}") from error
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() or cursor.is_symlink():
            try:
                mode = os.lstat(cursor).st_mode
            except OSError as error:
                raise HeldoutRefusal(f"cannot inspect path component: {cursor}") from error
            if stat.S_ISLNK(mode):
                raise HeldoutRefusal(f"symlink path component refused: {cursor}")
    resolved = path.resolve(strict=False)
    if resolved != root_resolved / relative:
        raise HeldoutRefusal(f"path has a noncanonical resolution: {path}")
    return resolved


def authenticate_target_capacity_profile(
    root: Path = ROOT,
    *,
    monitor: ResourceMonitor | None = None,
) -> dict[str, object]:
    record = strict_json(
        root / TARGET_V003_CAPACITY_PROFILE_RELATIVE_PATH,
        TARGET_V003_CAPACITY_PROFILE_SHA256,
        monitor=monitor,
    )
    expected = {
        "claim_boundary": (
            "TARGET_NUMERICAL_CAPACITY_ONLY__NO_GRAPH_HAMILTONIAN_ROUTE_"
            "OBSERVABLE_OR_TOLERANCE_CHANGE"
        ),
        "coarse": {
            "checkpoints": list(TARGET_V003_COARSE_CHECKPOINTS),
            "label": "coarse",
            "quadrature_nodes": TARGET_V003_COARSE_QUADRATURE_NODES,
            "tolerance": TARGET_V003_COARSE_TOLERANCE,
        },
        "fine": {
            "checkpoints": list(TARGET_V003_FINE_CHECKPOINTS),
            "label": "fine",
            "quadrature_nodes": TARGET_V003_FINE_QUADRATURE_NODES,
            "tolerance": TARGET_V003_FINE_TOLERANCE,
        },
        "maximum_subdivisions": TARGET_V003_MAX_SUBDIVISIONS,
        "repair_source_path": TARGET_V003_REPAIR_RELATIVE_PATH,
        "repair_source_sha256": TARGET_V003_REPAIR_SHA256,
        "schema": "OWNER_ONCE_HELDOUT_TARGET_V003_CAPACITY_PROFILE_V001",
    }
    if record != expected:
        raise HeldoutRefusal("authenticated target V003 capacity profile changed")
    return record


def authenticate_target_transitive_sources(
    root: Path = ROOT,
    *,
    monitor: ResourceMonitor | None = None,
) -> dict[str, str]:
    authenticate_target_capacity_profile(root, monitor=monitor)
    observed: dict[str, str] = {}
    for relative, expected in TARGET_TRANSITIVE_SOURCE_SHA256.items():
        actual = sha256_file(root / relative, monitor=monitor)
        if actual != expected:
            raise HeldoutRefusal(f"target transitive source drift: {relative}")
        observed[relative] = actual
    observed.update(authenticate_canonical_final_auditor(root, monitor=monitor))
    return observed


def finite(value: Any, label: str) -> float:
    try:
        answer = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise HeldoutRefusal(f"nonnumeric {label}: {value!r}") from error
    if not math.isfinite(answer):
        raise HeldoutRefusal(f"nonfinite {label}: {answer!r}")
    return answer


def bitcount(word: int) -> int:
    return bin(int(word)).count("1")


BYTE_POPCOUNT = np.array([bin(index).count("1") for index in range(256)], dtype=np.uint8)


def vector_bitcount(words: np.ndarray) -> np.ndarray:
    """Return population counts without a Python loop or platform popcount dependency."""
    contiguous = np.ascontiguousarray(words)
    if contiguous.dtype.kind != "u" or contiguous.dtype.itemsize not in (1, 2, 4, 8):
        raise HeldoutRefusal(f"unsupported word dtype for popcount: {contiguous.dtype}")
    bytes_view = contiguous.view(np.uint8).reshape(contiguous.shape + (contiguous.itemsize,))
    return np.sum(BYTE_POPCOUNT[bytes_view], axis=-1, dtype=np.uint16)


def fixed_words(width: int, weight: int) -> np.ndarray:
    """Synthetic/test-only canonical fixed-weight words."""
    import itertools

    if not 0 <= weight <= width:
        raise HeldoutRefusal("invalid fixed-word request")
    dtype = np.uint32 if width <= 32 else np.uint64
    output = np.empty(math.comb(width, weight), dtype=dtype)
    for index, positions in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        output[index] = word
    return output


@dataclass(frozen=True)
class HistoryBinding:
    length: int
    history_relative_path: str
    history_sha256: str
    workspace_relative_path: str
    cache_manifest_sha256: str
    expected_schema: str
    terminal_manifest_sha256: str
    terminal_total_bytes: int


HISTORY_BINDINGS: dict[int, HistoryBinding] = {
    10: HistoryBinding(
        length=10,
        history_relative_path=f"{TARGET_CACHE_DIR}/PHYSICAL_OUTPUTS/HISTORY_L10.json",
        history_sha256="898f09564d3e055fe6edeb55eab2179f2847c97b6f00cfd4b9dfb94c9c63afa7",
        workspace_relative_path=f"{TARGET_CACHE_DIR}/WORKSPACES/L10/sharp/prefix_09",
        cache_manifest_sha256="80f52efaa4b455c7d68f4abef4b413a65c5a81633ec25f30c87fbbb4f2b3e743",
        expected_schema="TARGET_CACHED_PREFIX_HISTORY_V012",
        terminal_manifest_sha256="c6d3538f02b21b7f9294acdb8c0dfeb8772de4f3c389da40c8a9879c77951cb8",
        terminal_total_bytes=160_241_360,
    ),
    12: HistoryBinding(
        length=12,
        history_relative_path=(
            f"{TARGET_CACHE_DIR}/PHYSICAL_OUTPUTS/"
            "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
        ),
        history_sha256="079499e7b989e1ba45b1c397882c8638106be149ccb994058a3703b235736764",
        workspace_relative_path=(
            f"{TARGET_CACHE_DIR}/WORKSPACES/"
            "L12_PROCESS_PARALLEL_V003R1/sharp/prefix_11"
        ),
        cache_manifest_sha256="c8efb9b36ab18a3727aab4548109256640c92b63c121a07d9993999e4c570d6a",
        expected_schema="TARGET_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V003",
        terminal_manifest_sha256="c4045ebb1ae2681832955537fe93c796ff2ddce3bcb300390e68b8588b1d594f",
        terminal_total_bytes=6_675_615_936,
    ),
}


@dataclass(frozen=True)
class AuthenticatedShard:
    q: int
    path: Path
    shape: tuple[int, int]
    byte_count: int
    sha256: str


@dataclass(frozen=True)
class AuthenticatedHistory:
    binding: HistoryBinding
    history: Mapping[str, object]
    shards: tuple[AuthenticatedShard, ...]


@dataclass
class StableOpenShard:
    """One immutable NPY shard held through one descriptor and mmap lifetime."""

    metadata: AuthenticatedShard
    descriptor: int
    opened_stat: os.stat_result
    payload_offset: int
    mapping: mmap.mmap
    array: np.ndarray
    closed: bool = False

    def verify(self, monitor: ResourceMonitor | None = None) -> None:
        if self.closed:
            raise HeldoutRefusal(f"stable shard already closed q={self.metadata.q}")
        _verify_descriptor_path(
            self.metadata.path, self.descriptor, self.opened_stat
        )
        digest = _sha256_descriptor(
            self.descriptor,
            self.metadata.byte_count,
            monitor=monitor,
            stage=f"reauth-shard-q{self.metadata.q}",
        )
        if digest != self.metadata.sha256:
            raise HeldoutRefusal(f"stable shard hash changed q={self.metadata.q}")

    def close(self) -> None:
        if self.closed:
            return
        self.array = np.empty((0, 0), dtype=np.complex128)
        self.mapping.close()
        os.close(self.descriptor)
        self.closed = True


@dataclass
class StableOpenHistory:
    authenticated: AuthenticatedHistory | None
    shards: tuple[StableOpenShard, ...]

    @property
    def arrays(self) -> tuple[np.ndarray, ...]:
        return tuple(item.array for item in self.shards)

    def verify(self, monitor: ResourceMonitor | None = None) -> None:
        for shard in self.shards:
            shard.verify(monitor)

    def close(self) -> None:
        for shard in self.shards:
            shard.close()


def authenticate_heldout_protocol(root: Path = ROOT) -> dict[str, str]:
    path = root / HELDOUT_PROTOCOL_RELATIVE_PATH
    actual = sha256_file(path)
    if actual != HELDOUT_PROTOCOL_SHA256:
        raise HeldoutRefusal(
            f"held-out protocol SHA-256 mismatch: expected={HELDOUT_PROTOCOL_SHA256} actual={actual}"
        )
    gate_path = root / HELDOUT_GATE_RELATIVE_PATH
    gate_actual = sha256_file(gate_path)
    if gate_actual != HELDOUT_GATE_SHA256:
        raise HeldoutRefusal(
            f"held-out gate SHA-256 mismatch: expected={HELDOUT_GATE_SHA256} "
            f"actual={gate_actual}"
        )
    validator_path = root / HELDOUT_GATE_VALIDATOR_RELATIVE_PATH
    validator_actual = sha256_file(validator_path)
    if validator_actual != HELDOUT_GATE_VALIDATOR_SHA256:
        raise HeldoutRefusal(
            "held-out gate validator SHA-256 mismatch: "
            f"expected={HELDOUT_GATE_VALIDATOR_SHA256} actual={validator_actual}"
        )
    return {
        "path": HELDOUT_PROTOCOL_RELATIVE_PATH,
        "sha256": actual,
        "gate_path": HELDOUT_GATE_RELATIVE_PATH,
        "gate_sha256": gate_actual,
        "validator_path": HELDOUT_GATE_VALIDATOR_RELATIVE_PATH,
        "validator_sha256": validator_actual,
    }


def authenticate_seed_authority(root: Path = ROOT) -> dict[str, object]:
    path = root / SEED_DISPOSITION_RELATIVE_PATH
    record = strict_json(path, SEED_DISPOSITION_SHA256)
    heldout = record.get("held_out_L10_L12")
    if (
        record.get("schema")
        != "OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_RECONCILIATION_V001"
        or record.get("protocol_classification") != SEED_CLASSIFICATION
        or record.get("reconciliation_disposition")
        != "SEALED_TARGET_HOSTILE_RECONCILIATION_COMPLETE"
        or record.get("passed") is not True
        or record.get("all_numerical_and_control_conditions_passed") is not True
        or type(record.get("T_4_8")) not in (int, float)
        or not math.isfinite(float(record["T_4_8"]))
        or float(record["T_4_8"]) <= 1.0
        or not isinstance(heldout, dict)
        or heldout.get("seed_prerequisites_1_through_3_satisfied") is not True
        or heldout.get("computed_or_opened_by_reconciliation") is not False
    ):
        raise HeldoutRefusal("sealed L4/L6/L8 authority does not authorize held-out preparation")
    return {
        "path": SEED_DISPOSITION_RELATIVE_PATH,
        "sha256": SEED_DISPOSITION_SHA256,
        "T_4_8": float(record["T_4_8"]),
        "classification": str(record["protocol_classification"]),
    }


def _npy_header_descriptor(
    descriptor: int, path: Path
) -> tuple[tuple[int, ...], np.dtype[Any], int]:
    with os.fdopen(os.dup(descriptor), "rb") as stream:
        version = np.lib.format.read_magic(stream)
        if version == (1, 0):
            shape, fortran, dtype = np.lib.format.read_array_header_1_0(stream)
        elif version in {(2, 0), (3, 0)}:
            shape, fortran, dtype = np.lib.format.read_array_header_2_0(stream)
        else:
            raise HeldoutRefusal(f"unsupported NPY version {version}: {path}")
        offset = stream.tell()
    if fortran:
        raise HeldoutRefusal(f"terminal shard is unexpectedly Fortran ordered: {path}")
    return tuple(int(item) for item in shape), np.dtype(dtype), offset


def _npy_header(path: Path) -> tuple[tuple[int, ...], np.dtype[Any], int]:
    descriptor, opened = _open_regular_nofollow(path, require_readonly=True)
    try:
        answer = _npy_header_descriptor(descriptor, path)
        _verify_descriptor_path(path, descriptor, opened)
        return answer
    finally:
        os.close(descriptor)


def authenticate_retained_history(
    length: int,
    *,
    root: Path = ROOT,
    verify_payload_hashes: bool,
    monitor: ResourceMonitor | None = None,
) -> AuthenticatedHistory:
    try:
        binding = HISTORY_BINDINGS[length]
    except KeyError as error:
        raise HeldoutRefusal(f"unsupported held-out size: {length}") from error
    record = strict_json(
        root / binding.history_relative_path,
        binding.history_sha256,
        monitor=monitor,
    )
    terminal = record.get("terminal_shards")
    if (
        record.get("schema") != binding.expected_schema
        or record.get("L") != length
        or record.get("cache_manifest_sha256") != binding.cache_manifest_sha256
        or record.get("lineage_authority")
        != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
        or not isinstance(terminal, list)
        or len(terminal) != length
    ):
        raise HeldoutRefusal(f"L{length} retained history identity mismatch")
    workspace = root / binding.workspace_relative_path
    require_no_symlink_chain(workspace, root)
    if workspace.is_symlink() or not workspace.is_dir():
        raise HeldoutRefusal(f"L{length} canonical retained workspace absent")
    expected_names = {f"q_{q:02d}.npy" for q in range(length)}
    try:
        actual_entries = list(os.scandir(workspace))
    except OSError as error:
        raise HeldoutRefusal(f"cannot enumerate retained workspace L{length}") from error
    actual_names = {entry.name for entry in actual_entries}
    if actual_names != expected_names or any(
        not entry.is_file(follow_symlinks=False) for entry in actual_entries
    ):
        raise HeldoutRefusal(f"L{length} retained workspace census mismatch")
    shards: list[AuthenticatedShard] = []
    for q, row in enumerate(terminal):
        expected_shape = (math.comb(length - 1, q), math.comb(2 * length, q))
        path = workspace / f"q_{q:02d}.npy"
        if isinstance(row, dict) and isinstance(row.get("path"), str):
            recorded_path = Path(str(row["path"]))
            if recorded_path.is_absolute():
                try:
                    recorded_relative = recorded_path.resolve().relative_to(root.resolve())
                except ValueError as error:
                    raise HeldoutRefusal(
                        f"L{length} q={q} recorded shard path escapes repository"
                    ) from error
            else:
                if ".." in recorded_path.parts:
                    raise HeldoutRefusal(f"L{length} q={q} unsafe recorded shard path")
                recorded_relative = recorded_path
            expected_relative = Path(binding.workspace_relative_path) / path.name
            if recorded_relative != expected_relative:
                raise HeldoutRefusal(f"L{length} q={q} recorded shard path mismatch")
        if (
            not isinstance(row, dict)
            or set(row) != {"bytes", "path", "q", "sha256", "shape"}
            or row.get("q") != q
            or row.get("shape") != list(expected_shape)
            or type(row.get("bytes")) is not int
            or type(row.get("sha256")) is not str
            or len(str(row["sha256"])) != 64
            or path.is_symlink()
            or not path.is_file()
            or path.stat().st_size != row["bytes"]
        ):
            raise HeldoutRefusal(f"L{length} q={q} terminal-shard manifest mismatch")
        shape, dtype, offset = _npy_header(path)
        expected_bytes = offset + 16 * math.prod(expected_shape)
        if shape != expected_shape or dtype != np.dtype(np.complex128) or row["bytes"] != expected_bytes:
            raise HeldoutRefusal(f"L{length} q={q} terminal-shard NPY layout mismatch")
        if verify_payload_hashes and sha256_file(
            path,
            monitor=monitor,
            require_readonly=True,
        ) != row["sha256"]:
            raise HeldoutRefusal(f"L{length} q={q} terminal-shard payload hash mismatch")
        shards.append(
            AuthenticatedShard(
                q=q,
                path=path,
                shape=expected_shape,
                byte_count=int(row["bytes"]),
                sha256=str(row["sha256"]),
            )
        )
    canonical_rows = [
        {
            "bytes": item.byte_count,
            "path": (
                Path(binding.workspace_relative_path) / item.path.name
            ).as_posix(),
            "q": item.q,
            "sha256": item.sha256,
            "shape": list(item.shape),
        }
        for item in shards
    ]
    if (
        sum(item.byte_count for item in shards) != binding.terminal_total_bytes
        or canonical_digest(canonical_rows) != binding.terminal_manifest_sha256
    ):
        raise HeldoutRefusal(f"L{length} canonical terminal manifest mismatch")
    return AuthenticatedHistory(binding=binding, history=record, shards=tuple(shards))


def open_authenticated_history(
    length: int,
    *,
    root: Path = ROOT,
    monitor: ResourceMonitor | None = None,
) -> StableOpenHistory:
    """Authenticate and retain one stable descriptor/mmap per target shard."""
    history = authenticate_retained_history(
        length,
        root=root,
        verify_payload_hashes=False,
        monitor=monitor,
    )
    opened: list[StableOpenShard] = []
    try:
        for metadata in history.shards:
            descriptor, descriptor_stat = _open_regular_nofollow(
                metadata.path, require_readonly=True
            )
            try:
                shape, dtype, offset = _npy_header_descriptor(
                    descriptor, metadata.path
                )
                if shape != metadata.shape or dtype != np.dtype(np.complex128):
                    raise HeldoutRefusal(
                        f"stable shard layout mismatch q={metadata.q}"
                    )
                if offset + 16 * math.prod(shape) != metadata.byte_count:
                    raise HeldoutRefusal(
                        f"stable shard byte layout mismatch q={metadata.q}"
                    )
                digest = _sha256_descriptor(
                    descriptor,
                    metadata.byte_count,
                    monitor=monitor,
                    stage=f"authenticate-shard-L{length}-q{metadata.q}",
                )
                if digest != metadata.sha256:
                    raise HeldoutRefusal(
                        f"stable shard digest mismatch q={metadata.q}"
                    )
                _verify_descriptor_path(metadata.path, descriptor, descriptor_stat)
                mapped = mmap.mmap(descriptor, 0, access=mmap.ACCESS_READ)
                array = np.ndarray(
                    shape,
                    dtype=np.complex128,
                    buffer=mapped,
                    offset=offset,
                    order="C",
                )
                array.flags.writeable = False
                opened.append(
                    StableOpenShard(
                        metadata=metadata,
                        descriptor=descriptor,
                        opened_stat=descriptor_stat,
                        payload_offset=offset,
                        mapping=mapped,
                        array=array,
                    )
                )
            except BaseException:
                os.close(descriptor)
                raise
        return StableOpenHistory(history, tuple(opened))
    except BaseException:
        for shard in opened:
            shard.close()
        raise


class TerminalBackend(Protocol):
    length: int

    def lineage_words(self, prefix: int, q: int) -> np.ndarray: ...

    def carrier_words(self, q: int) -> np.ndarray: ...

    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]: ...

    def evolve(self, q: int, amplitudes: np.ndarray, resolution: object) -> np.ndarray: ...

    def batch_rows(self, columns: int, resolution: object) -> int: ...

    def close(self) -> None: ...


@dataclass
class SectorMomentAccumulator:
    """Sufficient statistics for one final sharp-q sector.

    The row and column paths deliberately use different contraction orders.
    They consume bounded terminal windows and never materialize H_L.
    """

    length: int
    q: int
    carrier_words: np.ndarray
    lineage_mass_row: dict[int, float] = field(default_factory=dict)
    lineage_mass_column: dict[int, float] = field(default_factory=dict)
    carrier_mass_row: np.ndarray = field(init=False)
    carrier_mass_column: np.ndarray = field(init=False)
    w_row: float = 0.0
    w_column: float = 0.0
    maximum_charge_error: int = 0

    def __post_init__(self) -> None:
        if len(self.carrier_words) != math.comb(2 * self.length, self.q):
            raise HeldoutRefusal(f"carrier census mismatch L={self.length} q={self.q}")
        self.carrier_mass_row = np.zeros(len(self.carrier_words), dtype=np.float64)
        self.carrier_mass_column = np.zeros(len(self.carrier_words), dtype=np.float64)
        if len(self.carrier_words) and bool(
            np.any(vector_bitcount(self.carrier_words) != self.q)
        ):
            raise HeldoutRefusal(f"carrier charge mismatch L={self.length} q={self.q}")

    def consume(self, lineage_words: np.ndarray, amplitudes: np.ndarray) -> None:
        if amplitudes.shape != (len(lineage_words), len(self.carrier_words)):
            raise HeldoutRefusal(f"terminal window shape mismatch q={self.q}")
        if not bool(np.all(np.isfinite(amplitudes))):
            raise HeldoutRefusal(f"nonfinite terminal amplitudes q={self.q}")
        probability = amplitudes.real * amplitudes.real + amplitudes.imag * amplitudes.imag
        if not bool(np.all(np.isfinite(probability))) or float(np.min(probability)) < 0.0:
            raise HeldoutRefusal(f"invalid terminal probabilities q={self.q}")

        # Marginals are accumulated through transposed reduction paths so the
        # row/column control remains separately ordered without a Python loop
        # over the potentially millions of carrier columns.
        row_mass = np.sum(probability, axis=1)
        column_lineage_mass = np.sum(probability.T, axis=0)
        self.carrier_mass_row += np.sum(probability, axis=0)
        self.carrier_mass_column += np.sum(probability.T, axis=1)
        for local, raw_word in enumerate(lineage_words):
            word = int(raw_word)
            error = abs(bitcount(word) - self.q)
            self.maximum_charge_error = max(self.maximum_charge_error, error)
            self.lineage_mass_row[word] = (
                self.lineage_mass_row.get(word, 0.0) + float(row_mass[local])
            )
            self.lineage_mass_column[word] = (
                self.lineage_mass_column.get(word, 0.0)
                + float(column_lineage_mass[local])
            )

        lineage_bits = (
            (lineage_words.astype(np.uint64)[:, np.newaxis]
             >> np.arange(self.length, dtype=np.uint64)[np.newaxis, :])
            & 1
        ).astype(np.float64)
        centered = lineage_bits - self.q / self.length
        row_contributions = np.zeros(len(lineage_words), dtype=np.float64)
        column_contribution = 0.0
        for event in range(self.length):
            occupied = ((self.carrier_words >> event) & 1) == 1
            if not bool(np.any(occupied)):
                continue
            event_probability = probability[:, occupied]
            event_row_mass = np.sum(event_probability, axis=1)
            row_contributions += centered[:, event] * event_row_mass
            # This contraction starts from carrier columns and reduces the
            # lineage axis first.  It is mathematically identical but ordered
            # independently from the row accumulator above.
            by_column = np.dot(centered[:, event], event_probability)
            column_contribution += float(np.sum(by_column))
        self.w_row += float(np.sum(row_contributions)) / self.length
        self.w_column += column_contribution / self.length

    def finalize(self) -> dict[str, object]:
        words = sorted(set(self.lineage_mass_row) | set(self.lineage_mass_column))
        lineage_row = np.array([self.lineage_mass_row.get(word, 0.0) for word in words])
        lineage_column = np.array([self.lineage_mass_column.get(word, 0.0) for word in words])
        p_row = float(np.sum(lineage_row))
        p_column = float(np.sum(self.carrier_mass_column))
        lineage_first_moment = np.zeros(self.length)
        lineage_first_moment_column = np.zeros(self.length)
        for word, mass in zip(words, lineage_row):
            for event in range(self.length):
                if (word >> event) & 1:
                    lineage_first_moment[event] += mass
        for word, mass in zip(words, lineage_column):
            for event in range(self.length):
                if (word >> event) & 1:
                    lineage_first_moment_column[event] += mass
        carrier_first_moment = np.zeros(self.length)
        carrier_first_moment_column = np.zeros(self.length)
        for event in range(self.length):
            occupied = ((self.carrier_words >> event) & 1) == 1
            carrier_first_moment[event] = float(np.sum(self.carrier_mass_row[occupied]))
            carrier_first_moment_column[event] = float(
                np.sum(self.carrier_mass_column[occupied])
            )

        if p_row > 0.0:
            centered = lineage_first_moment - (self.q / self.length) * p_row
            sham = float(np.dot(centered, carrier_first_moment) / (self.length * p_row))
            direct_sham = 0.0
            for word, mass in zip(words, lineage_row):
                centered_bits = np.array(
                    [((word >> event) & 1) - self.q / self.length
                     for event in range(self.length)],
                    dtype=np.float64,
                )
                direct_sham += (
                    float(mass)
                    * float(np.dot(centered_bits, carrier_first_moment))
                    / (self.length * p_row)
                )
        else:
            sham = direct_sham = 0.0
        if p_column > 0.0:
            centered_column = (
                lineage_first_moment_column - (self.q / self.length) * p_column
            )
            sham_column = float(
                np.dot(centered_column, carrier_first_moment_column)
                / (self.length * p_column)
            )
        else:
            sham_column = 0.0

        # Exact permutation orbit identity: C(L-1,q-1)/C(L,q) == q/L.
        orbit = Fraction(0, 1) if self.q == 0 else Fraction(
            math.comb(self.length - 1, self.q - 1), math.comb(self.length, self.q)
        )
        shuffle_identity = orbit - Fraction(self.q, self.length)
        shuffle = float(shuffle_identity) * float(np.sum(carrier_first_moment)) / self.length
        row_d = self.w_row - sham
        column_d = self.w_column - sham_column
        marginal_error = max(
            abs(p_row - p_column),
            abs(float(np.sum(self.carrier_mass_row)) - p_row),
            abs(float(np.sum(self.carrier_mass_column)) - p_column),
            float(np.max(np.abs(lineage_row - lineage_column))) if len(words) else 0.0,
            float(np.max(np.abs(self.carrier_mass_row - self.carrier_mass_column)))
            if len(self.carrier_mass_row) else 0.0,
        )
        row_record = {
            "p_q": finite(p_row, f"p_q q={self.q}"),
            "w_q": finite(self.w_row, f"w_q q={self.q}"),
            "w_sham_q": finite(sham, f"w_sham_q q={self.q}"),
            "D_q": finite(row_d, f"D_q q={self.q}"),
            "w_shuffle_q": finite(shuffle, f"w_shuffle_q q={self.q}"),
        }
        column_record = {
            "p_q": finite(p_column, f"column p_q q={self.q}"),
            "w_q": finite(self.w_column, f"column w_q q={self.q}"),
            "w_sham_q": finite(sham_column, f"column w_sham_q q={self.q}"),
            "D_q": finite(column_d, f"column D_q q={self.q}"),
            "w_shuffle_q": finite(shuffle, f"column w_shuffle_q q={self.q}"),
        }
        return {
            **row_record,
            "row": row_record,
            "column": column_record,
            "residuals": {
                "row_column": max(
                    abs(float(row_record[key]) - float(column_record[key]))
                    for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q")
                ),
                "row_column_d_inputs": max(
                    abs(p_row - p_column), abs(row_d - column_d)
                ),
                "marginal_reconstruction": finite(
                    marginal_error, f"marginal reconstruction q={self.q}"
                ),
                "sharp_sector_QS_minus_QC": float(self.maximum_charge_error),
                "sham_self_covariance": abs(direct_sham - sham),
                "shuffle_expectation": max(abs(shuffle), abs(float(shuffle_identity))),
            },
            "negative_controls": {
                "sham_replacement_D": finite(
                    direct_sham - sham, f"sham replacement q={self.q}"
                ),
                "shuffle_replacement_w": finite(shuffle, f"shuffle replacement q={self.q}"),
            },
        }


def _totals(sectors: Sequence[Mapping[str, object]]) -> dict[str, float]:
    return {
        key: finite(sum(float(item[key]) for item in sectors), f"total {key}")
        for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q")
    }


def finalize_accumulators(accumulators: Sequence[SectorMomentAccumulator]) -> dict[str, object]:
    sectors = [item.finalize() for item in accumulators]
    totals = _totals(sectors)
    column_sectors = [item["column"] for item in sectors]
    column_totals = _totals(column_sectors)
    row_column = max(float(item["residuals"]["row_column"]) for item in sectors)
    row_column = max(
        row_column,
        *(
            abs(totals[key] - column_totals[key])
            for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q")
        ),
    )
    row_column_d_inputs = max(
        float(item["residuals"]["row_column_d_inputs"]) for item in sectors
    )
    row_column_d_inputs = max(
        row_column_d_inputs,
        abs(totals["w_q"] - column_totals["w_q"]),
        abs(totals["w_sham_q"] - column_totals["w_sham_q"]),
        abs(totals["D_q"] - column_totals["D_q"]),
    )
    marginal = max(
        float(item["residuals"]["marginal_reconstruction"]) for item in sectors
    )
    charge = max(
        float(item["residuals"]["sharp_sector_QS_minus_QC"]) for item in sectors
    )
    sham = max(float(item["residuals"]["sham_self_covariance"]) for item in sectors)
    shuffle = max(float(item["residuals"]["shuffle_expectation"]) for item in sectors)
    return {
        "registered": {
            "probability": totals["p_q"],
            "w": totals["w_q"],
            "w_sham": totals["w_sham_q"],
            "D": totals["D_q"],
            "w_shuffle": totals["w_shuffle_q"],
        },
        "row_stream": {
            "totals": {
                "probability": totals["p_q"],
                "w": totals["w_q"],
                "w_sham": totals["w_sham_q"],
                "D": totals["D_q"],
                "w_shuffle": totals["w_shuffle_q"],
            },
            "sectors": {str(q): dict(record["row"]) for q, record in enumerate(sectors)},
        },
        "column_stream": {
            "totals": {
                "probability": column_totals["p_q"],
                "w": column_totals["w_q"],
                "w_sham": column_totals["w_sham_q"],
                "D": column_totals["D_q"],
                "w_shuffle": column_totals["w_shuffle_q"],
            },
            "sectors": {
                str(q): dict(record["column"]) for q, record in enumerate(sectors)
            },
        },
        "q_contributions": {
            str(q): {
                key: float(record[key])
                for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q")
            }
            for q, record in enumerate(sectors)
        },
        "residuals": {
            "row_column_accumulator": row_column,
            "row_column_d_inputs": row_column_d_inputs,
            "probability_normalization": abs(totals["p_q"] - 1.0),
            "state_norm": abs(totals["p_q"] - 1.0),
            "marginal_reconstruction": marginal,
            "sharp_sector_QS_minus_QC": charge,
            "total_content": charge,
            "sham_self_covariance": sham,
            "shuffle_expectation": shuffle,
        },
        "negative_controls": {
            "sham_replacement_D": finite(
                sum(float(item["negative_controls"]["sham_replacement_D"]) for item in sectors),
                "total sham replacement D",
            ),
            "sham_replacement_max_sector_D": sham,
            "shuffle_replacement_w": totals["w_shuffle_q"],
        },
    }


def stream_terminal_children(
    *,
    length: int,
    shards: Sequence[np.ndarray],
    backend: TerminalBackend,
    resolution: object,
    monitor: ResourceMonitor | None = None,
) -> dict[str, object]:
    """Reconstruct and consume the exact two terminal children.

    ``shards[q]`` is H_(L-1),q.  The destination H_L is never materialized.
    Each source-row window is split into the last-lineage-bit 0 and 1 children,
    transported in its exact sharp-q carrier block, and immediately reduced to
    the registered sufficient statistics.
    """
    if length not in (10, 12) and not 2 <= length <= 8:
        raise HeldoutRefusal("terminal stream supports synthetic controls or held-out sizes")
    if backend.length != length or len(shards) != length:
        raise HeldoutRefusal("terminal stream backend/shard census mismatch")
    accumulators = [
        SectorMomentAccumulator(length, q, np.asarray(backend.carrier_words(q)))
        for q in range(length + 1)
    ]
    cosine = math.cos(PHI)
    sine = math.sin(PHI)
    event = length - 1
    maximum_window_bytes = 0
    for old_q, old in enumerate(shards):
        _monitor(monitor, f"terminal-sector-L{length}-q{old_q}")
        expected = (math.comb(length - 1, old_q), math.comb(2 * length, old_q))
        if tuple(old.shape) != expected or old.dtype != np.dtype(np.complex128):
            raise HeldoutRefusal(f"preterminal shard layout mismatch q={old_q}")
        lineages = np.asarray(backend.lineage_words(length - 1, old_q))
        carriers = np.asarray(backend.carrier_words(old_q))
        if len(lineages) != expected[0] or len(carriers) != expected[1]:
            raise HeldoutRefusal(f"preterminal basis census mismatch q={old_q}")
        blank, destination = backend.admission(event, old_q)
        blank = np.asarray(blank, dtype=np.int64)
        destination = np.asarray(destination, dtype=np.int64)
        if len(blank) != len(destination):
            raise HeldoutRefusal(f"admission map census mismatch q={old_q}")
        destination_columns = len(accumulators[old_q + 1].carrier_words)
        if (
            bool(np.any(blank < 0))
            or bool(np.any(blank >= len(carriers)))
            or bool(np.any(destination < 0))
            or bool(np.any(destination >= destination_columns))
            or len(np.unique(blank)) != len(blank)
            or len(np.unique(destination)) != len(destination)
        ):
            raise HeldoutRefusal(f"admission map range/injectivity mismatch q={old_q}")
        expected_blank = np.flatnonzero(((carriers >> event) & 1) == 0).astype(np.int64)
        if not np.array_equal(blank, expected_blank):
            raise HeldoutRefusal(f"admission source map is not canonical q={old_q}")
        destination_words = accumulators[old_q + 1].carrier_words[destination]
        expected_destination_words = carriers[blank] | np.asarray(
            1 << event, dtype=carriers.dtype
        )
        if not np.array_equal(destination_words, expected_destination_words):
            raise HeldoutRefusal(f"admission destination map is not canonical q={old_q}")
        engine_rows = max(
            1,
            min(
                int(backend.batch_rows(len(carriers), resolution)),
                int(backend.batch_rows(destination_columns, resolution)),
            ),
        )
        accumulator_rows = max(
            1,
            TERMINAL_ACCUMULATOR_WINDOW_BYTES
            // max(96, max(len(carriers), destination_columns) * 96),
        )
        rows = min(engine_rows, accumulator_rows)
        for lower in range(0, len(lineages), rows):
            _monitor(
                monitor,
                f"terminal-window-L{length}-q{old_q}-row{lower}",
            )
            upper = min(len(lineages), lower + rows)
            source = np.array(old[lower:upper], copy=True)
            stay = source.copy()
            stay[:, blank] *= cosine
            evolved = backend.evolve(old_q, stay, resolution)
            accumulators[old_q].consume(lineages[lower:upper], evolved)
            maximum_window_bytes = max(
                maximum_window_bytes,
                int(source.nbytes + stay.nbytes + evolved.nbytes),
            )
            if len(blank):
                accepted = np.zeros(
                    (upper - lower, destination_columns), dtype=np.complex128
                )
                accepted[:, destination] = -1.0j * sine * source[:, blank]
                accepted_evolved = backend.evolve(old_q + 1, accepted, resolution)
                full_lineages = lineages[lower:upper].astype(np.uint64, copy=True)
                full_lineages |= np.uint64(1 << event)
                accumulators[old_q + 1].consume(full_lineages, accepted_evolved)
                maximum_window_bytes = max(
                    maximum_window_bytes,
                    int(source.nbytes + accepted.nbytes + accepted_evolved.nbytes),
                )
            _monitor(
                monitor,
                f"terminal-window-complete-L{length}-q{old_q}-row{lower}",
            )
    _monitor(monitor, f"terminal-finalize-L{length}", force=True)
    result = finalize_accumulators(accumulators)
    result["streaming"] = {
        "preterminal_prefix": length - 1,
        "terminal_children_streamed": True,
        "full_terminal_array_allocated": False,
        "maximum_explicit_amplitude_window_bytes": maximum_window_bytes,
    }
    return result


class SyntheticBackend:
    """Small exact backend used only by synthetic tests."""

    def __init__(self, length: int, evolution: Callable[[int, np.ndarray], np.ndarray] | None = None):
        self.length = length
        self._evolution = evolution or (lambda _q, value: value.copy())

    def lineage_words(self, prefix: int, q: int) -> np.ndarray:
        return fixed_words(prefix, q)

    def carrier_words(self, q: int) -> np.ndarray:
        return fixed_words(2 * self.length, q)

    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
        old = self.carrier_words(q)
        new = self.carrier_words(q + 1)
        lookup = {int(word): index for index, word in enumerate(new)}
        blank = np.flatnonzero(((old >> event) & 1) == 0).astype(np.int64)
        destination = np.array(
            [lookup[int(old[index]) | (1 << event)] for index in blank], dtype=np.int64
        )
        return blank, destination

    def evolve(self, q: int, amplitudes: np.ndarray, resolution: object) -> np.ndarray:
        del resolution
        answer = np.asarray(self._evolution(q, amplitudes))
        if answer.shape != amplitudes.shape:
            raise HeldoutRefusal("synthetic evolution changed block shape")
        return answer

    def batch_rows(self, columns: int, resolution: object) -> int:
        del resolution
        return max(1, 1024 // max(1, columns))

    def close(self) -> None:
        return None


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise HeldoutRefusal(f"cannot import frozen dependency: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authenticate_fresh_telemetry(
    telemetry_path: Path,
    *,
    now_epoch_seconds: int,
    root: Path = ROOT,
) -> dict[str, object]:
    """Validate only the shared resource control plane, never hostile arrays/results."""
    authenticate_heldout_protocol(root)
    gate = strict_json(root / HELDOUT_GATE_RELATIVE_PATH, HELDOUT_GATE_SHA256)
    telemetry = strict_json(telemetry_path)
    validator = _load_module(
        "heldout_resource_telemetry_validator",
        root / HELDOUT_GATE_VALIDATOR_RELATIVE_PATH,
    )
    try:
        schedule = validator.validate_telemetry(
            telemetry, gate["resource_gate"], int(now_epoch_seconds)
        )
    except Exception as error:
        raise HeldoutRefusal(f"fresh held-out resource telemetry failed: {error}") from error
    return {
        "selected_schedule": str(schedule),
        "target_scratch_root": str(telemetry["target_scratch_root"]),
        "target_output_path": str(telemetry["target_output_path"]),
        "captured_epoch_seconds": int(telemetry["captured_epoch_seconds"]),
    }


def require_execution_authorization(authorization: str | None) -> None:
    if authorization != EXECUTION_AUTHORIZATION:
        raise HeldoutRefusal("exact target held-out execution authorization is absent")


def _load_v012_validator(root: Path) -> tuple[ModuleType, bool]:
    module_name = "production_obligation_validators"
    validator_path = (root / TARGET_V012_VALIDATORS_RELATIVE_PATH).resolve()
    existing = sys.modules.get(module_name)
    inserted = False
    if existing is None:
        source_dir = str(validator_path.parent)
        sys.path.insert(0, source_dir)
        try:
            existing = importlib.import_module(module_name)
            inserted = True
        finally:
            if sys.path and sys.path[0] == source_dir:
                sys.path.pop(0)
    if Path(getattr(existing, "__file__", "")).resolve() != validator_path:
        if inserted and sys.modules.get(module_name) is existing:
            sys.modules.pop(module_name, None)
        raise HeldoutRefusal("V012 production validator import authority drift")
    if sha256_file(validator_path) != TARGET_V012_VALIDATORS_SHA256:
        if inserted and sys.modules.get(module_name) is existing:
            sys.modules.pop(module_name, None)
        raise HeldoutRefusal("V012 production validator source drift")
    return existing, inserted


class _V012AuditorProvenanceCorrection:
    """One-leaf, in-memory correction for the authenticated V012 census skew."""

    def __init__(
        self,
        builder: ModuleType,
        *,
        root: Path,
        monitor: ResourceMonitor | None,
    ) -> None:
        self.builder = builder
        self.root = root
        self.validator: ModuleType | None = None
        self.validator_inserted = False
        self.installed = False
        self.original_track: object = None
        self.original_require: object = None
        self.original_validator_sha256: object = None

        authority = authenticate_canonical_final_auditor(root, monitor=monitor)
        if authority.get(CANONICAL_AUDITOR_RELATIVE_PATH) != CANONICAL_AUDITOR_SHA256:
            raise HeldoutRefusal("canonical final-auditor authority is absent")
        freeze = strict_json(
            root / TARGET_V012_FREEZE_RELATIVE_PATH,
            TARGET_V012_FREEZE_SHA256,
            monitor=monitor,
        )
        sealed_dependencies = freeze.get("sealed_dependencies")
        sealed_track = (
            sealed_dependencies.get("v012_production_dag_refinement_sources")
            if isinstance(sealed_dependencies, dict)
            else None
        )
        builder_track = getattr(builder, "TRACK_C_REFINEMENT_SHA256", None)
        if (
            builder_track != V012_STALE_TRACK_C_REFINEMENT_SHA256
            or sealed_track != V012_STALE_TRACK_C_REFINEMENT_SHA256
        ):
            raise HeldoutRefusal(
                "V012 provenance correction refused: drift is not the sole cb1681 leaf"
            )

        validator, inserted = _load_v012_validator(root)
        self.validator = validator
        self.validator_inserted = inserted
        if (
            getattr(validator, "FINAL_AUDITOR_PATH", None)
            != (root / CANONICAL_AUDITOR_RELATIVE_PATH)
            or getattr(validator, "FINAL_AUDITOR_SHA256", None)
            != STALE_V012_AUDITOR_SHA256
        ):
            self._remove_inserted_validator()
            raise HeldoutRefusal(
                "V012 provenance correction refused: validator leaf is not cb1681"
            )

        corrected_track = dict(V012_STALE_TRACK_C_REFINEMENT_SHA256)
        corrected_track[V012_AUDITOR_TRACK_KEY] = CANONICAL_AUDITOR_SHA256
        corrected_freeze = copy.deepcopy(freeze)
        corrected_freeze["sealed_dependencies"][
            "v012_production_dag_refinement_sources"
        ] = dict(corrected_track)

        self.original_track = builder.TRACK_C_REFINEMENT_SHA256
        self.original_require = builder.require_frozen_census
        self.original_validator_sha256 = validator.FINAL_AUDITOR_SHA256
        try:
            builder.TRACK_C_REFINEMENT_SHA256 = corrected_track
            validator.FINAL_AUDITOR_SHA256 = CANONICAL_AUDITOR_SHA256
            if hasattr(validator._final_auditor, "cache_clear"):
                validator._final_auditor.cache_clear()

            def require_compatible_frozen_census() -> dict[str, object]:
                return builder.validate_freeze_document(copy.deepcopy(corrected_freeze))

            builder.require_frozen_census = require_compatible_frozen_census
            self.installed = True
        except BaseException:
            self.restore()
            raise

    def _remove_inserted_validator(self) -> None:
        if (
            self.validator_inserted
            and self.validator is not None
            and sys.modules.get("production_obligation_validators") is self.validator
        ):
            sys.modules.pop("production_obligation_validators", None)
        self.validator_inserted = False

    def restore(self) -> None:
        if self.installed:
            self.builder.TRACK_C_REFINEMENT_SHA256 = self.original_track
            self.builder.require_frozen_census = self.original_require
            assert self.validator is not None
            self.validator.FINAL_AUDITOR_SHA256 = self.original_validator_sha256
            if hasattr(self.validator._final_auditor, "cache_clear"):
                self.validator._final_auditor.cache_clear()
            self.installed = False
        self._remove_inserted_validator()


class ProductionBackend:
    """Read-only adapter over the authenticated V012 target cache."""

    def __init__(
        self,
        length: int,
        root: Path = ROOT,
        monitor: ResourceMonitor | None = None,
    ):
        self.length = length
        self.monitor = monitor
        self.closed = False
        _monitor(monitor, f"backend-init-L{length}", force=True)
        binding = HISTORY_BINDINGS[length]
        consumer_path = root / TARGET_CONSUMER_RELATIVE_PATH
        authenticate_target_transitive_sources(root, monitor=monitor)
        self.auditor_provenance_correction: (
            _V012AuditorProvenanceCorrection | None
        ) = None
        consumer_dir = str(consumer_path.parent)
        sys.path.insert(0, consumer_dir)
        try:
            self.consumer = _load_module(
                f"heldout_target_consumer_L{length}", consumer_path
            )
        finally:
            if sys.path[0] == consumer_dir:
                sys.path.pop(0)
        loaded_paths = {
            TARGET_CONSUMER_RELATIVE_PATH: Path(self.consumer.__file__).resolve(),
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py":
                Path(self.consumer.builder.__file__).resolve(),
            "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py":
                Path(self.consumer.v004.__file__).resolve(),
            "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v002.py":
                Path(self.consumer.v004.v3.__file__).resolve(),
            "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history.py":
                Path(self.consumer.v004.v3.v1.__file__).resolve(),
            "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py":
                Path(self.consumer.v004.sealed.__file__).resolve(),
        }
        for relative, loaded in loaded_paths.items():
            if loaded != (root / relative).resolve():
                raise HeldoutRefusal(f"target module import authority drift: {relative}")
        self.auditor_provenance_correction = _V012AuditorProvenanceCorrection(
            self.consumer.builder,
            root=root,
            monitor=monitor,
        )
        self.original_builder_wall_limit = self.consumer.builder.WALL_LIMIT
        self.original_engine_wall_limit = self.consumer.v004.WALL_LIMIT
        self.original_max_subdivisions = self.consumer.v004.v3.MAX_SUBDIVISIONS
        cache_root = root / TARGET_CACHE_DIR / "CACHE_PAYLOADS_V012" / f"L{length}"
        self.context = None
        try:
            self.context = self.consumer.CacheContext(
                cache_root, length, binding.cache_manifest_sha256
            )
            # Authenticate the frozen cache under its original frozen resource
            # constants.  Only after that succeeds may the separately
            # authorized held-out runtime-capacity profile be installed.
            self.consumer.builder.WALL_LIMIT = 345_600.0
            self.consumer.v004.WALL_LIMIT = 345_600.0
            self.consumer.v004.v3.MAX_SUBDIVISIONS = TARGET_V003_MAX_SUBDIVISIONS
            self.target_coarse = self.consumer.v004.sealed.Resolution(
                "coarse",
                TARGET_V003_COARSE_CHECKPOINTS,
                TARGET_V003_COARSE_QUADRATURE_NODES,
                TARGET_V003_COARSE_TOLERANCE,
            )
            self.target_fine = self.consumer.v004.sealed.Resolution(
                "fine",
                TARGET_V003_FINE_CHECKPOINTS,
                TARGET_V003_FINE_QUADRATURE_NODES,
                TARGET_V003_FINE_TOLERANCE,
            )
        except BaseException:
            if self.context is not None:
                self.context.close()
            self.consumer.builder.WALL_LIMIT = self.original_builder_wall_limit
            self.consumer.v004.WALL_LIMIT = self.original_engine_wall_limit
            self.consumer.v004.v3.MAX_SUBDIVISIONS = self.original_max_subdivisions
            self.auditor_provenance_correction.restore()
            raise
        self.consumer.CACHE = self.context
        self.consumer.PHYSICAL_STARTED = time.monotonic()
        self.consumer.LAST_RESOURCE_CHECK = 0.0
        self.resolutions = {
            "coarse": self.target_coarse,
            "fine": self.target_fine,
        }
        self.solver_summary: dict[str, object] | None = None

    def lineage_words(self, prefix: int, q: int) -> np.ndarray:
        return self.context.lineage_words(prefix, q)

    def carrier_words(self, q: int) -> np.ndarray:
        return self.context.carrier_words(q)

    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
        return self.context.admission(event, q)

    def evolve(self, q: int, amplitudes: np.ndarray, resolution: object) -> np.ndarray:
        _monitor(self.monitor, f"propagate-start-L{self.length}-q{q}")
        sector = self.consumer.CachedSector(
            self.length, q, self.consumer.v004.sealed.graph(self.length)
        )
        try:
            evolved, _current, record = self.consumer.v004.v3.propagate_dispatch(
                self.length, sector, amplitudes, resolution
            )
            if self.solver_summary is None:
                self.solver_summary = self.consumer.v004.v3.empty_solver(resolution)
            self.consumer.v004.v3.update_solver(self.solver_summary, record)
            if record.get("converged") is not True:
                raise HeldoutRefusal(f"terminal propagation did not converge q={q}")
            _monitor(self.monitor, f"propagate-complete-L{self.length}-q{q}")
            return evolved
        finally:
            sector.close()

    def batch_rows(self, columns: int, resolution: object) -> int:
        return int(self.consumer.v004.v3.batch_rows(columns, resolution, False))

    def close(self) -> None:
        if self.closed:
            return
        try:
            self.consumer.CACHE = None
            self.context.close()
        finally:
            self.consumer.builder.WALL_LIMIT = self.original_builder_wall_limit
            self.consumer.v004.WALL_LIMIT = self.original_engine_wall_limit
            self.consumer.v004.v3.MAX_SUBDIVISIONS = self.original_max_subdivisions
            if self.auditor_provenance_correction is not None:
                self.auditor_provenance_correction.restore()
            self.closed = True


def production_preflight(root: Path = ROOT) -> dict[str, object]:
    """Authenticate authority and retained inputs without opening witness values."""
    protocol = authenticate_heldout_protocol(root)
    seed = authenticate_seed_authority(root)
    dependencies = {}
    for relative, expected in (
        (TARGET_CONSUMER_RELATIVE_PATH, TARGET_CONSUMER_SHA256),
        (TARGET_V004_RELATIVE_PATH, TARGET_V004_SHA256),
        (TARGET_V003_REPAIR_RELATIVE_PATH, TARGET_V003_REPAIR_SHA256),
    ):
        actual = sha256_file(root / relative)
        if actual != expected:
            raise HeldoutRefusal(f"frozen dependency drift: {relative}")
        dependencies[relative] = actual
    histories = {
        str(length): authenticate_retained_history(
            length, root=root, verify_payload_hashes=True
        )
        for length in (10, 12)
    }
    return {
        "protocol": protocol,
        "seed": seed,
        "dependencies": dependencies,
        "retained_history": {
            key: {
                "history_path": value.binding.history_relative_path,
                "history_sha256": value.binding.history_sha256,
                "terminal_shard_count": len(value.shards),
                "terminal_payload_bytes": sum(item.byte_count for item in value.shards),
            }
            for key, value in histories.items()
        },
        "physical_witness_values_opened": False,
    }


def _open_generated_shards(
    metadata: Sequence[AuthenticatedShard],
    *,
    monitor: ResourceMonitor | None,
) -> StableOpenHistory:
    opened: list[StableOpenShard] = []
    try:
        for item in metadata:
            descriptor, descriptor_stat = _open_regular_nofollow(
                item.path, require_readonly=False
            )
            try:
                shape, dtype, offset = _npy_header_descriptor(descriptor, item.path)
                if shape != item.shape or dtype != np.dtype(np.complex128):
                    raise HeldoutRefusal(f"generated shard layout mismatch q={item.q}")
                if offset + 16 * math.prod(shape) != item.byte_count:
                    raise HeldoutRefusal(f"generated shard byte mismatch q={item.q}")
                digest = _sha256_descriptor(
                    descriptor,
                    item.byte_count,
                    monitor=monitor,
                    stage=f"authenticate-generated-q{item.q}",
                )
                if digest != item.sha256:
                    raise HeldoutRefusal(f"generated shard digest mismatch q={item.q}")
                _verify_descriptor_path(item.path, descriptor, descriptor_stat)
                mapped = mmap.mmap(descriptor, 0, access=mmap.ACCESS_READ)
                array = np.ndarray(
                    shape,
                    dtype=np.complex128,
                    buffer=mapped,
                    offset=offset,
                    order="C",
                )
                array.flags.writeable = False
                opened.append(
                    StableOpenShard(
                        metadata=item,
                        descriptor=descriptor,
                        opened_stat=descriptor_stat,
                        payload_offset=offset,
                        mapping=mapped,
                        array=array,
                    )
                )
            except BaseException:
                os.close(descriptor)
                raise
        return StableOpenHistory(None, tuple(opened))
    except BaseException:
        for shard in opened:
            shard.close()
        raise


def _run_fine_terminal_from_retained(
    length: int,
    *,
    root: Path = ROOT,
    monitor: ResourceMonitor | None = None,
) -> dict[str, object]:
    """Internal atomic-orchestrator component; never a standalone release."""
    stable = open_authenticated_history(length, root=root, monitor=monitor)
    backend: ProductionBackend | None = None
    try:
        _monitor(monitor, f"fine-allocation-L{length}", force=True)
        backend = ProductionBackend(length, root, monitor=monitor)
        result = stream_terminal_children(
            length=length,
            shards=stable.arrays,
            backend=backend,
            resolution=backend.resolutions["fine"],
            monitor=monitor,
        )
        result["solver"] = dict(backend.solver_summary or {})
        stable.verify(monitor)
        return result
    finally:
        if backend is not None:
            backend.close()
        stable.close()


def _run_coarse_whole_history(
    length: int,
    scratch: Path,
    *,
    root: Path = ROOT,
    monitor: ResourceMonitor | None = None,
) -> dict[str, object]:
    """Regenerate the exact COARSE history, then stream its terminal witness.

    This uses the unchanged V012 cache-backed V004 history engine to create a
    fresh COARSE H_(L-1) under ``scratch`` and then streams both exact terminal
    children through the witness accumulator.  Scratch is preserved for
    post-run custody; this function never deletes it.
    """
    if length not in (10, 12):
        raise HeldoutRefusal(f"unsupported held-out coarse size: {length}")
    # Authenticate the corresponding retained target input before allocating
    # any physical scratch, even though this route regenerates the companion
    # rough history from the frozen blank source.
    authenticate_retained_history(
        length,
        root=root,
        verify_payload_hashes=True,
        monitor=monitor,
    )
    target_parent = scratch.parent.resolve()
    resolved_scratch = scratch.resolve()
    if (
        resolved_scratch.parent != target_parent
        or resolved_scratch.name != f"rough_L{length}"
        or resolved_scratch.exists()
    ):
        raise HeldoutRefusal(
            "coarse scratch must be the absent role/size child "
            f"{target_parent / ('rough_L' + str(length))}"
        )

    _monitor(monitor, f"coarse-allocation-L{length}", force=True)
    backend = ProductionBackend(length, root, monitor=monitor)
    v004 = backend.consumer.v004
    originals = (
        v004.sealed.fixed_words,
        v004.sealed.Sector,
        v004.create_admitted,
        v004.terminal_stream,
    )
    try:
        v004.sealed.fixed_words = backend.consumer.cached_fixed_words
        v004.sealed.Sector = backend.consumer.CachedSector
        v004.create_admitted = backend.consumer.cached_create_admitted
        v004.terminal_stream = backend.consumer.cached_terminal_stream
        history_record = v004.history(
            length,
            backend.resolutions["coarse"],
            resolved_scratch,
            retain_terminal=True,
        )
        _monitor(monitor, f"coarse-history-complete-L{length}", force=True)
    except BaseException:
        backend.close()
        raise
    finally:
        (
            v004.sealed.fixed_words,
            v004.sealed.Sector,
            v004.create_admitted,
            v004.terminal_stream,
        ) = originals

    terminal = history_record.get("terminal_shards")
    if not isinstance(terminal, list) or len(terminal) != length:
        backend.close()
        raise HeldoutRefusal("coarse history did not retain the complete H_(L-1) census")
    stable: StableOpenHistory | None = None
    try:
        metadata: list[AuthenticatedShard] = []
        for q, row in enumerate(terminal):
            if (
                not isinstance(row, dict)
                or set(row) != {"bytes", "path", "q", "sha256", "shape"}
                or row.get("q") != q
            ):
                raise HeldoutRefusal(f"coarse terminal shard record mismatch q={q}")
            path = Path(str(row.get("path")))
            expected = (math.comb(length - 1, q), math.comb(2 * length, q))
            if path.parent != resolved_scratch / f"prefix_{length - 1:02d}":
                raise HeldoutRefusal(f"coarse terminal shard escaped scratch q={q}")
            metadata.append(
                AuthenticatedShard(
                    q=q,
                    path=path,
                    shape=expected,
                    byte_count=int(row["bytes"]),
                    sha256=str(row["sha256"]),
                )
            )
        stable = _open_generated_shards(metadata, monitor=monitor)
        witness = stream_terminal_children(
            length=length,
            shards=stable.arrays,
            backend=backend,
            resolution=backend.resolutions["coarse"],
            monitor=monitor,
        )
        witness["solver"] = dict(backend.solver_summary or {})
        stable.verify(monitor)
        canonical_shards = [
            {
                "bytes": item.byte_count,
                "path": repository_relative(item.path, root),
                "q": item.q,
                "sha256": item.sha256,
                "shape": list(item.shape),
            }
            for item in metadata
        ]
        history_controls = {
            key: history_record[key]
            for key in (
                "dimension",
                "edges",
                "peak_logical_scratch_bytes",
                "preterminal_dimension",
                "rows",
                "terminal_state_retained",
            )
        }
        canonical_json_bytes(history_controls)
        return {
            "history_controls": history_controls,
            "generated_terminal_shards": canonical_shards,
            "generated_terminal_shard_manifest_sha256": canonical_digest(
                canonical_shards
            ),
            "terminal": witness,
            "scratch_preserved": True,
            "scratch_root": repository_relative(resolved_scratch, root),
        }
    finally:
        try:
            if stable is not None:
                stable.close()
        finally:
            backend.close()
        authenticate_retained_history(
            length,
            root=root,
            verify_payload_hashes=True,
            monitor=monitor,
        )


def run_fine_terminal_from_retained(*args: object, **kwargs: object) -> dict[str, object]:
    del args, kwargs
    raise HeldoutRefusal(
        "standalone fine execution is forbidden; use the atomic L10/L12 orchestrator"
    )


def run_coarse_whole_history(*args: object, **kwargs: object) -> dict[str, object]:
    del args, kwargs
    raise HeldoutRefusal(
        "standalone coarse execution is forbidden; use the atomic L10/L12 orchestrator"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--authorization")
    parser.add_argument("--output", type=Path, default=HERE / OUTPUT_NAME)
    args = parser.parse_args()
    if args.preflight_only:
        result = production_preflight(ROOT)
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
        return
    if args.authorization != EXECUTION_AUTHORIZATION:
        parser.error(
            "physical held-out execution is locked; provide the exact frozen authorization"
        )
    # Protocol and both exact target routes are hash-bound.  Physical execution
    # is exposed only through target_production_orchestrator.py so a standalone
    # component cannot create a partial held-out publication surface.
    authenticate_heldout_protocol(ROOT)
    raise HeldoutRefusal(
        "standalone execution is forbidden; use the frozen atomic L10/L12 orchestrator"
    )


if __name__ == "__main__":
    main()
