#!/usr/bin/env python3
"""Build the authenticated L4--L12 relational sector manifest once.

The bridge reads only already-produced target/blind native histories and their
hostile audit records.  It does not import or execute a history or spectrum
engine.  Every interval and atom is reconstructed before an owner-once output
is created.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
SIZES: Final[tuple[int, ...]] = (4, 6, 8, 10, 12)
SCHEMA: Final[str] = "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"
STATUS: Final[str] = (
    "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY"
)
PROTOCOL_SHA256: Final[str] = (
    "d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95"
)
BUILD_TOKEN: Final[str] = "BUILD_AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"
MAX_SOURCE_BYTES: Final[int] = 64 * 2**20
MAX_MANIFEST_BYTES: Final[int] = 16 * 2**20
CANONICAL_OUTPUT: Final[Path] = (
    ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001.json"
)
OBSERVABLE_FIELDS: Final[tuple[str, ...]] = (
    "W_n",
    "allow_probability",
    "blocked_probability",
    "reverse_support_probability",
    "connector_delta_l1",
    "connector_delta_signed",
    "q_retained_after_transport",
    "q_genesis_after",
)
CANONICAL_SOURCES: Final[dict[int, dict[str, str]]] = {
    4: {
        "target": "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L4.json",
        "blind": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L4.json",
        "audit": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/SEED_HOSTILE_RESULT.json",
    },
    6: {
        "target": "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L6.json",
        "blind": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L6.json",
        "audit": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/SEED_HOSTILE_RESULT.json",
    },
    8: {
        "target": "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L8.json",
        "blind": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/HISTORY_L8.json",
        "audit": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/SEED_HOSTILE_RESULT.json",
    },
    10: {
        "target": "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/STREAMED_HISTORY_L10_V002.json",
        "blind": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/RAW_HISTORY/BLIND_STREAMED_HISTORY_L10.json",
        "audit": "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/L10_V002_HOSTILE_RESULT.json",
    },
    12: {
        "target": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json",
        "blind": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json",
        "audit": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/FINAL_L12_TARGET_HOSTILE_AUDIT_V001.json",
    },
}
STAGE2_LINEAGE_SOURCES: Final[dict[str, dict[str, str]]] = {
    "target_L4": {"path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L4.json", "sha256": "bd84329008b969975be26e61e00defaf52b9f11de2d160488ad953ce0bb27254"},
    "target_L6": {"path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L6.json", "sha256": "d7d6f111c657d514c3251da1ca8a20db955b5298937b8effe9832eda73d8fbda"},
    "target_L8": {"path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L8.json", "sha256": "8cbefeccb4ef9273c20d90519d95501ddc4db0ee8c449fc762313ecefcbd232c"},
    "target_L10": {"path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L10.json", "sha256": "422cd12235d59d44986daf2490e467677c86f7eb82da16f31c8403769cf9675d"},
    "hostile_L10": {"path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json", "sha256": "151e9197512adb3c7ff3d9ce7a7b497e92fcf8dbd846e067dd4061c5191975b4"},
    "control_audit": {"path": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json", "sha256": "4da29efa71259c1e44b42bda8b8d48332940de9d9557c621025b706f4b93392f"},
    "l10_audit": {"path": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json", "sha256": "5b694804b9d0dfc7b1238ca2d8a3b4342849ffd7beaa9dc64d057633cc2d80a6"},
    "a18_cross_gate": {"path": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_HOSTILE_L10_CROSS_GATE_V001.json", "sha256": "84a99de5d97373f8daeb2a1bcf1adcf04d2f0e0ee17dab13f58859d35bf141c5"},
}
AUTHORITY_INSTANCE_CENSUS: Final[dict[str, int]] = {
    "A01_FREEZE_AND_SOURCE_PACKET": 1, "A02_NONPHYSICAL_PREFLIGHT": 1,
    "A03_PREPAYLOAD_AUDIT": 1, "A04_UNIVERSAL_CUSTODY_GATE": 1,
    "A05_FIVE_CACHE_SET": 5, "A06_POSTBUILD_AUDIT": 1,
    "A07_BASE_PHYSICAL_GATE": 1, "A08_PHYSICAL_GATE_AUDIT": 1,
    "A09_CONTROL_AUTHORIZATION": 1, "A10_CONTROL_HISTORIES": 3,
    "A11_CONTROL_STAGE_GATE": 1, "A12_CONTROL_STAGE_AUDIT": 1,
    "A13_L10_AUTHORIZATION": 1, "A14_L10_HISTORY": 1,
    "A15_L10_STAGE_GATE": 1, "A16_L10_STAGE_AUDIT": 1,
    "A17_HOSTILE_L12_ELIGIBILITY": 1, "A18_L10_CROSS_GATE": 1,
    "A20_SHARED_SCHEDULE_GATE": 1, "A21_SHARED_SCHEDULE_AUDIT": 1,
    "A22_TARGET_L12_AUTHORIZATION": 12, "A23_POSTRUN_TELEMETRY": 1,
    "A24_TARGET_L12_HISTORY": 1, "A25_HOSTILE_L12_HISTORY": 1,
    "A27_MUTATION_LEDGER": 1,
}
A17_SOURCE_LABELS: Final[tuple[str, ...]] = (
    "method", "builder", "consumer", "preflight", "freeze",
    "preflight_result", "independent_audit", "cached_L10_gate",
    "L12_cache_manifest",
)
A17_CANONICAL_SOURCES: Final[dict[str, str]] = {
    "method": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_METHOD.md",
    "builder": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/build_cache_v004r4.py",
    "consumer": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py",
    "preflight": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/validate_cache_preflight_v004r4.py",
    "freeze": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004R4.json",
    "preflight_result": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PREFLIGHT_RESULT.json",
    "independent_audit": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_AUDIT_RESULT_V004R4.json",
    "cached_L10_gate": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
    "L12_cache_manifest": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L12/CACHE_MANIFEST.json",
}
A17_RECORD_IDENTITIES: Final[dict[str, tuple[str, str, str]]] = {
    "freeze": ("AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4", "status", "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT"),
    "preflight_result": ("HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT_V001", "classification", "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT"),
    "independent_audit": ("HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001", "classification", "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE"),
    "cached_L10_gate": ("HOSTILE_V004R4_CACHED_L10_GATE", "classification", "PASS_HOSTILE_V004R4_CACHED_L10"),
    "L12_cache_manifest": ("HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4", "status", "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE"),
}
AUTHORITY_CANONICAL_SOURCES: Final[dict[tuple[str, int], str]] = {
    ("A01_FREEZE_AND_SOURCE_PACKET", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    ("A02_NONPHYSICAL_PREFLIGHT", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_RESULT_V001.json",
    ("A03_PREPAYLOAD_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
    ("A04_UNIVERSAL_CUSTODY_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
    ("A06_POSTBUILD_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/POSTBUILD_PAYLOAD_AUDIT_V001.json",
    ("A07_BASE_PHYSICAL_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_EXECUTION_GATE_V012.json",
    ("A08_PHYSICAL_GATE_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_GATE_HOSTILE_AUDIT_V001.json",
    ("A09_CONTROL_AUTHORIZATION", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json",
    ("A11_CONTROL_STAGE_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_V012.json",
    ("A12_CONTROL_STAGE_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
    ("A13_L10_AUTHORIZATION", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
    ("A14_L10_HISTORY", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L10.json",
    ("A15_L10_STAGE_GATE", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
    ("A16_L10_STAGE_AUDIT", 1): "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json",
    ("A18_L10_CROSS_GATE", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_HOSTILE_L10_CROSS_GATE_V001.json",
    ("A20_SHARED_SCHEDULE_GATE", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_V001.json",
    ("A21_SHARED_SCHEDULE_AUDIT", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/TARGET_L12_EXECUTION_GATE_V012.json",
    ("A22_TARGET_L12_AUTHORIZATION", 2): "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json",
    ("A22_TARGET_L12_AUTHORIZATION", 3): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_READY_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 4): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_READY_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 5): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_LAUNCH_HANDSHAKE_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 6): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_WORKER_RELEASE_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 7): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_COMMAND_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 8): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 9): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_ACK_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 10): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 11): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_COMPLETION_V001.json",
    ("A22_TARGET_L12_AUTHORIZATION", 12): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_COMPLETION_V001.json",
    ("A23_POSTRUN_TELEMETRY", 1): "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json",
    ("A24_TARGET_L12_HISTORY", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json",
    ("A25_HOSTILE_L12_HISTORY", 1): "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json",
    ("A27_MUTATION_LEDGER", 1): "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_MUTATION_LEDGER_V001.json",
}
for _instance, _length in enumerate((4, 6, 8, 10, 12), start=1):
    AUTHORITY_CANONICAL_SOURCES[("A05_FIVE_CACHE_SET", _instance)] = f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012/L{_length}/CACHE_MANIFEST.json"
for _instance, _length in enumerate((4, 6, 8), start=1):
    AUTHORITY_CANONICAL_SOURCES[("A10_CONTROL_HISTORIES", _instance)] = f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L{_length}.json"
AUDIT_IDENTITY_BY_L: Final[dict[int, tuple[str, str, int]]] = {
    4: (
        "SCALABLE_RELATIONAL_ACCUMULATION_SEED_HOSTILE_V001",
        "PASS_RELATIONAL_ACCUMULATION_SEED_L4_L8",
        205,
    ),
    6: (
        "SCALABLE_RELATIONAL_ACCUMULATION_SEED_HOSTILE_V001",
        "PASS_RELATIONAL_ACCUMULATION_SEED_L4_L8",
        205,
    ),
    8: (
        "SCALABLE_RELATIONAL_ACCUMULATION_SEED_HOSTILE_V001",
        "PASS_RELATIONAL_ACCUMULATION_SEED_L4_L8",
        205,
    ),
    10: (
        "L10_V002_MEMORY_REPAIR_HOSTILE_RESULT_V001",
        "PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_RESOURCE_BLOCKED",
        42,
    ),
    12: (
        "TARGET_V012_HOSTILE_V004R4_FINAL_L12_AUDIT_V001",
        "PASS_FINITE_L12_TARGET_HOSTILE_ACCUMULATION",
        119,
    ),
}
A26_CHECKS: Final[dict[str, int]] = {
    "postrun_telemetry": 1,
    "complete_l12_histories": 2,
    "terminal_shard_custody": 24,
    "basis_permutation_projections": 24,
    "terminal_numerical_comparisons": 12,
    "native_history_field_projections": 13,
    "transitive_authorization_bindings": 42,
    "independent_auditor_isolation": 1,
}


class ManifestRefusal(RuntimeError):
    """An input, reconstruction, or publication contract failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(16 * 2**20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def valid_sha256(value: object) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise ManifestRefusal("manifest is noncanonical or nonfinite") from error


def _reject_constant(value: str) -> object:
    raise ManifestRefusal(f"nonfinite JSON constant: {value}")


def _object_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ManifestRefusal(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _checked_repo_file(
    repo_root: Path, relative: str, expected_sha256: str, label: str,
) -> tuple[Path, bytes]:
    if (
        type(relative) is not str or not relative
        or Path(relative).is_absolute() or ".." in Path(relative).parts
        or not valid_sha256(expected_sha256)
    ):
        raise ManifestRefusal(f"{label} path/hash is malformed")
    path = repo_root / relative
    current = repo_root.resolve()
    for part in Path(relative).parts[:-1]:
        current /= part
        try:
            parent_metadata = os.stat(current, follow_symlinks=False)
        except OSError as error:
            raise ManifestRefusal(f"{label} parent is absent") from error
        if stat.S_ISLNK(parent_metadata.st_mode) or not stat.S_ISDIR(
            parent_metadata.st_mode
        ):
            raise ManifestRefusal(f"{label} parent is aliased or special")
    try:
        before = os.stat(path, follow_symlinks=False)
    except OSError as error:
        raise ManifestRefusal(f"{label} is absent") from error
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode):
        raise ManifestRefusal(f"{label} is aliased or special")
    if before.st_size > MAX_SOURCE_BYTES:
        raise ManifestRefusal(f"{label} exceeds the source byte guard")
    resolved_root = repo_root.resolve()
    resolved = path.resolve(strict=True)
    if resolved_root not in resolved.parents:
        raise ManifestRefusal(f"{label} escapes the repository")
    raw = path.read_bytes()
    after = os.stat(path, follow_symlinks=False)
    identity = lambda item: (
        item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns,
        item.st_ctime_ns, item.st_nlink, item.st_mode,
    )
    if (
        identity(before) != identity(after)
        or hashlib.sha256(raw).hexdigest() != expected_sha256
    ):
        raise ManifestRefusal(f"{label} changed or has the wrong SHA-256")
    return resolved, raw


def _load_history(
    repo_root: Path, relative: str, digest: str, label: str,
) -> dict[str, object]:
    _path, raw = _checked_repo_file(repo_root, relative, digest, label)
    try:
        record = json.loads(
            raw,
            object_pairs_hook=_object_no_duplicates,
            parse_float=Decimal,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ManifestRefusal(f"{label} JSON is malformed") from error
    if type(record) is not dict:
        raise ManifestRefusal(f"{label} is not a JSON object")
    return record


def _validate_complete_a26_authorities(
    audit: dict[str, object], source: dict[str, str], repo_root: Path,
) -> None:
    """Authenticate every logical A26 authority and all A17 physical inputs."""
    bindings = audit.get("authority_bindings")
    expected_logical = sum(AUTHORITY_INSTANCE_CENSUS.values())
    if (
        expected_logical != 42
        or type(bindings) is not list
        or len(bindings) != expected_logical
        or audit.get("checks") != A26_CHECKS
        or sum(A26_CHECKS.values()) != 119
    ):
        raise ManifestRefusal("L12 hostile audit complete authority census mismatch")
    by_identity: dict[tuple[str, int], dict[str, object]] = {}
    for binding in bindings:
        if (
            type(binding) is not dict
            or type(binding.get("artifact_id")) is not str
            or type(binding.get("instance")) is not int
        ):
            raise ManifestRefusal("L12 hostile audit authority identity malformed")
        identity = (binding["artifact_id"], binding["instance"])
        if identity in by_identity:
            raise ManifestRefusal("L12 hostile audit authority identity duplicated")
        by_identity[identity] = binding
    expected_identities = {
        (artifact_id, instance)
        for artifact_id, count in AUTHORITY_INSTANCE_CENSUS.items()
        for instance in range(1, count + 1)
    }
    if set(by_identity) != expected_identities:
        raise ManifestRefusal("L12 hostile audit authority identity census mismatch")

    for identity, relative in AUTHORITY_CANONICAL_SOURCES.items():
        binding = by_identity[identity]
        expected_path = str((repo_root / relative).resolve())
        if (
            set(binding) != {"artifact_id", "instance", "path", "sha256"}
            or binding.get("path") != expected_path
            or not valid_sha256(binding.get("sha256"))
        ):
            raise ManifestRefusal(
                f"L12 hostile audit {identity[0]}:{identity[1]} binding mismatch"
            )
        _checked_repo_file(
            repo_root, relative, str(binding["sha256"]),
            f"L12 authority {identity[0]}:{identity[1]}",
        )

    a17 = by_identity[("A17_HOSTILE_L12_ELIGIBILITY", 1)]
    if set(a17) != {"artifact_id", "instance", "sources", "sha256"}:
        raise ManifestRefusal("L12 hostile audit A17 binding key census mismatch")
    sources = a17.get("sources")
    if type(sources) is not list or len(sources) != len(A17_SOURCE_LABELS):
        raise ManifestRefusal("L12 hostile audit A17 physical-source census mismatch")
    branch: dict[str, object] = {"role": "hostile_v004r4"}
    for label, binding in zip(A17_SOURCE_LABELS, sources):
        relative = A17_CANONICAL_SOURCES[label]
        expected_path = str((repo_root / relative).resolve())
        if (
            type(binding) is not dict
            or set(binding) != {"label", "path", "sha256"}
            or binding.get("label") != label
            or binding.get("path") != expected_path
            or not valid_sha256(binding.get("sha256"))
        ):
            raise ManifestRefusal(f"L12 hostile audit A17 {label} binding mismatch")
        _path, raw = _checked_repo_file(
            repo_root, relative, str(binding["sha256"]),
            f"L12 A17 physical source {label}",
        )
        branch_binding: dict[str, object] = {
            "path": expected_path,
            "sha256": binding["sha256"],
        }
        if label in A17_RECORD_IDENTITIES:
            try:
                record = json.loads(
                    raw,
                    object_pairs_hook=_object_no_duplicates,
                    parse_float=Decimal,
                    parse_constant=_reject_constant,
                )
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
                raise ManifestRefusal(f"L12 A17 {label} JSON malformed") from error
            schema, field, value = A17_RECORD_IDENTITIES[label]
            if type(record) is not dict or record.get("schema") != schema or record.get(field) != value:
                raise ManifestRefusal(f"L12 A17 {label} identity mismatch")
            branch_binding.update({
                "schema": schema,
                "identity_field": field,
                "identity_value": value,
            })
        branch[label] = branch_binding
    composite = hashlib.sha256(canonical_json_bytes(branch)).hexdigest()
    if a17.get("sha256") != composite:
        raise ManifestRefusal("L12 hostile audit A17 composite mismatch")

    if (
        by_identity[("A24_TARGET_L12_HISTORY", 1)].get("sha256")
        != source["target_sha256"]
        or by_identity[("A25_HOSTILE_L12_HISTORY", 1)].get("sha256")
        != source["blind_sha256"]
    ):
        raise ManifestRefusal("L12 hostile audit history authority mismatch")


def _validate_stage2_lineage(
    chosen: dict[int, tuple[dict[str, object], dict[str, object]]],
    lineage_sources: dict[str, dict[str, str]], repo_root: Path,
) -> dict[str, object]:
    required = {
        "target_L4", "target_L6", "target_L8", "target_L10", "hostile_L10",
        "control_audit", "l10_audit", "a18_cross_gate",
    }
    if type(lineage_sources) is not dict or set(lineage_sources) != required:
        raise ManifestRefusal("Stage2 lineage source census mismatch")
    loaded: dict[str, dict[str, object]] = {}
    for label in sorted(required):
        binding = lineage_sources[label]
        expected_path = STAGE2_LINEAGE_SOURCES[label]["path"]
        if (
            type(binding) is not dict or set(binding) != {"path", "sha256"}
            or binding.get("path") != expected_path
            or not valid_sha256(binding.get("sha256"))
        ):
            raise ManifestRefusal(f"Stage2 {label} binding mismatch")
        loaded[label] = _load_history(
            repo_root, expected_path, str(binding["sha256"]), f"Stage2 {label}",
        )

    control_audit = loaded["control_audit"]
    expected_controls = {
        str(length): lineage_sources[f"target_L{length}"]["sha256"]
        for length in (4, 6, 8)
    }
    if (
        control_audit.get("schema") != "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001"
        or control_audit.get("classification") != "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8"
        or control_audit.get("checks_passed") != 47
        or control_audit.get("checks_total") != 47
        or control_audit.get("failures") != []
        or control_audit.get("history_sha256_by_L") != expected_controls
    ):
        raise ManifestRefusal("Stage2 L4-L8 audit lineage mismatch")
    l10_audit = loaded["l10_audit"]
    if (
        l10_audit.get("schema") != "TARGET_V012_CACHED_L10_GATE_AUDIT_V001"
        or l10_audit.get("classification") != "PASS_INDEPENDENT_TARGET_V012_CACHED_L10"
        or l10_audit.get("checks_passed") != 25
        or l10_audit.get("checks_total") != 25
        or l10_audit.get("failures") != []
        or l10_audit.get("history_sha256_by_L")
        != {"10": lineage_sources["target_L10"]["sha256"]}
    ):
        raise ManifestRefusal("Stage2 L10 audit lineage mismatch")
    a18 = loaded["a18_cross_gate"]
    if (
        a18.get("schema") != "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001"
        or a18.get("classification") != "PASS_EXACT_TARGET_HOSTILE_L10_CROSS_BENCHMARK"
        or a18.get("checks_passed") != 65
        or a18.get("checks_total") != 65
        or a18.get("failures") != []
        or type(a18.get("target")) is not dict
        or type(a18.get("hostile")) is not dict
        or a18["target"].get("history_sha256")
        != lineage_sources["target_L10"]["sha256"]
        or a18["hostile"].get("history_sha256")
        != lineage_sources["hostile_L10"]["sha256"]
    ):
        raise ManifestRefusal("Stage2 A18 benchmark lineage mismatch")

    differences: dict[str, object] = {}
    for length in (4, 6, 8, 10):
        sector, observable = _history_differences(
            chosen[length][0], loaded[f"target_L{length}"], length,
        )
        if sector > 1.0e-8 or observable > 1.0e-8:
            raise ManifestRefusal(f"Stage2 L{length} chosen-target bridge mismatch")
        differences[str(length)] = {
            "max_sector_weight_difference": sector,
            "max_history_observable_difference": observable,
        }
    sector, observable = _history_differences(
        chosen[10][1], loaded["hostile_L10"], 10,
    )
    if sector > 1.0e-8 or observable > 1.0e-8:
        raise ManifestRefusal("Stage2 hostile L10 chosen-history bridge mismatch")
    differences["hostile_L10"] = {
        "max_sector_weight_difference": sector,
        "max_history_observable_difference": observable,
    }
    return {
        "policy": "AUDITED_SCALABLE_L4_L10_HISTORIES_BRIDGED_TO_CURRENT_STAGE2_AND_A18",
        "authorities": lineage_sources,
        "chosen_history_comparisons": differences,
        "tolerance": 1.0e-8,
    }


def _validate_hostile_audit(
    audit: dict[str, object], length: int, source: dict[str, str],
    repo_root: Path,
) -> None:
    schema, classification, checks_total = AUDIT_IDENTITY_BY_L[length]
    if (
        audit.get("schema") != schema
        or audit.get("classification") != classification
        or type(audit.get("checks_total")) is not int
        or audit["checks_total"] != checks_total
        or type(audit.get("checks_passed")) is not int
        or audit["checks_passed"] != audit["checks_total"]
        or audit.get("failures") != []
    ):
        raise ManifestRefusal(
            f"L{length} hostile audit identity/result mismatch"
        )
    if length in {4, 6, 8}:
        registered = {"4", "6", "8"}
        target_hashes = audit.get("target_hashes")
        blind_hashes = audit.get("blind_hashes")
        if (
            type(target_hashes) is not dict
            or type(blind_hashes) is not dict
            or set(target_hashes) != registered
            or set(blind_hashes) != registered
            or any(not valid_sha256(value) for value in target_hashes.values())
            or any(not valid_sha256(value) for value in blind_hashes.values())
            or target_hashes[str(length)] != source["target_sha256"]
            or blind_hashes[str(length)] != source["blind_sha256"]
        ):
            raise ManifestRefusal(
                f"L{length} hostile audit history binding mismatch"
            )
        return
    if length == 10:
        if (
            audit.get("target_sha256") != source["target_sha256"]
            or audit.get("blind_sha256") != source["blind_sha256"]
            or not valid_sha256(audit.get("target_sha256"))
            or not valid_sha256(audit.get("blind_sha256"))
        ):
            raise ManifestRefusal(
                "L10 hostile audit history binding mismatch"
            )
        return
    if (
        audit.get("auditor_role") != "INDEPENDENT_FINAL_L12_AUDITOR"
        or type(audit.get("authority_records_authenticated")) is not int
        or audit["authority_records_authenticated"] != 42
    ):
        raise ManifestRefusal("L12 hostile audit authority census mismatch")
    _validate_complete_a26_authorities(audit, source, repo_root)


def _event_rows(history: dict[str, object], length: int) -> list[dict[str, object]]:
    if type(history.get("L")) is not int or history["L"] != length:
        raise ManifestRefusal(f"L{length} history size mismatch")
    comparison = history.get("comparison")
    rows = history.get("rows")
    if type(comparison) is not dict or comparison.get("resolved") is not True:
        raise ManifestRefusal(f"L{length} history is unresolved")
    if type(rows) is not list or len(rows) != length:
        raise ManifestRefusal(f"L{length} event census mismatch")
    by_event: dict[int, dict[str, object]] = {}
    for row in rows:
        if type(row) is not dict or type(row.get("event")) is not int:
            raise ManifestRefusal(f"L{length} event identifier is invalid")
        if row["event"] in by_event:
            raise ManifestRefusal(f"L{length} event identifier is duplicated")
        by_event[row["event"]] = row
    if set(by_event) != set(range(1, length + 1)):
        raise ManifestRefusal(f"L{length} events are not exactly 1..L")
    return [by_event[event] for event in range(1, length + 1)]


def _finite_number(value: object, label: str) -> float:
    if type(value) not in (int, float, Decimal) or not math.isfinite(float(value)):
        raise ManifestRefusal(f"{label} is not a finite JSON number")
    return float(value)


def _exact_numeric_zero(value: object) -> bool:
    if type(value) is Decimal:
        return value.is_finite() and value == 0
    return (
        type(value) in (int, float)
        and math.isfinite(float(value))
        and float(value) == 0.0
    )


def _weight_matrix(
    history: dict[str, object], length: int,
) -> list[list[float]]:
    matrix: list[list[float]] = []
    for event, row in enumerate(_event_rows(history, length), start=1):
        weights = row.get("sector_weights")
        if type(weights) is not list or len(weights) not in (
            length + 1, 2 * length + 1,
        ):
            raise ManifestRefusal(
                f"L{length} invalid sector-weight vector length at event {event}"
            )
        if len(weights) == 2 * length + 1:
            tail = weights[length + 1:]
            if any(not _exact_numeric_zero(value) for value in tail):
                raise ManifestRefusal(
                    f"L{length} nonzero or invalid q>L sector-weight tail "
                    f"at event {event}"
                )
            weights = weights[:length + 1]
        normalized = [
            _finite_number(value, f"L{length} event {event} sector weight")
            for value in weights
        ]
        if any(value < -1.0e-12 for value in normalized):
            raise ManifestRefusal(f"L{length} has a negative sector weight")
        if abs(sum(normalized) - 1.0) > 1.0e-9:
            raise ManifestRefusal(f"L{length} sector weights are not normalized")
        matrix.append(normalized)
    return matrix


def _pbar(history: dict[str, object], length: int) -> list[float]:
    late = _weight_matrix(history, length)[math.ceil(length / 2) - 1:]
    result = [
        sum(row[charge] for row in late) / len(late)
        for charge in range(length + 1)
    ]
    if abs(sum(result) - 1.0) > 1.0e-9:
        raise ManifestRefusal(f"L{length} late-history pbar is not normalized")
    return result


def _shortest_interval(weights: list[float]) -> tuple[int, int]:
    candidates: list[tuple[int, float, int, int]] = []
    for lower in range(len(weights)):
        mass = 0.0
        for upper in range(lower, len(weights)):
            mass += weights[upper]
            if mass >= 0.99:
                candidates.append((upper - lower, -mass, lower, upper))
    if not candidates:
        raise ManifestRefusal("no contiguous 99-percent sector interval")
    _width, _negative_mass, lower, upper = min(candidates)
    return lower, upper


def _density_envelope(
    length: int, lower: int, upper: int,
) -> tuple[Fraction, Fraction]:
    return (
        max(Fraction(0), Fraction(2 * lower - 1, 4 * length)),
        min(Fraction(1), Fraction(2 * upper + 1, 4 * length)),
    )


def _ratio(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def _q_at_density(length: int, density: Fraction) -> int:
    shifted = 2 * length * density + Fraction(1, 2)
    return min(length, max(0, shifted.numerator // shifted.denominator))


def _atoms(common: tuple[Fraction, Fraction]) -> list[dict[str, object]]:
    if common[0] >= common[1]:
        raise ManifestRefusal("L4-L12 accumulation intersection is empty")
    boundaries = {common[0], common[1]}
    for length in SIZES:
        for charge in range(length):
            boundary = Fraction(2 * charge + 1, 4 * length)
            if common[0] < boundary < common[1]:
                boundaries.add(boundary)
    ordered = sorted(boundaries)
    return [
        {
            "atom_id": f"A{index:03d}",
            "density_interval": [_ratio(left), _ratio(right)],
            "q_by_L": {
                str(length): _q_at_density(length, (left + right) / 2)
                for length in SIZES
            },
        }
        for index, (left, right) in enumerate(zip(ordered, ordered[1:]))
    ]


def _history_differences(
    target: dict[str, object], blind: dict[str, object], length: int,
) -> tuple[float, float]:
    target_rows = _event_rows(target, length)
    blind_rows = _event_rows(blind, length)
    target_weights = _weight_matrix(target, length)
    blind_weights = _weight_matrix(blind, length)
    sector = max(
        abs(target_weights[event][charge] - blind_weights[event][charge])
        for event in range(length)
        for charge in range(length + 1)
    )
    observable = 0.0
    for event, (left, right) in enumerate(
        zip(target_rows, blind_rows), start=1,
    ):
        for field in OBSERVABLE_FIELDS:
            observable = max(
                observable,
                abs(
                    _finite_number(left.get(field), f"target {field} event {event}")
                    - _finite_number(right.get(field), f"blind {field} event {event}")
                ),
            )
    return sector, observable


def build_manifest(
    sources: dict[int, dict[str, str]],
    lineage_sources: dict[str, dict[str, str]],
    repo_root: Path = ROOT,
) -> dict[str, object]:
    protocol = repo_root / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md"
    if not protocol.is_file() or sha256_file(protocol) != PROTOCOL_SHA256:
        raise ManifestRefusal("scalable accumulation protocol custody mismatch")
    if set(sources) != set(SIZES):
        raise ManifestRefusal("source size census must be exactly L4-L12")
    histories: dict[str, object] = {}
    chosen_histories: dict[int, tuple[dict[str, object], dict[str, object]]] = {}
    envelopes: dict[int, tuple[Fraction, Fraction]] = {}
    for length in SIZES:
        source = sources[length]
        required = {
            "target_path", "target_sha256", "blind_path", "blind_sha256",
            "audit_path", "audit_sha256",
        }
        if type(source) is not dict or set(source) != required:
            raise ManifestRefusal(f"L{length} source key census mismatch")
        canonical = CANONICAL_SOURCES[length]
        if any(
            source[f"{kind}_path"] != canonical[kind]
            for kind in ("target", "blind", "audit")
        ):
            raise ManifestRefusal(f"L{length} canonical source path mismatch")
        target = _load_history(
            repo_root, source["target_path"], source["target_sha256"],
            f"L{length} target history",
        )
        blind = _load_history(
            repo_root, source["blind_path"], source["blind_sha256"],
            f"L{length} blind history",
        )
        if (
            type(target.get("dimension")) is not int
            or target["dimension"] <= 0
            or target["dimension"] != blind.get("dimension")
        ):
            raise ManifestRefusal(f"L{length} target/blind dimension mismatch")
        audit = _load_history(
            repo_root, source["audit_path"], source["audit_sha256"],
            f"L{length} hostile audit",
        )
        _validate_hostile_audit(audit, length, source, repo_root)
        chosen_histories[length] = (target, blind)
        sector_difference, observable_difference = _history_differences(
            target, blind, length,
        )
        if sector_difference > 1.0e-8 or observable_difference > 1.0e-8:
            raise ManifestRefusal(f"L{length} target/blind tolerance exceeded")
        target_pbar = _pbar(target, length)
        blind_pbar = _pbar(blind, length)
        interval = _shortest_interval(target_pbar)
        if _shortest_interval(blind_pbar) != interval:
            raise ManifestRefusal(f"L{length} target/blind intervals differ")
        envelope = _density_envelope(length, *interval)
        envelopes[length] = envelope
        histories[str(length)] = {
            "target_history_path": source["target_path"],
            "target_history_sha256": source["target_sha256"],
            "blind_history_path": source["blind_path"],
            "blind_history_sha256": source["blind_sha256"],
            "hostile_audit_path": source["audit_path"],
            "hostile_audit_sha256": source["audit_sha256"],
            "hostile_verdict": "PASS",
            "max_target_blind_sector_weight_difference": sector_difference,
            "max_target_blind_history_observable_difference": observable_difference,
            "pbar_q": target_pbar,
            "q_interval": list(interval),
            "density_envelope": [_ratio(envelope[0]), _ratio(envelope[1])],
        }
    common = (
        max(envelope[0] for envelope in envelopes.values()),
        min(envelope[1] for envelope in envelopes.values()),
    )
    atoms = _atoms(common)
    if not atoms:
        raise ManifestRefusal("complete positive-width atom partition is empty")
    stage2_lineage = _validate_stage2_lineage(
        chosen_histories, lineage_sources, repo_root,
    )
    return {
        "schema": SCHEMA,
        "status": STATUS,
        # Both frozen consumers require the same protocol under different
        # historical field names.  Carrying both exact bindings weakens neither.
        "accumulation_protocol_sha256": PROTOCOL_SHA256,
        "scalable_accumulation_protocol_sha256": PROTOCOL_SHA256,
        "histories": histories,
        "stage2_benchmark_lineage": stage2_lineage,
        "I_acc": [_ratio(common[0]), _ratio(common[1])],
        "atoms": atoms,
        "claim_boundary": (
            "FINITE_AUTHENTICATED_L4_L12_ACCUMULATION_SECTOR_ONLY__NO_"
            "SPECTRUM_Z1_CONTINUUM_EMERGENCE_OR_GRAVITY"
        ),
    }


def publish_once(output: Path, manifest: dict[str, object]) -> str:
    payload = canonical_json_bytes(manifest)
    if len(payload) > MAX_MANIFEST_BYTES:
        raise ManifestRefusal("manifest exceeds the output byte guard")
    output = Path(os.path.abspath(output))
    if output.parent.resolve() != output.parent:
        raise ManifestRefusal("manifest output parent is aliased")
    if ROOT.resolve() not in output.parents:
        raise ManifestRefusal("manifest output must remain repository-local")
    try:
        os.stat(output, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        raise ManifestRefusal("manifest output already exists")
    if not output.parent.is_dir():
        raise ManifestRefusal("manifest output parent is absent")
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(output.parent, parent_flags)
    except OSError as error:
        raise ManifestRefusal("manifest output parent is aliased") from error
    descriptor = -1
    staging_name = (
        f".{output.name}.staging-{os.getpid()}-{os.urandom(12).hex()}"
    )
    linked = False
    try:
        descriptor = os.open(
            staging_name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400,
            dir_fd=parent_descriptor,
        )
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            if written <= 0:
                raise ManifestRefusal("short manifest write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        metadata = os.fstat(descriptor)
        expected = hashlib.sha256(payload).hexdigest()
        if (
            not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o222
            or metadata.st_nlink != 1 or metadata.st_size != len(payload)
            or hashlib.sha256(os.pread(descriptor, len(payload), 0)).hexdigest()
            != expected
        ):
            raise ManifestRefusal("manifest staging custody mismatch")
        try:
            os.link(
                staging_name,
                output.name,
                src_dir_fd=parent_descriptor,
                dst_dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileExistsError as error:
            raise ManifestRefusal("manifest output already exists") from error
        linked = True
        os.unlink(staging_name, dir_fd=parent_descriptor)
        os.fsync(parent_descriptor)
        verified = os.stat(
            output.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(verified.st_mode) or verified.st_mode & 0o222
            or verified.st_nlink != 1 or verified.st_size != len(payload)
            or sha256_file(output) != expected
        ):
            raise ManifestRefusal("published manifest custody mismatch")
        return expected
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if not linked:
            try:
                os.unlink(staging_name, dir_fd=parent_descriptor)
            except FileNotFoundError:
                pass
        os.close(parent_descriptor)


def _source_arguments(arguments: argparse.Namespace) -> dict[int, dict[str, str]]:
    result: dict[int, dict[str, str]] = {}
    for length in SIZES:
        paths = CANONICAL_SOURCES[length]
        result[length] = {
            "target_path": paths["target"],
            "target_sha256": getattr(arguments, f"target_l{length}_sha256"),
            "blind_path": paths["blind"],
            "blind_sha256": getattr(arguments, f"blind_l{length}_sha256"),
            "audit_path": paths["audit"],
            "audit_sha256": getattr(arguments, f"audit_l{length}_sha256"),
        }
    return result


def _lineage_arguments(
    arguments: argparse.Namespace,
) -> dict[str, dict[str, str]]:
    return {
        label: {
            "path": binding["path"],
            "sha256": getattr(arguments, f"stage2_{label}_sha256"),
        }
        for label, binding in STAGE2_LINEAGE_SOURCES.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", required=True)
    for length in SIZES:
        parser.add_argument(f"--target-l{length}-sha256", required=True)
        parser.add_argument(f"--blind-l{length}-sha256", required=True)
        parser.add_argument(f"--audit-l{length}-sha256", required=True)
    for label in STAGE2_LINEAGE_SOURCES:
        parser.add_argument(
            f"--stage2-{label.replace('_', '-')}-sha256", required=True,
        )
    args = parser.parse_args()
    if args.authorization != BUILD_TOKEN:
        print("REFUSED: literal manifest build token missing", file=sys.stderr)
        return 2
    if CANONICAL_OUTPUT.exists():
        print("REFUSED: canonical manifest already exists", file=sys.stderr)
        return 2
    try:
        manifest = build_manifest(
            _source_arguments(args), _lineage_arguments(args), ROOT,
        )
        digest = publish_once(CANONICAL_OUTPUT, manifest)
    except (ManifestRefusal, OSError, ValueError, MemoryError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": STATUS,
        "sha256": digest,
        "sizes": list(SIZES),
        "atoms": len(manifest["atoms"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
