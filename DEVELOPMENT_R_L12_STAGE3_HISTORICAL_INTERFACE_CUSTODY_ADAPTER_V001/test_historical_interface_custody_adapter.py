#!/usr/bin/env python3
"""Focused hostile tests for the development-only historical interface."""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import os
import stat
import sys
import tempfile
import types
import unittest
from pathlib import Path

import historical_interface_custody_adapter as adapter


class HistoricalInterfaceCustodyAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertFalse(adapter._PATCH_ACTIVE)

    def tearDown(self) -> None:
        self.assertFalse(adapter._PATCH_ACTIVE)

    def test_01_plan_pins_exact_disjoint_paths_and_hashes(self) -> None:
        before = adapter.evidence_state()
        result = adapter.plan()
        self.assertEqual(
            result["classification"], "MUTABLE_READINESS_ONLY_NOT_EXECUTION_AUTHORITY",
        )
        self.assertEqual(result["unchanged_hostile_source_count"], 12)
        self.assertEqual(
            result["unchanged_hostile_consumer_sha256"], adapter.CONSUMER_SHA256,
        )
        self.assertEqual(result["historical_target_sha256"], adapter.HISTORICAL_TARGET_SHA256)
        self.assertEqual(result["active_target_sha256"], adapter.ACTIVE_TARGET_SHA256)
        for name in adapter.TARGET_RELATIVE:
            self.assertEqual(result["historical_paths"][name], str(adapter.HISTORICAL_TARGET_PATHS[name]))
            self.assertEqual(result["active_paths"][name], str(adapter.ACTIVE_TARGET_PATHS[name]))
            self.assertNotEqual(result["historical_paths"][name], result["active_paths"][name])
        self.assertFalse(result["launch_available"])
        self.assertFalse(result["publication_available"])
        self.assertFalse(result["file_move_available"])
        self.assertFalse(result["physical_execution_available"])
        self.assertEqual(adapter.evidence_state(), before)

    def test_02_original_fails_and_adapter_restores_exact_capability(self) -> None:
        before = adapter.evidence_state()
        consumer = adapter.load_unchanged_hostile_consumer()
        _freeze, _audit, gate = adapter._hostile_gate_inputs(consumer)
        original = consumer.retain_build_authorization_inputs
        custody = consumer.AuthorityCustody()
        try:
            with self.assertRaisesRegex(consumer.Refusal, "target V012 freeze hash mismatch"):
                original(custody, gate)
        finally:
            custody.close()

        custody = consumer.AuthorityCustody()
        try:
            before_members = dict(vars(consumer))
            with adapter.historical_interface_scope(consumer) as capability:
                changed = {
                    name for name, value in before_members.items()
                    if getattr(consumer, name) is not value
                }
                self.assertEqual(changed, {"retain_build_authorization_inputs"})
                self.assertIs(consumer.retain_build_authorization_inputs, capability)
                capability(custody, gate)
                custody.verify_all()
                for path in adapter.HISTORICAL_TARGET_PATHS.values():
                    self.assertIn(path, custody.files)
                for path in adapter.ACTIVE_TARGET_PATHS.values():
                    self.assertNotIn(path, custody.files)
            self.assertIs(consumer.retain_build_authorization_inputs, original)
            with self.assertRaisesRegex(adapter.AdapterRefusal, "capability expired"):
                capability(custody, gate)
        finally:
            custody.close()
        self.assertEqual(adapter.evidence_state(), before)

    def test_03_self_test_has_no_evidence_or_source_byte_delta(self) -> None:
        before = adapter.evidence_state()
        source_before = hashlib.sha256(adapter.CONSUMER.read_bytes()).hexdigest()
        result = adapter.self_test()
        self.assertEqual(
            result["classification"], "PASS_MUTABLE_HISTORICAL_INTERFACE_READINESS",
        )
        self.assertEqual(result["patched_boundary_count"], 1)
        for name in ("launched", "published", "moved", "physical_execution"):
            self.assertFalse(result[name])
        self.assertEqual(hashlib.sha256(adapter.CONSUMER.read_bytes()).hexdigest(), source_before)
        self.assertEqual(source_before, adapter.CONSUMER_SHA256)
        self.assertEqual(adapter.evidence_state(), before)

    def test_04_nested_scope_and_runtime_tamper_refuse_closed(self) -> None:
        consumer = adapter.load_unchanged_hostile_consumer()
        with adapter.historical_interface_scope(consumer):
            with self.assertRaisesRegex(adapter.AdapterRefusal, "already active"):
                with adapter.historical_interface_scope(consumer):
                    pass
        original_read = consumer.read_authority
        consumer.read_authority = lambda *_args, **_kwargs: None
        try:
            with self.assertRaisesRegex(adapter.AdapterRefusal, "runtime changed"):
                with adapter.historical_interface_scope(consumer):
                    pass
        finally:
            consumer.read_authority = original_read

    def test_05_forged_module_identity_refuses_even_with_copied_members(self) -> None:
        consumer = adapter.load_unchanged_hostile_consumer()
        forged = types.ModuleType("forged_hostile_consumer")
        forged.__file__ = str(adapter.CONSUMER)
        for name in (
            "read_authority", "AuthorityCustody", "validate_hostile_prepayload_audit",
            "validate_hostile_build_authorization", "retain_build_authorization_inputs",
        ):
            setattr(forged, name, getattr(consumer, name))
        with self.assertRaisesRegex(adapter.AdapterRefusal, "exact unchanged hostile consumer"):
            with adapter.historical_interface_scope(forged):
                pass

    def test_06_active_path_substitution_refuses(self) -> None:
        with self.assertRaisesRegex(adapter.AdapterRefusal, "active-path substitution refused"):
            adapter._validate_path_partition(
                dict(adapter.ACTIVE_TARGET_PATHS), dict(adapter.ACTIVE_TARGET_PATHS),
            )
        swapped = dict(adapter.HISTORICAL_TARGET_PATHS)
        swapped["freeze"] = adapter.ACTIVE_TARGET_PATHS["freeze"]
        with self.assertRaisesRegex(adapter.AdapterRefusal, "active-path substitution refused"):
            adapter._validate_path_partition(swapped, dict(adapter.ACTIVE_TARGET_PATHS))

    def test_07_mutated_gate_or_interface_refuses(self) -> None:
        consumer = adapter.load_unchanged_hostile_consumer()
        _freeze, _audit, gate = adapter._hostile_gate_inputs(consumer)
        mutated = copy.deepcopy(gate)
        mutated["target_v012_interface"]["freeze_sha256"] = adapter.ACTIVE_TARGET_SHA256["freeze"]
        custody = consumer.AuthorityCustody()
        try:
            with adapter.historical_interface_scope(consumer) as capability:
                with self.assertRaisesRegex(adapter.AdapterRefusal, "exact historical build gate"):
                    capability(custody, mutated)
        finally:
            custody.close()

    def test_08_owner_once_reader_rejects_hash_permissions_links_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="adapter-test-", dir=adapter.HERE) as directory:
            root = Path(directory)
            path = root / "record.json"
            path.write_bytes(b"{}\n")
            path.chmod(0o444)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(adapter._read_owner_once(path, digest, "test record"), b"{}\n")
            with self.assertRaisesRegex(adapter.AdapterRefusal, "identity or digest changed"):
                adapter._read_owner_once(path, "0" * 64, "test record")

            path.chmod(0o644)
            with self.assertRaisesRegex(adapter.AdapterRefusal, "not immutable owner-once"):
                adapter._read_owner_once(path, digest, "test record")
            path.chmod(0o444)

            hardlink = root / "record-hardlink.json"
            os.link(path, hardlink)
            with self.assertRaisesRegex(adapter.AdapterRefusal, "not immutable owner-once"):
                adapter._read_owner_once(path, digest, "test record")
            hardlink.unlink()

            symlink = root / "record-symlink.json"
            symlink.symlink_to(path.name)
            with self.assertRaises(adapter.AdapterRefusal):
                adapter._read_owner_once(symlink, digest, "test record")

    def test_09_cli_exposes_only_plan_and_self_test(self) -> None:
        original_argv = sys.argv
        try:
            for forbidden in ("launch", "publish", "move", "execute"):
                sys.argv = [str(adapter.__file__), forbidden]
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(adapter.main(), 2)
                self.assertIn("exposes only plan or self-test", stderr.getvalue())
            for allowed in ("plan", "self-test"):
                sys.argv = [str(adapter.__file__), allowed]
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    self.assertEqual(adapter.main(), 0)
                self.assertIn('"schema"', stdout.getvalue())
        finally:
            sys.argv = original_argv


if __name__ == "__main__":
    unittest.main(verbosity=2)
