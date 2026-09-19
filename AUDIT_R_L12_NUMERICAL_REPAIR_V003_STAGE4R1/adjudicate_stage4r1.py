#!/usr/bin/env python3
"""Versioned schema-projection repair around the frozen V003 Stage-4 audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V003_PATH = ROOT / "AUDIT_R_L12_NUMERICAL_REPAIR_V003/adjudicate_v003.py"
V003_FREEZE = ROOT / "AUDIT_R_L12_NUMERICAL_REPAIR_V003/PRE_OUTPUT_FREEZE_V003.json"
FREEZE = HERE / "PRE_OUTPUT_FREEZE_STAGE4R1.json"
TARGET_HISTORY = (
    ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/"
    "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
HOSTILE_HISTORY = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS/"
    "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)


class Stage4R1Refusal(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise Stage4R1Refusal(message)


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
           "Stage4R1 freeze SHA-256 mismatch")
    value = json.loads(FREEZE.read_text())
    demand(value.get("schema") == "L12_V003R1_STAGE4R1_PRE_OUTPUT_FREEZE_V001",
           "Stage4R1 freeze schema")
    demand(value.get("status") == "FROZEN_AFTER_V003R1_HISTORIES_BEFORE_STAGE4R1_OUTPUT",
           "Stage4R1 freeze status")
    demand(value.get("stage4r1_outputs_present_at_freeze") is False,
           "Stage4R1 pre-output declaration")
    demand(value.get("physics_changed") is False
           and value.get("numerical_data_changed") is False
           and value.get("predicate_thresholds_changed") is False,
           "Stage4R1 prohibited mutation declaration")
    demand(value.get("schema_projection_change") == {
        "field_removed_before_predecessor_normalization": "dimension",
        "authenticated_alias_retained": "full_dimension",
        "manifest_adapter_required_absent": True,
    }, "Stage4R1 schema projection declaration")
    files = value.get("files")
    demand(isinstance(files, dict) and files, "Stage4R1 file census")
    for relative, expected_hash in files.items():
        path = (ROOT / relative).resolve()
        demand(path.is_relative_to(ROOT.resolve()) and path.is_file(),
               f"Stage4R1 frozen file missing: {relative}")
        demand(sha256(path) == expected_hash,
               f"Stage4R1 frozen file changed: {relative}")
    demand(files.get(str(Path(__file__).resolve().relative_to(ROOT))) == sha256(Path(__file__)),
           "Stage4R1 adapter custody")
    demand(value.get("target_history_sha256") == sha256(TARGET_HISTORY),
           "Stage4R1 target history custody")
    demand(value.get("hostile_history_sha256") == sha256(HOSTILE_HISTORY),
           "Stage4R1 hostile history custody")
    return value


def remove_redundant_dimension(projected: dict[str, Any]) -> dict[str, Any]:
    demand("manifest_adapter" not in projected,
           "Stage4R1 projected manifest_adapter must be absent")
    dimension = projected.get("dimension")
    demand(type(dimension) is int, "Stage4R1 projected dimension")
    demand(projected.get("full_dimension") == dimension,
           "Stage4R1 dimension/full_dimension identity")
    value = dict(projected)
    del value["dimension"]
    demand("dimension" not in value and value.get("full_dimension") == dimension,
           "Stage4R1 dimension projection")
    return value


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
    freeze = verify_freeze(arguments.stage4r1_freeze_sha256)
    demand(arguments.target.resolve() == TARGET_HISTORY.resolve()
           and arguments.target_sha256 == freeze["target_history_sha256"],
           "Stage4R1 target argument binding")
    demand(arguments.hostile.resolve() == HOSTILE_HISTORY.resolve()
           and arguments.hostile_sha256 == freeze["hostile_history_sha256"],
           "Stage4R1 hostile argument binding")
    demand(not arguments.blind_output.exists()
           and not arguments.output.exists()
           and not arguments.execution_record.exists(),
           "Stage4R1 output allocation is not fresh")

    v003 = load_module(V003_PATH, "frozen_v003_stage4_for_stage4r1")
    frozen_base = v003.load_base()
    v003.verify_freeze(sha256(V003_FREEZE), frozen_base)
    original_project_hostile = v003.project_hostile

    def project_hostile(source: dict[str, Any], base: Any,
                        original_freeze: dict[str, Any]) -> dict[str, Any]:
        return remove_redundant_dimension(
            original_project_hostile(source, base, original_freeze)
        )

    v003.project_hostile = project_hostile
    try:
        v003.run(argparse.Namespace(
            target=arguments.target,
            target_sha256=arguments.target_sha256,
            hostile=arguments.hostile,
            hostile_sha256=arguments.hostile_sha256,
            target_terminal_root=arguments.target_terminal_root,
            hostile_terminal_root=arguments.hostile_terminal_root,
            freeze_sha256=sha256(V003_FREEZE),
            blind_output=arguments.blind_output,
            output=arguments.output,
        ))
    finally:
        v003.project_hostile = original_project_hostile

    demand(arguments.blind_output.is_file() and arguments.output.is_file(),
           "Stage4R1 adjudication outputs absent")
    result = json.loads(arguments.output.read_text())
    demand(result.get("failures") == []
           and result.get("checks_passed") == result.get("checks_total")
           and result.get("classification") == "PASS_EXACT_L12_COMPLETE_PREFIX_HISTORY_GATE_V001",
           "Stage4R1 exact adjudication did not pass")
    write_new_atomic(arguments.execution_record, {
        "schema": "L12_V003R1_STAGE4R1_EXECUTION_RECORD_V001",
        "status": "PASS_EXACT_STAGE4_ADJUDICATION",
        "adapter_sha256": sha256(Path(__file__)),
        "freeze_sha256": sha256(FREEZE),
        "frozen_v003_adapter_sha256": sha256(V003_PATH),
        "frozen_v003_freeze_sha256": sha256(V003_FREEZE),
        "target_history_sha256": sha256(arguments.target),
        "hostile_history_sha256": sha256(arguments.hostile),
        "normalized_blind_history": str(arguments.blind_output.relative_to(ROOT)),
        "normalized_blind_history_sha256": sha256(arguments.blind_output),
        "exact_adjudication": str(arguments.output.relative_to(ROOT)),
        "exact_adjudication_sha256": sha256(arguments.output),
        "checks_total": result["checks_total"],
        "checks_passed": result["checks_passed"],
        "failures": result["failures"],
        "schema_projection_only": True,
        "physics_changed": False,
        "numerical_data_changed": False,
        "predicate_thresholds_changed": False,
        "stage5_started": False,
        "stage6_started": False,
        "stage7_started": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage4r1-freeze-sha256", required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--target-sha256", required=True)
    parser.add_argument("--hostile", type=Path, required=True)
    parser.add_argument("--hostile-sha256", required=True)
    parser.add_argument("--target-terminal-root", type=Path, required=True)
    parser.add_argument("--hostile-terminal-root", type=Path, required=True)
    parser.add_argument("--blind-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execution-record", type=Path, required=True)
    try:
        run(parser.parse_args())
    except (Exception, KeyboardInterrupt) as error:
        print(f"STAGE4R1_REFUSED {type(error).__name__}:{error}",
              file=sys.stderr, flush=True)
        return 2
    print("STAGE4R1_COMPLETE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
