#!/usr/bin/env python3
"""Independent A06 cache reconstruction and owner-once publisher.

The default CLI is validation-only.  ``--publish`` is the sole path that can
create the canonical A06 record, and it is accepted only after complete
independent reconstruction.  Downstream validators run separately after the
owner-once A06 publication and are never imported here.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import mmap
import os
import stat
import sys
from pathlib import Path
from typing import Final

import numpy as np


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
TARGET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
CACHE_PARENT: Final[Path] = TARGET / "CACHE_PAYLOADS_V012"
FREEZE: Final[Path] = TARGET / "FREEZE.json"
PREFLIGHT: Final[Path] = TARGET / "PREFLIGHT_RESULT_V001.json"
DUAL_GATE: Final[Path] = TARGET / "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json"
PREBUILD_AUDIT: Final[Path] = HERE / "HOSTILE_AUDIT_RESULT_V001.json"
CANONICAL_A06: Final[Path] = HERE / "POSTBUILD_PAYLOAD_AUDIT_V001.json"
SUPPORTED: Final[tuple[int, ...]] = (4, 6, 8, 10, 12)
WORD_DTYPE: Final[np.dtype] = np.dtype("<u4")
OFFSET_DTYPE: Final[np.dtype] = np.dtype("<u8")
INDEX_DTYPE: Final[np.dtype] = np.dtype("<i4")
OVERHEAD_RESERVE: Final[int] = 2**20
MAPPED_CACHE_LIMIT: Final[int] = 512 * 2**20
SCRATCH_LIMIT: Final[int] = 20 * 2**30
BUILDER_RSS_LIMIT: Final[int] = 4 * 2**30
CONSUMER_RSS_LIMIT: Final[int] = 16 * 2**30
WALL_LIMIT: Final[float] = 108_000.0
SCHEMA: Final[str] = "TARGET_V012_POSTBUILD_PAYLOAD_AUDIT_V001"
CLASSIFICATION: Final[str] = "PASS_TARGET_V012_FRESH_STORAGE_CACHE_PAYLOADS"
CLAIM: Final[str] = (
    "POSTBUILD_STORAGE_CACHE_AUDIT_ONLY__NO_PHYSICAL_HISTORY_SPECTRUM_"
    "CONTINUUM_OR_GRAVITY_RESULT"
)
MANIFEST_KEYS: Final[set[str]] = {
    "schema", "status", "L", "basis_order", "lineage_identity",
    "edge_layout", "hamiltonian_exchange_coefficient", "files", "payload",
    "resource_certificates", "builder_sha256", "consumer_sha256",
    "preflight_sha256", "production_obligation_validators_sha256",
    "method_sha256", "freeze_sha256", "dual_obstruction_gate_sha256",
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
    "superseded_v008_cache_manifest_sha256_by_L", "canonical_cache_root",
    "claim_boundary",
}
FREEZE_KEYS: Final[set[str]] = set("""
    cache_payload_created claim_boundary
    current_v004_target_or_hostile_execution_interrupted
    current_v004_workspace_output_or_cache_read_or_modified files
    frozen_before_nonphysical_preflight_output hard_locks obstruction_evidence
    physical_history_executed predecessor_compatibility_custody
    predecessor_v006_obstruction_custody predecessor_v007_obstruction_custody
    predecessor_v008_obstruction_custody predecessor_v009_obstruction_custody
    predecessor_v010_obstruction_custody predecessor_v011_obstruction_custody
    resource_limits schema sealed_dependencies sealed_input_commit status
    storage_census_including_offsets_and_full_masks
""".split())
PREFLIGHT_KEYS: Final[set[str]] = set("""
    L4_differential allocation_census checks claim_boundary classification
    compatibility files mutation_ledger physical_cache_payload_created
    physical_history_executed resource_limits schema
""".split())
PREBUILD_KEYS: Final[set[str]] = set("""
    absence_census audited_files_sha256 audited_freeze_sha256 audited_packet
    auditor_role checks checks_passed checks_total claim_boundary classification
    failures mutation_ledger no_symlinked_inputs payload_or_history_executed
    preflight_result_sha256 schema sealed_input_commit
    v005_v006_v007_v008_v009_v010_v011_bytes_preserved
""".split())
DUAL_KEYS: Final[set[str]] = set("""
    authorized_cache_lengths builder_sha256 claim_boundary classification
    consumer_sha256 freeze_sha256 hostile_v003_sha256 independent_hostile_audit
    method_sha256 obstructions preflight_result_sha256 preflight_sha256
    preserved_workspace_cross_diagnostic_sha256
    preserved_workspace_custody_sha256 runtime_compatibility_obstruction_sha256
    schema superseded_v005_cache_manifest_sha256_by_L
    superseded_v005_dual_gate_sha256
    superseded_v007_cache_manifest_sha256_by_L
    superseded_v007_dual_gate_sha256
    superseded_v008_cache_manifest_sha256_by_L
    superseded_v008_dual_gate_sha256 target_v004_sha256
    v006_hostile_audit_obstruction_sha256
    v007_runtime_compatibility_obstruction_sha256
    v008_postbuild_audit_binding_obstruction_sha256
    v009_hostile_audit_obstruction_sha256
    v010_audit_record_custody_correction_sha256
    v010_hostile_audit_obstruction_sha256
    v011_hostile_audit_obstruction_sha256
