#!/usr/bin/env python3
"""New exclusive 64D BS11 held-feedback loop/source receipt; see its protocol."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import socket
import sys
import time
import traceback

ROOT = Path("/Users/bgm/Documents/ChatGPT/Universal Network Theory")
HERE = ROOT / "UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation"
PROTOCOL = HERE / "BS11_HELD_FEEDBACK_LOOP_SOURCE_V001.md"
SOURCE = HERE / "bs11_held_feedback_loop_source_v001.py"
JSON_RESULT = HERE / "BS11_HELD_FEEDBACK_LOOP_SOURCE_V001_RESULT.json"
MD_RESULT = HERE / "BS11_HELD_FEEDBACK_LOOP_SOURCE_V001_RESULT.md"
REFERENCES = [
    ROOT / "program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md",
    ROOT / "program-worktree/MODEL.md",
    HERE / "NATIVE_MATTER_LOADING_FORMATION_RESPONSE_V001.md",
]
UD = Fraction(1)
DELTA = Fraction(0)
LR = Fraction(1, 2)
LJ = Fraction(1, 4)
ER = EP = Fraction(1)
HS = (Fraction(2, 25), Fraction(1, 10), Fraction(7, 50))
PATTERNS = {
    "alternating": (0, 1, 0, 1, 0, 1),
    "cluster": (1, 1, 1, 0, 0, 0),
}
ALPHA, BETA, DIM = 21, 42, 64
OP_TOL, PARITY_TOL, NULL_FACTOR = 1e-11, 1e-8, 2e-10
MAX_RSS = 100 * 1024 * 1024


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_hashes():
    return {str(p): sha(p) for p in [PROTOCOL, SOURCE, *REFERENCES]}


def frozen_inputs():
    return {
        "dimension": DIM, "active_internal_edges": 6,
        "active_vertices": 6, "exterior_vertices": 6,
        "bipartite_N_per_side": 6, "Omega_rule": "6*h",
        "degree_target": 2, "native_d_star": 2, "exterior_degree": 1,
        "U_d": str(UD), "bare_Delta": str(DELTA),
        "lambda_R": str(LR), "lambda_J": str(LJ),
        "epsilon_r": str(ER), "epsilon_psi": str(EP),
        "carrier_hopping": 0, "all_copy_couplings": 0,
        "h": [str(h) for h in HS], "patterns": PATTERNS,
        "records": ["all0", "all1"], "exterior_records_carriers": 0,
        "ice_states": [ALPHA, BETA],
        "source": "whole twelve-node half-edge allocation, affine nodal lapse",
        "positions": "regular unit hexagon; corresponding exterior at 2*R",
        "weighted_source_arm": [1e-6, -2e-6],
        "operator_tolerance": OP_TOL, "parity_tolerance": PARITY_TOL,
        "source_null_factor": NULL_FACTOR,
        "nonzero_amplitude_threshold": "100*source_null_tolerance",
        "loop_label_minimum_ice_weight": 0.5,
        "splitting_ratio_is_non_gating": True,
        "BLAS_threads": 1, "peak_RSS_limit_bytes": MAX_RSS,
    }


def exact_diagonal(q, p):
    activity = tuple(p[v] + p[(v + 1) % 6] - 2*p[v]*p[(v + 1) % 6]
                     for v in range(6))
    bias = tuple(DELTA + LJ*a - 2*LR*q for a in activity)
    constant = 6*UD + 6*DELTA + 6*q*ER + 3*EP + 3*LJ - 6*LR*q
    energies, degrees = [], []
    for state in range(DIM):
        bits = tuple((state >> e) & 1 for e in range(6))
        ds = tuple(1 + bits[(v - 1) % 6] + bits[v] for v in range(6))
        energies.append(constant + UD*sum((d - 2)**2 for d in ds)
                        + sum(bias[e]*bits[e] for e in range(6)))
        degrees.append(ds)
    return activity, bias, constant, energies, degrees


def prefix_coefficient(energies, initial):
    coefficient = Fraction(0)
    minimum = None
    histories = 0
    for order in itertools.permutations(range(6)):
        state, weight = initial, Fraction(1)
        for e in order[:-1]:
            state ^= 1 << e
            gap = energies[state] - energies[initial]
            minimum = gap if minimum is None else min(minimum, gap)
            if gap <= 0:
                raise ArithmeticError(f"Nonpositive prefix gap {gap}, state={state}")
            weight /= gap
        coefficient += weight
        histories += 1
    return coefficient, minimum, histories


def subset_coefficient(energies, initial):
    # Independent path recurrence over toggled subsets, rather than permutations.
    values = {0: Fraction(1)}
    for size in range(1, 6):
        for subset in range(1, DIM):
            if subset.bit_count() != size:
                continue
            numerator = sum(values[subset ^ (1 << e)]
                            for e in range(6) if (subset >> e) & 1)
            gap = energies[initial ^ subset] - energies[initial]
            if gap <= 0:
                raise ArithmeticError("Subset recurrence found nonpositive gap")
            values[subset] = numerator / gap
    return sum(values[63 ^ (1 << e)] for e in range(6))


def execute():
    if sys.platform != "darwin":
        raise RuntimeError("This newly authorized worker is restricted to this Mac")
    if SOURCE.resolve() != Path(__file__).resolve():
        raise RuntimeError("Unexpected source location")
    if JSON_RESULT.exists() or MD_RESULT.exists():
        raise FileExistsError("Existing result forbids execution or overwriting")
    for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS",
                     "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
                     "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
        os.environ[variable] = "1"

    started = time.perf_counter()
    receipt = {
        "status": "RUNNING", "started_utc": datetime.now(timezone.utc).isoformat(),
        "host": socket.gethostname(), "platform": sys.platform, "pid": os.getpid(),
        "inputs": frozen_inputs(), "input_sha256": input_hashes(),
        "checks": [], "pattern_coefficients": [], "rows": [],
        "qualification": (
            "Finite held supported Hamiltonian and proposed nodal-lapse port only; "
            "no physical gravity, pressure, formation, h(s), criticality or fit."
        ),
    }

    def check(name, passed, evidence=None):
        item = {"name": name, "passed": bool(passed)}
        if evidence is not None:
            item["evidence"] = evidence
        receipt["checks"].append(item)

    try:
        import numpy as np
        identity = np.eye(DIM)
        states = np.arange(DIM)
        bits = np.array([[(int(s) >> e) & 1 for e in range(6)]
                         for s in states], dtype=float)
        n_ops = np.array([np.diag(bits[:, e]) for e in range(6)])
        x_ops = np.zeros((6, DIM, DIM))
        for e in range(6):
            x_ops[e, states, states ^ (1 << e)] = 1.0
        positions = np.array([(np.cos(2*np.pi*v/6), np.sin(2*np.pi*v/6))
                              for v in range(6)])
        all_positions = np.vstack([positions, 2*positions])
        receipt["positions"] = all_positions.tolist()
        ice_projector = np.zeros(DIM)
        ice_projector[[ALPHA, BETA]] = 1.0

        def rotation(shift):
            matrix = np.zeros((DIM, DIM))
            for state in range(DIM):
                target = sum(((state >> e) & 1) << ((e + shift) % 6)
                             for e in range(6))
                matrix[target, state] = 1.0
            return matrix

        rot1, rot3 = rotation(1), rotation(3)
        case_energy = {}
        for pattern, p in PATTERNS.items():
            for q in (0, 1):
                label = f"{pattern}_q{q}"
                activity, bias, constant, energies, degrees = exact_diagonal(q, p)
                ice_energy = energies[ALPHA]
                other_minimum = min(energies[s]-ice_energy for s in range(DIM)
                                    if s not in (ALPHA, BETA))
                check(label + ":equal_ice_energy", ice_energy == energies[BETA])
                check(label + ":ice_degrees", degrees[ALPHA] == (2,)*6
                      and degrees[BETA] == (2,)*6)
                check(label + ":only_two_classical_minima", other_minimum > 0,
                      {"minimum_other_gap": str(other_minimum)})
                cf, gf, nf = prefix_coefficient(energies, ALPHA)
                cr, gr, nr = prefix_coefficient(energies, BETA)
                check(label + ":720_forward_and_reverse", nf == nr == 720)
                check(label + ":positive_all_prefix_gaps", min(gf, gr) > 0,
                      {"minimum": str(min(gf, gr))})
                check(label + ":exact_forward_reverse", cf == cr)
                check(label + ":exact_subset_forward",
                      cf == subset_coefficient(energies, ALPHA))
                check(label + ":exact_subset_reverse",
                      cr == subset_coefficient(energies, BETA))
                c6 = (cf + cr)/2
                case_energy[(pattern, q)] = ice_energy
                receipt["pattern_coefficients"].append({
                    "pattern": pattern, "q": q, "activity": activity,
                    "bias": [str(b) for b in bias], "constant": str(constant),
                    "complete_ice_energy": str(ice_energy),
                    "minimum_classical_other_gap": str(other_minimum),
                    "minimum_prefix_gap": str(min(gf, gr)),
                    "c6_forward": str(cf), "c6_reverse": str(cr),
                    "c6_hermitian": str(c6),
                    "classical_energies": [str(e) for e in energies],
                })

                for hq in HS:
                    h = float(hq)
                    row_label = f"{label}_h{hq}"
                    diagonal = np.array([float(e) for e in energies])
                    H = np.diag(diagonal) - h*np.sum(x_ops, axis=0)
                    node_energy = np.zeros((12, DIM, DIM))
                    for v in range(6):
                        ds = 1 + bits[:, (v - 1) % 6] + bits[:, v]
                        node_energy[v] += np.diag(float(UD)*(ds - 2)**2)
                        node_energy[v] += float(q*ER + p[v]*EP)*identity
                        node_energy[v + 6] += float(UD)*identity
                        external = float(DELTA + LJ*p[v] - LR*q)*identity
                        node_energy[v] += external/2
                        node_energy[v + 6] += external/2
                    for e in range(6):
                        edge = -h*x_ops[e] + float(bias[e])*n_ops[e]
                        node_energy[e] += edge/2
                        node_energy[(e + 1) % 6] += edge/2
                    source_x = np.einsum("v,vij->ij", all_positions[:, 0],
                                         node_energy)
                    source_y = np.einsum("v,vij->ij", all_positions[:, 1],
                                         node_energy)

                    def weighted_direct(lapses):
                        # Separate construction from weighted node allocation.
                        value = np.zeros((DIM, DIM))
                        for v in range(6):
                            ds = 1 + bits[:, (v - 1) % 6] + bits[:, v]
                            value += lapses[v]*np.diag(float(UD)*(ds - 2)**2)
                            value += (lapses[v]*float(q*ER + p[v]*EP)
                                      + lapses[v + 6]*float(UD))*identity
                            value += ((lapses[v] + lapses[v + 6])/2
                                      * float(DELTA + LJ*p[v] - LR*q))*identity
                        for e in range(6):
                            weight = (lapses[e] + lapses[(e + 1) % 6])/2
                            value += weight*(-h*x_ops[e]
                                             + float(bias[e])*n_ops[e])
                        return value

                    H_norm = float(np.linalg.norm(H, 2))
                    source_norm = max(1.0, float(np.linalg.norm(source_x, 2)),
                                      float(np.linalg.norm(source_y, 2)))
                    null_tolerance = NULL_FACTOR*source_norm
                    check(row_label + ":hermitian",
                          np.max(np.abs(H - H.T)) <= OP_TOL)
                    check(row_label + ":whole_node_sum",
                          np.max(np.abs(np.sum(node_energy, axis=0)-H)) <= OP_TOL)
                    eta = np.array([1e-6, -2e-6])
                    lapses = 1 + all_positions @ eta
                    check(row_label + ":positive_lapse_arm", np.min(lapses) > 0)
                    weighted_nodes = np.einsum("v,vij->ij", lapses, node_energy)
                    weighted_other = weighted_direct(lapses)
                    check(row_label + ":weighted_independent_ownership",
                          np.max(np.abs(weighted_nodes-weighted_other)) <= OP_TOL)
                    check(row_label + ":affine_source",
                          np.max(np.abs(weighted_other
                                        - (H + eta[0]*source_x
                                           + eta[1]*source_y))) <= OP_TOL)
                    check(row_label + ":uniform_lapse",
                          np.max(np.abs(weighted_direct(np.full(12, .93))
                                        - .93*H)) <= OP_TOL)
                    check(row_label + ":rotation3_commutator",
                          np.max(np.abs(rot3@H-H@rot3)) <= OP_TOL)
                    if pattern == "alternating":
                        check(row_label + ":rotation1_commutator",
                              np.max(np.abs(rot1@H-H@rot1)) <= OP_TOL)
                        cosine, sine = np.cos(np.pi/3), np.sin(np.pi/3)
                        check(row_label + ":dipole_C6_covariance",
                              np.max(np.abs(rot1@source_x@rot1.T
                                            - cosine*source_x
                                            - sine*source_y)) <= OP_TOL)
                    for name, source in (("x", source_x), ("y", source_y)):
                        centered_source = source - np.trace(source)/DIM*identity
                        check(row_label + f":dipole_C2_odd_{name}",
                              np.max(np.abs(rot3@centered_source@rot3.T
                                            + centered_source)) <= OP_TOL)

                    centered_energies, vectors = np.linalg.eigh(
                        H - float(ice_energy)*identity)
                    complete_energies = centered_energies + float(ice_energy)
                    gaps = centered_energies[1:] - centered_energies[0]
                    ground, partner = vectors[:, 0], vectors[:, 1]
                    check(row_label + ":strict_ground_gap", float(gaps[0]) > 0)
                    residual = np.max(np.abs(
                        (H - float(ice_energy)*identity)@vectors
                        - vectors*centered_energies))
                    check(row_label + ":eigen_residual",
                          residual <= OP_TOL*max(1.0, H_norm),
                          {"maximum": float(residual)})
                    check(row_label + ":orthonormal",
                          np.max(np.abs(vectors.T@vectors-identity)) <= OP_TOL)
                    parity0 = float(ground@rot3@ground)
                    parity1 = float(partner@rot3@partner)
                    check(row_label + ":ground_C2_even", abs(parity0-1) <= PARITY_TOL)
                    check(row_label + ":partner_C2_odd", abs(parity1+1) <= PARITY_TOL)
                    weight0 = float(np.sum(ice_projector*ground**2))
                    weight1 = float(np.sum(ice_projector*partner**2))
                    check(row_label + ":majority_ice_ground", weight0 > .5)
                    check(row_label + ":majority_ice_partner", weight1 > .5)
                    if pattern == "alternating":
                        check(row_label + ":ground_C6_k0",
                              abs(float(ground@rot1@ground)-1) <= PARITY_TOL)
                        check(row_label + ":partner_C6_k3",
                              abs(float(partner@rot1@partner)+1) <= PARITY_TOL)

                    transitions = np.column_stack([
                        vectors[:, 1:].T @ source_x @ ground,
                        vectors[:, 1:].T @ source_y @ ground,
                    ])
                    soft_vector = transitions[0]
                    soft_amplitude = float(np.linalg.norm(soft_vector))
                    chi = 2*transitions.T@(transitions/gaps[:, None])
                    loop_chi = 2*np.outer(soft_vector, soft_vector)/gaps[0]
                    chi_minimum = float(np.min(np.linalg.eigvalsh(chi)))
                    check(row_label + ":chi_positive_semidefinite",
                          chi_minimum >= -OP_TOL*max(1.0,
                                                    float(np.linalg.norm(chi, 2))))
                    ward_transitions = vectors[:, 1:].T @ H @ ground
                    check(row_label + ":uniform_time_transition_null",
                          np.max(np.abs(ward_transitions))
                          <= OP_TOL*max(1.0, H_norm))
                    if pattern == "alternating":
                        check(row_label + ":soft_dipole_selection_null",
                              soft_amplitude <= null_tolerance,
                              {"amplitude": soft_amplitude,
                               "tolerance": null_tolerance})
                    else:
                        check(row_label + ":soft_dipole_nonzero",
                              soft_amplitude > 100*null_tolerance,
                              {"amplitude": soft_amplitude,
                               "threshold": 100*null_tolerance})
                    leading_split = 2*float(hq**6*c6)
                    direct_ice_vector = np.array([
                        (source_x[ALPHA, ALPHA]-source_x[BETA, BETA])/2,
                        (source_y[ALPHA, ALPHA]-source_y[BETA, BETA])/2,
                    ])
                    row = {
                        "pattern": pattern, "q": q, "h": h,
                        "h_fraction": str(hq), "Omega": 6*h,
                        "complete_ice_energy": float(ice_energy),
                        "complete_ground_energy": float(complete_energies[0]),
                        "complete_partner_energy": float(complete_energies[1]),
                        "centered_exact_gap": float(gaps[0]),
                        "sixth_order_leading_split": leading_split,
                        "exact_to_sixth_order_ratio": float(gaps[0])/leading_split,
                        "comparison_is_non_gating": True,
                        "ice_weights": [weight0, weight1],
                        "C2_parities": [parity0, parity1],
                        "source_identity_dipole": [
                            float(np.trace(source_x)/DIM),
                            float(np.trace(source_y)/DIM)],
                        "complete_ground_source_mean": [
                            float(ground@source_x@ground),
                            float(ground@source_y@ground)],
                        "classical_ice_soft_vector": direct_ice_vector.tolist(),
                        "soft_transition_vector": soft_vector.tolist(),
                        "soft_transition_norm": soft_amplitude,
                        "soft_transition_weight": soft_amplitude**2,
                        "source_null_tolerance": null_tolerance,
                        "chi_full": chi.tolist(), "chi_loop": loop_chi.tolist(),
                        "loop_fraction_of_chi_trace": (
                            float(np.trace(loop_chi)/np.trace(chi))
                            if np.trace(chi) > 0 else None),
                        "all_centered_eigenvalues": centered_energies.tolist(),
                        "all_complete_eigenvalues": complete_energies.tolist(),
                        "all_eigenvectors_columns": vectors.tolist(),
                        "all_source_transition_vectors": transitions.tolist(),
                        "matrix_sha256": {
                            name: hashlib.sha256(
                                np.ascontiguousarray(matrix, dtype="<f8").tobytes()
                            ).hexdigest()
                            for name, matrix in (("H", H), ("Gx", source_x),
                                                 ("Gy", source_y))
                        },
                    }
                    receipt["rows"].append(row)

        for pattern in PATTERNS:
            check(pattern + ":record_paid_classical_energy_match",
                  case_energy[(pattern, 0)] == case_energy[(pattern, 1)],
                  {"q0": str(case_energy[(pattern, 0)]),
                   "q1": str(case_energy[(pattern, 1)])})
        check("input_bytes_unchanged", input_hashes() == receipt["input_sha256"])
        maximum_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        check("under_100MiB_peak_RSS", maximum_rss < MAX_RSS,
              {"peak_bytes": maximum_rss, "limit_bytes": MAX_RSS})
        failures = [item for item in receipt["checks"] if not item["passed"]]
        receipt["status"] = "QUALIFIED_ARITHMETIC" if not failures else "FAILED"
    except Exception:
        receipt["status"] = "ERROR"
        receipt["exception"] = traceback.format_exc()

    receipt["completed_utc"] = datetime.now(timezone.utc).isoformat()
    receipt["runtime_seconds"] = time.perf_counter() - started
    receipt["peak_RSS_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt["check_count"] = len(receipt["checks"])
    receipt["passed_count"] = sum(item["passed"] for item in receipt["checks"])
    receipt["failed_count"] = receipt["check_count"] - receipt["passed_count"]
    payload = (json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False)
               + "\n").encode()
    payload_sha = hashlib.sha256(payload).hexdigest()
    lines = [
        "# BS11 held-feedback loop/source V001: saved result",
        "", f"Status: {receipt['status']}. "
        f"Checks {receipt['passed_count']}/{receipt['check_count']}; "
        f"failures {receipt['failed_count']}.", "",
        receipt["qualification"], "",
        "The four patterns and three h values were frozen before execution. "
        "All exact prefix coefficients are newly computed. Splitting ratios "
        "are descriptive outcomes, not accuracy gates or remainder bounds.", "",
        "| Pattern | q | c6 exact | ice energy | smallest classical gap |",
        "|---|---:|---|---|---|",
    ]
    for case in receipt["pattern_coefficients"]:
        lines.append(
            f"| {case['pattern']} | {case['q']} | {case['c6_hermitian']} | "
            f"{case['complete_ice_energy']} | {case['minimum_classical_other_gap']} |")
    lines += [
        "", "| Pattern | q | h | exact gap | gap/(2J6) | dipole amplitude | loop chi fraction |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in receipt["rows"]:
        fraction = row["loop_fraction_of_chi_trace"]
        fraction_text = "undefined" if fraction is None else f"{fraction:.9g}"
        lines.append(
            f"| {row['pattern']} | {row['q']} | {row['h']:.2f} | "
            f"{row['centered_exact_gap']:.12g} | "
            f"{row['exact_to_sixth_order_ratio']:.9g} | "
            f"{row['soft_transition_norm']:.12g} | {fraction_text} |")
    lines += [
        "", "Record q=0/q=1 classical ice energies are matched by their "
        "retained storage/feedback terms. The carrier activity patterns "
        "have different energies and are not an energy-matched comparison.",
        "", "Alternating-case dipole null and cluster-case nonzero gates test "
        "this predeclared operational source. Neither identifies physical "
        "gravity or a universal source law. All mean identity-source offsets "
        "and complete energies are retained in JSON.",
        "", "The JSON retains all 64 eigenvalues/eigenvectors for every new "
        "finite-h row and all source transition vectors. External clamps, "
        "static records/carriers, full source ownership and the lack of a "
        "formation/pressure interpretation remain part of the result.",
        "", f"Runtime {receipt['runtime_seconds']:.6g}s; "
        f"peak process RSS {receipt['peak_RSS_bytes']} bytes; "
        f"PID {receipt['pid']}.", "",
        f"Result JSON SHA256: {payload_sha}", "",
        "Input SHA256 custody:",
    ]
    for path, digest in receipt["input_sha256"].items():
        lines.append(f"- {path}: {digest}")
    failed_items = [item for item in receipt["checks"] if not item["passed"]]
    if failed_items:
        lines += ["", "Failed gates are preserved:"]
        lines += ["- " + item["name"] + ": " + json.dumps(item.get("evidence"))
                  for item in failed_items]
    if "exception" in receipt:
        lines += ["", "The ERROR receipt preserves its traceback in JSON."]
    markdown = "\n".join(lines) + "\n"
    # Exclusive single-write result destinations; never replace an old receipt.
    with JSON_RESULT.open("xb") as handle:
        handle.write(payload)
    with MD_RESULT.open("x", encoding="utf-8") as handle:
        handle.write(markdown)
    print(json.dumps({
        "status": receipt["status"], "checks": receipt["check_count"],
        "passed": receipt["passed_count"], "failed": receipt["failed_count"],
        "rows": len(receipt["rows"]),
        "runtime_seconds": receipt["runtime_seconds"],
        "peak_RSS_bytes": receipt["peak_RSS_bytes"],
        "json_sha256": payload_sha,
        "json_path": str(JSON_RESULT), "markdown_path": str(MD_RESULT),
        "failed_gates": [item["name"] for item in failed_items],
        "exception": receipt.get("exception"),
    }, indent=2))
    return 0 if receipt["status"] == "QUALIFIED_ARITHMETIC" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true",
                        help="Root-approved single numerical execution")
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps({"mode": "describe_only", "inputs": frozen_inputs(),
                          "input_sha256": input_hashes()}, indent=2))
        return 0
    return execute()


if __name__ == "__main__":
    sys.exit(main())
