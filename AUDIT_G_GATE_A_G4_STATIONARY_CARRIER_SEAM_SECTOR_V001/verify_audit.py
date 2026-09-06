#!/usr/bin/env python3
"""Custody, independence, and fail-closed scope checks."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "DEVELOPMENT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001"
EXPECTED = {
    "OWNER_CENSUS_DELTA.json": "f8a246a65079a24910dfdf1569552b9cd8bb27bfd3d1dded92a44517b13952fd",
    "README.md": "1ebe2e60d52d4446a21249e99ee43ce5866f9ca234dc896a800ec72b39df5536",
    "RESULT.md": "628f4240b9fbaa9032cb58f19b56b104aef7a1e4b399090650366876a05272d6",
    "THEOREM.md": "166022c9b771759a708f6f559f486db1283fd74e027e4d27d8f99178575ec472",
    "verify_stationary_carrier_sector.py": "577f6591694dab2f6c1e97f3aa25e908bb4b4e5d116636f472925643f61a13ed",
}

checks = 0


def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


for name, digest in EXPECTED.items():
    check(hashlib.sha256((TARGET / name).read_bytes()).hexdigest() == digest,
          "target custody " + name)

source = (HERE / "independent_reconstruction.py").read_text()
check("verify_stationary_carrier_sector" not in source, "no target import")
run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True)
check("PASS_SECTOR_QUALIFIED__" in run.stdout, "independent run")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_SECTOR_QUALIFIED", "result disposition")
check(result["owner_delta_scope"] == "CARRIER_SECTOR_ONLY", "scope qualifier")
check(result["global_stationary_action"] == "OWNER_INCOMPLETE", "global fail closed")
check(result["gate_A"] == "OPEN" and result["gate_B"] == "UNAUTHORIZED",
      "gate ceiling")

delta = json.loads((TARGET / "OWNER_CENSUS_DELTA.json").read_text())
check(delta["scope"] == "carrier_sector_only", "target sector scope")
check(delta["global_stationary_action"] == "OWNER_INCOMPLETE", "target incomplete")
check(delta["physical_descent_residual"] == "UNDEFINED" and
      delta["physical_Ward_residual"] == "UNDEFINED", "undefined residuals")
check(len(delta["remaining_undefined"]) >= 9, "undefined owners retained")

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_SECTOR_QUALIFIED", "carrier_sector_only",
              "Gate A remains open", "Gate B remains unauthorized",
              "No Ward", "gravity"):
    check(token in report, "report token " + token)

print(f"PASS__G4_CARRIER_SECTOR_HOSTILE_AUDIT__{checks}/{checks}")
