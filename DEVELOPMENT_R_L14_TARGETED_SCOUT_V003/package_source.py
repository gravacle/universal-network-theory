#!/usr/bin/env python3
"""Create a deterministic source bundle only from authenticated kernel bindings."""

from __future__ import annotations

import argparse
import gzip
import io
import json
import sys
import tarfile
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any, Dict, Mapping, Sequence, Tuple

from durable_evidence import EvidenceError, canonical_json_bytes, immutable_write_bytes, immutable_write_json, load_json, sha256_bytes, sha256_file


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]


def safe_archive_path(raw: Any, label: str) -> str:
    if not isinstance(raw, str) or not raw:
        raise EvidenceError("{} must be a non-empty archive path".format(label))
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise EvidenceError("unsafe {}: {}".format(label, raw))
    return path.as_posix()


def authenticated_project_file(record: Mapping[str, Any], source_key: str, label: str) -> Tuple[Path, str]:
    raw_source = record.get(source_key)
    expected = record.get("sha256")
    if not isinstance(raw_source, str) or not isinstance(expected, str) or len(expected) != 64:
        raise EvidenceError("{} lacks an authenticated source path".format(label))
    source = (PROJECT_ROOT / raw_source).resolve()
    try:
        source.relative_to(PROJECT_ROOT.resolve())
    except ValueError as error:
        raise EvidenceError("{} escapes the project root".format(label)) from error
    if not source.is_file() or sha256_file(source) != expected:
        raise EvidenceError("{} is absent or changed".format(label))
    return source, expected


def add_authenticated_file(
    files: Dict[str, bytes],
    record: Mapping[str, Any],
    source_key: str,
    archive_key: str,
    label: str,
) -> Tuple[str, str]:
    source, digest = authenticated_project_file(record, source_key, label)
    archive_path = safe_archive_path(record.get(archive_key), "{} archive path".format(label))
    data = source.read_bytes()
    existing = files.get(archive_path)
    if existing is not None and existing != data:
        raise EvidenceError("bundle archive-path collision at {}".format(archive_path))
    files[archive_path] = data
    return archive_path, digest


def add_bundle_file_records(files: Dict[str, bytes], raw_records: Any, label: str) -> Dict[str, str]:
    if not isinstance(raw_records, list):
        raise EvidenceError("{} bundle_files must be a list".format(label))
    published: Dict[str, str] = {}
    for index, raw in enumerate(raw_records):
        if not isinstance(raw, dict):
            raise EvidenceError("{} bundle file {} is not an object".format(label, index))
        archive_path, digest = add_authenticated_file(
            files,
            raw,
            "source_path",
            "archive_path",
            "{} bundle file {}".format(label, index),
        )
        published[archive_path] = digest
    return published


