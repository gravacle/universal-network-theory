#!/usr/bin/env python3
"""Allocation-free q0-q14 capacity certificate for the L14 scout.

The certificate changes only scheduler concurrency.  It does not execute a
numerical solve and it does not alter a Hamiltonian, sector, tolerance,
quadrature, Krylov, classifier, or emergence predicate.  Each sector is
charged the frozen Hostile recurrence allocation estimate, with the existing
per-worker capacity floor retained for smaller sectors.
"""

from __future__ import annotations

import argparse
import json
import math
from decimal import Decimal, InvalidOperation, ROUND_FLOOR
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence


COMPLEX128_BYTES = 16
LENGTH = 14
Q_VALUES = tuple(range(LENGTH + 1))
LEGACY_Q_SPECIFIC_FIELDS = frozenset(
    {
        "hostile_q9_columns",
        "hostile_q9_single_row_estimate_bytes",
    }
)


class CapacityRefusal(RuntimeError):
    """The declared machine geometry cannot produce a safe capacity plan."""


def hostile_row_estimate_bytes(length: int, q: int, allocation_vector_slots: int) -> int:
    """Return the frozen recurrence's allocation charge for one row."""

    if length < 1 or not 0 <= q <= 2 * length or allocation_vector_slots < 1:
        raise CapacityRefusal("invalid hostile row-capacity inputs")
    return allocation_vector_slots * COMPLEX128_BYTES * math.comb(2 * length, q)


def safe_worker_ceiling(memory_mib: int, fraction: Decimal, per_worker_bytes: int) -> int:
    """Floor the number of charged workers admitted by the memory budget."""

    if (
        memory_mib < 1
        or per_worker_bytes < 1
        or not fraction.is_finite()
        or not Decimal(0) < fraction < Decimal(1)
    ):
        raise CapacityRefusal("invalid worker-capacity inputs")
    available = Decimal(memory_mib * 1024 * 1024) * fraction
    return int((available / Decimal(per_worker_bytes)).to_integral_value(rounding=ROUND_FLOOR))


def _positive_int(config: Mapping[str, Any], key: str) -> int:
    raw = config.get(key)
    if isinstance(raw, bool):
        raise CapacityRefusal("{} must be a positive integer".format(key))
    try:
        value = int(raw)
    except (TypeError, ValueError) as error:
        raise CapacityRefusal("{} must be a positive integer".format(key)) from error
    if value < 1 or str(value) != str(raw).strip():
        # JSON integer values stringify exactly.  Reject floats such as 1.5
        # rather than silently truncating them; accept Decimal/string integers.
        try:
            if Decimal(str(raw)) != Decimal(value):
                raise CapacityRefusal("{} must be a positive integer".format(key))
        except Exception as error:
            if isinstance(error, CapacityRefusal):
                raise
            raise CapacityRefusal("{} must be a positive integer".format(key)) from error
    return value


def q_capacity_rows(
    *,
    length: int,
    allocation_vector_slots: int,
    base_worker_charge_bytes: int,
    requested_workers: int,
    physical_cores: int,
    memory_mib: int,
    memory_fraction: Decimal,
) -> list[Dict[str, Any]]:
    """Construct the complete deterministic sector/concurrency schedule."""

    if length < 1:
        raise CapacityRefusal("length must be positive")
    if min(
        allocation_vector_slots,
        base_worker_charge_bytes,
        requested_workers,
        physical_cores,
        memory_mib,
    ) < 1:
        raise CapacityRefusal("capacity inputs must be positive")
    if not memory_fraction.is_finite() or not Decimal(0) < memory_fraction < Decimal(1):
        raise CapacityRefusal("memory fraction must be in (0, 1)")
    memory_budget = int(
        (Decimal(memory_mib * 1024 * 1024) * memory_fraction).to_integral_value(
            rounding=ROUND_FLOOR
        )
    )
    rows: list[Dict[str, Any]] = []
    for q in range(length + 1):
        columns = math.comb(2 * length, q)
        recurrence_bytes = hostile_row_estimate_bytes(length, q, allocation_vector_slots)
        worker_charge = max(base_worker_charge_bytes, recurrence_bytes)
        memory_ceiling = safe_worker_ceiling(memory_mib, memory_fraction, worker_charge)
        concurrency = min(requested_workers, physical_cores, memory_ceiling)
        total_charge = concurrency * worker_charge
        limiting_factors = [
            label
            for label, value in (
                ("requested_workers", requested_workers),
                ("physical_cores", physical_cores),
                ("memory_budget", memory_ceiling),
            )
            if value == concurrency
        ]
        rows.append(
            {
                "q": q,
                "columns": columns,
                "allocation_vector_slots": allocation_vector_slots,
                "single_row_recurrence_estimate_bytes": recurrence_bytes,
                "base_worker_charge_bytes": base_worker_charge_bytes,
                "certified_worker_charge_bytes": worker_charge,
                "memory_worker_ceiling": memory_ceiling,
                "certified_concurrency": concurrency,
                "certified_concurrent_charge_bytes": total_charge,
                "memory_budget_headroom_bytes": memory_budget - total_charge,
                "limiting_factors": limiting_factors,
            }
        )
    return rows


