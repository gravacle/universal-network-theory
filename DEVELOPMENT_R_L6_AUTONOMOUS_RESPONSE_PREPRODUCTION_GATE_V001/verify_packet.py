#!/usr/bin/env python3
"""Read-only exact custody and LOCKED-state check; never executes L6 physics."""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import static_estimator


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent.resolve()
SOURCE_NAMES = {
    "README.md", "GATE_MATRIX.json", "INPUT_FREEZE.json", "TASK_PLAN.json",
    "static_estimator.py", "test_static_estimator.py", "verify_packet.py",
}
EXPECTED_GATE_IDS = {
    "local_L6_input_census", "L4_target_dense_and_hardened_restart",
    "L4_independent_event0_reconciliation", "L6_target_successor_kernel_and_validation",
    "L6_target_source_task_input_authorization_freeze", "SSH_destination_remote_scratch_host_key",
    "one_way_allowlist_and_verified_return_manifest", "pinned_remote_numerical_environment",
    "remote_synthetic_interrupt_reboot_restart_corruption_tests",
    "measured_L6_response_q_benchmark_on_selected_host",
    "declared_maximum_uncheckpointed_q_wall_loss", "enforced_memory_disk_wall_and_power_resource_review",
    "hostile_L6_q_shard_and_q_output_restartable_successor",
    "hostile_L4_streaming_monolith_equivalence_and_restart_tests",
    "prospective_L6_cross_lane_fields_tolerances_and_unblind_order",
    "separate_L6_event0_execution_authorization",
    "L8_after_L6_target_hostile_agreement_and_revised_estimate",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def reject_constant(value: str) -> None:
    raise RuntimeError(f"nonfinite JSON token: {value}")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=strict_object, parse_constant=reject_constant)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_file(relative: str) -> Path:
    route = Path(relative)
    require(
        relative == route.as_posix() and not route.is_absolute()
        and route.parts and all(part not in (".", "..") for part in route.parts),
        f"unsafe relative path: {relative}",
    )
    current = ROOT
    for part in route.parts:
        current = current / part
        require(not current.is_symlink(), f"symlink route: {relative}")
    require(current.is_file(), f"missing regular file: {relative}")
    require(current.resolve().is_relative_to(ROOT), f"path escaped root: {relative}")
    return current


def check_source_hashes() -> int:
    source_file = PACKET / "SOURCE_HASHES.sha256"
    require(source_file.is_file() and not source_file.is_symlink(), "missing source hash list")
    lines = source_file.read_text(encoding="utf-8").splitlines()
    observed: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        require(match is not None, "malformed source hash list")
        digest, name = match.groups()
        require(name not in observed, "duplicate source hash path")
        observed[name] = digest
    require(set(observed) == SOURCE_NAMES, "packet source census")
    require(list(observed) == sorted(observed), "source hash list is not sorted")
    for name, digest in observed.items():
        path = PACKET / name
        require(path.is_file() and not path.is_symlink(), f"missing source: {name}")
        require(sha256(path) == digest, f"source changed: {name}")
    return len(observed)


def check_git(freeze: dict[str, Any]) -> None:
    parent = freeze["frozen_parent_commit"]
    require(re.fullmatch(r"[0-9a-f]{40}", parent) is not None, "parent commit shape")
    tree = subprocess.check_output(
        ["git", "rev-parse", f"{parent}^{{tree}}"], cwd=ROOT, text=True,
    ).strip()
    require(tree == freeze["frozen_parent_tree"], "frozen parent tree mismatch")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", parent, "HEAD"],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(ancestor.returncode == 0, "current checkout does not descend from frozen parent")


