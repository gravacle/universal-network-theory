#!/usr/bin/env python3
"""Process-parallel kernels for the independent hostile V004R4 semantics."""

from __future__ import annotations

import gc
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
HOSTILE_DIR = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
for directory in (HOSTILE_DIR, HERE):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import consume_cache_v004r4 as hostile  # noqa: E402
from parallel_runtime import (  # noqa: E402
    HARD_WALL_LIMIT_SECONDS,
    BranchProcessPool,
    ManifestMemmapCache,
    ParallelRefusal,
    close_mapping,
    worker_context,
)


WORD_DTYPE = np.dtype("<u4")
OFFSET_DTYPE = np.dtype("<u8")
INDEX_DTYPE = np.dtype("<i4")


class HostileWorkerCache:
    """V004R4 API facade over the common lazy immutable cache mapping."""

    def __init__(self, cache: ManifestMemmapCache):
        self._cache = cache
        self.length = cache.length
        self.edges = hostile.physical.hostile_edges(self.length)

    def _open(self, name: str, dtype: np.dtype[Any]) -> np.ndarray:
        return self._cache.open(name, dtype)

    def carrier(self, q: int, edges: list[tuple[int, int, str]]) -> Any:
        if edges != self.edges or q not in range(self.length + 1):
            raise ParallelRefusal("hostile carrier task changed graph/sector")
        prefix = f"q_{q:02d}"
        carrier = hostile.legacy.CachedCarrier(
            self.length,
            q,
            edges,
            self._open(f"{prefix}_words.u32", WORD_DTYPE),
            self._open(f"{prefix}_offsets.u64", OFFSET_DTYPE),
            self._open(f"{prefix}_sources.i32", INDEX_DTYPE)
            if q else np.empty(0, dtype=INDEX_DTYPE),
            self._open(f"{prefix}_targets.i32", INDEX_DTYPE)
            if q else np.empty(0, dtype=INDEX_DTYPE),
        )
        if (
            len(carrier.words) != math.comb(2 * self.length, q)
            or len(carrier.offsets) != 3 * self.length + 1
            or int(carrier.offsets[0]) != 0
            or int(carrier.offsets[-1]) != len(carrier.sources)
            or len(carrier.sources) != len(carrier.targets)
        ):
            carrier.release()
            raise ParallelRefusal("hostile carrier cached shape/offset mismatch")
        return carrier

    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
        if not 0 <= event < self.length or not 1 <= q <= event + 1:
            raise ParallelRefusal("hostile admission task outside cache census")
        return (
            self._open(f"event_{event:02d}_q_{q:02d}_occupied.i32", INDEX_DTYPE),
            self._open(f"event_{event:02d}_q_{q:02d}_old.i32", INDEX_DTYPE),
        )

    def lineage(self, event: int, q: int, added: bool) -> np.ndarray:
        if not 0 <= event < self.length - 1 or not 0 <= q <= event:
            raise ParallelRefusal("hostile lineage task outside cache census")
        role = "added" if added else "same"
        return self._open(f"prefix_{event:02d}_q_{q:02d}_{role}.i32", INDEX_DTYPE)


def _context() -> tuple[Any, HostileWorkerCache]:
    config, common = worker_context("hostile")
    cache = HostileWorkerCache(common)
    hostile.legacy.configure(config.length, cache, 0.0)
    hostile.physical.L12_WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    hostile.v3.WALL_LIMIT = HARD_WALL_LIMIT_SECONDS
    # The common absolute deadline is checked at each task boundary.  Disable
    # the predecessor-local elapsed clock (which has a different origin), but
    # retain its per-process RSS check.
    hostile.v3.EXECUTION_STARTED = None
    return config, cache


def _accuracy(label: str) -> Any:
    table = {
        hostile.physical.ROUGH.label: hostile.physical.ROUGH,
        hostile.physical.SHARP.label: hostile.physical.SHARP,
    }
    try:
        return table[label]
    except KeyError as error:
        raise ParallelRefusal("hostile accuracy label is not frozen rough/sharp") from error


def _window_work(rows: int, columns: int, step: int, depth: int) -> list[int]:
    return [
        (min(rows, lower + step) - lower) * columns * depth
        for lower in range(0, rows, step)
    ]


