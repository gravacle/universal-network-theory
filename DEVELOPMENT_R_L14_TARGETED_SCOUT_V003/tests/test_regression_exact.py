#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from regression_exact import (  # noqa: E402
    ExactKernelRefusal,
    _compare_classification_values,
)


def audit() -> dict[str, float | int]:
    return {
        "float_values": 0,
        "exact_discrete_values": 0,
        "maximum_absolute_difference": 0.0,
        "maximum_relative_difference": 0.0,
        "relative_tolerance": 1.0e-12,
        "absolute_tolerance": 5.0e-15,
    }


class ClassificationRegressionTests(unittest.TestCase):
    def test_cross_libm_ulp_difference_is_audited(self):
        record = audit()
        _compare_classification_values(
            {"score": 0.013920578614787472, "checks": {"passes": False}},
            {"score": 0.013920578614787746, "checks": {"passes": False}},
            "root",
            record,
        )
        self.assertEqual(record["float_values"], 1)
        self.assertGreater(record["maximum_relative_difference"], 0.0)

    def test_material_float_difference_fails_closed(self):
        with self.assertRaises(ExactKernelRefusal):
            _compare_classification_values(1.0, 1.0 + 1.0e-8, "root", audit())

    def test_discrete_decision_difference_fails_closed(self):
        with self.assertRaises(ExactKernelRefusal):
            _compare_classification_values(
                {"checks": {"passes": False}},
                {"checks": {"passes": True}},
                "root",
                audit(),
            )


if __name__ == "__main__":
    unittest.main()
