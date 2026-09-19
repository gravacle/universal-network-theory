#!/usr/bin/env python3
"""Authenticate an extracted L14 bundle and, optionally, its Python runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


class BundleVerificationError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(root: Path, raw: Any) -> Path:
    if not isinstance(raw, str) or not raw:
        raise BundleVerificationError("manifest contains an empty path")
    relative = PurePosixPath(raw)
    if relative.is_absolute() or any(part in ("", ".", "..") for part in relative.parts):
        raise BundleVerificationError("unsafe manifest path: {}".format(raw))
    path = (root / Path(*relative.parts)).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise BundleVerificationError("manifest path escapes bundle: {}".format(raw)) from error
    return path


def verify_files(root: Path, manifest: Mapping[str, Any]) -> None:
    if manifest.get("schema") != "L14_SOURCE_BUNDLE_MANIFEST_V002":
        raise BundleVerificationError("wrong source-bundle manifest schema")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise BundleVerificationError("manifest file inventory is empty")
    for raw_path, expected in sorted(files.items()):
        if not isinstance(expected, str) or len(expected) != 64:
            raise BundleVerificationError("invalid SHA-256 for {}".format(raw_path))
        path = safe_member(root, raw_path)
        if not path.is_file() or path.is_symlink():
            raise BundleVerificationError("missing or non-regular bundle file: {}".format(raw_path))
        actual = sha256_file(path)
        if actual != expected:
            raise BundleVerificationError("bundle digest mismatch at {}".format(raw_path))


def verify_runtime(manifest: Mapping[str, Any]) -> None:
    runtime = manifest.get("runtime")
    if not isinstance(runtime, dict):
        raise BundleVerificationError("runtime binding is absent")
    expected_python = runtime.get("python_version")
    actual_python = platform.python_version()
    if actual_python != expected_python:
        raise BundleVerificationError(
            "Python runtime mismatch: {} != {}".format(actual_python, expected_python)
        )
    try:
        import numpy  # type: ignore
    except ImportError as error:
        raise BundleVerificationError("NumPy is absent from the exact runtime") from error
    if numpy.__version__ != runtime.get("numpy_version"):
        raise BundleVerificationError(
            "NumPy runtime mismatch: {} != {}".format(
                numpy.__version__, runtime.get("numpy_version")
            )
        )
    try:
        import mpmath  # type: ignore
    except ImportError as error:
        raise BundleVerificationError("mpmath is absent from the exact runtime") from error
    if mpmath.__version__ != runtime.get("mpmath_version"):
        raise BundleVerificationError(
            "mpmath runtime mismatch: {} != {}".format(
                mpmath.__version__, runtime.get("mpmath_version")
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--verify-runtime", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = root / "BUNDLE_MANIFEST.json"
    if not manifest_path.is_file():
        raise BundleVerificationError("BUNDLE_MANIFEST.json is absent")
    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if not isinstance(manifest, dict):
        raise BundleVerificationError("bundle manifest is not an object")
    verify_files(root, manifest)
    if args.verify_runtime:
        verify_runtime(manifest)
    print(
        "L14_BUNDLE_VERIFIED files={} runtime={}".format(
            len(manifest["files"]), "yes" if args.verify_runtime else "not-requested"
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(
            "L14_BUNDLE_VERIFICATION_FAILURE type={} message={}".format(
                type(error).__name__, error
            ),
            file=sys.stderr,
            flush=True,
        )
        raise SystemExit(2)
