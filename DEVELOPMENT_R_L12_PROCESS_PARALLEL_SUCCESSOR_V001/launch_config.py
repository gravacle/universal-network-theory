#!/usr/bin/env python3
"""Canonical non-overwriting paths and fixed resources for the next L12 run."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from parallel_runtime import (
    CONFIGURED_TOTAL_WORKERS,
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
    ParallelRefusal,
)


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
TARGET_PACKET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE_PACKET: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"

TARGET_WORKSPACE: Final[Path] = (
    TARGET_PACKET / "WORKSPACES/L12_PROCESS_PARALLEL_V001"
)
TARGET_OUTPUT: Final[Path] = (
    TARGET_PACKET / "PHYSICAL_OUTPUTS/HISTORY_L12_PROCESS_PARALLEL_V001.json"
)
HOSTILE_WORKSPACE: Final[Path] = (
    HOSTILE_PACKET / "V004R4_WORKSPACES/L12_PROCESS_PARALLEL_V001"
)
HOSTILE_OUTPUT: Final[Path] = (
    HOSTILE_PACKET
    / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12_PROCESS_PARALLEL_V001.json"
)

PRESERVED_TARGET_WORKSPACE: Final[Path] = TARGET_PACKET / "WORKSPACES/L12"
PRESERVED_HOSTILE_WORKSPACE: Final[Path] = (
    HOSTILE_PACKET / "V004R4_WORKSPACES/L12"
)


def allocation_record(*, require_absent: bool = True) -> dict[str, object]:
    candidates = (
        TARGET_WORKSPACE,
        TARGET_OUTPUT,
        HOSTILE_WORKSPACE,
        HOSTILE_OUTPUT,
    )
    if len({str(path) for path in candidates}) != len(candidates):
        raise ParallelRefusal("successor workspace/output paths are aliased")
    for path in candidates:
        if ROOT not in path.parents or path.resolve() != path:
            raise ParallelRefusal("successor workspace/output path is noncanonical")
        if not path.parent.is_dir() or path.parent.is_symlink():
            raise ParallelRefusal("successor workspace/output parent is unsafe")
        if require_absent and (path.exists() or path.is_symlink()):
            raise ParallelRefusal(f"successor allocation is not fresh: {path}")
    if (
        not PRESERVED_TARGET_WORKSPACE.is_dir()
        or not PRESERVED_HOSTILE_WORKSPACE.is_dir()
        or PRESERVED_TARGET_WORKSPACE in candidates
        or PRESERVED_HOSTILE_WORKSPACE in candidates
    ):
        raise ParallelRefusal("preserved obstruction workspace custody is absent")
    return {
        "schema": "L12_PROCESS_PARALLEL_RELAUNCH_ALLOCATION_V001",
        "hard_wall_limit_seconds": HARD_WALL_LIMIT_SECONDS,
        "hard_wall_limit_hours": 96,
        "workers_by_branch": dict(CONFIGURED_WORKERS_BY_BRANCH),
        "total_numerical_workers": CONFIGURED_TOTAL_WORKERS,
        "target_workspace": str(TARGET_WORKSPACE),
        "target_output": str(TARGET_OUTPUT),
        "hostile_workspace": str(HOSTILE_WORKSPACE),
        "hostile_output": str(HOSTILE_OUTPUT),
        "preserved_target_workspace": str(PRESERVED_TARGET_WORKSPACE),
        "preserved_hostile_workspace": str(PRESERVED_HOSTILE_WORKSPACE),
        "candidate_paths_absent": all(not path.exists() for path in candidates),
    }
