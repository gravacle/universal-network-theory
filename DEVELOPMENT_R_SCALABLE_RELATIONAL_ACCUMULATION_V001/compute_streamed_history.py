#!/usr/bin/env python3
"""Exact-block adaptive-Krylov histories for the enlarged relational parent.

The representation is exact in the fixed-content basis.  Carrier-number
blocks and genesis rows are streamed through bounded batches; Krylov stopping
controls only numerical exponential-action accuracy and never deletes a
physical basis state.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import resource
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
RAW = HERE / "RAW_HISTORY"
PHI = math.pi / 4.0
DWELL = math.pi / 2.0
TARGET_SIZES = (4, 6, 8, 10)
L12_MIN_FREE_SCRATCH = 60 * 2**30
L10_RSS_LIMIT = 4 * 2**30
L10_WALL_LIMIT = 2 * 3600.0
KRYLOV_STORAGE_BYTES = 1_400_000_000


@dataclass(frozen=True)
class Resolution:
    label: str
    checkpoints: tuple[int, ...]
    quadrature_nodes: int
    tolerance: float


COARSE = Resolution("coarse", (12, 18, 24, 32, 48), 16, 2.0e-9)
FINE = Resolution("fine", (16, 24, 32, 48, 64), 24, 5.0e-11)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_words(width: int, weight: int) -> np.ndarray:
    dtype = np.uint32 if width <= 32 else np.uint64
    values = np.empty(math.comb(width, weight), dtype=dtype)
    for index, chosen in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for bit in chosen:
            word |= 1 << bit
        values[index] = word
    return values


def graph(length: int) -> list[tuple[int, int, str]]:
    edges: list[tuple[int, int, str]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length, f"rail_{rail + 1}"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


class Sector:
    def __init__(self, length: int, q: int, edges: list[tuple[int, int, str]]):
        self.length = length
        self.q = q
        self.words = fixed_words(2 * length, q)
        self.lookup = {int(word): index for index, word in enumerate(self.words)}
        self.pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for u, v, _ in edges:
            left = np.flatnonzero(
                (((self.words >> u) & 1) == 1)
                & (((self.words >> v) & 1) == 0)
            ).astype(np.int32)
            mask = type(self.words[0])((1 << u) | (1 << v)) if len(self.words) else 0
            right = np.fromiter(
                (self.lookup[int(self.words[column] ^ mask)] for column in left),
                dtype=np.int32,
                count=len(left),
            )
            self.pairs.append((left, right))

    def h(self, vector: np.ndarray) -> np.ndarray:
        result = np.zeros_like(vector)
        for left, right in self.pairs:
            result[:, left] -= vector[:, right]
            result[:, right] -= vector[:, left]
        return result

    def currents(self, vector: np.ndarray) -> np.ndarray:
        answer = np.empty(len(self.pairs), dtype=float)
        for edge, (left, right) in enumerate(self.pairs):
            answer[edge] = 2.0 * float(np.imag(np.vdot(vector[:, left], vector[:, right])))
        return answer


class ExactBlocks:
    def __init__(self, length: int):
        self.length = length
        self.sites = 2 * length
        self.edges = graph(length)
        self.connector_indices = [i for i, edge in enumerate(self.edges) if edge[2] == "connector"]
        self.incidence = np.zeros((self.sites, len(self.edges)), dtype=np.int8)
        for edge_index, (u, v, _) in enumerate(self.edges):
            self.incidence[u, edge_index] = 1
            self.incidence[v, edge_index] = -1
        self.sectors = [Sector(length, q, self.edges) for q in range(length + 1)]
        self.spent_words = [fixed_words(length, q) for q in range(length + 1)]
        self.spent_lookup = [
            {int(word): index for index, word in enumerate(words)} for words in self.spent_words
        ]
        self.dimension = sum(
            len(self.spent_words[q]) * len(self.sectors[q].words) for q in range(length + 1)
        )
        if self.dimension != math.comb(3 * length, length):
            raise AssertionError("Vandermonde dimension mismatch")
        self.admission_maps = self._admission_maps()

    def _admission_maps(self) -> list[list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]]:
        all_events = []
        for event in range(self.length):
            event_maps = []
            for q in range(self.length):
                source_rows = np.flatnonzero(((self.spent_words[q] >> event) & 1) == 0).astype(np.int32)
                destination_rows = np.fromiter(
                    (self.spent_lookup[q + 1][int(self.spent_words[q][row] | (1 << event))] for row in source_rows),
                    dtype=np.int32,
                    count=len(source_rows),
                )
                source_columns = np.flatnonzero(((self.sectors[q].words >> event) & 1) == 0).astype(np.int32)
                destination_columns = np.fromiter(
                    (self.sectors[q + 1].lookup[int(self.sectors[q].words[column] | (1 << event))]
                     for column in source_columns),
                    dtype=np.int32,
                    count=len(source_columns),
                )
                event_maps.append((source_rows, source_columns, destination_rows, destination_columns))
            all_events.append(event_maps)
        return all_events

    def initial(self) -> list[np.ndarray]:
        blocks = [
            np.zeros((len(self.spent_words[q]), len(self.sectors[q].words)), dtype=np.complex128)
            for q in range(self.length + 1)
        ]
        blocks[0][0, 0] = 1.0
        return blocks

    @staticmethod
    def copy(blocks: list[np.ndarray]) -> list[np.ndarray]:
        return [block.copy() for block in blocks]

    @staticmethod
    def norm(blocks: list[np.ndarray]) -> float:
        return float(sum(np.vdot(block, block).real for block in blocks))

    def sector_weights(self, blocks: list[np.ndarray]) -> np.ndarray:
        return np.array([float(np.vdot(block, block).real) for block in blocks])

    def retained_q(self, blocks: list[np.ndarray]) -> float:
        weights = self.sector_weights(blocks)
        return float(np.dot(np.arange(len(weights), dtype=float), weights))

    def genesis_q(self, blocks: list[np.ndarray]) -> float:
        weights = self.sector_weights(blocks)
        return float(np.dot(self.length - np.arange(len(weights), dtype=float), weights))

    def occupations(self, blocks: list[np.ndarray]) -> np.ndarray:
        answer = np.zeros(self.sites, dtype=float)
        for q, block in enumerate(blocks):
            if q == 0:
                continue
            column_probability = np.sum(np.abs(block) ** 2, axis=0)
            words = self.sectors[q].words
            for site in range(self.sites):
                answer[site] += float(np.sum(column_probability[((words >> site) & 1) == 1]))
        return answer

    def predicates(self, blocks: list[np.ndarray], event: int) -> tuple[float, float, float]:
        allow = blocked = reverse = 0.0
        for q, block in enumerate(blocks):
            spent = self.spent_words[q]
            carriers = self.sectors[q].words
            loaded_rows = np.flatnonzero(((spent >> event) & 1) == 0)
            spent_rows = np.flatnonzero(((spent >> event) & 1) == 1)
            blank_columns = np.flatnonzero(((carriers >> event) & 1) == 0)
            occupied_columns = np.flatnonzero(((carriers >> event) & 1) == 1)
            if len(loaded_rows) and len(blank_columns):
                view = block[np.ix_(loaded_rows, blank_columns)]
                allow += float(np.vdot(view, view).real)
            if len(loaded_rows) and len(occupied_columns):
                view = block[np.ix_(loaded_rows, occupied_columns)]
                blocked += float(np.vdot(view, view).real)
            if len(spent_rows) and len(occupied_columns):
                view = block[np.ix_(spent_rows, occupied_columns)]
                reverse += float(np.vdot(view, view).real)
        return allow, blocked, reverse

    def admit(self, blocks: list[np.ndarray], event: int) -> list[np.ndarray]:
        result = self.copy(blocks)
        cosine = math.cos(PHI)
        sine = math.sin(PHI)
        for q, maps in enumerate(self.admission_maps[event]):
            source_rows, source_columns, destination_rows, destination_columns = maps
            source_index = np.ix_(source_rows, source_columns)
            destination_index = np.ix_(destination_rows, destination_columns)
            left = blocks[q][source_index]
            right = blocks[q + 1][destination_index]
            result[q][source_index] = cosine * left - 1j * sine * right
            result[q + 1][destination_index] = cosine * right - 1j * sine * left
        return result


def tridiagonal_coefficients(
    alphas: list[float], betas: list[float], dimension: int, elapsed: float, norm: float
) -> np.ndarray:
    matrix = np.diag(np.array(alphas[:dimension], dtype=float))
    if dimension > 1:
        off = np.array(betas[: dimension - 1], dtype=float)
        matrix += np.diag(off, 1) + np.diag(off, -1)
    values, vectors = np.linalg.eigh(matrix)
    phased = np.exp(-1j * elapsed * values) * vectors[0, :] * norm
    return np.einsum("ij,j->i", vectors, phased, optimize=False)


def propagate_batch(
    sector: Sector, vector: np.ndarray, resolution: Resolution
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    flat = vector.reshape(-1)
    norm = float(np.linalg.norm(flat))
    if norm <= 1.0e-30 or sector.q == 0 or len(sector.words) == 1:
        return vector.copy(), np.zeros(len(sector.pairs)), {
            "steps": 0,
            "converged": True,
            "exp_difference": 0.0,
            "residual_indicator": 0.0,
        }

    maximum = min(max(resolution.checkpoints), flat.size)
    basis = np.empty((maximum, flat.size), dtype=np.complex128)
    basis[0] = flat / norm
    alphas: list[float] = []
    betas: list[float] = []
    boundary_betas: list[float] = []
    previous = None
    selected_state = None
    selected_coefficients = None
    selected_dimension = 0
    selected_difference = math.inf
    selected_residual = math.inf
    converged = False

    for step in range(maximum):
        work = sector.h(basis[step].reshape(vector.shape)).reshape(-1)
        if step:
            work -= betas[step - 1] * basis[step - 1]
        alpha = float(np.vdot(basis[step], work).real)
        work -= alpha * basis[step]
        # A bounded local cleanup suppresses roundoff in the three-term
        # recurrence without changing the exact represented subspace.
        for prior in range(max(0, step - 2), step + 1):
            overlap = np.vdot(basis[prior], work)
            work -= overlap * basis[prior]
        beta = float(np.linalg.norm(work))
        alphas.append(alpha)
        boundary_betas.append(beta)
        dimension = step + 1
        if dimension in resolution.checkpoints or dimension == maximum or beta <= 1.0e-14:
            coefficients = tridiagonal_coefficients(alphas, betas, dimension, DWELL, norm)
            candidate = np.einsum(
                "i,ij->j", coefficients, basis[:dimension], optimize=False
            )
            difference = math.inf if previous is None else float(np.linalg.norm(candidate - previous))
            residual = beta * abs(complex(coefficients[-1]))
            selected_state = candidate
            selected_coefficients = coefficients
            selected_dimension = dimension
            selected_difference = difference
            selected_residual = residual
            if previous is not None and difference <= resolution.tolerance and residual <= resolution.tolerance:
                converged = True
                break
            previous = candidate
        if beta <= 1.0e-14:
            converged = True
            break
        if dimension < maximum:
            betas.append(beta)
            basis[dimension] = work / beta

    if selected_state is None or selected_coefficients is None:
        raise AssertionError("Krylov selection failed")
    if not converged and flat.size <= selected_dimension:
        converged = True

    nodes, weights = np.polynomial.legendre.leggauss(resolution.quadrature_nodes)
    integrated = np.zeros(len(sector.pairs), dtype=float)
    for node, weight in zip(nodes, weights):
        elapsed = 0.5 * DWELL * (float(node) + 1.0)
        coefficients = tridiagonal_coefficients(
            alphas, betas, selected_dimension, elapsed, norm
        )
        sample = np.einsum(
            "i,ij->j", coefficients, basis[:selected_dimension], optimize=False
        ).reshape(vector.shape)
        integrated += float(weight) * sector.currents(sample)
    integrated *= 0.5 * DWELL
    return selected_state.reshape(vector.shape), integrated, {
        "steps": selected_dimension,
        "converged": converged,
        "exp_difference": selected_difference,
        "residual_indicator": selected_residual,
    }


def route_inplace(
    parent: ExactBlocks, blocks: list[np.ndarray], resolution: Resolution
) -> tuple[np.ndarray, dict[str, object]]:
    total_current = np.zeros(len(parent.edges), dtype=float)
    maximum_steps = 0
    maximum_difference = 0.0
    maximum_residual = 0.0
    converged = True
    batches = 0
    for q, block in enumerate(blocks):
        columns = block.shape[1]
        maximum = max(resolution.checkpoints)
        rows_per_batch = max(1, int(KRYLOV_STORAGE_BYTES // (maximum * columns * 16)))
        rows_per_batch = min(rows_per_batch, block.shape[0])
        for lower in range(0, block.shape[0], rows_per_batch):
            upper = min(block.shape[0], lower + rows_per_batch)
            evolved, current, record = propagate_batch(parent.sectors[q], block[lower:upper], resolution)
            block[lower:upper] = evolved
            total_current += current
            maximum_steps = max(maximum_steps, int(record["steps"]))
            if math.isfinite(float(record["exp_difference"])):
                maximum_difference = max(maximum_difference, float(record["exp_difference"]))
            maximum_residual = max(maximum_residual, float(record["residual_indicator"]))
            converged = converged and bool(record["converged"])
            batches += 1
    return total_current, {
        "converged": converged,
        "batches": batches,
        "maximum_krylov_steps": maximum_steps,
        "maximum_exp_difference": maximum_difference,
        "maximum_residual_indicator": maximum_residual,
        "quadrature_nodes": resolution.quadrature_nodes,
    }


def run_history(length: int, resolution: Resolution) -> dict[str, object]:
    parent = ExactBlocks(length)
    state = parent.initial()
    rows = []
    for event in range(length):
        before = state
        allow, blocked, reverse = parent.predicates(before, event)
        q_before = parent.retained_q(before)
        g_before = parent.genesis_q(before)
        occupation_before = parent.occupations(before)
        admitted = parent.admit(before, event)
        q_admitted = parent.retained_q(admitted)
        g_admitted = parent.genesis_q(admitted)
        occupation_admitted = parent.occupations(admitted)
        write = q_admitted - q_before

        actual_current, actual_solver = route_inplace(parent, admitted, resolution)
        null_current, null_solver = route_inplace(parent, before, resolution)
        occupation_after = parent.occupations(admitted)
        q_after = parent.retained_q(admitted)
        delta_current = actual_current - null_current
        transport_residual = occupation_after - occupation_admitted + parent.incidence @ actual_current
        rows.append({
            "event": event + 1,
            "cursor_vertex": event,
            "allow_probability": allow,
            "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": 0.0,
            "W_n": write,
            "expected_W_from_allow": (math.sin(PHI) ** 2) * allow,
            "q_retained_before": q_before,
            "q_retained_after_admission": q_admitted,
            "q_retained_after_transport": q_after,
            "q_genesis_before": g_before,
            "q_genesis_after": parent.genesis_q(admitted),
            "bandwidth_after": g_admitted,
            "lineage_sealed_after": length - g_admitted,
            "sector_weights": parent.sector_weights(admitted).tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta_current[parent.connector_indices]))),
            "connector_delta_signed": float(np.sum(delta_current[parent.connector_indices])),
            "admission_total_content_residual": (q_admitted - q_before) + (g_admitted - g_before),
            "admission_bandwidth_residual": (g_admitted - g_before) + write,
            "target_owner_residual": (occupation_admitted[event] - occupation_before[event]) - write,
            "transport_node_residual_l1": float(np.sum(np.abs(transport_residual))),
            "transport_node_residual_linf": float(np.max(np.abs(transport_residual))),
            "transport_number_drift": abs(q_after - q_admitted),
            "transport_genesis_drift": abs(parent.genesis_q(admitted) - g_admitted),
            "actual_norm_error": abs(parent.norm(admitted) - 1.0),
            "null_norm_error": abs(parent.norm(before) - 1.0),
            "actual_solver": actual_solver,
            "null_solver": null_solver,
        })
        state = admitted
    return {
        "rows": rows,
        "final_state": state,
        "dimension": parent.dimension,
        "edges": len(parent.edges),
    }


def shortest_interval(weights: np.ndarray) -> tuple[int, int, float]:
    candidates = []
    for lower in range(len(weights)):
        mass = 0.0
        for upper in range(lower, len(weights)):
            mass += float(weights[upper])
            if mass + 1.0e-15 >= 0.99:
                candidates.append((upper - lower, -mass, lower, upper))
                break
    if not candidates:
        raise AssertionError("no 99 percent interval")
    _, negative_mass, lower, upper = min(candidates)
    return lower, upper, -negative_mass


def summarize(length: int, coarse: dict[str, object], fine: dict[str, object]) -> dict[str, object]:
    keys = ("W_n", "allow_probability", "blocked_probability", "connector_delta_l1", "connector_delta_signed")
    observable_error = max(
        abs(float(left[key]) - float(right[key]))
        for left, right in zip(coarse["rows"], fine["rows"])
        for key in keys
    )
    sector_error = max(
        float(np.max(np.abs(np.array(left["sector_weights"]) - np.array(right["sector_weights"]))))
        for left, right in zip(coarse["rows"], fine["rows"])
    )
    disagreement = max(observable_error, sector_error)
    epsilon = max(1.0e-11, 50.0 * disagreement)
    late = fine["rows"][math.ceil(length / 2) - 1:]
    pbar = np.mean(np.array([row["sector_weights"] for row in late]), axis=0)
    lower, upper, mass = shortest_interval(pbar)
    sector = {
        "late_events": [row["event"] for row in late],
        "q_lower": lower,
        "q_upper": upper,
        "enclosed_mass": mass,
        "discarded_mass": 1.0 - mass,
        "density_interval": [
            max(0.0, (lower - 0.5) / (2.0 * length)),
            min(1.0, (upper + 0.5) / (2.0 * length)),
        ],
    }
    writes = np.array([float(row["W_n"]) for row in fine["rows"]])
    connectors = np.array([float(row["connector_delta_l1"]) for row in fine["rows"]])
    admission = 2.0 * writes
    connector_ratio = connectors / connectors[0]
    routed = np.minimum(admission, connector_ratio)
    max_accounting = max(
        abs(float(row[key]))
        for row in fine["rows"]
        for key in ("admission_total_content_residual", "admission_bandwidth_residual", "target_owner_residual")
    )
    all_solvers = [row[key] for row in fine["rows"] for key in ("actual_solver", "null_solver")]
    resolved = (
        all(bool(record["converged"]) for record in all_solvers)
        and max_accounting <= 1.0e-10
        and min(writes) >= -epsilon
        and max(float(row["reverse_support_probability"]) for row in fine["rows"]) <= 1.0e-11
        and max(float(row["transport_node_residual_l1"]) for row in fine["rows"]) <= max(1.0e-9, 100.0 * epsilon)
        and max(float(row["actual_norm_error"]) for row in fine["rows"]) <= 1.0e-10
        and max(float(row["transport_number_drift"]) for row in fine["rows"]) <= 1.0e-10
        and max(float(row["blocked_probability"]) for row in fine["rows"]) > 1.0e-6
    )
    return {
        "classification": "RESOLVED_RELATIONAL_HISTORY_L" if resolved else "UNRESOLVED_RELATIONAL_HISTORY_L",
        "resolved": resolved,
        "coarse_fine": {
            "observable_linf": observable_error,
            "sector_weight_linf": sector_error,
            "maximum_disagreement": disagreement,
        },
        "epsilon": epsilon,
        "admission_acceptance": admission.tolist(),
        "connector_ratio": connector_ratio.tolist(),
        "routed_acceptance": routed.tolist(),
        "sector": sector,
    }


def worker(length: int, output: Path) -> None:
    if length == 12:
        free = shutil.disk_usage(HERE).free
        if free < L12_MIN_FREE_SCRATCH:
            raise RuntimeError(
                f"L12 scratch guard: free={free}, required={L12_MIN_FREE_SCRATCH}; history not started"
            )
        raise RuntimeError("L12 streamed memmap stage is not authorized before the L4-L10 gate")
    if length not in TARGET_SIZES:
        raise ValueError(f"supported target sizes: {TARGET_SIZES}")
    started = time.perf_counter()
    coarse = run_history(length, COARSE)
    fine = run_history(length, FINE)
    comparison = summarize(length, coarse, fine)
    result = {
        "schema": "SCALABLE_RELATIONAL_STREAMED_HISTORY_ROW_V001",
        "L": length,
        "dimension": fine["dimension"],
        "events": length,
        "edges": fine["edges"],
        "representation": "EXACT_SHARP_Q_BLOCKS_STREAMED_BY_GENESIS_ROW_BATCH",
        "coarse_method": COARSE.__dict__,
        "fine_method": FINE.__dict__,
        "rows": fine["rows"],
        "comparison": comparison,
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "protocol_sha256": sha256(HERE / "PROTOCOL.md"),
        "implementation_sha256": sha256(Path(__file__)),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "claim_boundary": "FINITE_RELATIONAL_HISTORY_ROW_ONLY",
    }
    if length == 10:
        result["resource_guards"] = {
            "rss_limit_bytes": L10_RSS_LIMIT,
            "wall_limit_seconds": L10_WALL_LIMIT,
            "rss_pass": result["peak_rss_bytes"] <= L10_RSS_LIMIT,
            "wall_pass": result["wall_seconds"] <= L10_WALL_LIMIT,
        }
        if not all((result["resource_guards"]["rss_pass"], result["resource_guards"]["wall_pass"])):
            comparison["resolved"] = False
            comparison["classification"] = "EXACT_RELATIONAL_LINEAGE_SCALING_OBSTRUCTION"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(comparison["classification"])
    print(f"L={length} D={fine['dimension']} wall={result['wall_seconds']:.3f}s rss={result['peak_rss_bytes']}")
    print(f"coarse/fine={comparison['coarse_fine']['maximum_disagreement']:.3e}")
    print(f"sector={comparison['sector']['density_interval']}")
    if not comparison["resolved"]:
        raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or RAW / f"STREAMED_HISTORY_L{args.worker}.json"
    worker(args.worker, output)


if __name__ == "__main__":
    main()
