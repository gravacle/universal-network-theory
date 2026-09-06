#!/usr/bin/env python3
"""Custody, independence, and scope verifier for R-B hostile audit."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_GATE_B_L8_DENSITY_CONTROLLED_ACCUMULATION_V001"
EXPECTED = {
    "EXECUTION_CUSTODY.json": "999b0e3821669ed48a79693394d09c60bed9b8525efbedb822e84de43fbc9029",
    "README.md": "e926847afae69143220d226a9d3bdb8f92d2346949096d405cc508c4a85f0e3c",
    "RESULT.json": "0aeb7b5cbea9815bfed1514d119fa679e63d1db1ecf7d5945bdc953cdc14ae03",
    "THEOREM.md": "43f8183ef6c34cffa1e50eac148804ca52074ef9345a2b6f82cb26562158f083",
    "verify_l8_record_accumulation.py": "3b680569d6df6241c364da32465494ffb72f02cea6f06cc4ff1a3887901a94b9",
}
PLAN_HASH = "4ceb39337694b0782e01436e1d03021e6d4559043e5b3790baec4ef41cc93b5c"
checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


for name, digest in EXPECTED.items():
    check(hashlib.sha256((TARGET / name).read_bytes()).hexdigest() == digest,
          "target custody " + name)
plan = ROOT / "RECORD_FIRST_ACCUMULATION_GATE_PLAN_V002.md"
check(hashlib.sha256(plan.read_bytes()).hexdigest() == PLAN_HASH, "schedule custody")

source = (HERE / "independent_reconstruction.py").read_text()
check("verify_l8_record_accumulation" not in source, "no target import")
run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True)
check("PASS_AFTER_REPAIR__" in run.stdout, "independent run")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_AFTER_REPAIR", "disposition")
check(result["arithmetic"] == "PASS", "arithmetic passes")
check(result["scope"] == "CONDITIONAL_TENSOR_PRODUCT_PREPARED_HISTORY",
      "conditional scope")
check(result["generic_accumulation"] == "NOT_PROVED", "generic ceiling")
check(result["schedule_V002"] == "PASS_SEPARATION_AND_OWNER_ONCE", "schedule pass")
check(len(result["material_defects"]) == 0, "repair items closed")
check("ADOPTED_ALPHA_EQUALS_R0" in result["attachment"], "attachment custody")
check("CONTROLLER_FAILURE" in result["terminal_instrument"], "failure read")
check(result["carrier_residual_l1_linf"]["L8"] == ["0", "0"], "L8 residuals")
check(result["execution_custody"]["scope"] ==
      "EXACT_COMBINATORIAL_VERIFIER__NOT_DENSE_3_POW_512_EVOLUTION",
      "execution scope")
target_result = json.loads((TARGET / "RESULT.json").read_text())
check(target_result["R_B"] ==
      "PASS_BASELINE_PREPARED_ACCUMULATION_AFTER_HOSTILE_AUDIT",
      "sealed R-B disposition")

plan_text = plan.read_text()
for token in ("R-B does **not** require", "optional **M-series**",
              "Every action term present", "generic accumulation"):
    check(token in plan_text, "schedule token " + token)

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_AFTER_REPAIR", "absolute module-oriented", "net periodic",
              "alpha=r0", "controller effects", "does not overclaim generic",
              "exact combinatorial", "dense `3^512`", "future nonzero is unclassified"):
    check(token in report, "report token " + token)

print(f"PASS__R_B_HOSTILE_AUDIT_CUSTODY_AND_SCOPE__{checks}/{checks}")
