#!/usr/bin/env python3

import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from readiness import (
    authenticate_existing_scout_instances,
    extract_linux_on_demand_hourly_price,
    verify_local,
)


class ReadinessTests(unittest.TestCase):
    def test_budget_state_is_advisory_not_a_launch_blocker(self):
        source = (ROOT / "readiness.py").read_text(encoding="utf-8")
        for code in (
            '"AWS_BUDGET"',
            '"AWS_BUDGET_NOTIFICATIONS"',
            '"AWS_BUDGET_EMAIL_SUBSCRIBERS"',
        ):
            self.assertNotIn("check(False, {}".format(code), source)
        self.assertIn(
            '"{} observed versus {} configured; execution is not gated"', source
        )

    def test_extracts_unique_hourly_price(self):
        product = {
            "terms": {
                "OnDemand": {
                    "term": {
                        "priceDimensions": {
                            "dimension": {
                                "unit": "Hrs",
                                "pricePerUnit": {"USD": "21.2890000000"},
                            }
                        }
                    }
                }
            }
        }
        self.assertEqual(
            extract_linux_on_demand_hourly_price({"PriceList": [json.dumps(product)]}),
            Decimal("21.2890000000"),
        )

    def test_ambiguous_price_fails_closed(self):
        def product(price):
            return json.dumps(
                {
                    "terms": {
                        "OnDemand": {
                            "term": {
                                "priceDimensions": {
                                    "dimension": {"unit": "Hrs", "pricePerUnit": {"USD": price}}
                                }
                            }
                        }
                    }
                }
            )

        with self.assertRaises(RuntimeError):
            extract_linux_on_demand_hourly_price({"PriceList": [product("21"), product("22")]})

    def test_only_exact_declared_stopped_instances_are_allowed(self):
        allowed = [
            {
                "instance_id": "i-target",
                "run_id": "L14-SCOUT-R1",
                "branch": "target",
            },
            {
                "instance_id": "i-hostile",
                "run_id": "L14-SCOUT-R1",
                "branch": "hostile",
            },
        ]
        observed = [
            {
                "instance_id": "i-target",
                "state": "stopped",
                "tags": {"Project": "L14-Scout", "RunId": "L14-SCOUT-R1", "Branch": "target"},
            },
            {
                "instance_id": "i-hostile",
                "state": "stopped",
                "tags": {"Project": "L14-Scout", "RunId": "L14-SCOUT-R1", "Branch": "hostile"},
            },
        ]
        passed, _detail = authenticate_existing_scout_instances(observed, allowed)
        self.assertTrue(passed)

        observed[0]["state"] = "running"
        passed, _detail = authenticate_existing_scout_instances(observed, allowed)
        self.assertFalse(passed)

        observed[0]["state"] = "stopped"
        observed.append(
            {
                "instance_id": "i-undeclared",
                "state": "stopped",
                "tags": {"Project": "L14-Scout", "RunId": "L14-SCOUT-R1", "Branch": "target"},
            }
        )
        passed, _detail = authenticate_existing_scout_instances(observed, allowed)
        self.assertFalse(passed)

    def test_profiles_are_explicitly_separated(self):
        config = json.loads((ROOT / "AWS_RUN_CONFIG.example.json").read_text())
        bindings = json.loads((ROOT / "KERNEL_BINDINGS_RELEASE_V003R3.json").read_text())
        checks = []
        blockers = []
        verify_local(config, bindings, checks, blockers)
        by_code = {record["code"]: record for record in checks}
        self.assertTrue(by_code["INSPECTION_PROFILE_BOUND"]["passed"])
        self.assertTrue(by_code["CONTROL_PROFILE_BOUND_AND_SEPARATE"]["passed"])
        self.assertTrue(by_code["EXACT_KERNEL_PORT_AUDIT_AUTHENTICATED"]["passed"])

        config["control_profile"] = config["inspection_profile"]
        checks = []
        blockers = []
        verify_local(config, bindings, checks, blockers)
        by_code = {record["code"]: record for record in checks}
        self.assertFalse(by_code["CONTROL_PROFILE_BOUND_AND_SEPARATE"]["passed"])
        self.assertIn("CONTROL_PROFILE_BOUND_AND_SEPARATE", blockers)


if __name__ == "__main__":
    unittest.main()
