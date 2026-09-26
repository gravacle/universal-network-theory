#!/usr/bin/env python3
"""Strict regression tests for the independent L4 continuation audit."""

from __future__ import annotations

import importlib.util
import json
import math
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = HERE / "independent_validate.py"
RESULT = HERE / "INDEPENDENT_RESULT.json"
EXPECTED_RESULT_SHA256 = "86316a114201046f87789884c207ebe4d21356d0405475327e7bce455dd0352e"


def load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("independent_l4_validator", SOURCE)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load independent validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_finite_tree(test: unittest.TestCase, value: Any) -> None:
    if isinstance(value, dict):
        for child in value.values():
            assert_finite_tree(test, child)
    elif isinstance(value, list):
        for child in value:
            assert_finite_tree(test, child)
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        test.assertTrue(math.isfinite(float(value)))


class IndependentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.result = json.loads(RESULT.read_text())

    def test_result_custody(self) -> None:
        self.assertEqual(self.validator.sha256_file(RESULT), EXPECTED_RESULT_SHA256)
        self.assertEqual(self.validator.authenticate(), self.result["custody"])

    def test_contraction_source_excludes_warning_route(self) -> None:
        source = SOURCE.read_text()
        self.assertNotIn(chr(64), source)
        self.assertNotIn(".dot(", source)
        self.assertNotIn("matmul", source)
        self.assertNotIn("np.kron", source)
        self.assertIn('optimize=False', source)

    def test_independent_checkpoint_fingerprints(self) -> None:
        parent = self.validator.IndependentParent()
        self.assertEqual(
            self.validator.array_sha256(parent.words, "<u4"),
            self.validator.EXPECTED_BASIS_SHA256,
        )
        fine = parent.checkpoint(self.validator.FINE_STEPS)
        self.assertEqual(
            self.validator.array_sha256(fine, "<c16"),
            self.validator.EXPECTED_FINE_CHECKPOINT_SHA256,
        )

    def test_disposition_and_claim_ceiling(self) -> None:
        self.assertTrue(self.result["passed"])
        self.assertEqual(
            self.result["disposition"],
            "PASS_INDEPENDENT_L4_LINEAGE_SENSITIVE_CONTINUATION_VALIDATION",
        )
        self.assertEqual(
            self.result["classification"],
            "RESOLVED_L4_LINEAGE_SENSITIVE_CARRIER_CONTINUATION",
        )
        boundary = self.result["claim_boundary"]
        for excluded in ("NO_SCALING", "CURVATURE", "GEOMETRY", "GRAVITY"):
            self.assertIn(excluded, boundary)

    def test_warning_and_nonfinite_gate(self) -> None:
        self.assertEqual(self.result["warning_audit"]["captured_warnings"], [])
        self.assertFalse(self.result["warning_audit"]["accepted_on_faith"])
        assert_finite_tree(self, self.result)

    def test_primary_effect_reproduces(self) -> None:
        fine = self.result["fine"]["after_transport"]
        self.assertAlmostEqual(fine["carrier_trace_distance"], 0.14761185701903007, places=15)
        self.assertEqual(self.result["tau"], 1.0e-10)
        self.assertGreater(self.result["T_dyn"], 1.0e9)
        self.assertLess(
            self.result["controls"]["target_registered_observable_max_abs_difference"],
            2.0e-16,
        )

    def test_initial_carrier_equality_and_transport_invariance(self) -> None:
        controls = self.result["fine"]["controls"]
        self.assertLess(controls["carrier_marginal_equality"], 1.0e-16)
        self.assertLess(controls["lineage_marginal_equality"], 1.0e-16)
        self.assertLess(controls["q_weight_equality"], 2.0e-16)
        self.assertLess(controls["trace_distance_transport_invariance"], 2.0e-16)

    def test_occupation_profile_is_transport_sensitive(self) -> None:
        fine = self.result["fine"]
        self.assertLess(fine["after_admission"]["occupation_rms"], 2.0e-15)
        self.assertAlmostEqual(
            fine["after_transport"]["occupation_rms"],
            0.006009875541368592,
            places=16,
        )

    def test_all_controls_are_strictly_inside_frozen_limits(self) -> None:
        controls = self.result["controls"]
        self.assertTrue(controls["normalized_ranges"])
        self.assertLess(controls["coarse_fine_maximum"], 1.0e-8)
        self.assertLess(controls["maximum_residual"], 1.0e-11)
        self.assertGreaterEqual(
            self.result["fine"]["minimum_density_eigenvalue"], -1.0e-10
        )


if __name__ == "__main__":
    unittest.main()
