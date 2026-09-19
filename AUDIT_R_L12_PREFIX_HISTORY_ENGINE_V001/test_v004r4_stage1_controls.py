#!/usr/bin/env python3
"""Focused nonphysical adversarial tests for the Stage-1 hostile custody repair."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import socket
import stat
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock
from pathlib import Path

import consume_cache_v004r4 as contract
import validate_cache_preflight_v004r4 as preflight


HASH = "1" * 64
FILES = {"source.py": "2" * 64}


def valid_audit() -> dict[str, object]:
    return {
        "schema": "HOSTILE_V004R4_PREPAYLOAD_AUDIT_V001",
        "classification": "PASS_HOSTILE_V004R4_PREPAYLOAD_CONTROL_AND_SHARED_GATE_INTERFACE",
        "auditor_role": "INDEPENDENT_HOSTILE_READ_ONLY_REVIEW",
        "audited_freeze_sha256": HASH,
        "audited_files_sha256": FILES,
        "preflight_result_sha256": "3" * 64,
        "checks_passed": 19,
        "checks_total": 19,
        "failures": [],
        "v004r3_bytes_preserved": True,
        "absence_census": dict(contract.HOSTILE_AUDIT_ABSENCE),
        "payload_or_history_executed": False,
        "claim_boundary": "NONPHYSICAL_V004R4_CONTROL_PLANE_AUDIT_ONLY",
    }


def valid_gate(audit: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "HOSTILE_V004R4_CACHE_BUILD_AUTHORIZATION_GATE",
        "classification": "AUTHORIZE_HOSTILE_V004R4_CACHE_AFTER_INDEPENDENT_AUDIT",
        "authorized_cache_lengths": [4, 6, 8, 10, 12],
        "freeze_sha256": HASH,
        "files_sha256": FILES,
        "independent_hostile_audit": {
            "path": str(contract.INDEPENDENT_AUDIT),
            "sha256": "4" * 64,
            "schema": audit["schema"],
            "classification": audit["classification"],
            "checks_passed": audit["checks_passed"],
            "checks_total": audit["checks_total"],
        },
        "target_v012_interface": {
            "freeze_sha256": "5" * 64,
            "freeze_schema": "TARGET_L12_STORAGE_CACHE_FREEZE_V012",
            "audit_sha256": "6" * 64,
            "audit_schema": "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001",
            "audit_classification": "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE",
            "consumer_sha256": "7" * 64,
            "L10_gate_sha256": "8" * 64,
            "L10_gate_schema": "TARGET_V012_CACHED_L10_GATE",
            "L10_gate_classification": "PASS_TARGET_V012_CACHED_L10",
            "L12_cache_manifest_sha256": "9" * 64,
            "L12_cache_manifest_schema": "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
        },
        "dual_obstruction_custody": copy.deepcopy(
            contract.r2consumer.common.OBSTRUCTION_ROWS
        ),
        "claim_boundary": "CACHE_BUILD_AUTHORIZATION_ONLY__NO_HISTORY_OR_PHYSICS_RESULT",
    }


class AuditIntersectionTests(unittest.TestCase):
    def assert_audit_refuses(self, path: tuple[str, ...], value: object) -> None:
        row = copy.deepcopy(valid_audit())
        target: dict[str, object] = row
        for name in path[:-1]:
            target = target[name]  # type: ignore[assignment]
        if value is None:
            del target[path[-1]]
        else:
            target[path[-1]] = value
        with self.assertRaises(contract.Refusal):
            contract.validate_hostile_prepayload_audit(
                row, freeze_sha256=HASH, frozen_files=FILES,
                preflight_result_sha256="3" * 64,
            )

    def test_exact_audit_intersection_accepts(self) -> None:
        self.assertEqual(
            contract.validate_hostile_prepayload_audit(
                valid_audit(), freeze_sha256=HASH, frozen_files=FILES,
                preflight_result_sha256="3" * 64,
            )["checks_total"],
            19,
        )

    def test_audit_mutations_refuse(self) -> None:
        for path, value in (
            (("preflight_result_sha256",), None),
            (("auditor_role",), "SELF_REVIEW"),
            (("v004r3_bytes_preserved",), False),
            (("absence_census", "postbuild_payload_audit"), True),
            (("payload_or_history_executed",), True),
            (("claim_boundary",), "PHYSICS_RESULT"),
        ):
            with self.subTest(path=path):
                self.assert_audit_refuses(path, value)

    def test_build_gate_binds_exact_audit(self) -> None:
        audit = valid_audit()
        gate = valid_gate(audit)
        contract.validate_hostile_build_authorization(
            gate, audit, freeze_sha256=HASH, frozen_files=FILES,
            audit_sha256="4" * 64,
        )
        for mutation in (
            lambda row: row["independent_hostile_audit"].update({"checks_total": 20}),
            lambda row: row["target_v012_interface"].update(
                {"L10_gate_schema": "WRONG"}
            ),
            lambda row: row.update({"dual_obstruction_custody": {"target": {}}}),
            lambda row: row.update({"claim_boundary": "PHYSICAL"}),
            lambda row: row.update({"extra": False}),
        ):
            changed = copy.deepcopy(gate)
            mutation(changed)
            with self.assertRaises(contract.Refusal):
                contract.validate_hostile_build_authorization(
                    changed, audit, freeze_sha256=HASH, frozen_files=FILES,
                    audit_sha256="4" * 64,
                )


class OrchestratorWireTests(unittest.TestCase):
    def test_ready_release_ack_round_trip(self) -> None:
        parent, child = socket.socketpair()
        channel_id = "6" * 64
        session = contract.OrchestratedWorkerSession(
            role="hostile_v004r4", worker_id="hostile-test", control_fd=child.fileno(),
            control_channel_id=channel_id, executable=contract.CONSUMER,
            workspace=contract.WORKSPACE, output=contract.OUTPUT,
        )
        observed: dict[str, object] = {}

        def coordinator() -> None:
            ready_raw = b""
            while not ready_raw.endswith(b"\n"):
                ready_raw += parent.recv(4096)
            ready = json.loads(ready_raw)
            observed["ready"] = ready
            release = {
                "schema": contract.RELEASE_SCHEMA,
                "role": ready["role"], "worker_id": ready["worker_id"],
                "process_id": ready["process_id"],
                "process_start_token": ready["process_start_token"],
                "control_channel_id": ready["control_channel_id"],
                "nonce_commitment_sha256": ready["nonce_commitment_sha256"],
                "handshake_sha256": "7" * 64,
                "worker_release_sha256": "8" * 64,
                "release_epoch": int(time.time()),
            }
            release_raw = contract.canonical_json_bytes(release)
            observed["release_raw"] = release_raw
            parent.sendall(release_raw)
            ack_raw = b""
            while not ack_raw.endswith(b"\n"):
                ack_raw += parent.recv(4096)
            observed["ack"] = json.loads(ack_raw)

        thread = threading.Thread(target=coordinator)
        thread.start()
        try:
            session.announce_and_wait()
            session.acknowledge()
            thread.join(timeout=5.0)
            self.assertFalse(thread.is_alive())
            ready = observed["ready"]
            ack = observed["ack"]
            nonce = bytes.fromhex(ack["nonce_hex"])
            self.assertEqual(
                ready["nonce_commitment_sha256"],
                hashlib.sha256(contract.NONCE_DOMAIN + nonce).hexdigest(),
            )
            self.assertEqual(
                ack["ack_sha256"], hashlib.sha256(
                    contract.ACK_DOMAIN + nonce + observed["release_raw"]
                ).hexdigest(),
            )
        finally:
            session.close()
            parent.close()
            child.close()

    def test_non_socket_and_executable_drift_refuse(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "worker.py"
            path.write_bytes(b"pass\n")
            descriptor = os.open(path, os.O_RDONLY)
            try:
                with self.assertRaises(contract.Refusal):
                    contract.OrchestratedWorkerSession(
                        role="hostile_v004r4", worker_id="x", control_fd=descriptor,
                        control_channel_id="9" * 64, executable=path,
                        workspace=Path(temporary) / "w", output=Path(temporary) / "o",
                    )
            finally:
                os.close(descriptor)

            parent, child = socket.socketpair()
            session = contract.OrchestratedWorkerSession(
                role="hostile_v004r4", worker_id="x", control_fd=child.fileno(),
                control_channel_id="9" * 64, executable=path,
                workspace=Path(temporary) / "w", output=Path(temporary) / "o",
            )
            try:
                path.write_bytes(b"changed\n")
                with self.assertRaises(contract.Refusal):
                    session._verify_executable()
            finally:
                session.close()
                parent.close()
                child.close()

    def test_release_identity_mutations_refuse(self) -> None:
        mutations = (
            ("role", "target_v012"),
            ("process_id", os.getpid() + 1),
            ("process_start_token", "0" * 64),
            ("nonce_commitment_sha256", "0" * 64),
            ("handshake_sha256", "not-a-digest"),
            ("release_epoch", True),
        )
        for key, value in mutations:
            with self.subTest(key=key):
                parent, child = socket.socketpair()
                session = contract.OrchestratedWorkerSession(
                    role="hostile_v004r4", worker_id="mutant",
                    control_fd=child.fileno(), control_channel_id="a" * 64,
                    executable=contract.CONSUMER, workspace=contract.WORKSPACE,
                    output=contract.OUTPUT,
                )

                def coordinator() -> None:
                    raw = b""
                    while not raw.endswith(b"\n"):
                        raw += parent.recv(4096)
                    ready = json.loads(raw)
                    release = {
                        "schema": contract.RELEASE_SCHEMA,
                        "role": ready["role"], "worker_id": ready["worker_id"],
                        "process_id": ready["process_id"],
                        "process_start_token": ready["process_start_token"],
                        "control_channel_id": ready["control_channel_id"],
                        "nonce_commitment_sha256": ready["nonce_commitment_sha256"],
                        "handshake_sha256": "b" * 64,
                        "worker_release_sha256": "c" * 64,
                        "release_epoch": int(time.time()),
                    }
                    release[key] = value
                    parent.sendall(contract.canonical_json_bytes(release))

                thread = threading.Thread(target=coordinator)
                thread.start()
                try:
                    with self.assertRaises(contract.Refusal):
                        session.announce_and_wait()
                    thread.join(timeout=5.0)
                    self.assertFalse(thread.is_alive())
                finally:
                    session.close()
                    parent.close()
                    child.close()

    def test_target_and_hostile_completion_frames_hold_live_until_eof(self) -> None:
        target_path = contract.ROOT / (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
        )
        specification = importlib.util.spec_from_file_location(
            "stage1_target_consumer_completion_test", target_path,
        )
        target = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = target
        specification.loader.exec_module(target)

        roles = (
            (
                contract, contract.OrchestratedWorkerSession,
                "hostile_v004r4", contract.CONSUMER,
                contract.canonical_json_bytes,
            ),
            (
                target, target.OrchestratedWorkerSession,
                "target_v012", target_path, target._wire_canonical_json,
            ),
        )
        for module, session_type, role, executable, canonical in roles:
            with self.subTest(role=role), tempfile.TemporaryDirectory(
                dir="/private/tmp"
            ) as temporary:
                root = Path(temporary).resolve()
                output = root / "history.json"
                parent, child = socket.socketpair()
                keyword = {
                    "worker_id": f"{role}-completion-test",
                    "control_fd": child.fileno(),
                    "control_channel_id": hashlib.sha256(
                        f"{role}-channel".encode("ascii")
                    ).hexdigest(),
                    "executable": executable,
                    "workspace": root / "workspace",
                    "output": output,
                }
                if role == "hostile_v004r4":
                    keyword["role"] = role
                session = session_type(**keyword)
                observed: dict[str, object] = {}

                def receive_line() -> bytes:
                    raw = b""
                    while not raw.endswith(b"\n"):
                        block = parent.recv(4096)
                        if not block:
                            raise AssertionError("worker channel closed before record")
                        raw += block
                    return raw

                def coordinator() -> None:
                    ready = json.loads(receive_line())
                    release = {
                        "schema": module.RELEASE_SCHEMA,
                        "role": ready["role"],
                        "worker_id": ready["worker_id"],
                        "process_id": ready["process_id"],
                        "process_start_token": ready["process_start_token"],
                        "control_channel_id": ready["control_channel_id"],
                        "nonce_commitment_sha256": ready[
                            "nonce_commitment_sha256"
                        ],
                        "handshake_sha256": hashlib.sha256(
                            f"{role}-handshake".encode("ascii")
                        ).hexdigest(),
                        "worker_release_sha256": hashlib.sha256(
                            f"{role}-release".encode("ascii")
                        ).hexdigest(),
                        "release_epoch": int(time.time()),
                    }
                    parent.sendall(canonical(release))
                    observed["ack"] = json.loads(receive_line())
                    completion_raw = receive_line()
                    observed["completion_raw"] = completion_raw
                    observed["completion"] = json.loads(completion_raw)
                    parent.shutdown(socket.SHUT_WR)

                thread = threading.Thread(target=coordinator)
                thread.start()
                try:
                    session.announce_and_wait()
                    session.acknowledge()
                    output.write_bytes(b"authenticated history\n")
                    output.chmod(0o444)
                    digest = hashlib.sha256(output.read_bytes()).hexdigest()
                    result = session.complete(digest)
                    thread.join(timeout=5.0)
                    self.assertFalse(thread.is_alive())
                    self.assertEqual(result, observed["completion"])
                    self.assertEqual(
                        observed["completion_raw"], canonical(result),
                    )
                    self.assertLessEqual(len(observed["completion_raw"]), 2**20)
                    self.assertEqual(set(result), session.COMPLETION_KEYS)
                    self.assertEqual(result["schema"], module.COMPLETION_SCHEMA)
                    self.assertEqual(result["role"], role)
                    self.assertEqual(result["output_path"], str(output))
                    self.assertEqual(result["output_sha256"], digest)
                    self.assertIs(result["blocked_on_orchestrator_close"], True)
                    self.assertIs(type(result["completion_epoch"]), int)
                    self.assertGreater(result["completion_epoch"], 0)
                    with self.assertRaises(module.Refusal):
                        session.complete(digest)
                finally:
                    session.close()
                    thread.join(timeout=5.0)
                    parent.close()
                    child.close()


class CensusAndResourceTests(unittest.TestCase):
    def test_dependency_and_raw_c128_census(self) -> None:
        self.assertEqual(len(contract.EXECUTED_DEPENDENCIES), 8)
        self.assertTrue(all(path.is_file() for path in contract.EXECUTED_DEPENDENCIES.values()))
        self.assertEqual(
            contract.TARGET_V012_L12_MANIFEST,
            contract.TARGET_V012_DIR
            / "CACHE_PAYLOADS_V012/L12/CACHE_MANIFEST.json",
        )
        self.assertEqual(contract.EXPECTED_DISK_MINIMUM_BYTES, 9_600_935_128)
        self.assertEqual(9_600_954_452 + contract.EXPECTED_DISK_MINIMUM_BYTES,
                         19_201_889_580)
        self.assertNotEqual(contract.EXPECTED_DISK_MINIMUM_BYTES, 9_600_938_072)


class CustodyAndPublicationTests(unittest.TestCase):
    def test_cache_context_close_tolerates_semantic_mapping_already_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            payload = Path(temporary) / "mapping.c128"
            payload.write_bytes(bytes(16))
            mapping = contract.np.memmap(
                payload, dtype="<c16", mode="r", shape=(1,),
            )
            context = contract.CacheContext.__new__(contract.CacheContext)
            context.mappings = [mapping]
            context.fds = {}
            context.root_fd = -1
            context._close(mapping)
            context.close()

    def test_cache_contexts_refuse_postauthentication_ancestor_alias(self) -> None:
        target_path = contract.ROOT / (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
        )
        specification = importlib.util.spec_from_file_location(
            "stage1_target_cache_custody_test", target_path,
        )
        target = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = target
        specification.loader.exec_module(target)

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            base = Path(temporary).resolve()
            ancestor = base / "ancestor"
            held = base / "ancestor-held"
            root = ancestor / "cache"
            root.mkdir(parents=True)
            manifest = root / "CACHE_MANIFEST.json"
            payload = root / "payload.bin"
            manifest.write_bytes(b"{}\n")
            payload.write_bytes(b"payload")
            manifest.chmod(0o444)
            payload.chmod(0o444)
            root.chmod(0o555)

            target_cache = target.CacheContext.__new__(target.CacheContext)
            target_cache.closed = False
            target_cache.root = root
            target_cache.root_descriptor = os.open(
                root, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0),
            )
            target_cache.directory_identity = target._retained_directory_identity(
                root, target_cache.root_descriptor, "target cache fixture",
            )
            target_cache.manifest_descriptor = os.open(
                manifest.name, os.O_RDONLY, dir_fd=target_cache.root_descriptor,
            )
            target_cache.manifest_identity = target._cache_file_identity(
                os.fstat(target_cache.manifest_descriptor),
            )
            target_cache.manifest_sha256 = hashlib.sha256(b"{}\n").hexdigest()
            payload_descriptor = os.open(
                payload.name, os.O_RDONLY, dir_fd=target_cache.root_descriptor,
            )
            target_cache.descriptors = {payload.name: payload_descriptor}
            target_cache.identities = {
                payload.name: target._cache_file_identity(
                    os.fstat(payload_descriptor),
                )
            }
            target_cache.records = {
                payload.name: {"sha256": hashlib.sha256(b"payload").hexdigest()}
            }

            hostile_cache = contract.CacheContext.__new__(contract.CacheContext)
            hostile_cache.root = root
            hostile_cache.root_fd = os.dup(target_cache.root_descriptor)
            hostile_cache.root_identity = contract._file_identity(
                os.fstat(hostile_cache.root_fd),
            )
            hostile_cache.manifest_hash = target_cache.manifest_sha256
            hostile_manifest = os.open(
                manifest.name, os.O_RDONLY, dir_fd=hostile_cache.root_fd,
            )
            hostile_payload = os.open(
                payload.name, os.O_RDONLY, dir_fd=hostile_cache.root_fd,
            )
            hostile_cache.fds = {
                manifest.name: hostile_manifest, payload.name: hostile_payload,
            }
            hostile_cache.fingerprints = {
                name: contract._file_identity(os.fstat(descriptor))
                for name, descriptor in hostile_cache.fds.items()
            }
            hostile_cache.records = {
                payload.name: {"sha256": hashlib.sha256(b"payload").hexdigest()}
            }
            hostile_cache.mappings = []

            ancestor.rename(held)
            ancestor.symlink_to(held.name, target_is_directory=True)
            try:
                with self.assertRaises(target.Refusal):
                    target_cache.reauthenticate()
                with self.assertRaises(contract.Refusal):
                    hostile_cache.reauthenticate()
            finally:
                target_cache.close()
                hostile_cache.close()

    def test_mutable_legacy_evidence_is_retained_and_drift_refuses(self) -> None:
        row = contract.r2consumer.common.OBSTRUCTION_ROWS["target"]
        legacy = contract.ROOT / row["obstruction_path"]
        custody = contract.AuthorityCustody()
        try:
            custody.authenticate(
                legacy, "actual writable legacy evidence",
                row["obstruction_sha256"], immutable=False,
            )
            self.assertTrue(os.stat(legacy, follow_symlinks=False).st_mode & 0o222)
            self.assertFalse(custody.files[legacy].immutable_required)
            custody.verify_all()
        finally:
            custody.close()

        with tempfile.TemporaryDirectory() as temporary:
            path = (Path(temporary) / "legacy.txt").resolve()
            path.write_bytes(b"original")
            path.chmod(0o644)
            digest = hashlib.sha256(b"original").hexdigest()
            with self.assertRaises(contract.Refusal):
                immutable = contract.AuthorityCustody()
                try:
                    immutable.authenticate(path, "writable immutable evidence", digest)
                finally:
                    immutable.close()
            changed = contract.AuthorityCustody()
            try:
                changed.authenticate(
                    path, "mutable legacy evidence", digest, immutable=False,
                )
                changed.verify_all()
                path.write_bytes(b"changed")
                with self.assertRaises(contract.Refusal):
                    changed.verify_all()
            finally:
                changed.close()

    def test_retained_executable_reuse_is_exact_and_does_not_reopen(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            path = Path(temporary).resolve() / "worker.py"
            path.write_bytes(b"pass\n")
            path.chmod(0o444)
            digest = hashlib.sha256(b"pass\n").hexdigest()
            custody = contract.AuthorityCustody()
            try:
                custody.authenticate(path, "worker first custody", digest)
                descriptor = custody.files[path].descriptor
                _record, reused = custody.authenticate_or_reuse(
                    path, "worker handshake custody", digest,
                )
                self.assertEqual(reused, digest)
                self.assertEqual(custody.files[path].descriptor, descriptor)
                with self.assertRaises(contract.Refusal):
                    custody.authenticate_or_reuse(
                        path, "wrong worker handshake custody", "0" * 64,
                    )
            finally:
                custody.close()

            path.chmod(0o644)
            legacy = contract.AuthorityCustody()
            try:
                legacy.authenticate(
                    path, "legacy worker custody", digest, immutable=False,
                )
                with self.assertRaises(contract.Refusal):
                    legacy.authenticate_or_reuse(
                        path, "invalid immutable promotion", digest,
                    )
            finally:
                legacy.close()

    def test_retained_authority_refuses_parent_symlink_alias(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            parent = root / "authority-parent"
            original = root / "authority-parent-original"
            parent.mkdir()
            path = parent / "record.json"
            path.write_text("{}\n", encoding="utf-8")
            path.chmod(0o444)
            custody = contract.AuthorityCustody()
            try:
                custody.authenticate(path, "parent-alias authority")
                os.rename(parent, original)
                parent.symlink_to(original, target_is_directory=True)
                with self.assertRaisesRegex(
                    contract.Refusal, "retained authority changed"
                ):
                    custody.verify_all()
            finally:
                custody.close()

    def test_authority_custody_refuses_hardlink_parent_swap_and_hash_race(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            path = root / "hardlinked.json"
            path.write_text("{}\n", encoding="utf-8")
            path.chmod(0o444)
            os.link(path, root / "alias.json")
            custody = contract.AuthorityCustody()
            try:
                with self.assertRaisesRegex(contract.Refusal, "immutable ordinary file"):
                    custody.authenticate(path, "hardlinked authority")
            finally:
                custody.close()

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            parent = root / "authority-parent"
            held = root / "authority-parent-held"
            parent.mkdir()
            path = parent / "record.json"
            path.write_text("{}\n", encoding="utf-8")
            path.chmod(0o444)
            custody = contract.AuthorityCustody()
            try:
                custody.authenticate(path, "parent-swap authority")
                parent.rename(held)
                parent.mkdir()
                replacement = parent / path.name
                replacement.write_text("{}\n", encoding="utf-8")
                replacement.chmod(0o444)
                with self.assertRaisesRegex(
                    contract.Refusal, "retained authority changed"
                ):
                    custody.verify_all()
            finally:
                custody.close()

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            path = Path(temporary).resolve() / "metadata-race.json"
            path.write_text("{}\n", encoding="utf-8")
            path.chmod(0o444)
            original_hash = contract.descriptor_sha256

            def mutate_metadata(descriptor: int) -> str:
                digest = original_hash(descriptor)
                path.chmod(0o400)
                return digest

            custody = contract.AuthorityCustody()
            try:
                with mock.patch.object(
                    contract, "descriptor_sha256", side_effect=mutate_metadata,
                ), self.assertRaisesRegex(contract.Refusal, "changed during authentication"):
                    custody.authenticate(path, "metadata-race authority")
            finally:
                custody.close()

    def test_atomic_publish_keeps_postlink_failure_and_unowned_staging(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            output = root / "history.json"
            custody = contract.AuthorityCustody()
            try:
                with mock.patch.object(
                    contract, "fsync_directory", side_effect=OSError("forced fsync failure"),
                ):
                    with self.assertRaises(OSError):
                        contract.atomic_publish(output, {"L": 12}, custody)
                self.assertTrue(output.is_file())
                self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o444)
            finally:
                custody.close()

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            output = root / "history.json"

            class SwapCustody:
                def verify_all(self) -> None:
                    candidates = list(root.glob(f".{output.name}.staging-*"))
                    if len(candidates) != 1:
                        raise AssertionError("staging file census mismatch")
                    staging = candidates[0]
                    os.unlink(staging)
                    staging.write_bytes(b"unowned replacement")
                    raise contract.Refusal("forced prelink custody failure")

            with self.assertRaises(contract.Refusal):
                contract.atomic_publish(output, {"L": 12}, SwapCustody())
            candidates = list(root.glob(f".{output.name}.staging-*"))
            self.assertEqual(len(candidates), 1)
            staging = candidates[0]
            self.assertEqual(staging.read_bytes(), b"unowned replacement")
            self.assertFalse(output.exists())

    def test_atomic_publish_success_is_single_link_and_no_clobber(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            output = Path(temporary).resolve() / "history.json"
            custody = contract.AuthorityCustody()
            try:
                digest = contract.atomic_publish(output, {"L": 12}, custody)
                metadata = os.stat(output, follow_symlinks=False)
                self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o444)
                self.assertEqual(metadata.st_nlink, 1)
                self.assertEqual(
                    digest, hashlib.sha256(contract.canonical_json_bytes({"L": 12})).hexdigest(),
                )
                self.assertEqual(list(output.parent.glob(".*staging*")), [])
                with self.assertRaises(contract.Refusal):
                    contract.atomic_publish(output, {"L": 12}, custody)
            finally:
                custody.close()

    def test_publishers_refuse_parent_directory_swap(self) -> None:
        class SwapParentCustody:
            def __init__(self, parent: Path) -> None:
                self.parent = parent
                self.original = parent.with_name(parent.name + "-original")

            def verify_all(self) -> None:
                os.rename(self.parent, self.original)
                self.parent.mkdir()

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            parent = root / "history-parent"
            parent.mkdir()
            output = parent / "history.json"
            custody = SwapParentCustody(parent)
            with self.assertRaisesRegex(contract.Refusal, "parent identity changed"):
                contract.atomic_publish(output, {"L": 12}, custody)
            self.assertFalse(output.exists())
            self.assertEqual(
                list(custody.original.glob(f".{output.name}.staging-*")), [],
            )

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            parent = root / "preflight-parent"
            parent.mkdir()
            output = parent / "preflight.json"
            custody = SwapParentCustody(parent)
            with mock.patch.object(preflight, "OUTPUT", output):
                with self.assertRaisesRegex(
                    contract.Refusal, "parent identity changed"
                ):
                    preflight.publish({"schema": "TEMP"}, custody)
            self.assertFalse(output.exists())
            self.assertEqual(
                list(custody.original.glob(f".{output.name}.staging-*")), [],
            )

    def test_history_publisher_refuses_ancestor_symlink_to_same_parent(self) -> None:
        class AliasAncestorCustody:
            def __init__(self, ancestor: Path) -> None:
                self.ancestor = ancestor
                self.held = ancestor.with_name(ancestor.name + "-held")

            def verify_all(self) -> None:
                self.ancestor.rename(self.held)
                self.ancestor.symlink_to(self.held.name, target_is_directory=True)

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            ancestor = root / "ancestor"
            parent = ancestor / "history-parent"
            parent.mkdir(parents=True)
            output = parent / "history.json"
            custody = AliasAncestorCustody(ancestor)
            with self.assertRaisesRegex(contract.Refusal, "parent path is aliased"):
                contract.atomic_publish(output, {"L": 12}, custody)
            self.assertFalse(output.exists())
            held_parent = custody.held / parent.name
            self.assertEqual(
                list(held_parent.glob(f".{output.name}.staging-*")), [],
            )

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            root = Path(temporary).resolve()
            ancestor = root / "ancestor"
            parent = ancestor / "preflight-parent"
            parent.mkdir(parents=True)
            output = parent / "preflight.json"
            custody = AliasAncestorCustody(ancestor)
            with mock.patch.object(preflight, "OUTPUT", output):
                with self.assertRaisesRegex(contract.Refusal, "parent path is aliased"):
                    preflight.publish({"schema": "TEMP"}, custody)
            self.assertFalse(output.exists())
            held_parent = custody.held / parent.name
            self.assertEqual(
                list(held_parent.glob(f".{output.name}.staging-*")), [],
            )

    def test_preflight_publisher_keeps_postlink_failure(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            output = Path(temporary) / "preflight.json"
            custody = contract.AuthorityCustody()
            try:
                with mock.patch.object(preflight, "OUTPUT", output), mock.patch.object(
                    contract, "fsync_directory", side_effect=OSError("forced fsync failure"),
                ):
                    with self.assertRaises(OSError):
                        preflight.publish({"schema": "TEMP"}, custody)
                self.assertTrue(output.is_file())
                self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o444)
            finally:
                custody.close()


class CrossRoleAndFreshnessTests(unittest.TestCase):
    def test_cross_role_aliases_refuse(self) -> None:
        workers = {
            "target_v012": {
                "process_id": 100, "worker_id": "target",
                "control_channel_id": "a" * 64,
                "nonce_commitment_sha256": "b" * 64,
            },
            "hostile_v004r4": {
                "process_id": 101, "worker_id": "hostile",
                "control_channel_id": "c" * 64,
                "nonce_commitment_sha256": "d" * 64,
            },
        }
        authorizations = {
            "target_v012": "e" * 64, "hostile_v004r4": "f" * 64,
        }
        contract.validate_cross_role_identity_distinctness(
            workers, authorizations,
        )
        for field in (
            "process_id", "worker_id", "control_channel_id",
            "nonce_commitment_sha256",
        ):
            changed = copy.deepcopy(workers)
            changed["hostile_v004r4"][field] = changed["target_v012"][field]
            with self.subTest(field=field), self.assertRaises(contract.Refusal):
                contract.validate_cross_role_identity_distinctness(
                    changed, authorizations,
                )
        changed_authorizations = dict(authorizations)
        changed_authorizations["hostile_v004r4"] = authorizations["target_v012"]
        with self.assertRaises(contract.Refusal):
            contract.validate_cross_role_identity_distinctness(
                workers, changed_authorizations,
            )

    def test_preexisting_expired_records_refuse_on_both_workers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = (Path(temporary) / "authority.json").resolve()
            path.write_text("{}\n", encoding="utf-8")
            path.chmod(0o444)
            custody = contract.AuthorityCustody()
            try:
                with mock.patch.object(contract.time, "time", return_value=100):
                    with self.assertRaises(contract.Refusal):
                        contract.wait_authority(custody, path, "expired hostile", 99)
                self.assertNotIn(path, custody.files)
            finally:
                custody.close()

            target_path = contract.ROOT / (
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
            )
            specification = importlib.util.spec_from_file_location(
                "stage1_target_consumer_test", target_path,
            )
            target = importlib.util.module_from_spec(specification)
            sys.modules[specification.name] = target
            specification.loader.exec_module(target)
            with mock.patch.object(target.time, "time", return_value=100):
                with self.assertRaises(target.Refusal):
                    target._wait_for_immutable_record(
                        path, "expired target", 99,
                    )

    def test_authority_expiring_during_read_refuses_on_both_workers(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary:
            path = Path(temporary).resolve() / "authority.json"
            path.write_text("{}\n", encoding="utf-8")
            path.chmod(0o444)
            custody = contract.AuthorityCustody()
            try:
                with mock.patch.object(
                    contract.time, "time", side_effect=(99, 99, 101),
                ):
                    with self.assertRaisesRegex(contract.Refusal, "expired during"):
                        contract.wait_authority(custody, path, "hostile read", 100)
            finally:
                custody.close()

            target_path = contract.ROOT / (
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
            )
            specification = importlib.util.spec_from_file_location(
                "stage1_target_consumer_expiry_test", target_path,
            )
            target = importlib.util.module_from_spec(specification)
            sys.modules[specification.name] = target
            specification.loader.exec_module(target)
            with mock.patch.object(
                target.time, "time", side_effect=(99, 99, 101),
            ):
                with self.assertRaisesRegex(target.Refusal, "expired during"):
                    target._wait_for_immutable_record(
                        path, "target read", 100,
                    )

    def test_target_wire_records_hit_all_three_live_a22_sinks(self) -> None:
        target_path = contract.ROOT / (
            "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/consume_target_cache.py"
        )
        specification = importlib.util.spec_from_file_location(
            "stage1_target_consumer_wire_test", target_path,
        )
        target = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = target
        specification.loader.exec_module(target)
        parent, child = socket.socketpair()
        seen: list[str] = []
        original = target.builder.validate_production_obligation

        def traced(artifact_id: str, record: dict[str, object]) -> None:
            seen.append(record["schema"])
            original(artifact_id, record)

        def digest(label: str) -> str:
            return hashlib.sha256(label.encode("ascii")).hexdigest()

        with tempfile.TemporaryDirectory(dir="/private/tmp") as temporary, mock.patch.object(
            target.builder, "validate_production_obligation", side_effect=traced,
        ):
            session = target.OrchestratedWorkerSession(
                worker_id="target-test", control_fd=child.fileno(),
                control_channel_id=digest("channel"), executable=target_path,
                workspace=Path(temporary) / "w", output=Path(temporary) / "o",
            )

            def coordinator() -> None:
                raw = b""
                while not raw.endswith(b"\n"):
                    raw += parent.recv(4096)
                ready = json.loads(raw)
                release = {
                    "schema": target.RELEASE_SCHEMA,
                    "role": ready["role"], "worker_id": ready["worker_id"],
                    "process_id": ready["process_id"],
                    "process_start_token": ready["process_start_token"],
                    "control_channel_id": ready["control_channel_id"],
                    "nonce_commitment_sha256": ready["nonce_commitment_sha256"],
                    "handshake_sha256": digest("handshake"),
                    "worker_release_sha256": digest("release"),
                    "release_epoch": int(time.time()),
                }
                parent.sendall(target._wire_canonical_json(release))
                ack = b""
                while not ack.endswith(b"\n"):
                    ack += parent.recv(4096)

            thread = threading.Thread(target=coordinator, daemon=True)
            thread.start()
            try:
                session.announce_and_wait()
                session.acknowledge()
                thread.join(timeout=5.0)
                self.assertFalse(thread.is_alive())
            finally:
                session.close()
                parent.close()
                child.close()
        self.assertEqual(
            seen, [target.READY_SCHEMA, target.RELEASE_SCHEMA, target.ACK_SCHEMA],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
