#!/usr/bin/env python3
"""Verify Git-update allowlists without staging or otherwise mutating Git."""

from __future__ import annotations

import csv
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

from refresh_candidate_inventory import (
    INVENTORY_NAME,
    PLAN_DIR_NAME,
    REVIEW_NAME,
    RESOLUTIONS_NAME,
    candidate_states,
    categorical_exclusion,
    load_allowlists,
    load_review_resolutions,
    repo_root,
)


GITHUB_NORMAL_FILE_LIMIT = 100_000_000
EXPECTED_GROUPS = {
    "01_repository_hygiene",
    "02_l12_execution_control_foundation",
    "03_l12_repair_and_adjudication",
    "04_cross_scale_physical_products",
    "05_l14_reproducible_implementation",
    "06_urm_and_proof_reconciliation",
    "07_zenodo_scaffold",
    "08_l14_terminal_disposition",
}
ZENODO_GROUP = "07_zenodo_scaffold"
URM_GROUP = "06_urm_and_proof_reconciliation"
L14_DISPOSITION_GROUP = "08_l14_terminal_disposition"
L14_DISPOSITION_PATH = "L14_RUN_DISPOSITION_2026-09-16.md"
REQUIRED_ZENODO_PATHS = {
    "publication/zenodo_reproduction_v001/capsule_manifest.json",
    "publication/zenodo_reproduction_v001/UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.docx",
    "publication/zenodo_reproduction_v001/UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.docx",
    "publication/zenodo_reproduction_v001/UNIVERSAL_NETWORK_THEORY_MAJOR_PROOF_INDEX.md",
    "publication/zenodo_reproduction_v001/urm_validator_dependency_closure.json",
}
REQUIRED_CROSS_SCALE_PATHS = {
    "ARGER_GATE_ADOPTION_2026-09-16.md",
    "AUDIT_L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md",
    "DEVELOPMENT_R_ARGER_GATE_V001/README.md",
    "DEVELOPMENT_R_ARGER_GATE_V001/arger_gate.py",
    "DEVELOPMENT_R_ARGER_GATE_V001/test_arger_gate.py",
    (
        "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
        "STRICT_COMMON_LINEAGE_PROGRESSION_V001.json"
    ),
    "L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md",
    "L12_RECORD_BLOCK_MEMBERSHIP_THEOREM_AUDIT_2026-09-16.md",
    "L4_L12_EXTENDIBLE_RECORD_BLOCK_THEOREM_2026-09-16.md",
}
REQUIRED_URM_PATHS = {
    "ALPHA_PROGRAM_PROVENANCE_2026-09-15.md",
    "GLOSSARY.md",
    "GRAVITY_VERIFICATION_LEDGER.md",
    "MODEL.md",
    "PROOF_GUIDE.md",
    "RECORD_FORMATION_V001.md",
    "THE_CLAIMS_V001.md",
    "UNIVERSAL_NETWORK_THEORY_ARCHITECTURE_V001.md",
    "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md",
    "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md.sha256",
    "URM_VALIDATION_CURRENT_2026-09-16.md",
    "model/alpha_role.py",
    "model/project_model.py",
    "model/relational_accumulation.py",
    "model/universal_network_theory.py",
    "model/validate_alpha_role.py",
    "model/validate_relational_accumulation.py",
    "model/validate_universal_network_theory.py",
    "model/validate_urm.py",
    "proofsrc/CURRENT_RECONCILIATION.json",
}
RETIRED_ZENODO_PATH_FRAGMENTS = (
    "publication/zenodo_ladder_packet_blueprint_v001/",
    "/release_inputs/l14_runtime/",
    "stage6",
)
RETIRED_ZENODO_BASENAMES = {
    "L12_RELEASE_VERIFICATION_LAYOUT.json",
    "prepare_l14_public_runtime.py",
    "sanitize_l12_release_inputs.py",
    "test_prepare_l14_public_runtime.py",
    "test_sanitize_l12_release_inputs.py",
    "test_verify_l12_release_evidence.py",
    "verify_l12_release_evidence.py",
}
RETIRED_GOVERNING_CONTENT_PATTERN = re.compile(rb"stage[-_ ]?6", re.IGNORECASE)
ALLOWED_NATIVE_GATE_PREFIXES = (
    (
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/"
        "RUN_V002_L12_V003R1_STAGE6R2/"
    ),
    (
        "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001/"
        "RUN_V002_L12_V003R1_STAGE6R2/"
    ),
)
ALLOWED_NATIVE_GATE_SUFFIXES = (
    "SPECTRUM_INDEX.json",
    *(f"RAW/SECTOR_L10_Q{q}.json" for q in range(3, 7)),
    *(f"RAW/SECTOR_L12_Q{q}.json" for q in range(4, 8)),
)
ALLOWED_NATIVE_GATE_REFERENCES = {
    prefix + suffix
    for prefix in ALLOWED_NATIVE_GATE_PREFIXES
    for suffix in ALLOWED_NATIVE_GATE_SUFFIXES
}
LIVE_CONTENT_PATTERNS = (
    re.compile(rb"151193" rb"582766"),
    re.compile(rb"arn:aws:[^\s\"']*::151193" rb"582766:"),
    re.compile(rb"\bl14-" rb"personal\b"),
    re.compile(rb"\bl14-scout-" rb"control\b"),
    re.compile(rb"\b(?:i|vpc|subnet|sg)-[0-9a-f]{8,17}\b"),
    re.compile(rb"\bl14-scout-20260915-r1-" rb"control(?:-[a-z0-9-]+)?\b"),
)
SECRET_PATTERNS = (
    re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(rb"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def json_string_values(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from json_string_values(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from json_string_values(key)
            yield from json_string_values(item)


def disallowed_stage6_reference(path: str, content: bytes) -> str | None:
    """Return one retired Stage-6 reference, allowing only 18 native Gate inputs."""
    if not RETIRED_GOVERNING_CONTENT_PATTERN.search(content):
        return None
    suffix = PurePosixPath(path).suffix.casefold()
    if suffix != ".json":
        return "retired Stage-6 terminology"
    try:
        document = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return "invalid JSON containing retired Stage-6 terminology"
    for value in json_string_values(document):
        if not re.search(r"stage[-_ ]?6", value, re.IGNORECASE):
            continue
        normalized = value.removeprefix("urm/")
        if normalized not in ALLOWED_NATIVE_GATE_REFERENCES:
            return value
    return None


def main() -> int:
    repo = repo_root()
    plan_dir = repo / PLAN_DIR_NAME
    errors: list[str] = []

    index = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if index.returncode != 0:
        fail(errors, "Git index is not empty; verifier refuses to inspect a staged state")

    try:
        selected = load_allowlists(plan_dir)
        resolutions = load_review_resolutions(plan_dir)
    except Exception as exc:  # fail closed with the precise parser error
        fail(errors, f"allowlist parse failed: {exc}")
        selected = {}
        resolutions = {}

    groups = set(selected.values())
    if groups != EXPECTED_GROUPS:
        for group in sorted(EXPECTED_GROUPS - groups):
            fail(errors, f"required allowlist group is absent or empty: {group}")
        for group in sorted(groups - EXPECTED_GROUPS):
            fail(errors, f"unexpected allowlist group: {group}")

    disposition_paths = {
        path for path, group in selected.items() if group == L14_DISPOSITION_GROUP
    }
    if disposition_paths != {L14_DISPOSITION_PATH}:
        fail(
            errors,
            "L14 terminal-disposition group must contain exactly "
            f"{L14_DISPOSITION_PATH!r}",
        )

    zenodo_paths = {path for path, group in selected.items() if group == ZENODO_GROUP}
    for path in sorted(REQUIRED_ZENODO_PATHS - zenodo_paths):
        fail(errors, f"Zenodo allowlist omits required current packet path: {path}")
    for path in sorted(zenodo_paths):
        lowered = path.casefold()
        if any(fragment.casefold() in lowered for fragment in RETIRED_ZENODO_PATH_FRAGMENTS):
            fail(errors, f"Zenodo allowlist contains retired proof/runtime path: {path}")
        if PurePosixPath(path).name in RETIRED_ZENODO_BASENAMES:
            fail(errors, f"Zenodo allowlist contains retired preparation path: {path}")

    cross_scale_paths = {
        path
        for path, group in selected.items()
        if group == "04_cross_scale_physical_products"
    }
    for path in sorted(REQUIRED_CROSS_SCALE_PATHS - cross_scale_paths):
        fail(errors, f"cross-scale allowlist omits required progression path: {path}")

    urm_paths = {path for path, group in selected.items() if group == URM_GROUP}
    for path in sorted(REQUIRED_URM_PATHS - urm_paths):
        fail(errors, f"URM/proof allowlist omits required governing path: {path}")

    inventory_path = plan_dir / INVENTORY_NAME
    review_path = plan_dir / REVIEW_NAME
    try:
        inventory = read_tsv(inventory_path)
        reviews = read_tsv(review_path)
    except Exception as exc:
        fail(errors, f"inventory parse failed: {exc}")
        inventory = []
        reviews = []

    required_fields = {
        "path", "git_state", "disposition", "group", "reason", "review_required"
    }
    if inventory and set(inventory[0]) != required_fields:
        fail(errors, f"inventory columns differ from required schema: {sorted(inventory[0])}")

    inventory_by_path: dict[str, dict[str, str]] = {}
    for row in inventory:
        path = row.get("path", "")
        if not path:
            fail(errors, "inventory contains an empty path")
        elif path in inventory_by_path:
            fail(errors, f"inventory duplicates path: {path}")
        else:
            inventory_by_path[path] = row

    live_states = candidate_states(repo)
    recorded_paths = set(inventory_by_path)
    live_paths = set(live_states)
    for path in sorted(set(resolutions) - live_paths)[:50]:
        fail(errors, f"review resolution names a non-candidate path: {path}")
    for path in sorted(live_paths - recorded_paths)[:50]:
        fail(errors, f"candidate path is absent from inventory; refresh required: {path}")
    for path in sorted(recorded_paths - live_paths)[:50]:
        fail(errors, f"inventory path is no longer a worktree candidate; refresh required: {path}")

    for path in sorted(live_paths & recorded_paths):
        recorded_state = inventory_by_path[path].get("git_state")
        if recorded_state != live_states[path]:
            fail(
                errors,
                f"Git state mismatch for {path}: recorded={recorded_state!r} "
                f"live={live_states[path]!r}",
            )

    selected_from_inventory = {
        path
        for path, row in inventory_by_path.items()
        if row.get("disposition") == "selected"
    }
    if selected_from_inventory != set(selected):
        for path in sorted(set(selected) - selected_from_inventory)[:50]:
            fail(errors, f"allowlisted path is not recorded selected in inventory: {path}")
        for path in sorted(selected_from_inventory - set(selected))[:50]:
            fail(errors, f"inventory-selected path is absent from allowlists: {path}")

    for path, decision in sorted(resolutions.items()):
        resolution = decision.get("resolution", "")
        group = decision.get("group", "")
        row = inventory_by_path.get(path)
        if resolution in {"include", "selected_approved"}:
            if selected.get(path) != group:
                fail(
                    errors,
                    f"resolved selected path has wrong or absent allowlist group: {path}",
                )
            if row and row.get("review_required") != "-":
                fail(errors, f"content-approved selected path remains in review: {path}")
        elif resolution in {"exclude", "defer"}:
            expected = "deferred" if resolution == "defer" else "excluded"
            if path in selected:
                fail(errors, f"non-selected resolution remains allowlisted: {path}")
            if row and row.get("disposition") != expected:
                fail(
                    errors,
                    f"resolved path has wrong disposition for {resolution}: {path}",
                )
        else:
            fail(errors, f"unknown review resolution for {path}: {resolution!r}")

    for path, group in sorted(selected.items()):
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or path != pure.as_posix():
            fail(errors, f"allowlist path is not a normalized repository-relative path: {path}")
            continue
        target = repo / path
        if not target.is_file():
            fail(errors, f"allowlisted path does not exist as a regular file: {path}")
            continue
        exclusion = categorical_exclusion(path)
        if exclusion:
            fail(errors, f"allowlisted path matches excluded category ({exclusion[1]}): {path}")
        row = inventory_by_path.get(path)
        if row and row.get("group") != group:
            fail(
                errors,
                f"group mismatch for {path}: allowlist={group!r}, inventory={row.get('group')!r}",
            )
        size = target.stat().st_size
        if size >= GITHUB_NORMAL_FILE_LIMIT:
            fail(errors, f"allowlisted file is at least 100,000,000 bytes ({size}): {path}")

        try:
            content = target.read_bytes()
        except OSError as exc:
            fail(errors, f"cannot read allowlisted file {path}: {exc}")
            continue
        if group == ZENODO_GROUP and target.suffix.casefold() in {".json", ".md", ".tsv"}:
            retired_reference = disallowed_stage6_reference(path, content)
            if retired_reference is not None:
                fail(
                    errors,
                    "current Zenodo proof surface contains disallowed Stage-6 "
                    f"reference in {path}: {retired_reference}",
                )
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                fail(errors, f"allowlisted file matches a secret-key pattern: {path}")
                break
        for pattern in LIVE_CONTENT_PATTERNS:
            if pattern.search(content):
                fail(errors, f"allowlisted file contains a live AWS identifier pattern: {path}")
                break

    expected_reviews = {
        row["path"]
        for row in inventory
        if row.get("disposition") == "manual_review" or row.get("review_required") != "-"
    }
    recorded_reviews = {row.get("path", "") for row in reviews}
    if expected_reviews != recorded_reviews:
        for path in sorted(expected_reviews - recorded_reviews)[:50]:
            fail(errors, f"review queue omits required path: {path}")
        for path in sorted(recorded_reviews - expected_reviews)[:50]:
            fail(errors, f"review queue contains an unexpected path: {path}")
    if reviews:
        fail(
            errors,
            f"review queue is not empty after exact-path adjudication: {len(reviews)} row(s)",
        )

    selected_counts: dict[str, int] = {}
    state_counts: dict[str, int] = {}
    disposition_counts: dict[str, int] = {}
    for path, group in selected.items():
        selected_counts[group] = selected_counts.get(group, 0) + 1
    for row in inventory:
        state = row.get("git_state", "")
        disposition = row.get("disposition", "")
        state_counts[state] = state_counts.get(state, 0) + 1
        disposition_counts[disposition] = disposition_counts.get(disposition, 0) + 1

    if errors:
        print("ALLOWLIST_VERIFICATION: FAIL", file=sys.stderr)
        for message in errors:
            print(f"- {message}", file=sys.stderr)
        return 1

    print("ALLOWLIST_VERIFICATION: PASS")
    print(f"index_empty=yes candidates={len(inventory)} selected={len(selected)}")
    print("states=" + ",".join(f"{key}:{state_counts[key]}" for key in sorted(state_counts)))
    print(
        "dispositions="
        + ",".join(f"{key}:{disposition_counts[key]}" for key in sorted(disposition_counts))
    )
    for group in sorted(selected_counts):
        print(f"group {group}: {selected_counts[group]}")
    print(f"review_queue={len(reviews)} max_selected_bytes={max((repo / p).stat().st_size for p in selected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
