#!/usr/bin/env python3
"""Record small additive repair/math checks without rewriting scientific outputs."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
P = HERE.name + "/"
CHECKS = [
    ("aurft_successor", "AUTHENTICATED_REPLAY_CUSTODY_REPAIR_2026-09-27_V001/verify_axiomatic_urft_closure_v002.py", []),
    ("aurft_resolver_tests", "AUTHENTICATED_REPLAY_CUSTODY_REPAIR_2026-09-27_V001/test_manifest_resolution.py", []),
    ("l8_relocated_validator", "CUSTODY_RECOVERY_NUMERICS_2026-09-27_V001/validate_l8_relocated.py", []),
    ("numerical_recovery_tests", "CUSTODY_RECOVERY_NUMERICS_2026-09-27_V001/test_recovery.py", []),
    ("progression_recovery_tests", "CUSTODY_RECOVERY_NUMERICS_2026-09-27_V001/test_progression_recovery.py", []),
    ("progression_input_preflight", "CUSTODY_RECOVERY_NUMERICS_2026-09-27_V001/restore_progression_inputs.py", ["--preflight-only"]),
    ("carrier_closure_reconciliation", "DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001/test_reconcile_closure.py", []),
    ("finite_mass_arithmetic", P + "audit_finite_masses_v001.py", ["--root", str(ROOT)]),
    ("remaining_foundation_custody", P + "audit_foundation_custody_v001.py", ["--root", str(ROOT)]),
    ("lineage_exact_toy", P + "PROOF_DEVELOPMENT/verify_lineage_response_toy.py", []),
    ("dark_budget_exact_toy", P + "PROOF_DEVELOPMENT/verify_dark_sector_construction_toy.py", []),
    ("review_custody_tests", P + "test_review_custody.py", []),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    record = {"schema": "UNT_BOUNDED_REPAIR_MATH_CHECKS_V001",
              "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "python": sys.version, "checks": [],
              "meaning": "Recorded exits, including unresolved custody; not empirical validation."}
    for name, script, extra in CHECKS:
        path = ROOT / script
        start = time.monotonic()
        result = subprocess.run([sys.executable, "-B", str(path), *extra], cwd=ROOT,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
        raw = result.stdout
        log = args.output / (name + ".log")
        log.write_bytes(raw)
        record["checks"].append({"id": name, "script": script, "arguments": extra,
            "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "exit_code": result.returncode, "wall_seconds": time.monotonic() - start,
            "log": log.name, "log_bytes": len(raw), "log_sha256": hashlib.sha256(raw).hexdigest()})
        (args.output / "RESULTS.json").write_text(json.dumps(record, indent=2) + "\n")
        print(name, "exit", result.returncode, flush=True)


if __name__ == "__main__":
    main()
