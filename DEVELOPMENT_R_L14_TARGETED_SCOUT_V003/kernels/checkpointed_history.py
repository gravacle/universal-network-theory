#!/usr/bin/env python3
"""Crash-safe exact rough/sharp history orchestration for L14.

The retained volume owns cache members, committed prefix states, event rows,
and summaries.  Local NVMe is used only for disposable copies.  Publication is
event-granular: the next state is fully routed and renamed first, its reduction
is then committed immutably, and only then is the preceding prefix removed.
Consequently a crash can lose at most the in-flight event.
"""

from __future__ import annotations

import math
import os
import shutil
import stat
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

import numpy as np

from cache_builder import authenticate_cache
from exact_common import (
    ExactKernelRefusal,
    artifact,
    chmod_tree_readonly,
    directory_bytes,
    immutable_json,
    jsonable,
    load_frozen,
    one_node_pool_capacity,
    read_json,
    require_safe_root,
    sha256_file,
    state_census,
)
from resource_scheduler import (
    COMPLEX128_BYTES,
    LENGTH as SCHEDULER_LENGTH,
    MAX_HOSTILE_WORKSPACE_BYTES,
    MAX_TARGET_WORKSPACE_BYTES,
    NUMERICAL_RESERVATION_BUDGET_BYTES,
    hostile_batch_rows_l14,
    hostile_workspace_bytes,
    make_bounded_pool_type,
    sector_columns,
    target_batch_rows_l14,
    target_workspace_bytes,
    task_q,
)


LENGTH = 14
if LENGTH != SCHEDULER_LENGTH:
    raise RuntimeError("L14 scheduler/history length mismatch")
TARGET_CAP_BYTES = MAX_TARGET_WORKSPACE_BYTES
HOSTILE_WORKSPACE_BYTES = MAX_HOSTILE_WORKSPACE_BYTES
LOGICAL_SCRATCH_BYTES = 400 * 2**30


def _no_resource_guard() -> None:
    """V003 uses parent reservations, never live RSS or elapsed-time gates."""


def worker_context_l14(branch: str) -> tuple[Any, Any]:
    """Preserve cache/branch authentication without the frozen 96h cutoff."""

    runtime = __import__("parallel_runtime")
    config = getattr(runtime, "_WORKER_CONFIG", None)
    cache = getattr(runtime, "_WORKER_CACHE", None)
    if config is None or cache is None:
        raise runtime.ParallelRefusal("spawned worker context is absent")
    if config.branch != branch:
        raise runtime.ParallelRefusal("spawned worker branch mismatch")
    cache.verify_root()
    return config, cache


def _remember_worker(module: Any, name: str) -> Any:
    frozen_name = "_l14_frozen_" + name
    if not hasattr(module, frozen_name):
        setattr(module, frozen_name, getattr(module, name))
    return getattr(module, frozen_name)


def _install_target_parent_capacity(repair: Any) -> None:
    repair.install_target_capacity()
    target = repair.target
    target.v004.v3.CAP_BYTES = TARGET_CAP_BYTES
    target.v004.v3.TERMINAL_WINDOW_BYTES = TARGET_CAP_BYTES
    # Some preserved target paths consult the v004 I/O window directly.
    target.v004.IO_WINDOW_BYTES = TARGET_CAP_BYTES
    target.v004.v3.batch_rows = target_batch_rows_l14
    repair.target_parallel.worker_context = worker_context_l14
    _remember_worker(repair.target_parallel, "target_admission_worker")
    repair.target_parallel.target_admission_worker = target_admission_worker_l14
    repair.target_parallel.target_route_worker = target_route_worker_l14
    repair.target_parallel.target_terminal_worker = target_terminal_worker_l14


def _install_target_worker_capacity(repair: Any, q: int) -> None:
    _install_target_parent_capacity(repair)
    cap = target_workspace_bytes(q)
    repair.target.v004.v3.CAP_BYTES = cap
    repair.target.v004.v3.TERMINAL_WINDOW_BYTES = cap
    repair.target.v004.IO_WINDOW_BYTES = max(COMPLEX128_BYTES * sector_columns(q), cap)


