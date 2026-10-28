#!/usr/bin/env python3
"""Prospectively declared finite path dynamics; NOT the unavailable CH theorem.

M counts simultaneous binary links of a path with M+1 vertices. The model is
H = -h sum X_i + Ud[(n_1-1)^2 + sum_i(n_i+n_(i+1)-1)^2 + (n_M-1)^2].
Initial links are a common product blank n_i=0. The ancestry gates K_i=1 are
fixed inputs of this declared hold. This program does not derive their
preparation, native support formation, a record write/read mission, or EM.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply


PARAMETERS = {
    "path_link_counts_M": [1, 3, 5, 7, 9, 11, 13, 15],
    "h_per_link": 1.0,
    "Ud_values": [0.0, 1.0, 4.0],
    "reported_times": [0.0, 0.25, 0.5, 1.0, 2.0, 4.0],
    "propagation_grid_step": 0.25,
    "hbar": 1.0,
    "ancestry_gates_K_i": "fixed at 1 by construction; preparation is an input",
}


def path_operators(M: int, h: float, Ud: float):
    dimension = 1 << M
    basis = np.arange(dimension, dtype=np.int64)
    bits = ((basis[:, None] >> np.arange(M)) & 1).astype(float)
    degree_cost = (bits[:, 0] - 1) ** 2 + (bits[:, -1] - 1) ** 2
    if M > 1:
        degree_cost += ((bits[:, :-1] + bits[:, 1:] - 1) ** 2).sum(axis=1)
    diagonal = Ud * degree_cost
    rows, columns, values = [basis], [basis], [diagonal]
    for site in range(M):
        rows.append(basis ^ (1 << site))
        columns.append(basis)
        values.append(np.full(dimension, -h))
    H = coo_matrix((np.concatenate(values), (np.concatenate(rows), np.concatenate(columns))), shape=(dimension, dimension)).tocsr()
    H.sum_duplicates()
    H.eliminate_zeros()
    return H, bits, degree_cost


def uncoupled_control(M: int, h: float, Ud: float, t: float):
    """Keep endpoint Z fields of expanded H, remove only neighboring ZZ terms."""
    a = np.zeros(M)
    a[0] += Ud / 2.0
    a[-1] += Ud / 2.0  # M=1: both endpoint fields act on the same variable.
    frequencies = np.sqrt(h * h + a * a)
    occupation = h * h / frequencies ** 2 * np.sin(frequencies * t) ** 2
    variances = occupation * (1 - occupation)
    return {
        "mean_occupation": float(occupation.mean()),
        "single_link_occupations": occupation.tolist(),
        "nearest_neighbor_connected_covariance_mean": 0.0 if M > 1 else None,
        "center_to_near_end_connected_covariance": 0.0 if M > 1 else None,
        "end_to_end_connected_covariance": 0.0 if M > 1 else None,
        "connected_staggered_variance_per_link": float(variances.mean()),
        "staggered_offdiagonal_covariance_sum_per_link": 0.0,
        "maximum_absolute_offdiagonal_covariance": 0.0,
        "method": "Analytic independent two-level evolution retaining identical one-body endpoint fields",
    }


def observables(state, bits):
    M = bits.shape[1]
    probability = np.abs(state) ** 2
    norm_squared = float(probability.sum())
    # Keep the propagated normalization; do not normalize away numerical errors.
    mean = bits.T @ probability
    second = bits.T @ (probability[:, None] * bits)
    covariance = second - np.outer(mean, mean)
    alternating = np.where(np.arange(M) % 2 == 0, 1.0, -1.0)
    center = M // 2
    offdiagonal = covariance.copy()
    np.fill_diagonal(offdiagonal, 0.0)
    if M >= 5:
        near_ends = [1, M - 2]
    elif M > 1:
        near_ends = [0, M - 1]
    else:
        near_ends = []
    profile = []
    for distance in range(M):
        entries = np.diag(covariance, k=distance)
        profile.append({"distance": distance, "mean_connected_covariance": float(entries.mean()), "maximum_absolute_connected_covariance": float(np.abs(entries).max())})
    return {
        "norm_squared": norm_squared,
        "mean_occupation": float(mean.mean()),
        "single_link_occupations": mean.tolist(),
        "nearest_neighbor_connected_covariance_mean": float(np.diag(covariance, k=1).mean()) if M > 1 else None,
        "center_to_near_end_connected_covariance": float(np.mean([covariance[center, i] for i in near_ends])) if near_ends else None,
        "center_to_near_end_distances": [abs(center - i) for i in near_ends],
        "end_to_end_connected_covariance": float(covariance[0, -1]) if M > 1 else None,
        "connected_staggered_variance_per_link": float(alternating @ covariance @ alternating / M),
        "staggered_offdiagonal_covariance_sum_per_link": float(alternating @ offdiagonal @ alternating / M),
        "maximum_absolute_offdiagonal_covariance": float(np.abs(offdiagonal).max()),
        "covariance_distance_profile": profile,
        "center_connected_covariance_to_each_link": covariance[center, :].tolist(),
    }


def run_one(M: int, Ud: float):
    h = PARAMETERS["h_per_link"]
    H, bits, degree_cost = path_operators(M, h, Ud)
    blank = np.zeros(1 << M, dtype=complex)
    blank[0] = 1.0
    step = PARAMETERS["propagation_grid_step"]
    final = PARAMETERS["reported_times"][-1]
    grid_count = int(round(final / step)) + 1
    started = time.perf_counter()
    trajectories = expm_multiply(-1j * H, blank, start=0.0, stop=final, num=grid_count, endpoint=True, traceA=-1j * H.diagonal().sum())
    elapsed = time.perf_counter() - started
    initial_energy = float(H[0, 0])
    rows = []
    maximum_norm_error = maximum_energy_error = independent_error = 0.0
    for t in PARAMETERS["reported_times"]:
        state = trajectories[int(round(t / step))]
        row = {"time": t, **observables(state, bits)}
        row["mean_degree_penalty_before_multiplying_Ud"] = float(np.abs(state) ** 2 @ degree_cost)
        row["energy_expectation"] = float(np.vdot(state, H @ state).real)
        row["matched_uncoupled_control"] = uncoupled_control(M, h, Ud, t)
        maximum_norm_error = max(maximum_norm_error, abs(row["norm_squared"] - 1.0))
        maximum_energy_error = max(maximum_energy_error, abs(row["energy_expectation"] - initial_energy))
        if Ud == 0 or M == 1:
            control = row["matched_uncoupled_control"]
            independent_error = max(independent_error, abs(row["mean_occupation"] - control["mean_occupation"]), row["maximum_absolute_offdiagonal_covariance"], abs(row["connected_staggered_variance_per_link"] - control["connected_staggered_variance_per_link"]))
        rows.append(row)
    assert maximum_norm_error < 1e-9
    assert maximum_energy_error < 1e-8 * max(1, abs(initial_energy))
    assert independent_error < 1e-9
    return {
        "M_links": M,
        "path_vertices": M + 1,
        "hilbert_dimension": 1 << M,
        "sparse_H_nonzeros": H.nnz,
        "Ud": Ud,
        "h_per_link": h,
        "initial_energy": initial_energy,
        "propagation_wall_seconds": elapsed,
        "results": rows,
        "checks": {"maximum_norm_error": maximum_norm_error, "maximum_energy_conservation_error": maximum_energy_error, "independent_control_error_when_applicable": independent_error if Ud == 0 or M == 1 else None},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("declared_path_dynamics_results.json"))
    args = parser.parse_args()
    result = {
        "status": "NEW_EXPLICIT_FINITE_PATH_INSTANTIATION_NOT_CH_REPRODUCTION_NOT_EM",
        "date": "2026-10-28",
        "parameters_frozen_before_execution": PARAMETERS,
        "expanded_H": "-h sum_i X_i + Ud/2 sum_(i=1)^(M-1) Z_i Z_(i+1) + Ud/2 (Z_1+Z_M) + Ud(M+1)/2, where n_i=(1-Z_i)/2",
        "matched_control_H": "-h sum_i X_i + Ud/2 (Z_1+Z_M), with only an irrelevant constant omitted; no shared ZZ interaction",
        "initial_state": "product |n_1=0,...,n_M=0>; no ground-state or thermal preparation",
        "scope": [
            "A declared simultaneous hold of a finite path using inherited interaction forms; not a reconstruction of unavailable GRA-CH boundary details.",
            "M counts simultaneous binary links. It is not the BS06 adjacent-layer width N or composition-layer depth L.",
            "Local h=1 and Ud are fixed as M varies; total hardware, total coupling count and blank energy grow with M. This is not the original dense h_N=Omega/N scaling family.",
            "All ancestry gates K_i=1, physical support, and simultaneous hold are assumptions of this finite instantiation.",
            "Odd M avoids the zero-defect perfect-matching obstruction of even-link open paths. Endpoints are included, not discarded.",
            "Only one common blank trajectory is studied; no two-event write/read contrast or complete UNT record certification is claimed.",
            "No EM field, Maxwell dynamics, new phase, thermodynamic result, million-link result, or cosmological inference is claimed.",
            "Fixed time t<=4 cannot exclude slower effects or longer correlations at larger sizes or times.",
        ],
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "models": [],
    }
    for Ud in PARAMETERS["Ud_values"]:
        for M in PARAMETERS["path_link_counts_M"]:
            model = run_one(M, Ud)
            result["models"].append(model)
            args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            last = model["results"][-1]
            print(f"Ud={Ud:g} M={M:2d} t=4 mean_n={last['mean_occupation']:.9g} nn_cov={last['nearest_neighbor_connected_covariance_mean']} stagger_var/M={last['connected_staggered_variance_per_link']:.9g} seconds={model['propagation_wall_seconds']:.3f}", flush=True)
    print(f"Saved: {args.output}", flush=True)


if __name__ == "__main__":
    main()
