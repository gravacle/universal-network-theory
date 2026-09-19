#!/usr/bin/env python3
"""Read-only forensic reconstruction for the failed target L12 publication.

This program never invokes the launcher, never opens an array writable, and
never exits nonzero for an unresolved or incomplete reconstruction.  It uses
the exact comparison function reached by the target process through
``target_parallel.target.v004.sealed.summarize`` when complete rough and sharp
history dictionaries are available.

The failed PROCESS_PARALLEL_V001 run did not persist those dictionaries.  In
that case this program reports the exact on-disk census, streams the surviving
sharp preterminal state to recover the quantities that are derivable from it,
and explicitly marks terminal/post-transport quantities as unavailable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_PACKET = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
WORKSPACE = TARGET_PACKET / "WORKSPACES" / "L12_PROCESS_PARALLEL_V001"
SHARP_STATE = WORKSPACE / "sharp" / "prefix_11"
CACHE_ROOT = TARGET_PACKET / "CACHE_PAYLOADS_V012" / "L12"
CACHE_MANIFEST = CACHE_ROOT / "CACHE_MANIFEST.json"
TARGET_LOG = HERE / "RUN_LOGS" / "L12_PROCESS_PARALLEL_V001" / "target.log"
PUBLISHED_HISTORY = (
    TARGET_PACKET / "PHYSICAL_OUTPUTS" / "HISTORY_L12_PROCESS_PARALLEL_V001.json"
)
PRIOR_STATE = TARGET_PACKET / "WORKSPACES" / "L12" / "sharp" / "prefix_11"

LENGTH = 12
EXPECTED_TASKS = 4_714
EXPECTED_Q = tuple(range(LENGTH))
COMPARISON_METRICS = (
    "reverse_support_probability",
    "transport_node_residual_l1",
    "actual_norm_error",
    "transport_number_drift",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(16 * 2**20):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} is not a JSON object")
    return value


def exact_summarize() -> tuple[Any, str]:
    """Import the same function called at execution_integration.py:67."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import target_parallel  # pylint: disable=import-outside-toplevel

    function = target_parallel.target.v004.sealed.summarize
    source = Path(function.__code__.co_filename).resolve()
    return function, f"{source}:{function.__code__.co_firstlineno}"


def file_record(path: Path) -> dict[str, Any]:
    metadata = os.stat(path, follow_symlinks=False)
    return {
        "path": str(path),
        "bytes": metadata.st_size,
        "mode": stat.filemode(metadata.st_mode),
        "writable": bool(metadata.st_mode & 0o222),
        "sha256": sha256_file(path),
    }


def parse_terminal_log() -> dict[str, Any]:
    if not TARGET_LOG.is_file():
        return {"present": False, "path": str(TARGET_LOG)}
    lines = TARGET_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    final_progress = next(
        (line for line in reversed(lines) if "stage=full_rough_plus_sharp_run" in line),
        None,
    )
    refusal = next(
        (line for line in reversed(lines) if "L12_BRANCH_REFUSED branch=target" in line),
        None,
    )
    completed = total = None
    if final_progress:
        match = re.search(r"completed=(\d+)\s+total=(\d+)", final_progress)
        if match:
            completed, total = (int(match.group(1)), int(match.group(2)))
    return {
        "present": True,
        "path": str(TARGET_LOG),
        "sha256": sha256_file(TARGET_LOG),
        "final_progress": final_progress,
        "completed_tasks": completed,
        "total_tasks": total,
        "expected_tasks": EXPECTED_TASKS,
        "refusal": refusal,
    }


def manifest_files() -> dict[str, dict[str, Any]]:
    manifest = load_json(CACHE_MANIFEST)
    rows = manifest.get("files")
    if not isinstance(rows, list):
        raise TypeError("cache manifest files is not a list")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("path"), str):
            result[row["path"]] = row
    return result


