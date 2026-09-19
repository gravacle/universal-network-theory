#!/usr/bin/env python3
"""Hostile tests for V007's single replay-owned A18 parent."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "replay_a01_a18_v007.py"
SPEC = importlib.util.spec_from_file_location("replay_a01_a18_v007_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


class V007A18ParentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="v007-a18-parent-")
        self.root = Path(self.temporary.name).resolve()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def parent(self) -> Path:
        return self.root.joinpath(*replay.PARENT_RELATIVE.parts)

    def test_frozen_v006_packet_hashes_and_custody(self) -> None:
        for name, expected in replay.PINNED_V006_PACKET.items():
            path = HERE / name
            metadata = os.stat(path, follow_symlinks=False)
            self.assertTrue(stat.S_ISREG(metadata.st_mode))
            self.assertEqual(metadata.st_nlink, 1)
            self.assertFalse(metadata.st_mode & 0o222)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
            self.assertEqual(
                hashlib.sha256(replay._read_frozen_packet_file(name)).hexdigest(),
                expected,
            )

    def test_absent_parent_creation_publish_and_exact_a18_restart(self) -> None:
        record = {"schema": "SYNTHETIC_A18", "value": 18}
        custody = replay.A18ParentCustody.acquire(self.root)
        self.assertTrue(custody.created)
        self.assertEqual(custody.entry_state, "EMPTY_PRE_A18")
        try:
            result = replay._guarded_reconcile(
                custody, replay.v001._reconcile_or_publish_json,
                self.parent() / replay.A18_NAME, record,
                "A18_L10_CROSS_GATE", (),
            )
            self.assertFalse(result[1])
            self.assertEqual(result[0], custody.a18_sha256)
            identity = custody.a18_identity
            digest = custody.a18_sha256
        finally:
            custody.close()

        custody = replay.A18ParentCustody.acquire(self.root)
        self.assertFalse(custody.created)
        self.assertEqual(custody.entry_state, "A18_ONLY")
        self.assertEqual(custody.a18_identity, identity)
        self.assertEqual(custody.a18_sha256, digest)
        try:
            result = replay._guarded_reconcile(
                custody, replay.v001._reconcile_or_publish_json,
                self.parent() / replay.A18_NAME, record,
                "A18_L10_CROSS_GATE", (),
            )
            self.assertTrue(result[1])
            self.assertEqual(result[0], digest)
            self.assertEqual(custody.a18_identity, identity)
        finally:
            custody.close()

    def test_existing_exact_empty_parent_reconciles(self) -> None:
        self.parent().mkdir(mode=replay.PARENT_MODE)
        before = os.stat(self.parent(), follow_symlinks=False)
        custody = replay.A18ParentCustody.acquire(self.root)
        try:
            self.assertFalse(custody.created)
            self.assertEqual(custody.entry_state, "EMPTY_PRE_A18")
            self.assertEqual(
                custody.parent_identity,
                (before.st_dev, before.st_ino, before.st_mode),
            )
            self.assertEqual(tuple(self.parent().iterdir()), ())
        finally:
            custody.close()

    def test_created_parent_mode_is_exact_under_restrictive_umask(self) -> None:
        previous_umask = os.umask(0o077)
        try:
            custody = replay.A18ParentCustody.acquire(self.root)
        finally:
            os.umask(previous_umask)
        try:
            self.assertTrue(custody.created)
            self.assertEqual(
                stat.S_IMODE(os.stat(self.parent(), follow_symlinks=False).st_mode),
                replay.PARENT_MODE,
            )
            self.assertEqual(
                custody.authenticate_boundary(allow_transition=False),
                "EMPTY_PRE_A18",
            )
        finally:
            custody.close()

    def test_alias_file_wrong_mode_and_unregistered_child_refuse(self) -> None:
        external = tempfile.TemporaryDirectory(prefix="v007-parent-alias-")
        self.parent().symlink_to(Path(external.name), target_is_directory=True)
        with self.assertRaises(replay.Refusal):
            replay.A18ParentCustody.acquire(self.root)
        self.parent().unlink()
        external.cleanup()

        self.parent().write_bytes(b"not a directory")
        with self.assertRaises(replay.Refusal):
            replay.A18ParentCustody.acquire(self.root)
        self.parent().unlink()

        self.parent().mkdir(mode=0o700)
        self.parent().chmod(0o700)
        with self.assertRaisesRegex(replay.Refusal, "mode identity"):
            replay.A18ParentCustody.acquire(self.root)
        self.parent().rmdir()

        self.parent().mkdir(mode=replay.PARENT_MODE)
        extra = self.parent() / "UNREGISTERED"
        extra.write_bytes(b"preserve me")
        extra.chmod(0o444)
        with self.assertRaisesRegex(replay.Refusal, "unregistered child"):
            replay.A18ParentCustody.acquire(self.root)
        self.assertTrue(extra.is_file())

    def test_parent_swap_and_mode_change_refuse_while_descriptor_is_held(self) -> None:
        custody = replay.A18ParentCustody.acquire(self.root)
        moved = self.root / "retained-original-parent"
        self.parent().rename(moved)
        self.parent().mkdir(mode=replay.PARENT_MODE)
        try:
            with self.assertRaisesRegex(replay.Refusal, "identity mismatch"):
                custody.authenticate_boundary(allow_transition=False)
        finally:
            custody.close()
        self.assertTrue(moved.is_dir())
        self.parent().rmdir()
        moved.rename(self.parent())

        custody = replay.A18ParentCustody.acquire(self.root)
        self.parent().chmod(0o700)
        try:
            with self.assertRaisesRegex(replay.Refusal, "mode identity"):
                custody.authenticate_boundary(allow_transition=False)
        finally:
            custody.close()

    def test_repository_root_swap_refuses_while_descriptors_are_held(self) -> None:
        custody = replay.A18ParentCustody.acquire(self.root)
        moved = self.root.with_name(self.root.name + "-retained")
        self.root.rename(moved)
        self.root.mkdir(mode=0o700)
        try:
            with self.assertRaisesRegex(replay.Refusal, "root dev/inode/mode"):
                custody.authenticate_boundary(allow_transition=False)
        finally:
            custody.close()
            self.root.rmdir()
            moved.rename(self.root)

    def test_exact_a18_appearance_outside_guarded_boundary_refuses(self) -> None:
        custody = replay.A18ParentCustody.acquire(self.root)
        replay.retirement.publish_once(
            self.parent() / replay.A18_NAME, {"hostile": "outside boundary"},
        )
        try:
            with self.assertRaisesRegex(replay.Refusal, "outside publication boundary"):
                custody.authenticate_boundary(allow_transition=False)
            self.assertTrue((self.parent() / replay.A18_NAME).is_file())
        finally:
            custody.close()

    def test_unregistered_child_inside_publication_is_refused_and_preserved(self) -> None:
        custody = replay.A18ParentCustody.acquire(self.root)
        extra = self.parent() / "EXTRA"

        def hostile_original(path, record, artifact_id, sinks):
            extra.write_bytes(b"preserved hostile child")
            extra.chmod(0o444)
            return replay.v001._reconcile_or_publish_json(
                path, record, artifact_id, sinks,
            )

        try:
            with self.assertRaisesRegex(replay.Refusal, "unregistered child"):
                replay._guarded_reconcile(
                    custody, hostile_original,
                    self.parent() / replay.A18_NAME, {"synthetic": True},
                    "A18_L10_CROSS_GATE", (),
                )
            self.assertTrue(extra.is_file())
        finally:
            custody.close()

    def test_publication_identity_or_result_mismatch_refuses(self) -> None:
        custody = replay.A18ParentCustody.acquire(self.root)
        try:
            with self.assertRaisesRegex(replay.Refusal, "identity/path mismatch"):
                replay._guarded_reconcile(
                    custody, replay.v001._reconcile_or_publish_json,
                    self.parent() / "WRONG.json", {"x": 1},
                    "A18_L10_CROSS_GATE", (),
                )

            def wrong_result(path, record, _artifact_id, _sinks):
                digest = replay.retirement.publish_once(path, dict(record))
                return "0" * 64, False

            with self.assertRaisesRegex(replay.Refusal, "result/custody mismatch"):
                replay._guarded_reconcile(
                    custody, wrong_result,
                    self.parent() / replay.A18_NAME, {"x": 1},
                    "A18_L10_CROSS_GATE", (),
                )
            self.assertTrue((self.parent() / replay.A18_NAME).is_file())
        finally:
            custody.close()

    def test_wrong_canonical_input_refuses_before_a18_publication(self) -> None:
        with mock.patch.object(replay, "ROOT", self.root):
            custody = replay.A18ParentCustody.acquire(self.root)
            try:
                a18 = self.parent() / replay.A18_NAME
                self.assertFalse(replay.retirement.path_exists(a18))
                with self.assertRaisesRegex(replay.Refusal, "input digest mismatch"):
                    replay._guarded_reconcile(
                        custody, replay.v001._reconcile_or_publish_json,
                        a18, {"wrong": "canonical candidate"},
                        "A18_L10_CROSS_GATE", (),
                    )
                self.assertFalse(replay.retirement.path_exists(a18))
                self.assertEqual(
                    custody.authenticate_boundary(allow_transition=False),
                    "EMPTY_PRE_A18",
                )
            finally:
                custody.close()

    def test_arbitrary_delegate_failure_restores_reconcile_global_and_closes(self) -> None:
        original = replay.v001._reconcile_or_publish_json
        with mock.patch.object(
            replay.v006, "coordinate_canonical_a01_a18_replay",
            side_effect=RuntimeError("forced delegate failure"),
        ), mock.patch.object(
            replay.A18ParentCustody, "acquire",
            side_effect=AssertionError("parent acquired before A18 boundary"),
        ) as acquire:
            with self.assertRaisesRegex(RuntimeError, "forced delegate"):
                replay.coordinate_canonical_a01_a18_replay("a" * 64, "b" * 64)
        self.assertIs(replay.v001._reconcile_or_publish_json, original)
        acquire.assert_not_called()

    def test_delegate_cannot_report_success_without_exact_a18_boundary(self) -> None:
        original = replay.v001._reconcile_or_publish_json
        with mock.patch.object(
            replay.v006, "coordinate_canonical_a01_a18_replay", return_value={},
        ), mock.patch.object(
            replay.A18ParentCustody, "acquire",
            side_effect=AssertionError("parent acquired without A18 call"),
        ) as acquire:
            with self.assertRaisesRegex(replay.Refusal, "lacks its exact A18"):
                replay.coordinate_canonical_a01_a18_replay("a" * 64, "b" * 64)
        self.assertIs(replay.v001._reconcile_or_publish_json, original)
        acquire.assert_not_called()

    def test_current_plan_and_unauthorized_mode_do_not_create_parent(self) -> None:
        canonical_parent = replay.ROOT.joinpath(*replay.PARENT_RELATIVE.parts)
        self.assertFalse(replay.retirement.path_exists(canonical_parent))
        watched = (SOURCE, HERE / "replay_a01_a18_v006.py")
        before = {
            path: replay._identity(os.stat(path, follow_symlinks=False))
            for path in watched
        }
        plan = subprocess.run(
            [sys.executable, "-B", str(SOURCE), "--plan"],
            cwd=replay.ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(plan.returncode, 0, plan.stderr)
        self.assertIn("\"current_parent_status\": \"ABSENT\"", plan.stdout)
        refused = subprocess.run(
            [sys.executable, "-B", str(SOURCE), "--execute-canonical"],
            cwd=replay.ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(refused.returncode, 2)
        self.assertFalse(replay.retirement.path_exists(canonical_parent))
        after = {
            path: replay._identity(os.stat(path, follow_symlinks=False))
            for path in watched
        }
        self.assertEqual(after, before)

    def test_plan_claim_is_strictly_bounded(self) -> None:
        plan = replay.replay_plan()
        self.assertEqual(
            plan["classification"],
            "BOUNDED_NONEXECUTED_V007_A18_PARENT_CUSTODY_PLAN",
        )
        self.assertEqual(plan["current_parent_status"], "ABSENT")
        self.assertFalse(plan["record_or_publisher_order_changed"])
        self.assertFalse(plan["canonical_action_executed"])
        self.assertIn("NO_CONTINUOUS_EXTERNAL_WRITER_EXCLUSION", plan["claim_boundary"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
