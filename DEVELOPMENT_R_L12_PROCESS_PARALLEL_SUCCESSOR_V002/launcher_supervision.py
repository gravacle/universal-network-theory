#!/usr/bin/env python3
"""Independent dual-branch supervision; branch failure never kills its sibling."""

from __future__ import annotations

import os
import selectors
import signal
import subprocess
import sys
from pathlib import Path
from typing import IO, Mapping, Sequence


def branch_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment["PYTHONPYCACHEPREFIX"] = "/tmp/l12-process-v002-pycache"
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        environment[name] = "1"
    return environment


def supervise(
    *,
    commands: Mapping[str, Sequence[str]],
    log_root: Path,
    cwd: Path,
    environment: Mapping[str, str] | None = None,
) -> dict[str, int]:
    """Run all branches to their own terminal state without fail-fast coupling."""
    if not commands or any(not name or not command for name, command in commands.items()):
        raise ValueError("branch commands must be nonempty")
    if log_root.exists() or log_root.is_symlink() or not log_root.is_absolute():
        raise RuntimeError("launcher log root must be a fresh absolute path")
    log_root.mkdir(parents=True, exist_ok=False)
    selector = selectors.DefaultSelector()
    processes: dict[str, subprocess.Popen[str]] = {}
    streams: dict[IO[str], tuple[str, IO[str]]] = {}
    reported_exit: set[str] = set()
    stopping = False

    def external_stop(signum: int, _frame: object) -> None:
        nonlocal stopping
        if stopping:
            return
        stopping = True
        print(
            f"L12_LAUNCH_STOP signal={signum} preserving_workspaces=true",
            flush=True,
        )
        for process in processes.values():
            if process.poll() is None:
                process.send_signal(signal.SIGTERM)

    old_handlers = {
        signum: signal.getsignal(signum) for signum in (signal.SIGINT, signal.SIGTERM)
    }
    for signum in old_handlers:
        signal.signal(signum, external_stop)
    try:
        effective_environment = (
            dict(environment) if environment is not None else branch_environment()
        )
        for name, command in commands.items():
            log = (log_root / f"{name}.log").open("x", encoding="utf-8")
            process = subprocess.Popen(
                list(command),
                cwd=str(cwd),
                env=effective_environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            if process.stdout is None:
                raise RuntimeError("branch stdout pipe was not created")
            processes[name] = process
            streams[process.stdout] = (name, log)
            selector.register(process.stdout, selectors.EVENT_READ)
            print(f"L12_BRANCH_STARTED branch={name} parent_pid={process.pid}", flush=True)
        while streams:
            for key, _events in selector.select(timeout=1.0):
                stream = key.fileobj
                name, log = streams[stream]
                line = stream.readline()
                if line:
                    log.write(line)
                    log.flush()
                    print(f"[{name}] {line}", end="", flush=True)
                else:
                    selector.unregister(stream)
                    stream.close()
                    log.flush()
                    os.fsync(log.fileno())
                    log.close()
                    del streams[stream]
            for name, process in processes.items():
                code = process.poll()
                if code is not None and name not in reported_exit:
                    reported_exit.add(name)
                    live_siblings = sorted(
                        sibling
                        for sibling, candidate in processes.items()
                        if sibling != name and candidate.poll() is None
                    )
                    print(
                        "L12_BRANCH_EXIT "
                        f"branch={name} return_code={code} "
                        f"sibling_continues={bool(live_siblings)} "
                        f"live_siblings={live_siblings}",
                        flush=True,
                    )
        return_codes = {name: process.wait() for name, process in processes.items()}
        print(f"L12_LAUNCH_COMPLETE return_codes={return_codes}", flush=True)
        return return_codes
    finally:
        for signum, handler in old_handlers.items():
            signal.signal(signum, handler)
        for stream, (_name, log) in list(streams.items()):
            try:
                selector.unregister(stream)
            except Exception:
                pass
            stream.close()
            log.close()
        selector.close()

