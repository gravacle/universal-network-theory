#!/usr/bin/env python3
"""Independent sparse adaptive-Krylov centerline reconstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import platform
import resource
import sys
import time
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np


HERE = Path(__file__).resolve().parent
METHOD = HERE / "METHODOLOGY.md"
OUT = HERE / "INDEPENDENT_VALIDATION.json"
RAW = HERE / "RAW_VALIDATION"
EXPECTED_METHOD_SHA256 = "dbe28ec72e64cea10b9e974213277c284ffd20596877a06fdca4ee66ba4075a4"
VALIDATION_ROWS = ((4, 2), (6, 3), (8, 4))
FUTURE_ROWS = ((10, 5), (12, 6))
AUTHORIZATION = "ALLOW_REQUIRE_SEMANTIC_GATE_PASSED"
CHECKPOINTS = (8, 16, 32, 64, 96, 128)
MAX_KRYLOV = 128
ENERGY_GROUP_TOL = 1.0e-9
RESIDUAL_LIMIT = 1.0e-9
HERMITICITY_LIMIT = 1.0e-12
ORTHOGONALITY_LIMIT = 1.0e-10
PROJECTION_LIMIT = 1.0e-9
WALL_LIMIT_SECONDS = 3 * 60 * 60
RSS_LIMIT_BYTES = 16 * (1 << 30)
MATVEC_LIMIT = 2000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def peak_rss_bytes() -> int:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if sys.platform == "darwin" else raw * 1024


def prism_edges(length: int) -> tuple[tuple[int, int], ...]:
    edges: list[tuple[int, int]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length))
    for site in range(length):
        edges.append((site, length + (site + 1) % length))
    return tuple(edges)


def translate(word: int, length: int) -> int:
    rail_mask = (1 << length) - 1
    out = 0
    for rail in range(2):
        bits = (word >> (rail * length)) & rail_mask
        shifted = ((bits << 1) & rail_mask) | (bits >> (length - 1))
        out |= shifted << (rail * length)
    return out


def fixed_charge_words(site_count: int, charge: int) -> np.ndarray:
    words: list[int] = []
    for occupied in itertools.combinations(range(site_count), charge):
        word = 0
        for site in occupied:
            word |= 1 << site
        words.append(word)
    return np.asarray(words, dtype=np.int64)


@dataclass(frozen=True)
class OrbitBank:
    length: int
    charge: int
    words: np.ndarray
    word_index: dict[int, int]
    orbits: tuple[tuple[int, ...], ...]
    location: dict[int, tuple[int, int]]


def build_orbit_bank(length: int, charge: int) -> OrbitBank:
    words = fixed_charge_words(2 * length, charge)
    word_index = {int(word): row for row, word in enumerate(words)}
    unseen = set(word_index)
    orbits: list[tuple[int, ...]] = []
    location: dict[int, tuple[int, int]] = {}
    while unseen:
        representative = min(unseen)
        orbit: list[int] = []
        word = representative
        while word not in orbit:
            orbit.append(word)
            word = translate(word, length)
        if word != representative or length % len(orbit):
            raise AssertionError("translation orbit failed to close")
        orbit_id = len(orbits)
        for step, item in enumerate(orbit):
            if item not in unseen:
                raise AssertionError("translation orbits overlap")
            unseen.remove(item)
            location[item] = (orbit_id, step)
        orbits.append(tuple(orbit))
    return OrbitBank(length, charge, words, word_index, tuple(orbits), location)


@dataclass
class SparseBlock:
    dimension: int
    indptr: np.ndarray
    indices: np.ndarray
    data: np.ndarray
    allowed_orbits: tuple[int, ...]
    column_by_orbit: dict[int, int]
    momentum: int
    hermiticity_error: float

    def apply(self, vector: np.ndarray) -> np.ndarray:
        if len(vector) != self.dimension:
            raise ValueError("sparse-block vector has wrong dimension")
        products = self.data * vector[self.indices]
        return np.add.reduceat(products, self.indptr[:-1])


def orbit_coefficient(length: int, momentum: int, period: int, step: int) -> complex:
    wave = 2.0 * math.pi * momentum / length
    return np.exp(-1j * wave * step) / math.sqrt(period)


def build_sparse_block(bank: OrbitBank, momentum: int) -> SparseBlock:
    length = bank.length
    edges = prism_edges(length)
    allowed = tuple(
        orbit_id
        for orbit_id, orbit in enumerate(bank.orbits)
        if (momentum * len(orbit)) % length == 0
    )
    column_by_orbit = {orbit_id: column for column, orbit_id in enumerate(allowed)}
    dimension = len(allowed)
    row_maps: list[dict[int, complex]] = [dict() for _ in range(dimension)]

    # Deliberately apply every owner to every word in an orbit.  This is
    # slower but representation-distinct from a representative-only formula.
    for source_column, orbit_id in enumerate(allowed):
        source_orbit = bank.orbits[orbit_id]
        source_period = len(source_orbit)
        for source_step, word in enumerate(source_orbit):
            source_coefficient = orbit_coefficient(
                length, momentum, source_period, source_step
            )
            for left, right in edges:
                if ((word >> left) & 1) == ((word >> right) & 1):
                    continue
                destination = word ^ (1 << left) ^ (1 << right)
                destination_orbit, destination_step = bank.location[destination]
                destination_column = column_by_orbit.get(destination_orbit)
                if destination_column is None:
                    continue
                destination_period = len(bank.orbits[destination_orbit])
                destination_coefficient = orbit_coefficient(
                    length, momentum, destination_period, destination_step
                )
                value = -np.conjugate(destination_coefficient) * source_coefficient
                row = row_maps[destination_column]
                row[source_column] = row.get(source_column, 0.0j) + value

    for row in row_maps:
        for column in tuple(row):
            if abs(row[column]) <= 1.0e-13:
                del row[column]
    if any(not row for row in row_maps):
        raise AssertionError("sparse momentum block contains an empty row")

    hermiticity_error = 0.0
    for row_index, row in enumerate(row_maps):
        for column_index, value in row.items():
            reverse = row_maps[column_index].get(row_index, 0.0j)
            hermiticity_error = max(
                hermiticity_error, float(abs(value - np.conjugate(reverse)))
            )

    indptr = [0]
    indices: list[int] = []
    data: list[complex] = []
    for row in row_maps:
        for column, value in sorted(row.items()):
            indices.append(column)
            data.append(value)
        indptr.append(len(indices))
    values = np.asarray(data, dtype=np.complex128)
    if momentum == 0 and np.max(np.abs(values.imag), initial=0.0) <= 1.0e-13:
        values = values.real.astype(np.float64)
    return SparseBlock(
        dimension=dimension,
        indptr=np.asarray(indptr, dtype=np.int64),
        indices=np.asarray(indices, dtype=np.int32),
        data=values,
        allowed_orbits=allowed,
        column_by_orbit=column_by_orbit,
        momentum=momentum,
        hermiticity_error=hermiticity_error,
    )


def expand_to_words(bank: OrbitBank, block: SparseBlock, vector: np.ndarray) -> np.ndarray:
    out = np.zeros(len(bank.words), dtype=np.result_type(vector.dtype, np.complex128))
    for orbit_id, column in block.column_by_orbit.items():
        orbit = bank.orbits[orbit_id]
        for step, word in enumerate(orbit):
            out[bank.word_index[word]] = (
                orbit_coefficient(bank.length, block.momentum, len(orbit), step)
                * vector[column]
            )
    return out


def project_from_words(bank: OrbitBank, block: SparseBlock, vector: np.ndarray) -> np.ndarray:
    out = np.zeros(block.dimension, dtype=np.complex128)
    for orbit_id, column in block.column_by_orbit.items():
        orbit = bank.orbits[orbit_id]
        for step, word in enumerate(orbit):
            coefficient = orbit_coefficient(
                bank.length, block.momentum, len(orbit), step
            )
            out[column] += np.conjugate(coefficient) * vector[bank.word_index[word]]
    return out


def tridiagonal(alphas: list[float], betas: list[float], size: int) -> np.ndarray:
    matrix = np.diag(np.asarray(alphas[:size], dtype=float))
    if size > 1:
        off = np.asarray(betas[: size - 1], dtype=float)
        matrix += np.diag(off, 1) + np.diag(off, -1)
    return matrix


def orthogonality_error(vectors: np.ndarray) -> float:
    worst = 0.0
    count = vectors.shape[1]
    for first in range(count):
        for second in range(first, count):
            expected = 1.0 if first == second else 0.0
            worst = max(
                worst,
                float(abs(np.vdot(vectors[:, first], vectors[:, second]) - expected)),
            )
    return worst


def linear_combination(vectors: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
    out = np.zeros(vectors.shape[0], dtype=np.result_type(vectors.dtype, coefficients.dtype))
    for column, coefficient in enumerate(coefficients):
        out += coefficient * vectors[:, column]
    return out


def group_ritz(
    values: np.ndarray,
    weights: np.ndarray,
    residuals: np.ndarray,
    ground_energy: float,
) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    start = 0
    while start < len(values):
        stop = start + 1
        while stop < len(values) and abs(values[stop] - values[start]) <= ENERGY_GROUP_TOL:
            stop += 1
        groups.append(
            {
                "indices": list(range(start, stop)),
                "energy": float(np.mean(values[start:stop])),
                "omega": float(np.mean(values[start:stop]) - ground_energy),
                "weight": float(np.sum(weights[start:stop])),
                "residual_estimate": float(np.max(residuals[start:stop])),
            }
        )
        start = stop
    return groups


def response_metrics(snapshot: dict[str, object], ground_energy: float, start_norm: float) -> dict[str, object]:
    values = np.asarray(snapshot["ritz_values"])
    vectors = np.asarray(snapshot["ritz_vectors"])
    residuals = np.asarray(snapshot["ritz_residual_estimates"])
    weights = start_norm**2 * np.abs(vectors[0, :]) ** 2
    groups = group_ritz(values, weights, residuals, ground_energy)
    positive = [group for group in groups if float(group["omega"]) > 1.0e-10]
    total_weight = float(sum(float(group["weight"]) for group in positive))
    provisional = [
        group for group in positive if float(group["weight"]) > 1.0e-12 * total_weight
    ]
    if not provisional or total_weight <= 0.0:
        return {"resolved": False}
    provisional_active = min(provisional, key=lambda group: float(group["omega"]))
    active_residual = float(provisional_active["residual_estimate"])
    weight_floor = max(
        1.0e-12 * total_weight,
        100.0 * active_residual**2 * start_norm**2,
    )
    selected: list[dict[str, object] | None] = []
    for factor in (0.1, 1.0, 10.0):
        eligible = [
            group for group in positive if float(group["weight"]) > factor * weight_floor
        ]
        selected.append(
            None if not eligible else min(eligible, key=lambda group: float(group["omega"]))
        )
    stable = (
        all(group is not None for group in selected)
        and max(float(group["omega"]) for group in selected if group is not None)
        - min(float(group["omega"]) for group in selected if group is not None)
        <= ENERGY_GROUP_TOL
    )
    if selected[1] is None:
        return {"resolved": False}
    active = selected[1]
    chi_numerator = sum(
        float(group["weight"]) / float(group["omega"]) ** 2 for group in positive
    )
    return {
        "resolved": True,
        "Delta_act": float(active["omega"]),
        "chi_tau": math.sqrt(chi_numerator / total_weight),
        "R_low": float(active["weight"]) / total_weight,
        "active_indices": list(active["indices"]),
        "active_residual_estimate": float(active["residual_estimate"]),
        "total_weight": total_weight,
        "weight_floor": weight_floor,
        "threshold_stable": bool(stable),
        "threshold_omegas": [
            None if group is None else float(group["omega"]) for group in selected
        ],
    }


@dataclass
class KrylovOutcome:
    vectors: np.ndarray
    alphas: list[float]
    betas: list[float]
    snapshots: list[dict[str, object]]
    start_norm: float
    breakdown: bool
    matvecs: int
    orthogonality_error: float


def krylov(
    block: SparseBlock,
    start: np.ndarray,
    kind: str,
    ground_energy: float | None = None,
) -> KrylovOutcome:
    start_norm = float(np.linalg.norm(start))
    if not math.isfinite(start_norm) or start_norm == 0.0:
        raise AssertionError("invalid Krylov start")
    steps = min(MAX_KRYLOV, block.dimension)
    dtype = np.result_type(block.data.dtype, start.dtype)
    vectors = np.zeros((block.dimension, steps), dtype=dtype, order="F")
    vectors[:, 0] = start / start_norm
    alphas: list[float] = []
    betas: list[float] = []
    snapshots: list[dict[str, object]] = []
    breakdown = False
    completed = 0

    for step in range(steps):
        current = vectors[:, step]
        work = block.apply(current)
        alpha = float(np.vdot(current, work).real)
        work -= alpha * current
        if step:
            work -= betas[step - 1] * vectors[:, step - 1]

        # Two scalar MGS passes avoid importing the target's batched complex
        # reorthogonalization route.
        for _ in range(2):
            for prior in range(step + 1):
                coefficient = np.vdot(vectors[:, prior], work)
                work -= coefficient * vectors[:, prior]
        beta = float(np.linalg.norm(work))
        alphas.append(alpha)
        betas.append(beta)
        completed = step + 1
        breakdown = beta <= 1.0e-13

        checkpoint = completed in CHECKPOINTS or breakdown or completed == steps
        stop = False
        if checkpoint:
            tri = tridiagonal(alphas, betas, completed)
            values, ritz_vectors = np.linalg.eigh(tri)
            residuals = np.abs(beta * ritz_vectors[-1, :])
            snapshot: dict[str, object] = {
                "krylov_dimension": completed,
                "ritz_values": values,
                "ritz_vectors": ritz_vectors,
                "ritz_residual_estimates": residuals,
                "lowest_five_ritz_values": values[:5].tolist(),
            }
            if kind == "ground":
                snapshot["ground_energy"] = float(values[0])
                snapshot["ground_residual_estimate"] = float(residuals[0])
                if breakdown:
                    stop = True
                elif len(snapshots) and completed >= 16:
                    previous = snapshots[-1]
                    stop = (
                        relative_difference(
                            float(snapshot["ground_energy"]),
                            float(previous["ground_energy"]),
                        )
                        <= 2.0e-10
                        and float(snapshot["ground_residual_estimate"]) <= 1.0e-10
                    )
            elif kind == "response":
                if ground_energy is None:
                    raise AssertionError("response Krylov requires ground energy")
                metrics = response_metrics(snapshot, ground_energy, start_norm)
                snapshot["metrics"] = metrics
                if breakdown:
                    stop = True
                elif len(snapshots) and metrics.get("resolved"):
                    previous_metrics = snapshots[-1].get("metrics", {})
                    if previous_metrics.get("resolved"):
                        stop = (
                            relative_difference(
                                float(metrics["Delta_act"]),
                                float(previous_metrics["Delta_act"]),
                            )
                            <= 2.0e-7
                            and relative_difference(
                                float(metrics["chi_tau"]),
                                float(previous_metrics["chi_tau"]),
                            )
                            <= 2.0e-7
                            and relative_difference(
                                float(metrics["R_low"]),
                                float(previous_metrics["R_low"]),
                            )
                            <= 2.0e-6
                            and float(metrics["active_residual_estimate"]) <= RESIDUAL_LIMIT
                            and bool(metrics["threshold_stable"])
                        )
            else:
                raise ValueError("unknown Krylov kind")
            snapshots.append(snapshot)
            if stop:
                break

        if breakdown or completed == steps:
            break
        vectors[:, step + 1] = work / beta

    vectors = vectors[:, :completed]
    return KrylovOutcome(
        vectors=vectors,
        alphas=alphas,
        betas=betas,
        snapshots=snapshots,
        start_norm=start_norm,
        breakdown=breakdown,
        matvecs=completed,
        orthogonality_error=orthogonality_error(vectors),
    )


def public_snapshot(snapshot: dict[str, object]) -> dict[str, object]:
    report = {
        key: value
        for key, value in snapshot.items()
        if key not in {"ritz_values", "ritz_vectors", "ritz_residual_estimates"}
    }
    return report


def reconstruct_ground(block: SparseBlock, run: KrylovOutcome) -> tuple[float, np.ndarray, float]:
    final = run.snapshots[-1]
    values = np.asarray(final["ritz_values"])
    ritz_vectors = np.asarray(final["ritz_vectors"])
    size = int(final["krylov_dimension"])
    vector = linear_combination(run.vectors[:, :size], ritz_vectors[:, 0])
    energy = float(values[0])
    residual = float(np.linalg.norm(block.apply(vector) - energy * vector))
    return energy, vector, residual


def active_actual_residual(
    block: SparseBlock,
    run: KrylovOutcome,
    ground_energy: float,
) -> float:
    final = run.snapshots[-1]
    metrics = final.get("metrics", {})
    if not metrics.get("resolved"):
        return math.inf
    values = np.asarray(final["ritz_values"])
    ritz_vectors = np.asarray(final["ritz_vectors"])
    size = int(final["krylov_dimension"])
    worst = 0.0
    for index in metrics["active_indices"]:
        vector = linear_combination(run.vectors[:, :size], ritz_vectors[:, int(index)])
        residual = np.linalg.norm(block.apply(vector) - values[int(index)] * vector)
        worst = max(worst, float(residual))
    return worst


def deterministic_ground_start(dimension: int) -> np.ndarray:
    indices = np.arange(dimension, dtype=float)
    return 1.0 + ((37.0 * indices + 11.0) % 19.0) / 19.0


def structural_controls(length: int) -> dict[str, object]:
    edges = prism_edges(length)
    degrees = [0] * (2 * length)
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    one_h = np.zeros((2 * length, 2 * length), dtype=float)
    for left, right in edges:
        one_h[left, right] = -1.0
        one_h[right, left] = -1.0
    numeric = np.linalg.eigvalsh(one_h)
    formula = np.sort(
        np.asarray(
            [
                -2.0 * math.cos(2.0 * math.pi * momentum / length) + band
                for momentum in range(length)
                for band in (-1.0, 1.0)
            ]
        )
    )
    band_error = float(np.max(np.abs(numeric - formula)))
    return {
        "sites": 2 * length,
        "owner_edges": len(edges),
        "unique_edges": len({frozenset(edge) for edge in edges}),
        "degrees": degrees,
        "bipartite_edges": all(
            (left % length) % 2 != (right % length) % 2 for left, right in edges
        ),
        "one_carrier_band_linf": band_error,
        "q_conservation": "EXACT__EVERY_OWNER_ACTION_SWAPS_ONE_OCCUPIED_AND_ONE_BLANK_SITE",
        "particle_hole": "EXACT__BIT_COMPLEMENT_COMMUTES_WITH_EVERY_OWNER_SWAP",
        "hamiltonian_has_write_count_argument": False,
    }


def authorize_row(length: int, charge: int, authorization: str | None) -> None:
    pair = (length, charge)
    if pair in VALIDATION_ROWS:
        return
    if pair in FUTURE_ROWS and authorization == AUTHORIZATION:
        return
    if pair in FUTURE_ROWS:
        raise PermissionError("L10/L12 row blocked until ALLOW/REQUIRE semantic gate passes")
    raise ValueError("row is outside the frozen centerline")


def calculate_row(
    length: int,
    charge: int,
    authorization: str | None = None,
) -> dict[str, object]:
    authorize_row(length, charge, authorization)
    started = time.perf_counter()
    structural = structural_controls(length)
    bank = build_orbit_bank(length, charge)
    ground_block = build_sparse_block(bank, 0)
    ground_run = krylov(
        ground_block,
        deterministic_ground_start(ground_block.dimension),
        "ground",
    )
    ground_energy, ground_coefficients, ground_residual = reconstruct_ground(
        ground_block, ground_run
    )
    ground_words = expand_to_words(bank, ground_block, ground_coefficients)

    k = 2.0 * math.pi / length
    phases = np.exp(1j * k * np.arange(length))
    response_words = np.zeros(len(bank.words), dtype=np.complex128)
    for row, raw_word in enumerate(bank.words):
        word = int(raw_word)
        diagonal = 0.0j
        for site in range(length):
            diagonal += phases[site] * (
                ((word >> site) & 1) + ((word >> (length + site)) & 1)
            )
        response_words[row] = diagonal * ground_words[row]

    response_block = build_sparse_block(bank, length - 1)
    response_start = project_from_words(bank, response_block, response_words)
    full_norm = float(np.vdot(response_words, response_words).real)
    projected_norm = float(np.vdot(response_start, response_start).real)
    projection_error = abs(full_norm - projected_norm)

    translated = np.empty_like(response_words)
    for row, raw_word in enumerate(bank.words):
        destination = translate(int(raw_word), length)
        translated[bank.word_index[destination]] = response_words[row]
    covariance_error = float(
        np.max(np.abs(translated - np.exp(-1j * k) * response_words))
    )

    response_run = krylov(
        response_block,
        response_start,
        "response",
        ground_energy=ground_energy,
    )
    final_metrics = dict(response_run.snapshots[-1].get("metrics", {}))
    active_residual = active_actual_residual(
        response_block, response_run, ground_energy
    )

    ground_sequence = [public_snapshot(snapshot) for snapshot in ground_run.snapshots]
    response_sequence = [public_snapshot(snapshot) for snapshot in response_run.snapshots]
    ground_checkpoint_stable = ground_run.breakdown
    if len(ground_run.snapshots) >= 2:
        ground_checkpoint_stable = ground_checkpoint_stable or (
            relative_difference(
                float(ground_run.snapshots[-1]["ground_energy"]),
                float(ground_run.snapshots[-2]["ground_energy"]),
            )
            <= 2.0e-10
        )
    response_checkpoint_stable = response_run.breakdown
    if len(response_run.snapshots) >= 2:
        current = response_run.snapshots[-1].get("metrics", {})
        previous = response_run.snapshots[-2].get("metrics", {})
        if current.get("resolved") and previous.get("resolved"):
            response_checkpoint_stable = response_checkpoint_stable or (
                relative_difference(float(current["Delta_act"]), float(previous["Delta_act"]))
                <= 2.0e-7
                and relative_difference(float(current["chi_tau"]), float(previous["chi_tau"]))
                <= 2.0e-7
                and relative_difference(float(current["R_low"]), float(previous["R_low"]))
                <= 2.0e-6
            )

    elapsed = time.perf_counter() - started
    rss = peak_rss_bytes()
    total_matvecs = ground_run.matvecs + response_run.matvecs
    failures: list[str] = []
    if structural["owner_edges"] != 3 * length or structural["unique_edges"] != 3 * length:
        failures.append("OWNER_CENSUS")
    if any(degree != 3 for degree in structural["degrees"]):
        failures.append("DEGREE")
    if not structural["bipartite_edges"] or structural["one_carrier_band_linf"] > 1.0e-12:
        failures.append("STRUCTURAL_SPECTRUM")
    if max(ground_block.hermiticity_error, response_block.hermiticity_error) > HERMITICITY_LIMIT:
        failures.append("HERMITICITY")
    if max(ground_run.orthogonality_error, response_run.orthogonality_error) > ORTHOGONALITY_LIMIT:
        failures.append("ORTHOGONALITY")
    if ground_residual > RESIDUAL_LIMIT or not ground_checkpoint_stable:
        failures.append("GROUND_CONVERGENCE")
    if active_residual > RESIDUAL_LIMIT or not response_checkpoint_stable:
        failures.append("RESPONSE_CONVERGENCE")
    if not final_metrics.get("resolved") or not final_metrics.get("threshold_stable"):
        failures.append("ACTIVE_THRESHOLD")
    if float(final_metrics.get("R_low", 0.0)) < 1.0e-6:
        failures.append("ACTIVE_RESIDUE")
    if projection_error > PROJECTION_LIMIT or covariance_error > PROJECTION_LIMIT:
        failures.append("RESPONSE_PROJECTION")
    if elapsed > WALL_LIMIT_SECONDS:
        failures.append("WALL_GUARD")
    if rss > RSS_LIMIT_BYTES:
        failures.append("RSS_GUARD")
    if total_matvecs > MATVEC_LIMIT:
        failures.append("MATVEC_GUARD")

    return {
        "L": length,
        "q": charge,
        "rho": charge / (2.0 * length),
        "sector_dimension": len(bank.words),
        "translation_orbits": len(bank.orbits),
        "ground_block_dimension": ground_block.dimension,
        "ground_block_nnz": len(ground_block.data),
        "response_block_dimension": response_block.dimension,
        "response_block_nnz": len(response_block.data),
        "ground_energy": ground_energy,
        "ground_residual": ground_residual,
        "Delta_act": final_metrics.get("Delta_act"),
        "chi_tau": final_metrics.get("chi_tau"),
        "R_low": final_metrics.get("R_low"),
        "active_actual_residual": active_residual,
        "response_total_weight": final_metrics.get("total_weight"),
        "weight_floor": final_metrics.get("weight_floor"),
        "threshold_stable": final_metrics.get("threshold_stable", False),
        "response_projection_error": projection_error,
        "response_momentum_covariance_error": covariance_error,
        "ground_block_hermiticity_error": ground_block.hermiticity_error,
        "response_block_hermiticity_error": response_block.hermiticity_error,
        "ground_krylov_orthogonality_error": ground_run.orthogonality_error,
        "response_krylov_orthogonality_error": response_run.orthogonality_error,
        "ground_krylov_breakdown": ground_run.breakdown,
        "response_krylov_breakdown": response_run.breakdown,
        "ground_sequence": ground_sequence,
        "response_sequence": response_sequence,
        "ground_matvecs": ground_run.matvecs,
        "response_matvecs": response_run.matvecs,
        "total_matvecs": total_matvecs,
        "wall_seconds": elapsed,
        "peak_rss_bytes": rss,
        "structural_controls": structural,
        "failures": failures,
        "status": "RESOLVED" if not failures else "UNRESOLVED",
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    if sha256(METHOD) != EXPECTED_METHOD_SHA256:
        raise AssertionError("frozen methodology hash mismatch")
    parser = argparse.ArgumentParser()
    parser.add_argument("--single", action="store_true")
    parser.add_argument("--L", type=int)
    parser.add_argument("--q", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--authorization")
    arguments = parser.parse_args()

    if arguments.single:
        if arguments.L is None or arguments.q is None or arguments.output is None:
            parser.error("--single requires --L, --q, and --output")
        write_json(
            arguments.output,
            calculate_row(arguments.L, arguments.q, arguments.authorization),
        )
        return

    if any(value is not None for value in (arguments.L, arguments.q, arguments.output, arguments.authorization)):
        parser.error("row arguments are valid only with --single")
    started = time.perf_counter()
    rows = []
    for length, charge in VALIDATION_ROWS:
        row = calculate_row(length, charge)
        write_json(RAW / f"ROW_L{length}_Q{charge}.json", row)
        rows.append(row)
    result = {
        "schema": "INDEPENDENT_EXTENDED_CENTERLINE_VALIDATION_V001",
        "methodology_sha256": sha256(METHOD),
        "implementation_sha256": sha256(Path(__file__).resolve()),
        "scope": "L4_Q2__L6_Q3__L8_Q4_VALIDATION_ONLY",
        "new_rows_executed": [],
        "all_rows_resolved": all(row["status"] == "RESOLVED" for row in rows),
        "rows": rows,
        "telemetry": {
            "wall_seconds": time.perf_counter() - started,
            "peak_rss_bytes": peak_rss_bytes(),
            "worker_wall_seconds_sum": sum(float(row["wall_seconds"]) for row in rows),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "claim_boundary": {
            "validated": "INDEPENDENT_SPARSE_ADAPTIVE_RESPONSE_CYCLIC_KRYLOV_THROUGH_L8",
            "not_claimed": [
                "L10_OR_L12_RESULT",
                "Z_EQUALS_ONE",
                "GAPLESS_LIMIT",
                "CONTINUUM_ALGEBRA",
                "GRAVITY",
            ],
        },
    }
    write_json(OUT, result)
    if not result["all_rows_resolved"]:
        raise SystemExit("UNRESOLVED_VALIDATION")
    print("PASS_INDEPENDENT_CENTERLINE_VALIDATION_RAW__L4_L6_L8_ONLY")


if __name__ == "__main__":
    main()
