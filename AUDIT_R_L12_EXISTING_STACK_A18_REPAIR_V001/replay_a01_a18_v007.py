#!/usr/bin/env python3
"""Minimum A18-parent custody successor for the frozen V006 replay.

V006 reaches a fully validated A18 candidate, but V001 intentionally refuses
publication when the single canonical parent directory is absent.  This layer
creates or reconciles only that replay-owned ordinary parent, retains its
descriptor identity, and guards the exact V001 A18 reconciliation boundary.
It changes no record, sink, publisher order, history, formula, or threshold.
"""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import stat
import sys
import types
from pathlib import Path, PurePosixPath
from typing import Callable, Final, Mapping, Sequence


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
V006_PATH: Final[Path] = HERE / "replay_a01_a18_v006.py"
V006_MODULE_NAME: Final[str] = "authenticated_replay_a01_a18_v006"
PINNED_V006_PACKET: Final[dict[str, str]] = {
    "replay_a01_a18_v006.py":
        "4ae065b4321b8f800deddf3750b5272ca9c6c755ab582105eaaf856794a680d7",
    "test_replay_a01_a18_v006.py":
        "0f127ecaee48179e2cd3c9f2b1af0bbd8026c6357ef9fd6a4d88cb53e56652ad",
    "REPLAY_SOURCE_FREEZE_V006.json":
        "f4afb17a34a9bca730999696036c38be8c8749ea5ea793b2c6ea5bb38d994008",
    "REPLAY_CANDIDATE_RESULT_V006.json":
        "0f7f6e030ca8ce27b576eebe54e2c3ec9e3ee3083922f4e80ad45fb1e963d8a5",
}
V007_AUTHORIZATION: Final[str] = (
    "EXECUTE_EXACT_REPLAY_OWNED_A18_PARENT_CUSTODY_V007"
)
PARENT_RELATIVE: Final[PurePosixPath] = PurePosixPath(
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
)
A18_NAME: Final[str] = "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
PARENT_MODE: Final[int] = 0o755
EXPECTED_CANONICAL_A18_SHA256: Final[str] = (
    "84a99de5d97373f8daeb2a1bcf1adcf04d2f0e0ee17dab13f58859d35bf141c5"
)


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _read_frozen_packet_file(name: str) -> bytes:
    if name not in PINNED_V006_PACKET:
        raise RuntimeError("unregistered frozen V006 packet member")
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
            raise RuntimeError(f"frozen V006 packet custody mismatch: {name}")
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
            or digest.hexdigest() != PINNED_V006_PACKET[name]
        ):
            raise RuntimeError(f"frozen V006 packet digest mismatch: {name}")
        return bytes(raw)
    finally:
        os.close(descriptor)


