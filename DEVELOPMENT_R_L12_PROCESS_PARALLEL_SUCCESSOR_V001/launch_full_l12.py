#!/usr/bin/env python3
"""Launch and supervise both authenticated process-parallel L12 parents."""

from __future__ import annotations

import os
import selectors
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import IO

from hostile_parallel import hostile_run_plan
from launch_config import allocation_record
from parallel_runtime import (
    CONFIGURED_TOTAL_WORKERS,
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
)
from run_l12_branch import verify_successor_packet
from target_parallel import target_run_plan


HERE = Path(__file__).resolve().parent
RUN_LOG_ROOT = HERE / "RUN_LOGS/L12_PROCESS_PARALLEL_V001"
BRANCH_EXECUTABLE = HERE / "run_l12_branch.py"


def denominator() -> None:
    target = target_run_plan(12)
    hostile = hostile_run_plan(12)
    print(
        "L12_DENOMINATOR "
        f"target_charge_sectors={target['charge_sectors']} "
        f"target_row_windows={target['row_windows']} "
        f"target_tasks={target['total_tasks']} "
        f"target_solver_cell_steps={target['total_work_units']} "
        f"hostile_charge_sectors={hostile['charge_sectors']} "
        f"hostile_row_windows={hostile['row_windows']} "
        f"hostile_tasks={hostile['total_tasks']} "
        f"hostile_solver_cell_steps={hostile['total_work_units']} "
        f"combined_charge_sectors={target['charge_sectors'] + hostile['charge_sectors']} "
        f"combined_row_windows={target['row_windows'] + hostile['row_windows']} "
        f"combined_tasks={target['total_tasks'] + hostile['total_tasks']} "
        f"combined_solver_cell_steps={target['total_work_units'] + hostile['total_work_units']}",
        flush=True,
    )


def main() -> int:
    verify_successor_packet()
    allocation_record(require_absent=True)
    if RUN_LOG_ROOT.exists() or RUN_LOG_ROOT.is_symlink():
        raise RuntimeError("successor run-log allocation is not fresh")
    denominator()
    print(
        "L12_LAUNCH "
        f"workers_target={CONFIGURED_WORKERS_BY_BRANCH['target']} "
        f"workers_hostile={CONFIGURED_WORKERS_BY_BRANCH['hostile']} "
        f"workers_total={CONFIGURED_TOTAL_WORKERS} "
        f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f} "
        "branches=simultaneous",
        flush=True,
    )
    RUN_LOG_ROOT.mkdir(parents=True, exist_ok=False)
    processes: dict[str, subprocess.Popen[str]] = {}
    streams: dict[IO[str], tuple[str, IO[str]]] = {}
    selector = selectors.DefaultSelector()
    stopping = False

    def stop(signum: int, _frame: object) -> None:
        nonlocal stopping
        if stopping:
            return
        stopping = True
        print(f"L12_LAUNCH_STOP signal={signum} preserving_workspaces=true", flush=True)
        for process in processes.values():
            if process.poll() is None:
                process.send_signal(signal.SIGTERM)

    old_handlers = {
        signum: signal.getsignal(signum) for signum in (signal.SIGINT, signal.SIGTERM)
    }
    for signum in old_handlers:
        signal.signal(signum, stop)
    try:
        environment = dict(os.environ)
        environment["PYTHONPYCACHEPREFIX"] = "/tmp/l12-process-pycache"
        for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
            environment[name] = "1"
        for branch in ("target", "hostile"):
            log = (RUN_LOG_ROOT / f"{branch}.log").open("x", encoding="utf-8")
            process = subprocess.Popen(
                [sys.executable, str(BRANCH_EXECUTABLE), branch],
                cwd=str(HERE.parent),
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            if process.stdout is None:
                raise RuntimeError("branch stdout pipe was not created")
            processes[branch] = process
            streams[process.stdout] = (branch, log)
            selector.register(process.stdout, selectors.EVENT_READ)
            print(f"L12_BRANCH_STARTED branch={branch} parent_pid={process.pid}", flush=True)
        while streams:
            for key, _events in selector.select(timeout=1.0):
                stream = key.fileobj
                branch, log = streams[stream]
                line = stream.readline()
                if line:
                    log.write(line)
                    log.flush()
                    print(f"[{branch}] {line}", end="", flush=True)
                else:
                    selector.unregister(stream)
                    stream.close()
                    log.flush()
                    os.fsync(log.fileno())
                    log.close()
                    del streams[stream]
            if any(process.poll() not in (None, 0) for process in processes.values()):
                stop(signal.SIGTERM, None)
        return_codes = {branch: process.wait() for branch, process in processes.items()}
        print(f"L12_LAUNCH_COMPLETE return_codes={return_codes}", flush=True)
        return 0 if all(code == 0 for code in return_codes.values()) else 2
    finally:
        for signum, handler in old_handlers.items():
            signal.signal(signum, handler)
        for stream, (_branch, log) in list(streams.items()):
            try:
                selector.unregister(stream)
            except Exception:
                pass
            stream.close()
            log.close()
        selector.close()


if __name__ == "__main__":
    raise SystemExit(main())
