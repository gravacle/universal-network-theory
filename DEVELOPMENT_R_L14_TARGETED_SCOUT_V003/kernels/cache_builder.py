#!/usr/bin/env python3
"""Resumable immutable L14 cache construction for Target and Hostile."""

from __future__ import annotations

import json
import math
import os
import shutil
from pathlib import Path
from typing import Any, Dict, Iterator, Mapping, Tuple

import numpy as np

from exact_common import (
    ExactKernelRefusal,
    chmod_tree_readonly,
    fsync_directory,
    immutable_json,
    load_frozen,
    read_json,
    sha256_file,
)


def _write_raw(path: Path, array: np.ndarray) -> Dict[str, Any]:
    normalized = np.ascontiguousarray(array)
    expected_hash = __import__("hashlib").sha256(memoryview(normalized).cast("B")).hexdigest()
    if path.exists():
        expected_bytes = normalized.nbytes
        if path.stat().st_size != expected_bytes or sha256_file(path) != expected_hash:
            raise ExactKernelRefusal("partial cache member collision: {}".format(path))
        return {
            "path": path.name,
            "dtype": normalized.dtype.str,
            "shape": list(normalized.shape),
            "bytes": expected_bytes,
            "sha256": expected_hash,
        }
    descriptor = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        view = memoryview(normalized).cast("B")
        offset = 0
        while offset < len(view):
            written = os.write(descriptor, view[offset:])
            if written <= 0:
                raise ExactKernelRefusal("short cache write: {}".format(path))
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
    finally:
        os.close(descriptor)
    fsync_directory(path.parent)
    return {
        "path": path.name,
        "dtype": normalized.dtype.str,
        "shape": list(normalized.shape),
        "bytes": normalized.nbytes,
        "sha256": expected_hash,
    }


def _target_arrays(length: int, target: Any) -> Iterator[Tuple[str, np.ndarray, Dict[str, Any]]]:
    """Yield one cache array at a time so operator payloads are not accumulated."""
    edges = target.v004.sealed.graph(length)
    words_by_q: Dict[int, np.ndarray] = {}
    for q in range(length + 1):
        words, offsets, sources, targets = target.builder.exact_operator_arrays(length, q, edges)
        words_by_q[q] = words
        for name, array, role in (
            ("carrier_q_{:02d}_words.u32".format(q), words, "words"),
            ("carrier_q_{:02d}_offsets.u64".format(q), offsets, "offsets"),
            ("carrier_q_{:02d}_sources.i32".format(q), sources, "sources"),
            ("carrier_q_{:02d}_targets.i32".format(q), targets, "targets"),
        ):
            yield name, array, {"kind": "operator", "q": q, "role": role}
    for event in range(length):
        for q in range(event + 1):
            blank, destination = target.builder.exact_admission_arrays(
                length, event, q, words_by_q[q], words_by_q[q + 1]
            )
            yield (
                "admission_n_{:02d}_q_{:02d}_blank.i32".format(event, q), blank,
                {"kind": "admission", "event": event, "q": q, "role": "blank"},
            )
            yield (
                "admission_n_{:02d}_q_{:02d}_destination.i32".format(event, q), destination,
                {"kind": "admission", "event": event, "q": q, "role": "destination"},
            )
    lineage_by_prefix: Dict[Tuple[int, int], np.ndarray] = {}
    for prefix in range(length):
        for q in range(prefix + 1):
            words = target.builder.lineage_words(prefix, q)
            lineage_by_prefix[(prefix, q)] = words
            yield (
                "lineage_n_{:02d}_q_{:02d}_words.u32".format(prefix, q), words,
                {"kind": "lineage_mask", "prefix": prefix, "q": q, "role": "words"},
            )
    for prefix in range(length - 1):
        for q in range(prefix + 1):
            stay, accepted = target.builder.exact_lineage_maps(
                prefix,
                q,
                lineage_by_prefix[(prefix, q)],
                lineage_by_prefix[(prefix + 1, q)],
                lineage_by_prefix[(prefix + 1, q + 1)],
            )
            yield (
                "lineage_n_{:02d}_q_{:02d}_stay.i32".format(prefix, q), stay,
                {"kind": "lineage_map", "prefix": prefix, "q": q, "role": "stay"},
            )
            yield (
                "lineage_n_{:02d}_q_{:02d}_accepted.i32".format(prefix, q), accepted,
                {"kind": "lineage_map", "prefix": prefix, "q": q, "role": "accepted"},
            )


