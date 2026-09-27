#!/usr/bin/env python3
"""Binomial L6 array bounds only; this module cannot run numerical physics."""

from __future__ import annotations

import json
import math
from pathlib import Path


PACKET = Path(__file__).resolve().parent
LENGTH = 6


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def sector_bounds(q: int) -> dict[str, int]:
    if type(q) is not int or not 0 <= q <= LENGTH:
        raise ValueError("q must be an integer in 0..6")
    carrier = choose(2 * LENGTH, q)
    lineage = choose(LENGTH, q)
    actual_columns = 3 * lineage
    product_columns = 4 * (
        choose(LENGTH, q - 1) + lineage + choose(LENGTH, q + 1)
    )
    combined_columns = actual_columns + product_columns
    reduced_dimension = min(carrier, combined_columns)
    return {
        "q_out": q,
        "carrier_dimension": carrier,
        "lineage_dimension": lineage,
        "actual_factor_columns_bound": actual_columns,
        "product_factor_columns_bound": product_columns,
        "combined_factor_columns_bound": combined_columns,
        "raw_complex_factor_bytes_bound": 16 * carrier * combined_columns,
        "reduced_hermitian_bytes_bound": 16 * reduced_dimension * reduced_dimension,
    }


def static_report() -> dict[str, object]:
    sectors = [sector_bounds(q) for q in range(LENGTH + 1)]
    return {
        "schema": "UNT_L6_EVENT_ZERO_STATIC_ARRAY_BOUNDS_V001",
        "status": "STATIC_ONLY_NOT_RSS_WALL_POWER_OR_EXECUTION_ESTIMATE",
        "L": LENGTH,
        "event": 0,
        "sectors": sectors,
        "max_carrier_dimension": max(row["carrier_dimension"] for row in sectors),
        "max_combined_factor_columns_bound": max(
            row["combined_factor_columns_bound"] for row in sectors
        ),
        "max_raw_complex_factor_bytes_bound": max(
            row["raw_complex_factor_bytes_bound"] for row in sectors
        ),
        "max_reduced_hermitian_bytes_bound": max(
            row["reduced_hermitian_bytes_bound"] for row in sectors
        ),
        "omitted": [
            "Python_and_worker_overhead",
            "QR_BLAS_LAPACK_workspace",
            "solver_transport_workspace",
            "repeated_terminal_reconstruction",
            "filesystem_cache_and_checkpoint_io",
        ],
    }


def main() -> int:
    print(json.dumps(static_report(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
