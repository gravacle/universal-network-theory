#!/usr/bin/env python3
"""Non-physical tests for the Stage6R1 source-freeze repair."""

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
        "stage6r1_continuation_under_test", HERE / "continue_stage6r1.py"
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class Stage6R1Tests(unittest.TestCase):
    def test_01_predecessor_failure_is_reproduced(self) -> None:
        old = PACKET / "SOURCE_FREEZE.json"
        with self.assertRaisesRegex(control.Refusal, "file census mismatch"):
            control.validate_source_freeze(old, control.sha256_file(old))

    def test_02_repaired_freeze_passes_unchanged_validator(self) -> None:
        repaired = HERE / "SOURCE_FREEZE_STAGE6R1.json"
        value = control.validate_source_freeze(repaired, control.sha256_file(repaired))
        self.assertEqual(set(value["files"]), {
            "blind_adjudication_entrypoint.py",
            "blind_contract_control.py",
            "blind_index_publisher.py",
            "blind_interval_worker.py",
            "contract_common.py",
            "METHODOLOGY.md",
            "test_stage6_compatibility.py",
        })

    def test_03_failed_and_repaired_allocations_are_isolated(self) -> None:
        continuation = load_continuation()
        self.assertNotEqual(continuation.FAILED_BLIND_RUN, continuation.BLIND_RUN)
        self.assertNotEqual(continuation.BLIND_RUN, continuation.TARGET_RUN)
        self.assertTrue(continuation.FAILED_PLAN.is_file())
        failed_rows = continuation.FAILED_BLIND_RUN / "RAW"
        self.assertTrue(failed_rows.is_dir())
        self.assertEqual(list(failed_rows.iterdir()), [])

    def test_04_no_stage7_execution_path(self) -> None:
        source = (HERE / "continue_stage6r1.py").read_text(encoding="utf-8")
        self.assertNotIn("stage7(", source.lower())
        self.assertIn('"stage7_started": False', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
