#!/usr/bin/env python3
"""Owner-once obstruction custody for the pre-repair V012/V004R4 stack."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import time
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
TARGET_ROOT: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE_ROOT: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
VALIDATOR: Final[Path] = TARGET_ROOT / "production_obligation_validators.py"
OLD_VALIDATOR_SHA256: Final[str] = (
    "c1ba0881fa15348705161410a6d10d69f686ffef19cd0a5a7d0192c34db58314"
)
OBSTRUCTION: Final[Path] = (
    HOSTILE_ROOT / "A18_DUAL_SINK_ROLE_CONTRACT_OBSTRUCTION_V001.json"
)
OBSTRUCTION_SHA256: Final[str] = (
    "52882072cea1413ae2f403770d554f0e3b1654c0f352a026d744d80cd92e4f40"
)
VALIDATOR_BACKUP: Final[Path] = (
    HERE / "production_obligation_validators.V012_PRE_A18_REPAIR.py"
)
MANIFEST: Final[Path] = HERE / "EXISTING_STACK_OBSTRUCTION_CUSTODY_V001.json"
ROOTS: Final[tuple[tuple[str, Path], ...]] = (
    ("target_v012", TARGET_ROOT),
    ("hostile_v004r4", HOSTILE_ROOT),
)


class Refusal(RuntimeError):
    """The preservation or verification boundary refused closed."""


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("noncanonical custody value") from error


def publication_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("noncanonical custody publication") from error


def descriptor_sha256(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while True:
        block = os.pread(descriptor, 16 * 2**20, offset)
        if not block:
            return digest.hexdigest()
        digest.update(block)
        offset += len(block)


def identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_mode,
        metadata.st_nlink,
    )


def stable_file_row(path: Path) -> dict[str, object]:
    if path.resolve(strict=False) != path or not path.is_relative_to(ROOT):
        raise Refusal(f"noncanonical custody path: {path}")
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Refusal(f"custody file open failed: {path}") from error
    try:
        held_before = os.fstat(descriptor)
        named_before = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(held_before.st_mode)
            or stat.S_ISLNK(named_before.st_mode)
            or held_before.st_nlink != 1
            or identity(held_before) != identity(named_before)
        ):
            raise Refusal(f"custody file is not an owner-once ordinary file: {path}")
        digest = descriptor_sha256(descriptor)
        held_after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
        if (
            identity(held_before) != identity(held_after)
            or identity(held_before) != identity(named_after)
            or descriptor_sha256(descriptor) != digest
        ):
            raise Refusal(f"custody file drifted while held: {path}")
        return {
            "path": str(path.relative_to(ROOT)),
            "bytes": held_before.st_size,
            "mode": stat.S_IMODE(held_before.st_mode),
            "nlink": held_before.st_nlink,
            "sha256": digest,
        }
    finally:
        os.close(descriptor)


def inventory_root(label: str, root: Path) -> dict[str, object]:
    if root.resolve() != root or not root.is_dir() or root.is_symlink():
        raise Refusal(f"{label} root is absent or aliased")
    directories: list[dict[str, object]] = []
    files: list[dict[str, object]] = []
    for current_text, names, filenames in os.walk(root, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        metadata = os.stat(current, follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise Refusal(f"{label} directory is aliased: {current}")
        directories.append({
            "path": str(current.relative_to(ROOT)),
            "mode": stat.S_IMODE(metadata.st_mode),
        })
        for name in names:
            child = current / name
            child_metadata = os.stat(child, follow_symlinks=False)
            if (
                not stat.S_ISDIR(child_metadata.st_mode)
                or stat.S_ISLNK(child_metadata.st_mode)
            ):
                raise Refusal(f"{label} contains non-directory child: {child}")
        for name in filenames:
            files.append(stable_file_row(current / name))
    directories.sort(key=lambda row: str(row["path"]))
    files.sort(key=lambda row: str(row["path"]))
    material = {"directories": directories, "files": files}
    return {
        "label": label,
        "root": str(root.relative_to(ROOT)),
        "directory_count": len(directories),
        "file_count": len(files),
        "writable_file_count": sum(
            1 for row in files if int(row["mode"]) & 0o222
        ),
        "total_bytes": sum(int(row["bytes"]) for row in files),
        "inventory_sha256": hashlib.sha256(
            canonical_json_bytes(material)
        ).hexdigest(),
        **material,
    }


def atomic_publish_once(path: Path, raw: bytes) -> str:
    if path.parent != HERE or not path.is_absolute():
        raise Refusal("custody output escaped its versioned namespace")
    if path.exists() or path.is_symlink():
        raise Refusal(f"owner-once custody output already exists: {path.name}")
    staging = HERE / f".{path.name}.staging-{os.getpid()}-{os.urandom(8).hex()}"
    descriptor = -1
    digest = hashlib.sha256(raw).hexdigest()
    linked = False
    try:
        descriptor = os.open(
            staging,
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400,
        )
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise Refusal("custody staging write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        staged = os.fstat(descriptor)
        if (
            not stat.S_ISREG(staged.st_mode) or staged.st_mode & 0o222
            or staged.st_nlink != 1 or staged.st_size != len(raw)
            or descriptor_sha256(descriptor) != digest
        ):
            raise Refusal("custody staging authentication mismatch")
        try:
            os.link(staging, path, follow_symlinks=False)
            linked = True
        except FileExistsError as error:
            raise Refusal("custody output appeared before commit") from error
        committed = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(committed.st_mode) or committed.st_mode & 0o222
            or committed.st_nlink != 2
            or (committed.st_dev, committed.st_ino) != (staged.st_dev, staged.st_ino)
        ):
            raise Refusal("custody commit hard-link mismatch")
        os.unlink(staging)
        final = stable_file_row(path)
        if final["sha256"] != digest or final["bytes"] != len(raw):
            raise Refusal("custody output final authentication mismatch")
        return digest
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if staging.exists() and not staging.is_symlink():
            os.unlink(staging)
        if linked and not path.exists():
            raise Refusal("custody output disappeared after commit")


def read_stable_bytes(path: Path, expected_sha256: str | None = None) -> bytes:
    if path.resolve(strict=False) != path or not path.is_relative_to(ROOT):
        raise Refusal(f"noncanonical preserved input path: {path}")
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Refusal(f"preserved input open failed: {path}") from error
    try:
        held_before = os.fstat(descriptor)
        named_before = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(held_before.st_mode)
            or held_before.st_mode & 0o222 or held_before.st_nlink != 1
            or identity(held_before) != identity(named_before)
        ):
            raise Refusal(f"preserved input is not immutable owner-once: {path}")
        chunks: list[bytes] = []
        offset = 0
        while offset < held_before.st_size:
            block = os.pread(descriptor, min(16 * 2**20, held_before.st_size - offset), offset)
            if not block:
                raise Refusal(f"preserved input read made no progress: {path}")
            chunks.append(block)
            offset += len(block)
        raw = b"".join(chunks)
        digest = hashlib.sha256(raw).hexdigest()
        held_after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
        if (
            identity(held_before) != identity(held_after)
            or identity(held_before) != identity(named_after)
            or descriptor_sha256(descriptor) != digest
            or (expected_sha256 is not None and digest != expected_sha256)
        ):
            raise Refusal(f"preserved input bytes/hash drift: {path}")
        return raw
    finally:
        os.close(descriptor)


def build_manifest() -> dict[str, object]:
    roots = [inventory_root(label, path) for label, path in ROOTS]
    by_path = {
        row["path"]: row
        for item in roots for row in item["files"]
    }
    validator_relative = str(VALIDATOR.relative_to(ROOT))
    obstruction_relative = str(OBSTRUCTION.relative_to(ROOT))
    if (
        by_path.get(validator_relative, {}).get("sha256")
        != OLD_VALIDATOR_SHA256
        or by_path.get(obstruction_relative, {}).get("sha256")
        != OBSTRUCTION_SHA256
    ):
        raise Refusal("required pre-repair validator/obstruction is not present")
    return {
        "schema": "V012_V004R4_A18_EXISTING_STACK_OBSTRUCTION_CUSTODY_V001",
        "classification": "PRESERVED_COMPLETE_PRE_A18_REPAIR_STACK",
        "observation_epoch": int(time.time()),
        "roots": roots,
        "pre_repair_validator": {
            "source_path": validator_relative,
            "source_sha256": OLD_VALIDATOR_SHA256,
            "byte_backup_path": str(VALIDATOR_BACKUP.relative_to(ROOT)),
            "byte_backup_sha256": OLD_VALIDATOR_SHA256,
        },
        "a18_obstruction": {
            "path": obstruction_relative,
            "sha256": OBSTRUCTION_SHA256,
        },
        "file_count": sum(int(item["file_count"]) for item in roots),
        "total_bytes": sum(int(item["total_bytes"]) for item in roots),
        "claim_boundary": (
            "BYTE_AND_STRUCTURE_CUSTODY_OF_PRE_REPAIR_V012_V004R4_STACK_ONLY__"
            "NO_A18_PROMOTION_L12_LAUNCH_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def preserve() -> None:
    if MANIFEST.exists() or MANIFEST.is_symlink():
        raise Refusal("pre-repair obstruction custody manifest already exists")
    validator_raw = read_stable_bytes(VALIDATOR, OLD_VALIDATOR_SHA256)
    if VALIDATOR_BACKUP.exists() and not VALIDATOR_BACKUP.is_symlink():
        if read_stable_bytes(VALIDATOR_BACKUP, OLD_VALIDATOR_SHA256) != validator_raw:
            raise Refusal("existing pre-repair validator backup differs")
    else:
        atomic_publish_once(VALIDATOR_BACKUP, validator_raw)
    manifest = build_manifest()
    atomic_publish_once(MANIFEST, publication_json_bytes(manifest))
    verify(None)


def strict_manifest() -> dict[str, object]:
    raw = read_stable_bytes(MANIFEST)
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal("custody manifest malformed") from error
    if type(value) is not dict:
        raise Refusal("custody manifest is not an object")
    return value


def verify(allowed_validator_sha256: str | None) -> None:
    manifest = strict_manifest()
    observed_roots = [inventory_root(label, path) for label, path in ROOTS]
    expected_roots = manifest.get("roots")
    if allowed_validator_sha256 is None:
        if observed_roots != expected_roots:
            raise Refusal("pre-repair stack drifted from complete custody")
    else:
        if (
            len(allowed_validator_sha256) != 64
            or any(character not in "0123456789abcdef" for character in allowed_validator_sha256)
        ):
            raise Refusal("allowed successor validator hash malformed")
        expected = {
            row["path"]: row for item in expected_roots for row in item["files"]
        }
        observed = {
            row["path"]: row for item in observed_roots for row in item["files"]
        }
        validator_relative = str(VALIDATOR.relative_to(ROOT))
        if set(expected) != set(observed):
            raise Refusal("post-repair stack path census drift")
        differences = [
            path for path in sorted(expected) if expected[path] != observed[path]
        ]
        if differences != [validator_relative]:
            raise Refusal("post-repair hash blast exceeds the A18 validator")
        if (
            observed[validator_relative]["sha256"] != allowed_validator_sha256
            or observed[validator_relative]["mode"] != 0o444
            or observed[validator_relative]["nlink"] != 1
        ):
            raise Refusal("successor A18 validator custody mismatch")
        for expected_root, observed_root in zip(expected_roots, observed_roots):
            for key in (
                "label", "root", "directory_count", "file_count",
                "writable_file_count",
            ):
                if expected_root[key] != observed_root[key]:
                    raise Refusal("post-repair root census drift")
            if expected_root["directories"] != observed_root["directories"]:
                raise Refusal("post-repair directory census drift")
    backup = stable_file_row(VALIDATOR_BACKUP)
    if backup["sha256"] != OLD_VALIDATOR_SHA256:
        raise Refusal("pre-repair validator byte backup drift")
    print(
        "PASS_EXISTING_STACK_OBSTRUCTION_CUSTODY "
        f"files={manifest['file_count']} bytes={manifest['total_bytes']}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preserve", "verify"))
    parser.add_argument("--allowed-validator-sha256")
    args = parser.parse_args()
    try:
        if args.mode == "preserve":
            if args.allowed_validator_sha256 is not None:
                raise Refusal("preserve does not accept a successor hash")
            preserve()
        else:
            verify(args.allowed_validator_sha256)
    except (OSError, Refusal) as error:
        print(f"REFUSED: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
