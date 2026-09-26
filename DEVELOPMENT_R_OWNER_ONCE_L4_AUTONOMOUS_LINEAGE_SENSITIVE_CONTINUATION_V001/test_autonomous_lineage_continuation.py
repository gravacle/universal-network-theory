#!/usr/bin/env python3
"""Pre-output tests; these never execute the frozen continuation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

import autonomous_lineage_continuation as continuation


class ProspectiveFreezeTests(unittest.TestCase):
    def test_freeze_authenticates(self) -> None:
        records = continuation.authenticate_freeze()
        self.assertEqual(len(records), 4)
        self.assertIn("SOURCE_HASHES.sha256", records)

    def test_result_is_absent_before_review(self) -> None:
        self.assertFalse(continuation.OUTPUT.exists())

    def test_freeze_is_explicitly_pre_output(self) -> None:
        frozen = json.loads(continuation.FREEZE.read_text())
        self.assertEqual(frozen["status"], "FROZEN_CANDIDATE__PRE_REVIEW_AND_PRE_OUTPUT")
        self.assertIn("NO_SCALING", frozen["claim_boundary"])
        self.assertEqual(
            frozen["comparator"]["cross_sector_coherence"],
            "REMOVED_SYMMETRICALLY_IN_BOTH_ARMS",
        )

    def test_exact_checkpoint_fingerprint(self) -> None:
        module = continuation.load_parent()
        parent, state = continuation.regenerate_checkpoint(module, continuation.FINE_STEPS)
        self.assertEqual(len(state), 495)
        self.assertEqual(
            continuation.array_sha256(parent.words, "<u4"), continuation.BASIS_SHA256
        )
        self.assertEqual(
            continuation.array_sha256(state, "<c16"), continuation.CHECKPOINT_SHA256
        )

    def test_product_arm_preserves_both_quantum_marginals(self) -> None:
        module = continuation.load_parent()
        parent, state = continuation.regenerate_checkpoint(module, continuation.FINE_STEPS)
        actual, product, _ = continuation.build_sector_arms(parent, state)
        lineage, carrier, _ = continuation.labels(parent)
        actual_s, actual_c = continuation.reduced_marginals(actual, lineage, carrier)
        product_s, product_c = continuation.reduced_marginals(product, lineage, carrier)
        self.assertLess(float(np.max(np.abs(actual_s - product_s))), 1.0e-13)
        self.assertLess(float(np.max(np.abs(actual_c - product_c))), 1.0e-13)
        self.assertLess(abs(float(np.trace(actual).real) - 1.0), 1.0e-12)
        self.assertLess(abs(float(np.trace(product).real) - 1.0), 1.0e-12)

    def test_protocol_freezes_primary_statistic_and_falsifier(self) -> None:
        text = Path(continuation.PROTOCOL).read_text()
        self.assertIn("T_{\\rm dyn}=\\Delta_C/\\tau", text)
        self.assertIn("FALSIFIED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION_IN_FIXED_TEST", text)
        self.assertIn("initial carrier marginals are equal by construction", text)

    def test_admission_is_unitary_without_running_continuation(self) -> None:
        module = continuation.load_parent()
        parent = module.Parent(continuation.LENGTH)
        self.assertLess(continuation.admission_unitarity_residual(parent), 1.0e-13)

    def test_normalized_range_guard(self) -> None:
        record = {
            key: {
                "carrier_trace_distance": 0.0,
                "carrier_configuration_tv": 0.0,
                "carrier_number_sector_tv": 0.0,
                "occupation_rms": 0.0,
            }
            for key in ("after_admission", "after_transport")
        }
        self.assertTrue(continuation.normalized_ranges_pass(record))
        record["after_transport"]["occupation_rms"] = 1.01
        self.assertFalse(continuation.normalized_ranges_pass(record))


if __name__ == "__main__":
    unittest.main()
