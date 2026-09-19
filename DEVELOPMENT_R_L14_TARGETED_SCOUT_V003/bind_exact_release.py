#!/usr/bin/env python3
"""Owner-once binding of the exact L14 port and its complete frozen runtime."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from durable_evidence import immutable_write_json, load_json, sha256_file


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
FROZEN_DIRECTORIES = (
    "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V001",
    "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V002",
    "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V003",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001",
    "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001",
    "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001",
    "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001",
)
FROZEN_DEFINITIONS = (
    "DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/PROTOCOL.md",
    "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/METHODOLOGY.md",
    "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/POST_OUTPUT_METHOD.md",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md",
    "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/PROTOCOL.md",
    "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/ADJUDICATION_V002_L12_V003R1_STAGE6R2.json",
)


class BindingRefusal(RuntimeError):
    pass


def project_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError as error:
        raise BindingRefusal("binding source escapes project root: {}".format(path)) from error


def record(path: Path, archive_path: str) -> dict[str, str]:
    if not path.is_file() or path.is_symlink():
        raise BindingRefusal("binding source is absent or unsafe: {}".format(path))
    return {
        "source_path": project_path(path),
        "archive_path": archive_path,
        "sha256": sha256_file(path),
    }


def kernel(branch: str) -> dict[str, Any]:
    module = HERE / "kernels" / "{}_exact_kernel.py".format(branch)
    dependencies = [
        record(HERE / "kernels" / name, "kernel/{}".format(name))
        for name in (
            "exact_common.py",
            "cache_builder.py",
            "checkpointed_history.py",
            "geometry.py",
            "resource_scheduler.py",
        )
    ]
    return {
        "status": "BOUND",
        "module_path": project_path(module),
        "module_archive_path": "kernel/{}_exact_kernel.py".format(branch),
        "sha256": sha256_file(module),
        "bundle_files": dependencies,
        "scope": "EXACT_LENGTH_GENERIC_L14_PORT__ORIGINAL_PHYSICS_PREDICATES_AND_TOLERANCES_UNCHANGED",
    }


def frozen_runtime() -> list[dict[str, str]]:
    packet = PROJECT_ROOT / "audited-386ee2c"
    paths: set[Path] = set()
    for directory in FROZEN_DIRECTORIES:
        root = packet / directory
        if not root.is_dir():
            raise BindingRefusal("frozen source directory is absent: {}".format(root))
        paths.update(root.glob("*.py"))
    paths.update(packet / relative for relative in FROZEN_DEFINITIONS)
    records = []
    for path in sorted(paths):
        relative = path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
        records.append(record(path, "frozen/{}".format(relative)))
    return records


def build(regression_path: Path, audit_path: Path) -> dict[str, Any]:
    regression = load_json(regression_path)
    if (
        regression.get("schema") != "L14_L4_L12_EXACT_REGRESSION_V002"
        or regression.get("status") != "PASS"
        or regression.get("runtime", {}).get("system") != "linux"
        or regression.get("runtime", {}).get("machine") not in {"x86_64", "amd64"}
        or regression.get("runtime", {}).get("python_version") != "3.11.16"
        or regression.get("runtime", {}).get("numpy_version") != "2.0.2"
        or regression.get("runtime", {}).get("mpmath_version") != "1.3.0"
    ):
        raise BindingRefusal("production Linux regression is absent or has the wrong identity")
    audit = load_json(audit_path)
    if audit.get("schema") != "L14_EXACT_KERNEL_RELEASE_AUDIT_V003" or audit.get("status") != "PASS":
        raise BindingRefusal("exact release audit is absent or unresolved")

    runtime_records = [
        record(HERE / "runtime" / "requirements.lock", "runtime/requirements.lock"),
        record(
            HERE / "runtime" / "python" / "cpython-3.11.16+20260901-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz",
            "runtime/python/cpython-3.11.16+20260901-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz",
        ),
        record(
            HERE / "runtime" / "wheelhouse" / "numpy-2.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            "runtime/wheelhouse/numpy-2.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
        ),
        record(
            HERE / "runtime" / "wheelhouse" / "mpmath-1.3.0-py3-none-any.whl",
            "runtime/wheelhouse/mpmath-1.3.0-py3-none-any.whl",
        ),
    ]
    return {
        "schema": "L14_EXACT_KERNEL_BINDINGS_V002",
        "status": "BOUND_AND_REGRESSION_AUTHENTICATED",
        "target": kernel("target"),
        "hostile": kernel("hostile"),
        "runtime": {
            "status": "BOUND_AND_REGRESSION_AUTHENTICATED",
            "platform": "linux_x86_64_manylinux_2_17",
            "python_version": "3.11.16",
            "numpy_version": "2.0.2",
            "mpmath_version": "1.3.0",
            "requirements_archive_path": "runtime/requirements.lock",
            "wheelhouse_archive_path": "runtime/wheelhouse",
            "python_archive_path": "runtime/python/cpython-3.11.16+20260901-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz",
            "bundle_files": runtime_records,
        },
        "frozen_runtime": {
            "status": "BOUND",
            "bundle_files": frozen_runtime(),
        },
        "regression": {
            "status": "PASS",
            "report_path": project_path(regression_path),
            "sha256": sha256_file(regression_path),
        },
        "port_audit": {
            "status": "PASS",
            "report_path": project_path(audit_path),
            "sha256": sha256_file(audit_path),
        },
        "claim_boundary": "PREPARED_EXACT_L14_EXECUTABLE__NO_L14_NUMERICAL_RESULT__NO_AWS_RESOURCE_ALLOCATION__NO_LAUNCH_AUTHORIZATION",
        "remaining_launch_gates": [
            "launch_enabled must remain false until a separate paid-launch authorization",
            "live identity, quota, price, budget, AMI, subnet, and no-duplicate checks must pass immediately before launch",
            "the control role/profile must be created and assumed only for the authorized launch",
        ],
    }


def main(argv: Sequence[str] = ()) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--regression",
        type=Path,
        default=HERE / "L4_L12_EXACT_REGRESSION_LINUX_X86_64.json",
    )
    parser.add_argument(
        "--audit", type=Path, default=HERE / "EXACT_KERNEL_AUDIT_V003.json"
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv or sys.argv[1:])
    immutable_write_json(args.output, build(args.regression, args.audit))
    print("L14_EXACT_BINDING_COMPLETE output={} sha256={}".format(args.output, sha256_file(args.output)))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_EXACT_BINDING_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr)
        raise SystemExit(2)
