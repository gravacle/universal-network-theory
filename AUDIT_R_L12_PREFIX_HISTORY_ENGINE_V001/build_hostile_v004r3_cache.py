#!/usr/bin/env python3
"""Hard-locked immutable cache builder for hostile V004R3."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

import numpy as np

import build_hostile_v004r2_cache as algorithms
import independent_prefix_history as physical
import v004r3_common as common


def _fd_sha256(fd: int, size: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while offset < size:
        block = os.pread(fd, min(16 * 2**20, size - offset), offset)
        if not block:
            raise common.Refusal("short read during builder descriptor authentication")
        digest.update(block); offset += len(block)
    return digest.hexdigest()


def raw_write(root_fd: int, root, spec: dict[str, object], array: np.ndarray) -> dict[str, object]:
    normalized = np.ascontiguousarray(array)
    if normalized.dtype.str != spec["dtype"] or list(normalized.shape) != spec["shape"] or normalized.nbytes != spec["bytes"]:
        raise common.Refusal(f"array differs from exact specification: {spec['path']}")
    fd = os.open(str(spec["path"]), os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                 0o400, dir_fd=root_fd)
    try:
        data = memoryview(normalized).cast("B")
        cursor = 0
        while cursor < len(data):
            written = os.write(fd, data[cursor:])
            if written <= 0:
                raise common.Refusal("short write during cache creation")
            cursor += written
        os.fsync(fd); os.fchmod(fd, 0o444)
        info = os.fstat(fd)
        if info.st_size != normalized.nbytes:
            raise common.Refusal("builder descriptor byte census mismatch")
        digest = _fd_sha256(fd, info.st_size)
    finally:
        os.close(fd)
    path = root / str(spec["path"])
    info = path.lstat()
    if path.is_symlink() or info.st_mode & 0o222 or common.sha256(path) != digest:
        raise common.Refusal("builder path/descriptor custody mismatch")
    return dict(spec, sha256=digest)


def build(length: int) -> None:
    freeze = common.validate_freeze()
    _gate, dual_hash = common.require_dual_gate(length)
    root = common.cache_root(length)
    common.require_canonical(root, common.cache_root(length), "cache root")
    if root.exists():
        raise common.Refusal("refuse to overwrite V004R3 cache")
    if common.CACHE_PARENT.exists():
        if common.CACHE_PARENT.is_symlink() or not common.CACHE_PARENT.is_dir():
            raise common.Refusal("canonical cache parent invalid")
    else:
        common.CACHE_PARENT.mkdir(mode=0o755)
    workspace_fs = common.existing_ancestor(common.WORKSPACE_PARENT)
    if common.CACHE_PARENT.stat().st_dev != workspace_fs.stat().st_dev:
        raise common.Refusal("cache/workspace filesystem mismatch")
    required = common.FROZEN_STORAGE[str(length)]["state_plus_actual_cache_bytes"] + common.OVERHEAD_RESERVE
    if required > common.SCRATCH_LIMIT or shutil.disk_usage(workspace_fs).free < required:
        raise common.Refusal(f"workspace-filesystem scratch preflight failed: required={required}")
    root.mkdir(mode=0o700)
    root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
    records: list[dict[str, object]] = []
    specs = common.expected_specs(length)
    by_name = {row["path"]: row for row in specs}
    try:
        edges = physical.hostile_edges(length)
        words_by_q: dict[int, np.ndarray] = {}
        for q in range(length + 1):
            words, offsets, sources, targets = algorithms.operator_arrays(length, q, edges)
            words_by_q[q] = words
            arrays = {f"q_{q:02d}_words.u32": words, f"q_{q:02d}_offsets.u64": offsets,
                      f"q_{q:02d}_sources.i32": sources, f"q_{q:02d}_targets.i32": targets}
            for name, array in arrays.items():
                if name in by_name:
                    records.append(raw_write(root_fd, root, by_name[name], array))
        for event in range(length):
            for q in range(1, event + 2):
                occupied, old = algorithms.admission_arrays(length, event, q, words_by_q[q])
                for role, array in (("occupied", occupied), ("old", old)):
                    name = f"event_{event:02d}_q_{q:02d}_{role}.i32"
                    records.append(raw_write(root_fd, root, by_name[name], array))
        for event in range(length - 1):
            for q in range(event + 1):
                same, added = algorithms.lineage_arrays(event, q)
                for role, array in (("same", same), ("added", added)):
                    name = f"prefix_{event:02d}_q_{q:02d}_{role}.i32"
                    records.append(raw_write(root_fd, root, by_name[name], array))
        created_specs = [{key: value for key, value in row.items() if key != "sha256"} for row in records]
        if created_specs != specs:
            raise common.Refusal("created V004R3 record order/census mismatch")
        storage = common.FROZEN_STORAGE[str(length)]
        if len(records) != storage["array_file_count"] or sum(row["bytes"] for row in records) != storage["actual_cache_array_bytes"]:
            raise common.Refusal("created V004R3 file/byte total mismatch")
        manifest = {
            "schema": "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R3",
            "status": "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE", "L": length,
            "basis_order": "REVERSED_COMBINATION__FULL_MASK", "edge_layout": [list(edge) for edge in edges],
            "hamiltonian_exchange_coefficient": -1, "files": records,
            "array_file_count": len(records), "manifest_inclusive_file_count": len(records) + 1,
            "payload": storage, "method_sha256": freeze["files"]["method"],
            "common_sha256": freeze["files"]["common"], "builder_sha256": freeze["files"]["builder"],
            "consumer_sha256": freeze["files"]["consumer"], "freeze_sha256": common.sha256(common.FREEZE),
            "dual_obstruction_gate_sha256": dual_hash, "canonical_cache_root": str(root),
            "claim_boundary": "STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
        }
        encoded = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        fd = os.open("CACHE_MANIFEST.json", os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                     0o400, dir_fd=root_fd)
        try:
            os.write(fd, encoded); os.fsync(fd); os.fchmod(fd, 0o444)
            if _fd_sha256(fd, len(encoded)) != hashlib.sha256(encoded).hexdigest():
                raise common.Refusal("manifest stable-descriptor hash mismatch")
        finally:
            os.close(fd)
        os.fchmod(root_fd, 0o555)
    finally:
        os.close(root_fd)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--length", type=int, choices=common.SUPPORTED, required=True)
    args = parser.parse_args()
    try:
        build(args.length)
    except (AssertionError, MemoryError, OSError, common.Refusal, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