def _install_hostile_parent_capacity(repair: Any) -> None:
    repair.install_hostile_capacity()
    hostile = repair.hostile
    hostile.v3.SCRATCH_LIMIT = LOGICAL_SCRATCH_BYTES
    hostile.legacy.SCRATCH_LIMIT = LOGICAL_SCRATCH_BYTES
    hostile.v3.WORKSPACE_LIMIT = HOSTILE_WORKSPACE_BYTES
    hostile.legacy.replay.WORKSPACE_LIMIT = HOSTILE_WORKSPACE_BYTES
    hostile.legacy.replay.safe_batch_rows = hostile_batch_rows_l14
    hostile.physical.TERMINAL_WINDOW_BYTES = HOSTILE_WORKSPACE_BYTES
    hostile.v3.IO_WINDOW_LIMIT = HOSTILE_WORKSPACE_BYTES
    hostile.v3.guard_rss = _no_resource_guard
    repair.hostile_parallel.worker_context = worker_context_l14
    _remember_worker(repair.hostile_parallel, "hostile_admission_worker")
    repair.hostile_parallel.hostile_admission_worker = hostile_admission_worker_l14
    repair.hostile_parallel.hostile_route_worker = hostile_route_worker_l14
    repair.hostile_parallel.hostile_terminal_worker = hostile_terminal_worker_l14


def _install_hostile_worker_capacity(repair: Any, q: int) -> None:
    _install_hostile_parent_capacity(repair)
    cap = hostile_workspace_bytes(q)
    row_bytes = COMPLEX128_BYTES * sector_columns(q)
    repair.hostile.v3.WORKSPACE_LIMIT = cap
    repair.hostile.legacy.replay.WORKSPACE_LIMIT = cap
    # Admission streams one complete row at a time.  Its bound is derived only
    # from the q-sector geometry, never from a second fixed byte ceiling.
    repair.hostile.v3.IO_WINDOW_LIMIT = row_bytes
    repair.hostile.physical.TERMINAL_WINDOW_BYTES = cap


def _normalize_hostile_method(result: dict[str, Any]) -> dict[str, Any]:
    method = result.get("method")
    if isinstance(method, dict):
        # The q-specific cap performed the allocation.  The merged audit field
        # remains a single branch-wide ceiling as required by the frozen
        # reduction schema.
        method["allocation_limit_bytes"] = HOSTILE_WORKSPACE_BYTES
    return result


def target_admission_worker_l14(task: dict[str, Any]) -> dict[str, Any]:
    repair, _a, _b, _c, _d = load_frozen()
    _install_target_worker_capacity(repair, int(task["out_q"]))
    worker = _remember_worker(repair.target_parallel, "target_admission_worker")
    return worker(task)


def target_route_worker_l14(task: dict[str, Any]) -> dict[str, Any]:
    repair, _a, _b, _c, _d = load_frozen()
    _install_target_worker_capacity(repair, task_q("target", task))
    result = repair.target_route_worker_v003(task)
    _require_target_convergence(task, result, ("solver",))
    return result


def target_terminal_worker_l14(task: dict[str, Any]) -> dict[str, Any]:
    repair, _a, _b, _c, _d = load_frozen()
    _install_target_worker_capacity(repair, task_q("target", task))
    result = repair.target_terminal_worker_v003(task)
    _require_target_convergence(task, result, ("actual_solver", "null_solver"))
    return result


def _require_target_convergence(
    task: Mapping[str, Any], result: Mapping[str, Any], solver_names: Tuple[str, ...]
) -> None:
    """Refuse unresolved numerical work with its exact worker identity."""

    for solver_name in solver_names:
        solver = result.get(solver_name)
        if not isinstance(solver, Mapping):
            raise ExactKernelRefusal(
                "target worker omitted {} convergence evidence".format(solver_name)
            )
        if solver.get("converged") is not True:
            identity = {
                key: task[key]
                for key in (
                    "resolution",
                    "role",
                    "phase",
                    "q",
                    "source_q",
                    "lower",
                    "upper",
                )
                if key in task
            }
            raise ExactKernelRefusal(
                "target numerical convergence failure solver={} task={} evidence={}".format(
                    solver_name, identity, jsonable(solver)
                )
            )


def hostile_admission_worker_l14(task: dict[str, Any]) -> dict[str, Any]:
    repair, _a, _b, _c, _d = load_frozen()
    _install_hostile_worker_capacity(repair, int(task["out_q"]))
    worker = _remember_worker(repair.hostile_parallel, "hostile_admission_worker")
    return worker(task)


def hostile_route_worker_l14(task: dict[str, Any]) -> dict[str, Any]:
    repair, _a, _b, _c, _d = load_frozen()
    _install_hostile_worker_capacity(repair, task_q("hostile", task))
    result = _normalize_hostile_method(repair.hostile_route_worker_v003(task))
    _require_hostile_convergence(task, result)
    return result


def hostile_terminal_worker_l14(task: dict[str, Any]) -> dict[str, Any]:
    repair, _a, _b, _c, _d = load_frozen()
    _install_hostile_worker_capacity(repair, task_q("hostile", task))
    result = _normalize_hostile_method(repair.hostile_terminal_worker_v003(task))
    _require_hostile_convergence(task, result)
    return result


