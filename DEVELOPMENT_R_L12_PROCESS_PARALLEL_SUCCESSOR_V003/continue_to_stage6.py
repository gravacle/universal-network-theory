#!/usr/bin/env python3
"""Continue a legitimately resolved V003 L12 repair through Stage 6 only."""

from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_HISTORY = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/"
    "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
HOSTILE_HISTORY = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/"
    "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
TARGET_EVIDENCE = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/EVIDENCE/"
    "L12_PROCESS_PARALLEL_V003R1"
)
HOSTILE_EVIDENCE = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_EVIDENCE/"
    "L12_PROCESS_PARALLEL_V003R1"
)
TARGET_TERMINAL = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/"
    "L12_PROCESS_PARALLEL_V003R1/sharp"
)
HOSTILE_TERMINAL = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES/"
    "L12_PROCESS_PARALLEL_V002/sharp"
)
STAGE4 = ROOT / "AUDIT_R_L12_NUMERICAL_REPAIR_V003/adjudicate_v003.py"
STAGE4_FREEZE = ROOT / "AUDIT_R_L12_NUMERICAL_REPAIR_V003/PRE_OUTPUT_FREEZE_V003.json"
STAGE4_BLIND = ROOT / "AUDIT_R_L12_NUMERICAL_REPAIR_V003/NORMALIZED_BLIND_HISTORY_L12_V003R1.json"
STAGE4_RESULT = ROOT / "AUDIT_R_L12_NUMERICAL_REPAIR_V003/EXACT_ADJUDICATION_V003R1.json"
STAGE5 = ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/build_manifest_v003.py"
STAGE5_FREEZE = ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/PRE_OUTPUT_FREEZE_V003.json"
MANIFEST = ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
COMPATIBILITY = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001"
SPECTRUM = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
CONTROL = COMPATIBILITY / "blind_contract_control.py"
BLIND_WORKER = COMPATIBILITY / "blind_interval_worker.py"
BLIND_PUBLISHER = COMPATIBILITY / "blind_index_publisher.py"
ADJUDICATOR = COMPATIBILITY / "blind_adjudication_entrypoint.py"
SOURCE_FREEZE = COMPATIBILITY / "SOURCE_FREEZE.json"
TARGET_DRIVER = SPECTRUM / "interval_spectrum_driver.py"
BLIND_RUN = COMPATIBILITY / "RUN_V002_L12_V003R1"
TARGET_RUN = SPECTRUM / "RUN_V002_L12_V003R1"
PLAN = BLIND_RUN / "SECTOR_PLAN.json"
BLIND_FREEZE = BLIND_RUN / "BLIND_METHOD_FREEZE.json"
BLIND_ROWS = BLIND_RUN / "RAW"
BLIND_CREDENTIALS = BLIND_RUN / "AUTHORIZATION"
BLIND_INDEX = BLIND_RUN / "SPECTRUM_INDEX.json"
TARGET_INDEX = TARGET_RUN / "SPECTRUM_INDEX.json"
FINAL_RESULT = SPECTRUM / "ADJUDICATION_V002_L12_V003R1.json"
BLIND_TOKEN = "RUN_HASH_PINNED_BLIND_RELATIONAL_INTERVAL_SPECTRUM_V001"
TARGET_TOKEN = "RUN_HASH_PINNED_RELATIONAL_INTERVAL_SPECTRUM_V001"
MANIFEST_TOKEN = "BUILD_AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003"
MAX_WAVE = 4
MAX_SECTOR_SECONDS = 3 * 60 * 60
MAX_SECTOR_RSS = 6 * (1 << 30)
MAX_WAVE_RSS = 32 * (1 << 30)
ACTIVE_CHILDREN: list[subprocess.Popen[str]] = []


