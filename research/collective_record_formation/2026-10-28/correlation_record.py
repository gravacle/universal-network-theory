#!/usr/bin/env python3
"""Exploratory two-qubit correlation record; assumptions are not UNT derivations.

Run: python correlation_record.py
Dependencies: numpy, scipy. Times and Hamiltonian coefficients are dimensionless.
The output is written beside this script unless --output is provided.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm


def density(ket):
    return np.outer(ket, ket.conj())


def trace_distance(rho, sigma):
    delta = rho - sigma
    delta = (delta + delta.conj().T) / 2
    return float(np.sum(np.abs(np.linalg.eigvalsh(delta))) / 2)


def reductions(rho):
    tensor = rho.reshape(2, 2, 2, 2)  # a, b, a_prime, b_prime
    return np.trace(tensor, axis1=1, axis2=3), np.trace(tensor, axis1=0, axis2=2)


def probability(projector, rho):
    return float(np.trace(projector @ rho).real)


def metrics(states, p_plus, p_minus):
    r0, r1 = states
    a0, b0 = reductions(r0)
    a1, b1 = reductions(r1)
    plus0 = probability(p_plus, r0)
    plus1 = probability(p_plus, r1)
    return {
        "joint_trace_distance": trace_distance(r0, r1),
        "component_A_trace_distance": trace_distance(a0, a1),
        "component_B_trace_distance": trace_distance(b0, b1),
        "read_plus_probability_event_0": plus0,
        "read_plus_probability_event_1": plus1,
        "fixed_read_output_contrast": abs(plus0 - plus1),
        "equal_prior_fixed_read_success": (
            plus0 + probability(p_minus, r1)
        ) / 2,
    }


def compute():
    identity = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    z = np.diag([1, -1]).astype(complex)
    hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
    cnot = np.array(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
        dtype=complex,
    )
    xx, zz = np.kron(x, x), np.kron(z, z)
    z_a = np.kron(z, identity)
    blank = np.array([1, 0, 0, 0], dtype=complex)
    prepare = cnot @ np.kron(hadamard, identity)
    prepared = prepare @ blank
    event_kets = [prepared, z_a @ prepared]
    written_states = [density(ket) for ket in event_kets]
    p_plus = (np.eye(4) + xx) / 2
    p_minus = (np.eye(4) - xx) / 2

    # Assumed fixed interacting hold, with distinct energies for the two records.
    j, kappa = 1.0, 0.3
    h_hold = j * xx + kappa * zz
    gamma = 0.2
    times = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]
    ideal_rows, noise_rows = [], []
    max_analytic_error = 0.0
    max_state_sanity_error = 0.0

    for t in times:
        unitary = expm(-1j * t * h_hold)
        held = [unitary @ rho @ unitary.conj().T for rho in written_states]
        row = {"time": t, **metrics(held, p_plus, p_minus)}
        row["fidelity_with_written_event_0"] = probability(written_states[0], held[0])
        row["fidelity_with_written_event_1"] = probability(written_states[1], held[1])
        ideal_rows.append(row)

        # One declared perturbation: an event-independent local phase-flip channel.
        # For these states, this also equals continuous dephasing at rate gamma
        # during the hold, since all intermediate mixtures commute with H_hold.
        p_flip = (1 - math.exp(-gamma * t)) / 2
        noisy = [(1 - p_flip) * rho + p_flip * z_a @ rho @ z_a for rho in held]
        noise_row = {
            "time": t,
            "phase_flip_probability": p_flip,
            **metrics(noisy, p_plus, p_minus),
        }
        noise_rows.append(noise_row)
        expected_distance = math.exp(-gamma * t)
        expected_success = (1 + expected_distance) / 2
        max_analytic_error = max(
            max_analytic_error,
            abs(row["joint_trace_distance"] - 1),
            abs(row["fixed_read_output_contrast"] - 1),
            abs(row["equal_prior_fixed_read_success"] - 1),
            row["component_A_trace_distance"],
            row["component_B_trace_distance"],
            abs(noise_row["joint_trace_distance"] - expected_distance),
            abs(noise_row["fixed_read_output_contrast"] - expected_distance),
            abs(noise_row["equal_prior_fixed_read_success"] - expected_success),
            noise_row["component_A_trace_distance"],
            noise_row["component_B_trace_distance"],
        )
        for rho in held + noisy:
            max_state_sanity_error = max(
                max_state_sanity_error,
                abs(complex(np.trace(rho)) - 1),
                float(np.max(np.abs(rho - rho.conj().T))),
                max(0.0, -float(np.min(np.linalg.eigvalsh(rho)))),
            )

    if max(max_analytic_error, max_state_sanity_error) > 1e-12:
        raise RuntimeError("Numerical results exceed the declared 1e-12 verification guard")

    energies = [float(np.vdot(ket, h_hold @ ket).real) for ket in event_kets]
    eigen_residuals = [
        float(np.linalg.norm(h_hold @ ket - energy * ket))
        for ket, energy in zip(event_kets, energies)
    ]
    return {
        "study": "Exploratory correlation-only two-qubit input-event record",
        "date": "2026-10-28",
        "status": "CHECKED_TOY_MODEL_NOT_UNT_PROOF_OR_PHYSICAL_REALIZATION",
        "basis_order": ["00", "01", "10", "11"],
        "units": "Dimensionless; hbar=1; no physical time or energy calibration",
        "assumptions": [
            "Two abstract qubits and tensor-product quantum mechanics",
            "Common blank |00> and supplied preparation CNOT(Hadamard tensor I)",
            "Externally supplied classical event e chooses write (Z tensor I)^e",
            "Source disconnected after writing; no source or event input enters hold/read",
            "Supplied fixed interacting Hamiltonian J XX + kappa ZZ",
            "Supplied fixed joint read P_plus/minus=(I plus/minus XX)/2",
            "Noise comparison assumes an event-independent local phase-flip channel",
        ],
        "written_event_states": {
            "0": "(|00>+|11>)/sqrt(2)",
            "1": "(|00>-|11>)/sqrt(2)",
        },
        "local_states": "rho_A=rho_B=I/2 for either event, in ideal and noisy cases",
        "hold_parameters": {"J": j, "kappa": kappa},
        "hold_eigenenergies_event_0_1": energies,
        "hold_eigenvector_residuals_event_0_1": eigen_residuals,
        "written_metrics": metrics(written_states, p_plus, p_minus),
        "ideal_hold": ideal_rows,
        "noise": {
            "channel": "rho -> (1-p(t))*rho+p(t)*(Z tensor I)*rho*(Z tensor I)",
            "p_of_t": "(1-exp(-gamma*t))/2",
            "gamma": gamma,
            "analytic_joint_trace_distance_and_fixed_read_contrast": "exp(-gamma*t)",
            "analytic_equal_prior_fixed_read_success": "(1+exp(-gamma*t))/2",
            "success_at_least_0_9_through_time": -math.log(0.8) / gamma,
            "rows": noise_rows,
        },
        "verification": {
            "max_analytic_metric_error": max_analytic_error,
            "max_density_matrix_sanity_error": max_state_sanity_error,
            "guard": 1e-12,
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
        },
        "limitations": [
            "Preparation, write, interaction, and read are assumed primitives, not derived from UNT",
            "Stores an input-event bit in correlations; does not create information from nothing",
            "Not a derivation of electromagnetic fields, charge, currents, Maxwell dynamics, or alpha",
            "No claimed physical implementation, autonomous genesis, energy-cost accounting, or noise protection",
            "Collective-only claim refers to the accessible two-qubit record after source isolation",
            "Read can be implemented by measuring X on each component and comparing parity; either outcome alone is uninformative",
            "Noise survival applies only to the specified phase-flip model",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("correlation_record_results.json"))
    args = parser.parse_args()
    result = compute()
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "written_metrics": result["written_metrics"],
        "ideal_hold_success": [r["equal_prior_fixed_read_success"] for r in result["ideal_hold"]],
        "noise_time_distance_success": [
            [r["time"], r["joint_trace_distance"], r["equal_prior_fixed_read_success"]]
            for r in result["noise"]["rows"]
        ],
        "verification": result["verification"],
    }, indent=2))


if __name__ == "__main__":
    main()
