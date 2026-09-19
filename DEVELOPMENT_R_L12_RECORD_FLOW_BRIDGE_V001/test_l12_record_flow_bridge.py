#!/usr/bin/env python3
"""Gateway tests for the L12 record-flow bridge sidecar."""

from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np

import l12_record_flow_bridge as subject


def document(label: str, payload: dict[str, object]) -> subject.AuthenticatedJSON:
    return subject.AuthenticatedJSON(label, Path(f"/{label}.json"), "0" * 64, payload)


class RecordFlowBridgeTests(unittest.TestCase):
    def test_exact_terminal_bit_insertion_authenticates(self) -> None:
        source_words = np.array([0, 1, 2, 3], dtype=np.uint32)
        destination_words = np.array([8, 9, 10, 11], dtype=np.uint32)
        source = np.array([0, 1, 2, 3], dtype=np.int32)
        destination = np.array([0, 1, 2, 3], dtype=np.int32)
        checks = subject.validate_admission_map(
            source_words, destination_words, source, destination, event=3
        )
        self.assertTrue(checks["exact_terminal_bit_insertion"])
        self.assertEqual(checks["pair_count"], 4)

    def test_noninjective_admission_map_fails_closed(self) -> None:
        with self.assertRaisesRegex(subject.Refusal, "not injective"):
            subject.validate_admission_map(
                np.array([0, 1], dtype=np.uint32),
                np.array([8, 9], dtype=np.uint32),
                np.array([0, 0], dtype=np.int32),
                np.array([0, 1], dtype=np.int32),
                event=3,
            )

    def test_wrong_destination_word_fails_closed(self) -> None:
        with self.assertRaisesRegex(subject.Refusal, "does not exactly insert"):
            subject.validate_admission_map(
                np.array([0, 1], dtype=np.uint32),
                np.array([8, 10], dtype=np.uint32),
                np.array([0, 1], dtype=np.int32),
                np.array([0, 1], dtype=np.int32),
                event=3,
            )

    def test_selected_norm_is_read_only_and_exact(self) -> None:
        shard = np.array([[1 + 2j, 3 + 4j], [5 + 6j, 7 + 8j]], dtype=np.complex128)
        snapshot = shard.copy()
        observed = subject.selected_norm_squared(shard, np.array([1], dtype=np.int32), row_chunk=1)
        self.assertEqual(observed, 25.0 + 113.0)
        np.testing.assert_array_equal(shard, snapshot)

    def test_cross_branch_positive_agreement_passes(self) -> None:
        target = {
            "edge": "L12:Q04->L12:Q05",
            "source_q": 4,
            "destination_q": 5,
            "transferred_norm_squared": 0.088,
        }
        hostile = dict(target)
        hostile["transferred_norm_squared"] = 0.088 + 2e-16
        audit = subject.adjudicate_cross_branch(target, hostile)
        self.assertTrue(audit["certified"])

    def test_cross_branch_mismatch_fails_closed(self) -> None:
        target = {
            "edge": "L12:Q04->L12:Q05",
            "source_q": 4,
            "destination_q": 5,
            "transferred_norm_squared": 0.088,
        }
        hostile = dict(target)
        hostile["transferred_norm_squared"] = 0.089
        with self.assertRaisesRegex(subject.Refusal, "flow mismatch"):
            subject.adjudicate_cross_branch(target, hostile)

    def test_zero_flow_fails_closed(self) -> None:
        target = {
            "edge": "L12:Q04->L12:Q05",
            "source_q": 4,
            "destination_q": 5,
            "transferred_norm_squared": 0.0,
        }
        with self.assertRaisesRegex(subject.Refusal, "flow mismatch"):
            subject.adjudicate_cross_branch(target, dict(target))

    def test_endpoint_binding_requires_target_and_blind_consensus(self) -> None:
        atoms = [
            {"atom_id": "A4", "q_by_L": {"12": 4}},
            {"atom_id": "A5", "q_by_L": {"12": 5}},
            {"atom_id": "A6", "q_by_L": {"12": 6}},
        ]

        def classification(z: float, y: float) -> dict[str, object]:
            return {"gap_power_fit": {"exponent": z}, "chi_power_exponent_y": y}

        results = [
            {
                "atom": atom,
                "target_classification": classification(1.0, 1.0) if atom["atom_id"] != "A5" else classification(0.5, 0.5),
                "blind_classification": classification(1.0, 1.0) if atom["atom_id"] != "A5" else classification(0.5, 0.5),
            }
            for atom in atoms
        ]
        qmap, endpoints = subject.extract_atoms_and_endpoints(
            document("manifest", {"atoms": atoms}),
            document("adjudication", {"atom_results": results}),
        )
        self.assertEqual(qmap, {"A4": 4, "A5": 5, "A6": 6})
        self.assertEqual(endpoints["q4_passing_atoms"], ["A4"])
        self.assertEqual(endpoints["q6_passing_atoms"], ["A6"])

    def test_mass_is_deduplicated_by_sector(self) -> None:
        pbar = [0.0] * 13
        pbar[4], pbar[5], pbar[6] = 0.24, 0.20, 0.13
        pbar[0] = 0.43
        report = subject.sector_mass_report(
            document("manifest", {"histories": {"12": {"pbar_q": pbar}}})
        )
        self.assertEqual(report["deduplicated_q4_q5_q6"], "0.57")
        self.assertTrue(report["threshold_crossed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
