#!/usr/bin/env python3
"""Exact read-only census for the complete Stage-1 transfer boundary."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Final


ROOT: Final[Path] = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage1_handoff_verifier import (  # noqa: E402
    EXTERNAL_CACHE_MANIFEST_PATHS,
    STAGE1_RESULT_PATHS,
)


SOURCE_GROUPS: Final[dict[str, tuple[str, ...]]] = {
    "target_v012": tuple(
        f"DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/{name}"
        for name in (
            "METHOD.md", "build_target_cache.py", "consume_target_cache.py",
            "production_obligation_validators.py", "validate_preflight.py",
        )
    ),
    "hostile_v004r4": tuple(
        f"AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/{name}"
        for name in (
            "V004R4_CACHE_METHOD.md", "build_cache_v004r4.py",
            "consume_cache_v004r4.py", "validate_cache_preflight_v004r4.py",
            "independent_prefix_history.py", "independent_prefix_history_v002.py",
            "independent_prefix_history_v003.py", "independent_prefix_history_v004.py",
            "independent_prefix_history_v004r2.py", "v004r2_common.py",
            "validate_v004r4_zero_length_preflight.py", "v004r4_cache_io.py",
        )
    ),
    "dual_launch": (
        "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/dual_launch_coordinator.py",
        "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/production_dual_l12_launcher.py",
    ),
    "final_adjudication": (
        "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/independent_final_auditor.py",
        "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/production_dag_refinement.py",
        "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/production_evidence_orchestrator.py",
    ),
}

CONTROL_PATHS: Final[tuple[str, ...]] = (
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/FROZEN_MANIFEST_V004R4.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_RESULT_V001.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PREFLIGHT_RESULT.json",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_AUDIT_RESULT_V004R4.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_MUTATION_LEDGER_V001.json",
)
BOUNDARY_REQUIRED_PATHS: Final[tuple[str, ...]] = tuple(sorted(set(
    CONTROL_PATHS + STAGE1_RESULT_PATHS + EXTERNAL_CACHE_MANIFEST_PATHS
)))
EXPLICITLY_UNFROZEN: Final[tuple[str, ...]] = (
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/v004r4_cross_branch_contract.py",
)


class CensusRefusal(RuntimeError):
    """The Stage-1 artifact census is incomplete or ambiguous."""


def _identity(value: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode,
    )


def _safe_path(path_text: str) -> Path:
    if (
        type(path_text) is not str or not path_text or path_text.startswith("/")
        or "\x00" in path_text or Path(path_text).as_posix() != path_text
        or ".." in Path(path_text).parts
    ):
        raise CensusRefusal("unsafe Stage-1 census path")
    if ROOT.resolve() != ROOT:
        raise CensusRefusal("repository root is symlinked")
    cursor = ROOT
    for component in Path(path_text).parts[:-1]:
        cursor = cursor / component
        try:
            metadata = os.lstat(cursor)
        except OSError as error:
            raise CensusRefusal(f"missing parent: {path_text}") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise CensusRefusal(f"symlinked/non-directory parent: {path_text}")
    return ROOT / path_text


def _ordinary(path_text: str, *, require_read_only: bool) -> dict[str, object]:
    path = _safe_path(path_text)
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_DIRECTORY", 0)
    )
    file_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    parent_fd = -1
    file_fd = -1
    try:
        parent_fd = os.open(path.parent, parent_flags)
        parent_before = os.fstat(parent_fd)
        parent_path_before = os.stat(path.parent, follow_symlinks=False)
        if (
            not stat.S_ISDIR(parent_before.st_mode)
            or _identity(parent_before) != _identity(parent_path_before)
        ):
            raise CensusRefusal(f"parent identity mismatch: {path_text}")
        file_fd = os.open(path.name, file_flags, dir_fd=parent_fd)
        before = os.fstat(file_fd)
        path_before = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
            or _identity(before) != _identity(path_before)
            or (require_read_only and bool(before.st_mode & 0o222))
        ):
            raise CensusRefusal(f"ordinary owner-once file required: {path_text}")
        digest = hashlib.sha256()
        offset = 0
        while True:
            block = os.pread(file_fd, 16 * 2**20, offset)
            if not block:
                break
            digest.update(block)
            offset += len(block)
        after = os.fstat(file_fd)
        path_after = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        parent_after = os.fstat(parent_fd)
        parent_path_after = os.stat(path.parent, follow_symlinks=False)
        if (
            _identity(after) != _identity(before)
            or _identity(path_after) != _identity(before)
            or _identity(parent_after) != _identity(parent_before)
            or _identity(parent_path_after) != _identity(parent_before)
        ):
            raise CensusRefusal(f"descriptor/path identity drift: {path_text}")
        return {
            "path": path_text,
            "bytes": before.st_size,
            "sha256": digest.hexdigest(),
            "read_only": not bool(before.st_mode & 0o222),
        }
    except OSError as error:
        raise CensusRefusal(f"missing or unreadable artifact: {path_text}") from error
    finally:
        if file_fd >= 0:
            os.close(file_fd)
        if parent_fd >= 0:
            os.close(parent_fd)


def stage1_artifact_census(*, require_boundary_evidence: bool = False) -> dict[str, object]:
    """Return exact source/evidence custody, or refuse at the Stage-1 boundary."""
    source = {
        group: [
            _ordinary(path, require_read_only=require_boundary_evidence)
            for path in paths
        ]
        for group, paths in SOURCE_GROUPS.items()
    }
    required: list[dict[str, object] | None] = []
    missing: list[str] = []
    for path in BOUNDARY_REQUIRED_PATHS:
        try:
            required.append(_ordinary(
                path, require_read_only=require_boundary_evidence,
            ))
        except CensusRefusal:
            required.append(None)
            missing.append(path)
    if require_boundary_evidence and missing:
        raise CensusRefusal(
            "Stage-1 boundary evidence incomplete: " + ", ".join(missing)
        )
    unfrozen = [
        _ordinary(path, require_read_only=False) for path in EXPLICITLY_UNFROZEN
    ]
    return {
        "schema": "STAGE1_TARGET_HOSTILE_ARTIFACT_CENSUS_V002",
        "classification": (
            "PASS_COMPLETE_STAGE1_BOUNDARY_CENSUS"
            if not missing else "PREPARATION_SOURCE_CENSUS_ONLY"
        ),
        "source_by_group": source,
        "source_count_by_group": {
            group: len(paths) for group, paths in SOURCE_GROUPS.items()
        },
        "boundary_required_path_census": list(BOUNDARY_REQUIRED_PATHS),
        "boundary_required_artifacts": required,
        "boundary_required_count": len(BOUNDARY_REQUIRED_PATHS),
        "stage1_result_count": len(STAGE1_RESULT_PATHS),
        "external_cache_manifest_count": len(EXTERNAL_CACHE_MANIFEST_PATHS),
        "missing_boundary_evidence": missing,
        "explicitly_unfrozen_not_executed": unfrozen,
        "claim_boundary": (
            "STAGE1_CONTROL_AND_CUSTODY_CENSUS_ONLY__NO_CACHE_HISTORY_"
            "SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(stage1_artifact_census(), sort_keys=True, indent=2))