def hostile_run_plan(length: int) -> dict[str, int]:
    """Exact hostile task/window denominator for rough plus sharp."""
    admission_sectors = charge_sectors = row_windows = work_units = 0
    for accuracy in (hostile.physical.ROUGH, hostile.physical.SHARP):
        depth = max(accuracy.checkpoints)
        for event in range(length - 1):
            admission_sectors += event + 2
            charge_sectors += event + 2
            for prefix in (event + 1, event):
                for q in range(prefix + 1):
                    charge_sectors += 1
                    columns = math.comb(2 * length, q)
                    step = hostile.legacy.replay.safe_batch_rows(
                        columns, max(accuracy.checkpoints)
                    )
                    windows = _window_work(
                        math.comb(prefix, q), columns, step, depth
                    )
                    row_windows += len(windows)
                    work_units += sum(windows)
        prefix = length - 1
        for phase, q_range in (
            ("child0", range(length)),
            ("child1", range(1, length + 1)),
            ("null", range(length)),
        ):
            for q in q_range:
                source_q = q - 1 if phase == "child1" else q
                columns = math.comb(2 * length, q)
                step = hostile.legacy.replay.safe_batch_rows(
                    columns,
                    max(accuracy.checkpoints),
                    hostile.physical.TERMINAL_WINDOW_BYTES,
                )
                windows = _window_work(
                    math.comb(prefix, source_q), columns, step, depth
                )
                charge_sectors += 1
                row_windows += len(windows)
                work_units += sum(windows)
    return {
        "total_tasks": admission_sectors + row_windows,
        "charge_sectors": charge_sectors,
        "row_windows": row_windows,
        "total_work_units": work_units,
    }


def _merge_statistics(total: dict[str, Any], partial: dict[str, Any]) -> None:
    if set(total) != set(partial):
        raise ParallelRefusal("hostile statistics key census mismatch")
    for key in ("norm", "retained", "remaining"):
        total[key] = float(total[key]) + float(partial[key])
    total["sectors"] += partial["sectors"]
    total["occupation"] += partial["occupation"]


def _merge_method(total: dict[str, Any], partial: dict[str, Any]) -> None:
    if set(total) != set(partial):
        raise ParallelRefusal("hostile method key census mismatch")
    constants = (
        "algorithm",
        "quadrature_group_max",
        "allocation_vector_slots",
        "allocation_limit_bytes",
        "quadrature_nodes",
        "q_sharded",
    )
    if any(total[key] != partial[key] for key in constants):
        raise ParallelRefusal("hostile method constant changed across workers")
    total["converged"] = bool(total["converged"]) and bool(partial["converged"])
    total["batches"] = int(total["batches"]) + int(partial["batches"])
    for key in (
        "maximum_degree",
        "maximum_endpoint_difference",
        "maximum_tail_indicator_32",
        "maximum_allocation_estimate_bytes",
    ):
        total[key] = max(total[key], partial[key])


def _empty_method(accuracy: Any) -> dict[str, Any]:
    method = hostile.v3.method_record()
    method["quadrature_nodes"] = accuracy.gauss_order
    method["q_sharded"] = True
    return method


def hostile_admission_worker(task: dict[str, Any]) -> dict[str, Any]:
    """Write one hostile output-q shard; all target files are disjoint."""
    config, cache = _context()
    length = config.length
    event = int(task["event"])
    out_q = int(task["out_q"])
    root = Path(task["root"])
    if not 0 <= event < length - 1 or not 0 <= out_q <= event + 1:
        raise ParallelRefusal("hostile admission task identity mismatch")
    source_state = hostile.v3.DiskPrefix(root, event)
    output_state = hostile.v3.DiskPrefix(root, event + 1)
    carrier = cache.carrier(out_q, hostile.physical.hostile_edges(length))
    target_shard = output_state.create_shard(out_q)
    blocked_error = 0.0
    try:
        if out_q <= event:
            source = source_state.open_shard(out_q)
            target_rows = cache.lineage(event, out_q, False)
            blank = ((carrier.words >> event) & 1) == 0
            factors = np.where(blank, math.cos(hostile.physical.ANGLE), 1.0)
            step = hostile.v3.io_rows(len(carrier.words))
            try:
                for lower in range(0, len(source), step):
                    upper = min(len(source), lower + step)
                    data = np.array(source[lower:upper], copy=True)
                    data *= factors[np.newaxis, :]
                    target_shard[target_rows[lower:upper], :] = data
                    if np.any(~blank):
                        blocked_error = max(
                            blocked_error,
                            float(np.max(np.abs(
                                data[:, ~blank] - source[lower:upper, ~blank]
                            ))),
                        )
            finally:
                hostile.v3.close_memmap(source)
                close_mapping(target_rows)
        if out_q >= 1:
            source = source_state.open_shard(out_q - 1)
            target_rows = cache.lineage(event, out_q - 1, True)
            occupied_columns, old_columns = cache.admission(event, out_q)
            step = hostile.v3.io_rows(max(1, len(old_columns)))
            try:
                for lower in range(0, len(source), step):
                    upper = min(len(source), lower + step)
                    data = -1.0j * math.sin(hostile.physical.ANGLE) * np.asarray(
                        source[lower:upper, old_columns]
                    )
                    target_shard[np.ix_(target_rows[lower:upper], occupied_columns)] = data
            finally:
                hostile.v3.close_memmap(source)
                close_mapping(target_rows)
                close_mapping(occupied_columns)
                close_mapping(old_columns)
        hostile.v3.close_memmap(target_shard, write=True)
    finally:
        carrier.release()
    worker_context("hostile")[1].verify_root()
    return {"out_q": out_q, "blocked_error": blocked_error}


