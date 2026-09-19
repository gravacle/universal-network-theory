#!/usr/bin/env python3
"""Construct and publish only the preregistered live A26 record.

This bridge does not launch a worker and does not alter either history engine.
It reconstructs the finite target/hostile comparison from the immutable A23,
A24, A25, and A27 predecessors, then delegates validation and owner-once
publication to the existing independent final auditor and evidence
orchestrator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import mmap
import os
import stat
import sys
import types
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Callable, Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
AUDITOR_DIR: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
)
SOURCE_FREEZE: Final[Path] = HERE / "SOURCE_FREEZE.json"
AUDITOR_SOURCE: Final[Path] = AUDITOR_DIR / "independent_final_auditor.py"
EVIDENCE_SOURCE: Final[Path] = AUDITOR_DIR / "production_evidence_orchestrator.py"
TEST_SOURCE: Final[Path] = HERE / "test_build_final_a26.py"


PUBLISH_TOKEN: Final[str] = "PUBLISH_PREREGISTERED_A26_V001"
TERMINAL_CHUNK_BYTES: Final[int] = 8 * 2**20
MAX_PREDECESSOR_JSON_BYTES: Final[int] = 64 * 2**20
CLAIM_BOUNDARY: Final[str] = (
    "FINITE_L12_TARGET_HOSTILE_ACCUMULATION_ONLY__NO_SPECTRUM_Z1_"
    "CONTINUUM_EMERGENCE_OR_GRAVITY"
)
CHECKS: Final[dict[str, int]] = {
    "postrun_telemetry": 1,
    "complete_l12_histories": 2,
    "terminal_shard_custody": 24,
    "basis_permutation_projections": 24,
    "terminal_numerical_comparisons": 12,
    "native_history_field_projections": 13,
    "transitive_authorization_bindings": 42,
    "independent_auditor_isolation": 1,
}


class BridgeRefusal(RuntimeError):
    """A prerequisite, reconstruction, or publication contract failed."""


def _identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        stat.S_IMODE(metadata.st_mode),
    )


def _parent_identity(metadata: os.stat_result) -> tuple[int, int, int]:
    return metadata.st_dev, metadata.st_ino, stat.S_IFMT(metadata.st_mode)


def valid_sha256(value: object) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _require_unaliased_parents(path: Path, label: str) -> None:
    if not path.is_absolute() or Path(str(path)) != path or "\x00" in str(path):
        raise BridgeRefusal(f"{label} path is not absolute and normalized")
    cursor = Path(path.anchor)
    for component in path.parts[1:-1]:
        cursor /= component
        try:
            metadata = os.stat(cursor, follow_symlinks=False)
        except OSError as error:
            raise BridgeRefusal(f"{label} parent is absent") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise BridgeRefusal(f"{label} parent is aliased or non-directory")


def _sha256_descriptor(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while block := os.pread(descriptor, 16 * 2**20, offset):
        digest.update(block)
        offset += len(block)
    return digest.hexdigest()


def _descriptor_bytes(descriptor: int, size: int, label: str) -> bytes:
    if type(size) is not int or size < 0:
        raise BridgeRefusal(f"{label} size is malformed")
    payload = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(descriptor, min(16 * 2**20, size - offset), offset)
        if not block:
            raise BridgeRefusal(f"{label} descriptor read was short")
        payload.extend(block)
        offset += len(block)
    return bytes(payload)


@dataclass
class RetainedInput:
    path: Path
    label: str
    descriptor: int
    parent_descriptor: int
    identity: tuple[int, ...]
    parent_identity: tuple[int, int, int]
    digest: str
    raw: bytes

    @classmethod
    def open(
        cls, path: Path, expected_sha256: str, label: str,
        *, maximum_bytes: int | None = None,
    ) -> "RetainedInput":
        if not valid_sha256(expected_sha256):
            raise BridgeRefusal(f"{label} expected SHA-256 is malformed")
        _require_unaliased_parents(path, label)
        parent_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        file_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        parent_descriptor = -1
        descriptor = -1
        try:
            parent_descriptor = os.open(path.parent, parent_flags)
            parent_before = os.fstat(parent_descriptor)
            parent_current = os.stat(path.parent, follow_symlinks=False)
            parent_identity = _parent_identity(parent_before)
            if (
                not stat.S_ISDIR(parent_before.st_mode)
                or _parent_identity(parent_current) != parent_identity
            ):
                raise BridgeRefusal(f"{label} parent identity mismatch")
            descriptor = os.open(
                path.name, file_flags, dir_fd=parent_descriptor,
            )
            opened = os.fstat(descriptor)
            current = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
            identity = _identity(opened)
            if (
                not stat.S_ISREG(opened.st_mode) or opened.st_mode & 0o222
                or opened.st_nlink != 1 or _identity(current) != identity
                or (
                    maximum_bytes is not None
                    and opened.st_size > maximum_bytes
                )
            ):
                raise BridgeRefusal(
                    f"{label} is writable, aliased, special, or oversized"
                )
            digest = _sha256_descriptor(descriptor)
            raw = _descriptor_bytes(descriptor, opened.st_size, label)
            if digest != expected_sha256 or hashlib.sha256(raw).hexdigest() != digest:
                raise BridgeRefusal(f"{label} descriptor SHA-256 mismatch")
            retained = cls(
                path, label, descriptor, parent_descriptor, identity,
                parent_identity, digest, raw,
            )
            retained.verify()
            return retained
        except BaseException:
            if descriptor >= 0:
                os.close(descriptor)
            if parent_descriptor >= 0:
                os.close(parent_descriptor)
            raise

    def verify(self) -> None:
        _require_unaliased_parents(self.path, self.label)
        parent_opened = os.fstat(self.parent_descriptor)
        parent_current = os.stat(self.path.parent, follow_symlinks=False)
        opened_before = os.fstat(self.descriptor)
        current_before = os.stat(
            self.path.name, dir_fd=self.parent_descriptor,
            follow_symlinks=False,
        )
        digest = _sha256_descriptor(self.descriptor)
        opened_after = os.fstat(self.descriptor)
        current_after = os.stat(
            self.path.name, dir_fd=self.parent_descriptor,
            follow_symlinks=False,
        )
        if (
            _parent_identity(parent_opened) != self.parent_identity
            or _parent_identity(parent_current) != self.parent_identity
            or _identity(opened_before) != self.identity
            or _identity(current_before) != self.identity
            or _identity(opened_after) != self.identity
            or _identity(current_after) != self.identity
            or opened_before.st_mode & 0o222 or opened_before.st_nlink != 1
            or digest != self.digest
        ):
            raise BridgeRefusal(f"retained input changed: {self.label}")

    def close(self) -> None:
        if self.descriptor >= 0:
            os.close(self.descriptor)
            self.descriptor = -1
        if self.parent_descriptor >= 0:
            os.close(self.parent_descriptor)
            self.parent_descriptor = -1

    def verify_and_close(self) -> None:
        first: BaseException | None = None
        try:
            self.verify()
        except BaseException as error:
            first = error
        finally:
            try:
                self.close()
            except BaseException as error:
                if first is None:
                    first = error
        if first is not None:
            raise first


def _canonical_json_bytes_local(record: object) -> bytes:
    try:
        return (json.dumps(
            record, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise BridgeRefusal("record is not finite canonical JSON") from error


def _strict_json_object(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise BridgeRefusal(f"{label} has a duplicate JSON key")
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise BridgeRefusal(f"{label} has a nonfinite JSON constant")

    try:
        record = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=constant,
        )
    except BridgeRefusal:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise BridgeRefusal(f"{label} JSON is malformed") from error
    if type(record) is not dict or _canonical_json_bytes_local(record) != raw:
        raise BridgeRefusal(f"{label} is not one canonical JSON object")
    return record


def _load_authenticated_module(
    name: str, retained: RetainedInput,
) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__file__ = str(retained.path)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        code = compile(retained.raw, str(retained.path), "exec")
        exec(code, module.__dict__)
    except BaseException:
        if sys.modules.get(name) is module:
            del sys.modules[name]
        raise
    return module


def _authenticate_source_closure() -> tuple[
    object, object, object, tuple[RetainedInput, ...],
]:
    if ROOT.resolve() != ROOT:
        raise BridgeRefusal("repository root is aliased")
    freeze_digest = hashlib.sha256(SOURCE_FREEZE.read_bytes()).hexdigest()
    freeze = RetainedInput.open(
        SOURCE_FREEZE, freeze_digest, "A26 source freeze",
        maximum_bytes=64 * 1024,
    )
    retained_sources: list[RetainedInput] = []
    try:
        record = _strict_json_object(freeze.raw, "A26 source freeze")
        if set(record) != {
            "schema", "status", "files", "canonical_a26_published",
            "claim_boundary",
        }:
            raise BridgeRefusal("A26 source-freeze key census mismatch")
        expected_paths = {
            str(HERE.relative_to(ROOT) / "build_final_a26.py"): Path(__file__).resolve(),
            str(HERE.relative_to(ROOT) / "test_build_final_a26.py"): TEST_SOURCE,
            str(AUDITOR_SOURCE.relative_to(ROOT)): AUDITOR_SOURCE,
            str(EVIDENCE_SOURCE.relative_to(ROOT)): EVIDENCE_SOURCE,
        }
        files = record["files"]
        if type(files) is not dict or set(files) != set(expected_paths):
            raise BridgeRefusal("A26 source-freeze file census mismatch")
        if (
            record["schema"] != "AUDIT_PREPARATION_R_L12_FINAL_A26_SOURCE_FREEZE_V001"
            or record["status"] != "FROZEN_BEFORE_A26_PUBLICATION"
            or record["canonical_a26_published"] is not False
            or record["claim_boundary"]
            != "SOURCE_AND_TEST_CUSTODY_ONLY__NO_A26_PUBLICATION_OR_L12_RESULT"
        ):
            raise BridgeRefusal("A26 source-freeze identity mismatch")
        by_path: dict[Path, RetainedInput] = {}
        for relative, path in expected_paths.items():
            retained = RetainedInput.open(
                path, files[relative], f"A26 frozen source {relative}",
                maximum_bytes=16 * 2**20,
            )
            retained_sources.append(retained)
            by_path[path] = retained
        evidence_module = _load_authenticated_module(
            "production_evidence_orchestrator", by_path[EVIDENCE_SOURCE],
        )
        auditor_module = _load_authenticated_module(
            "independent_final_auditor", by_path[AUDITOR_SOURCE],
        )
        freeze.verify()
        for retained in retained_sources:
            retained.verify()
        return (
            auditor_module.np, auditor_module, evidence_module,
            (freeze, *retained_sources),
        )
    except BaseException:
        for retained in reversed(retained_sources):
            retained.close()
        freeze.close()
        raise


np, auditor, evidence, _SOURCE_GUARD = _authenticate_source_closure()


def verify_frozen_source_closure() -> None:
    for retained in _SOURCE_GUARD:
        retained.verify()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(16 * 2**20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record_sha256(record: object) -> str:
    return hashlib.sha256(evidence.canonical_json_bytes(record)).hexdigest()


def open_canonical_record(
    path: Path, expected_sha256: str, label: str,
) -> tuple[dict[str, object], RetainedInput]:
    retained = RetainedInput.open(
        path, expected_sha256, label,
        maximum_bytes=MAX_PREDECESSOR_JSON_BYTES,
    )
    try:
        record = _strict_json_object(retained.raw, label)
        retained.verify()
        return record, retained
    except BaseException:
        retained.close()
        raise


def read_canonical_record(path: Path, expected_sha256: str) -> dict[str, object]:
    record, retained = open_canonical_record(
        path, expected_sha256, "canonical predecessor",
    )
    try:
        retained.verify()
        return record
    finally:
        retained.verify_and_close()


def _rank_in_reversed_basis(
    width: int, charge: int, target_mask: tuple[int, ...],
) -> int:
    positions = tuple(width - 1 - value for value in reversed(target_mask))
    rank = 0
    previous = -1
    for index, position in enumerate(positions):
        choose = charge - index
        rank += math.comb(width - previous - 1, choose)
        rank -= math.comb(width - position, choose)
        previous = position
    return rank


@lru_cache(maxsize=None)
def basis_permutation(width: int, charge: int) -> np.ndarray:
    if (
        type(width) is not int or type(charge) is not int
        or width < 0 or not 0 <= charge <= width
    ):
        raise BridgeRefusal("basis-permutation parameters are invalid")
    count = math.comb(width, charge)
    result = np.fromiter(
        (
            _rank_in_reversed_basis(width, charge, mask)
            for mask in combinations(range(width), charge)
        ),
        dtype="<u8",
        count=count,
    )
    if (
        len(result) != count
        or (count and (int(result.min()) != 0 or int(result.max()) != count - 1))
        or len(np.unique(result)) != count
    ):
        raise BridgeRefusal("basis permutation is not bijective")
    result.flags.writeable = False
    return result


def basis_permutation_sha256(width: int, charge: int) -> str:
    values = basis_permutation(width, charge)
    digest = hashlib.sha256()
    digest.update(b"V001_LE_U64_TARGET_RANK_TO_HOSTILE_RANK\0")
    digest.update(
        int(width).to_bytes(4, "little")
        + int(charge).to_bytes(4, "little")
        + len(values).to_bytes(8, "little")
    )
    digest.update(values.tobytes(order="C"))
    return digest.hexdigest()


def _finite(value: object, label: str) -> float:
    if type(value) not in (int, float) or not math.isfinite(float(value)):
        raise BridgeRefusal(f"{label} is not a finite JSON number")
    return float(value)


def _projection_linf(left: object, right: object, label: str) -> float:
    if type(left) in (int, float) and type(left) is not bool:
        return abs(_finite(left, label) - _finite(right, label))
    if type(left) in (bool, str):
        if type(right) is not type(left) or right != left:
            raise BridgeRefusal(f"{label} discrete projection mismatch")
        return 0.0
    if type(left) is list:
        if type(right) is not list or len(left) != len(right):
            raise BridgeRefusal(f"{label} list projection mismatch")
        return max(
            (
                _projection_linf(a, b, f"{label}[{index}]")
                for index, (a, b) in enumerate(zip(left, right))
            ),
            default=0.0,
        )
    if type(left) is dict:
        if type(right) is not dict or set(left) != set(right):
            raise BridgeRefusal(f"{label} object projection mismatch")
        return max(
            (
                _projection_linf(left[key], right[key], f"{label}.{key}")
                for key in left
            ),
            default=0.0,
        )
    raise BridgeRefusal(f"{label} has an unsupported projection type")


def history_projection_errors(
    target: dict[str, object], hostile: dict[str, object],
) -> tuple[float, float]:
    target_rows = target.get("rows")
    hostile_rows = hostile.get("rows")
    if (
        type(target_rows) is not list or type(hostile_rows) is not list
        or len(target_rows) != 12 or len(hostile_rows) != 12
    ):
        raise BridgeRefusal("complete L12 event rows are absent")
    row_maximum = 0.0
    prior_retained = 0.0
    for index, (target_row, hostile_row) in enumerate(
        zip(target_rows, hostile_rows), start=1,
    ):
        if type(target_row) is not dict or type(hostile_row) is not dict:
            raise BridgeRefusal("L12 event row is malformed")
        shared = set(target_row) & set(hostile_row) - {
            "actual_solver", "null_solver",
        }
        projection = {key: hostile_row[key] for key in shared}
        projection.update({
            "bandwidth_after": hostile_row["q_genesis_after"],
            "cursor_vertex": hostile_row["input_prefix"],
            "expected_W_from_allow": 0.5 * hostile_row["allow_probability"],
            "lineage_sealed_after": 12.0 - hostile_row["q_genesis_after"],
            "q_genesis_before": 12.0 - prior_retained,
            "q_retained_after_admission": prior_retained + hostile_row["W_n"],
            "q_retained_before": prior_retained,
            "transport_genesis_drift": 0.0,
        })
        target_projection = {
            key: value for key, value in target_row.items()
            if key not in {"actual_solver", "null_solver"}
        }
        row_maximum = max(
            row_maximum,
            _projection_linf(
                target_projection, projection,
                f"target/hostile event {index}",
            ),
        )
        prior_retained = _finite(
            hostile_row["q_retained_after_transport"],
            "hostile retained charge",
        )
    target_comparison = target.get("comparison")
    hostile_comparison = hostile.get("comparison")
    if type(target_comparison) is not dict or type(hostile_comparison) is not dict:
        raise BridgeRefusal("L12 history comparison is absent")
    keys = {
        "admission_acceptance", "connector_ratio", "epsilon", "resolved",
        "routed_acceptance", "sector",
    }
    target_projection = {key: target_comparison[key] for key in keys}
    target_projection["resolution_comparison"] = target_comparison["coarse_fine"]
    hostile_projection = {key: hostile_comparison[key] for key in keys}
    hostile_projection["resolution_comparison"] = hostile_comparison["rough_sharp"]
    return row_maximum, _projection_linf(
        target_projection, hostile_projection, "target/hostile comparison",
    )


def _target_npy_layout(
    descriptor: int, label: str,
) -> tuple[tuple[int, ...], int]:
    try:
        with os.fdopen(os.dup(descriptor), "rb") as stream:
            version = np.lib.format.read_magic(stream)
            if version == (1, 0):
                shape, fortran, dtype = np.lib.format.read_array_header_1_0(
                    stream,
                )
            elif version in ((2, 0), (3, 0)):
                shape, fortran, dtype = np.lib.format.read_array_header_2_0(
                    stream,
                )
            else:
                raise BridgeRefusal(f"{label} NPY version is unsupported")
            offset = stream.tell()
    except (OSError, EOFError, ValueError) as error:
        raise BridgeRefusal(f"{label} NPY header is malformed") from error
    if (
        fortran or np.dtype(dtype) != np.dtype("<c16")
        or type(shape) is not tuple or len(shape) != 2
        or any(type(value) is not int or value <= 0 for value in shape)
    ):
        raise BridgeRefusal(f"{label} NPY layout mismatch")
    return tuple(shape), offset


def terminal_linf(
    target_binding: dict[str, object], hostile_binding: dict[str, object],
    charge: int,
) -> float:
    if type(charge) is not int or not 0 <= charge < 12:
        raise BridgeRefusal("terminal charge is invalid")
    target_path = Path(str(target_binding.get("path")))
    hostile_path = Path(str(hostile_binding.get("path")))
    target_hash = target_binding.get("sha256")
    hostile_hash = hostile_binding.get("sha256")
    if (
        not valid_sha256(target_hash) or not valid_sha256(hostile_hash)
    ):
        raise BridgeRefusal(f"terminal q={charge} custody mismatch")
    expected_shape = tuple(target_binding.get("shape", ()))
    if (
        expected_shape != tuple(hostile_binding.get("shape", ()))
        or len(expected_shape) != 2
        or any(type(value) is not int or value <= 0 for value in expected_shape)
        or type(target_binding.get("bytes")) is not int
        or type(hostile_binding.get("bytes")) is not int
    ):
        raise BridgeRefusal(f"terminal q={charge} shape mismatch")
    target_input = RetainedInput.open(
        target_path, target_hash, f"target terminal q={charge}",
    )
    hostile_input: RetainedInput | None = None
    target_mapping: mmap.mmap | None = None
    hostile_mapping: mmap.mmap | None = None
    try:
        hostile_input = RetainedInput.open(
            hostile_path, hostile_hash, f"hostile terminal q={charge}",
        )
        target_shape, target_offset = _target_npy_layout(
            target_input.descriptor, f"target terminal q={charge}",
        )
        count = math.prod(expected_shape)
        if (
            target_shape != expected_shape or target_offset != 128
            or target_input.identity[2] != target_binding["bytes"]
            or hostile_input.identity[2] != hostile_binding["bytes"]
            or target_binding["bytes"] != target_offset + 16 * count
            or hostile_binding["bytes"] != 16 * count
        ):
            raise BridgeRefusal(f"terminal q={charge} byte/layout mismatch")
        target_mapping = mmap.mmap(
            target_input.descriptor, 0, access=mmap.ACCESS_READ,
        )
        hostile_mapping = mmap.mmap(
            hostile_input.descriptor, 0, access=mmap.ACCESS_READ,
        )
        target = np.ndarray(
            expected_shape, dtype="<c16", buffer=target_mapping,
            offset=target_offset, order="C",
        )
        hostile = np.ndarray(
            expected_shape, dtype="<c16", buffer=hostile_mapping,
            offset=0, order="C",
        )
        lineage = basis_permutation(11, charge)
        carrier = basis_permutation(24, charge)
        rows, columns = expected_shape
        if len(lineage) != rows or len(carrier) != columns:
            raise BridgeRefusal(f"terminal q={charge} permutation census mismatch")
        chunk_columns = max(1, TERMINAL_CHUNK_BYTES // 16)
        maximum = 0.0
        for target_row in range(rows):
            hostile_row = int(lineage[target_row])
            for start in range(0, columns, chunk_columns):
                stop = min(columns, start + chunk_columns)
                left = np.asarray(target[target_row, start:stop])
                right = np.asarray(
                    hostile[hostile_row, carrier[start:stop]],
                )
                if (
                    not np.all(np.isfinite(left.real))
                    or not np.all(np.isfinite(left.imag))
                    or not np.all(np.isfinite(right.real))
                    or not np.all(np.isfinite(right.imag))
                ):
                    raise BridgeRefusal(f"terminal q={charge} is nonfinite")
                if len(left):
                    maximum = max(
                        maximum, float(np.max(np.abs(left - right))),
                    )
        del right
        del left
        del hostile
        del target
        target_input.verify()
        hostile_input.verify()
        return maximum
    finally:
        if hostile_mapping is not None:
            hostile_mapping.close()
        if target_mapping is not None:
            target_mapping.close()
        try:
            target_input.verify_and_close()
        finally:
            if hostile_input is not None:
                hostile_input.verify_and_close()


def build_a17_binding(repo_root: Path) -> dict[str, object]:
    sources: list[dict[str, object]] = []
    branch: dict[str, object] = {"role": "hostile_v004r4"}
    for label in auditor.A17_SOURCE_LABELS:
        path = repo_root / auditor.A17_CANONICAL_RELATIVE_PATHS[label]
        if not path.is_file():
            raise BridgeRefusal(f"A17 source is absent: {label}")
        digest = sha256_file(path)
        source = {"label": label, "path": str(path), "sha256": digest}
        sources.append(source)
        binding: dict[str, object] = {"path": str(path), "sha256": digest}
        if label in auditor.A17_RECORD_IDENTITIES:
            schema, identity_field, identity_value = (
                auditor.A17_RECORD_IDENTITIES[label]
            )
            binding.update({
                "schema": schema,
                "identity_field": identity_field,
                "identity_value": identity_value,
            })
        branch[label] = binding
    return {
        "artifact_id": "A17_HOSTILE_L12_ELIGIBILITY",
        "instance": 1,
        "sources": sources,
        "sha256": record_sha256(branch),
    }


def build_authority_bindings(repo_root: Path = ROOT) -> list[dict[str, object]]:
    bindings: list[dict[str, object]] = []
    for artifact_id, count in auditor.AUTHORITY_INSTANCE_CENSUS.items():
        for instance in range(1, count + 1):
            if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY":
                bindings.append(build_a17_binding(repo_root))
                continue
            relative = auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[
                (artifact_id, instance)
            ]
            path = repo_root / relative
            if not path.is_file():
                raise BridgeRefusal(
                    f"authority predecessor is absent: {artifact_id}:{instance}"
                )
            bindings.append({
                "artifact_id": artifact_id,
                "instance": instance,
                "path": str(path),
                "sha256": sha256_file(path),
            })
    if len(bindings) != 42:
        raise BridgeRefusal("authority binding census is not 42")
    return bindings


def construct_a26_record(
    target: dict[str, object],
    hostile: dict[str, object],
    authority_bindings: list[dict[str, object]],
    *,
    terminal_errors: list[float] | None = None,
    projection_errors: tuple[float, float] | None = None,
    permutation_hash: Callable[[int, int], str] = basis_permutation_sha256,
) -> dict[str, object]:
    if len(authority_bindings) != 42:
        raise BridgeRefusal("A26 requires exactly 42 authority bindings")
    if projection_errors is None:
        projection_errors = history_projection_errors(target, hostile)
    row_error, comparison_error = (
        _finite(projection_errors[0], "row projection error"),
        _finite(projection_errors[1], "comparison projection error"),
    )
    target_shards = target.get("terminal_shards")
    hostile_shards = hostile.get("terminal_shards")
    if (
        type(target_shards) is not list or type(hostile_shards) is not list
        or len(target_shards) != 12 or len(hostile_shards) != 12
    ):
        raise BridgeRefusal("complete 12-shard terminal census is absent")
    if terminal_errors is None:
        terminal_errors = [
            terminal_linf(target_shards[q], hostile_shards[q], q)
            for q in range(12)
        ]
    if len(terminal_errors) != 12:
        raise BridgeRefusal("terminal-error census is not 12")
    normalized_errors = [
        _finite(value, f"terminal q={q} error")
        for q, value in enumerate(terminal_errors)
    ]
    total = sum(CHECKS.values())
    if total != 119:
        raise BridgeRefusal("preregistered A26 check census drifted")
    return {
        "schema": "TARGET_V012_HOSTILE_V004R4_FINAL_L12_AUDIT_V001",
        "classification": "PASS_FINITE_L12_TARGET_HOSTILE_ACCUMULATION",
        "auditor_role": "INDEPENDENT_FINAL_L12_AUDITOR",
        "authority_bindings": authority_bindings,
        "comparison_policy": {
            "target_basis": "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER",
            "hostile_basis": "REVERSED_COMBINATION__FULL_MASK",
            "projection": "TARGET_RANK_TO_HOSTILE_RANK_ON_LINEAGE_AND_CARRIER_AXES",
            "permutation_serialization": "V001_TAGGED_LE_U64_TARGET_RANK_TO_HOSTILE_RANK",
            "tolerance": 1.0e-8,
            "nonfinite_refusal": True,
        },
        "history_projection": {
            "mapping": "NATIVE_HOSTILE_V004R3_TO_TARGET_PHYSICAL_FIELDS_V001",
            "row_linf_abs_error": row_error,
            "comparison_linf_abs_error": comparison_error,
            "tolerance": 1.0e-8,
        },
        "terminal_comparisons": [
            {
                "q": q,
                "target_sha256": target_shards[q]["sha256"],
                "hostile_sha256": hostile_shards[q]["sha256"],
                "lineage_target_to_hostile_permutation_sha256": (
                    permutation_hash(11, q)
                ),
                "carrier_target_to_hostile_permutation_sha256": (
                    permutation_hash(24, q)
                ),
                "linf_abs_error": normalized_errors[q],
            }
            for q in range(12)
        ],
        "checks": dict(CHECKS),
        "checks_total": total,
        "checks_passed": total,
        "failures": [],
        "authority_records_authenticated": 42,
        "custody": {
            "immutable_ordinary_file": True,
            "descriptor_authenticated": True,
            "rehash_after_validation": True,
            "atomically_created_once": True,
            "canonical_artifact_created_by_fixture": False,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _binding_digest(
    bindings: list[dict[str, object]], artifact_id: str,
) -> str:
    matches = [
        binding.get("sha256") for binding in bindings
        if binding.get("artifact_id") == artifact_id
        and binding.get("instance") == 1
    ]
    if len(matches) != 1 or not valid_sha256(matches[0]):
        raise BridgeRefusal(f"unique authority binding absent: {artifact_id}")
    return str(matches[0])


def publish_live_a26(explicit_hashes: dict[str, str]) -> str:
    verify_frozen_source_closure()
    output = Path(evidence.CANONICAL_OUTPUT_PATHS["A26_FINAL_L12_AUDIT"])
    if os.path.lexists(output):
        raise BridgeRefusal("canonical A26 output already exists")
    bindings = build_authority_bindings(ROOT)
    for artifact_id in evidence.PREDECESSOR_IDS:
        if explicit_hashes.get(artifact_id) != _binding_digest(
            bindings, artifact_id,
        ):
            raise BridgeRefusal(f"explicit predecessor hash mismatch: {artifact_id}")
    records: dict[str, dict[str, object]] = {}
    raw_inputs: list[RetainedInput] = []
    primary: BaseException | None = None
    try:
        for artifact_id in evidence.PREDECESSOR_IDS:
            record, retained = open_canonical_record(
                Path(evidence.CANONICAL_PREDECESSOR_PATHS[artifact_id]),
                explicit_hashes[artifact_id], artifact_id,
            )
            records[artifact_id] = record
            raw_inputs.append(retained)
        with evidence.FinalEvidenceOrchestrator(
            auditor.validate_artifact,
        ) as orchestrator:
            for artifact_id in evidence.PREDECESSOR_IDS:
                orchestrator.admit(
                    artifact_id,
                    evidence.CANONICAL_PREDECESSOR_PATHS[artifact_id],
                    explicit_hashes[artifact_id],
                )
            for retained in raw_inputs:
                retained.verify()
            verify_frozen_source_closure()
            candidate = construct_a26_record(
                records["A24_TARGET_L12_HISTORY"],
                records["A25_HOSTILE_L12_HISTORY"],
                bindings,
            )
            for retained in raw_inputs:
                retained.verify()
            verify_frozen_source_closure()
            # The independent sink repeats authority, projection, terminal,
            # count, resource, and claim-boundary validation before publication.
            digest = orchestrator.publish_a26(str(output), candidate)
            for retained in raw_inputs:
                retained.verify()
            verify_frozen_source_closure()
            return digest
    except BaseException as error:
        primary = error
        raise
    finally:
        first_close_error: BaseException | None = None
        for retained in raw_inputs:
            try:
                retained.verify_and_close()
            except BaseException as error:
                if first_close_error is None:
                    first_close_error = error
        try:
            verify_frozen_source_closure()
        except BaseException as error:
            if first_close_error is None:
                first_close_error = error
        if primary is None and first_close_error is not None:
            raise first_close_error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--a23-sha256", required=True)
    parser.add_argument("--a24-sha256", required=True)
    parser.add_argument("--a25-sha256", required=True)
    parser.add_argument("--a27-sha256", required=True)
    args = parser.parse_args()
    if args.authorization != PUBLISH_TOKEN:
        print("REFUSED: literal A26 publication token missing", file=sys.stderr)
        return 2
    explicit = {
        "A23_POSTRUN_TELEMETRY": args.a23_sha256,
        "A24_TARGET_L12_HISTORY": args.a24_sha256,
        "A25_HOSTILE_L12_HISTORY": args.a25_sha256,
        "A27_MUTATION_LEDGER": args.a27_sha256,
    }
    try:
        digest = publish_live_a26(explicit)
    except (
        BridgeRefusal, auditor.Refusal, evidence.OrchestrationRefusal,
        OSError, ValueError, MemoryError,
    ) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "PASS_FINITE_L12_TARGET_HOSTILE_ACCUMULATION",
        "checks": "119/119",
        "sha256": digest,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
