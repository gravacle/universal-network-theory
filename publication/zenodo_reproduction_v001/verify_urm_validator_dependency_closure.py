#!/usr/bin/env python3
"""Fail-closed byte verifier for the packaged URM-validator dependency closure.

The verifier reads only the closure specification and dependency bytes.  It
does not import a model module, invoke a validator, or execute physics code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from typing import Any


SCHEMA = "wac_urm_validator_dependency_closure_v001"
DEFAULT_SPEC_NAME = "urm_validator_dependency_closure.json"
EXTRACTED_SPEC = "inventory/URM_VALIDATOR_DEPENDENCY_CLOSURE.json"
SHA256 = re.compile(r"[0-9a-f]{64}")
ENTRY_KEYS = {
    "archive_path",
    "kind",
    "repository_path",
    "required_by",
    "sha256",
    "size_bytes",
}
RUNTIME_KEYS = {
    "archive_path",
    "repository_path",
    "required_by",
    "role",
    "sha256",
    "size_bytes",
}
VALIDATOR_KEYS = {
    "dependency_count",
    "dependency_total_bytes",
    "entrypoint",
    "id",
    "repository_entrypoint",
    "urm_methods_exercised",
}
CONFLICT_KEYS = {
    "affected_validators",
    "exact_archive_path",
    "exact_repository_path",
    "exact_sha256",
    "exact_size_bytes",
    "existing_public_archive_path",
    "path_rewrites",
    "public_substitute_repository_path",
    "public_substitute_sha256",
    "public_substitute_size_bytes",
    "status",
}
TOP_LEVEL_KEYS = {
    "archive_dependency_root",
    "closure_entry_count",
    "closure_total_bytes",
    "entries",
    "external_imports",
    "generation_policy",
    "runtime_artifact_count",
    "runtime_artifact_total_bytes",
    "runtime_artifacts",
    "sanitized_conflict_count",
    "sanitized_conflicts",
    "schema",
    "validators",
}
KINDS = {
    "custody_data",
    "custody_hash_list",
    "custody_seal",
    "model_source",
    "validator_source",
}
CONFLICT_STATUS = (
    "PUBLIC_PROJECTION_AUTHENTICATES_EXACT_SOURCE_PIN__"
    "RAW_PATH_BEARING_BYTES_OMITTED"
)
PUBLIC_PROJECTION_PATHS = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
    "CACHE_PAYLOADS_V012/L8/CACHE_MANIFEST.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
    "CACHE_PAYLOADS_V012/L10/CACHE_MANIFEST.json",
    "model/relational_accumulation.py",
}


class ClosureVerificationError(RuntimeError):
    """The specification or proposed extracted dependency root failed closed."""


def _exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    observed = set(value)
    if observed != expected:
        raise ClosureVerificationError(
            f"{context} keys differ: missing={sorted(expected - observed)}, "
            f"unexpected={sorted(observed - expected)}"
        )


def _safe_relative(value: Any, context: str) -> str:
    if not isinstance(value, str):
        raise ClosureVerificationError(f"{context} path is not a string")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or "." in path.parts
        or ".." in path.parts
        or "\\" in value
        or path.as_posix() != value
    ):
        raise ClosureVerificationError(f"unsafe or non-canonical {context} path: {value!r}")
    return value


def _nonnegative_int(value: Any, context: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ClosureVerificationError(f"{context} is not a nonnegative integer")
    return value


def _hash(value: Any, context: str) -> str:
    if not isinstance(value, str) or SHA256.fullmatch(value) is None:
        raise ClosureVerificationError(f"{context} is not a lowercase SHA-256")
    return value


def _string_list(value: Any, context: str, *, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        raise ClosureVerificationError(f"{context} is not a valid string list")
    if not all(isinstance(item, str) and item for item in value):
        raise ClosureVerificationError(f"{context} contains a non-string or empty item")
    if value != sorted(set(value)):
        raise ClosureVerificationError(f"{context} must be sorted and duplicate-free")
    return value


def load_and_validate_spec(spec_path: Path) -> dict[str, Any]:
    try:
        raw = spec_path.read_bytes()
    except OSError as exc:
        raise ClosureVerificationError(f"cannot read closure spec {spec_path}: {exc}") from exc
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClosureVerificationError(f"closure spec is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ClosureVerificationError("closure spec root is not an object")
    _exact_keys(value, TOP_LEVEL_KEYS, "spec")
    if value["schema"] != SCHEMA:
        raise ClosureVerificationError(f"unsupported closure schema: {value['schema']!r}")
    if value["archive_dependency_root"] != "urm":
        raise ClosureVerificationError("archive dependency root must remain exactly 'urm'")
    if value["generation_policy"] != (
        "HASH_PINNED_REPOSITORY_EXACT_CLOSURE__NO_NUMERICAL_VALIDATOR_OR_"
        "PHYSICS_EXECUTION"
    ):
        raise ClosureVerificationError("unexpected generation policy")
    if value["external_imports"] != ["numpy"]:
        raise ClosureVerificationError("external import surface changed")

    validators = value["validators"]
    if not isinstance(validators, list) or not validators:
        raise ClosureVerificationError("validators must be a nonempty list")
    validator_ids: list[str] = []
    validator_by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(validators):
        if not isinstance(row, dict):
            raise ClosureVerificationError(f"validator[{index}] is not an object")
        _exact_keys(row, VALIDATOR_KEYS, f"validator[{index}]")
        validator_id = row["id"]
        if not isinstance(validator_id, str) or not validator_id:
            raise ClosureVerificationError(f"validator[{index}] has invalid id")
        validator_ids.append(validator_id)
        validator_by_id[validator_id] = row
        _safe_relative(row["entrypoint"], f"validator[{index}] entrypoint")
        _safe_relative(
            row["repository_entrypoint"], f"validator[{index}] repository_entrypoint"
        )
        if row["entrypoint"] != f"urm/{row['repository_entrypoint']}":
            raise ClosureVerificationError(f"validator[{index}] entrypoint layout changed")
        _string_list(row["urm_methods_exercised"], f"validator[{index}] URM methods")
        _nonnegative_int(row["dependency_count"], f"validator[{index}] dependency_count")
        _nonnegative_int(
            row["dependency_total_bytes"],
            f"validator[{index}] dependency_total_bytes",
        )
    if validator_ids != sorted(set(validator_ids)):
        raise ClosureVerificationError("validator ids must be sorted and duplicate-free")
    validator_id_set = set(validator_ids)

    entries = value["entries"]
    if not isinstance(entries, list) or not entries:
        raise ClosureVerificationError("entries must be a nonempty list")
    repository_paths: list[str] = []
    archive_paths: set[str] = set()
    entry_by_repository: dict[str, dict[str, Any]] = {}
    computed_by_validator: dict[str, list[dict[str, Any]]] = {
        validator_id: [] for validator_id in validator_ids
    }
    for index, row in enumerate(entries):
        if not isinstance(row, dict):
            raise ClosureVerificationError(f"entry[{index}] is not an object")
        _exact_keys(row, ENTRY_KEYS, f"entry[{index}]")
        repository_path = _safe_relative(
            row["repository_path"], f"entry[{index}] repository"
        )
        archive_path = _safe_relative(row["archive_path"], f"entry[{index}] archive")
        if archive_path != f"urm/{repository_path}":
            raise ClosureVerificationError(
                f"entry[{index}] does not preserve repository-relative layout under urm"
            )
        if archive_path in archive_paths:
            raise ClosureVerificationError(f"duplicate archive path: {archive_path}")
        archive_paths.add(archive_path)
        repository_paths.append(repository_path)
        entry_by_repository[repository_path] = row
        if row["kind"] not in KINDS:
            raise ClosureVerificationError(f"entry[{index}] has unsupported kind")
        _hash(row["sha256"], f"entry[{index}] SHA-256")
        _nonnegative_int(row["size_bytes"], f"entry[{index}] size")
        required_by = _string_list(row["required_by"], f"entry[{index}] required_by")
        if not set(required_by) <= validator_id_set:
            raise ClosureVerificationError(f"entry[{index}] has unknown validator consumer")
        for validator_id in required_by:
            computed_by_validator[validator_id].append(row)
    if repository_paths != sorted(set(repository_paths)):
        raise ClosureVerificationError("repository entry paths must be sorted and duplicate-free")
    if value["closure_entry_count"] != len(entries):
        raise ClosureVerificationError("closure_entry_count mismatch")
    if value["closure_total_bytes"] != sum(row["size_bytes"] for row in entries):
        raise ClosureVerificationError("closure_total_bytes mismatch")
    for validator_id, rows in computed_by_validator.items():
        declared = validator_by_id[validator_id]
        if declared["dependency_count"] != len(rows):
            raise ClosureVerificationError(
                f"dependency_count mismatch for {validator_id}"
            )
        if declared["dependency_total_bytes"] != sum(row["size_bytes"] for row in rows):
            raise ClosureVerificationError(
                f"dependency_total_bytes mismatch for {validator_id}"
            )
        repository_entrypoint = declared["repository_entrypoint"]
        if repository_entrypoint not in entry_by_repository:
            raise ClosureVerificationError(f"entrypoint missing from closure: {validator_id}")
        entrypoint_row = entry_by_repository[repository_entrypoint]
        if (
            entrypoint_row["kind"] != "validator_source"
            or validator_id not in entrypoint_row["required_by"]
        ):
            raise ClosureVerificationError(f"entrypoint is not bound to {validator_id}")

    runtime = value["runtime_artifacts"]
    if not isinstance(runtime, list):
        raise ClosureVerificationError("runtime_artifacts must be a list")
    runtime_archive_paths: set[str] = set()
    runtime_repository_paths: set[str] = set()
    runtime_roles: set[str] = set()
    for index, row in enumerate(runtime):
        if not isinstance(row, dict):
            raise ClosureVerificationError(f"runtime[{index}] is not an object")
        _exact_keys(row, RUNTIME_KEYS, f"runtime[{index}]")
        repository_path = _safe_relative(
            row["repository_path"], f"runtime[{index}] repository"
        )
        archive_path = _safe_relative(row["archive_path"], f"runtime[{index}] archive")
        if repository_path in runtime_repository_paths or archive_path in runtime_archive_paths:
            raise ClosureVerificationError(f"duplicate runtime path at row {index}")
        runtime_repository_paths.add(repository_path)
        runtime_archive_paths.add(archive_path)
        role = row["role"]
        if not isinstance(role, str) or not role or role in runtime_roles:
            raise ClosureVerificationError(f"invalid or duplicate runtime role at row {index}")
        runtime_roles.add(role)
        _hash(row["sha256"], f"runtime[{index}] SHA-256")
        _nonnegative_int(row["size_bytes"], f"runtime[{index}] size")
        if _string_list(row["required_by"], f"runtime[{index}] required_by") != validator_ids:
            raise ClosureVerificationError(f"runtime[{index}] must bind all validators")
    if runtime_roles:
        raise ClosureVerificationError(
            "the focused closure must not embed a platform-specific runtime"
        )
    if value["runtime_artifact_count"] != len(runtime):
        raise ClosureVerificationError("runtime_artifact_count mismatch")
    if value["runtime_artifact_total_bytes"] != sum(
        row["size_bytes"] for row in runtime
    ):
        raise ClosureVerificationError("runtime_artifact_total_bytes mismatch")

    conflicts = value["sanitized_conflicts"]
    if not isinstance(conflicts, list):
        raise ClosureVerificationError("sanitized_conflicts is not a list")
    conflict_paths: list[str] = []
    for index, row in enumerate(conflicts):
        if not isinstance(row, dict):
            raise ClosureVerificationError(f"conflict[{index}] is not an object")
        _exact_keys(row, CONFLICT_KEYS, f"conflict[{index}]")
        exact_path = _safe_relative(
            row["exact_repository_path"], f"conflict[{index}] exact repository"
        )
        exact_archive = _safe_relative(
            row["exact_archive_path"], f"conflict[{index}] exact archive"
        )
        _safe_relative(
            row["existing_public_archive_path"],
            f"conflict[{index}] existing public archive",
        )
        _safe_relative(
            row["public_substitute_repository_path"],
            f"conflict[{index}] public substitute",
        )
        if exact_archive != f"urm/{exact_path}":
            raise ClosureVerificationError(f"conflict[{index}] exact layout changed")
        if row["existing_public_archive_path"] != exact_archive:
            raise ClosureVerificationError(
                f"conflict[{index}] must replace bytes at the exact archive path"
            )
        if exact_path not in entry_by_repository:
            raise ClosureVerificationError(f"conflict[{index}] exact entry is absent")
        exact_entry = entry_by_repository[exact_path]
        if (
            row["exact_sha256"] != exact_entry["sha256"]
            or row["exact_size_bytes"] != exact_entry["size_bytes"]
        ):
            raise ClosureVerificationError(f"conflict[{index}] exact pin mismatch")
        _hash(row["public_substitute_sha256"], f"conflict[{index}] substitute SHA-256")
        _nonnegative_int(
            row["public_substitute_size_bytes"], f"conflict[{index}] substitute size"
        )
        if _nonnegative_int(row["path_rewrites"], f"conflict[{index}] rewrites") == 0:
            raise ClosureVerificationError(f"conflict[{index}] has no declared path rewrite")
        affected = _string_list(
            row["affected_validators"], f"conflict[{index}] affected_validators"
        )
        if affected != exact_entry["required_by"]:
            raise ClosureVerificationError(f"conflict[{index}] consumer mismatch")
        if row["status"] != CONFLICT_STATUS:
            raise ClosureVerificationError(f"conflict[{index}] status changed")
        if row["public_substitute_sha256"] == row["exact_sha256"]:
            raise ClosureVerificationError(f"conflict[{index}] is not a byte conflict")
        conflict_paths.append(exact_path)
    if conflict_paths != sorted(set(conflict_paths)):
        raise ClosureVerificationError("sanitized conflicts must be sorted and duplicate-free")
    if value["sanitized_conflict_count"] != len(conflicts):
        raise ClosureVerificationError("sanitized_conflict_count mismatch")
    if set(conflict_paths) != PUBLIC_PROJECTION_PATHS:
        raise ClosureVerificationError(
            "focused URM public projection set changed"
        )
    return value


def _verify_file(path: Path, expected_size: int, expected_sha256: str, context: str) -> None:
    try:
        before = path.lstat()
    except OSError as exc:
        raise ClosureVerificationError(f"{context} is absent or unreadable: {path}: {exc}") from exc
    if not stat.S_ISREG(before.st_mode) or path.is_symlink():
        raise ClosureVerificationError(f"{context} is not a regular non-symlink file: {path}")
    try:
        raw = path.read_bytes()
        after = path.lstat()
    except OSError as exc:
        raise ClosureVerificationError(f"{context} cannot be read: {path}: {exc}") from exc
    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if identity_before != identity_after:
        raise ClosureVerificationError(f"{context} changed during verification: {path}")
    if len(raw) != expected_size:
        raise ClosureVerificationError(
            f"{context} size mismatch: {path}: expected {expected_size}, observed {len(raw)}"
        )
    observed = hashlib.sha256(raw).hexdigest()
    if observed != expected_sha256:
        raise ClosureVerificationError(
            f"{context} hash mismatch: {path}: expected {expected_sha256}, observed {observed}"
        )


def verify_root(spec: dict[str, Any], root: Path, layout: str) -> tuple[int, int]:
    if root.is_symlink() or not root.is_dir():
        raise ClosureVerificationError(f"verification root is not a non-symlink directory: {root}")
    root = root.resolve()
    public_archive = layout == "archive-public"
    path_field = "repository_path" if layout == "repository" else "archive_path"
    if public_archive:
        conflicts = spec.get("sanitized_conflicts", [])
        conflict_paths = {
            row["exact_repository_path"] for row in conflicts
        }
        rows = [
            row for row in spec["entries"] if row["repository_path"] not in conflict_paths
        ] + list(spec["runtime_artifacts"])
        for conflict in conflicts:
            rows.append(
                {
                    "archive_path": conflict["existing_public_archive_path"],
                    "repository_path": conflict["public_substitute_repository_path"],
                    "sha256": conflict["public_substitute_sha256"],
                    "size_bytes": conflict["public_substitute_size_bytes"],
                }
            )
    else:
        rows = list(spec["entries"]) + list(spec["runtime_artifacts"])
    verified_bytes = 0
    for index, row in enumerate(rows):
        relative = row[path_field]
        path = root.joinpath(*PurePosixPath(relative).parts)
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ClosureVerificationError(f"resolved dependency escapes root: {relative}") from exc
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError) as exc:
            raise ClosureVerificationError(
                f"dependency[{index}] resolves outside root or is absent: {relative}"
            ) from exc
        if resolved != path:
            raise ClosureVerificationError(
                f"dependency[{index}] traverses a symlinked path component: {relative}"
            )
        _verify_file(
            path,
            row["size_bytes"],
            row["sha256"],
            f"dependency[{index}]",
        )
        verified_bytes += row["size_bytes"]
    return len(rows), verified_bytes


def main(argv: list[str] | None = None) -> int:
    source_default = Path(__file__).resolve().with_name(DEFAULT_SPEC_NAME)
    extracted_default = Path(__file__).resolve().parents[1] / EXTRACTED_SPEC
    default_spec = source_default if source_default.is_file() else extracted_default
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument(
        "--layout",
        required=True,
        choices=("archive", "archive-public", "repository"),
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=default_spec,
    )
    args = parser.parse_args(argv)
    spec = load_and_validate_spec(args.spec)
    count, total = verify_root(spec, args.root, args.layout)
    spec_sha = hashlib.sha256(args.spec.read_bytes()).hexdigest()
    print(
        "URM_VALIDATOR_DEPENDENCY_CLOSURE_OK "
        f"layout={args.layout} files={count} bytes={total} spec_sha256={spec_sha}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ClosureVerificationError as exc:
        print(f"URM_VALIDATOR_DEPENDENCY_CLOSURE_REFUSAL {exc}", file=sys.stderr)
        raise SystemExit(2)
