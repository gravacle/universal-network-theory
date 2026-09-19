#!/usr/bin/env python3
"""Hostile V004R2 cached history consumer with stable-open authentication."""

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
import stat
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import independent_prefix_history_v004 as legacy
import v004r2_common as common


DTYPES = {"<u4": np.dtype("<u4"), "<u8": np.dtype("<u8"), "<i4": np.dtype("<i4")}


def _fd_sha256(fd: int, size: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while offset < size:
        chunk = os.pread(fd, min(16 * 2**20, size - offset), offset)
        if not chunk:
            raise common.Refusal("short cache read during hash authentication")
        digest.update(chunk)
        offset += len(chunk)
    return digest.hexdigest()


class SecureCacheContext:
    """One-open authenticated cache whose mappings derive only from held fds."""

    def __init__(self, length: int, expected_manifest_hash: str, started: float):
        self.length = length
        self.root = common.cache_root(length)
        common.require_canonical(self.root, common.cache_root(length), "cache root")
        self.started = started
        self.root_fd = -1
        self.fds: dict[str, int] = {}
        self.fingerprints: dict[str, tuple[int, int, int, int]] = {}
        self.mappings: list[np.memmap] = []
        flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
        self.root_fd = os.open(self.root, flags)
        root_stat = os.fstat(self.root_fd)
        if not stat.S_ISDIR(root_stat.st_mode) or root_stat.st_mode & 0o222:
            raise common.Refusal("cache root must be an immutable non-writable directory")
        members = sorted(os.listdir(self.root_fd))
        expected_names = [row["path"] for row in common.expected_specs(length)] + ["CACHE_MANIFEST.json"]
        if members != sorted(expected_names):
            raise common.Refusal("cache directory exact member census failed")
        manifest_fd = self._stable_open("CACHE_MANIFEST.json", None)
        manifest_size = os.fstat(manifest_fd).st_size
        if _fd_sha256(manifest_fd, manifest_size) != expected_manifest_hash:
            raise common.Refusal("cache manifest hash gate mismatch")
        manifest_bytes = os.pread(manifest_fd, manifest_size, 0)
        self.manifest = json.loads(manifest_bytes.decode("utf-8"))
        self._validate_manifest()
        for record in self.manifest["files"]:
            fd = self._stable_open(record["path"], int(record["bytes"]))
            if _fd_sha256(fd, int(record["bytes"])) != record["sha256"]:
                raise common.Refusal(f"cache member hash mismatch: {record['path']}")
        self.records = {row["path"]: row for row in self.manifest["files"]}
        self.edges = physical.hostile_edges(length)
        self._authenticate_semantics()

    def _stable_open(self, name: str, expected_size: int | None) -> int:
        if name in self.fds:
            raise common.Refusal("cache member opened more than once")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(name, flags, dir_fd=self.root_fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o222:
            os.close(fd)
            raise common.Refusal(f"cache member is non-ordinary or writable: {name}")
        if expected_size is not None and info.st_size != expected_size:
            os.close(fd)
            raise common.Refusal(f"cache member byte size mismatch: {name}")
        fingerprint = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
        self.fds[name] = fd
        self.fingerprints[name] = fingerprint
        return fd

    def _validate_manifest(self) -> None:
        freeze = common.validate_freeze()
        common.exact_keys(self.manifest, {
            "schema", "status", "L", "basis_order", "edge_layout",
            "hamiltonian_exchange_coefficient", "files", "array_file_count",
            "manifest_inclusive_file_count", "payload", "method_sha256", "common_sha256",
            "builder_sha256", "consumer_sha256", "freeze_sha256",
            "dual_obstruction_gate_sha256", "canonical_cache_root", "claim_boundary",
        }, "cache manifest")
        if not (self.manifest["schema"] == "HOSTILE_PREFIX_HISTORY_STORAGE_CACHE_V004R2"
                and self.manifest["status"] == "COMPLETE_IMMUTABLE_HASH_PINNED_STORAGE_ONLY_CACHE"
                and self.manifest["L"] == self.length
                and self.manifest["basis_order"] == "REVERSED_COMBINATION__FULL_MASK"
                and self.manifest["edge_layout"] == [list(edge) for edge in physical.hostile_edges(self.length)]
                and self.manifest["hamiltonian_exchange_coefficient"] == -1
                and self.manifest["canonical_cache_root"] == str(self.root)):
            raise common.Refusal("cache manifest physical identity failed")
        expected_hashes = {
            "method_sha256": freeze["files"]["method"], "common_sha256": freeze["files"]["common"],
            "builder_sha256": freeze["files"]["builder"], "consumer_sha256": freeze["files"]["consumer"],
            "freeze_sha256": common.sha256(common.FREEZE),
        }
        if any(self.manifest[key] != value for key, value in expected_hashes.items()):
            raise common.Refusal("cache manifest frozen-file lineage mismatch")
        if not common.DUAL_GATE.is_file() or common.sha256(common.DUAL_GATE) != self.manifest["dual_obstruction_gate_sha256"]:
            raise common.Refusal("cache manifest dual-gate lineage mismatch")
        common.require_dual_gate(self.length)
        common.validate_manifest_record_census(self.manifest, self.length)

    def _verify_fd(self, name: str) -> None:
        info = os.fstat(self.fds[name])
        if (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns) != self.fingerprints[name]:
            raise common.Refusal(f"cache fd changed after authentication: {name}")

    def _open(self, name: str, dtype: np.dtype) -> np.ndarray:
        record = self.records[name]
        if record["dtype"] != dtype.str:
            raise common.Refusal(f"cache dtype mismatch: {name}")
        self._verify_fd(name)
        shape = tuple(record["shape"])
        if int(record["bytes"]) == 0:
            array = np.empty(shape, dtype=dtype)
            array.flags.writeable = False
            return array
        stream = os.fdopen(os.dup(self.fds[name]), "rb", closefd=True)
        array = np.memmap(stream, dtype=dtype, mode="r", shape=shape)
        self.mappings.append(array)
        return array

    @staticmethod
    def _close(array: np.ndarray) -> None:
        legacy.close_mapping(array)

    def _authenticate_semantics(self) -> None:
        checks = 0
        edges = self.edges
        for q in range(self.length + 1):
            prefix = f"q_{q:02d}"
            words = self._open(f"{prefix}_words.u32", DTYPES["<u4"])
            offsets = self._open(f"{prefix}_offsets.u64", DTYPES["<u8"])
            sources = self._open(f"{prefix}_sources.i32", DTYPES["<i4"]) if q else np.empty(0, dtype="<i4")
            targets = self._open(f"{prefix}_targets.i32", DTYPES["<i4"]) if q else np.empty(0, dtype="<i4")
            expected_words = np.asarray(physical.reverse_masks(2 * self.length, q), dtype="<u4")
            if not np.array_equal(words, expected_words):
                raise common.Refusal(f"q={q} basis order/content mismatch")
            per_edge = math.comb(2 * self.length - 2, q - 1) if q else 0
            expected_offsets = np.arange(len(edges) + 1, dtype="<u8") * per_edge
            if not np.array_equal(offsets, expected_offsets) or len(sources) != len(targets):
                raise common.Refusal(f"q={q} edge offset census mismatch")
            for edge_index, (u, v, _label) in enumerate(edges):
                lower, upper = int(offsets[edge_index]), int(offsets[edge_index + 1])
                for start in range(lower, upper, 1_000_000):
                    stop = min(upper, start + 1_000_000)
                    s = np.asarray(sources[start:stop], dtype=np.int64)
                    t = np.asarray(targets[start:stop], dtype=np.int64)
                    if (np.any(s < 0) or np.any(t < 0) or np.any(s >= len(words)) or np.any(t >= len(words))):
                        raise common.Refusal("operator rank outside sector")
                    sw = words[s]
                    if np.any(((sw >> u) & 1) != 1) or np.any(((sw >> v) & 1) != 0):
                        raise common.Refusal("operator source predicate mismatch")
                    if not np.array_equal(words[t], sw ^ np.uint32((1 << u) | (1 << v))):
                        raise common.Refusal("operator XOR/target identity mismatch")
                checks += 1
            for array in (words, offsets, sources, targets):
                self._close(array)
        for event in range(self.length):
            for q in range(1, event + 2):
                occupied = self._open(f"event_{event:02d}_q_{q:02d}_occupied.i32", DTYPES["<i4"])
                old = self._open(f"event_{event:02d}_q_{q:02d}_old.i32", DTYPES["<i4"])
                new_words = np.asarray(physical.reverse_masks(2 * self.length, q), dtype="<u4")
                old_words = np.asarray(physical.reverse_masks(2 * self.length, q - 1), dtype="<u4")
                for start in range(0, len(old), 1_000_000):
                    stop = min(len(old), start + 1_000_000)
                    n, o = np.asarray(occupied[start:stop]), np.asarray(old[start:stop])
                    if np.any(n < 0) or np.any(o < 0) or np.any(n >= len(new_words)) or np.any(o >= len(old_words)):
                        raise common.Refusal("admission rank outside sector")
                    if not np.array_equal(old_words[o] | np.uint32(1 << event), new_words[n]):
                        raise common.Refusal("admission exact add-bit identity mismatch")
                self._close(occupied); self._close(old); checks += 1
        for event in range(self.length - 1):
            for q in range(event + 1):
                same = self._open(f"prefix_{event:02d}_q_{q:02d}_same.i32", DTYPES["<i4"])
                added = self._open(f"prefix_{event:02d}_q_{q:02d}_added.i32", DTYPES["<i4"])
                old_words = physical.reverse_masks(event, q)
                expected_same = np.fromiter((v3.reverse_rank(event + 1, q, int(word)) for word in old_words),
                                            dtype="<i4", count=len(old_words))
                expected_added = np.fromiter((v3.reverse_rank(event + 1, q + 1, int(word) | (1 << event))
                                              for word in old_words), dtype="<i4", count=len(old_words))
                if not np.array_equal(same, expected_same) or not np.array_equal(added, expected_added):
                    raise common.Refusal("lineage rank identity mismatch")
                self._close(same); self._close(added); checks += 1
        expected_checks = 3 * self.length * (self.length + 1) + self.length * (self.length + 1) // 2 + self.length * (self.length - 1) // 2
        if checks != expected_checks:
            raise common.Refusal("semantic sector census mismatch")
        self.semantic_checks = checks

    def carrier(self, q: int, edges: list[tuple[int, int, str]]) -> legacy.CachedCarrier:
        if edges != self.edges or q not in range(self.length + 1):
            raise common.Refusal("carrier request changed graph/sector")
        prefix = f"q_{q:02d}"
        carrier = legacy.CachedCarrier(
            self.length, q, edges, self._open(f"{prefix}_words.u32", DTYPES["<u4"]),
            self._open(f"{prefix}_offsets.u64", DTYPES["<u8"]),
            self._open(f"{prefix}_sources.i32", DTYPES["<i4"]) if q else np.empty(0, dtype="<i4"),
            self._open(f"{prefix}_targets.i32", DTYPES["<i4"]) if q else np.empty(0, dtype="<i4"),
        )
        mapped = sum(array.nbytes for array in (carrier.words, carrier.offsets, carrier.sources, carrier.targets))
        if mapped > common.FROZEN_STORAGE["12"]["maximum_q12_cache_plus_admission_bytes"]:
            raise MemoryError("one-sector cache exceeds frozen exact mapping certificate")
        return carrier

    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
        if not (0 <= event < self.length and 1 <= q <= event + 1):
            raise common.Refusal("admission request outside exact sector census")
        return (self._open(f"event_{event:02d}_q_{q:02d}_occupied.i32", DTYPES["<i4"]),
                self._open(f"event_{event:02d}_q_{q:02d}_old.i32", DTYPES["<i4"]))

    def lineage(self, event: int, q: int, added: bool) -> np.ndarray:
        if not (0 <= event < self.length - 1 and 0 <= q <= event):
            raise common.Refusal("lineage request outside exact sector census")
        role = "added" if added else "same"
        return self._open(f"prefix_{event:02d}_q_{q:02d}_{role}.i32", DTYPES["<i4"])

    def close(self) -> None:
        for mapping in self.mappings:
            self._close(mapping)
        self.mappings.clear()
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        if self.root_fd >= 0:
            os.close(self.root_fd); self.root_fd = -1


def _read_gate(path: Path, schema: str, classification: str, keys: set[str]) -> tuple[dict[str, Any], str]:
    if path.is_symlink() or not path.is_file():
        raise common.Refusal(f"physical execution locked: {path.name} absent")
    record = json.loads(path.read_text(encoding="utf-8"))
    common.exact_keys(record, keys, path.name)
    if record["schema"] != schema or record["classification"] != classification:
        raise common.Refusal(f"physical execution locked: {path.name} identity")
    return record, common.sha256(path)


def _verify_output_binding(row: dict[str, Any], length: int, cache_hash: str) -> None:
    common.exact_keys(row, {"output_path", "output_sha256", "cache_manifest_sha256"}, "history binding")
    expected = common.history_output(length)
    if row["output_path"] != str(expected) or row["cache_manifest_sha256"] != cache_hash:
        raise common.Refusal("history binding path/cache mismatch")
    if expected.is_symlink() or not expected.is_file() or common.sha256(expected) != row["output_sha256"]:
        raise common.Refusal("history binding output hash mismatch")
    output = json.loads(expected.read_text(encoding="utf-8"))
    if not (output.get("schema") == "INDEPENDENT_STORAGE_CACHED_PREFIX_HISTORY_V004R2"
            and output.get("L") == length and output.get("cache_manifest_sha256") == cache_hash
            and output.get("comparison", {}).get("resolved") is True
            and output.get("resource", {}).get("passed") is True):
        raise common.Refusal("bound history output internal result mismatch")


def _cache_hash(length: int) -> str:
    path = common.cache_root(length) / "CACHE_MANIFEST.json"
    if path.is_symlink() or not path.is_file():
        raise common.Refusal(f"L{length} canonical cache manifest absent")
    return common.sha256(path)


def _base_hashes(record: dict[str, Any], freeze: dict[str, Any]) -> None:
    expected = {"consumer_sha256": freeze["files"]["consumer"],
                "freeze_sha256": common.sha256(common.FREEZE),
                "dual_gate_sha256": common.sha256(common.DUAL_GATE)}
    if any(record[key] != value for key, value in expected.items()):
        raise common.Refusal("stage gate frozen/prerequisite hash mismatch")


def _verify_control_pass(freeze: dict[str, Any], execution_hash: str) -> str:
    keys = {"schema", "classification", "histories", "comparison_report", "prerequisites",
            "consumer_sha256", "freeze_sha256", "dual_gate_sha256", "claim_boundary"}
    gate, gate_hash = _read_gate(common.CONTROL_GATE, "HOSTILE_V004R2_CONTROL_PASS_GATE",
                                 "PASS_HOSTILE_V004R2_CACHED_CONTROLS_L4_L8", keys)
    _base_hashes(gate, freeze)
    histories = gate["histories"]
    if not isinstance(histories, dict) or set(histories) != {str(x) for x in common.CONTROL_LENGTHS}:
        raise common.Refusal("control pass history census mismatch")
    for length in common.CONTROL_LENGTHS:
        _verify_output_binding(histories[str(length)], length, _cache_hash(length))
    prereq = {"dual_gate_sha256": common.sha256(common.DUAL_GATE),
              "control_execution_gate_sha256": execution_hash}
    if gate["prerequisites"] != prereq:
        raise common.Refusal("control pass prerequisite chain mismatch")
    report = gate["comparison_report"]
    common.exact_keys(report, {"path", "sha256"}, "control comparison binding")
    report_path = common.HERE / "CONTROL_COMPARISON_V004R2.json"
    if report != {"path": str(report_path), "sha256": common.sha256(report_path) if report_path.is_file() else ""}:
        raise common.Refusal("control comparison report hash/path mismatch")
    body = json.loads(report_path.read_text(encoding="utf-8"))
    if body != {"schema": "HOSTILE_V004R2_CONTROL_COMPARISON", "classification": "PASS",
                "histories": histories, "checks_passed": body.get("checks_total"),
                "checks_total": body.get("checks_total"),
                "claim_boundary": "FINITE_CONTROL_COMPARISON_ONLY"}:
        raise common.Refusal("control comparison internal binding/checks mismatch")
    return gate_hash


def _verify_l10_pass(freeze: dict[str, Any], control_hash: str, execution_hash: str) -> str:
    keys = {"schema", "classification", "history", "comparison_report", "prerequisites",
            "consumer_sha256", "freeze_sha256", "dual_gate_sha256", "claim_boundary"}
    gate, gate_hash = _read_gate(common.L10_GATE, "HOSTILE_V004R2_L10_PASS_GATE",
                                 "PASS_HOSTILE_V004R2_CACHED_L10", keys)
    _base_hashes(gate, freeze)
    _verify_output_binding(gate["history"], 10, _cache_hash(10))
    prereq = {"dual_gate_sha256": common.sha256(common.DUAL_GATE),
              "control_pass_gate_sha256": control_hash, "L10_execution_gate_sha256": execution_hash}
    if gate["prerequisites"] != prereq:
        raise common.Refusal("L10 pass prerequisite chain mismatch")
    report = gate["comparison_report"]
    common.exact_keys(report, {"path", "sha256"}, "L10 comparison binding")
    report_path = common.HERE / "L10_COMPARISON_V004R2.json"
    if report["path"] != str(report_path) or not report_path.is_file() or common.sha256(report_path) != report["sha256"]:
        raise common.Refusal("L10 comparison report hash/path mismatch")
    body = json.loads(report_path.read_text(encoding="utf-8"))
    if not (body.get("schema") == "HOSTILE_V004R2_L10_COMPARISON" and body.get("classification") == "PASS"
            and body.get("history") == gate["history"] and body.get("checks_passed") == body.get("checks_total")):
        raise common.Refusal("L10 comparison internal binding/checks mismatch")
    return gate_hash


def _verify_target_gate() -> str:
    relative = "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json"
    expected_hash = common.SEALED_DEPENDENCIES[relative]
    path = common.safe_repo_file(relative, expected_hash)
    gate = json.loads(path.read_text(encoding="utf-8"))
    if not (gate.get("schema") == "R_TARGET_Q_SHARDED_HISTORY_GATE_V004"
            and gate.get("classification") == "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004"
            and gate.get("checks_passed") == gate.get("checks_total") == 273
            and gate.get("implementation_sha256") == common.OBSTRUCTION_ROWS["target"]["implementation_sha256"]
            and set(gate.get("histories", {})) == {"4", "6", "8", "10"}
            and all(isinstance(row.get("output_sha256"), str) and len(row["output_sha256"]) == 64
                    for row in gate["histories"].values())):
        raise common.Refusal("target V004 L12 prerequisite internal semantics mismatch")
    return expected_hash


def require_execution_gate(length: int, cache_hash: str) -> dict[str, str]:
    freeze = common.validate_freeze()
    _dual, dual_hash = common.require_dual_gate(length)
    common_keys = {"schema", "classification", "authorized_lengths", "cache_manifest_sha256_by_L",
                   "output_path_by_L", "workspace_path_by_L", "consumer_sha256", "freeze_sha256",
                   "dual_gate_sha256", "claim_boundary"}
    control, control_execution_hash = _read_gate(
        common.CONTROL_EXECUTION_GATE, "HOSTILE_V004R2_CONTROL_EXECUTION_GATE",
        "AUTHORIZE_HOSTILE_V004R2_CONTROLS_L4_L8", common_keys)
    _base_hashes(control, freeze)
    if control["authorized_lengths"] != list(common.CONTROL_LENGTHS):
        raise common.Refusal("control execution length census mismatch")
    for key, function in (("cache_manifest_sha256_by_L", _cache_hash),
                          ("output_path_by_L", lambda x: str(common.history_output(x))),
                          ("workspace_path_by_L", lambda x: str(common.workspace_root(x)))):
        expected = {str(x): function(x) for x in common.CONTROL_LENGTHS}
        if control[key] != expected:
            raise common.Refusal(f"control execution {key} exact binding mismatch")
    if length in common.CONTROL_LENGTHS:
        if cache_hash != control["cache_manifest_sha256_by_L"][str(length)]:
            raise common.Refusal("current control cache binding mismatch")
        return {"dual_gate_sha256": dual_hash, "control_execution_gate_sha256": control_execution_hash}
    control_hash = _verify_control_pass(freeze, control_execution_hash)
    l10_keys = {"schema", "classification", "authorized_length", "cache_manifest_sha256",
                "output_path", "workspace_path", "prerequisites", "consumer_sha256",
                "freeze_sha256", "dual_gate_sha256", "claim_boundary"}
    l10_exec, l10_execution_hash = _read_gate(common.L10_EXECUTION_GATE,
        "HOSTILE_V004R2_L10_EXECUTION_GATE", "AUTHORIZE_HOSTILE_V004R2_L10", l10_keys)
    _base_hashes(l10_exec, freeze)
    expected_prereq = {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash}
    if not (l10_exec["authorized_length"] == 10 and l10_exec["cache_manifest_sha256"] == _cache_hash(10)
            and l10_exec["output_path"] == str(common.history_output(10))
            and l10_exec["workspace_path"] == str(common.workspace_root(10))
            and l10_exec["prerequisites"] == expected_prereq):
        raise common.Refusal("L10 execution exact binding mismatch")
    if length == 10:
        if cache_hash != l10_exec["cache_manifest_sha256"]:
            raise common.Refusal("current L10 cache binding mismatch")
        return {**expected_prereq, "L10_execution_gate_sha256": l10_execution_hash}
    l10_hash = _verify_l10_pass(freeze, control_hash, l10_execution_hash)
    l12_keys = {"schema", "classification", "authorized_length", "cache_manifest_sha256",
                "output_path", "workspace_path", "prerequisites", "target_prerequisite",
                "consumer_sha256", "freeze_sha256", "dual_gate_sha256", "claim_boundary"}
    l12, l12_hash = _read_gate(common.L12_EXECUTION_GATE, "HOSTILE_V004R2_L12_EXECUTION_GATE",
                               "AUTHORIZE_HOSTILE_V004R2_L12", l12_keys)
    _base_hashes(l12, freeze)
    target_hash = _verify_target_gate()
    target_binding = {"path": str(common.REPO / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/TARGET_L12_GATE_V004.json"),
                      "sha256": target_hash, "classification": "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004",
                      "checks": "273/273"}
    prereq = {"dual_gate_sha256": dual_hash, "control_pass_gate_sha256": control_hash,
              "L10_pass_gate_sha256": l10_hash}
    if not (l12["authorized_length"] == 12 and l12["cache_manifest_sha256"] == cache_hash == _cache_hash(12)
            and l12["output_path"] == str(common.history_output(12))
            and l12["workspace_path"] == str(common.workspace_root(12))
            and l12["prerequisites"] == prereq and l12["target_prerequisite"] == target_binding):
        raise common.Refusal("L12 execution exact binding/prerequisite mismatch")
    return {**prereq, "L12_execution_gate_sha256": l12_hash, "target_gate_sha256": target_hash}


def execute(length: int) -> None:
    started = time.perf_counter()  # includes freeze, gates, full cache hashes, and semantic authentication
    common.validate_freeze()
    output = common.history_output(length)
    workspace = common.workspace_root(length)
    common.require_canonical(output, common.history_output(length), "history output")
    common.require_canonical(workspace, common.workspace_root(length), "history workspace")
    if output.exists() or workspace.exists():
        raise common.Refusal("refuse to overwrite canonical history output/workspace")
    manifest_path = common.cache_root(length) / "CACHE_MANIFEST.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise common.Refusal("canonical cache manifest absent")
    manifest_hash = common.sha256(manifest_path)
    prerequisite_hashes = require_execution_gate(length, manifest_hash)
    cache = SecureCacheContext(length, manifest_hash, started)
    try:
        workspace_anchor = common._existing_ancestor(common.WORKSPACE_PARENT)
        if workspace_anchor.stat().st_dev != cache.root.stat().st_dev:
            raise common.Refusal("cache and workspace filesystem identity mismatch")
        required = common.FROZEN_STORAGE[str(length)]["state_plus_actual_cache_bytes"] + common.OVERHEAD_RESERVE
        if required > common.SCRATCH_LIMIT or shutil.disk_usage(workspace_anchor).free < required:
            raise common.Refusal(f"workspace-filesystem scratch preflight failed: required={required}")
        common.WORKSPACE_PARENT.mkdir(mode=0o755, exist_ok=True)
        common.HISTORY_PARENT.mkdir(mode=0o755, exist_ok=True)
        legacy.configure(length, cache, started)
        rough_root, sharp_root = workspace / "rough", workspace / "sharp"
        rough = v3.history(length, physical.ROUGH, rough_root, retain_terminal=False)
        v3.remove_resolution(rough_root)
        sharp = v3.history(length, physical.SHARP, sharp_root, retain_terminal=True)
        comparison = physical.compare(length, rough, sharp)
        wall = time.perf_counter() - started
        rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        cache_bytes = common.FROZEN_STORAGE[str(length)]["actual_cache_array_bytes"]
        peak_scratch = max(int(rough["peak_logical_scratch_bytes"]), int(sharp["peak_logical_scratch_bytes"])) + cache_bytes
        allocation = max(int(row[key]["maximum_allocation_estimate_bytes"])
                         for row in sharp["rows"] for key in ("actual_solver", "null_solver"))
        passed = (comparison.get("resolved") is True and peak_scratch <= common.SCRATCH_LIMIT
                  and allocation <= common.NUMERICAL_WORKSPACE_LIMIT and rss <= common.RSS_LIMIT
                  and wall <= common.WALL_LIMIT)
        if not passed:
            raise common.Refusal("physical result failed numerical/resource gates; no result file written")
        result = {
            "schema": "INDEPENDENT_STORAGE_CACHED_PREFIX_HISTORY_V004R2", "L": length,
            "representation": "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_MASKS__IMMUTABLE_STORAGE_INDEX_CACHE",
            "rows": sharp["rows"], "comparison": comparison, "terminal_shards": sharp["terminal_shards"],
            "cache_manifest_path": str(manifest_path), "cache_manifest_sha256": manifest_hash,
            "semantic_cache_authentication_checks": cache.semantic_checks,
            "prerequisite_hashes": prerequisite_hashes,
            "resource": {"peak_logical_state_plus_cache_bytes": peak_scratch,
                         "scratch_limit_bytes": common.SCRATCH_LIMIT,
                         "maximum_numerical_allocation_estimate_bytes": allocation,
                         "numerical_workspace_limit_bytes": common.NUMERICAL_WORKSPACE_LIMIT,
                         "authentication_peak_certificate_bytes": common.FROZEN_STORAGE["12"]["authentication_peak_bytes"],
                         "peak_rss_bytes": rss, "rss_limit_bytes": common.RSS_LIMIT,
                         "wall_seconds_including_authentication": wall,
                         "wall_limit_seconds": common.WALL_LIMIT, "passed": True},
            "implementation_sha256": common.sha256(Path(__file__)),
            "method_sha256": common.sha256(common.METHOD), "freeze_sha256": common.sha256(common.FREEZE),
            "claim_boundary": "INDEPENDENT_FINITE_CACHED_PREFIX_HISTORY_ONLY__NO_CONTINUUM_OR_GRAVITY",
        }
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    finally:
        cache.close()
        legacy.CACHE = None
        gc.collect()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("execute", choices=("execute",))
    parser.add_argument("--length", type=int, choices=common.SUPPORTED, required=True)
    args = parser.parse_args()
    try:
        execute(args.length)
    except (AssertionError, MemoryError, OSError, common.Refusal, TimeoutError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
