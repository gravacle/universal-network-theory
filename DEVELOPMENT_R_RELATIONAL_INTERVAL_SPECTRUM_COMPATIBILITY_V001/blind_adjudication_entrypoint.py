#!/usr/bin/env python3
"""Execution-bound entrypoint for the frozen Stage 6 adjudicator.

This wrapper performs no spectrum calculation and changes no classification.
It authenticates every blind row against its owner-once execution credential,
then invokes the already-frozen target adjudicator with the same pinned inputs.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import blind_index_publisher as publisher
from contract_common import Refusal, demand, sha256_file


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
TARGET_DRIVER = (
    ROOT
    / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "interval_spectrum_driver.py"
)
TARGET_DRIVER_SHA256 = (
    "2e8fede6cbfae9444f39d9e329347237915e42282ad9b667cd2631f3c5c8d9ad"
)


def adjudicate(args: argparse.Namespace) -> None:
    demand(
        TARGET_DRIVER.is_file()
        and sha256_file(TARGET_DRIVER) == TARGET_DRIVER_SHA256,
        "frozen target adjudicator custody mismatch",
    )
    publisher.validate_execution_bound_index(
        args.blind_index, args.blind_index_sha256, args.manifest_sha256,
    )
    command = [
        sys.executable,
        "-B",
        str(TARGET_DRIVER),
        "--mode",
        "adjudicate",
        "--manifest",
        str(args.manifest),
        "--manifest-sha256",
        args.manifest_sha256,
        "--target-index",
        str(args.target_index),
        "--target-index-sha256",
        args.target_index_sha256,
        "--blind-index",
        str(args.blind_index),
        "--blind-index-sha256",
        args.blind_index_sha256,
        "--output",
        str(args.output),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    demand(
        completed.returncode == 0,
        "frozen target adjudicator refused: "
        + (completed.stderr or completed.stdout)[-1000:],
    )
    if completed.stdout:
        print(completed.stdout, end="")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--manifest", type=Path, required=True)
    result.add_argument("--manifest-sha256", required=True)
    result.add_argument("--target-index", type=Path, required=True)
    result.add_argument("--target-index-sha256", required=True)
    result.add_argument("--blind-index", type=Path, required=True)
    result.add_argument("--blind-index-sha256", required=True)
    result.add_argument("--output", type=Path, required=True)
    return result


def main() -> int:
    try:
        adjudicate(parser().parse_args())
    except (Refusal, OSError, ValueError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
