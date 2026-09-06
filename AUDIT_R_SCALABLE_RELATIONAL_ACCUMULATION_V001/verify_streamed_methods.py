#!/usr/bin/env python3
"""Pre-output validation and resource projection for streamed L10 methods."""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
OUT = HERE / "STREAMED_METHOD_PREFLIGHT_RESULT.json"
LENGTHS = (4, 6, 8)
FIELDS = (
    "W_n",
    "allow_probability",
    "blocked_probability",
    "connector_delta_l1",
    "connector_delta_signed",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[dict[str, object]] = []


def check(condition: bool, label: str, detail: object = None) -> None:
    checks.append({"passed": bool(condition), "label": label, "detail": detail})


maximum_target_blind = 0.0
maximum_target_seed = 0.0
target_l8_wall = blind_l8_wall = 0.0
target_l8_rss = blind_l8_rss = 0
for length in LENGTHS:
    target = json.loads((TARGET / "METHOD_VALIDATION" / f"STREAMED_HISTORY_L{length}.json").read_text())
    blind = json.loads((HERE / "METHOD_VALIDATION" / f"BLIND_STREAMED_HISTORY_L{length}.json").read_text())
    seed = json.loads((TARGET / "RAW_HISTORY" / f"HISTORY_L{length}.json").read_text())
    exact_dimension = math.comb(3 * length, length)
    check(target["dimension"] == exact_dimension, f"target exact dimension L{length}")
    check(blind["dimension"] == exact_dimension, f"blind exact dimension L{length}")
    check(target["comparison"]["resolved"], f"target resolved L{length}")
    check(blind["comparison"]["resolved"], f"blind resolved L{length}")
    check(
        target["comparison"]["sector"]["density_interval"]
        == blind["comparison"]["sector"]["density_interval"]
        == seed["comparison"]["sector"]["density_interval"],
        f"sector identity L{length}",
    )
    for target_row, blind_row, seed_row in zip(target["rows"], blind["rows"], seed["rows"]):
        for field in FIELDS:
            maximum_target_blind = max(
                maximum_target_blind, abs(float(target_row[field]) - float(blind_row[field]))
            )
            maximum_target_seed = max(
                maximum_target_seed, abs(float(target_row[field]) - float(seed_row[field]))
            )
        maximum_target_blind = max(
            maximum_target_blind,
            max(
                abs(float(a) - float(b))
                for a, b in zip(target_row["sector_weights"], blind_row["sector_weights"])
            ),
        )
        maximum_target_seed = max(
            maximum_target_seed,
            max(
                abs(float(a) - float(b))
                for a, b in zip(target_row["sector_weights"], seed_row["sector_weights"])
            ),
        )
    if length == 8:
        target_l8_wall = float(target["wall_seconds"])
        blind_l8_wall = float(blind["wall_seconds"])
        target_l8_rss = int(target["peak_rss_bytes"])
        blind_l8_rss = int(blind["peak_rss_bytes"])

check(maximum_target_blind <= 1.0e-8, "target/blind validation agreement", maximum_target_blind)
check(maximum_target_seed <= 2.0e-8, "streamed/sealed seed agreement", maximum_target_seed)

benchmark = json.loads((TARGET / "BLOCK_KERNEL_BENCHMARK.json").read_text())
bench_by_l = {int(row["L"]): row for row in benchmark["sizes"]}
h_ratio = (
    float(bench_by_l[10]["projected_full_state_h_action_seconds"])
    / float(bench_by_l[8]["projected_full_state_h_action_seconds"])
)
dimension_ratio = math.comb(30, 10) / math.comb(24, 8)
projection_ratio = max(h_ratio, dimension_ratio)
safety_factor = 2.0
target_projection = target_l8_wall * projection_ratio * safety_factor
blind_projection = blind_l8_wall * projection_ratio * safety_factor
state_bytes_l10 = math.comb(30, 10) * 16
projected_target_rss = 2 * state_bytes_l10 + 1_400_000_000 + state_bytes_l10 // 4
projected_blind_rss = projected_target_rss
check(target_projection <= 7200.0, "target L10 projected below two-hour guard", target_projection)
check(blind_projection <= 7200.0, "blind L10 projected below two-hour guard", blind_projection)
check(projected_target_rss <= 4 * 2**30, "target L10 projected below RSS guard", projected_target_rss)
check(projected_blind_rss <= 4 * 2**30, "blind L10 projected below RSS guard", projected_blind_rss)

free_scratch = shutil.disk_usage(ROOT).free
l12_required = 60 * 2**30
check(free_scratch < l12_required, "L12 scratch guard currently blocks execution", free_scratch)

method_files = {
    "target": TARGET / "compute_streamed_history.py",
    "blind": HERE / "blind_streamed_history.py",
    "benchmark": TARGET / "benchmark_block_kernel.py",
    "protocol": TARGET / "PROTOCOL.md",
    "method_note": TARGET / "STREAMED_METHOD_FREEZE.md",
    "adjudicator": HERE / "compare_L10_history.py",
}
failures = [row for row in checks if not row["passed"]]
result = {
    "schema": "SCALABLE_RELATIONAL_STREAMED_METHOD_PREFLIGHT_V001",
    "verdict": "PASS_L10_METHOD_FREEZE__L12_RESOURCE_BLOCKED" if not failures else "FAIL_CLOSED_METHOD_PREFLIGHT",
    "checks_passed": len(checks) - len(failures),
    "checks_total": len(checks),
    "failures": failures,
    "maximum_target_blind_validation_difference": maximum_target_blind,
    "maximum_streamed_seed_difference": maximum_target_seed,
    "benchmark_h_action_ratio_L10_over_L8": h_ratio,
    "dimension_ratio_L10_over_L8": dimension_ratio,
    "projection_safety_factor": safety_factor,
    "target_L10_projected_wall_seconds": target_projection,
    "blind_L10_projected_wall_seconds": blind_projection,
    "target_L10_projected_peak_rss_bytes": projected_target_rss,
    "blind_L10_projected_peak_rss_bytes": projected_blind_rss,
    "observed_target_L8_wall_seconds": target_l8_wall,
    "observed_blind_L8_wall_seconds": blind_l8_wall,
    "observed_target_L8_peak_rss_bytes": target_l8_rss,
    "observed_blind_L8_peak_rss_bytes": blind_l8_rss,
    "L12_free_scratch_bytes": free_scratch,
    "L12_required_free_scratch_bytes": l12_required,
    "L12_execution_authorized": False,
    "method_hashes": {name: sha256(path) for name, path in method_files.items()},
    "claim_boundary": "METHOD_AND_RESOURCE_PREFLIGHT_ONLY__NO_L10_OR_L12_HISTORY_OUTPUT",
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(result["verdict"])
print(f"checks {result['checks_passed']}/{result['checks_total']}")
print(f"target/blind {maximum_target_blind:.3e}; streamed/seed {maximum_target_seed:.3e}")
print(f"L10 projected target={target_projection:.1f}s blind={blind_projection:.1f}s")
print(f"L12 scratch free={free_scratch} required={l12_required}")
if failures:
    for failure in failures:
        print("FAIL", failure["label"], failure["detail"])
    raise SystemExit(1)
