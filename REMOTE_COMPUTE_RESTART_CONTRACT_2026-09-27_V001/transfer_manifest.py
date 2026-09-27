#!/usr/bin/env python3
"""Build or verify an exact, hash-pinned one-way transfer census.

This tool moves no bytes and starts no calculation.  The expected manifest
digest must be conveyed independently of the transferred manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any


SCHEMA = "UNT_REMOTE_TRANSFER_MANIFEST_V001"
HEX_256 = re.compile(r"[0-9a-f]{64}\Z")


class TransferError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TransferError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise TransferError(f"non-finite JSON constant: {value}")


def parse_canonical_json(raw: bytes) -> Any:
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=strict_object,
                           parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise TransferError(f"invalid manifest JSON: {error}") from error
    require(raw == canonical_bytes(value), "manifest is not canonical JSON")
    return value


def relative_name(value: str) -> str:
    require(isinstance(value, str), "file path must be a string")
    require(value and not value.startswith("/"), "absolute or empty file path")
    require("\\" not in value and all(32 <= ord(char) != 127 for char in value),
            "invalid file path character")
    parts = value.split("/")
    require(all(part not in ("", ".", "..") for part in parts), "noncanonical or traversing file path")
    require(".git" not in parts, "local Git metadata may not be transferred")
    return value


def checked_root(root: Path) -> Path:
    require(root.is_dir(), f"missing bundle directory: {root}")
    require(not root.is_symlink(), f"symlink bundle root: {root}")
    return root.resolve(strict=True)


def checked_file(root: Path, name: str) -> Path:
    path = root
    for part in relative_name(name).split("/"):
        path = path / part
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError as error:
            raise TransferError(f"missing file: {name}") from error
        require(not stat.S_ISLNK(mode), f"symlink in file route: {name}")
    require(stat.S_ISREG(path.lstat().st_mode), f"not a regular file: {name}")
    return path


def hash_stable_file(path: Path) -> tuple[int, str]:
    before = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            f"file changed while hashing: {path}")
    return after.st_size, digest.hexdigest()


def read_allowlist(path: Path) -> tuple[bytes, list[str]]:
    require(path.is_file() and not path.is_symlink(), "missing or symlink allowlist")
    raw = path.read_bytes()
    require(raw.endswith(b"\n"), "allowlist must end with newline")
    try:
        names = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise TransferError("allowlist must be UTF-8") from error
    require(names and all(names), "allowlist contains an empty line")
    for name in names:
        relative_name(name)
    require(names == sorted(set(names)), "allowlist must be sorted with no duplicates")
    require(raw == ("\n".join(names) + "\n").encode("utf-8"),
            "allowlist must use canonical LF line endings")
    return raw, names


def build_manifest(root: Path, allowlist: Path, output: Path) -> str:
    root = checked_root(root)
    raw_allowlist, names = read_allowlist(allowlist)
    output_parent = output.parent.resolve(strict=True)
    require(output_parent != root and root not in output_parent.parents,
            "manifest output must be outside bundle root")
    records: list[dict[str, Any]] = []
    total = 0
    for name in names:
        size, digest = hash_stable_file(checked_file(root, name))
        records.append({"path": name, "bytes": size, "sha256": digest})
        total += size
    manifest = {
        "schema": SCHEMA,
        "algorithm": "sha256",
        "allowlist_sha256": sha256_bytes(raw_allowlist),
        "files": records,
        "total_bytes": total,
    }
    raw = canonical_bytes(manifest)
    try:
        with output.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError as error:
        raise TransferError(f"owner-once manifest already exists: {output}") from error
    descriptor = os.open(str(output_parent), os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return sha256_bytes(raw)


def file_census(root: Path) -> set[str]:
    observed: set[str] = set()
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base = Path(current)
        for name in dirs:
            path = base / name
            require(not path.is_symlink(), f"symlink directory: {path.relative_to(root)}")
        for name in files:
            path = base / name
            require(not path.is_symlink(), f"symlink file: {path.relative_to(root)}")
            require(stat.S_ISREG(path.lstat().st_mode), f"nonregular file: {path.relative_to(root)}")
            observed.add(path.relative_to(root).as_posix())
    return observed


def verify_manifest(root: Path, manifest_path: Path, expected_sha256: str,
                    allow_extras: bool = False) -> dict[str, Any]:
    root = checked_root(root)
    require(bool(HEX_256.fullmatch(expected_sha256)), "expected manifest SHA-256 must be lowercase hex")
    require(manifest_path.is_file() and not manifest_path.is_symlink(), "missing or symlink manifest")
    raw = manifest_path.read_bytes()
    require(sha256_bytes(raw) == expected_sha256, "manifest SHA-256 mismatch")
    manifest = parse_canonical_json(raw)
    require(isinstance(manifest, dict) and set(manifest) ==
            {"schema", "algorithm", "allowlist_sha256", "files", "total_bytes"},
            "manifest field census")
    require(manifest["schema"] == SCHEMA and manifest["algorithm"] == "sha256",
            "manifest schema or algorithm")
    require(isinstance(manifest["allowlist_sha256"], str) and
            bool(HEX_256.fullmatch(manifest["allowlist_sha256"])), "allowlist digest")
    records = manifest["files"]
    require(isinstance(records, list) and bool(records), "empty or invalid file records")
    names: list[str] = []
    total = 0
    for record in records:
        require(isinstance(record, dict) and set(record) == {"path", "bytes", "sha256"},
                "file record census")
        name = relative_name(record["path"])
        require(type(record["bytes"]) is int and record["bytes"] >= 0, "file byte count")
        require(isinstance(record["sha256"], str) and
                bool(HEX_256.fullmatch(record["sha256"])), "file digest")
        size, digest = hash_stable_file(checked_file(root, name))
        require(size == record["bytes"] and digest == record["sha256"],
                f"file byte count or SHA-256 mismatch: {name}")
        names.append(name)
        total += size
    require(names == sorted(set(names)), "file records must be sorted and unique")
    require(type(manifest["total_bytes"]) is int and manifest["total_bytes"] == total,
            "manifest total byte count")
    expected_allowlist = ("\n".join(names) + "\n").encode("utf-8")
    require(sha256_bytes(expected_allowlist) == manifest["allowlist_sha256"],
            "allowlist digest does not match file census")
    if not allow_extras:
        require(file_census(root) == set(names), "bundle has missing or extra files")
    return {"status": "PASS_TRANSFER_VERIFICATION", "manifest_sha256": expected_sha256,
            "file_count": len(names), "total_bytes": total, "allow_extras": allow_extras}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    build = sub.add_parser("build")
    build.add_argument("--root", type=Path, required=True)
    build.add_argument("--allowlist", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--root", type=Path, required=True)
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--expected-sha256", required=True)
    verify.add_argument("--allow-extras", action="store_true")
    args = parser.parse_args()
    try:
        if args.action == "build":
            print(json.dumps({"status": "MANIFEST_CREATED_NO_TRANSFER", "sha256":
                              build_manifest(args.root, args.allowlist, args.output)}, sort_keys=True))
        else:
            print(json.dumps(verify_manifest(args.root, args.manifest, args.expected_sha256,
                                             args.allow_extras), sort_keys=True))
    except (TransferError, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
