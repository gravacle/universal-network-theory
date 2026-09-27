#!/usr/bin/env python3
"""Capture bounded review checks, including failures; never launch L6/L8/L12.

Use --output with a new directory. This is an observation runner, not a
scientific acceptance gate. Individual nonzero exits remain nonzero records.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("urm_aggregate", "model/validate_urm.py", []),
    ("aurft_standalone", "LANE_RFT_AXIOMATIC_URFT_CLOSURE_V001/verify_axiomatic_urft_closure.py", []),
    ("alpha_algebra", "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/verify_alpha_sector_inheritance.py", []),
    ("pmics_independent", "LANE_CROSS_RFT_GRA_GJ_Q4_PAIR_MEMORY_INTRINSIC_CURVATURE_SYMBOL_V001/INDEPENDENT_HOSTILE_AUDIT/independent_verify_pmics.py", []),
    ("pmsr_independent", "LANE_CROSS_RFT_GRA_GK_Q4_PAIR_MEMORY_SOURCE_RECIPROCITY_V001/INDEPENDENT_HOSTILE_AUDIT/verify_hostile_pmsr.py", []),
    ("l4_v002_packet", "DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/verify_packet.py", []),
    ("l4_reconciliation", "AUDIT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V001/verify_l4_reconciliation.py", []),
    ("l4_restart_fresh", "DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V002/test_hardened_runtime.py", ["--fresh-baseline"]),
    ("l4_reconciliation_tests", "AUDIT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V001/test_l4_reconciliation_verifier.py", []),
    ("l8_prospective_controls", "DEVELOPMENT_R_OWNER_ONCE_L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_V001/test_operator_incidence_curvature_response.py", []),
    ("l8_historical_curvature", "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/validate_result.py", []),
    ("l6_static_packet", "DEVELOPMENT_R_L6_AUTONOMOUS_RESPONSE_PREPRODUCTION_GATE_V001/verify_packet.py", []),
    ("l6_static_tests", "DEVELOPMENT_R_L6_AUTONOMOUS_RESPONSE_PREPRODUCTION_GATE_V001/test_static_estimator.py", []),
    ("transfer_contract_tests", "REMOTE_COMPUTE_RESTART_CONTRACT_2026-09-27_V001/test_transfer_manifest.py", []),
    ("migration_snapshot_legacy", "MIGRATION_CONTEXT_AUDIT_2026-09-27_V001/verify_context_audit.py", []),
    ("dark_prerequisites_legacy", "UNT_DARK_SECTOR_JOINT_PLAN_PREREQUISITE_AUDIT_V001/verify_packet.py", []),
]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only", choices=[row[0] for row in CHECKS])
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    record = {
        "schema": "UNT_BOUNDED_REVIEW_CHECKS_V001",
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_head": git("rev-parse", "HEAD"),
        "source_tree": git("rev-parse", "HEAD^{tree}"),
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "root": str(ROOT),
        "tracked_diff_at_start": git("diff", "--stat", "HEAD"),
        "scope": "Existing bounded validators and small L4/synthetic tests only; no production evolution or empirical corroboration.",
        "checks": [],
    }
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for name, relative, extra in CHECKS:
        if args.only and name != args.only:
            continue
        source = ROOT / relative
        command = [sys.executable, "-B", str(source), *extra]
        start = time.monotonic()
        print("START", name, flush=True)
        try:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=900)
            output, code, timed_out = result.stdout, result.returncode, False
        except subprocess.TimeoutExpired as error:
            output, code, timed_out = error.stdout or b"", None, True
        log = args.output / (name + ".log")
        log.write_bytes(output)
        row = {
            "id": name, "script": relative, "arguments": extra,
            "script_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "exit_code": code, "timed_out": timed_out,
            "wall_seconds": time.monotonic() - start,
            "log": log.name, "log_bytes": len(output),
            "log_sha256": hashlib.sha256(output).hexdigest(),
        }
        record["checks"].append(row)
        (args.output / "RESULTS.json").write_text(json.dumps(record, indent=2) + "\n")
        print("END", name, "exit", code, "seconds", round(row["wall_seconds"], 3), flush=True)
    print("RECORDED_RESULTS_NOT_A_BLANKET_PASS", args.output, flush=True)


if __name__ == "__main__":
    main()
