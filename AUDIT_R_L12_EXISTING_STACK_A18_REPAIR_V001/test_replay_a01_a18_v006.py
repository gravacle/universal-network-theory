#!/usr/bin/env python3
"""Hostile tests for V006 monotone canonical-prefix custody."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "replay_a01_a18_v006.py"
SPEC = importlib.util.spec_from_file_location("replay_a01_a18_v006_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


def canonical_path(artifact_id: str) -> Path:
    relative = replay.v001.TEMPLATE_PATH_BY_ARTIFACT[artifact_id]
    return replay.ROOT.joinpath(*PurePosixPath(relative).parts)


def current_control_candidates():
    v001 = replay.v001
    produced: dict[tuple[str, int], str] = {}
    existing = [
        ("A01_FREEZE_AND_SOURCE_PACKET", 1),
        ("A02_NONPHYSICAL_PREFLIGHT", 1),
        ("A03_PREPAYLOAD_AUDIT", 1),
        ("A04_UNIVERSAL_CUSTODY_GATE", 1),
        *(("A05_FIVE_CACHE_SET", instance) for instance in range(1, 6)),
        ("A06_POSTBUILD_AUDIT", 1),
        ("A07_BASE_PHYSICAL_GATE", 1),
        ("A08_PHYSICAL_GATE_AUDIT", 1),
        ("A09_CONTROL_AUTHORIZATION", 1),
        *(("A10_CONTROL_HISTORIES", instance) for instance in range(1, 4)),
    ]
    for key in existing:
        path = replay.ROOT.joinpath(
            *PurePosixPath(v001.PUBLISHED_PATH_BY_INSTANCE[key]).parts
        )
        produced[key] = v001._stable_owner_once_sha256(
            path, f"V006 test current {key[0]}/{key[1]}",
        )
    ledger = replay.ROOT.joinpath(*PurePosixPath(v001.MUTATION_LEDGER_PATH).parts)
    produced[("A27_MUTATION_LEDGER", 1)] = v001._stable_owner_once_sha256(
        ledger, "V006 test current A27",
    )
    census = replay.retirement.load_census()

    def candidate(artifact_id: str):
        template = v001.load_retired_template(replay.ROOT, census, artifact_id)
        updates = v001.measured_template_updates(
            replay.ROOT, artifact_id, produced,
        )
        return v001.update_authenticated_template(artifact_id, template, updates)

    a11 = candidate("A11_CONTROL_STAGE_GATE")
    produced[("A11_CONTROL_STAGE_GATE", 1)] = v001._predicted_publication_sha(a11)
    a12 = candidate("A12_CONTROL_STAGE_AUDIT")
    produced[("A12_CONTROL_STAGE_AUDIT", 1)] = v001._predicted_publication_sha(a12)
    a13 = candidate("A13_L10_AUTHORIZATION")
    cache_hashes = {
        str(length): produced[("A05_FIVE_CACHE_SET", instance)]
        for instance, length in enumerate((4, 6, 8, 10, 12), start=1)
    }
    return a11, a12, a13, cache_hashes, produced


class V006MonotonePrefixTests(unittest.TestCase):
    def setUp(self) -> None:
        for artifact_id in replay.v005.CANONICAL_ORDER:
            self.assertFalse(
                replay.retirement.path_exists(canonical_path(artifact_id)),
                f"test requires preserved pre-A11 checkpoint: {artifact_id}",
            )

    def test_frozen_v005_packet_hashes_and_custody(self) -> None:
        for name, expected in replay.PINNED_V005_PACKET.items():
            path = HERE / name
            metadata = os.stat(path, follow_symlinks=False)
            self.assertTrue(stat.S_ISREG(metadata.st_mode))
            self.assertEqual(metadata.st_nlink, 1)
            self.assertFalse(metadata.st_mode & 0o222)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
            self.assertEqual(
                hashlib.sha256(replay._read_frozen_packet_file(name)).hexdigest(),
                expected,
            )

    def _fake_prefix_fixture(self):
        a11, a12, a13, _cache, _produced = current_control_candidates()
        records = {
            "A11_CONTROL_STAGE_GATE": a11,
            "A12_CONTROL_STAGE_AUDIT": a12,
            "A13_L10_AUTHORIZATION": a13,
            "A15_L10_STAGE_GATE": {"synthetic": "A15 monotonicity only"},
            "A16_L10_STAGE_AUDIT": {"synthetic": "A16 monotonicity only"},
        }
        temporary = tempfile.TemporaryDirectory(prefix="v006-prefix-")
        fake_root = Path(temporary.name)
        paths = {
            artifact_id: fake_root / f"{index:02d}-{artifact_id}.json"
            for index, artifact_id in enumerate(replay.v005.CANONICAL_ORDER)
        }
        review = replay.MonotoneStagedPathReview(replay.ROOT)
        review._canonical_path = lambda artifact_id: paths[artifact_id]
        review._control_batch_closed = True
        review._l10_batch_closed = True
        for artifact_id, record in records.items():
            review._remember_candidate(artifact_id, record)
        return review, temporary, paths, records

    def test_disappearance_refuses_at_every_control_and_l10_prefix(self) -> None:
        for prefix_length in range(1, 6):
            with self.subTest(prefix_length=prefix_length):
                review, temporary, paths, records = self._fake_prefix_fixture()
                try:
                    for artifact_id in replay.v005.CANONICAL_ORDER[:prefix_length]:
                        replay.retirement.publish_once(
                            paths[artifact_id], records[artifact_id],
                        )
                    review._assert_canonical_state()
                    self.assertEqual(review._canonical_high_water, prefix_length)
                    removed = replay.v005.CANONICAL_ORDER[prefix_length - 1]
                    paths[removed].unlink()
                    with self.assertRaisesRegex(
                        replay.Refusal, "authenticated canonical prefix disappeared",
                    ):
                        review._assert_canonical_state()
                    self.assertEqual(review._canonical_high_water, prefix_length)
                    for artifact_id in replay.v005.CANONICAL_ORDER[:prefix_length - 1]:
                        self.assertTrue(paths[artifact_id].is_file())
                finally:
                    review.close()
                    temporary.cleanup()

    def test_high_water_advances_only_after_each_exact_prefix_passes(self) -> None:
        review, temporary, paths, records = self._fake_prefix_fixture()
        try:
            self.assertEqual(review._canonical_high_water, 0)
            for prefix_length, artifact_id in enumerate(
                replay.v005.CANONICAL_ORDER, start=1,
            ):
                replay.retirement.publish_once(paths[artifact_id], records[artifact_id])
                review._assert_canonical_state()
                self.assertEqual(review._canonical_high_water, prefix_length)
        finally:
            review.close()
            temporary.cleanup()

    def test_identical_byte_new_inode_reappearance_refuses_at_every_prefix(self) -> None:
        for prefix_length in range(1, 6):
            with self.subTest(prefix_length=prefix_length):
                review, temporary, paths, records = self._fake_prefix_fixture()
                try:
                    for artifact_id in replay.v005.CANONICAL_ORDER[:prefix_length]:
                        replay.retirement.publish_once(
                            paths[artifact_id], records[artifact_id],
                        )
                    review._assert_canonical_state()
                    self.assertEqual(review._canonical_high_water, prefix_length)
                    replaced = replay.v005.CANONICAL_ORDER[prefix_length - 1]
                    prior_inode = os.stat(
                        paths[replaced], follow_symlinks=False,
                    ).st_ino
                    paths[replaced].unlink()
                    replay.retirement.publish_once(
                        paths[replaced], records[replaced],
                    )
                    self.assertNotEqual(
                        os.stat(paths[replaced], follow_symlinks=False).st_ino,
                        prior_inode,
                    )
                    with self.assertRaisesRegex(
                        replay.Refusal, "canonical predecessor inode changed",
                    ):
                        review._assert_canonical_state()
                    self.assertEqual(review._canonical_high_water, prefix_length)
                    self.assertEqual(
                        paths[replaced].read_bytes(),
                        review._candidate_bytes[replaced],
                    )
                finally:
                    review.close()
                    temporary.cleanup()

    def test_failed_new_prefix_authentication_does_not_advance_high_water(self) -> None:
        review, temporary, paths, records = self._fake_prefix_fixture()
        try:
            replay.retirement.publish_once(
                paths["A11_CONTROL_STAGE_GATE"],
                records["A11_CONTROL_STAGE_GATE"],
            )
            review._assert_canonical_state()
            self.assertEqual(review._canonical_high_water, 1)
            replay.retirement.publish_once(
                paths["A12_CONTROL_STAGE_AUDIT"], {"hostile": "wrong bytes"},
            )
            with self.assertRaisesRegex(replay.Refusal, "differs from candidate"):
                review._assert_canonical_state()
            self.assertEqual(review._canonical_high_water, 1)
        finally:
            review.close()
            temporary.cleanup()

    def test_current_exact_a11_a13_chain_still_passes_without_publication(self) -> None:
        a11, a12, a13, cache_hashes, produced = current_control_candidates()
        review = replay.MonotoneStagedPathReview(replay.ROOT)
        try:
            for artifact_id, record in (
                ("A11_CONTROL_STAGE_GATE", a11),
                ("A12_CONTROL_STAGE_AUDIT", a12),
                ("A13_L10_AUTHORIZATION", a13),
            ):
                review.production_sink(artifact_id, record)
                review.independent_sink(artifact_id, record)
            review.validate_stage_chain(
                a11, a12, a13, cache_hashes,
                produced[("A07_BASE_PHYSICAL_GATE", 1)],
            )
            self.assertEqual(review._canonical_high_water, 0)
            self.assertTrue(review._control_batch_closed)
            self.assertTrue(all(
                not replay.retirement.path_exists(canonical_path(artifact_id))
                for artifact_id in replay.v005.CANONICAL_ORDER
            ))
        finally:
            review.close()

    def test_coordinate_substitution_cleanup_on_refusal(self) -> None:
        captured: list[object] = []

        def fake_coordinate(_old, _cache):
            instance = replay.v002.ExactLiveReview(replay.ROOT)
            captured.append(instance)
            raise RuntimeError("forced V004 refusal")

        original = replay.v002.ExactLiveReview
        with mock.patch.object(
            replay.v004, "coordinate_canonical_a01_a18_replay",
            side_effect=fake_coordinate,
        ):
            with self.assertRaisesRegex(RuntimeError, "forced V004"):
                replay.coordinate_canonical_a01_a18_replay("a" * 64, "b" * 64)
        self.assertIs(replay.v002.ExactLiveReview, original)
        self.assertFalse(replay._CAPTURE_COORDINATE_REVIEW)
        self.assertIsNone(replay._ACTIVE_COORDINATE_REVIEW)
        self.assertEqual(len(captured), 1)
        self.assertTrue(captured[0]._closed)

    def test_plan_is_bounded_and_nonexecuted(self) -> None:
        plan = replay.replay_plan()
        self.assertEqual(
            plan["classification"],
            "BOUNDED_NONEXECUTED_V006_MONOTONE_PREFIX_PLAN",
        )
        self.assertTrue(plan["high_water_initialized_from_entry_prefix"])
        self.assertTrue(plan["high_water_advances_after_exact_v005_authentication_only"])
        self.assertFalse(plan["authenticated_prefix_deletion_accepted"])
        self.assertFalse(plan["other_v005_behavior_changed"])
        self.assertFalse(plan["canonical_action_executed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
