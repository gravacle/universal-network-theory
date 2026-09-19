#!/usr/bin/env python3
"""Independent dual-branch launcher for the authorized V003 L12 repair."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V002 = ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V002"
if str(V002) not in sys.path:
    sys.path.append(str(V002))

from launcher_supervision import supervise  # noqa: E402

from launch_config import (  # noqa: E402
    CONFIGURED_TOTAL_WORKERS,
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
    RUN_LOG_ROOT,
    require_fresh_allocation,
)
from repair_kernels import hostile_repair_plan, target_repair_plan  # noqa: E402


BRANCH_EXECUTABLE = HERE / "run_l12_branch.py"


def denominator() -> None:
    target = target_repair_plan(12)
    hostile = hostile_repair_plan(12)
    print(
        "L12_V003_DENOMINATOR "
        f"target_charge_sectors={target['charge_sectors']} "
        f"target_row_windows={target['row_windows']} "
        f"target_tasks={target['total_tasks']} "
        f"target_estimated_solver_cell_steps={target['total_work_units']} "
        f"hostile_charge_sectors={hostile['charge_sectors']} "
        f"hostile_row_windows={hostile['row_windows']} "
        f"hostile_tasks={hostile['total_tasks']} "
        f"hostile_estimated_solver_cell_steps={hostile['total_work_units']} "
        f"combined_tasks={target['total_tasks'] + hostile['total_tasks']} "
        f"combined_estimated_solver_cell_steps={target['total_work_units'] + hostile['total_work_units']}",
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="verify fresh paths and print the denominator without launching",
    )
    arguments = parser.parse_args()
    require_fresh_allocation()
    denominator()
    if arguments.preflight:
        print("L12_V003_PREFLIGHT_PASS allocation=V003R1 launch_attempted=false", flush=True)
        return 0
    print(
        "L12_V003_LAUNCH "
        f"workers_target={CONFIGURED_WORKERS_BY_BRANCH['target']} "
        f"workers_hostile={CONFIGURED_WORKERS_BY_BRANCH['hostile']} "
        f"workers_total={CONFIGURED_TOTAL_WORKERS} "
        f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f} "
        "target_replay=rough_plus_sharp "
        "hostile_replay=rough_plus_resumed_sharp_event_12 "
        "branches=independent_simultaneous fail_fast=false",
        flush=True,
    )
    return_codes = supervise(
        commands={
            branch: [sys.executable, str(BRANCH_EXECUTABLE), branch]
            for branch in ("target", "hostile")
        },
        log_root=RUN_LOG_ROOT,
        cwd=ROOT,
    )
    return 0 if all(code == 0 for code in return_codes.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
