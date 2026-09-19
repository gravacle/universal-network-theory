#!/usr/bin/env python3
"""Shared fail-closed custody helpers for the Stage 6 compatibility packet."""

from __future__ import annotations

import hashlib
import json
import math
import os
import stat
from fractions import Fraction
from pathlib import Path
from typing import Final


SIZES: Final[tuple[int, ...]] = (4, 6, 8, 10, 12)
LARGE_SIZES: Final[tuple[int, ...]] = (10, 12)
MANIFEST_SCHEMA: Final = "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001"
MANIFEST_STATUS: Final = (
    "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY"
)
ACCUMULATION_PROTOCOL_SHA256: Final = (
    "d545a4dd0925d4ae47c1231f4f7632c4cdfef14d0864af292f19fd9f6a708d95"
)
PLAN_SCHEMA: Final = "BLIND_RELATIONAL_INTERVAL_SECTOR_PLAN_V001"
PLAN_STATUS: Final = "READY_FOR_PRE_TARGET_BLIND_METHOD_FREEZE"
FREEZE_SCHEMA: Final = "RELATIONAL_INTERVAL_BLIND_METHOD_FREEZE_V001"
FREEZE_STATUS: Final = "BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM"
INDEX_SCHEMA: Final = "RELATIONAL_INTERVAL_SPECTRUM_INDEX_V001"
HEX: Final = frozenset("0123456789abcdef")


