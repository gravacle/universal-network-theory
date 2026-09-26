#!/usr/bin/env python3
"""Synthetic-only tests for the target joint-witness implementation.

These tests must not evolve or inspect the mandatory L4/L6/L8 histories.
"""

from __future__ import annotations

import unittest
from unittest import mock

import numpy as np

import target_joint_witness as witness


def empty_blocks(length: int) -> tuple[list[np.ndarray], list[witness.SectorGeometry]]:
    geometries = [witness.SectorGeometry.build(length, q) for q in range(length + 1)]
    blocks = [np.zeros(geometry.kernel.shape, dtype=float) for geometry in geometries]
    return blocks, geometries


class SyntheticWitnessTests(unittest.TestCase):
    def test_frozen_protocol_hash(self) -> None:
        record = witness.authenticate_protocol()
        self.assertEqual(record["sha256"], witness.PROTOCOL_SHA256)

    def test_match_and_cross_have_opposite_registered_witness(self) -> None:
        length = 2
        matched, geometries = empty_blocks(length)
        crossed, _ = empty_blocks(length)
        # q=1 lineages are {0},{1}; first carrier columns are {0},{1}.
        matched[1][0, 0] = 0.5
        matched[1][1, 1] = 0.5
        crossed[1][0, 1] = 0.5
        crossed[1][1, 0] = 0.5
        match_result = witness.evaluate_probability_blocks(matched, geometries)
        cross_result = witness.evaluate_probability_blocks(crossed, geometries)
        self.assertAlmostEqual(match_result["registered"]["D"], 1.0 / (2 * length), places=15)
        self.assertAlmostEqual(cross_result["registered"]["D"], -1.0 / (2 * length), places=15)
        self.assertAlmostEqual(match_result["registered"]["w_sham"], 0.0, places=15)
        self.assertAlmostEqual(cross_result["registered"]["w_sham"], 0.0, places=15)
        match_accumulator = witness.accumulate_sector_rows(matched[1], geometries[1])
        cross_accumulator = witness.accumulate_sector_rows(crossed[1], geometries[1])
        np.testing.assert_allclose(
            match_accumulator["carrier_marginal"],
            cross_accumulator["carrier_marginal"],
        )
        np.testing.assert_allclose(
            match_accumulator["lineage_marginal"],
            cross_accumulator["lineage_marginal"],
        )

    def test_sector_matched_product_has_zero_D(self) -> None:
        length = 2
        blocks, geometries = empty_blocks(length)
        lineage = np.array([0.3, 0.7])
        carrier = np.array([0.2, 0.3, 0.1, 0.4])
        blocks[1] = np.outer(lineage, carrier)
        result = witness.evaluate_probability_blocks(blocks, geometries)
        self.assertAlmostEqual(result["registered"]["D"], 0.0, places=15)
        self.assertAlmostEqual(
            result["negative_controls"]["sham_replacement_D"], 0.0, places=15
        )
        self.assertAlmostEqual(
            result["negative_controls"]["shuffle_replacement_w"], 0.0, places=15
        )
        self.assertLessEqual(result["residuals"]["sham_self_covariance"], 1.0e-15)

    def test_exact_shuffle_identity_is_zero(self) -> None:
        for length in (2, 3, 5):
            for q in range(length + 1):
                geometry = witness.SectorGeometry.build(length, q)
                carrier = np.linspace(1.0, 2.0, len(geometry.carrier_words))
                value, residual = witness._shuffle_identity(geometry, carrier)
                self.assertEqual(value, 0.0)
                self.assertEqual(residual, 0.0)

    def test_row_and_column_streams_agree_on_synthetic_state(self) -> None:
        length = 3
        blocks, geometries = empty_blocks(length)
        values = np.arange(1, blocks[1].size + 1, dtype=float).reshape(blocks[1].shape)
        blocks[1] = values / np.sum(values)
        result = witness.evaluate_probability_blocks(blocks, geometries)
        self.assertLessEqual(result["residuals"]["row_column_accumulator"], 1.0e-14)
        self.assertLessEqual(result["residuals"]["marginal_reconstruction"], 1.0e-14)

    def test_nonfinite_and_negative_probabilities_fail_closed(self) -> None:
        blocks, geometries = empty_blocks(2)
        blocks[1][0, 0] = float("nan")
        with self.assertRaises(witness.WitnessFailure):
            witness.evaluate_probability_blocks(blocks, geometries)
        blocks, geometries = empty_blocks(2)
        blocks[1][0, 0] = -1.0e-17
        with self.assertRaises(witness.WitnessFailure):
            witness.evaluate_probability_blocks(blocks, geometries)

    def test_target_classification_requires_exact_mandatory_set(self) -> None:
        valid = [{"L": length, "passed": True} for length in witness.MANDATORY_LENGTHS]
        classification, passed = witness.classify_target(valid)
        self.assertTrue(passed)
        self.assertIn("AWAITING_INDEPENDENT", classification)
        for rows in ((), ({"L": 4, "passed": True},), tuple(reversed(valid))):
            classification, passed = witness.classify_target(rows)
            self.assertFalse(passed)
            self.assertIn("INVALID_MANDATORY_SIZE_SET", classification)

    def test_numeric_failure_returns_deterministic_unresolved_record(self) -> None:
        with mock.patch.object(
            witness, "run_resolution", side_effect=witness.WitnessFailure("synthetic failure")
        ):
            result = witness.build_target_result()
        self.assertFalse(result["passed"])
        self.assertEqual(
            result["classification"],
            "TARGET_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED",
        )
        self.assertEqual(result["failure"]["message"], "synthetic failure")
        self.assertEqual(result["rows"], [])

    def test_l4_exhaustive_control_on_synthetic_product(self) -> None:
        blocks, geometries = empty_blocks(4)
        lineage = np.arange(1, len(geometries[1].lineage_words) + 1, dtype=float)
        lineage /= np.sum(lineage)
        carrier = np.arange(1, len(geometries[1].carrier_words) + 1, dtype=float)
        carrier /= np.sum(carrier)
        blocks[1] = np.outer(lineage, carrier)
        result = witness.evaluate_probability_blocks(blocks, geometries, l4_exhaustive=True)
        self.assertLessEqual(result["l4_exhaustive"]["streamed_agreement"], 1.0e-14)
        self.assertLessEqual(abs(result["l4_exhaustive"]["w_shuffle"]), 1.0e-14)


if __name__ == "__main__":
    unittest.main()
