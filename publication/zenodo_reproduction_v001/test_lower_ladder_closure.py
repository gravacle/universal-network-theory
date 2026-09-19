#!/usr/bin/env python3
"""Tests for the standalone lower-ladder reproduction closure."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY_ROOT = HERE.parents[1]
MODULE_PATH = HERE / "lower_ladder_closure.py"
SPEC = HERE / "LOWER_LADDER_CLOSURE_SPEC.json"

module_spec = importlib.util.spec_from_file_location("lower_ladder_closure", MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
closure = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(closure)


class LowerLadderClosureTests(unittest.TestCase):
    def load_spec(self):
        return json.loads(SPEC.read_text(encoding="utf-8"))

    def test_checked_in_spec_and_public_projections_match_authenticated_sources(self):
        result = closure.verify_source(REPOSITORY_ROOT)
        self.assertEqual(result["status"], "VERIFIED_SOURCE_CLOSURE")
        self.assertEqual(result["member_count"], 34)
        self.assertEqual(result["expected_stdout"], closure.EXPECTED_STDOUT)

    def test_minimum_closure_preserves_original_relative_layout(self):
        spec = self.load_spec()
        members = spec["minimum_closure"]["members"]
        self.assertEqual(spec["minimum_closure"]["member_count"], 34)
        self.assertEqual(spec["minimum_closure"]["binary_member_count"], 30)
        self.assertEqual(sum(bool(item["binary"]) for item in members), 30)
        archives = {item["archive"] for item in members}
        prefix = f"{closure.ARCHIVE_PREFIX}/"
        self.assertTrue(all(path.startswith(prefix) for path in archives))
        self.assertIn(
            prefix
            + "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
            + "extract_lower_bound_progression.py",
            archives,
        )
        self.assertIn(
            prefix
            + "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/"
            + "L10/sharp/prefix_09/q_09.npy",
            archives,
        )

    def test_public_cache_manifests_are_minimal_path_neutral_projections(self):
        spec = self.load_spec()
        projections = {
            item["length"]: item
            for item in spec["minimum_closure"]["cache_manifest_projections"]
        }
        self.assertEqual(projections[8]["selected_file_count"], 8)
        self.assertEqual(projections[10]["selected_file_count"], 12)
        for length, expected_count in ((8, 8), (10, 12)):
            path = closure.PUBLIC_MANIFEST_PATHS[length]
            data = path.read_bytes()
            self.assertEqual(closure.leak_classes(data), [])
            payload = json.loads(data)
            self.assertEqual(payload["L"], length)
            self.assertEqual(len(payload["files"]), expected_count)
            self.assertEqual(
                payload["canonical_cache_root"], str(closure.cache_directory(length))
            )
            self.assertEqual(
                payload["public_projection"]["source_manifest_sha256"],
                projections[length]["source_sha256"],
            )

    def test_strong_path_cloud_operator_and_credential_leaks_are_detected(self):
        cases = (
            (b"/Users/example/private/file.json", "local_path"),
            (b"s3://private-bucket/key", "cloud_reference"),
            (b"arn:aws:iam::000000000000:role/example", "cloud_reference"),
            (b"AKIA" + b"ABCDEFGHIJKLMNOP", "credential"),
        )
        for data, expected in cases:
            with self.subTest(expected=expected):
                self.assertIn(expected, closure.leak_classes(data))
        source_manifest = json.loads(
            (
                REPOSITORY_ROOT
                / closure.source_manifest_path(8)
            ).read_text(encoding="utf-8")
        )
        path_parts = Path(source_manifest["canonical_cache_root"]).parts
        user_token = path_parts[path_parts.index("Users") + 1]
        self.assertIn(
            "operator_identifier", closure.leak_classes(user_token.encode("utf-8"))
        )

    def test_integration_contract_requires_explicit_binary_builder_support(self):
        integration = self.load_spec()["integration"]
        self.assertEqual(
            integration["allowed_suffix_additions"], [".i32", ".npy", ".u32"]
        )
        self.assertIn("binary=true", integration["integration_precondition"])
        self.assertIn("without UTF-8 decoding", integration["builder_capability_required"])
        binary_entries = [
            item for item in integration["manifest_entries"] if item["binary"]
        ]
        self.assertEqual(len(binary_entries), 30)
        self.assertTrue(all(not item["scan_release_markers"] for item in binary_entries))

    def test_materialized_original_layout_executes_and_reproduces_exact_values(self):
        with tempfile.TemporaryDirectory(prefix="wac-lower-ladder-") as temporary:
            capsule_root = Path(temporary)
            result = closure.materialize(REPOSITORY_ROOT, capsule_root, link=True)
            self.assertEqual(result["status"], "VERIFIED_EXTRACTED_LOWER_LADDER")
            self.assertEqual(result["stdout"], closure.EXPECTED_STDOUT)
            prefix = capsule_root / closure.ARCHIVE_PREFIX
            extra = prefix / "unexpected.txt"
            extra.write_text("unexpected\n", encoding="utf-8")
            with self.assertRaisesRegex(closure.Refusal, "member-set mismatch"):
                closure.verify_archive(capsule_root)
            extra.unlink()
            victim = capsule_root / closure.ARCHIVE_PREFIX / closure.EXTRACTOR
            original = victim.read_bytes()
            victim.unlink()
            victim.write_bytes(original + b"\n")
            with self.assertRaisesRegex(closure.Refusal, "authentication failed"):
                closure.verify_archive(capsule_root)


if __name__ == "__main__":
    unittest.main()
