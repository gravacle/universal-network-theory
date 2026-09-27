#!/usr/bin/env python3
"""Small exact-payload recovery tests; never copy the larger state shards."""
from pathlib import Path
import tempfile
import unittest

import restore_progression_inputs as target

class ProgressionRecoveryTests(unittest.TestCase):
    def fixture(self, root):
        pins = target.parse_pins(target.ROOT)
        manifests, indexes = target.manifests_and_indexes(target.ROOT, pins)
        routes = [target.MODULE] + [record["included"] for record in manifests + indexes]
        for relative in routes:
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((target.ROOT / relative).read_bytes())
        return manifests, indexes

    def test_complete_live_preflight_reads_all_33(self):
        result = target.run(target.ROOT, preflight_only=True)
        self.assertEqual(result["status"], "PASS_ALL_33_PROGRESSION_INPUTS_AUTHENTICATED")
        self.assertEqual(len(result["verified"]), 33)
        self.assertFalse(result["actions"])

    def test_small_inputs_restore_but_absent_external_shards_remain_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifests, indexes = self.fixture(root)
            result = target.run(root)
            self.assertEqual(len(result["actions"]), 22)
            self.assertEqual(len(result["missing"]), 11)  # ten shards + source extractor
            self.assertEqual(result["status"], "INCOMPLETE_MISSING_EXTERNAL_INPUTS")
            second = target.run(root)
            self.assertTrue(all(row["action"] == "EXISTING_IDENTICAL_PRESERVED" for row in second["actions"]))
            for record in manifests + indexes:
                self.assertEqual((root / record["path"]).read_bytes(),
                                 (root / record["included"]).read_bytes())

    def test_corrupt_index_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, indexes = self.fixture(root)
            (root / indexes[0]["included"]).write_bytes(b"bad")
            with self.assertRaises(ValueError):
                target.run(root)

    def test_conflicting_runtime_input_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifests, _ = self.fixture(root)
            destination = root / manifests[0]["path"]
            destination.parent.mkdir(parents=True)
            destination.write_bytes(b"conflict")
            with self.assertRaises(ValueError):
                target.run(root)
            self.assertEqual(destination.read_bytes(), b"conflict")

    def test_source_module_tamper_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / target.MODULE).write_bytes(b"pass\n")
            with self.assertRaises(ValueError):
                target.run(root)

    def test_runtime_symlink_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "outside").mkdir()
            (root / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012").symlink_to(root / "outside")
            with self.assertRaises(ValueError):
                target.run(root)

if __name__ == "__main__":
    unittest.main(verbosity=2)
