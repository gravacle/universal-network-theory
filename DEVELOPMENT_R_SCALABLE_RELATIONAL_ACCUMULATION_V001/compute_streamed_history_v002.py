#!/usr/bin/env python3
"""Memory-only V002 wrapper for the fail-closed L10 target history."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import compute_streamed_history as core


ORIGINAL_BATCH_BYTES = 1_400_000_000
REPAIRED_BATCH_BYTES = 1_000_000_000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(length: int, output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"V002 refuses to overwrite completed output: {output}")
    if core.KRYLOV_STORAGE_BYTES != ORIGINAL_BATCH_BYTES:
        raise AssertionError("unexpected V001 batch-memory constant")
    core.KRYLOV_STORAGE_BYTES = REPAIRED_BATCH_BYTES
    exit_code = 0
    try:
        core.worker(length, output)
    except SystemExit as error:
        exit_code = int(error.code or 0)
    if not output.exists():
        raise AssertionError("base worker produced no result")
    result = json.loads(output.read_text())
    result["schema"] = "SCALABLE_RELATIONAL_STREAMED_HISTORY_ROW_V002"
    result["memory_only_repair"] = {
        "base_implementation_sha256": result["implementation_sha256"],
        "wrapper_implementation_sha256": sha256(Path(__file__)),
        "original_krylov_batch_bytes": ORIGINAL_BATCH_BYTES,
        "repaired_krylov_batch_bytes": REPAIRED_BATCH_BYTES,
        "physical_operator_changed": False,
        "basis_or_branch_changed": False,
        "numerical_threshold_changed": False,
        "resource_limit_changed": False,
    }
    result["implementation_sha256"] = sha256(Path(__file__))
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if exit_code:
        raise SystemExit(exit_code)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.worker, args.output)


if __name__ == "__main__":
    main()
