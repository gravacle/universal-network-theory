#!/usr/bin/env python3
"""Fail-closed custody, JSON, freeze, and relocation checks for this packet.

This module authenticates inputs only.  In particular, checking the L8 shard
headers and hashes is not an L8 conductance extraction and never evaluates an
L8 observable.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import stat
from pathlib import Path, PurePosixPath
from typing import Any, Callable, TypeVar


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
MANIFEST = PACKET / "SOURCE_MANIFEST.json"
RECEIPT = PACKET / "MIGRATION_RECEIPT.json"

UNRESOLVED = "L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_UNRESOLVED"
CLAIM_BOUNDARY = (
    "FINITE_L8_OPERATOR_INCIDENCE_ASSOCIATION_ONLY__NO_SCALING_CONTINUUM_"
    "SPACETIME_CURVATURE_RGRL_WTC_OR_GRAVITY"
)
HISTORICAL_ROOT_PREFIX = (
    "/Users/brianmulconrey/PerInfo/where-atoms-come-from/audited-386ee2c/"
)

FROZEN_HASHES = {
    "README.md": "7682e0446362a95aa1df59f46d1ec60d030bb4ce533ebd5ede02538bac4764c9",
    "PROTOCOL.md": "357e2c826372f04084d2eb92a6becd0d07bdd0fd7fbeec71a9815af381853259",
    "FREEZE.json": "ceb13514be61b69ac89d8a55e915222133c6a73395d209070530e0a738444d3d",
}
RECEIPT_HASH = "07c06035aa2b5290eb556acdd01c7631bd827f7b2ff895d9b0d402d6c1929018"
SOURCE_RECORDS = {
    "MIGRATION_CONTEXT_AUDIT_2026-09-27_V001/INVENTORY.json": (
        10156,
        "68d69d9596d4f135bf7fe5700594c773d68d86cba0c5b91f52abfcbb1786a419",
    ),
    "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py": (
        25392,
        "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7",
    ),
    "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py": (
        17774,
        "24ea3626fda443dd4ae5076c7766e1aaca77ff5ce9f22c05bae96943fc627d55",
    ),
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L4.json": (
        15058,
        "754cc0876a31a0b6ff84aa44cfb3043e8d68964c9b29076ea2e565fd07e1f87c",
    ),
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L8.json": (
        26197,
        "ff55ddd70c3f5e3664e1a61384f211a86e9fcc5bcec2d7e02251d387bd17c786",
    ),
}

HISTORY_TOP_KEYS = {
    "L",
    "builder_sha256",
    "cache_manifest_sha256",
    "cached_control_l4_l8_gate_audit_sha256",
    "cached_control_l4_l8_gate_sha256",
    "cached_l10_gate_audit_sha256",
    "cached_l10_gate_sha256",
    "claim_boundary",
    "coarse_method",
    "comparison",
    "consumer_sha256",
    "dimension",
    "dual_obstruction_gate_sha256",
    "edges",
    "events",
    "execution_authorization_sha256",
    "fine_method",
    "freeze_sha256",
    "independent_hostile_audit_sha256",
    "l10_execution_authorization_gate_sha256",
    "lineage_authority",
    "method_sha256",
    "original_target_l12_gate_sha256",
    "physical_execution_gate_sha256",
    "preflight_result_sha256",
    "preserved_workspace_cross_diagnostic_sha256",
    "preserved_workspace_custody_sha256",
    "preterminal_dimension",
    "production_obligation_validators_sha256",
    "promotion_audit_sha256",
    "representation",
    "resource",
    "rows",
    "runtime_compatibility_obstruction_sha256",
    "schema",
    "shared_aggregate_schedule_gate_audit_sha256",
    "shared_aggregate_schedule_gate_sha256",
    "target_hostile_l10_cross_gate_sha256",
    "target_l12_execution_gate_sha256",
    "target_v004_sha256",
    "terminal_shards",
    "v006_hostile_audit_obstruction_sha256",
    "v007_runtime_compatibility_obstruction_sha256",
    "v008_postbuild_audit_binding_obstruction_sha256",
    "v009_hostile_audit_obstruction_sha256",
    "v010_audit_record_custody_correction_sha256",
    "v010_hostile_audit_obstruction_sha256",
    "v011_hostile_audit_obstruction_sha256",
}


class VerificationError(RuntimeError):
    """A fail-closed packet or input authentication failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise VerificationError(f"non-finite JSON constant: {value}")


