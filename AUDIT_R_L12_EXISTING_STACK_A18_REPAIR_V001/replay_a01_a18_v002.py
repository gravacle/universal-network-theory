#!/usr/bin/env python3
"""Exact V002 restart bridge for the frozen A01--A18 replay.

V001 remains immutable.  This wrapper authenticates and executes those exact
bytes, then derives a separately named independent auditor from authenticated
immutable source bytes by inserting the one omitted M25 custody-hook rule.
Both target and repaired-independent sinks validate the original A27 bytes.
"""

from __future__ import annotations

import ast
import hashlib
import os
import stat
import sys
import types
from pathlib import Path
from typing import Final, Mapping


HERE: Final[Path] = Path(__file__).resolve().parent
V001_PATH: Final[Path] = HERE / "replay_a01_a18.py"
V001_SHA256: Final[str] = (
    "31a772f788a33eca05655d2c4e1e2b5edf236dce6873f7ffba61e67476d9571c"
)
V001_MODULE_NAME: Final[str] = "authenticated_replay_a01_a18_v001"
CORRECT_M25_HOOK: Final[str] = (
    "validate_preflight.validate_independent_auditor_source_bytes"
)
EXPECTED_M25_ROWS: Final[tuple[tuple[int, str, str], ...]] = (
    (26, "A02_NONPHYSICAL_PREFLIGHT", "PF_A02"),
    (42, "A03_PREPAYLOAD_AUDIT", "PF_A03"),
    (192, "A12_CONTROL_STAGE_AUDIT", "PF_A12"),
    (259, "A16_L10_STAGE_AUDIT", "PF_A16"),
    (298, "A18_L10_CROSS_GATE", "PF_A18"),
    (339, "A21_SHARED_SCHEDULE_AUDIT", "PF_A21"),
    (445, "A26_FINAL_L12_AUDIT", "PF_A26"),
    (473, "A27_MUTATION_LEDGER", "PF_A27"),
)
INDEPENDENT_SOURCE_PATH: Final[Path] = (
    V001_PATH.parent.parent
    / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
    / "independent_final_auditor.py"
)
INDEPENDENT_SOURCE_SHA256: Final[str] = (
    "99677ffabeedc6db84047bd3637fd292e137d66c2de02eef66633ed789a92f2f"
)
REPAIRED_INDEPENDENT_SHA256: Final[str] = (
    "279b97755ab0bccd8c16cf98b0a52f37b323057a48c3ade23a914f6a4e5bfdc7"
)
REPAIRED_INDEPENDENT_MODULE_NAME: Final[str] = (
    "authenticated_independent_final_auditor_m25_v002"
)
INDEPENDENT_M25_ANCHOR: Final[bytes] = (
    b"        \"M13_DESCRIPTOR_TOCTOU\": \"validate_preflight.validate_held_descriptor_identity\",\n"
    b"        \"M28_PREMATURE_ARTIFACT\": \"validate_preflight.require_artifacts_absent\",\n"
)
INDEPENDENT_M25_REPLACEMENT: Final[bytes] = (
    b"        \"M13_DESCRIPTOR_TOCTOU\": \"validate_preflight.validate_held_descriptor_identity\",\n"
    b"        \"M25_IMPORT_TARGET_VALIDATOR\": (\n"
    b"            \"validate_preflight.validate_independent_auditor_source_bytes\"\n"
    b"        ),\n"
    b"        \"M28_PREMATURE_ARTIFACT\": \"validate_preflight.require_artifacts_absent\",\n"
)


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _read_frozen_v001() -> bytes:
    descriptor = os.open(
        V001_PATH,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        named_before = os.stat(V001_PATH, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named_before.st_mode)
            or before.st_nlink != 1 or before.st_mode & 0o222
            or _identity(before) != _identity(named_before)
        ):
            raise RuntimeError("frozen V001 replay custody mismatch")
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
        named_after = os.stat(V001_PATH, follow_symlinks=False)
        if (
            _identity(before) != _identity(after)
            or _identity(after) != _identity(named_after)
            or digest.hexdigest() != V001_SHA256
        ):
            raise RuntimeError("frozen V001 replay hash/identity mismatch")
        return bytes(raw)
    finally:
        os.close(descriptor)


def _load_v001() -> types.ModuleType:
    existing = sys.modules.get(V001_MODULE_NAME)
    if existing is not None:
        if (
            getattr(existing, "__file__", None) != str(V001_PATH)
            or getattr(existing, "__authenticated_sha256__", None) != V001_SHA256
        ):
            raise RuntimeError("frozen V001 replay module alias")
        return existing
    raw = _read_frozen_v001()
    module = types.ModuleType(V001_MODULE_NAME)
    module.__file__ = str(V001_PATH)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = V001_SHA256
    sys.modules[V001_MODULE_NAME] = module
    try:
        exec(compile(raw, str(V001_PATH), "exec", dont_inherit=True), module.__dict__)
    except BaseException:
        sys.modules.pop(V001_MODULE_NAME, None)
        raise
    _read_frozen_v001()
    return module


v001 = _load_v001()
Refusal = v001.Refusal


def derive_m25_rows(independent: object) -> tuple[tuple[int, str, str], ...]:
    """Derive the complete M25 row census from the authenticated matrix."""
    try:
        assignments = independent._matrix_assignments()
    except AttributeError as error:
        raise Refusal("frozen independent matrix assignment surface is absent") from error
    rows = tuple(
        (index, artifact_id, fixture_id)
        for index, (artifact_id, fixture_id, mutation_class) in enumerate(
            assignments, start=1,
        )
        if mutation_class == "M25_IMPORT_TARGET_VALIDATOR"
    )
    if rows != EXPECTED_M25_ROWS:
        raise Refusal("authenticated M25 matrix row census mismatch")
    return rows


