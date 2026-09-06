#!/usr/bin/env python3
"""Bounded parameter scan for the connected eight-record carrier ring."""

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


N = 8
DIM = 1 << N
T_HOP = 1.0
DELTAS = (0.0, 0.5, 1.0, 2.0)
TAUS = (
    math.pi / (4.0 * math.sqrt(2.0)),
    math.pi / (2.0 * math.sqrt(2.0)),
    math.pi / math.sqrt(2.0),
)
RESIDUAL_L1_TOL = 3e-11
RESIDUAL_LINF_TOL = 4e-12


def q_diag(site):
    return np.array([(mask >> site) & 1 for mask in range(DIM)], dtype=float)


Q = [q_diag(i) for i in range(N)]
NUMBER = np.array([bin(mask).count("1") for mask in range(DIM)], dtype=int)
PSI0 = np.ones(DIM, dtype=complex) / math.sqrt(DIM)
Q0 = np.array([np.dot(abs(PSI0) ** 2, Q[i]) for i in range(N)])
NUMBER_LAW0 = np.array(
    [np.sum(abs(PSI0[NUMBER == k]) ** 2) for k in range(N + 1)]
)


def hamiltonian(delta):
    h = np.zeros((DIM, DIM), dtype=float)
    for mask in range(DIM):
        h[mask, mask] = sum(
            (1.0 if i % 2 == 0 else -1.0) * delta * ((mask >> i) & 1)
            for i in range(N)
        )
    for i in range(N):
        j = (i + 1) % N
        for mask in range(DIM):
            if ((mask >> i) & 1) != ((mask >> j) & 1):
                swapped = mask ^ (1 << i) ^ (1 << j)
                h[swapped, mask] += -T_HOP
    return h


def current_operator(i):
    j = (i + 1) % N
    op = np.zeros((DIM, DIM), dtype=complex)
    for mask in range(DIM):
        if ((mask >> i) & 1) == 1 and ((mask >> j) & 1) == 0:
            swapped = mask ^ (1 << i) ^ (1 << j)
            op[swapped, mask] += 1j
            op[mask, swapped] += -1j
    return op


J_OPS = [current_operator(i) for i in range(N)]


def run_point(delta, tau):
    h = hamiltonian(delta)
    evals, evecs = np.linalg.eigh(h)
    coeff = np.einsum("ia,i->a", evecs.conj(), PSI0, optimize=False)
    phase = np.exp(-1j * evals * tau)
    psi = np.einsum("ia,a->i", evecs, phase * coeff, optimize=False)

    hpsi = np.einsum("ij,j->i", h, psi, optimize=False)
    hpsi0 = np.einsum("ij,j->i", h, PSI0, optimize=False)
    norm_error = abs(np.vdot(psi, psi).real - 1.0)
    energy_error = abs(
        np.vdot(psi, hpsi).real - np.vdot(PSI0, hpsi0).real
    )
    probs = abs(psi) ** 2
    q1 = np.array([np.dot(probs, Q[i]) for i in range(N)])

    currents = []
    d_e = evals[:, None] - evals[None, :]
    factor = np.empty_like(d_e, dtype=complex)
    near = np.abs(d_e) < 1e-12
    factor[near] = tau
    factor[~near] = (
        np.exp(1j * d_e[~near] * tau) - 1.0
    ) / (1j * d_e[~near])
    for op in J_OPS:
        je = np.einsum("ij,jb->ib", op, evecs, optimize=False)
        energy_op = np.einsum(
            "ia,ib->ab", evecs.conj(), je, optimize=False
        )
        integral = np.sum(
            coeff.conj()[:, None]
            * coeff[None, :]
            * energy_op
            * factor
        )
        currents.append(float(integral.real))
    currents = np.array(currents)
    residuals = q1 - Q0 + currents - np.roll(currents, 1)

    connected = []
    for i in range(N):
        j = (i + 1) % N
        connected.append(
            float(np.dot(probs, Q[i] * Q[j]) - q1[i] * q1[j])
        )
    number_law1 = np.array(
        [np.sum(probs[NUMBER == k]) for k in range(N + 1)]
    )
    total_before = float(np.sum(Q0))
    total_after = float(np.sum(q1))
    return {
        "staggered_delta": delta,
        "tau": tau,
        "q_min": float(np.min(q1)),
        "q_max": float(np.max(q1)),
        "staggered_occupation_amplitude": float(
            abs(np.mean(q1[::2]) - np.mean(q1[1::2]))
        ),
        "max_abs_nearest_neighbor_connected_correlation": float(
            np.max(np.abs(connected))
        ),
        "absolute_oriented_throughput_per_ring": float(
            np.sum(np.abs(currents))
        ),
        "signed_oriented_current_sum_per_ring": float(np.sum(currents)),
        "total_retained_before_per_ring": total_before,
        "total_retained_after_per_ring": total_after,
        "retained_total_change_per_ring": total_after - total_before,
        "record_ledger_residual_l1_per_ring": float(
            np.sum(np.abs(residuals))
        ),
        "record_ledger_residual_linf_per_ring": float(
            np.max(np.abs(residuals))
        ),
        "norm_error": float(norm_error),
        "energy_error": float(energy_error),
        "number_law_max_change": float(
            np.max(np.abs(number_law1 - NUMBER_LAW0))
        ),
    }


