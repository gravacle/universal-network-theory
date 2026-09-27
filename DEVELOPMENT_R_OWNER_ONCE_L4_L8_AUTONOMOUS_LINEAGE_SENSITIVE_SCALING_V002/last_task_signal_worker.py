#!/usr/bin/env python3
"""Test-only L4 worker: hold q4 open to test a final-in-flight SIGTERM."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import hardened_runtime as hard


def fixture_pool(checkpoint_root: Path) -> hard.HardenedPool:
    pool = hard.make_l4_pool(checkpoint_root)
    pool.kernel_module = Path(__file__).resolve().parent / "slow_kernel_fixture.py"
    pool.parameters["kernel_sha256"] = hard.durable.sha256_file(pool.kernel_module)
    return pool


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-root", required=True, type=Path)
    parser.add_argument("--final-marker", type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    outcome = fixture_pool(args.checkpoint_root).run(resume=args.resume)
    if outcome.status == "COMPLETE" and args.final_marker is not None:
        hard.durable.immutable_write_json(
            args.final_marker,
            {"schema": "L4_FINAL_PUBLICATION_FIXTURE_V001", "checkpoint_complete_sha256": hard.durable.sha256_file(outcome.complete_path)},
        )
    print(f"FIXTURE_OUTCOME {outcome.status} {outcome.completed}/{outcome.total}", flush=True)
    return 75 if outcome.status == "STOPPED" else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (hard.durable.EvidenceError, hard.target.ScalingError, RuntimeError, ValueError) as error:
        print(f"FIXTURE_ERROR {error}", file=sys.stderr, flush=True)
        raise SystemExit(1)
