#!/usr/bin/env python3
"""Exact, allocation-free L4-L12 regression for the L14 successor formulas.

The regression never runs L14 numerical work.  It regenerates every Target and
Hostile cache member for each frozen predecessor size, authenticates every
array against its preserved manifest, reproduces the preserved L12 comparison
diagnostics, and reproduces every frozen Stage-6R2 classification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import mpmath

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE / "kernels"))

import checkpointed_history  # noqa: E402
from cache_builder import _hostile_arrays, _target_arrays  # noqa: E402
from exact_common import (  # noqa: E402
    ExactKernelRefusal,
    immutable_json,
    load_frozen,
    packet_root,
    read_json,
    sha256_file,
)
from geometry import _atoms, _predecessor, _prior_adjudication  # noqa: E402


SIZES = (4, 6, 8, 10, 12)
CROSS_PLATFORM_FLOAT_REL_TOLERANCE = 1.0e-12
CROSS_PLATFORM_FLOAT_ABS_TOLERANCE = 5.0e-15


def _compare_classification_values(
    preserved: Any,
    observed: Any,
    path: str,
    audit: dict[str, Any],
) -> None:
    """Authenticate classifications without requiring cross-libm bit identity.

    The frozen classifier is pure Python, but transcendental functions may
    differ by a few ulps between the preserved macOS runtime and production
    Linux.  Structure, discrete values, input rows, predicates, and decisions
    remain exact; only derived finite floats receive this explicit audit bound.
    """

    if isinstance(preserved, Mapping):
        if not isinstance(observed, Mapping) or set(preserved) != set(observed):
            raise ExactKernelRefusal("classification structure mismatch at {}".format(path))
        for key in sorted(preserved):
            _compare_classification_values(
                preserved[key], observed[key], "{}/{}".format(path, key), audit
            )
        return
    if isinstance(preserved, list):
        if not isinstance(observed, list) or len(preserved) != len(observed):
            raise ExactKernelRefusal("classification sequence mismatch at {}".format(path))
        for index, (left, right) in enumerate(zip(preserved, observed)):
            _compare_classification_values(
                left, right, "{}/{}".format(path, index), audit
            )
        return
    if (
        isinstance(preserved, (int, float))
        and not isinstance(preserved, bool)
        and isinstance(observed, (int, float))
        and not isinstance(observed, bool)
    ):
        if isinstance(preserved, int) and isinstance(observed, int):
            if preserved != observed:
                raise ExactKernelRefusal("classification integer mismatch at {}".format(path))
            audit["exact_discrete_values"] += 1
            return
        left, right = float(preserved), float(observed)
        if not math.isfinite(left) or not math.isfinite(right):
            raise ExactKernelRefusal("non-finite classification scalar at {}".format(path))
        absolute = abs(left - right)
        relative = absolute / max(abs(left), abs(right), 1.0e-300)
        audit["float_values"] += 1
        audit["maximum_absolute_difference"] = max(
            audit["maximum_absolute_difference"], absolute
        )
        audit["maximum_relative_difference"] = max(
            audit["maximum_relative_difference"], relative
        )
        if not math.isclose(
            left,
            right,
            rel_tol=CROSS_PLATFORM_FLOAT_REL_TOLERANCE,
            abs_tol=CROSS_PLATFORM_FLOAT_ABS_TOLERANCE,
        ):
            raise ExactKernelRefusal(
                "classification float mismatch at {}: abs={} rel={}".format(
                    path, absolute, relative
                )
            )
        return
    if type(preserved) is not type(observed) or preserved != observed:
        raise ExactKernelRefusal("classification discrete mismatch at {}".format(path))
    audit["exact_discrete_values"] += 1


def _array_hash(array: np.ndarray) -> str:
    return hashlib.sha256(memoryview(np.ascontiguousarray(array)).cast("B")).hexdigest()


def _cache_regression(
    branch: str,
    arrays: Iterable[tuple[str, np.ndarray, Mapping[str, Any]]],
    manifest_path: Path,
) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    expected = {record["path"]: record for record in manifest.get("files", [])}
    if len(expected) != len(manifest.get("files", [])):
        raise ExactKernelRefusal("duplicate frozen cache member")
    observed = set()
    total_bytes = 0
    for name, array, metadata in arrays:
        if name in observed or name not in expected:
            raise ExactKernelRefusal("{} unexpected cache member {}".format(branch, name))
        record = expected[name]
        if (
            record.get("dtype") != array.dtype.str
            or record.get("shape") != list(array.shape)
            or record.get("bytes") != array.nbytes
            or record.get("sha256") != _array_hash(array)
        ):
            raise ExactKernelRefusal("{} cache mismatch at {}".format(branch, name))
        for key, value in metadata.items():
            if record.get(key) != value:
                raise ExactKernelRefusal("{} cache metadata mismatch at {} {}".format(branch, name, key))
        observed.add(name)
        total_bytes += int(array.nbytes)
    if observed != set(expected):
        raise ExactKernelRefusal("{} cache census mismatch".format(branch))
    return {
        "status": "EXACT",
        "member_count": len(observed),
        "total_bytes": total_bytes,
        "manifest_path": str(manifest_path.resolve()),
        "manifest_sha256": sha256_file(manifest_path),
    }


def _diagnostic_regression() -> dict[str, Any]:
    packet = packet_root()
    records = {}
    frozen_length = checkpointed_history.LENGTH
    checkpointed_history.LENGTH = 12
    try:
        definitions = {
            "target": (
                packet / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/EVIDENCE/L12_PROCESS_PARALLEL_V003R1",
                "histories/002680__ROUGH_SUMMARY.json",
                "histories/006205__SHARP_SUMMARY.json",
                "comparison/006207__PRE_GATE_COMPARISON.json",
            ),
            "hostile": (
                packet / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_EVIDENCE/L12_PROCESS_PARALLEL_V003R1",
                "histories/000902__ROUGH_SUMMARY.json",
                "histories/001352__SHARP_SUMMARY.json",
                "comparison/001354__PRE_GATE_COMPARISON.json",
            ),
        }
        for branch, (base, rough_name, sharp_name, diagnostic_name) in definitions.items():
            rough_path, sharp_path, diagnostic_path = (
                base / rough_name,
                base / sharp_name,
                base / diagnostic_name,
            )
            rough = read_json(rough_path)["payload"]
            sharp = read_json(sharp_path)["payload"]
            preserved = read_json(diagnostic_path)["payload"]
            observed = checkpointed_history._comparison_evidence(
                branch, rough, sharp, preserved["comparison"]
            )
            for key in (
                "raw_metrics",
                "predicates",
                "computed_resolved",
                "reported_resolved",
                "resolved_agrees_with_predicates",
            ):
                if observed.get(key) != preserved.get(key):
                    raise ExactKernelRefusal("{} comparison diagnostic mismatch at {}".format(branch, key))
            records[branch] = {
                "status": "EXACT",
                "predicate_count": len(observed["predicates"]),
                "rough_sha256": sha256_file(rough_path),
                "sharp_sha256": sha256_file(sharp_path),
                "pre_gate_sha256": sha256_file(diagnostic_path),
            }
    finally:
        checkpointed_history.LENGTH = frozen_length
    return records


def _classification_regression(classifier: Any) -> dict[str, Any]:
    prior = _prior_adjudication()
    results = prior.get("atom_results")
    if not isinstance(results, list) or not results:
        raise ExactKernelRefusal("Stage-6R2 atom results absent")
    count = 0
    unavailable = 0
    comparison_audit = {
        "float_values": 0,
        "exact_discrete_values": 0,
        "maximum_absolute_difference": 0.0,
        "maximum_relative_difference": 0.0,
        "relative_tolerance": CROSS_PLATFORM_FLOAT_REL_TOLERANCE,
        "absolute_tolerance": CROSS_PLATFORM_FLOAT_ABS_TOLERANCE,
    }
    for atom in results:
        for name in ("target_classification", "blind_classification"):
            preserved = atom.get(name)
            if preserved is None:
                unavailable += 1
                continue
            if not isinstance(preserved, dict):
                raise ExactKernelRefusal(
                    "Stage-6R2 classification absent at {} {}".format(
                        atom.get("atom", {}).get("atom_id"), name
                    )
                )
            _compare_classification_values(
                preserved,
                classifier.classify(preserved.get("rows", [])),
                "{}/{}".format(atom.get("atom", {}).get("atom_id"), name),
                comparison_audit,
            )
            count += 1
    successor_atoms = _atoms()
    predecessors = []
    for atom in successor_atoms:
        predecessor = _predecessor(atom, prior)
        predecessors.append(predecessor["atom"]["atom_id"])
        if 4 <= int(atom["q_by_L"]["14"]) <= 9:
            if not all(
                isinstance(predecessor.get(name), dict)
                and len(predecessor[name].get("rows", [])) == 5
                for name in ("target_classification", "blind_classification")
            ):
                raise ExactKernelRefusal("in-scope L14 atom lacks a resolved five-row predecessor")
    return {
        "status": "EXACT",
        "classification_count": count,
        "explicitly_unavailable_classifications": unavailable,
        "l14_atom_count": len(successor_atoms),
        "l14_predecessor_census": len(predecessors),
        "unique_l12_predecessors": len(set(predecessors)),
        "cross_platform_float_audit": comparison_audit,
        "stage6r2_sha256": sha256_file(
            packet_root()
            / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/ADJUDICATION_V002_L12_V003R1_STAGE6R2.json"
        ),
    }


def run(require_linux_x86_64: bool) -> dict[str, Any]:
    started = time.time()
    machine = platform.machine().lower()
    system = platform.system().lower()
    if require_linux_x86_64 and not (system == "linux" and machine in {"x86_64", "amd64"}):
        raise ExactKernelRefusal("regression must run on Linux x86_64")
    repair, _target_response, _hostile_response, classifier, _interval = load_frozen()
    packet = packet_root()
    caches: dict[str, dict[str, Any]] = {"target": {}, "hostile": {}}
    for length in SIZES:
        caches["target"][str(length)] = _cache_regression(
            "target",
            _target_arrays(length, repair.target),
            packet / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012" / "L{}".format(length) / "CACHE_MANIFEST.json",
        )
        caches["hostile"][str(length)] = _cache_regression(
            "hostile",
            _hostile_arrays(length, repair.hostile),
            packet / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS" / "L{}".format(length) / "CACHE_MANIFEST.json",
        )
        print("REGRESSION_CACHE_EXACT L={}".format(length), flush=True)
    diagnostics = _diagnostic_regression()
    classifications = _classification_regression(classifier)
    return {
        "schema": "L14_L4_L12_EXACT_REGRESSION_V002",
        "status": "PASS",
        "scope": {
            "sizes": list(SIZES),
            "cache_members": "EVERY_MEMBER_BYTES_DTYPE_SHAPE_HASH_AND_ROLE",
            "comparison": "L12_ROUGH_SHARP_RAW_METRICS_AND_EVERY_ORIGINAL_PREDICATE",
            "geometry": "EVERY_STAGE6R2_TARGET_AND_BLIND_CLASSIFICATION_PLUS_L14_PREDECESSOR_PARTITION",
            "excluded": "NO_L14_NUMERICAL_WORK_AND_NO_AWS_ALLOCATION",
        },
        "runtime": {
            "system": system,
            "machine": machine,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "mpmath_version": mpmath.__version__,
        },
        "cache_regression": caches,
        "comparison_regression": diagnostics,
        "classification_regression": classifications,
        "elapsed_seconds": time.time() - started,
    }


def main(argv: Sequence[str] = ()) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--require-linux-x86-64", action="store_true")
    args = parser.parse_args(argv or sys.argv[1:])
    report = run(args.require_linux_x86_64)
    immutable_json(args.output, report)
    print("L4_L12_EXACT_REGRESSION_PASS report={} sha256={}".format(args.output, sha256_file(args.output)))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L4_L12_EXACT_REGRESSION_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr)
        raise SystemExit(2)
