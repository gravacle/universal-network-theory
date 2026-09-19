#!/usr/bin/env python3
"""Authenticated parent for one process-parallel L12 numerical branch.

The executable authenticates the frozen storage cache in the parent, runs the
rough and sharp histories through the successor process pool, reauthenticates
the cache, seals terminal shards, and exclusively publishes a successor
history.  It never overwrites the timed-out workspace or an existing result.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import resource
import stat
import sys
import time
from pathlib import Path
from typing import Any

from execution_integration import (
    run_hostile_rough_and_sharp,
    run_target_rough_and_sharp,
)
from hostile_parallel import hostile
from launch_config import (
    HOSTILE_OUTPUT,
    HOSTILE_WORKSPACE,
    TARGET_OUTPUT,
    TARGET_WORKSPACE,
)
from parallel_runtime import (
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
    ParallelRefusal,
    sha256_file,
)
from target_parallel import target


HERE = Path(__file__).resolve().parent
LENGTH = 12
SOURCE_MANIFEST = HERE / "SOURCE_MANIFEST.json"
LAUNCH_AUTHORIZATION = HERE / "FULL_L12_LAUNCH_AUTHORIZATION_V001.json"
TARGET_CACHE_ROOT = (
    HERE.parent
    / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012/L12"
)
HOSTILE_CACHE_ROOT = (
    HERE.parent
    / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L12"
)


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ParallelRefusal(f"JSON authority is not an object: {path}")
    return value


def verify_successor_packet() -> str:
    """Authenticate every source named by the successor source manifest."""
    manifest = strict_json(SOURCE_MANIFEST)
    if manifest.get("schema") != "L12_PROCESS_PARALLEL_SUCCESSOR_SOURCE_MANIFEST_V001":
        raise ParallelRefusal("successor source manifest schema mismatch")
    rows = manifest.get("files")
    if type(rows) is not list or not rows:
        raise ParallelRefusal("successor source manifest census is absent")
    observed: set[str] = set()
    for row in rows:
        if type(row) is not dict or set(row) != {"path", "sha256"}:
            raise ParallelRefusal("successor source manifest row malformed")
        name = row["path"]
        digest = row["sha256"]
        if (
            type(name) is not str
            or not name
            or name in observed
            or Path(name).name != name
            or type(digest) is not str
            or len(digest) != 64
        ):
            raise ParallelRefusal("successor source manifest row identity mismatch")
        path = HERE / name
        if path.is_symlink() or not path.is_file() or sha256_file(path) != digest:
            raise ParallelRefusal(f"successor source changed: {name}")
        observed.add(name)
    required = {
        "parallel_runtime.py",
        "target_parallel.py",
        "hostile_parallel.py",
        "execution_integration.py",
        "launch_config.py",
        "run_l12_branch.py",
        "launch_full_l12.py",
        "FULL_L12_LAUNCH_AUTHORIZATION_V001.json",
    }
    if not required <= observed:
        raise ParallelRefusal("successor executable/authorization census incomplete")
    authorization = strict_json(LAUNCH_AUTHORIZATION)
    if (
        authorization.get("schema")
        != "L12_PROCESS_PARALLEL_FULL_LAUNCH_AUTHORIZATION_V001"
        or authorization.get("hard_wall_limit_seconds")
        != HARD_WALL_LIMIT_SECONDS
        or authorization.get("workers_by_branch")
        != CONFIGURED_WORKERS_BY_BRANCH
        or authorization.get("total_numerical_workers") != 14
    ):
        raise ParallelRefusal("full L12 launch authorization mismatch")
    return sha256_file(SOURCE_MANIFEST)


def atomic_publish(path: Path, value: dict[str, Any]) -> str:
    """Publish by a no-replace hard link after fsyncing immutable bytes."""
    if path.exists() or path.is_symlink():
        raise ParallelRefusal(f"refuse to overwrite successor output: {path}")
    payload = canonical_json_bytes(value)
    temporary = path.parent / f".{path.name}.tmp.{os.getpid()}"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o600,
    )
    linked = False
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        temporary.chmod(0o444)
        os.link(temporary, path, follow_symlinks=False)
        linked = True
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        digest = sha256_file(path)
        if digest != hashlib.sha256(payload).hexdigest():
            raise ParallelRefusal("published successor output hash mismatch")
        return digest
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary.exists():
            temporary.unlink()
        if linked and path.stat().st_mode & 0o222:
            raise ParallelRefusal("published successor output is writable")


def _target_result(
    *,
    source_manifest_sha256: str,
    manifest_sha256: str,
    rough: dict[str, Any],
    sharp: dict[str, Any],
    comparison: dict[str, Any],
    parallel_resource: dict[str, Any],
    wall_seconds: float,
) -> dict[str, Any]:
    if comparison.get("resolved") is not True:
        raise ParallelRefusal("target rough/sharp comparison is unresolved")
    peak_state = max(
        int(rough["peak_logical_scratch_bytes"]),
        int(sharp["peak_logical_scratch_bytes"]),
    )
    maximum_workset = max(
        int(row[role]["maximum_live_bytes"])
        for row in sharp["rows"]
        for role in ("actual_solver", "null_solver")
    )
    rss = target.builder.rss_bytes()
    if (
        wall_seconds > HARD_WALL_LIMIT_SECONDS
        or maximum_workset > target.v004.v3.CAP_BYTES
        or rss > target.v004.RSS_LIMIT
    ):
        raise ParallelRefusal("target successor resource reconstruction failed")
    return {
        "schema": "TARGET_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V001",
        "L": LENGTH,
        "events": LENGTH,
        "dimension": sharp["dimension"],
        "preterminal_dimension": sharp["preterminal_dimension"],
        "edges": sharp["edges"],
        "coarse_method": target.project_native_method_record(target.v004.sealed.COARSE),
        "fine_method": target.project_native_method_record(target.v004.sealed.FINE),
        "rows": target.project_native_history_rows(sharp["rows"]),
        "comparison": comparison,
        "terminal_shards": sharp["terminal_shards"],
        "cache_manifest_sha256": manifest_sha256,
        "successor_source_manifest_sha256": source_manifest_sha256,
        "launch_authorization_sha256": sha256_file(LAUNCH_AUTHORIZATION),
        "representation": (
            "Q_SHARDED_MEMMAP__PROCESS_PARALLEL_ROW_WINDOWS__"
            "FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS"
        ),
        "lineage_authority": "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING",
        "parallel_resource": parallel_resource,
        "resource": {
            "peak_live_state_bytes": peak_state,
            "cache_payload_bytes": target.builder.payload_bytes(LENGTH),
            "maximum_numerical_workset_bytes": maximum_workset,
            "peak_rss_bytes": rss,
            "rss_limit_bytes": target.v004.RSS_LIMIT,
            "wall_seconds": wall_seconds,
            "wall_limit_seconds": HARD_WALL_LIMIT_SECONDS,
            "passed": True,
        },
        "claim_boundary": (
            "FINITE_PROCESS_PARALLEL_TARGET_L12_HISTORY_ONLY__"
            "NO_SPECTRUM_CONTINUUM_OR_GRAVITY"
        ),
    }


def run_target(source_manifest_sha256: str) -> str:
    cache_root = TARGET_CACHE_ROOT.resolve()
    workspace = TARGET_WORKSPACE.resolve()
    output = TARGET_OUTPUT.resolve()
    manifest_sha256 = sha256_file(cache_root / "CACHE_MANIFEST.json")
    if workspace.exists() or workspace.is_symlink() or output.exists() or output.is_symlink():
        raise ParallelRefusal("target successor allocation is not fresh")
    context: Any = None
    patched = False
    started = time.perf_counter()
    target.PHYSICAL_STARTED = time.monotonic()
    try:
        context = target.CacheContext(cache_root, LENGTH, manifest_sha256)
        target.CACHE = context
        target.v004.sealed.fixed_words = target.cached_fixed_words
        target.v004.sealed.Sector = target.CachedSector
        patched = True
        print(
            "L12_BRANCH_ACK branch=target cache_authenticated=true workers=7 "
            f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f}",
            flush=True,
        )
        workspace.mkdir(parents=True, exist_ok=False)
        rough, sharp, comparison, parallel_resource = run_target_rough_and_sharp(
            length=LENGTH,
            cache_root=cache_root,
            cache_manifest_sha256=manifest_sha256,
            workspace=workspace,
            max_workers=CONFIGURED_WORKERS_BY_BRANCH["target"],
        )
        context.reauthenticate()
        target.seal_terminal_shards(LENGTH, sharp, workspace)
        wall = time.perf_counter() - started
        result = _target_result(
            source_manifest_sha256=source_manifest_sha256,
            manifest_sha256=manifest_sha256,
            rough=rough,
            sharp=sharp,
            comparison=comparison,
            parallel_resource=parallel_resource,
            wall_seconds=wall,
        )
        digest = atomic_publish(output, result)
        print(f"L12_BRANCH_COMPLETE branch=target output_sha256={digest}", flush=True)
        return digest
    finally:
        if patched:
            target.v004.sealed.fixed_words = target.ORIGINAL_FIXED_WORDS
            target.v004.sealed.Sector = target.ORIGINAL_SECTOR
        target.CACHE = None
        target.PHYSICAL_STARTED = None
        if context is not None:
            context.close()
        gc.collect()


def _hostile_source_hashes(manifest: dict[str, Any]) -> dict[str, str]:
    sources = {
        "method": hostile.METHOD,
        "builder": hostile.BUILDER,
        "consumer": hostile.CONSUMER,
        "preflight": hostile.PREFLIGHT,
        "freeze": hostile.FREEZE,
        "preflight_result": hostile.PREFLIGHT_RESULT,
        "independent_hostile_audit": hostile.INDEPENDENT_AUDIT,
    }
    result: dict[str, str] = {}
    for role, path in sources.items():
        digest = sha256_file(path)
        if manifest.get(f"{role}_sha256") != digest:
            raise ParallelRefusal(f"hostile cache source binding changed: {role}")
        result[role] = digest
    return result


def _hostile_result(
    *,
    source_manifest_sha256: str,
    manifest_sha256: str,
    rough: dict[str, Any],
    sharp: dict[str, Any],
    comparison: dict[str, Any],
    terminals: list[dict[str, object]],
    parallel_resource: dict[str, Any],
    wall_seconds: float,
) -> dict[str, Any]:
    hostile.validate_native_rows(sharp["rows"], LENGTH)
    hostile.validate_comparison(comparison, LENGTH)
    storage = hostile.storage_census(LENGTH)
    peak_state = max(
        int(rough["peak_logical_scratch_bytes"]),
        int(sharp["peak_logical_scratch_bytes"]),
    )
    maximum_allocation = max(
        int(row[role]["maximum_allocation_estimate_bytes"])
        for row in sharp["rows"]
        for role in ("actual_solver", "null_solver")
    )
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if (
        wall_seconds > HARD_WALL_LIMIT_SECONDS
        or peak_state != storage["maximum_live_state_bytes"]
        or maximum_allocation > hostile.NUMERICAL_WORKSPACE_LIMIT
        or rss > hostile.RSS_LIMIT
    ):
        raise ParallelRefusal("hostile successor resource reconstruction failed")
    return {
        "schema": "HOSTILE_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V001",
        "L": LENGTH,
        "events": LENGTH,
        "dimension": math.comb(3 * LENGTH, LENGTH),
        "preterminal_dimension": math.comb(3 * LENGTH - 1, LENGTH - 1),
        "edges": 3 * LENGTH,
        "coarse_method": hostile.accuracy_record(hostile.physical.ROUGH),
        "fine_method": hostile.accuracy_record(hostile.physical.SHARP),
        "rows": sharp["rows"],
        "comparison": comparison,
        "terminal_shards": terminals,
        "cache_manifest_sha256": manifest_sha256,
        "successor_source_manifest_sha256": source_manifest_sha256,
        "launch_authorization_sha256": sha256_file(LAUNCH_AUTHORIZATION),
        "representation": (
            "Q_SHARDED_MEMMAP__PROCESS_PARALLEL_ROW_WINDOWS__"
            "INDEPENDENT_HOSTILE_FULL_MASK"
        ),
        "lineage_authority": "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING",
        "parallel_resource": parallel_resource,
        "resource": {
            "peak_live_state_bytes": peak_state,
            "cache_payload_bytes": storage["actual_cache_array_bytes"],
            "maximum_numerical_allocation_estimate_bytes": maximum_allocation,
            "peak_rss_bytes": rss,
            "rss_limit_bytes": hostile.RSS_LIMIT,
            "wall_seconds": wall_seconds,
            "wall_limit_seconds": HARD_WALL_LIMIT_SECONDS,
            "passed": True,
        },
        "claim_boundary": (
            "FINITE_PROCESS_PARALLEL_HOSTILE_L12_HISTORY_ONLY__"
            "NO_SPECTRUM_CONTINUUM_OR_GRAVITY"
        ),
    }


def run_hostile(source_manifest_sha256: str) -> str:
    cache_root = HOSTILE_CACHE_ROOT.resolve()
    workspace = HOSTILE_WORKSPACE.resolve()
    output = HOSTILE_OUTPUT.resolve()
    manifest_path = cache_root / "CACHE_MANIFEST.json"
    manifest_sha256 = sha256_file(manifest_path)
    manifest = strict_json(manifest_path)
    source_hashes = _hostile_source_hashes(manifest)
    if workspace.exists() or workspace.is_symlink() or output.exists() or output.is_symlink():
        raise ParallelRefusal("hostile successor allocation is not fresh")
    custody = hostile.AuthorityCustody()
    context: Any = None
    started = time.perf_counter()
    try:
        context = hostile.CacheContext(
            LENGTH,
            cache_root,
            manifest,
            manifest_sha256,
            source_hashes,
            started,
        )
        hostile.legacy.configure(LENGTH, context, started)
        print(
            "L12_BRANCH_ACK branch=hostile cache_authenticated=true workers=7 "
            f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f}",
            flush=True,
        )
        rough, sharp, comparison, parallel_resource = run_hostile_rough_and_sharp(
            length=LENGTH,
            cache_root=cache_root,
            cache_manifest_sha256=manifest_sha256,
            workspace=workspace,
            max_workers=CONFIGURED_WORKERS_BY_BRANCH["hostile"],
        )
        context.reauthenticate()
        terminals = hostile.seal_terminal_shards(LENGTH, workspace, sharp, custody)
        wall = time.perf_counter() - started
        result = _hostile_result(
            source_manifest_sha256=source_manifest_sha256,
            manifest_sha256=manifest_sha256,
            rough=rough,
            sharp=sharp,
            comparison=comparison,
            terminals=terminals,
            parallel_resource=parallel_resource,
            wall_seconds=wall,
        )
        custody.verify_all()
        digest = atomic_publish(output, result)
        print(f"L12_BRANCH_COMPLETE branch=hostile output_sha256={digest}", flush=True)
        return digest
    finally:
        hostile.legacy.CACHE = None
        hostile.v3.EXECUTION_STARTED = None
        if context is not None:
            context.close()
        custody.close()
        gc.collect()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("branch", choices=("target", "hostile"))
    arguments = parser.parse_args()
    try:
        source_manifest_sha256 = verify_successor_packet()
        if arguments.branch == "target":
            run_target(source_manifest_sha256)
        else:
            run_hostile(source_manifest_sha256)
        return 0
    except BaseException as error:
        print(
            f"L12_BRANCH_REFUSED branch={arguments.branch} "
            f"error={type(error).__name__}:{error}",
            file=sys.stderr,
            flush=True,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
