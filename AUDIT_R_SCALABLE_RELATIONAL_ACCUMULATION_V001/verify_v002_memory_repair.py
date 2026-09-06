#!/usr/bin/env python3
"""Frozen preflight and adjudication for the L10 target V002 memory repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
WRAPPER = TARGET / "compute_streamed_history_v002.py"
BASE = TARGET / "compute_streamed_history.py"
NOTE = TARGET / "V002_MEMORY_REPAIR.md"
BLIND = HERE / "RAW_HISTORY" / "BLIND_STREAMED_HISTORY_L10.json"
VALIDATION = TARGET / "METHOD_VALIDATION" / "STREAMED_HISTORY_L8_V002_FREEZE.json"
REFERENCE = TARGET / "METHOD_VALIDATION" / "STREAMED_HISTORY_L8.json"
PREFLIGHT = HERE / "V002_MEMORY_REPAIR_PREFLIGHT.json"
TARGET_L10 = TARGET / "RAW_HISTORY" / "STREAMED_HISTORY_L10_V002.json"
RESULT = HERE / "L10_V002_HOSTILE_RESULT.json"
FIELDS = (
    "W_n",
    "allow_probability",
    "blocked_probability",
    "connector_delta_l1",
    "connector_delta_signed",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(left: dict[str, object], right: dict[str, object]) -> tuple[float, float]:
    observable = 0.0
    sector = 0.0
    for a, b in zip(left["rows"], right["rows"]):
        for field in FIELDS:
            observable = max(observable, abs(float(a[field]) - float(b[field])))
        sector = max(
            sector,
            max(abs(float(x) - float(y)) for x, y in zip(a["sector_weights"], b["sector_weights"])),
        )
    return observable, sector


def preflight() -> None:
    frozen_v1 = json.loads((HERE / "STREAMED_METHOD_PREFLIGHT_RESULT.json").read_text())
    validation = json.loads(VALIDATION.read_text())
    reference = json.loads(REFERENCE.read_text())
    blind = json.loads(BLIND.read_text())
    checks: list[dict[str, object]] = []

    def check(condition: bool, label: str, detail: object = None) -> None:
        checks.append({"passed": bool(condition), "label": label, "detail": detail})

    observable, sector = differences(validation, reference)
    check(sha256(BASE) == frozen_v1["method_hashes"]["target"], "V001 base hash")
    check(validation["schema"] == "SCALABLE_RELATIONAL_STREAMED_HISTORY_ROW_V002", "V002 validation schema")
    check(validation["L"] == 8 and validation["dimension"] == math.comb(24, 8), "L8 exact validation basis")
    check(validation["events"] == 8 and len(validation["rows"]) == 8, "complete L8 validation events")
    check(reference["events"] == 8 and len(reference["rows"]) == 8, "complete L8 reference events")
    check([row["event"] for row in validation["rows"]] == list(range(1, 9)), "L8 validation event identity")
    check(validation["comparison"]["resolved"], "L8 V002 internally resolved")
    check(observable <= 1.0e-10, "L8 V002/V001 observable agreement", observable)
    check(sector <= 1.0e-10, "L8 V002/V001 sector agreement", sector)
    repair = validation["memory_only_repair"]
    check(repair["original_krylov_batch_bytes"] == 1_400_000_000, "original batch bytes")
    check(repair["repaired_krylov_batch_bytes"] == 1_000_000_000, "repaired batch bytes")
    for field in (
        "physical_operator_changed",
        "basis_or_branch_changed",
        "numerical_threshold_changed",
        "resource_limit_changed",
    ):
        check(repair[field] is False, f"repair invariant {field}")
    check(blind["comparison"]["resolved"], "frozen blind L10 resolved")
    check(blind["resource_guards"]["rss_pass"] and blind["resource_guards"]["wall_pass"], "frozen blind resources")
    check(not TARGET_L10.exists(), "no V002 L10 output before freeze")
    files = {
        "wrapper": WRAPPER,
        "base": BASE,
        "repair_note": NOTE,
        "blind_L10": BLIND,
        "adjudicator": Path(__file__),
        "validation_L8_V002": VALIDATION,
    }
    failures = [row for row in checks if not row["passed"]]
    result = {
        "schema": "L10_V002_MEMORY_REPAIR_PREFLIGHT_V001",
        "verdict": "PASS_FREEZE_L10_V002_MEMORY_REPAIR" if not failures else "FAIL_CLOSED_V002_PREFLIGHT",
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "maximum_L8_V002_V001_observable_difference": observable,
        "maximum_L8_V002_V001_sector_difference": sector,
        "hashes": {name: sha256(path) for name, path in files.items()},
        "claim_boundary": "MEMORY_ONLY_METHOD_REPAIR__NO_L10_V002_OUTPUT",
    }
    PREFLIGHT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["verdict"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print(f"L8 observable={observable:.3e} sector={sector:.3e}")
    if failures:
        for failure in failures:
            print("FAIL", failure["label"], failure["detail"])
        raise SystemExit(1)


def adjudicate() -> None:
    frozen = json.loads(PREFLIGHT.read_text())
    target = json.loads(TARGET_L10.read_text())
    blind = json.loads(BLIND.read_text())
    checks: list[dict[str, object]] = []

    def check(condition: bool, label: str, detail: object = None) -> None:
        checks.append({"passed": bool(condition), "label": label, "detail": detail})

    current_hashes = {
        "wrapper": sha256(WRAPPER),
        "base": sha256(BASE),
        "repair_note": sha256(NOTE),
        "blind_L10": sha256(BLIND),
        "adjudicator": sha256(Path(__file__)),
        "validation_L8_V002": sha256(VALIDATION),
    }
    check(frozen["verdict"] == "PASS_FREEZE_L10_V002_MEMORY_REPAIR", "V002 preflight pass")
    for name, expected in frozen["hashes"].items():
        check(current_hashes[name] == expected, f"frozen hash {name}")
    check(target["schema"] == "SCALABLE_RELATIONAL_STREAMED_HISTORY_ROW_V002", "target V002 schema")
    check(target["L"] == blind["L"] == 10, "L10 identity")
    check(target["dimension"] == blind["dimension"] == math.comb(30, 10), "exact L10 dimension")
    check(target["events"] == blind["events"] == 10, "ten declared L10 events")
    check(len(target["rows"]) == len(blind["rows"]) == 10, "ten retained L10 rows")
    check([row["event"] for row in target["rows"]] == list(range(1, 11)), "target event identity")
    check([row["event"] for row in blind["rows"]] == list(range(1, 11)), "blind event identity")
    check(target["comparison"]["resolved"], "target V002 internally resolved")
    check(blind["comparison"]["resolved"], "blind internally resolved")
    check(float(target["wall_seconds"]) <= 7200.0, "target wall guard", target["wall_seconds"])
    check(int(target["peak_rss_bytes"]) <= 4 * 2**30, "target RSS guard", target["peak_rss_bytes"])
    check(float(blind["wall_seconds"]) <= 7200.0, "blind wall guard", blind["wall_seconds"])
    check(int(blind["peak_rss_bytes"]) <= 4 * 2**30, "blind RSS guard", blind["peak_rss_bytes"])
    repair = target["memory_only_repair"]
    check(repair["original_krylov_batch_bytes"] == 1_400_000_000, "target original batch bytes")
    check(repair["repaired_krylov_batch_bytes"] == 1_000_000_000, "target repaired batch bytes")
    check(not any(repair[field] for field in (
        "physical_operator_changed",
        "basis_or_branch_changed",
        "numerical_threshold_changed",
        "resource_limit_changed",
    )), "repair changes no scientific control")
    check(target["implementation_sha256"] == frozen["hashes"]["wrapper"], "target wrapper custody")
    check(repair["wrapper_implementation_sha256"] == frozen["hashes"]["wrapper"], "embedded wrapper custody")
    check(repair["base_implementation_sha256"] == frozen["hashes"]["base"], "embedded base custody")
    frozen_v1 = json.loads((HERE / "STREAMED_METHOD_PREFLIGHT_RESULT.json").read_text())
    protocol_hash = frozen_v1["method_hashes"]["protocol"]
    check(target["protocol_sha256"] == protocol_hash, "target protocol custody")
    check(blind["protocol_sha256"] == protocol_hash, "blind protocol custody")

    observable, sector = differences(target, blind)
    check(observable <= 1.0e-8, "target/blind observable agreement", observable)
    check(sector <= 1.0e-8, "target/blind sector agreement", sector)
    total_disagreement = max(
        observable,
        sector,
        float(target["comparison"]["coarse_fine"]["maximum_disagreement"]),
        float(blind["comparison"]["coarse_fine"]["maximum_disagreement"]),
    )
    epsilon = max(1.0e-11, 50.0 * total_disagreement)
    admission = node = number = norm = reverse = blocked_null = 0.0
    minimum_write = math.inf
    maximum_blocked = 0.0
    for result in (target, blind):
        for row in result["rows"]:
            admission = max(admission, *(abs(float(row[field])) for field in (
                "admission_total_content_residual",
                "admission_bandwidth_residual",
                "target_owner_residual",
            )))
            node = max(node, abs(float(row["transport_node_residual_l1"])))
            number = max(number, abs(float(row["transport_number_drift"])))
            norm = max(norm, abs(float(row["actual_norm_error"])), abs(float(row["null_norm_error"])))
            reverse = max(reverse, abs(float(row["reverse_support_probability"])))
            blocked_null = max(blocked_null, abs(float(row["blocked_null_state_error"])))
            minimum_write = min(minimum_write, float(row["W_n"]))
            maximum_blocked = max(maximum_blocked, float(row["blocked_probability"]))
    check(admission <= 1.0e-10, "strict admission accounting", admission)
    check(number <= 1.0e-10, "strict transport number", number)
    check(node <= max(1.0e-9, 100.0 * epsilon), "node continuity", node)
    check(norm <= 1.0e-10, "norm guards", norm)
    check(reverse <= 1.0e-11, "fresh reverse support", reverse)
    check(blocked_null <= 1.0e-11, "blocked-null records", blocked_null)
    check(minimum_write >= -epsilon, "nonnegative writes", minimum_write)
    check(maximum_blocked > 1.0e-6, "nonvacuous blocking", maximum_blocked)
    t_sector = target["comparison"]["sector"]
    b_sector = blind["comparison"]["sector"]
    check(t_sector["q_lower"] == b_sector["q_lower"], "q lower identity")
    check(t_sector["q_upper"] == b_sector["q_upper"], "q upper identity")
    check(t_sector["density_interval"] == b_sector["density_interval"], "density interval identity")
    seed = json.loads((TARGET / "SEED_RESULT.json").read_text())
    lower = max(float(seed["common_density_interval"][0]), float(t_sector["density_interval"][0]))
    upper = min(float(seed["common_density_interval"][1]), float(t_sector["density_interval"][1]))
    check(upper > lower, "positive L4-L10 common support", [lower, upper])

    failures = [row for row in checks if not row["passed"]]
    scratch_free = shutil.disk_usage(ROOT).free
    scratch_required = 60 * 2**30
    l10_pass = not failures
    l12_method_gate = l10_pass and scratch_free >= scratch_required
    classification = (
        "PASS_RELATIONAL_ACCUMULATION_L4_L10__AUTHORIZE_L12_METHOD_GATE"
        if l12_method_gate
        else "PASS_RELATIONAL_ACCUMULATION_L4_L10__L12_RESOURCE_BLOCKED"
    ) if l10_pass else "FAIL_CLOSED_L10_V002_MEMORY_REPAIR"
    result = {
        "schema": "L10_V002_MEMORY_REPAIR_HOSTILE_RESULT_V001",
        "classification": classification,
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "maximum_target_blind_observable_difference": observable,
        "maximum_target_blind_sector_difference": sector,
        "epsilon": epsilon,
        "maximum_admission_accounting_residual": admission,
        "maximum_transport_node_residual_l1": node,
        "maximum_transport_number_drift": number,
        "maximum_norm_error": norm,
        "minimum_write": minimum_write,
        "maximum_blocked_probability": maximum_blocked,
        "L10_sector": t_sector,
        "common_density_interval_L4_L10": [lower, upper],
        "target_wall_seconds": target["wall_seconds"],
        "target_peak_rss_bytes": target["peak_rss_bytes"],
        "blind_wall_seconds": blind["wall_seconds"],
        "blind_peak_rss_bytes": blind["peak_rss_bytes"],
        "L12_free_scratch_bytes": scratch_free,
        "L12_required_free_scratch_bytes": scratch_required,
        "L12_method_gate_authorized": l12_method_gate,
        "target_sha256": sha256(TARGET_L10),
        "blind_sha256": sha256(BLIND),
        "frozen_hashes": current_hashes,
        "claim_boundary": {
            "empirical": "FINITE_L4_L10_RELATIONAL_HISTORY_ONLY",
            "open": ["L12_HISTORY", "INTERVAL_SPECTRA", "Z1", "CRITICALITY", "CONTINUUM", "EMERGENCE", "GRAVITY"],
        },
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(classification)
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    print(f"observable={observable:.3e} sector={sector:.3e}")
    print(f"target wall={target['wall_seconds']:.3f}s rss={target['peak_rss_bytes']}")
    print(f"common={[lower, upper]} L12_method_gate={l12_method_gate}")
    if failures:
        for failure in failures:
            print("FAIL", failure["label"], failure["detail"])
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preflight", "adjudicate"))
    args = parser.parse_args()
    preflight() if args.mode == "preflight" else adjudicate()


if __name__ == "__main__":
    main()
