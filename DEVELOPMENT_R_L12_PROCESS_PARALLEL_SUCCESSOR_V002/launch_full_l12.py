#!/usr/bin/env python3
"""Staged V002 L12 launcher.  Do not invoke before post-L4 review."""

from __future__ import annotations

import sys
from pathlib import Path

from launch_config import (
    CONFIGURED_TOTAL_WORKERS,
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
    RUN_LOG_ROOT,
    allocation_record,
)
from launcher_supervision import supervise
from run_l12_branch import verify_successor_packet
from v001_bridge import hostile_parallel, target_parallel


HERE = Path(__file__).resolve().parent
BRANCH_EXECUTABLE = HERE / "run_l12_branch.py"


def denominator() -> None:
    target = target_parallel.target_run_plan(12)
    hostile = hostile_parallel.hostile_run_plan(12)
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
    denominator()
    print(
        "L12_LAUNCH "
        f"workers_target={CONFIGURED_WORKERS_BY_BRANCH['target']} "
        f"workers_hostile={CONFIGURED_WORKERS_BY_BRANCH['hostile']} "
        f"workers_total={CONFIGURED_TOTAL_WORKERS} "
        f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f} "
        "branches=independent_simultaneous fail_fast=false",
        flush=True,
    )
    return_codes = supervise(
        commands={
            branch: [sys.executable, str(BRANCH_EXECUTABLE), branch]
            for branch in ("target", "hostile")
        },
        log_root=RUN_LOG_ROOT,
        cwd=HERE.parent,
    )
    return 0 if all(code == 0 for code in return_codes.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())

