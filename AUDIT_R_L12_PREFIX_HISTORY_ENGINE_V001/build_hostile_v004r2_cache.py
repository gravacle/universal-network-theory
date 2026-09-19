#!/usr/bin/env python3
"""Gate-locked, canonical-path builder for the hostile V004R2 index cache."""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import stat
import sys
from pathlib import Path

import numpy as np

import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import v004r2_common as common


WORD = np.dtype("<u4")
OFFSET = np.dtype("<u8")
INDEX = np.dtype("<i4")


def reverse_words(width: int, q: int) -> np.ndarray:
    return np.asarray(physical.reverse_masks(width, q), dtype=WORD)


def operator_arrays(length: int, q: int, edges: list[tuple[int, int, str]]) -> tuple[np.ndarray, ...]:
    words = reverse_words(2 * length, q)
    if len(words) != math.comb(2 * length, q) or len(set(map(int, words))) != len(words):
        raise AssertionError("carrier word census/uniqueness")
    if any(bin(int(word)).count("1") != q for word in words):
        raise AssertionError("carrier Hamming census")
    lookup = {int(word): index for index, word in enumerate(words)}
    offsets = [0]
    source_parts: list[np.ndarray] = []
    target_parts: list[np.ndarray] = []
    for u, v, _label in edges:
        source = np.flatnonzero((((words >> u) & 1) == 1) & (((words >> v) & 1) == 0)).astype(INDEX)
        expected = math.comb(2 * length - 2, q - 1) if q else 0
        if len(source) != expected:
            raise AssertionError("edge source census")
        toggle = (1 << u) | (1 << v)
        target = np.fromiter((lookup[int(words[int(row)]) ^ toggle] for row in source),
                             dtype=INDEX, count=len(source))
        if any(int(words[int(t)]) != (int(words[int(s)]) ^ toggle) for s, t in zip(source, target)):
            raise AssertionError("edge XOR/rank identity")
        source_parts.append(source)
        target_parts.append(target)
        offsets.append(offsets[-1] + expected)
    return (words, np.asarray(offsets, dtype=OFFSET),
            np.concatenate(source_parts) if source_parts else np.empty(0, dtype=INDEX),
            np.concatenate(target_parts) if target_parts else np.empty(0, dtype=INDEX))


