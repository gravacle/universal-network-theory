#!/usr/bin/env python3
"""Authenticated, read-only L12 common-lineage support reconstruction.

This independent diagnostic reconstructs complete event-record histories from
the preserved prefix-11 sharp states and the exact terminal admission maps.
It never imports or launches a numerical solver and never mutates any prior
Stage-6 artifact.  Its primary measure is commensurate with Stage-5 ``pbar_q``:
for each native event 6..12 it counts the probability carried by a history
after its fifth acceptance (q4 -> q5) and before its sixth acceptance
(q5 -> q6), provided both boundary acceptances occur inside events 6..12,
then averages those seven event masses.

Publication fails closed unless Target and Hostile independently reproduce
the original q5 event ledger and terminal sector ledger and agree on the
strict common-lineage measure within the frozen tolerance.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import stat
import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LENGTH = 12
PREFIX = 11
TERMINAL_EVENT_ZERO_BASED = 11
EVENT_WINDOW = tuple(range(6, 13))
ADMISSION_FACTOR = math.sin(math.pi / 4.0) ** 2
STAY_BLANK_FACTOR = math.cos(math.pi / 4.0) ** 2
ABS_TOLERANCE = 1.0e-12
SCHEMA = "L12_LINEAGE_RESOLVED_SUPPORT_RECONSTRUCTION_V001"

DEFAULT_STAGE6 = (
    ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json"
)
DEFAULT_STAGE6R3 = (
    ROOT / "DEVELOPMENT_R_L12_STAGE6R3_RECORD_FLOW_ADJUDICATION_V001"
    / "STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json"
)
DEFAULT_FLOW = (
    ROOT / "DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001"
    / "RECORD_FLOW_BRIDGE_REPORT_V001.json"
)
DEFAULT_MANIFEST = (
    ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003"
    / "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
)
DEFAULT_TARGET_HISTORY = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012" / "PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
DEFAULT_HOSTILE_HISTORY = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "V004R4_PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
DEFAULT_TARGET_CACHE = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012" / "CACHE_PAYLOADS_V012" / "L12"
)
DEFAULT_HOSTILE_CACHE = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "V004R4_CACHE_PAYLOADS" / "L12"
)
DEFAULT_HOSTILE_SOURCE = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "independent_prefix_history.py"
DEFAULT_PROTOCOL = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001" / "PROTOCOL.md"
DEFAULT_DRIVER = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001" / "interval_spectrum_driver.py"
DEFAULT_OUTPUT = HERE / "LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json"

PINNED_SHA256 = {
    "stage6": "43c7c19daaf24902d2699c337851eca35a03c3db69f8e3f55f3b0142f87e137d",
    "stage6r3": "7fa2062f18be3c90c9167e917974d1cc609273da623966e4068f1c0d1133e2b4",
    "flow": "4a02db3eaea066a4c65bce921fcfaaffcc7e731b057d06f4c50180b6e38b40a6",
    "manifest": "292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a",
    "target_history": "079499e7b989e1ba45b1c397882c8638106be149ccb994058a3703b235736764",
    "hostile_history": "cbac18fd5033f83e4eadbfb16b46c89584455987e0b75fa6a33a33821246851c",
    "target_cache_manifest": "c8efb9b36ab18a3727aab4548109256640c92b63c121a07d9993999e4c570d6a",
    "hostile_cache_manifest": "1640607ea32c63a4af2139dc19a863e47b2fac5603656d059016710c774bceec",
    "hostile_source": "6ea113e5bb25f1c4b00c2ee186b253ce5eb0551773f90e25bdbb52ed1c636af5",
    "protocol": "db39a11dfb738fe206a5c0b5b34ec5c90ff29385f1d52aa33181814ec162ebb6",
    "driver": "2e8fede6cbfae9444f39d9e329347237915e42282ad9b667cd2631f3c5c8d9ad",
}


class Refusal(RuntimeError):
    """An authenticated input or a frozen reconstruction predicate failed."""


@dataclass(frozen=True)
class Identity:
    device: int
    inode: int
    size: int
    mtime_ns: int


@dataclass(frozen=True)
class AuthJSON:
    label: str
    path: Path
    sha256: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class Branch:
    label: str
    history: AuthJSON
    cache_manifest: AuthJSON
    cache_root: Path
    shard_root: Path
    shard_suffix: str

    def admission_names(self, source_q: int) -> tuple[str, str]:
        if self.label == "target":
            stem = f"admission_n_11_q_{source_q:02d}"
            return f"{stem}_blank.i32", f"{stem}_destination.i32"
        stem = f"event_11_q_{source_q + 1:02d}"
        return f"{stem}_old.i32", f"{stem}_occupied.i32"

    def carrier_name(self, q: int) -> str:
        if self.label == "target":
            return f"carrier_q_{q:02d}_words.u32"
        return f"q_{q:02d}_words.u32"


def identity(path: Path) -> Identity:
    try:
        item = path.stat()
    except OSError as error:
        raise Refusal(f"cannot stat {path}: {error}") from error
    if not stat.S_ISREG(item.st_mode):
        raise Refusal(f"not a regular file: {path}")
    return Identity(item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns)


def sha256_file(path: Path) -> tuple[str, Identity]:
    before = identity(path)
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(16 * 2**20), b""):
                digest.update(block)
    except OSError as error:
        raise Refusal(f"cannot hash {path}: {error}") from error
    after = identity(path)
    if after != before:
        raise Refusal(f"file changed while being hashed: {path}")
    return digest.hexdigest(), after


def authenticate_file(path: Path, expected: str, label: str) -> dict[str, Any]:
    actual, item = sha256_file(path)
    if actual != expected:
        raise Refusal(f"{label} SHA-256 mismatch: expected={expected} actual={actual} path={path}")
    return {"path": str(path.resolve()), "sha256": actual, "bytes": item.size}


def authenticate_json(path: Path, expected: str, label: str) -> AuthJSON:
    audit = authenticate_file(path, expected, label)
    before = identity(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{label} is not readable JSON: {error}") from error
    if identity(path) != before or not isinstance(payload, Mapping):
        raise Refusal(f"{label} changed while parsed or is not a JSON object")
    return AuthJSON(label, path.resolve(), audit["sha256"], payload)


def records(document: AuthJSON) -> dict[str, Mapping[str, Any]]:
    ledger = document.payload.get("files")
    if not isinstance(ledger, list):
        raise Refusal(f"{document.label}: files ledger absent")
    answer: dict[str, Mapping[str, Any]] = {}
    for item in ledger:
        if not isinstance(item, Mapping) or not isinstance(item.get("path"), str):
            raise Refusal(f"{document.label}: malformed cache record")
        name = item["path"]
        if name in answer:
            raise Refusal(f"{document.label}: duplicate cache record {name}")
        answer[name] = item
    return answer


def open_manifest_array(
    root: Path, ledger: Mapping[str, Mapping[str, Any]], name: str
) -> tuple[np.memmap, dict[str, Any], Identity]:
    record = ledger.get(name)
    if record is None:
        raise Refusal(f"cache manifest lacks {name}")
    try:
        dtype = np.dtype(record["dtype"])
        shape = tuple(record["shape"])
        expected_bytes = int(record["bytes"])
        expected_hash = str(record["sha256"])
    except (KeyError, TypeError, ValueError) as error:
        raise Refusal(f"malformed cache record {name}: {error}") from error
    if not shape or any(type(value) is not int or value < 0 for value in shape):
        raise Refusal(f"invalid shape for {name}: {shape}")
    if math.prod(shape) * dtype.itemsize != expected_bytes:
        raise Refusal(f"shape/byte mismatch in cache record {name}")
    path = (root / name).resolve()
    actual, item = sha256_file(path)
    if actual != expected_hash or item.size != expected_bytes:
        raise Refusal(f"cache array authentication failed: {name}")
    array = np.memmap(path, dtype=dtype, mode="r", shape=shape)
    audit = {
        "path": str(path), "sha256": actual, "bytes": item.size,
        "dtype": dtype.str, "shape": list(shape), "kind": record.get("kind"),
        "role": record.get("role"), "event": record.get("event"),
        "prefix": record.get("prefix"), "q": record.get("q"),
    }
    return array, audit, item


def close_array(array: np.ndarray) -> None:
    mapping = getattr(array, "_mmap", None)
    if mapping is not None:
        mapping.close()


def shard_record(history: AuthJSON, q: int) -> Mapping[str, Any]:
    shards = history.payload.get("terminal_shards")
    if not isinstance(shards, list):
        raise Refusal(f"{history.label}: terminal_shards absent")
    matches = [item for item in shards if isinstance(item, Mapping) and item.get("q") == q]
    if len(matches) != 1:
        raise Refusal(f"{history.label}: expected exactly one q={q} terminal shard")
    return matches[0]


def open_shard(branch: Branch, q: int) -> tuple[np.memmap, dict[str, Any], Identity]:
    record = shard_record(branch.history, q)
    expected_path = (branch.shard_root / f"q_{q:02d}{branch.shard_suffix}").resolve()
    try:
        recorded_path = Path(str(record["path"])).resolve()
        shape = tuple(record["shape"])
        expected_bytes = int(record["bytes"])
        expected_hash = str(record["sha256"])
    except (KeyError, TypeError, ValueError) as error:
        raise Refusal(f"{branch.label}: malformed q={q} shard record: {error}") from error
    expected_shape = (math.comb(PREFIX, q), math.comb(2 * LENGTH, q))
    if recorded_path != expected_path or shape != expected_shape:
        raise Refusal(
            f"{branch.label}: q={q} shard path/shape mismatch: "
            f"path={recorded_path}/{expected_path} shape={shape}/{expected_shape}"
        )
    actual, item = sha256_file(expected_path)
    if actual != expected_hash or item.size != expected_bytes:
        raise Refusal(f"{branch.label}: q={q} prefix shard failed authentication")
    if branch.shard_suffix == ".npy":
        array = np.load(expected_path, mmap_mode="r", allow_pickle=False)
    else:
        if expected_bytes != math.prod(shape) * np.dtype(np.complex128).itemsize:
            raise Refusal(f"{branch.label}: q={q} raw shard byte count is invalid")
        array = np.memmap(expected_path, dtype=np.complex128, mode="r", shape=shape)
    if array.shape != shape or array.dtype != np.dtype(np.complex128):
        close_array(array)
        raise Refusal(f"{branch.label}: q={q} shard array type/shape mismatch")
    return array, {
        "path": str(expected_path), "sha256": actual, "bytes": item.size,
        "dtype": array.dtype.str, "shape": list(shape), "prefix": PREFIX, "q": q,
    }, item


def fixed_masks(width: int, weight: int, reverse: bool = False) -> np.ndarray:
    order = reversed(range(width)) if reverse else range(width)
    answer = np.empty(math.comb(width, weight), dtype=np.uint32)
    for index, subset in enumerate(itertools.combinations(order, weight)):
        mask = 0
        for bit in subset:
            mask |= 1 << bit
        answer[index] = mask
    return answer


def validate_map(
    source_words: np.ndarray,
    destination_words: np.ndarray,
    source_indices: np.ndarray,
    destination_indices: np.ndarray,
) -> dict[str, Any]:
    if source_indices.ndim != 1 or destination_indices.ndim != 1:
        raise Refusal("terminal admission indices are not vectors")
    source = np.asarray(source_indices, dtype=np.int64)
    destination = np.asarray(destination_indices, dtype=np.int64)
    if len(source) == 0 or len(source) != len(destination):
        raise Refusal("terminal admission map is empty or unbalanced")
    if (
        source.min() < 0 or source.max() >= len(source_words)
        or destination.min() < 0 or destination.max() >= len(destination_words)
    ):
        raise Refusal("terminal admission index lies outside its carrier basis")
    if len(np.unique(source)) != len(source) or len(np.unique(destination)) != len(destination):
        raise Refusal("terminal admission map is not injective")
    before = np.asarray(source_words[source], dtype=np.uint64)
    after = np.asarray(destination_words[destination], dtype=np.uint64)
    event_bit = np.uint64(1 << TERMINAL_EVENT_ZERO_BASED)
    exact = bool(
        np.all(np.bitwise_and(before, event_bit) == 0)
        and np.all(np.bitwise_and(after, event_bit) != 0)
        and np.array_equal(after, np.bitwise_or(before, event_bit))
    )
    if not exact:
        raise Refusal("terminal admission map does not exactly insert event bit 11")
    return {
        "pair_count": len(source), "source_injective": True,
        "destination_injective": True, "exact_event_12_bit_insertion": True,
    }


def row_split(shard: np.ndarray, blank_indices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return final stay/accepted row norms after the event-12 admission."""
    stay = np.empty(shard.shape[0], dtype=np.float64)
    accepted = np.empty(shard.shape[0], dtype=np.float64)
    columns = np.asarray(blank_indices, dtype=np.int64)
    for row_index in range(shard.shape[0]):
        row = np.asarray(shard[row_index])
        total = float(np.vdot(row, row).real)
        selected = np.asarray(row[columns])
        blank = float(np.vdot(selected, selected).real)
        accepted[row_index] = ADMISSION_FACTOR * blank
        stay[row_index] = total - (1.0 - STAY_BLANK_FACTOR) * blank
    if (
        not np.all(np.isfinite(stay)) or not np.all(np.isfinite(accepted))
        or float(stay.min(initial=0.0)) < -ABS_TOLERANCE
        or float(accepted.min(initial=0.0)) < -ABS_TOLERANCE
    ):
        raise Refusal("terminal row split produced invalid probability mass")
    stay[abs(stay) < 1e-16] = 0.0
    accepted[abs(accepted) < 1e-16] = 0.0
    return stay, accepted


