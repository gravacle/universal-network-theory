#!/usr/bin/env python3
"""Fixed-scope repair/replay after the second pre-ACK L12 launch refusal.

This transaction promotes the audited one-helper hostile consumer successor,
retires exactly fourteen stale descendants, rebuilds only the hostile caches
and L10 control, reconstructs A18, and stops before any L12 launch action.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import os
import stat
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath
from typing import Final, Mapping


HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent
BASE_PATH: Final[Path] = (
    ROOT / "DEVELOPMENT_R_L12_STAGE3_DATA_LINEAGE_REPLAY_V001"
    / "stage3_data_lineage_replay.py"
)
BASE_SHA256: Final[str] = "68634cf16f2efa171018854e8e7041baa477dbaf6eb1a2584e807b8db8f7e268"
HOSTILE: Final[Path] = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001"
SHARED: Final[Path] = ROOT / "AUDIT_R_L12_PARALLEL_EXECUTION_V001"
TARGET: Final[Path] = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
AUDIT_ROOT: Final[Path] = ROOT / "AUDIT_R_L12_STAGE3_SECOND_LAUNCH_RECOVERY_V001"
CUSTODY: Final[Path] = AUDIT_ROOT / "RETIRED_SECOND_FAILED_LAUNCH_V001"
EVENTS: Final[Path] = CUSTODY / "RETIREMENT_EVENTS_V001"
INTENT: Final[Path] = CUSTODY / "RETIREMENT_INTENT_V001.json"
RECEIPT: Final[Path] = CUSTODY / "RETIREMENT_RECEIPT_V001.json"
RESULT: Final[Path] = AUDIT_ROOT / "SECOND_LAUNCH_RECOVERY_RESULT_V001.json"
LIVE_AUTHORIZATION: Final[str] = (
    "EXECUTE_EXACT_STAGE3_SECOND_LAUNCH_RECOVERY_V001__NO_L12_LAUNCH"
)

CONSUMER: Final[Path] = HOSTILE / "consume_cache_v004r4.py"
FREEZE: Final[Path] = HOSTILE / "FROZEN_MANIFEST_V004R4.json"
PREFLIGHT_RESULT: Final[Path] = HOSTILE / "V004R4_CACHE_PREFLIGHT_RESULT.json"
PREPAYLOAD: Final[Path] = HOSTILE / "HOSTILE_AUDIT_RESULT_V004R4.json"
BUILD_GATE: Final[Path] = HOSTILE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json"
CACHE_ROOT: Final[Path] = HOSTILE / "V004R4_CACHE_PAYLOADS"
POSTBUILD: Final[Path] = HOSTILE / "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json"
L10_AUTH: Final[Path] = HOSTILE / "L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json"
L10_GATE: Final[Path] = HOSTILE / "CACHED_L10_GATE_V004R4.json"
WORKSPACES: Final[Path] = HOSTILE / "V004R4_WORKSPACES"
OUTPUTS: Final[Path] = HOSTILE / "V004R4_PHYSICAL_OUTPUTS"
TARGET_A22: Final[Path] = TARGET / "TARGET_L12_EXECUTION_GATE_V012.json"
HOSTILE_A22: Final[Path] = HOSTILE / "HOSTILE_L12_EXECUTION_GATE_V004R4.json"

OLD_CONSUMER_SHA256: Final[str] = "700dce18ec8f50008a9e3022394a55c8d689268e21b80982896d37b92add7b74"
NEW_CONSUMER_SHA256: Final[str] = "0242ae1b318f47a89fbfe84bcf83e92b57fe67ea4f6230a0b5538ab64db5fd3b"
HELPER_BYTES: Final[bytes] = (
    b"def positive_integer(value: object) -> bool:\n"
    b"    return type(value) is int and value > 0\n\n\n"
)
INSERTION: Final[bytes] = b"def _lower_sha256(value: object, label: str) -> str:\n"

STALE: Final[dict[str, tuple[str, str]]] = {
    str(CONSUMER.relative_to(ROOT)): ("file", OLD_CONSUMER_SHA256),
    str(FREEZE.relative_to(ROOT)): ("file", "6c0d2efa83584a91df52f299d679e5baab8913cccc6955ddfc2dbeb43a87814a"),
    str(PREFLIGHT_RESULT.relative_to(ROOT)): ("file", "a0723a0caf9c826601984b99484227cb5da613608c8887edeeea234e54649f50"),
    str(PREPAYLOAD.relative_to(ROOT)): ("file", "7b4f677615d4688b3911e5350ce99bbd85e922786866648ac414866e1e3ddc32"),
    str(BUILD_GATE.relative_to(ROOT)): ("file", "ea291fd8e39804a780ec4eed6094e7311ff3b3c29aaf89572ef096128f4807b6"),
    str(CACHE_ROOT.relative_to(ROOT)): ("directory", "ccc229eff0a145357c888d6564ae79ed84cd3cd8b8bfc441e1cef29d16acd62c"),
    str(POSTBUILD.relative_to(ROOT)): ("file", "4c5e651b4b168c0f4a65d1502587629b5931658ff759669771390af612c71b22"),
    str(L10_AUTH.relative_to(ROOT)): ("file", "2959300977013221447dc505325e49b51caa11c9da33180eb2a84bee2bd39723"),
    str(L10_GATE.relative_to(ROOT)): ("file", "fc238bbb6e3fd290ad91fb8fbb97004577a178938cf226bc08f7ec0ae465d195"),
    str(WORKSPACES.relative_to(ROOT)): ("directory", "4d6cfdf839e1f72576eecbf13b3151555e3e9100cf8193e1d06870555c101fb3"),
    str(OUTPUTS.relative_to(ROOT)): ("directory", "8e468470d773307be26667a12e93cc8dd20dbbe780847fe0f93dea76484b94c3"),
    str(SHARED.relative_to(ROOT)): ("directory", "16b576250a0f8308f5cbdc5d232193ee45fb608e1fe5a846dc8b1ea3afde5bc2"),
    str(TARGET_A22.relative_to(ROOT)): ("file", "236159caaa0f627005d19c7d96b3d43b2f5b9e8295322701805ea7d6f1d18a90"),
    str(HOSTILE_A22.relative_to(ROOT)): ("file", "5a598118f2a15312063139dddf30dc29c1c6c89010cad07083ad7417a5594493"),
}

ABSENT: Final[tuple[Path, ...]] = (
    SHARED / "TARGET_V012_WORKER_RELEASE_ACK_V001.json",
    SHARED / "HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json",
    SHARED / "TARGET_V012_WORKER_COMPLETION_V001.json",
    SHARED / "HOSTILE_V004R4_WORKER_COMPLETION_V001.json",
    SHARED / "SHARED_AGGREGATE_TELEMETRY_V001.json",
    TARGET / "WORKSPACES/L12",
    HOSTILE / "V004R4_WORKSPACES/L12",
    TARGET / "PHYSICAL_OUTPUTS/HISTORY_L12.json",
    HOSTILE / "V004R4_PHYSICAL_OUTPUTS/HISTORY_L12.json",
)

PRESERVED: Final[dict[Path, str]] = {
    ROOT / "AUDIT_R_L12_STAGE3_DATA_LINEAGE_REPLAY_V001/DATA_LINEAGE_REPLAY_RESULT_V001.json":
        "943c63bac62261891ac8751cd131f764258c704fc54858c11c76277f65fc084d",
    ROOT / "AUDIT_R_L12_STAGE3_STORED_PUBLICATION_FRAMING_COMPATIBILITY_V003/stage3_a18_framing_compatibility.py":
        "a7feee0c0bcd525737f2db6980f1916b53e764fad06f4ec062d723a00fbb9bf5",
    ROOT / "AUDIT_R_L12_STAGE3_STORED_PUBLICATION_FRAMING_COMPATIBILITY_V003/test_stage3_a18_framing_compatibility.py":
        "e97fec87d68d223bae2a4c932a39cd01d0c8b8795f7b08cbb6fab0c5a6dc2ece",
    ROOT / "AUDIT_R_L12_STAGE3_STORED_PUBLICATION_FRAMING_COMPATIBILITY_V003/SOURCE_FREEZE.json":
        "2b8b582396f0763b17697344a8995638e8b2f74b82074f1ee22eb764b1c442d2",
    ROOT / "AUDIT_R_L12_STAGE3_STORED_PUBLICATION_FRAMING_COMPATIBILITY_V003/README.md":
        "8949dec6527387d7690599a47518791221dd30d472cf56d30437e92029e09d88",
    ROOT / "AUDIT_R_L12_STAGE3_STORED_PUBLICATION_FRAMING_COMPATIBILITY_V003/AUDIT_RESULT_V003.json":
        "3c4e83c2f493e6974c5949281675bab73e20ffd21862ff8668dbc5b131108ba3",
}

EXPECTED: Final[dict[str, object]] = {
    "freeze": "9e0fe9ea428476d22a74a83f50e53005eea398df8b03a18a5397e3bc2e9f1633",
    "preflight": "e83cbb5665ce3103dd3714ecaf41faeb4b26b40bc560a8d5be465b86afc38c2c",
    "prepayload": "057227a22c5e2b6194d44601104212e0326c24742574796745f452296b94255f",
    "build_gate": "12d3bf2561d4920e97bde1f54b3e75c659d4f8255bd6c7e285425ba3299b7849",
    "manifests": {
        4: "e29d5b99c51b4719e241d6b30819529d6fc459f322ed8bcd1aa1bc46999e550f",
        6: "e7745d3a1bcb31d863f7df38d917da47833a04d19ed4b275e484b35198418928",
        8: "4ea854042b042473285a0de65de08d078d3490f55134ecdd198ad95fe0d09969",
        10: "b6c1685a5b4cbd6f1c0d9b997763103bbba8f35a43c833dd736a5f4b38ffec28",
        12: "442103a16198f3b0354d1c76b4d7a5696606e749f9bd215dd01e930d230acbe0",
    },
    "postbuild": "c4f15f67c761eaf47e20d2553ebe71385484268fdefcda66b049910f5706fd11",
    "l10_authorization": "75380477c33aef263dba85decf831c4cc6e54b870331cfbb873670127a3a4053",
}


class Refusal(RuntimeError):
    pass


def _load_base():
    if hashlib.sha256(BASE_PATH.read_bytes()).hexdigest() != BASE_SHA256:
        raise Refusal("frozen predecessor replay source mismatch")
    spec = importlib.util.spec_from_file_location("stage3_replay_v001_pinned", BASE_PATH)
    if spec is None or spec.loader is None:
        raise Refusal("cannot load frozen predecessor replay")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = _load_base()


def read_json(path: Path) -> dict[str, object]:
    return base.strict_json(path.read_bytes(), str(path))


def digest_record(record: Mapping[str, object]) -> str:
    return base.sha256_bytes(base.canonical_json_bytes(dict(record)))


def _matches_predecessor(path: Path, logical: str) -> bool:
    if not os.path.lexists(path):
        return False
    kind, expected = STALE[logical]
    try:
        row = (base._file_census(path, logical) if kind == "file"
               else base._directory_census(path, logical))
    except (OSError, RuntimeError):
        return False
    observed = row["sha256"] if kind == "file" else row["inventory_sha256"]
    return observed == expected


def predecessor_path(logical: str) -> Path:
    active = ROOT.joinpath(*PurePosixPath(logical).parts)
    retired = CUSTODY.joinpath(*PurePosixPath(logical).parts)
    if os.path.lexists(RECEIPT):
        if not _matches_predecessor(retired, logical):
            raise Refusal(f"receipt exists without exact predecessor custody: {logical}")
        return retired
    matches = [path for path in (active, retired) if _matches_predecessor(path, logical)]
    if len(matches) != 1:
        raise Refusal(f"predecessor custody is not owner-once: {logical}")
    return matches[0]


def census() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for logical, (kind, expected) in STALE.items():
        path = predecessor_path(logical)
        row = (base._file_census(path, logical) if kind == "file"
               else base._directory_census(path, logical))
        observed = row["sha256"] if kind == "file" else row["inventory_sha256"]
        if observed != expected:
            raise Refusal(f"predecessor census mismatch: {logical}")
        rows.append(row)
    return rows


def successor_bytes() -> bytes:
    old = predecessor_path(str(CONSUMER.relative_to(ROOT))).read_bytes()
    if hashlib.sha256(old).hexdigest() != OLD_CONSUMER_SHA256:
        raise Refusal("predecessor consumer mismatch")
    if old.count(INSERTION) != 1 or b"def positive_integer(" in old:
        raise Refusal("successor insertion site mismatch")
    new = old.replace(INSERTION, HELPER_BYTES + INSERTION)
    if len(new) != 120286 or hashlib.sha256(new).hexdigest() != NEW_CONSUMER_SHA256:
        raise Refusal("successor consumer bytes mismatch")
    compile(new, str(CONSUMER), "exec")
    return new


def assert_absent() -> None:
    for path in ABSENT:
        if os.path.lexists(path):
            raise Refusal(f"L12 output must remain absent: {path}")


def assert_l12_authorizations_absent() -> None:
    for path in (TARGET_A22, HOSTILE_A22):
        if os.path.lexists(path):
            raise Refusal(f"L12 authorization must remain absent after retirement: {path}")


def authenticate_preserved() -> None:
    for path, expected in PRESERVED.items():
        base.authenticate_file(path, expected, f"preserved {path.name}")


def candidates() -> dict[str, object]:
    old_freeze = read_json(predecessor_path(str(FREEZE.relative_to(ROOT))))
    freeze = copy.deepcopy(old_freeze)
    freeze["files"][CONSUMER.name] = NEW_CONSUMER_SHA256

    old_preflight = read_json(predecessor_path(str(PREFLIGHT_RESULT.relative_to(ROOT))))
    preflight = copy.deepcopy(old_preflight)
    preflight["files"]["consumer_sha256"] = NEW_CONSUMER_SHA256
    preflight["files"]["freeze_sha256"] = digest_record(freeze)

    old_audit = read_json(predecessor_path(str(PREPAYLOAD.relative_to(ROOT))))
    audit = copy.deepcopy(old_audit)
    audit["audited_files_sha256"][CONSUMER.name] = NEW_CONSUMER_SHA256
    audit["audited_freeze_sha256"] = digest_record(freeze)
    audit["preflight_result_sha256"] = digest_record(preflight)

    old_gate = read_json(predecessor_path(str(BUILD_GATE.relative_to(ROOT))))
    gate = copy.deepcopy(old_gate)
    gate["files_sha256"][CONSUMER.name] = NEW_CONSUMER_SHA256
    gate["freeze_sha256"] = digest_record(freeze)
    gate["independent_hostile_audit"]["sha256"] = digest_record(audit)

    manifests: dict[int, dict[str, object]] = {}
    for length in (4, 6, 8, 10, 12):
        logical = f"{CACHE_ROOT.relative_to(ROOT)}/L{length}/CACHE_MANIFEST.json"
        old_manifest = read_json(predecessor_path(str(CACHE_ROOT.relative_to(ROOT))) / f"L{length}/CACHE_MANIFEST.json")
        manifest = copy.deepcopy(old_manifest)
        manifest["consumer_sha256"] = NEW_CONSUMER_SHA256
        manifest["freeze_sha256"] = digest_record(freeze)
        manifest["preflight_result_sha256"] = digest_record(preflight)
        manifest["independent_hostile_audit_sha256"] = digest_record(audit)
        manifest["cache_build_authorization_gate_sha256"] = digest_record(gate)
        manifests[length] = manifest

    old_postbuild = read_json(predecessor_path(str(POSTBUILD.relative_to(ROOT))))
    postbuild = copy.deepcopy(old_postbuild)
    postbuild["manifest_sha256"] = digest_record(manifests[12])

    old_l10_auth = read_json(predecessor_path(str(L10_AUTH.relative_to(ROOT))))
    l10_auth = copy.deepcopy(old_l10_auth)
    l10_auth.update({
        "consumer_sha256": NEW_CONSUMER_SHA256,
        "freeze_sha256": digest_record(freeze),
        "preflight_result_sha256": digest_record(preflight),
        "independent_hostile_audit_sha256": digest_record(audit),
        "l10_cache_manifest_sha256": digest_record(manifests[10]),
    })
    result: dict[str, object] = {
        "freeze": freeze, "preflight": preflight, "prepayload": audit,
        "build_gate": gate, "manifests": manifests,
        "postbuild": postbuild, "l10_authorization": l10_auth,
    }
    observed = {
        key: digest_record(result[key]) for key in
        ("freeze", "preflight", "prepayload", "build_gate", "postbuild", "l10_authorization")
    }
    observed["manifests"] = {length: digest_record(record) for length, record in manifests.items()}
    if observed != EXPECTED:
        raise Refusal("deterministic successor chain mismatch")
    del logical
    return result


def dry_run() -> dict[str, object]:
    rows = census()
    assert_absent()
    authenticate_preserved()
    raw = successor_bytes()
    records = candidates()
    consumer = load_successor_module(
        "consume_cache_v004r4_successor_dry_run_authenticated", raw,
    )
    validate_control_chain(records, consumer)
    if (
        consumer.positive_integer(True)
        or consumer.positive_integer(0)
        or consumer.positive_integer(-1)
        or consumer.positive_integer(1.0)
        or not consumer.positive_integer(1)
    ):
        raise Refusal("successor positive-integer semantics mismatch")
    return {
        "schema": "STAGE3_SECOND_LAUNCH_RECOVERY_DRY_RUN_V001",
        "classification": "PASS_FIXED_SCOPE_DRY_RUN_NO_MUTATION",
        "authenticated_predecessor_entries": len(rows),
        "authenticated_required_absences": len(ABSENT),
        "successor_consumer_sha256": NEW_CONSUMER_SHA256,
        "deterministic_candidate_sha256": {
            key: ({str(k): v for k, v in value.items()} if type(value) is dict else value)
            for key, value in EXPECTED.items()
        },
        "runtime_derived_after_replay": ["L10_history", "L10_gate", "A18"],
        "l12_launched": False,
        "claim_boundary": "DRY_RUN_ONLY__NO_RETIREMENT_CACHE_HISTORY_PUBLICATION_OR_L12_LAUNCH",
    }


def publish_json_once(path: Path, record: Mapping[str, object]) -> str:
    expected = digest_record(record)
    if os.path.lexists(path):
        base.authenticate_file(path, expected, f"existing successor {path.name}")
        if read_json(path) != dict(record):
            raise Refusal(f"existing successor content mismatch: {path}")
        return expected
    return base.publish_once(path, record)


def publish_bytes_once(path: Path, raw: bytes, expected: str) -> str:
    if hashlib.sha256(raw).hexdigest() != expected:
        raise Refusal("raw successor publication hash mismatch")
    if os.path.lexists(path):
        base.authenticate_file(path, expected, f"existing successor {path.name}")
        if path.read_bytes() != raw:
            raise Refusal("existing successor bytes mismatch")
        return expected
    if not path.parent.is_dir() or path.parent.is_symlink():
        raise Refusal("raw successor publication parent is absent or aliased")
    temporary = path.parent / f".{path.name}.recovery-{os.getpid()}-{os.urandom(8).hex()}"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o400,
    )
    linked = False
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise Refusal("short raw successor write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        os.link(temporary, path, follow_symlinks=False)
        linked = True
        os.unlink(temporary)
        base._fsync_directory(path.parent)
        base.authenticate_file(path, expected, f"published successor {path.name}")
        return expected
    finally:
        os.close(descriptor)
        if not linked and temporary.exists():
            temporary.unlink()


def retire(rows: list[dict[str, object]]) -> str:
    AUDIT_ROOT.mkdir(mode=0o755, exist_ok=True)
    CUSTODY.mkdir(mode=0o755, exist_ok=True)
    EVENTS.mkdir(mode=0o755, exist_ok=True)
    intent = {
        "schema": "STAGE3_SECOND_LAUNCH_OWNER_ONCE_RETIREMENT_INTENT_V001",
        "classification": "RETIRE_EXACT_SECOND_FAILED_LAUNCH_LINEAGE",
        "entries": rows,
        "entry_count": len(rows),
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_HISTORY_OR_L12_RESULT",
    }
    intent_hash = publish_json_once(INTENT, intent)
    event_hashes: list[str] = []
    for ordinal, row in enumerate(rows, start=1):
        logical = str(row["path"])
        source = ROOT.joinpath(*PurePosixPath(logical).parts)
        destination = CUSTODY.joinpath(*PurePosixPath(logical).parts)
        source_is_predecessor = _matches_predecessor(source, logical)
        destination_is_predecessor = _matches_predecessor(destination, logical)
        if source_is_predecessor == destination_is_predecessor:
            raise Refusal(f"predecessor retirement custody is not exclusive: {logical}")
        if source_is_predecessor:
            if os.path.lexists(destination):
                raise Refusal(f"retirement destination is occupied: {logical}")
            destination.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
            observed = (base._file_census(source, logical) if row["kind"] == "file"
                        else base._directory_census(source, logical))
            if observed != row:
                raise Refusal(f"predecessor changed before retirement: {logical}")
            base._rename_exclusive(source, destination)
            base._fsync_directory(source.parent)
            base._fsync_directory(destination.parent)
        observed = (base._file_census(destination, logical) if row["kind"] == "file"
                    else base._directory_census(destination, logical))
        if observed != row:
            raise Refusal(f"retired predecessor mismatch: {logical}")
        event = {
            "schema": "STAGE3_SECOND_LAUNCH_OWNER_ONCE_RETIREMENT_EVENT_V001",
            "ordinal": ordinal,
            "path": logical,
            "entry_sha256": base.sha256_bytes(base.canonical_json_bytes(row)),
            "intent_sha256": intent_hash,
        }
        event_hashes.append(publish_json_once(EVENTS / f"EVENT_{ordinal:03d}.json", event))
    receipt = {
        "schema": "STAGE3_SECOND_LAUNCH_OWNER_ONCE_RETIREMENT_RECEIPT_V001",
        "classification": "PASS_EXACT_SECOND_FAILED_LAUNCH_RETIREMENT",
        "intent_sha256": intent_hash,
        "event_sha256_by_ordinal": event_hashes,
        "entry_count": len(rows),
        "claim_boundary": "CUSTODY_ONLY__NO_NEW_HISTORY_OR_L12_RESULT",
    }
    return publish_json_once(RECEIPT, receipt)


def load_successor_module(name: str, raw: bytes):
    if hashlib.sha256(raw).hexdigest() != NEW_CONSUMER_SHA256:
        raise Refusal("successor module byte hash mismatch")
    if name in sys.modules:
        raise Refusal("successor hostile consumer module name is occupied")
    import types
    module = types.ModuleType(name)
    module.__file__ = str(CONSUMER)
    module.__authenticated_sha256__ = NEW_CONSUMER_SHA256
    sys.path.insert(0, str(HOSTILE))
    sys.modules[name] = module
    try:
        exec(compile(raw, str(CONSUMER), "exec"), module.__dict__)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    finally:
        if sys.path[0] == str(HOSTILE):
            sys.path.pop(0)
    if Path(module.__file__).resolve() != CONSUMER:
        raise Refusal("successor hostile consumer path mismatch")
    return module


def import_successor_consumer():
    base.authenticate_file(CONSUMER, NEW_CONSUMER_SHA256, "successor hostile consumer")
    return load_successor_module(
        "consume_cache_v004r4_successor_live_authenticated",
        CONSUMER.read_bytes(),
    )


def validate_control_chain(records: Mapping[str, object], consumer) -> None:
    freeze = records["freeze"]
    audit = records["prepayload"]
    gate = records["build_gate"]
    consumer.validate_hostile_prepayload_audit(
        audit,
        freeze_sha256=str(EXPECTED["freeze"]),
        frozen_files=freeze["files"],
        preflight_result_sha256=str(EXPECTED["preflight"]),
    )
    consumer.validate_hostile_build_authorization(
        gate,
        audit,
        freeze_sha256=str(EXPECTED["freeze"]),
        frozen_files=freeze["files"],
        audit_sha256=str(EXPECTED["prepayload"]),
    )
    custody = consumer.AuthorityCustody()
    try:
        consumer.retain_build_authorization_inputs(custody, gate)
        custody.verify_all()
    finally:
        custody.close()


def verify_or_build_caches(consumer) -> None:
    expected_manifests = EXPECTED["manifests"]
    source_hashes = {
        "method": base.PINNED_SOURCE_SHA256[base.METHOD],
        "builder": base.PINNED_SOURCE_SHA256[base.BUILDER],
        "consumer": NEW_CONSUMER_SHA256,
        "preflight": base.PINNED_SOURCE_SHA256[base.PREFLIGHT],
    }
    for length in (4, 6, 8, 10, 12):
        root = CACHE_ROOT / f"L{length}"
        manifest = root / "CACHE_MANIFEST.json"
        expected = expected_manifests[length]
        if not os.path.lexists(root):
            base.run_checked(
                [sys.executable, "-B", str(HOSTILE / "build_cache_v004r4.py"),
                 "build", "--length", str(length)],
                f"successor hostile L{length} cache build",
            )
        if not root.is_dir() or not manifest.is_file():
            raise Refusal(f"preserved partial successor cache obstruction: L{length}")
        base.authenticate_file(manifest, expected, f"successor L{length} manifest")
        record = read_json(manifest)
        context = consumer.CacheContext(
            length, root, record, str(expected), source_hashes, time.monotonic(),
        )
        try:
            context.reauthenticate()
        finally:
            context.close()


def validate_l10_history(path: Path, consumer) -> str:
    row = base._file_census(path, str(path.relative_to(ROOT)))
    history_hash = str(row["sha256"])
    base.authenticate_file(path, history_hash, "successor L10 history")
    history = read_json(path)
    if base.sha256(path) != history_hash:
        raise Refusal("successor L10 history changed during validation")
    expected_source = {
        "consumer_sha256": NEW_CONSUMER_SHA256,
        "builder_sha256": base.PINNED_SOURCE_SHA256[base.BUILDER],
        "method_sha256": base.PINNED_SOURCE_SHA256[base.METHOD],
        "preflight_sha256": base.PINNED_SOURCE_SHA256[base.PREFLIGHT],
        "freeze_sha256": EXPECTED["freeze"],
        "preflight_result_sha256": EXPECTED["preflight"],
        "independent_hostile_audit_sha256": EXPECTED["prepayload"],
        "cache_manifest_sha256": EXPECTED["manifests"][10],
        "cache_build_authorization_gate_sha256": EXPECTED["build_gate"],
        "l10_execution_authorization_gate_sha256": EXPECTED["l10_authorization"],
    }
    if (
        set(history) != consumer.L10_HISTORY_KEYS
        or history.get("schema") != "HOSTILE_CACHED_PREFIX_HISTORY_V004R4"
        or history.get("L") != 10 or type(history.get("L")) is not int
        or history.get("events") != 10
        or history.get("dimension") != 30_045_015
        or history.get("preterminal_dimension") != 10_015_005
        or any(history.get(key) != value for key, value in expected_source.items())
        or history.get("claim_boundary")
        != "FINITE_CACHED_HOSTILE_V004R4_HISTORY_ONLY__NO_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
        or set(history.get("resource", {})) != consumer.RESOURCE_KEYS
    ):
        raise Refusal("successor L10 history identity/lineage mismatch")
    resource = history["resource"]
    if (
        resource["peak_logical_state_plus_cache_bytes"] != 254_478_616
        or resource["scratch_limit_bytes"] != 21_474_836_480
        or type(resource["maximum_numerical_allocation_estimate_bytes"]) is not int
        or not 0 < resource["maximum_numerical_allocation_estimate_bytes"] <= 1_400_000_000
        or resource["numerical_workspace_limit_bytes"] != 1_400_000_000
        or resource["authentication_peak_certificate_bytes"] != 14_874_736
        or type(resource["peak_rss_bytes"]) is not int
        or not 0 < resource["peak_rss_bytes"] <= 17_179_869_184
        or resource["rss_limit_bytes"] != 17_179_869_184
        or type(resource["wall_seconds_including_authentication"]) is not float
        or not 0.0 < resource["wall_seconds_including_authentication"] <= 21_600.0
        or resource["wall_limit_seconds"] != 21_600.0
        or resource["passed"] is not True
    ):
        raise Refusal("successor L10 history resource gate mismatch")
    consumer.validate_native_rows(history["rows"], 10)
    consumer.validate_comparison(history["comparison"], 10)
    shards = history.get("terminal_shards")
    if type(shards) is not list or len(shards) != 10:
        raise Refusal("successor L10 terminal shard census mismatch")
    for index, shard in enumerate(shards):
        shape = [math.comb(9, index), math.comb(20, index)]
        if (
            type(shard) is not dict
            or set(shard) != {"bytes", "path", "q", "sha256", "shape"}
            or type(shard.get("path")) is not str
            or shard.get("q") != index or type(shard.get("q")) is not int
            or shard.get("shape") != shape
            or shard.get("bytes") != 16 * math.prod(shape)
        ):
            raise Refusal("successor L10 terminal shard binding malformed")
        shard_path = Path(shard["path"])
        if shard_path != WORKSPACES / f"L10/sharp/prefix_09/q_{index:02d}.c128":
            raise Refusal("successor L10 terminal shard path mismatch")
        base.authenticate_file(
            shard_path, str(shard.get("sha256")),
            f"successor L10 terminal shard q={index}",
        )
    custody = consumer.AuthorityCustody()
    try:
        consumer.authenticate_l10_context(custody)
        custody.verify_all()
    finally:
        custody.close()
    return history_hash


def construct_l10_gate(template: Mapping[str, object], history_hash: str) -> dict[str, object]:
    gate = copy.deepcopy(template)
    gate["consumer_sha256"] = NEW_CONSUMER_SHA256
    gate["freeze_sha256"] = EXPECTED["freeze"]
    gate["preflight_result_sha256"] = EXPECTED["preflight"]
    gate["independent_hostile_audit_sha256"] = EXPECTED["prepayload"]
    gate["cache_manifest_sha256_by_L"] = {"10": EXPECTED["manifests"][10]}
    gate["l10_execution_authorization"]["sha256"] = EXPECTED["l10_authorization"]
    gate["histories"][0]["sha256"] = history_hash
    if gate["checks_passed"] != gate["checks_total"] or gate["failures"] != []:
        raise Refusal("successor L10 gate template is not all-pass")
    return gate


def execute_live(authorization: str | None) -> dict[str, object]:
    if authorization != LIVE_AUTHORIZATION:
        raise Refusal("exact live authorization is absent")
    if os.path.lexists(RESULT):
        raise Refusal("completed recovery result already exists")
    rows = census()
    assert_absent()
    authenticate_preserved()
    new_consumer = successor_bytes()
    records = candidates()
    l10_gate_template = read_json(predecessor_path(str(L10_GATE.relative_to(ROOT))))
    receipt_hash = retire(rows)

    publish_bytes_once(CONSUMER, new_consumer, NEW_CONSUMER_SHA256)
    publish_json_once(FREEZE, records["freeze"])
    assert_l12_authorizations_absent()
    assert_absent()
    if not os.path.lexists(PREFLIGHT_RESULT):
        base.run_checked(
            [sys.executable, "-B", str(HOSTILE / "validate_cache_preflight_v004r4.py"), "run"],
            "successor hostile nonphysical preflight",
        )
    base.authenticate_file(PREFLIGHT_RESULT, str(EXPECTED["preflight"]), "successor preflight")
    publish_json_once(PREPAYLOAD, records["prepayload"])
    publish_json_once(BUILD_GATE, records["build_gate"])
    consumer = import_successor_consumer()
    validate_control_chain(records, consumer)
    verify_or_build_caches(consumer)
    publish_json_once(POSTBUILD, records["postbuild"])
    publish_json_once(L10_AUTH, records["l10_authorization"])

    history_path = OUTPUTS / "HISTORY_L10.json"
    if os.path.lexists(history_path) or os.path.lexists(WORKSPACES):
        raise Refusal("preserved pre-existing successor L10 execution requires adjudication")
    base.run_checked(
        [sys.executable, "-B", str(CONSUMER), "execute", "--length", "10"],
        "successor hostile exact L10 history",
    )
    history_hash = validate_l10_history(history_path, consumer)
    l10_gate = construct_l10_gate(l10_gate_template, history_hash)
    l10_gate_hash = publish_json_once(L10_GATE, l10_gate)

    if not os.path.lexists(SHARED):
        SHARED.mkdir(mode=0o755)
    elif SHARED.is_symlink() or not SHARED.is_dir() or list(SHARED.iterdir()):
        raise Refusal("pre-existing shared root is not the empty A18 publication checkpoint")
    a18, a18_hash = base.construct_a18(records["build_gate"])
    if publish_json_once(base.A18, a18) != a18_hash:
        raise Refusal("successor A18 publication mismatch")
    if sorted(path.name for path in SHARED.iterdir()) != [base.A18.name]:
        raise Refusal("shared root contains more than successor A18")
    assert_l12_authorizations_absent()
    assert_absent()
    result = {
        "schema": "STAGE3_SECOND_LAUNCH_RECOVERY_RESULT_V001",
        "classification": "PASS_SUCCESSOR_HOSTILE_LINEAGE_READY_FOR_VERSIONED_FRAMING",
        "retirement_receipt_sha256": receipt_hash,
        "successor_consumer_sha256": NEW_CONSUMER_SHA256,
        "freeze_sha256": EXPECTED["freeze"],
        "preflight_result_sha256": EXPECTED["preflight"],
        "prepayload_audit_sha256": EXPECTED["prepayload"],
        "build_gate_sha256": EXPECTED["build_gate"],
        "cache_manifest_sha256_by_L": {
            str(length): digest for length, digest in EXPECTED["manifests"].items()
        },
        "postbuild_audit_sha256": EXPECTED["postbuild"],
        "l10_authorization_sha256": EXPECTED["l10_authorization"],
        "l10_history_sha256": history_hash,
        "l10_gate_sha256": l10_gate_hash,
        "a18_sha256": a18_hash,
        "required_l12_absences": len(ABSENT),
        "l12_launched": False,
        "claim_boundary": "FINITE_HOSTILE_REPAIR_CACHE_AND_L10_RECERTIFICATION_ONLY__NO_L12_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT",
    }
    AUDIT_ROOT.mkdir(mode=0o755, exist_ok=True)
    publish_json_once(RESULT, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("plan", "dry-run", "execute"))
    parser.add_argument("--authorization")
    args = parser.parse_args()
    try:
        if args.mode == "plan":
            output = {
                "schema": "STAGE3_SECOND_LAUNCH_RECOVERY_PLAN_V001",
                "classification": "NONEXECUTING_FIXED_SCOPE_PLAN",
                "retire_exactly": len(STALE), "require_absent": len(ABSENT),
                "successor_consumer_sha256": NEW_CONSUMER_SHA256,
                "only_physical_replay": "HOSTILE_L10",
                "stops_before_l12": True,
            }
        elif args.mode == "dry-run":
            if args.authorization is not None:
                raise Refusal("dry-run rejects authorization")
            output = dry_run()
        else:
            output = execute_live(args.authorization)
    except (OSError, RuntimeError, ValueError, Refusal) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
