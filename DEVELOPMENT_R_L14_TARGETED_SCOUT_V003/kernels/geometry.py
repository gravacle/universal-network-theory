#!/usr/bin/env python3
"""Shared orchestration for the independent exact L14 response kernels.

Only bookkeeping is shared.  Target and Hostile compute their L14 response
rows with separate frozen implementations and are compared only after both
branch results have been durably published.
"""

from __future__ import annotations

import math
import os
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Mapping

from cache_builder import build_cache
from checkpointed_history import prepare_history
from exact_common import (
    ExactKernelRefusal,
    artifact,
    immutable_json,
    jsonable,
    load_frozen,
    packet_root,
    read_json,
)


LENGTH = 14
SIZES = (4, 6, 8, 10, 12, 14)
# L14 does not turn execution estimates into scientific rejection predicates.
# Linux/AWS own hardware health and the branch scheduler owns concurrency.  The
# frozen response kernels still report elapsed time, RSS, and matvec counts, but
# these sentinel values keep their legacy execution guards from rejecting an
# otherwise valid numerical row.
EXECUTION_GUARD_SENTINEL = 1 << 62


def _pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def _q_at_density(length: int, value: Fraction) -> int:
    shifted = 2 * length * value + Fraction(1, 2)
    return min(length, max(0, shifted.numerator // shifted.denominator))


def _atoms() -> list[dict[str, Any]]:
    lower, upper = Fraction(1, 48), Fraction(17, 48)
    boundaries = {lower, upper}
    for length in SIZES:
        for q in range(length):
            boundary = Fraction(2 * q + 1, 4 * length)
            if lower < boundary < upper:
                boundaries.add(boundary)
    ordered = sorted(boundaries)
    atoms = []
    for index, (left, right) in enumerate(zip(ordered, ordered[1:])):
        midpoint = (left + right) / 2
        atoms.append(
            {
                "atom_id": "L14A{:03d}".format(index),
                "density_interval": [_pair(left), _pair(right)],
                "q_by_L": {str(length): _q_at_density(length, midpoint) for length in SIZES},
                "midpoint": midpoint,
            }
        )
    return atoms


def _prior_adjudication() -> dict[str, Any]:
    path = packet_root() / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001" / "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json"
    payload = read_json(path)
    if payload.get("schema") != "RELATIONAL_INTERVAL_SPECTRUM_ADJUDICATION_V001":
        raise ExactKernelRefusal("prior Stage-6R2 adjudication identity mismatch")
    return payload


def _fraction(pair: list[int]) -> Fraction:
    return Fraction(int(pair[0]), int(pair[1]))


def _predecessor(atom: Mapping[str, Any], prior: Mapping[str, Any]) -> Mapping[str, Any]:
    midpoint = atom["midpoint"]
    matches = []
    for result in prior["atom_results"]:
        old = result["atom"]
        left, right = (_fraction(value) for value in old["density_interval"])
        if left < midpoint < right:
            matches.append(result)
    if len(matches) != 1:
        raise ExactKernelRefusal("L14 atom does not have exactly one L12 predecessor")
    return matches[0]


def prepare_phase(branch: str, phase: str, request: Mapping[str, Any], context: Mapping[str, Any]) -> Dict[str, Any]:
    del phase, request
    shared = Path(str(context["shared_root"])).resolve() / branch
    cache_root = shared / "cache_l14"
    build_cache(cache_root, branch, LENGTH)
    return prepare_history(branch, context)


def build_task_plan(branch: str, phase: str, request: Mapping[str, Any], context: Mapping[str, Any]) -> list[dict[str, Any]]:
    del branch, phase
    root = Path(str(context["checkpoint_root"])).resolve() / "artifacts"
    tasks = []
    for q in request["sectors"]:
        tasks.append(
            {
                "task_id": "response_q{:02d}".format(q),
                "payload": {"q": q, "output": str(root / "response_q{:02d}.json".format(q))},
                "work_units": max(1, math.comb(2 * LENGTH, q)),
            }
        )
    return tasks


def _target_row(q: int, output: Path, target: Any) -> dict[str, Any]:
    if output.exists():
        row = read_json(output)
    else:
        temporary = output.parent / ("." + output.name + ".{}.compute".format(os.getpid()))
        if temporary.exists():
            temporary.unlink()
        target.TARGET_ROWS[LENGTH] = (4, 5, 6, 7, 8, 9)
        target.RSS_LIMIT_BYTES = EXECUTION_GUARD_SENTINEL
        target.SECTOR_SECONDS_LIMIT = math.inf
        target.worker(LENGTH, q, temporary)
        row = read_json(temporary)
        immutable_json(output, row)
        temporary.unlink()
    if row.get("L") != LENGTH or row.get("q") != q or row.get("status") != "RESOLVED":
        raise ExactKernelRefusal("Target response row failed closed for q={}".format(q))
    return row


def _hostile_row(q: int, output: Path, hostile: Any) -> dict[str, Any]:
    if output.exists():
        row = read_json(output)
    else:
        hostile.FUTURE_ROWS = tuple(sorted(set(hostile.FUTURE_ROWS + tuple((LENGTH, charge) for charge in range(4, 10)))))
        hostile.RSS_LIMIT_BYTES = EXECUTION_GUARD_SENTINEL
        hostile.WALL_LIMIT_SECONDS = math.inf
        hostile.MATVEC_LIMIT = EXECUTION_GUARD_SENTINEL
        row = hostile.calculate_row(LENGTH, q, hostile.AUTHORIZATION)
        immutable_json(output, row)
    if row.get("L") != LENGTH or row.get("q") != q or row.get("status") != "RESOLVED":
        raise ExactKernelRefusal("Hostile response row failed closed for q={}".format(q))
    return row


def run_task(branch: str, payload: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    del context
    q = int(payload["q"])
    if q not in range(4, 10):
        raise ExactKernelRefusal("response q is outside frozen scout scope")
    output = Path(str(payload["output"])).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    _repair, target, hostile, _classifier, _interval = load_frozen()
    row = _target_row(q, output, target) if branch == "target" else _hostile_row(q, output, hostile)
    return {"q": q, "row": jsonable(row), "artifacts": [artifact(output)]}


def _metric_threshold(evidence: Mapping[str, Any], metric: str) -> float:
    threshold = evidence["predicate_thresholds"][metric]
    if isinstance(threshold, Mapping):
        threshold = threshold.get("value")
    value = float(threshold)
    if not math.isfinite(value):
        raise ExactKernelRefusal("non-finite threshold for {}".format(metric))
    return value


def _validation(history: Mapping[str, Any]) -> dict[str, bool]:
    evidence = history["comparison_evidence"]
    raw = evidence["raw_metrics"]
    rows = history["sharp"]["rows"]
    solvers = all(
        row.get(name, {}).get("converged") is True
        for row in rows
        for name in ("actual_solver", "null_solver")
    )
    return {
        "all_actual_and_null_solvers_converged": solvers,
        "residual_l1_within_original_bound": float(raw["transport_node_residual_l1"]) <= _metric_threshold(evidence, "transport_node_residual_l1"),
        "actual_norm_error_within_original_bound": float(raw["actual_norm_error"]) <= _metric_threshold(evidence, "actual_norm_error"),
        "transport_number_drift_within_original_bound": float(raw["transport_number_drift"]) <= _metric_threshold(evidence, "transport_number_drift"),
        "rough_sharp_agreement_within_original_bound": evidence["comparison"].get("resolved") is True,
        "all_original_prepublication_predicates_passed": evidence.get("computed_resolved") is True,
        "reported_resolution_agrees_with_predicates": evidence.get("resolved_agrees_with_predicates") is True,
    }


def reduce_results(branch: str, phase: str, request: Mapping[str, Any], results: list[Mapping[str, Any]], context: Mapping[str, Any]) -> dict[str, Any]:
    preparation = context.get("preparation")
    if not isinstance(preparation, Mapping) or not isinstance(preparation.get("history"), Mapping):
        raise ExactKernelRefusal("authenticated exact history preparation is absent")
    history = preparation["history"]
    rows = {int(result["q"]): result["row"] for result in results}
    if set(rows) != set(request["sectors"]):
        raise ExactKernelRefusal("response task census mismatch")
    _repair, _target, _hostile, classifier, _interval = load_frozen()
    prior = _prior_adjudication()
    atoms = []
    for atom in _atoms():
        q = int(atom["q_by_L"]["14"])
        if q not in rows:
            continue
        predecessor = _predecessor(atom, prior)
        old_classification = predecessor["target_classification" if branch == "target" else "blind_classification"]
        if not isinstance(old_classification, Mapping) or len(old_classification.get("rows", [])) != 5:
            raise ExactKernelRefusal("predecessor classification is unresolved")
        new_row = {
            "L": LENGTH,
            "rho_anchor": q / (2 * LENGTH),
            "source_q": [q],
            "weights": [1.0],
            **{key: float(rows[q][key]) for key in ("Delta_act", "chi_tau", "R_low")},
        }
        classification = classifier.classify(list(old_classification["rows"]) + [new_row])
        z = float(classification["gap_power_fit"]["exponent"])
        y = float(classification["chi_power_exponent_y"])
        atoms.append(
            {
                "atom_id": atom["atom_id"],
                "q": q,
                "density_interval": atom["density_interval"],
                "q_by_L": atom["q_by_L"],
                "predecessor_atom_id": predecessor["atom"]["atom_id"],
                "geometry": {
                    "resolved": True,
                    "z": z,
                    "y": y,
                    "passes_window": 0.90 <= z <= 1.10 and 0.90 <= y <= 1.10,
                    "passes_full_conjunction": classification.get("passes") is True,
                    "classification": jsonable(classification),
                },
                "l14_response": {key: jsonable(value) for key, value in rows[q].items() if key not in {"ground_sequence", "response_sequence"}},
            }
        )
    validation = _validation(history)
    if not all(validation.values()):
        raise ExactKernelRefusal("original numerical validation failed: {}".format(validation))
    return {
        "schema": "L14_SCOUT_BRANCH_RESULT_V002",
        "length": LENGTH,
        "branch": branch,
        "phase": phase,
        "computed_sectors": list(request["sectors"]),
        "sector_masses": dict(history["sector_masses"]),
        "numerical_validation": validation,
        "comparison_evidence": history["comparison_evidence"],
        "atoms": atoms,
        "provenance": {
            "history_preparation_sha256": context.get("preparation_sha256"),
            "task_result_set_sha256": context.get("task_result_set_sha256"),
            "classification_sizes": list(SIZES),
            "geometry_policy": "Z_AND_Y_EACH_IN_CLOSED_INTERVAL_0.90_1.10",
        },
    }
