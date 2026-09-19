#!/usr/bin/env python3
"""Non-physical allocation tests for Stage6R2."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKET = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001"
sys.path.insert(0, str(PACKET))

import blind_contract_control as control  # noqa: E402


def load_continuation():
    specification = importlib.util.spec_from_file_location(
        "stage6r2_continuation_under_test", HERE / "continue_stage6r2.py"
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class Stage6R2Tests(unittest.TestCase):
    def test_01_pre_output_source_freeze_remains_valid(self) -> None:
        continuation = load_continuation()
        control.validate_source_freeze(
            continuation.SOURCE_FREEZE,
            control.sha256_file(continuation.SOURCE_FREEZE),
        )

    def test_02_stage6r1_failure_census_is_preserved(self) -> None:
        continuation = load_continuation()
        rows = sorted((continuation.FAILED_R1_BLIND_RUN / "RAW").glob("*.json"))
        credentials = sorted(
            (continuation.FAILED_R1_BLIND_RUN / "AUTHORIZATION").glob("*.json")
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(credentials), 4)
        self.assertFalse(
            (continuation.FAILED_R1_BLIND_RUN / "SPECTRUM_INDEX.json").exists()
        )

    def test_03_stage6r2_paths_are_fresh_and_isolated(self) -> None:
        continuation = load_continuation()
        self.assertNotEqual(continuation.FAILED_R1_BLIND_RUN, continuation.BLIND_RUN)
        self.assertNotEqual(continuation.BLIND_RUN, continuation.TARGET_RUN)
        self.assertFalse(continuation.BLIND_RUN.exists())
        self.assertFalse(continuation.TARGET_RUN.exists())
        self.assertFalse(continuation.FINAL_RESULT.exists())

    def test_04_no_stage7_execution_path(self) -> None:
        source = (HERE / "continue_stage6r2.py").read_text(encoding="utf-8")
        self.assertNotIn("stage7(", source.lower())
        self.assertIn('"stage7_started": False', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)

