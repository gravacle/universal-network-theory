#!/usr/bin/env python3
"""Focused tests for the non-destructive L10/L12 recognition packet."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import recognize_heldout_witness as recognition


class RecognitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = recognition.DEFAULT_ROOT
        cls.result = recognition.recognize(cls.root)
        cls.recorded = json.loads(recognition.DEFAULT_RESULT.read_text(encoding="utf-8"))

    def test_recorded_result_is_exact_recomputation(self) -> None:
        self.assertEqual(self.recorded, self.result)
        self.assertEqual(
            recognition.DEFAULT_RESULT.read_bytes(),
            recognition.canonical_bytes(self.recorded),
        )

    def test_atomic_hashes_are_pinned(self) -> None:
        self.assertEqual(
            recognition.sha256_file(self.root / recognition.TARGET_PATH),
            recognition.PINNED_INPUT_HASHES[recognition.TARGET_PATH],
        )
        self.assertEqual(
            recognition.sha256_file(self.root / recognition.HOSTILE_PATH),
            recognition.PINNED_INPUT_HASHES[recognition.HOSTILE_PATH],
        )

    def test_independent_numerical_agreement_is_resolved(self) -> None:
        by_length = {row["length"]: row for row in self.result["sizes"]}
        self.assertLess(by_length[10]["absolute_target_hostile_D_disagreement"], 1e-16)
        self.assertLess(by_length[12]["absolute_target_hostile_D_disagreement"], 1e-16)
        self.assertTrue(all(all(row["conditions"].values()) for row in by_length.values()))
        self.assertGreater(self.result["computational_evidence"]["two_sided_T_10_12"], 1.0)
        self.assertTrue(self.result["computational_evidence"]["recognized"])

    def test_tau_is_independently_recomputed(self) -> None:
        for row in self.result["sizes"]:
            self.assertEqual(
                row["tau_L"],
                max(1e-9, 50.0 * row["d_L"], 100.0 * row["r_L"]),
            )
            self.assertAlmostEqual(
                row["T_L"], abs(row["D_L_target"]) / row["tau_L"], places=12
            )

    def test_signed_persistence_fails_without_failing_recognition(self) -> None:
        self.assertFalse(self.result["secondary_signed_persistence"]["pass"])
        for row in self.result["sizes"]:
            self.assertLess(row["D_L_target"], 0.0)
            self.assertLess(row["D_L_hostile"], 0.0)
            self.assertFalse(row["persistence_pass"])
            self.assertLess(row["magnitude_fraction_of_D8"], 1.0)
        self.assertTrue(self.result["computational_evidence"]["recognized"])

    def test_timing_is_disclosed_but_not_a_numerical_input(self) -> None:
        timing = self.result["timing_custody"]
        self.assertEqual(timing["release_observation"]["observed_gap_seconds"], 10748)
        self.assertEqual(timing["release_observation"]["frozen_maximum_seconds"], 60)
        self.assertFalse(timing["release_observation"]["within_frozen_maximum"])
        self.assertFalse(
            self.result["computational_evidence"]
            ["deterministic_numerical_validity_affected_by_timing_gap"]
        )
        chronology = timing["chronology"]
        self.assertLess(
            chronology["hostile_scratch_birth_epoch_seconds"],
            chronology["hostile_atomic_output_birth_epoch_seconds"],
        )
        self.assertLess(
            chronology["hostile_scratch_birth_epoch_seconds"],
            chronology["target_atomic_output_birth_epoch_seconds"],
        )

    def test_strict_protocol_is_not_relabelled(self) -> None:
        strict = self.result["strict_protocol"]
        self.assertFalse(strict["formal_pass_claimed"])
        self.assertTrue(strict["release_skew_deviation_disclosed"])
        self.assertIn("NOT_CLAIMED_AS_FORMALLY_PASSED", strict["status"])

    def test_claim_ceiling_excludes_promotions(self) -> None:
        boundary = self.result["claim_boundary"]
        for marker in ("NO_ALL_L", "GATE", "RGRL", "ALPHA", "GEOMETRY", "GRAVITY"):
            self.assertIn(marker, boundary)


if __name__ == "__main__":
    unittest.main()
