#!/usr/bin/env python3
"""Adaptive translation-block Krylov screen for an extended response phase."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = HERE / "RAW"
OUT = HERE / "RESULT.json"
PROTOCOL = HERE / "PROTOCOL.md"
PROTOCOL_SHA256 = "9a7bc040c990cdb14c01026ab0e3ce55cc94d767e738911c44bce1753c7584c2"
SEALED = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json"
TARGET_ROWS = {10: (5,), 12: (6,)}
VALIDATION_ROWS = ((4, 2), (6, 3), (8, 4))
ANCHOR = 0.25
CHECKPOINTS = (16, 32, 64, 96, 128)
MAX_KRYLOV = 128
RESIDUAL_LIMIT = 1.0e-9
HERMITICITY_LIMIT = 1.0e-12
ORTHOGONALITY_LIMIT = 1.0e-10
ENERGY_GROUP_TOL = 1.0e-9
SECTOR_SECONDS_LIMIT = 3 * 60 * 60
RSS_LIMIT_BYTES = 6 * (1 << 30)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words_with_weight(site_count: int, charge: int) -> np.ndarray:
    count = math.comb(site_count, charge)
    if charge == 0:
        return np.asarray([0], dtype=np.int64)

    def generate():
        word = (1 << charge) - 1
        limit = 1 << site_count
        while word < limit:
            yield word
            low = word & -word
            ripple = word + low
            word = (((ripple ^ word) >> 2) // low) | ripple

    return np.fromiter(generate(), dtype=np.int64, count=count)


def translate_word(word: int, length: int, shift: int = 1) -> int:
    mask = (1 << length) - 1
    shift %= length
    if shift == 0:
        return word
    out = 0
    for rail in range(2):
        bits = (word >> (rail * length)) & mask
        rotated = ((bits << shift) & mask) | (bits >> (length - shift))
        out |= rotated << (rail * length)
    return out


def edges_for(length: int) -> tuple[tuple[int, int], ...]:
    edges = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length))
    for site in range(length):
        edges.append((site, length + (site + 1) % length))
    return tuple(edges)


@dataclass
class OrbitData:
    words: np.ndarray
    word_to_row: np.ndarray
    orbit_by_row: np.ndarray
    step_by_row: np.ndarray
    representatives: np.ndarray
    periods: np.ndarray


def construct_orbits(length: int, charge: int) -> OrbitData:
    words = words_with_weight(2 * length, charge)
    word_to_row = np.full(1 << (2 * length), -1, dtype=np.int32)
    word_to_row[words] = np.arange(len(words), dtype=np.int32)
    orbit_by_row = np.full(len(words), -1, dtype=np.int32)
    step_by_row = np.zeros(len(words), dtype=np.uint8)
    representatives: list[int] = []
    periods: list[int] = []
    for row, raw_word in enumerate(words):
        if orbit_by_row[row] >= 0:
            continue
        representative = int(raw_word)
        orbit_id = len(representatives)
        representatives.append(representative)
        word = representative
        step = 0
        while True:
            target_row = int(word_to_row[word])
            if target_row < 0:
                raise AssertionError("translation left fixed-charge sector")
            if orbit_by_row[target_row] >= 0:
                if word != representative:
                    raise AssertionError("orbit closed away from its representative")
                break
            orbit_by_row[target_row] = orbit_id
            step_by_row[target_row] = step
            step += 1
            word = translate_word(word, length)
        periods.append(step)
    if np.any(orbit_by_row < 0):
        raise AssertionError("incomplete orbit assignment")
    return OrbitData(
        words=words,
        word_to_row=word_to_row,
        orbit_by_row=orbit_by_row,
        step_by_row=step_by_row,
        representatives=np.asarray(representatives, dtype=np.int64),
        periods=np.asarray(periods, dtype=np.int16),
    )


@dataclass
class CSRBlock:
    dimension: int
    indptr: np.ndarray
    indices: np.ndarray
    data: np.ndarray
    block_col_by_orbit: np.ndarray
    row_block_col: np.ndarray
    row_coefficient: np.ndarray
    hermiticity_error: float

    def apply(self, vector: np.ndarray) -> np.ndarray:
        products = self.data * vector[self.indices]
        return np.add.reduceat(products, self.indptr[:-1])


def construct_block(length: int, orbit_data: OrbitData, momentum: int) -> CSRBlock:
    periods = orbit_data.periods
    allowed = np.flatnonzero((momentum * periods) % length == 0)
    dimension = len(allowed)
    block_col_by_orbit = np.full(len(periods), -1, dtype=np.int32)
    block_col_by_orbit[allowed] = np.arange(dimension, dtype=np.int32)
    row_block_col = block_col_by_orbit[orbit_data.orbit_by_row]
    wave = 2.0 * math.pi * momentum / length
    row_coefficient = np.zeros(len(orbit_data.words), dtype=np.complex128)
    active_rows = row_block_col >= 0
    active_orbits = orbit_data.orbit_by_row[active_rows]
    row_coefficient[active_rows] = (
        np.exp(-1j * wave * orbit_data.step_by_row[active_rows])
        / np.sqrt(periods[active_orbits].astype(np.float64))
    )

    edges = edges_for(length)
    capacity = dimension * len(edges)
    coo_rows = np.empty(capacity, dtype=np.int32)
    coo_cols = np.empty(capacity, dtype=np.int32)
    coo_data = np.empty(capacity, dtype=np.complex128)
    used = 0
    for source_col, orbit_id in enumerate(allowed):
        representative = int(orbit_data.representatives[orbit_id])
        source_period = int(periods[orbit_id])
        for u, v in edges:
            if ((representative >> u) & 1) == ((representative >> v) & 1):
                continue
            destination = representative ^ (1 << u) ^ (1 << v)
            destination_row = int(orbit_data.word_to_row[destination])
            destination_orbit = int(orbit_data.orbit_by_row[destination_row])
            destination_col = int(block_col_by_orbit[destination_orbit])
            if destination_col < 0:
                continue
            destination_period = int(periods[destination_orbit])
            shift = int(orbit_data.step_by_row[destination_row])
            coo_rows[used] = destination_col
            coo_cols[used] = source_col
            coo_data[used] = (
                -math.sqrt(source_period / destination_period)
                * np.exp(1j * wave * shift)
            )
            used += 1
    coo_rows = coo_rows[:used]
    coo_cols = coo_cols[:used]
    coo_data = coo_data[:used]
    keys = coo_rows.astype(np.int64) * dimension + coo_cols
    order = np.argsort(keys, kind="mergesort")
    keys = keys[order]
    values = coo_data[order]
    starts = np.concatenate(([0], np.flatnonzero(np.diff(keys)) + 1))
    unique_keys = keys[starts]
    unique_values = np.add.reduceat(values, starts)
    keep = np.abs(unique_values) > 1.0e-14
    unique_keys = unique_keys[keep]
    unique_values = unique_values[keep]
    rows = (unique_keys // dimension).astype(np.int32)
    columns = (unique_keys % dimension).astype(np.int32)
    counts = np.bincount(rows, minlength=dimension)
    if np.any(counts == 0):
        raise AssertionError("translation block has an empty row")
    indptr = np.concatenate(([0], np.cumsum(counts))).astype(np.int64)

    reverse_keys = columns.astype(np.int64) * dimension + rows
    reverse_positions = np.searchsorted(unique_keys, reverse_keys)
    if np.any(reverse_positions >= len(unique_keys)) or np.any(
        unique_keys[reverse_positions] != reverse_keys
    ):
        raise AssertionError("translation block sparsity is not symmetric")
    hermiticity_error = float(
        np.max(np.abs(unique_values - np.conjugate(unique_values[reverse_positions])))
    )
    if momentum == 0:
        unique_values = unique_values.real.astype(np.float64)
        row_coefficient = row_coefficient.real.astype(np.float64)
    return CSRBlock(
        dimension=dimension,
        indptr=indptr,
        indices=columns,
        data=unique_values,
        block_col_by_orbit=block_col_by_orbit,
        row_block_col=row_block_col,
        row_coefficient=row_coefficient,
        hermiticity_error=hermiticity_error,
    )


def matrix_adjoint_vector(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    # Accelerate can surface a stale floating-point flag as a false matmul
    # RuntimeWarning even when all operands and outputs are finite.  Suppress
    # only the BLAS call and fail explicitly on any non-finite result.
    with np.errstate(all="ignore"):
        if not np.iscomplexobj(matrix) and not np.iscomplexobj(vector):
            out = matrix.T @ vector
        else:
            mr, mi = matrix.real, matrix.imag
            vr, vi = vector.real, vector.imag
            out = mr.T @ vr + mi.T @ vi + 1j * (mr.T @ vi - mi.T @ vr)
    if not np.all(np.isfinite(out)):
        raise FloatingPointError("non-finite adjoint matrix-vector product")
    return out


def matrix_vector(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    with np.errstate(all="ignore"):
        if not np.iscomplexobj(matrix) and not np.iscomplexobj(vector):
            out = matrix @ vector
        else:
            mr, mi = matrix.real, matrix.imag
            vr, vi = vector.real, vector.imag
            out = mr @ vr - mi @ vi + 1j * (mr @ vi + mi @ vr)
    if not np.all(np.isfinite(out)):
        raise FloatingPointError("non-finite matrix-vector product")
    return out


def orthogonality_error(matrix: np.ndarray) -> float:
    gram = matrix_adjoint_vector(matrix, matrix)
    gram -= np.eye(matrix.shape[1])
    return float(np.max(np.abs(gram)))


@dataclass
class LanczosRun:
    alphas: np.ndarray
    betas: np.ndarray
    vectors: np.ndarray
    start_norm: float
    checkpoints: list[dict[str, object]]
    matvecs: int
    orthogonality_error: float


def tridiagonal(alphas: np.ndarray, betas: np.ndarray, size: int) -> np.ndarray:
    out = np.diag(alphas[:size])
    if size > 1:
        off = betas[: size - 1]
        out += np.diag(off, 1) + np.diag(off, -1)
    return out


def lanczos(block: CSRBlock, start: np.ndarray, max_steps: int = MAX_KRYLOV) -> LanczosRun:
    start_norm = float(np.linalg.norm(start))
    if not math.isfinite(start_norm) or start_norm == 0.0:
        raise AssertionError("invalid Krylov start")
    dtype = np.result_type(block.data.dtype, start.dtype)
    vectors = np.empty((block.dimension, max_steps), dtype=dtype, order="F")
    alphas = np.zeros(max_steps, dtype=np.float64)
    betas = np.zeros(max_steps, dtype=np.float64)
    vectors[:, 0] = start / start_norm
    completed = 0
    for step in range(max_steps):
        current = vectors[:, step]
        work = block.apply(current)
        alpha = float(np.vdot(current, work).real)
        work -= alpha * current
        if step:
            work -= betas[step - 1] * vectors[:, step - 1]
        # Full reorthogonalization is deliberate: it prevents ghost low poles.
        active = vectors[:, : step + 1]
        correction = matrix_adjoint_vector(active, work)
        work -= matrix_vector(active, correction)
        alpha_correction = float(np.vdot(current, work).real)
        work -= alpha_correction * current
        alpha += alpha_correction
        beta = float(np.linalg.norm(work))
        alphas[step] = alpha
        betas[step] = beta
        completed = step + 1
        if step + 1 == max_steps or beta <= 1.0e-14:
            break
        vectors[:, step + 1] = work / beta
    vectors = vectors[:, :completed]
    alphas = alphas[:completed]
    betas = betas[:completed]
    checkpoints = []
    checkpoint_sizes = sorted(
        set(size for size in CHECKPOINTS if size <= completed) | {completed}
    )
    for size in checkpoint_sizes:
        values, coefficients = np.linalg.eigh(tridiagonal(alphas, betas, size))
        checkpoints.append(
            {
                "krylov_dimension": size,
                "ritz_values": values,
                "first_components": coefficients[0, :],
                "last_components": coefficients[-1, :],
                "ritz_residual_estimates": np.abs(betas[size - 1] * coefficients[-1, :]),
            }
        )
    return LanczosRun(
        alphas=alphas,
        betas=betas,
        vectors=vectors,
        start_norm=start_norm,
        checkpoints=checkpoints,
        matvecs=completed,
        orthogonality_error=orthogonality_error(vectors),
    )


def ground_from_run(block: CSRBlock, run: LanczosRun) -> tuple[float, np.ndarray, float, list[dict[str, float]]]:
    sequence = []
    final_coefficients = None
    final_energy = math.nan
    for checkpoint in run.checkpoints:
        size = int(checkpoint["krylov_dimension"])
        matrix = tridiagonal(run.alphas, run.betas, size)
        values, vectors = np.linalg.eigh(matrix)
        estimate = float(abs(run.betas[size - 1] * vectors[-1, 0]))
        sequence.append({
            "krylov_dimension": size,
            "energy": float(values[0]),
            "residual_estimate": estimate,
            "lowest_five_ritz_values": values[:5].tolist(),
        })
        final_coefficients = vectors[:, 0]
        final_energy = float(values[0])
    if final_coefficients is None:
        raise AssertionError("no ground checkpoint")
    size = len(final_coefficients)
    ground = matrix_vector(run.vectors[:, :size], final_coefficients)
    residual = float(np.linalg.norm(block.apply(ground) - final_energy * ground))
    return final_energy, ground, residual, sequence


def response_metrics_at_checkpoint(
    checkpoint: dict[str, object], ground_energy: float, start_norm: float
) -> dict[str, float | int | bool]:
    values = np.asarray(checkpoint["ritz_values"])
    first = np.asarray(checkpoint["first_components"])
    residuals = np.asarray(checkpoint["ritz_residual_estimates"])
    omegas = values - ground_energy
    weights = start_norm**2 * np.abs(first) ** 2
    positive = omegas > 1.0e-10
    total_weight = float(np.sum(weights[positive]))
    provisional_floor = 1.0e-12 * total_weight
    active_candidates = np.flatnonzero(positive & (weights > provisional_floor))
    if not len(active_candidates):
        return {"resolved": False}
    active_index = int(active_candidates[0])
    residual = float(residuals[active_index])
    floor = max(1.0e-12 * total_weight, 100.0 * residual**2 * start_norm**2)
    threshold_indices = []
    for factor in (0.1, 1.0, 10.0):
        candidates = np.flatnonzero(positive & (weights > factor * floor))
        threshold_indices.append(None if not len(candidates) else int(candidates[0]))
    stable = threshold_indices[0] == threshold_indices[1] == threshold_indices[2]
    if threshold_indices[1] is None:
        return {"resolved": False}
    active_index = int(threshold_indices[1])
    active_omega = float(omegas[active_index])
    group = np.flatnonzero(np.abs(omegas - active_omega) <= ENERGY_GROUP_TOL)
    low_weight = float(np.sum(weights[group]))
    chi = math.sqrt(float(np.sum(weights[positive] / omegas[positive] ** 2)) / total_weight)
    return {
        "resolved": True,
        "krylov_dimension": int(checkpoint["krylov_dimension"]),
        "lowest_five_ritz_values": values[:5].tolist(),
        "Delta_act": active_omega,
        "chi_tau": chi,
        "R_low": low_weight / total_weight,
        "active_ritz_index": active_index,
        "active_residual_estimate": float(residuals[active_index]),
        "total_weight": total_weight,
        "weight_floor": floor,
        "threshold_stable": stable,
        "threshold_indices": threshold_indices,
    }


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def worker(length: int, charge: int, output: Path) -> None:
    started = time.perf_counter()
    if sha256(PROTOCOL) != PROTOCOL_SHA256:
        raise AssertionError("protocol hash mismatch")
    if charge not in TARGET_ROWS.get(length, ()) and (length, charge) not in VALIDATION_ROWS:
        raise ValueError("row is outside the frozen target")
    memory_guards = []
    for guard_name in ("RLIMIT_AS", "RLIMIT_RSS"):
        guard = getattr(resource, guard_name, None)
        if guard is None:
            continue
        try:
            old_soft, old_hard = resource.getrlimit(guard)
            new_hard = RSS_LIMIT_BYTES if old_hard < 0 else min(old_hard, RSS_LIMIT_BYTES)
            resource.setrlimit(guard, (min(RSS_LIMIT_BYTES, new_hard), new_hard))
            memory_guards.append(guard_name)
        except (OSError, ValueError):
            pass
    orbits = construct_orbits(length, charge)
    ground_block = construct_block(length, orbits, 0)
    ground_start = np.ones(ground_block.dimension, dtype=np.float64)
    ground_run = lanczos(ground_block, ground_start)
    ground_energy, ground_vector, ground_residual, ground_sequence = ground_from_run(
        ground_block, ground_run
    )

    full_ground = np.zeros(len(orbits.words), dtype=np.float64)
    active_ground_rows = ground_block.row_block_col >= 0
    full_ground[active_ground_rows] = (
        ground_block.row_coefficient[active_ground_rows]
        * ground_vector[ground_block.row_block_col[active_ground_rows]]
    )
    k = 2.0 * math.pi / length
    phases = np.exp(1j * k * np.arange(length))
    nk_diagonal = np.zeros(len(orbits.words), dtype=np.complex128)
    for site in range(length):
        nk_diagonal += phases[site] * (
            ((orbits.words >> site) & 1)
            + ((orbits.words >> (length + site)) & 1)
        )
    full_response = nk_diagonal * full_ground
    response_block = construct_block(length, orbits, length - 1)
    response_start = np.zeros(response_block.dimension, dtype=np.complex128)
    active_response_rows = response_block.row_block_col >= 0
    np.add.at(
        response_start,
        response_block.row_block_col[active_response_rows],
        np.conjugate(response_block.row_coefficient[active_response_rows])
        * full_response[active_response_rows],
    )
    full_response_norm = float(np.vdot(full_response, full_response).real)
    projected_response_norm = float(np.vdot(response_start, response_start).real)
    projection_error = abs(full_response_norm - projected_response_norm)
    response_run = lanczos(response_block, response_start)
    response_sequence = [
        response_metrics_at_checkpoint(checkpoint, ground_energy, response_run.start_norm)
        for checkpoint in response_run.checkpoints
    ]
    response_sequence = [row for row in response_sequence if row.get("resolved")]
    response_exact_termination = bool(
        len(response_run.betas) and response_run.betas[-1] <= 1.0e-14
    )
    if len(response_sequence) == 1 and response_exact_termination:
        final_metrics = dict(response_sequence[-1])
        convergence = {
            "Delta_act_relative": 0.0,
            "chi_tau_relative": 0.0,
            "R_low_relative": 0.0,
            "resolved": True,
            "exact_krylov_termination": True,
        }
        size = int(final_metrics["krylov_dimension"])
        matrix = tridiagonal(response_run.alphas, response_run.betas, size)
        _, coefficient_matrix = np.linalg.eigh(matrix)
        active_index = int(final_metrics["active_ritz_index"])
        active_vector = matrix_vector(
            response_run.vectors[:, :size], coefficient_matrix[:, active_index]
        )
        active_energy = ground_energy + float(final_metrics["Delta_act"])
        active_actual_residual = float(
            np.linalg.norm(response_block.apply(active_vector) - active_energy * active_vector)
        )
    elif len(response_sequence) < 2:
        final_metrics: dict[str, object] = {"resolved": False}
        convergence = {"resolved": False}
        active_actual_residual = math.inf
    else:
        final_metrics = dict(response_sequence[-1])
        previous = response_sequence[-2]
        convergence = {
            "Delta_act_relative": relative_difference(float(final_metrics["Delta_act"]), float(previous["Delta_act"])),
            "chi_tau_relative": relative_difference(float(final_metrics["chi_tau"]), float(previous["chi_tau"])),
            "R_low_relative": relative_difference(float(final_metrics["R_low"]), float(previous["R_low"])),
        }
        convergence["resolved"] = (
            convergence["Delta_act_relative"] <= 2.0e-7
            and convergence["chi_tau_relative"] <= 2.0e-7
            and convergence["R_low_relative"] <= 2.0e-6
        )
        size = int(final_metrics["krylov_dimension"])
        matrix = tridiagonal(response_run.alphas, response_run.betas, size)
        _, coefficient_matrix = np.linalg.eigh(matrix)
        active_index = int(final_metrics["active_ritz_index"])
        active_vector = matrix_vector(
            response_run.vectors[:, :size], coefficient_matrix[:, active_index]
        )
        active_energy = ground_energy + float(final_metrics["Delta_act"])
        active_actual_residual = float(
            np.linalg.norm(response_block.apply(active_vector) - active_energy * active_vector)
        )

    ground_exact_termination = bool(
        len(ground_run.betas) and ground_run.betas[-1] <= 1.0e-14
    )
    ground_converged = (
        (
            len(ground_sequence) >= 2
            and relative_difference(ground_sequence[-1]["energy"], ground_sequence[-2]["energy"]) <= 2.0e-10
        )
        or (len(ground_sequence) == 1 and ground_exact_termination)
    )
    unresolved_reasons = []
    if ground_block.hermiticity_error > HERMITICITY_LIMIT or response_block.hermiticity_error > HERMITICITY_LIMIT:
        unresolved_reasons.append("BLOCK_HERMITICITY")
    if ground_run.orthogonality_error > ORTHOGONALITY_LIMIT or response_run.orthogonality_error > ORTHOGONALITY_LIMIT:
        unresolved_reasons.append("KRYLOV_ORTHOGONALITY")
    if ground_residual > RESIDUAL_LIMIT or not ground_converged:
        unresolved_reasons.append("GROUND_NOT_CONVERGED")
    if active_actual_residual > RESIDUAL_LIMIT:
        unresolved_reasons.append("ACTIVE_POLE_RESIDUAL")
    if not convergence.get("resolved", False):
        unresolved_reasons.append("RESPONSE_METRICS_NOT_STABLE")
    if not final_metrics.get("threshold_stable", False):
        unresolved_reasons.append("ACTIVE_THRESHOLD_SWITCH")
    if float(final_metrics.get("R_low", 0.0)) < 1.0e-6:
        unresolved_reasons.append("LOW_POLE_RESIDUE")
    if projection_error > 1.0e-9:
        unresolved_reasons.append("RESPONSE_PROJECTION_CLOSURE")

    elapsed = time.perf_counter() - started
    if elapsed > SECTOR_SECONDS_LIMIT:
        unresolved_reasons.append("SECTOR_WALL_GUARD")
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if rss > RSS_LIMIT_BYTES:
        unresolved_reasons.append("SECTOR_RSS_GUARD")
    row = {
        "L": length,
        "q": charge,
        "rho": charge / (2.0 * length),
        "sector_dimension": len(orbits.words),
        "translation_orbits": len(orbits.representatives),
        "ground_block_dimension": ground_block.dimension,
        "ground_block_nnz": len(ground_block.data),
        "response_block_dimension": response_block.dimension,
        "response_block_nnz": len(response_block.data),
        "ground_block_hermiticity_error": ground_block.hermiticity_error,
        "response_block_hermiticity_error": response_block.hermiticity_error,
        "ground_energy": ground_energy,
        "ground_residual": ground_residual,
        "ground_krylov_orthogonality": ground_run.orthogonality_error,
        "ground_sequence": ground_sequence,
        "response_full_norm_squared": full_response_norm,
        "response_projected_norm_squared": projected_response_norm,
        "response_projection_error": projection_error,
        "response_krylov_orthogonality": response_run.orthogonality_error,
        "response_sequence": response_sequence,
        "response_convergence": convergence,
        "active_actual_residual": active_actual_residual,
        "Delta_act": final_metrics.get("Delta_act"),
        "chi_tau": final_metrics.get("chi_tau"),
        "R_low": final_metrics.get("R_low"),
        "threshold_stable": final_metrics.get("threshold_stable", False),
        "ground_matvecs": ground_run.matvecs,
        "response_matvecs": response_run.matvecs,
        "total_matvecs": ground_run.matvecs + response_run.matvecs,
        "wall_seconds": elapsed,
        "max_rss_bytes": rss,
        "memory_guards": memory_guards,
        "unresolved_reasons": unresolved_reasons,
        "status": "RESOLVED" if not unresolved_reasons else "UNRESOLVED",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")


def centerline_row(rows: dict[int, dict[str, object]], length: int) -> dict[str, object]:
    charge = length // 2
    source = rows[charge]
    return {
        "L": length,
        "rho_anchor": ANCHOR,
        "source_q": [charge],
        "weights": [1.0],
        **{key: float(source[key]) for key in ("Delta_act", "chi_tau", "R_low")},
    }


def fit_power(lengths: np.ndarray, values: np.ndarray) -> dict[str, float]:
    slope, intercept = np.polyfit(np.log(lengths), np.log(values), 1)
    return {"amplitude": float(math.exp(intercept)), "exponent": float(-slope)}


def fit_gap_family(lengths: np.ndarray, values: np.ndarray, positive_gap: bool) -> dict[str, float]:
    best = None
    for exponent in np.linspace(0.25, 4.0, 15001):
        feature = lengths ** (-exponent)
        if positive_gap:
            design = np.column_stack((np.ones(len(lengths)), feature))
            parameters, *_ = np.linalg.lstsq(design, values, rcond=None)
            gap, amplitude = (float(value) for value in parameters)
            if gap <= 0.0 or amplitude <= 0.0:
                continue
            prediction = gap + amplitude * feature
        else:
            amplitude = float(np.dot(feature, values) / np.dot(feature, feature))
            gap = 0.0
            if amplitude <= 0.0:
                continue
            prediction = amplitude * feature
        error = float(np.sum((prediction - values) ** 2))
        if best is None or error < best[0]:
            best = (error, gap, amplitude, float(exponent))
    if best is None:
        return {"fit_status": "NO_ADMISSIBLE_PARAMETERS"}
    error, gap, amplitude, exponent = best
    return {
        "fit_status": "RESOLVED",
        "training_sse": error,
        "Delta_inf": gap,
        "amplitude": amplitude,
        "exponent": exponent,
    }


def fit_fixed_z1(lengths: np.ndarray, values: np.ndarray) -> dict[str, float | str]:
    design = np.column_stack((1.0 / lengths, 1.0 / lengths**2))
    parameters, *_ = np.linalg.lstsq(design, values, rcond=None)
    amplitude, correction = (float(value) for value in parameters)
    prediction = design @ parameters
    if amplitude <= 0.0 or np.any(prediction <= 0.0):
        return {"fit_status": "NO_ADMISSIBLE_PARAMETERS"}
    return {
        "fit_status": "RESOLVED",
        "amplitude": amplitude,
        "correction": correction,
        "training_sse": float(np.sum((prediction - values) ** 2)),
    }


def held_out_score(lengths: np.ndarray, values: np.ndarray, positive_gap: bool) -> tuple[float, list[dict[str, float]]]:
    rows = []
    total = 0.0
    for held in range(len(lengths)):
        mask = np.arange(len(lengths)) != held
        fit = fit_gap_family(lengths[mask], values[mask], positive_gap)
        if fit.get("fit_status") != "RESOLVED":
            return math.inf, rows
        prediction = float(fit["Delta_inf"]) + float(fit["amplitude"]) * lengths[held] ** (-float(fit["exponent"]))
        relative_error = (prediction - values[held]) / values[held]
        total += relative_error**2
        rows.append({
            "held_L": int(lengths[held]),
            "observed": float(values[held]),
            "predicted": prediction,
            "relative_error": float(relative_error),
        })
    return float(total), rows


def held_out_fixed_z1(lengths: np.ndarray, values: np.ndarray) -> tuple[float, list[dict[str, float]]]:
    rows = []
    total = 0.0
    for held in range(len(lengths)):
        mask = np.arange(len(lengths)) != held
        fit = fit_fixed_z1(lengths[mask], values[mask])
        if fit.get("fit_status") != "RESOLVED":
            return math.inf, rows
        prediction = float(fit["amplitude"]) / lengths[held] + float(fit["correction"]) / lengths[held] ** 2
        if prediction <= 0.0:
            return math.inf, rows
        relative_error = (prediction - values[held]) / values[held]
        total += relative_error**2
        rows.append({
            "held_L": int(lengths[held]),
            "observed": float(values[held]),
            "predicted": prediction,
            "relative_error": float(relative_error),
        })
    return float(total), rows


def relative_range(values: np.ndarray) -> float:
    return float((np.max(values) - np.min(values)) / np.mean(values))


def classify_anchor(rows: list[dict[str, object]]) -> dict[str, object]:
    lengths = np.asarray([row["L"] for row in rows], dtype=float)
    gaps = np.asarray([row["Delta_act"] for row in rows], dtype=float)
    chis = np.asarray([row["chi_tau"] for row in rows], dtype=float)
    residues = np.asarray([row["R_low"] for row in rows], dtype=float)
    gapless_score, gapless_predictions = held_out_score(lengths, gaps, False)
    gapped_score, gapped_predictions = held_out_score(lengths, gaps, True)
    fixed_z1_score, fixed_z1_predictions = held_out_fixed_z1(lengths, gaps)
    fixed_z1_fit = fit_fixed_z1(lengths, gaps)
    gap_fit = fit_power(lengths, gaps)
    chi_fit_raw = fit_power(lengths, 1.0 / chis)
    z = float(gap_fit["exponent"])
    y = float(chi_fit_raw["exponent"])
    tail = lengths >= 8
    scaled_gap = lengths * gaps
    scaled_chi = chis / lengths
    checks = {
        "gap_strictly_decreases": bool(np.all(np.diff(gaps) < 0.0)),
        "chi_strictly_increases": bool(np.all(np.diff(chis) > 0.0)),
        "fixed_z1_beats_positive_gap": fixed_z1_score < gapped_score,
        "fixed_z1_near_free_gapless": fixed_z1_score <= 1.25 * gapless_score,
        "z_in_window": 0.90 <= z <= 1.10,
        "y_in_window": 0.90 <= y <= 1.10,
        "exponents_agree": abs(z - y) <= 0.10,
        "tail_scaled_gap_stable": relative_range(scaled_gap[tail]) <= 0.05,
        "tail_scaled_chi_stable": relative_range(scaled_chi[tail]) <= 0.05,
        "residue_nonzero": bool(np.all(residues >= 1.0e-6)),
        "tail_residue_stable": relative_range(residues[tail]) <= 0.35,
    }
    return {
        "rows": rows,
        "L_times_Delta": scaled_gap.tolist(),
        "chi_over_L": scaled_chi.tolist(),
        "gap_power_fit": gap_fit,
        "fixed_z1_fit": fixed_z1_fit,
        "chi_power_exponent_y": y,
        "fixed_z1_heldout_sse_relative": fixed_z1_score,
        "gapless_heldout_sse_relative": gapless_score,
        "positive_gap_heldout_sse_relative": gapped_score,
        "fixed_z1_heldout_rows": fixed_z1_predictions,
        "gapless_heldout_rows": gapless_predictions,
        "positive_gap_heldout_rows": gapped_predictions,
        "tail_scaled_gap_relative_range": relative_range(scaled_gap[tail]),
        "tail_scaled_chi_relative_range": relative_range(scaled_chi[tail]),
        "tail_residue_relative_range": relative_range(residues[tail]),
        "checks": checks,
        "passes": all(checks.values()),
    }


def main(run_workers: bool = True) -> None:
    if sha256(PROTOCOL) != PROTOCOL_SHA256:
        raise AssertionError("protocol hash mismatch")
    sealed = json.loads(SEALED.read_text())
    prior_rows: dict[tuple[int, int], dict[str, object]] = {}
    for length_rows in sealed["sector_rows"].values():
        for row in length_rows:
            if int(row["q"]) > 0:
                prior_rows[(int(row["L"]), int(row["q"]))] = row
    started = time.perf_counter()
    worker_rows = []
    for length, charges in TARGET_ROWS.items():
        for charge in charges:
            output = RAW / f"SECTOR_L{length}_Q{charge}.json"
            if run_workers:
                command = [
                    sys.executable,
                    "-B",
                    str(Path(__file__).resolve()),
                    "--worker",
                    "--L",
                    str(length),
                    "--q",
                    str(charge),
                    "--output",
                    str(output),
                ]
                subprocess.run(command, check=True, timeout=SECTOR_SECONDS_LIMIT + 60)
            if not output.is_file():
                raise FileNotFoundError(f"missing frozen worker output: {output}")
            row = json.loads(output.read_text())
            worker_rows.append(row)
            if row["status"] != "RESOLVED":
                break
        if worker_rows and worker_rows[-1]["status"] != "RESOLVED":
            break

    all_resolved = len(worker_rows) == sum(len(values) for values in TARGET_ROWS.values()) and all(
        row["status"] == "RESOLVED" for row in worker_rows
    )
    centerline: dict[str, object] = {}
    classification = "UNRESOLVED"
    if all_resolved:
        rows_by_size: dict[int, dict[int, dict[str, object]]] = {}
        for (length, charge), row in prior_rows.items():
            rows_by_size.setdefault(length, {})[charge] = row
        for row in worker_rows:
            rows_by_size.setdefault(int(row["L"]), {})[int(row["q"])] = row
        aligned = [centerline_row(rows_by_size[length], length) for length in (4, 6, 8, 10, 12)]
        centerline = classify_anchor(aligned)
        classification = (
            "CENTERLINE_Z1_COMPATIBLE_L4_L12"
            if centerline["passes"]
            else "CENTERLINE_Z1_REJECTED_L4_L12"
        )

    result = {
        "packet": HERE.name,
        "protocol_sha256": sha256(PROTOCOL),
        "sealed_input_sha256": sha256(SEALED),
        "classification": classification,
        "all_required_rows_resolved": all_resolved,
        "target_rows": worker_rows,
        "centerline": centerline,
        "telemetry": {
            "wall_seconds": time.perf_counter() - started,
            "max_worker_rss_bytes": max((int(row["max_rss_bytes"]) for row in worker_rows), default=0),
            "worker_wall_seconds_sum": sum(float(row["wall_seconds"]) for row in worker_rows),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "claim_boundary": {
            "empirical": "FINITE_PRISM_RESPONSE_ACTIVE_SCALING_ONLY",
            "not_claimed": [
                "THERMODYNAMIC_PHASE",
                "CONTINUUM",
                "METRIC",
                "UNIVERSAL_COUPLING",
                "EMERGENCE",
                "GRAVITY",
            ],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(classification)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--L", type=int)
    parser.add_argument("--q", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--aggregate-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.worker:
        if arguments.L is None or arguments.q is None or arguments.output is None:
            parser.error("worker requires --L, --q, and --output")
        worker(arguments.L, arguments.q, arguments.output)
    else:
        main(run_workers=not arguments.aggregate_only)