""".split())
SUPERSEDED_PROVENANCE_KEYS: Final[tuple[str, ...]] = (
    "superseded_v005_dual_gate_sha256",
    "superseded_v005_cache_manifest_sha256_by_L",
    "superseded_v007_dual_gate_sha256",
    "superseded_v007_cache_manifest_sha256_by_L",
    "superseded_v008_dual_gate_sha256",
    "superseded_v008_cache_manifest_sha256_by_L",
)
A06_KEYS: Final[set[str]] = {
    "schema", "classification", "auditor_role", "audited_packet",
    "sealed_input_commit", "prebuild_hostile_audit_sha256",
    "dual_obstruction_and_compatibility_gate_sha256", "manifest_sha256_by_L",
    "payload_census_by_L", "checks", "checks_passed", "checks_total",
    "failures", "no_symlinked_or_writable_payload_inputs",
    "semantic_cachecontext", "physical_gate_or_history_executed",
    "claim_boundary",
}
CHECKS: Final[dict[str, int]] = {
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
PHYSICAL_ABSENCE_PATHS: Final[tuple[Path, ...]] = (
    TARGET / "PHYSICAL_EXECUTION_GATE_V012.json",
    TARGET / "CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json",
    TARGET / "CACHED_CONTROL_L4_L8_GATE_V012.json",
    TARGET / "L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
    TARGET / "CACHED_L10_GATE_V012.json",
    TARGET / "TARGET_L12_EXECUTION_GATE_V012.json",
    TARGET / "PHYSICAL_OUTPUTS",
    TARGET / "WORKSPACES",
)


class AuditRefusal(RuntimeError):
    """The cache set or publication request failed closed."""


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, indent=2, sort_keys=True, allow_nan=False,
        ) + "\n").encode("utf-8")
    except (TypeError, ValueError, OverflowError) as error:
        raise AuditRefusal("record is not finite canonical JSON") from error


def exact_tree_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(right) is dict:
        return set(left) == set(right) and all(
            exact_tree_equal(left[key], value) for key, value in right.items()
        )
    if type(right) is list:
        return len(left) == len(right) and all(
            exact_tree_equal(a, b) for a, b in zip(left, right)
        )
    return bool(left == right)


def _identity(value: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_nlink, stat.S_IMODE(value.st_mode),
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
            raise AuditRefusal("descriptor read made no progress")
        output.extend(block)
        offset += len(block)
    return bytes(output)


def _strict_json(raw: bytes, label: str) -> dict[str, object]:
    def exact_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AuditRefusal(f"{label} duplicate JSON key")
            result[key] = value
        return result

    def reject_constant(token: str) -> object:
        raise AuditRefusal(f"{label} nonfinite JSON constant: {token}")

    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=exact_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditRefusal(f"{label} malformed JSON") from error
    if type(value) is not dict:
        raise AuditRefusal(f"{label} is not an object")
    return value


def _require_no_symlink_parents(path: Path, label: str) -> None:
    resolved = path.resolve(strict=False)
    if resolved != path:
        raise AuditRefusal(f"{label} path is aliased")
    current = Path(path.anchor)
    for part in path.parts[1:-1]:
        current /= part
        try:
            metadata = os.stat(current, follow_symlinks=False)
        except OSError as error:
            raise AuditRefusal(f"{label} parent absent") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise AuditRefusal(f"{label} parent is symlinked or special")


def stable_bytes(path: Path, label: str) -> tuple[bytes, str]:
    if not path.is_absolute():
        raise AuditRefusal(f"{label} path is not absolute")
    _require_no_symlink_parents(path, label)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise AuditRefusal(f"{label} absent") from error
    try:
        before = os.fstat(descriptor)
        current = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or before.st_mode & 0o222
            or before.st_nlink != 1 or _identity(before) != _identity(current)
        ):
            raise AuditRefusal(f"{label} is not immutable owner-once evidence")
        digest = _descriptor_sha256(descriptor)
        raw = _descriptor_bytes(descriptor, before.st_size)
        after = os.fstat(descriptor)
        current_after = os.stat(path, follow_symlinks=False)
        if (
            _identity(after) != _identity(before)
            or _identity(current_after) != _identity(before)
            or _descriptor_sha256(descriptor) != digest
            or hashlib.sha256(raw).hexdigest() != digest
        ):
            raise AuditRefusal(f"{label} changed during authentication")
        return raw, digest
    finally:
        os.close(descriptor)


def stable_file(path: Path, label: str) -> tuple[dict[str, object], str]:
    raw, digest = stable_bytes(path, label)
    return _strict_json(raw, label), digest


class HeldAuthoritySet:
    """Retain A01--A04 and every source they freeze until publication ends."""

    def __init__(
        self, paths: dict[str, Path] | None = None,
        json_names: set[str] | None = None,
    ) -> None:
        self.paths = paths or {
            "A01": FREEZE,
            "A02": PREFLIGHT,
            "A03": PREBUILD_AUDIT,
            "A04": DUAL_GATE,
            **{
                f"source:{name}": TARGET / name
                for name in (
                    "METHOD.md", "build_target_cache.py",
                    "consume_target_cache.py",
                    "production_obligation_validators.py",
                    "validate_preflight.py",
                )
            },
        }
        self.json_names = json_names if json_names is not None else {
            "A01", "A02", "A03", "A04",
        }
        self.descriptors: dict[str, int] = {}
        self.identities: dict[str, tuple[int, int, int, int, int, int, int]] = {}
        self.hashes: dict[str, str] = {}
        self.raw: dict[str, bytes] = {}
        self.records: dict[str, dict[str, object]] = {}

    def __enter__(self) -> "HeldAuthoritySet":
        self.open_all()
        return self

    def __exit__(self, *_error: object) -> None:
        self.close()

    def close(self) -> None:
        for descriptor in self.descriptors.values():
            try:
                os.close(descriptor)
            except OSError:
                pass
        self.descriptors.clear()

    def open_all(self) -> None:
        if self.descriptors:
            raise AuditRefusal("authority set already open")
        if set(self.paths) != set(self.json_names) | {
            name for name in self.paths if name.startswith("source:")
        } or len(set(self.paths.values())) != len(self.paths):
            raise AuditRefusal("authority descriptor registry mismatch")
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        try:
            for name, path in self.paths.items():
                if not path.is_absolute():
                    raise AuditRefusal(f"{name} authority path is not absolute")
                _require_no_symlink_parents(path, f"{name} authority")
                try:
                    descriptor = os.open(path, flags)
                except OSError as error:
                    raise AuditRefusal(f"{name} authority absent or aliased") from error
                self.descriptors[name] = descriptor
                held = os.fstat(descriptor)
                named = os.stat(path, follow_symlinks=False)
                identity = _identity(held)
                if (
                    not stat.S_ISREG(held.st_mode) or held.st_mode & 0o222
                    or held.st_nlink != 1 or _identity(named) != identity
                ):
                    raise AuditRefusal(
                        f"{name} authority is not immutable owner-once evidence"
                    )
                raw = _descriptor_bytes(descriptor, held.st_size)
                digest = _descriptor_sha256(descriptor)
                if hashlib.sha256(raw).hexdigest() != digest:
                    raise AuditRefusal(f"{name} authority descriptor hash mismatch")
                self.identities[name] = identity
                self.hashes[name] = digest
                self.raw[name] = raw
                if name in self.json_names:
                    self.records[name] = _strict_json(raw, f"{name} authority")
            self.reauthenticate()
        except BaseException:
            self.close()
            raise

    def reauthenticate(self) -> None:
        if set(self.descriptors) != set(self.paths):
            raise AuditRefusal("authority descriptor set is not fully retained")
        for name, path in self.paths.items():
            descriptor = self.descriptors[name]
            try:
                named = os.stat(path, follow_symlinks=False)
            except OSError as error:
                raise AuditRefusal(f"{name} authority path changed") from error
            held = os.fstat(descriptor)
            if (
                _identity(held) != self.identities[name]
                or _identity(named) != self.identities[name]
                or _descriptor_sha256(descriptor) != self.hashes[name]
            ):
                raise AuditRefusal(f"{name} authority descriptor/path drift")


def fixed_words(width: int, weight: int) -> np.ndarray:
    values = np.empty(math.comb(width, weight), dtype=WORD_DTYPE)
    for index, chosen in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for bit in chosen:
            word |= 1 << bit
        values[index] = word
    return values


def graph(length: int) -> list[list[object]]:
    result: list[list[object]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            result.append([
                offset + site, offset + (site + 1) % length,
                f"rail_{rail + 1}",
            ])
    for site in range(length):
        result.append([site, length + (site + 1) % length, "connector"])
    return result


def operator_q_bytes(length: int, q: int) -> int:
    pairs = 3 * length * (math.comb(2 * length - 2, q - 1) if q else 0)
    return 4 * math.comb(2 * length, q) + 8 * pairs + 8 * (3 * length + 1)


def operator_bytes(length: int) -> int:
    return sum(operator_q_bytes(length, q) for q in range(length + 1))


def admission_bytes(length: int) -> int:
    return sum(
        8 * math.comb(2 * length - 1, q)
        for event in range(length) for q in range(event + 1)
    )


def lineage_mask_bytes(length: int) -> int:
    return sum(4 * 2**prefix for prefix in range(length))


def lineage_map_bytes(length: int) -> int:
    return sum(8 * 2**prefix for prefix in range(length - 1))


def payload_bytes(length: int) -> int:
    return (
        operator_bytes(length) + admission_bytes(length)
        + lineage_mask_bytes(length) + lineage_map_bytes(length)
    )


def maximum_state_bytes(length: int) -> int:
    dimensions = [
        sum(
            math.comb(prefix, q) * math.comb(2 * length, q)
            for q in range(prefix + 1)
        )
        for prefix in range(length)
    ]
    return 16 * max(
        dimensions[index] + dimensions[index + 1]
        for index in range(length - 1)
    )


def maximum_state_file_bytes(length: int) -> int:
    return maximum_state_bytes(length) + 128 * (2 * length - 1)


def carrier_word_bytes(length: int, q: int) -> int:
    return 4 * math.comb(2 * length, q)


def admission_pair_bytes(length: int, q: int) -> int:
    return 8 * math.comb(2 * length - 1, q)


def terminal_cache_peak_bytes(length: int) -> int:
    return max(
        operator_q_bytes(length, q + 1) + carrier_word_bytes(length, q)
        + admission_pair_bytes(length, q)
        for q in range(length)
    )


def authentication_cache_peak_bytes(length: int) -> int:
    all_words = sum(carrier_word_bytes(length, q) for q in range(length + 1))
    largest_nonword = max(
        operator_q_bytes(length, q) - carrier_word_bytes(length, q)
        for q in range(length + 1)
    )
    largest_admission = max(
        admission_pair_bytes(length, q) for q in range(length)
    )
    return all_words + largest_nonword + largest_admission


def expected_file_count(length: int) -> int:
    return (
        4 * (length + 1)
        + 2 * sum(event + 1 for event in range(length))
        + sum(prefix + 1 for prefix in range(length))
        + 2 * sum(prefix + 1 for prefix in range(length - 1))
    )


def expected_records(
    length: int,
) -> dict[str, tuple[str, tuple[int, ...], dict[str, object]]]:
    result: dict[str, tuple[str, tuple[int, ...], dict[str, object]]] = {}
    for q in range(length + 1):
        pairs = 3 * length * (
            math.comb(2 * length - 2, q - 1) if q else 0
        )
        result[f"carrier_q_{q:02d}_words.u32"] = (
            WORD_DTYPE.str, (math.comb(2 * length, q),),
            {"kind": "operator", "q": q, "role": "words"},
        )
        result[f"carrier_q_{q:02d}_offsets.u64"] = (
            OFFSET_DTYPE.str, (3 * length + 1,),
            {"kind": "operator", "q": q, "role": "offsets"},
        )
        for role in ("sources", "targets"):
            result[f"carrier_q_{q:02d}_{role}.i32"] = (
                INDEX_DTYPE.str, (pairs,),
                {"kind": "operator", "q": q, "role": role},
            )
    for event in range(length):
        for q in range(event + 1):
            shape = (math.comb(2 * length - 1, q),)
            for role in ("blank", "destination"):
                result[f"admission_n_{event:02d}_q_{q:02d}_{role}.i32"] = (
                    INDEX_DTYPE.str, shape,
                    {"kind": "admission", "event": event, "q": q, "role": role},
                )
    for prefix in range(length):
        for q in range(prefix + 1):
            result[f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32"] = (
                WORD_DTYPE.str, (math.comb(prefix, q),),
                {"kind": "lineage_mask", "prefix": prefix, "q": q, "role": "words"},
            )
    for prefix in range(length - 1):
        for q in range(prefix + 1):
            for role in ("stay", "accepted"):
                result[f"lineage_n_{prefix:02d}_q_{q:02d}_{role}.i32"] = (
                    INDEX_DTYPE.str, (math.comb(prefix, q),),
                    {"kind": "lineage_map", "prefix": prefix, "q": q, "role": role},
                )
    return result


class HeldCacheSet:
    """Retain all five directories, manifests, and 1,100 members."""

    def __init__(self, lengths: tuple[int, ...] = SUPPORTED) -> None:
        if (
            not lengths or len(set(lengths)) != len(lengths)
            or any(type(length) is not int or length not in SUPPORTED for length in lengths)
        ):
            raise AuditRefusal("cache length registry mismatch")
        self.lengths = lengths
        self.directory_fds: dict[int, int] = {}
        self.directory_identities: dict[int, tuple[int, int, int, int, int, int, int]] = {}
        self.manifest_fds: dict[int, int] = {}
        self.manifest_identities: dict[int, tuple[int, int, int, int, int, int, int]] = {}
        self.member_fds: dict[tuple[int, str], int] = {}
        self.member_identities: dict[tuple[int, str], tuple[int, int, int, int, int, int, int]] = {}
        self.member_hashes: dict[tuple[int, str], str] = {}
        self.manifests: dict[int, dict[str, object]] = {}
        self.manifest_hashes: dict[int, str] = {}

    def __enter__(self) -> "HeldCacheSet":
        return self

    def __exit__(self, *_error: object) -> None:
        self.close()

    def close(self) -> None:
        for descriptor in (
            list(self.member_fds.values()) + list(self.manifest_fds.values())
            + list(self.directory_fds.values())
        ):
            try:
                os.close(descriptor)
            except OSError:
                pass
        self.member_fds.clear()
        self.manifest_fds.clear()
        self.directory_fds.clear()

    def _open_member(self, length: int, name: str) -> tuple[int, tuple[int, int, int, int, int, int, int]]:
        if Path(name).name != name or not name or "/" in name or "\x00" in name:
            raise AuditRefusal("cache member name is not one canonical component")
        directory_fd = self.directory_fds[length]
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(name, flags, dir_fd=directory_fd)
        except OSError as error:
            raise AuditRefusal(f"L{length} cache member absent: {name}") from error
        try:
            held = os.fstat(descriptor)
            named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            identity = _identity(held)
            if (
                not stat.S_ISREG(held.st_mode) or held.st_mode & 0o222
                or held.st_nlink != 1 or _identity(named) != identity
            ):
                raise AuditRefusal(f"L{length} member not immutable owner-once: {name}")
            return descriptor, identity
        except BaseException:
            os.close(descriptor)
            raise

    def open_all(self) -> None:
        if self.directory_fds:
            raise AuditRefusal("cache set already open")
        for length in self.lengths:
            path = CACHE_PARENT / f"L{length}"
            _require_no_symlink_parents(path, f"L{length} cache")
            flags = (
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
            )
            try:
                descriptor = os.open(path, flags)
            except OSError as error:
                raise AuditRefusal(f"L{length} cache directory absent") from error
            self.directory_fds[length] = descriptor
            held = os.fstat(descriptor)
            named = os.stat(path, follow_symlinks=False)
            identity = _identity(held)
            if (
                not stat.S_ISDIR(held.st_mode) or held.st_mode & 0o222
                or _identity(named) != identity
            ):
                raise AuditRefusal(f"L{length} cache directory is writable or aliased")
            self.directory_identities[length] = identity
            manifest_fd, manifest_identity = self._open_member(
                length, "CACHE_MANIFEST.json",
            )
            self.manifest_fds[length] = manifest_fd
            self.manifest_identities[length] = manifest_identity
            raw = _descriptor_bytes(manifest_fd, manifest_identity[2])
            digest = _descriptor_sha256(manifest_fd)
            if hashlib.sha256(raw).hexdigest() != digest:
                raise AuditRefusal(f"L{length} manifest descriptor mismatch")
            manifest = _strict_json(raw, f"L{length} manifest")
            self.manifests[length] = manifest
            self.manifest_hashes[length] = digest
            rows = manifest.get("files")
            if type(rows) is not list:
                raise AuditRefusal(f"L{length} manifest file rows absent")
            for row in rows:
                if type(row) is not dict or type(row.get("path")) is not str:
                    raise AuditRefusal(f"L{length} malformed manifest row")
                name = row["path"]
                key = (length, name)
                if key in self.member_fds:
                    raise AuditRefusal(f"L{length} duplicate manifest member")
                member_fd, member_identity = self._open_member(length, name)
                self.member_fds[key] = member_fd
                self.member_identities[key] = member_identity
                self.member_hashes[key] = _descriptor_sha256(member_fd)

    def array(self, length: int, name: str, dtype: np.dtype, shape: tuple[int, ...]) -> tuple[np.ndarray, mmap.mmap | None]:
        descriptor = self.member_fds[(length, name)]
        if math.prod(shape) == 0:
            return np.empty(shape, dtype=dtype), None
        mapping = mmap.mmap(descriptor, 0, access=mmap.ACCESS_READ)
        return np.ndarray(shape, dtype=dtype, buffer=mapping), mapping

    def reauthenticate(self) -> None:
        for length in self.lengths:
            path = CACHE_PARENT / f"L{length}"
            held_dir = os.fstat(self.directory_fds[length])
            named_dir = os.stat(path, follow_symlinks=False)
            if (
                _identity(held_dir) != self.directory_identities[length]
                or _identity(named_dir) != self.directory_identities[length]
            ):
                raise AuditRefusal(f"L{length} cache directory changed")
            actual = os.listdir(self.directory_fds[length])
            expected = {
                "CACHE_MANIFEST.json",
                *[name for item_length, name in self.member_fds if item_length == length],
            }
            if len(actual) != len(expected) or set(actual) != expected:
                raise AuditRefusal(f"L{length} cache directory census changed")
            manifest_fd = self.manifest_fds[length]
            named_manifest = os.stat(
                "CACHE_MANIFEST.json", dir_fd=self.directory_fds[length],
                follow_symlinks=False,
            )
            if (
                _identity(os.fstat(manifest_fd)) != self.manifest_identities[length]
                or _identity(named_manifest) != self.manifest_identities[length]
                or _descriptor_sha256(manifest_fd) != self.manifest_hashes[length]
            ):
                raise AuditRefusal(f"L{length} manifest changed")
        for key, descriptor in self.member_fds.items():
            length, name = key
            named = os.stat(
                name, dir_fd=self.directory_fds[length], follow_symlinks=False,
            )
            if (
                _identity(os.fstat(descriptor)) != self.member_identities[key]
                or _identity(named) != self.member_identities[key]
                or _descriptor_sha256(descriptor) != self.member_hashes[key]
            ):
                raise AuditRefusal(f"L{length} cache member changed: {name}")


def expected_resources(length: int) -> dict[str, int | float]:
    terminal = terminal_cache_peak_bytes(length)
    authentication = authentication_cache_peak_bytes(length)
    state = maximum_state_file_bytes(length)
    payload = payload_bytes(length)
    return {
        "maximum_live_state_bytes": state,
        "state_plus_cache_bytes": state + payload,
        "overhead_reserve_bytes": OVERHEAD_RESERVE,
        "maximum_cache_window_bytes": max(terminal, authentication),
        "terminal_cache_peak_bytes": terminal,
        "authentication_cache_peak_bytes": authentication,
        "mapped_cache_limit_bytes": MAPPED_CACHE_LIMIT,
        "scratch_limit_bytes": SCRATCH_LIMIT,
        "builder_rss_limit_bytes": BUILDER_RSS_LIMIT,
        "consumer_rss_limit_bytes": CONSUMER_RSS_LIMIT,
        "wall_limit_seconds": WALL_LIMIT,
    }


def expected_provenance(
    length: int, freeze: dict[str, object], freeze_sha: str,
    preflight_sha: str, dual_sha: str,
    prebuild_sha: str,
) -> dict[str, object]:
    files = freeze["files"]
    dependencies = freeze["sealed_dependencies"]
    result = {
        "builder_sha256": files["build_target_cache.py"],
        "consumer_sha256": files["consume_target_cache.py"],
        "preflight_sha256": files["validate_preflight.py"],
        "production_obligation_validators_sha256": files[
            "production_obligation_validators.py"
        ],
        "method_sha256": files["METHOD.md"],
        "freeze_sha256": freeze_sha,
        "dual_obstruction_gate_sha256": dual_sha,
        "target_v004_sha256": dependencies["target_v004_implementation"],
        "target_v004_original_l12_gate_sha256": dependencies[
            "target_v004_original_l12_gate"
        ],
        "hostile_v003_sha256": dependencies["hostile_v003_implementation"],
        "target_v004_method_sha256": dependencies["target_v004_method"],
        "target_v004_freeze_sha256": dependencies["target_v004_freeze"],
        "hostile_v003_method_sha256": dependencies["hostile_v003_method"],
        "hostile_v003_freeze_sha256": dependencies["hostile_v003_freeze"],
        "preserved_workspace_custody_sha256": dependencies[
            "preserved_workspace_custody_v002"
        ],
        "preserved_workspace_cross_diagnostic_sha256": dependencies[
            "preserved_workspace_cross_diagnostic_v001"
        ],
        "runtime_compatibility_obstruction_sha256": dependencies[
            "target_v005_runtime_compatibility_obstruction_v001"
        ],
        "v006_hostile_audit_obstruction_sha256": dependencies[
            "target_v006_hostile_audit_obstruction_v001"
        ],
        "v007_runtime_compatibility_obstruction_sha256": dependencies[
            "target_v007_runtime_compatibility_obstruction_v001"
        ],
        "v008_postbuild_audit_binding_obstruction_sha256": dependencies[
            "target_v008_postbuild_audit_binding_obstruction_v001"
        ],
        "v009_hostile_audit_obstruction_sha256": dependencies[
            "target_v009_hostile_audit_obstruction_v001"
        ],
        "v010_hostile_audit_obstruction_sha256": dependencies[
            "target_v010_hostile_audit_obstruction_v001"
        ],
        "v010_audit_record_custody_correction_sha256": dependencies[
            "target_v010_audit_record_custody_correction_v001"
        ],
        "v011_hostile_audit_obstruction_sha256": dependencies[
            "target_v011_hostile_audit_obstruction_v001"
        ],
        "preflight_result_sha256": preflight_sha,
        "independent_hostile_audit_sha256": prebuild_sha,
        "canonical_cache_root": str(CACHE_PARENT / f"L{length}"),
    }
    if len(result) != 27:
        raise AuditRefusal("manifest provenance field census changed")
    return result


def _is_sha256(value: object) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def validate_authorities(custody: HeldAuthoritySet) -> tuple[
    dict[str, object], str, str, dict[str, object], str, str,
]:
    custody.reauthenticate()
    freeze, freeze_sha = custody.records["A01"], custody.hashes["A01"]
    preflight, preflight_sha = custody.records["A02"], custody.hashes["A02"]
    prebuild, prebuild_sha = custody.records["A03"], custody.hashes["A03"]
    dual, dual_sha = custody.records["A04"], custody.hashes["A04"]
    if (
        set(freeze) != FREEZE_KEYS
        or freeze.get("schema") != "TARGET_L12_STORAGE_CACHE_FREEZE_V012"
        or freeze.get("status")
        != "FROZEN_BEFORE_NONPHYSICAL_PREFLIGHT_V001_OUTPUT"
        or freeze.get("frozen_before_nonphysical_preflight_output") is not True
        or freeze.get("cache_payload_created") is not False
        or freeze.get("physical_history_executed") is not False
        or freeze.get("current_v004_target_or_hostile_execution_interrupted")
        is not False
        or freeze.get("current_v004_workspace_output_or_cache_read_or_modified")
        is not False
        or freeze.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or freeze.get("claim_boundary")
        != "AUDIT_BOUND_COMPATIBILITY_SUCCESSOR_PRE_PAYLOAD__NO_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
        or type(freeze.get("files")) is not dict
        or set(freeze["files"])
        != {
            "METHOD.md", "build_target_cache.py", "consume_target_cache.py",
            "production_obligation_validators.py", "validate_preflight.py",
        }
        or any(not _is_sha256(value) for value in freeze["files"].values())
        or type(freeze.get("sealed_dependencies")) is not dict
        or any(
            type(freeze.get(key)) is not dict
            for key in (
                "obstruction_evidence", "predecessor_compatibility_custody",
                "predecessor_v007_obstruction_custody",
                "predecessor_v008_obstruction_custody",
            )
        )
        or set(preflight) != PREFLIGHT_KEYS
        or preflight.get("schema")
        != "TARGET_L12_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT_V012"
        or preflight.get("classification")
        != "PASS_NONPHYSICAL_EXHAUSTIVE_INDEX_ALLOCATION_AND_HARD_LOCK_PREFLIGHT"
        or preflight.get("physical_cache_payload_created") is not False
        or preflight.get("physical_history_executed") is not False
        or preflight.get("claim_boundary")
        != "V012_PORTABLE_NONPHYSICAL_STORAGE_INDEX_PROOF_ONLY__NO_CACHE_PAYLOAD_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
        or type(preflight.get("files")) is not dict
        or type(preflight.get("mutation_ledger")) is not dict
        or set(prebuild) != PREBUILD_KEYS
        or prebuild.get("schema") != "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001"
        or prebuild.get("classification")
        != "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE"
        or prebuild.get("auditor_role") != "INDEPENDENT_HOSTILE_READ_ONLY_REVIEW"
        or prebuild.get("audited_packet")
        != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or prebuild.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or prebuild.get("payload_or_history_executed") is not False
        or prebuild.get("no_symlinked_inputs") is not True
        or prebuild.get("v005_v006_v007_v008_v009_v010_v011_bytes_preserved")
        is not True
        or prebuild.get("failures") != []
        or type(prebuild.get("checks_total")) is not int
        or prebuild.get("checks_total") != prebuild.get("checks_passed")
        or prebuild["checks_total"] <= 0
        or prebuild.get("claim_boundary")
        != "V012_PREPAYLOAD_CONTROL_PLANE_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        or set(dual) != DUAL_KEYS
        or dual.get("schema")
        != "TARGET_V012_DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE"
        or dual.get("classification")
        != "AUTHORIZE_TARGET_V012_FRESH_CACHE_AFTER_V005_V006_V007_V008_V009_V010_AND_V011_CONTROL_PLANE_OBSTRUCTIONS"
        or dual.get("authorized_cache_lengths") != list(SUPPORTED)
        or any(type(value) is not int for value in dual["authorized_cache_lengths"])
        or dual.get("freeze_sha256") != freeze_sha
        or dual.get("preflight_result_sha256") != preflight_sha
        or dual.get("claim_boundary")
        != "CONTROL_PLANE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT"
        or dual.get("independent_hostile_audit")
        != {
            "path": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
            "sha256": prebuild_sha,
        }
    ):
        raise AuditRefusal("A01--A04 authority chain mismatch")
    files = freeze["files"]
    dependencies = freeze["sealed_dependencies"]
    required_dependencies = {
        "target_v004_implementation", "hostile_v003_implementation",
        "preserved_workspace_custody_v002",
        "preserved_workspace_cross_diagnostic_v001",
        "target_v005_runtime_compatibility_obstruction_v001",
        "target_v006_hostile_audit_obstruction_v001",
        "target_v007_runtime_compatibility_obstruction_v001",
        "target_v008_postbuild_audit_binding_obstruction_v001",
        "target_v009_hostile_audit_obstruction_v001",
        "target_v010_hostile_audit_obstruction_v001",
        "target_v010_audit_record_custody_correction_v001",
        "target_v011_hostile_audit_obstruction_v001",
    }
    if (
        not required_dependencies.issubset(dependencies)
        or any(not _is_sha256(dependencies[key]) for key in required_dependencies)
    ):
        raise AuditRefusal("A01 sealed dependency provenance mismatch")
    required_nested_paths = {
        "obstruction_evidence": {
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_OBSTRUCTION.json",
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_OBSTRUCTION.json",
        },
        "predecessor_compatibility_custody": {
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/DUAL_SIX_HOUR_OBSTRUCTION_GATE_V005.json",
        },
        "predecessor_v007_obstruction_custody": {
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V007.json",
        },
        "predecessor_v008_obstruction_custody": {
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V008.json",
        },
    }
    if any(
        not paths.issubset(freeze[field])
        or any(not _is_sha256(freeze[field][path]) for path in paths)
        for field, paths in required_nested_paths.items()
    ):
        raise AuditRefusal("A01 predecessor authority provenance mismatch")
    expected_preflight_files = {
        "builder_sha256": files["build_target_cache.py"],
        "consumer_sha256": files["consume_target_cache.py"],
        "freeze_sha256": freeze_sha,
        "method_sha256": files["METHOD.md"],
        "preflight_sha256": files["validate_preflight.py"],
        "production_obligation_validators_sha256": files[
            "production_obligation_validators.py"
        ],
    }
    if (
        preflight["files"] != expected_preflight_files
        or preflight["mutation_ledger"].get("classification")
        != "PASS_EXECUTED_PREREGISTERED_MUTATION_ASSIGNMENTS"
        or preflight["mutation_ledger"].get("case_count") != 477
        or preflight["mutation_ledger"].get("mutation_sink_call_count") != 477
        or preflight["mutation_ledger"].get("positive_sink_call_count") != 33
        or preflight["mutation_ledger"].get("validator_module_sha256")
        != files["production_obligation_validators.py"]
        or prebuild.get("audited_files_sha256") != files
        or prebuild.get("audited_freeze_sha256") != freeze_sha
        or prebuild.get("preflight_result_sha256") != preflight_sha
        or prebuild.get("mutation_ledger") != preflight["mutation_ledger"]
    ):
        raise AuditRefusal("A01--A03 authority provenance mismatch")
    dual_links = {
        "builder_sha256": files["build_target_cache.py"],
        "consumer_sha256": files["consume_target_cache.py"],
        "method_sha256": files["METHOD.md"],
        "preflight_sha256": files["validate_preflight.py"],
        "target_v004_sha256": dependencies["target_v004_implementation"],
        "hostile_v003_sha256": dependencies["hostile_v003_implementation"],
        "preserved_workspace_custody_sha256": dependencies[
            "preserved_workspace_custody_v002"
        ],
        "preserved_workspace_cross_diagnostic_sha256": dependencies[
            "preserved_workspace_cross_diagnostic_v001"
        ],
        "runtime_compatibility_obstruction_sha256": dependencies[
            "target_v005_runtime_compatibility_obstruction_v001"
        ],
        "v006_hostile_audit_obstruction_sha256": dependencies[
            "target_v006_hostile_audit_obstruction_v001"
        ],
        "v007_runtime_compatibility_obstruction_sha256": dependencies[
            "target_v007_runtime_compatibility_obstruction_v001"
        ],
        "v008_postbuild_audit_binding_obstruction_sha256": dependencies[
            "target_v008_postbuild_audit_binding_obstruction_v001"
        ],
        "v009_hostile_audit_obstruction_sha256": dependencies[
            "target_v009_hostile_audit_obstruction_v001"
        ],
        "v010_hostile_audit_obstruction_sha256": dependencies[
            "target_v010_hostile_audit_obstruction_v001"
        ],
        "v010_audit_record_custody_correction_sha256": dependencies[
            "target_v010_audit_record_custody_correction_v001"
        ],
        "v011_hostile_audit_obstruction_sha256": dependencies[
            "target_v011_hostile_audit_obstruction_v001"
        ],
    }
    expected_obstructions = [
        {
            "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_OBSTRUCTION.json",
            "role": "target",
            "sha256": freeze["obstruction_evidence"][
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_OBSTRUCTION.json"
            ],
        },
        {
            "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_OBSTRUCTION.json",
            "role": "hostile",
            "sha256": freeze["obstruction_evidence"][
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_OBSTRUCTION.json"
            ],
        },
    ]
    predecessor_gate_links = {
        "superseded_v005_dual_gate_sha256": freeze[
            "predecessor_compatibility_custody"
        ]["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/DUAL_SIX_HOUR_OBSTRUCTION_GATE_V005.json"],
        "superseded_v007_dual_gate_sha256": freeze[
            "predecessor_v007_obstruction_custody"
        ]["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V007.json"],
        "superseded_v008_dual_gate_sha256": freeze[
            "predecessor_v008_obstruction_custody"
        ]["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V008.json"],
    }
    if (
        any(dual.get(key) != value for key, value in dual_links.items())
        or dual.get("obstructions") != expected_obstructions
        or any(dual.get(key) != value for key, value in predecessor_gate_links.items())
        or any(
            type(dual.get(key)) is not dict
            or set(dual[key]) != {str(length) for length in SUPPORTED}
            or any(not _is_sha256(value) for value in dual[key].values())
            for key in (
                "superseded_v005_cache_manifest_sha256_by_L",
                "superseded_v007_cache_manifest_sha256_by_L",
                "superseded_v008_cache_manifest_sha256_by_L",
            )
        )
    ):
        raise AuditRefusal("A04 authority provenance mismatch")
    for name, digest in files.items():
        if custody.hashes.get(f"source:{name}") != digest:
            raise AuditRefusal(f"frozen source hash mismatch: {name}")
    custody.reauthenticate()
    return freeze, freeze_sha, preflight_sha, dual, dual_sha, prebuild_sha


def validate_manifest(
    length: int, manifest: dict[str, object], custody: HeldCacheSet,
    provenance: dict[str, object], dual: dict[str, object],
) -> dict[str, tuple[str, tuple[int, ...], dict[str, object]]]:
    expected = expected_records(length)
    if (
        set(manifest) != MANIFEST_KEYS
        or manifest.get("schema") != "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012"
        or manifest.get("status") != "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE"
        or type(manifest.get("L")) is not int or manifest.get("L") != length
        or manifest.get("basis_order")
        != "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER"
        or manifest.get("lineage_identity") != "FULL_CANONICAL_MASK"
        or type(manifest.get("hamiltonian_exchange_coefficient")) is not int
        or manifest.get("hamiltonian_exchange_coefficient") != -1
        or manifest.get("edge_layout") != graph(length)
        or manifest.get("claim_boundary")
        != "TARGET_V012_PORTABLE_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_OR_GRAVITY"
    ):
        raise AuditRefusal(f"L{length} manifest identity mismatch")
    if any(
        manifest.get(key) != value
        or type(manifest.get(key)) is not type(value)
        for key, value in provenance.items()
    ) or any(
        not exact_tree_equal(manifest.get(key), dual.get(key))
        for key in SUPERSEDED_PROVENANCE_KEYS
    ):
        raise AuditRefusal(f"L{length} manifest provenance mismatch")
    rows = manifest.get("files")
    if type(rows) is not list or len(rows) != len(expected):
        raise AuditRefusal(f"L{length} manifest file census mismatch")
    seen: set[str] = set()
    totals = {"operator": 0, "admission": 0, "lineage_mask": 0, "lineage_map": 0}
    zero_q0 = 0
    for row in rows:
        if type(row) is not dict or type(row.get("path")) is not str:
            raise AuditRefusal(f"L{length} manifest row malformed")
        name = row["path"]
        if name in seen or name not in expected:
            raise AuditRefusal(f"L{length} manifest row duplicate/unexpected: {name}")
        seen.add(name)
        dtype, shape, metadata = expected[name]
        if (
            set(row) != {"path", "dtype", "shape", "bytes", "sha256", *metadata}
            or row.get("dtype") != dtype
            or row.get("shape") != list(shape)
            or any(type(value) is not int for value in row["shape"])
            or type(row.get("bytes")) is not int
            or row["bytes"] != math.prod(shape) * np.dtype(dtype).itemsize
            or row.get("sha256") != custody.member_hashes[(length, name)]
            or type(row.get("sha256")) is not str
            or len(row["sha256"]) != 64
            or any(row.get(key) != value or type(row.get(key)) is not type(value)
                   for key, value in metadata.items())
        ):
            raise AuditRefusal(f"L{length} manifest member mismatch: {name}")
        if custody.member_identities[(length, name)][2] != row["bytes"]:
            raise AuditRefusal(f"L{length} member byte mismatch: {name}")
        totals[metadata["kind"]] += row["bytes"]
        if metadata["kind"] == "operator" and metadata["q"] == 0 and metadata["role"] in {"sources", "targets"}:
            if row["bytes"] != 0:
                raise AuditRefusal(f"L{length} nonempty q0 carrier incidence")
            zero_q0 += 1
    if seen != set(expected) or zero_q0 != 2:
        raise AuditRefusal(f"L{length} manifest completeness mismatch")
    expected_payload = {
        "operator_bytes": operator_bytes(length),
        "admission_bytes": admission_bytes(length),
        "lineage_mask_bytes": lineage_mask_bytes(length),
        "lineage_map_bytes": lineage_map_bytes(length),
        "total_bytes": payload_bytes(length),
        "file_count": expected_file_count(length),
    }
    if (
        manifest.get("payload") != expected_payload
        or any(type(value) is not int for value in manifest["payload"].values())
        or totals != {
            "operator": expected_payload["operator_bytes"],
            "admission": expected_payload["admission_bytes"],
            "lineage_mask": expected_payload["lineage_mask_bytes"],
            "lineage_map": expected_payload["lineage_map_bytes"],
        }
        or not exact_tree_equal(manifest.get("resource_certificates"), expected_resources(length))
    ):
        raise AuditRefusal(f"L{length} manifest arithmetic/resource mismatch")
    return expected


def _close_mapping(mapping: mmap.mmap | None) -> None:
    if mapping is not None:
        mapping.close()


def validate_semantics(
    length: int, custody: HeldCacheSet,
    expected: dict[str, tuple[str, tuple[int, ...], dict[str, object]]],
) -> None:
    del expected
    carrier: dict[int, np.ndarray] = {}
    carrier_maps: dict[int, mmap.mmap | None] = {}
    lineage: dict[tuple[int, int], np.ndarray] = {}
    lineage_maps: dict[tuple[int, int], mmap.mmap | None] = {}
    visited: set[str] = set()
    try:
        for q in range(length + 1):
            name = f"carrier_q_{q:02d}_words.u32"
            words, mapping = custody.array(
                length, name, WORD_DTYPE, (math.comb(2 * length, q),),
            )
            direct = fixed_words(2 * length, q)
            if not np.array_equal(words, direct):
                raise AuditRefusal(f"L{length} q={q} carrier basis mismatch")
            carrier[q] = words
            carrier_maps[q] = mapping
            visited.add(name)
            offsets_name = f"carrier_q_{q:02d}_offsets.u64"
            offsets, offsets_map = custody.array(
                length, offsets_name, OFFSET_DTYPE, (3 * length + 1,),
            )
            pair_count = math.comb(2 * length - 2, q - 1) if q else 0
            direct_offsets = np.arange(3 * length + 1, dtype=OFFSET_DTYPE) * pair_count
            if not np.array_equal(offsets, direct_offsets):
                raise AuditRefusal(f"L{length} q={q} carrier offsets mismatch")
            visited.add(offsets_name)
            sources_name = f"carrier_q_{q:02d}_sources.i32"
            targets_name = f"carrier_q_{q:02d}_targets.i32"
            total_pairs = 3 * length * pair_count
            sources, sources_map = custody.array(
                length, sources_name, INDEX_DTYPE, (total_pairs,),
            )
            targets, targets_map = custody.array(
                length, targets_name, INDEX_DTYPE, (total_pairs,),
            )
            for edge_index, edge in enumerate(graph(length)):
                u, v = edge[:2]
                lower = edge_index * pair_count
                upper = lower + pair_count
                expected_sources = np.flatnonzero(
                    (((words >> u) & 1) == 1) & (((words >> v) & 1) == 0)
                ).astype(INDEX_DTYPE)
                observed_sources = sources[lower:upper]
                observed_targets = targets[lower:upper]
                if (
                    not np.array_equal(observed_sources, expected_sources)
                    or (len(observed_targets) and (
                        int(np.min(observed_targets)) < 0
                        or int(np.max(observed_targets)) >= len(words)
                    ))
                    or not np.array_equal(
                        words[observed_targets],
                        words[expected_sources] ^ ((1 << u) | (1 << v)),
                    )
                ):
                    raise AuditRefusal(
                        f"L{length} q={q} edge={edge_index} exchange map mismatch"
                    )
            visited.update((sources_name, targets_name))
            _close_mapping(offsets_map)
            _close_mapping(sources_map)
            _close_mapping(targets_map)
        for event in range(length):
            for q in range(event + 1):
                shape = (math.comb(2 * length - 1, q),)
                blank_name = f"admission_n_{event:02d}_q_{q:02d}_blank.i32"
                destination_name = f"admission_n_{event:02d}_q_{q:02d}_destination.i32"
                blank, blank_map = custody.array(length, blank_name, INDEX_DTYPE, shape)
                destination, destination_map = custody.array(
                    length, destination_name, INDEX_DTYPE, shape,
                )
                expected_blank = np.flatnonzero(
                    ((carrier[q] >> event) & 1) == 0
                ).astype(INDEX_DTYPE)
                if (
                    not np.array_equal(blank, expected_blank)
                    or (len(destination) and (
                        int(np.min(destination)) < 0
                        or int(np.max(destination)) >= len(carrier[q + 1])
                    ))
                    or not np.array_equal(
                        carrier[q + 1][destination],
                        carrier[q][expected_blank] | (1 << event),
                    )
                ):
                    raise AuditRefusal(
                        f"L{length} event={event} q={q} admission map mismatch"
                    )
                visited.update((blank_name, destination_name))
                _close_mapping(blank_map)
                _close_mapping(destination_map)
        for prefix in range(length):
            for q in range(prefix + 1):
                name = f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32"
                words, mapping = custody.array(
                    length, name, WORD_DTYPE, (math.comb(prefix, q),),
                )
                if not np.array_equal(words, fixed_words(prefix, q)):
                    raise AuditRefusal(
                        f"L{length} prefix={prefix} q={q} lineage basis mismatch"
                    )
                lineage[(prefix, q)] = words
                lineage_maps[(prefix, q)] = mapping
                visited.add(name)
        for prefix in range(length - 1):
            for q in range(prefix + 1):
                for accepted, role in ((False, "stay"), (True, "accepted")):
                    name = f"lineage_n_{prefix:02d}_q_{q:02d}_{role}.i32"
                    shape = (math.comb(prefix, q),)
                    indices, mapping = custody.array(
                        length, name, INDEX_DTYPE, shape,
                    )
                    target = lineage[(prefix + 1, q + int(accepted))]
                    expected_words = lineage[(prefix, q)] | (
                        (1 << prefix) if accepted else 0
                    )
                    if (
                        len(indices) and (
                            int(np.min(indices)) < 0
                            or int(np.max(indices)) >= len(target)
                        )
                    ) or not np.array_equal(target[indices], expected_words):
                        raise AuditRefusal(
                            f"L{length} prefix={prefix} q={q} {role} map mismatch"
                        )
                    visited.add(name)
                    _close_mapping(mapping)
        expected_names = {
            name for item_length, name in custody.member_fds
            if item_length == length
        }
        if visited != expected_names:
            raise AuditRefusal(f"L{length} semantic member coverage mismatch")
    finally:
        for mapping in carrier_maps.values():
            _close_mapping(mapping)
        for mapping in lineage_maps.values():
            _close_mapping(mapping)


def validate_a06_record(
    record: dict[str, object], manifest_hashes: dict[str, str],
    payload_census: dict[str, dict[str, int]], prebuild_sha: str,
    dual_sha: str,
) -> None:
    if (
        set(record) != A06_KEYS
        or record.get("schema") != SCHEMA
        or record.get("classification") != CLASSIFICATION
        or record.get("auditor_role")
        != "INDEPENDENT_HOSTILE_POSTBUILD_READ_ONLY_REVIEW"
        or record.get("audited_packet")
        != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or record.get("sealed_input_commit")
        != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or record.get("prebuild_hostile_audit_sha256") != prebuild_sha
        or record.get("dual_obstruction_and_compatibility_gate_sha256") != dual_sha
        or record.get("manifest_sha256_by_L") != manifest_hashes
        or record.get("payload_census_by_L") != payload_census
        or record.get("checks") != CHECKS
        or any(type(value) is not int or value <= 0 for value in record["checks"].values())
        or type(record.get("checks_total")) is not int
        or record.get("checks_total") != 3489
        or record.get("checks_total") != sum(CHECKS.values())
        or type(record.get("checks_passed")) is not int
        or record.get("checks_passed") != record["checks_total"]
        or record.get("failures") != []
        or record.get("no_symlinked_or_writable_payload_inputs") is not True
        or record.get("physical_gate_or_history_executed") is not False
        or record.get("semantic_cachecontext")
        != {
            "L4": {
                "descriptor_count": 62,
                "descriptor_reauthentication": "PASS",
                "full_index_identity": "PASS",
                "zero_length_q0_open": "PASS",
            },
            "L12": {
                "descriptor_count": 418,
                "descriptor_reauthentication": "PASS",
                "full_index_identity": "PASS",
                "zero_length_q0_open": "PASS",
            },
        }
        or record.get("claim_boundary") != CLAIM
    ):
        raise AuditRefusal("A06 exact record reconstruction mismatch")


def audit_record() -> tuple[dict[str, object], HeldCacheSet, HeldAuthoritySet]:
    authorities = HeldAuthoritySet()
    custody = HeldCacheSet()
    try:
        authorities.open_all()
        freeze, freeze_sha, preflight_sha, dual, dual_sha, prebuild_sha = (
            validate_authorities(authorities)
        )
        if any(path.exists() or path.is_symlink() for path in PHYSICAL_ABSENCE_PATHS):
            raise AuditRefusal("physical gate/workspace/history path present before A06")
        if CANONICAL_A06.exists() or CANONICAL_A06.is_symlink():
            raise AuditRefusal("canonical A06 already exists")
        custody.open_all()
        payload_census: dict[str, dict[str, int]] = {}
        for length in SUPPORTED:
            provenance = expected_provenance(
                length, freeze, freeze_sha, preflight_sha, dual_sha,
                prebuild_sha,
            )
            expected = validate_manifest(
                length, custody.manifests[length], custody, provenance, dual,
            )
            validate_semantics(length, custody, expected)
            payload_census[str(length)] = {
                "file_count": expected_file_count(length),
                "total_bytes": payload_bytes(length),
            }
        custody.reauthenticate()
        manifest_hashes = {
            str(length): custody.manifest_hashes[length] for length in SUPPORTED
        }
        record = {
            "schema": SCHEMA,
            "classification": CLASSIFICATION,
            "auditor_role": "INDEPENDENT_HOSTILE_POSTBUILD_READ_ONLY_REVIEW",
            "audited_packet": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012",
            "sealed_input_commit": "42f1ea3301ccf98802c07f3330d52999385cba0b",
            "prebuild_hostile_audit_sha256": prebuild_sha,
            "dual_obstruction_and_compatibility_gate_sha256": dual_sha,
            "manifest_sha256_by_L": manifest_hashes,
            "payload_census_by_L": payload_census,
            "checks": dict(CHECKS),
            "checks_passed": sum(CHECKS.values()),
            "checks_total": sum(CHECKS.values()),
            "failures": [],
            "no_symlinked_or_writable_payload_inputs": True,
            "semantic_cachecontext": {
                "L4": {
                    "descriptor_count": expected_file_count(4),
                    "descriptor_reauthentication": "PASS",
                    "full_index_identity": "PASS",
                    "zero_length_q0_open": "PASS",
                },
                "L12": {
                    "descriptor_count": expected_file_count(12),
                    "descriptor_reauthentication": "PASS",
                    "full_index_identity": "PASS",
                    "zero_length_q0_open": "PASS",
                },
            },
            "physical_gate_or_history_executed": False,
            "claim_boundary": CLAIM,
        }
        validate_a06_record(
            record, manifest_hashes, payload_census, prebuild_sha, dual_sha,
        )
        custody.reauthenticate()
        authorities.reauthenticate()
        return record, custody, authorities
    except BaseException:
        custody.close()
        authorities.close()
        raise


def _parent_identity(parent: Path, descriptor: int, label: str) -> tuple[int, int]:
    _require_no_symlink_parents(parent / "placeholder", label)
    held = os.fstat(descriptor)
    try:
        named = os.stat(parent, follow_symlinks=False)
    except OSError as error:
        raise AuditRefusal(f"{label} canonical parent changed") from error
    if (
        not stat.S_ISDIR(held.st_mode) or not stat.S_ISDIR(named.st_mode)
        or stat.S_ISLNK(named.st_mode)
        or (held.st_dev, held.st_ino) != (named.st_dev, named.st_ino)
    ):
        raise AuditRefusal(f"{label} canonical parent changed")
    return held.st_dev, held.st_ino


def _unlink_owned_at(
    parent_descriptor: int, name: str, identity: tuple[int, int],
) -> bool:
    try:
        value = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except FileNotFoundError:
        return False
    if (
        not stat.S_ISREG(value.st_mode)
        or (value.st_dev, value.st_ino) != identity
    ):
        return False
    os.unlink(name, dir_fd=parent_descriptor)
    return True


def _require_absent_at(parent_descriptor: int, name: str, label: str) -> None:
    try:
        os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except FileNotFoundError:
        return
    raise AuditRefusal(f"{label} was not removed")


def _atomic_publish_once(
    destination: Path, record: dict[str, object], expected: Path,
) -> str:
    if destination != expected or not destination.is_absolute():
        raise AuditRefusal("A06 output path is not the exact canonical path")
    _require_no_symlink_parents(destination, "A06 output")
    parent = destination.parent
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(parent, flags)
    except OSError as error:
        raise AuditRefusal("A06 parent is absent or aliased") from error
    staging_descriptor = -1
    staging_name = f".{destination.name}.staging-{os.getpid()}-{os.urandom(12).hex()}"
    staging_identity: tuple[int, int] | None = None
    raw = canonical_json_bytes(record)
    digest = hashlib.sha256(raw).hexdigest()
    try:
        _parent_identity(parent, parent_descriptor, "A06 output")
        try:
            os.stat(destination.name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise AuditRefusal("A06 canonical destination already exists")
        staging_descriptor = os.open(
            staging_name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400, dir_fd=parent_descriptor,
        )
        opened = os.fstat(staging_descriptor)
        staging_identity = (opened.st_dev, opened.st_ino)
        offset = 0
        while offset < len(raw):
            written = os.write(staging_descriptor, raw[offset:])
            if written <= 0:
                raise AuditRefusal("A06 staging write made no progress")
            offset += written
        os.fsync(staging_descriptor)
        os.fchmod(staging_descriptor, 0o444)
        os.fsync(staging_descriptor)
        sealed = os.fstat(staging_descriptor)
        if (
            not stat.S_ISREG(sealed.st_mode) or sealed.st_mode & 0o222
            or sealed.st_nlink != 1
            or (sealed.st_dev, sealed.st_ino) != staging_identity
            or sealed.st_size != len(raw)
            or _descriptor_sha256(staging_descriptor) != digest
        ):
            raise AuditRefusal("A06 staging authentication mismatch")
        _parent_identity(parent, parent_descriptor, "A06 output")
        try:
            os.link(
                staging_name, destination.name, src_dir_fd=parent_descriptor,
                dst_dir_fd=parent_descriptor, follow_symlinks=False,
            )
        except FileExistsError as error:
            raise AuditRefusal(
                "A06 canonical destination appeared before commit"
            ) from error
        _parent_identity(parent, parent_descriptor, "A06 output")
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
                or _descriptor_sha256(canonical) != digest
            ):
                raise AuditRefusal("A06 canonical link authentication mismatch")
        finally:
            os.close(canonical)
        if not _unlink_owned_at(
            parent_descriptor, staging_name, staging_identity,
        ):
            raise AuditRefusal("A06 staging custody changed after commit")
        _require_absent_at(parent_descriptor, staging_name, "A06 staging")
        os.fsync(parent_descriptor)
        _parent_identity(parent, parent_descriptor, "A06 output")
        final = os.open(
            destination.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_descriptor,
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
                or _descriptor_sha256(final) != digest
            ):
                raise AuditRefusal("published A06 custody mismatch")
        finally:
            os.close(final)
        _parent_identity(parent, parent_descriptor, "A06 output")
        return digest
    except BaseException as error:
        try:
            if staging_identity is not None:
                _unlink_owned_at(
                    parent_descriptor, staging_name, staging_identity,
                )
                _require_absent_at(
                    parent_descriptor, staging_name, "A06 staging cleanup",
                )
                os.fsync(parent_descriptor)
        except BaseException:
            raise AuditRefusal("A06 staging cleanup failed") from error
        raise
    finally:
        if staging_descriptor >= 0:
            os.close(staging_descriptor)
        os.close(parent_descriptor)


def revalidate_record_against_custody(
    record: dict[str, object], custody: HeldCacheSet,
    authorities: HeldAuthoritySet,
) -> None:
    if custody.lengths != SUPPORTED:
        raise AuditRefusal("A06 publication does not retain all cache lengths")
    manifest_hashes = {
        str(length): custody.manifest_hashes[length] for length in SUPPORTED
    }
    payload_census = {
        str(length): {
            "file_count": expected_file_count(length),
            "total_bytes": payload_bytes(length),
        }
        for length in SUPPORTED
    }
    validate_a06_record(
        record, manifest_hashes, payload_census,
        authorities.hashes["A03"], authorities.hashes["A04"],
    )


def run(*, publish: bool = False) -> dict[str, object]:
    record, custody, authorities = audit_record()
    try:
        revalidate_record_against_custody(record, custody, authorities)
        if publish:
            authorities.reauthenticate()
            custody.reauthenticate()
            digest = _atomic_publish_once(CANONICAL_A06, record, CANONICAL_A06)
            authorities.reauthenticate()
            custody.reauthenticate()
            observed, observed_digest = stable_file(CANONICAL_A06, "canonical A06")
            if observed_digest != digest or not exact_tree_equal(observed, record):
                raise AuditRefusal("canonical A06 postpublication mismatch")
            authorities.reauthenticate()
            custody.reauthenticate()
            revalidate_record_against_custody(observed, custody, authorities)
        else:
            authorities.reauthenticate()
            custody.reauthenticate()
            revalidate_record_against_custody(record, custody, authorities)
        return record
    finally:
        custody.close()
        authorities.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--publish", action="store_true",
        help="owner-once publish the canonical A06 after all checks pass",
    )
    args = parser.parse_args()
    try:
        record = run(publish=args.publish)
    except (AuditRefusal, OSError, ValueError, MemoryError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "classification": record["classification"],
        "checks_passed": record["checks_passed"],
        "checks_total": record["checks_total"],
        "manifest_sha256_by_L": record["manifest_sha256_by_L"],
        "published": args.publish,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
