#!/usr/bin/env python3
"""Custody, warning, numerical consistency, and scope verification."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "DEVELOPMENT_R_CONNECTED_RING_PARAMETER_SCAN_V001"
EXPECTED = {
    "README.md": "3da1d4904f69c321cced33f85879910d28925b9ff7293248a9e00132311fdd37",
    "RESULT.json": "0aaba5dac403360cb5b4a008f7d3047ca10152c1e6e3b88074d6a7171729cfa5",
    "THEOREM.md": "003b1b89ac3333833c8a42b7c9826dd221ec152a3c48292252834c219a0d52c8",
    "compute_parameter_scan.py": "6997a24fb4acb03b8ea433ff77f3af2bf077003ef3b699ef44ea2f139d120fe7",
}
checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


for name, digest in EXPECTED.items():
    check(hashlib.sha256((TARGET/name).read_bytes()).hexdigest() == digest,
          "target custody " + name)
source = (HERE/"independent_reconstruction.py").read_text()
check("compute_parameter_scan" not in source, "no target import")

env = os.environ.copy()
env["PYTHONWARNINGS"] = "error"
ind = subprocess.run([sys.executable, "-B", str(HERE/"independent_reconstruction.py")],
                     check=True, capture_output=True, text=True, env=env)
check("PASS_CONTROLLED_NUMERICAL_PARAMETER_SCAN__" in ind.stdout,
      "independent warning-free run")
audit = json.loads((HERE/"INDEPENDENT_RESULT.json").read_text())
hard = json.loads((TARGET/"RESULT.json").read_text())
check(audit["disposition"] == "PASS_CONTROLLED_NUMERICAL_PARAMETER_SCAN", "pass")
check(len(audit["points"]) == len(hard["points"]) == 12, "12 points")

mapping = {
    "delta": "staggered_delta", "tau": "tau", "q_min": "q_min",
    "q_max": "q_max", "amp": "staggered_occupation_amplitude",
    "corr": "max_abs_nearest_neighbor_connected_correlation",
    "throughput": "absolute_oriented_throughput_per_ring",
    "net_current": "signed_oriented_current_sum_per_ring",
    "retained_change": "retained_total_change_per_ring",
    "r1": "record_ledger_residual_l1_per_ring",
    "rinf": "record_ledger_residual_linf_per_ring", "norm": "norm_error",
    "energy": "energy_error", "number_law": "number_law_max_change",
}
for i, (a, h) in enumerate(zip(audit["points"], hard["points"])):
    for ak, hk in mapping.items():
        check(abs(a[ak]-h[hk]) < 5e-13, f"point {i} field {hk}")

check(audit["zero_bias"] ==
      "ZERO_POSITIONAL_RESPONSE_AND_CURRENT__NONZERO_CORRELATION_ALLOWED",
      "zero-bias interpretation")
check(audit["residuals"] == "RAW_UNASSIGNED_UNTIL_OWNER_CLASSIFICATION",
      "residual classification")
check(audit["defect_continuum_critical_Ward_gravity"] == "NOT_PROMOTED",
      "claim ceiling")
check(hard["attachment"] == "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
      "attachment")
check(hard["terminal_instrument"] == "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
      "complete read")
check(hard["envelope"]["max_record_ledger_residual_l1_per_ring"] < 3e-11 and
      hard["envelope"]["max_record_ledger_residual_linf_per_ring"] < 4e-12,
      "tolerances")

report = (HERE/"AUDIT_REPORT.md").read_text()
for token in ("PASS_CONTROLLED_NUMERICAL_PARAMETER_SCAN", "all 12",
              "dot(q_i)=-J_i+J_(i-1)", "zero staggered bias", "not say the evolution is trivial",
              "not called physical defects", "No material defect"):
    check(token in report, "report token " + token)

print(f"PASS__CONNECTED_RING_SCAN_HOSTILE_AUDIT__{checks}/{checks}")
