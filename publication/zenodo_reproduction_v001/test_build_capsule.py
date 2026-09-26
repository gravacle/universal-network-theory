#!/usr/bin/env python3
"""Focused safety tests for the deterministic capsule builder."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile

try:
    from publication.zenodo_reproduction_v001 import build_capsule as capsule
except ImportError:  # Supports execution after extraction under tools/.
    import build_capsule as capsule


PLACEHOLDERS = [
    "GIT_COMMIT",
    "GIT_TAG",
    "CONTENT_LICENSE_SPDX",
    "RELEASE_DATE",
    "RELEASE_VERSION",
    "SOFTWARE_LICENSE_SPDX",
    "ZENODO_DOI",
]

PATTERNS = {
    "GIT_COMMIT": r"[0-9a-f]{40}",
    "GIT_TAG": r"[A-Za-z0-9][A-Za-z0-9._/-]{0,127}",
    "CONTENT_LICENSE_SPDX": r"CC-BY-4\.0",
    "RELEASE_DATE": r"[0-9]{4}-[0-9]{2}-[0-9]{2}",
    "RELEASE_VERSION": r"[A-Za-z0-9][A-Za-z0-9._+-]{0,79}",
    "SOFTWARE_LICENSE_SPDX": r"Apache-2\.0",
    "ZENODO_DOI": r"10\.[0-9]{4,9}/[-._;()/:A-Za-z0-9]+",
}

VALUES = {
    "GIT_COMMIT": "a" * 40,
    "GIT_TAG": "reproduction-v1.0.0",
    "CONTENT_LICENSE_SPDX": "CC-BY-4.0",
    "RELEASE_DATE": "2026-09-15",
    "RELEASE_VERSION": "v1.0.0",
    "SOFTWARE_LICENSE_SPDX": "Apache-2.0",
    "ZENODO_DOI": "10.5281/zenodo.1234568",
}


class CapsuleBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.manifest_path = self.root / "manifest.json"
        self.values_path = self.root / "values.json"
        self.values_path.write_text(json.dumps(VALUES), encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def manifest(self, entries: list[dict], **overrides: object) -> dict:
        value = {
            "schema_version": 1,
            "capsule_name": "test-capsule",
            "archive_root": "test-capsule",
            "max_file_bytes": 1024,
            "max_total_bytes": 4096,
            "allowed_source_suffixes": [".txt"],
            "allowed_archive_suffixes": [".txt"],
            "release_placeholders": PLACEHOLDERS,
            "release_value_patterns": PATTERNS,
            "release_forbidden_markers": ["RELEASE-BLOCKER:TEST"],
            "authenticated_urm_validator_closure": None,
            "authenticated_proof_packet_layout_closure": None,
            "entries": entries,
        }
        value.update(overrides)
        self.manifest_path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return value

    def plan(self, *, release: bool = False) -> capsule.CapsulePlan:
        return capsule.prepare_plan(
            self.manifest_path,
            self.root,
            release=release,
            values_path=self.values_path if release else None,
        )

    def test_missing_required_file_fails(self) -> None:
        self.manifest([{"source": "missing.txt", "archive": "missing.txt"}])
        with self.assertRaisesRegex(capsule.CapsuleError, "missing preparation-required"):
            self.plan()

    def test_optional_preparation_file_becomes_release_required(self) -> None:
        self.manifest(
            [
                {
                    "source": "pending.txt",
                    "archive": "pending.txt",
                    "required": False,
                    "release_required": True,
                }
            ]
        )
        preparation = self.plan()
        self.assertEqual(preparation.pending, ("pending.txt",))
        with self.assertRaisesRegex(capsule.CapsuleError, "missing release-required"):
            self.plan(release=True)

    def test_parent_traversal_fails(self) -> None:
        self.manifest([{"source": "../outside.txt", "archive": "outside.txt"}])
        with self.assertRaisesRegex(capsule.CapsuleError, "not a normalized relative path"):
            self.plan()

    def test_windows_drive_style_path_fails(self) -> None:
        self.manifest([{"source": "C:/outside.txt", "archive": "outside.txt"}])
        with self.assertRaisesRegex(capsule.CapsuleError, "unsafe on common extraction"):
            self.plan()

    def test_symlink_source_fails(self) -> None:
        target = self.root / "target.txt"
        target.write_text("target", encoding="utf-8")
        link = self.root / "link.txt"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        self.manifest([{"source": "link.txt", "archive": "link.txt"}])
        with self.assertRaisesRegex(capsule.CapsuleError, "symlink forbidden"):
            self.plan()

    def test_casefolded_duplicate_archive_path_fails(self) -> None:
        (self.root / "one.txt").write_text("one", encoding="utf-8")
        (self.root / "two.txt").write_text("two", encoding="utf-8")
        self.manifest(
            [
                {"source": "one.txt", "archive": "Evidence.txt"},
                {"source": "two.txt", "archive": "evidence.txt"},
            ]
        )
        with self.assertRaisesRegex(capsule.CapsuleError, "duplicate/colliding archive"):
            self.plan()

    def test_same_source_may_be_archived_twice_at_distinct_paths(self) -> None:
        (self.root / "one.txt").write_text("one", encoding="utf-8")
        self.manifest(
            [
                {"source": "one.txt", "archive": "first.txt"},
                {"source": "one.txt", "archive": "second.txt"},
            ]
        )
        plan = self.plan()
        self.assertEqual([item.archive for item in plan.files], ["first.txt", "second.txt"])

    def test_binary_entry_is_byte_exact_without_utf8_decoding(self) -> None:
        payload = b"\xff\x00\x80binary\x00payload"
        (self.root / "array.bin").write_bytes(payload)
        self.manifest(
            [
                {
                    "source": "array.bin",
                    "archive": "data/array.bin",
                    "binary": True,
                    "scan_release_markers": False,
                }
            ],
            allowed_source_suffixes=[".bin"],
            allowed_archive_suffixes=[".bin"],
        )
        plan = self.plan(release=True)
        self.assertEqual(plan.files[0].data, payload)

    def test_binary_entry_may_not_be_a_template(self) -> None:
        (self.root / "array.txt").write_bytes(b"binary")
        self.manifest(
            [
                {
                    "source": "array.txt",
                    "archive": "array.txt",
                    "binary": True,
                    "template": True,
                    "scan_release_markers": False,
                }
            ]
        )
        with self.assertRaisesRegex(capsule.CapsuleError, "may not be a template"):
            self.plan()

    def test_binary_entry_must_explicitly_disable_text_marker_scan(self) -> None:
        (self.root / "array.txt").write_bytes(b"binary")
        self.manifest(
            [{"source": "array.txt", "archive": "array.txt", "binary": True}]
        )
        with self.assertRaisesRegex(capsule.CapsuleError, "must set scan_release_markers"):
            self.plan()

    def test_nonbinary_entry_remains_utf8_enforced_when_marker_scan_is_disabled(self) -> None:
        (self.root / "text.txt").write_bytes(b"\xff")
        self.manifest(
            [
                {
                    "source": "text.txt",
                    "archive": "text.txt",
                    "scan_release_markers": False,
                }
            ]
        )
        with self.assertRaisesRegex(capsule.CapsuleError, "not UTF-8 text"):
            self.plan()

    def test_oversized_file_fails(self) -> None:
        (self.root / "large.txt").write_text("four", encoding="utf-8")
        self.manifest(
            [{"source": "large.txt", "archive": "large.txt"}],
            max_file_bytes=3,
            max_total_bytes=10,
        )
        with self.assertRaisesRegex(capsule.CapsuleError, "exceeds max_file_bytes"):
            self.plan()

    def test_unresolved_release_placeholder_fails(self) -> None:
        unresolved = "@" * 2 + "UNDECLARED_VALUE" + "@" * 2 + "\n"
        (self.root / "input.txt").write_text(unresolved, encoding="utf-8")
        self.manifest([{"source": "input.txt", "archive": "input.txt"}])
        with self.assertRaisesRegex(capsule.CapsuleError, "unresolved release placeholders"):
            self.plan(release=True)

    def test_release_blocker_marker_fails(self) -> None:
        (self.root / "input.txt").write_text("RELEASE-BLOCKER:TEST\n", encoding="utf-8")
        self.manifest([{"source": "input.txt", "archive": "input.txt"}])
        with self.assertRaisesRegex(capsule.CapsuleError, "release blocker marker"):
            self.plan(release=True)

    def test_approved_dual_license_ids_are_fixed(self) -> None:
        values = dict(VALUES)
        values["SOFTWARE_LICENSE_SPDX"] = "MIT"
        self.values_path.write_text(json.dumps(values), encoding="utf-8")
        (self.root / "input.txt").write_text("licensed\n", encoding="utf-8")
        self.manifest([{"source": "input.txt", "archive": "input.txt"}])
        with self.assertRaisesRegex(
            capsule.CapsuleError,
            "release value SOFTWARE_LICENSE_SPDX does not match",
        ):
            self.plan(release=True)

    def test_version_doi_must_match_doi_syntax(self) -> None:
        values = dict(VALUES)
        values["ZENODO_DOI"] = "zenodo-not-a-doi"
        self.values_path.write_text(json.dumps(values), encoding="utf-8")
        (self.root / "input.txt").write_text("safe\n", encoding="utf-8")
        self.manifest([{"source": "input.txt", "archive": "input.txt"}])
        with self.assertRaisesRegex(
            capsule.CapsuleError,
            "release value ZENODO_DOI does not match",
        ):
            self.plan(release=True)

    def test_real_user_home_path_fails_after_preparation(self) -> None:
        source = self.root / "private.txt"
        private_path = "/Users/" + "researcher/private/cache"
        source.write_text(f"workstation={private_path}\n", encoding="utf-8")
        self.manifest([{"source": "private.txt", "archive": "private.txt"}])
        with self.assertRaisesRegex(capsule.CapsuleError, "private path leak"):
            self.plan()

    def test_dynamic_private_temp_path_fails_final_scan(self) -> None:
        dynamic = capsule.PreparedFile(
            "<dynamic>",
            "dynamic.txt",
            b"scratch=/private/tmp/" + b"claude-review/private.json\n",
        )
        with self.assertRaisesRegex(capsule.CapsuleError, "private path leak"):
            capsule._scan_prepared_private_paths([dynamic])

    def test_release_template_is_resolved(self) -> None:
        commit_token = "@" * 2 + "GIT_COMMIT" + "@" * 2
        tag_token = "@" * 2 + "GIT_TAG" + "@" * 2
        (self.root / "template.txt").write_text(
            f"commit={commit_token} tag={tag_token}\n", encoding="utf-8"
        )
        self.manifest(
            [
                {
                    "source": "template.txt",
                    "archive": "rendered.txt",
                    "template": True,
                }
            ]
        )
        plan = self.plan(release=True)
        self.assertIn(VALUES["GIT_COMMIT"].encode("ascii"), plan.files[0].data)
        self.assertNotIn(b"@@", plan.files[0].data)

    def test_build_is_deterministic_and_verifiable(self) -> None:
        (self.root / "input.txt").write_text("deterministic\n", encoding="utf-8")
        self.manifest([{"source": "input.txt", "archive": "input.txt"}])
        plan = self.plan()
        first = self.root / "first.zip"
        second = self.root / "second.zip"
        first_digest = capsule.build_archive(plan, first)
        second_digest = capsule.build_archive(plan, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(first_digest, second_digest)
        self.assertEqual(capsule.verify_archive(plan, first), first_digest)

    def test_verify_rejects_extra_archive_member(self) -> None:
        (self.root / "input.txt").write_text("deterministic\n", encoding="utf-8")
        self.manifest([{"source": "input.txt", "archive": "input.txt"}])
        plan = self.plan()
        archive_path = self.root / "extra.zip"
        capsule.build_archive(plan, archive_path)
        info = zipfile.ZipInfo("test-capsule/extra.txt", date_time=capsule.FIXED_ZIP_TIME)
        info.compress_type = zipfile.ZIP_STORED
        info.create_system = 3
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        with zipfile.ZipFile(archive_path, mode="a") as archive:
            archive.writestr(info, b"extra\n")
        with self.assertRaisesRegex(capsule.CapsuleError, "ZIP member set differs"):
            capsule.verify_archive(plan, archive_path)

    def test_builder_refuses_to_overwrite(self) -> None:
        (self.root / "input.txt").write_text("deterministic\n", encoding="utf-8")
        self.manifest([{"source": "input.txt", "archive": "input.txt"}])
        plan = self.plan()
        output = self.root / "existing.zip"
        output.write_bytes(b"existing")
        with self.assertRaisesRegex(capsule.CapsuleError, "refusing to overwrite"):
            capsule.build_archive(plan, output)


class ActualCapsuleIntegrationTests(unittest.TestCase):
    def test_extracted_l4_l12_core_proof_path(self) -> None:
        repository_root = Path(__file__).resolve().parents[2]
        manifest_path = (
            repository_root
            / "publication"
            / "zenodo_reproduction_v001"
            / "capsule_manifest.json"
        )
        verifier_source = (
            repository_root
            / "publication"
            / "zenodo_reproduction_v001"
            / "verify_extracted_capsule.py"
        )
        if not manifest_path.is_file() or not verifier_source.is_file():
            self.skipTest("repository integration sources are not present")

        plan = capsule.prepare_plan(
            manifest_path,
            repository_root,
            release=False,
            values_path=None,
        )
        by_archive = {item.archive: item for item in plan.files}
        self.assertFalse(
            any(
                path.startswith(("proof/L14/", "DEVELOPMENT_R_L14_TARGETED_SCOUT_"))
                for path in by_archive
            )
        )
        self.assertFalse(
            any(
                path.startswith(
                    ("proof/L12/stage6/", "proof/L12/stage6r3/", "proof/L12/record_flow/")
                )
                for path in by_archive
            )
        )
        self.assertNotIn(
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/"
            "STAGE6R4_THEOREM_PATH_SPEC.md",
            by_archive,
        )
        theorem = "L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md"
        audit = "AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md"
        self.assertEqual(
            hashlib.sha256(by_archive[theorem].data).hexdigest(),
            "2439e1c36a053fccd57155a858d666f9ecbe0e46ded0a79f3ec3b86cb473f5cc",
        )
        self.assertEqual(
            hashlib.sha256(by_archive[audit].data).hexdigest(),
            "d2404e7503117b3fbdd97220824f2155b45b2cc5b7f2c8e577d86abeb00d6ffd",
        )
        core_paths = {
            "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md",
            "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.docx",
            "UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.md",
            "UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.docx",
            "ARGER_GATE_ADOPTION_2026-09-16.md",
            "UNIVERSAL_NETWORK_THEORY_ARCHITECTURE_V001.md",
            "DEVELOPMENT_R_ARGER_GATE_V001/arger_gate.py",
            "DEVELOPMENT_R_ARGER_GATE_V001/test_arger_gate.py",
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/CONDITIONAL_Z1_BRIDGE_THEOREM.md",
            "DEVELOPMENT_R_L12_Z1_LUTTINGER_CROSSCHECK_V001/INTERNAL_Z1_THEOREM_ROUTE.md",
            "urm/URM_VALIDATION_CURRENT_2026-09-16.md",
            "alpha/LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/ALTERNATIVE_RECORD_WORLD.md",
            "alpha/LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/verify_alpha_sector_inheritance.py",
        }
        self.assertTrue(core_paths <= set(by_archive))
        self.assertTrue(
            by_archive["UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.docx"].data.startswith(
                b"PK\x03\x04"
            )
        )
        self.assertTrue(
            by_archive["UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.docx"].data.startswith(
                b"PK\x03\x04"
            )
        )
        for retired_navigation in ("PROOF_GUIDE.md", "HISTORY_AND_SCOPE.md"):
            self.assertNotIn(retired_navigation, by_archive)
        retired_framing = re.compile(
            r"stage[ _-]?6|record[ _-]?flow|atomwise classifier|"
            r"earlier classifier|old classifier|equivalence",
            re.IGNORECASE,
        )
        for archive_path in (
            "README.md",
            "UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.md",
            "PUBLICATION_CLAIM_MAP.tsv",
        ):
            text = by_archive[archive_path].data.decode("utf-8")
            self.assertIsNone(
                retired_framing.search(text),
                f"retired framing leaked into governing public surface {archive_path}",
            )
        self.assertFalse(any(path.startswith("runtime/") for path in by_archive))
        for unclosed_validator in (
            "urm/model/validate_urm.py",
            "urm/model/validate_alpha_role.py",
            "urm/model/validate_gravity_formation_theory.py",
            "urm/model/validate_gravity_microscopic_progress.py",
        ):
            self.assertNotIn(unclosed_validator, by_archive)
        lower_spec = json.loads(
            (
                repository_root
                / "publication"
                / "zenodo_reproduction_v001"
                / "LOWER_LADDER_CLOSURE_SPEC.json"
            ).read_text(encoding="utf-8")
        )
        lower_members = lower_spec["minimum_closure"]["members"]
        self.assertEqual(len(lower_members), 34)
        for member in lower_members:
            self.assertIn(member["archive"], by_archive)
            self.assertEqual(len(by_archive[member["archive"]].data), member["bytes"])
            self.assertEqual(
                hashlib.sha256(by_archive[member["archive"]].data).hexdigest(),
                member["sha256"],
            )
        proof_spec_path = (
            repository_root
            / "publication"
            / "zenodo_reproduction_v001"
            / "PROOF_PACKET_LAYOUT_CLOSURE_SPEC.json"
        )
        proof_spec = json.loads(proof_spec_path.read_text(encoding="utf-8"))
        self.assertEqual(proof_spec["member_count"], 58)
        self.assertEqual(proof_spec["total_bytes"], 1_649_218)
        self.assertEqual(
            hashlib.sha256(proof_spec_path.read_bytes()).hexdigest(),
            "51e9b760a2c5147b26bc801479a612acf45765c2c177eaf8683d419b21ae8515",
        )
        proof_packet_ids = {packet["id"] for packet in proof_spec["packets"]}
        self.assertEqual(
            proof_packet_ids,
            {
                "alpha_allow_require_scope_repair_v001",
                "l04_intrinsic_admission_final_hostile_v001",
                "l12_prefix_lineage_final_audit_v001",
                "l04_l10_streamed_preflight_inventory_v001",
            },
        )
        for packet in proof_spec["packets"]:
            if packet["id"] == "l04_l10_streamed_preflight_inventory_v001":
                self.assertFalse(packet["portable_capsule_gate"])
                self.assertEqual(
                    packet["classification"],
                    "ENVIRONMENT_DEPENDENT_HISTORICAL_PREFLIGHT_INVENTORY_ONLY",
                )
            else:
                self.assertTrue(packet["portable_capsule_gate"])
            for member in packet["members"]:
                self.assertIn(member["archive_path"], by_archive)
                self.assertEqual(
                    len(by_archive[member["archive_path"]].data), member["bytes"]
                )
                self.assertEqual(
                    hashlib.sha256(by_archive[member["archive_path"]].data).hexdigest(),
                    member["sha256"],
                )
            for output in packet["outputs_written"]:
                if "sha256" in output:
                    generated_archive = (
                        f"{packet['archive_prefix']}/{output['path']}"
                    )
                    self.assertNotIn(generated_archive, by_archive)
        lineage_diagnostic = "evidence/STRICT_COMMON_LINEAGE_PROGRESSION_V001.json"
        self.assertIn(lineage_diagnostic, by_archive)
        self.assertEqual(
            hashlib.sha256(by_archive[lineage_diagnostic].data).hexdigest(),
            "7076440b3c36eae95df8a276ce9494d5c8e0d82715e00e9f790b961278d2e35a",
        )
        urm_spec_path = (
            repository_root
            / "publication"
            / "zenodo_reproduction_v001"
            / "urm_validator_dependency_closure.json"
        )
        urm_spec = json.loads(urm_spec_path.read_text(encoding="utf-8"))
        self.assertEqual(urm_spec["closure_entry_count"], 68)
        self.assertEqual(urm_spec["closure_total_bytes"], 164003971)
        self.assertEqual(
            [row["id"] for row in urm_spec["validators"]],
            ["relational_accumulation"],
        )
        private_paths = {
            conflict["exact_repository_path"]
            for conflict in urm_spec["sanitized_conflicts"]
        }
        self.assertEqual(
            private_paths,
            {
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                "CACHE_PAYLOADS_V012/L8/CACHE_MANIFEST.json",
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                "CACHE_PAYLOADS_V012/L10/CACHE_MANIFEST.json",
                "model/relational_accumulation.py",
            },
        )
        self.assertEqual(urm_spec["sanitized_conflict_count"], 3)
        for row in urm_spec["entries"]:
            if row["repository_path"] in private_paths:
                self.assertIn(row["archive_path"], by_archive)
                self.assertNotEqual(
                    hashlib.sha256(by_archive[row["archive_path"]].data).hexdigest(),
                    row["sha256"],
                )
                continue
            self.assertIn(row["archive_path"], by_archive)
            self.assertEqual(len(by_archive[row["archive_path"]].data), row["size_bytes"])
            self.assertEqual(
                hashlib.sha256(by_archive[row["archive_path"]].data).hexdigest(),
                row["sha256"],
            )
        for conflict in urm_spec["sanitized_conflicts"]:
            public_archive = conflict["existing_public_archive_path"]
            self.assertIn(public_archive, by_archive)
            self.assertEqual(
                hashlib.sha256(by_archive[public_archive].data).hexdigest(),
                conflict["public_substitute_sha256"],
            )
            self.assertNotEqual(
                hashlib.sha256(by_archive[public_archive].data).hexdigest(),
                conflict["exact_sha256"],
            )
        for length, raw_sha in (
            (8, "d33ea5911dacf8c33aebe9f88f85d5ea8db754221fee5f80d4c2d440009e5ade"),
            (10, "80f52efaa4b455c7d68f4abef4b413a65c5a81633ec25f30c87fbbb4f2b3e743"),
        ):
            archive_path = (
                "urm/DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                f"CACHE_PAYLOADS_V012/L{length}/CACHE_MANIFEST.json"
            )
            projected = json.loads(by_archive[archive_path].data.decode("utf-8"))
            self.assertEqual(
                projected["public_projection"]["source_manifest_sha256"], raw_sha
            )
            self.assertNotIn(b"/Users/", by_archive[archive_path].data)
        self.assertEqual(
            hashlib.sha256(
                by_archive["urm/model/relational_accumulation_exact.py"].data
            ).hexdigest(),
            "d04ebd84c7dc98bd9d6aafae6c97aaf6430e994797138762be2cc87dcfb8bba4",
        )
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            archive_path = temporary_root / "capsule.zip"
            capsule.build_archive(plan, archive_path)
            capsule.verify_archive(plan, archive_path)
            extracted = temporary_root / "extracted"
            with zipfile.ZipFile(archive_path, "r") as archive:
                archive.extractall(extracted)
            capsule_root = extracted / plan.manifest["archive_root"]
            completed = subprocess.run(
                [
                    sys.executable,
                    str(capsule_root / "tools" / "verify_extracted_capsule.py"),
                    str(capsule_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                completed.returncode,
                0,
                msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
            )
            self.assertIn("EXTRACTED_CAPSULE_OK", completed.stdout)
            self.assertIn("core_proof_hashes=15", completed.stdout)
            self.assertIn("completed_proof_results=11", completed.stdout)
            self.assertIn("urm_status_markers=7", completed.stdout)
            self.assertIn(
                "arger_l12_block_mass=0.56956498393327842", completed.stdout
            )
            self.assertIn(
                "arger_minimum_visibility=0.4280947078156539", completed.stdout
            )
            self.assertIn("arger_gate=ADOPTED_FINITE_BLOCK_Z1", completed.stdout)
            self.assertIn("lower_ladder_members=34", completed.stdout)
            self.assertIn("proof_packet_members=58", completed.stdout)
            self.assertIn("proof_portable_gates=3", completed.stdout)
            self.assertIn("proof_inventory_only=1", completed.stdout)
            self.assertIn("urm_closure_files=68", completed.stdout)
            self.assertIn("urm_closure_bytes=163813617", completed.stdout)
            self.assertIn("urm_exact_validators=1", completed.stdout)
            self.assertIn("alpha_algebraic_checks=41", completed.stdout)
            self.assertIn(
                "strict_lineage_l12=0.11570852222694002", completed.stdout
            )
            self.assertIn(
                "l8_lineage_order_curvature=NO_RESOLVED", completed.stdout
            )
            self.assertIn(
                "l8_lineage_order_rho=0.1543033499620919", completed.stdout
            )
            self.assertIn(
                "l8_lineage_order_p_plus=0.3619047619047619", completed.stdout
            )
            self.assertIn(
                "l4_lineage_sensitive_delta=0.14761185701903007",
                completed.stdout,
            )
            self.assertIn(
                "l4_lineage_sensitive_occupation_rms=0.006009875541368592",
                completed.stdout,
            )
            self.assertEqual(
                [line for line in completed.stdout.splitlines() if line.startswith("L")],
                ["L08: 0.0244800482", "L10: 0.0687369678"],
            )
            urm_tests = subprocess.run(
                [
                    sys.executable,
                    str(capsule_root / "tests" / "test_urm_validator_dependency_closure.py"),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                urm_tests.returncode,
                0,
                msg=f"stdout:\n{urm_tests.stdout}\nstderr:\n{urm_tests.stderr}",
            )
            proof_packet_tests = subprocess.run(
                [
                    sys.executable,
                    str(capsule_root / "tests" / "test_proof_packet_layout_closure.py"),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                proof_packet_tests.returncode,
                0,
                msg=(
                    f"stdout:\n{proof_packet_tests.stdout}\n"
                    f"stderr:\n{proof_packet_tests.stderr}"
                ),
            )


if __name__ == "__main__":
    unittest.main()
