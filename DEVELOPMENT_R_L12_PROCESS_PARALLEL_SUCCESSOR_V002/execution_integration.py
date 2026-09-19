#!/usr/bin/env python3
"""Persistent V002 integration around the frozen V001 numerical kernels."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from comparison_gate import persist_hostile_before_gate, persist_target_before_gate
from evidence import EvidenceJournal
from persistent_runtime import PersistentBranchProcessPool
from v001_bridge import hostile, hostile_parallel, parallel_runtime, target, target_parallel


HARD_WALL_LIMIT_SECONDS = parallel_runtime.HARD_WALL_LIMIT_SECONDS


def run_target_rough_and_sharp(
    *,
    length: int,
    cache_root: Path,
    cache_manifest_sha256: str,
    workspace: Path,
    evidence: EvidenceJournal,
    deadline_monotonic: float | None = None,
    max_workers: int | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if target.CACHE is None:
        raise RuntimeError("target parent cache must be fully authenticated first")
    deadline = deadline_from_now() if deadline_monotonic is None else deadline_monotonic
    original_builder_wall = target.builder.WALL_LIMIT
    original_engine_wall = target.v004.WALL_LIMIT
    target.builder.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    target.v004.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    try:
        with PersistentBranchProcessPool(
            branch="target",
            cache_root=cache_root,
            manifest_sha256=cache_manifest_sha256,
            length=length,
            deadline_monotonic=deadline,
            max_workers=max_workers,
            evidence=evidence,
        ) as pool:
            with parallel_runtime.parent_termination_guard(pool), target_parallel.TargetParallelAdapter(pool):
                rough_root = workspace / "rough"
                sharp_root = workspace / "sharp"
                rough = target.v004.history(
                    length, target.v004.sealed.COARSE, rough_root, retain_terminal=False
                )
                evidence.history("rough", rough)
                target.v004.remove_resolution(rough_root, workspace)
                sharp = target.v004.history(
                    length, target.v004.sealed.FINE, sharp_root, retain_terminal=True
                )
                evidence.history("sharp", sharp)
                pool.assert_run_complete()
                comparison = target.v004.sealed.summarize(length, rough, sharp)
                diagnostic = persist_target_before_gate(
                    evidence, length, rough, sharp, comparison
                )
            resource = pool.resource_record()
    finally:
        target.builder.WALL_LIMIT = original_builder_wall
        target.v004.WALL_LIMIT = original_engine_wall
    return rough, sharp, comparison, diagnostic, resource


def run_hostile_rough_and_sharp(
    *,
    length: int,
    cache_root: Path,
    cache_manifest_sha256: str,
    workspace: Path,
    evidence: EvidenceJournal,
    deadline_monotonic: float | None = None,
    max_workers: int | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if hostile.legacy.CACHE is None:
        raise RuntimeError("hostile parent cache must be fully authenticated first")
    deadline = deadline_from_now() if deadline_monotonic is None else deadline_monotonic
    original_physical_wall = hostile.physical.L12_WALL_LIMIT
    original_engine_wall = hostile.v3.WALL_LIMIT
    hostile.physical.L12_WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    hostile.v3.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    try:
        with PersistentBranchProcessPool(
            branch="hostile",
            cache_root=cache_root,
            manifest_sha256=cache_manifest_sha256,
            length=length,
            deadline_monotonic=deadline,
            max_workers=max_workers,
            evidence=evidence,
        ) as pool:
            with parallel_runtime.parent_termination_guard(pool), hostile_parallel.HostileParallelAdapter(pool):
                rough_root = workspace / "rough"
                sharp_root = workspace / "sharp"
                rough = hostile.v3.history(
                    length, hostile.physical.ROUGH, rough_root, retain_terminal=False
                )
                evidence.history("rough", rough)
                hostile.v3.remove_resolution(rough_root)
                sharp = hostile.v3.history(
                    length, hostile.physical.SHARP, sharp_root, retain_terminal=True
                )
                evidence.history("sharp", sharp)
                pool.assert_run_complete()
                comparison = hostile.physical.compare(length, rough, sharp)
                diagnostic = persist_hostile_before_gate(
                    evidence, length, rough, sharp, comparison
                )
            resource = pool.resource_record()
    finally:
        hostile.physical.L12_WALL_LIMIT = original_physical_wall
        hostile.v3.WALL_LIMIT = original_engine_wall
    return rough, sharp, comparison, diagnostic, resource


def deadline_from_now(seconds: float = HARD_WALL_LIMIT_SECONDS) -> float:
    if not isinstance(seconds, float) or not 0.0 < seconds <= HARD_WALL_LIMIT_SECONDS:
        raise ValueError("seconds must be a positive float within 96 hours")
    return time.monotonic() + seconds

