#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COORDINATOR = ROOT / "scout_coordinator.py"
BRANCH_RUNNER = ROOT / "branch_runner.py"
KERNEL = ROOT / "tests" / "fixture_kernel.py"


def run_command(command, timeout=30.0):
    return subprocess.run(
        command,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
    )


def run_branch(root, branch, phase, request):
    checkpoint = root / "{}-{}-checkpoint".format(branch, phase)
    output = root / "{}-{}-result.json".format(branch, phase)
    completed = run_command(
        [
            sys.executable,
            "-B",
            str(BRANCH_RUNNER),
            "--branch",
            branch,
            "--phase",
            phase,
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
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stdout)
    return output


class GatewayTests(unittest.TestCase):
    def test_q5_sterility_halts_without_phase3_authorization(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_root = root / "coordinator"
            prepared = run_command(
                [
                    sys.executable,
                    "-B",
                    str(COORDINATOR),
                    "prepare",
                    "--run-root",
                    str(run_root),
                    "--run-id",
                    "sterile-test",
                ]
            )
            self.assertEqual(prepared.returncode, 0, prepared.stdout)
            request = run_root / "PHASE1_REQUEST.json"
            target_source = run_branch(root, "target", "bridge", request)
            hostile_source = run_branch(root, "hostile", "bridge", request)
            sterile_paths = []
            for branch, source in (("target", target_source), ("hostile", hostile_source)):
                payload = json.loads(source.read_text(encoding="utf-8"))
                payload["atoms"] = [atom for atom in payload["atoms"] if atom["q"] != 5]
                sterile = root / "{}-sterile.json".format(branch)
                sterile.write_text(json.dumps(payload), encoding="utf-8")
                sterile_paths.append(sterile)
            gated = run_command(
                [
                    sys.executable,
                    "-B",
                    str(COORDINATOR),
                    "phase2",
                    "--run-root",
                    str(run_root),
                    "--target",
                    str(sterile_paths[0]),
                    "--hostile",
                    str(sterile_paths[1]),
                ]
            )
            self.assertEqual(gated.returncode, 20, gated.stdout)
            self.assertIn("L14_Q5_STERILE", gated.stdout)
            self.assertFalse((run_root / "PHASE3_REQUEST.json").exists())

    def test_bridge_gate_authorizes_tail_and_final_mass_is_deduplicated(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_root = root / "coordinator"
            prepared = run_command(
                [
                    sys.executable,
                    "-B",
                    str(COORDINATOR),
                    "prepare",
                    "--run-root",
                    str(run_root),
                    "--run-id",
                    "gateway-test",
                    "--threshold",
                    "0.50",
                ]
            )
            self.assertEqual(prepared.returncode, 0, prepared.stdout)
            phase1_request = run_root / "PHASE1_REQUEST.json"
            target1 = run_branch(root, "target", "bridge", phase1_request)
            hostile1 = run_branch(root, "hostile", "bridge", phase1_request)
            gated = run_command(
                [
                    sys.executable,
                    "-B",
                    str(COORDINATOR),
                    "phase2",
                    "--run-root",
                    str(run_root),
                    "--target",
                    str(target1),
                    "--hostile",
                    str(hostile1),
                ]
            )
            self.assertEqual(gated.returncode, 0, gated.stdout)
            self.assertIn("L14_SCOUT_DECISION PROCEED", gated.stdout)
            phase3_request = run_root / "PHASE3_REQUEST.json"
            self.assertTrue(phase3_request.is_file())

            target3 = run_branch(root, "target", "conditional_tail", phase3_request)
            hostile3 = run_branch(root, "hostile", "conditional_tail", phase3_request)
            final = run_command(
                [
                    sys.executable,
                    "-B",
                    str(COORDINATOR),
                    "final",
                    "--run-root",
                    str(run_root),
                    "--target",
                    str(target3),
                    "--hostile",
                    str(hostile3),
                ]
            )
            self.assertEqual(final.returncode, 0, final.stdout)
            report = json.loads((run_root / "FINAL_GATE_REPORT.json").read_text(encoding="utf-8"))
            self.assertTrue(report["final_threshold_met"])
            self.assertEqual(report["final_passing_sectors"], [4, 5, 6, 7, 8, 9])
            self.assertEqual(report["final_deduplicated_mass"], "0.783")


if __name__ == "__main__":
    unittest.main()