def hostile_route_worker(task: dict[str, Any]) -> dict[str, Any]:
    """Evolve one disjoint q/row window and optionally update it in place."""
    config, cache = _context()
    q = int(task["q"])
    prefix = int(task["prefix"])
    lower, upper = int(task["lower"]), int(task["upper"])
    mutate = bool(task["mutate"])
    classify_event = task["classify_event"]
    if classify_event is not None:
        classify_event = int(classify_event)
    accuracy = _accuracy(str(task["accuracy"]))
    state = hostile.v3.DiskPrefix(Path(task["root"]), prefix)
    edges = hostile.physical.hostile_edges(config.length)
    carrier = cache.carrier(q, edges)
    shard = state.open_shard(q, "r+" if mutate else "r")
    initial = hostile.v3.empty_statistics()
    final_stats = hostile.v3.empty_statistics()
    integrated = np.zeros(len(edges))
    method = _empty_method(accuracy)
    allowed = blocked = 0.0
    try:
        vector = np.array(shard[lower:upper], copy=True)
        hostile.v3.add_statistics(initial, carrier, q, vector)
        if classify_event is not None:
            blank = ((carrier.words >> classify_event) & 1) == 0
            allowed += float(np.vdot(vector[:, blank], vector[:, blank]).real)
            blocked += float(np.vdot(vector[:, ~blank], vector[:, ~blank]).real)
        final, flux, record = hostile.legacy.replay.low_memory_evolve_batch(
            carrier, vector, accuracy
        )
        hostile.v3.guard_rss()
        hostile.v3.add_statistics(final_stats, carrier, q, final)
        integrated += flux
        hostile.v3.update_method(method, record)
        if mutate:
            shard[lower:upper] = final
    finally:
        hostile.v3.close_memmap(shard, write=mutate)
        carrier.release()
    worker_context("hostile")[1].verify_root()
    return {
        "q": q,
        "lower": lower,
        "initial": initial,
        "final": final_stats,
        "integrated": integrated,
        "method": method,
        "allowed": allowed,
        "blocked": blocked,
    }


def hostile_terminal_worker(task: dict[str, Any]) -> dict[str, Any]:
    """Evolve one hostile terminal window and return compact reductions."""
    config, cache = _context()
    length = config.length
    event = length - 1
    phase = str(task["phase"])
    q = int(task["q"])
    lower, upper = int(task["lower"]), int(task["upper"])
    accuracy = _accuracy(str(task["accuracy"]))
    state = hostile.v3.DiskPrefix(Path(task["root"]), event)
    edges = hostile.physical.hostile_edges(length)
    source_q = q - 1 if phase == "child1" else q
    source_map = state.open_shard(source_q)
    source = np.array(source_map[lower:upper], copy=True)
    hostile.v3.close_memmap(source_map)
    carrier = cache.carrier(q, edges)
    initial = hostile.v3.empty_statistics()
    admitted = hostile.v3.empty_statistics()
    final_stats = hostile.v3.empty_statistics()
    integrated = np.zeros(len(edges))
    method = _empty_method(accuracy)
    allowed = blocked = blocked_error = 0.0
    try:
        if phase == "child0":
            blank = ((carrier.words >> event) & 1) == 0
            child = source.copy()
            child[:, blank] *= math.cos(hostile.physical.ANGLE)
            if np.any(~blank):
                blocked_error = float(np.max(np.abs(
                    child[:, ~blank] - source[:, ~blank]
                )))
            hostile.v3.add_statistics(admitted, carrier, q, child)
            final, integrated, record = hostile.legacy.replay.low_memory_evolve_batch(
                carrier, child, accuracy
            )
            hostile.v3.add_statistics(final_stats, carrier, q, final)
            hostile.v3.update_method(method, record)
        elif phase == "child1":
            occupied_columns, old_columns = cache.admission(event, q)
            try:
                child = np.zeros((upper - lower, len(carrier.words)), dtype=np.complex128)
                child[:, occupied_columns] = (
                    -1.0j
                    * math.sin(hostile.physical.ANGLE)
                    * source[:, old_columns]
                )
            finally:
                close_mapping(occupied_columns)
                close_mapping(old_columns)
            hostile.v3.add_statistics(admitted, carrier, q, child)
            final, integrated, record = hostile.legacy.replay.low_memory_evolve_batch(
                carrier, child, accuracy
            )
            hostile.v3.add_statistics(final_stats, carrier, q, final)
            hostile.v3.update_method(method, record)
        elif phase == "null":
            hostile.v3.add_statistics(initial, carrier, q, source)
            blank = ((carrier.words >> event) & 1) == 0
            allowed = float(np.vdot(source[:, blank], source[:, blank]).real)
            blocked = float(np.vdot(source[:, ~blank], source[:, ~blank]).real)
            final, integrated, record = hostile.legacy.replay.low_memory_evolve_batch(
                carrier, source, accuracy
            )
            hostile.v3.add_statistics(final_stats, carrier, q, final)
            hostile.v3.update_method(method, record)
        else:
            raise ParallelRefusal("unknown hostile terminal phase")
        hostile.v3.guard_rss()
    finally:
        carrier.release()
    worker_context("hostile")[1].verify_root()
    return {
        "phase": phase,
        "q": q,
        "lower": lower,
        "initial": initial,
        "admitted": admitted,
        "final": final_stats,
        "integrated": integrated,
        "method": method,
        "allowed": allowed,
        "blocked": blocked,
        "blocked_error": blocked_error,
    }