def acceptance_events(mask: int) -> tuple[int, ...]:
    return tuple(bit + 1 for bit in range(LENGTH) if mask & (1 << bit))


def add_lineage_mass(
    buckets: dict[str, np.ndarray], mask: int, mass: float
) -> None:
    events = acceptance_events(mask)
    if len(events) < 5 or mass == 0.0:
        return
    entry = events[4]
    exit_event = events[5] if len(events) >= 6 else None
    if exit_event is None:
        category = "no_exit_by_event_12"
    elif entry >= EVENT_WINDOW[0] and exit_event <= EVENT_WINDOW[-1]:
        category = "strict_window_common_lineage"
    elif entry < EVENT_WINDOW[0] and exit_event <= EVENT_WINDOW[-1]:
        category = "prewindow_entry_then_window_exit"
    else:
        raise Refusal(f"unclassifiable q5 lineage: mask={mask} entry={entry} exit={exit_event}")
    for index, event in enumerate(EVENT_WINDOW):
        if entry <= event and (exit_event is None or event < exit_event):
            buckets[category][index] += mass


def history_rows(history: AuthJSON) -> list[Mapping[str, Any]]:
    rows = history.payload.get("rows")
    if not isinstance(rows, list) or len(rows) != LENGTH:
        raise Refusal(f"{history.label}: exact 12-row event ledger absent")
    for expected_event, row in enumerate(rows, 1):
        if not isinstance(row, Mapping) or row.get("event") != expected_event:
            raise Refusal(f"{history.label}: event ledger order mismatch")
    comparison = history.payload.get("comparison")
    if not isinstance(comparison, Mapping) or comparison.get("resolved") is not True:
        raise Refusal(f"{history.label}: history is not resolved")
    return rows


