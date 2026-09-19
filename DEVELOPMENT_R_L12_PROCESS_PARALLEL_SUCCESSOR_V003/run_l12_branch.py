#!/usr/bin/env python3
"""Run one independent branch of the bounded V003 L12 numerical repair."""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
import math
import resource
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V002 = ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V002"
V001 = ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V001"
if str(V002) not in sys.path:
    sys.path.append(str(V002))

from comparison_gate import (  # noqa: E402
    persist_hostile_before_gate,
    persist_target_before_gate,
    require_resolved,
)
from evidence import EvidenceJournal  # noqa: E402
from persistent_runtime import PersistentBranchProcessPool  # noqa: E402
from v001_bridge import hostile, parallel_runtime, target  # noqa: E402

from launch_config import (  # noqa: E402
    CONFIGURED_WORKERS_BY_BRANCH,
    HARD_WALL_LIMIT_SECONDS,
    HOSTILE_EVIDENCE,
    HOSTILE_OUTPUT,
    HOSTILE_SHARP_V002,
    HOSTILE_V002_WORKSPACE,
    HOSTILE_WORKSPACE,
    TARGET_EVIDENCE,
    TARGET_OUTPUT,
    TARGET_WORKSPACE,
)
from repair_kernels import (  # noqa: E402
    HOSTILE_ROUGH,
    HOSTILE_SHARP,
    TARGET_COARSE,
    TARGET_FINE,
    TARGET_MAX_SUBDIVISIONS,
    HostileRepairAdapter,
    TargetRepairAdapter,
    hostile_capacity_scope,
    target_capacity_scope,
)


_v002_spec = importlib.util.spec_from_file_location(
    "_l12_v002_branch_for_v003", V002 / "run_l12_branch.py"
)
if _v002_spec is None or _v002_spec.loader is None:
    raise RuntimeError("could not load the V002 branch result helpers")
v002_branch = importlib.util.module_from_spec(_v002_spec)
_v002_spec.loader.exec_module(v002_branch)

LENGTH = 12
TARGET_CACHE_ROOT = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012/L12"
)
HOSTILE_CACHE_ROOT = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L12"
)


def sha256_file(path: Path) -> str:
    return parallel_runtime.sha256_file(path)


def source_record() -> dict[str, str]:
    paths = {
        "repair_kernels": HERE / "repair_kernels.py",
        "branch": HERE / "run_l12_branch.py",
        "launch_config": HERE / "launch_config.py",
        "parallel_runtime": V001 / "parallel_runtime.py",
        "target_parallel": V001 / "target_parallel.py",
        "hostile_parallel": V001 / "hostile_parallel.py",
        "comparison_gate": V002 / "comparison_gate.py",
        "persistent_runtime": V002 / "persistent_runtime.py",
    }
    return {name: sha256_file(path) for name, path in paths.items()}


