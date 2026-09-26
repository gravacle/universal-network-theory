#!/usr/bin/env python3
"""Tests for the exact held-out input/resource gate validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("heldout_gate", HERE / "validate_heldout_gate.py")
assert SPEC is not None and SPEC.loader is not None
gate_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate_module)


class HeldoutGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = gate_module.strict_json(HERE / "INPUT_AND_RESOURCE_GATE.json")

    def test_packet_and_metadata_validate_without_opening_amplitudes(self) -> None:
        result = gate_module.validate_gate(full_shard_hash=False)
        self.assertEqual(result["classification"], "PASS_HELDOUT_INPUT_AND_RESOURCE_GATE_PREOUTPUT")
        self.assertFalse(result["witness_values_computed_or_opened"])
        self.assertEqual(result["input_histories_verified"], 4)
        self.assertEqual(result["terminal_shards_verified"], 44)

    def test_resource_arithmetic_is_exact_and_fail_closed(self) -> None:
        gate_module.validate_resource_arithmetic(self.gate["resource_gate"])
        broken = copy.deepcopy(self.gate["resource_gate"])
        broken["combined_scratch_minimum_bytes"] += 1
        with self.assertRaises(gate_module.Refusal):
            gate_module.validate_resource_arithmetic(broken)

    def test_duplicate_and_nonfinite_json_are_refused(self) -> None:
        with self.assertRaises(gate_module.Refusal):
            gate_module.strict_json_bytes(b'{"a":1,"a":2}')
        with self.assertRaises(gate_module.Refusal):
            gate_module.strict_json_bytes(b'{"a":NaN}')

    def telemetry(self, schedule: str = "SEQUENTIAL_TARGET_THEN_HOSTILE") -> dict[str, object]:
        return {
            "available_memory_bytes": 40_000_000_000,
            "captured_epoch_seconds": 1_000,
            "hostile_output_path": "heldout/hostile.json",
            "hostile_scratch_root": "scratch/hostile",
            "memory_pressure": "NORMAL",
            "schema": "OWNER_ONCE_HELDOUT_RESOURCE_TELEMETRY_V001",
            "selected_schedule": schedule,
            "shared_filesystem_free_bytes": 20_000_000_000,
            "target_output_path": "heldout/target.json",
            "target_scratch_root": "scratch/target",
            "total_host_memory_bytes": 48_000_000_000,
        }

    def test_fresh_sequential_and_concurrent_telemetry(self) -> None:
        resource = self.gate["resource_gate"]
        self.assertEqual(
            gate_module.validate_telemetry(self.telemetry(), resource, 1_300),
            "SEQUENTIAL_TARGET_THEN_HOSTILE",
        )
        self.assertEqual(
            gate_module.validate_telemetry(
                self.telemetry("CONCURRENT_TARGET_AND_HOSTILE"), resource, 1_300
            ),
            "CONCURRENT_TARGET_AND_HOSTILE",
        )

    def test_stale_or_underprovisioned_telemetry_is_refused(self) -> None:
        resource = self.gate["resource_gate"]
        with self.assertRaises(gate_module.Refusal):
            gate_module.validate_telemetry(self.telemetry(), resource, 1_301)
        low_ram = self.telemetry("CONCURRENT_TARGET_AND_HOSTILE")
        low_ram["available_memory_bytes"] = resource["concurrent_available_memory_minimum_bytes"] - 1
        with self.assertRaises(gate_module.Refusal):
            gate_module.validate_telemetry(low_ram, resource, 1_100)
        low_disk = self.telemetry()
        low_disk["shared_filesystem_free_bytes"] = resource["combined_scratch_minimum_bytes"] - 1
        with self.assertRaises(gate_module.Refusal):
            gate_module.validate_telemetry(low_disk, resource, 1_100)

    def test_telemetry_paths_must_be_distinct_and_relative(self) -> None:
        resource = self.gate["resource_gate"]
        duplicate = self.telemetry()
        duplicate["hostile_scratch_root"] = duplicate["target_scratch_root"]
        with self.assertRaises(gate_module.Refusal):
            gate_module.validate_telemetry(duplicate, resource, 1_100)
        absolute = self.telemetry()
        absolute["target_output_path"] = "/tmp/target.json"
        with self.assertRaises(gate_module.Refusal):
            gate_module.validate_telemetry(absolute, resource, 1_100)

    def test_canonical_manifest_digest_is_order_and_path_sensitive(self) -> None:
        rows = [
            {"bytes": 16, "path": "x/q_00.c128", "q": 0, "sha256": "0" * 64, "shape": [1, 1]},
            {"bytes": 32, "path": "x/q_01.c128", "q": 1, "sha256": "1" * 64, "shape": [1, 2]},
        ]
        digest = gate_module.shard_manifest_digest(rows)
        self.assertNotEqual(digest, gate_module.shard_manifest_digest(list(reversed(rows))))
        changed = copy.deepcopy(rows)
        changed[0]["path"] = "y/q_00.c128"
        self.assertNotEqual(digest, gate_module.shard_manifest_digest(changed))


if __name__ == "__main__":
    unittest.main()
