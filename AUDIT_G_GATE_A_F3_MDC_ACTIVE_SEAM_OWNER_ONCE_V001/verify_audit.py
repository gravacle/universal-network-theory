#!/usr/bin/env python3
"""Custody and anti-circularity checks for the hostile audit."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001"

EXPECTED = {
    "GLOBAL_OWNER_CENSUS.json": "a5d9cf29b209ed87156c4e42bade8f4498845cbedfb0bf73e6ac6b352142162e",
    "README.md": "d2ba95bfe30b007fd5af2b7c56c5a029f488d544fa5223eb181bc995082e7d64",
    "RESULT.md": "1c0589f17dee3af66c38074781f97480caa431f5e09151bd15e89a073853aa76",
    "THEOREM.md": "2313e53b0fe4d8b53d8049fce43c7b836ce8af909e03a190196ca2e3cf804adb",
    "verify_active_seam_owner_once.py": "c259476e50eac735ee6ef752cf523875b9333535f970974dc3413b2431714e5a",
}

checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


for name, digest in EXPECTED.items():
    check(hashlib.sha256((TARGET / name).read_bytes()).hexdigest() == digest,
          "custody " + name)

source = (HERE / "independent_reconstruction.py").read_text()
check("verify_active_seam_owner_once" not in source, "no target-verifier import")
check("subprocess" not in source, "reconstruction does not execute target")

run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True)
check("PASS_AFTER_REPAIR__" in run.stdout, "independent reconstruction ran")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_AFTER_REPAIR", "hostile disposition")
check(result["seam_current"] == "1/2", "current result")
check(result["gate_A"] == "OPEN" and result["gate_B"] == "UNAUTHORIZED",
      "scope ceiling")

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_AFTER_REPAIR", "equal branches", "Gate A remains open",
              "Gate B is unauthorized", "No Ward", "gravity"):
    check(token in report, "report token " + token)

print(f"PASS__HOSTILE_AUDIT_CUSTODY_AND_SCOPE__{checks}/{checks}")
