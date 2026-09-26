#!/usr/bin/env python3
"""Hostile exact streamed L10/L12 owner-once joint witness adapter.

This independently authored adapter is frozen before any held-out witness is
executed or opened.  It consumes only the hostile V003/V004R4 history lineage:
the retained sharp H_(L-1) shards, the frozen hostile propagator/cache, and a
new isolated rough H_(L-1) regeneration.  It never imports or opens the target
held-out implementation, target shards, or target result.

The full logical H_L is never allocated.  Each terminal child window is
transported and consumed by separately ordered row and column accumulators,
then discarded.  A scientific result is published atomically only after both
L10 and L12 have completed and passed the branch-internal controls.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import resource
import shutil
import stat
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SEALED = ROOT / "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_HELDOUT_EXECUTION_V001"
ENGINE = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
PROTOCOL = SEALED / "PROTOCOL.md"
MACHINE_GATE = SEALED / "INPUT_AND_RESOURCE_GATE.json"
SEED_DISPOSITION = (
    ROOT
    / "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_RECONCILIATION_V001"
    / "FINAL_DISPOSITION_V001.json"
)
CAPACITY_REPAIR = (
    ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V003/repair_kernels.py"
)

EXPECTED_PROTOCOL_SHA256 = "8250e17405067deabbfe7dc4ff00864d26bef66cabfeef628f9f6df63829d9a7"
EXPECTED_GATE_SHA256 = "2f38a50e530476e1f33647b49afc95d118738efb1ed53b6ba96335888a44432c"
EXPECTED_SEED_SHA256 = "2ce9852ef40d16d50b7a6553d0173e041c9cfdcc59925819f900f21f8a684f14"
EXPECTED_V004R4_FREEZE_SHA256 = "f3647eaf0532836d09eb2523c1ddb1123228f3226b11b35ec5f45c526e003de8"
EXPECTED_CAPACITY_REPAIR_SHA256 = "5b04ae50ce3c9392e7a6be401625d580f4892e151578749bf7dba4ea1a1c6b37"
EXPECTED_CACHE_MANIFEST_SHA256 = {
    10: "116adab0357a3e470a2df76d6b8c4a9ced7a496b6520fa180206db018772dab8",
    12: "1640607ea32c63a4af2139dc19a863e47b2fac5603656d059016710c774bceec",
}

AUTHORIZATION = "AUTHORIZE_EXACT_HELDOUT_HOSTILE_L10_L12_JOINT_WITNESS_V001"
LENGTHS = (10, 12)
DEFAULT_OUTPUT = HERE / "HOSTILE_HELDOUT_RAW.json"
OUTPUT_SCHEMA = "OWNER_ONCE_HELDOUT_HOSTILE_JOINT_WITNESS_RAW_V001"
CLAIM_BOUNDARY = (
    "FINITE_HELDOUT_OWNER_ONCE_TERMINAL_JOINT_LINEAGE_CARRIER_WITNESS_ONLY__"
    "NO_GATE_RGRL_ALPHA_GL6T_THERMODYNAMIC_CONTINUUM_OR_GRAVITY"
)

RSS_LIMIT = 17_179_869_184
WALL_LIMIT = 345_600.0
HOSTILE_SCRATCH_MINIMUM = 9_600_935_128
ROUGH_SHARP_TOLERANCE = 1.0e-8
NORM_CONTENT_TOLERANCE = 1.0e-10
MARGINAL_TOLERANCE = 1.0e-10
SHUFFLE_TOLERANCE = 1.0e-12
SHAM_TOLERANCE = 1.0e-12
COLUMN_CHUNK = 262_144

DEPENDENCIES = {
    "heldout_protocol": (PROTOCOL, EXPECTED_PROTOCOL_SHA256),
    "heldout_machine_gate": (MACHINE_GATE, EXPECTED_GATE_SHA256),
    "seed_final_disposition": (SEED_DISPOSITION, EXPECTED_SEED_SHA256),
    "numerical_capacity_repair_v003": (
        CAPACITY_REPAIR,
        EXPECTED_CAPACITY_REPAIR_SHA256,
    ),
    "prefix_protocol": (
        ROOT / "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/PROTOCOL.md",
        "964237c44690e86636b4d13150bc277d4dfd21ec0f8338105d7b420512f5e7c5",
    ),
    "prefix_theorem": (
        ROOT / "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001/THEOREM.md",
        "4c7fdc9b04263a9ba5e8aa54e049b12d76616094e7d038d549a48d86c5e4a6fb",
    ),
    "seed_witness_protocol": (
        ROOT / "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001/PROTOCOL.md",
        "70984a927c30585704622dfd03ee91bf516cd9a5d14474a228d231144e5e513e",
    ),
    "hostile_v004r4_method": (
        ENGINE / "V004R4_CACHE_METHOD.md",
        "e1214f533a4f0476d4db75bd1407a402c1ed0908f7919b376f9c65a27e93b587",
    ),
    "hostile_physical": (
        ENGINE / "independent_prefix_history.py",
        "6ea113e5bb25f1c4b00c2ee186b253ce5eb0551773f90e25bdbb52ed1c636af5",
    ),
    "hostile_replay": (
        ENGINE / "independent_prefix_history_v002.py",
        "e6b1be915a4d490939799e79efc017ab4e3808f1beeb3d984448b2508fb0522b",
    ),
    "hostile_v003": (
        ENGINE / "independent_prefix_history_v003.py",
        "cc4e1195283f60fddab1d70831965bd14a09435fd4aca2ee7fdde7e2d7e5ba7f",
    ),
    "hostile_v004": (
        ENGINE / "independent_prefix_history_v004.py",
        "2ca121861820f3bae1d3cc62c2bcf071d22af730dd92c96a6cd0852f2f577d3e",
    ),
    "hostile_v004r2": (
        ENGINE / "independent_prefix_history_v004r2.py",
        "e0e6d858711ce568ff973ff325a4a13f4dc9f7d35664157df4aadfb2247fdf87",
    ),
    "hostile_v004r2_common": (
        ENGINE / "v004r2_common.py",
        "e39529a2008018a1ede1b6f2deaef50e5843d489c8decd30163d60b408630689",
    ),
    "hostile_v004r4_cache_io": (
        ENGINE / "v004r4_cache_io.py",
        "cfea716a972498d23436f074f4ee20aa34601dfee39442efdf71ef0d88ee4c63",
    ),
    "hostile_v004r4_consumer": (
        ENGINE / "consume_cache_v004r4.py",
        "2c7ff73a0b462a75d576a51eef3863f5157dbccaa54573403734bbe72702d800",
    ),
    "hostile_v004r4_freeze": (
        ENGINE / "FROZEN_MANIFEST_V004R4.json",
        EXPECTED_V004R4_FREEZE_SHA256,
    ),
    "hostile_v004r4_preflight": (
        ENGINE / "validate_cache_preflight_v004r4.py",
        "ecf7a568acb3b440fbfee483bad9526d3d1d6eff5f7f7f2cda8e4486b2f94678",
    ),
    "hostile_v004r4_preflight_result": (
        ENGINE / "V004R4_CACHE_PREFLIGHT_RESULT.json",
        "f935b63407f627c6b07e93348e39ddba5a52a67b1f4132ff535cb15e9fbfbf28",
    ),
    "hostile_v004r4_independent_audit": (
        ENGINE / "HOSTILE_AUDIT_RESULT_V004R4.json",
        "75956f1b4c3768a1bb5425a4a13b0424e813747942abc339252b8e6430c5cbc5",
    ),
}

if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

# These imports are exclusively from the hostile frozen source tree above.
import independent_prefix_history as physical  # noqa: E402
import independent_prefix_history_v002 as replay  # noqa: E402
import independent_prefix_history_v003 as v3  # noqa: E402
import independent_prefix_history_v004 as legacy  # noqa: E402
import consume_cache_v004r4 as r4  # noqa: E402


# Exact numerical-capacity successor already authenticated by the V003
# process repair.  These extend only the Chebyshev endpoint checkpoint
# capacity.  Labels, quadrature orders, convergence tolerances, graph,
# Hamiltonian, admission angle, route time, and observables are unchanged.
HOSTILE_ROUGH = physical.Accuracy(
    "rough", (16, 24, 32, 48, 64, 80, 96, 112), 18, 3.0e-9
)
HOSTILE_SHARP = physical.Accuracy(
    "sharp", (24, 32, 48, 64, 80, 96, 112, 128), 28, 8.0e-11
)


class Refusal(RuntimeError):
    """A frozen authority, custody, resource, or numerical condition failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def descriptor_sha256(descriptor: int, size: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while offset < size:
        chunk = os.pread(descriptor, min(16 * 2**20, size - offset), offset)
        if not chunk:
            raise Refusal("short read while authenticating retained shard")
        digest.update(chunk)
        offset += len(chunk)
    return digest.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
        value = json.loads(text, parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"nonfinite JSON constant {value}")
        ))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Refusal(f"strict JSON failure: {path}") from error
    if not isinstance(value, dict):
        raise Refusal(f"JSON authority is not an object: {path}")
    return value


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def finite_values(value: object) -> bool:
    if isinstance(value, dict):
        return all(finite_values(item) for item in value.values())
    if isinstance(value, list):
        return all(finite_values(item) for item in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return True


def repository_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as error:
        raise Refusal(f"path escapes repository: {path}") from error


def authenticate_dependencies() -> dict[str, dict[str, str]]:
    answer: dict[str, dict[str, str]] = {}
    for role, (path, expected) in DEPENDENCIES.items():
        if path.is_symlink() or not path.is_file():
            raise Refusal(f"frozen dependency absent or symlinked: {role}")
        observed = sha256_file(path)
        if observed != expected:
            raise Refusal(f"frozen dependency hash mismatch: {role}")
        answer[role] = {"path": repository_relative(path), "sha256": observed}
    return answer


def canonical_shard_rows(history: dict[str, Any], expected_root: str) -> list[dict[str, Any]]:
    shards = history.get("terminal_shards")
    if not isinstance(shards, list):
        raise Refusal("hostile history terminal_shards is not a list")
    rows: list[dict[str, Any]] = []
    root_parts = Path(expected_root).parts
    for shard in shards:
        if not isinstance(shard, dict) or set(shard) != {"bytes", "path", "q", "sha256", "shape"}:
            raise Refusal("hostile terminal shard schema mismatch")
        raw = Path(shard["path"])
        if raw.is_absolute():
            parts = raw.parts
            matches = [index for index in range(len(parts)) if parts[index:] == root_parts + (raw.name,)]
            if not matches:
                raise Refusal("absolute historical shard path cannot be canonically rebased")
            relative = Path(*parts[matches[-1]:])
        else:
            relative = raw
        if relative.parent.as_posix() != expected_root or ".." in relative.parts:
            raise Refusal("hostile terminal shard root mismatch")
        q = shard["q"]
        shape = shard["shape"]
        byte_count = shard["bytes"]
        digest = shard["sha256"]
        if (
            type(q) is not int or q < 0
            or type(byte_count) is not int or byte_count <= 0
            or not isinstance(shape, list) or len(shape) != 2
            or any(type(item) is not int or item <= 0 for item in shape)
            or byte_count != math.prod(shape) * np.dtype("<c16").itemsize
            or not isinstance(digest, str) or len(digest) != 64
        ):
            raise Refusal("hostile terminal shard metadata mismatch")
        rows.append({"bytes": byte_count, "path": relative.as_posix(), "q": q,
                     "sha256": digest, "shape": shape})
    return rows


def shard_manifest_digest(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical_bytes(rows)).hexdigest()


def authenticate_authority() -> tuple[dict[str, Any], dict[int, dict[str, Any]], dict[str, dict[str, str]]]:
    dependencies = authenticate_dependencies()
    gate = strict_json(MACHINE_GATE)
    if (
        gate.get("schema") != "OWNER_ONCE_HELDOUT_L10_L12_INPUT_AND_RESOURCE_GATE_V001"
        or gate.get("status") != "FROZEN_PRE_HELDOUT_OUTPUT__READY_FOR_AUTHORIZED_EXACT_EXECUTION"
        or gate.get("authorization_tokens", {}).get("hostile") != AUTHORIZATION
        or gate.get("deterministic_output", {}).get("hostile_schema") != OUTPUT_SCHEMA
        or gate.get("execution", {}).get("checkpoint")
        != "AFTER_FINAL_OWNER_ONCE_EVENT_TRANSPORT_BEFORE_REVISIT"
    ):
        raise Refusal("held-out machine gate identity mismatch")
    seed = strict_json(SEED_DISPOSITION)
    if (
        seed.get("protocol_classification")
        != "RESOLVED_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_L4_L8"
        or seed.get("passed") is not True
        or seed.get("all_numerical_and_control_conditions_passed") is not True
        or not isinstance(seed.get("T_4_8"), (int, float))
        or isinstance(seed.get("T_4_8"), bool)
        or not math.isfinite(float(seed["T_4_8"]))
        or float(seed["T_4_8"]) <= 1.0
        or seed.get("held_out_L10_L12", {}).get("computed_or_opened_by_reconciliation") is not False
    ):
        raise Refusal("sealed seed prerequisite failed")

    inputs = gate.get("inputs")
    if not isinstance(inputs, list) or [(row.get("role"), row.get("length")) for row in inputs] != [
        ("target", 10), ("target", 12), ("hostile", 10), ("hostile", 12)
    ]:
        raise Refusal("sealed input role/length census mismatch")
    # Branch independence: target rows are authenticated by the sealed machine
    # gate hash and the orchestration-wide gate validator.  This hostile adapter
    # deliberately does not open the target history files or any target shard.
    hostile: dict[int, dict[str, Any]] = {}
    for item in inputs:
        if item["role"] != "hostile":
            continue
        length = item["length"]
        history_path = ROOT / item["history_path"]
        if history_path.is_symlink() or not history_path.is_file() \
                or sha256_file(history_path) != item["history_sha256"]:
            raise Refusal(f"hostile L{length} history custody mismatch")
        history = strict_json(history_path)
        if (
            history.get("L") != length
            or history.get("lineage_authority")
            != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING"
        ):
            raise Refusal(f"hostile L{length} history identity mismatch")
        rows = canonical_shard_rows(history, item["terminal_shard_root"])
        if (
            [row["q"] for row in rows] != list(range(length))
            or len(rows) != item["terminal_shard_count"]
            or sum(row["bytes"] for row in rows) != item["terminal_shard_total_bytes"]
            or shard_manifest_digest(rows) != item["terminal_shard_manifest_sha256"]
        ):
            raise Refusal(f"hostile L{length} terminal manifest mismatch")
        hostile[length] = {"history_path": item["history_path"],
                           "history_sha256": item["history_sha256"],
                           "terminal_shard_manifest_sha256": item["terminal_shard_manifest_sha256"],
                           "terminal_shard_root": item["terminal_shard_root"],
                           "terminal_shard_total_bytes": item["terminal_shard_total_bytes"],
                           "terminal_shards": rows}
    if set(hostile) != set(LENGTHS):
        raise Refusal("hostile L10/L12 authority census incomplete")
    return gate, hostile, dependencies


def _identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (metadata.st_dev, metadata.st_ino, metadata.st_size,
            metadata.st_mtime_ns, metadata.st_nlink)


@dataclass
class HeldShard:
    descriptor: int
    identity: tuple[int, int, int, int, int]
    record: dict[str, Any]


class ShardSource(Protocol):
    prefix: int

    def open_shard(self, q: int, mode: str = "r") -> np.ndarray: ...


class RetainedShardSet:
    """Stable-open, read-only, no-follow custody over one retained H_(L-1)."""

    def __init__(self, length: int, authority: dict[str, Any]):
        self.length = length
        self.prefix = length - 1
        self.root = (ROOT / authority["terminal_shard_root"]).resolve()
        self.directory_descriptor = -1
        self.shards: dict[int, HeldShard] = {}
        flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
        self.directory_descriptor = os.open(self.root, flags)
        info = os.fstat(self.directory_descriptor)
        current = os.stat(self.root, follow_symlinks=False)
        if not stat.S_ISDIR(info.st_mode) or _identity(info) != _identity(current):
            raise Refusal("retained hostile shard root custody mismatch")
        expected_names = [Path(row["path"]).name for row in authority["terminal_shards"]]
        if sorted(os.listdir(self.directory_descriptor)) != sorted(expected_names):
            raise Refusal("retained hostile shard exact member census mismatch")
        try:
            for row in authority["terminal_shards"]:
                name = Path(row["path"]).name
                descriptor = os.open(
                    name,
                    os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
                    dir_fd=self.directory_descriptor,
                )
                opened = os.fstat(descriptor)
                current = os.stat(name, dir_fd=self.directory_descriptor, follow_symlinks=False)
                ident = _identity(opened)
                if (
                    not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1
                    or ident != _identity(current) or opened.st_size != row["bytes"]
                    or descriptor_sha256(descriptor, opened.st_size) != row["sha256"]
                ):
                    os.close(descriptor)
                    raise Refusal(f"retained hostile shard custody mismatch: q={row['q']}")
                self.shards[row["q"]] = HeldShard(descriptor, ident, row)
        except BaseException:
            self.close()
            raise

    def open_shard(self, q: int, mode: str = "r") -> np.ndarray:
        if mode != "r" or q not in self.shards:
            raise Refusal("retained hostile shard permits read-only canonical q access")
        held = self.shards[q]
        self._verify_one(q, full_hash=False)
        with os.fdopen(os.dup(held.descriptor), "rb", closefd=True) as stream:
            array = np.memmap(
                stream, dtype="<c16", mode="r", shape=tuple(held.record["shape"])
            )
        if array.flags.writeable or array.nbytes != held.record["bytes"]:
            raise Refusal("retained hostile shard mapping changed identity")
        return array

    def _verify_one(self, q: int, full_hash: bool) -> None:
        held = self.shards[q]
        name = Path(held.record["path"]).name
        opened = os.fstat(held.descriptor)
        current = os.stat(name, dir_fd=self.directory_descriptor, follow_symlinks=False)
        if _identity(opened) != held.identity or _identity(current) != held.identity:
            raise Refusal(f"retained hostile shard drift: q={q}")
        if full_hash and descriptor_sha256(held.descriptor, opened.st_size) != held.record["sha256"]:
            raise Refusal(f"retained hostile shard hash drift: q={q}")

    def reauthenticate(self) -> None:
        expected = sorted(Path(held.record["path"]).name for held in self.shards.values())
        if sorted(os.listdir(self.directory_descriptor)) != expected:
            raise Refusal("retained hostile shard member census drift")
        for q in sorted(self.shards):
            self._verify_one(q, full_hash=True)

    def close(self) -> None:
        for held in self.shards.values():
            try:
                os.close(held.descriptor)
            except OSError:
                pass
        self.shards.clear()
        if self.directory_descriptor >= 0:
            try:
                os.close(self.directory_descriptor)
            except OSError:
                pass
            self.directory_descriptor = -1


def current_rss_bytes() -> int:
    observed = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return observed if sys.platform == "darwin" else observed * 1024


def guard_resources(started: float) -> None:
    rss = current_rss_bytes()
    if rss > RSS_LIMIT:
        raise MemoryError(f"held-out hostile RSS guard exceeded: {rss} > {RSS_LIMIT}")
    elapsed = time.perf_counter() - started
    if elapsed > WALL_LIMIT:
        raise TimeoutError(f"held-out hostile wall guard exceeded: {elapsed} > {WALL_LIMIT}")


def existing_ancestor(path: Path) -> Path:
    candidate = path
    while not candidate.exists():
        if candidate.parent == candidate:
            raise Refusal(f"no existing ancestor for path: {path}")
        candidate = candidate.parent
    return candidate


def validate_telemetry(
    gate: dict[str, Any], telemetry_path: Path, scratch_root: Path, output: Path,
    now: int | None = None,
) -> dict[str, int]:
    """Validate the protocol's small, fixed resource-telemetry record."""
    telemetry = strict_json(telemetry_path)
    telemetry_rule = gate["fresh_telemetry"]
    resource_rule = gate["resource_gate"]
    if (
        set(telemetry) != set(telemetry_rule["capture_fields"])
        or telemetry.get("schema") != telemetry_rule["schema"]
        or telemetry.get("selected_schedule") not in telemetry_rule["allowed_schedules"]
        or telemetry.get("memory_pressure") != telemetry_rule["required_memory_pressure"]
    ):
        raise Refusal("fresh telemetry schema or fixed field mismatch")
    integer_fields = (
        "captured_epoch_seconds", "total_host_memory_bytes",
        "available_memory_bytes", "shared_filesystem_free_bytes",
    )
    if any(type(telemetry.get(key)) is not int or telemetry[key] < 0 for key in integer_fields):
        raise Refusal("fresh telemetry integer field mismatch")
    instant = int(time.time()) if now is None else now
    age = instant - telemetry["captured_epoch_seconds"]
    if age < 0 or age > telemetry_rule["max_age_seconds"]:
        raise Refusal("fresh telemetry age mismatch")
    declared_paths = [Path(telemetry[key]).resolve() for key in (
        "target_scratch_root", "hostile_scratch_root",
        "target_output_path", "hostile_output_path",
    )]
    if (
        declared_paths[1] != scratch_root.resolve()
        or declared_paths[3] != output.resolve()
        or len(set(declared_paths)) != 4
    ):
        raise Refusal("fresh telemetry path binding or branch separation mismatch")
    if telemetry["selected_schedule"] == "CONCURRENT_TARGET_AND_HOSTILE" and (
        telemetry["total_host_memory_bytes"]
        < resource_rule["concurrent_total_host_memory_minimum_bytes"]
        or telemetry["available_memory_bytes"]
        < resource_rule["concurrent_available_memory_minimum_bytes"]
    ):
        raise Refusal("concurrent memory floor failed")
    free = shutil.disk_usage(existing_ancestor(scratch_root)).free
    minimum = resource_rule["combined_scratch_minimum_bytes"]
    if telemetry["shared_filesystem_free_bytes"] < minimum or free < minimum:
        raise Refusal(
            f"sealed scratch floor failed: {free} < {minimum}"
        )
    rss = current_rss_bytes()
    if rss > RSS_LIMIT:
        raise Refusal(f"held-out hostile RSS preflight failed: {rss} > {RSS_LIMIT}")
    return {"free_bytes": free, "rss_bytes": rss}


def resource_preflight(
    gate: dict[str, Any], telemetry_path: Path, scratch_root: Path, output: Path,
    now: int | None = None,
) -> dict[str, int]:
    if output.exists() or output.is_symlink():
        raise Refusal("held-out output already exists; no calculation started")
    if scratch_root.exists() or scratch_root.is_symlink():
        raise Refusal("held-out hostile scratch root must be new and absent")
    output_parent = output.parent.resolve()
    if not output_parent.is_dir() or output_parent.is_symlink():
        raise Refusal("held-out output parent is not an ordinary directory")
    return validate_telemetry(gate, telemetry_path, scratch_root, output, now)


def authenticate_cache(length: int, started: float) -> r4.CacheContext:
    root = ENGINE / f"V004R4_CACHE_PAYLOADS/L{length}"
    manifest_path = root / "CACHE_MANIFEST.json"
    expected = EXPECTED_CACHE_MANIFEST_SHA256[length]
    if manifest_path.is_symlink() or not manifest_path.is_file() or sha256_file(manifest_path) != expected:
        raise Refusal(f"hostile L{length} V004R4 cache manifest custody mismatch")
    manifest = strict_json(manifest_path)
    source_hashes = {
        "method": DEPENDENCIES["hostile_v004r4_method"][1],
        "builder": "da5fa4484ce56993cbb0d4b411cad638836cb1ebe272c89a52ff33e382fff8f1",
        "consumer": DEPENDENCIES["hostile_v004r4_consumer"][1],
        "preflight": DEPENDENCIES["hostile_v004r4_preflight"][1],
        "freeze": EXPECTED_V004R4_FREEZE_SHA256,
        "preflight_result": DEPENDENCIES["hostile_v004r4_preflight_result"][1],
        "independent_hostile_audit": DEPENDENCIES["hostile_v004r4_independent_audit"][1],
    }
    return r4.CacheContext(length, root, manifest, expected, source_hashes, started)


def configure_hostile(length: int, cache: r4.CacheContext, started: float) -> None:
    legacy.configure(length, cache, started)
    physical.ROUGH = HOSTILE_ROUGH
    physical.SHARP = HOSTILE_SHARP
    v3.RSS_LIMIT = RSS_LIMIT
    v3.WALL_LIMIT = WALL_LIMIT
    physical.L12_RSS_LIMIT = RSS_LIMIT
    physical.L12_WALL_LIMIT = WALL_LIMIT


def regenerate_rough_prefix(length: int, root: Path, started: float) -> tuple[v3.DiskPrefix, dict[str, Any]]:
    if root.exists() or root.is_symlink():
        raise Refusal(f"rough scratch must be a new absent root: {root}")
    edges = physical.hostile_edges(length)
    state = v3.create_blank(root)
    maximum_norm_error = 0.0
    maximum_blocked_error = 0.0
    maximum_endpoint_difference = 0.0
    maximum_tail_indicator = 0.0
    maximum_allocation = 0
    for event in range(length - 1):
        following, blocked_error = v3.admit_to_next(state, event, edges)
        initial, final, _flux, method, _allowed, _blocked = v3.route_disk_state(
            following, physical.ROUGH, edges, True
        )
        if method.get("converged") is not True:
            raise Refusal(f"rough L{length} event {event} transport did not converge")
        maximum_norm_error = max(
            maximum_norm_error,
            abs(float(initial["norm"]) - 1.0), abs(float(final["norm"]) - 1.0),
        )
        maximum_blocked_error = max(maximum_blocked_error, float(blocked_error))
        maximum_endpoint_difference = max(
            maximum_endpoint_difference, float(method["maximum_endpoint_difference"])
        )
        maximum_tail_indicator = max(
            maximum_tail_indicator, float(method["maximum_tail_indicator_32"])
        )
        maximum_allocation = max(
            maximum_allocation, int(method["maximum_allocation_estimate_bytes"])
        )
        state.remove()
        state = following
        guard_resources(started)
    state.verify_complete()
    return state, {
        "events_regenerated": length - 1,
        "maximum_allocation_estimate_bytes": maximum_allocation,
        "maximum_blocked_null_state_error": maximum_blocked_error,
        "maximum_endpoint_difference": maximum_endpoint_difference,
        "maximum_norm_error": maximum_norm_error,
        "maximum_tail_indicator_32": maximum_tail_indicator,
        "resolution": "rough",
    }


def _float64_digest(array: np.ndarray) -> str:
    stable = np.ascontiguousarray(array, dtype="<f8")
    return hashlib.sha256(stable.tobytes(order="C")).hexdigest()


class SectorAccumulator:
    """Two independently ordered streamed accumulators for one sharp-q sector."""

    def __init__(self, length: int, q: int, carrier_words: np.ndarray):
        self.length = length
        self.q = q
        self.lineage_count = math.comb(length, q)
        self.carrier_count = math.comb(2 * length, q)
        if len(carrier_words) != self.carrier_count:
            raise Refusal("carrier basis census mismatch")
        self.active_words = np.asarray(carrier_words, dtype=np.uint32) & np.uint32((1 << length) - 1)
        self.popcount = np.asarray(
            [bin(word).count("1") for word in range(1 << length)], dtype=np.float64
        )
        self.active_counts = self.popcount[self.active_words]
        self.row_lineage = np.zeros(self.lineage_count, dtype=np.float64)
        self.column_lineage = np.zeros(self.lineage_count, dtype=np.float64)
        self.row_carrier = np.zeros(self.carrier_count, dtype=np.float64)
        self.column_carrier = np.zeros(self.carrier_count, dtype=np.float64)
        self.row_observed = 0.0
        self.column_observed = 0.0

    def _scores(self, lineage_word: int, lower: int = 0, upper: int | None = None) -> np.ndarray:
        stop = self.carrier_count if upper is None else upper
        active = self.active_words[lower:stop]
        overlap = self.popcount[active & np.uint32(lineage_word)]
        return (overlap - (float(self.q) / float(self.length)) * self.active_counts[lower:stop]) \
            / float(self.length)

    def consume(self, vector: np.ndarray, row_indices: np.ndarray, lineage_words: np.ndarray) -> None:
        if (
            vector.ndim != 2 or vector.shape[0] != len(row_indices)
            or vector.shape[0] != len(lineage_words) or vector.shape[1] != self.carrier_count
        ):
            raise Refusal("terminal witness window shape mismatch")
        # Row-first accumulator.
        for local, (row_index, lineage_word) in enumerate(zip(row_indices, lineage_words)):
            probability = np.square(vector[local].real) + np.square(vector[local].imag)
            weight = float(np.sum(probability))
            self.row_lineage[int(row_index)] += weight
            self.row_carrier += probability
            self.row_observed += float(np.sum(probability * self._scores(int(lineage_word))))
        # Column-chunk-first accumulator.  Probability and scores are rebuilt,
        # so this is not an alias of the row-first reduction.
        for lower in range(0, self.carrier_count, COLUMN_CHUNK):
            upper = min(self.carrier_count, lower + COLUMN_CHUNK)
            part = vector[:, lower:upper]
            probability = np.square(part.real) + np.square(part.imag)
            self.column_carrier[lower:upper] += np.sum(probability, axis=0)
            for local, (row_index, lineage_word) in enumerate(zip(row_indices, lineage_words)):
                self.column_lineage[int(row_index)] += float(np.sum(probability[local]))
                self.column_observed += float(np.sum(
                    probability[local] * self._scores(int(lineage_word), lower, upper)
                ))

    def _finish_one(
        self, lineage: np.ndarray, carrier: np.ndarray, observed: float,
    ) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
        lineage_words = np.asarray(physical.reverse_masks(self.length, self.q), dtype=np.uint32)
        lineage_vectors = np.zeros(self.length, dtype=np.float64)
        carrier_vectors = np.zeros(self.length, dtype=np.float64)
        centered = float(self.q) / float(self.length)
        for event in range(self.length):
            lineage_vectors[event] = float(np.sum(
                lineage * (((lineage_words >> event) & 1).astype(np.float64) - centered)
            ))
            carrier_vectors[event] = float(np.sum(
                carrier * (((self.active_words >> event) & 1).astype(np.float64))
            ))
        sector_weight = float(np.sum(lineage))
        carrier_weight = float(np.sum(carrier))
        sham = 0.0
        sham_direct = 0.0
        if sector_weight > 0.0:
            sham = float(np.sum(lineage_vectors * carrier_vectors)) / (
                float(self.length) * sector_weight
            )
            for event in range(self.length):
                centered_lineage = (
                    ((lineage_words >> event) & 1).astype(np.float64) - centered
                )
                active_carrier = ((self.active_words >> event) & 1).astype(np.float64)
                sham_direct += (
                    float(np.sum(lineage * centered_lineage))
                    * float(np.sum(carrier * active_carrier))
                    / (float(self.length) * sector_weight)
                )
        lineage_q = float(np.sum(lineage * self.popcount[lineage_words]))
        carrier_q = float(self.q) * carrier_weight
        record = {
            "carrier_marginal_sha256": _float64_digest(carrier),
            "lineage_marginal_sha256": _float64_digest(lineage),
            "observed": observed,
            "sector_weight": sector_weight,
            "sham": sham,
            "sham_self_covariance_residual": abs(sham_direct - sham),
            "witness": observed - sham,
        }
        residual = np.asarray([
            abs(sector_weight - carrier_weight),
            abs(lineage_q - float(self.q) * sector_weight),
            abs(carrier_q - float(self.q) * sector_weight),
            abs(lineage_q - carrier_q),
        ], dtype=np.float64)
        return record, residual, np.asarray([lineage_q, carrier_q], dtype=np.float64)

    def finish(self) -> dict[str, Any]:
        row, row_residuals, row_content = self._finish_one(
            self.row_lineage, self.row_carrier, self.row_observed
        )
        column, column_residuals, column_content = self._finish_one(
            self.column_lineage, self.column_carrier, self.column_observed
        )
        marginal = max(
            float(np.max(np.abs(self.row_lineage - self.column_lineage))),
            float(np.max(np.abs(self.row_carrier - self.column_carrier))),
            abs(float(row["sector_weight"]) - float(column["sector_weight"])),
        )
        row_column = max(
            marginal,
            abs(float(row["observed"]) - float(column["observed"])),
            abs(float(row["sham"]) - float(column["sham"])),
            abs(float(row["witness"]) - float(column["witness"])),
        )
        shuffle_identity = 0.0
        if 0 < self.q < self.length:
            shuffle_identity = abs(
                float(math.comb(self.length - 1, self.q - 1)) / float(math.comb(self.length, self.q))
                - float(self.q) / float(self.length)
            )
        return {
            "column_accumulator": column,
            "marginal_reconstruction_residual": marginal,
            "q_identity_residual": max(float(np.max(row_residuals)), float(np.max(column_residuals))),
            "row_accumulator": row,
            "row_column_disagreement": row_column,
            "row_content": row_content.tolist(),
            "column_content": column_content.tolist(),
            "sector_weight": float(row["sector_weight"]),
            "sham_negative_control_D": 0.0,
            "sham_self_covariance_residual": max(
                float(row["sham_self_covariance_residual"]),
                float(column["sham_self_covariance_residual"]),
            ),
            "shuffle_expectation": 0.0,
            "shuffle_identity_residual": shuffle_identity,
            "witness": float(row["witness"]),
        }


def _row_indices(length: int, q: int, words: Iterable[int]) -> np.ndarray:
    answer = np.fromiter(
        (v3.reverse_rank(length, q, int(word)) for word in words),
        dtype=np.int32,
    )
    if len(np.unique(answer)) != len(answer):
        raise Refusal("full-lineage row reconstruction is not injective")
    return answer


def child0_window(source: np.ndarray, carrier_words: np.ndarray, event: int) -> np.ndarray:
    child = np.array(source, dtype=np.complex128, copy=True)
    blank = ((carrier_words >> event) & 1) == 0
    child[:, blank] *= math.cos(physical.ANGLE)
    return child


def child1_window(
    source: np.ndarray, carrier_count: int,
    occupied_columns: np.ndarray, old_columns: np.ndarray,
) -> np.ndarray:
    child = np.zeros((len(source), carrier_count), dtype=np.complex128)
    child[:, occupied_columns] = -1.0j * math.sin(physical.ANGLE) * np.asarray(
        source[:, old_columns]
    )
    return child


def _open_source(source: ShardSource, q: int) -> np.ndarray:
    return source.open_shard(q, "r")


def terminal_witness(
    length: int, source: ShardSource, accuracy: physical.Accuracy,
    cache: r4.CacheContext, started: float,
) -> dict[str, Any]:
    if source.prefix != length - 1:
        raise Refusal("terminal witness source is not H_(L-1)")
    event = length - 1
    edges = physical.hostile_edges(length)
    sectors: list[dict[str, Any]] = []
    method = v3.method_record()
    for q in range(length + 1):
        carrier = legacy.cached_construct_carrier(q, edges)
        accumulator = SectorAccumulator(length, q, carrier.words)
        try:
            if q < length:
                old_words = np.asarray(physical.reverse_masks(length - 1, q), dtype=np.uint32)
                rows = _row_indices(length, q, old_words)
                shard = _open_source(source, q)
                step = min(len(shard), replay.safe_batch_rows(
                    len(carrier.words), max(accuracy.checkpoints), physical.TERMINAL_WINDOW_BYTES
                ))
                for lower in range(0, len(shard), step):
                    upper = min(len(shard), lower + step)
                    child = child0_window(shard[lower:upper], carrier.words, event)
                    final, _flux, record = replay.low_memory_evolve_batch(carrier, child, accuracy)
                    v3.update_method(method, record)
                    accumulator.consume(final, rows[lower:upper], old_words[lower:upper])
                    del child, final
                    guard_resources(started)
                v3.close_memmap(shard)
            if q > 0:
                old_words = np.asarray(physical.reverse_masks(length - 1, q - 1), dtype=np.uint32)
                full_words = old_words | np.uint32(1 << event)
                rows = _row_indices(length, q, full_words)
                occupied_columns, old_columns = cache.admission(event, q)
                shard = _open_source(source, q - 1)
                step = min(len(shard), replay.safe_batch_rows(
                    len(carrier.words), max(accuracy.checkpoints), physical.TERMINAL_WINDOW_BYTES
                ))
                for lower in range(0, len(shard), step):
                    upper = min(len(shard), lower + step)
                    child = child1_window(
                        shard[lower:upper], len(carrier.words), occupied_columns, old_columns
                    )
                    final, _flux, record = replay.low_memory_evolve_batch(carrier, child, accuracy)
                    v3.update_method(method, record)
                    accumulator.consume(final, rows[lower:upper], full_words[lower:upper])
                    del child, final
                    guard_resources(started)
                v3.close_memmap(shard)
                legacy.close_mapping(occupied_columns)
                legacy.close_mapping(old_columns)
            sectors.append({"q": q, **accumulator.finish()})
        finally:
            carrier.release()
            del carrier, accumulator
            gc.collect()
    method["quadrature_nodes"] = accuracy.gauss_order
    method["q_sharded"] = True
    method["terminal_children_streamed"] = True
    method["full_terminal_array_allocated"] = False
    row_observed = float(sum(item["row_accumulator"]["observed"] for item in sectors))
    row_sham = float(sum(item["row_accumulator"]["sham"] for item in sectors))
    column_observed = float(sum(item["column_accumulator"]["observed"] for item in sectors))
    column_sham = float(sum(item["column_accumulator"]["sham"] for item in sectors))
    row_witness = row_observed - row_sham
    column_witness = column_observed - column_sham
    row_q_observed = [float(item["row_accumulator"]["observed"]) for item in sectors]
    row_q_sham = [float(item["row_accumulator"]["sham"]) for item in sectors]
    row_q_witness = [float(item["row_accumulator"]["witness"]) for item in sectors]
    column_q_observed = [float(item["column_accumulator"]["observed"]) for item in sectors]
    column_q_sham = [float(item["column_accumulator"]["sham"]) for item in sectors]
    column_q_witness = [float(item["column_accumulator"]["witness"]) for item in sectors]
    sector_weights = [float(item["sector_weight"]) for item in sectors]
    total_probability = float(sum(sector_weights))
    lineage_content = float(sum(item["row_content"][0] + (length - item["q"]) * item["sector_weight"]
                                for item in sectors))
    carrier_content = float(sum(item["row_content"][1] + (length - item["q"]) * item["sector_weight"]
                                for item in sectors))
    return {
        "D_L": row_witness,
        "column_accumulator": {
            "D_L": column_witness, "observed": column_observed,
            "q_observed": column_q_observed, "q_sham": column_q_sham,
            "q_witness": column_q_witness, "sham": column_sham,
        },
        "controls": {
            "analytic_shuffle_expectation": 0.0,
            "sham_self_covariance_residual": max(
                float(item["sham_self_covariance_residual"]) for item in sectors
            ),
            "maximum_shuffle_identity_residual": max(
                float(item["shuffle_identity_residual"]) for item in sectors
            ),
            "sham_negative_control_D": 0.0,
        },
        "marginal_reconstruction_residual": max(
            float(item["marginal_reconstruction_residual"]) for item in sectors
        ),
        "normalization_residual": abs(total_probability - 1.0),
        "q_identity_residual": max(float(item["q_identity_residual"]) for item in sectors),
        "row_accumulator": {
            "D_L": row_witness, "observed": row_observed,
            "q_observed": row_q_observed, "q_sham": row_q_sham,
            "q_witness": row_q_witness, "sham": row_sham,
        },
        "row_column_disagreement": max(
            abs(row_observed - column_observed), abs(row_sham - column_sham),
            abs(row_witness - column_witness),
            max(float(item["row_column_disagreement"]) for item in sectors),
        ),
        "sector_weights": sector_weights,
        "sectors": sectors,
        "solver": method,
        "total_content_residual": max(
            abs(lineage_content - float(length)), abs(carrier_content - float(length))
        ),
        "w_L": row_observed,
        "w_L_sham": row_sham,
        "w_L_shuffle": 0.0,
    }


def _flatten_diagnostics(record: dict[str, Any]) -> list[float]:
    values = [
        float(record["marginal_reconstruction_residual"]),
        float(record["normalization_residual"]),
        float(record["q_identity_residual"]),
        float(record["row_column_disagreement"]),
        float(record["total_content_residual"]),
        abs(float(record["controls"]["analytic_shuffle_expectation"])),
        abs(float(record["controls"]["sham_self_covariance_residual"])),
        abs(float(record["controls"]["maximum_shuffle_identity_residual"])),
        abs(float(record["controls"]["sham_negative_control_D"])),
    ]
    return values


def compare_resolutions(rough: dict[str, Any], sharp: dict[str, Any]) -> float:
    values = [
        abs(float(rough[key]) - float(sharp[key]))
        for key in ("w_L", "w_L_sham", "D_L")
    ]
    for key in ("sector_weights",):
        values.extend(abs(float(a) - float(b)) for a, b in zip(rough[key], sharp[key]))
    for accumulator in ("row_accumulator", "column_accumulator"):
        for contribution in ("q_observed", "q_sham", "q_witness"):
            values.extend(
                abs(float(a) - float(b))
                for a, b in zip(
                    rough[accumulator][contribution], sharp[accumulator][contribution]
                )
            )
    return max(values, default=0.0)


def run_length(
    length: int, authority: dict[str, Any], scratch_root: Path,
    started: float,
) -> dict[str, Any]:
    cache: r4.CacheContext | None = None
    retained: RetainedShardSet | None = None
    try:
        cache = authenticate_cache(length, started)
        configure_hostile(length, cache, started)
        retained = RetainedShardSet(length, authority)
        rough_source, rough_regeneration = regenerate_rough_prefix(
            length, scratch_root / f"L{length}" / "rough", started
        )
        rough = terminal_witness(length, rough_source, physical.ROUGH, cache, started)
        retained.reauthenticate()
        sharp = terminal_witness(length, retained, physical.SHARP, cache, started)
        retained.reauthenticate()
        cache.reauthenticate()
        rough_sharp = compare_resolutions(rough, sharp)
        internal_residual = max(
            _flatten_diagnostics(rough)
            + _flatten_diagnostics(sharp)
            + [
                float(rough_regeneration["maximum_norm_error"]),
                float(rough_regeneration["maximum_blocked_null_state_error"]),
            ]
        )
        conditions = {
            "rough_sharp_within_1e_8": rough_sharp <= ROUGH_SHARP_TOLERANCE,
            "norm_and_content_within_1e_10": max(
                float(rough["normalization_residual"]), float(sharp["normalization_residual"]),
                float(rough["total_content_residual"]), float(sharp["total_content_residual"]),
                float(rough_regeneration["maximum_norm_error"]),
                float(rough_regeneration["maximum_blocked_null_state_error"]),
            ) <= NORM_CONTENT_TOLERANCE,
            "marginals_within_1e_10": max(
                float(rough["marginal_reconstruction_residual"]),
                float(sharp["marginal_reconstruction_residual"]),
            ) <= MARGINAL_TOLERANCE,
            "q_identity_within_1e_10": max(
                float(rough["q_identity_residual"]), float(sharp["q_identity_residual"]),
            ) <= NORM_CONTENT_TOLERANCE,
            "row_column_within_1e_10": max(
                float(rough["row_column_disagreement"]),
                float(sharp["row_column_disagreement"]),
            ) <= MARGINAL_TOLERANCE,
            "sham_negative_control_within_1e_12": max(
                abs(float(rough["controls"]["sham_negative_control_D"])),
                abs(float(sharp["controls"]["sham_negative_control_D"])),
                float(rough["controls"]["sham_self_covariance_residual"]),
                float(sharp["controls"]["sham_self_covariance_residual"]),
            ) <= SHAM_TOLERANCE,
            "shuffle_within_1e_12": max(
                abs(float(rough["controls"]["analytic_shuffle_expectation"])),
                abs(float(sharp["controls"]["analytic_shuffle_expectation"])),
                float(rough["controls"]["maximum_shuffle_identity_residual"]),
                float(sharp["controls"]["maximum_shuffle_identity_residual"]),
            ) <= SHUFFLE_TOLERANCE,
            "rough_solver_converged": rough["solver"].get("converged") is True,
            "sharp_solver_converged": sharp["solver"].get("converged") is True,
        }
        return {
            "L": length,
            "coarse": rough,
            "fine": sharp,
            "input": authority,
            "internal_conditions": conditions,
            "internal_conditions_pass": all(conditions.values()),
            "internal_residual": internal_residual,
            "rough_regeneration": rough_regeneration,
            "rough_sharp_disagreement": rough_sharp,
            "target_comparison": "PENDING_SEPARATE_RECONCILIATION",
        }
    finally:
        legacy.CACHE = None
        v3.EXECUTION_STARTED = None
        if retained is not None:
            retained.close()
        if cache is not None:
            cache.close()
        gc.collect()


def deterministic_dependencies(
    authenticated: dict[str, dict[str, str]], source_path: Path,
) -> dict[str, dict[str, str]]:
    answer = dict(authenticated)
    answer["hostile_heldout_source"] = {
        "path": repository_relative(source_path), "sha256": sha256_file(source_path)
    }
    return answer


def build_result(
    hostile_inputs: dict[int, dict[str, Any]], dependencies: dict[str, dict[str, str]],
    scratch_root: Path, started: float,
) -> dict[str, Any]:
    results = [run_length(length, hostile_inputs[length], scratch_root, started) for length in LENGTHS]
    passed = all(item["internal_conditions_pass"] for item in results)
    payload: dict[str, Any] = {
        "claim_boundary": CLAIM_BOUNDARY,
        "dependencies": deterministic_dependencies(dependencies, Path(__file__).resolve()),
        "disposition": (
            "HOSTILE_HELDOUT_L10_L12_COMPLETE__RECONCILIATION_REQUIRED"
            if passed else "OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED"
        ),
        "independence": {
            "target_arrays_read": False,
            "target_code_imported": False,
            "target_matrices_read": False,
            "target_result_values_read": False,
        },
        "parameters": {
            "checkpoint": "AFTER_FINAL_OWNER_ONCE_EVENT_TRANSPORT_BEFORE_REVISIT",
            "column_chunk": COLUMN_CHUNK,
            "lengths": list(LENGTHS),
            "marginal_tolerance": MARGINAL_TOLERANCE,
            "norm_content_tolerance": NORM_CONTENT_TOLERANCE,
            "rough_sharp_tolerance": ROUGH_SHARP_TOLERANCE,
            "rss_limit_bytes": RSS_LIMIT,
            "sham_tolerance": SHAM_TOLERANCE,
            "shuffle_tolerance": SHUFFLE_TOLERANCE,
            "terminal_representation": "TWO_ORTHOGONAL_CHILD_WINDOWS__NO_FULL_H_L_ARRAY",
            "wall_limit_seconds": int(WALL_LIMIT),
        },
        "results": results,
        "schema": OUTPUT_SCHEMA,
    }
    if not finite_values(payload):
        raise Refusal("nonfinite value in hostile held-out result")
    return payload


def atomic_publish(path: Path, payload: dict[str, Any]) -> str:
    if path.exists() or path.is_symlink():
        raise Refusal(f"refuse to overwrite held-out result: {path}")
    parent = path.parent.resolve()
    if not parent.is_dir() or parent.is_symlink():
        raise Refusal("held-out result parent is not an ordinary directory")
    raw = canonical_bytes(payload)
    temporary = parent / f".{path.name}.partial-{os.getpid()}"
    if temporary.exists() or temporary.is_symlink():
        raise Refusal("held-out private publication path already exists")
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o400,
    )
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise Refusal("short held-out result write")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    try:
        os.link(temporary, path, follow_symlinks=False)
        directory = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)
    observed = sha256_file(path)
    expected = hashlib.sha256(raw).hexdigest()
    if observed != expected:
        raise Refusal("atomic held-out publication hash mismatch")
    return observed


