#!/usr/bin/env python3
"""Synthetic-only tests for Track C refinement and A23--A27 sinks."""

from __future__ import annotations

import ast
import hashlib
import inspect
import itertools
import os
import stat
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

import numpy as np

import independent_final_auditor as auditor
import production_dag_refinement as refinement
import production_evidence_orchestrator as evidence
import stage1_artifact_census as stage1_census
import stage1_handoff_verifier as handoff
from synthetic_upstream_authority_fixtures import fixture as upstream_fixture


auditor._install_synthetic_upstream_fixture(upstream_fixture)


class FinalAuditorTests(unittest.TestCase):
    def test_fixture_provider_is_explicit_and_validation_independent(self):
        auditor._positive_fixture_bundle_cached.cache_clear()
        with mock.patch.object(
            auditor, "_SYNTHETIC_UPSTREAM_FIXTURE", None,
        ):
            with self.assertRaisesRegex(
                auditor.Refusal, "synthetic fixture provider not installed",
            ):
                auditor.positive_fixture("A26_FINAL_L12_AUDIT")
            auditor._install_synthetic_upstream_fixture(upstream_fixture)
            auditor._positive_fixture_bundle_cached.cache_clear()
            fixture = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
            self.assertEqual(fixture["authority_records_authenticated"], 42)
            telemetry = auditor.positive_fixture("A23_POSTRUN_TELEMETRY")
            auditor.validate_postrun_telemetry(telemetry, fixture_mode=True)

    def test_all_five_native_positive_fixtures_pass(self):
        for artifact_id in auditor.ARTIFACT_IDS:
            accepted = auditor.validate_artifact(
                artifact_id, auditor.positive_fixture(artifact_id),
                fixture_mode=True,
            )
            self.assertIs(type(accepted), dict)

    def test_all_113_matrix_assigned_native_mutations_refuse_cleanly(self):
        total = 0
        observed_native_refusals = set()
        for artifact_id, mutation_classes in auditor.MUTATION_ASSIGNMENTS.items():
            for mutation_class in mutation_classes:
                total += 1
                value, expected, _description = auditor.mutated_fixture(
                    artifact_id, mutation_class
                )
                with self.assertRaisesRegex(
                    auditor.Refusal, f"^{expected}",
                ) as refusal:
                    auditor.validate_artifact(
                        artifact_id, value, fixture_mode=True
                    )
                key = (artifact_id, mutation_class)
                if key in auditor.FINAL_NATIVE_MUTATION_REFUSAL:
                    observed_native_refusals.add(key)
                    self.assertTrue(
                        str(refusal.exception).endswith(
                            auditor.FINAL_NATIVE_MUTATION_REFUSAL[key]
                        )
                    )
        self.assertEqual(total, 113)
        self.assertEqual(len(auditor.FINAL_NATIVE_MUTATION_REFUSAL), 73)
        self.assertEqual(
            observed_native_refusals,
            set(auditor.FINAL_NATIVE_MUTATION_REFUSAL),
        )

    def test_unknown_ids_and_malformed_dispatch_types_refuse(self):
        cases = (
            (None, {}, True),
            ("A22_TARGET_L12_AUTHORIZATION", {}, True),
            ("A23_POSTRUN_TELEMETRY", {}, 1),
            ("A23_POSTRUN_TELEMETRY", None, True),
            ("A24_TARGET_L12_HISTORY", [], True),
        )
        for artifact_id, record, fixture_mode in cases:
            with self.assertRaises(auditor.Refusal):
                auditor.validate_artifact(
                    artifact_id, record, fixture_mode=fixture_mode
                )

    def test_native_histories_justify_only_the_first_null_zero_step(self):
        artifact_id = "A24_TARGET_L12_HISTORY"
        fixture = auditor.positive_fixture(artifact_id)
        self.assertEqual(
            fixture["rows"][0]["null_solver"]["maximum_krylov_steps"], 0
        )
        auditor.validate_artifact(artifact_id, fixture, fixture_mode=True)
        unjustified = deepcopy(fixture)
        unjustified["rows"][1]["null_solver"]["maximum_krylov_steps"] = 0
        with self.assertRaises(auditor.Refusal):
            auditor.validate_artifact(
                artifact_id, unjustified, fixture_mode=True
            )

    def test_a23_runtime_window_and_worker_identity_are_exact(self):
        for mutation in ("disk_start", "sample_identity"):
            fixture = auditor.positive_fixture("A23_POSTRUN_TELEMETRY")
            if mutation == "disk_start":
                fixture["free_disk_bytes_samples"][0]["captured_epoch"] += 1
            else:
                fixture["runtime_samples_by_role"]["target_v012"][1][
                    "process_start_token"
                ] = "0" * 64
            with self.assertRaises(auditor.Refusal):
                auditor.validate_postrun_telemetry(fixture, fixture_mode=True)

    def test_hostile_history_preserves_native_chebyshev_and_raw_c128_contract(self):
        fixture = auditor._hostile_history_fixture()
        self.assertEqual(len(fixture["rows"][0]["actual_solver"]), 12)
        self.assertEqual(len(fixture["rows"][-1]["actual_solver"]), 16)
        self.assertEqual(
            fixture["rows"][0]["actual_solver"]["algorithm"],
            "RECURRENCE_REPLAY_GL_GROUPS",
        )
        for shard in fixture["terminal_shards"]:
            self.assertTrue(shard["path"].endswith(".c128"))
            self.assertEqual(shard["bytes"], 16 * np.prod(shard["shape"]))
        auditor.validate_hostile_l12_history(fixture, fixture_mode=True)
        relabeled = deepcopy(fixture)
        relabeled["rows"][0]["actual_solver"] = auditor._solver_fixture(1, False)
        with self.assertRaises(auditor.Refusal):
            auditor.validate_hostile_l12_history(relabeled, fixture_mode=True)

    def test_native_history_path_type_mutants_are_controlled_refusals(self):
        for artifact_id in (
            "A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY"
        ):
            for value in (None, 7, [], {}, "relative/q_00.npy"):
                fixture = auditor.positive_fixture(artifact_id)
                fixture["terminal_shards"][0]["path"] = value
                with self.assertRaises(auditor.Refusal):
                    auditor.validate_artifact(
                        artifact_id, fixture, fixture_mode=True
                    )

    def test_tolerance_close_different_hashes_pass_but_large_or_nonfinite_refuse(self):
        fixture = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
        comparison = fixture["terminal_comparisons"][0]
        self.assertNotEqual(comparison["target_sha256"], comparison["hostile_sha256"])
        comparison["linf_abs_error"] = 9.999e-9
        auditor.validate_artifact(
            "A26_FINAL_L12_AUDIT", fixture, fixture_mode=True
        )
        for value in (1.0001e-8, float("nan"), float("inf"), 0):
            mutant = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
            mutant["terminal_comparisons"][0]["linf_abs_error"] = value
            with self.assertRaises(auditor.Refusal):
                auditor.validate_artifact(
                    "A26_FINAL_L12_AUDIT", mutant, fixture_mode=True
                )

    def test_final_audit_reconstructs_native_history_projection_not_only_hashes(self):
        fixture = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
        bindings = {
            (row["artifact_id"], row["instance"]): row
            for row in fixture["authority_bindings"]
        }
        target_binding = bindings[("A24_TARGET_L12_HISTORY", 1)]
        telemetry_binding = bindings[("A23_POSTRUN_TELEMETRY", 1)]
        completion_binding = bindings[("A22_TARGET_L12_AUTHORIZATION", 11)]
        target_binding["record"]["rows"][0]["W_n"] += 2.0e-8
        target_binding["sha256"] = auditor.record_sha256(target_binding["record"])
        completion_binding["record"]["output_sha256"] = target_binding["sha256"]
        completion_binding["sha256"] = auditor.record_sha256(
            completion_binding["record"]
        )
        telemetry_binding["record"]["output_sha256_by_role"]["target_v012"] = (
            target_binding["sha256"]
        )
        telemetry_binding["record"]["completion_sha256_by_role"]["target_v012"] = (
            completion_binding["sha256"]
        )
        telemetry_binding["sha256"] = auditor.record_sha256(
            telemetry_binding["record"]
        )
        with self.assertRaisesRegex(auditor.Refusal, "history projection"):
            auditor.validate_final_l12_audit(fixture, fixture_mode=True)

    def test_final_audit_authenticates_exact_42_record_authority_census(self):
        fixture = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
        bindings = fixture["authority_bindings"]
        self.assertEqual(len(bindings), 42)
        self.assertEqual(fixture["authority_records_authenticated"], 42)
        self.assertEqual(
            {(row["artifact_id"], row["instance"]) for row in bindings},
            {
                (artifact_id, instance)
                for artifact_id, count in auditor.AUTHORITY_INSTANCE_CENSUS.items()
                for instance in range(1, count + 1)
            },
        )
        a03 = next(
            row for row in bindings
            if row["artifact_id"] == "A03_PREPAYLOAD_AUDIT"
        )
        self.assertEqual(
            set(a03["record"]["audited_files_sha256"]),
            auditor.A03_AUDITED_FILES,
        )
        missing_a03_file = deepcopy(fixture)
        missing_a03_binding = next(
            row for row in missing_a03_file["authority_bindings"]
            if row["artifact_id"] == "A03_PREPAYLOAD_AUDIT"
        )
        missing_a03_binding["record"]["audited_files_sha256"].pop(
            "METHOD.md"
        )
        missing_a03_binding["sha256"] = auditor.record_sha256(
            missing_a03_binding["record"]
        )
        with self.assertRaisesRegex(
            auditor.Refusal, "A03 audited file census mismatch",
        ):
            auditor.validate_final_l12_audit(
                missing_a03_file, fixture_mode=True
            )
        for mutate in ("delete", "duplicate"):
            mutant = deepcopy(fixture)
            if mutate == "delete":
                mutant["authority_bindings"].pop()
            else:
                mutant["authority_bindings"][-1] = deepcopy(
                    mutant["authority_bindings"][0]
                )
            with self.assertRaisesRegex(auditor.Refusal, "authority binding"):
                auditor.validate_final_l12_audit(mutant, fixture_mode=True)

    def test_a17_composite_reconstructs_nine_sources_and_binds_a18(self):
        fixture = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
        bindings = {
            (row["artifact_id"], row["instance"]): row
            for row in fixture["authority_bindings"]
        }
        a17 = bindings[("A17_HOSTILE_L12_ELIGIBILITY", 1)]
        self.assertEqual(
            [row["label"] for row in a17["sources"]],
            list(auditor.A17_SOURCE_LABELS),
        )
        self.assertEqual(len(a17["sources"]), 9)
        mutant = deepcopy(fixture)
        mutant_a18 = next(
            row for row in mutant["authority_bindings"]
            if row["artifact_id"] == "A18_L10_CROSS_GATE"
        )
        mutant_a18["record"]["hostile"]["branch"]["method"]["sha256"] = (
            "0" * 64
        )
        mutant_a18["sha256"] = auditor.record_sha256(mutant_a18["record"])
        with self.assertRaisesRegex(auditor.Refusal, "^A26_FINAL_L12_AUDIT"):
            auditor.validate_final_l12_audit(mutant, fixture_mode=True)

    def test_authority_owner_path_and_descriptor_path_swap_refuse(self):
        with tempfile.TemporaryDirectory(
            prefix="a26_authority_", dir=auditor.ROOT,
        ) as directory:
            root = Path(directory)
            payload = auditor.canonical_json_bytes({"schema": "TEST"})
            digest = hashlib.sha256(payload).hexdigest()
            canonical = root / "canonical.json"
            canonical.write_bytes(payload)
            canonical.chmod(0o444)
            wrong_path_binding = {
                "artifact_id": "A01_FREEZE_AND_SOURCE_PACKET",
                "instance": 1,
                "path": str(canonical),
                "sha256": digest,
            }
            with self.assertRaisesRegex(auditor.Refusal, "owner-once"):
                auditor._authority_binding(
                    wrong_path_binding, "A26_FINAL_L12_AUDIT", False,
                )

            _record, retained = auditor._open_immutable_json(
                str(canonical), digest, "A26_FINAL_L12_AUDIT", "swap test",
            )
            held = root / "held.json"
            canonical.rename(held)
            canonical.write_bytes(payload)
            canonical.chmod(0o444)
            with self.assertRaisesRegex(auditor.Refusal, "changed"):
                retained.verify_and_close()
            self.assertEqual(retained.descriptor, -1)
            self.assertEqual(retained.parent_descriptor, -1)

    def test_refusal_cleanup_closes_every_retained_authority(self):
        with tempfile.TemporaryDirectory(
            prefix="a26_cleanup_", dir=auditor.ROOT,
        ) as directory:
            root = Path(directory)
            payload = auditor.canonical_json_bytes({"schema": "TEST"})
            digest = hashlib.sha256(payload).hexdigest()
            retained = []
            for index in range(2):
                path = root / f"authority_{index}.json"
                path.write_bytes(payload)
                path.chmod(0o444)
                _record, held = auditor._open_immutable_json(
                    str(path), digest, "A26_FINAL_L12_AUDIT",
                    f"cleanup {index}",
                )
                retained.append(held)
            original = root / "authority_0.json"
            original.rename(root / "displaced.json")
            original.write_bytes(payload)
            original.chmod(0o444)
            with self.assertRaises(auditor.Refusal):
                auditor._verify_close_authority_inputs(retained)
            self.assertTrue(all(
                item.descriptor == item.parent_descriptor == -1
                for item in retained
            ))

    def test_terminal_descriptor_path_swap_refuses(self):
        with tempfile.TemporaryDirectory(
            prefix="a26_terminal_", dir=auditor.ROOT,
        ) as directory:
            root = Path(directory)
            payload = b"\x00" * 16
            digest = hashlib.sha256(payload).hexdigest()
            path = root / "q_00.c128"
            path.write_bytes(payload)
            path.chmod(0o444)
            binding = {
                "path": str(path), "sha256": digest, "bytes": len(payload),
            }
            retained = auditor._open_terminal(
                binding, "A26_FINAL_L12_AUDIT", "hostile q=0",
            )
            try:
                path.rename(root / "displaced.c128")
                path.write_bytes(payload)
                path.chmod(0o444)
                with self.assertRaises(auditor.Refusal):
                    auditor._verify_terminal_input(
                        retained, binding,
                        "A26_FINAL_L12_AUDIT", "hostile", 0,
                    )
            finally:
                retained.close()

    def test_authority_and_terminal_parent_symlink_substitution_refuse(self):
        with tempfile.TemporaryDirectory(
            prefix="a26_parent_alias_", dir=auditor.ROOT,
        ) as directory:
            root = Path(directory)
            parent = root / "canonical_parent"
            parent.mkdir()
            json_payload = auditor.canonical_json_bytes({"schema": "TEST"})
            terminal_payload = b"\x00" * 16
            json_path = parent / "authority.json"
            terminal_path = parent / "terminal.c128"
            json_path.write_bytes(json_payload)
            terminal_path.write_bytes(terminal_payload)
            json_path.chmod(0o444)
            terminal_path.chmod(0o444)
            json_digest = hashlib.sha256(json_payload).hexdigest()
            terminal_digest = hashlib.sha256(terminal_payload).hexdigest()
            _record, retained = auditor._open_immutable_json(
                str(json_path), json_digest, "A26_FINAL_L12_AUDIT",
                "parent alias authority",
            )
            terminal_binding = {
                "path": str(terminal_path), "sha256": terminal_digest,
                "bytes": len(terminal_payload),
            }
            terminal_retained = auditor._open_terminal(
                terminal_binding, "A26_FINAL_L12_AUDIT",
                "parent alias terminal",
            )
            displaced = root / "displaced_parent"
            parent.rename(displaced)
            parent.symlink_to(displaced, target_is_directory=True)
            with self.assertRaisesRegex(auditor.Refusal, "parent path"):
                retained.verify_and_close()
            try:
                with self.assertRaisesRegex(auditor.Refusal, "parent path"):
                    auditor._verify_terminal_input(
                        terminal_retained, terminal_binding,
                        "A26_FINAL_L12_AUDIT", "hostile", 0,
                    )
            finally:
                terminal_retained.close()

    def test_final_auditor_parent_directory_replacement_refuses(self):
        with tempfile.TemporaryDirectory(
            prefix="a26_parent_replace_", dir=auditor.ROOT,
        ) as directory:
            root = Path(directory)
            parent = root / "authority"
            parent.mkdir()
            path = parent / "record.json"
            payload = auditor.canonical_json_bytes({"schema": "TEST"})
            path.write_bytes(payload)
            path.chmod(0o444)
            digest = hashlib.sha256(payload).hexdigest()
            _record, retained = auditor._open_immutable_json(
                str(path), digest, "A26_FINAL_L12_AUDIT",
                "parent replacement",
            )
            held = root / "authority-held"
            parent.rename(held)
            parent.mkdir()
            replacement = parent / path.name
            replacement.write_bytes(payload)
            replacement.chmod(0o444)
            with self.assertRaisesRegex(auditor.Refusal, "parent"):
                retained.verify_and_close()
            self.assertEqual(retained.descriptor, -1)
            self.assertEqual(retained.parent_descriptor, -1)

    def test_final_auditor_hardlinks_and_noncanonical_json_refuse(self):
        with tempfile.TemporaryDirectory(
            prefix="a26_exact_bytes_", dir=auditor.ROOT,
        ) as directory:
            root = Path(directory)
            canonical = root / "canonical.json"
            payload = auditor.canonical_json_bytes({"schema": "TEST"})
            canonical.write_bytes(payload)
            canonical.chmod(0o444)
            os.link(canonical, root / "second-link.json")
            with self.assertRaisesRegex(auditor.Refusal, "owner-once"):
                auditor._open_immutable_json(
                    str(canonical), hashlib.sha256(payload).hexdigest(),
                    "A26_FINAL_L12_AUDIT", "hardlinked authority",
                )

            noncanonical = root / "noncanonical.json"
            raw = b'{ "schema": "TEST" }\n'
            noncanonical.write_bytes(raw)
            noncanonical.chmod(0o444)
            with self.assertRaisesRegex(auditor.Refusal, "canonical JSON"):
                auditor._open_immutable_json(
                    str(noncanonical), hashlib.sha256(raw).hexdigest(),
                    "A26_FINAL_L12_AUDIT", "noncanonical authority",
                )

            terminal = root / "terminal.c128"
            terminal.write_bytes(b"\0" * 16)
            terminal.chmod(0o444)
            os.link(terminal, root / "terminal-alias.c128")
            with self.assertRaisesRegex(auditor.Refusal, "owner-once"):
                auditor._open_terminal({
                    "path": str(terminal),
                    "sha256": hashlib.sha256(terminal.read_bytes()).hexdigest(),
                    "bytes": 16,
                }, "A26_FINAL_L12_AUDIT", "hardlinked terminal")

    def test_final_auditor_metadata_change_during_hash_refuses(self):
        with tempfile.TemporaryDirectory(
            prefix="a26_hash_race_", dir=auditor.ROOT,
        ) as directory:
            path = Path(directory) / "record.json"
            payload = auditor.canonical_json_bytes({"schema": "TEST"})
            path.write_bytes(payload)
            path.chmod(0o444)
            digest = hashlib.sha256(payload).hexdigest()
            real_hash = auditor._descriptor_sha256

            def mutate_after_hash(descriptor):
                result = real_hash(descriptor)
                path.chmod(0o644)
                return result

            with mock.patch.object(
                auditor, "_descriptor_sha256", side_effect=mutate_after_hash,
            ):
                with self.assertRaisesRegex(auditor.Refusal, "changed"):
                    auditor._open_immutable_json(
                        str(path), digest, "A26_FINAL_L12_AUDIT",
                        "metadata race",
                    )

    def test_final_audit_reconstructs_upstream_and_launch_authority_edges(self):
        cases = (
            ("A03_PREPAYLOAD_AUDIT", 1, "audited_freeze_sha256"),
            ("A10_CONTROL_HISTORIES", 1, "execution_authorization_sha256"),
            ("A18_L10_CROSS_GATE", 1, "target"),
            ("A22_TARGET_L12_AUTHORIZATION", 5, "schedule_sha256"),
        )
        for artifact_id, instance, field in cases:
            fixture = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
            binding = next(
                row for row in fixture["authority_bindings"]
                if row["artifact_id"] == artifact_id
                and row["instance"] == instance
            )
            record = binding["record"]
            if field == "target":
                record["target"]["history_sha256"] = "0" * 64
            else:
                record[field] = "0" * 64
            binding["sha256"] = auditor.record_sha256(record)
            with self.assertRaisesRegex(
                auditor.Refusal, "^A26_FINAL_L12_AUDIT",
            ):
                auditor.validate_final_l12_audit(fixture, fixture_mode=True)

    def test_a11_a16_target_fixtures_match_independent_contracts(self):
        for artifact_id in (
            "A11_CONTROL_STAGE_GATE", "A12_CONTROL_STAGE_AUDIT",
            "A13_L10_AUTHORIZATION", "A14_L10_HISTORY",
            "A15_L10_STAGE_GATE", "A16_L10_STAGE_AUDIT",
        ):
            with self.subTest(artifact_id=artifact_id):
                accepted = auditor._validate_independent_upstream_record(
                    artifact_id, upstream_fixture(artifact_id),
                    "A26_FINAL_L12_AUDIT", True,
                )
                self.assertIs(type(accepted), dict)

    def test_a26_upstream_a11_a16_malformed_records_refuse(self):
        cases = (
            (
                "A11_CONTROL_STAGE_GATE", "history row extra key",
                lambda row: row["histories"][0].update(extra_nested=1),
                "exact key census mismatch",
            ),
            (
                "A11_CONTROL_STAGE_GATE", "wrong absolute history path",
                lambda row: row["histories"][0].update(
                    path="/synthetic/WRONG/HISTORY.json",
                ),
                "canonical path mismatch",
            ),
            (
                "A11_CONTROL_STAGE_GATE", "traversal history path",
                lambda row: row["histories"][0].update(path="../escape.json"),
                "canonical path mismatch",
            ),
            (
                "A15_L10_STAGE_GATE", "history row extra key",
                lambda row: row["histories"][0].update(extra_nested=1),
                "exact key census mismatch",
            ),
            (
                "A15_L10_STAGE_GATE", "wrong absolute history path",
                lambda row: row["histories"][0].update(
                    path="/synthetic/WRONG/HISTORY.json",
                ),
                "canonical path mismatch",
            ),
            (
                "A15_L10_STAGE_GATE", "traversal history path",
                lambda row: row["histories"][0].update(path="../escape.json"),
                "canonical path mismatch",
            ),
            (
                "A12_CONTROL_STAGE_AUDIT", "fabricated check names",
                lambda row: row.update(
                    checks={"fabricated_positive_alpha": 23,
                            "fabricated_positive_beta": 24},
                    checks_total=47, checks_passed=47,
                ),
                "exact check map mismatch",
            ),
            (
                "A16_L10_STAGE_AUDIT", "fabricated check names",
                lambda row: row.update(
                    checks={"fabricated_positive_alpha": 12,
                            "fabricated_positive_beta": 13},
                    checks_total=25, checks_passed=25,
                ),
                "exact check map mismatch",
            ),
            (
                "A13_L10_AUTHORIZATION", "authorized length eleven",
                lambda row: row.update(authorized_length=11),
                "authorized length mismatch",
            ),
            (
                "A13_L10_AUTHORIZATION", "authorized length boolean",
                lambda row: row.update(authorized_length=True),
                "must be an exact integer",
            ),
            (
                "A13_L10_AUTHORIZATION", "authorized length float",
                lambda row: row.update(authorized_length=10.0),
                "must be an exact integer",
            ),
            (
                "A14_L10_HISTORY", "event row extra key",
                lambda row: row["rows"][0].update(extra_nested=1),
                "exact key census mismatch",
            ),
            (
                "A14_L10_HISTORY", "comparison extra key",
                lambda row: row["comparison"].update(extra_nested=1),
                "exact key census mismatch",
            ),
            (
                "A14_L10_HISTORY", "resource extra key",
                lambda row: row["resource"].update(extra_nested=1),
                "exact key census mismatch",
            ),
            (
                "A14_L10_HISTORY", "terminal shard extra key",
                lambda row: row["terminal_shards"][0].update(extra_nested=1),
                "exact key census mismatch",
            ),
            (
                "A14_L10_HISTORY", "canonical V004 projection mismatch",
                lambda row: row["rows"][0].update(
                    W_n=row["rows"][0]["W_n"] + 0.125,
                ),
                "canonical V004 mismatch",
            ),
        )
        for artifact_id, label, mutate, expected in cases:
            with self.subTest(artifact_id=artifact_id, mutation=label):
                fixture = auditor.positive_fixture("A26_FINAL_L12_AUDIT")
                binding = next(
                    row for row in fixture["authority_bindings"]
                    if row["artifact_id"] == artifact_id
                )
                mutate(binding["record"])
                binding["sha256"] = auditor.record_sha256(binding["record"])
                with self.assertRaisesRegex(auditor.Refusal, expected):
                    auditor.validate_final_l12_audit(
                        fixture, fixture_mode=True,
                    )

    def test_a27_is_the_matrix_authoritative_477_case_33_fixture_ledger(self):
        fixture = auditor.positive_fixture("A27_MUTATION_LEDGER")
        self.assertEqual(fixture["case_count"], 477)
        self.assertEqual(fixture["positive_sink_call_count"], 33)
        self.assertEqual(len(fixture["cases"]), 477)
        auditor.validate_mutation_ledger(fixture, fixture_mode=True)

    def test_reversed_basis_hash_matches_bruteforce_rank_bijection(self):
        marker = b"V001_LE_U64_TARGET_RANK_TO_HOSTILE_RANK\0"
        for width in range(1, 9):
            for q in range(width + 1):
                target = list(itertools.combinations(range(width), q))
                hostile = list(itertools.combinations(reversed(range(width)), q))
                hostile_rank = {
                    tuple(sorted(mask)): rank for rank, mask in enumerate(hostile)
                }
                permutation = [hostile_rank[mask] for mask in target]
                self.assertEqual(sorted(permutation), list(range(len(target))))
                import struct
                material = marker + struct.pack("<IIQ", width, q, len(target))
                material += struct.pack(f"<{len(target)}Q", *permutation)
                self.assertEqual(
                    hashlib.sha256(material).hexdigest(),
                    auditor.basis_permutation_sha256(width, q),
                )

    def test_production_terminal_comparison_reads_descriptors_and_projects_both_axes(self):
        with tempfile.TemporaryDirectory(prefix="track_c_terminal_") as directory:
            root = Path(directory)
            target_path = root / "target.npy"
            hostile_path = root / "hostile.c128"
            target = np.arange(12, dtype=np.float64).reshape(3, 4).astype("<c16")
            hostile = target[::-1, ::-1] + 5.0e-9
            np.save(target_path, target, allow_pickle=False)
            hostile.astype("<c16").tofile(hostile_path)
            target_path.chmod(0o444)
            hostile_path.chmod(0o444)

            def binding(path: Path) -> dict[str, object]:
                return {
                    "path": str(path), "shape": [3, 4],
                    "bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }

            with mock.patch.object(auditor, "ROOT", root):
                observed = auditor._compare_terminal_files(
                    binding(target_path), binding(hostile_path), 1,
                    lineage_width=3, carrier_width=4,
                )
            self.assertAlmostEqual(observed, 5.0e-9, places=14)
            hostile_path.chmod(0o644)
            with mock.patch.object(auditor, "ROOT", root):
                with self.assertRaises(auditor.Refusal):
                    auditor._compare_terminal_files(
                        binding(target_path), binding(hostile_path), 1,
                        lineage_width=3, carrier_width=4,
                    )

    def test_stable_json_reader_requires_immutable_descriptor_and_rehashes(self):
        with tempfile.TemporaryDirectory(prefix="track_c_json_") as directory:
            path = Path(directory) / "record.json"
            payload = auditor.canonical_json_bytes({"schema": "S"})
            path.write_bytes(payload)
            digest = hashlib.sha256(payload).hexdigest()
            with mock.patch.object(auditor, "ROOT", Path(directory)):
                with self.assertRaises(auditor.Refusal):
                    auditor._open_immutable_json(
                        str(path), digest, "A26_FINAL_L12_AUDIT", "test"
                    )
            path.chmod(0o444)
            with mock.patch.object(auditor, "ROOT", Path(directory)):
                record, retained = auditor._open_immutable_json(
                    str(path), digest, "A26_FINAL_L12_AUDIT", "test"
                )
                self.assertEqual(record, {"schema": "S"})
                retained.verify_and_close()

    def test_final_module_has_no_target_import_or_write_launch_calls(self):
        tree = ast.parse(Path(auditor.__file__).read_text(encoding="utf-8"))
        imported = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertTrue({
            "build_target_cache", "consume_target_cache",
            "compute_prefix_history_v004", "subprocess", "multiprocessing",
        }.isdisjoint(imported))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotIn(node.func.attr, {
                    "write", "write_text", "write_bytes", "Popen", "spawn", "fork",
                })


class RefinementTests(unittest.TestCase):
    def test_stage1_census_is_complete_and_fail_closed_at_boundary(self):
        result = stage1_census.stage1_artifact_census()
        self.assertEqual(
            result["source_count_by_group"],
            {
                "target_v012": 5, "hostile_v004r4": 12,
                "dual_launch": 2, "final_adjudication": 3,
            },
        )
        self.assertEqual(result["stage1_result_count"], 15)
        expected_target_manifests = tuple(
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            f"CACHE_PAYLOADS_V012/L{length}/CACHE_MANIFEST.json"
            for length in (4, 6, 8, 10, 12)
        )
        self.assertEqual(
            handoff.EXTERNAL_CACHE_MANIFEST_PATHS,
            expected_target_manifests,
        )
        self.assertEqual(result["external_cache_manifest_count"], 5)
        self.assertTrue(
            set(expected_target_manifests).issubset(
                result["boundary_required_path_census"]
            )
        )
        hostile_stage2_paths = {
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS",
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json",
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json",
        }
        self.assertTrue(
            hostile_stage2_paths.issubset(handoff.FORBIDDEN_STAGE2_PATHS)
        )
        self.assertTrue(
            hostile_stage2_paths.isdisjoint(
                handoff.EXTERNAL_CACHE_MANIFEST_PATHS
            )
        )
        self.assertIn(
            "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
            "v004r4_cross_branch_contract.py",
            [row["path"] for row in result["explicitly_unfrozen_not_executed"]],
        )
        if result["missing_boundary_evidence"]:
            with self.assertRaises(stage1_census.CensusRefusal):
                stage1_census.stage1_artifact_census(
                    require_boundary_evidence=True,
                )

    def test_dynamic_model_loader_is_exactly_registered(self):
        with self.assertRaisesRegex(
            refinement.RefinementRefusal,
            "dynamic model load is outside the exact registry",
        ):
            refinement._load(
                refinement.HERE / "test_production_dag_refinement.py",
                "track_c_final_contract",
            )

    def test_declared_graph_refines_all_22_abstract_edges(self):
        result = refinement.validate_declared_refinement()
        self.assertEqual(result["production_nodes"], 30)
        self.assertEqual(result["abstract_nodes"], 18)
        self.assertEqual(result["abstract_edges_proved"], 22)

    def test_abstract_authorization_and_launch_models_match(self):
        self.assertEqual(
            refinement.validate_abstract_model()["authorization_model_edges"],
            22,
        )
        self.assertEqual(
            refinement.validate_launch_model()["launch_refinement_edges"], 14
        )

    def test_static_production_entrypoint_and_predecessor_interfaces_match(self):
        result = refinement.validate_static_production_interfaces()
        self.assertEqual(result["ordered_stage_calls"], 14)
        self.assertEqual(result["predecessor_argument_bindings"], 37)
        self.assertEqual(result["stage_gate_call_sites"], 2)
        self.assertEqual(result["shared_dispatcher_bindings"], 4)
        self.assertEqual(result["live_final_publication_sinks"], 5)
        self.assertEqual(result["registered_unorchestrated_final_sinks"], 0)
        self.assertEqual(result["hostile_identity_literals"], 11)
        self.assertEqual(result["hostile_native_contract_bindings"], 12)

    def test_hostile_manifest_postbuild_hash_direction_is_acyclic(self):
        result = refinement.validate_static_production_interfaces()
        self.assertEqual(result["hostile_manifest_preregistration_fields"], 4)
        self.assertEqual(result["hostile_cryptographic_dependency_nodes"], 3)
        self.assertEqual(result["hostile_cryptographic_dependency_edges"], 3)
        self.assertEqual(result["hostile_cryptographic_cycles"], 0)
        self.assertEqual(result["hostile_downstream_digest_bindings"], 2)

    def test_graph_edge_deletion_and_cycle_mutations_refuse(self):
        missing = dict(refinement.PRODUCTION_NODES)
        node = missing["P19_DUAL_L12_RELEASE"]
        missing["P19_DUAL_L12_RELEASE"] = refinement.ProductionNode(
            node.interface, frozenset()
        )
        with self.assertRaises(refinement.RefinementRefusal):
            refinement.validate_declared_refinement(missing)
        cycle = dict(refinement.PRODUCTION_NODES)
        node = cycle["P01_PREPAYLOAD_AUDIT"]
        cycle["P01_PREPAYLOAD_AUDIT"] = refinement.ProductionNode(
            node.interface, frozenset({"P24_FINAL_ADJUDICATION"})
        )
        with self.assertRaises(refinement.RefinementRefusal):
            refinement.validate_declared_refinement(cycle)

    def test_public_final_sink_signatures_are_callable(self):
        for name in (
            "validate_postrun_telemetry", "validate_target_l12_history",
            "validate_hostile_l12_history", "validate_final_l12_audit",
            "validate_mutation_ledger",
        ):
            signature = inspect.signature(getattr(auditor, name))
            self.assertEqual(tuple(signature.parameters), ("record", "fixture_mode"))
            self.assertEqual(
                signature.parameters["fixture_mode"].kind,
                inspect.Parameter.KEYWORD_ONLY,
            )

    def test_worker_identity_limitation_is_closed_by_nonce_and_parent_handle(self):
        result = refinement.run_all_refinement_checks()
        limitations = result["remaining_identity_limitations"]
        self.assertEqual(limitations, [])


class ProductionEvidenceOrchestratorTests(unittest.TestCase):
    @staticmethod
    def validator(artifact_id, record, *, fixture_mode):
        if fixture_mode is not False or record != {
            "artifact_id": artifact_id, "passed": True,
        }:
            raise evidence.OrchestrationRefusal("fixture validator refusal")
        return record

    @staticmethod
    def authority(root: Path, artifact_id: str) -> tuple[str, str]:
        path = root / f"{artifact_id}.json"
        payload = evidence.canonical_json_bytes({
            "artifact_id": artifact_id, "passed": True,
        })
        path.write_bytes(payload)
        path.chmod(0o444)
        return str(path), hashlib.sha256(payload).hexdigest()

    @staticmethod
    def registries(root: Path) -> tuple[dict[str, str], dict[str, str]]:
        predecessors = {
            artifact_id: str(root / f"{artifact_id}.json")
            for artifact_id in evidence.PREDECESSOR_IDS
        }
        outputs = {
            "A23_POSTRUN_TELEMETRY": predecessors["A23_POSTRUN_TELEMETRY"],
            "A27_MUTATION_LEDGER": predecessors["A27_MUTATION_LEDGER"],
            "A26_FINAL_L12_AUDIT": str(root / "A26_FINAL_L12_AUDIT.json"),
        }
        return predecessors, outputs

    @staticmethod
    def temporary_directory(prefix: str) -> tempfile.TemporaryDirectory:
        # Resolve macOS /var -> /private/var so the strict parent census does
        # not mistake the test harness alias for a production path alias.
        return tempfile.TemporaryDirectory(
            prefix=prefix, dir=str(Path(tempfile.gettempdir()).resolve()),
        )

    class CoordinatorAuthority:
        def __init__(self, record):
            self.stage = "TELEMETRY_ACCEPTED"
            self.record = record

        def accepted_record(self, node):
            if node != "telemetry":
                raise RuntimeError("wrong node")
            return deepcopy(self.record)

        def accepted_sha256(self, node):
            return hashlib.sha256(
                evidence.canonical_json_bytes(self.accepted_record(node))
            ).hexdigest()

    def test_a23_and_a27_are_live_validated_and_atomically_published_once(self):
        with self.temporary_directory("stage_evidence_") as directory:
            root = Path(directory)
            predecessors, outputs = self.registries(root)
            with mock.patch.object(
                evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
            ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                publisher = evidence.StageEvidencePublisher(self.validator)
                a23 = {"artifact_id": "A23_POSTRUN_TELEMETRY", "passed": True}
                a27 = {"artifact_id": "A27_MUTATION_LEDGER", "passed": True}
                a23_path = Path(outputs["A23_POSTRUN_TELEMETRY"])
                a27_path = Path(outputs["A27_MUTATION_LEDGER"])
                publisher.publish_a23(
                    str(a23_path), a23, self.CoordinatorAuthority(a23),
                )
                publisher.publish_a27(str(a27_path), a27)
                for path in (a23_path, a27_path):
                    self.assertEqual(path.stat().st_mode & 0o222, 0)
                    self.assertEqual(path.stat().st_nlink, 1)
                with self.assertRaises(evidence.OrchestrationRefusal):
                    publisher.publish_a23(
                        str(root / "A23_again.json"), a23,
                        self.CoordinatorAuthority(a23),
                    )
                with self.assertRaises(evidence.OrchestrationRefusal):
                    publisher.publish_a27(str(root / "A27_again.json"), a27)

    def test_a23_refuses_telemetry_not_accepted_by_live_coordinator(self):
        with self.temporary_directory("stage_evidence_refuse_") as directory:
            root = Path(directory)
            predecessors, outputs = self.registries(root)
            with mock.patch.object(
                evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
            ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                a23 = {"artifact_id": "A23_POSTRUN_TELEMETRY", "passed": True}
                coordinator = self.CoordinatorAuthority({
                    "artifact_id": "A23_POSTRUN_TELEMETRY", "passed": False,
                })
                with self.assertRaises(evidence.OrchestrationRefusal):
                    evidence.StageEvidencePublisher(self.validator).publish_a23(
                        outputs["A23_POSTRUN_TELEMETRY"], a23, coordinator,
                    )
                self.assertFalse(
                    Path(outputs["A23_POSTRUN_TELEMETRY"]).exists()
                )

    def test_all_24_predecessor_orders_reach_one_time_a26_publication(self):
        for order in itertools.permutations(evidence.PREDECESSOR_IDS):
            with self.temporary_directory("final_orchestrator_") as directory:
                root = Path(directory)
                predecessors, outputs = self.registries(root)
                with mock.patch.object(
                    evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
                ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                    inputs = {
                        aid: self.authority(root, aid)
                        for aid in evidence.PREDECESSOR_IDS
                    }
                    with evidence.FinalEvidenceOrchestrator(
                        self.validator,
                    ) as orchestrator:
                        for aid in order:
                            orchestrator.admit(aid, *inputs[aid])
                        self.assertEqual(
                            orchestrator.stage, "PREDECESSORS_RETAINED",
                        )
                        output = Path(outputs["A26_FINAL_L12_AUDIT"])
                        digest = orchestrator.publish_a26(
                            str(output), {
                                "artifact_id": "A26_FINAL_L12_AUDIT",
                                "passed": True,
                            },
                        )
                        self.assertEqual(
                            digest, hashlib.sha256(output.read_bytes()).hexdigest(),
                        )
                        self.assertEqual(orchestrator.stage, "A26_PUBLISHED")
                        with self.assertRaises(evidence.OrchestrationRefusal):
                            orchestrator.publish_a26(str(output), {})

    def test_missing_duplicate_writable_and_retained_drift_refuse(self):
        with self.temporary_directory("final_orchestrator_refusal_") as directory:
            root = Path(directory)
            predecessors, outputs = self.registries(root)
            with mock.patch.object(
                evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
            ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                inputs = {
                    aid: self.authority(root, aid)
                    for aid in evidence.PREDECESSOR_IDS
                }
                with evidence.FinalEvidenceOrchestrator(
                    self.validator,
                ) as orchestrator:
                    aid = evidence.PREDECESSOR_IDS[0]
                    orchestrator.admit(aid, *inputs[aid])
                    with self.assertRaises(evidence.OrchestrationRefusal):
                        orchestrator.admit(aid, *inputs[aid])
                    with self.assertRaises(evidence.OrchestrationRefusal):
                        orchestrator.publish_a26(
                            outputs["A26_FINAL_L12_AUDIT"], {},
                        )
                writable = Path(predecessors[evidence.PREDECESSOR_IDS[1]])
                writable.chmod(0o644)
                with self.assertRaises(evidence.OrchestrationRefusal):
                    evidence.open_authority(
                        evidence.PREDECESSOR_IDS[1], str(writable),
                        inputs[evidence.PREDECESSOR_IDS[1]][1], self.validator,
                    )
                writable.chmod(0o444)
                retained = []
                with evidence.FinalEvidenceOrchestrator(
                    self.validator,
                ) as orchestrator:
                    for aid in evidence.PREDECESSOR_IDS:
                        orchestrator.admit(aid, *inputs[aid])
                    retained = list(orchestrator._accepted.values())
                    drift = Path(inputs[evidence.PREDECESSOR_IDS[2]][0])
                    drift.chmod(0o644)
                    with self.assertRaises(evidence.OrchestrationRefusal):
                        orchestrator.publish_a26(
                            outputs["A26_FINAL_L12_AUDIT"], {
                                "artifact_id": "A26_FINAL_L12_AUDIT",
                                "passed": True,
                            },
                        )
                self.assertTrue(all(
                    item.descriptor == item.parent_descriptor == -1
                    for item in retained
                ))

    def test_exact_path_registry_rejects_aliases(self):
        with self.temporary_directory("evidence_alias_") as directory:
            root = Path(directory)
            predecessors, outputs = self.registries(root)
            with mock.patch.object(
                evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
            ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                artifact_id = "A24_TARGET_L12_HISTORY"
                canonical_path, digest = self.authority(root, artifact_id)
                alias = root / "alias.json"
                alias.write_bytes(Path(canonical_path).read_bytes())
                alias.chmod(0o444)
                with self.assertRaises(evidence.OrchestrationRefusal):
                    evidence.open_authority(
                        artifact_id, str(alias), digest, self.validator,
                    )
                a27 = {"artifact_id": "A27_MUTATION_LEDGER", "passed": True}
                with self.assertRaises(evidence.OrchestrationRefusal):
                    evidence.StageEvidencePublisher(self.validator).publish_a27(
                        str(root / "alias-output.json"), a27,
                    )

    def test_postlink_failure_preserves_owned_immutable_canonical_evidence(self):
        with self.temporary_directory("evidence_postlink_") as directory:
            output = Path(directory) / "output.json"
            payload = evidence.canonical_json_bytes({"passed": True})
            real_fsync = evidence.os.fsync
            calls = 0

            def fail_directory_fsync(descriptor):
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise OSError("injected post-link fsync failure")
                return real_fsync(descriptor)

            with mock.patch.object(
                evidence.os, "fsync", side_effect=fail_directory_fsync,
            ):
                with self.assertRaises(OSError):
                    evidence._atomic_publish_once(
                        str(output), payload, str(output),
                    )
            self.assertEqual(output.read_bytes(), payload)
            self.assertEqual(output.stat().st_mode & 0o222, 0)
            self.assertEqual(output.stat().st_nlink, 1)
            self.assertFalse(any(
                path.name.startswith(f".{output.name}.staging-")
                for path in output.parent.iterdir()
            ))

    def test_atomic_publish_refuses_parent_swap_without_publishing(self):
        with self.temporary_directory("evidence_parent_swap_") as directory:
            root = Path(directory)
            parent = root / "parent"
            parent.mkdir()
            moved = root / "parent-held"
            output = parent / "output.json"
            payload = evidence.canonical_json_bytes({"passed": True})
            real_parent_identity = evidence._parent_identity
            calls = 0

            def swap_on_second_check(path, descriptor, label):
                nonlocal calls
                calls += 1
                if calls == 2:
                    parent.rename(moved)
                    parent.mkdir()
                return real_parent_identity(path, descriptor, label)

            with mock.patch.object(
                evidence, "_parent_identity", side_effect=swap_on_second_check,
            ):
                with self.assertRaises(evidence.OrchestrationRefusal):
                    evidence._atomic_publish_once(
                        str(output), payload, str(output),
                    )
            self.assertFalse(output.exists())
            self.assertFalse(any(
                path.name.startswith(f".{output.name}.staging-")
                for path in moved.iterdir()
            ))

    def test_retained_path_replacement_refuses_and_closes_all_handles(self):
        with self.temporary_directory("authority_replacement_") as directory:
            root = Path(directory)
            predecessors, outputs = self.registries(root)
            with mock.patch.object(
                evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
            ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                inputs = {
                    aid: self.authority(root, aid)
                    for aid in evidence.PREDECESSOR_IDS
                }
                retained = []
                with evidence.FinalEvidenceOrchestrator(
                    self.validator,
                ) as orchestrator:
                    for aid in evidence.PREDECESSOR_IDS:
                        orchestrator.admit(aid, *inputs[aid])
                    retained = list(orchestrator._accepted.values())
                    victim = Path(inputs["A24_TARGET_L12_HISTORY"][0])
                    original = victim.with_suffix(".original")
                    victim.rename(original)
                    victim.write_bytes(original.read_bytes())
                    victim.chmod(0o444)
                    with self.assertRaises(evidence.OrchestrationRefusal):
                        orchestrator.publish_a26(
                            outputs["A26_FINAL_L12_AUDIT"], {
                                "artifact_id": "A26_FINAL_L12_AUDIT",
                                "passed": True,
                            },
                        )
                self.assertTrue(all(
                    item.descriptor == item.parent_descriptor == -1
                    for item in retained
                ))

    def test_retained_parent_symlink_replacement_refuses(self):
        with self.temporary_directory("authority_parent_alias_") as directory:
            root = Path(directory)
            authority_root = root / "authorities"
            authority_root.mkdir()
            predecessors, outputs = self.registries(authority_root)
            outputs["A26_FINAL_L12_AUDIT"] = str(root / "A26.json")
            with mock.patch.object(
                evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
            ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                inputs = {
                    aid: self.authority(authority_root, aid)
                    for aid in evidence.PREDECESSOR_IDS
                }
                with evidence.FinalEvidenceOrchestrator(
                    self.validator,
                ) as orchestrator:
                    for aid in evidence.PREDECESSOR_IDS:
                        orchestrator.admit(aid, *inputs[aid])
                    held = root / "authorities-held"
                    authority_root.rename(held)
                    authority_root.symlink_to(held.name, target_is_directory=True)
                    with self.assertRaises(evidence.OrchestrationRefusal):
                        orchestrator.publish_a26(
                            outputs["A26_FINAL_L12_AUDIT"], {
                                "artifact_id": "A26_FINAL_L12_AUDIT",
                                "passed": True,
                            },
                        )

    def test_retained_metadata_change_during_hash_refuses(self):
        with self.temporary_directory("authority_hash_race_") as directory:
            root = Path(directory)
            predecessors, outputs = self.registries(root)
            with mock.patch.object(
                evidence, "CANONICAL_PREDECESSOR_PATHS", predecessors,
            ), mock.patch.object(evidence, "CANONICAL_OUTPUT_PATHS", outputs):
                artifact_id = "A24_TARGET_L12_HISTORY"
                path, digest = self.authority(root, artifact_id)
                retained = evidence.open_authority(
                    artifact_id, path, digest, self.validator,
                )
                real_hash = evidence._descriptor_sha256

                def mutate_after_hash(descriptor):
                    result = real_hash(descriptor)
                    Path(path).chmod(0o644)
                    return result

                try:
                    with mock.patch.object(
                        evidence, "_descriptor_sha256",
                        side_effect=mutate_after_hash,
                    ):
                        with self.assertRaises(evidence.OrchestrationRefusal):
                            retained.verify()
                finally:
                    retained.close()
                self.assertEqual(retained.descriptor, -1)
                self.assertEqual(retained.parent_descriptor, -1)


if __name__ == "__main__":
    unittest.main()
