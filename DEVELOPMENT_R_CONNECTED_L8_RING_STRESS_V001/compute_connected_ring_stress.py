#!/usr/bin/env python3
"""Numerical connected 8-site native-carrier ring accumulation stress."""

import json
import math
import os

# The bundled macOS NumPy can route tiny dense products through unstable
# oversubscribed Accelerate paths. Freeze one thread before importing NumPy.
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


n = 8
dim = 1 << n
t_hop = 1.0
delta = 1.0
tau = math.pi / (2.0 * math.sqrt(2.0))


def q_diag(site):
    return np.array([(mask >> site) & 1 for mask in range(dim)], dtype=float)


H = np.zeros((dim, dim), dtype=float)
for mask in range(dim):
    H[mask, mask] = sum((1.0 if i % 2 == 0 else -1.0) * delta *
                        ((mask >> i) & 1) for i in range(n))
for i in range(n):
    j = (i + 1) % n
    for mask in range(dim):
        bi = (mask >> i) & 1
        bj = (mask >> j) & 1
        if bi != bj:
            swapped = mask ^ (1 << i) ^ (1 << j)
            H[swapped, mask] += -t_hop

evals, evecs = np.linalg.eigh(H)
psi0 = np.ones(dim, dtype=complex) / math.sqrt(dim)
coeff = np.einsum("ia,i->a", evecs.conj(), psi0, optimize=False)
phase = np.exp(-1j * evals * tau)
psi = np.einsum("ia,a->i", evecs, phase * coeff, optimize=False)

norm_error = abs(np.vdot(psi, psi).real - 1.0)
Hpsi = np.einsum("ij,j->i", H, psi, optimize=False)
Hpsi0 = np.einsum("ij,j->i", H, psi0, optimize=False)
energy_error = abs(np.vdot(psi, Hpsi).real - np.vdot(psi0, Hpsi0).real)

q0 = np.array([np.dot(abs(psi0) ** 2, q_diag(i)) for i in range(n)])
q1 = np.array([np.dot(abs(psi) ** 2, q_diag(i)) for i in range(n)])

# Edge currents J_i oriented i -> i+1, matching BS07.
currents = []
for i in range(n):
    j = (i + 1) % n
    J = np.zeros((dim, dim), dtype=complex)
    for mask in range(dim):
        bi = (mask >> i) & 1
        bj = (mask >> j) & 1
        if bi == 1 and bj == 0:
            swapped = mask ^ (1 << i) ^ (1 << j)
            J[swapped, mask] += 1j
            J[mask, swapped] += -1j

    Je = np.einsum("ij,jb->ib", J, evecs, optimize=False)
    O = np.einsum("ia,ib->ab", evecs.conj(), Je, optimize=False)
    dE = evals[:, None] - evals[None, :]
    factor = np.empty_like(dE, dtype=complex)
    near = np.abs(dE) < 1e-12
    factor[near] = tau
    factor[~near] = (np.exp(1j * dE[~near] * tau) - 1.0) / (1j * dE[~near])
    # c_a^* c_b O_ab integral exp(i(Ea-Eb)t)
    integral = np.sum(coeff.conj()[:, None] * coeff[None, :] * O * factor)
    currents.append(float(integral.real))

currents = np.array(currents)
residuals = q1 - q0 + currents - np.roll(currents, 1)

number = np.array([bin(mask).count("1") for mask in range(dim)], dtype=int)
number_law0 = np.array([np.sum(abs(psi0[number == k]) ** 2) for k in range(n + 1)])
number_law1 = np.array([np.sum(abs(psi[number == k]) ** 2) for k in range(n + 1)])

# Connected nearest-neighbor occupation correlations after the stress.
connected = []
probs = abs(psi) ** 2
for i in range(n):
    j = (i + 1) % n
    qi = q_diag(i)
    qj = q_diag(j)
    connected.append(float(np.dot(probs, qi * qj) - q1[i] * q1[j]))

out = {
    "schema": "R_CONNECTED_L8_RING_STRESS_NUMERICAL_V001",
    "sites_per_ring": n,
    "hilbert_dimension": dim,
    "tau": tau,
    "parameters": {"t_hop": t_hop, "staggered_delta": delta},
    "norm_error": norm_error,
    "energy_error": energy_error,
    "q_before": q0.tolist(),
    "q_after": q1.tolist(),
    "integrated_oriented_currents": currents.tolist(),
    "record_ledger_residuals": residuals.tolist(),
    "residual_l1": float(np.sum(np.abs(residuals))),
    "residual_linf": float(np.max(np.abs(residuals))),
    "total_retained_before": float(np.sum(q0)),
    "total_retained_after": float(np.sum(q1)),
    "number_law_max_change": float(np.max(np.abs(number_law1 - number_law0))),
    "nearest_neighbor_connected_correlations": connected,
    "rings_in_L8_tiling": 32,
    "L8_total_retained_before": float(32 * np.sum(q0)),
    "L8_total_retained_after": float(32 * np.sum(q1)),
    "L8_absolute_oriented_throughput": float(32 * np.sum(np.abs(currents))),
    "L8_net_oriented_ring_current": float(32 * np.sum(currents)),
    "L8_residual_l1_bound": float(32 * np.sum(np.abs(residuals))),
    "L8_residual_linf": float(np.max(np.abs(residuals))),
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "scope": "NUMERICAL_CONNECTED_RING_PREPARED_STRESS__NO_CONTINUUM_INFERENCE"
}
print(json.dumps(out, indent=2, sort_keys=True))

tol = 2e-12
assert norm_error < tol
assert energy_error < tol
assert abs(out["total_retained_after"] - out["total_retained_before"]) < tol
assert out["number_law_max_change"] < tol
assert out["residual_l1"] < 2e-11
assert out["residual_linf"] < 3e-12
assert max(abs(x) for x in connected) > 1e-4
assert abs(out["L8_total_retained_after"] - 128.0) < 7e-14
assert abs(out["L8_net_oriented_ring_current"]) < 3e-14
assert out["terminal_instrument"].startswith("COMPLETE_FAILURE")
print("PASS__R_CONNECTED_L8_RING_STRESS__10/10")
