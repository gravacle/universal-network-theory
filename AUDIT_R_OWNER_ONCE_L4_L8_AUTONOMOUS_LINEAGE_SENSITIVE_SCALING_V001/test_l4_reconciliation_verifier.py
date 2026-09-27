#!/usr/bin/env python3
"""Mutation tests for the post-seal L4 reconciliation gate."""

from __future__ import annotations

import copy
import unittest

import reconcile_l4


class L4ReconciliationMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.target = reconcile_l4.load_exact(
            reconcile_l4.TARGET_RESULT, reconcile_l4.TARGET_SHA256
        )
        cls.hostile = reconcile_l4.load_exact(
            reconcile_l4.HOSTILE_RESULT, reconcile_l4.HOSTILE_SHA256
        )

    def test_sealed_inputs_reconcile_before_mutation(self) -> None:
        result = reconcile_l4.build_reconciliation(self.target, self.hostile)
        self.assertTrue(result["passed"])
        self.assertTrue(result["all_registered_common_fields_pass"])
        self.assertTrue(
            result["classification_reconciliation"][
                "semantic_disposition_compatible"
            ]
        )
        self.assertLessEqual(
            result["maximum_non_T_dyn_absolute_difference"],
            reconcile_l4.TOLERANCE,
        )
        self.assertLessEqual(result["maximum_registered_tolerance_fraction"], 1.0)

    def test_aggregate_observable_mutation_fails_numerical_gate(self) -> None:
        target = copy.deepcopy(self.target)
        target["after_transport"]["carrier_configuration_tv"] += 1.0e-4
        result = reconcile_l4.build_reconciliation(target, self.hostile)
        self.assertFalse(result["passed"])
        self.assertFalse(result["all_registered_common_fields_pass"])
        mutated = next(
            item
            for item in result["registered_comparisons"]
            if item["field"] == "after_transport.carrier_configuration_tv"
        )
        self.assertFalse(mutated["passed"])

    def test_sector_invariant_mutation_fails_numerical_gate(self) -> None:
        target = copy.deepcopy(self.target)
        target["sector_results"][2]["after_transport"]["trace_actual"] += 1.0e-4
        result = reconcile_l4.build_reconciliation(target, self.hostile)
        self.assertFalse(result["passed"])
        self.assertFalse(
            result["per_sector_reconciliation"][2][
                "all_common_invariants_pass"
            ]
        )

    def test_hostile_classification_mutation_fails_typed_gate(self) -> None:
        hostile = copy.deepcopy(self.hostile)
        hostile["events"][0]["classification"] = "UNRESOLVED"
        result = reconcile_l4.build_reconciliation(self.target, hostile)
        self.assertFalse(result["passed"])
        self.assertTrue(result["all_registered_common_fields_pass"])
        self.assertFalse(
            result["classification_reconciliation"][
                "semantic_disposition_compatible"
            ]
        )

    def test_hostile_control_mutation_fails_typed_gate(self) -> None:
        hostile = copy.deepcopy(self.hostile)
        hostile["events"][0]["controls_pass"] = False
        result = reconcile_l4.build_reconciliation(self.target, hostile)
        self.assertFalse(result["passed"])
        self.assertFalse(
            result["classification_reconciliation"][
                "semantic_disposition_compatible"
            ]
        )

    def test_target_execution_status_mutation_fails_typed_gate(self) -> None:
        target = copy.deepcopy(self.target)
        target["status"] = "L6_EXECUTED_WITHOUT_AUTHORIZATION"
        result = reconcile_l4.build_reconciliation(target, self.hostile)
        self.assertFalse(result["passed"])
        self.assertFalse(
            result["classification_reconciliation"][
                "semantic_disposition_compatible"
            ]
        )

    def test_wrong_hash_is_rejected_before_json_use(self) -> None:
        with self.assertRaisesRegex(
            reconcile_l4.ReconciliationFailure, "sealed input changed"
        ):
            reconcile_l4.load_exact(reconcile_l4.TARGET_RESULT, "0" * 64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
