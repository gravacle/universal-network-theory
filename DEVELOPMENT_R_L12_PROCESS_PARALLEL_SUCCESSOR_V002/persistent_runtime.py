#!/usr/bin/env python3
"""V002 process pool with durable parent-side task checkpoints."""

from __future__ import annotations

import concurrent.futures
import time
from typing import Any, Callable, Iterable, TypeVar

from evidence import EvidenceJournal
from v001_bridge import parallel_runtime as runtime


T = TypeVar("T")
R = TypeVar("R")


class PersistentBranchProcessPool(runtime.BranchProcessPool):
    """Preserve denominator and each parent completion batch before reduction."""

    def __init__(self, *, evidence: EvidenceJournal, **kwargs: Any) -> None:
        self.evidence = evidence
        super().__init__(**kwargs)

    def set_run_plan(
        self,
        *,
        total_tasks: int,
        charge_sectors: int,
        row_windows: int,
        total_work_units: int,
    ) -> None:
        super().set_run_plan(
            total_tasks=total_tasks,
            charge_sectors=charge_sectors,
            row_windows=row_windows,
            total_work_units=total_work_units,
        )
        self.evidence.progress(
            "RUN_DENOMINATOR",
            self._run_progress.progress.snapshot(),
        )

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
            raise runtime.ParallelRefusal("parallel L12 pool is closing")
        materialized = list(tasks)
        materialized_work = list(work_units)
        if len(materialized_work) != len(materialized) or any(
            type(value) is not int or value < 0 for value in materialized_work
        ):
            raise runtime.ParallelRefusal(
                "parent work-unit census does not match tasks"
            )
        self._submitted_any = True
        progress = runtime.ParentProgress(
            branch=self.branch,
            stage=stage,
            total_tasks=len(materialized),
            charge_sectors=charge_sectors,
            row_windows=row_windows,
            total_work_units=sum(materialized_work),
        )
        self.evidence.progress(
            "STAGE_START",
            {"stage_progress": progress.snapshot(), "completed_task_indices": []},
        )
        if not materialized:
            return []
        submission = sorted(
            enumerate(zip(materialized, materialized_work)),
            key=lambda row: (-row[1][1], row[0]),
        )
        future_rows = [
            (index, self._executor.submit(function, task), work)
            for index, (task, work) in submission
        ]
        futures = [row[1] for row in future_rows]
        work_by_future = {future: work for _index, future, work in future_rows}
        index_by_future = {future: index for index, future, _work in future_rows}
        try:
            pending = set(futures)
            while pending:
                if self._stop.is_set():
                    raise runtime.ParallelRefusal("parallel L12 stop requested")
                remaining = self.deadline_monotonic - time.monotonic()
                if remaining <= 0.0:
                    raise TimeoutError("parallel L12 branch deadline exceeded")
                done, pending = concurrent.futures.wait(
                    pending,
                    timeout=min(1.0, remaining),
                    return_when=concurrent.futures.FIRST_COMPLETED,
                )
                for future in done:
                    exception = future.exception()
                    if exception is not None:
                        raise exception
                if done:
                    self._observe_children()
                    completed_work = sum(work_by_future[future] for future in done)
                    progress.advance(len(done), completed_work)
                    if self._run_progress is not None:
                        self._run_progress.advance(len(done), completed_work)
                    self.evidence.progress(
                        "TASK_BATCH_COMPLETE",
                        {
                            "stage": stage,
                            "completed_task_indices": sorted(
                                index_by_future[future] for future in done
                            ),
                            "stage_progress": progress.snapshot(),
                            "run_progress": (
                                self._run_progress.progress.snapshot()
                                if self._run_progress is not None
                                else None
                            ),
                        },
                    )
            results_by_index = {
                index: future.result() for index, future, _work in future_rows
            }
            results = [results_by_index[index] for index in range(len(materialized))]
            self.evidence.progress(
                "STAGE_COMPLETE",
                {"stage_progress": progress.snapshot()},
            )
            return results
        except BaseException as error:
            for future in futures:
                future.cancel()
            self.evidence.progress(
                "STAGE_FAILURE",
                {
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "stage_progress": progress.snapshot(),
                    "run_progress": (
                        self._run_progress.progress.snapshot()
                        if self._run_progress is not None
                        else None
                    ),
                },
            )
            self.emit_stop_snapshot(type(error).__name__)
            self.request_stop(terminate_running=True)
            raise

    def assert_run_complete(self) -> None:
        super().assert_run_complete()
        self.evidence.progress(
            "RUN_COMPLETE",
            self._run_progress.progress.snapshot(),
        )