class ContinuationRefusal(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise ContinuationRefusal(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            value.update(chunk)
    return value.hexdigest()


def run_checked(command: list[str], label: str) -> None:
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    ACTIVE_CHILDREN.append(process)
    try:
        stdout, stderr = process.communicate()
    except BaseException:
        terminate_wave([((0, 0), process, time.monotonic())])
        raise
    finally:
        if process in ACTIVE_CHILDREN:
            ACTIVE_CHILDREN.remove(process)
    if stdout:
        print(stdout, end="", flush=True)
    if process.returncode != 0:
        raise ContinuationRefusal(
            f"{label} refused ({process.returncode}): "
            + (stderr or stdout)[-2000:]
        )


def verify_completion(history: Path, evidence: Path, role: str) -> str:
    demand(history.is_file(), f"{role}: V003 history absent")
    history_hash = sha256(history)
    records = sorted((evidence / "lifecycle").glob("*__BRANCH_COMPLETE.json"))
    demand(len(records) == 1, f"{role}: completion-record census")
    record = json.loads(records[0].read_text())
    payload = record.get("payload")
    demand(isinstance(payload, dict), f"{role}: completion payload")
    demand(Path(str(payload.get("output"))).resolve() == history.resolve(),
           f"{role}: completion output binding")
    demand(payload.get("output_sha256") == history_hash,
           f"{role}: completion SHA-256 binding")
    value = json.loads(history.read_text())
    comparison = value.get("comparison")
    demand(isinstance(comparison, dict) and comparison.get("resolved") is True,
           f"{role}: history is not legitimately resolved")
    return history_hash


def stage4() -> None:
    target_hash = verify_completion(TARGET_HISTORY, TARGET_EVIDENCE, "target")
    hostile_hash = verify_completion(HOSTILE_HISTORY, HOSTILE_EVIDENCE, "hostile")
    run_checked([
        sys.executable, "-B", str(STAGE4),
        "--target", str(TARGET_HISTORY), "--target-sha256", target_hash,
        "--hostile", str(HOSTILE_HISTORY), "--hostile-sha256", hostile_hash,
        "--target-terminal-root", str(TARGET_TERMINAL),
        "--hostile-terminal-root", str(HOSTILE_TERMINAL),
        "--freeze-sha256", sha256(STAGE4_FREEZE),
        "--blind-output", str(STAGE4_BLIND),
        "--output", str(STAGE4_RESULT),
    ], "Stage 4 exact V003 adjudication")


def stage5() -> None:
    run_checked([
        sys.executable, "-B", str(STAGE5),
        "--authorization", MANIFEST_TOKEN,
        "--freeze-sha256", sha256(STAGE5_FREEZE),
    ], "Stage 5 L4--L12 sector construction")


def process_rss(pid: int) -> int:
    completed = subprocess.run(
        ["ps", "-o", "rss=", "-p", str(pid)],
        capture_output=True, text=True, check=False,
    )
    demand(completed.returncode == 0 and completed.stdout.strip().isdigit(),
           f"cannot read blind worker RSS for PID {pid}")
    return int(completed.stdout.strip()) * 1024


def terminate_wave(processes: list[tuple[tuple[int, int], subprocess.Popen[str], float]]) -> None:
    for _pair, process, _started in processes:
        if process.poll() is None:
            process.terminate()
    deadline = time.monotonic() + 10.0
    while time.monotonic() < deadline and any(p.poll() is None for _, p, _ in processes):
        time.sleep(0.1)
    for _pair, process, _started in processes:
        if process.poll() is None:
            process.kill()
    for _pair, process, _started in processes:
        process.wait()
        if process in ACTIVE_CHILDREN:
            ACTIVE_CHILDREN.remove(process)


def run_blind_rows(pairs: list[tuple[int, int]], freeze_hash: str) -> None:
    environment = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
    }
    for start in range(0, len(pairs), MAX_WAVE):
        wave = pairs[start:start + MAX_WAVE]
        processes: list[tuple[tuple[int, int], subprocess.Popen[str], float]] = []
        try:
            for length, charge in wave:
                row = BLIND_ROWS / f"SECTOR_L{length}_Q{charge}.json"
                credential = BLIND_CREDENTIALS / f"SECTOR_L{length}_Q{charge}.json"
                run_checked([
                    sys.executable, "-B", str(CONTROL), "issue-credential",
                    "--freeze", str(BLIND_FREEZE),
                    "--freeze-sha256", freeze_hash,
                    "--L", str(length), "--q", str(charge),
                    "--physical-output", str(row), "--output", str(credential),
                ], f"blind credential L{length}q{charge}")
                process = subprocess.Popen(
                    [
                        sys.executable, "-B", str(BLIND_WORKER),
                        "--L", str(length), "--q", str(charge),
                        "--run-token", BLIND_TOKEN,
                        "--credential", str(credential),
                        "--credential-sha256", sha256(credential),
                        "--output", str(row),
                    ],
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=environment,
                )
                ACTIVE_CHILDREN.append(process)
                processes.append(((length, charge), process, time.monotonic()))
            while any(process.poll() is None for _, process, _ in processes):
                live = [(pair, process, begun) for pair, process, begun in processes
                        if process.poll() is None]
                rss = []
                for _pair, process, _begun in live:
                    try:
                        rss.append(process_rss(process.pid))
                    except ContinuationRefusal:
                        if process.poll() is None:
                            raise
                        rss.append(0)
                demand(all(value <= MAX_SECTOR_RSS for value in rss),
                       "blind sector RSS guard exceeded")
                demand(sum(rss) <= MAX_WAVE_RSS, "blind wave RSS guard exceeded")
                demand(all(time.monotonic() - begun <= MAX_SECTOR_SECONDS
                           for _, _, begun in live),
                       "blind sector wall guard exceeded")
                time.sleep(0.2)
            for pair, process, _begun in processes:
                stdout, stderr = process.communicate()
                if stdout:
                    print(stdout, end="", flush=True)
                demand(process.returncode == 0,
                       f"blind L{pair[0]}q{pair[1]} refused: {(stderr or stdout)[-1500:]}")
                demand((BLIND_ROWS / f"SECTOR_L{pair[0]}_Q{pair[1]}.json").is_file(),
                       f"blind L{pair[0]}q{pair[1]} output absent")
                if process in ACTIVE_CHILDREN:
                    ACTIVE_CHILDREN.remove(process)
                print(f"STAGE6_BLIND_COMPLETE L={pair[0]} q={pair[1]}", flush=True)
        except BaseException:
            terminate_wave(processes)
            raise


def stage6() -> None:
    manifest_hash = sha256(MANIFEST)
    BLIND_RUN.mkdir(parents=True, exist_ok=False)
    BLIND_ROWS.mkdir()
    BLIND_CREDENTIALS.mkdir()
    run_checked([
        sys.executable, "-B", str(CONTROL), "produce-plan",
        "--manifest", str(MANIFEST), "--manifest-sha256", manifest_hash,
        "--output", str(PLAN),
    ], "Stage 6 blind sector plan")
    plan_hash = sha256(PLAN)
    run_checked([
        sys.executable, "-B", str(CONTROL), "produce-freeze",
        "--manifest", str(MANIFEST), "--manifest-sha256", manifest_hash,
        "--sector-plan", str(PLAN), "--sector-plan-sha256", plan_hash,
        "--source-freeze", str(SOURCE_FREEZE),
        "--source-freeze-sha256", sha256(SOURCE_FREEZE),
        "--output", str(BLIND_FREEZE),
    ], "Stage 6 runnable blind freeze")
    freeze_hash = sha256(BLIND_FREEZE)
    plan = json.loads(PLAN.read_text())
    raw_pairs = plan.get("planned_sectors")
    demand(isinstance(raw_pairs, list) and raw_pairs,
           "Stage 6 positive sector plan is empty")
    pairs = [(int(item[0]), int(item[1])) for item in raw_pairs]
    demand(pairs == sorted(set(pairs)), "Stage 6 sector plan order/census")
    print(f"STAGE6_DENOMINATOR sectors={len(pairs)} pairs={pairs}", flush=True)
    run_blind_rows(pairs, freeze_hash)
    run_checked([
        sys.executable, "-B", str(BLIND_PUBLISHER),
        "--freeze", str(BLIND_FREEZE), "--freeze-sha256", freeze_hash,
        "--rows-dir", str(BLIND_ROWS),
        "--credentials-dir", str(BLIND_CREDENTIALS),
        "--output", str(BLIND_INDEX),
    ], "Stage 6 blind index")
    run_checked([
        sys.executable, "-B", str(TARGET_DRIVER),
        "--mode", "execute-target",
        "--manifest", str(MANIFEST), "--manifest-sha256", manifest_hash,
        "--authorization", TARGET_TOKEN,
        "--blind-freeze", str(BLIND_FREEZE),
        "--blind-freeze-sha256", freeze_hash,
        "--output-dir", str(TARGET_RUN),
    ], "Stage 6 target interval sectors")
    run_checked([
        sys.executable, "-B", str(ADJUDICATOR),
        "--manifest", str(MANIFEST), "--manifest-sha256", manifest_hash,
        "--target-index", str(TARGET_INDEX),
        "--target-index-sha256", sha256(TARGET_INDEX),
        "--blind-index", str(BLIND_INDEX),
        "--blind-index-sha256", sha256(BLIND_INDEX),
        "--output", str(FINAL_RESULT),
    ], "Stage 6 exact target/blind adjudication")
    result = json.loads(FINAL_RESULT.read_text())
    print(json.dumps({
        "stage": 6,
        "result": str(FINAL_RESULT.relative_to(ROOT)),
        "sha256": sha256(FINAL_RESULT),
        "classification": result.get("classification"),
        "status": result.get("status"),
        "stage7_started": False,
    }, sort_keys=True), flush=True)


def main() -> int:
    def stop(_signum: int, _frame: Any) -> None:
        terminate_wave([
            ((0, 0), process, time.monotonic())
            for process in list(ACTIVE_CHILDREN)
        ])
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        demand(not any(path.exists() for path in (
            STAGE4_BLIND, STAGE4_RESULT, MANIFEST, BLIND_RUN, TARGET_RUN, FINAL_RESULT,
        )), "downstream V003R1 allocation is not fresh")
        stage4()
        stage5()
        stage6()
    except (ContinuationRefusal, OSError, ValueError, MemoryError, KeyboardInterrupt) as error:
        print(f"STAGE4_TO_STAGE6_REFUSED {type(error).__name__}:{error}",
              file=sys.stderr, flush=True)
        return 2
    print("STAGE4_TO_STAGE6_COMPLETE__PAUSED_BEFORE_STAGE7", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