def _import_fingerprint(raw: bytes) -> tuple[str, ...]:
    try:
        tree = ast.parse(raw, filename=str(INDEPENDENT_SOURCE_PATH))
    except (SyntaxError, ValueError) as error:
        raise Refusal("independent auditor source syntax mismatch") from error
    return tuple(sorted(
        ast.dump(node, include_attributes=False)
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ))


def derive_repaired_independent_source() -> bytes:
    """Insert exactly the missing M25 hook into held authenticated bytes."""
    try:
        original = v001._read_pinned_source_bytes(
            INDEPENDENT_SOURCE_PATH, INDEPENDENT_SOURCE_SHA256,
            "frozen independent final auditor", require_immutable=True,
        )
    except RuntimeError as error:
        raise Refusal(str(error)) from error
    if (
        original.count(INDEPENDENT_M25_ANCHOR) != 1
        or original.count(INDEPENDENT_M25_REPLACEMENT) != 0
    ):
        raise Refusal("independent M25 repair anchor census mismatch")
    repaired = original.replace(
        INDEPENDENT_M25_ANCHOR, INDEPENDENT_M25_REPLACEMENT, 1,
    )
    if hashlib.sha256(repaired).hexdigest() != REPAIRED_INDEPENDENT_SHA256:
        raise Refusal("repaired independent auditor digest mismatch")
    if _import_fingerprint(original) != _import_fingerprint(repaired):
        raise Refusal("independent M25 repair changed the import closure")
    return repaired


def load_repaired_independent() -> types.ModuleType:
    existing = sys.modules.get(REPAIRED_INDEPENDENT_MODULE_NAME)
    if existing is not None:
        if (
            getattr(existing, "__file__", None) != str(INDEPENDENT_SOURCE_PATH)
            or getattr(existing, "__authenticated_sha256__", None)
            != REPAIRED_INDEPENDENT_SHA256
        ):
            raise Refusal("repaired independent auditor module alias")
        return existing
    raw = derive_repaired_independent_source()
    module = types.ModuleType(REPAIRED_INDEPENDENT_MODULE_NAME)
    module.__file__ = str(INDEPENDENT_SOURCE_PATH)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = REPAIRED_INDEPENDENT_SHA256
    sys.modules[REPAIRED_INDEPENDENT_MODULE_NAME] = module
    try:
        exec(
            compile(raw, str(INDEPENDENT_SOURCE_PATH), "exec", dont_inherit=True),
            module.__dict__,
        )
    except BaseException:
        sys.modules.pop(REPAIRED_INDEPENDENT_MODULE_NAME, None)
        raise
    derive_repaired_independent_source()
    derive_m25_rows(module)
    return module


class ExactLiveReview(v001.ExactLiveReview):
    """V001 review with direct target and repaired-independent A27 sinks."""

    def __init__(self, root: Path):
        super().__init__(root)
        self.preflight = v001._load_authenticated_module(
            "authenticated_validate_preflight"
        )
        self.repaired_independent = load_repaired_independent()

    def production_sink(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> None:
        if artifact_id != "A27_MUTATION_LEDGER":
            super().production_sink(artifact_id, record)
            return
        before = v001.retirement.canonical_json_bytes(record)
        matrix, matrix_sha = self.preflight.load_obligation_matrix()
        if matrix_sha != self.preflight.OBLIGATION_MATRIX_SHA256:
            raise Refusal("target A27 obligation matrix digest mismatch")
        freeze = self.builder.require_frozen_census()
        self.preflight.validate_mutation_ledger(dict(record), matrix, freeze)
        if v001.retirement.canonical_json_bytes(record) != before:
            raise Refusal("A27 target validator mutated original record")

    def independent_sink(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> None:
        if artifact_id != "A27_MUTATION_LEDGER":
            super().independent_sink(artifact_id, record)
            return
        before = v001.retirement.canonical_json_bytes(record)
        self.repaired_independent.validate_mutation_ledger(
            dict(record), fixture_mode=False,
        )
        if v001.retirement.canonical_json_bytes(record) != before:
            raise Refusal("A27 repaired independent validator mutated original record")


def coordinate_canonical_a01_a18_replay(
    expected_retirement_receipt_sha256: str,
) -> dict[tuple[str, int], str]:
    """Resume the fixed V001 replay using the bounded V002 review class."""
    previous = v001.ExactLiveReview
    if previous.__module__ != v001.__name__:
        raise Refusal("frozen V001 live-review class was already replaced")
    v001.ExactLiveReview = ExactLiveReview
    try:
        return v001.coordinate_canonical_a01_a18_replay(
            expected_retirement_receipt_sha256,
        )
    finally:
        v001.ExactLiveReview = previous


def main() -> int:
    previous = v001.ExactLiveReview
    if previous.__module__ != v001.__name__:
        print("REFUSED: frozen V001 live-review class was already replaced", file=sys.stderr)
        return 2
    v001.ExactLiveReview = ExactLiveReview
    try:
        return v001.main()
    finally:
        v001.ExactLiveReview = previous


def __getattr__(name: str) -> object:
    return getattr(v001, name)


if __name__ == "__main__":
    raise SystemExit(main())
