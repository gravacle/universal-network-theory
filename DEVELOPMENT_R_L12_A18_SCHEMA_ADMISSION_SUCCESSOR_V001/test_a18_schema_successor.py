#!/usr/bin/env python3
"""Focused fail-closed tests for the A18 schema-admission successor."""

from __future__ import annotations

import copy
import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import a18_schema_successor as successor


class A18SchemaSuccessorTests(unittest.TestCase):
    def test_exact_candidate_passes_and_binds_wire_hash(self) -> None:
        with successor.PredecessorCustody() as custody:
            record = successor.construct_a18_candidate(custody)
            self.assertEqual(
                hashlib.sha256(successor.publication_json_bytes(record)).hexdigest(),
                successor.A18_CANDIDATE_WIRE_SHA256,
            )
            self.assertNotIn("role", record)
            self.assertEqual(record["target"]["branch"]["role"], "target_v012")
            self.assertEqual(
                record["hostile"]["branch"]["role"], "hostile_v004r4",
            )

    def test_wrong_target_nested_role_refuses(self) -> None:
        with successor.PredecessorCustody() as custody:
            record = copy.deepcopy(custody.candidate)
            record["target"]["branch"]["role"] = "target"
            with self.assertRaises(successor.Refusal):
                successor.validate_a18(record, custody)

    def test_wrong_hostile_nested_role_refuses(self) -> None:
        with successor.PredecessorCustody() as custody:
            record = copy.deepcopy(custody.candidate)
            record["hostile"]["branch"]["role"] = "hostile"
            with self.assertRaises(successor.Refusal):
                successor.validate_a18(record, custody)

    def test_forbidden_top_level_role_refuses(self) -> None:
        with successor.PredecessorCustody() as custody:
            record = copy.deepcopy(custody.candidate)
            record["role"] = "target"
            with self.assertRaises(successor.Refusal):
                successor.validate_a18(record, custody)

    def test_altered_predecessor_hash_refuses_before_admission(self) -> None:
        with mock.patch.object(successor, "A16_SHA256", "0" * 64):
            with self.assertRaises(successor.Refusal):
                successor.PredecessorCustody().open()

    def test_owner_once_publication_is_immutable_and_no_clobber(self) -> None:
        raw = b'{"bounded":"A18-test"}\n'
        with tempfile.TemporaryDirectory(dir=successor.HERE) as directory:
            destination = Path(directory).resolve() / "A18.json"
            digest = successor._atomic_publish_once(
                destination, raw, destination,
            )
            self.assertEqual(digest, hashlib.sha256(raw).hexdigest())
            self.assertEqual(destination.read_bytes(), raw)
            metadata = os.stat(destination, follow_symlinks=False)
            self.assertEqual(metadata.st_mode & 0o222, 0)
            self.assertEqual(metadata.st_nlink, 1)
            with self.assertRaises(successor.Refusal):
                successor._atomic_publish_once(
                    destination, b'{"replacement":true}\n', destination,
                )
            self.assertEqual(destination.read_bytes(), raw)
            self.assertEqual(
                list(destination.parent.glob(f".{destination.name}.staging-*")),
                [],
            )

    def test_frozen_downstream_chain_is_authenticated_but_incomplete(self) -> None:
        report = successor.downstream_executability_report()
        self.assertEqual(
            report["classification"],
            "INCOMPLETE_FAIL_CLOSED_BEFORE_A20_A21_OR_L12",
        )
        self.assertEqual(
            report["frozen_source_sha256"],
            {
                "target_worker": successor.FROZEN_TARGET_WORKER_SHA256,
                "hostile_worker": successor.FROZEN_HOSTILE_WORKER_SHA256,
                "dual_launcher": successor.FROZEN_DUAL_LAUNCHER_SHA256,
            },
        )
        self.assertNotEqual(
            Path(report["successor_a18_path"]),
            successor.ROOT / report["frozen_chain_a18_path"],
        )

    def test_a18_only_successor_never_claims_downstream_execution(self) -> None:
        with self.assertRaisesRegex(
            successor.Refusal, "successor A18 is not downstream executable",
        ):
            successor.require_downstream_executable()


if __name__ == "__main__":
    unittest.main(verbosity=2)