def source_record_sha256(record: dict[str, str]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def load_checkpoint_payload(
    path: Path, *, branch: str, category: str, label: str
) -> tuple[dict[str, Any], str]:
    digest = sha256_file(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if (
        type(value) is not dict
        or value.get("branch") != branch
        or value.get("category") != category
        or value.get("label") != label
        or type(value.get("payload")) is not dict
    ):
        raise parallel_runtime.ParallelRefusal(
            f"V002 checkpoint identity mismatch: {path}"
        )
    return value["payload"], digest


def _resource_with_repair_provenance(
    resource_record: dict[str, Any], *, source_record_value: dict[str, str]
) -> dict[str, Any]:
    value = dict(resource_record)
    value.update(
        {
            "numerical_successor": "V003",
            "physical_operator_changed": False,
            "admission_or_route_time_changed": False,
            "observable_or_threshold_changed": False,
            "source_record": source_record_value,
        }
    )
    return value


def run_target() -> str:
    cache_root = TARGET_CACHE_ROOT.resolve()
    workspace = TARGET_WORKSPACE.resolve()
    output = TARGET_OUTPUT.resolve()
    evidence_root = TARGET_EVIDENCE.resolve()
    manifest_sha256 = sha256_file(cache_root / "CACHE_MANIFEST.json")
    if any(path.exists() or path.is_symlink() for path in (workspace, output, evidence_root)):
        raise parallel_runtime.ParallelRefusal("target V003 allocation is not fresh")
    source = source_record()
    source_digest = source_record_sha256(source)
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
        journal.write(
            "lifecycle",
            "V003_NUMERICAL_REPAIR_OPEN",
            {
                "source_record": source,
                "source_record_sha256": source_digest,
                "target_coarse": target.project_native_method_record(TARGET_COARSE),
                "target_fine": target.project_native_method_record(TARGET_FINE),
                "maximum_subdivisions": TARGET_MAX_SUBDIVISIONS,
                "resume_decision": (
                    "FULL_ROUGH_AND_SHARP_REPLAY_REQUIRED__ONLY_RETAINED_PREFIX_11_"
                    "IS_DOWNSTREAM_OF_FAILED_EVENTS"
                ),
            },
        )
        print(
            "L12_BRANCH_ACK branch=target repair=V003 cache_authenticated=true "
            f"workers=7 wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f}",
            flush=True,
        )
        workspace.mkdir(parents=True, exist_ok=False)
        deadline = time.monotonic() + HARD_WALL_LIMIT_SECONDS
        with target_capacity_scope():
            with PersistentBranchProcessPool(
                branch="target",
                cache_root=cache_root,
                manifest_sha256=manifest_sha256,
                length=LENGTH,
                deadline_monotonic=deadline,
                max_workers=CONFIGURED_WORKERS_BY_BRANCH["target"],
                evidence=journal,
            ) as pool:
                with parallel_runtime.parent_termination_guard(pool), TargetRepairAdapter(pool):
                    rough_root = workspace / "rough"
                    sharp_root = workspace / "sharp"
                    rough = target.v004.history(
                        LENGTH, TARGET_COARSE, rough_root, retain_terminal=False
                    )
                    journal.history("rough", rough)
                    target.v004.remove_resolution(rough_root, workspace)
                    sharp = target.v004.history(
                        LENGTH, TARGET_FINE, sharp_root, retain_terminal=True
                    )
                    journal.history("sharp", sharp)
                    pool.assert_run_complete()
                    comparison = target.v004.sealed.summarize(LENGTH, rough, sharp)
                    diagnostic = persist_target_before_gate(
                        journal, LENGTH, rough, sharp, comparison
                    )
                    require_resolved(diagnostic)
                parallel_resource = pool.resource_record()
        context.reauthenticate()
        target.seal_terminal_shards(LENGTH, sharp, workspace)
        wall = time.perf_counter() - started
        with target_capacity_scope():
            result = v002_branch._finish_target_result(
                source_manifest_sha256=source_digest,
                manifest_sha256=manifest_sha256,
                rough=rough,
                sharp=sharp,
                comparison=comparison,
                parallel_resource=_resource_with_repair_provenance(
                    parallel_resource, source_record_value=source
                ),
                wall_seconds=wall,
            )
        result.update(
            {
                "schema": "TARGET_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V003",
                "successor_source_manifest_sha256": source_digest,
                "launch_authorization_sha256": source_digest,
                "parent_evidence_root": str(evidence_root),
                "numerical_repair": {
                    "target_max_subdivisions": TARGET_MAX_SUBDIVISIONS,
                    "coarse_checkpoints": list(TARGET_COARSE.checkpoints),
                    "fine_checkpoints": list(TARGET_FINE.checkpoints),
                    "coarse_tolerance": TARGET_COARSE.tolerance,
                    "fine_tolerance": TARGET_FINE.tolerance,
                    "physical_operator_changed": False,
                    "predicate_thresholds_changed": False,
                },
            }
        )
        digest = v002_branch.v001_branch.atomic_publish(output, result)
        journal.write(
            "lifecycle",
            "BRANCH_COMPLETE",
            {"output": str(output), "output_sha256": digest, "wall_seconds": wall},
        )
        print(f"L12_BRANCH_COMPLETE branch=target repair=V003 output_sha256={digest}", flush=True)
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


def hostile_terminal_row(
    terminal: tuple[Any, ...], edges: list[tuple[int, int, str]]
) -> dict[str, Any]:
    (
        before,
        admitted,
        after,
        null_after,
        actual_flux,
        null_flux,
        actual_method,
        null_method,
        allowed,
        blocked,
        blocked_error,
    ) = terminal
    incidence = np.zeros((2 * LENGTH, len(edges)), dtype=np.int8)
    for index, (u, v, _role) in enumerate(edges):
        incidence[u, index] = 1
        incidence[v, index] = -1
    connectors = np.array(
        [index for index, edge in enumerate(edges) if edge[2] == "connector"],
        dtype=np.int32,
    )
    write = float(admitted["retained"]) - float(before["retained"])
    actual_node = after["occupation"] - admitted["occupation"] + incidence @ actual_flux
    null_node = null_after["occupation"] - before["occupation"] + incidence @ null_flux
    delta = actual_flux - null_flux
    event = LENGTH
    return {
        "event": event,
        "input_prefix": event - 1,
        "input_prefix_dimension": math.comb(2 * LENGTH + event - 1, event - 1),
        "logical_output_prefix_dimension": math.comb(2 * LENGTH + event, event),
        "terminal_children_streamed": True,
        "allow_probability": float(allowed),
        "blocked_probability": float(blocked),
        "reverse_support_probability": 0.0,
        "blocked_null_state_error": float(blocked_error),
        "W_n": write,
        "q_retained_after_transport": float(after["retained"]),
        "q_genesis_after": float(after["remaining"]),
        "sector_weights": [float(value) for value in after["sectors"]],
        "connector_delta_l1": float(np.sum(np.abs(delta[connectors]))),
        "connector_delta_signed": float(np.sum(delta[connectors])),
        "admission_total_content_residual": float(
            write + float(admitted["remaining"]) - float(before["remaining"])
        ),
        "admission_bandwidth_residual": float(
            float(admitted["remaining"]) - float(before["remaining"]) + write
        ),
        "target_owner_residual": float(
            float(admitted["occupation"][event - 1])
            - float(before["occupation"][event - 1])
            - write
        ),
        "transport_node_residual_l1": float(np.sum(np.abs(actual_node))),
        "transport_node_residual_linf": float(np.max(np.abs(actual_node))),
        "null_transport_node_residual_l1": float(np.sum(np.abs(null_node))),
        "transport_number_drift": abs(
            float(after["retained"]) - float(admitted["retained"])
        ),
        "null_transport_number_drift": abs(
            float(null_after["retained"]) - float(before["retained"])
        ),
        "actual_norm_error": abs(float(after["norm"]) - 1.0),
        "null_norm_error": abs(float(null_after["norm"]) - 1.0),
        "actual_solver": actual_method,
        "null_solver": null_method,
    }


def authenticate_resumed_hostile_prefix(
    custody: Any, sharp: dict[str, Any]
) -> list[dict[str, object]]:
    native_rows = sharp.get("terminal_shards")
    if type(native_rows) is not list or len(native_rows) != LENGTH:
        raise parallel_runtime.ParallelRefusal("hostile V002 prefix descriptor census mismatch")
    terminal_root = (HOSTILE_V002_WORKSPACE / "sharp" / "prefix_11").resolve()
    terminals: list[dict[str, object]] = []
    for q, native in enumerate(native_rows):
        relative = f"prefix_11/q_{q:02d}.c128"
        shape = [math.comb(11, q), math.comb(24, q)]
        byte_count = 16 * math.prod(shape)
        if native != {
            "q": q,
            "path": relative,
            "shape": shape,
            "logical_bytes": byte_count,
        }:
            raise parallel_runtime.ParallelRefusal("hostile V002 prefix descriptor mismatch")
        path = (HOSTILE_V002_WORKSPACE / "sharp" / relative).resolve()
        if path != terminal_root / f"q_{q:02d}.c128" or path.stat().st_size != byte_count:
            raise parallel_runtime.ParallelRefusal("hostile V002 prefix file mismatch")
        _record, digest = custody.authenticate(
            path, f"hostile V003 resumable prefix q={q}", immutable=False
        )
        terminals.append(
            {"q": q, "path": str(path), "shape": shape, "bytes": byte_count, "sha256": digest}
        )
    custody.verify_all()
    return terminals


def run_hostile() -> str:
    cache_root = HOSTILE_CACHE_ROOT.resolve()
    workspace = HOSTILE_WORKSPACE.resolve()
    output = HOSTILE_OUTPUT.resolve()
    evidence_root = HOSTILE_EVIDENCE.resolve()
    manifest_path = cache_root / "CACHE_MANIFEST.json"
    manifest_sha256 = sha256_file(manifest_path)
    manifest = v002_branch.strict_json(manifest_path)
    source_hashes = v002_branch.v001_branch._hostile_source_hashes(manifest)
    if any(path.exists() or path.is_symlink() for path in (workspace, output, evidence_root)):
        raise parallel_runtime.ParallelRefusal("hostile V003 allocation is not fresh")
    old_sharp, old_sharp_digest = load_checkpoint_payload(
        HOSTILE_SHARP_V002,
        branch="hostile",
        category="histories",
        label="SHARP_SUMMARY",
    )
    source = source_record()
    source_digest = source_record_sha256(source)
    custody = hostile.AuthorityCustody()
    context: Any = None
    journal: EvidenceJournal | None = None
    started = time.perf_counter()
    try:
        terminals = authenticate_resumed_hostile_prefix(custody, old_sharp)
        context = hostile.CacheContext(
            LENGTH, cache_root, manifest, manifest_sha256, source_hashes, started
        )
        hostile.legacy.configure(LENGTH, context, started)
        journal = EvidenceJournal(evidence_root, "hostile")
        journal.write(
            "lifecycle",
            "V003_NUMERICAL_REPAIR_OPEN",
            {
                "source_record": source,
                "source_record_sha256": source_digest,
                "hostile_rough": hostile.accuracy_record(HOSTILE_ROUGH),
                "hostile_sharp": hostile.accuracy_record(HOSTILE_SHARP),
                "resumed_sharp_summary": str(HOSTILE_SHARP_V002),
                "resumed_sharp_summary_sha256": old_sharp_digest,
                "resumed_prefix_files": terminals,
                "resume_decision": "SHARP_EVENT_12_FROM_AUTHENTICATED_V002_PREFIX_11",
            },
        )
        print(
            "L12_BRANCH_ACK branch=hostile repair=V003 cache_authenticated=true "
            "resume_prefix_11_authenticated=true workers=7 "
            f"wall_limit_seconds={HARD_WALL_LIMIT_SECONDS:.1f}",
            flush=True,
        )
        workspace.mkdir(parents=True, exist_ok=False)
        deadline = time.monotonic() + HARD_WALL_LIMIT_SECONDS
        with hostile_capacity_scope():
            with PersistentBranchProcessPool(
                branch="hostile",
                cache_root=cache_root,
                manifest_sha256=manifest_sha256,
                length=LENGTH,
                deadline_monotonic=deadline,
                max_workers=CONFIGURED_WORKERS_BY_BRANCH["hostile"],
                evidence=journal,
            ) as pool:
                with parallel_runtime.parent_termination_guard(pool), HostileRepairAdapter(pool):
                    rough_root = workspace / "rough"
                    rough = hostile.v3.history(
                        LENGTH, HOSTILE_ROUGH, rough_root, retain_terminal=False
                    )
                    journal.history("rough", rough)
                    hostile.v3.remove_resolution(rough_root)
                    state = hostile.v3.DiskPrefix(
                        (HOSTILE_V002_WORKSPACE / "sharp").resolve(), LENGTH - 1
                    )
                    state.verify_complete()
                    edges = hostile.physical.hostile_edges(LENGTH)
                    terminal = hostile.v3.terminal_route(state, HOSTILE_SHARP, edges)
                    sharp = dict(old_sharp)
                    sharp["rows"] = [dict(row) for row in old_sharp["rows"][:-1]] + [
                        hostile_terminal_row(terminal, edges)
                    ]
                    sharp["peak_logical_scratch_bytes"] = max(
                        int(old_sharp["peak_logical_scratch_bytes"]),
                        int(rough["peak_logical_scratch_bytes"]),
                    )
                    journal.history("sharp", sharp)
                    pool.assert_run_complete()
                    comparison = hostile.physical.compare(LENGTH, rough, sharp)
                    diagnostic = persist_hostile_before_gate(
                        journal, LENGTH, rough, sharp, comparison
                    )
                    require_resolved(diagnostic)
                parallel_resource = pool.resource_record()
        context.reauthenticate()
        custody.verify_all()
        wall = time.perf_counter() - started
        with hostile_capacity_scope():
            result = v002_branch._finish_hostile_result(
                source_manifest_sha256=source_digest,
                manifest_sha256=manifest_sha256,
                rough=rough,
                sharp=sharp,
                comparison=comparison,
                terminals=terminals,
                parallel_resource=_resource_with_repair_provenance(
                    parallel_resource, source_record_value=source
                ),
                wall_seconds=wall,
            )
        result.update(
            {
                "schema": "HOSTILE_CACHED_PREFIX_HISTORY_PROCESS_PARALLEL_V003",
                "successor_source_manifest_sha256": source_digest,
                "launch_authorization_sha256": source_digest,
                "parent_evidence_root": str(evidence_root),
                "numerical_repair": {
                    "rough_checkpoints": list(HOSTILE_ROUGH.checkpoints),
                    "sharp_checkpoints": list(HOSTILE_SHARP.checkpoints),
                    "rough_tolerance": HOSTILE_ROUGH.tolerance,
                    "sharp_tolerance": HOSTILE_SHARP.tolerance,
                    "sharp_resume_prefix": 11,
                    "resumed_sharp_summary_sha256": old_sharp_digest,
                    "physical_operator_changed": False,
                    "predicate_thresholds_changed": False,
                },
            }
        )
        digest = v002_branch.v001_branch.atomic_publish(output, result)
        journal.write(
            "lifecycle",
            "BRANCH_COMPLETE",
            {"output": str(output), "output_sha256": digest, "wall_seconds": wall},
        )
        print(f"L12_BRANCH_COMPLETE branch=hostile repair=V003 output_sha256={digest}", flush=True)
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
        if arguments.branch == "target":
            run_target()
        else:
            run_hostile()
        return 0
    except BaseException as error:
        print(
            f"L12_BRANCH_REFUSED branch={arguments.branch} repair=V003 "
            f"error={type(error).__name__}:{error}",
            file=sys.stderr,
            flush=True,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
