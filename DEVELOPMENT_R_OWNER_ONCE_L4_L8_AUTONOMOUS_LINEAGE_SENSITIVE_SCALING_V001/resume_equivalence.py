#!/usr/bin/env python3
"""Real SIGTERM/resume and checkpoint-refusal gate for the L4 target route."""

from __future__ import annotations

import copy
import json
import math
import os
import resource
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

import target_lineage_scaling as target


PACKET = Path(__file__).resolve().parent
EVIDENCE_ROOT = PACKET / "RESUME_EQUIVALENCE_V001R1"
RESULT_PATH = EVIDENCE_ROOT / "RESULT.json"
TARGET_SCRIPT = PACKET / "target_lineage_scaling.py"


class ResumeGateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResumeGateError(message)


def directory_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def rss_bytes(which: int) -> int:
    raw = int(resource.getrusage(which).ru_maxrss)
    return raw if sys.platform == "darwin" else raw * 1024


def command(checkpoint: Path, output: Path, resume: bool = False) -> list[str]:
    value = [
        sys.executable,
        str(TARGET_SCRIPT),
        "run-l4",
        "--checkpoint-root",
        str(checkpoint),
        "--output",
        str(output),
    ]
    if resume:
        value.append("--resume")
    return value


def run_checked(value: list[str], timeout: float = 60.0) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        value,
        cwd=target.ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
    )
    require(completed.returncode == 0, f"command failed ({completed.returncode}): {completed.stdout}")
    return completed


def canonical_sector_payload(path: Path) -> dict[str, Any]:
    outer = target.load_json(path)
    require(outer.get("schema") == "L14_RESUMABLE_TASK_RESULT_V002", f"sector schema: {path}")
    result = copy.deepcopy(outer["result"])
    result.pop("resource", None)
    return {
        "schema": outer["schema"],
        "run_id": outer["run_id"],
        "branch": outer["branch"],
        "phase": outer["phase"],
        "task_id": outer["task_id"],
        "task_sha256": outer["task_sha256"],
        "work_units": outer["work_units"],
        "result": result,
    }


def canonical_final_payload(path: Path) -> dict[str, Any]:
    result = copy.deepcopy(target.load_json(path))
    result.pop("resource", None)
    result.pop("checkpoint", None)
    for sector in result.get("sector_results", []):
        sector.pop("resource", None)
    return result


def canonical_hash(payload: Any) -> str:
    return target.sha256_bytes(target.canonical_json_bytes(payload))


