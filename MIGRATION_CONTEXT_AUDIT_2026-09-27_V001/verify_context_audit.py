#!/usr/bin/env python3
"""Fail-closed verifier for the UNT migration/context audit V001."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
INVENTORY = PACKET / "INVENTORY.json"
LEDGER = PACKET / "CLAIM_LEDGER.tsv"
VALIDATION = PACKET / "CURRENT_MACHINE_VALIDATION_2026-09-27.json"

EXPECTED_SCHEMA = "UNT_MIGRATION_CONTEXT_AUDIT_V001"
EXPECTED_HEAD = "f5973628fa25c8cc0e2812142e6d8516d0b5d28d"
EXPECTED_TREE = "be83f661a6e806c61a6291be315bf78b08bbc006"
EXPECTED_BRANCH = "integration/post-gate-a-20260915"
ALLOWED_CATEGORIES = {
    "definition",
    "assumption",
    "construction",
    "analytic theorem",
    "exact finite computation",
    "conditional consequence",
    "empirical comparison",
    "open",
}
REQUIRED_CLAIMS = {f"MCA-{index:03d}" for index in range(1, 27)}
EXPECTED_TOP_KEYS = {
    "schema",
    "audit_date",
    "status",
    "authoritative_source",
    "source_inventory",
    "development_clone",
    "custody_classes",
    "source_files",
    "external_inputs",
    "paused_workstreams",
    "release_reconciliation",
}


def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    with INVENTORY.open("r", encoding="utf-8") as stream:
        inventory = json.load(
            stream,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )

    require(set(inventory) == EXPECTED_TOP_KEYS, "inventory top-level key census")
    require(inventory["schema"] == EXPECTED_SCHEMA, "inventory schema")
    source = inventory["authoritative_source"]
    require(source["head"] == EXPECTED_HEAD, "recorded HEAD")
    require(source["tree"] == EXPECTED_TREE, "recorded tree")
    require(source["branch"] == EXPECTED_BRANCH, "recorded branch")
    require(git("rev-parse", "HEAD") == EXPECTED_HEAD, "live clone HEAD")
    require(git("rev-parse", "HEAD^{tree}") == EXPECTED_TREE, "live clone tree")
    require(git("branch", "--show-current") == EXPECTED_BRANCH, "live clone branch")

    seen_paths: set[str] = set()
    for record in inventory["source_files"]:
        require(set(record) == {"path", "sha256", "custody"}, "source record keys")
        relative = record["path"]
        require(relative not in seen_paths, f"duplicate source path: {relative}")
        seen_paths.add(relative)
        require(isinstance(relative, str) and not relative.startswith("/"), "relative source path")
        candidate = (ROOT / relative).resolve()
        require(candidate.is_relative_to(ROOT.resolve()), f"source escaped root: {relative}")
        require(candidate.is_file(), f"missing source: {relative}")
        require(sha256(candidate) == record["sha256"], f"source hash: {relative}")
        require(record["custody"] in inventory["custody_classes"], f"custody: {relative}")

    with LEDGER.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    require(
        rows and set(rows[0]) == {
            "claim_id",
            "category",
            "status",
            "statement",
            "evidence_path",
            "evidence_sha256",
            "ceiling",
        },
        "claim ledger columns",
    )
    ids = {row["claim_id"] for row in rows}
    require(ids == REQUIRED_CLAIMS, "claim id census")
    require(len(ids) == len(rows), "unique claim ids")
    require({row["category"] for row in rows} <= ALLOWED_CATEGORIES, "claim categories")
    for row in rows:
        require(all(row.values()), f"blank claim field: {row['claim_id']}")
        if row["evidence_sha256"] == "SELF":
            require(row["evidence_path"] == str(PACKET.relative_to(ROOT) / "INVENTORY.json"), "SELF evidence path")
        else:
            require(row["evidence_path"] in seen_paths, f"unregistered evidence: {row['claim_id']}")
            matching = next(item for item in inventory["source_files"] if item["path"] == row["evidence_path"])
            require(matching["sha256"] == row["evidence_sha256"], f"claim evidence hash: {row['claim_id']}")

    with VALIDATION.open("r", encoding="utf-8") as stream:
        validation = json.load(
            stream,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    require(validation["schema"] == "UNT_CURRENT_MACHINE_VALIDATION_RECORD_V001", "validation schema")
    authoritative = validation["authoritative_checkout_run"]
    require(authoritative["head"] == EXPECTED_HEAD, "validation HEAD")
    require(authoritative["exit_code"] == 1, "fail-closed validation exit")
    require(
        authoritative["overall"] == "FAIL_MISSING_TWO_ZERO_WEIGHT_HISTORICAL_FIXTURE_FAMILIES",
        "validation classification",
    )
    require(len(authoritative["failed_zero_weight_fixture_families"]) == 2, "fixture-family census")
    require(validation["fixture_policy"] == {
        "invent_replacements": False,
        "scientific_promotion_from_failed_aggregate": False,
        "preserve_fail_closed_exit": True,
    }, "fixture policy")

    print(
        f"PASS {EXPECTED_SCHEMA}: {len(seen_paths)} source hashes, "
        f"{len(rows)} typed claims, current-machine validation boundary"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL {EXPECTED_SCHEMA}: {error}", file=sys.stderr)
        raise SystemExit(1)
