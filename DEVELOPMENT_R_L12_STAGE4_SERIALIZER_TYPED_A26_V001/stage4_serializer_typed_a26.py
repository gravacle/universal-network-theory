#!/usr/bin/env python3
"""Mutable Stage-4 serializer-typed readiness bridge.

The frozen A26 bridge and independent final auditor admit JSON inputs only in
their compact serialization.  The actual owner-once authority chain contains
both compact JSON and the older sorted/indented publication serialization.
This module does not alter either family of bytes.  It authenticates the
frozen A26 sources, constructs an exact physical-input registry, and provides
one temporary compatibility scope for the three compact-only read boundaries.

There is intentionally no A26 publication or L12 execution entry point here.
The production scope remains unavailable until all future A20--A25 authority
records exist and an exact complete registry has been frozen and independently
audited.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
import types
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterator


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
FROZEN_PACKET: Final[Path] = (
    ROOT / "AUDIT_PREPARATION_R_L12_FINAL_A26_BRIDGE_V001"
)
FROZEN_BRIDGE: Final[Path] = FROZEN_PACKET / "build_final_a26.py"
FROZEN_MODULE_NAME: Final[str] = "authenticated_frozen_final_a26_bridge_v001"
FINAL_REGISTRY_PATH: Final[Path] = HERE / "AUTHORITY_SERIALIZER_REGISTRY_V001.json"

PINNED_FROZEN_STAGE4: Final[dict[str, str]] = {
    "SOURCE_FREEZE.json":
        "0e976b3e01e0cc0b873a04f94bed294cdb77f460977b36fe84f3d48192fd7f39",
    "build_final_a26.py":
        "1a54a92672f64c8667b9e38e1fa35fdb33395477e4925ecf1d8d6dce56e63b0c",
    "test_build_final_a26.py":
        "2fe2345e571efefcfdc65e869b3541af68cd519e75b9b0a0a3c2201dcb21b3c6",
}
PINNED_FROZEN_DEPENDENCIES: Final[dict[str, str]] = {
    "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/independent_final_auditor.py":
        "99677ffabeedc6db84047bd3637fd292e137d66c2de02eef66633ed789a92f2f",
    "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/production_evidence_orchestrator.py":
        "d85275417f92961a2809822bcfc635d9e23e16bc7ad4fde43183ddcb78620b20",
}

REGISTRY_SCHEMA: Final[str] = "V012_STAGE4_AUTHORITY_SERIALIZER_REGISTRY_V001"
REGISTRY_INCOMPLETE: Final[str] = "MUTABLE_INCOMPLETE_WAITING_FOR_A20_A25"
REGISTRY_COMPLETE: Final[str] = "READY_FOR_FREEZE_AND_HOSTILE_AUDIT_ONLY"
CLAIM_BOUNDARY: Final[str] = (
    "SERIALIZER_TYPED_STAGE4_READINESS_ONLY__NO_A26_PUBLICATION_L12_RESULT_"
    "SECTOR_SPECTRUM_CONTINUUM_OR_GRAVITY"
)
PRETTY: Final[str] = "SORTED_INDENT2_ASCII_LF_V001"
COMPACT: Final[str] = "SORTED_COMPACT_ASCII_LF_V001"
RAW: Final[str] = "RAW_BYTES_V001"
FRAMINGS: Final[frozenset[str]] = frozenset({PRETTY, COMPACT, RAW})
EXPECTED_LOGICAL_AUTHORITIES: Final[int] = 42
EXPECTED_PHYSICAL_INPUTS: Final[int] = 50
EXPECTED_FRAMING_CENSUS: Final[dict[str, int]] = {
    PRETTY: 25,
    COMPACT: 21,
    RAW: 4,
}
FUTURE_ARTIFACT_IDS: Final[frozenset[str]] = frozenset({
    "A20_SHARED_SCHEDULE_GATE", "A21_SHARED_SCHEDULE_AUDIT",
    "A22_TARGET_L12_AUTHORIZATION", "A23_POSTRUN_TELEMETRY",
    "A24_TARGET_L12_HISTORY", "A25_HOSTILE_L12_HISTORY",
})

# The first Stage-3 launch is preserved at the frozen auditor's V001 paths as
# obstruction evidence.  A successful retry is authorized only in this exact,
# disjoint V002 namespace.  Stage 4 must therefore bind A20--A23 to these
# identities and must never fall back to the occupied failed-launch paths.
RETRY_V002_AUTHORITY_RELATIVE_PATHS: Final[
    dict[tuple[str, int], str]
] = {
    ("A20_SHARED_SCHEDULE_GATE", 1):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "SHARED_AGGREGATE_SCHEDULE_GATE_RETRY_V002.json",
    ("A21_SHARED_SCHEDULE_AUDIT", 1):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 1):
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "TARGET_L12_EXECUTION_GATE_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 2):
        "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
        "HOSTILE_L12_EXECUTION_GATE_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 3):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "TARGET_V012_WORKER_READY_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 4):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "HOSTILE_V004R4_WORKER_READY_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 5):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "DUAL_L12_LAUNCH_HANDSHAKE_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 6):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "DUAL_L12_WORKER_RELEASE_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 7):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "TARGET_V012_WORKER_RELEASE_COMMAND_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 8):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "HOSTILE_V004R4_WORKER_RELEASE_COMMAND_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 9):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "TARGET_V012_WORKER_RELEASE_ACK_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 10):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "HOSTILE_V004R4_WORKER_RELEASE_ACK_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 11):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "TARGET_V012_WORKER_COMPLETION_RETRY_V002.json",
    ("A22_TARGET_L12_AUTHORIZATION", 12):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "HOSTILE_V004R4_WORKER_COMPLETION_RETRY_V002.json",
    ("A23_POSTRUN_TELEMETRY", 1):
        "AUDIT_R_L12_PARALLEL_EXECUTION_RETRY_V002/"
        "SHARED_AGGREGATE_TELEMETRY_RETRY_V002.json",
}
RETRY_V002_TELEMETRY_PATH: Final[Path] = (
    ROOT / RETRY_V002_AUTHORITY_RELATIVE_PATHS[
        ("A23_POSTRUN_TELEMETRY", 1)
    ]
)
COMPACT_ORDINARY_IDS: Final[frozenset[str]] = frozenset({
    "A20_SHARED_SCHEDULE_GATE", "A21_SHARED_SCHEDULE_AUDIT",
    "A22_TARGET_L12_AUTHORIZATION", "A23_POSTRUN_TELEMETRY",
    "A25_HOSTILE_L12_HISTORY",
})
PENDING_SHA256: Final[str] = "UNAVAILABLE_PENDING_STAGE3_L12"

# These are the exact owner-once identities present at this readiness boundary.
# They are deliberately constants rather than values discovered from whichever
# bytes happen to occupy the canonical paths when ``plan`` is invoked.
PINNED_CURRENT_AUTHORITY_SHA256: Final[
    dict[tuple[str, int, str | None], str]
] = {
    ("A01_FREEZE_AND_SOURCE_PACKET", 1, None):
        "a6997822fd2daa2be0079e67d81833f1eac69fe01c6ff0b9188560f2c1234395",
    ("A02_NONPHYSICAL_PREFLIGHT", 1, None):
        "73ab3c2778f11b3d768bf818865fac120210b8c5417a1aa0bb19edc874bda57c",
    ("A03_PREPAYLOAD_AUDIT", 1, None):
        "a50044557c5316d50f3b1e4cfefb035c674321a96147690aa3017b2e01cb2301",
    ("A04_UNIVERSAL_CUSTODY_GATE", 1, None):
        "e9e1714852d03cca9e6dcc90745e16a6a7722bf41e29e4717d5032a9cd250256",
    ("A05_FIVE_CACHE_SET", 1, None):
        "1dd52b25ef64a57df5a25cbacdbc2fedceae205835f0eb39068211a484c6940c",
    ("A05_FIVE_CACHE_SET", 2, None):
        "6a135b942fe837ce1806595dcfb2080533974a4beb0265dfdc45a4c3450d59f6",
    ("A05_FIVE_CACHE_SET", 3, None):
        "78210f5b2a2c580fe4b3da6c8db8bdfa060de82239fe6f2d6bfd07ff35a5e4e2",
    ("A05_FIVE_CACHE_SET", 4, None):
        "ac5c8f6299753357be18d7239a0c88e0ff7012cfa566ae2524bbcaae9111fe37",
    ("A05_FIVE_CACHE_SET", 5, None):
        "859e01f5a735eeb10f93960068c1fd048ec6ab085a7f5a1df29f9176f9be1e76",
    ("A06_POSTBUILD_AUDIT", 1, None):
        "160dc8360e647832476ce0da40d3728ab31964217949febe7603aee86dcffc45",
    ("A07_BASE_PHYSICAL_GATE", 1, None):
        "1233104dc6d51e104bd14f2f496242d48e26845957a2382440f9f572aeb4e2d1",
    ("A08_PHYSICAL_GATE_AUDIT", 1, None):
        "e0165be9ef749260b1d993380e26cfa18989171cfbf28670fe74e952c6ce01b4",
    ("A09_CONTROL_AUTHORIZATION", 1, None):
        "a2f9dd391691cfba4c1ad64a821babd3ab7615acf88cd52aacc8b92a1e168c07",
    ("A10_CONTROL_HISTORIES", 1, None):
        "bd84329008b969975be26e61e00defaf52b9f11de2d160488ad953ce0bb27254",
    ("A10_CONTROL_HISTORIES", 2, None):
        "d7d6f111c657d514c3251da1ca8a20db955b5298937b8effe9832eda73d8fbda",
    ("A10_CONTROL_HISTORIES", 3, None):
        "8cbefeccb4ef9273c20d90519d95501ddc4db0ee8c449fc762313ecefcbd232c",
    ("A11_CONTROL_STAGE_GATE", 1, None):
        "0dbba128a7bf4ea6319c64c687181c6cf95207a917c57721d58cef3764da6371",
    ("A12_CONTROL_STAGE_AUDIT", 1, None):
        "4da29efa71259c1e44b42bda8b8d48332940de9d9557c621025b706f4b93392f",
    ("A13_L10_AUTHORIZATION", 1, None):
        "9094d717db0adfb63219cfa8c9779b0db575cccd19c013c0c158d1a34f2a5085",
    ("A14_L10_HISTORY", 1, None):
        "422cd12235d59d44986daf2490e467677c86f7eb82da16f31c8403769cf9675d",
    ("A15_L10_STAGE_GATE", 1, None):
        "20261b35e21d626b61b69a8e29b8dee7c4521bd157aca787aff0fba4524e5ad2",
    ("A16_L10_STAGE_AUDIT", 1, None):
        "5b694804b9d0dfc7b1238ca2d8a3b4342849ffd7beaa9dc64d057633cc2d80a6",
    ("A18_L10_CROSS_GATE", 1, None):
        "84a99de5d97373f8daeb2a1bcf1adcf04d2f0e0ee17dab13f58859d35bf141c5",
    ("A27_MUTATION_LEDGER", 1, None):
        "c8a8b23261d3376d69e2175512ae946ba3cdde96a464ac4ae33cb06010c4bf90",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "method"):
        "e1214f533a4f0476d4db75bd1407a402c1ed0908f7919b376f9c65a27e93b587",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "builder"):
        "da5fa4484ce56993cbb0d4b411cad638836cb1ebe272c89a52ff33e382fff8f1",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "consumer"):
        "700dce18ec8f50008a9e3022394a55c8d689268e21b80982896d37b92add7b74",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "preflight"):
        "ecf7a568acb3b440fbfee483bad9526d3d1d6eff5f7f7f2cda8e4486b2f94678",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "freeze"):
        "6c0d2efa83584a91df52f299d679e5baab8913cccc6955ddfc2dbeb43a87814a",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "preflight_result"):
        "a0723a0caf9c826601984b99484227cb5da613608c8887edeeea234e54649f50",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "independent_audit"):
        "7b4f677615d4688b3911e5350ce99bbd85e922786866648ac414866e1e3ddc32",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "cached_L10_gate"):
        "c61f3a50a544fe3fa21c97bbdc3115740d7926329b543e7f4dc0bc16a9ce6d5a",
    ("A17_HOSTILE_L12_ELIGIBILITY", 1, "L12_cache_manifest"):
        "734998db87ff7358706b56f692fe5cd6832442987b7267f5325915b53d5b43ed",
}


class CompatibilityRefusal(RuntimeError):
    """The serializer-typed Stage-4 readiness contract refused closed."""


def _identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev, metadata.st_ino, metadata.st_size,
        metadata.st_mtime_ns, metadata.st_ctime_ns, metadata.st_nlink,
        stat.S_IMODE(metadata.st_mode), stat.S_IFMT(metadata.st_mode),
    )


def _require_canonical_repository_path(path: Path, label: str) -> None:
    if (
        not isinstance(path, Path) or not path.is_absolute()
        or Path(str(path)) != path or ROOT not in path.parents
        or "\x00" in str(path)
    ):
        raise CompatibilityRefusal(f"{label} path is not canonical")
    cursor = Path(path.anchor)
    for component in path.parts[1:-1]:
        cursor /= component
        try:
            metadata = os.stat(cursor, follow_symlinks=False)
        except OSError as error:
            raise CompatibilityRefusal(f"{label} parent is absent") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise CompatibilityRefusal(f"{label} parent is aliased or special")


def _read_exact_owner_once(
    path: Path, expected_sha256: str, label: str,
) -> bytes:
    if (
        type(expected_sha256) is not str or len(expected_sha256) != 64
        or any(character not in "0123456789abcdef" for character in expected_sha256)
    ):
        raise CompatibilityRefusal(f"{label} expected SHA-256 is malformed")
    _require_canonical_repository_path(path, label)
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_descriptor = -1
    descriptor = -1
    try:
        parent_descriptor = os.open(path.parent, parent_flags)
        parent_before = os.fstat(parent_descriptor)
        parent_named = os.stat(path.parent, follow_symlinks=False)
        if (
            not stat.S_ISDIR(parent_before.st_mode)
            or (parent_before.st_dev, parent_before.st_ino)
            != (parent_named.st_dev, parent_named.st_ino)
        ):
            raise CompatibilityRefusal(f"{label} parent identity mismatch")
        descriptor = os.open(path.name, file_flags, dir_fd=parent_descriptor)
        before = os.fstat(descriptor)
        named_before = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(before.st_mode) or before.st_mode & 0o222
            or before.st_nlink != 1 or _identity(before) != _identity(named_before)
        ):
            raise CompatibilityRefusal(
                f"{label} is not an immutable owner-once ordinary file"
            )
        raw = bytearray()
        offset = 0
        while offset < before.st_size:
            block = os.pread(
                descriptor, min(16 * 2**20, before.st_size - offset), offset,
            )
            if not block:
                raise CompatibilityRefusal(f"{label} retained read was short")
            raw.extend(block)
            offset += len(block)
        after = os.fstat(descriptor)
        named_after = os.stat(
            path.name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
        parent_after = os.fstat(parent_descriptor)
        parent_named_after = os.stat(path.parent, follow_symlinks=False)
        digest = hashlib.sha256(raw).hexdigest()
        if (
            _identity(after) != _identity(before)
            or _identity(named_after) != _identity(before)
            or (parent_after.st_dev, parent_after.st_ino)
            != (parent_before.st_dev, parent_before.st_ino)
            or (parent_named_after.st_dev, parent_named_after.st_ino)
            != (parent_before.st_dev, parent_before.st_ino)
            or digest != expected_sha256
        ):
            raise CompatibilityRefusal(f"{label} changed or has the wrong digest")
        return bytes(raw)
    except OSError as error:
        raise CompatibilityRefusal(f"{label} cannot be retained") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if parent_descriptor >= 0:
            os.close(parent_descriptor)


def _strict_object(raw: bytes, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise CompatibilityRefusal(f"{label} has a duplicate JSON key")
            result[key] = value
        return result

    def constant(_token: str) -> object:
        raise CompatibilityRefusal(f"{label} has a nonfinite JSON constant")

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=constant,
        )
    except CompatibilityRefusal:
        raise
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise CompatibilityRefusal(f"{label} is not strict ASCII JSON") from error
    if type(value) is not dict:
        raise CompatibilityRefusal(f"{label} is not one JSON object")
    return value


def _serialize(value: object, framing: str) -> bytes:
    if framing == PRETTY:
        parameters = {"indent": 2, "sort_keys": True}
    elif framing == COMPACT:
        parameters = {"sort_keys": True, "separators": (",", ":")}
    else:
        raise CompatibilityRefusal("JSON serializer requested for a raw input")
    try:
        return (json.dumps(
            value, ensure_ascii=True, allow_nan=False, **parameters,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise CompatibilityRefusal("record is not finite serializer-typed JSON") from error


def _require_exact_frame(raw: bytes, framing: str, label: str) -> dict[str, object]:
    if framing == RAW:
        raise CompatibilityRefusal(f"{label} is raw, not JSON")
    record = _strict_object(raw, label)
    if _serialize(record, framing) != raw:
        raise CompatibilityRefusal(f"{label} serializer framing mismatch")
    return record


def _authenticate_frozen_stage4_sources() -> dict[Path, bytes]:
    sources: dict[Path, bytes] = {}
    for name, digest in PINNED_FROZEN_STAGE4.items():
        path = FROZEN_PACKET / name
        sources[path] = _read_exact_owner_once(
            path, digest, f"frozen Stage4 {name}",
        )
    for relative, digest in PINNED_FROZEN_DEPENDENCIES.items():
        path = ROOT / relative
        sources[path] = _read_exact_owner_once(
            path, digest, f"frozen Stage4 dependency {relative}",
        )
    freeze = _strict_object(
        sources[FROZEN_PACKET / "SOURCE_FREEZE.json"],
        "frozen Stage4 SOURCE_FREEZE",
    )
    if _serialize(freeze, COMPACT) != sources[FROZEN_PACKET / "SOURCE_FREEZE.json"]:
        raise CompatibilityRefusal("frozen Stage4 SOURCE_FREEZE framing mismatch")
    if freeze.get("files") != {
        "AUDIT_PREPARATION_R_L12_FINAL_A26_BRIDGE_V001/build_final_a26.py":
            PINNED_FROZEN_STAGE4["build_final_a26.py"],
        "AUDIT_PREPARATION_R_L12_FINAL_A26_BRIDGE_V001/test_build_final_a26.py":
            PINNED_FROZEN_STAGE4["test_build_final_a26.py"],
        **PINNED_FROZEN_DEPENDENCIES,
    }:
        raise CompatibilityRefusal("frozen Stage4 SOURCE_FREEZE source census mismatch")
    return sources


def _execute_frozen_bridge(
    module_name: str = FROZEN_MODULE_NAME,
) -> types.ModuleType:
    if type(module_name) is not str or not module_name:
        raise CompatibilityRefusal("frozen bridge module name is malformed")
    if module_name in sys.modules:
        raise CompatibilityRefusal("frozen bridge module alias is already occupied")
    sources = _authenticate_frozen_stage4_sources()
    raw = sources[FROZEN_BRIDGE]
    module = types.ModuleType(module_name)
    module.__file__ = str(FROZEN_BRIDGE)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = PINNED_FROZEN_STAGE4["build_final_a26.py"]
    sys.modules[module_name] = module
    try:
        exec(
            compile(raw, str(FROZEN_BRIDGE), "exec", dont_inherit=True),
            module.__dict__,
        )
        module.verify_frozen_source_closure()
        _authenticate_frozen_stage4_sources()
        return module
    except BaseException:
        if sys.modules.get(module_name) is module:
            sys.modules.pop(module_name, None)
        raise


_FROZEN_BRIDGE_MODULE: types.ModuleType | None = None
_FROZEN_RUNTIME_IDENTITIES: dict[str, object] | None = None
_FROZEN_RUNTIME_STRUCTURE: tuple[object, ...] | None = None


def _runtime_identity_map(module: types.ModuleType) -> dict[str, object]:
    """Return the proof-relevant callables loaded from retained frozen bytes."""
    return {
        "bridge.verify_frozen_source_closure":
            module.verify_frozen_source_closure,
        "bridge.open_canonical_record": module.open_canonical_record,
        "bridge.build_authority_bindings": module.build_authority_bindings,
        "bridge.publish_live_a26": module.publish_live_a26,
        "bridge.construct_a26_record": module.construct_a26_record,
        "auditor._open_immutable_json": module.auditor._open_immutable_json,
        "auditor._open_retained_file": module.auditor._open_retained_file,
        "auditor._descriptor_bytes": module.auditor._descriptor_bytes,
        "auditor._expected_path": module.auditor._expected_path,
        "auditor.validate_artifact": module.auditor.validate_artifact,
        "evidence.open_authority": module.evidence.open_authority,
        "evidence.canonical_json_bytes": module.evidence.canonical_json_bytes,
        "evidence._atomic_publish_once": module.evidence._atomic_publish_once,
        "evidence.FinalEvidenceOrchestrator":
            module.evidence.FinalEvidenceOrchestrator,
    }


def _runtime_structure(module: types.ModuleType) -> tuple[object, ...]:
    """Snapshot immutable values that select authority paths and identities."""
    auditor = module.auditor
    evidence = module.evidence
    return (
        tuple(sorted(auditor.AUTHORITY_INSTANCE_CENSUS.items())),
        tuple(sorted(
            (artifact_id, instance, relative)
            for (artifact_id, instance), relative
            in auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS.items()
        )),
        tuple(auditor.A17_SOURCE_LABELS),
        tuple(sorted(auditor.A17_CANONICAL_RELATIVE_PATHS.items())),
        tuple(sorted(auditor.A17_RECORD_IDENTITIES.items())),
        tuple(evidence.PREDECESSOR_IDS),
        tuple(sorted(evidence.CANONICAL_PREDECESSOR_PATHS.items())),
        tuple(sorted(evidence.CANONICAL_OUTPUT_PATHS.items())),
    )


def _verify_frozen_runtime_identity(
    module: types.ModuleType,
    expected: dict[str, object] | None = None,
    expected_structure: tuple[object, ...] | None = None,
) -> None:
    baseline = _FROZEN_RUNTIME_IDENTITIES if expected is None else expected
    if baseline is None:
        raise CompatibilityRefusal("frozen runtime identity baseline is absent")
    if (
        sys.modules.get(FROZEN_MODULE_NAME) is not module
        or sys.modules.get("independent_final_auditor") is not module.auditor
        or sys.modules.get("production_evidence_orchestrator") is not module.evidence
    ):
        raise CompatibilityRefusal("authenticated frozen runtime module alias changed")
    if (
        _FROZEN_RUNTIME_STRUCTURE is None
        or _runtime_structure(module) != (
            _FROZEN_RUNTIME_STRUCTURE
            if expected_structure is None else expected_structure
        )
    ):
        raise CompatibilityRefusal("authenticated frozen runtime structure changed")
    observed = _runtime_identity_map(module)
    if set(observed) != set(baseline) or any(
        observed[name] is not value for name, value in baseline.items()
    ):
        raise CompatibilityRefusal("authenticated frozen runtime callable changed")
    verify = baseline["bridge.verify_frozen_source_closure"]
    verify()


def frozen_bridge() -> types.ModuleType:
    global _FROZEN_BRIDGE_MODULE, _FROZEN_RUNTIME_IDENTITIES
    global _FROZEN_RUNTIME_STRUCTURE
    if _FROZEN_BRIDGE_MODULE is None:
        _FROZEN_BRIDGE_MODULE = _execute_frozen_bridge()
        _FROZEN_RUNTIME_IDENTITIES = _runtime_identity_map(
            _FROZEN_BRIDGE_MODULE,
        )
        _FROZEN_RUNTIME_STRUCTURE = _runtime_structure(
            _FROZEN_BRIDGE_MODULE,
        )
    _verify_frozen_runtime_identity(_FROZEN_BRIDGE_MODULE)
    return _FROZEN_BRIDGE_MODULE


@dataclass(frozen=True)
class InputSpec:
    artifact_id: str
    instance: int
    source_label: str | None
    relative_path: str
    framing: str

    @property
    def key(self) -> tuple[str, int, str | None]:
        return self.artifact_id, self.instance, self.source_label


def expected_input_specs() -> tuple[InputSpec, ...]:
    bridge = frozen_bridge()
    auditor = bridge.auditor
    result: list[InputSpec] = []
    for artifact_id, count in auditor.AUTHORITY_INSTANCE_CENSUS.items():
        for instance in range(1, count + 1):
            if artifact_id == "A17_HOSTILE_L12_ELIGIBILITY":
                continue
            key = (artifact_id, instance)
            relative = RETRY_V002_AUTHORITY_RELATIVE_PATHS.get(
                key, auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[key],
            )
            framing = COMPACT if artifact_id in COMPACT_ORDINARY_IDS else PRETTY
            result.append(InputSpec(
                artifact_id, instance, None, relative, framing,
            ))
    for label in auditor.A17_SOURCE_LABELS:
        framing = COMPACT if label in auditor.A17_RECORD_IDENTITIES else RAW
        result.append(InputSpec(
            "A17_HOSTILE_L12_ELIGIBILITY", 1, label,
            auditor.A17_CANONICAL_RELATIVE_PATHS[label], framing,
        ))
    current_keys = {
        item.key for item in result
        if item.artifact_id not in FUTURE_ARTIFACT_IDS
    }
    retry_keys = {
        (item.artifact_id, item.instance): item.relative_path
        for item in result
        if (item.artifact_id, item.instance)
        in RETRY_V002_AUTHORITY_RELATIVE_PATHS
    }
    if (
        len(result) != EXPECTED_PHYSICAL_INPUTS
        or len({item.key for item in result}) != len(result)
        or len({item.relative_path for item in result}) != len(result)
        or {
            framing: sum(item.framing == framing for item in result)
            for framing in FRAMINGS
        } != EXPECTED_FRAMING_CENSUS
        or set(PINNED_CURRENT_AUTHORITY_SHA256) != current_keys
        or retry_keys != RETRY_V002_AUTHORITY_RELATIVE_PATHS
        or any(
            RETRY_V002_AUTHORITY_RELATIVE_PATHS[key]
            == auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[key]
            for key in RETRY_V002_AUTHORITY_RELATIVE_PATHS
        )
    ):
        raise CompatibilityRefusal("internal Stage4 input census mismatch")
    return tuple(result)


def _discover_entry(spec: InputSpec) -> dict[str, object]:
    path = ROOT / spec.relative_path
    exists = os.path.lexists(path)
    if spec.artifact_id in FUTURE_ARTIFACT_IDS:
        # In-flight Stage3 records are not self-admitted.  ``present`` here
        # means that an exact expected identity is available to this registry,
        # not merely that a pathname has appeared during a concurrent run.
        return {
            "artifact_id": spec.artifact_id,
            "instance": spec.instance,
            "source_label": spec.source_label,
            "relative_path": spec.relative_path,
            "framing": spec.framing,
            "present": False,
            "bytes": None,
            "raw_sha256": PENDING_SHA256,
        }
    if not exists:
        raise CompatibilityRefusal(
            f"nonfuture authority is absent: {spec.artifact_id}:{spec.instance}"
        )
    digest = PINNED_CURRENT_AUTHORITY_SHA256.get(spec.key)
    if digest is None:
        raise CompatibilityRefusal("current authority has no pinned exact identity")
    raw = _read_exact_owner_once(
        path, digest,
        f"Stage4 registry {spec.artifact_id}:{spec.instance}:{spec.source_label}",
    )
    if spec.framing != RAW:
        _require_exact_frame(raw, spec.framing, spec.relative_path)
    return {
        "artifact_id": spec.artifact_id,
        "instance": spec.instance,
        "source_label": spec.source_label,
        "relative_path": spec.relative_path,
        "framing": spec.framing,
        "present": True,
        "bytes": len(raw),
        "raw_sha256": digest,
    }


def _a17_composite_sha256(entries: list[dict[str, object]]) -> str:
    bridge = frozen_bridge()
    auditor = bridge.auditor
    by_label = {
        item["source_label"]: item for item in entries
        if item["artifact_id"] == "A17_HOSTILE_L12_ELIGIBILITY"
    }
    if set(by_label) != set(auditor.A17_SOURCE_LABELS):
        raise CompatibilityRefusal("A17 physical-source census mismatch")
    branch: dict[str, object] = {"role": "hostile_v004r4"}
    for label in auditor.A17_SOURCE_LABELS:
        item = by_label[label]
        digest = item["raw_sha256"]
        if type(digest) is not str:
            raise CompatibilityRefusal("A17 source digest is absent")
        binding: dict[str, object] = {
            "path": str(ROOT / str(item["relative_path"])),
            "sha256": digest,
        }
        if label in auditor.A17_RECORD_IDENTITIES:
            schema, identity_field, identity_value = (
                auditor.A17_RECORD_IDENTITIES[label]
            )
            binding.update({
                "schema": schema,
                "identity_field": identity_field,
                "identity_value": identity_value,
            })
        branch[label] = binding
    return hashlib.sha256(_serialize(branch, COMPACT)).hexdigest()


def build_registry_draft() -> dict[str, object]:
    entries = [_discover_entry(spec) for spec in expected_input_specs()]
    missing = [
        f"{item['artifact_id']}:{item['instance']}"
        for item in entries if item["present"] is False
    ]
    present_framing = {
        framing: sum(
            item["present"] is True and item["framing"] == framing
            for item in entries
        )
        for framing in sorted(FRAMINGS)
    }
    return {
        "schema": REGISTRY_SCHEMA,
        "status": REGISTRY_INCOMPLETE if missing else REGISTRY_COMPLETE,
        "frozen_stage4_sha256": {
            **{
                f"AUDIT_PREPARATION_R_L12_FINAL_A26_BRIDGE_V001/{name}": digest
                for name, digest in PINNED_FROZEN_STAGE4.items()
            },
            **PINNED_FROZEN_DEPENDENCIES,
        },
        "logical_authority_census": EXPECTED_LOGICAL_AUTHORITIES,
        "physical_input_census": EXPECTED_PHYSICAL_INPUTS,
        "expected_framing_census": dict(EXPECTED_FRAMING_CENSUS),
        "present_framing_census": present_framing,
        "present_input_count": sum(item["present"] is True for item in entries),
        "missing_authorities": missing,
        "a17_logical_composite_sha256": _a17_composite_sha256(entries),
        "entries": entries,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def registry_json_bytes(record: object) -> bytes:
    return _serialize(record, COMPACT)


@dataclass(frozen=True)
class ValidatedRegistry:
    record: dict[str, object]
    entries_by_path: dict[str, dict[str, object]]
    complete: bool

    def lookup(self, path: Path | str, digest: str) -> dict[str, object] | None:
        path_text = str(path)
        item = self.entries_by_path.get(path_text)
        if item is None:
            return None
        if item["present"] is not True or item["raw_sha256"] != digest:
            raise CompatibilityRefusal(
                f"registered Stage4 authority hash mismatch: {item['artifact_id']}"
            )
        return item


def _validate_registry_shape(
    record: object, *, require_complete: bool,
) -> ValidatedRegistry:
    if type(record) is not dict or set(record) != {
        "schema", "status", "frozen_stage4_sha256",
        "logical_authority_census", "physical_input_census",
        "expected_framing_census", "present_framing_census",
        "present_input_count", "missing_authorities",
        "a17_logical_composite_sha256", "entries", "claim_boundary",
    }:
        raise CompatibilityRefusal("registry top-level census mismatch")
    if (
        record["schema"] != REGISTRY_SCHEMA
        or record["frozen_stage4_sha256"] != {
            **{
                f"AUDIT_PREPARATION_R_L12_FINAL_A26_BRIDGE_V001/{name}": digest
                for name, digest in PINNED_FROZEN_STAGE4.items()
            },
            **PINNED_FROZEN_DEPENDENCIES,
        }
        or record["logical_authority_census"] != EXPECTED_LOGICAL_AUTHORITIES
        or type(record["logical_authority_census"]) is not int
        or record["physical_input_census"] != EXPECTED_PHYSICAL_INPUTS
        or type(record["physical_input_census"]) is not int
        or record["expected_framing_census"] != EXPECTED_FRAMING_CENSUS
        or record["claim_boundary"] != CLAIM_BOUNDARY
    ):
        raise CompatibilityRefusal("registry identity/census mismatch")
    entries = record["entries"]
    specs = expected_input_specs()
    if type(entries) is not list or len(entries) != len(specs):
        raise CompatibilityRefusal("registry entry census mismatch")
    expected_keys = {
        "artifact_id", "instance", "source_label", "relative_path",
        "framing", "present", "bytes", "raw_sha256",
    }
    paths: set[str] = set()
    digests: set[str] = set()
    missing: list[str] = []
    present_framing = {framing: 0 for framing in sorted(FRAMINGS)}
    absolute: dict[str, dict[str, object]] = {}
    for item, spec in zip(entries, specs):
        if (
            type(item) is not dict or set(item) != expected_keys
            or item["artifact_id"] != spec.artifact_id
            or item["instance"] != spec.instance
            or type(item["instance"]) is not int
            or item["source_label"] != spec.source_label
            or item["relative_path"] != spec.relative_path
            or item["framing"] != spec.framing
            or item["framing"] not in FRAMINGS
            or type(item["present"]) is not bool
            or item["relative_path"] in paths
        ):
            raise CompatibilityRefusal("registry entry identity/order mismatch")
        paths.add(item["relative_path"])
        if item["present"]:
            digest = item["raw_sha256"]
            if (
                type(item["bytes"]) is not int or item["bytes"] < 0
                or type(digest) is not str or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
                or digest in digests
                or (
                    spec.artifact_id not in FUTURE_ARTIFACT_IDS
                    and digest != PINNED_CURRENT_AUTHORITY_SHA256.get(spec.key)
                )
            ):
                raise CompatibilityRefusal("registry raw identity mismatch")
            digests.add(digest)
            present_framing[item["framing"]] += 1
        else:
            if (
                item["bytes"] is not None
                or item["raw_sha256"] != PENDING_SHA256
                or item["artifact_id"] not in FUTURE_ARTIFACT_IDS
            ):
                raise CompatibilityRefusal("registry absence contract mismatch")
            missing.append(f"{item['artifact_id']}:{item['instance']}")
        absolute[str(ROOT / spec.relative_path)] = item
    if (
        record["present_input_count"] != len(entries) - len(missing)
        or type(record["present_input_count"]) is not int
        or record["present_framing_census"] != present_framing
        or record["missing_authorities"] != missing
        or type(record["missing_authorities"]) is not list
        or record["a17_logical_composite_sha256"]
        != _a17_composite_sha256(entries)
    ):
        raise CompatibilityRefusal("registry reconstruction mismatch")
    complete = not missing
    expected_status = REGISTRY_COMPLETE if complete else REGISTRY_INCOMPLETE
    if record["status"] != expected_status or (require_complete and not complete):
        raise CompatibilityRefusal("complete Stage4 serializer registry is absent")
    return ValidatedRegistry(record, absolute, complete)


def validate_registry(
    record: object, *, require_complete: bool, verify_files: bool = True,
) -> ValidatedRegistry:
    validated = _validate_registry_shape(record, require_complete=require_complete)
    if verify_files:
        for path_text, item in validated.entries_by_path.items():
            if item["present"] is not True:
                continue
            raw = _read_exact_owner_once(
                Path(path_text), str(item["raw_sha256"]),
                f"registered {item['artifact_id']}:{item['instance']}",
            )
            if len(raw) != item["bytes"]:
                raise CompatibilityRefusal("registered input byte census mismatch")
            if item["framing"] != RAW:
                _require_exact_frame(raw, str(item["framing"]), path_text)
    return validated


def open_complete_registry(
    path: Path, expected_sha256: str,
) -> ValidatedRegistry:
    if path != FINAL_REGISTRY_PATH:
        raise CompatibilityRefusal("final registry path is not canonical")
    raw = _read_exact_owner_once(path, expected_sha256, "final Stage4 registry")
    record = _strict_object(raw, "final Stage4 registry")
    if registry_json_bytes(record) != raw:
        raise CompatibilityRefusal("final Stage4 registry is not compact canonical JSON")
    return validate_registry(record, require_complete=True, verify_files=True)


_EVIDENCE_SERIALIZER: ContextVar[dict[str, object] | None] = ContextVar(
    "stage4_evidence_serializer", default=None,
)
_PATCH_ACTIVE = False


@contextmanager
def _typed_read_scope(
    registry: ValidatedRegistry, *, readiness_test: bool = False,
) -> Iterator[None]:
    """Patch the exact typed readers and V002 authority paths; never publish."""
    global _PATCH_ACTIVE
    if type(registry) is not ValidatedRegistry:
        raise CompatibilityRefusal("validated serializer registry is required")
    if not registry.complete and not readiness_test:
        raise CompatibilityRefusal("incomplete registry cannot enter production scope")
    if _PATCH_ACTIVE:
        raise CompatibilityRefusal("serializer compatibility scope is already active")
    bridge = frozen_bridge()
    auditor = bridge.auditor
    evidence = bridge.evidence
    originals = {
        "bridge_open": bridge.open_canonical_record,
        "auditor_open": auditor._open_immutable_json,
        "auditor_expected_path": auditor._expected_path,
        "auditor_authority_paths": dict(
            auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS
        ),
        "evidence_open": evidence.open_authority,
        "evidence_serializer": evidence.canonical_json_bytes,
        "evidence_predecessor_paths": dict(
            evidence.CANONICAL_PREDECESSOR_PATHS
        ),
        "evidence_output_paths": dict(evidence.CANONICAL_OUTPUT_PATHS),
    }
    live = {"active": True}
    expected_runtime = dict(_FROZEN_RUNTIME_IDENTITIES or {})
    expected_structure = _FROZEN_RUNTIME_STRUCTURE

    def require_live() -> None:
        if not live["active"]:
            raise CompatibilityRefusal("serializer compatibility capability expired")
        _verify_frozen_runtime_identity(
            bridge, expected_runtime, expected_structure,
        )

    def bridge_open(path: Path, digest: str, label: str):
        require_live()
        item = registry.lookup(path, digest)
        if item is None or item["framing"] == COMPACT:
            return originals["bridge_open"](path, digest, label)
        if item["instance"] != 1 or label != item["artifact_id"]:
            raise CompatibilityRefusal("bridge authority registry identity mismatch")
        retained = bridge.RetainedInput.open(
            path, digest, label, maximum_bytes=bridge.MAX_PREDECESSOR_JSON_BYTES,
        )
        try:
            record = _require_exact_frame(retained.raw, str(item["framing"]), label)
            retained.verify()
            return record, retained
        except BaseException:
            retained.close()
            raise

    def auditor_open(path_text: str, digest: str, aid: str, label: str):
        require_live()
        item = registry.lookup(path_text, digest)
        if item is None or item["framing"] == COMPACT:
            return originals["auditor_open"](path_text, digest, aid, label)
        expected_label = (
            f"A17 {item['source_label']}"
            if item["source_label"] is not None
            else f"authority {item['artifact_id']}:{item['instance']}"
        )
        if aid != "A26_FINAL_L12_AUDIT" or label != expected_label:
            raise CompatibilityRefusal("auditor authority registry identity mismatch")
        retained = auditor._open_retained_file(path_text, digest, aid, label)
        try:
            raw = auditor._descriptor_bytes(
                retained.descriptor, retained.before[2], aid, label,
            )
            if hashlib.sha256(raw).hexdigest() != digest:
                raise CompatibilityRefusal(f"{label} raw hash mismatch")
            record = _require_exact_frame(raw, str(item["framing"]), label)
            retained.verify()
            return record, retained
        except BaseException:
            retained.close()
            raise

    def evidence_serializer(record: object) -> bytes:
        context = _EVIDENCE_SERIALIZER.get()
        if context is None:
            return originals["evidence_serializer"](record)
        require_live()
        return _serialize(record, str(context["framing"]))

    def evidence_open(
        artifact_id: str, path: str, digest: str, validator,
    ):
        require_live()
        item = registry.lookup(path, digest)
        if item is None:
            return originals["evidence_open"](
                artifact_id, path, digest, validator,
            )
        if (
            item["artifact_id"] != artifact_id or item["instance"] != 1
            or artifact_id not in evidence.PREDECESSOR_IDS
        ):
            raise CompatibilityRefusal("evidence authority registry identity mismatch")

        # The framing override is only for the stored-byte equality check in
        # ``open_authority``.  The semantic validator must retain the frozen
        # compact canonical serializer used for all record hashes and for the
        # eventual A26 publication.
        def compact_validator(*args, **kwargs):
            validator_token = _EVIDENCE_SERIALIZER.set(None)
            try:
                return validator(*args, **kwargs)
            finally:
                _EVIDENCE_SERIALIZER.reset(validator_token)

        token = _EVIDENCE_SERIALIZER.set(item)
        try:
            return originals["evidence_open"](
                artifact_id, path, digest, compact_validator,
            )
        finally:
            _EVIDENCE_SERIALIZER.reset(token)

    def auditor_expected_path(
        role: str, kind: str, fixture_mode: bool, q: int | None = None,
    ) -> str:
        require_live()
        if not fixture_mode and kind == "telemetry":
            return str(RETRY_V002_TELEMETRY_PATH)
        return originals["auditor_expected_path"](
            role, kind, fixture_mode, q,
        )

    _PATCH_ACTIVE = True
    bridge.open_canonical_record = bridge_open
    auditor._open_immutable_json = auditor_open
    auditor._expected_path = auditor_expected_path
    for key, relative in RETRY_V002_AUTHORITY_RELATIVE_PATHS.items():
        auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS[key] = relative
    evidence.open_authority = evidence_open
    evidence.canonical_json_bytes = evidence_serializer
    evidence.CANONICAL_PREDECESSOR_PATHS["A23_POSTRUN_TELEMETRY"] = str(
        RETRY_V002_TELEMETRY_PATH
    )
    evidence.CANONICAL_OUTPUT_PATHS["A23_POSTRUN_TELEMETRY"] = str(
        RETRY_V002_TELEMETRY_PATH
    )
    expected_runtime.update({
        "bridge.open_canonical_record": bridge_open,
        "auditor._open_immutable_json": auditor_open,
        "auditor._expected_path": auditor_expected_path,
        "evidence.open_authority": evidence_open,
        "evidence.canonical_json_bytes": evidence_serializer,
    })
    expected_structure = _runtime_structure(bridge)
    _verify_frozen_runtime_identity(
        bridge, expected_runtime, expected_structure,
    )
    primary: BaseException | None = None
    try:
        yield
    except BaseException as error:
        primary = error
        raise
    finally:
        live["active"] = False
        drift = (
            bridge.open_canonical_record is not bridge_open
            or auditor._open_immutable_json is not auditor_open
            or auditor._expected_path is not auditor_expected_path
            or evidence.open_authority is not evidence_open
            or evidence.canonical_json_bytes is not evidence_serializer
            or _runtime_structure(bridge) != expected_structure
        )
        bridge.open_canonical_record = originals["bridge_open"]
        auditor._open_immutable_json = originals["auditor_open"]
        auditor._expected_path = originals["auditor_expected_path"]
        auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS.clear()
        auditor.AUTHORITY_CANONICAL_RELATIVE_PATHS.update(
            originals["auditor_authority_paths"]
        )
        evidence.open_authority = originals["evidence_open"]
        evidence.canonical_json_bytes = originals["evidence_serializer"]
        evidence.CANONICAL_PREDECESSOR_PATHS.clear()
        evidence.CANONICAL_PREDECESSOR_PATHS.update(
            originals["evidence_predecessor_paths"]
        )
        evidence.CANONICAL_OUTPUT_PATHS.clear()
        evidence.CANONICAL_OUTPUT_PATHS.update(
            originals["evidence_output_paths"]
        )
        _PATCH_ACTIVE = False
        _verify_frozen_runtime_identity(bridge)
        if drift and primary is None:
            raise CompatibilityRefusal("serializer read boundary changed in scope")


@contextmanager
def production_typed_read_scope(
    registry_path: Path, registry_sha256: str,
) -> Iterator[None]:
    """Future-only scope; presently refuses because the final registry is absent."""
    registry = open_complete_registry(registry_path, registry_sha256)
    with _typed_read_scope(registry):
        yield


def plan() -> dict[str, object]:
    bridge = frozen_bridge()
    bridge.verify_frozen_source_closure()
    registry = build_registry_draft()
    validated = validate_registry(
        registry, require_complete=False, verify_files=True,
    )
    a26_path = Path(
        bridge.evidence.CANONICAL_OUTPUT_PATHS["A26_FINAL_L12_AUDIT"]
    )
    if os.path.lexists(a26_path):
        raise CompatibilityRefusal("canonical A26 unexpectedly exists")
    observed_pending = [
        f"{spec.artifact_id}:{spec.instance}"
        for spec in expected_input_specs()
        if spec.artifact_id in FUTURE_ARTIFACT_IDS
        and os.path.lexists(ROOT / spec.relative_path)
    ]
    return {
        "schema": "V012_STAGE4_SERIALIZER_TYPED_A26_READINESS_PLAN_V001",
        "classification": "MUTABLE_READINESS_ONLY_NOT_EXECUTABLE_CERTIFICATION",
        "logical_authority_census": registry["logical_authority_census"],
        "physical_input_census": registry["physical_input_census"],
        "present_input_count": registry["present_input_count"],
        "missing_input_count": len(registry["missing_authorities"]),
        "observed_pending_authorities": observed_pending,
        "observed_pending_input_count": len(observed_pending),
        "present_framing_census": registry["present_framing_census"],
        "expected_framing_census": registry["expected_framing_census"],
        "missing_authorities": registry["missing_authorities"],
        "a17_logical_composite_sha256": registry["a17_logical_composite_sha256"],
        "complete_registry": validated.complete,
        "canonical_a26_present": False,
        "patched": False,
        "published": False,
        "executed": False,
        "blocker": (
            "A20_A25_EXACT_AUTHENTICATED_IDENTITIES_ARE_NOT_ALL_AVAILABLE__"
            "REGISTRY_CANNOT_BE_FROZEN_OR_CERTIFIED"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> int:
    if sys.argv[1:] != ["plan"]:
        print("REFUSED: mutable Stage4 candidate exposes only plan", file=sys.stderr)
        return 2
    try:
        result = plan()
    except BaseException as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