points = [run_point(delta, tau) for delta in DELTAS for tau in TAUS]
out = {
    "schema": "R_CONNECTED_RING_PARAMETER_SCAN_NUMERICAL_V001",
    "sites_per_ring": N,
    "hilbert_dimension": DIM,
    "rings_in_L8_tiling": 32,
    "parameter_grid": {
        "t_hop": T_HOP,
        "staggered_deltas": list(DELTAS),
        "taus": list(TAUS),
    },
    "points": points,
    "envelope": {
        "max_record_ledger_residual_l1_per_ring": max(
            p["record_ledger_residual_l1_per_ring"] for p in points
        ),
        "max_record_ledger_residual_linf_per_ring": max(
            p["record_ledger_residual_linf_per_ring"] for p in points
        ),
        "max_abs_retained_total_change_per_ring": max(
            abs(p["retained_total_change_per_ring"]) for p in points
        ),
        "max_norm_error": max(p["norm_error"] for p in points),
        "max_energy_error": max(p["energy_error"] for p in points),
        "max_number_law_change": max(
            p["number_law_max_change"] for p in points
        ),
        "max_staggered_occupation_amplitude": max(
            p["staggered_occupation_amplitude"] for p in points
        ),
        "max_abs_connected_correlation": max(
            p["max_abs_nearest_neighbor_connected_correlation"]
            for p in points
        ),
        "max_absolute_oriented_throughput_per_ring": max(
            p["absolute_oriented_throughput_per_ring"] for p in points
        ),
    },
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "classification": (
        "CONTROLLED_NUMERICAL_PARAMETER_SCAN__RESIDUALS_UNASSIGNED_"
        "UNTIL_OWNER_CLASSIFICATION"
    ),
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
}

rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
Path(__file__).with_name("RESULT.json").write_text(rendered)
print(rendered, end="")

assert len(points) == 12
zero_control = [p for p in points if p["staggered_delta"] == 0.0]
assert max(p["staggered_occupation_amplitude"] for p in zero_control) < 2e-14
assert max(p["absolute_oriented_throughput_per_ring"] for p in zero_control) < 2e-13
assert out["envelope"]["max_staggered_occupation_amplitude"] > 0.1
assert out["envelope"]["max_abs_connected_correlation"] > 1e-3
assert out["envelope"]["max_absolute_oriented_throughput_per_ring"] > 0.1
assert out["envelope"]["max_record_ledger_residual_l1_per_ring"] < RESIDUAL_L1_TOL
assert out["envelope"]["max_record_ledger_residual_linf_per_ring"] < RESIDUAL_LINF_TOL
assert out["envelope"]["max_abs_retained_total_change_per_ring"] < 3e-14
assert out["envelope"]["max_norm_error"] < 3e-14
assert out["envelope"]["max_energy_error"] < 3e-13
assert out["envelope"]["max_number_law_change"] < 3e-14
assert out["classification"].endswith("UNTIL_OWNER_CLASSIFICATION")
print("PASS__R_CONNECTED_RING_PARAMETER_SCAN__13/13")
