#!/usr/bin/env python3
"""Fail-closed verifier for the target scaling packet V001."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import target_lineage_scaling as target
import resume_equivalence as resume


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
SOURCE_HASHES = PACKET / "SOURCE_HASHES.sha256"
RESULT_MANIFEST = PACKET / "RESULT_MANIFEST.json"
RESUME_MANIFEST = PACKET / "RESUME_EQUIVALENCE_MANIFEST.json"
EXPECTED_SOURCE_FILES = {
    "README.md",
    "ATTEMPT_LOG.md",
    "EXECUTION_PLAN.md",
    "PROTOCOL.md",
    "FREEZE.json",
    "SOURCE_INVENTORY.json",
    "target_lineage_scaling.py",
    "resume_equivalence.py",
    "test_target_lineage_scaling.py",
    "verify_packet.py",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(
            stream,
            object_pairs_hook=strict_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"nonfinite JSON constant: {value}")
            ),
        )


def verify_sources() -> None:
    require(SOURCE_HASHES.is_file(), "missing SOURCE_HASHES.sha256")
    records: dict[str, str] = {}
    for line in SOURCE_HASHES.read_text(encoding="utf-8").splitlines():
        digest, separator, relative = line.partition("  ")
        require(separator == "  " and len(digest) == 64, "malformed source hash line")
        require(relative not in records, f"duplicate source hash: {relative}")
        records[relative] = digest
    require(set(records) == EXPECTED_SOURCE_FILES, "source file census")
    for relative, expected in records.items():
        path = PACKET / relative
        require(path.is_file(), f"missing source file: {relative}")
        require(sha256(path) == expected, f"source hash mismatch: {relative}")


def verify_inventory() -> None:
    inventory = load_json(PACKET / "SOURCE_INVENTORY.json")
    require(
        set(inventory)
        == {
            "schema",
            "status",
            "repository_head",
            "packet_sources",
            "dependency_sources",
            "ignored_inputs",
            "claim_boundary",
        },
        "source inventory key census",
    )
    require(set(inventory["packet_sources"]) == EXPECTED_SOURCE_FILES, "inventory packet census")
    dependencies = {record["path"]: record["sha256"] for record in inventory["dependency_sources"]}
    for relative, expected in target.DEPENDENCY_HASHES.items():
        require(dependencies.get(relative) == expected, f"inventory dependency: {relative}")
    for length, expected in target.HISTORY_HASHES.items():
        relative = target.history_relative(length).as_posix()
        require(dependencies.get(relative) == expected, f"inventory history: L{length}")


def verify_result() -> None:
    require(RESULT_MANIFEST.is_file(), "missing RESULT_MANIFEST.json")
    manifest = load_json(RESULT_MANIFEST)
    require(
        set(manifest)
        == {
            "schema",
            "classification",
            "result_path",
            "result_sha256",
            "result_bytes",
            "checkpoint_complete_path",
            "checkpoint_complete_sha256",
            "claim_boundary",
        },
        "result manifest key census",
    )
    result_path = PACKET / manifest["result_path"]
    complete_path = PACKET / manifest["checkpoint_complete_path"]
    require(result_path.is_file(), "missing L4 result")
    require(sha256(result_path) == manifest["result_sha256"], "L4 result hash")
    require(result_path.stat().st_size == manifest["result_bytes"], "L4 result bytes")
    require(complete_path.is_file(), "missing checkpoint COMPLETE")
    require(sha256(complete_path) == manifest["checkpoint_complete_sha256"], "checkpoint COMPLETE hash")
    result = target.verify_l4_output(result_path)
    complete = load_json(complete_path)
    require(complete["schema"] == "L14_RESUMABLE_RUN_COMPLETE_V002", "checkpoint complete schema")
    require(complete["completed_tasks"] == complete["total_tasks"] == 5, "checkpoint task census")
    require(len(complete["result_files"]) == 5, "checkpoint result-file census")
    for record in complete["result_files"]:
        task_path = complete_path.parent / "results" / f"{record['task_id']}.json"
        require(task_path.is_file(), f"missing checkpoint task: {record['task_id']}")
        require(sha256(task_path) == record["sha256"], f"checkpoint task hash: {record['task_id']}")
    require(result["controls"]["passed"] is True, "L4 final controls")


def verify_resume_gate() -> None:
    require(RESUME_MANIFEST.is_file(), "missing RESUME_EQUIVALENCE_MANIFEST.json")
    manifest = load_json(RESUME_MANIFEST)
    require(
        set(manifest)
        == {
            "schema",
            "classification",
            "result_path",
            "result_sha256",
            "result_bytes",
            "control_result_path",
            "control_result_sha256",
            "resumed_result_path",
            "resumed_result_sha256",
            "control_complete_path",
            "control_complete_sha256",
            "resumed_complete_path",
            "resumed_complete_sha256",
            "canonical_final_sha256",
            "harness_sha256",
            "claim_boundary",
        },
        "resume manifest key census",
    )
    paths = {
        "result": PACKET / manifest["result_path"],
        "control_result": PACKET / manifest["control_result_path"],
        "resumed_result": PACKET / manifest["resumed_result_path"],
        "control_complete": PACKET / manifest["control_complete_path"],
        "resumed_complete": PACKET / manifest["resumed_complete_path"],
    }
    for label, path in paths.items():
        require(path.is_file(), f"missing resume evidence: {label}")
        require(sha256(path) == manifest[f"{label}_sha256"], f"resume evidence hash: {label}")
    require(paths["result"].stat().st_size == manifest["result_bytes"], "resume result bytes")
    require(sha256(PACKET / "resume_equivalence.py") == manifest["harness_sha256"], "resume harness hash")
    result = load_json(paths["result"])
    require(
        set(result)
        == {
            "schema",
            "classification",
            "source_binding",
            "interruption",
            "equivalence",
            "refusals",
            "orphan_temp",
            "resource",
            "logs",
            "claim_boundary",
        },
        "resume result key census",
    )
    require(result["classification"] == "PASS_L4_TARGET_SIGTERM_RESUME_EQUIVALENCE", "resume classification")
    interruption = result["interruption"]
    require(interruption["committed_before_signal"] >= 2, "pre-SIGTERM commit floor")
    require(2 <= interruption["committed_after_graceful_stop"] < 5, "partial stop census")
    require(interruption["interrupted_returncode"] == 75, "interrupted return code")
    require(interruption["premature_final_output"] is False, "premature final output")
    require(interruption["premature_complete_marker"] is False, "premature COMPLETE")
    require(interruption["explicit_resume_flag"] is True, "explicit resume")
    equivalence = result["equivalence"]
    require(equivalence["all_sector_hashes_equal"] is True, "sector equivalence flag")
    require(equivalence["final_hash_equal"] is True, "final equivalence flag")
    require(
        equivalence["control_final_canonical_sha256"]
        == equivalence["resumed_final_canonical_sha256"]
        == manifest["canonical_final_sha256"],
        "recorded canonical final hash",
    )
    control_final = resume.canonical_hash(resume.canonical_final_payload(paths["control_result"]))
    resumed_final = resume.canonical_hash(resume.canonical_final_payload(paths["resumed_result"]))
    require(control_final == resumed_final == manifest["canonical_final_sha256"], "recomputed final equivalence")
    control_sectors = resume.sector_hashes(paths["control_complete"].parent)
    resumed_sectors = resume.sector_hashes(paths["resumed_complete"].parent)
    require(control_sectors == resumed_sectors == equivalence["sector_canonical_sha256"], "recomputed sector equivalence")
    require(len(control_sectors) == 5, "resume sector census")
    require(
        {record["label"] for record in result["refusals"]}
        == {
            "changed_config",
            "changed_input",
            "changed_source",
            "changed_task_plan",
            "truncated_checkpoint",
            "corrupt_checkpoint",
        },
        "resume refusal census",
    )
    orphan = paths["result"].parent / result["orphan_temp"]["relative_path"]
    require(orphan.is_file(), "missing orphan-temp fixture")
    require(sha256(orphan) == result["orphan_temp"]["sha256"], "orphan-temp hash")
    require(result["orphan_temp"]["ignored_without_mutation"] is True, "orphan-temp disposition")


def main() -> int:
    verify_sources()
    verify_inventory()
    authenticated = target.authenticate_all_inputs()
    require(sum(len(row["shards"]) for row in authenticated["histories"].values()) == 18, "shard census")
    for length in (6, 8):
        try:
            target.validate_execution_length(length)
        except target.ScalingError:
            pass
        else:
            raise AssertionError(f"L{length} execution was not locked")
    verify_result()
    verify_resume_gate()
    print("PASS L4_L8_TARGET_SCALING_PACKET_V001: 10 sources, 18 shards, L4 result+resume, L6/L8 locked")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, TypeError, ValueError, target.ScalingError) as error:
        print(f"FAIL L4_L8_TARGET_SCALING_PACKET_V001: {error}", file=sys.stderr)
        raise SystemExit(1)
