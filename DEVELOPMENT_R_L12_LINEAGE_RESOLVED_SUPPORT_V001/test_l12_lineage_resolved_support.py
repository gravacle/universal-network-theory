#!/usr/bin/env python3
"""Focused unit tests for the frozen lineage measure and Stage-6 autopsy."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "lineage", HERE / "l12_lineage_resolved_support.py"
)
assert SPEC is not None and SPEC.loader is not None
lineage = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = lineage
SPEC.loader.exec_module(lineage)


def mask(*events: int) -> int:
    answer = 0
    for event in events:
        answer |= 1 << (event - 1)
    return answer


class LineageMeasureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.buckets = {
            "strict_window_common_lineage": np.zeros(7),
            "prewindow_entry_then_window_exit": np.zeros(7),
            "no_exit_by_event_12": np.zeros(7),
        }

    def test_strict_common_lineage_is_resident_only_between_entry_and_exit(self) -> None:
        lineage.add_lineage_mass(self.buckets, mask(1, 2, 3, 4, 7, 10), 0.25)
        self.assertEqual(
            self.buckets["strict_window_common_lineage"].tolist(),
            [0.0, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0],
        )

    def test_prewindow_entry_and_no_exit_are_separate(self) -> None:
        lineage.add_lineage_mass(self.buckets, mask(1, 2, 3, 4, 5, 9), 0.2)
        lineage.add_lineage_mass(self.buckets, mask(1, 2, 3, 4, 8), 0.3)
        self.assertEqual(
            self.buckets["prewindow_entry_then_window_exit"].tolist(),
            [0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0],
        )
        self.assertEqual(
            self.buckets["no_exit_by_event_12"].tolist(),
            [0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 0.3],
        )

    def test_row_split_conserves_probability(self) -> None:
        shard = np.asarray([[1 + 0j, 2 + 0j], [3 + 0j, 4 + 0j]], dtype=np.complex128)
        stay, accepted = lineage.row_split(shard, np.asarray([1], dtype=np.int32))
        original = np.sum(abs(shard) ** 2, axis=1)
        np.testing.assert_allclose(stay + accepted, original, atol=1e-15, rtol=0)

    def test_atomic_report_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            lineage.atomic_create_json(path, {"ok": True})
            with self.assertRaises(lineage.Refusal):
                lineage.atomic_create_json(path, {"ok": False})


class RealAutopsyTests(unittest.TestCase):
    def test_real_stage6_false_predicates_are_completely_accounted(self) -> None:
        document = lineage.authenticate_json(
            lineage.DEFAULT_STAGE6, lineage.PINNED_SHA256["stage6"], "Stage-6"
        )
        result = lineage.failed_predicate_autopsy(document)
        self.assertEqual(
            result["A011"]["branches"]["target"]["false_predicates"],
            ["exponents_agree", "tail_scaled_chi_stable", "tail_scaled_gap_stable"],
        )
        self.assertEqual(
            result["A016"]["branches"]["target"]["false_predicates"],
            ["fixed_z1_beats_positive_gap", "fixed_z1_near_free_gapless"],
        )
        self.assertIn("NOT_A_MASS_PREDICATE", result["A016"]["failure_domain"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