def build_file_set(bindings: Mapping[str, Any]) -> Tuple[Dict[str, bytes], Dict[str, Any]]:
    """Authenticate every runtime/kernel dependency and return bundle bytes."""

    if bindings.get("schema") != "L14_EXACT_KERNEL_BINDINGS_V002":
        raise EvidenceError("wrong exact-kernel binding schema")
    if bindings.get("status") != "BOUND_AND_REGRESSION_AUTHENTICATED":
        raise EvidenceError("exact L14 kernels are not bound and regression-authenticated")

    regression = bindings.get("regression", {})
    if not isinstance(regression, dict) or regression.get("status") != "PASS":
        raise EvidenceError("L4-L12 exact regression is not authenticated")
    report_path, report_digest = authenticated_project_file(regression, "report_path", "L4-L12 exact regression report")

    runtime = bindings.get("runtime", {})
    if not isinstance(runtime, dict) or runtime.get("status") != "BOUND_AND_REGRESSION_AUTHENTICATED":
        raise EvidenceError("exact Linux x86_64 runtime is not bound and regression-authenticated")
    python_version = runtime.get("python_version")
    numpy_version = runtime.get("numpy_version")
    mpmath_version = runtime.get("mpmath_version")
    if not all(isinstance(value, str) and value for value in (python_version, numpy_version, mpmath_version)):
        raise EvidenceError("exact runtime lacks Python/NumPy/mpmath version bindings")

    files: Dict[str, bytes] = {}
    for relative in (
        "durable_evidence.py",
        "resumable_runtime.py",
        "branch_runner.py",
        "aws/aws_branch_once.py",
        "aws/run_branch_once.sh",
        "aws/run_performance_preflight.sh",
        "aws/runtime_guard.py",
        "aws/performance_preflight.py",
        "aws/verify_bundle.py",
    ):
        files[relative] = (HERE / relative).read_bytes()
    files["KERNEL_BINDINGS.json"] = canonical_json_bytes(dict(bindings))
    files["SOURCE_LINEAGE.json"] = (HERE / "SOURCE_LINEAGE.json").read_bytes()
    files["evidence/L4_L12_EXACT_REGRESSION.json"] = report_path.read_bytes()

    runtime_files = add_bundle_file_records(files, runtime.get("bundle_files"), "runtime")
    if not runtime_files:
        raise EvidenceError("exact runtime bundle is empty")
    requirements_path = safe_archive_path(
        runtime.get("requirements_archive_path"), "runtime requirements archive path"
    )
    wheelhouse_path = safe_archive_path(
        runtime.get("wheelhouse_archive_path"), "runtime wheelhouse archive path"
    ).rstrip("/")
    python_archive_path = safe_archive_path(
        runtime.get("python_archive_path"), "runtime Python archive path"
    )
    if (
        requirements_path != "runtime/requirements.lock"
        or wheelhouse_path != "runtime/wheelhouse"
        or not python_archive_path.startswith("runtime/python/")
        or not python_archive_path.endswith(".tar.gz")
    ):
        raise EvidenceError("runtime paths must use the reviewed Python/requirements/wheelhouse locations")
    if requirements_path not in runtime_files:
        raise EvidenceError("runtime requirements lock is not authenticated in bundle_files")
    if python_archive_path not in runtime_files:
        raise EvidenceError("runtime Python archive is not authenticated in bundle_files")
    wheel_prefix = wheelhouse_path + "/"
    if not any(path.startswith(wheel_prefix) and path.endswith(".whl") for path in runtime_files):
        raise EvidenceError("runtime wheelhouse contains no authenticated wheel")

    frozen_runtime = bindings.get("frozen_runtime", {})
    if not isinstance(frozen_runtime, dict) or frozen_runtime.get("status") != "BOUND":
        raise EvidenceError("frozen predecessor runtime is not bound")
    frozen_runtime_files = add_bundle_file_records(
        files, frozen_runtime.get("bundle_files"), "frozen predecessor runtime"
    )
    frozen_prefix = "frozen/audited-386ee2c/"
    if not frozen_runtime_files or any(
        not path.startswith(frozen_prefix) for path in frozen_runtime_files
    ):
        raise EvidenceError("frozen predecessor runtime must be isolated under frozen/audited-386ee2c")
    required_frozen_files = {
        frozen_prefix
        + "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/"
        + "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json",
        frozen_prefix
        + "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/PROTOCOL.md",
        frozen_prefix
        + "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/METHODOLOGY.md",
        frozen_prefix
        + "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/POST_OUTPUT_METHOD.md",
        frozen_prefix
        + "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md",
        frozen_prefix
        + "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/PROTOCOL.md",
    }
    absent = sorted(required_frozen_files - set(frozen_runtime_files))
    if absent:
        raise EvidenceError(
            "authenticated frozen mathematical definitions are absent: {}".format(absent)
        )

    kernel_locations: Dict[str, Dict[str, Any]] = {}
    for branch in ("target", "hostile"):
        record = bindings.get(branch, {})
        if not isinstance(record, dict) or record.get("status") != "BOUND":
            raise EvidenceError("{} exact kernel binding is absent".format(branch))
        arcname, digest = add_authenticated_file(
            files,
            record,
            "module_path",
            "module_archive_path",
            "{} exact kernel".format(branch),
        )
        dependencies = add_bundle_file_records(files, record.get("bundle_files"), "{} kernel".format(branch))
        kernel_locations[branch] = {
            "path": arcname,
            "sha256": digest,
            "dependencies": dependencies,
        }

    manifest = {
        "schema": "L14_SOURCE_BUNDLE_MANIFEST_V002",
        "regression": {
            "path": "evidence/L4_L12_EXACT_REGRESSION.json",
            "sha256": report_digest,
        },
        "runtime": {
            "python_version": python_version,
            "numpy_version": numpy_version,
            "mpmath_version": mpmath_version,
            "requirements_path": requirements_path,
            "wheelhouse_path": wheelhouse_path,
            "python_archive_path": python_archive_path,
            "files": runtime_files,
        },
        "frozen_runtime": {
            "files": frozen_runtime_files,
        },
        "kernels": kernel_locations,
        "files": {name: sha256_bytes(data) for name, data in sorted(files.items())},
    }
    return files, manifest


def tar_entry(archive: tarfile.TarFile, arcname: str, data: bytes, mode: int = 0o444) -> None:
    info = tarfile.TarInfo("l14-v003/" + arcname)
    info.size = len(data)
    info.mode = mode
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = 0
    archive.addfile(info, io.BytesIO(data))


def main(argv: Sequence[str] = ()) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bindings", type=Path, default=HERE / "KERNEL_BINDINGS_RELEASE_V003R3.json")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args(argv or sys.argv[1:])
    bindings = load_json(args.bindings)
    files, manifest = build_file_set(bindings)
    files["BUNDLE_MANIFEST.json"] = canonical_json_bytes(manifest)
    raw = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w") as archive:
            for name, data in sorted(files.items()):
                mode = 0o555 if name.endswith((".sh", ".py")) else 0o444
                tar_entry(archive, name, data, mode=mode)
    archive_bytes = raw.getvalue()
    immutable_write_bytes(args.output, archive_bytes)
    published_manifest = dict(manifest)
    published_manifest["archive"] = {
        "path": str(args.output.resolve()),
        "sha256": sha256_bytes(archive_bytes),
        "bytes": len(archive_bytes),
    }
    immutable_write_json(args.manifest, published_manifest)
    print("L14_SOURCE_BUNDLE output={} sha256={}".format(args.output, sha256_file(args.output)))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_SOURCE_BUNDLE_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr)
        raise SystemExit(2)
