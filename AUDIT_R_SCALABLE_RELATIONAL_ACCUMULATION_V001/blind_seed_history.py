#!/usr/bin/env python3
"""Independent reversed-layout L4/L6/L8 relational seed histories."""

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
PHI = math.pi / 4.0
KAPPA = math.pi / 2.0
ORDER = 14
COARSE_STEPS = 96
FINE_STEPS = 192
SIZES = (4, 6, 8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph(length: int) -> list[tuple[int, int, str]]:
    result = []
    for i in range(length):
        result.append((i, (i + 1) % length, "rail_1"))
    for i in range(length):
        result.append((length + i, length + (i + 1) % length, "rail_2"))
    for i in range(length):
        result.append((i, length + (i + 1) % length, "connector"))
    return result


def words_of_weight(width: int, weight: int) -> np.ndarray:
    words = []
    for chosen in itertools.combinations(reversed(range(width)), weight):
        value = 0
        for position in chosen:
            value += 1 << position
        words.append(value)
    return np.array(words, dtype=np.uint32)


def counts(words: np.ndarray, width: int) -> np.ndarray:
    result = np.zeros(len(words), dtype=np.uint8)
    work = words.copy()
    for _ in range(width):
        result += (work % 2).astype(np.uint8)
        work //= 2
    return result


class BlindParent:
    def __init__(self, length: int):
        self.length = length
        self.carrier_sites = 2 * length
        self.basis = words_of_weight(3 * length, length)
        self.lookup = {int(word): index for index, word in enumerate(self.basis)}
        carrier_mask = (1 << self.carrier_sites) - 1
        self.carrier = self.basis & np.uint32(carrier_mask)
        self.genesis = self.basis >> np.uint32(self.carrier_sites)
        self.q_values = counts(self.carrier, self.carrier_sites)
        self.g_values = counts(self.genesis, length)
        self.edge_list = graph(length)
        self.connectors = [i for i, row in enumerate(self.edge_list) if row[2] == "connector"]
        self.incidence = np.zeros((self.carrier_sites, 3 * length), dtype=np.int8)
        self.moves = []
        for edge_index, (u, v, _) in enumerate(self.edge_list):
            u_bits = ((self.carrier >> u) & 1).astype(np.int8)
            v_bits = ((self.carrier >> v) & 1).astype(np.int8)
            source = np.flatnonzero(u_bits != v_bits).astype(np.int32)
            mask = np.uint32((1 << u) | (1 << v))
            destination = np.fromiter(
                (self.lookup[int(word ^ mask)] for word in self.basis[source]),
                dtype=np.int32,
                count=len(source),
            )
            self.moves.append((source, destination, (v_bits[source] - u_bits[source]).astype(np.int8)))
            self.incidence[u, edge_index] = 1
            self.incidence[v, edge_index] = -1
        self.admissions = []
        for event in range(length):
            loaded = ((self.genesis >> event) & 1) == 1
            blank = ((self.carrier >> event) & 1) == 0
            source = np.flatnonzero(loaded & blank).astype(np.int32)
            mask = np.uint32((1 << (self.carrier_sites + event)) | (1 << event))
            destination = np.fromiter(
                (self.lookup[int(word ^ mask)] for word in self.basis[source]),
                dtype=np.int32,
                count=len(source),
            )
            self.admissions.append((source, destination))

    def start(self) -> np.ndarray:
        vector = np.zeros(len(self.basis), dtype=np.complex128)
        genesis_full = ((1 << self.length) - 1) << self.carrier_sites
        vector[self.lookup[genesis_full]] = 1.0
        return vector

    def q(self, vector: np.ndarray) -> float:
        return float(np.sum(np.abs(vector) ** 2 * self.q_values))

    def g(self, vector: np.ndarray) -> float:
        return float(np.sum(np.abs(vector) ** 2 * self.g_values))

    def probabilities(self, vector: np.ndarray, event: int) -> tuple[float, float, float]:
        loaded = ((self.genesis >> event) & 1) == 1
        occupied = ((self.carrier >> event) & 1) == 1
        p = np.abs(vector) ** 2
        return (
            float(np.sum(p[loaded & ~occupied])),
            float(np.sum(p[loaded & occupied])),
            float(np.sum(p[~loaded & occupied])),
        )

    def admit(self, vector: np.ndarray, event: int) -> np.ndarray:
        source, destination = self.admissions[event]
        result = vector.copy()
        left = vector[source]
        right = vector[destination]
        c = math.cos(PHI)
        s = math.sin(PHI)
        result[source] = c * left - 1j * s * right
        result[destination] = c * right - 1j * s * left
        return result

    def h(self, vector: np.ndarray) -> np.ndarray:
        result = np.zeros_like(vector)
        for source, destination, _ in self.moves:
            result[source] -= vector[destination]
        return result

    def edge_current(self, vector: np.ndarray) -> np.ndarray:
        result = []
        for source, destination, orientation in self.moves:
            value = np.sum(np.conjugate(vector[source]) * (1j * orientation) * vector[destination]).real
            result.append(float(value))
        return np.array(result)

    def occupation(self, vector: np.ndarray) -> np.ndarray:
        p = np.abs(vector) ** 2
        return np.array([
            float(np.sum(p[((self.carrier >> site) & 1) == 1]))
            for site in range(self.carrier_sites)
        ])

    def sectors(self, vector: np.ndarray) -> np.ndarray:
        return np.bincount(self.q_values, weights=np.abs(vector) ** 2, minlength=self.carrier_sites + 1).astype(float)

    def step(self, vector: np.ndarray, dt: float) -> np.ndarray:
        answer = vector.copy()
        term = vector.copy()
        for degree in range(1, ORDER + 1):
            term = (-1j * dt / degree) * self.h(term)
            answer += term
        return answer

    def route(self, vector: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray]:
        dt = KAPPA / steps
        routed = vector.copy()
        flux = self.edge_current(routed)
        for tick in range(1, steps + 1):
            routed = self.step(routed, dt)
            coefficient = 1 if tick == steps else (4 if tick % 2 else 2)
            flux += coefficient * self.edge_current(routed)
        return routed, flux * dt / 3.0


def minimal_mass_interval(weights: np.ndarray) -> tuple[int, int, float]:
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


def solve(length: int, steps: int) -> dict[str, object]:
    parent = BlindParent(length)
    vector = parent.start()
    rows = []
    for event in range(length):
        before = vector
        allow, blocked, reverse = parent.probabilities(before, event)
        q0 = parent.q(before)
        g0 = parent.g(before)
        occ0 = parent.occupation(before)
        accepted = parent.admit(before, event)
        q1 = parent.q(accepted)
        g1 = parent.g(accepted)
        occ1 = parent.occupation(accepted)
        write = q1 - q0
        actual, actual_flux = parent.route(accepted, steps)
        null, null_flux = parent.route(before, steps)
        delta_flux = actual_flux - null_flux
        occ2 = parent.occupation(actual)
        residual = occ2 - occ1 + parent.incidence @ actual_flux
        rows.append({
            "event": event + 1,
            "allow_probability": allow,
            "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": 0.0,
            "W_n": write,
            "q_retained_after_transport": parent.q(actual),
            "q_genesis_after": parent.g(actual),
            "sector_weights": parent.sectors(actual).tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta_flux[parent.connectors]))),
            "connector_delta_signed": float(np.sum(delta_flux[parent.connectors])),
            "admission_total_content_residual": write + g1 - g0,
            "admission_bandwidth_residual": g1 - g0 + write,
            "target_owner_residual": occ1[event] - occ0[event] - write,
            "transport_node_residual_l1": float(np.sum(np.abs(residual))),
            "transport_node_residual_linf": float(np.max(np.abs(residual))),
            "transport_number_drift": abs(parent.q(actual) - q1),
            "actual_norm_error": abs(float(np.vdot(actual, actual).real) - 1.0),
            "null_norm_error": abs(float(np.vdot(null, null).real) - 1.0),
        })
        vector = actual
    late = rows[math.ceil(length / 2) - 1:]
    pbar = np.mean(np.array([row["sector_weights"] for row in late]), axis=0)
    lower, upper, mass = minimal_mass_interval(pbar)
    return {
        "rows": rows,
        "final": vector,
        "dimension": len(parent.basis),
        "sector": {
            "late_events": [row["event"] for row in late],
            "q_lower": lower,
            "q_upper": upper,
            "enclosed_mass": mass,
            "discarded_mass": 1.0 - mass,
            "density_interval": [max(0.0, (lower - 0.5) / (2 * length)), min(1.0, (upper + 0.5) / (2 * length))],
        },
    }


