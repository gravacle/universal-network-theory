#!/usr/bin/env python3
"""Equivalence and process-topology tests for the L12 parallel successor."""

from __future__ import annotations

import io
import json
import math
import tempfile
import time
import unittest
import warnings
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

import numpy as np

import hostile_parallel
import launch_config
import parallel_runtime
import target_parallel


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
warnings.filterwarnings("ignore", category=ResourceWarning)


def assert_numeric_close(
    case: unittest.TestCase, observed: Any, expected: Any, tolerance: float = 2.0e-12
) -> None:
    if isinstance(expected, np.ndarray):
        np.testing.assert_allclose(observed, expected, atol=tolerance, rtol=tolerance)
    elif isinstance(expected, dict):
        case.assertEqual(set(observed), set(expected))
        for key in expected:
            assert_numeric_close(case, observed[key], expected[key], tolerance)
    elif isinstance(expected, tuple):
        case.assertEqual(len(observed), len(expected))
        for left, right in zip(observed, expected):
            assert_numeric_close(case, left, right, tolerance)
    elif type(expected) is float:
        case.assertAlmostEqual(float(observed), expected, delta=tolerance)
    else:
        case.assertEqual(observed, expected)


class ParallelSuccessorTests(unittest.TestCase):
    def test_exact_l12_denominator_and_parent_eta(self) -> None:
        self.assertEqual(
            target_parallel.target_run_plan(12),
            {
                "total_tasks": 4714,
                "charge_sectors": 488,
                "row_windows": 4560,
                "total_work_units": 274_768_288_592,
            },
        )
        self.assertEqual(
            hostile_parallel.hostile_run_plan(12),
            {
                "total_tasks": 1670,
                "charge_sectors": 512,
                "row_windows": 1516,
                "total_work_units": 431_778_739_216,
            },
        )
        output = io.StringIO()
        with redirect_stdout(output):
            progress = parallel_runtime.ParentProgress(
                branch="target",
                stage="telemetry_test",
                total_tasks=2,
                charge_sectors=1,
                row_windows=1,
                total_work_units=100,
            )
            progress.advance(1, 0)
            progress.advance(1, 100)
        lines = output.getvalue().splitlines()
        self.assertIn("total_tasks=2 charge_sectors=1 row_windows=1", lines[0])
        self.assertIn("completed=1 total=2", lines[1])
        self.assertIn("eta=unknown", lines[1])
        self.assertIn("completed=2 total=2", lines[2])
        self.assertTrue(progress.snapshot()["complete"])

    def test_parent_stop_snapshot_reports_exact_remainder(self) -> None:
        output = io.StringIO()
        pool = object.__new__(parallel_runtime.BranchProcessPool)
        pool.branch = "target"
        pool._stop_snapshot_emitted = False
        pool._run_progress = parallel_runtime.ParentRunProgress(
            branch="target",
            total_tasks=10,
            charge_sectors=4,
            row_windows=6,
            total_work_units=1000,
        )
        pool._run_progress.advance(3, 400)
        with redirect_stdout(output):
            pool.emit_stop_snapshot("test_ceiling")
            pool.emit_stop_snapshot("duplicate")
        record = output.getvalue().splitlines()
        self.assertEqual(len(record), 1)
        self.assertIn("reason=test_ceiling", record[0])
        self.assertIn("completed=3 remaining=7", record[0])
        self.assertIn("completed_solver_cell_steps=400", record[0])
        self.assertIn("remaining_solver_cell_steps=600", record[0])

    def test_dual_branch_worker_budget(self) -> None:
        ram = 51_539_607_552
        self.assertEqual(
            parallel_runtime.recommended_branch_workers(
                branch="target", cpu_count=14, memory_bytes=ram
            ),
            7,
        )
        self.assertEqual(
            parallel_runtime.recommended_branch_workers(
                branch="hostile", cpu_count=14, memory_bytes=ram
            ),
            7,
        )
        self.assertEqual(
            parallel_runtime.CONFIGURED_WORKERS_BY_BRANCH,
            {"target": 7, "hostile": 7},
        )
        self.assertEqual(parallel_runtime.CONFIGURED_TOTAL_WORKERS, 14)
        self.assertEqual(parallel_runtime.HARD_WALL_LIMIT_SECONDS, 345_600.0)
        allocation = launch_config.allocation_record()
        self.assertEqual(allocation["hard_wall_limit_hours"], 96)
        self.assertEqual(allocation["total_numerical_workers"], 14)
        self.assertTrue(allocation["candidate_paths_absent"])

    def test_target_l4_terminal_matches_serial(self) -> None:
        target = target_parallel.target
        cache_root = (
            ROOT
            / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
            / "CACHE_PAYLOADS_V012/L4"
        ).resolve()
        manifest_hash = parallel_runtime.sha256_file(cache_root / "CACHE_MANIFEST.json")
        before = (
            ROOT
            / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
            / "WORKSPACES/L4/sharp/prefix_03"
        ).resolve()
        context = target.CacheContext(cache_root, 4, manifest_hash)
        original_cache = target.CACHE
        original_words = target.v004.sealed.fixed_words
        original_sector = target.v004.sealed.Sector
        try:
            target.CACHE = context
            target.v004.sealed.fixed_words = target.cached_fixed_words
            target.v004.sealed.Sector = target.CachedSector
            serial = target.cached_terminal_stream(
                4, before, 3, 3, target.v004.sealed.FINE
            )
        finally:
            target.v004.sealed.fixed_words = original_words
            target.v004.sealed.Sector = original_sector
            target.CACHE = original_cache
            context.close()
        with parallel_runtime.BranchProcessPool(
            branch="target",
            cache_root=cache_root,
            manifest_sha256=manifest_hash,
            length=4,
            deadline_monotonic=time.monotonic() + 300.0,
            max_workers=parallel_runtime.CONFIGURED_WORKERS_BY_BRANCH["target"],
        ) as pool:
            parallel = target_parallel.TargetParallelAdapter(pool).terminal_stream(
                4, before, 3, 3, target.v004.sealed.FINE
            )
            self.assertEqual(len(pool.child_pids), 7)
        assert_numeric_close(self, parallel, serial)

    def test_target_l4_full_rough_history_matches_serial(self) -> None:
        target = target_parallel.target
        cache_root = (
            ROOT
            / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
            / "CACHE_PAYLOADS_V012/L4"
        ).resolve()
        manifest_hash = parallel_runtime.sha256_file(cache_root / "CACHE_MANIFEST.json")
        context = target.CacheContext(cache_root, 4, manifest_hash)
        original_cache = target.CACHE
        original_words = target.v004.sealed.fixed_words
        original_sector = target.v004.sealed.Sector
        original_create = target.v004.create_admitted
        original_terminal = target.v004.terminal_stream
        original_route = target.v004.route_pair
        try:
            target.CACHE = context
            target.v004.sealed.fixed_words = target.cached_fixed_words
            target.v004.sealed.Sector = target.CachedSector
            target.v004.create_admitted = target.cached_create_admitted
            target.v004.terminal_stream = target.cached_terminal_stream
            with tempfile.TemporaryDirectory(prefix="l12-target-history-") as temporary:
                base = Path(temporary).resolve()
                serial = target.v004.history(
                    4, target.v004.sealed.COARSE, base / "serial", False
                )
                with parallel_runtime.BranchProcessPool(
                    branch="target",
                    cache_root=cache_root,
                    manifest_sha256=manifest_hash,
                    length=4,
                    deadline_monotonic=time.monotonic() + 300.0,
                    max_workers=2,
                ) as pool:
                    with target_parallel.TargetParallelAdapter(pool):
                        parallel = target.v004.history(
                            4, target.v004.sealed.COARSE, base / "parallel", False
                        )
                assert_numeric_close(self, parallel, serial)
        finally:
            target.v004.route_pair = original_route
            target.v004.create_admitted = original_create
            target.v004.terminal_stream = original_terminal
            target.v004.sealed.fixed_words = original_words
            target.v004.sealed.Sector = original_sector
            target.CACHE = original_cache
            context.close()

    def test_hostile_l4_terminal_matches_serial(self) -> None:
        hostile = hostile_parallel.hostile
        cache_root = (
            ROOT
            / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
            / "V004R4_CACHE_PAYLOADS/L4"
        ).resolve()
        manifest_path = cache_root / "CACHE_MANIFEST.json"
        manifest_hash = parallel_runtime.sha256_file(manifest_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source_hashes = {
            role: manifest[f"{role}_sha256"]
            for role in ("method", "builder", "consumer", "preflight")
        }
        with tempfile.TemporaryDirectory(prefix="l12-hostile-l4-") as temporary:
            state_root = Path(temporary).resolve()
            hostile.v3.LENGTH = 4
            state = hostile.v3.DiskPrefix(state_root, 3)
            state.create()
            rng = np.random.default_rng(4012)
            norm_squared = 0.0
            for q in range(4):
                shard = state.create_shard(q)
                shard[:] = rng.normal(size=shard.shape) + 1.0j * rng.normal(
                    size=shard.shape
                )
                norm_squared += float(np.vdot(shard, shard).real)
                hostile.v3.close_memmap(shard, write=True)
            scale = math.sqrt(norm_squared)
            for q in range(4):
                shard = state.open_shard(q, "r+")
                shard[:] /= scale
                hostile.v3.close_memmap(shard, write=True)
            started = time.perf_counter()
            context = hostile.CacheContext(
                4, cache_root, manifest, manifest_hash, source_hashes, started
            )
            try:
                hostile.legacy.configure(4, context, started)
                serial = hostile.legacy.cached_terminal_route(
                    state, hostile.physical.SHARP, hostile.physical.hostile_edges(4)
                )
            finally:
                hostile.legacy.CACHE = None
                hostile.v3.EXECUTION_STARTED = None
                context.close()
            with parallel_runtime.BranchProcessPool(
                branch="hostile",
                cache_root=cache_root,
                manifest_sha256=manifest_hash,
                length=4,
                deadline_monotonic=time.monotonic() + 300.0,
                max_workers=parallel_runtime.CONFIGURED_WORKERS_BY_BRANCH["hostile"],
            ) as pool:
                parallel = hostile_parallel.HostileParallelAdapter(pool).terminal_route(
                    state, hostile.physical.SHARP, hostile.physical.hostile_edges(4)
                )
                self.assertEqual(len(pool.child_pids), 7)
            assert_numeric_close(self, parallel, serial)

    def test_hostile_l4_full_rough_history_matches_serial(self) -> None:
        hostile = hostile_parallel.hostile
        cache_root = (
            ROOT
            / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
            / "V004R4_CACHE_PAYLOADS/L4"
        ).resolve()
        manifest_path = cache_root / "CACHE_MANIFEST.json"
        manifest_hash = parallel_runtime.sha256_file(manifest_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source_hashes = {
            role: manifest[f"{role}_sha256"]
            for role in ("method", "builder", "consumer", "preflight")
        }
        context = hostile.CacheContext(
            4, cache_root, manifest, manifest_hash, source_hashes, time.perf_counter()
        )
        originals = (
            hostile.v3.route_disk_state,
            hostile.v3.admit_to_next,
            hostile.v3.terminal_route,
        )
        try:
            hostile.legacy.configure(4, context, time.perf_counter())
            with tempfile.TemporaryDirectory(prefix="l12-hostile-history-") as temporary:
                base = Path(temporary).resolve()
                serial = hostile.v3.history(
                    4, hostile.physical.ROUGH, base / "serial", False
                )
                hostile.legacy.configure(4, context, time.perf_counter())
                with parallel_runtime.BranchProcessPool(
                    branch="hostile",
                    cache_root=cache_root,
                    manifest_sha256=manifest_hash,
                    length=4,
                    deadline_monotonic=time.monotonic() + 300.0,
                    max_workers=2,
                ) as pool:
                    with hostile_parallel.HostileParallelAdapter(pool):
                        parallel = hostile.v3.history(
                            4, hostile.physical.ROUGH, base / "parallel", False
                        )
                assert_numeric_close(self, parallel, serial)
        finally:
            (
                hostile.v3.route_disk_state,
                hostile.v3.admit_to_next,
                hostile.v3.terminal_route,
            ) = originals
            hostile.legacy.CACHE = None
            hostile.v3.EXECUTION_STARTED = None
            context.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
