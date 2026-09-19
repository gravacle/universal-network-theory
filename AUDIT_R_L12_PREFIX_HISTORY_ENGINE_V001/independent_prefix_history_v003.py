#!/usr/bin/env python3
"""Q-sharded hostile L12 prefix-history engine; execution is gate locked."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import mmap
import resource
import shutil
import time
from pathlib import Path

import numpy as np

import independent_prefix_history as physical
import independent_prefix_history_v002 as replay


HERE = Path(__file__).resolve().parent
METHOD = HERE / "V003_L12_EXECUTABLE_METHOD.md"
MANIFEST = HERE / "FROZEN_MANIFEST_V003.json"
L10_GATE = HERE / "L10_GATE_V002.json"
LENGTH = 12
WORKSPACE_LIMIT = 1_400_000_000
IO_WINDOW_LIMIT = 512 * 2**20
SCRATCH_LIMIT = 20 * 2**30
RSS_LIMIT = 16 * 2**30
WALL_LIMIT = 6 * 3600.0
EXPECTED_FULL = 1_251_677_700
EXPECTED_PRETERMINAL = 417_225_900
EXPECTED_CHILD1_INPUT = 286_097_760
EXPECTED_LIVE_ENTRIES = 548_354_040
EXPECTED_LIVE_BYTES = 8_773_664_640
EXECUTION_STARTED: float | None = None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def colex_rank(mask: int) -> int:
    rank = 0
    ordinal = 1
    bit = 0
    value = mask
    while value:
        if value & 1:
            rank += math.comb(bit, ordinal)
            ordinal += 1
        bit += 1
        value >>= 1
    return rank


def reverse_rank(width: int, weight: int, mask: int) -> int:
    if mask < 0 or mask >= (1 << width) or bin(mask).count("1") != weight:
        raise ValueError("mask outside reverse fixed-weight block")
    return math.comb(width, weight) - 1 - colex_rank(mask)


def prefix_dimension(prefix: int) -> int:
    direct = sum(math.comb(prefix, q) * math.comb(2 * LENGTH, q)
                 for q in range(prefix + 1))
    closed = math.comb(2 * LENGTH + prefix, prefix)
    if direct != closed:
        raise AssertionError("prefix Vandermonde identity")
    return direct


def shard_shape(prefix: int, q: int) -> tuple[int, int]:
    if not 0 <= q <= prefix <= LENGTH:
        raise ValueError("invalid prefix shard")
    return math.comb(prefix, q), math.comb(2 * LENGTH, q)


def shard_bytes(prefix: int, q: int) -> int:
    rows, columns = shard_shape(prefix, q)
    return rows * columns * 16


def close_memmap(array: np.memmap, write: bool = False) -> None:
    if write:
        array.flush()
    mapping = getattr(array, "_mmap", None)
    if mapping is not None:
        try:
            mapping.madvise(mmap.MADV_DONTNEED)
        except (AttributeError, OSError):
            pass
        mapping.close()


def guard_rss() -> None:
    observed = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if observed > RSS_LIMIT:
        raise MemoryError(f"process RSS guard exceeded: {observed} > {RSS_LIMIT}")
    if EXECUTION_STARTED is not None:
        elapsed = time.perf_counter() - EXECUTION_STARTED
        if elapsed > WALL_LIMIT:
            raise TimeoutError(f"method wall guard exceeded: {elapsed} > {WALL_LIMIT}")


class DiskPrefix:
    def __init__(self, root: Path, prefix: int):
        self.root = root
        self.prefix = prefix

    @property
    def directory(self) -> Path:
        return self.root / f"prefix_{self.prefix:02d}"

    def path(self, q: int) -> Path:
        return self.directory / f"q_{q:02d}.c128"

    def create(self) -> None:
        if self.directory.exists():
            raise FileExistsError(f"prefix directory already exists: {self.directory}")
        self.directory.mkdir(parents=True)

    def create_shard(self, q: int) -> np.memmap:
        expected = shard_bytes(self.prefix, q)
        if expected > SCRATCH_LIMIT:
            raise MemoryError(f"single logical shard exceeds scratch guard: {expected}")
        return np.memmap(
            self.path(q), dtype=np.complex128, mode="w+", shape=shard_shape(self.prefix, q)
        )

    def open_shard(self, q: int, mode: str = "r") -> np.memmap:
        path = self.path(q)
        expected = shard_bytes(self.prefix, q)
        if not path.exists() or path.stat().st_size != expected:
            raise RuntimeError(f"shard custody/size failure: {path}")
        return np.memmap(path, dtype=np.complex128, mode=mode,
                         shape=shard_shape(self.prefix, q))

    def logical_bytes(self) -> int:
        return sum(shard_bytes(self.prefix, q) for q in range(self.prefix + 1))

    def verify_complete(self) -> None:
        for q in range(self.prefix + 1):
            path = self.path(q)
            if not path.exists() or path.stat().st_size != shard_bytes(self.prefix, q):
                raise RuntimeError(f"incomplete prefix state: {path}")

    def remove(self) -> None:
        self.verify_complete()
        for q in range(self.prefix + 1):
            self.path(q).unlink()
        self.directory.rmdir()


def empty_statistics() -> dict[str, object]:
    return {
        "norm": 0.0,
        "sectors": np.zeros(LENGTH + 1),
        "occupation": np.zeros(2 * LENGTH),
        "retained": 0.0,
        "remaining": 0.0,
    }


def add_statistics(statistics: dict[str, object], carrier: physical.CarrierBlock,
                   q: int, vector: np.ndarray) -> None:
    probability = np.sum(np.abs(vector) ** 2, axis=0)
    norm = float(np.sum(probability))
    statistics["norm"] = float(statistics["norm"]) + norm
    statistics["sectors"][q] += norm
    statistics["retained"] = float(statistics["retained"]) + q * norm
    statistics["remaining"] = float(statistics["remaining"]) + (LENGTH - q) * norm
    for site in range(2 * LENGTH):
        statistics["occupation"][site] += float(
            np.sum(probability[((carrier.words >> site) & 1) != 0])
        )


def io_rows(columns: int) -> int:
    one_row = columns * 16
    if one_row > IO_WINDOW_LIMIT:
        raise MemoryError(f"one row exceeds I/O window: {one_row} > {IO_WINDOW_LIMIT}")
    rows = IO_WINDOW_LIMIT // one_row
    if rows < 1:
        raise MemoryError("no complete lineage row fits I/O window")
    return int(rows)


def lineage_row_map(old_prefix: int, q: int, event: int, add_event: bool) -> np.ndarray:
    words = physical.reverse_masks(old_prefix, q)
    weight = q + int(add_event)
    mapped = np.fromiter(
        (reverse_rank(old_prefix + 1, weight,
                      int(word) | ((1 << event) if add_event else 0))
         for word in words),
        dtype=np.int32,
        count=len(words),
    )
    if len(np.unique(mapped)) != len(mapped):
        raise AssertionError("lineage row map is not injective")
    return mapped


def construct_carrier(q: int, edges: list[tuple[int, int, str]]) -> physical.CarrierBlock:
    block = physical.CarrierBlock(LENGTH, q, edges)
    exchange_bytes = sum(source.nbytes + target.nbytes
                         for source, target in block.exchanges)
    word_bytes = block.words.nbytes
    if exchange_bytes + word_bytes > 2 * 2**30:
        raise MemoryError(
            f"one-q carrier arrays exceed 2 GiB: q={q} bytes={exchange_bytes + word_bytes}"
        )
    guard_rss()
    return block


def create_blank(root: Path) -> DiskPrefix:
    state = DiskPrefix(root, 0)
    state.create()
    shard = state.create_shard(0)
    shard[0, 0] = 1.0
    close_memmap(shard, write=True)
    return state


def admit_to_next(state: DiskPrefix, event: int,
                  edges: list[tuple[int, int, str]]) -> tuple[DiskPrefix, float]:
    if state.prefix != event or event >= LENGTH - 1:
        raise AssertionError("nonterminal admission prefix mismatch")
    output = DiskPrefix(state.root, event + 1)
    output.create()
    cosine = math.cos(physical.ANGLE)
    sine = math.sin(physical.ANGLE)
    blocked_error = 0.0
    for out_q in range(event + 2):
        carrier = construct_carrier(out_q, edges)
        target = output.create_shard(out_q)
        # A new memmap is zero-filled by file extension. Only authenticated
        # child support is assigned below.
        if out_q <= event:
            source = state.open_shard(out_q)
            target_rows = lineage_row_map(event, out_q, event, False)
            blank = ((carrier.words >> event) & 1) == 0
            factors = np.where(blank, cosine, 1.0)
            step = io_rows(len(carrier.words))
            for lower in range(0, len(source), step):
                upper = min(len(source), lower + step)
                data = np.array(source[lower:upper], copy=True)
                data *= factors[np.newaxis, :]
                target[target_rows[lower:upper], :] = data
                if np.any(~blank):
                    blocked_error = max(
                        blocked_error,
                        float(np.max(np.abs(data[:, ~blank] - source[lower:upper, ~blank]))),
                    )
            close_memmap(source)
        if out_q >= 1:
            old_q = out_q - 1
            source = state.open_shard(old_q)
            target_rows = lineage_row_map(event, old_q, event, True)
            occupied_columns = np.flatnonzero(((carrier.words >> event) & 1) != 0).astype(np.int32)
            old_columns = np.fromiter(
                (reverse_rank(2 * LENGTH, old_q,
                              int(carrier.words[column]) & ~(1 << event))
                 for column in occupied_columns),
                dtype=np.int32,
                count=len(occupied_columns),
            )
            step = io_rows(max(1, len(old_columns)))
            for lower in range(0, len(source), step):
                upper = min(len(source), lower + step)
                data = -1.0j * sine * np.asarray(source[lower:upper, old_columns])
                target[np.ix_(target_rows[lower:upper], occupied_columns)] = data
            close_memmap(source)
        close_memmap(target, write=True)
        del carrier
        gc.collect()
    output.verify_complete()
    return output, blocked_error


def method_record() -> dict[str, object]:
    return replay.blank_method(0)


def update_method(total: dict[str, object], record: dict[str, object]) -> None:
    replay.combine_method(total, record)


def route_disk_state(state: DiskPrefix, accuracy: physical.Accuracy,
                     edges: list[tuple[int, int, str]], mutate: bool,
                     classify_event: int | None = None
                     ) -> tuple[dict[str, object], dict[str, object], np.ndarray,
                                dict[str, object], float, float]:
    initial = empty_statistics()
    final_stats = empty_statistics()
    integrated = np.zeros(len(edges))
    method = method_record()
    allowed = 0.0
    blocked = 0.0
    for q in range(state.prefix + 1):
        carrier = construct_carrier(q, edges)
        shard = state.open_shard(q, "r+" if mutate else "r")
        step = min(len(shard), replay.safe_batch_rows(
            len(carrier.words), max(accuracy.checkpoints)
        ))
        for lower in range(0, len(shard), step):
            upper = min(len(shard), lower + step)
            vector = np.array(shard[lower:upper], copy=True)
            add_statistics(initial, carrier, q, vector)
            if classify_event is not None:
                blank_columns = ((carrier.words >> classify_event) & 1) == 0
                allowed += float(np.vdot(vector[:, blank_columns], vector[:, blank_columns]).real)
                blocked += float(np.vdot(vector[:, ~blank_columns], vector[:, ~blank_columns]).real)
            final, flux, record = replay.low_memory_evolve_batch(carrier, vector, accuracy)
            guard_rss()
            add_statistics(final_stats, carrier, q, final)
            integrated += flux
            update_method(method, record)
            if mutate:
                shard[lower:upper] = final
        close_memmap(shard, write=mutate)
        del carrier
        gc.collect()
    method["quadrature_nodes"] = accuracy.gauss_order
    method["q_sharded"] = True
    return initial, final_stats, integrated, method, allowed, blocked


def terminal_route(state: DiskPrefix, accuracy: physical.Accuracy,
                   edges: list[tuple[int, int, str]]) -> tuple[
                       dict[str, object], dict[str, object], dict[str, object],
                       dict[str, object],
                       np.ndarray, np.ndarray, dict[str, object], dict[str, object],
                       float, float, float]:
    if state.prefix != LENGTH - 1:
        raise AssertionError("terminal route requires H_11")
    event = LENGTH - 1
    cosine = math.cos(physical.ANGLE)
    sine = math.sin(physical.ANGLE)
    admitted = empty_statistics()
    actual_final = empty_statistics()
    actual_flux = np.zeros(len(edges))
    actual_method = method_record()
    blocked_error = 0.0

    # Child zero: actual carrier number q is the preterminal q.
    for q in range(LENGTH):
        carrier = construct_carrier(q, edges)
        source = state.open_shard(q)
        blank_columns = ((carrier.words >> event) & 1) == 0
        occupied_columns = ~blank_columns
        step = min(len(source), replay.safe_batch_rows(
            len(carrier.words), max(accuracy.checkpoints), physical.TERMINAL_WINDOW_BYTES
        ))
        for lower in range(0, len(source), step):
            upper = min(len(source), lower + step)
            child = np.array(source[lower:upper], copy=True)
            child[:, blank_columns] *= cosine
            if np.any(occupied_columns):
                blocked_error = max(
                    blocked_error,
                    float(np.max(np.abs(
                        child[:, occupied_columns] - source[lower:upper, occupied_columns]
                    ))),
                )
            add_statistics(admitted, carrier, q, child)
            final, flux, record = replay.low_memory_evolve_batch(carrier, child, accuracy)
            guard_rss()
            add_statistics(actual_final, carrier, q, final)
            actual_flux += flux
            update_method(actual_method, record)
        close_memmap(source)
        del carrier
        gc.collect()

    # Child one: construct only the actual q carrier block. Event-occupied
    # columns map uniquely back to the q-1 preterminal carrier rank.
    for q in range(1, LENGTH + 1):
        carrier = construct_carrier(q, edges)
        source = state.open_shard(q - 1)
        occupied_columns = np.flatnonzero(((carrier.words >> event) & 1) != 0).astype(np.int32)
        old_columns = np.fromiter(
            (reverse_rank(2 * LENGTH, q - 1,
                          int(carrier.words[column]) & ~(1 << event))
             for column in occupied_columns),
            dtype=np.int32,
            count=len(occupied_columns),
        )
        step = min(len(source), replay.safe_batch_rows(
            len(carrier.words), max(accuracy.checkpoints), physical.TERMINAL_WINDOW_BYTES
        ))
        for lower in range(0, len(source), step):
            upper = min(len(source), lower + step)
            child = np.zeros((upper - lower, len(carrier.words)), dtype=np.complex128)
            child[:, occupied_columns] = -1.0j * sine * np.asarray(
                source[lower:upper, old_columns]
            )
            add_statistics(admitted, carrier, q, child)
            final, flux, record = replay.low_memory_evolve_batch(carrier, child, accuracy)
            guard_rss()
            add_statistics(actual_final, carrier, q, final)
            actual_flux += flux
            update_method(actual_method, record)
        close_memmap(source)
        del carrier
        gc.collect()

    before, null_final, null_flux, null_method, allowed, blocked = route_disk_state(
        state, accuracy, edges, False, classify_event=event
    )
    actual_method["quadrature_nodes"] = accuracy.gauss_order
    actual_method["q_sharded"] = True
    actual_method["terminal_children_streamed"] = True
    actual_method["terminal_child0_entries"] = EXPECTED_PRETERMINAL
    actual_method["terminal_child1_nonzero_admission_entries"] = EXPECTED_CHILD1_INPUT
    actual_method["full_terminal_array_allocated"] = False
    return (before, admitted, actual_final, null_final, actual_flux, null_flux,
            actual_method, null_method, allowed, blocked, blocked_error)


def workspace_bytes(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*.c128")) if root.exists() else 0


def history(length: int, accuracy: physical.Accuracy, root: Path,
            retain_terminal: bool) -> dict[str, object]:
    if length != LENGTH:
        raise ValueError("V003 executable is the bounded L12 engine")
    if root.exists():
        raise FileExistsError(f"resolution workspace exists: {root}")
    root.mkdir(parents=True)
    edges = physical.hostile_edges(length)
    connectors = np.array([index for index, edge in enumerate(edges)
                           if edge[2] == "connector"], dtype=np.int32)
    incidence = np.zeros((2 * length, len(edges)), dtype=np.int8)
    for index, (u, v, _) in enumerate(edges):
        incidence[u, index] = 1
        incidence[v, index] = -1
    state = create_blank(root)
    rows: list[dict[str, object]] = []
    peak_scratch = workspace_bytes(root)
    for event in range(length):
        if event < length - 1:
            admitted_state, blocked_error = admit_to_next(state, event, edges)
            peak_scratch = max(peak_scratch, workspace_bytes(root))
            if peak_scratch > SCRATCH_LIMIT:
                raise MemoryError(f"live logical scratch exceeded: {peak_scratch}")
            admitted, after, actual_flux, actual_method, _, _ = route_disk_state(
                admitted_state, accuracy, edges, True
            )
            before, null_after, null_flux, null_method, allowed, blocked = route_disk_state(
                state, accuracy, edges, False, classify_event=event
            )
            state.remove()
            state = admitted_state
            terminal = False
        else:
            (before, admitted, after, null_after, actual_flux, null_flux,
             actual_method, null_method, allowed, blocked,
             blocked_error) = terminal_route(state, accuracy, edges)
            terminal = True
        write = float(admitted["retained"]) - float(before["retained"])
        actual_node = after["occupation"] - admitted["occupation"] + incidence @ actual_flux
        null_node = null_after["occupation"] - before["occupation"] + incidence @ null_flux
        delta = actual_flux - null_flux
        rows.append({
            "event": event + 1,
            "input_prefix": event,
            "input_prefix_dimension": prefix_dimension(event),
            "logical_output_prefix_dimension": prefix_dimension(event + 1),
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
            "admission_total_content_residual": (
                write + float(admitted["remaining"]) - float(before["remaining"])
            ),
            "admission_bandwidth_residual": (
                float(admitted["remaining"]) - float(before["remaining"]) + write
            ),
            "target_owner_residual": (
                float(admitted["occupation"][event])
                - float(before["occupation"][event]) - write
            ),
            "transport_node_residual_l1": float(np.sum(np.abs(actual_node))),
            "transport_node_residual_linf": float(np.max(np.abs(actual_node))),
            "null_transport_node_residual_l1": float(np.sum(np.abs(null_node))),
            "transport_number_drift": abs(float(after["retained"]) - float(admitted["retained"])),
            "null_transport_number_drift": abs(
                float(null_after["retained"]) - float(before["retained"])
            ),
            "actual_norm_error": abs(float(after["norm"]) - 1.0),
            "null_norm_error": abs(float(null_after["norm"]) - 1.0),
            "actual_solver": actual_method,
            "null_solver": null_method,
        })
    state.verify_complete()
    retained = [
        {"q": q, "path": str(state.path(q).relative_to(root)),
         "shape": list(shard_shape(length - 1, q)),
         "logical_bytes": shard_bytes(length - 1, q)}
        for q in range(length)
    ]
    if not retain_terminal:
        state.remove()
    return {
        "rows": rows,
        "full_dimension": prefix_dimension(length),
        "largest_materialized_dimension": prefix_dimension(length - 1),
        "peak_logical_scratch_bytes": peak_scratch,
        "terminal_state_retained": retain_terminal,
        "terminal_shards": retained if retain_terminal else [],
        "edge_layout": [list(edge) for edge in edges],
    }


def remove_resolution(root: Path) -> None:
    if not root.exists():
        return
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            path.rmdir()
    root.rmdir()


def require_l12_gate() -> None:
    if not L10_GATE.exists():
        raise RuntimeError("L12 locked: future L10 V002 gate is absent")
    gate = json.loads(L10_GATE.read_text())
    if gate.get("classification") != "PASS_PREFIX_HISTORY_L10_GATE_V002":
        raise RuntimeError("L12 locked: L10 V002 gate did not pass")
    if gate.get("hostile_v003_sha256") != sha256(Path(__file__)):
        raise RuntimeError("L12 locked: L10 gate does not pin V003")
    free = shutil.disk_usage(HERE).free
    if free < SCRATCH_LIMIT:
        raise RuntimeError(f"L12 scratch gate failed: free={free} required={SCRATCH_LIMIT}")


def execute_l12(output: Path, workspace: Path) -> None:
    global EXECUTION_STARTED
    require_l12_gate()
    if output.exists() or workspace.exists():
        raise FileExistsError("refuse to overwrite L12 output or workspace")
    started = time.perf_counter()
    EXECUTION_STARTED = started
    rough_root = workspace / "rough"
    sharp_root = workspace / "sharp"
    rough = history(LENGTH, physical.ROUGH, rough_root, retain_terminal=False)
    remove_resolution(rough_root)
    sharp = history(LENGTH, physical.SHARP, sharp_root, retain_terminal=True)
    comparison = physical.compare(LENGTH, rough, sharp)
    peak_scratch = max(
        int(rough["peak_logical_scratch_bytes"]),
        int(sharp["peak_logical_scratch_bytes"]),
    )
    maximum_allocation = max(
        int(row[key]["maximum_allocation_estimate_bytes"])
        for row in sharp["rows"] for key in ("actual_solver", "null_solver")
    )
    wall = time.perf_counter() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    resource_pass = (
        peak_scratch <= SCRATCH_LIMIT
        and maximum_allocation <= WORKSPACE_LIMIT
        and rss <= RSS_LIMIT
        and wall <= WALL_LIMIT
    )
    if not resource_pass:
        comparison["resolved"] = False
        comparison["classification"] = "EXACT_Q_SHARDED_L12_RESOURCE_OBSTRUCTION"
    result = {
        "schema": "INDEPENDENT_Q_SHARDED_PREFIX_HISTORY_L12_V003",
        "L": LENGTH,
        "events": LENGTH,
        "full_dimension": EXPECTED_FULL,
        "largest_materialized_dimension": EXPECTED_PRETERMINAL,
        "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS",
        "lineage_authority": "FULL_CANONICAL_MASK__SHA256_CUSTODY_ONLY",
        "rows": sharp["rows"],
        "comparison": comparison,
        "terminal_shards": sharp["terminal_shards"],
        "terminal_support": {
            "child0_entries": EXPECTED_PRETERMINAL,
            "child1_nonzero_admission_entries": EXPECTED_CHILD1_INPUT,
            "full_terminal_array_allocated": False,
        },
        "resource": {
            "peak_logical_scratch_bytes": peak_scratch,
            "scratch_limit_bytes": SCRATCH_LIMIT,
            "maximum_numerical_allocation_estimate_bytes": maximum_allocation,
            "numerical_workspace_limit_bytes": WORKSPACE_LIMIT,
            "peak_rss_bytes": rss,
            "rss_limit_bytes": RSS_LIMIT,
            "wall_seconds": wall,
            "wall_limit_seconds": WALL_LIMIT,
            "passed": resource_pass,
        },
        "implementation_sha256": sha256(Path(__file__)),
        "method_sha256": sha256(METHOD),
        "l10_gate_sha256": sha256(L10_GATE),
        "claim_boundary": "INDEPENDENT_FINITE_L12_PREFIX_HISTORY_ONLY",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(comparison["classification"])
    print(f"scratch={peak_scratch} allocation={maximum_allocation} rss={rss} wall={wall:.3f}")
    if not comparison["resolved"]:
        raise SystemExit(2)


def invariant_validation(output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"refuse to overwrite invariant output: {output}")
    manifest = json.loads(MANIFEST.read_text())
    checks: list[tuple[bool, str]] = []
    checks.append((sha256(Path(__file__)) == manifest["files"]["implementation"],
                   "V003 implementation freeze"))
    checks.append((sha256(METHOD) == manifest["files"]["method"], "V003 method freeze"))
    checks.append((not L10_GATE.exists(), "L12 L10-gate absent at invariant validation"))
    index_checks = 0
    for width in range(1, 17):
        for weight in range(width + 1):
            words = physical.reverse_masks(width, weight)
            for index, word in enumerate(words):
                checks.append((reverse_rank(width, weight, int(word)) == index,
                               f"reverse rank w{width} q{weight} i{index}"))
                index_checks += 1
    for weight in range(13):
        words = physical.reverse_masks(24, weight)
        probes = sorted({0, len(words) // 7, len(words) // 3, len(words) // 2,
                         max(0, len(words) - 2), len(words) - 1})
        for index in probes:
            checks.append((reverse_rank(24, weight, int(words[index])) == index,
                           f"reverse rank width24 q{weight} probe{index}"))
    dimensions = [prefix_dimension(prefix) for prefix in range(LENGTH + 1)]
    checks.append((dimensions[-1] == EXPECTED_FULL, "full L12 dimension"))
    checks.append((dimensions[-2] == EXPECTED_PRETERMINAL, "preterminal dimension"))
    live_entries = max(dimensions[index] + dimensions[index + 1]
                       for index in range(LENGTH - 1))
    checks.append((live_entries == EXPECTED_LIVE_ENTRIES, "maximum adjacent entries"))
    checks.append((16 * live_entries == EXPECTED_LIVE_BYTES, "maximum adjacent bytes"))
    child1 = sum(math.comb(11, q) * math.comb(23, q) for q in range(12))
    checks.append((child1 == EXPECTED_CHILD1_INPUT == math.comb(34, 11),
                   "terminal child-one admission support"))
    allocations = {}
    for q in range(9, 13):
        columns = math.comb(24, q)
        old = 97 * columns * 16
        new = replay.allocation_estimate(columns * 16)
        allocations[str(q)] = {
            "carrier_columns": columns,
            "v001_degree96_basis_bytes": old,
            "v003_one_row_certificate_bytes": new,
        }
        checks.append((old > WORKSPACE_LIMIT, f"V001 obstruction q{q}"))
        checks.append((new <= WORKSPACE_LIMIT, f"V003 allocation q{q}"))
        checks.append((replay.safe_batch_rows(columns, 96) >= 1, f"V003 batch q{q}"))
    checks.append((EXPECTED_LIVE_BYTES < SCRATCH_LIMIT, "logical scratch bound"))
    checks.append((EXPECTED_PRETERMINAL * 16 < SCRATCH_LIMIT,
                   "retained terminal scratch bound"))
    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V003_INVARIANTS",
        "classification": (
            "PASS_V003_SYNTAX_ALLOCATION_INDEX_INVARIANTS__L12_LOCKED"
            if not failures else "FAIL_V003_EXECUTABLE_METHOD_INVARIANTS"
        ),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "reverse_rank_checks": index_checks,
        "prefix_dimensions": dimensions,
        "allocation_certificates": allocations,
        "maximum_live_logical_scratch_bytes": EXPECTED_LIVE_BYTES,
        "retained_terminal_state_bytes": EXPECTED_PRETERMINAL * 16,
        "terminal_child0_entries": EXPECTED_PRETERMINAL,
        "terminal_child1_nonzero_admission_entries": EXPECTED_CHILD1_INPUT,
        "full_D12_array_allocated": False,
        "implementation_sha256": sha256(Path(__file__)),
        "method_sha256": sha256(METHOD),
        "claim_boundary": "METHOD_INVARIANTS_ONLY__NO_L12_HISTORY_SPECTRUM_Z1_OR_GRAVITY",
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("validate-invariants", "execute-l12"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workspace", type=Path)
    arguments = parser.parse_args()
    if arguments.mode == "validate-invariants":
        invariant_validation(arguments.output)
    else:
        if arguments.workspace is None:
            parser.error("--workspace is required for execute-l12")
        execute_l12(arguments.output, arguments.workspace)