def sector_hashes(checkpoint: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted((checkpoint / "results").glob("L04_event00_qout*.json")):
        payload = canonical_sector_payload(path)
        result[payload["task_id"]] = canonical_hash(payload)
    return result


def standard_tasks(runtime: Any) -> list[Any]:
    return [
        runtime.TaskSpec(
            task_id=f"L04_event00_qout{q:02d}",
            payload={"L": 4, "event": 0, "q_out": q},
            work_units=max(1, math.comb(8, q)),
        )
        for q in range(5)
    ]


def standard_parameters() -> dict[str, Any]:
    return {
        "schema": "L4_L8_TARGET_SCALING_RUN_PARAMETERS_V001",
        "authorized_lengths": [4],
        "L": 4,
        "events": [0],
        "resolution": "TARGET_V004_FINE",
        "history_sha256": target.HISTORY_HASHES[4],
        "engine_sha256": target.DEPENDENCY_HASHES[str(target.ENGINE_RELATIVE)],
        "kernel_sha256": target.sha256_file(TARGET_SCRIPT),
        "dense_baseline_sha256": target.DEPENDENCY_HASHES[str(target.DENSE_RESULT_RELATIVE)],
    }


def make_runner(
    runtime: Any,
    checkpoint: Path,
    *,
    parameters: Mapping[str, Any] | None = None,
    tasks: list[Any] | None = None,
    kernel: Path = TARGET_SCRIPT,
) -> Any:
    return runtime.ResumableProcessPool(
        checkpoint_root=checkpoint,
        run_id="L4-L8-TARGET-SCALING-V001-L4-EVENT00",
        branch="target",
        phase="dense-l4-reproduction",
        kernel_module=kernel,
        kernel_function="sector_kernel",
        tasks=standard_tasks(runtime) if tasks is None else tasks,
        workers=1,
        parameters=standard_parameters() if parameters is None else dict(parameters),
    )


def expect_identity_refusal(label: str, operation: Any) -> dict[str, str]:
    try:
        operation()
    except Exception as error:  # exact refusal type is recorded below
        return {"label": label, "error_type": type(error).__name__, "message": str(error)}
    raise ResumeGateError(f"{label} was not refused")


def copy_checkpoint(source: Path, destination: Path) -> None:
    require(not destination.exists(), f"refuse to overwrite checkpoint copy: {destination}")
    shutil.copytree(source, destination)


def main() -> int:
    require(not EVIDENCE_ROOT.exists(), f"refuse to overwrite evidence root: {EVIDENCE_ROOT}")
    EVIDENCE_ROOT.mkdir(parents=True)
    started = time.perf_counter()
    target.authenticate_all_inputs()
    durable, runtime = target.load_resume_runtime()

    control_checkpoint = EVIDENCE_ROOT / "CONTROL_CHECKPOINT"
    control_output = EVIDENCE_ROOT / "CONTROL_RESULT.json"
    control_started = time.perf_counter()
    control_process = run_checked(command(control_checkpoint, control_output))
    control_wall = time.perf_counter() - control_started
    require(control_output.is_file(), "uninterrupted control did not publish final output")
    require((control_checkpoint / "COMPLETE.json").is_file(), "control COMPLETE missing")

    interrupted_checkpoint = EVIDENCE_ROOT / "INTERRUPTED_CHECKPOINT"
    interrupted_output = EVIDENCE_ROOT / "INTERRUPTED_RESULT.json"
    interrupted_started = time.perf_counter()
    process = subprocess.Popen(
        command(interrupted_checkpoint, interrupted_output),
        cwd=target.ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    deadline = time.monotonic() + 30.0
    committed_before_signal = 0
    while time.monotonic() < deadline:
        committed_before_signal = len(
            list((interrupted_checkpoint / "results").glob("L04_event00_qout*.json"))
        )
        if committed_before_signal >= 2 or process.poll() is not None:
            break
        time.sleep(0.005)
    require(committed_before_signal >= 2, "fewer than two checkpoints committed before SIGTERM")
    require(process.poll() is None, "process ended before deliberate SIGTERM")
    process.send_signal(signal.SIGTERM)
    interrupted_log, _ = process.communicate(timeout=60.0)
    interrupted_wall = time.perf_counter() - interrupted_started
    require(process.returncode == 75, f"interrupted exit {process.returncode}: {interrupted_log}")
    committed_after_stop = len(
        list((interrupted_checkpoint / "results").glob("L04_event00_qout*.json"))
    )
    require(2 <= committed_after_stop < 5, "interruption did not leave a resumable partial sector set")
    require(not interrupted_output.exists(), "premature final output after SIGTERM")
    require(not (interrupted_checkpoint / "COMPLETE.json").exists(), "premature COMPLETE after SIGTERM")

    refusals: list[dict[str, str]] = []
    changed_config = standard_parameters()
    changed_config["resolution"] = "CHANGED_CONFIG_MUST_REFUSE"
    refusals.append(
        expect_identity_refusal(
            "changed_config",
            lambda: make_runner(runtime, interrupted_checkpoint, parameters=changed_config).bind_identity(True),
        )
    )
    changed_input = standard_parameters()
    changed_input["history_sha256"] = "0" * 64
    refusals.append(
        expect_identity_refusal(
            "changed_input",
            lambda: make_runner(runtime, interrupted_checkpoint, parameters=changed_input).bind_identity(True),
        )
    )
    refusals.append(
        expect_identity_refusal(
            "changed_source",
            lambda: make_runner(runtime, interrupted_checkpoint, kernel=Path(__file__)).bind_identity(True),
        )
    )
    changed_tasks = standard_tasks(runtime)[:-1]
    refusals.append(
        expect_identity_refusal(
            "changed_task_plan",
            lambda: make_runner(runtime, interrupted_checkpoint, tasks=changed_tasks).bind_identity(True),
        )
    )

    first_result = sorted((interrupted_checkpoint / "results").glob("*.json"))[0]
    truncated_root = EVIDENCE_ROOT / "TRUNCATED_CHECKPOINT_COPY"
    copy_checkpoint(interrupted_checkpoint, truncated_root)
    truncated_file = truncated_root / "results" / first_result.name
    os.chmod(truncated_file, 0o644)
    original_bytes = truncated_file.read_bytes()
    truncated_file.write_bytes(original_bytes[: max(1, len(original_bytes) // 2)])
    refusals.append(
        expect_identity_refusal(
            "truncated_checkpoint",
            lambda: (make_runner(runtime, truncated_root).bind_identity(True), make_runner(runtime, truncated_root).load_completed()),
        )
    )

    corrupt_root = EVIDENCE_ROOT / "CORRUPT_CHECKPOINT_COPY"
    copy_checkpoint(interrupted_checkpoint, corrupt_root)
    corrupt_file = corrupt_root / "results" / first_result.name
    os.chmod(corrupt_file, 0o644)
    corrupt_payload = target.load_json(corrupt_file)
    corrupt_payload["task_sha256"] = "f" * 64
    corrupt_file.write_bytes(target.canonical_json_bytes(corrupt_payload))
    refusals.append(
        expect_identity_refusal(
            "corrupt_checkpoint",
            lambda: (make_runner(runtime, corrupt_root).bind_identity(True), make_runner(runtime, corrupt_root).load_completed()),
        )
    )

    orphan = interrupted_checkpoint / "results" / ".orphan-sector.tmp"
    orphan.write_bytes(b"not-json-and-not-a-final-task\n")
    resumed_started = time.perf_counter()
    resumed_process = run_checked(command(interrupted_checkpoint, interrupted_output, resume=True))
    resumed_wall = time.perf_counter() - resumed_started
    require(orphan.read_bytes() == b"not-json-and-not-a-final-task\n", "orphan temp was interpreted or altered")
    require(interrupted_output.is_file(), "resumed run did not publish final output")
    require((interrupted_checkpoint / "COMPLETE.json").is_file(), "resumed COMPLETE missing")

    control_sector_hashes = sector_hashes(control_checkpoint)
    resumed_sector_hashes = sector_hashes(interrupted_checkpoint)
    require(len(control_sector_hashes) == len(resumed_sector_hashes) == 5, "final sector census")
    require(control_sector_hashes == resumed_sector_hashes, "canonical sector hashes differ")
    control_final_hash = canonical_hash(canonical_final_payload(control_output))
    resumed_final_hash = canonical_hash(canonical_final_payload(interrupted_output))
    require(control_final_hash == resumed_final_hash, "canonical final outputs differ")

    refusal_labels = {record["label"] for record in refusals}
    require(
        refusal_labels
        == {
            "changed_config",
            "changed_input",
            "changed_source",
            "changed_task_plan",
            "truncated_checkpoint",
            "corrupt_checkpoint",
        },
        "refusal census",
    )
    result = {
        "schema": "L4_TARGET_SIGTERM_RESUME_EQUIVALENCE_V001",
        "classification": "PASS_L4_TARGET_SIGTERM_RESUME_EQUIVALENCE",
        "source_binding": {
            "harness_sha256": target.sha256_file(Path(__file__)),
            "target_kernel_sha256": target.sha256_file(TARGET_SCRIPT),
            "runtime_sha256": target.DEPENDENCY_HASHES[str(target.RUNTIME_RELATIVE)],
            "durable_evidence_sha256": target.DEPENDENCY_HASHES[str(target.DURABLE_RELATIVE)],
            "history_sha256": target.HISTORY_HASHES[4],
            "dense_baseline_sha256": target.DEPENDENCY_HASHES[str(target.DENSE_RESULT_RELATIVE)],
        },
        "interruption": {
            "signal": "SIGTERM",
            "minimum_required_commits": 2,
            "committed_before_signal": committed_before_signal,
            "committed_after_graceful_stop": committed_after_stop,
            "total_tasks": 5,
            "interrupted_returncode": process.returncode,
            "premature_final_output": False,
            "premature_complete_marker": False,
            "explicit_resume_flag": True,
        },
        "equivalence": {
            "canonicalization": (
                "UTF8_SORTED_KEYS_COMPACT_ALLOW_NAN_FALSE_TRAILING_LF;_"
                "EXCLUDE_EXECUTION_RESOURCE_AND_CHECKPOINT_LOCATION_ONLY"
            ),
            "control_final_canonical_sha256": control_final_hash,
            "resumed_final_canonical_sha256": resumed_final_hash,
            "sector_canonical_sha256": control_sector_hashes,
            "all_sector_hashes_equal": True,
            "final_hash_equal": True,
            "control_raw_result_sha256": target.sha256_file(control_output),
            "resumed_raw_result_sha256": target.sha256_file(interrupted_output),
        },
        "refusals": refusals,
        "orphan_temp": {
            "relative_path": str(orphan.relative_to(EVIDENCE_ROOT)),
            "sha256": target.sha256_file(orphan),
            "ignored_without_mutation": True,
        },
        "resource": {
            "total_harness_wall_seconds": time.perf_counter() - started,
            "control_wall_seconds": control_wall,
            "interrupted_wall_seconds": interrupted_wall,
            "resume_wall_seconds": resumed_wall,
            "peak_harness_rss_bytes": rss_bytes(resource.RUSAGE_SELF),
            "peak_child_rss_bytes": rss_bytes(resource.RUSAGE_CHILDREN),
            "control_checkpoint_bytes": directory_bytes(control_checkpoint),
            "resumed_checkpoint_bytes": directory_bytes(interrupted_checkpoint),
            "test_evidence_bytes_before_result": directory_bytes(EVIDENCE_ROOT),
        },
        "logs": {
            "control_stdout_sha256": target.sha256_bytes(control_process.stdout.encode("utf-8")),
            "interrupted_stdout_sha256": target.sha256_bytes(interrupted_log.encode("utf-8")),
            "resumed_stdout_sha256": target.sha256_bytes(resumed_process.stdout.encode("utf-8")),
        },
        "claim_boundary": (
            "L4_TARGET_CHECKPOINT_DURABILITY_AND_EQUIVALENCE_ONLY__"
            "NO_INDEPENDENT_AUDIT_L6_L8_OR_PHYSICAL_SCALING_RESULT"
        ),
    }
    durable.immutable_write_json(RESULT_PATH, result)
    print(result["classification"])
    print(
        "commits={}/{} canonical_final={} wall={:.6f}s evidence_bytes={}".format(
            committed_before_signal,
            committed_after_stop,
            control_final_hash,
            result["resource"]["total_harness_wall_seconds"],
            directory_bytes(EVIDENCE_ROOT),
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ResumeGateError, OSError, ValueError, subprocess.SubprocessError, target.ScalingError) as error:
        print(f"FAIL L4 target resume equivalence: {error}", file=sys.stderr)
        raise SystemExit(1)
