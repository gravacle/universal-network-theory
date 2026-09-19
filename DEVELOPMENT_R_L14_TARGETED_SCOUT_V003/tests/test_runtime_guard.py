#!/usr/bin/env python3

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "aws" / "runtime_guard.py"
spec = importlib.util.spec_from_file_location("l14_runtime_guard", str(PATH))
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class RuntimeGuardTests(unittest.TestCase):
    def test_minutes_accumulate_across_boot_ids_without_double_counting(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(module.record_minutes_through(root, "boot-a", 1), 1)
            self.assertEqual(module.record_minutes_through(root, "boot-a", 1), 1)
            self.assertEqual(module.record_minutes_through(root, "boot-a", 3), 3)
            self.assertEqual(module.record_minutes_through(root, "boot-b", 1), 4)

    def test_timer_gap_cannot_undercount_elapsed_minutes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(module.record_minutes_through(root, "boot-a", 0), 0)
            self.assertEqual(module.record_minutes_through(root, "boot-a", 5), 5)
            self.assertEqual(
                sorted(path.name for path in root.glob("*.json")),
                ["boot-a__{:08d}.json".format(index) for index in range(1, 6)],
            )

    def test_runtime_threshold_is_advisory_only(self):
        self.assertEqual(module.decide_action(834, 835), "CONTINUE")
        self.assertEqual(module.decide_action(835, 835), "ADVISORY_CONTINUE")
        self.assertEqual(module.decide_action(2_000, 835), "ADVISORY_CONTINUE")

    def test_advisory_is_durable_and_owner_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = module.record_advisory(root, 835, 835)
            self.assertEqual(destination, module.record_advisory(root, 900, 835))
            payload = json.loads(destination.read_text(encoding="utf-8"))
            self.assertEqual(payload["classification"], "ADVISORY_ONLY__EXECUTION_CONTINUES")
            self.assertEqual(payload["first_observed_consumed_minutes"], 835)
            self.assertEqual(len(list(root.glob("RUNTIME_ADVISORY_*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
