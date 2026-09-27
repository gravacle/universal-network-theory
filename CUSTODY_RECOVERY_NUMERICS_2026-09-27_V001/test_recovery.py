#!/usr/bin/env python3
"""Bounded recovery/migration controls; no state evolution or persistent outputs."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import restore_l8_manifest as restore
import validate_l8_relocated as adapter

class RecoveryTests(unittest.TestCase):
    def fixture(self, root):
        for relative in (restore.FREEZE, restore.COPY):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((restore.ROOT / relative).read_bytes())

    def test_clean_checkout_missing_runtime_manifest_restored_and_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(restore.restore(root)["status"], "RESTORED_EXACT_FROZEN_INPUT")
            self.assertEqual(restore.restore(root)["status"], "EXISTING_IDENTICAL_PRESERVED")
            self.assertEqual((root / restore.MANIFEST).read_bytes(), (root / restore.COPY).read_bytes())

    def test_conflicting_runtime_manifest_refused_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            destination = root / restore.MANIFEST
            destination.parent.mkdir(parents=True)
            destination.write_bytes(b"conflict")
            with self.assertRaises(ValueError):
                restore.restore(root)
            self.assertEqual(destination.read_bytes(), b"conflict")

    def test_corrupt_tracked_copy_refused_before_creating_runtime_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / restore.COPY).write_bytes(b"corrupt")
            with self.assertRaises(ValueError):
                restore.restore(root)
            self.assertFalse((root / restore.MANIFEST).exists())

    def test_symlink_parent_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "outside").mkdir()
            (root / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012").symlink_to(root / "outside")
            with self.assertRaises(ValueError):
                restore.restore(root)

    def test_exact_path_map_refuses_traversal_wrong_prefix_unknown_q(self):
        mapping = adapter.relocation_map(restore.ROOT)
        for value in (adapter.PREFIX + "../x", "/tmp/q_00.npy", adapter.PREFIX + "q_99.npy"):
            with self.assertRaises(ValueError):
                adapter.mapped_path(value, mapping)
        self.assertEqual(len(mapping), 8)

    def test_historical_result_and_controls_with_adapter(self):
        self.assertGreater(adapter.run()["checks"], 80)

def historical_suite():
    path = restore.ROOT / "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/test_validate_result.py"
    restore.authenticated_bytes(path, "7cc8d4d24dd06ac42f98a9078e69a7bb23ac446817dc2339a189f89b1892e055")
    # Resolve the frozen test's import to the authenticated adapted module.
    import sys
    previous = sys.modules.get("validate_result")
    sys.modules["validate_result"] = adapter.load_validator()
    try:
        spec = importlib.util.spec_from_file_location("unt_frozen_l8_curvature_tests", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if previous is None:
            del sys.modules["validate_result"]
        else:
            sys.modules["validate_result"] = previous
    return unittest.defaultTestLoader.loadTestsFromModule(module)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RecoveryTests)
    suite.addTests(historical_suite())
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
