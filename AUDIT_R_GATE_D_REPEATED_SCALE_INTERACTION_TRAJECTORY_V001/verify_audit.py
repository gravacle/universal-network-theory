#!/usr/bin/env python3
"""Custody, independence, and scope checks for R-D hostile audit."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "DEVELOPMENT_R_GATE_D_REPEATED_SCALE_INTERACTION_TRAJECTORY_V001"
EXPECTED = {
    "README.md": "59b74508ad84c436d55e11257a0be9789bc7807b938915eec86aef7ff4f50eb3",
    "RESULT.json": "ae084bb592097956ba9802d72ead74c5ade7e901f862bdc481b635b37926d579",
    "THEOREM.md": "79a121e689e9f9ac036ce0835d766c627be9b31b726eb43ea18875c79f234c23",
    "verify_repeated_scale_trajectory.py": "b23cbdd05eb4c5d390d37725da0de01fcd79df5d9d4d1d8079f69979bd2f8514",
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
# Authority files are cumulative journals. Pin the audited R-D section's
# semantic invariants instead of invalidating this packet on later appends.
continuation = (HERE.parent / "CURRENT_CONTINUATION.md").read_text()
ledger = (HERE.parent / "GRAVITY_VERIFICATION_LEDGER.md").read_text()
check("repeated `L=4 -> L=8` interaction trajectory also passes hostile audit at\nprepared fixed-density scope" in continuation,
      "continuation R-D status")
check("This is algebraic volume replication,\nnot a continuum or critical exponent" in continuation,
      "continuation R-D ceiling")
check("Gate R-D — REPEATED-SCALE INTERACTION TRAJECTORY: PASS, PREPARED SCOPE" in ledger,
      "ledger R-D status")
check("accepts eight only as exact fixed-density disjoint-block\nvolume replication" in ledger and
      "not a continuum, critical, or generic accumulation" in ledger,
      "ledger R-D ceiling")
source = (HERE / "independent_reconstruction.py").read_text()
check("verify_repeated_scale_trajectory" not in source, "no target import")
run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True)
check("PASS_CONDITIONAL_FIXED_DENSITY_TRAJECTORY__" in run.stdout, "independent run")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_CONDITIONAL_FIXED_DENSITY_TRAJECTORY", "pass")
check(result["general_even_L"]["blocks"] == "L^3/4", "general blocks")
check(result["L4"] == ["64", "16", "16", "4", "4", "12", "0", "0"], "L4")
check(result["L8"] == ["512", "128", "128", "32", "32", "96", "0", "0"], "L8")
check(result["ratios"] == ["8"]*6, "ratios")
check("ADOPTED_ALPHA_EQUALS_R0" in result["attachment"], "attachment")
check(result["scope"] == "CONDITIONAL_FIXED_DENSITY_DISJOINT_BLOCK_FAMILY", "scope")
check("CONTROLLER_FAILURE" in result["terminal_instrument"], "complete read")
check(result["ratio_interpretation"] ==
      "VOLUME_REPLICATION_ONLY__NOT_CONTINUUM_CRITICAL_OR_GENERIC", "interpretation")
check(result["individual_lineage_criticality_continuum_gravity"] == "NOT_CLAIMED",
      "claim ceiling")
target_result = json.loads((TARGET / "RESULT.json").read_text())
check(target_result["R_D"] ==
      "PASS_PREPARED_REPEATED_SCALE_TRAJECTORY_AFTER_HOSTILE_AUDIT",
      "sealed R-D disposition")

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_CONDITIONAL_FIXED_DENSITY_TRAJECTORY", "arbitrary positive even",
              "(64,16,16,4,4,12,0,0)", "alpha=r0=14441248/6075",
              "OK/FAILURE", "algebraic volume replication",
              "not a fitted scaling", "No material defect"):
    check(token in report, "report token " + token)

print(f"PASS__R_D_HOSTILE_AUDIT_CUSTODY_AND_SCOPE__{checks}/{checks}")