def _finite_float(value: str) -> float:
    answer = float(value)
    if not math.isfinite(answer):
        raise VerificationError(f"non-finite JSON number: {value}")
    return answer


def strict_json_loads(payload: str | bytes) -> Any:
    """Parse JSON while rejecting duplicate keys and every non-finite number."""
    try:
        return json.loads(
            payload,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"invalid JSON: {error}") from error


def strict_json_load(path: Path) -> Any:
    return strict_json_loads(path.read_bytes())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_relative(relative: str) -> PurePosixPath:
    require(isinstance(relative, str) and relative != "", "source path must be nonempty text")
    require("\\" not in relative, f"backslash prohibited in source path: {relative}")
    parsed = PurePosixPath(relative)
    require(not parsed.is_absolute(), f"absolute source path prohibited: {relative}")
    require(all(part not in {"", ".", ".."} for part in parsed.parts),
            f"non-canonical source path: {relative}")
    require(str(parsed) == relative, f"source path spelling is not canonical: {relative}")
    return parsed


def safe_repository_file(relative: str) -> Path:
    parsed = _safe_relative(relative)
    candidate = ROOT.joinpath(*parsed.parts)
    current = ROOT
    for part in parsed.parts:
        current = current / part
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError as error:
            raise VerificationError(f"missing source: {relative}") from error
        require(not stat.S_ISLNK(mode), f"symlink prohibited in source path: {relative}")
    require(stat.S_ISREG(os.lstat(candidate).st_mode), f"source is not a regular file: {relative}")
    require(candidate.resolve().is_relative_to(ROOT.resolve()), f"source escaped root: {relative}")
    return candidate


T = TypeVar("T")


def read_authenticated(
    path: Path,
    expected_sha256: str,
    expected_bytes: int | None,
    reader: Callable[[Path], T],
) -> T:
    """Authenticate, consume, then reauthenticate the same regular file."""
    before = os.lstat(path)
    require(stat.S_ISREG(before.st_mode) and not stat.S_ISLNK(before.st_mode),
            f"authenticated input is not a plain regular file: {path}")
    if expected_bytes is not None:
        require(before.st_size == expected_bytes, f"byte count mismatch: {path}")
    require(sha256_file(path) == expected_sha256, f"pre-read hash mismatch: {path}")
    result = reader(path)
    after = os.lstat(path)
    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    require(identity_before == identity_after, f"input identity changed while reading: {path}")
    require(sha256_file(path) == expected_sha256, f"post-read hash mismatch: {path}")
    return result


def _read_npy_header(path: Path) -> tuple[tuple[int, ...], bool, str]:
    try:
        import numpy as np
    except ImportError as error:  # pragma: no cover - production environment has numpy.
        raise VerificationError("numpy is required only to authenticate NPY headers") from error
    with path.open("rb") as stream:
        version = np.lib.format.read_magic(stream)
        require(version in {(1, 0), (2, 0), (3, 0)}, f"unsupported NPY version: {version}")
        if version == (1, 0):
            shape, fortran_order, dtype = np.lib.format.read_array_header_1_0(stream)
        else:
            shape, fortran_order, dtype = np.lib.format.read_array_header_2_0(stream)
    return tuple(int(value) for value in shape), bool(fortran_order), dtype.str


