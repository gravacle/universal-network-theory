#!/usr/bin/env python3
"""Hostile tests for the bounded V003 failed-cache restart layer."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "replay_a01_a18_v003.py"
SPEC = importlib.util.spec_from_file_location("replay_a01_a18_v003_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


class V003RestartTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="v003-restart-")
        self.root = Path(self.temporary.name).resolve()
        self._copy_boundary()
        self._make_failed_tree()
        self.census = replay.build_census(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _copy_boundary(self) -> None:
        (self.root / "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001").mkdir(
            parents=True, exist_ok=True,
        )
        for relative in replay.RESTART_BOUNDARY_PATHS.values():
            source = replay.ROOT.joinpath(*PurePosixPath(relative).parts)
            target = self.root.joinpath(*PurePosixPath(relative).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
            target.chmod(0o444)

    def _make_failed_tree(self) -> None:
        parent = self.root.joinpath(*PurePosixPath(replay.SOURCE_RELATIVE).parts)
        parent.mkdir(parents=True)
        for length in replay.LENGTHS:
            cache = parent / f"L{length}"
            cache.mkdir()
            manifest = {
                "L": length,
                "canonical_cache_root": f"{replay.SOURCE_RELATIVE}/L{length}",
                "schema": "SYNTHETIC_FAILED_CACHE_V003",
            }
            raw = replay.retirement.publication_json_bytes(manifest)
            (cache / "CACHE_MANIFEST.json").write_bytes(raw)
            (cache / "payload.bin").write_bytes(bytes([length]) * length)
            (cache / "CACHE_MANIFEST.json").chmod(0o444)
            (cache / "payload.bin").chmod(0o444)
            cache.chmod(0o555)

    def _paths(self):
        return replay._transaction_paths(self.root, self.census)

    def test_production_census_is_exact_and_inclusive(self) -> None:
        census = replay.load_census()
        self.assertEqual(census["directory_count"], 6)
        self.assertEqual(census["file_count"], 1105)
        self.assertEqual(census["total_bytes"], 873_578_206)
        manifest_paths = {
            f"L{length}/CACHE_MANIFEST.json" for length in replay.LENGTHS
        }
        payloads = [row for row in census["files"] if row["path"] not in manifest_paths]
        self.assertEqual(len(payloads), 1100)
        self.assertEqual(sum(row["bytes"] for row in payloads), 873_210_476)
        self.assertEqual(census["manifest_mismatch_count"], 5)
        self.assertEqual(census["restart_boundary_sha256"], replay.RESTART_BOUNDARY_SHA256)
        self.assertEqual(
            census["required_absent_before_custody"],
            list(replay.REQUIRED_ABSENT_BEFORE_CUSTODY),
        )
        self.assertEqual(
            hashlib.sha256(replay.CENSUS_PATH.read_bytes()).hexdigest(),
            replay.CENSUS_SHA256,
        )
        metadata = os.stat(replay.CENSUS_PATH, follow_symlinks=False)
        self.assertEqual(metadata.st_nlink, 1)
        self.assertFalse(metadata.st_mode & 0o222)

    def test_exact_seventeen_value_token_action_diff_only(self) -> None:
        original = replay.ORIGINAL_EXISTING_PUBLISHER_ACTIONS()
        revised = replay.absolute_existing_publisher_actions()
        self.assertEqual(len(original), 11)
        self.assertEqual(len(revised), len(original))
        differences = []
        expected_flags = []
        for before, after in zip(original, revised):
            self.assertEqual(before[:2], after[:2])
            self.assertEqual(len(before.command), len(after.command))
            self.assertEqual(before.command[:3], after.command[:3])
            self.assertFalse(PurePosixPath(after.command[2]).is_absolute())
            for index, (left, right) in enumerate(zip(before.command, after.command)):
                if left != right:
                    differences.append((before.artifact_id, before.instance, index, left, right))
                    self.assertTrue(PurePosixPath(right).is_absolute())
                    self.assertFalse(PurePosixPath(left).is_absolute())
                    expected_flags.append(before.command[index - 1])
        self.assertEqual(len(differences), 17)
        self.assertEqual(expected_flags.count("--output"), 9)
        self.assertEqual(expected_flags.count("--cache-root"), 4)
        self.assertEqual(expected_flags.count("--workspace"), 4)

    def test_success_retains_complete_tree_identity_and_restarts(self) -> None:
        before = copy.deepcopy(self.census["directories"]), copy.deepcopy(self.census["files"])
        result = replay.retire_failed_cache(self.root, self.census)
        source, custody, target, intent, receipt = self._paths()
        self.assertEqual(result["classification"], "PASS_EXACT_OWNER_ONCE_FAILED_CACHE_CUSTODY")
        self.assertFalse(replay.retirement.path_exists(source))
        self.assertTrue(target.is_dir())
        replay.inspect_tree(target, self.census)
        inventory = replay._tree_inventory(target)
        self.assertEqual((inventory["directories"], inventory["files"]), before)
        self.assertEqual(
            {child.name for child in custody.iterdir()},
            {replay.CUSTODY_TREE_NAME, replay.INTENT_NAME, replay.RECEIPT_NAME},
        )
        self.assertTrue(intent.is_file())
        self.assertTrue(receipt.is_file())
        restarted = replay.retire_failed_cache(self.root, self.census)
        self.assertEqual(restarted["classification"], "PASS_COMPLETED_CUSTODY_RECONCILED")
        self.assertEqual(restarted["receipt_sha256"], result["receipt_sha256"])

    def test_all_interruption_windows_restart_to_exact_success(self) -> None:
        for injection in (
            "after_custody_mkdir", "after_intent", "after_rename", "after_fsync",
        ):
            with self.subTest(injection=injection):
                if injection != "after_custody_mkdir":
                    self.tearDown()
                    self.setUp()
                with self.assertRaisesRegex(RuntimeError, "injected"):
                    replay.retire_failed_cache(
                        self.root, self.census, inject_at=injection,
                    )
                result = replay.retire_failed_cache(self.root, self.census)
                self.assertEqual(
                    result["classification"],
                    "PASS_EXACT_OWNER_ONCE_FAILED_CACHE_CUSTODY",
                )
                source, _custody, target, _intent, _receipt = self._paths()
                self.assertFalse(replay.retirement.path_exists(source))
                replay.inspect_tree(target, self.census)

    def test_destination_symlink_extra_and_identity_attacks_refuse(self) -> None:
        source, custody, target, _intent, _receipt = self._paths()
        custody.mkdir()
        (custody / "EXTRA").write_text("attacker", encoding="utf-8")
        with self.assertRaises(replay.Refusal):
            replay.retire_failed_cache(self.root, self.census)
        self.assertTrue(source.is_dir())

        self.tearDown()
        self.setUp()
        source, custody, _target, _intent, _receipt = self._paths()
        alias = self.root / "alias"
        alias.mkdir()
        custody.symlink_to(alias, target_is_directory=True)
        with self.assertRaises(replay.Refusal):
            replay.retire_failed_cache(self.root, self.census)
        self.assertTrue(source.is_dir())

        self.tearDown()
        self.setUp()
        source, custody, target, _intent, _receipt = self._paths()
        replay.retire_failed_cache(self.root, self.census)
        (custody / "EXTRA").write_text("attacker", encoding="utf-8")
        with self.assertRaises(replay.Refusal):
            replay.retire_failed_cache(self.root, self.census)
        replay.inspect_tree(target, self.census)

        self.tearDown()
        self.setUp()
        source, _custody, _target, _intent, _receipt = self._paths()
        attacked = source / "L4/payload.bin"
        raw = attacked.read_bytes()
        replacement = source / "L4/replacement.bin"
        attacked.parent.chmod(0o755)
        replacement.write_bytes(raw)
        replacement.chmod(0o444)
        os.replace(replacement, attacked)
        attacked.parent.chmod(0o555)
        with self.assertRaisesRegex(replay.Refusal, "tree differs"):
            replay.retire_failed_cache(self.root, self.census)

    def test_boundary_and_required_absence_attacks_refuse_before_move(self) -> None:
        source, custody, _target, _intent, _receipt = self._paths()
        boundary = self.root.joinpath(
            *PurePosixPath(replay.RESTART_BOUNDARY_PATHS["A04_UNIVERSAL_CUSTODY_GATE"]).parts
        )
        boundary.chmod(0o644)
        with self.assertRaises(replay.Refusal):
            replay.retire_failed_cache(self.root, self.census)
        self.assertTrue(source.is_dir())
        self.assertFalse(replay.retirement.path_exists(custody))

        self.tearDown()
        self.setUp()
        source, custody, _target, _intent, _receipt = self._paths()
        forbidden = self.root.joinpath(
            *PurePosixPath(replay.REQUIRED_ABSENT_BEFORE_CUSTODY[0]).parts
        )
        forbidden.parent.mkdir(parents=True, exist_ok=True)
        forbidden.write_text("too late", encoding="utf-8")
        with self.assertRaisesRegex(replay.Refusal, "must be absent"):
            replay.retire_failed_cache(self.root, self.census)
        self.assertTrue(source.is_dir())
        self.assertFalse(replay.retirement.path_exists(custody))

    def _make_distinct_rebuilt(self, complete: bool) -> None:
        source, _custody, _target, _intent, _receipt = self._paths()
        source.mkdir(parents=True)
        lengths = replay.LENGTHS if complete else (4,)
        for length in lengths:
            cache = source / f"L{length}"
            cache.mkdir()
            manifest = {
                "L": length,
                "canonical_cache_root": str(source / f"L{length}"),
                "schema": "SYNTHETIC_REBUILT_CACHE_V003",
            }
            (cache / "CACHE_MANIFEST.json").write_bytes(
                replay.retirement.publication_json_bytes(manifest)
            )
            (cache / "CACHE_MANIFEST.json").chmod(0o444)
            if complete:
                (cache / "payload.bin").write_bytes(b"new" + bytes([length]))
                (cache / "payload.bin").chmod(0o444)
                cache.chmod(0o555)

    def test_completed_custody_accepts_partial_or_complete_distinct_rebuild(self) -> None:
        for complete in (False, True):
            with self.subTest(complete=complete):
                if complete:
                    self.tearDown()
                    self.setUp()
                replay.retire_failed_cache(self.root, self.census)
                self._make_distinct_rebuilt(complete)
                result = replay.retire_failed_cache(self.root, self.census)
                self.assertEqual(
                    result["classification"],
                    "PASS_COMPLETED_CUSTODY_WITH_DISTINCT_REBUILT_CANONICAL_PARENT",
                )

    def test_completed_custody_rejects_reappeared_malformed_copy(self) -> None:
        replay.retire_failed_cache(self.root, self.census)
        source, _custody, target, _intent, _receipt = self._paths()
        shutil.copytree(target, source, copy_function=shutil.copy2)
        with self.assertRaisesRegex(replay.Refusal, "reappeared"):
            replay.retire_failed_cache(self.root, self.census)

    def test_wrong_or_lookalike_receipt_refuses_before_v002(self) -> None:
        calls: list[str] = []
        with mock.patch.object(
            replay, "authenticate_original_retirement",
            side_effect=lambda _digest: calls.append("old-auth"),
        ), mock.patch.object(
            replay, "retire_failed_cache",
            side_effect=lambda *_args: calls.append("custody"),
        ), mock.patch.object(
            replay.v002, "coordinate_canonical_a01_a18_replay",
            side_effect=lambda *_args: calls.append("v002"),
        ):
            with self.assertRaisesRegex(replay.Refusal, "receipt authorization"):
                replay.coordinate_canonical_a01_a18_replay(
                    replay.ORIGINAL_RETIREMENT_RECEIPT_SHA256, "0" * 64,
                )
        self.assertEqual(calls, [])

        replay.retire_failed_cache(self.root, self.census)
        _source, _custody, _target, _intent, receipt = self._paths()
        receipt.chmod(0o644)
        receipt.write_bytes(replay.retirement.publication_json_bytes({
            "schema": "V012_FAILED_CACHE_CUSTODY_RECEIPT_V003",
            "classification": "PASS_EXACT_OWNER_ONCE_FAILED_CACHE_CUSTODY",
        }))
        receipt.chmod(0o444)
        with self.assertRaises(replay.Refusal):
            replay.retire_failed_cache(self.root, self.census)

    def test_receipt_result_bound_and_action_patch_always_restored(self) -> None:
        original = replay.v001.existing_publisher_actions
        with mock.patch.object(replay, "authenticate_original_retirement"), \
                mock.patch.object(replay, "load_census", return_value=self.census), \
                mock.patch.object(
                    replay, "retire_failed_cache",
                    return_value={"receipt_sha256": "wrong"},
                ), mock.patch.object(
                    replay.v002, "coordinate_canonical_a01_a18_replay",
                ) as delegate:
            with self.assertRaisesRegex(replay.Refusal, "receipt digest"):
                replay.coordinate_canonical_a01_a18_replay(
                    replay.ORIGINAL_RETIREMENT_RECEIPT_SHA256,
                    replay.FAILED_CACHE_RECEIPT_SHA256,
                )
            delegate.assert_not_called()
        self.assertIs(replay.v001.existing_publisher_actions, original)

        observed = []
        def delegated(_digest):
            observed.append(replay.v001.existing_publisher_actions)
            raise RuntimeError("hostile delegated interruption")

        with mock.patch.object(replay, "authenticate_original_retirement"), \
                mock.patch.object(replay, "load_census", return_value=self.census), \
                mock.patch.object(
                    replay, "retire_failed_cache",
                    return_value={"receipt_sha256": replay.FAILED_CACHE_RECEIPT_SHA256},
                ), mock.patch.object(
                    replay.v002, "coordinate_canonical_a01_a18_replay",
                    side_effect=delegated,
                ):
            with self.assertRaisesRegex(RuntimeError, "delegated interruption"):
                replay.coordinate_canonical_a01_a18_replay(
                    replay.ORIGINAL_RETIREMENT_RECEIPT_SHA256,
                    replay.FAILED_CACHE_RECEIPT_SHA256,
                )
        self.assertEqual(observed, [replay.absolute_existing_publisher_actions])
        self.assertIs(replay.v001.existing_publisher_actions, original)

    def test_plan_and_unauthorized_entry_do_not_mutate_canonical_tree(self) -> None:
        watched = [
            replay.ROOT.joinpath(*PurePosixPath(replay.SOURCE_RELATIVE).parts),
            replay.CENSUS_PATH,
        ]
        before = [(os.stat(path, follow_symlinks=False).st_ino,
                   os.stat(path, follow_symlinks=False).st_mtime_ns) for path in watched]
        custody = replay.ROOT.joinpath(*PurePosixPath(replay.CUSTODY_ROOT_RELATIVE).parts)
        self.assertFalse(replay.retirement.path_exists(custody))
        plan = subprocess.run(
            [sys.executable, "-B", str(SOURCE), "--plan"],
            cwd=replay.ROOT, check=False, capture_output=True, text=True,
        )
        self.assertEqual(plan.returncode, 0, plan.stderr)
        refused = subprocess.run(
            [sys.executable, "-B", str(SOURCE), "--execute-canonical"],
            cwd=replay.ROOT, check=False, capture_output=True, text=True,
        )
        self.assertEqual(refused.returncode, 2)
        after = [(os.stat(path, follow_symlinks=False).st_ino,
                  os.stat(path, follow_symlinks=False).st_mtime_ns) for path in watched]
        self.assertEqual(after, before)
        self.assertFalse(replay.retirement.path_exists(custody))

    def test_source_has_no_delete_wildcard_or_direct_v001_delegate(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        for forbidden in ("unlink(", "rmtree(", ".glob(", "os.remove("):
            self.assertNotIn(forbidden, source)
        coordinate = inspect.getsource(replay.coordinate_canonical_a01_a18_replay)
        self.assertIn("v002.coordinate_canonical_a01_a18_replay", coordinate)
        self.assertNotIn("v001.coordinate_canonical_a01_a18_replay", coordinate)
        self.assertEqual(
            list(inspect.signature(replay.coordinate_canonical_a01_a18_replay).parameters),
            ["expected_retirement_receipt_sha256", "expected_failed_cache_receipt_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
