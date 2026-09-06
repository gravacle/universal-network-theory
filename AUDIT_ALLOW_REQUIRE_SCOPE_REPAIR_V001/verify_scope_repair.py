#!/usr/bin/env python3
"""Mechanical hostile screen for a later allow/require scope repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FROZEN = HERE / "FROZEN_METHOD.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text())


def keyed(rows, field: str):
    result = {}
    for row in rows:
        key = row.get(field)
        if key in result:
            raise AssertionError(f"duplicate {field}: {key}")
        result[key] = row
    return result


class Checks:
    def __init__(self):
        self.passed = 0
        self.total = 0
        self.failures = []

    def check(self, condition, label: str):
        self.total += 1
        if condition:
            self.passed += 1
        else:
            self.failures.append(label)


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    frozen = load_json(FROZEN)
    result = Checks()

    result.check(digest(HERE / "METHODOLOGY.md") == frozen["methodology_sha256"], "frozen methodology hash")
    result.check(digest(HERE / "TARGET_MANIFEST_SCHEMA.json") == frozen["schema_sha256"], "frozen schema hash")
    result.check(digest(Path(__file__)) == frozen["verifier_sha256"], "frozen verifier hash")

    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    result.check(manifest_path.is_file(), "target manifest exists")
    if not manifest_path.is_file():
        print("FAIL: target manifest does not exist")
        return 1
    manifest = load_json(manifest_path)
    result.check(manifest.get("schema") == "ALLOW_REQUIRE_SCOPE_REPAIR_TARGET_V001", "target schema")
    result.check(nonempty(manifest.get("target_packet")), "target packet named")

    artifacts = manifest.get("artifacts", [])
    result.check(bool(artifacts), "target artifacts declared")
    for artifact in artifacts:
        rel = artifact.get("path", "")
        artifact_path = root / rel
        result.check(nonempty(rel) and artifact_path.is_file(), f"artifact exists: {rel}")
        expected = artifact.get("sha256", "")
        result.check(bool(re.fullmatch(r"[0-9a-f]{64}", expected)), f"artifact hash syntax: {rel}")
        if artifact_path.is_file() and re.fullmatch(r"[0-9a-f]{64}", expected or ""):
            result.check(digest(artifact_path) == expected, f"artifact hash match: {rel}")
        result.check(nonempty(artifact.get("role")), f"artifact role: {rel}")

    provenance = keyed(manifest.get("provenance", []), "key")
    permitted_dispositions = set(frozen["permitted_provenance_dispositions"])
    for key in frozen["required_provenance_keys"]:
        result.check(key in provenance, f"provenance covered: {key}")
        if key not in provenance:
            continue
        row = provenance[key]
        baseline = frozen["provenance_anchors"][key]
        result.check(row.get("source_path") == baseline["source_path"], f"provenance source: {key}")
        result.check(nonempty(row.get("locator")), f"provenance locator: {key}")
        result.check(row.get("disposition") in permitted_dispositions, f"provenance disposition: {key}")
        result.check(nonempty(row.get("post_repair_scope")), f"provenance scope: {key}")
        result.check(nonempty(row.get("reason")), f"provenance reason: {key}")

    types = keyed(manifest.get("types", []), "name")
    for name, expected in frozen["required_types"].items():
        result.check(name in types, f"type defined: {name}")
        if name not in types:
            continue
        row = types[name]
        result.check(row.get("kind") in expected["permitted_kinds"], f"type kind: {name}")
        result.check(row.get("commutator_eligible") is expected["commutator_eligible"], f"commutator eligibility: {name}")
        result.check(nonempty(row.get("definition")), f"type definition text: {name}")

    theorem = manifest.get("fixed_parent_theorem", {})
    for field in frozen["fixed_parent_true_fields"]:
        result.check(theorem.get(field) is True, f"fixed-parent antecedent/conclusion true: {field}")
    for field in frozen["fixed_parent_false_fields"]:
        result.check(theorem.get(field) is False, f"fixed-parent overclaim false: {field}")

    enlarged = manifest.get("enlarged_parent", {})
    for field in frozen["enlarged_parent_true_fields"]:
        result.check(enlarged.get(field) is True, f"enlarged-parent opening true: {field}")
    for field in frozen["enlarged_parent_false_fields"]:
        result.check(enlarged.get(field) is False, f"enlarged-parent claim ceiling false: {field}")

    adm = manifest.get("adm_correction", {})
    for field in frozen["adm_true_fields"]:
        result.check(adm.get(field) is True, f"ADM correction true: {field}")
    for field in frozen["adm_false_fields"]:
        result.check(adm.get(field) is False, f"ADM overclaim false: {field}")
    result.check(nonempty(adm.get("authoritative_reference")), "ADM authoritative reference")

    dispositions = keyed(manifest.get("dependency_dispositions", []), "id")
    for row_id, allowed in frozen["required_dependency_dispositions"].items():
        result.check(row_id in dispositions, f"dependency disposition present: {row_id}")
        if row_id not in dispositions:
            continue
        row = dispositions[row_id]
        result.check(row.get("disposition") in allowed, f"dependency disposition allowed: {row_id}")
        result.check(nonempty(row.get("post_repair_scope")), f"dependency scope: {row_id}")
        result.check(nonempty(row.get("reason")), f"dependency reason: {row_id}")

    guards = manifest.get("operator_guard", {})
    for field in frozen["operator_guard_false_fields"]:
        result.check(guards.get(field) is False, f"operator category-error guard: {field}")

    preserved = keyed(manifest.get("historical_preservation", []), "path")
    for rel, expected_hash in frozen["historical_hashes"].items():
        current_path = root / rel
        result.check(current_path.is_file(), f"historical file exists: {rel}")
        if current_path.is_file():
            result.check(digest(current_path) == expected_hash, f"historical bytes preserved: {rel}")
        result.check(rel in preserved, f"historical manifest row: {rel}")
        if rel in preserved:
            row = preserved[rel]
            result.check(row.get("baseline_sha256") == expected_hash, f"historical baseline hash: {rel}")
            result.check(row.get("current_sha256") == expected_hash, f"historical current hash: {rel}")
            result.check(row.get("edited") is False, f"historical edited false: {rel}")

    policy = manifest.get("historical_policy", {})
    result.check(policy.get("sealed_history_edited") is False, "sealed history not edited")
    result.check(policy.get("dated_erratum_present") is True, "dated erratum present")
    result.check(isinstance(policy.get("live_files_modified"), list) and bool(policy["live_files_modified"]), "modified live files enumerated")

    boundary = manifest.get("claim_boundary", {})
    for field, allowed in frozen["claim_boundary"].items():
        result.check(boundary.get(field) in allowed, f"claim boundary: {field}")

    verdict = "PASS_MECHANICAL__SEMANTIC_HOSTILE_READ_REQUIRED" if not result.failures else "FAIL_CLOSED"
    report = {
        "schema": "ALLOW_REQUIRE_SCOPE_REPAIR_AUDIT_RESULT_V001",
        "verdict": verdict,
        "checks_passed": result.passed,
        "checks_total": result.total,
        "failures": result.failures,
        "manifest": str(manifest_path),
        "manifest_sha256": digest(manifest_path),
        "semantic_promotion_required": True,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.write_text(rendered)
    print(rendered, end="")
    return 0 if not result.failures else 1


if __name__ == "__main__":
    sys.exit(main())