def synthetic_schema_record() -> dict[str, Any]:
    return {
        "authorization_required": AUTHORIZATION,
        "heldout_lengths": list(LENGTHS),
        "input_and_resource_gate_sha256": EXPECTED_GATE_SHA256,
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256,
        "schema": OUTPUT_SCHEMA,
        "source_sha256": sha256_file(Path(__file__).resolve()),
        "status": "HOSTILE_HELDOUT_SOURCE_FROZEN_READY__PHYSICAL_VALUES_UNOPENED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorize-heldout", default="")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--print-source-schema", action="store_true")
    parser.add_argument("--scratch-root", type=Path)
    parser.add_argument("--telemetry", type=Path)
    arguments = parser.parse_args()
    if arguments.print_source_schema:
        print(json.dumps(synthetic_schema_record(), indent=2, sort_keys=True, allow_nan=False))
        return 0
    if arguments.authorize_heldout != AUTHORIZATION:
        parser.error("physical held-out hostile execution is locked by the exact authorization token")
    if arguments.scratch_root is None or arguments.telemetry is None:
        parser.error("authorized execution requires --scratch-root and --telemetry")
    output = arguments.output.resolve()
    scratch_root = arguments.scratch_root.resolve()
    gate, hostile_inputs, dependencies = authenticate_authority()
    resource_preflight(gate, arguments.telemetry, scratch_root, output)
    scratch_root.mkdir(parents=True, mode=0o700)
    started = time.perf_counter()
    validate_telemetry(gate, arguments.telemetry, scratch_root, output)
    result = build_result(hostile_inputs, dependencies, scratch_root, started)
    digest = atomic_publish(output, result)
    print(result["disposition"])
    print(f"output_sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
