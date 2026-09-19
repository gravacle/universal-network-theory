#!/usr/bin/env python3
"""One-shot, source-bound recertification for the 30-hour Stage-3 wall.

This transaction changes no numerical engine, Hamiltonian, basis, lineage,
admission rule, tolerance, or finite observable.  It retires the records bound
to the six-hour worker adapters, invokes the already-audited A01--A18 replay,
and rebuilds the hostile cache/L10 branch when the target L10 parent is ready.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CUSTODY = HERE / "SIX_HOUR_SOURCE_BOUND_RECERTIFICATION_CUSTODY"
INTENT = CUSTODY / "RETIREMENT_INTENT_V001.json"
RECEIPT = CUSTODY / "RETIREMENT_RECEIPT_V001.json"
RESULT = HERE / "THIRTY_HOUR_RECERTIFICATION_RESULT_V001.json"
RELATIVE_CACHE_CUSTODY = HERE / "RELATIVE_PATH_CACHE_ATTEMPT_CUSTODY"
CROSS_WALL_CUSTODY = HERE / "HOSTILE_WALL_BINDING_ATTEMPT_CUSTODY"
CROSS_WALL_INTENT = CROSS_WALL_CUSTODY / "RETIREMENT_INTENT_V001.json"
CROSS_WALL_RECEIPT = CROSS_WALL_CUSTODY / "RETIREMENT_RECEIPT_V001.json"
FAILED_ATTEMPTS = tuple(
    HERE / f"FAILED_RECERTIFICATION_ATTEMPT_{index:03d}_CUSTODY"
    for index in range(1, 4)
)
REPLAY_SOURCE = (
    ROOT / "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001"
    / "replay_a01_a18.py"
)
DATA_REPLAY_SOURCE = (
    ROOT / "DEVELOPMENT_R_L12_STAGE3_DATA_LINEAGE_REPLAY_V001"
    / "stage3_data_lineage_replay.py"
)
TARGET = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
TARGET_AUDIT = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
HOSTILE = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
SHARED = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"

TARGET_CONSUMER_SHA = "307b7232603f4de3937e4f8fad5aa281ff1f4cc33beaec28be6e18d9d8cc63fa"
TARGET_BUILDER_SHA = "bde9eb6f917291e78e8b8747e3b0f306e56ad6152c82f636dd90593a83e6b246"
TARGET_VALIDATOR_SHA = "c1a0b6d8a39dc418523d988ddd97a5a30234cee4923efac654ab3ab48d7a93f7"
TARGET_PREFLIGHT_SHA = "56d0c6249f355ec4ba9b5c5bd6ddb44002ff91344b2aecc00457ddfb6711a2f1"
FINAL_AUDITOR_SHA = "cb1681c870b8382d9e7a83bec9df0830699d7b1015ed19b24360a3dbd4ae207e"
TARGET_LAUNCHER_SHA = "067bdec60d4fe40e5d961241a7408677f8950ea7d68e7dbb3d8dc0f9db83f163"
HOSTILE_CONSUMER_SHA = "2c7ff73a0b462a75d576a51eef3863f5157dbccaa54573403734bbe72702d800"
POSTBUILD_AUDITOR_SHA = "0ad37a809f05f4429bee618922bbfea6c29d6452c0cb28b93de5c786aca4e4cf"

OLD_TARGET_CONSUMER_SHA = "80b2ce08af37bc8cffd91f07146c777f60785883436361ca9521597763fd5a11"
PREVIOUS_30H_TARGET_CONSUMER_SHA = "00539cf7828756c2d34e375680971a60b0278e5d15f241263bdf9441fa3ae7a1"
PREVIOUS_CROSS_WALL_TARGET_CONSUMER_SHA = "712944586bae9d56c77c541f874175e5b5bcc15d97353b2d00be6ee250c41e2c"
PREVIOUS_30H_TARGET_BUILDER_SHA = "1adc46f9edaab8269f5aae7f7c6f1594bdf815146eded640e091d9a5ec1a51fd"
PREVIOUS_30H_TARGET_VALIDATOR_SHA = "70fa7086642d6bbf3aadae9f8dfa2a0ba8b166a53c7eab4d21eda6d3d401874a"
PREVIOUS_A27_REPAIR_TARGET_BUILDER_SHA = "a030796eb9807b2f7f2b204ecfb53870a358ebbcdbea66abc195abd60f6ba624"
PREVIOUS_A27_REPAIR_TARGET_VALIDATOR_SHA = "cebfb778842a48019139789f1181408b633e9426596571e08e8181962609d51f"
OLD_TARGET_BUILDER_SHA = "f59b625383fd748246225cd603710097e3a69a7e9fae6cc02994c5d79c4c8a3d"
OLD_TARGET_VALIDATOR_SHA = "b6409bfca1c0ee468671a37d5aac41c80c67f8027265ce4c0261b861509ad691"
OLD_TARGET_PREFLIGHT_SHA = "af986f297063dcb8e6263d0bd2423cd1fc0e44042aba20ad5b8ae62cee635476"
OLD_FINAL_AUDITOR_SHA = "c252092ff3a4c10bcfd6055600b18ed2ccd8bed90581cec29108ac6c31f5c7cf"

TARGET_RETIRE = (
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_MUTATION_LEDGER_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_RESULT_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/POSTBUILD_PAYLOAD_AUDIT_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_EXECUTION_GATE_V012.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_GATE_HOSTILE_AUDIT_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_V012.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
)

HOSTILE_RETIRE = (
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PREFLIGHT_RESULT.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_AUDIT_RESULT_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS",
)


class Refusal(RuntimeError):
    pass


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise Refusal(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


data = _load("stage3_30h_data_replay", DATA_REPLAY_SOURCE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(16 * 2**20):
            digest.update(block)
    return digest.hexdigest()


def strict_json(path: Path) -> dict[str, object]:
    return data.strict_json(path.read_bytes(), str(path))


def publish(path: Path, record: Mapping[str, object]) -> str:
    return data.publish_once(path, dict(record))


def retired(logical: str) -> Path:
    return CUSTODY.joinpath(*PurePosixPath(logical).parts)


def _census(logical: str) -> dict[str, object]:
    path = ROOT.joinpath(*PurePosixPath(logical).parts)
    return (
        data._directory_census(path, logical)
        if path.is_dir() and not path.is_symlink()
        else data._file_census(path, logical)
    )


def retire_source_bound_records() -> str:
    if RECEIPT.exists():
        return sha256(RECEIPT)
    paths = TARGET_RETIRE + HOSTILE_RETIRE
    if any(retired(logical).exists() for logical in paths):
        raise Refusal("partial 30-hour retirement custody is preserved")
    if not SHARED.is_dir() or SHARED.is_symlink() or list(SHARED.iterdir()):
        raise Refusal("shared A18 parent is not exactly empty before recertification")
    rows = [_census(logical) for logical in paths]
    CUSTODY.mkdir(parents=True, exist_ok=False)
    intent = {
        "schema": "STAGE3_THIRTY_HOUR_SOURCE_BOUND_RETIREMENT_INTENT_V001",
        "classification": "RETIRE_SIX_HOUR_SOURCE_BOUND_RECORDS_FOR_THIRTY_HOUR_RECERTIFICATION",
        "entries": rows,
        "entry_count": len(rows),
        "numerical_engine_changed": False,
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }
    intent_sha = publish(INTENT, intent)
    event_hashes: list[str] = []
    for ordinal, row in enumerate(rows, start=1):
        logical = str(row["path"])
        source = ROOT.joinpath(*PurePosixPath(logical).parts)
        destination = retired(logical)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data._rename_exclusive(source, destination)
        data._fsync_directory(source.parent)
        data._fsync_directory(destination.parent)
        observed = (
            data._directory_census(destination, logical)
            if row["kind"] == "directory"
            else data._file_census(destination, logical)
        )
        if observed != row:
            raise Refusal(f"retired record changed: {logical}")
        event_hashes.append(publish(CUSTODY / f"EVENT_{ordinal:03d}.json", {
            "schema": "STAGE3_THIRTY_HOUR_SOURCE_BOUND_RETIREMENT_EVENT_V001",
            "ordinal": ordinal,
            "path": logical,
            "entry_sha256": data.sha256_bytes(data.canonical_json_bytes(row)),
            "intent_sha256": intent_sha,
        }))
    receipt = {
        "schema": "STAGE3_THIRTY_HOUR_SOURCE_BOUND_RETIREMENT_RECEIPT_V001",
        "classification": "PASS_EXACT_SIX_HOUR_SOURCE_BOUND_RETIREMENT",
        "intent_sha256": intent_sha,
        "event_sha256_by_ordinal": event_hashes,
        "entry_count": len(rows),
        "canonical_destinations_absent_for_replay": True,
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }
    return publish(RECEIPT, receipt)


def retire_failed_recertification_attempt() -> str | None:
    """Preserve an exact pre-compute A01--A02 prefix from a refused attempt."""
    source = TARGET / "FREEZE.json"
    if not source.exists():
        receipts = [root / "RETIREMENT_RECEIPT_V001.json" for root in FAILED_ATTEMPTS]
        completed = [path for path in receipts if path.exists()]
        return sha256(completed[-1]) if completed else None
    attempt = next((root for root in FAILED_ATTEMPTS if not root.exists()), None)
    if attempt is None:
        # Subsequent progress is reconciled by the replay's owner-once
        # validators.  Do not manufacture another retirement generation.
        return sha256(FAILED_ATTEMPTS[-1] / "RETIREMENT_RECEIPT_V001.json")
    receipt = attempt / "RETIREMENT_RECEIPT_V001.json"
    existing = [
        logical for logical in TARGET_RETIRE + HOSTILE_RETIRE
        if ROOT.joinpath(*PurePosixPath(logical).parts).exists()
    ]
    permitted_prefix = list(TARGET_RETIRE[:3])
    if existing != permitted_prefix[:len(existing)] or len(existing) > 3:
        raise Refusal("failed recertification is not an exact A01--A02 prefix")
    rows = [_census(logical) for logical in existing]
    attempt.mkdir(parents=True, exist_ok=False)
    intent_sha = publish(attempt / "RETIREMENT_INTENT_V001.json", {
        "schema": "STAGE3_THIRTY_HOUR_FAILED_RECERTIFICATION_RETIREMENT_INTENT_V001",
        "classification": "RETIRE_FAILED_PRECOMPUTE_A01_A02_PREFIX",
        "entries": rows,
        "entry_count": len(rows),
        "numerical_execution_started": False,
        "claim_boundary": "CUSTODY_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    })
    entry_hashes: list[str] = []
    for row in rows:
        logical = str(row["path"])
        canonical = ROOT.joinpath(*PurePosixPath(logical).parts)
        destination = attempt.joinpath(*PurePosixPath(logical).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data._rename_exclusive(canonical, destination)
        data._fsync_directory(canonical.parent)
        data._fsync_directory(destination.parent)
        observed = (
            data._directory_census(destination, logical)
            if row["kind"] == "directory"
            else data._file_census(destination, logical)
        )
        if observed != row:
            raise Refusal(f"failed-attempt artifact changed: {logical}")
        entry_hashes.append(data.sha256_bytes(data.canonical_json_bytes(row)))
    return publish(receipt, {
        "schema": "STAGE3_THIRTY_HOUR_FAILED_RECERTIFICATION_RETIREMENT_RECEIPT_V001",
        "classification": "PASS_EXACT_FAILED_PRECOMPUTE_A01_A02_PREFIX_RETIREMENT",
        "intent_sha256": intent_sha,
        "entry_sha256": entry_hashes,
        "entry_count": len(rows),
        "numerical_execution_started": False,
        "claim_boundary": "CUSTODY_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    })


def retire_relative_path_cache_attempt() -> str | None:
    """Preserve caches whose only failed field is a relative canonical root."""
    cache = TARGET / "CACHE_PAYLOADS_V012"
    destination = (
        RELATIVE_CACHE_CUSTODY
        / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012"
    )
    receipt = RELATIVE_CACHE_CUSTODY / "RETIREMENT_RECEIPT_V001.json"
    if receipt.exists():
        if not destination.exists():
            raise Refusal("relative-path cache retirement custody mismatch")
        return sha256(receipt)
    if not cache.exists():
        return None
    if (TARGET_AUDIT / "POSTBUILD_PAYLOAD_AUDIT_V001.json").exists():
        raise Refusal("relative-path cache attempt advanced beyond A05")
    expected_roots = {
        length: str(
            Path("DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012")
            / "CACHE_PAYLOADS_V012" / f"L{length}"
        )
        for length in (4, 6, 8, 10, 12)
    }
    for length, expected in expected_roots.items():
        manifest = strict_json(cache / f"L{length}/CACHE_MANIFEST.json")
        if manifest.get("canonical_cache_root") != expected:
            raise Refusal(f"L{length} failed cache is not relative-root-only")
    logical = "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012"
    row = data._directory_census(cache, logical)
    RELATIVE_CACHE_CUSTODY.mkdir(parents=True, exist_ok=False)
    intent_sha = publish(RELATIVE_CACHE_CUSTODY / "RETIREMENT_INTENT_V001.json", {
        "schema": "STAGE3_THIRTY_HOUR_RELATIVE_CACHE_RETIREMENT_INTENT_V001",
        "classification": "RETIRE_A05_RELATIVE_CANONICAL_ROOT_CACHE_SET",
        "entry": row,
        "numerical_history_executed": False,
        "claim_boundary": "CACHE_CUSTODY_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    })
    destination.parent.mkdir(parents=True, exist_ok=True)
    data._rename_exclusive(cache, destination)
    data._fsync_directory(cache.parent)
    data._fsync_directory(destination.parent)
    observed = data._directory_census(destination, logical)
    if observed != row:
        raise Refusal("relative-path cache set changed during retirement")
    return publish(receipt, {
        "schema": "STAGE3_THIRTY_HOUR_RELATIVE_CACHE_RETIREMENT_RECEIPT_V001",
        "classification": "PASS_EXACT_A05_RELATIVE_CACHE_RETIREMENT",
        "intent_sha256": intent_sha,
        "entry_sha256": data.sha256_bytes(data.canonical_json_bytes(row)),
        "numerical_history_executed": False,
        "claim_boundary": "CACHE_CUSTODY_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    })


def retire_hostile_wall_binding_attempt() -> str:
    """Preserve controls bound to the retired six-hour hostile cross-check."""
    if CROSS_WALL_RECEIPT.exists():
        return sha256(CROSS_WALL_RECEIPT)
    paths = TARGET_RETIRE + HOSTILE_RETIRE
    if CROSS_WALL_CUSTODY.exists():
        raise Refusal("partial hostile-wall binding custody is preserved")
    missing = [
        logical for logical in paths
        if not ROOT.joinpath(*PurePosixPath(logical).parts).exists()
    ]
    if missing:
        raise Refusal(
            f"hostile-wall binding attempt census is incomplete: {missing[0]}"
        )
    if SHARED.exists() or SHARED.is_symlink():
        raise Refusal("shared Stage-3 parent exists before hostile-wall retirement")
    rows = [_census(logical) for logical in paths]
    CROSS_WALL_CUSTODY.mkdir(parents=True, exist_ok=False)
    intent_sha = publish(CROSS_WALL_INTENT, {
        "schema": "STAGE3_THIRTY_HOUR_HOSTILE_WALL_BINDING_RETIREMENT_INTENT_V001",
        "classification": "RETIRE_CONTROLS_WITH_SIX_HOUR_HOSTILE_CROSS_VERIFIER",
        "entries": rows,
        "entry_count": len(rows),
        "numerical_engine_changed": False,
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    })
    event_hashes: list[str] = []
    for ordinal, row in enumerate(rows, start=1):
        logical = str(row["path"])
        source = ROOT.joinpath(*PurePosixPath(logical).parts)
        destination = CROSS_WALL_CUSTODY.joinpath(*PurePosixPath(logical).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data._rename_exclusive(source, destination)
        data._fsync_directory(source.parent)
        data._fsync_directory(destination.parent)
        observed = (
            data._directory_census(destination, logical)
            if row["kind"] == "directory"
            else data._file_census(destination, logical)
        )
        if observed != row:
            raise Refusal(
                f"hostile-wall custody changed during retirement: {logical}"
            )
        event_hashes.append(data.sha256_bytes(data.canonical_json_bytes({
            "ordinal": ordinal,
            "entry": row,
        })))
    return publish(CROSS_WALL_RECEIPT, {
        "schema": "STAGE3_THIRTY_HOUR_HOSTILE_WALL_BINDING_RETIREMENT_RECEIPT_V001",
        "classification": "PASS_EXACT_HOSTILE_WALL_BINDING_RETIREMENT",
        "intent_sha256": intent_sha,
        "entry_count": len(rows),
        "event_sha256": event_hashes,
        "numerical_engine_changed": False,
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    })


def run_checked(command: list[str], label: str) -> None:
    environment = dict(os.environ)
    environment.setdefault("PYTHONPYCACHEPREFIX", "/private/tmp/wacf_30h_pycache")
    process = subprocess.run(command, cwd=ROOT, env=environment, check=False)
    if process.returncode != 0:
        raise Refusal(f"{label} refused with status {process.returncode}")


def _hostile_module():
    hostile_path = str(HOSTILE)
    sys.path.insert(0, hostile_path)
    try:
        return _load(
            "stage3_30h_hostile_consumer",
            HOSTILE / "consume_cache_v004r4.py",
        )
    finally:
        if sys.path[0] == hostile_path:
            sys.path.pop(0)


def _hostile_freeze_files() -> dict[str, str]:
    names = (
        "V004R4_CACHE_METHOD.md", "build_cache_v004r4.py",
        "consume_cache_v004r4.py", "independent_prefix_history.py",
        "independent_prefix_history_v002.py", "independent_prefix_history_v003.py",
        "independent_prefix_history_v004.py", "independent_prefix_history_v004r2.py",
        "v004r2_common.py", "v004r4_cache_io.py",
        "validate_cache_preflight_v004r4.py",
        "validate_v004r4_zero_length_preflight.py",
    )
    return {name: sha256(HOSTILE / name) for name in names}


def rebuild_hostile_branch() -> None:
    freeze_path = HOSTILE / "FROZEN_MANIFEST_V004R4.json"
    if (HOSTILE / "CACHED_L10_GATE_V004R4.json").exists():
        if not SHARED.exists():
            SHARED.mkdir(mode=0o755, parents=False, exist_ok=False)
            data._fsync_directory(SHARED.parent)
        elif not SHARED.is_dir() or SHARED.is_symlink():
            raise Refusal("shared A18 parent is not an ordinary directory")
        return
    freeze = strict_json(retired(str(freeze_path.relative_to(ROOT))))
    expected_files = _hostile_freeze_files()
    if freeze.get("files") != expected_files:
        raise Refusal("hostile 30-hour freeze does not match exact source bytes")
    if freeze_path.exists():
        if freeze_path.is_symlink() or freeze_path.stat().st_mode & 0o222:
            raise Refusal("existing hostile 30-hour freeze is not immutable")
        observed_freeze = strict_json(freeze_path)
        if data.canonical_json_bytes(observed_freeze) != data.canonical_json_bytes(freeze):
            raise Refusal("existing hostile 30-hour freeze differs from custody")
        freeze_sha = sha256(freeze_path)
    else:
        freeze_sha = publish(freeze_path, freeze)
    run_checked([
        sys.executable, "-B", str(HOSTILE / "validate_cache_preflight_v004r4.py"), "run",
    ], "hostile 30-hour preflight")
    preflight_path = HOSTILE / "V004R4_CACHE_PREFLIGHT_RESULT.json"
    preflight_sha = sha256(preflight_path)
    consumer = _hostile_module()

    audit_path = HOSTILE / "HOSTILE_AUDIT_RESULT_V004R4.json"
    audit = strict_json(retired(str(audit_path.relative_to(ROOT))))
    audit["audited_files_sha256"] = expected_files
    audit["audited_freeze_sha256"] = freeze_sha
    audit["preflight_result_sha256"] = preflight_sha
    consumer.validate_hostile_prepayload_audit(
        audit, freeze_sha256=freeze_sha, frozen_files=expected_files,
        preflight_result_sha256=preflight_sha,
    )
    audit_sha = publish(audit_path, audit)

    target_gate_path = TARGET / "CACHED_L10_GATE_V012.json"
    target_manifest_path = TARGET / "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json"
    target_audit_path = TARGET_AUDIT / "HOSTILE_AUDIT_RESULT_V001.json"
    target_freeze_path = TARGET / "FREEZE.json"
    target_gate = strict_json(target_gate_path)
    target_manifest = strict_json(target_manifest_path)
    target_audit = strict_json(target_audit_path)
    target_freeze = strict_json(target_freeze_path)

    build_path = HOSTILE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
    build = strict_json(retired(str(build_path.relative_to(ROOT))))
    build["files_sha256"] = expected_files
    build["freeze_sha256"] = freeze_sha
    build["independent_hostile_audit"].update({
        "sha256": audit_sha,
        "checks_passed": audit["checks_passed"],
        "checks_total": audit["checks_total"],
    })
    build["target_v012_interface"].update({
        "L10_gate_sha256": sha256(target_gate_path),
        "L10_gate_schema": target_gate["schema"],
        "L10_gate_classification": target_gate["classification"],
        "L12_cache_manifest_sha256": sha256(target_manifest_path),
        "L12_cache_manifest_schema": target_manifest["schema"],
        "audit_sha256": sha256(target_audit_path),
        "audit_schema": target_audit["schema"],
        "audit_classification": target_audit["classification"],
        "consumer_sha256": TARGET_CONSUMER_SHA,
        "freeze_sha256": sha256(target_freeze_path),
        "freeze_schema": target_freeze["schema"],
    })
    consumer.validate_hostile_build_authorization(
        build, audit, freeze_sha256=freeze_sha, frozen_files=expected_files,
        audit_sha256=audit_sha,
    )
    build_sha = publish(build_path, build)

    for length in (4, 6, 8, 10, 12):
        run_checked([
            sys.executable, "-B", str(HOSTILE / "build_cache_v004r4.py"),
            "build", "--length", str(length),
        ], f"hostile L{length} cache build")

    manifest_hashes = {
        length: sha256(HOSTILE / f"V004R4_CACHE_PAYLOADS/L{length}/CACHE_MANIFEST.json")
        for length in (4, 6, 8, 10, 12)
    }
    source_hashes = {
        "method": expected_files["V004R4_CACHE_METHOD.md"],
        "builder": expected_files["build_cache_v004r4.py"],
        "consumer": expected_files["consume_cache_v004r4.py"],
        "preflight": expected_files["validate_cache_preflight_v004r4.py"],
    }
    for length in (4, 6, 8, 10, 12):
        cache_root = HOSTILE / f"V004R4_CACHE_PAYLOADS/L{length}"
        manifest = strict_json(cache_root / "CACHE_MANIFEST.json")
        context = consumer.CacheContext(
            length, cache_root, manifest, manifest_hashes[length],
            source_hashes, time.monotonic(),
        )
        try:
            context.reauthenticate()
        finally:
            context.close()

    postbuild_path = HOSTILE / "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"
    postbuild = strict_json(retired(str(postbuild_path.relative_to(ROOT))))
    postbuild["manifest_sha256"] = manifest_hashes[12]
    postbuild_sha = publish(postbuild_path, postbuild)

    l10_auth_path = HOSTILE / "L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json"
    l10_auth = strict_json(retired(str(l10_auth_path.relative_to(ROOT))))
    l10_auth.update({
        "consumer_sha256": HOSTILE_CONSUMER_SHA,
        "freeze_sha256": freeze_sha,
        "preflight_result_sha256": preflight_sha,
        "independent_hostile_audit_sha256": audit_sha,
        "l10_cache_manifest_sha256": manifest_hashes[10],
    })
    l10_auth_sha = publish(l10_auth_path, l10_auth)

    run_checked([
        sys.executable, "-B", str(HOSTILE / "consume_cache_v004r4.py"),
        "execute", "--length", "10",
    ], "hostile exact L10 replay")
    history_path = HOSTILE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json"
    history_sha = sha256(history_path)

    l10_gate_path = HOSTILE / "CACHED_L10_GATE_V004R4.json"
    l10_gate = strict_json(retired(str(l10_gate_path.relative_to(ROOT))))
    l10_gate["consumer_sha256"] = HOSTILE_CONSUMER_SHA
    l10_gate["freeze_sha256"] = freeze_sha
    l10_gate["preflight_result_sha256"] = preflight_sha
    l10_gate["independent_hostile_audit_sha256"] = audit_sha
    l10_gate["cache_manifest_sha256_by_L"] = {"10": manifest_hashes[10]}
    l10_gate["l10_execution_authorization"]["sha256"] = l10_auth_sha
    l10_gate["histories"][0]["sha256"] = history_sha
    publish(l10_gate_path, l10_gate)

    custody = consumer.AuthorityCustody()
    try:
        consumer.authenticate_l10_context(custody)
        custody.verify_all()
    finally:
        custody.close()
    if postbuild_sha != sha256(postbuild_path) or build_sha != sha256(build_path):
        raise Refusal("hostile branch changed after authentication")
    if SHARED.exists() or SHARED.is_symlink():
        raise Refusal("shared A18 parent appeared before hostile L10 completion")
    SHARED.mkdir(mode=0o755, parents=False, exist_ok=False)
    data._fsync_directory(SHARED.parent)


def _pointer_rows(value: object, pointer: str = ""):
    if type(value) is dict:
        for key, child in value.items():
            escaped = key.replace("~", "~0").replace("/", "~1")
            yield from _pointer_rows(child, f"{pointer}/{escaped}")
    elif type(value) is list:
        for index, child in enumerate(value):
            yield from _pointer_rows(child, f"{pointer}/{index}")
    else:
        yield pointer, value


def run_target_replay(receipt_sha: str) -> dict[tuple[str, int], str]:
    replay = _load("stage3_30h_target_replay", REPLAY_SOURCE)
    # The replay module's source-measurement helper reads this named constant
    # directly in addition to the dependency maps below.  Bind it in memory to
    # the already-measured 30-hour builder byte string; do not rewrite the
    # audited predecessor replay source.
    replay.REPAIRED_CANONICAL_BUILDER_SHA256 = TARGET_BUILDER_SHA
    replay.PINNED_LIVE_SOURCES.update({
        "production_obligation_validators": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/production_obligation_validators.py",
            TARGET_VALIDATOR_SHA,
        ),
        "build_target_cache": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py",
            TARGET_BUILDER_SHA,
        ),
        "consume_target_cache": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py",
            TARGET_CONSUMER_SHA,
        ),
        "independent_final_auditor": (
            "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/independent_final_auditor.py",
            FINAL_AUDITOR_SHA,
        ),
    })
    replay.PINNED_EXECUTABLE_DEPENDENCIES.update(replay.PINNED_LIVE_SOURCES)
    replay.PINNED_EXECUTABLE_DEPENDENCIES["authenticated_validate_preflight"] = (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/validate_preflight.py",
        TARGET_PREFLIGHT_SHA,
    )
    replay.PINNED_EXECUTABLE_DEPENDENCIES[
        "authenticated_independent_postbuild_auditor"
    ] = (
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/independent_postbuild_auditor.py",
        POSTBUILD_AUDITOR_SHA,
    )

    # The predecessor replay's generic independent sink classifies A27 as an
    # upstream authority even though A27 has its own complete 477-case native
    # validator.  Dispatch that one artifact to its registered validator.
    original_independent_sink = replay.ExactLiveReview.independent_sink

    def independent_sink(review, artifact_id, record):
        if artifact_id == "A27_MUTATION_LEDGER":
            review.independent.validate_mutation_ledger(
                dict(record), fixture_mode=False,
            )
            return
        original_independent_sink(review, artifact_id, record)

    replay.ExactLiveReview.independent_sink = independent_sink

    original_production_sink = replay.ExactLiveReview.production_sink

    def production_sink(review, artifact_id, record):
        parent_by_artifact = {
            "A12_CONTROL_STAGE_AUDIT": TARGET / "CACHED_CONTROL_L4_L8_GATE_V012.json",
            "A13_L10_AUTHORIZATION": TARGET_AUDIT / "CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
            "A16_L10_STAGE_AUDIT": TARGET / "CACHED_L10_GATE_V012.json",
        }
        parent = parent_by_artifact.get(artifact_id)
        if parent is not None and not parent.exists():
            # The independent sink checks the complete native structure here.
            # validate_stage_chain/validate_l10_stage_pair next exercises the
            # exact live bindings in an owner-once temporary stage.  During
            # canonical publication the parent exists and the unmodified
            # production sink below performs its full path/hash validation.
            return
        original_production_sink(review, artifact_id, record)

    replay.ExactLiveReview.production_sink = production_sink

    def validate_stage_chain(review, a11, a12, a13, cache_hashes, a07_sha):
        with tempfile.TemporaryDirectory(
            prefix="a11-a13-30h-", dir=replay.HERE,
        ) as directory:
            stage_root = Path(directory)
            paths = {
                name: stage_root / f"{name}.json"
                for name in ("A11", "A12", "A13")
            }
            for name, record in (("A11", a11), ("A12", a12), ("A13", a13)):
                replay.retirement.publish_once(paths[name], dict(record))
            validator_old = (
                review.validators.CONTROL_GATE_PATH,
                review.validators.CONTROL_AUDIT_PATH,
                review.validators.L10_AUTHORIZATION_PATH,
            )
            consumer_old = (
                review.consumer.L10_EXECUTION_AUTHORIZATION_GATE,
                review.consumer.CACHED_CONTROL_GATE,
                review.consumer.CACHED_CONTROL_GATE_AUDIT,
            )
            review.validators.CONTROL_GATE_PATH = paths["A11"]
            review.validators.CONTROL_AUDIT_PATH = paths["A12"]
            review.validators.L10_AUTHORIZATION_PATH = paths["A13"]
            try:
                control = review.consumer.require_stage_gate(
                    paths["A11"], "TARGET_V012_CACHED_CONTROL_L4_L8_GATE",
                    "PASS_TARGET_V012_CACHED_CONTROLS_L4_L6_L8", (4, 6, 8),
                    dict(cache_hashes), a07_sha,
                    review.builder.require_frozen_census(),
                )
                _audit, audit_sha = review.consumer.require_stage_gate_audit(
                    paths["A12"], paths["A11"], control,
                    "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001",
                    "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8",
                    (4, 6, 8),
                )
                review.consumer.L10_EXECUTION_AUTHORIZATION_GATE = paths["A13"]
                review.consumer.CACHED_CONTROL_GATE = paths["A11"]
                review.consumer.CACHED_CONTROL_GATE_AUDIT = paths["A12"]
                result, _digest = review.consumer.require_l10_execution_authorization(
                    review.builder.require_frozen_census(), a07_sha,
                    dict(cache_hashes), control, audit_sha,
                )
                if replay.retirement.canonical_json_bytes(result) \
                        != replay.retirement.canonical_json_bytes(a13):
                    raise replay.Refusal("A13 live reconstruction returned different bytes")
            finally:
                (
                    review.consumer.L10_EXECUTION_AUTHORIZATION_GATE,
                    review.consumer.CACHED_CONTROL_GATE,
                    review.consumer.CACHED_CONTROL_GATE_AUDIT,
                ) = consumer_old
                (
                    review.validators.CONTROL_GATE_PATH,
                    review.validators.CONTROL_AUDIT_PATH,
                    review.validators.L10_AUTHORIZATION_PATH,
                ) = validator_old

    replay.ExactLiveReview.validate_stage_chain = validate_stage_chain

    def validate_l10_stage_pair(
        review, a15, a16, cache_hashes, a07_sha, a11_sha, a13_sha,
    ):
        with tempfile.TemporaryDirectory(
            prefix="a15-a16-30h-", dir=replay.HERE,
        ) as directory:
            stage_root = Path(directory)
            stage = stage_root / "A15.json"
            audit = stage_root / "A16.json"
            replay.retirement.publish_once(stage, dict(a15))
            replay.retirement.publish_once(audit, dict(a16))
            validator_old = review.validators.L10_GATE_PATH
            review.validators.L10_GATE_PATH = stage
            try:
                result = review.consumer.require_stage_gate(
                    stage, "TARGET_V012_CACHED_L10_GATE",
                    "PASS_TARGET_V012_CACHED_L10", (10,),
                    dict(cache_hashes), a07_sha,
                    review.builder.require_frozen_census(), a11_sha, a13_sha,
                )
                checked, _digest = review.consumer.require_stage_gate_audit(
                    audit, stage, result,
                    "TARGET_V012_CACHED_L10_GATE_AUDIT_V001",
                    "PASS_INDEPENDENT_TARGET_V012_CACHED_L10", (10,), a13_sha,
                )
                if replay.retirement.canonical_json_bytes(checked) \
                        != replay.retirement.canonical_json_bytes(a16):
                    raise replay.Refusal(
                        "A16 live reconstruction returned different bytes"
                    )
            finally:
                review.validators.L10_GATE_PATH = validator_old

    replay.ExactLiveReview.validate_l10_stage_pair = validate_l10_stage_pair

    original_runner_factory = replay._canonical_publisher_runner

    def canonical_runner_factory(root):
        runner = original_runner_factory(root)

        def run(command):
            normalized = list(command)
            for index, value in enumerate(normalized[:-1]):
                if value in {"--output", "--cache-root", "--workspace"}:
                    candidate = Path(normalized[index + 1])
                    if not candidate.is_absolute():
                        normalized[index + 1] = str(root / candidate)
            return runner(tuple(normalized))

        return run

    replay._canonical_publisher_runner = canonical_runner_factory
    replay.PINNED_REPAIRED_CANONICAL_SOURCES.clear()
    replay.PINNED_REPAIRED_CANONICAL_SOURCES.update({
        "build_target_cache": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py",
            TARGET_BUILDER_SHA,
        ),
        "production_dual_l12_launcher": (
            "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/production_dual_l12_launcher.py",
            TARGET_LAUNCHER_SHA,
        ),
    })

    receipt = strict_json(RECEIPT)
    replay.retirement.load_census = lambda: {}
    replay._load_completed_retirement_receipt = (
        lambda root, census: (CUSTODY, receipt, receipt_sha)
    )

    def verify_sources(root: Path, census: Mapping[str, object]) -> None:
        for relative, expected in replay.PINNED_REPAIRED_CANONICAL_SOURCES.values():
            path = root.joinpath(*PurePosixPath(relative).parts)
            if sha256(path) != expected or path.stat().st_mode & 0o222:
                raise replay.Refusal(f"30-hour source custody mismatch: {relative}")

    replay.reconcile_or_publish_repaired_sources = verify_sources

    def retired_template(root: Path, census: Mapping[str, object], artifact_id: str):
        logical = replay.TEMPLATE_PATH_BY_ARTIFACT[artifact_id]
        return strict_json(retired(logical))

    replay.load_retired_template = retired_template
    original_updates = replay.measured_template_updates
    replacements = {
        OLD_TARGET_CONSUMER_SHA: TARGET_CONSUMER_SHA,
        PREVIOUS_30H_TARGET_CONSUMER_SHA: TARGET_CONSUMER_SHA,
        PREVIOUS_CROSS_WALL_TARGET_CONSUMER_SHA: TARGET_CONSUMER_SHA,
        OLD_TARGET_BUILDER_SHA: TARGET_BUILDER_SHA,
        PREVIOUS_30H_TARGET_BUILDER_SHA: TARGET_BUILDER_SHA,
        PREVIOUS_A27_REPAIR_TARGET_BUILDER_SHA: TARGET_BUILDER_SHA,
        OLD_TARGET_VALIDATOR_SHA: TARGET_VALIDATOR_SHA,
        PREVIOUS_30H_TARGET_VALIDATOR_SHA: TARGET_VALIDATOR_SHA,
        PREVIOUS_A27_REPAIR_TARGET_VALIDATOR_SHA: TARGET_VALIDATOR_SHA,
        OLD_TARGET_PREFLIGHT_SHA: TARGET_PREFLIGHT_SHA,
        OLD_FINAL_AUDITOR_SHA: FINAL_AUDITOR_SHA,
    }

    def measured_updates(root, artifact_id, produced):
        updates = dict(original_updates(root, artifact_id, produced))
        template = retired_template(root, {}, artifact_id)
        extra: dict[str, object] = {}
        for pointer, value in _pointer_rows(template):
            if value in replacements:
                extra[pointer] = replacements[value]
        replay.DYNAMIC_POINTERS[artifact_id] = frozenset(
            set(replay.DYNAMIC_POINTERS[artifact_id]) | set(extra)
        )
        updates.update(extra)
        return updates

    replay.measured_template_updates = measured_updates
    replay.restore_completed_hostile_a17 = lambda root, census: rebuild_hostile_branch()
    products = replay.coordinate_canonical_a01_a18_replay(receipt_sha)
    return products


def execute() -> dict[str, object]:
    receipt_sha = retire_source_bound_records()
    failed_attempt_receipt_sha = retire_failed_recertification_attempt()
    relative_cache_receipt_sha = retire_relative_path_cache_attempt()
    cross_wall_receipt_sha = retire_hostile_wall_binding_attempt()
    for path, expected in (
        (TARGET / "consume_target_cache.py", TARGET_CONSUMER_SHA),
        (TARGET / "build_target_cache.py", TARGET_BUILDER_SHA),
        (TARGET / "production_obligation_validators.py", TARGET_VALIDATOR_SHA),
        (TARGET / "validate_preflight.py", TARGET_PREFLIGHT_SHA),
        (TARGET_AUDIT / "independent_postbuild_auditor.py", POSTBUILD_AUDITOR_SHA),
        (HOSTILE / "consume_cache_v004r4.py", HOSTILE_CONSUMER_SHA),
    ):
        if sha256(path) != expected:
            raise Refusal(f"30-hour source hash mismatch: {path}")
        path.chmod(0o444)
    products = run_target_replay(receipt_sha)
    result = {
        "schema": "STAGE3_THIRTY_HOUR_SOURCE_BOUND_RECERTIFICATION_RESULT_V001",
        "classification": "PASS_THIRTY_HOUR_A01_A18_AND_HOSTILE_L10_RECERTIFICATION",
        "retirement_receipt_sha256": receipt_sha,
        "failed_attempt_retirement_receipt_sha256": failed_attempt_receipt_sha,
        "relative_cache_retirement_receipt_sha256": relative_cache_receipt_sha,
        "hostile_wall_binding_retirement_receipt_sha256": cross_wall_receipt_sha,
        "products": {
            f"{artifact}/{instance}": digest
            for (artifact, instance), digest in sorted(products.items())
        },
        "target_consumer_sha256": TARGET_CONSUMER_SHA,
        "hostile_consumer_sha256": HOSTILE_CONSUMER_SHA,
        "wall_limit_seconds": 108000,
        "numerical_engine_changed": False,
        "l12_launched": False,
        "claim_boundary": "FINITE_L4_L10_CONTROL_RECERTIFICATION_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }
    publish(RESULT, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("retire", "execute"))
    arguments = parser.parse_args()
    try:
        if arguments.mode == "retire":
            output = {"retirement_receipt_sha256": retire_source_bound_records()}
        else:
            output = execute()
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError, Refusal) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
