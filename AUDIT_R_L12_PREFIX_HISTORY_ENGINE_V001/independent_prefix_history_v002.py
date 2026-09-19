#!/usr/bin/env python3
"""Low-memory recurrence-replay supplement for the frozen hostile engine."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

import independent_prefix_history as base


HERE = Path(__file__).resolve().parent
CONTROL_GATE = HERE / "CONTROL_GATE_V002.json"
SEALED_L10_GATE = HERE / "SEALED_L10_GATE_V002.json"
QUADRATURE_GROUP = 12
ALLOCATION_VECTOR_SLOTS = 20
WORKSPACE_LIMIT = 1_400_000_000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allocation_estimate(vector_bytes: int) -> int:
    return ALLOCATION_VECTOR_SLOTS * vector_bytes


def safe_batch_rows(columns: int, degree: int, amplitude_window: int | None = None) -> int:
    del degree
    one_row = columns * 16
    if amplitude_window is not None and one_row > amplitude_window:
        raise MemoryError(
            f"one amplitude row exceeds terminal window: {one_row} > {amplitude_window}"
        )
    if allocation_estimate(one_row) > WORKSPACE_LIMIT:
        raise MemoryError(
            f"one recurrence-replay row exceeds workspace: "
            f"{allocation_estimate(one_row)} > {WORKSPACE_LIMIT}"
        )
    rows = WORKSPACE_LIMIT // allocation_estimate(one_row)
    if amplitude_window is not None:
        rows = min(rows, amplitude_window // one_row)
    if rows < 1:
        raise MemoryError("no row fits the frozen allocation guards")
    estimate = allocation_estimate(rows * one_row)
    if estimate > WORKSPACE_LIMIT:
        raise MemoryError(f"batch estimate exceeds workspace: {estimate} > {WORKSPACE_LIMIT}")
    return int(rows)


def endpoint_selection(
    carrier: base.CarrierBlock, vector: np.ndarray, accuracy: base.Accuracy
) -> tuple[np.ndarray, int, float, float, bool]:
    flat = vector.reshape(-1)
    maximum = max(accuracy.checkpoints)
    scale = 3.0 * carrier.q
    coefficient = np.asarray(base.coefficients(scale, base.ROUTE_TIME, maximum),
                             dtype=np.complex128)
    previous_term = flat
    accumulator = coefficient[0] * flat
    current_term = carrier.multiply(vector).reshape(-1)
    current_term /= scale
    accumulator += coefficient[1] * current_term
    prior_checkpoint: np.ndarray | None = None
    selected_degree = 0
    selected_difference = math.inf
    selected_tail = math.inf
    converged = False
    for degree in range(2, maximum + 1):
        following = carrier.multiply(current_term.reshape(vector.shape)).reshape(-1)
        following *= 2.0 / scale
        following -= previous_term
        accumulator += coefficient[degree] * following
        previous_term, current_term = current_term, following
        if degree in accuracy.checkpoints:
            difference = (
                math.inf if prior_checkpoint is None
                else float(np.linalg.norm(accumulator - prior_checkpoint))
            )
            indicator = base.tail_indicator(scale, base.ROUTE_TIME, degree)
            selected_degree = degree
            selected_difference = difference
            selected_tail = indicator
            if prior_checkpoint is not None and difference <= accuracy.tolerance \
                    and indicator <= accuracy.tolerance:
                converged = True
                break
            prior_checkpoint = accumulator.copy()
    return accumulator.copy(), selected_degree, selected_difference, selected_tail, converged


def quadrature_replay(
    carrier: base.CarrierBlock, vector: np.ndarray, accuracy: base.Accuracy, degree: int
) -> np.ndarray:
    flat = vector.reshape(-1)
    scale = 3.0 * carrier.q
    nodes, weights = np.polynomial.legendre.leggauss(accuracy.gauss_order)
    integrated = np.zeros(len(carrier.exchanges))
    for group_start in range(0, len(nodes), QUADRATURE_GROUP):
        group_stop = min(len(nodes), group_start + QUADRATURE_GROUP)
        group_nodes = nodes[group_start:group_stop]
        group_weights = weights[group_start:group_stop]
        elapsed = 0.5 * base.ROUTE_TIME * (group_nodes + 1.0)
        coefficient = np.asarray(
            [base.coefficients(scale, float(time), degree) for time in elapsed],
            dtype=np.complex128,
        )
        samples = coefficient[:, 0, np.newaxis] * flat[np.newaxis, :]
        previous_term = flat
        current_term = carrier.multiply(vector).reshape(-1)
        current_term /= scale
        samples += coefficient[:, 1, np.newaxis] * current_term[np.newaxis, :]
        for order in range(2, degree + 1):
            following = carrier.multiply(current_term.reshape(vector.shape)).reshape(-1)
            following *= 2.0 / scale
            following -= previous_term
            samples += coefficient[:, order, np.newaxis] * following[np.newaxis, :]
            previous_term, current_term = current_term, following
        for index, weight in enumerate(group_weights):
            integrated += float(weight) * carrier.currents(samples[index].reshape(vector.shape))
    return 0.5 * base.ROUTE_TIME * integrated


def low_memory_evolve_batch(
    carrier: base.CarrierBlock, vector: np.ndarray, accuracy: base.Accuracy
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    flat = vector.reshape(-1)
    estimate = allocation_estimate(flat.nbytes)
    if estimate > WORKSPACE_LIMIT:
        raise MemoryError(f"frozen allocation estimate exceeded: {estimate} > {WORKSPACE_LIMIT}")
    if not np.any(flat) or carrier.q == 0:
        return vector.copy(), np.zeros(len(carrier.exchanges)), {
            "converged": True,
            "degree": 0,
            "endpoint_difference": 0.0,
            "tail_indicator_32": 0.0,
            "algorithm": "RECURRENCE_REPLAY_GL_GROUPS",
            "quadrature_group_max": QUADRATURE_GROUP,
            "allocation_vector_slots": ALLOCATION_VECTOR_SLOTS,
            "allocation_estimate_bytes": estimate,
            "allocation_limit_bytes": WORKSPACE_LIMIT,
        }
    final, degree, difference, indicator, converged = endpoint_selection(
        carrier, vector, accuracy
    )
    integrated = quadrature_replay(carrier, vector, accuracy, degree)
    return final.reshape(vector.shape), integrated, {
        "converged": converged,
        "degree": degree,
        "endpoint_difference": difference,
        "tail_indicator_32": indicator,
        "algorithm": "RECURRENCE_REPLAY_GL_GROUPS",
        "quadrature_group_max": QUADRATURE_GROUP,
        "allocation_vector_slots": ALLOCATION_VECTOR_SLOTS,
        "allocation_estimate_bytes": estimate,
        "allocation_limit_bytes": WORKSPACE_LIMIT,
    }


def blank_method(edge_count: int) -> dict[str, object]:
    del edge_count
    return {
        "converged": True,
        "batches": 0,
        "maximum_degree": 0,
        "maximum_endpoint_difference": 0.0,
        "maximum_tail_indicator_32": 0.0,
        "algorithm": "RECURRENCE_REPLAY_GL_GROUPS",
        "quadrature_group_max": QUADRATURE_GROUP,
        "allocation_vector_slots": ALLOCATION_VECTOR_SLOTS,
        "maximum_allocation_estimate_bytes": 0,
        "allocation_limit_bytes": WORKSPACE_LIMIT,
    }


_base_combine_method = base.combine_method


def combine_method(total: dict[str, object], record: dict[str, object]) -> None:
    _base_combine_method(total, record)
    total["maximum_allocation_estimate_bytes"] = max(
        int(total["maximum_allocation_estimate_bytes"]),
        int(record["allocation_estimate_bytes"]),
    )


def require_gate(path: Path, classification: str) -> None:
    if not path.exists():
        raise RuntimeError(f"required V002 sealed gate is absent: {path.name}")
    record = json.loads(path.read_text())
    if record.get("classification") != classification:
        raise RuntimeError(f"required V002 gate did not pass: {path.name}")
    if record.get("implementation_sha256") != sha256(Path(__file__)):
        raise RuntimeError(f"required V002 gate does not pin this implementation: {path.name}")


def authorize(length: int) -> None:
    if length in base.CONTROL_SIZES:
        return
    if length == 10:
        require_gate(CONTROL_GATE, "PASS_PREFIX_HISTORY_CONTROLS_L4_L8_V002")
        return
    if length == 12:
        require_gate(CONTROL_GATE, "PASS_PREFIX_HISTORY_CONTROLS_L4_L8_V002")
        require_gate(SEALED_L10_GATE, "PASS_PREFIX_HISTORY_L10_GATE_V002")
        free = base.shutil.disk_usage(HERE).free
        if free < base.L12_SCRATCH_GATE:
            raise RuntimeError(
                f"L12 scratch gate failed: free={free} required={base.L12_SCRATCH_GATE}"
            )
        return
    raise ValueError("supported even sizes are 4, 6, 8, 10, and 12")


def run(length: int, output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"V002 refuses to overwrite custody output: {output}")
    base.evolve_batch = low_memory_evolve_batch
    base.batch_rows = safe_batch_rows
    base.blank_method = blank_method
    base.combine_method = combine_method
    base.authorize = authorize
    exit_code = 0
    try:
        base.run(length, output)
    except SystemExit as error:
        exit_code = int(error.code or 0)
    if not output.exists():
        raise AssertionError("V002 base engine produced no result")
    result = json.loads(output.read_text())
    base_hash = result["implementation_sha256"]
    result["schema"] = "INDEPENDENT_PREFIX_LINEAGE_HISTORY_CONTROL_V002"
    result["low_memory_repair"] = {
        "base_implementation_sha256": base_hash,
        "wrapper_implementation_sha256": sha256(Path(__file__)),
        "base_methodology_sha256": result["methodology_sha256"],
        "supplement_sha256": sha256(HERE / "V002_LOW_MEMORY_SUPPLEMENT.md"),
        "algorithm": "RECURRENCE_REPLAY_GL_GROUPS",
        "quadrature_group_max": QUADRATURE_GROUP,
        "allocation_vector_slots": ALLOCATION_VECTOR_SLOTS,
        "workspace_limit_bytes": WORKSPACE_LIMIT,
        "physical_operator_changed": False,
        "basis_or_branch_changed": False,
        "degree_or_tolerance_changed": False,
        "observable_or_ledger_changed": False,
    }
    result["implementation_sha256"] = sha256(Path(__file__))
    result["methodology_sha256"] = sha256(HERE / "V002_LOW_MEMORY_SUPPLEMENT.md")
    result["claim_boundary"] = "INDEPENDENT_FINITE_PREFIX_HISTORY_V002_CONTROL_ONLY"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if exit_code:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.worker, arguments.output)
