#!/usr/bin/env python3
"""Narrow V003 numerical-capacity successor for the L12 history kernels.

The physical graph, Hamiltonian, admission angle, route time, observables,
quadrature rules, and convergence tolerances are inherited unchanged.  V003
only extends the endpoint approximation capacity and the low-memory
subdivision ceiling.  The worker entry points install those settings inside
spawned processes before delegating to the reviewed V001 process kernels.
"""

from __future__ import annotations

import math
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V002 = ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V002"
if str(V002) not in sys.path:
    sys.path.append(str(V002))

from v001_bridge import hostile, hostile_parallel, target, target_parallel  # noqa: E402


TARGET_MAX_SUBDIVISIONS = 256
TARGET_COARSE = target.v004.sealed.Resolution(
    "coarse", (12, 18, 24, 32, 48, 64, 80), 16, 2.0e-9
)
TARGET_FINE = target.v004.sealed.Resolution(
    "fine", (16, 24, 32, 48, 64, 80, 96), 24, 5.0e-11
)
HOSTILE_ROUGH = hostile.physical.Accuracy(
    "rough", (16, 24, 32, 48, 64, 80, 96, 112), 18, 3.0e-9
)
HOSTILE_SHARP = hostile.physical.Accuracy(
    "sharp", (24, 32, 48, 64, 80, 96, 112, 128), 28, 8.0e-11
)


_TARGET_ROUTE_V001 = target_parallel.target_route_worker
_TARGET_TERMINAL_V001 = target_parallel.target_terminal_worker
_HOSTILE_ROUTE_V001 = hostile_parallel.hostile_route_worker
_HOSTILE_TERMINAL_V001 = hostile_parallel.hostile_terminal_worker


def install_target_capacity() -> None:
    target.v004.sealed.COARSE = TARGET_COARSE
    target.v004.sealed.FINE = TARGET_FINE
    target.v004.v3.MAX_SUBDIVISIONS = TARGET_MAX_SUBDIVISIONS


def install_hostile_capacity() -> None:
    hostile.physical.ROUGH = HOSTILE_ROUGH
    hostile.physical.SHARP = HOSTILE_SHARP


def target_route_worker_v003(task: dict[str, Any]) -> dict[str, Any]:
    install_target_capacity()
    return _TARGET_ROUTE_V001(task)


def target_terminal_worker_v003(task: dict[str, Any]) -> dict[str, Any]:
    install_target_capacity()
    return _TARGET_TERMINAL_V001(task)


def hostile_route_worker_v003(task: dict[str, Any]) -> dict[str, Any]:
    install_hostile_capacity()
    return _HOSTILE_ROUTE_V001(task)


def hostile_terminal_worker_v003(task: dict[str, Any]) -> dict[str, Any]:
    install_hostile_capacity()
    return _HOSTILE_TERMINAL_V001(task)


def _target_plan(length: int) -> dict[str, int]:
    admission = sectors = windows = work = 0
    for resolution in (TARGET_COARSE, TARGET_FINE):
        depth = max(resolution.checkpoints)
        for event in range(length - 1):
            admission += event + 2
            sectors += event + 2
            for prefix in (event + 1, event):
                for q in range(prefix + 1):
                    sectors += 1
                    rows = math.comb(prefix, q)
                    columns = math.comb(2 * length, q)
                    step = target.v004.v3.batch_rows(columns, resolution, False)
                    count = math.ceil(rows / step)
                    windows += count
                    work += rows * columns * depth
        prefix = length - 1
        for q in range(length):
            rows = math.comb(prefix, q)
            sectors += 2
            columns = math.comb(2 * length, q)
            step = target.v004.v3.batch_rows(columns, resolution, False)
            windows += math.ceil(rows / step)
            work += 2 * rows * columns * depth
            columns = math.comb(2 * length, q + 1)
            step = target.v004.v3.batch_rows(columns, resolution, False)
            windows += math.ceil(rows / step)
            work += rows * columns * depth
    return {
        "total_tasks": admission + windows,
        "charge_sectors": sectors,
        "row_windows": windows,
        "total_work_units": work,
    }


