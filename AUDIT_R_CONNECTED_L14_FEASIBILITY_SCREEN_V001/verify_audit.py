#!/usr/bin/env python3
"""Fail-closed hostile verifier for the L14 feasibility packet."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_CONNECTED_L14_FEASIBILITY_SCREEN_V001"
PINS = {
    "screen_l14.py": "5f7d6fbea948f209c17af9b0e2488766e18b271f4314382fccb979479787a753",
    "RESULT.json": "6ce39d9c57a070544b5f7857a5154557e580ec5682484cabe9e5373a34706bc0",
    "README.md": "16643852cf4f2c29234f8c4da13519d42ab6f3e9f497c3a991dc9a52766a5053",
    "THEOREM.md": "68a14aba6246e7cc3600236b8905f53e42959b52351aba4cffd39e40fc01c03b",
}

for name, expected in PINS.items():
    assert hashlib.sha256((TARGET / name).read_bytes()).hexdigest() == expected

target_run = subprocess.run(
    [sys.executable, "-B", str(TARGET / "screen_l14.py")],
    env={"PYTHONWARNINGS": "error"}, text=True, capture_output=True, check=True,
)
assert target_run.stdout.strip() == "PASS__R_CONNECTED_L14_FEASIBILITY_SCREEN__18/18"

independent_run = subprocess.run(
    [sys.executable, "-B", str(HERE / "reconstruct_independent.py")],
    env={"PYTHONWARNINGS": "error"}, text=True, capture_output=True, check=True,
)
assert independent_run.stdout.strip() == "PASS__INDEPENDENT_L14_FEASIBILITY_RECONSTRUCTION"

t = json.loads((TARGET / "RESULT.json").read_text())
a = json.loads((HERE / "RESULT.json").read_text())
assert t["finite_group"]["orbit_dimension"] == a["orbit_dimension"]
assert t["finite_group"]["burnside_fixed_word_sum"] == a["burnside_fixed_word_sum"]
assert t["candidate_fixed_width_layout"]["transition_entries_upper"] == a["transition_slots_upper"]
assert t["candidate_fixed_width_layout"]["payload_bytes_by_array"] == a["payload_bytes_by_array"]
assert t["candidate_fixed_width_layout"]["raw_numeric_payload_upper_bytes"] == a["raw_numeric_payload_upper_bytes"]
assert "PROCESS_RSS_NOT_CERTIFIED" in t["candidate_fixed_width_layout"]["status"]
assert "NOT_AN_L14_ACCUMULATION_RESULT" in t["screen_decision"]
for forbidden in ("GRID", "CONTINUUM", "WARD", "PHASE", "GRAVITON", "GRAVITY"):
    assert forbidden in t["not_claimed"]

print("PASS__AUDIT_R_CONNECTED_L14_FEASIBILITY_SCREEN__TARGET_UNCHANGED__ENGINEERING_ONLY")
