#!/usr/bin/env python3
"""Clean-room reversed-layout Chebyshev prefix-lineage histories."""

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
from functools import lru_cache
from pathlib import Path

import mpmath
import numpy as np


HERE = Path(__file__).resolve().parent
ANGLE = math.pi / 4.0
ROUTE_TIME = math.pi / 2.0
CONTROL_SIZES = (4, 6, 8)
CONTROL_GATE = HERE / "CONTROL_GATE.json"
SEALED_L10_GATE = HERE / "SEALED_L10_GATE.json"
L12_SCRATCH_GATE = 20 * 2**30
L12_RSS_LIMIT = 16 * 2**30
L12_WALL_LIMIT = 6 * 3600.0
KRYLOV_BYTES = 1_400_000_000
TERMINAL_WINDOW_BYTES = 512 * 2**20
LINEAGE_DOMAIN = b"R-PREFIX-LINEAGE-V001\0"


@dataclass(frozen=True)
class Accuracy:
    label: str
    checkpoints: tuple[int, ...]
    gauss_order: int
    tolerance: float


ROUGH = Accuracy("rough", (16, 24, 32, 48, 64, 80), 18, 3.0e-9)
SHARP = Accuracy("sharp", (24, 32, 48, 64, 80, 96), 28, 8.0e-11)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reverse_masks(width: int, weight: int) -> np.ndarray:
    dtype = np.uint32 if width <= 32 else np.uint64
    answer = np.empty(math.comb(width, weight), dtype=dtype)
    for index, subset in enumerate(itertools.combinations(reversed(range(width)), weight)):
        mask = 0
        for bit in subset:
            mask |= 1 << bit
        answer[index] = mask
    return answer


def hostile_edges(length: int) -> list[tuple[int, int, str]]:
    answer: list[tuple[int, int, str]] = []
    for site in reversed(range(length)):
        answer.append((length + site, length + (site + 1) % length, "rail_2"))
    for site in reversed(range(length)):
        answer.append((site, length + (site + 1) % length, "connector"))
    for site in reversed(range(length)):
        answer.append((site, (site + 1) % length, "rail_1"))
    return answer


