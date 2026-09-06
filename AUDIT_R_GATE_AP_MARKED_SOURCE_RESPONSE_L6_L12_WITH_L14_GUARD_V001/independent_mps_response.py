#!/usr/bin/env python3
"""Independent periodic-rung MPS response reconstruction.

This is deliberately separate from the target marked-orbit implementation.
Two graph sites are grouped into each four-state rung.  A fourth-order
Suzuki/Yoshida TEBD evolves open-boundary MPS tensors.  The MPS cut is moved
around the finite cycle by exact local SWAP gates, so every Hamiltonian gate
is nearest-neighbour when it is applied.  Complete currents are integrated
by composite Simpson quadrature.
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import time
from pathlib import Path

import numpy as np


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--length", type=int, choices=(6, 8, 10, 12), required=True)
PARSER.add_argument("--coarse-steps", type=int, default=16)
PARSER.add_argument("--fine-steps", type=int, default=32)
PARSER.add_argument("--max-bond", type=int, default=192)
PARSER.add_argument("--cutoff", type=float, default=1e-12)
ARGS = PARSER.parse_args()

LENGTH = ARGS.length
KAPPA = math.pi / 2.0
ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "DEVELOPMENT_R_GATE_AP_MARKED_SOURCE_ENGINE_V001" / f"RESULT_L{LENGTH}.json"
STARTED = time.perf_counter()
D = 4


def edge_hamiltonian():
    h = np.zeros((4, 4), dtype=complex)
    # Pair basis |00>, |01>, |10>, |11>.
    h[1, 2] = -1.0
    h[2, 1] = -1.0
    return h


def edge_current():
    j = np.zeros((4, 4), dtype=complex)
    j[1, 2] = 1.0j
    j[2, 1] = -1.0j
    return j


I2 = np.eye(2, dtype=complex)
Q2 = np.diag([0.0, 1.0]).astype(complex)
ANN = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
CREATE = ANN.T
QA = np.kron(Q2, I2)
QC = np.kron(I2, Q2)
ANN_A = np.kron(ANN, I2)
CREATE_A = np.kron(CREATE, I2)
ANN_C = np.kron(I2, ANN)
CREATE_C = np.kron(I2, CREATE)
H_CONNECTOR = edge_hamiltonian()
J_CONNECTOR = edge_current()


def two_rung_operator(single_pair_operator, component):
    out = np.zeros((D, D, D, D), dtype=complex)
    # Rung state index is 2*A+C.  Pair operator basis is |left,right>.
    for left_out in range(D):
        ao, co = divmod(left_out, 2)
        for right_out in range(D):
            bo, do = divmod(right_out, 2)
            for left_in in range(D):
                ai, ci = divmod(left_in, 2)
                for right_in in range(D):
                    bi, di = divmod(right_in, 2)
                    if component == "A" and co == ci and do == di:
                        out[left_out, right_out, left_in, right_in] = single_pair_operator[2 * ao + bo, 2 * ai + bi]
                    if component == "C" and ao == ai and bo == bi:
                        out[left_out, right_out, left_in, right_in] = single_pair_operator[2 * co + do, 2 * ci + di]
    return out


H_BOND = two_rung_operator(H_CONNECTOR, "A") + two_rung_operator(H_CONNECTOR, "C")
J_BOND_A = two_rung_operator(J_CONNECTOR, "A")
J_BOND_C = two_rung_operator(J_CONNECTOR, "C")


def swap_gate():
    out = np.zeros((D, D, D, D), dtype=complex)
    for left in range(D):
        for right in range(D):
            out[right, left, left, right] = 1.0
    return out


SWAP = swap_gate()


def unitary(matrix, time_step, pair=False):
    shape = matrix.shape
    flat = matrix.reshape(D * D, D * D) if pair else matrix
    values, vectors = np.linalg.eigh(flat)
    phased = vectors * np.exp(-1.0j * time_step * values)
    # einsum avoids a spurious Accelerate complex-matmul warning on Python 3.9.
    gate = np.einsum("ik,jk->ij", phased, vectors.conj(), optimize=True)
    return gate.reshape(shape)


def product_mps(local_vectors):
    return [vector.reshape(1, D, 1).astype(complex) for vector in local_vectors]


def apply_one(tensor, gate):
    return np.einsum("pq,lqr->lpr", gate, tensor, optimize=True)


def apply_pair(mps, position, gate, max_bond, cutoff, tracker):
    left = mps[position]
    right = mps[position + 1]
    theta = np.einsum("lam,mbr->labr", left, right, optimize=True)
    theta = np.einsum("ABab,labr->lABr", gate, theta, optimize=True)
    ldim, _, _, rdim = theta.shape
    matrix = theta.reshape(ldim * D, D * rdim)
    u, singular, vh = np.linalg.svd(matrix, full_matrices=False)
    relative = cutoff * singular[0] if singular.size else 0.0
    keep = min(max_bond, max(1, int(np.sum(singular > relative))))
    discarded = float(np.sqrt(np.sum(singular[keep:] ** 2)))
    tracker["max_discarded_norm"] = max(tracker["max_discarded_norm"], discarded)
    tracker["sum_discarded_norm"] += discarded
    tracker["max_observed_bond"] = max(tracker["max_observed_bond"], keep)
    mps[position] = u[:, :keep].reshape(ldim, D, keep)
    mps[position + 1] = (singular[:keep, None] * vh[:keep]).reshape(keep, D, rdim)


def right_canonicalize(mps):
    """Put every tensor right of the first site in right-canonical form."""
    for position in range(LENGTH - 1, 0, -1):
        tensor = mps[position]
        left_dim, _, right_dim = tensor.shape
        q, r = np.linalg.qr(tensor.reshape(left_dim, D * right_dim).T)
        rank = q.shape[1]
        mps[position] = q.T.reshape(rank, D, right_dim)
        mps[position - 1] = np.einsum(
            "lpa,ab->lpb", mps[position - 1], r.T, optimize=True
        )


def shift_center_right(mps, position):
    """Move the orthogonality center from one site to the following site."""
    tensor = mps[position]
    left_dim, _, right_dim = tensor.shape
    q, r = np.linalg.qr(tensor.reshape(left_dim * D, right_dim))
    rank = q.shape[1]
    mps[position] = q.reshape(left_dim, D, rank)
    mps[position + 1] = np.einsum(
        "ab,bpc->apc", r, mps[position + 1], optimize=True
    )


def rotate_cut_left(mps, labels, max_bond, cutoff, tracker):
    """Move the first physical rung to the end without changing the state."""
    right_canonicalize(mps)
    for position in range(LENGTH - 1):
        apply_pair(mps, position, SWAP, max_bond, cutoff, tracker)
        labels[position], labels[position + 1] = labels[position + 1], labels[position]


def apply_cycle_matching(mps, labels, parity, gate, max_bond, cutoff, tracker):
    """Apply the cycle matching whose oriented left labels have given parity."""
    if labels[0] % 2 != parity:
        raise AssertionError("MPS cut parity does not match requested cycle matching")
    right_canonicalize(mps)
    for position in range(0, LENGTH, 2):
        left_label = labels[position]
        right_label = labels[position + 1]
        if right_label != (left_label + 1) % LENGTH or left_label % 2 != parity:
            raise AssertionError("cyclic MPS label/matching mismatch")
        apply_pair(mps, position, gate, max_bond, cutoff, tracker)
        if position + 2 < LENGTH:
            shift_center_right(mps, position + 1)


def left_environments(mps):
    envs = [np.ones((1, 1), dtype=complex)]
    for tensor in mps:
        envs.append(np.einsum("ab,apc,bpd->cd", envs[-1], tensor.conj(), tensor, optimize=True))
    return envs


def right_environments(mps):
    envs = [None] * (len(mps) + 1)
    envs[-1] = np.ones((1, 1), dtype=complex)
    for position in range(len(mps) - 1, -1, -1):
        tensor = mps[position]
        envs[position] = np.einsum("apc,bpd,cd->ab", tensor.conj(), tensor, envs[position + 1], optimize=True)
    return envs


def expect_one(mps, position, operator, left_envs, right_envs):
    tensor = mps[position]
    value = np.einsum(
        "ab,apc,pq,bqd,cd->", left_envs[position], tensor.conj(),
        operator, tensor, right_envs[position + 1], optimize=True,
    )
    return value


def expect_adjacent(mps, position, operator, left_envs, right_envs):
    theta = np.einsum("lam,mbr->labr", mps[position], mps[position + 1], optimize=True)
    value = np.einsum(
        "xy,xabr,abAB,yABs,rs->", left_envs[position], theta.conj(),
        operator, theta, right_envs[position + 2], optimize=True,
    )
    return value


def expect_product(mps, operators):
    env = np.ones((1, 1), dtype=complex)
    identity = np.eye(D, dtype=complex)
    for position, tensor in enumerate(mps):
        operator = operators.get(position, identity)
        env = np.einsum("ab,apc,pq,bqd->cd", env, tensor.conj(), operator, tensor, optimize=True)
    return env[0, 0]


def norm(mps):
    return float(left_environments(mps)[-1][0, 0].real)


def observe(mps, labels):
    left_envs = left_environments(mps)
    right_envs = right_environments(mps)
    normalization = left_envs[-1][0, 0]
    occupations_a = [0.0] * LENGTH
    occupations_c = [0.0] * LENGTH
    for position, rung in enumerate(labels):
        occupations_a[rung] = float(
            (expect_one(mps, position, QA, left_envs, right_envs) / normalization).real
        )
        occupations_c[rung] = float(
            (expect_one(mps, position, QC, left_envs, right_envs) / normalization).real
        )
    # Convert C_i=B_{i+1} back to target B-site order.
    occupations_b = [occupations_c[(site - 1) % LENGTH] for site in range(LENGTH)]
    current_a = [0.0] * LENGTH
    current_b = [0.0] * LENGTH
    for position in range(LENGTH - 1):
        rung = labels[position]
        if labels[position + 1] != (rung + 1) % LENGTH:
            raise AssertionError("MPS order is not a cyclic rung order")
        current_a[rung] = float(
            (expect_adjacent(mps, position, J_BOND_A, left_envs, right_envs) / normalization).real
        )
        current_b[(rung + 1) % LENGTH] = float(
            (expect_adjacent(mps, position, J_BOND_C, left_envs, right_envs) / normalization).real
        )
    # The only non-adjacent cycle bond crosses the current MPS cut.
    cut_rung = labels[-1]
    if labels[0] != (cut_rung + 1) % LENGTH:
        raise AssertionError("MPS cut does not close the rung cycle")
    periodic_a = 1.0j * (
        expect_product(mps, {0: CREATE_A, LENGTH - 1: ANN_A})
        - expect_product(mps, {0: ANN_A, LENGTH - 1: CREATE_A})
    ) / normalization
    periodic_c = 1.0j * (
        expect_product(mps, {0: CREATE_C, LENGTH - 1: ANN_C})
        - expect_product(mps, {0: ANN_C, LENGTH - 1: CREATE_C})
    ) / normalization
    current_a[cut_rung] = float(periodic_a.real)
    current_b[(cut_rung + 1) % LENGTH] = float(periodic_c.real)
    connectors = [0.0] * LENGTH
    for position, rung in enumerate(labels):
        connectors[rung] = float(
            (expect_one(mps, position, J_CONNECTOR, left_envs, right_envs) / normalization).real
        )
    return np.array(occupations_a + occupations_b), np.array(current_a + current_b + connectors)


def second_order(mps, labels, step, max_bond, cutoff, tracker, gate_cache):
    key = float(step)
    if key not in gate_cache:
        gate_cache[key] = (
            unitary(H_CONNECTOR, 0.5 * step),
            unitary(H_BOND, 0.5 * step, pair=True),
            unitary(H_BOND, step, pair=True),
        )
    onsite_half, even_half, odd_full = gate_cache[key]
    for rung in range(LENGTH):
        mps[rung] = apply_one(mps[rung], onsite_half)
    apply_cycle_matching(mps, labels, 0, even_half, max_bond, cutoff, tracker)
    rotate_cut_left(mps, labels, max_bond, cutoff, tracker)
    apply_cycle_matching(mps, labels, 1, odd_full, max_bond, cutoff, tracker)
    rotate_cut_left(mps, labels, max_bond, cutoff, tracker)
    apply_cycle_matching(mps, labels, 0, even_half, max_bond, cutoff, tracker)
    for rung in range(LENGTH):
        mps[rung] = apply_one(mps[rung], onsite_half)


def fourth_order_step(mps, labels, step, max_bond, cutoff, tracker, gate_cache):
    p1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
    p2 = 1.0 - 2.0 * p1
    second_order(mps, labels, p1 * step, max_bond, cutoff, tracker, gate_cache)
    second_order(mps, labels, p2 * step, max_bond, cutoff, tracker, gate_cache)
    second_order(mps, labels, p1 * step, max_bond, cutoff, tracker, gate_cache)


def initial_vectors(perturbed):
    vectors = []
    blank = np.array([1.0, 0.0], dtype=complex)
    plus = np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0)
    source = np.array([1.0, -1.0j], dtype=complex) / math.sqrt(2.0)
    for rung in range(LENGTH):
        a_state = plus if rung % 2 else blank
        c_state = plus if rung % 2 == 0 else blank
        if perturbed and rung == 0:
            a_state = source
        vectors.append(np.kron(a_state, c_state))
    return vectors


def evolve(step_count, perturbed, max_bond, cutoff):
    mps = product_mps(initial_vectors(perturbed))
    labels = list(range(LENGTH))
    q_initial, current_initial = observe(mps, labels)
    integrated = current_initial.copy()
    step = KAPPA / step_count
    tracker = {"max_discarded_norm": 0.0, "sum_discarded_norm": 0.0, "max_observed_bond": 1}
    gate_cache = {}
    quarter = max(1, step_count // 4)
    for index in range(1, step_count + 1):
        fourth_order_step(mps, labels, step, max_bond, cutoff, tracker, gate_cache)
        _, current = observe(mps, labels)
        weight = 1.0 if index == step_count else (4.0 if index % 2 else 2.0)
        integrated += weight * current
        if index % quarter == 0:
            print(
                f"PROGRESS_L{LENGTH}_{'PERT' if perturbed else 'BASE'}_{step_count}={index}/{step_count}"
                f"__CHI={tracker['max_observed_bond']}__DISCARD={tracker['max_discarded_norm']:.3e}",
                flush=True,
            )
    q_final, _ = observe(mps, labels)
    return {
        "q_initial": q_initial,
        "q_final": q_final,
        "integrated_current": integrated * step / 3.0,
        "norm": norm(mps),
        "tracker": tracker,
    }


def run_resolution(step_count):
    baseline = evolve(step_count, False, ARGS.max_bond, ARGS.cutoff)
    perturbed = evolve(step_count, True, ARGS.max_bond, ARGS.cutoff)
    return baseline, perturbed


coarse_baseline, coarse_perturbed = run_resolution(ARGS.coarse_steps)
fine_baseline, fine_perturbed = run_resolution(ARGS.fine_steps)
target = json.loads(TARGET.read_text())
target_q0 = np.array([row["baseline_q_after"] for row in target["site_records"]])
target_q1 = np.array([row["perturbed_q_after"] for row in target["site_records"]])
target_j0 = np.array([row["baseline_J"] for row in target["edge_records"]])
target_j1 = np.array([row["perturbed_J"] for row in target["edge_records"]])

q0 = fine_baseline["q_final"]
q1 = fine_perturbed["q_final"]
j0 = fine_baseline["integrated_current"]
j1 = fine_perturbed["integrated_current"]
dq = q1 - q0
dj = j1 - j0
edges = []
for ring in range(2):
    for site in range(LENGTH):
        edges.append((ring * LENGTH + site, ring * LENGTH + (site + 1) % LENGTH, "internal"))
for site in range(LENGTH):
    edges.append((site, LENGTH + (site + 1) % LENGTH, "connector"))
incidence = np.zeros((2 * LENGTH, 3 * LENGTH))
for index, (left, right, _) in enumerate(edges):
    incidence[left, index] = 1.0
    incidence[right, index] = -1.0
source = np.zeros(2 * LENGTH)
source[0] = 0.5
residual = dq + incidence @ dj - source

out = {
    "schema": f"AUDIT_R_GATE_AP_INDEPENDENT_PERIODIC_RUNG_MPS_L{LENGTH}_V001",
    "method": "FOURTH_ORDER_YOSHIDA_TEBD__FOUR_STATE_RUNGS__CYCLIC_CUT_EXACT_LOCAL_SWAPS__COMPOSITE_SIMPSON_CURRENT",
    "parameters": {
        "L": LENGTH,
        "coarse_steps": ARGS.coarse_steps,
        "fine_steps": ARGS.fine_steps,
        "max_bond": ARGS.max_bond,
        "relative_svd_cutoff": ARGS.cutoff,
        "kappa": KAPPA,
    },
    "complete_vectors": {
        "baseline_q_after": q0.tolist(),
        "perturbed_q_after": q1.tolist(),
        "delta_q_after": dq.tolist(),
        "baseline_J": j0.tolist(),
        "perturbed_J": j1.tolist(),
        "delta_J": dj.tolist(),
    },
    "target_reproduction_linf": {
        "baseline_q": float(np.max(abs(q0 - target_q0))),
        "perturbed_q": float(np.max(abs(q1 - target_q1))),
        "delta_q": float(np.max(abs(dq - (target_q1 - target_q0)))),
        "baseline_J": float(np.max(abs(j0 - target_j0))),
        "perturbed_J": float(np.max(abs(j1 - target_j1))),
        "delta_J": float(np.max(abs(dj - (target_j1 - target_j0)))),
    },
    "coarse_fine_linf": {
        "baseline_q": float(np.max(abs(q0 - coarse_baseline["q_final"]))),
        "perturbed_q": float(np.max(abs(q1 - coarse_perturbed["q_final"]))),
        "baseline_J": float(np.max(abs(j0 - coarse_baseline["integrated_current"]))),
        "perturbed_J": float(np.max(abs(j1 - coarse_perturbed["integrated_current"]))),
    },
    "differential_ledger": {
        "L1": float(np.sum(abs(residual))),
        "Linf": float(np.max(abs(residual))),
        "delta_q_sum": float(np.sum(dq)),
        "incidence_column_sum_linf": float(np.max(abs(np.sum(incidence, axis=0)))),
    },
    "norms": {
        "baseline": fine_baseline["norm"],
        "perturbed": fine_perturbed["norm"],
    },
    "truncation": {
        "coarse_baseline": coarse_baseline["tracker"],
        "coarse_perturbed": coarse_perturbed["tracker"],
        "fine_baseline": fine_baseline["tracker"],
        "fine_perturbed": fine_perturbed["tracker"],
    },
    "not_claimed": "EXACT_MPS_EQUALITY__LOCALITY_OR_SCALING_LAW__PHYSICAL_DISTANCE_OR_BOUNDARY__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY",
}
print("INDEPENDENT_MPS_RESULT_BEGIN")
print(json.dumps(out, indent=2, sort_keys=True))
print("INDEPENDENT_MPS_RESULT_END")
print(f"INDEPENDENT_MPS_RUNTIME_SECONDS={time.perf_counter() - STARTED:.9f}")
print(f"INDEPENDENT_MPS_MAX_RSS_RAW={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
