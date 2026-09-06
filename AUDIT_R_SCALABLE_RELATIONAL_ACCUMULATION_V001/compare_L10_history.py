#!/usr/bin/env python3
"""Frozen target/blind adjudication for the exact streamed L10 histories."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
TARGET_RESULT = TARGET / "RAW_HISTORY" / "STREAMED_HISTORY_L10.json"
BLIND_RESULT = HERE / "RAW_HISTORY" / "BLIND_STREAMED_HISTORY_L10.json"
OUT = HERE / "L10_STREAMED_HOSTILE_RESULT.json"
PREFLIGHT = HERE / "STREAMED_METHOD_PREFLIGHT_RESULT.json"
OBSERVABLE_FIELDS = (
    "W_n",
    "allow_probability",
    "blocked_probability",
    "connector_delta_l1",
    "connector_delta_signed",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> None:
    target = json.loads(TARGET_RESULT.read_text())
    blind = json.loads(BLIND_RESULT.read_text())
    frozen = json.loads(PREFLIGHT.read_text())
    checks: list[dict[str, object]] = []

    def check(condition: bool, label: str, detail: object = None) -> None:
        checks.append({"passed": bool(condition), "label": label, "detail": detail})

    current_hashes = {
        "target": sha256(TARGET / "compute_streamed_history.py"),
        "blind": sha256(HERE / "blind_streamed_history.py"),
        "benchmark": sha256(TARGET / "benchmark_block_kernel.py"),
        "protocol": sha256(TARGET / "PROTOCOL.md"),
        "method_note": sha256(TARGET / "STREAMED_METHOD_FREEZE.md"),
        "adjudicator": sha256(Path(__file__)),
    }
    for name, expected in frozen["method_hashes"].items():
        check(current_hashes[name] == expected, f"frozen method hash {name}")
    check(frozen["verdict"] == "PASS_L10_METHOD_FREEZE__L12_RESOURCE_BLOCKED", "method preflight passed")
    check(target["L"] == blind["L"] == 10, "L10 identity")
    check(target["dimension"] == blind["dimension"] == math.comb(30, 10), "exact dimension")
    check(len(target["rows"]) == len(blind["rows"]) == 10, "ten cursor events")
    check(target["comparison"]["resolved"], "target internally resolved")
    check(blind["comparison"]["resolved"], "blind internally resolved")
    check(int(target["peak_rss_bytes"]) <= 4 * 2**30, "target RSS guard", target["peak_rss_bytes"])
    check(float(target["wall_seconds"]) <= 7200.0, "target wall guard", target["wall_seconds"])
    check(int(blind["peak_rss_bytes"]) <= 4 * 2**30, "blind RSS guard", blind["peak_rss_bytes"])
    check(float(blind["wall_seconds"]) <= 7200.0, "blind wall guard", blind["wall_seconds"])

    maximum_observable = 0.0
    maximum_sector = 0.0
    maximum_admission_accounting = 0.0
    maximum_transport_node_residual = 0.0
    maximum_transport_number_drift = 0.0
    maximum_norm = 0.0
    maximum_reverse = 0.0
    maximum_blocked_null = 0.0
    minimum_write = math.inf
    maximum_blocking = 0.0
    for target_row, blind_row in zip(target["rows"], blind["rows"]):
        for field in OBSERVABLE_FIELDS:
            maximum_observable = max(
                maximum_observable, abs(float(target_row[field]) - float(blind_row[field]))
            )
        maximum_sector = max(
            maximum_sector,
            max(
                abs(float(a) - float(b))
                for a, b in zip(target_row["sector_weights"], blind_row["sector_weights"])
            ),
        )
        for row in (target_row, blind_row):
            maximum_admission_accounting = max(
                maximum_admission_accounting,
                abs(float(row["admission_total_content_residual"])),
                abs(float(row["admission_bandwidth_residual"])),
                abs(float(row["target_owner_residual"])),
            )
            maximum_transport_node_residual = max(
                maximum_transport_node_residual,
                abs(float(row["transport_node_residual_l1"])),
            )
            maximum_transport_number_drift = max(
                maximum_transport_number_drift,
                abs(float(row["transport_number_drift"])),
            )
            maximum_norm = max(
                maximum_norm,
                abs(float(row["actual_norm_error"])),
                abs(float(row["null_norm_error"])),
            )
            maximum_reverse = max(maximum_reverse, abs(float(row["reverse_support_probability"])))
            maximum_blocked_null = max(maximum_blocked_null, abs(float(row["blocked_null_state_error"])))
            minimum_write = min(minimum_write, float(row["W_n"]))
            maximum_blocking = max(maximum_blocking, float(row["blocked_probability"]))
    total_disagreement = max(
        maximum_observable,
        maximum_sector,
        float(target["comparison"]["coarse_fine"]["maximum_disagreement"]),
        float(blind["comparison"]["coarse_fine"]["maximum_disagreement"]),
    )
    epsilon = max(1.0e-11, 50.0 * total_disagreement)
    check(maximum_observable <= 1.0e-8, "target/blind observable agreement", maximum_observable)
    check(maximum_sector <= 1.0e-8, "target/blind sector agreement", maximum_sector)
    check(
        maximum_admission_accounting <= 1.0e-10,
        "strict admission accounting guards",
        maximum_admission_accounting,
    )
    check(
        maximum_transport_number_drift <= 1.0e-10,
        "strict transport number guard",
        maximum_transport_number_drift,
    )
    check(
        maximum_transport_node_residual <= max(1.0e-9, 100.0 * epsilon),
        "transport node-ledger guard",
        maximum_transport_node_residual,
    )
    check(maximum_norm <= 1.0e-10, "all norm guards", maximum_norm)
    check(maximum_reverse <= 1.0e-11, "fresh-cell reverse support", maximum_reverse)
    check(maximum_blocked_null <= 1.0e-11, "blocked-null records", maximum_blocked_null)
    check(minimum_write >= -epsilon, "all writes nonnegative", minimum_write)
    check(maximum_blocking > 1.0e-6, "blocking dynamically nonzero", maximum_blocking)

    target_sector = target["comparison"]["sector"]
    blind_sector = blind["comparison"]["sector"]
    check(target_sector["q_lower"] == blind_sector["q_lower"], "q lower identity")
    check(target_sector["q_upper"] == blind_sector["q_upper"], "q upper identity")
    check(target_sector["density_interval"] == blind_sector["density_interval"], "density interval identity")
    seed = json.loads((TARGET / "SEED_RESULT.json").read_text())
    lower = max(float(seed["common_density_interval"][0]), float(target_sector["density_interval"][0]))
    upper = min(float(seed["common_density_interval"][1]), float(target_sector["density_interval"][1]))
    check(upper > lower, "positive-width L4-L10 common interval", [lower, upper])

    free_scratch = shutil.disk_usage(ROOT).free
    required_scratch = 60 * 2**30
    l12_authorized = free_scratch >= required_scratch
    classification = (
        "PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_METHOD_GATE"
        if l12_authorized
        else "PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_RESOURCE_BLOCKED"
    )
    failures = [row for row in checks if not row["passed"]]
    if failures:
        classification = "FAIL_CLOSED_L10_STREAMED_HISTORY"
    result = {
        "schema": "SCALABLE_RELATIONAL_L10_HOSTILE_RESULT_V001",
        "classification": classification,
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "maximum_target_blind_observable_difference": maximum_observable,
        "maximum_target_blind_sector_difference": maximum_sector,
        "maximum_admission_accounting_residual": maximum_admission_accounting,
        "maximum_transport_node_residual_l1": maximum_transport_node_residual,
        "maximum_transport_number_drift": maximum_transport_number_drift,
        "maximum_norm_error": maximum_norm,
        "minimum_write": minimum_write,
        "maximum_blocked_probability": maximum_blocking,
        "epsilon": epsilon,
        "L10_sector": target_sector,
        "common_density_interval_L4_L10": [lower, upper],
        "target_wall_seconds": target["wall_seconds"],
        "blind_wall_seconds": blind["wall_seconds"],
        "target_peak_rss_bytes": target["peak_rss_bytes"],
        "blind_peak_rss_bytes": blind["peak_rss_bytes"],
        "L12_free_scratch_bytes": free_scratch,
        "L12_required_free_scratch_bytes": required_scratch,
        "L12_execution_authorized": l12_authorized,
        "target_result_sha256": sha256(TARGET_RESULT),
        "blind_result_sha256": sha256(BLIND_RESULT),
        "method_hashes": current_hashes,
        "claim_boundary": {
            "empirical": "FINITE_L4_L10_RELATIONAL_HISTORY_ONLY",
            "open": [
                "L12_HISTORY",
                "L4_L12_COMMON_SECTOR",
                "INTERVAL_SPECTRA",
                "Z1",
                "CRITICALITY",
                "CONTINUUM",
                "EMERGENCE",
                "GRAVITY",
            ],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(classification)
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print(f"target/blind observable={maximum_observable:.3e} sector={maximum_sector:.3e}")
    print(f"L4-L10 interval={[lower, upper]}")
    print(f"L12 scratch free={free_scratch} required={required_scratch}")
    if failures:
        for failure in failures:
            print("FAIL", failure["label"], failure["detail"])
        raise SystemExit(1)


if __name__ == "__main__":
    run()
