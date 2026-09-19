#!/usr/bin/env python3
"""Replay-only staged-path adapter for the frozen V004 restart.

V004 constructs A11--A13 and A15--A16 as dependency-closed batches before
publication.  Three production validators nevertheless resolve predecessors
only through their eventual canonical paths.  This wrapper gives those
validators authenticated owner-once stage paths while the batches are being
checked.  It changes no record byte, publisher, history, formula, threshold,
or publication order.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import tempfile
import threading
import types
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Final, Iterator, Mapping


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
V004_PATH: Final[Path] = HERE / "replay_a01_a18_v004.py"
V004_MODULE_NAME: Final[str] = "authenticated_replay_a01_a18_v004"
PINNED_V004_PACKET: Final[dict[str, str]] = {
    "replay_a01_a18_v004.py":
        "b4aef8f37e3937a2d9e89170b3326dbebc9f83f18ca8561378e9456e8c74ffa8",
    "test_replay_a01_a18_v004.py":
        "46a367e50cd9aee86a397cc3f1ccda410d26493e0e2e3e1b0c50e25eaa76a67a",
    "REPLAY_SOURCE_FREEZE_V004.json":
        "db0f0320b589ec42a770e80fbba708ddff83ea2c42dbbbc13304caf6acd12d95",
    "REPLAY_CANDIDATE_RESULT_V004.json":
        "44c548dda51bd8539c3605afc3dd8b081dbd3452bfb82effd394d9c5b89c5ff2",
}
EXPECTED_CANDIDATE_SHA256: Final[dict[str, str]] = {
    "A11_CONTROL_STAGE_GATE":
        "0dbba128a7bf4ea6319c64c687181c6cf95207a917c57721d58cef3764da6371",
    "A12_CONTROL_STAGE_AUDIT":
        "4da29efa71259c1e44b42bda8b8d48332940de9d9557c621025b706f4b93392f",
    "A13_L10_AUTHORIZATION":
        "9094d717db0adfb63219cfa8c9779b0db575cccd19c013c0c158d1a34f2a5085",
}
STAGED_NAME: Final[dict[str, str]] = {
    "A11_CONTROL_STAGE_GATE": "A11.json",
    "A12_CONTROL_STAGE_AUDIT": "A12.json",
    "A15_L10_STAGE_GATE": "A15.json",
}
PATH_PREDECESSOR: Final[dict[str, str]] = {
    "CONTROL_GATE_PATH": "A11_CONTROL_STAGE_GATE",
    "CONTROL_AUDIT_PATH": "A12_CONTROL_STAGE_AUDIT",
    "L10_GATE_PATH": "A15_L10_STAGE_GATE",
}
TRACKED_ARTIFACTS: Final[frozenset[str]] = frozenset({
    *STAGED_NAME,
    "A13_L10_AUTHORIZATION",
    "A16_L10_STAGE_AUDIT",
})
CANONICAL_ORDER: Final[tuple[str, ...]] = (
    "A11_CONTROL_STAGE_GATE",
    "A12_CONTROL_STAGE_AUDIT",
    "A13_L10_AUTHORIZATION",
    "A15_L10_STAGE_GATE",
    "A16_L10_STAGE_AUDIT",
)
V005_AUTHORIZATION: Final[str] = (
    "EXECUTE_EXACT_DEPENDENCY_CLOSED_STAGED_PATH_REPLAY_V005"
)
STAGE_TEMP_PARENT: Final[Path] = Path("/private/tmp")


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _read_frozen_packet_file(name: str) -> bytes:
    if name not in PINNED_V004_PACKET:
        raise RuntimeError("unregistered frozen V004 packet member")
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
            raise RuntimeError(f"frozen V004 packet custody mismatch: {name}")
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
            or digest.hexdigest() != PINNED_V004_PACKET[name]
        ):
            raise RuntimeError(f"frozen V004 packet digest mismatch: {name}")
        return bytes(raw)
    finally:
        os.close(descriptor)


def _load_v004() -> types.ModuleType:
    for name in PINNED_V004_PACKET:
        _read_frozen_packet_file(name)
    existing = sys.modules.get(V004_MODULE_NAME)
    if existing is not None:
        if (
            getattr(existing, "__file__", None) != str(V004_PATH)
            or getattr(existing, "__authenticated_sha256__", None)
            != PINNED_V004_PACKET[V004_PATH.name]
        ):
            raise RuntimeError("frozen V004 replay module alias")
        return existing
    raw = _read_frozen_packet_file(V004_PATH.name)
    module = types.ModuleType(V004_MODULE_NAME)
    module.__file__ = str(V004_PATH)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = PINNED_V004_PACKET[V004_PATH.name]
    sys.modules[V004_MODULE_NAME] = module
    try:
        exec(compile(raw, str(V004_PATH), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(V004_MODULE_NAME, None)
        raise
    for name in PINNED_V004_PACKET:
        _read_frozen_packet_file(name)
    return module


v004 = _load_v004()
v003 = v004.v003
v002 = v003.v002
v001 = v003.v001
retirement = v003.retirement
Refusal = v003.Refusal
ORIGINAL_V002_REVIEW: Final[object] = v002.ExactLiveReview


class StagedPathReview(v002.ExactLiveReview):
    """Bind only authenticated, exact predecessor bytes during batch review."""

    def __init__(self, root: Path):
        super().__init__(root)
        self._pid = os.getpid()
        self._thread = threading.get_ident()
        self._closed = False
        self._temporary: tempfile.TemporaryDirectory[str] | None = None
        self._staged_identity: dict[str, tuple[int, ...]] = {}
        self._candidate_bytes: dict[str, bytes] = {}
        self._original_paths = {
            "CONTROL_GATE_PATH": self.validators.CONTROL_GATE_PATH,
            "CONTROL_AUDIT_PATH": self.validators.CONTROL_AUDIT_PATH,
            "L10_GATE_PATH": self.validators.L10_GATE_PATH,
        }
        try:
            self._temporary = tempfile.TemporaryDirectory(
                prefix="v005-staged-path-", dir=STAGE_TEMP_PARENT,
            )
            self._stage_root = Path(self._temporary.name).resolve()
            stage_metadata = os.stat(self._stage_root, follow_symlinks=False)
            if (
                not stat.S_ISDIR(stage_metadata.st_mode)
                or stat.S_ISLNK(stage_metadata.st_mode)
            ):
                raise Refusal(
                    "V005 internal stage root is not an ordinary directory"
                )
            self._stage_root_identity = (
                stage_metadata.st_dev, stage_metadata.st_ino,
                stage_metadata.st_mode,
            )
            self._assert_shared_dispatch_identity()
            self._assert_original_paths()
            if any(
                original != self._canonical_path(PATH_PREDECESSOR[name])
                for name, original in self._original_paths.items()
            ):
                raise Refusal("V005 original validator path value mismatch")
            if self._stage_root.parent != STAGE_TEMP_PARENT.resolve():
                raise Refusal("V005 internal stage root escaped its fixed parent")
            self._canonical_identity: dict[str, tuple[int, ...]] = {}
            self._canonical_bytes: dict[str, bytes] = {}
            initial_present: list[str] = []
            for artifact_id in CANONICAL_ORDER:
                path = self._canonical_path(artifact_id)
                if retirement.path_exists(path):
                    _record, _digest, raw = v001._stable_owner_once_json(
                        path, f"V005 entry {artifact_id}",
                    )
                    metadata = os.stat(path, follow_symlinks=False)
                    self._canonical_identity[artifact_id] = _identity(metadata)
                    self._canonical_bytes[artifact_id] = raw
                    initial_present.append(artifact_id)
            if tuple(initial_present) != CANONICAL_ORDER[:len(initial_present)]:
                raise Refusal("V005 canonical entry is not a dependency-order prefix")
            self._entry_prefix_count = len(initial_present)
            # An exact pre-existing dependency prefix is the sole restart
            # state accepted from an earlier publication interruption.
            self._control_batch_closed = self._entry_prefix_count > 0
            self._l10_batch_closed = self._entry_prefix_count > 3
            self._assert_canonical_state()
        except BaseException:
            self.close()
            raise

    def _assert_single_thread(self) -> None:
        if (
            self._closed or os.getpid() != self._pid
            or threading.get_ident() != self._thread
        ):
            raise Refusal("V005 staged review crossed its single-thread lifetime")

    def _assert_shared_dispatch_identity(self) -> None:
        """Prove target, builder dispatch, and consumer use one module graph."""
        validators = sys.modules.get("production_obligation_validators")
        if validators is not self.validators:
            raise Refusal("V005 production validator module identity mismatch")
        if (
            Path(getattr(self.validators, "__file__", "")).resolve()
            != Path(self.builder.PRODUCTION_VALIDATORS).resolve()
        ):
            raise Refusal("V005 builder production validator path mismatch")
        if self.consumer.builder is not self.builder:
            raise Refusal("V005 consumer/builder module identity mismatch")
        dispatch = self.builder._dispatch_production_obligation
        if (
            dispatch.__globals__ is not self.builder.__dict__
            or dispatch.__globals__.get("PRODUCTION_VALIDATORS")
            != self.builder.PRODUCTION_VALIDATORS
        ):
            raise Refusal("V005 builder dispatch identity mismatch")

    def _assert_original_paths(self) -> None:
        for name, original in self._original_paths.items():
            if getattr(self.validators, name) is not original:
                raise Refusal(f"V005 validator path was not restored: {name}")

    def _assert_stage_root(self) -> None:
        try:
            metadata = os.stat(self._stage_root, follow_symlinks=False)
        except OSError as error:
            raise Refusal("V005 stage root disappeared") from error
        observed = (
            metadata.st_dev, metadata.st_ino, metadata.st_mode,
        )
        if (
            not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode)
            or observed != self._stage_root_identity
        ):
            raise Refusal("V005 stage-root identity mismatch")

    def _assert_canonical_state(self) -> None:
        """Check the exact boundary prefix; this is not a writer lock."""
        self._assert_single_thread()
        present: list[str] = []
        observed_raw: dict[str, bytes] = {}
        observed_identity: dict[str, tuple[int, ...]] = {}
        for artifact_id in CANONICAL_ORDER:
            path = self._canonical_path(artifact_id)
            if not retirement.path_exists(path):
                continue
            _record, _digest, raw = v001._stable_owner_once_json(
                path, f"V005 boundary {artifact_id}",
            )
            metadata = os.stat(path, follow_symlinks=False)
            present.append(artifact_id)
            observed_raw[artifact_id] = raw
            observed_identity[artifact_id] = _identity(metadata)
        if tuple(present) != CANONICAL_ORDER[:len(present)]:
            raise Refusal("V005 canonical publications are not an exact prefix")
        maximum = 0
        if self._control_batch_closed:
            maximum = 3
        if self._l10_batch_closed:
            maximum = 5
        if len(present) < self._entry_prefix_count or len(present) > maximum:
            raise Refusal("V005 canonical prefix changed outside a closed batch")
        for artifact_id in present:
            prior_raw = self._canonical_bytes.get(artifact_id)
            prior_identity = self._canonical_identity.get(artifact_id)
            candidate = self._candidate_bytes.get(artifact_id)
            if prior_raw is not None and observed_raw[artifact_id] != prior_raw:
                raise Refusal("V005 canonical predecessor bytes changed")
            if prior_identity is not None and observed_identity[artifact_id] != prior_identity:
                raise Refusal("V005 canonical predecessor inode changed")
            if candidate is not None and observed_raw[artifact_id] != candidate:
                raise Refusal("V005 canonical predecessor differs from candidate")
            if prior_raw is None:
                if candidate is None:
                    raise Refusal("V005 canonical publication appeared before its candidate")
                self._canonical_bytes[artifact_id] = observed_raw[artifact_id]
                self._canonical_identity[artifact_id] = observed_identity[artifact_id]

    def _record_bytes(self, record: Mapping[str, object]) -> bytes:
        return retirement.publication_json_bytes(dict(record))

    def _remember_candidate(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> bytes:
        if artifact_id not in TRACKED_ARTIFACTS:
            raise Refusal("V005 unregistered staged-path artifact")
        raw = self._record_bytes(record)
        expected = EXPECTED_CANDIDATE_SHA256.get(artifact_id)
        if expected is not None and retirement.sha256_bytes(raw) != expected:
            raise Refusal(f"V005 {artifact_id} candidate digest mismatch")
        prior = self._candidate_bytes.get(artifact_id)
        if prior is not None and prior != raw:
            raise Refusal(f"V005 {artifact_id} candidate bytes changed")
        self._candidate_bytes[artifact_id] = raw
        canonical = self._canonical_bytes.get(artifact_id)
        if canonical is not None and canonical != raw:
            raise Refusal(f"V005 canonical {artifact_id} differs from candidate")
        return raw

    def _stage_once(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> Path:
        self._assert_single_thread()
        self._assert_stage_root()
        raw = self._remember_candidate(artifact_id, record)
        name = STAGED_NAME.get(artifact_id)
        if name is None:
            raise Refusal("V005 artifact has no staged predecessor role")
        path = self._stage_root / name
        if artifact_id not in self._staged_identity:
            retirement.publish_once(path, dict(record))
            metadata = os.stat(path, follow_symlinks=False)
            if (
                not stat.S_ISREG(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode)
                or metadata.st_nlink != 1 or metadata.st_mode & 0o222
            ):
                raise Refusal("V005 staged publication is not owner-once")
            self._staged_identity[artifact_id] = _identity(metadata)
        return self._require_stage(artifact_id)

    def _require_stage(self, artifact_id: str) -> Path:
        self._assert_single_thread()
        self._assert_stage_root()
        name = STAGED_NAME.get(artifact_id)
        expected_identity = self._staged_identity.get(artifact_id)
        expected_raw = self._candidate_bytes.get(artifact_id)
        if name is None or expected_identity is None or expected_raw is None:
            raise Refusal(f"V005 staged predecessor is absent: {artifact_id}")
        expected_names = {
            STAGED_NAME[key] for key in self._staged_identity
        }
        try:
            if (
                self._stage_root.is_symlink() or not self._stage_root.is_dir()
                or {child.name for child in self._stage_root.iterdir()}
                != expected_names
            ):
                raise Refusal("V005 stage-root child census mismatch")
            path = self._stage_root / name
            descriptor = os.open(
                path,
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0),
            )
        except (OSError, ValueError) as error:
            raise Refusal("V005 staged predecessor open/census mismatch") from error
        try:
            before = os.fstat(descriptor)
            named = os.stat(path, follow_symlinks=False)
            if (
                not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
                or before.st_nlink != 1 or before.st_mode & 0o222
                or _identity(before) != _identity(named)
                or _identity(before) != expected_identity
            ):
                raise Refusal("V005 staged predecessor identity mismatch")
            chunks: list[bytes] = []
            offset = 0
            while True:
                block = os.pread(descriptor, 16 * 2**20, offset)
                if not block:
                    break
                chunks.append(block)
                offset += len(block)
            raw = b"".join(chunks)
            after = os.fstat(descriptor)
            named_after = os.stat(path, follow_symlinks=False)
            if (
                raw != expected_raw or _identity(before) != _identity(after)
                or _identity(after) != _identity(named_after)
                or retirement.descriptor_sha256(descriptor)
                != retirement.sha256_bytes(expected_raw)
            ):
                raise Refusal("V005 staged predecessor bytes changed")
            return path
        finally:
            os.close(descriptor)

    def _canonical_path(self, artifact_id: str) -> Path:
        relative = v001.TEMPLATE_PATH_BY_ARTIFACT[artifact_id]
        return ROOT.joinpath(*PurePosixPath(relative).parts)

    def _select_predecessor(self, artifact_id: str) -> tuple[Path, bool]:
        """Prefer an exact canonical predecessor, else its exact stage copy."""
        self._assert_canonical_state()
        stage = self._require_stage(artifact_id)
        canonical = self._canonical_path(artifact_id)
        if not retirement.path_exists(canonical):
            return stage, True
        _record, _digest, raw = v001._stable_owner_once_json(
            canonical, f"V005 canonical {artifact_id}",
        )
        if raw != self._candidate_bytes[artifact_id]:
            raise Refusal(f"V005 canonical {artifact_id} differs from staged bytes")
        return canonical, False

    @contextmanager
    def _bound_validator_paths(
        self, bindings: Mapping[str, Path], absent: tuple[Path, ...] = (),
    ) -> Iterator[None]:
        self._assert_single_thread()
        self._assert_canonical_state()
        self._assert_shared_dispatch_identity()
        self._assert_original_paths()
        if any(retirement.path_exists(path) for path in absent):
            raise Refusal("V005 canonical predecessor appeared before binding")
        try:
            for name, path in bindings.items():
                if name not in self._original_paths or not isinstance(path, Path):
                    raise Refusal("V005 unregistered validator path binding")
                setattr(self.validators, name, path)
            yield
            self._assert_canonical_state()
            if any(retirement.path_exists(path) for path in absent):
                raise Refusal("V005 canonical predecessor appeared during binding")
        finally:
            for name, original in self._original_paths.items():
                setattr(self.validators, name, original)
            self._assert_original_paths()
            self._assert_canonical_state()

    def _production_with_predecessors(
        self,
        artifact_id: str,
        record: Mapping[str, object],
        required: Mapping[str, str],
    ) -> None:
        bindings: dict[str, Path] = {}
        absent: list[Path] = []
        for constant, predecessor in required.items():
            path, used_stage = self._select_predecessor(predecessor)
            bindings[constant] = path
            if used_stage:
                absent.append(self._canonical_path(predecessor))
        with self._bound_validator_paths(bindings, tuple(absent)):
            super().production_sink(artifact_id, record)

    def production_sink(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> None:
        self._assert_single_thread()
        self._assert_canonical_state()
        before = self._record_bytes(record)
        if artifact_id == "A12_CONTROL_STAGE_AUDIT":
            self._production_with_predecessors(
                artifact_id, record,
                {"CONTROL_GATE_PATH": "A11_CONTROL_STAGE_GATE"},
            )
        elif artifact_id == "A13_L10_AUTHORIZATION":
            self._production_with_predecessors(
                artifact_id, record, {
                    "CONTROL_GATE_PATH": "A11_CONTROL_STAGE_GATE",
                    "CONTROL_AUDIT_PATH": "A12_CONTROL_STAGE_AUDIT",
                },
            )
        elif artifact_id == "A16_L10_STAGE_AUDIT":
            self._production_with_predecessors(
                artifact_id, record,
                {"L10_GATE_PATH": "A15_L10_STAGE_GATE"},
            )
        else:
            super().production_sink(artifact_id, record)
        if self._record_bytes(record) != before:
            raise Refusal(f"V005 target sink mutated {artifact_id}")
        if artifact_id in TRACKED_ARTIFACTS:
            self._remember_candidate(artifact_id, record)
        if artifact_id in STAGED_NAME:
            self._stage_once(artifact_id, record)
        self._assert_canonical_state()

    def independent_sink(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> None:
        self._assert_single_thread()
        self._assert_canonical_state()
        before = self._record_bytes(record)
        if artifact_id in TRACKED_ARTIFACTS:
            if self._candidate_bytes.get(artifact_id) != before:
                raise Refusal("V005 independent sink did not receive target bytes")
            if artifact_id in STAGED_NAME:
                self._require_stage(artifact_id)
        super().independent_sink(artifact_id, record)
        if self._record_bytes(record) != before:
            raise Refusal(f"V005 independent sink mutated {artifact_id}")
        self._assert_canonical_state()

    def validate_stage_chain(
        self,
        a11: Mapping[str, object],
        a12: Mapping[str, object],
        a13: Mapping[str, object],
        cache_hashes: Mapping[str, str],
        a07_sha: str,
    ) -> None:
        paths = {
            "A11_CONTROL_STAGE_GATE": self._require_stage(
                "A11_CONTROL_STAGE_GATE"
            ),
            "A12_CONTROL_STAGE_AUDIT": self._require_stage(
                "A12_CONTROL_STAGE_AUDIT"
            ),
        }
        for artifact_id, record in (
            ("A11_CONTROL_STAGE_GATE", a11),
            ("A12_CONTROL_STAGE_AUDIT", a12),
            ("A13_L10_AUTHORIZATION", a13),
        ):
            if self._candidate_bytes.get(artifact_id) != self._record_bytes(record):
                raise Refusal("V005 stage-chain bytes differ from common sinks")
        absent = tuple(
            self._canonical_path(artifact_id)
            for artifact_id in paths
            if not retirement.path_exists(self._canonical_path(artifact_id))
        )
        with self._bound_validator_paths({
            "CONTROL_GATE_PATH": paths["A11_CONTROL_STAGE_GATE"],
            "CONTROL_AUDIT_PATH": paths["A12_CONTROL_STAGE_AUDIT"],
        }, absent):
            super().validate_stage_chain(a11, a12, a13, cache_hashes, a07_sha)
        self._control_batch_closed = True
        self._assert_canonical_state()

    def validate_l10_stage_pair(
        self,
        a15: Mapping[str, object],
        a16: Mapping[str, object],
        cache_hashes: Mapping[str, str],
        a07_sha: str,
        a11_sha: str,
        a13_sha: str,
    ) -> None:
        stage = self._require_stage("A15_L10_STAGE_GATE")
        for artifact_id, record in (
            ("A15_L10_STAGE_GATE", a15),
            ("A16_L10_STAGE_AUDIT", a16),
        ):
            if self._candidate_bytes.get(artifact_id) != self._record_bytes(record):
                raise Refusal("V005 L10-stage bytes differ from common sinks")
        canonical = self._canonical_path("A15_L10_STAGE_GATE")
        absent = (canonical,) if not retirement.path_exists(canonical) else ()
        with self._bound_validator_paths({"L10_GATE_PATH": stage}, absent):
            super().validate_l10_stage_pair(
                a15, a16, cache_hashes, a07_sha, a11_sha, a13_sha,
            )
        self._l10_batch_closed = True
        self._assert_canonical_state()

    def close(self) -> None:
        if getattr(self, "_closed", True):
            return
        try:
            for name, original in self._original_paths.items():
                setattr(self.validators, name, original)
            self._assert_original_paths()
        finally:
            self._closed = True
            if self._temporary is not None:
                self._temporary.cleanup()


_CAPTURE_COORDINATE_REVIEW = False
_ACTIVE_COORDINATE_REVIEW: StagedPathReview | None = None


class CoordinateStagedPathReview(StagedPathReview):
    """Capture the sole live review so its temporary custody is always closed."""

    def __init__(self, root: Path):
        global _ACTIVE_COORDINATE_REVIEW
        if not _CAPTURE_COORDINATE_REVIEW or _ACTIVE_COORDINATE_REVIEW is not None:
            raise Refusal("V005 coordinate review lifetime mismatch")
        super().__init__(root)
        _ACTIVE_COORDINATE_REVIEW = self


def coordinate_canonical_a01_a18_replay(
    expected_retirement_receipt_sha256: str,
    expected_failed_cache_receipt_sha256: str,
) -> dict[tuple[str, int], str]:
    """Run V004 with only the bounded staged-path review substituted."""
    global _ACTIVE_COORDINATE_REVIEW, _CAPTURE_COORDINATE_REVIEW
    previous = v002.ExactLiveReview
    if previous is not ORIGINAL_V002_REVIEW:
        raise Refusal("frozen V002 review class was already replaced")
    if _CAPTURE_COORDINATE_REVIEW or _ACTIVE_COORDINATE_REVIEW is not None:
        raise Refusal("V005 coordinate is already active")
    _CAPTURE_COORDINATE_REVIEW = True
    v002.ExactLiveReview = CoordinateStagedPathReview
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
        "classification": "BOUNDED_NONEXECUTED_V005_STAGED_PATH_PLAN",
        "predecessor_plan": v004.replay_plan(),
        "predecessor_source_sha256": PINNED_V004_PACKET[V004_PATH.name],
        "staged_predecessors": dict(STAGED_NAME),
        "temporarily_bound_validator_paths": [
            "CONTROL_GATE_PATH", "CONTROL_AUDIT_PATH", "L10_GATE_PATH",
        ],
        "expected_control_candidate_sha256": dict(EXPECTED_CANDIDATE_SHA256),
        "record_bytes_changed": False,
        "publisher_or_publication_order_changed": False,
        "canonical_action_executed": False,
        "claim_boundary": (
            "REPLAY_ONLY_DEPENDENCY_CLOSED_STAGE_PATH_COMPATIBILITY__NO_ACTION_"
            "SOURCE_HISTORY_PHYSICS_THRESHOLD_A18_L12_SPECTRUM_CONTINUUM_OR_"
            "GRAVITY_RESULT"
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
    arguments = parser.parse_args()
    try:
        fields = (
            arguments.retirement_receipt_sha256,
            arguments.failed_cache_receipt_sha256,
            arguments.authorization,
            arguments.v003_authorization,
            arguments.v004_authorization,
            arguments.v005_authorization,
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
            if arguments.v005_authorization != V005_AUTHORIZATION:
                raise Refusal("V005 staged-path authorization string is absent")
            if arguments.retirement_receipt_sha256 is None:
                raise Refusal("retirement receipt hash is absent")
            if arguments.failed_cache_receipt_sha256 is None:
                raise Refusal("failed-cache custody receipt hash is absent")
            products = coordinate_canonical_a01_a18_replay(
                arguments.retirement_receipt_sha256,
                arguments.failed_cache_receipt_sha256,
            )
            result = {
                "classification": "PASS_EXACT_V005_A01_A18_CANONICAL_REPLAY",
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
    return getattr(v004, name)


if __name__ == "__main__":
    raise SystemExit(main())
