#!/usr/bin/env python3
"""Supervise Target and Hostile without fail-fast sibling termination."""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from durable_evidence import AppendOnlyJournal, EvidenceError, immutable_write_json, load_json


CONFIG_SCHEMA = "L14_INDEPENDENT_LAUNCH_CONFIG_V002"


def next_attempt(log_directory: Path) -> Tuple[int, Path]:
    log_directory.mkdir(parents=True, exist_ok=True)
    indices = []
    for path in log_directory.glob("attempt_*.log"):
        try:
            indices.append(int(path.stem.split("_", 1)[1]))
        except (IndexError, ValueError):
            raise EvidenceError("malformed attempt log: {}".format(path))
    index = max(indices, default=0) + 1
    return index, log_directory / "attempt_{:03d}.log".format(index)


def validate_config(config: Mapping[str, Any]) -> None:
    if config.get("schema") != CONFIG_SCHEMA:
        raise EvidenceError("wrong independent-launch schema")
    branches = config.get("branches")
    if not isinstance(branches, dict) or set(branches) != {"target", "hostile"}:
        raise EvidenceError("config requires exactly target and hostile branches")
    for name, record in branches.items():
        if not isinstance(record, dict):
            raise EvidenceError("malformed {} branch config".format(name))
        command = record.get("command")
        if not isinstance(command, list) or not command or not all(isinstance(token, str) and token for token in command):
            raise EvidenceError("{} command must be a non-empty argument array".format(name))


class ExternalStop:
    def __init__(self) -> None:
        self.signal_number: Optional[int] = None

    def handler(self, signum: int, _frame: Any) -> None:
        self.signal_number = signum


def main(argv: Sequence[str] = ()) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args(argv or sys.argv[1:])
    config = load_json(args.config)
    validate_config(config)
    run_root = Path(config["run_root"]).expanduser().resolve()
    run_root.mkdir(parents=True, exist_ok=True)
    journal = AppendOnlyJournal(run_root / "launcher_journal")

    processes: Dict[str, subprocess.Popen] = {}
    logs: Dict[str, Tuple[Any, Path]] = {}
    for branch in ("target", "hostile"):
        command = config["branches"][branch]["command"]
        attempt, log_path = next_attempt(run_root / "logs" / branch)
        descriptor = os.open(str(log_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
        handle = os.fdopen(descriptor, "w", encoding="utf-8")
        handle.write("L14_BRANCH_COMMAND {}\n".format(json.dumps(command)))
        handle.flush()
        processes[branch] = subprocess.Popen(command, stdout=handle, stderr=subprocess.STDOUT, text=True)
        logs[branch] = (handle, log_path)
        journal.append("BRANCH_STARTED", {"branch": branch, "attempt": attempt, "pid": processes[branch].pid})
        print("L14_LAUNCH branch={} pid={} attempt={}".format(branch, processes[branch].pid, attempt), flush=True)

    stopper = ExternalStop()
    previous = {}
    for signum in (signal.SIGINT, signal.SIGTERM):
        previous[signum] = signal.getsignal(signum)
        signal.signal(signum, stopper.handler)

    exits: Dict[str, int] = {}
    stop_forwarded = False
    try:
        while len(exits) < len(processes):
            for branch, process in processes.items():
                if branch in exits:
                    continue
                return_code = process.poll()
                if return_code is not None:
                    exits[branch] = return_code
                    journal.append("BRANCH_EXITED", {"branch": branch, "return_code": return_code})
                    print("L14_BRANCH_EXIT branch={} return_code={}".format(branch, return_code), flush=True)
                    # Deliberately do not signal the sibling on branch failure.
            if stopper.signal_number is not None and not stop_forwarded:
                stop_forwarded = True
                journal.append("EXTERNAL_STOP_REQUESTED", {"signal": stopper.signal_number})
                for branch, process in processes.items():
                    if branch not in exits and process.poll() is None:
                        process.send_signal(signal.SIGTERM)
                        journal.append("EXTERNAL_STOP_FORWARDED", {"branch": branch, "pid": process.pid})
            if len(exits) < len(processes):
                time.sleep(0.25)
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)
        for branch, (handle, _path) in logs.items():
            handle.write("L14_BRANCH_LOG_CLOSED return_code={}\n".format(exits.get(branch, "unknown")))
            handle.flush()
            os.fsync(handle.fileno())
            os.fchmod(handle.fileno(), 0o444)
            handle.close()

    summary = {
        "schema": "L14_INDEPENDENT_LAUNCH_COMPLETE_V002",
        "run_id": config.get("run_id"),
        "external_stop_signal": stopper.signal_number,
        "branches": {
            branch: {"return_code": exits[branch], "log": str(logs[branch][1])}
            for branch in sorted(exits)
        },
        "all_succeeded": all(code == 0 for code in exits.values()),
        "sibling_failure_policy": "WAIT_FOR_SURVIVING_BRANCH__NO_FAIL_FAST_SIGNAL",
    }
    summary_path = run_root / "LAUNCHER_ATTEMPT_{:08d}.json".format(journal.sequence + 1)
    immutable_write_json(summary_path, summary)
    journal.append("LAUNCHER_EXIT", {"summary": str(summary_path), "all_succeeded": summary["all_succeeded"]})
    return 0 if summary["all_succeeded"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("L14_LAUNCHER_FAILURE type={} message={}".format(type(error).__name__, error), file=sys.stderr, flush=True)
        raise SystemExit(2)