def reconstruct_branch(branch: Branch) -> dict[str, Any]:
    ledger = records(branch.cache_manifest)
    rows = history_rows(branch.history)
    observed_q5 = np.asarray(
        [float(rows[event - 1]["sector_weights"][5]) for event in EVENT_WINDOW],
        dtype=np.float64,
    )
    buckets = {
        "strict_window_common_lineage": np.zeros(len(EVENT_WINDOW), dtype=np.float64),
        "prewindow_entry_then_window_exit": np.zeros(len(EVENT_WINDOW), dtype=np.float64),
        "no_exit_by_event_12": np.zeros(len(EVENT_WINDOW), dtype=np.float64),
    }
    terminal = np.zeros(LENGTH + 1, dtype=np.float64)
    input_audits: list[dict[str, Any]] = []

    for source_q in range(4, 12):
        source_name, destination_name = branch.admission_names(source_q)
        blank, blank_audit, blank_identity = open_manifest_array(branch.cache_root, ledger, source_name)
        destination, destination_audit, destination_identity = open_manifest_array(
            branch.cache_root, ledger, destination_name
        )
        source_words, source_words_audit, source_words_identity = open_manifest_array(
            branch.cache_root, ledger, branch.carrier_name(source_q)
        )
        destination_words, destination_words_audit, destination_words_identity = open_manifest_array(
            branch.cache_root, ledger, branch.carrier_name(source_q + 1)
        )
        lineage_identity: Identity | None = None
        if branch.label == "target":
            lineage_name = f"lineage_n_11_q_{source_q:02d}_words.u32"
            lineage, lineage_audit, lineage_identity = open_manifest_array(
                branch.cache_root, ledger, lineage_name
            )
        else:
            lineage = fixed_masks(PREFIX, source_q, reverse=True)
            lineage_audit = {
                "source": "hash-pinned independent_prefix_history.reverse_masks",
                "shape": list(lineage.shape), "dtype": lineage.dtype.str,
                "prefix": PREFIX, "q": source_q,
            }
        shard, shard_audit, shard_identity = open_shard(branch, source_q)
        try:
            expected_pairs = math.comb(2 * LENGTH - 1, source_q)
            map_q = source_q if branch.label == "target" else source_q + 1
            expected_roles = ("blank", "destination") if branch.label == "target" else ("old", "occupied")
            for audit, role in ((blank_audit, expected_roles[0]), (destination_audit, expected_roles[1])):
                if (
                    audit["kind"] != "admission" or audit["role"] != role
                    or audit["event"] != TERMINAL_EVENT_ZERO_BASED or audit["q"] != map_q
                    or audit["shape"] != [expected_pairs]
                ):
                    raise Refusal(f"{branch.label}: malformed q={source_q} admission metadata")
            for audit, q in ((source_words_audit, source_q), (destination_words_audit, source_q + 1)):
                if (
                    audit["kind"] != "operator" or audit["role"] != "words"
                    or audit["q"] != q or audit["shape"] != [math.comb(2 * LENGTH, q)]
                ):
                    raise Refusal(f"{branch.label}: malformed q={q} carrier-word metadata")
            if branch.label == "target":
                if (
                    lineage_audit["kind"] != "lineage_mask" or lineage_audit["role"] != "words"
                    or lineage_audit["prefix"] != PREFIX or lineage_audit["q"] != source_q
                ):
                    raise Refusal(f"target: malformed q={source_q} lineage metadata")
                expected_lineage = fixed_masks(PREFIX, source_q)
                if not np.array_equal(np.asarray(lineage), expected_lineage):
                    raise Refusal(f"target: q={source_q} lineage order differs from fixed mask order")
            if len(lineage) != shard.shape[0]:
                raise Refusal(f"{branch.label}: q={source_q} lineage/shard row mismatch")
            map_checks = validate_map(source_words, destination_words, blank, destination)
            stay, accepted = row_split(shard, blank)
            terminal[source_q] += float(np.sum(stay, dtype=np.float64))
            terminal[source_q + 1] += float(np.sum(accepted, dtype=np.float64))
            for row_index, prefix_mask in enumerate(np.asarray(lineage, dtype=np.uint32)):
                add_lineage_mass(buckets, int(prefix_mask), float(stay[row_index]))
                add_lineage_mass(
                    buckets,
                    int(prefix_mask) | (1 << TERMINAL_EVENT_ZERO_BASED),
                    float(accepted[row_index]),
                )
            input_audits.append({
                "source_q": source_q, "admission_map": map_checks,
                "blank_indices": blank_audit, "destination_indices": destination_audit,
                "source_carrier_words": source_words_audit,
                "destination_carrier_words": destination_words_audit,
                "lineage_words": lineage_audit, "prefix_shard": shard_audit,
            })
            identities = [
                ((branch.cache_root / source_name).resolve(), blank_identity),
                ((branch.cache_root / destination_name).resolve(), destination_identity),
                ((branch.cache_root / branch.carrier_name(source_q)).resolve(), source_words_identity),
                ((branch.cache_root / branch.carrier_name(source_q + 1)).resolve(), destination_words_identity),
                ((branch.shard_root / f"q_{source_q:02d}{branch.shard_suffix}").resolve(), shard_identity),
            ]
            if lineage_identity is not None:
                identities.append(((branch.cache_root / lineage_name).resolve(), lineage_identity))
            if any(identity(path) != item for path, item in identities):
                raise Refusal(f"{branch.label}: authenticated q={source_q} input changed during read")
        finally:
            for array in (blank, destination, source_words, destination_words, lineage, shard):
                close_array(array)

    reconstructed_q5 = sum(buckets.values(), np.zeros(len(EVENT_WINDOW), dtype=np.float64))
    event_residual = reconstructed_q5 - observed_q5
    observed_terminal = np.asarray(rows[-1]["sector_weights"], dtype=np.float64)
    terminal_residual = terminal[5:13] - observed_terminal[5:13]
    if float(np.max(np.abs(event_residual))) > ABS_TOLERANCE:
        raise Refusal(f"{branch.label}: q5 event decomposition does not reproduce history")
    if float(np.max(np.abs(terminal_residual))) > ABS_TOLERANCE:
        raise Refusal(f"{branch.label}: terminal sectors q5..q12 do not reproduce history")
    strict = buckets["strict_window_common_lineage"]
    prewindow = buckets["prewindow_entry_then_window_exit"]
    return {
        "branch": branch.label,
        "event_window": list(EVENT_WINDOW),
        "strict_common_lineage_support_by_event": strict.tolist(),
        "strict_common_lineage_pbar_support": float(np.mean(strict)),
        "prewindow_entry_then_window_exit_by_event": prewindow.tolist(),
        "prewindow_entry_then_window_exit_pbar": float(np.mean(prewindow)),
        "all_entry_common_exit_pbar_support": float(np.mean(strict + prewindow)),
        "no_exit_by_event_12_by_event": buckets["no_exit_by_event_12"].tolist(),
        "no_exit_by_event_12_pbar": float(np.mean(buckets["no_exit_by_event_12"])),
        "observed_q5_mass_by_event": observed_q5.tolist(),
        "observed_q5_pbar": float(np.mean(observed_q5)),
        "decomposition_residual_by_event": event_residual.tolist(),
        "maximum_absolute_decomposition_residual": float(np.max(np.abs(event_residual))),
        "reconstructed_terminal_sector_mass_q5_through_q12": terminal[5:13].tolist(),
        "observed_terminal_sector_mass_q5_through_q12": observed_terminal[5:13].tolist(),
        "terminal_residual_q5_through_q12": terminal_residual.tolist(),
        "maximum_absolute_terminal_residual": float(np.max(np.abs(terminal_residual))),
        "authenticated_inputs_by_source_q": input_audits,
    }


