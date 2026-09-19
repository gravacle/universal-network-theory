#!/usr/bin/env python3
"""Verify the sealed Stage-6R3 report and reproduce it from pinned inputs."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import stage6r3_supplemental_adjudicator as adjudicator


HERE = Path(__file__).resolve().parent
REPORT = HERE / "STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json"
REPORT_SHA256 = "7fa2062f18be3c90c9167e917974d1cc609273da623966e4068f1c0d1133e2b4"
ADJUDICATOR_SHA256 = "c46b7511bcab4a99ea180b4390293cd92d1ec1ccf614cbb05475adbb4db31393"


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    raw = REPORT.read_bytes()
    actual_report_hash = hashlib.sha256(raw).hexdigest()
    demand(actual_report_hash == REPORT_SHA256, "sealed Stage-6R3 report hash mismatch")
    actual_script_hash = hashlib.sha256((HERE / "stage6r3_supplemental_adjudicator.py").read_bytes()).hexdigest()
    demand(actual_script_hash == ADJUDICATOR_SHA256, "Stage-6R3 adjudicator hash mismatch")
    sealed = json.loads(raw.decode("utf-8"))
    rebuilt = adjudicator.build_report(adjudicator.parser().parse_args([]))
    demand(sealed == rebuilt, "fresh Stage-6R3 reconstruction differs from sealed report")
    demand(
        sealed["classification"]
        == "STAGE6R3_RECORD_FLOW_OBSERVED__ORIGINAL_Z1_GATE_REMAINS_REJECTED",
        "Stage-6R3 classification mismatch",
    )
    demand(
        sealed["aggregation_rules"]["whole_sector_connectivity_rule"]["arithmetic_threshold_crossed"]
        is True,
        "whole-sector arithmetic result changed",
    )
    demand(
        sealed["aggregation_rules"]["whole_sector_connectivity_rule"]["admissible_as_stage6_candidate"]
        is False,
        "unadopted whole-sector rule was treated as admissible",
    )
    demand(
        sealed["aggregation_rules"]["conservative_flow_support_rule"]["threshold_disposition"]
        == "UNRESOLVED_FAIL_CLOSED",
        "conservative flow rule did not remain fail-closed",
    )
    demand(sealed["stage7_gate"]["authorized"] is False, "Stage 7 was unexpectedly authorized")
    print("STAGE6R3_VERIFICATION=PASS")
    print(f"REPORT_SHA256={actual_report_hash}")
    print("DETERMINISTIC_RECONSTRUCTION_MATCH=TRUE")
    print("STAGE7_AUTHORIZED=FALSE")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, RuntimeError, adjudicator.Refusal) as error:
        print(f"STAGE6R3_VERIFICATION=FAIL: {error}")
        sys.exit(2)
