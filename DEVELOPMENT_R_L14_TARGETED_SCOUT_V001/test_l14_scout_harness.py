#!/usr/bin/env python3
"""Gateway tests for the L14 scout early-stop decision."""

from __future__ import annotations

import tempfile
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from l14_scout_harness import (
    Atom,
    Geometry,
    PhaseResult,
    evaluate_phase2,
    owner_once_json,
)


PASS = Geometry(True, Decimal("1.0"), Decimal("1.0"))
FAIL = Geometry(True, Decimal("1.2"), Decimal("1.0"))


def atom(atom_id: str, q: int, left: Fraction, right: Fraction, passes: bool = True) -> Atom:
    geometry = PASS if passes else FAIL
    return Atom(atom_id, q, (left, right), geometry, geometry)


def phase(atoms, masses) -> PhaseResult:
    return PhaseResult(
        phase="bridge",
        sectors=(4, 5, 6, 7),
        masses={q: Decimal(value) for q, value in masses.items()},
        atoms=tuple(atoms),
        source_path=Path("synthetic-phase1.json"),
        source_sha256="0" * 64,
    )


def complete_bridge_atoms(q5_passes: bool = True):
    return [
        atom("B04", 4, Fraction(1, 8), Fraction(3, 16)),
        atom("B05", 5, Fraction(3, 16), Fraction(11, 56), q5_passes),
        atom("B06", 6, Fraction(11, 56), Fraction(11, 48)),
        atom("B07", 7, Fraction(11, 48), Fraction(1, 4)),
    ]


class GateTests(unittest.TestCase):
    def test_bridge_and_optimistic_bound_authorize_phase3(self):
        observed = phase(
            complete_bridge_atoms(),
            {4: "0.05", 5: "0.14", 6: "0.13", 7: "0.03", 8: "0.10", 9: "0.05"},
        )
        decision = evaluate_phase2(observed)
        self.assertTrue(decision.proceed)
        self.assertTrue(decision.q5_has_passing_atom)
        self.assertTrue(decision.q6_has_passing_atom)
        self.assertTrue(decision.bridge_support_contiguously_covered)
        self.assertEqual(decision.phase1_passing_mass, Decimal("0.35"))
        self.assertEqual(decision.optimistic_total_upper_bound, Decimal("0.50"))

    def test_literal_q5_sterility_halts_before_phase3(self):
        observed = phase(
            complete_bridge_atoms(q5_passes=False),
            {4: "0.10", 5: "0.15", 6: "0.15", 7: "0.10", 8: "0.10", 9: "0.05"},
        )
        decision = evaluate_phase2(observed)
        self.assertFalse(decision.proceed)
        self.assertIn("L14_Q5_STERILE", decision.reasons)
        self.assertIn("NO_CONTIGUOUS_COVERAGE_OF_L12_Q5_DENSITY_SUPPORT", decision.reasons)

    def test_q6_density_core_sterility_halts_even_if_q5_passes(self):
        atoms = complete_bridge_atoms()
        atoms[2] = atom("B06", 6, Fraction(11, 56), Fraction(11, 48), False)
        observed = phase(
            atoms,
            {4: "0.10", 5: "0.15", 6: "0.15", 7: "0.10", 8: "0.10", 9: "0.05"},
        )
        decision = evaluate_phase2(observed)
        self.assertFalse(decision.proceed)
        self.assertIn("L12_Q5_DENSITY_CORE_STERILE_AT_L14_Q6", decision.reasons)

    def test_mathematical_upper_bound_halts(self):
        observed = phase(
            complete_bridge_atoms(),
            {4: "0.02", 5: "0.08", 6: "0.08", 7: "0.02", 8: "0.04", 9: "0.01"},
        )
        decision = evaluate_phase2(observed)
        self.assertFalse(decision.proceed)
        self.assertEqual(decision.optimistic_total_upper_bound, Decimal("0.25"))
        self.assertIn("Q8_Q9_CANNOT_REACH_THRESHOLD_EVEN_IF_BOTH_PASS", decision.reasons)

    def test_owner_once_evidence_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            owner_once_json(path, {"value": 1})
            with self.assertRaises(FileExistsError):
                owner_once_json(path, {"value": 2})


if __name__ == "__main__":
    unittest.main(verbosity=2)
