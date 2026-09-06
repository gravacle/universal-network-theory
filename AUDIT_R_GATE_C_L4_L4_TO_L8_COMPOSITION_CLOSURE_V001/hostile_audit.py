#!/usr/bin/env python3
"""Hash-pinned hostile verifier for the frozen L4->L8 composition closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_RESULT.json"

EXPECTED = {
    "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/PROTOCOL.md": "e0245dc81edb15be8b5ece72ff196f19754976a41a5785941e3dba2428bdcbb4",
    "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/README.md": "e114fc5526ab55812e700d250e2c2319055116e3cbe971f51371a8909b720e0d",
    "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/THEOREM.md": "f5e0ac7077fb7460d0345513c1f62e791633f2f21cad93e4756a5a8f27f6b4d2",
    "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/RESULT.md": "60d2d3913ebfcab7c16f239bf783db30bd893c3fac330d64ea469b520bb0839a",
    "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/RESULT.json": "b30e73a943bbbb525039478273ec803652a9667b695a3b2ab38067f0350956d5",
    "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/compute_closure.py": "98e8576f9683875fccb3a3ae9db9fac50b67868f8510d3956a32e210f9868e6d",
    "ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001/MANIFEST.sha256": "c0a2a501259f5d71275c9d65d2bd4a9b392454975eba1e727c20647988bdc896",
    "ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001/README.md": "e6c2a69b7df2bd4c1ac401a6452581f7ebe874fbfb02fde10a3ee3670970078d",
    "ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001/REPORT.md": "34e0cc94203f8fc70b8abe22296eba68160a8c35393b3d97d209cda6311fe8f5",
    "ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001/RESULT.json": "fd0347a57dc10aaaa03c91f661b5715db1db57e86e48ed161144110c9e4fe924",
    "ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001/adversarial_equal_time_record.py": "aa47d35a22e6d43a2fed2d23ffca6d829ddddbafd64f9059a621f9d81fec4638",
    "AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/FROZEN_INDEPENDENT.json": "07b0f4674d40e6a04c4ac44361c04fef39c3970944a47212ad74dbadc64846ca",
    "AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/FROZEN_REFINEMENT.json": "9111c9f24c02bee1185ce0d960b3a71e7fbfad2fb2a1c446d06471169e9de5b9",
    "AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/FROZEN_CONSERVATION.json": "f8a251697de73179006fecc241dba5372f59d8e459af18addff88c324c8bb550",
    "AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/freeze_independent.py": "6b1fdb608801eb14ecbd14b5706d602dfb11cd6e91866c91a76a29cc05019ed0",
    "AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/refine_independent.py": "0660a9662cd33b35588cadb45309aac059f9af1568f1fdad696d146cd857338b",
    "AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/freeze_conservation.py": "618a73ecc1c2d315a2f54ad045c925b97c2a656a9e41e517f6b1774bb4475861",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str, passed: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    passed.append(label)


def canonical_edges(length: int) -> set[tuple[int, int, str]]:
    edges = set()
    for rail in (0, 1):
        offset = rail * length
        for node in range(length):
            edges.add((offset + node, offset + (node + 1) % length, f"rail_{rail + 1}"))
    for node in range(length):
        edges.add((node, length + (node + 1) % length, "connector"))
    return edges


def block_edges(rail_one: list[int], rail_two: list[int]) -> set[tuple[int, int, str]]:
    edges = set()
    for name, sites in (("rail_1", rail_one), ("rail_2", rail_two)):
        for index in range(4):
            edges.add((sites[index], sites[(index + 1) % 4], name))
    for index in range(4):
        edges.add((rail_one[index], rail_two[(index + 1) % 4], "connector"))
    return edges


def maxdiff(a, b) -> float:
    return max(abs(float(x) - float(y)) for x, y in zip(a, b))


def main() -> None:
    passed: list[str] = []
    actual_hashes = {name: sha256(ROOT / name) for name in EXPECTED}
    require(actual_hashes == EXPECTED, "all_target_adversarial_and_frozen_hashes_match", passed)

    frozen = json.loads((HERE / "FROZEN_INDEPENDENT.json").read_text())
    refine = json.loads((HERE / "FROZEN_REFINEMENT.json").read_text())
    conservation = json.loads((HERE / "FROZEN_CONSERVATION.json").read_text())
    target = json.loads((ROOT / "DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/RESULT.json").read_text())
    adversarial = json.loads((ROOT / "ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001/RESULT.json").read_text())

    protocol_hash = EXPECTED["DEVELOPMENT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001/PROTOCOL.md"]
    require(all(x["protocol_sha256"] == protocol_hash for x in (frozen, refine, conservation, target, adversarial)),
            "all_records_pin_frozen_protocol", passed)

    isolated = block_edges([0, 1, 2, 3], [8, 9, 10, 11]) | block_edges([4, 5, 6, 7], [12, 13, 14, 15])
    removed = {tuple(x) for x in frozen["topology"]["removed_owner_edges"]}
    added = {tuple(x) for x in frozen["topology"]["added_owner_edges"]}
    joined = (isolated - removed) | added
    require(len(isolated) == 24 and len(removed) == 6 and len(added) == 6 and len(joined) == 24,
            "six_remove_six_add_owner_count_exact", passed)
    require(removed <= isolated and not (added & isolated) and joined == canonical_edges(8),
            "owner_surgery_set_equals_canonical_L8", passed)
    removed_pairs = {tuple(sorted((x[0], x[1]))) for x in removed}
    added_pairs = {tuple(sorted((x[0], x[1]))) for x in added}
    require(target["owner_surgery_exact"] is True
            and {tuple(x) for x in target["removed_owners"]} == removed_pairs
            and {tuple(x) for x in target["added_owners"]} == added_pairs,
            "target_owner_surgery_matches_independent_reconstruction", passed)
    require(frozen["source_factorization"]["matrix_linf_error"] == 0.0,
            "uniform_source_factorization_exact", passed)

    obs4 = frozen["observations"]["4"]["lanczos_interface"]
    obs8 = frozen["observations"]["8"]["lanczos_interface"]
    require(obs4["ranks_by_absolute_threshold"] == {"threshold_1e-08": 16, "threshold_1e-10": 16,
            "threshold_1e-12": 16, "threshold_1e-14": 16} and obs4["smallest_singular_value"] > 4e-6,
            "D4_equals_16_and_is_well_separated", passed)
    require(obs8["ranks_by_absolute_threshold"]["threshold_1e-08"] == 251
            and refine["ranks_by_absolute_threshold"]["threshold_1e-08"] == 251,
            "common_solver_stable_D8_lower_bound_is_251", passed)
    require(target["exact_D8_interval_pending_hostile_resolution"] == [251, 256]
            and target["hostile_common_robust_D8_lower_bound"] == 251,
            "target_preserves_unresolved_D8_interval_251_256", passed)
    require(obs8["full_rank_reconstruction_error"] < 1e-12
            and target["exact_reconstruction_dimension_D8"] == 256,
            "D256_is_sufficient_for_exact_numerical_reconstruction", passed)
    require(target["certified_ratio_lower_bound"] == 251 / 16
            and target["fractional_lower_bound_L8"] == 251 / 256,
            "exponential_obstruction_lower_bounds_exact", passed)

    target_rows = {str(row["L"]): row for row in target["rows"]}
    comparison = {}
    for length in ("4", "8"):
        row = target_rows[length]
        fine = conservation["rows"][length]["fine"]
        q_delta = maxdiff(fine["q_final"], row["q_after"])
        current_delta = maxdiff(fine["integrated_owner_currents"], row["currents"])
        corr_delta = abs(fine["max_abs_connected_edge_correlation"] - row["max_abs_connected_edge_correlation"])
        require(q_delta < 1e-9 and current_delta < 1e-9 and corr_delta < 1e-9,
                f"L{length}_independent_conservation_observables_agree", passed)
        require(fine["ledger_l1"] < 1e-8 and row["ledger_l1"] < 1e-8,
                f"L{length}_owner_once_ledger_closes", passed)
        tails = frozen["observations"][length]["lanczos_interface"]["optimal_frobenius_tail_error_by_retained_D"]
        tail_delta = max(abs(tails[int(d)] - value) for d, value in row["tail_l2_checkpoints"].items())
        require(tail_delta < 1e-12, f"L{length}_optimal_tail_checkpoints_agree", passed)
        comparison[length] = {
            "q_linf": q_delta,
            "integrated_current_linf": current_delta,
            "correlation_max_abs_difference": corr_delta,
            "tail_checkpoint_linf": tail_delta,
            "independent_fine_ledger_l1": fine["ledger_l1"],
            "target_ledger_l1": row["ledger_l1"],
        }

    attack = frozen["lower_order_boundary_record_attack"]
    require(attack["verdict"] == "LOWER_ORDER_EQUAL_TIME_RECORD_DOES_NOT_CLOSE_FUTURE_JOINED_OUTPUT"
            and attack["future_port_record_linf_difference"] > 0.17,
            "independent_lower_order_boundary_collision", passed)
    require(adversarial["status"] == "PASS_EQUAL_TIME_RECORD_NOT_CLOSED"
            and adversarial["checks_passed"] == adversarial["checks_total"] == 19,
            "target_adversarial_boundary_packet_passes_19_of_19", passed)
    require(target["stop_rule"] == "STOP_EXPONENTIAL_LOWER_BOUND__EXACT_D8_UNRESOLVED",
            "mandatory_stop_rule_is_exact_rank_honest", passed)
    forbidden = {"grid", "continuum", "Ward", "graviton", "gravity"}
    target_not_claimed = set(target["not_claimed"].split("__"))
    require({"GRID", "CONTINUUM", "WARD", "GRAVITON", "GRAVITY"} <= target_not_claimed,
            "forbidden_emergence_claims_explicitly_not_made", passed)

    result = {
        "schema": "AUDIT_R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001",
        "status": "PASS_HOSTILE_AUDIT_OBSTRUCTION_STOP__EXACT_D8_UNRESOLVED",
        "checks_passed": len(passed),
        "checks_total": len(passed),
        "checks": passed,
        "protocol_sha256": protocol_hash,
        "scope": "L4_AND_L8_ONLY__NO_L6_OR_L12",
        "classification": {
            "D4": 16,
            "D4_status": "WELL_SEPARATED",
            "exact_D8": "UNRESOLVED",
            "exact_D8_interval": [251, 256],
            "common_solver_stable_D8_lower_bound": 251,
            "D8_full_exact_numerical_reconstruction_dimension": 256,
            "D8_over_D4_certified_lower_bound": 251 / 16,
            "D8_fraction_certified_lower_bound": 251 / 256,
            "target_threshold_estimate": 254,
            "independent_threshold_estimates": {"1e-8": 251, "1e-10": 253, "1e-12": 255, "1e-14": 256},
            "rank_disposition": "LAST_MODES_BELOW_SOLVER_DISCREPANCY_CERTIFICATION__DO_NOT_PROMOTE_AN_EXACT_D8",
            "stop_rule": "STOP_EXPONENTIAL_LOWER_BOUND__EXACT_D8_UNRESOLVED",
        },
        "independent_methods": ["MATRIX_FREE_HERMITIAN_LANCZOS", "UNITARY_FOURTH_ORDER_SUZUKI_YOSHIDA"],
        "target_comparison": comparison,
        "lower_order_collision": {
            "independent_internal_roots": attack["internal_root_sites"],
            "independent_future_record_linf": attack["future_port_record_linf_difference"],
            "target_packet_status": adversarial["status"],
            "claim_boundary": attack["root_boundary"],
        },
        "hashes": actual_hashes,
        "claims": {
            "proved": ["exact owner surgery", "exact source factorization", "Schmidt minimality identity", "exact candidate-map rank/nullity and equality of the collision input record"],
            "empirical": ["well-separated numerical D4=16", "cross-solver-stable numerical D8>=251", "D=256 reconstruction within recorded floating-point error", "future-read collision separation", "L4/L8 spectra and observable agreement within recorded numerical controls"],
            "conditional": ["finite-L record result under the frozen protocol and adopted microscopic model"],
            "open": ["exact D8 in [251,256]", "larger-L behavior", "continuum/macroscopic response"],
            "not_claimed": sorted(forbidden | {"emergence", "phase"}),
        },
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if OUT.exists() and OUT.read_text() != encoded:
        raise AssertionError("existing INDEPENDENT_RESULT.json differs")
    OUT.write_text(encoded)
    print(result["status"])


if __name__ == "__main__":
    main()
