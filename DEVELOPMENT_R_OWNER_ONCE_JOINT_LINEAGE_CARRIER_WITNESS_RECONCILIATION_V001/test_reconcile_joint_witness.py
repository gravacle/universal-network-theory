#!/usr/bin/env python3
"""Tests for the sealed joint-witness reconciler."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import reconcile_joint_witness as reconciliation  # noqa: E402


class ReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = reconciliation.reconcile(ROOT)

    def test_real_packet_resolves_exact_protocol_classification(self) -> None:
        self.assertTrue(self.result["passed"])
        self.assertTrue(self.result["all_numerical_and_control_conditions_passed"])
        self.assertEqual(self.result["protocol_classification"], reconciliation.RESOLVED)
        self.assertGreater(self.result["T_4_8"], 1.0)

    def test_required_lengths_and_values(self) -> None:
        rows = self.result["per_size"]
        self.assertEqual([row["length"] for row in rows], [4, 6, 8])
        expected = {
            4: 0.025544765930507966,
            6: 0.0018321913827511092,
            8: 0.001963064475535806,
        }
        for row in rows:
            self.assertEqual(row["D_L"], expected[row["length"]])
            self.assertEqual(row["tau_L"], 1.0e-9)
            self.assertTrue(row["passed"])

    def test_all_target_hostile_comparisons_are_within_frozen_tolerance(self) -> None:
        for row in self.result["per_size"]:
            differences = [
                field["absolute_disagreement"]
                for field in row["target_hostile_comparisons"].values()
            ]
            self.assertLessEqual(max(differences), reconciliation.TOLERANCES["target_independent"])
            self.assertEqual(max(differences), row["d_components"]["target_vs_independent"])

    def test_input_authentication_covers_protocol_results_and_seals(self) -> None:
        authenticated = self.result["authenticated_inputs"]
        self.assertEqual(set(authenticated), set(reconciliation.PINNED_HASHES))
        for relative, expected in reconciliation.PINNED_HASHES.items():
            self.assertEqual(authenticated[relative]["sha256"], expected)

    def test_json_serialization_is_byte_deterministic(self) -> None:
        first = reconciliation.deterministic_json(reconciliation.reconcile(ROOT))
        second = reconciliation.deterministic_json(reconciliation.reconcile(ROOT))
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))
        self.assertEqual(
            hashlib.sha256(first.encode("utf-8")).hexdigest(),
            hashlib.sha256(second.encode("utf-8")).hexdigest(),
        )

    def test_classification_boundaries_are_frozen(self) -> None:
        self.assertEqual(reconciliation.protocol_classification(True, 1.0000001), reconciliation.RESOLVED)
        self.assertEqual(reconciliation.protocol_classification(True, 1.0), reconciliation.FALSIFIED)
        self.assertEqual(reconciliation.protocol_classification(True, 0.0), reconciliation.FALSIFIED)
        self.assertEqual(reconciliation.protocol_classification(False, 1.0e20), reconciliation.UNRESOLVED)
        self.assertEqual(reconciliation.protocol_classification(True, math.nan), reconciliation.UNRESOLVED)

    def test_condition_tamper_fails_closed(self) -> None:
        target = reconciliation.strict_json(ROOT / reconciliation.TARGET_RESULT)
        row = copy.deepcopy(target["rows"][0])
        row["conditions"]["shuffle_control"] = False
        with self.assertRaises(reconciliation.ReconciliationError):
            reconciliation.validate_target_row(row)

    def test_nonfinite_json_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"x": NaN}\n', encoding="utf-8")
            with self.assertRaises(reconciliation.ReconciliationError):
                reconciliation.strict_json(path)
            path.write_text('{"x": 1e999}\n', encoding="utf-8")
            with self.assertRaises(reconciliation.ReconciliationError):
                reconciliation.strict_json(path)

    def test_manifest_hash_tamper_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            artifact = folder / "artifact.txt"
            artifact.write_text("sealed\n", encoding="utf-8")
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            manifest = folder / "MANIFEST.sha256"
            manifest.write_text(f"{digest}  artifact.txt\n", encoding="utf-8")
            self.assertEqual(
                reconciliation.verify_manifest(manifest, {"artifact.txt"}),
                {"artifact.txt": digest},
            )
            artifact.write_text("tampered\n", encoding="utf-8")
            with self.assertRaises(reconciliation.ReconciliationError):
                reconciliation.verify_manifest(manifest, {"artifact.txt"})

    def test_absolute_and_parent_paths_are_rejected(self) -> None:
        for value in ("/tmp/result.json", "../result.json", "a/../result.json"):
            with self.subTest(value=value):
                with self.assertRaises(reconciliation.ReconciliationError):
                    reconciliation.relative_path(value, "test")

    def test_runtime_metadata_is_rejected(self) -> None:
        for key in ("host", "timestamp", "generated_at", "measurement_timestamp"):
            with self.subTest(key=key):
                with self.assertRaises(reconciliation.ReconciliationError):
                    reconciliation.verify_no_runtime_metadata({key: "forbidden"}, "record")

    def test_held_out_sizes_are_not_adjudicated(self) -> None:
        held_out = self.result["held_out_L10_L12"]
        self.assertFalse(held_out["computed_or_opened_by_reconciliation"])
        self.assertFalse(held_out["resource_gate_evaluated_by_reconciliation"])
        self.assertEqual(held_out["disposition"], "NOT_ADJUDICATED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
