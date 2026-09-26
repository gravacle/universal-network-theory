#!/usr/bin/env python3
"""Guarded implementation skeleton for the frozen L8 lineage-order test.

Importing this module and ``--check-freeze`` never evaluate curvature or a
correlation.  Physical evaluation requires the explicit authorization flag.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import resource
import stat
import tempfile
import time
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = HERE / "PROTOCOL.md"
FREEZE = HERE / "FREEZE.json"
SOURCE_HASHES = HERE / "SOURCE_HASHES.sha256"
OUTPUT = HERE / "RESULT.json"
LENGTH = 8
PHI = math.pi / 4.0


class Unresolved(RuntimeError):
    """A frozen custody, numerical, or implementation condition failed."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise Unresolved(f"expected JSON object: {path.relative_to(ROOT)}")
    return value


def authenticate_source_freeze() -> dict[str, str]:
    records: dict[str, str] = {}
    for raw in SOURCE_HASHES.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, relative = raw.split("  ", 1)
        path = ROOT / relative
        if sha256(path) != digest:
            raise Unresolved(f"source freeze mismatch: {relative}")
        records[relative] = digest
    required = {
        str(PROTOCOL.relative_to(ROOT)),
        str(FREEZE.relative_to(ROOT)),
        str(Path(__file__).resolve().relative_to(ROOT)),
    }
    if set(records) != required:
        raise Unresolved("source freeze census mismatch")
    return records


def authenticate_declared_inputs(freeze: dict) -> dict[str, str]:
    observed: dict[str, str] = {}
    simple = ("history", "cache_manifest", "joint_witness")
    for name in simple:
        record = freeze["inputs"][name]
        path = ROOT / record["path"]
        digest = sha256(path)
        if digest != record["sha256"]:
            raise Unresolved(f"input hash mismatch: {name}")
        observed[record["path"]] = digest
    for record in freeze["inputs"]["representation_sources"]:
        path = ROOT / record["path"]
        digest = sha256(path)
        if digest != record["sha256"]:
            raise Unresolved(f"representation-source hash mismatch: {record['path']}")
        observed[record["path"]] = digest
    return observed


def fixed_words(width: int, weight: int) -> np.ndarray:
    values = np.empty(math.comb(width, weight), dtype=np.uint32)
    for index, positions in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        values[index] = word
    return values


