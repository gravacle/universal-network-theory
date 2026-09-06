#!/usr/bin/env python3
"""Blind translation-block reconstruction of the frozen L4/L6/L8 seed screen."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import resource
import time
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
PROTOCOL = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "PROTOCOL.md"
OUT = Path(os.environ.get("R_CRITICALITY_AUDIT_OUTPUT", str(HERE / "INDEPENDENT_RESULT.json")))
EXPECTED_PROTOCOL_SHA256 = "3da9e74b0dcc2d8b65ce98cfb42735864cf3d045e41655082baa7a7a295cb334"
SIZES = tuple(int(value) for value in os.environ.get("R_CRITICALITY_AUDIT_SIZES", "4,6,8").split(","))
if not SIZES or any(length not in (4, 6, 8) for length in SIZES):
    raise ValueError("audit sizes must be a nonempty subset of 4,6,8")
ENERGY_GROUP_TOL = 1.0e-10
RESIDUAL_TOL = 1.0e-10
RELATIVE_CHI_MARGIN = 1.0e-9


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_for(length: int):
    edges = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length))
    for site in range(length):
        edges.append((site, length + (site + 1) % length))
    return tuple(edges)


def translate_word(word: int, length: int, shift: int = 1) -> int:
    mask = (1 << length) - 1
    shift %= length
    if shift == 0:
        return word
    out = 0
    for rail in range(2):
        bits = (word >> (rail * length)) & mask
        rotated = ((bits << shift) & mask) | (bits >> (length - shift))
        out |= rotated << (rail * length)
    return out


def sector_words(site_count: int, charge: int) -> np.ndarray:
    words = []
    for occupied in itertools.combinations(range(site_count), charge):
        word = 0
        for site in occupied:
            word |= 1 << site
        words.append(word)
    return np.asarray(words, dtype=np.int64)


def sector_graph(words: np.ndarray, edges):
    index = {int(word): row for row, word in enumerate(words)}
    neighbors = []
    for row, raw_word in enumerate(words):
        word = int(raw_word)
        row_neighbors = []
        for u, v in edges:
            if ((word >> u) & 1) != ((word >> v) & 1):
                swapped = word ^ (1 << u) ^ (1 << v)
                row_neighbors.append(index[swapped])
        neighbors.append(tuple(row_neighbors))
    return tuple(neighbors), index


def h_apply(neighbors, vector):
    out = np.empty_like(vector)
    for row, adjacent in enumerate(neighbors):
        out[row] = -np.sum(vector[np.asarray(adjacent, dtype=int)], axis=0)
    return out


def translation_orbits(words: np.ndarray, index, length: int):
    unseen = set(int(word) for word in words)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = []
        word = representative
        while word not in orbit:
            orbit.append(word)
            word = translate_word(word, length)
        if word != representative:
            raise AssertionError("translation orbit failed to close at representative")
        for item in orbit:
            unseen.remove(item)
        orbits.append(tuple(index[item] for item in orbit))
    return tuple(orbits)


def momentum_basis(dimension: int, orbits, length: int, momentum: int):
    row_columns = np.full(dimension, -1, dtype=np.int64)
    row_coefficients = np.zeros(dimension, dtype=np.complex128)
    column = 0
    wave = 2.0 * math.pi * momentum / length
    for orbit in orbits:
        period = len(orbit)
        if (momentum * period) % length:
            continue
        scale = 1.0 / math.sqrt(period)
        for step, row in enumerate(orbit):
            row_columns[row] = column
            row_coefficients[row] = scale * np.exp(-1j * wave * step)
        column += 1
    return row_columns, row_coefficients, column


def dense_block(neighbors, basis):
    row_columns, row_coefficients, dimension = basis
    block = np.zeros((dimension, dimension), dtype=np.complex128)
    for row, adjacent in enumerate(neighbors):
        left = int(row_columns[row])
        if left < 0:
            continue
        left_coefficient = np.conjugate(row_coefficients[row])
        for column_row in adjacent:
            right = int(row_columns[column_row])
            if right >= 0:
                block[left, right] -= left_coefficient * row_coefficients[column_row]
    return 0.5 * (block + block.conjugate().T)


def expand_basis(basis, coefficients):
    row_columns, row_coefficients, _ = basis
    out = np.zeros(len(row_columns), dtype=np.complex128)
    active = row_columns >= 0
    out[active] = row_coefficients[active] * coefficients[row_columns[active]]
    return out


def project_basis(basis, vector):
    row_columns, row_coefficients, dimension = basis
    out = np.zeros(dimension, dtype=np.complex128)
    for row in np.flatnonzero(row_columns >= 0):
        out[row_columns[row]] += np.conjugate(row_coefficients[row]) * vector[row]
    return out


def complex_matrix_product_via_real(left, right):
    """Avoid the host Accelerate complex-batch FPE-flag warning path."""
    left_real = left.real
    left_imag = left.imag
    right_real = right.real
    right_imag = right.imag
    return (
        left_real @ right_real - left_imag @ right_imag
        + 1j * (left_real @ right_imag + left_imag @ right_real)
    )


def adjoint_vector_product_via_real(matrix, vector):
    """Return matrix^* vector using only real matrix-vector products."""
    matrix_real = matrix.real
    matrix_imag = matrix.imag
    vector_real = vector.real
    vector_imag = vector.imag
    return (
        matrix_real.T @ vector_real + matrix_imag.T @ vector_imag
        + 1j * (matrix_real.T @ vector_imag - matrix_imag.T @ vector_real)
    )


def group_response(eigenvalues, weights, residuals, ground_energy):
    records = []
    start = 0
    while start < len(eigenvalues):
        stop = start + 1
        while (
            stop < len(eigenvalues)
            and abs(eigenvalues[stop] - eigenvalues[start]) <= ENERGY_GROUP_TOL
        ):
            stop += 1
        omega = float(np.mean(eigenvalues[start:stop]) - ground_energy)
        records.append({
            "omega": omega,
            "energy_min": float(eigenvalues[start]),
            "energy_max": float(eigenvalues[stop - 1]),
            "multiplicity": stop - start,
            "weight": float(np.sum(weights[start:stop])),
            "eigen_residual_max": float(np.max(residuals[start:stop])),
        })
        start = stop
    return records


def active_at(groups, threshold):
    candidates = [row for row in groups if row["omega"] > ENERGY_GROUP_TOL and row["weight"] > threshold]
    if not candidates:
        return None
    return min(candidates, key=lambda row: row["omega"])


def density_cell(length: int, charge: int):
    return (
        max(0.0, (charge - 0.5) / (2.0 * length)),
        min(0.5, (charge + 0.5) / (2.0 * length)),
    )


def intersect_many(intervals):
    low = max(interval[0] for interval in intervals)
    high = min(interval[1] for interval in intervals)
    return (low, high) if low <= high else None


def merge_intervals(intervals):
    merged = []
    for low, high in sorted(intervals):
        if not merged or low > merged[-1][1]:
            merged.append([low, high])
        else:
            merged[-1][1] = max(merged[-1][1], high)
    return [tuple(interval) for interval in merged]


started = time.perf_counter()
if sha256(PROTOCOL) != EXPECTED_PROTOCOL_SHA256:
    raise AssertionError("frozen protocol hash mismatch")

structural = {}
rows_by_size = {}
all_checks = []

for length in SIZES:
    sites = 2 * length
    edges = edges_for(length)
    degrees = [0] * sites
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    all_checks.extend([
        (len(edges) == 3 * length, f"L{length} owner-once edge census"),
        (len(set(frozenset(edge) for edge in edges)) == len(edges), f"L{length} unique owners"),
        (all(degree == 3 for degree in degrees), f"L{length} degree three"),
        (all((u % length) % 2 != (v % length) % 2 for u, v in edges), f"L{length} bipartite base"),
    ])

    one_words = sector_words(sites, 1)
    one_neighbors, _ = sector_graph(one_words, edges)
    one_h = np.zeros((sites, sites), dtype=float)
    for row, adjacent in enumerate(one_neighbors):
        one_h[row, np.asarray(adjacent, dtype=int)] = -1.0
    one_numeric = np.linalg.eigvalsh(one_h)
    one_formula = np.sort(np.asarray([
        -2.0 * math.cos(2.0 * math.pi * momentum / length) + band
        for momentum in range(length)
        for band in (-1.0, 1.0)
    ]))
    band_error = float(np.max(np.abs(one_numeric - one_formula)))
    all_checks.append((band_error < 1.0e-12, f"L{length} exact one-carrier bands"))

    structural[str(length)] = {
        "sites": sites,
        "owner_edges": len(edges),
        "degrees": degrees,
        "hamiltonian_has_write_count_argument": False,
        "q_conservation": "EXACT__EVERY_ACTION_IS_ONE_OCCUPIED_ONE_BLANK_SWAP",
        "particle_hole": "EXACT__BIT_COMPLEMENT_COMMUTES_WITH_EVERY_SWAP",
        "chiral": "EXACT__ODD_I_OCCUPANCY_PARITY_FLIPS_ON_EVERY_HOP",
        "one_carrier_numeric": one_numeric.tolist(),
        "one_carrier_formula": one_formula.tolist(),
        "one_carrier_band_linf": band_error,
        "exact_zero_multiplicity": int(np.sum(np.abs(one_numeric) <= 1.0e-12)),
    }

    ground_energies = {0: 0.0}
    rows = []
    for charge in range(1, length + 1):
        words = sector_words(sites, charge)
        neighbors, word_index = sector_graph(words, edges)
        orbits = translation_orbits(words, word_index, length)
        b_ground = momentum_basis(len(words), orbits, length, 0)
        h_ground = dense_block(neighbors, b_ground)
        eval_ground, evec_ground = np.linalg.eigh(h_ground)
        ground_energy = float(eval_ground[0])
        ground_coefficients = evec_ground[:, 0]
        ground_vector = expand_basis(b_ground, ground_coefficients)
        ground_residual = float(np.linalg.norm(h_apply(neighbors, ground_vector) - ground_energy * ground_vector))
        ground_energies[charge] = ground_energy

        response_momentum = length - 1
        b_response = momentum_basis(len(words), orbits, length, response_momentum)
        h_response = dense_block(neighbors, b_response)
        eval_response, evec_response = np.linalg.eigh(h_response)
        h_times_eigenvectors = complex_matrix_product_via_real(
            h_response, evec_response
        )
        response_residuals = np.asarray([
            np.linalg.norm(
                h_times_eigenvectors[:, column]
                - eval_response[column] * evec_response[:, column]
            )
            for column in range(len(eval_response))
        ])
        response_residual_max = float(np.max(response_residuals))

        k = 2.0 * math.pi / length
        nk_diagonal = np.empty(len(words), dtype=np.complex128)
        for row, raw_word in enumerate(words):
            word = int(raw_word)
            nk_diagonal[row] = sum(
                np.exp(1j * k * site)
                * (((word >> site) & 1) + ((word >> (length + site)) & 1))
                for site in range(length)
            )
        response_vector = nk_diagonal * ground_vector
        response_coefficients = project_basis(b_response, response_vector)
        spectral_coefficients = adjoint_vector_product_via_real(
            evec_response, response_coefficients
        )
        weights = np.abs(spectral_coefficients) ** 2
        response_weight = float(np.vdot(response_vector, response_vector).real)
        weight_closure = float(abs(np.sum(weights) - response_weight))

        translated_response = np.empty_like(response_vector)
        for row, raw_word in enumerate(words):
            translated = translate_word(int(raw_word), length)
            translated_response[word_index[translated]] = response_vector[row]
        expected_phase = np.exp(-1j * k)
        momentum_covariance_error = float(np.max(np.abs(translated_response - expected_phase * response_vector)))

        groups = group_response(
            eval_response, weights, response_residuals, ground_energy
        )
        weight_floor = max(
            1.0e-12 * response_weight,
            100.0 * response_residual_max ** 2 * response_weight,
        )
        active_rows = [active_at(groups, factor * weight_floor) for factor in (0.1, 1.0, 10.0)]
        threshold_stable = (
            all(row is not None for row in active_rows)
            and max(row["omega"] for row in active_rows) - min(row["omega"] for row in active_rows) <= ENERGY_GROUP_TOL
        )
        active = active_rows[1]
        positive_groups = [row for row in groups if row["omega"] > ENERGY_GROUP_TOL]
        chi_denominator = sum(row["weight"] for row in positive_groups)
        chi_numerator = sum(row["weight"] / row["omega"] ** 2 for row in positive_groups)
        chi_tau = math.sqrt(chi_numerator / chi_denominator) if chi_denominator > 0 else math.nan
        delta = active["omega"] if active is not None else math.nan
        residue = active["weight"] / chi_denominator if active is not None and chi_denominator > 0 else math.nan
        unresolved_reasons = []
        if ground_residual > RESIDUAL_TOL:
            unresolved_reasons.append("GROUND_RESIDUAL")
        if response_residual_max > RESIDUAL_TOL:
            unresolved_reasons.append("RESPONSE_EIGEN_RESIDUAL")
        if weight_closure > RESIDUAL_TOL:
            unresolved_reasons.append("RESPONSE_WEIGHT_CLOSURE")
        if momentum_covariance_error > RESIDUAL_TOL:
            unresolved_reasons.append("MOMENTUM_COVARIANCE")
        if not threshold_stable:
            unresolved_reasons.append("ACTIVE_THRESHOLD_SWITCH")
        if active is None:
            unresolved_reasons.append("NO_ACTIVE_POLE")

        rows.append({
            "L": length,
            "q": charge,
            "rho": charge / sites,
            "density_cell": density_cell(length, charge),
            "sector_dimension": len(words),
            "translation_orbit_count": len(orbits),
            "ground_block_dimension": int(b_ground[2]),
            "response_block_momentum": response_momentum,
            "response_block_dimension": int(b_response[2]),
            "ground_energy": ground_energy,
            "ground_residual": ground_residual,
            "response_eigen_residual_max": response_residual_max,
            "response_weight": response_weight,
            "response_weight_closure": weight_closure,
            "momentum_covariance_linf": momentum_covariance_error,
            "weight_floor": weight_floor,
            "threshold_active_omegas": [None if row is None else row["omega"] for row in active_rows],
            "threshold_stable": threshold_stable,
            "delta_act": delta,
            "chi_tau": chi_tau,
            "R_low": residue,
            "spectral_group_count": len(groups),
            "response_groups": groups,
            "unresolved_reasons": unresolved_reasons,
        })

        del neighbors, b_ground, h_ground, eval_ground, evec_ground
        del b_response, h_response, eval_response, evec_response, h_times_eigenvectors

    for row in rows:
        charge = row["q"]
        upper_charge = charge + 1
        if upper_charge <= length:
            upper_energy = ground_energies[upper_charge]
        else:
            upper_energy = ground_energies[sites - upper_charge]
        lower_energy = ground_energies[charge - 1]
        row["delta_Q"] = upper_energy + lower_energy - 2.0 * ground_energies[charge]

    rows_by_size[str(length)] = rows

seeds_by_size = {}
any_unresolved = False
for length in SIZES:
    rows = rows_by_size[str(length)]
    by_charge = {row["q"]: row for row in rows}
    seeds = []
    for charge in range(2, length):
        lower = by_charge[charge - 1]
        center = by_charge[charge]
        upper = by_charge[charge + 1]
        relevant = (lower, center, upper)
        if any(row["unresolved_reasons"] for row in relevant):
            any_unresolved = True
            continue
        delta_margin = 10.0 * max(
            row["ground_residual"] + row["response_eigen_residual_max"]
            for row in relevant
        ) + 1.0e-12
        gap_min = center["delta_act"] + delta_margin < min(lower["delta_act"], upper["delta_act"])
        chi_scale = max(1.0, lower["chi_tau"], center["chi_tau"], upper["chi_tau"])
        chi_max = center["chi_tau"] > max(lower["chi_tau"], upper["chi_tau"]) + RELATIVE_CHI_MARGIN * chi_scale
        residue_pass = center["R_low"] >= 1.0e-6
        if gap_min and chi_max and residue_pass and center["threshold_stable"]:
            seeds.append({
                "q": charge,
                "rho": center["rho"],
                "density_cell": center["density_cell"],
                "delta_act": center["delta_act"],
                "chi_tau": center["chi_tau"],
                "R_low": center["R_low"],
                "delta_margin": delta_margin,
            })
    seeds_by_size[str(length)] = seeds

candidate_triplets = []
if set(SIZES) == {4, 6, 8}:
    for seed4 in seeds_by_size["4"]:
        for seed6 in seeds_by_size["6"]:
            for seed8 in seeds_by_size["8"]:
                intersection = intersect_many([
                    seed4["density_cell"], seed6["density_cell"], seed8["density_cell"]
                ])
                if intersection is None:
                    continue
                decreasing_gap = seed4["delta_act"] > seed6["delta_act"] > seed8["delta_act"]
                increasing_chi = seed4["chi_tau"] < seed6["chi_tau"] < seed8["chi_tau"]
                if decreasing_gap and increasing_chi:
                    candidate_triplets.append({
                        "q_by_L": {"4": seed4["q"], "6": seed6["q"], "8": seed8["q"]},
                        "intersection": intersection,
                        "decreasing_gap": True,
                        "increasing_chi_tau": True,
                    })

candidate_intervals = merge_intervals([row["intersection"] for row in candidate_triplets])
if set(SIZES) != {4, 6, 8}:
    classification = "PARTIAL_BLIND_SELF_TEST"
elif candidate_intervals:
    classification = "CANDIDATE_INTERVAL_L4_L8"
elif any_unresolved:
    classification = "UNRESOLVED_L4_L8"
else:
    classification = "NO_CANDIDATE_L4_L8"

all_checks.extend([
    (all(not row["unresolved_reasons"] for rows in rows_by_size.values() for row in rows), "all response rows resolved"),
    (all(row["threshold_stable"] for rows in rows_by_size.values() for row in rows), "all active poles threshold stable"),
    (all(row["R_low"] >= 0.0 for rows in rows_by_size.values() for row in rows), "all residues nonnegative"),
])
failed_checks = [label for passed, label in all_checks if not passed]

result = {
    "schema": "AUDIT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001",
    "independence": "METHOD_AND_CODE_FROZEN_BEFORE_TARGET_RESULT_INSPECTION",
    "protocol_sha256": sha256(PROTOCOL),
    "method": "EXACT_TRANSLATION_ORBITS__COMPLETE_M0_AND_RESPONSE_MOMENTUM_BLOCKS",
    "sizes_executed": list(SIZES),
    "sizes_forbidden_and_not_executed": [10, 12],
    "structural": structural,
    "rows": rows_by_size,
    "seeds": seeds_by_size,
    "candidate_triplets": candidate_triplets,
    "candidate_intervals": candidate_intervals,
    "classification": classification,
    "claim_boundary": "FINITE_SECTOR_SEED_SCREEN_ONLY__NO_RHO_C__NO_CONTINUUM__NO_GRAVITY",
    "checks_passed": sum(passed for passed, _ in all_checks),
    "checks_total": len(all_checks),
    "failed_checks": failed_checks,
    "runtime_seconds": time.perf_counter() - started,
    "max_rss_bytes_darwin": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}
OUT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({
    "classification": classification,
    "seeds": seeds_by_size,
    "candidate_intervals": candidate_intervals,
    "checks": f"{result['checks_passed']}/{result['checks_total']}",
    "failed_checks": failed_checks,
    "runtime_seconds": result["runtime_seconds"],
    "max_rss_bytes_darwin": result["max_rss_bytes_darwin"],
}, indent=2))
