#!/usr/bin/env python3
"""Print strict ancestry support for the authenticated L08 and L10 caches."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

import numpy as np


ROOT = Path(__file__).resolve().parent.parent
ADMISSION_FACTOR = math.sin(math.pi / 4.0) ** 2
STAY_BLANK_FACTOR = math.cos(math.pi / 4.0) ** 2
ABS_TOLERANCE = 1.0e-12


class ExtractionError(RuntimeError):
    """An authenticated cache predicate failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(16 * 2**20), b""):
                digest.update(block)
    except OSError as error:
        raise ExtractionError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def cache_records(document: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    ledger = document.get("files")
    if not isinstance(ledger, list):
        raise ExtractionError("cache files ledger absent")
    answer: dict[str, Mapping[str, Any]] = {}
    for item in ledger:
        if not isinstance(item, Mapping) or not isinstance(item.get("path"), str):
            raise ExtractionError("malformed cache record")
        name = item["path"]
        if name in answer:
            raise ExtractionError(f"duplicate cache record {name}")
        answer[name] = item
    return answer


def open_cache_array(
    root: Path, ledger: Mapping[str, Mapping[str, Any]], name: str
) -> np.memmap:
    record = ledger.get(name)
    if record is None:
        raise ExtractionError(f"cache manifest lacks {name}")
    try:
        dtype = np.dtype(record["dtype"])
        shape = tuple(record["shape"])
        expected_bytes = int(record["bytes"])
        expected_hash = str(record["sha256"])
    except (KeyError, TypeError, ValueError) as error:
        raise ExtractionError(f"malformed cache record {name}: {error}") from error
    if not shape or any(type(value) is not int or value < 0 for value in shape):
        raise ExtractionError(f"invalid shape for {name}: {shape}")
    if math.prod(shape) * dtype.itemsize != expected_bytes:
        raise ExtractionError(f"shape/byte mismatch for {name}")
    path = (root / name).resolve()
    if path.parent != root.resolve() or not path.is_file() or path.is_symlink():
        raise ExtractionError(f"unsafe or absent cache array {name}")
    if path.stat().st_size != expected_bytes or sha256_file(path) != expected_hash:
        raise ExtractionError(f"cache array authentication failed: {name}")
    return np.memmap(path, dtype=dtype, mode="r", shape=shape)


def close_array(array: np.ndarray) -> None:
    mapping = getattr(array, "_mmap", None)
    if mapping is not None:
        mapping.close()


def row_split(
    shard: np.ndarray, blank_indices: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    stay = np.empty(shard.shape[0], dtype=np.float64)
    accepted = np.empty(shard.shape[0], dtype=np.float64)
    columns = np.asarray(blank_indices, dtype=np.int64)
    for row_index in range(shard.shape[0]):
        row = np.asarray(shard[row_index])
        total = float(np.vdot(row, row).real)
        selected = np.asarray(row[columns])
        blank = float(np.vdot(selected, selected).real)
        accepted[row_index] = ADMISSION_FACTOR * blank
        stay[row_index] = total - (1.0 - STAY_BLANK_FACTOR) * blank
    if (
        not np.all(np.isfinite(stay))
        or not np.all(np.isfinite(accepted))
        or float(stay.min(initial=0.0)) < -ABS_TOLERANCE
        or float(accepted.min(initial=0.0)) < -ABS_TOLERANCE
    ):
        raise ExtractionError("terminal row split produced invalid probability mass")
    stay[abs(stay) < 1e-16] = 0.0
    accepted[abs(accepted) < 1e-16] = 0.0
    return stay, accepted


def weight(length: int) -> float:
    prefix = length - 1
    cache = (
        ROOT
        / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        / "CACHE_PAYLOADS_V012"
        / f"L{length}"
    )
    shards = (
        ROOT
        / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        / "WORKSPACES"
        / f"L{length}"
        / "sharp"
        / f"prefix_{prefix:02d}"
    )
    manifest_path = cache / "CACHE_MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ExtractionError(f"cache manifest is unreadable: {error}") from error
    if not isinstance(manifest, Mapping):
        raise ExtractionError("cache manifest is not a JSON object")
    records = cache_records(manifest)
    event_window = range(6, length + 1)
    event_mass = np.zeros(len(event_window), dtype=np.float64)

    for q in range(4, length):
        blank_name = f"admission_n_{prefix:02d}_q_{q:02d}_blank.i32"
        lineage_name = f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32"
        blank = open_cache_array(cache, records, blank_name)
        lineage = open_cache_array(cache, records, lineage_name)
        shard_path = (shards / f"q_{q:02d}.npy").resolve()
        if shard_path.parent != shards.resolve() or shard_path.is_symlink():
            raise ExtractionError(f"unsafe shard path for q={q}")
        shard = np.load(shard_path, mmap_mode="r", allow_pickle=False)
        try:
            stay, accepted = row_split(shard, blank)
            for row, mask_value in enumerate(lineage):
                for mask, mass in (
                    (int(mask_value), float(stay[row])),
                    (int(mask_value) | (1 << prefix), float(accepted[row])),
                ):
                    events = tuple(
                        bit + 1 for bit in range(length) if mask & (1 << bit)
                    )
                    if len(events) < 6 or events[4] < 6 or events[5] > length:
                        continue
                    for index, event in enumerate(event_window):
                        if events[4] <= event < events[5]:
                            event_mass[index] += mass
        finally:
            close_array(blank)
            close_array(lineage)
            close_array(shard)

    return float(np.mean(event_mass))


def main() -> None:
    for size in (8, 10):
        print(f"L{size:02d}: {weight(size):.10f}")


if __name__ == "__main__":
    main()