def _require_hostile_convergence(
    task: Mapping[str, Any], result: Mapping[str, Any]
) -> None:
    """Refuse an exhausted Hostile recurrence at its originating window."""

    method = result.get("method")
    if not isinstance(method, Mapping):
        raise ExactKernelRefusal("hostile worker omitted convergence evidence")
    if method.get("converged") is not True:
        identity = {
            key: task[key]
            for key in (
                "accuracy",
                "phase",
                "q",
                "prefix",
                "lower",
                "upper",
                "mutate",
            )
            if key in task
        }
        raise ExactKernelRefusal(
            "hostile numerical convergence failure task={} evidence={}".format(
                identity, jsonable(method)
            )
        )


def _remove_owned(path: Path, owner: Path) -> None:
    path = path.resolve()
    owner = owner.resolve()
    if path == owner or owner not in path.parents:
        raise ExactKernelRefusal("refuse unsafe owned cleanup: {}".format(path))
    if path.exists():
        shutil.rmtree(path)


def _make_writeable(root: Path) -> None:
    for path in root.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o600)
        elif path.is_dir():
            os.chmod(path, 0o700)
    os.chmod(root, 0o700)


def _copy_state(source: Path, destination: Path) -> None:
    if destination.exists():
        raise ExactKernelRefusal("copy destination already exists: {}".format(destination))
    shutil.copytree(source, destination, copy_function=shutil.copyfile)
    _make_writeable(destination)


def _state_record(state: Path, suffix: str) -> Dict[str, Any]:
    members = state_census(state, suffix)
    for member in members:
        path = state / member["path"]
        if stat.S_IMODE(path.stat().st_mode) & 0o222:
            raise ExactKernelRefusal("committed state member remains writable")
        member["sha256"] = sha256_file(path)
    return {
        "path": str(state.resolve()),
        "bytes": directory_bytes(state, suffix),
        "members": members,
        "read_only": True,
    }


def _verify_state(record: Mapping[str, Any], suffix: str) -> Path:
    path = Path(str(record.get("path", "")))
    if not path.is_dir() or path.is_symlink():
        raise ExactKernelRefusal("committed state is absent")
    observed = state_census(path, suffix)
    expected = record.get("members")
    if not isinstance(expected, list) or len(observed) != len(expected):
        raise ExactKernelRefusal("committed state census mismatch")
    for actual, frozen in zip(observed, expected):
        if actual != {key: frozen.get(key) for key in ("path", "bytes")}:
            raise ExactKernelRefusal("committed state census mismatch")
        if sha256_file(path / actual["path"]) != frozen.get("sha256"):
            raise ExactKernelRefusal("committed state hash mismatch")
        if stat.S_IMODE((path / actual["path"]).stat().st_mode) & 0o222:
            raise ExactKernelRefusal("committed state member is writable")
    if directory_bytes(path, suffix) != record.get("bytes"):
        raise ExactKernelRefusal("committed state byte mismatch")
    return path


def _resolution_paths(history_root: Path, label: str) -> Tuple[Path, Path, Path]:
    base = history_root / label
    return base, base / "states", base / "events"


def _authenticate_summary(
    summary: Mapping[str, Any], branch: str, label: str, suffix: str
) -> Dict[str, Any]:
    """Fail closed when a resumed summary or retained sharp state changed."""

    rows = summary.get("rows")
    if not isinstance(rows, list) or len(rows) != LENGTH:
        raise ExactKernelRefusal("{} summary row census mismatch".format(branch.title()))
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("event") != index + 1:
            raise ExactKernelRefusal("{} summary event sequence mismatch".format(branch.title()))
        if bool(row.get("terminal_children_streamed")) != (index == LENGTH - 1):
            raise ExactKernelRefusal("{} summary terminal sequence mismatch".format(branch.title()))
    retained = summary.get("terminal_state_retained")
    if retained is not (label == "sharp"):
        raise ExactKernelRefusal("{} summary retained-state identity mismatch".format(branch.title()))
    shards = summary.get("terminal_shards")
    if not isinstance(shards, list) or len(shards) != (LENGTH if label == "sharp" else 0):
        raise ExactKernelRefusal("{} summary terminal shard census mismatch".format(branch.title()))
    for q, record in enumerate(shards):
        if not isinstance(record, dict) or record.get("q") != q:
            raise ExactKernelRefusal("{} terminal shard identity mismatch".format(branch.title()))
        path = Path(str(record.get("path", "")))
        if (
            not path.is_file()
            or path.is_symlink()
            or path.suffix != suffix
            or path.stat().st_size != record.get("bytes")
            or sha256_file(path) != record.get("sha256")
        ):
            raise ExactKernelRefusal("{} terminal shard authentication failed".format(branch.title()))
        if stat.S_IMODE(path.stat().st_mode) & 0o222:
            raise ExactKernelRefusal("{} terminal shard is writable".format(branch.title()))
    return dict(summary)


