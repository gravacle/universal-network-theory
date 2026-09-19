#!/usr/bin/env python3
"""Restart-safe owner-once retirement for the exact pre-repair A01-A17 stack.

The canonical transaction is never run by this module's tests.  Tests exercise
the same machinery against synthetic temporary roots.  ``--execute`` is a
separate, explicit future action and is not authorized by this source alone.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import os
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
CENSUS: Final[Path] = HERE / "RETIREMENT_CENSUS_V001.json"
CENSUS_SHA256: Final[str] = (
    "dc63434d16e8fa8722123f79aeef964b49fac864c2ec11984539ff6bdf641357"
)
INTENT_NAME: Final[str] = "RETIREMENT_INTENT_V001.json"
EVENT_DIRECTORY_NAME: Final[str] = "RETIREMENT_EVENTS_V001"
RECEIPT_NAME: Final[str] = "RETIREMENT_RECEIPT_V001.json"
AT_FDCWD: Final[int] = -2
RENAME_EXCL: Final[int] = 0x00000004


class Refusal(RuntimeError):
    """The retirement boundary refused without authorizing replay."""


class InjectedInterruption(RuntimeError):
    """Test-only interruption used to prove in-process rollback."""


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("noncanonical retirement value") from error


def publication_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("noncanonical retirement publication") from error


def strict_json(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise Refusal(f"{label} duplicate JSON key")
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise Refusal(f"{label} nonfinite JSON constant")

    try:
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except Refusal:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Refusal(f"{label} malformed JSON") from error
    if type(value) is not dict:
        raise Refusal(f"{label} exact object required")
    return value


def path_exists(path: Path) -> bool:
    return os.path.lexists(path)


def canonical_relative(value: object, label: str) -> str:
    if type(value) is not str or not value:
        raise Refusal(f"{label} exact relative path required")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute() or ".." in pure.parts or "." in pure.parts
        or str(pure) != value
    ):
        raise Refusal(f"{label} noncanonical relative path")
    return value


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def descriptor_sha256(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while True:
        block = os.pread(descriptor, 16 * 2**20, offset)
        if not block:
            return digest.hexdigest()
        digest.update(block)
        offset += len(block)


def descriptor_identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_mode,
        metadata.st_nlink,
    )


def retained_identity_fields(metadata: os.stat_result) -> dict[str, int]:
    return {
        "device": metadata.st_dev,
        "inode": metadata.st_ino,
        "bytes": metadata.st_size,
        "mode": stat.S_IMODE(metadata.st_mode),
        "nlink": metadata.st_nlink,
    }


def retained_file_identity(path: Path, logical_path: str) -> dict[str, object]:
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Refusal(
            f"retirement identity file open failed: {logical_path}"
        ) from error
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_nlink != 1
            or descriptor_identity(before) != descriptor_identity(named)
        ):
            raise Refusal(
                f"retirement identity file is not owner-once: {logical_path}"
            )
        digest = descriptor_sha256(descriptor)
        after = os.fstat(descriptor)
        if (
            descriptor_identity(before) != descriptor_identity(after)
            or descriptor_sha256(descriptor) != digest
        ):
            raise Refusal(
                f"retirement identity file drifted while held: {logical_path}"
            )
        return {
            "path": logical_path,
            **retained_identity_fields(before),
            "sha256": digest,
        }
    finally:
        os.close(descriptor)


def retained_entry_identity(
    path: Path, entry: dict[str, object],
) -> dict[str, object]:
    logical_path = str(entry["path"])
    if entry["kind"] == "file":
        return {
            "kind": "file",
            **retained_file_identity(path, logical_path),
        }
    if path.is_symlink() or not path.is_dir():
        raise Refusal(
            f"retirement identity directory is absent or aliased: {logical_path}"
        )
    directories: list[dict[str, object]] = []
    files: list[dict[str, object]] = []
    for current_text, names, filenames in os.walk(path, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        relative = current.relative_to(path)
        current_logical = (
            logical_path if relative == Path(".")
            else f"{logical_path}/{relative.as_posix()}"
        )
        metadata = os.stat(current, follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise Refusal(
                f"retirement identity directory alias: {current_logical}"
            )
        directories.append({
            "path": current_logical,
            **retained_identity_fields(metadata),
        })
        for name in names:
            child = current / name
            child_metadata = os.stat(child, follow_symlinks=False)
            if (
                not stat.S_ISDIR(child_metadata.st_mode)
                or stat.S_ISLNK(child_metadata.st_mode)
            ):
                raise Refusal(
                    f"retirement identity tree contains alias: {child}"
                )
        for name in filenames:
            child = current / name
            files.append(retained_file_identity(
                child, f"{current_logical}/{name}",
            ))
    directories.sort(key=lambda row: str(row["path"]))
    files.sort(key=lambda row: str(row["path"]))
    material = {"directories": directories, "files": files}
    return {
        "kind": "directory",
        "path": logical_path,
        "directories": directories,
        "files": files,
        "inventory_sha256": sha256_bytes(canonical_json_bytes(material)),
    }


def file_row(path: Path, logical_path: str) -> dict[str, object]:
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Refusal(f"retirement file open failed: {logical_path}") from error
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        before_identity = (
            before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
            before.st_ctime_ns, before.st_mode, before.st_nlink,
        )
        named_identity = (
            named.st_dev, named.st_ino, named.st_size, named.st_mtime_ns,
            named.st_ctime_ns, named.st_mode, named.st_nlink,
        )
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_nlink != 1 or before_identity != named_identity
        ):
            raise Refusal(f"retirement file is not owner-once: {logical_path}")
        digest = descriptor_sha256(descriptor)
        after = os.fstat(descriptor)
        if (
            before_identity != (
                after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                after.st_ctime_ns, after.st_mode, after.st_nlink,
            )
            or descriptor_sha256(descriptor) != digest
        ):
            raise Refusal(f"retirement file drifted while held: {logical_path}")
        return {
            "path": logical_path,
            "bytes": before.st_size,
            "mode": stat.S_IMODE(before.st_mode),
            "nlink": before.st_nlink,
            "sha256": digest,
        }
    finally:
        os.close(descriptor)


def directory_row(path: Path, logical_path: str) -> dict[str, object]:
    if path.is_symlink() or not path.is_dir():
        raise Refusal(f"retirement directory is absent or aliased: {logical_path}")
    directories: list[dict[str, object]] = []
    files: list[dict[str, object]] = []
    for current_text, names, filenames in os.walk(path, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        relative = current.relative_to(path)
        current_logical = (
            logical_path if relative == Path(".")
            else f"{logical_path}/{relative.as_posix()}"
        )
        metadata = os.stat(current, follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise Refusal(f"retirement directory alias: {current_logical}")
        directories.append({
            "path": current_logical,
            "mode": stat.S_IMODE(metadata.st_mode),
        })
        for name in names:
            child = current / name
            child_metadata = os.stat(child, follow_symlinks=False)
            if (
                not stat.S_ISDIR(child_metadata.st_mode)
                or stat.S_ISLNK(child_metadata.st_mode)
            ):
                raise Refusal(f"retirement tree contains alias: {child}")
        for name in filenames:
            child = current / name
            logical = f"{current_logical}/{name}"
            files.append(file_row(child, logical))
    directories.sort(key=lambda row: str(row["path"]))
    files.sort(key=lambda row: str(row["path"]))
    material = {"directories": directories, "files": files}
    return {
        "path": logical_path,
        "kind": "directory",
        "directory_count": len(directories),
        "file_count": len(files),
        "total_bytes": sum(int(row["bytes"]) for row in files),
        "inventory_sha256": sha256_bytes(canonical_json_bytes(material)),
    }


def inspect_entry(physical: Path, entry: dict[str, object]) -> dict[str, object]:
    logical = str(entry["path"])
    if entry["kind"] == "file":
        row = {"kind": "file", **file_row(physical, logical)}
    else:
        row = directory_row(physical, logical)
    if row != entry:
        raise Refusal(f"retirement census mismatch: {logical}")
    return row


def load_census(path: Path = CENSUS) -> dict[str, object]:
    metadata = os.stat(path, follow_symlinks=False)
    if (
        path == CENSUS
        and (
            not stat.S_ISREG(metadata.st_mode) or path.is_symlink()
            or metadata.st_mode & 0o222 or metadata.st_nlink != 1
        )
    ):
        raise Refusal("frozen retirement census custody mismatch")
    raw = path.read_bytes()
    if path == CENSUS and sha256_bytes(raw) != CENSUS_SHA256:
        raise Refusal("frozen retirement census hash mismatch")
    census = strict_json(raw, "retirement census")
    return validate_census(census)


def validate_census(census: dict[str, object]) -> dict[str, object]:
    expected_keys = {
        "schema", "classification", "custody_root", "entries",
        "required_absent_paths", "entry_count", "source_file_count",
        "source_total_bytes", "executed", "claim_boundary",
    }
    if (
        set(census) != expected_keys
        or census.get("schema")
        != "V012_A01_A17_PRE_A18_RETIREMENT_CENSUS_V001"
        or census.get("classification")
        != "EXACT_NONEXECUTED_OWNER_ONCE_RETIREMENT_CENSUS"
        or census.get("executed") is not False
    ):
        raise Refusal("retirement census identity or keyset mismatch")
    custody = canonical_relative(census.get("custody_root"), "custody root")
    entries = census.get("entries")
    absent = census.get("required_absent_paths")
    if type(entries) is not list or not entries or type(absent) is not list:
        raise Refusal("retirement entry/absence census mismatch")
    paths: list[str] = []
    file_count = 0
    total_bytes = 0
    for index, value in enumerate(entries):
        if type(value) is not dict:
            raise Refusal(f"retirement entry {index} is not an object")
        kind = value.get("kind")
        expected = (
            {"path", "kind", "bytes", "mode", "nlink", "sha256"}
            if kind == "file" else
            {"path", "kind", "directory_count", "file_count", "total_bytes", "inventory_sha256"}
            if kind == "directory" else set()
        )
        if not expected or set(value) != expected:
            raise Refusal(f"retirement entry {index} keyset mismatch")
        relative = canonical_relative(value.get("path"), f"entry {index}")
        paths.append(relative)
        if kind == "file":
            if (
                type(value.get("bytes")) is not int or value["bytes"] < 0
                or type(value.get("mode")) is not int
                or type(value.get("nlink")) is not int or value["nlink"] != 1
                or type(value.get("sha256")) is not str
                or len(value["sha256"]) != 64
            ):
                raise Refusal(f"retirement file entry {index} value mismatch")
            file_count += 1
            total_bytes += int(value["bytes"])
        else:
            for key in ("directory_count", "file_count", "total_bytes"):
                if type(value.get(key)) is not int or value[key] < 0:
                    raise Refusal(f"retirement directory entry {index} value mismatch")
            if (
                type(value.get("inventory_sha256")) is not str
                or len(value["inventory_sha256"]) != 64
            ):
                raise Refusal(f"retirement directory hash {index} mismatch")
            file_count += int(value["file_count"])
            total_bytes += int(value["total_bytes"])
    if len(paths) != len(set(paths)) or len(absent) != len(set(absent)):
        raise Refusal("retirement path census contains duplicates")
    for index, value in enumerate(absent):
        canonical_relative(value, f"required absent path {index}")
    pure_paths = [PurePosixPath(value) for value in paths]
    for left_index, left in enumerate(pure_paths):
        for right in pure_paths[left_index + 1:]:
            if left in right.parents or right in left.parents:
                raise Refusal("retirement top-level paths overlap")
    custody_path = PurePosixPath(custody)
    if any(
        custody_path == path or custody_path in path.parents
        or path in custody_path.parents
        for path in pure_paths
    ):
        raise Refusal("retirement custody overlaps a source path")
    if (
        census.get("entry_count") != len(entries)
        or census.get("source_file_count") != file_count
        or census.get("source_total_bytes") != total_bytes
    ):
        raise Refusal("retirement reconstructed totals mismatch")
    return census


def fsync_directory(path: Path) -> None:
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def fsync_regular_file(path: Path, logical_path: str) -> None:
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Refusal(f"moved file fsync open failed: {logical_path}") from error
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_nlink != 1
            or descriptor_identity(before) != descriptor_identity(named)
        ):
            raise Refusal(f"moved file fsync identity mismatch: {logical_path}")
        os.fsync(descriptor)
        after = os.fstat(descriptor)
        if descriptor_identity(before) != descriptor_identity(after):
            raise Refusal(f"moved file drifted during fsync: {logical_path}")
    finally:
        os.close(descriptor)


def fsync_moved_entry(path: Path, entry: dict[str, object]) -> None:
    logical_path = str(entry["path"])
    if entry["kind"] == "file":
        fsync_regular_file(path, logical_path)
        return
    if path.is_symlink() or not path.is_dir():
        raise Refusal(
            f"moved directory is absent or aliased during fsync: {logical_path}"
        )
    directories: list[Path] = []
    for current_text, names, filenames in os.walk(path, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        relative = current.relative_to(path)
        current_logical = (
            logical_path if relative == Path(".")
            else f"{logical_path}/{relative.as_posix()}"
        )
        metadata = os.stat(current, follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise Refusal(f"moved directory alias during fsync: {current_logical}")
        directories.append(current)
        for name in names:
            child = current / name
            child_metadata = os.stat(child, follow_symlinks=False)
            if (
                not stat.S_ISDIR(child_metadata.st_mode)
                or stat.S_ISLNK(child_metadata.st_mode)
            ):
                raise Refusal(f"moved tree alias during fsync: {child}")
        for name in filenames:
            fsync_regular_file(
                current / name, f"{current_logical}/{name}",
            )
    for directory in sorted(
        directories, key=lambda item: len(item.parts), reverse=True,
    ):
        fsync_directory(directory)


def rename_exclusive(source: Path, target: Path) -> None:
    if sys.platform != "darwin":
        raise Refusal("atomic no-replace rename requires macOS renameatx_np")
    try:
        function = ctypes.CDLL(None, use_errno=True).renameatx_np
    except AttributeError as error:
        raise Refusal("macOS atomic no-replace rename is unavailable") from error
    function.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    ctypes.set_errno(0)
    result = function(
        AT_FDCWD, os.fsencode(source), AT_FDCWD, os.fsencode(target),
        RENAME_EXCL,
    )
    if result == 0:
        return
    error_number = ctypes.get_errno()
    if error_number in {errno.EEXIST, errno.ENOTEMPTY}:
        raise Refusal(f"retirement destination appeared: {target}")
    raise Refusal(
        f"atomic no-replace rename failed ({error_number}): "
        f"{os.strerror(error_number)}"
    )


def publish_once(path: Path, record: dict[str, object]) -> str:
    if path_exists(path):
        raise Refusal(f"transaction record already exists: {path.name}")
    raw = publication_json_bytes(record)
    digest = sha256_bytes(raw)
    descriptor = os.open(
        path,
        os.O_RDWR | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o400,
    )
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise Refusal("transaction record write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        metadata = os.fstat(descriptor)
        if (
            metadata.st_nlink != 1 or metadata.st_mode & 0o222
            or descriptor_sha256(descriptor) != digest
        ):
            raise Refusal("transaction record authentication mismatch")
    finally:
        os.close(descriptor)
    fsync_directory(path.parent)
    return digest


def ensure_root(root: Path) -> None:
    if not root.is_absolute() or root.resolve() != root or root.is_symlink():
        raise Refusal("retirement repository root is not canonical")


def destination(custody: Path, entry: dict[str, object]) -> Path:
    return custody.joinpath(*PurePosixPath(str(entry["path"])).parts)


def preflight(root: Path, census: dict[str, object]) -> dict[str, object]:
    ensure_root(root)
    custody = root.joinpath(*PurePosixPath(str(census["custody_root"])).parts)
    if path_exists(custody):
        raise Refusal("retirement custody destination is not absent")
    for entry in census["entries"]:
        source = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
        inspect_entry(source, entry)
    for value in census["required_absent_paths"]:
        path = root.joinpath(*PurePosixPath(str(value)).parts)
        if path_exists(path):
            raise Refusal(f"required future path is already present: {value}")
    return {
        "schema": "V012_A01_A17_RETIREMENT_DRY_RUN_V001",
        "classification": "PASS_EXACT_RETIREMENT_DRY_RUN_NO_MUTATION",
        "entry_count": census["entry_count"],
        "source_file_count": census["source_file_count"],
        "source_total_bytes": census["source_total_bytes"],
        "custody_destination_absent": True,
        "canonical_path_moved": False,
        "claim_boundary": "DRY_RUN_ONLY__NO_CANONICAL_PATH_MOVED_DELETED_OR_OVERWRITTEN",
    }


def make_parents_beneath(custody: Path, path: Path) -> None:
    current = custody
    for part in path.relative_to(custody).parent.parts:
        current = current / part
        if path_exists(current):
            metadata = os.stat(current, follow_symlinks=False)
            if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
                raise Refusal("retirement destination parent is aliased")
        else:
            os.mkdir(current, 0o700)
            fsync_directory(current.parent)


def move_entry(root: Path, custody: Path, entry: dict[str, object], ordinal: int) -> None:
    source = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
    target = destination(custody, entry)
    inspect_entry(source, entry)
    retained_source_identity = retained_entry_identity(source, entry)
    if path_exists(target):
        raise Refusal(f"retirement destination appeared: {entry['path']}")
    make_parents_beneath(custody, target)
    source_parent = source.parent
    target_parent = target.parent
    if os.stat(source_parent).st_dev != os.stat(target_parent).st_dev:
        raise Refusal("retirement attempted a cross-filesystem move")
    rename_exclusive(source, target)
    fsync_moved_entry(target, entry)
    fsync_directory(source_parent)
    fsync_directory(target_parent)
    inspect_entry(target, entry)
    retained_target_identity = retained_entry_identity(target, entry)
    if retained_target_identity != retained_source_identity:
        raise Refusal(
            f"retirement identity changed across rename: {entry['path']}"
        )
    event = {
        "schema": "V012_OWNER_ONCE_RETIREMENT_EVENT_V001",
        "ordinal": ordinal,
        "path": entry["path"],
        "entry_sha256": sha256_bytes(canonical_json_bytes(entry)),
        "source_absent": True,
        "destination_authenticated": True,
    }
    publish_once(
        custody / EVENT_DIRECTORY_NAME / f"EVENT_{ordinal:03d}.json", event,
    )


def remove_transaction_tree(custody: Path) -> None:
    event_root = custody / EVENT_DIRECTORY_NAME
    if path_exists(event_root):
        if event_root.is_symlink() or not event_root.is_dir():
            raise Refusal("retirement event directory is aliased")
        for child in sorted(event_root.iterdir()):
            if not child.name.startswith("EVENT_") or child.suffix != ".json":
                raise Refusal("unregistered retirement event file")
            os.unlink(child)
        os.rmdir(event_root)
    intent = custody / INTENT_NAME
    if path_exists(intent):
        os.unlink(intent)
    for current_text, names, filenames in os.walk(custody, topdown=False):
        current = Path(current_text)
        if filenames:
            raise Refusal("unregistered file prevents retirement rollback cleanup")
        for name in names:
            child = current / name
            if path_exists(child):
                os.rmdir(child)
    os.rmdir(custody)
    fsync_directory(custody.parent)


def recover(root: Path, census: dict[str, object]) -> dict[str, object]:
    ensure_root(root)
    custody = root.joinpath(*PurePosixPath(str(census["custody_root"])).parts)
    if not path_exists(custody):
        return {
            "classification": "NO_ACTIVE_RETIREMENT_TRANSACTION",
            "restored_entry_count": 0,
        }
    if custody.is_symlink() or not custody.is_dir():
        raise Refusal("retirement custody root is aliased")
    if path_exists(custody / RECEIPT_NAME):
        raise Refusal("completed retirement cannot be automatically reversed")
    intent_path = custody / INTENT_NAME
    if not path_exists(intent_path):
        for entry in census["entries"]:
            source = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
            target = destination(custody, entry)
            if path_exists(target):
                raise Refusal("intent-free transaction contains moved custody")
            inspect_entry(source, entry)
        remove_transaction_tree(custody)
        preflight(root, census)
        return {
            "classification": "PASS_EMPTY_INTERRUPTED_TRANSACTION_REMOVED",
            "restored_entry_count": 0,
        }
    if not intent_path.is_file() or intent_path.is_symlink():
        raise Refusal("interrupted retirement intent is aliased")
    intent = strict_json(intent_path.read_bytes(), "retirement intent")
    if (
        intent.get("schema") != "V012_OWNER_ONCE_RETIREMENT_INTENT_V001"
        or intent.get("census_sha256") != sha256_bytes(publication_json_bytes(census))
        or intent.get("paths") != [entry["path"] for entry in census["entries"]]
    ):
        raise Refusal("interrupted retirement intent mismatch")
    restored = 0
    for entry in reversed(census["entries"]):
        source = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
        target = destination(custody, entry)
        source_present = path_exists(source)
        target_present = path_exists(target)
        if source_present and target_present:
            raise Refusal(f"retirement recovery found duplicate custody: {entry['path']}")
        if not source_present and not target_present:
            raise Refusal(f"retirement recovery lost custody: {entry['path']}")
        if target_present:
            inspect_entry(target, entry)
            retained_target_identity = retained_entry_identity(target, entry)
            rename_exclusive(target, source)
            fsync_moved_entry(source, entry)
            fsync_directory(target.parent)
            fsync_directory(source.parent)
            inspect_entry(source, entry)
            retained_source_identity = retained_entry_identity(source, entry)
            if retained_source_identity != retained_target_identity:
                raise Refusal(
                    f"retirement identity changed during recovery: "
                    f"{entry['path']}"
                )
            restored += 1
        else:
            inspect_entry(source, entry)
    remove_transaction_tree(custody)
    preflight(root, census)
    return {
        "classification": "PASS_INTERRUPTED_RETIREMENT_ROLLED_BACK",
        "restored_entry_count": restored,
    }


def retire(
    root: Path, census: dict[str, object], *, inject_after: int | None = None,
) -> dict[str, object]:
    preflight(root, census)
    custody = root.joinpath(*PurePosixPath(str(census["custody_root"])).parts)
    if custody.parent.is_symlink() or not custody.parent.is_dir():
        raise Refusal("retirement custody parent is absent or aliased")
    os.mkdir(custody, 0o700)
    fsync_directory(custody.parent)
    try:
        os.mkdir(custody / EVENT_DIRECTORY_NAME, 0o700)
        fsync_directory(custody)
        intent = {
            "schema": "V012_OWNER_ONCE_RETIREMENT_INTENT_V001",
            "census_sha256": sha256_bytes(publication_json_bytes(census)),
            "paths": [entry["path"] for entry in census["entries"]],
            "entry_count": census["entry_count"],
            "source_file_count": census["source_file_count"],
            "source_total_bytes": census["source_total_bytes"],
        }
        publish_once(custody / INTENT_NAME, intent)
        for ordinal, entry in enumerate(census["entries"], start=1):
            move_entry(root, custody, entry, ordinal)
            if inject_after == ordinal:
                raise InjectedInterruption(f"injected after entry {ordinal}")
        for entry in census["entries"]:
            source = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
            if path_exists(source):
                raise Refusal(f"retired source remained present: {entry['path']}")
            inspect_entry(destination(custody, entry), entry)
        receipt = {
            "schema": "V012_A01_A17_OWNER_ONCE_RETIREMENT_RECEIPT_V001",
            "classification": "PASS_EXACT_OWNER_ONCE_RETIREMENT",
            "census_sha256": sha256_bytes(publication_json_bytes(census)),
            "intent_sha256": sha256_bytes((custody / INTENT_NAME).read_bytes()),
            "entry_count": census["entry_count"],
            "source_file_count": census["source_file_count"],
            "source_total_bytes": census["source_total_bytes"],
            "retired_paths": [entry["path"] for entry in census["entries"]],
            "canonical_destinations_absent_for_replay": True,
            "claim_boundary": "RETIREMENT_CUSTODY_ONLY__NO_A01_A18_REPLAY_OR_PROMOTION",
        }
        receipt_sha256 = publish_once(custody / RECEIPT_NAME, receipt)
        fsync_directory(custody)
        return {
            "classification": "PASS_EXACT_OWNER_ONCE_RETIREMENT",
            "receipt_sha256": receipt_sha256,
            "entry_count": census["entry_count"],
        }
    except Exception as error:
        try:
            recovery = recover(root, census)
        except Exception as recovery_error:
            raise Refusal(
                f"retirement failed and automatic rollback also refused: "
                f"{error}; rollback: {recovery_error}"
            ) from recovery_error
        raise Refusal(
            f"retirement failed and rolled back {recovery['restored_entry_count']} entries: {error}"
        ) from error


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--execute", action="store_true")
    action.add_argument("--recover", action="store_true")
    arguments = parser.parse_args()
    try:
        census = load_census()
        if arguments.dry_run:
            result = preflight(ROOT, census)
        elif arguments.recover:
            result = recover(ROOT, census)
        else:
            result = retire(ROOT, census)
    except (OSError, ValueError, json.JSONDecodeError, Refusal) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
