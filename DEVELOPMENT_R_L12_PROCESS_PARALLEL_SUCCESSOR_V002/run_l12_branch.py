#!/usr/bin/env python3
"""Authenticated V002 branch parent with pre-gate durable evidence."""

from __future__ import annotations

import argparse
import gc
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

from comparison_gate import require_resolved
from evidence import EvidenceJournal
from execution_integration import run_hostile_rough_and_sharp, run_target_rough_and_sharp
from launch_config import (
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
    HOSTILE_EVIDENCE,
    HOSTILE_OUTPUT,
    HOSTILE_WORKSPACE,
    TARGET_EVIDENCE,
    TARGET_OUTPUT,
    TARGET_WORKSPACE,
)
from v001_bridge import hostile, parallel_runtime, target


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
_v001_branch_spec = importlib.util.spec_from_file_location(
    "_l12_v001_run_l12_branch",
    ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V001/run_l12_branch.py",
)
if _v001_branch_spec is None or _v001_branch_spec.loader is None:
    raise RuntimeError("could not load the frozen V001 branch helper")
v001_branch = importlib.util.module_from_spec(_v001_branch_spec)
_v001_branch_spec.loader.exec_module(v001_branch)
ParallelRefusal = parallel_runtime.ParallelRefusal
sha256_file = parallel_runtime.sha256_file

LENGTH = 12
SOURCE_MANIFEST = HERE / "SOURCE_MANIFEST.json"
STAGING_CONFIGURATION = HERE / "L12_STAGING_CONFIGURATION_V002.json"
TARGET_CACHE_ROOT = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012/L12"
)
HOSTILE_CACHE_ROOT = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L12"
)


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ParallelRefusal(f"JSON authority is not an object: {path}")
    return value


def verify_successor_packet() -> str:
    """Authenticate V002 wrappers and the reused frozen V001 kernels."""
    manifest = strict_json(SOURCE_MANIFEST)
    if manifest.get("schema") != "L12_PROCESS_PARALLEL_SUCCESSOR_SOURCE_MANIFEST_V002":
        raise ParallelRefusal("V002 source manifest schema mismatch")
    rows = manifest.get("files")
    if type(rows) is not list or not rows:
        raise ParallelRefusal("V002 source manifest census is absent")
    observed: set[str] = set()
    for row in rows:
        if type(row) is not dict or set(row) != {"path", "sha256"}:
            raise ParallelRefusal("V002 source manifest row malformed")
        name = row["path"]
        digest = row["sha256"]
        if (
            type(name) is not str
            or not name
            or name in observed
            or Path(name).is_absolute()
            or type(digest) is not str
            or len(digest) != 64
        ):
            raise ParallelRefusal("V002 source manifest row identity mismatch")
        candidate = (HERE / name).resolve()
        if (
            ROOT.resolve() not in candidate.parents
            or candidate.is_symlink()
            or not candidate.is_file()
            or sha256_file(candidate) != digest
        ):
            raise ParallelRefusal(f"V002 source changed: {name}")
        observed.add(name)
    required = {
        "v001_bridge.py",
        "evidence.py",
        "persistent_runtime.py",
        "comparison_gate.py",
        "execution_integration.py",
        "launch_config.py",
        "launcher_supervision.py",
        "run_l12_branch.py",
        "launch_full_l12.py",
        "L12_STAGING_CONFIGURATION_V002.json",
        "../DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V001/parallel_runtime.py",
        "../DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V001/target_parallel.py",
        "../DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V001/hostile_parallel.py",
    }
    if not required <= observed:
        raise ParallelRefusal("V002 executable/frozen-kernel census incomplete")
    staging = strict_json(STAGING_CONFIGURATION)
    if (
        staging.get("schema") != "L12_PROCESS_PARALLEL_STAGING_CONFIGURATION_V002"
        or staging.get("launch_state") != "STAGED_NOT_TRIGGERED"
        or staging.get("requires_explicit_post_l4_review") is not True
        or staging.get("hard_wall_limit_seconds") != HARD_WALL_LIMIT_SECONDS
        or staging.get("workers_by_branch") != CONFIGURED_WORKERS_BY_BRANCH
        or staging.get("total_numerical_workers") != 14
        or staging.get("fail_fast_branch_coupling") is not False
    ):
        raise ParallelRefusal("V002 staging configuration mismatch")
    return sha256_file(SOURCE_MANIFEST)


def _finish_target_result(
    *,
    source_manifest_sha256: str,
    manifest_sha256: str,
    rough: dict[str, Any],
    sharp: dict[str, Any],
    comparison: dict[str, Any],
    parallel_resource: dict[str, Any],
    wall_seconds: float,
) -> dict[str, Any]:
    result = v001_branch._target_result(
        source_manifest_sha256=source_manifest_sha256,
        manifest_sha256=manifest_sha256,
        rough=rough,
        sharp=sharp,
        comparison=comparison,
        parallel_resource=parallel_resource,
        wall_seconds=wall_seconds,
    )
    result["schema"] = "TARGET_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V002"
    result["successor_source_manifest_sha256"] = source_manifest_sha256
    result["launch_authorization_sha256"] = sha256_file(STAGING_CONFIGURATION)
    result["parent_evidence_root"] = str(TARGET_EVIDENCE)
    return result


