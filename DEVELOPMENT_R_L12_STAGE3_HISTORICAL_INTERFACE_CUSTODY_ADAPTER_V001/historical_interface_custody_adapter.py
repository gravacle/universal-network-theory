#!/usr/bin/env python3
"""Development-only historical target-interface custody adapter.

The immutable hostile V004R4 cache build gate predates the current target
V012 replay. Its four target record hashes remain owner-once in the
authenticated A18 retirement snapshot. This module prepares exactly one
temporary substitution: the unchanged hostile consumer's
``retain_build_authorization_inputs`` reads those historical records from
their retained paths instead of requiring old hashes at successor paths.

Only ``plan`` and ``self-test`` are exposed. No worker launch, cache/history
creation, publication, file move, or L12 authorization exists here.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
import types
import weakref
from contextlib import contextmanager
from pathlib import Path
from typing import Final, Iterator


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
HOSTILE: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
CONSUMER: Final[Path] = HOSTILE / "consume_cache_v004r4.py"
FREEZE: Final[Path] = HOSTILE / "FROZEN_MANIFEST_V004R4.json"
GATE: Final[Path] = HOSTILE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
HOSTILE_AUDIT: Final[Path] = HOSTILE / "HOSTILE_AUDIT_RESULT_V004R4.json"
HOSTILE_PREFLIGHT: Final[Path] = HOSTILE / "V004R4_CACHE_PREFLIGHT_RESULT.json"
RETIREMENT_ROOT: Final[Path] = (
    ROOT / "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001"
    / "RETIRED_CANONICAL_A01_A17_PRE_A18_REPAIR_V001"
)
RETIREMENT_RECEIPT: Final[Path] = RETIREMENT_ROOT / "RETIREMENT_RECEIPT_V001.json"

TARGET_RELATIVE: Final[dict[str, str]] = {
    "freeze": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    "audit": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
    "L10_gate": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
    "L12_cache_manifest": (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json"
    ),
}
HISTORICAL_TARGET_PATHS: Final[dict[str, Path]] = {
    name: RETIREMENT_ROOT / relative for name, relative in TARGET_RELATIVE.items()
}
ACTIVE_TARGET_PATHS: Final[dict[str, Path]] = {
    name: ROOT / relative for name, relative in TARGET_RELATIVE.items()
}
TARGET_CONSUMER: Final[Path] = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
)

CONSUMER_SHA256: Final[str] = "700dce18ec8f50008a9e3022394a55c8d689268e21b80982896d37b92add7b74"
FREEZE_SHA256: Final[str] = "6c0d2efa83584a91df52f299d679e5baab8913cccc6955ddfc2dbeb43a87814a"
GATE_SHA256: Final[str] = "58ae7037de078d1d3cd7ac0de48d4cb15c176274871e90c6d7cf231d1d12dd05"
RETIREMENT_RECEIPT_SHA256: Final[str] = "5c8d714973bb2ac22b50643e8f84de042e7a41e282f8f3d25c7d32e64c10fbf0"
HOSTILE_AUDIT_SHA256: Final[str] = "7b4f677615d4688b3911e5350ce99bbd85e922786866648ac414866e1e3ddc32"
HOSTILE_PREFLIGHT_SHA256: Final[str] = "a0723a0caf9c826601984b99484227cb5da613608c8887edeeea234e54649f50"
TARGET_CONSUMER_SHA256: Final[str] = "80b2ce08af37bc8cffd91f07146c777f60785883436361ca9521597763fd5a11"
HISTORICAL_TARGET_SHA256: Final[dict[str, str]] = {
    "freeze": "b3a4ba272c7ed36cb46416443179832e0ddf1c4ac053534369299f9ca019a903",
    "audit": "ad5686920481060d9a6208c20367530f6081b1eb40b896fe39db592a19dab764",
    "L10_gate": "4a0a8959b5a5286bd0d52275fa6ac55ef2be68e7d2c6aa6f98ebf7a306eddd12",
    "L12_cache_manifest": "f3d632fad10711e519750d4d0332768dc8df13c095eaee40e91ec5c1145f7a63",
}
ACTIVE_TARGET_SHA256: Final[dict[str, str]] = {
    "freeze": "a6997822fd2daa2be0079e67d81833f1eac69fe01c6ff0b9188560f2c1234395",
    "audit": "a50044557c5316d50f3b1e4cfefb035c674321a96147690aa3017b2e01cb2301",
    "L10_gate": "20261b35e21d626b61b69a8e29b8dee7c4521bd157aca787aff0fba4524e5ad2",
    "L12_cache_manifest": "859e01f5a735eeb10f93960068c1fd048ec6ab085a7f5a1df29f9176f9be1e76",
}
EXPECTED_INTERFACE: Final[dict[str, str]] = {
    "freeze_sha256": HISTORICAL_TARGET_SHA256["freeze"],
    "freeze_schema": "TARGET_L12_STORAGE_CACHE_FREEZE_V012",
    "audit_sha256": HISTORICAL_TARGET_SHA256["audit"],
    "audit_schema": "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001",
    "audit_classification": "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE",
    "consumer_sha256": TARGET_CONSUMER_SHA256,
    "L10_gate_sha256": HISTORICAL_TARGET_SHA256["L10_gate"],
    "L10_gate_schema": "TARGET_V012_CACHED_L10_GATE",
    "L10_gate_classification": "PASS_TARGET_V012_CACHED_L10",
    "L12_cache_manifest_sha256": HISTORICAL_TARGET_SHA256["L12_cache_manifest"],
    "L12_cache_manifest_schema": "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
}
CLAIM_BOUNDARY: Final[str] = (
    "MUTABLE_HISTORICAL_INTERFACE_CUSTODY_READINESS_ONLY__NO_LAUNCH_"
    "PUBLICATION_PHYSICAL_RESULT_SPECTRUM_CONTINUUM_OR_GRAVITY"
)
LOCAL_IMPORT_NAMES: Final[tuple[str, ...]] = (
    "independent_prefix_history", "independent_prefix_history_v002",
    "independent_prefix_history_v003", "independent_prefix_history_v004",
    "independent_prefix_history_v004r2", "v004r2_common",
    "validate_v004r4_zero_length_preflight", "v004r4_cache_io",
)
_AUTHENTICATED_MODULES: "weakref.WeakKeyDictionary[types.ModuleType, dict[str, object]]" = (
    weakref.WeakKeyDictionary()
)


class AdapterRefusal(RuntimeError):
    """A historical-interface custody obligation refused closed."""


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_nlink, stat.S_IMODE(value.st_mode),
        stat.S_IFMT(value.st_mode),
    )


def _read_owner_once(path: Path, digest: str, label: str) -> bytes:
    if (
        not isinstance(path, Path) or not path.is_absolute() or Path(str(path)) != path
        or ROOT not in path.parents or "\x00" in str(path)
        or type(digest) is not str or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
    ):
        raise AdapterRefusal(f"{label} path/hash contract mismatch")
    cursor = Path(path.anchor)
    try:
        for component in path.parts[1:-1]:
            cursor /= component
            metadata = os.stat(cursor, follow_symlinks=False)
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                raise AdapterRefusal(f"{label} parent is aliased or special")
    except OSError as error:
        raise AdapterRefusal(f"{label} parent is absent") from error
    parent_fd = file_fd = -1
    try:
        parent_fd = os.open(
            path.parent, os.O_RDONLY | os.O_DIRECTORY
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        parent_before = os.fstat(parent_fd)
        file_fd = os.open(
            path.name, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd,
        )
        before = os.fstat(file_fd)
        named = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or before.st_mode & 0o222
            or before.st_nlink != 1 or _identity(before) != _identity(named)
        ):
            raise AdapterRefusal(f"{label} is not immutable owner-once")
        raw = bytearray()
        offset = 0
        while offset < before.st_size:
            block = os.pread(file_fd, min(16 * 2**20, before.st_size - offset), offset)
            if not block:
                raise AdapterRefusal(f"{label} retained read was short")
            raw.extend(block)
            offset += len(block)
        after = os.fstat(file_fd)
        named_after = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        parent_after = os.fstat(parent_fd)
        if (
            _identity(after) != _identity(before)
            or _identity(named_after) != _identity(before)
            or (parent_after.st_dev, parent_after.st_ino)
            != (parent_before.st_dev, parent_before.st_ino)
            or hashlib.sha256(raw).hexdigest() != digest
        ):
            raise AdapterRefusal(f"{label} identity or digest changed")
        return bytes(raw)
    except OSError as error:
        raise AdapterRefusal(f"{label} cannot be retained") from error
    finally:
        if file_fd >= 0:
            os.close(file_fd)
        if parent_fd >= 0:
            os.close(parent_fd)


def _strict_object(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise AdapterRefusal(f"{label} has a duplicate JSON key")
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise AdapterRefusal(f"{label} has a nonfinite JSON value")

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs, parse_constant=constant,
        )
    except AdapterRefusal:
        raise
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise AdapterRefusal(f"{label} is not strict JSON") from error
    if type(value) is not dict:
        raise AdapterRefusal(f"{label} is not one JSON object")
    return value


def _record(path: Path, digest: str, label: str) -> dict[str, object]:
    return _strict_object(_read_owner_once(path, digest, label), label)


def _validate_path_partition(
    historical: dict[str, Path], active: dict[str, Path],
) -> None:
    if set(historical) != set(TARGET_RELATIVE) or set(active) != set(TARGET_RELATIVE):
        raise AdapterRefusal("historical/active target path census mismatch")
    for name, relative in TARGET_RELATIVE.items():
        expected_historical = RETIREMENT_ROOT / relative
        expected_active = ROOT / relative
        if (
            historical[name] != expected_historical
            or active[name] != expected_active
            or historical[name] == active[name]
            or RETIREMENT_ROOT not in historical[name].parents
            or RETIREMENT_ROOT in active[name].parents
        ):
            raise AdapterRefusal(f"active-path substitution refused: {name}")


def authenticate_static_inputs() -> dict[str, object]:
    """Authenticate exact current sources plus historical and successor records."""
    _validate_path_partition(HISTORICAL_TARGET_PATHS, ACTIVE_TARGET_PATHS)
    freeze = _record(FREEZE, FREEZE_SHA256, "hostile frozen source manifest")
    files = freeze.get("files")
    if (
        freeze.get("schema")
        != "AUDIT_R_L12_PREFIX_HISTORY_STORAGE_CACHE_FREEZE_V004R4"
        or type(files) is not dict
        or files.get(CONSUMER.name) != CONSUMER_SHA256
    ):
        raise AdapterRefusal("hostile frozen consumer binding mismatch")
    source_hashes: dict[str, str] = {}
    for name, digest in files.items():
        if type(name) is not str or type(digest) is not str:
            raise AdapterRefusal("hostile frozen source identity malformed")
        _read_owner_once(HOSTILE / name, digest, f"hostile frozen source {name}")
        source_hashes[name] = digest
    if source_hashes.get(CONSUMER.name) != CONSUMER_SHA256:
        raise AdapterRefusal("unchanged hostile consumer was not authenticated")

    gate = _record(GATE, GATE_SHA256, "hostile historical build gate")
    if gate.get("target_v012_interface") != EXPECTED_INTERFACE:
        raise AdapterRefusal("hostile build gate historical interface mismatch")
    receipt = _record(
        RETIREMENT_RECEIPT, RETIREMENT_RECEIPT_SHA256, "A18 retirement receipt",
    )
    if (
        receipt.get("schema") != "V012_A01_A17_OWNER_ONCE_RETIREMENT_RECEIPT_V001"
        or receipt.get("classification") != "PASS_EXACT_OWNER_ONCE_RETIREMENT"
        or type(receipt.get("retired_paths")) is not list
        or receipt.get("canonical_destinations_absent_for_replay") is not True
    ):
        raise AdapterRefusal("A18 retirement receipt identity mismatch")
    retired = set(receipt["retired_paths"])
    required_retired = {
        TARGET_RELATIVE["freeze"], TARGET_RELATIVE["audit"],
        TARGET_RELATIVE["L10_gate"],
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012",
    }
    if not required_retired <= retired:
        raise AdapterRefusal("A18 retirement receipt omits historical target custody")

    for name, path in HISTORICAL_TARGET_PATHS.items():
        _record(path, HISTORICAL_TARGET_SHA256[name], f"historical target {name}")
    for name, path in ACTIVE_TARGET_PATHS.items():
        if HISTORICAL_TARGET_SHA256[name] == ACTIVE_TARGET_SHA256[name]:
            raise AdapterRefusal("historical/current target identities did not advance")
        _record(path, ACTIVE_TARGET_SHA256[name], f"active target {name}")
    _read_owner_once(TARGET_CONSUMER, TARGET_CONSUMER_SHA256, "target consumer")
    return {"source_hashes": source_hashes, "gate": gate, "receipt": receipt}


def load_unchanged_hostile_consumer() -> types.ModuleType:
    """Execute retained consumer bytes and verify every imported local dependency."""
    inputs = authenticate_static_inputs()
    source = _read_owner_once(CONSUMER, CONSUMER_SHA256, "hostile consumer")
    freeze_files = inputs["source_hashes"]
    if type(freeze_files) is not dict:
        raise AdapterRefusal("hostile source hash census unavailable")
    alias = "stage3_historical_interface_unchanged_hostile_consumer_v001"
    if alias in sys.modules:
        raise AdapterRefusal("hostile consumer module alias is occupied")
    saved = {name: sys.modules.get(name) for name in LOCAL_IMPORT_NAMES}
    original_path = tuple(sys.path)
    original_dont_write_bytecode = sys.dont_write_bytecode
    module = types.ModuleType(alias)
    module.__file__ = str(CONSUMER)
    module.__package__ = ""
    module.__cached__ = None
    try:
        for name in LOCAL_IMPORT_NAMES:
            sys.modules.pop(name, None)
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(HOSTILE))
        sys.modules[alias] = module
        exec(compile(source, str(CONSUMER), "exec", dont_inherit=True), module.__dict__)
        if Path(module.__file__) != CONSUMER:
            raise AdapterRefusal("hostile consumer runtime path changed")
        for name in LOCAL_IMPORT_NAMES:
            imported = sys.modules.get(name)
            if imported is None:
                continue
            expected_path = HOSTILE / f"{name}.py"
            if Path(str(getattr(imported, "__file__", ""))).resolve() != expected_path:
                raise AdapterRefusal(f"hostile dependency module path mismatch: {name}")
            expected_digest = freeze_files.get(expected_path.name)
            if type(expected_digest) is not str:
                raise AdapterRefusal(f"hostile dependency is outside freeze: {name}")
            _read_owner_once(
                expected_path, expected_digest, f"loaded hostile dependency {name}",
            )
        _AUTHENTICATED_MODULES[module] = {
            "read_authority": module.read_authority,
            "AuthorityCustody": module.AuthorityCustody,
            "validate_hostile_prepayload_audit":
                module.validate_hostile_prepayload_audit,
            "validate_hostile_build_authorization":
                module.validate_hostile_build_authorization,
            "retain_build_authorization_inputs":
                module.retain_build_authorization_inputs,
        }
        return module
    finally:
        sys.modules.pop(alias, None)
        for name in LOCAL_IMPORT_NAMES:
            sys.modules.pop(name, None)
            if saved[name] is not None:
                sys.modules[name] = saved[name]
        sys.path[:] = original_path
        sys.dont_write_bytecode = original_dont_write_bytecode


def _retain_historical_inputs(
    consumer: types.ModuleType, custody: object, authorization: dict[str, object],
) -> None:
    """Mirror the frozen boundary, changing only four target record paths."""
    static = authenticate_static_inputs()
    if authorization != static["gate"]:
        raise AdapterRefusal("caller did not supply the exact historical build gate")
    interface = authorization.get("target_v012_interface")
    if interface != EXPECTED_INTERFACE:
        raise AdapterRefusal("historical target interface is not exact")

    freeze, _ = consumer.read_authority(
        custody, HISTORICAL_TARGET_PATHS["freeze"], "historical target V012 freeze",
        HISTORICAL_TARGET_SHA256["freeze"],
    )
    audit, _ = consumer.read_authority(
        custody, HISTORICAL_TARGET_PATHS["audit"], "historical target V012 audit",
        HISTORICAL_TARGET_SHA256["audit"],
    )
    _unused, _ = custody.authenticate(
        TARGET_CONSUMER, "unchanged target V012 consumer", TARGET_CONSUMER_SHA256,
    )
    l10, _ = consumer.read_authority(
        custody, HISTORICAL_TARGET_PATHS["L10_gate"],
        "historical target V012 cached L10 gate", HISTORICAL_TARGET_SHA256["L10_gate"],
    )
    manifest, _ = consumer.read_authority(
        custody, HISTORICAL_TARGET_PATHS["L12_cache_manifest"],
        "historical target V012 L12 cache manifest",
        HISTORICAL_TARGET_SHA256["L12_cache_manifest"],
    )
    if (
        freeze.get("schema") != EXPECTED_INTERFACE["freeze_schema"]
        or audit.get("schema") != EXPECTED_INTERFACE["audit_schema"]
        or audit.get("classification") != EXPECTED_INTERFACE["audit_classification"]
        or audit.get("audited_freeze_sha256") != HISTORICAL_TARGET_SHA256["freeze"]
        or audit.get("checks_passed") != audit.get("checks_total")
        or audit.get("failures") != []
        or audit.get("payload_or_history_executed") is not False
        or l10.get("schema") != EXPECTED_INTERFACE["L10_gate_schema"]
        or l10.get("classification") != EXPECTED_INTERFACE["L10_gate_classification"]
        or l10.get("consumer_sha256") != TARGET_CONSUMER_SHA256
        or l10.get("freeze_sha256") != HISTORICAL_TARGET_SHA256["freeze"]
        or manifest.get("schema") != EXPECTED_INTERFACE["L12_cache_manifest_schema"]
        or manifest.get("L") != 12 or type(manifest.get("L")) is not int
        or manifest.get("consumer_sha256") != TARGET_CONSUMER_SHA256
        or manifest.get("freeze_sha256") != HISTORICAL_TARGET_SHA256["freeze"]
    ):
        raise AdapterRefusal("historical target interface content mismatch")

    # This is byte-for-byte the non-target custody tail of the frozen function.
    for role, row in authorization["dual_obstruction_custody"].items():
        if role not in {"target", "hostile"} or type(row) is not dict:
            raise AdapterRefusal("dual obstruction custody role mismatch")
        for path_key, hash_key in (
            ("obstruction_path", "obstruction_sha256"),
            ("log_path", "log_sha256"), ("monitor_path", "monitor_sha256"),
        ):
            path = ROOT / row[path_key]
            _unused, _ = custody.authenticate(
                path, f"{role} obstruction custody {path_key}", row[hash_key],
                immutable=False,
            )
        implementation_paths = {
            "target": (
                ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py",
                ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/Q_SHARDED_TARGET_METHOD_V004.md",
                ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_METHOD_V004.json",
            ),
            "hostile": (
                HOSTILE / "independent_prefix_history_v003.py",
                HOSTILE / "V003_L12_EXECUTABLE_METHOD.md",
                HOSTILE / "FROZEN_MANIFEST_V003.json",
            ),
        }
        for path, hash_key in zip(
            implementation_paths[role],
            ("implementation_sha256", "method_sha256", "freeze_sha256"),
        ):
            if path in custody.files:
                if custody.files[path].digest != row[hash_key]:
                    raise AdapterRefusal(f"{role} obstruction parent hash mismatch")
            else:
                _unused, _ = custody.authenticate(
                    path, f"{role} obstruction parent {hash_key}", row[hash_key],
                    immutable=False,
                )


_PATCH_ACTIVE = False


@contextmanager
def historical_interface_scope(consumer: types.ModuleType) -> Iterator[object]:
    """Temporarily replace only ``retain_build_authorization_inputs``."""
    global _PATCH_ACTIVE
    if _PATCH_ACTIVE:
        raise AdapterRefusal("historical interface scope is already active")
    runtime = _AUTHENTICATED_MODULES.get(consumer)
    if (
        not isinstance(consumer, types.ModuleType)
        or Path(str(getattr(consumer, "__file__", ""))) != CONSUMER
        or runtime is None
    ):
        raise AdapterRefusal("exact unchanged hostile consumer module is required")
    observed_runtime = {
        "read_authority": consumer.read_authority,
        "AuthorityCustody": consumer.AuthorityCustody,
        "validate_hostile_prepayload_audit": consumer.validate_hostile_prepayload_audit,
        "validate_hostile_build_authorization": consumer.validate_hostile_build_authorization,
        "retain_build_authorization_inputs": consumer.retain_build_authorization_inputs,
    }
    if any(observed_runtime[key] is not value for key, value in runtime.items()):
        raise AdapterRefusal("authenticated hostile consumer runtime changed")
    _read_owner_once(CONSUMER, CONSUMER_SHA256, "hostile consumer before patch")
    original = consumer.retain_build_authorization_inputs
    live = {"active": True}

    def replacement(custody: object, authorization: dict[str, object]) -> None:
        if not live["active"]:
            raise AdapterRefusal("historical interface capability expired")
        if consumer.retain_build_authorization_inputs is not replacement:
            raise AdapterRefusal("historical interface boundary changed in scope")
        for name, value in runtime.items():
            observed = (
                replacement if name == "retain_build_authorization_inputs"
                else getattr(consumer, name)
            )
            if observed is not value and name != "retain_build_authorization_inputs":
                raise AdapterRefusal("authenticated hostile consumer runtime changed")
        _read_owner_once(CONSUMER, CONSUMER_SHA256, "hostile consumer in scope")
        _retain_historical_inputs(consumer, custody, authorization)

    _PATCH_ACTIVE = True
    consumer.retain_build_authorization_inputs = replacement
    primary: BaseException | None = None
    try:
        yield replacement
    except BaseException as error:
        primary = error
        raise
    finally:
        live["active"] = False
        drift = consumer.retain_build_authorization_inputs is not replacement
        consumer.retain_build_authorization_inputs = original
        _PATCH_ACTIVE = False
        _read_owner_once(CONSUMER, CONSUMER_SHA256, "hostile consumer after patch")
        if drift and primary is None:
            raise AdapterRefusal("historical interface boundary changed in scope")


def _hostile_gate_inputs(consumer: types.ModuleType) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    freeze = _record(FREEZE, FREEZE_SHA256, "hostile source freeze")
    audit = _record(HOSTILE_AUDIT, HOSTILE_AUDIT_SHA256, "hostile prepayload audit")
    preflight = _record(
        HOSTILE_PREFLIGHT, HOSTILE_PREFLIGHT_SHA256, "hostile preflight result",
    )
    gate = _record(GATE, GATE_SHA256, "hostile build gate")
    consumer.validate_hostile_prepayload_audit(
        audit, freeze_sha256=FREEZE_SHA256, frozen_files=freeze["files"],
        preflight_result_sha256=HOSTILE_PREFLIGHT_SHA256,
    )
    consumer.validate_hostile_build_authorization(
        gate, audit, freeze_sha256=FREEZE_SHA256,
        frozen_files=freeze["files"], audit_sha256=HOSTILE_AUDIT_SHA256,
    )
    return freeze, audit, gate


def self_test() -> dict[str, object]:
    before = evidence_state()
    consumer = load_unchanged_hostile_consumer()
    _freeze, _audit, gate = _hostile_gate_inputs(consumer)

    original = consumer.retain_build_authorization_inputs
    custody = consumer.AuthorityCustody()
    try:
        try:
            original(custody, gate)
        except consumer.Refusal as error:
            if "target V012 freeze hash mismatch" not in str(error):
                raise AdapterRefusal("original boundary refused for the wrong reason") from error
        else:
            raise AdapterRefusal("original stale boundary unexpectedly accepted")
    finally:
        custody.close()

    custody = consumer.AuthorityCustody()
    leaked = None
    try:
        with historical_interface_scope(consumer) as leaked:
            if consumer.retain_build_authorization_inputs is not leaked:
                raise AdapterRefusal("only patched boundary is not active")
            leaked(custody, gate)
            custody.verify_all()
            for path in HISTORICAL_TARGET_PATHS.values():
                if path not in custody.files:
                    raise AdapterRefusal("historical target was not retained")
        if consumer.retain_build_authorization_inputs is not original:
            raise AdapterRefusal("historical boundary was not restored")
        try:
            leaked(custody, gate)
        except AdapterRefusal as error:
            if "capability expired" not in str(error):
                raise
        else:
            raise AdapterRefusal("leaked historical capability remained active")
    finally:
        custody.close()

    after = evidence_state()
    if before != after:
        raise AdapterRefusal("self-test changed a source, authority, or execution path")
    return {
        "schema": "V012_STAGE3_HISTORICAL_INTERFACE_CUSTODY_SELF_TEST_V001",
        "classification": "PASS_MUTABLE_HISTORICAL_INTERFACE_READINESS",
        "unchanged_hostile_consumer_sha256": CONSUMER_SHA256,
        "historical_target_sha256": dict(HISTORICAL_TARGET_SHA256),
        "active_target_sha256": dict(ACTIVE_TARGET_SHA256),
        "retirement_receipt_sha256": RETIREMENT_RECEIPT_SHA256,
        "patched_boundary_count": 1,
        "launched": False,
        "published": False,
        "moved": False,
        "physical_execution": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evidence_state() -> dict[str, object]:
    hostile_freeze = _record(FREEZE, FREEZE_SHA256, "hostile source freeze state")
    target_freeze = _record(
        ACTIVE_TARGET_PATHS["freeze"], ACTIVE_TARGET_SHA256["freeze"],
        "active target source freeze state",
    )
    hostile_sources = hostile_freeze.get("files")
    target_sources = target_freeze.get("files")
    if type(hostile_sources) is not dict or type(target_sources) is not dict:
        raise AdapterRefusal("source freeze census is malformed")
    files = {
        "hostile_consumer": CONSUMER,
        "hostile_freeze": FREEZE,
        "hostile_gate": GATE,
        "hostile_audit": HOSTILE_AUDIT,
        "hostile_preflight": HOSTILE_PREFLIGHT,
        "retirement_receipt": RETIREMENT_RECEIPT,
        "target_consumer": TARGET_CONSUMER,
        **{f"historical_{name}": path for name, path in HISTORICAL_TARGET_PATHS.items()},
        **{f"active_{name}": path for name, path in ACTIVE_TARGET_PATHS.items()},
        **{f"hostile_source_{name}": HOSTILE / name for name in hostile_sources},
        **{
            f"target_source_{name}": ACTIVE_TARGET_PATHS["freeze"].parent / name
            for name in target_sources
        },
    }
    execution_paths = (
        ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L12",
        ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L12.json",
        HOSTILE / "V004R4_WORKSPACES/L12",
        HOSTILE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json",
        ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json",
    )
    return {
        "files": {
            label: hashlib.sha256(path.read_bytes()).hexdigest()
            for label, path in files.items()
        },
        "execution_paths": {
            str(path): os.path.lexists(path) for path in execution_paths
        },
    }


def plan() -> dict[str, object]:
    authenticated = authenticate_static_inputs()
    return {
        "schema": "V012_STAGE3_HISTORICAL_INTERFACE_CUSTODY_PLAN_V001",
        "classification": "MUTABLE_READINESS_ONLY_NOT_EXECUTION_AUTHORITY",
        "unchanged_hostile_consumer_sha256": CONSUMER_SHA256,
        "unchanged_hostile_source_count": len(authenticated["source_hashes"]),
        "historical_build_gate_sha256": GATE_SHA256,
        "retirement_receipt_sha256": RETIREMENT_RECEIPT_SHA256,
        "historical_target_sha256": dict(HISTORICAL_TARGET_SHA256),
        "active_target_sha256": dict(ACTIVE_TARGET_SHA256),
        "historical_paths": {
            name: str(path) for name, path in HISTORICAL_TARGET_PATHS.items()
        },
        "active_paths": {
            name: str(path) for name, path in ACTIVE_TARGET_PATHS.items()
        },
        "dependency_graph": [
            "retirement_receipt -> historical_target_quartet",
            "hostile_freeze -> unchanged_hostile_consumer",
            "historical_build_gate -> historical_target_quartet",
            "temporary_single_boundary -> retained_historical_descriptors",
            "existing_hostile_cache_manifest -> unchanged_historical_build_gate",
        ],
        "patched_boundary": "retain_build_authorization_inputs",
        "patched_boundary_count": 1,
        "launch_available": False,
        "publication_available": False,
        "file_move_available": False,
        "physical_execution_available": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> int:
    if sys.argv[1:] == ["plan"]:
        action = plan
    elif sys.argv[1:] == ["self-test"]:
        action = self_test
    else:
        print("REFUSED: development adapter exposes only plan or self-test", file=sys.stderr)
        return 2
    try:
        result = action()
    except BaseException as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
