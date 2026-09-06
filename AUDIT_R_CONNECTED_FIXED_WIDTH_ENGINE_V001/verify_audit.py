#!/usr/bin/env python3
"""Fail-closed verifier for the hostile fixed-width-engine audit."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_CONNECTED_FIXED_WIDTH_ENGINE_V001"
PINS = {
    TARGET / "README.md": "a93a1fed5ebbf6fa966a9c58a32f2be346b2781c7f3b78e2676ce882d1e7bebd",
    TARGET / "RESULT.json": "338ebcb186bd506bbc0108b888a779b73ffce9233c53328b2adf213a51ac4526",
    TARGET / "THEOREM.md": "e4ead0f98489b2ad961018c9eb9f283b9549f3be6f52634e1e86264b58654c1d",
    TARGET / "validate_engine.py": "bf9d680a40d307f583ca8d1a1d6abf86d02bcdd7296c466cd7e915d1fc44e2fd",
    ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001" / "RESULT.json": "043c85675cfc4956fa2e5216a324e941bf84523bf4abd0054ed2be07f378bbdc",
    ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001" / "RESULT.json": "e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
    ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001" / "RESULT.json": "7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63",
    ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001" / "RESULT.json": "06256f48fb39df0b5121ea01b38893ffeb84ba1bc7f842d22935ccd5279cdcbf",
    ROOT / "AUDIT_R_CONNECTED_PRISM_ORBIT_REDUCTION_V001" / "independent_reconstruction.py": "e027390012d6b7a9a4e17c06c9940b75bbdbbbd2157c33bf7025399437acd6a4",
    ROOT / "AUDIT_R_CONNECTED_PRISM_ORBIT_REDUCTION_V001" / "INDEPENDENT_RESULT.json": "6620a6abe8b571e87580da9548383a90fc57e907f54e83536ff7b926709cce73",
}
for path, expected in PINS.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"custody mismatch: {path}"

env = os.environ.copy()
env.update({"PYTHONWARNINGS": "error", "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "VECLIB_MAXIMUM_THREADS": "1"})
target_run = subprocess.run([sys.executable, "-B", str(TARGET / "validate_engine.py")], env=env, text=True, capture_output=True, check=True)
assert target_run.stdout.strip() == "PASS__R_CONNECTED_FIXED_WIDTH_ENGINE__40/40"
assert hashlib.sha256((TARGET / "RESULT.json").read_bytes()).hexdigest() == PINS[TARGET / "RESULT.json"]

attack = subprocess.run([sys.executable, "-B", str(HERE / "independent_checks.py")], env=env, text=True, capture_output=True, check=True)
assert "PASS__INDEPENDENT_FIXED_WIDTH_ENGINE_ATTACKS" in attack.stdout

result = json.loads((HERE / "RESULT.json").read_text())
assert result["target_checks"] == "PASS__40/40" and result["target_disposition"] == "UNCHANGED"
assert "NO_CONTINUITY_OR_WARD_USED" in result["signed_current_attack"]
assert result["authorization"].startswith("GUARDED_NUMERICAL_L14_IMPLEMENTATION_ONLY")
required = {"L14_ACCUMULATION", "GRID", "CONTINUUM", "CONTINUITY_AXIOM", "WARD", "PHASE", "GRAVITON", "GRAVITY", "SCALING", "COMPLEXITY_LAW"}
assert required <= set(result["not_claimed"])

theorem = (TARGET / "THEOREM.md").read_text()
for phrase in ("failed closed", "Explicit float64", "promotion repaired", "does not insert a\ncontinuity equation or Ward axiom", "evolution and quadrature remain numerical"):
    assert phrase in theorem

print("PASS__AUDIT_R_CONNECTED_FIXED_WIDTH_ENGINE__TARGET_UNCHANGED__GUARDED_NUMERICAL_USE_ONLY")
