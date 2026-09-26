#!/usr/bin/env python3
"""Fail-closed synthetic tests for target production custody/orchestration."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

import heldout_target_adapter as target
import target_production_orchestrator as production


class BadAdmissionBackend(target.SyntheticBackend):
    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
        del event, q
        return np.array([0, 0], dtype=np.int64), np.array([0, 0], dtype=np.int64)


def initial_shards(length: int) -> list[np.ndarray]:
    blocks = [
        np.zeros(
            (
                len(target.fixed_words(length - 1, q)),
                len(target.fixed_words(2 * length, q)),
            ),
            dtype=np.complex128,
        )
        for q in range(length)
    ]
    blocks[0][0, 0] = 1.0
    return blocks


def telemetry_record(now: int) -> dict[str, object]:
    return {
        "available_memory_bytes": 40_000_000_000,
        "captured_epoch_seconds": now,
        "hostile_output_path": "HOSTILE/OUTPUT.json",
        "hostile_scratch_root": "HOSTILE/SCRATCH",
        "memory_pressure": "NORMAL",
        "schema": "OWNER_ONCE_HELDOUT_RESOURCE_TELEMETRY_V001",
        "selected_schedule": "SEQUENTIAL_TARGET_THEN_HOSTILE",
        "shared_filesystem_free_bytes": 40_000_000_000,
        "target_output_path": production.TARGET_OUTPUT_RELATIVE,
        "target_scratch_root": production.TARGET_SCRATCH_RELATIVE,
        "total_host_memory_bytes": 48_000_000_000,
    }


class ProductionGuardTests(unittest.TestCase):
    def _load_v012_consumer_without_cache(self) -> object:
        path = target.ROOT / target.TARGET_CONSUMER_RELATIVE_PATH
        source_dir = str(path.parent)
        sys.path.insert(0, source_dir)
        try:
            return target._load_module("guard_test_v012_consumer", path)
        finally:
            if sys.path and sys.path[0] == source_dir:
                sys.path.pop(0)

    def test_authenticated_v003_capacity_profile(self) -> None:
        record = target.authenticate_target_capacity_profile()
        self.assertEqual(record["maximum_subdivisions"], 256)
        self.assertEqual(record["coarse"]["checkpoints"][-1], 80)
        self.assertEqual(record["fine"]["checkpoints"][-1], 96)

    def test_canonical_auditor_and_v012_cache_manifests_authenticate(self) -> None:
        authority = target.authenticate_canonical_final_auditor()
        self.assertEqual(
            authority[target.CANONICAL_AUDITOR_RELATIVE_PATH],
            target.CANONICAL_AUDITOR_SHA256,
        )
        observed = target.authenticate_target_transitive_sources()
        for relative, expected in target.TARGET_V012_CACHE_MANIFEST_SHA256.items():
            self.assertEqual(observed[relative], expected)

    def test_v012_auditor_correction_changes_one_leaf_and_restores(self) -> None:
        consumer = self._load_v012_consumer_without_cache()
        builder = consumer.builder
        original_track = builder.TRACK_C_REFINEMENT_SHA256
        original_require = builder.require_frozen_census
        correction = target._V012AuditorProvenanceCorrection(
            builder, root=target.ROOT, monitor=None
        )
        try:
            changed = {
                key
                for key in original_track
                if original_track[key] != builder.TRACK_C_REFINEMENT_SHA256[key]
            }
            self.assertEqual(changed, {target.V012_AUDITOR_TRACK_KEY})
            self.assertEqual(
                builder.TRACK_C_REFINEMENT_SHA256[target.V012_AUDITOR_TRACK_KEY],
                target.CANONICAL_AUDITOR_SHA256,
            )
            freeze = builder.require_frozen_census()
            self.assertEqual(
                freeze["sealed_dependencies"]
                ["v012_production_dag_refinement_sources"]
                [target.V012_AUDITOR_TRACK_KEY],
                target.CANONICAL_AUDITOR_SHA256,
            )
        finally:
            correction.restore()
        self.assertIs(builder.TRACK_C_REFINEMENT_SHA256, original_track)
        self.assertIs(builder.require_frozen_census, original_require)

    def test_v012_auditor_correction_refuses_any_other_drift(self) -> None:
        consumer = self._load_v012_consumer_without_cache()
        builder = consumer.builder
        original_track = builder.TRACK_C_REFINEMENT_SHA256
        drifted = dict(original_track)
        drifted[
            f"{target.CANONICAL_AUDITOR_PACKET_DIR}/production_dag_refinement.py"
        ] = "0" * 64
        builder.TRACK_C_REFINEMENT_SHA256 = drifted
        try:
            with self.assertRaises(target.HeldoutRefusal):
                target._V012AuditorProvenanceCorrection(
                    builder, root=target.ROOT, monitor=None
                )
        finally:
            builder.TRACK_C_REFINEMENT_SHA256 = original_track

    def test_backend_authenticates_cache_before_runtime_capacity_overrides(self) -> None:
        consumer = self._load_v012_consumer_without_cache()
        original_builder_wall = consumer.builder.WALL_LIMIT
        original_engine_wall = consumer.v004.WALL_LIMIT
        original_subdivisions = consumer.v004.v3.MAX_SUBDIVISIONS
        observed: list[tuple[float, float, int]] = []

        class FrozenContextProbe:
            def __init__(self, root: Path, length: int, manifest_sha256: str):
                del root, length, manifest_sha256
                observed.append(
                    (
                        consumer.builder.WALL_LIMIT,
                        consumer.v004.WALL_LIMIT,
                        consumer.v004.v3.MAX_SUBDIVISIONS,
                    )
                )

            def close(self) -> None:
                return None

        with (
            patch.object(
                target, "authenticate_target_transitive_sources", return_value={}
            ),
            patch.object(target, "_load_module", return_value=consumer),
            patch.object(consumer, "CacheContext", FrozenContextProbe),
        ):
            backend = target.ProductionBackend(10)
            try:
                self.assertEqual(
                    observed,
                    [
                        (
                            original_builder_wall,
                            original_engine_wall,
                            original_subdivisions,
                        )
                    ],
                )
                self.assertEqual(consumer.builder.WALL_LIMIT, 345_600.0)
                self.assertEqual(consumer.v004.WALL_LIMIT, 345_600.0)
                self.assertEqual(
                    consumer.v004.v3.MAX_SUBDIVISIONS,
                    target.TARGET_V003_MAX_SUBDIVISIONS,
                )
            finally:
                backend.close()
        self.assertEqual(consumer.builder.WALL_LIMIT, original_builder_wall)
        self.assertEqual(consumer.v004.WALL_LIMIT, original_engine_wall)
        self.assertEqual(consumer.v004.v3.MAX_SUBDIVISIONS, original_subdivisions)

    def test_admission_map_must_be_injective_and_canonical(self) -> None:
        with self.assertRaises(target.HeldoutRefusal):
            target.stream_terminal_children(
                length=2,
                shards=initial_shards(2),
                backend=BadAdmissionBackend(2),
                resolution="synthetic",
            )

    def test_stable_descriptor_detects_path_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "q_00.npy"
            np.save(path, np.ones((1, 1), dtype=np.complex128), allow_pickle=False)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            metadata = target.AuthenticatedShard(
                q=0,
                path=path,
                shape=(1, 1),
                byte_count=path.stat().st_size,
                sha256=digest,
            )
            stable = target._open_generated_shards([metadata], monitor=None)
            try:
                original = root / "original.npy"
                path.rename(original)
                np.save(path, np.zeros((1, 1), dtype=np.complex128), allow_pickle=False)
                with self.assertRaises(target.HeldoutRefusal):
                    stable.verify()
            finally:
                stable.close()

    def test_live_resource_guard_refuses_wall_and_rss(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scratch = root / "scratch"
            scratch.mkdir()
            times = iter([0.0, 6.0])
            wall = production.LiveResourceGuard(
                root=root,
                scratch_root=scratch,
                monotonic=lambda: next(times),
                rss_probe=lambda: 0,
                wall_limit_seconds=5,
            )
            with self.assertRaises(target.HeldoutRefusal):
                wall.check("wall-test", force=True)
            rss = production.LiveResourceGuard(
                root=root,
                scratch_root=scratch,
                monotonic=lambda: 0.0,
                rss_probe=lambda: 101,
                rss_limit_bytes=100,
            )
            with self.assertRaises(target.HeldoutRefusal):
                rss.check("rss-test", force=True)

    def test_runtime_paths_refuse_alias(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            telemetry = telemetry_record(100)
            telemetry["hostile_scratch_root"] = production.TARGET_SCRATCH_RELATIVE
            with self.assertRaises(target.HeldoutRefusal):
                production._safe_runtime_paths(telemetry, root)

    def test_neutral_receipt_rejects_stale_replay(self) -> None:
        now = 1_000
        gate = target.strict_json(
            target.ROOT / target.HELDOUT_GATE_RELATIVE_PATH,
            target.HELDOUT_GATE_SHA256,
        )
        telemetry = telemetry_record(now)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            telemetry_path = root / "telemetry.json"
            telemetry_path.write_bytes(target.canonical_json_bytes(telemetry))
            receipt = {
                "classification": production.NEUTRAL_RECEIPT_CLASSIFICATION,
                "concurrent_release_deadline_epoch_seconds": None,
                "expires_epoch_seconds": now + 300,
                "full_gate_validation": {
                    "classification": "PASS_HELDOUT_INPUT_AND_RESOURCE_GATE_PREOUTPUT",
                    "full_shard_hashes_verified": True,
                    "input_histories_verified": 4,
                    "schema": "OWNER_ONCE_HELDOUT_GATE_VALIDATION_V001",
                    "terminal_shard_bytes_verified": 13_671_711_776,
                    "terminal_shards_verified": 44,
                    "witness_values_computed_or_opened": False,
                },
                "gate_input_census_sha256": target.canonical_digest(gate["inputs"]),
                "gate_resource_sha256": target.canonical_digest(gate["resource_gate"]),
                "gate_sha256": target.HELDOUT_GATE_SHA256,
                "gate_validator_sha256": target.HELDOUT_GATE_VALIDATOR_SHA256,
                "issued_epoch_seconds": now,
                "maximum_release_skew_seconds": 60,
                "protocol_sha256": target.HELDOUT_PROTOCOL_SHA256,
                "schema": production.NEUTRAL_RECEIPT_SCHEMA,
                "selected_schedule": "SEQUENTIAL_TARGET_THEN_HOSTILE",
                "telemetry_sha256": target.sha256_file(telemetry_path),
                "witness_values_computed_or_opened": False,
            }
            receipt_path = root / "receipt.json"
            receipt_path.write_bytes(target.canonical_json_bytes(receipt))
            production._validate_neutral_receipt(
                receipt_path,
                telemetry_path,
                root=target.ROOT,
                now_epoch_seconds=now,
            )
            with self.assertRaises(target.HeldoutRefusal):
                production._validate_neutral_receipt(
                    receipt_path,
                    telemetry_path,
                    root=target.ROOT,
                    now_epoch_seconds=now + 301,
                )

    def _run_synthetic_atomic(
        self,
        root: Path,
        runner: object,
    ) -> tuple[dict[str, object], Path, list[str]]:
        telemetry = telemetry_record(100)
        telemetry_path = (
            root / production.CONTROL_TELEMETRY_PARENT_RELATIVE / "telemetry.json"
        )
        receipt_path = (
            root / production.CONTROL_RECEIPT_PARENT_RELATIVE / "receipt.json"
        )
        telemetry_path.parent.mkdir(parents=True)
        receipt_path.parent.mkdir(parents=True)
        telemetry_path.write_text("{}\n", encoding="ascii")
        receipt_path.write_text("{}\n", encoding="ascii")
        with (
            patch.object(target, "authenticate_heldout_protocol", return_value={}),
            patch.object(target, "authenticate_seed_authority", return_value={}),
            patch.object(target, "authenticate_target_transitive_sources", return_value={}),
            patch.object(production, "validate_local_source_manifest", return_value={}),
            patch.object(
                production,
                "_validate_neutral_receipt",
                return_value=(
                    {"selected_schedule": "SEQUENTIAL_TARGET_THEN_HOSTILE"},
                    telemetry,
                ),
            ),
            patch.object(
                production,
                "build_raw_result",
                return_value={"schema": production.SCHEMA, "status": production.STATUS},
            ),
        ):
            result = production.run_atomic_target(
                authorization=target.EXECUTION_AUTHORIZATION,
                telemetry_path=telemetry_path,
                neutral_receipt_path=receipt_path,
                root=root,
                now=lambda: 100.0,
                monotonic=lambda: 0.0,
                component_runner=runner,
                rss_probe=lambda: 0,
            )
        output = root / production.TARGET_OUTPUT_RELATIVE
        return result, output, []

    def test_atomic_schedule_runs_both_sizes_before_publication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            calls: list[tuple[int, str]] = []

            def runner(
                length: int,
                mode: str,
                scratch: Path,
                run_root: Path,
                monitor: production.LiveResourceGuard,
            ) -> dict[str, object]:
                del scratch, run_root, monitor
                calls.append((length, mode))
                return {"registered": {"D": 0.0}}

            _result, output, stages = self._run_synthetic_atomic(root, runner)
            self.assertEqual(
                calls,
                [(10, "coarse"), (10, "fine"), (12, "coarse"), (12, "fine")],
            )
            self.assertEqual(stages, [])
            self.assertTrue(output.is_file())
            self.assertEqual(
                json.loads(output.read_text(encoding="ascii"))["status"],
                production.STATUS,
            )

    def test_atomic_failure_never_publishes_partial_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            calls = 0

            def runner(
                length: int,
                mode: str,
                scratch: Path,
                run_root: Path,
                monitor: production.LiveResourceGuard,
            ) -> dict[str, object]:
                nonlocal calls
                del length, mode, scratch, run_root, monitor
                calls += 1
                if calls == 3:
                    raise target.HeldoutRefusal("synthetic L12 obstruction")
                return {}

            with self.assertRaises(target.HeldoutRefusal):
                self._run_synthetic_atomic(root, runner)
            self.assertFalse((root / production.TARGET_OUTPUT_RELATIVE).exists())


if __name__ == "__main__":
    unittest.main()