def failed_predicate_autopsy(stage6: AuthJSON) -> dict[str, Any]:
    results = stage6.payload.get("atom_results")
    if not isinstance(results, list):
        raise Refusal("Stage-6 atom_results absent")
    indexed = {
        item.get("atom", {}).get("atom_id"): item
        for item in results if isinstance(item, Mapping) and isinstance(item.get("atom"), Mapping)
    }
    answer: dict[str, Any] = {}
    for atom_id in ("A011", "A016"):
        item = indexed.get(atom_id)
        if not isinstance(item, Mapping):
            raise Refusal(f"Stage-6 result lacks {atom_id}")
        branch_reports: dict[str, Any] = {}
        for branch_name, key in (("target", "target_classification"), ("blind", "blind_classification")):
            classification = item.get(key)
            if not isinstance(classification, Mapping) or not isinstance(classification.get("checks"), Mapping):
                raise Refusal(f"Stage-6 {atom_id}/{branch_name} classification absent")
            checks = classification["checks"]
            failures: list[dict[str, Any]] = []
            if checks.get("exponents_agree") is False:
                z = float(classification["gap_power_fit"]["exponent"])
                y = float(classification["chi_power_exponent_y"])
                value = abs(z - y)
                failures.append({
                    "predicate": "exponents_agree", "expression": "abs(z-y) <= 0.10",
                    "z": z, "y": y, "value": value, "threshold": 0.10,
                    "excess_over_threshold": value - 0.10,
                })
            for check, scalar in (
                ("tail_scaled_gap_stable", "tail_scaled_gap_relative_range"),
                ("tail_scaled_chi_stable", "tail_scaled_chi_relative_range"),
            ):
                if checks.get(check) is False:
                    value = float(classification[scalar])
                    failures.append({
                        "predicate": check, "expression": f"{scalar} <= 0.05",
                        "value": value, "threshold": 0.05,
                        "excess_over_threshold": value - 0.05,
                    })
            if checks.get("fixed_z1_beats_positive_gap") is False:
                fixed = float(classification["fixed_z1_heldout_sse_relative"])
                positive = float(classification["positive_gap_heldout_sse_relative"])
                failures.append({
                    "predicate": "fixed_z1_beats_positive_gap",
                    "expression": "fixed_z1_heldout_sse_relative < positive_gap_heldout_sse_relative",
                    "fixed_z1_heldout_sse_relative": fixed,
                    "positive_gap_heldout_sse_relative": positive,
                    "ratio_fixed_to_positive_gap": fixed / positive,
                    "failed_margin": fixed - positive,
                })
            if checks.get("fixed_z1_near_free_gapless") is False:
                fixed = float(classification["fixed_z1_heldout_sse_relative"])
                gapless = float(classification["gapless_heldout_sse_relative"])
                ceiling = 1.25 * gapless
                failures.append({
                    "predicate": "fixed_z1_near_free_gapless",
                    "expression": "fixed_z1_heldout_sse_relative <= 1.25 * gapless_heldout_sse_relative",
                    "fixed_z1_heldout_sse_relative": fixed,
                    "gapless_heldout_sse_relative": gapless,
                    "multiplier": 1.25, "ceiling": ceiling,
                    "ratio_fixed_to_gapless": fixed / gapless,
                    "excess_over_ceiling": fixed - ceiling,
                })
            false_checks = sorted(name for name, passed in checks.items() if passed is False)
            if sorted(failure["predicate"] for failure in failures) != false_checks:
                raise Refusal(
                    f"autopsy did not account for every false predicate in {atom_id}/{branch_name}: "
                    f"accounted={sorted(failure['predicate'] for failure in failures)} actual={false_checks}"
                )
            branch_reports[branch_name] = {
                "classification": classification.get("classification"),
                "passes": classification.get("passes"),
                "false_predicates": false_checks,
                "failure_scalars": failures,
            }
        answer[atom_id] = {
            "q_at_L12": item["atom"]["q_by_L"]["12"],
            "original_full_conjunction_passes": item.get("passes"),
            "failure_domain": "FINITE_SIZE_SPECTRAL_SCALING_OR_MODEL_SELECTION__NOT_A_MASS_PREDICATE",
            "branches": branch_reports,
        }
    return answer


