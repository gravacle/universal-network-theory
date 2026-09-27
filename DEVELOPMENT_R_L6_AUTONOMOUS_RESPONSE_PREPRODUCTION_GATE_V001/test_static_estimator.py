#!/usr/bin/env python3
"""Synthetic/static tests only; no L6 scientific engine is imported."""

from __future__ import annotations

import json
import math
import unittest
from pathlib import Path

import static_estimator as estimator


PACKET = Path(__file__).resolve().parent


class StaticEstimatorTests(unittest.TestCase):
    def test_seven_exact_carrier_dimensions(self) -> None:
        self.assertEqual(
            [estimator.sector_bounds(q)["carrier_dimension"] for q in range(7)],
            [1, 12, 66, 220, 495, 792, 924],
        )

    def test_conservative_factors_and_maxima(self) -> None:
        report = estimator.static_report()
        self.assertEqual(report["max_carrier_dimension"], 924)
        self.assertEqual(report["max_combined_factor_columns_bound"], 260)
        self.assertEqual(report["max_raw_complex_factor_bytes_bound"], 1655280)
        self.assertEqual(report["max_reduced_hermitian_bytes_bound"], 774400)
        for row in report["sectors"]:
            q = row["q_out"]
            self.assertEqual(row["lineage_dimension"], math.comb(6, q))
            self.assertEqual(
                row["raw_complex_factor_bytes_bound"],
                16 * row["carrier_dimension"] * row["combined_factor_columns_bound"],
            )

    def test_invalid_q_refused(self) -> None:
        for q in (-1, 7, 0.0, True):
            with self.subTest(q=q), self.assertRaises(ValueError):
                estimator.sector_bounds(q)

    def test_task_dependency_census(self) -> None:
        plan = json.loads((PACKET / "TASK_PLAN.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["status"], "DESIGN_ONLY_NO_RUNNER_OR_EXECUTION_AUTHORIZATION")
        self.assertEqual(len(plan["tasks"]), 7)
        for q, task in enumerate(plan["tasks"]):
            self.assertEqual(task["q_out"], q)
            self.assertEqual(task["work_units"], math.comb(12, q))
            terminal = list(range(max(0, q - 1), min(6, q + 1) + 1))
            preterminal = sorted({old for t in terminal for old in (t - 1, t) if 0 <= old < 6})
            self.assertEqual(task["terminal_q_inputs"], terminal)
            self.assertEqual(task["preterminal_q_inputs"], preterminal)

    def test_lock_state(self) -> None:
        gates = json.loads((PACKET / "GATE_MATRIX.json").read_text(encoding="utf-8"))
        self.assertEqual(gates["status"], "LOCKED_NO_L6_NUMERICAL_EXECUTION")
        self.assertIs(gates["L6_execution_authorized"], False)
        self.assertIs(gates["L8_execution_authorized"], False)
        self.assertIs(gates["has_L6_numerical_runner"], False)
        self.assertIsNone(gates["evidence"]["L6_response_wall_seconds"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
