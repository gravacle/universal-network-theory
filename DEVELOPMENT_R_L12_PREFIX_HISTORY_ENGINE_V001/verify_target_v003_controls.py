#!/usr/bin/env python3
"""Adjudicate the terminal-streamed, whole-workset-capped target controls."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SEALED = ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "METHOD_VALIDATION"
HASHES = {
    4: "6c89ba97c389b6755b81fe305949d044ffecc4f7ebe4256fb305d0e608435759",
    6: "131524c51fe72e9506fe320f339c6b50068955d8c6bbd55e1d915c6c080d10b2",
    8: "2b492cd026c5d7592e4b125b69db4c1b5ed0c8bbd0052b11fb79c8d8d777f981",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks = []
    report = {}
    for length, expected_hash in HASHES.items():
        path = HERE / "CONTROL_HISTORY" / f"TARGET_V003_L{length}.json"
        checks.append((digest(path) == expected_hash, f"L{length} target V003 hash"))
        new = json.loads(path.read_text())
        old = json.loads((SEALED / f"STREAMED_HISTORY_L{length}.json").read_text())
        numeric = 0.0
        sector = 0.0
        for a, b in zip(new["rows"], old["rows"]):
            for key, value in b.items():
                if key in ("actual_solver", "null_solver", "sector_weights"):
                    continue
                if isinstance(value, (int, float)) and isinstance(a.get(key), (int, float)):
                    numeric = max(numeric, abs(float(a[key]) - float(value)))
            sector = max(sector, float(np.max(np.abs(
                np.asarray(a["sector_weights"]) - np.asarray(b["sector_weights"])
            ))))
        terminal = new["rows"][-1]
        checks.extend((
            (new["comparison"]["resolved"] is True, f"L{length} resolved"),
            (numeric <= 1e-8, f"L{length} numeric agreement"),
            (sector <= 1e-8, f"L{length} sector agreement"),
            (terminal["terminal_children_streamed"] is True, f"L{length} terminal stream"),
            (all(not row["terminal_children_streamed"] for row in new["rows"][:-1]),
             f"L{length} terminal only at final event"),
            (terminal["actual_solver"]["maximum_live_bytes"] <= 1_000_000_000,
             f"L{length} actual workset cap"),
            (terminal["null_solver"]["maximum_live_bytes"] <= 1_000_000_000,
             f"L{length} null workset cap"),
        ))
        report[str(length)] = {
            "numeric_linf": numeric,
            "sector_linf": sector,
            "terminal_actual_maximum_live_bytes": terminal["actual_solver"]["maximum_live_bytes"],
            "terminal_null_maximum_live_bytes": terminal["null_solver"]["maximum_live_bytes"],
            "wall_seconds": new["wall_seconds"],
            "peak_rss_bytes": new["peak_rss_bytes"],
        }
    failures = [label for passed, label in checks if not passed]
    result = {
        "schema": "R_PREFIX_HISTORY_TARGET_V003_CONTROL_GATE",
        "classification": ("PASS_TARGET_V003_TERMINAL_STREAM_CONTROLS_L4_L8__HOSTILE_V002_REQUIRED"
                           if not failures else "FAIL_TARGET_V003_CONTROLS"),
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failures": failures,
        "controls": report,
        "next_gate": "HOSTILE_LOW_MEMORY_CONTROLS_THEN_CROSS_GATE",
        "claim_boundary": "TARGET_EXECUTABLE_CONTROLS_ONLY__NO_L10_L12_SPECTRUM_Z1_OR_GRAVITY",
    }
    output = HERE / "TARGET_V003_CONTROL_GATE.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["classification"])
    print(f"checks {result['checks_passed']}/{result['checks_total']}")
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
