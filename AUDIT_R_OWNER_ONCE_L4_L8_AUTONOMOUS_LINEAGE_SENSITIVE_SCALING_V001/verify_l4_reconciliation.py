#!/usr/bin/env python3
"""Read-only verifier for the sealed hostile result and L4 reconciliation."""

from __future__ import annotations

import json
from pathlib import Path

import independent_scaling_audit as audit_tools
import reconcile_l4


def parse_hash_manifest(path: Path) -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    seen: set[str] = set()
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        if relative in seen or not audit_tools.HASH_PATTERN.fullmatch(digest):
            raise reconcile_l4.ReconciliationFailure(f"invalid manifest entry: {line}")
        seen.add(relative)
        entries.append((digest, reconcile_l4.ROOT / relative))
    return entries


def verify_manifest(path: Path) -> dict[str, str]:
    observed: dict[str, str] = {}
    for expected, target in parse_hash_manifest(path):
        actual = audit_tools.sha256_file(target)
        if actual != expected:
            raise reconcile_l4.ReconciliationFailure(
                f"manifest mismatch for {target}: {actual} != {expected}"
            )
        observed[target.relative_to(reconcile_l4.ROOT).as_posix()] = actual
    return observed


def verify() -> dict[str, object]:
    audit_tools.verify_freeze(reconcile_l4.ROOT)
    hostile_manifest = verify_manifest(reconcile_l4.HERE / "L4_RESULT_HASHES.sha256")
    source_manifest = verify_manifest(reconcile_l4.SOURCE_MANIFEST)
    output_manifest = verify_manifest(reconcile_l4.OUTPUT_MANIFEST)
    target = reconcile_l4.load_exact(reconcile_l4.TARGET_RESULT, reconcile_l4.TARGET_SHA256)
    hostile = reconcile_l4.load_exact(reconcile_l4.HOSTILE_RESULT, reconcile_l4.HOSTILE_SHA256)
    seal = reconcile_l4.load_exact(reconcile_l4.HOSTILE_SEAL, reconcile_l4.HOSTILE_SEAL_SHA256)
    if seal.get("target_output_read_before_seal") is not False:
        raise reconcile_l4.ReconciliationFailure("hostile seal is not blind")
    expected = reconcile_l4.build_reconciliation(target, hostile)
    rendered = audit_tools.canonical_json_bytes(expected)
    actual = reconcile_l4.OUTPUT.read_bytes()
    if actual != rendered:
        raise reconcile_l4.ReconciliationFailure("reconciliation bytes do not reproduce")
    stored = audit_tools.strict_json_bytes(actual, str(reconcile_l4.OUTPUT))
    if stored.get("passed") is not True or stored.get("all_registered_common_fields_pass") is not True:
        raise reconcile_l4.ReconciliationFailure("stored reconciliation is not a pass")
    if stored.get("maximum_registered_tolerance_fraction", 2.0) > 1.0:
        raise reconcile_l4.ReconciliationFailure("stored numerical gate exceeds tolerance")
    if not all(item.get("passed") is True for item in stored["registered_comparisons"]):
        raise reconcile_l4.ReconciliationFailure("a stored registered comparison failed")
    report = reconcile_l4.report_markdown(stored).encode()
    if reconcile_l4.REPORT.read_bytes() != report:
        raise reconcile_l4.ReconciliationFailure("reconciliation report does not reproduce")
    return {
        "schema": "L4_TARGET_HOSTILE_RECONCILIATION_VERIFICATION_V001",
        "status": "PASS_L4_TARGET_HOSTILE_RECONCILIATION_VERIFICATION",
        "hostile_result_sha256": reconcile_l4.HOSTILE_SHA256,
        "hostile_result_seal_sha256": reconcile_l4.HOSTILE_SEAL_SHA256,
        "target_result_sha256": reconcile_l4.TARGET_SHA256,
        "reconciliation_sha256": audit_tools.sha256_file(reconcile_l4.OUTPUT),
        "maximum_registered_absolute_difference": stored[
            "maximum_registered_absolute_difference"
        ],
        "maximum_non_T_dyn_absolute_difference": stored[
            "maximum_non_T_dyn_absolute_difference"
        ],
        "maximum_registered_tolerance_fraction": stored[
            "maximum_registered_tolerance_fraction"
        ],
        "tolerance": stored["tolerance"],
        "hostile_manifest_entries": len(hostile_manifest),
        "source_manifest_entries": len(source_manifest),
        "output_manifest_entries": len(output_manifest),
        "L6_executed": False,
        "L8_executed": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
