#!/usr/bin/env python3
"""Read-only feasibility arithmetic for the exact L14 scout mass ledger.

The frozen prefix history stores a q shard with shape

    binomial(prefix, q) x binomial(2L, q)

in complex128.  Admission is lower triangular in q: output q depends on the
old q and q-1 shards.  Consequently an exact requested ceiling q_max requires
every shard q=0,...,q_max; starting directly at q=4 would delete physical
paths.  This script records the resulting storage lower bounds without
allocating any numerical state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LENGTH = 14
SCRATCH_LIMIT_BYTES = 20 * 2**30
SCHEMA = "L14_EXACT_MASS_LEDGER_FEASIBILITY_V001"
SHAPE_SOURCE = (
    ROOT
    / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "compute_prefix_history_v004.py"
)
PROTOCOL_SOURCE = (
    ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "PROTOCOL.md"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def state_bytes(length: int, prefix: int, maximum_q: int) -> int:
    return 16 * sum(
        math.comb(prefix, q) * math.comb(2 * length, q)
        for q in range(min(prefix, maximum_q) + 1)
    )


def exact_prefix_case(maximum_q: int) -> dict[str, Any]:
    previous = state_bytes(LENGTH, LENGTH - 2, maximum_q)
    terminal = state_bytes(LENGTH, LENGTH - 1, maximum_q)
    peak_lower_bound = previous + terminal
    return {
        "requested_q_max": maximum_q,
        "required_q_shards": list(range(maximum_q + 1)),
        "reason": "ADMISSION_OUTPUT_Q_DEPENDS_ON_OLD_Q_AND_Q_MINUS_1",
        "prefix_12_bytes": previous,
        "prefix_13_bytes": terminal,
        "admission_peak_lower_bound_bytes": peak_lower_bound,
        "admission_peak_lower_bound_gib": peak_lower_bound / 2**30,
        "frozen_scratch_limit_bytes": SCRATCH_LIMIT_BYTES,
        "fits_frozen_scratch_limit": peak_lower_bound <= SCRATCH_LIMIT_BYTES,
    }


def translation_orbit_count(length: int, q: int) -> int:
    """Burnside count for simultaneous cyclic translation of both rails."""

    fixed_sum = 0
    for shift in range(length):
        cycles_per_rail = math.gcd(length, shift)
        cycle_length = length // cycles_per_rail
        if q % cycle_length == 0:
            selected_cycles = q // cycle_length
            if selected_cycles <= 2 * cycles_per_rail:
                fixed_sum += math.comb(2 * cycles_per_rail, selected_cycles)
    if fixed_sum % length:
        raise AssertionError("Burnside sum is not divisible by group order")
    return fixed_sum // length


def spectrum_structure(q: int) -> dict[str, Any]:
    words = math.comb(2 * LENGTH, q)
    orbits = translation_orbit_count(LENGTH, q)
    return {
        "q": q,
        "fixed_charge_words": words,
        "translation_orbits": orbits,
        "full_word_lookup_int32_bytes": 4 * 2 ** (2 * LENGTH),
        "two_128_vector_krylov_banks_upper_bytes": 2 * 128 * orbits * 16,
        "two_csr_coo_capacity_upper_bytes": 2 * orbits * (3 * LENGTH) * 24,
        "note": "STRUCTURAL_UPPER_ARITHMETIC_ONLY__NOT_A_RUNTIME_OR_RSS_GUARANTEE",
    }


def build_report() -> dict[str, Any]:
    filesystem = os.statvfs(HERE)
    available = int(filesystem.f_bavail * filesystem.f_frsize)
    phase1 = exact_prefix_case(7)
    phase3 = exact_prefix_case(9)
    full = exact_prefix_case(LENGTH - 1)
    return {
        "schema": SCHEMA,
        "classification": "CURRENT_EXACT_PREFIX_REPRESENTATION_OBSTRUCTED_FOR_L14_SCOUT",
        "L": LENGTH,
        "phase1_q4_through_q7_mass": phase1,
        "phase3_q8_q9_mass": phase3,
        "full_history": full,
        "observed_filesystem_available_bytes": available,
        "phase1_obstruction": (
            "EXACT_Q4_Q7_MASS_REQUIRES_Q0_Q7_AND_EXCEEDS_FROZEN_SCRATCH_GUARD"
        ),
        "phase3_obstruction": (
            "EXACT_Q8_Q9_MASS_REQUIRES_Q0_Q9_AND_EXCEEDS_BOTH_FROZEN_SCRATCH_"
            "GUARD_AND_OBSERVED_FREE_STORAGE"
            if phase3["admission_peak_lower_bound_bytes"] > available
            else "EXACT_Q8_Q9_MASS_REQUIRES_Q0_Q9_AND_EXCEEDS_FROZEN_SCRATCH_GUARD"
        ),
        "spectrum_sector_structure": [spectrum_structure(q) for q in range(4, 10)],
        "source": {
            "shape_source_path": str(SHAPE_SOURCE.resolve()),
            "shape_source_sha256": sha256_file(SHAPE_SOURCE),
            "protocol_path": str(PROTOCOL_SOURCE.resolve()),
            "protocol_sha256": sha256_file(PROTOCOL_SOURCE),
            "implementation_sha256": sha256_file(Path(__file__)),
        },
        "decision": (
            "DO_NOT_LAUNCH_L14_SCOUT_WITH_CURRENT_MASS_ENGINE__"
            "REQUIRE_VALIDATED_COMPACT_MASS_REPRESENTATION_OR_REVISED_EXPLORATORY_GATE"
        ),
        "claim_boundary": "RESOURCE_AND_DEPENDENCY_ARITHMETIC_ONLY__NO_L14_NUMERICAL_RESULT",
    }


def owner_once_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        payload = (
            json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            if written <= 0:
                raise RuntimeError("owner-once write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
    finally:
        os.close(descriptor)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(list(argv) if argv is not None else None)
    report = build_report()
    for label in (
        "phase1_q4_through_q7_mass",
        "phase3_q8_q9_mass",
        "full_history",
    ):
        row = report[label]
        print(
            f"L14_MASS_FEASIBILITY case={label} q_max={row['requested_q_max']} "
            f"peak_gib={row['admission_peak_lower_bound_gib']:.6f} "
            f"fits_frozen_guard={str(row['fits_frozen_scratch_limit']).lower()}"
        )
    print(f"L14_MASS_FEASIBILITY_DECISION {report['decision']}")
    if arguments.output is not None:
        owner_once_json(arguments.output.resolve(), report)
        print(f"L14_MASS_FEASIBILITY_OUTPUT {arguments.output.resolve()}")
    return 20


if __name__ == "__main__":
    raise SystemExit(main())
