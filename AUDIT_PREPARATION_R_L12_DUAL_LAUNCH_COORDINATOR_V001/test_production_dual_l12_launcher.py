#!/usr/bin/env python3
"""Bounded non-physics tests for the executable dual-L12 launcher."""

from __future__ import annotations

import os
import socket
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import production_dual_l12_launcher as launcher
from dual_launch_coordinator import DualLaunchCoordinator, Refusal
from synthetic_fixtures import fresh_bundle, valid_coordinator_through


class ProductionLauncherTests(unittest.TestCase):
    def test_kernel_token_and_live_rss_bind_this_process(self):
        token = launcher.process_start_token(os.getpid())
        self.assertRegex(token, r"^[0-9a-f]{64}$")
        self.assertGreater(launcher.live_rss(os.getpid(), token), 0)
        with self.assertRaises(launcher.LaunchRefusal):
            launcher.live_rss(os.getpid(), "0" * 64)

    def test_wire_parser_requires_one_canonical_bounded_record(self):
        left, right = socket.socketpair()
        self.addCleanup(left.close)
        self.addCleanup(right.close)
        left.settimeout(1)
        right.sendall(b'{"a":1}\n')
        record, raw = launcher.receive_frame(left, "fixture")
        self.assertEqual(record, {"a": 1})
        self.assertEqual(raw, b'{"a":1}\n')
        with self.assertRaises(launcher.LaunchRefusal):
            launcher._strict_frame(b'{"a":1,"a":2}\n', "duplicate")
        with self.assertRaises(launcher.LaunchRefusal):
            launcher._strict_frame(b'{ "a":1}\n', "noncanonical")

    def test_record_builders_are_accepted_by_exact_coordinator(self):
        bundle = fresh_bundle()
        coordinator = valid_coordinator_through("hostile_authorization")
        with patch.object(launcher.time, "time", return_value=1_900_000_110):
            handshake = launcher.build_handshake(coordinator, bundle["handshake"]["workers"])
        coordinator.commit_handshake(handshake)
        release_epochs = {"target_v012": 1_900_000_111, "hostile_v004r4": 1_900_000_112}
        release = launcher.build_release(coordinator, release_epochs)
        decision = coordinator.release_workers(release)
        self.assertEqual(decision.record_sha256, coordinator.accepted_sha256("release"))

    def test_release_builder_type_and_hash_mutants_refuse(self):
        bundle = fresh_bundle()
        coordinator = valid_coordinator_through("handshake")
        release = launcher.build_release(
            coordinator,
            {"target_v012": 1_900_000_111, "hostile_v004r4": 1_900_000_112},
        )
        for mutant in (
            {**deepcopy(release), "observed_launch_skew_seconds": 1.0},
            {**deepcopy(release), "handshake_sha256": "0" * 64},
        ):
            with self.assertRaises(Refusal):
                coordinator.release_workers(mutant)

    def test_worker_argv_is_exact_and_role_bounded(self):
        target = launcher._worker_argv("target_v012", 9, "1" * 64, "target-id", "2" * 64)
        hostile = launcher._worker_argv("hostile_v004r4", 10, "3" * 64, "hostile-id", "2" * 64)
        self.assertEqual(target[1], str(launcher.TARGET_EXECUTABLE))
        self.assertIn(str(launcher.TARGET_CACHE_ROOT), target)
        self.assertEqual(hostile[1], str(launcher.HOSTILE_EXECUTABLE))
        self.assertNotIn("--cache-root", hostile)
        self.assertNotEqual(target[-1], hostile[-1])

    def test_stable_input_refuses_hardlinks_file_swap_and_parent_swap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            parent = root / "authority"
            parent.mkdir()
            path = parent / "record.json"
            path.write_bytes(b'{"a":1}\n')
            path.chmod(0o444)
            with patch.object(launcher, "ROOT", root):
                retained = launcher.StableInput.open("fixture", path, json_record=True)
                path.chmod(0o644)
                path.unlink()
                path.write_bytes(b'{"a":2}\n')
                path.chmod(0o444)
                with self.assertRaises(launcher.LaunchRefusal):
                    retained.verify()
                retained.close()

                hardlink = parent / "hardlink.json"
                os.link(path, hardlink)
                with self.assertRaises(launcher.LaunchRefusal):
                    launcher.StableInput.open("hardlink", path, json_record=True)
                hardlink.unlink()

                retained = launcher.StableInput.open("parent", path, json_record=True)
                moved = root / "moved"
                parent.rename(moved)
                parent.mkdir()
                replacement = parent / path.name
                replacement.write_bytes(b'{"a":2}\n')
                replacement.chmod(0o444)
                with self.assertRaises(launcher.LaunchRefusal):
                    retained.verify()
                retained.close()

    def test_live_sampling_refuses_process_exit_rss_and_disk_limits(self):
        ready = {
            "process_id": 7,
            "process_start_token": "1" * 64,
            "executable_path": "/fixture/worker.py",
            "executable_sha256": "2" * 64,
        }
        worker = launcher.Worker(
            "target_v012", SimpleNamespace(poll=lambda: None, pid=7),
            SimpleNamespace(), "channel", "worker", ready=ready,
            token="1" * 64,
        )
        policy = launcher.LaunchPolicy(
            launcher.RolePaths("/t", "/tw", "/to", 1),
            launcher.RolePaths("/h", "/hw", "/ho", 1), "/telemetry",
        )
        with patch.object(
            launcher, "live_rss",
            return_value=policy.per_process_rss_limit_bytes + 1,
        ):
            with self.assertRaisesRegex(launcher.LaunchRefusal, "live RSS"):
                launcher._sample_worker(worker, 1, policy, [])
        disk_guard = SimpleNamespace(
            disk_state=lambda: (
                17, policy.minimum_workspace_free_disk_bytes - 1,
            )
        )
        with self.assertRaisesRegex(launcher.LaunchRefusal, "free disk"):
            launcher._sample_disk(1, 17, policy, [], disk_guard)

    def test_stable_input_refuses_short_read_and_metadata_change_during_hash(self):
        with self.assertRaisesRegex(launcher.LaunchRefusal, "read was short"):
            with patch.object(launcher.os, "pread", return_value=b""):
                launcher._read_exact_fd(9, 1)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            parent = root / "authority"
            parent.mkdir()
            path = parent / "record.json"
            path.write_bytes(b'{"a":1}\n')
            path.chmod(0o444)
            with patch.object(launcher, "ROOT", root):
                retained = launcher.StableInput.open("fixture", path, json_record=True)
                original_hash = launcher._sha256_fd

                def mutate(descriptor):
                    digest = original_hash(descriptor)
                    path.chmod(0o644)
                    with path.open("ab") as stream:
                        stream.write(b" ")
                    path.chmod(0o444)
                    return digest

                with patch.object(launcher, "_sha256_fd", side_effect=mutate):
                    with self.assertRaisesRegex(launcher.LaunchRefusal, "changed"):
                        retained.verify()
                retained.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
