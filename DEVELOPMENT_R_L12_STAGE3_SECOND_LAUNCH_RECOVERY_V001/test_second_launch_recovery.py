#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import os
import tempfile
import types
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "second_launch_recovery.py"
SPEC = importlib.util.spec_from_file_location("second_launch_recovery_under_test", SOURCE)
assert SPEC is not None and SPEC.loader is not None
recovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recovery)


class SecondLaunchRecoveryTests(unittest.TestCase):
    def test_exact_scope_and_atomic_shared_retirement(self) -> None:
        self.assertEqual(len(recovery.STALE), 14)
        self.assertEqual(len(set(recovery.STALE)), 14)
        shared = str(recovery.SHARED.relative_to(recovery.ROOT))
        self.assertIn(shared, recovery.STALE)
        self.assertFalse(any(path.startswith(shared + "/") for path in recovery.STALE))

    def test_exact_nine_absences(self) -> None:
        self.assertEqual(len(recovery.ABSENT), 9)
        self.assertEqual(len(set(recovery.ABSENT)), 9)
        recovery.assert_absent()

    def test_successor_is_only_exact_helper(self) -> None:
        new = recovery.successor_bytes()
        old = recovery.predecessor_path(
            str(recovery.CONSUMER.relative_to(recovery.ROOT))
        ).read_bytes()
        self.assertEqual(len(new) - len(old), 91)
        self.assertEqual(new.count(recovery.HELPER_BYTES), 1)
        self.assertEqual(hashlib.sha256(new).hexdigest(), recovery.NEW_CONSUMER_SHA256)

    def test_candidate_chain_exact(self) -> None:
        records = recovery.candidates()
        observed = {
            key: recovery.digest_record(records[key]) for key in
            ("freeze", "preflight", "prepayload", "build_gate", "postbuild", "l10_authorization")
        }
        observed["manifests"] = {
            length: recovery.digest_record(record)
            for length, record in records["manifests"].items()
        }
        self.assertEqual(observed, recovery.EXPECTED)

    def test_full_dry_run_does_not_mutate(self) -> None:
        watched = [recovery.ROOT / path for path in recovery.STALE]
        before = [(os.lstat(path).st_ino, os.lstat(path).st_size) for path in watched]
        result = recovery.dry_run()
        after = [(os.lstat(path).st_ino, os.lstat(path).st_size) for path in watched]
        self.assertEqual(before, after)
        self.assertEqual(result["authenticated_predecessor_entries"], 14)
        self.assertEqual(result["authenticated_required_absences"], 9)
        self.assertFalse(result["l12_launched"])

    def test_live_refuses_without_exact_authorization_before_mutation(self) -> None:
        watched = [recovery.ROOT / path for path in recovery.STALE]
        before = [(os.lstat(path).st_ino, os.lstat(path).st_size) for path in watched]
        with self.assertRaisesRegex(recovery.Refusal, "exact live authorization"):
            recovery.execute_live(None)
        after = [(os.lstat(path).st_ino, os.lstat(path).st_size) for path in watched]
        self.assertEqual(before, after)

    def test_source_contains_no_l12_execute_or_launcher_dispatch(self) -> None:
        raw = SOURCE.read_text(encoding="utf-8")
        self.assertIn('str(CONSUMER), "execute", "--length", "10"', raw)
        self.assertNotIn('str(CONSUMER), "execute", "--length", "12"', raw)
        self.assertNotIn("production_dual_l12_launcher.py", raw)

    def test_receipt_selects_retired_predecessor_over_identical_successor(self) -> None:
        saved = recovery.ROOT, recovery.CUSTODY, recovery.RECEIPT, recovery.STALE
        try:
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                custody = root / "custody"
                logical = "packet/workspace.bin"
                active = root / logical
                retired = custody / logical
                active.parent.mkdir(parents=True)
                retired.parent.mkdir(parents=True)
                active.write_bytes(b"identical successor and predecessor bytes")
                retired.write_bytes(active.read_bytes())
                active.chmod(0o444)
                retired.chmod(0o444)
                digest = hashlib.sha256(active.read_bytes()).hexdigest()
                receipt = custody / "receipt.json"
                receipt.write_bytes(b"{}\n")
                receipt.chmod(0o444)
                recovery.ROOT = root
                recovery.CUSTODY = custody
                recovery.RECEIPT = receipt
                recovery.STALE = {logical: ("file", digest)}
                self.assertEqual(recovery.predecessor_path(logical), retired)
        finally:
            recovery.ROOT, recovery.CUSTODY, recovery.RECEIPT, recovery.STALE = saved

    def test_live_source_enforces_review_blockers(self) -> None:
        raw = SOURCE.read_text(encoding="utf-8")
        self.assertIn("sys.modules[name] = module", raw)
        self.assertIn("context = consumer.CacheContext", raw)
        self.assertIn("validate_l10_history(history_path, consumer)", raw)
        self.assertGreaterEqual(raw.count("assert_l12_authorizations_absent()"), 2)
        self.assertIn("preserved pre-existing successor L10 execution requires adjudication", raw)

    def test_forged_preloaded_successor_module_is_refused(self) -> None:
        name = "forged_successor_module_review"
        forged = types.ModuleType(name)
        forged.__authenticated_sha256__ = recovery.NEW_CONSUMER_SHA256
        sys.modules[name] = forged
        try:
            with self.assertRaisesRegex(recovery.Refusal, "module name is occupied"):
                recovery.load_successor_module(name, recovery.successor_bytes())
        finally:
            sys.modules.pop(name, None)


if __name__ == "__main__":
    unittest.main()
