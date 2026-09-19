#!/usr/bin/env python3

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().with_name("arger_gate.py")
SPEC = importlib.util.spec_from_file_location("arger_gate", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load arger_gate.py")
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def check(name: str, condition: bool) -> None:
    """Give the repository proof gate a named, executable assertion."""
    if not condition:
        raise AssertionError(name)


class ArgerGateEvidenceTest(unittest.TestCase):
    def test_native_inputs(self) -> None:
        result = gate.build_evidence()
        self.assertEqual(result["schema"], "WAC_ARGER_GATE_EVIDENCE_V001")
        block = result["record_block"]
        self.assertTrue(block["all_sizes_majority"])
        self.assertTrue(block["all_sectors_positive_finite_visibility"])
        self.assertEqual(block["minimum_R_low"], "0.4280947078156539")
        self.assertEqual(block["minimum_w_star"], "0.5")
        self.assertEqual(block["masses_by_L"]["12"], "0.56956498393327842")
        self.assertEqual(block["l12_majority_margin"], "0.06956498393327842")
        self.assertEqual(len(block["unique_sectors"]), 13)
        check(
            "ARGER-GATE-1 exact bounded membership and majority mass at L4--L12",
            block["all_sizes_majority"]
            and block["all_sectors_positive_finite_visibility"]
            and len(block["unique_sectors"]) == 13,
        )

    def test_adopted_gate(self) -> None:
        result = gate.build_evidence()
        decision = result["gate"]
        self.assertEqual(decision["name"], "ARGER Gate 1")
        self.assertEqual(decision["membership"], "PASS")
        self.assertEqual(decision["majority"], "PASS")
        self.assertEqual(decision["visibility"], "PASS")
        self.assertEqual(decision["finite_gft_z1"], "PASS")
        check(
            "ARGER-GATE-1 finite discrete GFT z=1 Gate passes",
            decision == {
                "id": "ARGER-GATE-1",
                "name": "ARGER Gate 1",
                "membership": "PASS",
                "majority": "PASS",
                "visibility": "PASS",
                "finite_gft_z1": "PASS",
            },
        )
        self.assertEqual(
            result["separate_claims"]["premise_free_uniform_all_L_z1"],
            "OPEN_STRONGER_RESULT_NOT_GATE_REQUIREMENT",
        )


if __name__ == "__main__":
    unittest.main()
