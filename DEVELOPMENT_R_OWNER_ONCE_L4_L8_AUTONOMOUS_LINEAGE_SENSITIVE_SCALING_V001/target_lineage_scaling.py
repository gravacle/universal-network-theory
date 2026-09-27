#!/usr/bin/env python3
"""Authenticated target route for finite L4--L8 lineage-response scaling.

Only L4 execution is authorized in V001.  L6 and L8 inputs can be authenticated,
but every numerical entry point rejects those lengths until the frozen L4,
restart, independent-audit, and resource gates have passed.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import resource
import subprocess
import sys
import time
import warnings
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterable, Mapping

import numpy as np


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent.resolve()
SUPPORTED_LENGTHS = (4, 6, 8)
AUTHORIZED_EXECUTION_LENGTHS = (4,)
EXPECTED_HEAD = "f5973628fa25c8cc0e2812142e6d8516d0b5d28d"
HISTORICAL_ROOT = "/Users/brianmulconrey/PerInfo/where-atoms-come-from/audited-386ee2c/"

ENGINE_RELATIVE = Path("DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py")
RUNTIME_RELATIVE = Path("DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/resumable_runtime.py")
DURABLE_RELATIVE = Path("DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/durable_evidence.py")
DENSE_RESULT_RELATIVE = Path(
    "DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/"
    "PHYSICAL_OUTPUTS/L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_RESULT_V001.json"
)

DEPENDENCY_HASHES = {
    "MIGRATION_CONTEXT_AUDIT_2026-09-27_V001/INVENTORY.json":
        "68d69d9596d4f135bf7fe5700594c773d68d86cba0c5b91f52abfcbb1786a419",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py":
        "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v002.py":
        "71458cd4b958d5b38cb24409ed769e790d9a83e1da8ac71fd2d3098fdb779694",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history.py":
        "8bc59c363c638edd35db12fccb953a2590464b8f422f8a71f5ed4f3972951515",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md":
        "864113577059c5214923d4d1709e0d2a4483131f816b42bc43f7fc14a72b19ef",
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json":
        "629ab8bc8e3c2a70c8e79a788ddeb6bafd3503491cef3b331bcc97a1555c2359",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py":
        "2cce210fff77ceb4ea91bce6fdd50ea75e1c7c5027471eaf4264ae794cc03b16",
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py":
        "24ea3626fda443dd4ae5076c7766e1aaca77ff5ce9f22c05bae96943fc627d55",
    "DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/resumable_runtime.py":
        "3bd65f288a7023b20c9ed70929aa8ce0c84a9dae43f0c95456ed9738d47e3a81",
    "DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/durable_evidence.py":
        "c83d305463903e31a0b1868be9497ba095951529e5628419b94193b03582b634",
    str(DENSE_RESULT_RELATIVE):
        "ad134b528761c4e865df35678097dab4fb56297c5237a910ca482bac77c0c0dc",
}

HISTORY_HASHES = {
    4: "754cc0876a31a0b6ff84aa44cfb3043e8d68964c9b29076ea2e565fd07e1f87c",
    6: "39deaf48167f3f684e5e44d11f85da55ae297c4b91d4116cda7f04060234a6d6",
    8: "ff55ddd70c3f5e3664e1a61384f211a86e9fcc5bcec2d7e02251d387bd17c786",
}

BASE_TAU = 1.0e-10
DENSE_REPRODUCTION_TOLERANCE = 5.0e-12
CONTROL_TOLERANCE = 1.0e-11
NORMALIZED_SLOP = 1.0e-12


class ScalingError(RuntimeError):
    """Fail-closed authentication or numerical error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ScalingError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ScalingError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ScalingError(f"non-finite JSON constant: {value}")


