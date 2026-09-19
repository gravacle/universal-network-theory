#!/usr/bin/env python3
"""Refresh the fail-closed inventory without changing any commit allowlist.

New worktree paths are classified only as categorically excluded or as
manual-review items.  This script never adds a path to an allowlist.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile


PLAN_DIR_NAME = "git_update_allowlists_2026-09-15"
INVENTORY_NAME = "candidate_inventory.tsv"
REVIEW_NAME = "manual_review.tsv"
RESOLUTIONS_NAME = "review_resolutions.tsv"
SANITIZE_BEFORE_SELECTION = {
    "DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/EXACT_KERNEL_AUDIT_V003R6.json",
    "DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/aws/stage_assets.py",
    "DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/aws/stage_control.py",
    "DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/readiness.py",
    "DEVELOPMENT_R_L14_TARGETED_SCOUT_V003/tests/test_infrastructure_static.py",
}


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def repo_root() -> Path:
    here = Path(__file__).resolve().parent
    result = git(here, "rev-parse", "--show-toplevel")
    return Path(result.stdout.decode().strip()).resolve()


def nul_paths(data: bytes) -> set[str]:
    return {item.decode("utf-8", "strict") for item in data.split(b"\0") if item}


def candidate_states(repo: Path) -> dict[str, str]:
    modified = nul_paths(git(repo, "diff", "--name-only", "-z").stdout)
    untracked = nul_paths(
        git(repo, "ls-files", "--others", "--exclude-standard", "-z").stdout
    )
    overlap = modified & untracked
    if overlap:
        raise RuntimeError(f"paths reported as both tracked-modified and untracked: {sorted(overlap)!r}")
    states = {path: "tracked_modified" for path in modified}
    states.update({path: "untracked" for path in untracked})
    return states


def load_allowlists(plan_dir: Path) -> dict[str, str]:
    selected: dict[str, str] = {}
    for allowlist in sorted(plan_dir.glob("allowlist_*.txt")):
        group = allowlist.stem.removeprefix("allowlist_")
        for line_number, raw in enumerate(allowlist.read_text(encoding="utf-8").splitlines(), 1):
            path = raw.strip()
            if not path or path.startswith("#"):
                continue
            if path in selected:
                raise RuntimeError(
                    f"duplicate selected path {path!r} in {selected[path]!r} and "
                    f"{allowlist.name}:{line_number}"
                )
            selected[path] = group
    if not selected:
        raise RuntimeError("no allowlist entries found")
    return selected


def load_review_resolutions(plan_dir: Path) -> dict[str, dict[str, str]]:
    """Load exact-path review decisions made for the current public update."""
    path = plan_dir / RESOLUTIONS_NAME
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required = {"path", "resolution", "group", "reason"}
    if rows and set(rows[0]) != required:
        raise RuntimeError(
            f"{RESOLUTIONS_NAME} columns differ from required schema: "
            f"{sorted(rows[0])!r}"
        )
    resolutions: dict[str, dict[str, str]] = {}
    allowed = {"include", "selected_approved", "exclude", "defer"}
    for line_number, row in enumerate(rows, 2):
        item = row["path"]
        resolution = row["resolution"]
        group = row["group"]
        reason = row["reason"]
        if not item or item in resolutions:
            raise RuntimeError(
                f"invalid or duplicate review path at {RESOLUTIONS_NAME}:{line_number}: "
                f"{item!r}"
            )
        if resolution not in allowed:
            raise RuntimeError(
                f"unknown resolution at {RESOLUTIONS_NAME}:{line_number}: {resolution!r}"
            )
        if not reason:
            raise RuntimeError(
                f"empty reason at {RESOLUTIONS_NAME}:{line_number}"
            )
        if resolution in {"include", "selected_approved"} and group == "-":
            raise RuntimeError(
                f"selected resolution lacks a group at {RESOLUTIONS_NAME}:{line_number}"
            )
        if resolution in {"exclude", "defer"} and group != "-":
            raise RuntimeError(
                f"non-selected resolution names a group at {RESOLUTIONS_NAME}:{line_number}"
            )
        resolutions[item] = row
    return resolutions


def categorical_exclusion(path: str) -> tuple[str, str] | None:
    """Return (disposition, reason) for categories forbidden from selection."""
    pure = PurePosixPath(path)
    parts = pure.parts
    lowered = tuple(part.casefold() for part in parts)
    basename = pure.name
    base_lower = basename.casefold()

    if path.startswith("publication/zenodo_ladder_packet_blueprint_v001/"):
        return "excluded", "superseded Zenodo planning blueprint"

    if path in SANITIZE_BEFORE_SELECTION:
        return "excluded", "L14 source or audit embeds live AWS account, profile, or instance binding"

    if any(
        "cache_payloads" in part or "workspaces" in part or part == "workspace"
        for part in lowered
    ):
        return "excluded", "generated numerical cache or workspace"

    if "progress" in lowered:
        return "excluded", "generated progress journal"

    if (
        any(part in {"run_log", "run_logs", "logs", "test_logs"} for part in lowered)
        or base_lower.endswith(".log")
        or re.search(r"(?:^|_)(?:audit|test|worker|coordinator)_log(?:_|\.|$)", base_lower)
    ):
        return "excluded", "raw log or execution journal"

    archive_suffixes = (
        ".whl",
        ".tar",
        ".tar.gz",
        ".tar.xz",
        ".tar.bz2",
        ".tgz",
        ".tbz2",
        ".zip",
        ".pyc",
        ".pyd",
        ".so",
        ".dylib",
        ".exe",
        ".bin",
    )
    if base_lower.endswith(archive_suffixes):
        return "excluded", "runtime binary, wheel, bytecode, or generated archive"
    if any(part in {"wheelhouse", "python_runtime", "packaged_runtime"} for part in lowered):
        return "excluded", "packaged runtime or wheelhouse"

    if any(part in {"paid_attempts", "aws_launch_journal"} for part in lowered):
        return "excluded", "raw paid-attempt or AWS launch journal"

    operational_dir = any(
        part.startswith(("aws_run_", "aws_control_", "aws_deploy_"))
        for part in lowered[1:-1]
    )
    operational_name = (
        base_lower.startswith(
            (
                "aws_instance_allocation",
                "aws_user_data",
                "aws_discovery",
                "aws_readiness",
                "aws_run_config",
                "aws_stack_inputs",
                "aws_stack_parameters",
                "aws_asset_staging",
                "aws_asset_prestaging",
                "stack_input_evidence",
                "stack_parameters",
                "ssm_",
                "target_activation_script_staging",
                "target_r6_clean_restart_authorization",
                "activate_target_",
            )
        )
        or base_lower in {"phase1_request.json", "run_identity.json"}
    )
    if operational_dir or operational_name:
        return "excluded", "live AWS allocation, configuration, readiness, or activation state"

    nested_dirs = lowered[1:-1]
    if any(
        "custody" in part
        or part.startswith("retired")
        or part == "retirement_events_v001"
        or part == "predecessor_source_bytes"
        for part in nested_dirs
    ):
        return "excluded", "duplicated nested custody or retired tree"

    return None


def selected_review_reason(
    path: str,
    group: str,
    resolutions: dict[str, dict[str, str]],
) -> str:
    resolved = resolutions.get(path)
    if resolved and resolved["resolution"] in {"include", "selected_approved"}:
        return "-"
    pure = PurePosixPath(path)
    lower = path.casefold()
    if group.startswith("05_") and (
        "/aws/" in lower
        or pure.suffix.casefold() in {".json", ".yaml", ".yml", ".sh"}
    ):
        return "review L14 source/config content for operational identifiers before staging"
    return "-"


def excluded_review_reason(path: str) -> str:
    if path in SANITIZE_BEFORE_SELECTION:
        return "create and review a sanitized replacement before Git admission"
    return "-"


def write_tsv_atomic(path: Path, header: list[str], rows: list[list[str]]) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(header)
            writer.writerows(rows)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    repo = repo_root()
    plan_dir = repo / PLAN_DIR_NAME
    selected = load_allowlists(plan_dir)
    resolutions = load_review_resolutions(plan_dir)
    states = candidate_states(repo)

    unknown_resolutions = sorted(set(resolutions) - set(states))
    if unknown_resolutions:
        preview = "\n".join(unknown_resolutions[:20])
        raise RuntimeError(
            "review resolutions name paths that are not worktree candidates:\n" + preview
        )

    for path, decision in sorted(resolutions.items()):
        resolution = decision["resolution"]
        group = decision["group"]
        if resolution in {"include", "selected_approved"}:
            if selected.get(path) != group:
                raise RuntimeError(
                    f"review resolution for {path!r} requires allowlist group {group!r}; "
                    f"found {selected.get(path)!r}"
                )
        elif path in selected:
            raise RuntimeError(
                f"review resolution for {path!r} is {resolution!r} but the path remains "
                "allowlisted"
            )

    missing_from_worktree = sorted(set(selected) - set(states))
    if missing_from_worktree:
        preview = "\n".join(missing_from_worktree[:20])
        raise RuntimeError(
            "allowlisted paths are no longer tracked modifications or untracked files:\n" + preview
        )

    inventory_rows: list[list[str]] = []
    review_rows: list[list[str]] = []
    for path in sorted(states):
        state = states[path]
        if path in selected:
            disposition = "selected"
            group = selected[path]
            reason = "exact path admitted to proposed Git update commit group"
            review = selected_review_reason(path, group, resolutions)
        elif path in resolutions:
            decision = resolutions[path]
            disposition = (
                "deferred" if decision["resolution"] == "defer" else "excluded"
            )
            group = "-"
            reason = decision["reason"]
            review = "-"
        else:
            exclusion = categorical_exclusion(path)
            if exclusion:
                disposition, reason = exclusion
                group = "-"
                review = excluded_review_reason(path)
            else:
                disposition = "manual_review"
                group = "-"
                reason = "not admitted by an exact reviewed allowlist"
                review = "decide include, exclude, or defer; no automatic selection"

        row = [path, state, disposition, group, reason, review]
        inventory_rows.append(row)
        if disposition == "manual_review" or review != "-":
            review_rows.append(row)

    header = ["path", "git_state", "disposition", "group", "reason", "review_required"]
    write_tsv_atomic(plan_dir / INVENTORY_NAME, header, inventory_rows)
    write_tsv_atomic(plan_dir / REVIEW_NAME, header, review_rows)

    counts: dict[str, int] = {}
    for row in inventory_rows:
        counts[row[2]] = counts.get(row[2], 0) + 1
    print(
        "candidate inventory refreshed: "
        + ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
        + f", review_rows={len(review_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
