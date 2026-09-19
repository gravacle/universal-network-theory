#!/usr/bin/env python3
"""Hostile plan-only tests for the exact stored-publication successor."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import types
import unittest
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "stage3_a18_framing_compatibility.py"
SPEC = importlib.util.spec_from_file_location("stage3_a18_frame_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
compat = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = compat
SPEC.loader.exec_module(compat)


class StoredPublicationFramingCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = compat.stage3.frozen_runtime()
        self.stable = self.runtime.launcher.StableInput
        self.original_descriptor = self.stable.__dict__["open"]
        self.a18_raw = compat.PRODUCTION_A18_CONTRACT.path.read_bytes()
        self.a18_record = json.loads(self.a18_raw)
        self.target_raw = compat.PRODUCTION_TARGET_MANIFEST_CONTRACT.path.read_bytes()
        self.target_record = json.loads(self.target_raw)

    def tearDown(self) -> None:
        self.assertIs(self.stable.__dict__["open"], self.original_descriptor)

    def immutable(self, path: Path, raw: bytes) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        os.chmod(path, 0o444)
        return path

    def contract(self, path: Path, raw: bytes) -> object:
        return compat._PrettyInputContract(
            "A18 L10 cross gate fixture", path,
            hashlib.sha256(raw).hexdigest(),
            frozenset({compat.ADAPTER_A18_LABEL, compat.LAUNCHER_A18_LABEL}),
            "TARGET_V012_HOSTILE_V004R4_L10_CROSS_GATE_V001", "L", 10,
        )

    @contextmanager
    def isolated_open(self, contracts):
        """Test-only injection around the internal opener, never the CLI path."""
        original_descriptor = self.stable.__dict__["open"]
        original_open = self.stable.open
        capability = compat._PatchCapability()

        def opener(cls, label: str, path: Path, *, json_record: bool):
            return compat._open_from_registry(
                original_open, self.runtime, capability, contracts,
                label, path, json_record=json_record,
            )

        self.stable.open = classmethod(opener)
        try:
            yield
        finally:
            capability.active = False
            self.stable.open = original_descriptor

    def self_packet(self, packet: Path) -> tuple[dict[str, object], dict[str, bytes]]:
        packet.mkdir(parents=True)
        content = {
            compat.SELF_SOURCE_NAME: b"synthetic source\n",
            compat.SELF_TEST_NAME: b"synthetic test\n",
            compat.SELF_README_NAME: b"synthetic readme\n",
        }
        for name, raw in content.items():
            self.immutable(packet / name, raw)
        record = {
            "schema": compat.SELF_FREEZE_SCHEMA,
            "status": compat.SELF_FREEZE_STATUS,
            "files": {
                name: hashlib.sha256(raw).hexdigest()
                for name, raw in content.items()
            },
            "frozen_stage3_packet": compat.PINNED_STAGE3_PACKET,
            "pretty_input_registry": compat.EXPECTED_PRETTY_INPUT_REGISTRY,
            "claim_boundary": compat.SELF_CLAIM_BOUNDARY,
        }
        self.immutable(
            packet / compat.SELF_FREEZE_NAME,
            compat._compact_json_bytes(record),
        )
        return record, content

    def rewrite_freeze(self, packet: Path, record: dict[str, object]) -> None:
        path = packet / compat.SELF_FREEZE_NAME
        os.chmod(path, 0o644)
        path.write_bytes(compat._compact_json_bytes(record))
        os.chmod(path, 0o444)

    def test_frozen_compact_reader_refuses_current_pretty_a18(self) -> None:
        with self.assertRaisesRegex(
            self.runtime.launcher.LaunchRefusal, "not canonical JSON",
        ):
            self.stable.open(
                compat.ADAPTER_A18_LABEL,
                compat.PRODUCTION_A18_CONTRACT.path,
                json_record=True,
            )

    def test_exact_current_publication_frame_is_accepted_and_restored(self) -> None:
        with compat._patched_pretty_inputs_open():
            item = self.stable.open(
                compat.ADAPTER_A18_LABEL,
                compat.PRODUCTION_A18_CONTRACT.path,
                json_record=True,
            )
            try:
                self.assertEqual(item.digest, compat.EXPECTED_A18_SHA256)
                self.assertEqual(item.record, self.a18_record)
                item.verify()
            finally:
                item.close()
        self.assertIs(self.stable.__dict__["open"], self.original_descriptor)

    def test_non_a18_label_and_path_delegate_unchanged(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            base = Path(raw_dir).resolve()
            pretty = self.immutable(base / "A18.json", self.a18_raw)
            compact_raw = b'{"fixture":true}\n'
            other = self.immutable(base / "other.json", compact_raw)
            contract = self.contract(pretty, self.a18_raw)
            with self.isolated_open((contract,)):
                wrong_label = self.stable.open(
                    "wrong A18 label", other, json_record=True,
                )
                wrong_path = self.stable.open(
                    compat.ADAPTER_A18_LABEL, other, json_record=True,
                )
                try:
                    self.assertEqual(wrong_label.record, {"fixture": True})
                    self.assertEqual(wrong_path.record, {"fixture": True})
                finally:
                    wrong_label.close()
                    wrong_path.close()

    def test_reformat_and_compact_are_refused_after_hash_admission(self) -> None:
        variants = (
            json.dumps(self.a18_record, indent=4, sort_keys=True).encode("ascii") + b"\n",
            json.dumps(
                self.a18_record, sort_keys=True, separators=(",", ":"),
            ).encode("ascii") + b"\n",
            json.dumps(
                dict(reversed(tuple(self.a18_record.items()))), indent=2,
            ).encode("ascii") + b"\n",
            self.a18_raw[:-1] + b" \n",
        )
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            base = Path(raw_dir).resolve()
            for index, raw in enumerate(variants):
                path = self.immutable(base / f"variant-{index}.json", raw)
                with self.isolated_open((self.contract(path, raw),)):
                    with self.assertRaisesRegex(
                        compat.FramingRefusal, "publication framing",
                    ):
                        self.stable.open(
                            compat.ADAPTER_A18_LABEL, path, json_record=True,
                        )

    def test_duplicate_nonfinite_and_nonascii_are_refused(self) -> None:
        variants = (
            b'{"schema":"x","schema":"y"}\n',
            b'{"schema":"x","value":NaN}\n',
            b'{"schema":"x","value":"\xff"}\n',
        )
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            base = Path(raw_dir).resolve()
            for index, raw in enumerate(variants):
                path = self.immutable(base / f"attack-{index}.json", raw)
                with self.isolated_open((self.contract(path, raw),)):
                    with self.assertRaisesRegex(
                        compat.FramingRefusal, "strict ASCII JSON",
                    ):
                        self.stable.open(
                            compat.ADAPTER_A18_LABEL, path, json_record=True,
                        )

    def test_semantic_tamper_refuses_after_test_hash_admission(self) -> None:
        mutant = dict(self.a18_record)
        mutant["L"] = 11
        raw = compat._publication_json_bytes(mutant)
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            path = self.immutable(Path(raw_dir).resolve() / "tampered.json", raw)
            contract = self.contract(path, raw)
            with self.isolated_open((contract,)):
                with self.assertRaisesRegex(
                    compat.FramingRefusal, "identity semantics",
                ):
                    self.stable.open(
                        compat.ADAPTER_A18_LABEL, path, json_record=True,
                    )

    def test_wrong_exact_hash_refuses_and_closes_descriptors(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            path = self.immutable(Path(raw_dir).resolve() / "A18.json", self.a18_raw)
            contract = self.contract(path, self.a18_raw)
            contract = compat._PrettyInputContract(
                contract.name, contract.path, "0" * 64, contract.labels,
                contract.schema, contract.identity_field, contract.identity_value,
            )
            with self.isolated_open((contract,)):
                with self.assertRaisesRegex(compat.FramingRefusal, "hash mismatch"):
                    self.stable.open(
                        compat.ADAPTER_A18_LABEL, path, json_record=True,
                    )

    def test_retained_inode_swap_is_refused(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            path = self.immutable(Path(raw_dir).resolve() / "A18.json", self.a18_raw)
            contract = self.contract(path, self.a18_raw)
            with self.isolated_open((contract,)):
                item = self.stable.open(
                    compat.ADAPTER_A18_LABEL, path, json_record=True,
                )
                old = path.with_name("old-A18.json")
                path.rename(old)
                self.immutable(path, self.a18_raw)
                try:
                    with self.assertRaisesRegex(
                        self.runtime.launcher.LaunchRefusal, "retained input changed",
                    ):
                        item.verify()
                finally:
                    item.close()

    def test_retained_parent_swap_is_refused(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            base = Path(raw_dir).resolve()
            parent = base / "parent"
            path = self.immutable(parent / "A18.json", self.a18_raw)
            contract = self.contract(path, self.a18_raw)
            with self.isolated_open((contract,)):
                item = self.stable.open(
                    compat.ADAPTER_A18_LABEL, path, json_record=True,
                )
                old_parent = base / "old-parent"
                parent.rename(old_parent)
                parent.mkdir()
                try:
                    with self.assertRaisesRegex(
                        self.runtime.launcher.LaunchRefusal, "retained input changed",
                    ):
                        item.verify()
                finally:
                    item.close()

    def test_launcher_label_is_separately_exact(self) -> None:
        with compat._patched_pretty_inputs_open():
            item = self.stable.open(
                compat.LAUNCHER_A18_LABEL,
                compat.PRODUCTION_A18_CONTRACT.path,
                json_record=True,
            )
            try:
                self.assertEqual(item.digest, compat.EXPECTED_A18_SHA256)
            finally:
                item.close()

    def test_global_is_restored_on_body_failure(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "injected"):
            with compat._patched_pretty_inputs_open():
                raise RuntimeError("injected compatibility-scope failure")
        self.assertIs(self.stable.__dict__["open"], self.original_descriptor)

    def test_leaked_bound_compatible_open_refuses_after_scope_exit(self) -> None:
        leaked = None
        with compat._patched_pretty_inputs_open():
            leaked = self.stable.open
            item = leaked(
                compat.ADAPTER_A18_LABEL,
                compat.PRODUCTION_A18_CONTRACT.path,
                json_record=True,
            )
            item.close()
        assert leaked is not None
        with self.assertRaisesRegex(compat.FramingRefusal, "capability is inactive"):
            leaked(
                compat.ADAPTER_A18_LABEL,
                compat.PRODUCTION_A18_CONTRACT.path,
                json_record=True,
            )

    def test_nested_patch_scope_refuses_without_disabling_outer_scope(self) -> None:
        with compat._patched_pretty_inputs_open():
            with self.assertRaisesRegex(compat.FramingRefusal, "occupied or nested"):
                with compat._patched_pretty_inputs_open():
                    self.fail("nested compatibility scope entered")
            item = self.stable.open(
                compat.ADAPTER_A18_LABEL,
                compat.PRODUCTION_A18_CONTRACT.path,
                json_record=True,
            )
            item.close()

    def test_reentrant_internal_open_refuses(self) -> None:
        capability = compat._PatchCapability()

        def recursive(label: str, path: Path, *, json_record: bool):
            return compat._open_from_registry(
                recursive, self.runtime, capability, (),
                label, path, json_record=json_record,
            )

        with self.assertRaisesRegex(compat.FramingRefusal, "reentrant"):
            recursive("unregistered", HERE / "absent.json", json_record=False)

    def test_occupied_stable_open_refuses_without_overwrite(self) -> None:
        occupied = classmethod(lambda cls, *args, **kwargs: None)
        self.stable.open = occupied
        try:
            with self.assertRaisesRegex(compat.FramingRefusal, "occupied or nested"):
                with compat._patched_pretty_inputs_open():
                    self.fail("occupied StableInput.open was overwritten")
            self.assertIs(self.stable.__dict__["open"], occupied)
        finally:
            self.stable.open = self.original_descriptor

    def test_arbitrary_pretty_a01_does_not_enter_production_registry(self) -> None:
        raw = compat._publication_json_bytes({"schema": "A01_ARBITRARY_PRETTY"})
        with tempfile.TemporaryDirectory(prefix="a01-pretty-", dir=HERE) as raw_dir:
            path = self.immutable(Path(raw_dir).resolve() / "A01.json", raw)
            with compat._patched_pretty_inputs_open():
                with self.assertRaisesRegex(
                    self.runtime.launcher.LaunchRefusal, "not canonical JSON",
                ):
                    self.stable.open(
                        "A01 freeze and source packet", path, json_record=True,
                    )

    def test_exact_target_manifest_publication_frame_is_accepted(self) -> None:
        with self.assertRaisesRegex(
            self.runtime.launcher.LaunchRefusal, "not canonical JSON",
        ):
            self.stable.open(
                compat.ADAPTER_TARGET_MANIFEST_LABEL,
                compat.PRODUCTION_TARGET_MANIFEST_CONTRACT.path,
                json_record=True,
            )
        with compat._patched_pretty_inputs_open():
            item = self.stable.open(
                compat.ADAPTER_TARGET_MANIFEST_LABEL,
                compat.PRODUCTION_TARGET_MANIFEST_CONTRACT.path,
                json_record=True,
            )
            try:
                self.assertEqual(item.digest, compat.EXPECTED_TARGET_MANIFEST_SHA256)
                self.assertEqual(item.record, self.target_record)
                item.verify()
            finally:
                item.close()

    def test_cross_artifact_label_and_path_do_not_enter_compatibility(self) -> None:
        with compat._patched_pretty_inputs_open():
            for label, path in (
                (
                    compat.ADAPTER_A18_LABEL,
                    compat.PRODUCTION_TARGET_MANIFEST_CONTRACT.path,
                ),
                (
                    compat.ADAPTER_TARGET_MANIFEST_LABEL,
                    compat.PRODUCTION_A18_CONTRACT.path,
                ),
            ):
                with self.assertRaisesRegex(
                    self.runtime.launcher.LaunchRefusal, "not canonical JSON",
                ):
                    self.stable.open(label, path, json_record=True)

    def test_writable_hardlinked_and_symlinked_registered_inputs_refuse(self) -> None:
        with tempfile.TemporaryDirectory(prefix="a18-frame-", dir=HERE) as raw_dir:
            base = Path(raw_dir).resolve()
            writable = base / "writable.json"
            writable.write_bytes(self.a18_raw)
            writable_contract = self.contract(writable, self.a18_raw)
            hardlinked = self.immutable(base / "hardlinked.json", self.a18_raw)
            os.link(hardlinked, base / "second-link.json")
            hardlink_contract = self.contract(hardlinked, self.a18_raw)
            symlink = base / "symlink.json"
            symlink.symlink_to(compat.PRODUCTION_A18_CONTRACT.path)
            symlink_contract = self.contract(symlink, self.a18_raw)
            for contract in (writable_contract, hardlink_contract, symlink_contract):
                with self.isolated_open((contract,)):
                    with self.assertRaises(self.runtime.launcher.LaunchRefusal):
                        self.stable.open(
                            compat.ADAPTER_A18_LABEL,
                            contract.path,
                            json_record=True,
                        )

    def test_adapter_and_launcher_call_sites_reach_both_registered_inputs(self) -> None:
        def exercise(a18_label: str, target_label: str) -> dict[str, object]:
            opened = []
            try:
                for label, contract in (
                    (a18_label, compat.PRODUCTION_A18_CONTRACT),
                    (target_label, compat.PRODUCTION_TARGET_MANIFEST_CONTRACT),
                ):
                    opened.append(self.stable.open(
                        label, contract.path, json_record=True,
                    ))
                return {item.label: item.digest for item in opened}
            finally:
                for item in opened:
                    item.close()

        original_prepare = compat.stage3.prepare_production
        original_launch = compat.stage3.launch_authenticated_l12
        try:
            compat.stage3.prepare_production = lambda *, publish: exercise(
                compat.ADAPTER_A18_LABEL, compat.ADAPTER_TARGET_MANIFEST_LABEL,
            )
            compat.stage3.launch_authenticated_l12 = lambda: exercise(
                compat.LAUNCHER_A18_LABEL, compat.LAUNCHER_TARGET_MANIFEST_LABEL,
            )
            prepared = compat.prepare_production(publish=False)
            launched = compat.launch_authenticated_l12()
        finally:
            compat.stage3.prepare_production = original_prepare
            compat.stage3.launch_authenticated_l12 = original_launch
        self.assertEqual(
            prepared[compat.ADAPTER_A18_LABEL], compat.EXPECTED_A18_SHA256,
        )
        self.assertEqual(
            prepared[compat.ADAPTER_TARGET_MANIFEST_LABEL],
            compat.EXPECTED_TARGET_MANIFEST_SHA256,
        )
        self.assertEqual(
            launched[compat.LAUNCHER_A18_LABEL], compat.EXPECTED_A18_SHA256,
        )
        self.assertEqual(
            launched[compat.LAUNCHER_TARGET_MANIFEST_LABEL],
            compat.EXPECTED_TARGET_MANIFEST_SHA256,
        )
        self.assertIs(self.stable.__dict__["open"], self.original_descriptor)

    def test_frozen_dry_run_input_call_site_reaches_registry(self) -> None:
        with compat._patched_pretty_inputs_open():
            inputs = compat.stage3._open_production_inputs()
            try:
                by_label = {item.label: item for item in inputs}
                self.assertEqual(
                    by_label[compat.ADAPTER_A18_LABEL].digest,
                    compat.EXPECTED_A18_SHA256,
                )
                self.assertEqual(
                    by_label[compat.ADAPTER_TARGET_MANIFEST_LABEL].digest,
                    compat.EXPECTED_TARGET_MANIFEST_SHA256,
                )
            finally:
                compat.stage3._close_inputs(inputs)

    def test_frozen_launcher_call_site_reaches_registry_before_sentinel(self) -> None:
        class Sentinel(RuntimeError):
            pass

        class Dummy:
            def __init__(self, label: str, path: Path) -> None:
                self.label = label
                self.path = path
                self.digest = "1" * 64
                self.record = {}

            def verify(self) -> None:
                pass

            def close(self) -> None:
                pass

        seen: list[tuple[str, Path, bool]] = []
        original_descriptor = self.stable.__dict__["open"]
        original_bound = self.stable.open

        def intercept(cls, label: str, path: Path, *, json_record: bool):
            seen.append((label, path, json_record))
            if path in {
                compat.PRODUCTION_A18_CONTRACT.path,
                compat.PRODUCTION_TARGET_MANIFEST_CONTRACT.path,
            }:
                return original_bound(label, path, json_record=json_record)
            if label == "hostile cache manifest":
                raise Sentinel("stop before coordinator or worker action")
            return Dummy(label, path)

        intercept_descriptor = classmethod(intercept)
        prior_frozen_descriptor = compat.FROZEN_STABLE_OPEN_DESCRIPTOR
        setattr(self.stable, "open", intercept_descriptor)
        compat.FROZEN_STABLE_OPEN_DESCRIPTOR = intercept_descriptor
        try:
            with self.assertRaisesRegex(Sentinel, "before coordinator"):
                compat.launch_authenticated_l12()
        finally:
            compat.FROZEN_STABLE_OPEN_DESCRIPTOR = prior_frozen_descriptor
            setattr(self.stable, "open", original_descriptor)
        self.assertIn(
            (
                compat.LAUNCHER_A18_LABEL,
                compat.PRODUCTION_A18_CONTRACT.path,
                False,
            ),
            seen,
        )
        self.assertIn(
            (
                compat.LAUNCHER_TARGET_MANIFEST_LABEL,
                compat.PRODUCTION_TARGET_MANIFEST_CONTRACT.path,
                False,
            ),
            seen,
        )

    def test_cli_dispatches_exact_modes_without_real_actions(self) -> None:
        calls: list[tuple[str, object]] = []

        def fake_plan() -> dict[str, object]:
            calls.append(("plan", None))
            return {"mode": "plan"}

        def fake_prepare(*, publish: bool) -> dict[str, object]:
            calls.append(("prepare", publish))
            return {"mode": "publish" if publish else "dry-run"}

        def fake_launch() -> dict[str, object]:
            calls.append(("launch", None))
            return {"mode": "launch"}

        with (
            mock.patch.object(compat, "plan", fake_plan),
            mock.patch.object(compat, "prepare_production", fake_prepare),
            mock.patch.object(compat, "launch_authenticated_l12", fake_launch),
        ):
            for mode in ("plan", "dry-run", "publish", "launch"):
                with mock.patch.object(compat.sys, "argv", [str(SOURCE), mode]):
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.assertEqual(compat.main(), 0)
                    self.assertEqual(json.loads(output.getvalue())["mode"], mode)
        self.assertEqual(calls, [
            ("plan", None), ("prepare", False),
            ("prepare", True), ("launch", None),
        ])

    def test_cli_invalid_modes_refuse_without_dispatch(self) -> None:
        for argv in (
            [str(SOURCE)], [str(SOURCE), "fixture"],
            [str(SOURCE), "dry-run", "extra"],
        ):
            error = io.StringIO()
            with mock.patch.object(compat.sys, "argv", argv), redirect_stderr(error):
                self.assertEqual(compat.main(), 2)
            self.assertIn("exact mode", error.getvalue())

    def test_self_freeze_fixture_authenticates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="self-freeze-", dir=HERE) as raw_dir:
            packet = Path(raw_dir).resolve() / "packet"
            record, _content = self.self_packet(packet)
            self.assertEqual(compat._authenticate_self_packet_at(packet), record)

    def test_self_freeze_source_and_test_drift_refuse(self) -> None:
        for name in (compat.SELF_SOURCE_NAME, compat.SELF_TEST_NAME):
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="self-freeze-", dir=HERE,
            ) as raw_dir:
                packet = Path(raw_dir).resolve() / "packet"
                self.self_packet(packet)
                path = packet / name
                os.chmod(path, 0o644)
                path.write_bytes(b"drifted bytes\n")
                os.chmod(path, 0o444)
                with self.assertRaisesRegex(compat.FramingRefusal, "digest mismatch"):
                    compat._authenticate_self_packet_at(packet)

    def test_self_freeze_missing_and_extra_manifest_members_refuse(self) -> None:
        for mode in ("missing", "extra"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(
                prefix="self-freeze-", dir=HERE,
            ) as raw_dir:
                packet = Path(raw_dir).resolve() / "packet"
                record, _content = self.self_packet(packet)
                files = dict(record["files"])
                if mode == "missing":
                    files.pop(compat.SELF_TEST_NAME)
                else:
                    files["unregistered.py"] = "0" * 64
                record["files"] = files
                self.rewrite_freeze(packet, record)
                with self.assertRaisesRegex(compat.FramingRefusal, "member census"):
                    compat._authenticate_self_packet_at(packet)

    def test_self_freeze_writable_hardlink_and_symlink_cases_refuse(self) -> None:
        for target_name in (compat.SELF_FREEZE_NAME, compat.SELF_SOURCE_NAME):
            for mutation in ("writable", "hardlink", "symlink"):
                with self.subTest(target=target_name, mutation=mutation), \
                     tempfile.TemporaryDirectory(
                         prefix="self-freeze-", dir=HERE,
                     ) as raw_dir:
                    packet = Path(raw_dir).resolve() / "packet"
                    self.self_packet(packet)
                    target = packet / target_name
                    if mutation == "writable":
                        os.chmod(target, 0o644)
                    elif mutation == "hardlink":
                        os.link(target, packet / f"linked-{target_name}")
                    else:
                        target.unlink()
                        target.symlink_to(packet / compat.SELF_README_NAME)
                    with self.assertRaises(compat.FramingRefusal):
                        compat._authenticate_self_packet_at(packet)

    def test_forged_matching_stage3_module_alias_is_never_trusted(self) -> None:
        prior = sys.modules.get(compat.STAGE3_MODULE_NAME)
        forged = types.ModuleType(compat.STAGE3_MODULE_NAME)
        forged.__file__ = str(compat.STAGE3_ADAPTER)
        forged.__authenticated_sha256__ = compat.PINNED_STAGE3_PACKET[
            compat.STAGE3_ADAPTER.name
        ]
        forged.used = False

        def forged_runtime():
            forged.used = True
            raise AssertionError("forged module was trusted")

        forged.frozen_runtime = forged_runtime
        sys.modules[compat.STAGE3_MODULE_NAME] = forged
        try:
            loaded = compat._load_stage3()
            self.assertIsNot(loaded, forged)
            self.assertFalse(forged.used)
            self.assertIs(sys.modules[compat.STAGE3_MODULE_NAME], loaded)
            self.assertIs(loaded.frozen_runtime(), loaded._RUNTIME)
        finally:
            if prior is None:
                sys.modules.pop(compat.STAGE3_MODULE_NAME, None)
            else:
                sys.modules[compat.STAGE3_MODULE_NAME] = prior

    def test_occupied_stage3_alias_is_replaced_by_fresh_authenticated_module(self) -> None:
        prior = sys.modules.get(compat.STAGE3_MODULE_NAME)
        occupied = types.ModuleType(compat.STAGE3_MODULE_NAME)
        occupied.marker = "untrusted occupied alias"
        sys.modules[compat.STAGE3_MODULE_NAME] = occupied
        try:
            loaded = compat._load_stage3()
            self.assertIsNot(loaded, occupied)
            self.assertIs(sys.modules[compat.STAGE3_MODULE_NAME], loaded)
            self.assertEqual(
                loaded.__authenticated_sha256__,
                compat.PINNED_STAGE3_PACKET[compat.STAGE3_ADAPTER.name],
            )
        finally:
            if prior is None:
                sys.modules.pop(compat.STAGE3_MODULE_NAME, None)
            else:
                sys.modules[compat.STAGE3_MODULE_NAME] = prior

    def test_stage3_load_failure_restores_occupied_alias(self) -> None:
        prior = sys.modules.get(compat.STAGE3_MODULE_NAME)
        occupied = types.ModuleType(compat.STAGE3_MODULE_NAME)
        sys.modules[compat.STAGE3_MODULE_NAME] = occupied
        try:
            with mock.patch.object(
                compat, "compile", side_effect=RuntimeError("injected compile"),
                create=True,
            ):
                with self.assertRaisesRegex(RuntimeError, "injected compile"):
                    compat._load_stage3()
            self.assertIs(sys.modules[compat.STAGE3_MODULE_NAME], occupied)
        finally:
            if prior is None:
                sys.modules.pop(compat.STAGE3_MODULE_NAME, None)
            else:
                sys.modules[compat.STAGE3_MODULE_NAME] = prior

    def test_stage3_load_failure_removes_fresh_alias_when_unoccupied(self) -> None:
        prior = sys.modules.pop(compat.STAGE3_MODULE_NAME, None)
        try:
            with mock.patch.object(
                compat, "compile", side_effect=RuntimeError("injected compile"),
                create=True,
            ):
                with self.assertRaisesRegex(RuntimeError, "injected compile"):
                    compat._load_stage3()
            self.assertNotIn(compat.STAGE3_MODULE_NAME, sys.modules)
        finally:
            if prior is not None:
                sys.modules[compat.STAGE3_MODULE_NAME] = prior

    def test_plan_is_read_only_and_restores_global(self) -> None:
        watched = (
            *compat.stage3.OUTPUT_PATHS,
            compat.stage3.TARGET_WORKSPACE, compat.stage3.HOSTILE_WORKSPACE,
            compat.stage3.TARGET_OUTPUT, compat.stage3.HOSTILE_OUTPUT,
            compat.stage3.TELEMETRY,
        )
        before = {path: os.path.lexists(path) for path in watched}
        result = compat.plan()
        after = {path: os.path.lexists(path) for path in watched}
        self.assertEqual(before, after)
        self.assertEqual(
            result["classification"],
            "PASS_MUTABLE_PLAN_ONLY_EXACT_STORED_PUBLICATION_FRAME_COMPATIBILITY",
        )
        self.assertFalse(result["published"])
        self.assertFalse(result["launched"])
        self.assertIs(self.stable.__dict__["open"], self.original_descriptor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
