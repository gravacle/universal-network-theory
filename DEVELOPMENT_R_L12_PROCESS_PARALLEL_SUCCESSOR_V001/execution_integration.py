#!/usr/bin/env python3
"""Narrow integration points for successor target/hostile consumers.

These functions begin only after the existing parent process has authenticated
all frozen sources, gates, manifests, and cache payloads.  They stop before
sealing or publishing any history.  A successor consumer must bind the hashes
of this packet and then call its existing publication path on the returned
objects.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from hostile_parallel import HostileParallelAdapter, hostile
from parallel_runtime import (
    HARD_WALL_LIMIT_SECONDS,
    BranchProcessPool,
    parent_termination_guard,
)
from target_parallel import TargetParallelAdapter, target


def run_target_rough_and_sharp(
    *,
    length: int,
    cache_root: Path,
    cache_manifest_sha256: str,
    workspace: Path,
    deadline_monotonic: float | None = None,
    max_workers: int | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Replace the two serial ``v004.history`` calls in a target successor."""
    if target.CACHE is None:
        raise RuntimeError("target parent cache must be fully authenticated first")
    deadline = (
        deadline_from_now()
        if deadline_monotonic is None
        else deadline_monotonic
    )
    original_builder_wall = target.builder.WALL_LIMIT
    original_engine_wall = target.v004.WALL_LIMIT
    target.builder.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    target.v004.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    try:
        with BranchProcessPool(
            branch="target",
            cache_root=cache_root,
            manifest_sha256=cache_manifest_sha256,
            length=length,
            deadline_monotonic=deadline,
            max_workers=max_workers,
        ) as pool:
            with parent_termination_guard(pool), TargetParallelAdapter(pool):
                rough_root = workspace / "rough"
                sharp_root = workspace / "sharp"
                rough = target.v004.history(
                    length, target.v004.sealed.COARSE, rough_root, retain_terminal=False
                )
                target.v004.remove_resolution(rough_root, workspace)
                sharp = target.v004.history(
                    length, target.v004.sealed.FINE, sharp_root, retain_terminal=True
                )
                pool.assert_run_complete()
                comparison = target.v004.sealed.summarize(length, rough, sharp)
            resource = pool.resource_record()
    finally:
        target.builder.WALL_LIMIT = original_builder_wall
        target.v004.WALL_LIMIT = original_engine_wall
    return rough, sharp, comparison, resource


def run_hostile_rough_and_sharp(
    *,
    length: int,
    cache_root: Path,
    cache_manifest_sha256: str,
    workspace: Path,
    deadline_monotonic: float | None = None,
    max_workers: int | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Replace the two serial ``v3.history`` calls in a hostile successor."""
    if hostile.legacy.CACHE is None:
        raise RuntimeError("hostile parent cache must be fully authenticated first")
    deadline = (
        deadline_from_now()
        if deadline_monotonic is None
        else deadline_monotonic
    )
    original_physical_wall = hostile.physical.L12_WALL_LIMIT
    original_engine_wall = hostile.v3.WALL_LIMIT
    hostile.physical.L12_WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    hostile.v3.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    try:
        with BranchProcessPool(
            branch="hostile",
            cache_root=cache_root,
            manifest_sha256=cache_manifest_sha256,
            length=length,
            deadline_monotonic=deadline,
            max_workers=max_workers,
        ) as pool:
            with parent_termination_guard(pool), HostileParallelAdapter(pool):
                rough_root = workspace / "rough"
                sharp_root = workspace / "sharp"
                rough = hostile.v3.history(
                    length, hostile.physical.ROUGH, rough_root, retain_terminal=False
                )
                hostile.v3.remove_resolution(rough_root)
                sharp = hostile.v3.history(
                    length, hostile.physical.SHARP, sharp_root, retain_terminal=True
                )
                pool.assert_run_complete()
                comparison = hostile.physical.compare(length, rough, sharp)
            resource = pool.resource_record()
    finally:
        hostile.physical.L12_WALL_LIMIT = original_physical_wall
        hostile.v3.WALL_LIMIT = original_engine_wall
    return rough, sharp, comparison, resource


def deadline_from_now(seconds: float = HARD_WALL_LIMIT_SECONDS) -> float:
    """Return a live deadline bounded by the successor's 96-hour ceiling."""
    if (
        not isinstance(seconds, float)
        or not 0.0 < seconds <= HARD_WALL_LIMIT_SECONDS
    ):
        raise ValueError("seconds must be a positive float within 96 hours")
    return time.monotonic() + seconds
