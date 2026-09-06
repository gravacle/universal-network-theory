#!/usr/bin/env python3
"""Custody, warning, result-consistency, and scope verifier."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "DEVELOPMENT_R_CONNECTED_L8_RING_STRESS_V001"
EXPECTED = {
    "README.md": "e7c3565f03d5bf08b8324c39490df87493eb91acd5187f36f7c32250956a3c89",
    "RESULT.json": "7aab465080331b33ee8ff8baf8b3299806a6fa305459c42a205f4556ffed7a13",
    "THEOREM.md": "3a18aecb96ee0acd575e066d00350c7ea8fe1700d8de778ce89ab8a5716acc2e",
    "compute_connected_ring_stress.py": "e84397107eef89c81ad1e4bbae037ef40f43dc9811ba3cefa230002f979a1de2",
}
AUTHORITY = {
    "CURRENT_CONTINUATION.md": "c3740c3635042b53a136ef7584fbfa5cd149ba30f6fd77c96c86ec9e212f7087",
    "GRAVITY_VERIFICATION_LEDGER.md": "4341591924eaccddb8aa80dff2ed53322b50a52f6c3b814f34fbd0cd734b114f",
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
check("compute_connected_ring_stress" not in source, "no target import")

env = os.environ.copy()
env["PYTHONWARNINGS"] = "error"
target_run = subprocess.run([sys.executable, "-B", str(TARGET / "compute_connected_ring_stress.py")],
                            check=True, capture_output=True, text=True, env=env)
check("PASS__R_CONNECTED_L8_RING_STRESS__10/10" in target_run.stdout,
      "target warning-free pass")
payload = json.loads(target_run.stdout[:target_run.stdout.rfind("\nPASS__")])
hard = json.loads((TARGET / "RESULT.json").read_text())
check(hard["rings"] == payload["rings_in_L8_tiling"] == 32, "ring result")
for hk, pk, tol in (
    ("retained_total_after", "L8_total_retained_after", 1e-13),
    ("absolute_oriented_throughput", "L8_absolute_oriented_throughput", 1e-12),
    ("signed_ring_current_sum", "L8_net_oriented_ring_current", 1e-13),
    ("L8_residual_l1_bound", "L8_residual_l1_bound", 1e-13),
    ("number_law_max_change", "number_law_max_change", 1e-13),
):
    check(abs(hard[hk]-payload[pk]) < tol, "hard-coded consistency " + hk)

run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True, env=env)
check("PASS_CONTROLLED_NUMERICAL_PREPARED_STRESS__" in run.stdout,
      "independent warning-free run")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_CONTROLLED_NUMERICAL_PREPARED_STRESS", "pass")
check((result["rings"], result["heads"]) == (32, 256), "coverage")
check(result["number_commutator_max"] == "0", "number conservation")
check(result["residual_l1"] < 2e-11 and result["residual_linf"] < 3e-12,
      "ledger tolerances")
check(abs(result["retained_L8"]-128) < 7e-14, "retention")
check(abs(result["net_current_L8"]) < 3e-14, "net current")
check(result["generic_critical_continuum_Ward_gravity"] == "NOT_CLAIMED",
      "scope ceiling")
check(hard["attachment"] == "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
      "attachment provenance")
check(hard["terminal_instrument"] == "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
      "complete read")
check(hard["status"] ==
      "PASS_CONTROLLED_NUMERICAL_PREPARED_STRESS_AFTER_HOSTILE_AUDIT",
      "sealed target status")
continuation = (HERE.parent / "CURRENT_CONTINUATION.md").read_text()
ledger = (HERE.parent / "GRAVITY_VERIFICATION_LEDGER.md").read_text()
check("connected-ring successor now passes hostile audit as controlled\nnumerical prepared-history evidence" in continuation and
      "Do not promote this to generic retention" in continuation,
      "continuation summary")
check("Connected L8 carrier-ring stress" in ledger and
      "Generic\nretention, individual lineage motion, criticality" in ledger,
      "ledger summary")

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_CONTROLLED_NUMERICAL_PREPARED_STRESS", "32", "256",
              "PYTHONWARNINGS=error", "two explicit contraction steps",
              "Hard-coded RESULT", "No material defect"):
    check(token in report, "report token " + token)

print(f"PASS__CONNECTED_RING_HOSTILE_AUDIT__{checks}/{checks}")
