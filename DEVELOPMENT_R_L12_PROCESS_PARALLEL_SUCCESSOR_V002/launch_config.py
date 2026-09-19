#!/usr/bin/env python3
"""Fresh V002 allocation with V001 forensic custody preserved."""

from __future__ import annotations

from pathlib import Path
from typing import Final

from v001_bridge import parallel_runtime


ParallelRefusal = parallel_runtime.ParallelRefusal
CONFIGURED_WORKERS_BY_BRANCH = parallel_runtime.CONFIGURED_WORKERS_BY_BRANCH
CONFIGURED_TOTAL_WORKERS = parallel_runtime.CONFIGURED_TOTAL_WORKERS
HARD_WALL_LIMIT_SECONDS = parallel_runtime.HARD_WALL_LIMIT_SECONDS

HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
TARGET_PACKET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE_PACKET: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"

TARGET_WORKSPACE: Final[Path] = TARGET_PACKET / "WORKSPACES/L12_PROCESS_PARALLEL_V002"
TARGET_OUTPUT: Final[Path] = TARGET_PACKET / "PHYSICAL_OUTPUTS/HISTORY_L12_PROCESS_PARALLEL_V002.json"
TARGET_EVIDENCE: Final[Path] = TARGET_PACKET / "EVIDENCE/L12_PROCESS_PARALLEL_V002"
HOSTILE_WORKSPACE: Final[Path] = HOSTILE_PACKET / "V004R4_WORKSPACES/L12_PROCESS_PARALLEL_V002"
HOSTILE_OUTPUT: Final[Path] = HOSTILE_PACKET / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12_PROCESS_PARALLEL_V002.json"
HOSTILE_EVIDENCE: Final[Path] = HOSTILE_PACKET / "V004R4_EVIDENCE/L12_PROCESS_PARALLEL_V002"
RUN_LOG_ROOT: Final[Path] = HERE / "RUN_LOGS/L12_PROCESS_PARALLEL_V002"

PRESERVED_TARGET_SERIAL: Final[Path] = TARGET_PACKET / "WORKSPACES/L12"
PRESERVED_HOSTILE_SERIAL: Final[Path] = HOSTILE_PACKET / "V004R4_WORKSPACES/L12"
PRESERVED_TARGET_V001: Final[Path] = TARGET_PACKET / "WORKSPACES/L12_PROCESS_PARALLEL_V001"
PRESERVED_HOSTILE_V001: Final[Path] = HOSTILE_PACKET / "V004R4_WORKSPACES/L12_PROCESS_PARALLEL_V001"


def allocation_record(*, require_absent: bool = True) -> dict[str, object]:
    candidates = (
        TARGET_WORKSPACE,
        TARGET_OUTPUT,
        TARGET_EVIDENCE,
        HOSTILE_WORKSPACE,
        HOSTILE_OUTPUT,
        HOSTILE_EVIDENCE,
        RUN_LOG_ROOT,
    )
    if len({str(path) for path in candidates}) != len(candidates):
        raise ParallelRefusal("V002 workspace/output/evidence paths are aliased")
    for candidate in candidates:
        if ROOT not in candidate.parents or candidate.resolve() != candidate:
            raise ParallelRefusal("V002 path is noncanonical")
        if candidate.parent.is_symlink() or not candidate.parent.is_dir():
            raise ParallelRefusal(f"V002 parent path is unsafe: {candidate.parent}")
        if require_absent and (candidate.exists() or candidate.is_symlink()):
            raise ParallelRefusal(f"V002 allocation is not fresh: {candidate}")
    preserved = (
        PRESERVED_TARGET_SERIAL,
        PRESERVED_HOSTILE_SERIAL,
        PRESERVED_TARGET_V001,
        PRESERVED_HOSTILE_V001,
    )
    if any(not path.is_dir() or path.is_symlink() for path in preserved):
        raise ParallelRefusal("preserved serial/V001 forensic custody is absent")
    return {
        "schema": "L12_PROCESS_PARALLEL_RELAUNCH_ALLOCATION_V002",
        "hard_wall_limit_seconds": HARD_WALL_LIMIT_SECONDS,
        "hard_wall_limit_hours": 96,
        "workers_by_branch": dict(CONFIGURED_WORKERS_BY_BRANCH),
        "total_numerical_workers": CONFIGURED_TOTAL_WORKERS,
        "target_workspace": str(TARGET_WORKSPACE),
        "target_output": str(TARGET_OUTPUT),
        "target_evidence": str(TARGET_EVIDENCE),
        "hostile_workspace": str(HOSTILE_WORKSPACE),
        "hostile_output": str(HOSTILE_OUTPUT),
        "hostile_evidence": str(HOSTILE_EVIDENCE),
        "run_log_root": str(RUN_LOG_ROOT),
        "preserved_forensic_paths": [str(path) for path in preserved],
        "candidate_paths_absent": all(not path.exists() for path in candidates),
        "launch_state": "STAGED_NOT_TRIGGERED",
    }