def compare_internal(coarse: dict[str, object], fine: dict[str, object]) -> dict[str, object]:
    overlap = abs(np.vdot(coarse["final"], fine["final"]))
    state_error = math.sqrt(max(0.0, 1.0 - min(1.0, float(overlap) ** 2)))
    row_error = max(
        abs(float(a[key]) - float(b[key]))
        for a, b in zip(coarse["rows"], fine["rows"])
        for key in ("W_n", "allow_probability", "blocked_probability", "connector_delta_l1", "connector_delta_signed")
    )
    sector_error = max(
        float(np.max(np.abs(np.array(a["sector_weights"]) - np.array(b["sector_weights"]))))
        for a, b in zip(coarse["rows"], fine["rows"])
    )
    disagreement = max(state_error, row_error, sector_error)
    epsilon = max(1.0e-11, 50.0 * disagreement)
    rows = fine["rows"]
    resolved = (
        min(float(row["W_n"]) for row in rows) >= -epsilon
        and max(float(row["reverse_support_probability"]) for row in rows) <= 1.0e-11
        and max(abs(float(row["admission_total_content_residual"])) for row in rows) <= 1.0e-10
        and max(float(row["transport_node_residual_l1"]) for row in rows) <= max(1.0e-9, 100.0 * epsilon)
        and max(float(row["actual_norm_error"]) for row in rows) <= 1.0e-10
        and max(float(row["transport_number_drift"]) for row in rows) <= 1.0e-10
        and max(float(row["blocked_probability"]) for row in rows) > 1.0e-6
    )
    return {
        "classification": "RESOLVED_RELATIONAL_HISTORY_L" if resolved else "UNRESOLVED_RELATIONAL_HISTORY_L",
        "resolved": resolved,
        "coarse_fine": {
            "final_projective_error": state_error,
            "observable_linf": row_error,
            "sector_weight_linf": sector_error,
            "maximum_disagreement": disagreement,
        },
        "epsilon": epsilon,
        "sector": fine["sector"],
    }


def worker(length: int, output: Path) -> None:
    if length not in SIZES:
        raise ValueError("blind seed supports L4/L6/L8")
    started = time.perf_counter()
    coarse = solve(length, COARSE_STEPS)
    fine = solve(length, FINE_STEPS)
    result = {
        "schema": "SCALABLE_RELATIONAL_ACCUMULATION_BLIND_ROW_V001",
        "L": length,
        "dimension": fine["dimension"],
        "events": length,
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
        "taylor_order": ORDER,
        "rows": fine["rows"],
        "comparison": compare_internal(coarse, fine),
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "protocol_sha256": sha256(ROOT_PROTOCOL()),
        "implementation_sha256": sha256(Path(__file__)),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "claim_boundary": {"empirical": "FINITE_BLIND_SEED_ROW_ONLY", "not_claimed": ["CONTINUUM", "EMERGENCE", "GRAVITY"]},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"BLIND L{length} {result['comparison']['classification']} D={result['dimension']} wall={result['wall_seconds']:.3f}s")


def ROOT_PROTOCOL() -> Path:
    return HERE.parent / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "PROTOCOL.md"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    worker(args.L, args.output)
