#!/usr/bin/env python3
"""Deterministic L14 numerical reservations and bounded submission.

This is an execution-only successor.  It does not inspect live RSS, CPU, or
host memory and it does not alter any Hamiltonian, tolerance, or convergence
predicate.  Each task receives a conservative q-specific reservation and the
parent submits work only while the sum of live reservations fits the declared
one-node numerical budget.
"""

from __future__ import annotations

import concurrent.futures
import math
from collections import deque
from typing import Any, Callable, Iterable, Mapping, TypeVar


LENGTH = 14
COMPLEX128_BYTES = 16
DECLARED_INSTANCE_MEMORY_MIB = 1_572_864
NUMERICAL_MEMORY_PERCENT = 55
NUMERICAL_RESERVATION_BUDGET_BYTES = (
    DECLARED_INSTANCE_MEMORY_MIB * 2**20 * NUMERICAL_MEMORY_PERCENT // 100
)
BASE_WORKSPACE_BYTES = 2_400_000_000
HOSTILE_ALLOCATION_VECTOR_SLOTS = 20
TARGET_MAX_KRYLOV_DEPTH = 96
TARGET_WORKING_VECTOR_SLOTS = 4
TARGET_MINIMUM_LIVE_VECTORS = (
    TARGET_MAX_KRYLOV_DEPTH + TARGET_WORKING_VECTOR_SLOTS
)

T = TypeVar("T")
R = TypeVar("R")


def sector_columns(q: int) -> int:
    if type(q) is not int or not 0 <= q <= LENGTH:
        raise ValueError("L14 sector q must be in [0, 14]")
    return math.comb(2 * LENGTH, q)


def q_from_columns(columns: int) -> int:
    if type(columns) is not int or columns < 1:
        raise ValueError("sector columns must be a positive integer")
    for q in range(LENGTH + 1):
        if sector_columns(q) == columns:
            return q
    raise ValueError("columns are not an L14 q-sector dimension")


def hostile_workspace_bytes(q: int) -> int:
    one_row = HOSTILE_ALLOCATION_VECTOR_SLOTS * COMPLEX128_BYTES * sector_columns(q)
    return max(BASE_WORKSPACE_BYTES, one_row)


def target_workspace_bytes(q: int) -> int:
    one_row = TARGET_MINIMUM_LIVE_VECTORS * COMPLEX128_BYTES * sector_columns(q)
    return max(BASE_WORKSPACE_BYTES, one_row)


MAX_HOSTILE_WORKSPACE_BYTES = hostile_workspace_bytes(LENGTH)
MAX_TARGET_WORKSPACE_BYTES = target_workspace_bytes(LENGTH)


