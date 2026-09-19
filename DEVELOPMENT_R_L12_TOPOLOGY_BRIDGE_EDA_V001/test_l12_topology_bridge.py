#!/usr/bin/env python3
"""Gateway tests for strict L12 topology authentication and traversal."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path

import l12_topology_bridge as subject


def document(payload: object, label: str = "synthetic") -> subject.InputDocument:
    return subject.InputDocument(
        label=label,
        path=Path(f"/{label}.json"),
        sha256="0" * 64,
        payload=payload,
    )


def atoms_payload(edges: object | None = None) -> dict[str, object]:
    payload: dict[str, object] = {
        "atoms": [
            {"atom_id": "A4", "q": 4, "z": 1.0, "y": 1.0},
            {"atom_id": "A5a", "q": 5, "z": 0.2, "y": 0.2},
            {"atom_id": "A5b", "q": 5, "z": 0.3, "y": 0.3},
            {"atom_id": "A6", "q": 6, "z": 1.0, "y": 1.0},
        ],
        "sector_masses": {"4": 0.22, "5": 0.20, "6": 0.14},
    }
    if edges is not None:
        payload["edges"] = edges
    return payload


def report_for(payload: object) -> dict[str, object]:
    return subject.build_report(
        [document(payload)],
        Decimal("0.90"),
        Decimal("1.10"),
        Decimal("0.50"),
        "consensus",
    )


class StrictTopologyTests(unittest.TestCase):
    def test_absent_topology_fails_before_endpoints_and_mass(self) -> None:
        report = report_for(atoms_payload())
        self.assertEqual(report["classification"], "AUTHENTICATION_FAILURE")
        self.assertIsNone(report["endpoints"])
        self.assertIsNone(report["mass"])
        output = io.StringIO()
        with redirect_stdout(output):
            subject.print_report(report)
        self.assertIn(
            "AUTHENTICATION_FAILURE: No explicit atom-level topology found in schema.",
            output.getvalue(),
        )
        self.assertNotIn("Deduplicated triad mass", output.getvalue())

    def test_global_edges_authenticate_exact_q5_chain(self) -> None:
        report = report_for(
            atoms_payload([["A4", "A5a"], ["A5a", "A5b"], ["A5b", "A6"]])
        )
        self.assertEqual(report["classification"], "TOPOLOGICALLY_CONTIGUOUS_Q4_Q5_Q6")
        self.assertEqual(report["bridge"]["path"], ["A4", "A5a", "A5b", "A6"])
        self.assertEqual(report["bridge"]["path_sectors"], [4, 5, 5, 6])
        self.assertEqual(report["mass"]["deduplicated_q4_q5_q6"], "0.56")
        self.assertTrue(report["mass"]["threshold_crossed"])
        sources = report["schema_discovery"]["authenticated_edge_fields"]
        self.assertEqual(sources[0]["json_path"], "$.edges")
        self.assertEqual(sources[0]["key"], "edges")

    def test_labeled_edge_layout_authenticates_known_atom_ids(self) -> None:
        payload = atoms_payload()
        payload["edge_layout"] = [
            ["A4", "A5a", "admission"],
            ["A5a", "A5b", "transport"],
            ["A5b", "A6", "admission"],
        ]
        report = report_for(payload)
        self.assertEqual(report["bridge"]["path"], ["A4", "A5a", "A5b", "A6"])

    def test_physical_vertex_edges_do_not_become_atom_edges(self) -> None:
        payload = atoms_payload()
        payload["edge_layout"] = [[0, 1, "rail_1"], [0, 3, "connector"]]
        report = report_for(payload)
        self.assertEqual(report["classification"], "AUTHENTICATION_FAILURE")
        self.assertEqual(report["schema_discovery"]["accepted_explicit_edge_count"], 0)

    def test_per_atom_neighbors_authenticate_direct_shared_q5_node(self) -> None:
        payload = atoms_payload()
        atoms = payload["atoms"]
        atoms[0]["neighbors"] = ["A5a"]
        atoms[1]["neighbors"] = ["A6"]
        report = report_for(payload)
        self.assertEqual(report["bridge"]["path"], ["A4", "A5a", "A6"])
        self.assertEqual(report["endpoints"]["shared_direct_q5_nodes"], ["A5a"])

    def test_global_adjacency_mapping_authenticates(self) -> None:
        payload = atoms_payload()
        payload["adjacency"] = {
            "A4": ["A5a"],
            "A5a": {"A5b": {"weight": 1}},
            "A5b": ["A6"],
        }
        report = report_for(payload)
        self.assertEqual(report["bridge"]["path"], ["A4", "A5a", "A5b", "A6"])
        sources = report["schema_discovery"]["authenticated_edge_fields"]
        self.assertEqual(sources[0]["kind"], "global_adjacency_mapping")

    def test_explicit_edges_without_bridge_do_not_authorize_mass_sum(self) -> None:
        report = report_for(atoms_payload([["A4", "A5a"], ["A5b", "A6"]]))
        self.assertEqual(report["classification"], "NO_AUTHENTICATED_Q4_Q5_Q6_BRIDGE")
        self.assertFalse(report["bridge"]["contiguous"])
        self.assertIsNone(report["mass"])

    def test_unknown_edge_endpoints_do_not_authenticate(self) -> None:
        report = report_for(atoms_payload([["A4", "UNKNOWN"]]))
        self.assertEqual(report["classification"], "AUTHENTICATION_FAILURE")
        self.assertEqual(report["schema_discovery"]["accepted_explicit_edge_count"], 0)
        self.assertGreater(report["schema_discovery"]["rejected_relation_items"], 0)

    def test_direct_q4_q6_edge_is_not_a_q5_bridge(self) -> None:
        report = report_for(atoms_payload([["A4", "A6"]]))
        self.assertEqual(report["classification"], "NO_AUTHENTICATED_Q4_Q5_Q6_BRIDGE")
        self.assertIsNone(report["mass"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
