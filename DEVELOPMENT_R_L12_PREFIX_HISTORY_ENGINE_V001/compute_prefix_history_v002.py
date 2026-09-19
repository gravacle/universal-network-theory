#!/usr/bin/env python3
"""Terminal-streamed, memory-bounded Lanczos prefix-history target."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import compute_prefix_history as v1  # noqa: E402


sealed = v1.sealed
CAP_BYTES = 1_000_000_000
TERMINAL_WINDOW_BYTES = 512 * 2**20
MAX_SUBDIVISIONS = 16
FORCED_LOW_MEMORY_L10_Q = (9, 10)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def segment_lanczos(sector, vector, resolution, elapsed: float, tolerance: float,
                    maximum: int):
    flat = vector.reshape(-1)
    norm = float(np.linalg.norm(flat))
    if norm <= 1e-30 or sector.q == 0 or len(sector.words) == 1:
        return vector.copy(), np.zeros(len(sector.pairs)), {
            "steps": 0, "converged": True, "exp_difference": 0.0,
            "residual_indicator": 0.0,
        }
    if (maximum + 4) * flat.size * 16 > CAP_BYTES:
        raise MemoryError("low-memory Lanczos live-vector bound exceeded")
    basis = np.empty((maximum, flat.size), dtype=np.complex128)
    basis[0] = flat / norm
    alphas = []
    betas = []
    previous = None
    selected = None
    selected_coefficients = None
    selected_dimension = 0
    selected_difference = math.inf
    selected_residual = math.inf
    converged = False
    first_checkpoint = max(4, maximum // 2)
    checkpoints = {first_checkpoint, maximum}
    for step in range(maximum):
        work = sector.h(basis[step].reshape(vector.shape)).reshape(-1)
        if step:
            work -= betas[step - 1] * basis[step - 1]
        alpha = float(np.vdot(basis[step], work).real)
        work -= alpha * basis[step]
        for prior in range(max(0, step - 2), step + 1):
            work -= np.vdot(basis[prior], work) * basis[prior]
        beta = float(np.linalg.norm(work))
        alphas.append(alpha)
        dimension = step + 1
        if dimension in checkpoints or beta <= 1e-14:
            coefficients = sealed.tridiagonal_coefficients(
                alphas, betas, dimension, elapsed, norm
            )
            candidate = np.einsum("i,ij->j", coefficients, basis[:dimension], optimize=False)
            difference = math.inf if previous is None else float(np.linalg.norm(candidate - previous))
            residual = beta * abs(complex(coefficients[-1]))
            selected = candidate
            selected_coefficients = coefficients
            selected_dimension = dimension
            selected_difference = difference
            selected_residual = residual
            if previous is not None and difference <= tolerance and residual <= tolerance:
                converged = True
                break
            previous = candidate
        if beta <= 1e-14:
            converged = True
            break
        if dimension < maximum:
            betas.append(beta)
            basis[dimension] = work / beta
    if selected is None or selected_coefficients is None:
        raise AssertionError("no low-memory Lanczos endpoint")
    nodes, weights = np.polynomial.legendre.leggauss(resolution.quadrature_nodes)
    integrated = np.zeros(len(sector.pairs))
    for node, weight in zip(nodes, weights):
        local_time = 0.5 * elapsed * (float(node) + 1.0)
        coefficients = sealed.tridiagonal_coefficients(
            alphas, betas, selected_dimension, local_time, norm
        )
        sample = np.einsum(
            "i,ij->j", coefficients, basis[:selected_dimension], optimize=False
        ).reshape(vector.shape)
        integrated += float(weight) * sector.currents(sample)
    integrated *= 0.5 * elapsed
    return selected.reshape(vector.shape), integrated, {
        "steps": selected_dimension,
        "converged": converged,
        "exp_difference": selected_difference,
        "residual_indicator": selected_residual,
    }


def low_memory_propagate(sector, vector, resolution):
    vector_bytes = vector.size * 16
    maximum = min(max(resolution.checkpoints), CAP_BYTES // vector_bytes - 4)
    if maximum < 8:
        raise MemoryError("one physical row cannot satisfy the frozen Lanczos cap")
    initial = max(1, math.ceil(max(resolution.checkpoints) / maximum))
    subdivisions = 1
    while subdivisions < initial:
        subdivisions *= 2
    while subdivisions <= MAX_SUBDIVISIONS:
        state = vector.copy()
        integrated = np.zeros(len(sector.pairs))
        records = []
        elapsed = sealed.DWELL / subdivisions
        for _ in range(subdivisions):
            state, current, record = segment_lanczos(
                sector, state, resolution, elapsed,
                resolution.tolerance / subdivisions, int(maximum),
            )
            integrated += current
            records.append(record)
            if not record["converged"]:
                break
        if len(records) == subdivisions and all(record["converged"] for record in records):
            finite_differences = [float(record["exp_difference"]) for record in records
                                  if math.isfinite(float(record["exp_difference"]))]
            return state, integrated, {
                "steps": max(int(record["steps"]) for record in records),
                "converged": True,
                "exp_difference": max(finite_differences, default=0.0),
                "residual_indicator": max(float(record["residual_indicator"])
                                          for record in records),
                "low_memory": True,
                "subdivisions": subdivisions,
                "maximum_live_bytes": int((maximum + 4) * vector_bytes),
            }
        subdivisions *= 2
    return vector.copy(), np.zeros(len(sector.pairs)), {
        "steps": int(maximum), "converged": False, "exp_difference": math.inf,
        "residual_indicator": math.inf, "low_memory": True,
        "subdivisions": MAX_SUBDIVISIONS, "maximum_live_bytes": int((maximum + 4) * vector_bytes),
    }


def empty_solver(resolution):
    return {
        "converged": True, "batches": 0, "maximum_krylov_steps": 0,
        "maximum_exp_difference": 0.0, "maximum_residual_indicator": 0.0,
        "quadrature_nodes": resolution.quadrature_nodes,
        "low_memory_batches": 0, "maximum_subdivisions": 1,
        "maximum_live_bytes": 0,
    }


def update_solver(total, record):
    total["converged"] = total["converged"] and bool(record["converged"])
    total["batches"] += 1
    total["maximum_krylov_steps"] = max(total["maximum_krylov_steps"], int(record["steps"]))
    if math.isfinite(float(record["exp_difference"])):
        total["maximum_exp_difference"] = max(total["maximum_exp_difference"],
                                               float(record["exp_difference"]))
    total["maximum_residual_indicator"] = max(total["maximum_residual_indicator"],
                                               float(record["residual_indicator"]))
    total["maximum_live_bytes"] = max(total["maximum_live_bytes"],
                                       int(record["maximum_live_bytes"]))
    if record.get("low_memory"):
        total["low_memory_batches"] += 1
        total["maximum_subdivisions"] = max(total["maximum_subdivisions"],
                                             int(record["subdivisions"]))


def propagate_dispatch(length: int, sector, vector, resolution):
    forced = length == 10 and sector.q in FORCED_LOW_MEMORY_L10_Q
    ordinary_bytes = (max(resolution.checkpoints) + 4) * vector.size * 16
    if forced or ordinary_bytes > CAP_BYTES:
        return low_memory_propagate(sector, vector, resolution)
    evolved, current, record = sealed.propagate_batch(sector, vector, resolution)
    record = dict(record)
    record.update({"low_memory": False, "subdivisions": 1,
                   "maximum_live_bytes": int(ordinary_bytes)})
    if ordinary_bytes > CAP_BYTES:
        raise MemoryError("ordinary Lanczos cap exceeded")
    return evolved, current, record


def block_statistics(parent, q: int, block):
    probability = np.sum(np.abs(block) ** 2, axis=0)
    occupation = np.zeros(parent.sites)
    words = parent.sectors[q].words
    for site in range(parent.sites):
        occupation[site] = float(np.sum(probability[((words >> site) & 1) == 1]))
    return float(np.sum(probability)), occupation


def batch_rows(columns: int, resolution, force_low: bool) -> int:
    amplitude_rows = max(1, TERMINAL_WINDOW_BYTES // (columns * 16))
    if force_low:
        maximum = min(max(resolution.checkpoints), 20)
        krylov_rows = max(1, CAP_BYTES // ((maximum + 4) * columns * 16))
    else:
        krylov_rows = max(1, CAP_BYTES // ((max(resolution.checkpoints) + 4) * columns * 16))
    return int(max(1, min(amplitude_rows, krylov_rows)))


def terminal_actual(parent, before, event: int, resolution):
    admitted_sectors = np.zeros(parent.length + 1)
    admitted_occupation = np.zeros(parent.sites)
    after_sectors = np.zeros(parent.length + 1)
    after_occupation = np.zeros(parent.sites)
    current = np.zeros(len(parent.edges))
    solver = empty_solver(resolution)
    cosine = math.cos(sealed.PHI)
    sine = math.sin(sealed.PHI)
    blocked_error = 0.0
    for q, old in enumerate(before):
        words = parent.sectors[q].words
        blank_columns = np.flatnonzero(((words >> event) & 1) == 0).astype(np.int32)
        occupied_columns = np.flatnonzero(((words >> event) & 1) == 1).astype(np.int32)
        force_zero = parent.length == 10 and q in FORCED_LOW_MEMORY_L10_Q
        rows = batch_rows(len(words), resolution, force_zero)
        for lower in range(0, old.shape[0], rows):
            upper = min(old.shape[0], lower + rows)
            child = old[lower:upper].copy()
            child[:, blank_columns] *= cosine
            if len(occupied_columns):
                blocked_error = max(blocked_error, float(np.max(np.abs(
                    child[:, occupied_columns] - old[lower:upper, occupied_columns]
                ))))
            norm, occupation = block_statistics(parent, q, child)
            admitted_sectors[q] += norm
            admitted_occupation += occupation
            evolved, flux, record = propagate_dispatch(parent.length, parent.sectors[q], child, resolution)
            norm, occupation = block_statistics(parent, q, evolved)
            after_sectors[q] += norm
            after_occupation += occupation
            current += flux
            update_solver(solver, record)
        if not len(blank_columns):
            continue
        destination = parent.sectors[q + 1]
        destination_columns = np.fromiter(
            (destination.lookup[int(words[column]) | (1 << event)] for column in blank_columns),
            dtype=np.int32, count=len(blank_columns),
        )
        force_one = parent.length == 10 and q + 1 in FORCED_LOW_MEMORY_L10_Q
        rows = batch_rows(len(destination.words), resolution, force_one)
        for lower in range(0, old.shape[0], rows):
            upper = min(old.shape[0], lower + rows)
            child = np.zeros((upper - lower, len(destination.words)), dtype=np.complex128)
            child[:, destination_columns] = -1.0j * sine * old[lower:upper, blank_columns]
            norm, occupation = block_statistics(parent, q + 1, child)
            admitted_sectors[q + 1] += norm
            admitted_occupation += occupation
            evolved, flux, record = propagate_dispatch(parent.length, destination, child, resolution)
            norm, occupation = block_statistics(parent, q + 1, evolved)
            after_sectors[q + 1] += norm
            after_occupation += occupation
            current += flux
            update_solver(solver, record)
    return admitted_sectors, admitted_occupation, after_sectors, after_occupation, current, solver, blocked_error


def terminal_null(parent, before, resolution):
    after_sectors = np.zeros(parent.length + 1)
    after_occupation = np.zeros(parent.sites)
    current = np.zeros(len(parent.edges))
    solver = empty_solver(resolution)
    for q, old in enumerate(before):
        force = parent.length == 10 and q in FORCED_LOW_MEMORY_L10_Q
        rows = batch_rows(old.shape[1], resolution, force)
        for lower in range(0, old.shape[0], rows):
            upper = min(old.shape[0], lower + rows)
            evolved, flux, record = propagate_dispatch(
                parent.length, parent.sectors[q], old[lower:upper].copy(), resolution
            )
            norm, occupation = block_statistics(parent, q, evolved)
            after_sectors[q] += norm
            after_occupation += occupation
            current += flux
            update_solver(solver, record)
    return after_sectors, after_occupation, current, solver


def history(length: int, resolution):
    parent = v1.PrefixParent(length)
    state = parent.blank()
    rows = []
    for event in range(length):
        before = state
        allow, blocked, reverse = parent.predicates(before, event)
        q_before = parent.retained(before)
        g_before = parent.remaining(before)
        occupation_before = parent.occupations(before)
        if event < length - 1:
            admitted = parent.admit(before, event)
            q_admitted = parent.retained(admitted)
            g_admitted = parent.remaining(admitted)
            occupation_admitted = parent.occupations(admitted)
            actual_current, actual_solver = v1.route(parent, admitted, resolution)
            null_current, null_solver = v1.route(parent, before, resolution)
            sector_weights = parent.weights(admitted)
            occupation_after = parent.occupations(admitted)
            q_after = parent.retained(admitted)
            actual_norm = parent.norm(admitted)
            null_norm = parent.norm(before)
            blocked_error = 0.0
            terminal = False
            state = admitted
        else:
            (sector_weights, occupation_admitted, after_sectors, occupation_after,
             actual_current, actual_solver, blocked_error) = terminal_actual(
                parent, before, event, resolution
            )
            null_sectors, _, null_current, null_solver = terminal_null(parent, before, resolution)
            q_admitted = float(np.dot(np.arange(length + 1), sector_weights))
            q_after = float(np.dot(np.arange(length + 1), after_sectors))
            g_admitted = length - q_admitted
            actual_norm = float(np.sum(after_sectors))
            null_norm = float(np.sum(null_sectors))
            terminal = True
        write = q_admitted - q_before
        delta = actual_current - null_current
        transport_residual = occupation_after - occupation_admitted + parent.incidence @ actual_current
        rows.append({
            "event": event + 1, "cursor_vertex": event,
            "allow_probability": allow, "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": blocked_error,
            "W_n": write,
            "expected_W_from_allow": (math.sin(sealed.PHI) ** 2) * allow,
            "q_retained_before": q_before,
            "q_retained_after_admission": q_admitted,
            "q_retained_after_transport": q_after,
            "q_genesis_before": g_before,
            "q_genesis_after": g_admitted,
            "bandwidth_after": g_admitted,
            "lineage_sealed_after": length - g_admitted,
            "sector_weights": sector_weights.tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta[parent.connector_indices]))),
            "connector_delta_signed": float(np.sum(delta[parent.connector_indices])),
            "admission_total_content_residual": (q_admitted - q_before) + (g_admitted - g_before),
            "admission_bandwidth_residual": (g_admitted - g_before) + write,
            "target_owner_residual": (occupation_admitted[event] - occupation_before[event]) - write,
            "transport_node_residual_l1": float(np.sum(np.abs(transport_residual))),
            "transport_node_residual_linf": float(np.max(np.abs(transport_residual))),
            "transport_number_drift": abs(q_after - q_admitted),
            "transport_genesis_drift": 0.0,
            "actual_norm_error": abs(actual_norm - 1.0),
            "null_norm_error": abs(null_norm - 1.0),
            "actual_solver": actual_solver,
            "null_solver": null_solver,
            "terminal_children_streamed": terminal,
        })
    return {"rows": rows, "dimension": math.comb(3 * length, length),
            "preterminal_dimension": math.comb(3 * length - 1, length - 1),
            "edges": len(parent.edges)}


def worker(length: int, output: Path):
    if output.exists():
        raise FileExistsError(f"refuse overwrite: {output}")
    if length == 12:
        raise RuntimeError("L12 hard lock: large-sector cache/memmap supplement and L10 gate required")
    if length not in v1.SUPPORTED:
        raise ValueError(f"supported sizes: {v1.SUPPORTED}")
    started = time.perf_counter()
    coarse = history(length, sealed.COARSE)
    fine = history(length, sealed.FINE)
    comparison = sealed.summarize(length, coarse, fine)
    terminal_records = [row[key] for row in fine["rows"][-1:] for key in ("actual_solver", "null_solver")]
    if length == 10 and not all(record["low_memory_batches"] > 0 for record in terminal_records):
        comparison["resolved"] = False
        comparison["classification"] = "L10_LOW_MEMORY_PATH_NOT_EXERCISED"
    result = {
        "schema": "R_PREFIX_LINEAGE_HISTORY_ENGINE_TARGET_V002",
        "L": length, "dimension": fine["dimension"],
        "preterminal_dimension": fine["preterminal_dimension"],
        "events": length, "edges": fine["edges"],
        "representation": "EXACT_PREFIX_ROWS__TERMINAL_TWO_CHILD_STREAM__MEMORY_BOUNDED_LANCZOS",
        "coarse_method": sealed.COARSE.__dict__, "fine_method": sealed.FINE.__dict__,
        "rows": fine["rows"], "comparison": comparison,
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "method_sha256": digest(Path(__file__)),
        "v1_method_sha256": digest(HERE / "compute_prefix_history.py"),
        "supplement_sha256": digest(HERE / "LOW_MEMORY_TERMINAL_SUPPLEMENT_V002.md"),
        "claim_boundary": "FINITE_PREFIX_HISTORY_CONTROL_OR_L10_BENCHMARK_ONLY__NO_L12",
    }
    if length == 10:
        result["resource_guards"] = {
            "rss_limit_bytes": v1.RSS_LIMIT, "wall_limit_seconds": v1.WALL_LIMIT,
            "rss_pass": result["peak_rss_bytes"] <= v1.RSS_LIMIT,
            "wall_pass": result["wall_seconds"] <= v1.WALL_LIMIT,
            "same_path_25_percent_projection_limit_seconds": 387.35,
            "projection_margin_pass": result["wall_seconds"] <= 387.35,
        }
        if not all(result["resource_guards"][key] for key in
                   ("rss_pass", "wall_pass", "projection_margin_pass")):
            comparison["resolved"] = False
            comparison["classification"] = "PREFIX_L10_RESOURCE_OR_PROJECTION_GATE_FAILED"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(comparison["classification"])
    print(f"L={length} wall={result['wall_seconds']:.6f}s rss={result['peak_rss_bytes']}")
    print(f"difference={comparison['coarse_fine']['maximum_disagreement']:.3e}")
    if not comparison["resolved"]:
        raise SystemExit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    worker(arguments.worker, arguments.output)
