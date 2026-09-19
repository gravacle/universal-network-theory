#!/usr/bin/env python3
"""Nonphysical index/allocation and hard-lock preflight for hostile V004."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

import build_hostile_v004_cache as builder
import independent_prefix_history as physical
import independent_prefix_history_v003 as v3


HERE = Path(__file__).resolve().parent
FREEZE = HERE / "FROZEN_MANIFEST_V004.json"
METHOD = HERE / "V004_STORAGE_ONLY_CACHE_METHOD.md"
CONSUMER = HERE / "independent_prefix_history_v004.py"
GATES = (
    HERE / "CACHE_PAYLOAD_BUILD_GATE_V004.json",
    HERE / "PHYSICAL_CONTROL_EXECUTION_GATE_V004.json",
    HERE / "CONTROL_GATE_V004.json",
    HERE / "L10_GATE_V004.json",
)
SUPPORTED = (4, 6, 8, 10, 12)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def freeze_and_syntax() -> dict[str, object]:
    manifest = json.loads(FREEZE.read_text(encoding="utf-8"))
    require(manifest["status"] == "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT", "freeze status")
    paths = {
        "method": METHOD,
        "builder": HERE / "build_hostile_v004_cache.py",
        "consumer": CONSUMER,
        "preflight": Path(__file__),
    }
    for role, path in paths.items():
        require(sha256(path) == manifest["files"][role], f"frozen {role} hash")
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for dependency, expected in manifest["sealed_dependencies"].items():
        require(sha256(HERE / dependency) == expected, f"sealed dependency {dependency}")
    return {"status": "PASS", "freeze_sha256": sha256(FREEZE)}


def exhaustive_rank_index() -> dict[str, object]:
    checks = 0
    for width in range(17):
        for q in range(width + 1):
            words = physical.reverse_masks(width, q)
            require(len(words) == math.comb(width, q), f"rank basis census w{width}q{q}")
            for index, word in enumerate(words):
                require(v3.reverse_rank(width, q, int(word)) == index,
                        f"reverse rank w{width}q{q}i{index}")
                checks += 1
    return {"status": "PASS", "exhaustive_width_max": 16, "rank_checks": checks}


def exhaustive_l4_materialization() -> dict[str, object]:
    length = 4
    edges = physical.hostile_edges(length)
    operator_bytes = 0
    admission_bytes = 0
    lineage_bytes = 0
    array_checks = 0
    words_by_q: dict[int, np.ndarray] = {}
    for q in range(length + 1):
        words, offsets, sources, targets = builder.exact_operator_arrays(length, q, edges)
        words_by_q[q] = words
        require(len(offsets) == 3 * length + 1, f"L4 q{q} offset census")
        require(int(offsets[0]) == 0 and int(offsets[-1]) == len(sources), f"L4 q{q} offsets")
        require(len(sources) == len(targets), f"L4 q{q} pair census")
        operator_bytes += words.nbytes + sources.nbytes + targets.nbytes
        array_checks += 4
    for event in range(length):
        for q in range(1, event + 2):
            occupied, old = builder.admission_arrays(length, event, q, words_by_q[q])
            require(len(occupied) == len(old), f"L4 event{event}q{q} admission pair")
            admission_bytes += occupied.nbytes + old.nbytes
            array_checks += 2
    for event in range(length - 1):
        for q in range(event + 1):
            same, added = builder.lineage_arrays(event, q)
            require(len(same) == len(added) == math.comb(event, q),
                    f"L4 event{event}q{q} lineage pair")
            lineage_bytes += same.nbytes + added.nbytes
            array_checks += 2
    require(operator_bytes == builder.cache_operator_bytes(length), "L4 operator bytes")
    require(admission_bytes == builder.cache_admission_bytes(length), "L4 admission bytes")
    require(lineage_bytes == builder.cache_lineage_bytes(length), "L4 lineage bytes")
    return {
        "status": "PASS",
        "array_checks": array_checks,
        "operator_bytes": operator_bytes,
        "admission_bytes": admission_bytes,
        "lineage_bytes": lineage_bytes,
        "payload_bytes": operator_bytes + admission_bytes + lineage_bytes,
    }


def allocation_census() -> dict[str, object]:
    rows: dict[str, object] = {}
    checks = 0
    for length in SUPPORTED:
        operator = builder.cache_operator_bytes(length)
        admission = builder.cache_admission_bytes(length)
        lineage = builder.cache_lineage_bytes(length)
        cache = builder.cache_payload_bytes(length)
        state = builder.maximum_state_bytes(length)
        require(cache == operator + admission + lineage, f"L{length} cache sum")
        require(cache + state + builder.OVERHEAD_RESERVE < builder.SCRATCH_LIMIT,
                f"L{length} scratch allocation")
        max_rank = max(math.comb(2 * length, q) for q in range(length + 1)) - 1
        require(max_rank <= np.iinfo(np.int32).max, f"L{length} int32 carrier ranks")
        edge_pairs = sum(
            3 * length * (math.comb(2 * length - 2, q - 1) if q else 0)
            for q in range(length + 1)
        )
        require(operator == 4 * sum(math.comb(2 * length, q) for q in range(length + 1))
                + 8 * edge_pairs, f"L{length} operator closed form")
        admission_pairs = sum(
            math.comb(2 * length - 1, q - 1)
            for event in range(length) for q in range(1, event + 2)
        )
        require(admission == 8 * admission_pairs, f"L{length} admission closed form")
        rows[str(length)] = {
            "operator_bytes": operator,
            "admission_bytes": admission,
            "lineage_bytes": lineage,
            "cache_payload_bytes_excluding_offsets": cache,
            "maximum_live_state_bytes": state,
            "state_plus_cache_bytes": state + cache,
            "maximum_carrier_rank": max_rank,
            "ordered_exchange_pairs": edge_pairs,
        }
        checks += 7
    require(rows["12"]["cache_payload_bytes_excluding_offsets"] == 826_218_064,
            "frozen L12 cache payload")
    require(rows["12"]["maximum_live_state_bytes"] == 8_773_664_640,
            "frozen L12 state payload")
    require(rows["12"]["state_plus_cache_bytes"] == 9_599_882_704,
            "frozen L12 combined payload")
    return {"status": "PASS", "checks": checks + 3, "sizes": rows}


def hard_lock_refusal() -> dict[str, object]:
    require(all(not gate.exists() for gate in GATES), "a future V004 gate exists at preflight")
    with tempfile.TemporaryDirectory(prefix="hostile-v004-lock-") as temporary:
        root = Path(temporary)
        cache_output = root / "cache_must_not_exist"
        build = subprocess.run(
            [sys.executable, str(HERE / "build_hostile_v004_cache.py"),
             "--length", "4", "--output", str(cache_output)],
            cwd=HERE, capture_output=True, text=True, check=False,
        )
        require(build.returncode == 2 and not cache_output.exists(), "cache builder did not lock")
        history_output = root / "history_must_not_exist.json"
        workspace = root / "workspace_must_not_exist"
        consume = subprocess.run(
            [sys.executable, str(CONSUMER), "execute", "--length", "4",
             "--output", str(history_output), "--workspace", str(workspace),
             "--cache-root", str(root / "absent_cache")],
            cwd=HERE, capture_output=True, text=True, check=False,
        )
        require(
            consume.returncode == 2 and not history_output.exists() and not workspace.exists(),
            "physical consumer did not lock before output/workspace",
        )
    return {
        "status": "PASS",
        "cache_builder_returncode": 2,
        "cache_payload_created": False,
        "physical_consumer_returncode": 2,
        "history_output_created": False,
        "history_workspace_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("refuse to overwrite V004 preflight output")
    result: dict[str, object] = {
        "schema": "HOSTILE_V004_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT",
        "cache_payload_created": False,
        "physical_history_executed": False,
        "tests": {},
    }
    try:
        result["tests"] = {
            "freeze_and_syntax": freeze_and_syntax(),
            "exhaustive_reverse_rank": exhaustive_rank_index(),
            "exhaustive_L4_cache_indices": exhaustive_l4_materialization(),
            "allocation_census_L4_L12": allocation_census(),
            "hard_lock_refusal": hard_lock_refusal(),
        }
        result["classification"] = "PASS_V004_STORAGE_CACHE_PREFLIGHT__ALL_PHYSICAL_MODES_LOCKED"
    except Exception as error:
        result["classification"] = "FAIL_V004_STORAGE_CACHE_PREFLIGHT"
        result["error"] = f"{type(error).__name__}: {error}"
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if result["classification"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
