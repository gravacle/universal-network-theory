#!/usr/bin/env python3
"""Dense independent reconstruction of the intrinsic L4 admission trace."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_DIR = ROOT / "DEVELOPMENT_R_INTRINSIC_ADMISSION_PARENT_L4_V001"
TARGET = TARGET_DIR / "TRACE_L4.json"
OUT = HERE / "INDEPENDENT_TRACE_L4.json"
PHI = math.pi / 4.0
KAPPA = math.pi / 2.0
SITES = 8
DONORS = 4
TARGETS = (0, 1, 2, 3)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def count_bits(value: int) -> int:
    return value.bit_count()


def prism_edges() -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for rail in range(2):
        for site in range(4):
            result.append((4 * rail + site, 4 * rail + (site + 1) % 4))
    result.extend((site, 4 + (site + 1) % 4) for site in range(4))
    return result


def dense_hamiltonian() -> np.ndarray:
    hamiltonian = np.zeros((1 << SITES, 1 << SITES), dtype=np.complex128)
    for word in range(1 << SITES):
        for u, v in prism_edges():
            if ((word >> u) & 1) != ((word >> v) & 1):
                hamiltonian[word ^ (1 << u) ^ (1 << v), word] -= 1.0
    return hamiltonian


def retained_q(state: np.ndarray) -> float:
    counts = np.array([count_bits(word) for word in range(1 << SITES)], dtype=float)
    return float(np.sum(np.abs(state) ** 2 * counts[np.newaxis, :]))


def genesis_q(state: np.ndarray) -> float:
    counts = np.array([count_bits(word) for word in range(1 << DONORS)], dtype=float)
    return float(np.sum(np.abs(state) ** 2 * counts[:, np.newaxis]))


def predicates(state: np.ndarray, donor: int, target: int) -> tuple[float, float, float]:
    allow = blocked = reverse = 0.0
    for donor_word in range(1 << DONORS):
        loaded = (donor_word >> donor) & 1
        for carrier_word in range(1 << SITES):
            probability = abs(state[donor_word, carrier_word]) ** 2
            occupied = (carrier_word >> target) & 1
            if loaded and not occupied:
                allow += probability
            elif loaded and occupied:
                blocked += probability
            elif not loaded and occupied:
                reverse += probability
    return float(allow), float(blocked), float(reverse)


def admission(state: np.ndarray, donor: int, target: int) -> np.ndarray:
    result = state.copy()
    cosine = math.cos(PHI)
    sine = math.sin(PHI)
    for donor_word in range(1 << DONORS):
        if ((donor_word >> donor) & 1) == 0:
            continue
        spent_word = donor_word ^ (1 << donor)
        for carrier_word in range(1 << SITES):
            if (carrier_word >> target) & 1:
                continue
            occupied_word = carrier_word ^ (1 << target)
            left = state[donor_word, carrier_word]
            right = state[spent_word, occupied_word]
            result[donor_word, carrier_word] = cosine * left - 1j * sine * right
            result[spent_word, occupied_word] = cosine * right - 1j * sine * left
    return result


def blocked_error(state: np.ndarray, donor: int, target: int) -> float:
    projected = np.zeros_like(state)
    for donor_word in range(1 << DONORS):
        if ((donor_word >> donor) & 1) == 0:
            continue
        for carrier_word in range(1 << SITES):
            if (carrier_word >> target) & 1:
                projected[donor_word, carrier_word] = state[donor_word, carrier_word]
    return float(np.linalg.norm(admission(projected, donor, target) - projected))


def run() -> dict[str, object]:
    target = json.loads(TARGET.read_text())
    hamiltonian = dense_hamiltonian()
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    unitary = (eigenvectors * np.exp(-1j * KAPPA * eigenvalues)) @ eigenvectors.conj().T
    state = np.zeros((1 << DONORS, 1 << SITES), dtype=np.complex128)
    state[(1 << DONORS) - 1, 0] = 1.0
    rows = []
    for event, target_vertex in enumerate(TARGETS, start=1):
        donor = event - 1
        allow, blocked, reverse = predicates(state, donor, target_vertex)
        null_error = blocked_error(state, donor, target_vertex)
        q_before = retained_q(state)
        g_before = genesis_q(state)
        admitted = admission(state, donor, target_vertex)
        q_admitted = retained_q(admitted)
        g_admitted = genesis_q(admitted)
        write = q_admitted - q_before
        state = (unitary @ admitted.T).T
        rows.append({
            "event": event,
            "allow_probability": allow,
            "blocked_probability": blocked,
            "reverse_support_probability": reverse,
            "blocked_null_state_error": null_error,
            "W_n": write,
            "admission_total_content_residual": write + g_admitted - g_before,
            "q_retained_after_transport": retained_q(state),
            "q_genesis_after_transport": genesis_q(state),
            "norm_error": abs(float(np.vdot(state, state).real) - 1.0),
        })

    keys = ("allow_probability", "blocked_probability", "reverse_support_probability", "W_n", "q_retained_after_transport")
    maximum_disagreement = max(
        abs(float(row[key]) - float(target["rows"][index][key]))
        for index, row in enumerate(rows)
        for key in keys
    )
    checks = {
        "dense_hamiltonian_hermitian": float(np.max(np.abs(hamiltonian - hamiltonian.conj().T))) <= 1.0e-14,
        "dense_transport_unitary": float(np.max(np.abs(unitary.conj().T @ unitary - np.eye(1 << SITES)))) <= 1.0e-12,
        "target_classification_pass": target["classification"] == "PASS_L4_INTRINSIC_ADMISSION__COHERENT_UNWRITING_ELIMINATED_ON_DECLARED_TRACE",
        "target_checks_all_pass": all(bool(value) for value in target["checks"].values()),
        "independent_writes_nonnegative": min(float(row["W_n"]) for row in rows) >= -1.0e-12,
        "independent_blocked_null": max(float(row["blocked_null_state_error"]) for row in rows) <= 1.0e-12,
        "independent_reverse_support_zero": max(float(row["reverse_support_probability"]) for row in rows) <= 1.0e-12,
        "independent_content_conserved": max(abs(float(row["admission_total_content_residual"])) for row in rows) <= 1.0e-12,
        "independent_norms_close": max(float(row["norm_error"]) for row in rows) <= 1.0e-12,
        "nonvacuous_blocking": max(float(row["blocked_probability"]) for row in rows) > 1.0e-6,
        "target_independent_agreement": maximum_disagreement <= 1.0e-9,
        "target_transport_ledger_pass": max(float(row["transport_node_residual_l1"]) for row in target["rows"]) <= 1.0e-9,
    }
    verdict = "PASS_HOSTILE_INTRINSIC_ADMISSION_L4" if all(checks.values()) else "FAIL_CLOSED_HOSTILE_INTRINSIC_ADMISSION_L4"
    return {
        "schema": "INTRINSIC_ADMISSION_PARENT_L4_INDEPENDENT_AUDIT_V001",
        "verdict": verdict,
        "checks": checks,
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "maximum_target_independent_disagreement": maximum_disagreement,
        "dense_hermiticity_error": float(np.max(np.abs(hamiltonian - hamiltonian.conj().T))),
        "dense_unitarity_error": float(np.max(np.abs(unitary.conj().T @ unitary - np.eye(1 << SITES)))),
        "rows": rows,
        "target_sha256": digest(TARGET),
        "target_protocol_sha256": digest(TARGET_DIR / "PROTOCOL.md"),
        "independent_implementation_sha256": digest(Path(__file__)),
        "claim_boundary": {
            "proved_if_pass": "FINITE_L4_ONE_PASS_NULL_ADMISSION_AND_NONNEGATIVE_WRITE",
            "not_claimed": ["GENERIC_ACCUMULATION", "BACKGROUND_INDEPENDENCE_THEOREM", "CONTINUUM", "EMERGENCE", "GRAVITY"],
        },
    }


if __name__ == "__main__":
    result = run()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["verdict"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print(f"maximum disagreement {result['maximum_target_independent_disagreement']:.3e}")
    if not all(result["checks"].values()):
        for name, passed in result["checks"].items():
            if not passed:
                print("FAIL", name)
        raise SystemExit(1)