def evaluate(config: Mapping[str, Any]) -> Dict[str, Any]:
    """Evaluate all q0-q14 sectors without allocating numerical arrays."""

    slots = _positive_int(config, "hostile_allocation_vector_slots")
    base_charge = _positive_int(config, "hostile_numerical_workspace_limit_bytes")
    requested_workers = _positive_int(config, "workers_per_branch")
    physical_cores = _positive_int(config, "physical_cores_per_instance")
    memory_mib = _positive_int(config, "observed_memory_mib_per_instance")
    try:
        fraction = Decimal(str(config["worker_memory_fraction_limit"]))
    except (KeyError, ValueError, InvalidOperation) as error:
        raise CapacityRefusal("worker_memory_fraction_limit must be decimal") from error
    if not fraction.is_finite() or not Decimal(0) < fraction < Decimal(1):
        raise CapacityRefusal("worker_memory_fraction_limit must be in (0, 1)")

    rows = q_capacity_rows(
        length=LENGTH,
        allocation_vector_slots=slots,
        base_worker_charge_bytes=base_charge,
        requested_workers=requested_workers,
        physical_cores=physical_cores,
        memory_mib=memory_mib,
        memory_fraction=fraction,
    )
    memory_budget = int(
        (Decimal(memory_mib * 1024 * 1024) * fraction).to_integral_value(
            rounding=ROUND_FLOOR
        )
    )
    legacy_fields = sorted(LEGACY_Q_SPECIFIC_FIELDS.intersection(config))
    checks = {
        "complete_q0_q14_sector_census": [row["q"] for row in rows] == list(Q_VALUES),
        "all_sector_dimensions_match_exact_combinatorics": all(
            row["columns"] == math.comb(2 * LENGTH, row["q"]) for row in rows
        ),
        "all_sector_charges_cover_frozen_recurrence_estimate": all(
            row["certified_worker_charge_bytes"]
            >= row["single_row_recurrence_estimate_bytes"]
            for row in rows
        ),
        "all_sectors_admit_at_least_one_worker": all(
            row["certified_concurrency"] >= 1 for row in rows
        ),
        "all_sector_concurrency_caps_respect_memory_budget": all(
            row["certified_concurrent_charge_bytes"] <= memory_budget for row in rows
        ),
        "all_sector_concurrency_caps_respect_worker_and_core_limits": all(
            row["certified_concurrency"] <= min(requested_workers, physical_cores)
            for row in rows
        ),
        "configuration_has_no_q_specific_capacity_certificate": not legacy_fields,
    }
    return {
        "schema": "L14_Q_AWARE_CAPACITY_PLAN_V003",
        "classification": (
            "PASS_ALLOCATION_FREE_Q0_Q14_CAPACITY_CERTIFICATE__NO_NUMERICAL_EXECUTION"
            if all(checks.values())
            else "FAIL_CLOSED_Q0_Q14_CAPACITY_CERTIFICATE"
        ),
        "length": LENGTH,
        "q_min": Q_VALUES[0],
        "q_max": Q_VALUES[-1],
        "sector_count": len(rows),
        "complex128_bytes": COMPLEX128_BYTES,
        "allocation_vector_slots": slots,
        "base_worker_charge_bytes": base_charge,
        "instance_memory_mib": memory_mib,
        "worker_memory_fraction_limit": str(fraction),
        "memory_budget_bytes": memory_budget,
        "requested_workers": requested_workers,
        "physical_cores": physical_cores,
        "minimum_certified_concurrency": min(
            row["certified_concurrency"] for row in rows
        ),
        "legacy_q_specific_fields": legacy_fields,
        "sectors": rows,
        "checks": checks,
        "scheduler_effect": "CONCURRENCY_ONLY__Q_AWARE_MEMORY_ADMISSION",
        "physics_changes": [],
        "claim_boundary": (
            "RESOURCE_ARITHMETIC_AND_SCHEDULER_CONCURRENCY_ONLY__DOES_NOT_CHANGE_"
            "PHYSICS_SECTORS_TOLERANCES_QUADRATURE_KRYLOV_CLASSIFICATION_OR_EMERGENCE_"
            "PREDICATES__DOES_NOT_EXECUTE_OR_PROVE_L14_PHYSICS"
        ),
    }


def main(argv: Sequence[str] = ()) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("AWS_RUN_CONFIG.example.json"),
    )
    arguments = parser.parse_args(argv or None)
    config = json.loads(arguments.config.read_text(encoding="utf-8"))
    result = evaluate(config)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["classification"].startswith("PASS_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