class HostileParallelAdapter:
    """Parent-owned deterministic adapter for one hostile rough+sharp history."""

    def __init__(self, pool: BranchProcessPool):
        if pool.branch != "hostile":
            raise ValueError("hostile adapter requires hostile branch pool")
        self.pool = pool
        self._originals: tuple[Any, Any, Any] | None = None
        self.pool.set_run_plan(**hostile_run_plan(pool.length))

    def admit_to_next(
        self, state: Any, event: int, edges: list[tuple[int, int, str]]
    ) -> tuple[Any, float]:
        if event != state.prefix or edges != hostile.physical.hostile_edges(self.pool.length):
            raise ParallelRefusal("hostile parent admission identity mismatch")
        output = hostile.v3.DiskPrefix(state.root, event + 1)
        output.create()
        tasks = [
            {"root": str(state.root.resolve()), "event": event, "out_q": out_q}
            for out_q in range(event + 2)
        ]
        results = self.pool.map_ordered(
            hostile_admission_worker,
            tasks,
            stage=f"admission_event_{event + 1:02d}",
            charge_sectors=len(tasks),
            row_windows=0,
            work_units=[0] * len(tasks),
        )
        if [row["out_q"] for row in results] != list(range(event + 2)):
            raise ParallelRefusal("hostile admission completion census mismatch")
        output.verify_complete()
        return output, max((row["blocked_error"] for row in results), default=0.0)

    def route_disk_state(
        self,
        state: Any,
        accuracy: Any,
        edges: list[tuple[int, int, str]],
        mutate: bool,
        classify_event: int | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any], np.ndarray, dict[str, Any], float, float]:
        if edges != hostile.physical.hostile_edges(self.pool.length):
            raise ParallelRefusal("hostile parent route graph mismatch")
        tasks: list[dict[str, Any]] = []
        task_work: list[int] = []
        for q in range(state.prefix + 1):
            rows = math.comb(state.prefix, q)
            step = min(
                rows,
                hostile.legacy.replay.safe_batch_rows(
                    math.comb(2 * self.pool.length, q), max(accuracy.checkpoints)
                ),
            )
            for lower in range(0, rows, step):
                tasks.append({
                    "root": str(state.root.resolve()),
                    "prefix": state.prefix,
                    "q": q,
                    "lower": lower,
                    "upper": min(rows, lower + step),
                    "mutate": mutate,
                    "classify_event": classify_event,
                    "accuracy": accuracy.label,
                })
                task_work.append(
                    (min(rows, lower + step) - lower)
                    * math.comb(2 * self.pool.length, q)
                    * max(accuracy.checkpoints)
                )
        results = self.pool.map_ordered(
            hostile_route_worker,
            tasks,
            stage=f"route_{accuracy.label}_prefix_{state.prefix:02d}",
            charge_sectors=state.prefix + 1,
            row_windows=len(tasks),
            work_units=task_work,
        )
        initial = hostile.v3.empty_statistics()
        final_stats = hostile.v3.empty_statistics()
        integrated = np.zeros(len(edges))
        method = _empty_method(accuracy)
        allowed = blocked = 0.0
        for row in results:
            _merge_statistics(initial, row["initial"])
            _merge_statistics(final_stats, row["final"])
            integrated += row["integrated"]
            _merge_method(method, row["method"])
            allowed += row["allowed"]
            blocked += row["blocked"]
        return initial, final_stats, integrated, method, allowed, blocked

    def terminal_route(
        self, state: Any, accuracy: Any, edges: list[tuple[int, int, str]]
    ) -> tuple[Any, ...]:
        length = self.pool.length
        event = length - 1
        if state.prefix != event or edges != hostile.physical.hostile_edges(length):
            raise ParallelRefusal("hostile terminal parent identity mismatch")
        tasks: list[dict[str, Any]] = []
        task_work: list[int] = []
        # Submission order is the predecessor's exact reduction order:
        # every child0 sector, then every child1 sector, then every null sector.
        for phase, q_range in (
            ("child0", range(length)),
            ("child1", range(1, length + 1)),
            ("null", range(length)),
        ):
            for q in q_range:
                source_q = q - 1 if phase == "child1" else q
                rows = math.comb(event, source_q)
                columns = math.comb(2 * length, q)
                step = min(
                    rows,
                    hostile.legacy.replay.safe_batch_rows(
                        columns,
                        max(accuracy.checkpoints),
                        hostile.physical.TERMINAL_WINDOW_BYTES,
                    ),
                )
                for lower in range(0, rows, step):
                    tasks.append({
                        "phase": phase,
                        "q": q,
                        "lower": lower,
                        "upper": min(rows, lower + step),
                        "root": str(state.root.resolve()),
                        "accuracy": accuracy.label,
                    })
                    task_work.append(
                        (min(rows, lower + step) - lower)
                        * columns
                        * max(accuracy.checkpoints)
                    )
        results = self.pool.map_ordered(
            hostile_terminal_worker,
            tasks,
            stage=f"terminal_{accuracy.label}",
            charge_sectors=3 * length,
            row_windows=len(tasks),
            work_units=task_work,
        )
        before = hostile.v3.empty_statistics()
        admitted = hostile.v3.empty_statistics()
        actual_final = hostile.v3.empty_statistics()
        null_final = hostile.v3.empty_statistics()
        actual_flux = np.zeros(len(edges))
        null_flux = np.zeros(len(edges))
        actual_method = _empty_method(accuracy)
        null_method = _empty_method(accuracy)
        allowed = blocked = blocked_error = 0.0
        for row in results:
            if row["phase"] in {"child0", "child1"}:
                _merge_statistics(admitted, row["admitted"])
                _merge_statistics(actual_final, row["final"])
                actual_flux += row["integrated"]
                _merge_method(actual_method, row["method"])
                blocked_error = max(blocked_error, row["blocked_error"])
            else:
                _merge_statistics(before, row["initial"])
                _merge_statistics(null_final, row["final"])
                null_flux += row["integrated"]
                _merge_method(null_method, row["method"])
                allowed += row["allowed"]
                blocked += row["blocked"]
        actual_method.update({
            "terminal_children_streamed": True,
            "terminal_child0_entries": hostile.v3.EXPECTED_PRETERMINAL,
            "terminal_child1_nonzero_admission_entries": hostile.v3.EXPECTED_CHILD1_INPUT,
            "full_terminal_array_allocated": False,
        })
        return (
            before,
            admitted,
            actual_final,
            null_final,
            actual_flux,
            null_flux,
            actual_method,
            null_method,
            allowed,
            blocked,
            blocked_error,
        )

    def install(self) -> None:
        """Patch hostile loop entry points after full parent authentication."""
        if self._originals is not None:
            raise ParallelRefusal("hostile parallel adapter already installed")
        self._originals = (
            hostile.v3.route_disk_state,
            hostile.v3.admit_to_next,
            hostile.v3.terminal_route,
        )
        hostile.v3.route_disk_state = self.route_disk_state
        hostile.v3.admit_to_next = self.admit_to_next
        hostile.v3.terminal_route = self.terminal_route

    def restore(self) -> None:
        if self._originals is None:
            return
        (
            hostile.v3.route_disk_state,
            hostile.v3.admit_to_next,
            hostile.v3.terminal_route,
        ) = self._originals
        self._originals = None

    def __enter__(self) -> "HostileParallelAdapter":
        self.install()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.restore()
        gc.collect()
