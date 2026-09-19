#!/usr/bin/env python3
"""Bounded ProcessPool runtime with authenticated task-level resume.

This module provides persistence mechanics only.  It does not weaken, replace,
or infer any physics predicate.  A numerical kernel must return its original
convergence evidence and immutable artifact hashes in every task result.
"""

from __future__ import annotations

import importlib.util
import os
import signal
import sys
import threading
import time
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from durable_evidence import (
    AppendOnlyJournal,
    DurableMirror,
    EvidenceError,
    canonical_json_bytes,
    immutable_write_json,
    load_json,
    sha256_bytes,
    sha256_file,
    validate_artifact,
)


IDENTITY_SCHEMA = "L14_RESUMABLE_RUN_IDENTITY_V002"
RESULT_SCHEMA = "L14_RESUMABLE_TASK_RESULT_V002"
COMPLETE_SCHEMA = "L14_RESUMABLE_RUN_COMPLETE_V002"


class RuntimeConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    payload: Mapping[str, Any]
    work_units: int = 1

    @property
    def task_sha256(self) -> str:
        body = {"task_id": self.task_id, "payload": dict(self.payload), "work_units": self.work_units}
        return sha256_bytes(canonical_json_bytes(body))


@dataclass(frozen=True)
class RunOutcome:
    status: str
    completed: int
    total: int
    completed_work_units: int
    total_work_units: int
    complete_path: Optional[Path]


class StopController:
    def __init__(self) -> None:
        self.requested = threading.Event()
        self.signal_number: Optional[int] = None
        self._previous: Dict[int, Any] = {}

    def _handler(self, signum: int, _frame: Any) -> None:
        self.signal_number = signum
        self.requested.set()

    def install(self) -> None:
        if threading.current_thread() is not threading.main_thread():
            return
        for signum in (signal.SIGINT, signal.SIGTERM):
            self._previous[signum] = signal.getsignal(signum)
            signal.signal(signum, self._handler)

    def restore(self) -> None:
        for signum, handler in self._previous.items():
            signal.signal(signum, handler)
        self._previous.clear()


def _worker_initializer() -> None:
    # Only the parent owns graceful orchestration.  A service-level hard stop can
    # still kill the entire cgroup after the external grace period expires.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)


