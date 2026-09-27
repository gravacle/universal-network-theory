#!/usr/bin/env python3
"""Blind independent algebra and custody controls for lineage-response scaling.

This packet deliberately has no dependency on the corresponding DEVELOPMENT
scaling lane.  It binds the pre-existing hostile V002 prefix engine, represents
the post-checkpoint revisit as compact Schmidt/SVD data, and reduces the two
arms to a signed low-rank carrier density.  The production entry points are
library functions only; the command line performs custody checks and synthetic
self-tests, never an L6 or L8 scientific execution.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterable, Mapping, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FORBIDDEN_TARGET_COMPONENT = (
    "DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V001"
)
FREEZE = HERE / "AUDIT_SOURCE_INPUT_FREEZE_V001.json"
HASH_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
ANGLE = math.pi / 4.0
DEFAULT_RELATIVE_CUTOFF = 128.0 * np.finfo(np.float64).eps
DEFAULT_ABSOLUTE_TOLERANCE = 1.0e-13

# These are hard-coded independently of the packet freeze so changing both an
# upstream file and the JSON census cannot silently retarget the audit.
PINNED_HOSTILE_V002 = {
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history.py":
        "6ea113e5bb25f1c4b00c2ee186b253ce5eb0551773f90e25bdbb52ed1c636af5",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py":
        "e6b1be915a4d490939799e79efc017ab4e3808f1beeb3d984448b2508fb0522b",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V002_LOW_MEMORY_SUPPLEMENT.md":
        "d88c2e08eb518f28baabe23f8c150012d06047e2a5880216c3be9d7e0a98a1f7",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V002.json":
        "80f265a8d2c51f0df06a95871e9c6e62714284348cfeda477dd2573e1cbe317c",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CONTROL_GATE_V002.json":
        "fa398fd376c5ed3997fb85e838f6911c1640b3bcb599c79163471c2fff954ef4",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CONTROL_HISTORY_L4_V002.json":
        "771fb104419a77e023e76c5636b2a7fb5a3ab4e9ea6eb73d3b6790ec29c7f643",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CONTROL_HISTORY_L6_V002.json":
        "9c0c6aa806807b2f0927736058e1bcdd92d64c0e2cc06c3a7c227776d6e50435",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CONTROL_HISTORY_L8_V002.json":
        "f0f8aba0e4c2288835a6dac1465bb1be94d29b0997c9ffdfae5eafa6a922dcde",
}

PINNED_DENSE_L4_AUDIT = {
    "AUDIT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/"
    "independent_validate.py":
        "8f2d07667d5b0818c13c0ed425dcdac03a9abd44f75657742f4521a831ec93aa",
    "AUDIT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/"
    "INDEPENDENT_RESULT.json":
        "86316a114201046f87789884c207ebe4d21356d0405475327e7bce455dd0352e",
    "AUDIT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/"
    "MANIFEST.sha256":
        "f0244e08f09a2b7073f489b6b89d43c917dc7c718cacb0e3891b719c60af2c10",
}

LEGACY_ROOTS = (
    Path("/Users/brianmulconrey/PerInfo/where-atoms-come-from/audited-386ee2c"),
    Path("/Users/bgm/PerInfo/where-atoms-come-from/audited-386ee2c"),
)


class AuditFailure(RuntimeError):
    """Fail-closed custody, algebra, checkpoint, or verifier failure."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode(
        "utf-8"
    )


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditFailure(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(data: bytes, label: str) -> Any:
    def reject_constant(value: str) -> None:
        raise AuditFailure(f"non-finite JSON token in {label}: {value}")

    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditFailure(f"invalid canonical JSON input {label}: {error}") from error


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _reject_symlink_path(root: Path, relative: Path) -> None:
    cursor = root
    for component in relative.parts:
        cursor = cursor / component
        if cursor.is_symlink():
            raise AuditFailure(f"symlinked custody component refused: {cursor}")


def resolve_custody_path(
    repo_root: Path,
    provenance_path: str,
    legacy_roots: Sequence[Path] = LEGACY_ROOTS,
) -> Path:
    """Resolve one frozen path without modifying its provenance spelling.

    Relative paths are rooted at ``repo_root``.  Absolute paths are accepted
    only when they lie under the current root or one exact frozen legacy root;
    the suffix is then mapped into the current root.  Traversal, symlinks,
    unknown absolute roots, the blinded target lane, and escapes are refused.
    """

    root = repo_root.resolve(strict=True)
    supplied = Path(provenance_path)
    if FORBIDDEN_TARGET_COMPONENT in supplied.parts:
        raise AuditFailure("blinded DEVELOPMENT scaling lane is forbidden")
    if ".." in supplied.parts:
        raise AuditFailure(f"path traversal refused: {provenance_path}")

    relative: Path | None = None
    if supplied.is_absolute():
        for prefix in (root, *legacy_roots):
            try:
                relative = supplied.relative_to(prefix)
                break
            except ValueError:
                continue
        if relative is None:
            raise AuditFailure(f"unknown absolute custody root: {provenance_path}")
    else:
        relative = supplied
    if not relative.parts or relative == Path("."):
        raise AuditFailure("empty custody path refused")
    if FORBIDDEN_TARGET_COMPONENT in relative.parts:
        raise AuditFailure("blinded DEVELOPMENT scaling lane is forbidden")
    _reject_symlink_path(root, relative)
    candidate = (root / relative).resolve(strict=True)
    if not _within(candidate, root):
        raise AuditFailure(f"custody path escaped repository root: {provenance_path}")
    if not candidate.is_file():
        raise AuditFailure(f"custody path is not a regular file: {provenance_path}")
    return candidate


def authenticate_entry(
    repo_root: Path,
    entry: Mapping[str, Any],
    legacy_roots: Sequence[Path] = LEGACY_ROOTS,
) -> Path:
    try:
        provenance = str(entry["path"])
        expected = str(entry["sha256"])
    except KeyError as error:
        raise AuditFailure(f"incomplete custody descriptor: {error}") from error
    if not HASH_PATTERN.fullmatch(expected):
        raise AuditFailure(f"invalid SHA-256 spelling for {provenance}")
    path = resolve_custody_path(repo_root, provenance, legacy_roots)
    if "size_bytes" in entry and path.stat().st_size != int(entry["size_bytes"]):
        raise AuditFailure(f"byte-count mismatch for {provenance}")
    observed = sha256_file(path)
    if observed != expected:
        raise AuditFailure(f"SHA-256 mismatch for {provenance}: {observed} != {expected}")
    return path


def authenticate_pinned_inputs(repo_root: Path = ROOT) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in {**PINNED_HOSTILE_V002, **PINNED_DENSE_L4_AUDIT}.items():
        path = resolve_custody_path(repo_root, relative)
        actual = sha256_file(path)
        if actual != expected:
            raise AuditFailure(f"pinned input changed: {relative}: {actual} != {expected}")
        observed[relative] = actual
    engine_root = repo_root / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    nested_freeze = strict_json_bytes(
        (engine_root / "FROZEN_MANIFEST_V002.json").read_bytes(),
        "FROZEN_MANIFEST_V002.json",
    )
    if nested_freeze.get("schema") != "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_FREEZE_V002":
        raise AuditFailure("hostile V002 nested freeze schema mismatch")
    if nested_freeze.get("frozen_before_v002_control_output") is not True:
        raise AuditFailure("hostile V002 source was not frozen before control output")
    for section in ("files", "preserved_v001"):
        entries = nested_freeze.get(section)
        if not isinstance(entries, dict):
            raise AuditFailure(f"hostile V002 freeze has no {section} census")
        for relative, expected in entries.items():
            path = engine_root / relative
            if sha256_file(path) != expected:
                raise AuditFailure(f"hostile V002 nested custody mismatch: {relative}")
    gate = strict_json_bytes(
        (engine_root / "CONTROL_GATE_V002.json").read_bytes(),
        "CONTROL_GATE_V002.json",
    )
    if (
        gate.get("schema") != "AUDIT_R_PREFIX_HISTORY_CROSS_CONTROL_GATE_V002"
        or gate.get("classification") != "PASS_PREFIX_HISTORY_CONTROLS_L4_L8_V002"
        or gate.get("checks_passed") != gate.get("checks_total")
        or gate.get("implementation_sha256")
        != PINNED_HOSTILE_V002[
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py"
        ]
    ):
        raise AuditFailure("hostile V002 cross-control credential is not valid")
    for length, expected in ((4, PINNED_HOSTILE_V002[
        "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CONTROL_HISTORY_L4_V002.json"
    ]), (6, PINNED_HOSTILE_V002[
        "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CONTROL_HISTORY_L6_V002.json"
    ]), (8, PINNED_HOSTILE_V002[
        "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CONTROL_HISTORY_L8_V002.json"
    ])):
        if gate.get("controls", {}).get(str(length), {}).get("hostile_output_sha256") != expected:
            raise AuditFailure(f"hostile V002 gate does not bind L{length} control history")
    return observed


def authenticate_history(
    repo_root: Path,
    descriptor: Mapping[str, Any],
    length: int,
    legacy_roots: Sequence[Path] = LEGACY_ROOTS,
) -> dict[str, Any]:
    path = authenticate_entry(repo_root, descriptor, legacy_roots)
    record = strict_json_bytes(path.read_bytes(), str(descriptor["path"]))
    expected = {
        "schema": "INDEPENDENT_PREFIX_LINEAGE_HISTORY_CONTROL_V002",
        "L": length,
        "implementation_sha256": PINNED_HOSTILE_V002[
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py"
        ],
        "methodology_sha256": PINNED_HOSTILE_V002[
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V002_LOW_MEMORY_SUPPLEMENT.md"
        ],
        "claim_boundary": "INDEPENDENT_FINITE_PREFIX_HISTORY_V002_CONTROL_ONLY",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise AuditFailure(f"history {key} mismatch: {record.get(key)!r} != {value!r}")
    comparison = record.get("comparison")
    if not isinstance(comparison, dict) or comparison.get("resolved") is not True:
        raise AuditFailure("hostile V002 history is not internally resolved")
    return record


def load_authenticated_shard_census(
    repo_root: Path,
    census_descriptor: Mapping[str, Any],
    legacy_roots: Sequence[Path] = LEGACY_ROOTS,
) -> tuple[dict[str, Any], list[np.ndarray]]:
    """Authenticate a future sharp preterminal q-shard census and payloads."""

    census_path = authenticate_entry(repo_root, census_descriptor, legacy_roots)
    census = strict_json_bytes(census_path.read_bytes(), str(census_descriptor["path"]))
    if census.get("schema") != "AUDIT_LINEAGE_RESPONSE_PRETERMINAL_SHARD_CENSUS_V001":
        raise AuditFailure("unexpected preterminal shard census schema")
    length = int(census.get("L", -1))
    prefix = int(census.get("prefix", -1))
    if length not in (4, 6, 8) or prefix != length - 1:
        raise AuditFailure("shard census length/prefix mismatch")
    if census.get("accuracy") != "sharp":
        raise AuditFailure("only sharp hostile checkpoints are admissible")
    if census.get("engine_sha256") != PINNED_HOSTILE_V002[
        "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py"
    ]:
        raise AuditFailure("shard census does not bind the hostile V002 wrapper")
    authenticate_history(repo_root, census["history"], length, legacy_roots)

    descriptors = census.get("shards")
    if not isinstance(descriptors, list):
        raise AuditFailure("shard census has no ordered shard list")
    q_values = [int(item.get("q", -1)) for item in descriptors]
    if q_values != list(range(prefix + 1)):
        raise AuditFailure("shard q census is not complete and ordered")
    arrays: list[np.ndarray] = []
    for q, descriptor in zip(q_values, descriptors):
        path = authenticate_entry(repo_root, descriptor, legacy_roots)
        expected_shape = (math.comb(prefix, q), math.comb(2 * length, q))
        shape = tuple(int(value) for value in descriptor.get("shape", ()))
        if shape != expected_shape:
            raise AuditFailure(f"declared q={q} shape is not canonical: {shape}")
        expected_dtype = np.dtype(descriptor.get("dtype", ""))
        if expected_dtype.str not in ("<c16", "=c16"):
            raise AuditFailure(f"q={q} shard dtype must be complex128")
        try:
            array = np.load(path, mmap_mode="r", allow_pickle=False)
        except Exception as error:  # numpy raises several header-specific types
            raise AuditFailure(f"invalid q={q} NumPy shard: {error}") from error
        if array.shape != expected_shape or array.dtype != np.dtype(np.complex128):
            raise AuditFailure(f"q={q} shard header differs from census")
        if not bool(np.all(np.isfinite(array))):
            raise AuditFailure(f"q={q} shard contains non-finite amplitudes")
        arrays.append(array)
    return census, arrays


def checkpoint_identity_payload(
    census: Mapping[str, Any], source_freeze_sha256: str, stage: str
) -> dict[str, Any]:
    if not HASH_PATTERN.fullmatch(source_freeze_sha256):
        raise AuditFailure("invalid source-freeze hash")
    if stage not in {
        "PRETERMINAL_SHARP",
        "TERMINAL_OWNER_ONCE",
        "REVISIT_AFTER_ADMISSION",
        "REVISIT_AFTER_TRANSPORT",
    }:
        raise AuditFailure(f"unknown checkpoint stage: {stage}")
    shards = census.get("shards")
    if not isinstance(shards, list):
        raise AuditFailure("identity census has no shards")
    normalized = []
    for item in shards:
        normalized.append({
            "q": int(item["q"]),
            "sha256": str(item["sha256"]),
            "size_bytes": int(item["size_bytes"]),
            "shape": [int(value) for value in item["shape"]],
            "dtype": np.dtype(item["dtype"]).str,
        })
    return {
        "schema": "AUDIT_LINEAGE_RESPONSE_CHECKPOINT_IDENTITY_V001",
        "stage": stage,
        "L": int(census["L"]),
        "prefix": int(census["prefix"]),
        "accuracy": str(census["accuracy"]),
        "engine_sha256": str(census["engine_sha256"]),
        "history_sha256": str(census["history"]["sha256"]),
        "source_freeze_sha256": source_freeze_sha256,
        "shards": normalized,
    }


def checkpoint_identity(
    census: Mapping[str, Any], source_freeze_sha256: str, stage: str
) -> str:
    return canonical_json_sha256(checkpoint_identity_payload(census, source_freeze_sha256, stage))


def verify_checkpoint_receipt(
    receipt: Mapping[str, Any],
    census: Mapping[str, Any],
    source_freeze_sha256: str,
) -> None:
    if receipt.get("schema") != "AUDIT_LINEAGE_RESPONSE_CHECKPOINT_RECEIPT_V001":
        raise AuditFailure("checkpoint receipt schema mismatch")
    stage = str(receipt.get("stage"))
    expected = checkpoint_identity(census, source_freeze_sha256, stage)
    if receipt.get("checkpoint_identity_sha256") != expected:
        raise AuditFailure("checkpoint receipt identity mismatch")
    if receipt.get("complete") is not True:
        raise AuditFailure("checkpoint receipt is not complete")
    if receipt.get("unblinded_to_target") is not False:
        raise AuditFailure("checkpoint receipt violates target blindness")


def atomic_create(path: Path, payload: bytes) -> str:
    """Create one custody file atomically, refusing any overwrite."""

    if path.exists() or path.is_symlink():
        raise AuditFailure(f"refusing to overwrite custody path: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            # A hard-link publication is atomic and, unlike replace(), cannot
            # overwrite a path that appears after the initial check.
            os.link(temporary, path)
        except FileExistsError as error:
            raise AuditFailure(f"custody path appeared during create: {path}") from error
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()
    observed = sha256_file(path)
    expected = hashlib.sha256(payload).hexdigest()
    if observed != expected:
        raise AuditFailure(f"post-publication digest mismatch: {observed} != {expected}")
    return observed


def fixed_weight_words(width: int, weight: int) -> np.ndarray:
    if weight < 0 or weight > width:
        return np.empty(0, dtype=np.uint32 if width <= 32 else np.uint64)
    dtype = np.uint32 if width <= 32 else np.uint64
    values = np.empty(math.comb(width, weight), dtype=dtype)
    for index, positions in enumerate(itertools.combinations(reversed(range(width)), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        values[index] = word
    return values


def _finite(array: np.ndarray, label: str) -> None:
    if not bool(np.all(np.isfinite(array))):
        raise AuditFailure(f"non-finite array in {label}")


@dataclass(frozen=True)
class CompactAmplitude:
    """Canonical thin SVD ``U diag(s) V^H`` for one pure amplitude matrix."""

    left: np.ndarray
    singular: np.ndarray
    right: np.ndarray
    shape: tuple[int, int]
    discarded_frobenius: float = 0.0

    def __post_init__(self) -> None:
        rows, columns = self.shape
        rank = len(self.singular)
        if self.left.shape != (rows, rank) or self.right.shape != (columns, rank):
            raise AuditFailure("compact amplitude shape/rank mismatch")
        if self.singular.ndim != 1 or np.any(self.singular < 0.0):
            raise AuditFailure("compact singular values are invalid")
        _finite(self.left, "compact left factors")
        _finite(self.singular, "compact singular values")
        _finite(self.right, "compact right factors")

    @property
    def rank(self) -> int:
        return len(self.singular)

    @property
    def norm_squared(self) -> float:
        return float(np.dot(self.singular, self.singular))

    def dense(self) -> np.ndarray:
        return (self.left * self.singular[np.newaxis, :]) @ self.right.conj().T

    def carrier_factors(self) -> np.ndarray:
        # For row-major amplitudes A[s,c], Tr_S |A><A| = A^T A*.
        return self.right.conj() * self.singular[np.newaxis, :]

    @classmethod
    def from_dense(
        cls,
        matrix: np.ndarray,
        relative_cutoff: float = DEFAULT_RELATIVE_CUTOFF,
    ) -> "CompactAmplitude":
        matrix = np.asarray(matrix, dtype=np.complex128)
        if matrix.ndim != 2:
            raise AuditFailure("amplitude matrix must be rank two")
        _finite(matrix, "dense amplitude")
        if not np.any(matrix):
            return cls(
                np.zeros((matrix.shape[0], 0), dtype=np.complex128),
                np.zeros(0, dtype=np.float64),
                np.zeros((matrix.shape[1], 0), dtype=np.complex128),
                matrix.shape,
            )
        left, singular, right_h = np.linalg.svd(matrix, full_matrices=False)
        threshold = relative_cutoff * max(matrix.shape) * float(singular[0])
        keep = singular > threshold
        discarded = float(np.linalg.norm(singular[~keep]))
        return cls(left[:, keep], singular[keep], right_h.conj().T[:, keep], matrix.shape, discarded)

    @classmethod
    def from_product_factors(
        cls,
        left_factor: np.ndarray,
        right_factor: np.ndarray,
        shape: tuple[int, int],
        relative_cutoff: float = DEFAULT_RELATIVE_CUTOFF,
    ) -> "CompactAmplitude":
        """Compress ``left_factor @ right_factor^H`` through a small SVD."""

        left_factor = np.asarray(left_factor, dtype=np.complex128)
        right_factor = np.asarray(right_factor, dtype=np.complex128)
        if left_factor.ndim != 2 or right_factor.ndim != 2:
            raise AuditFailure("low-rank factors must be matrices")
        if left_factor.shape[1] != right_factor.shape[1]:
            raise AuditFailure("low-rank factor column mismatch")
        if left_factor.shape[0] != shape[0] or right_factor.shape[0] != shape[1]:
            raise AuditFailure("low-rank factor outer shape mismatch")
        _finite(left_factor, "left product factors")
        _finite(right_factor, "right product factors")
        if left_factor.shape[1] == 0 or not np.any(left_factor) or not np.any(right_factor):
            return cls(
                np.zeros((shape[0], 0), dtype=np.complex128),
                np.zeros(0, dtype=np.float64),
                np.zeros((shape[1], 0), dtype=np.complex128),
                shape,
            )
        q_left, r_left = np.linalg.qr(left_factor, mode="reduced")
        q_right, r_right = np.linalg.qr(right_factor, mode="reduced")
        middle = r_left @ r_right.conj().T
        small_left, singular, small_right_h = np.linalg.svd(middle, full_matrices=False)
        threshold = relative_cutoff * max(shape) * float(singular[0]) if len(singular) else 0.0
        keep = singular > threshold
        discarded = float(np.linalg.norm(singular[~keep]))
        return cls(
            q_left @ small_left[:, keep],
            singular[keep],
            q_right @ small_right_h.conj().T[:, keep],
            shape,
            discarded,
        )


def _sum_compact_terms(
    shape: tuple[int, int],
    terms: Iterable[tuple[complex, np.ndarray, np.ndarray]],
    relative_cutoff: float,
) -> CompactAmplitude:
    left_parts: list[np.ndarray] = []
    right_parts: list[np.ndarray] = []
    for coefficient, left, right in terms:
        if left.shape[1] != right.shape[1]:
            raise AuditFailure("term factor rank mismatch")
        if left.shape[0] != shape[0] or right.shape[0] != shape[1]:
            raise AuditFailure("term factor outer shape mismatch")
        if coefficient != 0.0 and left.shape[1]:
            left_parts.append(coefficient * left)
            right_parts.append(right)
    if not left_parts:
        return CompactAmplitude.from_product_factors(
            np.zeros((shape[0], 0), dtype=np.complex128),
            np.zeros((shape[1], 0), dtype=np.complex128),
            shape,
            relative_cutoff,
        )
    return CompactAmplitude.from_product_factors(
        np.concatenate(left_parts, axis=1),
        np.concatenate(right_parts, axis=1),
        shape,
        relative_cutoff,
    )


def _word_positions(words: np.ndarray) -> dict[int, int]:
    return {int(word): index for index, word in enumerate(words)}


def _project_embed(
    factors: np.ndarray,
    source_words: np.ndarray,
    selected: np.ndarray,
    target_words: np.ndarray,
    transform: Callable[[int], int],
) -> np.ndarray:
    target = np.zeros((len(target_words), factors.shape[1]), dtype=np.complex128)
    positions = _word_positions(target_words)
    rows = np.flatnonzero(selected)
    mapped = np.fromiter(
        (positions[transform(int(source_words[row]))] for row in rows),
        dtype=np.int64,
        count=len(rows),
    )
    target[mapped, :] = factors[rows, :]
    return target


def actual_revisit_branches(
    amplitude: CompactAmplitude,
    lineage_words: np.ndarray,
    carrier_words: np.ndarray,
    length: int,
    q: int,
    event: int,
    relative_cutoff: float = DEFAULT_RELATIVE_CUTOFF,
) -> dict[int, CompactAmplitude]:
    if amplitude.shape != (len(lineage_words), len(carrier_words)):
        raise AuditFailure("amplitude word census mismatch")
    bit = 1 << event
    lineage_one = (lineage_words & bit) != 0
    carrier_one = (carrier_words & bit) != 0
    left = amplitude.left * amplitude.singular[np.newaxis, :]
    right = amplitude.right
    cosine = math.cos(ANGLE)
    sine = math.sin(ANGLE)
    same = _sum_compact_terms(
        amplitude.shape,
        (
            (1.0, left, right),
            (cosine - 1.0, left * (~lineage_one)[:, None], right * (~carrier_one)[:, None]),
            (cosine - 1.0, left * lineage_one[:, None], right * carrier_one[:, None]),
        ),
        relative_cutoff,
    )
    branches = {q: same}
    if q < length:
        out_lineage = fixed_weight_words(length, q + 1)
        out_carrier = fixed_weight_words(2 * length, q + 1)
        up_left = _project_embed(
            left, lineage_words, ~lineage_one, out_lineage, lambda word: word | bit
        )
        up_right = _project_embed(
            right, carrier_words, ~carrier_one, out_carrier, lambda word: word | bit
        )
        branches[q + 1] = CompactAmplitude.from_product_factors(
            -1.0j * sine * up_left,
            up_right,
            (len(out_lineage), len(out_carrier)),
            relative_cutoff,
        )
    if q > 0:
        out_lineage = fixed_weight_words(length, q - 1)
        out_carrier = fixed_weight_words(2 * length, q - 1)
        down_left = _project_embed(
            left, lineage_words, lineage_one, out_lineage, lambda word: word & ~bit
        )
        down_right = _project_embed(
            right, carrier_words, carrier_one, out_carrier, lambda word: word & ~bit
        )
        branches[q - 1] = CompactAmplitude.from_product_factors(
            -1.0j * sine * down_left,
            down_right,
            (len(out_lineage), len(out_carrier)),
            relative_cutoff,
        )
    return branches


def _lineage_bit_reduction(
    amplitude: CompactAmplitude,
    lineage_words: np.ndarray,
    event: int,
) -> np.ndarray:
    bit = 1 << event
    left = amplitude.left * amplitude.singular[np.newaxis, :]
    reduced = np.zeros((2, 2), dtype=np.complex128)
    positions = _word_positions(lineage_words)
    for index, word_value in enumerate(lineage_words):
        word = int(word_value)
        b = 1 if word & bit else 0
        reduced[b, b] += np.vdot(left[index], left[index])
        partner = word ^ bit
        if b == 0 and partner in positions:
            other = positions[partner]
            value = np.dot(left[index], left[other].conj())
            reduced[0, 1] += value
            reduced[1, 0] += value.conjugate()
    return reduced


def product_revisit_carrier_factors(
    amplitude: CompactAmplitude,
    lineage_words: np.ndarray,
    carrier_words: np.ndarray,
    length: int,
    q: int,
    event: int,
    coherence_tolerance: float = DEFAULT_ABSOLUTE_TOLERANCE,
) -> tuple[dict[int, list[np.ndarray]], float]:
    """Carrier factors for the sectorwise matched-product comparator arm."""

    p = amplitude.norm_squared
    if p <= 0.0:
        return {}, 0.0
    reduced_lineage = _lineage_bit_reduction(amplitude, lineage_words, event)
    coherence = float(max(abs(reduced_lineage[0, 1]), abs(reduced_lineage[1, 0])))
    if coherence > coherence_tolerance:
        raise AuditFailure(
            f"fixed-q lineage one-bit coherence is not zero: {coherence}"
        )
    weights = np.real(np.diag(reduced_lineage))
    if np.min(weights) < -coherence_tolerance or abs(float(np.sum(weights)) - p) > max(
        coherence_tolerance, coherence_tolerance * p
    ):
        raise AuditFailure("lineage bit weights fail positivity/normalization")
    weights = np.maximum(weights, 0.0)
    carrier_factor = amplitude.carrier_factors()
    bit = 1 << event
    carrier_one = (carrier_words & bit) != 0
    cosine = math.cos(ANGLE)
    sine = math.sin(ANGLE)
    branches: dict[int, list[np.ndarray]] = {q: []}
    if weights[0] > 0.0:
        scale = np.where(carrier_one, 1.0, cosine)
        branches[q].append(math.sqrt(float(weights[0]) / p) * scale[:, None] * carrier_factor)
        if q < length:
            target_words = fixed_weight_words(2 * length, q + 1)
            embedded = _project_embed(
                carrier_factor,
                carrier_words,
                ~carrier_one,
                target_words,
                lambda word: word | bit,
            )
            branches.setdefault(q + 1, []).append(
                sine * math.sqrt(float(weights[0]) / p) * embedded
            )
    if weights[1] > 0.0:
        scale = np.where(carrier_one, cosine, 1.0)
        branches[q].append(math.sqrt(float(weights[1]) / p) * scale[:, None] * carrier_factor)
        if q > 0:
            target_words = fixed_weight_words(2 * length, q - 1)
            embedded = _project_embed(
                carrier_factor,
                carrier_words,
                carrier_one,
                target_words,
                lambda word: word & ~bit,
            )
            branches.setdefault(q - 1, []).append(
                sine * math.sqrt(float(weights[1]) / p) * embedded
            )
    return branches, coherence


def compress_density_factors(
    factors: np.ndarray,
    relative_cutoff: float = DEFAULT_RELATIVE_CUTOFF,
) -> tuple[np.ndarray, float]:
    factors = np.asarray(factors, dtype=np.complex128)
    if factors.ndim != 2:
        raise AuditFailure("density factor array must be rank two")
    _finite(factors, "density factors")
    if factors.shape[1] == 0 or not np.any(factors):
        return np.zeros((factors.shape[0], 0), dtype=np.complex128), 0.0
    left, singular, _ = np.linalg.svd(factors, full_matrices=False)
    threshold = relative_cutoff * max(factors.shape) * float(singular[0])
    keep = singular > threshold
    discarded_density_trace = float(np.dot(singular[~keep], singular[~keep]))
    return left[:, keep] * singular[keep][None, :], discarded_density_trace


@dataclass(frozen=True)
class SignedCarrierBlock:
    q: int
    words: np.ndarray
    positive: np.ndarray
    negative: np.ndarray
    discarded_trace_bound: float = 0.0

    def __post_init__(self) -> None:
        if self.positive.shape[0] != len(self.words) or self.negative.shape[0] != len(self.words):
            raise AuditFailure("signed carrier factor dimension mismatch")
        _finite(self.positive, "positive carrier factors")
        _finite(self.negative, "negative carrier factors")

    def dense(self) -> np.ndarray:
        return self.positive @ self.positive.conj().T - self.negative @ self.negative.conj().T

    def diagonal(self) -> np.ndarray:
        return np.sum(np.abs(self.positive) ** 2, axis=1) - np.sum(
            np.abs(self.negative) ** 2, axis=1
        )

    def trace(self) -> float:
        return float(np.sum(np.abs(self.positive) ** 2) - np.sum(np.abs(self.negative) ** 2))

    def eigenvalues(self) -> np.ndarray:
        joined = np.concatenate((self.positive, self.negative), axis=1)
        if joined.shape[1] == 0:
            return np.zeros(0, dtype=np.float64)
        q_basis, r_factor = np.linalg.qr(joined, mode="reduced")
        del q_basis
        signs = np.concatenate(
            (np.ones(self.positive.shape[1]), -np.ones(self.negative.shape[1]))
        )
        small = (r_factor * signs[np.newaxis, :]) @ r_factor.conj().T
        hermitian = 0.5 * (small + small.conj().T)
        return np.linalg.eigvalsh(hermitian)

    def trace_distance(self) -> float:
        return 0.5 * float(np.sum(np.abs(self.eigenvalues())))


def build_revisit_signed_blocks(
    checkpoint_blocks: Mapping[int, np.ndarray],
    length: int,
    event: int,
    relative_cutoff: float = DEFAULT_RELATIVE_CUTOFF,
) -> tuple[dict[int, SignedCarrierBlock], dict[str, Any]]:
    if length < 1 or event < 0 or event >= length:
        raise AuditFailure("invalid length/event")
    expected_q = list(range(length + 1))
    if sorted(checkpoint_blocks) != expected_q:
        raise AuditFailure("terminal checkpoint q blocks are incomplete")
    positive: dict[int, list[np.ndarray]] = {q: [] for q in expected_q}
    negative: dict[int, list[np.ndarray]] = {q: [] for q in expected_q}
    checkpoint_norm = 0.0
    maximum_reconstruction = 0.0
    maximum_discarded_amplitude = 0.0
    maximum_lineage_coherence = 0.0
    ranks: dict[str, int] = {}

    for q in expected_q:
        lineage_words = fixed_weight_words(length, q)
        carrier_words = fixed_weight_words(2 * length, q)
        matrix = np.asarray(checkpoint_blocks[q], dtype=np.complex128)
        expected_shape = (len(lineage_words), len(carrier_words))
        if matrix.shape != expected_shape:
            raise AuditFailure(f"q={q} checkpoint shape {matrix.shape} != {expected_shape}")
        _finite(matrix, f"q={q} checkpoint")
        amplitude = CompactAmplitude.from_dense(matrix, relative_cutoff)
        checkpoint_norm += amplitude.norm_squared
        reconstruction = float(np.linalg.norm(matrix - amplitude.dense()))
        maximum_reconstruction = max(maximum_reconstruction, reconstruction)
        maximum_discarded_amplitude = max(
            maximum_discarded_amplitude, amplitude.discarded_frobenius
        )
        ranks[str(q)] = amplitude.rank
        if amplitude.rank == 0:
            continue
        actual = actual_revisit_branches(
            amplitude,
            lineage_words,
            carrier_words,
            length,
            q,
            event,
            relative_cutoff,
        )
        for out_q, branch in actual.items():
            positive[out_q].append(branch.carrier_factors())
            maximum_discarded_amplitude = max(
                maximum_discarded_amplitude, branch.discarded_frobenius
            )
        product, coherence = product_revisit_carrier_factors(
            amplitude, lineage_words, carrier_words, length, q, event
        )
        maximum_lineage_coherence = max(maximum_lineage_coherence, coherence)
        for out_q, factors in product.items():
            negative[out_q].extend(factors)

    blocks: dict[int, SignedCarrierBlock] = {}
    discarded_trace = 0.0
    for q in expected_q:
        rows = math.comb(2 * length, q)
        p_joined = (
            np.concatenate(positive[q], axis=1)
            if positive[q]
            else np.zeros((rows, 0), dtype=np.complex128)
        )
        n_joined = (
            np.concatenate(negative[q], axis=1)
            if negative[q]
            else np.zeros((rows, 0), dtype=np.complex128)
        )
        p_compact, p_discarded = compress_density_factors(p_joined, relative_cutoff)
        n_compact, n_discarded = compress_density_factors(n_joined, relative_cutoff)
        bound = p_discarded + n_discarded
        discarded_trace += bound
        blocks[q] = SignedCarrierBlock(
            q,
            fixed_weight_words(2 * length, q),
            p_compact,
            n_compact,
            bound,
        )
    signed_trace = sum(block.trace() for block in blocks.values())
    diagnostics = {
        "checkpoint_norm": checkpoint_norm,
        "maximum_checkpoint_svd_reconstruction_frobenius": maximum_reconstruction,
        "maximum_discarded_amplitude_frobenius": maximum_discarded_amplitude,
        "maximum_fixed_q_lineage_bit_coherence": maximum_lineage_coherence,
        "signed_trace_after_admission": signed_trace,
        "discarded_density_trace_bound": discarded_trace,
        "checkpoint_schmidt_ranks": ranks,
        "algebra": "COMPACT_SVD_ACTUAL__ANALYTIC_MATCHED_PRODUCT_CHANNEL__SIGNED_CARRIER_FACTORS",
    }
    return blocks, diagnostics


def apply_carrier_unitaries(
    blocks: Mapping[int, SignedCarrierBlock],
    unitaries: Mapping[int, np.ndarray],
    tolerance: float = 1.0e-11,
) -> tuple[dict[int, SignedCarrierBlock], float]:
    output: dict[int, SignedCarrierBlock] = {}
    maximum_unitarity = 0.0
    for q, block in blocks.items():
        unitary = np.asarray(unitaries[q], dtype=np.complex128)
        if unitary.shape != (len(block.words), len(block.words)):
            raise AuditFailure(f"q={q} carrier unitary shape mismatch")
        residual = float(
            np.max(np.abs(unitary.conj().T @ unitary - np.eye(len(block.words))))
        )
        maximum_unitarity = max(maximum_unitarity, residual)
        if residual > tolerance:
            raise AuditFailure(f"q={q} carrier transport is not unitary: {residual}")
        output[q] = SignedCarrierBlock(
            q,
            block.words.copy(),
            unitary @ block.positive,
            unitary @ block.negative,
            block.discarded_trace_bound,
        )
    return output, maximum_unitarity


def summarize_observables(
    blocks: Mapping[int, SignedCarrierBlock], length: int
) -> dict[str, Any]:
    if sorted(blocks) != list(range(length + 1)):
        raise AuditFailure("observable block census is incomplete")
    delta_n = np.zeros(2 * length, dtype=np.float64)
    trace_distance = 0.0
    configuration_tv = 0.0
    sector_traces = []
    per_q: dict[str, Any] = {}
    for q, block in blocks.items():
        diagonal = block.diagonal()
        trace = float(np.sum(diagonal))
        distance = block.trace_distance()
        trace_distance += distance
        configuration_tv += 0.5 * float(np.sum(np.abs(diagonal)))
        sector_traces.append(trace)
        for site in range(2 * length):
            delta_n[site] += float(np.sum(diagonal[((block.words >> site) & 1) != 0]))
        per_q[str(q)] = {
            "signed_trace": trace,
            "trace_distance": distance,
            "positive_rank": block.positive.shape[1],
            "negative_rank": block.negative.shape[1],
            "discarded_trace_bound": block.discarded_trace_bound,
        }
    result = {
        "carrier_trace_distance": trace_distance,
        "carrier_configuration_tv": configuration_tv,
        "carrier_number_sector_tv": 0.5 * float(np.sum(np.abs(sector_traces))),
        "occupation_rms": float(np.sqrt(np.mean(delta_n * delta_n))),
        "delta_n": delta_n.tolist(),
        "delta_n_0": float(delta_n[0]),
        "signed_trace": float(np.sum(sector_traces)),
        "per_q": per_q,
    }
    for value in (
        result["carrier_trace_distance"],
        result["carrier_configuration_tv"],
        result["carrier_number_sector_tv"],
        result["occupation_rms"],
        result["signed_trace"],
    ):
        if not math.isfinite(float(value)):
            raise AuditFailure("non-finite observable")
    return result


@dataclass(frozen=True)
class HostileV002Modules:
    base: ModuleType
    wrapper: ModuleType


def load_pinned_hostile_v002(repo_root: Path = ROOT) -> HostileV002Modules:
    """Load the authenticated hostile engine without searching arbitrary paths."""

    authenticate_pinned_inputs(repo_root)
    directory = repo_root / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    base_path = directory / "independent_prefix_history.py"
    wrapper_path = directory / "independent_prefix_history_v002.py"
    base_name = "_unt_audit_pinned_prefix_base"
    wrapper_name = "_unt_audit_pinned_prefix_v002"
    prior_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        base_spec = importlib.util.spec_from_file_location(base_name, base_path)
        if base_spec is None or base_spec.loader is None:
            raise AuditFailure("cannot construct pinned hostile base module")
        base_module = importlib.util.module_from_spec(base_spec)
        sys.modules[base_name] = base_module
        base_spec.loader.exec_module(base_module)

        prior = sys.modules.get("independent_prefix_history")
        sys.modules["independent_prefix_history"] = base_module
        try:
            wrapper_spec = importlib.util.spec_from_file_location(wrapper_name, wrapper_path)
            if wrapper_spec is None or wrapper_spec.loader is None:
                raise AuditFailure("cannot construct pinned hostile V002 module")
            wrapper_module = importlib.util.module_from_spec(wrapper_spec)
            sys.modules[wrapper_name] = wrapper_module
            wrapper_spec.loader.exec_module(wrapper_module)
        finally:
            if prior is None:
                sys.modules.pop("independent_prefix_history", None)
            else:
                sys.modules["independent_prefix_history"] = prior
    finally:
        sys.dont_write_bytecode = prior_bytecode
    if wrapper_module.base is not base_module:
        raise AuditFailure("hostile wrapper imported an unexpected base module")
    # Close the local time-of-check/time-of-use window.
    authenticate_pinned_inputs(repo_root)
    return HostileV002Modules(base_module, wrapper_module)


def configure_hostile_v002(modules: HostileV002Modules) -> None:
    base = modules.base
    wrapper = modules.wrapper
    base.evolve_batch = wrapper.low_memory_evolve_batch
    base.batch_rows = wrapper.safe_batch_rows
    base.blank_method = wrapper.blank_method
    base.combine_method = wrapper.combine_method


def regenerate_preterminal_sharp_in_memory(
    length: int,
    modules: HostileV002Modules,
) -> tuple[Any, Any, list[dict[str, Any]]]:
    """Future production hook; deliberately not called by this packet's tests."""

    if length not in (4, 6, 8):
        raise AuditFailure("audit scaling sizes are restricted to L4/L6/L8")
    configure_hostile_v002(modules)
    base = modules.base
    basis = base.PrefixBasis(length)
    state = basis.blank()
    methods: list[dict[str, Any]] = []
    for event in range(length - 1):
        state, blocked_error = base.admit_prefix(basis, state, event)
        if blocked_error > DEFAULT_ABSOLUTE_TOLERANCE:
            raise AuditFailure(f"hostile admission blocked-state error: {blocked_error}")
        _, method = base.evolve_state(basis, state, base.SHARP)
        if method.get("converged") is not True:
            raise AuditFailure(f"hostile sharp evolution did not converge at event {event}")
        methods.append(method)
    if state.prefix != length - 1:
        raise AuditFailure("hostile preterminal prefix cursor mismatch")
    return basis, state, methods


def _hostile_evolve_rows(
    modules: HostileV002Modules,
    carrier: Any,
    rows: np.ndarray,
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    if not len(rows):
        return rows.copy(), []
    wrapper = modules.wrapper
    base = modules.base
    batch = min(len(rows), wrapper.safe_batch_rows(rows.shape[1], max(base.SHARP.checkpoints)))
    answer = np.empty_like(rows)
    methods: list[dict[str, Any]] = []
    for lower in range(0, len(rows), batch):
        upper = min(len(rows), lower + batch)
        final, _, method = wrapper.low_memory_evolve_batch(
            carrier, rows[lower:upper].copy(), base.SHARP
        )
        if method.get("converged") is not True:
            raise AuditFailure("hostile terminal sharp batch did not converge")
        answer[lower:upper] = final
        methods.append(method)
    return answer, methods


def materialize_terminal_owner_once_checkpoint(
    length: int,
    modules: HostileV002Modules,
    basis: Any,
    preterminal_state: Any,
) -> tuple[dict[int, np.ndarray], list[dict[str, Any]]]:
    """Complete the last owner-once event with the pinned hostile transport."""

    if preterminal_state.prefix != length - 1:
        raise AuditFailure("terminal materialization requires prefix L-1")
    event = length - 1
    bit = 1 << event
    cosine = math.cos(ANGLE)
    sine = math.sin(ANGLE)
    blocks = {
        q: np.zeros(
            (len(basis.lineages(length, q)), len(basis.carriers[q].words)),
            dtype=np.complex128,
        )
        for q in range(length + 1)
    }
    methods: list[dict[str, Any]] = []
    for q, old in enumerate(preterminal_state.blocks):
        old_lineages = basis.lineages(length - 1, q)
        old_carrier = basis.carriers[q]
        carrier_one = (old_carrier.words & bit) != 0
        same_rows = np.fromiter(
            (basis.lineage_positions(length, q)[int(word)] for word in old_lineages),
            dtype=np.int64,
            count=len(old_lineages),
        )
        same = old.copy()
        same[:, ~carrier_one] *= cosine
        final_same, records = _hostile_evolve_rows(modules, old_carrier, same)
        blocks[q][same_rows, :] = final_same
        methods.extend(records)
        if q >= length:
            continue
        selected = np.flatnonzero(~carrier_one)
        new_carrier = basis.carriers[q + 1]
        new_columns = np.fromiter(
            (new_carrier.position[int(old_carrier.words[column]) | bit] for column in selected),
            dtype=np.int64,
            count=len(selected),
        )
        added_rows = np.fromiter(
            (
                basis.lineage_positions(length, q + 1)[int(word) | bit]
                for word in old_lineages
            ),
            dtype=np.int64,
            count=len(old_lineages),
        )
        child = np.zeros((len(old), len(new_carrier.words)), dtype=np.complex128)
        child[:, new_columns] = -1.0j * sine * old[:, selected]
        final_added, records = _hostile_evolve_rows(modules, new_carrier, child)
        blocks[q + 1][added_rows, :] = final_added
        methods.extend(records)
    norm = sum(float(np.vdot(block, block).real) for block in blocks.values())
    if abs(norm - 1.0) > 1.0e-9:
        raise AuditFailure(f"terminal checkpoint norm failure: {norm}")
    return blocks, methods


def transport_signed_blocks_with_hostile_v002(
    blocks: Mapping[int, SignedCarrierBlock],
    modules: HostileV002Modules,
    length: int,
) -> tuple[dict[int, SignedCarrierBlock], list[dict[str, Any]]]:
    """Apply one common pinned hostile transport to signed carrier factors."""

    configure_hostile_v002(modules)
    basis = modules.base.PrefixBasis(length)
    output: dict[int, SignedCarrierBlock] = {}
    records: list[dict[str, Any]] = []
    for q, block in blocks.items():
        positive_rows, p_records = _hostile_evolve_rows(
            modules, basis.carriers[q], block.positive.T.copy()
        )
        negative_rows, n_records = _hostile_evolve_rows(
            modules, basis.carriers[q], block.negative.T.copy()
        )
        output[q] = SignedCarrierBlock(
            q,
            block.words.copy(),
            positive_rows.T,
            negative_rows.T,
            block.discarded_trace_bound,
        )
        records.extend(p_records)
        records.extend(n_records)
    return output, records


def verify_freeze(repo_root: Path = ROOT) -> dict[str, Any]:
    custody = authenticate_pinned_inputs(repo_root)
    if not FREEZE.exists():
        raise AuditFailure("audit source/input freeze is absent")
    freeze = strict_json_bytes(FREEZE.read_bytes(), str(FREEZE))
    if freeze.get("schema") != "AUDIT_LINEAGE_SCALING_SOURCE_INPUT_FREEZE_V001":
        raise AuditFailure("audit freeze schema mismatch")
    if freeze.get("target_lane_read_or_import_authorized") is not False:
        raise AuditFailure("audit freeze does not preserve target blindness")
    if freeze.get("scientific_execution_authorized") != "SYNTHETIC_ONLY":
        raise AuditFailure("audit freeze exceeds synthetic authorization")
    frozen_inputs = {
        item["path"]: item["sha256"] for item in freeze.get("upstream_inputs", [])
    }
    if frozen_inputs != custody:
        raise AuditFailure("audit freeze upstream census differs from hard-coded pins")
    for item in freeze.get("audit_sources", []):
        path = HERE / item["path"]
        if sha256_file(path) != item["sha256"]:
            raise AuditFailure(f"audit source changed after freeze: {item['path']}")
    return freeze


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-freeze", action="store_true")
    parser.add_argument("--print-pinned-census", action="store_true")
    arguments = parser.parse_args()
    if arguments.verify_freeze:
        record = verify_freeze(ROOT)
        print(json.dumps({
            "schema": record["schema"],
            "freeze_sha256": sha256_file(FREEZE),
            "status": "PASS_AUDIT_SOURCE_INPUT_FREEZE",
        }, sort_keys=True))
    elif arguments.print_pinned_census:
        print(json.dumps(authenticate_pinned_inputs(ROOT), indent=2, sort_keys=True))
    else:
        parser.error("choose a non-production verification action")


if __name__ == "__main__":
    main()
