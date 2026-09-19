#!/usr/bin/env python3
"""Shared, non-physical support for the two independent L14 kernels.

This module locates the preserved predecessor sources, enforces single-threaded
math libraries, canonicalizes NumPy-heavy records, and publishes only immutable
evidence.  It deliberately contains no Hamiltonian or admission formula.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import math
import os
import stat
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, Mapping, Tuple

import numpy as np

from resource_scheduler import (
    MAX_HOSTILE_WORKSPACE_BYTES,
    MAX_TARGET_WORKSPACE_BYTES,
)


THREAD_ENV = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)
TARGET_WORKSET_BYTES = MAX_TARGET_WORKSPACE_BYTES
HOSTILE_WORKSET_BYTES = MAX_HOSTILE_WORKSPACE_BYTES
RETAINED_DISK_FLOOR_BYTES = 750 * 2**30
SCRATCH_DISK_FLOOR_BYTES = 750 * 2**30


class ExactKernelRefusal(RuntimeError):
    """A source, identity, convergence, or persistence gate failed closed."""


def configure_single_thread_math() -> None:
    for name in THREAD_ENV:
        os.environ[name] = "1"


def jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def first_nonfinite_path(value: Any, path: str = "$") -> Tuple[str, float] | None:
    """Locate the first non-finite evidence value without making it publishable."""

    normalized = jsonable(value)
    if isinstance(normalized, float) and not math.isfinite(normalized):
        return path, normalized
    if isinstance(normalized, Mapping):
        for key in sorted(normalized):
            found = first_nonfinite_path(normalized[key], "{}.{}".format(path, key))
            if found is not None:
                return found
    elif isinstance(normalized, list):
        for index, item in enumerate(normalized):
            found = first_nonfinite_path(item, "{}[{}]".format(path, index))
            if found is not None:
                return found
    return None


def canonical_json_bytes(value: Any) -> bytes:
    normalized = jsonable(value)
    nonfinite = first_nonfinite_path(normalized)
    if nonfinite is not None:
        path, number = nonfinite
        raise ExactKernelRefusal(
            "non-finite evidence value at {}: {}".format(path, repr(number))
        )
    return (
        json.dumps(normalized, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(16 * 2**20), b""):
            digest.update(block)
    return digest.hexdigest()


def fsync_directory(path: Path) -> None:
    descriptor = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def immutable_json(path: Path, value: Any) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_json_bytes(value)
    digest = hashlib.sha256(raw).hexdigest()
    if path.exists():
        if not path.is_file() or sha256_file(path) != digest:
            raise ExactKernelRefusal("immutable collision at {}".format(path))
        return digest
    temporary = path.parent / ("." + path.name + ".{}.tmp".format(os.getpid()))
    if temporary.exists():
        temporary.unlink()
    descriptor = os.open(str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o444)
        try:
            os.link(temporary, path)
        except FileExistsError:
            if sha256_file(path) != digest:
                raise ExactKernelRefusal("immutable publication race at {}".format(path))
        fsync_directory(path.parent)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return digest


def artifact(path: Path) -> Dict[str, Any]:
    path = Path(path).resolve()
    if not path.is_file():
        raise ExactKernelRefusal("artifact is absent: {}".format(path))
    return {"path": str(path), "sha256": sha256_file(path), "bytes": path.stat().st_size}


def find_project_root() -> Path:
    candidates = [Path(__file__).resolve()] + list(Path(__file__).resolve().parents)
    for candidate in candidates:
        root = candidate if candidate.is_dir() else candidate.parent
        if (root / "audited-386ee2c").is_dir():
            return root
        if (root / "frozen" / "audited-386ee2c").is_dir():
            return root
    raise ExactKernelRefusal("preserved audited-386ee2c source tree is absent")


def packet_root() -> Path:
    root = find_project_root()
    direct = root / "audited-386ee2c"
    return direct if direct.is_dir() else root / "frozen" / "audited-386ee2c"


def add_source_paths() -> Path:
    packet = packet_root()
    paths = (
        packet / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V002",
        packet / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V003",
        packet / "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001",
        packet / "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001",
        packet / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001",
    )
    for path in paths:
        if not path.is_dir():
            raise ExactKernelRefusal("required frozen source directory is absent: {}".format(path))
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    return packet


def load_frozen() -> Tuple[Any, Any, Any, Any, Any]:
    """Return V003 repair bridge plus the two response engines/classifier."""

    configure_single_thread_math()
    add_source_paths()
    repair = importlib.import_module("repair_kernels")
    target_response = importlib.import_module("compute_phase_screen")
    hostile_response = importlib.import_module("independent_centerline")
    classifier = importlib.import_module("compare_and_classify")
    interval = importlib.import_module("interval_spectrum_driver")
    return repair, target_response, hostile_response, classifier, interval


def read_json(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_safe_root(path: Path, label: str) -> Path:
    path = Path(path).resolve()
    if not path.is_absolute() or path == Path("/"):
        raise ExactKernelRefusal("{} root is unsafe".format(label))
    path.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or not path.is_dir():
        raise ExactKernelRefusal("{} root is not an ordinary directory".format(label))
    return path


def directory_bytes(path: Path, suffix: str | None = None) -> int:
    if not path.exists():
        return 0
    iterator = path.rglob("*" if suffix is None else "*" + suffix)
    return sum(member.stat().st_size for member in iterator if member.is_file())


def chmod_tree_readonly(root: Path) -> None:
    for path in sorted(Path(root).rglob("*"), reverse=True):
        if path.is_symlink():
            raise ExactKernelRefusal("symlink in immutable tree: {}".format(path))
        os.chmod(path, 0o444 if path.is_file() else 0o555)
    os.chmod(root, 0o555)
    fsync_directory(root.parent)


def state_census(root: Path, suffix: str) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(root.glob("*" + suffix)):
        metadata = path.stat()
        if not stat.S_ISREG(metadata.st_mode) or path.is_symlink():
            raise ExactKernelRefusal("state member is not regular: {}".format(path))
        rows.append({"path": path.name, "bytes": metadata.st_size})
    if not rows:
        raise ExactKernelRefusal("state census is empty: {}".format(root))
    return rows


@contextmanager
def one_node_pool_capacity(runtime: Any, branch: str, workers: int) -> Iterator[None]:
    """Admit a declared pool without polling live CPU, RAM, or RSS.

    V003 bounds active numerical work separately with deterministic q-aware
    reservations.  The preserved constructor still asks for a capacity
    callback, so this narrow scope supplies the already-declared process count
    instead of reinterpreting transient host observations as a stop gate.
    """

    original = runtime.recommended_branch_workers

    def recommended(**kwargs: Any) -> int:
        del kwargs
        return workers

    old_target = runtime.TARGET_WORKSET_BYTES
    old_hostile = runtime.HOSTILE_WORKSET_BYTES
    runtime.TARGET_WORKSET_BYTES = TARGET_WORKSET_BYTES
    runtime.HOSTILE_WORKSET_BYTES = HOSTILE_WORKSET_BYTES
    runtime.recommended_branch_workers = recommended
    try:
        yield
    finally:
        runtime.recommended_branch_workers = original
        runtime.TARGET_WORKSET_BYTES = old_target
        runtime.HOSTILE_WORKSET_BYTES = old_hostile


def deadline(context: Mapping[str, Any]) -> float:
    """Return the V003 no-compute-deadline sentinel.

    Wall estimates are telemetry only.  Numerical completion remains governed
    by the unchanged convergence predicates and explicit external stop
    requests, never by an elapsed-time cutoff.
    """

    del context
    return math.inf


def finite_max(rows: list[Mapping[str, Any]], *fields: str) -> float:
    values = [abs(float(row[field])) for row in rows for field in fields]
    if not values or not all(math.isfinite(value) for value in values):
        raise ExactKernelRefusal("non-finite or empty metric reduction")
    return max(values)