def reconstruct_terminal_lineage(freeze: dict) -> tuple[np.ndarray, np.ndarray, dict[str, str]]:
    history_path = ROOT / freeze["inputs"]["history"]["path"]
    history = load_json(history_path)
    if history.get("L") != LENGTH or history.get("lineage_authority") != (
        "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
    ):
        raise Unresolved("L8 history lineage authority mismatch")
    shards = history.get("terminal_shards")
    if not isinstance(shards, list) or [row.get("q") for row in shards] != list(range(LENGTH)):
        raise Unresolved("terminal shard census mismatch")

    terminal = np.zeros(1 << LENGTH, dtype=float)
    sector = np.zeros(LENGTH + 1, dtype=float)
    shard_hashes: dict[str, str] = {}
    cosine2 = math.cos(PHI) ** 2
    sine2 = math.sin(PHI) ** 2
    root = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L8/sharp/prefix_07"
    for q, record in enumerate(shards):
        path = root / f"q_{q:02d}.npy"
        if Path(record["path"]).resolve() != path.resolve():
            raise Unresolved(f"noncanonical terminal shard path q={q}")
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode != 0o444 or path.stat().st_size != record["bytes"]:
            raise Unresolved(f"terminal shard mode/size mismatch q={q}")
        digest = sha256(path)
        if digest != record["sha256"]:
            raise Unresolved(f"terminal shard hash mismatch q={q}")
        shard_hashes[str(path.relative_to(ROOT))] = digest

        block = np.load(path, mmap_mode="r", allow_pickle=False)
        expected_shape = (math.comb(7, q), math.comb(16, q))
        if tuple(block.shape) != expected_shape or list(block.shape) != record["shape"]:
            raise Unresolved(f"terminal shard shape mismatch q={q}")
        probability = np.abs(np.asarray(block)) ** 2
        carrier_words = fixed_words(16, q)
        blank = ((carrier_words >> 7) & 1) == 0
        blank_row = np.sum(probability[:, blank], axis=1)
        occupied_row = np.sum(probability[:, ~blank], axis=1)
        for row, word_raw in enumerate(fixed_words(7, q)):
            word = int(word_raw)
            stay = float(occupied_row[row] + cosine2 * blank_row[row])
            accepted = float(sine2 * blank_row[row])
            if stay < -1e-15 or accepted < -1e-15:
                raise Unresolved("negative reconstructed lineage probability")
            terminal[word] += max(0.0, stay)
            terminal[word | (1 << 7)] += max(0.0, accepted)
            sector[q] += max(0.0, stay)
            sector[q + 1] += max(0.0, accepted)

    if not np.all(np.isfinite(terminal)) or abs(float(np.sum(terminal)) - 1.0) > 1e-12:
        raise Unresolved("terminal lineage normalization failure")
    history_sector = np.asarray(history["rows"][-1]["sector_weights"], dtype=float)
    if float(np.max(np.abs(sector - history_sector))) > 1e-10:
        raise Unresolved("history terminal-sector reconstruction mismatch")

    witness = load_json(ROOT / freeze["inputs"]["joint_witness"]["path"])
    rows = [row for row in witness.get("rows", []) if row.get("L") == LENGTH]
    if len(rows) != 1:
        raise Unresolved("joint-witness L8 row mismatch")
    q_rows = rows[0]["fine"]["terminal"]["q_contributions"]
    witness_sector = np.asarray([q_rows[str(q)]["p_q"] for q in range(LENGTH + 1)])
    if float(np.max(np.abs(sector - witness_sector))) > 1e-10:
        raise Unresolved("joint-witness terminal-sector reconstruction mismatch")
    return terminal, sector, shard_hashes


def path_measures(alpha: float) -> list[np.ndarray]:
    measures: list[np.ndarray] = []
    for node in range(LENGTH):
        neighbors = [item for item in (node - 1, node + 1) if 0 <= item < LENGTH]
        measure = np.zeros(LENGTH, dtype=float)
        measure[node] = alpha
        for neighbor in neighbors:
            measure[neighbor] += (1.0 - alpha) / len(neighbors)
        measures.append(measure)
    return measures


def path_wasserstein(left: np.ndarray, right: np.ndarray) -> float:
    """Exact W1 cut formula for a unit path."""
    return float(np.sum(np.abs(np.cumsum(left - right)[:-1])))


def curvature_vector(alpha: float) -> tuple[list[float], np.ndarray]:
    measures = path_measures(alpha)
    edges = [1.0 - path_wasserstein(measures[x], measures[x + 1]) for x in range(7)]
    nodes = np.zeros(LENGTH, dtype=float)
    for node in range(LENGTH):
        incident = []
        if node:
            incident.append(edges[node - 1])
        if node < LENGTH - 1:
            incident.append(edges[node])
        nodes[node] = float(sum(incident) / len(incident))
    return edges, nodes


def midranks(values: Sequence[float]) -> np.ndarray:
    order = sorted(range(len(values)), key=lambda index: (values[index], index))
    ranks = np.empty(len(values), dtype=float)
    lower = 0
    while lower < len(order):
        upper = lower + 1
        while upper < len(order) and values[order[upper]] == values[order[lower]]:
            upper += 1
        rank = 0.5 * ((lower + 1) + upper)
        for index in order[lower:upper]:
            ranks[index] = rank
        lower = upper
    return ranks


def spearman(left: Sequence[float], right: Sequence[float]) -> float:
    a = midranks(left)
    b = midranks(right)
    a -= float(np.mean(a))
    b -= float(np.mean(b))
    denominator = math.sqrt(float(np.dot(a, a) * np.dot(b, b)))
    if denominator == 0.0:
        raise Unresolved("zero-variance Spearman input")
    value = float(np.dot(a, b) / denominator)
    if not math.isfinite(value):
        raise Unresolved("nonfinite Spearman statistic")
    return value


