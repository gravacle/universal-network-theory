#!/usr/bin/env python3
"""Read-only seal and arithmetic verifier for the V001 reconstruction report."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPORT = HERE / "LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json"
REPORT_SHA256 = "182a78f3ef11c72d5089a488e85cb9f91e842f1950d3d5a474f7678bfd23ca08"
TOLERANCE = 1.0e-12
PRIOR = {
    ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json":
        "43c7c19daaf24902d2699c337851eca35a03c3db69f8e3f55f3b0142f87e137d",
    ROOT / "DEVELOPMENT_R_L12_STAGE6R3_RECORD_FLOW_ADJUDICATION_V001"
    / "STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json":
        "7fa2062f18be3c90c9167e917974d1cc609273da623966e4068f1c0d1133e2b4",
    ROOT / "DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001"
    / "RECORD_FLOW_BRIDGE_REPORT_V001.json":
        "4a02db3eaea066a4c65bce921fcfaaffcc7e731b057d06f4c50180b6e38b40a6",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(16 * 2**20), b""):
            value.update(block)
    return value.hexdigest()


def close(left: float, right: float) -> bool:
    return math.isfinite(left) and math.isfinite(right) and abs(left - right) <= TOLERANCE


def main() -> int:
    assert digest(REPORT) == REPORT_SHA256
    for path, expected in PRIOR.items():
        assert digest(path) == expected, path
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["schema"] == "L12_LINEAGE_RESOLVED_SUPPORT_RECONSTRUCTION_V001"
    assert report["classification"] == "LINEAGE_RESOLVED_Q5_SUPPORT_BELOW_REQUIRED_THRESHOLD"
    assert report["prior_artifacts_mutated"] is False
    assert report["stage7_started"] is False
    gate = report["threshold_adjudication"]
    assert close(gate["stage5_q4_mass"] + gate["stage5_q6_mass"]
                 + gate["required_q5_common_lineage_support"], 0.5)
    assert close(gate["conservative_support"], min(
        gate["target_strict_support"], gate["hostile_strict_support"]
    ))
    assert close(gate["shortfall"],
                 gate["required_q5_common_lineage_support"] - gate["conservative_support"])
    assert gate["threshold_cleared"] is False
    for name in ("target", "hostile"):
        branch = report[name]
        strict = branch["strict_common_lineage_support_by_event"]
        prewindow = branch["prewindow_entry_then_window_exit_by_event"]
        no_exit = branch["no_exit_by_event_12_by_event"]
        observed = branch["observed_q5_mass_by_event"]
        assert len(strict) == len(prewindow) == len(no_exit) == len(observed) == 7
        assert all(close(a + b + c, d) for a, b, c, d in zip(strict, prewindow, no_exit, observed))
        assert close(sum(strict) / 7, branch["strict_common_lineage_pbar_support"])
        assert close(sum(observed) / 7, branch["observed_q5_pbar"])
        assert branch["maximum_absolute_decomposition_residual"] <= TOLERANCE
        assert branch["maximum_absolute_terminal_residual"] <= TOLERANCE
    autopsy = report["original_stage6_conjunction_autopsy"]
    expected = {
        "A011": ["exponents_agree", "tail_scaled_chi_stable", "tail_scaled_gap_stable"],
        "A016": ["fixed_z1_beats_positive_gap", "fixed_z1_near_free_gapless"],
    }
    for atom, false_predicates in expected.items():
        assert autopsy[atom]["original_full_conjunction_passes"] is False
        assert autopsy[atom]["failure_domain"].endswith("NOT_A_MASS_PREDICATE")
        for branch in ("target", "blind"):
            assert autopsy[atom]["branches"][branch]["false_predicates"] == false_predicates
    print("VERIFIED: immutable report SHA-256 and all frozen arithmetic/audit predicates")
    print(f"REPORT_SHA256: {REPORT_SHA256}")
    print(f"CLASSIFICATION: {report['classification']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
