#!/usr/bin/env python3

import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "kernels"))

from capacity_plan import evaluate, hostile_row_estimate_bytes, safe_worker_ceiling
import resource_scheduler


def capacity_config():
    return {
        "workers_per_branch": 180,
        "physical_cores_per_instance": 192,
        "observed_memory_mib_per_instance": 1_572_864,
        "worker_memory_fraction_limit": 0.55,
        "hostile_allocation_vector_slots": 20,
        "hostile_numerical_workspace_limit_bytes": 2_400_000_000,
    }


class CapacityPlanTests(unittest.TestCase):
    def test_frozen_recurrence_arithmetic_is_preserved(self):
        self.assertEqual(hostile_row_estimate_bytes(14, 9, 20), 2_210_208_000)
        self.assertEqual(hostile_row_estimate_bytes(14, 14, 20), 12_837_312_000)

    def test_worker_ceiling_floors_the_declared_memory_fraction(self):
        self.assertEqual(
            safe_worker_ceiling(1_572_864, Decimal("0.55"), 12_837_312_000),
            70,
        )

    def test_certificate_covers_every_sector_through_the_centerline(self):
        result = evaluate(capacity_config())
        self.assertTrue(result["classification"].startswith("PASS_"))
        self.assertEqual(result["schema"], "L14_Q_AWARE_CAPACITY_PLAN_V003")
        self.assertEqual([row["q"] for row in result["sectors"]], list(range(15)))
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["physics_changes"], [])

    def test_large_sectors_taper_concurrency_instead_of_rejecting_physics(self):
        result = evaluate(capacity_config())
        by_q = {row["q"]: row for row in result["sectors"]}
        self.assertEqual(by_q[0]["certified_concurrency"], 180)
        self.assertEqual(by_q[9]["certified_concurrency"], 180)
        self.assertEqual(by_q[10]["certified_concurrency"], 180)
        self.assertEqual(by_q[11]["certified_concurrency"], 132)
        self.assertEqual(by_q[12]["certified_concurrency"], 93)
        self.assertEqual(by_q[13]["certified_concurrency"], 75)
        self.assertEqual(by_q[14]["certified_concurrency"], 70)
        for row in result["sectors"]:
            self.assertGreaterEqual(row["memory_budget_headroom_bytes"], 0)

    def test_certificate_matches_the_bundled_q_aware_scheduler(self):
        config = capacity_config()
        result = evaluate(config)
        self.assertEqual(
            result["memory_budget_bytes"],
            resource_scheduler.NUMERICAL_RESERVATION_BUDGET_BYTES,
        )
        self.assertEqual(
            config["hostile_allocation_vector_slots"],
            resource_scheduler.HOSTILE_ALLOCATION_VECTOR_SLOTS,
        )
        for row in result["sectors"]:
            q = row["q"]
            charge = resource_scheduler.hostile_workspace_bytes(q)
            expected = min(
                config["workers_per_branch"],
                config["physical_cores_per_instance"],
                resource_scheduler.NUMERICAL_RESERVATION_BUDGET_BYTES // charge,
            )
            self.assertEqual(row["certified_worker_charge_bytes"], charge)
            self.assertEqual(row["certified_concurrency"], expected)

    def test_q_specific_legacy_certificate_fields_fail_closed(self):
        config = capacity_config()
        config["hostile_q9_columns"] = 6_906_900
        config["hostile_q9_single_row_estimate_bytes"] = 2_210_208_000
        result = evaluate(config)
        self.assertFalse(
            result["checks"]["configuration_has_no_q_specific_capacity_certificate"]
        )
        self.assertEqual(result["classification"], "FAIL_CLOSED_Q0_Q14_CAPACITY_CERTIFICATE")

    def test_memory_that_cannot_admit_one_centerline_worker_fails_closed(self):
        config = capacity_config()
        config["observed_memory_mib_per_instance"] = 1024
        result = evaluate(config)
        self.assertFalse(result["checks"]["all_sectors_admit_at_least_one_worker"])
        self.assertEqual(result["classification"], "FAIL_CLOSED_Q0_Q14_CAPACITY_CERTIFICATE")

    def test_checked_in_configuration_has_the_same_complete_certificate(self):
        config = json.loads(
            (ROOT / "AWS_RUN_CONFIG.example.json").read_text(encoding="utf-8")
        )
        result = evaluate(config)
        self.assertTrue(result["classification"].startswith("PASS_"))
        self.assertEqual(result["sector_count"], 15)
        self.assertEqual(result["minimum_certified_concurrency"], 70)


if __name__ == "__main__":
    unittest.main()
