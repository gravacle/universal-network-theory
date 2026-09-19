#!/usr/bin/env python3
"""Adverse tests for the exact retirement coordinator; canonical paths untouched."""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "retire_canonical_stack.py"
SPEC = importlib.util.spec_from_file_location("retire_canonical_stack_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
retirement = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(retirement)


class RetirementCoordinatorTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> dict[str, object]:
        (root / "target/tree/nested").mkdir(parents=True)
        (root / "hostile").mkdir()
        (root / "audit").mkdir()
        payloads = {
            root / "target/a.json": b'{"a":1}\n',
            root / "target/tree/b.bin": b"branch-b",
            root / "target/tree/nested/c.bin": b"branch-c",
            root / "hostile/d.json": b'{"d":4}\n',
        }
        for path, raw in payloads.items():
            path.write_bytes(raw)
            path.chmod(0o444)
        directory = retirement.directory_row(
            root / "target/tree", "target/tree",
        )
        entries = [
            {
                "kind": "file",
                **retirement.file_row(root / "target/a.json", "target/a.json"),
            },
            directory,
            {
                "kind": "file",
                **retirement.file_row(root / "hostile/d.json", "hostile/d.json"),
            },
        ]
        census = {
            "schema": "V012_A01_A17_PRE_A18_RETIREMENT_CENSUS_V001",
            "classification": "EXACT_NONEXECUTED_OWNER_ONCE_RETIREMENT_CENSUS",
            "custody_root": "audit/retired-v001",
            "entries": entries,
            "required_absent_paths": ["future/a18.json"],
            "entry_count": len(entries),
            "source_file_count": sum(
                1 if entry["kind"] == "file" else entry["file_count"]
                for entry in entries
            ),
            "source_total_bytes": sum(
                entry["bytes"] if entry["kind"] == "file"
                else entry["total_bytes"]
                for entry in entries
            ),
            "executed": False,
            "claim_boundary": "SYNTHETIC_TEST_ONLY",
        }
        return retirement.validate_census(census)

    def assert_sources_present(self, root: Path, census: dict[str, object]) -> None:
        for entry in census["entries"]:
            source = root.joinpath(*retirement.PurePosixPath(entry["path"]).parts)
            retirement.inspect_entry(source, entry)
        custody = root.joinpath(
            *retirement.PurePosixPath(census["custody_root"]).parts
        )
        self.assertFalse(retirement.path_exists(custody))

    def test_dry_run_has_no_filesystem_effect(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            before = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
            result = retirement.preflight(root, census)
            after = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
            self.assertEqual(result["classification"], "PASS_EXACT_RETIREMENT_DRY_RUN_NO_MUTATION")
            self.assertEqual(before, after)
            self.assert_sources_present(root, census)

    def test_no_clobber_refuses_preexisting_custody(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            custody = root / "audit/retired-v001"
            custody.mkdir(parents=True)
            with self.assertRaisesRegex(retirement.Refusal, "destination is not absent"):
                retirement.preflight(root, census)
            self.assertTrue((root / "target/a.json").is_file())

    def test_atomic_no_replace_refuses_destination_race(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            custody = root / "audit/retired-v001"
            custody.mkdir(mode=0o700)
            (custody / retirement.EVENT_DIRECTORY_NAME).mkdir(mode=0o700)
            entry = census["entries"][0]
            target = retirement.destination(custody, entry)
            original_make_parents = retirement.make_parents_beneath

            def inject_destination_race(custody_path: Path, path: Path) -> None:
                original_make_parents(custody_path, path)
                path.write_bytes(b"hostile-preexisting-destination")

            retirement.make_parents_beneath = inject_destination_race
            try:
                with self.assertRaisesRegex(
                    retirement.Refusal, "retirement destination appeared",
                ):
                    retirement.move_entry(root, custody, entry, 1)
            finally:
                retirement.make_parents_beneath = original_make_parents
            self.assertEqual(target.read_bytes(), b"hostile-preexisting-destination")
            retirement.inspect_entry(root / "target/a.json", entry)

    def test_inode_substitution_is_refused_after_move(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            custody = root / "audit/retired-v001"
            custody.mkdir(mode=0o700)
            (custody / retirement.EVENT_DIRECTORY_NAME).mkdir(mode=0o700)
            entry = census["entries"][0]
            source = root / "target/a.json"
            target = retirement.destination(custody, entry)
            source_inode = os.stat(source, follow_symlinks=False).st_ino
            original_rename = retirement.rename_exclusive

            def substitute_inode(source_path: Path, target_path: Path) -> None:
                mode = os.stat(source_path, follow_symlinks=False).st_mode & 0o777
                target_path.write_bytes(source_path.read_bytes())
                target_path.chmod(mode)
                source_path.unlink()

            retirement.rename_exclusive = substitute_inode
            try:
                with self.assertRaisesRegex(
                    retirement.Refusal, "identity changed across rename",
                ):
                    retirement.move_entry(root, custody, entry, 1)
            finally:
                retirement.rename_exclusive = original_rename
            self.assertNotEqual(
                os.stat(target, follow_symlinks=False).st_ino, source_inode,
            )

    def test_injected_interruption_rolls_back_without_partial_retirement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            with self.assertRaisesRegex(retirement.Refusal, "failed and rolled back"):
                retirement.retire(root, census, inject_after=2)
            self.assert_sources_present(root, census)
            retirement.preflight(root, census)

    def test_restart_recovery_infers_moved_state_and_restores(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            retirement.preflight(root, census)
            custody = root / "audit/retired-v001"
            custody.mkdir(parents=True, mode=0o700)
            (custody / retirement.EVENT_DIRECTORY_NAME).mkdir(mode=0o700)
            intent = {
                "schema": "V012_OWNER_ONCE_RETIREMENT_INTENT_V001",
                "census_sha256": retirement.sha256_bytes(
                    retirement.publication_json_bytes(census)
                ),
                "paths": [entry["path"] for entry in census["entries"]],
                "entry_count": census["entry_count"],
                "source_file_count": census["source_file_count"],
                "source_total_bytes": census["source_total_bytes"],
            }
            retirement.publish_once(custody / retirement.INTENT_NAME, intent)
            retirement.move_entry(root, custody, census["entries"][0], 1)
            self.assertFalse((root / "target/a.json").exists())
            result = retirement.recover(root, census)
            self.assertEqual(result["restored_entry_count"], 1)
            self.assert_sources_present(root, census)

    def test_restart_recovery_removes_empty_pre_intent_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            custody = root / "audit/retired-v001"
            custody.mkdir(mode=0o700)
            result = retirement.recover(root, census)
            self.assertEqual(
                result["classification"],
                "PASS_EMPTY_INTERRUPTED_TRANSACTION_REMOVED",
            )
            self.assert_sources_present(root, census)

    def test_source_drift_refuses_before_any_move(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            (root / "target/a.json").chmod(0o644)
            with self.assertRaisesRegex(retirement.Refusal, "census mismatch"):
                retirement.preflight(root, census)
            self.assertFalse((root / "audit/retired-v001").exists())

    def test_synthetic_success_publishes_once_without_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            result = retirement.retire(root, census)
            self.assertEqual(result["classification"], "PASS_EXACT_OWNER_ONCE_RETIREMENT")
            custody = root / "audit/retired-v001"
            self.assertTrue((custody / retirement.RECEIPT_NAME).is_file())
            for entry in census["entries"]:
                source = root.joinpath(*retirement.PurePosixPath(entry["path"]).parts)
                self.assertFalse(retirement.path_exists(source))
                retirement.inspect_entry(retirement.destination(custody, entry), entry)
            with self.assertRaisesRegex(retirement.Refusal, "destination is not absent"):
                retirement.retire(root, census)

    def test_every_moved_payload_file_is_fsynced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census = self.make_fixture(root)
            payload_identities = {
                (
                    os.stat(path, follow_symlinks=False).st_dev,
                    os.stat(path, follow_symlinks=False).st_ino,
                )
                for path in root.rglob("*")
                if path.is_file() and not path.is_symlink()
            }
            fsynced_identities: set[tuple[int, int]] = set()
            original_fsync = retirement.os.fsync

            def record_fsync(descriptor: int) -> None:
                metadata = retirement.os.fstat(descriptor)
                fsynced_identities.add((metadata.st_dev, metadata.st_ino))
                original_fsync(descriptor)

            retirement.os.fsync = record_fsync
            try:
                result = retirement.retire(root, census)
            finally:
                retirement.os.fsync = original_fsync
            self.assertEqual(
                result["classification"], "PASS_EXACT_OWNER_ONCE_RETIREMENT",
            )
            self.assertTrue(payload_identities.issubset(fsynced_identities))


if __name__ == "__main__":
    unittest.main(verbosity=2)
