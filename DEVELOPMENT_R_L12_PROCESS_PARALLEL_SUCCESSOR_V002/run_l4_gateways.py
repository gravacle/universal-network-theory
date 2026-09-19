#!/usr/bin/env python3
"""Run the three required L4 V002 observability/survival gateways."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

from comparison_gate import (
    UnresolvedComparison,
    persist_target_before_gate,
    require_resolved,
)
from evidence import EvidenceJournal
from execution_integration import run_hostile_rough_and_sharp, run_target_rough_and_sharp
from launcher_supervision import branch_environment, supervise
from v001_bridge import hostile, parallel_runtime, target


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARTIFACT_ROOT = HERE / "TEST_ARTIFACTS/L4_GATEWAYS_V002"
LOG_ROOT = HERE / "TEST_LOGS/L4_GATEWAYS_V002"
FIXTURE = HERE / "l4_branch_fixture.py"


def write_log(name: str, text: str) -> dict[str, Any]:
    path = LOG_ROOT / name
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o600,
    )
    try:
        payload = text.encode("utf-8")
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    path.chmod(0o444)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"L4_TEST_LOG name={name} sha256={digest} path={path}", flush=True)
    return {"path": str(path), "sha256": digest}


def normal_target_l4() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    case_root = ARTIFACT_ROOT / "normal_completion/target"
    case_root.mkdir(parents=True, exist_ok=False)
    cache_root = (
        ROOT
        / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        / "CACHE_PAYLOADS_V012/L4"
    ).resolve()
    manifest_hash = parallel_runtime.sha256_file(cache_root / "CACHE_MANIFEST.json")
    context = target.CacheContext(cache_root, 4, manifest_hash)
    original_cache = target.CACHE
    original_words = target.v004.sealed.fixed_words
    original_sector = target.v004.sealed.Sector
    target.PHYSICAL_STARTED = time.monotonic()
    try:
        target.CACHE = context
        target.v004.sealed.fixed_words = target.cached_fixed_words
        target.v004.sealed.Sector = target.CachedSector
        journal = EvidenceJournal(case_root / "evidence", "target")
        rough, sharp, comparison, diagnostic, resource = run_target_rough_and_sharp(
            length=4,
            cache_root=cache_root,
            cache_manifest_sha256=manifest_hash,
            workspace=case_root / "workspace",
            evidence=journal,
            deadline_monotonic=time.monotonic() + 300.0,
            max_workers=2,
        )
        require_resolved(diagnostic)
        context.reauthenticate()
    finally:
        target.v004.sealed.fixed_words = original_words
        target.v004.sealed.Sector = original_sector
        target.CACHE = original_cache
        target.PHYSICAL_STARTED = None
        context.close()
    checkpoint_count = len(list((case_root / "evidence").rglob("*.json")))
    required = {
        "ROUGH_SUMMARY",
        "SHARP_SUMMARY",
        "PRE_GATE_COMPARISON",
        "RUN_COMPLETE",
    }
    labels = {
        json.loads(path.read_text(encoding="utf-8"))["label"]
        for path in (case_root / "evidence").rglob("*.json")
    }
    if comparison.get("resolved") is not True or not required <= labels:
        raise AssertionError("normal L4 persistence gateway did not resolve")
    return rough, sharp, {
        "branch": "target",
        "status": "PASS",
        "comparison_resolved": comparison["resolved"],
        "comparison_classification": comparison["classification"],
        "checkpoint_count": checkpoint_count,
        "required_checkpoint_labels": sorted(required),
        "raw_metrics": diagnostic["raw_metrics"],
        "full_run_progress": resource["full_run_progress"],
        "observed_worker_pids": resource["observed_worker_pids"],
        "evidence_root": str(case_root / "evidence"),
    }


def normal_hostile_l4() -> dict[str, Any]:
    case_root = ARTIFACT_ROOT / "normal_completion/hostile"
    case_root.mkdir(parents=True, exist_ok=False)
    cache_root = (
        ROOT
        / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
        / "V004R4_CACHE_PAYLOADS/L4"
    ).resolve()
    manifest_path = cache_root / "CACHE_MANIFEST.json"
    manifest_hash = parallel_runtime.sha256_file(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_hashes = {
        role: manifest[f"{role}_sha256"]
        for role in ("method", "builder", "consumer", "preflight")
    }
    started = time.perf_counter()
    context = hostile.CacheContext(
        4, cache_root, manifest, manifest_hash, source_hashes, started
    )
    try:
        hostile.legacy.configure(4, context, started)
        journal = EvidenceJournal(case_root / "evidence", "hostile")
        _rough, _sharp, comparison, diagnostic, resource = run_hostile_rough_and_sharp(
            length=4,
            cache_root=cache_root,
            cache_manifest_sha256=manifest_hash,
            workspace=case_root / "workspace",
            evidence=journal,
            deadline_monotonic=time.monotonic() + 300.0,
            max_workers=2,
        )
        require_resolved(diagnostic)
        context.reauthenticate()
    finally:
        hostile.legacy.CACHE = None
        hostile.v3.EXECUTION_STARTED = None
        context.close()
    checkpoint_count = len(list((case_root / "evidence").rglob("*.json")))
    required = {
        "ROUGH_SUMMARY",
        "SHARP_SUMMARY",
        "PRE_GATE_COMPARISON",
        "RUN_COMPLETE",
    }
    labels = {
        json.loads(path.read_text(encoding="utf-8"))["label"]
        for path in (case_root / "evidence").rglob("*.json")
    }
    if comparison.get("resolved") is not True or not required <= labels:
        raise AssertionError("hostile normal L4 persistence gateway did not resolve")
    return {
        "branch": "hostile",
        "status": "PASS",
        "comparison_resolved": comparison["resolved"],
        "comparison_classification": comparison["classification"],
        "checkpoint_count": checkpoint_count,
        "required_checkpoint_labels": sorted(required),
        "raw_metrics": diagnostic["raw_metrics"],
        "full_run_progress": resource["full_run_progress"],
        "observed_worker_pids": resource["observed_worker_pids"],
        "evidence_root": str(case_root / "evidence"),
    }


def forced_unresolved_l4(
    rough: dict[str, Any], sharp: dict[str, Any]
) -> dict[str, Any]:
    case_root = ARTIFACT_ROOT / "forced_unresolved"
    journal = EvidenceJournal(case_root / "evidence", "target")
    forced_sharp = copy.deepcopy(sharp)
    forced_sharp["rows"][0]["transport_node_residual_l1"] = 1.0
    forced_comparison = target.v004.sealed.summarize(4, rough, forced_sharp)
    journal.history("rough", rough)
    journal.history("sharp", forced_sharp)
    diagnostic = persist_target_before_gate(
        journal, 4, rough, forced_sharp, forced_comparison
    )
    caught = None
    try:
        require_resolved(diagnostic)
    except UnresolvedComparison as error:
        caught = str(error)
        journal.write(
            "lifecycle",
            "EXPECTED_GATE_REFUSAL",
            {"error_type": type(error).__name__, "error": str(error)},
        )
    if caught is None:
        raise AssertionError("forced unresolved L4 comparison was not refused")
    failed = [row for row in diagnostic["predicates"] if row["passed"] is not True]
    if [row["name"] for row in failed] != ["maximum_transport_node_residual_l1"]:
        raise AssertionError("forced unresolved gateway failed the wrong predicate")
    comparison_paths = list((case_root / "evidence/comparison").glob("*.json"))
    if len(comparison_paths) != 1:
        raise AssertionError("pre-gate comparison was not durably persisted")
    return {
        "case": "forced_unresolved_comparison",
        "status": "PASS",
        "gate_refusal": caught,
        "comparison_persisted_before_gate": True,
        "comparison_checkpoint": str(comparison_paths[0]),
        "failed_predicates": failed,
        "raw_metrics": diagnostic["raw_metrics"],
    }


def independent_branch_survival_l4() -> dict[str, Any]:
    case_root = ARTIFACT_ROOT / "independent_branch_survival"
    case_root.mkdir(parents=True, exist_ok=False)
    supervision = io.StringIO()
    with redirect_stdout(supervision):
        return_codes = supervise(
            commands={
                "forced_failure": [sys.executable, str(FIXTURE), "forced_failure"],
                "survivor": [sys.executable, str(FIXTURE), "survivor"],
            },
            log_root=case_root / "branch_logs",
            cwd=ROOT,
            environment=branch_environment(),
        )
    transcript = supervision.getvalue()
    survivor_log = (case_root / "branch_logs/survivor.log").read_text(encoding="utf-8")
    failure_log = (case_root / "branch_logs/forced_failure.log").read_text(
        encoding="utf-8"
    )
    if return_codes != {"forced_failure": 7, "survivor": 0}:
        raise AssertionError(f"unexpected independent return codes: {return_codes}")
    if "L4_FIXTURE_SURVIVOR_COMPLETE" not in survivor_log:
        raise AssertionError("surviving sibling did not reach its terminal record")
    if "branch=forced_failure return_code=7 sibling_continues=True" not in transcript:
        raise AssertionError("launcher did not observe failed branch while sibling lived")
    return {
        "case": "one_branch_failure",
        "status": "PASS",
        "return_codes": return_codes,
        "failed_branch_log": failure_log.splitlines(),
        "survivor_branch_log": survivor_log.splitlines(),
        "launcher_transcript": transcript.splitlines(),
        "sibling_survived_to_completion": True,
    }


def main() -> int:
    if ARTIFACT_ROOT.exists() or ARTIFACT_ROOT.is_symlink():
        raise RuntimeError(f"L4 artifact allocation is not fresh: {ARTIFACT_ROOT}")
    if LOG_ROOT.exists() or LOG_ROOT.is_symlink():
        raise RuntimeError(f"L4 log allocation is not fresh: {LOG_ROOT}")
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=False)
    LOG_ROOT.mkdir(parents=True, exist_ok=False)
    print("L4_GATEWAYS_START version=V002 full_l12_started=false", flush=True)
    rough, sharp, target_normal = normal_target_l4()
    hostile_normal = normal_hostile_l4()
    normal = {
        "case": "normal_completion",
        "status": "PASS",
        "branches": {"target": target_normal, "hostile": hostile_normal},
    }
    normal_log = write_log("normal_completion.log", json.dumps(normal, indent=2) + "\n")
    unresolved = forced_unresolved_l4(rough, sharp)
    unresolved_log = write_log(
        "forced_unresolved_comparison.log", json.dumps(unresolved, indent=2) + "\n"
    )
    survival = independent_branch_survival_l4()
    survival_log = write_log(
        "one_branch_failure.log", json.dumps(survival, indent=2) + "\n"
    )
    summary = {
        "schema": "L12_PROCESS_PARALLEL_V002_L4_GATEWAY_RESULT",
        "classification": "PASS_L4_V002_GATEWAYS",
        "full_l12_started": False,
        "cases": [normal, unresolved, survival],
        "logs": [normal_log, unresolved_log, survival_log],
    }
    write_log("SUMMARY.log", json.dumps(summary, indent=2) + "\n")
    print("L4_GATEWAYS_COMPLETE classification=PASS_L4_V002_GATEWAYS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