def terminal_record_concentration(probability: np.ndarray) -> np.ndarray:
    result = np.zeros(LENGTH, dtype=float)
    for word, weight in enumerate(probability):
        for event in range(LENGTH):
            if (word >> event) & 1:
                result[event] += float(weight)
    return result


def exact_permutation_null(curvature: np.ndarray, record: np.ndarray, guard: float) -> dict:
    observed = spearman(curvature, record)
    plus = minus = total = 0
    for permutation in itertools.permutations(range(LENGTH)):
        value = spearman(curvature, record[list(permutation)])
        total += 1
        plus += int(value >= observed - guard)
        minus += int(value <= observed + guard)
    if total != math.factorial(LENGTH):
        raise Unresolved("permutation census mismatch")
    return {
        "rho_observed": observed,
        "p_plus": plus / total,
        "p_minus": minus / total,
        "plus_count": plus,
        "minus_count": minus,
        "permutations": total,
    }


def rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if os.uname().sysname == "Darwin" else value * 1024


def execute(freeze: dict, source_hashes: dict[str, str], input_hashes: dict[str, str]) -> dict:
    started = time.monotonic()
    lineage, sector, shard_hashes = reconstruct_terminal_lineage(freeze)
    edge_curvature, node_curvature = curvature_vector(float(freeze["ollivier_ricci"]["idleness"]))
    record = terminal_record_concentration(lineage)
    null = exact_permutation_null(node_curvature, record, float(freeze["comparison_guard"]))
    rho = null["rho_observed"]
    floor = float(freeze["effect_floor"])
    ceiling = float(freeze["tail_probability_ceiling"])
    if rho >= floor and null["p_plus"] <= ceiling:
        classification = "POSITIVE_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8"
    elif rho <= -floor and null["p_minus"] <= ceiling:
        classification = "OPPOSITE_SIGN_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8"
    else:
        classification = "NO_RESOLVED_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8"
    elapsed = time.monotonic() - started
    peak = rss_bytes()
    if elapsed > freeze["runtime"]["wall_seconds_max"] or peak > freeze["runtime"]["rss_bytes_max"]:
        raise Unresolved("frozen runtime budget exceeded")
    return {
        "schema": "L8_LINEAGE_ORDER_OLLIVIER_RICCI_RESULT_V001",
        "classification": classification,
        "passed_positive_prediction": classification.startswith("POSITIVE_"),
        "graph_ceiling": "FINITE_SCHEDULE_DERIVED_DIAGNOSTIC__NOT_SPACETIME_CURVATURE_OR_GRAVITY",
        "edge_curvature": edge_curvature,
        "node_curvature": node_curvature.tolist(),
        "record_concentration": record.tolist(),
        "terminal_sector_weights": sector.tolist(),
        "statistic": null,
        "controls": {
            "lineage_probability_sum": float(np.sum(lineage)),
            "source_hashes": source_hashes,
            "input_hashes": input_hashes,
            "shard_hashes": shard_hashes,
            "wall_seconds": elapsed,
            "peak_rss_bytes": peak,
        },
    }


def atomic_publish(result: dict) -> None:
    if OUTPUT.exists():
        raise Unresolved("refuse to overwrite existing result")
    payload = json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n"
    descriptor, name = tempfile.mkstemp(prefix=".RESULT.", suffix=".tmp", dir=HERE)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, OUTPUT)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-freeze", action="store_true")
    parser.add_argument("--authorize-frozen-analysis", action="store_true")
    arguments = parser.parse_args()
    source_hashes = authenticate_source_freeze()
    freeze = load_json(FREEZE)
    input_hashes = authenticate_declared_inputs(freeze)
    if arguments.check_freeze and not arguments.authorize_frozen_analysis:
        print("L8_LINEAGE_ORDER_CURVATURE_FREEZE_AUTHENTICATED__NO_ANALYSIS_RUN")
        return 0
    if not arguments.authorize_frozen_analysis:
        raise SystemExit("physical analysis requires --authorize-frozen-analysis")
    if freeze.get("execution_authorized") is not False:
        raise Unresolved("review freeze authorization field changed")
    result = execute(freeze, source_hashes, input_hashes)
    atomic_publish(result)
    print(result["classification"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
