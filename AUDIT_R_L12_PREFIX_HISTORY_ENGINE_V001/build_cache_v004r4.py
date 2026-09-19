#!/usr/bin/env python3
"""Build one immutable hostile V004R4 reversed-index cache."""

from __future__ import annotations

import argparse
import math
import os
import shutil
import stat
import sys
from pathlib import Path

import numpy as np

import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import consume_cache_v004r4 as contract


WORD = np.dtype("<u4")
OFFSET = np.dtype("<u8")
INDEX = np.dtype("<i4")
SUPPORTED = (4, 6, 8, 10, 12)


def reverse_words(width: int, q: int) -> np.ndarray:
    return np.asarray(physical.reverse_masks(width, q), dtype=WORD)


def operator_arrays(
    length: int, q: int, edges: list[tuple[int, int, str]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    words = reverse_words(2 * length, q)
    if len(words) != math.comb(2 * length, q) or len(set(map(int, words))) != len(words):
        raise contract.Refusal("carrier word census/uniqueness mismatch")
    lookup = {int(word): index for index, word in enumerate(words)}
    offsets = [0]
    source_parts: list[np.ndarray] = []
    target_parts: list[np.ndarray] = []
    for u, v, _label in edges:
        source = np.flatnonzero(
            (((words >> u) & 1) == 1) & (((words >> v) & 1) == 0)
        ).astype(INDEX)
        expected = math.comb(2 * length - 2, q - 1) if q else 0
        if len(source) != expected:
            raise contract.Refusal("operator edge source census mismatch")
        toggle = (1 << u) | (1 << v)
        target = np.fromiter(
            (lookup[int(words[int(row)]) ^ toggle] for row in source),
            dtype=INDEX, count=len(source),
        )
        if any(
            int(words[int(target_row)]) != (int(words[int(source_row)]) ^ toggle)
            for source_row, target_row in zip(source, target)
        ):
            raise contract.Refusal("operator XOR/rank mismatch")
        source_parts.append(source)
        target_parts.append(target)
        offsets.append(offsets[-1] + expected)
    return (
        words, np.asarray(offsets, dtype=OFFSET),
        np.concatenate(source_parts) if source_parts else np.empty(0, dtype=INDEX),
        np.concatenate(target_parts) if target_parts else np.empty(0, dtype=INDEX),
    )


def admission_arrays(
    length: int, event: int, q: int, words: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    occupied = np.flatnonzero(((words >> event) & 1) == 1).astype(INDEX)
    expected = math.comb(2 * length - 1, q - 1)
    if len(occupied) != expected:
        raise contract.Refusal("admission occupied census mismatch")
    old = np.fromiter(
        (
            v3.reverse_rank(
                2 * length, q - 1,
                int(words[int(column)]) & ~(1 << event),
            )
            for column in occupied
        ),
        dtype=INDEX, count=expected,
    )
    old_words = reverse_words(2 * length, q - 1)
    if any(
        (int(old_words[int(old_row)]) | (1 << event)) != int(words[int(new_row)])
        for old_row, new_row in zip(old, occupied)
    ):
        raise contract.Refusal("admission add-event identity mismatch")
    return occupied, old


def lineage_arrays(event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
    old_words = physical.reverse_masks(event, q)
    same = np.fromiter(
        (v3.reverse_rank(event + 1, q, int(word)) for word in old_words),
        dtype=INDEX, count=len(old_words),
    )
    added = np.fromiter(
        (
            v3.reverse_rank(event + 1, q + 1, int(word) | (1 << event))
            for word in old_words
        ),
        dtype=INDEX, count=len(old_words),
    )
    same_words = physical.reverse_masks(event + 1, q)
    added_words = physical.reverse_masks(event + 1, q + 1)
    if any(int(same_words[int(row)]) != int(word) for row, word in zip(same, old_words)):
        raise contract.Refusal("lineage same-rank identity mismatch")
    if any(
        int(added_words[int(row)]) != (int(word) | (1 << event))
        for row, word in zip(added, old_words)
    ):
        raise contract.Refusal("lineage add-rank identity mismatch")
    return same, added


def cache_root(length: int) -> Path:
    return contract.HERE / f"V004R4_CACHE_PAYLOADS/L{length}"


def read_frozen_sources(custody: contract.AuthorityCustody) -> tuple[dict[str, object], dict[str, str], str]:
    freeze, freeze_hash = contract.read_authority(custody, contract.FREEZE, "V004R4 freeze")
    expected_paths = {
        contract.METHOD.name: contract.METHOD,
        Path(__file__).name: Path(__file__).resolve(),
        contract.CONSUMER.name: contract.CONSUMER,
        contract.PREFLIGHT.name: contract.PREFLIGHT,
        **contract.EXECUTED_DEPENDENCIES,
    }
    hashes: dict[str, str] = {}
    for name, path in expected_paths.items():
        expected = freeze.get("files", {}).get(name)
        if not contract.sha256_text(expected):
            raise contract.Refusal(f"V004R4 freeze omits source: {name}")
        _unused, hashes[name] = custody.authenticate(path, f"V004R4 source {name}", expected)
    if (
        freeze.get("schema") != "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4"
        or freeze.get("status") != "FROZEN_BEFORE_CACHE_OR_HISTORY_OUTPUT"
        or freeze.get("files") != hashes
        or freeze.get("cache_payload_created") is not False
        or freeze.get("physical_history_executed") is not False
        or freeze.get("claim_boundary")
        != "V004R4_CROSS_BRANCH_STORAGE_CONTROL_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY"
    ):
        raise contract.Refusal("V004R4 freeze/source contract mismatch")
    return freeze, hashes, freeze_hash


def require_build_authorization(
    custody: contract.AuthorityCustody, freeze: dict[str, object],
    source_hashes: dict[str, str], freeze_hash: str, length: int,
) -> tuple[str, str, str]:
    preflight, preflight_hash = contract.read_authority(
        custody, contract.PREFLIGHT_RESULT, "V004R4 nonphysical preflight",
    )
    gate, gate_hash = contract.read_authority(
        custody, contract.CACHE_BUILD_AUTHORIZATION,
        "V004R4 cache build authorization",
    )
    audit_binding = contract.exact_keys(
        gate.get("independent_hostile_audit"),
        {"path", "sha256", "schema", "classification", "checks_passed", "checks_total"},
        "V004R4 cache build audit binding",
    )
    audit, audit_hash = contract.read_authority(
        custody, contract.INDEPENDENT_AUDIT, "V004R4 independent pre-payload audit",
        audit_binding["sha256"],
    )
    if (
        preflight.get("schema") != "HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT_V001"
        or preflight.get("classification") != "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT"
        or preflight.get("files") != {
            "method_sha256": source_hashes[contract.METHOD.name],
            "builder_sha256": source_hashes[Path(__file__).name],
            "consumer_sha256": source_hashes[contract.CONSUMER.name],
            "preflight_sha256": source_hashes[contract.PREFLIGHT.name],
            "freeze_sha256": freeze_hash,
        }
        or type(preflight.get("checks_total")) is not int
        or preflight["checks_total"] <= 0
        or type(preflight.get("checks_passed")) is not int
        or preflight.get("checks_passed") != preflight.get("checks_total")
        or preflight.get("failures") != []
        or preflight.get("cache_payload_created") is not False
        or preflight.get("physical_history_executed") is not False
    ):
        raise contract.Refusal("V004R4 preflight result mismatch")
    contract.validate_hostile_prepayload_audit(
        audit, freeze_sha256=freeze_hash, frozen_files=source_hashes,
        preflight_result_sha256=preflight_hash,
    )
    contract.validate_hostile_build_authorization(
        gate, audit, freeze_sha256=freeze_hash, frozen_files=source_hashes,
        audit_sha256=audit_hash,
    )
    contract.retain_build_authorization_inputs(custody, gate)
    if length not in gate["authorized_cache_lengths"]:
        raise contract.Refusal("V004R4 cache length is not authorized")
    del freeze
    return gate_hash, preflight_hash, audit_hash


def raw_write(
    root_fd: int, root: Path, spec: dict[str, object], array: np.ndarray,
    custody: contract.AuthorityCustody,
) -> dict[str, object]:
    normalized = np.ascontiguousarray(array)
    if (
        normalized.dtype.str != spec["dtype"]
        or list(normalized.shape) != spec["shape"]
        or normalized.nbytes != spec["bytes"]
    ):
        raise contract.Refusal(f"array differs from exact specification: {spec['path']}")
    descriptor = os.open(
        str(spec["path"]),
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o400, dir_fd=root_fd,
    )
    try:
        data = memoryview(normalized).cast("B")
        offset = 0
        while offset < len(data):
            written = os.write(descriptor, data[offset:])
            if written <= 0:
                raise contract.Refusal("short cache write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    path = root / str(spec["path"])
    _unused, digest = custody.authenticate(path, f"new V004R4 cache member {spec['path']}")
    return {**spec, "sha256": digest}


def build(length: int) -> None:
    root = cache_root(length)
    if root.exists() or root.is_symlink():
        raise contract.Refusal("refuse to overwrite V004R4 cache root")
    custody = contract.AuthorityCustody()
    root_fd = -1
    try:
        freeze, source_hashes_by_name, freeze_hash = read_frozen_sources(custody)
        build_gate_hash, preflight_hash, audit_hash = require_build_authorization(
            custody, freeze, source_hashes_by_name, freeze_hash, length,
        )
        parent = root.parent
        if parent.exists():
            if parent.is_symlink() or not parent.is_dir():
                raise contract.Refusal("V004R4 cache parent is not an ordinary directory")
        else:
            parent.mkdir(mode=0o755)
        storage = contract.storage_census(length)
        if shutil.disk_usage(contract.existing_ancestor(parent)).free < storage["state_cache_plus_reserve_bytes"]:
            raise contract.Refusal("V004R4 cache/workspace filesystem floor failed")
        root.mkdir(mode=0o700)
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
        specs = contract.cache_specs(length)
        by_name = {row["path"]: row for row in specs}
        records: list[dict[str, object]] = []
        edges = physical.hostile_edges(length)
        words_by_q: dict[int, np.ndarray] = {}
        for q in range(length + 1):
            words, offsets, sources, targets = operator_arrays(length, q, edges)
            words_by_q[q] = words
            arrays = {
                f"q_{q:02d}_words.u32": words,
                f"q_{q:02d}_offsets.u64": offsets,
                f"q_{q:02d}_sources.i32": sources,
                f"q_{q:02d}_targets.i32": targets,
            }
            for name, array in arrays.items():
                if name in by_name:
                    records.append(raw_write(root_fd, root, by_name[name], array, custody))
        for event in range(length):
            for q in range(1, event + 2):
                occupied, old = admission_arrays(length, event, q, words_by_q[q])
                for role, array in (("occupied", occupied), ("old", old)):
                    name = f"event_{event:02d}_q_{q:02d}_{role}.i32"
                    records.append(raw_write(root_fd, root, by_name[name], array, custody))
        for event in range(length - 1):
            for q in range(event + 1):
                same, added = lineage_arrays(event, q)
                for role, array in (("same", same), ("added", added)):
                    name = f"prefix_{event:02d}_q_{q:02d}_{role}.i32"
                    records.append(raw_write(root_fd, root, by_name[name], array, custody))
        if [{key: value for key, value in row.items() if key != "sha256"} for row in records] != specs:
            raise contract.Refusal("created V004R4 cache order/census mismatch")
        if len(records) != storage["array_file_count"] or sum(row["bytes"] for row in records) != storage["actual_cache_array_bytes"]:
            raise contract.Refusal("created V004R4 cache file/byte census mismatch")
        source_hashes = {
            "method": source_hashes_by_name[contract.METHOD.name],
            "builder": source_hashes_by_name[Path(__file__).name],
            "consumer": source_hashes_by_name[contract.CONSUMER.name],
            "preflight": source_hashes_by_name[contract.PREFLIGHT.name],
        }
        postbuild_path = contract.HERE / "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"
        manifest = {
            "schema": "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R4",
            "status": "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE",
            "L": length, "basis_order": "REVERSED_COMBINATION__FULL_MASK",
            "lineage_identity": "FULL_CANONICAL_MASK",
            "edge_layout": [list(edge) for edge in edges],
            "hamiltonian_exchange_coefficient": -1,
            "files": records, "array_file_count": len(records),
            "manifest_inclusive_file_count": len(records) + 1,
            "payload": storage,
            "method_sha256": source_hashes["method"],
            "builder_sha256": source_hashes["builder"],
            "consumer_sha256": source_hashes["consumer"],
            "preflight_sha256": source_hashes["preflight"],
            "freeze_sha256": freeze_hash,
            "preflight_result_sha256": preflight_hash,
            "independent_hostile_audit_sha256": audit_hash,
            "cache_build_authorization_gate_sha256": build_gate_hash,
            "postbuild_payload_audit": ({
                "path": str(postbuild_path),
                "schema": "HOSTILE_V004R4_POSTBUILD_PAYLOAD_AUDIT_V001",
                "identity_field": "classification",
                "identity_value": "PASS_HOSTILE_V004R4_L12_STORAGE_CACHE",
            } if length == 12 else None),
            "canonical_cache_root": str(root),
            "claim_boundary": "HOSTILE_V004R4_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
        }
        custody.verify_all()
        contract.atomic_publish(root / "CACHE_MANIFEST.json", manifest, custody)
        os.fchmod(root_fd, 0o555)
        os.fsync(root_fd)
        contract.fsync_directory(parent)
    finally:
        if root_fd >= 0:
            os.close(root_fd)
        custody.close()


def self_test() -> None:
    for length in SUPPORTED:
        specs = contract.cache_specs(length)
        storage = contract.storage_census(length)
        if (
            len(specs) != storage["array_file_count"]
            or sum(row["bytes"] for row in specs) != storage["actual_cache_array_bytes"]
            or len({row["path"] for row in specs}) != len(specs)
            or storage["state_cache_plus_reserve_bytes"]
            != storage["maximum_live_state_bytes"] + storage["actual_cache_array_bytes"]
            + contract.OVERHEAD_RESERVE
        ):
            raise contract.Refusal(f"V004R4 builder census self-test failed at L={length}")
    edges = physical.hostile_edges(4)
    for q in range(5):
        arrays = operator_arrays(4, q, edges)
        if arrays[0].dtype != WORD or arrays[1].dtype != OFFSET:
            raise contract.Refusal("V004R4 builder dtype self-test failed")
    print("PASS_V004R4_CACHE_BUILDER_SELF_TEST")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "self-test"))
    parser.add_argument("--length", type=int, choices=SUPPORTED)
    arguments = parser.parse_args()
    try:
        if arguments.mode == "self-test":
            self_test()
        else:
            if arguments.length is None:
                raise contract.Refusal("--length is required for build")
            build(arguments.length)
        return 0
    except (AssertionError, MemoryError, OSError, ValueError, contract.Refusal) as error:
        print(f"REFUSE: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
