#!/usr/bin/env python3
"""Focused hostile tests for the independent V012 A06 auditor."""

from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import shutil
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "independent_postbuild_auditor.py"
SPECIFICATION = importlib.util.spec_from_file_location("a06_under_test", SOURCE)
if SPECIFICATION is None or SPECIFICATION.loader is None:
    raise RuntimeError("cannot load A06 auditor")
A06 = importlib.util.module_from_spec(SPECIFICATION)
SPECIFICATION.loader.exec_module(A06)


class IndependentPostbuildAuditorTests(unittest.TestCase):
    @staticmethod
    def copy_l4_cache(directory: str) -> tuple[Path, Path]:
        cache_parent = Path(directory).resolve() / "CACHE_PAYLOADS_V012"
        cache_parent.mkdir()
        destination = cache_parent / "L4"
        shutil.copytree(A06.CACHE_PARENT / "L4", destination)
        return cache_parent, destination

    @staticmethod
    def manifest_inputs(
        manifest: dict[str, object],
    ) -> tuple[object, dict[str, object], dict[str, object]]:
        class ManifestCustody:
            pass

        custody = ManifestCustody()
        custody.member_hashes = {
            (4, row["path"]): row["sha256"] for row in manifest["files"]
        }
        custody.member_identities = {
            (4, row["path"]): (0, 0, row["bytes"], 0, 0, 1, 0o444)
            for row in manifest["files"]
        }
        excluded = {
            "schema", "status", "L", "basis_order", "lineage_identity",
            "edge_layout", "hamiltonian_exchange_coefficient", "files",
            "payload", "resource_certificates", "claim_boundary",
            *A06.SUPERSEDED_PROVENANCE_KEYS,
        }
        provenance = {
            key: manifest[key] for key in A06.MANIFEST_KEYS - excluded
        }
        dual = {
            key: manifest[key] for key in A06.SUPERSEDED_PROVENANCE_KEYS
        }
        return custody, provenance, dual

    @staticmethod
    def record() -> tuple[dict[str, object], dict[str, str], dict[str, dict[str, int]]]:
        manifest_hashes = {str(length): f"{length:064x}" for length in A06.SUPPORTED}
        census = {
            str(length): {
                "file_count": A06.expected_file_count(length),
                "total_bytes": A06.payload_bytes(length),
            }
            for length in A06.SUPPORTED
        }
        record = {
            "schema": A06.SCHEMA,
            "classification": A06.CLASSIFICATION,
            "auditor_role": "INDEPENDENT_HOSTILE_POSTBUILD_READ_ONLY_REVIEW",
            "audited_packet": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012",
            "sealed_input_commit": "42f1ea3301ccf98802c07f3330d52999385cba0b",
            "prebuild_hostile_audit_sha256": "a" * 64,
            "dual_obstruction_and_compatibility_gate_sha256": "b" * 64,
            "manifest_sha256_by_L": manifest_hashes,
            "payload_census_by_L": census,
            "checks": dict(A06.CHECKS),
            "checks_passed": 3489,
            "checks_total": 3489,
            "failures": [],
            "no_symlinked_or_writable_payload_inputs": True,
            "semantic_cachecontext": {
                "L4": {
                    "descriptor_count": 62,
                    "descriptor_reauthentication": "PASS",
                    "full_index_identity": "PASS",
                    "zero_length_q0_open": "PASS",
                },
                "L12": {
                    "descriptor_count": 418,
                    "descriptor_reauthentication": "PASS",
                    "full_index_identity": "PASS",
                    "zero_length_q0_open": "PASS",
                },
            },
            "physical_gate_or_history_executed": False,
            "claim_boundary": A06.CLAIM,
        }
        return record, manifest_hashes, census

    def test_check_census_and_storage_arithmetic_are_exact(self) -> None:
        self.assertEqual(sum(A06.CHECKS.values()), 3489)
        self.assertEqual(
            [A06.expected_file_count(length) for length in A06.SUPPORTED],
            [62, 121, 200, 299, 418],
        )
        self.assertEqual(
            [A06.payload_bytes(length) for length in A06.SUPPORTED],
            [6136, 118660, 2334440, 44512948, 826238292],
        )

    def test_strict_json_refuses_duplicate_and_nonfinite_values(self) -> None:
        with self.assertRaises(A06.AuditRefusal):
            A06._strict_json(b'{"x": 1, "x": 2}', "duplicate")
        with self.assertRaises(A06.AuditRefusal):
            A06._strict_json(b'{"x": NaN}', "nonfinite")

    def test_stable_bytes_requires_owner_once_immutable_regular_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a06-stability-") as directory:
            parent = Path(directory).resolve()
            source = parent / "source.bin"
            source.write_bytes(b"authenticated")
            with self.assertRaises(A06.AuditRefusal):
                A06.stable_bytes(source, "writable")
            source.chmod(0o444)
            raw, digest = A06.stable_bytes(source, "immutable")
            self.assertEqual(raw, b"authenticated")
            self.assertEqual(digest, hashlib.sha256(raw).hexdigest())
            alias = parent / "alias.bin"
            alias.symlink_to(source)
            with self.assertRaises(A06.AuditRefusal):
                A06.stable_bytes(alias, "symlink")

    def test_exact_record_validator_rejects_extra_and_wrong_check_count(self) -> None:
        record, hashes, census = self.record()
        A06.validate_a06_record(record, hashes, census, "a" * 64, "b" * 64)
        extra = copy.deepcopy(record)
        extra["unregistered"] = True
        with self.assertRaises(A06.AuditRefusal):
            A06.validate_a06_record(extra, hashes, census, "a" * 64, "b" * 64)
        wrong = copy.deepcopy(record)
        wrong["checks_total"] = 3488
        with self.assertRaises(A06.AuditRefusal):
            A06.validate_a06_record(wrong, hashes, census, "a" * 64, "b" * 64)

    def test_m17_provenance_and_validator_hash_substitution_refuse(self) -> None:
        manifest = json.loads(
            (A06.CACHE_PARENT / "L4" / "CACHE_MANIFEST.json").read_bytes()
        )
        custody, provenance, dual = self.manifest_inputs(manifest)
        A06.validate_manifest(4, manifest, custody, provenance, dual)
        mutated = copy.deepcopy(manifest)
        mutated["production_obligation_validators_sha256"] = "0" * 64
        with self.assertRaises(A06.AuditRefusal):
            A06.validate_manifest(4, mutated, custody, provenance, dual)
        record, hashes, census = self.record()
        record["prebuild_hostile_audit_sha256"] = "c" * 64
        with self.assertRaises(A06.AuditRefusal):
            A06.validate_a06_record(record, hashes, census, "a" * 64, "b" * 64)

    def test_independent_source_has_no_validator_import_or_execution(self) -> None:
        raw = SOURCE.read_text(encoding="utf-8")
        tree = ast.parse(raw, str(SOURCE))
        imported = {
            alias.name for node in ast.walk(tree) if isinstance(node, ast.Import)
            for alias in node.names
        } | {
            node.module for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }
        self.assertNotIn("importlib", imported)
        self.assertNotIn("importlib.util", imported)
        self.assertNotIn("build_target_cache", imported)
        self.assertNotIn("consume_target_cache", imported)
        self.assertNotIn("require_postbuild_payload_audit", raw)
        self.assertNotIn("independent_final_auditor", raw)

    def test_m12_writable_cache_member_refuses(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a06-m12-") as directory:
            cache_parent, cache = self.copy_l4_cache(directory)
            victim = cache / "carrier_q_00_words.u32"
            victim.chmod(0o644)
            custody = A06.HeldCacheSet((4,))
            with mock.patch.object(A06, "CACHE_PARENT", cache_parent):
                try:
                    with self.assertRaises(A06.AuditRefusal):
                        custody.open_all()
                finally:
                    custody.close()

    def test_m13_manifest_and_member_descriptor_mutations_refuse(self) -> None:
        for victim_name in (
            "CACHE_MANIFEST.json", "carrier_q_01_words.u32",
        ):
            with self.subTest(victim=victim_name):
                with tempfile.TemporaryDirectory(prefix="a06-m13-") as directory:
                    cache_parent, cache = self.copy_l4_cache(directory)
                    custody = A06.HeldCacheSet((4,))
                    with mock.patch.object(A06, "CACHE_PARENT", cache_parent):
                        try:
                            custody.open_all()
                            victim = cache / victim_name
                            victim.chmod(0o644)
                            with victim.open("ab") as stream:
                                stream.write(b"drift")
                            with self.assertRaises(A06.AuditRefusal):
                                custody.reauthenticate()
                        finally:
                            custody.close()

    def test_m18_hash_consistent_cache_semantic_mutation_refuses(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a06-m18-") as directory:
            cache_parent, cache = self.copy_l4_cache(directory)
            victim = cache / "carrier_q_01_targets.i32"
            victim.chmod(0o644)
            raw = bytearray(victim.read_bytes())
            original = int.from_bytes(raw[:4], "little", signed=True)
            raw[:4] = ((original + 1) % 8).to_bytes(4, "little", signed=True)
            victim.write_bytes(raw)
            victim.chmod(0o444)
            manifest_path = cache / "CACHE_MANIFEST.json"
            manifest_path.chmod(0o644)
            manifest = json.loads(manifest_path.read_bytes())
            for row in manifest["files"]:
                if row["path"] == victim.name:
                    row["sha256"] = hashlib.sha256(raw).hexdigest()
                    break
            manifest_path.write_bytes(A06.canonical_json_bytes(manifest))
            manifest_path.chmod(0o444)
            cache.chmod(0o555)
            custody = A06.HeldCacheSet((4,))
            with mock.patch.object(A06, "CACHE_PARENT", cache_parent):
                try:
                    custody.open_all()
                    provenance_source = custody.manifests[4]
                    _fake, provenance, dual = self.manifest_inputs(provenance_source)
                    expected = A06.validate_manifest(
                        4, provenance_source, custody, provenance, dual,
                    )
                    with self.assertRaises(A06.AuditRefusal):
                        A06.validate_semantics(4, custody, expected)
                finally:
                    custody.close()

    def test_held_authority_descriptor_refuses_path_substitution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a06-authority-") as directory:
            parent = Path(directory).resolve()
            gate = parent / "gate.json"
            validator = parent / "validator.py"
            gate.write_bytes(b"{}\n")
            validator.write_bytes(b"original\n")
            gate.chmod(0o444)
            validator.chmod(0o444)
            custody = A06.HeldAuthoritySet(
                {"gate": gate, "source:validator.py": validator}, {"gate"},
            )
            custody.open_all()
            try:
                original = parent / "validator.original"
                validator.rename(original)
                validator.write_bytes(original.read_bytes())
                validator.chmod(0o444)
                with self.assertRaises(A06.AuditRefusal):
                    custody.reauthenticate()
            finally:
                custody.close()

    def test_atomic_publisher_is_exact_immutable_and_no_clobber(self) -> None:
        record, _hashes, _census = self.record()
        with tempfile.TemporaryDirectory(prefix="a06-publish-") as directory:
            destination = Path(directory).resolve() / "POSTBUILD_PAYLOAD_AUDIT_V001.json"
            digest = A06._atomic_publish_once(destination, record, destination)
            raw = destination.read_bytes()
            self.assertEqual(digest, hashlib.sha256(raw).hexdigest())
            self.assertEqual(json.loads(raw), record)
            metadata = destination.stat()
            self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o444)
            self.assertEqual(metadata.st_nlink, 1)
            before = (metadata.st_dev, metadata.st_ino, raw)
            with self.assertRaises(A06.AuditRefusal):
                A06._atomic_publish_once(destination, record, destination)
            after = destination.stat()
            self.assertEqual(
                (after.st_dev, after.st_ino, destination.read_bytes()), before,
            )

    def test_parent_swap_after_link_refuses_and_cleans_staging(self) -> None:
        record, _hashes, _census = self.record()
        with tempfile.TemporaryDirectory(prefix="a06-parent-swap-") as directory:
            root = Path(directory).resolve()
            parent = root / "parent"
            parent.mkdir()
            moved = root / "parent-held"
            destination = parent / "POSTBUILD_PAYLOAD_AUDIT_V001.json"
            real_parent_identity = A06._parent_identity
            calls = 0

            def swap_on_postlink(path: Path, descriptor: int, label: str):
                nonlocal calls
                calls += 1
                if calls == 3:
                    parent.rename(moved)
                    parent.mkdir()
                return real_parent_identity(path, descriptor, label)

            with mock.patch.object(
                A06, "_parent_identity", side_effect=swap_on_postlink,
            ):
                with self.assertRaises(A06.AuditRefusal):
                    A06._atomic_publish_once(destination, record, destination)
            self.assertFalse(destination.exists())
            preserved = moved / destination.name
            self.assertTrue(preserved.is_file())
            self.assertEqual(stat.S_IMODE(preserved.stat().st_mode), 0o444)
            self.assertFalse(any(
                path.name.startswith(f".{destination.name}.staging-")
                for path in moved.iterdir()
            ))

    def test_postlink_fsync_failure_preserves_canonical_and_cleans_staging(self) -> None:
        record, _hashes, _census = self.record()
        with tempfile.TemporaryDirectory(prefix="a06-postlink-") as directory:
            destination = (
                Path(directory).resolve() / "POSTBUILD_PAYLOAD_AUDIT_V001.json"
            )
            real_fsync = A06.os.fsync
            calls = 0

            def fail_first_directory_fsync(descriptor: int) -> None:
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise OSError("injected post-link fsync failure")
                real_fsync(descriptor)

            with mock.patch.object(
                A06.os, "fsync", side_effect=fail_first_directory_fsync,
            ):
                with self.assertRaises(OSError):
                    A06._atomic_publish_once(destination, record, destination)
            self.assertTrue(destination.is_file())
            self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o444)
            self.assertEqual(destination.stat().st_nlink, 1)
            self.assertFalse(any(
                path.name.startswith(f".{destination.name}.staging-")
                for path in destination.parent.iterdir()
            ))

    def test_run_reauthenticates_caches_and_authorities_through_publish(self) -> None:
        record, _hashes, _census = self.record()

        class SentinelCustody:
            def __init__(self, *, cache: bool) -> None:
                self.reauthentications = 0
                self.closed = False
                if cache:
                    self.lengths = A06.SUPPORTED
                    self.manifest_hashes = {
                        length: record["manifest_sha256_by_L"][str(length)]
                        for length in A06.SUPPORTED
                    }
                else:
                    self.hashes = {
                        "A03": record["prebuild_hostile_audit_sha256"],
                        "A04": record[
                            "dual_obstruction_and_compatibility_gate_sha256"
                        ],
                    }

            def reauthenticate(self) -> None:
                self.reauthentications += 1

            def close(self) -> None:
                self.closed = True

        cache = SentinelCustody(cache=True)
        authorities = SentinelCustody(cache=False)
        with tempfile.TemporaryDirectory(prefix="a06-run-") as directory:
            destination = (
                Path(directory).resolve() / "POSTBUILD_PAYLOAD_AUDIT_V001.json"
            )
            with mock.patch.object(
                A06, "audit_record", return_value=(record, cache, authorities),
            ), mock.patch.object(A06, "CANONICAL_A06", destination):
                self.assertEqual(A06.run(publish=True), record)
        self.assertEqual(cache.reauthentications, 3)
        self.assertEqual(authorities.reauthentications, 3)
        self.assertTrue(cache.closed)
        self.assertTrue(authorities.closed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
