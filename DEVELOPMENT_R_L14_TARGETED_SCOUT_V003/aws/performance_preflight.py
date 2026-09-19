#!/usr/bin/env python3
"""Record observed node geometry as telemetry without gating computation."""

from __future__ import annotations

import os
import platform
import re
import socket
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from durable_evidence import immutable_write_json


CPU_DIRECTORY = re.compile(r"^cpu[0-9]+$")


def integer_env(name: str) -> int:
    try:
        value = int(os.environ[name])
    except (KeyError, ValueError) as error:
        raise RuntimeError("missing or invalid {}".format(name)) from error
    if value < 1:
        raise RuntimeError("{} must be positive".format(name))
    return value


def expanded_cpu_list(raw: str) -> Iterable[int]:
    for item in raw.strip().split(","):
        if "-" in item:
            start, end = (int(value) for value in item.split("-", 1))
            yield from range(start, end + 1)
        elif item:
            yield int(item)


def cpu_topology() -> Tuple[int, int, int]:
    records = []
    for cpu in sorted(Path("/sys/devices/system/cpu").iterdir()):
        if not CPU_DIRECTORY.fullmatch(cpu.name):
            continue
        online = cpu / "online"
        if online.exists() and online.read_text(encoding="utf-8").strip() != "1":
            continue
        topology = cpu / "topology"
        package = int((topology / "physical_package_id").read_text().strip())
        core = int((topology / "core_id").read_text().strip())
        siblings = len(set(expanded_cpu_list((topology / "thread_siblings_list").read_text())))
        records.append((package, core, siblings))
    if not records:
        raise RuntimeError("no online CPU topology records")
    return len(records), len({(package, core) for package, core, _ in records}), max(row[2] for row in records)


def memory_mib() -> int:
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        if line.startswith("MemTotal:"):
            return int(line.split()[1]) // 1024
    raise RuntimeError("MemTotal is absent")


def cpu_identity() -> Tuple[str, set[str]]:
    model = ""
    flags: set[str] = set()
    for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
        if line.startswith("model name") and not model:
            model = line.split(":", 1)[1].strip()
        elif line.startswith("flags") and not flags:
            flags = set(line.split(":", 1)[1].split())
    return model, flags


def mount_record(path: Path) -> Dict[str, Any]:
    resolved = path.resolve()
    for line in Path("/proc/self/mounts").read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if len(fields) >= 3 and fields[1].replace("\\040", " ") == str(resolved):
            stats = os.statvfs(str(resolved))
            return {
                "source": fields[0],
                "filesystem": fields[2],
                "device": os.stat(str(resolved)).st_dev,
                "free_gib": (stats.f_bavail * stats.f_frsize) // (1024 ** 3),
            }
    raise RuntimeError("{} is not an explicit mount".format(resolved))


def main() -> int:
    workers = integer_env("L14_WORKERS")
    expected_cpus = integer_env("L14_EXPECTED_LOGICAL_CPUS")
    expected_cores = integer_env("L14_EXPECTED_PHYSICAL_CORES")
    minimum_memory = integer_env("L14_MIN_MEMORY_MIB")
    branch = os.environ.get("L14_BRANCH", "")
    if branch not in ("target", "hostile"):
        raise RuntimeError("invalid L14_BRANCH")

    logical_cpus, physical_cores, maximum_threads_per_core = cpu_topology()
    observed_memory = memory_mib()
    model, flags = cpu_identity()
    checkpoint = mount_record(Path(os.environ["L14_CHECKPOINT_ROOT"]).parent)
    scratch = mount_record(Path(os.environ["L14_SCRATCH_ROOT"]).parent)
    thread_caps = {
        name: os.environ.get(name)
        for name in (
            "OMP_NUM_THREADS",
            "MKL_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
        )
    }
    checks = {
        "architecture_x86_64": platform.machine() == "x86_64",
        "logical_cpu_count_exact": logical_cpus == expected_cpus,
        "physical_core_count_exact": physical_cores == expected_cores,
        "single_thread_per_core": maximum_threads_per_core == 1,
        "worker_headroom_at_least_8_cores": workers <= physical_cores - 8,
        "memory_minimum": observed_memory >= minimum_memory,
        "amd_epyc_cpu": "AMD EPYC" in model,
        "avx512_available": "avx512f" in flags,
        "thread_caps_equal_one": all(value == "1" for value in thread_caps.values()),
        "dynamic_blas_disabled": os.environ.get("OMP_DYNAMIC") == "FALSE" and os.environ.get("MKL_DYNAMIC") == "FALSE",
        "checkpoint_is_retained_xfs": checkpoint["filesystem"] == "xfs",
        "scratch_is_xfs": scratch["filesystem"] == "xfs",
        "checkpoint_and_scratch_are_distinct": checkpoint["device"] != scratch["device"],
    }
    boot_id = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="utf-8").strip()
    payload = {
        "schema": "L14_NODE_PERFORMANCE_PREFLIGHT_V002",
        "classification": "MATCHES_PLANNED_GEOMETRY" if all(checks.values()) else "ADVISORY_VARIANCE__EXECUTION_CONTINUES",
        "branch": branch,
        "boot_id": boot_id,
        "hostname": socket.gethostname(),
        "workers": workers,
        "cpu": {
            "logical_cpus": logical_cpus,
            "physical_cores": physical_cores,
            "maximum_threads_per_core": maximum_threads_per_core,
            "model": model,
            "avx512f": "avx512f" in flags,
        },
        "memory_mib": observed_memory,
        "thread_caps": thread_caps,
        "checkpoint": checkpoint,
        "scratch": scratch,
        "checks": checks,
    }
    destination = Path(os.environ["L14_CHECKPOINT_ROOT"]) / "NODE_PREFLIGHT_{}_{}.json".format(branch, boot_id)
    immutable_write_json(destination, payload)
    print(
        "L14_NODE_PREFLIGHT classification={} cores={} workers={} memory_mib={} checkpoint_free_gib={} scratch_free_gib={}".format(
            payload["classification"], physical_cores, workers, observed_memory,
            checkpoint["free_gib"], scratch["free_gib"]
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(
            "L14_NODE_PREFLIGHT_ADVISORY type={} message={} execution=CONTINUES".format(
                type(error).__name__, error
            ),
            file=sys.stderr,
            flush=True,
        )
        raise SystemExit(0)
