#!/usr/bin/env python3
"""Copied-checkpoint fault injection and real-signal tests for V002 custody."""

from __future__ import annotations

import argparse
import copy
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any

import hardened_runtime as hard
from last_task_signal_worker import fixture_pool


PACKET = Path(__file__).resolve().parent
SEALED_R3 = PACKET / "CHECKPOINTS" / "L4_EVENT00_TARGET_V002R3"
FIXTURE_WORKER = PACKET / "last_task_signal_worker.py"


def scientific(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("resource")
    return result


def write_json(path: Path, value: Any) -> None:
    # Published checkpoint files are read-only; fault injection touches only
    # private copies and deliberately removes that filesystem protection.
    if path.exists():
        path.chmod(0o600)
    path.write_bytes(hard.durable.canonical_json_bytes(value))


def last_journal_path(root: Path) -> Path:
    return sorted((root / "journal").glob("*.json"))[-1]


def verified_pool(root: Path) -> hard.HardenedPool:
    pool = hard.make_l4_pool(root)
    pool.bind_identity(resume=True)
    pool.verify_complete()
    return pool


class HardenedRuntimeTests(unittest.TestCase):
    sealed_checkpoint = SEALED_R3
    fresh_baseline = False

    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline_scratch = None
        if cls.fresh_baseline:
            cls.baseline_scratch = tempfile.TemporaryDirectory(prefix="unt-v002-baseline-")
            cls.sealed_checkpoint = Path(cls.baseline_scratch.name) / "checkpoint"
            outcome = hard.make_l4_pool(cls.sealed_checkpoint).run(resume=False)
            if outcome.status != "COMPLETE":
                raise RuntimeError(f"fresh baseline did not complete: {outcome.status}")
        if not cls.sealed_checkpoint.is_dir():
            raise RuntimeError(f"missing sealed checkpoint: {cls.sealed_checkpoint}")
        cls.sealed = verified_pool(cls.sealed_checkpoint)
        cls.reference = {
            task.task_id: scientific(cls.sealed.load_completed()[task.task_id])
            for task in cls.sealed.tasks
        }

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.baseline_scratch is not None:
            cls.baseline_scratch.cleanup()

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(prefix="unt-v002-fault-")
        self.root = Path(self.scratch.name) / "checkpoint"
        shutil.copytree(self.sealed_checkpoint, self.root)

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def assert_science_matches_reference(self, pool: hard.HardenedPool) -> None:
        observed = pool.load_completed()
        self.assertEqual(set(observed), set(self.reference))
        for task_id, expected in self.reference.items():
            self.assertEqual(scientific(observed[task_id]), expected, task_id)

    def assert_refused(self, root: Path | None = None) -> None:
        checkpoint = root or self.root
        with self.assertRaises((hard.durable.EvidenceError, hard.target.ScalingError, RuntimeError, ValueError)):
            verified_pool(checkpoint)

    def test_00_unmodified_copy_is_verifiable(self) -> None:
        self.assert_science_matches_reference(verified_pool(self.root))

    def test_01_outer_metadata_mutation_refused(self) -> None:
        path = self.root / "results" / "L04_event00_qout00.json"
        body = hard.target.load_json(path)
        body["work_units"] += 1
        write_json(path, body)
        self.assert_refused()

    def test_02_sector_numeric_mutation_refused(self) -> None:
        path = self.root / "results" / "L04_event00_qout00.json"
        body = hard.target.load_json(path)
        body["result"]["after_admission"]["carrier_trace_distance"] += 0.001
        write_json(path, body)
        self.assert_refused()

    def test_03_task_binding_mutation_refused(self) -> None:
        path = self.root / "results" / "L04_event00_qout00.json"
        body = hard.target.load_json(path)
        body["result"]["task_binding"]["kernel_sha256"] = "0" * 64
        write_json(path, body)
        self.assert_refused()

    def test_04_receipt_mutation_refused(self) -> None:
        path = self.root / "receipts" / "L04_event00_qout00.json"
        receipt = hard.target.load_json(path)
        receipt["scientific_sha256"] = "0" * 64
        write_json(path, receipt)
        self.assert_refused()

    def test_05_identity_mutation_refused(self) -> None:
        path = self.root / "RUN_IDENTITY.json"
        identity = hard.target.load_json(path)
        identity["parameters"]["authorized_lengths"] = [4, 6]
        write_json(path, identity)
        self.assert_refused()

    def test_06_complete_mutation_refused(self) -> None:
        path = self.root / "COMPLETE.json"
        complete = hard.target.load_json(path)
        complete["result_files"][0]["sha256"] = "0" * 64
        write_json(path, complete)
        self.assert_refused()

    def test_07_journal_mutation_refused(self) -> None:
        path = self.root / "journal" / "00000003__TASK_COMMITTED.json"
        event = hard.target.load_json(path)
        event["payload"]["result_sha256"] = "0" * 64
        write_json(path, event)
        self.assert_refused()

    def test_08_duplicate_json_key_refused(self) -> None:
        path = self.root / "results" / "L04_event00_qout00.json"
        path.chmod(0o600)
        path.write_bytes(b'{"schema":"A","schema":"B"}\n')
        self.assert_refused()

    def test_09_unexpected_result_file_refused(self) -> None:
        path = self.root / "results" / "unplanned.json"
        path.write_bytes(b"{}\n")
        self.assert_refused()

    def test_10_missing_run_bound_recovered(self) -> None:
        # Identity was published, then the process died before RUN_BOUND.
        (self.root / "COMPLETE.json").unlink()
        for folder_name in ("journal", "results", "receipts"):
            for path in (self.root / folder_name).glob("*.json"):
                path.unlink()
        pool = hard.make_l4_pool(self.root)
        outcome = pool.run(resume=True)
        self.assertEqual(outcome.status, "COMPLETE")
        pool.verify_complete()
        self.assert_science_matches_reference(pool)
        self.assertEqual(hard.target.load_json(self.root / "journal" / "00000001__RUN_BOUND.json")["event"], "RUN_BOUND")

    def _remove_q4_commit_and_complete(self, *, remove_receipt: bool) -> None:
        # The on-disk q4 result survives, but TASK_COMMITTED was not appended.
        (self.root / "COMPLETE.json").unlink()
        (self.root / "journal" / "00000008__RUN_COMPLETE.json").unlink()
        (self.root / "journal" / "00000007__TASK_COMMITTED.json").unlink()
        if remove_receipt:
            (self.root / "receipts" / "L04_event00_qout04.json").unlink()

    def test_11_result_only_crash_window_recovered_by_replay(self) -> None:
        self._remove_q4_commit_and_complete(remove_receipt=True)
        pool = hard.make_l4_pool(self.root)
        outcome = pool.run(resume=True)
        self.assertEqual(outcome.status, "COMPLETE")
        pool.verify_complete()
        self.assert_science_matches_reference(pool)
        events = [entry["event"] for entry in pool.journal.entries()]
        self.assertIn("TASK_COMMIT_RECOVERED", events)
        self.assertIn("RUN_INTERRUPTED_RECOVERED", events)

    def test_12_result_receipt_crash_window_recovered_by_replay(self) -> None:
        self._remove_q4_commit_and_complete(remove_receipt=False)
        pool = hard.make_l4_pool(self.root)
        outcome = pool.run(resume=True)
        self.assertEqual(outcome.status, "COMPLETE")
        pool.verify_complete()
        self.assert_science_matches_reference(pool)
        events = [entry["event"] for entry in pool.journal.entries()]
        self.assertIn("TASK_COMMIT_RECOVERED", events)

    def test_13_complete_without_journal_recovered(self) -> None:
        (self.root / "journal" / "00000008__RUN_COMPLETE.json").unlink()
        pool = hard.make_l4_pool(self.root)
        outcome = pool.run(resume=True)
        self.assertEqual(outcome.status, "COMPLETE")
        self.assertEqual(last_journal_path(self.root).name, "00000008__RUN_COMPLETE_RECOVERED.json")
        pool.verify_complete()
        self.assert_science_matches_reference(pool)

    def test_14_sigterm_during_last_inflight_task(self) -> None:
        fixture_root = Path(self.scratch.name) / "fixture-stop"
        normal_root = Path(self.scratch.name) / "fixture-normal"
        final_marker = Path(self.scratch.name) / "fixture-final.json"
        worker = [
            sys.executable, str(FIXTURE_WORKER), "--checkpoint-root", str(fixture_root),
            "--final-marker", str(final_marker),
        ]
        process = subprocess.Popen(worker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                results = list((fixture_root / "results").glob("*.json"))
                q4_marker = fixture_root / "Q4_STARTED.fixture.json"
                if len(results) == 4 and q4_marker.is_file():
                    break
                if process.poll() is not None:
                    self.fail(f"fixture exited before q4 signal: {process.communicate()}")
                time.sleep(0.01)
            else:
                self.fail("timed out waiting for four committed sectors and durable Q4_STARTED")
            marker = hard.target.load_json(q4_marker)
            self.assertEqual(marker["task_id"], "L04_event00_qout04")
            self.assertFalse((fixture_root / "results" / "L04_event00_qout04.json").exists())
            os.kill(process.pid, signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 75, f"{stdout}\n{stderr}")
            self.assertIn("FIXTURE_OUTCOME STOPPED", stdout)
            self.assertFalse((fixture_root / "COMPLETE.json").exists())
            self.assertFalse(final_marker.exists())
            self.assertEqual(last_journal_path(fixture_root).name.split("__", 1)[1], "RUN_STOPPED.json")
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()
        resumed = subprocess.run(worker + ["--resume"], capture_output=True, text=True, timeout=30)
        self.assertEqual(resumed.returncode, 0, f"{resumed.stdout}\n{resumed.stderr}")
        self.assertIn("FIXTURE_OUTCOME COMPLETE", resumed.stdout)
        self.assertTrue(final_marker.is_file())
        stopped_pool = fixture_pool(fixture_root)
        stopped_pool.bind_identity(resume=True)
        stopped_pool.verify_complete()
        normal = subprocess.run(
            [sys.executable, str(FIXTURE_WORKER), "--checkpoint-root", str(normal_root)],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(normal.returncode, 0, f"{normal.stdout}\n{normal.stderr}")
        normal_pool = fixture_pool(normal_root)
        normal_pool.bind_identity(resume=True)
        normal_pool.verify_complete()
        for task in stopped_pool.tasks:
            self.assertEqual(
                scientific(stopped_pool.load_completed()[task.task_id]),
                scientific(normal_pool.load_completed()[task.task_id]),
                task.task_id,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sealed-checkpoint", type=Path, default=SEALED_R3)
    parser.add_argument("--fresh-baseline", action="store_true")
    args, remaining = parser.parse_known_args()
    HardenedRuntimeTests.sealed_checkpoint = args.sealed_checkpoint.resolve()
    HardenedRuntimeTests.fresh_baseline = args.fresh_baseline
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
