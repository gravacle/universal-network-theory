#!/usr/bin/env python3
"""Gateway tests for the L14 mass-ledger reduction and resource audit."""

from __future__ import annotations

import math
import unittest

import l14_mass_feasibility as feasibility
import l14_mass_ledger as reduction


class MassFeasibilityTests(unittest.TestCase):
    def test_shape_arithmetic_reproduces_frozen_l12_vandermonde_totals(self):
        self.assertEqual(
            feasibility.state_bytes(12, 11, 11),
            math.comb(35, 11) * 16,
        )
        self.assertEqual(
            feasibility.state_bytes(12, 10, 11),
            math.comb(34, 10) * 16,
        )

    def test_phase1_requires_lower_triangular_prefix_and_exceeds_guard(self):
        case = feasibility.exact_prefix_case(7)
        self.assertEqual(case["required_q_shards"], list(range(8)))
        self.assertEqual(case["prefix_13_bytes"], 45_126_260_000)
        self.assertEqual(case["admission_peak_lower_bound_bytes"], 67_119_641_280)
        self.assertFalse(case["fits_frozen_scratch_limit"])

    def test_phase3_exact_mass_exceeds_current_representation_guard(self):
        case = feasibility.exact_prefix_case(9)
        self.assertEqual(case["required_q_shards"], list(range(10)))
        self.assertEqual(case["prefix_13_bytes"], 188_143_294_160)
        self.assertEqual(case["admission_peak_lower_bound_bytes"], 259_065_155_040)
        self.assertFalse(case["fits_frozen_scratch_limit"])

    def test_translation_orbit_burnside_census_is_integral(self):
        for q in range(4, 10):
            orbits = feasibility.translation_orbit_count(14, q)
            words = math.comb(28, q)
            self.assertGreater(orbits, 0)
            self.assertLessEqual(orbits, words)


class ReductionAuditTests(unittest.TestCase):
    def test_two_gaussian_constructions_agree_internally(self):
        direct = reduction.reduced_history(6)
        global_rows = reduction.global_history(6)
        self.assertLessEqual(
            reduction.maximum_row_difference(direct, global_rows), 2.0e-12
        )

    def test_gaussian_candidate_is_rejected_by_preserved_many_body_histories(self):
        report = reduction.build_audit()
        self.assertEqual(
            report["classification"],
            "GAUSSIAN_MASS_REDUCTION_REFUTED_BY_PRESERVED_HISTORY",
        )
        self.assertFalse(report["regression_validation"]["passed"])
        self.assertGreater(
            report["regression_validation"]["maximum_sector_weight_difference"],
            1.0e-2,
        )
        self.assertNotIn("sector_masses", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
