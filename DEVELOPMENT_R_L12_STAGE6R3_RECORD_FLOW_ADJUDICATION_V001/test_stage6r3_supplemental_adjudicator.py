#!/usr/bin/env python3
"""Fail-closed gateways for the Stage-6R3 supplemental adjudicator."""

from __future__ import annotations

import unittest
from decimal import Decimal

import stage6r3_supplemental_adjudicator as subject


def classification(z: float, y: float, passes: bool = False) -> dict[str, object]:
    return {
        "gap_power_fit": {"exponent": z},
        "chi_power_exponent_y": y,
        "passes": passes,
        "checks": {"z_in_window": 0.9 <= z <= 1.1, "example_full_gate": passes},
    }


def synthetic_stage6() -> dict[str, object]:
    rows = []
    for index in range(24):
        atom_id = f"A{index:03d}"
        q = 4 if index <= 11 else 5 if index <= 15 else 6 if index == 16 else 7
        geometry = classification(1.0, 1.0) if index in (11, 16) else classification(0.5, 0.5)
        rows.append(
            {
                "atom": {"atom_id": atom_id, "q_by_L": {"12": q}},
                "passes": False,
                "failures": ["preregistered z=1 conjunction rejected"],
                "target_classification": geometry,
                "blind_classification": geometry,
            }
        )
    return {
        "classification": "AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12",
        "atom_results": rows,
    }


def synthetic_flow() -> dict[str, object]:
    return {
        "status": "PASS",
        "classification": "AUTHENTICATED_L12_RECORD_FLOW_SECTOR_BRIDGE",
        "typed_topology": {
            "exact_bridge_path": ["A011", "L12:Q04", "L12:Q05", "L12:Q06", "A016"],
            "contiguous_under_record_flow": True,
            "certified_sector_flow_edges": [
                {
                    "edge": "L12:Q04->L12:Q05",
                    "certified": True,
                    "target_positive": True,
                    "hostile_positive": True,
                    "cross_branch_agreement": True,
                    "target_transferred_norm_squared": 0.088,
                    "hostile_transferred_norm_squared": 0.088,
                },
                {
                    "edge": "L12:Q05->L12:Q06",
                    "certified": True,
                    "target_positive": True,
                    "hostile_positive": True,
                    "cross_branch_agreement": True,
                    "target_transferred_norm_squared": 0.105,
                    "hostile_transferred_norm_squared": 0.105,
                },
            ],
        },
        "mass": {
            "q4": "0.24",
            "q5": "0.20",
            "q6": "0.13",
            "deduplicated_q4_q5_q6": "0.57",
        },
        "conclusion": {"stage6_frozen_result_modified": False},
    }


class Stage6R3Tests(unittest.TestCase):
    def test_reconstructs_late_event_average_not_terminal_row(self) -> None:
        rows = []
        for event in range(1, 13):
            weights = [0.0] * 13
            weights[4 if event < 12 else 5] = 1.0
            rows.append({"event": event, "sector_weights": weights})
        history = {"L": 12, "comparison": {"resolved": True}, "rows": rows}
        pbar = subject.reconstruct_late_pbar(history)
        self.assertEqual(pbar["events"], [6, 7, 8, 9, 10, 11, 12])
        self.assertEqual(Decimal(pbar["pbar_q"][4]), Decimal(6) / Decimal(7))
        self.assertEqual(Decimal(pbar["pbar_q"][5]), Decimal(1) / Decimal(7))

    def test_endpoint_window_does_not_become_full_stage6_pass(self) -> None:
        audit = subject.atom_audit(synthetic_stage6())
        self.assertTrue(all(row["target_blind_geometry_window_pass"] for row in audit["endpoints"]))
        self.assertFalse(audit["both_endpoints_pass_original_full_gate"])
        self.assertEqual(audit["q5_geometry_window_pass_count"], 0)
        self.assertEqual(audit["q5_original_stage6_pass_count"], 0)

    def test_flow_sidecar_requires_exact_typed_path(self) -> None:
        flow = synthetic_flow()
        flow["typed_topology"]["exact_bridge_path"][2] = "L12:Q99"
        with self.assertRaisesRegex(subject.Refusal, "typed path changed"):
            subject.flow_audit(flow)

    def test_flow_sidecar_requires_both_independent_branches(self) -> None:
        flow = synthetic_flow()
        flow["typed_topology"]["certified_sector_flow_edges"][0]["hostile_positive"] = False
        with self.assertRaisesRegex(subject.Refusal, "independently positive"):
            subject.flow_audit(flow)

    def test_whole_sector_arithmetic_pass_remains_inadmissible(self) -> None:
        atoms = subject.atom_audit(synthetic_stage6())
        flow = subject.flow_audit(synthetic_flow())
        pbar = {"pbar_q": ["0"] * 4 + ["0.24", "0.20", "0.13"] + ["0"] * 6}
        rules = subject.evaluate_rules(atoms, flow, pbar)
        whole = rules["whole_sector_connectivity_rule"]
        self.assertEqual(whole["deduplicated_mass"], "0.57")
        self.assertTrue(whole["arithmetic_threshold_crossed"])
        self.assertFalse(whole["admissible_as_stage6_candidate"])

    def test_conservative_rule_fails_closed_on_measure_and_lineage(self) -> None:
        atoms = subject.atom_audit(synthetic_stage6())
        flow = subject.flow_audit(synthetic_flow())
        pbar = {"pbar_q": ["0"] * 4 + ["0.24", "0.20", "0.13"] + ["0"] * 6}
        conservative = subject.evaluate_rules(atoms, flow, pbar)["conservative_flow_support_rule"]
        self.assertFalse(conservative["same_measure_or_conversion_theorem_authenticated"])
        self.assertFalse(conservative["common_lineage_intersection_authenticated"])
        self.assertIsNone(conservative["certified_total_mass"])
        self.assertEqual(conservative["threshold_disposition"], "UNRESOLVED_FAIL_CLOSED")

    def test_mass_disagreement_fails_closed(self) -> None:
        atoms = subject.atom_audit(synthetic_stage6())
        flow = subject.flow_audit(synthetic_flow())
        pbar = {"pbar_q": ["0"] * 4 + ["0.25", "0.20", "0.13"] + ["0"] * 6}
        with self.assertRaisesRegex(subject.Refusal, "q4 mass does not match"):
            subject.evaluate_rules(atoms, flow, pbar)


if __name__ == "__main__":
    unittest.main(verbosity=2)
