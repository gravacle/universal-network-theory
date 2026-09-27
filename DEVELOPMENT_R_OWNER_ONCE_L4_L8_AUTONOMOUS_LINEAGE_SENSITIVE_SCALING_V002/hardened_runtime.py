#!/usr/bin/env python3
"""V002 target checkpoint adapter; V001 scientific kernel is kept byte-for-byte."""

from __future__ import annotations

import fcntl
import hashlib
import math
import re
import subprocess
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

import sys


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
V001 = ROOT / "DEVELOPMENT_R_OWNER_ONCE_L4_L8_AUTONOMOUS_LINEAGE_SENSITIVE_SCALING_V001"
EXPECTED_V001_KERNEL_SHA256 = "06fcea51701c5dcf4ceb2dbf31e9a4a02c556ada57d9148a0c32793de054a5fd"
_v001_kernel = V001 / "target_lineage_scaling.py"
if _v001_kernel.is_symlink() or not _v001_kernel.is_file() or hashlib.sha256(_v001_kernel.read_bytes()).hexdigest() != EXPECTED_V001_KERNEL_SHA256:
    raise RuntimeError("frozen V001 scientific kernel mismatch before import")
sys.path.insert(0, str(V001))
import target_lineage_scaling as target  # noqa: E402


EXPECTED_PARENT_TREE = "be83f661a6e806c61a6291be315bf78b08bbc006"