def hostile_batch_rows_l14(
    columns: int, degree: int, amplitude_window: int | None = None
) -> int:
    """Return a q-aware recurrence window; no independent row-size gate."""

    del degree, amplitude_window
    q = q_from_columns(columns)
    one_row = HOSTILE_ALLOCATION_VECTOR_SLOTS * COMPLEX128_BYTES * columns
    return max(1, hostile_workspace_bytes(q) // one_row)


def target_batch_rows_l14(columns: int, resolution: Any, force_low: bool) -> int:
    """Return a q-aware Lanczos window; capacity is the sole row bound."""

    q = q_from_columns(columns)
    depth = min(max(resolution.checkpoints), 20) if force_low else max(resolution.checkpoints)
    one_row = (depth + 4) * COMPLEX128_BYTES * columns
    workspace = target_workspace_bytes(q)
    if one_row > workspace:
        raise ValueError(
            "target workspace cannot hold one complete Krylov row: "
            "q={} required_bytes={} reserved_bytes={}".format(q, one_row, workspace)
        )
    return max(1, workspace // one_row)


def task_q(branch: str, task: Mapping[str, Any]) -> int:
    if branch not in {"target", "hostile"}:
        raise ValueError("branch must be target or hostile")
    if "q" in task:
        q = int(task["q"])
    elif "out_q" in task:
        q = int(task["out_q"])
    elif branch == "target" and "source_q" in task:
        q = int(task["source_q"])
        if task.get("phase") == "child1":
            q += 1
    else:
        # Unknown metadata is charged at the largest L14 sector rather than
        # admitted without a reservation.
        q = LENGTH
    if not 0 <= q <= LENGTH:
        raise ValueError("task q is outside the L14 sector census")
    return q


def task_reservation_bytes(branch: str, task: Mapping[str, Any]) -> int:
    q = task_q(branch, task)
    return target_workspace_bytes(q) if branch == "target" else hostile_workspace_bytes(q)


def make_bounded_pool_type(runtime: Any) -> type:
    """Build a V003 parent pool over the preserved spawn implementation."""

    class DeterministicBoundedPool(runtime.BranchProcessPool):
        def __init__(
            self,
            *,
            reservation_budget_bytes: int = NUMERICAL_RESERVATION_BUDGET_BYTES,
            **kwargs: Any,
        ) -> None:
            if type(reservation_budget_bytes) is not int or reservation_budget_bytes < 1:
                raise ValueError("reservation budget must be a positive integer")
            self.reservation_budget_bytes = reservation_budget_bytes
            self.peak_reserved_bytes = 0
            super().__init__(**kwargs)

        def map_ordered(
            self,
            function: Callable[[T], R],
            tasks: Iterable[T],
            *,
            stage: str,
            charge_sectors: int,
            row_windows: int,
            work_units: Iterable[int],
        ) -> list[R]:
            if self._closed or self._stop.is_set():
                raise runtime.ParallelRefusal("parallel L14 pool is closing")
            materialized = list(tasks)
            materialized_work = list(work_units)
            if len(materialized_work) != len(materialized) or any(
                type(value) is not int or value < 0 for value in materialized_work
            ):
                raise runtime.ParallelRefusal("parent work-unit census does not match tasks")
            reservations = []
            for task in materialized:
                if not isinstance(task, Mapping):
                    raise runtime.ParallelRefusal("L14 task metadata is not a mapping")
                reservation = task_reservation_bytes(self.branch, task)
                if reservation > self.reservation_budget_bytes:
                    raise runtime.ParallelRefusal("one L14 task exceeds the declared reservation budget")
                reservations.append(reservation)
            self._submitted_any = True
            progress = runtime.ParentProgress(
                branch=self.branch,
                stage=stage,
                total_tasks=len(materialized),
                charge_sectors=charge_sectors,
                row_windows=row_windows,
                total_work_units=sum(materialized_work),
            )
            if not materialized:
                return []
            # Preserve the reviewed heavy-first ordering, but create futures
            # only when both a worker slot and a numerical reservation exist.
            waiting = deque(sorted(
                (
                    (index, task, materialized_work[index], reservations[index])
                    for index, task in enumerate(materialized)
                ),
                key=lambda row: (-row[2], row[0]),
            ))
            pending: dict[Any, tuple[int, int, int]] = {}
            results_by_index: dict[int, R] = {}
            reserved = 0
            try:
                while waiting or pending:
                    while waiting and len(pending) < self.max_workers:
                        index, task, work, reservation = waiting[0]
                        if pending and reserved + reservation > self.reservation_budget_bytes:
                            break
                        waiting.popleft()
                        future = self._executor.submit(function, task)
                        pending[future] = (index, work, reservation)
                        reserved += reservation
                        self.peak_reserved_bytes = max(self.peak_reserved_bytes, reserved)
                    if not pending:
                        raise runtime.ParallelRefusal("L14 reservation scheduler made no progress")
                    done, _not_done = concurrent.futures.wait(
                        tuple(pending), return_when=concurrent.futures.FIRST_COMPLETED
                    )
                    completed_work = 0
                    for future in done:
                        index, work, reservation = pending.pop(future)
                        reserved -= reservation
                        results_by_index[index] = future.result()
                        completed_work += work
                    self._observe_children()
                    progress.advance(len(done), completed_work)
                    if self._run_progress is not None:
                        self._run_progress.advance(len(done), completed_work)
                    if self._stop.is_set():
                        raise runtime.ParallelRefusal("parallel L14 stop requested")
                return [results_by_index[index] for index in range(len(materialized))]
            except BaseException as error:
                for future in pending:
                    future.cancel()
                self.emit_stop_snapshot(type(error).__name__)
                self.request_stop(terminate_running=True)
                raise

        @property
        def concurrent_numerical_workset_bytes(self) -> int:
            return self.peak_reserved_bytes

        def resource_record(self) -> dict[str, Any]:
            record = super().resource_record()
            record.update({
                "reservation_policy": "DETERMINISTIC_Q_AWARE_BOUNDED_SUBMISSION",
                "reservation_budget_bytes": self.reservation_budget_bytes,
                "peak_reserved_bytes": self.peak_reserved_bytes,
                "live_rss_or_hardware_polling": False,
                "automatic_wall_time_cancellation": False,
            })
            return record

    return DeterministicBoundedPool
