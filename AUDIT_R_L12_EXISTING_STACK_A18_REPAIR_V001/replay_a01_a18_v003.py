#!/usr/bin/env python3
"""Bounded V003 restart for the failed relative-root A05 cache set.

V001 and V002 remain immutable.  Before V002 resumes, this layer authenticates
the completed original retirement, moves the exact failed five-cache parent as
one owner-once directory into fixed obstruction custody, and temporarily makes
only publisher data-path arguments absolute.  Publisher script entry paths
remain the registered relative paths consumed by the authenticated runner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import types
from pathlib import Path, PurePosixPath
from typing import Final, Mapping, Sequence


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
V002_PATH: Final[Path] = HERE / "replay_a01_a18_v002.py"
V002_SHA256: Final[str] = (
    "aea072cdc4786f45c0dfb00b098dfacef5289b48fd48382fc19652516162c18b"
)
V002_MODULE_NAME: Final[str] = "authenticated_replay_a01_a18_v002"
CENSUS_PATH: Final[Path] = HERE / "FAILED_CACHE_OBSTRUCTION_CENSUS_V003.json"
# Filled only after the one-time noncanonical census capture, before review.
CENSUS_SHA256: Final[str] = (
    "2f14a2380991efcc46ea139b7271be16acc1392f3b1c2fa186d20954b98394b5"
)
SOURCE_RELATIVE: Final[str] = (
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012"
)
CUSTODY_ROOT_RELATIVE: Final[str] = (
    "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001/"
    "FAILED_CACHE_OBSTRUCTION_CUSTODY_V003"
)
CUSTODY_TREE_NAME: Final[str] = "CACHE_PAYLOADS_V012"
INTENT_NAME: Final[str] = "FAILED_CACHE_CUSTODY_INTENT_V003.json"
RECEIPT_NAME: Final[str] = "FAILED_CACHE_CUSTODY_RECEIPT_V003.json"
ORIGINAL_RETIREMENT_RECEIPT_SHA256: Final[str] = (
    "5c8d714973bb2ac22b50643e8f84de042e7a41e282f8f3d25c7d32e64c10fbf0"
)
ORIGINAL_AUTHORIZATION: Final[str] = "EXECUTE_EXACT_A01_A18_REPLAY_V001"
V003_AUTHORIZATION: Final[str] = (
    "EXECUTE_EXACT_FAILED_CACHE_CUSTODY_AND_ABSOLUTE_PATH_REPLAY_V003"
)
FAILED_CACHE_RECEIPT_SHA256: Final[str] = (
    "c38fa0ac4c18f11b3fd9ec171c5b909e0c6ab4c1647cd52bf68b0ae9147e854f"
)
LENGTHS: Final[tuple[int, ...]] = (4, 6, 8, 10, 12)
RESTART_BOUNDARY_SHA256: Final[dict[str, str]] = {
    "A01_FREEZE_AND_SOURCE_PACKET":
        "a6997822fd2daa2be0079e67d81833f1eac69fe01c6ff0b9188560f2c1234395",
    "A02_NONPHYSICAL_PREFLIGHT":
        "73ab3c2778f11b3d768bf818865fac120210b8c5417a1aa0bb19edc874bda57c",
    "A03_PREPAYLOAD_AUDIT":
        "a50044557c5316d50f3b1e4cfefb035c674321a96147690aa3017b2e01cb2301",
    "A04_UNIVERSAL_CUSTODY_GATE":
        "e9e1714852d03cca9e6dcc90745e16a6a7722bf41e29e4717d5032a9cd250256",
    "A27_MUTATION_LEDGER":
        "c8a8b23261d3376d69e2175512ae946ba3cdde96a464ac4ae33cb06010c4bf90",
}
RESTART_BOUNDARY_PATHS: Final[dict[str, str]] = {
    "A01_FREEZE_AND_SOURCE_PACKET":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    "A02_NONPHYSICAL_PREFLIGHT":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_RESULT_V001.json",
    "A03_PREPAYLOAD_AUDIT":
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
    "A04_UNIVERSAL_CUSTODY_GATE":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
    "A27_MUTATION_LEDGER":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "PREFLIGHT_MUTATION_LEDGER_V001.json",
}
REQUIRED_ABSENT_BEFORE_CUSTODY: Final[tuple[str, ...]] = (
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/POSTBUILD_PAYLOAD_AUDIT_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_EXECUTION_GATE_V012.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_GATE_HOSTILE_AUDIT_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_V012.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json",
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_HOSTILE_L10_CROSS_GATE_V001.json",
)


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _read_frozen_v002() -> bytes:
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(V002_PATH, flags)
    try:
        before = os.fstat(descriptor)
        named = os.stat(V002_PATH, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_nlink != 1 or before.st_mode & 0o222
            or _identity(before) != _identity(named)
        ):
            raise RuntimeError("frozen V002 replay custody mismatch")
        raw = bytearray()
        digest = hashlib.sha256()
        offset = 0
        while True:
            block = os.pread(descriptor, 16 * 2**20, offset)
            if not block:
                break
            raw.extend(block)
            digest.update(block)
            offset += len(block)
        after = os.fstat(descriptor)
        named_after = os.stat(V002_PATH, follow_symlinks=False)
        if (
            _identity(before) != _identity(after)
            or _identity(after) != _identity(named_after)
            or digest.hexdigest() != V002_SHA256
        ):
            raise RuntimeError("frozen V002 replay hash/identity mismatch")
        return bytes(raw)
    finally:
        os.close(descriptor)


def _load_v002() -> types.ModuleType:
    existing = sys.modules.get(V002_MODULE_NAME)
    if existing is not None:
        if (
            getattr(existing, "__file__", None) != str(V002_PATH)
            or getattr(existing, "__authenticated_sha256__", None)
            != V002_SHA256
        ):
            raise RuntimeError("frozen V002 replay module alias")
        return existing
    raw = _read_frozen_v002()
    module = types.ModuleType(V002_MODULE_NAME)
    module.__file__ = str(V002_PATH)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = V002_SHA256
    sys.modules[V002_MODULE_NAME] = module
    try:
        exec(compile(raw, str(V002_PATH), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(V002_MODULE_NAME, None)
        raise
    _read_frozen_v002()
    return module


v002 = _load_v002()
v001 = v002.v001
retirement = v001.retirement
Refusal = v001.Refusal
PublisherAction = v001.PublisherAction
ORIGINAL_EXISTING_PUBLISHER_ACTIONS: Final[object] = v001.existing_publisher_actions


def _relative(value: object, label: str) -> str:
    return retirement.canonical_relative(value, label)


def _regular_file_row(path: Path, logical: str) -> dict[str, object]:
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Refusal(f"failed-cache file open failed: {logical}") from error
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_nlink != 1 or before.st_mode & 0o222
            or _identity(before) != _identity(named)
        ):
            raise Refusal(f"failed-cache file is not owner-once: {logical}")
        digest = retirement.descriptor_sha256(descriptor)
        after = os.fstat(descriptor)
        if _identity(before) != _identity(after):
            raise Refusal(f"failed-cache file drifted while held: {logical}")
        return {
            "path": logical,
            "device": before.st_dev,
            "inode": before.st_ino,
            "bytes": before.st_size,
            "mode": stat.S_IMODE(before.st_mode),
            "nlink": before.st_nlink,
            "sha256": digest,
        }
    finally:
        os.close(descriptor)


def _tree_inventory(path: Path) -> dict[str, object]:
    if path.is_symlink() or not path.is_dir():
        raise Refusal("failed-cache parent is absent or aliased")
    directories: list[dict[str, object]] = []
    files: list[dict[str, object]] = []
    for current_text, names, filenames in os.walk(path, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        relative = current.relative_to(path)
        logical = "." if relative == Path(".") else relative.as_posix()
        metadata = os.stat(current, follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise Refusal(f"failed-cache directory alias: {logical}")
        directories.append({
            "path": logical,
            "device": metadata.st_dev,
            "inode": metadata.st_ino,
            "bytes": metadata.st_size,
            "mode": stat.S_IMODE(metadata.st_mode),
            "nlink": metadata.st_nlink,
        })
        for name in names:
            child = current / name
            child_metadata = os.stat(child, follow_symlinks=False)
            if (
                not stat.S_ISDIR(child_metadata.st_mode)
                or stat.S_ISLNK(child_metadata.st_mode)
            ):
                raise Refusal(f"failed-cache tree contains alias: {child}")
        for name in filenames:
            child_logical = name if logical == "." else f"{logical}/{name}"
            files.append(_regular_file_row(current / name, child_logical))
    directories.sort(key=lambda row: str(row["path"]))
    files.sort(key=lambda row: str(row["path"]))
    material = {"directories": directories, "files": files}
    content_material = {
        "directories": [
            {"path": row["path"], "mode": row["mode"]}
            for row in directories
        ],
        "files": [
            {
                "path": row["path"], "bytes": row["bytes"],
                "mode": row["mode"], "sha256": row["sha256"],
            }
            for row in files
        ],
    }
    return {
        **material,
        "directory_count": len(directories),
        "file_count": len(files),
        "total_bytes": sum(int(row["bytes"]) for row in files),
        "inventory_sha256": retirement.sha256_bytes(
            retirement.canonical_json_bytes(material)
        ),
        "content_inventory_sha256": retirement.sha256_bytes(
            retirement.canonical_json_bytes(content_material)
        ),
    }


def _stable_json(path: Path, label: str) -> tuple[dict[str, object], str]:
    record, digest, _raw = v001._stable_owner_once_json(path, label)
    return record, digest


def build_census(root: Path, source_relative: str = SOURCE_RELATIVE,
                 custody_relative: str = CUSTODY_ROOT_RELATIVE) -> dict[str, object]:
    """Measure the exact current failed cache tree without changing it."""
    v001.retirement.ensure_root(root)
    source_relative = _relative(source_relative, "failed-cache source")
    custody_relative = _relative(custody_relative, "failed-cache custody")
    source = root.joinpath(*PurePosixPath(source_relative).parts)
    inventory = _tree_inventory(source)
    boundary: dict[str, str] = {}
    for artifact_id, relative in RESTART_BOUNDARY_PATHS.items():
        _record, digest = _stable_json(
            root.joinpath(*PurePosixPath(relative).parts),
            f"V003 restart boundary {artifact_id}",
        )
        if root == ROOT and digest != RESTART_BOUNDARY_SHA256[artifact_id]:
            raise Refusal(f"V003 restart boundary changed: {artifact_id}")
        boundary[artifact_id] = digest
    for relative in REQUIRED_ABSENT_BEFORE_CUSTODY:
        if retirement.path_exists(root.joinpath(*PurePosixPath(relative).parts)):
            raise Refusal(f"V003 precustody path must be absent: {relative}")
    mismatches: list[dict[str, object]] = []
    for length in LENGTHS:
        relative_manifest = f"L{length}/CACHE_MANIFEST.json"
        manifest, manifest_sha = _stable_json(
            source / relative_manifest,
            f"failed-cache L{length} manifest",
        )
        observed = manifest.get("canonical_cache_root")
        required = str(root / source_relative / f"L{length}")
        if (
            manifest.get("L") != length or type(observed) is not str
            or observed != f"{source_relative}/L{length}"
            or observed == required
        ):
            raise Refusal(f"failed-cache L{length} mismatch signature changed")
        mismatches.append({
            "L": length,
            "path": relative_manifest,
            "sha256": manifest_sha,
            "observed_canonical_cache_root": observed,
            "required_canonical_cache_root": required,
            "mismatch": "RELATIVE_INSTEAD_OF_ABSOLUTE",
        })
    return {
        "schema": "V012_FAILED_CACHE_OBSTRUCTION_CENSUS_V003",
        "classification": "EXACT_NONEXECUTED_FAILED_CACHE_CENSUS",
        "source_path": source_relative,
        "custody_root": custody_relative,
        "custody_tree_name": CUSTODY_TREE_NAME,
        "directories": inventory["directories"],
        "files": inventory["files"],
        "directory_count": inventory["directory_count"],
        "file_count": inventory["file_count"],
        "total_bytes": inventory["total_bytes"],
        "inventory_sha256": inventory["inventory_sha256"],
        "content_inventory_sha256": inventory["content_inventory_sha256"],
        "manifest_path_mismatches": mismatches,
        "manifest_mismatch_count": len(mismatches),
        "restart_boundary_sha256": boundary,
        "required_absent_before_custody": list(REQUIRED_ABSENT_BEFORE_CUSTODY),
        "executed": False,
        "claim_boundary": (
            "FAILED_CACHE_PATH_OBSTRUCTION_CENSUS_ONLY__NO_PAYLOAD_PHYSICS_"
            "HISTORY_A18_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def validate_census(census: dict[str, object], root: Path) -> dict[str, object]:
    expected_keys = {
        "schema", "classification", "source_path", "custody_root",
        "custody_tree_name", "directories", "files", "directory_count",
        "file_count", "total_bytes", "inventory_sha256",
        "content_inventory_sha256", "restart_boundary_sha256",
        "required_absent_before_custody",
        "manifest_path_mismatches", "manifest_mismatch_count", "executed",
        "claim_boundary",
    }
    if (
        set(census) != expected_keys
        or census.get("schema") != "V012_FAILED_CACHE_OBSTRUCTION_CENSUS_V003"
        or census.get("classification")
        != "EXACT_NONEXECUTED_FAILED_CACHE_CENSUS"
        or census.get("executed") is not False
        or census.get("custody_tree_name") != CUSTODY_TREE_NAME
    ):
        raise Refusal("failed-cache census identity/keyset mismatch")
    source_relative = _relative(census.get("source_path"), "census source")
    custody_relative = _relative(census.get("custody_root"), "census custody")
    if source_relative == custody_relative:
        raise Refusal("failed-cache source/custody alias")
    directories = census.get("directories")
    files = census.get("files")
    mismatches = census.get("manifest_path_mismatches")
    if type(directories) is not list or type(files) is not list \
            or type(mismatches) is not list:
        raise Refusal("failed-cache census list type mismatch")
    directory_keys = {"path", "device", "inode", "bytes", "mode", "nlink"}
    file_keys = directory_keys | {"sha256"}
    for index, row in enumerate(directories):
        if type(row) is not dict or set(row) != directory_keys:
            raise Refusal(f"failed-cache directory row {index} mismatch")
    for index, row in enumerate(files):
        if type(row) is not dict or set(row) != file_keys:
            raise Refusal(f"failed-cache file row {index} mismatch")
        if row.get("nlink") != 1 or int(row.get("mode", 0)) & 0o222:
            raise Refusal(f"failed-cache file row {index} is not owner-once")
        if type(row.get("sha256")) is not str or len(row["sha256"]) != 64:
            raise Refusal(f"failed-cache file row {index} digest mismatch")
    directory_paths = [row["path"] for row in directories]
    file_paths = [row["path"] for row in files]
    if (
        directory_paths != sorted(directory_paths)
        or file_paths != sorted(file_paths)
        or len(directory_paths) != len(set(directory_paths))
        or len(file_paths) != len(set(file_paths))
        or not directory_paths or directory_paths[0] != "."
    ):
        raise Refusal("failed-cache census path ordering mismatch")
    material = {"directories": directories, "files": files}
    content_material = {
        "directories": [
            {"path": row["path"], "mode": row["mode"]}
            for row in directories
        ],
        "files": [
            {
                "path": row["path"], "bytes": row["bytes"],
                "mode": row["mode"], "sha256": row["sha256"],
            }
            for row in files
        ],
    }
    if (
        census.get("directory_count") != len(directories)
        or census.get("file_count") != len(files)
        or census.get("total_bytes")
        != sum(int(row["bytes"]) for row in files)
        or census.get("inventory_sha256")
        != retirement.sha256_bytes(retirement.canonical_json_bytes(material))
        or census.get("content_inventory_sha256")
        != retirement.sha256_bytes(
            retirement.canonical_json_bytes(content_material)
        )
    ):
        raise Refusal("failed-cache census aggregate mismatch")
    boundary = census.get("restart_boundary_sha256")
    absences = census.get("required_absent_before_custody")
    if (
        type(boundary) is not dict or boundary != RESTART_BOUNDARY_SHA256
        or absences != list(REQUIRED_ABSENT_BEFORE_CUSTODY)
    ):
        raise Refusal("failed-cache restart boundary census mismatch")
    if len(mismatches) != len(LENGTHS) or census.get("manifest_mismatch_count") != 5:
        raise Refusal("failed-cache manifest mismatch census count changed")
    expected_mismatch_keys = {
        "L", "path", "sha256", "observed_canonical_cache_root",
        "required_canonical_cache_root", "mismatch",
    }
    if len(mismatches) != len(LENGTHS):
        raise Refusal("failed-cache manifest mismatch census count changed")
    for row, length in zip(mismatches, LENGTHS):
        if type(row) is not dict or set(row) != expected_mismatch_keys:
            raise Refusal("failed-cache manifest row keyset mismatch")
        if (
            row.get("L") != length
            or row.get("path") != f"L{length}/CACHE_MANIFEST.json"
            or row.get("observed_canonical_cache_root")
            != f"{source_relative}/L{length}"
            or row.get("required_canonical_cache_root")
            != str(root / source_relative / f"L{length}")
            or row.get("mismatch") != "RELATIVE_INSTEAD_OF_ABSOLUTE"
        ):
            raise Refusal("failed-cache manifest mismatch signature changed")
    return census


def load_census(path: Path = CENSUS_PATH, root: Path = ROOT) -> dict[str, object]:
    metadata = os.stat(path, follow_symlinks=False)
    if path == CENSUS_PATH and (
        not stat.S_ISREG(metadata.st_mode) or path.is_symlink()
        or metadata.st_nlink != 1 or metadata.st_mode & 0o222
    ):
        raise Refusal("frozen failed-cache census custody mismatch")
    raw = path.read_bytes()
    if path == CENSUS_PATH and retirement.sha256_bytes(raw) != CENSUS_SHA256:
        raise Refusal("frozen failed-cache census digest mismatch")
    return validate_census(retirement.strict_json(raw, "failed-cache census"), root)


def inspect_tree(path: Path, census: Mapping[str, object]) -> None:
    inventory = _tree_inventory(path)
    for key in (
        "directories", "files", "directory_count", "file_count",
        "total_bytes", "inventory_sha256",
        "content_inventory_sha256",
    ):
        if inventory[key] != census[key]:
            raise Refusal(f"failed-cache tree differs from census: {key}")


def authenticate_restart_boundary(
    root: Path, census: Mapping[str, object], *, require_absences: bool,
) -> None:
    if census.get("restart_boundary_sha256") != RESTART_BOUNDARY_SHA256:
        raise Refusal("V003 restart boundary binding mismatch")
    for artifact_id, relative in RESTART_BOUNDARY_PATHS.items():
        _record, digest = _stable_json(
            root.joinpath(*PurePosixPath(relative).parts),
            f"V003 restart boundary {artifact_id}",
        )
        if digest != RESTART_BOUNDARY_SHA256[artifact_id]:
            raise Refusal(f"V003 restart boundary changed: {artifact_id}")
    if require_absences:
        for relative in census["required_absent_before_custody"]:
            path = root.joinpath(*PurePosixPath(str(relative)).parts)
            if retirement.path_exists(path):
                raise Refusal(f"V003 precustody path must be absent: {relative}")


def _fsync_tree(path: Path) -> None:
    if path.is_symlink() or not path.is_dir():
        raise Refusal("failed-cache fsync root is absent or aliased")
    directories: list[Path] = []
    for current_text, names, filenames in os.walk(path, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        directories.append(current)
        for name in names:
            child = current / name
            metadata = os.stat(child, follow_symlinks=False)
            if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
                raise Refusal("failed-cache fsync encountered directory alias")
        for name in filenames:
            retirement.fsync_regular_file(current / name, str(current / name))
    for directory in sorted(directories, key=lambda value: len(value.parts), reverse=True):
        retirement.fsync_directory(directory)


def _content_inventory_sha256(path: Path) -> str:
    """Hash path/content/mode while allowing a distinct partial rebuilt tree."""
    if path.is_symlink() or not path.is_dir():
        raise Refusal("rebuilt canonical cache parent is absent or aliased")
    directories: list[dict[str, object]] = []
    files: list[dict[str, object]] = []
    for current_text, names, filenames in os.walk(path, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        relative = current.relative_to(path)
        logical = "." if relative == Path(".") else relative.as_posix()
        metadata = os.stat(current, follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise Refusal("rebuilt canonical cache contains directory alias")
        directories.append({"path": logical, "mode": stat.S_IMODE(metadata.st_mode)})
        for name in names:
            child = current / name
            child_metadata = os.stat(child, follow_symlinks=False)
            if (
                not stat.S_ISDIR(child_metadata.st_mode)
                or stat.S_ISLNK(child_metadata.st_mode)
            ):
                raise Refusal("rebuilt canonical cache contains alias")
        for name in filenames:
            child = current / name
            child_logical = name if logical == "." else f"{logical}/{name}"
            flags = (
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            descriptor = os.open(child, flags)
            try:
                before = os.fstat(descriptor)
                named = os.stat(child, follow_symlinks=False)
                if (
                    not stat.S_ISREG(before.st_mode)
                    or stat.S_ISLNK(named.st_mode)
                    or _identity(before) != _identity(named)
                ):
                    raise Refusal("rebuilt canonical cache contains file alias")
                digest = retirement.descriptor_sha256(descriptor)
                after = os.fstat(descriptor)
                if _identity(before) != _identity(after):
                    raise Refusal("rebuilt canonical cache changed while held")
                files.append({
                    "path": child_logical,
                    "bytes": before.st_size,
                    "mode": stat.S_IMODE(before.st_mode),
                    "sha256": digest,
                })
            finally:
                os.close(descriptor)
    directories.sort(key=lambda row: str(row["path"]))
    files.sort(key=lambda row: str(row["path"]))
    return retirement.sha256_bytes(retirement.canonical_json_bytes({
        "directories": directories, "files": files,
    }))


def _require_exact_children(path: Path, names: set[str]) -> None:
    if path.is_symlink() or not path.is_dir():
        raise Refusal("failed-cache custody root is absent or aliased")
    observed = {child.name for child in path.iterdir()}
    if observed != names:
        raise Refusal("failed-cache custody contains unregistered entries")


def _transaction_paths(root: Path, census: Mapping[str, object]) -> tuple[Path, ...]:
    source = root.joinpath(*PurePosixPath(str(census["source_path"])).parts)
    custody = root.joinpath(*PurePosixPath(str(census["custody_root"])).parts)
    target = custody / str(census["custody_tree_name"])
    return source, custody, target, custody / INTENT_NAME, custody / RECEIPT_NAME


def _intent(census: Mapping[str, object]) -> dict[str, object]:
    return {
        "schema": "V012_FAILED_CACHE_CUSTODY_INTENT_V003",
        "census_sha256": retirement.sha256_bytes(
            retirement.publication_json_bytes(dict(census))
        ),
        "source_path": census["source_path"],
        "custody_root": census["custody_root"],
        "custody_tree_name": census["custody_tree_name"],
        "inventory_sha256": census["inventory_sha256"],
        "file_count": census["file_count"],
        "total_bytes": census["total_bytes"],
        "restart_boundary_sha256": census["restart_boundary_sha256"],
        "required_absent_before_custody": census[
            "required_absent_before_custody"
        ],
    }


def _authenticate_intent(path: Path, census: Mapping[str, object]) -> str:
    record, digest = _stable_json(path, "failed-cache custody intent")
    if record != _intent(census):
        raise Refusal("failed-cache custody intent mismatch")
    return digest


def _receipt(census: Mapping[str, object], intent_sha: str) -> dict[str, object]:
    return {
        "schema": "V012_FAILED_CACHE_CUSTODY_RECEIPT_V003",
        "classification": "PASS_EXACT_OWNER_ONCE_FAILED_CACHE_CUSTODY",
        "census_sha256": retirement.sha256_bytes(
            retirement.publication_json_bytes(dict(census))
        ),
        "intent_sha256": intent_sha,
        "source_absent": True,
        "custody_tree_authenticated": True,
        "retained_identity_equal": True,
        "manifest_mismatch_count": 5,
        "covered_lengths": list(LENGTHS),
        "atomic_move_count": 1,
        "atomic_move_scope": "WHOLE_FIVE_ROOT_CACHE_PARENT",
        "file_count": census["file_count"],
        "total_bytes": census["total_bytes"],
        "claim_boundary": (
            "FAILED_CACHE_OBSTRUCTION_CUSTODY_ONLY__NO_PAYLOAD_PHYSICS_"
            "HISTORY_A18_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def transaction_status(root: Path, census: Mapping[str, object]) -> str:
    source, custody, target, intent, receipt = _transaction_paths(root, census)
    states = tuple(retirement.path_exists(path) for path in (source, custody, target, intent, receipt))
    if states == (True, False, False, False, False):
        authenticate_restart_boundary(root, census, require_absences=True)
        inspect_tree(source, census)
        return "READY_EXACT_FAILED_CACHE_PRESENT"
    if states == (True, True, False, False, False):
        _require_exact_children(custody, set())
        authenticate_restart_boundary(root, census, require_absences=True)
        inspect_tree(source, census)
        return "RESTART_AFTER_EMPTY_CUSTODY_BEFORE_INTENT"
    if states in {
        (False, True, True, True, True),
        (True, True, True, True, True),
    }:
        _require_exact_children(custody, {CUSTODY_TREE_NAME, INTENT_NAME, RECEIPT_NAME})
        authenticate_restart_boundary(root, census, require_absences=False)
        intent_sha = _authenticate_intent(intent, census)
        record, _digest = _stable_json(receipt, "failed-cache custody receipt")
        if record != _receipt(census, intent_sha):
            raise Refusal("failed-cache custody receipt mismatch")
        inspect_tree(target, census)
        if retirement.path_exists(source):
            if _content_inventory_sha256(source) == census["content_inventory_sha256"]:
                raise Refusal("retired malformed cache tree reappeared at canonical path")
            return "PASS_COMPLETED_CUSTODY_WITH_DISTINCT_REBUILT_CANONICAL_PARENT"
        return "PASS_COMPLETED_CUSTODY_RECONCILED"
    if states == (True, True, False, True, False):
        _require_exact_children(custody, {INTENT_NAME})
        authenticate_restart_boundary(root, census, require_absences=True)
        _authenticate_intent(intent, census)
        inspect_tree(source, census)
        return "RESTART_AFTER_INTENT_BEFORE_RENAME"
    if states == (False, True, True, True, False):
        _require_exact_children(custody, {CUSTODY_TREE_NAME, INTENT_NAME})
        authenticate_restart_boundary(root, census, require_absences=True)
        _authenticate_intent(intent, census)
        inspect_tree(target, census)
        return "RESTART_AFTER_RENAME_BEFORE_RECEIPT"
    raise Refusal(f"failed-cache custody state mismatch: {states}")


def retire_failed_cache(root: Path, census: dict[str, object], *,
                        inject_at: str | None = None) -> dict[str, object]:
    """Move or reconcile one exact cache parent; never delete or overwrite."""
    retirement.ensure_root(root)
    validate_census(census, root)
    source, custody, target, intent_path, receipt_path = _transaction_paths(root, census)
    status = transaction_status(root, census)
    if status.startswith("PASS_COMPLETED_CUSTODY"):
        _record, receipt_sha = _stable_json(
            receipt_path, "failed-cache custody receipt",
        )
        return {"classification": status, "receipt_sha256": receipt_sha}
    if status == "READY_EXACT_FAILED_CACHE_PRESENT":
        parent = custody.parent
        if parent.is_symlink() or not parent.is_dir():
            raise Refusal("failed-cache custody parent is absent or aliased")
        os.mkdir(custody, 0o700)
        retirement.fsync_directory(parent)
        if inject_at == "after_custody_mkdir":
            raise RuntimeError("injected after failed-cache custody mkdir")
    if status in {
        "READY_EXACT_FAILED_CACHE_PRESENT",
        "RESTART_AFTER_EMPTY_CUSTODY_BEFORE_INTENT",
    }:
        retirement.publish_once(intent_path, _intent(census))
        _require_exact_children(custody, {INTENT_NAME})
        if inject_at == "after_intent":
            raise RuntimeError("injected after failed-cache intent")
    intent_sha = _authenticate_intent(intent_path, census)
    source_present = retirement.path_exists(source)
    target_present = retirement.path_exists(target)
    if source_present and not target_present:
        inspect_tree(source, census)
        if os.stat(source.parent).st_dev != os.stat(custody).st_dev:
            raise Refusal("failed-cache custody move crosses filesystems")
        retirement.rename_exclusive(source, target)
        if inject_at == "after_rename":
            raise RuntimeError("injected after failed-cache rename")
    elif not source_present and target_present:
        inspect_tree(target, census)
    else:
        raise Refusal("failed-cache custody has duplicate or missing tree")
    _fsync_tree(target)
    retirement.fsync_directory(source.parent)
    retirement.fsync_directory(custody)
    inspect_tree(target, census)
    if retirement.path_exists(source):
        raise Refusal("failed-cache source remained after custody move")
    if inject_at == "after_fsync":
        raise RuntimeError("injected after failed-cache fsync")
    receipt_record = _receipt(census, intent_sha)
    receipt_sha = retirement.publish_once(receipt_path, receipt_record)
    retirement.fsync_directory(custody)
    _require_exact_children(custody, {CUSTODY_TREE_NAME, INTENT_NAME, RECEIPT_NAME})
    inspect_tree(target, census)
    return {
        "classification": "PASS_EXACT_OWNER_ONCE_FAILED_CACHE_CUSTODY",
        "receipt_sha256": receipt_sha,
    }


def _replace_flag(command: list[str], flag: str, absolute: str) -> None:
    if command.count(flag) != 1:
        raise Refusal(f"publisher action flag census mismatch: {flag}")
    index = command.index(flag) + 1
    if index >= len(command):
        raise Refusal(f"publisher action flag lacks value: {flag}")
    if PurePosixPath(command[index]).is_absolute():
        raise Refusal(f"publisher predecessor data path unexpectedly absolute: {flag}")
    command[index] = absolute


def absolute_existing_publisher_actions(
    cache_hashes: Mapping[int, str] | None = None,
) -> tuple[PublisherAction, ...]:
    """Return the V001 registry with exactly 17 data-path values absolutized."""
    original = ORIGINAL_EXISTING_PUBLISHER_ACTIONS(cache_hashes)
    revised: list[PublisherAction] = []
    changes = 0
    for action in original:
        command = list(action.command)
        if len(command) < 3 or PurePosixPath(command[2]).is_absolute():
            raise Refusal("authenticated publisher script entry path changed")
        if action.artifact_id == "A05_FIVE_CACHE_SET":
            length = int(command[command.index("--length") + 1])
            _replace_flag(
                command, "--output",
                str(ROOT / SOURCE_RELATIVE / f"L{length}"),
            )
            changes += 1
        elif action.artifact_id in {"A10_CONTROL_HISTORIES", "A14_L10_HISTORY"}:
            length = int(command[command.index("--length") + 1])
            replacements = {
                "--cache-root": str(ROOT / SOURCE_RELATIVE / f"L{length}"),
                "--output": str(
                    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
                    / "PHYSICAL_OUTPUTS" / f"HISTORY_L{length}.json"
                ),
                "--workspace": str(
                    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
                    / "WORKSPACES" / f"L{length}"
                ),
            }
            for flag, value in replacements.items():
                _replace_flag(command, flag, value)
                changes += 1
        revised.append(PublisherAction(action.artifact_id, action.instance, tuple(command)))
    if changes != 17 or len(revised) != len(original):
        raise Refusal("absolute publisher action change census mismatch")
    return tuple(revised)


def authenticate_original_retirement(expected_sha256: str) -> None:
    if expected_sha256 != ORIGINAL_RETIREMENT_RECEIPT_SHA256:
        raise Refusal("completed retirement receipt authorization mismatch")
    old_census = retirement.load_census()
    _custody, _receipt_record, observed = v001._load_completed_retirement_receipt(
        ROOT, old_census,
    )
    if observed != expected_sha256:
        raise Refusal("completed retirement receipt authentication mismatch")


def coordinate_canonical_a01_a18_replay(
    expected_retirement_receipt_sha256: str,
    expected_failed_cache_receipt_sha256: str,
) -> dict[tuple[str, int], str]:
    """Custody the exact obstruction, then resume V002 with bounded actions."""
    if expected_failed_cache_receipt_sha256 != FAILED_CACHE_RECEIPT_SHA256:
        raise Refusal("failed-cache custody receipt authorization mismatch")
    authenticate_original_retirement(expected_retirement_receipt_sha256)
    census = load_census()
    custody_result = retire_failed_cache(ROOT, census)
    if custody_result.get("receipt_sha256") != expected_failed_cache_receipt_sha256:
        raise Refusal("completed failed-cache custody receipt digest mismatch")
    previous = v001.existing_publisher_actions
    if previous is not ORIGINAL_EXISTING_PUBLISHER_ACTIONS:
        raise Refusal("V001 publisher action registry was already replaced")
    v001.existing_publisher_actions = absolute_existing_publisher_actions
    try:
        return v002.coordinate_canonical_a01_a18_replay(
            expected_retirement_receipt_sha256,
        )
    finally:
        v001.existing_publisher_actions = previous


def replay_plan() -> dict[str, object]:
    census = load_census()
    actions = absolute_existing_publisher_actions()
    return {
        "classification": "BOUNDED_NONEXECUTED_V003_RESTART_PLAN",
        "failed_cache_status": transaction_status(ROOT, census),
        "failed_cache_census_sha256": CENSUS_SHA256,
        "failed_cache_inventory_sha256": census["inventory_sha256"],
        "failed_cache_receipt_sha256": FAILED_CACHE_RECEIPT_SHA256,
        "failed_cache_file_count": census["file_count"],
        "failed_cache_total_bytes": census["total_bytes"],
        "manifest_path_mismatch_count": census["manifest_mismatch_count"],
        "custody_root": census["custody_root"],
        "publisher_action_count": len(actions),
        "absolute_data_path_change_count": 17,
        "script_entry_paths_remain_relative": all(
            not PurePosixPath(action.command[2]).is_absolute() for action in actions
        ),
        "canonical_action_executed": False,
        "claim_boundary": (
            "FAILED_CACHE_PATH_AND_RESTART_CONTROL_REPAIR_ONLY__NO_PAYLOAD_"
            "PHYSICS_HISTORY_A18_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true")
    action.add_argument("--execute-canonical", action="store_true")
    parser.add_argument("--retirement-receipt-sha256")
    parser.add_argument("--failed-cache-receipt-sha256")
    parser.add_argument("--authorization")
    parser.add_argument("--v003-authorization")
    arguments = parser.parse_args()
    try:
        if arguments.plan:
            if any((arguments.retirement_receipt_sha256,
                    arguments.failed_cache_receipt_sha256, arguments.authorization,
                    arguments.v003_authorization)):
                raise Refusal("plan mode rejects execution authorization fields")
            result = replay_plan()
        else:
            if arguments.authorization != ORIGINAL_AUTHORIZATION:
                raise Refusal("original exact replay authorization string is absent")
            if arguments.v003_authorization != V003_AUTHORIZATION:
                raise Refusal("V003 custody/restart authorization string is absent")
            if arguments.retirement_receipt_sha256 is None:
                raise Refusal("retirement receipt hash is absent")
            if arguments.failed_cache_receipt_sha256 is None:
                raise Refusal("failed-cache custody receipt hash is absent")
            products = coordinate_canonical_a01_a18_replay(
                arguments.retirement_receipt_sha256,
                arguments.failed_cache_receipt_sha256,
            )
            result = {
                "classification": "PASS_EXACT_V003_A01_A18_CANONICAL_REPLAY",
                "products": {
                    f"{artifact_id}/{instance}": digest
                    for (artifact_id, instance), digest in sorted(products.items())
                },
                "claim_boundary": (
                    "FINITE_CONTROL_L10_RECERTIFICATION_ONLY__NO_L12_SPECTRUM_"
                    "CONTINUUM_OR_GRAVITY_RESULT"
                ),
            }
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError, Refusal) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
