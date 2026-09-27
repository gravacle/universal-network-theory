#!/usr/bin/env python3
"""Deterministic tests for the independent owner-once closure audit."""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

import numpy as np

import hostile_carrier_closure as hostile


HERE = Path(__file__).resolve().parent


class HostileCarrierClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = hostile.build_result()
        cls.by_length = {item["length"]: item for item in cls.payload["results"]}

    def test_frozen_mandatory_controls_pass(self) -> None:
        self.assertEqual(tuple(hostile.MANDATORY_LENGTHS), (4, 6))
        self.assertEqual(set(self.by_length), {4, 6})
        self.assertTrue(
            self.payload["disposition"].startswith(
                "PASS_EXACT_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE"
            )
        )
        for length, result in self.by_length.items():
            self.assertTrue(result["passed"], msg=f"L={length}")
            self.assertLessEqual(
                result["maximum_full_reduced_disagreement"],
                hostile.EQUIVALENCE_TOLERANCE,
            )
            self.assertLessEqual(
                result["maximum_absolute_norm_control_error"],
                hostile.CONTROL_TOLERANCE,
            )
            self.assertLessEqual(
                result["maximum_fresh_lineage_probability"],
                hostile.EQUIVALENCE_TOLERANCE,
            )
            self.assertEqual(len(result["events"]), length)
            self.assertEqual(len(result["checkpoints"]), 1 + 2 * length)

    def test_explicit_l4_trace_distance_is_present(self) -> None:
        for checkpoint in self.by_length[4]["checkpoints"]:
            value = checkpoint["reduced_carrier_trace_distance"]
            self.assertIsNotNone(value)
            self.assertTrue(math.isfinite(value))
            self.assertLessEqual(value, hostile.EQUIVALENCE_TOLERANCE)
        for checkpoint in self.by_length[6]["checkpoints"]:
            self.assertIsNone(checkpoint["reduced_carrier_trace_distance"])
            self.assertTrue(
                math.isfinite(checkpoint["reduced_carrier_trace_distance_upper_bound"])
            )

    def test_kraus_channel_preserves_trace(self) -> None:
        parent = hostile.build_parent(4)
        carrier = hostile.initial_carrier(parent)
        before = hostile.factor_norm(carrier)
        for event in range(4):
            carrier = hostile.carrier_channel(parent, carrier, event)
            self.assertAlmostEqual(hostile.factor_norm(carrier), before, places=14)

    def test_closed_ladder_negative_control_is_detected(self) -> None:
        parent = hostile.build_parent(4)
        joint = hostile.joint_admission(parent, hostile.initial_joint(parent), 0)
        closed_only = hostile.initial_carrier(parent)
        disagreement = hostile.compare_states(
            parent, joint, closed_only, include_trace_distance=True
        )
        self.assertGreater(disagreement["reduced_carrier_trace_distance"], 0.1)
        self.assertGreater(disagreement["sector_weight_max_abs"], 0.1)

    def test_output_is_finite_relative_and_canonically_serializable(self) -> None:
        self.assertTrue(hostile.finite_values(self.payload))
        encoded_a = json.dumps(
            self.payload, indent=2, sort_keys=True, allow_nan=False
        ) + "\n"
        encoded_b = json.dumps(
            self.payload, indent=2, sort_keys=True, allow_nan=False
        ) + "\n"
        self.assertEqual(encoded_a, encoded_b)
        self.assertNotIn(str(hostile.ROOT), encoded_a)
        self.assertNotIn("hostname", encoded_a.lower())
        self.assertNotIn("timestamp", encoded_a.lower())

    def test_hostile_source_does_not_name_or_import_target_verifier(self) -> None:
        source = (HERE / "hostile_carrier_closure.py").read_text()
        self.assertNotIn("DEVELOPMENT_R_LINEAGE_CARRIER_REDUCTION_V001", source)
        self.assertNotIn("import compute_seed_history", source)
        self.assertNotIn("import compute_streamed_history", source)
        self.assertFalse(self.payload["independence"]["target_verifier_imports"])
        self.assertFalse(self.payload["independence"]["target_matrix_imports"])
        self.assertFalse(self.payload["independence"]["target_result_values_read"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