def stream_preterminal_state() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Recover only event-12 *input* statistics from the retained sharp state."""
    files = manifest_files()
    sector_weights = np.zeros(LENGTH + 1, dtype=np.float64)
    allow_probability = 0.0
    blocked_probability = 0.0
    shard_records: list[dict[str, Any]] = []
    maximum_chunk_bytes = 64 * 2**20

    for q in EXPECTED_Q:
        shard = SHARP_STATE / f"q_{q:02d}.npy"
        if shard.is_symlink() or not shard.is_file():
            raise FileNotFoundError(f"missing canonical sharp shard q={q}: {shard}")
        block = np.load(shard, mmap_mode="r", allow_pickle=False)
        expected_shape = (math.comb(LENGTH - 1, q), math.comb(2 * LENGTH, q))
        if block.dtype != np.dtype("<c16") or block.shape != expected_shape:
            raise ValueError(
                f"sharp shard q={q} has dtype/shape {block.dtype}/{block.shape}, "
                f"expected complex128/{expected_shape}"
            )

        words_name = f"carrier_q_{q:02d}_words.u32"
        words_record = files.get(words_name)
        if not isinstance(words_record, dict):
            raise KeyError(f"cache manifest lacks {words_name}")
        words_path = CACHE_ROOT / words_name
        if words_path.is_symlink() or not words_path.is_file():
            raise FileNotFoundError(f"missing canonical carrier words q={q}")
        if sha256_file(words_path) != words_record.get("sha256"):
            raise ValueError(f"carrier words q={q} failed manifest SHA-256")
        words = np.memmap(words_path, dtype=np.dtype("<u4"), mode="r")
        if words.shape != (expected_shape[1],):
            raise ValueError(f"carrier words q={q} shape mismatch")
        occupied = ((words >> (LENGTH - 1)) & 1) == 1

        rows_per_chunk = max(
            1, maximum_chunk_bytes // max(16, expected_shape[1] * 16)
        )
        weight = 0.0
        allowed = 0.0
        blocked = 0.0
        for lower in range(0, expected_shape[0], rows_per_chunk):
            upper = min(expected_shape[0], lower + rows_per_chunk)
            view = np.asarray(block[lower:upper])
            probabilities = np.einsum(
                "ij,ij->j", view.real, view.real, optimize=False
            )
            probabilities += np.einsum(
                "ij,ij->j", view.imag, view.imag, optimize=False
            )
            weight += float(np.sum(probabilities))
            blocked += float(np.sum(probabilities[occupied]))
            allowed += float(np.sum(probabilities[~occupied]))

        sector_weights[q] = weight
        allow_probability += allowed
        blocked_probability += blocked
        record = file_record(shard)
        record.update({"q": q, "dtype": block.dtype.str, "shape": list(block.shape)})
        if (PRIOR_STATE / shard.name).is_file():
            record["prior_serial_copy_sha256"] = sha256_file(PRIOR_STATE / shard.name)
            record["matches_prior_serial_copy"] = (
                record["prior_serial_copy_sha256"] == record["sha256"]
            )
        shard_records.append(record)
        del block, words, occupied

    norm = float(np.sum(sector_weights))
    retained_number = float(np.dot(np.arange(LENGTH + 1), sector_weights))
    return (
        {
            "scope": "sharp event-12 input (prefix_11), not the lost terminal output",
            "sector_weights": sector_weights.tolist(),
            "norm": norm,
            "preterminal_null_norm_error": abs(norm - 1.0),
            "retained_number": retained_number,
            "allow_probability": allow_probability,
            "blocked_probability": blocked_probability,
            "reverse_support_probability": 0.0,
            "reverse_support_basis": (
                "the frozen target statistics() assigns reverse=0.0 for every row"
            ),
        },
        shard_records,
    )


def maxima_from_rows(rows: Any) -> dict[str, float]:
    if not isinstance(rows, list) or not rows:
        raise TypeError("history rows are absent")
    return {
        key: max(abs(float(row[key])) for row in rows)
        for key in COMPARISON_METRICS
    }


def comparison_thresholds() -> dict[str, Any]:
    return {
        "all_fine_actual_and_null_solvers_converged": True,
        "maximum_admission_or_owner_accounting_residual": 1.0e-10,
        "minimum_W_n": ">= -epsilon",
        "epsilon": "max(1e-11, 50 * max(observable_linf, sector_weight_linf))",
        "maximum_reverse_support_probability": 1.0e-11,
        "maximum_transport_node_residual_l1": "max(1e-9, 100 * epsilon)",
        "maximum_actual_norm_error": 1.0e-10,
        "maximum_transport_number_drift": 1.0e-10,
        "maximum_blocked_probability": "> 1e-6",
        "important": (
            "maximum rough/sharp disagreement has no direct upper-bound predicate; "
            "it only sets epsilon"
        ),
    }


def reconstruct(args: argparse.Namespace) -> dict[str, Any]:
    summarize, summarize_source = exact_summarize()
    payload: dict[str, Any] = {
        "schema": "TARGET_L12_READ_ONLY_FORENSIC_RECONSTRUCTION_V001",
        "read_only": True,
        "launcher_invoked": False,
        "summarize_source": summarize_source,
        "log": parse_terminal_log(),
        "comparison_thresholds": comparison_thresholds(),
        "published_history_present": PUBLISHED_HISTORY.is_file(),
        "rough_workspace_present": (WORKSPACE / "rough").exists(),
    }

    preterminal, shards = stream_preterminal_state()
    payload["preserved_shard_census"] = {
        "count": len(shards),
        "expected_q": list(EXPECTED_Q),
        "all_read_only": all(not row["writable"] for row in shards),
        "all_match_prior_serial_copy": all(
            row.get("matches_prior_serial_copy") is True for row in shards
        ),
        "total_bytes": sum(int(row["bytes"]) for row in shards),
        "shards": shards,
    }
    payload["recoverable_preterminal_metrics"] = preterminal

    if args.rough_summary and args.sharp_summary:
        rough = load_json(args.rough_summary)
        sharp = load_json(args.sharp_summary)
        comparison = summarize(LENGTH, rough, sharp)
        payload["status"] = (
            "RESOLVED_RELATIONAL_HISTORY_L"
            if comparison.get("resolved") is True
            else "UNRESOLVED_RELATIONAL_HISTORY_L"
        )
        payload["comparison"] = comparison
        payload["requested_metric_maxima"] = maxima_from_rows(sharp.get("rows"))
        payload["complete_parent_dictionary_reconstructed"] = True
        return payload

    if PUBLISHED_HISTORY.is_file():
        history = load_json(PUBLISHED_HISTORY)
        payload["status"] = "PUBLISHED_HISTORY_FOUND"
        payload["comparison"] = history.get("comparison")
        payload["requested_metric_maxima"] = maxima_from_rows(history.get("rows"))
        payload["complete_parent_dictionary_reconstructed"] = False
        payload["note"] = "sharp maxima recovered; rough rows are still required to rerun summarize()"
        return payload

    payload["status"] = "UNRESOLVED_RELATIONAL_HISTORY_L__INSUFFICIENT_PERSISTED_REDUCTIONS"
    payload["comparison"] = None
    payload["requested_metric_maxima"] = {
        "reverse_support_probability": 0.0,
        "transport_node_residual_l1": None,
        "actual_norm_error": None,
        "transport_number_drift": None,
    }
    payload["complete_parent_dictionary_reconstructed"] = False
    payload["missing_evidence"] = [
        "rough rows for events 1-12 (rough workspace was deliberately removed)",
        "sharp rows for events 1-11 (worker reductions existed only in parent memory)",
        "sharp terminal event-12 reduction (worker reductions existed only in parent memory)",
        "24 fine actual/null solver convergence summaries",
        "the comparison dictionary itself (publication occurred after the resolved gate)",
    ]
    payload["conclusion"] = (
        "No exact failing predicate can be selected from the surviving files. "
        "The 12 retained arrays are the sharp preterminal state, not 4,714 persisted "
        "task-result shards. Re-running terminal evolution would still not recover the "
        "deleted rough rows or sharp event 1-11 reductions."
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rough-summary",
        type=Path,
        help="optional complete rough history dictionary for exact summarize() replay",
    )
    parser.add_argument(
        "--sharp-summary",
        type=Path,
        help="optional complete sharp history dictionary for exact summarize() replay",
    )
    try:
        arguments = parser.parse_args()
        print(json.dumps(reconstruct(arguments), indent=2, sort_keys=True))
    except BaseException as error:  # forensic tooling must report, never fail closed
        print(json.dumps({
            "schema": "TARGET_L12_READ_ONLY_FORENSIC_RECONSTRUCTION_V001",
            "read_only": True,
            "launcher_invoked": False,
            "status": "FORENSIC_RECONSTRUCTION_ERROR_CAUGHT",
            "error_type": type(error).__name__,
            "error": str(error),
        }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
