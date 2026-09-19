#!/usr/bin/env python3
"""Seal q-sharded target controls and the same-path L=10 benchmark."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUDIT = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
TOLERANCE = 1.0e-8
IMPLEMENTATION = "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7"
OUTPUT_HASHES = {
    4: "8bf8f4eb54781c599a9fb3ae407207e08504396128c82e1e838d5b47a1d564b2",
    6: "06ccf6f419b8e743c6aea014c90ba1598786fc5bb28331488cde0f0846215f33",
    8: "affc775a91186883b5dd7c7180340b06105523ad5744c38a470331c1a631868a",
    10: "873e45b6b37654910947711af1d8dc93d0def8ea0ef994587db206ab47b4267c",
}
REFERENCE_PATHS = {
    4: HERE / "CONTROL_HISTORY" / "TARGET_V003_L4.json",
    6: HERE / "CONTROL_HISTORY" / "TARGET_V003_L6.json",
    8: HERE / "CONTROL_HISTORY" / "TARGET_V003_L8.json",
    10: ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
        / "RAW_HISTORY" / "STREAMED_HISTORY_L10_V002.json",
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
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(16 * 2**20):
            value.update(block)
    return value.hexdigest()


def result_path(length: int) -> Path:
    if length < 10:
        return HERE / "CONTROL_HISTORY" / f"TARGET_V004_L{length}.json"
    return HERE / "BENCHMARK" / "TARGET_V004_QSHARD_L10.json"


def compare(left: dict, right: dict) -> tuple[dict[str, float], float]:
    if len(left["rows"]) != len(right["rows"]):
        return {key: math.inf for key in SCALARS}, math.inf
    maxima = {key: 0.0 for key in SCALARS}
    sector = 0.0
    for a, b in zip(left["rows"], right["rows"]):
        for key in SCALARS:
            maxima[key] = max(maxima[key], abs(float(a[key]) - float(b[key])))
        if len(a["sector_weights"]) != len(b["sector_weights"]):
            sector = math.inf
        else:
            sector = max(sector, max(
                (abs(float(x) - float(y))
                 for x, y in zip(a["sector_weights"], b["sector_weights"])),
                default=0.0,
            ))
    return maxima, sector


def main() -> None:
    checks: list[tuple[bool, str]] = []
    records = {}
    checks.extend((
        (digest(HERE / "compute_prefix_history_v004.py") == IMPLEMENTATION,
         "implementation custody"),
        (digest(HERE / "FROZEN_METHOD_V004.json")
         == "d98f994572a2830746bbb305bfa0146f417662abebc2bf5861e48c05071e90d2",
         "freeze custody"),
        (digest(HERE / "TARGET_V004_INVARIANTS.json")
         == "ee0ec87dcbd963dc0cc5acb70b7dcc6eb5bee81efa2c6bf766c2e382e57fae34",
         "invariant custody"),
        (json.loads((HERE / "TARGET_V004_INVARIANTS.json").read_text())
         ["classification"] == "PASS", "invariant pass"),
        (json.loads((AUDIT / "L10_GATE_V002.json").read_text())
         ["classification"] == "PASS_PREFIX_HISTORY_L10_GATE_V002",
         "independent L10 gate"),
    ))
    for length in (4, 6, 8, 10):
        path = result_path(length)
        checks.append((digest(path) == OUTPUT_HASHES[length], f"L{length} output custody"))
        result = json.loads(path.read_text())
        reference = json.loads(REFERENCE_PATHS[length].read_text())
        scalar, sector = compare(result, reference)
        checks.extend((
            (result["implementation_sha256"] == IMPLEMENTATION,
             f"L{length} self-custody"),
            (result["L"] == length and result["events"] == length,
             f"L{length} identity"),
            (result["comparison"]["resolved"] is True, f"L{length} resolved"),
            (result["resource"]["passed"] is True, f"L{length} resource"),
            (max(scalar.values()) <= TOLERANCE, f"L{length} observable agreement"),
            (sector <= TOLERANCE, f"L{length} sector agreement"),
            (result["rows"][-1]["terminal_children_streamed"] is True,
             f"L{length} terminal stream"),
            (all(not row["terminal_children_streamed"] for row in result["rows"][:-1]),
             f"L{length} terminal flag isolation"),
            (result["resource"]["maximum_numerical_workset_bytes"] <= 1_000_000_000,
             f"L{length} numerical workset"),
            (result["resource"]["peak_logical_scratch_bytes"] <= 20 * 2**30,
             f"L{length} logical scratch"),
        ))
        for event, row in enumerate(result["rows"], start=1):
            checks.extend((
                (row["event"] == event, f"L{length} event order {event}"),
                (row["actual_solver"]["converged"] is True,
                 f"L{length} actual convergence {event}"),
                (row["null_solver"]["converged"] is True,
                 f"L{length} null convergence {event}"),
                (abs(float(row["reverse_support_probability"])) <= TOLERANCE,
                 f"L{length} reverse null {event}"),
                (abs(float(row["blocked_null_state_error"])) <= TOLERANCE,
                 f"L{length} blocked null {event}"),
            ))
        for shard in result["terminal_shards"]:
            shard_file = Path(shard["path"])
            checks.extend((
                (shard_file.is_file(), f"L{length} q{shard['q']} shard present"),
                (shard_file.stat().st_size == shard["bytes"],
                 f"L{length} q{shard['q']} shard bytes"),
                (digest(shard_file) == shard["sha256"],
                 f"L{length} q{shard['q']} shard custody"),
            ))
        records[str(length)] = {
            "output_sha256": OUTPUT_HASHES[length],
            "maximum_observable_difference": max(scalar.values()),
            "maximum_sector_weight_difference": sector,
            "wall_seconds": result["resource"]["wall_seconds"],
            "peak_rss_bytes": result["resource"]["peak_rss_bytes"],
            "peak_logical_scratch_bytes": result["resource"]["peak_logical_scratch_bytes"],
            "maximum_numerical_workset_bytes":
                result["resource"]["maximum_numerical_workset_bytes"],
        }
    failures = [label for passed, label in checks if not passed]
    output = {
        "schema": "R_TARGET_Q_SHARDED_HISTORY_GATE_V004",
        "classification": (
            "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004"
            if not failures else "FAIL_TARGET_Q_SHARDED_L4_L10_GATE_V004"
        ),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "implementation_sha256": IMPLEMENTATION,
        "tolerance": TOLERANCE,
        "histories": records,
        "authorization_if_pass": "TARGET_V004_L12_EXECUTION_SUBJECT_TO_20GIB_SCRATCH_16GIB_RSS_6H_WALL_GUARDS",
        "claim_boundary": "FINITE_L4_L10_Q_SHARDED_CONTROLS__NO_L12_RESULT_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    }
    path = HERE / "TARGET_L12_GATE_V004.json"
    if path.exists():
        raise FileExistsError(f"refuse overwrite: {path}")
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(output["classification"])
    print(f"checks {output['checks_passed']}/{output['checks_total']}")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
