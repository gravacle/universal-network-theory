#!/usr/bin/env python3
"""Minimum Stage-3 compatibility for two owner-once publication frames.

The frozen Stage-3 launcher requires compact canonical JSON for every JSON
input.  The completed Stage-2 owner-once transaction intentionally publishes
A18 with ``publication_json_bytes`` instead.  The target L12 cache manifest
uses the same authenticated framing.  This successor changes only those two
explicit ``StableInput.open`` boundaries while retaining the launcher's file
and parent descriptors, identity checks, immutable-file rules, and later
``verify`` calls.  Every other open is delegated unchanged.

This mutable candidate does not publish or launch when invoked in ``plan``
mode.  The production entry functions exist only for a later frozen and
independently authorized successor.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
import types
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterator


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
STAGE3_PACKET: Final[Path] = ROOT / "AUDIT_PREPARATION_R_L12_STAGE3_ENTRY_V001"
STAGE3_ADAPTER: Final[Path] = STAGE3_PACKET / "stage3_entry_adapter.py"
STAGE3_MODULE_NAME: Final[str] = (
    "authenticated_stage3_entry_adapter_stored_publication_v003"
)
SELF_FREEZE_NAME: Final[str] = "SOURCE_FREEZE.json"
SELF_SOURCE_NAME: Final[str] = "stage3_a18_framing_compatibility.py"
SELF_TEST_NAME: Final[str] = "test_stage3_a18_framing_compatibility.py"
SELF_README_NAME: Final[str] = "README.md"
SELF_MEMBER_NAMES: Final[frozenset[str]] = frozenset({
    SELF_SOURCE_NAME, SELF_TEST_NAME, SELF_README_NAME,
})
SELF_FREEZE_SCHEMA: Final[str] = (
    "V012_STAGE3_STORED_PUBLICATION_FRAMING_COMPATIBILITY_SOURCE_FREEZE_V003"
)
SELF_FREEZE_STATUS: Final[str] = (
    "FROZEN_BEFORE_STAGE3_DRY_RUN_PUBLICATION_OR_LAUNCH"
)
SELF_CLAIM_BOUNDARY: Final[str] = (
    "FROZEN_CONTROL_PLANE_COMPATIBILITY_SOURCE_ONLY__NO_A20_A22_"
    "PUBLICATION_L12_EXECUTION_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
)

PINNED_STAGE3_PACKET: Final[dict[str, str]] = {
    "README.md":
        "1c3b520d35732fb73bc947e0963696858f1e07c19e6609f1f84f03bc9c167254",
    "SOURCE_FREEZE.json":
        "dbec9f7918ca3fcce1fc77743339e55c458fe9d9de1d2ff92ae691a62e5c72a7",
    "independent_a20_auditor.py":
        "9074ef86d28457f93db9976615639a5a6915dbcae8c6db505aa61d2bc82f7b25",
    "production_dual_l12_launcher_candidate.py":
        "067bdec60d4fe40e5d961241a7408677f8950ea7d68e7dbb3d8dc0f9db83f163",
    "stage3_entry_adapter.py":
        "6cac68dc300d42e27933581a3baa16e677da9420b5e54d25ad592a4b03e9e53e",
    "test_stage3_entry_adapter.py":
        "af60092dcfe95c9e1026024cf04ab1b843b093685136e7a4f6ff024cc466ac65",
}

EXPECTED_A18_SHA256: Final[str] = (
    "defab8ecda42112db25fec75bdd146a7e593d5883a885660c769571a388e93a0"
)
EXPECTED_TARGET_MANIFEST_SHA256: Final[str] = (
    "859e01f5a735eeb10f93960068c1fd048ec6ab085a7f5a1df29f9176f9be1e76"
)
ADAPTER_A18_LABEL: Final[str] = "A18 L10 cross gate"
LAUNCHER_A18_LABEL: Final[str] = "L10 cross gate"
ADAPTER_TARGET_MANIFEST_LABEL: Final[str] = "target L12 cache manifest"
LAUNCHER_TARGET_MANIFEST_LABEL: Final[str] = "target cache manifest"

EXPECTED_PRETTY_INPUT_REGISTRY: Final[list[dict[str, object]]] = [
    {
        "name": "A18 L10 cross gate",
        "relative_path": (
            "AUDIT_R_L12_PARALLEL_EXECUTION_V001/"
            "TARGET_HOSTILE_L10_CROSS_GATE_V001.json"
        ),
        "sha256": EXPECTED_A18_SHA256,
        "labels": [ADAPTER_A18_LABEL, LAUNCHER_A18_LABEL],
        "schema": "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001",
        "identity_field": "L",
        "identity_value": 10,
    },
    {
        "name": "target L12 cache manifest",
        "relative_path": (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
            "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json"
        ),
        "sha256": EXPECTED_TARGET_MANIFEST_SHA256,
        "labels": [
            ADAPTER_TARGET_MANIFEST_LABEL, LAUNCHER_TARGET_MANIFEST_LABEL,
        ],
        "schema": "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
        "identity_field": "status",
        "identity_value": "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE",
    },
]


class FramingRefusal(RuntimeError):
    """The exact stored-publication framing successor refused closed."""


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
        value.st_ctime_ns, value.st_mode, value.st_nlink,
    )


def _parent_identity(value: os.stat_result) -> tuple[int, int, int]:
    return value.st_dev, value.st_ino, stat.S_IFMT(value.st_mode)


@dataclass
class _RetainedSelfMember:
    path: Path
    descriptor: int
    parent_descriptor: int
    identity: tuple[int, ...]
    parent_identity: tuple[int, int, int]
    raw: bytes
    sha256: str

    @classmethod
    def open(
        cls, path: Path, expected_sha256: str | None, label: str,
    ) -> "_RetainedSelfMember":
        if (
            not path.is_absolute() or ROOT not in path.parents
            or Path(str(path)) != path or "\x00" in str(path)
        ):
            raise FramingRefusal(f"{label} is outside the canonical repository")
        cursor = ROOT
        for component in path.relative_to(ROOT).parts[:-1]:
            cursor /= component
            try:
                parent_component = os.lstat(cursor)
            except OSError as error:
                raise FramingRefusal(f"{label} parent is absent") from error
            if (
                stat.S_ISLNK(parent_component.st_mode)
                or not stat.S_ISDIR(parent_component.st_mode)
            ):
                raise FramingRefusal(f"{label} parent is aliased or special")
        parent_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        file_flags = (
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        parent_descriptor = -1
        descriptor = -1
        try:
            parent_descriptor = os.open(path.parent, parent_flags)
            parent_opened = os.fstat(parent_descriptor)
            parent_named = os.stat(path.parent, follow_symlinks=False)
            if (
                not stat.S_ISDIR(parent_opened.st_mode)
                or _parent_identity(parent_opened) != _parent_identity(parent_named)
            ):
                raise FramingRefusal(f"{label} parent identity mismatch")
            descriptor = os.open(path.name, file_flags, dir_fd=parent_descriptor)
            before = os.fstat(descriptor)
            named = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
        except BaseException as error:
            if descriptor >= 0:
                os.close(descriptor)
            if parent_descriptor >= 0:
                os.close(parent_descriptor)
            if isinstance(error, OSError):
                raise FramingRefusal(f"{label} cannot be opened") from error
            raise
        try:
            identity = _identity(before)
            if (
                not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(named.st_mode)
                or before.st_mode & 0o222 or before.st_nlink != 1
                or identity != _identity(named)
            ):
                raise FramingRefusal(f"{label} is writable, linked, or special")
            raw = bytearray()
            offset = 0
            while offset < before.st_size:
                block = os.pread(
                    descriptor, min(16 * 2**20, before.st_size - offset), offset,
                )
                if not block:
                    raise FramingRefusal(f"{label} retained read was short")
                raw.extend(block)
                offset += len(block)
            digest = hashlib.sha256(raw).hexdigest()
            result = cls(
                path, descriptor, parent_descriptor, identity,
                _parent_identity(parent_opened), bytes(raw), digest,
            )
            if expected_sha256 is not None and digest != expected_sha256:
                raise FramingRefusal(f"{label} digest mismatch")
            result.verify()
            return result
        except BaseException:
            os.close(descriptor)
            os.close(parent_descriptor)
            raise

    def verify(self) -> None:
        opened = os.fstat(self.descriptor)
        named = os.stat(
            self.path.name, dir_fd=self.parent_descriptor,
            follow_symlinks=False,
        )
        parent_opened = os.fstat(self.parent_descriptor)
        parent_named = os.stat(self.path.parent, follow_symlinks=False)
        if (
            _identity(opened) != self.identity
            or _identity(named) != self.identity
            or _parent_identity(parent_opened) != self.parent_identity
            or _parent_identity(parent_named) != self.parent_identity
            or hashlib.sha256(self.raw).hexdigest() != self.sha256
        ):
            raise FramingRefusal(f"retained self-freeze member changed: {self.path}")

    def close(self) -> None:
        if self.descriptor >= 0:
            os.close(self.descriptor)
            self.descriptor = -1
        if self.parent_descriptor >= 0:
            os.close(self.parent_descriptor)
            self.parent_descriptor = -1


def _strict_self_freeze(raw: bytes) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise FramingRefusal("duplicate self-freeze JSON key")
            result[key] = value
        return result

    def constant(_value: str) -> object:
        raise FramingRefusal("nonfinite self-freeze JSON constant")

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=constant,
        )
    except FramingRefusal:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise FramingRefusal("self-freeze is not strict ASCII JSON") from error
    if type(value) is not dict or _compact_json_bytes(value) != raw:
        raise FramingRefusal("self-freeze is not one compact canonical object")
    return value


def _compact_json_bytes(value: object) -> bytes:
    try:
        return (json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
            allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise FramingRefusal("self-freeze value is not canonical") from error


def _authenticate_self_packet_at(packet: Path) -> dict[str, object]:
    freeze = _RetainedSelfMember.open(
        packet / SELF_FREEZE_NAME, None, "stored-publication source freeze",
    )
    members: list[_RetainedSelfMember] = []
    try:
        record = _strict_self_freeze(freeze.raw)
        if set(record) != {
            "schema", "status", "files", "frozen_stage3_packet",
            "pretty_input_registry", "claim_boundary",
        }:
            raise FramingRefusal("self-freeze top-level census mismatch")
        files = record.get("files")
        if type(files) is not dict or set(files) != set(SELF_MEMBER_NAMES):
            raise FramingRefusal("self-freeze member census mismatch")
        if (
            record.get("schema") != SELF_FREEZE_SCHEMA
            or record.get("status") != SELF_FREEZE_STATUS
            or record.get("frozen_stage3_packet") != PINNED_STAGE3_PACKET
            or record.get("pretty_input_registry")
            != EXPECTED_PRETTY_INPUT_REGISTRY
            or record.get("claim_boundary") != SELF_CLAIM_BOUNDARY
        ):
            raise FramingRefusal("self-freeze contract mismatch")
        for name in sorted(SELF_MEMBER_NAMES):
            digest = files[name]
            if (
                type(digest) is not str or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
            ):
                raise FramingRefusal("self-freeze member digest is malformed")
            members.append(_RetainedSelfMember.open(
                packet / name, digest, f"stored-publication source {name}",
            ))
        freeze.verify()
        for member in members:
            member.verify()
        return record
    finally:
        for member in members:
            member.close()
        freeze.close()


def _read_pinned_stage3_member(name: str) -> bytes:
    if name not in PINNED_STAGE3_PACKET:
        raise FramingRefusal("unregistered frozen Stage3 packet member")
    path = STAGE3_PACKET / name
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
            or before.st_mode & 0o222 or before.st_nlink != 1
            or _identity(before) != _identity(named)
        ):
            raise FramingRefusal(f"frozen Stage3 custody mismatch: {name}")
        raw = bytearray()
        offset = 0
        while offset < before.st_size:
            block = os.pread(
                descriptor, min(16 * 2**20, before.st_size - offset), offset,
            )
            if not block:
                raise FramingRefusal(f"short frozen Stage3 read: {name}")
            raw.extend(block)
            offset += len(block)
        after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
        digest = hashlib.sha256(raw).hexdigest()
        if (
            _identity(after) != _identity(before)
            or _identity(named_after) != _identity(before)
            or digest != PINNED_STAGE3_PACKET[name]
        ):
            raise FramingRefusal(f"frozen Stage3 digest mismatch: {name}")
        return bytes(raw)
    finally:
        os.close(descriptor)


def _load_stage3() -> types.ModuleType:
    for name in PINNED_STAGE3_PACKET:
        _read_pinned_stage3_member(name)
    retained = _RetainedSelfMember.open(
        STAGE3_ADAPTER, PINNED_STAGE3_PACKET[STAGE3_ADAPTER.name],
        "retained frozen Stage3 adapter",
    )
    previous = sys.modules.get(STAGE3_MODULE_NAME)
    module = types.ModuleType(STAGE3_MODULE_NAME)
    module.__file__ = str(STAGE3_ADAPTER)
    module.__package__ = ""
    module.__cached__ = None
    module.__authenticated_sha256__ = PINNED_STAGE3_PACKET[STAGE3_ADAPTER.name]
    sys.modules[STAGE3_MODULE_NAME] = module
    completed = False
    try:
        exec(
            compile(
                retained.raw, str(STAGE3_ADAPTER), "exec", dont_inherit=True,
            ),
            module.__dict__,
        )
        # This authenticates and retains the complete frozen dependency closure
        # before executing any dependency source.
        runtime = module.frozen_runtime()
        retained.verify()
        for name in PINNED_STAGE3_PACKET:
            _read_pinned_stage3_member(name)
        if (
            sys.modules.get(STAGE3_MODULE_NAME) is not module
            or module.__file__ != str(STAGE3_ADAPTER)
            or module.__authenticated_sha256__
            != PINNED_STAGE3_PACKET[STAGE3_ADAPTER.name]
            or getattr(module, "_RUNTIME", None) is not runtime
            or module.frozen_runtime() is not runtime
        ):
            raise FramingRefusal("fresh Stage3 post-load identity mismatch")
        completed = True
        return module
    finally:
        retained.close()
        if not completed:
            if previous is None:
                sys.modules.pop(STAGE3_MODULE_NAME, None)
            else:
                sys.modules[STAGE3_MODULE_NAME] = previous


SELF_FREEZE_RECORD: Final[dict[str, object]] = _authenticate_self_packet_at(HERE)
stage3 = _load_stage3()


@dataclass(frozen=True)
class _PrettyInputContract:
    name: str
    path: Path
    sha256: str
    labels: frozenset[str]
    schema: str
    identity_field: str
    identity_value: object


PRODUCTION_A18_CONTRACT: Final[_PrettyInputContract] = _PrettyInputContract(
    "A18 L10 cross gate",
    stage3.L10_CROSS_GATE,
    EXPECTED_A18_SHA256,
    frozenset({ADAPTER_A18_LABEL, LAUNCHER_A18_LABEL}),
    "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001",
    "L",
    10,
)
PRODUCTION_TARGET_MANIFEST_CONTRACT: Final[_PrettyInputContract] = (
    _PrettyInputContract(
        "target L12 cache manifest",
        stage3.TARGET_CACHE_MANIFEST,
        EXPECTED_TARGET_MANIFEST_SHA256,
        frozenset({
            ADAPTER_TARGET_MANIFEST_LABEL, LAUNCHER_TARGET_MANIFEST_LABEL,
        }),
        "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
        "status",
        "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE",
    )
)
PRODUCTION_PRETTY_INPUTS: Final[tuple[_PrettyInputContract, ...]] = (
    PRODUCTION_A18_CONTRACT, PRODUCTION_TARGET_MANIFEST_CONTRACT,
)
FROZEN_STABLE_OPEN_DESCRIPTOR: Final[object] = (
    stage3.frozen_runtime().launcher.StableInput.__dict__["open"]
)


def _publication_json_bytes(value: object) -> bytes:
    """Exact Stage-2 ``publication_json_bytes`` serialization contract."""
    try:
        return (json.dumps(
            value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False,
        ) + "\n").encode("ascii")
    except (TypeError, ValueError, OverflowError) as error:
        raise FramingRefusal("input cannot be serialized as a publication record") from error


def _parse_exact_publication(
    raw: bytes, runtime, contract: _PrettyInputContract,
) -> dict[str, object]:
    if type(raw) is not bytes:
        raise FramingRefusal(f"{contract.name} raw publication must be exact bytes")
    try:
        text = raw.decode("ascii")
        value = runtime.coordinator.parse_strict_json(text)
    except (UnicodeDecodeError, runtime.coordinator.Refusal) as error:
        raise FramingRefusal(f"{contract.name} is not strict ASCII JSON") from error
    if type(value) is not dict:
        raise FramingRefusal(f"{contract.name} must contain one object")
    is_a18 = contract.schema == "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001"
    expected_raw = _compact_json_bytes(value) if is_a18 else _publication_json_bytes(value)
    if expected_raw != raw:
        raise FramingRefusal(
            f"{contract.name} does not use its exact registered framing"
        )
    if (
        value.get("schema") != contract.schema
        or value.get(contract.identity_field) != contract.identity_value
    ):
        raise FramingRefusal(f"{contract.name} identity semantics refused")
    if contract is PRODUCTION_A18_CONTRACT:
        try:
            runtime.validators.validate_record(
                "A18_L10_CROSS_GATE", value,
                mutation_class="PRODUCTION_NATIVE_RECORD", fixture_mode=False,
            )
        except BaseException as error:
            raise FramingRefusal("A18 production semantics refused") from error
    return value


def _read_retained(item) -> bytes:
    item.verify()
    size = int(item.identity[2])
    raw = bytearray()
    offset = 0
    while offset < size:
        block = os.pread(
            item.descriptor, min(16 * 2**20, size - offset), offset,
        )
        if not block:
            raise FramingRefusal("pretty input retained read was short")
        raw.extend(block)
        offset += len(block)
    result = bytes(raw)
    if hashlib.sha256(result).hexdigest() != item.digest:
        raise FramingRefusal("pretty input retained read/hash mismatch")
    item.verify()
    return result


def _matches_contract(
    label: object, path: object, json_record: object,
    contract: _PrettyInputContract,
) -> bool:
    return (
        type(label) is str and label in contract.labels
        and isinstance(path, Path) and path == contract.path
        and str(path) == str(contract.path)
        and json_record is True
    )


@dataclass
class _PatchCapability:
    active: bool = True
    in_call: bool = False


def _open_from_registry(
    original_open, runtime, capability: _PatchCapability,
    contracts: tuple[_PrettyInputContract, ...],
    label: str, path: Path, *, json_record: bool,
):
    """Internal algorithm; the production context supplies only frozen contracts."""
    if not capability.active:
        raise FramingRefusal("stored-publication open capability is inactive")
    if capability.in_call:
        raise FramingRefusal("reentrant stored-publication open refused")
    capability.in_call = True
    try:
        matching = tuple(
            item for item in contracts
            if _matches_contract(label, path, json_record, item)
        )
        if not matching:
            return original_open(label, path, json_record=json_record)
        if len(matching) != 1:
            raise FramingRefusal("pretty-input call matched an ambiguous registry")
        contract = matching[0]
        retained = original_open(label, path, json_record=False)
        try:
            retained.verify()
            if retained.digest != contract.sha256:
                raise FramingRefusal(
                    f"{contract.name} exact publication hash mismatch"
                )
            raw = _read_retained(retained)
            retained.record = _parse_exact_publication(raw, runtime, contract)
            retained.verify()
            return retained
        except BaseException:
            retained.close()
            raise
    finally:
        capability.in_call = False


@contextmanager
def _patched_pretty_inputs_open() -> Iterator[None]:
    """Temporarily patch only the registered ``StableInput.open`` calls."""
    contracts = PRODUCTION_PRETTY_INPUTS
    if not contracts or len({(item.path, item.sha256) for item in contracts}) != len(contracts):
        raise FramingRefusal("pretty-input registry is empty or ambiguous")
    runtime = stage3.frozen_runtime()
    stable = runtime.launcher.StableInput
    original_descriptor = stable.__dict__.get("open")
    if original_descriptor is not FROZEN_STABLE_OPEN_DESCRIPTOR:
        raise FramingRefusal("frozen StableInput.open is occupied or nested")
    original_open = stable.open
    capability = _PatchCapability()

    def compatible_open(cls, label: str, path: Path, *, json_record: bool):
        return _open_from_registry(
            original_open, runtime, capability, contracts,
            label, path, json_record=json_record,
        )

    installed_descriptor = classmethod(compatible_open)
    setattr(stable, "open", installed_descriptor)
    primary: BaseException | None = None
    try:
        yield
    except BaseException as error:
        primary = error
        raise
    finally:
        capability.active = False
        altered = stable.__dict__.get("open") is not installed_descriptor
        setattr(stable, "open", original_descriptor)
        if altered and primary is None:
            raise FramingRefusal("StableInput.open changed during compatibility scope")


def prepare_production(*, publish: bool) -> dict[str, object]:
    with _patched_pretty_inputs_open():
        return stage3.prepare_production(publish=publish)


def launch_authenticated_l12() -> dict[str, object]:
    with _patched_pretty_inputs_open():
        return stage3.launch_authenticated_l12()


def plan() -> dict[str, object]:
    """Authenticate both registered pretty inputs without mutation."""
    runtime = stage3.frozen_runtime()
    before = stable_descriptor = runtime.launcher.StableInput.__dict__["open"]
    digests: dict[str, str] = {}
    with _patched_pretty_inputs_open():
        for contract, label in (
            (PRODUCTION_A18_CONTRACT, ADAPTER_A18_LABEL),
            (PRODUCTION_TARGET_MANIFEST_CONTRACT, ADAPTER_TARGET_MANIFEST_LABEL),
        ):
            item = runtime.launcher.StableInput.open(
                label, contract.path, json_record=True,
            )
            try:
                item.verify()
                if not isinstance(item.record, dict):
                    raise FramingRefusal(f"{contract.name} record is absent")
                digests[contract.name] = item.digest
            finally:
                item.close()
    if runtime.launcher.StableInput.__dict__["open"] is not before:
        raise FramingRefusal("StableInput.open was not restored after plan")
    return {
        "schema": "V012_STAGE3_STORED_PUBLICATION_FRAMING_COMPATIBILITY_PLAN_V003",
        "classification": (
            "PASS_MUTABLE_PLAN_ONLY_EXACT_STORED_PUBLICATION_FRAME_COMPATIBILITY"
        ),
        "a18_path": str(PRODUCTION_A18_CONTRACT.path),
        "sha256_by_pretty_input": digests,
        "accepted_frame": "EXACT_STAGE2_PUBLICATION_JSON_BYTES",
        "stable_input_open_restored": stable_descriptor is before,
        "published": False,
        "launched": False,
        "next_required_gate": (
            "FREEZE_AND_TWO_INDEPENDENT_SAME_HASH_HOSTILE_REVIEWS_BEFORE_"
            "STAGE3_DRY_RUN_PUBLICATION_OR_LAUNCH"
        ),
        "claim_boundary": (
            "MUTABLE_CONTROL_PLANE_COMPATIBILITY_ONLY__NO_A20_A22_"
            "PUBLICATION_L12_EXECUTION_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        ),
    }


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {
        "plan", "dry-run", "publish", "launch",
    }:
        print(
            "REFUSED: exact mode is plan, dry-run, publish, or launch",
            file=sys.stderr,
        )
        return 2
    try:
        if sys.argv[1] == "plan":
            result = plan()
        elif sys.argv[1] in {"dry-run", "publish"}:
            result = prepare_production(publish=sys.argv[1] == "publish")
        else:
            result = launch_authenticated_l12()
    except BaseException as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
