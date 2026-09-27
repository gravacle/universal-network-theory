#!/usr/bin/env python3
"""Focused path/JSON/baseline refusal tests; never edit real review evidence."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import verify_review as review
import build_review_seal as builder


class ReviewCustodyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.root_patch = mock.patch.object(review, "ROOT", self.root)
        self.root_patch.start()
        (self.root / "plain.txt").write_bytes(b"authenticated bytes\n")

    def tearDown(self):
        self.root_patch.stop()
        self.temporary.cleanup()

    def test_regular_file_is_admitted(self):
        self.assertEqual(review.safe_file("plain.txt"), self.root / "plain.txt")

    def test_absolute_traversal_and_noncanonical_routes_refused(self):
        for route in ("", "/tmp/x", "../plain.txt", "a/../plain.txt", "./plain.txt",
                      "a//plain.txt", "a\\plain.txt"):
            with self.subTest(route=route), self.assertRaises(ValueError):
                review.safe_file(route)

    def test_leaf_symlink_refused(self):
        (self.root / "alias.txt").symlink_to(self.root / "plain.txt")
        with self.assertRaises(ValueError):
            review.safe_file("alias.txt")

    def test_parent_symlink_refused(self):
        (self.root / "nested").mkdir()
        (self.root / "nested" / "plain.txt").write_bytes(b"x")
        (self.root / "alias").symlink_to(self.root / "nested")
        with self.assertRaises(ValueError):
            review.safe_file("alias/plain.txt")

    def test_missing_or_directory_refused(self):
        (self.root / "directory").mkdir()
        for route in ("missing", "directory"):
            with self.subTest(route=route), self.assertRaises(ValueError):
                review.safe_file(route)

    def test_duplicate_json_keys_refused(self):
        path = self.root / "duplicate.json"
        path.write_text('{"a":1,"a":2}')
        with self.assertRaises(ValueError):
            review.load(path)

    def test_nonfinite_json_refused(self):
        path = self.root / "nonfinite.json"
        for value in ("NaN", "Infinity", "-Infinity"):
            path.write_text('{"a":' + value + '}')
            with self.subTest(value=value), self.assertRaises(ValueError):
                review.load(path)

    def test_baseline_bytes_authenticate_and_mutation_refuses(self):
        raw = (self.root / "plain.txt").read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        entry = b"100644 blob " + blob.encode() + b"\tplain.txt\0"
        def git(*arguments):
            if arguments == ("rev-parse", review.BASE + "^{tree}"):
                return review.TREE.encode() + b"\n"
            if arguments == ("ls-tree", "-rz", review.BASE):
                return entry
            raise AssertionError("unexpected git call: " + repr(arguments))
        with mock.patch.object(review, "git", side_effect=git):
            self.assertEqual(review.verify_baseline(), 1)
            (self.root / "plain.txt").write_bytes(b"changed bytes\n")
            with self.assertRaises(ValueError):
                review.verify_baseline()

    def seal_fixture(self):
        raw = (self.root / "plain.txt").read_bytes()
        return {"schema": "UNT_PROGRAM_REVIEW_SEAL_V001",
                "baseline_commit": review.BASE, "baseline_tree": review.TREE,
                "meaning": "Test byte custody only",
                "artifacts": [{"path": "plain.txt", "bytes": len(raw), "sha256": review.sha(raw)}]}

    def test_exact_seal_census_accepts_and_missing_member_refuses(self):
        seal = self.seal_fixture()
        with mock.patch.object(review, "SCOPES", ["plain.txt"]):
            self.assertEqual(review.verify_seal(seal), {"plain.txt"})
            seal["artifacts"] = []
            with self.assertRaises(ValueError):
                review.verify_seal(seal)

    def test_unlisted_new_file_and_out_of_scope_member_refuse(self):
        packet = self.root / "packet"
        packet.mkdir()
        (packet / "first.txt").write_bytes(b"first")
        seal = self.seal_fixture()
        seal["artifacts"] = [{"path": "packet/first.txt", "bytes": 5,
                              "sha256": review.sha(b"first")}]
        with mock.patch.object(review, "SCOPES", ["packet"]), mock.patch.object(review, "PACKET", packet):
            review.verify_seal(seal)
            (packet / "unlisted.txt").write_bytes(b"new")
            with self.assertRaises(ValueError):
                review.verify_seal(seal)
        with mock.patch.object(review, "SCOPES", ["plain.txt"]):
            seal = self.seal_fixture()
            seal["artifacts"].append({"path": "packet/first.txt", "bytes": 5,
                                      "sha256": review.sha(b"first")})
            with self.assertRaises(ValueError):
                review.verify_seal(seal)

    def test_duplicate_artifact_and_wrong_identity_refuse(self):
        with mock.patch.object(review, "SCOPES", ["plain.txt"]):
            seal = self.seal_fixture()
            seal["artifacts"].append(copy.deepcopy(seal["artifacts"][0]))
            with self.assertRaises(ValueError):
                review.verify_seal(seal)
            for field in ("schema", "baseline_commit", "baseline_tree"):
                seal = self.seal_fixture()
                seal[field] = "wrong"
                with self.subTest(field=field), self.assertRaises(ValueError):
                    review.verify_seal(seal)

    def test_artifact_hash_length_and_content_mutation_refuse(self):
        with mock.patch.object(review, "SCOPES", ["plain.txt"]):
            for field, value in (("bytes", 1), ("sha256", "0" * 64)):
                seal = self.seal_fixture()
                seal["artifacts"][0][field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    review.verify_seal(seal)
            seal = self.seal_fixture()
            (self.root / "plain.txt").write_bytes(b"new bytes")
            with self.assertRaises(ValueError):
                review.verify_seal(seal)

    def test_artifact_scope_overlap_and_symlink_refuse(self):
        with mock.patch.object(review, "SCOPES", ["plain.txt", "plain.txt"]):
            with self.assertRaises(ValueError):
                review.artifact_paths()
        (self.root / "scope_alias").symlink_to(self.root / "plain.txt")
        with mock.patch.object(review, "SCOPES", ["scope_alias"]):
            with self.assertRaises(ValueError):
                review.artifact_paths()

    def test_safe_destination_accepts_missing_leaf_and_refuses_symlinks(self):
        self.assertEqual(review.safe_destination("new.json"), self.root / "new.json")
        (self.root / "alias.json").symlink_to(self.root / "plain.txt")
        with self.assertRaises(ValueError):
            review.safe_destination("alias.json")
        with self.assertRaises(ValueError):
            review.safe_destination("../outside.json")

    def test_builder_atomic_publication_no_overwrite_and_explicit_replace(self):
        path = self.root / "new.json"
        with mock.patch.object(builder, "ROOT", self.root):
            builder.publish_json(path, {"version": 1})
            with self.assertRaises(FileExistsError):
                builder.publish_json(path, {"version": 2})
            self.assertEqual(json.loads(path.read_text()), {"version": 1})
            builder.publish_json(path, {"version": 2}, replace=True)
            self.assertEqual(json.loads(path.read_text()), {"version": 2})
        self.assertEqual(list(self.root.glob(".review-draft-*")), [])

    def test_builder_symlink_target_parent_and_outside_root_refused(self):
        (self.root / "alias.json").symlink_to(self.root / "plain.txt")
        (self.root / "nested").mkdir()
        (self.root / "alias_dir").symlink_to(self.root / "nested")
        original = (self.root / "plain.txt").read_bytes()
        with mock.patch.object(builder, "ROOT", self.root):
            for path in (self.root / "alias.json", self.root / "alias_dir" / "new.json",
                         self.root.parent / "outside-review.json"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    builder.publish_json(path, {"bad": True}, replace=True)
        self.assertEqual((self.root / "plain.txt").read_bytes(), original)
        self.assertEqual(list(self.root.glob(".review-draft-*")), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
