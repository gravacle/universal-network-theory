#!/usr/bin/env python3
"""Run the source-freeze census repair through Stage 6, never Stage 7."""

from __future__ import annotations

import argparse
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
SOURCE_FREEZE = HERE / "SOURCE_FREEZE_STAGE6R1.json"
PRE_OUTPUT_FREEZE = HERE / "PRE_OUTPUT_FREEZE_STAGE6R1.json"
EXECUTION_RECORD = HERE / "STAGE6R1_EXECUTION_RECORD.json"
STAGE5R1_DIR = ROOT / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003_STAGE5R1"
STAGE5R1_EXECUTION = STAGE5R1_DIR / "STAGE5R1_EXECUTION_RECORD.json"
STAGE5R1_FREEZE = STAGE5R1_DIR / "PRE_OUTPUT_FREEZE_STAGE5R1.json"
COMPATIBILITY = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001"
SPECTRUM = ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
FAILED_BLIND_RUN = COMPATIBILITY / "RUN_V002_L12_V003R1"
FAILED_PLAN = FAILED_BLIND_RUN / "SECTOR_PLAN.json"
BLIND_RUN = COMPATIBILITY / "RUN_V002_L12_V003R1_STAGE6R1"
TARGET_RUN = SPECTRUM / "RUN_V002_L12_V003R1_STAGE6R1"
FINAL_RESULT = SPECTRUM / "ADJUDICATION_V002_L12_V003R1_STAGE6R1.json"

EXPECTED = {
    "manifest": "292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a",
    "stage5r1_execution": "52391568ac35cdb96e524205a65bc6b34b38e89ba1b4bf342caa7b5b997db9b6",
    "stage5r1_freeze": "2af41eadfef1acd168ca766a1ff071c4a81fe9c08d96a021dbf5f54bb4638256",
    "failed_plan": "8118cc0b7ec8b5a121ec92a9d29771edfeed2bb63ec6e227b0786fd523e3ec08",
}


class Stage6R1Refusal(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise Stage6R1Refusal(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            value.update(chunk)
    return value.hexdigest()


def load_base() -> Any:
    specification = importlib.util.spec_from_file_location(
        "frozen_v003_continuation_for_stage6r1", BASE_CONTINUATION
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
        with temporary.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-sha256", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
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
        demand(sha256(PRE_OUTPUT_FREEZE) == args.freeze_sha256,
               "Stage6R1 pre-output freeze hash mismatch")
        demand(sha256(base.MANIFEST) == EXPECTED["manifest"],
               "Stage 5 manifest hash mismatch")
        demand(sha256(STAGE5R1_EXECUTION) == EXPECTED["stage5r1_execution"],
               "Stage5R1 execution hash mismatch")
        demand(sha256(STAGE5R1_FREEZE) == EXPECTED["stage5r1_freeze"],
               "Stage5R1 pre-output freeze hash mismatch")
        demand(sha256(FAILED_PLAN) == EXPECTED["failed_plan"],
               "preserved failed sector plan hash mismatch")
        demand(not (FAILED_BLIND_RUN / "BLIND_METHOD_FREEZE.json").exists(),
               "failed allocation contains a runnable blind freeze")
        failed_rows = FAILED_BLIND_RUN / "RAW"
        demand(not failed_rows.exists()
               or (failed_rows.is_dir() and not any(failed_rows.iterdir())),
               "failed allocation contains physical blind rows")
        failed_credentials = FAILED_BLIND_RUN / "AUTHORIZATION"
        demand(not failed_credentials.exists()
               or (failed_credentials.is_dir()
                   and not any(failed_credentials.iterdir())),
               "failed allocation contains execution credentials")
        demand(not any(path.exists() for path in (
            BLIND_RUN, TARGET_RUN, FINAL_RESULT, EXECUTION_RECORD,
        )), "Stage6R1 allocation is not fresh")

        base.SOURCE_FREEZE = SOURCE_FREEZE
        base.BLIND_RUN = BLIND_RUN
        base.TARGET_RUN = TARGET_RUN
        base.PLAN = BLIND_RUN / "SECTOR_PLAN.json"
        base.BLIND_FREEZE = BLIND_RUN / "BLIND_METHOD_FREEZE.json"
        base.BLIND_ROWS = BLIND_RUN / "RAW"
        base.BLIND_CREDENTIALS = BLIND_RUN / "AUTHORIZATION"
        base.BLIND_INDEX = BLIND_RUN / "SPECTRUM_INDEX.json"
        base.TARGET_INDEX = TARGET_RUN / "SPECTRUM_INDEX.json"
        base.FINAL_RESULT = FINAL_RESULT

        base.stage6()
        result = json.loads(FINAL_RESULT.read_text(encoding="utf-8"))
        write_new_atomic(EXECUTION_RECORD, {
            "schema": "L12_V003R1_STAGE6R1_EXECUTION_RECORD_V001",
            "status": "COMPLETE__PAUSED_BEFORE_STAGE7",
            "stage5_manifest_sha256": sha256(base.MANIFEST),
            "stage5r1_execution_record_sha256": sha256(STAGE5R1_EXECUTION),
            "stage6r1_pre_output_freeze_sha256": sha256(PRE_OUTPUT_FREEZE),
            "stage6r1_source_freeze_sha256": sha256(SOURCE_FREEZE),
            "failed_stage6_plan_sha256": sha256(FAILED_PLAN),
            "stage6_blind_plan_sha256": sha256(base.PLAN),
            "stage6_blind_method_freeze_sha256": sha256(base.BLIND_FREEZE),
            "stage6_blind_index_sha256": sha256(base.BLIND_INDEX),
            "stage6_target_index_sha256": sha256(base.TARGET_INDEX),
            "stage6_result_sha256": sha256(FINAL_RESULT),
            "stage6_status": result.get("status"),
            "stage6_classification": result.get("classification"),
            "stage7_started": False,
        })
    except (Exception, MemoryError, KeyboardInterrupt) as error:
        print(f"STAGE6R1_REFUSED {type(error).__name__}:{error}",
              file=sys.stderr, flush=True)
        return 2
    print("STAGE6R1_COMPLETE__PAUSED_BEFORE_STAGE7", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
