#!/usr/bin/env python3
"""Custody, independence, and scope checks for the R-C hostile audit."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "DEVELOPMENT_R_GATE_C_L8_INTERACTION_RETENTION_STRESS_V001"
EXPECTED = {
    "README.md": "549a8ce6016106d40db6c262c000ef4a969858f913a0c1b6d22afedef4595b86",
    "RESULT.json": "af5f789b58efab01913657f564a9a7cd3a42f7a42fe86b0bc14cbb1826db33f8",
    "THEOREM.md": "57e9d54269b930abfb711d87b68209280f0c052b59f471d9d3ca792bebed1469",
    "verify_interaction_retention_stress.py": "cb8b40adc002fe479d18bf0e4f93474e378548b02d5f6b474bb620d1f994464a",
}
AUTHORITY = {
    "CURRENT_CONTINUATION.md": "baf71f37ff381020e2cefd92fee58eda924c2588321a1e88b5f6d5a1d02d4bc0",
    "GRAVITY_VERIFICATION_LEDGER.md": "44fb5db81d618b7d67b0aa7234a3edde89c41048c38b255178515b4473f84828",
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
for name, digest in AUTHORITY.items():
    check(hashlib.sha256((HERE.parent / name).read_bytes()).hexdigest() == digest,
          "authority custody " + name)
source = (HERE / "independent_reconstruction.py").read_text()
check("verify_interaction_retention_stress" not in source, "no target import")
run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True)
check("PASS_CONDITIONAL_INTERACTION_STRESS__" in run.stdout, "independent run")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_CONDITIONAL_INTERACTION_STRESS", "pass")
check(result["pair_after"] == ["1/4", "1/2", "0", "1/4"], "distribution")
check(result["TV"] == "1/4" and result["oriented_current"] == "1/4",
      "TV and current")
check(result["pair_residuals"] == ["0", "0"], "ledgers")
check(result["number_distribution"] == ["1/4", "1/2", "1/4"], "number law")
check(result["L8"] == {"heads": 256, "blocks": 128, "retained": "128",
                        "throughput": "32", "positional_after": ["32", "96"]},
      "L8 census")
check(result["read"] == "COMPLETE_FAILURE_INCLUSIVE_PRODUCT", "complete read")
check(result["individual_lineage_motion"] == "NOT_CLAIMED", "lineage ceiling")
check(result["criticality_continuum_gravity"] == "NOT_CLAIMED", "macro ceiling")
target_result = json.loads((TARGET / "RESULT.json").read_text())
check(target_result["R_C"] ==
      "PASS_CONDITIONAL_INTERACTION_STRESS_AFTER_HOSTILE_AUDIT",
      "sealed R-C disposition")
continuation = (HERE.parent / "CURRENT_CONTINUATION.md").read_text()
ledger = (HERE.parent / "GRAVITY_VERIFICATION_LEDGER.md").read_text()
check("Gate R-C interaction/retention stress now passes hostile audit" in continuation and
      "do not infer individual lineage transport, criticality, or continuum behavior" in continuation,
      "continuation summary ceiling")
check("Gate R-C — FIRST INTERACTION/RETENTION STRESS: PASS, CONDITIONAL" in ledger and
      "Individual source-lineage\nmotion, criticality, generic interacting accumulation, and continuum behavior" in ledger,
      "ledger summary ceiling")

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_CONDITIONAL_INTERACTION_STRESS", "128 disjoint", "256 odd-first-coordinate heads",
              "oriented physical", "individual source-lineage", "criticality",
              "No material defect"):
    check(token in report, "report token " + token)

print(f"PASS__R_C_HOSTILE_AUDIT_CUSTODY_AND_SCOPE__{checks}/{checks}")
