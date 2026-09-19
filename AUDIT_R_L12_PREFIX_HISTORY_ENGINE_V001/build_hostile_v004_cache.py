#!/usr/bin/env python3
"""Gate-locked builder for the hostile V004 storage-only index cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import sys
from pathlib import Path

import numpy as np

import independent_prefix_history as physical
import independent_prefix_history_v003 as v3


HERE = Path(__file__).resolve().parent
FREEZE = HERE / "FROZEN_MANIFEST_V004.json"
METHOD = HERE / "V004_STORAGE_ONLY_CACHE_METHOD.md"
CONSUMER = HERE / "independent_prefix_history_v004.py"
BUILD_GATE = HERE / "CACHE_PAYLOAD_BUILD_GATE_V004.json"
SUPPORTED = (4, 6, 8, 10, 12)
SCRATCH_LIMIT = 20 * 2**30
OVERHEAD_RESERVE = 2**20
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


def cache_operator_bytes(length: int) -> int:
    return sum(
        4 * math.comb(2 * length, q)
        + 8 * (3 * length) * (math.comb(2 * length - 2, q - 1) if q else 0)
        for q in range(length + 1)
    )


def cache_admission_bytes(length: int) -> int:
    return sum(
        8 * math.comb(2 * length - 1, q - 1)
        for event in range(length)
        for q in range(1, event + 2)
    )


def cache_lineage_bytes(length: int) -> int:
    return sum(8 * (2**event) for event in range(length - 1))


def cache_payload_bytes(length: int) -> int:
    return cache_operator_bytes(length) + cache_admission_bytes(length) + cache_lineage_bytes(length)


def maximum_state_bytes(length: int) -> int:
    dimensions = [
        sum(math.comb(prefix, q) * math.comb(2 * length, q) for q in range(prefix + 1))
        for prefix in range(length)
    ]
    if length == 1:
        return 16 * dimensions[0]
    return 16 * max(dimensions[index] + dimensions[index + 1] for index in range(length - 1))


def reverse_words(width: int, q: int) -> np.ndarray:
    words = physical.reverse_masks(width, q)
    return np.asarray(words, dtype=WORD_DTYPE)


def raw_write(path: Path, array: np.ndarray) -> dict[str, object]:
    if path.exists():
        raise Refusal(f"refuse to overwrite cache member: {path}")
    normalized = np.ascontiguousarray(array)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(normalized.tobytes(order="C"))
    return {
        "path": path.name,
        "dtype": normalized.dtype.str,
        "shape": list(normalized.shape),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def exact_operator_arrays(length: int, q: int, edges: list[tuple[int, int, str]]) -> tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray
]:
    words = reverse_words(2 * length, q)
    if len(words) != math.comb(2 * length, q):
        raise AssertionError("carrier basis census")
    if len(set(map(int, words))) != len(words):
        raise AssertionError("carrier basis uniqueness")
    if any(bin(int(word)).count("1") != q for word in words):
        raise AssertionError("carrier basis Hamming weight")
    lookup = {int(word): index for index, word in enumerate(words)}
    offsets = [0]
    source_parts: list[np.ndarray] = []
    target_parts: list[np.ndarray] = []
    for u, v, _label in edges:
        source = np.flatnonzero(
            (((words >> u) & 1) != 0) & (((words >> v) & 1) == 0)
        ).astype(INDEX_DTYPE)
        expected = math.comb(2 * length - 2, q - 1) if q else 0
        if len(source) != expected:
            raise AssertionError("edge source census")
        toggle = (1 << u) | (1 << v)
        target = np.fromiter(
            (lookup[int(words[index]) ^ toggle] for index in source),
            dtype=INDEX_DTYPE,
            count=len(source),
        )
        if len(np.unique(source)) != len(source) or len(np.unique(target)) != len(target):
            raise AssertionError("edge rank injectivity")
        if any(int(words[int(target_row)]) != (int(words[int(source_row)]) ^ toggle)
               for source_row, target_row in zip(source, target)):
            raise AssertionError("edge XOR/rank identity")
        source_parts.append(source)
        target_parts.append(target)
        offsets.append(offsets[-1] + len(source))
    sources = np.concatenate(source_parts) if source_parts else np.empty(0, dtype=INDEX_DTYPE)
    targets = np.concatenate(target_parts) if target_parts else np.empty(0, dtype=INDEX_DTYPE)
    return (
        words,
        np.asarray(offsets, dtype=OFFSET_DTYPE),
        np.asarray(sources, dtype=INDEX_DTYPE),
        np.asarray(targets, dtype=INDEX_DTYPE),
    )


def admission_arrays(length: int, event: int, q: int, words: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    occupied = np.flatnonzero(((words >> event) & 1) != 0).astype(INDEX_DTYPE)
    expected = math.comb(2 * length - 1, q - 1)
    if len(occupied) != expected:
        raise AssertionError("admission occupied-column census")
    old = np.fromiter(
        (
            v3.reverse_rank(2 * length, q - 1, int(words[column]) & ~(1 << event))
            for column in occupied
        ),
        dtype=INDEX_DTYPE,
        count=len(occupied),
    )
    old_words = reverse_words(2 * length, q - 1)
    if any(
        int(old_words[int(old_row)]) | (1 << event) != int(words[int(new_row)])
        for old_row, new_row in zip(old, occupied)
    ):
        raise AssertionError("admission exact add-event identity")
    if len(np.unique(old)) != len(old) or len(np.unique(occupied)) != len(occupied):
        raise AssertionError("admission map injectivity")
    return occupied, old


def lineage_arrays(event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
    old_words = physical.reverse_masks(event, q)
    same = np.fromiter(
        (v3.reverse_rank(event + 1, q, int(word)) for word in old_words),
        dtype=INDEX_DTYPE,
        count=len(old_words),
    )
    added = np.fromiter(
        (v3.reverse_rank(event + 1, q + 1, int(word) | (1 << event)) for word in old_words),
        dtype=INDEX_DTYPE,
        count=len(old_words),
    )
    same_words = physical.reverse_masks(event + 1, q)
    added_words = physical.reverse_masks(event + 1, q + 1)
    if any(int(same_words[int(rank)]) != int(word) for rank, word in zip(same, old_words)):
        raise AssertionError("lineage stay identity")
    if any(int(added_words[int(rank)]) != (int(word) | (1 << event))
           for rank, word in zip(added, old_words)):
        raise AssertionError("lineage write identity")
    return same, added


def require_build_gate(length: int) -> dict[str, object]:
    if not BUILD_GATE.is_file():
        raise Refusal("cache payload locked: future build gate is absent")
    gate = json.loads(BUILD_GATE.read_text(encoding="utf-8"))
    if gate.get("classification") != "AUTHORIZE_HOSTILE_V004_CACHE_AFTER_DUAL_6H_OBSTRUCTION":
        raise Refusal("cache payload locked: authorization classification absent")
    required = {
        "builder_sha256": sha256(Path(__file__)),
        "consumer_sha256": sha256(CONSUMER),
        "method_sha256": sha256(METHOD),
        "freeze_sha256": sha256(FREEZE),
    }
    for key, value in required.items():
        if gate.get(key) != value:
            raise Refusal(f"cache payload gate does not pin {key}")
    authorized_lengths = gate.get("authorized_lengths")
    if not isinstance(authorized_lengths, list) or length not in authorized_lengths:
        raise Refusal("cache payload gate length mismatch")
    obstructions = gate.get("current_run_obstructions")
    if not isinstance(obstructions, list) or {row.get("role") for row in obstructions if isinstance(row, dict)} != {"target", "hostile"}:
        raise Refusal("dual current-run obstruction custody is absent")
    for row in obstructions:
        relative = row.get("path")
        if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise Refusal("current-run obstruction path is unsafe")
        path = HERE.parent / relative
        if not path.is_file() or sha256(path) != row.get("sha256"):
            raise Refusal("current-run obstruction hash mismatch")
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("wall_limit_seconds") != 21600 or record.get("classification") != "SIX_HOUR_RESOURCE_OBSTRUCTION":
            raise Refusal("current run did not record the frozen six-hour obstruction")
    return gate


def build(length: int, output: Path) -> None:
    if length not in SUPPORTED:
        raise Refusal("unsupported cache size")
    require_build_gate(length)
    if output.exists():
        raise Refusal("refuse to overwrite cache output")
    required = cache_payload_bytes(length) + maximum_state_bytes(length) + OVERHEAD_RESERVE
    if not output.parent.is_dir():
        raise Refusal("cache output parent does not exist")
    free = shutil.disk_usage(output.parent).free
    if required > SCRATCH_LIMIT or free < required:
        raise Refusal(f"cache scratch preflight failed: required={required} free={free}")
    output.mkdir(parents=False)
    edges = physical.hostile_edges(length)
    files: list[dict[str, object]] = []
    operator_bytes = 0
    admission_bytes = 0
    lineage_bytes = 0
    for q in range(length + 1):
        words, offsets, sources, targets = exact_operator_arrays(length, q, edges)
        prefix = f"q_{q:02d}"
        records = [
            raw_write(output / f"{prefix}_words.u32", words),
            raw_write(output / f"{prefix}_offsets.u64", offsets),
            raw_write(output / f"{prefix}_sources.i32", sources),
            raw_write(output / f"{prefix}_targets.i32", targets),
        ]
        for record in records:
            record.update({"kind": "operator", "q": q})
        files.extend(records)
        operator_bytes += sum(int(record["bytes"]) for record in records if "offsets" not in record["path"])
        # Offsets are format overhead, excluded from the frozen raw-payload identity.
        for event in range(q - 1, length):
            if q == 0:
                continue
            occupied, old = admission_arrays(length, event, q, words)
            for label, array in (("occupied", occupied), ("old", old)):
                record = raw_write(output / f"event_{event:02d}_q_{q:02d}_{label}.i32", array)
                record.update({"kind": "admission", "event": event, "q": q, "role": label})
                files.append(record)
                admission_bytes += int(record["bytes"])
    for event in range(length - 1):
        for q in range(event + 1):
            same, added = lineage_arrays(event, q)
            for label, array in (("same", same), ("added", added)):
                record = raw_write(output / f"prefix_{event:02d}_q_{q:02d}_{label}.i32", array)
                record.update({"kind": "lineage", "event": event, "q": q, "role": label})
                files.append(record)
                lineage_bytes += int(record["bytes"])
    if operator_bytes != cache_operator_bytes(length):
        raise AssertionError("operator cache byte census")
    if admission_bytes != cache_admission_bytes(length):
        raise AssertionError("admission cache byte census")
    if lineage_bytes != cache_lineage_bytes(length):
        raise AssertionError("lineage cache byte census")
    manifest = {
        "schema": "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004",
        "status": "COMPLETE_HASH_PINNED_STORAGE_ONLY_CACHE",
        "L": length,
        "basis_order": "REVERSED_COMBINATION__FULL_MASK",
        "edge_layout": [list(edge) for edge in edges],
        "hamiltonian_exchange_coefficient": -1,
        "files": files,
        "payload": {
            "operator_bytes_excluding_offsets": operator_bytes,
            "admission_bytes": admission_bytes,
            "lineage_bytes": lineage_bytes,
            "closed_form_raw_payload_bytes_excluding_offsets": cache_payload_bytes(length),
            "actual_files_bytes_including_offsets": sum(int(row["bytes"]) for row in files),
        },
        "builder_sha256": sha256(Path(__file__)),
        "consumer_sha256": sha256(CONSUMER),
        "method_sha256": sha256(METHOD),
        "freeze_sha256": sha256(FREEZE),
        "build_gate_sha256": sha256(BUILD_GATE),
        "claim_boundary": "STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_OR_GRAVITY",
    }
    manifest_path = output / "CACHE_MANIFEST.json"
    descriptor = os.open(manifest_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, choices=SUPPORTED, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        build(args.length, args.output)
    except (AssertionError, MemoryError, OSError, Refusal, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
