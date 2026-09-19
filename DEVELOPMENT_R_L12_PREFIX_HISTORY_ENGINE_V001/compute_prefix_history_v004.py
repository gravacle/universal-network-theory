#!/usr/bin/env python3
"""Exact q-sharded prefix-lineage history target for L=4,...,12."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import resource
import shutil
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import compute_prefix_history_v002 as v3  # noqa: E402


sealed = v3.sealed
SUPPORTED = (4, 6, 8, 10, 12)
IO_WINDOW_BYTES = 512 * 2**20
STATS_WINDOW_BYTES = 96 * 2**20
SCRATCH_LIMIT = 20 * 2**30
RSS_LIMIT = 16 * 2**30
WALL_LIMIT = 6 * 3600.0
TARGET_GATE = HERE / "TARGET_L12_GATE_V004.json"
METHOD = HERE / "Q_SHARDED_TARGET_METHOD_V004.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(16 * 2**20):
            digest.update(block)
    return digest.hexdigest()


def shard_path(root: Path, q: int) -> Path:
    return root / f"q_{q:02d}.npy"


def shape(length: int, prefix: int, q: int) -> tuple[int, int]:
    return math.comb(prefix, q), math.comb(2 * length, q)


def open_shard(root: Path, q: int, mode: str = "r") -> np.memmap:
    return np.load(shard_path(root, q), mmap_mode=mode)


def workspace_bytes(root: Path) -> int:
    if not root.exists():
        return 0
    return sum(path.stat().st_size for path in root.rglob("*.npy"))


def safe_remove_state(path: Path, workspace: Path) -> None:
    path = path.resolve()
    workspace = workspace.resolve()
    if path == workspace or workspace not in path.parents or not path.is_dir():
        raise RuntimeError(f"refuse unsafe scratch cleanup: {path}")
    for child in path.iterdir():
        if not child.is_file() or child.suffix != ".npy":
            raise RuntimeError(f"unexpected scratch member: {child}")
        child.unlink()
    path.rmdir()


def create_blank(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=False)
    block = np.lib.format.open_memmap(shard_path(root, 0), mode="w+",
                                      dtype=np.complex128, shape=(1, 1))
    block[0, 0] = 1.0
    block.flush()
    del block


def row_lookup(width: int, q: int) -> tuple[np.ndarray, dict[int, int]]:
    words = sealed.fixed_words(width, q)
    return words, {int(word): index for index, word in enumerate(words)}


def create_admitted(length: int, before: Path, prefix: int,
                    event: int, output: Path) -> None:
    if prefix != event:
        raise AssertionError("sequential prefix/event identity failed")
    output.mkdir(parents=True, exist_ok=False)
    cosine = math.cos(sealed.PHI)
    sine = math.sin(sealed.PHI)
    for q in range(prefix + 2):
        lineage_words, lineage_lookup = row_lookup(prefix + 1, q)
        carrier_words, carrier_lookup = row_lookup(2 * length, q)
        rows, columns = len(lineage_words), len(carrier_words)
        destination = np.lib.format.open_memmap(
            shard_path(output, q), mode="w+", dtype=np.complex128,
            shape=(rows, columns),
        )
        destination[:] = 0.0
        blank = ((carrier_words >> event) & 1) == 0
        if q <= prefix:
            source = open_shard(before, q)
            source_lineages = sealed.fixed_words(prefix, q)
            if source.shape != shape(length, prefix, q):
                raise AssertionError("stay-source shard shape mismatch")
            for source_row, word in enumerate(source_lineages):
                target_row = lineage_lookup[int(word)]
                row = np.array(source[source_row], copy=True)
                row[blank] *= cosine
                destination[target_row] = row
            del source, source_lineages
        if q and q - 1 <= prefix:
            source = open_shard(before, q - 1)
            source_lineages = sealed.fixed_words(prefix, q - 1)
            source_carriers = sealed.fixed_words(2 * length, q - 1)
            source_blank = np.flatnonzero(((source_carriers >> event) & 1) == 0)
            target_columns = np.fromiter(
                (carrier_lookup[int(source_carriers[column]) | (1 << event)]
                 for column in source_blank),
                dtype=np.int32, count=len(source_blank),
            )
            for source_row, word in enumerate(source_lineages):
                target_row = lineage_lookup[int(word) | (1 << event)]
                destination[target_row, target_columns] = (
                    -1.0j * sine * source[source_row, source_blank]
                )
            del source, source_lineages, source_carriers, source_blank, target_columns
        destination.flush()
        del destination, lineage_words, lineage_lookup, carrier_words, carrier_lookup, blank
        gc.collect()


def column_probabilities(block: np.ndarray) -> np.ndarray:
    columns = block.shape[1]
    rows = max(1, STATS_WINDOW_BYTES // max(16, columns * 16 * 3))
    result = np.zeros(columns, dtype=np.float64)
    for lower in range(0, block.shape[0], rows):
        upper = min(block.shape[0], lower + rows)
        view = np.asarray(block[lower:upper])
        result += np.sum(view.real * view.real + view.imag * view.imag, axis=0)
    return result


def statistics(length: int, root: Path, prefix: int,
               cursor: int | None = None) -> dict[str, object]:
    weights = np.zeros(length + 1)
    occupation = np.zeros(2 * length)
    allow = blocked = 0.0
    for q in range(prefix + 1):
        block = open_shard(root, q)
        if block.shape != shape(length, prefix, q):
            raise AssertionError("statistics shard shape mismatch")
        probability = column_probabilities(block)
        words = sealed.fixed_words(2 * length, q)
        weights[q] = float(np.sum(probability))
        for site in range(2 * length):
            occupation[site] += float(np.sum(probability[((words >> site) & 1) == 1]))
        if cursor is not None:
            if prefix != cursor:
                raise AssertionError("predicate cursor must be next prefix bit")
            occupied = ((words >> cursor) & 1) == 1
            blocked += float(np.sum(probability[occupied]))
            allow += float(np.sum(probability[~occupied]))
        del block, probability, words
    retained = float(np.dot(np.arange(length + 1), weights))
    return {
        "weights": weights,
        "occupation": occupation,
        "norm": float(np.sum(weights)),
        "retained": retained,
        "genesis": float(length - retained),
        "allow": allow,
        "blocked": blocked,
        "reverse": 0.0,
    }


def route_one(root: Path, q: int, sector, resolution,
              summary: dict[str, object]) -> np.ndarray:
    block = open_shard(root, q, mode="r+")
    rows = v3.batch_rows(block.shape[1], resolution, False)
    current = np.zeros(len(sector.pairs))
    for lower in range(0, block.shape[0], rows):
        upper = min(block.shape[0], lower + rows)
        window = np.array(block[lower:upper], copy=True)
        evolved, flux, record = v3.propagate_dispatch(
            sector.length, sector, window, resolution
        )
        block[lower:upper] = evolved
        current += flux
        v3.update_solver(summary, record)
    block.flush()
    del block
    return current


def route_pair(length: int, actual: Path, actual_prefix: int,
               null: Path, null_prefix: int, resolution):
    edges = sealed.graph(length)
    actual_current = np.zeros(len(edges))
    null_current = np.zeros(len(edges))
    actual_solver = v3.empty_solver(resolution)
    null_solver = v3.empty_solver(resolution)
    for q in range(actual_prefix + 1):
        sector = sealed.Sector(length, q, edges)
        actual_current += route_one(actual, q, sector, resolution, actual_solver)
        if q <= null_prefix:
            null_current += route_one(null, q, sector, resolution, null_solver)
        del sector
        gc.collect()
    return actual_current, actual_solver, null_current, null_solver


def block_statistics(words: np.ndarray, block: np.ndarray, sites: int):
    probability = column_probabilities(block)
    weight = float(np.sum(probability))
    occupation = np.zeros(sites)
    for site in range(sites):
        occupation[site] = float(np.sum(probability[((words >> site) & 1) == 1]))
    return weight, occupation


def route_ephemeral(length: int, sector, block: np.ndarray, resolution,
                    summary: dict[str, object]):
    evolved, current, record = v3.propagate_dispatch(length, sector, block, resolution)
    v3.update_solver(summary, record)
    return evolved, current


def terminal_stream(length: int, before: Path, prefix: int, event: int, resolution):
    if prefix != length - 1 or event != length - 1:
        raise AssertionError("terminal stream invoked outside final event")
    edges = sealed.graph(length)
    admitted_weights = np.zeros(length + 1)
    admitted_occupation = np.zeros(2 * length)
    after_weights = np.zeros(length + 1)
    after_occupation = np.zeros(2 * length)
    null_weights = np.zeros(length + 1)
    actual_current = np.zeros(len(edges))
    null_current = np.zeros(len(edges))
    actual_solver = v3.empty_solver(resolution)
    null_solver = v3.empty_solver(resolution)
    cosine = math.cos(sealed.PHI)
    sine = math.sin(sealed.PHI)
    blocked_error = 0.0
    for q in range(prefix + 1):
        old = open_shard(before, q)
        carrier_words = sealed.fixed_words(2 * length, q)
        blank_columns = np.flatnonzero(((carrier_words >> event) & 1) == 0)
        occupied_columns = np.flatnonzero(((carrier_words >> event) & 1) == 1)
        sector = sealed.Sector(length, q, edges)
        rows = v3.batch_rows(len(carrier_words), resolution, False)
        for lower in range(0, old.shape[0], rows):
            upper = min(old.shape[0], lower + rows)
            source = np.array(old[lower:upper], copy=True)
            child = source.copy()
            child[:, blank_columns] *= cosine
            if len(occupied_columns):
                blocked_error = max(
                    blocked_error,
                    float(np.max(np.abs(child[:, occupied_columns]
                                        - source[:, occupied_columns]))),
                )
            weight, occupation = block_statistics(carrier_words, child, 2 * length)
            admitted_weights[q] += weight
            admitted_occupation += occupation
            evolved, flux = route_ephemeral(length, sector, child, resolution,
                                             actual_solver)
            weight, occupation = block_statistics(carrier_words, evolved, 2 * length)
            after_weights[q] += weight
            after_occupation += occupation
            actual_current += flux
            null_evolved, flux = route_ephemeral(length, sector, source, resolution,
                                                 null_solver)
            null_weights[q] += block_statistics(carrier_words, null_evolved,
                                                 2 * length)[0]
            null_current += flux
        del sector
        gc.collect()
        if len(blank_columns):
            destination = sealed.Sector(length, q + 1, edges)
            destination_columns = np.fromiter(
                (destination.lookup[int(carrier_words[column]) | (1 << event)]
                 for column in blank_columns),
                dtype=np.int32, count=len(blank_columns),
            )
            rows = v3.batch_rows(len(destination.words), resolution, False)
            for lower in range(0, old.shape[0], rows):
                upper = min(old.shape[0], lower + rows)
                child = np.zeros((upper - lower, len(destination.words)),
                                 dtype=np.complex128)
                child[:, destination_columns] = (
                    -1.0j * sine * old[lower:upper, blank_columns]
                )
                weight, occupation = block_statistics(destination.words, child,
                                                       2 * length)
                admitted_weights[q + 1] += weight
                admitted_occupation += occupation
                evolved, flux = route_ephemeral(length, destination, child, resolution,
                                                 actual_solver)
                weight, occupation = block_statistics(destination.words, evolved,
                                                       2 * length)
                after_weights[q + 1] += weight
                after_occupation += occupation
                actual_current += flux
            del destination, destination_columns
            gc.collect()
        del old, carrier_words, blank_columns, occupied_columns
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


def make_row(length: int, event: int, before_stats: dict[str, object],
             admitted_weights: np.ndarray, admitted_occupation: np.ndarray,
             after_weights: np.ndarray, after_occupation: np.ndarray,
             actual_current: np.ndarray, null_current: np.ndarray,
             actual_solver: dict[str, object], null_solver: dict[str, object],
             incidence: np.ndarray, connector_indices: list[int],
             blocked_error: float, terminal: bool) -> dict[str, object]:
    q_before = float(before_stats["retained"])
    q_admitted = float(np.dot(np.arange(length + 1), admitted_weights))
    q_after = float(np.dot(np.arange(length + 1), after_weights))
    g_before = float(before_stats["genesis"])
    g_admitted = float(length - q_admitted)
    write = q_admitted - q_before
    delta = actual_current - null_current
    residual = after_occupation - admitted_occupation + incidence @ actual_current
    return {
        "event": event + 1,
        "cursor_vertex": event,
        "allow_probability": float(before_stats["allow"]),
        "blocked_probability": float(before_stats["blocked"]),
        "reverse_support_probability": float(before_stats["reverse"]),
        "blocked_null_state_error": blocked_error,
        "W_n": write,
        "expected_W_from_allow": (math.sin(sealed.PHI) ** 2)
            * float(before_stats["allow"]),
        "q_retained_before": q_before,
        "q_retained_after_admission": q_admitted,
        "q_retained_after_transport": q_after,
        "q_genesis_before": g_before,
        "q_genesis_after": g_admitted,
        "bandwidth_after": g_admitted,
        "lineage_sealed_after": length - g_admitted,
        "sector_weights": admitted_weights.tolist(),
        "connector_delta_l1": float(np.sum(np.abs(delta[connector_indices]))),
        "connector_delta_signed": float(np.sum(delta[connector_indices])),
        "admission_total_content_residual": (q_admitted - q_before)
            + (g_admitted - g_before),
        "admission_bandwidth_residual": (g_admitted - g_before) + write,
        "target_owner_residual": (admitted_occupation[event]
            - before_stats["occupation"][event]) - write,
        "transport_node_residual_l1": float(np.sum(np.abs(residual))),
        "transport_node_residual_linf": float(np.max(np.abs(residual))),
        "transport_number_drift": abs(q_after - q_admitted),
        "transport_genesis_drift": 0.0,
        "actual_norm_error": abs(float(np.sum(after_weights)) - 1.0),
        "null_norm_error": abs(float(before_stats["norm"]) - 1.0),
        "actual_solver": actual_solver,
        "null_solver": null_solver,
        "terminal_children_streamed": terminal,
    }


def history(length: int, resolution, root: Path, retain_terminal: bool):
    edges = sealed.graph(length)
    connector_indices = [index for index, edge in enumerate(edges)
                         if edge[2] == "connector"]
    incidence = np.zeros((2 * length, len(edges)), dtype=np.int8)
    for edge_index, (u, v, _) in enumerate(edges):
        incidence[u, edge_index] = 1
        incidence[v, edge_index] = -1
    root.mkdir(parents=True, exist_ok=False)
    state = root / "prefix_00"
    create_blank(state)
    prefix = 0
    peak_scratch = workspace_bytes(root)
    rows = []
    for event in range(length):
        before = state
        before_stats = statistics(length, before, prefix, cursor=event)
        if event < length - 1:
            admitted = root / f"prefix_{event + 1:02d}"
            create_admitted(length, before, prefix, event, admitted)
            peak_scratch = max(peak_scratch, workspace_bytes(root))
            if peak_scratch > SCRATCH_LIMIT:
                raise MemoryError("logical scratch cap exceeded")
            admitted_stats = statistics(length, admitted, prefix + 1)
            actual_current, actual_solver, null_current, null_solver = route_pair(
                length, admitted, prefix + 1, before, prefix, resolution
            )
            after_stats = statistics(length, admitted, prefix + 1)
            row = make_row(
                length, event, before_stats,
                admitted_stats["weights"], admitted_stats["occupation"],
                after_stats["weights"], after_stats["occupation"],
                actual_current, null_current, actual_solver, null_solver,
                incidence, connector_indices, 0.0, False,
            )
            safe_remove_state(before, root)
            state = admitted
            prefix += 1
        else:
            terminal = terminal_stream(length, before, prefix, event, resolution)
            row = make_row(
                length, event, before_stats,
                terminal["admitted_weights"], terminal["admitted_occupation"],
                terminal["after_weights"], terminal["after_occupation"],
                terminal["actual_current"], terminal["null_current"],
                terminal["actual_solver"], terminal["null_solver"],
                incidence, connector_indices, terminal["blocked_error"], True,
            )
        rows.append(row)
    terminal_shards = []
    if retain_terminal:
        for q in range(prefix + 1):
            path = shard_path(state, q)
            terminal_shards.append({
                "q": q,
                "path": str(path),
                "shape": list(shape(length, prefix, q)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
    return {
        "rows": rows,
        "dimension": math.comb(3 * length, length),
        "preterminal_dimension": math.comb(3 * length - 1, length - 1),
        "edges": len(edges),
        "peak_logical_scratch_bytes": peak_scratch,
        "terminal_state_retained": retain_terminal,
        "terminal_shards": terminal_shards,
    }


def remove_resolution(root: Path, workspace: Path) -> None:
    if not root.exists():
        return
    for state in sorted((path for path in root.iterdir() if path.is_dir()), reverse=True):
        safe_remove_state(state, root)
    if any(root.iterdir()):
        raise RuntimeError("unexpected resolution scratch member")
    if root.resolve() == workspace.resolve() or workspace.resolve() not in root.resolve().parents:
        raise RuntimeError("unsafe resolution cleanup")
    root.rmdir()


def require_target_gate() -> None:
    if not TARGET_GATE.exists():
        raise RuntimeError("L12 locked: target V004 gate absent")
    gate = json.loads(TARGET_GATE.read_text())
    if gate.get("classification") != "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004":
        raise RuntimeError("L12 locked: target V004 gate did not pass")
    if gate.get("implementation_sha256") != sha256(Path(__file__)):
        raise RuntimeError("L12 locked: target V004 gate does not pin implementation")
    if shutil.disk_usage(HERE).free < SCRATCH_LIMIT:
        raise RuntimeError("L12 locked: less than 20 GiB scratch is free")


def execute(length: int, output: Path, workspace: Path) -> None:
    if length not in SUPPORTED:
        raise ValueError(f"supported sizes: {SUPPORTED}")
    if length == 12:
        require_target_gate()
    if output.exists() or workspace.exists():
        raise FileExistsError("refuse to overwrite output or workspace")
    started = time.perf_counter()
    rough_root = workspace / "rough"
    sharp_root = workspace / "sharp"
    workspace.mkdir(parents=True, exist_ok=False)
    rough = history(length, sealed.COARSE, rough_root, retain_terminal=False)
    remove_resolution(rough_root, workspace)
    sharp = history(length, sealed.FINE, sharp_root, retain_terminal=True)
    comparison = sealed.summarize(length, rough, sharp)
    wall = time.perf_counter() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    peak_scratch = max(int(rough["peak_logical_scratch_bytes"]),
                       int(sharp["peak_logical_scratch_bytes"]))
    maximum_workset = max(
        int(row[key]["maximum_live_bytes"])
        for row in sharp["rows"] for key in ("actual_solver", "null_solver")
    )
    resource_pass = (
        peak_scratch <= SCRATCH_LIMIT
        and maximum_workset <= v3.CAP_BYTES
        and rss <= RSS_LIMIT
        and (length < 12 or wall <= WALL_LIMIT)
    )
    if not resource_pass:
        comparison["resolved"] = False
        comparison["classification"] = "TARGET_Q_SHARDED_RESOURCE_OBSTRUCTION"
    result = {
        "schema": "TARGET_Q_SHARDED_PREFIX_HISTORY_V004",
        "L": length,
        "events": length,
        "dimension": sharp["dimension"],
        "preterminal_dimension": sharp["preterminal_dimension"],
        "edges": sharp["edges"],
        "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS",
        "lineage_authority": "FULL_CANONICAL_MASK__SHA256_CUSTODY_ONLY",
        "coarse_method": sealed.COARSE.__dict__,
        "fine_method": sealed.FINE.__dict__,
        "rows": sharp["rows"],
        "comparison": comparison,
        "terminal_shards": sharp["terminal_shards"],
        "resource": {
            "peak_logical_scratch_bytes": peak_scratch,
            "scratch_limit_bytes": SCRATCH_LIMIT,
            "maximum_numerical_workset_bytes": maximum_workset,
            "numerical_workset_limit_bytes": v3.CAP_BYTES,
            "peak_rss_bytes": rss,
            "rss_limit_bytes": RSS_LIMIT,
            "wall_seconds": wall,
            "wall_limit_seconds": WALL_LIMIT,
            "passed": resource_pass,
        },
        "implementation_sha256": sha256(Path(__file__)),
        "method_sha256": sha256(METHOD),
        "claim_boundary": "FINITE_Q_SHARDED_PREFIX_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(comparison["classification"])
    print(f"L={length} scratch={peak_scratch} workset={maximum_workset} rss={rss} wall={wall:.3f}")
    if not comparison["resolved"]:
        raise SystemExit(2)


def invariants(output: Path) -> None:
    checks: list[tuple[bool, str]] = []
    for length in SUPPORTED:
        for prefix in range(length):
            total = sum(math.prod(shape(length, prefix, q)) for q in range(prefix + 1))
            checks.append((total == math.comb(2 * length + prefix, prefix),
                           f"Vandermonde L{length} n{prefix}"))
    checks.extend((
        (math.comb(36, 12) == 1_251_677_700, "D12"),
        (math.comb(35, 11) == 417_225_900, "H11"),
        ((math.comb(34, 10) + math.comb(35, 11)) * 16 == 8_773_664_640,
         "H10 plus H11 bytes"),
        (math.comb(35, 11) * 16 == 6_675_614_400, "retained H11 bytes"),
        (v3.CAP_BYTES == 1_000_000_000, "target numerical cap"),
        (SCRATCH_LIMIT == 20 * 2**30, "scratch cap"),
    ))
    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "TARGET_Q_SHARDED_PREFIX_HISTORY_INVARIANTS_V004",
        "classification": "PASS" if not failures else "FAIL",
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "implementation_sha256": sha256(Path(__file__)),
        "method_sha256": sha256(METHOD),
        "claim_boundary": "INDEX_AND_RESOURCE_ARITHMETIC_ONLY__NO_PHYSICAL_HISTORY",
    }
    if output.exists():
        raise FileExistsError(f"refuse overwrite: {output}")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"], result["checks_passed"], result["checks_total"])
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("invariants", "execute"))
    parser.add_argument("--worker", type=int)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workspace", type=Path)
    arguments = parser.parse_args()
    if arguments.mode == "invariants":
        invariants(arguments.output)
    else:
        if arguments.worker is None or arguments.workspace is None:
            parser.error("execute requires --worker and --workspace")
        execute(arguments.worker, arguments.output, arguments.workspace)
