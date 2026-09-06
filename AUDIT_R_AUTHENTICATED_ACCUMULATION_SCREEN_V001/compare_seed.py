#!/usr/bin/env python3
"""Post-output target/blind hostile comparison for the L4--L8 seed."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001"
FREEZE = HERE / "FROZEN_NUMERICAL_REPAIR.json"
POST = HERE / "POST_OUTPUT_FREEZE.json"
OUT = HERE / "HOSTILE_SEED_RESULT.json"
SIZES = (4, 6, 8)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


frozen = json.loads(FREEZE.read_text())
post = json.loads(POST.read_text())
checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


method_paths = {
    "PROTOCOL.md": TARGET / "PROTOCOL.md",
    "compute_authenticated_history.py": TARGET / "compute_authenticated_history.py",
    "METHODOLOGY.md": HERE / "METHODOLOGY.md",
    "blind_history.py": HERE / "blind_history.py",
    "preflight.py": HERE / "preflight.py",
    "compare_seed.py": HERE / "compare_seed.py",
}
for name, path in method_paths.items():
    check(digest(path) == frozen["current_files"][name], f"method custody {name}")

target_aggregate_path = TARGET / "HISTORY_SEED_RESULT.json"
blind_aggregate_path = HERE / "BLIND_SEED_RESULT.json"
output_paths = {
    "target_aggregate": target_aggregate_path,
    "blind_aggregate": blind_aggregate_path,
}
for length in SIZES:
    output_paths[f"target_L{length}"] = TARGET / "RAW_HISTORY" / f"HISTORY_L{length}.json"
    output_paths[f"blind_L{length}"] = HERE / "RAW_HISTORY" / f"HISTORY_L{length}.json"
for name, path in output_paths.items():
    check(path.is_file(), f"output exists {name}")
    if path.is_file():
        check(digest(path) == post["files"][name], f"output custody {name}")

target_aggregate = json.loads(target_aggregate_path.read_text())
blind_aggregate = json.loads(blind_aggregate_path.read_text())
check(target_aggregate["classification"] == blind_aggregate["classification"], "aggregate classification agreement")
check(target_aggregate["next_gate"] == blind_aggregate["next_gate"], "next-gate agreement")
check(target_aggregate["common_density_interval"] == blind_aggregate["common_density_interval"], "common interval exact agreement")

maxima = {"W_n": 0.0, "rho_bar": 0.0, "sector_weight": 0.0, "capacity": 0.0, "connector_l1": 0.0}
for length in SIZES:
    target = json.loads((TARGET / "RAW_HISTORY" / f"HISTORY_L{length}.json").read_text())
    blind = json.loads((HERE / "RAW_HISTORY" / f"HISTORY_L{length}.json").read_text())
    check(target["dimension"] == blind["dimension"] == 2 ** (2 * length), f"dimension L{length}")
    check(target["events"] == blind["events"] == 4 * length, f"event census L{length}")
    check(target["edges"] == blind["edges"] == 3 * length, f"owner census L{length}")
    check(target["connectors"] == blind["connectors"] == length, f"connector census L{length}")
    check(target["comparison"]["classification"] == blind["comparison"]["classification"], f"row classification L{length}")
    check(target["comparison"]["n_075"] == blind["comparison"]["n_075"], f"n075 L{length}")
    check(target["comparison"]["n_025"] == blind["comparison"]["n_025"], f"n025 L{length}")
    check(target["comparison"]["admissible_depletion_window"] == blind["comparison"]["admissible_depletion_window"], f"window Boolean L{length}")
    check(len(target["fine_rows"]) == len(blind["fine_rows"]) == 4 * length, f"complete event rows L{length}")
    for target_row, blind_row in zip(target["fine_rows"], blind["fine_rows"]):
        event = int(target_row["event"])
        check(event == int(blind_row["event"]), f"event label L{length}n{event}")
        for key in ("W_n", "rho_bar"):
            difference = rel(float(target_row[key]), float(blind_row[key]))
            maxima[key] = max(maxima[key], difference)
            check(difference <= 2.0e-7, f"{key} agreement L{length}n{event}", difference)
        sector_difference = float(np.max(np.abs(np.array(target_row["sector_weights"]) - np.array(blind_row["sector_weights"]))))
        maxima["sector_weight"] = max(maxima["sector_weight"], sector_difference)
        check(sector_difference <= 2.0e-7, f"sector agreement L{length}n{event}", sector_difference)
        connector_difference = rel(float(target_row["connector_delta_l1"]), float(blind_row["connector_delta_l1"]))
        maxima["connector_l1"] = max(maxima["connector_l1"], connector_difference)
        check(connector_difference <= 2.0e-6, f"connector agreement L{length}n{event}", connector_difference)
        check(float(target_row["event_residual_l1"]) <= 2.0e-7, f"target ledger L{length}n{event}")
        check(float(blind_row["event_residual_l1"]) <= 2.0e-7, f"blind ledger L{length}n{event}")
        check(math.isfinite(float(target_row["W_n"])) and math.isfinite(float(blind_row["W_n"])), f"finite write L{length}n{event}")
    target_capacity = np.array(target["comparison"]["capacity"], dtype=float)
    blind_capacity = np.array(blind["comparison"]["capacity"], dtype=float)
    capacity_difference = float(np.max(np.abs(target_capacity - blind_capacity)))
    maxima["capacity"] = max(maxima["capacity"], capacity_difference)
    check(capacity_difference <= 2.0e-7, f"capacity agreement L{length}", capacity_difference)
    if target["comparison"]["sector"] is not None and blind["comparison"]["sector"] is not None:
        for key in ("q_lower", "q_upper"):
            check(target["comparison"]["sector"][key] == blind["comparison"]["sector"][key], f"sector {key} L{length}")
        check(target["comparison"]["sector"]["density_interval"] == blind["comparison"]["sector"]["density_interval"], f"density interval L{length}")

classification = target_aggregate["classification"]
check(classification in {
    "SEED_ACCUMULATION_SECTOR_L4_L8",
    "NO_COMMON_ACCUMULATION_SECTOR_L4_L8",
    "UNRESOLVED_AUTHENTICATED_ACCUMULATION_SEED_L4_L8",
}, "declared finite classification")
check(target_aggregate["claim_boundary"]["not_claimed"] == ["CRITICAL_DENSITY", "Z_EQUALS_ONE", "CONTINUUM", "GRAVITY"], "target claim ceiling")

failures = [row for row in checks if not row["passed"]]
if failures:
    verdict = "FAIL_CLOSED_AUTHENTICATED_ACCUMULATION_SEED_AUDIT"
elif classification == "SEED_ACCUMULATION_SECTOR_L4_L8":
    verdict = "PASS_HOSTILE_SEED__AUTHORIZE_L10_L12_HISTORY"
else:
    verdict = "PASS_HOSTILE_NULL__HALT_BEFORE_L10_L12_AND_SPECTRUM"
result = {
    "schema": "AUTHENTICATED_ACCUMULATION_HOSTILE_SEED_AUDIT_V001",
    "verdict": verdict,
    "classification": classification,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "maximum_target_blind_differences": maxima,
    "mandated_next_gate": target_aggregate["next_gate"] if not failures else "HALT_FAILED_AUDIT",
    "claim_boundary": {
        "empirical": "FINITE_AUTHENTICATED_HISTORY_SEED_ONLY",
        "not_claimed": ["CRITICAL_DENSITY", "Z_EQUALS_ONE", "CONTINUUM", "METRIC", "EMERGENCE", "GRAVITY"],
    },
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(verdict)
print(f"checks {result['checks_passed']}/{result['checks_total']}")
for failure in failures:
    print("FAIL", failure["label"], failure["detail"])
if failures:
    raise SystemExit(1)
