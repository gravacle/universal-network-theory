#!/usr/bin/env python3
"""Persistent, cross-restart runtime advisory stored on retained EBS.

This observer never stops the branch or the instance.  The configured minute is
an estimate checkpoint: crossing it creates durable evidence and execution
continues until the numerical program finishes or an operator intervenes.
"""

import argparse
import json
import os
import time
from pathlib import Path


def record_minutes_through(root, boot_id, minute):
    """Account for every elapsed whole minute in this boot, even after timer delay."""

    root.mkdir(parents=True, exist_ok=True)
    for elapsed_minute in range(1, minute + 1):
        record = root / "{}__{:08d}.json".format(boot_id, elapsed_minute)
        if record.exists():
            continue
        temporary = record.with_name(".{}-{}".format(record.name, os.getpid()))
        data = json.dumps(
            {
                "schema": "L14_BILLED_MINUTE_V002",
                "boot_id": boot_id,
                "monotonic_minute": elapsed_minute,
            },
            sort_keys=True,
        ).encode("utf-8") + b"\n"
        descriptor = os.open(str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
        try:
            offset = 0
            while offset < len(data):
                written = os.write(descriptor, data[offset:])
                if written <= 0:
                    raise RuntimeError("runtime-ledger write made no progress")
                offset += written
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        try:
            os.link(str(temporary), str(record))
        except FileExistsError:
            pass
        finally:
            temporary.unlink(missing_ok=True)
    return len(list(root.glob("*.json")))


def decide_action(consumed, advisory_at):
    if consumed >= advisory_at:
        return "ADVISORY_CONTINUE"
    return "CONTINUE"


def record_advisory(root, consumed, advisory_at):
    """Create the owner-once threshold warning on the retained checkpoint disk."""

    root.mkdir(parents=True, exist_ok=True)
    destination = root / "RUNTIME_ADVISORY_{:08d}.json".format(advisory_at)
    if destination.exists():
        return destination
    temporary = destination.with_name(".{}-{}".format(destination.name, os.getpid()))
    data = json.dumps(
        {
            "schema": "L14_RUNTIME_ADVISORY_V003",
            "classification": "ADVISORY_ONLY__EXECUTION_CONTINUES",
            "advisory_minutes": advisory_at,
            "first_observed_consumed_minutes": consumed,
        },
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    descriptor = os.open(str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        offset = 0
        while offset < len(data):
            written = os.write(descriptor, data[offset:])
            if written <= 0:
                raise RuntimeError("runtime-advisory write made no progress")
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    try:
        os.link(str(temporary), str(destination))
    except FileExistsError:
        pass
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    root = Path(os.environ["L14_CHECKPOINT_ROOT"]) / "runtime_ledger"
    boot_id = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="utf-8").strip()
    minute = int(time.monotonic() // 60)
    consumed = record_minutes_through(root, boot_id, minute)
    advisory_at = int(os.environ["L14_RUNTIME_ADVISORY_MINUTES"])
    if advisory_at < 1:
        raise RuntimeError("L14_RUNTIME_ADVISORY_MINUTES must be positive")
    action = decide_action(consumed, advisory_at)
    advisory_path = None
    if action == "ADVISORY_CONTINUE":
        advisory_path = record_advisory(
            Path(os.environ["L14_CHECKPOINT_ROOT"]) / "runtime_advisories",
            consumed,
            advisory_at,
        )
    print(
        "L14_RUNTIME_ADVISORY consumed_minutes={} advisory_minutes={} action={} evidence={}".format(
            consumed,
            advisory_at,
            action,
            advisory_path or "none",
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