def check_inputs(freeze: dict[str, Any]) -> tuple[int, int]:
    require(freeze["status"] == "LOCAL_INPUT_CUSTODY_ONLY__NO_L6_NUMERICAL_AUTHORIZATION", "input freeze status")
    require(freeze["L"] == 6 and freeze["historical_absolute_paths_are_provenance_only"] is True, "input freeze scope")
    check_git(freeze)
    sources = freeze["frozen_source_and_prior_evidence"]
    require(len(sources) == 10 and len({row["path"] for row in sources}) == 10, "frozen source census")
    for row in sources:
        require(sha256(safe_file(row["path"])) == row["sha256"], f"source/evidence hash mismatch: {row['path']}")
    history_record = freeze["history"]
    history_path = safe_file(history_record["path"])
    require(sha256(history_path) == history_record["sha256"], "L6 history hash")
    history = load(history_path)
    require(history["schema"] == history_record["schema"] and history["L"] == 6, "L6 history identity")
    engine = next(row for row in sources if row["role"] == "frozen_target_transport_engine")
    require(history["target_v004_sha256"] == engine["sha256"], "history/engine binding")
    shards = freeze["preterminal_shards"]
    require(len(shards) == history_record["terminal_shard_count"] == 6, "L6 shard census")
    require([row["q"] for row in shards] == list(range(6)), "L6 shard order")
    historical = history["terminal_shards"]
    require(len(historical) == 6, "history shard census")
    total = 0
    prefix = "/Users/brianmulconrey/PerInfo/where-atoms-come-from/audited-386ee2c/"
    for expected, sealed in zip(shards, historical):
        q = expected["q"]
        require(expected["path"] == f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L6/sharp/prefix_05/q_{q:02d}.npy", "shard relative route")
        require(expected["historical_path"] == prefix + expected["path"], "historical route")
        require(
            {key: expected[key] for key in ("q", "shape", "bytes", "sha256")} ==
            {key: sealed[key] for key in ("q", "shape", "bytes", "sha256")}
            and expected["historical_path"] == sealed["path"],
            f"history shard record mismatch: q{q}",
        )
        require(expected["shape"] == [math.comb(5, q), math.comb(12, q)], "shard shape")
        file = safe_file(expected["path"])
        require(file.stat().st_size == expected["bytes"] and sha256(file) == expected["sha256"], f"L6 shard bytes/hash q{q}")
        total += expected["bytes"]
    require(total == history_record["shard_bytes_total"] == 99776, "L6 input byte total")
    require(freeze["additional_ignored_cache_payloads_required_beyond_six_sealed_shards"] is False, "additional cache payloads unexpectedly required")
    return len(sources), len(shards)


def check_plan_and_gates(plan: dict[str, Any], gates: dict[str, Any]) -> None:
    require(plan["status"] == "DESIGN_ONLY_NO_RUNNER_OR_EXECUTION_AUTHORIZATION", "task plan status")
    require(plan["L"] == 6 and plan["event"] == 0 and plan["workers_initial"] == 1, "task plan scope")
    require(plan["resolution"] == "TARGET_V004_FINE" and plan["branch"] == "target", "task plan method")
    require(plan["checkpoint_unit"] == "ONE_EVENT_OUTPUT_CARRIER_NUMBER_SECTOR_q", "checkpoint unit")
    tasks = plan["tasks"]
    require(len(tasks) == 7 and [task["q_out"] for task in tasks] == list(range(7)), "seven task census")
    for q, task in enumerate(tasks):
        terminal = list(range(max(0, q - 1), min(6, q + 1) + 1))
        preterminal = sorted({old for t in terminal for old in (t - 1, t) if 0 <= old < 6})
        require(task == {
            "task_id": f"L06_event00_qout{q:02d}", "q_out": q,
            "work_units": math.comb(12, q),
            "terminal_q_inputs": terminal, "preterminal_q_inputs": preterminal,
        }, f"task design mismatch q{q}")
        require(static_estimator.sector_bounds(q)["carrier_dimension"] == task["work_units"], "static/task dimension")
    require(gates["status"] == "LOCKED_NO_L6_NUMERICAL_EXECUTION", "gate status")
    for key in ("L6_execution_authorized", "L8_execution_authorized", "has_L6_numerical_runner", "has_L6_response_result"):
        require(gates[key] is False, f"gate {key} unexpectedly opened")
    require(all(gates["evidence"][key] is None for key in (
        "L6_response_wall_seconds", "L6_response_peak_process_tree_rss_bytes",
        "L6_response_checkpoint_bytes", "L6_response_power_watts", "remote_host_benchmark",
    )), "invented L6 response evidence")
    observed = {row["id"]: row["status"] for row in gates["required_gates"]}
    require(len(observed) == len(gates["required_gates"]) and set(observed) == EXPECTED_GATE_IDS, "gate census")
    require(observed["separate_L6_event0_execution_authorization"] == "MISSING", "L6 authorization state")
    require(observed["L8_after_L6_target_hostile_agreement_and_revised_estimate"] == "LOCKED", "L8 state")
    require(all(status not in ("PASS", "AUTHORIZED") for key, status in observed.items() if key.startswith("L6_")), "L6 gate prematurely passed")
    report = static_estimator.static_report()
    require(report["max_raw_complex_factor_bytes_bound"] == 1655280, "static factor bound")
    require(report["max_reduced_hermitian_bytes_bound"] == 774400, "static reduced bound")


def main() -> int:
    source_count = check_source_hashes()
    freeze = load(PACKET / "INPUT_FREEZE.json")
    source_inputs, shards = check_inputs(freeze)
    check_plan_and_gates(load(PACKET / "TASK_PLAN.json"), load(PACKET / "GATE_MATRIX.json"))
    print(
        "PASS_LOCKED_L6_PREPRODUCTION_PACKET: "
        f"{source_count} packet sources, {source_inputs} frozen source/evidence files, "
        f"{shards} sealed L6 shards, seven static tasks; no L6 numerical execution"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, KeyError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL_LOCKED_L6_PREPRODUCTION_PACKET: {error}", file=sys.stderr)
        raise SystemExit(1)