def relocate_historical_path(historical: str, expected_suffix: str) -> Path:
    """Apply the one allowed exact-prefix relocation without rewriting provenance."""
    require(isinstance(historical, str), "historical path must be text")
    require(historical.startswith(HISTORICAL_ROOT_PREFIX), "historical root prefix mismatch")
    suffix = historical[len(HISTORICAL_ROOT_PREFIX):]
    require(suffix == expected_suffix, "historical suffix does not match the allowlisted shard")
    return safe_repository_file(expected_suffix)


def _verify_inventory() -> None:
    relative = "MIGRATION_CONTEXT_AUDIT_2026-09-27_V001/INVENTORY.json"
    expected_bytes, expected_hash = SOURCE_RECORDS[relative]
    path = safe_repository_file(relative)
    inventory = read_authenticated(path, expected_hash, expected_bytes, strict_json_load)
    require(inventory.get("schema") == "UNT_MIGRATION_CONTEXT_AUDIT_V001",
            "migration inventory schema")
    records = inventory.get("source_files")
    require(isinstance(records, list), "migration source inventory must be a list")
    by_path: dict[str, dict[str, Any]] = {}
    for record in records:
        require(isinstance(record, dict) and set(record) == {"path", "sha256", "custody"},
                "migration source record shape")
        source_path = record["path"]
        require(source_path not in by_path, f"duplicate migration source record: {source_path}")
        by_path[source_path] = record
    for name, expected_hash in FROZEN_HASHES.items():
        relative_frozen = f"{PACKET.name}/{name}"
        require(relative_frozen in by_path, f"frozen file absent from migration inventory: {name}")
        require(by_path[relative_frozen]["sha256"] == expected_hash,
                f"migration inventory frozen hash mismatch: {name}")
        require(by_path[relative_frozen]["custody"] == "migrated_untracked_authenticated",
                f"migration custody class mismatch: {name}")
    # The migration inventory explicitly enumerates the histories and v004
    # engine.  The dense parent is instead bound directly by the byte-frozen
    # FREEZE.json and is tracked in Git; do not pretend the inventory listed it.
    inventory_bound = {
        "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py",
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L4.json",
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L8.json",
    }
    for source_path in inventory_bound:
        _, expected_hash = SOURCE_RECORDS[source_path]
        if source_path == relative:
            continue
        require(source_path in by_path, f"source absent from migration inventory: {source_path}")
        require(by_path[source_path]["sha256"] == expected_hash,
                f"migration inventory hash mismatch: {source_path}")


