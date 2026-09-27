#!/usr/bin/env python3
"""Tests for the fail-closed CMC-1 reconciliation."""

from __future__ import annotations

import copy
import unittest

import reconcile_closure as reconciliation


class ClosureReconciliationTests(unittest.TestCase):
    def test_current_packets_reconcile(self) -> None:
        result = reconciliation.build_disposition()
        self.assertEqual(result["disposition"], reconciliation.PASS)

    def test_target_classification_tamper_fails(self) -> None:
        target = reconciliation.load_json("target_primary_result")
        target = copy.deepcopy(target)
        target["classification"] = "CARRIER_REDUCTION_MISMATCH"
        with self.assertRaises(reconciliation.ReconciliationFailure):
            reconciliation.validate_target(target)

    def test_missing_mandatory_target_row_fails(self) -> None:
        target = reconciliation.load_json("target_primary_result")
        target = copy.deepcopy(target)
        target["rows"] = target["rows"][:1]
        with self.assertRaises(reconciliation.ReconciliationFailure):
            reconciliation.validate_target(target)

    def test_hostile_independence_tamper_fails(self) -> None:
        hostile = reconciliation.load_json("hostile_result")
        hostile = copy.deepcopy(hostile)
        hostile["independence"]["target_result_values_read"] = True
        with self.assertRaises(reconciliation.ReconciliationFailure):
            reconciliation.validate_hostile(hostile)

    def test_nonfinite_tree_fails(self) -> None:
        with self.assertRaises(reconciliation.ReconciliationFailure):
            reconciliation.require_finite_tree({"bad": float("nan")})


if __name__ == "__main__":
    unittest.main()
