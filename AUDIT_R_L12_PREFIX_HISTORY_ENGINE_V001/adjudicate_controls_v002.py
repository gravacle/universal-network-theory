#!/usr/bin/env python3
"""Cross-adjudicate the frozen target V003 and hostile V002 L=4--8 controls."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
TOLERANCE = 1.0e-8

TARGET_IMPLEMENTATION = "71458cd4b958d5b38cb24409ed769e790d9a83e1da8ac71fd2d3098fdb779694"
HOSTILE_IMPLEMENTATION = "e6b1be915a4d490939799e79efc017ab4e3808f1beeb3d984448b2508fb0522b"
TARGET_OUTPUTS = {
    4: "6c89ba97c389b6755b81fe305949d044ffecc4f7ebe4256fb305d0e608435759",
    6: "131524c51fe72e9506fe320f339c6b50068955d8c6bbd55e1d915c6c080d10b2",
    8: "2b492cd026c5d7592e4b125b69db4c1b5ed0c8bbd0052b11fb79c8d8d777f981",
}
HOSTILE_OUTPUTS = {
    4: "771fb104419a77e023e76c5636b2a7fb5a3ab4e9ea6eb73d3b6790ec29c7f643",
    6: "9c0c6aa806807b2f0927736058e1bcdd92d64c0e2cc06c3a7c227776d6e50435",
    8: "f0f8aba0e4c2288835a6dac1465bb1be94d29b0997c9ffdfae5eafa6a922dcde",
}
SCALARS = (
    "W_n",
    "allow_probability",
    "blocked_probability",
    "reverse_support_probability",
    "blocked_null_state_error",
    "connector_delta_l1",
    "connector_delta_signed",
    "admission_total_content_residual",
    "admission_bandwidth_residual",
    "target_owner_residual",
    "transport_node_residual_l1",
    "transport_node_residual_linf",
    "transport_number_drift",
    "actual_norm_error",
    "null_norm_error",
    "q_genesis_after",
    "q_retained_after_transport",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def maximum_sequence_difference(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        return float("inf")
    return max((abs(float(a) - float(b)) for a, b in zip(left, right)), default=0.0)


def main() -> None:
    checks: list[tuple[bool, str]] = []
    records: dict[str, object] = {}
    target_code = TARGET / "compute_prefix_history_v002.py"
    hostile_code = HERE / "independent_prefix_history_v002.py"
    checks.extend((
        (digest(target_code) == TARGET_IMPLEMENTATION, "target implementation hash"),
        (digest(hostile_code) == HOSTILE_IMPLEMENTATION, "hostile implementation hash"),
    ))
    for length in (4, 6, 8):
        target_path = TARGET / "CONTROL_HISTORY" / f"TARGET_V003_L{length}.json"
        hostile_path = HERE / f"CONTROL_HISTORY_L{length}_V002.json"
        checks.extend((
            (digest(target_path) == TARGET_OUTPUTS[length], f"L{length} target output hash"),
            (digest(hostile_path) == HOSTILE_OUTPUTS[length], f"L{length} hostile output hash"),
        ))
        target = json.loads(target_path.read_text())
        hostile = json.loads(hostile_path.read_text())
        checks.extend((
            (target["method_sha256"] == TARGET_IMPLEMENTATION,
             f"L{length} target self-custody"),
            (hostile["implementation_sha256"] == HOSTILE_IMPLEMENTATION,
             f"L{length} hostile self-custody"),
            (target["comparison"]["resolved"] is True, f"L{length} target resolved"),
            (hostile["comparison"]["resolved"] is True, f"L{length} hostile resolved"),
            (len(target["rows"]) == length, f"L{length} target event count"),
            (len(hostile["rows"]) == length, f"L{length} hostile event count"),
        ))
        scalar_maxima = {key: 0.0 for key in SCALARS}
        sector_linf = 0.0
        for event, (target_row, hostile_row) in enumerate(
                zip(target["rows"], hostile["rows"]), start=1):
            checks.extend((
                (target_row["event"] == event, f"L{length} target event {event} order"),
                (hostile_row["event"] == event, f"L{length} hostile event {event} order"),
                (target_row["terminal_children_streamed"] == (event == length),
                 f"L{length} target terminal flag {event}"),
                (hostile_row["terminal_children_streamed"] == (event == length),
                 f"L{length} hostile terminal flag {event}"),
            ))
            for key in SCALARS:
                difference = abs(float(target_row[key]) - float(hostile_row[key]))
                scalar_maxima[key] = max(scalar_maxima[key], difference)
            sector_linf = max(
                sector_linf,
                maximum_sequence_difference(
                    target_row["sector_weights"], hostile_row["sector_weights"]
                ),
            )
            checks.extend((
                (target_row["actual_solver"]["converged"] is True,
                 f"L{length} target actual convergence {event}"),
                (target_row["null_solver"]["converged"] is True,
                 f"L{length} target null convergence {event}"),
                (hostile_row["actual_solver"]["converged"] is True,
                 f"L{length} hostile actual convergence {event}"),
                (hostile_row["null_solver"]["converged"] is True,
                 f"L{length} hostile null convergence {event}"),
            ))
        for key, difference in scalar_maxima.items():
            checks.append((difference <= TOLERANCE, f"L{length} cross {key}"))
        checks.extend((
            (sector_linf <= TOLERANCE, f"L{length} cross sector weights"),
            (target["rows"][-1]["actual_solver"]["maximum_live_bytes"] <= 1_000_000_000,
             f"L{length} target terminal actual workset"),
            (target["rows"][-1]["null_solver"]["maximum_live_bytes"] <= 1_000_000_000,
             f"L{length} target terminal null workset"),
            (hostile["rows"][-1]["actual_solver"]["maximum_allocation_estimate_bytes"]
             <= 1_400_000_000, f"L{length} hostile terminal actual workset"),
            (hostile["rows"][-1]["null_solver"]["maximum_allocation_estimate_bytes"]
             <= 1_400_000_000, f"L{length} hostile terminal null workset"),
        ))
        records[str(length)] = {
            "target_output_sha256": TARGET_OUTPUTS[length],
            "hostile_output_sha256": HOSTILE_OUTPUTS[length],
            "cross_scalar_linf": scalar_maxima,
            "cross_sector_weight_linf": sector_linf,
            "target_wall_seconds": target["wall_seconds"],
            "target_peak_rss_bytes": target["peak_rss_bytes"],
            "hostile_wall_seconds": hostile["wall_seconds"],
            "hostile_peak_rss_bytes": hostile["peak_rss_bytes"],
        }
    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "AUDIT_R_PREFIX_HISTORY_CROSS_CONTROL_GATE_V002",
        "classification": (
            "PASS_PREFIX_HISTORY_CONTROLS_L4_L8_V002"
            if not failures else "FAIL_PREFIX_HISTORY_CONTROLS_L4_L8_V002"
        ),
        "implementation_sha256": HOSTILE_IMPLEMENTATION,
        "target_implementation_sha256": TARGET_IMPLEMENTATION,
        "tolerance": TOLERANCE,
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "controls": records,
        "authorization_if_pass": "L10_TARGET_AND_HOSTILE_BENCHMARK_ONLY",
        "claim_boundary": "FINITE_PREFIX_HISTORY_CONTROLS_ONLY__NO_L10_L12_SPECTRUM_Z1_OR_GRAVITY",
    }
    output = HERE / "CONTROL_GATE_V002.json"
    if output.exists():
        raise FileExistsError(f"refuse overwrite: {output}")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
