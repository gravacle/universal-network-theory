#!/usr/bin/env python3
"""Hostile verifier for the fail-closed L4 accumulation obstruction."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001"
OUT = HERE / "FINAL_HOSTILE_RESULT.json"

EXPECTED = {
    "protocol": "95db90a5fbf18d4a76495e29633c9a2db081e328e9395da4333a75f76c03f127",
    "target_L4": "d377484624723dedf62265f8875d267eb3185c3ba4fa8278a8b576c2d93ad60b",
    "blind_L4": "655cbed5b2ab2602c16d27c652ee729058d7e3ce88aa39c646080843a2114c83",
    "adjudication_method": "7fb6c742bb293c487d42036c05893e5ca1f82ad7e567c700697d76471ff82e9b",
    "adjudication_code": "b0e6de0b03d670f042bd878983b8b96a0f030f6caceaf27e63c06677627675a0",
    "adjudication_result": "a4696500f455e6f607763793859dcf85b2800cc8ca26ae4ea7ab86389e4eb4c1",
    "target_result_json": "fc1d43f7ddb94e5682932440800aa147a0784e2d8e836a9803b7582ee73f3c43",
    "target_result_md": "57ca9a9f290462bf7f1d217a225a12699b33560563b2d6690442951e52a3b36e",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = {
    "protocol": TARGET / "PROTOCOL.md",
    "target_L4": TARGET / "RAW_HISTORY" / "HISTORY_L4.json",
    "blind_L4": HERE / "RAW_HISTORY" / "HISTORY_L4.json",
    "adjudication_method": HERE / "ADJUDICATION_METHOD.md",
    "adjudication_code": HERE / "adjudicate_l4_negative_write.py",
    "adjudication_result": HERE / "L4_SIGN_ADJUDICATION.json",
    "target_result_json": TARGET / "RESULT.json",
    "target_result_md": TARGET / "RESULT.md",
}
checks = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


for name, path in paths.items():
    check(path.is_file(), f"file exists {name}")
    if path.is_file():
        check(digest(path) == EXPECTED[name], f"hash {name}")

protocol = (TARGET / "PROTOCOL.md").read_text()
target = json.loads((TARGET / "RAW_HISTORY" / "HISTORY_L4.json").read_text())
blind = json.loads((HERE / "RAW_HISTORY" / "HISTORY_L4.json").read_text())
adjudication = json.loads((HERE / "L4_SIGN_ADJUDICATION.json").read_text())
result = json.loads((TARGET / "RESULT.json").read_text())
human = (TARGET / "RESULT.md").read_text()

check("the first three `W_n` are positive above error" in protocol, "frozen first-three-positive prerequisite")
check("No result-dependent" in protocol, "no result-dependent schedule")
check(target["comparison"]["classification"] == "NO_BOUNDED_DEPLETION_WINDOW_L", "target L4 classification")
check(blind["comparison"]["classification"] == "UNRESOLVED_HISTORY_L", "blind guard retained unresolved")
check(float(blind["comparison"]["coarse_fine"]["maximum_disagreement"]) <= 2.0e-7, "blind observables converge")
check(max(float(row["norm_error"]) for row in blind["fine_rows"]) > 1.0e-10, "blind norm guard really fails")
check(max(float(row["norm_error"]) for row in blind["fine_rows"]) < 1.5e-10, "blind norm miss bounded")

direct_writes = [float(value) for value in adjudication["writes"]]
target_writes = [float(target["fine_rows"][index]["W_n"]) for index in range(3)]
blind_writes = [float(blind["fine_rows"][index]["W_n"]) for index in range(3)]
check(all(math.isfinite(value) for value in direct_writes + target_writes + blind_writes), "finite first-three writes")
check(direct_writes[0] > 0 and direct_writes[1] > 0, "first two writes positive")
check(direct_writes[2] < 0, "third write negative")
check(float(adjudication["W3_upper_bound"]) < -1.0e-6, "negative sign certified beyond guard")
check(max(abs(direct_writes[index] - target_writes[index]) for index in range(3)) <= 1.0e-10, "direct-target first-three agreement")
check(max(abs(direct_writes[index] - blind_writes[index]) for index in range(3)) <= 1.0e-10, "direct-blind first-three agreement")
check(adjudication["classification"] == "CONFIRMED_NEGATIVE_W3__FAIL_CLOSED_HISTORY", "adjudication classification")
check(all(bool(value) for value in adjudication["checks"].values()), "all adjudication controls")
check(len(adjudication["checks"]) == 8, "exact adjudication check census")

for packet in (TARGET, HERE):
    for length in (6, 8, 10, 12):
        check(not (packet / "RAW_HISTORY" / f"HISTORY_L{length}.json").exists(), f"no forbidden larger history {packet.name} L{length}")
check(not (TARGET / "SPECTRAL_RESULT.json").exists(), "no spectral result")
check(not (HERE / "SPECTRAL_HOSTILE_RESULT.json").exists(), "no spectral audit result")

check(result["classification"] == "NO_COMMON_ACCUMULATION_SECTOR_L4_L12", "final target classification")
check(result["mandated_next_gate"] == "HALT__DO_NOT_RUN_L6_L8_L10_L12_OR_SPECTRAL_INTERVAL_SWEEP", "final target halt")
check(result["executed_sizes"] == [4], "exact executed size census")
check(len(result["not_executed"]) == 7, "downstream non-execution census")
check("not evidence that native record accumulation is impossible" in human, "bounded history interpretation")
check("No grid, graviton, Ward axiom, continuum assumption, Gate B promotion" in human, "human claim ceiling")
check("gravity" in result["claim_boundary"]["not_claimed"][-1].lower(), "machine gravity ceiling")

failures = [row for row in checks if not row["passed"]]
verdict = (
    "PASS_HOSTILE_L4_NEGATIVE_WRITE_OBSTRUCTION__NO_COMMON_SECTOR__HALT"
    if not failures
    else "FAIL_CLOSED_FINAL_HALT_AUDIT"
)
audit = {
    "schema": "AUTHENTICATED_ACCUMULATION_FINAL_HOSTILE_AUDIT_V001",
    "verdict": verdict,
    "classification": result["classification"],
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "W3": direct_writes[2],
    "W3_upper_bound": float(adjudication["W3_upper_bound"]),
    "maximum_three_method_write_disagreement": max(
        abs(a[index] - b[index])
        for a, b in (
            (direct_writes, target_writes),
            (direct_writes, blind_writes),
            (target_writes, blind_writes),
        )
        for index in range(3)
    ),
    "logical_result": "L4_PREREQUISITE_FALSE_IMPLIES_NO_COMMON_L4_L12_SECTOR",
    "mandated_next_gate": result["mandated_next_gate"] if not failures else "HALT_FAILED_AUDIT",
    "claim_boundary": {
        "proved": "DECLARED_L4_FIRST_THREE_POSITIVE_WRITE_BOOLEAN_FALSE",
        "not_claimed": ["GENERIC_ACCUMULATION_NULL", "Z_EQUALS_ONE_OR_NOT", "CONTINUUM", "EMERGENCE", "GRAVITY"],
    },
}
OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
print(verdict)
print(f"checks {audit['checks_passed']}/{audit['checks_total']}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
