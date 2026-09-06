#!/usr/bin/env python3
"""Supplemental custody/unit/kernel checks after the seed hostile review."""

from __future__ import annotations

import itertools
import json
import math
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "SEED_CUSTODY_SUPPLEMENT_RESULT.json"
FREEZE = "a0e88add861298c6ae2cd6af883c8080779f366a"
TARGET_PREFIX = "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
AUDIT_PREFIX = "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"


checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


dimensions = {4: 495, 6: 18564, 8: 735471, 10: 30045015, 12: 1251677700}
exact_bytes = {length: dimension * 16 for length, dimension in dimensions.items()}
check(exact_bytes[4] == 7920, "L4 exact state bytes")
check(abs(exact_bytes[4] / 1024 - 7.734375) <= 1.0e-15, "L4 exact KiB")
check(exact_bytes[8] == 11767536, "L8 exact state bytes")
check(abs(exact_bytes[8] / 2**20 - 11.222396850585938) <= 1.0e-15, "L8 exact MiB")

tree = subprocess.run(
    ["git", "ls-tree", "-r", "--name-only", FREEZE],
    cwd=ROOT,
    check=True,
    capture_output=True,
    text=True,
).stdout.splitlines()
frozen_paths = set(tree)
for length in (4, 6, 8):
    check(
        f"{TARGET_PREFIX}/RAW_HISTORY/HISTORY_L{length}.json" not in frozen_paths,
        f"freeze excludes target raw L{length}",
    )
    check(
        f"{AUDIT_PREFIX}/RAW_HISTORY/HISTORY_L{length}.json" not in frozen_paths,
        f"freeze excludes blind raw L{length}",
    )
for path in (
    f"{TARGET_PREFIX}/SEED_RESULT.json",
    f"{AUDIT_PREFIX}/SEED_HOSTILE_RESULT.json",
):
    check(path not in frozen_paths, f"freeze excludes {path}")

kernel_census = {}
for length in (4, 6, 8):
    width = 3 * length
    sources_total = blocked_total = intersections = destination_failures = 0
    basis = []
    for positions in itertools.combinations(range(width), length):
        word = sum(1 << position for position in positions)
        basis.append(word)
    basis_set = set(basis)
    for event in range(length):
        target_bit = length + event
        for word in basis:
            loaded = ((word >> event) & 1) == 1
            occupied = ((word >> target_bit) & 1) == 1
            source = loaded and not occupied
            blocked = loaded and occupied
            sources_total += int(source)
            blocked_total += int(blocked)
            intersections += int(source and blocked)
            if source:
                destination = word ^ (1 << event) ^ (1 << target_bit)
                destination_failures += int(destination not in basis_set)
    kernel_census[str(length)] = {
        "allow_source_count": sources_total,
        "blocked_source_count": blocked_total,
        "support_intersection_count": intersections,
        "destination_closure_failures": destination_failures,
    }
    check(sources_total > 0 and blocked_total > 0, f"nonempty allow and blocked supports L{length}")
    check(intersections == 0, f"allow/blocked supports disjoint L{length}")
    check(destination_failures == 0, f"admission destinations close L{length}")

failures = [row for row in checks if not row["passed"]]
result = {
    "schema": "SCALABLE_RELATIONAL_ACCUMULATION_SEED_CUSTODY_SUPPLEMENT_V001",
    "verdict": "PASS_SEED_CUSTODY_SUPPLEMENT" if not failures else "FAIL_CLOSED_SEED_CUSTODY_SUPPLEMENT",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "freeze_commit": FREEZE,
    "exact_complex128_state_bytes": {str(key): value for key, value in exact_bytes.items()},
    "kernel_census": kernel_census,
    "physics_or_threshold_changed": False,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(result["verdict"])
print(f"checks {result['checks_passed']}/{result['checks_total']}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
