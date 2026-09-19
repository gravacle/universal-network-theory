#!/usr/bin/env python3
"""Bounded A01--A18 replay primitives for the repaired V012 control stack.

This module deliberately contains no solver, history, cache, or physics
implementation.  It can only:

* derive and owner-once publish the repaired canonical launcher/builder pair
  from census-authenticated retired bytes and one frozen launcher candidate;
* reconstruct enumerated JSON authorities from census-authenticated retired
  bytes by replacing their complete, artifact-specific dynamic binding set;
* invoke the five already-existing publishers in forked children whose entry
  code and complete repository-local import closure came from retained,
  hash-pinned source descriptors;
* restore the seven authenticated hostile A17 entries after a completed
  retirement using an owner-once, no-replace rename transaction; and
* construct A18 from the authenticated 65-check obstruction candidate while
  changing only enumerated path/hash bindings and requiring two injected
  validation sinks.

No canonical action is performed on import or by the test suite.  The CLI has
one hash-gated, fixed-order live entry point; it is inert unless the exact
authorization string and completed-retirement receipt hash are supplied.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import sys
import tempfile
import types
from pathlib import Path, PurePosixPath
from typing import Callable, Final, Mapping, NamedTuple, Sequence


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
RETIREMENT_SOURCE: Final[Path] = HERE / "retire_canonical_stack.py"
A18_OBSTRUCTION: Final[Path] = (
    ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
    / "A18_DUAL_SINK_ROLE_CONTRACT_OBSTRUCTION_V001.json"
)
A18_OBSTRUCTION_SHA256: Final[str] = (
    "52882072cea1413ae2f403770d554f0e3b1654c0f352a026d744d80cd92e4f40"
)
A18_CANONICAL_PATH: Final[str] = (
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
    "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
)
OLD_CANONICAL_BUILDER_PATH: Final[str] = (
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py"
)
OLD_CANONICAL_BUILDER_SHA256: Final[str] = (
    "34e5f18ed1fb3f4be1b729fee0be51640dbf49a786d24d7ce90f5edd7a19309c"
)
REPAIRED_CANONICAL_BUILDER_SHA256: Final[str] = (
    "f59b625383fd748246225cd603710097e3a69a7e9fae6cc02994c5d79c4c8a3d"
)
OLD_CANONICAL_LAUNCHER_PATH: Final[str] = (
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/"
    "production_dual_l12_launcher.py"
)
OLD_CANONICAL_LAUNCHER_SHA256: Final[str] = (
    "095f8cd25499ea4f36cba913038cfbdadfe6e56309046370d4eeb03c347c1d71"
)
REPAIRED_CANONICAL_LAUNCHER_SHA256: Final[str] = (
    "067bdec60d4fe40e5d961241a7408677f8950ea7d68e7dbb3d8dc0f9db83f163"
)
REPAIRED_LAUNCHER_CANDIDATE_PATH: Final[str] = (
    "AUDIT_PREPARATION_R_L12_STAGE3_ENTRY_V001/"
    "production_dual_l12_launcher_candidate.py"
)
PINNED_REPAIRED_CANONICAL_SOURCES: Final[dict[str, tuple[str, str]]] = {
    "build_target_cache": (
        OLD_CANONICAL_BUILDER_PATH, REPAIRED_CANONICAL_BUILDER_SHA256,
    ),
    "production_dual_l12_launcher": (
        OLD_CANONICAL_LAUNCHER_PATH, REPAIRED_CANONICAL_LAUNCHER_SHA256,
    ),
}
PINNED_LIVE_SOURCES: Final[dict[str, tuple[str, str]]] = {
    "production_obligation_validators": (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "production_obligation_validators.py",
        "b6409bfca1c0ee468671a37d5aac41c80c67f8027265ce4c0261b861509ad691",
    ),
    "build_target_cache": (
        OLD_CANONICAL_BUILDER_PATH,
        REPAIRED_CANONICAL_BUILDER_SHA256,
    ),
    "consume_target_cache": (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py",
        "80b2ce08af37bc8cffd91f07146c777f60785883436361ca9521597763fd5a11",
    ),
    "independent_final_auditor": (
        "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/"
        "independent_final_auditor.py",
        "99677ffabeedc6db84047bd3637fd292e137d66c2de02eef66633ed789a92f2f",
    ),
}

PINNED_EXECUTABLE_DEPENDENCIES: Final[dict[str, tuple[str, str]]] = {
    "v012_exact_retirement_for_replay": (
        "AUDIT_R_L12_EXISTING_STACK_A18_REPAIR_V001/retire_canonical_stack.py",
        "5a6264410f6e2ee09b7f6853ee434ed8b6396a1d975a7c4ef5c094da22bad6ed",
    ),
    "compute_streamed_history": (
        "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/compute_streamed_history.py",
        "2cce210fff77ceb4ea91bce6fdd50ea75e1c7c5027471eaf4264ae794cc03b16",
    ),
    "compute_prefix_history": (
        "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history.py",
        "8bc59c363c638edd35db12fccb953a2590464b8f422f8a71f5ed4f3972951515",
    ),
    "compute_prefix_history_v002": (
        "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v002.py",
        "71458cd4b958d5b38cb24409ed769e790d9a83e1da8ac71fd2d3098fdb779694",
    ),
    "compute_prefix_history_v004": (
        "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001/compute_prefix_history_v004.py",
        "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7",
    ),
    **PINNED_LIVE_SOURCES,
    "authenticated_validate_preflight": (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/validate_preflight.py",
        "af986f297063dcb8e6263d0bd2423cd1fc0e44042aba20ad5b8ae62cee635476",
    ),
    "authenticated_independent_postbuild_auditor": (
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/independent_postbuild_auditor.py",
        "d5fa4c91f45d64501dd228e16b4cd50faa520b8c3a8c313d4dc33a82e6848f86",
    ),
}

PINNED_MODULE_PREREQUISITES: Final[dict[str, tuple[str, ...]]] = {
    "v012_exact_retirement_for_replay": (),
    "compute_streamed_history": (),
    "compute_prefix_history": ("compute_streamed_history",),
    "compute_prefix_history_v002": ("compute_prefix_history",),
    "compute_prefix_history_v004": ("compute_prefix_history_v002",),
    "production_obligation_validators": (),
    "build_target_cache": ("compute_prefix_history_v004",),
    "consume_target_cache": ("compute_prefix_history_v004", "build_target_cache"),
    "independent_final_auditor": (),
    "authenticated_validate_preflight": (
        "production_obligation_validators", "build_target_cache",
        "consume_target_cache",
    ),
    "authenticated_independent_postbuild_auditor": (),
}


# The complete permitted old-launcher transformation.  Each left-hand anchor
# must occur exactly once, in this order, and the final bytes must equal the
# independently frozen Stage-3 candidate digest above.
EXACT_LAUNCHER_REPLACEMENTS: Final[tuple[tuple[bytes, bytes], ...]] = (
    (
        b"import selectors\nimport shutil\nimport signal\n",
        b"import selectors\nimport signal\n",
    ),
    (
        b"    rows: list[dict[str, object]],\n"
        b") -> None:\n"
        b"    device = os.stat(ROOT, follow_symlinks=False).st_dev\n"
        b"    free = shutil.disk_usage(ROOT).free\n",
        b"    rows: list[dict[str, object]],\n"
        b"    execution_guard: object,\n"
        b") -> None:\n"
        b"    sampler = getattr(execution_guard, \"disk_state\", None)\n"
        b"    if not callable(sampler):\n"
        b"        raise LaunchRefusal(\"authenticated Stage-3 disk guard is absent\")\n"
        b"    state = sampler()\n"
        b"    if (\n"
        b"        type(state) is not tuple or len(state) != 2\n"
        b"        or type(state[0]) is not int or type(state[1]) is not int\n"
        b"    ):\n"
        b"        raise LaunchRefusal(\"authenticated Stage-3 disk guard is malformed\")\n"
        b"    device, free = state\n",
    ),
    (
        b"def execute() -> str:\n"
        b"    \"\"\"Run both exact L12 workers and publish accepted A23 telemetry once.\"\"\"\n",
        b"def _guard_phase(execution_guard: object | None, phase: str) -> None:\n"
        b"    checker = getattr(execution_guard, \"verify_phase\", None)\n"
        b"    if not callable(checker):\n"
        b"        raise LaunchRefusal(\"authenticated Stage-3 execution guard is absent\")\n"
        b"    checker(phase)\n\n\n"
        b"def execute(execution_guard: object | None = None) -> str:\n"
        b"    \"\"\"Run both exact L12 workers and publish accepted A23 telemetry once.\"\"\"\n"
        b"    _guard_phase(execution_guard, \"initial\")\n",
    ),
    (
        b"            _publish(WIRE_PATHS[f\"ready:{role}\"], record)\n\n"
        b"        handshake = build_handshake(coordinator, ready)\n",
        b"            _publish(WIRE_PATHS[f\"ready:{role}\"], record)\n\n"
        b"        _guard_phase(execution_guard, \"pre_handshake\")\n"
        b"        handshake = build_handshake(coordinator, ready)\n",
    ),
    (
        b"        release = build_release(coordinator, release_epochs)\n"
        b"        coordinator.release_workers(release)\n",
        b"        release = build_release(coordinator, release_epochs)\n"
        b"        _guard_phase(execution_guard, \"pre_release\")\n"
        b"        coordinator.release_workers(release)\n",
    ),
    (
        b"        _sample_disk(first_release, expected_filesystem, policy, disk)\n",
        b"        _sample_disk(first_release, expected_filesystem, policy, disk, execution_guard)\n",
    ),
    (
        b"            _sample_disk(epoch, expected_filesystem, policy, disk)\n",
        b"            _sample_disk(epoch, expected_filesystem, policy, disk, execution_guard)\n",
    ),
    (
        b"        _sample_disk(final_epoch, expected_filesystem, policy, disk)\n",
        b"        _sample_disk(final_epoch, expected_filesystem, policy, disk, execution_guard)\n",
    ),
    (
        b"        for item in retained:\n"
        b"            item.verify()\n"
        b"        return digest\n",
        b"        for item in retained:\n"
        b"            item.verify()\n"
        b"        _guard_phase(execution_guard, \"final\")\n"
        b"        return digest\n",
    ),
)


def _read_pinned_source_bytes(
    path: Path, expected_sha256: str, label: str, *,
    require_immutable: bool = False,
) -> bytes:
    """Return exact hash-pinned source bytes held through one descriptor."""
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise RuntimeError(f"{label} source open failed") from error
    try:
        before = os.fstat(descriptor)
        named_before = os.stat(path, follow_symlinks=False)
        identity = lambda value: (
            value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_nlink,
        )
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_ISLNK(named_before.st_mode)
            or before.st_nlink != 1
            or (require_immutable and before.st_mode & 0o222)
            or identity(before) != identity(named_before)
        ):
            raise RuntimeError(f"{label} source identity mismatch")
        chunks: list[bytes] = []
        offset = 0
        digest = hashlib.sha256()
        while True:
            block = os.pread(descriptor, 16 * 2**20, offset)
            if not block:
                break
            chunks.append(block)
            digest.update(block)
            offset += len(block)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
        if (
            identity(before) != identity(after)
            or identity(after) != identity(named_after)
            or (require_immutable and after.st_mode & 0o222)
            or digest.hexdigest() != expected_sha256
        ):
            raise RuntimeError(f"{label} source hash/custody mismatch")
        return raw
    finally:
        os.close(descriptor)


def _apply_exact_launcher_replacements(old_raw: bytes) -> bytes:
    result = old_raw
    for ordinal, (anchor, replacement) in enumerate(
        EXACT_LAUNCHER_REPLACEMENTS, start=1,
    ):
        if result.count(anchor) != 1:
            raise Refusal(
                f"launcher repair anchor {ordinal} does not occur exactly once"
            )
        result = result.replace(anchor, replacement, 1)
    return result


def _retired_source_bytes(
    root: Path,
    census: Mapping[str, object],
    relative: str,
    expected_sha256: str,
    label: str,
) -> bytes:
    entry = _entry_by_path(census, relative)
    if entry.get("kind") != "file" or entry.get("sha256") != expected_sha256:
        raise Refusal(f"{label} retirement census binding mismatch")
    custody = root.joinpath(*PurePosixPath(str(census["custody_root"])).parts)
    source = retirement.destination(custody, entry)
    retirement.inspect_entry(source, entry)
    try:
        return _read_pinned_source_bytes(
            source, expected_sha256, label, require_immutable=True,
        )
    except RuntimeError as error:
        raise Refusal(str(error)) from error


def derive_repaired_source_bytes(
    root: Path, census: Mapping[str, object],
) -> dict[str, bytes]:
    """Derive both new canonical sources from frozen, independently bound bytes."""
    old_launcher = _retired_source_bytes(
        root, census, OLD_CANONICAL_LAUNCHER_PATH,
        OLD_CANONICAL_LAUNCHER_SHA256, "retired canonical launcher",
    )
    candidate_path = root.joinpath(
        *PurePosixPath(REPAIRED_LAUNCHER_CANDIDATE_PATH).parts
    )
    try:
        candidate = _read_pinned_source_bytes(
            candidate_path, REPAIRED_CANONICAL_LAUNCHER_SHA256,
            "frozen repaired launcher candidate", require_immutable=True,
        )
    except RuntimeError as error:
        raise Refusal(str(error)) from error
    derived_launcher = _apply_exact_launcher_replacements(old_launcher)
    if candidate != derived_launcher:
        raise Refusal("repaired launcher candidate differs from exact transformation")
    if retirement.sha256_bytes(derived_launcher) \
            != REPAIRED_CANONICAL_LAUNCHER_SHA256:
        raise Refusal("exact launcher transformation digest mismatch")

    old_builder = _retired_source_bytes(
        root, census, OLD_CANONICAL_BUILDER_PATH,
        OLD_CANONICAL_BUILDER_SHA256, "retired canonical builder",
    )
    old_binding = OLD_CANONICAL_LAUNCHER_SHA256.encode("ascii")
    new_binding = REPAIRED_CANONICAL_LAUNCHER_SHA256.encode("ascii")
    if old_builder.count(old_binding) != 1 or old_builder.count(new_binding) != 0:
        raise Refusal("retired builder launcher binding census mismatch")
    derived_builder = old_builder.replace(old_binding, new_binding, 1)
    if retirement.sha256_bytes(derived_builder) \
            != REPAIRED_CANONICAL_BUILDER_SHA256:
        raise Refusal("exact builder transformation digest mismatch")
    return {
        OLD_CANONICAL_LAUNCHER_PATH: derived_launcher,
        OLD_CANONICAL_BUILDER_PATH: derived_builder,
    }


def _retained_parent_chain(root: Path, path: Path, label: str) -> list[int]:
    retirement.ensure_root(root)
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise Refusal(f"{label} is outside the canonical root") from error
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptors: list[int] = []
    try:
        descriptors.append(os.open(root, flags))
        for part in relative.parent.parts:
            descriptor = os.open(part, flags, dir_fd=descriptors[-1])
            metadata = os.fstat(descriptor)
            named = os.stat(part, dir_fd=descriptors[-1], follow_symlinks=False)
            if (
                not stat.S_ISDIR(metadata.st_mode)
                or stat.S_ISLNK(named.st_mode)
                or retirement.descriptor_identity(metadata)
                != retirement.descriptor_identity(named)
            ):
                os.close(descriptor)
                raise Refusal(f"{label} parent chain is aliased")
            descriptors.append(descriptor)
        return descriptors
    except (OSError, ValueError) as error:
        for descriptor in reversed(descriptors):
            os.close(descriptor)
        raise Refusal(f"{label} parent chain authentication failed") from error
    except BaseException:
        for descriptor in reversed(descriptors):
            os.close(descriptor)
        raise


def _close_descriptors(descriptors: Sequence[int]) -> None:
    for descriptor in reversed(descriptors):
        os.close(descriptor)


def _read_owner_once_source_beneath(
    root: Path, path: Path, expected_sha256: str, label: str,
) -> bytes:
    parents = _retained_parent_chain(root, path, label)
    descriptor = -1
    try:
        descriptor = os.open(
            path.name,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parents[-1],
        )
        before = os.fstat(descriptor)
        named_before = os.stat(
            path.name, dir_fd=parents[-1], follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named_before.st_mode)
            or before.st_nlink != 1 or before.st_mode & 0o222
            or retirement.descriptor_identity(before)
            != retirement.descriptor_identity(named_before)
        ):
            raise Refusal(f"{label} is not an owner-once regular file")
        raw = bytearray()
        offset = 0
        while True:
            block = os.pread(descriptor, 16 * 2**20, offset)
            if not block:
                break
            raw.extend(block)
            offset += len(block)
        after = os.fstat(descriptor)
        named_after = os.stat(
            path.name, dir_fd=parents[-1], follow_symlinks=False,
        )
        if (
            retirement.descriptor_identity(before)
            != retirement.descriptor_identity(after)
            or retirement.descriptor_identity(after)
            != retirement.descriptor_identity(named_after)
            or retirement.descriptor_sha256(descriptor) != expected_sha256
        ):
            raise Refusal(f"{label} changed while held")
        return bytes(raw)
    except OSError as error:
        raise Refusal(f"{label} open failed") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        _close_descriptors(parents)


def _publish_owner_once_source(
    root: Path, path: Path, raw: bytes, expected_sha256: str,
) -> None:
    if retirement.sha256_bytes(raw) != expected_sha256:
        raise Refusal("repaired source publication input digest mismatch")
    parents = _retained_parent_chain(root, path, "repaired source publication")
    descriptor = -1
    try:
        descriptor = os.open(
            path.name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            0o400, dir_fd=parents[-1],
        )
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise Refusal("repaired source write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        metadata = os.fstat(descriptor)
        named = os.stat(
            path.name, dir_fd=parents[-1], follow_symlinks=False,
        )
        if (
            metadata.st_nlink != 1 or metadata.st_mode & 0o222
            or retirement.descriptor_identity(metadata)
            != retirement.descriptor_identity(named)
            or retirement.descriptor_sha256(descriptor) != expected_sha256
        ):
            raise Refusal("repaired source publication authentication mismatch")
        os.fsync(parents[-1])
    except FileExistsError as error:
        raise Refusal(f"repaired source destination already exists: {path}") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        _close_descriptors(parents)
    observed = _read_owner_once_source_beneath(
        root, path, expected_sha256, "new repaired canonical source",
    )
    if observed != raw:
        raise Refusal("repaired source publication byte mismatch")


def reconcile_or_publish_repaired_sources(
    root: Path, census: Mapping[str, object],
) -> dict[str, object]:
    """Publish the exact source pair once, or reconcile only a complete pair.

    A crash between the two owner-once publications is preserved and refused;
    the operator must adjudicate that partial boundary rather than overwrite it.
    """
    retirement.ensure_root(root)
    expected = derive_repaired_source_bytes(root, census)
    paths = {
        relative: root.joinpath(*PurePosixPath(relative).parts)
        for relative in expected
    }
    present = {
        relative: retirement.path_exists(path)
        for relative, path in paths.items()
    }
    if any(present.values()) and not all(present.values()):
        raise Refusal("partial repaired source publication is preserved and refused")
    if all(present.values()):
        for relative, raw in expected.items():
            expected_sha = (
                REPAIRED_CANONICAL_LAUNCHER_SHA256
                if relative == OLD_CANONICAL_LAUNCHER_PATH
                else REPAIRED_CANONICAL_BUILDER_SHA256
            )
            try:
                observed = _read_owner_once_source_beneath(
                    root, paths[relative], expected_sha,
                    f"reconciled repaired source {relative}",
                )
            except (OSError, RuntimeError) as error:
                raise Refusal(str(error)) from error
            if observed != raw:
                raise Refusal("completed repaired source publication differs")
        return {
            "classification": "PASS_RECONCILED_COMPLETE_REPAIRED_SOURCE_PAIR",
            "reconciled": True,
            "sha256_by_path": {
                OLD_CANONICAL_LAUNCHER_PATH: REPAIRED_CANONICAL_LAUNCHER_SHA256,
                OLD_CANONICAL_BUILDER_PATH: REPAIRED_CANONICAL_BUILDER_SHA256,
            },
        }

    _publish_owner_once_source(
        root,
        paths[OLD_CANONICAL_LAUNCHER_PATH],
        expected[OLD_CANONICAL_LAUNCHER_PATH],
        REPAIRED_CANONICAL_LAUNCHER_SHA256,
    )
    _publish_owner_once_source(
        root,
        paths[OLD_CANONICAL_BUILDER_PATH],
        expected[OLD_CANONICAL_BUILDER_PATH],
        REPAIRED_CANONICAL_BUILDER_SHA256,
    )
    return {
        "classification": "PASS_OWNER_ONCE_REPAIRED_SOURCE_PAIR_PUBLICATION",
        "reconciled": False,
        "sha256_by_path": {
            OLD_CANONICAL_LAUNCHER_PATH: REPAIRED_CANONICAL_LAUNCHER_SHA256,
            OLD_CANONICAL_BUILDER_PATH: REPAIRED_CANONICAL_BUILDER_SHA256,
        },
    }


def _load_authenticated_module(name: str):
    try:
        relative, expected = PINNED_EXECUTABLE_DEPENDENCIES[name]
        prerequisites = PINNED_MODULE_PREREQUISITES[name]
    except KeyError as error:
        raise RuntimeError(f"unregistered executable dependency: {name}") from error
    path = ROOT.joinpath(*PurePosixPath(relative).parts)
    existing = sys.modules.get(name)
    if existing is not None:
        if (
            Path(getattr(existing, "__file__", "")).resolve() != path.resolve()
            or getattr(existing, "__authenticated_sha256__", None) != expected
        ):
            raise RuntimeError(f"executable dependency name is aliased: {name}")
        return existing
    for prerequisite in prerequisites:
        _load_authenticated_module(prerequisite)
    raw = _read_pinned_source_bytes(path, expected, name)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = expected
    sys.modules[name] = module
    try:
        code = compile(raw, str(path), "exec", dont_inherit=True)
        exec(code, module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    # Execution consumed the retained bytes above.  A post-execution read is a
    # custody alarm only; no source path is used to obtain executable code.
    _read_pinned_source_bytes(path, expected, name)
    return module


def _load_retirement_module():
    return _load_authenticated_module("v012_exact_retirement_for_replay")


retirement = _load_retirement_module()
Refusal = retirement.Refusal


TEMPLATE_PATH_BY_ARTIFACT: Final[dict[str, str]] = {
    "A01_FREEZE_AND_SOURCE_PACKET":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/FREEZE.json",
    "A03_PREPAYLOAD_AUDIT":
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json",
    "A04_UNIVERSAL_CUSTODY_GATE":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
    "A07_BASE_PHYSICAL_GATE":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "PHYSICAL_EXECUTION_GATE_V012.json",
    "A08_PHYSICAL_GATE_AUDIT":
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "PHYSICAL_GATE_HOSTILE_AUDIT_V001.json",
    "A09_CONTROL_AUTHORIZATION":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json",
    "A11_CONTROL_STAGE_GATE":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHED_CONTROL_L4_L8_GATE_V012.json",
    "A12_CONTROL_STAGE_AUDIT":
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
    "A13_L10_AUTHORIZATION":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
    "A15_L10_STAGE_GATE":
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_V012.json",
    "A16_L10_STAGE_AUDIT":
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/"
        "CACHED_L10_GATE_AUDIT_V001.json",
}


# These are the complete permitted changes to each retired authority.  Every
# listed pointer is required for a replay; no unlisted field can be supplied.
DYNAMIC_POINTERS: Final[dict[str, frozenset[str]]] = {
    "A01_FREEZE_AND_SOURCE_PACKET": frozenset({
        "/files/build_target_cache.py",
        "/files/production_obligation_validators.py",
        "/sealed_dependencies/v012_dual_launch_coordinator_packet/"
        "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001~1"
        "production_dual_l12_launcher.py",
    }),
    "A03_PREPAYLOAD_AUDIT": frozenset({
        "/audited_files_sha256/build_target_cache.py",
        "/audited_files_sha256/production_obligation_validators.py",
        "/audited_freeze_sha256",
        "/preflight_result_sha256",
        "/mutation_ledger/sha256",
        "/mutation_ledger/validator_module_sha256",
    }),
    "A04_UNIVERSAL_CUSTODY_GATE": frozenset({
        "/builder_sha256",
        "/freeze_sha256", "/preflight_result_sha256",
        "/independent_hostile_audit/sha256",
    }),
    "A07_BASE_PHYSICAL_GATE": frozenset({
        "/builder_sha256",
        "/freeze_sha256", "/preflight_result_sha256",
        "/independent_hostile_audit_sha256", "/dual_obstruction_gate_sha256",
        "/cache_manifest_sha256_by_L/4", "/cache_manifest_sha256_by_L/6",
        "/cache_manifest_sha256_by_L/8", "/cache_manifest_sha256_by_L/10",
        "/cache_manifest_sha256_by_L/12",
        "/postbuild_payload_audit/sha256",
    }),
    "A08_PHYSICAL_GATE_AUDIT": frozenset({
        "/freeze_sha256", "/physical_execution_gate_sha256",
        "/postbuild_payload_audit_sha256",
    }),
    "A09_CONTROL_AUTHORIZATION": frozenset({
        "/builder_sha256",
        "/freeze_sha256", "/preflight_result_sha256",
        "/postbuild_payload_audit/sha256",
        "/physical_execution_gate/sha256",
        "/physical_gate_hostile_audit/sha256",
    }),
    "A11_CONTROL_STAGE_GATE": frozenset({
        "/builder_sha256",
        "/freeze_sha256", "/preflight_result_sha256",
        "/independent_hostile_audit_sha256", "/physical_execution_gate_sha256",
        "/cache_manifest_sha256_by_L/4", "/cache_manifest_sha256_by_L/6",
        "/cache_manifest_sha256_by_L/8",
        "/histories/0/sha256", "/histories/1/sha256", "/histories/2/sha256",
    }),
    "A12_CONTROL_STAGE_AUDIT": frozenset({
        "/stage_gate_sha256", "/history_sha256_by_L/4",
        "/history_sha256_by_L/6", "/history_sha256_by_L/8",
    }),
    "A13_L10_AUTHORIZATION": frozenset({
        "/builder_sha256",
        "/freeze_sha256", "/physical_execution_gate_sha256",
        "/cached_control_l4_l8_gate_sha256",
        "/cached_control_l4_l8_gate_audit_sha256",
        "/l10_cache_manifest_sha256",
    }),
    "A15_L10_STAGE_GATE": frozenset({
        "/builder_sha256",
        "/freeze_sha256", "/preflight_result_sha256",
        "/independent_hostile_audit_sha256", "/physical_execution_gate_sha256",
        "/cache_manifest_sha256_by_L/10",
        "/cached_control_l4_l8_gate_sha256",
        "/l10_execution_authorization_gate_sha256", "/histories/0/sha256",
    }),
    "A16_L10_STAGE_AUDIT": frozenset({
        "/stage_gate_sha256", "/l10_execution_authorization_gate_sha256",
        "/history_sha256_by_L/10",
    }),
}


HOSTILE_A17_RESTORE_PATHS: Final[tuple[str, ...]] = (
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
    "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
    "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/"
    "L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES",
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS",
)

RESTORE_INTENT_NAME: Final[str] = "HOSTILE_A17_RESTORE_INTENT_V001.json"
RESTORE_EVENT_DIRECTORY_NAME: Final[str] = "HOSTILE_A17_RESTORE_EVENTS_V001"
RESTORE_RECEIPT_NAME: Final[str] = "HOSTILE_A17_RESTORE_RECEIPT_V001.json"


class PublisherAction(NamedTuple):
    artifact_id: str
    instance: int
    command: tuple[str, ...]


REPLAY_SEQUENCE: Final[tuple[tuple[str, str, int], ...]] = (
    ("template", "A01_FREEZE_AND_SOURCE_PACKET", 1),
    ("publisher", "A02_NONPHYSICAL_PREFLIGHT", 1),
    ("template", "A03_PREPAYLOAD_AUDIT", 1),
    ("template", "A04_UNIVERSAL_CUSTODY_GATE", 1),
    *(("publisher", "A05_FIVE_CACHE_SET", instance)
      for instance in range(1, 6)),
    ("publisher", "A06_POSTBUILD_AUDIT", 1),
    ("template", "A07_BASE_PHYSICAL_GATE", 1),
    ("template", "A08_PHYSICAL_GATE_AUDIT", 1),
    ("template", "A09_CONTROL_AUTHORIZATION", 1),
    *(("publisher", "A10_CONTROL_HISTORIES", instance)
      for instance in range(1, 4)),
    ("template", "A11_CONTROL_STAGE_GATE", 1),
    ("template", "A12_CONTROL_STAGE_AUDIT", 1),
    ("template", "A13_L10_AUTHORIZATION", 1),
    ("publisher", "A14_L10_HISTORY", 1),
    ("template", "A15_L10_STAGE_GATE", 1),
    ("template", "A16_L10_STAGE_AUDIT", 1),
    ("restore", "A17_HOSTILE_L12_ELIGIBILITY", 1),
    ("construct", "A18_L10_CROSS_GATE", 1),
)


PUBLISHED_PATH_BY_INSTANCE: Final[dict[tuple[str, int], str]] = {
    (artifact_id, 1): path
    for artifact_id, path in TEMPLATE_PATH_BY_ARTIFACT.items()
}
PUBLISHED_PATH_BY_INSTANCE.update({
    ("A02_NONPHYSICAL_PREFLIGHT", 1):
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_RESULT_V001.json",
    ("A06_POSTBUILD_AUDIT", 1):
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/POSTBUILD_PAYLOAD_AUDIT_V001.json",
    ("A18_L10_CROSS_GATE", 1): A18_CANONICAL_PATH,
})
for _instance, _length in enumerate((4, 6, 8, 10, 12), start=1):
    PUBLISHED_PATH_BY_INSTANCE[("A05_FIVE_CACHE_SET", _instance)] = (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        f"CACHE_PAYLOADS_V012/L{_length}/CACHE_MANIFEST.json"
    )
for _instance, _length in enumerate((4, 6, 8), start=1):
    PUBLISHED_PATH_BY_INSTANCE[("A10_CONTROL_HISTORIES", _instance)] = (
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
        f"PHYSICAL_OUTPUTS/HISTORY_L{_length}.json"
    )
PUBLISHED_PATH_BY_INSTANCE[("A14_L10_HISTORY", 1)] = (
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L10.json"
)
MUTATION_LEDGER_PATH: Final[str] = (
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
    "PREFLIGHT_MUTATION_LEDGER_V001.json"
)


def existing_publisher_actions(
    cache_hashes: Mapping[int, str] | None = None,
) -> tuple[PublisherAction, ...]:
    """Return only the existing A02/A05/A06/A10/A14 publisher invocations."""
    hashes = dict(cache_hashes or {})
    for length, digest in hashes.items():
        if length not in {4, 6, 8, 10, 12} or not _sha256_text(digest):
            raise Refusal("publisher cache-hash map mismatch")
    actions: list[PublisherAction] = [PublisherAction(
        "A02_NONPHYSICAL_PREFLIGHT", 1,
        ("python3", "-B",
         "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/validate_preflight.py"),
    )]
    for instance, length in enumerate((4, 6, 8, 10, 12), start=1):
        actions.append(PublisherAction(
            "A05_FIVE_CACHE_SET", instance,
            ("python3", "-B",
             "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py",
             "--length", str(length), "--output",
             "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
             f"CACHE_PAYLOADS_V012/L{length}"),
        ))
    actions.append(PublisherAction(
        "A06_POSTBUILD_AUDIT", 1,
        ("python3", "-B",
         "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/"
         "independent_postbuild_auditor.py", "--publish"),
    ))
    for instance, length in enumerate((4, 6, 8, 10), start=1):
        digest = hashes.get(length, "<fresh-cache-manifest-sha256>")
        actions.append(PublisherAction(
            "A10_CONTROL_HISTORIES" if length < 10 else "A14_L10_HISTORY",
            instance if length < 10 else 1,
            ("python3", "-B",
             "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py",
             "execute", "--length", str(length), "--cache-root",
             "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
             f"CACHE_PAYLOADS_V012/L{length}", "--cache-manifest-sha256", digest,
             "--output", "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
             f"PHYSICAL_OUTPUTS/HISTORY_L{length}.json", "--workspace",
             "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/"
             f"L{length}"),
        ))
    return tuple(actions)


def run_existing_publisher(
    action: PublisherAction,
    runner: Callable[[Sequence[str]], int],
) -> None:
    """Invoke an enumerated publisher only through a caller-supplied runner."""
    if action not in existing_publisher_actions(_hashes_from_action(action)):
        raise Refusal("unregistered existing publisher action")
    result = runner(action.command)
    if type(result) is not int or result != 0:
        raise Refusal(f"existing publisher failed: {action.artifact_id}")


def _stable_owner_once_sha256(path: Path, label: str) -> str:
    identity = retirement.retained_file_identity(path, label)
    if identity["mode"] & 0o222:
        raise Refusal(f"{label} is writable after owner-once publication")
    return str(identity["sha256"])


def _stable_owner_once_json(
    path: Path, label: str,
) -> tuple[dict[str, object], str, bytes]:
    """Read one immutable JSON inode without a path re-open race."""
    flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise Refusal(f"{label} open failed") from error
    try:
        before = os.fstat(descriptor)
        named_before = os.stat(path, follow_symlinks=False)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_ISLNK(named_before.st_mode)
            or before.st_nlink != 1
            or before.st_mode & 0o222
            or retirement.descriptor_identity(before)
            != retirement.descriptor_identity(named_before)
        ):
            raise Refusal(f"{label} is not an owner-once regular file")
        chunks: list[bytes] = []
        offset = 0
        while True:
            block = os.pread(descriptor, 16 * 2**20, offset)
            if not block:
                break
            chunks.append(block)
            offset += len(block)
        raw = b"".join(chunks)
        digest = retirement.sha256_bytes(raw)
        after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
        if (
            retirement.descriptor_identity(before)
            != retirement.descriptor_identity(after)
            or retirement.descriptor_identity(after)
            != retirement.descriptor_identity(named_after)
            or retirement.descriptor_sha256(descriptor) != digest
        ):
            raise Refusal(f"{label} changed while held")
        return retirement.strict_json(raw, label), digest, raw
    finally:
        os.close(descriptor)


def _load_pinned_module(root: Path, name: str):
    try:
        if root != ROOT or name not in PINNED_LIVE_SOURCES:
            raise Refusal(f"unregistered live module: {name}")
        return _load_authenticated_module(name)
    except RuntimeError as error:
        raise Refusal(str(error)) from error


class ExactLiveReview:
    """Hash-pinned target plus independent validators for canonical replay."""

    def __init__(self, root: Path):
        if root != ROOT:
            raise Refusal("live replay root differs from the sealed repository")
        self.root = root
        self.validators = _load_pinned_module(root, "production_obligation_validators")
        self.builder = _load_pinned_module(root, "build_target_cache")
        self.consumer = _load_pinned_module(root, "consume_target_cache")
        self.independent = _load_pinned_module(root, "independent_final_auditor")
        self.reauthenticate_pinned_sources()

    def production_sink(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> None:
        self.validators.validate_record(
            artifact_id, dict(record),
            mutation_class="PRODUCTION_NATIVE_RECORD", fixture_mode=False,
        )

    def independent_sink(
        self, artifact_id: str, record: Mapping[str, object],
    ) -> None:
        self.independent._validate_independent_upstream_record(
            artifact_id, dict(record), f"REPLAY_{artifact_id}",
            fixture_mode=False,
        )

    def common_sinks(self) -> tuple[
        Callable[[str, Mapping[str, object]], None], ...
    ]:
        return (self.production_sink, self.independent_sink)

    def reauthenticate_pinned_sources(self) -> None:
        for name, (relative, expected) in PINNED_EXECUTABLE_DEPENDENCIES.items():
            path = self.root.joinpath(*PurePosixPath(relative).parts)
            try:
                _read_pinned_source_bytes(path, expected, name)
            except RuntimeError as error:
                raise Refusal(str(error)) from error
        for name, (relative, expected) in PINNED_REPAIRED_CANONICAL_SOURCES.items():
            path = self.root.joinpath(*PurePosixPath(relative).parts)
            try:
                _read_pinned_source_bytes(path, expected, name, require_immutable=True)
            except RuntimeError as error:
                raise Refusal(str(error)) from error

    def validate_completed_publisher(
        self,
        artifact_id: str,
        record: Mapping[str, object],
        *,
        mutation_ledger: Mapping[str, object] | None = None,
        mutation_ledger_sha: str | None = None,
    ) -> None:
        validate_with_sinks(
            artifact_id, record, self.common_sinks(), required_count=2,
        )
        if artifact_id == "A02_NONPHYSICAL_PREFLIGHT":
            if mutation_ledger is None or not _sha256_text(mutation_ledger_sha):
                raise Refusal("A02 completed publication lacks A27")
            validate_with_sinks(
                "A27_MUTATION_LEDGER", mutation_ledger,
                self.common_sinks(), required_count=2,
            )
            binding = record.get("mutation_ledger")
            if type(binding) is not dict or binding.get("sha256") != mutation_ledger_sha:
                raise Refusal("A02/A27 completed publication binding mismatch")
            freeze = self.builder.require_frozen_census()
            self.builder.require_preflight_mutation_ledger(
                dict(binding), freeze,
                _stable_owner_once_sha256(self.builder.FREEZE, "A01 freeze"),
            )
        elif mutation_ledger is not None or mutation_ledger_sha is not None:
            raise Refusal("mutation ledger supplied for a non-A02 publisher")
        self.reauthenticate_pinned_sources()

    def validate_freeze(self, record: Mapping[str, object]) -> None:
        self.builder.validate_freeze_document(dict(record))

    def validate_a03(
        self, record: Mapping[str, object], freeze: Mapping[str, object],
        preflight_sha: str,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="a03-replay-", dir=HERE) as directory:
            stage = Path(directory) / "A03.json"
            retirement.publish_once(stage, dict(record))
            relative = str(stage.relative_to(ROOT))
            old = self.builder.FUTURE_HOSTILE_AUDIT_PATH
            self.builder.FUTURE_HOSTILE_AUDIT_PATH = relative
            try:
                result = self.builder.require_future_v012_hostile_audit(
                    {"path": relative, "sha256": _stable_owner_once_sha256(stage, "A03 stage")},
                    dict(freeze), preflight_sha,
                )
                if retirement.canonical_json_bytes(result) != retirement.canonical_json_bytes(record):
                    raise Refusal("A03 live reconstruction returned different bytes")
            finally:
                self.builder.FUTURE_HOSTILE_AUDIT_PATH = old

    def validate_a04(
        self, record: Mapping[str, object], freeze: Mapping[str, object],
        preflight_sha: str,
    ) -> None:
        for length in (4, 6, 8, 10, 12):
            result = self.builder.validate_dual_gate_document(
                dict(record), length, dict(freeze), preflight_sha,
            )
            if retirement.canonical_json_bytes(result) != retirement.canonical_json_bytes(record):
                raise Refusal("A04 live reconstruction returned different bytes")

    def validate_control_triple(
        self,
        a07: Mapping[str, object],
        a08: Mapping[str, object],
        a09: Mapping[str, object],
        cache_hashes: Mapping[str, str],
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="a07-a09-replay-", dir=HERE) as directory:
            stage_root = Path(directory)
            paths = {
                "physical": stage_root / "A07.json",
                "audit": stage_root / "A08.json",
                "control": stage_root / "A09.json",
            }
            for key, record in (("physical", a07), ("audit", a08), ("control", a09)):
                retirement.publish_once(paths[key], dict(record))
            old_values = (
                self.consumer.PHYSICAL_GATE,
                self.consumer.PHYSICAL_GATE_HOSTILE_AUDIT,
                self.consumer.CONTROL_AUTHORIZATION_GATE,
                self.builder.safe_repo_file,
            )
            self.consumer.PHYSICAL_GATE = paths["physical"]
            self.consumer.PHYSICAL_GATE_HOSTILE_AUDIT = paths["audit"]
            self.consumer.CONTROL_AUTHORIZATION_GATE = paths["control"]
            original_safe_repo_file = self.builder.safe_repo_file

            def staged_safe_repo_file(
                relative: object, digest: object, label: str,
            ) -> Path:
                if relative == self.builder.FUTURE_PHYSICAL_GATE_AUDIT_PATH:
                    if digest != _stable_owner_once_sha256(paths["audit"], label):
                        raise self.builder.Refusal(
                            "staged physical-gate audit hash mismatch"
                        )
                    return paths["audit"]
                return original_safe_repo_file(relative, digest, label)

            self.builder.safe_repo_file = staged_safe_repo_file
            try:
                for length in (4, 6, 8):
                    result = self.consumer.require_physical_gate(
                        length, cache_hashes[str(length)],
                    )
                    if retirement.canonical_json_bytes(result["physical"]) != retirement.canonical_json_bytes(a07):
                        raise Refusal("A07 live reconstruction returned different bytes")
            finally:
                (
                    self.consumer.PHYSICAL_GATE,
                    self.consumer.PHYSICAL_GATE_HOSTILE_AUDIT,
                    self.consumer.CONTROL_AUTHORIZATION_GATE,
                    self.builder.safe_repo_file,
                ) = old_values

    def validate_stage_chain(
        self,
        a11: Mapping[str, object],
        a12: Mapping[str, object],
        a13: Mapping[str, object],
        cache_hashes: Mapping[str, str],
        a07_sha: str,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="a11-a13-replay-", dir=HERE) as directory:
            stage_root = Path(directory)
            paths = {name: stage_root / f"{name}.json" for name in ("A11", "A12", "A13")}
            for name, record in (("A11", a11), ("A12", a12), ("A13", a13)):
                retirement.publish_once(paths[name], dict(record))
            control = self.consumer.require_stage_gate(
                paths["A11"], "TARGET_V012_CACHED_CONTROL_L4_L8_GATE",
                "PASS_TARGET_V012_CACHED_CONTROLS_L4_L6_L8", (4, 6, 8),
                dict(cache_hashes), a07_sha, self.builder.require_frozen_census(),
            )
            _audit, audit_sha = self.consumer.require_stage_gate_audit(
                paths["A12"], paths["A11"], control,
                "TARGET_V012_CACHED_CONTROL_L4_L8_GATE_AUDIT_V001",
                "PASS_INDEPENDENT_TARGET_V012_CACHED_CONTROLS_L4_L8", (4, 6, 8),
            )
            old = self.consumer.L10_EXECUTION_AUTHORIZATION_GATE
            old_control = self.consumer.CACHED_CONTROL_GATE
            old_control_audit = self.consumer.CACHED_CONTROL_GATE_AUDIT
            self.consumer.L10_EXECUTION_AUTHORIZATION_GATE = paths["A13"]
            self.consumer.CACHED_CONTROL_GATE = paths["A11"]
            self.consumer.CACHED_CONTROL_GATE_AUDIT = paths["A12"]
            try:
                result, _digest = self.consumer.require_l10_execution_authorization(
                    self.builder.require_frozen_census(), a07_sha,
                    dict(cache_hashes), control, audit_sha,
                )
                if retirement.canonical_json_bytes(result) != retirement.canonical_json_bytes(a13):
                    raise Refusal("A13 live reconstruction returned different bytes")
            finally:
                self.consumer.L10_EXECUTION_AUTHORIZATION_GATE = old
                self.consumer.CACHED_CONTROL_GATE = old_control
                self.consumer.CACHED_CONTROL_GATE_AUDIT = old_control_audit

    def validate_l10_stage_pair(
        self,
        a15: Mapping[str, object],
        a16: Mapping[str, object],
        cache_hashes: Mapping[str, str],
        a07_sha: str,
        a11_sha: str,
        a13_sha: str,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="a15-a16-replay-", dir=HERE) as directory:
            stage_root = Path(directory)
            stage = stage_root / "A15.json"
            audit = stage_root / "A16.json"
            retirement.publish_once(stage, dict(a15))
            retirement.publish_once(audit, dict(a16))
            result = self.consumer.require_stage_gate(
                stage, "TARGET_V012_CACHED_L10_GATE",
                "PASS_TARGET_V012_CACHED_L10", (10,), dict(cache_hashes),
                a07_sha, self.builder.require_frozen_census(), a11_sha, a13_sha,
            )
            checked, _digest = self.consumer.require_stage_gate_audit(
                audit, stage, result,
                "TARGET_V012_CACHED_L10_GATE_AUDIT_V001",
                "PASS_INDEPENDENT_TARGET_V012_CACHED_L10", (10,), a13_sha,
            )
            if retirement.canonical_json_bytes(checked) != retirement.canonical_json_bytes(a16):
                raise Refusal("A16 live reconstruction returned different bytes")

    def validate_a17_branch(
        self, branch: Mapping[str, object],
    ) -> dict[str, object]:
        target_result = self.consumer._validate_shared_branch(
            dict(branch), "hostile_v004r4",
        )
        self.production_sink("A17_HOSTILE_L12_ELIGIBILITY", branch)
        sources = [
            {
                "label": label,
                "path": branch[label]["path"],
                "sha256": branch[label]["sha256"],
            }
            for label in self.independent.A17_SOURCE_LABELS
        ]
        digest = retirement.sha256_bytes(retirement.canonical_json_bytes(branch))
        row = {
            "artifact_id": "A17_HOSTILE_L12_ELIGIBILITY",
            "instance": 1,
            "sources": sources,
            "sha256": digest,
        }
        (
            artifact_id, instance, independent_branch, independent_digest,
            retained, _paths, metadata,
        ) = self.independent._a17_authority_binding(
            row, "REPLAY_A17_HOSTILE_L12_ELIGIBILITY", False,
        )
        try:
            if (
                artifact_id != "A17_HOSTILE_L12_ELIGIBILITY" or instance != 1
                or independent_digest != digest
                or retirement.canonical_json_bytes(independent_branch)
                != retirement.canonical_json_bytes(branch)
                or not set(self.independent.A17_RECORD_IDENTITIES).issubset(
                    target_result
                )
            ):
                raise Refusal("A17 target/independent reconstruction mismatch")
        finally:
            self.independent._verify_close_authority_inputs(retained)
        return metadata

    def validate_a18(
        self,
        record: Mapping[str, object],
        produced: Mapping[tuple[str, int], str],
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="a18-replay-", dir=HERE) as directory:
            stage = Path(directory) / "A18.json"
            retirement.publish_once(stage, dict(record))
            old = self.consumer.TARGET_HOSTILE_L10_CROSS_GATE
            self.consumer.TARGET_HOSTILE_L10_CROSS_GATE = stage
            try:
                freeze = self.builder.require_frozen_census()
                cache_hashes = {
                    str(length): produced[("A05_FIVE_CACHE_SET", instance)]
                    for instance, length in enumerate((4, 6, 8, 10, 12), start=1)
                }
                l10_stage = self.consumer.require_stage_gate(
                    self.consumer.CACHED_L10_GATE,
                    "TARGET_V012_CACHED_L10_GATE", "PASS_TARGET_V012_CACHED_L10",
                    (10,), cache_hashes, produced[("A07_BASE_PHYSICAL_GATE", 1)],
                    freeze, produced[("A11_CONTROL_STAGE_GATE", 1)],
                    produced[("A13_L10_AUTHORIZATION", 1)],
                )
                checked, checked_sha, _hostile_branch, _hostile_records = (
                    self.consumer.require_target_hostile_l10_cross_gate(
                        freeze, cache_hashes, l10_stage,
                        produced[("A16_L10_STAGE_AUDIT", 1)],
                    )
                )
                expected_sha = retirement.sha256_bytes(
                    retirement.publication_json_bytes(record)
                )
                if (
                    checked_sha != expected_sha
                    or retirement.canonical_json_bytes(checked)
                    != retirement.canonical_json_bytes(record)
                ):
                    raise Refusal("A18 live 65-check reconstruction mismatch")
            finally:
                self.consumer.TARGET_HOSTILE_L10_CROSS_GATE = old


def _publisher_action(
    artifact_id: str, instance: int, produced: Mapping[tuple[str, int], str],
) -> PublisherAction:
    cache_hashes = {
        length: produced[("A05_FIVE_CACHE_SET", cache_instance)]
        for cache_instance, length in enumerate((4, 6, 8, 10, 12), start=1)
        if ("A05_FIVE_CACHE_SET", cache_instance) in produced
    }
    matches = [
        action for action in existing_publisher_actions(cache_hashes)
        if action.artifact_id == artifact_id and action.instance == instance
    ]
    if len(matches) != 1:
        raise Refusal(f"publisher instance is not unique: {artifact_id}/{instance}")
    action = matches[0]
    if "<fresh-cache-manifest-sha256>" in action.command:
        raise Refusal(f"publisher predecessor is not measured: {artifact_id}/{instance}")
    return action


def _coordinate_with_injected_test_backend(
    root: Path,
    census: Mapping[str, object],
    update_provider: Callable[
        [str, Mapping[tuple[str, int], str]], Mapping[str, object]
    ],
    sinks_by_artifact: Mapping[
        str, Sequence[Callable[[str, Mapping[str, object]], None]]
    ],
    publisher_runner: Callable[[Sequence[str]], int],
    a18_update_provider: Callable[
        [Mapping[tuple[str, int], str]], Mapping[str, object]
    ],
    a18_target_sink: Callable[[str, Mapping[str, object]], None],
    a18_independent_sink: Callable[[str, Mapping[str, object]], None],
) -> dict[tuple[str, int], str]:
    """Synthetic-test harness for the one fixed replay DAG.

    It is intentionally private, is not a canonical execution path, and may
    only be used with temporary synthetic roots.  The live path below accepts
    no injected hashes, sinks, or runners.
    """
    if root == ROOT or ROOT in root.parents:
        raise Refusal("injected replay backend is synthetic-root only")
    produced: dict[tuple[str, int], str] = {}
    for operation, artifact_id, instance in REPLAY_SEQUENCE:
        if operation == "template":
            record = reconstruct_retired_authority(
                root, census, artifact_id,
                update_provider(artifact_id, dict(produced)),
                sinks_by_artifact.get(artifact_id, ()),
            )
            digest = publish_reconstructed_authority(root, artifact_id, record)
        elif operation == "publisher":
            action = _publisher_action(artifact_id, instance, produced)
            run_existing_publisher(action, publisher_runner)
            relative = PUBLISHED_PATH_BY_INSTANCE[(artifact_id, instance)]
            path = root.joinpath(*PurePosixPath(relative).parts)
            digest = _stable_owner_once_sha256(
                path, f"{artifact_id}/{instance} publication",
            )
            if artifact_id == "A02_NONPHYSICAL_PREFLIGHT":
                ledger = root.joinpath(*PurePosixPath(MUTATION_LEDGER_PATH).parts)
                produced[("A27_MUTATION_LEDGER", 1)] = _stable_owner_once_sha256(
                    ledger, "A27 mutation ledger publication",
                )
        elif operation == "restore":
            outcome = restore_completed_hostile_a17(root, census)
            digest = str(outcome["receipt_sha256"])
        elif operation == "construct":
            record = construct_a18(
                a18_update_provider(dict(produced)),
                a18_target_sink, a18_independent_sink,
            )
            digest = publish_a18(root, record)
        else:
            raise Refusal("internal replay operation mismatch")
        if not _sha256_text(digest):
            raise Refusal(f"{artifact_id}/{instance} produced invalid SHA-256")
        produced[(artifact_id, instance)] = digest
    if set(produced) != {
        (artifact_id, instance)
        for _operation, artifact_id, instance in REPLAY_SEQUENCE
    } | {("A27_MUTATION_LEDGER", 1)}:
        raise Refusal("completed replay product census mismatch")
    return produced


def _hashes_from_action(action: PublisherAction) -> dict[int, str]:
    command = action.command
    if "--cache-manifest-sha256" not in command:
        return {}
    index = command.index("--cache-manifest-sha256")
    length = int(command[command.index("--length") + 1])
    digest = command[index + 1]
    return {length: digest} if _sha256_text(digest) else {}


def _sha256_text(value: object) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _decode_pointer(pointer: str) -> tuple[str, ...]:
    if not pointer.startswith("/") or pointer == "/":
        raise Refusal("noncanonical JSON pointer")
    parts = pointer[1:].split("/")
    decoded = tuple(part.replace("~1", "/").replace("~0", "~") for part in parts)
    if any(not part for part in decoded):
        raise Refusal("empty JSON pointer component")
    return decoded


def _set_pointer(record: object, pointer: str, value: object) -> None:
    parts = _decode_pointer(pointer)
    current = record
    for part in parts[:-1]:
        if type(current) is dict:
            if part not in current:
                raise Refusal(f"dynamic pointer is absent: {pointer}")
            current = current[part]
        elif type(current) is list and part.isdigit():
            index = int(part)
            if index >= len(current):
                raise Refusal(f"dynamic pointer index is absent: {pointer}")
            current = current[index]
        else:
            raise Refusal(f"dynamic pointer parent mismatch: {pointer}")
    leaf = parts[-1]
    if type(current) is dict:
        if leaf not in current:
            raise Refusal(f"dynamic pointer leaf is absent: {pointer}")
        old = current[leaf]
        if type(old) is not type(value):
            raise Refusal(f"dynamic pointer type mismatch: {pointer}")
        current[leaf] = value
    elif type(current) is list and leaf.isdigit():
        index = int(leaf)
        if index >= len(current) or type(current[index]) is not type(value):
            raise Refusal(f"dynamic pointer list mismatch: {pointer}")
        current[index] = value
    else:
        raise Refusal(f"dynamic pointer target mismatch: {pointer}")


def _leaf_differences(left: object, right: object, base: str = "") -> set[str]:
    if type(left) is not type(right):
        return {base or "/"}
    if type(left) is dict:
        if set(left) != set(right):
            return {base or "/"}
        result: set[str] = set()
        for key in sorted(left):
            escaped = key.replace("~", "~0").replace("/", "~1")
            result |= _leaf_differences(left[key], right[key], f"{base}/{escaped}")
        return result
    if type(left) is list:
        if len(left) != len(right):
            return {base or "/"}
        result = set()
        for index, (a, b) in enumerate(zip(left, right)):
            result |= _leaf_differences(a, b, f"{base}/{index}")
        return result
    return set() if left == right else {base or "/"}


def update_authenticated_template(
    artifact_id: str,
    template: Mapping[str, object],
    updates: Mapping[str, object],
) -> dict[str, object]:
    allowed = DYNAMIC_POINTERS.get(artifact_id)
    if allowed is None:
        raise Refusal("artifact has no retired-template replay rule")
    if set(updates) != set(allowed):
        missing = sorted(set(allowed) - set(updates))
        extra = sorted(set(updates) - set(allowed))
        raise Refusal(f"dynamic binding census mismatch; missing={missing}, extra={extra}")
    result = copy.deepcopy(dict(template))
    for pointer in sorted(allowed):
        value = updates[pointer]
        if not _sha256_text(value):
            raise Refusal(f"dynamic SHA-256 mismatch: {pointer}")
        _set_pointer(result, pointer, value)
    differences = _leaf_differences(template, result)
    # Reusing an identical measured digest is legitimate, so differences may
    # be a strict subset.  Any actual difference still has to be enumerated.
    if not differences.issubset(allowed):
        raise Refusal("retired template changed outside dynamic binding census")
    return result


def _entry_by_path(census: Mapping[str, object], path: str) -> dict[str, object]:
    matches = [entry for entry in census["entries"] if entry["path"] == path]
    if len(matches) != 1 or type(matches[0]) is not dict:
        raise Refusal(f"retirement census lacks unique entry: {path}")
    return matches[0]


def load_retired_template(
    root: Path, census: Mapping[str, object], artifact_id: str,
) -> dict[str, object]:
    path = TEMPLATE_PATH_BY_ARTIFACT.get(artifact_id)
    if path is None:
        raise Refusal("unknown retired template artifact")
    entry = _entry_by_path(census, path)
    if entry.get("kind") != "file":
        raise Refusal("retired JSON template is not a file")
    custody = root.joinpath(*PurePosixPath(str(census["custody_root"])).parts)
    physical = retirement.destination(custody, entry)
    retirement.inspect_entry(physical, entry)
    record, digest, _raw = _stable_owner_once_json(
        physical, f"{artifact_id} retired template",
    )
    if digest != entry["sha256"]:
        raise Refusal(f"{artifact_id} retired-template digest mismatch")
    return record


def validate_with_sinks(
    artifact_id: str,
    record: Mapping[str, object],
    sinks: Sequence[Callable[[str, Mapping[str, object]], None]],
    *, required_count: int = 1,
) -> None:
    if len(sinks) < required_count:
        raise Refusal(f"{artifact_id} lacks required independent sinks")
    canonical = retirement.canonical_json_bytes(record)
    for sink in sinks:
        before = hashlib.sha256(canonical).hexdigest()
        sink(artifact_id, record)
        after = hashlib.sha256(retirement.canonical_json_bytes(record)).hexdigest()
        if after != before:
            raise Refusal(f"{artifact_id} sink mutated candidate bytes")


def reconstruct_retired_authority(
    root: Path,
    census: Mapping[str, object],
    artifact_id: str,
    updates: Mapping[str, object],
    sinks: Sequence[Callable[[str, Mapping[str, object]], None]],
) -> dict[str, object]:
    template = load_retired_template(root, census, artifact_id)
    result = update_authenticated_template(artifact_id, template, updates)
    validate_with_sinks(artifact_id, result, sinks)
    return result


def _measured_repaired_source_hashes(root: Path) -> tuple[str, str, str]:
    paths = {
        "builder": (
            OLD_CANONICAL_BUILDER_PATH, REPAIRED_CANONICAL_BUILDER_SHA256,
        ),
        "launcher": (
            OLD_CANONICAL_LAUNCHER_PATH, REPAIRED_CANONICAL_LAUNCHER_SHA256,
        ),
        "validator": PINNED_LIVE_SOURCES["production_obligation_validators"],
    }
    measured: dict[str, str] = {}
    for label, (relative, expected) in paths.items():
        path = root.joinpath(*PurePosixPath(relative).parts)
        observed = _stable_owner_once_sha256(path, f"repaired {label} source")
        if observed != expected:
            raise Refusal(f"repaired {label} source digest mismatch")
        measured[label] = observed
    return measured["builder"], measured["launcher"], measured["validator"]


def measured_template_updates(
    root: Path,
    artifact_id: str,
    produced: Mapping[tuple[str, int], str],
) -> dict[str, object]:
    """Derive every template update from a measured predecessor or source.

    There is no caller-supplied hash surface here.  A missing predecessor is a
    stage-order refusal, and all source hashes are measured through stable,
    owner-once descriptors.
    """
    def prior(name: str, instance: int = 1) -> str:
        value = produced.get((name, instance))
        if not _sha256_text(value):
            raise Refusal(f"{artifact_id} predecessor is absent: {name}/{instance}")
        return value

    builder_sha, launcher_sha, validator_sha = _measured_repaired_source_hashes(root)
    if artifact_id == "A01_FREEZE_AND_SOURCE_PACKET":
        result = {
            "/files/build_target_cache.py": builder_sha,
            "/files/production_obligation_validators.py": validator_sha,
            "/sealed_dependencies/v012_dual_launch_coordinator_packet/"
            "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001~1"
            "production_dual_l12_launcher.py": launcher_sha,
        }
    elif artifact_id == "A03_PREPAYLOAD_AUDIT":
        result = {
            "/audited_files_sha256/build_target_cache.py": builder_sha,
            "/audited_files_sha256/production_obligation_validators.py": validator_sha,
            "/audited_freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/preflight_result_sha256": prior("A02_NONPHYSICAL_PREFLIGHT"),
            "/mutation_ledger/sha256": prior("A27_MUTATION_LEDGER"),
            "/mutation_ledger/validator_module_sha256": validator_sha,
        }
    elif artifact_id == "A04_UNIVERSAL_CUSTODY_GATE":
        result = {
            "/builder_sha256": builder_sha,
            "/freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/preflight_result_sha256": prior("A02_NONPHYSICAL_PREFLIGHT"),
            "/independent_hostile_audit/sha256": prior("A03_PREPAYLOAD_AUDIT"),
        }
    elif artifact_id == "A07_BASE_PHYSICAL_GATE":
        result = {
            "/builder_sha256": builder_sha,
            "/freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/preflight_result_sha256": prior("A02_NONPHYSICAL_PREFLIGHT"),
            "/independent_hostile_audit_sha256": prior("A03_PREPAYLOAD_AUDIT"),
            "/dual_obstruction_gate_sha256": prior("A04_UNIVERSAL_CUSTODY_GATE"),
            **{
                f"/cache_manifest_sha256_by_L/{length}": prior(
                    "A05_FIVE_CACHE_SET", instance,
                )
                for instance, length in enumerate((4, 6, 8, 10, 12), start=1)
            },
            "/postbuild_payload_audit/sha256": prior("A06_POSTBUILD_AUDIT"),
        }
    elif artifact_id == "A08_PHYSICAL_GATE_AUDIT":
        result = {
            "/freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/physical_execution_gate_sha256": prior("A07_BASE_PHYSICAL_GATE"),
            "/postbuild_payload_audit_sha256": prior("A06_POSTBUILD_AUDIT"),
        }
    elif artifact_id == "A09_CONTROL_AUTHORIZATION":
        result = {
            "/builder_sha256": builder_sha,
            "/freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/preflight_result_sha256": prior("A02_NONPHYSICAL_PREFLIGHT"),
            "/postbuild_payload_audit/sha256": prior("A06_POSTBUILD_AUDIT"),
            "/physical_execution_gate/sha256": prior("A07_BASE_PHYSICAL_GATE"),
            "/physical_gate_hostile_audit/sha256": prior(
                "A08_PHYSICAL_GATE_AUDIT"
            ),
        }
    elif artifact_id == "A11_CONTROL_STAGE_GATE":
        result = {
            "/builder_sha256": builder_sha,
            "/freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/preflight_result_sha256": prior("A02_NONPHYSICAL_PREFLIGHT"),
            "/independent_hostile_audit_sha256": prior("A03_PREPAYLOAD_AUDIT"),
            "/physical_execution_gate_sha256": prior("A07_BASE_PHYSICAL_GATE"),
            **{
                f"/cache_manifest_sha256_by_L/{length}": prior(
                    "A05_FIVE_CACHE_SET", instance,
                )
                for instance, length in enumerate((4, 6, 8), start=1)
            },
            **{
                f"/histories/{instance - 1}/sha256": prior(
                    "A10_CONTROL_HISTORIES", instance,
                )
                for instance in range(1, 4)
            },
        }
    elif artifact_id == "A12_CONTROL_STAGE_AUDIT":
        result = {
            "/stage_gate_sha256": prior("A11_CONTROL_STAGE_GATE"),
            **{
                f"/history_sha256_by_L/{length}": prior(
                    "A10_CONTROL_HISTORIES", instance,
                )
                for instance, length in enumerate((4, 6, 8), start=1)
            },
        }
    elif artifact_id == "A13_L10_AUTHORIZATION":
        result = {
            "/builder_sha256": builder_sha,
            "/freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/physical_execution_gate_sha256": prior("A07_BASE_PHYSICAL_GATE"),
            "/cached_control_l4_l8_gate_sha256": prior("A11_CONTROL_STAGE_GATE"),
            "/cached_control_l4_l8_gate_audit_sha256": prior(
                "A12_CONTROL_STAGE_AUDIT"
            ),
            "/l10_cache_manifest_sha256": prior("A05_FIVE_CACHE_SET", 4),
        }
    elif artifact_id == "A15_L10_STAGE_GATE":
        result = {
            "/builder_sha256": builder_sha,
            "/freeze_sha256": prior("A01_FREEZE_AND_SOURCE_PACKET"),
            "/preflight_result_sha256": prior("A02_NONPHYSICAL_PREFLIGHT"),
            "/independent_hostile_audit_sha256": prior("A03_PREPAYLOAD_AUDIT"),
            "/physical_execution_gate_sha256": prior("A07_BASE_PHYSICAL_GATE"),
            "/cache_manifest_sha256_by_L/10": prior("A05_FIVE_CACHE_SET", 4),
            "/cached_control_l4_l8_gate_sha256": prior("A11_CONTROL_STAGE_GATE"),
            "/l10_execution_authorization_gate_sha256": prior(
                "A13_L10_AUTHORIZATION"
            ),
            "/histories/0/sha256": prior("A14_L10_HISTORY"),
        }
    elif artifact_id == "A16_L10_STAGE_AUDIT":
        result = {
            "/stage_gate_sha256": prior("A15_L10_STAGE_GATE"),
            "/l10_execution_authorization_gate_sha256": prior(
                "A13_L10_AUTHORIZATION"
            ),
            "/history_sha256_by_L/10": prior("A14_L10_HISTORY"),
        }
    else:
        raise Refusal(f"no measured template update map: {artifact_id}")
    if set(result) != set(DYNAMIC_POINTERS[artifact_id]):
        raise Refusal(f"internal measured binding census mismatch: {artifact_id}")
    return result


def publish_reconstructed_authority(
    root: Path,
    artifact_id: str,
    record: Mapping[str, object],
) -> str:
    relative = TEMPLATE_PATH_BY_ARTIFACT.get(artifact_id)
    if relative is None:
        raise Refusal("unknown reconstructed authority path")
    path = root.joinpath(*PurePosixPath(relative).parts)
    if not path.parent.is_dir() or path.parent.is_symlink():
        raise Refusal("canonical authority parent is absent or aliased")
    return retirement.publish_once(path, dict(record))


def _reconcile_or_publish_json(
    path: Path,
    record: Mapping[str, object],
    artifact_id: str,
    sinks: Sequence[Callable[[str, Mapping[str, object]], None]],
) -> tuple[str, bool]:
    """Publish once, or authenticate an identical completed publication.

    An existing byte is never replaced.  Reconciliation accepts only the
    exact canonical publication bytes that would have been written now and
    reruns every supplied sink over the authenticated record.
    """
    expected_raw = retirement.publication_json_bytes(dict(record))
    expected_sha = retirement.sha256_bytes(expected_raw)
    if retirement.path_exists(path):
        observed, observed_sha, observed_raw = _stable_owner_once_json(
            path, f"{artifact_id} reconciled publication",
        )
        if observed_sha != expected_sha or observed_raw != expected_raw:
            raise Refusal(f"{artifact_id} existing publication differs from replay")
        validate_with_sinks(artifact_id, observed, sinks, required_count=len(sinks))
        return observed_sha, True
    digest = retirement.publish_once(path, dict(record))
    if digest != expected_sha:
        raise Refusal(f"{artifact_id} publication digest mismatch")
    observed, observed_sha, observed_raw = _stable_owner_once_json(
        path, f"{artifact_id} new publication",
    )
    if observed_sha != digest or observed_raw != expected_raw:
        raise Refusal(f"{artifact_id} new publication reauthentication mismatch")
    validate_with_sinks(artifact_id, observed, sinks, required_count=len(sinks))
    return digest, False


def _load_completed_retirement_receipt(
    root: Path, census: Mapping[str, object],
) -> tuple[Path, dict[str, object], str]:
    custody = root.joinpath(*PurePosixPath(str(census["custody_root"])).parts)
    receipt_path = custody / retirement.RECEIPT_NAME
    if receipt_path.is_symlink() or not receipt_path.is_file():
        raise Refusal("completed retirement receipt is absent or aliased")
    receipt, receipt_sha, raw = _stable_owner_once_json(
        receipt_path, "completed retirement receipt",
    )
    expected_keys = {
        "schema", "classification", "census_sha256", "intent_sha256",
        "entry_count", "source_file_count", "source_total_bytes",
        "retired_paths", "canonical_destinations_absent_for_replay",
        "claim_boundary",
    }
    if (
        set(receipt) != expected_keys
        or receipt.get("schema")
        != "V012_A01_A17_OWNER_ONCE_RETIREMENT_RECEIPT_V001"
        or receipt.get("classification") != "PASS_EXACT_OWNER_ONCE_RETIREMENT"
        or receipt.get("census_sha256")
        != retirement.sha256_bytes(retirement.publication_json_bytes(census))
        or receipt.get("entry_count") != census["entry_count"]
        or receipt.get("source_file_count") != census["source_file_count"]
        or receipt.get("source_total_bytes") != census["source_total_bytes"]
        or receipt.get("retired_paths")
        != [entry["path"] for entry in census["entries"]]
        or receipt.get("canonical_destinations_absent_for_replay") is not True
        or receipt.get("claim_boundary")
        != "RETIREMENT_CUSTODY_ONLY__NO_A01_A18_REPLAY_OR_PROMOTION"
    ):
        raise Refusal("completed retirement receipt mismatch")
    intent_path = custody / retirement.INTENT_NAME
    _intent, intent_sha, _intent_raw = _stable_owner_once_json(
        intent_path, "completed retirement intent",
    )
    if intent_sha != receipt["intent_sha256"]:
        raise Refusal("completed retirement intent binding mismatch")
    return custody, receipt, receipt_sha


def _hostile_entries(census: Mapping[str, object]) -> list[dict[str, object]]:
    entries = [_entry_by_path(census, path) for path in HOSTILE_A17_RESTORE_PATHS]
    if [entry["path"] for entry in entries] != list(HOSTILE_A17_RESTORE_PATHS):
        raise Refusal("hostile restore ordering mismatch")
    return entries


def _restore_paths(custody: Path) -> tuple[Path, Path, Path]:
    return (
        custody / RESTORE_INTENT_NAME,
        custody / RESTORE_EVENT_DIRECTORY_NAME,
        custody / RESTORE_RECEIPT_NAME,
    )


def _expected_restore_intent(retirement_receipt_sha: str) -> dict[str, object]:
    return {
        "schema": "V012_HOSTILE_A17_OWNER_ONCE_RESTORE_INTENT_V001",
        "retirement_receipt_sha256": retirement_receipt_sha,
        "paths": list(HOSTILE_A17_RESTORE_PATHS),
        "entry_count": len(HOSTILE_A17_RESTORE_PATHS),
        "claim_boundary": "HOSTILE_A17_RESTORE_ONLY__NO_A18_OR_L12_AUTHORIZATION",
    }


def _identity_sha256(identity: Mapping[str, object]) -> str:
    return retirement.sha256_bytes(retirement.canonical_json_bytes(dict(identity)))


def _expected_restore_event(
    ordinal: int, entry: Mapping[str, object], identity_sha: str,
) -> dict[str, object]:
    return {
        "schema": "V012_HOSTILE_A17_OWNER_ONCE_RESTORE_EVENT_V001",
        "ordinal": ordinal,
        "path": entry["path"],
        "entry_sha256": retirement.sha256_bytes(
            retirement.canonical_json_bytes(dict(entry))
        ),
        "retained_identity_sha256": identity_sha,
        "retirement_source_absent": True,
        "canonical_destination_authenticated": True,
    }


def _expected_restore_receipt(
    entries: Sequence[Mapping[str, object]],
    retirement_receipt_sha: str,
    intent_sha: str,
    event_hashes: Sequence[str],
) -> dict[str, object]:
    return {
        "schema": "V012_HOSTILE_A17_OWNER_ONCE_RESTORE_RECEIPT_V001",
        "classification": "PASS_EXACT_COMPLETED_RETIREMENT_HOSTILE_RESTORE",
        "retirement_receipt_sha256": retirement_receipt_sha,
        "restore_intent_sha256": intent_sha,
        "event_sha256_by_ordinal": list(event_hashes),
        "paths": list(HOSTILE_A17_RESTORE_PATHS),
        "entry_count": len(entries),
        "source_file_count": sum(
            1 if entry["kind"] == "file" else int(entry["file_count"])
            for entry in entries
        ),
        "source_total_bytes": sum(
            int(entry["bytes"])
            if entry["kind"] == "file" else int(entry["total_bytes"])
            for entry in entries
        ),
        "claim_boundary": "HOSTILE_A17_RESTORE_ONLY__NO_A18_OR_L12_AUTHORIZATION",
    }


def _ordinary_event_directory(
    event_root: Path, *, require_immutable: bool = False,
) -> None:
    try:
        metadata = os.stat(event_root, follow_symlinks=False)
    except OSError as error:
        raise Refusal("hostile restore event directory is absent") from error
    if (
        not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode)
        or (require_immutable and metadata.st_mode & 0o222)
    ):
        raise Refusal("hostile restore event directory is aliased")


def _load_restore_events(
    event_root: Path,
    entries: Sequence[Mapping[str, object]],
    *,
    require_complete: bool,
) -> tuple[list[str], list[dict[str, object]]]:
    _ordinary_event_directory(event_root, require_immutable=require_complete)
    children = sorted(event_root.iterdir(), key=lambda path: path.name)
    if len(children) > len(entries):
        raise Refusal("hostile restore event census exceeds the restore census")
    expected_names = [f"EVENT_{ordinal:03d}.json" for ordinal in range(1, len(children) + 1)]
    if [child.name for child in children] != expected_names:
        raise Refusal("hostile restore event sequence is not a contiguous prefix")
    if require_complete and len(children) != len(entries):
        raise Refusal("completed hostile restore event census mismatch")
    hashes: list[str] = []
    records: list[dict[str, object]] = []
    for ordinal, (path, entry) in enumerate(zip(children, entries), start=1):
        record, digest, _raw = _stable_owner_once_json(
            path, f"hostile restore event {ordinal}",
        )
        if (
            record.get("schema")
            != "V012_HOSTILE_A17_OWNER_ONCE_RESTORE_EVENT_V001"
            or record.get("ordinal") != ordinal
            or record.get("path") != entry["path"]
            or record.get("entry_sha256")
            != retirement.sha256_bytes(
                retirement.canonical_json_bytes(dict(entry))
            )
            or not _sha256_text(record.get("retained_identity_sha256"))
            or record.get("retirement_source_absent") is not True
            or record.get("canonical_destination_authenticated") is not True
            or set(record) != {
                "schema", "ordinal", "path", "entry_sha256",
                "retained_identity_sha256", "retirement_source_absent",
                "canonical_destination_authenticated",
            }
        ):
            raise Refusal(f"hostile restore event {ordinal} mismatch")
        hashes.append(digest)
        records.append(record)
    if [child.name for child in sorted(event_root.iterdir(), key=lambda path: path.name)] \
            != expected_names:
        raise Refusal("hostile restore event directory changed while held")
    return hashes, records


def _reconcile_completed_hostile_restore(
    root: Path,
    census: Mapping[str, object],
    custody: Path,
    retirement_receipt_sha: str,
) -> dict[str, object]:
    entries = _hostile_entries(census)
    intent_path, event_root, receipt_path = _restore_paths(custody)
    intent, intent_sha, intent_raw = _stable_owner_once_json(
        intent_path, "completed hostile restore intent",
    )
    expected_intent = _expected_restore_intent(retirement_receipt_sha)
    if intent_raw != retirement.publication_json_bytes(expected_intent):
        raise Refusal("completed hostile restore intent mismatch")
    event_hashes, events = _load_restore_events(
        event_root, entries, require_complete=True,
    )
    for entry, event in zip(entries, events):
        source = retirement.destination(custody, dict(entry))
        target = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
        if retirement.path_exists(source) or not retirement.path_exists(target):
            raise Refusal("completed hostile restore custody state mismatch")
        retirement.inspect_entry(target, dict(entry))
        identity = retirement.retained_entry_identity(target, dict(entry))
        if _identity_sha256(identity) != event["retained_identity_sha256"]:
            raise Refusal("completed hostile restore identity mismatch")
    expected_receipt = _expected_restore_receipt(
        entries, retirement_receipt_sha, intent_sha, event_hashes,
    )
    receipt, receipt_sha, receipt_raw = _stable_owner_once_json(
        receipt_path, "completed hostile restore receipt",
    )
    if receipt_raw != retirement.publication_json_bytes(expected_receipt):
        raise Refusal("completed hostile restore receipt mismatch")
    return {
        "classification": receipt["classification"],
        "receipt_sha256": receipt_sha,
        "restored_entry_count": len(entries),
        "reconciled": True,
    }


def recover_interrupted_hostile_a17_restore(
    root: Path, census: Mapping[str, object],
) -> dict[str, object]:
    """Return an incomplete restore to the authenticated retired state."""
    retirement.ensure_root(root)
    custody, _retirement_receipt, retirement_receipt_sha = (
        _load_completed_retirement_receipt(root, census)
    )
    entries = _hostile_entries(census)
    intent_path, event_root, receipt_path = _restore_paths(custody)
    if retirement.path_exists(receipt_path):
        raise Refusal("completed hostile restore cannot be recovered")
    if not retirement.path_exists(intent_path):
        if not retirement.path_exists(event_root):
            return {"classification": "NO_INTERRUPTED_HOSTILE_RESTORE", "restored_entry_count": 0}
        _ordinary_event_directory(event_root)
        if list(event_root.iterdir()):
            raise Refusal("hostile restore events exist without an intent")
        for entry in entries:
            source = retirement.destination(custody, entry)
            target = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
            retirement.inspect_entry(source, entry)
            if retirement.path_exists(target):
                raise Refusal("hostile restore destination exists without an intent")
        os.rmdir(event_root)
        retirement.fsync_directory(custody)
        return {"classification": "RECOVERED_EMPTY_HOSTILE_RESTORE", "restored_entry_count": 0}
    intent, _intent_sha, intent_raw = _stable_owner_once_json(
        intent_path, "interrupted hostile restore intent",
    )
    del intent
    if intent_raw != retirement.publication_json_bytes(
        _expected_restore_intent(retirement_receipt_sha)
    ):
        raise Refusal("interrupted hostile restore intent mismatch")
    if not retirement.path_exists(event_root):
        for entry in entries:
            source = retirement.destination(custody, entry)
            target = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
            retirement.inspect_entry(source, entry)
            if retirement.path_exists(target):
                raise Refusal("hostile restore event directory lost before recovery")
        os.unlink(intent_path)
        retirement.fsync_directory(custody)
        return {
            "classification": "RECOVERED_HOSTILE_RESTORE_METADATA_CLEANUP",
            "restored_entry_count": 0,
        }
    event_hashes, events = _load_restore_events(
        event_root, entries, require_complete=False,
    )
    del event_hashes
    target_prefix: list[dict[str, object]] = []
    for entry in entries:
        source = retirement.destination(custody, entry)
        target = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
        source_exists = retirement.path_exists(source)
        target_exists = retirement.path_exists(target)
        if source_exists == target_exists:
            raise Refusal(f"interrupted hostile restore ambiguous custody: {entry['path']}")
        if target_exists:
            retirement.inspect_entry(target, entry)
            target_prefix.append(entry)
        else:
            retirement.inspect_entry(source, entry)
    expected_prefix = entries[:len(target_prefix)]
    if (
        target_prefix != expected_prefix
        or len(events) < max(0, len(target_prefix) - 1)
    ):
        raise Refusal("interrupted hostile restore ordering mismatch")
    for ordinal, event in enumerate(events, start=1):
        entry = entries[ordinal - 1]
        target = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
        source = retirement.destination(custody, entry)
        physical = target if retirement.path_exists(target) else source
        identity = retirement.retained_entry_identity(physical, entry)
        if _identity_sha256(identity) != event["retained_identity_sha256"]:
            raise Refusal("interrupted hostile restore event identity mismatch")
    os.chmod(event_root, 0o700)
    retirement.fsync_directory(event_root)
    retirement.fsync_directory(custody)
    for entry in reversed(target_prefix):
        source = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
        target = retirement.destination(custody, entry)
        retained = retirement.retained_entry_identity(source, entry)
        retirement.rename_exclusive(source, target)
        retirement.fsync_moved_entry(target, entry)
        retirement.fsync_directory(source.parent)
        retirement.fsync_directory(target.parent)
        retirement.inspect_entry(target, entry)
        if retirement.retained_entry_identity(target, entry) != retained:
            raise Refusal("hostile restore recovery identity changed")
    for child in sorted(event_root.iterdir(), reverse=True):
        os.unlink(child)
    os.rmdir(event_root)
    os.unlink(intent_path)
    retirement.fsync_directory(custody)
    return {
        "classification": "RECOVERED_INTERRUPTED_HOSTILE_A17_RESTORE",
        "restored_entry_count": len(target_prefix),
    }


def restore_completed_hostile_a17(
    root: Path,
    census: Mapping[str, object],
    *,
    inject_after: int | None = None,
) -> dict[str, object]:
    """Restore only A17 hostile entries from a completed retirement.

    Completed transactions reconcile without mutation.  An interrupted prior
    transaction is first authenticated and rolled back, then retried.
    """
    retirement.ensure_root(root)
    custody, _retirement_receipt, retirement_receipt_sha = (
        _load_completed_retirement_receipt(root, census)
    )
    entries = _hostile_entries(census)
    intent_path, event_root, receipt_path = _restore_paths(custody)
    if retirement.path_exists(receipt_path):
        return _reconcile_completed_hostile_restore(
            root, census, custody, retirement_receipt_sha,
        )
    if retirement.path_exists(intent_path) or retirement.path_exists(event_root):
        recover_interrupted_hostile_a17_restore(root, census)
    for entry in entries:
        source = retirement.destination(custody, entry)
        target = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
        retirement.inspect_entry(source, entry)
        if retirement.path_exists(target):
            raise Refusal(f"hostile restore destination is not absent: {entry['path']}")
    os.mkdir(event_root, 0o700)
    retirement.fsync_directory(custody)
    moved: list[dict[str, object]] = []
    try:
        intent = _expected_restore_intent(retirement_receipt_sha)
        intent_sha = retirement.publish_once(intent_path, intent)
        event_hashes: list[str] = []
        for ordinal, entry in enumerate(entries, start=1):
            source = retirement.destination(custody, entry)
            target = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
            retirement.make_parents_beneath(root, target)
            if os.stat(source.parent).st_dev != os.stat(target.parent).st_dev:
                raise Refusal("hostile restore attempted a cross-filesystem move")
            retained = retirement.retained_entry_identity(source, entry)
            retirement.rename_exclusive(source, target)
            # Record custody immediately after the atomic boundary so every
            # later failure, including fsync/authentication failure, rolls it
            # back in process.
            moved.append(entry)
            retirement.fsync_moved_entry(target, entry)
            retirement.fsync_directory(source.parent)
            retirement.fsync_directory(target.parent)
            retirement.inspect_entry(target, entry)
            if retirement.retained_entry_identity(target, entry) != retained:
                raise Refusal(f"hostile restore identity changed: {entry['path']}")
            event = _expected_restore_event(
                ordinal, entry, _identity_sha256(retained),
            )
            event_hashes.append(retirement.publish_once(
                event_root / f"EVENT_{ordinal:03d}.json", event,
            ))
            if inject_after == ordinal:
                raise retirement.InjectedInterruption(
                    f"injected hostile restore interruption after {ordinal}"
                )
        os.chmod(event_root, 0o555)
        retirement.fsync_directory(event_root)
        retirement.fsync_directory(custody)
        receipt = _expected_restore_receipt(
            entries, retirement_receipt_sha, intent_sha, event_hashes,
        )
        digest = retirement.publish_once(receipt_path, receipt)
        return {
            "classification": receipt["classification"],
            "receipt_sha256": digest,
            "restored_entry_count": len(entries),
        }
    except Exception as error:
        rollback_error: Exception | None = None
        try:
            for entry in reversed(moved):
                source = root.joinpath(*PurePosixPath(str(entry["path"])).parts)
                target = retirement.destination(custody, entry)
                retained = retirement.retained_entry_identity(source, entry)
                retirement.rename_exclusive(source, target)
                retirement.fsync_moved_entry(target, entry)
                retirement.fsync_directory(source.parent)
                retirement.fsync_directory(target.parent)
                retirement.inspect_entry(target, entry)
                if retirement.retained_entry_identity(target, entry) != retained:
                    raise Refusal("hostile restore rollback identity changed")
            if retirement.path_exists(event_root):
                os.chmod(event_root, 0o700)
                for child in sorted(event_root.iterdir(), reverse=True):
                    os.unlink(child)
                os.rmdir(event_root)
            if retirement.path_exists(intent_path):
                os.unlink(intent_path)
            retirement.fsync_directory(custody)
        except Exception as caught:
            rollback_error = caught
        if rollback_error is not None:
            raise Refusal(
                f"hostile restore failed and rollback refused: {error}; "
                f"rollback: {rollback_error}"
            ) from rollback_error
        raise Refusal(f"hostile restore failed and rolled back: {error}") from error


def a18_dynamic_pointers() -> frozenset[str]:
    pointers = {
        "/target/cached_L10_gate_sha256",
        "/target/cached_L10_gate_audit_sha256",
        "/target/history_sha256",
        "/hostile/cached_L10_gate_sha256",
        "/hostile/l10_execution_authorization_gate_sha256",
        "/hostile/independent_prepayload_audit_sha256",
        "/hostile/history_sha256",
    }
    for role in ("target", "hostile"):
        for binding in (
            "method", "builder", "consumer", "preflight", "freeze",
            "preflight_result", "independent_audit", "cached_L10_gate",
            "L12_cache_manifest",
        ):
            pointers.add(f"/{role}/branch/{binding}/path")
            pointers.add(f"/{role}/branch/{binding}/sha256")
    for q in range(10):
        pointers.add(f"/comparison_policy/terminal_projection_by_q/{q}/target_sha256")
        pointers.add(f"/comparison_policy/terminal_projection_by_q/{q}/hostile_sha256")
        pointers.add(f"/comparison_policy/terminal_projection_by_q/{q}/linf_abs_error")
    return frozenset(pointers)


A18_DYNAMIC_POINTERS: Final[frozenset[str]] = a18_dynamic_pointers()


def load_a18_candidate_template(path: Path = A18_OBSTRUCTION) -> dict[str, object]:
    obstruction, digest, _raw = _stable_owner_once_json(
        path, "authenticated A18 obstruction",
    )
    if digest != A18_OBSTRUCTION_SHA256:
        raise Refusal("authenticated A18 obstruction custody mismatch")
    candidate = obstruction.get("candidate_a18_record")
    if type(candidate) is not dict:
        raise Refusal("A18 obstruction candidate is absent")
    if (
        candidate.get("checks_total") != 65
        or candidate.get("checks_passed") != 65
        or sum(candidate.get("checks", {}).values()) != 65
        or candidate.get("failures") != []
        or candidate.get("comparison_policy", {}).get("physical_abs_tolerance")
        != 1.0e-8
    ):
        raise Refusal("A18 65-check comparison policy mismatch")
    return candidate


def construct_a18(
    updates: Mapping[str, object],
    target_sink: Callable[[str, Mapping[str, object]], None],
    independent_sink: Callable[[str, Mapping[str, object]], None],
    *,
    template: Mapping[str, object] | None = None,
) -> dict[str, object]:
    if set(updates) != set(A18_DYNAMIC_POINTERS):
        raise Refusal("A18 dynamic path/hash binding census mismatch")
    original = copy.deepcopy(dict(template or load_a18_candidate_template()))
    record = copy.deepcopy(original)
    for pointer in sorted(A18_DYNAMIC_POINTERS):
        value = updates[pointer]
        if pointer.endswith("sha256") and not _sha256_text(value):
            raise Refusal(f"A18 dynamic SHA-256 mismatch: {pointer}")
        if pointer.endswith("/path"):
            if type(value) is not str or not value.startswith(str(ROOT) + "/"):
                raise Refusal(f"A18 dynamic canonical path mismatch: {pointer}")
        _set_pointer(record, pointer, value)
    if not _leaf_differences(original, record).issubset(A18_DYNAMIC_POINTERS):
        raise Refusal("A18 constructor changed a formula, schema, or threshold")
    for immutable_key in (
        "schema", "classification", "auditor_role", "sealed_input_commit",
        "L", "comparison_policy", "checks", "checks_passed", "checks_total",
        "failures", "claim_boundary",
    ):
        if immutable_key == "comparison_policy":
            # Only terminal payload hashes may vary within this otherwise frozen
            # comparison policy.
            continue
        if record[immutable_key] != original[immutable_key]:
            raise Refusal("A18 immutable field drift")
    validate_with_sinks(
        "A18_L10_CROSS_GATE", record, (target_sink, independent_sink),
        required_count=2,
    )
    return record


def construct_live_a17_branch(review: ExactLiveReview) -> tuple[
    dict[str, object], dict[str, object]
]:
    template = load_a18_candidate_template()["hostile"]["branch"]
    branch = copy.deepcopy(template)
    for label in review.independent.A17_SOURCE_LABELS:
        path = Path(branch[label]["path"])
        branch[label]["sha256"] = _stable_owner_once_sha256(
            path, f"A17 hostile {label}",
        )
    metadata = review.validate_a17_branch(branch)
    return branch, metadata


def measured_a18_updates(
    review: ExactLiveReview,
    produced: Mapping[tuple[str, int], str],
    hostile_branch: Mapping[str, object],
    hostile_metadata: Mapping[str, object],
) -> dict[str, object]:
    template = load_a18_candidate_template()
    updates: dict[str, object] = {
        pointer: _pointer_value(template, pointer)
        for pointer in A18_DYNAMIC_POINTERS
    }
    target_branch = template["target"]["branch"]
    for role, branch in (("target", target_branch), ("hostile", hostile_branch)):
        for label in review.independent.A17_SOURCE_LABELS:
            path = Path(branch[label]["path"])
            digest = _stable_owner_once_sha256(
                path, f"A18 {role} branch {label}",
            )
            updates[f"/{role}/branch/{label}/path"] = str(path)
            updates[f"/{role}/branch/{label}/sha256"] = digest
    updates.update({
        "/target/cached_L10_gate_sha256": produced[("A15_L10_STAGE_GATE", 1)],
        "/target/cached_L10_gate_audit_sha256": produced[("A16_L10_STAGE_AUDIT", 1)],
        "/target/history_sha256": produced[("A14_L10_HISTORY", 1)],
        "/hostile/cached_L10_gate_sha256": hostile_branch["cached_L10_gate"]["sha256"],
        "/hostile/l10_execution_authorization_gate_sha256": (
            hostile_metadata["l10_execution_authorization_sha256"]
        ),
        "/hostile/independent_prepayload_audit_sha256": (
            hostile_branch["independent_audit"]["sha256"]
        ),
        "/hostile/history_sha256": hostile_metadata["history_sha256"],
    })
    target_history_path = review.consumer.PHYSICAL_OUTPUT_PARENT / "HISTORY_L10.json"
    hostile_history_path = (
        review.consumer.ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
        / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L10.json"
    )
    target_history, target_history_sha, _target_raw = _stable_owner_once_json(
        target_history_path, "A18 target L10 history",
    )
    hostile_history, hostile_history_sha, _hostile_raw = _stable_owner_once_json(
        hostile_history_path, "A18 hostile L10 history",
    )
    if (
        target_history_sha != produced[("A14_L10_HISTORY", 1)]
        or hostile_history_sha != hostile_metadata["history_sha256"]
    ):
        raise Refusal("A18 history binding mismatch")
    target_shards = target_history.get("terminal_shards")
    hostile_shards = hostile_history.get("terminal_shards")
    if type(target_shards) is not list or type(hostile_shards) is not list \
            or len(target_shards) != 10 or len(hostile_shards) != 10:
        raise Refusal("A18 terminal shard census mismatch")
    for q, (target_shard, hostile_shard) in enumerate(zip(target_shards, hostile_shards)):
        target_path = Path(target_shard["path"])
        hostile_path = Path(hostile_shard["path"])
        projection = review.consumer._compare_terminal_target_npy_hostile_raw(
            target_path, target_shard, hostile_path, hostile_shard, 1.0e-8, q,
        )
        policy = template["comparison_policy"]["terminal_projection_by_q"][q]
        for key in (
            "lineage_target_to_hostile_permutation_sha256",
            "carrier_target_to_hostile_permutation_sha256",
        ):
            if projection[key] != policy[key]:
                raise Refusal(f"A18 basis permutation changed at q={q}")
        updates[f"/comparison_policy/terminal_projection_by_q/{q}/target_sha256"] = (
            target_shard["sha256"]
        )
        updates[f"/comparison_policy/terminal_projection_by_q/{q}/hostile_sha256"] = (
            hostile_shard["sha256"]
        )
        updates[f"/comparison_policy/terminal_projection_by_q/{q}/linf_abs_error"] = (
            projection["linf_abs_error"]
        )
    if set(updates) != set(A18_DYNAMIC_POINTERS):
        raise Refusal("measured A18 binding census mismatch")
    return updates


def _pointer_value(record: object, pointer: str) -> object:
    current = record
    for part in _decode_pointer(pointer):
        if type(current) is dict:
            current = current[part]
        elif type(current) is list and part.isdigit():
            current = current[int(part)]
        else:
            raise Refusal(f"A18 template pointer mismatch: {pointer}")
    return copy.deepcopy(current)


def publish_a18(root: Path, record: Mapping[str, object]) -> str:
    path = root.joinpath(*PurePosixPath(A18_CANONICAL_PATH).parts)
    if not path.parent.is_dir() or path.parent.is_symlink():
        raise Refusal("A18 canonical parent is absent or aliased")
    return retirement.publish_once(path, dict(record))


def _predicted_publication_sha(record: Mapping[str, object]) -> str:
    return retirement.sha256_bytes(retirement.publication_json_bytes(record))


def _canonical_publisher_runner(root: Path) -> Callable[[Sequence[str]], int]:
    entry_module_by_script = {
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/validate_preflight.py":
            "authenticated_validate_preflight",
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/build_target_cache.py":
            "build_target_cache",
        "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/independent_postbuild_auditor.py":
            "authenticated_independent_postbuild_auditor",
        "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py":
            "consume_target_cache",
    }

    def run(command: Sequence[str]) -> int:
        if (
            root != ROOT or len(command) < 3
            or tuple(command[:2]) != ("python3", "-B")
            or command[2] not in entry_module_by_script
        ):
            raise Refusal("publisher command lacks an authenticated entry")
        module_name = entry_module_by_script[command[2]]
        for dependency, (relative, expected) in PINNED_EXECUTABLE_DEPENDENCIES.items():
            try:
                _read_pinned_source_bytes(
                    root.joinpath(*PurePosixPath(relative).parts),
                    expected, dependency,
                )
            except RuntimeError as error:
                raise Refusal(str(error)) from error
        for dependency, (relative, expected) in PINNED_REPAIRED_CANONICAL_SOURCES.items():
            try:
                _read_pinned_source_bytes(
                    root.joinpath(*PurePosixPath(relative).parts),
                    expected, dependency, require_immutable=True,
                )
            except RuntimeError as error:
                raise Refusal(str(error)) from error
        sys.stdout.flush()
        sys.stderr.flush()
        try:
            child = os.fork()
        except OSError as error:
            raise Refusal("authenticated publisher fork failed") from error
        if child == 0:
            try:
                os.chdir(root)
                module = _load_authenticated_module(module_name)
                sys.argv = [command[2], *command[3:]]
                result = module.main()
                if type(result) is not int:
                    result = 2
                sys.stdout.flush()
                sys.stderr.flush()
            except BaseException as error:
                print(f"REFUSED: authenticated publisher failed: {error}", file=sys.stderr)
                sys.stderr.flush()
                result = 2
            os._exit(result)
        _pid, status = os.waitpid(child, 0)
        if not os.WIFEXITED(status):
            return 2
        return os.WEXITSTATUS(status)
    return run


def _ordinary_directory(
    path: Path, label: str, *, require_immutable: bool = False,
) -> None:
    try:
        metadata = os.stat(path, follow_symlinks=False)
    except OSError as error:
        raise Refusal(f"{label} is absent") from error
    if (
        not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode)
        or (require_immutable and metadata.st_mode & 0o222)
    ):
        raise Refusal(f"{label} is not an ordinary directory")


def _publisher_workspace(root: Path, action: PublisherAction) -> Path | None:
    if action.artifact_id not in {
        "A10_CONTROL_HISTORIES", "A14_L10_HISTORY",
    }:
        return None
    try:
        value = action.command[action.command.index("--workspace") + 1]
    except (ValueError, IndexError) as error:
        raise Refusal("history publisher lacks its fixed workspace") from error
    return root.joinpath(*PurePosixPath(value).parts)


def _reconcile_or_run_existing_publisher(
    root: Path,
    review: ExactLiveReview,
    action: PublisherAction,
    runner: Callable[[Sequence[str]], int],
) -> tuple[str, str | None, bool]:
    """Run an existing publisher, or authenticate its complete prior result.

    Incomplete publisher effects are never deleted, overwritten, or guessed.
    They are preserved and refused.  This permits restart after every completed
    owner-once boundary while making an interruption inside a non-resumable
    external publisher an explicit obstruction.
    """
    relative = PUBLISHED_PATH_BY_INSTANCE[(action.artifact_id, action.instance)]
    primary = root.joinpath(*PurePosixPath(relative).parts)
    ledger = root.joinpath(*PurePosixPath(MUTATION_LEDGER_PATH).parts)
    workspace = _publisher_workspace(root, action)
    primary_exists = retirement.path_exists(primary)
    ledger_exists = retirement.path_exists(ledger)

    if action.artifact_id == "A02_NONPHYSICAL_PREFLIGHT":
        if primary_exists != ledger_exists:
            raise Refusal("A02/A27 partial publication is preserved")
    elif action.artifact_id == "A05_FIVE_CACHE_SET":
        cache_root_exists = retirement.path_exists(primary.parent)
        if not primary_exists and cache_root_exists:
            raise Refusal(
                f"{action.artifact_id}/{action.instance} partial cache is preserved"
            )
    elif workspace is not None:
        workspace_exists = retirement.path_exists(workspace)
        if primary_exists != workspace_exists:
            raise Refusal(
                f"{action.artifact_id}/{action.instance} partial history is preserved"
            )

    reconciled = primary_exists
    if not primary_exists:
        run_existing_publisher(action, runner)

    record, digest, _raw = _stable_owner_once_json(
        primary, f"{action.artifact_id}/{action.instance} canonical publication",
    )
    ledger_record: Mapping[str, object] | None = None
    ledger_sha: str | None = None
    if action.artifact_id == "A02_NONPHYSICAL_PREFLIGHT":
        ledger_record, ledger_sha, _ledger_raw = _stable_owner_once_json(
            ledger, "A27 canonical mutation ledger",
        )
    if action.artifact_id == "A05_FIVE_CACHE_SET":
        _ordinary_directory(primary.parent, "completed cache root")
    if workspace is not None:
        _ordinary_directory(
            workspace, "completed history workspace", require_immutable=True,
        )
    review.validate_completed_publisher(
        action.artifact_id, record,
        mutation_ledger=ledger_record, mutation_ledger_sha=ledger_sha,
    )
    return digest, ledger_sha, reconciled


def coordinate_canonical_a01_a18_replay(
    expected_retirement_receipt_sha256: str,
) -> dict[tuple[str, int], str]:
    """Run the exact canonical repair replay after a certified retirement.

    This is the sole live entry point.  It accepts no hash, path, sink, runner,
    formula, threshold, or ordering injection.  The retirement receipt hash is
    an explicit custody gate; every other dynamic value is measured from the
    fixed predecessor DAG.
    """
    if not _sha256_text(expected_retirement_receipt_sha256):
        raise Refusal("exact retirement receipt SHA-256 is required")
    census = retirement.load_census()
    _custody, _receipt, observed_receipt_sha = _load_completed_retirement_receipt(
        ROOT, census,
    )
    if observed_receipt_sha != expected_retirement_receipt_sha256:
        raise Refusal("completed retirement receipt authorization mismatch")
    # The retirement transaction also removed the old launcher and builder.
    # Reconstruct and owner-once publish their complete repaired pair before
    # any live validator, builder, or publisher module can be loaded.
    reconcile_or_publish_repaired_sources(ROOT, census)
    review = ExactLiveReview(ROOT)
    runner = _canonical_publisher_runner(ROOT)
    produced: dict[tuple[str, int], str] = {}

    def template_candidate(artifact_id: str) -> dict[str, object]:
        template = load_retired_template(ROOT, census, artifact_id)
        updates = measured_template_updates(ROOT, artifact_id, produced)
        record = update_authenticated_template(artifact_id, template, updates)
        validate_with_sinks(
            artifact_id, record, review.common_sinks(), required_count=2,
        )
        return record

    def publish_template(artifact_id: str, record: Mapping[str, object]) -> str:
        relative = TEMPLATE_PATH_BY_ARTIFACT[artifact_id]
        path = ROOT.joinpath(*PurePosixPath(relative).parts)
        if not path.parent.is_dir() or path.parent.is_symlink():
            raise Refusal("canonical authority parent is absent or aliased")
        digest, _reconciled = _reconcile_or_publish_json(
            path, record, artifact_id, review.common_sinks(),
        )
        produced[(artifact_id, 1)] = digest
        return digest

    def run_publisher(artifact_id: str, instance: int) -> str:
        action = _publisher_action(artifact_id, instance, produced)
        digest, ledger_sha, _reconciled = _reconcile_or_run_existing_publisher(
            ROOT, review, action, runner,
        )
        produced[(artifact_id, instance)] = digest
        if artifact_id == "A02_NONPHYSICAL_PREFLIGHT":
            if not _sha256_text(ledger_sha):
                raise Refusal("A02 publisher did not authenticate A27")
            produced[("A27_MUTATION_LEDGER", 1)] = str(ledger_sha)
        return digest

    # A01--A04: source freeze, full preflight/mutation replay, independent
    # prepayload reconstruction, and five-length obstruction gate.
    a01 = template_candidate("A01_FREEZE_AND_SOURCE_PACKET")
    review.validate_freeze(a01)
    publish_template("A01_FREEZE_AND_SOURCE_PACKET", a01)
    run_publisher("A02_NONPHYSICAL_PREFLIGHT", 1)
    a03 = template_candidate("A03_PREPAYLOAD_AUDIT")
    review.validate_a03(
        a03, a01, produced[("A02_NONPHYSICAL_PREFLIGHT", 1)],
    )
    publish_template("A03_PREPAYLOAD_AUDIT", a03)
    a04 = template_candidate("A04_UNIVERSAL_CUSTODY_GATE")
    review.validate_a04(
        a04, a01, produced[("A02_NONPHYSICAL_PREFLIGHT", 1)],
    )
    publish_template("A04_UNIVERSAL_CUSTODY_GATE", a04)

    # A05--A06 use their existing exact publishers.
    for instance in range(1, 6):
        run_publisher("A05_FIVE_CACHE_SET", instance)
    run_publisher("A06_POSTBUILD_AUDIT", 1)
    cache_hashes = {
        str(length): produced[("A05_FIVE_CACHE_SET", instance)]
        for instance, length in enumerate((4, 6, 8, 10, 12), start=1)
    }

    # A07--A09 are constructed as one dependency-closed batch and all three
    # pass both record sinks plus the exact live control reconstruction before
    # any member is published.
    a07 = template_candidate("A07_BASE_PHYSICAL_GATE")
    predicted_a07 = _predicted_publication_sha(a07)
    produced[("A07_BASE_PHYSICAL_GATE", 1)] = predicted_a07
    a08 = template_candidate("A08_PHYSICAL_GATE_AUDIT")
    predicted_a08 = _predicted_publication_sha(a08)
    produced[("A08_PHYSICAL_GATE_AUDIT", 1)] = predicted_a08
    a09 = template_candidate("A09_CONTROL_AUTHORIZATION")
    review.validate_control_triple(a07, a08, a09, cache_hashes)
    publish_template("A07_BASE_PHYSICAL_GATE", a07)
    publish_template("A08_PHYSICAL_GATE_AUDIT", a08)
    publish_template("A09_CONTROL_AUTHORIZATION", a09)
    for length in (4, 6, 8):
        live = review.consumer.require_physical_gate(
            length, cache_hashes[str(length)],
        )
        if retirement.canonical_json_bytes(live["physical"]) \
                != retirement.canonical_json_bytes(a07):
            raise Refusal("A07-A09 canonical reconstruction changed staged bytes")

    # Existing exact history publishers reproduce L4/L6/L8.
    for instance in range(1, 4):
        run_publisher("A10_CONTROL_HISTORIES", instance)

    # Construct and prevalidate A11--A13 as one closed staged chain.
    a11 = template_candidate("A11_CONTROL_STAGE_GATE")
    produced[("A11_CONTROL_STAGE_GATE", 1)] = _predicted_publication_sha(a11)
    a12 = template_candidate("A12_CONTROL_STAGE_AUDIT")
    produced[("A12_CONTROL_STAGE_AUDIT", 1)] = _predicted_publication_sha(a12)
    a13 = template_candidate("A13_L10_AUTHORIZATION")
    review.validate_stage_chain(
        a11, a12, a13, cache_hashes,
        produced[("A07_BASE_PHYSICAL_GATE", 1)],
    )
    publish_template("A11_CONTROL_STAGE_GATE", a11)
    publish_template("A12_CONTROL_STAGE_AUDIT", a12)
    publish_template("A13_L10_AUTHORIZATION", a13)

    # Existing exact L10 history publisher, then staged A15/A16 reconstruction.
    run_publisher("A14_L10_HISTORY", 1)
    a15 = template_candidate("A15_L10_STAGE_GATE")
    produced[("A15_L10_STAGE_GATE", 1)] = _predicted_publication_sha(a15)
    a16 = template_candidate("A16_L10_STAGE_AUDIT")
    review.validate_l10_stage_pair(
        a15, a16, cache_hashes,
        produced[("A07_BASE_PHYSICAL_GATE", 1)],
        produced[("A11_CONTROL_STAGE_GATE", 1)],
        produced[("A13_L10_AUTHORIZATION", 1)],
    )
    publish_template("A15_L10_STAGE_GATE", a15)
    publish_template("A16_L10_STAGE_AUDIT", a16)

    # Restore, independently reconstruct, and hash the A17 composite branch.
    restore_completed_hostile_a17(ROOT, census)
    hostile_branch, hostile_metadata = construct_live_a17_branch(review)
    produced[("A17_HOSTILE_L12_ELIGIBILITY", 1)] = retirement.sha256_bytes(
        retirement.canonical_json_bytes(hostile_branch)
    )

    # A18 is measured from both actual histories and all terminal shards, then
    # passed through the repaired target validator, independent validator, and
    # the existing live 65-check comparison reconstruction before publication.
    a18_updates = measured_a18_updates(
        review, produced, hostile_branch, hostile_metadata,
    )
    a18 = construct_a18(
        a18_updates, review.production_sink, review.independent_sink,
    )
    review.validate_a18(a18, produced)
    a18_path = ROOT.joinpath(*PurePosixPath(A18_CANONICAL_PATH).parts)
    a18_sha, _reconciled = _reconcile_or_publish_json(
        a18_path, a18, "A18_L10_CROSS_GATE", review.common_sinks(),
    )
    review.validate_a18(a18, produced)
    produced[("A18_L10_CROSS_GATE", 1)] = a18_sha

    expected = {
        (artifact_id, instance)
        for _operation, artifact_id, instance in REPLAY_SEQUENCE
    } | {("A27_MUTATION_LEDGER", 1)}
    if set(produced) != expected:
        raise Refusal("canonical completed replay product census mismatch")
    return produced


def replay_plan() -> dict[str, object]:
    return {
        "classification": "BOUNDED_NONEXECUTED_A01_A18_REPLAY_PLAN",
        "retired_template_artifacts": list(TEMPLATE_PATH_BY_ARTIFACT),
        "existing_publisher_artifacts": [
            "A02_NONPHYSICAL_PREFLIGHT", "A05_FIVE_CACHE_SET",
            "A06_POSTBUILD_AUDIT", "A10_CONTROL_HISTORIES", "A14_L10_HISTORY",
        ],
        "hostile_restore_entries": list(HOSTILE_A17_RESTORE_PATHS),
        "a18_dynamic_binding_count": len(A18_DYNAMIC_POINTERS),
        "retired_template_dynamic_binding_count": sum(
            len(values) for values in DYNAMIC_POINTERS.values()
        ),
        "authenticated_executable_dependency_count": len(
            PINNED_EXECUTABLE_DEPENDENCIES
        ),
        "repaired_canonical_source_sha256": {
            relative: digest
            for relative, digest in PINNED_REPAIRED_CANONICAL_SOURCES.values()
        },
        "source_repair_policy": (
            "EXACT_NINE_ANCHOR_LAUNCHER_TRANSFORMATION__EXACT_ONE_OCCURRENCE_"
            "BUILDER_BINDING_SUBSTITUTION__OWNER_ONCE_COMPLETE_PAIR"
        ),
        "restart_policy": (
            "RECONCILE_EXACT_COMPLETED_OWNER_ONCE_OUTPUTS__RECOVER_AUTHENTICATED_"
            "A17_RESTORE__RECONCILE_COMPLETE_SOURCE_PAIR__PRESERVE_AND_REFUSE_"
            "PARTIAL_SOURCE_PAIR_OR_INCOMPLETE_EXTERNAL_PUBLISHERS"
        ),
        "canonical_action_executed": False,
        "claim_boundary": (
            "REPLAY_IMPLEMENTATION_PLAN_ONLY__NO_RETIREMENT_RESTORE_CACHE_"
            "HISTORY_A18_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true")
    action.add_argument("--execute-canonical", action="store_true")
    parser.add_argument("--retirement-receipt-sha256")
    parser.add_argument("--authorization")
    arguments = parser.parse_args()
    try:
        if arguments.plan:
            if arguments.retirement_receipt_sha256 is not None \
                    or arguments.authorization is not None:
                raise Refusal("plan mode rejects execution authorization fields")
            result: object = replay_plan()
        else:
            if arguments.authorization != "EXECUTE_EXACT_A01_A18_REPLAY_V001":
                raise Refusal("exact canonical replay authorization string is absent")
            if arguments.retirement_receipt_sha256 is None:
                raise Refusal("retirement receipt hash is absent")
            products = coordinate_canonical_a01_a18_replay(
                arguments.retirement_receipt_sha256,
            )
            result = {
                "classification": "PASS_EXACT_A01_A18_CANONICAL_REPLAY",
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
