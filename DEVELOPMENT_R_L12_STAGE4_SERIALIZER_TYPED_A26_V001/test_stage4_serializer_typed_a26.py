#!/usr/bin/env python3
"""Hostile readiness tests for the mutable serializer-typed A26 bridge."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "stage4_serializer_typed_a26.py"
SPEC = importlib.util.spec_from_file_location("stage4_serializer_typed_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
compat = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = compat
SPEC.loader.exec_module(compat)


class Stage4SerializerTypedReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bridge = compat.frozen_bridge()
        cls.auditor = cls.bridge.auditor
        cls.evidence = cls.bridge.evidence
        cls.draft = compat.build_registry_draft()
        cls.registry = compat.validate_registry(
            cls.draft, require_complete=False, verify_files=True,
        )

    @staticmethod
    def _complete_synthetic_registry(
        draft: dict[str, object],
    ) -> tuple[dict[str, object], dict[str, bytes]]:
        record = copy.deepcopy(draft)
        raw_by_path: dict[str, bytes] = {}
        for item in record["entries"]:
            if item["present"]:
                continue
            value = {
                "artifact_id": item["artifact_id"],
                "instance": item["instance"],
                "relative_path": item["relative_path"],
                "synthetic_future_authority": True,
            }
            raw = compat._serialize(value, item["framing"])
            item["present"] = True
            item["bytes"] = len(raw)
            item["raw_sha256"] = hashlib.sha256(raw).hexdigest()
            raw_by_path[item["relative_path"]] = raw
        record["status"] = compat.REGISTRY_COMPLETE
        record["present_input_count"] = compat.EXPECTED_PHYSICAL_INPUTS
        record["present_framing_census"] = dict(
            compat.EXPECTED_FRAMING_CENSUS
        )
        record["missing_authorities"] = []
        return record, raw_by_path

    def test_frozen_stage4_sources_are_exact_and_retained(self) -> None:
        sources = compat._authenticate_frozen_stage4_sources()
        expected = {
            **{
                compat.FROZEN_PACKET / name: digest
                for name, digest in compat.PINNED_FROZEN_STAGE4.items()
            },
            **{
                compat.ROOT / relative: digest
                for relative, digest in compat.PINNED_FROZEN_DEPENDENCIES.items()
            },
        }
        self.assertEqual(set(sources), set(expected))
        for path, raw in sources.items():
            self.assertEqual(hashlib.sha256(raw).hexdigest(), expected[path])
        self.bridge.verify_frozen_source_closure()

    def test_preexisting_frozen_module_alias_refuses(self) -> None:
        name = "stage4_forged_preexisting_alias_probe"
        forged = types.ModuleType(name)
        forged.__file__ = str(compat.FROZEN_BRIDGE)
        forged.__authenticated_sha256__ = compat.PINNED_FROZEN_STAGE4[
            "build_final_a26.py"
        ]
        sys.modules[name] = forged
        try:
            with self.assertRaisesRegex(
                compat.CompatibilityRefusal, "alias is already occupied",
            ):
                compat._execute_frozen_bridge(name)
        finally:
            sys.modules.pop(name, None)

    def test_current_registry_is_exact_24_pretty_plus_a17(self) -> None:
        self.assertFalse(self.registry.complete)
        self.assertEqual(self.draft["logical_authority_census"], 42)
        self.assertEqual(self.draft["physical_input_census"], 50)
        self.assertEqual(self.draft["present_input_count"], 33)
        self.assertEqual(len(self.draft["missing_authorities"]), 17)
        self.assertTrue(all(
            item["raw_sha256"] == compat.PENDING_SHA256
            for item in self.draft["entries"] if not item["present"]
        ))
        self.assertEqual(self.draft["present_framing_census"], {
            compat.PRETTY: 24, compat.COMPACT: 5, compat.RAW: 4,
        })
        present = [item for item in self.draft["entries"] if item["present"]]
        ordinary_pretty = [
            item for item in present
            if item["source_label"] is None and item["framing"] == compat.PRETTY
        ]
        a17 = [item for item in present if item["source_label"] is not None]
        self.assertEqual(len(ordinary_pretty), 24)
        self.assertEqual(len(a17), 9)
        self.assertEqual(
            self.draft["a17_logical_composite_sha256"],
            "ad9c4c30b6bc199000a5c3f50bde6711adab35cc4bbdcfa19787051bea9ca21e",
        )

    def test_synthetic_future_census_has_pretty_a24_only(self) -> None:
        complete, raw_by_path = self._complete_synthetic_registry(self.draft)
        validated = compat.validate_registry(
            complete, require_complete=True, verify_files=False,
        )
        self.assertTrue(validated.complete)
        self.assertEqual(len(raw_by_path), 17)
        for item in complete["entries"]:
            if item["relative_path"] not in raw_by_path:
                continue
            raw = raw_by_path[item["relative_path"]]
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(), item["raw_sha256"],
            )
            compat._require_exact_frame(
                raw, item["framing"], item["relative_path"],
            )
            if item["artifact_id"] == "A24_TARGET_L12_HISTORY":
                self.assertEqual(item["framing"], compat.PRETTY)
            else:
                self.assertEqual(item["framing"], compat.COMPACT)

    def test_complete_registry_cannot_skip_file_verification(self) -> None:
        complete, _raw = self._complete_synthetic_registry(self.draft)
        with self.assertRaises(compat.CompatibilityRefusal):
            compat.validate_registry(
                complete, require_complete=True, verify_files=True,
            )

    def test_registry_order_path_mode_hash_and_absence_mutations_refuse(self) -> None:
        mutations = []
        swapped = copy.deepcopy(self.draft)
        swapped["entries"][0], swapped["entries"][1] = (
            swapped["entries"][1], swapped["entries"][0]
        )
        mutations.append(swapped)
        duplicate_path = copy.deepcopy(self.draft)
        duplicate_path["entries"][1]["relative_path"] = (
            duplicate_path["entries"][0]["relative_path"]
        )
        mutations.append(duplicate_path)
        wrong_mode = copy.deepcopy(self.draft)
        wrong_mode["entries"][0]["framing"] = compat.COMPACT
        mutations.append(wrong_mode)
        absent_current = copy.deepcopy(self.draft)
        absent_current["entries"][0].update({
            "present": False, "bytes": None, "raw_sha256": None,
        })
        mutations.append(absent_current)
        replaced_current = copy.deepcopy(self.draft)
        replaced_current["entries"][0]["raw_sha256"] = "0" * 64
        mutations.append(replaced_current)
        extra = copy.deepcopy(self.draft)
        extra["entries"].append(copy.deepcopy(extra["entries"][-1]))
        mutations.append(extra)
        for mutation in mutations:
            with self.subTest(index=mutations.index(mutation)):
                with self.assertRaises(compat.CompatibilityRefusal):
                    compat.validate_registry(
                        mutation, require_complete=False, verify_files=False,
                    )

    def test_raw_hash_is_not_semantic_compact_rehash(self) -> None:
        for artifact_id in (
            "A01_FREEZE_AND_SOURCE_PACKET", "A18_L10_CROSS_GATE",
            "A27_MUTATION_LEDGER",
        ):
            item = next(
                row for row in self.draft["entries"]
                if row["artifact_id"] == artifact_id
                and row["source_label"] is None
            )
            raw = (compat.ROOT / item["relative_path"]).read_bytes()
            parsed = compat._strict_object(raw, artifact_id)
            compact = compat._serialize(parsed, compat.COMPACT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["raw_sha256"])
            self.assertNotEqual(raw, compact)
            self.assertNotEqual(
                item["raw_sha256"], hashlib.sha256(compact).hexdigest(),
            )

    def test_current_authority_discovery_uses_predeclared_hash(self) -> None:
        item = next(
            spec for spec in compat.expected_input_specs()
            if spec.artifact_id == "A01_FREEZE_AND_SOURCE_PACKET"
        )
        expected = compat.PINNED_CURRENT_AUTHORITY_SHA256[item.key]
        with mock.patch.object(
            compat, "_read_exact_owner_once",
            side_effect=compat.CompatibilityRefusal("captured pinned call"),
        ) as reader:
            with self.assertRaisesRegex(
                compat.CompatibilityRefusal, "captured pinned call",
            ):
                compat._discover_entry(item)
        reader.assert_called_once_with(
            compat.ROOT / item.relative_path,
            expected,
            "Stage4 registry A01_FREEZE_AND_SOURCE_PACKET:1:None",
        )

    def test_future_authority_is_pending_and_cannot_self_authenticate(self) -> None:
        item = next(
            spec for spec in compat.expected_input_specs()
            if spec.artifact_id == "A20_SHARED_SCHEDULE_GATE"
        )
        with mock.patch.object(compat.os.path, "lexists", return_value=True), \
             mock.patch.object(compat, "_read_exact_owner_once") as reader:
            discovered = compat._discover_entry(item)
        self.assertFalse(discovered["present"])
        self.assertEqual(discovered["raw_sha256"], compat.PENDING_SHA256)
        reader.assert_not_called()

    def test_retry_v002_authority_namespace_is_exact_and_disjoint(self) -> None:
        expected = {
            ("A20_SHARED_SCHEDULE_GATE", 1):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "SHARED_AGGREGATE_SCHEDULE_GATE_RETRY_V002.json",
            ("A21_SHARED_SCHEDULE_AUDIT", 1):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 1):
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                "TARGET_L12_EXECUTION_GATE_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 2):
                "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
                "HOSTILE_L12_EXECUTION_GATE_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 3):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "TARGET_V012_WORKER_READY_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 4):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "HOSTILE_V004R4_WORKER_READY_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 5):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "DUAL_L12_LAUNCH_HANDSHAKE_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 6):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "DUAL_L12_WORKER_RELEASE_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 7):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "TARGET_V012_WORKER_RELEASE_COMMAND_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 8):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "HOSTILE_V004R4_WORKER_RELEASE_COMMAND_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 9):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "TARGET_V012_WORKER_RELEASE_ACK_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 10):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "HOSTILE_V004R4_WORKER_RELEASE_ACK_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 11):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "TARGET_V012_WORKER_COMPLETION_RETRY_V002.json",
            ("A22_TARGET_L12_AUTHORIZATION", 12):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "HOSTILE_V004R4_WORKER_COMPLETION_RETRY_V002.json",
            ("A23_POSTRUN_TELEMETRY", 1):
                "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
                "SHARED_AGGREGATE_TELEMETRY_RETRY_V002.json",
        }
        self.assertEqual(compat.RETRY_V002_AUTHORITY_RELATIVE_PATHS, expected)
        specs = {
            (item.artifact_id, item.instance): item.relative_path
            for item in compat.expected_input_specs()
        }
        self.assertEqual(
            {key: specs[key] for key in expected}, expected,
        )
        for key, retry_path in expected.items():
            self.assertNotEqual(
                retry_path,
                self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[key],
            )
        self.assertEqual(
            specs[("A24_TARGET_L12_HISTORY", 1)],
            self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[
                ("A24_TARGET_L12_HISTORY", 1)
            ],
        )
        self.assertEqual(
            specs[("A25_HOSTILE_L12_HISTORY", 1)],
            self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[
                ("A25_HOSTILE_L12_HISTORY", 1)
            ],
        )

    def test_failed_v001_paths_cannot_satisfy_retry_authorities(self) -> None:
        for key, retry_path in compat.RETRY_V002_AUTHORITY_RELATIVE_PATHS.items():
            artifact_id, instance = key
            old_path = self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[key]
            item = next(
                row for row in self.draft["entries"]
                if row["artifact_id"] == artifact_id
                and row["instance"] == instance
            )
            self.assertEqual(item["relative_path"], retry_path)
            self.assertIsNone(
                self.registry.lookup(compat.ROOT / old_path, "0" * 64)
            )
            replaced = copy.deepcopy(self.draft)
            changed = next(
                row for row in replaced["entries"]
                if row["artifact_id"] == artifact_id
                and row["instance"] == instance
            )
            changed["relative_path"] = old_path
            with self.assertRaisesRegex(
                compat.CompatibilityRefusal, "registry entry identity/order",
            ):
                compat.validate_registry(
                    replaced, require_complete=False, verify_files=False,
                )

    def test_scope_retargets_only_a20_through_a23_path_consumers(self) -> None:
        original_authority_paths = dict(
            self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS
        )
        original_predecessors = dict(self.evidence.CANONICAL_PREDECESSOR_PATHS)
        original_outputs = dict(self.evidence.CANONICAL_OUTPUT_PATHS)
        original_expected_path = self.auditor._expected_path
        with compat._typed_read_scope(self.registry, readiness_test=True):
            for key, relative in (
                compat.RETRY_V002_AUTHORITY_RELATIVE_PATHS.items()
            ):
                self.assertEqual(
                    self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[key],
                    relative,
                )
            untouched = set(original_authority_paths) - set(
                compat.RETRY_V002_AUTHORITY_RELATIVE_PATHS
            )
            self.assertTrue(all(
                self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[key]
                == original_authority_paths[key]
                for key in untouched
            ))
            self.assertEqual(
                self.evidence.CANONICAL_PREDECESSOR_PATHS[
                    "A23_POSTRUN_TELEMETRY"
                ], str(compat.RETRY_V002_TELEMETRY_PATH),
            )
            self.assertEqual(
                self.evidence.CANONICAL_OUTPUT_PATHS[
                    "A23_POSTRUN_TELEMETRY"
                ], str(compat.RETRY_V002_TELEMETRY_PATH),
            )
            for mapping_name, original, current in (
                ("predecessor", original_predecessors,
                 self.evidence.CANONICAL_PREDECESSOR_PATHS),
                ("output", original_outputs,
                 self.evidence.CANONICAL_OUTPUT_PATHS),
            ):
                with self.subTest(mapping=mapping_name):
                    self.assertTrue(all(
                        current[key] == value
                        for key, value in original.items()
                        if key != "A23_POSTRUN_TELEMETRY"
                    ))
            self.assertEqual(
                self.auditor._expected_path(
                    "target_v012", "telemetry", False,
                ), str(compat.RETRY_V002_TELEMETRY_PATH),
            )
            self.assertEqual(
                self.auditor._expected_path(
                    "target_v012", "history", False,
                ), original_expected_path(
                    "target_v012", "history", False,
                ),
            )
        self.assertEqual(
            self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS,
            original_authority_paths,
        )
        self.assertEqual(
            self.evidence.CANONICAL_PREDECESSOR_PATHS, original_predecessors,
        )
        self.assertEqual(self.evidence.CANONICAL_OUTPUT_PATHS, original_outputs)
        self.assertIs(self.auditor._expected_path, original_expected_path)

    def test_live_binding_builder_selects_retry_not_failed_paths(self) -> None:
        failed_paths = {
            key: relative
            for key, relative in self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS.items()
            if key in compat.RETRY_V002_AUTHORITY_RELATIVE_PATHS
        }
        synthetic_a17 = {
            "artifact_id": "A17_HOSTILE_L12_ELIGIBILITY",
            "instance": 1,
            "sources": [],
            "sha256": "2" * 64,
        }
        with compat._typed_read_scope(self.registry, readiness_test=True), \
             mock.patch.object(Path, "is_file", return_value=True), \
             mock.patch.object(self.bridge, "sha256_file", return_value="1" * 64), \
             mock.patch.object(
                 self.bridge, "build_a17_binding", return_value=synthetic_a17,
             ):
            bindings = self.bridge.build_authority_bindings(compat.ROOT)
        selected = {
            (row["artifact_id"], row["instance"]):
                str(Path(row["path"]).relative_to(compat.ROOT))
            for row in bindings
            if row["artifact_id"] in {
                "A20_SHARED_SCHEDULE_GATE", "A21_SHARED_SCHEDULE_AUDIT",
                "A22_TARGET_L12_AUTHORIZATION", "A23_POSTRUN_TELEMETRY",
            }
        }
        self.assertEqual(
            selected, compat.RETRY_V002_AUTHORITY_RELATIVE_PATHS,
        )
        self.assertTrue(all(
            selected[key] != failed_paths[key] for key in selected
        ))

    def test_duplicate_nonfinite_nonascii_and_reformat_refuse(self) -> None:
        invalid = (
            (b'{"a":1,"a":2}\n', compat.COMPACT),
            (b'{"a":NaN}\n', compat.COMPACT),
            (b'{"a":"\xff"}\n', compat.COMPACT),
            (b'{"a":1} \n', compat.COMPACT),
            (b'{\n  "a": 1\n}\r\n', compat.PRETTY),
            (b'{"a":1}\n', compat.PRETTY),
        )
        for raw, framing in invalid:
            with self.subTest(raw=raw, framing=framing):
                with self.assertRaises(compat.CompatibilityRefusal):
                    compat._require_exact_frame(raw, framing, "hostile fixture")

    def test_bridge_auditor_and_evidence_pretty_boundaries(self) -> None:
        a27 = next(
            item for item in self.draft["entries"]
            if item["artifact_id"] == "A27_MUTATION_LEDGER"
        )
        a01 = next(
            item for item in self.draft["entries"]
            if item["artifact_id"] == "A01_FREEZE_AND_SOURCE_PACKET"
        )
        a27_path = compat.ROOT / a27["relative_path"]
        a01_path = compat.ROOT / a01["relative_path"]
        with self.assertRaises(self.bridge.BridgeRefusal):
            self.bridge.open_canonical_record(
                a27_path, a27["raw_sha256"], "unpatched A27",
            )
        with self.assertRaises(self.auditor.Refusal):
            self.auditor._open_immutable_json(
                str(a01_path), a01["raw_sha256"],
                "A26_FINAL_L12_AUDIT", "unpatched A01",
            )
        with self.assertRaises(self.evidence.OrchestrationRefusal):
            self.evidence.open_authority(
                "A27_MUTATION_LEDGER", str(a27_path), a27["raw_sha256"],
                lambda *_args, **_kwargs: {},
            )
        originals = (
            self.bridge.open_canonical_record,
            self.auditor._open_immutable_json,
            self.evidence.open_authority,
            self.evidence.canonical_json_bytes,
        )
        with compat._typed_read_scope(self.registry, readiness_test=True):
            record, held = self.bridge.open_canonical_record(
                a27_path, a27["raw_sha256"], "A27_MUTATION_LEDGER",
            )
            try:
                self.assertEqual(record["schema"], "TARGET_V012_PREPAYLOAD_MUTATION_LEDGER_V001")
                held.verify()
            finally:
                held.close()
            record, held = self.auditor._open_immutable_json(
                str(a01_path), a01["raw_sha256"],
                "A26_FINAL_L12_AUDIT",
                "authority A01_FREEZE_AND_SOURCE_PACKET:1",
            )
            try:
                self.assertEqual(record["schema"], "TARGET_L12_STORAGE_CACHE_FREEZE_V012")
                held.verify()
            finally:
                held.close()
            validator_serialization = {}

            def validator(_artifact_id, value, **_kwargs):
                validator_serialization["raw"] = (
                    self.evidence.canonical_json_bytes(value)
                )
                return {}

            held = self.evidence.open_authority(
                "A27_MUTATION_LEDGER", str(a27_path), a27["raw_sha256"],
                validator,
            )
            try:
                self.assertEqual(held.record["schema"], "TARGET_V012_PREPAYLOAD_MUTATION_LEDGER_V001")
                held.verify()
            finally:
                held.close()
            self.assertEqual(
                validator_serialization["raw"], originals[3](held.record),
            )
            self.assertNotEqual(
                validator_serialization["raw"], a27_path.read_bytes(),
            )
            value = {"future_A26": True}
            self.assertEqual(
                self.evidence.canonical_json_bytes(value),
                originals[3](value),
            )
        self.assertEqual((
            self.bridge.open_canonical_record,
            self.auditor._open_immutable_json,
            self.evidence.open_authority,
            self.evidence.canonical_json_bytes,
        ), originals)

    def test_bridge_and_auditor_registered_identity_mismatch_refuses(self) -> None:
        a27 = next(
            item for item in self.draft["entries"]
            if item["artifact_id"] == "A27_MUTATION_LEDGER"
        )
        a01 = next(
            item for item in self.draft["entries"]
            if item["artifact_id"] == "A01_FREEZE_AND_SOURCE_PACKET"
        )
        with compat._typed_read_scope(self.registry, readiness_test=True):
            with self.assertRaisesRegex(
                compat.CompatibilityRefusal, "bridge authority registry identity",
            ):
                self.bridge.open_canonical_record(
                    compat.ROOT / a27["relative_path"],
                    a27["raw_sha256"], "A18_L10_CROSS_GATE",
                )
            for aid, label in (
                ("A25_HOSTILE_L12_HISTORY",
                 "authority A01_FREEZE_AND_SOURCE_PACKET:1"),
                ("A26_FINAL_L12_AUDIT", "authority A02_NONPHYSICAL_PREFLIGHT:1"),
            ):
                with self.subTest(aid=aid, label=label):
                    with self.assertRaisesRegex(
                        compat.CompatibilityRefusal,
                        "auditor authority registry identity",
                    ):
                        self.auditor._open_immutable_json(
                            str(compat.ROOT / a01["relative_path"]),
                            a01["raw_sha256"], aid, label,
                        )

    def test_active_scope_rechecks_authenticated_runtime_identities(self) -> None:
        a27 = next(
            item for item in self.draft["entries"]
            if item["artifact_id"] == "A27_MUTATION_LEDGER"
        )
        original = self.auditor.validate_artifact
        with compat._typed_read_scope(self.registry, readiness_test=True):
            self.auditor.validate_artifact = lambda *_args, **_kwargs: {}
            try:
                with self.assertRaisesRegex(
                    compat.CompatibilityRefusal,
                    "authenticated frozen runtime callable changed",
                ):
                    self.bridge.open_canonical_record(
                        compat.ROOT / a27["relative_path"],
                        a27["raw_sha256"], "A27_MUTATION_LEDGER",
                    )
            finally:
                self.auditor.validate_artifact = original

    def test_active_scope_rechecks_authenticated_runtime_structure(self) -> None:
        a27 = next(
            item for item in self.draft["entries"]
            if item["artifact_id"] == "A27_MUTATION_LEDGER"
        )
        key = ("A01_FREEZE_AND_SOURCE_PACKET", 1)
        paths = self.auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS
        original = paths[key]
        with compat._typed_read_scope(self.registry, readiness_test=True):
            paths[key] = a27["relative_path"]
            try:
                with self.assertRaisesRegex(
                    compat.CompatibilityRefusal,
                    "authenticated frozen runtime structure changed",
                ):
                    self.bridge.open_canonical_record(
                        compat.ROOT / a27["relative_path"],
                        a27["raw_sha256"], "A27_MUTATION_LEDGER",
                    )
            finally:
                paths[key] = original

    def test_nonregistered_compact_input_delegates_exactly(self) -> None:
        path = compat.FROZEN_PACKET / "SOURCE_FREEZE.json"
        digest = compat.PINNED_FROZEN_STAGE4["SOURCE_FREEZE.json"]
        original_record, original_held = self.auditor._open_immutable_json(
            str(path), digest, "A26_FINAL_L12_AUDIT", "unregistered compact",
        )
        original_held.close()
        with compat._typed_read_scope(self.registry, readiness_test=True):
            record, held = self.auditor._open_immutable_json(
                str(path), digest, "A26_FINAL_L12_AUDIT", "unregistered compact",
            )
            try:
                self.assertEqual(record, original_record)
                self.assertEqual(held.digest, digest)
            finally:
                held.close()

    def test_registered_hash_mismatch_refuses_before_delegation(self) -> None:
        item = next(
            row for row in self.draft["entries"]
            if row["artifact_id"] == "A18_L10_CROSS_GATE"
        )
        with self.assertRaisesRegex(
            compat.CompatibilityRefusal, "authority hash mismatch",
        ):
            self.registry.lookup(
                compat.ROOT / item["relative_path"], "0" * 64,
            )

    def test_scope_restores_on_failure_and_revokes_captured_functions(self) -> None:
        original = self.bridge.open_canonical_record
        leaked = None
        with self.assertRaisesRegex(RuntimeError, "injected"):
            with compat._typed_read_scope(self.registry, readiness_test=True):
                leaked = self.bridge.open_canonical_record
                raise RuntimeError("injected")
        self.assertIs(self.bridge.open_canonical_record, original)
        self.assertIsNotNone(leaked)
        a27 = next(
            item for item in self.draft["entries"]
            if item["artifact_id"] == "A27_MUTATION_LEDGER"
        )
        with self.assertRaisesRegex(
            compat.CompatibilityRefusal, "capability expired",
        ):
            leaked(
                compat.ROOT / a27["relative_path"],
                a27["raw_sha256"], "expired",
            )

    def test_scope_detects_boundary_tamper_and_restores(self) -> None:
        original = self.bridge.open_canonical_record
        with self.assertRaisesRegex(
            compat.CompatibilityRefusal, "changed in scope",
        ):
            with compat._typed_read_scope(self.registry, readiness_test=True):
                self.bridge.open_canonical_record = lambda *_args: None
        self.assertIs(self.bridge.open_canonical_record, original)

    def test_incomplete_registry_cannot_enter_production_scope(self) -> None:
        with self.assertRaisesRegex(
            compat.CompatibilityRefusal, "incomplete registry",
        ):
            with compat._typed_read_scope(self.registry):
                self.fail("incomplete registry entered production scope")
        with self.assertRaises(compat.CompatibilityRefusal):
            compat.open_complete_registry(
                compat.FINAL_REGISTRY_PATH, "0" * 64,
            )

    def test_plan_and_tests_preserve_all_canonical_absences(self) -> None:
        paths = [
            compat.ROOT / spec.relative_path
            for spec in compat.expected_input_specs()
            if spec.artifact_id in compat.FUTURE_ARTIFACT_IDS
        ]
        paths.append(Path(
            self.evidence.CANONICAL_OUTPUT_PATHS["A26_FINAL_L12_AUDIT"]
        ))
        before = {str(path): os.path.lexists(path) for path in paths}
        result = compat.plan()
        after = {str(path): os.path.lexists(path) for path in paths}
        self.assertEqual(before, after)
        self.assertFalse(after[str(paths[-1])])
        self.assertEqual(
            result["observed_pending_input_count"],
            sum(before[str(path)] for path in paths[:-1]),
        )
        self.assertEqual(
            result["classification"],
            "MUTABLE_READINESS_ONLY_NOT_EXECUTABLE_CERTIFICATION",
        )
        self.assertFalse(result["published"])
        self.assertFalse(result["executed"])

    def test_cli_exposes_plan_only(self) -> None:
        for args in ([], ["publish"], ["execute"], ["plan", "extra"]):
            error = io.StringIO()
            with mock.patch.object(compat.sys, "argv", [str(SOURCE), *args]), \
                 redirect_stderr(error):
                self.assertEqual(compat.main(), 2)
            self.assertIn("exposes only plan", error.getvalue())

    def test_owner_once_reader_refuses_writable_hardlink_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage4-custody-", dir=HERE) as raw:
            directory = Path(raw).resolve()
            payload = b'{"fixture":true}\n'
            writable = directory / "writable.json"
            writable.write_bytes(payload)
            immutable = directory / "immutable.json"
            immutable.write_bytes(payload)
            immutable.chmod(0o444)
            linked = directory / "linked.json"
            os.link(immutable, linked)
            symlink = directory / "symlink.json"
            symlink.symlink_to(immutable)
            digest = hashlib.sha256(payload).hexdigest()
            for path in (writable, immutable, symlink):
                with self.subTest(path=path):
                    with self.assertRaises(compat.CompatibilityRefusal):
                        compat._read_exact_owner_once(path, digest, "custody fixture")


if __name__ == "__main__":
    unittest.main(verbosity=2)
