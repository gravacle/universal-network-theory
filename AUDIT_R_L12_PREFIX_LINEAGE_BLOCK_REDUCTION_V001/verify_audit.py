#!/usr/bin/env python3
"""Hash-pinned post-output adjudicator for the L12 representation gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEV = ROOT / "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001"
AUDIT = ROOT / "AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001"
TARGET = DEV / "PREFLIGHT_RESULT.json"
HOSTILE = AUDIT / "HOSTILE_RESULT.json"
EXPECTED_TARGET_HASH = "dfca001f201dc1d7827dcf5cfa8d128d4e7024acb77c6dba890d3620652bced8"
EXPECTED_HOSTILE_HASH = "bbcb2d76e470e892979519b9eec9756ee28255a748eaccad9c0502d38540e53d"
EXPECTED_CENSUS = {
    "full_terminal_dimension": 1_251_677_700,
    "largest_materialized_dimension": 417_225_900,
    "maximum_adjacent_live_entries": 548_354_040,
    "maximum_adjacent_complex128_bytes": 8_773_664_640,
    "one_resolution_routed_entries": 2_453_288_291,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks = []

    def check(condition: bool, label: str):
        checks.append((bool(condition), label))

    manifest1 = json.loads((DEV / "FROZEN_MANIFEST.json").read_text())
    manifest2 = json.loads((DEV / "FROZEN_MANIFEST_V002.json").read_text())
    target = json.loads(TARGET.read_text())
    hostile = json.loads(HOSTILE.read_text())

    check(manifest1["frozen_before_output"] is True, "V001 declared pre-output")
    check(manifest2["frozen_before_output"] is True, "V002 declared pre-output")
    check(manifest2["prior_result_created"] is False, "V001 failed before result")
    check(manifest2["change"] == "PYTHON39_POPCOUNT_COMPATIBILITY_ONLY", "V002 change bounded")
    check(manifest2["prior_failed_freeze"] == "FROZEN_MANIFEST.json", "V001 custody retained")
    for relative, expected in manifest2["files"].items():
        check(digest(ROOT / relative) == expected, f"V002 frozen hash {relative}")
    v1_target = "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/verify_prefix_reduction.py"
    for relative, expected in manifest1["files"].items():
        if relative == v1_target:
            check(expected == "a00ed04d85c6d26c09e26564a13af837cf642f5f070e4fa2fc7553fcc2b1b9ba",
                  "V001 failed implementation hash retained")
            check(digest(ROOT / relative) != expected, "V001 implementation superseded")
        else:
            check(digest(ROOT / relative) == expected, f"unchanged V001 hash {relative}")

    check(digest(TARGET) == EXPECTED_TARGET_HASH, "target result hash")
    check(digest(HOSTILE) == EXPECTED_HOSTILE_HASH, "hostile result hash")
    check(hostile["target_result_sha256"] == EXPECTED_TARGET_HASH, "hostile pins target result")
    check(target["classification"] ==
          "PASS_EXACT_PREFIX_LINEAGE_REPRESENTATION__L12_HISTORY_NOT_AUTHORIZED",
          "target bounded classification")
    check(hostile["classification"] ==
          "PASS_HOSTILE_EXACT_PREFIX_LINEAGE_REPRESENTATION__L12_HISTORY_NOT_AUTHORIZED",
          "hostile bounded classification")
    check(target["checks_passed"] == target["checks_total"] == 119_429,
          "target 119429/119429")
    check(hostile["checks_passed"] == hostile["checks_total"] == 110_624,
          "hostile 110624/110624")
    check(not target["failures"] and not hostile["failures"], "empty failure lists")
    check(target["dimensions"] == hostile["dimensions"], "dimension tables agree")
    check(target["L12_census"] == EXPECTED_CENSUS, "target exact L12 census")
    check(hostile["L12_census"] == EXPECTED_CENSUS, "hostile exact L12 census")
    check(target["lineage"]["canonical_encodings"] == 4096, "target lineage census")
    check(target["lineage"]["observed_distinct_sha256_digests"] == 4096,
          "target digest census")
    check(hostile["canonical_lineages"] == hostile["observed_distinct_digests"] == 4096,
          "hostile lineage/digest census")
    check(target["lineage"]["authoritative_key"] == "FULL_MASK__DIGEST_IS_CUSTODY_ONLY",
          "hash not quotient key")
    check(target["terminal_control"]["amplitude_linf"] <= 2e-12 and
          target["terminal_control"]["registered_observable_linf"] <= 2e-12,
          "target terminal reconstruction")
    check(hostile["terminal_control"]["amplitude_linf"] <= 2e-12 and
          hostile["terminal_control"]["registered_observable_linf"] <= 2e-12,
          "hostile terminal reconstruction")
    check(target["resource"]["scratch_gate_pass"] is True, "new scratch gate")
    check(target["resource"]["projected_L12_target_seconds"] < 21_600 and
          target["resource"]["projected_L12_hostile_seconds"] < 21_600,
          "planning projections under guard")
    check("L10_REDUCED_BENCHMARK_REQUIRED" in target["resource"]["projection_status"],
          "projection cannot authorize L12")

    prohibited_outputs = (
        DEV / "RAW_HISTORY" / "PREFIX_HISTORY_L12.json",
        AUDIT / "RAW_HISTORY" / "BLIND_PREFIX_HISTORY_L12.json",
        DEV / "SPECTRUM_L12.json",
        AUDIT / "SPECTRUM_L12.json",
    )
    check(not any(path.exists() for path in prohibited_outputs), "no L12 history or spectrum output")
    packet_text = "\n".join((DEV / name).read_text() for name in ("PROTOCOL.md", "THEOREM.md"))
    check("AUTONOMOUS_CONNECTED_L12" not in packet_text, "no prior orbit quotient imported")
    check("No state, branch, lineage mask, or amplitude is\nidentified" in packet_text,
          "explicit no-lineage-identification boundary")

    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "FINAL_AUDIT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001",
        "classification": ("PASS_HOSTILE_SCREEN__EXACT_L12_REPRESENTATION_ONLY__L12_HISTORY_AWAITS_BENCHMARK"
                           if not failures else "FAIL_L12_PREFIX_LINEAGE_REPRESENTATION_GATE"),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "target_result_sha256": EXPECTED_TARGET_HASH,
        "hostile_result_sha256": EXPECTED_HOSTILE_HASH,
        "claim_boundary": "REPRESENTATION_GATE_ONLY__NO_L12_HISTORY_SPECTRUM_Z1_CONTINUUM_EMERGENCE_OR_GRAVITY",
    }
    output = AUDIT / "FINAL_AUDIT_RESULT.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