def pbar_q5(manifest: AuthJSON) -> float:
    histories = manifest.payload.get("histories")
    l12 = histories.get("12") if isinstance(histories, Mapping) else None
    values = l12.get("pbar_q") if isinstance(l12, Mapping) else None
    if not isinstance(values, list) or len(values) != LENGTH + 1:
        raise Refusal("Stage-5 L12 pbar_q absent")
    return float(values[5])


def required_support(manifest: AuthJSON) -> float:
    histories = manifest.payload.get("histories")
    l12 = histories.get("12") if isinstance(histories, Mapping) else None
    values = l12.get("pbar_q") if isinstance(l12, Mapping) else None
    if not isinstance(values, list) or len(values) != LENGTH + 1:
        raise Refusal("Stage-5 L12 pbar_q absent")
    required = Decimal("0.50") - Decimal(str(values[4])) - Decimal(str(values[6]))
    if required <= 0:
        raise Refusal("derived q5 support requirement is not positive")
    return float(required)


def atomic_create_json(path: Path, payload: Mapping[str, Any]) -> str:
    if path.exists():
        raise Refusal(f"refusing to overwrite existing report: {path}")
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(path, flags, 0o444)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        try:
            path.unlink()
        except OSError:
            pass
        raise
    return hashlib.sha256(encoded).hexdigest()


