#!/usr/bin/env python3
"""Compare the frozen independent L<=8 Krylov output with sealed references."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FREEZE = HERE / "FROZEN_METHOD.json"
INDEPENDENT = HERE / "INDEPENDENT_VALIDATION.json"
TARGET_PROTOCOL = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "PROTOCOL.md"
TARGET_RESULT = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json"
OUT = HERE / "VALIDATION_AUDIT.json"
EXPECTED_TARGET_PROTOCOL_SHA256 = "3da9e74b0dcc2d8b65ce98cfb42735864cf3d045e41655082baa7a7a295cb334"
EXPECTED_TARGET_RESULT_SHA256 = "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05"
EXPECTED_ROWS = ((4, 2), (6, 3), (8, 4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


freeze = json.loads(FREEZE.read_text())
independent = json.loads(INDEPENDENT.read_text())
target = json.loads(TARGET_RESULT.read_text())
checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"label": label, "passed": bool(condition), "detail": detail})


check(sha256(TARGET_PROTOCOL) == EXPECTED_TARGET_PROTOCOL_SHA256, "sealed protocol hash")
check(sha256(TARGET_RESULT) == EXPECTED_TARGET_RESULT_SHA256, "sealed result hash")
for filename in ("METHODOLOGY.md", "independent_centerline.py", "verify_validation.py"):
    path = HERE / filename
    check(
        sha256(path) == freeze["files"][filename]["sha256"],
        f"frozen hash {filename}",
    )

source = (HERE / "independent_centerline.py").read_text()
check("DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001" not in source, "no target extended module path")
check("DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" not in source, "no sealed target result path")
check("importlib" not in source and "sys.path" not in source, "no dynamic target import")
check("np.zeros((dimension, dimension" not in source, "no dense physical block constructor")

check(independent["scope"] == "L4_Q2__L6_Q3__L8_Q4_VALIDATION_ONLY", "validation-only scope")
check(independent["new_rows_executed"] == [], "no new rows executed")
check(independent["all_rows_resolved"] is True, "all independent rows resolved")
check(independent["methodology_sha256"] == freeze["files"]["METHODOLOGY.md"]["sha256"], "result method hash")
check(independent["implementation_sha256"] == freeze["files"]["independent_centerline.py"]["sha256"], "result implementation hash")

independent_rows = {(int(row["L"]), int(row["q"])): row for row in independent["rows"]}
target_rows = {
    (int(row["L"]), int(row["q"])): row
    for length_rows in target["sector_rows"].values()
    for row in length_rows
}
check(tuple(sorted(independent_rows)) == EXPECTED_ROWS, "exact validation row set")

raw_paths = sorted((HERE / "RAW_VALIDATION").glob("ROW_L*_Q*.json"))
check(len(raw_paths) == len(EXPECTED_ROWS), "exact raw output count", len(raw_paths))
for pair in EXPECTED_ROWS:
    length, charge = pair
    raw_path = HERE / "RAW_VALIDATION" / f"ROW_L{length}_Q{charge}.json"
    check(raw_path.exists(), f"raw row exists L{length}q{charge}")
    if raw_path.exists():
        check(json.loads(raw_path.read_text()) == independent_rows[pair], f"raw row matches aggregate L{length}q{charge}")

comparison_limits = {
    "ground_energy": 2.0e-8,
    "Delta_act": 2.0e-8,
    "chi_tau": 5.0e-7,
    "R_low": 5.0e-6,
}
max_differences = {key: 0.0 for key in comparison_limits}
for pair in EXPECTED_ROWS:
    length, charge = pair
    row = independent_rows[pair]
    reference = target_rows[pair]
    check(row["status"] == "RESOLVED", f"row resolved L{length}q{charge}", row["failures"])
    check(row["rho"] == 0.25, f"rho centerline L{length}q{charge}")
    check(row["sector_dimension"] == math.comb(2 * length, charge), f"sector dimension L{length}q{charge}")
    check(row["structural_controls"]["owner_edges"] == 3 * length, f"owner census L{length}q{charge}")
    check(row["structural_controls"]["unique_edges"] == 3 * length, f"unique owners L{length}q{charge}")
    check(all(value == 3 for value in row["structural_controls"]["degrees"]), f"degree three L{length}q{charge}")
    check(row["structural_controls"]["bipartite_edges"] is True, f"bipartite control L{length}q{charge}")
    check(row["structural_controls"]["one_carrier_band_linf"] <= 1.0e-12, f"one-carrier bands L{length}q{charge}")
    check(row["ground_block_hermiticity_error"] <= 1.0e-12, f"ground Hermiticity L{length}q{charge}")
    check(row["response_block_hermiticity_error"] <= 1.0e-12, f"response Hermiticity L{length}q{charge}")
    check(row["ground_residual"] <= 1.0e-9, f"ground residual L{length}q{charge}")
    check(row["active_actual_residual"] <= 1.0e-9, f"active residual L{length}q{charge}")
    check(row["ground_krylov_orthogonality_error"] <= 1.0e-10, f"ground orthogonality L{length}q{charge}")
    check(row["response_krylov_orthogonality_error"] <= 1.0e-10, f"response orthogonality L{length}q{charge}")
    check(row["response_projection_error"] <= 1.0e-9, f"projection closure L{length}q{charge}")
    check(row["response_momentum_covariance_error"] <= 1.0e-9, f"momentum covariance L{length}q{charge}")
    check(row["threshold_stable"] is True, f"threshold stability L{length}q{charge}")
    check(row["total_matvecs"] <= 2000, f"matvec guard L{length}q{charge}")
    check(row["wall_seconds"] <= 3 * 60 * 60, f"wall guard L{length}q{charge}")
    check(row["peak_rss_bytes"] <= 16 * (1 << 30), f"RSS guard L{length}q{charge}")
    for sequence_name in ("ground_sequence", "response_sequence"):
        sequence = row[sequence_name]
        check(bool(sequence), f"{sequence_name} present L{length}q{charge}")
        if sequence:
            count = min(5, int(sequence[-1]["krylov_dimension"]))
            check(
                len(sequence[-1]["lowest_five_ritz_values"]) == count,
                f"lowest five reported {sequence_name} L{length}q{charge}",
            )
    for key, limit in comparison_limits.items():
        difference = relative_difference(float(row[key]), float(reference[key]))
        max_differences[key] = max(max_differences[key], difference)
        check(difference <= limit, f"reference agreement {key} L{length}q{charge}", difference)

future_outputs = sorted(
    path.name
    for path in (HERE / "RAW_VALIDATION").glob("ROW_L*_Q*.json")
    if path.name.startswith(("ROW_L10_", "ROW_L12_"))
)
check(not future_outputs, "no L10/L12 raw output", future_outputs)

failures = [row for row in checks if not row["passed"]]
result = {
    "schema": "EXTENDED_CENTERLINE_VALIDATION_AUDIT_V001",
    "verdict": (
        "PASS_READY_FOR_SEMANTIC_GATE__NO_L10_L12_EXECUTED"
        if not failures
        else "FAIL_NOT_READY"
    ),
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "max_relative_reference_differences": max_differences,
    "independent_result_sha256": sha256(INDEPENDENT),
    "frozen_method_sha256": sha256(FREEZE),
    "claim_boundary": {
        "ready": "BLIND_SPARSE_ADAPTIVE_KRYLOV_METHOD_VALIDATED_THROUGH_L8",
        "new_rows_executed": [],
        "not_claimed": ["L10", "L12", "Z_EQUALS_ONE", "CONTINUUM", "GRAVITY"],
    },
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(result["verdict"])
print(f"checks {result['checks_passed']}/{result['checks_total']}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure.get("detail"))
    raise SystemExit(1)
