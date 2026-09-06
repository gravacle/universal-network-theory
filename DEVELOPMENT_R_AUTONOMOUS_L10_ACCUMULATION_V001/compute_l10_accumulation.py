#!/usr/bin/env python3
"""L10 autonomous BS09 accumulation using an audited symmetry current reduction."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


SIZE = 10
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
PRIOR = ROOT / "DEVELOPMENT_R_AUTONOMOUS_KAPPA_TRAJECTORY_V001" / "RESULT.json"
OUT = Path(__file__).with_name("RESULT.json")
EXECUTION_RECORD = Path(__file__).with_name("EXECUTION_RECORD.json")


def q_diagonal(size: int, site: int) -> np.ndarray:
    dimension = 1 << size
    return np.array([(word >> site) & 1 for word in range(dimension)], dtype=float)


def build_ring(size: int) -> tuple[np.ndarray, list[np.ndarray], np.ndarray]:
    dimension = 1 << size
    h0 = np.zeros((dimension, dimension), dtype=float)
    for site in range(size):
        neighbor = (site + 1) % size
        for word in range(dimension):
            if ((word >> site) & 1) != ((word >> neighbor) & 1):
                swapped = word ^ (1 << site) ^ (1 << neighbor)
                h0[swapped, word] += -1.0
    q_ops = [q_diagonal(size, site) for site in range(size)]
    psi0 = np.zeros(dimension, dtype=complex)
    amplitude = 1.0 / math.sqrt(1 << (size // 2))
    for word in range(dimension):
        if all(((word >> site) & 1) == 0 for site in range(0, size, 2)):
            psi0[word] = amplitude
    return h0, q_ops, psi0


prior = json.loads(PRIOR.read_text())
execution_record = json.loads(EXECUTION_RECORD.read_text())

# On the alternating preparation and translation/reflection invariant ring,
# Delta q is period two and reflection removes the uniform circulation mode.
# The integrated continuity equation then fixes J_i=-Delta q_i/2. Check this
# reduction against every directly integrated current in the audited L4/L6/L8
# trajectory before using it for L10.
reduction_difference = 0.0
prior_period_two_difference = 0.0
for row in prior["rows"]:
    size = row["L"]
    q0 = np.array([0.0 if site % 2 == 0 else 0.5 for site in range(size)])
    q1 = np.array(row["q_after"])
    reconstructed = -0.5 * (q1 - q0)
    direct = np.array(row["integrated_oriented_currents"])
    reduction_difference = max(
        reduction_difference, float(np.max(np.abs(reconstructed - direct)))
    )
    prior_period_two_difference = max(
        prior_period_two_difference,
        float(np.max(np.abs(q1[::2] - q1[0]))),
        float(np.max(np.abs(q1[1::2] - q1[1]))),
    )

h0, q_ops, psi0 = build_ring(SIZE)
eigenvalues, eigenvectors = np.linalg.eigh(h0)
coefficients = np.einsum("ia,i->a", eigenvectors.conj(), psi0, optimize=False)
probabilities0 = np.abs(psi0) ** 2
q0 = np.array([np.dot(probabilities0, q) for q in q_ops])
number = np.array([bin(word).count("1") for word in range(1 << SIZE)], dtype=int)
number_law0 = np.array(
    [np.sum(probabilities0[number == count]) for count in range(SIZE + 1)]
)
hpsi0 = np.einsum("ij,j->i", h0, psi0, optimize=False)
initial_energy = float(np.vdot(psi0, hpsi0).real)

total_q = np.diag(number.astype(float))
onsite_commutator = np.einsum(
    "ij,jk->ik", h0, total_q, optimize=False
) - np.einsum("ij,jk->ik", total_q, h0, optimize=False)

rows = []
for kappa in KAPPAS:
    phase = np.exp(-1j * eigenvalues * kappa)
    psi = np.einsum("ia,a->i", eigenvectors, phase * coefficients, optimize=False)
    probabilities = np.abs(psi) ** 2
    q1 = np.array([np.dot(probabilities, q) for q in q_ops])
    currents = -0.5 * (q1 - q0)
    residuals = q1 - q0 + currents - np.roll(currents, 1)
    connected = []
    for site in range(SIZE):
        neighbor = (site + 1) % SIZE
        connected.append(
            float(
                np.dot(probabilities, q_ops[site] * q_ops[neighbor])
                - q1[site] * q1[neighbor]
            )
        )
    number_law = np.array(
        [np.sum(probabilities[number == count]) for count in range(SIZE + 1)]
    )
    hpsi = np.einsum("ij,j->i", h0, psi, optimize=False)
    throughput_per_cycle = float(np.sum(np.abs(currents)))
    cycles = SIZE * SIZE
    retained_total = float(cycles * np.sum(q1))
    throughput_total = cycles * throughput_per_cycle
    rows.append(
        {
            "L": SIZE,
            "kappa": kappa,
            "cycles": cycles,
            "sites_total": SIZE**3,
            "sites_per_F3_layer": SIZE**3 // 2,
            "possible_F3_links": (SIZE**3 // 2) ** 2,
            "selected_cycle_edges": SIZE**3,
            "prepared_source_lineages": SIZE**3 // 2,
            "expected_retained_total": retained_total,
            "q_after": q1.tolist(),
            "integrated_oriented_currents": currents.tolist(),
            "active_current_supports_per_cycle": int(np.sum(np.abs(currents) > 1.0e-12)),
            "absolute_oriented_throughput_per_cycle": throughput_per_cycle,
            "absolute_oriented_throughput_total": throughput_total,
            "throughput_per_retained_record": throughput_total / retained_total,
            "max_abs_connected_edge_correlation": float(np.max(np.abs(connected))),
            "record_ledger_residual_l1_per_cycle": float(np.sum(np.abs(residuals))),
            "record_ledger_residual_linf_per_cycle": float(np.max(np.abs(residuals))),
            "record_ledger_residual_l1_tiled_bound": float(cycles * np.sum(np.abs(residuals))),
            "period_two_occupation_error": float(
                max(
                    np.max(np.abs(q1[::2] - q1[0])),
                    np.max(np.abs(q1[1::2] - q1[1])),
                )
            ),
            "norm_error": float(abs(np.vdot(psi, psi).real - 1.0)),
            "energy_error": float(abs(np.vdot(psi, hpsi).real - initial_energy)),
            "number_law_max_change": float(
                np.max(np.abs(number_law - number_law0))
            ),
            "uniform_onsite_commutator_linf": float(
                np.max(np.abs(onsite_commutator))
            ),
        }
    )

prior_l8 = {row["kappa"]: row for row in prior["rows"] if row["L"] == 8}
ratios = []
for row in rows:
    l8 = prior_l8[row["kappa"]]
    if l8["absolute_oriented_throughput_total"] > 1.0e-14:
        total_ratio = (
            row["absolute_oriented_throughput_total"]
            / l8["absolute_oriented_throughput_total"]
        )
        per_record_ratio = (
            row["throughput_per_retained_record"]
            / l8["throughput_per_retained_record"]
        )
    else:
        total_ratio = None
        per_record_ratio = None
    ratios.append(
        {
            "kappa": row["kappa"],
            "L10_over_L8_throughput_total": total_ratio,
            "L10_over_L8_throughput_per_retained_record": per_record_ratio,
        }
    )

throughputs = [row["absolute_oriented_throughput_total"] for row in rows]
checks = [
    (len(rows) == 10, "ten-point L10 census"),
    (reduction_difference < 8.0e-12, "symmetry currents reproduce audited L4/L6/L8 currents"),
    (prior_period_two_difference < 8.0e-12, "audited lower-size period-two control"),
    (all(row["sites_total"] == 1000 and row["prepared_source_lineages"] == 500 for row in rows), "L10 site and lineage census"),
    (all(abs(row["expected_retained_total"] - 250.0) < 2.0e-11 for row in rows), "L10 retained total"),
    (rows[0]["active_current_supports_per_cycle"] == 0, "zero-kappa current control"),
    (all(row["active_current_supports_per_cycle"] == 10 for row in rows[1:]), "positive-kappa supports active"),
    (all(row["absolute_oriented_throughput_total"] > 0.0 for row in rows[1:]), "positive-kappa throughput"),
    (max(row["record_ledger_residual_l1_per_cycle"] for row in rows) < 1.0e-11, "ledger L1"),
    (max(row["record_ledger_residual_linf_per_cycle"] for row in rows) < 2.0e-12, "ledger Linf"),
    (max(row["period_two_occupation_error"] for row in rows) < 8.0e-12, "L10 period-two control"),
    (max(row["norm_error"] for row in rows) < 1.0e-13, "norm"),
    (max(row["energy_error"] for row in rows) < 2.0e-12, "energy"),
    (max(row["number_law_max_change"] for row in rows) < 1.0e-13, "number law"),
    (max(row["uniform_onsite_commutator_linf"] for row in rows) == 0.0, "uniform onsite commutator"),
    (any(throughputs[index + 1] < throughputs[index] for index in range(len(throughputs) - 1)), "finite throughput nonmonotone"),
    (0.0 < execution_record["observed_runtime_seconds"] < 30.0, "bounded observed runtime"),
    (0.0 < execution_record["observed_maximum_resident_set_mib"] < 48.0 * 1024.0, "bounded observed RSS"),
]
failures = [label for ok, label in checks if not ok]

out = {
    "schema": "R_AUTONOMOUS_L10_ACCUMULATION_V001",
    "classification": "CONDITIONAL_SUPPORT_AND_KAPPA__AUTONOMOUS_BS09_L10_MICROSCOPIC_ACCUMULATION",
    "scope": "MICROSCOPIC_RECORD_ACCUMULATION__NO_CONTINUUM_INFERENCE",
    "support_status": "CONDITIONAL_FIXED_CYCLE_PROGRAM__NOT_AUTONOMOUSLY_SELECTED",
    "parameter_status": "KAPPA_SCAN_IS_CONDITIONAL__T_AND_TAU_NOT_SEPARATELY_SELECTED",
    "source_status": "F3_MDC_PREPARED_HEADS__ADOPTED_ALPHA_R0__SOURCES_OFF_DURING_ACCUMULATION",
    "current_reconstruction": "PERIOD_TWO_PLUS_REFLECTION_AND_CONTINUITY_GIVE_J_I_EQUALS_MINUS_DELTA_Q_I_OVER_TWO",
    "lower_size_direct_current_max_abs_difference": reduction_difference,
    "rows": rows,
    "ratios": ratios,
    "execution": {
        "environment_memory_gib": 48,
        "cycle_hilbert_dimension": 1 << SIZE,
        "global_factorization": "100_DISJOINT_IDENTICAL_CYCLES__NO_2_POW_1000_STATE_ALLOCATED",
        "frozen_observation": "EXECUTION_RECORD.json",
    },
    "terminal_instrument": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "residual_status": "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS",
    "not_claimed": "AUTONOMOUS_SUPPORT_OR_PARAMETER_SELECTION__GENERIC_PHASE__GRID__CONTINUUM__WARD__GRAVITY",
}


def assert_compatible(observed: object, canonical: object, path: str = "root") -> None:
    """Validate a replay against the frozen record without hiding raw floats."""
    if isinstance(canonical, dict):
        if not isinstance(observed, dict) or set(observed) != set(canonical):
            raise AssertionError(f"canonical keys differ at {path}")
        for key in canonical:
            assert_compatible(observed[key], canonical[key], f"{path}.{key}")
        return
    if isinstance(canonical, list):
        if not isinstance(observed, list) or len(observed) != len(canonical):
            raise AssertionError(f"canonical list differs at {path}")
        for index, (left, right) in enumerate(zip(observed, canonical)):
            assert_compatible(left, right, f"{path}[{index}]")
        return
    if isinstance(canonical, float):
        if not isinstance(observed, (int, float)) or abs(float(observed) - canonical) > 8.0e-12:
            raise AssertionError(f"canonical float differs at {path}")
        return
    if observed != canonical:
        raise AssertionError(f"canonical value differs at {path}")


if OUT.exists():
    assert_compatible(out, json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

if failures:
    raise AssertionError(failures)
print(f"PASS__R_AUTONOMOUS_L10_ACCUMULATION__{len(checks)}/{len(checks)}")