def run(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    documents = {
        "stage6": authenticate_json(args.stage6, PINNED_SHA256["stage6"], "Stage-6R2 adjudication"),
        "stage6r3": authenticate_json(args.stage6r3, PINNED_SHA256["stage6r3"], "Stage-6R3 adjudication"),
        "flow": authenticate_json(args.flow, PINNED_SHA256["flow"], "record-flow sidecar"),
        "manifest": authenticate_json(args.manifest, PINNED_SHA256["manifest"], "Stage-5 manifest"),
        "target_history": authenticate_json(
            args.target_history, PINNED_SHA256["target_history"], "Target history"
        ),
        "hostile_history": authenticate_json(
            args.hostile_history, PINNED_SHA256["hostile_history"], "Hostile history"
        ),
        "target_cache_manifest": authenticate_json(
            args.target_cache / "CACHE_MANIFEST.json", PINNED_SHA256["target_cache_manifest"],
            "Target cache manifest",
        ),
        "hostile_cache_manifest": authenticate_json(
            args.hostile_cache / "CACHE_MANIFEST.json", PINNED_SHA256["hostile_cache_manifest"],
            "Hostile cache manifest",
        ),
    }
    source_audits = {
        "hostile_lineage_order_source": authenticate_file(
            args.hostile_source, PINNED_SHA256["hostile_source"], "Hostile lineage source"
        ),
        "stage6_protocol": authenticate_file(args.protocol, PINNED_SHA256["protocol"], "protocol"),
        "stage6_driver": authenticate_file(args.driver, PINNED_SHA256["driver"], "driver"),
    }
    target = Branch(
        "target", documents["target_history"], documents["target_cache_manifest"],
        args.target_cache.resolve(),
        (ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012" / "WORKSPACES"
         / "L12_PROCESS_PARALLEL_V003R1" / "sharp" / "prefix_11").resolve(),
        ".npy",
    )
    hostile = Branch(
        "hostile", documents["hostile_history"], documents["hostile_cache_manifest"],
        args.hostile_cache.resolve(),
        (ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "V004R4_WORKSPACES"
         / "L12_PROCESS_PARALLEL_V002" / "sharp" / "prefix_11").resolve(),
        ".c128",
    )
    print("AUTHENTICATION_OK: pinned Stage-5/6 histories, cache manifests, and method sources")
    print("RECONSTRUCTING: Target complete record lineages from prefix_11 q=4..11")
    target_result = reconstruct_branch(target)
    print("RECONSTRUCTING: Hostile complete record lineages from prefix_11 q=4..11")
    hostile_result = reconstruct_branch(hostile)

    required = required_support(documents["manifest"])
    manifest_q5 = pbar_q5(documents["manifest"])
    target_value = float(target_result["strict_common_lineage_pbar_support"])
    hostile_value = float(hostile_result["strict_common_lineage_pbar_support"])
    cross_difference = abs(target_value - hostile_value)
    if cross_difference > ABS_TOLERANCE:
        raise Refusal(
            f"Target/Hostile strict support mismatch: {target_value}/{hostile_value}"
        )
    if abs(float(target_result["observed_q5_pbar"]) - manifest_q5) > ABS_TOLERANCE:
        raise Refusal("Target event-native q5 average differs from Stage-5 pbar_q[5]")
    if abs(float(hostile_result["observed_q5_pbar"]) - manifest_q5) > ABS_TOLERANCE:
        raise Refusal("Hostile event-native q5 average differs from Stage-5 pbar_q[5]")
    conservative = min(target_value, hostile_value)
    cleared = conservative >= required
    autopsy = failed_predicate_autopsy(documents["stage6"])
    classification = (
        "LINEAGE_RESOLVED_Q5_SUPPORT_THRESHOLD_CLEARED"
        if cleared else "LINEAGE_RESOLVED_Q5_SUPPORT_BELOW_REQUIRED_THRESHOLD"
    )
    report = {
        "schema": SCHEMA,
        "status": "COMPLETE__READ_ONLY_RECONSTRUCTION",
        "classification": classification,
        "claim_boundary": (
            "EXACT_FINITE_L12_EVENT_RECORD_LINEAGE_SUPPORT_DIAGNOSTIC_ONLY__"
            "DOES_NOT_MODIFY_OR_SUPERSEDE_STAGE6R2_STAGE6R3_OR_RECORD_FLOW_SIDECAR"
        ),
        "method": {
            "event_window": list(EVENT_WINDOW),
            "primary_measure": (
                "mean over native events 6..12 of final-history probability mass resident in q5 "
                "after its fifth acceptance and before its sixth acceptance, with both acceptance "
                "events inside 6..12"
            ),
            "lineage_boundary": "fifth acceptance is q4->q5; sixth acceptance is q5->q6",
            "terminal_reconstruction": {
                "accepted_row_mass": "sin(pi/4)^2 * prefix-row blank-column norm",
                "stay_row_mass": "prefix-row norm - (1-cos(pi/4)^2) * blank-column norm",
                "row_norm_after_transport": "unchanged by row-independent unitary transport",
            },
            "absolute_audit_tolerance": ABS_TOLERANCE,
        },
        "threshold_adjudication": {
            "macroscopic_mass_threshold": 0.50,
            "stage5_q4_mass": float(documents["manifest"].payload["histories"]["12"]["pbar_q"][4]),
            "stage5_q6_mass": float(documents["manifest"].payload["histories"]["12"]["pbar_q"][6]),
            "required_q5_common_lineage_support": required,
            "target_strict_support": target_value,
            "hostile_strict_support": hostile_value,
            "conservative_support": conservative,
            "shortfall": max(0.0, required - conservative),
            "target_hostile_absolute_difference": cross_difference,
            "threshold_cleared": cleared,
        },
        "target": target_result,
        "hostile": hostile_result,
        "original_stage6_conjunction_autopsy": autopsy,
        "authenticated_documents": {
            name: {"path": str(doc.path), "sha256": doc.sha256}
            for name, doc in documents.items()
        },
        "authenticated_method_sources": source_audits,
        "prior_artifacts_mutated": False,
        "stage7_started": False,
    }
    report_hash = atomic_create_json(args.output, report)
    print("\nLINEAGE FLOW (strict common q4 -> q5 -> q6 support)")
    for index, event in enumerate(EVENT_WINDOW):
        print(
            f"  event={event:2d} target={target_result['strict_common_lineage_support_by_event'][index]:.17g} "
            f"hostile={hostile_result['strict_common_lineage_support_by_event'][index]:.17g}"
        )
    print(f"  target pbar support:      {target_value:.17g}")
    print(f"  hostile pbar support:     {hostile_value:.17g}")
    print(f"  conservative support:     {conservative:.17g}")
    print(f"  required q5 support:      {required:.17g}")
    print(f"  shortfall:                {max(0.0, required - conservative):.17g}")
    print(f"  THRESHOLD_CLEARED:        {cleared}")
    print("\nORIGINAL STAGE-6 CONJUNCTION AUTOPSY")
    for atom_id, atom in autopsy.items():
        for branch_name, branch_report in atom["branches"].items():
            print(f"  {atom_id}/{branch_name}: {', '.join(branch_report['false_predicates'])}")
            for failure in branch_report["failure_scalars"]:
                print(f"    {failure['predicate']}: {json.dumps(failure, sort_keys=True)}")
    print(f"\nREPORT: {args.output.resolve()}")
    print(f"REPORT_SHA256: {report_hash}")
    return report, report_hash


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--stage6", type=Path, default=DEFAULT_STAGE6)
    value.add_argument("--stage6r3", type=Path, default=DEFAULT_STAGE6R3)
    value.add_argument("--flow", type=Path, default=DEFAULT_FLOW)
    value.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    value.add_argument("--target-history", type=Path, default=DEFAULT_TARGET_HISTORY)
    value.add_argument("--hostile-history", type=Path, default=DEFAULT_HOSTILE_HISTORY)
    value.add_argument("--target-cache", type=Path, default=DEFAULT_TARGET_CACHE)
    value.add_argument("--hostile-cache", type=Path, default=DEFAULT_HOSTILE_CACHE)
    value.add_argument("--hostile-source", type=Path, default=DEFAULT_HOSTILE_SOURCE)
    value.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    value.add_argument("--driver", type=Path, default=DEFAULT_DRIVER)
    value.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        run(parser().parse_args(argv))
        return 0
    except Refusal as error:
        print(f"AUTHENTICATED_RECONSTRUCTION_REFUSAL: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
