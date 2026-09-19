#!/usr/bin/env python3
"""Minimum V004 boundary successor for the frozen V003 restart.

This layer changes no publisher action or payload rule.  It reuses the exact
V003 transaction while authenticating the already-bound A01--A04/A27 records
and twelve absences immediately before and after the cache-parent rename and
receipt publication.  These are explicit transaction-boundary checks, not a
claim of continuous exclusion against arbitrary noncooperative writers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import types
from pathlib import Path, PurePosixPath
from typing import Final, Mapping


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
V003_PATH: Final[Path] = HERE / "replay_a01_a18_v003.py"
V003_MODULE_NAME: Final[str] = "authenticated_replay_a01_a18_v003"
PINNED_V003_PACKET: Final[dict[str, str]] = {
    "replay_a01_a18_v003.py":
        "7b7d548ba6a01c379986c71291ba3bc28e3da30cd3f92ae150029a88aaac0f8b",
    "test_replay_a01_a18_v003.py":
        "d2de9ab3a31d205f38dfbc25e4c4977a8e86c90f5a27f72eb46a791a7775fc07",
    "FAILED_CACHE_OBSTRUCTION_CENSUS_V003.json":
        "2f14a2380991efcc46ea139b7271be16acc1392f3b1c2fa186d20954b98394b5",
    "REPLAY_SOURCE_FREEZE_V003.json":
        "b94afc1a41ff2e637d6e1d9ffcf2495786fc0022d80615bee5c59eb93cb50880",
    "REPLAY_CANDIDATE_RESULT_V003.json":
        "500711e99807ac5eb80647690329fcb6f7f56981c65f480cf14bc66125a4759f",
}
V004_AUTHORIZATION: Final[str] = (
    "EXECUTE_EXACT_TRANSACTION_BOUNDARY_RECHECK_REPLAY_V004"
)


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _read_frozen_packet_file(name: str) -> bytes:
    if name not in PINNED_V003_PACKET:
        raise RuntimeError("unregistered frozen V003 packet member")
    path = HERE / name
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_nlink != 1 or before.st_mode & 0o222
            or _identity(before) != _identity(named)
        ):
            raise RuntimeError(f"frozen V003 packet custody mismatch: {name}")
        digest = hashlib.sha256()
        raw = bytearray()
        offset = 0
        while True:
            block = os.pread(descriptor, 16 * 2**20, offset)
            if not block:
                break
            raw.extend(block)
            digest.update(block)
            offset += len(block)
        after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
        if (
            _identity(before) != _identity(after)
            or _identity(after) != _identity(named_after)
            or digest.hexdigest() != PINNED_V003_PACKET[name]
        ):
            raise RuntimeError(f"frozen V003 packet digest mismatch: {name}")
        return bytes(raw)
    finally:
        os.close(descriptor)


def _load_v003() -> types.ModuleType:
    for name in PINNED_V003_PACKET:
        _read_frozen_packet_file(name)
    existing = sys.modules.get(V003_MODULE_NAME)
    if existing is not None:
        if (
            getattr(existing, "__file__", None) != str(V003_PATH)
            or getattr(existing, "__authenticated_sha256__", None)
            != PINNED_V003_PACKET[V003_PATH.name]
        ):
            raise RuntimeError("frozen V003 replay module alias")
        return existing
    raw = _read_frozen_packet_file(V003_PATH.name)
    module = types.ModuleType(V003_MODULE_NAME)
    module.__file__ = str(V003_PATH)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = PINNED_V003_PACKET[V003_PATH.name]
    sys.modules[V003_MODULE_NAME] = module
    try:
        exec(compile(raw, str(V003_PATH), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(V003_MODULE_NAME, None)
        raise
    for name in PINNED_V003_PACKET:
        _read_frozen_packet_file(name)
    return module


v003 = _load_v003()
v002 = v003.v002
v001 = v003.v001
retirement = v003.retirement
Refusal = v003.Refusal
ORIGINAL_V003_RETIRE_FAILED_CACHE: Final[object] = v003.retire_failed_cache
ORIGINAL_RENAME_EXCLUSIVE: Final[object] = retirement.rename_exclusive
ORIGINAL_PUBLISH_ONCE: Final[object] = retirement.publish_once


def _authenticate_explicit_boundary(
    root: Path, census: Mapping[str, object], label: str,
) -> None:
    """Authenticate the exact frozen records and all twelve current absences."""
    try:
        v003.authenticate_restart_boundary(root, census, require_absences=True)
    except (OSError, RuntimeError, ValueError, Refusal) as error:
        raise Refusal(f"{label}: {error}") from error


def retire_failed_cache(
    root: Path, census: dict[str, object], *, inject_at: str | None = None,
    test_rename_primitive: object | None = None,
    test_publish_primitive: object | None = None,
) -> dict[str, object]:
    """Execute V003 with explicit checks around its rename and receipt calls."""
    if root == ROOT and (
        test_rename_primitive is not None or test_publish_primitive is not None
    ):
        raise Refusal("V004 test primitive is forbidden at the canonical root")
    status = v003.transaction_status(root, census)
    if status.startswith("PASS_COMPLETED_CUSTODY"):
        # A later replay may legitimately contain A06 or histories.  V003
        # authenticates the completed receipt and distinct rebuilt parent and
        # then defers their exact reconciliation to the existing V001 policy.
        return ORIGINAL_V003_RETIRE_FAILED_CACHE(
            root, census, inject_at=inject_at,
        )
    _authenticate_explicit_boundary(root, census, "V004 transaction entry")
    _source, _custody, _target, _intent_path, receipt_path = (
        v003._transaction_paths(root, census)
    )
    prior_rename = retirement.rename_exclusive
    prior_publish = retirement.publish_once
    if prior_rename is not ORIGINAL_RENAME_EXCLUSIVE:
        raise Refusal("V004 rename primitive was already replaced")
    if prior_publish is not ORIGINAL_PUBLISH_ONCE:
        raise Refusal("V004 publication primitive was already replaced")
    rename_primitive = (
        ORIGINAL_RENAME_EXCLUSIVE
        if test_rename_primitive is None else test_rename_primitive
    )
    publish_primitive = (
        ORIGINAL_PUBLISH_ONCE
        if test_publish_primitive is None else test_publish_primitive
    )
    if not callable(rename_primitive) or not callable(publish_primitive):
        raise Refusal("V004 test primitive is not callable")

    def guarded_rename(source: Path, target: Path) -> None:
        _authenticate_explicit_boundary(root, census, "V004 pre-rename boundary")
        rename_primitive(source, target)
        _authenticate_explicit_boundary(root, census, "V004 post-rename boundary")

    def guarded_publish(path: Path, record: dict[str, object]) -> str:
        if path != receipt_path:
            return publish_primitive(path, record)
        _authenticate_explicit_boundary(root, census, "V004 pre-receipt boundary")
        digest = publish_primitive(path, record)
        _authenticate_explicit_boundary(root, census, "V004 post-receipt boundary")
        return digest

    retirement.rename_exclusive = guarded_rename
    retirement.publish_once = guarded_publish
    try:
        result = ORIGINAL_V003_RETIRE_FAILED_CACHE(
            root, census, inject_at=inject_at,
        )
    finally:
        retirement.rename_exclusive = prior_rename
        retirement.publish_once = prior_publish
    _authenticate_explicit_boundary(root, census, "V004 pre-V002 boundary")
    return result


def coordinate_canonical_a01_a18_replay(
    expected_retirement_receipt_sha256: str,
    expected_failed_cache_receipt_sha256: str,
) -> dict[tuple[str, int], str]:
    """Use the authenticated V003 entry with only its transaction tightened."""
    previous = v003.retire_failed_cache
    if previous is not ORIGINAL_V003_RETIRE_FAILED_CACHE:
        raise Refusal("frozen V003 retirement entry was already replaced")
    v003.retire_failed_cache = retire_failed_cache
    try:
        return v003.coordinate_canonical_a01_a18_replay(
            expected_retirement_receipt_sha256,
            expected_failed_cache_receipt_sha256,
        )
    finally:
        v003.retire_failed_cache = previous


def replay_plan() -> dict[str, object]:
    predecessor = v003.replay_plan()
    return {
        "classification": "BOUNDED_NONEXECUTED_V004_BOUNDARY_RECHECK_PLAN",
        "predecessor_plan": predecessor,
        "predecessor_source_sha256": PINNED_V003_PACKET[V003_PATH.name],
        "explicit_absence_boundary_count": 4,
        "explicit_absence_boundaries": [
            "IMMEDIATELY_BEFORE_RENAME",
            "IMMEDIATELY_AFTER_RENAME_BEFORE_FSYNC_OR_RECEIPT",
            "IMMEDIATELY_BEFORE_RECEIPT",
            "IMMEDIATELY_AFTER_RECEIPT_BEFORE_V002",
        ],
        "bound_record_count": len(v003.RESTART_BOUNDARY_SHA256),
        "bound_absence_count": len(v003.REQUIRED_ABSENT_BEFORE_CUSTODY),
        "general_lock_or_continuous_exclusion_claim": False,
        "canonical_action_executed": False,
        "claim_boundary": (
            "EXPLICIT_TRANSACTION_BOUNDARY_AUTHENTICATION_ONLY__NO_CONTINUOUS_"
            "EXTERNAL_WRITER_EXCLUSION_PAYLOAD_PHYSICS_HISTORY_A18_L12_"
            "SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true")
    action.add_argument("--execute-canonical", action="store_true")
    parser.add_argument("--retirement-receipt-sha256")
    parser.add_argument("--failed-cache-receipt-sha256")
    parser.add_argument("--authorization")
    parser.add_argument("--v003-authorization")
    parser.add_argument("--v004-authorization")
    arguments = parser.parse_args()
    try:
        fields = (
            arguments.retirement_receipt_sha256,
            arguments.failed_cache_receipt_sha256,
            arguments.authorization,
            arguments.v003_authorization,
            arguments.v004_authorization,
        )
        if arguments.plan:
            if any(fields):
                raise Refusal("plan mode rejects execution authorization fields")
            result: object = replay_plan()
        else:
            if arguments.authorization != v003.ORIGINAL_AUTHORIZATION:
                raise Refusal("original exact replay authorization string is absent")
            if arguments.v003_authorization != v003.V003_AUTHORIZATION:
                raise Refusal("V003 custody/restart authorization string is absent")
            if arguments.v004_authorization != V004_AUTHORIZATION:
                raise Refusal("V004 boundary-recheck authorization string is absent")
            if arguments.retirement_receipt_sha256 is None:
                raise Refusal("retirement receipt hash is absent")
            if arguments.failed_cache_receipt_sha256 is None:
                raise Refusal("failed-cache custody receipt hash is absent")
            products = coordinate_canonical_a01_a18_replay(
                arguments.retirement_receipt_sha256,
                arguments.failed_cache_receipt_sha256,
            )
            result = {
                "classification": "PASS_EXACT_V004_A01_A18_CANONICAL_REPLAY",
                "products": {
                    f"{artifact_id}/{instance}": digest
                    for (artifact_id, instance), digest in sorted(products.items())
                },
                "claim_boundary": (
                    "FINITE_CONTROL_L10_RECERTIFICATION_ONLY__NO_L12_SPECTRUM_"
                    "CONTINUUM_OR_GRAVITY_RESULT"
                ),
            }
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError, Refusal) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
