#!/usr/bin/env python3
"""Fixed-scope tests for the existing-stack A18 role-contract repair."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
sys.path.insert(0, str(TARGET))

import build_target_cache as builder  # noqa: E402
import production_obligation_validators as validator  # noqa: E402


ARTIFACT = "A18_L10_CROSS_GATE"
OBSTRUCTION = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "A18_DUAL_SINK_ROLE_CONTRACT_OBSTRUCTION_V001.json"
)
TARGET_KEYS = {
    "branch", "cached_L10_gate_sha256", "cached_L10_gate_audit_sha256",
    "history_sha256",
}
HOSTILE_KEYS = {
    "branch", "cached_L10_gate_sha256",
    "l10_execution_authorization_gate_sha256",
    "independent_prepayload_audit_sha256", "history_sha256",
}
BRANCH_KEYS = {
    "role", "method", "builder", "consumer", "preflight", "freeze",
    "preflight_result", "independent_audit", "cached_L10_gate",
    "L12_cache_manifest",
}
FILESYSTEM_HOOK_CLASSES = {
    "M12_SYMLINK_OR_WRITABLE", "M13_DESCRIPTOR_TOCTOU",
    "M25_IMPORT_TARGET_VALIDATOR", "M28_PREMATURE_ARTIFACT",
}


def exact_candidate() -> dict[str, object]:
    value = json.loads(OBSTRUCTION.read_bytes())
    return value["candidate_a18_record"]


class A18ExistingStackRepairTests(unittest.TestCase):
    def test_positive_fixture_is_exact_consumer_shape(self) -> None:
        record = validator.positive_fixture(ARTIFACT)
        self.assertEqual(set(record["target"]), TARGET_KEYS)
        self.assertEqual(set(record["hostile"]), HOSTILE_KEYS)
        self.assertEqual(set(record["target"]["branch"]), BRANCH_KEYS)
        self.assertEqual(set(record["hostile"]["branch"]), BRANCH_KEYS)
        for branch in (
            record["target"]["branch"], record["hostile"]["branch"],
        ):
            for name in ("method", "builder", "consumer", "preflight"):
                self.assertEqual(set(branch[name]), {"path", "sha256"})
            for name in (
                "freeze", "preflight_result", "independent_audit",
                "cached_L10_gate", "L12_cache_manifest",
            ):
                self.assertEqual(
                    set(branch[name]),
                    {"path", "sha256", "schema", "identity_field", "identity_value"},
                )
        self.assertNotIn("role", record["target"])
        self.assertNotIn("role", record["hostile"])
        self.assertEqual(record["target"]["branch"]["role"], "target_v012")
        self.assertEqual(
            record["hostile"]["branch"]["role"], "hostile_v004r4",
        )
        validator.validate_record(
            ARTIFACT, record, mutation_class="POSITIVE_CONTROL",
            fixture_mode=True,
        )

    def test_frozen_independent_candidate_passes_live_shape(self) -> None:
        record = exact_candidate()
        accepted = validator.validate_record(
            ARTIFACT, record, mutation_class="EXACT_FROZEN_A18_CANDIDATE",
            fixture_mode=False,
        )
        self.assertEqual(accepted, record)

    def test_wrong_target_nested_role_refuses(self) -> None:
        record = exact_candidate()
        record["target"]["branch"]["role"] = "target"
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="WRONG_TARGET_BRANCH_ROLE",
            )

    def test_wrong_hostile_nested_role_refuses(self) -> None:
        record = exact_candidate()
        record["hostile"]["branch"]["role"] = "hostile"
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="WRONG_HOSTILE_BRANCH_ROLE",
            )

    def test_projection_top_level_role_is_forbidden(self) -> None:
        for projection in ("target", "hostile"):
            with self.subTest(projection=projection):
                record = exact_candidate()
                record[projection]["role"] = projection
                with self.assertRaisesRegex(
                    validator.Refusal, "cross-role alias mismatch",
                ):
                    validator.validate_record(
                        ARTIFACT, record,
                        mutation_class="FORBIDDEN_PROJECTION_ROLE",
                    )

    def test_equal_history_hashes_refuse(self) -> None:
        record = exact_candidate()
        record["hostile"]["history_sha256"] = record["target"]["history_sha256"]
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_HISTORIES",
            )

    def test_cross_branch_source_digest_alias_refuses(self) -> None:
        record = exact_candidate()
        record["hostile"]["branch"]["method"]["sha256"] = (
            record["target"]["branch"]["method"]["sha256"]
        )
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_BRANCH_SOURCE_DIGEST",
            )

    def test_cross_branch_source_path_alias_refuses(self) -> None:
        record = exact_candidate()
        record["hostile"]["branch"]["method"]["path"] = (
            record["target"]["branch"]["method"]["path"]
        )
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_BRANCH_SOURCE_PATH",
            )

    def test_equal_cached_l10_gate_hashes_refuse(self) -> None:
        record = exact_candidate()
        record["hostile"]["cached_L10_gate_sha256"] = (
            record["target"]["cached_L10_gate_sha256"]
        )
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_CACHED_L10_GATE",
            )

    def test_target_branch_source_digest_alias_refuses(self) -> None:
        record = exact_candidate()
        record["target"]["branch"]["method"]["sha256"] = (
            record["target"]["branch"]["builder"]["sha256"]
        )
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_TARGET_SOURCE_DIGEST",
            )

    def test_target_branch_source_path_alias_refuses(self) -> None:
        record = exact_candidate()
        record["target"]["branch"]["method"]["path"] = (
            record["target"]["branch"]["builder"]["path"]
        )
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_TARGET_SOURCE_PATH",
            )

    def test_hostile_branch_source_digest_alias_refuses(self) -> None:
        record = exact_candidate()
        record["hostile"]["branch"]["method"]["sha256"] = (
            record["hostile"]["branch"]["builder"]["sha256"]
        )
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_HOSTILE_SOURCE_DIGEST",
            )

    def test_hostile_branch_source_path_alias_refuses(self) -> None:
        record = exact_candidate()
        record["hostile"]["branch"]["method"]["path"] = (
            record["hostile"]["branch"]["builder"]["path"]
        )
        with self.assertRaisesRegex(validator.Refusal, "cross-role alias mismatch"):
            validator.validate_record(
                ARTIFACT, record, mutation_class="ALIASED_HOSTILE_SOURCE_PATH",
            )

    def test_all_a18_record_mutation_assignments_refuse(self) -> None:
        matrix = json.loads(
            (
                ROOT / "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012"
                / "AUDIT_OBLIGATIONS_V001.json"
            ).read_bytes()
        )
        row = next(item for item in matrix["artifacts"] if item["id"] == ARTIFACT)
        executed = 0
        for mutation_class in row["mutation_classes"]:
            if mutation_class in FILESYSTEM_HOOK_CLASSES:
                continue
            with self.subTest(mutation_class=mutation_class):
                mutated, expected, _description = validator.mutated_fixture(
                    ARTIFACT, mutation_class,
                )
                raw = (
                    mutated if type(mutated) is bytes
                    else validator.canonical_json_bytes(mutated)
                )
                with self.assertRaises(builder.Refusal) as captured:
                    builder.validate_audit_obligation_fixture(
                        ARTIFACT, raw, mutation_class=mutation_class,
                    )
                self.assertTrue(
                    builder.exact_refusal_match(str(captured.exception), expected),
                    str(captured.exception),
                )
                executed += 1
        self.assertEqual(executed, 18)

    def test_fixture_copy_does_not_alias_nested_branches(self) -> None:
        record = validator.positive_fixture(ARTIFACT)
        copied = copy.deepcopy(record)
        copied["target"]["branch"]["role"] = "changed"
        self.assertEqual(record["target"]["branch"]["role"], "target_v012")


if __name__ == "__main__":
    unittest.main(verbosity=2)
