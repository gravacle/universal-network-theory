#!/usr/bin/env python3
"""Exact fixed-content seed histories for scalable relational accumulation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
RAW = HERE / "RAW_HISTORY"
SEED_OUT = HERE / "SEED_RESULT.json"
PHI = math.pi / 4.0
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 12
COARSE_STEPS = 64
FINE_STEPS = 128
SEED_SIZES = (4, 6, 8)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bitcounts(words: np.ndarray, width: int) -> np.ndarray:
    work = words.copy()
    result = np.zeros(len(words), dtype=np.uint8)
    for _ in range(width):
        result += (work & 1).astype(np.uint8)
        work >>= 1
    return result


def prism_edges(length: int) -> list[tuple[int, int, str]]:
    answer: list[tuple[int, int, str]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            answer.append((offset + site, offset + (site + 1) % length, f"rail_{rail + 1}"))
    for site in range(length):
        answer.append((site, length + (site + 1) % length, "connector"))
    return answer


def fixed_weight_words(width: int, weight: int) -> np.ndarray:
    count = math.comb(width, weight)
    values = np.empty(count, dtype=np.uint32)
    for index, positions in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        values[index] = word
    return values


class Parent:
    def __init__(self, length: int):
        self.length = length
        self.sites = 2 * length
        self.width = 3 * length
        self.words = fixed_weight_words(self.width, length)
        self.dimension = len(self.words)
        self.index = {int(word): index for index, word in enumerate(self.words)}
        self.carrier_words = self.words >> np.uint32(length)
        self.carrier_counts = bitcounts(self.carrier_words, self.sites)
        self.genesis_counts = length - self.carrier_counts
        self.edges = prism_edges(length)
        self.connector_indices = [i for i, edge in enumerate(self.edges) if edge[2] == "connector"]
        self.incidence = np.zeros((self.sites, len(self.edges)), dtype=np.int8)
        self.actions: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for edge_index, (u, v, _) in enumerate(self.edges):
            bit_u = ((self.carrier_words >> u) & 1).astype(np.int8)
            bit_v = ((self.carrier_words >> v) & 1).astype(np.int8)
            active = np.flatnonzero(bit_u != bit_v).astype(np.int32)
            global_mask = np.uint32((1 << (length + u)) | (1 << (length + v)))
            destinations = np.fromiter(
                (self.index[int(word ^ global_mask)] for word in self.words[active]),
                dtype=np.int32,
                count=len(active),
            )
            signs = (bit_v[active] - bit_u[active]).astype(np.int8)
            self.actions.append((active, destinations, signs))
            self.incidence[u, edge_index] = 1
            self.incidence[v, edge_index] = -1
        self.admission_pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for event in range(length):
            genesis_loaded = ((self.words >> event) & 1) == 1
            target_blank = ((self.carrier_words >> event) & 1) == 0
            sources = np.flatnonzero(genesis_loaded & target_blank).astype(np.int32)
            mask = np.uint32((1 << event) | (1 << (length + event)))
            destinations = np.fromiter(
                (self.index[int(word ^ mask)] for word in self.words[sources]),
                dtype=np.int32,
                count=len(sources),
            )
            self.admission_pairs.append((sources, destinations))

    def initial_state(self) -> np.ndarray:
        state = np.zeros(self.dimension, dtype=np.complex128)
        state[self.index[(1 << self.length) - 1]] = 1.0
        return state

    def q(self, state: np.ndarray) -> float:
        return float(np.dot(self.carrier_counts.astype(float), np.abs(state) ** 2))

    def genesis_q(self, state: np.ndarray) -> float:
        return float(np.dot(self.genesis_counts.astype(float), np.abs(state) ** 2))

    def sector_weights(self, state: np.ndarray) -> np.ndarray:
        return np.bincount(
            self.carrier_counts,
            weights=np.abs(state) ** 2,
            minlength=self.sites + 1,
        ).astype(float)

    def occupations(self, state: np.ndarray) -> np.ndarray:
        probability = np.abs(state) ** 2
        return np.array([
            float(np.sum(probability[((self.carrier_words >> site) & 1) == 1]))
            for site in range(self.sites)
        ])

    def predicates(self, state: np.ndarray, event: int) -> tuple[float, float, float]:
        genesis_loaded = ((self.words >> event) & 1) == 1
        target_occupied = ((self.carrier_words >> event) & 1) == 1
        probability = np.abs(state) ** 2
        allow = float(np.sum(probability[genesis_loaded & ~target_occupied]))
        blocked = float(np.sum(probability[genesis_loaded & target_occupied]))
        reverse = float(np.sum(probability[~genesis_loaded & target_occupied]))
        return allow, blocked, reverse

    def apply_admission(self, state: np.ndarray, event: int) -> np.ndarray:
        sources, destinations = self.admission_pairs[event]
        out = state.copy()
        left = state[sources]
        right = state[destinations]
        cosine = math.cos(PHI)
        sine = math.sin(PHI)
        out[sources] = cosine * left - 1j * sine * right
        out[destinations] = cosine * right - 1j * sine * left
        return out

    def h_action(self, state: np.ndarray) -> np.ndarray:
        out = np.zeros_like(state)
        for sources, destinations, _ in self.actions:
            out[sources] -= state[destinations]
        return out

    def currents(self, state: np.ndarray) -> np.ndarray:
        answer = np.empty(len(self.actions), dtype=float)
        for index, (sources, destinations, signs) in enumerate(self.actions):
            answer[index] = float(np.sum(
                np.conjugate(state[sources]) * (1j * signs) * state[destinations]
            ).real)
        return answer

    def taylor_step(self, state: np.ndarray, step: float) -> np.ndarray:
        updated = state.copy()
        term = state.copy()
        for order in range(1, TAYLOR_ORDER + 1):
            term = (-1j * step / order) * self.h_action(term)
            updated += term
        return updated

    def transport(self, state: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray]:
        step = KAPPA / steps
        evolved = state.copy()
        integrated = self.currents(evolved)
        for index in range(1, steps + 1):
            evolved = self.taylor_step(evolved, step)
            weight = 1 if index == steps else (4 if index % 2 else 2)
            integrated += weight * self.currents(evolved)
        integrated *= step / 3.0
        return evolved, integrated


def shortest_interval(weights: np.ndarray, coverage: float = 0.99) -> tuple[int, int, float]:
    best: tuple[int, float, int, int] | None = None
    for lower in range(len(weights)):
        total = 0.0
        for upper in range(lower, len(weights)):
            total += float(weights[upper])
            if total + 1.0e-15 >= coverage:
                candidate = (upper - lower, -total, lower, upper)
                if best is None or candidate < best:
                    best = candidate
                break
    if best is None:
        raise AssertionError("sector mass below coverage")
    _, negative_mass, lower, upper = best
    return lower, upper, -negative_mass


def run_resolution(length: int, steps: int) -> dict[str, object]:
    parent = Parent(length)
    state = parent.initial_state()
    rows = []
    for event in range(length):
        before = state
        allow, blocked, reverse = parent.predicates(before, event)
        q_before = parent.q(before)
        g_before = parent.genesis_q(before)
        occ_before = parent.occupations(before)
        admitted = parent.apply_admission(before, event)
        q_admitted = parent.q(admitted)
        g_admitted = parent.genesis_q(admitted)
        occ_admitted = parent.occupations(admitted)
        write = q_admitted - q_before
        actual, actual_currents = parent.transport(admitted, steps)
        null, null_currents = parent.transport(before, steps)
        occ_after = parent.occupations(actual)
        q_after = parent.q(actual)
        transport_residual = occ_after - occ_admitted + parent.incidence @ actual_currents
        delta_current = actual_currents - null_currents
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
            "q_genesis_after": parent.genesis_q(actual),
            "bandwidth_after": g_admitted,
            "lineage_sealed_after": length - g_admitted,
            "sector_weights": parent.sector_weights(actual).tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta_current[parent.connector_indices]))),
            "connector_delta_signed": float(np.sum(delta_current[parent.connector_indices])),
            "admission_total_content_residual": (q_admitted - q_before) + (g_admitted - g_before),
            "admission_bandwidth_residual": (g_admitted - g_before) + write,
            "target_owner_residual": (occ_admitted[event] - occ_before[event]) - write,
            "transport_node_residual_l1": float(np.sum(np.abs(transport_residual))),
            "transport_node_residual_linf": float(np.max(np.abs(transport_residual))),
            "transport_number_drift": abs(q_after - q_admitted),
            "transport_genesis_drift": abs(parent.genesis_q(actual) - g_admitted),
            "actual_norm_error": abs(float(np.vdot(actual, actual).real) - 1.0),
            "null_norm_error": abs(float(np.vdot(null, null).real) - 1.0),
        })
        state = actual
    late_start = math.ceil(length / 2)
    selected = rows[late_start - 1:]
    pbar = np.mean(np.array([row["sector_weights"] for row in selected]), axis=0)
    lower, upper, mass = shortest_interval(pbar)
    return {
        "steps": steps,
        "rows": rows,
        "final_state": state,
        "pbar": pbar,
        "sector": {
            "late_events": [row["event"] for row in selected],
            "q_lower": lower,
            "q_upper": upper,
            "enclosed_mass": mass,
            "discarded_mass": 1.0 - mass,
            "density_interval": [
                max(0.0, (lower - 0.5) / (2.0 * length)),
                min(1.0, (upper + 0.5) / (2.0 * length)),
            ],
        },
        "dimension": parent.dimension,
        "edges": len(parent.edges),
    }


def compare_resolutions(length: int, coarse: dict[str, object], fine: dict[str, object]) -> dict[str, object]:
    coarse_rows = coarse["rows"]
    fine_rows = fine["rows"]
    overlap = abs(np.vdot(coarse["final_state"], fine["final_state"]))
    projective_error = math.sqrt(max(0.0, 1.0 - min(1.0, float(overlap) ** 2)))
    keys = ("W_n", "allow_probability", "blocked_probability", "connector_delta_l1", "connector_delta_signed")
    observable_error = max(
        abs(float(left[key]) - float(right[key]))
        for left, right in zip(coarse_rows, fine_rows)
        for key in keys
    )
    sector_error = max(
        float(np.max(np.abs(np.array(left["sector_weights"]) - np.array(right["sector_weights"]))))
        for left, right in zip(coarse_rows, fine_rows)
    )
    disagreement = max(projective_error, observable_error, sector_error)
    epsilon = max(1.0e-11, 50.0 * disagreement)
    writes = np.array([float(row["W_n"]) for row in fine_rows])
    connectors = np.array([float(row["connector_delta_l1"]) for row in fine_rows])
    admission = 2.0 * writes
    connector_ratio = connectors / connectors[0]
    routed = np.minimum(admission, connector_ratio)
    max_accounting = max(
        abs(float(row[key]))
        for row in fine_rows
        for key in ("admission_total_content_residual", "admission_bandwidth_residual", "target_owner_residual")
    )
    resolved = (
        max_accounting <= 1.0e-10
        and min(writes) >= -epsilon
        and max(float(row["reverse_support_probability"]) for row in fine_rows) <= 1.0e-11
        and max(float(row["transport_node_residual_l1"]) for row in fine_rows) <= max(1.0e-9, 100.0 * epsilon)
        and max(float(row["actual_norm_error"]) for row in fine_rows) <= 1.0e-10
        and max(float(row["transport_number_drift"]) for row in fine_rows) <= 1.0e-10
        and max(float(row["blocked_probability"]) for row in fine_rows) > 1.0e-6
    )
    return {
        "classification": "RESOLVED_RELATIONAL_HISTORY_L" if resolved else "UNRESOLVED_RELATIONAL_HISTORY_L",
        "resolved": resolved,
        "coarse_fine": {
            "final_projective_error": projective_error,
            "observable_linf": observable_error,
            "sector_weight_linf": sector_error,
            "maximum_disagreement": disagreement,
        },
        "epsilon": epsilon,
        "admission_acceptance": admission.tolist(),
        "connector_ratio": connector_ratio.tolist(),
        "routed_acceptance": routed.tolist(),
        "sector": fine["sector"],
    }


def worker(length: int, output: Path) -> None:
    if length not in SEED_SIZES:
        raise ValueError("seed worker supports L4, L6, L8")
    started = time.perf_counter()
    coarse = run_resolution(length, COARSE_STEPS)
    fine = run_resolution(length, FINE_STEPS)
    comparison = compare_resolutions(length, coarse, fine)
    result = {
        "schema": "SCALABLE_RELATIONAL_ACCUMULATION_HISTORY_ROW_V001",
        "L": length,
        "dimension": fine["dimension"],
        "events": length,
        "edges": fine["edges"],
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
        "taylor_order": TAYLOR_ORDER,
        "rows": fine["rows"],
        "comparison": comparison,
        "final_sector_weights": parent_weights(fine["final_state"], length),
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "protocol_sha256": digest(HERE / "PROTOCOL.md"),
        "implementation_sha256": digest(Path(__file__)),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "claim_boundary": {
            "empirical": "FINITE_RELATIONAL_HISTORY_ROW_ONLY",
            "not_claimed": ["COMMON_SECTOR", "CRITICALITY", "Z_EQUALS_ONE", "CONTINUUM", "EMERGENCE", "GRAVITY"],
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"L{length} {comparison['classification']} D={fine['dimension']} wall={result['wall_seconds']:.3f}s")


def parent_weights(state: np.ndarray, length: int) -> list[float]:
    words = fixed_weight_words(3 * length, length)
    counts = bitcounts(words >> np.uint32(length), 2 * length)
    return np.bincount(counts, weights=np.abs(state) ** 2, minlength=2 * length + 1).astype(float).tolist()


def aggregate_seed() -> None:
    rows = [json.loads((RAW / f"HISTORY_L{length}.json").read_text()) for length in SEED_SIZES]
    resolved = all(row["comparison"]["resolved"] for row in rows)
    lower = max(float(row["comparison"]["sector"]["density_interval"][0]) for row in rows)
    upper = min(float(row["comparison"]["sector"]["density_interval"][1]) for row in rows)
    common = [lower, upper] if resolved and lower < upper else None
    classification = "RELATIONAL_ACCUMULATION_SEED_L4_L8" if common is not None else (
        "UNRESOLVED_RELATIONAL_ACCUMULATION_SEED" if not resolved else "NO_COMMON_RELATIONAL_ACCUMULATION_SECTOR_L4_L8"
    )
    result = {
        "schema": "SCALABLE_RELATIONAL_ACCUMULATION_SEED_V001",
        "classification": classification,
        "rows": rows,
        "common_density_interval": common,
        "next_gate": "FREEZE_L10_L12_HISTORY_METHODS" if common is not None else "HALT_BEFORE_L10_L12_AND_SPECTRUM",
        "protocol_sha256": digest(HERE / "PROTOCOL.md"),
        "implementation_sha256": digest(Path(__file__)),
        "claim_boundary": {
            "empirical": "FINITE_L4_L8_HISTORY_SEED_ONLY",
            "not_claimed": ["CRITICALITY", "Z_EQUALS_ONE", "CONTINUUM", "EMERGENCE", "GRAVITY"],
        },
    }
    SEED_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(classification, common)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--aggregate", action="store_true")
    parser.add_argument("--L", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        if args.L is None or args.output is None:
            parser.error("--worker requires --L and --output")
        worker(args.L, args.output)
    elif args.aggregate:
        aggregate_seed()
    else:
        parser.error("select --worker or --aggregate")
