#!/usr/bin/env python3
"""Restore only the hash-authenticated L8 manifest omitted by Git ignore rules."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PACKET = "CUSTODY_RECOVERY_NUMERICS_2026-09-27_V001"
FREEZE = "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/FREEZE.json"
FREEZE_SHA = "9ceac93c5571c021e7fe5c3a197b4d4c7f1cec13fecc07d7ed96589bcf7efece"
MANIFEST = "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012/L8/CACHE_MANIFEST.json"
COPY = PACKET + "/RECOVERED_INPUTS/L8_CACHE_MANIFEST.json"
MANIFEST_SHA = "d33ea5911dacf8c33aebe9f88f85d5ea8db754221fee5f80d4c2d440009e5ade"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def safe_path(root, relative):
    route = Path(relative)
    require(not route.is_absolute() and ".." not in route.parts and str(route) == relative,
            "noncanonical relative path")
    require(root.is_dir() and not root.is_symlink(), "invalid root")
    path = root
    for part in route.parts:
        path = path / part
        require(not path.is_symlink(), "symlink refused: " + relative)
    return path

def authenticated_bytes(path, digest):
    require(path.is_file() and not path.is_symlink(), "missing or unsafe file: " + str(path))
    before = path.stat()
    data = path.read_bytes()
    after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), "file changed while read")
    require(hashlib.sha256(data).hexdigest() == digest, "hash mismatch: " + str(path))
    return data

def restore(root):
    freeze = json.loads(authenticated_bytes(safe_path(root, FREEZE), FREEZE_SHA))
    require(freeze["inputs"]["cache_manifest"] == {"path": MANIFEST, "sha256": MANIFEST_SHA},
            "frozen manifest binding mismatch")
    data = authenticated_bytes(safe_path(root, COPY), MANIFEST_SHA)
    destination = safe_path(root, MANIFEST)
    if destination.exists():
        authenticated_bytes(destination, MANIFEST_SHA)
        return {"status": "EXISTING_IDENTICAL_PRESERVED", "path": MANIFEST,
                "sha256": MANIFEST_SHA, "bytes": len(data)}
    current = root
    for part in Path(MANIFEST).parts[:-1]:
        current = current / part
        if not current.exists():
            current.mkdir()
        require(current.is_dir() and not current.is_symlink(), "unsafe destination directory")
    fd, temporary_name = tempfile.mkstemp(prefix=".manifest-recovery-", dir=destination.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        safe_path(root, MANIFEST)
        os.link(str(temporary), str(destination))  # atomic publication, refuses overwrite
    finally:
        temporary.unlink()
    authenticated_bytes(destination, MANIFEST_SHA)
    return {"status": "RESTORED_EXACT_FROZEN_INPUT", "path": MANIFEST,
            "sha256": MANIFEST_SHA, "bytes": len(data)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = restore(args.root.absolute())
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
