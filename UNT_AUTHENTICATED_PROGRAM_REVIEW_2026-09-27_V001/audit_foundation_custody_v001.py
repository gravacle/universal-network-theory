#!/usr/bin/env python3
"""Read-only foundational custody audit; emits JSON, never changes inputs.

This audits bytes, manifest resolution, and review coverage. It does not certify
mathematical truth, discharge physical premises, or replace any sealed verifier.
Exit 1 means missing, mismatched, or unresolvable custody remains; exit 2 is usage.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


ALPHA = "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001"
AURFT = "LANE_RFT_AXIOMATIC_URFT_CLOSURE_V001"
CTS = "LANE_RFT_RECORD_TO_CTS_NONIMPLICATION_V001"
CAUSAL = "LANE_RFT_STANDARD_CAUSAL_URFT_SCOPE_V001"
PMICS = "LANE_CROSS_RFT_GRA_GJ_Q4_PAIR_MEMORY_INTRINSIC_CURVATURE_SYMBOL_V001"
GL6BQ = "LANE_CROSS_RFT_GRA_GL6BQ_AUTHENTICATED_ORIENTATION_REFINEMENT_RICCI_BOUNDARY_V001"
RECOVERY = "DEVELOPMENT_UNT_FOUNDATIONAL_PREMISE_DISCHARGE_V001"
CLOSURE = "GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md"
CAPSULE = "publication/zenodo_reproduction_v001/capsule_manifest.json"
ARCHIVE = ("publication/zenodo_reproduction_v001/dist/zenodo-upload-v1.0.0/"
           "universal-network-theory-reproduction-v1.0.0.zip")
HISTORICAL_MANIFEST_SHA256 = "75b8a80ad8dc39e92d1a3b031469fbe1019fc1a072d6b7bf3fd97abd0794dca9"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def relative(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def inspect_file(root: Path, path: Path, expected: str | None = None) -> dict:
    row = {"path": relative(root, path)}
    if expected is not None:
        row["expected_sha256"] = expected
    try:
        resolved = path.resolve()
        if resolved != root and root not in resolved.parents:
            row["status"] = "OUTSIDE_ROOT"
        elif path.is_symlink():
            row["status"] = "SYMLINK_NOT_ADMITTED"
        elif not path.is_file():
            row["status"] = "MISSING_OR_NOT_FILE"
        else:
            row["actual_sha256"] = digest(path)
            row["bytes"] = path.stat().st_size
            row["status"] = ("MATCH" if expected == row["actual_sha256"]
                             else "HASH_MISMATCH" if expected is not None
                             else "PRESENT")
    except OSError as exc:
        row["status"] = "READ_ERROR"
        row["error"] = str(exc)
    return row


def parse_manifest(path: Path) -> tuple[list[tuple[str, str]], list[dict]]:
    entries = []
    errors = []
    seen = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [], [{"status": "MANIFEST_READ_ERROR", "error": str(exc)}]
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})\s+(.+)", line)
        if not match:
            errors.append({"line": number, "status": "MALFORMED_MANIFEST_LINE"})
            continue
        expected, name = match.groups()
        if name in seen:
            errors.append({"line": number, "status": "DUPLICATE_PATH", "path": name})
        seen.add(name)
        if Path(name).is_absolute() or ".." in Path(name).parts:
            errors.append({"line": number, "status": "UNSAFE_PATH", "path": name})
            continue
        entries.append((expected, name))
    return entries, errors


def audit_manifest(root: Path, name: str, scope: str) -> dict:
    manifest = root / name
    entries, errors = parse_manifest(manifest)
    base = root if scope == "repository" else manifest.parent
    rows = [inspect_file(root, base / path, expected) for expected, path in entries]
    return {
        "manifest": inspect_file(root, manifest),
        "resolution_scope": scope,
        "entry_count": len(entries),
        "counts": dict(Counter(row["status"] for row in rows)),
        "errors": errors,
        "entries": rows,
    }


def original_resolver_diagnostics(root: Path) -> list[dict]:
    """Model only the sealed resolver's existing path choice; do not repair it."""
    rows = []
    for packet in (ALPHA, CTS, CAUSAL):
        manifest = root / packet / "MANIFEST.sha256"
        entries, _ = parse_manifest(manifest)
        collisions = []
        for expected, name in entries:
            root_candidate = root / name
            local_candidate = manifest.parent / name
            selected = root_candidate if root_candidate.is_file() else local_candidate
            if selected != local_candidate:
                collisions.append({
                    "manifest_item": name,
                    "original_resolver_selected": inspect_file(root, selected, expected),
                    "manifest_local_candidate": inspect_file(root, local_candidate, expected),
                })
        rows.append({"manifest": relative(root, manifest), "root_first_collisions": collisions})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Exact UNT checkout root")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir() or not (root / CLOSURE).is_file():
        parser.error("--root must be an existing UNT checkout containing the working closure")

    specifications = [
        (f"{ALPHA}/MANIFEST.sha256", "manifest_directory"),
        (f"{CTS}/MANIFEST.sha256", "manifest_directory"),
        (f"{CAUSAL}/MANIFEST.sha256", "manifest_directory"),
        (f"{AURFT}/MANIFEST.sha256", "repository"),
        (f"{AURFT}/DEPENDENCIES.sha256", "repository"),
        (f"{PMICS}/INDEPENDENT_HOSTILE_AUDIT/TARGET_CUSTODY.sha256", "pmics_packet"),
        (f"{PMICS}/DEPENDENCIES.sha256", "repository"),
        (f"{GL6BQ}/MANIFEST.sha256", "manifest_directory"),
    ]
    manifests = []
    for name, scope in specifications:
        if scope == "pmics_packet":
            path = root / name
            entries, errors = parse_manifest(path)
            rows = [inspect_file(root, root / PMICS / item, sha) for sha, item in entries]
            manifests.append({
                "manifest": inspect_file(root, path),
                "resolution_scope": "PMICS_packet_directory",
                "entry_count": len(entries),
                "counts": dict(Counter(row["status"] for row in rows)),
                "errors": errors,
                "entries": rows,
            })
        else:
            manifests.append(audit_manifest(root, name, scope))

    closure_text = (root / CLOSURE).read_text(encoding="utf-8")
    pins = re.findall(r"^\|[^\n|]+\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|", closure_text, re.M)
    closure_rows = [inspect_file(root, root / path, sha) for path, sha in pins]
    ledger_path = root / RECOVERY / "FOUNDATIONAL_CLAIM_LEDGER.tsv"
    with ledger_path.open(encoding="utf-8", newline="") as stream:
        ledger = list(csv.DictReader(stream, delimiter="\t"))
    ledger_counts = Counter(row["review_state"] for row in ledger)
    seeded = [row["claim_id"] for row in ledger if row["review_state"].startswith("seeded")]

    capsule_path = root / CAPSULE
    capsule = json.loads(capsule_path.read_text(encoding="utf-8"))
    direct_sources = {entry.get("source") for entry in capsule["entries"]}
    capsule_hash = digest(capsule_path)
    diagnostics = original_resolver_diagnostics(root)
    failures = [row for manifest in manifests for row in manifest["entries"] if row["status"] != "MATCH"]
    failures.extend(row for row in closure_rows if row["status"] != "MATCH")
    parse_errors = [error for manifest in manifests for error in manifest["errors"]]
    collisions = [collision for row in diagnostics for collision in row["root_first_collisions"]
                  if collision["original_resolver_selected"]["status"] != "MATCH"]
    expected_pin_count_ok = len(pins) == 12
    incomplete = bool(failures or parse_errors or collisions or not expected_pin_count_ok)
    report = {
        "schema": "UNT_FOUNDATIONAL_CUSTODY_REVIEW_V001",
        "root": str(root),
        "scope": "READ_ONLY_BYTE_CUSTODY_AND_COVERAGE_AUDIT_NOT_SCIENTIFIC_REPRODUCTION",
        "status": "INCOMPLETE_CUSTODY_AND_REPLAY_DIAGNOSTICS" if incomplete else "CHECKED_CUSTODY_PASS",
        "scientific_verifiers_modified": False,
        "scientific_verifiers_run_by_this_script": False,
        "manifest_checks": manifests,
        "working_closure": {
            "source": inspect_file(root, root / CLOSURE),
            "expected_pin_count": 12,
            "actual_pin_count": len(pins),
            "expected_pin_count_matches": expected_pin_count_ok,
            "counts": dict(Counter(row["status"] for row in closure_rows)),
            "dependencies": closure_rows,
            "scope_note": "Direct pins only; PMICS transitive dependencies are checked separately.",
        },
        "original_aurft_resolver": {
            "source": inspect_file(root, root / AURFT / "verify_axiomatic_urft_closure.py"),
            "diagnosis": "Original resolver prefers an existing repository-root name over manifest-local bytes.",
            "failing_collision_count": len(collisions),
            "diagnostics": diagnostics,
            "scope_note": "Path choice modeled read-only; no sealed verifier replaced, patched, or made to pass.",
        },
        "foundational_ledger": {
            "source": inspect_file(root, ledger_path),
            "row_count": len(ledger),
            "review_state_counts": dict(ledger_counts),
            "seeded_row_count": len(seeded),
            "seeded_claim_ids": seeded,
            "historical_readme_stated_row_count": 41,
            "readme_count_matches": len(ledger) == 41,
        },
        "publication_coverage": {
            "current_manifest": inspect_file(root, capsule_path),
            "historical_2026_09_25_manifest_sha256": HISTORICAL_MANIFEST_SHA256,
            "current_manifest_matches_historical_audit": capsule_hash == HISTORICAL_MANIFEST_SHA256,
            "archive": inspect_file(root, root / ARCHIVE),
            "working_closure_direct_entry_coverage": [
                {"path": path, "direct_manifest_entry": path in direct_sources} for path, _ in pins
            ],
            "scope_note": "Direct source-entry census, not a build or ZIP-membership certification; generated/transitive inclusion was not inferred.",
        },
        "failure_summary": {
            "hash_or_file_failures": len(failures),
            "manifest_parse_errors": len(parse_errors),
            "original_resolver_failing_collisions": len(collisions),
            "missing_or_failed_files": failures,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main())
