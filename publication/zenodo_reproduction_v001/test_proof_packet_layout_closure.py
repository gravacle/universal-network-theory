#!/usr/bin/env python3
"""Focused tests for the original-layout proof-packet closure."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path, PurePosixPath


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "proof_packet_layout_closure.py"
SOURCE_LAYOUT = (HERE / "PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json").is_file()
if SOURCE_LAYOUT:
    REPOSITORY_ROOT = HERE.parents[1]
    SPEC_PATH = HERE / "PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
else:  # Packaged under tests/ with the tool under tools/ and spec under inventory/.
    REPOSITORY_ROOT = HERE.parent
    MODULE_PATH = HERE.parent / "tools" / "proof_packet_layout_closure.py"
    SPEC_PATH = HERE.parent / "inventory" / "PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"

module_spec = importlib.util.spec_from_file_location(
    "proof_packet_layout_closure", MODULE_PATH
)
assert module_spec is not None and module_spec.loader is not None
closure = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(closure)


class ProofPacketLayoutClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = None
        if SOURCE_LAYOUT:
            cls.temporary = tempfile.TemporaryDirectory(
                prefix="wac-proof-layout-tests-"
            )
            cls.archive = Path(cls.temporary.name) / "archive"
            cls.materialized = closure.materialize(
                REPOSITORY_ROOT, cls.archive, SPEC_PATH, run_portable=True
            )
        else:
            cls.archive = REPOSITORY_ROOT
            cls.materialized = closure.verify_archive(
                cls.archive, SPEC_PATH, run_portable=True
            )
        cls.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        cls.by_id = {row["id"]: row for row in cls.spec["packets"]}

    @classmethod
    def tearDownClass(cls):
        if cls.temporary is not None:
            cls.temporary.cleanup()

    def packet_root(self, packet_id: str) -> Path:
        return self.archive / self.by_id[packet_id]["archive_prefix"]

    def test_checked_spec_exactly_matches_all_revision_pinned_sources(self):
        if SOURCE_LAYOUT:
            result = closure.verify_source(REPOSITORY_ROOT, SPEC_PATH)
            self.assertEqual(
                result["status"], "VERIFIED_PINNED_PROOF_PACKET_SOURCE_CLOSURE"
            )
            self.assertEqual(result["packet_count"], 4)
        else:
            result = closure.verify_archive(
                REPOSITORY_ROOT, SPEC_PATH, run_portable=False
            )
            self.assertEqual(
                result["status"], "VERIFIED_EXTRACTED_PROOF_PACKET_LAYOUT"
            )
        self.assertEqual(result["member_count"], 58)
        self.assertEqual(self.spec["leakage_scan"]["finding_count"], 0)

    def test_archive_layout_preserves_complete_original_paths_and_basenames(self):
        for packet in self.spec["packets"]:
            prefix = PurePosixPath(packet["archive_prefix"])
            self.assertEqual(packet["member_count"], len(packet["members"]))
            for member in packet["members"]:
                original = PurePosixPath(member["path"])
                archive = PurePosixPath(member["archive_path"])
                self.assertEqual(archive, prefix / original)
                self.assertEqual(archive.name, original.name)
                self.assertRegex(member["sha256"], r"^[0-9a-f]{64}$")
                self.assertGreater(member["bytes"], 0)

    def test_alpha_packet_contains_target_manifest_and_every_declared_dependency(self):
        packet = self.by_id[closure.ALPHA_ID]
        packet_root = self.packet_root(closure.ALPHA_ID)
        manifest = json.loads((packet_root / closure.ALPHA_MANIFEST).read_text())
        frozen = json.loads((packet_root / closure.ALPHA_FROZEN).read_text())
        declared = {row["path"] for row in manifest["artifacts"]}
        declared.update(frozen["historical_hashes"])
        declared.update(str(path) for path in closure.ALPHA_FIXED_INPUTS)
        packaged = {row["path"] for row in packet["members"]}
        self.assertEqual(packaged, declared)
        self.assertEqual(packet["member_count"], 19)
        self.assertEqual(packet["source_revision"], closure.REVISIONS[closure.ALPHA_ID])

    def test_l4_packet_includes_both_bounded_repair_siblings(self):
        packet = self.by_id[closure.L4_ID]
        packaged = {row["path"] for row in packet["members"]}
        self.assertIn(
            "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/BOUNDED_BACKEND_REPAIR.md",
            packaged,
        )
        self.assertIn(
            "AUDIT_R_INTRINSIC_ADMISSION_PARENT_L4_V001/FROZEN_REPAIR.json",
            packaged,
        )
        self.assertEqual(packet["member_count"], 11)

    def test_l12_packet_includes_freezes_and_preserves_all_absence_predicates(self):
        packet = self.by_id[closure.L12_ID]
        packaged = {row["path"] for row in packet["members"]}
        self.assertIn(str(closure.L12_FROZEN), packaged)
        self.assertIn(str(closure.L12_FROZEN_V002), packaged)
        absences = {row["path"] for row in packet["absence_predicates"]}
        self.assertEqual(absences, {str(path) for path in closure.L12_ABSENCES})
        packet_root = self.packet_root(closure.L12_ID)
        self.assertTrue(all(not (packet_root / path).exists() for path in absences))

    def test_portable_verifiers_execute_in_disposable_trees_and_archive_stays_pristine(self):
        executions = {
            row["id"]: row for row in self.materialized["executed_portable_packets"]
        }
        self.assertEqual(
            set(executions), {closure.ALPHA_ID, closure.L4_ID, closure.L12_ID}
        )
        self.assertEqual(executions[closure.ALPHA_ID]["checks_passed"], 300)
        self.assertEqual(executions[closure.L4_ID]["checks_passed"], 50)
        self.assertEqual(executions[closure.L12_ID]["checks_passed"], 40)
        for packet_id in (closure.L4_ID, closure.L12_ID):
            for output in self.by_id[packet_id]["outputs_written"]:
                self.assertFalse((self.packet_root(packet_id) / output["path"]).exists())
        second = closure.verify_archive(self.archive, SPEC_PATH, run_portable=True)
        self.assertEqual(
            second["status"],
            "VERIFIED_EXTRACTED_PROOF_PACKET_LAYOUT_AND_PORTABLE_GATES",
        )

    def test_streamed_preflight_is_authenticated_inventory_never_a_portable_pass(self):
        packet = self.by_id[closure.STREAMED_ID]
        self.assertFalse(packet["portable_capsule_gate"])
        self.assertEqual(
            packet["classification"],
            "ENVIRONMENT_DEPENDENT_HISTORICAL_PREFLIGHT_INVENTORY_ONLY",
        )
        self.assertEqual(
            packet["execution"]["mode"],
            "DO_NOT_EXECUTE_AS_A_PORTABLE_CAPSULE_GATE",
        )
        self.assertIn("disk_usage", packet["nonportable_reason"])
        self.assertEqual(
            self.materialized["inventory_only_packets"], [closure.STREAMED_ID]
        )
        output = packet["outputs_written"][0]["path"]
        self.assertFalse((self.packet_root(closure.STREAMED_ID) / output).exists())

    def test_mutation_missing_member_and_absence_violation_fail_closed(self):
        if not SOURCE_LAYOUT:
            self.skipTest("repository-focused mutation copies are not run after extraction")
        with tempfile.TemporaryDirectory(prefix="wac-proof-mutations-") as temporary:
            mutation_root = Path(temporary) / "archive"
            shutil.copytree(self.archive, mutation_root)
            alpha_member = self.by_id[closure.ALPHA_ID]["members"][0]
            alpha_path = mutation_root / alpha_member["archive_path"]
            alpha_path.write_bytes(alpha_path.read_bytes() + b"\n")
            with self.assertRaisesRegex(closure.Refusal, "authentication failed"):
                closure.verify_archive(mutation_root, SPEC_PATH, run_portable=False)

        with tempfile.TemporaryDirectory(prefix="wac-proof-missing-") as temporary:
            missing_root = Path(temporary) / "archive"
            shutil.copytree(self.archive, missing_root)
            l4_member = self.by_id[closure.L4_ID]["members"][0]
            (missing_root / l4_member["archive_path"]).unlink()
            with self.assertRaisesRegex(closure.Refusal, "member-set mismatch"):
                closure.verify_archive(missing_root, SPEC_PATH, run_portable=False)

        with tempfile.TemporaryDirectory(prefix="wac-proof-absence-") as temporary:
            absence_root = Path(temporary) / "archive"
            shutil.copytree(self.archive, absence_root)
            packet_root = (
                absence_root / self.by_id[closure.L12_ID]["archive_prefix"]
            )
            prohibited = packet_root / self.by_id[closure.L12_ID][
                "absence_predicates"
            ][0]["path"]
            prohibited.parent.mkdir(parents=True, exist_ok=True)
            prohibited.write_text("must remain absent\n", encoding="utf-8")
            with self.assertRaisesRegex(closure.Refusal, "member-set mismatch"):
                closure.verify_archive(absence_root, SPEC_PATH, run_portable=False)

    def test_private_raw_l12_release_artifacts_are_out_of_scope(self):
        boundary = self.spec["private_l12_release_evidence"]
        self.assertIn("NO_PRIVATE_RAW_L12_ARTIFACT_IS_INCLUDED_HERE", boundary)
        all_paths = {
            row["path"]
            for packet in self.spec["packets"]
            for row in packet["members"]
        }
        self.assertFalse(
            any("TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012" in path for path in all_paths)
        )

    def test_leakage_scan_rejects_sensitive_release_markers(self):
        cases = {
            (b"/" + b"Users" + b"/example/private.json"): "local_path",
            (b"s3" + b"://private-bucket/key"): "cloud_reference",
            (b"AK" + b"IAABCDEFGHIJKLMNOP"): "credential",
            (b"operator" + b"@example.org"): "email",
        }
        for sample, expected in cases.items():
            with self.subTest(expected=expected):
                self.assertIn(expected, closure.leakage_classes(sample))


if __name__ == "__main__":
    unittest.main()
