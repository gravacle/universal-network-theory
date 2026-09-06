#!/usr/bin/env python3
"""Custody and scope verifier for the hostile join-screen audit."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "DEVELOPMENT_G_GATE_A_SAME_PARENT_OWNER_JOIN_SCREEN_V001"
EXPECTED = {
    "README.md": "dfb724d5a17f61013ed4c90fe98c62d0bf5860599ede57e82cc3724b2ec9f33b",
    "RESULT.json": "cec6871e32f9def26fe550618a3ce527fa246adbb3adc4ef51e6906abc385249",
    "THEOREM.md": "31d88353d895aaa5d68cf4ccc4e2965573cb4c24c065386fe02f25a90982b97e",
    "verify_same_parent_join_screen.py": "181c486f63fc0f30b60f189cd4862efac55d89efc1a3c7b41fb19c2597c307b5",
}
checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


for name, digest in EXPECTED.items():
    check(hashlib.sha256((TARGET / name).read_bytes()).hexdigest() == digest,
          "target custody " + name)

source = (HERE / "independent_reconstruction.py").read_text()
check("verify_same_parent_join_screen" not in source, "no target verifier import")
run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True)
check("PASS_AFTER_REPAIR__" in run.stdout, "independent reconstruction")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_AFTER_REPAIR", "disposition")
check(result["material_defect"] is None, "defect closed")
check(result["false_result_promotion_found"] is False, "not false-result promotion")
check(result["factual_screen"]["GD_recoil"] == "OPTIONAL_PARENT_BRANCH",
      "optional recoil")
check(result["global_action"] == "OWNER_INCOMPLETE", "global fail closed")
check(result["descent"] == "UNDEFINED" and result["Ward"] == "UNDEFINED",
      "undefined residuals")
check(result["gate_A"] == "OPEN" and result["gate_B"] == "UNAUTHORIZED",
      "gate ceiling")

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_AFTER_REPAIR", "microscopic record work",
              "optional enlarged physical parent", "db187df", "ea52b62",
              "Gate A remains open", "Gate B remains unauthorized"):
    check(token in report, "report token " + token)

print(f"PASS__SAME_PARENT_JOIN_HOSTILE_AUDIT__{checks}/{checks}")
