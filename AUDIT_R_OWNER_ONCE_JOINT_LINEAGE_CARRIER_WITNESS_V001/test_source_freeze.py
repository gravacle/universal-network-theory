#!/usr/bin/env python3
"""Non-physical source-freeze tests for the hostile joint witness.

These tests use only synthetic L2/L3 controls.  They do not call the seed
reporter and do not generate or inspect L4/L6/L8 physical witness values.
"""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

import numpy as np

import independent_joint_witness as hostile


HERE = Path(__file__).resolve().parent


def two_term_blocks(parent: hostile.Parent, crossed: bool) -> list[np.ndarray]:
    blocks = [
        np.zeros(
            (len(sector.lineage_words), len(sector.carrier_words)),
            dtype=np.complex128,
        )
        for sector in parent.sectors
    ]
    sector = parent.sectors[1]
    amplitude = 1.0 / math.sqrt(2.0)
    terms = [
        (1 << 0, 1 << (1 if crossed else 0)),
        (1 << 1, 1 << (0 if crossed else 1)),
    ]
    for lineage, carrier in terms:
        blocks[1][
            sector.lineage_lookup[lineage], sector.carrier_lookup[carrier]
        ] = amplitude
    return blocks


def carrier_reduced(blocks: list[np.ndarray]) -> list[np.ndarray]:
    return [
        np.einsum("sc,sd->cd", block, block.conj(), optimize=False)
        for block in blocks
    ]


class SourceFreezeTests(unittest.TestCase):
    def test_frozen_protocol_hash(self) -> None:
        self.assertEqual(
            hostile.sha256_file(hostile.PROTOCOL), hostile.EXPECTED_PROTOCOL_SHA256
        )

    def test_independent_basis_and_prism_census_on_synthetic_l3(self) -> None:
        parent = hostile.build_parent(3)
        self.assertEqual(len(parent.edges), 9)
        degree = [0] * parent.sites
        for left, right, _ in parent.edges:
            degree[left] += 1
            degree[right] += 1
        self.assertEqual(degree, [3] * parent.sites)
        self.assertEqual(parent.sectors[1].lineage_words, (4, 2, 1))
        self.assertEqual(parent.sectors[1].carrier_words, (32, 16, 8, 4, 2, 1))

    def test_synthetic_l2_admission_pair_and_norm(self) -> None:
        parent = hostile.build_parent(2)
        before = hostile.blank_state(parent)
        after = hostile.admit(parent, before, 0)
        self.assertAlmostEqual(hostile.state_norm(after), 1.0, places=15)
        self.assertAlmostEqual(after[0][0, 0].real, math.cos(hostile.PHI), places=15)
        sector = parent.sectors[1]
        amplitude = after[1][
            sector.lineage_lookup[1], sector.carrier_lookup[1]
        ]
        self.assertAlmostEqual(amplitude.real, 0.0, places=15)
        self.assertAlmostEqual(amplitude.imag, -math.sin(hostile.PHI), places=15)

    def test_synthetic_l2_transport_is_numerically_controlled(self) -> None:
        parent = hostile.build_parent(2)
        state = hostile.admit(parent, hostile.blank_state(parent), 0)
        evolved, drift, absolute = hostile.transport(parent, state, 8)
        self.assertEqual(len(evolved), 3)
        self.assertLess(drift, 1.0e-8)
        self.assertLess(absolute, 1.0e-8)

    def test_nonidentifiability_pair_has_same_carrier_marginal(self) -> None:
        parent = hostile.build_parent(3)
        matched = two_term_blocks(parent, crossed=False)
        crossed = two_term_blocks(parent, crossed=True)
        for left, right in zip(carrier_reduced(matched), carrier_reduced(crossed)):
            self.assertLess(float(np.max(np.abs(left - right))), 1.0e-15)

        matched_result = hostile.evaluate_witness(
            parent, matched, include_negative_controls=True
        )
        crossed_result = hostile.evaluate_witness(
            parent, crossed, include_negative_controls=True
        )
        expected = 1.0 / (2.0 * parent.length)
        self.assertAlmostEqual(matched_result["D_L"], expected, places=15)
        self.assertAlmostEqual(crossed_result["D_L"], -expected, places=15)
        self.assertLess(matched_result["row_column_disagreement"], 1.0e-15)
        self.assertLess(crossed_result["row_column_disagreement"], 1.0e-15)
        self.assertLess(
            matched_result["controls"]["sham_self_covariance_residual"], 1.0e-15
        )

    def test_synthetic_l3_full_shuffle_enumeration_is_zero(self) -> None:
        parent = hostile.build_parent(3)
        blocks = two_term_blocks(parent, crossed=False)
        value = hostile.exhaustive_shuffle_expectation(parent, blocks)
        self.assertLess(abs(value), 1.0e-15)

    def test_synthetic_l3_dense_direct_sums_match_streamed_accumulators(self) -> None:
        parent = hostile.build_parent(3)
        blocks = two_term_blocks(parent, crossed=False)
        streamed = hostile.evaluate_witness(
            parent, blocks, include_negative_controls=True
        )
        direct = hostile.exhaustive_direct_controls(parent, blocks)
        self.assertAlmostEqual(
            direct["observed"], streamed["row_accumulator"]["observed"], places=15
        )
        self.assertAlmostEqual(
            direct["sham"], streamed["row_accumulator"]["sham"], places=15
        )
        self.assertAlmostEqual(direct["witness"], streamed["D_L"], places=15)
        self.assertLess(streamed["q_identity_residual"], 1.0e-15)
        self.assertLess(streamed["total_content_residual"], 1.0e-15)

    def test_source_schema_is_deterministic_and_nonphysical(self) -> None:
        first = json.dumps(
            hostile.synthetic_schema_record(), sort_keys=True, allow_nan=False
        )
        second = json.dumps(
            hostile.synthetic_schema_record(), sort_keys=True, allow_nan=False
        )
        self.assertEqual(first, second)
        self.assertIn("HOSTILE_SOURCE_FROZEN_READY", first)
        self.assertNotIn(str(hostile.ROOT), first)
        self.assertNotIn("w_L", first)
        self.assertNotIn("D_L", first)

    def test_source_does_not_import_or_name_target_implementation(self) -> None:
        source = (HERE / "independent_joint_witness.py").read_text()
        self.assertNotIn("TARGET_RESULT.json", source)
        self.assertNotIn("target_joint_witness", source)
        self.assertNotIn("import compute_seed_history", source)
        self.assertNotIn("import compute_streamed_history", source)

    def test_witness_readout_avoids_blas_backed_reductions(self) -> None:
        source = (HERE / "independent_joint_witness.py").read_text()
        self.assertNotIn("np.dot(", source)
        self.assertNotIn(" @ ", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
