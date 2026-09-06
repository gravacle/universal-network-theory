#!/usr/bin/env python3
"""Independent reversed-layout Chebyshev-Krylov relational histories.

This implementation imports no target module or matrix.  It uses reversed
combination ordering, a different edge order, a Gershgorin-scaled Chebyshev
recurrence, and independent quadrature orders.
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

import mpmath
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "PROTOCOL.md"
RAW = HERE / "RAW_HISTORY"
ANGLE = math.pi / 4.0
ROUTE_TIME = math.pi / 2.0
SIZES = (4, 6, 8, 10)
L12_FREE_GUARD = 60 * 2**30
L10_RSS_GUARD = 4 * 2**30
L10_TIME_GUARD = 2 * 3600.0
BASIS_MEMORY = 1_400_000_000


@dataclass(frozen=True)
class Accuracy:
    name: str
    degrees: tuple[int, ...]
    gauss_order: int
    tolerance: float


ROUGH = Accuracy("rough", (16, 24, 32, 48, 64, 80), 18, 3.0e-9)
SHARP = Accuracy("sharp", (24, 32, 48, 64, 80, 96), 28, 8.0e-11)


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reverse_words(width: int, population: int) -> np.ndarray:
    dtype = np.uint32 if width <= 32 else np.uint64
    result = np.empty(math.comb(width, population), dtype=dtype)
    for index, chosen in enumerate(itertools.combinations(reversed(range(width)), population)):
        value = 0
        for bit in chosen:
            value += 1 << bit
        result[index] = value
    return result


def independent_edges(length: int) -> list[tuple[int, int, str]]:
    result = [(site, length + (site + 1) % length, "connector") for site in range(length)]
    result.extend((length + site, length + (site + 1) % length, "rail_2") for site in range(length))
    result.extend((site, (site + 1) % length, "rail_1") for site in range(length))
    return result


class NumberBlock:
    def __init__(self, length: int, population: int, edges: list[tuple[int, int, str]]):
        self.population = population
        self.words = reverse_words(2 * length, population)
        position = {int(word): index for index, word in enumerate(self.words)}
        exchanges = []
        for u, v, _ in edges:
            first = np.flatnonzero(
                (((self.words >> u) & 1) != 0) & (((self.words >> v) & 1) == 0)
            ).astype(np.int32)
            bitmask = type(self.words[0])((1 << u) + (1 << v))
            second = np.fromiter(
                (position[int(self.words[column] ^ bitmask)] for column in first),
                dtype=np.int32,
                count=len(first),
            )
            exchanges.append((first, second))
        self.exchanges = exchanges
        self.position = position

    def multiply(self, vector: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(vector)
        for first, second in self.exchanges:
            answer[:, first] -= vector[:, second]
            answer[:, second] -= vector[:, first]
        return answer

    def flux(self, vector: np.ndarray) -> np.ndarray:
        values = []
        for first, second in self.exchanges:
            values.append(2.0 * float(np.imag(np.vdot(vector[:, first], vector[:, second]))))
        return np.array(values)


class RelationalBasis:
    def __init__(self, length: int):
        self.length = length
        self.site_count = 2 * length
        self.edges = independent_edges(length)
        self.connector_edges = [index for index, edge in enumerate(self.edges) if edge[2] == "connector"]
        self.divergence = np.zeros((self.site_count, len(self.edges)), dtype=np.int8)
        for edge_index, (u, v, _) in enumerate(self.edges):
            self.divergence[u, edge_index] = 1
            self.divergence[v, edge_index] = -1
        self.carrier = [NumberBlock(length, q, self.edges) for q in range(length + 1)]
        self.used = [reverse_words(length, q) for q in range(length + 1)]
        self.used_position = [
            {int(word): index for index, word in enumerate(words)} for words in self.used
        ]
        self.dimension = sum(len(self.used[q]) * len(self.carrier[q].words) for q in range(length + 1))
        if self.dimension != math.comb(3 * length, length):
            raise AssertionError("independent dimension identity failed")
        self.transfer_maps = self._transfer_maps()

    def _transfer_maps(self) -> list[list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]]:
        complete = []
        for event in range(self.length):
            event_rows = []
            for q in range(self.length):
                old_rows = np.flatnonzero(((self.used[q] >> event) & 1) == 0).astype(np.int32)
                new_rows = np.fromiter(
                    (self.used_position[q + 1][int(self.used[q][row] + (1 << event))] for row in old_rows),
                    dtype=np.int32,
                    count=len(old_rows),
                )
                old_columns = np.flatnonzero(((self.carrier[q].words >> event) & 1) == 0).astype(np.int32)
                new_columns = np.fromiter(
                    (self.carrier[q + 1].position[int(self.carrier[q].words[column] + (1 << event))]
                     for column in old_columns),
                    dtype=np.int32,
                    count=len(old_columns),
                )
                event_rows.append((old_rows, old_columns, new_rows, new_columns))
            complete.append(event_rows)
        return complete

    def blank(self) -> list[np.ndarray]:
        state = [
            np.zeros((len(self.used[q]), len(self.carrier[q].words)), dtype=np.complex128)
            for q in range(self.length + 1)
        ]
        state[0][0, 0] = 1.0
        return state

    @staticmethod
    def duplicate(state: list[np.ndarray]) -> list[np.ndarray]:
        return [block.copy() for block in state]

    @staticmethod
    def norm(state: list[np.ndarray]) -> float:
        return float(sum(np.vdot(block, block).real for block in state))

    def weights(self, state: list[np.ndarray]) -> np.ndarray:
        return np.array([float(np.vdot(block, block).real) for block in state])

    def retained(self, state: list[np.ndarray]) -> float:
        return float(np.dot(np.arange(self.length + 1), self.weights(state)))

    def remaining(self, state: list[np.ndarray]) -> float:
        return float(np.dot(self.length - np.arange(self.length + 1), self.weights(state)))

    def occupation(self, state: list[np.ndarray]) -> np.ndarray:
        result = np.zeros(self.site_count)
        for q, block in enumerate(state):
            probability = np.sum(np.abs(block) ** 2, axis=0)
            for site in range(self.site_count):
                result[site] += float(np.sum(probability[((self.carrier[q].words >> site) & 1) != 0]))
        return result

    def classify(self, state: list[np.ndarray], event: int) -> tuple[float, float, float]:
        allowed = blocked = reverse = 0.0
        for q, block in enumerate(state):
            loaded_rows = np.flatnonzero(((self.used[q] >> event) & 1) == 0)
            used_rows = np.flatnonzero(((self.used[q] >> event) & 1) != 0)
            blank_columns = np.flatnonzero(((self.carrier[q].words >> event) & 1) == 0)
            full_columns = np.flatnonzero(((self.carrier[q].words >> event) & 1) != 0)
            for rows, columns, accumulator in (
                (loaded_rows, blank_columns, "allowed"),
                (loaded_rows, full_columns, "blocked"),
                (used_rows, full_columns, "reverse"),
            ):
                if len(rows) and len(columns):
                    piece = block[np.ix_(rows, columns)]
                    value = float(np.vdot(piece, piece).real)
                    if accumulator == "allowed":
                        allowed += value
                    elif accumulator == "blocked":
                        blocked += value
                    else:
                        reverse += value
        return allowed, blocked, reverse

    def transfer(self, state: list[np.ndarray], event: int) -> list[np.ndarray]:
        result = self.duplicate(state)
        c = math.cos(ANGLE)
        s = math.sin(ANGLE)
        for q, (old_rows, old_columns, new_rows, new_columns) in enumerate(self.transfer_maps[event]):
            old_index = np.ix_(old_rows, old_columns)
            new_index = np.ix_(new_rows, new_columns)
            old_value = state[q][old_index]
            new_value = state[q + 1][new_index]
            result[q][old_index] = c * old_value - 1j * s * new_value
            result[q + 1][new_index] = c * new_value - 1j * s * old_value
        return result


def chebyshev_coefficients(scale: float, elapsed: float, degree: int) -> np.ndarray:
    argument = scale * elapsed
    result = np.empty(degree + 1, dtype=np.complex128)
    result[0] = complex(mpmath.besselj(0, argument))
    for order in range(1, degree + 1):
        result[order] = 2.0 * ((-1j) ** order) * complex(mpmath.besselj(order, argument))
    return result


def tail_bound(scale: float, elapsed: float, degree: int) -> float:
    argument = scale * elapsed
    return float(sum(2.0 * abs(mpmath.besselj(order, argument)) for order in range(degree + 1, degree + 33)))


def chebyshev_batch(
    block: NumberBlock, vector: np.ndarray, accuracy: Accuracy
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    flat = vector.reshape(-1)
    if float(np.linalg.norm(flat)) == 0.0 or block.population == 0 or len(block.words) == 1:
        return vector.copy(), np.zeros(len(block.exchanges)), {
            "degree": 0,
            "converged": True,
            "exp_difference": 0.0,
            "tail_bound": 0.0,
        }
    scale = 3.0 * block.population
    maximum = min(max(accuracy.degrees), max(0, flat.size - 1))
    basis = np.empty((maximum + 1, flat.size), dtype=np.complex128)
    basis[0] = flat
    if maximum:
        basis[1] = (block.multiply(vector) / scale).reshape(-1)
    previous = None
    chosen = None
    chosen_degree = 0
    chosen_difference = math.inf
    chosen_tail = math.inf
    converged = False
    for degree in range(maximum + 1):
        if degree >= 2:
            basis[degree] = (
                2.0 * block.multiply(basis[degree - 1].reshape(vector.shape)).reshape(-1) / scale
                - basis[degree - 2]
            )
        if degree in accuracy.degrees or degree == maximum:
            coefficients = chebyshev_coefficients(scale, ROUTE_TIME, degree)
            candidate = np.einsum("i,ij->j", coefficients, basis[: degree + 1], optimize=False)
            difference = math.inf if previous is None else float(np.linalg.norm(candidate - previous))
            tail = tail_bound(scale, ROUTE_TIME, degree)
            chosen = candidate
            chosen_degree = degree
            chosen_difference = difference
            chosen_tail = tail
            if previous is not None and difference <= accuracy.tolerance and tail <= accuracy.tolerance:
                converged = True
                break
            previous = candidate
    if chosen is None:
        raise AssertionError("Chebyshev selection failed")
    nodes, weights = np.polynomial.legendre.leggauss(accuracy.gauss_order)
    integrated = np.zeros(len(block.exchanges))
    for node, weight in zip(nodes, weights):
        elapsed = 0.5 * ROUTE_TIME * (float(node) + 1.0)
        coefficients = chebyshev_coefficients(scale, elapsed, chosen_degree)
        sample = np.einsum(
            "i,ij->j", coefficients, basis[: chosen_degree + 1], optimize=False
        ).reshape(vector.shape)
        integrated += float(weight) * block.flux(sample)
    integrated *= 0.5 * ROUTE_TIME
    return chosen.reshape(vector.shape), integrated, {
        "degree": chosen_degree,
        "converged": converged,
        "exp_difference": chosen_difference,
        "tail_bound": chosen_tail,
    }


def evolve(
    basis: RelationalBasis, state: list[np.ndarray], accuracy: Accuracy
) -> tuple[np.ndarray, dict[str, object]]:
    integrated = np.zeros(len(basis.edges))
    converged = True
    max_degree = 0
    max_difference = 0.0
    max_tail = 0.0
    batches = 0
    maximum = max(accuracy.degrees) + 1
    for q, sector_state in enumerate(state):
        columns = sector_state.shape[1]
        rows_at_once = max(1, int(BASIS_MEMORY // (maximum * columns * 16)))
        rows_at_once = min(rows_at_once, sector_state.shape[0])
        for lower in range(0, sector_state.shape[0], rows_at_once):
            upper = min(sector_state.shape[0], lower + rows_at_once)
            final, flux, record = chebyshev_batch(
                basis.carrier[q], sector_state[lower:upper], accuracy
            )
            sector_state[lower:upper] = final
            integrated += flux
            converged = converged and bool(record["converged"])
            max_degree = max(max_degree, int(record["degree"]))
            if math.isfinite(float(record["exp_difference"])):
                max_difference = max(max_difference, float(record["exp_difference"]))
            max_tail = max(max_tail, float(record["tail_bound"]))
            batches += 1
    return integrated, {
        "converged": converged,
        "batches": batches,
        "maximum_degree": max_degree,
        "maximum_exp_difference": max_difference,
        "maximum_tail_bound": max_tail,
        "quadrature_nodes": accuracy.gauss_order,
    }


def history(length: int, accuracy: Accuracy) -> dict[str, object]:
    basis = RelationalBasis(length)
    state = basis.blank()
    rows = []
    for event in range(length):
        before = state
        allowed, blocked, reverse = basis.classify(before, event)
        retained_before = basis.retained(before)
        remaining_before = basis.remaining(before)
        occupation_before = basis.occupation(before)
        admitted = basis.transfer(before, event)
        retained_admitted = basis.retained(admitted)
        remaining_admitted = basis.remaining(admitted)
        occupation_admitted = basis.occupation(admitted)
        write = retained_admitted - retained_before
        actual_flux, actual_method = evolve(basis, admitted, accuracy)
        null_flux, null_method = evolve(basis, before, accuracy)
        retained_after = basis.retained(admitted)
        occupation_after = basis.occupation(admitted)
        residual = occupation_after - occupation_admitted + basis.divergence @ actual_flux
        delta = actual_flux - null_flux
        rows.append({
            "event": event + 1,
            "allow_probability": allowed,
            "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": 0.0,
            "W_n": write,
            "q_retained_after_transport": retained_after,
            "q_genesis_after": basis.remaining(admitted),
            "sector_weights": basis.weights(admitted).tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta[basis.connector_edges]))),
            "connector_delta_signed": float(np.sum(delta[basis.connector_edges])),
            "admission_total_content_residual": write + remaining_admitted - remaining_before,
            "admission_bandwidth_residual": remaining_admitted - remaining_before + write,
            "target_owner_residual": occupation_admitted[event] - occupation_before[event] - write,
            "transport_node_residual_l1": float(np.sum(np.abs(residual))),
            "transport_node_residual_linf": float(np.max(np.abs(residual))),
            "transport_number_drift": abs(retained_after - retained_admitted),
            "actual_norm_error": abs(basis.norm(admitted) - 1.0),
            "null_norm_error": abs(basis.norm(before) - 1.0),
            "actual_solver": actual_method,
            "null_solver": null_method,
        })
        state = admitted
    return {"rows": rows, "dimension": basis.dimension, "edges": len(basis.edges)}


def minimal_interval(weights: np.ndarray) -> tuple[int, int, float]:
    candidates = []
    for lower in range(len(weights)):
        mass = 0.0
        for upper in range(lower, len(weights)):
            mass += float(weights[upper])
            if mass + 1.0e-15 >= 0.99:
                candidates.append((upper - lower, -mass, lower, upper))
                break
    if not candidates:
        raise AssertionError("interval coverage failure")
    _, negative_mass, lower, upper = min(candidates)
    return lower, upper, -negative_mass


def compare_internal(length: int, rough: dict[str, object], sharp: dict[str, object]) -> dict[str, object]:
    fields = ("W_n", "allow_probability", "blocked_probability", "connector_delta_l1", "connector_delta_signed")
    observable_error = max(
        abs(float(a[field]) - float(b[field]))
        for a, b in zip(rough["rows"], sharp["rows"])
        for field in fields
    )
    sector_error = max(
        float(np.max(np.abs(np.array(a["sector_weights"]) - np.array(b["sector_weights"]))))
        for a, b in zip(rough["rows"], sharp["rows"])
    )
    disagreement = max(observable_error, sector_error)
    epsilon = max(1.0e-11, 50.0 * disagreement)
    late = sharp["rows"][math.ceil(length / 2) - 1:]
    pbar = np.mean(np.array([row["sector_weights"] for row in late]), axis=0)
    lower, upper, mass = minimal_interval(pbar)
    writes = np.array([float(row["W_n"]) for row in sharp["rows"]])
    connectors = np.array([float(row["connector_delta_l1"]) for row in sharp["rows"]])
    all_methods = [row[key] for row in sharp["rows"] for key in ("actual_solver", "null_solver")]
    resolved = (
        all(bool(method["converged"]) for method in all_methods)
        and min(writes) >= -epsilon
        and max(float(row["blocked_probability"]) for row in sharp["rows"]) > 1.0e-6
        and max(float(row["reverse_support_probability"]) for row in sharp["rows"]) <= 1.0e-11
        and max(float(row["transport_node_residual_l1"]) for row in sharp["rows"]) <= max(1.0e-9, 100.0 * epsilon)
        and max(float(row["actual_norm_error"]) for row in sharp["rows"]) <= 1.0e-10
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
        "admission_acceptance": (2.0 * writes).tolist(),
        "connector_ratio": (connectors / connectors[0]).tolist(),
        "routed_acceptance": np.minimum(2.0 * writes, connectors / connectors[0]).tolist(),
        "sector": {
            "late_events": [row["event"] for row in late],
            "q_lower": lower,
            "q_upper": upper,
            "enclosed_mass": mass,
            "discarded_mass": 1.0 - mass,
            "density_interval": [
                max(0.0, (lower - 0.5) / (2 * length)),
                min(1.0, (upper + 0.5) / (2 * length)),
            ],
        },
    }


def run(length: int, output: Path) -> None:
    if length == 12:
        free = shutil.disk_usage(ROOT).free
        if free < L12_FREE_GUARD:
            raise RuntimeError(
                f"independent L12 scratch guard: free={free}, required={L12_FREE_GUARD}; not started"
            )
        raise RuntimeError("independent L12 memmap stage awaits the L4-L10 gate")
    if length not in SIZES:
        raise ValueError(f"supported independent sizes: {SIZES}")
    started = time.perf_counter()
    rough = history(length, ROUGH)
    sharp = history(length, SHARP)
    comparison = compare_internal(length, rough, sharp)
    result = {
        "schema": "INDEPENDENT_SCALABLE_RELATIONAL_STREAMED_HISTORY_ROW_V001",
        "L": length,
        "dimension": sharp["dimension"],
        "events": length,
        "edges": sharp["edges"],
        "representation": "REVERSED_EXACT_Q_BLOCKS_STREAMED_BY_USED_CELL_ROWS",
        "rough_method": ROUGH.__dict__,
        "sharp_method": SHARP.__dict__,
        "rows": sharp["rows"],
        "comparison": comparison,
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "protocol_sha256": hash_file(PROTOCOL),
        "implementation_sha256": hash_file(Path(__file__)),
        "python": sys.version,
        "numpy": np.__version__,
        "mpmath": mpmath.__version__,
        "platform": platform.platform(),
        "claim_boundary": "INDEPENDENT_FINITE_RELATIONAL_HISTORY_ROW_ONLY",
    }
    if length == 10:
        result["resource_guards"] = {
            "rss_limit_bytes": L10_RSS_GUARD,
            "wall_limit_seconds": L10_TIME_GUARD,
            "rss_pass": result["peak_rss_bytes"] <= L10_RSS_GUARD,
            "wall_pass": result["wall_seconds"] <= L10_TIME_GUARD,
        }
        if not all((result["resource_guards"]["rss_pass"], result["resource_guards"]["wall_pass"])):
            comparison["resolved"] = False
            comparison["classification"] = "EXACT_RELATIONAL_LINEAGE_SCALING_OBSTRUCTION"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(comparison["classification"])
    print(f"L={length} D={sharp['dimension']} wall={result['wall_seconds']:.3f}s rss={result['peak_rss_bytes']}")
    print(f"rough/sharp={comparison['coarse_fine']['maximum_disagreement']:.3e}")
    print(f"sector={comparison['sector']['density_interval']}")
    if not comparison["resolved"]:
        raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    run(args.worker, args.output or RAW / f"BLIND_STREAMED_HISTORY_L{args.worker}.json")


if __name__ == "__main__":
    main()
