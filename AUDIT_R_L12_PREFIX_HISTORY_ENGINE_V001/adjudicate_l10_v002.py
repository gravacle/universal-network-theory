#!/usr/bin/env python3
"""Adjudicate the frozen target/hostile L=10 prefix-history benchmark."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_DIR = ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
SEALED_TARGET = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "RAW_HISTORY" / "STREAMED_HISTORY_L10_V002.json"
SEALED_HOSTILE = ROOT / "AUDIT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "RAW_HISTORY" / "BLIND_STREAMED_HISTORY_L10.json"
TARGET_RESULT = TARGET_DIR / "BENCHMARK" / "TARGET_V003_L10.json"
HOSTILE_RESULT = HERE / "BENCHMARK" / "HOSTILE_V002_L10.json"
HOSTILE_V003 = HERE / "independent_prefix_history_v003.py"
TOLERANCE = 1.0e-8

EXPECTED = {
    SEALED_TARGET: "928498a703457fd4c268ffa95bedf3704d6467add5082bd9fc7a5f6e4e327af5",
    SEALED_HOSTILE: "7dcaf32ed06a37e976dad88fd5d6d8dae5afcc3df88d573b70af486954ef3e29",
    TARGET_RESULT: "3c096dd3a40d2ad5e18aca1a8b8e6a13988a35ea4986f53164635bde7eceec0e",
    HOSTILE_RESULT: "bd921e1957b6bb07aeb2afa4871a1d0c5d39edfaf786177c8c74696fd6167173",
    TARGET_DIR / "compute_prefix_history_v002.py": "71458cd4b958d5b38cb24409ed769e790d9a83e1da8ac71fd2d3098fdb779694",
    HERE / "independent_prefix_history_v002.py": "e6b1be915a4d490939799e79efc017ab4e3808f1beeb3d984448b2508fb0522b",
    HOSTILE_V003: "cc4e1195283f60fddab1d70831965bd14a09435fd4aca2ee7fdde7e2d7e5ba7f",
}
SCALARS = (
    "W_n", "allow_probability", "blocked_probability",
    "reverse_support_probability", "blocked_null_state_error",
    "connector_delta_l1", "connector_delta_signed",
    "admission_total_content_residual", "admission_bandwidth_residual",
    "target_owner_residual", "transport_node_residual_l1",
    "transport_node_residual_linf", "transport_number_drift",
    "actual_norm_error", "null_norm_error", "q_genesis_after",
    "q_retained_after_transport",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sequence_linf(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        return math.inf
    return max((abs(float(a) - float(b)) for a, b in zip(left, right)), default=0.0)


def compare_histories(left: dict, right: dict) -> dict[str, object]:
    maxima = {key: 0.0 for key in SCALARS}
    sector = 0.0
    if len(left["rows"]) != len(right["rows"]):
        return {"scalar_linf": maxima, "sector_weight_linf": math.inf,
                "event_count_equal": False}
    for a, b in zip(left["rows"], right["rows"]):
        for key in SCALARS:
            maxima[key] = max(maxima[key], abs(float(a[key]) - float(b[key])))
        sector = max(sector, sequence_linf(a["sector_weights"], b["sector_weights"]))
    return {"scalar_linf": maxima, "sector_weight_linf": sector,
            "event_count_equal": True}


def comparison_pass(record: dict[str, object]) -> bool:
    return (
        bool(record["event_count_equal"])
        and float(record["sector_weight_linf"]) <= TOLERANCE
        and all(float(value) <= TOLERANCE
                for value in record["scalar_linf"].values())
    )


def main() -> None:
    checks: list[tuple[bool, str]] = []
    for path, expected in EXPECTED.items():
        checks.append((digest(path) == expected, f"custody {path.name}"))
    target = json.loads(TARGET_RESULT.read_text())
    hostile = json.loads(HOSTILE_RESULT.read_text())
    sealed_target = json.loads(SEALED_TARGET.read_text())
    sealed_hostile = json.loads(SEALED_HOSTILE.read_text())
    comparisons = {
        "target_to_sealed_target": compare_histories(target, sealed_target),
        "hostile_to_sealed_hostile": compare_histories(hostile, sealed_hostile),
        "target_to_hostile": compare_histories(target, hostile),
    }
    for label, comparison in comparisons.items():
        checks.append((comparison_pass(comparison), label))
    target_terminal = target["rows"][-1]
    hostile_terminal = hostile["rows"][-1]
    checks.extend((
        (target["L"] == 10 and hostile["L"] == 10, "L10 identities"),
        (len(target["rows"]) == 10 and len(hostile["rows"]) == 10, "event counts"),
        (target["comparison"]["coarse_fine"]["maximum_disagreement"] <= TOLERANCE,
         "target coarse/fine"),
        (hostile["comparison"]["rough_sharp"]["maximum_disagreement"] <= TOLERANCE,
         "hostile rough/sharp"),
        (hostile["comparison"]["resolved"] is True, "hostile resolved"),
        (target["resource_guards"]["rss_pass"] is True, "target RSS hard guard"),
        (target["resource_guards"]["wall_pass"] is True, "target wall hard guard"),
        (target["resource_guards"]["projection_margin_pass"] is False,
         "target conservative projection miss recorded"),
        (target_terminal["terminal_children_streamed"] is True,
         "target terminal stream"),
        (hostile_terminal["terminal_children_streamed"] is True,
         "hostile terminal stream"),
        (target_terminal["actual_solver"]["low_memory_batches"] > 0,
         "target actual low-memory path"),
        (target_terminal["null_solver"]["low_memory_batches"] > 0,
         "target null low-memory path"),
        (hostile_terminal["actual_solver"]["algorithm"] == "RECURRENCE_REPLAY_GL_GROUPS",
         "hostile actual recurrence path"),
        (hostile_terminal["null_solver"]["algorithm"] == "RECURRENCE_REPLAY_GL_GROUPS",
         "hostile null recurrence path"),
        (target_terminal["actual_solver"]["converged"] is True
         and target_terminal["null_solver"]["converged"] is True,
         "target terminal convergence"),
        (hostile_terminal["actual_solver"]["converged"] is True
         and hostile_terminal["null_solver"]["converged"] is True,
         "hostile terminal convergence"),
        (target["peak_rss_bytes"] <= 4 * 2**30, "target observed RSS"),
        (hostile["peak_rss_bytes"] <= 4 * 2**30, "hostile observed RSS"),
        (target["wall_seconds"] <= 2 * 3600, "target observed hard wall"),
        (hostile["wall_seconds"] <= 2 * 3600, "hostile observed hard wall"),
    ))
    for name, history in (("target", target), ("hostile", hostile)):
        for event, row in enumerate(history["rows"], start=1):
            checks.extend((
                (row["event"] == event, f"{name} event order {event}"),
                (row["terminal_children_streamed"] == (event == 10),
                 f"{name} terminal flag {event}"),
                (abs(float(row["reverse_support_probability"])) <= TOLERANCE,
                 f"{name} reverse null {event}"),
                (abs(float(row["blocked_null_state_error"])) <= TOLERANCE,
                 f"{name} blocked-null {event}"),
                (row["actual_solver"]["converged"] is True,
                 f"{name} actual convergence {event}"),
                (row["null_solver"]["converged"] is True,
                 f"{name} null convergence {event}"),
            ))
    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "AUDIT_R_PREFIX_HISTORY_L10_GATE_V002",
        "classification": (
            "PASS_PREFIX_HISTORY_L10_GATE_V002"
            if not failures else "FAIL_PREFIX_HISTORY_L10_GATE_V002"
        ),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "tolerance": TOLERANCE,
        "comparisons": comparisons,
        "target_v003_result_sha256": EXPECTED[TARGET_RESULT],
        "hostile_v002_result_sha256": EXPECTED[HOSTILE_RESULT],
        "hostile_v003_sha256": EXPECTED[HOSTILE_V003],
        "target_resource": {
            "wall_seconds": target["wall_seconds"],
            "peak_rss_bytes": target["peak_rss_bytes"],
            "hard_wall_pass": target["resource_guards"]["wall_pass"],
            "hard_rss_pass": target["resource_guards"]["rss_pass"],
            "conservative_387_35_second_projection_pass":
                target["resource_guards"]["projection_margin_pass"],
        },
        "hostile_resource": {
            "wall_seconds": hostile["wall_seconds"],
            "peak_rss_bytes": hostile["peak_rss_bytes"],
        },
        "authorization_if_pass": (
            "HOSTILE_V003_L12_EXECUTION_SUBJECT_TO_ITS_20GIB_SCRATCH_16GIB_RSS_6H_WALL_GUARDS"
        ),
        "claim_boundary": (
            "EXACT_FINITE_L10_HISTORY_BENCHMARK__CONSERVATIVE_RUNTIME_PROJECTION_MISSED__"
            "NO_L12_RESULT_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
        ),
    }
    output = HERE / "L10_GATE_V002.json"
    if output.exists():
        raise FileExistsError(f"refuse overwrite: {output}")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    for label, comparison in comparisons.items():
        print(label, max(comparison["scalar_linf"].values()),
              comparison["sector_weight_linf"])
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
