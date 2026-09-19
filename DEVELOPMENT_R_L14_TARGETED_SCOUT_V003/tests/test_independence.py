#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "independent_launcher.py"
FIXTURE = ROOT / "tests" / "fixture_process.py"


class IndependenceTests(unittest.TestCase):
    def test_one_branch_failure_does_not_terminate_survivor(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marker = root / "hostile-survived.txt"
            config = {
                "schema": "L14_INDEPENDENT_LAUNCH_CONFIG_V002",
                "run_id": "independence-test",
                "run_root": str(root / "run"),
                "branches": {
                    "target": {
                        "command": [sys.executable, "-B", str(FIXTURE), "--sleep", "0.05", "--exit-code", "7"]
                    },
                    "hostile": {
                        "command": [
                            sys.executable,
                            "-B",
                            str(FIXTURE),
                            "--sleep",
                            "0.75",
                            "--exit-code",
                            "0",
                            "--marker",
                            str(marker),
                        ]
                    },
                },
            }
            config_path = root / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-B", str(LAUNCHER), "--config", str(config_path)],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=20.0,
            )
            self.assertEqual(completed.returncode, 2, completed.stdout)
            self.assertTrue(marker.is_file(), completed.stdout)
            summaries = list((root / "run").glob("LAUNCHER_ATTEMPT_*.json"))
            self.assertEqual(len(summaries), 1)
            summary = json.loads(summaries[0].read_text(encoding="utf-8"))
            self.assertEqual(summary["branches"]["target"]["return_code"], 7)
            self.assertEqual(summary["branches"]["hostile"]["return_code"], 0)
            self.assertEqual(summary["sibling_failure_policy"], "WAIT_FOR_SURVIVING_BRANCH__NO_FAIL_FAST_SIGNAL")


if __name__ == "__main__":
    unittest.main()

