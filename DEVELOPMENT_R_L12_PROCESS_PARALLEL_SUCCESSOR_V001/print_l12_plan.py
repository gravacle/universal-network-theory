#!/usr/bin/env python3
"""Print the exact static L12 process plan without starting a worker."""

from __future__ import annotations

import json
import os

from launch_config import allocation_record
from hostile_parallel import hostile_run_plan
from parallel_runtime import (
    CONFIGURED_TOTAL_WORKERS,
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
    physical_memory_bytes,
    recommended_branch_workers,
)
from target_parallel import target_run_plan


def main() -> None:
    ram = physical_memory_bytes()
    target = target_run_plan(12)
    hostile = hostile_run_plan(12)
    record = {
        "schema": "L12_PROCESS_PARALLEL_STATIC_PLAN_V001",
        "L": 12,
        "logical_cpu_count": os.cpu_count() or 1,
        "physical_memory_bytes": ram,
        "simultaneous_branches": 2,
        "target_workers": CONFIGURED_WORKERS_BY_BRANCH["target"],
        "hostile_workers": CONFIGURED_WORKERS_BY_BRANCH["hostile"],
        "total_numerical_workers": CONFIGURED_TOTAL_WORKERS,
        "hard_wall_limit_seconds": HARD_WALL_LIMIT_SECONDS,
        "worker_capacity": {
            "target": recommended_branch_workers(
                branch="target", memory_bytes=ram
            ),
            "hostile": recommended_branch_workers(
                branch="hostile", memory_bytes=ram
            ),
        },
        "allocation": allocation_record(require_absent=False),
        "target": target,
        "hostile": hostile,
        "combined": {
            key: target[key] + hostile[key]
            for key in ("total_tasks", "charge_sectors", "row_windows", "total_work_units")
        },
        "large_arrays_transported_between_processes": False,
        "parent_only_progress_and_reduction": True,
    }
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