def _load_prefix(base: Path, states: Path, events: Path, suffix: str) -> Tuple[int, Path, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    prefix = 0
    state = states / "prefix_00"
    for event in range(LENGTH):
        record_path = events / "event_{:02d}.json".format(event + 1)
        if not record_path.exists():
            break
        record = read_json(record_path)
        if record.get("schema") != "L14_EXACT_EVENT_COMMIT_V002" or record.get("event") != event + 1:
            raise ExactKernelRefusal("event commit identity mismatch: {}".format(record_path))
        rows.append(record["row"])
        if event < LENGTH - 1:
            prefix = event + 1
            # Earlier committed prefix states are deliberately deleted only
            # after their successor event is durable.  Authenticate the most
            # recent surviving state after the journal scan, not every
            # historical state referenced by the audit trail.
            state = Path(str(record["state"].get("path", "")))
    if not state.is_dir():
        raise ExactKernelRefusal("current committed prefix state is absent")
    if rows:
        last_nonterminal = min(len(rows), LENGTH - 1) - 1
        if last_nonterminal >= 0:
            record = read_json(events / "event_{:02d}.json".format(last_nonterminal + 1))
            state = _verify_state(record["state"], suffix)
    return prefix, state, rows


def _commit_event(
    events: Path,
    event: int,
    row: Mapping[str, Any],
    state: Path,
    suffix: str,
    terminal: bool,
) -> None:
    record = {
        "schema": "L14_EXACT_EVENT_COMMIT_V002",
        "event": event + 1,
        "terminal": terminal,
        "row": jsonable(row),
        "state": _state_record(state, suffix),
    }
    immutable_json(events / "event_{:02d}.json".format(event + 1), record)


def _new_pool(repair: Any, branch: str, cache_root: Path, manifest_hash: str, context: Mapping[str, Any]) -> Any:
    runtime = repair.target_parallel.parallel_runtime if hasattr(repair.target_parallel, "parallel_runtime") else __import__("parallel_runtime")
    workers = int(context["workers"])
    pool_type = make_bounded_pool_type(runtime)
    # The finite value is accepted only by the frozen constructor.  V003's
    # parent map and worker context intentionally do not enforce it.
    construction_deadline = time.monotonic() + float(runtime.HARD_WALL_LIMIT_SECONDS)
    with one_node_pool_capacity(runtime, branch, workers):
        pool = pool_type(
            branch=branch,
            cache_root=cache_root.resolve(),
            manifest_sha256=manifest_hash,
            length=LENGTH,
            deadline_monotonic=construction_deadline,
            max_workers=workers,
            reservation_budget_bytes=NUMERICAL_RESERVATION_BUDGET_BYTES,
        )
    return pool


def _full_history_plan(repair: Any, branch: str) -> Dict[str, int]:
    """Return the exact denominator for both complete L14 resolutions."""

    if branch == "target":
        _install_target_parent_capacity(repair)
        return dict(repair.target_parallel.target_run_plan(LENGTH))
    if branch == "hostile":
        _install_hostile_parent_capacity(repair)
        return dict(repair.hostile_parallel.hostile_run_plan(LENGTH))
    raise ValueError("branch must be target or hostile")


def _target_resolution(
    repair: Any,
    cache_root: Path,
    manifest_hash: str,
    history_root: Path,
    scratch_root: Path,
    label: str,
    context: Mapping[str, Any],
    pool: Any,
) -> Dict[str, Any]:
    target = repair.target
    runtime = __import__("parallel_runtime")
    base, states, events = _resolution_paths(history_root, label)
    base.mkdir(parents=True, exist_ok=True)
    states.mkdir(parents=True, exist_ok=True)
    events.mkdir(parents=True, exist_ok=True)
    summary_path = base / "SUMMARY.json"
    if summary_path.exists():
        return _authenticate_summary(read_json(summary_path), "target", label, ".npy")
    initial = states / "prefix_00"
    if not initial.exists():
        target.v004.create_blank(initial)
        chmod_tree_readonly(initial)
    prefix, state, rows = _load_prefix(base, states, events, ".npy")

    cache = runtime.ManifestMemmapCache(str(cache_root), manifest_hash, "target", LENGTH)
    facade = repair.target_parallel.TargetWorkerCache(cache)
    target.CACHE = facade
    target.v004.sealed.fixed_words = target.cached_fixed_words
    target.v004.sealed.Sector = target.CachedSector
    _install_target_parent_capacity(repair)
    adapter = repair.TargetRepairAdapter.__new__(repair.TargetRepairAdapter)
    adapter.pool = pool
    adapter._originals = None
    edges = target.v004.sealed.graph(LENGTH)
    connectors = [index for index, edge in enumerate(edges) if edge[2] == "connector"]
    incidence = np.zeros((2 * LENGTH, len(edges)), dtype=np.int8)
    for edge_index, (left, right, _role) in enumerate(edges):
        incidence[left, edge_index] = 1
        incidence[right, edge_index] = -1
    resolution = repair.TARGET_COARSE if label == "rough" else repair.TARGET_FINE
    peak = directory_bytes(states, ".npy")
    try:
        while len(rows) < LENGTH:
            event = len(rows)
            prefix = event
            state = states / "prefix_{:02d}".format(prefix)
            before_stats = target.v004.statistics(LENGTH, state, prefix, cursor=event)
            disposable = scratch_root / label / "event_{:02d}".format(event + 1)
            if disposable.exists():
                _remove_owned(disposable, scratch_root)
            disposable.parent.mkdir(parents=True, exist_ok=True)
            if event < LENGTH - 1:
                staging = states / ".event_{:02d}_staging".format(event + 1)
                if staging.exists():
                    _remove_owned(staging, states)
                null_state = disposable / "null"
                _copy_state(state, null_state)
                adapter.create_admitted(LENGTH, state, prefix, event, staging)
                admitted = target.v004.statistics(LENGTH, staging, prefix + 1)
                actual_current, actual_solver, null_current, null_solver = adapter.route_pair(
                    LENGTH, staging, prefix + 1, null_state, prefix, resolution
                )
                after = target.v004.statistics(LENGTH, staging, prefix + 1)
                row = target.v004.make_row(
                    LENGTH,
                    event,
                    before_stats,
                    admitted["weights"],
                    admitted["occupation"],
                    after["weights"],
                    after["occupation"],
                    actual_current,
                    null_current,
                    actual_solver,
                    null_solver,
                    incidence,
                    connectors,
                    0.0,
                    False,
                )
                final = states / "prefix_{:02d}".format(event + 1)
                if final.exists():
                    _remove_owned(final, states)
                chmod_tree_readonly(staging)
                staging.rename(final)
                _commit_event(events, event, row, final, ".npy", False)
                if state.exists():
                    _remove_owned(state, states)
                _remove_owned(disposable, scratch_root)
                state = final
            else:
                terminal = adapter.terminal_stream(LENGTH, state, prefix, event, resolution)
                row = target.v004.make_row(
                    LENGTH,
                    event,
                    before_stats,
                    terminal["admitted_weights"],
                    terminal["admitted_occupation"],
                    terminal["after_weights"],
                    terminal["after_occupation"],
                    terminal["actual_current"],
                    terminal["null_current"],
                    terminal["actual_solver"],
                    terminal["null_solver"],
                    incidence,
                    connectors,
                    terminal["blocked_error"],
                    True,
                )
                _commit_event(events, event, row, state, ".npy", True)
            rows.append(jsonable(row))
            peak = max(peak, directory_bytes(states, ".npy"))
            immutable_json(events / "progress_{:02d}_of_14.json".format(event + 1), {
                "schema": "L14_PARENT_PROGRESS_V002", "completed_events": event + 1,
                "total_events": LENGTH, "branch": "target", "resolution": label,
            })
    finally:
        cache.close()
    terminal_shards = []
    if label == "sharp":
        for q in range(LENGTH):
            path = state / "q_{:02d}.npy".format(q)
            terminal_shards.append({
                "q": q, "path": str(path.resolve()), "bytes": path.stat().st_size,
                "sha256": sha256_file(path), "shape": list(target.v004.shape(LENGTH, LENGTH - 1, q)),
            })
    summary = {
        "rows": rows,
        "dimension": math.comb(3 * LENGTH, LENGTH),
        "preterminal_dimension": math.comb(3 * LENGTH - 1, LENGTH - 1),
        "edges": len(edges),
        "peak_retained_state_bytes": peak,
        "terminal_state_retained": label == "sharp",
        "terminal_shards": terminal_shards,
    }
    immutable_json(summary_path, summary)
    if label == "rough" and state.exists():
        _remove_owned(state, states)
    return summary


def _hostile_row(hostile: Any, event: int, before: Mapping[str, Any], admitted: Mapping[str, Any], after: Mapping[str, Any], null_after: Mapping[str, Any], actual_flux: np.ndarray, null_flux: np.ndarray, actual_method: Mapping[str, Any], null_method: Mapping[str, Any], allowed: float, blocked: float, blocked_error: float, incidence: np.ndarray, connectors: np.ndarray, terminal: bool) -> Dict[str, Any]:
    write = float(admitted["retained"]) - float(before["retained"])
    actual_node = after["occupation"] - admitted["occupation"] + incidence @ actual_flux
    null_node = null_after["occupation"] - before["occupation"] + incidence @ null_flux
    delta = actual_flux - null_flux
    return {
        "event": event + 1,
        "input_prefix": event,
        "input_prefix_dimension": hostile.v3.prefix_dimension(event),
        "logical_output_prefix_dimension": hostile.v3.prefix_dimension(event + 1),
        "terminal_children_streamed": terminal,
        "allow_probability": allowed,
        "blocked_probability": blocked,
        "reverse_support_probability": 0.0,
        "blocked_null_state_error": blocked_error,
        "W_n": write,
        "q_retained_after_transport": float(after["retained"]),
        "q_genesis_after": float(after["remaining"]),
        "sector_weights": after["sectors"].tolist(),
        "connector_delta_l1": float(np.sum(np.abs(delta[connectors]))),
        "connector_delta_signed": float(np.sum(delta[connectors])),
        "admission_total_content_residual": write + float(admitted["remaining"]) - float(before["remaining"]),
        "admission_bandwidth_residual": float(admitted["remaining"]) - float(before["remaining"]) + write,
        "target_owner_residual": float(admitted["occupation"][event]) - float(before["occupation"][event]) - write,
        "transport_node_residual_l1": float(np.sum(np.abs(actual_node))),
        "transport_node_residual_linf": float(np.max(np.abs(actual_node))),
        "null_transport_node_residual_l1": float(np.sum(np.abs(null_node))),
        "transport_number_drift": abs(float(after["retained"]) - float(admitted["retained"])),
        "null_transport_number_drift": abs(float(null_after["retained"]) - float(before["retained"])),
        "actual_norm_error": abs(float(after["norm"]) - 1.0),
        "null_norm_error": abs(float(null_after["norm"]) - 1.0),
        "actual_solver": jsonable(actual_method),
        "null_solver": jsonable(null_method),
    }


def _hostile_resolution(repair: Any, cache_root: Path, manifest_hash: str, history_root: Path, scratch_root: Path, label: str, context: Mapping[str, Any], pool: Any) -> Dict[str, Any]:
    hostile = repair.hostile
    runtime = __import__("parallel_runtime")
    base, states, events = _resolution_paths(history_root, label)
    base.mkdir(parents=True, exist_ok=True)
    states.mkdir(parents=True, exist_ok=True)
    events.mkdir(parents=True, exist_ok=True)
    summary_path = base / "SUMMARY.json"
    if summary_path.exists():
        return _authenticate_summary(read_json(summary_path), "hostile", label, ".c128")
    cache = runtime.ManifestMemmapCache(str(cache_root), manifest_hash, "hostile", LENGTH)
    facade = repair.hostile_parallel.HostileWorkerCache(cache)
    hostile.legacy.configure(LENGTH, facade, 0.0)
    _install_hostile_parent_capacity(repair)
    initial = states / "prefix_00"
    if not initial.exists():
        hostile.v3.create_blank(states)
        chmod_tree_readonly(initial)
    prefix, state_path, rows = _load_prefix(base, states, events, ".c128")
    adapter = repair.HostileRepairAdapter.__new__(repair.HostileRepairAdapter)
    adapter.pool = pool
    adapter._originals = None
    accuracy = repair.HOSTILE_ROUGH if label == "rough" else repair.HOSTILE_SHARP
    edges = hostile.physical.hostile_edges(LENGTH)
    connectors = np.asarray([index for index, edge in enumerate(edges) if edge[2] == "connector"], dtype=np.int32)
    incidence = np.zeros((2 * LENGTH, len(edges)), dtype=np.int8)
    for index, (left, right, _role) in enumerate(edges):
        incidence[left, index] = 1
        incidence[right, index] = -1
    peak = directory_bytes(states, ".c128")
    try:
        while len(rows) < LENGTH:
            event = len(rows)
            state_path = states / "prefix_{:02d}".format(event)
            committed = hostile.v3.DiskPrefix(states, event)
            disposable = scratch_root / label / "event_{:02d}".format(event + 1)
            if disposable.exists():
                _remove_owned(disposable, scratch_root)
            disposable.parent.mkdir(parents=True, exist_ok=True)
            if event < LENGTH - 1:
                staging = states / ".event_{:02d}_staging".format(event + 1)
                if staging.exists():
                    _remove_owned(staging, states)
                staging.mkdir(parents=True)
                staged_old = staging / "prefix_{:02d}".format(event)
                _copy_state(state_path, staged_old)
                old_state = hostile.v3.DiskPrefix(staging, event)
                admitted_state, blocked_error = adapter.admit_to_next(old_state, event, edges)
                admitted, after, actual_flux, actual_method, _unused_allow, _unused_blocked = adapter.route_disk_state(admitted_state, accuracy, edges, True)
                before, null_after, null_flux, null_method, allowed, blocked = adapter.route_disk_state(committed, accuracy, edges, False, classify_event=event)
                row = _hostile_row(hostile, event, before, admitted, after, null_after, actual_flux, null_flux, actual_method, null_method, allowed, blocked, blocked_error, incidence, connectors, False)
                staged_final = staging / "prefix_{:02d}".format(event + 1)
                final = states / "prefix_{:02d}".format(event + 1)
                if final.exists():
                    _remove_owned(final, states)
                chmod_tree_readonly(staged_final)
                staged_final.rename(final)
                _commit_event(events, event, row, final, ".c128", False)
                _remove_owned(staging, states)
                _remove_owned(state_path, states)
                state_path = final
            else:
                values = adapter.terminal_route(committed, accuracy, edges)
                before, admitted, after, null_after, actual_flux, null_flux, actual_method, null_method, allowed, blocked, blocked_error = values
                row = _hostile_row(hostile, event, before, admitted, after, null_after, actual_flux, null_flux, actual_method, null_method, allowed, blocked, blocked_error, incidence, connectors, True)
                _commit_event(events, event, row, state_path, ".c128", True)
            rows.append(jsonable(row))
            peak = max(peak, directory_bytes(states, ".c128"))
            immutable_json(events / "progress_{:02d}_of_14.json".format(event + 1), {
                "schema": "L14_PARENT_PROGRESS_V002", "completed_events": event + 1,
                "total_events": LENGTH, "branch": "hostile", "resolution": label,
            })
    finally:
        cache.close()
    terminal_shards = []
    if label == "sharp":
        final_state = hostile.v3.DiskPrefix(states, LENGTH - 1)
        final_state.verify_complete()
        for q in range(LENGTH):
            path = final_state.path(q)
            terminal_shards.append({
                "q": q, "path": str(path.resolve()), "bytes": path.stat().st_size,
                "sha256": sha256_file(path), "shape": list(hostile.v3.shard_shape(LENGTH - 1, q)),
            })
    summary = {
        "rows": rows,
        "full_dimension": hostile.v3.prefix_dimension(LENGTH),
        "largest_materialized_dimension": hostile.v3.prefix_dimension(LENGTH - 1),
        "peak_retained_state_bytes": peak,
        "terminal_state_retained": label == "sharp",
        "terminal_shards": terminal_shards,
        "edge_layout": [list(edge) for edge in edges],
    }
    immutable_json(summary_path, summary)
    if label == "rough" and state_path.exists():
        _remove_owned(state_path, states)
    return summary


def _comparison_evidence(branch: str, rough: Mapping[str, Any], sharp: Mapping[str, Any], comparison: Mapping[str, Any]) -> Dict[str, Any]:
    """Persist the V002 diagnostic's exact original predicates before the gate."""

    diagnostic_module = __import__("comparison_gate")
    diagnostic = (
        diagnostic_module.target_diagnostic(LENGTH, dict(rough), dict(sharp), dict(comparison))
        if branch == "target"
        else diagnostic_module.hostile_diagnostic(LENGTH, dict(rough), dict(sharp), dict(comparison))
    )
    raw = diagnostic["raw_metrics"]
    by_name = {row["name"]: row for row in diagnostic["predicates"]}
    names = {
        "reverse_support_probability": "maximum_reverse_support_probability",
        "transport_node_residual_l1": (
            "maximum_transport_node_residual_l1"
            if branch == "target"
            else "maximum_node_continuity_residual_l1"
        ),
        "actual_norm_error": (
            "maximum_actual_norm_error" if branch == "target" else "maximum_norm_error"
        ),
        "transport_number_drift": (
            "maximum_transport_number_drift" if branch == "target" else "maximum_number_drift"
        ),
    }
    return {
        "raw_metrics": raw,
        "predicate_thresholds": {
            metric: {
                "operator": by_name[predicate]["operator"],
                "value": by_name[predicate]["threshold"],
            }
            for metric, predicate in names.items()
        },
        "predicates": diagnostic["predicates"],
        "computed_resolved": diagnostic["computed_resolved"],
        "reported_resolved": diagnostic["reported_resolved"],
        "resolved_agrees_with_predicates": diagnostic["resolved_agrees_with_predicates"],
        "comparison": jsonable(comparison),
        "branch": branch,
    }


def _sector_masses(rows: list[Mapping[str, Any]]) -> Dict[str, str]:
    late = rows[math.ceil(LENGTH / 2) - 1 :]
    average = np.mean(np.asarray([row["sector_weights"] for row in late], dtype=np.float64), axis=0)
    return {str(q): format(float(average[q]), ".17g") for q in range(4, 10)}


def prepare_history(branch: str, context: Mapping[str, Any]) -> Dict[str, Any]:
    repair, _target_response, _hostile_response, _classifier, _interval = load_frozen()
    shared = require_safe_root(Path(str(context["shared_root"])) / branch, "retained branch")
    scratch = require_safe_root(Path(str(context["scratch_root"])) / branch, "local scratch")
    cache_root = shared / "cache_l14"
    manifest_hash, _manifest = authenticate_cache(cache_root, branch, LENGTH)
    history_root = shared / "history_l14"
    history_root.mkdir(parents=True, exist_ok=True)
    resolution = _target_resolution if branch == "target" else _hostile_resolution
    summaries_complete = all(
        (history_root / label / "SUMMARY.json").is_file()
        for label in ("rough", "sharp")
    )
    pool = None
    if not summaries_complete:
        # Unlike the older Hostile repair helper, this is the actual full
        # rough plus full sharp history executed below, including every sharp
        # admission and intermediate route.
        plan = _full_history_plan(repair, branch)
        pool = _new_pool(repair, branch, cache_root, manifest_hash, context)
        pool.set_run_plan(**plan)
    try:
        rough = resolution(
            repair, cache_root, manifest_hash, history_root, scratch, "rough", context, pool
        )
        sharp = resolution(
            repair, cache_root, manifest_hash, history_root, scratch, "sharp", context, pool
        )
        if pool is not None:
            pool.assert_run_complete()
    finally:
        if pool is not None:
            pool.close(wait=True)
    comparison = repair.target.v004.sealed.summarize(LENGTH, rough, sharp) if branch == "target" else repair.hostile.physical.compare(LENGTH, rough, sharp)
    comparison_evidence = _comparison_evidence(branch, rough, sharp, comparison)
    pre_gate = history_root / "PRE_GATE_COMPARISON.json"
    immutable_json(pre_gate, {
        "schema": "L14_PRE_GATE_COMPARISON_V002",
        "branch": branch,
        "comparison_evidence": comparison_evidence,
    })
    if comparison.get("resolved") is not True:
        failure = history_root / "UNRESOLVED_COMPARISON.json"
        immutable_json(failure, {
            "branch": branch,
            "comparison": comparison,
            "comparison_evidence": comparison_evidence,
        })
        raise ExactKernelRefusal("{} original rough/sharp comparison unresolved".format(branch))
    if (
        comparison_evidence.get("computed_resolved") is not True
        or comparison_evidence.get("reported_resolved") is not True
        or comparison_evidence.get("resolved_agrees_with_predicates") is not True
    ):
        raise ExactKernelRefusal("{} exact comparison diagnostic disagrees with resolved gate".format(branch))
    final = {
        "schema": "L14_EXACT_HISTORY_PREPARATION_V002",
        "branch": branch,
        "length": LENGTH,
        "cache_manifest_sha256": manifest_hash,
        "rough": rough,
        "sharp": sharp,
        "comparison_evidence": comparison_evidence,
        "sector_masses": _sector_masses(sharp["rows"]),
        "capacity_successor": {
            "physics_or_tolerance_changed": False,
            "workspace_policy": "Q_AWARE_L14_COMPLETE_ROW_RESERVATIONS",
            "target_numerical_workset_limit_bytes": TARGET_CAP_BYTES,
            "hostile_numerical_workspace_limit_bytes": HOSTILE_WORKSPACE_BYTES,
            "target_maximum_numerical_workset_limit_bytes": TARGET_CAP_BYTES,
            "hostile_maximum_numerical_workspace_limit_bytes": HOSTILE_WORKSPACE_BYTES,
            "numerical_reservation_budget_bytes": NUMERICAL_RESERVATION_BUDGET_BYTES,
            "live_rss_or_hardware_polling": False,
            "automatic_wall_time_cancellation": False,
            "retained_logical_scratch_limit_bytes": LOGICAL_SCRATCH_BYTES,
        },
    }
    path = history_root / "HISTORY_PREPARATION.json"
    immutable_json(path, final)
    post_hash, _post = authenticate_cache(cache_root, branch, LENGTH)
    if post_hash != manifest_hash:
        raise ExactKernelRefusal("cache changed during exact history")
    return {"history": final, "artifacts": [artifact(path), artifact(pre_gate), artifact(cache_root / "CACHE_MANIFEST.json")]}
