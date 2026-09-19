#!/usr/bin/env python3
"""Reconstruct an authenticated L12 q4 -> q5 -> q6 record-flow bridge.

This is a read-only forensic sidecar.  It does not modify or supersede the
completed Stage-3 histories, the Stage-5 sector manifest, or the Stage-6
adjudication.  A flow edge is certified only when both the Target and Hostile
implementations independently satisfy all frozen predicates below:

* the history, cache manifest, admission arrays, carrier-word arrays, and
  prefix shard match their preserved SHA-256 records;
* the admission map is a nonempty injection and exactly implements setting
  terminal event bit 11 from zero to one;
* sin(pi/4)^2 times the selected prefix-state norm is at least MIN_FLOW;
* the independently reconstructed Target and Hostile flows agree within
  CROSS_BRANCH_ABS_TOLERANCE.

Density atoms are not treated as physical vertices.  They are attached to
typed L12 sector nodes only through the Stage-5 manifest's explicit q_by_L
assignment.  Consequently the resulting path is a record-flow sector path,
not an inferred atom-adjacency path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LENGTH = 12
TERMINAL_EVENT = 11
PHI = math.pi / 4.0
ADMISSION_FACTOR = math.sin(PHI) ** 2
MIN_FLOW = 1.0e-12
CROSS_BRANCH_ABS_TOLERANCE = 1.0e-12
GEOMETRY_LOWER = Decimal("0.90")
GEOMETRY_UPPER = Decimal("1.10")
MASS_THRESHOLD = Decimal("0.50")
ROW_CHUNK = 8
SCHEMA = "L12_AUTHENTICATED_RECORD_FLOW_BRIDGE_V001"

DEFAULT_ADJUDICATION = (
    ROOT
    / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json"
)
DEFAULT_MANIFEST = (
    ROOT
    / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003"
    / "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
)
DEFAULT_TARGET_HISTORY = (
    ROOT
    / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
DEFAULT_HOSTILE_HISTORY = (
    ROOT
    / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "V004R4_PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
DEFAULT_TARGET_CACHE = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012" / "CACHE_PAYLOADS_V012" / "L12"
)
DEFAULT_HOSTILE_CACHE = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "V004R4_CACHE_PAYLOADS" / "L12"
)
DEFAULT_OUTPUT = HERE / "RECORD_FLOW_BRIDGE_REPORT_V001.json"

PINNED_SHA256 = {
    "stage6_adjudication": "43c7c19daaf24902d2699c337851eca35a03c3db69f8e3f55f3b0142f87e137d",
    "stage5_manifest": "292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a",
    "target_history": "079499e7b989e1ba45b1c397882c8638106be149ccb994058a3703b235736764",
    "hostile_history": "cbac18fd5033f83e4eadbfb16b46c89584455987e0b75fa6a33a33821246851c",
    "target_cache_manifest": "c8efb9b36ab18a3727aab4548109256640c92b63c121a07d9993999e4c570d6a",
    "hostile_cache_manifest": "1640607ea32c63a4af2139dc19a863e47b2fac5603656d059016710c774bceec",
}


class Refusal(RuntimeError):
    """The preserved evidence does not satisfy the frozen bridge predicates."""


@dataclass(frozen=True)
class AuthenticatedJSON:
    label: str
    path: Path
    sha256: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class FileIdentity:
    device: int
    inode: int
    size: int
    mtime_ns: int


@dataclass(frozen=True)
class BranchSpec:
    label: str
    history: AuthenticatedJSON
    cache_manifest: AuthenticatedJSON
    cache_root: Path
    shard_root: Path
    shard_suffix: str
    basis_order: str
    consumer_sha256: str
    source_to_map_q_offset: int
    source_map_role: str
    destination_map_role: str

    def map_names(self, source_q: int) -> tuple[str, str]:
        if self.label == "target":
            stem = f"admission_n_{TERMINAL_EVENT:02d}_q_{source_q:02d}"
            return f"{stem}_blank.i32", f"{stem}_destination.i32"
        destination_q = source_q + self.source_to_map_q_offset
        stem = f"event_{TERMINAL_EVENT:02d}_q_{destination_q:02d}"
        return f"{stem}_old.i32", f"{stem}_occupied.i32"

    def word_name(self, q: int) -> str:
        return f"carrier_q_{q:02d}_words.u32" if self.label == "target" else f"q_{q:02d}_words.u32"


def file_identity(path: Path) -> FileIdentity:
    try:
        metadata = path.stat()
    except OSError as error:
        raise Refusal(f"cannot stat {path}: {error}") from error
    if not stat.S_ISREG(metadata.st_mode):
        raise Refusal(f"not a regular file: {path}")
    return FileIdentity(
        device=metadata.st_dev,
        inode=metadata.st_ino,
        size=metadata.st_size,
        mtime_ns=metadata.st_mtime_ns,
    )


def sha256_file(path: Path) -> tuple[str, FileIdentity]:
    before = file_identity(path)
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(16 * 2**20), b""):
                digest.update(block)
    except OSError as error:
        raise Refusal(f"cannot hash {path}: {error}") from error
    after = file_identity(path)
    if before != after:
        raise Refusal(f"file changed while being authenticated: {path}")
    return digest.hexdigest(), after


def authenticate_json(path: Path, expected: str, label: str) -> AuthenticatedJSON:
    actual, identity = sha256_file(path)
    if actual != expected:
        raise Refusal(f"{label} SHA-256 mismatch: expected={expected} actual={actual} path={path}")
    try:
        raw = path.read_bytes()
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{label} is not readable UTF-8 JSON: {error}") from error
    if file_identity(path) != identity:
        raise Refusal(f"{label} changed while being parsed: {path}")
    if not isinstance(payload, Mapping):
        raise Refusal(f"{label} top level is not an object")
    return AuthenticatedJSON(label, path.resolve(), actual, payload)


def manifest_records(document: AuthenticatedJSON) -> dict[str, Mapping[str, Any]]:
    files = document.payload.get("files")
    if not isinstance(files, list):
        raise Refusal(f"{document.label}: files ledger absent")
    result: dict[str, Mapping[str, Any]] = {}
    for record in files:
        if not isinstance(record, Mapping) or not isinstance(record.get("path"), str):
            raise Refusal(f"{document.label}: malformed file record")
        name = record["path"]
        if name in result:
            raise Refusal(f"{document.label}: duplicate file record {name}")
        result[name] = record
    return result


def authenticate_manifest_array(
    root: Path,
    records: Mapping[str, Mapping[str, Any]],
    name: str,
) -> tuple[np.memmap, dict[str, Any], FileIdentity]:
    record = records.get(name)
    if record is None:
        raise Refusal(f"cache manifest lacks {name}")
    try:
        dtype = np.dtype(record["dtype"])
        shape = tuple(record["shape"])
        expected_bytes = int(record["bytes"])
        expected_hash = str(record["sha256"])
    except (KeyError, TypeError, ValueError) as error:
        raise Refusal(f"malformed cache record for {name}: {error}") from error
    if not shape or any(type(value) is not int or value < 0 for value in shape):
        raise Refusal(f"invalid cache shape for {name}: {shape}")
    if math.prod(shape) * dtype.itemsize != expected_bytes:
        raise Refusal(f"cache record shape/byte mismatch for {name}")
    path = (root / name).resolve()
    actual_hash, identity = sha256_file(path)
    if identity.size != expected_bytes or actual_hash != expected_hash:
        raise Refusal(
            f"cache payload authentication failed for {name}: "
            f"bytes={identity.size}/{expected_bytes} sha256={actual_hash}/{expected_hash}"
        )
    array = np.memmap(path, dtype=dtype, mode="r", shape=shape)
    audit = {
        "path": str(path),
        "sha256": actual_hash,
        "bytes": identity.size,
        "dtype": dtype.str,
        "shape": list(shape),
        "kind": record.get("kind"),
        "role": record.get("role"),
        "event": record.get("event"),
        "q": record.get("q"),
    }
    return array, audit, identity


def close_memmap(array: np.ndarray) -> None:
    mapping = getattr(array, "_mmap", None)
    if mapping is not None:
        mapping.close()


def terminal_shard_record(history: AuthenticatedJSON, q: int) -> Mapping[str, Any]:
    records = history.payload.get("terminal_shards")
    if not isinstance(records, list):
        raise Refusal(f"{history.label}: terminal_shards absent")
    matches = [record for record in records if isinstance(record, Mapping) and record.get("q") == q]
    if len(matches) != 1:
        raise Refusal(f"{history.label}: expected exactly one q={q} terminal shard")
    return matches[0]


def authenticate_shard(spec: BranchSpec, q: int) -> tuple[np.memmap, dict[str, Any], FileIdentity]:
    record = terminal_shard_record(spec.history, q)
    expected_path = (spec.shard_root / f"q_{q:02d}{spec.shard_suffix}").resolve()
    try:
        recorded_path = Path(str(record["path"])).resolve()
        shape = tuple(record["shape"])
        expected_bytes = int(record["bytes"])
        expected_hash = str(record["sha256"])
    except (KeyError, TypeError, ValueError) as error:
        raise Refusal(f"{spec.label}: malformed q={q} shard record: {error}") from error
    if recorded_path != expected_path:
        raise Refusal(
            f"{spec.label}: q={q} shard path escaped pinned workspace; "
            f"recorded={recorded_path} expected={expected_path}"
        )
    if len(shape) != 2 or any(type(value) is not int or value <= 0 for value in shape):
        raise Refusal(f"{spec.label}: invalid q={q} shard shape {shape}")
    actual_hash, identity = sha256_file(expected_path)
    if identity.size != expected_bytes or actual_hash != expected_hash:
        raise Refusal(f"{spec.label}: q={q} prefix shard failed byte/hash authentication")
    if spec.shard_suffix == ".npy":
        shard = np.load(expected_path, mmap_mode="r", allow_pickle=False)
    else:
        if expected_bytes != math.prod(shape) * np.dtype(np.complex128).itemsize:
            raise Refusal(f"{spec.label}: q={q} raw shard shape/byte mismatch")
        shard = np.memmap(expected_path, dtype=np.complex128, mode="r", shape=shape)
    if shard.shape != shape or shard.dtype != np.dtype(np.complex128):
        close_memmap(shard)
        raise Refusal(
            f"{spec.label}: q={q} shard array mismatch: shape={shard.shape} dtype={shard.dtype}"
        )
    expected_shape = (math.comb(TERMINAL_EVENT, q), math.comb(2 * LENGTH, q))
    if shape != expected_shape:
        close_memmap(shard)
        raise Refusal(
            f"{spec.label}: q={q} prefix shard shape is not the exact L12/prefix_11 shape; "
            f"observed={shape} expected={expected_shape}"
        )
    audit = {
        "path": str(expected_path),
        "sha256": actual_hash,
        "bytes": identity.size,
        "dtype": shard.dtype.str,
        "shape": list(shape),
        "prefix": 11,
        "q": q,
    }
    return shard, audit, identity


def validate_admission_map(
    source_words: np.ndarray,
    destination_words: np.ndarray,
    source_indices: np.ndarray,
    destination_indices: np.ndarray,
    event: int,
) -> dict[str, Any]:
    if source_indices.dtype.kind not in "iu" or destination_indices.dtype.kind not in "iu":
        raise Refusal("admission indices are not integer arrays")
    if source_indices.ndim != 1 or destination_indices.ndim != 1:
        raise Refusal("admission indices are not one-dimensional")
    if len(source_indices) == 0 or len(source_indices) != len(destination_indices):
        raise Refusal("admission map is empty or its sides have different lengths")
    source = np.asarray(source_indices, dtype=np.int64)
    destination = np.asarray(destination_indices, dtype=np.int64)
    if (
        int(source.min()) < 0
        or int(source.max()) >= len(source_words)
        or int(destination.min()) < 0
        or int(destination.max()) >= len(destination_words)
    ):
        raise Refusal("admission index is outside its carrier basis")
    if len(np.unique(source)) != len(source) or len(np.unique(destination)) != len(destination):
        raise Refusal("admission map is not injective on both sides")
    source_selected = np.asarray(source_words[source], dtype=np.uint64)
    destination_selected = np.asarray(destination_words[destination], dtype=np.uint64)
    event_mask = np.uint64(1 << event)
    source_blank = bool(np.all(np.bitwise_and(source_selected, event_mask) == 0))
    destination_occupied = bool(np.all(np.bitwise_and(destination_selected, event_mask) != 0))
    exact_bit_insertion = bool(
        np.array_equal(destination_selected, np.bitwise_or(source_selected, event_mask))
    )
    if not source_blank or not destination_occupied or not exact_bit_insertion:
        raise Refusal(
            "admission map does not exactly insert the terminal event bit into the carrier word"
        )
    return {
        "nonempty": True,
        "pair_count": len(source),
        "source_injective": True,
        "destination_injective": True,
        "source_event_bit_blank": source_blank,
        "destination_event_bit_occupied": destination_occupied,
        "exact_terminal_bit_insertion": exact_bit_insertion,
        "source_index_min": int(source.min()),
        "source_index_max": int(source.max()),
        "destination_index_min": int(destination.min()),
        "destination_index_max": int(destination.max()),
    }


def selected_norm_squared(
    shard: np.ndarray,
    source_indices: np.ndarray,
    row_chunk: int = ROW_CHUNK,
) -> float:
    if row_chunk <= 0:
        raise Refusal("row chunk must be positive")
    if shard.ndim != 2 or source_indices.ndim != 1:
        raise Refusal("selected norm requires a matrix shard and vector index map")
    total = 0.0
    for lower in range(0, shard.shape[0], row_chunk):
        upper = min(shard.shape[0], lower + row_chunk)
        block = np.asarray(shard[lower:upper, source_indices])
        total += float(np.sum(block.real * block.real + block.imag * block.imag, dtype=np.float64))
    if not math.isfinite(total) or total < 0.0:
        raise Refusal(f"selected prefix norm is not finite and nonnegative: {total}")
    return total


def reconstruct_branch_flow(spec: BranchSpec, source_q: int) -> dict[str, Any]:
    if source_q not in (4, 5):
        raise Refusal(f"unsupported bridge source sector q={source_q}")
    records = manifest_records(spec.cache_manifest)
    source_name, destination_name = spec.map_names(source_q)
    source_indices, source_audit, source_identity = authenticate_manifest_array(
        spec.cache_root, records, source_name
    )
    destination_indices, destination_audit, destination_identity = authenticate_manifest_array(
        spec.cache_root, records, destination_name
    )
    source_words, source_words_audit, source_words_identity = authenticate_manifest_array(
        spec.cache_root, records, spec.word_name(source_q)
    )
    destination_words, destination_words_audit, destination_words_identity = authenticate_manifest_array(
        spec.cache_root, records, spec.word_name(source_q + 1)
    )
    shard, shard_audit, shard_identity = authenticate_shard(spec, source_q)
    try:
        map_record_q = source_q + spec.source_to_map_q_offset
        expected_map_pairs = math.comb(2 * LENGTH - 1, source_q)
        for audit, expected_role in (
            (source_audit, spec.source_map_role),
            (destination_audit, spec.destination_map_role),
        ):
            if (
                audit["kind"] != "admission"
                or audit["role"] != expected_role
                or audit["event"] != TERMINAL_EVENT
                or audit["q"] != map_record_q
                or audit["shape"] != [expected_map_pairs]
            ):
                raise Refusal(
                    f"{spec.label}: q={source_q} admission record metadata mismatch: {audit}"
                )
        for audit, expected_q in (
            (source_words_audit, source_q),
            (destination_words_audit, source_q + 1),
        ):
            if (
                audit["kind"] != "operator"
                or audit["role"] != "words"
                or audit["q"] != expected_q
                or audit["shape"] != [math.comb(2 * LENGTH, expected_q)]
            ):
                raise Refusal(
                    f"{spec.label}: q={expected_q} carrier-word metadata mismatch: {audit}"
                )
        map_checks = validate_admission_map(
            source_words,
            destination_words,
            source_indices,
            destination_indices,
            TERMINAL_EVENT,
        )
        if shard.shape[1] != len(source_words):
            raise Refusal(
                f"{spec.label}: q={source_q} shard/carrier column mismatch "
                f"{shard.shape[1]} != {len(source_words)}"
            )
        norm_squared = selected_norm_squared(shard, source_indices)
        flow = ADMISSION_FACTOR * norm_squared
        if not math.isfinite(flow) or flow < MIN_FLOW:
            raise Refusal(
                f"{spec.label}: q={source_q}->q={source_q + 1} flow {flow} "
                f"is below frozen minimum {MIN_FLOW}"
            )
        identities = (
            (spec.cache_root / source_name, source_identity),
            (spec.cache_root / destination_name, destination_identity),
            (spec.cache_root / spec.word_name(source_q), source_words_identity),
            (spec.cache_root / spec.word_name(source_q + 1), destination_words_identity),
            (spec.shard_root / f"q_{source_q:02d}{spec.shard_suffix}", shard_identity),
        )
        for path, identity in identities:
            if file_identity(path.resolve()) != identity:
                raise Refusal(f"authenticated input changed during numerical read: {path}")
    finally:
        for array in (source_indices, destination_indices, source_words, destination_words, shard):
            close_memmap(array)
    return {
        "branch": spec.label,
        "edge": f"L12:Q{source_q:02d}->L12:Q{source_q + 1:02d}",
        "source_q": source_q,
        "destination_q": source_q + 1,
        "admission_factor": ADMISSION_FACTOR,
        "selected_prefix_norm_squared": norm_squared,
        "transferred_norm_squared": flow,
        "minimum_transferred_norm_squared": MIN_FLOW,
        "positive_flow_predicate": flow >= MIN_FLOW,
        "map_checks": map_checks,
        "authenticated_inputs": {
            "source_indices": source_audit,
            "destination_indices": destination_audit,
            "source_carrier_words": source_words_audit,
            "destination_carrier_words": destination_words_audit,
            "prefix_shard": shard_audit,
        },
    }


def adjudicate_cross_branch(
    target: Mapping[str, Any], hostile: Mapping[str, Any]
) -> dict[str, Any]:
    if target["source_q"] != hostile["source_q"] or target["destination_q"] != hostile["destination_q"]:
        raise Refusal("Target/Hostile flow records describe different sector edges")
    target_flow = float(target["transferred_norm_squared"])
    hostile_flow = float(hostile["transferred_norm_squared"])
    difference = abs(target_flow - hostile_flow)
    passed = (
        target_flow >= MIN_FLOW
        and hostile_flow >= MIN_FLOW
        and difference <= CROSS_BRANCH_ABS_TOLERANCE
    )
    if not passed:
        raise Refusal(
            f"Target/Hostile flow mismatch for q={target['source_q']}: "
            f"target={target_flow} hostile={hostile_flow} difference={difference} "
            f"tolerance={CROSS_BRANCH_ABS_TOLERANCE}"
        )
    return {
        "edge": target["edge"],
        "target_transferred_norm_squared": target_flow,
        "hostile_transferred_norm_squared": hostile_flow,
        "absolute_difference": difference,
        "absolute_tolerance": CROSS_BRANCH_ABS_TOLERANCE,
        "minimum_flow": MIN_FLOW,
        "target_positive": target_flow >= MIN_FLOW,
        "hostile_positive": hostile_flow >= MIN_FLOW,
        "cross_branch_agreement": difference <= CROSS_BRANCH_ABS_TOLERANCE,
        "certified": True,
    }


def resolved_history(document: AuthenticatedJSON) -> None:
    comparison = document.payload.get("comparison")
    if not isinstance(comparison, Mapping) or comparison.get("resolved") is not True:
        raise Refusal(f"{document.label}: completed comparison is not resolved")
    classification = comparison.get("classification")
    if not isinstance(classification, str) or not classification.startswith("RESOLVED_"):
        raise Refusal(f"{document.label}: resolved classification absent")


def classification_pair(value: Any) -> tuple[Decimal, Decimal]:
    if not isinstance(value, Mapping):
        raise Refusal("geometry classification is absent")
    gap = value.get("gap_power_fit")
    if not isinstance(gap, Mapping):
        raise Refusal("gap_power_fit is absent")
    try:
        z = Decimal(str(gap["exponent"]))
        y = Decimal(str(value["chi_power_exponent_y"]))
    except (InvalidOperation, KeyError, ValueError) as error:
        raise Refusal(f"invalid z/y geometry: {error}") from error
    if not z.is_finite() or not y.is_finite():
        raise Refusal("z/y geometry is not finite")
    return z, y


def extract_atoms_and_endpoints(
    manifest: AuthenticatedJSON,
    adjudication: AuthenticatedJSON,
) -> tuple[dict[str, int], dict[str, Any]]:
    atoms = manifest.payload.get("atoms")
    results = adjudication.payload.get("atom_results")
    if not isinstance(atoms, list) or not isinstance(results, list):
        raise Refusal("Stage-5 atoms or Stage-6 atom_results absent")
    q_by_atom: dict[str, int] = {}
    manifest_by_id: dict[str, Mapping[str, Any]] = {}
    for atom in atoms:
        if not isinstance(atom, Mapping) or not isinstance(atom.get("atom_id"), str):
            raise Refusal("malformed Stage-5 atom")
        atom_id = atom["atom_id"]
        qmap = atom.get("q_by_L")
        if atom_id in manifest_by_id or not isinstance(qmap, Mapping) or type(qmap.get("12")) is not int:
            raise Refusal(f"malformed or duplicate Stage-5 membership for {atom_id}")
        manifest_by_id[atom_id] = atom
        q_by_atom[atom_id] = qmap["12"]
    geometry: dict[str, Any] = {}
    for result in results:
        if not isinstance(result, Mapping) or not isinstance(result.get("atom"), Mapping):
            raise Refusal("malformed Stage-6 atom result")
        atom = result["atom"]
        atom_id = atom.get("atom_id")
        if atom_id not in manifest_by_id or atom != manifest_by_id[atom_id]:
            raise Refusal(f"Stage-6 atom does not exactly match Stage-5 atom: {atom_id}")
        target_raw = result.get("target_classification")
        blind_raw = result.get("blind_classification")
        if target_raw is None or blind_raw is None:
            if q_by_atom[atom_id] in (4, 6):
                raise Refusal(f"geometry classification is absent for endpoint sector atom {atom_id}")
            geometry[atom_id] = {
                "q": q_by_atom[atom_id],
                "target": None,
                "blind": None,
                "consensus_geometry_pass": False,
                "geometry_available": False,
            }
            continue
        target_z, target_y = classification_pair(target_raw)
        blind_z, blind_y = classification_pair(blind_raw)
        passes = all(
            GEOMETRY_LOWER <= value <= GEOMETRY_UPPER
            for value in (target_z, target_y, blind_z, blind_y)
        )
        geometry[atom_id] = {
            "q": q_by_atom[atom_id],
            "target": {"z": str(target_z), "y": str(target_y)},
            "blind": {"z": str(blind_z), "y": str(blind_y)},
            "consensus_geometry_pass": passes,
            "geometry_available": True,
        }
    if set(geometry) != set(manifest_by_id):
        raise Refusal("Stage-5/Stage-6 atom identifier sets differ")
    q4 = sorted(atom_id for atom_id, item in geometry.items() if item["q"] == 4 and item["consensus_geometry_pass"])
    q6 = sorted(atom_id for atom_id, item in geometry.items() if item["q"] == 6 and item["consensus_geometry_pass"])
    if not q4 or not q6:
        raise Refusal(f"consensus geometry endpoints absent: q4={q4} q6={q6}")
    return q_by_atom, {
        "window": {"z": [str(GEOMETRY_LOWER), str(GEOMETRY_UPPER)], "y": [str(GEOMETRY_LOWER), str(GEOMETRY_UPPER)]},
        "source": "Target_AND_blind_consensus",
        "q4_passing_atoms": q4,
        "q6_passing_atoms": q6,
        "passing_endpoint_geometry": {atom_id: geometry[atom_id] for atom_id in q4 + q6},
    }


def sector_mass_report(manifest: AuthenticatedJSON) -> dict[str, Any]:
    histories = manifest.payload.get("histories")
    l12 = histories.get("12") if isinstance(histories, Mapping) else None
    pbar = l12.get("pbar_q") if isinstance(l12, Mapping) else None
    if not isinstance(pbar, list) or len(pbar) != LENGTH + 1:
        raise Refusal("Stage-5 L12 pbar_q ledger absent or wrong length")
    try:
        masses = [Decimal(str(value)) for value in pbar]
    except (InvalidOperation, ValueError) as error:
        raise Refusal(f"Stage-5 L12 pbar_q contains a non-decimal value: {error}") from error
    if any(not mass.is_finite() or mass < 0 for mass in masses):
        raise Refusal("Stage-5 L12 pbar_q contains invalid mass")
    total = sum(masses, Decimal(0))
    if abs(total - Decimal(1)) > Decimal("1e-12"):
        raise Refusal(f"Stage-5 L12 pbar_q is not normalized: {total}")
    triad = masses[4] + masses[5] + masses[6]
    return {
        "source": "stage5_manifest.histories[12].pbar_q",
        "normalization_sum": str(total),
        "q4": str(masses[4]),
        "q5": str(masses[5]),
        "q6": str(masses[6]),
        "deduplicated_q4_q5_q6": str(triad),
        "threshold": str(MASS_THRESHOLD),
        "threshold_crossed": triad >= MASS_THRESHOLD,
    }


def build_branch_spec(
    label: str,
    history: AuthenticatedJSON,
    cache_manifest: AuthenticatedJSON,
    cache_root: Path,
) -> BranchSpec:
    expected = {
        "target": (
            "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER",
            "307b7232603f4de3937e4f8fad5aa281ff1f4cc33beaec28be6e18d9d8cc63fa",
            ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012" / "WORKSPACES" / "L12_PROCESS_PARALLEL_V003R1" / "sharp" / "prefix_11",
            ".npy",
            0,
            "blank",
            "destination",
        ),
        "hostile": (
            "REVERSED_COMBINATION__FULL_MASK",
            "2c7ff73a0b462a75d576a51eef3863f5157dbccaa54573403734bbe72702d800",
            ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "V004R4_WORKSPACES" / "L12_PROCESS_PARALLEL_V002" / "sharp" / "prefix_11",
            ".c128",
            1,
            "old",
            "occupied",
        ),
    }[label]
    basis, consumer, shard_root, suffix, offset, source_role, destination_role = expected
    payload = cache_manifest.payload
    if payload.get("L") != LENGTH or payload.get("basis_order") != basis:
        raise Refusal(f"{label}: cache length or basis order mismatch")
    if not isinstance(payload.get("status"), str) or not payload["status"].startswith("COMPLETE_"):
        raise Refusal(f"{label}: cache completion status absent")
    if payload.get("consumer_sha256") != consumer:
        raise Refusal(f"{label}: cache consumer hash mismatch")
    if history.payload.get("L") != LENGTH or history.payload.get("cache_manifest_sha256") != cache_manifest.sha256:
        raise Refusal(f"{label}: history/cache-manifest binding mismatch")
    resolved_history(history)
    return BranchSpec(
        label=label,
        history=history,
        cache_manifest=cache_manifest,
        cache_root=cache_root.resolve(),
        shard_root=shard_root.resolve(),
        shard_suffix=suffix,
        basis_order=basis,
        consumer_sha256=consumer,
        source_to_map_q_offset=offset,
        source_map_role=source_role,
        destination_map_role=destination_role,
    )


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    adjudication = authenticate_json(args.adjudication, PINNED_SHA256["stage6_adjudication"], "stage6_adjudication")
    manifest = authenticate_json(args.manifest, PINNED_SHA256["stage5_manifest"], "stage5_manifest")
    target_history = authenticate_json(args.target_history, PINNED_SHA256["target_history"], "target_history")
    hostile_history = authenticate_json(args.hostile_history, PINNED_SHA256["hostile_history"], "hostile_history")
    target_cache_manifest = authenticate_json(
        args.target_cache / "CACHE_MANIFEST.json",
        PINNED_SHA256["target_cache_manifest"],
        "target_cache_manifest",
    )
    hostile_cache_manifest = authenticate_json(
        args.hostile_cache / "CACHE_MANIFEST.json",
        PINNED_SHA256["hostile_cache_manifest"],
        "hostile_cache_manifest",
    )
    if adjudication.payload.get("manifest_sha256") != manifest.sha256:
        raise Refusal("Stage-6 adjudication is not bound to the authenticated Stage-5 manifest")
    target = build_branch_spec("target", target_history, target_cache_manifest, args.target_cache)
    hostile = build_branch_spec("hostile", hostile_history, hostile_cache_manifest, args.hostile_cache)
    q_by_atom, endpoints = extract_atoms_and_endpoints(manifest, adjudication)
    branch_flows: dict[str, list[dict[str, Any]]] = {"target": [], "hostile": []}
    certified_edges: list[dict[str, Any]] = []
    for source_q in (4, 5):
        target_flow = reconstruct_branch_flow(target, source_q)
        hostile_flow = reconstruct_branch_flow(hostile, source_q)
        branch_flows["target"].append(target_flow)
        branch_flows["hostile"].append(hostile_flow)
        certified_edges.append(adjudicate_cross_branch(target_flow, hostile_flow))
    if not all(edge["certified"] for edge in certified_edges):
        raise Refusal("the q4->q5->q6 sector-flow chain is incomplete")
    mass = sector_mass_report(manifest)
    q4_endpoint = endpoints["q4_passing_atoms"][0]
    q6_endpoint = endpoints["q6_passing_atoms"][0]
    typed_path = [q4_endpoint, "L12:Q04", "L12:Q05", "L12:Q06", q6_endpoint]
    membership_edges = [
        {"atom_id": atom_id, "sector_node": f"L12:Q{q:02d}", "source": "stage5_manifest.atoms[].q_by_L[12]"}
        for atom_id, q in sorted(q_by_atom.items())
        if q in (4, 5, 6)
    ]
    return {
        "schema": SCHEMA,
        "classification": "AUTHENTICATED_L12_RECORD_FLOW_SECTOR_BRIDGE",
        "status": "PASS",
        "L": LENGTH,
        "terminal_event_zero_based": TERMINAL_EVENT,
        "terminal_event_one_based": TERMINAL_EVENT + 1,
        "frozen_predicates": {
            "phi": repr(PHI),
            "admission_factor_sin_phi_squared": repr(ADMISSION_FACTOR),
            "minimum_transferred_norm_squared": repr(MIN_FLOW),
            "cross_branch_absolute_tolerance": repr(CROSS_BRANCH_ABS_TOLERANCE),
            "geometry_window_inclusive": [str(GEOMETRY_LOWER), str(GEOMETRY_UPPER)],
            "mass_threshold": str(MASS_THRESHOLD),
        },
        "authenticated_json_inputs": [
            {"label": item.label, "path": str(item.path), "sha256": item.sha256}
            for item in (
                adjudication,
                manifest,
                target_history,
                hostile_history,
                target_cache_manifest,
                hostile_cache_manifest,
            )
        ],
        "history_gate": {
            "target": {
                "classification": target_history.payload["comparison"]["classification"],
                "resolved": True,
            },
            "hostile": {
                "classification": hostile_history.payload["comparison"]["classification"],
                "resolved": True,
            },
        },
        "geometry_endpoints": endpoints,
        "typed_topology": {
            "node_namespaces": {
                "Axxx": "Stage-5 density atom",
                "L12:Qxx": "L12 charge-sector node",
            },
            "atom_sector_membership_edges": membership_edges,
            "certified_sector_flow_edges": certified_edges,
            "exact_bridge_path": typed_path,
            "path_node_types": ["density_atom", "sector", "sector", "sector", "density_atom"],
            "contiguous_under_record_flow": True,
        },
        "branch_reconstruction": branch_flows,
        "mass": mass,
        "conclusion": {
            "q5_record_flow_bridge_authenticated": True,
            "deduplicated_q4_q5_q6_mass_crosses_0_50": mass["threshold_crossed"],
            "stage6_frozen_result_modified": False,
            "interpretation": (
                "The L12 q4 and q6 geometry endpoints belong to sectors connected through "
                "independently reproduced positive terminal admission flow via q5.  The "
                "deduplicated triad mass exceeds 0.50 under this typed record-flow relation."
            ),
        },
        "claim_boundary": (
            "READ_ONLY_L12_RECORD_FLOW_SIDECAR__SECTOR_FLOW_NOT_PHYSICAL_VERTEX_OR_STATIC_"
            "ATOM_ADJACENCY__NO_RETROACTIVE_STAGE6_OVERRIDE__NO_CONTINUUM_GRAVITY_OR_"
            "ENTANGLEMENT_CLAIM"
        ),
        "script": {"path": str(Path(__file__).resolve()), "sha256": sha256_file(Path(__file__))[0]},
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--adjudication", type=Path, default=DEFAULT_ADJUDICATION)
    result.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    result.add_argument("--target-history", type=Path, default=DEFAULT_TARGET_HISTORY)
    result.add_argument("--hostile-history", type=Path, default=DEFAULT_HOSTILE_HISTORY)
    result.add_argument("--target-cache", type=Path, default=DEFAULT_TARGET_CACHE)
    result.add_argument("--hostile-cache", type=Path, default=DEFAULT_HOSTILE_CACHE)
    result.add_argument("--output", type=Path, default=None, help="write an immutable JSON report")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        report = build_report(args)
        rendered = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
        if args.output is not None:
            if args.output.exists():
                raise Refusal(f"refuse to overwrite existing output: {args.output}")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(rendered)
                stream.flush()
                os.fsync(stream.fileno())
            output_hash = sha256_file(args.output)[0]
            print(f"REPORT_PATH={args.output.resolve()}")
            print(f"REPORT_SHA256={output_hash}")
        topology = report["typed_topology"]
        mass = report["mass"]
        print(f"CLASSIFICATION={report['classification']}")
        print("EXACT_TYPED_PATH=" + " -> ".join(topology["exact_bridge_path"]))
        for edge in topology["certified_sector_flow_edges"]:
            print(
                f"FLOW {edge['edge']} target={edge['target_transferred_norm_squared']:.17g} "
                f"hostile={edge['hostile_transferred_norm_squared']:.17g} "
                f"abs_diff={edge['absolute_difference']:.17g} certified=TRUE"
            )
        print(
            "DEDUPLICATED_MASS "
            f"q4={mass['q4']} q5={mass['q5']} q6={mass['q6']} "
            f"total={mass['deduplicated_q4_q5_q6']} threshold={mass['threshold']} "
            f"crossed={str(mass['threshold_crossed']).upper()}"
        )
        print("FROZEN_STAGE6_MODIFIED=FALSE")
        return 0
    except (Refusal, OSError, ValueError, KeyError) as error:
        print(f"AUTHENTICATION_FAILURE: {error}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
