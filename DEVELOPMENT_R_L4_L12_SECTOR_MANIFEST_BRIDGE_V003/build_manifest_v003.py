#!/usr/bin/env python3
"""Build the Stage-5 sector manifest from the exact V003 L12 audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREDECESSOR = (
    ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V001/"
    "build_sector_manifest.py"
)
FREEZE = HERE / "PRE_OUTPUT_FREEZE_V003.json"
TARGET_L12 = (
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/"
    "HISTORY_L12_PROCESS_PARALLEL_V003R1.json"
)
BLIND_L12 = (
    "AUDIT_R_L12_NUMERICAL_REPAIR_V003/"
    "NORMALIZED_BLIND_HISTORY_L12_V003R1.json"
)
AUDIT_L12 = (
    "AUDIT_R_L12_NUMERICAL_REPAIR_V003/EXACT_ADJUDICATION_V003R1.json"
)
OUTPUT = HERE / "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
TOKEN = "BUILD_AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003"


class BridgeRefusal(RuntimeError):
    pass


def load_predecessor():
    specification = importlib.util.spec_from_file_location(
        "frozen_sector_manifest_builder_v001_for_v003", PREDECESSOR
    )
    if specification is None or specification.loader is None:
        raise BridgeRefusal("cannot load frozen manifest builder")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            value.update(chunk)
    return value.hexdigest()


def verify_freeze(expected: str) -> None:
    if not FREEZE.is_file() or sha256_file(FREEZE) != expected:
        raise BridgeRefusal("V003 Stage-5 freeze SHA-256 mismatch")
    value = json.loads(FREEZE.read_text())
    if (
        value.get("schema") != "L4_L12_SECTOR_MANIFEST_BRIDGE_V003_PRE_OUTPUT_FREEZE"
        or value.get("status") != "FROZEN_BEFORE_V003_L12_HISTORY_OUTPUT"
        or value.get("v003_l12_history_present_at_freeze") is not False
        or value.get("files") != {
            "METHOD.md": sha256_file(HERE / "METHOD.md"),
            "build_manifest_v003.py": sha256_file(Path(__file__)),
            "predecessor": sha256_file(PREDECESSOR),
        }
        or value.get("thresholds_changed") is not False
    ):
        raise BridgeRefusal("V003 Stage-5 pre-output freeze mismatch")


def valid_number(value: object) -> bool:
    return type(value) in (int, float, Decimal) and math.isfinite(float(value))


def validate_v003_l12_audit(
    audit: dict[str, object], source: dict[str, str], builder: Any
) -> None:
    required_numbers = (
        "maximum_target_hostile_history_observable_difference",
        "maximum_target_blind_manifest_observable_difference",
        "maximum_target_hostile_sector_weight_difference",
        "maximum_target_hostile_terminal_amplitude_difference",
    )
    if (
        audit.get("schema") != "AUDIT_R_L12_COMPLETE_PREFIX_HISTORY_GATE_V001"
        or audit.get("classification")
        != "PASS_EXACT_L12_COMPLETE_PREFIX_HISTORY_GATE_V001"
        or type(audit.get("checks_total")) is not int
        or type(audit.get("checks_passed")) is not int
        or audit["checks_total"] <= 0
        or audit["checks_passed"] != audit["checks_total"]
        or audit.get("failures") != []
        or audit.get("tolerance") != 1e-8
        or audit.get("target_history_sha256") != source["target_sha256"]
        or audit.get("blind_history_sha256") != source["blind_sha256"]
        or not builder.valid_sha256(audit.get("hostile_history_sha256"))
        or any(not valid_number(audit.get(field)) for field in required_numbers)
        or any(float(audit[field]) > 1e-8 for field in required_numbers)
    ):
        raise builder.ManifestRefusal("L12 V003 exact audit identity/result mismatch")
    shards = audit.get("terminal_shards")
    if (
        type(shards) is not list
        or len(shards) != 12
        or [row.get("q") for row in shards if type(row) is dict] != list(range(12))
        or any(
            type(row) is not dict
            or row.get("shape") != [math.comb(11, q), math.comb(24, q)]
            or not builder.valid_sha256(row.get("target_sha256"))
            or not builder.valid_sha256(row.get("hostile_sha256"))
            or not valid_number(row.get("amplitude_linf"))
            or float(row["amplitude_linf"]) > 1e-8
            for q, row in enumerate(shards)
        )
    ):
        raise builder.ManifestRefusal("L12 V003 terminal audit census mismatch")


def build() -> tuple[dict[str, object], str]:
    builder = load_predecessor()
    original_sources = {length: dict(value)
                        for length, value in builder.CANONICAL_SOURCES.items()}
    original_validator = builder._validate_hostile_audit
    builder.CANONICAL_SOURCES[12] = {
        "target": TARGET_L12,
        "blind": BLIND_L12,
        "audit": AUDIT_L12,
    }

    def validator(audit: dict[str, object], length: int,
                  source: dict[str, str], repo_root: Path) -> None:
        if length != 12:
            original_validator(audit, length, source, repo_root)
            return
        validate_v003_l12_audit(audit, source, builder)

    builder._validate_hostile_audit = validator
    try:
        sources: dict[int, dict[str, str]] = {}
        for length in builder.SIZES:
            paths = builder.CANONICAL_SOURCES[length]
            sources[length] = {
                "target_path": paths["target"],
                "target_sha256": builder.sha256_file(ROOT / paths["target"]),
                "blind_path": paths["blind"],
                "blind_sha256": builder.sha256_file(ROOT / paths["blind"]),
                "audit_path": paths["audit"],
                "audit_sha256": builder.sha256_file(ROOT / paths["audit"]),
            }
        lineage = {
            label: {
                "path": binding["path"],
                "sha256": builder.sha256_file(ROOT / binding["path"]),
            }
            for label, binding in builder.STAGE2_LINEAGE_SOURCES.items()
        }
        manifest = builder.build_manifest(sources, lineage, ROOT)
        output_hash = builder.publish_once(OUTPUT, manifest)
        return manifest, output_hash
    finally:
        builder.CANONICAL_SOURCES.clear()
        builder.CANONICAL_SOURCES.update(original_sources)
        builder._validate_hostile_audit = original_validator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--freeze-sha256", required=True)
    arguments = parser.parse_args()
    if arguments.authorization != TOKEN:
        print("REFUSED: V003 manifest authorization token missing", file=sys.stderr)
        return 2
    if OUTPUT.exists():
        print("REFUSED: V003 manifest already exists", file=sys.stderr)
        return 2
    try:
        verify_freeze(arguments.freeze_sha256)
        manifest, output_hash = build()
    except (BridgeRefusal, OSError, ValueError, MemoryError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": manifest["status"],
        "sha256": output_hash,
        "sizes": list(range(4, 13, 2)),
        "atoms": len(manifest["atoms"]),
        "l12_audit": AUDIT_L12,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