class Refusal(RuntimeError):
    """A custody or exact-contract check failed closed."""


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise Refusal(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def valid_digest(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= HEX


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def load_pinned_json(path: Path, digest: str, label: str) -> dict[str, object]:
    demand(path.is_file(), f"{label}: regular file absent")
    demand(valid_digest(digest), f"{label}: invalid lowercase SHA-256")
    demand(sha256_file(path) == digest, f"{label}: SHA-256 mismatch")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise Refusal(f"{label}: invalid JSON") from error
    demand(isinstance(value, dict), f"{label}: top-level object required")
    return value


def repo_file(repo_root: Path, raw: object, digest: object, label: str) -> Path:
    demand(isinstance(raw, str) and raw, f"{label}: path absent")
    demand(valid_digest(digest), f"{label}: invalid SHA-256")
    relative = Path(raw)
    demand(
        not relative.is_absolute() and ".." not in relative.parts,
        f"{label}: noncanonical path",
    )
    root = repo_root.resolve()
    try:
        resolved = (root / relative).resolve(strict=True)
    except OSError as error:
        raise Refusal(f"{label}: regular file absent") from error
    demand(
        resolved.is_file() and root in resolved.parents,
        f"{label}: path escapes repository",
    )
    demand(sha256_file(resolved) == digest, f"{label}: SHA-256 mismatch")
    return resolved


def repo_relative(repo_root: Path, path: Path, label: str) -> str:
    root = repo_root.resolve()
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise Refusal(f"{label}: regular file absent") from error
    demand(
        resolved.is_file() and root in resolved.parents,
        f"{label}: outside repository",
    )
    return resolved.relative_to(root).as_posix()


def atomic_owner_once_json(repo_root: Path, output: Path, value: object) -> None:
    root = repo_root.resolve()
    declared = Path(os.path.abspath(output))
    demand(root in declared.parents, "output must remain repository-local")
    current = root
    for part in declared.relative_to(root).parts[:-1]:
        current /= part
        try:
            metadata = os.stat(current, follow_symlinks=False)
        except OSError as error:
            raise Refusal("output parent is absent") from error
        demand(
            stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode),
            "output parent is aliased or special",
        )
    demand(
        not os.path.lexists(declared),
        "owner-once output already exists or is aliased",
    )
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(declared.parent, parent_flags)
    except OSError as error:
        raise Refusal("output parent is aliased or special") from error
    descriptor = -1
    try:
        parent_before = os.fstat(parent_descriptor)
        parent_named = os.stat(declared.parent, follow_symlinks=False)
        demand(
            stat.S_ISDIR(parent_before.st_mode)
            and not stat.S_ISLNK(parent_named.st_mode)
            and (parent_before.st_dev, parent_before.st_ino)
            == (parent_named.st_dev, parent_named.st_ino),
            "output parent identity changed",
        )
        try:
            os.stat(
                declared.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            pass
        else:
            raise Refusal("owner-once output already exists or is aliased")
        descriptor = os.open(
            declared.name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400,
            dir_fd=parent_descriptor,
        )
        payload = canonical_json(value).encode("utf-8")
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            demand(written > 0, "owner-once write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        held = os.fstat(descriptor)
        named = os.stat(
            declared.name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        demand(
            stat.S_ISREG(held.st_mode)
            and not stat.S_ISLNK(named.st_mode)
            and held.st_nlink == 1
            and stat.S_IMODE(held.st_mode) == 0o444
            and held.st_size == len(payload)
            and (held.st_dev, held.st_ino) == (named.st_dev, named.st_ino),
            "owner-once custody failed",
        )
        os.fsync(parent_descriptor)
        parent_after = os.stat(declared.parent, follow_symlinks=False)
        demand(
            (parent_before.st_dev, parent_before.st_ino)
            == (parent_after.st_dev, parent_after.st_ino),
            "output parent identity changed",
        )
    except BaseException:
        # Retain an exclusively created inode as obstruction evidence.
        raise
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        os.close(parent_descriptor)


def reduced_pair(value: object, label: str) -> tuple[int, int]:
    demand(
        isinstance(value, list)
        and len(value) == 2
        and type(value[0]) is int
        and type(value[1]) is int,
        f"{label}: reduced integer pair required",
    )
    numerator, denominator = int(value[0]), int(value[1])
    demand(
        denominator > 0 and math.gcd(numerator, denominator) == 1,
        f"{label}: rational not reduced",
    )
    return numerator, denominator


def q_at_density(length: int, density: Fraction) -> int:
    shifted = 2 * length * density + Fraction(1, 2)
    return min(length, max(0, shifted.numerator // shifted.denominator))


def fraction_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def exact_atom_partition(
    common_left: Fraction, common_right: Fraction
) -> list[dict[str, object]]:
    boundaries = {common_left, common_right}
    for length in SIZES:
        for charge in range(length):
            boundary = Fraction(2 * charge + 1, 4 * length)
            if common_left < boundary < common_right:
                boundaries.add(boundary)
    ordered = sorted(boundaries)
    atoms: list[dict[str, object]] = []
    for ordinal, (left, right) in enumerate(zip(ordered, ordered[1:])):
        midpoint = (left + right) / 2
        atoms.append(
            {
                "atom_id": f"A{ordinal:03d}",
                "density_interval": [fraction_pair(left), fraction_pair(right)],
                "q_by_L": {
                    str(length): q_at_density(length, midpoint)
                    for length in SIZES
                },
            }
        )
    return atoms


def validate_authenticated_manifest(
    repo_root: Path,
    manifest_path: Path,
    manifest_sha256: str,
) -> dict[str, object]:
    manifest = load_pinned_json(
        manifest_path, manifest_sha256, "accumulation manifest"
    )
    demand(manifest.get("schema") == MANIFEST_SCHEMA, "manifest schema mismatch")
    demand(manifest.get("status") == MANIFEST_STATUS, "manifest status mismatch")
    demand(
        manifest.get("accumulation_protocol_sha256")
        == ACCUMULATION_PROTOCOL_SHA256,
        "accumulation protocol binding mismatch",
    )
    histories = manifest.get("histories")
    demand(
        isinstance(histories, dict)
        and set(histories) == {str(length) for length in SIZES},
        "manifest history size census mismatch",
    )
    for length in SIZES:
        entry = histories[str(length)]
        demand(isinstance(entry, dict), f"L{length}: history entry invalid")
        repo_file(
            repo_root,
            entry.get("target_history_path"),
            entry.get("target_history_sha256"),
            f"L{length} target history",
        )
        repo_file(
            repo_root,
            entry.get("blind_history_path"),
            entry.get("blind_history_sha256"),
            f"L{length} blind history",
        )
        audit = repo_file(
            repo_root,
            entry.get("hostile_audit_path"),
            entry.get("hostile_audit_sha256"),
            f"L{length} hostile audit",
        )
        demand(
            entry.get("hostile_verdict") == "PASS",
            f"L{length}: hostile verdict not PASS",
        )
        audit_text = audit.read_text(encoding="utf-8")
        demand(
            "PASS" in audit_text
            and str(entry.get("target_history_sha256")) in audit_text
            and str(entry.get("blind_history_sha256")) in audit_text,
            f"L{length}: hostile audit does not bind both histories",
        )

    lineage = manifest.get("stage2_benchmark_lineage")
    demand(
        isinstance(lineage, dict)
        and set(lineage) == {
            "policy", "authorities", "chosen_history_comparisons", "tolerance",
        }
        and lineage.get("policy")
        == "AUDITED_SCALABLE_L4_L10_HISTORIES_BRIDGED_TO_CURRENT_STAGE2_AND_A18"
        and lineage.get("tolerance") == 1.0e-8,
        "manifest Stage2 benchmark lineage identity mismatch",
    )
    authorities = lineage.get("authorities")
    authority_labels = {
        "target_L4", "target_L6", "target_L8", "target_L10", "hostile_L10",
        "control_audit", "l10_audit", "a18_cross_gate",
    }
    demand(
        isinstance(authorities, dict) and set(authorities) == authority_labels,
        "manifest Stage2 benchmark authority census mismatch",
    )
    for label, binding in authorities.items():
        demand(
            isinstance(binding, dict) and set(binding) == {"path", "sha256"},
            f"manifest Stage2 {label} authority malformed",
        )
        repo_file(
            repo_root, binding.get("path"), binding.get("sha256"),
            f"manifest Stage2 {label} authority",
        )
    comparisons = lineage.get("chosen_history_comparisons")
    comparison_labels = {"4", "6", "8", "10", "hostile_L10"}
    demand(
        isinstance(comparisons, dict) and set(comparisons) == comparison_labels,
        "manifest Stage2 comparison census mismatch",
    )
    for label, comparison in comparisons.items():
        demand(
            isinstance(comparison, dict)
            and set(comparison) == {
                "max_sector_weight_difference",
                "max_history_observable_difference",
            },
            f"manifest Stage2 {label} comparison malformed",
        )
        for name, raw in comparison.items():
            demand(
                type(raw) in (int, float) and math.isfinite(float(raw))
                and 0.0 <= float(raw) <= 1.0e-8,
                f"manifest Stage2 {label} {name} exceeds the bridge tolerance",
            )

    atoms = manifest.get("atoms")
    demand(isinstance(atoms, list) and atoms, "manifest atom partition absent")
    common = manifest.get("I_acc")
    demand(
        isinstance(common, list) and len(common) == 2,
        "manifest I_acc absent",
    )
    common_left = Fraction(*reduced_pair(common[0], "I_acc.left"))
    common_right = Fraction(*reduced_pair(common[1], "I_acc.right"))
    demand(common_left < common_right, "manifest I_acc has no positive width")
    seen: set[str] = set()
    previous_right: Fraction | None = None
    normalized_atoms: list[dict[str, object]] = []
    for ordinal, atom in enumerate(atoms):
        demand(isinstance(atom, dict), "manifest atom is not an object")
        demand(
            set(atom) == {"atom_id", "density_interval", "q_by_L"},
            "manifest atom key census mismatch",
        )
        atom_id = atom.get("atom_id")
        demand(
            isinstance(atom_id, str) and atom_id and atom_id not in seen,
            "atom ID census mismatch",
        )
        seen.add(atom_id)
        interval = atom.get("density_interval")
        demand(
            isinstance(interval, list) and len(interval) == 2,
            f"{atom_id}: interval absent",
        )
        left_pair = reduced_pair(interval[0], f"{atom_id}.left")
        right_pair = reduced_pair(interval[1], f"{atom_id}.right")
        left, right = Fraction(*left_pair), Fraction(*right_pair)
        demand(left < right, f"{atom_id}: non-positive width")
        demand(
            previous_right is None or previous_right == left,
            "atom partition gap/reorder",
        )
        if ordinal == 0:
            demand(left == common_left, "atom partition does not begin at I_acc")
        previous_right = right
        qmap = atom.get("q_by_L")
        demand(
            isinstance(qmap, dict)
            and set(qmap) == {str(length) for length in SIZES},
            f"{atom_id}: q census",
        )
        midpoint = (left + right) / 2
        normalized_q: dict[str, int] = {}
        for length in SIZES:
            value = qmap[str(length)]
            demand(
                type(value) is int and 0 <= value <= length,
                f"{atom_id}: invalid L{length} q",
            )
            demand(
                value == q_at_density(length, midpoint),
                f"{atom_id}: L{length} q not reconstructed",
            )
            normalized_q[str(length)] = value
        normalized_atoms.append(
            {
                "atom_id": atom_id,
                "density_interval": [list(left_pair), list(right_pair)],
                "q_by_L": normalized_q,
            }
        )
    demand(previous_right == common_right, "atom partition does not end at I_acc")
    demand(
        normalized_atoms == exact_atom_partition(common_left, common_right),
        "atom partition is not the exact complete boundary partition",
    )
    return {
        "manifest": manifest,
        "atoms": normalized_atoms,
        "manifest_sha256": manifest_sha256,
    }


def reconstruct_sector_plan(
    repo_root: Path,
    manifest_path: Path,
    manifest_sha256: str,
) -> dict[str, object]:
    validated = validate_authenticated_manifest(
        repo_root, manifest_path, manifest_sha256
    )
    atoms = validated["atoms"]
    demand(isinstance(atoms, list), "validated atom census malformed")
    planned = sorted(
        {
            (length, int(atom["q_by_L"][str(length)]))
            for atom in atoms
            for length in LARGE_SIZES
            if int(atom["q_by_L"][str(length)]) > 0
        }
    )
    zero = sorted(
        [
            {"atom_id": str(atom["atom_id"]), "L": length, "q": 0}
            for atom in atoms
            for length in SIZES
            if int(atom["q_by_L"][str(length)]) == 0
        ],
        key=lambda row: (str(row["atom_id"]), int(row["L"])),
    )
    return {
        "schema": PLAN_SCHEMA,
        "status": PLAN_STATUS,
        "manifest_path": repo_relative(
            repo_root, manifest_path, "accumulation manifest"
        ),
        "manifest_sha256": manifest_sha256,
        "accumulation_protocol_sha256": ACCUMULATION_PROTOCOL_SHA256,
        "planned_sectors": [list(pair) for pair in planned],
        "zero_response_dispositions": zero,
        "atoms": atoms,
        "claim_boundary": (
            "DETERMINISTIC_SECTOR_PLAN_ONLY__NO_SPECTRUM_OR_GRAVITY_RESULT"
        ),
    }
