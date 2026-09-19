#!/usr/bin/env python3
"""Static census for execution-only stops accidentally carried into V003.

Frozen predecessor sources deliberately remain in the authenticated bundle.
They are evidence and implementation dependencies, so this census scans the
active V003 wrappers and control plane and separately verifies that wrappers
neutralize predecessor-only execution guards before calling frozen kernels.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BUNDLED_COMPUTE_PATHS = (
    "resumable_runtime.py",
    "branch_runner.py",
    "aws/aws_branch_once.py",
    "aws/run_branch_once.sh",
    "kernels/exact_common.py",
    "kernels/resource_scheduler.py",
    "kernels/cache_builder.py",
    "kernels/checkpointed_history.py",
    "kernels/geometry.py",
    "kernels/target_exact_kernel.py",
    "kernels/hostile_exact_kernel.py",
)

CONTROL_PATHS = (
    "capacity_plan.py",
    "readiness.py",
    "stack_parameters.py",
    "aws/launch_phase1.py",
    "aws/start_phase3.py",
    "AWS_RUN_CONFIG.example.json",
)

Q_CERTIFICATE_CONTROL_PATHS = (
    "readiness.py",
    "AWS_RUN_CONFIG.example.json",
)

RULES = {
    "compute_path_machine_poweroff": (
        BUNDLED_COMPUTE_PATHS,
        re.compile(
            r"(?:systemctl\s+(?:poweroff|halt|reboot)|"
            r"(?:^|[;&|]\s*)(?:sudo\s+)?(?:/sbin/)?poweroff\b|"
            r"\bshutdown\s+-[hPr])",
            re.IGNORECASE | re.MULTILINE,
        ),
    ),
    "fixed_512mib_terminal_or_io_gate": (
        BUNDLED_COMPUTE_PATHS,
        re.compile(
            r"(?:512\s*\*\s*(?:2\s*\*\*\s*20|1024\s*\*\s*1024)|"
            r"536_?870_?912)"
        ),
    ),
    "fixed_64gib_response_rss_gate": (
        BUNDLED_COMPUTE_PATHS,
        re.compile(
            r"(?:RESPONSE_RSS_BYTES|RSS_LIMIT_BYTES)\s*=\s*"
            r"(?:64\s*\*\s*(?:2\s*\*\*\s*30|\(1\s*<<\s*30\))|"
            r"68_?719_?476_?736)"
        ),
    ),
    "fixed_three_hour_response_timeout": (
        BUNDLED_COMPUTE_PATHS,
        re.compile(
            r"(?:SECTOR_SECONDS_LIMIT|WALL_LIMIT_SECONDS)\s*=\s*"
            r"(?:3\s*\*\s*60\s*\*\s*60|10_?800)"
        ),
    ),
    "single_sector_capacity_certificate": (
        Q_CERTIFICATE_CONTROL_PATHS,
        re.compile(
            r"(?:HOSTILE_Q9_CAPACITY_CERTIFICATE|hostile_q9_columns|"
            r"hostile_q9_single_row_estimate_bytes|L14_HOSTILE_CAPACITY_PLAN_V002)"
        ),
    ),
    "manual_prior_attempt_arithmetic": (
        CONTROL_PATHS,
        re.compile(r"(?:prior_paid_attempt_minutes_each|prior_compute_cost_usd)"),
    ),
}


def census() -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {name: [] for name in RULES}
    for name, (relative_paths, pattern) in RULES.items():
        for relative in relative_paths:
            path = ROOT / relative
            if not path.is_file():
                findings[name].append("{}: MISSING".format(relative))
                continue
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if pattern.search(line):
                    findings[name].append(
                        "{}:{}: {}".format(relative, line_number, line.strip())
                    )
    return findings


class StopConditionCensusTests(unittest.TestCase):
    def test_q_aware_scheduler_is_part_of_each_kernel_bundle(self):
        source = (ROOT / "bind_exact_release.py").read_text(encoding="utf-8")
        self.assertIn('"resource_scheduler.py"', source)

    def test_active_bundle_and_control_plane_have_no_hidden_stop_conditions(self):
        findings = census()
        failures = [
            "{}\n  {}".format(name, "\n  ".join(records))
            for name, records in findings.items()
            if records
        ]
        self.assertEqual(failures, [], "\n" + "\n".join(failures))

    def test_response_wrappers_neutralize_legacy_execution_guards_before_call(self):
        source = (ROOT / "kernels" / "geometry.py").read_text(encoding="utf-8")
        ordered_contracts = (
            ("target.RSS_LIMIT_BYTES = EXECUTION_GUARD_SENTINEL", "target.worker("),
            ("target.SECTOR_SECONDS_LIMIT = math.inf", "target.worker("),
            ("hostile.RSS_LIMIT_BYTES = EXECUTION_GUARD_SENTINEL", "hostile.calculate_row("),
            ("hostile.WALL_LIMIT_SECONDS = math.inf", "hostile.calculate_row("),
        )
        for override, invocation in ordered_contracts:
            with self.subTest(override=override):
                self.assertIn(override, source)
                self.assertIn(invocation, source)
                self.assertLess(source.index(override), source.index(invocation))

    def test_history_wrapper_rebinds_legacy_terminal_and_io_windows(self):
        source = (ROOT / "kernels" / "checkpointed_history.py").read_text(
            encoding="utf-8"
        )
        # These names are the execution-relevant 512 MiB predecessor gates.
        # V003 may retain the frozen files, but every name must be rebound by
        # the active wrapper to its q-aware worker reservation.
        for name in (
            "TERMINAL_WINDOW_BYTES",
            "IO_WINDOW_BYTES",
            "IO_WINDOW_LIMIT",
        ):
            with self.subTest(name=name):
                self.assertIn(name, source)
        for binding in (
            "cap = target_workspace_bytes(q)",
            "repair.target.v004.v3.TERMINAL_WINDOW_BYTES = cap",
            "repair.target.v004.IO_WINDOW_BYTES = max(COMPLEX128_BYTES * sector_columns(q), cap)",
            "cap = hostile_workspace_bytes(q)",
            "repair.hostile.v3.IO_WINDOW_LIMIT = row_bytes",
            "repair.hostile.physical.TERMINAL_WINDOW_BYTES = cap",
        ):
            with self.subTest(binding=binding):
                self.assertIn(binding, source)


if __name__ == "__main__":
    unittest.main()