def _hostile_arrays(length: int, hostile: Any) -> Iterator[Tuple[str, np.ndarray, Dict[str, Any]]]:
    """Yield one independent-control cache array at a time."""
    builder = __import__("build_cache_v004r4")
    edges = hostile.physical.hostile_edges(length)
    words_by_q: Dict[int, np.ndarray] = {}
    for q in range(length + 1):
        words, offsets, sources, targets = builder.operator_arrays(length, q, edges)
        words_by_q[q] = words
        pairs = (
            ("q_{:02d}_words.u32".format(q), words, "words"),
            ("q_{:02d}_offsets.u64".format(q), offsets, "offsets"),
        )
        for name, array, role in pairs:
            yield name, array, {"kind": "operator", "q": q, "role": role}
        if q:
            yield "q_{:02d}_sources.i32".format(q), sources, {"kind": "operator", "q": q, "role": "sources"}
            yield "q_{:02d}_targets.i32".format(q), targets, {"kind": "operator", "q": q, "role": "targets"}
    for event in range(length):
        for q in range(1, event + 2):
            occupied, old = builder.admission_arrays(length, event, q, words_by_q[q])
            yield "event_{:02d}_q_{:02d}_occupied.i32".format(event, q), occupied, {"kind": "admission", "event": event, "q": q, "role": "occupied"}
            yield "event_{:02d}_q_{:02d}_old.i32".format(event, q), old, {"kind": "admission", "event": event, "q": q, "role": "old"}
    for event in range(length - 1):
        for q in range(event + 1):
            same, added = builder.lineage_arrays(event, q)
            yield "prefix_{:02d}_q_{:02d}_same.i32".format(event, q), same, {"kind": "lineage", "event": event, "q": q, "role": "same"}
            yield "prefix_{:02d}_q_{:02d}_added.i32".format(event, q), added, {"kind": "lineage", "event": event, "q": q, "role": "added"}


def authenticate_cache(root: Path, branch: str, length: int) -> Tuple[str, Dict[str, Any]]:
    manifest_path = root / "CACHE_MANIFEST.json"
    if not manifest_path.is_file():
        raise ExactKernelRefusal("cache manifest absent: {}".format(root))
    manifest = read_json(manifest_path)
    schema = "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012" if branch == "target" else "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4"
    if manifest.get("schema") != schema or manifest.get("L") != length:
        raise ExactKernelRefusal("cache manifest identity mismatch")
    records = manifest.get("files")
    if not isinstance(records, list):
        raise ExactKernelRefusal("cache manifest file census absent")
    expected = {record["path"] for record in records}
    observed = {path.name for path in root.iterdir()} - {"CACHE_MANIFEST.json"}
    if expected != observed:
        raise ExactKernelRefusal("cache exact member census mismatch")
    for record in records:
        path = root / record["path"]
        if path.is_symlink() or not path.is_file() or path.stat().st_size != record["bytes"]:
            raise ExactKernelRefusal("cache member identity mismatch: {}".format(path))
        if sha256_file(path) != record["sha256"]:
            raise ExactKernelRefusal("cache member hash mismatch: {}".format(path))
    return sha256_file(manifest_path), manifest


def build_cache(root: Path, branch: str, length: int = 14) -> Tuple[str, Dict[str, Any]]:
    """Build each member owner-once and resume safely at file granularity."""

    if length != 14 or branch not in {"target", "hostile"}:
        raise ExactKernelRefusal("L14 cache identity mismatch")
    if (root / "CACHE_MANIFEST.json").exists():
        return authenticate_cache(root, branch, length)
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink():
        raise ExactKernelRefusal("cache root may not be a symlink")
    repair, _target_response, _hostile_response, _classifier, _interval = load_frozen()
    arrays = _target_arrays(length, repair.target) if branch == "target" else _hostile_arrays(length, repair.hostile)
    records = []
    for name, array, metadata in arrays:
        record = _write_raw(root / name, array)
        record.update(metadata)
        records.append(record)
        immutable_json(root / ".journal" / (name + ".json"), record)
    schema = "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012" if branch == "target" else "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4"
    manifest = {
        "schema": schema,
        "L": length,
        "branch": branch,
        "files": records,
        "total_bytes": sum(record["bytes"] for record in records),
        "construction": "FILE_GRANULAR_OWNER_ONCE_EXACT_LENGTH_GENERIC_PREDECESSOR_FORMULAS",
    }
    journal = root / ".journal"
    if journal.exists():
        shutil.rmtree(journal)
        fsync_directory(root)
    immutable_json(root / "CACHE_MANIFEST.json", manifest)
    chmod_tree_readonly(root)
    return authenticate_cache(root, branch, length)
