#!/usr/bin/env python3
"""Small child processes used only to prove independent launcher survival."""

from __future__ import annotations

import argparse
import time


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=("forced_failure", "survivor"))
    arguments = parser.parse_args()
    print(f"L4_FIXTURE_START role={arguments.role}", flush=True)
    if arguments.role == "forced_failure":
        print("L4_FIXTURE_FORCED_FAILURE return_code=7", flush=True)
        return 7
    time.sleep(1.5)
    print("L4_FIXTURE_SURVIVOR_PROGRESS event=4", flush=True)
    print("L4_FIXTURE_SURVIVOR_COMPLETE sibling_failure_did_not_terminate=true", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

