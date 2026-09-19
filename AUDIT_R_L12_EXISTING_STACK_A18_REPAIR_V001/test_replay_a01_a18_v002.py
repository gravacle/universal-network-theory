#!/usr/bin/env python3
"""Hostile tests for the bounded V002 A27 ordering repair and restart."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import os
import stat
import sys
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "replay_a01_a18_v002.py"
SPEC = importlib.util.spec_from_file_location("replay_a01_a18_v002_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


class A27OrderingRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.review = replay.ExactLiveReview(replay.v001.ROOT)
        cls.a02, cls.a02_sha, _ = replay.v001._stable_owner_once_json(
            replay.v001.ROOT
            / replay.v001.PUBLISHED_PATH_BY_INSTANCE[
                ("A02_NONPHYSICAL_PREFLIGHT", 1)
            ],
            "preserved canonical A02",
        )
        cls.a27, cls.a27_sha, _ = replay.v001._stable_owner_once_json(
            replay.v001.ROOT / replay.v001.MUTATION_LEDGER_PATH,
            "preserved canonical A27",
        )

    def test_frozen_v001_custody_and_exact_repair_derivation(self) -> None:
        metadata = os.stat(replay.V001_PATH, follow_symlinks=False)
        self.assertTrue(stat.S_ISREG(metadata.st_mode))
        self.assertEqual(metadata.st_nlink, 1)
        self.assertFalse(metadata.st_mode & 0o222)
        self.assertEqual(
            hashlib.sha256(replay._read_frozen_v001()).hexdigest(),
            replay.V001_SHA256,
        )
        original = replay.v001._read_pinned_source_bytes(
            replay.INDEPENDENT_SOURCE_PATH, replay.INDEPENDENT_SOURCE_SHA256,
            "independent auditor test source", require_immutable=True,
        )
        repaired = replay.derive_repaired_independent_source()
        self.assertEqual(original.count(replay.INDEPENDENT_M25_ANCHOR), 1)
        self.assertEqual(original.count(replay.INDEPENDENT_M25_REPLACEMENT), 0)
        self.assertEqual(
            repaired,
            original.replace(
                replay.INDEPENDENT_M25_ANCHOR,
                replay.INDEPENDENT_M25_REPLACEMENT, 1,
            ),
        )
        self.assertEqual(
            hashlib.sha256(repaired).hexdigest(),
            replay.REPAIRED_INDEPENDENT_SHA256,
        )
        self.assertEqual(
            replay._import_fingerprint(original),
            replay._import_fingerprint(repaired),
        )

    def test_authenticated_matrix_derives_exact_eight_m25_rows(self) -> None:
        independent = replay.load_repaired_independent()
        assignments = independent._matrix_assignments()
        self.assertEqual(len(assignments), 477)
        self.assertEqual(
            replay.derive_m25_rows(independent), replay.EXPECTED_M25_ROWS,
        )
        for index, artifact_id, fixture_id in replay.EXPECTED_M25_ROWS:
            assignment = assignments[index - 1]
            self.assertEqual(
                assignment,
                (artifact_id, fixture_id, "M25_IMPORT_TARGET_VALIDATOR"),
            )
            self.assertEqual(
                independent._ledger_expected_hook(*assignment),
                replay.CORRECT_M25_HOOK,
            )
            self.assertEqual(
                independent._ledger_expected_validator(*assignment),
                replay.CORRECT_M25_HOOK,
            )

    def test_matrix_missing_extra_or_wrong_m25_row_refuses(self) -> None:
        assignments = list(
            replay.load_repaired_independent()._matrix_assignments()
        )

        class Fake:
            def __init__(self, rows: list[tuple[str, str, str]]):
                self.rows = tuple(rows)

            def _matrix_assignments(self):
                return self.rows

        variants = {
            "missing": assignments[:25] + assignments[26:],
            "extra": assignments[:26] + [assignments[25]] + assignments[26:],
            "wrong": [
                *assignments[:25],
                (assignments[25][0], "PF_WRONG", assignments[25][2]),
                *assignments[26:],
            ],
        }
        for label, rows in variants.items():
            with self.subTest(label=label):
                with self.assertRaisesRegex(replay.Refusal, "row census"):
                    replay.derive_m25_rows(Fake(rows))

    def test_any_other_independent_source_difference_refuses(self) -> None:
        original = replay.v001._read_pinned_source_bytes(
            replay.INDEPENDENT_SOURCE_PATH, replay.INDEPENDENT_SOURCE_SHA256,
            "independent auditor test source", require_immutable=True,
        )
        for label, attacked in (
            ("other-byte", original + b"\n"),
            ("extra-anchor", original + replay.INDEPENDENT_M25_ANCHOR),
        ):
            with self.subTest(label=label), mock.patch.object(
                replay.v001, "_read_pinned_source_bytes", return_value=attacked,
            ):
                with self.assertRaises(replay.Refusal):
                    replay.derive_repaired_independent_source()

    def test_original_a27_passes_both_direct_sinks_all_477_rows(self) -> None:
        before = replay.v001.retirement.canonical_json_bytes(self.a27)
        self.review.production_sink("A27_MUTATION_LEDGER", self.a27)
        self.review.independent_sink("A27_MUTATION_LEDGER", self.a27)
        self.assertEqual(
            replay.v001.retirement.canonical_json_bytes(self.a27), before,
        )
        self.assertEqual(len(self.a27["cases"]), 477)
        for index, artifact_id, fixture_id in replay.EXPECTED_M25_ROWS:
            row = self.a27["cases"][index - 1]
            self.assertEqual(
                (row["artifact_id"], row["fixture_id"], row["mutation_class"]),
                (artifact_id, fixture_id, "M25_IMPORT_TARGET_VALIDATOR"),
            )
            self.assertEqual(row["production_hook"], replay.CORRECT_M25_HOOK)
            self.assertEqual(row["validator_function"], replay.CORRECT_M25_HOOK)

    def test_both_sinks_receive_identical_original_canonical_bytes(self) -> None:
        observed: list[bytes] = []
        target = self.review.preflight.validate_mutation_ledger
        independent = self.review.repaired_independent.validate_mutation_ledger

        def target_capture(record, *args, **kwargs):
            observed.append(replay.v001.retirement.canonical_json_bytes(record))
            return target(record, *args, **kwargs)

        def independent_capture(record, *args, **kwargs):
            observed.append(replay.v001.retirement.canonical_json_bytes(record))
            return independent(record, *args, **kwargs)

        with mock.patch.object(
            self.review.preflight, "validate_mutation_ledger",
            side_effect=target_capture,
        ), mock.patch.object(
            self.review.repaired_independent, "validate_mutation_ledger",
            side_effect=independent_capture,
        ):
            self.review.production_sink("A27_MUTATION_LEDGER", self.a27)
            self.review.independent_sink("A27_MUTATION_LEDGER", self.a27)
        expected = replay.v001.retirement.canonical_json_bytes(self.a27)
        self.assertEqual(observed, [expected, expected])

    def test_missing_extra_wrong_m25_and_non_m25_record_refuse(self) -> None:
        variants = {}
        missing = copy.deepcopy(self.a27)
        missing["cases"].pop()
        variants["missing-row"] = missing
        extra = copy.deepcopy(self.a27)
        extra["cases"].append(copy.deepcopy(extra["cases"][-1]))
        variants["extra-row"] = extra
        wrong_m25 = copy.deepcopy(self.a27)
        wrong_m25["cases"][25]["production_hook"] = "wrong.hook"
        variants["wrong-m25-row"] = wrong_m25
        wrong_non_m25 = copy.deepcopy(self.a27)
        wrong_non_m25["cases"][0]["production_hook"] = "wrong.hook"
        variants["wrong-non-m25-row"] = wrong_non_m25
        refusal_types = (
            replay.Refusal,
            self.review.preflight.Failure,
            self.review.repaired_independent.Refusal,
        )
        for label, record in variants.items():
            with self.subTest(label=label):
                with self.assertRaises(refusal_types):
                    self.review.production_sink("A27_MUTATION_LEDGER", record)
                with self.assertRaises(refusal_types):
                    self.review.independent_sink("A27_MUTATION_LEDGER", record)

    def test_mutating_target_or_independent_sink_refuses(self) -> None:
        def mutate(record, *_args, **_kwargs):
            record["cases"][0]["passed"] = False

        for label, owner in (
            ("target", self.review.preflight),
            ("independent", self.review.repaired_independent),
        ):
            record = copy.deepcopy(self.a27)
            with self.subTest(label=label), mock.patch.object(
                owner, "validate_mutation_ledger", side_effect=mutate,
            ):
                sink = (
                    self.review.production_sink
                    if label == "target" else self.review.independent_sink
                )
                with self.assertRaisesRegex(replay.Refusal, "mutated original"):
                    sink("A27_MUTATION_LEDGER", record)

    def test_live_a02_a27_restart_reconciles_without_publisher(self) -> None:
        action = replay.v001.existing_publisher_actions()[0]
        a02_path = replay.v001.ROOT / replay.v001.PUBLISHED_PATH_BY_INSTANCE[
            ("A02_NONPHYSICAL_PREFLIGHT", 1)
        ]
        a27_path = replay.v001.ROOT / replay.v001.MUTATION_LEDGER_PATH
        before = {
            path: (os.stat(path, follow_symlinks=False).st_ino,
                   hashlib.sha256(path.read_bytes()).hexdigest())
            for path in (a02_path, a27_path)
        }
        invoked = False

        def forbidden(_command: object) -> int:
            nonlocal invoked
            invoked = True
            raise AssertionError("completed A02/A27 must not rerun publisher")

        result = replay.v001._reconcile_or_run_existing_publisher(
            replay.v001.ROOT, self.review, action, forbidden,
        )
        self.assertTrue(result[2])
        self.assertEqual(result[:2], (self.a02_sha, self.a27_sha))
        self.assertFalse(invoked)
        after = {
            path: (os.stat(path, follow_symlinks=False).st_ino,
                   hashlib.sha256(path.read_bytes()).hexdigest())
            for path in (a02_path, a27_path)
        }
        self.assertEqual(after, before)

    def test_live_entry_still_has_one_hash_only_and_no_projection(self) -> None:
        self.assertEqual(
            list(inspect.signature(
                replay.coordinate_canonical_a01_a18_replay
            ).parameters),
            ["expected_retirement_receipt_sha256"],
        )
        source = SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("project_a27", source)
        self.assertNotIn("copy.deepcopy", source)


if __name__ == "__main__":
    unittest.main()
