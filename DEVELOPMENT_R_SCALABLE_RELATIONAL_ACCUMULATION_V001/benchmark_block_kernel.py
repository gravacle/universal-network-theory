#!/usr/bin/env python3
"""Benchmark exact retained-sector kernels before any L10 history output.

This is a resource projection, not a history solver.  It constructs each
sharp carrier-number block, times a deterministic batched Hamiltonian action
and edge-current evaluation, and scales only over the exact genesis-row
multiplicity.  No state, branch, edge, or correlation is truncated.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
OUT = HERE / "BLOCK_KERNEL_BENCHMARK.json"
SIZES = (8, 10)
REPEATS = 3
MAX_BENCH_ROWS = 4


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def carrier_words(width: int, weight: int) -> np.ndarray:
    values = np.empty(math.comb(width, weight), dtype=np.uint32)
    for index, chosen in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for bit in chosen:
            word |= 1 << bit
        values[index] = word
    return values


def prism_edges(length: int) -> list[tuple[int, int]]:
    edges = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length))
    for site in range(length):
        edges.append((site, length + (site + 1) % length))
    return edges


class CarrierSector:
    def __init__(self, length: int, q: int):
        self.length = length
        self.q = q
        self.words = carrier_words(2 * length, q)
        self.index = {int(word): index for index, word in enumerate(self.words)}
        self.pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for u, v in prism_edges(length):
            left = np.flatnonzero(
                (((self.words >> u) & 1) == 1)
                & (((self.words >> v) & 1) == 0)
            ).astype(np.int32)
            mask = np.uint32((1 << u) | (1 << v))
            right = np.fromiter(
                (self.index[int(self.words[column] ^ mask)] for column in left),
                dtype=np.int32,
                count=len(left),
            )
            self.pairs.append((left, right))

    def h(self, vector: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(vector)
        for left, right in self.pairs:
            answer[:, left] -= vector[:, right]
            answer[:, right] -= vector[:, left]
        return answer

    def currents(self, vector: np.ndarray) -> np.ndarray:
        result = np.empty(len(self.pairs), dtype=float)
        for edge, (left, right) in enumerate(self.pairs):
            result[edge] = 2.0 * float(np.imag(np.vdot(vector[:, left], vector[:, right])))
        return result


def benchmark_size(length: int) -> dict[str, object]:
    sectors = []
    full_h_seconds = 0.0
    full_current_seconds = 0.0
    rng = np.random.default_rng(8191 + length)
    for q in range(length + 1):
        sector = CarrierSector(length, q)
        genesis_rows = math.comb(length, q)
        bench_rows = min(MAX_BENCH_ROWS, genesis_rows)
        width = len(sector.words)
        sample = (
            rng.standard_normal((bench_rows, width))
            + 1j * rng.standard_normal((bench_rows, width))
        ).astype(np.complex128)
        sample /= np.linalg.norm(sample)

        sector.h(sample)
        started = time.perf_counter()
        for _ in range(REPEATS):
            sector.h(sample)
        h_seconds = (time.perf_counter() - started) / REPEATS

        sector.currents(sample)
        started = time.perf_counter()
        for _ in range(REPEATS):
            sector.currents(sample)
        current_seconds = (time.perf_counter() - started) / REPEATS

        scaled_h = h_seconds * genesis_rows / bench_rows
        scaled_current = current_seconds * genesis_rows / bench_rows
        full_h_seconds += scaled_h
        full_current_seconds += scaled_current
        sectors.append({
            "q": q,
            "genesis_rows": genesis_rows,
            "carrier_columns": width,
            "block_dimension": genesis_rows * width,
            "bench_rows": bench_rows,
            "h_seconds": h_seconds,
            "current_seconds": current_seconds,
            "scaled_full_block_h_seconds": scaled_h,
            "scaled_full_block_current_seconds": scaled_current,
            "directed_pair_entries": int(sum(len(left) for left, _ in sector.pairs)),
        })
    exact_dimension = math.comb(3 * length, length)
    return {
        "L": length,
        "exact_dimension": exact_dimension,
        "complex128_state_bytes": exact_dimension * 16,
        "projected_full_state_h_action_seconds": full_h_seconds,
        "projected_full_state_current_seconds": full_current_seconds,
        "sectors": sectors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    started = time.perf_counter()
    rows = [benchmark_size(length) for length in SIZES]
    result = {
        "schema": "SCALABLE_RELATIONAL_BLOCK_KERNEL_BENCHMARK_V001",
        "classification": "RESOURCE_BENCHMARK_ONLY__NO_HISTORY_OUTPUT",
        "sizes": rows,
        "repeats": REPEATS,
        "maximum_benchmark_rows": MAX_BENCH_ROWS,
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "implementation_sha256": sha256(Path(__file__)),
        "protocol_sha256": sha256(HERE / "PROTOCOL.md"),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "claim_boundary": "TIMING_PROJECTION_ONLY__NO_PHYSICS_OR_SCALING_CLAIM",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    for row in rows:
        print(
            f"L={row['L']} D={row['exact_dimension']} "
            f"H={row['projected_full_state_h_action_seconds']:.6f}s "
            f"J={row['projected_full_state_current_seconds']:.6f}s"
        )
    print(f"wall={result['wall_seconds']:.3f}s rss={result['peak_rss_bytes']}")


if __name__ == "__main__":
    main()
