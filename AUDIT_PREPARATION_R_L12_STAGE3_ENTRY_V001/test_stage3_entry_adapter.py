#!/usr/bin/env python3
"""Hostile nonphysical tests for the A20/A21/two-A22 adapter."""

from __future__ import annotations

import copy
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "stage3_entry_adapter.py"
SPEC = importlib.util.spec_from_file_location("stage3_entry_adapter_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
entry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = entry
SPEC.loader.exec_module(entry)


class Stage3EntryAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = entry.fixture_environment()
        (
            self.capture, self.digests, self.policy, self.observations,
        ) = self.fixture.__enter__()

    def tearDown(self) -> None:
        self.fixture.__exit__(None, None, None)

    def bundle(self):
        return self.capture, self.digests

    def records(self):
        return entry.build_all_records(
            self.capture, self.digests, self.capture.captured_epoch,
            policy=self.policy, observations=self.observations,
        )

    def schedule(self, capture=None):
        return entry.build_schedule(
            self.capture if capture is None else capture,
            self.digests, self.capture.captured_epoch, policy=self.policy,
        )

    def test_complete_fixture_reaches_two_authorizations(self) -> None:
        capture, digests = self.bundle()
        records = self.records()
        coordinator = entry.frozen_runtime().coordinator.DualLaunchCoordinator(
            self.policy, capture.captured_epoch,
        )
        coordinator.admit_schedule(records["schedule"])
        coordinator.admit_schedule_audit(records["schedule_audit"])
        coordinator.admit_authorization(records["hostile_authorization"])
        coordinator.admit_authorization(records["target_authorization"])
        self.assertEqual(coordinator.stage, "AUTHORIZATIONS_COMPLETE")
        self.assertNotEqual(
            entry.frozen_runtime().coordinator.record_sha256(
                records["target_authorization"],
            ),
            entry.frozen_runtime().coordinator.record_sha256(
                records["hostile_authorization"],
            ),
        )

    def test_stale_resource_capture_refuses(self) -> None:
        capture, digests = self.bundle()
        stale = entry.ResourceCapture(
            capture.captured_epoch - 301,
            capture.host_physical_memory_bytes,
            capture.available_memory_bytes,
            capture.workspace_free_disk_bytes,
            capture.workspace_filesystem_device,
            True, "NORMAL", True,
        )
        with self.assertRaises((
            entry.EntryRefusal, entry.frozen_runtime().coordinator.Refusal,
        )):
            entry.build_schedule(
                stale, digests, capture.captured_epoch, policy=self.policy,
            )

    def test_insufficient_memory_refuses(self) -> None:
        capture, digests = self.bundle()
        low = entry.ResourceCapture(
            capture.captured_epoch, 47_999_999_999,
            capture.available_memory_bytes, capture.workspace_free_disk_bytes,
            capture.workspace_filesystem_device, True, "NORMAL", True,
        )
        with self.assertRaises((
            entry.EntryRefusal, entry.frozen_runtime().coordinator.Refusal,
        )):
            entry.build_schedule(
                low, digests, capture.captured_epoch, policy=self.policy,
            )

    def test_insufficient_disk_refuses(self) -> None:
        capture, digests = self.bundle()
        low = entry.ResourceCapture(
            capture.captured_epoch, capture.host_physical_memory_bytes,
            capture.available_memory_bytes, 19_201_889_579,
            capture.workspace_filesystem_device, True, "NORMAL", True,
        )
        with self.assertRaises((
            entry.EntryRefusal, entry.frozen_runtime().coordinator.Refusal,
        )):
            entry.build_schedule(
                low, digests, capture.captured_epoch, policy=self.policy,
            )

    def test_wrong_memory_pressure_and_false_pass_refuse(self) -> None:
        capture, digests = self.bundle()
        for pressure, passes in (("WARNING", True), ("NORMAL", False)):
            mutant = entry.ResourceCapture(
                capture.captured_epoch, capture.host_physical_memory_bytes,
                capture.available_memory_bytes,
                capture.workspace_free_disk_bytes,
                capture.workspace_filesystem_device, True, pressure, passes,
            )
            with self.assertRaises((
                entry.EntryRefusal, entry.frozen_runtime().coordinator.Refusal,
            )):
                entry.build_schedule(
                    mutant, digests, capture.captured_epoch, policy=self.policy,
                )

    def test_swapped_role_path_refuses(self) -> None:
        capture, digests = self.bundle()
        schedule = self.schedule()
        mutant = copy.deepcopy(schedule)
        mutant["roles"]["target_v012"]["worker_executable_path"] = str(
            entry.HOSTILE_EXECUTABLE
        )
        coordinator = entry.frozen_runtime().coordinator.DualLaunchCoordinator(
            self.policy, capture.captured_epoch,
        )
        with self.assertRaises(entry.frozen_runtime().coordinator.Refusal):
            coordinator.admit_schedule(mutant)

    def test_swapped_authorization_hash_refuses_adapter_binding(self) -> None:
        capture, digests = self.bundle()
        records = self.records()
        mutant = copy.deepcopy(records["target_authorization"])
        mutant["consumer_sha256"] = digests.hostile_executable
        with self.assertRaisesRegex(entry.EntryRefusal, "input binding"):
            entry.validate_authorization_bindings(
                mutant, records["hostile_authorization"], digests,
            )

    def test_premature_authorization_refuses(self) -> None:
        capture, digests = self.bundle()
        schedule = self.schedule()
        coordinator = entry.frozen_runtime().coordinator.DualLaunchCoordinator(
            self.policy, capture.captured_epoch,
        )
        coordinator.admit_schedule(schedule)
        with self.assertRaisesRegex(entry.EntryRefusal, "premature"):
            entry.build_authorization("target_v012", coordinator, digests)

    def test_independent_audit_requires_observed_custody_and_absence(self) -> None:
        capture, digests = self.bundle()
        schedule = self.schedule()
        target_output = Path(self.policy.target.output)
        target_output.symlink_to(target_output.with_name("missing-target"))
        with self.assertRaises(Exception):
            entry.independent_schedule_audit(
                schedule, capture.captured_epoch,
                policy=self.policy, observations=self.observations,
            )
        target_output.unlink()

    def test_existing_destination_refuses_without_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            absent = root / "absent.json"
            present = root / "present.json"
            present.write_bytes(b"hostile-preexisting")
            with self.assertRaisesRegex(entry.EntryRefusal, "already present"):
                entry.require_absent((absent, present))
            self.assertEqual(present.read_bytes(), b"hostile-preexisting")
            self.assertFalse(absent.exists())

    def test_memory_pressure_parse_is_conservative(self) -> None:
        raw = (
            "The system has 51539607552 (3145728 pages with a page size of "
            "16384).\nSystem-wide memory free percentage: 70%\n"
        )
        total, available = entry.parse_memory_pressure(raw, 2_000_000_000)
        self.assertEqual(total, 51_539_607_552)
        self.assertEqual(available, total * 69 // 100)

    def test_memory_pressure_arithmetic_or_shape_refuses(self) -> None:
        for raw in (
            "The system has 100 (2 pages with a page size of 40).\n"
            "System-wide memory free percentage: 80%\n",
            "System-wide memory free percentage: 80%\n",
        ):
            with self.assertRaises(entry.EntryRefusal):
                entry.parse_memory_pressure(raw, 2_000_000_000)

    def test_owner_once_publication_refuses_existing_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve() / "record.json"
            payload = b'{"exact":true}\n'
            digest = entry.frozen_runtime().evidence._atomic_publish_once(
                str(output), payload, str(output),
            )
            self.assertEqual(digest, entry.hashlib.sha256(payload).hexdigest())
            metadata = os.stat(output, follow_symlinks=False)
            self.assertEqual(metadata.st_nlink, 1)
            self.assertEqual(metadata.st_mode & 0o222, 0)
            with self.assertRaises(Exception):
                entry.frozen_runtime().evidence._atomic_publish_once(
                    str(output), b"other\n", str(output),
                )
            self.assertEqual(output.read_bytes(), payload)

    def test_fixture_mode_creates_no_canonical_outputs(self) -> None:
        before = {path: os.path.lexists(path) for path in entry.OUTPUT_PATHS}
        self.records()
        after = {path: os.path.lexists(path) for path in entry.OUTPUT_PATHS}
        self.assertEqual(before, after)

    def test_launcher_direct_entry_refuses_without_stage3_guard(self) -> None:
        with self.assertRaisesRegex(
            entry.frozen_runtime().launcher.LaunchRefusal,
            "authenticated Stage-3 execution guard is absent",
        ):
            entry.frozen_runtime().launcher.execute()

    def test_guard_phase_order_and_fd_disk_custody(self) -> None:
        class Census:
            def __init__(self) -> None:
                self.calls = []

            def require_exact_names(self, destinations, present, label) -> None:
                self.calls.append((destinations, present, label))

            def filesystem_state(self):
                return (1234, 56_000_000_000)

            def close(self) -> None:
                pass

        census = Census()
        guard = entry.Stage3ExecutionGuard(census)
        with self.assertRaisesRegex(entry.EntryRefusal, "outside execution phase"):
            guard.disk_state()
        guard.verify_phase("initial")
        guard.verify_phase("pre_handshake")
        guard.verify_phase("pre_release")
        self.assertEqual(guard.disk_state(), (1234, 56_000_000_000))
        guard.verify_phase("final")
        self.assertEqual([call[2] for call in census.calls], [
            "Stage3 immediate initial name census",
            "Stage3 immediate pre_handshake name census",
            "Stage3 immediate pre_release name census",
            "Stage3 immediate final name census",
        ])
        with self.assertRaisesRegex(entry.EntryRefusal, "phase order"):
            guard.verify_phase("final")

    def test_guard_rejects_out_of_order_phase(self) -> None:
        class Census:
            def require_exact_names(self, *_args) -> None:
                raise AssertionError("census must not run after phase refusal")

        guard = entry.Stage3ExecutionGuard(Census())
        with self.assertRaisesRegex(entry.EntryRefusal, "phase order"):
            guard.verify_phase("pre_handshake")

    def test_destination_census_rejects_dangling_symlink_name(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage3_census_", dir=entry.HERE) as directory:
            parent = Path(directory).resolve() / "parent"
            parent.mkdir()
            destination = parent / "output.json"
            destination.symlink_to(parent / "missing")
            census = entry.RetainedDestinationCensus.open((destination,))
            try:
                with self.assertRaisesRegex(entry.EntryRefusal, "already present"):
                    census.require_absent((destination,), "hostile dangling alias")
            finally:
                census.close()

    def test_destination_census_rejects_parent_substitution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage3_parent_", dir=entry.HERE) as directory:
            base = Path(directory).resolve()
            parent = base / "parent"
            moved = base / "held-parent"
            parent.mkdir()
            census = entry.RetainedDestinationCensus.open((parent / "output.json",))
            parent.rename(moved)
            parent.mkdir()
            try:
                with self.assertRaisesRegex(entry.EntryRefusal, "parent changed"):
                    census.verify_parents()
                with self.assertRaisesRegex(entry.EntryRefusal, "parent changed"):
                    census.close()
            finally:
                parent.rmdir()
                moved.rename(parent)

    def test_source_freeze_names_complete_executed_closure(self) -> None:
        names = [name for name, _path in entry.TRANSITIVE_MODULE_ORDER]
        self.assertEqual(names, [
            "dual_launch_coordinator",
            "production_evidence_orchestrator",
            "independent_final_auditor",
            "production_dual_l12_launcher",
            "production_obligation_validators",
            "independent_a20_auditor",
        ])
        self.assertIn(entry.LAUNCHER_CANDIDATE, entry.TRANSITIVE_DEPENDENCY_SHA256)


if __name__ == "__main__":
    unittest.main(verbosity=2)
