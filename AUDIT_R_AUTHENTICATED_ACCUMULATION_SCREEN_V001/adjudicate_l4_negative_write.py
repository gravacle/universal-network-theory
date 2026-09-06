#!/usr/bin/env python3
"""Complete-space L4 adjudication of the third signed source term."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_RAW = ROOT / "DEVELOPMENT_R_AUTHENTICATED_ACCUMULATION_SCREEN_V001" / "RAW_HISTORY" / "HISTORY_L4.json"
BLIND_RAW = HERE / "RAW_HISTORY" / "HISTORY_L4.json"
OUT = HERE / "L4_SIGN_ADJUDICATION.json"
LENGTH = 4
SITES = 8
DIMENSION = 256


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


edges = []
for rail in range(2):
    base = rail * LENGTH
    for site in range(LENGTH):
        edges.append((base + site, base + (site + 1) % LENGTH))
for site in range(LENGTH):
    edges.append((site, LENGTH + (site + 1) % LENGTH))

hamiltonian = np.zeros((DIMENSION, DIMENSION), dtype=float)
for word in range(DIMENSION):
    for u, v in edges:
        if ((word >> u) & 1) != ((word >> v) & 1):
            hamiltonian[word, word ^ (1 << u) ^ (1 << v)] -= 1.0

values, vectors = np.linalg.eigh(hamiltonian)
phases = np.exp(-1j * values * math.pi / 2.0)
transport = np.einsum("ik,k,jk->ij", vectors, phases, vectors, optimize=False)
q_values = np.array([bin(word).count("1") for word in range(DIMENSION)], dtype=float)
low = np.array([word for word in range(DIMENSION) if (word & 1) == 0], dtype=int)
high = low | 1


def write(state: np.ndarray) -> np.ndarray:
    result = state.copy()
    result[low] = (state[low] - 1j * state[high]) / math.sqrt(2.0)
    result[high] = (state[high] - 1j * state[low]) / math.sqrt(2.0)
    return result


def q(state: np.ndarray) -> float:
    return float(np.dot(q_values, np.abs(state) ** 2))


state = np.zeros(DIMENSION, dtype=np.complex128)
state[0] = 1.0
writes = []
norm_errors = []
for _ in range(3):
    before = q(state)
    state = write(state)
    writes.append(q(state) - before)
    state = np.einsum("ij,j->i", transport, state, optimize=False)
    norm_errors.append(abs(float(np.vdot(state, state).real) - 1.0))

target = json.loads(TARGET_RAW.read_text())
blind = json.loads(BLIND_RAW.read_text())
target_w3 = float(target["fine_rows"][2]["W_n"])
blind_w3 = float(blind["fine_rows"][2]["W_n"])
w3 = float(writes[2])
hermiticity = float(np.max(np.abs(hamiltonian - hamiltonian.T)))
eigen_action = np.einsum("ij,jk->ik", hamiltonian, vectors, optimize=False)
eigen_residual = float(np.max(np.linalg.norm(eigen_action - vectors * values, axis=0)))
unitary_product = np.einsum("ki,kj->ij", np.conjugate(transport), transport, optimize=False)
unitarity = float(np.max(np.abs(unitary_product - np.eye(DIMENSION))))
agreement = max(abs(w3 - target_w3), abs(w3 - blind_w3), abs(target_w3 - blind_w3))
error_bound = max(1.0e-12, 20.0 * max(hermiticity, eigen_residual, unitarity, max(norm_errors), agreement))
checks = {
    "owner_edges_12": len(edges) == 12 and len(set(tuple(sorted(edge)) for edge in edges)) == 12,
    "hermiticity_below_1e_10": hermiticity <= 1.0e-10,
    "eigen_residual_below_1e_10": eigen_residual <= 1.0e-10,
    "unitarity_below_1e_10": unitarity <= 1.0e-10,
    "norm_error_below_1e_10": max(norm_errors) <= 1.0e-10,
    "first_write_one_half": abs(writes[0] - 0.5) <= 1.0e-12,
    "target_blind_direct_agreement_below_1e_10": agreement <= 1.0e-10,
    "negative_upper_bound_below_minus_1e_6": w3 + error_bound < -1.0e-6,
}
confirmed = all(checks.values())
result = {
    "schema": "AUTHENTICATED_ACCUMULATION_L4_SIGN_ADJUDICATION_V001",
    "classification": "CONFIRMED_NEGATIVE_W3__FAIL_CLOSED_HISTORY" if confirmed else "UNRESOLVED_W3_SIGN",
    "writes": writes,
    "W3": w3,
    "target_W3": target_w3,
    "blind_W3": blind_w3,
    "agreement_error": agreement,
    "conservative_error_bound": error_bound,
    "W3_upper_bound": w3 + error_bound,
    "controls": {
        "hermiticity_error": hermiticity,
        "eigenpair_residual_max": eigen_residual,
        "unitarity_error_linf": unitarity,
        "norm_error_max": max(norm_errors),
    },
    "checks": checks,
    "input_sha256": {
        "target_L4": digest(TARGET_RAW),
        "blind_L4_repaired": digest(BLIND_RAW),
        "method": digest(HERE / "ADJUDICATION_METHOD.md"),
        "implementation": digest(Path(__file__)),
    },
    "mandated_next_gate": "HALT_BEFORE_L6_L8_L10_L12_AND_SPECTRUM",
    "claim_boundary": {
        "proved_boolean": "FIRST_THREE_POSITIVE_WRITES_IS_FALSE_FOR_DECLARED_L4_HISTORY",
        "not_claimed": ["GENERIC_ACCUMULATION_NULL", "CRITICAL_DENSITY", "CONTINUUM", "EMERGENCE", "GRAVITY"],
    },
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(result["classification"])
print("W3", w3, "upper", w3 + error_bound)
print("checks", sum(checks.values()), "/", len(checks))
if not confirmed:
    raise SystemExit(1)
