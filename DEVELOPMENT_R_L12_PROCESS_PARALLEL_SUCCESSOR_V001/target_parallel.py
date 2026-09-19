#!/usr/bin/env python3
"""Process-parallel kernels for the frozen target V012 numerical semantics."""

from __future__ import annotations

import gc
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
ENGINE_DIR = ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
for directory in (TARGET_DIR, ENGINE_DIR, HERE):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import consume_target_cache as target  # noqa: E402
from parallel_runtime import (  # noqa: E402
    HARD_WALL_LIMIT_SECONDS,
    BranchProcessPool,
    ManifestMemmapCache,
    ParallelRefusal,
    close_mapping,
    worker_context,
)


WORD_DTYPE = np.dtype("<u4")
INDEX_DTYPE = np.dtype("<i4")


class TargetWorkerCache:
    """Target API facade over the common lazy immutable cache mapping."""

    def __init__(self, cache: ManifestMemmapCache):
        self._cache = cache
        self.length = cache.length
        self.edges = target.v004.sealed.graph(self.length)

    def open(self, name: str, dtype: np.dtype[Any]) -> np.ndarray:
        return self._cache.open(name, dtype)

    def carrier_words(self, q: int) -> np.ndarray:
        return self.open(f"carrier_q_{q:02d}_words.u32", WORD_DTYPE)

    def lineage_words(self, prefix: int, q: int) -> np.ndarray:
        return self.open(f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32", WORD_DTYPE)

    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
        return (
            self.open(f"admission_n_{event:02d}_q_{q:02d}_blank.i32", INDEX_DTYPE),
            self.open(f"admission_n_{event:02d}_q_{q:02d}_destination.i32", INDEX_DTYPE),
        )

    def lineage_map(self, prefix: int, q: int, accepted: bool) -> np.ndarray:
        role = "accepted" if accepted else "stay"
        return self.open(f"lineage_n_{prefix:02d}_q_{q:02d}_{role}.i32", INDEX_DTYPE)


def _context() -> tuple[Any, TargetWorkerCache]:
    config, common = worker_context("target")
    cache = TargetWorkerCache(common)
    target.CACHE = cache
    target.builder.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    target.v004.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    # CachedSector's inner Hamiltonian calls the predecessor guard.  The
    # successor checks the shared absolute deadline at every task boundary;
    # leaving this predecessor-local timer unset avoids resetting authority.
    target.PHYSICAL_STARTED = None
    return config, cache


def _resolution(label: str) -> Any:
    table = {
        target.v004.sealed.COARSE.label: target.v004.sealed.COARSE,
        target.v004.sealed.FINE.label: target.v004.sealed.FINE,
    }
    try:
        return table[label]
    except KeyError as error:
        raise ParallelRefusal("target resolution label is not frozen coarse/fine") from error


def _window_work(
    rows: int, columns: int, step: int, depth: int, multiplier: int = 1
) -> list[int]:
    return [
        (min(rows, lower + step) - lower) * columns * depth * multiplier
        for lower in range(0, rows, step)
    ]


def target_run_plan(length: int) -> dict[str, int]:
    """Exact target task/window denominator for rough plus sharp."""
    admission_sectors = charge_sectors = row_windows = work_units = 0
    for resolution in (target.v004.sealed.COARSE, target.v004.sealed.FINE):
        depth = max(resolution.checkpoints)
        for event in range(length - 1):
            admission_sectors += event + 2
            charge_sectors += event + 2
            for prefix in (event + 1, event):
                for q in range(prefix + 1):
                    charge_sectors += 1
                    columns = math.comb(2 * length, q)
                    step = target.v004.v3.batch_rows(columns, resolution, False)
                    windows = _window_work(
                        math.comb(prefix, q), columns, step, depth
                    )
                    row_windows += len(windows)
                    work_units += sum(windows)
        prefix = length - 1
        for q in range(length):
            source_rows = math.comb(prefix, q)
            charge_sectors += 2
            columns = math.comb(2 * length, q)
            step = target.v004.v3.batch_rows(columns, resolution, False)
            windows = _window_work(source_rows, columns, step, depth, 2)
            row_windows += len(windows)
            work_units += sum(windows)
            columns = math.comb(2 * length, q + 1)
            step = target.v004.v3.batch_rows(columns, resolution, False)
            windows = _window_work(source_rows, columns, step, depth)
            row_windows += len(windows)
            work_units += sum(windows)
    return {
        "total_tasks": admission_sectors + row_windows,
        "charge_sectors": charge_sectors,
        "row_windows": row_windows,
        "total_work_units": work_units,
    }


def _merge_solver(total: dict[str, Any], partial: dict[str, Any]) -> None:
    if set(total) != set(partial):
        raise ParallelRefusal("target solver summary key census mismatch")
    if total["quadrature_nodes"] != partial["quadrature_nodes"]:
        raise ParallelRefusal("target solver quadrature changed across workers")
    total["converged"] = bool(total["converged"]) and bool(partial["converged"])
    total["batches"] = int(total["batches"]) + int(partial["batches"])
    total["low_memory_batches"] = (
        int(total["low_memory_batches"]) + int(partial["low_memory_batches"])
    )
    for key in (
        "maximum_krylov_steps",
        "maximum_exp_difference",
        "maximum_residual_indicator",
        "maximum_subdivisions",
        "maximum_live_bytes",
    ):
        total[key] = max(total[key], partial[key])


def target_admission_worker(task: dict[str, Any]) -> dict[str, Any]:
    """Write exactly one output-q admission shard; no other task touches it."""
    config, cache = _context()
    length = config.length
    prefix = int(task["prefix"])
    event = int(task["event"])
    out_q = int(task["out_q"])
    before = Path(task["before"])
    output = Path(task["output"])
    if prefix != event or not 0 <= out_q <= prefix + 1 or event >= length - 1:
        raise ParallelRefusal("target admission task identity mismatch")
    destination = np.lib.format.open_memmap(
        target.v004.shard_path(output, out_q),
        mode="w+",
        dtype=np.complex128,
        shape=target.v004.shape(length, prefix + 1, out_q),
    )
    try:
        destination[:] = 0.0
        cosine = math.cos(target.v004.sealed.PHI)
        sine = math.sin(target.v004.sealed.PHI)
        if out_q <= prefix:
            source = target.v004.open_shard(before, out_q)
            stay_rows = cache.lineage_map(prefix, out_q, False)
            blank_columns, unused = cache.admission(event, out_q)
            close_mapping(unused)
            try:
                for source_row, target_row in enumerate(stay_rows):
                    row = np.array(source[source_row], copy=True)
                    row[blank_columns] *= cosine
                    destination[int(target_row)] = row
            finally:
                close_mapping(source)
                close_mapping(stay_rows)
                close_mapping(blank_columns)
        if out_q and out_q - 1 <= prefix:
            source = target.v004.open_shard(before, out_q - 1)
            accepted_rows = cache.lineage_map(prefix, out_q - 1, True)
            blank_columns, destination_columns = cache.admission(event, out_q - 1)
            try:
                for source_row, target_row in enumerate(accepted_rows):
                    destination[int(target_row), destination_columns] = (
                        -1.0j * sine * source[source_row, blank_columns]
                    )
            finally:
                close_mapping(source)
                close_mapping(accepted_rows)
                close_mapping(blank_columns)
                close_mapping(destination_columns)
        destination.flush()
    finally:
        close_mapping(destination)
    common = worker_context("target")[1]
    common.verify_root()
    return {"out_q": out_q}


def target_route_worker(task: dict[str, Any]) -> dict[str, Any]:
    """Mutate one disjoint q/row window in an actual or null shard."""
    config, _cache = _context()
    q = int(task["q"])
    lower, upper = int(task["lower"]), int(task["upper"])
    role = str(task["role"])
    resolution = _resolution(str(task["resolution"]))
    edges = target.v004.sealed.graph(config.length)
    sector = target.CachedSector(config.length, q, edges)
    solver = target.v004.v3.empty_solver(resolution)
    current = np.zeros(len(edges))
    try:
        if role not in {"actual", "null"}:
            raise ParallelRefusal("target route role mismatch")
        block = target.v004.open_shard(Path(task["root"]), q, mode="r+")
        try:
            window = np.array(block[lower:upper], copy=True)
            evolved, current, record = target.v004.v3.propagate_dispatch(
                config.length, sector, window, resolution
            )
            block[lower:upper] = evolved
            block.flush()
            target.v004.v3.update_solver(solver, record)
        finally:
            close_mapping(block)
    finally:
        sector.close()
    worker_context("target")[1].verify_root()
    return {
        "q": q,
        "lower": lower,
        "role": role,
        "current": current,
        "solver": solver,
    }


def target_terminal_worker(task: dict[str, Any]) -> dict[str, Any]:
    """Evolve one terminal row window and return only its small reduction."""
    config, cache = _context()
    length = config.length
    event = length - 1
    phase = str(task["phase"])
    source_q = int(task["source_q"])
    lower, upper = int(task["lower"]), int(task["upper"])
    resolution = _resolution(str(task["resolution"]))
    before = Path(task["before"])
    edges = target.v004.sealed.graph(length)
    old = target.v004.open_shard(before, source_q)
    source = np.array(old[lower:upper], copy=True)
    close_mapping(old)
    actual_solver = target.v004.v3.empty_solver(resolution)
    null_solver = target.v004.v3.empty_solver(resolution)
    result: dict[str, Any] = {
        "phase": phase,
        "source_q": source_q,
        "lower": lower,
        "admitted_weight": 0.0,
        "admitted_occupation": np.zeros(2 * length),
        "after_weight": 0.0,
        "after_occupation": np.zeros(2 * length),
        "null_weight": 0.0,
        "actual_current": np.zeros(len(edges)),
        "null_current": np.zeros(len(edges)),
        "actual_solver": actual_solver,
        "null_solver": null_solver,
        "blocked_error": 0.0,
    }
    if phase == "child0":
        q = source_q
        carrier_words = cache.carrier_words(q)
        blank_columns, unused = cache.admission(event, q)
        close_mapping(unused)
        occupied_columns = np.flatnonzero(((carrier_words >> event) & 1) == 1)
        sector = target.CachedSector(length, q, edges)
        try:
            child = source.copy()
            child[:, blank_columns] *= math.cos(target.v004.sealed.PHI)
            if len(occupied_columns):
                result["blocked_error"] = float(np.max(np.abs(
                    child[:, occupied_columns] - source[:, occupied_columns]
                )))
            weight, occupation = target.v004.block_statistics(
                carrier_words, child, 2 * length
            )
            result["admitted_weight"] = weight
            result["admitted_occupation"] = occupation
            evolved, flux = target.v004.route_ephemeral(
                length, sector, child, resolution, actual_solver
            )
            weight, occupation = target.v004.block_statistics(
                carrier_words, evolved, 2 * length
            )
            result["after_weight"] = weight
            result["after_occupation"] = occupation
            result["actual_current"] = flux
            null_evolved, flux = target.v004.route_ephemeral(
                length, sector, source, resolution, null_solver
            )
            result["null_weight"] = target.v004.block_statistics(
                carrier_words, null_evolved, 2 * length
            )[0]
            result["null_current"] = flux
        finally:
            sector.close()
            close_mapping(carrier_words)
            close_mapping(blank_columns)
    elif phase == "child1":
        q = source_q + 1
        carrier_words = cache.carrier_words(q)
        blank_columns, destination_columns = cache.admission(event, source_q)
        sector = target.CachedSector(length, q, edges)
        try:
            child = np.zeros((upper - lower, len(carrier_words)), dtype=np.complex128)
            child[:, destination_columns] = (
                -1.0j
                * math.sin(target.v004.sealed.PHI)
                * source[:, blank_columns]
            )
            weight, occupation = target.v004.block_statistics(
                carrier_words, child, 2 * length
            )
            result["admitted_weight"] = weight
            result["admitted_occupation"] = occupation
            evolved, flux = target.v004.route_ephemeral(
                length, sector, child, resolution, actual_solver
            )
            weight, occupation = target.v004.block_statistics(
                carrier_words, evolved, 2 * length
            )
            result["after_weight"] = weight
            result["after_occupation"] = occupation
            result["actual_current"] = flux
        finally:
            sector.close()
            close_mapping(carrier_words)
            close_mapping(blank_columns)
            close_mapping(destination_columns)
    else:
        raise ParallelRefusal("unknown target terminal phase")
    worker_context("target")[1].verify_root()
    return result


class TargetParallelAdapter:
    """Parent-owned deterministic adapter for one complete target history."""

    def __init__(self, pool: BranchProcessPool):
        if pool.branch != "target":
            raise ValueError("target adapter requires target branch pool")
        self.pool = pool
        self._originals: tuple[Any, Any, Any] | None = None
        self.pool.set_run_plan(**target_run_plan(pool.length))

    def create_admitted(
        self, length: int, before: Path, prefix: int, event: int, output: Path
    ) -> None:
        if length != self.pool.length or prefix != event or output.exists():
            raise ParallelRefusal("target parent admission request mismatch")
        output.mkdir(parents=True, exist_ok=False)
        tasks = [
            {
                "before": str(before.resolve()),
                "output": str(output.resolve()),
                "prefix": prefix,
                "event": event,
                "out_q": out_q,
            }
            for out_q in range(prefix + 2)
        ]
        results = self.pool.map_ordered(
            target_admission_worker,
            tasks,
            stage=f"admission_event_{event + 1:02d}",
            charge_sectors=len(tasks),
            row_windows=0,
            work_units=[0] * len(tasks),
        )
        if [row["out_q"] for row in results] != list(range(prefix + 2)):
            raise ParallelRefusal("target admission completion census mismatch")

    def route_pair(
        self,
        length: int,
        actual: Path,
        actual_prefix: int,
        null: Path,
        null_prefix: int,
        resolution: Any,
    ) -> tuple[np.ndarray, dict[str, Any], np.ndarray, dict[str, Any]]:
        if length != self.pool.length:
            raise ParallelRefusal("target route length mismatch")
        tasks: list[dict[str, Any]] = []
        task_work: list[int] = []
        sector_count = 0
        for q in range(actual_prefix + 1):
            step = target.v004.v3.batch_rows(
                math.comb(2 * length, q), resolution, False
            )
            for role, root, prefix in (
                ("actual", actual, actual_prefix),
                ("null", null, null_prefix),
            ):
                if q > prefix:
                    continue
                sector_count += 1
                rows = math.comb(prefix, q)
                for lower in range(0, rows, step):
                    tasks.append({
                        "q": q,
                        "lower": lower,
                        "upper": min(rows, lower + step),
                        "role": role,
                        "root": str(root.resolve()),
                        "resolution": resolution.label,
                    })
                    task_work.append(
                        (min(rows, lower + step) - lower)
                        * math.comb(2 * length, q)
                        * max(resolution.checkpoints)
                    )
        results = self.pool.map_ordered(
            target_route_worker,
            tasks,
            stage=f"route_{resolution.label}_prefix_{actual_prefix:02d}",
            charge_sectors=sector_count,
            row_windows=len(tasks),
            work_units=task_work,
        )
        edges = target.v004.sealed.graph(length)
        actual_current = np.zeros(len(edges))
        null_current = np.zeros(len(edges))
        actual_solver = target.v004.v3.empty_solver(resolution)
        null_solver = target.v004.v3.empty_solver(resolution)
        for row in results:
            if row["role"] == "actual":
                actual_current += row["current"]
                _merge_solver(actual_solver, row["solver"])
            elif row["role"] == "null":
                null_current += row["current"]
                _merge_solver(null_solver, row["solver"])
            else:
                raise ParallelRefusal("target route result role mismatch")
        return actual_current, actual_solver, null_current, null_solver

    def terminal_stream(
        self, length: int, before: Path, prefix: int, event: int, resolution: Any
    ) -> dict[str, Any]:
        if length != self.pool.length or prefix != length - 1 or event != prefix:
            raise ParallelRefusal("target terminal parent identity mismatch")
        tasks: list[dict[str, Any]] = []
        task_work: list[int] = []
        for q in range(length):
            source_rows = math.comb(prefix, q)
            child0_rows = target.v004.v3.batch_rows(
                math.comb(2 * length, q), resolution, False
            )
            for lower in range(0, source_rows, child0_rows):
                tasks.append({
                    "phase": "child0",
                    "source_q": q,
                    "lower": lower,
                    "upper": min(source_rows, lower + child0_rows),
                    "before": str(before.resolve()),
                    "resolution": resolution.label,
                })
                task_work.append(
                    (min(source_rows, lower + child0_rows) - lower)
                    * math.comb(2 * length, q)
                    * max(resolution.checkpoints)
                    * 2
                )
            child1_rows = target.v004.v3.batch_rows(
                math.comb(2 * length, q + 1), resolution, False
            )
            for lower in range(0, source_rows, child1_rows):
                tasks.append({
                    "phase": "child1",
                    "source_q": q,
                    "lower": lower,
                    "upper": min(source_rows, lower + child1_rows),
                    "before": str(before.resolve()),
                    "resolution": resolution.label,
                })
                task_work.append(
                    (min(source_rows, lower + child1_rows) - lower)
                    * math.comb(2 * length, q + 1)
                    * max(resolution.checkpoints)
                )
        results = self.pool.map_ordered(
            target_terminal_worker,
            tasks,
            stage=f"terminal_{resolution.label}",
            charge_sectors=2 * length,
            row_windows=len(tasks),
            work_units=task_work,
        )
        edges = target.v004.sealed.graph(length)
        admitted_weights = np.zeros(length + 1)
        admitted_occupation = np.zeros(2 * length)
        after_weights = np.zeros(length + 1)
        after_occupation = np.zeros(2 * length)
        null_weights = np.zeros(length + 1)
        actual_current = np.zeros(len(edges))
        null_current = np.zeros(len(edges))
        actual_solver = target.v004.v3.empty_solver(resolution)
        null_solver = target.v004.v3.empty_solver(resolution)
        blocked_error = 0.0
        for row in results:
            source_q = row["source_q"]
            output_q = source_q if row["phase"] == "child0" else source_q + 1
            admitted_weights[output_q] += row["admitted_weight"]
            admitted_occupation += row["admitted_occupation"]
            after_weights[output_q] += row["after_weight"]
            after_occupation += row["after_occupation"]
            actual_current += row["actual_current"]
            _merge_solver(actual_solver, row["actual_solver"])
            if row["phase"] == "child0":
                null_weights[source_q] += row["null_weight"]
                null_current += row["null_current"]
                _merge_solver(null_solver, row["null_solver"])
                blocked_error = max(blocked_error, row["blocked_error"])
        return {
            "admitted_weights": admitted_weights,
            "admitted_occupation": admitted_occupation,
            "after_weights": after_weights,
            "after_occupation": after_occupation,
            "null_weights": null_weights,
            "actual_current": actual_current,
            "null_current": null_current,
            "actual_solver": actual_solver,
            "null_solver": null_solver,
            "blocked_error": blocked_error,
        }

    def install(self) -> None:
        """Patch numerical loop entry points after parent cache authentication."""
        if self._originals is not None:
            raise ParallelRefusal("target parallel adapter already installed")
        self._originals = (
            target.v004.route_pair,
            target.v004.create_admitted,
            target.v004.terminal_stream,
        )
        target.v004.route_pair = self.route_pair
        target.v004.create_admitted = self.create_admitted
        target.v004.terminal_stream = self.terminal_stream

    def restore(self) -> None:
        if self._originals is None:
            return
        (
            target.v004.route_pair,
            target.v004.create_admitted,
            target.v004.terminal_stream,
        ) = self._originals
        self._originals = None

    def __enter__(self) -> "TargetParallelAdapter":
        self.install()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.restore()
        gc.collect()
