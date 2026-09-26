#!/usr/bin/env python3
"""Strict validator for the frozen L8 lineage-order curvature result."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULT = HERE / "RESULT.json"
FREEZE = HERE / "FREEZE.json"
SOURCE_HASHES = HERE / "SOURCE_HASHES.sha256"
MANIFEST = HERE / "MANIFEST.sha256"
EXPECTED_CLASSIFICATION = "NO_RESOLVED_LINEAGE_ORDER_CURVATURE_RECORD_ASSOCIATION_L8"
EXPECTED_CEILING = "FINITE_SCHEDULE_DERIVED_DIAGNOSTIC__NOT_SPACETIME_CURVATURE_OR_GRAVITY"
EXPECTED_EDGE_CURVATURE = [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5]
EXPECTED_NODE_CURVATURE = [0.5, 0.25, 0.0, 0.0, 0.0, 0.0, 0.25, 0.5]


class ValidationFailure(AssertionError):
    pass


class Checks:
    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, message: str) -> None:
        self.count += 1
        if not condition:
            raise ValidationFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if type(value) is not dict:
        raise ValidationFailure(f"not a JSON object: {path.name}")
    return value


def parse_hash_manifest(path: Path) -> dict[str, str]:
    records: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        try:
            digest, relative = line.split("  ", 1)
        except ValueError as error:
            raise ValidationFailure(f"malformed hash line in {path.name}") from error
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ValidationFailure(f"malformed digest in {path.name}")
        if relative in records:
            raise ValidationFailure(f"duplicate manifest member: {relative}")
        records[relative] = digest
    return records


def authenticate_manifest(path: Path, checks: Checks) -> dict[str, str]:
    records = parse_hash_manifest(path)
    for relative, digest in records.items():
        member = ROOT / relative
        checks.require(member.is_file(), f"missing manifest member: {relative}")
        checks.require(sha256(member) == digest, f"manifest hash mismatch: {relative}")
    return records


def finite_number(value: Any) -> bool:
    return type(value) in (int, float) and type(value) is not bool and math.isfinite(float(value))


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return math.isfinite(float(left)) and abs(float(left) - float(right)) <= tolerance


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
    a -= np.mean(a)
    b -= np.mean(b)
    denominator = math.sqrt(float(np.dot(a, a) * np.dot(b, b)))
    if denominator == 0.0:
        raise ValidationFailure("zero-variance Spearman input")
    return float(np.dot(a, b) / denominator)


def independent_null(curvature: Sequence[float], record: Sequence[float], guard: float) -> dict[str, Any]:
    observed = spearman(curvature, record)
    plus = minus = total = 0
    for permutation in itertools.permutations(range(8)):
        shuffled = [record[index] for index in permutation]
        value = spearman(curvature, shuffled)
        total += 1
        plus += int(value >= observed - guard)
        minus += int(value <= observed + guard)
    return {
        "rho_observed": observed,
        "plus_count": plus,
        "minus_count": minus,
        "permutations": total,
        "p_plus": plus / total,
        "p_minus": minus / total,
    }


def validate(record: dict[str, Any], *, authenticate_packet: bool = True) -> int:
    checks = Checks()
    freeze = read_json(FREEZE)
    source_records = authenticate_manifest(SOURCE_HASHES, checks)
    checks.require(set(source_records) == {
        "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/PROTOCOL.md",
        "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/FREEZE.json",
        "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/compute_lineage_order_curvature.py",
    }, "source-freeze census mismatch")
    if authenticate_packet:
        packet = authenticate_manifest(MANIFEST, checks)
        checks.require("DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/RESULT.json" in packet,
                       "result absent from packet manifest")

    checks.require(set(record) == {
        "schema", "classification", "passed_positive_prediction", "graph_ceiling",
        "edge_curvature", "node_curvature", "record_concentration",
        "terminal_sector_weights", "statistic", "controls",
    }, "result key census mismatch")
    checks.require(record["schema"] == "L8_LINEAGE_ORDER_OLLIVIER_RICCI_RESULT_V001",
                   "result schema mismatch")
    checks.require(record["classification"] == EXPECTED_CLASSIFICATION,
                   "result classification mismatch")
    checks.require(record["passed_positive_prediction"] is False,
                   "positive-prediction Boolean mismatch")
    checks.require(record["graph_ceiling"] == EXPECTED_CEILING, "claim ceiling mismatch")

    for key, expected in (("edge_curvature", EXPECTED_EDGE_CURVATURE),
                          ("node_curvature", EXPECTED_NODE_CURVATURE)):
        values = record[key]
        checks.require(type(values) is list and len(values) == len(expected), f"{key} census mismatch")
        for index, (value, reference) in enumerate(zip(values, expected)):
            checks.require(finite_number(value) and close(value, reference, 1e-15),
                           f"{key}[{index}] mismatch")

    concentration = record["record_concentration"]
    checks.require(type(concentration) is list and len(concentration) == 8,
                   "record concentration census mismatch")
    for index, value in enumerate(concentration):
        checks.require(finite_number(value) and 0.0 <= value <= 1.0,
                       f"record concentration out of range at {index}")

    sectors = record["terminal_sector_weights"]
    checks.require(type(sectors) is list and len(sectors) == 9, "sector census mismatch")
    for index, value in enumerate(sectors):
        checks.require(finite_number(value) and value >= 0.0, f"sector weight invalid at {index}")
    checks.require(close(sum(sectors), 1.0, 1e-12), "sector normalization mismatch")

    statistic = record["statistic"]
    checks.require(set(statistic) == {
        "rho_observed", "p_plus", "p_minus", "plus_count", "minus_count", "permutations",
    }, "statistic key census mismatch")
    recomputed = independent_null(record["node_curvature"], concentration,
                                  float(freeze["comparison_guard"]))
    for key in ("plus_count", "minus_count", "permutations"):
        checks.require(type(statistic[key]) is int and statistic[key] == recomputed[key],
                       f"statistic {key} mismatch")
    for key in ("rho_observed", "p_plus", "p_minus"):
        checks.require(finite_number(statistic[key]) and close(statistic[key], recomputed[key], 1e-15),
                       f"statistic {key} mismatch")
    checks.require(statistic["permutations"] == math.factorial(8), "null census is not 8 factorial")
    checks.require(statistic["rho_observed"] < freeze["effect_floor"] or
                   statistic["p_plus"] > freeze["tail_probability_ceiling"],
                   "null classification contradicts positive pass rule")
    checks.require(not (statistic["rho_observed"] <= -freeze["effect_floor"] and
                        statistic["p_minus"] <= freeze["tail_probability_ceiling"]),
                   "null classification contradicts opposite-sign rule")

    controls = record["controls"]
    checks.require(set(controls) == {
        "input_hashes", "lineage_probability_sum", "peak_rss_bytes", "shard_hashes",
        "source_hashes", "wall_seconds",
    }, "control key census mismatch")
    checks.require(close(controls["lineage_probability_sum"], 1.0, 1e-12),
                   "lineage normalization mismatch")
    checks.require(finite_number(controls["wall_seconds"]) and
                   0.0 <= controls["wall_seconds"] <= freeze["runtime"]["wall_seconds_max"],
                   "wall budget mismatch")
    checks.require(type(controls["peak_rss_bytes"]) is int and
                   0 < controls["peak_rss_bytes"] <= freeze["runtime"]["rss_bytes_max"],
                   "RSS budget mismatch")
    checks.require(controls["source_hashes"] == source_records, "reported source hashes mismatch")

    declared_inputs = {}
    for name in ("history", "cache_manifest", "joint_witness"):
        item = freeze["inputs"][name]
        declared_inputs[item["path"]] = item["sha256"]
    for item in freeze["inputs"]["representation_sources"]:
        declared_inputs[item["path"]] = item["sha256"]
    checks.require(controls["input_hashes"] == declared_inputs, "reported input hashes mismatch")
    for relative, digest in controls["input_hashes"].items():
        checks.require(sha256(ROOT / relative) == digest, f"live input hash mismatch: {relative}")

    history = read_json(ROOT / freeze["inputs"]["history"]["path"])
    expected_shards = {
        str(Path(item["path"]).resolve().relative_to(ROOT)): item["sha256"]
        for item in history["terminal_shards"]
    }
    checks.require(controls["shard_hashes"] == expected_shards, "reported shard hashes mismatch")
    for relative, digest in controls["shard_hashes"].items():
        checks.require(sha256(ROOT / relative) == digest, f"live shard hash mismatch: {relative}")

    history_sectors = history["rows"][-1]["sector_weights"]
    for index, (value, reference) in enumerate(zip(sectors, history_sectors)):
        checks.require(close(value, reference, 1e-10), f"history sector mismatch at {index}")
    witness = read_json(ROOT / freeze["inputs"]["joint_witness"]["path"])
    witness_rows = [row for row in witness["rows"] if row["L"] == 8]
    checks.require(len(witness_rows) == 1, "joint-witness L8 row census mismatch")
    q_rows = witness_rows[0]["fine"]["terminal"]["q_contributions"]
    for q, value in enumerate(sectors):
        checks.require(close(value, q_rows[str(q)]["p_q"], 1e-10),
                       f"joint-witness sector mismatch at {q}")
    return checks.count


def main() -> int:
    record = read_json(RESULT)
    count = validate(record)
    print(f"PASS_L8_LINEAGE_ORDER_CURVATURE_RESULT checks={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
