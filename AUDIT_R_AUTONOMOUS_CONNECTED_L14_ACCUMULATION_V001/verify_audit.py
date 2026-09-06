#!/usr/bin/env python3
"""Verify sealed custody and arithmetic of the independent L14 PASS packet."""

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001"

TARGET_PINS = {
    "README.md": "f1d40ecd46dab30ad2ba78059c8d57f441e422ab67e473dc35ffaa30a0ff85da",
    "RESULT.json": "e8134d5311b9bdfd62ce7df5988da803b110516606ce905a1bc49bd65cdb5fbe",
    "RESULT.md": "81e37ce367f9fd22a8a70ebc38e1268c5a5e53d4384a4f91cf6ce6096f3fdb76",
    "RUN_OBSERVATION.md": "251259486852b4b7677eb370fc1126a3466c9e1acc5daf3c6cbb8dd3e6cdc816",
    "THEOREM.md": "526ed6c51c878272c9845ca4a9822a419d97820b8b41c6c09f549ee8ab74da1a",
    "compute_connected_l14.py": "b136a8d1fb5ea1d44c6aa771745b696a48140bf62bbbdc7cb3ab941b87ec5319",
}
AUDIT_PINS = {
    "README.md": "9aac3d1e996c597439d06e17baf3d4bd039f72a141774d70c6f99cbdbaa30045",
    "REPORT.md": "806f67f07b01ff629032a781dcd201d1b37898c322ab5a5e6a99a343910c50a3",
    "RESULT.json": "cf4301e55f0c911196ecfbd2f02d60ebcfc32def3353472dccb87077ca77d204",
    "RESULT.md": "4984418bc9556a5b8458fc3542a91b470c1e10d66f738cce350e35eed892a819",
    "RUN_OBSERVATION.md": "21b41aa0a01a5914e32f43815253ff7f27211b6e686439c5e4de96d6752f7a4c",
    "independent_reconstruction.py": "5078fed910e0c9348bf22a36e75d2a530851408e7ad9bf8f5c9101595dd888fa",
    "INDEPENDENT_RESULT.json": "bfa8fd0eb4ff793662af546408882b84ba55ec0ff38145263d8c9747660919be",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = []


def check(condition, label):
    checks.append((bool(condition), label))


check(all(digest(TARGET / name) == pin for name, pin in TARGET_PINS.items()), "target custody pins")
check(all(digest(HERE / name) == pin for name, pin in AUDIT_PINS.items()), "audit custody pins")

target = json.loads((TARGET / "RESULT.json").read_text())
audit = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
summary = json.loads((HERE / "RESULT.json").read_text())
check(target["checks_passed"] == target["checks_total"] == 28, "target canonical 28/28")
check(audit["checks_passed"] == audit["checks_total"] == 29 and not audit["failures"], "independent 29/29")
check(audit["verdict"] == "PASS__INDEPENDENT_L14_NUMERICAL_RECONSTRUCTION", "independent PASS verdict")
check(summary["verdict"] == audit["verdict"], "summary PASS verdict")
check(summary["target_disposition"] == "ELIGIBLE_FOR_PROMOTION_WITH_CLAIM_CEILINGS", "bounded target disposition")

basis = audit["finite_orbit_basis"]
histogram = basis["orbit_size_histogram"]
check(basis["full_dimension"] == 1 << 28, "full word census")
check(basis["finite_group_order"] == 28, "finite group census")
check(basis["orbit_dimension"] == 9_608_050, "generator-BFS orbit census")
check(histogram == {"1": 4, "2": 6, "7": 252, "14": 41742, "28": 9566046}, "orbit histogram")
check(sum(int(size) * count for size, count in histogram.items()) == 1 << 28, "complete orbit coverage")
check(basis["aggregated_csr_entries"] == 201_326_276 < 201_769_050, "aggregated entry census")
check(8 * (9_608_050 + 1) + 15 * 201_326_276 == basis["aggregated_csr_bytes"] == 3_096_758_548, "aggregated fixed-width bytes")
check(basis["signed_edge_orbits"] == 2, "signed edge orbit census")
check("NO_PYTHON_OBJECTS_PROPORTIONAL_TO_TRANSITIONS" in basis["storage_status"], "fixed-width storage ceiling")

l4 = audit["l4_full_space_validation"]
check(l4["orbit_dimension"] == 55 and l4["aggregated_entries"] == 184, "L4 independent quotient census")
check(l4["full_space_action_linf"] < 2e-14, "L4 full-space action")
check(l4["full_space_current_linf"] < 2e-14, "L4 full-space currents")
check(l4["full_space_diagonal_linf"] < 2e-14, "L4 representative diagonals")

q0 = audit["q_before"]
q = audit["q_after"]
currents = audit["integrated_oriented_currents"]
check(len(q0) == len(q) == 28, "occupation vector lengths")
check(len(currents) == 42, "oriented current vector length")
check(all(abs(q[index] - q[index % 2]) < 2e-15 for index in range(28)), "parity occupation orbit")
check(all(abs(currents[index] - currents[index % 2]) < 2e-15 for index in range(28)), "internal signed current orbit")
check(all(abs(currents[index] - currents[28 + (index - 28) % 2]) < 2e-15 for index in range(28, 42)), "connector signed current orbit")
check(all(abs(value) > 1e-10 for value in currents), "all oriented currents active")

balance = [0.0] * 28
edges = []
for layer in range(2):
    for site in range(14):
        edges.append((layer * 14 + site, layer * 14 + (site + 1) % 14))
for site in range(14):
    edges.append((site, 14 + (site + 1) % 14))
for current, (u, v) in zip(currents, edges):
    balance[u] += current
    balance[v] -= current
residual = [q[index] - q0[index] + balance[index] for index in range(28)]
residual_l1 = sum(abs(value) for value in residual)
residual_linf = max(abs(value) for value in residual)
check(abs(residual_l1 - audit["record_ledger_residual_l1_per_component"]) < 3e-15, "explicit owner-edge residual L1")
check(abs(residual_linf - audit["record_ledger_residual_linf_per_component"]) < 3e-15, "explicit owner-edge residual Linf")
check(abs(98 * residual_l1 - audit["record_ledger_residual_l1_global_bound"]) < 3e-13, "global residual bound")
check(audit["residual_status"] == "RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS", "raw residual status")

target_q_linf = max(abs(left - right) for left, right in zip(q, target["q_after"]))
target_current_linf = max(abs(left - right) for left, right in zip(currents, target["integrated_oriented_currents"]))
check(abs(target_q_linf - audit["target_reproduction"]["q_linf"]) < 2e-16 and target_q_linf < 6e-9, "target occupations")
check(abs(target_current_linf - audit["target_reproduction"]["current_linf"]) < 2e-16 and target_current_linf < 6e-9, "all target oriented currents")
check(audit["target_reproduction"]["correlation_abs"] < 6e-9, "target correlation metric")
check(audit["target_reproduction"]["retained_abs"] < 2e-7, "target retained total")
check(audit["target_reproduction"]["total_throughput_abs"] < 3e-6, "target total throughput")
check(audit["target_reproduction"]["connector_throughput_abs"] < 2e-6, "target connector throughput")

throughput = 98 * sum(abs(value) for value in currents)
connector = 98 * sum(abs(value) for value in currents[28:])
check(abs(throughput - audit["absolute_oriented_throughput_global"]) < 3e-12, "independent total throughput arithmetic")
check(abs(connector - audit["absolute_connector_throughput_global"]) < 3e-12, "independent connector throughput arithmetic")
check(abs(98 * sum(q) - audit["expected_retained_global"]) < 3e-12, "independent retained arithmetic")

comparator_error = max(
    abs(audit["comparators"][key][field] - target["comparators"][key][field])
    for key in target["comparators"]
    for field in target["comparators"][key]
)
check(abs(comparator_error - audit["target_reproduction"]["all_comparator_linf"]) < 2e-15, "all comparator difference arithmetic")
check(comparator_error < 6e-8 and len(audit["comparators"]) == 5, "all total and connector comparators")

target_l1_difference = abs(residual_l1 - target["record_ledger_residual_l1_per_component"])
target_linf_difference = abs(residual_linf - target["record_ledger_residual_linf_per_component"])
check(abs(target_l1_difference - summary["target_reproduction"]["raw_residual_l1_norm_abs"]) < 3e-15, "target raw residual L1 norm")
check(abs(target_linf_difference - summary["target_reproduction"]["raw_residual_linf_norm_abs"]) < 3e-15, "target raw residual Linf norm")

check(audit["state_refinement_linf"] < 2e-8, "state refinement")
check(audit["occupation_refinement_linf"] < 2e-8, "occupation refinement")
check(audit["current_refinement_linf"] < 2e-8, "current refinement")
check(audit["record_ledger_residual_l1_per_component"] < 2e-8, "raw residual L1 bound")
check(audit["record_ledger_residual_linf_per_component"] < 2e-9, "raw residual Linf bound")
check(audit["norm_error"] < 2e-8, "norm")
check(audit["energy_error"] < 2e-7 and audit["energy_imag_abs"] < 2e-8, "energy")
check(audit["number_law_max_change"] < 2e-8, "number-sector law")
check(audit["runtime_seconds"] > 0 and audit["max_rss_bytes"] == 5_746_900_992, "runtime and RSS logged")
check(audit["max_rss_bytes"] < audit["guard_bytes"] == 40 * (1 << 30), "resource guard")

check(audit["history"][:3] == [
    "PRIOR_FAIL_CLOSED__NO_INDEPENDENT_L14_EVOLUTION",
    "REJECTED_FULL_WORD_KERNEL_LIFT__NOT_MEMORY_BOUNDED",
    "REJECTED_PYTHON_OBJECT_TRANSITION_LIFT__NOT_MEMORY_BOUNDED",
], "prior fail-closed history retained")
check(audit["claim_ceiling"] == "CONDITIONAL_MICROSCOPIC_NUMERICAL_RECORD_ONLY", "claim ceiling")
check(audit["not_claimed"] == "CONVERGENCE__LIMIT__FIT__SCALING__AUTONOMOUS_SUPPORT__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY", "prohibited promotions withheld")

failures = [label for passed, label in checks if not passed]
if failures:
    raise AssertionError(failures)
print(f"PASS__HOSTILE_L14_AUDIT_PACKET__{len(checks)}/{len(checks)}")
