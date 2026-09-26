#!/usr/bin/env python3
"""Focused fail-closed tests for the L8 curvature-result validator."""

from __future__ import annotations

import copy
import unittest

import validate_result as target


class ResultValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = target.read_json(target.RESULT)

    def accepted(self, mutation) -> bool:
        candidate = copy.deepcopy(self.record)
        mutation(candidate)
        try:
            target.validate(candidate, authenticate_packet=False)
        except target.ValidationFailure:
            return False
        return True

    def test_frozen_result_passes(self) -> None:
        self.assertGreater(target.validate(copy.deepcopy(self.record), authenticate_packet=False), 80)

    def test_classification_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value.__setitem__("classification", "PASS")))

    def test_claim_ceiling_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value.__setitem__("graph_ceiling", "GRAVITY")))

    def test_unexpected_key_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value.__setitem__("extra", 1)))

    def test_edge_curvature_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value["edge_curvature"].__setitem__(0, 0.4)))

    def test_node_curvature_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value["node_curvature"].__setitem__(1, 0.2)))

    def test_record_concentration_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value["record_concentration"].__setitem__(0, 2.0)))

    def test_rho_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value["statistic"].__setitem__("rho_observed", 0.9)))

    def test_tail_count_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value["statistic"].__setitem__("plus_count", 1)))

    def test_sector_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value["terminal_sector_weights"].__setitem__(0, 0.2)))

    def test_source_hash_mutation_fails(self) -> None:
        def mutate(value):
            key = next(iter(value["controls"]["source_hashes"]))
            value["controls"]["source_hashes"][key] = "0" * 64
        self.assertFalse(self.accepted(mutate))

    def test_input_hash_mutation_fails(self) -> None:
        def mutate(value):
            key = next(iter(value["controls"]["input_hashes"]))
            value["controls"]["input_hashes"][key] = "0" * 64
        self.assertFalse(self.accepted(mutate))

    def test_shard_hash_mutation_fails(self) -> None:
        def mutate(value):
            key = next(iter(value["controls"]["shard_hashes"]))
            value["controls"]["shard_hashes"][key] = "0" * 64
        self.assertFalse(self.accepted(mutate))

    def test_runtime_budget_mutation_fails(self) -> None:
        self.assertFalse(self.accepted(lambda value: value["controls"].__setitem__("wall_seconds", 301.0)))


if __name__ == "__main__":
    unittest.main()
