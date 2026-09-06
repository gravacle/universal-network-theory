#!/usr/bin/env python3
"""Autonomous source-prepared carrier rings selected by the physical parent."""

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


SIZES = (4, 8)
T_HOP = 1.0
TAU = math.pi / 2.0


def source_preparation_control():
    phi = math.pi / 4.0
    write = np.array(
        [[math.cos(phi), -1j * math.sin(phi)],
         [-1j * math.sin(phi), math.cos(phi)]],
        dtype=complex,
    )
    after_write = np.zeros(4, dtype=complex)
    # Pair bit order is tail,head: |BB>, |Bx>, |xB>, |xx>.
    after_write[0] = write[0, 0]
    after_write[2] = write[1, 0]
    transfer = np.eye(4, dtype=complex)
    transfer[1, 1] = 0.0
    transfer[2, 2] = 0.0
    transfer[1, 2] = 1j
    transfer[2, 1] = 1j
    final = np.einsum("ij,j->i", transfer, after_write, optimize=False)
    expected = np.array([1.0, 1.0, 0.0, 0.0], dtype=complex) / math.sqrt(2.0)
    return float(np.max(abs(final - expected)))


def q_diag(size, site):
    dim = 1 << size
    return np.array([(mask >> site) & 1 for mask in range(dim)], dtype=float)


