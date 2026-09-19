#!/usr/bin/env python3
"""Spawn-only process runtime for the L12 target and hostile successors.

The runtime deliberately transports metadata, never amplitude arrays.  Each
child reopens read-only cache/state mappings and returns only small numerical
reductions.  The caller owns all state-directory creation, graph mutation,
ordered reduction, authentication, and publication.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import math
import multiprocessing
import os
import signal
import stat
import threading
import time
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar

import numpy as np


THREAD_LIMIT_ENV = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)

TARGET_WORKSET_BYTES = 1_000_000_000
HOSTILE_WORKSET_BYTES = 1_400_000_000
DEFAULT_MEMORY_FRACTION = 0.55
HARD_WALL_LIMIT_SECONDS = 96 * 3600.0
CONFIGURED_WORKERS_BY_BRANCH = {"target": 7, "hostile": 7}
CONFIGURED_TOTAL_WORKERS = sum(CONFIGURED_WORKERS_BY_BRANCH.values())


class ParallelRefusal(RuntimeError):
    """A fail-closed process, cache, deadline, or reduction check failed."""


class GracefulTermination(SystemExit):
    """The parent received a termination request and stopped publication."""


def configure_single_thread_math() -> None:
    """Prevent a process pool from nesting BLAS/OpenMP thread pools."""
    for name in THREAD_LIMIT_ENV:
        os.environ[name] = "1"


def physical_memory_bytes() -> int | None:
    """Return installed RAM without adding a third-party dependency."""
    try:
        page_size = os.sysconf("SC_PAGE_SIZE")
        pages = os.sysconf("SC_PHYS_PAGES")
    except (AttributeError, OSError, ValueError):
        return None
    if type(page_size) is int and type(pages) is int and page_size > 0 and pages > 0:
        return page_size * pages
    return None


def recommended_branch_workers(
    *,
    branch: str,
    concurrent_branches: int = 2,
    cpu_count: int | None = None,
    memory_bytes: int | None = None,
    memory_fraction: float = DEFAULT_MEMORY_FRACTION,
) -> int:
    """Bound workers by both the dual-branch CPU split and RAM worksets."""
    if branch not in {"target", "hostile"}:
        raise ValueError("branch must be target or hostile")
    if type(concurrent_branches) is not int or concurrent_branches < 1:
        raise ValueError("concurrent_branches must be a positive integer")
    if not 0.0 < memory_fraction <= 1.0:
        raise ValueError("memory_fraction must be in (0, 1]")
    cores = cpu_count if cpu_count is not None else (os.cpu_count() or 1)
    if type(cores) is not int or cores < 1:
        raise ValueError("cpu_count must be a positive integer")
    ram = memory_bytes if memory_bytes is not None else physical_memory_bytes()
    cpu_bound = max(1, cores // concurrent_branches)
    if ram is None:
        return cpu_bound
    workset = TARGET_WORKSET_BYTES if branch == "target" else HOSTILE_WORKSET_BYTES
    # The memory allowance is also split between simultaneously running
    # target/hostile branches.  Immutable mappings share the OS page cache and
    # are not multiplied into this anonymous numerical-workset bound.
    memory_bound = max(
        1,
        int(ram * memory_fraction) // concurrent_branches // workset,
    )
    return max(1, min(cpu_bound, memory_bound))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(block)
    return digest.hexdigest()


def _identity(metadata: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
        metadata.st_mode,
        metadata.st_nlink,
    )


class ManifestMemmapCache:
    """Per-child, lazy, read-only view of a parent-authenticated cache.

    The parent remains responsible for full SHA-256 authentication before and
    after the pool.  Children bind the same manifest hash and stable inode
    identity, enforce immutable cache members, and map only arrays needed by
    their assigned charge/window.  This avoids pickling or copying the cache.
    """

    def __init__(self, root: str, manifest_sha256: str, branch: str, length: int):
        self.root = Path(root)
        self.branch = branch
        self.length = length
        if (
            not self.root.is_absolute()
            or self.root.is_symlink()
            or not self.root.is_dir()
            or branch not in {"target", "hostile"}
        ):
            raise ParallelRefusal("worker cache root/branch is not canonical")
        flags = (
            os.O_RDONLY
            | os.O_DIRECTORY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        self.root_fd = os.open(self.root, flags)
        opened_root = os.fstat(self.root_fd)
        current_root = os.stat(self.root, follow_symlinks=False)
        if (
            not stat.S_ISDIR(opened_root.st_mode)
            or opened_root.st_mode & 0o222
            or _identity(opened_root) != _identity(current_root)
        ):
            raise ParallelRefusal("worker cache root is not immutable/stable")
        self.root_identity = _identity(opened_root)
        manifest_path = self.root / "CACHE_MANIFEST.json"
        if sha256_file(manifest_path) != manifest_sha256:
            raise ParallelRefusal("worker cache manifest hash mismatch")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_schema = (
            "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012"
            if branch == "target"
            else "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4"
        )
        if manifest.get("schema") != expected_schema or manifest.get("L") != length:
            raise ParallelRefusal("worker cache manifest branch/length mismatch")
        rows = manifest.get("files")
        if not isinstance(rows, list):
            raise ParallelRefusal("worker cache file census absent")
        self.records: dict[str, dict[str, Any]] = {}
        for row in rows:
            if not isinstance(row, dict) or type(row.get("path")) is not str:
                raise ParallelRefusal("worker cache record malformed")
            name = row["path"]
            if Path(name).name != name or "/" in name or name in self.records:
                raise ParallelRefusal("worker cache member path is unsafe/duplicated")
            self.records[name] = row
        if set(os.listdir(self.root_fd)) != set(self.records) | {"CACHE_MANIFEST.json"}:
            raise ParallelRefusal("worker cache exact member census mismatch")

    def open(self, name: str, expected_dtype: np.dtype[Any] | str) -> np.ndarray:
        row = self.records.get(name)
        dtype = np.dtype(expected_dtype)
        if row is None or row.get("dtype") != dtype.str:
            raise ParallelRefusal(f"worker cache dtype record mismatch: {name}")
        raw_shape = row.get("shape")
        if (
            not isinstance(raw_shape, list)
            or any(type(axis) is not int or axis < 0 for axis in raw_shape)
        ):
            raise ParallelRefusal(f"worker cache shape record mismatch: {name}")
        shape = tuple(raw_shape)
        expected_bytes = math.prod(shape) * dtype.itemsize
        if type(row.get("bytes")) is not int or row["bytes"] != expected_bytes:
            raise ParallelRefusal(f"worker cache byte record mismatch: {name}")
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(name, flags, dir_fd=self.root_fd)
        try:
            opened = os.fstat(descriptor)
            current = os.stat(name, dir_fd=self.root_fd, follow_symlinks=False)
            if (
                not stat.S_ISREG(opened.st_mode)
                or opened.st_mode & 0o222
                or opened.st_nlink != 1
                or opened.st_size != expected_bytes
                or _identity(opened) != _identity(current)
            ):
                raise ParallelRefusal(f"worker cache member identity mismatch: {name}")
            if expected_bytes == 0:
                result = np.empty(shape, dtype=dtype)
                result.flags.writeable = False
                return result
            with os.fdopen(os.dup(descriptor), "rb", closefd=True) as stream:
                result = np.memmap(stream, dtype=dtype, mode="r", shape=shape)
            if result.flags.writeable or result.nbytes != expected_bytes:
                raise ParallelRefusal(f"worker cache mapping mismatch: {name}")
            return result
        finally:
            os.close(descriptor)

    def verify_root(self) -> None:
        opened = os.fstat(self.root_fd)
        current = os.stat(self.root, follow_symlinks=False)
        if (
            _identity(opened) != self.root_identity
            or _identity(current) != self.root_identity
            or set(os.listdir(self.root_fd)) != set(self.records) | {"CACHE_MANIFEST.json"}
        ):
            raise ParallelRefusal("worker cache root changed during task")

    def close(self) -> None:
        if getattr(self, "root_fd", -1) >= 0:
            os.close(self.root_fd)
            self.root_fd = -1


def close_mapping(array: np.ndarray, *, write: bool = False) -> None:
    if write and hasattr(array, "flush"):
        array.flush()
    mapping = getattr(array, "_mmap", None)
    if mapping is not None:
        try:
            mapping.close()
        except (BufferError, OSError):
            pass


@dataclass(frozen=True)
class WorkerConfig:
    branch: str
    cache_root: str
    manifest_sha256: str
    length: int
    deadline_monotonic: float


_WORKER_CONFIG: WorkerConfig | None = None
_WORKER_CACHE: ManifestMemmapCache | None = None


def initialize_worker(config: WorkerConfig) -> None:
    """Spawn initializer shared by both numerical adapters."""
    global _WORKER_CONFIG, _WORKER_CACHE
    configure_single_thread_math()
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    _WORKER_CONFIG = config
    _WORKER_CACHE = ManifestMemmapCache(
        config.cache_root, config.manifest_sha256, config.branch, config.length
    )


def worker_context(branch: str) -> tuple[WorkerConfig, ManifestMemmapCache]:
    if _WORKER_CONFIG is None or _WORKER_CACHE is None:
        raise ParallelRefusal("spawned worker context is absent")
    if _WORKER_CONFIG.branch != branch:
        raise ParallelRefusal("spawned worker branch mismatch")
    if time.monotonic() >= _WORKER_CONFIG.deadline_monotonic:
        raise TimeoutError("parallel L12 worker deadline exceeded")
    _WORKER_CACHE.verify_root()
    return _WORKER_CONFIG, _WORKER_CACHE


T = TypeVar("T")
R = TypeVar("R")


class ParentProgress:
    """Low-overhead rolling telemetry emitted only by the parent process."""

    def __init__(
        self,
        *,
        branch: str,
        stage: str,
        total_tasks: int,
        charge_sectors: int,
        row_windows: int,
        total_work_units: int,
    ) -> None:
        if min(total_tasks, charge_sectors, row_windows, total_work_units) < 0:
            raise ValueError("progress denominators cannot be negative")
        self.branch = branch
        self.stage = stage
        self.total = total_tasks
        self.charge_sectors = charge_sectors
        self.row_windows = row_windows
        self.completed = 0
        self.total_work_units = total_work_units
        self.completed_work_units = 0
        self.started = time.perf_counter()
        self.last_emit = self.started
        self.samples: deque[tuple[float, int, int]] = deque(maxlen=64)
        self.samples.append((self.started, 0, 0))
        print(
            "L12_PROGRESS_START "
            f"branch={branch} stage={stage} total_tasks={total_tasks} "
            f"charge_sectors={charge_sectors} row_windows={row_windows} "
            f"estimated_solver_cell_steps={total_work_units}",
            flush=True,
        )

    @staticmethod
    def _duration(seconds: float) -> str:
        if not math.isfinite(seconds) or seconds < 0.0:
            return "unknown"
        whole = int(seconds)
        hours, remainder = divmod(whole, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def advance(self, count: int = 1, work_units: int = 0) -> None:
        if (
            type(count) is not int
            or type(work_units) is not int
            or count < 0
            or work_units < 0
            or self.completed + count > self.total
            or self.completed_work_units + work_units > self.total_work_units
        ):
            raise ParallelRefusal("parent progress exceeded its declared denominator")
        self.completed += count
        self.completed_work_units += work_units
        now = time.perf_counter()
        self.samples.append((now, self.completed, self.completed_work_units))
        # Show the first few completions immediately so a ten-minute observer
        # gets an early rate.  Thereafter cap routine log volume at roughly one
        # line per five seconds, always emitting the terminal update.
        should_emit = (
            self.completed <= min(10, self.total)
            or self.completed == self.total
            or now - self.last_emit >= 5.0
        )
        if not should_emit:
            return
        self.last_emit = now
        elapsed = now - self.started
        first_time, first_count, first_work = self.samples[0]
        interval = now - first_time
        interval_done = self.completed - first_count
        rolling_rate = interval_done / interval if interval > 0.0 else 0.0
        overall_rate = self.completed / elapsed if elapsed > 0.0 else 0.0
        rate = rolling_rate if interval_done > 0 else overall_rate
        remaining = self.total - self.completed
        work_interval_done = self.completed_work_units - first_work
        work_rate = work_interval_done / interval if interval > 0.0 else 0.0
        work_remaining = self.total_work_units - self.completed_work_units
        if self.total_work_units > 0:
            # A task-rate ETA is actively misleading while only zero-work
            # admission tasks have completed.  Wait for at least one measured
            # numerical window, then project from weighted solver work.
            eta_seconds = (
                work_remaining / work_rate if work_rate > 0.0 else math.inf
            )
        else:
            eta_seconds = remaining / rate if rate > 0.0 else math.inf
        percent = 100.0 * self.completed / self.total if self.total else 100.0
        work_percent = (
            100.0 * self.completed_work_units / self.total_work_units
            if self.total_work_units else percent
        )
        print(
            "L12_PROGRESS "
            f"branch={self.branch} stage={self.stage} "
            f"completed={self.completed} total={self.total} percent={percent:.3f} "
            f"work_percent={work_percent:.3f} "
            f"elapsed={self._duration(elapsed)} eta={self._duration(eta_seconds)} "
            f"rolling_tasks_per_second={rate:.6g} "
            f"rolling_solver_cell_steps_per_second={work_rate:.6g}",
            flush=True,
        )

    def snapshot(self) -> dict[str, int | float | str | bool]:
        elapsed = time.perf_counter() - self.started
        return {
            "branch": self.branch,
            "stage": self.stage,
            "total_tasks": self.total,
            "completed_tasks": self.completed,
            "remaining_tasks": self.total - self.completed,
            "charge_sectors": self.charge_sectors,
            "row_windows": self.row_windows,
            "estimated_solver_cell_steps": self.total_work_units,
            "completed_solver_cell_steps": self.completed_work_units,
            "remaining_solver_cell_steps": (
                self.total_work_units - self.completed_work_units
            ),
            "elapsed_seconds": elapsed,
            "complete": (
                self.completed == self.total
                and self.completed_work_units == self.total_work_units
            ),
        }


class ParentRunProgress:
    """Whole-branch rough+sharp progress with a predeclared denominator."""

    def __init__(
        self,
        *,
        branch: str,
        total_tasks: int,
        charge_sectors: int,
        row_windows: int,
        total_work_units: int,
    ) -> None:
        self.progress = ParentProgress(
            branch=branch,
            stage="full_rough_plus_sharp_run",
            total_tasks=total_tasks,
            charge_sectors=charge_sectors,
            row_windows=row_windows,
            total_work_units=total_work_units,
        )

    def advance(self, count: int, work_units: int) -> None:
        self.progress.advance(count, work_units)


class BranchProcessPool:
    """One persistent spawn pool for an entire rough+sharp branch history."""

    def __init__(
        self,
        *,
        branch: str,
        cache_root: Path,
        manifest_sha256: str,
        length: int,
        deadline_monotonic: float,
        max_workers: int | None = None,
    ) -> None:
        if branch not in {"target", "hostile"}:
            raise ValueError("invalid L12 branch")
        if not cache_root.is_absolute():
            raise ValueError("cache_root must be absolute")
        configure_single_thread_math()
        self.branch = branch
        self.length = length
        remaining = deadline_monotonic - time.monotonic()
        if (
            not math.isfinite(deadline_monotonic)
            or remaining <= 0.0
            or remaining > HARD_WALL_LIMIT_SECONDS
        ):
            raise ValueError("deadline must be live and within the 96-hour ceiling")
        self.deadline_monotonic = deadline_monotonic
        self.max_workers = (
            CONFIGURED_WORKERS_BY_BRANCH[branch]
            if max_workers is None
            else max_workers
        )
        if type(self.max_workers) is not int or self.max_workers < 1:
            raise ValueError("max_workers must be a positive integer")
        capacity = recommended_branch_workers(branch=branch)
        if self.max_workers > capacity:
            raise ParallelRefusal(
                f"configured {branch} workers exceed current CPU/RAM capacity"
            )
        self._stop = threading.Event()
        self._closed = False
        self.child_pids: set[int] = set()
        self._run_progress: ParentRunProgress | None = None
        self._submitted_any = False
        self._stop_snapshot_emitted = False
        context = multiprocessing.get_context("spawn")
        config = WorkerConfig(
            branch=branch,
            cache_root=str(cache_root),
            manifest_sha256=manifest_sha256,
            length=length,
            deadline_monotonic=deadline_monotonic,
        )
        self._executor = concurrent.futures.ProcessPoolExecutor(
            max_workers=self.max_workers,
            mp_context=context,
            initializer=initialize_worker,
            initargs=(config,),
        )

    def set_run_plan(
        self,
        *,
        total_tasks: int,
        charge_sectors: int,
        row_windows: int,
        total_work_units: int,
    ) -> None:
        """Print the full denominator before the first future is submitted."""
        if self._submitted_any:
            raise ParallelRefusal("full L12 run plan arrived after task submission")
        if self._run_progress is not None:
            expected = self._run_progress.progress
            if (
                expected.total != total_tasks
                or expected.charge_sectors != charge_sectors
                or expected.row_windows != row_windows
                or expected.total_work_units != total_work_units
            ):
                raise ParallelRefusal("conflicting full L12 run plans")
            return
        self._run_progress = ParentRunProgress(
            branch=self.branch,
            total_tasks=total_tasks,
            charge_sectors=charge_sectors,
            row_windows=row_windows,
            total_work_units=total_work_units,
        )

    def request_stop(self, *, terminate_running: bool = False) -> None:
        """Stop accepting work and cancel tasks which have not started."""
        self._stop.set()
        if terminate_running:
            # Python 3.9 has no public ProcessPoolExecutor.terminate_workers().
            # Keep the compatibility access isolated here.  Each branch parent
            # owns only this pool, so no unrelated child is targeted.
            processes = getattr(self._executor, "_processes", None)
            if isinstance(processes, dict):
                for process in tuple(processes.values()):
                    if process is not None and process.is_alive():
                        process.terminate()

    def emit_stop_snapshot(self, reason: str) -> None:
        """Flush the exact parent-owned remainder before abnormal shutdown."""
        if self._stop_snapshot_emitted:
            return
        self._stop_snapshot_emitted = True
        snapshot = (
            self._run_progress.progress.snapshot()
            if self._run_progress is not None
            else None
        )
        if snapshot is None:
            print(
                f"L12_PROGRESS_STOP branch={self.branch} reason={reason} "
                "denominator=unregistered",
                flush=True,
            )
            return
        print(
            f"L12_PROGRESS_STOP branch={self.branch} reason={reason} "
            f"completed={snapshot['completed_tasks']} "
            f"remaining={snapshot['remaining_tasks']} "
            f"completed_solver_cell_steps={snapshot['completed_solver_cell_steps']} "
            f"remaining_solver_cell_steps={snapshot['remaining_solver_cell_steps']} "
            f"elapsed={ParentProgress._duration(snapshot['elapsed_seconds'])}",
            flush=True,
        )

    def _observe_children(self) -> None:
        """Collect process topology from the parent; workers do no tracking."""
        processes = getattr(self._executor, "_processes", None)
        if isinstance(processes, dict):
            for process in tuple(processes.values()):
                pid = getattr(process, "pid", None)
                if type(pid) is int and pid > 0:
                    self.child_pids.add(pid)

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
            raise ParallelRefusal("parallel L12 pool is closing")
        materialized = list(tasks)
        materialized_work = list(work_units)
        if len(materialized_work) != len(materialized) or any(
            type(value) is not int or value < 0 for value in materialized_work
        ):
            raise ParallelRefusal("parent work-unit census does not match tasks")
        self._submitted_any = True
        if not materialized:
            ParentProgress(
                branch=self.branch,
                stage=stage,
                total_tasks=0,
                charge_sectors=charge_sectors,
                row_windows=row_windows,
                total_work_units=0,
            )
            return []
        progress = ParentProgress(
            branch=self.branch,
            stage=stage,
            total_tasks=len(materialized),
            charge_sectors=charge_sectors,
            row_windows=row_windows,
            total_work_units=sum(materialized_work),
        )
        # Start the heaviest windows first to avoid a central-q tail and to
        # make the first velocity sample representative.  Results are still
        # restored to canonical predecessor order before parent reduction.
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
        try:
            pending = set(futures)
            while pending:
                if self._stop.is_set():
                    raise ParallelRefusal("parallel L12 stop requested")
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
            results_by_index = {
                index: future.result() for index, future, _work in future_rows
            }
            results = [results_by_index[index] for index in range(len(materialized))]
        except BaseException as error:
            for future in futures:
                future.cancel()
            self.emit_stop_snapshot(type(error).__name__)
            self.request_stop(terminate_running=True)
            raise
        return results

    def assert_run_complete(self) -> None:
        if self._run_progress is None:
            raise ParallelRefusal("full L12 run denominator was not registered")
        snapshot = self._run_progress.progress.snapshot()
        if not snapshot["complete"]:
            self.emit_stop_snapshot("denominator_mismatch")
            raise ParallelRefusal(
                "full L12 run did not consume its declared task/work denominator"
            )

    @property
    def concurrent_numerical_workset_bytes(self) -> int:
        per_worker = (
            TARGET_WORKSET_BYTES if self.branch == "target" else HOSTILE_WORKSET_BYTES
        )
        return self.max_workers * per_worker

    def resource_record(self) -> dict[str, Any]:
        progress = (
            self._run_progress.progress.snapshot()
            if self._run_progress is not None
            else None
        )
        return {
            "process_start_method": "spawn",
            "max_workers": self.max_workers,
            "configured_total_workers": CONFIGURED_TOTAL_WORKERS,
            "hard_wall_limit_seconds": HARD_WALL_LIMIT_SECONDS,
            "observed_worker_pids": sorted(self.child_pids),
            "concurrent_numerical_workset_bytes": self.concurrent_numerical_workset_bytes,
            "thread_limited_math_libraries": list(THREAD_LIMIT_ENV),
            "large_arrays_transported_between_processes": False,
            "parent_only_ordered_reduction": True,
            "parent_only_publication": True,
            "parent_only_progress_tracking": True,
            "full_run_progress": progress,
        }

    def close(self, *, wait: bool = True) -> None:
        if self._closed:
            return
        self._closed = True
        self._executor.shutdown(wait=wait, cancel_futures=True)

    def __enter__(self) -> "BranchProcessPool":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if exc is not None:
            self.request_stop(terminate_running=True)
        self.close(wait=True)


@contextmanager
def parent_termination_guard(pool: BranchProcessPool):
    """Forward SIGINT/SIGTERM to pool children and leave scratch in place."""
    if threading.current_thread() is not threading.main_thread():
        yield
        return
    previous: dict[int, Any] = {}

    def stop(signum: int, _frame: object) -> None:
        pool.emit_stop_snapshot(f"signal_{signum}")
        pool.request_stop(terminate_running=True)
        raise GracefulTermination(
            f"parallel L12 parent received signal {signum}; partial workspace preserved"
        )

    for signum in (signal.SIGINT, signal.SIGTERM):
        previous[signum] = signal.getsignal(signum)
        signal.signal(signum, stop)
    try:
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