def _load_v006() -> types.ModuleType:
    for name in PINNED_V006_PACKET:
        _read_frozen_packet_file(name)
    existing = sys.modules.get(V006_MODULE_NAME)
    if existing is not None:
        if (
            getattr(existing, "__file__", None) != str(V006_PATH)
            or getattr(existing, "__authenticated_sha256__", None)
            != PINNED_V006_PACKET[V006_PATH.name]
        ):
            raise RuntimeError("frozen V006 replay module alias")
        return existing
    raw = _read_frozen_packet_file(V006_PATH.name)
    module = types.ModuleType(V006_MODULE_NAME)
    module.__file__ = str(V006_PATH)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = PINNED_V006_PACKET[V006_PATH.name]
    sys.modules[V006_MODULE_NAME] = module
    try:
        exec(compile(raw, str(V006_PATH), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(V006_MODULE_NAME, None)
        raise
    for name in PINNED_V006_PACKET:
        _read_frozen_packet_file(name)
    return module


v006 = _load_v006()
v005 = v006.v005
v004 = v006.v004
v003 = v006.v003
v002 = v006.v002
v001 = v006.v001
retirement = v006.retirement
Refusal = v006.Refusal
ORIGINAL_A18_RECONCILE: Final[object] = v001._reconcile_or_publish_json

# Derive rather than duplicate the V001 destination contract.
_a18_pure = PurePosixPath(v001.A18_CANONICAL_PATH)
if _a18_pure.parent != PARENT_RELATIVE or _a18_pure.name != A18_NAME:
    raise RuntimeError("V007 A18 parent/name differs from frozen V001")


class A18ParentCustody:
    """Retain one ordinary parent and its empty-or-single-A18 child census."""

    def __init__(
        self, root: Path, root_descriptor: int, parent_descriptor: int,
        root_identity: tuple[int, int, int], *, created: bool,
    ):
        self.root = root
        self.path = root.joinpath(*PARENT_RELATIVE.parts)
        self.root_descriptor = root_descriptor
        self.root_identity = root_identity
        self.parent_descriptor = parent_descriptor
        self.created = created
        self.closed = False
        parent = os.fstat(parent_descriptor)
        self.parent_identity = (parent.st_dev, parent.st_ino, parent.st_mode)
        self.a18_identity: tuple[int, ...] | None = None
        self.a18_sha256: str | None = None
        state = self.authenticate_boundary(allow_transition=False)
        self.entry_state = state

    @classmethod
    def acquire(cls, root: Path) -> "A18ParentCustody":
        try:
            retirement.ensure_root(root)
        except (OSError, RuntimeError, ValueError) as error:
            raise Refusal("V007 repository root custody mismatch") from error
        if len(PARENT_RELATIVE.parts) != 1:
            raise Refusal("V007 A18 parent is not one canonical component")
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        root_descriptor = -1
        parent_descriptor = -1
        created = False
        try:
            root_descriptor = os.open(root, flags)
            root_before = os.fstat(root_descriptor)
            root_named = os.stat(root, follow_symlinks=False)
            if (
                not stat.S_ISDIR(root_before.st_mode)
                or stat.S_ISLNK(root_named.st_mode)
                or _identity(root_before) != _identity(root_named)
            ):
                raise Refusal("V007 repository root descriptor mismatch")
            root_identity = (
                root_before.st_dev, root_before.st_ino, root_before.st_mode,
            )
            name = PARENT_RELATIVE.name
            try:
                os.mkdir(name, PARENT_MODE, dir_fd=root_descriptor)
                os.fsync(root_descriptor)
                created = True
            except FileExistsError:
                pass
            except OSError as error:
                if error.errno != errno.EEXIST:
                    raise
            parent_descriptor = os.open(name, flags, dir_fd=root_descriptor)
            if created:
                os.fchmod(parent_descriptor, PARENT_MODE)
                os.fsync(parent_descriptor)
                os.fsync(root_descriptor)
            custody = cls(
                root, root_descriptor, parent_descriptor, root_identity,
                created=created,
            )
            root_descriptor = -1
            parent_descriptor = -1
            return custody
        except (OSError, RuntimeError, ValueError, Refusal) as error:
            if isinstance(error, Refusal):
                raise
            raise Refusal("V007 A18 parent acquisition failed") from error
        finally:
            if parent_descriptor >= 0:
                os.close(parent_descriptor)
            if root_descriptor >= 0:
                os.close(root_descriptor)

    def _assert_open(self) -> None:
        if self.closed:
            raise Refusal("V007 A18 parent custody is closed")

    def _authenticate_root(self) -> None:
        self._assert_open()
        try:
            held = os.fstat(self.root_descriptor)
            named = os.stat(self.root, follow_symlinks=False)
        except OSError as error:
            raise Refusal("V007 repository root descriptor lookup failed") from error
        held_identity = (held.st_dev, held.st_ino, held.st_mode)
        named_identity = (named.st_dev, named.st_ino, named.st_mode)
        if (
            not stat.S_ISDIR(held.st_mode) or stat.S_ISLNK(named.st_mode)
            or held_identity != self.root_identity
            or named_identity != self.root_identity
        ):
            raise Refusal("V007 repository root dev/inode/mode identity mismatch")

    def _authenticate_parent(self) -> None:
        self._assert_open()
        self._authenticate_root()
        try:
            held = os.fstat(self.parent_descriptor)
            named = os.stat(
                PARENT_RELATIVE.name, dir_fd=self.root_descriptor,
                follow_symlinks=False,
            )
        except OSError as error:
            raise Refusal("V007 A18 parent descriptor lookup failed") from error
        identity = (held.st_dev, held.st_ino, held.st_mode)
        named_identity = (named.st_dev, named.st_ino, named.st_mode)
        if (
            not stat.S_ISDIR(held.st_mode) or stat.S_ISLNK(named.st_mode)
            or stat.S_IMODE(held.st_mode) != PARENT_MODE
            or identity != self.parent_identity or identity != named_identity
        ):
            raise Refusal("V007 A18 parent descriptor/mode identity mismatch")

    def _authenticate_a18(self) -> tuple[tuple[int, ...], str]:
        flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = -1
        try:
            descriptor = os.open(A18_NAME, flags, dir_fd=self.parent_descriptor)
            before = os.fstat(descriptor)
            named = os.stat(
                A18_NAME, dir_fd=self.parent_descriptor, follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
                or before.st_nlink != 1 or before.st_mode & 0o222
                or _identity(before) != _identity(named)
            ):
                raise Refusal("V007 A18 child is not owner-once")
            raw = bytearray()
            offset = 0
            while True:
                block = os.pread(descriptor, 16 * 2**20, offset)
                if not block:
                    break
                raw.extend(block)
                offset += len(block)
            retirement.strict_json(bytes(raw), "V007 A18 child")
            digest = retirement.sha256_bytes(bytes(raw))
            if self.root == ROOT and digest != EXPECTED_CANONICAL_A18_SHA256:
                raise Refusal("V007 canonical A18 child digest mismatch")
            after = os.fstat(descriptor)
            named_after = os.stat(
                A18_NAME, dir_fd=self.parent_descriptor, follow_symlinks=False,
            )
            if (
                _identity(before) != _identity(after)
                or _identity(after) != _identity(named_after)
                or retirement.descriptor_sha256(descriptor) != digest
            ):
                raise Refusal("V007 A18 child changed while held")
            return _identity(before), digest
        except OSError as error:
            raise Refusal("V007 A18 child open failed") from error
        finally:
            if descriptor >= 0:
                os.close(descriptor)

    def authenticate_boundary(self, *, allow_transition: bool) -> str:
        self._authenticate_parent()
        try:
            names = tuple(sorted(os.listdir(self.parent_descriptor)))
        except OSError as error:
            raise Refusal("V007 A18 parent child census failed") from error
        if names == ():
            if self.a18_identity is not None:
                raise Refusal("V007 authenticated A18 child disappeared")
            return "EMPTY_PRE_A18"
        if names != (A18_NAME,):
            raise Refusal("V007 A18 parent contains an unregistered child")
        identity, digest = self._authenticate_a18()
        if self.a18_identity is None:
            if not allow_transition and hasattr(self, "entry_state"):
                raise Refusal("V007 A18 child appeared outside publication boundary")
            self.a18_identity = identity
            self.a18_sha256 = digest
        elif identity != self.a18_identity or digest != self.a18_sha256:
            raise Refusal("V007 A18 child identity/hash changed")
        return "A18_ONLY"

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            os.close(self.parent_descriptor)
        finally:
            os.close(self.root_descriptor)


def _guarded_reconcile(
    custody: A18ParentCustody,
    original: Callable[..., tuple[str, bool]],
    path: Path,
    record: Mapping[str, object],
    artifact_id: str,
    sinks: Sequence[Callable[[str, Mapping[str, object]], None]],
) -> tuple[str, bool]:
    expected = custody.path / A18_NAME
    if artifact_id != "A18_L10_CROSS_GATE" or path != expected:
        if artifact_id == "A18_L10_CROSS_GATE" or path == expected:
            raise Refusal("V007 A18 publication identity/path mismatch")
        return original(path, record, artifact_id, sinks)
    input_sha256 = retirement.sha256_bytes(
        retirement.publication_json_bytes(dict(record))
    )
    if custody.root == ROOT and input_sha256 != EXPECTED_CANONICAL_A18_SHA256:
        raise Refusal("V007 canonical A18 input digest mismatch")
    custody.authenticate_boundary(allow_transition=False)
    try:
        result = original(path, record, artifact_id, sinks)
    except BaseException:
        custody.authenticate_boundary(allow_transition=True)
        raise
    state = custody.authenticate_boundary(allow_transition=True)
    if (
        state != "A18_ONLY" or type(result) is not tuple or len(result) != 2
        or result[0] != custody.a18_sha256 or type(result[1]) is not bool
    ):
        raise Refusal("V007 A18 publication result/custody mismatch")
    if custody.root == ROOT and result[0] != EXPECTED_CANONICAL_A18_SHA256:
        raise Refusal("V007 canonical A18 publication digest mismatch")
    os.fsync(custody.parent_descriptor)
    custody.authenticate_boundary(allow_transition=False)
    return result


def coordinate_canonical_a01_a18_replay(
    expected_retirement_receipt_sha256: str,
    expected_failed_cache_receipt_sha256: str,
) -> dict[tuple[str, int], str]:
    """Add only the held A18 parent around the authenticated V006 replay."""
    previous = v001._reconcile_or_publish_json
    if previous is not ORIGINAL_A18_RECONCILE:
        raise Refusal("frozen V001 reconciliation primitive was already replaced")
    active_custody: A18ParentCustody | None = None
    a18_boundary_count = 0

    def guarded(
        path: Path,
        record: Mapping[str, object],
        artifact_id: str,
        sinks: Sequence[Callable[[str, Mapping[str, object]], None]],
    ) -> tuple[str, bool]:
        nonlocal active_custody, a18_boundary_count
        expected = ROOT.joinpath(*PARENT_RELATIVE.parts) / A18_NAME
        is_a18_artifact = artifact_id == "A18_L10_CROSS_GATE"
        is_a18_path = path == expected
        if not is_a18_artifact and not is_a18_path:
            return ORIGINAL_A18_RECONCILE(path, record, artifact_id, sinks)
        if not is_a18_artifact or not is_a18_path:
            raise Refusal("V007 A18 publication identity/path mismatch")
        if active_custody is not None or a18_boundary_count != 0:
            raise Refusal("V007 A18 publication boundary is reentrant")
        custody = A18ParentCustody.acquire(ROOT)
        active_custody = custody
        try:
            result = _guarded_reconcile(
                custody, ORIGINAL_A18_RECONCILE,
                path, record, artifact_id, sinks,
            )
            a18_boundary_count = 1
            return result
        finally:
            try:
                custody.authenticate_boundary(allow_transition=False)
            finally:
                custody.close()
                active_custody = None

    v001._reconcile_or_publish_json = guarded
    try:
        products = v006.coordinate_canonical_a01_a18_replay(
            expected_retirement_receipt_sha256,
            expected_failed_cache_receipt_sha256,
        )
        if (
            a18_boundary_count != 1
            or products.get(("A18_L10_CROSS_GATE", 1))
            != EXPECTED_CANONICAL_A18_SHA256
        ):
            raise Refusal("V007 completed replay lacks its exact A18 boundary")
        return products
    finally:
        v001._reconcile_or_publish_json = previous
        if active_custody is not None:
            try:
                active_custody.authenticate_boundary(allow_transition=False)
            finally:
                active_custody.close()
                active_custody = None


def parent_status() -> str:
    path = ROOT.joinpath(*PARENT_RELATIVE.parts)
    if not retirement.path_exists(path):
        return "ABSENT"
    try:
        metadata = os.stat(path, follow_symlinks=False)
    except OSError:
        return "PRESENT_UNREADABLE"
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        return "PRESENT_NONORDINARY"
    if stat.S_IMODE(metadata.st_mode) != PARENT_MODE:
        return "PRESENT_WRONG_MODE"
    try:
        names = tuple(sorted(child.name for child in path.iterdir()))
    except OSError:
        return "PRESENT_UNREADABLE"
    if names == ():
        return "EXACT_EMPTY"
    if names == (A18_NAME,):
        return "EXACT_NAME_CENSUS_A18_ONLY"
    return "PRESENT_UNREGISTERED_CHILD_CENSUS"


def replay_plan() -> dict[str, object]:
    return {
        "classification": "BOUNDED_NONEXECUTED_V007_A18_PARENT_CUSTODY_PLAN",
        "predecessor_plan": v006.replay_plan(),
        "predecessor_source_sha256": PINNED_V006_PACKET[V006_PATH.name],
        "a18_parent_relative": str(PARENT_RELATIVE),
        "a18_child_name": A18_NAME,
        "a18_parent_mode": PARENT_MODE,
        "expected_canonical_a18_sha256": EXPECTED_CANONICAL_A18_SHA256,
        "current_parent_status": parent_status(),
        "allowed_child_census": ["EMPTY_PRE_A18", "A18_ONLY"],
        "retained_parent_dev_inode_mode": True,
        "record_or_publisher_order_changed": False,
        "canonical_action_executed": False,
        "claim_boundary": (
            "REPLAY_OWNED_A18_PARENT_CREATION_RECONCILIATION_AND_EXPLICIT_"
            "BOUNDARY_CUSTODY_ONLY__NO_CONTINUOUS_EXTERNAL_WRITER_EXCLUSION_"
            "ACTION_SOURCE_HISTORY_PHYSICS_THRESHOLD_L12_SPECTRUM_CONTINUUM_"
            "OR_GRAVITY_RESULT"
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
    parser.add_argument("--v007-authorization")
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
            arguments.v007_authorization,
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
            if arguments.v006_authorization != v006.V006_AUTHORIZATION:
                raise Refusal("V006 monotone-prefix authorization string is absent")
            if arguments.v007_authorization != V007_AUTHORIZATION:
                raise Refusal("V007 A18-parent authorization string is absent")
            if arguments.retirement_receipt_sha256 is None:
                raise Refusal("retirement receipt hash is absent")
            if arguments.failed_cache_receipt_sha256 is None:
                raise Refusal("failed-cache custody receipt hash is absent")
            products = coordinate_canonical_a01_a18_replay(
                arguments.retirement_receipt_sha256,
                arguments.failed_cache_receipt_sha256,
            )
            result = {
                "classification": "PASS_EXACT_V007_A01_A18_CANONICAL_REPLAY",
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
    return getattr(v006, name)


if __name__ == "__main__":
    raise SystemExit(main())
