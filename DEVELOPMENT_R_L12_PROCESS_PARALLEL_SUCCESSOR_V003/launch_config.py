#!/usr/bin/env python3
"""Isolated allocation for the V003 bounded numerical repair."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
V002: Final[Path] = ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V002"
if str(V002) not in sys.path:
    sys.path.append(str(V002))

from v001_bridge import parallel_runtime  # noqa: E402


CONFIGURED_WORKERS_BY_BRANCH = {"target": 7, "hostile": 7}
CONFIGURED_TOTAL_WORKERS = 14
HARD_WALL_LIMIT_SECONDS = 96 * 3600.0
if parallel_runtime.HARD_WALL_LIMIT_SECONDS != HARD_WALL_LIMIT_SECONDS:
    raise RuntimeError("V001 process runtime no longer provides the authorized 96-hour ceiling")

TARGET_PACKET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE_PACKET: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"

TARGET_WORKSPACE: Final[Path] = TARGET_PACKET / "WORKSPACES/L12_PROCESS_PARALLEL_V003R1"
TARGET_OUTPUT: Final[Path] = TARGET_PACKET / "PHYSICAL_OUTPUTS/HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
TARGET_EVIDENCE: Final[Path] = TARGET_PACKET / "EVIDENCE/L12_PROCESS_PARALLEL_V003R1"
HOSTILE_WORKSPACE: Final[Path] = HOSTILE_PACKET / "V004R4_WORKSPACES/L12_PROCESS_PARALLEL_V003R1"
HOSTILE_OUTPUT: Final[Path] = HOSTILE_PACKET / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
HOSTILE_EVIDENCE: Final[Path] = HOSTILE_PACKET / "V004R4_EVIDENCE/L12_PROCESS_PARALLEL_V003R1"
RUN_LOG_ROOT: Final[Path] = HERE / "RUN_LOGS/L12_PROCESS_PARALLEL_V003R1"

TARGET_V002_EVIDENCE: Final[Path] = TARGET_PACKET / "EVIDENCE/L12_PROCESS_PARALLEL_V002"
TARGET_V002_WORKSPACE: Final[Path] = TARGET_PACKET / "WORKSPACES/L12_PROCESS_PARALLEL_V002"
HOSTILE_V002_EVIDENCE: Final[Path] = HOSTILE_PACKET / "V004R4_EVIDENCE/L12_PROCESS_PARALLEL_V002"
HOSTILE_V002_WORKSPACE: Final[Path] = HOSTILE_PACKET / "V004R4_WORKSPACES/L12_PROCESS_PARALLEL_V002"

TARGET_ROUGH_V002: Final[Path] = TARGET_V002_EVIDENCE / "histories/002222__ROUGH_SUMMARY.json"
HOSTILE_SHARP_V002: Final[Path] = HOSTILE_V002_EVIDENCE / "histories/001798__SHARP_SUMMARY.json"


def allocated_paths() -> tuple[Path, ...]:
    return (
        TARGET_WORKSPACE,
        TARGET_OUTPUT,
        TARGET_EVIDENCE,
        HOSTILE_WORKSPACE,
        HOSTILE_OUTPUT,
        HOSTILE_EVIDENCE,
        RUN_LOG_ROOT,
    )


def require_fresh_allocation() -> None:
    occupied = [str(path) for path in allocated_paths() if path.exists() or path.is_symlink()]
    if occupied:
        raise RuntimeError(f"V003 allocation is not fresh: {occupied}")
