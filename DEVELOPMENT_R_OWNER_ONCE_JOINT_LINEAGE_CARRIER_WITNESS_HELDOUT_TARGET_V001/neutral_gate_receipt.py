#!/usr/bin/env python3
"""Issue the neutral, pre-output full-gate receipt for the held-out run.

This control-plane program hashes and authenticates all four retained inputs
through the independently frozen gate validator.  It never imports either
branch implementation and never interprets an amplitude or witness value.
The target and hostile branches consume the resulting receipt independently.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import time
from pathlib import Path
from types import ModuleType
from typing import Callable

import heldout_target_adapter as target


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RECEIPT_SCHEMA = "OWNER_ONCE_HELDOUT_NEUTRAL_FULL_GATE_RECEIPT_V001"
RECEIPT_CLASSIFICATION = "PASS_NEUTRAL_FULL_GATE_PREOUTPUT"
DEFAULT_RECEIPT = HERE / "CONTROL_PLANE_RECEIPTS/NEUTRAL_FULL_GATE_RECEIPT_V001.json"
CONTROL_TELEMETRY_PARENT = HERE / "CONTROL_PLANE_TELEMETRY"
CONTROL_RECEIPT_PARENT = HERE / "CONTROL_PLANE_RECEIPTS"


def _load_validator(root: Path) -> ModuleType:
    path = root / target.HELDOUT_GATE_VALIDATOR_RELATIVE_PATH
    spec = importlib.util.spec_from_file_location("neutral_heldout_gate_validator", path)
    if spec is None or spec.loader is None:
        raise target.HeldoutRefusal("cannot import frozen neutral gate validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _safe_absent_path(raw: object, root: Path, label: str) -> Path:
    if not isinstance(raw, str) or not raw:
        raise target.HeldoutRefusal(f"invalid {label} path")
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise target.HeldoutRefusal(f"unsafe {label} path")
    absolute = root / path
    target.require_no_symlink_chain(absolute, root)
    if absolute.exists() or absolute.is_symlink():
        raise target.HeldoutRefusal(f"pre-existing {label} refused")
    return absolute.resolve(strict=False)


def issue_receipt(
    *,
    telemetry_path: Path,
    output_path: Path,
    authorization: str | None,
    root: Path = ROOT,
    now: Callable[[], float] = time.time,
    gate_validator: Callable[[bool], dict[str, object]] | None = None,
) -> dict[str, object]:
    target.require_execution_authorization(authorization)
    target.require_no_symlink_chain(telemetry_path, root)
    if telemetry_path.resolve(strict=False).parent != CONTROL_TELEMETRY_PARENT.resolve(
        strict=False
    ):
        raise target.HeldoutRefusal("telemetry is outside the frozen control root")
    target.require_no_symlink_chain(output_path, root)
    if output_path.resolve(strict=False).parent != CONTROL_RECEIPT_PARENT.resolve(
        strict=False
    ):
        raise target.HeldoutRefusal("receipt is outside the frozen control root")
    protocol = target.authenticate_heldout_protocol(root)
    gate = target.strict_json(
        root / target.HELDOUT_GATE_RELATIVE_PATH,
        target.HELDOUT_GATE_SHA256,
    )
    validator = _load_validator(root)
    validator_fn = gate_validator or validator.validate_gate
    validated = validator_fn(True)
    if validated != {
        "classification": "PASS_HELDOUT_INPUT_AND_RESOURCE_GATE_PREOUTPUT",
        "full_shard_hashes_verified": True,
        "input_histories_verified": 4,
        "schema": "OWNER_ONCE_HELDOUT_GATE_VALIDATION_V001",
        "terminal_shard_bytes_verified": 13_671_711_776,
        "terminal_shards_verified": 44,
        "witness_values_computed_or_opened": False,
    }:
        raise target.HeldoutRefusal("neutral full-gate validation record mismatch")

    issued = int(now())
    telemetry = target.strict_json(telemetry_path)
    try:
        schedule = validator.validate_telemetry(
            telemetry, gate["resource_gate"], issued
        )
    except Exception as error:
        raise target.HeldoutRefusal(f"neutral telemetry validation failed: {error}") from error

    resolved_paths = [
        _safe_absent_path(telemetry[name], root, name)
        for name in (
            "target_scratch_root",
            "hostile_scratch_root",
            "target_output_path",
            "hostile_output_path",
        )
    ]
    if len(set(resolved_paths)) != 4:
        raise target.HeldoutRefusal("neutral scratch/output paths alias")

    target.require_no_symlink_chain(output_path.parent, root)
    if output_path.exists() or output_path.is_symlink():
        raise target.HeldoutRefusal("neutral receipt already exists")
    output_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    target.require_no_symlink_chain(output_path.parent, root)
    if output_path.resolve(strict=False) in resolved_paths:
        raise target.HeldoutRefusal("neutral receipt aliases branch scratch/output")

    receipt = {
        "classification": RECEIPT_CLASSIFICATION,
        "concurrent_release_deadline_epoch_seconds": (
            issued + int(gate["resource_gate"]["maximum_release_skew_seconds"])
            if schedule == "CONCURRENT_TARGET_AND_HOSTILE"
            else None
        ),
        "expires_epoch_seconds": issued + int(gate["resource_gate"]["telemetry_max_age_seconds"]),
        "full_gate_validation": validated,
        "gate_input_census_sha256": target.canonical_digest(gate["inputs"]),
        "gate_resource_sha256": target.canonical_digest(gate["resource_gate"]),
        "gate_sha256": target.HELDOUT_GATE_SHA256,
        "gate_validator_sha256": target.HELDOUT_GATE_VALIDATOR_SHA256,
        "issued_epoch_seconds": issued,
        "maximum_release_skew_seconds": int(
            gate["resource_gate"]["maximum_release_skew_seconds"]
        ),
        "protocol_sha256": protocol["sha256"],
        "schema": RECEIPT_SCHEMA,
        "selected_schedule": schedule,
        "telemetry_sha256": target.sha256_file(telemetry_path),
        "witness_values_computed_or_opened": False,
    }
    raw = target.canonical_json_bytes(receipt)
    temporary = output_path.parent / f".{output_path.name}.{os.getpid()}.tmp"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
        0o400,
    )
    try:
        written = 0
        while written < len(raw):
            count = os.write(descriptor, raw[written:])
            if count <= 0:
                raise target.HeldoutRefusal("short neutral receipt write")
            written += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    if output_path.exists() or output_path.is_symlink():
        raise target.HeldoutRefusal("neutral receipt destination appeared during write")
    os.replace(temporary, output_path)
    parent_descriptor = os.open(output_path.parent, os.O_RDONLY)
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)
    if target.sha256_file(output_path, require_readonly=True) != hashlib.sha256(raw).hexdigest():
        raise target.HeldoutRefusal("neutral receipt seal verification failed")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--telemetry", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--authorization", required=True)
    args = parser.parse_args()
    try:
        issue_receipt(
            telemetry_path=args.telemetry,
            output_path=args.output,
            authorization=args.authorization,
        )
        print("PASS_NEUTRAL_FULL_GATE_PREOUTPUT")
        return 0
    except target.HeldoutRefusal as error:
        print(f"REFUSED: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
