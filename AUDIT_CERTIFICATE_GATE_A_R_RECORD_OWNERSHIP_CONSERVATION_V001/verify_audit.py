#!/usr/bin/env python3
"""Custody and independence checks for the Gate A-R hostile audit."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CERT = ROOT / "CERTIFICATE_GATE_A_R_RECORD_OWNERSHIP_CONSERVATION_V001"
EXPECTED = {
    "CERTIFICATE.md": "3e496fb08e2badbbc4a70110adccc6b3528beeb19d42bef5b8af2e0e1b1348df",
    "README.md": "7f691ae26d863349024cf9efcf0405f478c1641e7b4960323ade96a910239595",
    "RESULT.json": "51c80f95c7a8819c21cd7d7f6bba06111a4b03a95d641d1296f407ecada3d432",
    "verify_gate_a_r_certificate.py": "49618db2497f49c1668d2b429793b8b4b0edf1dea360da70a7635f81607d81b9",
}
AUTHORITY = {
    "CURRENT_CONTINUATION.md": "daac2a66951c88b2f08095b926c9a3e0bac04e75b1fd6bed6dac4ff40df75542",
    "GRAVITY_VERIFICATION_LEDGER.md": "ecc9a5ab3bc9396e9c3af72fb5f679719cc4a49551753e44d2ac36bca0a59439",
    "RECORD_FIRST_ACCUMULATION_GATE_PLAN_V002.md": "4ceb39337694b0782e01436e1d03021e6d4559043e5b3790baec4ef41cc93b5c",
}
checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


for name, digest in EXPECTED.items():
    check(hashlib.sha256((CERT / name).read_bytes()).hexdigest() == digest,
          "certificate custody " + name)
for name, digest in AUTHORITY.items():
    check(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
          "authority custody " + name)

source = (HERE / "independent_reconstruction.py").read_text()
check("verify_gate_a_r_certificate" not in source, "no target verifier import")
run = subprocess.run([sys.executable, "-B", str(HERE / "independent_reconstruction.py")],
                     check=True, capture_output=True, text=True)
check("PASS_AFTER_REPAIR__" in run.stdout, "independent reconstruction")
result = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
check(result["disposition"] == "PASS_AFTER_REPAIR", "disposition")
check(result["certificate_premises"] == "PASS_AT_CONDITIONAL_RECORD_SCOPE",
      "premises pass")
check(result["join_counts"] == {"target": "28/28", "hostile_reconstruction": "18/18"},
      "join layers")
check(result["gate_B_R"] == "AUTHORIZED" and result["gate_A_P"] == "OPEN",
      "gate split")
check(result["M_series"] == "NOT_PROMOTED" and
      result["continuum_Ward_gravity"] == "NOT_PROMOTED", "scope ceiling")

report = (HERE / "AUDIT_REPORT.md").read_text()
for token in ("PASS_AFTER_REPAIR", "28/28", "18/18", "alpha=r0",
              "does not block authorized B-R", "optional",
              "does not close A-P"):
    check(token in report, "report token " + token)

print(f"PASS__GATE_A_R_CERTIFICATE_HOSTILE_AUDIT__{checks}/{checks}")
