#!/usr/bin/env python3
"""Fail-closed complete-state adjudication of target/hostile L12 histories."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import tempfile
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FREEZE = HERE / "L12_CROSS_ADJUDICATION_FREEZE_V001.json"
METHOD = HERE / "L12_CROSS_ADJUDICATION_METHOD_V001.md"
EXECUTION_CUSTODY = HERE / "L12_ACTIVE_EXECUTION_CUSTODY_V001.json"
LENGTH = 12
TOLERANCE = 1.0e-8
TARGET_SCHEMA = "TARGET_Q_SHARDED_PREFIX_HISTORY_V004"
HOSTILE_SCHEMA = "INDEPENDENT_Q_SHARDED_PREFIX_HISTORY_L12_V003"
REPRESENTATION = "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS"
LINEAGE_AUTHORITY = "FULL_CANONICAL_MASK__SHA256_CUSTODY_ONLY"
EXPECTED_DEPENDENCIES = {
    "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py":
        "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7",
    "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md":
        "864113577059c5214923d4d1709e0d2a4483131f816b42bc43f7fc14a72b19ef",
    "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json":
        "629ab8bc8e3c2a70c8e79a788ddeb6bafd3503491cef3b331bcc97a1555c2359",
    "independent_prefix_history_v003.py":
        "cc4e1195283f60fddab1d70831965bd14a09435fd4aca2ee7fdde7e2d7e5ba7f",
    "V003_L12_EXECUTABLE_METHOD.md":
        "32a6f397c586328c07fdefc1aae0b4bb8e98de7783386c209104a68d577b418a",
    "L10_GATE_V002.json":
        "c94685d15e15016c5d10673857b96bf1b9ee0ec1a1da3b0d11a9957320f18eb2",
    "L12_ACTIVE_EXECUTION_CUSTODY_V001.json":
        "a57a29cc0116556ad3b2a7777d25d499596c4a4cd035865384a858af43808ddd",
}
SCALARS = (
    "W_n",
    "allow_probability",
    "blocked_probability",
    "reverse_support_probability",
    "blocked_null_state_error",
    "connector_delta_l1",
    "connector_delta_signed",
    "admission_total_content_residual",
    "admission_bandwidth_residual",
    "target_owner_residual",
    "transport_node_residual_l1",
    "transport_node_residual_linf",
    "transport_number_drift",
    "actual_norm_error",
    "null_norm_error",
    "q_genesis_after",
    "q_retained_after_transport",
)


class FailClosed(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise FailClosed(message)


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            result.update(chunk)
    return result.hexdigest()


def valid_digest(value: str) -> bool:
    return len(value) == 64 and set(value) <= set("0123456789abcdef")


def checked_result(path: Path, expected: str, label: str) -> dict[str, object]:
    demand(valid_digest(expected), f"{label}: invalid SHA-256")
    resolved = path.resolve()
    demand(resolved.is_relative_to(ROOT.resolve()), f"{label}: result escapes repository")
    demand(resolved.is_file(), f"{label}: result missing")
    demand(digest(resolved) == expected, f"{label}: result SHA-256 mismatch")
    return json.loads(resolved.read_text())


def verify_freeze(expected_digest: str) -> None:
    demand(FREEZE.is_file(), "cross-adjudication freeze missing")
    demand(valid_digest(expected_digest) and digest(FREEZE) == expected_digest,
           "cross-adjudication freeze SHA-256")
    freeze = json.loads(FREEZE.read_text())
    demand(freeze.get("schema") == "AUDIT_R_L12_CROSS_ADJUDICATION_PRE_OUTPUT_FREEZE_V001",
           "cross-adjudication freeze schema")
    demand(freeze.get("status") == "FROZEN_BEFORE_L12_HISTORY_OUTPUT",
           "cross-adjudication freeze status")
    demand(freeze.get("l12_history_outputs_present_at_freeze") is False,
           "cross-adjudication pre-output declaration")
    files = freeze.get("files")
    demand(isinstance(files, dict) and set(files) == {METHOD.name, Path(__file__).name},
           "cross-adjudication file census")
    demand(files.get(METHOD.name) == digest(METHOD), "cross-adjudication method custody")
    demand(files.get(Path(__file__).name) == digest(Path(__file__)),
           "cross-adjudication implementation custody")
    dependencies = freeze.get("dependencies")
    demand(dependencies == EXPECTED_DEPENDENCIES, "cross-adjudication dependency census")
    for relative, expected in dependencies.items():
        path = (HERE / relative).resolve()
        demand(path.is_relative_to(ROOT.resolve()) and path.is_file(),
               f"cross-adjudication dependency path: {relative}")
        demand(valid_digest(expected) and digest(path) == expected,
               f"cross-adjudication dependency custody: {relative}")
    demand(freeze.get("tolerance") == TOLERANCE, "cross-adjudication tolerance")
    demand(freeze.get("complete_terminal_state_required") is True,
           "complete-terminal-state requirement")
    demand(freeze.get("claim_boundary") ==
           "PRE_OUTPUT_METHOD_FREEZE_ONLY__NO_L12_RESULT_OR_PHYSICS_CLAIM",
           "cross-adjudication claim boundary")


def finite(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(float(value))


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def rows(history: dict[str, object], label: str) -> list[dict[str, object]]:
    value = history.get("rows")
    demand(isinstance(value, list) and len(value) == LENGTH, f"{label}: event census")
    demand(all(isinstance(row, dict) for row in value), f"{label}: row type")
    demand(all(type(row.get("event")) is int for row in value),
           f"{label}: integer event identifiers")
    demand([row["event"] for row in value] == list(range(1, LENGTH + 1)),
           f"{label}: event order")
    return value


def solver_pass(record: object, label: str, role: str, terminal: bool) -> None:
    demand(isinstance(record, dict), f"{label}: solver record")
    demand(record.get("converged") is True, f"{label}: solver unresolved")
    if role == "target":
        required_int = (
            "batches", "low_memory_batches", "maximum_krylov_steps",
            "maximum_live_bytes", "maximum_subdivisions", "quadrature_nodes",
        )
        required_float = ("maximum_exp_difference", "maximum_residual_indicator")
        for field in required_int:
            demand(type(record.get(field)) is int and int(record[field]) >= 0,
                   f"{label}: integer {field}")
        demand(record["batches"] > 0 and record["maximum_subdivisions"] >= 1,
               f"{label}: target batch/subdivision census")
        demand(record["maximum_subdivisions"] <= 16,
               f"{label}: target subdivision cap")
        demand(record["low_memory_batches"] <= record["batches"],
               f"{label}: target low-memory batch census")
        demand(record["maximum_krylov_steps"] <= 64,
               f"{label}: target Krylov cap")
        demand(record["maximum_live_bytes"] <= 1_000_000_000,
               f"{label}: target workset cap")
        demand(record["quadrature_nodes"] == 24,
               f"{label}: target quadrature")
        for field in required_float:
            demand(finite(record.get(field)) and float(record[field]) >= 0.0,
                   f"{label}: finite {field}")
        demand(float(record["maximum_exp_difference"]) <= 5.0e-11,
               f"{label}: target endpoint comparison")
        demand(float(record["maximum_residual_indicator"]) <= 1.0e-8,
               f"{label}: target residual indicator")
    else:
        required_int = (
            "allocation_limit_bytes", "allocation_vector_slots", "batches",
            "maximum_allocation_estimate_bytes", "maximum_degree",
            "quadrature_group_max", "quadrature_nodes",
        )
        required_float = ("maximum_endpoint_difference", "maximum_tail_indicator_32")
        demand(record.get("algorithm") == "RECURRENCE_REPLAY_GL_GROUPS",
               f"{label}: hostile algorithm")
        for field in required_int:
            demand(type(record.get(field)) is int and int(record[field]) >= 0,
                   f"{label}: integer {field}")
        demand(record["batches"] > 0 and record["allocation_vector_slots"] == 20,
               f"{label}: hostile batch/vector census")
        demand(record["allocation_limit_bytes"] == 1_400_000_000,
               f"{label}: hostile allocation limit")
        demand(record["maximum_allocation_estimate_bytes"] <= 1_400_000_000,
               f"{label}: hostile allocation cap")
        demand(record["maximum_degree"] <= 96 and record["quadrature_group_max"] == 12
               and record["quadrature_nodes"] == 28,
               f"{label}: hostile method caps")
        for field in required_float:
            demand(finite(record.get(field)) and float(record[field]) >= 0.0,
                   f"{label}: finite {field}")
        demand(float(record["maximum_endpoint_difference"]) <= 8.0e-11,
               f"{label}: hostile endpoint comparison")
        demand(float(record["maximum_tail_indicator_32"]) <= 8.0e-11,
               f"{label}: hostile tail indicator")
        if terminal and label.endswith("actual"):
            demand(record.get("terminal_children_streamed") is True,
                   f"{label}: hostile terminal stream")
            demand(record.get("terminal_child0_entries") ==
                   math.comb(3 * LENGTH - 1, LENGTH - 1),
                   f"{label}: hostile terminal child0 census")
            demand(record.get("terminal_child1_nonzero_admission_entries") ==
                   math.comb(3 * LENGTH - 2, LENGTH - 1),
                   f"{label}: hostile terminal child1 census")
            demand(record.get("full_terminal_array_allocated") is False,
                   f"{label}: hostile H12 nonallocation")


def resource_pass(history: dict[str, object], role: str) -> bool:
    record = history.get("resource")
    if not isinstance(record, dict):
        return False
    common = (
        type(record.get("peak_logical_scratch_bytes")) is int
        and type(record.get("scratch_limit_bytes")) is int
        and record["scratch_limit_bytes"] == 20 * 2**30
        and 0 <= record["peak_logical_scratch_bytes"] <= record["scratch_limit_bytes"]
        and type(record.get("peak_rss_bytes")) is int
        and type(record.get("rss_limit_bytes")) is int
        and record["rss_limit_bytes"] == 16 * 2**30
        and 0 <= record["peak_rss_bytes"] <= record["rss_limit_bytes"]
        and finite(record.get("wall_seconds"))
        and finite(record.get("wall_limit_seconds"))
        and float(record["wall_limit_seconds"]) == 21600.0
        and 0.0 <= float(record["wall_seconds"]) <= float(record["wall_limit_seconds"])
    )
    if role == "target":
        expected_keys = {
            "peak_logical_scratch_bytes", "scratch_limit_bytes",
            "maximum_numerical_workset_bytes", "numerical_workset_limit_bytes",
            "peak_rss_bytes", "rss_limit_bytes", "wall_seconds",
            "wall_limit_seconds", "passed",
        }
        method = (
            set(record) == expected_keys
            and type(record.get("maximum_numerical_workset_bytes")) is int
            and type(record.get("numerical_workset_limit_bytes")) is int
            and record["numerical_workset_limit_bytes"] == 1_000_000_000
            and 0 <= record["maximum_numerical_workset_bytes"]
            <= record["numerical_workset_limit_bytes"]
        )
    else:
        expected_keys = {
            "peak_logical_scratch_bytes", "scratch_limit_bytes",
            "maximum_numerical_allocation_estimate_bytes",
            "numerical_workspace_limit_bytes", "peak_rss_bytes", "rss_limit_bytes",
            "wall_seconds", "wall_limit_seconds", "passed",
        }
        method = (
            set(record) == expected_keys
            and type(record.get("maximum_numerical_allocation_estimate_bytes")) is int
            and type(record.get("numerical_workspace_limit_bytes")) is int
            and record["numerical_workspace_limit_bytes"] == 1_400_000_000
            and 0 <= record["maximum_numerical_allocation_estimate_bytes"]
            <= record["numerical_workspace_limit_bytes"]
        )
    return bool(common and method and record.get("passed") is True)


def resolution_pass(history: dict[str, object], key: str) -> bool:
    comparison = history.get("comparison")
    if not isinstance(comparison, dict):
        return False
    record = comparison.get(key)
    if not isinstance(record, dict) or set(record) != {
        "maximum_disagreement", "observable_linf", "sector_weight_linf"
    }:
        return False
    if not all(finite(record.get(field)) and float(record[field]) >= 0.0
               for field in record):
        return False
    reconstructed = max(float(record["observable_linf"]),
                        float(record["sector_weight_linf"]))
    return (
        abs(float(record["maximum_disagreement"]) - reconstructed) <= 1.0e-15
        and all(float(record[field]) <= TOLERANCE for field in record)
    )


def shape(prefix: int, q: int) -> tuple[int, int]:
    return math.comb(prefix, q), math.comb(2 * LENGTH, q)


def target_terminal_map(history: dict[str, object]) -> dict[int, dict[str, object]]:
    shards = history.get("terminal_shards")
    demand(isinstance(shards, list) and len(shards) == LENGTH,
           "target: terminal shard census")
    demand(all(isinstance(row, dict) and type(row.get("q")) is int for row in shards),
           "target: integer terminal q census")
    result = {row["q"]: row for row in shards}
    demand(set(result) == set(range(LENGTH)), "target: terminal q census")
    return result


def hostile_terminal_map(history: dict[str, object]) -> dict[int, dict[str, object]]:
    shards = history.get("terminal_shards")
    demand(isinstance(shards, list) and len(shards) == LENGTH,
           "hostile: terminal shard census")
    demand(all(isinstance(row, dict) and type(row.get("q")) is int for row in shards),
           "hostile: integer terminal q census")
    result = {row["q"]: row for row in shards}
    demand(set(result) == set(range(LENGTH)), "hostile: terminal q census")
    return result


def resolve_target_shard(root: Path, record: dict[str, object], q: int) -> Path:
    path = Path(str(record.get("path"))).resolve()
    demand(path.is_relative_to(root.resolve()) and path.is_file(),
           f"target q{q}: shard missing or outside pinned root")
    demand(path == (root / f"prefix_11/q_{q:02d}.npy").resolve(),
           f"target q{q}: canonical shard path")
    expected_shape = shape(LENGTH - 1, q)
    demand(record.get("shape") == list(expected_shape), f"target q{q}: shape record")
    demand(record.get("bytes") == path.stat().st_size, f"target q{q}: byte record")
    demand(record.get("sha256") == digest(path), f"target q{q}: shard hash")
    return path


def resolve_hostile_shard(root: Path, record: dict[str, object], q: int) -> Path:
    relative = Path(str(record.get("path")))
    demand(not relative.is_absolute() and ".." not in relative.parts,
           f"hostile q{q}: unsafe shard path")
    demand(relative == Path(f"prefix_11/q_{q:02d}.c128"),
           f"hostile q{q}: canonical shard path")
    path = (root / relative).resolve()
    demand(path.is_relative_to(root.resolve()) and path.is_file(),
           f"hostile q{q}: shard missing")
    expected_shape = shape(LENGTH - 1, q)
    demand(record.get("shape") == list(expected_shape), f"hostile q{q}: shape record")
    demand(record.get("logical_bytes") == 16 * math.prod(expected_shape),
           f"hostile q{q}: logical-byte record")
    demand(path.stat().st_size == 16 * math.prod(expected_shape),
           f"hostile q{q}: physical-byte census")
    return path


def lexicographic_combination_rank(width: int, weight: int,
                                   subset: tuple[int, ...]) -> int:
    demand(len(subset) == weight and tuple(sorted(subset)) == subset,
           "combination rank input")
    return math.comb(width, weight) - 1 - sum(
        math.comb(width - 1 - value, weight - index)
        for index, value in enumerate(subset)
    )


def ascending_to_hostile_permutation(width: int, weight: int) -> np.ndarray:
    count = math.comb(width, weight)
    mapping = np.empty(count, dtype=np.int32)
    for target_rank, subset in enumerate(itertools.combinations(range(width), weight)):
        reverse_positions = tuple(width - 1 - bit for bit in reversed(subset))
        mapping[target_rank] = lexicographic_combination_rank(
            width, weight, reverse_positions
        )
    demand(int(mapping.min(initial=0)) == 0 and int(mapping.max(initial=0)) == count - 1,
           "basis permutation range")
    demand(bool(np.array_equal(np.sort(mapping), np.arange(count, dtype=np.int32))),
           "basis permutation bijection")
    return mapping


def compare_shard(target_path: Path, hostile_path: Path,
                  expected_shape: tuple[int, int], q: int) -> tuple[float, str, str, str, str]:
    target_hash_before = digest(target_path)
    hostile_hash_before = digest(hostile_path)
    target = np.load(target_path, mmap_mode="r")
    demand(target.dtype == np.dtype("complex128") and target.shape == expected_shape,
           "target decoded shard format")
    hostile = np.memmap(hostile_path, dtype=np.complex128, mode="r", shape=expected_shape)
    row_permutation = ascending_to_hostile_permutation(LENGTH - 1, q)
    column_permutation = ascending_to_hostile_permutation(2 * LENGTH, q)
    row_permutation_hash = hashlib.sha256(row_permutation.tobytes()).hexdigest()
    column_permutation_hash = hashlib.sha256(column_permutation.tobytes()).hexdigest()
    maximum = 0.0
    columns = expected_shape[1]
    rows_per_chunk = max(1, (64 * 2**20) // max(16 * columns, 1))
    for lower in range(0, expected_shape[0], rows_per_chunk):
        upper = min(expected_shape[0], lower + rows_per_chunk)
        target_chunk = np.asarray(target[lower:upper])
        hostile_chunk = np.asarray(hostile[np.ix_(
            row_permutation[lower:upper], column_permutation
        )])
        demand(bool(np.all(np.isfinite(target_chunk.real)))
               and bool(np.all(np.isfinite(target_chunk.imag))),
               "target terminal shard contains non-finite amplitude")
        demand(bool(np.all(np.isfinite(hostile_chunk.real)))
               and bool(np.all(np.isfinite(hostile_chunk.imag))),
               "hostile terminal shard contains non-finite amplitude")
        difference = float(np.max(np.abs(target_chunk - hostile_chunk)))
        demand(math.isfinite(difference), "terminal amplitude difference non-finite")
        maximum = max(maximum, difference)
    target_hash_after = digest(target_path)
    hostile_hash_after = digest(hostile_path)
    demand(target_hash_before == target_hash_after, "target shard changed during audit")
    demand(hostile_hash_before == hostile_hash_after, "hostile shard changed during audit")
    return (maximum, target_hash_after, hostile_hash_after,
            row_permutation_hash, column_permutation_hash)


def write_new_atomic(path: Path, value: object) -> None:
    demand(path.resolve().is_relative_to(ROOT.resolve()), "output escapes repository")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--target-sha256", required=True)
    parser.add_argument("--hostile", type=Path, required=True)
    parser.add_argument("--hostile-sha256", required=True)
    parser.add_argument("--target-terminal-root", type=Path, required=True)
    parser.add_argument("--hostile-terminal-root", type=Path, required=True)
    parser.add_argument("--freeze-sha256", required=True)
    parser.add_argument("--blind-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    verify_freeze(args.freeze_sha256)
    demand(not args.output.exists(), "refuse to overwrite adjudication output")
    demand(not args.blind_output.exists(), "refuse to overwrite normalized blind output")
    demand(args.blind_output.resolve().is_relative_to(ROOT.resolve()),
           "normalized blind output escapes repository")
    target_root = args.target_terminal_root.resolve()
    hostile_root = args.hostile_terminal_root.resolve()
    custody = json.loads(EXECUTION_CUSTODY.read_text())
    demand(custody.get("schema") == "L12_ACTIVE_EXECUTION_CUSTODY_OBSERVATION_V001"
           and custody.get("status") == "OBSERVED_ACTIVE_BEFORE_HISTORY_OUTPUT"
           and custody.get("history_outputs_present_at_observation") is False,
           "active execution custody record")
    demand(custody.get("target", {}).get("implementation_sha256") ==
           EXPECTED_DEPENDENCIES[
               "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py"]
           and custody.get("hostile", {}).get("implementation_sha256") ==
           EXPECTED_DEPENDENCIES["independent_prefix_history_v003.py"],
           "active execution implementation custody")
    demand(target_root == Path(custody["target"]["terminal_root"]).resolve(),
           "target terminal root differs from observed execution")
    demand(hostile_root == Path(custody["hostile"]["terminal_root"]).resolve(),
           "hostile terminal root differs from observed execution")
    demand(target_root.is_dir(), "target terminal root missing")
    demand(hostile_root.is_dir(), "hostile terminal root missing")
    target = checked_result(args.target, args.target_sha256, "target")
    hostile = checked_result(args.hostile, args.hostile_sha256, "hostile")
    checks: list[tuple[bool, str]] = []
    checks.extend((
        (target.get("schema") == TARGET_SCHEMA, "target schema"),
        (hostile.get("schema") == HOSTILE_SCHEMA, "hostile schema"),
        (type(target.get("L")) is int and type(hostile.get("L")) is int
         and target["L"] == LENGTH and hostile["L"] == LENGTH, "L12 identity"),
        (type(target.get("events")) is int and type(hostile.get("events")) is int
         and target["events"] == LENGTH and hostile["events"] == LENGTH,
         "event identities"),
        (type(target.get("dimension")) is int
         and target["dimension"] == math.comb(3 * LENGTH, LENGTH),
         "target full dimension"),
        (type(hostile.get("full_dimension")) is int
         and hostile["full_dimension"] == math.comb(3 * LENGTH, LENGTH),
         "hostile full dimension"),
        (type(target.get("preterminal_dimension")) is int
         and target["preterminal_dimension"] == math.comb(3 * LENGTH - 1, LENGTH - 1),
         "target preterminal dimension"),
        (type(hostile.get("largest_materialized_dimension")) is int
         and hostile["largest_materialized_dimension"] == math.comb(3 * LENGTH - 1, LENGTH - 1),
         "hostile preterminal dimension"),
        (type(target.get("edges")) is int and target["edges"] == 3 * LENGTH,
         "target edge census"),
        (isinstance(hostile.get("edge_layout"), list)
         and len(hostile["edge_layout"]) == 3 * LENGTH
         and all(isinstance(edge, list) and len(edge) == 3 for edge in hostile["edge_layout"]),
         "hostile edge census"),
        (target.get("representation") == REPRESENTATION
         and hostile.get("representation") == REPRESENTATION,
         "representation identity"),
        (target.get("lineage_authority") == LINEAGE_AUTHORITY
         and hostile.get("lineage_authority") == LINEAGE_AUTHORITY,
         "lineage authority identity"),
        (target.get("implementation_sha256") == EXPECTED_DEPENDENCIES[
            "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py"],
         "target implementation custody"),
        (target.get("method_sha256") == EXPECTED_DEPENDENCIES[
            "../DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md"],
         "target method custody"),
        (hostile.get("implementation_sha256") == EXPECTED_DEPENDENCIES[
            "independent_prefix_history_v003.py"], "hostile implementation custody"),
        (hostile.get("method_sha256") == EXPECTED_DEPENDENCIES[
            "V003_L12_EXECUTABLE_METHOD.md"], "hostile method custody"),
        (hostile.get("l10_gate_sha256") == EXPECTED_DEPENDENCIES["L10_GATE_V002.json"],
         "hostile L10 gate custody"),
        (target.get("comparison", {}).get("resolved") is True, "target resolved"),
        (hostile.get("comparison", {}).get("resolved") is True, "hostile resolved"),
        (target.get("comparison", {}).get("classification") ==
         "RESOLVED_RELATIONAL_HISTORY_L", "target classification"),
        (hostile.get("comparison", {}).get("classification") ==
         "RESOLVED_PREFIX_HISTORY_CONTROL", "hostile classification"),
        (resource_pass(target, "target"), "target reconstructed resource pass"),
        (resource_pass(hostile, "hostile"), "hostile reconstructed resource pass"),
        (resolution_pass(target, "coarse_fine"), "target coarse/fine"),
        (resolution_pass(hostile, "rough_sharp"), "hostile rough/sharp"),
        (isinstance(hostile.get("terminal_support"), dict)
         and hostile["terminal_support"].get("child0_entries") ==
         math.comb(3 * LENGTH - 1, LENGTH - 1)
         and hostile["terminal_support"].get("child1_nonzero_admission_entries") ==
         math.comb(3 * LENGTH - 2, LENGTH - 1)
         and hostile["terminal_support"].get("full_terminal_array_allocated") is False,
         "hostile streamed H12 support"),
    ))
    target_rows = rows(target, "target")
    hostile_rows = rows(hostile, "hostile")
    maxima = {field: 0.0 for field in SCALARS}
    sector_maximum = 0.0
    previous_target_retained = 0.0
    previous_hostile_retained = 0.0
    for event, (left, right) in enumerate(zip(target_rows, hostile_rows), start=1):
        for role, row, previous in (
            ("target", left, previous_target_retained),
            ("hostile", right, previous_hostile_retained),
        ):
            for field in SCALARS:
                checks.append((finite(row.get(field)), f"{role} event {event} finite {field}"))
            weights = row.get("sector_weights")
            checks.append((
                isinstance(weights, list) and len(weights) == LENGTH + 1
                and all(finite(value) and float(value) >= -1.0e-12 for value in weights)
                and abs(sum(float(value) for value in weights) - 1.0) <= 1.0e-9,
                f"{role} event {event} sector census",
            ))
            checks.extend((
                (row.get("terminal_children_streamed") is (event == LENGTH),
                 f"{role} event {event} terminal flag"),
                (abs(float(row["reverse_support_probability"])) <= TOLERANCE,
                 f"{role} event {event} reverse null"),
                (0.0 <= float(row["allow_probability"]) <= 1.0 + TOLERANCE,
                 f"{role} event {event} allow range"),
                (0.0 <= float(row["blocked_probability"]) <= 1.0 + TOLERANCE,
                 f"{role} event {event} blocked range"),
                (0.0 <= float(row["W_n"]) <= 0.5 + TOLERANCE,
                 f"{role} event {event} write range"),
                (0.0 <= float(row["q_retained_after_transport"]) <= LENGTH + TOLERANCE,
                 f"{role} event {event} retained range"),
                (0.0 <= float(row["q_genesis_after"]) <= LENGTH + TOLERANCE,
                 f"{role} event {event} genesis range"),
                (float(row["connector_delta_l1"]) + TOLERANCE
                 >= abs(float(row["connector_delta_signed"])),
                 f"{role} event {event} connector L1 bound"),
                (abs(float(row["blocked_null_state_error"])) <= TOLERANCE,
                 f"{role} event {event} blocked null"),
                (abs(float(row["allow_probability"]) + float(row["blocked_probability"]) - 1.0)
                 <= TOLERANCE, f"{role} event {event} allow/blocked partition"),
                (abs(float(row["W_n"]) - 0.5 * float(row["allow_probability"]))
                 <= TOLERANCE, f"{role} event {event} authenticated write"),
                (abs(float(row["q_retained_after_transport"]) - previous - float(row["W_n"]))
                 <= TOLERANCE, f"{role} event {event} retained ledger"),
                (abs(float(row["q_genesis_after"]) + float(row["q_retained_after_transport"])
                     - LENGTH) <= TOLERANCE, f"{role} event {event} total ledger"),
                (abs(sum(q * float(weight) for q, weight in enumerate(weights))
                     - float(row["q_retained_after_transport"])) <= TOLERANCE,
                 f"{role} event {event} sector charge moment"),
                (abs(float(row["admission_total_content_residual"])) <= TOLERANCE,
                 f"{role} event {event} admission content residual"),
                (abs(float(row["admission_bandwidth_residual"])) <= TOLERANCE,
                 f"{role} event {event} bandwidth residual"),
                (abs(float(row["target_owner_residual"])) <= TOLERANCE,
                 f"{role} event {event} owner-once residual"),
                (abs(float(row["transport_node_residual_l1"])) <= TOLERANCE,
                 f"{role} event {event} node continuity"),
                (abs(float(row["transport_node_residual_linf"])) <= TOLERANCE,
                 f"{role} event {event} node continuity Linf"),
                (abs(float(row["transport_number_drift"])) <= TOLERANCE,
                 f"{role} event {event} transport number"),
                (abs(float(row["actual_norm_error"])) <= TOLERANCE,
                 f"{role} event {event} norm"),
                (abs(float(row["null_norm_error"])) <= TOLERANCE,
                 f"{role} event {event} null norm"),
            ))
            if role == "target":
                checks.extend((
                    (type(row.get("cursor_vertex")) is int
                     and row["cursor_vertex"] == event - 1,
                     f"target event {event} cursor"),
                    (abs(float(row.get("q_retained_before", math.inf)) - previous)
                     <= TOLERANCE, f"target event {event} retained-before"),
                    (abs(float(row.get("q_retained_after_admission", math.inf))
                         - previous - float(row["W_n"])) <= TOLERANCE,
                     f"target event {event} retained admission"),
                    (abs(float(row.get("q_genesis_before", math.inf)) + previous - LENGTH)
                     <= TOLERANCE, f"target event {event} genesis-before"),
                    (abs(float(row.get("expected_W_from_allow", math.inf))
                         - float(row["W_n"])) <= TOLERANCE,
                     f"target event {event} expected write"),
                    (finite(row.get("lineage_sealed_after"))
                     and abs(float(row["lineage_sealed_after"])
                             - float(row["q_retained_after_admission"])) <= TOLERANCE,
                     f"target event {event} sealed lineage"),
                    (finite(row.get("bandwidth_after"))
                     and abs(float(row["bandwidth_after"])
                             - float(row["q_genesis_after"])) <= TOLERANCE,
                     f"target event {event} bandwidth"),
                    (abs(float(row.get("transport_genesis_drift", math.inf))) <= TOLERANCE,
                     f"target event {event} transport genesis"),
                ))
            else:
                checks.extend((
                    (type(row.get("input_prefix")) is int
                     and row["input_prefix"] == event - 1,
                     f"hostile event {event} input prefix"),
                    (type(row.get("input_prefix_dimension")) is int
                     and row["input_prefix_dimension"] ==
                     math.comb(2 * LENGTH + event - 1, event - 1),
                     f"hostile event {event} input dimension"),
                    (type(row.get("logical_output_prefix_dimension")) is int
                     and row["logical_output_prefix_dimension"] ==
                     math.comb(2 * LENGTH + event, event),
                     f"hostile event {event} output dimension"),
                    (finite(row.get("null_transport_node_residual_l1"))
                     and abs(float(row["null_transport_node_residual_l1"])) <= TOLERANCE,
                     f"hostile event {event} null node continuity"),
                    (finite(row.get("null_transport_number_drift"))
                     and abs(float(row["null_transport_number_drift"])) <= TOLERANCE,
                     f"hostile event {event} null transport number"),
                ))
            solver_pass(row.get("actual_solver"), f"{role} event {event} actual",
                        role, event == LENGTH)
            solver_pass(row.get("null_solver"), f"{role} event {event} null",
                        role, event == LENGTH)
        previous_target_retained = float(left["q_retained_after_transport"])
        previous_hostile_retained = float(right["q_retained_after_transport"])
        for field in SCALARS:
            maxima[field] = max(maxima[field], abs(float(left[field]) - float(right[field])))
        sector_maximum = max(sector_maximum, max(
            abs(float(a) - float(b))
            for a, b in zip(left["sector_weights"], right["sector_weights"])
        ))
    checks.append((all(value <= TOLERANCE for value in maxima.values()),
                   "target/hostile observable agreement"))
    checks.append((sector_maximum <= TOLERANCE, "target/hostile sector agreement"))
    target_shards = target_terminal_map(target)
    hostile_shards = hostile_terminal_map(hostile)
    shard_records = []
    amplitude_maximum = 0.0
    for q in range(LENGTH):
        target_path = resolve_target_shard(target_root, target_shards[q], q)
        hostile_path = resolve_hostile_shard(hostile_root, hostile_shards[q], q)
        (maximum, target_hash, hostile_hash,
         row_permutation_hash, column_permutation_hash) = compare_shard(
            target_path, hostile_path, shape(LENGTH - 1, q), q
        )
        amplitude_maximum = max(amplitude_maximum, maximum)
        checks.append((maximum <= TOLERANCE, f"terminal amplitude agreement q{q}"))
        shard_records.append({
            "q": q,
            "shape": list(shape(LENGTH - 1, q)),
            "target_sha256": target_hash,
            "hostile_sha256": hostile_hash,
            "target_to_hostile_lineage_permutation_sha256": row_permutation_hash,
            "target_to_hostile_carrier_permutation_sha256": column_permutation_hash,
            "amplitude_linf": maximum,
        })
    failures = [label for passed, label in checks if not passed]
    manifest_fields = (
        "W_n", "allow_probability", "blocked_probability",
        "reverse_support_probability", "connector_delta_l1",
        "connector_delta_signed", "q_retained_after_transport", "q_genesis_after",
    )
    manifest_observable_maximum = max(maxima[field] for field in manifest_fields)
    blind_hash = None
    if not failures:
        demand("dimension" not in hostile and "manifest_adapter" not in hostile,
               "schema adapter is not add-only")
        normalized = dict(hostile)
        normalized["dimension"] = hostile["full_dimension"]
        normalized["manifest_adapter"] = {
            "classification": "SCHEMA_ONLY_FULL_DIMENSION_ALIAS",
            "source_history_sha256": args.hostile_sha256,
            "adjudicator_sha256": digest(Path(__file__)),
            "freeze_sha256": args.freeze_sha256,
            "fields_added": ["dimension", "manifest_adapter"],
            "physical_fields_changed": False,
        }
        write_new_atomic(args.blind_output, normalized)
        blind_hash = digest(args.blind_output)
    output = {
        "schema": "AUDIT_R_L12_COMPLETE_PREFIX_HISTORY_GATE_V001",
        "classification": (
            "PASS_EXACT_L12_COMPLETE_PREFIX_HISTORY_GATE_V001"
            if not failures else "FAIL_EXACT_L12_COMPLETE_PREFIX_HISTORY_GATE_V001"
        ),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "tolerance": TOLERANCE,
        "target_history_sha256": args.target_sha256,
        "hostile_history_sha256": args.hostile_sha256,
        "blind_history_sha256": blind_hash,
        "maximum_target_hostile_history_observable_difference": max(maxima.values()),
        "maximum_target_blind_manifest_observable_difference": manifest_observable_maximum,
        "maximum_target_hostile_sector_weight_difference": sector_maximum,
        "maximum_target_hostile_terminal_amplitude_difference": amplitude_maximum,
        "observable_linf_by_field": maxima,
        "terminal_shards": shard_records,
        "claim_boundary": (
            "FINITE_EXACT_L12_HISTORY_AND_COMPLETE_H11_STATE_AGREEMENT_ONLY__"
            "NO_SPECTRAL_SCALING_CRITICALITY_CONTINUUM_EMERGENCE_OR_GRAVITY"
        ),
    }
    try:
        write_new_atomic(args.output, output)
    except Exception:
        if blind_hash is not None and args.blind_output.is_file():
            args.blind_output.unlink()
        raise
    print(output["classification"])
    print(f"checks={output['checks_passed']}/{output['checks_total']}")
    print(f"observable={max(maxima.values()):.17g} sector={sector_maximum:.17g} "
          f"state={amplitude_maximum:.17g}")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
