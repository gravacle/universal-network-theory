#!/usr/bin/env python3
"""Fail-closed validator for the exact L10/L12 held-out input/resource gate.

This program authenticates control-plane documents and retained shard bytes.
It never interprets an amplitude or computes a witness value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any


PACKET = Path(__file__).resolve().parent
REPO = PACKET.parent
GATE_PATH = PACKET / "INPUT_AND_RESOURCE_GATE.json"
SOURCE_MANIFEST = PACKET / "SOURCE_HASHES.sha256"

SCHEMA = "OWNER_ONCE_HELDOUT_L10_L12_INPUT_AND_RESOURCE_GATE_V001"
STATUS = "FROZEN_PRE_HELDOUT_OUTPUT__READY_FOR_AUTHORIZED_EXACT_EXECUTION"
TELEMETRY_SCHEMA = "OWNER_ONCE_HELDOUT_RESOURCE_TELEMETRY_V001"


class Refusal(RuntimeError):
    """A fail-closed custody, schema, or resource refusal."""


def sha256(path: Path, chunk: int = 8 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise Refusal(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_json_bytes(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Refusal("JSON is not UTF-8") from error

    def nonfinite(token: str) -> None:
        raise Refusal(f"nonfinite JSON constant: {token}")

    try:
        return json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=nonfinite,
        )
    except Refusal:
        raise
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise Refusal("invalid strict JSON") from error


def strict_json(path: Path) -> Any:
    if path.is_symlink() or not path.is_file():
        raise Refusal(f"required JSON is absent, nonregular, or symlinked: {path}")
    return strict_json_bytes(path.read_bytes())


def require_exact_keys(record: dict[str, Any], keys: set[str], label: str) -> None:
    actual = set(record)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        raise Refusal(f"{label} key mismatch; missing={missing} extra={extra}")


def canonical_relative(raw: str) -> str:
    path = Path(raw)
    if path.is_absolute():
        try:
            path = path.resolve().relative_to(REPO.resolve())
        except ValueError as error:
            raise Refusal(f"absolute shard path escapes repository: {raw}") from error
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise Refusal(f"unsafe shard path: {raw}")
    return path.as_posix()


def canonical_shard_rows(history: dict[str, Any], expected_root: str) -> list[dict[str, Any]]:
    shards = history.get("terminal_shards")
    if not isinstance(shards, list):
        raise Refusal("history terminal_shards is not a list")
    rows: list[dict[str, Any]] = []
    for shard in shards:
        if not isinstance(shard, dict):
            raise Refusal("terminal shard is not an object")
        require_exact_keys(shard, {"bytes", "path", "q", "sha256", "shape"}, "terminal shard")
        rel = canonical_relative(shard["path"])
        if Path(rel).parent.as_posix() != expected_root:
            raise Refusal(f"terminal shard root mismatch: {rel}")
        if type(shard["q"]) is not int or shard["q"] < 0:
            raise Refusal("invalid terminal shard q")
        if type(shard["bytes"]) is not int or shard["bytes"] <= 0:
            raise Refusal("invalid terminal shard byte count")
        if not isinstance(shard["sha256"], str) or len(shard["sha256"]) != 64:
            raise Refusal("invalid terminal shard digest")
        shape = shard["shape"]
        if (
            not isinstance(shape, list)
            or len(shape) != 2
            or any(type(item) is not int or item <= 0 for item in shape)
        ):
            raise Refusal("invalid terminal shard shape")
        rows.append(
            {
                "bytes": shard["bytes"],
                "path": rel,
                "q": shard["q"],
                "sha256": shard["sha256"],
                "shape": shape,
            }
        )
    return rows


def shard_manifest_digest(rows: list[dict[str, Any]]) -> str:
    raw = (json.dumps(rows, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_resource_arithmetic(resource: dict[str, Any]) -> None:
    expected = {
        "combined_scratch_minimum_bytes": 19_201_889_580,
        "concurrent_available_memory_minimum_bytes": 34_865_626_528,
        "concurrent_headroom_on_decimal_48gb_host_bytes": 13_134_373_472,
        "concurrent_total_host_memory_minimum_bytes": 48_000_000_000,
        "hard_wall_limit_seconds_per_branch": 345_600,
        "hostile_scratch_minimum_bytes": 9_600_935_128,
        "maximum_release_skew_seconds": 60,
        "per_process_rss_limit_bytes": 17_179_869_184,
        "schedule_selection": "CONCURRENT_IF_FRESH_GATE_PASSES_ELSE_SEQUENTIAL",
        "successor_resource_arithmetic": "2*(17179869184+252944080)=34865626528",
        "target_scratch_minimum_bytes": 9_600_954_452,
        "telemetry_max_age_seconds": 300,
        "v003_successor_only": True,
    }
    if resource != expected:
        raise Refusal("resource gate differs from frozen exact values")
    authentication_peak = 252_944_080
    if 2 * (resource["per_process_rss_limit_bytes"] + authentication_peak) != resource[
        "concurrent_available_memory_minimum_bytes"
    ]:
        raise Refusal("concurrent memory arithmetic mismatch")
    if (
        resource["concurrent_total_host_memory_minimum_bytes"]
        - resource["concurrent_available_memory_minimum_bytes"]
        != resource["concurrent_headroom_on_decimal_48gb_host_bytes"]
    ):
        raise Refusal("headroom arithmetic mismatch")
    if (
        resource["target_scratch_minimum_bytes"]
        + resource["hostile_scratch_minimum_bytes"]
        != resource["combined_scratch_minimum_bytes"]
    ):
        raise Refusal("scratch arithmetic mismatch")


def validate_telemetry(
    telemetry: dict[str, Any], resource: dict[str, Any], now_epoch_seconds: int
) -> str:
    required = {
        "schema",
        "selected_schedule",
        "captured_epoch_seconds",
        "total_host_memory_bytes",
        "available_memory_bytes",
        "memory_pressure",
        "shared_filesystem_free_bytes",
        "target_scratch_root",
        "hostile_scratch_root",
        "target_output_path",
        "hostile_output_path",
    }
    require_exact_keys(telemetry, required, "telemetry")
    if telemetry["schema"] != TELEMETRY_SCHEMA:
        raise Refusal("telemetry schema mismatch")
    schedule = telemetry["selected_schedule"]
    if schedule not in {"SEQUENTIAL_TARGET_THEN_HOSTILE", "CONCURRENT_TARGET_AND_HOSTILE"}:
        raise Refusal("invalid selected schedule")
    capture = telemetry["captured_epoch_seconds"]
    if type(capture) is not int or type(now_epoch_seconds) is not int:
        raise Refusal("telemetry epochs must be integers")
    age = now_epoch_seconds - capture
    if age < 0 or age > resource["telemetry_max_age_seconds"]:
        raise Refusal("telemetry is stale or future-dated")
    for key in ("total_host_memory_bytes", "available_memory_bytes", "shared_filesystem_free_bytes"):
        if type(telemetry[key]) is not int or telemetry[key] < 0:
            raise Refusal(f"invalid telemetry integer: {key}")
    if telemetry["memory_pressure"] != "NORMAL":
        raise Refusal("memory pressure is not NORMAL")
    if telemetry["shared_filesystem_free_bytes"] < resource["combined_scratch_minimum_bytes"]:
        raise Refusal("insufficient shared-filesystem scratch")
    paths = [
        telemetry["target_scratch_root"],
        telemetry["hostile_scratch_root"],
        telemetry["target_output_path"],
        telemetry["hostile_output_path"],
    ]
    if any(not isinstance(item, str) or not item or Path(item).is_absolute() or ".." in Path(item).parts for item in paths):
        raise Refusal("telemetry paths must be safe repository-relative paths")
    if len(set(paths)) != len(paths):
        raise Refusal("scratch and output paths are not pairwise distinct")
    if schedule == "CONCURRENT_TARGET_AND_HOSTILE":
        if telemetry["total_host_memory_bytes"] < resource["concurrent_total_host_memory_minimum_bytes"]:
            raise Refusal("concurrent total host memory gate failed")
        if telemetry["available_memory_bytes"] < resource["concurrent_available_memory_minimum_bytes"]:
            raise Refusal("concurrent available-memory gate failed")
    return schedule


def validate_source_manifest() -> None:
    if SOURCE_MANIFEST.is_symlink() or not SOURCE_MANIFEST.is_file():
        raise Refusal("SOURCE_HASHES.sha256 absent or symlinked")
    lines = SOURCE_MANIFEST.read_text(encoding="ascii").splitlines()
    expected_names = {
        "INPUT_AND_RESOURCE_GATE.json",
        "PROTOCOL.md",
        "README.md",
        "test_validate_heldout_gate.py",
        "validate_heldout_gate.py",
    }
    seen: set[str] = set()
    for line in lines:
        parts = line.split("  ")
        if len(parts) != 2 or len(parts[0]) != 64:
            raise Refusal("malformed source manifest row")
        digest, name = parts
        if name in seen or name not in expected_names:
            raise Refusal("unexpected or duplicate source manifest member")
        seen.add(name)
        member = PACKET / name
        if member.is_symlink() or not member.is_file() or sha256(member) != digest:
            raise Refusal(f"source manifest mismatch: {name}")
    if seen != expected_names:
        raise Refusal("source manifest census mismatch")


def validate_gate(full_shard_hash: bool = False) -> dict[str, Any]:
    gate = strict_json(GATE_PATH)
    if not isinstance(gate, dict) or gate.get("schema") != SCHEMA or gate.get("status") != STATUS:
        raise Refusal("gate schema or status mismatch")
    require_exact_keys(
        gate,
        {
            "absence_at_freeze",
            "authorization_tokens",
            "authority",
            "claim_boundary",
            "classifications",
            "deterministic_output",
            "execution",
            "fresh_telemetry",
            "heldout_statistic",
            "historical_runtime_reference",
            "inputs",
            "resource_gate",
            "schema",
            "status",
        },
        "gate",
    )
    if gate["absence_at_freeze"] != {
        "heldout_hostile_result_present": False,
        "heldout_reconciliation_present": False,
        "heldout_target_result_present": False,
        "l10_witness_computed_or_opened": False,
        "l12_witness_computed_or_opened": False,
    }:
        raise Refusal("held-out absence declaration changed")
    validate_resource_arithmetic(gate["resource_gate"])

    for record in gate["authority"].values():
        path = REPO / record["path"]
        if path.is_symlink() or not path.is_file() or sha256(path) != record["sha256"]:
            raise Refusal(f"authority hash mismatch: {record['path']}")

    seed = strict_json(REPO / gate["authority"]["seed_final_disposition"]["path"])
    if (
        seed.get("protocol_classification")
        != gate["authority"]["seed_final_disposition"]["required_classification"]
        or seed.get("passed") is not True
        or seed.get("all_numerical_and_control_conditions_passed") is not True
        or not isinstance(seed.get("T_4_8"), (int, float))
        or isinstance(seed.get("T_4_8"), bool)
        or not math.isfinite(seed["T_4_8"])
        or seed["T_4_8"] <= 1
        or seed.get("held_out_L10_L12", {}).get("computed_or_opened_by_reconciliation") is not False
    ):
        raise Refusal("seed prerequisite failed")

    inputs = gate["inputs"]
    if not isinstance(inputs, list) or [(row.get("role"), row.get("length")) for row in inputs] != [
        ("target", 10),
        ("target", 12),
        ("hostile", 10),
        ("hostile", 12),
    ]:
        raise Refusal("input role/length census mismatch")
    verified_shards = 0
    verified_bytes = 0
    for item in inputs:
        history_path = REPO / item["history_path"]
        if history_path.is_symlink() or not history_path.is_file() or sha256(history_path) != item["history_sha256"]:
            raise Refusal(f"history hash mismatch: {item['history_path']}")
        history = strict_json(history_path)
        if history.get("L") != item["length"] or history.get("lineage_authority") != "FULL_CANONICAL_MASK__NO_QUOTIENT_TRUNCATION_OR_SAMPLING":
            raise Refusal("history length or lineage authority mismatch")
        rows = canonical_shard_rows(history, item["terminal_shard_root"])
        if [row["q"] for row in rows] != list(range(item["length"])):
            raise Refusal("terminal shard q order/census mismatch")
        if len(rows) != item["terminal_shard_count"] or sum(row["bytes"] for row in rows) != item["terminal_shard_total_bytes"]:
            raise Refusal("terminal shard count/byte total mismatch")
        if shard_manifest_digest(rows) != item["terminal_shard_manifest_sha256"]:
            raise Refusal("terminal shard manifest digest mismatch")
        root = REPO / item["terminal_shard_root"]
        actual_names = sorted(path.name for path in root.iterdir() if path.is_file() or path.is_symlink())
        expected_names = sorted(Path(row["path"]).name for row in rows)
        if actual_names != expected_names:
            raise Refusal("terminal shard directory census mismatch")
        for row in rows:
            path = REPO / row["path"]
            if path.is_symlink() or not path.is_file() or path.stat().st_size != row["bytes"]:
                raise Refusal(f"terminal shard file/size mismatch: {row['path']}")
            if full_shard_hash and sha256(path) != row["sha256"]:
                raise Refusal(f"terminal shard hash mismatch: {row['path']}")
            verified_shards += 1
            verified_bytes += row["bytes"]

    validate_source_manifest()
    return {
        "classification": "PASS_HELDOUT_INPUT_AND_RESOURCE_GATE_PREOUTPUT",
        "full_shard_hashes_verified": full_shard_hash,
        "input_histories_verified": len(inputs),
        "schema": "OWNER_ONCE_HELDOUT_GATE_VALIDATION_V001",
        "terminal_shard_bytes_verified": verified_bytes,
        "terminal_shards_verified": verified_shards,
        "witness_values_computed_or_opened": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-shard-hash", action="store_true")
    parser.add_argument("--telemetry", type=Path)
    parser.add_argument("--now-epoch-seconds", type=int)
    args = parser.parse_args()
    try:
        result = validate_gate(full_shard_hash=args.full_shard_hash)
        if args.telemetry is not None:
            if args.now_epoch_seconds is None:
                raise Refusal("--now-epoch-seconds is required with --telemetry")
            gate = strict_json(GATE_PATH)
            telemetry = strict_json(args.telemetry)
            result["selected_schedule"] = validate_telemetry(
                telemetry, gate["resource_gate"], args.now_epoch_seconds
            )
            result["telemetry_validated"] = True
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    except Refusal as error:
        print(f"REFUSED: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
