#!/usr/bin/env python3
"""Check, build, and verify a deterministic Zenodo reproduction capsule.

The default action is a read-only preparation check. This program intentionally
contains no network, Git mutation, Zenodo upload, DOI, or publication code.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata
from typing import Any
import zipfile


SCHEMA_VERSION = 1
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
GENERATED_ARCHIVE_PATHS = frozenset({"CAPSULE_BUILD.json", "SHA256SUMS"})
PLACEHOLDER_RE = re.compile(r"@@([A-Z][A-Z0-9_]*)@@")
PLACEHOLDER_NAME_RE = re.compile(r"[A-Z][A-Z0-9_]*")
WINDOWS_RESERVED_NAMES = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{index}" for index in range(1, 10)}
    | {f"lpt{index}" for index in range(1, 10)}
)
ROOT_KEYS = frozenset(
    {
        "schema_version",
        "capsule_name",
        "archive_root",
        "max_file_bytes",
        "max_total_bytes",
        "allowed_source_suffixes",
        "allowed_archive_suffixes",
        "release_placeholders",
        "release_value_patterns",
        "release_forbidden_markers",
        "authenticated_urm_validator_closure",
        "authenticated_proof_packet_layout_closure",
        "entries",
    }
)
ENTRY_KEYS = frozenset(
    {
        "source",
        "archive",
        "required",
        "release_required",
        "template",
        "binary",
        "scan_release_markers",
    }
)
URM_CLOSURE_KEYS = frozenset(
    {
        "archive_spec",
        "public_conflict_policy",
        "spec_sha256",
        "spec_source",
    }
)
PROOF_PACKET_CLOSURE_KEYS = frozenset(
    {
        "archive_spec",
        "inventory_only_packet",
        "portable_packets",
        "spec_sha256",
        "spec_source",
    }
)
SHA256_RE = re.compile(r"[0-9a-f]{64}")
URM_CLOSURE_ROUTES = {
    "tools/build_urm_validator_dependency_closure.py": (
        "publication/zenodo_reproduction_v001/build_urm_validator_dependency_closure.py"
    ),
    "tools/verify_urm_validator_dependency_closure.py": (
        "publication/zenodo_reproduction_v001/verify_urm_validator_dependency_closure.py"
    ),
    "tests/test_urm_validator_dependency_closure.py": (
        "publication/zenodo_reproduction_v001/test_urm_validator_dependency_closure.py"
    ),
    "inventory/URM_VALIDATOR_DEPENDENCY_CLOSURE.json": (
        "publication/zenodo_reproduction_v001/urm_validator_dependency_closure.json"
    ),
}
URM_PUBLIC_CONFLICT_POLICY = (
    "THREE_PINNED_PUBLIC_PROJECTIONS__EXACT_SOURCE_PROVENANCE_RETAINED"
)
URM_BINARY_SUFFIXES = (".i32", ".npy", ".tar.gz", ".u32", ".whl")
PRIVATE_PATH_PATTERNS = (
    (
        "non-synthetic macOS user home",
        re.compile(rb"/Users/(?!example(?:/|\\b))[A-Za-z0-9._-]+(?:/[^\x00\r\n\t \"'<>]*)?"),
    ),
    (
        "Claude private temporary path",
        re.compile(
            rb"/private/tmp/" rb"claude-" rb"[^\x00\r\n\t \"'<>]+",
            re.I,
        ),
    ),
)
PROOF_PACKET_CLOSURE_ROUTES = {
    "tools/proof_packet_layout_closure.py": (
        "publication/zenodo_reproduction_v001/proof_packet_layout_closure.py"
    ),
    "tests/test_proof_packet_layout_closure.py": (
        "publication/zenodo_reproduction_v001/test_proof_packet_layout_closure.py"
    ),
    "inventory/PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json": (
        "publication/zenodo_reproduction_v001/PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
    ),
}
PROOF_PACKET_PORTABLE_IDS = (
    "alpha_allow_require_scope_repair_v001",
    "l04_intrinsic_admission_final_hostile_v001",
    "l12_prefix_lineage_final_audit_v001",
)
PROOF_PACKET_INVENTORY_ONLY_ID = "l04_l10_streamed_preflight_inventory_v001"
PROOF_PACKET_MEMBER_COUNT = 58
PROOF_PACKET_TOTAL_BYTES = 1_649_218


class CapsuleError(RuntimeError):
    """A fail-closed capsule validation error."""


@dataclass(frozen=True)
class PreparedFile:
    source: str
    archive: str
    data: bytes


@dataclass(frozen=True)
class CapsulePlan:
    manifest: dict
    manifest_path: Path
    manifest_sha256: str
    repository_root: Path
    release: bool
    files: tuple[PreparedFile, ...]
    pending: tuple[str, ...]


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise CapsuleError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_nonstandard_json_constant(value: str) -> None:
    raise CapsuleError(f"non-standard JSON constant is forbidden: {value}")


def _load_json(path: Path) -> tuple[dict, bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CapsuleError(f"cannot read JSON file {path}: {exc}") from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CapsuleError(f"JSON file is not UTF-8: {path}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_json_keys,
            parse_constant=_reject_nonstandard_json_constant,
        )
    except CapsuleError:
        raise
    except json.JSONDecodeError as exc:
        raise CapsuleError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CapsuleError(f"JSON root must be an object: {path}")
    return value, raw


def _require_exact_keys(value: dict, allowed: frozenset[str], where: str) -> None:
    unknown = set(value) - allowed
    if unknown:
        raise CapsuleError(f"unknown key(s) in {where}: {sorted(unknown)}")


def _require_bool(value: object, where: str) -> bool:
    if type(value) is not bool:
        raise CapsuleError(f"{where} must be a JSON boolean")
    return value


def _require_positive_int(value: object, where: str) -> int:
    if type(value) is not int or value <= 0:
        raise CapsuleError(f"{where} must be a positive integer")
    return value


def _safe_relative_path(value: object, where: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise CapsuleError(f"{where} must be a non-empty string")
    if unicodedata.normalize("NFC", value) != value:
        raise CapsuleError(f"{where} must use NFC-normalized Unicode: {value!r}")
    if "\\" in value:
        raise CapsuleError(f"{where} contains a backslash: {value!r}")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise CapsuleError(f"{where} contains a control character")
    components = value.split("/")
    if any(component in {"", ".", ".."} for component in components):
        raise CapsuleError(f"{where} is not a normalized relative path: {value!r}")
    for component in components:
        if ":" in component or component.endswith((" ", ".")):
            raise CapsuleError(f"{where} is unsafe on common extraction platforms: {value!r}")
        if component.split(".", 1)[0].casefold() in WINDOWS_RESERVED_NAMES:
            raise CapsuleError(f"{where} uses a reserved device name: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute():
        raise CapsuleError(f"{where} must be relative: {value!r}")
    if any(component == ".git" for component in path.parts):
        raise CapsuleError(f"{where} may not address .git content: {value!r}")
    return path


def _collision_key(path: PurePosixPath) -> str:
    return unicodedata.normalize("NFC", path.as_posix()).casefold()


def _validate_suffixes(value: object, where: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise CapsuleError(f"{where} must be a non-empty array")
    suffixes: list[str] = []
    for suffix in value:
        if (
            not isinstance(suffix, str)
            or not suffix.startswith(".")
            or "/" in suffix
            or "\\" in suffix
            or suffix in {".", ".."}
        ):
            raise CapsuleError(f"unsafe suffix in {where}: {suffix!r}")
        suffixes.append(suffix)
    if len({item.casefold() for item in suffixes}) != len(suffixes):
        raise CapsuleError(f"duplicate suffix in {where}")
    return tuple(sorted(suffixes, key=len, reverse=True))


def _has_allowed_suffix(path: PurePosixPath, suffixes: tuple[str, ...]) -> bool:
    return any(path.as_posix().endswith(suffix) for suffix in suffixes)


def _check_source_path(repository_root: Path, source: PurePosixPath) -> tuple[Path, os.stat_result]:
    current = repository_root
    for component in source.parts:
        current = current / component
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise CapsuleError(f"cannot inspect source {source}: {exc}") from exc
        if stat.S_ISLNK(metadata.st_mode):
            raise CapsuleError(f"symlink forbidden in source path: {source}")
    if not stat.S_ISREG(metadata.st_mode):
        raise CapsuleError(f"source is not a regular file: {source}")
    return current, metadata


def _read_stable_file(path: Path, before: os.stat_result, source: str) -> bytes:
    try:
        data = path.read_bytes()
        after = os.lstat(path)
    except OSError as exc:
        raise CapsuleError(f"cannot read source {source}: {exc}") from exc
    before_identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    after_identity = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if before_identity != after_identity or len(data) != after.st_size:
        raise CapsuleError(f"source changed while being read: {source}")
    if stat.S_ISLNK(after.st_mode) or not stat.S_ISREG(after.st_mode):
        raise CapsuleError(f"source changed type while being read: {source}")
    return data


def _load_release_values(manifest: dict, values_path: Path | None) -> dict[str, str]:
    if values_path is None:
        raise CapsuleError("release mode requires --values")
    values, _ = _load_json(values_path)
    placeholders = manifest["release_placeholders"]
    expected = set(placeholders)
    actual = set(values)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise CapsuleError(f"release value keys differ: missing={missing}, extra={extra}")
    patterns = manifest["release_value_patterns"]
    result: dict[str, str] = {}
    for name in placeholders:
        value = values[name]
        if not isinstance(value, str) or not value or "\n" in value or "\r" in value:
            raise CapsuleError(f"release value {name} must be a non-empty single-line string")
        if not re.fullmatch(patterns[name], value):
            raise CapsuleError(f"release value {name} does not match its required pattern")
        lowered = value.casefold()
        if "placeholder" in lowered or "choose-before-release" in lowered or "example" in lowered:
            raise CapsuleError(f"release value {name} is still an example value")
        result[name] = value
    if set(result["GIT_COMMIT"]) == {"0"}:
        raise CapsuleError("GIT_COMMIT may not be the all-zero example")
    try:
        date.fromisoformat(result["RELEASE_DATE"])
    except ValueError as exc:
        raise CapsuleError("RELEASE_DATE is not a real ISO calendar date") from exc
    if result["ZENODO_DOI"].casefold() == result["ZENODO_CONCEPT_DOI"].casefold():
        raise CapsuleError("version-specific and concept Zenodo DOIs must differ")
    return result


def _render_template(data: bytes, values: dict[str, str], source: str) -> bytes:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CapsuleError(f"template is not UTF-8: {source}") from exc
    for name, value in values.items():
        text = text.replace(f"@@{name}@@", value)
    unresolved = sorted(set(PLACEHOLDER_RE.findall(text)))
    if unresolved:
        raise CapsuleError(f"unresolved release placeholders in {source}: {unresolved}")
    return text.encode("utf-8")


def _validate_manifest_shape(manifest: dict) -> None:
    _require_exact_keys(manifest, ROOT_KEYS, "manifest")
    missing = ROOT_KEYS - set(manifest)
    if missing:
        raise CapsuleError(f"missing manifest key(s): {sorted(missing)}")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise CapsuleError(f"unsupported manifest schema_version: {manifest['schema_version']!r}")
    if not isinstance(manifest["capsule_name"], str) or not manifest["capsule_name"]:
        raise CapsuleError("capsule_name must be a non-empty string")
    _safe_relative_path(manifest["archive_root"], "archive_root")
    _require_positive_int(manifest["max_file_bytes"], "max_file_bytes")
    _require_positive_int(manifest["max_total_bytes"], "max_total_bytes")
    if manifest["max_total_bytes"] < manifest["max_file_bytes"]:
        raise CapsuleError("max_total_bytes may not be less than max_file_bytes")
    _validate_suffixes(manifest["allowed_source_suffixes"], "allowed_source_suffixes")
    _validate_suffixes(manifest["allowed_archive_suffixes"], "allowed_archive_suffixes")

    placeholders = manifest["release_placeholders"]
    if not isinstance(placeholders, list) or not placeholders:
        raise CapsuleError("release_placeholders must be a non-empty array")
    if any(not isinstance(item, str) or not PLACEHOLDER_NAME_RE.fullmatch(item) for item in placeholders):
        raise CapsuleError("release_placeholders contains an invalid name")
    if len(set(placeholders)) != len(placeholders):
        raise CapsuleError("release_placeholders contains duplicates")

    patterns = manifest["release_value_patterns"]
    if not isinstance(patterns, dict) or set(patterns) != set(placeholders):
        raise CapsuleError("release_value_patterns keys must exactly match release_placeholders")
    for name, pattern in patterns.items():
        if not isinstance(pattern, str) or not pattern:
            raise CapsuleError(f"release pattern for {name} must be a non-empty string")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise CapsuleError(f"invalid release pattern for {name}: {exc}") from exc

    markers = manifest["release_forbidden_markers"]
    if not isinstance(markers, list) or any(not isinstance(item, str) or not item for item in markers):
        raise CapsuleError("release_forbidden_markers must be an array of non-empty strings")
    if len(set(markers)) != len(markers):
        raise CapsuleError("release_forbidden_markers contains duplicates")

    entries = manifest["entries"]
    if not isinstance(entries, list) or not entries:
        raise CapsuleError("entries must be a non-empty array")

    urm_closure = manifest["authenticated_urm_validator_closure"]
    if urm_closure is not None:
        if not isinstance(urm_closure, dict):
            raise CapsuleError("authenticated_urm_validator_closure must be null or an object")
        _require_exact_keys(
            urm_closure,
            URM_CLOSURE_KEYS,
            "authenticated_urm_validator_closure",
        )
        missing = URM_CLOSURE_KEYS - set(urm_closure)
        if missing:
            raise CapsuleError(
                "missing authenticated_urm_validator_closure key(s): "
                f"{sorted(missing)}"
            )
        _safe_relative_path(
            urm_closure["spec_source"],
            "authenticated_urm_validator_closure.spec_source",
        )
        _safe_relative_path(
            urm_closure["archive_spec"],
            "authenticated_urm_validator_closure.archive_spec",
        )
        _require_sha256(
            urm_closure["spec_sha256"],
            "authenticated_urm_validator_closure.spec_sha256",
        )
        if urm_closure["public_conflict_policy"] != URM_PUBLIC_CONFLICT_POLICY:
            raise CapsuleError("authenticated URM closure conflict policy changed")

    proof_closure = manifest["authenticated_proof_packet_layout_closure"]
    if proof_closure is not None:
        if not isinstance(proof_closure, dict):
            raise CapsuleError(
                "authenticated_proof_packet_layout_closure must be null or an object"
            )
        _require_exact_keys(
            proof_closure,
            PROOF_PACKET_CLOSURE_KEYS,
            "authenticated_proof_packet_layout_closure",
        )
        missing = PROOF_PACKET_CLOSURE_KEYS - set(proof_closure)
        if missing:
            raise CapsuleError(
                "missing authenticated_proof_packet_layout_closure key(s): "
                f"{sorted(missing)}"
            )
        _safe_relative_path(
            proof_closure["spec_source"],
            "authenticated_proof_packet_layout_closure.spec_source",
        )
        _safe_relative_path(
            proof_closure["archive_spec"],
            "authenticated_proof_packet_layout_closure.archive_spec",
        )
        _require_sha256(
            proof_closure["spec_sha256"],
            "authenticated_proof_packet_layout_closure.spec_sha256",
        )
        portable = proof_closure["portable_packets"]
        if (
            not isinstance(portable, list)
            or tuple(portable) != PROOF_PACKET_PORTABLE_IDS
        ):
            raise CapsuleError("authenticated proof-packet portable set changed")
        if (
            proof_closure["inventory_only_packet"]
            != PROOF_PACKET_INVENTORY_ONLY_ID
        ):
            raise CapsuleError("authenticated proof-packet inventory-only set changed")

def _require_sha256(value: object, where: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise CapsuleError(f"{where} must be a lowercase SHA-256 digest")
    return value


def _canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def _prepare_proof_packet_layout_closure(
    manifest: dict,
    repository_root: Path,
    source_suffixes: tuple[str, ...],
    archive_suffixes: tuple[str, ...],
    archive_keys: dict[str, str],
    *,
    release: bool,
) -> tuple[list[PreparedFile], int]:
    """Embed and authenticate the isolated historical proof-packet layouts.

    The alpha packet deliberately comes from its isolated passing Git commit,
    not from later live ledgers.  L4 and L12 likewise come from their sealed
    commits.  The companion tool proves the exact revision/path/hash/byte
    inventory before this function reads any Git blob.  The streamed L4--L10
    packet is included only as authenticated inventory because its historical
    verdict depends on free space at the extraction root.
    """

    config = manifest["authenticated_proof_packet_layout_closure"]
    if config is None:
        return [], 0

    routed = {
        entry.get("archive"): entry.get("source")
        for entry in manifest["entries"]
        if isinstance(entry, dict)
        and isinstance(entry.get("archive"), str)
        and isinstance(entry.get("source"), str)
        and entry.get("archive") in PROOF_PACKET_CLOSURE_ROUTES
    }
    if routed != PROOF_PACKET_CLOSURE_ROUTES:
        missing = sorted(set(PROOF_PACKET_CLOSURE_ROUTES) - set(routed))
        wrong = sorted(
            archive
            for archive, source in routed.items()
            if PROOF_PACKET_CLOSURE_ROUTES.get(archive) != source
        )
        raise CapsuleError(
            f"proof-packet closure archive routes differ: missing={missing}, wrong={wrong}"
        )
    if (
        config["spec_source"]
        != PROOF_PACKET_CLOSURE_ROUTES[
            "inventory/PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
        ]
        or config["archive_spec"]
        != "inventory/PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
    ):
        raise CapsuleError("authenticated proof-packet closure spec route changed")

    spec_path = repository_root / config["spec_source"]
    try:
        spec_raw = spec_path.read_bytes()
    except OSError as exc:
        raise CapsuleError(
            f"cannot read authenticated proof-packet closure spec: {exc}"
        ) from exc
    if hashlib.sha256(spec_raw).hexdigest() != config["spec_sha256"]:
        raise CapsuleError("authenticated proof-packet closure spec SHA-256 mismatch")

    tool_path = repository_root / PROOF_PACKET_CLOSURE_ROUTES[
        "tools/proof_packet_layout_closure.py"
    ]
    module_name = "capsule_proof_packet_layout_closure_preflight"
    try:
        module_spec = importlib.util.spec_from_file_location(module_name, tool_path)
        if module_spec is None or module_spec.loader is None:
            raise CapsuleError("cannot load the proof-packet layout closure tool")
        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)
        verification = module.verify_source(repository_root, spec_path)
        closure = module.load_checked_spec(spec_path)
        if verification != {
            "member_count": PROOF_PACKET_MEMBER_COUNT,
            "packet_count": 4,
            "status": "VERIFIED_PINNED_PROOF_PACKET_SOURCE_CLOSURE",
            "total_bytes": PROOF_PACKET_TOTAL_BYTES,
        }:
            raise CapsuleError(
                f"authenticated proof-packet source census changed: {verification!r}"
            )

        packets = closure.get("packets")
        if not isinstance(packets, list) or len(packets) != 4:
            raise CapsuleError("authenticated proof-packet inventory changed")
        packet_by_id = {
            packet.get("id"): packet
            for packet in packets
            if isinstance(packet, dict) and isinstance(packet.get("id"), str)
        }
        if set(packet_by_id) != {
            *PROOF_PACKET_PORTABLE_IDS,
            PROOF_PACKET_INVENTORY_ONLY_ID,
        }:
            raise CapsuleError("authenticated proof-packet id set changed")
        for packet_id in PROOF_PACKET_PORTABLE_IDS:
            if packet_by_id[packet_id].get("portable_capsule_gate") is not True:
                raise CapsuleError(
                    f"portable proof-packet gate was demoted: {packet_id}"
                )
        inventory = packet_by_id[PROOF_PACKET_INVENTORY_ONLY_ID]
        if (
            inventory.get("portable_capsule_gate") is not False
            or inventory.get("classification")
            != "ENVIRONMENT_DEPENDENT_HISTORICAL_PREFLIGHT_INVENTORY_ONLY"
            or inventory.get("execution", {}).get("mode")
            != "DO_NOT_EXECUTE_AS_A_PORTABLE_CAPSULE_GATE"
        ):
            raise CapsuleError(
                "environment-dependent streamed preflight was promoted to a portable gate"
            )

        selected: list[PreparedFile] = []
        selected_bytes = 0
        for packet in packets:
            packet_id = packet["id"]
            revision = packet.get("source_revision")
            members = packet.get("members")
            if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
                raise CapsuleError(
                    f"proof-packet revision is not a full commit id: {packet_id}"
                )
            if not isinstance(members, list) or len(members) != packet.get("member_count"):
                raise CapsuleError(f"proof-packet member census changed: {packet_id}")
            packet_bytes = 0
            for member in members:
                if not isinstance(member, dict):
                    raise CapsuleError(f"proof-packet member is not an object: {packet_id}")
                source = _safe_relative_path(
                    member.get("path"), f"proof-packet {packet_id} source"
                )
                archive = _safe_relative_path(
                    member.get("archive_path"), f"proof-packet {packet_id} archive"
                )
                expected_archive = PurePosixPath(packet["archive_prefix"]) / source
                if archive != expected_archive:
                    raise CapsuleError(
                        f"proof-packet original-layout route changed: {packet_id}:{source}"
                    )
                expected_bytes = member.get("bytes")
                if type(expected_bytes) is not int or expected_bytes <= 0:
                    raise CapsuleError(
                        f"proof-packet byte count is invalid: {packet_id}:{source}"
                    )
                expected_digest = _require_sha256(
                    member.get("sha256"), f"proof-packet {packet_id}:{source} sha256"
                )
                if not _has_allowed_suffix(source, source_suffixes):
                    raise CapsuleError(
                        f"proof-packet source has a disallowed suffix: {source}"
                    )
                if not _has_allowed_suffix(archive, archive_suffixes):
                    raise CapsuleError(
                        f"proof-packet archive has a disallowed suffix: {archive}"
                    )
                archive_key = _collision_key(archive)
                if archive_key in archive_keys:
                    raise CapsuleError(
                        f"duplicate/colliding proof-packet archive path: {archive}"
                    )
                data = module.git_blob(repository_root, revision, source)
                if len(data) != expected_bytes or hashlib.sha256(data).hexdigest() != expected_digest:
                    raise CapsuleError(
                        f"proof-packet Git blob changed: {packet_id}:{source}"
                    )
                module.require_no_leakage(data, f"{packet_id}:{source}")
                try:
                    decoded = data.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise CapsuleError(
                        f"proof-packet source is not UTF-8: {packet_id}:{source}"
                    ) from exc
                if release:
                    unresolved = sorted(set(PLACEHOLDER_RE.findall(decoded)))
                    if unresolved:
                        raise CapsuleError(
                            f"unresolved release placeholders in proof packet {source}: "
                            f"{unresolved}"
                        )
                    found = [
                        marker
                        for marker in manifest["release_forbidden_markers"]
                        if marker in decoded
                    ]
                    if found:
                        raise CapsuleError(
                            f"release blocker marker(s) in proof packet {source}: {found}"
                        )
                if len(data) > manifest["max_file_bytes"]:
                    raise CapsuleError(
                        f"proof-packet source exceeds max_file_bytes: {source}"
                    )
                archive_keys[archive_key] = archive.as_posix()
                selected.append(
                    PreparedFile(
                        f"<git:{revision}:{source.as_posix()}>",
                        archive.as_posix(),
                        data,
                    )
                )
                selected_bytes += len(data)
                packet_bytes += len(data)
            if packet_bytes != packet.get("total_bytes"):
                raise CapsuleError(f"proof-packet byte census changed: {packet_id}")
    except CapsuleError:
        raise
    except Exception as exc:
        raise CapsuleError(
            f"authenticated proof-packet closure failed: {type(exc).__name__}: {exc}"
        ) from exc
    finally:
        sys.modules.pop(module_name, None)

    if (
        len(selected) != PROOF_PACKET_MEMBER_COUNT
        or selected_bytes != PROOF_PACKET_TOTAL_BYTES
    ):
        raise CapsuleError(
            "proof-packet integration census changed: "
            f"files={len(selected)} bytes={selected_bytes}"
        )
    return selected, selected_bytes


def _prepare_urm_validator_closure(
    manifest: dict,
    repository_root: Path,
    source_suffixes: tuple[str, ...],
    archive_suffixes: tuple[str, ...],
    archive_keys: dict[str, str],
    existing_files: list[PreparedFile],
    *,
    release: bool,
) -> tuple[list[PreparedFile], int]:
    """Embed the focused exact URM closure declared by its pinned inventory."""

    config = manifest["authenticated_urm_validator_closure"]
    if config is None:
        return [], 0

    routed = {
        entry.get("archive"): entry.get("source")
        for entry in manifest["entries"]
        if isinstance(entry, dict)
        and isinstance(entry.get("archive"), str)
        and isinstance(entry.get("source"), str)
        and entry.get("archive") in URM_CLOSURE_ROUTES
    }
    if routed != URM_CLOSURE_ROUTES:
        missing = sorted(set(URM_CLOSURE_ROUTES) - set(routed))
        wrong = sorted(
            archive
            for archive, source in routed.items()
            if URM_CLOSURE_ROUTES.get(archive) != source
        )
        raise CapsuleError(
            f"URM closure archive routes differ: missing={missing}, wrong={wrong}"
        )
    if (
        config["spec_source"]
        != URM_CLOSURE_ROUTES["inventory/URM_VALIDATOR_DEPENDENCY_CLOSURE.json"]
        or config["archive_spec"]
        != "inventory/URM_VALIDATOR_DEPENDENCY_CLOSURE.json"
    ):
        raise CapsuleError("authenticated URM closure spec route changed")

    spec_path = repository_root / config["spec_source"]
    try:
        spec_raw = spec_path.read_bytes()
    except OSError as exc:
        raise CapsuleError(f"cannot read authenticated URM closure spec: {exc}") from exc
    if hashlib.sha256(spec_raw).hexdigest() != config["spec_sha256"]:
        raise CapsuleError("authenticated URM closure spec SHA-256 mismatch")

    verifier_path = repository_root / URM_CLOSURE_ROUTES[
        "tools/verify_urm_validator_dependency_closure.py"
    ]
    module_name = "capsule_urm_validator_closure_preflight"
    try:
        module_spec = importlib.util.spec_from_file_location(module_name, verifier_path)
        if module_spec is None or module_spec.loader is None:
            raise CapsuleError("cannot load the authenticated URM closure verifier")
        verifier = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = verifier
        module_spec.loader.exec_module(verifier)
        closure = verifier.load_and_validate_spec(spec_path)
        verified_count, verified_bytes = verifier.verify_root(
            closure, repository_root, "repository"
        )
    except CapsuleError:
        raise
    except Exception as exc:
        raise CapsuleError(
            f"authenticated URM closure preflight failed: {type(exc).__name__}: {exc}"
        ) from exc
    finally:
        sys.modules.pop(module_name, None)
    expected_repository_count = (
        closure["closure_entry_count"] + closure["runtime_artifact_count"]
    )
    expected_repository_bytes = (
        closure["closure_total_bytes"] + closure["runtime_artifact_total_bytes"]
    )
    if (verified_count, verified_bytes) != (
        expected_repository_count,
        expected_repository_bytes,
    ):
        raise CapsuleError("authenticated URM repository closure census changed")

    conflict_by_path = {
        row["exact_repository_path"]: row for row in closure["sanitized_conflicts"]
    }
    if closure["sanitized_conflict_count"] != len(conflict_by_path):
        raise CapsuleError(
            "authenticated URM public-projection census changed"
        )
    existing_by_archive = {item.archive: item for item in existing_files}
    for conflict in conflict_by_path.values():
        exact_archive = conflict["exact_archive_path"]
        public_archive = conflict["existing_public_archive_path"]
        if public_archive != exact_archive:
            raise CapsuleError(
                f"URM projection must replace bytes at the exact archive path: {exact_archive}"
            )
        if _collision_key(PurePosixPath(exact_archive)) not in archive_keys:
            raise CapsuleError(
                f"URM public projection is not selected by the manifest: {public_archive}"
            )
        public_file = existing_by_archive.get(public_archive)
        if public_file is None:
            raise CapsuleError(
                f"sanitized URM public substitute is absent: {public_archive}"
            )
        if (
            public_file.source != conflict["public_substitute_repository_path"]
            or len(public_file.data) != conflict["public_substitute_size_bytes"]
            or hashlib.sha256(public_file.data).hexdigest()
            != conflict["public_substitute_sha256"]
        ):
            raise CapsuleError(
                f"sanitized URM public substitute changed: {public_archive}"
            )

    selected: list[PreparedFile] = []
    selected_bytes = 0
    reused = len(conflict_by_path)
    for row in closure["entries"]:
        source_text = row["repository_path"]
        if source_text in conflict_by_path:
            continue
        archive_text = row["archive_path"]
        source = _safe_relative_path(source_text, "URM closure source")
        archive = _safe_relative_path(archive_text, "URM closure archive")
        if not _has_allowed_suffix(source, source_suffixes):
            raise CapsuleError(f"URM closure source has a disallowed suffix: {source}")
        if not _has_allowed_suffix(archive, archive_suffixes):
            raise CapsuleError(f"URM closure archive has a disallowed suffix: {archive}")
        source_path, metadata = _check_source_path(repository_root, source)
        if metadata.st_size != row["size_bytes"]:
            raise CapsuleError(f"URM closure source byte count changed: {source}")
        if metadata.st_size > manifest["max_file_bytes"]:
            raise CapsuleError(f"URM closure source exceeds max_file_bytes: {source}")
        data = _read_stable_file(source_path, metadata, source.as_posix())
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise CapsuleError(f"URM closure source hash changed: {source}")
        binary = source.as_posix().endswith(URM_BINARY_SUFFIXES)
        if binary:
            decoded = ""
        else:
            try:
                decoded = data.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise CapsuleError(f"URM closure source is not UTF-8: {source}") from exc
        if release and not binary:
            unresolved = sorted(set(PLACEHOLDER_RE.findall(decoded)))
            if unresolved:
                raise CapsuleError(
                    f"unresolved release placeholders in URM closure source {source}: "
                    f"{unresolved}"
                )
            found = [
                marker
                for marker in manifest["release_forbidden_markers"]
                if marker in decoded
            ]
            if found:
                raise CapsuleError(
                    f"release blocker marker(s) in URM closure source {source}: {found}"
                )

        archive_key = _collision_key(archive)
        if archive_key in archive_keys:
            existing = existing_by_archive.get(archive.as_posix())
            if (
                existing is None
                or existing.source != source.as_posix()
                or existing.data != data
            ):
                raise CapsuleError(
                    f"URM closure archive collision is not an exact reuse: {archive}"
                )
            reused += 1
            continue
        archive_keys[archive_key] = archive.as_posix()
        item = PreparedFile(source.as_posix(), archive.as_posix(), data)
        selected.append(item)
        existing_by_archive[item.archive] = item
        selected_bytes += len(data)

    for row in closure["runtime_artifacts"]:
        source = _safe_relative_path(
            row["repository_path"], "URM runtime source"
        )
        archive = _safe_relative_path(row["archive_path"], "URM runtime archive")
        if not _has_allowed_suffix(source, source_suffixes):
            raise CapsuleError(f"URM runtime source has a disallowed suffix: {source}")
        if not _has_allowed_suffix(archive, archive_suffixes):
            raise CapsuleError(f"URM runtime archive has a disallowed suffix: {archive}")
        source_path, metadata = _check_source_path(repository_root, source)
        if metadata.st_size != row["size_bytes"]:
            raise CapsuleError(f"URM runtime byte count changed: {source}")
        if metadata.st_size > manifest["max_file_bytes"]:
            raise CapsuleError(f"URM runtime exceeds max_file_bytes: {source}")
        data = _read_stable_file(source_path, metadata, source.as_posix())
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise CapsuleError(f"URM runtime hash changed: {source}")
        archive_key = _collision_key(archive)
        if archive_key in archive_keys:
            raise CapsuleError(f"URM runtime archive path collides: {archive}")
        archive_keys[archive_key] = archive.as_posix()
        item = PreparedFile(source.as_posix(), archive.as_posix(), data)
        selected.append(item)
        existing_by_archive[item.archive] = item
        selected_bytes += len(data)

    expected_selected = (
        closure["closure_entry_count"]
        + closure["runtime_artifact_count"]
        - reused
    )
    if len(selected) != expected_selected:
        raise CapsuleError(
            "URM closure integration census changed: "
            f"reused={reused}, added={len(selected)}, expected={expected_selected}"
        )
    return selected, selected_bytes


def prepare_plan(
    manifest_path: Path,
    repository_root: Path,
    *,
    release: bool = False,
    values_path: Path | None = None,
) -> CapsulePlan:
    """Validate sources and return an immutable in-memory capsule plan."""

    manifest_path = manifest_path.resolve()
    repository_root = repository_root.resolve()
    if not repository_root.is_dir():
        raise CapsuleError(f"repository root is not a directory: {repository_root}")
    manifest, manifest_raw = _load_json(manifest_path)
    _validate_manifest_shape(manifest)
    source_suffixes = _validate_suffixes(
        manifest["allowed_source_suffixes"], "allowed_source_suffixes"
    )
    archive_suffixes = _validate_suffixes(
        manifest["allowed_archive_suffixes"], "allowed_archive_suffixes"
    )
    values = _load_release_values(manifest, values_path) if release else {}
    if values_path is not None and not release:
        raise CapsuleError("--values is accepted only with --release")

    archive_keys: dict[str, str] = {}
    source_keys: dict[str, str] = {}
    prepared: list[PreparedFile] = []
    pending: list[str] = []
    total_bytes = 0

    for index, entry in enumerate(manifest["entries"]):
        where = f"entries[{index}]"
        if not isinstance(entry, dict):
            raise CapsuleError(f"{where} must be an object")
        _require_exact_keys(entry, ENTRY_KEYS, where)
        if "source" not in entry or "archive" not in entry:
            raise CapsuleError(f"{where} requires source and archive")
        source = _safe_relative_path(entry["source"], f"{where}.source")
        archive = _safe_relative_path(entry["archive"], f"{where}.archive")
        required = _require_bool(entry.get("required", True), f"{where}.required")
        release_required = _require_bool(
            entry.get("release_required", required), f"{where}.release_required"
        )
        template = _require_bool(entry.get("template", False), f"{where}.template")
        binary = _require_bool(entry.get("binary", False), f"{where}.binary")
        scan_markers = _require_bool(
            entry.get("scan_release_markers", True), f"{where}.scan_release_markers"
        )
        if binary and template:
            raise CapsuleError(f"{where} binary entry may not be a template")
        if binary and scan_markers:
            raise CapsuleError(
                f"{where} binary entry must set scan_release_markers to false"
            )
        if required and not release_required:
            raise CapsuleError(f"{where} cannot be required in preparation but optional in release")
        if not _has_allowed_suffix(source, source_suffixes):
            raise CapsuleError(f"source has a disallowed suffix: {source}")
        if not _has_allowed_suffix(archive, archive_suffixes):
            raise CapsuleError(f"archive path has a disallowed suffix: {archive}")
        if archive.as_posix() in GENERATED_ARCHIVE_PATHS:
            raise CapsuleError(f"archive path is reserved for generated custody: {archive}")

        source_key = _collision_key(source)
        archive_key = _collision_key(archive)
        if source_key in source_keys and source_keys[source_key] != source.as_posix():
            raise CapsuleError(
                f"duplicate/colliding source paths: {source_keys[source_key]!r}, {source.as_posix()!r}"
            )
        if archive_key in archive_keys:
            raise CapsuleError(
                f"duplicate/colliding archive paths: {archive_keys[archive_key]!r}, {archive.as_posix()!r}"
            )
        source_keys[source_key] = source.as_posix()
        archive_keys[archive_key] = archive.as_posix()

        try:
            source_path, metadata = _check_source_path(repository_root, source)
        except FileNotFoundError:
            if required or (release and release_required):
                mode = "release" if release and release_required else "preparation"
                raise CapsuleError(f"missing {mode}-required source: {source}")
            pending.append(source.as_posix())
            continue
        if metadata.st_size > manifest["max_file_bytes"]:
            raise CapsuleError(
                f"source exceeds max_file_bytes ({metadata.st_size}): {source}"
            )
        data = _read_stable_file(source_path, metadata, source.as_posix())
        decoded: str | None = None
        if not binary:
            try:
                decoded = data.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise CapsuleError(f"capsule source is not UTF-8 text: {source}") from exc

        if template and release:
            data = _render_template(data, values, source.as_posix())
            decoded = data.decode("utf-8")
        if release and not binary:
            assert decoded is not None
            unresolved = sorted(set(PLACEHOLDER_RE.findall(decoded)))
            if unresolved:
                raise CapsuleError(
                    f"unresolved release placeholders in {source}: {unresolved}"
                )
            if scan_markers:
                found = [marker for marker in manifest["release_forbidden_markers"] if marker in decoded]
                if found:
                    raise CapsuleError(f"release blocker marker(s) in {source}: {found}")

        total_bytes += len(data)
        if total_bytes > manifest["max_total_bytes"]:
            raise CapsuleError(
                f"selected sources exceed max_total_bytes ({total_bytes})"
            )
        prepared.append(
            PreparedFile(source.as_posix(), archive.as_posix(), data)
        )

    proof_packet_files, proof_packet_bytes = _prepare_proof_packet_layout_closure(
        manifest,
        repository_root,
        source_suffixes,
        archive_suffixes,
        archive_keys,
        release=release,
    )
    total_bytes += proof_packet_bytes
    if total_bytes > manifest["max_total_bytes"]:
        raise CapsuleError(
            f"selected sources exceed max_total_bytes ({total_bytes})"
        )
    prepared.extend(proof_packet_files)

    urm_files, urm_bytes = _prepare_urm_validator_closure(
        manifest,
        repository_root,
        source_suffixes,
        archive_suffixes,
        archive_keys,
        prepared,
        release=release,
    )
    total_bytes += urm_bytes
    if total_bytes > manifest["max_total_bytes"]:
        raise CapsuleError(
            f"selected sources exceed max_total_bytes ({total_bytes})"
        )
    prepared.extend(urm_files)

    _scan_prepared_private_paths(prepared)

    prepared.sort(key=lambda item: item.archive)
    return CapsulePlan(
        manifest=manifest,
        manifest_path=manifest_path,
        manifest_sha256=hashlib.sha256(manifest_raw).hexdigest(),
        repository_root=repository_root,
        release=release,
        files=tuple(prepared),
        pending=tuple(sorted(pending)),
    )


def _scan_prepared_private_paths(files: list[PreparedFile]) -> None:
    """Reject real workstation paths after all dynamic closure expansion."""

    for item in files:
        for label, pattern in PRIVATE_PATH_PATTERNS:
            match = pattern.search(item.data)
            if match is not None:
                sample = match.group(0).decode("utf-8", errors="replace")
                raise CapsuleError(
                    f"private path leak ({label}) in prepared archive member "
                    f"{item.archive} from {item.source}: {sample}"
                )


def _archive_payload(plan: CapsulePlan) -> tuple[PreparedFile, ...]:
    file_rows = [
        {
            "archive": item.archive,
            "bytes": len(item.data),
            "sha256": hashlib.sha256(item.data).hexdigest(),
            "source": item.source,
        }
        for item in plan.files
    ]
    build_record = {
        "capsule_name": plan.manifest["capsule_name"],
        "draft_not_for_publication": not plan.release,
        "files": file_rows,
        "manifest_sha256": plan.manifest_sha256,
        "release_mode": plan.release,
        "schema_version": 1,
    }
    build_data = (json.dumps(build_record, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with_build = list(plan.files) + [
        PreparedFile("<generated>", "CAPSULE_BUILD.json", build_data)
    ]
    checksum_lines = [
        f"{hashlib.sha256(item.data).hexdigest()}  {item.archive}\n"
        for item in sorted(with_build, key=lambda item: item.archive)
    ]
    checksums = "".join(checksum_lines).encode("utf-8")
    payload = with_build + [PreparedFile("<generated>", "SHA256SUMS", checksums)]
    return tuple(sorted(payload, key=lambda item: item.archive))


def _full_archive_name(plan: CapsulePlan, archive: str) -> str:
    return f"{plan.manifest['archive_root']}/{archive}"


def build_archive(plan: CapsulePlan, output: Path) -> str:
    """Build a new deterministic, stored ZIP and return its SHA-256."""

    output = output.resolve()
    if output.exists():
        raise CapsuleError(f"refusing to overwrite existing output: {output}")
    if not output.parent.is_dir():
        raise CapsuleError(f"output parent does not exist: {output.parent}")
    payload = _archive_payload(plan)
    created = False
    try:
        with zipfile.ZipFile(output, mode="x", compression=zipfile.ZIP_STORED) as archive:
            created = True
            for item in payload:
                name = _full_archive_name(plan, item.archive)
                _safe_relative_path(name, "generated ZIP member")
                info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
                info.compress_type = zipfile.ZIP_STORED
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                archive.writestr(info, item.data)
    except Exception:
        if created:
            try:
                output.unlink()
            except OSError:
                pass
        raise
    return hashlib.sha256(output.read_bytes()).hexdigest()


def verify_archive(plan: CapsulePlan, archive_path: Path) -> str:
    """Verify exact members, metadata, and bytes against a newly prepared plan."""

    archive_path = archive_path.resolve()
    if not archive_path.is_file():
        raise CapsuleError(f"archive does not exist: {archive_path}")
    expected = {
        _full_archive_name(plan, item.archive): item.data for item in _archive_payload(plan)
    }
    try:
        with zipfile.ZipFile(archive_path, mode="r") as archive:
            if archive.testzip() is not None:
                raise CapsuleError("ZIP CRC verification failed")
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise CapsuleError("ZIP contains duplicate member names")
            folded: set[str] = set()
            for info in infos:
                member = _safe_relative_path(info.filename, "ZIP member")
                key = _collision_key(member)
                if key in folded:
                    raise CapsuleError("ZIP contains case-folded or Unicode-normalized collisions")
                folded.add(key)
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise CapsuleError(f"ZIP symlink member forbidden: {info.filename}")
                if info.is_dir() or not stat.S_ISREG(mode):
                    raise CapsuleError(f"ZIP member is not a regular file: {info.filename}")
                if info.date_time != FIXED_ZIP_TIME:
                    raise CapsuleError(f"ZIP member has nondeterministic timestamp: {info.filename}")
                if info.compress_type != zipfile.ZIP_STORED:
                    raise CapsuleError(f"ZIP member is not deterministically stored: {info.filename}")
            actual_names = set(names)
            expected_names = set(expected)
            if actual_names != expected_names:
                missing = sorted(expected_names - actual_names)
                extra = sorted(actual_names - expected_names)
                raise CapsuleError(f"ZIP member set differs: missing={missing}, extra={extra}")
            for name, data in expected.items():
                if archive.read(name) != data:
                    raise CapsuleError(f"ZIP member bytes differ: {name}")
    except zipfile.BadZipFile as exc:
        raise CapsuleError(f"invalid ZIP archive: {archive_path}") from exc
    return hashlib.sha256(archive_path.read_bytes()).hexdigest()


def _default_repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail-closed deterministic reproduction-capsule checker/builder"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("check", "build", "verify"),
        default="check",
        help="default: check",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().with_name("capsule_manifest.json"),
    )
    parser.add_argument("--repo-root", type=Path, default=_default_repository_root())
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--values", type=Path)
    parser.add_argument("--output", type=Path, help="required for build")
    parser.add_argument("--archive", type=Path, help="required for verify")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "build" and args.output is None:
            raise CapsuleError("build requires --output")
        if args.command == "verify" and args.archive is None:
            raise CapsuleError("verify requires --archive")
        if args.command != "build" and args.output is not None:
            raise CapsuleError("--output is valid only with build")
        if args.command != "verify" and args.archive is not None:
            raise CapsuleError("--archive is valid only with verify")

        plan = prepare_plan(
            args.manifest,
            args.repo_root,
            release=args.release,
            values_path=args.values,
        )
        total_bytes = sum(len(item.data) for item in plan.files)
        print(
            f"CHECK OK mode={'RELEASE' if plan.release else 'PREPARATION'} "
            f"files={len(plan.files)} bytes={total_bytes} pending={len(plan.pending)}"
        )
        for source in plan.pending:
            print(f"PENDING release input: {source}")

        if args.command == "build":
            digest = build_archive(plan, args.output)
            print(f"BUILD OK sha256={digest} output={args.output.resolve()}")
        elif args.command == "verify":
            digest = verify_archive(plan, args.archive)
            print(f"VERIFY OK sha256={digest} archive={args.archive.resolve()}")
        return 0
    except CapsuleError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
