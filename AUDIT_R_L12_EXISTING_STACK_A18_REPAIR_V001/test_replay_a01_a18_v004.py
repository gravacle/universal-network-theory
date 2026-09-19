#!/usr/bin/env python3
"""Hostile tests for the four explicit V004 transaction boundaries."""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "replay_a01_a18_v004.py"
SPEC = importlib.util.spec_from_file_location("replay_a01_a18_v004_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


class V004BoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="v004-boundary-")
        self.root = Path(self.temporary.name).resolve()
        (self.root / "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001").mkdir(
            parents=True,
        )
        for relative in replay.v003.RESTART_BOUNDARY_PATHS.values():
            source = replay.ROOT.joinpath(*PurePosixPath(relative).parts)
            target = self.root.joinpath(*PurePosixPath(relative).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
            target.chmod(0o444)
        cache_parent = self.root.joinpath(
            *PurePosixPath(replay.v003.SOURCE_RELATIVE).parts
        )
        cache_parent.mkdir(parents=True)
        for length in replay.v003.LENGTHS:
            cache = cache_parent / f"L{length}"
            cache.mkdir()
            manifest = {
                "L": length,
                "canonical_cache_root": (
                    f"{replay.v003.SOURCE_RELATIVE}/L{length}"
                ),
                "schema": "SYNTHETIC_FAILED_CACHE_V004",
            }
            (cache / "CACHE_MANIFEST.json").write_bytes(
                replay.retirement.publication_json_bytes(manifest)
            )
            (cache / "payload.bin").write_bytes(bytes([length]) * length)
            (cache / "CACHE_MANIFEST.json").chmod(0o444)
            (cache / "payload.bin").chmod(0o444)
            cache.chmod(0o555)
        self.census = replay.v003.build_census(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _paths(self):
        return replay.v003._transaction_paths(self.root, self.census)

    def _a06(self) -> Path:
        relative = replay.v003.REQUIRED_ABSENT_BEFORE_CUSTODY[0]
        return self.root.joinpath(*PurePosixPath(relative).parts)

    def _publish_a06(self) -> None:
        path = self._a06()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"hostile A06 appearance\n")
        path.chmod(0o444)

    def test_all_five_frozen_v003_predecessor_hashes_and_custody(self) -> None:
        for name, expected in replay.PINNED_V003_PACKET.items():
            path = HERE / name
            metadata = os.stat(path, follow_symlinks=False)
            self.assertTrue(stat.S_ISREG(metadata.st_mode))
            self.assertEqual(metadata.st_nlink, 1)
            self.assertFalse(metadata.st_mode & 0o222)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
            self.assertEqual(hashlib.sha256(replay._read_frozen_packet_file(name)).hexdigest(), expected)

    def test_boundaries_are_ordered_around_rename_fsync_and_receipt(self) -> None:
        events: list[str] = []
        authenticate = replay._authenticate_explicit_boundary
        fsync_tree = replay.v003._fsync_tree

        def observed_authenticate(root, census, label):
            events.append(label)
            return authenticate(root, census, label)

        def observed_fsync(path):
            events.append("FSYNC_TREE")
            return fsync_tree(path)

        with mock.patch.object(
            replay, "_authenticate_explicit_boundary",
            side_effect=observed_authenticate,
        ), mock.patch.object(
            replay.v003, "_fsync_tree", side_effect=observed_fsync,
        ):
            result = replay.retire_failed_cache(self.root, self.census)
        self.assertEqual(
            result["classification"],
            "PASS_EXACT_OWNER_ONCE_FAILED_CACHE_CUSTODY",
        )
        required = [
            "V004 transaction entry",
            "V004 pre-rename boundary",
            "V004 post-rename boundary",
            "FSYNC_TREE",
            "V004 pre-receipt boundary",
            "V004 post-receipt boundary",
            "V004 pre-V002 boundary",
        ]
        self.assertEqual(events, required)

    def test_hostile_a06_inside_rename_refuses_and_preserves_moved_tree(self) -> None:
        delegated: list[str] = []

        def hostile_rename(source, target):
            replay.ORIGINAL_RENAME_EXCLUSIVE(source, target)
            self._publish_a06()

        strict_retire = replay.retire_failed_cache

        def injected_retire(root, census, **kwargs):
            return strict_retire(
                root, census, test_rename_primitive=hostile_rename, **kwargs,
            )

        def fake_v003_coordinate(_old_receipt, _cache_receipt):
            replay.v003.retire_failed_cache(self.root, self.census)
            delegated.append("V002")
            return {}

        with mock.patch.object(
            replay, "retire_failed_cache", side_effect=injected_retire,
        ), mock.patch.object(
            replay.v003, "coordinate_canonical_a01_a18_replay",
            side_effect=fake_v003_coordinate,
        ):
            with self.assertRaisesRegex(replay.Refusal, "post-rename"):
                replay.coordinate_canonical_a01_a18_replay(
                    replay.v003.ORIGINAL_RETIREMENT_RECEIPT_SHA256,
                    replay.v003.FAILED_CACHE_RECEIPT_SHA256,
                )
        self.assertEqual(delegated, [])
        source, custody, target, intent, receipt = self._paths()
        self.assertFalse(replay.retirement.path_exists(source))
        self.assertTrue(custody.is_dir())
        replay.v003.inspect_tree(target, self.census)
        self.assertTrue(intent.is_file())
        self.assertFalse(replay.retirement.path_exists(receipt))
        self.assertTrue(self._a06().is_file())

    def test_post_receipt_a06_refuses_before_delegate_and_preserves_receipt(self) -> None:
        delegated: list[str] = []

        def hostile_publish(path, record):
            digest = replay.ORIGINAL_PUBLISH_ONCE(path, record)
            if path.name == replay.v003.RECEIPT_NAME:
                self._publish_a06()
            return digest

        strict_retire = replay.retire_failed_cache

        def injected_retire(root, census, **kwargs):
            return strict_retire(
                root, census, test_publish_primitive=hostile_publish, **kwargs,
            )

        def fake_v003_coordinate(_old_receipt, _cache_receipt):
            replay.v003.retire_failed_cache(self.root, self.census)
            delegated.append("V002")
            return {}

        with mock.patch.object(
            replay, "retire_failed_cache", side_effect=injected_retire,
        ), mock.patch.object(
            replay.v003, "coordinate_canonical_a01_a18_replay",
            side_effect=fake_v003_coordinate,
        ):
            with self.assertRaisesRegex(replay.Refusal, "post-receipt"):
                replay.coordinate_canonical_a01_a18_replay(
                    replay.v003.ORIGINAL_RETIREMENT_RECEIPT_SHA256,
                    replay.v003.FAILED_CACHE_RECEIPT_SHA256,
                )
        self.assertEqual(delegated, [])
        source, _custody, target, intent, receipt = self._paths()
        self.assertFalse(replay.retirement.path_exists(source))
        replay.v003.inspect_tree(target, self.census)
        self.assertTrue(intent.is_file())
        self.assertTrue(receipt.is_file())

    def test_ordinary_preexisting_a06_refuses_without_move(self) -> None:
        self._publish_a06()
        source, custody, _target, _intent, _receipt = self._paths()
        with self.assertRaisesRegex(replay.Refusal, "must be absent"):
            replay.retire_failed_cache(self.root, self.census)
        replay.v003.inspect_tree(source, self.census)
        self.assertFalse(replay.retirement.path_exists(custody))

    def test_completed_receipt_allows_later_legitimate_downstream_restart(self) -> None:
        first = replay.retire_failed_cache(self.root, self.census)
        self._publish_a06()
        second = replay.retire_failed_cache(self.root, self.census)
        self.assertEqual(
            second["classification"], "PASS_COMPLETED_CUSTODY_RECONCILED",
        )
        self.assertEqual(second["receipt_sha256"], first["receipt_sha256"])

    def test_primitives_and_v003_entry_restore_after_refusal(self) -> None:
        original_v003_retire = replay.v003.retire_failed_cache
        original_rename = replay.retirement.rename_exclusive
        original_publish = replay.retirement.publish_once

        def hostile_rename(source, target):
            replay.ORIGINAL_RENAME_EXCLUSIVE(source, target)
            self._publish_a06()

        with self.assertRaises(replay.Refusal):
            replay.retire_failed_cache(
                self.root, self.census,
                test_rename_primitive=hostile_rename,
            )
        self.assertIs(replay.retirement.rename_exclusive, original_rename)
        self.assertIs(replay.retirement.publish_once, original_publish)

        with mock.patch.object(
            replay.v003, "coordinate_canonical_a01_a18_replay",
            side_effect=RuntimeError("injected V003 refusal"),
        ):
            with self.assertRaisesRegex(RuntimeError, "injected V003"):
                replay.coordinate_canonical_a01_a18_replay(
                    replay.v003.ORIGINAL_RETIREMENT_RECEIPT_SHA256,
                    replay.v003.FAILED_CACHE_RECEIPT_SHA256,
                )
        self.assertIs(replay.v003.retire_failed_cache, original_v003_retire)

    def test_plan_and_unauthorized_modes_do_not_mutate_canonical_tree(self) -> None:
        watched = [
            replay.ROOT.joinpath(*PurePosixPath(replay.v003.SOURCE_RELATIVE).parts),
            replay.v003.CENSUS_PATH,
        ]
        before = [
            (os.stat(path, follow_symlinks=False).st_ino,
             os.stat(path, follow_symlinks=False).st_mtime_ns)
            for path in watched
        ]
        custody = replay.ROOT.joinpath(
            *PurePosixPath(replay.v003.CUSTODY_ROOT_RELATIVE).parts
        )
        self.assertFalse(replay.retirement.path_exists(custody))
        plan = subprocess.run(
            [sys.executable, "-B", str(SOURCE), "--plan"],
            cwd=replay.ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(plan.returncode, 0, plan.stderr)
        refused = subprocess.run(
            [sys.executable, "-B", str(SOURCE), "--execute-canonical"],
            cwd=replay.ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(refused.returncode, 2)
        after = [
            (os.stat(path, follow_symlinks=False).st_ino,
             os.stat(path, follow_symlinks=False).st_mtime_ns)
            for path in watched
        ]
        self.assertEqual(after, before)
        self.assertFalse(replay.retirement.path_exists(custody))

    def test_claim_and_surface_are_strictly_bounded(self) -> None:
        plan = replay.replay_plan()
        self.assertEqual(plan["explicit_absence_boundary_count"], 4)
        self.assertFalse(plan["general_lock_or_continuous_exclusion_claim"])
        source = SOURCE.read_text(encoding="utf-8")
        for forbidden in ("unlink(", "rmtree(", ".glob(", "os.remove("):
            self.assertNotIn(forbidden, source)
        self.assertNotIn("fcntl", source)
        coordinate = inspect.getsource(replay.coordinate_canonical_a01_a18_replay)
        self.assertIn("v003.coordinate_canonical_a01_a18_replay", coordinate)
        self.assertNotIn("v002.coordinate_canonical_a01_a18_replay", coordinate)


if __name__ == "__main__":
    unittest.main()
