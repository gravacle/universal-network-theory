#!/usr/bin/env python3
"""Finite L4/L6/L8 BS09 record trajectory versus kappa=t*tau/hbar."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


SIZES = (4, 6, 8)
KAPPAS = (
    0.0,
    math.pi / 16.0,
    math.pi / 8.0,
    math.pi / 4.0,
    3.0 * math.pi / 8.0,
    math.pi / 2.0,
    3.0 * math.pi / 4.0,
    math.pi,
    3.0 * math.pi / 2.0,
    2.0 * math.pi,
)
ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001" / "RESULT.json"
OUT = Path(__file__).with_name("RESULT.json")


def q_diagonal(size: int, site: int) -> np.ndarray:
    dimension = 1 << size
    return np.array([(word >> site) & 1 for word in range(dimension)], dtype=float)


def prepare_ring(size: int) -> dict[str, object]:
    dimension = 1 << size
    q_ops = [q_diagonal(size, site) for site in range(size)]
    h0 = np.zeros((dimension, dimension), dtype=float)
    current_ops = []
    for site in range(size):
        neighbor = (site + 1) % size
        current = np.zeros((dimension, dimension), dtype=complex)
        for word in range(dimension):
            if ((word >> site) & 1) != ((word >> neighbor) & 1):
                swapped = word ^ (1 << site) ^ (1 << neighbor)
                h0[swapped, word] += -1.0
            if ((word >> site) & 1) == 1 and ((word >> neighbor) & 1) == 0:
                swapped = word ^ (1 << site) ^ (1 << neighbor)
                current[swapped, word] += 1j
                current[word, swapped] += -1j
        current_ops.append(current)

    psi0 = np.zeros(dimension, dtype=complex)
    amplitude = 1.0 / math.sqrt(1 << (size // 2))
    for word in range(dimension):
        if all(((word >> site) & 1) == 0 for site in range(0, size, 2)):
            psi0[word] = amplitude

    eigenvalues, eigenvectors = np.linalg.eigh(h0)
    coefficients = np.einsum("ia,i->a", eigenvectors.conj(), psi0, optimize=False)
    energy_currents = []
    for current in current_ops:
        acted = np.einsum("ij,jb->ib", current, eigenvectors, optimize=False)
        energy_currents.append(
            np.einsum("ia,ib->ab", eigenvectors.conj(), acted, optimize=False)
        )

    total_q = np.diag(
        np.array([bin(word).count("1") for word in range(dimension)], dtype=float)
    )
    onsite_commutator = np.einsum(
        "ij,jk->ik", h0, total_q, optimize=False
    ) - np.einsum("ij,jk->ik", total_q, h0, optimize=False)
    number = np.array([bin(word).count("1") for word in range(dimension)], dtype=int)
    probabilities0 = np.abs(psi0) ** 2
    number_law0 = np.array(
        [np.sum(probabilities0[number == count]) for count in range(size + 1)]
    )
    q0 = np.array([np.dot(probabilities0, q) for q in q_ops])
    hpsi0 = np.einsum("ij,j->i", h0, psi0, optimize=False)
    return {
        "size": size,
        "dimension": dimension,
        "q_ops": q_ops,
        "h0": h0,
        "psi0": psi0,
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "coefficients": coefficients,
        "energy_currents": energy_currents,
        "energy_differences": eigenvalues[:, None] - eigenvalues[None, :],
        "onsite_commutator_linf": float(np.max(np.abs(onsite_commutator))),
        "number": number,
        "number_law0": number_law0,
        "q0": q0,
        "initial_energy": float(np.vdot(psi0, hpsi0).real),
    }


def run_at_kappa(prepared: dict[str, object], kappa: float) -> dict[str, object]:
    size = int(prepared["size"])
    eigenvalues = prepared["eigenvalues"]
    eigenvectors = prepared["eigenvectors"]
    coefficients = prepared["coefficients"]
    phase = np.exp(-1j * eigenvalues * kappa)
    psi = np.einsum("ia,a->i", eigenvectors, phase * coefficients, optimize=False)
    probabilities = np.abs(psi) ** 2
    q_ops = prepared["q_ops"]
    q1 = np.array([np.dot(probabilities, q) for q in q_ops])

    differences = prepared["energy_differences"]
    factor = np.empty_like(differences, dtype=complex)
    near = np.abs(differences) < 1.0e-12
    factor[near] = kappa
    factor[~near] = (
        np.exp(1j * differences[~near] * kappa) - 1.0
    ) / (1j * differences[~near])
    currents = []
    for energy_current in prepared["energy_currents"]:
        integral = np.sum(
            coefficients.conj()[:, None]
            * coefficients[None, :]
            * energy_current
            * factor
        )
        currents.append(float(integral.real))
    currents = np.array(currents)
    q0 = prepared["q0"]
    residuals = q1 - q0 + currents - np.roll(currents, 1)

    number = prepared["number"]
    number_law = np.array(
        [np.sum(probabilities[number == count]) for count in range(size + 1)]
    )
    connected = []
    for site in range(size):
        neighbor = (site + 1) % size
        connected.append(
            float(
                np.dot(probabilities, q_ops[site] * q_ops[neighbor])
                - q1[site] * q1[neighbor]
            )
        )
    hpsi = np.einsum("ij,j->i", prepared["h0"], psi, optimize=False)
    cycles = size * size
    retained_total = float(cycles * np.sum(q1))
    throughput_total = float(cycles * np.sum(np.abs(currents)))
    return {
        "L": size,
        "kappa": kappa,
        "cycles": cycles,
        "prepared_source_lineages": size**3 // 2,
        "expected_retained_total": retained_total,
        "active_current_supports_per_cycle": int(np.sum(np.abs(currents) > 1.0e-12)),
        "q_after": q1.tolist(),
        "integrated_oriented_currents": currents.tolist(),
        "absolute_oriented_throughput_per_cycle": float(np.sum(np.abs(currents))),
        "absolute_oriented_throughput_total": throughput_total,
        "throughput_per_retained_record": (
            throughput_total / retained_total if retained_total else 0.0
        ),
        "max_abs_connected_edge_correlation": float(np.max(np.abs(connected))),
        "record_ledger_residual_l1_per_cycle": float(np.sum(np.abs(residuals))),
        "record_ledger_residual_linf_per_cycle": float(np.max(np.abs(residuals))),
        "record_ledger_residual_l1_tiled_bound": float(cycles * np.sum(np.abs(residuals))),
        "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
        "energy_error": float(
            abs(np.vdot(psi, hpsi).real - prepared["initial_energy"])
        ),
        "number_law_max_change": float(
            np.max(np.abs(number_law - prepared["number_law0"]))
        ),
        "uniform_onsite_commutator_linf": prepared["onsite_commutator_linf"],
    }


prepared_sizes = {size: prepare_ring(size) for size in SIZES}
rows = [
    run_at_kappa(prepared_sizes[size], kappa)
    for kappa in KAPPAS
    for size in SIZES
]
by_kappa = []
for kappa in KAPPAS:
    selected = {row["L"]: row for row in rows if row["kappa"] == kappa}
    l4 = selected[4]
    l8 = selected[8]
    if l4["absolute_oriented_throughput_total"] > 1.0e-14:
        total_ratio = (
            l8["absolute_oriented_throughput_total"]
            / l4["absolute_oriented_throughput_total"]
        )
        per_record_ratio = (
            l8["throughput_per_retained_record"]
            / l4["throughput_per_retained_record"]
        )
    else:
        total_ratio = None
        per_record_ratio = None
    by_kappa.append(
        {
            "kappa": kappa,
            "L8_over_L4_throughput_total": total_ratio,
            "L8_over_L4_throughput_per_retained_record": per_record_ratio,
        }
    )

baseline = json.loads(BASELINE.read_text())
baseline_rows = {row["L"]: row for row in baseline["rows"]}
scan_baseline = {row["L"]: row for row in rows if row["kappa"] == math.pi / 2.0}
baseline_difference = 0.0
for size in (4, 8):
    for key in (
        "expected_retained_after_total",
        "absolute_oriented_throughput_total",
        "max_abs_connected_edge_correlation",
        "record_ledger_residual_l1_per_cycle",
        "record_ledger_residual_linf_per_cycle",
    ):
        scan_key = "expected_retained_total" if key == "expected_retained_after_total" else key
        baseline_difference = max(
            baseline_difference,
            abs(scan_baseline[size][scan_key] - baseline_rows[size][key]),
        )
    for key in ("q_after", "integrated_oriented_currents"):
        baseline_difference = max(
            baseline_difference,
            float(
                np.max(
                    np.abs(
                        np.array(scan_baseline[size][key])
                        - np.array(baseline_rows[size][key])
                    )
                )
            ),
        )

positive_rows = [row for row in rows if row["kappa"] > 0.0]
throughput_sequences = {
    str(size): [
        row["absolute_oriented_throughput_per_cycle"]
        for row in rows
        if row["L"] == size
    ]
    for size in SIZES
}

checks = [
    (len(rows) == len(SIZES) * len(KAPPAS), "complete size/kappa census"),
    ({row["L"] for row in rows} == set(SIZES), "L4/L6/L8 present"),
    (all(abs(row["expected_retained_total"] - row["L"]**3 / 4.0) < 5.0e-12 for row in rows), "retained totals"),
    (all(row["prepared_source_lineages"] == row["L"]**3 // 2 for row in rows), "lineage census"),
    (all(row["active_current_supports_per_cycle"] == 0 for row in rows if row["kappa"] == 0.0), "zero-kappa current control"),
    (all(row["active_current_supports_per_cycle"] == row["L"] for row in scan_baseline.values()), "baseline supports active"),
    (all(row["absolute_oriented_throughput_total"] > 0.0 for row in positive_rows), "positive-kappa recorded throughput"),
    (max(row["record_ledger_residual_l1_per_cycle"] for row in rows) < 5.0e-11, "ledger L1"),
    (max(row["record_ledger_residual_linf_per_cycle"] for row in rows) < 8.0e-12, "ledger Linf"),
    (max(row["norm_error"] for row in rows) < 8.0e-14, "norm"),
    (max(row["energy_error"] for row in rows) < 5.0e-13, "energy"),
    (max(row["number_law_max_change"] for row in rows) < 8.0e-14, "number law"),
    (max(row["uniform_onsite_commutator_linf"] for row in rows) == 0.0, "uniform onsite commutator"),
    (baseline_difference < 5.0e-12, "pi/2 baseline reproduction"),
    (all(any(values[i + 1] < values[i] for i in range(len(values) - 1)) for values in throughput_sequences.values()), "finite throughput is nonmonotone"),
]
failures = [label for ok, label in checks if not ok]

out = {
    "schema": "R_AUTONOMOUS_BS09_KAPPA_TRAJECTORY_V001",
    "classification": "CONDITIONAL_SUPPORT_AND_KAPPA__AUTONOMOUS_BS09_EVOLUTION__FINITE_MICROSCOPIC_RECORD_TRAJECTORY",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "physical_parameter": "KAPPA_EQUALS_T_TIMES_TAU_OVER_HBAR",
    "parameter_status": "SCANNED_CONDITIONAL_MISSION_DATA__NOT_SELECTED_OR_DERIVED",
    "support_status": "CONDITIONAL_FIXED_CYCLE_PROGRAM__UNCHANGED_PARENT_DOES_NOT_AUTONOMOUSLY_SELECT_IT",
    "source_status": "F3_MDC_PREPARED_HEADS__ADOPTED_ALPHA_R0__SOURCES_OFF_DURING_ACCUMULATION",
    "kappas": list(KAPPAS),
    "rows": rows,
    "ratios": by_kappa,
    "pi_over_2_baseline_max_abs_difference": baseline_difference,
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "not_claimed": "COEFFICIENT_OR_CLOCK_SELECTION__GENERIC_PHASE__GRID__CONTINUUM__WARD__GRAVITY",
}
OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

if failures:
    raise AssertionError(failures)
print(f"PASS__R_AUTONOMOUS_KAPPA_TRAJECTORY__{len(checks)}/{len(checks)}")
