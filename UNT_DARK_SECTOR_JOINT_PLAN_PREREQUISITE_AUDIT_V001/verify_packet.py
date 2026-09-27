#!/usr/bin/env python3
"""Verify source custody and gate/type census for the dark-sector audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
FREEZE = PACKET / "SOURCE_FREEZE.json"
MATRIX = PACKET / "PREREQUISITE_MATRIX.tsv"
LEDGER = PACKET / "CLAIM_LEDGER.tsv"
SCHEMA = "UNT_DARK_SECTOR_JOINT_PLAN_PREREQUISITE_AUDIT_V001"
EXPECTED_HEAD = "f5973628fa25c8cc0e2812142e6d8516d0b5d28d"
EXPECTED_TREE = "be83f661a6e806c61a6291be315bf78b08bbc006"
ALLOWED_CATEGORIES = {
    "definition", "assumption", "construction", "analytic theorem",
    "exact finite computation", "conditional consequence",
    "empirical comparison", "open",
}


def pairs_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant {value}")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    with FREEZE.open("r", encoding="utf-8") as stream:
        freeze = json.load(stream, object_pairs_hook=pairs_no_duplicates, parse_constant=reject_constant)
    require(freeze["schema"] == SCHEMA, "schema")
    require(freeze["status"] == "PREREQUISITES_FAIL__NO_COSMOLOGY_EXECUTION", "status")
    require(git("rev-parse", "HEAD") == EXPECTED_HEAD, "HEAD")
    require(git("rev-parse", "HEAD^{tree}") == EXPECTED_TREE, "tree")

    registered: dict[str, str] = {}
    for item in freeze["repository_sources"]:
        require(set(item) == {"path", "sha256", "git_blob", "role"}, f"source keys {item}")
        path = ROOT / item["path"]
        require(path.is_file() and not path.is_symlink(), f"source file {item['path']}")
        require(digest(path) == item["sha256"], f"source hash {item['path']}")
        require(git("rev-parse", f"HEAD:{item['path']}") == item["git_blob"], f"blob {item['path']}")
        registered[item["path"]] = item["sha256"]

    plan = freeze["external_plan"]
    plan_path = Path(plan["observed_path"])
    require(plan_path.is_file() and not plan_path.is_symlink(), "external plan present")
    raw = plan_path.read_bytes()
    require(len(raw) == plan["bytes"], "external plan bytes")
    require(len(raw.splitlines()) == plan["lines"], "external plan lines")
    require(hashlib.sha256(raw).hexdigest() == plan["sha256"], "external plan hash")

    matrix = read_tsv(MATRIX)
    require(len(matrix) == 14, "prerequisite row census")
    require({row["gate_id"] for row in matrix} == {f"DSP-G{i:02d}" for i in range(1, 15)}, "gate ids")
    require(not any(row["status"] == "PASS" for row in matrix), "no scientific prerequisite may pass")

    claims = read_tsv(LEDGER)
    require(len(claims) == 11, "claim row census")
    require({row["claim_id"] for row in claims} == {f"DSP-C{i:02d}" for i in range(1, 12)}, "claim ids")
    require({row["category"] for row in claims} <= ALLOWED_CATEGORIES, "claim category vocabulary")
    for row in claims:
        require(all(row.values()), f"blank claim field {row['claim_id']}")
        evidence = row["evidence_path"]
        if evidence.startswith("EXTERNAL:"):
            require(row["evidence_sha256"] == plan["sha256"], f"external claim hash {row['claim_id']}")
        elif row["evidence_sha256"] == "SELF":
            require(evidence == str(PACKET.relative_to(ROOT) / "README.md"), "SELF path")
        else:
            require(registered.get(evidence) == row["evidence_sha256"], f"registered claim evidence {row['claim_id']}")

    execution = freeze["execution"]
    require(execution["cosmology_software_or_likelihood_run"] is False, "no cosmology run")
    require(execution["scientific_promotion"] is False, "no promotion")
    print(f"PASS {SCHEMA}: 9 source hashes, 14 prerequisite gates, 11 typed claims")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL {SCHEMA}: {error}", file=sys.stderr)
        raise SystemExit(1)

