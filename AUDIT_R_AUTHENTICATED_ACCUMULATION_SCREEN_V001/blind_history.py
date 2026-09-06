#!/usr/bin/env python3
"""Blind RK4 reconstruction of authenticated accumulation histories."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import resource
import sys
import time
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = ROOT / "DEVELOPMENT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001" / "PROTOCOL.md"
RAW = HERE / "RAW_HISTORY"
OUT = HERE / "BLIND_SEED_RESULT.json"
PHI = math.pi / 4.0
KAPPA = math.pi / 2.0
COARSE_STEPS = 256
FINE_STEPS = 512
SIZES = (4, 6, 8)
MASS = 0.99


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_edges(length: int) -> list[tuple[int, int, str]]:
    result = []
    for rail in range(2):
        base = rail * length
        result.extend((base + i, base + (i + 1) % length, f"rail_{rail + 1}") for i in range(length))
    result.extend((i, length + (i + 1) % length, "connector") for i in range(length))
    return result


def bit_counts(words: np.ndarray, sites: int) -> np.ndarray:
    result = np.zeros(len(words), dtype=np.uint8)
    for bit in range(sites):
        result += ((words >> bit) & 1).astype(np.uint8)
    return result


class BlindCarrier:
    def __init__(self, length: int):
        self.length = length
        self.sites = 2 * length
        self.dimension = 2 ** self.sites
        self.words = np.arange(self.dimension, dtype=np.uint32)
        self.counts = bit_counts(self.words, self.sites)
        self.edges = make_edges(length)
        self.pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for u, v, _ in self.edges:
            sources = np.flatnonzero(
                (((self.words >> u) & 1) == 1)
                & (((self.words >> v) & 1) == 0)
            ).astype(np.uint32)
            destinations = sources ^ np.uint32((1 << u) | (1 << v))
            self.pairs.append((sources, destinations))
        self.connectors = [i for i, edge in enumerate(self.edges) if edge[2] == "connector"]
        self.incidence = np.zeros((self.sites, len(self.edges)), dtype=float)
        for index, (u, v, _) in enumerate(self.edges):
            self.incidence[u, index] = 1.0
            self.incidence[v, index] = -1.0
        self.low = np.flatnonzero((self.words & 1) == 0).astype(np.uint32)
        self.high = self.low | np.uint32(1)

    def blank(self) -> np.ndarray:
        state = np.zeros(self.dimension, dtype=np.complex128)
        state[0] = 1.0
        return state

    def h(self, vector: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(vector)
        for source, destination in self.pairs:
            answer[source] -= vector[destination]
            answer[destination] -= vector[source]
        return answer

    def write(self, vector: np.ndarray) -> np.ndarray:
        answer = vector.copy()
        lo = vector[self.low]
        hi = vector[self.high]
        answer[self.low] = (lo - 1j * hi) / math.sqrt(2.0)
        answer[self.high] = (hi - 1j * lo) / math.sqrt(2.0)
        return answer

    def derivative(self, vector: np.ndarray) -> np.ndarray:
        return -1j * self.h(vector)

    def rk4(self, vector: np.ndarray, step: float) -> np.ndarray:
        k1 = self.derivative(vector)
        k2 = self.derivative(vector + 0.5 * step * k1)
        k3 = self.derivative(vector + 0.5 * step * k2)
        k4 = self.derivative(vector + step * k3)
        return vector + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def current(self, vector: np.ndarray) -> np.ndarray:
        answer = np.empty(len(self.pairs), dtype=float)
        for index, (source, destination) in enumerate(self.pairs):
            answer[index] = 2.0 * float(np.vdot(vector[source], vector[destination]).imag)
        return answer

    def evolve(self, vector: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray]:
        if steps % 2:
            raise ValueError("even Simpson grid required")
        step = KAPPA / steps
        state = vector.copy()
        current_sum = self.current(state)
        for index in range(1, steps + 1):
            state = self.rk4(state, step)
            weight = 1 if index == steps else (4 if index % 2 else 2)
            current_sum += weight * self.current(state)
        return state, current_sum * step / 3.0

    def occupations(self, vector: np.ndarray) -> np.ndarray:
        probability = np.real(np.conjugate(vector) * vector)
        return np.array([
            float(np.sum(probability[((self.words >> bit) & 1) != 0]))
            for bit in range(self.sites)
        ])

    def q(self, vector: np.ndarray) -> float:
        return float(np.dot(self.counts, np.real(np.conjugate(vector) * vector)))

    def sectors(self, vector: np.ndarray) -> np.ndarray:
        return np.bincount(
            self.counts,
            weights=np.real(np.conjugate(vector) * vector),
            minlength=self.sites + 1,
        ).astype(float)


def resolution(length: int, steps: int) -> dict[str, object]:
    carrier = BlindCarrier(length)
    state = carrier.blank()
    rows = []
    for event in range(1, 4 * length + 1):
        before = state
        occ_before = carrier.occupations(before)
        q_before = carrier.q(before)
        after_write = carrier.write(before)
        occ_write = carrier.occupations(after_write)
        q_write = carrier.q(after_write)
        write = q_write - q_before
        write_residual = occ_write - occ_before
        write_residual[0] -= write
        actual, currents = carrier.evolve(after_write, steps)
        null, null_currents = carrier.evolve(before, steps)
        occ_after = carrier.occupations(actual)
        event_residual = occ_after - occ_before + carrier.incidence @ currents
        event_residual[0] -= write
        delta = currents - null_currents
        weights = carrier.sectors(actual)
        q_after = carrier.q(actual)
        rows.append({
            "event": event,
            "W_n": write,
            "rho_bar": q_after / carrier.sites,
            "sector_weights": weights.tolist(),
            "connector_delta_l1": float(np.sum(np.abs(delta[carrier.connectors]))),
            "connector_delta_signed": float(np.sum(delta[carrier.connectors])),
            "event_residual_l1": float(np.sum(np.abs(event_residual))),
            "event_residual_linf": float(np.max(np.abs(event_residual))),
            "write_residual_l1": float(np.sum(np.abs(write_residual))),
            "norm_error": abs(float(np.vdot(actual, actual).real) - 1.0),
            "null_norm_error": abs(float(np.vdot(null, null).real) - 1.0),
            "number_transport_error": abs(q_after - q_write),
        })
        state = actual
    return {"state": state, "rows": rows, "dimension": carrier.dimension}


def crossing(values: np.ndarray, epsilon: float, level: float) -> int | None:
    for index in range(len(values) - 2):
        if all(float(value) + epsilon <= level for value in values[index:index + 3]):
            return index + 1
    return None


def mass_interval(weights: np.ndarray) -> tuple[int, int, float]:
    candidates = []
    for lower in range(len(weights)):
        running = 0.0
        for upper in range(lower, len(weights)):
            running += float(weights[upper])
            if running + 1.0e-15 >= MASS:
                candidates.append((upper - lower, -running, lower, upper))
                break
    if not candidates:
        raise AssertionError("missing probability mass")
    _, negative, lower, upper = min(candidates)
    return lower, upper, -negative


def analyze(length: int, coarse: dict[str, object], fine: dict[str, object]) -> dict[str, object]:
    cr = coarse["rows"]
    fr = fine["rows"]
    overlap = abs(np.vdot(coarse["state"], fine["state"]))
    projective = math.sqrt(max(0.0, 1.0 - min(1.0, float(overlap) ** 2)))
    write_error = max(abs(float(a["W_n"]) - float(b["W_n"])) for a, b in zip(cr, fr))
    rho_error = max(abs(float(a["rho_bar"]) - float(b["rho_bar"])) for a, b in zip(cr, fr))
    connector_error = max(abs(float(a["connector_delta_l1"]) - float(b["connector_delta_l1"])) for a, b in zip(cr, fr))
    sector_error = max(float(np.max(np.abs(np.array(a["sector_weights"]) - np.array(b["sector_weights"])))) for a, b in zip(cr, fr))
    disagreement = max(projective, write_error, rho_error, connector_error, sector_error)
    eps = max(1.0e-8, 50.0 * disagreement)
    writes = np.array([float(row["W_n"]) for row in fr])
    connectors = np.array([float(row["connector_delta_l1"]) for row in fr])
    if abs(writes[0]) <= 1.0e-14 or connectors[0] <= 1.0e-14:
        cw = np.full_like(writes, np.nan)
        cj = np.full_like(connectors, np.nan)
        capacity = np.full_like(writes, np.nan)
    else:
        cw = writes / writes[0]
        cj = connectors / connectors[0]
        capacity = np.minimum(np.maximum(cw, 0.0), cj)
    n75 = crossing(capacity, eps, 0.75) if np.all(np.isfinite(capacity)) else None
    n25 = crossing(capacity, eps, 0.25) if np.all(np.isfinite(capacity)) else None
    numerical = (
        disagreement <= 2.0e-7
        and max(float(row["event_residual_l1"]) for row in fr) <= max(1.0e-10, 100.0 * disagreement)
        and max(float(row["event_residual_linf"]) for row in fr) <= max(1.0e-11, 20.0 * disagreement)
        and max(float(row["norm_error"]) for row in fr) <= 1.0e-10
    )
    admitted = (
        numerical and n75 is not None and n25 is not None and n25 > n75
        and abs(float(capacity[0]) - 1.0) <= eps
        and np.all(writes[:3] > eps)
        and np.all(writes[:n25] >= -eps)
    )
    sector = None
    if admitted:
        selected = fr[n75 - 1:n25 + 2]
        pbar = np.mean(np.array([row["sector_weights"] for row in selected]), axis=0)
        low, high, enclosed = mass_interval(pbar)
        sector = {
            "n_075": n75,
            "n_025": n25,
            "pbar": pbar.tolist(),
            "q_lower": low,
            "q_upper": high,
            "enclosed_mass": enclosed,
            "density_interval": [max(0.0, (low - 0.5) / (2 * length)), min(1.0, (high + 0.5) / (2 * length))],
        }
    return {
        "classification": "BOUNDED_DEPLETION_WINDOW_L" if admitted else ("NO_BOUNDED_DEPLETION_WINDOW_L" if numerical else "UNRESOLVED_HISTORY_L"),
        "numerical_resolved": numerical,
        "admissible_depletion_window": admitted,
        "epsilon_capacity": eps,
        "c_W": cw.tolist(),
        "c_J": cj.tolist(),
        "capacity": capacity.tolist(),
        "n_075": n75,
        "n_025": n25,
        "sector": sector,
        "coarse_fine": {
            "state_projective_error": projective,
            "write_linf": write_error,
            "rho_linf": rho_error,
            "connector_delta_l1_linf": connector_error,
            "sector_weight_linf": sector_error,
            "maximum_disagreement": disagreement,
        },
    }


def worker(length: int, output: Path) -> None:
    started = time.perf_counter()
    coarse = resolution(length, COARSE_STEPS)
    fine = resolution(length, FINE_STEPS)
    result = {
        "schema": "BLIND_AUTHENTICATED_ACCUMULATION_HISTORY_ROW_V001",
        "L": length,
        "sites": 2 * length,
        "dimension": int(fine["dimension"]),
        "events": 4 * length,
        "edges": 3 * length,
        "connectors": length,
        "source_site": 0,
        "method": "INDEPENDENT_DISJOINT_PAIR_RK4_SIMPSON",
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
        "fine_rows": fine["rows"],
        "comparison": analyze(length, coarse, fine),
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "claim_boundary": "FINITE_HISTORY_RECONSTRUCTION_ONLY",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"BLIND_L{length}", result["comparison"]["classification"], f"wall={result['wall_seconds']:.3f}s")


def aggregate() -> None:
    rows = [json.loads((RAW / f"HISTORY_L{length}.json").read_text()) for length in SIZES]
    resolved = all(row["comparison"]["numerical_resolved"] for row in rows)
    windows = all(row["comparison"]["admissible_depletion_window"] for row in rows)
    common = None
    if windows:
        lower = max(float(row["comparison"]["sector"]["density_interval"][0]) for row in rows)
        upper = min(float(row["comparison"]["sector"]["density_interval"][1]) for row in rows)
        if lower < upper:
            common = [lower, upper]
    classification = (
        "UNRESOLVED_AUTHENTICATED_ACCUMULATION_SEED_L4_L8"
        if not resolved
        else ("SEED_ACCUMULATION_SECTOR_L4_L8" if common is not None else "NO_COMMON_ACCUMULATION_SECTOR_L4_L8")
    )
    result = {
        "schema": "BLIND_AUTHENTICATED_ACCUMULATION_HISTORY_SEED_V001",
        "classification": classification,
        "protocol_sha256": digest(PROTOCOL),
        "implementation_sha256": digest(Path(__file__)),
        "rows": rows,
        "common_density_interval": common,
        "next_gate": "AUTHORIZE_L10_L12_HISTORY" if common is not None else "HALT_BEFORE_L10_L12_AND_SPECTRUM",
        "claim_boundary": "FINITE_HISTORY_SEED_ONLY",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(classification)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--L", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--aggregate", action="store_true")
    args = parser.parse_args()
    if args.worker:
        if args.L is None or args.output is None:
            parser.error("worker needs L and output")
        worker(args.L, args.output)
    elif args.aggregate:
        aggregate()
    else:
        parser.error("choose worker or aggregate")
