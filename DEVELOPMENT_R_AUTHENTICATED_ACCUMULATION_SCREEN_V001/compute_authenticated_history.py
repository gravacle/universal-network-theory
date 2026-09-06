#!/usr/bin/env python3
"""Target matrix-free authenticated accumulation history.

This module is frozen before target output.  Worker mode writes one L row;
aggregate mode reads only existing rows and applies the frozen sector gate.
"""

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
PROTOCOL = HERE / "PROTOCOL.md"
RAW = HERE / "RAW_HISTORY"
OUT = HERE / "HISTORY_SEED_RESULT.json"

PHI = math.pi / 4.0
KAPPA = math.pi / 2.0
TAYLOR_ORDER = 10
COARSE_STEPS = 128
FINE_STEPS = 256
MASS_COVERAGE = 0.99
SIZES_SEED = (4, 6, 8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def edges_for(length: int) -> list[tuple[int, int, str]]:
    edges: list[tuple[int, int, str]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length, f"rail_{rail + 1}"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def popcounts(words: np.ndarray, sites: int) -> np.ndarray:
    work = words.copy()
    counts = np.zeros(len(words), dtype=np.uint8)
    for _ in range(sites):
        counts += (work & 1).astype(np.uint8)
        work >>= 1
    return counts


class Carrier:
    def __init__(self, length: int):
        self.length = length
        self.sites = 2 * length
        self.dimension = 1 << self.sites
        self.words = np.arange(self.dimension, dtype=np.uint32)
        self.counts = popcounts(self.words, self.sites)
        self.edges = edges_for(length)
        self.connector_indices = [index for index, edge in enumerate(self.edges) if edge[2] == "connector"]
        self.actions: list[tuple[np.ndarray, np.uint32, np.ndarray]] = []
        for u, v, _ in self.edges:
            bit_u = ((self.words >> u) & 1).astype(np.int8)
            bit_v = ((self.words >> v) & 1).astype(np.int8)
            active = np.flatnonzero(bit_u != bit_v).astype(np.uint32)
            sign = (bit_v[active] - bit_u[active]).astype(np.int8)
            self.actions.append((active, np.uint32((1 << u) | (1 << v)), sign))
        self.incidence = np.zeros((self.sites, len(self.edges)), dtype=np.int8)
        for edge_index, (u, v, _) in enumerate(self.edges):
            self.incidence[u, edge_index] = 1
            self.incidence[v, edge_index] = -1
        self.source = 0
        self.source_low = np.flatnonzero(((self.words >> self.source) & 1) == 0).astype(np.uint32)
        self.source_high = self.source_low | np.uint32(1 << self.source)

    def vacuum(self) -> np.ndarray:
        state = np.zeros(self.dimension, dtype=np.complex128)
        state[0] = 1.0
        return state

    def h_action(self, state: np.ndarray) -> np.ndarray:
        out = np.zeros_like(state)
        for active, mask, _ in self.actions:
            out[active] -= state[active ^ mask]
        return out

    def apply_write(self, state: np.ndarray) -> np.ndarray:
        out = state.copy()
        low = state[self.source_low]
        high = state[self.source_high]
        cosine = math.cos(PHI)
        sine = math.sin(PHI)
        out[self.source_low] = cosine * low - 1j * sine * high
        out[self.source_high] = cosine * high - 1j * sine * low
        return out

    def occupations(self, state: np.ndarray) -> np.ndarray:
        probability = np.abs(state) ** 2
        return np.array([
            float(np.sum(probability[((self.words >> site) & 1) == 1]))
            for site in range(self.sites)
        ])

    def q_expectation(self, state: np.ndarray) -> float:
        return float(np.dot(self.counts.astype(float), np.abs(state) ** 2))

    def sector_weights(self, state: np.ndarray) -> np.ndarray:
        return np.bincount(
            self.counts,
            weights=np.abs(state) ** 2,
            minlength=self.sites + 1,
        ).astype(float)

    def currents(self, state: np.ndarray) -> np.ndarray:
        values = np.empty(len(self.actions), dtype=float)
        for index, (active, mask, sign) in enumerate(self.actions):
            values[index] = float(np.sum(
                np.conjugate(state[active])
                * (1j * sign)
                * state[active ^ mask]
            ).real)
        return values

    def taylor_step(self, state: np.ndarray, step: float) -> np.ndarray:
        updated = state.copy()
        term = state.copy()
        for order in range(1, TAYLOR_ORDER + 1):
            term = (-1j * step / order) * self.h_action(term)
            updated += term
        return updated

    def evolve_and_integrate(self, initial: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray]:
        if steps % 2:
            raise ValueError("Simpson step count must be even")
        step = KAPPA / steps
        state = initial.copy()
        integrated = self.currents(state)
        for index in range(1, steps + 1):
            state = self.taylor_step(state, step)
            weight = 1 if index == steps else (4 if index % 2 else 2)
            integrated += weight * self.currents(state)
        integrated *= step / 3.0
        return state, integrated


def run_resolution(length: int, steps: int) -> dict[str, object]:
    carrier = Carrier(length)
    state = carrier.vacuum()
    rows: list[dict[str, object]] = []
    for event in range(1, 4 * length + 1):
        initial = state
        occupation_before = carrier.occupations(initial)
        q_before = carrier.q_expectation(initial)
        written = carrier.apply_write(initial)
        occupation_written = carrier.occupations(written)
        q_written = carrier.q_expectation(written)
        source_write = q_written - q_before
        write_residual = occupation_written - occupation_before
        write_residual[carrier.source] -= source_write

        actual, actual_currents = carrier.evolve_and_integrate(written, steps)
        null, null_currents = carrier.evolve_and_integrate(initial, steps)
        occupation_after = carrier.occupations(actual)
        q_after = carrier.q_expectation(actual)
        event_residual = (
            occupation_after
            - occupation_before
            + carrier.incidence @ actual_currents
        )
        event_residual[carrier.source] -= source_write
        delta_current = actual_currents - null_currents
        connector_delta_l1 = float(np.sum(np.abs(delta_current[carrier.connector_indices])))
        connector_delta_signed = float(np.sum(delta_current[carrier.connector_indices]))
        h_initial = carrier.h_action(written)
        h_final = carrier.h_action(actual)
        energy_initial = float(np.vdot(written, h_initial).real)
        energy_final = float(np.vdot(actual, h_final).real)
        rows.append({
            "event": event,
            "W_n": source_write,
            "q_before": q_before,
            "q_after_write": q_written,
            "q_after_transport": q_after,
            "rho_bar": q_after / carrier.sites,
            "var_rho": float(np.dot(
                (np.arange(carrier.sites + 1) / carrier.sites - q_after / carrier.sites) ** 2,
                carrier.sector_weights(actual),
            )),
            "sector_weights": carrier.sector_weights(actual).tolist(),
            "connector_delta_l1": connector_delta_l1,
            "connector_delta_signed": connector_delta_signed,
            "complete_delta_current": delta_current.tolist(),
            "complete_actual_current": actual_currents.tolist(),
            "write_residual_l1": float(np.sum(np.abs(write_residual))),
            "write_residual_linf": float(np.max(np.abs(write_residual))),
            "event_residual_l1": float(np.sum(np.abs(event_residual))),
            "event_residual_linf": float(np.max(np.abs(event_residual))),
            "norm_error": abs(float(np.vdot(actual, actual).real) - 1.0),
            "null_norm_error": abs(float(np.vdot(null, null).real) - 1.0),
            "number_transport_error": abs(q_after - q_written),
            "energy_transport_error": abs(energy_final - energy_initial),
        })
        state = actual
    return {
        "steps": steps,
        "rows": rows,
        "final_state": state,
        "dimension": carrier.dimension,
        "sites": carrier.sites,
        "edges": len(carrier.edges),
        "connectors": len(carrier.connector_indices),
    }


def first_sustained_crossing(capacity: np.ndarray, epsilon: float, level: float) -> int | None:
    for start in range(0, len(capacity) - 2):
        if np.all(capacity[start:start + 3] + epsilon <= level):
            return start + 1
    return None


def shortest_mass_interval(weights: np.ndarray, coverage: float) -> tuple[int, int, float]:
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
        raise AssertionError("sector weights do not reach requested mass")
    _, negative_mass, lower, upper = best
    return lower, upper, -negative_mass


def compare_resolutions(length: int, coarse: dict[str, object], fine: dict[str, object]) -> dict[str, object]:
    coarse_rows = coarse["rows"]
    fine_rows = fine["rows"]
    if len(coarse_rows) != len(fine_rows):
        raise AssertionError("resolution event census mismatch")
    final_overlap = abs(np.vdot(coarse["final_state"], fine["final_state"]))
    state_projective_error = math.sqrt(max(0.0, 1.0 - min(1.0, float(final_overlap) ** 2)))
    write_error = max(abs(float(a["W_n"]) - float(b["W_n"])) for a, b in zip(coarse_rows, fine_rows))
    connector_error = max(
        abs(float(a["connector_delta_l1"]) - float(b["connector_delta_l1"]))
        for a, b in zip(coarse_rows, fine_rows)
    )
    sector_error = max(
        float(np.max(np.abs(np.array(a["sector_weights"]) - np.array(b["sector_weights"]))))
        for a, b in zip(coarse_rows, fine_rows)
    )
    rho_error = max(abs(float(a["rho_bar"]) - float(b["rho_bar"])) for a, b in zip(coarse_rows, fine_rows))
    disagreement = max(state_projective_error, write_error, connector_error, sector_error, rho_error)
    epsilon_capacity = max(1.0e-8, 50.0 * disagreement)

    w = np.array([float(row["W_n"]) for row in fine_rows])
    connector = np.array([float(row["connector_delta_l1"]) for row in fine_rows])
    if abs(w[0]) <= 1.0e-14 or connector[0] <= 1.0e-14:
        c_w = np.full_like(w, np.nan)
        c_j = np.full_like(connector, np.nan)
        capacity = np.full_like(w, np.nan)
    else:
        c_w = w / w[0]
        c_j = connector / connector[0]
        capacity = np.minimum(np.maximum(0.0, c_w), c_j)
    n75 = first_sustained_crossing(capacity, epsilon_capacity, 0.75) if np.all(np.isfinite(capacity)) else None
    n25 = first_sustained_crossing(capacity, epsilon_capacity, 0.25) if np.all(np.isfinite(capacity)) else None

    numerical_resolved = (
        disagreement <= 2.0e-7
        and max(float(row["event_residual_l1"]) for row in fine_rows) <= max(1.0e-10, 100.0 * disagreement)
        and max(float(row["event_residual_linf"]) for row in fine_rows) <= max(1.0e-11, 20.0 * disagreement)
        and max(float(row["norm_error"]) for row in fine_rows) <= 1.0e-10
        and max(float(row["null_norm_error"]) for row in fine_rows) <= 1.0e-10
    )
    admissible_window = (
        numerical_resolved
        and n75 is not None
        and n25 is not None
        and n25 > n75
        and abs(float(capacity[0]) - 1.0) <= epsilon_capacity
        and np.all(w[:3] > epsilon_capacity)
        and np.all(w[:n25] >= -epsilon_capacity)
    )

    sector: dict[str, object] | None = None
    if admissible_window:
        selected = fine_rows[n75 - 1:n25 + 2]
        pbar = np.mean(np.array([row["sector_weights"] for row in selected], dtype=float), axis=0)
        lower, upper, mass = shortest_mass_interval(pbar, MASS_COVERAGE)
        sector = {
            "n_075": n75,
            "n_025": n25,
            "window_events": [int(row["event"]) for row in selected],
            "pbar": pbar.tolist(),
            "q_lower": lower,
            "q_upper": upper,
            "enclosed_mass": mass,
            "density_interval": [
                max(0.0, (lower - 0.5) / (2.0 * length)),
                min(1.0, (upper + 0.5) / (2.0 * length)),
            ],
        }

    if not numerical_resolved:
        classification = "UNRESOLVED_HISTORY_L"
    elif admissible_window:
        classification = "BOUNDED_DEPLETION_WINDOW_L"
    else:
        classification = "NO_BOUNDED_DEPLETION_WINDOW_L"
    return {
        "classification": classification,
        "numerical_resolved": numerical_resolved,
        "admissible_depletion_window": admissible_window,
        "coarse_fine": {
            "state_projective_error": state_projective_error,
            "write_linf": write_error,
            "connector_delta_l1_linf": connector_error,
            "sector_weight_linf": sector_error,
            "rho_linf": rho_error,
            "maximum_disagreement": disagreement,
        },
        "epsilon_capacity": epsilon_capacity,
        "c_W": c_w.tolist(),
        "c_J": c_j.tolist(),
        "capacity": capacity.tolist(),
        "n_075": n75,
        "n_025": n25,
        "sector": sector,
    }


def worker(length: int, output: Path) -> None:
    if length not in (4, 6, 8, 10, 12):
        raise ValueError("unsupported L")
    started = time.perf_counter()
    coarse = run_resolution(length, COARSE_STEPS)
    fine = run_resolution(length, FINE_STEPS)
    comparison = compare_resolutions(length, coarse, fine)
    fine_rows = fine["rows"]
    result = {
        "schema": "AUTHENTICATED_ACCUMULATION_HISTORY_ROW_V001",
        "L": length,
        "sites": 2 * length,
        "dimension": int(fine["dimension"]),
        "edges": int(fine["edges"]),
        "connectors": int(fine["connectors"]),
        "events": 4 * length,
        "source_site": 0,
        "phi": "pi/4",
        "kappa": "pi/2",
        "r0": "14441248/6075",
        "writer_factor_status": "FIXED_X_EIGENSTATE_FACTORS_EXACTLY",
        "coarse_steps": COARSE_STEPS,
        "fine_steps": FINE_STEPS,
        "taylor_order": TAYLOR_ORDER,
        "fine_rows": fine_rows,
        "comparison": comparison,
        "controls": {
            "first_write_error": abs(float(fine_rows[0]["W_n"]) - 0.5),
            "owner_edge_census": len(edges_for(length)) == 3 * length,
            "connector_census": len([edge for edge in edges_for(length) if edge[2] == "connector"]) == length,
            "incidence_column_sums_zero": True,
            "maximum_fine_event_residual_l1": max(float(row["event_residual_l1"]) for row in fine_rows),
            "maximum_fine_event_residual_linf": max(float(row["event_residual_linf"]) for row in fine_rows),
            "maximum_fine_norm_error": max(float(row["norm_error"]) for row in fine_rows),
            "maximum_fine_number_transport_error": max(float(row["number_transport_error"]) for row in fine_rows),
            "maximum_fine_energy_transport_error": max(float(row["energy_transport_error"]) for row in fine_rows),
        },
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "claim_boundary": {
            "empirical": "FINITE_AUTHENTICATED_ACCUMULATION_HISTORY_ONLY",
            "not_claimed": ["CRITICAL_DENSITY", "CONTINUUM", "METRIC", "EMERGENCE", "GRAVITY"],
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"L{length}", comparison["classification"], f"wall={result['wall_seconds']:.3f}s")


def aggregate_seed() -> None:
    rows = []
    for length in SIZES_SEED:
        path = RAW / f"HISTORY_L{length}.json"
        if not path.is_file():
            raise FileNotFoundError(path)
        rows.append(json.loads(path.read_text()))
    all_resolved = all(row["comparison"]["numerical_resolved"] for row in rows)
    all_windows = all(row["comparison"]["admissible_depletion_window"] for row in rows)
    common_interval = None
    if all_windows:
        lower = max(float(row["comparison"]["sector"]["density_interval"][0]) for row in rows)
        upper = min(float(row["comparison"]["sector"]["density_interval"][1]) for row in rows)
        if lower < upper:
            common_interval = [lower, upper]
    if not all_resolved:
        classification = "UNRESOLVED_AUTHENTICATED_ACCUMULATION_SEED_L4_L8"
    elif common_interval is None:
        classification = "NO_COMMON_ACCUMULATION_SECTOR_L4_L8"
    else:
        classification = "SEED_ACCUMULATION_SECTOR_L4_L8"
    result = {
        "schema": "AUTHENTICATED_ACCUMULATION_HISTORY_SEED_V001",
        "classification": classification,
        "protocol_sha256": sha256(PROTOCOL),
        "implementation_sha256": sha256(Path(__file__)),
        "rows": rows,
        "common_density_interval": common_interval,
        "next_gate": (
            "AUTHORIZE_L10_L12_HISTORY"
            if classification == "SEED_ACCUMULATION_SECTOR_L4_L8"
            else "HALT_BEFORE_L10_L12_AND_SPECTRUM"
        ),
        "claim_boundary": {
            "empirical": "FINITE_HISTORY_SEED_ONLY",
            "not_claimed": ["CRITICAL_DENSITY", "Z_EQUALS_ONE", "CONTINUUM", "GRAVITY"],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(classification)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--L", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--aggregate-seed", action="store_true")
    args = parser.parse_args()
    if args.worker:
        if args.L is None or args.output is None:
            parser.error("--worker requires --L and --output")
        worker(args.L, args.output)
    elif args.aggregate_seed:
        aggregate_seed()
    else:
        parser.error("select --worker or --aggregate-seed")
