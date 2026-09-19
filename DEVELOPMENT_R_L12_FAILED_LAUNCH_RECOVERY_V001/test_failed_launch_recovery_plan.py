#!/usr/bin/env python3
"""Read-only tests for the failed-launch custody and retry plan."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "failed_launch_recovery_plan.py"
SPEC = importlib.util.spec_from_file_location("failed_launch_plan_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
planmod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = planmod
SPEC.loader.exec_module(planmod)


class FailedLaunchRecoveryPlanTests(unittest.TestCase):
    def test_exact_live_census_and_plan(self) -> None:
        result = planmod.build_plan()
        self.assertEqual(result["failed_attempt"]["present_count"], 12)
        self.assertEqual(result["failed_attempt"]["absent_count"], 9)
        self.assertFalse(result["failed_attempt"]["physical_history_compute_began"])
        self.assertEqual(
            result["failed_attempt"]["target_failure_classification"],
            "SECONDARY_PEER_EXIT_CASCADE",
        )

    def test_all_present_artifacts_are_immutable_and_exact(self) -> None:
        self.assertEqual(len(planmod.PRESENT_ATTEMPT_ARTIFACTS), 12)
        for artifact in planmod.PRESENT_ATTEMPT_ARTIFACTS:
            planmod._authenticate(artifact)
            metadata = os.stat(artifact.path, follow_symlinks=False)
            self.assertEqual(metadata.st_mode & 0o222, 0)
            self.assertEqual(metadata.st_nlink, 1)

    def test_nine_absences_include_all_four_final_paths(self) -> None:
        self.assertEqual(len(planmod.ABSENT_ATTEMPT_PATHS), 9)
        self.assertEqual(
            set(planmod.UNCHANGED_FINAL_PATHS.values()).issubset(
                set(planmod.ABSENT_ATTEMPT_PATHS.values())
            ),
            True,
        )
        for name, path in planmod.ABSENT_ATTEMPT_PATHS.items():
            self.assertFalse(os.path.lexists(path), name)

    def test_retry_namespace_is_unique_absent_and_keeps_final_paths(self) -> None:
        result = planmod.build_plan()["retry_v002"]
        retry = set(planmod.RETRY_CONTROL_PATHS.values())
        prior = {item.path for item in planmod.PRESENT_ATTEMPT_ARTIFACTS}
        final = set(planmod.UNCHANGED_FINAL_PATHS.values())
        self.assertEqual(len(retry), 18)
        self.assertFalse(retry & prior)
        self.assertFalse(retry & final)
        self.assertEqual(
            result["unchanged_final_paths"],
            {name: str(path) for name, path in planmod.UNCHANGED_FINAL_PATHS.items()},
        )
        for path in retry:
            self.assertFalse(os.path.lexists(path))

    def test_historical_interface_is_exactly_the_build_gate_interface(self) -> None:
        gate = planmod._authenticate(planmod.HOSTILE_BUILD_AUTHORIZATION)
        self.assertIsInstance(gate, dict)
        interface = gate["target_v012_interface"]
        expected = {
            "freeze_sha256": planmod.HISTORICAL_TARGET_INTERFACE[0].sha256,
            "audit_sha256": planmod.HISTORICAL_TARGET_INTERFACE[1].sha256,
            "L10_gate_sha256": planmod.HISTORICAL_TARGET_INTERFACE[2].sha256,
            "L12_cache_manifest_sha256": planmod.HISTORICAL_TARGET_INTERFACE[3].sha256,
            "consumer_sha256": planmod.TARGET_CONSUMER.sha256,
        }
        for key, digest in expected.items():
            self.assertEqual(interface[key], digest)
        for artifact in planmod.HISTORICAL_TARGET_INTERFACE:
            planmod._authenticate(artifact)

    def test_active_target_hashes_are_not_substituted_for_historical_lineage(self) -> None:
        active = (
            planmod.TARGET / "FREEZE.json",
            planmod.ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
            planmod.TARGET / "CACHED_L10_GATE_V012.json",
            planmod.TARGET / "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json",
        )
        import hashlib
        observed = [hashlib.sha256(path.read_bytes()).hexdigest() for path in active]
        historical = [item.sha256 for item in planmod.HISTORICAL_TARGET_INTERFACE]
        self.assertTrue(all(left != right for left, right in zip(observed, historical)))

    def test_future_adapter_is_absent_and_blocks_execution_readiness(self) -> None:
        result = planmod.build_plan()["retry_v002"]
        self.assertFalse(os.path.lexists(planmod.FUTURE_HOSTILE_ADAPTER_PATH))
        self.assertFalse(result["execution_ready"])
        self.assertFalse(
            result["future_hostile_adapter"]["physical_operator_change_permitted"]
        )
        self.assertEqual(len(result["blocking_preconditions"]), 4)

    def test_unchanged_physical_consumers_are_hash_authenticated(self) -> None:
        planmod._authenticate(planmod.TARGET_CONSUMER)
        planmod._authenticate(planmod.HOSTILE_CONSUMER)
        result = planmod.build_plan()["retry_v002"]["physical_consumers"]
        self.assertEqual(
            result["target_v012"]["sha256"], planmod.TARGET_CONSUMER.sha256,
        )
        self.assertEqual(
            result["hostile_v004r4"]["sha256"], planmod.HOSTILE_CONSUMER.sha256,
        )

    def test_wrong_hash_and_occupied_future_path_refuse(self) -> None:
        artifact = planmod.PRESENT_ATTEMPT_ARTIFACTS[0]
        mutant = planmod.Artifact(
            artifact.name, artifact.path, "0" * 64,
            artifact.schema, artifact.classification,
        )
        with self.assertRaisesRegex(planmod.PlanRefusal, "hash or identity"):
            planmod._authenticate(mutant)
        occupied = planmod.RETRY_CONTROL_PATHS["schedule"]
        real_lexists = os.path.lexists
        with mock.patch.object(
            planmod.os.path, "lexists",
            side_effect=lambda path: (
                True if Path(path) == occupied else real_lexists(path)
            ),
        ):
            with self.assertRaisesRegex(planmod.PlanRefusal, "already occupied"):
                planmod._require_absent(occupied, "synthetic occupied")

    def test_plan_has_no_canonical_side_effect(self) -> None:
        watched = (
            *(item.path for item in planmod.PRESENT_ATTEMPT_ARTIFACTS),
            *planmod.ABSENT_ATTEMPT_PATHS.values(),
            *planmod.RETRY_CONTROL_PATHS.values(),
            *planmod.UNCHANGED_FINAL_PATHS.values(),
            planmod.FUTURE_HOSTILE_ADAPTER_PATH,
        )
        before = {path: os.path.lexists(path) for path in watched}
        result = planmod.build_plan()
        after = {path: os.path.lexists(path) for path in watched}
        self.assertEqual(before, after)
        self.assertFalse(result["published"])
        self.assertFalse(result["launched"])

    def test_cli_is_plan_only(self) -> None:
        with mock.patch.object(planmod.sys, "argv", [str(SOURCE), "plan"]):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(planmod.main(), 0)
            self.assertEqual(
                json.loads(output.getvalue())["classification"],
                "PASS_DEVELOPMENT_ONLY_FAILED_LAUNCH_CUSTODY_AND_RETRY_PLAN",
            )
        for argv in ([str(SOURCE)], [str(SOURCE), "launch"], [str(SOURCE), "plan", "extra"]):
            with self.subTest(argv=argv), mock.patch.object(planmod.sys, "argv", argv):
                error = io.StringIO()
                with redirect_stderr(error):
                    self.assertEqual(planmod.main(), 2)
                self.assertIn("exact DEVELOPMENT mode is plan", error.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
