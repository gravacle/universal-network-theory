#!/usr/bin/env python3
"""Focused non-live tests for the fixed Stage-3 data-lineage replay."""

from __future__ import annotations

import copy
import hashlib
import json
import stat
import tempfile
import unittest
from pathlib import Path

import stage3_data_lineage_replay as replay


class FixedScopeTests(unittest.TestCase):
    def test_plan_is_nonexecuting_and_exact_scope(self) -> None:
        row = replay.plan()
        self.assertEqual(row["stale_entry_count"], 20)
        self.assertEqual(len(set(row["stale_paths"])), 20)
        self.assertTrue(row["live_stops_before_l12_launch"])
        self.assertEqual(
            row["candidate_build_gate_sha256"],
            replay.EXPECTED_BUILD_GATE_SHA256,
        )
        self.assertEqual(
            row["unchanged_physics_executables"]["consumer"],
            replay.PINNED_SOURCE_SHA256[replay.CONSUMER],
        )

    def test_current_dry_run_authenticates_without_output(self) -> None:
        before = replay.AUDIT_ROOT.exists()
        row = replay.dry_run()
        self.assertEqual(row["classification"], "PASS_FIXED_SCOPE_DRY_RUN_NO_MUTATION")
        self.assertEqual(row["authenticated_stale_entry_count"], 20)
        self.assertFalse(row["canonical_action_executed"])
        self.assertEqual(replay.AUDIT_ROOT.exists(), before)

    def test_build_gate_exact_four_hash_transform(self) -> None:
        old = replay.strict_json(replay.BUILD_GATE.read_bytes(), "old gate")
        candidate = replay.build_gate_candidate(old)
        self.assertEqual(
            hashlib.sha256(replay.canonical_json_bytes(candidate)).hexdigest(),
            replay.EXPECTED_BUILD_GATE_SHA256,
        )
        changed = {
            key for key in replay.CURRENT_TARGET_INTERFACE
            if old["target_v012_interface"][key]
            != candidate["target_v012_interface"][key]
        }
        self.assertEqual(changed, {
            "freeze_sha256", "audit_sha256", "L10_gate_sha256",
            "L12_cache_manifest_sha256",
        })

    def test_build_gate_non_four_hash_drift_refuses(self) -> None:
        old = replay.strict_json(replay.BUILD_GATE.read_bytes(), "old gate")
        changed = copy.deepcopy(old)
        changed["target_v012_interface"]["consumer_sha256"] = "0" * 64
        with self.assertRaises(replay.Refusal):
            replay.build_gate_candidate(changed)
        extra = copy.deepcopy(old)
        extra["extra"] = False
        with self.assertRaises(replay.Refusal):
            replay.build_gate_candidate(extra)

    def test_manifest_predictions_are_exact(self) -> None:
        self.assertEqual(
            replay.predicted_manifest_hashes(),
            replay.EXPECTED_MANIFEST_SHA256,
        )

    def test_l10_authorization_is_exact_candidate(self) -> None:
        record = replay.l10_authorization_record()
        self.assertEqual(
            hashlib.sha256(replay.canonical_json_bytes(record)).hexdigest(),
            replay.EXPECTED_L10_AUTHORIZATION_SHA256,
        )

    def test_l10_gate_fixed_obligations(self) -> None:
        record = replay.l10_gate_record("1" * 64)
        self.assertEqual(record["checks_passed"], 27)
        self.assertEqual(record["checks_total"], sum(record["checks"].values()))
        self.assertEqual(
            record["cache_manifest_sha256_by_L"]["10"],
            replay.EXPECTED_MANIFEST_SHA256[10],
        )

    def test_transitive_target_interface_accepts_and_rejects(self) -> None:
        branch = {
            "freeze": {"sha256": replay.CURRENT_TARGET_INTERFACE["freeze_sha256"]},
            "independent_audit": {"sha256": replay.CURRENT_TARGET_INTERFACE["audit_sha256"]},
            "consumer": {"sha256": replay.CURRENT_TARGET_INTERFACE["consumer_sha256"]},
            "cached_L10_gate": {"sha256": replay.CURRENT_TARGET_INTERFACE["L10_gate_sha256"]},
            "L12_cache_manifest": {"sha256": replay.CURRENT_TARGET_INTERFACE["L12_cache_manifest_sha256"]},
        }
        gate = {"target_v012_interface": dict(replay.CURRENT_TARGET_INTERFACE)}
        replay.transitive_target_interface_equal({"target": {"branch": branch}}, gate)
        forged = copy.deepcopy(branch)
        forged["freeze"]["sha256"] = "2" * 64
        with self.assertRaises(replay.Refusal):
            replay.transitive_target_interface_equal({"target": {"branch": forged}}, gate)

    def test_live_requires_exact_authorization_before_mutation(self) -> None:
        before = replay.AUDIT_ROOT.exists()
        with self.assertRaises(replay.Refusal):
            replay.execute_live(None)
        with self.assertRaises(replay.Refusal):
            replay.execute_live("wrong")
        self.assertEqual(replay.AUDIT_ROOT.exists(), before)

    def test_synthetic_publish_once_is_no_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.json"
            digest = replay.publish_once(path, {"schema": "SYNTHETIC"})
            self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o444)
            with self.assertRaises(replay.Refusal):
                replay.publish_once(path, {"schema": "CHANGED"})
            self.assertEqual(replay.strict_json(path.read_bytes(), "synthetic")["schema"], "SYNTHETIC")

    def test_no_adapter_or_generalized_execution_surface(self) -> None:
        source = Path(replay.__file__).read_text(encoding="utf-8")
        for forbidden in (
            "HISTORICAL_INTERFACE_CUSTODY_ADAPTER",
            "historical_interface_custody_adapter",
            "sys.modules[",
            "exec(compile",
            "eval(",
        ):
            self.assertNotIn(forbidden, source)
        self.assertNotIn("L12", replay.run_checked.__doc__ or "")


if __name__ == "__main__":
    unittest.main()