def verify_freeze_and_manifest() -> dict[str, Any]:
    """Verify frozen bytes, strict schemas, receipt, manifest, and source hashes."""
    require(set(FROZEN_HASHES) == {"README.md", "PROTOCOL.md", "FREEZE.json"},
            "internal frozen census")
    for name, expected_hash in FROZEN_HASHES.items():
        path = safe_repository_file(f"{PACKET.name}/{name}")
        require(sha256_file(path) == expected_hash, f"frozen byte mismatch: {name}")

    freeze = strict_json_load(PACKET / "FREEZE.json")
    expected_freeze_keys = {
        "schema", "status", "L", "support", "conductance", "ollivier_ricci",
        "predictor", "response", "statistic", "null", "effect_floor_abs_rho",
        "tail_probability_ceiling", "comparison_guard", "inputs", "runtime",
        "outputs", "execution_authorized", "claim_boundary",
    }
    require(isinstance(freeze, dict) and set(freeze) == expected_freeze_keys,
            "freeze top-level key census")
    require(freeze["schema"] == "L8_OPERATOR_INCIDENCE_CURVATURE_RESPONSE_FREEZE_V001",
            "freeze schema")
    require(freeze["L"] == 8 and type(freeze["L"]) is int, "freeze L")
    require(freeze["execution_authorized"] is False, "L8 execution must remain unauthorized")
    require(freeze["claim_boundary"] == CLAIM_BOUNDARY, "freeze claim boundary")
    require(freeze["inputs"]["history"] == {
        "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L8.json",
        "sha256": SOURCE_RECORDS[
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L8.json"
        ][1],
    }, "frozen L8 history input")
    require(freeze["inputs"]["engine"] == {
        "path": "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py",
        "sha256": SOURCE_RECORDS[
            "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py"
        ][1],
    }, "frozen engine input")
    require(freeze["inputs"]["l4_parent"] == {
        "path": "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py",
        "sha256": SOURCE_RECORDS[
            "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_seed_history.py"
        ][1],
    }, "frozen dense-parent input")

    require(sha256_file(RECEIPT) == RECEIPT_HASH, "migration receipt byte hash")
    receipt = strict_json_load(RECEIPT)
    require(isinstance(receipt, dict) and set(receipt) == {
        "schema", "date", "status", "custody", "historical_root_prefix",
        "runtime_root", "relocation_policy", "frozen_packet", "authenticated_sources",
        "retained_terminal_shards", "response_adapter", "execution_authorized",
        "scientific_status", "claim_boundary",
    }, "migration receipt top-level key census")
    require(receipt["schema"] == "L8_OPERATOR_INCIDENCE_CURVATURE_MIGRATION_RECEIPT_V001",
            "migration receipt schema")
    require(receipt["date"] == "2026-09-27", "migration receipt date")
    require(receipt["status"] == (
        "MIGRATED_PREPRODUCTION_INPUTS_AUTHENTICATED__L8_PRODUCTION_NOT_AUTHORIZED"
    ), "migration receipt status")
    require(receipt["custody"] == "MIGRATED_UNTRACKED_AUTHENTICATED",
            "migration receipt custody")
    require(receipt["historical_root_prefix"] == HISTORICAL_ROOT_PREFIX,
            "migration historical root")
    require(receipt["runtime_root"] == str(ROOT), "migration runtime root")
    require(receipt["relocation_policy"] == (
        "EXACT_PREFIX_TO_REPOSITORY_RELATIVE_SUFFIX__NO_PROVENANCE_REWRITE"
    ), "migration relocation policy")
    require(receipt["execution_authorized"] is False, "migration execution authorization")
    require(receipt["scientific_status"] == UNRESOLVED, "migration scientific status")
    require(receipt["claim_boundary"] == CLAIM_BOUNDARY, "migration claim boundary")
    require(receipt["response_adapter"] == {
        "required_schema": "L8_ALL_EVENT_AUTONOMOUS_LINEAGE_RESPONSE_V001",
        "present": False,
        "fabricated": False,
    }, "missing response-adapter receipt")

    manifest = strict_json_load(MANIFEST)
    require(isinstance(manifest, dict) and set(manifest) == {
        "schema", "status", "migration_receipt", "frozen_files", "repository_sources",
        "history_contract", "terminal_shards", "production_inputs",
        "execution_authorized", "scientific_status", "claim_boundary",
    }, "source manifest top-level key census")
    require(manifest["schema"] == "L8_OPERATOR_INCIDENCE_CURVATURE_SOURCE_MANIFEST_V001",
            "source manifest schema")
    require(manifest["status"] == (
        "PREPRODUCTION_SOURCES_FROZEN__NO_L8_RESPONSE_ADAPTER__NO_L8_EXECUTION"
    ), "source manifest status")
    require(manifest["migration_receipt"] == {
        "path": f"{PACKET.name}/MIGRATION_RECEIPT.json",
        "bytes": RECEIPT.stat().st_size,
        "sha256": RECEIPT_HASH,
    }, "source manifest receipt binding")
    frozen_records = manifest["frozen_files"]
    require(isinstance(frozen_records, list) and len(frozen_records) == 3,
            "source manifest frozen census")
    require(all(isinstance(record, dict) and set(record) == {"name", "sha256"}
                for record in frozen_records), "source manifest frozen record keys")
    require({record["name"]: record["sha256"] for record in frozen_records} == FROZEN_HASHES,
            "source manifest frozen hashes")
    repository_sources = manifest["repository_sources"]
    require(isinstance(repository_sources, list) and len(repository_sources) == len(SOURCE_RECORDS),
            "source manifest repository-source census")
    seen: set[str] = set()
    for record in repository_sources:
        require(isinstance(record, dict) and set(record) == {"path", "bytes", "sha256", "custody"},
                "source manifest repository-source record")
        relative = record["path"]
        require(relative not in seen, f"duplicate source manifest path: {relative}")
        seen.add(relative)
        require(relative in SOURCE_RECORDS, f"unexpected source manifest path: {relative}")
        expected_bytes, expected_hash = SOURCE_RECORDS[relative]
        require(record["bytes"] == expected_bytes and record["sha256"] == expected_hash,
                f"source manifest identity mismatch: {relative}")
        candidate = safe_repository_file(relative)
        read_authenticated(candidate, expected_hash, expected_bytes, lambda _: None)
    require(seen == set(SOURCE_RECORDS), "source manifest source paths")
    contract = manifest["history_contract"]
    require(contract == {
        "schema": "TARGET_CACHED_PREFIX_HISTORY_V012",
        "representation": (
            "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__"
            "AUTHENTICATED_INDEX_CACHE"
        ),
        "historical_root_prefix": HISTORICAL_ROOT_PREFIX,
        "allowed_suffix_template": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L{L}/sharp/"
            "prefix_{L_minus_1_two_digits}/q_{q_two_digits}.npy"
        ),
        "npy_dtype": "<c16",
        "npy_fortran_order": False,
    }, "source manifest history contract")
    require(manifest["production_inputs"] == {
        "conductance_adapter": "ABSENT_NOT_PRODUCED",
        "response_adapter": "ABSENT_NOT_FABRICATED",
        "result": "ABSENT_NOT_PRODUCED",
    }, "preproduction output absence declaration")
    require(manifest["execution_authorized"] is False, "manifest execution authorization")
    require(manifest["scientific_status"] == UNRESOLVED, "manifest scientific status")
    require(manifest["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary")

    _verify_inventory()
    return freeze


def verify_history_relocation(length: int) -> dict[str, Any]:
    """Authenticate one retained preterminal history and every relocated shard."""
    require(length in {4, 8}, "only authenticated L4/L8 histories may be checked")
    manifest = strict_json_load(MANIFEST)
    manifest_shards = manifest["terminal_shards"][f"L{length}"]
    relative_history = (
        f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L{length}.json"
    )
    expected_bytes, expected_hash = SOURCE_RECORDS[relative_history]
    history_path = safe_repository_file(relative_history)
    history = read_authenticated(history_path, expected_hash, expected_bytes, strict_json_load)
    require(isinstance(history, dict) and set(history) == HISTORY_TOP_KEYS,
            f"L{length} history top-level key census")
    require(history["schema"] == "TARGET_CACHED_PREFIX_HISTORY_V012", "history schema")
    require(history["representation"] == (
        "Q_SHARDED_MEMMAP__FULL_CANONICAL_LINEAGE_AND_CARRIER_MASKS__"
        "AUTHENTICATED_INDEX_CACHE"
    ), "history representation")
    require(history["L"] == length and type(history["L"]) is int, "history length")
    require(history["events"] == length, "history event count")
    require(history["edges"] == 3 * length, "history prism-edge count")
    require(history["dimension"] == math.comb(3 * length, length), "history dimension")
    require(history["preterminal_dimension"] == math.comb(3 * length - 1, length - 1),
            "history preterminal dimension")
    require(history["target_v004_sha256"] == SOURCE_RECORDS[
        "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py"
    ][1], "history engine binding")
    records = history["terminal_shards"]
    require(isinstance(records, list) and len(records) == length,
            f"L{length} terminal shard census")
    require(isinstance(manifest_shards, list) and len(manifest_shards) == length,
            f"L{length} manifest shard census")
    by_q: dict[int, dict[str, Any]] = {}
    for record in records:
        require(isinstance(record, dict) and set(record) == {
            "q", "path", "shape", "bytes", "sha256",
        }, "history shard record keys")
        q = record["q"]
        require(type(q) is int and q not in by_q, f"duplicate or invalid q shard: {q}")
        by_q[q] = record
    require(set(by_q) == set(range(length)), f"L{length} q-shard labels")

    expected_names = {f"q_{q:02d}.npy" for q in range(length)}
    shard_directory: Path | None = None
    verified: list[dict[str, Any]] = []
    for q in range(length):
        record = by_q[q]
        manifest_record = manifest_shards[q]
        require(manifest_record == {
            "q": q,
            "bytes": record["bytes"],
            "shape": record["shape"],
            "sha256": record["sha256"],
        }, f"L{length} q={q} history/manifest disagreement")
        expected_shape = [math.comb(length - 1, q), math.comb(2 * length, q)]
        require(record["shape"] == expected_shape, f"L{length} q={q} shape contract")
        expected_suffix = (
            f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L{length}/sharp/"
            f"prefix_{length - 1:02d}/q_{q:02d}.npy"
        )
        candidate = relocate_historical_path(record["path"], expected_suffix)
        if shard_directory is None:
            shard_directory = candidate.parent
        require(candidate.parent == shard_directory, "terminal shards span unexpected directories")
        shape, fortran_order, dtype = read_authenticated(
            candidate,
            record["sha256"],
            record["bytes"],
            _read_npy_header,
        )
        require(list(shape) == expected_shape, f"L{length} q={q} NPY shape")
        require(dtype == "<c16", f"L{length} q={q} NPY dtype")
        require(fortran_order is False, f"L{length} q={q} NPY order")
        verified.append({
            "q": q,
            "historical_path": record["path"],
            "runtime_path": str(candidate),
            "bytes": record["bytes"],
            "sha256": record["sha256"],
            "shape": expected_shape,
            "dtype": dtype,
            "fortran_order": fortran_order,
        })
    require(shard_directory is not None, "missing shard directory")
    actual_names = {entry.name for entry in shard_directory.iterdir()}
    require(actual_names == expected_names,
            f"unexpected or missing members in L{length} terminal shard directory")
    require(sha256_file(history_path) == expected_hash, "history changed after shard verification")
    return {
        "L": length,
        "history": relative_history,
        "history_sha256": expected_hash,
        "shards": verified,
        "total_bytes": sum(record["bytes"] for record in records),
        "operation": "AUTHENTICATION_ONLY__NO_CONDUCTANCE_EXTRACTION",
    }


def verify_all_preproduction_inputs() -> dict[str, Any]:
    freeze = verify_freeze_and_manifest()
    l4 = verify_history_relocation(4)
    l8 = verify_history_relocation(8)
    return {
        "schema": "L8_OPERATOR_INCIDENCE_CURVATURE_PREPRODUCTION_VERIFICATION_V001",
        "status": "PASS_PREPRODUCTION_INPUT_AUTHENTICATION__L8_PRODUCTION_NOT_RUN",
        "frozen_packet_sha256": FROZEN_HASHES,
        "freeze_schema": freeze["schema"],
        "relocation_checks": [l4, l8],
        "l8_numerical_extraction_run": False,
        "response_adapter_present": False,
        "execution_authorized": False,
        "scientific_status": UNRESOLVED,
        "claim_boundary": CLAIM_BOUNDARY,
    }


if __name__ == "__main__":
    try:
        print(json.dumps(verify_all_preproduction_inputs(), indent=2, sort_keys=True))
    except (OSError, KeyError, TypeError, VerificationError) as error:
        print(f"FAIL preproduction verification: {error}", file=os.sys.stderr)
        raise SystemExit(1)
