#!/usr/bin/env python3
"""Tiny external process used to prove non-fail-fast supervision."""

import argparse
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--exit-code", type=int, default=0)
    parser.add_argument("--marker", type=Path)
    args = parser.parse_args()
    time.sleep(args.sleep)
    if args.marker:
        args.marker.write_text("survived\n", encoding="utf-8")
    return args.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

