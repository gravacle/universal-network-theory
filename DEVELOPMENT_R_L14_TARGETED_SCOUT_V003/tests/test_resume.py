#!/usr/bin/env python3

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRANCH_RUNNER = ROOT / "branch_runner.py"
KERNEL = ROOT / "tests" / "fixture_kernel.py"


def request_payload(run_id, repeat=1, sleep_seconds=0.0):
    return {
        "schema": "L14_SCOUT_PHASE_REQUEST_V002",
        "run_id": run_id,
        "length": 14,
        "phase": "bridge",
        "sectors": [4, 5, 6, 7],
        "mass_ledger_sectors": [4, 5, 6, 7, 8, 9],
        "branches": ["target", "hostile"],
        "geometry_history_sizes": [4, 6, 8, 10, 12, 14],
        "geometry_window": {"z": ["0.90", "1.10"], "y": ["0.90", "1.10"]},
        "fixture": {"repeat": repeat, "sleep_seconds": sleep_seconds},
    }


def command(request, checkpoint, output, resume=False):
    value = [
        sys.executable,
        "-B",
        str(BRANCH_RUNNER),
        "--branch",
        "target",
        "--phase",
        "bridge",
        "--request",
        str(request),
        "--kernel-module",
        str(KERNEL),
        "--checkpoint-root",
        str(checkpoint),
        "--output",
        str(output),
        "--workers",
        "2",
    ]
    if resume:
        value.append("--resume")
    return value


class ResumeTests(unittest.TestCase):
    def test_sigterm_resume_matches_uninterrupted_reduction(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            interrupted_request = root / "interrupted-request.json"
            interrupted_request.write_text(json.dumps(request_payload("fixture-resume", 6, 0.20)), encoding="utf-8")
            interrupted_checkpoint = root / "interrupted-checkpoint"
            interrupted_output = root / "interrupted-output.json"
            process = subprocess.Popen(
                command(interrupted_request, interrupted_checkpoint, interrupted_output),
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            deadline = time.monotonic() + 20.0
            committed = 0
            while time.monotonic() < deadline:
                committed = len(list((interrupted_checkpoint / "results").glob("*.json")))
                if committed >= 2:
                    break
                if process.poll() is not None:
                    break
                time.sleep(0.05)
            self.assertGreaterEqual(committed, 2)
            process.send_signal(signal.SIGTERM)
            first_output, _ = process.communicate(timeout=30.0)
            self.assertEqual(process.returncode, 75, first_output)
            after_stop = len(list((interrupted_checkpoint / "results").glob("*.json")))
            self.assertGreaterEqual(after_stop, committed)
            self.assertLess(after_stop, 24)
            self.assertFalse(interrupted_output.exists())

            resumed = subprocess.run(
                command(interrupted_request, interrupted_checkpoint, interrupted_output, resume=True),
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=60.0,
            )
            self.assertEqual(resumed.returncode, 0, resumed.stdout)
            self.assertTrue((interrupted_checkpoint / "COMPLETE.json").is_file())
            self.assertTrue((interrupted_checkpoint / "PREPARATION.json").is_file())

            clean_request = root / "clean-request.json"
            clean_request.write_text(json.dumps(request_payload("fixture-clean", 6, 0.0)), encoding="utf-8")
            clean_checkpoint = root / "clean-checkpoint"
            clean_output = root / "clean-output.json"
            clean = subprocess.run(
                command(clean_request, clean_checkpoint, clean_output),
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=60.0,
            )
            self.assertEqual(clean.returncode, 0, clean.stdout)
            interrupted = json.loads(interrupted_output.read_text(encoding="utf-8"))
            uninterrupted = json.loads(clean_output.read_text(encoding="utf-8"))
            for payload in (interrupted, uninterrupted):
                payload.pop("fixture_only", None)
            self.assertEqual(interrupted, uninterrupted)

    def test_resume_rejects_changed_task_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = root / "request.json"
            request.write_text(json.dumps(request_payload("identity-test", 1, 0.0)), encoding="utf-8")
            checkpoint = root / "checkpoint"
            output = root / "output.json"
            first = subprocess.run(command(request, checkpoint, output), cwd=str(ROOT), capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            changed = root / "changed.json"
            changed.write_text(json.dumps(request_payload("identity-test", 2, 0.0)), encoding="utf-8")
            retry = subprocess.run(command(changed, checkpoint, output, resume=True), cwd=str(ROOT), capture_output=True, text=True)
            self.assertNotEqual(retry.returncode, 0)
            refusal = retry.stdout + retry.stderr
            self.assertTrue(
                "resume identity mismatch" in refusal
                or "phase preparation identity mismatch" in refusal,
                refusal,
            )


if __name__ == "__main__":
    unittest.main()
