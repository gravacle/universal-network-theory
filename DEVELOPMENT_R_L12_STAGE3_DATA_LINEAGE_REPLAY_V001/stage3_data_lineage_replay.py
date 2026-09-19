#!/usr/bin/env python3
"""Fixed-scope Stage-3 hostile lineage replay.

The live path is deliberately narrow: preserve one enumerated stale lineage
set, republish one build gate with four current target hashes, invoke the
already-frozen hostile builder/consumer, reconstruct the L10 gate and A18, and
stop before L12 launch.  Plan, dry-run, and tests never publish or rename.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib
import json
import os
import stat
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath
from typing import Final, Mapping


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
HOSTILE: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
TARGET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
TARGET_AUDIT: Final[Path] = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012"
SHARED: Final[Path] = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
AUDIT_ROOT: Final[Path] = ROOT / "AUDIT_R_L12_STAGE3_DATA_LINEAGE_REPLAY_V001"
CUSTODY: Final[Path] = AUDIT_ROOT / "RETIRED_STALE_LINEAGE_AND_FAILED_LAUNCH_V001"
INTENT: Final[Path] = CUSTODY / "RETIREMENT_INTENT_V001.json"
EVENTS: Final[Path] = CUSTODY / "RETIREMENT_EVENTS_V001"
RECEIPT: Final[Path] = CUSTODY / "RETIREMENT_RECEIPT_V001.json"
RESULT: Final[Path] = AUDIT_ROOT / "DATA_LINEAGE_REPLAY_RESULT_V001.json"

LIVE_AUTHORIZATION: Final[str] = (
    "EXECUTE_EXACT_STAGE3_DATA_LINEAGE_REPLAY_V001__NO_L12_LAUNCH"
)
SEALED_INPUT_COMMIT: Final[str] = "42f1ea3301ccf98802c07f3330d52999385cba0b"

BUILD_GATE: Final[Path] = HOSTILE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
FREEZE: Final[Path] = HOSTILE / "FROZEN_MANIFEST_V004R4.json"
PREFLIGHT_RESULT: Final[Path] = HOSTILE / "V004R4_CACHE_PREFLIGHT_RESULT.json"
PREFLIGHT: Final[Path] = HOSTILE / "validate_cache_preflight_v004r4.py"
PREPAYLOAD_AUDIT: Final[Path] = HOSTILE / "HOSTILE_AUDIT_RESULT_V004R4.json"
BUILDER: Final[Path] = HOSTILE / "build_cache_v004r4.py"
CONSUMER: Final[Path] = HOSTILE / "consume_cache_v004r4.py"
METHOD: Final[Path] = HOSTILE / "V004R4_CACHE_METHOD.md"
POSTBUILD: Final[Path] = HOSTILE / "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"
L10_AUTHORIZATION: Final[Path] = HOSTILE / "L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json"
L10_HISTORY: Final[Path] = HOSTILE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json"
L10_GATE: Final[Path] = HOSTILE / "CACHED_L10_GATE_V004R4.json"
A18: Final[Path] = SHARED / "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
A18_CORE: Final[Path] = (
    ROOT / "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001/replay_a01_a18.py"
)

CURRENT_TARGET_INTERFACE: Final[dict[str, str]] = {
    "freeze_sha256": "a6997822fd2daa2be0079e67d81833f1eac69fe01c6ff0b9188560f2c1234395",
    "freeze_schema": "TARGET_L12_STORAGE_CACHE_FREEZE_V012",
    "audit_sha256": "a50044557c5316d50f3b1e4cfefb035c674321a96147690aa3017b2e01cb2301",
    "audit_schema": "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001",
    "audit_classification": "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE",
    "consumer_sha256": "80b2ce08af37bc8cffd91f07146c777f60785883436361ca9521597763fd5a11",
    "L10_gate_sha256": "20261b35e21d626b61b69a8e29b8dee7c4521bd157aca787aff0fba4524e5ad2",
    "L10_gate_schema": "TARGET_V012_CACHED_L10_GATE",
    "L10_gate_classification": "PASS_TARGET_V012_CACHED_L10",
    "L12_cache_manifest_sha256": "859e01f5a735eeb10f93960068c1fd048ec6ab085a7f5a1df29f9176f9be1e76",
    "L12_cache_manifest_schema": "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
}
TARGET_INTERFACE_PATHS: Final[dict[str, Path]] = {
    "freeze_sha256": TARGET / "FREEZE.json",
    "audit_sha256": TARGET_AUDIT / "HOSTILE_AUDIT_RESULT_V001.json",
    "consumer_sha256": TARGET / "consume_target_cache.py",
    "L10_gate_sha256": TARGET / "CACHED_L10_GATE_V012.json",
    "L12_cache_manifest_sha256": TARGET / "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json",
}
PINNED_SOURCE_SHA256: Final[dict[Path, str]] = {
    FREEZE: "6c0d2efa83584a91df52f299d679e5baab8913cccc6955ddfc2dbeb43a87814a",
    PREFLIGHT_RESULT: "a0723a0caf9c826601984b99484227cb5da613608c8887edeeea234e54649f50",
    PREFLIGHT: "ecf7a568acb3b440fbfee483bad9526d3d1d6eff5f7f7f2cda8e4486b2f94678",
    PREPAYLOAD_AUDIT: "7b4f677615d4688b3911e5350ce99bbd85e922786866648ac414866e1e3ddc32",
    BUILDER: "da5fa4484ce56993cbb0d4b411cad638836cb1ebe272c89a52ff33e382fff8f1",
    CONSUMER: "700dce18ec8f50008a9e3022394a55c8d689268e21b80982896d37b92add7b74",
    METHOD: "e1214f533a4f0476d4db75bd1407a402c1ed0908f7919b376f9c65a27e93b587",
    A18_CORE: "31a772f788a33eca05655d2c4e1e2b5edf236dce6873f7ffba61e67476d9571c",
}

EXPECTED_BUILD_GATE_SHA256: Final[str] = (
    "ea291fd8e39804a780ec4eed6094e7311ff3b3c29aaf89572ef096128f4807b6"
)
EXPECTED_MANIFEST_SHA256: Final[dict[int, str]] = {
    4: "77e27bffdbade06e27d2ef3a75aed7fd8b8ff4cb2a9c7ec2750e12c5ea5a7559",
    6: "3a86e88ffb7e573e31c4d5fb3a101416fff507260697c005f9dd88d728a4652b",
    8: "7e96a28efd2988cae6e9d6466d28760b01081c925075d5baeda772b80662444c",
    10: "128dc4f79a7ef627eedd96ce40e344ebadee4c53595fee98b9b31c9a04e5b5a4",
    12: "f53c4cae94e3672489100256d3a69f57c69532df4194f92b66139fb575902da6",
}
EXPECTED_POSTBUILD_SHA256: Final[str] = (
    "4c5e651b4b168c0f4a65d1502587629b5931658ff759669771390af612c71b22"
)
EXPECTED_L10_AUTHORIZATION_SHA256: Final[str] = (
    "2959300977013221447dc505325e49b51caa11c9da33180eb2a84bee2bd39723"
)


class Refusal(RuntimeError):
    """Fail closed without broadening the replay scope."""


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("noncanonical JSON value") from error


def publication_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, indent=2, sort_keys=True, ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise Refusal("noncanonical publication value") from error


def strict_json(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise Refusal(f"{label} duplicate JSON key")
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise Refusal(f"{label} nonfinite JSON constant")

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=constant,
        )
    except Refusal:
        raise
    except (UnicodeDecodeError, ValueError, TypeError) as error:
        raise Refusal(f"{label} is not strict ASCII JSON") from error
    if type(value) is not dict:
        raise Refusal(f"{label} is not one JSON object")
    return value


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_pinned_json(path: Path, expected: str, label: str) -> dict[str, object]:
    authenticate_file(path, expected, label)
    raw = path.read_bytes()
    if sha256_bytes(raw) != expected:
        raise Refusal(f"{label} changed after authentication")
    return strict_json(raw, label)


def authenticate_file(path: Path, expected: str, label: str) -> None:
    try:
        opened = os.stat(path, follow_symlinks=False)
    except OSError as error:
        raise Refusal(f"{label} is absent") from error
    if (
        stat.S_ISLNK(opened.st_mode) or not stat.S_ISREG(opened.st_mode)
        or opened.st_mode & 0o222 or opened.st_nlink != 1
        or sha256(path) != expected
    ):
        raise Refusal(f"{label} custody/hash mismatch")


def _file_census(path: Path, logical: str) -> dict[str, object]:
    metadata = os.stat(path, follow_symlinks=False)
    if (
        stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_mode & 0o222 or metadata.st_nlink != 1
    ):
        raise Refusal(f"stale file is not immutable owner-once: {logical}")
    return {
        "path": logical, "kind": "file", "bytes": metadata.st_size,
        "mode": stat.S_IMODE(metadata.st_mode), "nlink": metadata.st_nlink,
        "sha256": sha256(path),
    }


def _directory_census(path: Path, logical: str) -> dict[str, object]:
    if path.is_symlink() or not path.is_dir():
        raise Refusal(f"stale directory absent or aliased: {logical}")
    directories: list[dict[str, object]] = []
    files: list[dict[str, object]] = []
    for current_text, names, filenames in os.walk(path, followlinks=False):
        current = Path(current_text)
        names.sort()
        filenames.sort()
        relative = current.relative_to(path)
        current_logical = logical if relative == Path(".") else f"{logical}/{relative.as_posix()}"
        metadata = os.stat(current, follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise Refusal(f"stale directory tree alias: {current_logical}")
        directories.append({"path": current_logical, "mode": stat.S_IMODE(metadata.st_mode)})
        for name in names:
            child = current / name
            child_metadata = os.stat(child, follow_symlinks=False)
            if stat.S_ISLNK(child_metadata.st_mode) or not stat.S_ISDIR(child_metadata.st_mode):
                raise Refusal(f"stale directory child alias: {child}")
        for name in filenames:
            file_row = _file_census(current / name, f"{current_logical}/{name}")
            files.append({key: value for key, value in file_row.items() if key != "kind"})
    directories.sort(key=lambda row: str(row["path"]))
    files.sort(key=lambda row: str(row["path"]))
    material = {"directories": directories, "files": files}
    return {
        "path": logical, "kind": "directory",
        "directory_count": len(directories), "file_count": len(files),
        "total_bytes": sum(int(row["bytes"]) for row in files),
        "inventory_sha256": sha256_bytes(canonical_json_bytes(material)),
    }


STALE_EXPECTED: Final[dict[str, tuple[str, str]]] = {
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json":
        ("file", "58ae7037de078d1d3cd7ac0de48d4cb15c176274871e90c6d7cf231d1d12dd05"),
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS":
        ("directory", "47b1055dd0262b6099bc634a71eaa7efc2f5cd3dd06f5e5bf80a27d644cda54a"),
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json":
        ("file", "6d041b3ef08190a0424bb2acdeecf1348da2febd75702345c83db25e1eacc683"),
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json":
        ("file", "6b710284da8e8cebe557f4022b760e61f0f07712d15043d8b42729a6c707d163"),
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json":
        ("file", "c61f3a50a544fe3fa21c97bbdc3115740d7926329b543e7f4dc0bc16a9ce6d5a"),
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES":
        ("directory", "4d6cfdf839e1f72576eecbf13b3151555e3e9100cf8193e1d06870555c101fb3"),
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS":
        ("directory", "45c41af4b435778caa95add404d1f075681575045194f011a9e96ae8a4eecc43"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_HOSTILE_L10_CROSS_GATE_V001.json":
        ("file", "84a99de5d97373f8daeb2a1bcf1adcf04d2f0e0ee17dab13f58859d35bf141c5"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_V001.json":
        ("file", "9d87a8bed36c4daa366f956b5103873ad254e7f21bd0d2d67b779eccbb857d67"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json":
        ("file", "2eee41e771ba228d6461045b282eb250686d790ef01c3030a1e9f55612951297"),
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/TARGET_L12_EXECUTION_GATE_V012.json":
        ("file", "44ed80086a7f7fbc562961b7723386d61175889a9f6b18dc039ce44f7bff5282"),
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json":
        ("file", "ffa8a12657706799d74e9a10d697cff4b24f9648ad36bf363d308cc6a6157ac4"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_READY_V001.json":
        ("file", "36f8a5b18d7bc0a296e80f51f9073a607528368588bfc2e635897114a5820b13"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_READY_V001.json":
        ("file", "296ac9b6be0184bb2df5488a3450922647b952533744fe4009ffdcb1e07e2750"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_LAUNCH_HANDSHAKE_V002.json":
        ("file", "ecc4b3c6eee52af71660551868265adf39faf5176976fcb5913e6578dbed3289"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_WORKER_RELEASE_V002.json":
        ("file", "ad9029911ecd73f5ffc3066da796ef6e60ce39528e42ba765ec7dc31cb4f8567"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_COMMAND_V001.json":
        ("file", "081bb53255dedcbe56b56f52425cf3827ed7f6f82922884308dbfee01521ef69"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json":
        ("file", "af5ba939b71ba8112f0c24965b681c8e857265dd5f2ec31f11a5719f91f2a704"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_LOG_V001.txt":
        ("file", "71c3436ee4d13f096cd07e5bff645fcdf1ded15b0fa8e90b10ed525c297be603"),
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_LOG_V001.txt":
        ("file", "012cb342797b3ea04118ad747dcfe78f685aef3fedf41851ab8bc6d59990d63a"),
}


def inspect_stale(root: Path = ROOT) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for logical, (kind, expected) in STALE_EXPECTED.items():
        pure = PurePosixPath(logical)
        if pure.is_absolute() or ".." in pure.parts or str(pure) != logical:
            raise Refusal("registered stale path is noncanonical")
        physical = root.joinpath(*pure.parts)
        row = _file_census(physical, logical) if kind == "file" else _directory_census(physical, logical)
        observed = row["sha256"] if kind == "file" else row["inventory_sha256"]
        if observed != expected:
            raise Refusal(f"stale entry census mismatch: {logical}")
        rows.append(row)
    return rows


def authenticate_fixed_sources() -> None:
    for path, digest in PINNED_SOURCE_SHA256.items():
        authenticate_file(path, digest, f"pinned source {path.name}")
    for key, path in TARGET_INTERFACE_PATHS.items():
        authenticate_file(path, CURRENT_TARGET_INTERFACE[key], f"current target {key}")


def build_gate_candidate(old_gate: Mapping[str, object]) -> dict[str, object]:
    if set(old_gate) != {
        "schema", "classification", "authorized_cache_lengths", "freeze_sha256",
        "files_sha256", "independent_hostile_audit", "target_v012_interface",
        "dual_obstruction_custody", "claim_boundary",
    }:
        raise Refusal("stale build gate exact key census mismatch")
    candidate = json.loads(json.dumps(old_gate))
    old_interface = candidate.get("target_v012_interface")
    if type(old_interface) is not dict or set(old_interface) != set(CURRENT_TARGET_INTERFACE):
        raise Refusal("stale target interface exact key census mismatch")
    differing = {
        key for key in CURRENT_TARGET_INTERFACE
        if old_interface[key] != CURRENT_TARGET_INTERFACE[key]
    }
    if differing != {
        "freeze_sha256", "audit_sha256", "L10_gate_sha256",
        "L12_cache_manifest_sha256",
    }:
        raise Refusal("build gate differs from current target outside exact four hashes")
    candidate["target_v012_interface"] = dict(CURRENT_TARGET_INTERFACE)
    if sha256_bytes(canonical_json_bytes(candidate)) != EXPECTED_BUILD_GATE_SHA256:
        raise Refusal("current target build gate candidate hash mismatch")
    return candidate


def _expected_manifest_from_old(old: Mapping[str, object]) -> dict[str, object]:
    candidate = json.loads(json.dumps(old))
    candidate["cache_build_authorization_gate_sha256"] = EXPECTED_BUILD_GATE_SHA256
    return candidate


def predicted_manifest_hashes(root: Path = ROOT) -> dict[int, str]:
    result: dict[int, str] = {}
    for length in (4, 6, 8, 10, 12):
        path = root / f"AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS/L{length}/CACHE_MANIFEST.json"
        old = strict_json(path.read_bytes(), f"stale L{length} manifest")
        digest = sha256_bytes(canonical_json_bytes(_expected_manifest_from_old(old)))
        if digest != EXPECTED_MANIFEST_SHA256[length]:
            raise Refusal(f"predicted L{length} manifest hash mismatch")
        result[length] = digest
    return result


def plan(root: Path = ROOT) -> dict[str, object]:
    return {
        "schema": "STAGE3_DATA_LINEAGE_REPLAY_PLAN_V001",
        "classification": "NONEXECUTING_FIXED_SCOPE_PLAN",
        "stale_entry_count": len(STALE_EXPECTED),
        "stale_paths": list(STALE_EXPECTED),
        "current_target_interface": dict(CURRENT_TARGET_INTERFACE),
        "candidate_build_gate_sha256": EXPECTED_BUILD_GATE_SHA256,
        "predicted_manifest_sha256_by_L": {
            str(key): value for key, value in EXPECTED_MANIFEST_SHA256.items()
        },
        "unchanged_physics_executables": {
            "builder": PINNED_SOURCE_SHA256[BUILDER],
            "consumer": PINNED_SOURCE_SHA256[CONSUMER],
        },
        "live_authorization": LIVE_AUTHORIZATION,
        "live_stops_before_l12_launch": True,
        "claim_boundary": (
            "FIXED_DATA_LINEAGE_REPLAY_PLAN_ONLY__NO_RETIREMENT_PUBLICATION_"
            "PHYSICAL_HISTORY_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def dry_run(root: Path = ROOT) -> dict[str, object]:
    if root == ROOT:
        authenticate_fixed_sources()
    rows = inspect_stale(root)
    old_gate_path = root / BUILD_GATE.relative_to(ROOT)
    old_gate = strict_json(old_gate_path.read_bytes(), "stale hostile build gate")
    candidate = build_gate_candidate(old_gate)
    manifests = predicted_manifest_hashes(root)
    return {
        "schema": "STAGE3_DATA_LINEAGE_REPLAY_DRY_RUN_V001",
        "classification": "PASS_FIXED_SCOPE_DRY_RUN_NO_MUTATION",
        "authenticated_stale_entry_count": len(rows),
        "authenticated_stale_total_file_bytes": sum(
            int(row.get("bytes", row.get("total_bytes", 0))) for row in rows
        ),
        "candidate_build_gate_sha256": sha256_bytes(canonical_json_bytes(candidate)),
        "predicted_manifest_sha256_by_L": {
            str(key): value for key, value in manifests.items()
        },
        "canonical_action_executed": False,
        "claim_boundary": "DRY_RUN_ONLY__NO_RETIREMENT_PUBLICATION_COMPUTE_OR_L12_LAUNCH",
    }


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_once(path: Path, record: Mapping[str, object]) -> str:
    if path.exists() or path.is_symlink():
        raise Refusal(f"refuse overwrite: {path}")
    if not path.parent.is_dir() or path.parent.is_symlink():
        raise Refusal(f"publication parent absent or aliased: {path.parent}")
    raw = canonical_json_bytes(dict(record))
    temporary = path.parent / f".{path.name}.stage3-{os.getpid()}-{os.urandom(8).hex()}"
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o400)
    linked = False
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise Refusal("short owner-once publication write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        if sha256(temporary) != sha256_bytes(raw):
            raise Refusal("staged publication hash mismatch")
        os.link(temporary, path, follow_symlinks=False)
        linked = True
        os.unlink(temporary)
        _fsync_directory(path.parent)
        authenticate_file(path, sha256_bytes(raw), f"published {path.name}")
        return sha256_bytes(raw)
    finally:
        os.close(descriptor)
        if not linked and temporary.exists():
            temporary.unlink()


def _rename_exclusive(source: Path, destination: Path) -> None:
    if sys.platform != "darwin":
        raise Refusal("owner-once retirement requires macOS renameatx_np")
    function = ctypes.CDLL(None, use_errno=True).renameatx_np
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    result = function(-2, os.fsencode(source), -2, os.fsencode(destination), 0x00000004)
    if result != 0:
        error = ctypes.get_errno()
        raise Refusal(f"exclusive retirement rename failed: {os.strerror(error)}")


def _census_at(root: Path, logical: str, kind: str) -> dict[str, object]:
    path = root.joinpath(*PurePosixPath(logical).parts)
    return _file_census(path, logical) if kind == "file" else _directory_census(path, logical)


def retire_stale(rows: list[dict[str, object]]) -> str:
    AUDIT_ROOT.mkdir(mode=0o755, exist_ok=True)
    if AUDIT_ROOT.is_symlink() or not AUDIT_ROOT.is_dir():
        raise Refusal("audit output root is aliased")
    CUSTODY.mkdir(mode=0o755, exist_ok=True)
    EVENTS.mkdir(mode=0o755, exist_ok=True)
    expected_intent = {
        "schema": "STAGE3_DATA_LINEAGE_OWNER_ONCE_RETIREMENT_INTENT_V001",
        "classification": "RETIRE_EXACT_STALE_LINEAGE_AND_FAILED_LAUNCH",
        "entries": rows,
        "entry_count": len(rows),
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_LINEAGE_HISTORY_OR_L12_RESULT",
    }
    intent_sha = sha256_bytes(canonical_json_bytes(expected_intent))
    if INTENT.exists():
        if read_pinned_json(INTENT, intent_sha, "retirement intent") != expected_intent:
            raise Refusal("retirement intent restart mismatch")
    else:
        publish_once(INTENT, expected_intent)
    event_hashes: list[str] = []
    for ordinal, row in enumerate(rows, start=1):
        logical = str(row["path"])
        source = ROOT.joinpath(*PurePosixPath(logical).parts)
        destination = CUSTODY.joinpath(*PurePosixPath(logical).parts)
        event_path = EVENTS / f"EVENT_{ordinal:03d}.json"
        source_present = os.path.lexists(source)
        destination_present = os.path.lexists(destination)
        if source_present and destination_present:
            raise Refusal(f"dual custody for stale entry: {logical}")
        if not source_present and not destination_present:
            raise Refusal(f"lost custody for stale entry: {logical}")
        if source_present:
            destination.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
            observed = _census_at(ROOT, logical, str(row["kind"]))
            if observed != row:
                raise Refusal(f"stale entry changed before retirement: {logical}")
            _rename_exclusive(source, destination)
            _fsync_directory(source.parent)
            _fsync_directory(destination.parent)
        observed_destination = _census_at(CUSTODY, logical, str(row["kind"]))
        if observed_destination != row:
            raise Refusal(f"retired entry custody mismatch: {logical}")
        event = {
            "schema": "STAGE3_DATA_LINEAGE_OWNER_ONCE_RETIREMENT_EVENT_V001",
            "ordinal": ordinal, "path": logical,
            "entry_sha256": sha256_bytes(canonical_json_bytes(row)),
            "intent_sha256": intent_sha,
        }
        event_sha = sha256_bytes(canonical_json_bytes(event))
        if event_path.exists():
            if read_pinned_json(event_path, event_sha, f"retirement event {ordinal}") != event:
                raise Refusal("retirement event restart mismatch")
        else:
            publish_once(event_path, event)
        event_hashes.append(event_sha)
    receipt = {
        "schema": "STAGE3_DATA_LINEAGE_OWNER_ONCE_RETIREMENT_RECEIPT_V001",
        "classification": "PASS_EXACT_STALE_LINEAGE_AND_FAILED_LAUNCH_RETIREMENT",
        "intent_sha256": intent_sha, "event_sha256_by_ordinal": event_hashes,
        "entry_count": len(rows),
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_LINEAGE_HISTORY_OR_L12_RESULT",
    }
    receipt_sha = sha256_bytes(canonical_json_bytes(receipt))
    if RECEIPT.exists():
        if read_pinned_json(RECEIPT, receipt_sha, "retirement receipt") != receipt:
            raise Refusal("retirement receipt restart mismatch")
    else:
        publish_once(RECEIPT, receipt)
    return receipt_sha


def run_checked(command: list[str], label: str) -> None:
    completed = subprocess.run(
        command, cwd=ROOT, check=False, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if completed.returncode != 0:
        raise Refusal(f"{label} failed ({completed.returncode}): {completed.stdout[-2000:]}")


def import_hostile_consumer():
    authenticate_file(CONSUMER, PINNED_SOURCE_SHA256[CONSUMER], "hostile consumer")
    sys.path.insert(0, str(HOSTILE))
    try:
        module = importlib.import_module("consume_cache_v004r4")
    finally:
        if sys.path[0] == str(HOSTILE):
            sys.path.pop(0)
    if Path(module.__file__).resolve() != CONSUMER:
        raise Refusal("hostile consumer import path mismatch")
    return module


def validate_new_build_gate(candidate: dict[str, object]) -> None:
    consumer = import_hostile_consumer()
    freeze = read_pinned_json(FREEZE, PINNED_SOURCE_SHA256[FREEZE], "hostile freeze")
    audit = read_pinned_json(PREPAYLOAD_AUDIT, PINNED_SOURCE_SHA256[PREPAYLOAD_AUDIT], "hostile prepayload audit")
    consumer.validate_hostile_build_authorization(
        candidate, audit, freeze_sha256=PINNED_SOURCE_SHA256[FREEZE],
        frozen_files=freeze["files"], audit_sha256=PINNED_SOURCE_SHA256[PREPAYLOAD_AUDIT],
    )
    custody = consumer.AuthorityCustody()
    try:
        consumer.retain_build_authorization_inputs(custody, candidate)
        custody.verify_all()
    finally:
        custody.close()


def audit_l12_cache() -> dict[str, object]:
    consumer = import_hostile_consumer()
    manifest_path = HOSTILE / "V004R4_CACHE_PAYLOADS/L12/CACHE_MANIFEST.json"
    manifest_hash = sha256(manifest_path)
    if manifest_hash != EXPECTED_MANIFEST_SHA256[12]:
        raise Refusal("new hostile L12 manifest hash mismatch")
    manifest = strict_json(manifest_path.read_bytes(), "new hostile L12 manifest")
    source_hashes = {
        "method": PINNED_SOURCE_SHA256[METHOD], "builder": PINNED_SOURCE_SHA256[BUILDER],
        "consumer": PINNED_SOURCE_SHA256[CONSUMER],
        "preflight": PINNED_SOURCE_SHA256[PREFLIGHT],
    }
    context = consumer.CacheContext(
        12, manifest_path.parent, manifest, manifest_hash,
        source_hashes, time.monotonic(),
    )
    try:
        context.reauthenticate()
    finally:
        context.close()
    count = int(manifest["array_file_count"])
    record = {
        "schema": "HOSTILE_V004R4_POSTBUILD_PAYLOAD_AUDIT_V001",
        "classification": "PASS_HOSTILE_V004R4_L12_STORAGE_CACHE",
        "auditor_role": "INDEPENDENT_HOSTILE_POSTBUILD_READ_ONLY_REVIEW",
        "sealed_input_commit": SEALED_INPUT_COMMIT,
        "manifest_sha256": manifest_hash,
        "manifest_file_count": count,
        "manifest_payload_bytes": int(manifest["payload"]["actual_cache_array_bytes"]),
        "checks": {
            "manifest_exact_schema": 1, "manifest_member_records": count,
            "semantic_index_records": count, "stable_descriptor_records": count + 1,
            "zero_length_operator_records": 2,
        },
        "checks_passed": 3 * count + 4, "checks_total": 3 * count + 4,
        "failures": [], "no_symlinked_or_writable_inputs": True,
        "semantic_cachecontext_passed": True, "physical_history_executed": False,
        "claim_boundary": "HOSTILE_V004R4_POSTBUILD_STORAGE_AUDIT_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
    }
    if sha256_bytes(canonical_json_bytes(record)) != EXPECTED_POSTBUILD_SHA256:
        raise Refusal("new hostile postbuild audit candidate hash mismatch")
    return record


def l10_authorization_record() -> dict[str, object]:
    record = {
        "schema": "HOSTILE_V004R4_L10_EXECUTION_AUTHORIZATION_GATE_V001",
        "classification": "AUTHORIZE_AUDITED_HOSTILE_V004R4_L10",
        "role": "hostile_v004r4", "authorized_length": 10,
        "l10_cache_manifest_sha256": EXPECTED_MANIFEST_SHA256[10],
        "consumer_sha256": PINNED_SOURCE_SHA256[CONSUMER],
        "builder_sha256": PINNED_SOURCE_SHA256[BUILDER],
        "method_sha256": PINNED_SOURCE_SHA256[METHOD],
        "freeze_sha256": PINNED_SOURCE_SHA256[FREEZE],
        "preflight_result_sha256": PINNED_SOURCE_SHA256[PREFLIGHT_RESULT],
        "independent_hostile_audit_sha256": PINNED_SOURCE_SHA256[PREPAYLOAD_AUDIT],
        "claim_boundary": "FINITE_HOSTILE_V004R4_L10_AUTHORIZATION_ONLY__NO_L12_OR_RESULT",
    }
    if sha256_bytes(canonical_json_bytes(record)) != EXPECTED_L10_AUTHORIZATION_SHA256:
        raise Refusal("new hostile L10 authorization candidate hash mismatch")
    return record


def l10_gate_record(history_sha: str) -> dict[str, object]:
    if len(history_sha) != 64:
        raise Refusal("hostile L10 history hash malformed")
    return {
        "schema": "HOSTILE_V004R4_CACHED_L10_GATE",
        "classification": "PASS_HOSTILE_V004R4_CACHED_L10",
        "auditor_role": "INDEPENDENT_HOSTILE_STAGE_GATE_REVIEW",
        "sealed_input_commit": SEALED_INPUT_COMMIT,
        "consumer_sha256": PINNED_SOURCE_SHA256[CONSUMER],
        "builder_sha256": PINNED_SOURCE_SHA256[BUILDER],
        "method_sha256": PINNED_SOURCE_SHA256[METHOD],
        "freeze_sha256": PINNED_SOURCE_SHA256[FREEZE],
        "preflight_result_sha256": PINNED_SOURCE_SHA256[PREFLIGHT_RESULT],
        "independent_hostile_audit_sha256": PINNED_SOURCE_SHA256[PREPAYLOAD_AUDIT],
        "cache_manifest_sha256_by_L": {"10": EXPECTED_MANIFEST_SHA256[10]},
        "l10_execution_authorization": {
            "path": str(L10_AUTHORIZATION),
            "sha256": EXPECTED_L10_AUTHORIZATION_SHA256,
            "schema": "HOSTILE_V004R4_L10_EXECUTION_AUTHORIZATION_GATE_V001",
            "identity_field": "classification",
            "identity_value": "AUTHORIZE_AUDITED_HOSTILE_V004R4_L10",
        },
        "histories": [{
            "L": 10,
            "path": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json",
            "sha256": history_sha,
        }],
        "checks": {
            "canonical_v004_projection": 1, "l10_cache_manifest": 1,
            "l10_execution_authorization": 1, "l10_history": 1,
            "stable_descriptor_records": 13, "terminal_shard_records": 10,
        },
        "checks_passed": 27, "checks_total": 27, "failures": [],
        "claim_boundary": "FINITE_HOSTILE_V004R4_CACHED_L10_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }


TARGET_PRODUCT_PATHS: Final[dict[tuple[str, int], Path]] = {
    **{("A05_FIVE_CACHE_SET", index): TARGET / f"CACHE_PAYLOADS_V012/L{length}/CACHE_MANIFEST.json"
       for index, length in enumerate((4, 6, 8, 10, 12), start=1)},
    ("A07_BASE_PHYSICAL_GATE", 1): TARGET / "PHYSICAL_EXECUTION_GATE_V012.json",
    ("A11_CONTROL_STAGE_GATE", 1): TARGET / "CACHED_CONTROL_L4_L8_GATE_V012.json",
    ("A13_L10_AUTHORIZATION", 1): TARGET / "L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
    ("A14_L10_HISTORY", 1): TARGET / "PHYSICAL_OUTPUTS/HISTORY_L10.json",
    ("A15_L10_STAGE_GATE", 1): TARGET / "CACHED_L10_GATE_V012.json",
    ("A16_L10_STAGE_AUDIT", 1): TARGET_AUDIT / "CACHED_L10_GATE_AUDIT_V001.json",
}


def transitive_target_interface_equal(a18: Mapping[str, object], gate: Mapping[str, object]) -> None:
    target = a18.get("target")
    branch = target.get("branch") if type(target) is dict else None
    interface = gate.get("target_v012_interface")
    if type(branch) is not dict or type(interface) is not dict:
        raise Refusal("A18/build-gate transitive interface absent")
    observed = {
        "freeze_sha256": branch["freeze"]["sha256"],
        "audit_sha256": branch["independent_audit"]["sha256"],
        "consumer_sha256": branch["consumer"]["sha256"],
        "L10_gate_sha256": branch["cached_L10_gate"]["sha256"],
        "L12_cache_manifest_sha256": branch["L12_cache_manifest"]["sha256"],
    }
    expected = {key: interface[key] for key in observed}
    if observed != expected or expected != {
        key: CURRENT_TARGET_INTERFACE[key] for key in observed
    }:
        raise Refusal("A18/build-gate current target interface mismatch")


def construct_a18(candidate_gate: dict[str, object]) -> tuple[dict[str, object], str]:
    authenticate_file(A18_CORE, PINNED_SOURCE_SHA256[A18_CORE], "A18 constructor core")
    sys.path.insert(0, str(A18_CORE.parent))
    try:
        core = importlib.import_module("replay_a01_a18")
    finally:
        if sys.path[0] == str(A18_CORE.parent):
            sys.path.pop(0)
    if Path(core.__file__).resolve() != A18_CORE:
        raise Refusal("A18 constructor import path mismatch")
    produced = {key: sha256(path) for key, path in TARGET_PRODUCT_PATHS.items()}
    review = core.ExactLiveReview(ROOT)
    hostile_branch, metadata = core.construct_live_a17_branch(review)
    updates = core.measured_a18_updates(review, produced, hostile_branch, metadata)
    record = core.construct_a18(updates, review.production_sink, review.independent_sink)
    review.validate_a18(record, produced)
    transitive_target_interface_equal(record, candidate_gate)
    return record, sha256_bytes(canonical_json_bytes(record))


def execute_live(authorization: str | None) -> dict[str, object]:
    if authorization != LIVE_AUTHORIZATION:
        raise Refusal("exact live authorization is absent")
    if RESULT.exists() or RESULT.is_symlink():
        raise Refusal("live replay result already exists")
    authenticate_fixed_sources()
    rows = inspect_stale(ROOT)
    old_gate = read_pinned_json(BUILD_GATE, STALE_EXPECTED[str(BUILD_GATE.relative_to(ROOT))][1], "stale build gate")
    candidate_gate = build_gate_candidate(old_gate)
    predicted_manifest_hashes(ROOT)
    receipt_hash = retire_stale(rows)
    BUILD_GATE.parent.mkdir(mode=0o755, exist_ok=True)
    build_gate_hash = publish_once(BUILD_GATE, candidate_gate)
    validate_new_build_gate(candidate_gate)
    for length in (4, 6, 8, 10, 12):
        run_checked([sys.executable, "-B", str(BUILDER), "build", "--length", str(length)], f"hostile L{length} cache build")
        manifest = HOSTILE / f"V004R4_CACHE_PAYLOADS/L{length}/CACHE_MANIFEST.json"
        authenticate_file(manifest, EXPECTED_MANIFEST_SHA256[length], f"new hostile L{length} manifest")
    postbuild = audit_l12_cache()
    postbuild_hash = publish_once(POSTBUILD, postbuild)
    l10_authorization = l10_authorization_record()
    l10_authorization_hash = publish_once(L10_AUTHORIZATION, l10_authorization)
    run_checked([sys.executable, "-B", str(CONSUMER), "execute", "--length", "10"], "hostile L10 exact history")
    history_hash = sha256(L10_HISTORY)
    l10_gate = l10_gate_record(history_hash)
    l10_gate_hash = publish_once(L10_GATE, l10_gate)
    a18, a18_hash = construct_a18(candidate_gate)
    if publish_once(A18, a18) != a18_hash:
        raise Refusal("A18 publication hash mismatch")
    result = {
        "schema": "STAGE3_DATA_LINEAGE_REPLAY_RESULT_V001",
        "classification": "PASS_CURRENT_TARGET_TRANSITIVE_HOSTILE_LINEAGE_READY_FOR_EXISTING_L12_LAUNCHER",
        "retirement_receipt_sha256": receipt_hash,
        "build_gate_sha256": build_gate_hash,
        "cache_manifest_sha256_by_L": {str(key): value for key, value in EXPECTED_MANIFEST_SHA256.items()},
        "postbuild_audit_sha256": postbuild_hash,
        "l10_authorization_sha256": l10_authorization_hash,
        "l10_history_sha256": history_hash,
        "l10_gate_sha256": l10_gate_hash,
        "a18_sha256": a18_hash,
        "transitive_target_interface_equal": True,
        "frozen_builder_sha256": PINNED_SOURCE_SHA256[BUILDER],
        "frozen_consumer_sha256": PINNED_SOURCE_SHA256[CONSUMER],
        "l12_launched": False,
        "claim_boundary": "FINITE_HOSTILE_LINEAGE_REPLAY_AND_L10_RECERTIFICATION_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }
    publish_once(RESULT, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("plan", "dry-run", "execute"))
    parser.add_argument("--authorization")
    arguments = parser.parse_args()
    try:
        if arguments.mode == "plan":
            if arguments.authorization is not None:
                raise Refusal("plan mode rejects authorization")
            output = plan()
        elif arguments.mode == "dry-run":
            if arguments.authorization is not None:
                raise Refusal("dry-run mode rejects authorization")
            output = dry_run()
        else:
            output = execute_live(arguments.authorization)
    except (OSError, RuntimeError, ValueError, Refusal, subprocess.SubprocessError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
