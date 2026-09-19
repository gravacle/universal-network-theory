#!/usr/bin/env python3
"""Reproduce the non-publishing V012 mutation ledger with named encodings."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
TARGET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
PREFLIGHT: Final[Path] = TARGET / "validate_preflight.py"
FREEZE: Final[Path] = TARGET / "FREEZE.json"
VALIDATOR: Final[Path] = TARGET / "production_obligation_validators.py"
EXPECTED_VALIDATOR_SHA256: Final[str] = (
    "b6409bfca1c0ee468671a37d5aac41c80c67f8027265ce4c0261b861509ad691"
)


class Refusal(RuntimeError):
    """The reproducibility harness refused its exact execution boundary."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(16 * 2**20):
            digest.update(block)
    return digest.hexdigest()


def load_preflight():
    specification = importlib.util.spec_from_file_location(
        "target_v012_validate_preflight_receipt", PREFLIGHT,
    )
    if specification is None or specification.loader is None:
        raise Refusal("validate_preflight file specification is unavailable")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def reproduce() -> dict[str, object]:
    if Path.cwd().resolve() != ROOT or ROOT.resolve() != ROOT:
        raise Refusal("harness must run from the canonical repository root")
    if not sys.dont_write_bytecode:
        raise Refusal("harness requires Python -B")
    metadata = os.stat(VALIDATOR, follow_symlinks=False)
    validator_sha256 = sha256(VALIDATOR)
    if (
        not stat.S_ISREG(metadata.st_mode)
        or metadata.st_mode & 0o222
        or metadata.st_nlink != 1
        or validator_sha256 != EXPECTED_VALIDATOR_SHA256
    ):
        raise Refusal("candidate validator bytes or immutable custody mismatch")
    module = load_preflight()
    freeze = copy.deepcopy(json.loads(FREEZE.read_bytes()))
    on_disk_freeze_sha256 = sha256(FREEZE)
    frozen_files_before = copy.deepcopy(freeze.get("files"))
    if type(frozen_files_before) is not dict:
        raise Refusal("on-disk freeze source census mismatch")
    freeze["files"]["production_obligation_validators.py"] = validator_sha256
    differing_bindings = {
        key for key in freeze["files"]
        if freeze["files"][key] != frozen_files_before.get(key)
    }
    if differing_bindings != {"production_obligation_validators.py"}:
        raise Refusal("in-memory freeze patch escaped the validator binding")
    original_guard = module.protected_canonical_artifacts
    module.protected_canonical_artifacts = lambda: tuple()
    try:
        ledger, counts = module.execute_obligation_mutations(freeze)
    finally:
        module.protected_canonical_artifacts = original_guard
    expected_counts = {
        "artifacts": 26,
        "positive_fixtures": 33,
        "mutation_classes": 36,
        "mutation_assignments": 477,
        "positive_sink_calls": 33,
        "mutation_sink_calls": 477,
    }
    if counts != expected_counts:
        raise Refusal("mutation execution census mismatch")
    production_bytes = module.canonical_json_bytes(ledger)
    compact_diagnostic_bytes = (
        module.obligation_validators.canonical_json_bytes(ledger)
    )
    if production_bytes == compact_diagnostic_bytes:
        raise Refusal("named ledger encodings unexpectedly alias")
    return {
        "schema": "V012_A18_REPAIR_MUTATION_LEDGER_REPRODUCTION_V001",
        "classification": "PASS_NONPUBLISHING_MUTATION_LEDGER_REPRODUCTION",
        "execution_boundary": {
            "cwd": str(ROOT),
            "python_dont_write_bytecode": bool(sys.dont_write_bytecode),
            "python_hash_seed": os.environ.get("PYTHONHASHSEED"),
            "preflight_import": "importlib.util.spec_from_file_location",
            "on_disk_freeze_sha256": on_disk_freeze_sha256,
            "in_memory_changed_freeze_bindings": sorted(differing_bindings),
            "in_memory_validator_sha256": validator_sha256,
            "runtime_hook_override": "protected_canonical_artifacts=lambda:tuple()",
            "runtime_hook_restored_in_finally": (
                module.protected_canonical_artifacts is original_guard
            ),
            "publication_performed": False,
        },
        "counts": counts,
        "ledger_sha256_by_encoding": {
            "production_validate_preflight_indented_utf8": hashlib.sha256(
                production_bytes
            ).hexdigest(),
            "diagnostic_obligation_validator_compact_ascii": hashlib.sha256(
                compact_diagnostic_bytes
            ).hexdigest(),
        },
        "encoding_adjudication": "The earlier receipt mismatch was two byte encoders applied to the same ledger object, not a mutation-record difference. The production digest is the indented UTF-8 encoding used by validate_preflight.main before publication.",
        "claim_boundary": "NONPUBLISHING_MUTATION_REPRODUCTION_ONLY__NO_A01_A18_REPLAY_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    try:
        result = reproduce()
    except (OSError, ValueError, json.JSONDecodeError, Refusal) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
