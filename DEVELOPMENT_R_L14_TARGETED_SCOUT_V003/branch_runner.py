#!/usr/bin/env python3
"""Run one L14 target or hostile branch through a bound exact kernel.

Kernel modules must export three callables:

* build_task_plan(branch, phase, request, context) -> list[task]
* run_task(task_payload, context) -> JSON object
* reduce_results(branch, phase, request, results, context) -> branch result

An exact kernel may additionally export::

    prepare_phase(branch, phase, request, context) -> JSON object

The optional preparation hook owns parent-side, dependency-ordered numerical
work such as cache construction and event-history propagation.  Its result is
committed immutably before the flat response-task pool is opened.  This keeps
the event DAG out of a misleading flat-task abstraction while retaining the
same authenticated resume boundary for both phases.

The adapter supplies durability and restart semantics.  The kernel remains the
sole owner of physics definitions, convergence predicates, and numerical work.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from durable_evidence import (
    DurableMirror,
    EvidenceError,
    immutable_write_json,
    load_json,
    sha256_file,
    validate_artifact,
)
from resumable_runtime import ResumableProcessPool, TaskSpec, _load_module, load_task_results


REQUEST_SCHEMA = "L14_SCOUT_PHASE_REQUEST_V002"
BRANCH_SCHEMA = "L14_SCOUT_BRANCH_RESULT_V002"
PREPARATION_SCHEMA = "L14_SCOUT_PHASE_PREPARATION_V002"


def finite_decimal(value: Any, label: str) -> Decimal:
    if isinstance(value, bool):
        raise EvidenceError("{} must be numeric".format(label))
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise EvidenceError("{} must be numeric".format(label)) from error
    if not result.is_finite():
        raise EvidenceError("{} must be finite".format(label))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True, choices=("target", "hostile"))
    parser.add_argument("--phase", required=True, choices=("bridge", "conditional_tail"))
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--kernel-module", required=True, type=Path)
    parser.add_argument("--checkpoint-root", required=True, type=Path)
    parser.add_argument("--shared-root", type=Path)
    parser.add_argument("--scratch-root", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--workers", required=True, type=int)
    parser.add_argument("--mirror-destination")
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args(argv)


def validate_request(request: Mapping[str, Any], branch: str, phase: str) -> None:
    if request.get("schema") != REQUEST_SCHEMA:
        raise EvidenceError("wrong request schema")
    if request.get("length") != 14:
        raise EvidenceError("L14 branch runner accepts length=14 only")
    if request.get("phase") != phase:
        raise EvidenceError("phase mismatch between CLI and request")
    expected = [4, 5, 6, 7] if phase == "bridge" else [8, 9]
    if request.get("sectors") != expected:
        raise EvidenceError("request sectors must be exactly {}".format(expected))
    if request.get("geometry_window") != {"z": ["0.90", "1.10"], "y": ["0.90", "1.10"]}:
        raise EvidenceError("geometry window is not the frozen scout window")
    branches = request.get("branches")
    if branches != ["target", "hostile"]:
        raise EvidenceError("request must bind both independent branches")
    if branch not in branches:
        raise EvidenceError("branch is not authorized by request")
    if request.get("mass_ledger_sectors") != [4, 5, 6, 7, 8, 9]:
        raise EvidenceError("mass ledger must cover q4-q9")
    if request.get("geometry_history_sizes") != [4, 6, 8, 10, 12, 14]:
        raise EvidenceError("geometry history must be exactly L4-L14")
    run_id = request.get("run_id")
    if not isinstance(run_id, str) or not run_id or any(
        character not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-" for character in run_id
    ):
        raise EvidenceError("request run_id is unsafe")
    if phase == "conditional_tail":
        authorization = request.get("phase2_authorization")
        if not isinstance(authorization, dict):
            raise EvidenceError("conditional tail lacks Phase-2 authorization")
        for key in ("gate_report_sha256", "phase1_result_sha256"):
            value = authorization.get(key)
            if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
                raise EvidenceError("conditional-tail authorization lacks {}".format(key))


def make_tasks(raw_tasks: Any) -> List[TaskSpec]:
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise EvidenceError("kernel returned an empty or malformed task plan")
    tasks = []
    for index, raw in enumerate(raw_tasks):
        if not isinstance(raw, dict):
            raise EvidenceError("task plan entry {} is not an object".format(index))
        task_id = raw.get("task_id")
        payload = raw.get("payload")
        work_units = raw.get("work_units", 1)
        if not isinstance(task_id, str) or not isinstance(payload, dict) or not isinstance(work_units, int):
            raise EvidenceError("malformed task plan entry {}".format(index))
        tasks.append(TaskSpec(task_id=task_id, payload=payload, work_units=work_units))
    return tasks


def _preparation_identity(
    branch: str,
    phase: str,
    request: Mapping[str, Any],
    context: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "branch": branch,
        "phase": phase,
        "run_id": request["run_id"],
        "length": request["length"],
        "sectors": request["sectors"],
        "mass_ledger_sectors": request["mass_ledger_sectors"],
        "kernel_sha256": context["kernel_sha256"],
        "request_sha256": context["request_sha256"],
    }


def _validate_preparation_artifacts(payload: Mapping[str, Any]) -> None:
    artifacts = payload.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise EvidenceError("preparation artifacts must be a list")
    for index, record in enumerate(artifacts):
        if not isinstance(record, dict):
            raise EvidenceError("preparation artifact {} is malformed".format(index))
        raw_path = record.get("path")
        raw_sha256 = record.get("sha256")
        raw_bytes = record.get("bytes")
        if not isinstance(raw_path, str) or not isinstance(raw_sha256, str) or type(raw_bytes) is not int:
            raise EvidenceError("preparation artifact {} lacks path/sha256/bytes".format(index))
        validate_artifact(Path(raw_path), raw_sha256, raw_bytes)


def prepare_kernel_phase(
    kernel: Any,
    branch: str,
    phase: str,
    request: Mapping[str, Any],
    context: Dict[str, Any],
    resume: bool,
    mirror: DurableMirror,
) -> Tuple[Dict[str, Any], Optional[str]]:
    """Run or authenticate the optional parent-owned phase preparation."""

    prepare = getattr(kernel, "prepare_phase", None)
    if prepare is None:
        return {}, None
    if not callable(prepare):
        raise EvidenceError("kernel prepare_phase attribute is not callable")

    checkpoint_root = Path(context["checkpoint_root"])
    record_path = checkpoint_root / "PREPARATION.json"
    identity = _preparation_identity(branch, phase, request, context)
    if record_path.exists():
        record = load_json(record_path)
        if (
            record.get("schema") != PREPARATION_SCHEMA
            or record.get("identity") != identity
            or not isinstance(record.get("payload"), dict)
        ):
            raise EvidenceError("phase preparation identity mismatch at {}".format(record_path))
        _validate_preparation_artifacts(record["payload"])
        return dict(record["payload"]), sha256_file(record_path)
    if resume:
        # A preparation hook may checkpoint its own incomplete event DAG under
        # shared_root and resume from there.  Absence of PREPARATION.json means
        # only that the parent-side preparation never reached its commit gate.
        context["preparation_resume"] = True
    payload = prepare(branch, phase, request, dict(context))
    if not isinstance(payload, dict):
        raise EvidenceError("kernel prepare_phase did not return an object")
    _validate_preparation_artifacts(payload)
    record = {"schema": PREPARATION_SCHEMA, "identity": identity, "payload": payload}
    immutable_write_json(record_path, record)
    mirror.publish(record_path, "PREPARATION.json")
    return payload, sha256_file(record_path)


def validate_branch_result(payload: Mapping[str, Any], branch: str, phase: str, request: Mapping[str, Any]) -> None:
    if payload.get("schema") != BRANCH_SCHEMA:
        raise EvidenceError("wrong branch-result schema")
    if payload.get("length") != 14 or payload.get("branch") != branch or payload.get("phase") != phase:
        raise EvidenceError("branch-result identity mismatch")
    if payload.get("computed_sectors") != request.get("sectors"):
        raise EvidenceError("branch-result sector mismatch")
    validation = payload.get("numerical_validation")
    if not isinstance(validation, dict):
        raise EvidenceError("missing numerical_validation")
    required_predicates = (
        "all_actual_and_null_solvers_converged",
        "residual_l1_within_original_bound",
        "actual_norm_error_within_original_bound",
        "transport_number_drift_within_original_bound",
        "rough_sharp_agreement_within_original_bound",
    )
    for predicate in required_predicates:
        if validation.get(predicate) is not True:
            raise EvidenceError("original numerical predicate failed: {}".format(predicate))
    comparison = payload.get("comparison_evidence")
    if not isinstance(comparison, dict):
        raise EvidenceError("comparison_evidence is absent")
    raw_metrics = comparison.get("raw_metrics")
    thresholds = comparison.get("predicate_thresholds")
    required_metrics = (
        "reverse_support_probability",
        "transport_node_residual_l1",
        "actual_norm_error",
        "transport_number_drift",
    )
    if not isinstance(raw_metrics, dict) or not isinstance(thresholds, dict):
        raise EvidenceError("raw comparison metrics or thresholds are absent")
    for metric in required_metrics:
        finite_decimal(raw_metrics.get(metric), "raw metric {}".format(metric))
        if metric not in thresholds:
            raise EvidenceError("predicate threshold absent for {}".format(metric))
    masses = payload.get("sector_masses")
    required_mass_sectors = request.get("mass_ledger_sectors")
    if (
        not isinstance(masses, dict)
        or not isinstance(required_mass_sectors, list)
        or sorted(int(key) for key in masses) != sorted(required_mass_sectors)
    ):
        raise EvidenceError("branch-result sector mass ledger is incomplete")
    for key, value in masses.items():
        mass = finite_decimal(value, "sector mass {}".format(key))
        if not Decimal(0) <= mass <= Decimal(1):
            raise EvidenceError("invalid mass for sector {}".format(key))
    atoms = payload.get("atoms")
    if not isinstance(atoms, list):
        raise EvidenceError("branch-result atoms must be a list")
    seen = set()
    for atom in atoms:
        if not isinstance(atom, dict):
            raise EvidenceError("malformed atom")
        atom_id = atom.get("atom_id")
        q = atom.get("q")
        interval = atom.get("density_interval")
        geometry = atom.get("geometry")
        if not isinstance(atom_id, str) or atom_id in seen:
            raise EvidenceError("missing or duplicate atom_id")
        seen.add(atom_id)
        if q not in request.get("sectors"):
            raise EvidenceError("atom q outside requested sectors: {}".format(atom_id))
        if (
            not isinstance(interval, list)
            or len(interval) != 2
            or not all(
                isinstance(bound, list)
                and len(bound) == 2
                and type(bound[0]) is int
                and type(bound[1]) is int
                and bound[1] > 0
                for bound in interval
            )
        ):
            raise EvidenceError("invalid density interval: {}".format(atom_id))
        if interval[0][0] * interval[1][1] >= interval[1][0] * interval[0][1]:
            raise EvidenceError("empty density interval: {}".format(atom_id))
        if not isinstance(geometry, dict) or geometry.get("resolved") is not True:
            raise EvidenceError("unresolved atom geometry: {}".format(atom_id))
        for coordinate in ("z", "y"):
            value = geometry.get(coordinate)
            finite_decimal(value, "{} coordinate {}".format(coordinate, atom_id))


def main(argv: Sequence[str] = ()) -> int:
    args = parse_args(argv or sys.argv[1:])
    request = load_json(args.request)
    validate_request(request, args.branch, args.phase)
    kernel_path = args.kernel_module.resolve()
    kernel = _load_module(str(kernel_path))
    for name in ("build_task_plan", "run_task", "reduce_results"):
        if not callable(getattr(kernel, name, None)):
            raise EvidenceError("kernel lacks required callable: {}".format(name))

    context: Dict[str, Any] = {
        "branch": args.branch,
        "phase": args.phase,
        "checkpoint_root": str(args.checkpoint_root.resolve()),
        "kernel_sha256": sha256_file(kernel_path),
        "request_sha256": sha256_file(args.request),
        "workers": args.workers,
        "resume": bool(args.resume),
        "shared_root": str((args.shared_root or (args.checkpoint_root / "shared")).resolve()),
        "scratch_root": str((args.scratch_root or args.checkpoint_root).resolve()),
    }
    mirror = DurableMirror(args.mirror_destination)
    preparation, preparation_sha256 = prepare_kernel_phase(
        kernel,
        args.branch,
        args.phase,
        request,
        context,
        args.resume,
        mirror,
    )
    context["preparation"] = preparation
    context["preparation_sha256"] = preparation_sha256
    tasks = make_tasks(kernel.build_task_plan(args.branch, args.phase, request, context))
    run_id = request["run_id"]
    runtime = ResumableProcessPool(
        checkpoint_root=args.checkpoint_root,
        run_id=run_id,
        branch=args.branch,
        phase=args.phase,
        kernel_module=kernel_path,
        kernel_function="run_task",
        tasks=tasks,
        workers=args.workers,
        parameters={
            "length": 14,
            "phase": args.phase,
            "sectors": request["sectors"],
            "geometry_window": request["geometry_window"],
            "request_sha256": sha256_file(args.request),
            "preparation_sha256": preparation_sha256,
            "shared_root": context["shared_root"],
            "scratch_root": context["scratch_root"],
        },
        mirror_destination=args.mirror_destination,
    )
    outcome = runtime.run(resume=args.resume)
    if outcome.status == "STOPPED":
        print(
            "L14_BRANCH_STOPPED branch={} phase={} completed={}/{}".format(
                args.branch, args.phase, outcome.completed, outcome.total
            ),
            flush=True,
        )
        return 75

    results = load_task_results(args.checkpoint_root, tasks)
    reduce_context = dict(context)
    reduce_context["task_result_set_sha256"] = load_json(args.checkpoint_root / "COMPLETE.json")["result_set_sha256"]
    branch_result = kernel.reduce_results(args.branch, args.phase, request, results, reduce_context)
    if not isinstance(branch_result, dict):
        raise EvidenceError("kernel reducer did not return an object")
    validate_branch_result(branch_result, args.branch, args.phase, request)
    immutable_write_json(args.output, branch_result)
    mirror.publish(args.output, "BRANCH_RESULT.json")
    print(
        "L14_BRANCH_COMPLETE branch={} phase={} tasks={} output={} sha256={}".format(
            args.branch, args.phase, len(tasks), args.output, sha256_file(args.output)
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_BRANCH_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr, flush=True)
        raise SystemExit(2)
