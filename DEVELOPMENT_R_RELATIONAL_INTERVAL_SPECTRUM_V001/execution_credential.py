#!/usr/bin/env python3
"""Owner-once target-sector admission under the repository custody model.

This control proves ordering through the hash-pinned trusted code path.  It is
not a signature service and makes no adversary-resistant wall-clock claim.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import secrets
import stat
from decimal import Decimal
from pathlib import Path


CREDENTIAL_SCHEMA = "TARGET_INTERVAL_EXECUTION_CREDENTIAL_V001"
CREDENTIAL_STATUS = "AUTHORIZED_AFTER_BLIND_METHOD_AND_SECTOR_FREEZE"
BINDING_SCHEMA = "TARGET_INTERVAL_EXECUTION_BINDING_V001"
ORDERING_MODEL = "TRUSTED_HASH_PINNED_CODE_PATH__NO_WALL_CLOCK_ATTESTATION"
MANIFEST_SCHEMA = "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"
MANIFEST_STATUS = "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY"
PLAN_SCHEMA = "BLIND_RELATIONAL_INTERVAL_SECTOR_PLAN_V001"
PLAN_STATUS = "READY_FOR_PRE_TARGET_BLIND_METHOD_FREEZE"
BLIND_FREEZE_SCHEMA = "RELATIONAL_INTERVAL_BLIND_METHOD_FREEZE_V001"
BLIND_FREEZE_STATUS = "BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM"
SOURCE_FREEZE_SCHEMA = "RELATIONAL_INTERVAL_BLIND_COMPATIBILITY_SOURCE_FREEZE_V001"
SOURCE_FREEZE_STATUS = "CANDIDATE_SOURCES_FROZEN__NO_PHYSICAL_SPECTRUM_EXECUTED"
TARGET_FREEZE_SCHEMA = "RELATIONAL_INTERVAL_SPECTRUM_PRE_OUTPUT_FREEZE_V001"
TARGET_FREEZE_STATUS = "FROZEN_PRE_OUTPUT__NO_PHYSICAL_SPECTRUM_EXECUTED"
HEX = frozenset("0123456789abcdef")
IDENTITY_KEYS = {
    "path", "sha256", "device", "inode", "size", "mtime_ns", "ctime_ns",
    "mode", "nlink",
}


class CredentialRefusal(RuntimeError):
    """An authorization credential or one of its authorities failed closed."""


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise CredentialRefusal(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def valid_digest(value: object) -> bool:
    return type(value) is str and len(value) == 64 and set(value) <= HEX


def _reject_constant(value: str) -> object:
    raise CredentialRefusal(f"nonfinite JSON constant: {value}")


def _object_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        demand(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, label: str) -> dict[str, object]:
    try:
        value = json.loads(
            raw,
            object_pairs_hook=_object_no_duplicates,
            parse_float=Decimal,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise CredentialRefusal(f"{label}: invalid JSON") from error
    demand(type(value) is dict, f"{label}: top-level object required")
    return value


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (
            json.dumps(
                value, sort_keys=True, separators=(",", ":"),
                ensure_ascii=True, allow_nan=False,
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise CredentialRefusal("credential is not canonical JSON") from error


def _relative(root: Path, path: Path, label: str) -> str:
    resolved_root = root.resolve()
    resolved = path.resolve(strict=True)
    demand(resolved_root in resolved.parents, f"{label}: outside repository")
    return resolved.relative_to(resolved_root).as_posix()


def _identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_mode,
        metadata.st_nlink,
    )


def _read_authenticated_file(
    root: Path, path: Path, label: str,
) -> tuple[Path, dict[str, object], bytes]:
    root = root.resolve()
    path = Path(os.path.abspath(path))
    demand(root in path.parents, f"{label}: outside repository")
    current = root
    for part in path.relative_to(root).parts[:-1]:
        current /= part
        metadata = os.stat(current, follow_symlinks=False)
        demand(
            stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode),
            f"{label}: parent aliased or special",
        )
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor = os.open(path.parent, parent_flags)
    descriptor = -1
    try:
        parent_before = os.fstat(parent_descriptor)
        parent_named_before = os.stat(path.parent, follow_symlinks=False)
        demand(
            stat.S_ISDIR(parent_before.st_mode)
            and not stat.S_ISLNK(parent_named_before.st_mode)
            and (parent_before.st_dev, parent_before.st_ino)
            == (parent_named_before.st_dev, parent_named_before.st_ino),
            f"{label}: parent identity mismatch",
        )
        named_before = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        descriptor = os.open(
            path.name, descriptor_flags, dir_fd=parent_descriptor,
        )
        held_before = os.fstat(descriptor)
        demand(
            stat.S_ISREG(held_before.st_mode)
            and not stat.S_ISLNK(named_before.st_mode)
            and held_before.st_nlink == 1
            and _identity(held_before) == _identity(named_before),
            f"{label}: descriptor/name identity mismatch",
        )
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        raw = b"".join(chunks)
        held_after = os.fstat(descriptor)
        named_after = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        parent_after = os.stat(path.parent, follow_symlinks=False)
        demand(
            _identity(held_before) == _identity(held_after)
            and _identity(held_after) == _identity(named_after),
            f"{label}: changed or name-swapped while read",
        )
        demand(
            (parent_before.st_dev, parent_before.st_ino)
            == (parent_after.st_dev, parent_after.st_ino),
            f"{label}: parent changed while read",
        )
        demand(len(raw) == held_after.st_size, f"{label}: short descriptor read")
        binding = {
            "path": path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "device": held_after.st_dev,
            "inode": held_after.st_ino,
            "size": held_after.st_size,
            "mtime_ns": held_after.st_mtime_ns,
            "ctime_ns": held_after.st_ctime_ns,
            "mode": stat.S_IMODE(held_after.st_mode),
            "nlink": held_after.st_nlink,
        }
        return path, binding, raw
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(parent_descriptor)


def file_binding(root: Path, path: Path, label: str) -> dict[str, object]:
    _path, binding, _raw = _read_authenticated_file(root, path, label)
    return binding


def checked_binding(root: Path, binding: object, label: str) -> tuple[Path, bytes]:
    demand(type(binding) is dict and set(binding) == IDENTITY_KEYS, f"{label}: identity census")
    assert isinstance(binding, dict)
    raw_path = binding.get("path")
    demand(type(raw_path) is str and raw_path, f"{label}: path missing")
    relative = Path(raw_path)
    demand(not relative.is_absolute() and ".." not in relative.parts, f"{label}: path noncanonical")
    path = root.resolve() / relative
    resolved, actual, raw = _read_authenticated_file(root, path, label)
    demand(actual == binding, f"{label}: inode/hash identity mismatch")
    return resolved, raw


def _bound_json(root: Path, binding: object, label: str) -> tuple[Path, dict[str, object]]:
    path, raw = checked_binding(root, binding, label)
    return path, strict_json_bytes(raw, label)


def _path_hash(record: dict[str, object], prefix: str) -> tuple[object, object]:
    return record.get(f"{prefix}_path"), record.get(f"{prefix}_sha256")


def _planned_pairs(value: object) -> list[list[int]]:
    demand(type(value) is list and bool(value), "planned sector census absent")
    pairs: list[list[int]] = []
    for item in value:
        demand(
            type(item) is list and len(item) == 2
            and all(type(field) is int for field in item),
            "planned sector malformed",
        )
        length, charge = item
        demand(length in (10, 12) and 1 <= charge <= length, "planned sector outside domain")
        pairs.append([length, charge])
    demand(
        pairs == [list(pair) for pair in sorted({tuple(pair) for pair in pairs})],
        "planned sector order/census",
    )
    return pairs


def validate_authorities(
    root: Path,
    identities: dict[str, object],
    length: int,
    charge: int,
    expected_worker: tuple[Path, str],
    expected_driver: tuple[Path, str],
    expected_engine: tuple[Path, str],
    expected_control: tuple[Path, str],
    expected_target_freeze: tuple[Path, str],
) -> dict[str, object]:
    expected_labels = {
        "manifest", "sector_plan", "blind_method_freeze",
        "blind_source_freeze", "target_source_freeze", "target_driver",
        "target_worker", "target_engine", "credential_control",
    }
    demand(set(identities) == expected_labels, "credential authority census")
    loaded: dict[str, tuple[Path, bytes]] = {
        label: checked_binding(root, identities[label], label)
        for label in sorted(expected_labels)
    }
    for label, (path, digest) in {
        "target_worker": expected_worker,
        "target_driver": expected_driver,
        "target_engine": expected_engine,
        "credential_control": expected_control,
        "target_source_freeze": expected_target_freeze,
    }.items():
        bound_path, raw = loaded[label]
        demand(bound_path == path.resolve(), f"{label}: exact path mismatch")
        demand(hashlib.sha256(raw).hexdigest() == digest, f"{label}: exact hash mismatch")

    manifest = strict_json_bytes(loaded["manifest"][1], "manifest")
    demand(manifest.get("schema") == MANIFEST_SCHEMA, "manifest schema")
    demand(manifest.get("status") == MANIFEST_STATUS, "manifest status")

    plan = strict_json_bytes(loaded["sector_plan"][1], "sector plan")
    demand(plan.get("schema") == PLAN_SCHEMA and plan.get("status") == PLAN_STATUS, "sector plan identity")
    planned = _planned_pairs(plan.get("planned_sectors"))
    demand([length, charge] in planned, "sector absent from exact plan")
    demand(plan.get("manifest_sha256") == identities["manifest"]["sha256"], "plan/manifest binding")

    blind_freeze = strict_json_bytes(loaded["blind_method_freeze"][1], "blind method freeze")
    demand(
        blind_freeze.get("schema") == BLIND_FREEZE_SCHEMA
        and blind_freeze.get("status") == BLIND_FREEZE_STATUS,
        "blind method freeze identity",
    )
    demand(blind_freeze.get("target_code_or_matrices_imported") is False, "blind freeze target dependency")
    demand(blind_freeze.get("physical_spectrum_executed_at_freeze") is False, "blind freeze is not pre-output")
    demand(blind_freeze.get("planned_sectors") == planned, "blind freeze/plan sectors")
    demand(blind_freeze.get("manifest_sha256") == identities["manifest"]["sha256"], "blind freeze/manifest binding")
    demand(
        _path_hash(blind_freeze, "sector_plan")
        == (identities["sector_plan"]["path"], identities["sector_plan"]["sha256"]),
        "blind freeze/sector-plan binding",
    )
    demand(
        _path_hash(blind_freeze, "source_freeze")
        == (identities["blind_source_freeze"]["path"], identities["blind_source_freeze"]["sha256"]),
        "blind freeze/source binding",
    )

    source_freeze = strict_json_bytes(loaded["blind_source_freeze"][1], "blind source freeze")
    demand(
        source_freeze.get("schema") == SOURCE_FREEZE_SCHEMA
        and source_freeze.get("status") == SOURCE_FREEZE_STATUS,
        "blind source freeze identity",
    )
    demand(source_freeze.get("physical_spectrum_executed") is False, "blind source freeze is not pre-output")
    source_files = source_freeze.get("files")
    demand(type(source_files) is dict, "blind source file census")
    implementation_path, implementation_sha = _path_hash(blind_freeze, "implementation")
    demand(type(implementation_path) is str and valid_digest(implementation_sha), "blind implementation binding")
    demand(
        Path(implementation_path).name in source_files
        and source_files[Path(implementation_path).name] == implementation_sha,
        "blind method/source implementation mismatch",
    )
    implementation_relative = Path(str(implementation_path))
    demand(
        not implementation_relative.is_absolute()
        and ".." not in implementation_relative.parts,
        "blind implementation path noncanonical",
    )
    implementation = (root.resolve() / implementation_relative).resolve(strict=True)
    demand(root.resolve() in implementation.parents, "blind implementation outside repository")
    _path, implementation_binding, _raw = _read_authenticated_file(
        root, implementation, "blind implementation",
    )
    demand(
        implementation_binding["sha256"] == implementation_sha,
        "blind implementation changed",
    )

    target_freeze = strict_json_bytes(loaded["target_source_freeze"][1], "target source freeze")
    demand(
        target_freeze.get("schema") == TARGET_FREEZE_SCHEMA
        and target_freeze.get("status") == TARGET_FREEZE_STATUS,
        "target source freeze identity",
    )
    demand(target_freeze.get("physical_spectrum_outputs_present_at_freeze") is False, "target source freeze is not pre-output")
    target_files = target_freeze.get("files")
    demand(type(target_files) is dict, "target source file census")
    for label in ("target_driver", "target_worker", "credential_control"):
        binding = identities[label]
        assert isinstance(binding, dict)
        demand(target_files.get(binding["path"]) == binding["sha256"], f"target freeze/{label} binding")

    return {"planned_sectors": planned, "loaded": loaded}


def _publish_owner_once(root: Path, output: Path, payload: dict[str, object]) -> str:
    root = root.resolve()
    output = Path(os.path.abspath(output))
    demand(root in output.parents, "credential output outside repository")
    demand(output.parent.is_dir(), "credential output parent absent")
    parent = os.open(
        output.parent,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    descriptor = -1
    try:
        descriptor = os.open(
            output.name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o400,
            dir_fd=parent,
        )
        raw = canonical_json_bytes(payload)
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            demand(written > 0, "credential write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        held = os.fstat(descriptor)
        named = os.stat(output.name, dir_fd=parent, follow_symlinks=False)
        demand(
            stat.S_ISREG(held.st_mode) and not stat.S_ISLNK(named.st_mode)
            and held.st_nlink == 1 and stat.S_IMODE(held.st_mode) == 0o444
            and (held.st_dev, held.st_ino) == (named.st_dev, named.st_ino),
            "credential owner-once custody",
        )
        os.fsync(parent)
        return hashlib.sha256(raw).hexdigest()
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(parent)


def issue_execution_credential(
    root: Path,
    output: Path,
    length: int,
    charge: int,
    physical_output: Path,
    authority_paths: dict[str, Path],
    expected_worker: tuple[Path, str],
    expected_driver: tuple[Path, str],
    expected_engine: tuple[Path, str],
    expected_control: tuple[Path, str],
    expected_target_freeze: tuple[Path, str],
    execution_token: str,
) -> str:
    identities = {
        label: file_binding(root, path, label)
        for label, path in authority_paths.items()
    }
    validate_authorities(
        root, identities, length, charge, expected_worker, expected_driver,
        expected_engine, expected_control, expected_target_freeze,
    )
    nonce = secrets.token_hex(32)
    payload = {
        "schema": CREDENTIAL_SCHEMA,
        "status": CREDENTIAL_STATUS,
        "ordering_model": ORDERING_MODEL,
        "claim_boundary": (
            "AUTHENTICATED_TRUSTED_CODE_PATH_ORDERING_ONLY__"
            "NO_ADVERSARY_RESISTANT_WALL_CLOCK_ATTESTATION"
        ),
        "authorization_nonce": nonce,
        "execution_token_sha256": hashlib.sha256(execution_token.encode("ascii")).hexdigest(),
        "L": length,
        "q": charge,
        "physical_output_path": _relative(root, physical_output, "physical output parent")
        if physical_output.exists()
        else physical_output.resolve().relative_to(root.resolve()).as_posix(),
        "authorities": identities,
        "planned_sectors": validate_authorities(
            root, identities, length, charge, expected_worker, expected_driver,
            expected_engine, expected_control, expected_target_freeze,
        )["planned_sectors"],
        "creation_order_evidence": {
            "authorities_validated_before_nonce": True,
            "fresh_nonce_bits": 256,
        },
    }
    return _publish_owner_once(root, output, payload)


def validate_execution_credential(
    root: Path,
    credential_path: Path,
    credential_sha256: str,
    length: int,
    charge: int,
    physical_output: Path,
    expected_worker: tuple[Path, str],
    expected_driver: tuple[Path, str],
    expected_engine: tuple[Path, str],
    expected_control: tuple[Path, str],
    expected_target_freeze: tuple[Path, str],
    execution_token: str,
) -> dict[str, object]:
    demand(valid_digest(credential_sha256), "credential SHA-256 malformed")
    _credential_path, credential_binding, credential_raw = _read_authenticated_file(
        root, credential_path, "execution credential",
    )
    demand(credential_binding["sha256"] == credential_sha256, "credential SHA-256 mismatch")
    demand(credential_binding["mode"] == 0o444, "credential mode custody")
    credential = strict_json_bytes(credential_raw, "execution credential")
    demand(
        set(credential) == {
            "schema", "status", "ordering_model", "claim_boundary",
            "authorization_nonce", "execution_token_sha256", "L", "q",
            "physical_output_path", "authorities", "planned_sectors",
            "creation_order_evidence",
        },
        "credential key census",
    )
    demand(credential.get("schema") == CREDENTIAL_SCHEMA and credential.get("status") == CREDENTIAL_STATUS, "credential identity")
    demand(credential.get("ordering_model") == ORDERING_MODEL, "credential ordering model")
    nonce = credential.get("authorization_nonce")
    demand(type(nonce) is str and len(nonce) == 64 and set(nonce) <= HEX, "credential nonce")
    demand(
        credential.get("execution_token_sha256")
        == hashlib.sha256(execution_token.encode("ascii")).hexdigest(),
        "credential execution token binding",
    )
    demand(type(credential.get("L")) is int and credential["L"] == length, "credential L binding")
    demand(type(credential.get("q")) is int and credential["q"] == charge, "credential q binding")
    expected_output = physical_output.resolve().relative_to(root.resolve()).as_posix()
    demand(credential.get("physical_output_path") == expected_output, "credential output binding")
    authorities = credential.get("authorities")
    demand(type(authorities) is dict, "credential authority map")
    validated = validate_authorities(
        root, authorities, length, charge, expected_worker, expected_driver,
        expected_engine, expected_control, expected_target_freeze,
    )
    demand(credential.get("planned_sectors") == validated["planned_sectors"], "credential planned sectors")
    creation = credential.get("creation_order_evidence")
    demand(
        creation == {
            "authorities_validated_before_nonce": True,
            "fresh_nonce_bits": 256,
        },
        "credential creation-order evidence",
    )
    latest_authority_ctime = max(
        int(binding["ctime_ns"]) for binding in authorities.values()
    )
    demand(
        int(credential_binding["ctime_ns"]) >= latest_authority_ctime,
        "credential predates an authority",
    )
    return {
        "schema": BINDING_SCHEMA,
        "ordering_model": ORDERING_MODEL,
        "credential_path": credential_binding["path"],
        "credential_sha256": credential_sha256,
        "authorization_nonce": nonce,
        "manifest_sha256": authorities["manifest"]["sha256"],
        "sector_plan_sha256": authorities["sector_plan"]["sha256"],
        "blind_method_freeze_sha256": authorities["blind_method_freeze"]["sha256"],
        "blind_source_freeze_sha256": authorities["blind_source_freeze"]["sha256"],
    }
