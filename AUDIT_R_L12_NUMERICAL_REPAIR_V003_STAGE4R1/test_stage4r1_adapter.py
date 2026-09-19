#!/usr/bin/env python3
"""Focused regression tests for the Stage4R1 schema projection."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ADAPTER = HERE / "adjudicate_stage4r1.py"
ROOT = HERE.parent


def load_adapter():
    specification = importlib.util.spec_from_file_location("stage4r1_adapter", ADAPTER)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class Stage4R1ProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.adapter = load_adapter()

    def test_removes_only_redundant_dimension(self) -> None:
        source = {"dimension": 17, "full_dimension": 17, "rows": [1, 2]}
        projected = self.adapter.remove_redundant_dimension(source)
        self.assertNotIn("dimension", projected)
        self.assertEqual(projected["full_dimension"], 17)
        self.assertEqual(projected["rows"], [1, 2])
        self.assertEqual(source["dimension"], 17)

    def test_rejects_dimension_mismatch(self) -> None:
        with self.assertRaisesRegex(
            self.adapter.Stage4R1Refusal, "dimension/full_dimension identity"
        ):
            self.adapter.remove_redundant_dimension({
                "dimension": 17,
                "full_dimension": 18,
            })

    def test_rejects_existing_manifest_adapter(self) -> None:
        with self.assertRaisesRegex(
            self.adapter.Stage4R1Refusal, "manifest_adapter must be absent"
        ):
            self.adapter.remove_redundant_dimension({
                "dimension": 17,
                "full_dimension": 17,
                "manifest_adapter": {},
            })

    def test_real_hostile_projection_is_predecessor_compatible(self) -> None:
        v003 = self.adapter.load_module(
            self.adapter.V003_PATH, "frozen_v003_stage4_projection_test"
        )
        base = v003.load_base()
        freeze = v003.verify_freeze(self.adapter.sha256(self.adapter.V003_FREEZE), base)
        history = json.loads(self.adapter.HOSTILE_HISTORY.read_text())
        projected = self.adapter.remove_redundant_dimension(
            v003.project_hostile(history, base, freeze)
        )
        self.assertNotIn("dimension", projected)
        self.assertNotIn("manifest_adapter", projected)
        self.assertEqual(projected["full_dimension"], history["dimension"])
        self.assertEqual(projected["rows"], history["rows"])
        self.assertEqual(projected["comparison"], history["comparison"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
