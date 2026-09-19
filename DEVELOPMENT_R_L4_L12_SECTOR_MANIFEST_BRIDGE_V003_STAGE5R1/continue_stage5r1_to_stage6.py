#!/usr/bin/env python3
"""Owner-once Stage5R1 continuation through Stage 6, never Stage 7."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE_CONTINUATION = (
    ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V003/continue_to_stage6.py"
)
STAGE5R1 = HERE / "build_manifest_stage5r1.py"
STAGE5R1_FREEZE = HERE / "PRE_OUTPUT_FREEZE_STAGE5R1.json"
STAGE5R1_EXECUTION = HERE / "STAGE5R1_EXECUTION_RECORD.json"
STAGE4R1_EXECUTION = (
    ROOT / "AUDIT_R_L12_NUMERICAL_REPAIR_V003_STAGE4R1/STAGE4R1_EXECUTION_RECORD.json"
)
CONTINUATION_RECORD = HERE / "STAGE5R1_TO_STAGE6_EXECUTION_RECORD.json"


class ContinuationR1Refusal(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise ContinuationR1Refusal(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            value.update(chunk)
    return value.hexdigest()


def load_base() -> Any:
    specification = importlib.util.spec_from_file_location(
        "frozen_v003_continuation_for_stage5r1", BASE_CONTINUATION
    )
    demand(specification is not None and specification.loader is not None,
           "cannot load frozen V003 continuation")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def write_new_atomic(path: Path, value: object) -> None:
    demand(not path.exists(), f"refusing overwrite: {path}")
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    try:
        with temporary.open("x") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    base = load_base()

    def stop(_signum: int, _frame: Any) -> None:
        base.terminate_wave([
            ((0, 0), process, time.monotonic())
            for process in list(base.ACTIVE_CHILDREN)
        ])
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        demand(base.STAGE4_BLIND.is_file()
               and base.STAGE4_RESULT.is_file()
               and STAGE4R1_EXECUTION.is_file(),
               "authenticated Stage4R1 inputs absent")
        demand(not any(path.exists() for path in (
            base.MANIFEST,
            STAGE5R1_EXECUTION,
            base.BLIND_RUN,
            base.TARGET_RUN,
            base.FINAL_RESULT,
            CONTINUATION_RECORD,
        )), "Stage5R1 downstream allocation is not fresh")
        base.run_checked([
            sys.executable,
            "-B",
            str(STAGE5R1),
            "--stage5r1-freeze-sha256",
            sha256(STAGE5R1_FREEZE),
            "--v003-freeze-sha256",
            sha256(base.STAGE5_FREEZE),
            "--authorization",
            base.MANIFEST_TOKEN,
        ], "Stage 5 V003R1 Stage5R1 sector construction")
        demand(STAGE5R1_EXECUTION.is_file(), "Stage5R1 execution record absent")
        print("STAGE5R1_AUTHENTICATED", flush=True)
        base.stage6()
        result = json.loads(base.FINAL_RESULT.read_text())
        write_new_atomic(CONTINUATION_RECORD, {
            "schema": "L12_V003R1_STAGE5R1_TO_STAGE6_EXECUTION_RECORD_V001",
            "status": "COMPLETE__PAUSED_BEFORE_STAGE7",
            "stage4r1_execution_record_sha256": sha256(STAGE4R1_EXECUTION),
            "stage5r1_execution_record_sha256": sha256(STAGE5R1_EXECUTION),
            "stage5_manifest_sha256": sha256(base.MANIFEST),
            "stage6_blind_index_sha256": sha256(base.BLIND_INDEX),
            "stage6_target_index_sha256": sha256(base.TARGET_INDEX),
            "stage6_result_sha256": sha256(base.FINAL_RESULT),
            "stage6_status": result.get("status"),
            "stage6_classification": result.get("classification"),
            "stage7_started": False,
        })
    except (Exception, MemoryError, KeyboardInterrupt) as error:
        print(f"STAGE5R1_TO_STAGE6_REFUSED {type(error).__name__}:{error}",
              file=sys.stderr, flush=True)
        return 2
    print("STAGE5R1_TO_STAGE6_COMPLETE__PAUSED_BEFORE_STAGE7", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
