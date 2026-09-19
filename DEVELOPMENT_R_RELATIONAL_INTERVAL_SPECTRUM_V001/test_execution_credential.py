#!/usr/bin/env python3
"""No-solver hostile tests for target interval execution admission."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


control = load_module("execution_credential_tested", HERE / "execution_credential.py")
worker = load_module("target_interval_worker_tested", HERE / "target_interval_worker.py")
driver = load_module("interval_spectrum_driver_tested", HERE / "interval_spectrum_driver.py")


class ReachedWorker(RuntimeError):
    pass


class DummyEngine:
    TARGET_ROWS: dict[int, tuple[int, ...]] = {}

    @staticmethod
    def worker(length: int, charge: int, output: Path) -> None:
        raise ReachedWorker(f"REACHED_WORKER_L{length}_Q{charge}")


class ExecutionCredentialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="credential_test_", dir=HERE))
        self.paths: dict[str, Path] = {}

        def raw_file(label: str, relative: str, raw: bytes) -> Path:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            os.chmod(path, 0o444)
            self.paths[label] = path
            return path

        def json_file(label: str, relative: str, value: object) -> Path:
            return raw_file(
                label,
                relative,
                (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            )

        manifest = json_file(
            "manifest",
            "sector/MANIFEST.json",
            {
                "schema": control.MANIFEST_SCHEMA,
                "status": control.MANIFEST_STATUS,
            },
        )
        manifest_sha = control.sha256_file(manifest)
        plan = json_file(
            "sector_plan",
            "blind/SECTOR_PLAN.json",
            {
                "schema": control.PLAN_SCHEMA,
                "status": control.PLAN_STATUS,
                "manifest_sha256": manifest_sha,
                "planned_sectors": [[10, 1], [10, 2]],
            },
        )
        blind_worker = raw_file(
            "blind_worker", "blind/blind_interval_worker.py", b"# frozen blind worker\n",
        )
        blind_worker_sha = control.sha256_file(blind_worker)
        source_freeze = json_file(
            "blind_source_freeze",
            "blind/SOURCE_FREEZE.json",
            {
                "schema": control.SOURCE_FREEZE_SCHEMA,
                "status": control.SOURCE_FREEZE_STATUS,
                "physical_spectrum_executed": False,
                "files": {"blind_interval_worker.py": blind_worker_sha},
            },
        )
        blind_freeze = json_file(
            "blind_method_freeze",
            "blind/BLIND_FREEZE.json",
            {
                "schema": control.BLIND_FREEZE_SCHEMA,
                "status": control.BLIND_FREEZE_STATUS,
                "manifest_sha256": manifest_sha,
                "planned_sectors": [[10, 1], [10, 2]],
                "sector_plan_path": plan.relative_to(self.root).as_posix(),
                "sector_plan_sha256": control.sha256_file(plan),
                "source_freeze_path": source_freeze.relative_to(self.root).as_posix(),
                "source_freeze_sha256": control.sha256_file(source_freeze),
                "implementation_path": blind_worker.relative_to(self.root).as_posix(),
                "implementation_sha256": blind_worker_sha,
                "target_code_or_matrices_imported": False,
                "physical_spectrum_executed_at_freeze": False,
            },
        )
        target_driver = raw_file("target_driver", "target/interval_spectrum_driver.py", b"# driver\n")
        target_worker = raw_file("target_worker", "target/target_interval_worker.py", b"# worker\n")
        target_engine = raw_file("target_engine", "target/compute_phase_screen.py", b"# engine\n")
        credential_source = raw_file("credential_control", "target/execution_credential.py", b"# credential\n")
        target_freeze = json_file(
            "target_source_freeze",
            "target/FREEZE.json",
            {
                "schema": control.TARGET_FREEZE_SCHEMA,
                "status": control.TARGET_FREEZE_STATUS,
                "physical_spectrum_outputs_present_at_freeze": False,
                "files": {
                    target_driver.relative_to(self.root).as_posix(): control.sha256_file(target_driver),
                    target_worker.relative_to(self.root).as_posix(): control.sha256_file(target_worker),
                    credential_source.relative_to(self.root).as_posix(): control.sha256_file(credential_source),
                },
            },
        )
        self.authorities = {
            label: self.paths[label]
            for label in (
                "manifest", "sector_plan", "blind_method_freeze",
                "blind_source_freeze", "target_source_freeze",
                "target_driver", "target_worker", "target_engine",
                "credential_control",
            )
        }
        self.expected = {
            "worker": (target_worker, control.sha256_file(target_worker)),
            "driver": (target_driver, control.sha256_file(target_driver)),
            "engine": (target_engine, control.sha256_file(target_engine)),
            "control": (credential_source, control.sha256_file(credential_source)),
            "target_freeze": (target_freeze, control.sha256_file(target_freeze)),
        }
        self.output = self.root / "target" / "RAW" / "SECTOR_L10_Q1.json"
        self.output.parent.mkdir()
        self.credential = self.root / "target" / "AUTHORIZATION" / "SECTOR_L10_Q1.json"
        self.credential.parent.mkdir()
        self.digest = control.issue_execution_credential(
            self.root,
            self.credential,
            10,
            1,
            self.output,
            self.authorities,
            self.expected["worker"],
            self.expected["driver"],
            self.expected["engine"],
            self.expected["control"],
            self.expected["target_freeze"],
            worker.EXECUTION_TOKEN,
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.root)

    def dispatch(self, *, credential: Path | None = None, digest: str | None = None,
                 charge: int = 1, output: Path | None = None) -> None:
        worker.run_physical(
            10,
            charge,
            self.credential if credential is None else credential,
            self.digest if digest is None else digest,
            self.output if output is None else output,
            repo_root=self.root,
            expectations=self.expected,
            engine_loader=lambda: DummyEngine,
        )

    def test_valid_exact_credential_reaches_monkeypatched_worker(self) -> None:
        with self.assertRaisesRegex(ReachedWorker, "REACHED_WORKER_L10_Q1"):
            self.dispatch()
        self.assertFalse(self.output.exists())

    def test_missing_credential_refuses_before_worker(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "credential refused"):
            self.dispatch(credential=self.root / "absent.json")
        self.assertFalse(self.output.exists())

    def test_direct_cli_without_credential_refuses_without_output(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(HERE / "target_interval_worker.py"),
                "--L", "10",
                "--q", "1",
                "--output", str(self.output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("credential", completed.stderr)
        self.assertFalse(self.output.exists())

    def test_wrong_credential_digest_refuses_before_worker(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "SHA-256 mismatch"):
            self.dispatch(digest="0" * 64)
        self.assertFalse(self.output.exists())

    def test_swapped_sector_credential_refuses_before_worker(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "credential q binding"):
            self.dispatch(charge=2)
        self.assertFalse(self.output.exists())

    def test_swapped_output_credential_refuses_before_worker(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "credential output binding"):
            self.dispatch(output=self.output.with_name("SECTOR_L10_Q2.json"))
        self.assertFalse(self.output.exists())

    def test_stale_plan_identity_refuses_before_worker(self) -> None:
        plan = self.paths["sector_plan"]
        os.chmod(plan, 0o644)
        plan.write_bytes(plan.read_bytes() + b" ")
        os.chmod(plan, 0o444)
        with self.assertRaisesRegex(RuntimeError, "inode/hash identity mismatch"):
            self.dispatch()
        self.assertFalse(self.output.exists())

    def test_authority_name_swap_during_retained_read_refuses(self) -> None:
        path = self.paths["sector_plan"]
        binding = control.file_binding(self.root, path, "sector plan")
        replacement = path.with_name("replacement-plan.json")
        replacement.write_bytes(path.read_bytes() + b" ")
        os.chmod(replacement, 0o444)
        moved = path.with_name("moved-plan.json")
        original_read = os.read
        swapped = False

        def swap_then_read(descriptor: int, count: int) -> bytes:
            nonlocal swapped
            if not swapped:
                swapped = True
                path.rename(moved)
                replacement.rename(path)
            return original_read(descriptor, count)

        with mock.patch.object(control.os, "read", side_effect=swap_then_read):
            with self.assertRaisesRegex(
                control.CredentialRefusal, "changed or name-swapped while read",
            ):
                control.checked_binding(self.root, binding, "sector plan")
        self.assertTrue(swapped)

    def test_credential_name_swap_during_retained_read_refuses(self) -> None:
        replacement = self.credential.with_name("replacement-credential.json")
        replacement.write_bytes(self.credential.read_bytes() + b" ")
        os.chmod(replacement, 0o444)
        moved = self.credential.with_name("moved-credential.json")
        original_read = os.read
        swapped = False

        def swap_then_read(descriptor: int, count: int) -> bytes:
            nonlocal swapped
            if not swapped:
                swapped = True
                self.credential.rename(moved)
                replacement.rename(self.credential)
            return original_read(descriptor, count)

        with mock.patch.object(control.os, "read", side_effect=swap_then_read):
            with self.assertRaisesRegex(
                control.CredentialRefusal, "changed or name-swapped while read",
            ):
                control.validate_execution_credential(
                    self.root,
                    self.credential,
                    self.digest,
                    10,
                    1,
                    self.output,
                    self.expected["worker"],
                    self.expected["driver"],
                    self.expected["engine"],
                    self.expected["control"],
                    self.expected["target_freeze"],
                    worker.EXECUTION_TOKEN,
                )
        self.assertTrue(swapped)

    def test_credential_custody_and_claim_boundary(self) -> None:
        metadata = self.credential.stat()
        self.assertEqual(metadata.st_nlink, 1)
        self.assertEqual(metadata.st_mode & 0o777, 0o444)
        record = json.loads(self.credential.read_text())
        self.assertEqual(record["ordering_model"], control.ORDERING_MODEL)
        self.assertIn("NO_ADVERSARY_RESISTANT_WALL_CLOCK_ATTESTATION", record["claim_boundary"])
        self.assertEqual(self.digest, hashlib.sha256(self.credential.read_bytes()).hexdigest())

    def test_postworker_and_index_binding_helper_revalidates_credential(self) -> None:
        binding = control.validate_execution_credential(
            self.root,
            self.credential,
            self.digest,
            10,
            1,
            self.output,
            self.expected["worker"],
            self.expected["driver"],
            self.expected["engine"],
            self.expected["control"],
            self.expected["target_freeze"],
            worker.EXECUTION_TOKEN,
        )
        saved_root = driver.ROOT
        saved_loader = driver.load_credential_control
        saved_expectations = driver.credential_expectations
        try:
            driver.ROOT = self.root
            driver.load_credential_control = lambda: control
            driver.credential_expectations = lambda: self.expected
            driver.validate_target_execution_binding(
                {"execution_authorization": binding},
                (10, 1),
                self.output,
                self.credential,
                self.digest,
            )
            altered = json.loads(json.dumps(binding))
            altered["authorization_nonce"] = "0" * 64
            with self.assertRaisesRegex(driver.FailClosed, "row execution-authorization binding"):
                driver.validate_target_execution_binding(
                    {"execution_authorization": altered},
                    (10, 1),
                    self.output,
                    self.credential,
                    self.digest,
                )
        finally:
            driver.ROOT = saved_root
            driver.load_credential_control = saved_loader
            driver.credential_expectations = saved_expectations


if __name__ == "__main__":
    unittest.main(verbosity=2)
