#!/usr/bin/env python3
"""Gate-locked hostile V004 consumer for storage-only cached indices."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import mmap
import os
import resource
import shutil
import sys
import time
from pathlib import Path

import numpy as np

import independent_prefix_history as physical
import independent_prefix_history_v002 as replay
import independent_prefix_history_v003 as v3


HERE = Path(__file__).resolve().parent
FREEZE = HERE / "FROZEN_MANIFEST_V004.json"
METHOD = HERE / "V004_STORAGE_ONLY_CACHE_METHOD.md"
INITIAL_PHYSICAL_GATE = HERE / "PHYSICAL_CONTROL_EXECUTION_GATE_V004.json"
CONTROL_GATE = HERE / "CONTROL_GATE_V004.json"
L10_GATE = HERE / "L10_GATE_V004.json"
SUPPORTED = (4, 6, 8, 10, 12)
SCRATCH_LIMIT = 20 * 2**30
RSS_LIMIT = 16 * 2**30
WALL_LIMIT = 6 * 3600.0
WORD_DTYPE = np.dtype("<u4")
OFFSET_DTYPE = np.dtype("<u8")
INDEX_DTYPE = np.dtype("<i4")


class Refusal(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def close_mapping(array: np.memmap) -> None:
    mapping = getattr(array, "_mmap", None)
    if mapping is not None:
        try:
            mapping.madvise(mmap.MADV_DONTNEED)
        except (AttributeError, OSError):
            pass
        try:
            mapping.close()
        except (BufferError, OSError):
            pass


class CachedCarrier:
    def __init__(self, length: int, q: int, edges: list[tuple[int, int, str]],
                 words: np.memmap, offsets: np.memmap,
                 sources: np.memmap, targets: np.memmap):
        self.length = length
        self.q = q
        self.words = words
        self.offsets = offsets
        self.sources = sources
        self.targets = targets
        self.exchanges = [
            (
                self.sources[int(self.offsets[index]):int(self.offsets[index + 1])],
                self.targets[int(self.offsets[index]):int(self.offsets[index + 1])],
            )
            for index in range(len(edges))
        ]

    def multiply(self, vector: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(vector)
        for source, target in self.exchanges:
            answer[:, source] -= vector[:, target]
            answer[:, target] -= vector[:, source]
        return answer

    def currents(self, vector: np.ndarray) -> np.ndarray:
        answer = np.zeros(len(self.exchanges))
        for edge, (source, target) in enumerate(self.exchanges):
            answer[edge] = 2.0 * float(np.imag(np.vdot(vector[:, source], vector[:, target])))
        return answer

    def release(self) -> None:
        self.exchanges.clear()
        for array in (self.words, self.offsets, self.sources, self.targets):
            close_mapping(array)

    def __del__(self) -> None:
        try:
            self.release()
        except Exception:
            pass


class CacheContext:
    def __init__(self, root: Path, length: int, pinned_hash: str):
        self.root = root.resolve()
        self.manifest_path = self.root / "CACHE_MANIFEST.json"
        if not self.manifest_path.is_file() or sha256(self.manifest_path) != pinned_hash:
            raise Refusal("cache manifest hash custody failed")
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        if (
            manifest.get("schema") != "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004"
            or manifest.get("status") != "COMPLETE_HASH_PINNED_STORAGE_ONLY_CACHE"
            or manifest.get("L") != length
            or manifest.get("basis_order") != "REVERSED_COMBINATION__FULL_MASK"
            or manifest.get("hamiltonian_exchange_coefficient") != -1
        ):
            raise Refusal("cache manifest identity failed")
        expected_edges = [list(edge) for edge in physical.hostile_edges(length)]
        if manifest.get("edge_layout") != expected_edges:
            raise Refusal("cache hostile edge order mismatch")
        frozen = json.loads(FREEZE.read_text(encoding="utf-8"))
        for field, actual in (
            ("builder_sha256", sha256(HERE / "build_hostile_v004_cache.py")),
            ("consumer_sha256", sha256(Path(__file__))),
            ("method_sha256", sha256(METHOD)),
            ("freeze_sha256", sha256(FREEZE)),
        ):
            if manifest.get(field) != actual:
                raise Refusal(f"cache does not bind frozen {field}")
        records = manifest.get("files")
        if not isinstance(records, list):
            raise Refusal("cache file census absent")
        self.records: dict[str, dict[str, object]] = {}
        actual_bytes = 0
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("path"), str):
                raise Refusal("invalid cache file record")
            relative = Path(record["path"])
            if relative.is_absolute() or len(relative.parts) != 1 or relative.name in self.records:
                raise Refusal("unsafe or duplicate cache member")
            path = self.root / relative
            if (
                not path.is_file()
                or path.stat().st_size != record.get("bytes")
                or sha256(path) != record.get("sha256")
            ):
                raise Refusal(f"cache member custody failed: {relative}")
            self.records[relative.name] = record
            actual_bytes += path.stat().st_size
        if manifest.get("payload", {}).get("actual_files_bytes_including_offsets") != actual_bytes:
            raise Refusal("cache byte census mismatch")
        self.manifest = manifest
        self.length = length
        self.edges = physical.hostile_edges(length)

    def _open(self, name: str, dtype: np.dtype) -> np.memmap:
        record = self.records.get(name)
        if record is None or record.get("dtype") != dtype.str:
            raise Refusal(f"cache array type record absent: {name}")
        shape = tuple(record.get("shape", ()))
        if not shape or any(isinstance(item, bool) or not isinstance(item, int) or item < 0 for item in shape):
            raise Refusal(f"cache array shape invalid: {name}")
        if math.prod(shape) * dtype.itemsize != record.get("bytes"):
            raise Refusal(f"cache array shape/byte mismatch: {name}")
        return np.memmap(self.root / name, dtype=dtype, mode="r", shape=shape)

    def carrier(self, q: int, edges: list[tuple[int, int, str]]) -> CachedCarrier:
        if edges != self.edges or not 0 <= q <= self.length:
            raise Refusal("cached carrier request changed graph or charge")
        prefix = f"q_{q:02d}"
        words = self._open(f"{prefix}_words.u32", WORD_DTYPE)
        offsets = self._open(f"{prefix}_offsets.u64", OFFSET_DTYPE)
        sources = self._open(f"{prefix}_sources.i32", INDEX_DTYPE)
        targets = self._open(f"{prefix}_targets.i32", INDEX_DTYPE)
        if words.shape != (math.comb(2 * self.length, q),) or offsets.shape != (3 * self.length + 1,):
            raise Refusal("cached carrier exact shape mismatch")
        if int(offsets[0]) != 0 or int(offsets[-1]) != len(sources) or len(sources) != len(targets):
            raise Refusal("cached carrier offsets mismatch")
        return CachedCarrier(self.length, q, edges, words, offsets, sources, targets)

    def admission(self, event: int, q: int) -> tuple[np.memmap, np.memmap]:
        return (
            self._open(f"event_{event:02d}_q_{q:02d}_occupied.i32", INDEX_DTYPE),
            self._open(f"event_{event:02d}_q_{q:02d}_old.i32", INDEX_DTYPE),
        )

    def lineage(self, event: int, q: int, added: bool) -> np.memmap:
        label = "added" if added else "same"
        return self._open(f"prefix_{event:02d}_q_{q:02d}_{label}.i32", INDEX_DTYPE)


CACHE: CacheContext | None = None


def cached_construct_carrier(q: int, edges: list[tuple[int, int, str]]) -> CachedCarrier:
    if CACHE is None:
        raise Refusal("cache context is not authenticated")
    carrier = CACHE.carrier(q, edges)
    bytes_used = sum(source.nbytes + target.nbytes for source, target in carrier.exchanges)
    bytes_used += carrier.words.nbytes + carrier.offsets.nbytes
    if bytes_used > 2 * 2**30:
        raise MemoryError("one-q cached carrier arrays exceed frozen 2-GiB certificate")
    v3.guard_rss()
    return carrier


def cached_lineage_row_map(old_prefix: int, q: int, event: int, add_event: bool) -> np.ndarray:
    if CACHE is None or old_prefix != event:
        raise Refusal("cached lineage map request outside sequential prefix")
    return CACHE.lineage(event, q, add_event)


def cached_admit_to_next(state: v3.DiskPrefix, event: int,
                         edges: list[tuple[int, int, str]]) -> tuple[v3.DiskPrefix, float]:
    if CACHE is None or state.prefix != event or event >= CACHE.length - 1:
        raise AssertionError("nonterminal cached admission prefix mismatch")
    output = v3.DiskPrefix(state.root, event + 1)
    output.create()
    cosine = math.cos(physical.ANGLE)
    sine = math.sin(physical.ANGLE)
    blocked_error = 0.0
    for out_q in range(event + 2):
        carrier = cached_construct_carrier(out_q, edges)
        target = output.create_shard(out_q)
        if out_q <= event:
            source = state.open_shard(out_q)
            target_rows = CACHE.lineage(event, out_q, False)
            blank = ((carrier.words >> event) & 1) == 0
            factors = np.where(blank, cosine, 1.0)
            step = v3.io_rows(len(carrier.words))
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
            v3.close_memmap(source)
            close_mapping(target_rows)
        if out_q >= 1:
            source = state.open_shard(out_q - 1)
            target_rows = CACHE.lineage(event, out_q - 1, True)
            occupied_columns, old_columns = CACHE.admission(event, out_q)
            step = v3.io_rows(max(1, len(old_columns)))
            for lower in range(0, len(source), step):
                upper = min(len(source), lower + step)
                data = -1.0j * sine * np.asarray(source[lower:upper, old_columns])
                target[np.ix_(target_rows[lower:upper], occupied_columns)] = data
            v3.close_memmap(source)
            for mapping in (target_rows, occupied_columns, old_columns):
                close_mapping(mapping)
        v3.close_memmap(target, write=True)
        carrier.release()
        del carrier
        gc.collect()
    output.verify_complete()
    return output, blocked_error


def cached_terminal_route(state: v3.DiskPrefix, accuracy: physical.Accuracy,
                          edges: list[tuple[int, int, str]]):
    if CACHE is None or state.prefix != CACHE.length - 1:
        raise AssertionError("cached terminal route prefix mismatch")
    length = CACHE.length
    event = length - 1
    cosine = math.cos(physical.ANGLE)
    sine = math.sin(physical.ANGLE)
    admitted = v3.empty_statistics()
    actual_final = v3.empty_statistics()
    actual_flux = np.zeros(len(edges))
    actual_method = v3.method_record()
    blocked_error = 0.0
    for q in range(length):
        carrier = cached_construct_carrier(q, edges)
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
                blocked_error = max(blocked_error, float(np.max(np.abs(
                    child[:, occupied_columns] - source[lower:upper, occupied_columns]
                ))))
            v3.add_statistics(admitted, carrier, q, child)
            final, flux, record = replay.low_memory_evolve_batch(carrier, child, accuracy)
            v3.guard_rss()
            v3.add_statistics(actual_final, carrier, q, final)
            actual_flux += flux
            v3.update_method(actual_method, record)
        v3.close_memmap(source)
        carrier.release()
        del carrier
        gc.collect()
    for q in range(1, length + 1):
        carrier = cached_construct_carrier(q, edges)
        source = state.open_shard(q - 1)
        occupied_columns, old_columns = CACHE.admission(event, q)
        step = min(len(source), replay.safe_batch_rows(
            len(carrier.words), max(accuracy.checkpoints), physical.TERMINAL_WINDOW_BYTES
        ))
        for lower in range(0, len(source), step):
            upper = min(len(source), lower + step)
            child = np.zeros((upper - lower, len(carrier.words)), dtype=np.complex128)
            child[:, occupied_columns] = -1.0j * sine * np.asarray(
                source[lower:upper, old_columns]
            )
            v3.add_statistics(admitted, carrier, q, child)
            final, flux, record = replay.low_memory_evolve_batch(carrier, child, accuracy)
            v3.guard_rss()
            v3.add_statistics(actual_final, carrier, q, final)
            actual_flux += flux
            v3.update_method(actual_method, record)
        v3.close_memmap(source)
        close_mapping(occupied_columns)
        close_mapping(old_columns)
        carrier.release()
        del carrier
        gc.collect()
    before, null_final, null_flux, null_method, allowed, blocked = v3.route_disk_state(
        state, accuracy, edges, False, classify_event=event
    )
    actual_method["quadrature_nodes"] = accuracy.gauss_order
    actual_method["q_sharded"] = True
    actual_method["terminal_children_streamed"] = True
    actual_method["terminal_child0_entries"] = v3.EXPECTED_PRETERMINAL
    actual_method["terminal_child1_nonzero_admission_entries"] = v3.EXPECTED_CHILD1_INPUT
    actual_method["full_terminal_array_allocated"] = False
    return (before, admitted, actual_final, null_final, actual_flux, null_flux,
            actual_method, null_method, allowed, blocked, blocked_error)


def require_record(path: Path, classification: str) -> dict[str, object]:
    if not path.is_file():
        raise Refusal(f"physical execution locked: {path.name} absent")
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("classification") != classification:
        raise Refusal(f"physical execution locked: {path.name} classification")
    if record.get("consumer_sha256") != sha256(Path(__file__)):
        raise Refusal(f"physical execution locked: {path.name} consumer hash")
    if record.get("freeze_sha256") != sha256(FREEZE):
        raise Refusal(f"physical execution locked: {path.name} freeze hash")
    return record


def require_execution_gate(length: int, cache_root: Path) -> str:
    initial = require_record(
        INITIAL_PHYSICAL_GATE,
        "AUTHORIZE_HOSTILE_V004_CACHED_PHYSICAL_CONTROLS_AFTER_DUAL_6H_OBSTRUCTION",
    )
    manifest_path = cache_root / "CACHE_MANIFEST.json"
    cache_hash = sha256(manifest_path) if manifest_path.is_file() else ""
    for field, actual in (
        ("consumer_sha256", sha256(Path(__file__))),
        ("freeze_sha256", sha256(FREEZE)),
    ):
        if initial.get(field) != actual:
            raise Refusal(f"physical execution gate does not pin {field}")
    cache_manifests = initial.get("cache_manifest_sha256_by_L")
    if not isinstance(cache_manifests, dict) or cache_manifests.get(str(length)) != cache_hash:
        raise Refusal("physical execution gate does not pin this size's cache manifest")
    if length == 10:
        require_record(CONTROL_GATE, "PASS_HOSTILE_V004_CACHED_CONTROLS_L4_L8")
    elif length == 12:
        require_record(CONTROL_GATE, "PASS_HOSTILE_V004_CACHED_CONTROLS_L4_L8")
        require_record(L10_GATE, "PASS_HOSTILE_V004_CACHED_L10_GATE")
        if shutil.disk_usage(cache_root).free < SCRATCH_LIMIT:
            raise Refusal("L12 cached scratch gate failed")
    return cache_hash


def configure(length: int, cache: CacheContext, started: float) -> None:
    global CACHE
    CACHE = cache
    v3.LENGTH = length
    v3.EXPECTED_FULL = math.comb(3 * length, length)
    v3.EXPECTED_PRETERMINAL = math.comb(3 * length - 1, length - 1)
    v3.EXPECTED_CHILD1_INPUT = math.comb(3 * length - 2, length - 1)
    v3.EXPECTED_LIVE_ENTRIES = max(
        v3.prefix_dimension(index) + v3.prefix_dimension(index + 1)
        for index in range(length - 1)
    ) if length > 1 else 1
    v3.EXPECTED_LIVE_BYTES = 16 * v3.EXPECTED_LIVE_ENTRIES
    v3.EXECUTION_STARTED = started
    v3.construct_carrier = cached_construct_carrier
    v3.lineage_row_map = cached_lineage_row_map
    v3.admit_to_next = cached_admit_to_next
    v3.terminal_route = cached_terminal_route


def execute(length: int, output: Path, workspace: Path, cache_root: Path) -> None:
    if length not in SUPPORTED:
        raise Refusal("unsupported cached history size")
    if output.exists() or workspace.exists():
        raise Refusal("refuse to overwrite cached history output/workspace")
    cache_hash = require_execution_gate(length, cache_root)
    cache = CacheContext(cache_root, length, cache_hash)
    started = time.perf_counter()
    configure(length, cache, started)
    rough_root = workspace / "rough"
    sharp_root = workspace / "sharp"
    rough = v3.history(length, physical.ROUGH, rough_root, retain_terminal=False)
    v3.remove_resolution(rough_root)
    sharp = v3.history(length, physical.SHARP, sharp_root, retain_terminal=True)
    comparison = physical.compare(length, rough, sharp)
    wall = time.perf_counter() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    peak_scratch = max(
        int(rough["peak_logical_scratch_bytes"]),
        int(sharp["peak_logical_scratch_bytes"]),
    ) + int(cache.manifest["payload"]["actual_files_bytes_including_offsets"])
    maximum_allocation = max(
        int(row[key]["maximum_allocation_estimate_bytes"])
        for row in sharp["rows"] for key in ("actual_solver", "null_solver")
    )
    passed = (
        comparison.get("resolved") is True
        and peak_scratch <= SCRATCH_LIMIT
        and maximum_allocation <= v3.WORKSPACE_LIMIT
        and rss <= RSS_LIMIT
        and wall <= WALL_LIMIT
    )
    result = {
        "schema": "INDEPENDENT_STORAGE_CACHED_PREFIX_HISTORY_V004",
        "L": length,
        "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS__STORAGE_INDEX_CACHE",
        "rows": sharp["rows"],
        "comparison": comparison,
        "terminal_shards": sharp["terminal_shards"],
        "cache_manifest_path": str((cache_root / "CACHE_MANIFEST.json").resolve()),
        "cache_manifest_sha256": cache_hash,
        "resource": {
            "peak_logical_state_plus_cache_bytes": peak_scratch,
            "scratch_limit_bytes": SCRATCH_LIMIT,
            "maximum_numerical_allocation_estimate_bytes": maximum_allocation,
            "peak_rss_bytes": rss,
            "rss_limit_bytes": RSS_LIMIT,
            "wall_seconds": wall,
            "wall_limit_seconds": WALL_LIMIT,
            "passed": passed,
        },
        "implementation_sha256": sha256(Path(__file__)),
        "method_sha256": sha256(METHOD),
        "freeze_sha256": sha256(FREEZE),
        "claim_boundary": "INDEPENDENT_FINITE_CACHED_PREFIX_HISTORY_ONLY",
    }
    if not passed:
        result["comparison"]["resolved"] = False
        result["comparison"]["classification"] = "CACHED_PREFIX_HISTORY_RESOURCE_OR_NUMERICAL_OBSTRUCTION"
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("execute", choices=("execute",))
    parser.add_argument("--length", type=int, choices=SUPPORTED, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        execute(args.length, args.output, args.workspace, args.cache_root)
    except (AssertionError, MemoryError, OSError, Refusal, TimeoutError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
