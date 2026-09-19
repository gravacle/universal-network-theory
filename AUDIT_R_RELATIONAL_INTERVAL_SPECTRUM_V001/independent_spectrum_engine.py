#!/usr/bin/env python3
"""Independent matrix-free prism response spectrum engine.

This module deliberately has no loader for target code or target matrices.
Physical execution is gated by a separately built hash-pinned freeze.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import sys
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np


SCHEMA = "RELATIONAL_INTERVAL_SPECTRUM_INDEX_V001"
RUN_TOKEN = "RUN_HASH_PINNED_BLIND_RELATIONAL_INTERVAL_SPECTRUM_V001"
CHECKPOINTS = (16, 32, 64, 96, 128)
MAX_VECTORS = 128
MAX_MATVECS = 2000
MAX_SECONDS = 10_800.0
MAX_ADDRESS_BYTES = 6 * 1024**3
EXPECTED_MANIFEST_SCHEMA = "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"
EXPECTED_MANIFEST_STATUS = (
    "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY"
)
EXPECTED_PROTOCOL_SHA256 = (
    "d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95"
)


class FailClosed(RuntimeError):
    """A contract, custody, resource, or numerical guard failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_repo_file(repo_root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise FailClosed(f"non-repository-relative path: {relative!r}")
    resolved_root = repo_root.resolve()
    resolved = (resolved_root / candidate).resolve(strict=True)
    if resolved_root not in resolved.parents or not resolved.is_file():
        raise FailClosed(f"path escapes repository or is not a file: {relative!r}")
    return resolved


def finite_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FailClosed(f"{label} is not a JSON number")
    result = float(value)
    if not math.isfinite(result):
        raise FailClosed(f"{label} is not finite")
    return result


def install_address_space_guard() -> None:
    if not hasattr(resource, "RLIMIT_AS"):
        return
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    requested = MAX_ADDRESS_BYTES
    if hard != resource.RLIM_INFINITY:
        requested = min(requested, hard)
    if soft == resource.RLIM_INFINITY or soft > requested:
        resource.setrlimit(resource.RLIMIT_AS, (requested, hard))


def peak_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform.startswith("linux"):
        return value * 1024
    return value


def prism_edges(L: int) -> tuple[tuple[int, int], ...]:
    if isinstance(L, bool) or not isinstance(L, int) or L < 3:
        raise FailClosed("L must be an integer at least 3")
    edges: set[tuple[int, int]] = set()
    for rail in (0, 1):
        offset = rail * L
        for i in range(L):
            u, v = offset + i, offset + ((i + 1) % L)
            edges.add((min(u, v), max(u, v)))
    for i in range(L):
        edges.add((i, L + i))
    ordered = tuple(sorted(edges))
    degree = [0] * (2 * L)
    for u, v in ordered:
        degree[u] += 1
        degree[v] += 1
    if len(ordered) != 3 * L or any(item != 3 for item in degree):
        raise FailClosed("internal prism reconstruction failure")
    return ordered


def fixed_charge_basis(site_count: int, q: int) -> np.ndarray:
    if (
        isinstance(site_count, bool)
        or isinstance(q, bool)
        or not isinstance(site_count, int)
        or not isinstance(q, int)
        or site_count < 1
        or not 0 <= q <= site_count
    ):
        raise FailClosed("invalid fixed-charge basis request")
    dimension = math.comb(site_count, q)
    masks = np.empty(dimension, dtype=np.uint64)
    filled = 0
    for row, occupied in enumerate(combinations(range(site_count), q)):
        mask = 0
        for site in occupied:
            mask |= 1 << site
        masks[row] = mask
        filled += 1
    if filled != dimension:
        raise FailClosed("basis census mismatch")
    return masks


@dataclass(frozen=True)
class TransitionTable:
    L: int
    q: int
    basis: np.ndarray
    sources: tuple[np.ndarray, ...]
    destinations: tuple[np.ndarray, ...]
    nonzero_count: int


def translate_mask(mask: int, L: int, shift: int = 1) -> int:
    shift %= L
    rail_mask = (1 << L) - 1
    output = 0
    for rail in (0, 1):
        value = (mask >> (rail * L)) & rail_mask
        rotated = ((value << shift) | (value >> (L - shift))) & rail_mask if shift else value
        output |= rotated << (rail * L)
    return output


@dataclass(frozen=True)
class OrbitCatalog:
    L: int
    q: int
    basis: np.ndarray
    basis_index: dict[int, int]
    orbits: tuple[tuple[int, ...], ...]
    membership: dict[int, tuple[int, int]]


def build_orbit_catalog(L: int, q: int) -> OrbitCatalog:
    basis = fixed_charge_basis(2 * L, q)
    basis_index = {int(mask): index for index, mask in enumerate(basis)}
    unseen = set(basis_index)
    orbit_rows: list[tuple[int, ...]] = []
    while unseen:
        seed = min(unseen)
        rotations: list[int] = []
        value = seed
        while value not in rotations:
            rotations.append(value)
            value = translate_mask(value, L)
        representative = min(rotations)
        states: list[int] = []
        value = representative
        while not states or value != representative:
            states.append(value)
            value = translate_mask(value, L)
        for state in states:
            unseen.discard(state)
        orbit_rows.append(tuple(states))
    orbit_rows.sort(key=lambda states: states[0])
    membership: dict[int, tuple[int, int]] = {}
    for orbit_index, states in enumerate(orbit_rows):
        for translation, state in enumerate(states):
            if state in membership:
                raise FailClosed("duplicate orbit membership")
            membership[state] = (orbit_index, translation)
    if set(membership) != set(basis_index):
        raise FailClosed("orbit catalog does not partition the sector")
    return OrbitCatalog(
        L=L,
        q=q,
        basis=basis,
        basis_index=basis_index,
        orbits=tuple(orbit_rows),
        membership=membership,
    )


@dataclass(frozen=True)
class OrbitBlock:
    catalog: OrbitCatalog
    momentum: int
    compatible_orbits: tuple[int, ...]
    orbit_to_block: dict[int, int]
    rows: np.ndarray
    columns: np.ndarray
    amplitudes: np.ndarray
    nonzero_count: int

    @property
    def dimension(self) -> int:
        return len(self.compatible_orbits)


def build_orbit_block(catalog: OrbitCatalog, momentum: int) -> OrbitBlock:
    L = catalog.L
    momentum %= L
    compatible = tuple(
        orbit_index
        for orbit_index, states in enumerate(catalog.orbits)
        if (momentum * len(states)) % L == 0
    )
    orbit_to_block = {orbit_index: block for block, orbit_index in enumerate(compatible)}
    entries: dict[tuple[int, int], complex] = {}
    edges = prism_edges(L)
    for source_block, source_orbit in enumerate(compatible):
        source_states = catalog.orbits[source_orbit]
        source_norm = math.sqrt(len(source_states))
        for source_translation, mask in enumerate(source_states):
            source_phase = np.exp(2j * np.pi * momentum * source_translation / L) / source_norm
            for u, v in edges:
                if ((mask >> u) & 1) == ((mask >> v) & 1):
                    continue
                destination_mask = mask ^ (1 << u) ^ (1 << v)
                destination_orbit, destination_translation = catalog.membership[destination_mask]
                destination_block = orbit_to_block.get(destination_orbit)
                if destination_block is None:
                    # Individual hops can land in an incompatible orbit.  Its
                    # projected amplitude cancels only after the complete
                    # source-orbit sum, so it has no coordinate in this block.
                    continue
                destination_norm = math.sqrt(len(catalog.orbits[destination_orbit]))
                destination_phase = (
                    np.exp(2j * np.pi * momentum * destination_translation / L)
                    / destination_norm
                )
                key = (destination_block, source_block)
                entries[key] = entries.get(key, 0.0j) - np.conjugate(destination_phase) * source_phase
    retained = [
        (row, column, amplitude)
        for (row, column), amplitude in sorted(entries.items())
        if abs(amplitude) > 1e-13
    ]
    rows = np.asarray([item[0] for item in retained], dtype=np.int64)
    columns = np.asarray([item[1] for item in retained], dtype=np.int64)
    amplitudes = np.asarray([item[2] for item in retained], dtype=np.complex128)
    transpose = {(row, column): amplitude for row, column, amplitude in retained}
    hermiticity_error = max(
        (
            abs(amplitude - np.conjugate(transpose.get((column, row), complex("nan"))))
            for row, column, amplitude in retained
        ),
        default=0.0,
    )
    if not math.isfinite(hermiticity_error) or hermiticity_error > 1e-12:
        raise FailClosed("reconstructed orbit block is not Hermitian")
    return OrbitBlock(
        catalog=catalog,
        momentum=momentum,
        compatible_orbits=compatible,
        orbit_to_block=orbit_to_block,
        rows=rows,
        columns=columns,
        amplitudes=amplitudes,
        nonzero_count=len(retained),
    )


def expand_block_vector(block: OrbitBlock, coefficients: np.ndarray) -> np.ndarray:
    if coefficients.ndim != 1 or coefficients.size != block.dimension:
        raise FailClosed("block expansion dimension mismatch")
    full = np.zeros(block.catalog.basis.size, dtype=np.complex128)
    L, m = block.catalog.L, block.momentum
    for block_row, orbit_index in enumerate(block.compatible_orbits):
        states = block.catalog.orbits[orbit_index]
        norm = math.sqrt(len(states))
        for translation, state in enumerate(states):
            phase = np.exp(2j * np.pi * m * translation / L) / norm
            full[block.catalog.basis_index[state]] = coefficients[block_row] * phase
    return full


def project_full_vector(block: OrbitBlock, full: np.ndarray) -> np.ndarray:
    if full.ndim != 1 or full.size != block.catalog.basis.size:
        raise FailClosed("block projection dimension mismatch")
    projected = np.zeros(block.dimension, dtype=np.complex128)
    L, m = block.catalog.L, block.momentum
    for block_row, orbit_index in enumerate(block.compatible_orbits):
        states = block.catalog.orbits[orbit_index]
        norm = math.sqrt(len(states))
        for translation, state in enumerate(states):
            phase = np.exp(2j * np.pi * m * translation / L) / norm
            projected[block_row] += np.conjugate(phase) * full[block.catalog.basis_index[state]]
    return projected


def build_transition_table(L: int, q: int) -> TransitionTable:
    basis = fixed_charge_basis(2 * L, q)
    lookup = {int(mask): index for index, mask in enumerate(basis)}
    sources: list[np.ndarray] = []
    destinations: list[np.ndarray] = []
    nonzero_count = 0
    for u, v in prism_edges(L):
        src: list[int] = []
        dst: list[int] = []
        flip = (1 << u) | (1 << v)
        for row, mask_value in enumerate(basis):
            mask = int(mask_value)
            if ((mask >> u) & 1) != ((mask >> v) & 1):
                src.append(row)
                try:
                    dst.append(lookup[mask ^ flip])
                except KeyError as error:
                    raise FailClosed("transition left fixed-charge sector") from error
        src_array = np.asarray(src, dtype=np.int64)
        dst_array = np.asarray(dst, dtype=np.int64)
        sources.append(src_array)
        destinations.append(dst_array)
        nonzero_count += len(src)
    return TransitionTable(
        L=L,
        q=q,
        basis=basis,
        sources=tuple(sources),
        destinations=tuple(destinations),
        nonzero_count=nonzero_count,
    )


class GuardedHamiltonian:
    def __init__(self, representation: TransitionTable | OrbitBlock, start_time: float) -> None:
        self.representation = representation
        self.start_time = start_time
        self.matvecs = 0

    @property
    def dimension(self) -> int:
        if isinstance(self.representation, OrbitBlock):
            return self.representation.dimension
        return int(self.representation.basis.size)

    def check_guards(self) -> None:
        if self.matvecs > MAX_MATVECS:
            raise FailClosed("2000-matvec sector guard exceeded")
        if time.monotonic() - self.start_time > MAX_SECONDS:
            raise FailClosed("3-hour sector wall-time guard exceeded")
        if peak_rss_bytes() > MAX_ADDRESS_BYTES:
            raise FailClosed("6-GiB sector peak-RSS guard exceeded")

    def __call__(self, vector: np.ndarray) -> np.ndarray:
        self.check_guards()
        if vector.ndim != 1 or vector.size != self.dimension:
            raise FailClosed("matvec dimension mismatch")
        self.matvecs += 1
        self.check_guards()
        output = np.zeros_like(vector)
        if isinstance(self.representation, OrbitBlock):
            np.add.at(
                output,
                self.representation.rows,
                self.representation.amplitudes * vector[self.representation.columns],
            )
        else:
            for src, dst in zip(self.representation.sources, self.representation.destinations):
                output[dst] -= vector[src]
        self.check_guards()
        return output


@dataclass
class LanczosResult:
    alphas: np.ndarray
    betas: np.ndarray
    vectors: list[np.ndarray]
    checkpoints: list[dict[str, object]]
    exact_termination: bool
    final_beta: float
    orthogonality_error: float


def _ritz_record(alphas: Sequence[float], betas: Sequence[float], tail: float) -> dict[str, object]:
    k = len(alphas)
    tridiagonal = np.diag(np.asarray(alphas, dtype=np.float64))
    if k > 1:
        off = np.asarray(betas[: k - 1], dtype=np.float64)
        tridiagonal += np.diag(off, 1) + np.diag(off, -1)
    values, vectors = np.linalg.eigh(tridiagonal)
    count = min(5, k)
    residuals = np.abs(tail * vectors[-1, :count])
    return {
        "krylov_dimension": k,
        "lowest_ritz_values": [float(item) for item in values[:count]],
        "lowest_ritz_residuals": [float(item) for item in residuals],
    }


def fully_reorthogonalized_lanczos(
    matvec: Callable[[np.ndarray], np.ndarray],
    seed: np.ndarray,
    *,
    max_vectors: int = MAX_VECTORS,
    termination_tolerance: float = 1e-13,
) -> LanczosResult:
    if not 1 <= max_vectors <= MAX_VECTORS:
        raise FailClosed("Lanczos vector cap is outside frozen range")
    norm = float(np.linalg.norm(seed))
    if not math.isfinite(norm) or norm <= 0.0:
        raise FailClosed("Lanczos seed norm is not strictly positive and finite")
    current = np.asarray(seed, dtype=np.complex128) / norm
    vectors: list[np.ndarray] = []
    alphas: list[float] = []
    betas: list[float] = []
    checkpoints: list[dict[str, object]] = []
    previous: np.ndarray | None = None
    previous_beta = 0.0
    final_beta = math.inf
    exact_termination = False

    for _ in range(max_vectors):
        vectors.append(current.copy())
        work = matvec(current)
        alpha_complex = np.vdot(current, work)
        if abs(float(alpha_complex.imag)) > 1e-12:
            raise FailClosed("non-real Lanczos alpha violates Hermiticity")
        alpha = float(alpha_complex.real)
        work = work - alpha * current
        if previous is not None:
            work = work - previous_beta * previous
        # Two deterministic complete MGS passes.
        for _pass in range(2):
            for basis_vector in vectors:
                work = work - np.vdot(basis_vector, work) * basis_vector
        beta = float(np.linalg.norm(work))
        if not math.isfinite(alpha) or not math.isfinite(beta):
            raise FailClosed("non-finite Lanczos coefficient")
        alphas.append(alpha)
        final_beta = beta
        k = len(alphas)
        terminate = beta <= termination_tolerance
        if k in CHECKPOINTS or terminate or k == max_vectors:
            checkpoints.append(_ritz_record(alphas, betas, beta))
        if terminate:
            exact_termination = True
            break
        if k == max_vectors:
            break
        betas.append(beta)
        previous, current = current, work / beta
        previous_beta = beta

    stacked = np.column_stack(vectors)
    gram = stacked.conj().T @ stacked
    orthogonality_error = float(np.max(np.abs(gram - np.eye(len(vectors)))))
    if len(vectors) > MAX_VECTORS:
        raise FailClosed("retained-vector guard exceeded")
    return LanczosResult(
        alphas=np.asarray(alphas, dtype=np.float64),
        betas=np.asarray(betas, dtype=np.float64),
        vectors=vectors,
        checkpoints=checkpoints,
        exact_termination=exact_termination,
        final_beta=final_beta,
        orthogonality_error=orthogonality_error,
    )


def final_ritz(result: LanczosResult) -> tuple[np.ndarray, np.ndarray]:
    k = len(result.alphas)
    tri = np.diag(result.alphas)
    if k > 1:
        tri += np.diag(result.betas[: k - 1], 1)
        tri += np.diag(result.betas[: k - 1], -1)
    return np.linalg.eigh(tri)


def response_checkpoint_metrics(
    result: LanczosResult,
    k: int,
    ground_energy: float,
    response_norm: float,
) -> dict[str, object]:
    if not 1 <= k <= len(result.alphas):
        raise FailClosed("response checkpoint dimension outside Lanczos chain")
    diagonal = result.alphas[:k]
    off_diagonal = result.betas[: max(0, k - 1)]
    tri = np.diag(diagonal)
    if k > 1:
        tri += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
    values, vectors = np.linalg.eigh(tri)
    residues = response_norm**2 * np.abs(vectors[0, :]) ** 2
    total_weight = float(np.sum(residues))
    weight_floor = max(1e-14 * total_weight, 1e-15)
    tail = result.betas[k - 1] if k < len(result.alphas) else result.final_beta

    def active_at(threshold: float) -> int:
        candidates = [
            index
            for index, value in enumerate(values)
            if float(value - ground_energy) > 1e-12 and float(residues[index]) > threshold
        ]
        if not candidates:
            raise FailClosed("checkpoint has no positive pole above threshold")
        return candidates[0]

    threshold_indices = {
        "floor_over_10": active_at(weight_floor / 10.0),
        "floor": active_at(weight_floor),
        "ten_floor": active_at(10.0 * weight_floor),
    }
    if len(set(threshold_indices.values())) != 1:
        raise FailClosed("active-pole threshold identity is unstable")
    active = threshold_indices["floor"]
    chi_tau = float(
        sum(
            float(weight) / float(value - ground_energy)
            for value, weight in zip(values, residues)
            if float(value - ground_energy) > 1e-12
        )
    )
    return {
        "active_pole_index": active,
        "active_pole_energy": float(values[active]),
        "Delta_act": float(values[active] - ground_energy),
        "chi_tau": chi_tau,
        "R_low": float(residues[active]),
        "active_pole_residual": float(abs(tail * vectors[-1, active])),
        "total_response_weight": total_weight,
        "adaptive_weight_floor": weight_floor,
        "threshold_active_indices": threshold_indices,
    }


def reconstruct_ritz_vector(result: LanczosResult, coefficients: np.ndarray) -> np.ndarray:
    if len(result.vectors) != coefficients.size:
        raise FailClosed("Ritz-vector reconstruction dimension mismatch")
    output = np.zeros_like(result.vectors[0])
    for coefficient, basis_vector in zip(coefficients, result.vectors):
        output += coefficient * basis_vector
    norm = float(np.linalg.norm(output))
    if not math.isfinite(norm) or norm <= 0:
        raise FailClosed("invalid reconstructed Ritz vector")
    return output / norm


def total_rail_momentum_one_multiplier(catalog: OrbitCatalog) -> np.ndarray:
    phases = np.exp(2j * np.pi * np.arange(catalog.L) / catalog.L)
    values = np.empty(catalog.basis.size, dtype=np.complex128)
    for row, mask_value in enumerate(catalog.basis):
        mask = int(mask_value)
        total = 0.0j
        for j, phase in enumerate(phases):
            total += phase * (((mask >> j) & 1) + ((mask >> (catalog.L + j)) & 1))
        values[row] = total / catalog.q if catalog.q else 0.0j
    return values


def hermiticity_probe(operator: GuardedHamiltonian, dimension: int) -> float:
    rng = np.random.default_rng(0x5EED)
    left = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
    right = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
    left /= np.linalg.norm(left)
    right /= np.linalg.norm(right)
    discrepancy = np.vdot(left, operator(right)) - np.vdot(operator(left), right)
    return float(abs(discrepancy))


def sector_spectrum(L: int, q: int, *, synthetic: bool = False) -> dict[str, object]:
    if not synthetic:
        install_address_space_guard()
    started = time.monotonic()
    catalog = build_orbit_catalog(L, q)
    ground_block = build_orbit_block(catalog, 0)
    response_block = build_orbit_block(catalog, 1)
    ground_operator = GuardedHamiltonian(ground_block, started)
    response_operator = GuardedHamiltonian(response_block, started)
    ground_hermiticity = hermiticity_probe(ground_operator, ground_operator.dimension)
    response_hermiticity = (
        hermiticity_probe(response_operator, response_operator.dimension)
        if response_operator.dimension
        else 0.0
    )
    hermiticity_error = max(ground_hermiticity, response_hermiticity)
    if hermiticity_error > 1e-12:
        raise FailClosed("Hermiticity guard failed")
    # Projection of the positive full-space all-ones seed into m=0.
    ground_seed = np.asarray(
        [math.sqrt(len(catalog.orbits[index])) for index in ground_block.compatible_orbits],
        dtype=np.complex128,
    )
    ground = fully_reorthogonalized_lanczos(ground_operator, ground_seed)
    ground_values, ground_vectors = final_ritz(ground)
    ground_energy = float(ground_values[0])
    ground_residual = float(abs(ground.final_beta * ground_vectors[-1, 0]))
    if ground_residual > 1e-9:
        raise FailClosed("ground residual guard failed")
    if ground.orthogonality_error > 1e-10:
        raise FailClosed("ground Krylov orthogonality guard failed")
    ground_block_vector = reconstruct_ritz_vector(ground, ground_vectors[:, 0])
    ground_full_vector = expand_block_vector(ground_block, ground_block_vector)
    raw_full = total_rail_momentum_one_multiplier(catalog) * ground_full_vector
    response_raw = project_full_vector(response_block, raw_full)
    response_norm = float(np.linalg.norm(response_raw))
    projected_full = expand_block_vector(response_block, response_raw)
    projection_error = float(np.linalg.norm(raw_full - projected_full))

    common: dict[str, object] = {
        "L": L,
        "q": q,
        "rho": [q, 2 * L],
        "raw_sector_dimension": math.comb(2 * L, q),
        "orbit_count": len(catalog.orbits),
        "ground_block_dimension": ground_block.dimension,
        "block_dimension": response_block.dimension,
        "ground_sparse_nonzero_count": ground_block.nonzero_count,
        "sparse_nonzero_count": response_block.nonzero_count,
        "ground_energy": ground_energy,
        "ground_residual": ground_residual,
        "ground_checkpoints": ground.checkpoints,
        "ground_exact_termination": ground.exact_termination,
        "ground_krylov_dimension": len(ground.alphas),
        "ground_orthogonality_error": ground.orthogonality_error,
        "hermiticity_error": hermiticity_error,
        "response_norm": response_norm,
    }
    if response_norm <= 1e-14:
        common.update(
            {
                "status": "ZERO_RESPONSE_NORM__ATOM_NONPASSING",
                "response_checkpoints": [],
                "total_matvecs": ground_operator.matvecs + response_operator.matvecs,
                "sector_wall_seconds": time.monotonic() - started,
                "sector_peak_rss_bytes": peak_rss_bytes(),
            }
        )
        return common

    if projection_error > 1e-9:
        raise FailClosed("response projection closure guard failed")
    response = fully_reorthogonalized_lanczos(response_operator, response_raw / response_norm)
    response_checkpoints: list[dict[str, object]] = []
    for record in response.checkpoints:
        enriched = dict(record)
        enriched.update(
            response_checkpoint_metrics(
                response,
                int(record["krylov_dimension"]),
                ground_energy,
                response_norm,
            )
        )
        response_checkpoints.append(enriched)
    final_metrics = response_checkpoints[-1]
    active = int(final_metrics["active_pole_index"])
    delta = float(final_metrics["Delta_act"])
    chi_tau = float(final_metrics["chi_tau"])
    residue = float(final_metrics["R_low"])
    active_residual = float(final_metrics["active_pole_residual"])
    total_weight = float(final_metrics["total_response_weight"])
    weight_floor = float(final_metrics["adaptive_weight_floor"])
    if len(response_checkpoints) >= 2:
        previous_metrics = response_checkpoints[-2]

        def relative_drift(label: str) -> float:
            latest = float(final_metrics[label])
            previous_value = float(previous_metrics[label])
            return abs(latest - previous_value) / max(abs(latest), abs(previous_value), 1e-15)

        delta_drift = relative_drift("Delta_act")
        chi_drift = relative_drift("chi_tau")
        residue_drift = relative_drift("R_low")
        final_metrics["last_pair_relative_drift_Delta_act"] = delta_drift
        final_metrics["last_pair_relative_drift_chi_tau"] = chi_drift
        final_metrics["last_pair_relative_drift_R_low"] = residue_drift
        if delta_drift > 2e-7 or chi_drift > 2e-7 or residue_drift > 2e-6:
            raise FailClosed("response last-pair drift guard failed")
    elif not response.exact_termination or len(response.alphas) >= MAX_VECTORS:
        raise FailClosed("one-checkpoint response lacks sub-cap exact termination")
    if active_residual > 1e-9:
        raise FailClosed("active-pole residual guard failed")
    if response.orthogonality_error > 1e-10:
        raise FailClosed("response Krylov orthogonality guard failed")
    if not (delta > 0.0 and chi_tau > 0.0 and 1e-6 <= residue <= 1.0 + 1e-12):
        raise FailClosed("resolved response positivity/probability guard failed")
    if not total_weight > 10.0 * weight_floor:
        raise FailClosed("response support bound failed")
    ground_operator.check_guards()
    response_operator.check_guards()
    common.update(
        {
            "status": "RESOLVED_POSITIVE_RESPONSE_SECTOR",
            "Delta_act": delta,
            "chi_tau": chi_tau,
            "R_low": residue,
            "active_pole_index": active,
            "active_pole_energy": final_metrics["active_pole_energy"],
            "active_pole_residual": active_residual,
            "response_checkpoints": response_checkpoints,
            "response_exact_termination": response.exact_termination,
            "response_krylov_dimension": len(response.alphas),
            "response_orthogonality_error": response.orthogonality_error,
            "response_projection_error": projection_error,
            "total_response_weight": total_weight,
            "adaptive_weight_floor": weight_floor,
            "total_matvecs": ground_operator.matvecs + response_operator.matvecs,
            "sector_wall_seconds": time.monotonic() - started,
            "sector_peak_rss_bytes": peak_rss_bytes(),
        }
    )
    return common


def _load_pinned_json(path: Path, expected_hash: str) -> dict[str, object]:
    if not path.is_file() or len(expected_hash) != 64 or sha256_file(path) != expected_hash:
        raise FailClosed(f"hash-pinned JSON unavailable or mismatched: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise FailClosed(f"top-level JSON object required: {path}")
    return value


def _verify_freeze_custody(freeze_path: Path, freeze: dict[str, object]) -> Path:
    resolved_freeze = freeze_path.resolve()
    repo_root: Path | None = None
    for candidate in (resolved_freeze.parent, *resolved_freeze.parents):
        if (candidate / ".git").exists():
            repo_root = candidate
            break
    if repo_root is None:
        raise FailClosed("cannot locate repository root for freeze custody")
    bindings = (
        ("accumulation_manifest_path", "accumulation_manifest_sha256"),
        ("sector_plan_path", "sector_plan_sha256"),
        ("pre_output_method_freeze_path", "pre_output_method_freeze_sha256"),
        ("implementation_path", "implementation_sha256"),
        ("methodology_path", "methodology_sha256"),
        ("builder_path", "builder_sha256"),
        ("self_test_result_path", "self_test_result_sha256"),
    )
    for path_key, hash_key in bindings:
        relative, claimed = freeze.get(path_key), freeze.get(hash_key)
        if not isinstance(relative, str) or not isinstance(claimed, str):
            raise FailClosed(f"freeze binding absent: {path_key}/{hash_key}")
        resolved = regular_repo_file(repo_root, relative)
        if sha256_file(resolved) != claimed:
            raise FailClosed(f"freeze dependency hash mismatch: {relative}")
    if Path(freeze["implementation_path"]).name != Path(__file__).name:
        raise FailClosed("runnable freeze identifies a different implementation")
    if sha256_file(Path(__file__).resolve()) != freeze["implementation_sha256"]:
        raise FailClosed("executing implementation differs from frozen implementation")
    return repo_root


def _relative_sse(actual: np.ndarray, predicted: np.ndarray) -> float:
    scale = np.maximum(np.abs(actual), 1e-15)
    return float(np.sum(((predicted - actual) / scale) ** 2))


def _leave_one_out_linear(actual: np.ndarray, design: np.ndarray) -> float:
    predicted = np.empty_like(actual)
    for held in range(actual.size):
        keep = np.arange(actual.size) != held
        coefficients = np.linalg.lstsq(design[keep], actual[keep], rcond=None)[0]
        predicted[held] = float(design[held] @ coefficients)
    return _relative_sse(actual, predicted)


def _power_exponent(sizes: np.ndarray, values: np.ndarray, inverse: bool) -> tuple[float, float]:
    slope, intercept = np.polyfit(np.log(sizes), np.log(values), 1)
    exponent = -float(slope) if inverse else float(slope)
    prediction = np.exp(intercept) * sizes ** slope
    return exponent, _relative_sse(values, prediction)


def classify_atom(atom: dict[str, object], rows: dict[str, object]) -> dict[str, object]:
    q_by_L = atom.get("q_by_L")
    if not isinstance(q_by_L, dict):
        raise FailClosed("frozen atom plan lacks q_by_L")
    sizes = np.asarray((4, 6, 8, 10, 12), dtype=np.float64)
    selected: list[dict[str, object]] = []
    for L in (4, 6, 8, 10, 12):
        q = q_by_L.get(str(L))
        if q == 0:
            return {
                "status": "ZERO_RESPONSE_NORM__ATOM_NONPASSING",
                "classification": None,
            }
        key = f"L{L}_q{q}"
        row = rows.get(key)
        if not isinstance(row, dict) or row.get("status") != "RESOLVED_POSITIVE_RESPONSE_SECTOR":
            raise FailClosed(f"atom references absent or unresolved positive sector: {key}")
        selected.append(row)
    gaps = np.asarray([finite_number(row["Delta_act"], "Delta_act") for row in selected])
    chis = np.asarray([finite_number(row["chi_tau"], "chi_tau") for row in selected])
    residues = np.asarray([finite_number(row["R_low"], "R_low") for row in selected])
    z, free_sse = _power_exponent(sizes, gaps, True)
    y, _chi_sse = _power_exponent(sizes, chis, False)
    fixed_design = np.column_stack((1.0 / sizes, 1.0 / sizes**2))
    fixed_sse = _leave_one_out_linear(gaps, fixed_design)
    best_positive_sse = math.inf
    best_positive_z = math.nan
    best_positive_limit = math.nan
    # Deterministic bounded refinement, independent of scipy and target code.
    left, right = 0.25, 4.0
    for _ in range(6):
        grid = np.linspace(left, right, 401)
        local: list[tuple[float, float, float]] = []
        for exponent in grid:
            design = np.column_stack((np.ones_like(sizes), sizes ** (-exponent)))
            coefficients = np.linalg.lstsq(design, gaps, rcond=None)[0]
            prediction = design @ coefficients
            score = _relative_sse(gaps, prediction)
            if coefficients[0] > 0.0:
                local.append((score, float(exponent), float(coefficients[0])))
        if not local:
            break
        best_positive_sse, best_positive_z, best_positive_limit = min(local)
        spacing = (right - left) / 400.0
        left = max(0.25, best_positive_z - spacing)
        right = min(4.0, best_positive_z + spacing)
    monotone = bool(np.all(np.diff(gaps) < 0.0) and np.all(np.diff(chis) > 0.0))
    model_order = bool(fixed_sse < best_positive_sse and fixed_sse <= 1.25 * free_sse)
    exponent_window = bool(0.90 <= z <= 1.10 and 0.90 <= y <= 1.10 and abs(z - y) <= 0.10)
    scaled_gap = sizes[2:] * gaps[2:]
    scaled_chi = chis[2:] / sizes[2:]
    relative_range = lambda values: float((np.max(values) - np.min(values)) / np.mean(values))
    plateau = bool(relative_range(scaled_gap) <= 0.05 and relative_range(scaled_chi) <= 0.05)
    residue_guard = bool(np.all(residues >= 1e-6) and relative_range(residues[2:]) <= 0.35)
    passed = monotone and model_order and exponent_window and plateau and residue_guard
    return {
        "status": "ATOM_Z1_PASS" if passed else "ATOM_Z1_REJECT",
        "classification": {
            "passes": passed,
            "strict_gap_down_chi_up": monotone,
            "fixed_z1_model_order": model_order,
            "exponent_window": exponent_window,
            "scaled_plateau": plateau,
            "residue_guard": residue_guard,
            "z": z,
            "y": y,
            "fixed_z1_heldout_relative_sse": fixed_sse,
            "free_gapless_relative_sse": free_sse,
            "positive_gap_relative_sse": best_positive_sse,
            "positive_gap_z": best_positive_z,
            "positive_gap_limit": best_positive_limit,
            "L8_L12_relative_range_LDelta": relative_range(scaled_gap),
            "L8_L12_relative_range_chi_over_L": relative_range(scaled_chi),
            "L8_L12_relative_range_R_low": relative_range(residues[2:]),
        },
    }


def execute_from_freeze(freeze_path: Path, freeze_hash: str, token: str, output: Path) -> None:
    if token != RUN_TOKEN:
        raise FailClosed("literal blind execution token missing")
    freeze = _load_pinned_json(freeze_path, freeze_hash)
    if freeze.get("status") != "BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM":
        raise FailClosed("runnable blind method freeze is absent")
    _verify_freeze_custody(freeze_path, freeze)
    plan = freeze.get("positive_q_sector_plan")
    if not isinstance(plan, list) or not plan:
        raise FailClosed("frozen positive-q sector plan is absent")
    rows: dict[str, object] = {}
    for item in plan:
        if not isinstance(item, dict):
            raise FailClosed("invalid sector-plan row")
        L, q = item.get("L"), item.get("q")
        if isinstance(L, bool) or isinstance(q, bool) or not isinstance(L, int) or not isinstance(q, int):
            raise FailClosed("sector coordinates must be literal integers")
        key = f"L{L}_q{q}"
        if key in rows:
            raise FailClosed("duplicate sector in frozen plan")
        rows[key] = sector_spectrum(L, q)
    atoms = freeze.get("atom_plan")
    if not isinstance(atoms, list) or not atoms:
        raise FailClosed("frozen complete atom plan is absent")
    atom_classifications: dict[str, object] = {}
    for atom in atoms:
        if not isinstance(atom, dict) or not isinstance(atom.get("atom_id"), str):
            raise FailClosed("invalid frozen atom-plan row")
        atom_id = atom["atom_id"]
        if atom_id in atom_classifications:
            raise FailClosed("duplicate atom ID in frozen plan")
        atom_classifications[atom_id] = classify_atom(atom, rows)
    result = {
        "schema": SCHEMA,
        "role": "blind",
        "status": "BLIND_COMPLETE__READY_FOR_HOSTILE_ADJUDICATION",
        "accumulation_manifest_sha256": freeze["accumulation_manifest_sha256"],
        "pre_target_method_freeze_path": str(freeze_path),
        "pre_target_method_freeze_sha256": freeze_hash,
        "implementation_path": freeze["implementation_path"],
        "implementation_sha256": freeze["implementation_sha256"],
        "rows": rows,
        "atom_classifications": atom_classifications,
    }
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if output.exists():
        raise FailClosed("blind output path already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(payload)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--freeze-sha256", required=True)
    parser.add_argument("--run-token", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        execute_from_freeze(args.freeze, args.freeze_sha256, args.run_token, args.output)
    except (FailClosed, MemoryError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL_CLOSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
