#!/usr/bin/env python3
"""Owner-once coordinator for the two-node L14 targeted scout."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

from branch_runner import REQUEST_SCHEMA
from durable_evidence import EvidenceError, immutable_write_json, load_json, sha256_file
from merge_branches import merge


PHASE1_SECTORS = [4, 5, 6, 7]
PHASE3_SECTORS = [8, 9]
MASS_LEDGER_SECTORS = [4, 5, 6, 7, 8, 9]


def load_v1_gate():
    path = Path(__file__).resolve().parents[1] / "DEVELOPMENT_R_L14_TARGETED_SCOUT_V001" / "l14_scout_harness.py"
    spec = importlib.util.spec_from_file_location("l14_scout_gate_v001", str(path))
    if spec is None or spec.loader is None:
        raise EvidenceError("cannot import frozen V001 gate")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def phase_request(run_id: str, phase: str, authorization: Mapping[str, Any] = None) -> Dict[str, Any]:
    sectors = PHASE1_SECTORS if phase == "bridge" else PHASE3_SECTORS
    payload: Dict[str, Any] = {
        "schema": REQUEST_SCHEMA,
        "run_id": run_id,
        "length": 14,
        "phase": phase,
        "sectors": sectors,
        "mass_ledger_sectors": MASS_LEDGER_SECTORS,
        "branches": ["target", "hostile"],
        "geometry_history_sizes": [4, 6, 8, 10, 12, 14],
        "geometry_window": {"z": ["0.90", "1.10"], "y": ["0.90", "1.10"]},
        "classification_policy": "TARGET_AND_HOSTILE_CONSENSUS",
        "numerical_policy": "ALL_ORIGINAL_PREDICATES_MUST_PASS_NO_OVERRIDE",
        "probability_policy": "DEDUPLICATE_BY_Q_BEFORE_SUM",
        "claim_boundary": "TARGETED_FINITE_L14_SCOUT_ONLY",
    }
    if phase == "conditional_tail":
        if not authorization:
            raise EvidenceError("Phase 3 requires owner-once authorization")
        payload["phase2_authorization"] = dict(authorization)
    return payload


def prepare(args: argparse.Namespace) -> int:
    root = args.run_root.expanduser().resolve()
    if root.exists():
        raise EvidenceError("run root must be fresh: {}".format(root))
    root.mkdir(parents=True, exist_ok=False)
    identity = {
        "schema": "L14_SCOUT_COORDINATOR_IDENTITY_V002",
        "run_id": args.run_id,
        "length": 14,
        "threshold": args.threshold,
        "phase_policy": "Q4_Q7_THEN_CONDITIONAL_Q8_Q9",
        "branch_policy": "INDEPENDENT_TARGET_AND_HOSTILE",
    }
    immutable_write_json(root / "RUN_IDENTITY.json", identity)
    immutable_write_json(root / "PHASE1_REQUEST.json", phase_request(args.run_id, "bridge"))
    print("L14_COORDINATOR_PREPARED run_root={} phase1_request={}".format(root, root / "PHASE1_REQUEST.json"))
    return 0


def phase2(args: argparse.Namespace) -> int:
    root = args.run_root.expanduser().resolve()
    identity = load_json(root / "RUN_IDENTITY.json")
    request = load_json(root / "PHASE1_REQUEST.json")
    if request.get("run_id") != identity.get("run_id"):
        raise EvidenceError("run identity/request mismatch")
    result_path = root / "PHASE1_RESULT.json"
    merged = merge(args.target, args.hostile)
    immutable_write_json(result_path, merged)
    gate = load_v1_gate()
    phase1 = gate.parse_phase_result(result_path, "bridge", tuple(PHASE1_SECTORS))
    threshold = Decimal(str(identity["threshold"]))
    decision = gate.evaluate_phase2(phase1, threshold)
    gate.print_phase2(decision, threshold)
    report = gate.report_value(
        "AUTHORIZED_PHASE3__NOT_EXECUTED" if decision.proceed else "HALT__L14_BRIDGE_HYPOTHESIS_REJECTED",
        phase1,
        decision,
        threshold,
    )
    report_path = root / "PHASE2_GATE_REPORT.json"
    immutable_write_json(report_path, report)
    if not decision.proceed:
        return 20
    authorization = {
        "gate_report_path": str(report_path),
        "gate_report_sha256": sha256_file(report_path),
        "phase1_result_path": str(result_path),
        "phase1_result_sha256": sha256_file(result_path),
    }
    immutable_write_json(root / "PHASE3_REQUEST.json", phase_request(identity["run_id"], "conditional_tail", authorization))
    print("L14_PHASE3_AUTHORIZED request={}".format(root / "PHASE3_REQUEST.json"), flush=True)
    return 0


def final(args: argparse.Namespace) -> int:
    root = args.run_root.expanduser().resolve()
    identity = load_json(root / "RUN_IDENTITY.json")
    request = load_json(root / "PHASE3_REQUEST.json")
    authorization = request.get("phase2_authorization")
    if not isinstance(authorization, dict):
        raise EvidenceError("Phase 3 request lacks authorization")
    for path_key, hash_key in (
        ("gate_report_path", "gate_report_sha256"),
        ("phase1_result_path", "phase1_result_sha256"),
    ):
        path = Path(authorization[path_key]).resolve()
        if not path.is_file() or sha256_file(path) != authorization[hash_key]:
            raise EvidenceError("Phase 3 authorization artifact changed: {}".format(path_key))

    phase3_path = root / "PHASE3_RESULT.json"
    immutable_write_json(phase3_path, merge(args.target, args.hostile))
    gate = load_v1_gate()
    phase1 = gate.parse_phase_result(root / "PHASE1_RESULT.json", "bridge", tuple(PHASE1_SECTORS))
    phase3 = gate.parse_phase_result(phase3_path, "conditional_tail", tuple(PHASE3_SECTORS))
    for q in PHASE3_SECTORS:
        if phase1.masses[q] != phase3.masses[q]:
            raise EvidenceError("q={} mass changed across phase boundary".format(q))
    combined_atoms = tuple(phase1.atoms) + tuple(phase3.atoms)
    gate.validate_atoms(combined_atoms)
    passing = gate.passing_atoms(combined_atoms)
    passing_q = tuple(sorted({atom.q for atom in passing}))
    final_mass = gate.sum_unique_mass(passing_q, phase1.masses)
    threshold = Decimal(str(identity["threshold"]))
    phase2_report = load_json(root / "PHASE2_GATE_REPORT.json")
    report = {
        "schema": gate.REPORT_SCHEMA,
        "classification": "COMPLETE__L14_SCOUT_THRESHOLD_MET" if final_mass >= threshold else "COMPLETE__L14_SCOUT_THRESHOLD_NOT_MET",
        "length": 14,
        "threshold": str(threshold),
        "phase1": {"path": str((root / "PHASE1_RESULT.json").resolve()), "sha256": sha256_file(root / "PHASE1_RESULT.json")},
        "phase2_gate": {"path": str((root / "PHASE2_GATE_REPORT.json").resolve()), "sha256": sha256_file(root / "PHASE2_GATE_REPORT.json"), "decision": phase2_report["gate"]},
        "phase3": {"path": str(phase3_path.resolve()), "sha256": sha256_file(phase3_path)},
        "final_passing_sectors": list(passing_q),
        "final_deduplicated_mass": str(final_mass),
        "final_threshold_met": final_mass >= threshold,
        "final_passing_blocks": [[atom.atom_id for atom in block] for block in gate.passing_blocks(passing)],
        "claim_boundary": "TARGETED_FINITE_L14_SCOUT_ONLY__NO_LIMIT_CONTINUUM_GRAVITY_OR_STAGE7_CLAIM",
    }
    immutable_write_json(root / "FINAL_GATE_REPORT.json", report)
    print(
        "L14_SCOUT_FINAL passing_sectors={} deduplicated_mass={} threshold={} verdict={}".format(
            list(passing_q), final_mass, threshold, "MEETS_OR_EXCEEDS" if final_mass >= threshold else "BELOW"
        ),
        flush=True,
    )
    return 0 if final_mass >= threshold else 21


def main(argv: Sequence[str] = ()) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--run-root", required=True, type=Path)
    prepare_parser.add_argument("--run-id", required=True)
    prepare_parser.add_argument("--threshold", default="0.50")
    prepare_parser.set_defaults(function=prepare)
    for name, function in (("phase2", phase2), ("final", final)):
        child = subparsers.add_parser(name)
        child.add_argument("--run-root", required=True, type=Path)
        child.add_argument("--target", required=True, type=Path)
        child.add_argument("--hostile", required=True, type=Path)
        child.set_defaults(function=function)
    args = parser.parse_args(argv or sys.argv[1:])
    return args.function(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_COORDINATOR_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr, flush=True)
        raise SystemExit(2)
