#!/usr/bin/env python3
"""Versioned Decimal interface repair around the frozen V003 Stage-5 bridge."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V003_BRIDGE = ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/build_manifest_v003.py"
V003_FREEZE = ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003/PRE_OUTPUT_FREEZE_V003.json"
FREEZE = HERE / "PRE_OUTPUT_FREEZE_STAGE5R1.json"
EXECUTION_RECORD = HERE / "STAGE5R1_EXECUTION_RECORD.json"


class Stage5R1Refusal(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise Stage5R1Refusal(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            value.update(chunk)
    return value.hexdigest()


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    demand(specification is not None and specification.loader is not None,
           f"cannot load {name}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def verify_freeze(expected: str) -> dict[str, Any]:
    demand(FREEZE.is_file() and sha256(FREEZE) == expected,
           "Stage5R1 freeze SHA-256 mismatch")
    value = json.loads(FREEZE.read_text())
    demand(value.get("schema") == "L12_V003R1_STAGE5R1_PRE_OUTPUT_FREEZE_V001",
           "Stage5R1 freeze schema")
    demand(value.get("status") == "FROZEN_AFTER_STAGE4R1_BEFORE_STAGE5R1_OUTPUT",
           "Stage5R1 freeze status")
    demand(value.get("stage5r1_outputs_present_at_freeze") is False,
           "Stage5R1 pre-output declaration")
    demand(value.get("physics_changed") is False
           and value.get("numerical_data_changed") is False
           and value.get("predicate_thresholds_changed") is False,
           "Stage5R1 prohibited mutation declaration")
    demand(value.get("representation_projection") == {
        "source_type": "Decimal",
        "required_exact_value": "1E-8",
        "validator_interface_type": "float",
        "on_disk_audit_changed": False,
    }, "Stage5R1 representation declaration")
    files = value.get("files")
    demand(isinstance(files, dict) and files, "Stage5R1 file census")
    for relative, expected_hash in files.items():
        path = (ROOT / relative).resolve()
        demand(path.is_relative_to(ROOT.resolve()) and path.is_file(),
               f"Stage5R1 frozen file missing: {relative}")
        demand(sha256(path) == expected_hash,
               f"Stage5R1 frozen file changed: {relative}")
    demand(files.get(str(Path(__file__).resolve().relative_to(ROOT))) == sha256(Path(__file__)),
           "Stage5R1 builder custody")
    return value


def project_decimal_tolerance(
    audit: dict[str, object],
    source: dict[str, str],
    builder: Any,
    original_validator: Any,
) -> None:
    tolerance = audit.get("tolerance")
    demand(type(tolerance) is Decimal,
           "Stage5R1 tolerance was not parsed as Decimal")
    demand(tolerance == Decimal("1e-8"),
           "Stage5R1 exact tolerance changed")
    projected = dict(audit)
    projected["tolerance"] = 1e-8
    original_validator(projected, source, builder)


def write_new_atomic(path: Path, value: object) -> None:
    demand(not path.exists(), f"refusing overwrite: {path}")
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    try:
        with temporary.open("x") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def run(arguments: argparse.Namespace) -> None:
    freeze = verify_freeze(arguments.stage5r1_freeze_sha256)
    bridge = load_module(V003_BRIDGE, "frozen_v003_stage5_for_stage5r1")
    demand(arguments.authorization == bridge.TOKEN,
           "Stage5R1 authorization token")
    demand(arguments.v003_freeze_sha256 == sha256(V003_FREEZE),
           "Stage5R1 frozen V003 freeze binding")
    bridge.verify_freeze(arguments.v003_freeze_sha256)
    demand(not bridge.OUTPUT.exists() and not EXECUTION_RECORD.exists(),
           "Stage5R1 output allocation is not fresh")

    original_validator = bridge.validate_v003_l12_audit

    def validator(audit: dict[str, object], source: dict[str, str],
                  builder: Any) -> None:
        project_decimal_tolerance(audit, source, builder, original_validator)

    bridge.validate_v003_l12_audit = validator
    try:
        manifest, output_hash = bridge.build()
    finally:
        bridge.validate_v003_l12_audit = original_validator
    demand(bridge.OUTPUT.is_file() and sha256(bridge.OUTPUT) == output_hash,
           "Stage5R1 manifest publication")
    write_new_atomic(EXECUTION_RECORD, {
        "schema": "L12_V003R1_STAGE5R1_EXECUTION_RECORD_V001",
        "status": "PASS_AUTHENTICATED_STAGE5_MANIFEST",
        "builder_sha256": sha256(Path(__file__)),
        "freeze_sha256": sha256(FREEZE),
        "frozen_v003_bridge_sha256": sha256(V003_BRIDGE),
        "frozen_v003_freeze_sha256": sha256(V003_FREEZE),
        "stage4_exact_adjudication_sha256": freeze["stage4_exact_adjudication_sha256"],
        "stage4_normalized_blind_history_sha256": freeze["stage4_normalized_blind_history_sha256"],
        "manifest": str(bridge.OUTPUT.relative_to(ROOT)),
        "manifest_sha256": output_hash,
        "manifest_status": manifest.get("status"),
        "manifest_sector_count": len(manifest.get("atoms", [])),
        "representation_projection_only": True,
        "physics_changed": False,
        "numerical_data_changed": False,
        "predicate_thresholds_changed": False,
        "stage6_started": False,
        "stage7_started": False,
    })
    print(json.dumps({
        "status": manifest.get("status"),
        "sha256": output_hash,
        "sizes": list(range(4, 13, 2)),
        "atoms": len(manifest.get("atoms", [])),
        "stage5r1": True,
    }, sort_keys=True), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage5r1-freeze-sha256", required=True)
    parser.add_argument("--v003-freeze-sha256", required=True)
    parser.add_argument("--authorization", required=True)
    try:
        run(parser.parse_args())
    except (Exception, KeyboardInterrupt) as error:
        print(f"STAGE5R1_REFUSED {type(error).__name__}:{error}",
              file=sys.stderr, flush=True)
        return 2
    print("STAGE5R1_COMPLETE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
