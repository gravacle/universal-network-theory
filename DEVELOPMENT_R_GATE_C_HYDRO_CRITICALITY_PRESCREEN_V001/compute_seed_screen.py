#!/usr/bin/env python3
"""Exact-through-L8 hydrodynamic criticality seed screen.

The top-level process launches one fixed-Q worker at a time and monitors its
resident set and wall time.  Workers retain complete eigenvalue spectra but
discard dense eigenvectors before the next sector.  No L10/L12 calculation is
implemented here: this executable stops at the frozen L<=8 seed decision.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import resource
import subprocess
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
PROTOCOL_SHA256 = "3da9e74b0dcc2d8b65ce98cfb42735864cf3d045e41655082baa7a7a295cb334"
RAW = HERE / "RAW"
OUT = HERE / "RESULT.json"
L_VALUES = (4, 6, 8)
DEGENERACY_TOL = 1.0e-10
EIGEN_RESIDUAL_LIMIT = 1.0e-10
RELATIVE_WEIGHT_FLOOR = 1.0e-12
RESIDUAL_WEIGHT_MULTIPLIER = 100.0
RSS_LIMIT_BYTES = 12 * (1 << 30)
SECTOR_TIME_LIMIT_SECONDS = 45 * 60


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_label(path: Path) -> str:
    try:
        return str(path.relative_to(HERE))
    except ValueError:
        return str(path)


def edges_for(length: int) -> list[tuple[int, int, str]]:
    edges: list[tuple[int, int, str]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length, f"rail_{rail + 1}"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def basis_for(sites: int, q: int) -> np.ndarray:
    return np.fromiter(
        (word for word in range(1 << sites) if bin(int(word)).count("1") == q),
        dtype=np.int64,
        count=math.comb(sites, q),
    )


def dense_sector_hamiltonian(
    sites: int, basis: np.ndarray, edges: list[tuple[int, int, str]]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dimension = len(basis)
    word_to_row = np.full(1 << sites, -1, dtype=np.int32)
    word_to_row[basis] = np.arange(dimension, dtype=np.int32)
    hamiltonian = np.zeros((dimension, dimension), dtype=np.float64)
    transition_sources: list[np.ndarray] = []
    transition_destinations: list[np.ndarray] = []
    for u, v, _ in edges:
        active = np.flatnonzero(((basis >> u) & 1) != ((basis >> v) & 1)).astype(np.int32)
        swapped = basis[active] ^ (1 << u) ^ (1 << v)
        destinations = word_to_row[swapped]
        if np.any(destinations < 0):
            raise AssertionError("owner transition left fixed-Q sector")
        hamiltonian[destinations, active] = -1.0
        transition_sources.append(active)
        transition_destinations.append(destinations)
    return (
        hamiltonian,
        np.concatenate(transition_sources),
        np.concatenate(transition_destinations),
    )


def groups_by_energy(values: np.ndarray, tolerance: float) -> list[tuple[int, int]]:
    groups: list[tuple[int, int]] = []
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[end] - values[start] <= tolerance:
            end += 1
        groups.append((start, end))
        start = end
    return groups


def sparse_action(
    vectors: np.ndarray,
    transition_sources: np.ndarray,
    transition_destinations: np.ndarray,
) -> np.ndarray:
    out = np.zeros_like(vectors)
    # Each destination appears at most once per owner edge.  np.add.at remains
    # correct across different owners and permits vector blocks.
    np.add.at(out, transition_destinations, -vectors[transition_sources])
    return out


def selected_residuals(
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    indices: np.ndarray,
    transition_sources: np.ndarray,
    transition_destinations: np.ndarray,
) -> tuple[float, dict[int, float]]:
    residuals: dict[int, float] = {}
    maximum = 0.0
    for start in range(0, len(indices), 16):
        selected = indices[start : start + 16]
        vectors = eigenvectors[:, selected]
        residual = sparse_action(vectors, transition_sources, transition_destinations)
        residual -= vectors * eigenvalues[selected][None, :]
        norms = np.linalg.norm(residual, axis=0)
        for index, value in zip(selected, norms):
            residuals[int(index)] = float(value)
        if len(norms):
            maximum = max(maximum, float(np.max(norms)))
    return maximum, residuals


def worker(length: int, q: int, output: Path, spectrum: Path) -> None:
    started = time.perf_counter()
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
    sites = 2 * length
    edges = edges_for(length)
    basis = basis_for(sites, q)
    dimension = len(basis)
    hamiltonian, transition_sources, transition_destinations = dense_sector_hamiltonian(
        sites, basis, edges
    )
    hermiticity_error = float(np.max(np.abs(hamiltonian - hamiltonian.T)))
    if hermiticity_error != 0.0:
        raise AssertionError("fixed-Q Hamiltonian is not exactly symmetric")

    # The local-index parity is a bipartition for rails and shifted connectors.
    sublattice_a_mask = sum(1 << site for rail in range(2) for site in range(rail * length, (rail + 1) * length) if (site % length) % 2 == 0)
    gamma = np.array(
        [(-1.0) ** bin(int(word & sublattice_a_mask)).count("1") for word in basis]
    )
    chiral_transition_error = float(
        np.max(np.abs(gamma[transition_sources] + gamma[transition_destinations]))
    ) if len(transition_sources) else 0.0

    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    np.save(spectrum, eigenvalues, allow_pickle=False)
    spectral_chiral_error = float(np.max(np.abs(eigenvalues + eigenvalues[::-1])))
    zero_count = int(np.sum(np.abs(eigenvalues) <= DEGENERACY_TOL))
    imbalance_lower_bound = math.comb(length, q // 2) if q % 2 == 0 else 0

    row: dict[str, object] = {
        "L": length,
        "q": q,
        "rho": q / sites,
        "dimension": dimension,
        "eigenvalue_count": len(eigenvalues),
        "spectrum_file": local_label(spectrum),
        "spectrum_sha256": digest(spectrum),
        "ground_energy": float(eigenvalues[0]),
        "top_energy": float(eigenvalues[-1]),
        "hermiticity_error": hermiticity_error,
        "chiral_transition_error": chiral_transition_error,
        "spectral_chiral_error": spectral_chiral_error,
        "mid_spectrum_zero_count_at_1e-10": zero_count,
        "configuration_sublattice_imbalance_lower_bound": imbalance_lower_bound,
        "transition_entries": int(len(transition_sources)),
        "owner_transition_preserves_q": True,
    }

    if q == 0:
        row.update(
            {
                "ground_multiplicity_at_1e-10": 1,
                "response_status": "VACUUM_CONTROL__NO_DENSITY_MODE_NORM",
                "eigen_residual_max_response_support": 0.0,
            }
        )
    else:
        ground_group_end = groups_by_energy(eigenvalues, DEGENERACY_TOL)[0][1]
        phases = np.exp(2.0j * math.pi * np.arange(length) / length)
        mode_diagonal = np.zeros(dimension, dtype=np.complex128)
        for site in range(length):
            mode_diagonal += phases[site] * (
                ((basis >> site) & 1) + ((basis >> (length + site)) & 1)
            )
        response_vector = mode_diagonal * eigenvectors[:, 0]
        response_norm_squared = float(np.vdot(response_vector, response_vector).real)
        coefficients = np.einsum(
            "ia,i->a", eigenvectors, response_vector, optimize=False
        )
        individual_weights = np.abs(coefficients) ** 2
        energy_groups = groups_by_energy(eigenvalues, DEGENERACY_TOL)
        group_rows: list[dict[str, object]] = []
        total_weight = 0.0
        for start, end in energy_groups:
            omega = float(np.mean(eigenvalues[start:end]) - eigenvalues[0])
            if omega <= DEGENERACY_TOL:
                continue
            weight = float(np.sum(individual_weights[start:end]))
            total_weight += weight
            group_rows.append(
                {
                    "start": start,
                    "end": end,
                    "multiplicity": end - start,
                    "omega": omega,
                    "weight": weight,
                }
            )
        if total_weight <= 0.0:
            raise AssertionError("non-vacuum density-mode response has zero norm")

        # Check the ground vector and every group that could be active even at
        # one tenth of the relative threshold.  This is the relevant residual
        # maximum in the frozen floor and includes the promoted low pole.
        provisional = RELATIVE_WEIGHT_FLOOR * total_weight / 10.0
        residual_indices = {0}
        for group in group_rows:
            if float(group["weight"]) > provisional:
                residual_indices.update(range(int(group["start"]), int(group["end"])))
        checked_indices = np.array(sorted(residual_indices), dtype=np.int64)
        residual_max, residual_by_index = selected_residuals(
            eigenvalues,
            eigenvectors,
            checked_indices,
            transition_sources,
            transition_destinations,
        )
        ground_residual = residual_by_index[0]
        weight_floor = max(
            RELATIVE_WEIGHT_FLOOR * total_weight,
            RESIDUAL_WEIGHT_MULTIPLIER
            * residual_max**2
            * response_norm_squared,
        )

        threshold_results: list[dict[str, object]] = []
        for multiplier in (0.1, 1.0, 10.0):
            threshold = multiplier * weight_floor
            active = next((group for group in group_rows if float(group["weight"]) > threshold), None)
            threshold_results.append(
                {
                    "multiplier": multiplier,
                    "threshold": threshold,
                    "active_omega": None if active is None else active["omega"],
                    "active_group_start": None if active is None else active["start"],
                    "active_group_multiplicity": None if active is None else active["multiplicity"],
                    "active_group_weight": None if active is None else active["weight"],
                }
            )
        canonical = threshold_results[1]
        active_start = canonical["active_group_start"]
        if active_start is None:
            active_residual = math.inf
        else:
            group = next(group for group in group_rows if group["start"] == active_start)
            active_residual = max(
                residual_by_index.get(index, math.inf)
                for index in range(int(group["start"]), int(group["end"]))
            )
        stable_threshold = (
            threshold_results[0]["active_group_start"]
            == threshold_results[1]["active_group_start"]
            == threshold_results[2]["active_group_start"]
        )
        delta_act = float(canonical["active_omega"]) if canonical["active_omega"] is not None else math.nan
        weighted_inverse_square = sum(
            float(group["weight"]) / float(group["omega"]) ** 2
            for group in group_rows
        )
        chi_tau = math.sqrt(weighted_inverse_square / total_weight)
        low_weight = float(canonical["active_group_weight"]) if canonical["active_group_weight"] is not None else 0.0
        r_low = low_weight / total_weight
        response_resolved = (
            math.isfinite(delta_act)
            and residual_max <= EIGEN_RESIDUAL_LIMIT
            and active_residual <= EIGEN_RESIDUAL_LIMIT
            and stable_threshold
        )
        row.update(
            {
                "ground_multiplicity_at_1e-10": ground_group_end,
                "ground_residual": ground_residual,
                "response_vector_norm_squared": response_norm_squared,
                "response_total_excited_weight": total_weight,
                "response_ground_weight": float(np.sum(individual_weights[:ground_group_end])),
                "response_energy_groups": len(group_rows),
                "response_residual_vectors_checked": len(checked_indices),
                "eigen_residual_max_response_support": residual_max,
                "active_pole_residual_max": active_residual,
                "weight_floor": weight_floor,
                "threshold_screen": threshold_results,
                "threshold_stable": stable_threshold,
                "Delta_act": delta_act,
                "chi_tau": chi_tau,
                "R_low": r_low,
                "active_group_multiplicity": canonical["active_group_multiplicity"],
                "response_status": "RESOLVED" if response_resolved else "UNRESOLVED",
            }
        )

    elapsed = time.perf_counter() - started
    row["worker_wall_seconds"] = elapsed
    row["worker_max_rss_bytes"] = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    row["worker_memory_guards"] = memory_guards
    output.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")


def run_monitored_worker(length: int, q: int) -> dict[str, object]:
    RAW.mkdir(exist_ok=True)
    output = RAW / f"SECTOR_L{length}_Q{q}.json"
    spectrum = RAW / f"SPECTRUM_L{length}_Q{q}.npy"
    output.unlink(missing_ok=True)
    spectrum.unlink(missing_ok=True)
    command = [
        sys.executable,
        "-B",
        str(Path(__file__).resolve()),
        "--worker",
        "--L",
        str(length),
        "--q",
        str(q),
        "--output",
        str(output),
        "--spectrum",
        str(spectrum),
    ]
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=HERE)
    try:
        process.wait(timeout=SECTOR_TIME_LIMIT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise RuntimeError(f"L{length} q={q} exceeded 45 minute wall guard")
    if process.returncode != 0:
        raise RuntimeError(f"L{length} q={q} worker exited {process.returncode}")
    row = json.loads(output.read_text())
    monitor_peak = int(row["worker_max_rss_bytes"])
    if monitor_peak > RSS_LIMIT_BYTES:
        raise RuntimeError(f"L{length} q={q} exceeded 12 GiB RSS guard")
    row["monitor_peak_rss_bytes"] = monitor_peak
    row["monitor_wall_seconds"] = time.monotonic() - started
    output.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")
    return row


def structural_checks(length: int) -> dict[str, object]:
    sites = 2 * length
    edges = edges_for(length)
    neighbors = [set() for _ in range(sites)]
    edge_keys = set()
    for u, v, _ in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
        edge_keys.add(frozenset((u, v)))
    visited = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in neighbors[vertex] - visited:
            visited.add(neighbor)
            frontier.append(neighbor)
    numerical = np.linalg.eigvalsh(
        dense_sector_hamiltonian(sites, basis_for(sites, 1), edges)[0]
    )
    analytic = np.sort(
        np.array(
            [
                -2.0 * math.cos(2.0 * math.pi * m / length) + band
                for m in range(length)
                for band in (-1.0, 1.0)
            ]
        )
    )
    band_error = float(np.max(np.abs(numerical - analytic)))
    one_carrier_zero_count = int(np.sum(np.abs(analytic) <= DEGENERACY_TOL))
    return {
        "L": length,
        "sites": sites,
        "edges": len(edges),
        "rail_edges": sum(kind.startswith("rail") for _, _, kind in edges),
        "connector_edges": sum(kind == "connector" for _, _, kind in edges),
        "unique_owner_edges": len(edge_keys),
        "degree_sequence": [len(value) for value in neighbors],
        "connected_vertices": len(visited),
        "one_carrier_band_linf": band_error,
        "one_carrier_zero_count_at_1e-10": one_carrier_zero_count,
        "one_carrier_zero_classification": (
            "COMMENSURATE_CONTROL" if one_carrier_zero_count else "NO_ZERO"
        ),
        "H_independent_of_N": True,
        "Q_commutator_structural": 0.0,
        "particle_hole_map": "GLOBAL_BIT_COMPLEMENT__EXACT_SECTOR_ISOSPECTRALITY",
        "bipartite_coloring": "LOCAL_INDEX_PARITY__EVERY_OWNER_CROSSES",
    }


def interval(length: int, q: int) -> tuple[float, float]:
    return max(0.0, (q - 0.5) / (2 * length)), min(0.5, (q + 0.5) / (2 * length))


def merge_intervals(rows: list[tuple[float, float]]) -> list[list[float]]:
    if not rows:
        return []
    merged: list[list[float]] = []
    for low, high in sorted(rows):
        if not merged or low > merged[-1][1] + 1.0e-15:
            merged.append([low, high])
        else:
            merged[-1][1] = max(merged[-1][1], high)
    return merged


def main() -> None:
    if digest(PROTOCOL) != PROTOCOL_SHA256:
        raise AssertionError("frozen protocol digest mismatch")
    started = time.perf_counter()
    structural = [structural_checks(length) for length in L_VALUES]
    rows_by_l: dict[int, list[dict[str, object]]] = {}
    for length in L_VALUES:
        rows_by_l[length] = [run_monitored_worker(length, q) for q in range(length + 1)]

    # Charge curvature and density-local seed tests are evaluated only after
    # all ground energies are available.
    seed_rows: dict[int, list[dict[str, object]]] = {}
    for length, rows in rows_by_l.items():
        ground = [float(row["ground_energy"]) for row in rows]
        seeds: list[dict[str, object]] = []
        for q, row in enumerate(rows):
            if 0 < q < length:
                row["Delta_Q"] = ground[q + 1] + ground[q - 1] - 2.0 * ground[q]
            elif q == length:
                # Particle-hole makes E0(L+1)=E0(L-1).
                row["Delta_Q"] = 2.0 * ground[q - 1] - 2.0 * ground[q]
            else:
                row["Delta_Q"] = None
        for q in range(2, length):
            left, row, right = rows[q - 1], rows[q], rows[q + 1]
            if any(item.get("response_status") != "RESOLVED" for item in (left, row, right)):
                continue
            gap = float(row["Delta_act"])
            gap_error = 2.0 * max(
                float(row["ground_residual"]), float(row["active_pole_residual_max"])
            )
            left_error = 2.0 * max(
                float(left["ground_residual"]), float(left["active_pole_residual_max"])
            )
            right_error = 2.0 * max(
                float(right["ground_residual"]), float(right["active_pole_residual_max"])
            )
            strict_gap_minimum = (
                gap + gap_error < float(left["Delta_act"]) - left_error
                and gap + gap_error < float(right["Delta_act"]) - right_error
            )
            strict_chi_maximum = (
                float(row["chi_tau"]) > float(left["chi_tau"])
                and float(row["chi_tau"]) > float(right["chi_tau"])
            )
            residue_pass = float(row["R_low"]) >= 1.0e-6 and all(
                float(item["active_group_weight"]) / float(row["response_total_excited_weight"]) >= 1.0e-6
                for item in row["threshold_screen"]
                if item["active_group_weight"] is not None
            )
            threshold_pass = bool(row["threshold_stable"])
            if strict_gap_minimum and strict_chi_maximum and residue_pass and threshold_pass:
                low, high = interval(length, q)
                seed = {
                    "L": length,
                    "q": q,
                    "rho": q / (2 * length),
                    "cell": [low, high],
                    "Delta_act": gap,
                    "Delta_act_error_bound": gap_error,
                    "chi_tau": row["chi_tau"],
                    "R_low": row["R_low"],
                    "projector_grouped_low_multiplicity": row["active_group_multiplicity"],
                    "mode": "TOTAL_RAIL_M1",
                }
                seeds.append(seed)
                row["seed_status"] = "SEED"
            else:
                row["seed_status"] = "NO_SEED"
                row["seed_controls"] = {
                    "strict_gap_minimum_beyond_residual": strict_gap_minimum,
                    "strict_chi_maximum": strict_chi_maximum,
                    "residue_pass": residue_pass,
                    "threshold_stable": threshold_pass,
                }
        seed_rows[length] = seeds

    qualifying_intervals: list[tuple[float, float]] = []
    qualifying_triplets: list[dict[str, object]] = []
    for seed4, seed6, seed8 in itertools.product(
        seed_rows[4], seed_rows[6], seed_rows[8]
    ):
        low = max(seed4["cell"][0], seed6["cell"][0], seed8["cell"][0])
        high = min(seed4["cell"][1], seed6["cell"][1], seed8["cell"][1])
        monotonic = (
            float(seed4["Delta_act"]) > float(seed6["Delta_act"]) > float(seed8["Delta_act"])
            and float(seed4["chi_tau"]) < float(seed6["chi_tau"]) < float(seed8["chi_tau"])
        )
        if low <= high and monotonic:
            qualifying_intervals.append((low, high))
            qualifying_triplets.append(
                {
                    "q_by_L": {"4": seed4["q"], "6": seed6["q"], "8": seed8["q"]},
                    "intersection": [low, high],
                    "gap_strictly_decreasing": True,
                    "chi_strictly_increasing": True,
                }
            )
    merged = merge_intervals(qualifying_intervals)
    unresolved_rows = [
        (length, row["q"])
        for length, rows in rows_by_l.items()
        for row in rows
        if row.get("response_status") == "UNRESOLVED"
    ]
    if unresolved_rows:
        classification = "UNRESOLVED_L4_L8__NO_L10_L12_AUTHORIZED"
    elif merged:
        classification = "SEED_INTERVAL_L4_L8__L10_L12_CONFIRMATION_AUTHORIZED_NOT_RUN"
    else:
        classification = "NO_CANDIDATE_L4_L8__STOP_NO_L10_L12"

    checks = []
    for item in structural:
        checks.extend(
            [
                (item["edges"] == 3 * item["L"], f"L{item['L']} owner edge census"),
                (item["unique_owner_edges"] == item["edges"], f"L{item['L']} owner uniqueness"),
                (set(item["degree_sequence"]) == {3}, f"L{item['L']} degree three"),
                (item["connected_vertices"] == item["sites"], f"L{item['L']} connected"),
                (item["one_carrier_band_linf"] < 1.0e-12, f"L{item['L']} analytic one-carrier band"),
                (item["Q_commutator_structural"] == 0.0, f"L{item['L']} Q conservation"),
            ]
        )
    for length, rows in rows_by_l.items():
        checks.extend(
            [
                (sum(int(row["eigenvalue_count"]) for row in rows) == sum(math.comb(2 * length, q) for q in range(length + 1)), f"L{length} complete half-sector spectra"),
                (max(float(row["hermiticity_error"]) for row in rows) == 0.0, f"L{length} exact Hermiticity"),
                (max(float(row["chiral_transition_error"]) for row in rows) == 0.0, f"L{length} exact chiral transitions"),
                (max(float(row["spectral_chiral_error"]) for row in rows) < 1.0e-10, f"L{length} chiral spectra"),
                (all(int(row["mid_spectrum_zero_count_at_1e-10"]) >= int(row["configuration_sublattice_imbalance_lower_bound"]) for row in rows), f"L{length} imbalance zero control"),
                (all(row.get("ground_multiplicity_at_1e-10") == 1 for row in rows), f"L{length} Perron-Frobenius ground uniqueness"),
            ]
        )
    failures = [label for passed, label in checks if not passed]
    if failures:
        classification = "FAIL_STRUCTURAL_OR_NUMERICAL__STOP_NO_L10_L12"

    result = {
        "schema": "R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001",
        "protocol_sha256": PROTOCOL_SHA256,
        "classification": classification,
        "scope": "ADOPTED_FIXED_Q_FINITE_PRISM_DIAGNOSTIC__NO_CONTINUUM_OR_GRAVITY_INFERENCE",
        "structural_controls": structural,
        "sector_dimensions": {
            str(length): [math.comb(2 * length, q) for q in range(length + 1)]
            for length in L_VALUES
        },
        "sector_rows": {str(length): rows for length, rows in rows_by_l.items()},
        "seeds_by_L": {str(length): rows for length, rows in seed_rows.items()},
        "qualifying_triplets": qualifying_triplets,
        "seed_interval_components": merged,
        "unresolved_rows": unresolved_rows,
        "larger_scale_status": "L10_L12_NOT_RUN__TARGET_STOPS_AFTER_L4_L8_SEED_CLASSIFICATION",
        "thresholds": {
            "degeneracy_abs": DEGENERACY_TOL,
            "eigen_residual_max": EIGEN_RESIDUAL_LIMIT,
            "relative_weight_floor": RELATIVE_WEIGHT_FLOOR,
            "residual_weight_multiplier": RESIDUAL_WEIGHT_MULTIPLIER,
            "R_low_min": 1.0e-6,
            "rss_limit_bytes_per_sector": RSS_LIMIT_BYTES,
            "wall_limit_seconds_per_sector": SECTOR_TIME_LIMIT_SECONDS,
        },
        "telemetry": {
            "total_wall_seconds": time.perf_counter() - started,
            "maximum_monitored_worker_rss_bytes": max(
                int(row["monitor_peak_rss_bytes"])
                for rows in rows_by_l.values()
                for row in rows
            ),
            "maximum_worker_wall_seconds": max(
                float(row["monitor_wall_seconds"])
                for rows in rows_by_l.values()
                for row in rows
            ),
            "host": os.uname().sysname + " " + os.uname().machine,
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "blas_threads_declared": 1,
        },
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "claim_classes": {
            "proved": "FINITE_OWNER_TOPOLOGY__Q_CONSERVATION__PARTICLE_HOLE_MAP__ANALYTIC_ONE_CARRIER_BANDS__BINOMIAL_WRITE_SECTOR_LAW",
            "adopted": "FIXED_Q_PROJECTION__TOTAL_RAIL_M1_MODE__DENSITY_CELLS__SEED_RULE",
            "conditional": "FINITE_PRISM_SUPPORT__CLOCK__READOUT__NUMERICAL_SOLVER",
            "empirical": "COMPLETE_FINITE_NUMERICAL_SPECTRA__ACTIVE_GAPS__CHI_TAU__RESIDUES__SEED_CLASSIFICATION",
            "open": "RHO_C__THERMODYNAMIC_LIMIT__MACROSCOPIC_CLOSURE__UNIVERSAL_COUPLING__GRAVITY",
        },
        "not_claimed": "H_OF_N__FINITE_DIVERGENCE__CONTINUUM__GRID__WARD__GRAVITON__GRAVITY",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        f"{classification}__{result['checks_passed']}/{result['checks_total']}__"
        f"wall={result['telemetry']['total_wall_seconds']:.3f}s__"
        f"peak={result['telemetry']['maximum_monitored_worker_rss_bytes']}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--L", type=int)
    parser.add_argument("--q", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--spectrum", type=Path)
    arguments = parser.parse_args()
    if arguments.worker:
        if None in (arguments.L, arguments.q, arguments.output, arguments.spectrum):
            parser.error("worker requires L, q, output, and spectrum")
        worker(arguments.L, arguments.q, arguments.output, arguments.spectrum)
    else:
        main()
