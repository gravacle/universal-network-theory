#!/usr/bin/env python3
"""Exact finite-state exploration of cooperative record formation and retention.

This is an explicitly assumed stochastic toy model, not an implementation or
proof of Universal Network Theory and not a derivation of electromagnetism.
Uses matrix exponentials, with no Monte Carlo sampling or parameter fitting.
"""

from __future__ import annotations

import argparse
import itertools
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm


PARAMETERS = {
    "beta": 1.0,
    "attempt_rate_nu": 1.0,
    "write_field_magnitude": 1.5,
    "write_duration": 5.0,
    "hold_times": [0.0, 1.0, 5.0, 20.0],
    "models": [
        {"name": "one_component", "N": 1, "J": 0.0},
        {"name": "three_independent", "N": 3, "J": 0.0},
        {"name": "three_interacting", "N": 3, "J": 1.0},
    ],
}


def energy(states: np.ndarray, J: float, h: float) -> np.ndarray:
    """H = -J sum_{i<j} q_i q_j - h sum_i q_i, q_i in {-1,+1}."""
    total = states.sum(axis=1)
    pair_sum = (total * total - states.shape[1]) / 2.0
    return -J * pair_sum - h * total


def generator(states: np.ndarray, J: float, h: float) -> np.ndarray:
    """Column generator: dp/dt = Q p; one variable changes per transition."""
    beta, nu = PARAMETERS["beta"], PARAMETERS["attempt_rate_nu"]
    energies = energy(states, J, h)
    lookup = {tuple(s): i for i, s in enumerate(states)}
    Q = np.zeros((len(states), len(states)))
    for column, state in enumerate(states):
        for site in range(states.shape[1]):
            flipped = state.copy()
            flipped[site] *= -1
            row = lookup[tuple(flipped)]
            delta = energies[row] - energies[column]
            Q[row, column] = nu / (1.0 + np.exp(beta * delta))
        Q[column, column] = -Q[:, column].sum()
    return Q


def equilibrium(states: np.ndarray, J: float, h: float) -> np.ndarray:
    logs = -PARAMETERS["beta"] * energy(states, J, h)
    weights = np.exp(logs - logs.max())
    return weights / weights.sum()


def run_model(spec: dict) -> dict:
    N, J = spec["N"], spec["J"]
    states = np.array(list(itertools.product([-1, 1], repeat=N)), dtype=int)
    p_blank = equilibrium(states, J, 0.0)
    hold_Q = generator(states, J, 0.0)
    # Both event alternatives have exactly the same event-independent blank.
    written = {}
    for event in (-1, 1):
        write_Q = generator(states, J, event * PARAMETERS["write_field_magnitude"])
        written[event] = expm(write_Q * PARAMETERS["write_duration"]) @ p_blank

    # One fixed query for both event alternatives. Odd N avoids tie conventions.
    positive_majority = states.sum(axis=1) > 0
    rows, all_probabilities = [], [p_blank, *written.values()]
    for hold in PARAMETERS["hold_times"]:
        evolution = expm(hold_Q * hold)
        p_minus, p_plus = evolution @ written[-1], evolution @ written[1]
        all_probabilities.extend([p_minus, p_plus])
        read_minus = float(p_minus[positive_majority].sum())
        read_plus = float(p_plus[positive_majority].sum())
        read_tv = abs(read_plus - read_minus)
        joint_tv = float(np.abs(p_plus - p_minus).sum() / 2.0)
        rows.append({
            "hold_time": hold,
            "P_read_plus_given_event_plus": read_plus,
            "P_read_plus_given_event_minus": read_minus,
            "majority_readout_total_variation": read_tv,
            "joint_state_total_variation": joint_tv,
            "balanced_majority_accuracy": (read_plus + 1.0 - read_minus) / 2.0,
        })

    flow = hold_Q * p_blank[np.newaxis, :]
    detailed_balance_error = float(np.max(np.abs(flow - flow.T)))
    checks = {
        "max_probability_normalization_error": float(max(abs(p.sum() - 1.0) for p in all_probabilities)),
        "minimum_probability": float(min(p.min() for p in all_probabilities)),
        "hold_generator_column_sum_error": float(np.max(np.abs(hold_Q.sum(axis=0)))),
        "hold_equilibrium_stationarity_error": float(np.max(np.abs(hold_Q @ p_blank))),
        "hold_detailed_balance_error": detailed_balance_error,
        "readout_TV_not_greater_than_joint_TV": all(r["majority_readout_total_variation"] <= r["joint_state_total_variation"] + 1e-12 for r in rows),
    }
    assert checks["max_probability_normalization_error"] < 1e-12
    assert checks["minimum_probability"] > -1e-12
    assert checks["hold_generator_column_sum_error"] < 1e-12
    assert checks["hold_equilibrium_stationarity_error"] < 1e-12
    assert checks["hold_detailed_balance_error"] < 1e-12
    assert checks["readout_TV_not_greater_than_joint_TV"]

    return {
        **spec,
        "state_count": len(states),
        "states_in_probability_order": states.tolist(),
        "event_independent_blank_distribution": p_blank.tolist(),
        "zero_field_mean_blank_energy": float(p_blank @ energy(states, J, 0.0)),
        "results": rows,
        "numerical_checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("cooperative_record_results.json"))
    args = parser.parse_args()
    result = {
        "status": "EXPLORATORY_TOY_MODEL_NOT_UNT_PROOF_NOT_EM_DERIVATION",
        "computed_date": "2026-10-28",
        "method": "Full finite continuous-time Markov generator; scipy.linalg.expm; no sampling or fitting",
        "parameters_frozen_before_execution": PARAMETERS,
        "energy": "H(q;h) = -J sum_{i<j} q_i q_j - h sum_i q_i",
        "transition_rate": "w(q -> flip_i(q)) = nu/(1+exp(beta*(H(flip_i(q))-H(q))))",
        "protocol": "Common zero-field Gibbs blank, finite pulse h=event*1.5 for time 5, then h=0 with source disconnected; fixed sign-of-sum readout.",
        "inputs_not_derived": [
            "Abstract binary degrees of freedom and interaction energy",
            "Thermal bath and detailed-balance transition rule",
            "A source event, write pulse, and timing controls",
            "Preparation of the event-independent equilibrium ensemble",
            "Access to the fixed majority readout",
        ],
        "interpretation_limits": [
            "Finite readable contrast under stated assumptions, not a certification of the full UNT REC predicate.",
            "The interacting zero-field Gibbs blank already has intercomponent correlations but no information about the later event; this experiment does not derive those correlations from an uncorrelated blank.",
            "No electromagnetic field, current, Maxwell action or identification with physical electromagnetism.",
            "No creation of information without an input event or origin-of-the-universe claim.",
            "N=3 independent versus N=3 interacting is the primary same-component-count comparison; coupling and equilibrium preparation resources differ.",
            "N=1 versus N=3 also changes the component count and total write-field coupling; no equal-energy-resource claim is made.",
            "At finite temperature all these finite chains eventually lose event information; retention is finite, not permanent.",
            "This parameter point is an illustrative existence example, not an optimization or general proof.",
        ],
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "models": [run_model(spec) for spec in PARAMETERS["models"]],
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for model in result["models"]:
        print(model["name"])
        for row in model["results"]:
            print(f"  hold={row['hold_time']:g} read_TV={row['majority_readout_total_variation']:.12g} joint_TV={row['joint_state_total_variation']:.12g}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
