#!/usr/bin/env python3
"""Fail-closed verifier for the blind lineage-scaling audit packet.

With no checkpoint arguments this verifies the frozen source/input census.
The optional checkpoint mode authenticates a shard census and receipt without
executing the physical engine and without reading the blinded target lane.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import independent_scaling_audit as audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", help="repository-relative checkpoint census path")
    parser.add_argument("--census-sha256")
    parser.add_argument("--receipt", help="repository-relative checkpoint receipt path")
    parser.add_argument("--receipt-sha256")
    arguments = parser.parse_args()

    freeze = audit.verify_freeze(audit.ROOT)
    response: dict[str, object] = {
        "schema": "AUDIT_LINEAGE_SCALING_PACKET_VERIFICATION_V001",
        "source_input_freeze_sha256": audit.sha256_file(audit.FREEZE),
        "source_input_freeze_pass": True,
        "checkpoint_pass": None,
        "target_lane_read_or_imported": False,
    }
    supplied = (
        arguments.census,
        arguments.census_sha256,
        arguments.receipt,
        arguments.receipt_sha256,
    )
    if any(value is not None for value in supplied):
        if not all(value is not None for value in supplied):
            parser.error("checkpoint verification requires census/receipt paths and both hashes")
        census_descriptor = {
            "path": arguments.census,
            "sha256": arguments.census_sha256,
        }
        census_path = audit.authenticate_entry(audit.ROOT, census_descriptor)
        census_descriptor["size_bytes"] = census_path.stat().st_size
        census, _ = audit.load_authenticated_shard_census(audit.ROOT, census_descriptor)
        receipt_descriptor = {
            "path": arguments.receipt,
            "sha256": arguments.receipt_sha256,
        }
        receipt_path = audit.authenticate_entry(audit.ROOT, receipt_descriptor)
        receipt = audit.strict_json_bytes(receipt_path.read_bytes(), str(arguments.receipt))
        audit.verify_checkpoint_receipt(
            receipt,
            census,
            audit.sha256_file(audit.FREEZE),
        )
        response.update({
            "checkpoint_pass": True,
            "checkpoint_stage": receipt["stage"],
            "checkpoint_identity_sha256": receipt["checkpoint_identity_sha256"],
        })
    response["status"] = "PASS_AUDIT_PACKET_VERIFICATION"
    response["scientific_execution_authorized"] = freeze["scientific_execution_authorized"]
    print(json.dumps(response, sort_keys=True))


if __name__ == "__main__":
    main()
