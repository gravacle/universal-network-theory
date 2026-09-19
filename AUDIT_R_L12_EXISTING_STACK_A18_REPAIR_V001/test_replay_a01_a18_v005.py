#!/usr/bin/env python3
"""Hostile tests for the V005 dependency-closed staged-path adapter."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "replay_a01_a18_v005.py"
SPEC = importlib.util.spec_from_file_location("replay_a01_a18_v005_tested", SOURCE)
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
            path, f"V005 test current {key[0]}/{key[1]}",
        )
    ledger = replay.ROOT.joinpath(*PurePosixPath(v001.MUTATION_LEDGER_PATH).parts)
    produced[("A27_MUTATION_LEDGER", 1)] = v001._stable_owner_once_sha256(
        ledger, "V005 test current A27",
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


class V005StagedPathTests(unittest.TestCase):
    def setUp(self) -> None:
        for artifact_id in replay.CANONICAL_ORDER:
            self.assertFalse(
                replay.retirement.path_exists(canonical_path(artifact_id)),
                f"test requires the preserved pre-A11 checkpoint: {artifact_id}",
            )

    def test_frozen_v004_packet_hashes_and_custody(self) -> None:
        for name, expected in replay.PINNED_V004_PACKET.items():
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

    def test_exact_current_a11_a13_hashes_and_full_live_chain_pass(self) -> None:
        a11, a12, a13, cache_hashes, produced = current_control_candidates()
        observed = {
            artifact_id: replay.retirement.sha256_bytes(
                replay.retirement.publication_json_bytes(record)
            )
            for artifact_id, record in (
                ("A11_CONTROL_STAGE_GATE", a11),
                ("A12_CONTROL_STAGE_AUDIT", a12),
                ("A13_L10_AUTHORIZATION", a13),
            )
        }
        self.assertEqual(observed, replay.EXPECTED_CANDIDATE_SHA256)
        review = replay.StagedPathReview(replay.ROOT)
        originals = dict(review._original_paths)
        try:
            for artifact_id, record in (
                ("A11_CONTROL_STAGE_GATE", a11),
                ("A12_CONTROL_STAGE_AUDIT", a12),
                ("A13_L10_AUTHORIZATION", a13),
            ):
                for sink in review.common_sinks():
                    sink(artifact_id, record)
                self.assertTrue(all(
                    getattr(review.validators, name) is value
                    for name, value in originals.items()
                ))
            for artifact_id in (
                "A11_CONTROL_STAGE_GATE", "A12_CONTROL_STAGE_AUDIT",
            ):
                path = review._require_stage(artifact_id)
                metadata = os.stat(path, follow_symlinks=False)
                self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o444)
                self.assertEqual(metadata.st_nlink, 1)
                self.assertEqual(
                    path.read_bytes(), review._candidate_bytes[artifact_id],
                )
            review.validate_stage_chain(
                a11, a12, a13, cache_hashes,
                produced[("A07_BASE_PHYSICAL_GATE", 1)],
            )
            self.assertTrue(review._control_batch_closed)
            self.assertTrue(all(
                not replay.retirement.path_exists(canonical_path(artifact_id))
                for artifact_id in replay.CANONICAL_ORDER
            ))
        finally:
            stage_root = review._stage_root
            review.close()
        self.assertFalse(stage_root.exists())
        self.assertTrue(all(
            getattr(review.validators, name) is value
            for name, value in originals.items()
        ))

    def test_builder_and_consumer_dispatch_same_authenticated_module(self) -> None:
        review = replay.StagedPathReview(replay.ROOT)
        try:
            review._assert_shared_dispatch_identity()
            observed: list[object] = []

            def marker(artifact_id, record, *, mutation_class, fixture_mode):
                observed.extend((artifact_id, record, mutation_class, fixture_mode))

            with mock.patch.object(review.validators, "validate_record", marker):
                review.builder.validate_production_obligation("V005_PROBE", {"x": 1})
            self.assertEqual(
                observed,
                ["V005_PROBE", {"x": 1}, "PRODUCTION_NATIVE_RECORD", False],
            )
            self.assertIs(
                sys.modules["production_obligation_validators"],
                review.validators,
            )
            self.assertIs(review.consumer.builder, review.builder)
        finally:
            review.close()

    def test_preexisting_validator_path_replacement_refuses_and_restores(self) -> None:
        validators = replay.v001._load_pinned_module(
            replay.ROOT, "production_obligation_validators",
        )
        original = validators.CONTROL_GATE_PATH
        hostile = Path("/private/tmp/not-the-canonical-control-gate.json")
        validators.CONTROL_GATE_PATH = hostile
        try:
            with self.assertRaisesRegex(replay.Refusal, "path value mismatch"):
                replay.StagedPathReview(replay.ROOT)
            self.assertIs(validators.CONTROL_GATE_PATH, hostile)
        finally:
            validators.CONTROL_GATE_PATH = original

    def test_byte_tamper_refuses(self) -> None:
        a11, _a12, _a13, _cache, _produced = current_control_candidates()
        review = replay.StagedPathReview(replay.ROOT)
        try:
            path = review._stage_once("A11_CONTROL_STAGE_GATE", a11)
            path.chmod(0o644)
            path.write_bytes(b"tampered\n")
            path.chmod(0o444)
            with self.assertRaisesRegex(replay.Refusal, "identity|bytes"):
                review._require_stage("A11_CONTROL_STAGE_GATE")
        finally:
            review.close()

    def test_same_byte_inode_swap_refuses(self) -> None:
        a11, _a12, _a13, _cache, _produced = current_control_candidates()
        review = replay.StagedPathReview(replay.ROOT)
        try:
            path = review._stage_once("A11_CONTROL_STAGE_GATE", a11)
            raw = review._candidate_bytes["A11_CONTROL_STAGE_GATE"]
            path.unlink()
            path.write_bytes(raw)
            path.chmod(0o444)
            with self.assertRaisesRegex(replay.Refusal, "identity"):
                review._require_stage("A11_CONTROL_STAGE_GATE")
        finally:
            review.close()

    def test_alias_and_stage_root_identity_swaps_refuse(self) -> None:
        a11, _a12, _a13, _cache, _produced = current_control_candidates()
        review = replay.StagedPathReview(replay.ROOT)
        external = tempfile.TemporaryDirectory(prefix="v005-stage-alias-")
        try:
            path = review._stage_once("A11_CONTROL_STAGE_GATE", a11)
            raw = review._candidate_bytes["A11_CONTROL_STAGE_GATE"]
            other = Path(external.name) / "other"
            other.write_bytes(raw)
            other.chmod(0o444)
            path.unlink()
            path.symlink_to(other)
            with self.assertRaises(replay.Refusal):
                review._require_stage("A11_CONTROL_STAGE_GATE")
        finally:
            review.close()
            external.cleanup()

        review = replay.StagedPathReview(replay.ROOT)
        old_root = review._stage_root
        moved = old_root.with_name(old_root.name + "-moved")
        try:
            old_root.rename(moved)
            old_root.mkdir(mode=0o700)
            with self.assertRaisesRegex(replay.Refusal, "stage-root identity"):
                review._stage_once("A11_CONTROL_STAGE_GATE", a11)
        finally:
            # close removes the replacement root; remove the retained original
            # after restoring its name so TemporaryDirectory can close it.
            if old_root.exists():
                old_root.rmdir()
            moved.rename(old_root)
            review.close()

    def test_each_bound_production_refusal_restores_globals(self) -> None:
        a11, a12, a13, _cache, _produced = current_control_candidates()
        cases = (
            ("A12_CONTROL_STAGE_AUDIT", a12, (("A11_CONTROL_STAGE_GATE", a11),)),
            (
                "A13_L10_AUTHORIZATION", a13,
                (("A11_CONTROL_STAGE_GATE", a11),
                 ("A12_CONTROL_STAGE_AUDIT", a12)),
            ),
            (
                "A16_L10_STAGE_AUDIT", {"synthetic": "A16"},
                (("A15_L10_STAGE_GATE", {"synthetic": "A15"}),),
            ),
        )
        for artifact_id, record, predecessors in cases:
            review = replay.StagedPathReview(replay.ROOT)
            originals = dict(review._original_paths)
            try:
                for predecessor, predecessor_record in predecessors:
                    review._stage_once(predecessor, predecessor_record)
                with mock.patch.object(
                    replay.v002.ExactLiveReview, "production_sink",
                    side_effect=RuntimeError(f"forced {artifact_id} refusal"),
                ):
                    with self.assertRaisesRegex(RuntimeError, "forced"):
                        review.production_sink(artifact_id, record)
                self.assertTrue(all(
                    getattr(review.validators, name) is value
                    for name, value in originals.items()
                ))
                self.assertTrue(all(
                    not replay.retirement.path_exists(canonical_path(name))
                    for name in replay.CANONICAL_ORDER
                ))
            finally:
                review.close()

    def test_stage_chain_consumer_refusal_restores_globals(self) -> None:
        a11, a12, a13, cache_hashes, produced = current_control_candidates()
        review = replay.StagedPathReview(replay.ROOT)
        originals = dict(review._original_paths)
        try:
            review._stage_once("A11_CONTROL_STAGE_GATE", a11)
            review._stage_once("A12_CONTROL_STAGE_AUDIT", a12)
            review._remember_candidate("A13_L10_AUTHORIZATION", a13)
            with mock.patch.object(
                replay.v002.ExactLiveReview, "validate_stage_chain",
                side_effect=RuntimeError("forced consumer refusal"),
            ):
                with self.assertRaisesRegex(RuntimeError, "forced consumer"):
                    review.validate_stage_chain(
                        a11, a12, a13, cache_hashes,
                        produced[("A07_BASE_PHYSICAL_GATE", 1)],
                    )
            self.assertTrue(all(
                getattr(review.validators, name) is value
                for name, value in originals.items()
            ))
            self.assertFalse(review._control_batch_closed)
        finally:
            review.close()

    def test_unexpected_canonical_appearance_refuses_and_is_preserved(self) -> None:
        a11, a12, _a13, _cache, _produced = current_control_candidates()
        review = replay.StagedPathReview(replay.ROOT)
        originals = dict(review._original_paths)
        temporary = tempfile.TemporaryDirectory(prefix="v005-canonical-appearance-")
        fake_root = Path(temporary.name)
        fake_paths = {
            artifact_id: fake_root / f"{index:02d}-{artifact_id}.json"
            for index, artifact_id in enumerate(replay.CANONICAL_ORDER)
        }

        def fake_canonical(artifact_id):
            return fake_paths[artifact_id]

        def hostile_super(_self, _artifact_id, _record):
            # A13 appears without A11/A12 and before the control batch closes.
            replay.retirement.publish_once(
                fake_paths["A13_L10_AUTHORIZATION"], {"hostile": True},
            )

        try:
            review._canonical_path = fake_canonical
            review._stage_once("A11_CONTROL_STAGE_GATE", a11)
            with mock.patch.object(
                replay.v002.ExactLiveReview, "production_sink", hostile_super,
            ):
                with self.assertRaisesRegex(
                    replay.Refusal, "not an exact prefix|outside a closed batch",
                ):
                    review.production_sink("A12_CONTROL_STAGE_AUDIT", a12)
            self.assertTrue(
                fake_paths["A13_L10_AUTHORIZATION"].is_file(),
                "hostile appearance must be preserved, never removed",
            )
            self.assertTrue(all(
                getattr(review.validators, name) is value
                for name, value in originals.items()
            ))
        finally:
            review.close()
            temporary.cleanup()

    def test_current_a01_a10_publishers_reconcile_without_run_or_mutation(self) -> None:
        _a11, _a12, _a13, cache_hashes, _produced = current_control_candidates()
        integer_cache_hashes = {
            int(length): digest for length, digest in cache_hashes.items()
        }
        actions = tuple(
            action for action in replay.v003.absolute_existing_publisher_actions(
                integer_cache_hashes,
            )
            if action.artifact_id in {
                "A02_NONPHYSICAL_PREFLIGHT", "A05_FIVE_CACHE_SET",
                "A06_POSTBUILD_AUDIT", "A10_CONTROL_HISTORIES",
            }
        )
        self.assertEqual(len(actions), 10)
        paths = [
            replay.ROOT.joinpath(*PurePosixPath(
                replay.v001.PUBLISHED_PATH_BY_INSTANCE[
                    (action.artifact_id, action.instance)
                ]
            ).parts)
            for action in actions
        ]
        paths.append(replay.ROOT.joinpath(
            *PurePosixPath(replay.v001.MUTATION_LEDGER_PATH).parts
        ))
        before = {
            path: (
                replay.v001._stable_owner_once_sha256(path, "V005 no-run before"),
                replay._identity(os.stat(path, follow_symlinks=False)),
            )
            for path in paths
        }
        runner_calls: list[object] = []

        def forbidden_runner(command):
            runner_calls.append(command)
            raise AssertionError("completed A01-A10 publisher was rerun")

        review = replay.StagedPathReview(replay.ROOT)
        try:
            for action in actions:
                _digest, _ledger, reconciled = (
                    replay.v001._reconcile_or_run_existing_publisher(
                        replay.ROOT, review, action, forbidden_runner,
                    )
                )
                self.assertTrue(reconciled)
        finally:
            review.close()
        self.assertEqual(runner_calls, [])
        after = {
            path: (
                replay.v001._stable_owner_once_sha256(path, "V005 no-run after"),
                replay._identity(os.stat(path, follow_symlinks=False)),
            )
            for path in paths
        }
        self.assertEqual(after, before)

    def test_latent_a15_a16_binding_and_consumer_use_identical_bytes(self) -> None:
        a15 = {"synthetic": "exact A15 adapter mechanics"}
        a16 = {"synthetic": "exact A16 adapter mechanics"}
        review = replay.StagedPathReview(replay.ROOT)
        originals = dict(review._original_paths)
        seen: list[tuple[str, bytes]] = []

        def production(_self, artifact_id, record):
            if artifact_id == "A16_L10_STAGE_AUDIT":
                self.assertEqual(
                    review.validators.L10_GATE_PATH,
                    review._require_stage("A15_L10_STAGE_GATE"),
                )
            seen.append((artifact_id, review._record_bytes(record)))

        def independent(_self, artifact_id, record):
            seen.append((artifact_id, review._record_bytes(record)))

        def pair(_self, *args):
            self.assertEqual(
                review.validators.L10_GATE_PATH,
                review._require_stage("A15_L10_STAGE_GATE"),
            )

        try:
            with mock.patch.object(
                replay.v002.ExactLiveReview, "production_sink", production,
            ), mock.patch.object(
                replay.v002.ExactLiveReview, "independent_sink", independent,
            ), mock.patch.object(
                replay.v002.ExactLiveReview, "validate_l10_stage_pair", pair,
            ):
                for artifact_id, record in (
                    ("A15_L10_STAGE_GATE", a15),
                    ("A16_L10_STAGE_AUDIT", a16),
                ):
                    review.production_sink(artifact_id, record)
                    review.independent_sink(artifact_id, record)
                review.validate_l10_stage_pair(
                    a15, a16, {}, "a" * 64, "b" * 64, "c" * 64,
                )
            self.assertEqual(
                seen,
                [
                    ("A15_L10_STAGE_GATE", review._record_bytes(a15)),
                    ("A15_L10_STAGE_GATE", review._record_bytes(a15)),
                    ("A16_L10_STAGE_AUDIT", review._record_bytes(a16)),
                    ("A16_L10_STAGE_AUDIT", review._record_bytes(a16)),
                ],
            )
            self.assertTrue(review._l10_batch_closed)
            self.assertTrue(all(
                getattr(review.validators, name) is value
                for name, value in originals.items()
            ))
        finally:
            review.close()

    def test_coordinate_substitution_and_cleanup_on_refusal(self) -> None:
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
        self.assertFalse(captured[0]._stage_root.exists())

    def test_plan_claim_boundary_and_no_canonical_execution(self) -> None:
        plan = replay.replay_plan()
        self.assertEqual(
            plan["classification"],
            "BOUNDED_NONEXECUTED_V005_STAGED_PATH_PLAN",
        )
        self.assertFalse(plan["record_bytes_changed"])
        self.assertFalse(plan["publisher_or_publication_order_changed"])
        self.assertFalse(plan["canonical_action_executed"])
        self.assertIn("NO_ACTION_SOURCE_HISTORY_PHYSICS_THRESHOLD", plan["claim_boundary"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
