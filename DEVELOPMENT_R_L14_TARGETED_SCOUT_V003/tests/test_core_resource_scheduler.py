#!/usr/bin/env python3

from __future__ import annotations

import concurrent.futures
import math
import sys
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KERNELS = ROOT / "kernels"
for path in (ROOT, KERNELS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import checkpointed_history as history  # noqa: E402
import exact_common  # noqa: E402
from resource_scheduler import (  # noqa: E402
    BASE_WORKSPACE_BYTES,
    HOSTILE_ALLOCATION_VECTOR_SLOTS,
    MAX_HOSTILE_WORKSPACE_BYTES,
    MAX_TARGET_WORKSPACE_BYTES,
    NUMERICAL_RESERVATION_BUDGET_BYTES,
    TARGET_MAX_KRYLOV_DEPTH,
    TARGET_MINIMUM_LIVE_VECTORS,
    TARGET_WORKING_VECTOR_SLOTS,
    hostile_batch_rows_l14,
    hostile_workspace_bytes,
    make_bounded_pool_type,
    target_batch_rows_l14,
    target_workspace_bytes,
    task_reservation_bytes,
)


class _Resolution:
    checkpoints = (24, 48, 96)


class _FutureExecutor:
    def submit(self, function, task):
        future = concurrent.futures.Future()
        try:
            future.set_result(function(task))
        except BaseException as error:
            future.set_exception(error)
        return future


class _Progress:
    def __init__(self, **kwargs):
        self.total = kwargs["total_tasks"]
        self.completed = 0
        self.work = 0

    def advance(self, count, work):
        self.completed += count
        self.work += work


class _BasePool:
    def __init__(self, *, branch, max_workers, **kwargs):
        del kwargs
        self.branch = branch
        self.max_workers = max_workers
        self._closed = False
        self._stop = threading.Event()
        self._submitted_any = False
        self._run_progress = None
        self._executor = _FutureExecutor()

    def _observe_children(self):
        return None

    def emit_stop_snapshot(self, reason):
        del reason

    def request_stop(self, terminate_running=False):
        del terminate_running
        self._stop.set()

    def resource_record(self):
        return {}


class _Runtime:
    BranchProcessPool = _BasePool
    ParentProgress = _Progress

    class ParallelRefusal(RuntimeError):
        pass


class CoreResourceSchedulerTests(unittest.TestCase):
    def test_q14_workspaces_admit_exactly_one_complete_row(self):
        columns = math.comb(28, 14)
        self.assertEqual(
            hostile_workspace_bytes(14),
            HOSTILE_ALLOCATION_VECTOR_SLOTS * 16 * columns,
        )
        self.assertEqual(target_workspace_bytes(14), 100 * 16 * columns)
        self.assertEqual(MAX_HOSTILE_WORKSPACE_BYTES, 12_837_312_000)
        self.assertEqual(MAX_TARGET_WORKSPACE_BYTES, 64_186_560_000)

    def test_target_workspace_covers_complete_sharp_krylov_depth_for_every_q(self):
        self.assertEqual(TARGET_MAX_KRYLOV_DEPTH, max(_Resolution.checkpoints))
        repair, _a, _b, _c, _d = history.load_frozen()
        self.assertEqual(
            TARGET_MAX_KRYLOV_DEPTH,
            max(
                max(repair.TARGET_COARSE.checkpoints),
                max(repair.TARGET_FINE.checkpoints),
            ),
        )
        self.assertEqual(
            TARGET_MINIMUM_LIVE_VECTORS,
            TARGET_MAX_KRYLOV_DEPTH + TARGET_WORKING_VECTOR_SLOTS,
        )
        for q in range(15):
            columns = math.comb(28, q)
            complete_row = (
                TARGET_MINIMUM_LIVE_VECTORS * 16 * columns
            )
            self.assertGreaterEqual(target_workspace_bytes(q), complete_row)

    def test_no_separate_terminal_or_io_row_ceiling(self):
        columns = math.comb(28, 14)
        self.assertEqual(hostile_batch_rows_l14(columns, 128, amplitude_window=1), 1)
        self.assertEqual(target_batch_rows_l14(columns, _Resolution(), False), 1)

    def test_all_q_reservations_fit_declared_budget(self):
        for q in range(15):
            hostile = task_reservation_bytes("hostile", {"q": q})
            target = task_reservation_bytes("target", {"q": q})
            self.assertGreaterEqual(hostile, BASE_WORKSPACE_BYTES)
            self.assertGreaterEqual(target, BASE_WORKSPACE_BYTES)
            self.assertLessEqual(hostile, NUMERICAL_RESERVATION_BUDGET_BYTES)
            self.assertLessEqual(target, NUMERICAL_RESERVATION_BUDGET_BYTES)
        self.assertEqual(
            NUMERICAL_RESERVATION_BUDGET_BYTES // hostile_workspace_bytes(14), 70
        )
        self.assertEqual(
            NUMERICAL_RESERVATION_BUDGET_BYTES // target_workspace_bytes(14), 14
        )
        self.assertEqual(
            NUMERICAL_RESERVATION_BUDGET_BYTES // target_workspace_bytes(10), 43
        )

    def test_target_batch_rows_refuses_a_resolution_deeper_than_its_reservation(self):
        class _TooDeep:
            checkpoints = (TARGET_MAX_KRYLOV_DEPTH + 1,)

        with self.assertRaisesRegex(ValueError, "cannot hold one complete Krylov row"):
            target_batch_rows_l14(math.comb(28, 14), _TooDeep(), False)

    def test_nonfinite_evidence_is_refused_with_its_exact_path(self):
        with self.assertRaisesRegex(
            exact_common.ExactKernelRefusal,
            r"\$\.row\.actual_solver\.maximum_residual_indicator",
        ):
            exact_common.canonical_json_bytes({
                "row": {
                    "actual_solver": {"maximum_residual_indicator": math.inf}
                }
            })

    def test_target_worker_convergence_refusal_reports_task_identity(self):
        task = {
            "resolution": "coarse",
            "role": "actual",
            "q": 10,
            "lower": 0,
            "upper": 1,
        }
        with self.assertRaisesRegex(
            exact_common.ExactKernelRefusal,
            "target numerical convergence failure.*'q': 10",
        ):
            history._require_target_convergence(
                task,
                {
                    "solver": {
                        "converged": False,
                        "maximum_residual_indicator": math.inf,
                    }
                },
                ("solver",),
            )

    def test_hostile_worker_convergence_refusal_reports_task_identity(self):
        task = {
            "accuracy": "sharp",
            "phase": "child1",
            "q": 13,
            "lower": 0,
            "upper": 1,
        }
        with self.assertRaisesRegex(
            exact_common.ExactKernelRefusal,
            "hostile numerical convergence failure.*'q': 13",
        ):
            history._require_hostile_convergence(
                task,
                {
                    "method": {
                        "converged": False,
                        "maximum_degree": 128,
                    }
                },
            )

    def test_pool_submits_under_sum_of_live_reservations(self):
        pool_type = make_bounded_pool_type(_Runtime)
        per_task = hostile_workspace_bytes(14)
        pool = pool_type(
            branch="hostile",
            max_workers=180,
            reservation_budget_bytes=2 * per_task,
        )
        tasks = [{"q": 14, "value": index} for index in range(5)]
        results = pool.map_ordered(
            lambda task: task["value"],
            tasks,
            stage="test",
            charge_sectors=5,
            row_windows=5,
            work_units=[5, 4, 3, 2, 1],
        )
        self.assertEqual(results, list(range(5)))
        self.assertEqual(pool.peak_reserved_bytes, 2 * per_task)
        self.assertLessEqual(pool.peak_reserved_bytes, pool.reservation_budget_bytes)

    def test_full_hostile_plan_includes_sharp_intermediate_history(self):
        repair, _a, _b, _c, _d = history.load_frozen()
        target = history._full_history_plan(repair, "target")
        full = history._full_history_plan(repair, "hostile")
        older_suffix_only = repair.hostile_repair_plan(14)
        self.assertEqual(target, {
            "total_tasks": 43_671,
            "charge_sectors": 654,
            "row_windows": 43_463,
            "total_work_units": 18_285_993_728_464,
        })
        self.assertEqual(full, {
            "total_tasks": 24_772,
            "charge_sectors": 682,
            "row_windows": 24_564,
            "total_work_units": 24_935_445_993_360,
        })
        for field in ("total_tasks", "charge_sectors", "row_windows", "total_work_units"):
            self.assertGreater(full[field], older_suffix_only[field])

    def test_history_deadline_is_explicitly_unbounded(self):
        self.assertTrue(math.isinf(exact_common.deadline({"wall_seconds": 1})))


if __name__ == "__main__":
    unittest.main()