def run_target(source_manifest_sha256: str) -> str:
    cache_root = TARGET_CACHE_ROOT.resolve()
    workspace = TARGET_WORKSPACE.resolve()
    output = TARGET_OUTPUT.resolve()
    evidence_root = TARGET_EVIDENCE.resolve()
    manifest_sha256 = sha256_file(cache_root / "CACHE_MANIFEST.json")
    if any(path.exists() or path.is_symlink() for path in (workspace, output, evidence_root)):
        raise ParallelRefusal("target V002 allocation is not fresh")
    context: Any = None
    journal: EvidenceJournal | None = None
    patched = False
    started = time.perf_counter()
    target.PHYSICAL_STARTED = time.monotonic()
    try:
        context = target.CacheContext(cache_root, LENGTH, manifest_sha256)
        target.CACHE = context
        target.v004.sealed.fixed_words = target.cached_fixed_words
        target.v004.sealed.Sector = target.CachedSector
        patched = True
        journal = EvidenceJournal(evidence_root, "target")
        print(
            "L12_BRANCH_ACK branch=target cache_authenticated=true workers=7 "
            f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f}",
            flush=True,
        )
        workspace.mkdir(parents=True, exist_ok=False)
        rough, sharp, comparison, diagnostic, parallel_resource = run_target_rough_and_sharp(
            length=LENGTH,
            cache_root=cache_root,
            cache_manifest_sha256=manifest_sha256,
            workspace=workspace,
            evidence=journal,
            max_workers=CONFIGURED_WORKERS_BY_BRANCH["target"],
        )
        require_resolved(diagnostic)
        context.reauthenticate()
        target.seal_terminal_shards(LENGTH, sharp, workspace)
        wall = time.perf_counter() - started
        result = _finish_target_result(
            source_manifest_sha256=source_manifest_sha256,
            manifest_sha256=manifest_sha256,
            rough=rough,
            sharp=sharp,
            comparison=comparison,
            parallel_resource=parallel_resource,
            wall_seconds=wall,
        )
        digest = v001_branch.atomic_publish(output, result)
        journal.write(
            "lifecycle",
            "BRANCH_COMPLETE",
            {"output": str(output), "output_sha256": digest, "wall_seconds": wall},
        )
        print(f"L12_BRANCH_COMPLETE branch=target output_sha256={digest}", flush=True)
        return digest
    except BaseException as error:
        if journal is not None:
            journal.write(
                "lifecycle",
                "BRANCH_REFUSAL",
                {"error_type": type(error).__name__, "error": str(error)},
            )
        raise
    finally:
        if patched:
            target.v004.sealed.fixed_words = target.ORIGINAL_FIXED_WORDS
            target.v004.sealed.Sector = target.ORIGINAL_SECTOR
        target.CACHE = None
        target.PHYSICAL_STARTED = None
        if context is not None:
            context.close()
        gc.collect()


def _finish_hostile_result(
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
    result = v001_branch._hostile_result(
        source_manifest_sha256=source_manifest_sha256,
        manifest_sha256=manifest_sha256,
        rough=rough,
        sharp=sharp,
        comparison=comparison,
        terminals=terminals,
        parallel_resource=parallel_resource,
        wall_seconds=wall_seconds,
    )
    result["schema"] = "HOSTILE_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V002"
    result["successor_source_manifest_sha256"] = source_manifest_sha256
    result["launch_authorization_sha256"] = sha256_file(STAGING_CONFIGURATION)
    result["parent_evidence_root"] = str(HOSTILE_EVIDENCE)
    return result


def run_hostile(source_manifest_sha256: str) -> str:
    cache_root = HOSTILE_CACHE_ROOT.resolve()
    workspace = HOSTILE_WORKSPACE.resolve()
    output = HOSTILE_OUTPUT.resolve()
    evidence_root = HOSTILE_EVIDENCE.resolve()
    manifest_path = cache_root / "CACHE_MANIFEST.json"
    manifest_sha256 = sha256_file(manifest_path)
    manifest = strict_json(manifest_path)
    source_hashes = v001_branch._hostile_source_hashes(manifest)
    if any(path.exists() or path.is_symlink() for path in (workspace, output, evidence_root)):
        raise ParallelRefusal("hostile V002 allocation is not fresh")
    custody = hostile.AuthorityCustody()
    context: Any = None
    journal: EvidenceJournal | None = None
    started = time.perf_counter()
    try:
        context = hostile.CacheContext(
            LENGTH, cache_root, manifest, manifest_sha256, source_hashes, started
        )
        hostile.legacy.configure(LENGTH, context, started)
        journal = EvidenceJournal(evidence_root, "hostile")
        print(
            "L12_BRANCH_ACK branch=hostile cache_authenticated=true workers=7 "
            f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f}",
            flush=True,
        )
        workspace.mkdir(parents=True, exist_ok=False)
        rough, sharp, comparison, diagnostic, parallel_resource = run_hostile_rough_and_sharp(
            length=LENGTH,
            cache_root=cache_root,
            cache_manifest_sha256=manifest_sha256,
            workspace=workspace,
            evidence=journal,
            max_workers=CONFIGURED_WORKERS_BY_BRANCH["hostile"],
        )
        require_resolved(diagnostic)
        context.reauthenticate()
        terminals = hostile.seal_terminal_shards(LENGTH, workspace, sharp, custody)
        wall = time.perf_counter() - started
        result = _finish_hostile_result(
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
        digest = v001_branch.atomic_publish(output, result)
        journal.write(
            "lifecycle",
            "BRANCH_COMPLETE",
            {"output": str(output), "output_sha256": digest, "wall_seconds": wall},
        )
        print(f"L12_BRANCH_COMPLETE branch=hostile output_sha256={digest}", flush=True)
        return digest
    except BaseException as error:
        if journal is not None:
            journal.write(
                "lifecycle",
                "BRANCH_REFUSAL",
                {"error_type": type(error).__name__, "error": str(error)},
            )
        raise
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