def run_ring(size):
    dim = 1 << size
    q_ops = [q_diag(size, i) for i in range(size)]
    hamiltonian = np.zeros((dim, dim), dtype=float)
    for i in range(size):
        j = (i + 1) % size
        for mask in range(dim):
            if ((mask >> i) & 1) != ((mask >> j) & 1):
                swapped = mask ^ (1 << i) ^ (1 << j)
                hamiltonian[swapped, mask] += -T_HOP
    total_q = np.diag(
        np.array([bin(mask).count("1") for mask in range(dim)], dtype=float)
    )
    uniform_onsite_commutator = np.einsum(
        "ij,jk->ik", hamiltonian, total_q, optimize=False
    ) - np.einsum("ij,jk->ik", total_q, hamiltonian, optimize=False)

    # The audited write plus pi/2 tail-to-head transfer gives blank even tails
    # and (|B>+|x>)/sqrt(2) on odd heads, with no phase left over.
    psi0 = np.zeros(dim, dtype=complex)
    amplitude = 1.0 / math.sqrt(1 << (size // 2))
    for mask in range(dim):
        if all(((mask >> i) & 1) == 0 for i in range(0, size, 2)):
            psi0[mask] = amplitude

    evals, evecs = np.linalg.eigh(hamiltonian)
    coeff = np.einsum("ia,i->a", evecs.conj(), psi0, optimize=False)
    phase = np.exp(-1j * evals * TAU)
    psi = np.einsum("ia,a->i", evecs, phase * coeff, optimize=False)
    probs0 = abs(psi0) ** 2
    probs = abs(psi) ** 2
    q0 = np.array([np.dot(probs0, q_ops[i]) for i in range(size)])
    q1 = np.array([np.dot(probs, q_ops[i]) for i in range(size)])

    currents = []
    d_e = evals[:, None] - evals[None, :]
    factor = np.empty_like(d_e, dtype=complex)
    near = np.abs(d_e) < 1e-12
    factor[near] = TAU
    factor[~near] = (
        np.exp(1j * d_e[~near] * TAU) - 1.0
    ) / (1j * d_e[~near])
    for i in range(size):
        j = (i + 1) % size
        current = np.zeros((dim, dim), dtype=complex)
        for mask in range(dim):
            if ((mask >> i) & 1) == 1 and ((mask >> j) & 1) == 0:
                swapped = mask ^ (1 << i) ^ (1 << j)
                current[swapped, mask] += 1j
                current[mask, swapped] += -1j
        je = np.einsum("ij,jb->ib", current, evecs, optimize=False)
        energy_current = np.einsum(
            "ia,ib->ab", evecs.conj(), je, optimize=False
        )
        integral = np.sum(
            coeff.conj()[:, None]
            * coeff[None, :]
            * energy_current
            * factor
        )
        currents.append(float(integral.real))
    currents = np.array(currents)
    residuals = q1 - q0 + currents - np.roll(currents, 1)

    number = np.array([bin(mask).count("1") for mask in range(dim)], dtype=int)
    number_law0 = np.array(
        [np.sum(probs0[number == k]) for k in range(size + 1)]
    )
    number_law1 = np.array(
        [np.sum(probs[number == k]) for k in range(size + 1)]
    )
    connected = []
    for i in range(size):
        j = (i + 1) % size
        connected.append(
            float(np.dot(probs, q_ops[i] * q_ops[j]) - q1[i] * q1[j])
        )
    hpsi = np.einsum("ij,j->i", hamiltonian, psi, optimize=False)
    hpsi0 = np.einsum("ij,j->i", hamiltonian, psi0, optimize=False)
    cycles = size * size
    return {
        "L": size,
        "cycles_in_VL": cycles,
        "sites_per_cycle": size,
        "hilbert_dimension_per_cycle": dim,
        "prepared_heads_per_cycle": size // 2,
        "prepared_source_lineages": size ** 3 // 2,
        "expected_retained_before_per_cycle": float(np.sum(q0)),
        "expected_retained_after_per_cycle": float(np.sum(q1)),
        "expected_retained_before_total": float(cycles * np.sum(q0)),
        "expected_retained_after_total": float(cycles * np.sum(q1)),
        "q_before": q0.tolist(),
        "q_after": q1.tolist(),
        "integrated_oriented_currents": currents.tolist(),
        "active_current_supports_per_cycle": int(
            np.sum(np.abs(currents) > 1e-12)
        ),
        "absolute_oriented_throughput_per_cycle": float(
            np.sum(np.abs(currents))
        ),
        "absolute_oriented_throughput_total": float(
            cycles * np.sum(np.abs(currents))
        ),
        "record_ledger_residual_l1_per_cycle": float(
            np.sum(np.abs(residuals))
        ),
        "record_ledger_residual_linf_per_cycle": float(
            np.max(np.abs(residuals))
        ),
        "record_ledger_residual_l1_tiled_bound": float(
            cycles * np.sum(np.abs(residuals))
        ),
        "max_abs_connected_edge_correlation": float(
            np.max(np.abs(connected))
        ),
        "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
        "energy_error": float(
            abs(np.vdot(psi, hpsi).real - np.vdot(psi0, hpsi0).real)
        ),
        "number_law_max_change": float(
            np.max(np.abs(number_law1 - number_law0))
        ),
        "uniform_onsite_commutator_linf": float(
            np.max(np.abs(uniform_onsite_commutator))
        ),
    }


rows = [run_ring(size) for size in SIZES]
l4, l8 = rows
out = {
    "schema": "R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_NUMERICAL_V001",
    "physical_parent_selection": {
        "source_preparation": (
            "F3_MDC_WRITE_PHI_PI_OVER_4_THEN_NATIVE_TRANSFER_THETA_PI_OVER_2"
        ),
        "prepared_cycle_state": (
            "EVEN_TAILS_BLANK__ODD_HEADS_(B_PLUS_X)_OVER_SQRT2"
        ),
        "source_status_during_accumulation": "OFF",
        "carrier_generator": "BS09_H_EQUALS_MINUS_T_SUM_N_E_T_E",
        "evolution": "AUTONOMOUS_EXP_MINUS_I_H_TAU__NO_GATE_ORDER",
        "uniform_onsite_term": (
            "COMMUTES_WITH_H_AND_RECORDED_OCCUPATION_OBSERVABLES__"
            "ZERO_REPRESENTATIVE_USED"
        ),
        "incidence_support": (
            "CONDITIONAL_FIXED_PROGRAM__FIRST_GENERATOR_CYCLES_ACTIVE"
        ),
    },
    "parameters": {
        "t_hop": T_HOP,
        "tau": TAU,
        "t_tau_over_hbar": T_HOP * TAU,
        "node_dependent_onsite_stagger": 0.0,
    },
    "source_preparation_vector_error": source_preparation_control(),
    "rows": rows,
    "raw_L8_over_L4": {
        "expected_retained_total": (
            l8["expected_retained_after_total"]
            / l4["expected_retained_after_total"]
        ),
        "absolute_oriented_throughput_total": (
            l8["absolute_oriented_throughput_total"]
            / l4["absolute_oriented_throughput_total"]
        ),
        "throughput_per_retained_record": (
            (
                l8["absolute_oriented_throughput_total"]
                / l8["expected_retained_after_total"]
            )
            /
            (
                l4["absolute_oriented_throughput_total"]
                / l4["expected_retained_after_total"]
            )
        ),
    },
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "attachment": "INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
    "coordinate_status": "INHERITED_FINITE_FAMILY_ENUMERATION__NOT_PHYSICAL_GRID",
    "prior_programmed_circuit_classification": (
        "ORDERED_STAGGERED_CIRCUITS_ARE_CONDITIONAL_PROGRAMMED_CONTROL_"
        "RECORDS__NOT_AUTONOMOUS_BS09_SELECTION"
    ),
    "classification": (
        "CONDITIONAL_PHYSICAL_PARENT_SELECTED_PREPARATION_AND_AUTONOMOUS_"
        "EVOLUTION__SUPPORT_PROGRAM_AND_COEFFICIENTS_REMAIN_CONDITIONAL__"
        "RESIDUALS_UNASSIGNED_UNTIL_OWNER_CLASSIFICATION"
    ),
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
}

rendered = json.dumps(out, indent=2, sort_keys=True) + "\n"
Path(__file__).with_name("RESULT.json").write_text(rendered)
print(rendered, end="")

assert [row["cycles_in_VL"] for row in rows] == [16, 64]
assert out["source_preparation_vector_error"] < 3e-16
assert [row["prepared_source_lineages"] for row in rows] == [32, 256]
assert all(
    row["active_current_supports_per_cycle"] == row["sites_per_cycle"]
    for row in rows
)
assert abs(l4["expected_retained_after_total"] - 16.0) < 1e-13
assert abs(l8["expected_retained_after_total"] - 128.0) < 5e-13
assert all(row["absolute_oriented_throughput_total"] > 0.1 for row in rows)
assert all(row["max_abs_connected_edge_correlation"] > 1e-4 for row in rows)
assert max(row["record_ledger_residual_l1_per_cycle"] for row in rows) < 3e-11
assert max(row["record_ledger_residual_linf_per_cycle"] for row in rows) < 4e-12
assert max(row["norm_error"] for row in rows) < 3e-14
assert max(row["energy_error"] for row in rows) < 3e-13
assert max(row["number_law_max_change"] for row in rows) < 3e-14
assert max(row["uniform_onsite_commutator_linf"] for row in rows) == 0.0
assert out["parameters"]["node_dependent_onsite_stagger"] == 0.0
assert "NO_GATE_ORDER" in out["physical_parent_selection"]["evolution"]
assert out["prior_programmed_circuit_classification"].endswith(
    "NOT_AUTONOMOUS_BS09_SELECTION"
)
assert out["classification"].endswith("UNTIL_OWNER_CLASSIFICATION")
print("PASS__R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION__16/16")