def authenticate_frozen_dependencies() -> dict[str, str]:
    """Keep the historical source seal valid after additive packet commits."""
    current = target.git("rev-parse", "HEAD")
    require_parent = subprocess.run(
        ["git", "merge-base", "--is-ancestor", target.EXPECTED_HEAD, current],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    if require_parent.returncode != 0:
        raise target.ScalingError("execution HEAD does not descend from frozen source commit")
    if target.git("rev-parse", f"{target.EXPECTED_HEAD}^{{tree}}") != EXPECTED_PARENT_TREE:
        raise target.ScalingError("frozen source tree mismatch")
    kernel_path = V001 / "target_lineage_scaling.py"
    if kernel_path.is_symlink() or not kernel_path.is_file() or target.sha256_file(kernel_path) != EXPECTED_V001_KERNEL_SHA256:
        raise target.ScalingError("frozen V001 scientific kernel mismatch")
    observed: dict[str, str] = {}
    for relative, expected in target.DEPENDENCY_HASHES.items():
        candidate = ROOT / relative
        if not candidate.is_file() or candidate.is_symlink() or target.sha256_file(candidate) != expected:
            raise target.ScalingError(f"frozen dependency mismatch: {relative}")
        observed[relative] = expected
    return observed


target.authenticate_dependencies = authenticate_frozen_dependencies
durable, base = target.load_resume_runtime()
SCHEMA = "L4_L8_HARDENED_COMPLETE_V002"
RECEIPT_SCHEMA = "L4_L8_HARDENED_TASK_RECEIPT_V002"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise durable.EvidenceError(message)


def strict_number(value: Any, *, minimum: float | None = None, maximum: float | None = None) -> float:
    require(type(value) in (int, float), "expected strict JSON number")
    number = float(value)
    require(math.isfinite(number), "nonfinite checkpoint number")
    if minimum is not None:
        require(number >= minimum, "checkpoint number below domain")
    if maximum is not None:
        require(number <= maximum, "checkpoint number above domain")
    return number


def exact_keys(value: Any, expected: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == expected, f"{label} key census")


def validate_solver(value: Any) -> None:
    exact_keys(
        value,
        {"converged", "exp_difference", "low_memory", "maximum_live_bytes", "residual_indicator", "steps", "subdivisions"},
        "solver",
    )
    require(type(value["converged"]) is int and value["converged"] == 1, "solver convergence")
    require(type(value["low_memory"]) is int and value["low_memory"] in (0, 1), "solver memory mode")
    for key in ("maximum_live_bytes", "steps", "subdivisions"):
        require(type(value[key]) is int and value[key] >= 0, f"solver {key}")
    strict_number(value["residual_indicator"], minimum=0)
    if value["exp_difference"] is not None:
        strict_number(value["exp_difference"], minimum=0)


def validate_stage(value: Any) -> None:
    exact_keys(
        value,
        {"carrier_configuration_tv", "carrier_trace_distance", "controls", "delta_n", "trace_actual", "trace_product"},
        "sector stage",
    )
    trace_distance = strict_number(value["carrier_trace_distance"], minimum=0, maximum=1 + 1e-11)
    configuration_tv = strict_number(value["carrier_configuration_tv"], minimum=0, maximum=1 + 1e-11)
    require(configuration_tv <= trace_distance + 1e-11, "configuration TV exceeds trace distance")
    for key in ("trace_actual", "trace_product"):
        strict_number(value[key], minimum=0, maximum=1 + 1e-11)
    require(type(value["delta_n"]) is list and len(value["delta_n"]) == 8, "delta_n census")
    for number in value["delta_n"]:
        strict_number(number, minimum=-1 - 1e-11, maximum=1 + 1e-11)
    controls = value["controls"]
    exact_keys(
        controls,
        {"factor_columns_actual", "factor_columns_product", "reduced_dimension", "qr_reconstruction", "reduced_hermiticity", "eigenvalue_sum_trace_residual"},
        "sector stage controls",
    )
    for key in ("factor_columns_actual", "factor_columns_product", "reduced_dimension"):
        require(type(controls[key]) is int and controls[key] >= 1, f"stage {key}")
    for key in ("qr_reconstruction", "reduced_hermiticity", "eigenvalue_sum_trace_residual"):
        require(strict_number(controls[key], minimum=0) <= 1e-11, f"stage {key} tolerance")


def validate_sector_result(task: Any, body: Any, pool: Any) -> dict[str, Any]:
    exact_keys(
        body,
        {"schema", "run_id", "branch", "phase", "task_id", "task_sha256", "work_units", "result"},
        "checkpoint outer",
    )
    require(body["schema"] == base.RESULT_SCHEMA, "checkpoint outer schema")
    for key, expected in (
        ("run_id", pool.run_id), ("branch", pool.branch), ("phase", pool.phase),
        ("task_id", task.task_id), ("task_sha256", task.task_sha256), ("work_units", task.work_units),
    ):
        require(type(body[key]) is type(expected) and body[key] == expected, f"checkpoint outer {key}")
    result = body["result"]
    exact_keys(
        result,
        {"schema", "L", "event", "q_out", "after_admission", "after_transport", "controls", "task_binding", "resource", "artifacts"},
        "sector result",
    )
    require(result["schema"] == "L4_L8_TARGET_RESPONSE_SECTOR_V001", "sector schema")
    require(type(result["L"]) is int and result["L"] == 4, "sector L")
    require(type(result["event"]) is int and result["event"] == 0, "sector event")
    require(type(result["q_out"]) is int and result["q_out"] == task.payload["q_out"], "sector q")
    binding = result["task_binding"]
    exact_keys(binding, {"task_id", "task_sha256", "history_sha256", "engine_sha256", "kernel_sha256"}, "sector binding")
    for key, expected in (
        ("task_id", task.task_id), ("task_sha256", task.task_sha256),
        ("history_sha256", target.HISTORY_HASHES[4]),
        ("engine_sha256", target.DEPENDENCY_HASHES[str(target.ENGINE_RELATIVE)]),
        ("kernel_sha256", durable.sha256_file(pool.kernel_module)),
    ):
        require(binding[key] == expected, f"sector binding {key}")
    validate_stage(result["after_admission"])
    validate_stage(result["after_transport"])
    controls = result["controls"]
    exact_keys(
        controls,
        {"actual_transport_solver", "product_transport_solver", "terminal_reconstruction", "trace_distance_transport_invariance"},
        "sector controls",
    )
    for key in ("actual_transport_solver", "product_transport_solver"):
        validate_solver(controls[key])
    require(type(controls["terminal_reconstruction"]) is list, "terminal reconstruction census")
    for terminal in controls["terminal_reconstruction"]:
        exact_keys(terminal, {"norm", "q", "shape", "solver"}, "terminal reconstruction")
        strict_number(terminal["norm"], minimum=0, maximum=1 + 1e-11)
        require(type(terminal["q"]) is int and 0 <= terminal["q"] <= 4, "terminal q")
        require(type(terminal["shape"]) is list and len(terminal["shape"]) == 2, "terminal shape")
        for size in terminal["shape"]:
            require(type(size) is int and size >= 1, "terminal dimension")
        validate_solver(terminal["solver"])
    invariance = strict_number(controls["trace_distance_transport_invariance"], minimum=0)
    require(invariance <= 1e-11, "trace-distance transport invariance")
    require(
        abs(result["after_admission"]["carrier_trace_distance"] - result["after_transport"]["carrier_trace_distance"])
        <= invariance + 1e-12,
        "invariance control does not match stages",
    )
    resource = result["resource"]
    exact_keys(resource, {"wall_seconds", "peak_rss_bytes"}, "sector resource")
    strict_number(resource["wall_seconds"], minimum=0)
    require(type(resource["peak_rss_bytes"]) is int and resource["peak_rss_bytes"] > 0, "sector RSS")
    require(result["artifacts"] == [], "unexpected sector artifact")
    return result


class HardenedPool(base.ResumableProcessPool):
    """Target-specific exact schema, receipt, journal, and stop-aware runtime."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if Path(kwargs["kernel_module"]).resolve() == _v001_kernel.resolve():
            kwargs["kernel_module"] = PACKET / "frozen_kernel_adapter.py"
        parameters = dict(kwargs["parameters"])
        parameters["hardened_runtime_sha256"] = durable.sha256_file(Path(__file__))
        parameters["hardened_runner_sha256"] = durable.sha256_file(PACKET / "run_l4_v002.py")
        kwargs["parameters"] = parameters
        super().__init__(*args, **kwargs)
        self.receipt_root = self.root / "receipts"
        global ACTIVE_POOL
        ACTIVE_POOL = self

    def _receipt_path(self, task: Any) -> Path:
        return self.receipt_root / f"{task.task_id}.json"

    def _validate_result_payload(self, task: Any, body: Mapping[str, Any]) -> Any:
        return validate_sector_result(task, body, self)

    def _validate_receipt(self, task: Any, path: Path) -> None:
        receipt_path = self._receipt_path(task)
        require(receipt_path.is_file() and not receipt_path.is_symlink(), f"missing receipt: {task.task_id}")
        receipt = target.load_json(receipt_path)
        exact_keys(
            receipt,
            {"schema", "task_id", "task_sha256", "run_identity_sha256", "result_sha256", "result_bytes", "scientific_sha256"},
            "task receipt",
        )
        require(receipt["schema"] == RECEIPT_SCHEMA, "receipt schema")
        require(receipt["task_id"] == task.task_id and receipt["task_sha256"] == task.task_sha256, "receipt task")
        require(receipt["run_identity_sha256"] == durable.sha256_file(self.identity_path), "receipt run identity")
        require(receipt["result_sha256"] == durable.sha256_file(path), "receipt result hash")
        require(type(receipt["result_bytes"]) is int and receipt["result_bytes"] == path.stat().st_size, "receipt bytes")
        body = target.load_json(path)
        scientific = dict(body["result"])
        scientific.pop("resource")
        require(receipt["scientific_sha256"] == durable.sha256_bytes(durable.canonical_json_bytes(scientific)), "receipt scientific hash")

    def _commit_result(self, task: Any, result: Any) -> Any:
        validated = super()._commit_result(task, result)
        path = self._task_result_path(task)
        self._publish_receipt(task, validated, path)
        return validated

    def _publish_receipt(self, task: Any, validated: Mapping[str, Any], path: Path) -> None:
        scientific = dict(validated)
        scientific.pop("resource")
        receipt = {
            "schema": RECEIPT_SCHEMA,
            "task_id": task.task_id,
            "task_sha256": task.task_sha256,
            "run_identity_sha256": durable.sha256_file(self.identity_path),
            "result_sha256": durable.sha256_file(path),
            "result_bytes": path.stat().st_size,
            "scientific_sha256": durable.sha256_bytes(durable.canonical_json_bytes(scientific)),
        }
        durable.immutable_write_json(self._receipt_path(task), receipt)
        self._validate_receipt(task, path)

    def _replay_scientific_result(self, task: Any) -> Any:
        context = {
            "run_id": self.run_id, "branch": self.branch, "phase": self.phase,
            "task_id": task.task_id, "task_sha256": task.task_sha256,
            "checkpoint_root": str(self.root), "parameters": self.parameters,
        }
        with ProcessPoolExecutor(max_workers=1, initializer=base._worker_initializer) as executor:
            replay = executor.submit(
                base.invoke_kernel, str(self.kernel_module), self.kernel_function,
                dict(task.payload), context,
            ).result()
        body = {
            "schema": base.RESULT_SCHEMA, "run_id": self.run_id, "branch": self.branch,
            "phase": self.phase, "task_id": task.task_id, "task_sha256": task.task_sha256,
            "work_units": task.work_units, "result": replay,
        }
        return self._validate_result_payload(task, body)

    def recover_unjournaled_results(self) -> None:
        """Replay a crash-window task before accepting a result or adding a receipt."""
        if not list(self.journal.root.glob("*.json")):
            # The identity link may have landed just before a power loss.
            require(self.identity_path.is_file() and not self.identity_path.is_symlink(), "recovery identity")
            require(target.load_json(self.identity_path) == self._identity_payload(), "recovery identity mismatch")
            self.journal.append("RUN_BOUND", {"identity_sha256": durable.sha256_file(self.identity_path)})
        was_running = self.verify_journal(allow_complete_recovery=self.complete_path.exists())
        if self.complete_path.exists():
            return
        committed = {
            entry["payload"]["task_id"]
            for entry in self.journal.entries()
            if entry["event"] in ("TASK_COMMITTED", "TASK_COMMIT_RECOVERED")
        }
        pending_recovery = [
            task for task in self.tasks
            if task.task_id not in committed and self._task_result_path(task).exists()
        ]
        if pending_recovery and not was_running:
            # An earlier journal write may have failed and closed that attempt
            # with RUN_FAILED; recovery itself must be a distinct attempt.
            self.journal.append("RUN_RESUMED", {"recovery_only": True})
        for task in self.tasks:
            path = self._task_result_path(task)
            receipt_path = self._receipt_path(task)
            require(not receipt_path.exists() or path.exists(), "receipt without result")
            if task.task_id in committed or not path.exists():
                continue
            require(path.is_file() and not path.is_symlink(), "unjournaled result type")
            original = self._validate_result_payload(task, target.load_json(path))
            replay = self._replay_scientific_result(task)
            original_scientific = dict(original)
            replay_scientific = dict(replay)
            original_scientific.pop("resource")
            replay_scientific.pop("resource")
            require(original_scientific == replay_scientific, f"replay mismatch: {task.task_id}")
            if receipt_path.exists():
                self._validate_receipt(task, path)
            else:
                self._publish_receipt(task, original, path)
            self.journal.append("TASK_COMMIT_RECOVERED", {
                "task_id": task.task_id,
                "result_sha256": durable.sha256_file(path),
                "receipt_sha256": durable.sha256_file(receipt_path),
                "replay_scientific_sha256": durable.sha256_bytes(durable.canonical_json_bytes(replay_scientific)),
            })
        if was_running or pending_recovery:
            self.journal.append("RUN_INTERRUPTED_RECOVERED", {"run_identity_sha256": durable.sha256_file(self.identity_path)})

    def load_completed(self) -> dict[str, Any]:
        require(self.identity_path.is_file() and not self.identity_path.is_symlink(), "missing run identity")
        require(target.load_json(self.identity_path) == self._identity_payload(), "run identity mismatch")
        require(self.result_root.is_dir() or not self.result_root.exists(), "result root type")
        require(self.receipt_root.is_dir() or not self.receipt_root.exists(), "receipt root type")
        expected_names = {f"{task.task_id}.json" for task in self.tasks}
        for folder in (self.result_root, self.receipt_root):
            if folder.exists():
                require(not folder.is_symlink(), "checkpoint directory symlink")
                require({p.name for p in folder.glob("*.json")} <= expected_names, "unexpected checkpoint JSON")
        completed: dict[str, Any] = {}
        for task in self.tasks:
            path = self._task_result_path(task)
            if path.exists():
                completed[task.task_id] = self._validate_result_payload(task, target.load_json(path))
        for task in self.tasks:
            path = self._task_result_path(task)
            receipt_path = self._receipt_path(task)
            require(path.exists() == receipt_path.exists(), f"incomplete result/receipt pair: {task.task_id}")
            if path.exists():
                require(not path.is_symlink(), f"result symlink: {task.task_id}")
                self._validate_receipt(task, path)
        return completed

    def verify_complete(self, *, allow_journal_recovery: bool = False) -> None:
        require(self.complete_path.is_file() and not self.complete_path.is_symlink(), "missing COMPLETE")
        complete = target.load_json(self.complete_path)
        exact_keys(
            complete,
            {"schema", "run_id", "branch", "phase", "run_identity_sha256", "completed_tasks", "total_tasks", "completed_work_units", "total_work_units", "result_files", "receipt_files", "result_set_sha256", "receipt_set_sha256"},
            "COMPLETE",
        )
        require(complete["schema"] == SCHEMA, "COMPLETE schema")
        for key in ("run_id", "branch", "phase"):
            require(complete[key] == getattr(self, key), f"COMPLETE {key}")
        require(complete["run_identity_sha256"] == durable.sha256_file(self.identity_path), "COMPLETE identity")
        require(complete["completed_tasks"] == complete["total_tasks"] == len(self.tasks), "COMPLETE task census")
        work = sum(task.work_units for task in self.tasks)
        require(complete["completed_work_units"] == complete["total_work_units"] == work, "COMPLETE work census")
        results = [{"task_id": task.task_id, "sha256": durable.sha256_file(self._task_result_path(task))} for task in self.tasks]
        receipts = [{"task_id": task.task_id, "sha256": durable.sha256_file(self._receipt_path(task))} for task in self.tasks]
        require(complete["result_files"] == results and complete["receipt_files"] == receipts, "COMPLETE file hashes")
        require(complete["result_set_sha256"] == durable.sha256_bytes(durable.canonical_json_bytes(results)), "COMPLETE result set")
        require(complete["receipt_set_sha256"] == durable.sha256_bytes(durable.canonical_json_bytes(receipts)), "COMPLETE receipt set")
        completed = self.load_completed()
        require(len(completed) == len(self.tasks), "COMPLETE without task results")
        self.verify_journal(completed, allow_complete_recovery=allow_journal_recovery)

    def verify_journal(self, completed: Mapping[str, Any] | None = None, *, allow_complete_recovery: bool = False) -> bool:
        require(self.journal.root.is_dir() and not self.journal.root.is_symlink(), "journal directory")
        all_paths = sorted(self.journal.root.iterdir())
        orphan_pattern = re.compile(r"^\.[0-9]{8}__[A-Z_]+\.json-[A-Za-z0-9_-]+$")
        require(all(
            path.is_file() and not path.is_symlink()
            and (path.suffix == ".json" or orphan_pattern.fullmatch(path.name))
            for path in all_paths
        ), "journal file census")
        paths = [path for path in all_paths if path.suffix == ".json"]
        entries = [target.load_json(path) for path in paths]
        require(entries and entries[0]["event"] == "RUN_BOUND", "journal origin")
        exact_keys(entries[0]["payload"], {"identity_sha256"}, "journal origin payload")
        require(entries[0]["payload"]["identity_sha256"] == durable.sha256_file(self.identity_path), "journal identity")
        committed: list[str] = []
        started = False
        closed = False
        for index, entry in enumerate(entries, 1):
            exact_keys(entry, {"schema", "sequence", "event", "payload"}, "journal entry")
            require(entry["schema"] == "L14_APPEND_ONLY_EVENT_V002" and type(entry["sequence"]) is int and entry["sequence"] == index, "journal sequence")
            require(paths[index - 1].name == f"{index:08d}__{entry['event']}.json", "journal filename")
            event = entry["event"]
            require(event in {"RUN_BOUND", "RUN_STARTED", "RUN_RESUMED", "TASK_COMMITTED", "TASK_COMMIT_RECOVERED", "RUN_STOPPED", "RUN_FAILED", "RUN_INTERRUPTED_RECOVERED", "RUN_COMPLETE", "RUN_COMPLETE_RECOVERED"}, "unknown journal event")
            require(index == 1 or event != "RUN_BOUND", "duplicate journal origin")
            require(not closed, "journal event after completion")
            if event in ("RUN_STARTED", "RUN_RESUMED"):
                require(not started, "overlapping run attempts")
                started = True
            if event in ("RUN_STOPPED", "RUN_FAILED", "RUN_INTERRUPTED_RECOVERED"):
                require(started, "run terminal event without start")
                if event == "RUN_INTERRUPTED_RECOVERED":
                    exact_keys(entry["payload"], {"run_identity_sha256"}, "interruption recovery payload")
                    require(entry["payload"]["run_identity_sha256"] == durable.sha256_file(self.identity_path), "interruption recovery identity")
                started = False
            if event in ("TASK_COMMITTED", "TASK_COMMIT_RECOVERED"):
                require(started, "journal task without running attempt")
                task_id = entry["payload"]["task_id"]
                require(task_id not in committed, "duplicate journal task")
                task = next((candidate for candidate in self.tasks if candidate.task_id == task_id), None)
                require(task is not None, "unknown journal task")
                require(entry["payload"]["result_sha256"] == durable.sha256_file(self._task_result_path(task)), "journal task result hash")
                require(entry["payload"]["receipt_sha256"] == durable.sha256_file(self._receipt_path(task)), "journal task receipt hash")
                if event == "TASK_COMMIT_RECOVERED":
                    body = target.load_json(self._task_result_path(task))
                    scientific = dict(body["result"])
                    scientific.pop("resource")
                    require(entry["payload"]["replay_scientific_sha256"] == durable.sha256_bytes(durable.canonical_json_bytes(scientific)), "journal replay hash")
                committed.append(task_id)
            if event in ("RUN_COMPLETE", "RUN_COMPLETE_RECOVERED"):
                require(started and self.complete_path.exists(), "journal completion without durable COMPLETE")
                require(set(committed) == {task.task_id for task in self.tasks}, "journal completion task census")
                closed = True
                started = False
        if completed is not None:
            require(set(committed) == set(completed), "journal/result task census")
        if self.complete_path.exists():
            if closed:
                require(entries[-1]["event"] in ("RUN_COMPLETE", "RUN_COMPLETE_RECOVERED"), "journal completion event")
                require(entries[-1]["payload"]["complete_sha256"] == durable.sha256_file(self.complete_path), "journal COMPLETE hash")
            else:
                require(allow_complete_recovery and started and len(committed) == len(self.tasks), "journal completion event")
        else:
            require(not closed, "journal completion without COMPLETE")
        return started

    def run(self, resume: bool = False, max_inflight: int | None = None) -> Any:
        self.root.mkdir(parents=True, exist_ok=True)
        with (self.root / "OWNER.lock").open("a+b") as lock:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise durable.EvidenceError("checkpoint root already has an active owner") from error
            self.journal.sequence = self.journal._discover_last_sequence()
            try:
                return self._run_locked(resume=resume, max_inflight=max_inflight)
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    def _run_locked(self, resume: bool = False, max_inflight: int | None = None) -> Any:
        self.bind_identity(resume=resume)
        if resume:
            self.recover_unjournaled_results()
        completed = self.load_completed()
        self.verify_journal(completed, allow_complete_recovery=self.complete_path.exists())
        total_work = sum(task.work_units for task in self.tasks)
        completed_work = sum(task.work_units for task in self.tasks if task.task_id in completed)
        if self.complete_path.exists():
            entries = list(self.journal.entries())
            if entries[-1]["event"] not in ("RUN_COMPLETE", "RUN_COMPLETE_RECOVERED"):
                # A power loss after durable COMPLETE but before the journal
                # append is recoverable only after every file/hash is checked.
                self.verify_complete(allow_journal_recovery=True)
                self.journal.append("RUN_COMPLETE_RECOVERED", {"complete_sha256": durable.sha256_file(self.complete_path)})
            self.verify_complete()
            return base.RunOutcome("COMPLETE", len(completed), len(self.tasks), completed_work, total_work, self.complete_path)
        controller = base.StopController()
        controller.install()
        started = time.monotonic()
        pending = [task for task in self.tasks if task.task_id not in completed]
        limit = max_inflight or self.workers
        require(limit >= 1, "max_inflight must be positive")
        self.journal.append("RUN_RESUMED" if resume else "RUN_STARTED", self._progress(completed, started))
        failed: tuple[Any, BaseException] | None = None
        futures: dict[Any, Any] = {}
        next_index = 0
        try:
            with ProcessPoolExecutor(max_workers=self.workers, initializer=base._worker_initializer) as executor:
                while next_index < len(pending) or futures:
                    while not controller.requested.is_set() and failed is None and next_index < len(pending) and len(futures) < limit:
                        task = pending[next_index]
                        next_index += 1
                        context = {
                            "run_id": self.run_id, "branch": self.branch, "phase": self.phase,
                            "task_id": task.task_id, "task_sha256": task.task_sha256,
                            "checkpoint_root": str(self.root), "parameters": self.parameters,
                        }
                        future = executor.submit(
                            base.invoke_kernel, str(self.kernel_module), self.kernel_function,
                            dict(task.payload), context,
                        )
                        futures[future] = task
                    if not futures:
                        break
                    done, _ = wait(list(futures), return_when=FIRST_COMPLETED, timeout=1.0)
                    for future in done:
                        task = futures.pop(future)
                        try:
                            completed[task.task_id] = self._commit_result(task, future.result())
                            progress = self._progress(completed, started)
                            progress.update({
                                "task_id": task.task_id,
                                "result_sha256": durable.sha256_file(self._task_result_path(task)),
                                "receipt_sha256": durable.sha256_file(self._receipt_path(task)),
                            })
                            self.journal.append("TASK_COMMITTED", progress)
                        except BaseException as error:
                            failed = (task, error)
                            controller.requested.set()
        finally:
            controller.restore()
        completed = self.load_completed()
        progress = self._progress(completed, started)
        completed_work = int(progress["completed_work_units"])
        if failed is not None:
            task, error = failed
            self.journal.append("RUN_FAILED", {**progress, "failed_task_id": task.task_id, "error_type": type(error).__name__, "error": str(error)})
            raise RuntimeError(f"task {task.task_id} failed: {error}") from error
        # A signal always stops publication, including when the last in-flight
        # task happened to finish during the graceful wait.
        if controller.requested.is_set():
            self.journal.append("RUN_STOPPED", {**progress, "signal": controller.signal_number})
            return base.RunOutcome("STOPPED", len(completed), len(self.tasks), completed_work, total_work, None)
        require(len(completed) == len(self.tasks), "runtime ended with uncommitted tasks")
        results = [{"task_id": task.task_id, "sha256": durable.sha256_file(self._task_result_path(task))} for task in self.tasks]
        receipts = [{"task_id": task.task_id, "sha256": durable.sha256_file(self._receipt_path(task))} for task in self.tasks]
        complete = {
            "schema": SCHEMA, "run_id": self.run_id, "branch": self.branch, "phase": self.phase,
            "run_identity_sha256": durable.sha256_file(self.identity_path),
            "completed_tasks": len(self.tasks), "total_tasks": len(self.tasks),
            "completed_work_units": total_work, "total_work_units": total_work,
            "result_files": results, "receipt_files": receipts,
            "result_set_sha256": durable.sha256_bytes(durable.canonical_json_bytes(results)),
            "receipt_set_sha256": durable.sha256_bytes(durable.canonical_json_bytes(receipts)),
        }
        durable.immutable_write_json(self.complete_path, complete)
        self.journal.append("RUN_COMPLETE", {"complete_sha256": durable.sha256_file(self.complete_path), **progress})
        self.verify_complete()
        return base.RunOutcome("COMPLETE", len(completed), len(self.tasks), total_work, total_work, self.complete_path)


ACTIVE_POOL: HardenedPool | None = None


def load_task_results(checkpoint_root: Path, tasks: list[Any]) -> list[Any]:
    require(ACTIVE_POOL is not None and ACTIVE_POOL.root == Path(checkpoint_root).resolve(), "active checkpoint binding")
    require(
        [(task.task_id, task.task_sha256, task.work_units) for task in ACTIVE_POOL.tasks]
        == [(task.task_id, task.task_sha256, task.work_units) for task in tasks],
        "task plan binding",
    )
    ACTIVE_POOL.verify_complete()
    completed = ACTIVE_POOL.load_completed()
    return [completed[task.task_id] for task in tasks]


def make_l4_pool(checkpoint_root: Path) -> HardenedPool:
    tasks = [
        base.TaskSpec(
            task_id=f"L04_event00_qout{q:02d}",
            payload={"L": 4, "event": 0, "q_out": q},
            work_units=max(1, math.comb(8, q)),
        )
        for q in range(5)
    ]
    return HardenedPool(
        checkpoint_root=checkpoint_root,
        run_id="L4-L8-TARGET-SCALING-V001-L4-EVENT00",
        branch="target",
        phase="dense-l4-reproduction",
        kernel_module=PACKET / "frozen_kernel_adapter.py",
        kernel_function="sector_kernel",
        tasks=tasks,
        workers=1,
        parameters={
            "schema": "L4_L8_TARGET_SCALING_RUN_PARAMETERS_V001",
            "authorized_lengths": [4],
            "L": 4,
            "events": [0],
            "resolution": "TARGET_V004_FINE",
            "history_sha256": target.HISTORY_HASHES[4],
            "engine_sha256": target.DEPENDENCY_HASHES[str(target.ENGINE_RELATIVE)],
            "kernel_sha256": durable.sha256_file(V001 / "target_lineage_scaling.py"),
            "dense_baseline_sha256": target.DEPENDENCY_HASHES[str(target.DENSE_RESULT_RELATIVE)],
        },
    )


runtime_adapter = SimpleNamespace(
    TaskSpec=base.TaskSpec,
    ResumableProcessPool=HardenedPool,
    load_task_results=load_task_results,
)