def _load_module(module_path: str):
    path = Path(module_path).resolve()
    module_name = "l14_kernel_{}".format(sha256_bytes(str(path).encode("utf-8"))[:16])
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeConfigurationError("cannot import kernel module: {}".format(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def invoke_kernel(module_path: str, function_name: str, task_payload: Mapping[str, Any], context: Mapping[str, Any]) -> Any:
    module = _load_module(module_path)
    function = getattr(module, function_name, None)
    if not callable(function):
        raise RuntimeConfigurationError("kernel function is not callable: {}:{}".format(module_path, function_name))
    return function(dict(task_payload), dict(context))


class ResumableProcessPool:
    def __init__(
        self,
        checkpoint_root: Path,
        run_id: str,
        branch: str,
        phase: str,
        kernel_module: Path,
        kernel_function: str,
        tasks: Sequence[TaskSpec],
        workers: int,
        parameters: Mapping[str, Any],
        mirror_destination: Optional[str] = None,
        mirror_artifacts: bool = False,
    ) -> None:
        self.root = Path(checkpoint_root).resolve()
        self.run_id = run_id
        self.branch = branch
        self.phase = phase
        self.kernel_module = Path(kernel_module).resolve()
        self.kernel_function = kernel_function
        self.tasks = list(tasks)
        self.workers = workers
        self.parameters = dict(parameters)
        self.mirror = DurableMirror(mirror_destination)
        self.mirror_artifacts = mirror_artifacts
        self.journal = AppendOnlyJournal(self.root / "journal")
        self.result_root = self.root / "results"
        self.identity_path = self.root / "RUN_IDENTITY.json"
        self.complete_path = self.root / "COMPLETE.json"
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        if self.workers < 1:
            raise RuntimeConfigurationError("workers must be positive")
        if not self.kernel_module.is_file():
            raise RuntimeConfigurationError("missing kernel module: {}".format(self.kernel_module))
        seen = set()
        for task in self.tasks:
            if not task.task_id or any(character not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-" for character in task.task_id):
                raise RuntimeConfigurationError("unsafe task id: {!r}".format(task.task_id))
            if task.task_id in seen:
                raise RuntimeConfigurationError("duplicate task id: {}".format(task.task_id))
            if task.work_units < 1:
                raise RuntimeConfigurationError("non-positive work units: {}".format(task.task_id))
            seen.add(task.task_id)

    def _identity_payload(self) -> Dict[str, Any]:
        return {
            "schema": IDENTITY_SCHEMA,
            "run_id": self.run_id,
            "branch": self.branch,
            "phase": self.phase,
            "kernel": {
                "path": str(self.kernel_module),
                "sha256": sha256_file(self.kernel_module),
                "function": self.kernel_function,
            },
            "parameters": self.parameters,
            "tasks": [
                {"task_id": task.task_id, "task_sha256": task.task_sha256, "work_units": task.work_units}
                for task in self.tasks
            ],
        }

    def bind_identity(self, resume: bool) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        expected = self._identity_payload()
        if self.identity_path.exists():
            actual = load_json(self.identity_path)
            if actual != expected:
                raise EvidenceError("resume identity mismatch at {}".format(self.identity_path))
            if not resume and not self.complete_path.exists():
                raise EvidenceError("checkpoint already exists; explicit --resume is required")
        else:
            if resume:
                raise EvidenceError("cannot resume without RUN_IDENTITY.json")
            immutable_write_json(self.identity_path, expected)
            self.mirror.publish(self.identity_path, "RUN_IDENTITY.json")
            self.journal.append("RUN_BOUND", {"identity_sha256": sha256_file(self.identity_path)})

    def _task_result_path(self, task: TaskSpec) -> Path:
        return self.result_root / "{}.json".format(task.task_id)

    def _validate_artifact_record(self, record: Mapping[str, Any]) -> None:
        raw_path = record.get("path")
        raw_digest = record.get("sha256")
        raw_bytes = record.get("bytes")
        if not isinstance(raw_path, str) or not isinstance(raw_digest, str):
            raise EvidenceError("artifact record requires path and sha256")
        path = Path(raw_path).resolve()
        try:
            path.relative_to(self.root)
        except ValueError:
            raise EvidenceError("committed artifact must be beneath checkpoint root: {}".format(path))
        validate_artifact(path, raw_digest, int(raw_bytes) if raw_bytes is not None else None)

    def _validate_result_payload(self, task: TaskSpec, body: Mapping[str, Any]) -> Any:
        if body.get("schema") != RESULT_SCHEMA:
            raise EvidenceError("wrong task-result schema for {}".format(task.task_id))
        if body.get("task_id") != task.task_id or body.get("task_sha256") != task.task_sha256:
            raise EvidenceError("task-result identity mismatch for {}".format(task.task_id))
        result = body.get("result")
        if not isinstance(result, dict):
            raise EvidenceError("kernel result must be a JSON object for {}".format(task.task_id))
        artifacts = result.get("artifacts", [])
        if not isinstance(artifacts, list):
            raise EvidenceError("artifacts must be a list for {}".format(task.task_id))
        for record in artifacts:
            if not isinstance(record, dict):
                raise EvidenceError("malformed artifact record for {}".format(task.task_id))
            self._validate_artifact_record(record)
        return result

    def load_completed(self) -> Dict[str, Any]:
        completed: Dict[str, Any] = {}
        for task in self.tasks:
            path = self._task_result_path(task)
            if not path.exists():
                continue
            result = self._validate_result_payload(task, load_json(path))
            completed[task.task_id] = result
        return completed

    def _commit_result(self, task: TaskSpec, result: Any) -> Any:
        if not isinstance(result, dict):
            raise EvidenceError("kernel result is not a JSON object for {}".format(task.task_id))
        body = {
            "schema": RESULT_SCHEMA,
            "run_id": self.run_id,
            "branch": self.branch,
            "phase": self.phase,
            "task_id": task.task_id,
            "task_sha256": task.task_sha256,
            "work_units": task.work_units,
            "result": result,
        }
        path = self._task_result_path(task)
        immutable_write_json(path, body)
        validated = self._validate_result_payload(task, load_json(path))
        if self.mirror_artifacts:
            for record in validated.get("artifacts", []):
                artifact_path = Path(record["path"]).resolve()
                relative = artifact_path.relative_to(self.root)
                self.mirror.publish(artifact_path, relative.as_posix())
        self.mirror.publish(path, path.relative_to(self.root).as_posix())
        return validated

    def _progress(self, completed: Mapping[str, Any], started_at: float) -> Dict[str, Any]:
        task_index = {task.task_id: task for task in self.tasks}
        completed_work = sum(task_index[task_id].work_units for task_id in completed)
        total_work = sum(task.work_units for task in self.tasks)
        elapsed = max(0.0, time.monotonic() - started_at)
        velocity = completed_work / elapsed if elapsed > 0.0 else 0.0
        eta = (total_work - completed_work) / velocity if velocity > 0.0 else None
        return {
            "completed_tasks": len(completed),
            "total_tasks": len(self.tasks),
            "completed_work_units": completed_work,
            "total_work_units": total_work,
            "elapsed_seconds": elapsed,
            "work_units_per_second": velocity,
            "eta_seconds": eta,
        }

    def run(self, resume: bool = False, max_inflight: Optional[int] = None) -> RunOutcome:
        self.bind_identity(resume=resume)
        completed = self.load_completed()
        total_work = sum(task.work_units for task in self.tasks)
        task_index = {task.task_id: task for task in self.tasks}
        completed_work = sum(task_index[task_id].work_units for task_id in completed)

        if self.complete_path.exists():
            complete = load_json(self.complete_path)
            if complete.get("schema") != COMPLETE_SCHEMA or complete.get("completed_tasks") != len(self.tasks):
                raise EvidenceError("invalid COMPLETE.json")
            return RunOutcome("COMPLETE", len(completed), len(self.tasks), completed_work, total_work, self.complete_path)

        controller = StopController()
        controller.install()
        started_at = time.monotonic()
        pending = [task for task in self.tasks if task.task_id not in completed]
        inflight_limit = max_inflight or self.workers
        if inflight_limit < 1:
            raise RuntimeConfigurationError("max_inflight must be positive")
        self.journal.append("RUN_STARTED" if not resume else "RUN_RESUMED", self._progress(completed, started_at))

        failed: Optional[Tuple[TaskSpec, BaseException]] = None
        futures: Dict[Future, TaskSpec] = {}
        next_index = 0
        try:
            with ProcessPoolExecutor(max_workers=self.workers, initializer=_worker_initializer) as executor:
                while next_index < len(pending) or futures:
                    while (
                        not controller.requested.is_set()
                        and failed is None
                        and next_index < len(pending)
                        and len(futures) < inflight_limit
                    ):
                        task = pending[next_index]
                        next_index += 1
                        context = {
                            "run_id": self.run_id,
                            "branch": self.branch,
                            "phase": self.phase,
                            "task_id": task.task_id,
                            "task_sha256": task.task_sha256,
                            "checkpoint_root": str(self.root),
                            "parameters": self.parameters,
                        }
                        future = executor.submit(
                            invoke_kernel,
                            str(self.kernel_module),
                            self.kernel_function,
                            dict(task.payload),
                            context,
                        )
                        futures[future] = task

                    if not futures:
                        break
                    done, _not_done = wait(list(futures), return_when=FIRST_COMPLETED, timeout=1.0)
                    if not done:
                        continue
                    for future in done:
                        task = futures.pop(future)
                        try:
                            completed[task.task_id] = self._commit_result(task, future.result())
                            progress = self._progress(completed, started_at)
                            progress["task_id"] = task.task_id
                            self.journal.append("TASK_COMMITTED", progress)
                            print(
                                "L14_PROGRESS branch={} phase={} tasks={}/{} work={}/{} eta_seconds={}".format(
                                    self.branch,
                                    self.phase,
                                    progress["completed_tasks"],
                                    progress["total_tasks"],
                                    progress["completed_work_units"],
                                    progress["total_work_units"],
                                    "unknown" if progress["eta_seconds"] is None else "{:.3f}".format(progress["eta_seconds"]),
                                ),
                                flush=True,
                            )
                        except BaseException as error:  # preserve every completed sibling before surfacing failure
                            failed = (task, error)
                            controller.requested.set()
                # Context manager waits for already-running tasks.  They are not
                # killed because a sibling task failed or because TERM requested
                # a graceful checkpoint stop.
        finally:
            controller.restore()

        completed = self.load_completed()
        progress = self._progress(completed, started_at)
        completed_work = int(progress["completed_work_units"])
        if failed is not None:
            task, error = failed
            self.journal.append(
                "RUN_FAILED",
                {**progress, "failed_task_id": task.task_id, "error_type": type(error).__name__, "error": str(error)},
            )
            raise RuntimeError("task {} failed: {}".format(task.task_id, error)) from error

        if controller.requested.is_set() and len(completed) < len(self.tasks):
            self.journal.append("RUN_STOPPED", {**progress, "signal": controller.signal_number})
            return RunOutcome("STOPPED", len(completed), len(self.tasks), completed_work, total_work, None)

        if len(completed) != len(self.tasks):
            self.journal.append("RUN_INCOMPLETE", progress)
            raise EvidenceError("runtime ended with uncommitted tasks")

        ordered_result_hashes = []
        for task in self.tasks:
            path = self._task_result_path(task)
            ordered_result_hashes.append({"task_id": task.task_id, "sha256": sha256_file(path)})
        complete_payload = {
            "schema": COMPLETE_SCHEMA,
            "run_id": self.run_id,
            "branch": self.branch,
            "phase": self.phase,
            "completed_tasks": len(self.tasks),
            "total_tasks": len(self.tasks),
            "completed_work_units": total_work,
            "total_work_units": total_work,
            "result_files": ordered_result_hashes,
            "result_set_sha256": sha256_bytes(canonical_json_bytes(ordered_result_hashes)),
        }
        immutable_write_json(self.complete_path, complete_payload)
        self.mirror.publish(self.complete_path, "COMPLETE.json")
        self.journal.append("RUN_COMPLETE", {"complete_sha256": sha256_file(self.complete_path), **progress})
        return RunOutcome("COMPLETE", len(completed), len(self.tasks), total_work, total_work, self.complete_path)


def load_task_results(checkpoint_root: Path, tasks: Sequence[TaskSpec]) -> List[Any]:
    root = Path(checkpoint_root)
    results = []
    for task in tasks:
        body = load_json(root / "results" / "{}.json".format(task.task_id))
        if body.get("schema") != RESULT_SCHEMA or body.get("task_sha256") != task.task_sha256:
            raise EvidenceError("invalid committed task result: {}".format(task.task_id))
        results.append(body["result"])
    return results