def load_json(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(
            stream,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def git(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def authenticate_dependencies() -> dict[str, str]:
    require(git("rev-parse", "HEAD") == EXPECTED_HEAD, "unexpected Git HEAD")
    observed: dict[str, str] = {}
    for relative, expected in DEPENDENCY_HASHES.items():
        path = ROOT / relative
        require(path.is_file(), f"missing dependency: {relative}")
        actual = sha256_file(path)
        require(actual == expected, f"dependency hash mismatch: {relative}")
        observed[relative] = actual
    return observed


def history_relative(length: int) -> Path:
    return Path(
        f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L{length}.json"
    )


def shard_relative(length: int, q: int) -> Path:
    return Path(
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/"
        f"L{length}/sharp/prefix_{length - 1:02d}/q_{q:02d}.npy"
    )


def _reject_symlink_route(path: Path) -> None:
    cursor = path
    while True:
        require(not cursor.is_symlink(), f"symlink prohibited in shard route: {cursor}")
        if cursor == ROOT:
            return
        require(cursor != cursor.parent, f"shard route escaped root: {path}")
        cursor = cursor.parent


def authenticate_history(length: int) -> dict[str, Any]:
    require(length in SUPPORTED_LENGTHS, f"unsupported input length: {length}")
    relative = history_relative(length)
    path = ROOT / relative
    require(path.is_file(), f"missing history: {relative}")
    require(sha256_file(path) == HISTORY_HASHES[length], f"history hash mismatch: L{length}")
    history = load_json(path)
    require(history.get("schema") == "TARGET_CACHED_PREFIX_HISTORY_V012", "history schema")
    require(history.get("L") == length, "history length")
    require(
        history.get("target_v004_sha256") == DEPENDENCY_HASHES[str(ENGINE_RELATIVE)],
        "history target-engine binding",
    )
    records = history.get("terminal_shards")
    require(isinstance(records, list) and len(records) == length, "terminal-shard census")
    result: list[dict[str, Any]] = []
    seen: set[int] = set()
    for record in records:
        require(
            isinstance(record, dict)
            and set(record) == {"bytes", "path", "q", "sha256", "shape"},
            "terminal-shard record schema",
        )
        q = record["q"]
        require(isinstance(q, int) and 0 <= q < length and q not in seen, "terminal-shard q")
        seen.add(q)
        relative_shard = shard_relative(length, q)
        historical = record["path"]
        require(
            historical == HISTORICAL_ROOT + relative_shard.as_posix(),
            f"historical shard path mismatch: L{length} q{q}",
        )
        candidate = ROOT / relative_shard
        _reject_symlink_route(candidate)
        resolved = candidate.resolve(strict=True)
        require(resolved.is_relative_to(ROOT), "resolved shard escaped repository")
        require(resolved.is_file(), f"missing relocated shard: {relative_shard}")
        expected_shape = [math.comb(length - 1, q), math.comb(2 * length, q)]
        require(record["shape"] == expected_shape, f"sealed shard shape: L{length} q{q}")
        require(resolved.stat().st_size == record["bytes"], f"shard byte count: L{length} q{q}")
        require(sha256_file(resolved) == record["sha256"], f"shard hash: L{length} q{q}")
        array = np.load(resolved, mmap_mode="r", allow_pickle=False)
        require(list(array.shape) == expected_shape, f"runtime shard shape: L{length} q{q}")
        require(array.dtype == np.dtype("<c16"), f"runtime shard dtype: L{length} q{q}")
        require(bool(array.flags.c_contiguous), f"runtime shard order: L{length} q{q}")
        del array
        result.append(
            {
                **record,
                "historical_path": historical,
                "runtime_relative_path": relative_shard.as_posix(),
                "runtime_path": str(resolved),
            }
        )
    require(seen == set(range(length)), "terminal-shard q coverage")
    return {
        "history": history,
        "history_relative_path": relative.as_posix(),
        "history_sha256": HISTORY_HASHES[length],
        "shards": sorted(result, key=lambda item: item["q"]),
    }


def authenticate_all_inputs() -> dict[str, Any]:
    dependencies = authenticate_dependencies()
    histories = {str(length): authenticate_history(length) for length in SUPPORTED_LENGTHS}
    return {
        "git_head": EXPECTED_HEAD,
        "dependencies": dependencies,
        "histories": {
            length: {
                "history_relative_path": record["history_relative_path"],
                "history_sha256": record["history_sha256"],
                "shards": [
                    {
                        key: shard[key]
                        for key in (
                            "q",
                            "shape",
                            "bytes",
                            "sha256",
                            "historical_path",
                            "runtime_relative_path",
                        )
                    }
                    for shard in record["shards"]
                ],
            }
            for length, record in histories.items()
        },
    }


def _load_module(path: Path, name: str) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def load_target_engine() -> ModuleType:
    authenticate_dependencies()
    engine_dir = (ROOT / ENGINE_RELATIVE).parent
    if str(engine_dir) not in sys.path:
        sys.path.insert(0, str(engine_dir))
    return _load_module(ROOT / ENGINE_RELATIVE, "unt_target_prefix_v004_scaling")


def load_resume_runtime() -> tuple[ModuleType, ModuleType]:
    authenticate_dependencies()
    runtime_dir = (ROOT / RUNTIME_RELATIVE).parent
    if str(runtime_dir) not in sys.path:
        sys.path.insert(0, str(runtime_dir))
    durable = _load_module(ROOT / DURABLE_RELATIVE, "durable_evidence")
    # ProcessPool uses spawn on macOS.  The class's defining module therefore
    # must retain its importable canonical name for child-process unpickling.
    runtime = _load_module(ROOT / RUNTIME_RELATIVE, "resumable_runtime")
    return durable, runtime


def validate_execution_length(length: int) -> None:
    require(length in SUPPORTED_LENGTHS, f"unsupported length: {length}")
    require(
        length in AUTHORIZED_EXECUTION_LENGTHS,
        f"L{length} execution locked pending dense-L4, restart, independent-audit, and benchmark gates",
    )


def fixed_words(width: int, weight: int) -> np.ndarray:
    require(0 <= weight <= width, "invalid fixed-weight request")
    result = np.empty(math.comb(width, weight), dtype=np.uint32)
    for index, positions in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        result[index] = word
    return result


def _lookup(words: np.ndarray) -> dict[int, int]:
    return {int(word): index for index, word in enumerate(words)}


def _load_shard(record: Mapping[str, Any]) -> np.ndarray:
    path = Path(str(record["runtime_path"]))
    before = sha256_file(path)
    require(before == record["sha256"], f"pre-read shard hash: {path}")
    value = np.array(np.load(path, mmap_mode="r", allow_pickle=False), copy=True)
    after = sha256_file(path)
    require(after == before, f"post-read shard hash: {path}")
    require(np.all(np.isfinite(value)), f"nonfinite shard: {path}")
    return value


def reconstruct_terminal_sector(
    length: int,
    q_out: int,
    engine: ModuleType,
    authenticated: Mapping[str, Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    """Reconstruct one post-final-transport terminal amplitude matrix."""

    validate_execution_length(length)
    require(0 <= q_out <= length, "terminal q range")
    records = {record["q"]: record for record in authenticated["shards"]}
    lineage_out = fixed_words(length, q_out)
    carrier_out = fixed_words(2 * length, q_out)
    lineage_lookup = _lookup(lineage_out)
    carrier_lookup = _lookup(carrier_out)
    admitted = np.zeros((len(lineage_out), len(carrier_out)), dtype=np.complex128)
    event = length - 1
    cosine = math.cos(float(engine.sealed.PHI))
    sine = math.sin(float(engine.sealed.PHI))

    if q_out < length:
        old = _load_shard(records[q_out])
        lineage_before = fixed_words(length - 1, q_out)
        carrier_before = fixed_words(2 * length, q_out)
        blank = ((carrier_before >> event) & 1) == 0
        for source_row, word in enumerate(lineage_before):
            target_row = lineage_lookup[int(word)]
            admitted[target_row] = old[source_row]
            admitted[target_row, blank] *= cosine

    if q_out > 0:
        source_q = q_out - 1
        old = _load_shard(records[source_q])
        lineage_before = fixed_words(length - 1, source_q)
        carrier_before = fixed_words(2 * length, source_q)
        blank_columns = np.flatnonzero(((carrier_before >> event) & 1) == 0)
        target_columns = np.fromiter(
            (
                carrier_lookup[int(carrier_before[column]) | (1 << event)]
                for column in blank_columns
            ),
            dtype=np.int32,
            count=len(blank_columns),
        )
        for source_row, word in enumerate(lineage_before):
            target_row = lineage_lookup[int(word) | (1 << event)]
            admitted[target_row, target_columns] = (
                -1.0j * sine * old[source_row, blank_columns]
            )

    require(np.all(np.isfinite(admitted)), "nonfinite admitted terminal sector")
    engine_words = engine.sealed.fixed_words(2 * length, q_out)
    require(np.array_equal(engine_words, carrier_out), "carrier basis ordering mismatch")
    sector = engine.sealed.Sector(length, q_out, engine.sealed.graph(length))
    evolved, _current, solver = engine.v3.propagate_dispatch(
        length, sector, admitted, engine.sealed.FINE
    )
    require(bool(solver.get("converged")), f"terminal solver failed: L{length} q{q_out}")
    require(np.all(np.isfinite(evolved)), "nonfinite terminal sector")
    return evolved, {
        "q": q_out,
        "shape": list(evolved.shape),
        "norm": float(np.vdot(evolved, evolved).real),
        "solver": _clean_solver_record(solver),
    }


def _clean_solver_record(record: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in record.items():
        if isinstance(value, (np.integer, int)):
            result[key] = int(value)
        elif isinstance(value, (np.floating, float)):
            number = float(value)
            result[key] = number if math.isfinite(number) else None
        elif isinstance(value, (np.bool_, bool)):
            result[key] = bool(value)
        else:
            result[key] = value
    return result


def actual_admission_factors(
    length: int, event: int, q: int, amplitude: np.ndarray
) -> dict[int, np.ndarray]:
    """Carrier factors after the joint reversible admission of one pure q block."""

    lineage_words = fixed_words(length, q)
    carrier_words = fixed_words(2 * length, q)
    require(amplitude.shape == (len(lineage_words), len(carrier_words)), "amplitude shape")
    lineage_bit = ((lineage_words >> event) & 1).astype(np.uint8)
    carrier_bit = ((carrier_words >> event) & 1).astype(np.uint8)
    cosine = math.cos(math.pi / 4.0)
    sine = math.sin(math.pi / 4.0)
    result: dict[int, np.ndarray] = {}

    stay = amplitude.copy()
    stay[lineage_bit[:, None] == carrier_bit[None, :]] *= cosine
    result[q] = stay.T

    if q < length:
        out_lineage = fixed_words(length, q + 1)
        out_carrier = fixed_words(2 * length, q + 1)
        lineage_lookup = _lookup(out_lineage)
        carrier_lookup = _lookup(out_carrier)
        source_rows = np.flatnonzero(lineage_bit == 0)
        source_columns = np.flatnonzero(carrier_bit == 0)
        target_rows = np.fromiter(
            (lineage_lookup[int(lineage_words[row]) | (1 << event)] for row in source_rows),
            dtype=np.int32,
            count=len(source_rows),
        )
        target_columns = np.fromiter(
            (carrier_lookup[int(carrier_words[column]) | (1 << event)] for column in source_columns),
            dtype=np.int32,
            count=len(source_columns),
        )
        child = np.zeros((len(out_lineage), len(out_carrier)), dtype=np.complex128)
        child[np.ix_(target_rows, target_columns)] = (
            -1.0j * sine * amplitude[np.ix_(source_rows, source_columns)]
        )
        result[q + 1] = child.T

    if q > 0:
        out_lineage = fixed_words(length, q - 1)
        out_carrier = fixed_words(2 * length, q - 1)
        lineage_lookup = _lookup(out_lineage)
        carrier_lookup = _lookup(out_carrier)
        source_rows = np.flatnonzero(lineage_bit == 1)
        source_columns = np.flatnonzero(carrier_bit == 1)
        target_rows = np.fromiter(
            (lineage_lookup[int(lineage_words[row]) & ~(1 << event)] for row in source_rows),
            dtype=np.int32,
            count=len(source_rows),
        )
        target_columns = np.fromiter(
            (carrier_lookup[int(carrier_words[column]) & ~(1 << event)] for column in source_columns),
            dtype=np.int32,
            count=len(source_columns),
        )
        child = np.zeros((len(out_lineage), len(out_carrier)), dtype=np.complex128)
        child[np.ix_(target_rows, target_columns)] = (
            -1.0j * sine * amplitude[np.ix_(source_rows, source_columns)]
        )
        result[q - 1] = child.T
    return result


def product_admission_factors(
    length: int, event: int, q: int, amplitude: np.ndarray
) -> dict[int, list[np.ndarray]]:
    """Exact channel factors for the same-q product comparator."""

    lineage_words = fixed_words(length, q)
    carrier_words = fixed_words(2 * length, q)
    require(amplitude.shape == (len(lineage_words), len(carrier_words)), "amplitude shape")
    sector_weight = float(np.vdot(amplitude, amplitude).real)
    require(sector_weight > 0.0, "zero-weight sector supplied to product comparator")
    lineage_bit = ((lineage_words >> event) & 1).astype(np.uint8)
    carrier_bit = ((carrier_words >> event) & 1).astype(np.uint8)
    probabilities = [
        float(np.sum(np.abs(amplitude[lineage_bit == value]) ** 2)) / sector_weight
        for value in (0, 1)
    ]
    require(abs(sum(probabilities) - 1.0) <= CONTROL_TOLERANCE, "lineage-bit probabilities")
    carrier_factor = amplitude.T
    cosine = math.cos(math.pi / 4.0)
    sine = math.sin(math.pi / 4.0)
    result: dict[int, list[np.ndarray]] = {}

    for lineage_value, probability in enumerate(probabilities):
        if probability <= 1.0e-30:
            continue
        scale = math.sqrt(probability)
        stay = carrier_factor.copy()
        stay[carrier_bit == lineage_value] *= cosine
        result.setdefault(q, []).append(scale * stay)

        if lineage_value == 0 and q < length:
            out_carrier = fixed_words(2 * length, q + 1)
            carrier_lookup = _lookup(out_carrier)
            source_rows = np.flatnonzero(carrier_bit == 0)
            target_rows = np.fromiter(
                (
                    carrier_lookup[int(carrier_words[row]) | (1 << event)]
                    for row in source_rows
                ),
                dtype=np.int32,
                count=len(source_rows),
            )
            child = np.zeros((len(out_carrier), carrier_factor.shape[1]), dtype=np.complex128)
            child[target_rows] = -1.0j * sine * scale * carrier_factor[source_rows]
            result.setdefault(q + 1, []).append(child)

        if lineage_value == 1 and q > 0:
            out_carrier = fixed_words(2 * length, q - 1)
            carrier_lookup = _lookup(out_carrier)
            source_rows = np.flatnonzero(carrier_bit == 1)
            target_rows = np.fromiter(
                (
                    carrier_lookup[int(carrier_words[row]) & ~(1 << event)]
                    for row in source_rows
                ),
                dtype=np.int32,
                count=len(source_rows),
            )
            child = np.zeros((len(out_carrier), carrier_factor.shape[1]), dtype=np.complex128)
            child[target_rows] = -1.0j * sine * scale * carrier_factor[source_rows]
            result.setdefault(q - 1, []).append(child)
    return result


def signed_low_rank_metrics(
    actual: np.ndarray, product: np.ndarray
) -> dict[str, Any]:
    require(actual.ndim == product.ndim == 2, "factor rank")
    require(actual.shape[0] == product.shape[0], "factor carrier dimension")
    require(actual.shape[1] and product.shape[1], "empty signed factor")
    require(np.all(np.isfinite(actual)) and np.all(np.isfinite(product)), "nonfinite factor")
    combined = np.concatenate((actual, product), axis=1)
    signs = np.concatenate((np.ones(actual.shape[1]), -np.ones(product.shape[1])))
    q_factor, r_factor = np.linalg.qr(combined, mode="reduced")
    reduced_raw = (r_factor * signs[None, :]) @ r_factor.conj().T
    hermiticity = float(np.max(np.abs(reduced_raw - reduced_raw.conj().T)))
    reduced = (reduced_raw + reduced_raw.conj().T) / 2.0
    eigenvalues = np.linalg.eigvalsh(reduced)
    diagonal_actual = np.sum(actual.real * actual.real + actual.imag * actual.imag, axis=1)
    diagonal_product = np.sum(product.real * product.real + product.imag * product.imag, axis=1)
    qr_reconstruction = float(np.max(np.abs(combined - q_factor @ r_factor)))
    trace_actual = float(np.sum(diagonal_actual))
    trace_product = float(np.sum(diagonal_product))
    return {
        "carrier_trace_distance": 0.5 * float(np.sum(np.abs(eigenvalues))),
        "carrier_configuration_tv": 0.5 * float(
            np.sum(np.abs(diagonal_actual - diagonal_product))
        ),
        "trace_actual": trace_actual,
        "trace_product": trace_product,
        "diagonal_difference": diagonal_actual - diagonal_product,
        "controls": {
            "factor_columns_actual": int(actual.shape[1]),
            "factor_columns_product": int(product.shape[1]),
            "reduced_dimension": int(reduced.shape[0]),
            "qr_reconstruction": qr_reconstruction,
            "reduced_hermiticity": hermiticity,
            "eigenvalue_sum_trace_residual": abs(
                float(np.sum(eigenvalues)) - (trace_actual - trace_product)
            ),
        },
    }


def transport_factor(
    length: int, q: int, factor: np.ndarray, engine: ModuleType
) -> tuple[np.ndarray, dict[str, Any]]:
    sector = engine.sealed.Sector(length, q, engine.sealed.graph(length))
    evolved, _current, solver = engine.v3.propagate_dispatch(
        length, sector, factor.T, engine.sealed.FINE
    )
    require(bool(solver.get("converged")), f"factor transport did not converge: L{length} q{q}")
    require(np.all(np.isfinite(evolved)), "nonfinite transported factor")
    return evolved.T, _clean_solver_record(solver)


def _sector_observables(
    length: int, q_out: int, actual: np.ndarray, product: np.ndarray
) -> dict[str, Any]:
    metrics = signed_low_rank_metrics(actual, product)
    diagonal_difference = metrics.pop("diagonal_difference")
    words = fixed_words(2 * length, q_out)
    delta_n = [
        float(np.sum(diagonal_difference[((words >> site) & 1) == 1]))
        for site in range(2 * length)
    ]
    metrics["delta_n"] = delta_n
    return metrics


def response_sector(
    length: int,
    event: int,
    q_out: int,
    engine: ModuleType,
    authenticated: Mapping[str, Any],
) -> dict[str, Any]:
    validate_execution_length(length)
    require(0 <= event < length, "event range")
    require(0 <= q_out <= length, "output q range")
    actual_parts: list[np.ndarray] = []
    product_parts: list[np.ndarray] = []
    terminal_controls = []
    for q_in in range(max(0, q_out - 1), min(length, q_out + 1) + 1):
        amplitude, terminal_control = reconstruct_terminal_sector(
            length, q_in, engine, authenticated
        )
        terminal_controls.append(terminal_control)
        actual = actual_admission_factors(length, event, q_in, amplitude)
        if q_out in actual:
            actual_parts.append(actual[q_out])
        product = product_admission_factors(length, event, q_in, amplitude)
        product_parts.extend(product.get(q_out, []))
    require(actual_parts and product_parts, "missing response factors")
    actual_factor = np.concatenate(actual_parts, axis=1)
    product_factor = np.concatenate(product_parts, axis=1)
    after_admission = _sector_observables(
        length, q_out, actual_factor, product_factor
    )
    actual_terminal, actual_solver = transport_factor(length, q_out, actual_factor, engine)
    product_terminal, product_solver = transport_factor(length, q_out, product_factor, engine)
    after_transport = _sector_observables(
        length, q_out, actual_terminal, product_terminal
    )
    return {
        "schema": "L4_L8_TARGET_RESPONSE_SECTOR_V001",
        "L": length,
        "event": event,
        "q_out": q_out,
        "after_admission": after_admission,
        "after_transport": after_transport,
        "controls": {
            "trace_distance_transport_invariance": abs(
                float(after_admission["carrier_trace_distance"])
                - float(after_transport["carrier_trace_distance"])
            ),
            "terminal_reconstruction": terminal_controls,
            "actual_transport_solver": actual_solver,
            "product_transport_solver": product_solver,
        },
    }


def _rss_bytes(which: int) -> int:
    value = int(resource.getrusage(which).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


def sector_kernel(
    task_payload: Mapping[str, Any], context: Mapping[str, Any]
) -> dict[str, Any]:
    """Resumable-runtime entry point.  It is deliberately hard-locked to L4."""

    started = time.perf_counter()
    length = int(task_payload["L"])
    event = int(task_payload["event"])
    q_out = int(task_payload["q_out"])
    validate_execution_length(length)
    require(length == 4, "V001 sector kernel is L4-only")
    old_settings = np.seterr(all="raise")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            authenticated = authenticate_history(length)
            engine = load_target_engine()
            result = response_sector(length, event, q_out, engine, authenticated)
    finally:
        np.seterr(**old_settings)
    result["task_binding"] = {
        "task_id": context["task_id"],
        "task_sha256": context["task_sha256"],
        "history_sha256": HISTORY_HASHES[length],
        "engine_sha256": DEPENDENCY_HASHES[str(ENGINE_RELATIVE)],
        "kernel_sha256": sha256_file(Path(__file__)),
    }
    result["resource"] = {
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": _rss_bytes(resource.RUSAGE_SELF),
    }
    result["artifacts"] = []
    return result


def aggregate_stage(
    length: int, sector_results: Iterable[Mapping[str, Any]], stage: str
) -> dict[str, Any]:
    ordered = sorted(sector_results, key=lambda row: int(row["q_out"]))
    require([int(row["q_out"]) for row in ordered] == list(range(length + 1)), "q result census")
    rows = [row[stage] for row in ordered]
    delta_n = np.sum(np.array([row["delta_n"] for row in rows], dtype=float), axis=0)
    trace_actual = np.array([float(row["trace_actual"]) for row in rows])
    trace_product = np.array([float(row["trace_product"]) for row in rows])
    return {
        "carrier_trace_distance": float(
            sum(float(row["carrier_trace_distance"]) for row in rows)
        ),
        "carrier_configuration_tv": float(
            sum(float(row["carrier_configuration_tv"]) for row in rows)
        ),
        "carrier_number_sector_tv": 0.5 * float(
            np.sum(np.abs(trace_actual - trace_product))
        ),
        "occupation_rms": float(np.sqrt(np.mean(delta_n * delta_n))),
        "delta_n": delta_n.tolist(),
        "delta_n_0": float(delta_n[0]),
        "sector_weights_actual": trace_actual.tolist(),
        "sector_weights_product": trace_product.tolist(),
    }


def registered_values(record: Mapping[str, Any]) -> list[float]:
    values: list[float] = []
    for stage in ("after_admission", "after_transport"):
        row = record[stage]
        values.extend(
            float(row[key])
            for key in (
                "carrier_trace_distance",
                "carrier_configuration_tv",
                "carrier_number_sector_tv",
                "occupation_rms",
                "delta_n_0",
            )
        )
        values.extend(float(value) for value in row["delta_n"])
    return values


def _directory_bytes(root: Path) -> int:
    if not root.exists():
        return 0
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def _all_controls(sector_results: list[Mapping[str, Any]]) -> dict[str, float]:
    qr = []
    hermiticity = []
    eigen_trace = []
    transport = []
    solver_residual = []
    for sector in sector_results:
        transport.append(float(sector["controls"]["trace_distance_transport_invariance"]))
        for stage in ("after_admission", "after_transport"):
            controls = sector[stage]["controls"]
            qr.append(float(controls["qr_reconstruction"]))
            hermiticity.append(float(controls["reduced_hermiticity"]))
            eigen_trace.append(float(controls["eigenvalue_sum_trace_residual"]))
        for label in ("actual_transport_solver", "product_transport_solver"):
            value = sector["controls"][label].get("residual_indicator")
            if value is not None:
                solver_residual.append(float(value))
        for terminal in sector["controls"]["terminal_reconstruction"]:
            value = terminal["solver"].get("residual_indicator")
            if value is not None:
                solver_residual.append(float(value))
    return {
        "maximum_qr_reconstruction": max(qr, default=0.0),
        "maximum_reduced_hermiticity": max(hermiticity, default=0.0),
        "maximum_eigenvalue_sum_trace_residual": max(eigen_trace, default=0.0),
        "maximum_trace_distance_transport_invariance": max(transport, default=0.0),
        "maximum_solver_residual_indicator": max(solver_residual, default=0.0),
    }


def build_l4_result(
    sector_results: list[Mapping[str, Any]],
    preflight: Mapping[str, Any],
    checkpoint_root: Path,
    elapsed: float,
) -> dict[str, Any]:
    baseline = load_json(ROOT / DENSE_RESULT_RELATIVE)
    require(
        baseline.get("classification")
        == "RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION",
        "dense baseline classification",
    )
    after_admission = aggregate_stage(4, sector_results, "after_admission")
    after_transport = aggregate_stage(4, sector_results, "after_transport")
    candidate = {
        "after_admission": after_admission,
        "after_transport": after_transport,
    }
    target_difference = max(
        abs(left - right)
        for left, right in zip(registered_values(candidate), registered_values(baseline["fine"]))
    )
    controls = _all_controls(sector_results)
    controls.update(
        {
            "input_carrier_marginal_equality": 0.0,
            "input_lineage_marginal_equality": 0.0,
            "input_q_weight_equality": 0.0,
            "actual_trace_error": abs(sum(after_transport["sector_weights_actual"]) - 1.0),
            "product_trace_error": abs(sum(after_transport["sector_weights_product"]) - 1.0),
            "dense_target_registered_observable_max_abs_difference": target_difference,
            "configuration_tv_le_trace_distance_residual": max(
                0.0,
                float(after_transport["carrier_configuration_tv"])
                - float(after_transport["carrier_trace_distance"]),
            ),
            "number_tv_le_configuration_tv_residual": max(
                0.0,
                float(after_transport["carrier_number_sector_tv"])
                - float(after_transport["carrier_configuration_tv"]),
            ),
        }
    )
    finite = all(math.isfinite(value) for value in registered_values(candidate))
    normalized = all(
        -NORMALIZED_SLOP <= float(candidate[stage][key]) <= 1.0 + NORMALIZED_SLOP
        for stage in ("after_admission", "after_transport")
        for key in (
            "carrier_trace_distance",
            "carrier_configuration_tv",
            "carrier_number_sector_tv",
            "occupation_rms",
        )
    )
    controls_pass = (
        finite
        and normalized
        and target_difference <= DENSE_REPRODUCTION_TOLERANCE
        and max(
            controls["maximum_qr_reconstruction"],
            controls["maximum_reduced_hermiticity"],
            controls["maximum_eigenvalue_sum_trace_residual"],
            controls["maximum_trace_distance_transport_invariance"],
            controls["maximum_solver_residual_indicator"],
            controls["actual_trace_error"],
            controls["product_trace_error"],
            controls["configuration_tv_le_trace_distance_residual"],
            controls["number_tv_le_configuration_tv_residual"],
        )
        <= CONTROL_TOLERANCE
    )
    tau = BASE_TAU
    delta_c = float(after_transport["carrier_trace_distance"])
    return {
        "schema": "L4_L8_TARGET_LINEAGE_SENSITIVE_SCALING_RESULT_V001",
        "classification": (
            "PASS_DENSE_L4_TARGET_REPRODUCTION"
            if controls_pass
            else "FAIL_DENSE_L4_TARGET_REPRODUCTION"
        ),
        "status": "L4_ONLY__L6_L8_EXECUTION_LOCKED",
        "claim_boundary": (
            "TARGET_L4_DENSE_REPRODUCTION_ONLY__NO_INDEPENDENT_AUDIT_SCALING_"
            "PERSISTENCE_CURVATURE_GEOMETRY_OR_GRAVITY"
        ),
        "L": 4,
        "event": 0,
        "schedule": "ONE_INDEPENDENT_REVISIT_FROM_COMMON_AUTHENTICATED_TERMINAL_CHECKPOINT",
        "after_admission": after_admission,
        "after_transport": after_transport,
        "controls": {**controls, "finite": finite, "normalized_ranges": normalized, "passed": controls_pass},
        "tau": tau,
        "T_dyn": delta_c / tau,
        "dependencies": {
            "git_head": preflight["git_head"],
            "engine_sha256": DEPENDENCY_HASHES[str(ENGINE_RELATIVE)],
            "history_sha256": HISTORY_HASHES[4],
            "dense_baseline_sha256": DEPENDENCY_HASHES[str(DENSE_RESULT_RELATIVE)],
            "kernel_sha256": sha256_file(Path(__file__)),
            "runtime_sha256": DEPENDENCY_HASHES[str(RUNTIME_RELATIVE)],
            "durable_evidence_sha256": DEPENDENCY_HASHES[str(DURABLE_RELATIVE)],
        },
        "checkpoint": {
            "root": str(checkpoint_root.relative_to(ROOT)),
            "unit": "ONE_EVENT_OUTPUT_CARRIER_NUMBER_SECTOR_q",
            "completed_sectors": len(sector_results),
            "total_sectors": 5,
            "resume_required_if_incomplete": True,
            "recovery_command": (
                "python3 DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_"
                "SCALING_V001/target_lineage_scaling.py run-l4 --resume"
            ),
        },
        "resource": {
            "wall_seconds": elapsed,
            "peak_parent_rss_bytes": _rss_bytes(resource.RUSAGE_SELF),
            "peak_child_rss_bytes": _rss_bytes(resource.RUSAGE_CHILDREN),
            "maximum_sector_wall_seconds": max(
                float(row["resource"]["wall_seconds"]) for row in sector_results
            ),
            "maximum_sector_peak_rss_bytes": max(
                int(row["resource"]["peak_rss_bytes"]) for row in sector_results
            ),
            "checkpoint_storage_bytes": _directory_bytes(checkpoint_root),
            "authenticated_preterminal_input_bytes": sum(
                int(shard["bytes"])
                for shard in preflight["histories"]["4"]["shards"]
            ),
            "host": {
                "platform": sys.platform,
                "python": sys.version.split()[0],
                "numpy": np.__version__,
                "pid": os.getpid(),
            },
        },
        "sector_results": [
            {
                "q_out": int(row["q_out"]),
                "task_sha256": row["task_binding"]["task_sha256"],
                "after_admission": row["after_admission"],
                "after_transport": row["after_transport"],
                "controls": row["controls"],
                "resource": row["resource"],
            }
            for row in sorted(sector_results, key=lambda item: int(item["q_out"]))
        ],
    }


def run_l4(output: Path, checkpoint_root: Path, resume: bool) -> dict[str, Any]:
    validate_execution_length(4)
    require(not output.exists(), f"refuse to overwrite final output: {output}")
    started = time.perf_counter()
    preflight = authenticate_all_inputs()
    durable, runtime = load_resume_runtime()
    tasks = [
        runtime.TaskSpec(
            task_id=f"L04_event00_qout{q:02d}",
            payload={"L": 4, "event": 0, "q_out": q},
            work_units=max(1, math.comb(8, q)),
        )
        for q in range(5)
    ]
    runner = runtime.ResumableProcessPool(
        checkpoint_root=checkpoint_root,
        run_id="L4-L8-TARGET-SCALING-V001-L4-EVENT00",
        branch="target",
        phase="dense-l4-reproduction",
        kernel_module=Path(__file__),
        kernel_function="sector_kernel",
        tasks=tasks,
        workers=1,
        parameters={
            "schema": "L4_L8_TARGET_SCALING_RUN_PARAMETERS_V001",
            "authorized_lengths": [4],
            "L": 4,
            "events": [0],
            "resolution": "TARGET_V004_FINE",
            "history_sha256": HISTORY_HASHES[4],
            "engine_sha256": DEPENDENCY_HASHES[str(ENGINE_RELATIVE)],
            "kernel_sha256": sha256_file(Path(__file__)),
            "dense_baseline_sha256": DEPENDENCY_HASHES[str(DENSE_RESULT_RELATIVE)],
        },
    )
    outcome = runner.run(resume=resume, max_inflight=1)
    if outcome.status == "STOPPED":
        print("STOPPED: resume with --resume", file=sys.stderr)
        raise SystemExit(75)
    require(outcome.status == "COMPLETE", "resumable runtime did not complete")
    sector_results = runtime.load_task_results(checkpoint_root, tasks)
    elapsed = time.perf_counter() - started
    result = build_l4_result(sector_results, preflight, checkpoint_root, elapsed)
    require(result["controls"]["passed"], "dense L4 target reproduction gate failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    durable.immutable_write_json(output, result)
    print(result["classification"])
    print(
        "L4 wall={:.6f}s rss={} checkpoint_bytes={} dense_difference={:.3e}".format(
            result["resource"]["wall_seconds"],
            max(
                result["resource"]["peak_parent_rss_bytes"],
                result["resource"]["peak_child_rss_bytes"],
                result["resource"]["maximum_sector_peak_rss_bytes"],
            ),
            result["resource"]["checkpoint_storage_bytes"],
            result["controls"]["dense_target_registered_observable_max_abs_difference"],
        )
    )
    return result


def verify_l4_output(path: Path) -> dict[str, Any]:
    result = load_json(path)
    require(
        set(result)
        == {
            "schema",
            "classification",
            "status",
            "claim_boundary",
            "L",
            "event",
            "schedule",
            "after_admission",
            "after_transport",
            "controls",
            "tau",
            "T_dyn",
            "dependencies",
            "checkpoint",
            "resource",
            "sector_results",
        },
        "L4 output top-level key census",
    )
    require(result["schema"] == "L4_L8_TARGET_LINEAGE_SENSITIVE_SCALING_RESULT_V001", "L4 schema")
    require(result["classification"] == "PASS_DENSE_L4_TARGET_REPRODUCTION", "L4 classification")
    require(result["status"] == "L4_ONLY__L6_L8_EXECUTION_LOCKED", "L4 lock status")
    require(result["L"] == 4 and result["event"] == 0, "L4 identity")
    require(result["controls"]["passed"] is True, "L4 controls")
    require(
        float(result["controls"]["dense_target_registered_observable_max_abs_difference"])
        <= DENSE_REPRODUCTION_TOLERANCE,
        "L4 dense reproduction tolerance",
    )
    require(len(result["sector_results"]) == 5, "L4 sector census")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("authenticate")
    run_parser = subparsers.add_parser("run-l4")
    run_parser.add_argument("--resume", action="store_true")
    run_parser.add_argument(
        "--output",
        type=Path,
        default=PACKET / "PHYSICAL_OUTPUTS" / "L4_TARGET_REPRODUCTION_V001.json",
    )
    run_parser.add_argument(
        "--checkpoint-root",
        type=Path,
        default=PACKET / "CHECKPOINTS" / "L4_EVENT00_TARGET_V001R1",
    )
    verify_parser = subparsers.add_parser("verify-l4")
    verify_parser.add_argument(
        "--output",
        type=Path,
        default=PACKET / "PHYSICAL_OUTPUTS" / "L4_TARGET_REPRODUCTION_V001.json",
    )
    arguments = parser.parse_args()
    if arguments.command == "authenticate":
        authenticated = authenticate_all_inputs()
        count = sum(len(row["shards"]) for row in authenticated["histories"].values())
        print(f"PASS target inputs: {len(authenticated['dependencies'])} dependencies, {count} shards")
    elif arguments.command == "run-l4":
        run_l4(arguments.output.resolve(), arguments.checkpoint_root.resolve(), arguments.resume)
    else:
        authenticate_all_inputs()
        result = verify_l4_output(arguments.output.resolve())
        print(
            "PASS L4 target output: dense difference {:.3e}".format(
                result["controls"]["dense_target_registered_observable_max_abs_difference"]
            )
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ScalingError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL target scaling V001: {error}", file=sys.stderr)
        raise SystemExit(2)
