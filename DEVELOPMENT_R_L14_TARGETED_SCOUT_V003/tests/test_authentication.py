#!/usr/bin/env python3

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from durable_evidence import EvidenceError
from merge_branches import merge


def branch_payload(branch):
    return {
        "schema": "L14_SCOUT_BRANCH_RESULT_V002",
        "length": 14,
        "branch": branch,
        "phase": "bridge",
        "computed_sectors": [4, 5, 6, 7],
        "sector_masses": {"4": "0.16", "5": "0.203", "6": "0.15", "7": "0.12", "8": "0.10", "9": "0.05"},
        "numerical_validation": {
            "all_actual_and_null_solvers_converged": True,
            "residual_l1_within_original_bound": True,
            "actual_norm_error_within_original_bound": True,
            "transport_number_drift_within_original_bound": True,
            "rough_sharp_agreement_within_original_bound": True,
        },
        "comparison_evidence": {
            "raw_metrics": {
                "reverse_support_probability": "0.75",
                "transport_node_residual_l1": "1e-13",
                "actual_norm_error": "1e-14",
                "transport_number_drift": "1e-15"
            },
            "predicate_thresholds": {
                "reverse_support_probability": {"comparison": "test"},
                "transport_node_residual_l1": "1e-10",
                "actual_norm_error": "1e-10",
                "transport_number_drift": "1e-10"
            }
        },
        "atoms": [
            {
                "atom_id": "A005",
                "q": 5,
                "density_interval": [[3, 16], [11, 56]],
                "geometry": {"resolved": True, "z": 1.0, "y": 1.0},
            }
        ],
    }


class AuthenticationTests(unittest.TestCase):
    def write(self, path, payload):
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_unresolved_solver_predicate_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = branch_payload("target")
            hostile = branch_payload("hostile")
            target["numerical_validation"]["all_actual_and_null_solvers_converged"] = False
            self.write(root / "target.json", target)
            self.write(root / "hostile.json", hostile)
            with self.assertRaises(EvidenceError):
                merge(root / "target.json", root / "hostile.json")

    def test_probability_mass_disagreement_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = branch_payload("target")
            hostile = branch_payload("hostile")
            hostile["sector_masses"]["5"] = "0.204"
            self.write(root / "target.json", target)
            self.write(root / "hostile.json", hostile)
            with self.assertRaises(EvidenceError):
                merge(root / "target.json", root / "hostile.json")

    def test_missing_raw_comparison_metric_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = branch_payload("target")
            hostile = branch_payload("hostile")
            del hostile["comparison_evidence"]["raw_metrics"]["actual_norm_error"]
            self.write(root / "target.json", target)
            self.write(root / "hostile.json", hostile)
            with self.assertRaises(EvidenceError):
                merge(root / "target.json", root / "hostile.json")


if __name__ == "__main__":
    unittest.main()