class CarrierBlock:
    def __init__(self, length: int, q: int, edge_list: list[tuple[int, int, str]]):
        self.q = q
        self.words = reverse_masks(2 * length, q)
        self.position = {int(word): index for index, word in enumerate(self.words)}
        self.exchanges: list[tuple[np.ndarray, np.ndarray]] = []
        dtype = self.words.dtype.type
        for u, v, _ in edge_list:
            source = np.flatnonzero(
                (((self.words >> u) & 1) != 0) & (((self.words >> v) & 1) == 0)
            ).astype(np.int32)
            toggle = dtype((1 << u) | (1 << v))
            target = np.fromiter(
                (self.position[int(self.words[index] ^ toggle)] for index in source),
                dtype=np.int32,
                count=len(source),
            )
            self.exchanges.append((source, target))

    def multiply(self, vector: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(vector)
        for source, target in self.exchanges:
            answer[:, source] -= vector[:, target]
            answer[:, target] -= vector[:, source]
        return answer

    def currents(self, vector: np.ndarray) -> np.ndarray:
        answer = np.zeros(len(self.exchanges))
        for edge, (source, target) in enumerate(self.exchanges):
            answer[edge] = 2.0 * float(np.imag(np.vdot(vector[:, source], vector[:, target])))
        return answer


@dataclass
class PrefixState:
    prefix: int
    blocks: list[np.ndarray]


class PrefixBasis:
    def __init__(self, length: int):
        self.length = length
        self.sites = 2 * length
        self.edges = hostile_edges(length)
        self.connectors = np.array(
            [index for index, edge in enumerate(self.edges) if edge[2] == "connector"],
            dtype=np.int32,
        )
        self.incidence = np.zeros((self.sites, len(self.edges)), dtype=np.int8)
        for index, (u, v, _) in enumerate(self.edges):
            self.incidence[u, index] = 1
            self.incidence[v, index] = -1
        self.carriers = [CarrierBlock(length, q, self.edges) for q in range(length + 1)]
        self._lineages: dict[tuple[int, int], np.ndarray] = {}
        self._positions: dict[tuple[int, int], dict[int, int]] = {}

    def lineages(self, prefix: int, q: int) -> np.ndarray:
        key = (prefix, q)
        if key not in self._lineages:
            words = reverse_masks(prefix, q)
            if len(set(map(int, words))) != len(words):
                raise AssertionError("canonical lineage masks are not injective")
            if any(int(word) >> prefix for word in words):
                raise AssertionError("future lineage bit populated")
            self._lineages[key] = words
        return self._lineages[key]

    def lineage_positions(self, prefix: int, q: int) -> dict[int, int]:
        key = (prefix, q)
        if key not in self._positions:
            self._positions[key] = {
                int(word): index for index, word in enumerate(self.lineages(prefix, q))
            }
        return self._positions[key]

    def dimension(self, prefix: int) -> int:
        direct = sum(math.comb(prefix, q) * math.comb(2 * self.length, q)
                     for q in range(prefix + 1))
        closed = math.comb(2 * self.length + prefix, prefix)
        if direct != closed:
            raise AssertionError("prefix dimension identity")
        return direct

    def blank(self) -> PrefixState:
        return PrefixState(0, [np.ones((1, 1), dtype=np.complex128)])

    def allocate(self, prefix: int) -> PrefixState:
        return PrefixState(prefix, [
            np.zeros((len(self.lineages(prefix, q)), len(self.carriers[q].words)),
                     dtype=np.complex128)
            for q in range(prefix + 1)
        ])


def state_norm(state: PrefixState) -> float:
    return float(sum(np.vdot(block, block).real for block in state.blocks))


def state_weights(state: PrefixState, length: int) -> np.ndarray:
    answer = np.zeros(length + 1)
    for q, block in enumerate(state.blocks):
        answer[q] = float(np.vdot(block, block).real)
    return answer


def block_statistics(
    carrier: CarrierBlock, q: int, vector: np.ndarray, length: int
) -> tuple[float, np.ndarray]:
    probability = np.sum(np.abs(vector) ** 2, axis=0)
    norm = float(np.sum(probability))
    occupation = np.zeros(2 * length)
    for site in range(2 * length):
        occupation[site] = float(np.sum(probability[((carrier.words >> site) & 1) != 0]))
    return norm, occupation


def state_statistics(basis: PrefixBasis, state: PrefixState) -> dict[str, object]:
    sectors = np.zeros(basis.length + 1)
    occupation = np.zeros(basis.sites)
    for q, vector in enumerate(state.blocks):
        norm, occupied = block_statistics(basis.carriers[q], q, vector, basis.length)
        sectors[q] += norm
        occupation += occupied
    return {
        "norm": float(np.sum(sectors)),
        "sectors": sectors,
        "occupation": occupation,
        "retained": float(np.dot(np.arange(basis.length + 1), sectors)),
        "remaining": float(np.dot(basis.length - np.arange(basis.length + 1), sectors)),
    }


def classify(basis: PrefixBasis, state: PrefixState, event: int) -> tuple[float, float, float]:
    if state.prefix != event:
        raise AssertionError("event does not equal fresh prefix")
    allowed = 0.0
    blocked = 0.0
    for q, vector in enumerate(state.blocks):
        words = basis.carriers[q].words
        blank = ((words >> event) & 1) == 0
        allowed += float(np.vdot(vector[:, blank], vector[:, blank]).real)
        blocked += float(np.vdot(vector[:, ~blank], vector[:, ~blank]).real)
    return allowed, blocked, 0.0


def admit_prefix(basis: PrefixBasis, state: PrefixState, event: int) -> tuple[PrefixState, float]:
    if event != state.prefix or event >= basis.length - 1:
        raise AssertionError("nonterminal fresh admission expected")
    answer = basis.allocate(event + 1)
    cosine = math.cos(ANGLE)
    sine = math.sin(ANGLE)
    blocked_error = 0.0
    for q, old in enumerate(state.blocks):
        old_lineage = basis.lineages(event, q)
        same_position = basis.lineage_positions(event + 1, q)
        same_rows = np.fromiter((same_position[int(word)] for word in old_lineage),
                                dtype=np.int32, count=len(old_lineage))
        carrier_words = basis.carriers[q].words
        blank = ((carrier_words >> event) & 1) == 0
        factors = np.where(blank, cosine, 1.0)
        answer.blocks[q][same_rows, :] = old * factors[np.newaxis, :]
        if np.any(~blank):
            blocked_error = max(
                blocked_error,
                float(np.max(np.abs(answer.blocks[q][np.ix_(same_rows, np.flatnonzero(~blank))]
                                    - old[:, ~blank]))),
            )
        if q == basis.length:
            continue
        added_position = basis.lineage_positions(event + 1, q + 1)
        added_rows = np.fromiter(
            (added_position[int(word) | (1 << event)] for word in old_lineage),
            dtype=np.int32,
            count=len(old_lineage),
        )
        old_columns = np.flatnonzero(blank).astype(np.int32)
        new_block = basis.carriers[q + 1]
        new_columns = np.fromiter(
            (new_block.position[int(carrier_words[column]) | (1 << event)]
             for column in old_columns),
            dtype=np.int32,
            count=len(old_columns),
        )
        answer.blocks[q + 1][np.ix_(added_rows, new_columns)] = -1.0j * sine * old[:, old_columns]
    return answer, blocked_error


@lru_cache(maxsize=None)
def coefficients(scale: float, elapsed: float, degree: int) -> tuple[complex, ...]:
    argument = scale * elapsed
    values = [complex(mpmath.besselj(0, argument))]
    values.extend(
        2.0 * ((-1.0j) ** order) * complex(mpmath.besselj(order, argument))
        for order in range(1, degree + 1)
    )
    return tuple(values)


@lru_cache(maxsize=None)
def tail_indicator(scale: float, elapsed: float, degree: int) -> float:
    argument = scale * elapsed
    return float(sum(
        2.0 * abs(mpmath.besselj(order, argument))
        for order in range(degree + 1, degree + 33)
    ))


def evolve_batch(
    carrier: CarrierBlock, vector: np.ndarray, accuracy: Accuracy
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    flat = vector.reshape(-1)
    if not np.any(flat) or carrier.q == 0:
        return vector.copy(), np.zeros(len(carrier.exchanges)), {
            "converged": True,
            "degree": 0,
            "endpoint_difference": 0.0,
            "tail_indicator_32": 0.0,
        }
    maximum = max(accuracy.checkpoints)
    scale = 3.0 * carrier.q
    chebyshev = np.empty((maximum + 1, flat.size), dtype=np.complex128)
    chebyshev[0] = flat
    chebyshev[1] = (carrier.multiply(vector) / scale).reshape(-1)
    previous: np.ndarray | None = None
    selected: np.ndarray | None = None
    selected_degree = 0
    selected_difference = math.inf
    selected_tail = math.inf
    converged = False
    for degree in range(maximum + 1):
        if degree >= 2:
            chebyshev[degree] = (
                2.0 * carrier.multiply(chebyshev[degree - 1].reshape(vector.shape)).reshape(-1) / scale
                - chebyshev[degree - 2]
            )
        if degree in accuracy.checkpoints:
            weight = np.asarray(coefficients(scale, ROUTE_TIME, degree), dtype=np.complex128)
            candidate = np.einsum("i,ij->j", weight, chebyshev[:degree + 1], optimize=False)
            difference = math.inf if previous is None else float(np.linalg.norm(candidate - previous))
            indicator = tail_indicator(scale, ROUTE_TIME, degree)
            selected = candidate
            selected_degree = degree
            selected_difference = difference
            selected_tail = indicator
            if previous is not None and difference <= accuracy.tolerance and indicator <= accuracy.tolerance:
                converged = True
                break
            previous = candidate
    if selected is None:
        raise AssertionError("no Chebyshev checkpoint")
    nodes, weights = np.polynomial.legendre.leggauss(accuracy.gauss_order)
    integrated = np.zeros(len(carrier.exchanges))
    for node, weight in zip(nodes, weights):
        elapsed = 0.5 * ROUTE_TIME * (float(node) + 1.0)
        coefficient = np.asarray(coefficients(scale, elapsed, selected_degree), dtype=np.complex128)
        sample = np.einsum(
            "i,ij->j", coefficient, chebyshev[:selected_degree + 1], optimize=False
        ).reshape(vector.shape)
        integrated += float(weight) * carrier.currents(sample)
    integrated *= 0.5 * ROUTE_TIME
    return selected.reshape(vector.shape), integrated, {
        "converged": converged,
        "degree": selected_degree,
        "endpoint_difference": selected_difference,
        "tail_indicator_32": selected_tail,
    }


def blank_method(edge_count: int) -> dict[str, object]:
    return {
        "converged": True,
        "batches": 0,
        "maximum_degree": 0,
        "maximum_endpoint_difference": 0.0,
        "maximum_tail_indicator_32": 0.0,
    }


def combine_method(total: dict[str, object], record: dict[str, object]) -> None:
    total["converged"] = bool(total["converged"]) and bool(record["converged"])
    total["batches"] = int(total["batches"]) + 1
    total["maximum_degree"] = max(int(total["maximum_degree"]), int(record["degree"]))
    if math.isfinite(float(record["endpoint_difference"])):
        total["maximum_endpoint_difference"] = max(
            float(total["maximum_endpoint_difference"]), float(record["endpoint_difference"])
        )
    total["maximum_tail_indicator_32"] = max(
        float(total["maximum_tail_indicator_32"]), float(record["tail_indicator_32"])
    )


def batch_rows(columns: int, degree: int, amplitude_window: int | None = None) -> int:
    rows = max(1, KRYLOV_BYTES // ((degree + 1) * columns * 16))
    if amplitude_window is not None:
        rows = min(rows, max(1, amplitude_window // (columns * 16)))
    return rows


def evolve_state(
    basis: PrefixBasis, state: PrefixState, accuracy: Accuracy
) -> tuple[np.ndarray, dict[str, object]]:
    integrated = np.zeros(len(basis.edges))
    method = blank_method(len(basis.edges))
    for q, sector in enumerate(state.blocks):
        step = min(len(sector), batch_rows(sector.shape[1], max(accuracy.checkpoints)))
        for lower in range(0, len(sector), step):
            upper = min(len(sector), lower + step)
            final, flux, record = evolve_batch(basis.carriers[q], sector[lower:upper], accuracy)
            sector[lower:upper] = final
            integrated += flux
            combine_method(method, record)
    method["quadrature_nodes"] = accuracy.gauss_order
    return integrated, method


def empty_statistics(length: int) -> dict[str, object]:
    return {
        "norm": 0.0,
        "sectors": np.zeros(length + 1),
        "occupation": np.zeros(2 * length),
        "retained": 0.0,
        "remaining": 0.0,
    }


def add_block_statistics(
    statistics: dict[str, object], basis: PrefixBasis, q: int, vector: np.ndarray
) -> None:
    norm, occupation = block_statistics(basis.carriers[q], q, vector, basis.length)
    statistics["norm"] = float(statistics["norm"]) + norm
    statistics["sectors"][q] += norm
    statistics["occupation"] += occupation
    statistics["retained"] = float(statistics["retained"]) + q * norm
    statistics["remaining"] = float(statistics["remaining"]) + (basis.length - q) * norm


def terminal_actual(
    basis: PrefixBasis, state: PrefixState, event: int, accuracy: Accuracy
) -> tuple[dict[str, object], dict[str, object], np.ndarray, dict[str, object], float]:
    if event != basis.length - 1 or state.prefix != event:
        raise AssertionError("terminal prefix mismatch")
    admitted = empty_statistics(basis.length)
    transported = empty_statistics(basis.length)
    integrated = np.zeros(len(basis.edges))
    method = blank_method(len(basis.edges))
    cosine = math.cos(ANGLE)
    sine = math.sin(ANGLE)
    blocked_error = 0.0
    for q, old in enumerate(state.blocks):
        old_carrier = basis.carriers[q]
        blank = ((old_carrier.words >> event) & 1) == 0
        occupied = ~blank
        step0 = min(len(old), batch_rows(old.shape[1], max(accuracy.checkpoints), TERMINAL_WINDOW_BYTES))
        for lower in range(0, len(old), step0):
            upper = min(len(old), lower + step0)
            child = old[lower:upper].copy()
            child[:, blank] *= cosine
            if np.any(occupied):
                blocked_error = max(
                    blocked_error,
                    float(np.max(np.abs(child[:, occupied] - old[lower:upper, occupied]))),
                )
            add_block_statistics(admitted, basis, q, child)
            final, flux, record = evolve_batch(old_carrier, child, accuracy)
            add_block_statistics(transported, basis, q, final)
            integrated += flux
            combine_method(method, record)
        if q >= basis.length:
            continue
        old_columns = np.flatnonzero(blank).astype(np.int32)
        new_carrier = basis.carriers[q + 1]
        new_columns = np.fromiter(
            (new_carrier.position[int(old_carrier.words[column]) | (1 << event)]
             for column in old_columns),
            dtype=np.int32,
            count=len(old_columns),
        )
        step1 = min(
            len(old),
            batch_rows(len(new_carrier.words), max(accuracy.checkpoints), TERMINAL_WINDOW_BYTES),
        )
        for lower in range(0, len(old), step1):
            upper = min(len(old), lower + step1)
            child = np.zeros((upper - lower, len(new_carrier.words)), dtype=np.complex128)
            child[:, new_columns] = -1.0j * sine * old[lower:upper, old_columns]
            add_block_statistics(admitted, basis, q + 1, child)
            final, flux, record = evolve_batch(new_carrier, child, accuracy)
            add_block_statistics(transported, basis, q + 1, final)
            integrated += flux
            combine_method(method, record)
    method["quadrature_nodes"] = accuracy.gauss_order
    method["terminal_children_streamed"] = True
    method["terminal_window_bytes"] = TERMINAL_WINDOW_BYTES
    return admitted, transported, integrated, method, blocked_error


def run_history(length: int, accuracy: Accuracy) -> dict[str, object]:
    basis = PrefixBasis(length)
    state = basis.blank()
    rows: list[dict[str, object]] = []
    for event in range(length):
        before = state
        before_stats = state_statistics(basis, before)
        allowed, blocked, reverse = classify(basis, before, event)
        if event == length - 1:
            admitted_stats, after_stats, actual_flux, actual_method, blocked_error = terminal_actual(
                basis, before, event, accuracy
            )
            null_flux, null_method = evolve_state(basis, before, accuracy)
            null_stats = state_statistics(basis, before)
            terminal = True
        else:
            admitted, blocked_error = admit_prefix(basis, before, event)
            admitted_stats = state_statistics(basis, admitted)
            actual_flux, actual_method = evolve_state(basis, admitted, accuracy)
            after_stats = state_statistics(basis, admitted)
            null_flux, null_method = evolve_state(basis, before, accuracy)
            null_stats = state_statistics(basis, before)
            state = admitted
            terminal = False
        write = float(admitted_stats["retained"]) - float(before_stats["retained"])
        actual_node = (
            after_stats["occupation"] - admitted_stats["occupation"]
            + basis.incidence @ actual_flux
        )
        null_node = (
            null_stats["occupation"] - before_stats["occupation"]
            + basis.incidence @ null_flux
        )
        delta = actual_flux - null_flux
        rows.append({
            "event": event + 1,
            "input_prefix": event,
            "input_prefix_dimension": basis.dimension(event),
            "logical_output_prefix_dimension": basis.dimension(event + 1),
            "terminal_children_streamed": terminal,
            "allow_probability": allowed,
            "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": blocked_error,
            "W_n": write,
            "q_retained_after_transport": float(after_stats["retained"]),
            "q_genesis_after": float(after_stats["remaining"]),
            "sector_weights": after_stats["sectors"].tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta[basis.connectors]))),
            "connector_delta_signed": float(np.sum(delta[basis.connectors])),
            "admission_total_content_residual": (
                write + float(admitted_stats["remaining"]) - float(before_stats["remaining"])
            ),
            "admission_bandwidth_residual": (
                float(admitted_stats["remaining"]) - float(before_stats["remaining"]) + write
            ),
            "target_owner_residual": (
                float(admitted_stats["occupation"][event])
                - float(before_stats["occupation"][event]) - write
            ),
            "transport_node_residual_l1": float(np.sum(np.abs(actual_node))),
            "transport_node_residual_linf": float(np.max(np.abs(actual_node))),
            "null_transport_node_residual_l1": float(np.sum(np.abs(null_node))),
            "transport_number_drift": abs(
                float(after_stats["retained"]) - float(admitted_stats["retained"])
            ),
            "null_transport_number_drift": abs(
                float(null_stats["retained"]) - float(before_stats["retained"])
            ),
            "actual_norm_error": abs(float(after_stats["norm"]) - 1.0),
            "null_norm_error": abs(float(null_stats["norm"]) - 1.0),
            "actual_solver": actual_method,
            "null_solver": null_method,
        })
    return {
        "rows": rows,
        "full_dimension": basis.dimension(length),
        "largest_materialized_dimension": basis.dimension(length - 1),
        "edges": len(basis.edges),
        "edge_layout": [list(edge) for edge in basis.edges],
    }


def minimal_interval(weights: np.ndarray) -> tuple[int, int, float]:
    candidates: list[tuple[int, float, int, int]] = []
    for lower in range(len(weights)):
        mass = 0.0
        for upper in range(lower, len(weights)):
            mass += float(weights[upper])
            if mass + 1.0e-15 >= 0.99:
                candidates.append((upper - lower, -mass, lower, upper))
                break
    if not candidates:
        raise AssertionError("no 99-percent sector interval")
    _, negative_mass, lower, upper = min(candidates)
    return lower, upper, -negative_mass


def compare(length: int, rough: dict[str, object], sharp: dict[str, object]) -> dict[str, object]:
    fields = (
        "W_n", "allow_probability", "blocked_probability",
        "connector_delta_l1", "connector_delta_signed",
    )
    observable = max(
        abs(float(left[field]) - float(right[field]))
        for left, right in zip(rough["rows"], sharp["rows"])
        for field in fields
    )
    sector = max(
        max(abs(float(a) - float(b)) for a, b in zip(left["sector_weights"], right["sector_weights"]))
        for left, right in zip(rough["rows"], sharp["rows"])
    )
    disagreement = max(observable, sector)
    epsilon = max(1.0e-11, 50.0 * disagreement)
    rows = sharp["rows"]
    admission = max(abs(float(row[field])) for row in rows for field in (
        "admission_total_content_residual", "admission_bandwidth_residual", "target_owner_residual"
    ))
    node = max(max(abs(float(row["transport_node_residual_l1"])),
                   abs(float(row["null_transport_node_residual_l1"]))) for row in rows)
    number = max(max(abs(float(row["transport_number_drift"])),
                     abs(float(row["null_transport_number_drift"]))) for row in rows)
    norm = max(max(abs(float(row["actual_norm_error"])), abs(float(row["null_norm_error"])))
               for row in rows)
    methods = [row[key] for row in rows for key in ("actual_solver", "null_solver")]
    late = rows[math.ceil(length / 2) - 1:]
    average = np.mean(np.asarray([row["sector_weights"] for row in late]), axis=0)
    lower, upper, mass = minimal_interval(average)
    writes = np.asarray([float(row["W_n"]) for row in rows])
    connector = np.asarray([float(row["connector_delta_l1"]) for row in rows])
    passed = (
        len(rows) == length
        and [row["event"] for row in rows] == list(range(1, length + 1))
        and rows[-1]["terminal_children_streamed"] is True
        and all(not row["terminal_children_streamed"] for row in rows[:-1])
        and all(bool(method["converged"]) for method in methods)
        and admission <= 1.0e-10
        and node <= max(1.0e-9, 100.0 * epsilon)
        and number <= 1.0e-10
        and norm <= 1.0e-10
        and max(abs(float(row["reverse_support_probability"])) for row in rows) <= 1.0e-11
        and max(abs(float(row["blocked_null_state_error"])) for row in rows) <= 1.0e-11
        and min(writes) >= -epsilon
        and max(float(row["blocked_probability"]) for row in rows) > 1.0e-6
    )
    return {
        "classification": "RESOLVED_PREFIX_HISTORY_CONTROL" if passed else "UNRESOLVED_PREFIX_HISTORY_CONTROL",
        "resolved": passed,
        "rough_sharp": {
            "observable_linf": observable,
            "sector_weight_linf": sector,
            "maximum_disagreement": disagreement,
        },
        "epsilon": epsilon,
        "maximum_admission_accounting_residual": admission,
        "maximum_node_continuity_residual_l1": node,
        "maximum_number_drift": number,
        "maximum_norm_error": norm,
        "admission_acceptance": (2.0 * writes).tolist(),
        "connector_ratio": (connector / connector[0]).tolist(),
        "routed_acceptance": np.minimum(2.0 * writes, connector / connector[0]).tolist(),
        "sector": {
            "late_events": [row["event"] for row in late],
            "q_lower": lower,
            "q_upper": upper,
            "enclosed_mass": mass,
            "discarded_mass": 1.0 - mass,
            "density_interval": [
                max(0.0, (lower - 0.5) / (2.0 * length)),
                min(1.0, (upper + 0.5) / (2.0 * length)),
            ],
        },
    }


def require_gate(path: Path, classification: str) -> None:
    if not path.exists():
        raise RuntimeError(f"required sealed gate is absent: {path.name}")
    record = json.loads(path.read_text())
    if record.get("classification") != classification:
        raise RuntimeError(f"required sealed gate did not pass: {path.name}")
    if record.get("implementation_sha256") != sha256(Path(__file__)):
        raise RuntimeError(f"required gate does not pin this implementation: {path.name}")


def authorize(length: int) -> None:
    if length in CONTROL_SIZES:
        return
    if length == 10:
        require_gate(CONTROL_GATE, "PASS_PREFIX_HISTORY_CONTROLS_L4_L8")
        return
    if length == 12:
        require_gate(CONTROL_GATE, "PASS_PREFIX_HISTORY_CONTROLS_L4_L8")
        require_gate(SEALED_L10_GATE, "PASS_PREFIX_HISTORY_L10_GATE")
        free = shutil.disk_usage(HERE).free
        if free < L12_SCRATCH_GATE:
            raise RuntimeError(f"L12 scratch gate failed: free={free} required={L12_SCRATCH_GATE}")
        return
    raise ValueError("supported even sizes are 4, 6, 8, 10, and 12")


def run(length: int, output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"refuse to overwrite custody output: {output}")
    authorize(length)
    started = time.perf_counter()
    rough = run_history(length, ROUGH)
    sharp = run_history(length, SHARP)
    comparison = compare(length, rough, sharp)
    result = {
        "schema": "INDEPENDENT_PREFIX_LINEAGE_HISTORY_CONTROL_V001",
        "L": length,
        "events": length,
        "full_dimension": sharp["full_dimension"],
        "largest_materialized_dimension": sharp["largest_materialized_dimension"],
        "representation": "REVERSED_CANONICAL_PREFIX_MASKS__TERMINAL_TWO_CHILD_WINDOWS",
        "lineage_authority": "FULL_CANONICAL_MASK__SHA256_CUSTODY_ONLY",
        "edge_layout": sharp["edge_layout"],
        "rough_method": {
            "label": ROUGH.label,
            "checkpoints": ROUGH.checkpoints,
            "gauss_order": ROUGH.gauss_order,
            "tolerance": ROUGH.tolerance,
        },
        "sharp_method": {
            "label": SHARP.label,
            "checkpoints": SHARP.checkpoints,
            "gauss_order": SHARP.gauss_order,
            "tolerance": SHARP.tolerance,
        },
        "rows": sharp["rows"],
        "comparison": comparison,
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "implementation_sha256": sha256(Path(__file__)),
        "methodology_sha256": sha256(HERE / "METHODOLOGY.md"),
        "python": sys.version,
        "numpy": np.__version__,
        "mpmath": mpmath.__version__,
        "platform": platform.platform(),
        "claim_boundary": "INDEPENDENT_FINITE_PREFIX_HISTORY_CONTROL_ONLY",
    }
    if length == 12:
        result["resource_guards"] = {
            "rss_limit_bytes": L12_RSS_LIMIT,
            "wall_limit_seconds": L12_WALL_LIMIT,
            "rss_pass": result["peak_rss_bytes"] <= L12_RSS_LIMIT,
            "wall_pass": result["wall_seconds"] <= L12_WALL_LIMIT,
        }
        if not all(result["resource_guards"][key] for key in ("rss_pass", "wall_pass")):
            comparison["resolved"] = False
            comparison["classification"] = "EXACT_PREFIX_HISTORY_RESOURCE_OBSTRUCTION"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(comparison["classification"])
    print(f"L={length} D={result['full_dimension']} materialized={result['largest_materialized_dimension']}")
    print(f"rough/sharp={comparison['rough_sharp']['maximum_disagreement']:.3e}")
    print(f"wall={result['wall_seconds']:.3f}s rss={result['peak_rss_bytes']}")
    if not comparison["resolved"]:
        raise SystemExit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.worker, arguments.output)
