#!/usr/bin/env python3
"""Tests for the finite lineage carrier-reduction verifier."""

from __future__ import annotations

import unittest
from unittest import mock

import numpy as np

import verify_carrier_reduction as verifier


class CarrierReductionTests(unittest.TestCase):
    def test_kraus_channel_preserves_norm_for_fresh_event(self) -> None:
        channel = verifier.CarrierChannel(4)
        blocks = channel.initial()
        for event in range(4):
            self.assertLessEqual(verifier.freshness_probability(blocks, channel, event), 1.0e-15)
            before_norm = channel.norm(blocks)
            blocks = channel.apply_channel(blocks, event)
            self.assertAlmostEqual(channel.norm(blocks), before_norm, places=14)
            blocks, _ = channel.transport(blocks, 16)
            self.assertLess(abs(channel.norm(blocks) - 1.0), 1.0e-10)

    def test_l4_joint_and_carrier_channel_agree(self) -> None:
        row = verifier.verify_length(4, steps=16, explicit_trace=True)
        self.assertTrue(row["passed"])
        self.assertLessEqual(
            row["maximum_equivalence_disagreement"], verifier.ABS_TOLERANCE
        )
        self.assertLessEqual(row["maximum_numerical_control_error"], verifier.ABS_TOLERANCE)
        for event in row["events"]:
            self.assertIsNotNone(event["after_transport"]["reduced_carrier_trace_distance"])

    def test_density_residual_detects_perturbation(self) -> None:
        channel = verifier.CarrierChannel(4)
        left = channel.initial()
        right = [block.copy() for block in left]
        right[0][0, 0] = np.sqrt(0.9)
        self.assertGreater(verifier.carrier_hilbert_schmidt_residual(left, right), 0.05)

    def test_result_is_deterministic(self) -> None:
        first = verifier.build_result((4,), steps=16)
        second = verifier.build_result((4,), steps=16)
        self.assertEqual(first, second)

    def test_nonfinite_stage_metrics_fail_closed(self) -> None:
        base = {
            "fresh_lineage_probability_before_admission": 0.0,
            "after_admission": {"purification_l2": 0.0},
            "after_transport": {"purification_l2": float("nan")},
        }
        with self.assertRaises(verifier.VerificationFailure):
            verifier.stage_maxima(base)
        base["after_transport"]["purification_l2"] = float("inf")
        with self.assertRaises(verifier.VerificationFailure):
            verifier.stage_maxima(base)

    def test_nonfinite_initial_metrics_fail_closed(self) -> None:
        with self.assertRaises(verifier.VerificationFailure):
            verifier.metric_maxima({"purification_l2": float("nan")})
        with self.assertRaises(verifier.VerificationFailure):
            verifier.metric_maxima({"full_norm_error": float("-inf")})

    def test_invalid_negative_squared_residual_fails_closed(self) -> None:
        with self.assertRaises(verifier.VerificationFailure):
            verifier.validated_nonnegative(-1.0e-3, 1.0, "test")
        self.assertEqual(verifier.validated_nonnegative(-1.0e-16, 1.0, "roundoff"), 0.0)

    @staticmethod
    def fake_row(length: int) -> dict[str, object]:
        return {"L": length, "passed": True}

    def test_primary_disposition_requires_l4_and_l6(self) -> None:
        with mock.patch.object(
            verifier,
            "verify_length",
            side_effect=lambda length, steps, explicit_trace: self.fake_row(length),
        ):
            empty = verifier.build_result((), steps=1)
            l4_only = verifier.build_result((4,), steps=1)
            primary = verifier.build_result((4, 6), steps=1)
        self.assertEqual(empty["classification"], "INVALID_EMPTY_LENGTH_SET")
        self.assertFalse(empty["passed"])
        self.assertEqual(l4_only["classification"], "INCOMPLETE_MANDATORY_PROTOCOL_COVERAGE")
        self.assertFalse(l4_only["passed"])
        self.assertEqual(primary["classification"], "CARRIER_REDUCTION_VERIFIED_FINITE")
        self.assertTrue(primary["primary_protocol_passed"])

    def test_l8_only_is_supplemental(self) -> None:
        with mock.patch.object(
            verifier,
            "verify_length",
            return_value=self.fake_row(8),
        ):
            result = verifier.build_result((8,), steps=1)
        self.assertEqual(
            result["classification"],
            "SUPPLEMENTAL_L8_CARRIER_REDUCTION_VERIFIED_FINITE",
        )
        self.assertTrue(result["passed"])
        self.assertFalse(result["primary_protocol_passed"])
        self.assertTrue(result["supplemental_l8_passed"])

    def test_frozen_document_hashes_are_bound(self) -> None:
        records = verifier.authenticate_frozen_documents()
        for label, (_, expected) in verifier.FROZEN_DOCUMENTS.items():
            self.assertEqual(records[label]["sha256"], expected)


if __name__ == "__main__":
    unittest.main()