def admission_arrays(length: int, event: int, q: int, words: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    occupied = np.flatnonzero(((words >> event) & 1) == 1).astype(INDEX)
    expected = math.comb(2 * length - 1, q - 1)
    if len(occupied) != expected:
        raise AssertionError("admission occupied census")
    old = np.fromiter((v3.reverse_rank(2 * length, q - 1,
                                      int(words[int(column)]) & ~(1 << event))
                       for column in occupied), dtype=INDEX, count=expected)
    old_words = reverse_words(2 * length, q - 1)
    if any((int(old_words[int(o)]) | (1 << event)) != int(words[int(n)])
           for o, n in zip(old, occupied)):
        raise AssertionError("admission add-event identity")
    return occupied, old


def lineage_arrays(event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
    old_words = physical.reverse_masks(event, q)
    same = np.fromiter((v3.reverse_rank(event + 1, q, int(word)) for word in old_words),
                       dtype=INDEX, count=len(old_words))
    added = np.fromiter((v3.reverse_rank(event + 1, q + 1, int(word) | (1 << event))
                         for word in old_words), dtype=INDEX, count=len(old_words))
    same_words = physical.reverse_masks(event + 1, q)
    added_words = physical.reverse_masks(event + 1, q + 1)
    if any(int(same_words[int(row)]) != int(word) for row, word in zip(same, old_words)):
        raise AssertionError("lineage stay identity")
    if any(int(added_words[int(row)]) != (int(word) | (1 << event))
           for row, word in zip(added, old_words)):
        raise AssertionError("lineage write identity")
    return same, added


def raw_write(root_fd: int, spec: dict[str, object], array: np.ndarray) -> dict[str, object]:
    normalized = np.ascontiguousarray(array)
    if normalized.dtype.str != spec["dtype"] or list(normalized.shape) != spec["shape"] or normalized.nbytes != spec["bytes"]:
        raise AssertionError(f"array disagrees with frozen specification: {spec['path']}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(str(spec["path"]), flags, 0o444, dir_fd=root_fd)
    try:
        data = memoryview(normalized).cast("B")
        cursor = 0
        while cursor < len(data):
            cursor += os.write(fd, data[cursor:])
        os.fsync(fd)
        os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    record = dict(spec)
    record["sha256"] = common.sha256(common.cache_root(int(spec["L"])) / str(spec["path"]))
    record.pop("L")
    return record


def _prepare_parent() -> None:
    if common.CACHE_PARENT.exists():
        if common.CACHE_PARENT.is_symlink() or not common.CACHE_PARENT.is_dir():
            raise common.Refusal("canonical cache parent is not an ordinary directory")
    else:
        common.CACHE_PARENT.mkdir(mode=0o755)


def build(length: int) -> None:
    common.validate_freeze()
    _gate, dual_hash = common.require_dual_gate(length)
    root = common.cache_root(length)
    common.require_canonical(root, common.cache_root(length), "cache root")
    if root.exists():
        raise common.Refusal("refuse to overwrite canonical cache root")
    _prepare_parent()
    cache_fs = common.CACHE_PARENT.stat().st_dev
    workspace_anchor = common._existing_ancestor(common.WORKSPACE_PARENT)
    if cache_fs != workspace_anchor.stat().st_dev:
        raise common.Refusal("cache and physical workspace are not on the same frozen filesystem")
    storage = common.FROZEN_STORAGE[str(length)]
    required = storage["state_plus_actual_cache_bytes"] + common.OVERHEAD_RESERVE
    if required > common.SCRATCH_LIMIT or shutil.disk_usage(workspace_anchor).free < required:
        raise common.Refusal(f"workspace-filesystem preflight failed: required={required}")
    root.mkdir(mode=0o700)
    root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
    records: list[dict[str, object]] = []
    specs = common.expected_specs(length)
    specs_by_name = {row["path"]: dict(row, L=length) for row in specs}
    try:
        edges = physical.hostile_edges(length)
        words_by_q: dict[int, np.ndarray] = {}
        for q in range(length + 1):
            words, offsets, sources, targets = operator_arrays(length, q, edges)
            words_by_q[q] = words
            arrays = {
                f"q_{q:02d}_words.u32": words, f"q_{q:02d}_offsets.u64": offsets,
                f"q_{q:02d}_sources.i32": sources, f"q_{q:02d}_targets.i32": targets,
            }
            for name, array in arrays.items():
                if name in specs_by_name:  # q=0 source/target arrays are uniquely empty and omitted.
                    records.append(raw_write(root_fd, specs_by_name[name], array))
        for event in range(length):
            for q in range(1, event + 2):
                occupied, old = admission_arrays(length, event, q, words_by_q[q])
                for role, array in (("occupied", occupied), ("old", old)):
                    name = f"event_{event:02d}_q_{q:02d}_{role}.i32"
                    records.append(raw_write(root_fd, specs_by_name[name], array))
        for event in range(length - 1):
            for q in range(event + 1):
                same, added = lineage_arrays(event, q)
                for role, array in (("same", same), ("added", added)):
                    name = f"prefix_{event:02d}_q_{q:02d}_{role}.i32"
                    records.append(raw_write(root_fd, specs_by_name[name], array))
        expected_without_hash = specs
        if [{k: v for k, v in row.items() if k != "sha256"} for row in records] != expected_without_hash:
            raise AssertionError("created cache record order/census mismatch")
        actual = sum(int(row["bytes"]) for row in records)
        if len(records) != storage["array_file_count"] or actual != storage["actual_cache_array_bytes"]:
            raise AssertionError("created cache byte/file census mismatch")
        freeze = common.validate_freeze()
        manifest = {
            "schema": "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R2",
            "status": "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE",
            "L": length, "basis_order": "REVERSED_COMBINATION__FULL_MASK",
            "edge_layout": [list(edge) for edge in edges], "hamiltonian_exchange_coefficient": -1,
            "files": records, "array_file_count": len(records),
            "manifest_inclusive_file_count": len(records) + 1,
            "payload": storage, "method_sha256": freeze["files"]["method"],
            "common_sha256": freeze["files"]["common"], "builder_sha256": freeze["files"]["builder"],
            "consumer_sha256": freeze["files"]["consumer"], "freeze_sha256": common.sha256(common.FREEZE),
            "dual_obstruction_gate_sha256": dual_hash,
            "canonical_cache_root": str(root),
            "claim_boundary": "STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
        }
        name = "CACHE_MANIFEST.json"
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                     0o444, dir_fd=root_fd)
        try:
            encoded = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
            os.write(fd, encoded)
            os.fsync(fd)
            os.fchmod(fd, 0o444)
        finally:
            os.close(fd)
        os.fchmod(root_fd, 0o555)
    finally:
        os.close(root_fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, choices=common.SUPPORTED, required=True)
    args = parser.parse_args()
    try:
        build(args.length)
    except (AssertionError, MemoryError, OSError, common.Refusal, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
