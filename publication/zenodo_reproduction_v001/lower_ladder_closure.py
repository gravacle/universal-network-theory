#!/usr/bin/env python3
"""Fail-closed closure for the L08/L10 lower-ladder reproduction.

This tool is deliberately independent of the main capsule builder.  It
authenticates the minimum source inputs used by
``extract_lower_bound_progression.py``, produces path-neutral cache-manifest
projections, materializes the inputs in their original repository-relative
layout, and executes the extracted calculation.

Historical verifier inventories remain in the full Git research record and
are intentionally outside this focused reproduction closure.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


SCHEMA = "WAC_LOWER_LADDER_CLOSURE_V001"
PROJECTION_SCHEMA = "WAC_LOWER_LADDER_CACHE_PROJECTION_V001"
ARCHIVE_PREFIX = PurePosixPath("reproduction/lower_ladder_original_layout")
EXPECTED_STDOUT = "L08: 0.0244800482\nL10: 0.0687369678\n"
EXPECTED_VALUES = {"L08": "0.0244800482", "L10": "0.0687369678"}

HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY_ROOT = HERE.parents[1]
SPEC_PATH = HERE / "LOWER_LADDER_CLOSURE_SPEC.json"
EXTRACTED_SPEC_PATH = HERE.parent / "inventory" / "LOWER_LADDER_CLOSURE_SPEC.json"
PUBLIC_MANIFEST_PATHS = {
    8: HERE / "release_inputs" / "L08_CACHE_MANIFEST_MINIMAL_PUBLIC.json",
    10: HERE / "release_inputs" / "L10_CACHE_MANIFEST_MINIMAL_PUBLIC.json",
}

EXTRACTOR = PurePosixPath(
    "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
    "extract_lower_bound_progression.py"
)
SUPPORT = PurePosixPath(
    "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
    "l12_lineage_resolved_support.py"
)
CACHE_BASE = PurePosixPath(
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012"
)
WORKSPACE_BASE = PurePosixPath(
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES"
)

# The value is the SHA-256 of the lower-cased operator token, not the token.
# This lets the scanner recognize the known token without publishing it in
# the release tooling or generated specification.
OPERATOR_TOKEN_SHA256S = {
    "69df503cfc88dfc746c27933e07eab08b6b060022e44c99044bdec1724d89cc2",
}

BYTE_LEAK_PATTERNS: tuple[tuple[str, re.Pattern[bytes]], ...] = (
    ("local_path", re.compile(rb"/(?:Users|home|root|var/folders)/[^\x00\r\n\t \"']+", re.I)),
    ("local_path", re.compile(rb"[A-Za-z]:\\\\Users\\\\[^\x00\r\n\t \"']+", re.I)),
    ("local_path", re.compile(rb"file://", re.I)),
    ("cloud_reference", re.compile(rb"arn:aws(?:-us-gov|-cn)?:", re.I)),
    ("cloud_reference", re.compile(rb"(?:s3|https?)://[^\x00\r\n\t ]*amazonaws\.com", re.I)),
    ("cloud_reference", re.compile(rb"s3://", re.I)),
    ("cloud_reference", re.compile(rb"\b(?:i|vpc|subnet|sg)-[0-9a-f]{8,17}\b", re.I)),
    ("credential", re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("credential", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
TOKEN_RE = re.compile(r"[a-z0-9._+-]+")
EMAIL_RE = re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", re.I)


class Refusal(RuntimeError):
    """A closure, authentication, safety, or reproduction predicate failed."""


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _reject_constant(value: str) -> None:
    raise Refusal(f"non-standard JSON numeric constant: {value}")


def _unique_object(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Refusal(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(data: bytes, label: str) -> Mapping[str, Any]:
    try:
        text = data.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{label} is not strict UTF-8 JSON: {error}") from error
    if not isinstance(value, Mapping):
        raise Refusal(f"{label} must contain a JSON object")
    return value


def normalized_relative(value: str | PurePosixPath) -> PurePosixPath:
    raw = str(value)
    if not raw or "\x00" in raw or "\\" in raw:
        raise Refusal(f"unsafe relative path: {raw!r}")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise Refusal(f"unsafe relative path: {raw!r}")
    return path


def repository_path(root: Path, relative: str | PurePosixPath) -> Path:
    rel = normalized_relative(relative)
    root_resolved = root.resolve()
    candidate = root_resolved.joinpath(*rel.parts)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise Refusal(f"missing source file {rel}: {error}") from error
    try:
        resolved.relative_to(root_resolved)
    except ValueError as error:
        raise Refusal(f"source escapes repository root: {rel}") from error
    current = root_resolved
    for part in rel.parts:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except OSError as error:
            raise Refusal(f"cannot lstat source component {current}: {error}") from error
        if stat.S_ISLNK(mode):
            raise Refusal(f"symlink forbidden in source path: {rel}")
    if not resolved.is_file():
        raise Refusal(f"source is not a regular file: {rel}")
    return resolved


def stable_read(path: Path) -> bytes:
    try:
        before = path.stat()
    except OSError as error:
        raise Refusal(f"cannot stat {path}: {error}") from error
    if not stat.S_ISREG(before.st_mode) or path.is_symlink():
        raise Refusal(f"not a non-symlink regular file: {path}")
    try:
        data = path.read_bytes()
    except OSError as error:
        raise Refusal(f"cannot read {path}: {error}") from error
    after = path.stat()
    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if identity_before != identity_after or len(data) != before.st_size:
        raise Refusal(f"file changed while read: {path}")
    return data


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(root: Path, relative: str | PurePosixPath) -> dict[str, Any]:
    rel = normalized_relative(relative)
    data = stable_read(repository_path(root, rel))
    return {"path": str(rel), "sha256": digest_bytes(data), "bytes": len(data)}


def leak_classes(data: bytes) -> list[str]:
    classes = {label for label, pattern in BYTE_LEAK_PATTERNS if pattern.search(data)}
    try:
        text = data.decode("utf-8").lower()
    except UnicodeDecodeError:
        text = ""
    if text:
        if EMAIL_RE.search(text):
            classes.add("email")
        for token in TOKEN_RE.findall(text):
            if digest_bytes(token.encode("utf-8")) in OPERATOR_TOKEN_SHA256S:
                classes.add("operator_identifier")
                break
        if re.search(r"\b\d{12}\b", text) and (
            "aws" in text or "account" in text or "amazon" in text
        ):
            classes.add("cloud_account_identifier")
    return sorted(classes)


def require_no_leaks(data: bytes, label: str) -> None:
    found = leak_classes(data)
    if found:
        raise Refusal(f"release leakage in {label}: {', '.join(found)}")


def _json_string_leaks(value: Any, pointer: str = "") -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if isinstance(value, str):
        classes = leak_classes(value.encode("utf-8"))
        if classes:
            findings.append({"json_pointer": pointer or "/", "classes": classes})
    elif isinstance(value, Mapping):
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            findings.extend(_json_string_leaks(child, f"{pointer}/{escaped}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_json_string_leaks(child, f"{pointer}/{index}"))
    return findings


def selected_cache_names(length: int) -> list[str]:
    prefix = length - 1
    names: list[str] = []
    for q in range(4, length):
        names.extend(
            (
                f"admission_n_{prefix:02d}_q_{q:02d}_blank.i32",
                f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32",
            )
        )
    return sorted(names)


def cache_directory(length: int) -> PurePosixPath:
    return CACHE_BASE / f"L{length}"


def source_manifest_path(length: int) -> PurePosixPath:
    return cache_directory(length) / "CACHE_MANIFEST.json"


def workspace_shard_path(length: int, q: int) -> PurePosixPath:
    return WORKSPACE_BASE / f"L{length}" / "sharp" / f"prefix_{length - 1:02d}" / f"q_{q:02d}.npy"


def public_manifest(root: Path, length: int) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_rel = source_manifest_path(length)
    raw = stable_read(repository_path(root, manifest_rel))
    source_sha = digest_bytes(raw)
    source = strict_json_bytes(raw, str(manifest_rel))
    expected_leaks = [
        {
            "json_pointer": "/canonical_cache_root",
            "classes": ["local_path", "operator_identifier"],
        }
    ]
    actual_leaks = _json_string_leaks(source)
    if actual_leaks != expected_leaks:
        raise Refusal(
            f"unexpected source-manifest leakage for L{length}: {actual_leaks!r}"
        )
    if source.get("L") != length:
        raise Refusal(f"cache manifest L mismatch for L{length}")
    ledger = source.get("files")
    if not isinstance(ledger, list):
        raise Refusal(f"cache manifest files ledger absent for L{length}")
    by_name: dict[str, Mapping[str, Any]] = {}
    for record in ledger:
        if not isinstance(record, Mapping) or not isinstance(record.get("path"), str):
            raise Refusal(f"malformed cache record for L{length}")
        name = record["path"]
        if name in by_name:
            raise Refusal(f"duplicate cache record for L{length}: {name}")
        by_name[name] = record
    names = selected_cache_names(length)
    missing = sorted(set(names) - set(by_name))
    if missing:
        raise Refusal(f"source cache manifest lacks selected records: {missing}")
    selected: list[dict[str, Any]] = []
    total = 0
    for name in names:
        record = copy.deepcopy(dict(by_name[name]))
        try:
            expected_bytes = int(record["bytes"])
            expected_sha = str(record["sha256"])
        except (KeyError, TypeError, ValueError) as error:
            raise Refusal(f"malformed selected cache record {name}: {error}") from error
        data = stable_read(repository_path(root, cache_directory(length) / name))
        if len(data) != expected_bytes or digest_bytes(data) != expected_sha:
            raise Refusal(f"selected cache payload authentication failed: L{length}/{name}")
        total += len(data)
        selected.append(record)
    keep = (
        "schema",
        "status",
        "L",
        "basis_order",
        "lineage_identity",
        "claim_boundary",
        "hamiltonian_exchange_coefficient",
    )
    projection = {key: copy.deepcopy(source[key]) for key in keep if key in source}
    projection["canonical_cache_root"] = str(cache_directory(length))
    projection["files"] = selected
    projection["public_projection"] = {
        "schema": PROJECTION_SCHEMA,
        "source_manifest_sha256": source_sha,
        "selection": "MINIMUM_INPUTS_FOR_EXTRACT_LOWER_BOUND_PROGRESSION_V001",
        "selected_file_count": len(selected),
        "selected_file_bytes": total,
        "removed_source_leak_fields": ["/canonical_cache_root"],
    }
    encoded = canonical_json(projection)
    require_no_leaks(encoded, f"public L{length} cache manifest")
    metadata = {
        "length": length,
        "source": str(manifest_rel),
        "source_sha256": source_sha,
        "source_bytes": len(raw),
        "source_expected_leaks": expected_leaks,
        "public_sha256": digest_bytes(encoded),
        "public_bytes": len(encoded),
        "selected_file_count": len(selected),
        "selected_file_bytes": total,
    }
    return projection, metadata


def _lower_member(
    root: Path,
    source: PurePosixPath,
    *,
    archive_relative: PurePosixPath | None = None,
    kind: str = "exact",
    public_data: bytes | None = None,
) -> dict[str, Any]:
    archive_rel = archive_relative or source
    archive = ARCHIVE_PREFIX / archive_rel
    if public_data is None:
        data = stable_read(repository_path(root, source))
    else:
        data = public_data
    require_no_leaks(data, str(source))
    suffix = source.suffix.lower()
    binary = suffix in (".i32", ".npy", ".u32")
    return {
        "source": str(source),
        "archive": str(archive),
        "sha256": digest_bytes(data),
        "bytes": len(data),
        "kind": kind,
        "binary": binary,
        "scan_release_markers": not binary,
    }


def lower_ladder_members(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    members = [_lower_member(root, EXTRACTOR), _lower_member(root, SUPPORT)]
    projections: list[dict[str, Any]] = []
    for length in (8, 10):
        projected, metadata = public_manifest(root, length)
        projection_data = canonical_json(projected)
        public_source = PurePosixPath(
            f"publication/zenodo_reproduction_v001/release_inputs/"
            f"L{length:02d}_CACHE_MANIFEST_MINIMAL_PUBLIC.json"
        )
        members.append(
            _lower_member(
                root,
                public_source,
                archive_relative=source_manifest_path(length),
                kind="path_neutral_manifest_projection",
                public_data=projection_data,
            )
        )
        projections.append(metadata)
        for name in selected_cache_names(length):
            members.append(_lower_member(root, cache_directory(length) / name))
        for q in range(4, length):
            members.append(_lower_member(root, workspace_shard_path(length, q)))
    members.sort(key=lambda item: item["archive"])
    if len(members) != 34:
        raise Refusal(f"minimum lower-ladder member census changed: {len(members)} != 34")
    if len({item["archive"] for item in members}) != len(members):
        raise Refusal("duplicate lower-ladder archive member")
    return members, projections


def generate_spec(root: Path) -> dict[str, Any]:
    root = root.resolve()
    members, projections = lower_ladder_members(root)
    total_bytes = sum(int(item["bytes"]) for item in members)
    binary_members = [
        item["archive"] for item in members if not item["scan_release_markers"]
    ]
    integration_entries = [
        {
            "source": item["source"],
            "archive": item["archive"],
            "required": True,
            "binary": item["binary"],
            "scan_release_markers": item["scan_release_markers"],
        }
        for item in members
    ]
    integration_entries.extend(
        (
            {
                "source": "publication/zenodo_reproduction_v001/lower_ladder_closure.py",
                "archive": "tools/lower_ladder_closure.py",
                "required": True,
                "binary": False,
                "scan_release_markers": True,
            },
            {
                "source": "publication/zenodo_reproduction_v001/LOWER_LADDER_CLOSURE_SPEC.json",
                "archive": "inventory/LOWER_LADDER_CLOSURE_SPEC.json",
                "required": True,
                "binary": False,
                "scan_release_markers": True,
            },
            {
                "source": "publication/zenodo_reproduction_v001/test_lower_ladder_closure.py",
                "archive": "tools/test_lower_ladder_closure.py",
                "required": True,
                "binary": False,
                "scan_release_markers": True,
            },
        )
    )
    return {
        "schema": SCHEMA,
        "claim_boundary": (
            "REPRODUCES_CACHED_L08_AND_L10_COMMON_LINEAGE_WEIGHTS_ONLY__"
            "DOES_NOT_RECONSTRUCT_CACHE_GENERATION_OR_CLAIM_L14"
        ),
        "expected_stdout": EXPECTED_STDOUT,
        "expected_values": EXPECTED_VALUES,
        "archive_prefix": str(ARCHIVE_PREFIX),
        "minimum_closure": {
            "member_count": len(members),
            "total_bytes": total_bytes,
            "members": members,
            "binary_member_count": len(binary_members),
            "binary_members": binary_members,
            "cache_manifest_projections": projections,
        },
        "integration": {
            "manifest_entries": integration_entries,
            "allowed_suffix_additions": [".i32", ".npy", ".u32"],
            "builder_capability_required": (
                "entries explicitly marked binary=true must be non-template, copied and hashed "
                "as bytes without UTF-8 decoding, and exempt only from text placeholder/marker scans"
            ),
            "integration_precondition": (
                "do not add the binary entries until build_capsule.py recognizes binary=true; "
                "adding suffixes or scan_release_markers=false alone is insufficient"
            ),
            "extracted_verification_command": (
                "python3 tools/lower_ladder_closure.py verify-archive --capsule-root ."
            ),
        },
    }


def _checked_spec() -> Mapping[str, Any]:
    path = SPEC_PATH if SPEC_PATH.is_file() else EXTRACTED_SPEC_PATH
    return strict_json_bytes(stable_read(path), str(path))


def verify_source(root: Path) -> dict[str, Any]:
    expected = canonical_json(generate_spec(root))
    actual = stable_read(SPEC_PATH)
    if actual != expected:
        raise Refusal(
            "LOWER_LADDER_CLOSURE_SPEC.json is stale; regenerate only after reviewing source changes"
        )
    for length, destination in PUBLIC_MANIFEST_PATHS.items():
        projected, _ = public_manifest(root, length)
        expected_manifest = canonical_json(projected)
        actual_manifest = stable_read(destination)
        if actual_manifest != expected_manifest:
            raise Refusal(f"checked-in public cache projection is stale: {destination.name}")
    spec = _checked_spec()
    return {
        "status": "VERIFIED_SOURCE_CLOSURE",
        "member_count": spec["minimum_closure"]["member_count"],
        "total_bytes": spec["minimum_closure"]["total_bytes"],
        "expected_stdout": spec["expected_stdout"],
    }


def write_artifacts(root: Path, replace: bool) -> None:
    outputs: list[tuple[Path, bytes]] = []
    for length, destination in PUBLIC_MANIFEST_PATHS.items():
        projected, _ = public_manifest(root, length)
        outputs.append((destination, canonical_json(projected)))
    outputs.append((SPEC_PATH, canonical_json(generate_spec(root))))
    for destination, data in outputs:
        if destination.exists() and not replace:
            raise Refusal(f"refusing to overwrite without --replace: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    verify_source(root)


def _safe_destination(root: Path, archive: str) -> Path:
    rel = normalized_relative(archive)
    root_resolved = root.resolve()
    candidate = root_resolved.joinpath(*rel.parts)
    try:
        candidate.parent.resolve().relative_to(root_resolved)
    except ValueError as error:
        raise Refusal(f"archive destination escapes capsule root: {archive}") from error
    return candidate


def materialize(root: Path, capsule_root: Path, link: bool = False) -> dict[str, Any]:
    verify_source(root)
    spec = _checked_spec()
    capsule_root.mkdir(parents=True, exist_ok=True)
    prefix_path = _safe_destination(capsule_root, str(ARCHIVE_PREFIX))
    if prefix_path.exists() and any(prefix_path.iterdir()):
        raise Refusal(f"archive prefix already exists and is nonempty: {prefix_path}")
    for member in spec["minimum_closure"]["members"]:
        source = repository_path(root, member["source"])
        destination = _safe_destination(capsule_root, member["archive"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            raise Refusal(f"refusing to overwrite archive member: {destination}")
        if link:
            os.link(source, destination)
        else:
            shutil.copyfile(source, destination)
            os.chmod(destination, 0o444)
    return verify_archive(capsule_root)


def _archive_files(prefix: Path) -> list[Path]:
    if not prefix.is_dir() or prefix.is_symlink():
        raise Refusal(f"archive prefix missing or unsafe: {prefix}")
    files: list[Path] = []
    for directory, dirnames, filenames in os.walk(prefix, followlinks=False):
        base = Path(directory)
        for name in dirnames:
            if (base / name).is_symlink():
                raise Refusal(f"symlink directory forbidden in archive: {base / name}")
        for name in filenames:
            path = base / name
            if path.is_symlink() or not path.is_file():
                raise Refusal(f"non-regular archive member: {path}")
            files.append(path)
    return files


def verify_archive(capsule_root: Path, python: str | None = None) -> dict[str, Any]:
    spec = _checked_spec()
    expected_members = {
        item["archive"]: item for item in spec["minimum_closure"]["members"]
    }
    prefix = _safe_destination(capsule_root, str(ARCHIVE_PREFIX))
    actual_paths = _archive_files(prefix)
    actual_names = {
        str(PurePosixPath(*path.relative_to(capsule_root.resolve()).parts)): path
        for path in actual_paths
    }
    missing = sorted(set(expected_members) - set(actual_names))
    extra = sorted(set(actual_names) - set(expected_members))
    if missing or extra:
        raise Refusal(f"archive member-set mismatch: missing={missing} extra={extra}")
    for archive, member in expected_members.items():
        data = stable_read(actual_names[archive])
        if len(data) != member["bytes"] or digest_bytes(data) != member["sha256"]:
            raise Refusal(f"archive authentication failed: {archive}")
        require_no_leaks(data, archive)
    executable = python or sys.executable
    extractor = _safe_destination(capsule_root, str(ARCHIVE_PREFIX / EXTRACTOR))
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(
            [executable, str(extractor)],
            cwd=prefix,
            env=environment,
            text=True,
            encoding="utf-8",
            errors="strict",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise Refusal(f"could not execute extracted lower-ladder calculation: {error}") from error
    if completed.returncode != 0:
        raise Refusal(
            f"extracted calculation failed ({completed.returncode}): {completed.stderr.strip()}"
        )
    if completed.stderr:
        raise Refusal(f"extracted calculation wrote stderr: {completed.stderr!r}")
    if completed.stdout != spec["expected_stdout"]:
        raise Refusal(
            f"lower-ladder output mismatch: expected={spec['expected_stdout']!r} "
            f"actual={completed.stdout!r}"
        )
    return {
        "status": "VERIFIED_EXTRACTED_LOWER_LADDER",
        "member_count": len(expected_members),
        "stdout": completed.stdout,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--repository-root", type=Path, default=DEFAULT_REPOSITORY_ROOT
    )
    sub = result.add_subparsers(dest="command", required=True)
    write = sub.add_parser("write-artifacts")
    write.add_argument("--replace", action="store_true")
    sub.add_parser("verify-source")
    create = sub.add_parser("materialize")
    create.add_argument("--capsule-root", type=Path, required=True)
    create.add_argument(
        "--link",
        action="store_true",
        help="hard-link exact members (tests only; never use for a release artifact)",
    )
    verify = sub.add_parser("verify-archive")
    verify.add_argument("--capsule-root", type=Path, required=True)
    verify.add_argument("--python", default=None)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "write-artifacts":
            write_artifacts(arguments.repository_root, arguments.replace)
            print("WROTE_AND_VERIFIED_LOWER_LADDER_CLOSURE")
        elif arguments.command == "verify-source":
            result = verify_source(arguments.repository_root)
            print(result["status"])
            print(f"members={result['member_count']} bytes={result['total_bytes']}")
            print(result["expected_stdout"], end="")
        elif arguments.command == "materialize":
            result = materialize(
                arguments.repository_root, arguments.capsule_root, arguments.link
            )
            print(result["status"])
            print(result["stdout"], end="")
        elif arguments.command == "verify-archive":
            result = verify_archive(arguments.capsule_root, arguments.python)
            print(result["status"])
            print(result["stdout"], end="")
        else:  # pragma: no cover - argparse enforces this
            raise Refusal(f"unknown command: {arguments.command}")
    except Refusal as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
