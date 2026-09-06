#!/usr/bin/env python3
"""Freeze and verify the bounded blind RK4 Richardson repair."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001"
FREEZE = HERE / "FROZEN_NUMERICAL_REPAIR.json"
OUT = HERE / "NUMERICAL_REPAIR_PREFLIGHT.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


frozen = json.loads(FREEZE.read_text())
paths = {
    "PROTOCOL.md": TARGET / "PROTOCOL.md",
    "compute_authenticated_history.py": TARGET / "compute_authenticated_history.py",
    "METHODOLOGY.md": HERE / "METHODOLOGY.md",
    "blind_history.py": HERE / "blind_history.py",
    "preflight.py": HERE / "preflight.py",
    "compare_seed.py": HERE / "compare_seed.py",
    "NUMERICAL_REPAIR.md": HERE / "NUMERICAL_REPAIR.md",
    "verify_numerical_repair.py": HERE / "verify_numerical_repair.py",
}
checks = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


for name, path in paths.items():
    check(digest(path) == frozen["current_files"][name], f"current hash {name}")
check(digest(HERE / "FROZEN_METHOD.json") == frozen["original_freeze_sha256"], "original freeze custody")
check(digest(HERE / "PREFLIGHT_RESULT.json") == frozen["original_preflight_sha256"], "original preflight custody")
check(
    digest(TARGET / "RAW_HISTORY" / "HISTORY_L4.json") == frozen["initial_outputs"]["target_L4"],
    "initial target L4 custody",
)
check(
    digest(HERE / "RAW_HISTORY" / "HISTORY_L4.json") == frozen["initial_outputs"]["blind_L4"],
    "initial blind L4 custody",
)
for length in (6, 8):
    check(not (TARGET / "RAW_HISTORY" / f"HISTORY_L{length}.json").exists(), f"no target L{length} before repair freeze")
    check(not (HERE / "RAW_HISTORY" / f"HISTORY_L{length}.json").exists(), f"no blind L{length} before repair freeze")

blind_source = (HERE / "blind_history.py").read_text()
check("16.0 * half - full" in blind_source, "Richardson combination present")
check("compute_authenticated_history" not in blind_source, "blind still does not import target")
check(frozen["repair_scope"] == "BLIND_NUMERICAL_PROPAGATOR_ONLY", "bounded repair scope")

failures = [row for row in checks if not row["passed"]]
result = {
    "schema": "AUTHENTICATED_ACCUMULATION_NUMERICAL_REPAIR_PREFLIGHT_V001",
    "verdict": "PASS_REPAIR_FROZEN_BEFORE_L6_L8" if not failures else "FAIL_REPAIR_FREEZE",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "claim_boundary": "BLIND_NUMERICAL_METHOD_REPAIR_ONLY__NO_PHYSICS_CHANGE",
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(result["verdict"])
print(f"checks {result['checks_passed']}/{result['checks_total']}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
