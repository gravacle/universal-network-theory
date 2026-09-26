#!/usr/bin/env python3
"""Fail-closed validator for the L10/L12 recognition packet."""

from __future__ import annotations

import re
from pathlib import Path

import recognize_heldout_witness as recognition


EXPECTED_MANIFEST_FILES = {
    "CUSTODY_TIMING_OBSERVATION_V001.json",
    "README.md",
    "RECOGNITION_RESULT_V001.json",
    "RESULT.md",
    "recognize_heldout_witness.py",
    "test_recognition.py",
    "validate_recognition.py",
}
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  ([A-Za-z0-9_.-]+)$")
passed = 0


def check(condition: bool, label: str) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


def validate_manifest() -> None:
    manifest = recognition.PACKET / "MANIFEST.sha256"
    check(manifest.is_file() and not manifest.is_symlink(), "manifest is a regular file")
    entries: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        match = MANIFEST_LINE.fullmatch(line)
        check(match is not None, "manifest line syntax")
        assert match is not None
        digest, name = match.groups()
        check(name not in entries, f"manifest entry {name} is unique")
        path = recognition.PACKET / name
        check(path.is_file() and not path.is_symlink(), f"manifest target {name}")
        check(recognition.sha256_file(path) == digest, f"manifest hash {name}")
        entries[name] = digest
    check(set(entries) == EXPECTED_MANIFEST_FILES, "manifest entry set")


def main() -> int:
    validate_manifest()
    result = recognition.validate_expected()
    check(result["schema"] == recognition.SCHEMA, "recognition schema")
    check(result["computational_evidence"]["recognized"] is True, "evidence recognized")
    check(
        result["computational_evidence"]["status"]
        == "VALID_INDEPENDENTLY_REPRODUCED_FINITE_L10_L12_ASSOCIATION",
        "evidence status",
    )
    check(result["strict_protocol"]["formal_pass_claimed"] is False, "strict pass not claimed")
    check(
        result["strict_protocol"]["release_skew_deviation_disclosed"] is True,
        "timing deviation disclosed",
    )
    check(result["secondary_signed_persistence"]["pass"] is False, "persistence failure recorded")
    check(tuple(row["length"] for row in result["sizes"]) == (10, 12), "size sequence")
    check(all(row["T_L"] > 1.0 for row in result["sizes"]), "two-sided resolution")
    check(all(all(row["conditions"].values()) for row in result["sizes"]), "numerical controls")
    check(all(row["D_L_target"] < 0.0 for row in result["sizes"]), "target sign reversal")
    check(all(row["D_L_hostile"] < 0.0 for row in result["sizes"]), "hostile sign reversal")
    check(all(not row["persistence_pass"] for row in result["sizes"]), "floor failure")
    check(
        result["timing_custody"]["release_observation"]
        == {
            "deviation_seconds": 10688,
            "frozen_maximum_seconds": 60,
            "observed_gap_seconds": 10748,
            "within_frozen_maximum": False,
        },
        "timing arithmetic",
    )
    check(
        "OPERATIONAL_NOT_SCIENTIFIC"
        in result["policy_adjudication"]["release_skew_rule_role"],
        "policy classification",
    )
    check(
        result["computational_evidence"]
        ["deterministic_numerical_validity_affected_by_timing_gap"]
        is False,
        "timing does not alter arithmetic",
    )
    for marker in ("NO_FORMAL_STRICT_PROTOCOL_PASS_CLAIM", "NO_ALL_L", "RGRL", "ALPHA", "GRAVITY"):
        check(marker in result["claim_boundary"], f"claim boundary {marker}")
    print(f"PASS: {passed} recognition checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