def _hostile_rough_plan(length: int) -> dict[str, int]:
    admission = sectors = windows = work = 0
    accuracy = HOSTILE_ROUGH
    depth = max(accuracy.checkpoints)
    for event in range(length - 1):
        admission += event + 2
        sectors += event + 2
        for prefix in (event + 1, event):
            for q in range(prefix + 1):
                sectors += 1
                rows = math.comb(prefix, q)
                columns = math.comb(2 * length, q)
                step = hostile.legacy.replay.safe_batch_rows(columns, depth)
                windows += math.ceil(rows / step)
                work += rows * columns * depth
    prefix = length - 1
    for phase, q_range in (
        ("child0", range(length)),
        ("child1", range(1, length + 1)),
        ("null", range(length)),
    ):
        for q in q_range:
            source_q = q - 1 if phase == "child1" else q
            rows = math.comb(prefix, source_q)
            columns = math.comb(2 * length, q)
            step = hostile.legacy.replay.safe_batch_rows(
                columns, depth, hostile.physical.TERMINAL_WINDOW_BYTES
            )
            sectors += 1
            windows += math.ceil(rows / step)
            work += rows * columns * depth
    return {
        "total_tasks": admission + windows,
        "charge_sectors": sectors,
        "row_windows": windows,
        "total_work_units": work,
    }


def _hostile_sharp_terminal_plan(length: int) -> dict[str, int]:
    sectors = windows = work = 0
    accuracy = HOSTILE_SHARP
    depth = max(accuracy.checkpoints)
    prefix = length - 1
    for phase, q_range in (
        ("child0", range(length)),
        ("child1", range(1, length + 1)),
        ("null", range(length)),
    ):
        for q in q_range:
            source_q = q - 1 if phase == "child1" else q
            rows = math.comb(prefix, source_q)
            columns = math.comb(2 * length, q)
            step = hostile.legacy.replay.safe_batch_rows(
                columns, depth, hostile.physical.TERMINAL_WINDOW_BYTES
            )
            sectors += 1
            windows += math.ceil(rows / step)
            work += rows * columns * depth
    return {
        "total_tasks": windows,
        "charge_sectors": sectors,
        "row_windows": windows,
        "total_work_units": work,
    }


def target_repair_plan(length: int = 12) -> dict[str, int]:
    install_target_capacity()
    return _target_plan(length)


def hostile_repair_plan(length: int = 12) -> dict[str, int]:
    install_hostile_capacity()
    rough = _hostile_rough_plan(length)
    terminal = _hostile_sharp_terminal_plan(length)
    return {key: rough[key] + terminal[key] for key in rough}


class TargetRepairAdapter(target_parallel.TargetParallelAdapter):
    """Full Target rough+sharp replay with the V003 capacities."""

    def __init__(self, pool: Any):
        if pool.branch != "target":
            raise ValueError("target adapter requires target branch pool")
        self.pool = pool
        self._originals = None
        pool.set_run_plan(**target_repair_plan(pool.length))


class HostileRepairAdapter(hostile_parallel.HostileParallelAdapter):
    """Hostile rough replay plus sharp terminal suffix replay."""

    def __init__(self, pool: Any):
        if pool.branch != "hostile":
            raise ValueError("hostile adapter requires hostile branch pool")
        self.pool = pool
        self._originals = None
        pool.set_run_plan(**hostile_repair_plan(pool.length))


@contextmanager
def target_capacity_scope() -> Iterator[None]:
    old = (
        target.v004.sealed.COARSE,
        target.v004.sealed.FINE,
        target.v004.v3.MAX_SUBDIVISIONS,
        target_parallel.target_route_worker,
        target_parallel.target_terminal_worker,
    )
    install_target_capacity()
    target_parallel.target_route_worker = target_route_worker_v003
    target_parallel.target_terminal_worker = target_terminal_worker_v003
    try:
        yield
    finally:
        (
            target.v004.sealed.COARSE,
            target.v004.sealed.FINE,
            target.v004.v3.MAX_SUBDIVISIONS,
            target_parallel.target_route_worker,
            target_parallel.target_terminal_worker,
        ) = old


@contextmanager
def hostile_capacity_scope() -> Iterator[None]:
    old = (
        hostile.physical.ROUGH,
        hostile.physical.SHARP,
        hostile_parallel.hostile_route_worker,
        hostile_parallel.hostile_terminal_worker,
    )
    install_hostile_capacity()
    hostile_parallel.hostile_route_worker = hostile_route_worker_v003
    hostile_parallel.hostile_terminal_worker = hostile_terminal_worker_v003
    try:
        yield
    finally:
        (
            hostile.physical.ROUGH,
            hostile.physical.SHARP,
            hostile_parallel.hostile_route_worker,
            hostile_parallel.hostile_terminal_worker,
        ) = old
