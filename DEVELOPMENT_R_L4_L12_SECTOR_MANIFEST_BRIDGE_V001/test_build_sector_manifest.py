#!/usr/bin/env python3
"""Positive, adverse, and owner-once sector-manifest bridge tests."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


bridge = load_module("sector_manifest_bridge", HERE / "build_sector_manifest.py")
target = load_module(
    "target_interval_driver_for_bridge_test",
    ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "interval_spectrum_driver.py",
)
blind = load_module(
    "blind_freeze_builder_for_bridge_test",
    ROOT / "AUDIT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "build_blind_freeze.py",
)


class SectorManifestBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(tempfile.mkdtemp(prefix="manifest_bridge_", dir=HERE))
        protocol_dir = (
            self.directory / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
        )
        protocol_dir.mkdir()
        shutil.copyfile(
            ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md",
            protocol_dir / "PROTOCOL.md",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)

    @staticmethod
    def history(length: int, delta: float = 0.0) -> dict[str, object]:
        rows = []
        for event in range(1, length + 1):
            weights = [0.0] * (length + 1)
            weights[length // 2] = 1.0
            if length in (4, 6, 8):
                weights.extend([0.0] * length)
            rows.append({
                "event": event,
                "sector_weights": weights,
                "W_n": 0.5 + delta,
                "allow_probability": 1.0 + delta,
                "blocked_probability": 0.1 + delta,
                "reverse_support_probability": 0.0 + delta,
                "connector_delta_l1": 0.2 + delta,
                "connector_delta_signed": 0.0 + delta,
                "q_retained_after_transport": float(event) + delta,
                "q_genesis_after": float(length - event) - delta,
            })
        return {
            "L": length,
            "dimension": 3 * length,
            "comparison": {"resolved": True},
            "rows": rows,
        }

    def write_sources(self) -> dict[int, dict[str, str]]:
        sources: dict[int, dict[str, str]] = {}
        for length in bridge.SIZES:
            canonical = bridge.CANONICAL_SOURCES[length]
            target_path = self.directory / canonical["target"]
            blind_path = self.directory / canonical["blind"]
            audit_path = self.directory / canonical["audit"]
            target_path.parent.mkdir(parents=True, exist_ok=True)
            blind_path.parent.mkdir(parents=True, exist_ok=True)
            audit_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(json.dumps(self.history(length), sort_keys=True))
            blind_path.write_text(json.dumps(self.history(length), sort_keys=True))
            target_hash = bridge.sha256_file(target_path)
            blind_hash = bridge.sha256_file(blind_path)
            sources[length] = {
                "target_path": canonical["target"],
                "target_sha256": target_hash,
                "blind_path": canonical["blind"],
                "blind_sha256": blind_hash,
                "audit_path": canonical["audit"],
                "audit_sha256": "0" * 64,
            }
        seed = {
            "schema": "SCALABLE_RELATIONAL_ACCUMULATION_SEED_HOSTILE_V001",
            "classification": "PASS_RELATIONAL_ACCUMULATION_SEED_L4_L8",
            "checks_passed": 205,
            "checks_total": 205,
            "failures": [],
            "target_hashes": {
                str(length): sources[length]["target_sha256"]
                for length in (4, 6, 8)
            },
            "blind_hashes": {
                str(length): sources[length]["blind_sha256"]
                for length in (4, 6, 8)
            },
        }
        l10 = {
            "schema": "L10_V002_MEMORY_REPAIR_HOSTILE_RESULT_V001",
            "classification": (
                "PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_RESOURCE_BLOCKED"
            ),
            "checks_passed": 42,
            "checks_total": 42,
            "failures": [],
            "target_sha256": sources[10]["target_sha256"],
            "blind_sha256": sources[10]["blind_sha256"],
        }
        self.lineage_sources = {}
        for label, binding in bridge.STAGE2_LINEAGE_SOURCES.items():
            path = self.directory / binding["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            if label.startswith("target_L"):
                length = int(label.removeprefix("target_L"))
                path.write_text(json.dumps(self.history(length), sort_keys=True))
            elif label == "hostile_L10":
                path.write_text(json.dumps(self.history(10), sort_keys=True))
        control = {
            "schema": "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001",
            "classification": "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8",
            "checks_passed": 47,
            "checks_total": 47,
            "failures": [],
            "history_sha256_by_L": {
                str(length): bridge.sha256_file(
                    self.directory
                    / bridge.STAGE2_LINEAGE_SOURCES[f"target_L{length}"]["path"]
                )
                for length in (4, 6, 8)
            },
        }
        l10_stage2 = {
            "schema": "TARGET_V012_CACHED_L10_GATE_AUDIT_V001",
            "classification": "PASS_INDEPENDENT_TARGET_V012_CACHED_L10",
            "checks_passed": 25,
            "checks_total": 25,
            "failures": [],
            "history_sha256_by_L": {
                "10": bridge.sha256_file(
                    self.directory
                    / bridge.STAGE2_LINEAGE_SOURCES["target_L10"]["path"]
                )
            },
        }
        a18 = {
            "schema": "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001",
            "classification": "PASS_EXACT_TARGET_HOSTILE_L10_CROSS_BENCHMARK",
            "checks_passed": 65,
            "checks_total": 65,
            "failures": [],
            "target": {"history_sha256": l10_stage2["history_sha256_by_L"]["10"]},
            "hostile": {
                "history_sha256": bridge.sha256_file(
                    self.directory
                    / bridge.STAGE2_LINEAGE_SOURCES["hostile_L10"]["path"]
                )
            },
        }
        for label, record in (
            ("control_audit", control), ("l10_audit", l10_stage2),
            ("a18_cross_gate", a18),
        ):
            path = self.directory / bridge.STAGE2_LINEAGE_SOURCES[label]["path"]
            path.write_text(json.dumps(record, sort_keys=True))
        for label, binding in bridge.STAGE2_LINEAGE_SOURCES.items():
            path = self.directory / binding["path"]
            self.lineage_sources[label] = {
                "path": binding["path"], "sha256": bridge.sha256_file(path),
            }

        for label, relative in bridge.A17_CANONICAL_SOURCES.items():
            path = self.directory / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if label in bridge.A17_RECORD_IDENTITIES:
                schema, field, value = bridge.A17_RECORD_IDENTITIES[label]
                path.write_text(json.dumps({"schema": schema, field: value}, sort_keys=True))
            else:
                path.write_text(f"fixture A17 {label}\n")
        a17_sources = []
        a17_branch = {"role": "hostile_v004r4"}
        for label in bridge.A17_SOURCE_LABELS:
            relative = bridge.A17_CANONICAL_SOURCES[label]
            path = self.directory / relative
            digest = bridge.sha256_file(path)
            absolute = str(path.resolve())
            a17_sources.append({"label": label, "path": absolute, "sha256": digest})
            branch_binding = {"path": absolute, "sha256": digest}
            if label in bridge.A17_RECORD_IDENTITIES:
                schema, field, value = bridge.A17_RECORD_IDENTITIES[label]
                branch_binding.update({
                    "schema": schema, "identity_field": field,
                    "identity_value": value,
                })
            a17_branch[label] = branch_binding
        a17_binding = {
            "artifact_id": "A17_HOSTILE_L12_ELIGIBILITY", "instance": 1,
            "sources": a17_sources,
            "sha256": hashlib.sha256(
                bridge.canonical_json_bytes(a17_branch)
            ).hexdigest(),
        }
        l12_bindings = []
        for artifact_id, count in bridge.AUTHORITY_INSTANCE_CENSUS.items():
            for instance in range(1, count + 1):
                if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY":
                    l12_bindings.append(a17_binding)
                    continue
                relative = bridge.AUTHORITY_CANONICAL_SOURCES[(artifact_id, instance)]
                path = self.directory / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    path.write_text(json.dumps({
                        "fixture": f"{artifact_id}:{instance}",
                    }, sort_keys=True))
                l12_bindings.append({
                    "artifact_id": artifact_id, "instance": instance,
                    "path": str(path.resolve()), "sha256": bridge.sha256_file(path),
                })
        l12 = {
            "schema": "TARGET_V012_HOSTILE_V004R4_FINAL_L12_AUDIT_V001",
            "classification": "PASS_FINITE_L12_TARGET_HOSTILE_ACCUMULATION",
            "auditor_role": "INDEPENDENT_FINAL_L12_AUDITOR",
            "authority_bindings": l12_bindings,
            "authority_records_authenticated": 42,
            "checks": dict(bridge.A26_CHECKS),
            "checks_passed": 119,
            "checks_total": 119,
            "failures": [],
        }
        for length, audit in ((4, seed), (10, l10), (12, l12)):
            audit_path = self.directory / bridge.CANONICAL_SOURCES[length]["audit"]
            audit_path.write_text(json.dumps(audit, sort_keys=True))
        for length in bridge.SIZES:
            audit_path = self.directory / sources[length]["audit_path"]
            sources[length]["audit_sha256"] = bridge.sha256_file(audit_path)
        return sources

    def build_manifest(
        self, sources: dict[int, dict[str, str]],
    ) -> dict[str, object]:
        return bridge.build_manifest(
            sources, self.lineage_sources, self.directory,
        )

    def rewrite_audit(
        self, sources: dict[int, dict[str, str]], length: int,
        value: dict[str, object] | str,
    ) -> None:
        audit_path = self.directory / sources[length]["audit_path"]
        audit_path.write_text(
            value if type(value) is str else json.dumps(value, sort_keys=True)
        )
        digest = bridge.sha256_file(audit_path)
        for row in sources.values():
            if row["audit_path"] == sources[length]["audit_path"]:
                row["audit_sha256"] = digest

    def test_positive_manifest_passes_both_frozen_consumers(self) -> None:
        manifest = self.build_manifest(self.write_sources())
        self.assertEqual(
            manifest["accumulation_protocol_sha256"],
            manifest["scalable_accumulation_protocol_sha256"],
        )
        output = self.directory / "manifest.json"
        digest = bridge.publish_once(output, manifest)
        # The target consumer fixes its repository root.  Copy the temporary
        # source tree beneath that root and express paths relative to it.
        relative_prefix = self.directory.relative_to(ROOT).as_posix()
        adjusted = json.loads(json.dumps(manifest))
        for entry in adjusted["histories"].values():
            for key in (
                "target_history_path", "blind_history_path", "hostile_audit_path",
            ):
                entry[key] = f"{relative_prefix}/{entry[key]}"
        adjusted_output = self.directory / "manifest_for_target.json"
        adjusted_digest = bridge.publish_once(adjusted_output, adjusted)
        validated = target.validate_manifest(adjusted_output, adjusted_digest)
        self.assertEqual(validated["manifest"]["status"], bridge.STATUS)
        plan = blind.reconstruct_plan(adjusted, adjusted_digest)
        self.assertEqual(plan["schema"], blind.PLAN_SCHEMA)
        self.assertTrue(plan["positive_q_sector_plan"])
        self.assertEqual(digest, hashlib.sha256(output.read_bytes()).hexdigest())

    def test_adverse_fail_audit_with_pass_comment_and_hashes_is_refused(self) -> None:
        attacks = (
            ("FAIL_RELATIONAL_ACCUMULATION_L10", [], "classification"),
            (
                "PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_RESOURCE_BLOCKED",
                ["hostile mismatch"],
                "failure ledger",
            ),
            (
                "FAIL_RELATIONAL_ACCUMULATION_L10",
                ["hostile mismatch"],
                "combined",
            ),
        )
        for classification, failures, label in attacks:
            with self.subTest(label=label):
                sources = self.write_sources()
                audit_path = self.directory / sources[10]["audit_path"]
                audit = json.loads(audit_path.read_text())
                audit["classification"] = classification
                audit["failures"] = failures
                audit["comment"] = (
                    "NOT A PASS " + sources[10]["target_sha256"] + " "
                    + sources[10]["blind_sha256"]
                )
                self.rewrite_audit(sources, 10, audit)
                with self.assertRaisesRegex(
                    bridge.ManifestRefusal, "identity/result mismatch",
                ):
                    self.build_manifest(sources)

    def test_adverse_audit_duplicate_and_nonfinite_json_are_refused(self) -> None:
        for attack in (
            '{"schema":"one","schema":"two"}',
            '{"schema":"one","probe":NaN}',
        ):
            with self.subTest(attack=attack):
                sources = self.write_sources()
                self.rewrite_audit(sources, 10, attack)
                with self.assertRaisesRegex(
                    bridge.ManifestRefusal,
                    "duplicate JSON key|nonfinite JSON constant",
                ):
                    self.build_manifest(sources)

    def test_adverse_audit_schema_count_and_hash_bindings_are_refused(self) -> None:
        mutations = (
            ("schema", "WRONG_SCHEMA", "identity/result mismatch"),
            ("checks_total", 43, "identity/result mismatch"),
            ("checks_passed", 41, "identity/result mismatch"),
            ("target_sha256", "f" * 64, "history binding mismatch"),
            ("blind_sha256", "e" * 64, "history binding mismatch"),
        )
        for key, value, message in mutations:
            with self.subTest(key=key):
                sources = self.write_sources()
                audit_path = self.directory / sources[10]["audit_path"]
                audit = json.loads(audit_path.read_text())
                audit[key] = value
                self.rewrite_audit(sources, 10, audit)
                with self.assertRaisesRegex(bridge.ManifestRefusal, message):
                    self.build_manifest(sources)

    def test_adverse_noncanonical_source_path_is_refused(self) -> None:
        sources = self.write_sources()
        sources[8]["target_path"] = sources[6]["target_path"]
        sources[8]["target_sha256"] = sources[6]["target_sha256"]
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "canonical source path mismatch",
        ):
            self.build_manifest(sources)

    def test_adverse_l12_authority_path_or_hash_binding_is_refused(self) -> None:
        for key, value in (("path", "/wrong/history.json"), ("sha256", "f" * 64)):
            with self.subTest(key=key):
                sources = self.write_sources()
                audit_path = self.directory / sources[12]["audit_path"]
                audit = json.loads(audit_path.read_text())
                target_binding = next(
                    row for row in audit["authority_bindings"]
                    if row["artifact_id"] == "A24_TARGET_L12_HISTORY"
                )
                target_binding[key] = value
                self.rewrite_audit(sources, 12, audit)
                with self.assertRaisesRegex(
                    bridge.ManifestRefusal,
                    "A24_TARGET_L12_HISTORY.*(binding mismatch|wrong SHA-256)",
                ):
                    self.build_manifest(sources)

    def test_arbitrary_nonhistory_a26_authority_substitution_is_refused(self) -> None:
        sources = self.write_sources()
        audit_path = self.directory / sources[12]["audit_path"]
        audit = json.loads(audit_path.read_text())
        binding = next(
            row for row in audit["authority_bindings"]
            if row["artifact_id"] == "A20_SHARED_SCHEDULE_GATE"
        )
        binding["artifact_id"] = "FIXTURE_AUTHORITY_SUBSTITUTION"
        self.rewrite_audit(sources, 12, audit)
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "authority identity census mismatch",
        ):
            self.build_manifest(sources)

    def test_arbitrary_a17_physical_source_substitution_is_refused(self) -> None:
        sources = self.write_sources()
        audit_path = self.directory / sources[12]["audit_path"]
        audit = json.loads(audit_path.read_text())
        a17 = next(
            row for row in audit["authority_bindings"]
            if row["artifact_id"] == "A17_HOSTILE_L12_ELIGIBILITY"
        )
        a17["sources"][0]["label"] = "unregistered_method"
        self.rewrite_audit(sources, 12, audit)
        with self.assertRaisesRegex(bridge.ManifestRefusal, "A17 method binding"):
            self.build_manifest(sources)

    def test_stage2_a18_history_substitution_is_refused(self) -> None:
        sources = self.write_sources()
        binding = self.lineage_sources["a18_cross_gate"]
        path = self.directory / binding["path"]
        record = json.loads(path.read_text())
        record["target"]["history_sha256"] = "f" * 64
        path.write_text(json.dumps(record, sort_keys=True))
        binding["sha256"] = bridge.sha256_file(path)
        with self.assertRaisesRegex(
            bridge.ManifestRefusal,
            "A18_L10_CROSS_GATE.*wrong SHA-256|A18 benchmark lineage",
        ):
            self.build_manifest(sources)

    def test_owner_once_publication_refuses_second_writer(self) -> None:
        manifest = self.build_manifest(self.write_sources())
        output = self.directory / "owner_once.json"
        digest = bridge.publish_once(output, manifest)
        original = output.read_bytes()
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "already exists",
        ):
            bridge.publish_once(output, manifest)
        self.assertEqual(original, output.read_bytes())
        self.assertEqual(digest, bridge.sha256_file(output))
        self.assertEqual(output.stat().st_mode & 0o222, 0)

    def test_owner_once_publication_refuses_broken_symlink_destination(self) -> None:
        manifest = self.build_manifest(self.write_sources())
        output = self.directory / "aliased.json"
        target_path = self.directory / "not_created.json"
        output.symlink_to(target_path)
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "already exists",
        ):
            bridge.publish_once(output, manifest)
        self.assertTrue(output.is_symlink())
        self.assertFalse(target_path.exists())

    def test_adverse_target_blind_observable_drift_is_refused(self) -> None:
        sources = self.write_sources()
        blind_path = self.directory / sources[6]["blind_path"]
        record = json.loads(blind_path.read_text())
        record["rows"][2]["W_n"] += 2.0e-8
        blind_path.write_text(json.dumps(record, sort_keys=True))
        sources[6]["blind_sha256"] = bridge.sha256_file(blind_path)
        audit_path = self.directory / sources[6]["audit_path"]
        audit = json.loads(audit_path.read_text())
        audit["blind_hashes"]["6"] = sources[6]["blind_sha256"]
        self.rewrite_audit(sources, 6, audit)
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "target/blind tolerance exceeded",
        ):
            self.build_manifest(sources)

    def test_actual_shape_zero_tail_projects_to_authenticated_q_range(self) -> None:
        manifest = self.build_manifest(self.write_sources())
        for length in (4, 6, 8):
            with self.subTest(length=length):
                pbar = manifest["histories"][str(length)]["pbar_q"]
                self.assertEqual(len(pbar), length + 1)
                self.assertEqual(pbar[length // 2], 1.0)

    def test_nonzero_expanded_tail_is_refused(self) -> None:
        sources = self.write_sources()
        target_path = self.directory / sources[4]["target_path"]
        record = json.loads(target_path.read_text())
        record["rows"][0]["sector_weights"][5] = 1.0e-30
        target_path.write_text(json.dumps(record, sort_keys=True))
        sources[4]["target_sha256"] = bridge.sha256_file(target_path)
        audit_path = self.directory / sources[4]["audit_path"]
        audit = json.loads(audit_path.read_text())
        audit["target_hashes"]["4"] = sources[4]["target_sha256"]
        self.rewrite_audit(sources, 4, audit)
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "nonzero or invalid q>L sector-weight tail",
        ):
            self.build_manifest(sources)

    def test_underflowing_nonzero_expanded_tail_is_refused(self) -> None:
        sources = self.write_sources()
        target_path = self.directory / sources[4]["target_path"]
        raw = target_path.read_text()
        raw = raw.replace(
            '"sector_weights": [0.0, 0.0, 1.0, 0.0, 0.0, 0.0,',
            '"sector_weights": [0.0, 0.0, 1.0, 0.0, 0.0, 1e-400,',
            1,
        )
        self.assertIn("1e-400", raw)
        target_path.write_text(raw)
        sources[4]["target_sha256"] = bridge.sha256_file(target_path)
        audit_path = self.directory / sources[4]["audit_path"]
        audit = json.loads(audit_path.read_text())
        audit["target_hashes"]["4"] = sources[4]["target_sha256"]
        self.rewrite_audit(sources, 4, audit)
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "nonzero or invalid q>L sector-weight tail",
        ):
            self.build_manifest(sources)

    def test_wrong_sector_weight_length_is_refused(self) -> None:
        sources = self.write_sources()
        target_path = self.directory / sources[4]["target_path"]
        record = json.loads(target_path.read_text())
        record["rows"][0]["sector_weights"] = [0.0] * 8
        target_path.write_text(json.dumps(record, sort_keys=True))
        sources[4]["target_sha256"] = bridge.sha256_file(target_path)
        audit_path = self.directory / sources[4]["audit_path"]
        audit = json.loads(audit_path.read_text())
        audit["target_hashes"]["4"] = sources[4]["target_sha256"]
        self.rewrite_audit(sources, 4, audit)
        with self.assertRaisesRegex(
            bridge.ManifestRefusal, "invalid sector-weight vector length",
        ):
            self.build_manifest(sources)

    def test_generator_does_not_import_or_launch_physics_engines(self) -> None:
        source = Path(bridge.__file__).read_text()
        self.assertNotIn("import subprocess", source)
        self.assertNotIn("compute_streamed_history", source)
        self.assertNotIn("compute_phase_screen", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
