#!/usr/bin/env python3
"""Minimum monotone-prefix successor for the frozen V005 replay adapter.

V005 authenticated every observed canonical A11/A12/A13/A15/A16 prefix, but
its lower bound remained the prefix present when the review was constructed.
This wrapper adds one monotone high-water counter: after a longer exact prefix
is observed and authenticated, a shorter prefix is a refusal.  Nothing else in
the frozen staged-path adapter or replay DAG is changed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import types
from pathlib import Path
from typing import Final


HERE: Final[Path] = Path(__file__).resolve().parent
V005_PATH: Final[Path] = HERE / "replay_a01_a18_v005.py"
V005_MODULE_NAME: Final[str] = "authenticated_replay_a01_a18_v005"
PINNED_V005_PACKET: Final[dict[str, str]] = {
    "replay_a01_a18_v005.py":
        "d9f75788b10c8cd16180cf66511e926868602f7b7b35c588b46cc793fa5f82a3",
    "test_replay_a01_a18_v005.py":
        "19a0cb371931a236b300a3e690c3f02240b7ce85c536f1337acdf0d4b12914c7",
    "REPLAY_SOURCE_FREEZE_V005.json":
        "ff8c8d903001d5ba6be177bb465238c2bf35146c2c4dd1d0a0374282218dde83",
    "REPLAY_CANDIDATE_RESULT_V005.json":
        "14b3225201e051975a0d70bdc7d922382aaeb497354d6990bcdf7db355f66da4",
}
V006_AUTHORIZATION: Final[str] = (
    "EXECUTE_EXACT_MONOTONE_CANONICAL_PREFIX_REPLAY_V006"
)


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _read_frozen_packet_file(name: str) -> bytes:
    if name not in PINNED_V005_PACKET:
        raise RuntimeError("unregistered frozen V005 packet member")
    path = HERE / name
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
            or before.st_nlink != 1 or before.st_mode & 0o222
            or _identity(before) != _identity(named)
        ):
            raise RuntimeError(f"frozen V005 packet custody mismatch: {name}")
        raw = bytearray()
        digest = hashlib.sha256()
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
            or digest.hexdigest() != PINNED_V005_PACKET[name]
        ):
            raise RuntimeError(f"frozen V005 packet digest mismatch: {name}")
        return bytes(raw)
    finally:
        os.close(descriptor)


def _load_v005() -> types.ModuleType:
    for name in PINNED_V005_PACKET:
        _read_frozen_packet_file(name)
    existing = sys.modules.get(V005_MODULE_NAME)
    if existing is not None:
        if (
            getattr(existing, "__file__", None) != str(V005_PATH)
            or getattr(existing, "__authenticated_sha256__", None)
            != PINNED_V005_PACKET[V005_PATH.name]
        ):
            raise RuntimeError("frozen V005 replay module alias")
        return existing
    raw = _read_frozen_packet_file(V005_PATH.name)
    module = types.ModuleType(V005_MODULE_NAME)
    module.__file__ = str(V005_PATH)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = PINNED_V005_PACKET[V005_PATH.name]
    sys.modules[V005_MODULE_NAME] = module
    try:
        exec(compile(raw, str(V005_PATH), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(V005_MODULE_NAME, None)
        raise
    for name in PINNED_V005_PACKET:
        _read_frozen_packet_file(name)
    return module


v005 = _load_v005()
v004 = v005.v004
v003 = v005.v003
v002 = v005.v002
v001 = v005.v001
retirement = v005.retirement
Refusal = v005.Refusal
ORIGINAL_V002_REVIEW: Final[object] = v005.ORIGINAL_V002_REVIEW


class MonotoneStagedPathReview(v005.StagedPathReview):
    """Require every successfully observed canonical prefix to be retained."""

    def __init__(self, root: Path):
        self._canonical_high_water: int | None = None
        super().__init__(root)
        if self._canonical_high_water != self._entry_prefix_count:
            self.close()
            raise Refusal("V006 canonical high-water initialization mismatch")

    def _presence_snapshot(self) -> tuple[bool, ...]:
        return tuple(
            retirement.path_exists(self._canonical_path(artifact_id))
            for artifact_id in v005.CANONICAL_ORDER
        )

    def _assert_canonical_state(self) -> None:
        before = self._presence_snapshot()
        super()._assert_canonical_state()
        after = self._presence_snapshot()
        if before != after:
            raise Refusal("V006 canonical prefix changed across authentication")
        present = sum(after)
        high_water = self._canonical_high_water
        if high_water is None:
            if present != self._entry_prefix_count:
                raise Refusal("V006 initial canonical prefix mismatch")
            self._canonical_high_water = present
        elif present < high_water:
            raise Refusal("V006 authenticated canonical prefix disappeared")
        elif present > high_water:
            # V005 returned only after authenticating exact bytes, inode, prefix
            # order, closed-batch eligibility, and candidate equality.
            self._canonical_high_water = present


_CAPTURE_COORDINATE_REVIEW = False
_ACTIVE_COORDINATE_REVIEW: MonotoneStagedPathReview | None = None


class CoordinateMonotoneStagedPathReview(MonotoneStagedPathReview):
    """Capture the sole live review for unconditional close/restoration."""

    def __init__(self, root: Path):
        global _ACTIVE_COORDINATE_REVIEW
        if not _CAPTURE_COORDINATE_REVIEW or _ACTIVE_COORDINATE_REVIEW is not None:
            raise Refusal("V006 coordinate review lifetime mismatch")
        super().__init__(root)
        _ACTIVE_COORDINATE_REVIEW = self


def coordinate_canonical_a01_a18_replay(
    expected_retirement_receipt_sha256: str,
    expected_failed_cache_receipt_sha256: str,
) -> dict[tuple[str, int], str]:
    """Run V004 with the exact V005 adapter plus monotone prefix custody."""
    global _ACTIVE_COORDINATE_REVIEW, _CAPTURE_COORDINATE_REVIEW
    previous = v002.ExactLiveReview
    if previous is not ORIGINAL_V002_REVIEW:
        raise Refusal("frozen V002 review class was already replaced")
    if _CAPTURE_COORDINATE_REVIEW or _ACTIVE_COORDINATE_REVIEW is not None:
        raise Refusal("V006 coordinate is already active")
    _CAPTURE_COORDINATE_REVIEW = True
    v002.ExactLiveReview = CoordinateMonotoneStagedPathReview
    try:
        return v004.coordinate_canonical_a01_a18_replay(
            expected_retirement_receipt_sha256,
            expected_failed_cache_receipt_sha256,
        )
    finally:
        v002.ExactLiveReview = previous
        review = _ACTIVE_COORDINATE_REVIEW
        _ACTIVE_COORDINATE_REVIEW = None
        _CAPTURE_COORDINATE_REVIEW = False
        if review is not None:
            review.close()


def replay_plan() -> dict[str, object]:
    return {
        "classification": "BOUNDED_NONEXECUTED_V006_MONOTONE_PREFIX_PLAN",
        "predecessor_plan": v005.replay_plan(),
        "predecessor_source_sha256": PINNED_V005_PACKET[V005_PATH.name],
        "canonical_prefix_order": list(v005.CANONICAL_ORDER),
        "high_water_initialized_from_entry_prefix": True,
        "high_water_advances_after_exact_v005_authentication_only": True,
        "authenticated_prefix_deletion_accepted": False,
        "other_v005_behavior_changed": False,
        "canonical_action_executed": False,
        "claim_boundary": (
            "REPLAY_ONLY_CANONICAL_PREFIX_MONOTONICITY_AT_EXPLICIT_CHECK_"
            "BOUNDARIES__NO_CONTINUOUS_EXTERNAL_WRITER_EXCLUSION_ACTION_SOURCE_"
            "HISTORY_PHYSICS_THRESHOLD_A18_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_"
            "RESULT"
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
    parser.add_argument("--v005-authorization")
    parser.add_argument("--v006-authorization")
    arguments = parser.parse_args()
    try:
        fields = (
            arguments.retirement_receipt_sha256,
            arguments.failed_cache_receipt_sha256,
            arguments.authorization,
            arguments.v003_authorization,
            arguments.v004_authorization,
            arguments.v005_authorization,
            arguments.v006_authorization,
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
            if arguments.v004_authorization != v004.V004_AUTHORIZATION:
                raise Refusal("V004 boundary-recheck authorization string is absent")
            if arguments.v005_authorization != v005.V005_AUTHORIZATION:
                raise Refusal("V005 staged-path authorization string is absent")
            if arguments.v006_authorization != V006_AUTHORIZATION:
                raise Refusal("V006 monotone-prefix authorization string is absent")
            if arguments.retirement_receipt_sha256 is None:
                raise Refusal("retirement receipt hash is absent")
            if arguments.failed_cache_receipt_sha256 is None:
                raise Refusal("failed-cache custody receipt hash is absent")
            products = coordinate_canonical_a01_a18_replay(
                arguments.retirement_receipt_sha256,
                arguments.failed_cache_receipt_sha256,
            )
            result = {
                "classification": "PASS_EXACT_V006_A01_A18_CANONICAL_REPLAY",
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


def __getattr__(name: str) -> object:
    return getattr(v005, name)


if __name__ == "__main__":
    raise SystemExit(main())
