#!/usr/bin/env python3

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LaunchGateTests(unittest.TestCase):
    def test_paid_launch_is_disabled_in_checked_in_config(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(ROOT / "aws" / "launch_phase1.py"),
                "--config",
                str(ROOT / "AWS_RUN_CONFIG.example.json"),
                "--stack-name",
                "not-contacted",
                "--run-root",
                "/private/tmp/not-created",
                "--stack-input-evidence",
                "/private/tmp/not-contacted.json",
                "--run-id",
                "gate-test",
                "--attempt-id",
                "ATTEMPT1",
                "--authorize-paid-launch",
                "gate-test:ATTEMPT1",
            ],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("does not explicitly enable launch", completed.stdout)

    def test_source_bundle_refuses_unbound_kernels(self):
        with tempfile.TemporaryDirectory() as temporary:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "package_source.py"),
                    "--bindings",
                    str(ROOT / "KERNEL_BINDINGS.json"),
                    "--output",
                    str(Path(temporary) / "bundle.tar.gz"),
                    "--manifest",
                    str(Path(temporary) / "manifest.json"),
                ],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("not bound", completed.stdout)

    def test_stack_inputs_refuse_unbound_kernels(self):
        with tempfile.TemporaryDirectory() as temporary:
            fake_manifest = Path(temporary) / "manifest.json"
            fake_manifest.write_text("{}\n", encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "stack_parameters.py"),
                    "--bindings",
                    str(ROOT / "KERNEL_BINDINGS.json"),
                    "--source-manifest",
                    str(fake_manifest),
                    "--run-id",
                    "gate-test",
                    "--output",
                    str(Path(temporary) / "parameters.json"),
                    "--evidence",
                    str(Path(temporary) / "evidence.json"),
                ],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("exact kernels are not ready", completed.stdout)


if __name__ == "__main__":
    unittest.main()
