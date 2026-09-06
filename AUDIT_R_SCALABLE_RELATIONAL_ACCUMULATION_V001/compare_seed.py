#!/usr/bin/env python3
"""Compare independent L4/L6/L8 relational accumulation histories."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
OUT = HERE / "SEED_HOSTILE_RESULT.json"
SIZES = (4, 6, 8)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


target_rows = []
blind_rows = []
maximum_disagreement = 0.0
for length in SIZES:
    target_path = TARGET / "RAW_HISTORY" / f"HISTORY_L{length}.json"
    blind_path = HERE / "RAW_HISTORY" / f"HISTORY_L{length}.json"
    check(target_path.is_file(), f"target exists L{length}")
    check(blind_path.is_file(), f"blind exists L{length}")
    target = json.loads(target_path.read_text())
    blind = json.loads(blind_path.read_text())
    target_rows.append(target)
    blind_rows.append(blind)
    check(target["L"] == blind["L"] == length, f"L identity {length}")
    check(target["dimension"] == blind["dimension"], f"dimension {length}")
    check(target["comparison"]["resolved"], f"target resolved {length}")
    check(blind["comparison"]["resolved"], f"blind resolved {length}")
    check(len(target["rows"]) == len(blind["rows"]) == length, f"event census {length}")
    for event, (left, right) in enumerate(zip(target["rows"], blind["rows"]), start=1):
        for key in ("W_n", "allow_probability", "blocked_probability", "reverse_support_probability", "connector_delta_l1", "connector_delta_signed", "q_retained_after_transport", "q_genesis_after"):
            difference = abs(float(left[key]) - float(right[key]))
            maximum_disagreement = max(maximum_disagreement, difference)
            check(difference <= 1.0e-8, f"{key} L{length} n{event}", difference)
        sector_difference = float(np.max(np.abs(np.array(left["sector_weights"]) - np.array(right["sector_weights"]))))
        maximum_disagreement = max(maximum_disagreement, sector_difference)
        check(sector_difference <= 1.0e-8, f"sector weights L{length} n{event}", sector_difference)
    target_sector = target["comparison"]["sector"]
    blind_sector = blind["comparison"]["sector"]
    check(target_sector["q_lower"] == blind_sector["q_lower"], f"q lower L{length}")
    check(target_sector["q_upper"] == blind_sector["q_upper"], f"q upper L{length}")
    check(max(float(row["blocked_probability"]) for row in target["rows"]) > 1.0e-6, f"nonvacuous target blocking L{length}")
    check(min(float(row["W_n"]) for row in target["rows"]) >= -target["comparison"]["epsilon"], f"nonnegative target W L{length}")

sealed = json.loads((ROOT / "DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001" / "TRACE_L4.json").read_text())
for event in range(4):
    check(abs(float(target_rows[0]["rows"][event]["W_n"]) - float(sealed["rows"][event]["W_n"])) <= 1.0e-9, f"sealed L4 W n{event + 1}")
    check(abs(float(target_rows[0]["rows"][event]["blocked_probability"]) - float(sealed["rows"][event]["blocked_probability"])) <= 1.0e-9, f"sealed L4 blocked n{event + 1}")


def intersection(rows: list[dict[str, object]]) -> list[float] | None:
    lower = max(float(row["comparison"]["sector"]["density_interval"][0]) for row in rows)
    upper = min(float(row["comparison"]["sector"]["density_interval"][1]) for row in rows)
    return [lower, upper] if lower < upper else None


target_interval = intersection(target_rows)
blind_interval = intersection(blind_rows)
check((target_interval is None) == (blind_interval is None), "common interval existence")
if target_interval is not None and blind_interval is not None:
    check(max(abs(a - b) for a, b in zip(target_interval, blind_interval)) <= 1.0e-12, "common interval agreement")

failures = [row for row in checks if not row["passed"]]
if failures:
    classification = "FAIL_CLOSED_RELATIONAL_ACCUMULATION_SEED_AUDIT"
    next_gate = "HALT_FAILED_AUDIT"
elif target_interval is None:
    classification = "NO_COMMON_RELATIONAL_ACCUMULATION_SECTOR_L4_L8"
    next_gate = "HALT_BEFORE_L10_L12_AND_SPECTRUM"
else:
    classification = "PASS_RELATIONAL_ACCUMULATION_SEED_L4_L8"
    next_gate = "FREEZE_L10_L12_HISTORY_METHODS"

result = {
    "schema": "SCALABLE_RELATIONAL_ACCUMULATION_SEED_HOSTILE_V001",
    "classification": classification,
    "next_gate": next_gate,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "maximum_target_blind_disagreement": maximum_disagreement,
    "target_common_density_interval": target_interval,
    "blind_common_density_interval": blind_interval,
    "target_hashes": {str(length): digest(TARGET / "RAW_HISTORY" / f"HISTORY_L{length}.json") for length in SIZES},
    "blind_hashes": {str(length): digest(HERE / "RAW_HISTORY" / f"HISTORY_L{length}.json") for length in SIZES},
    "claim_boundary": {"empirical": "FINITE_L4_L8_RELATIONAL_SEED_ONLY", "not_claimed": ["CRITICALITY", "Z_EQUALS_ONE", "CONTINUUM", "EMERGENCE", "GRAVITY"]},
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(classification)
print(f"checks {result['checks_passed']}/{result['checks_total']}")
print("maximum disagreement", maximum_disagreement)
print("common interval", target_interval)
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
